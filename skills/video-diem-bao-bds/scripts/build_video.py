#!/usr/bin/env python3
"""Dựng video dọc 9:16 cho kênh TRUNG - BUÔN CHUYỆN BĐS từ một file spec JSON.

Dùng:
  python3 build_video.py spec.json                  # xuất MP4
  python3 build_video.py spec.json --preview 3 20   # chỉ chụp khung hình tại giây 3 và 20 (kiểm tra bố cục)

Cần: ffmpeg, Google Chrome hoặc Chromium, Python playwright (pip install playwright --break-system-packages).
Xem examples/knight-frank.json để biết cấu trúc spec.
"""
import os
import base64, json, os, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
import sys as _s; _s.path.insert(0, str(HERE))
from moitruong import add_fonts, launch_browser, has_rubberband
FPS = 30
W, H = 1080, 1920


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def duration(path):
    out = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]).stdout
    return float(out.strip())


def line_timings(voice, texts, breaks=None):
    """Tìm khoảng nghỉ giữa các câu trong giọng đọc để biết mỗi câu bắt đầu/kết thúc lúc nào.
    Chọn n-1 khoảng lặng vừa dài vừa nằm gần vị trí dự kiến (theo tỷ lệ số ký tự của từng câu)."""
    n_lines = len(texts)
    total = duration(voice)
    # Giọng đọc năng lượng cao nghỉ rất ngắn giữa câu: dò khoảng lặng dài trước, thiếu thì hạ dần ngưỡng.
    for dmin in ((0.1,) if breaks else (0.3, 0.22, 0.15, 0.1)):
        err = sh(["ffmpeg", "-i", str(voice), "-af", f"silencedetect=n=-35dB:d={dmin}", "-f", "null", "-"]).stderr
        starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
        ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
        sil = list(zip(starts, ends))
        lead = 0.0
        if sil and sil[0][0] < 0.05:          # khoảng lặng đầu file
            lead = sil[0][1]; sil = sil[1:]
        sil = [x for x in sil if x[1] < total - 0.05]   # bỏ khoảng lặng cuối file
        if len(sil) >= n_lines - 1:
            break
    if len(sil) < n_lines - 1:
        sys.exit(f"Chỉ tìm thấy {len(sil)} khoảng nghỉ cho {n_lines} câu. Tạo lại giọng đọc với [pause] giữa các câu.")
    if breaks:
        # Mốc ngắt câu chỉnh tay (giây trong file giọng gốc): lấy khoảng lặng gần mỗi mốc nhất.
        gaps = [min(sil, key=lambda x: abs(x[0] - t)) for t in breaks]
        bounds, cur = [], lead
        for s0, e0 in gaps:
            bounds.append((cur, s0)); cur = e0
        bounds.append((cur, total))
        return bounds, total
    # Quy hoạch động: chọn n-1 khoảng lặng theo thứ tự sao cho
    #  (1) khoảng lặng càng dài càng tốt ([pause] giữa câu thường dài hơn dấu phẩy),
    #  (2) thời lượng mỗi câu khớp với số ký tự của câu đó (tốc độ đọc trung bình của cả bài).
    lens = [len(t) for t in texts]
    speech = total - lead
    rate = speech / sum(lens)
    m, k = len(sil), n_lines - 1
    pts = [lead] + [s for s, _ in sil]          # điểm kết thúc câu = đầu khoảng lặng
    nxt = [lead] + [e for _, e in sil]          # câu sau bắt đầu ở cuối khoảng lặng
    import math
    def dev(d, exp_d):
        # lệch tuyến tính + phạt nặng câu bị nén/kéo quá mức (tỷ lệ log bình phương)
        r = max(d, 0.2) / exp_d
        return abs(d - exp_d) / exp_d + LW * math.log(r) ** 2
    def cost_line(i, a, b):
        d = pts[b] - nxt[a] if b > 0 else 0
        exp_d = lens[i] * rate
        return dev(d, exp_d)
    INF = float("-inf")
    GW, DW = float(os.environ.get("GW", 4.0)), float(os.environ.get("DW", 1.5))
    LW = float(os.environ.get("LW", 0.0))
    best = [[INF] * (m + 1) for _ in range(k + 1)]
    prev = [[None] * (m + 1) for _ in range(k + 1)]
    best[0][0] = 0.0
    for i in range(1, k + 1):
        for j in range(i, m + 1):
            s, e = sil[j - 1]
            for jj in range(i - 1, j):
                if best[i - 1][jj] == INF:
                    continue
                sc = best[i - 1][jj] + GW * (e - s) - DW * cost_line(i - 1, jj, j)
                if sc > best[i][j]:
                    best[i][j], prev[i][j] = sc, jj
    # câu cuối: từ khoảng lặng đã chọn tới hết file
    j = max(range(k, m + 1), key=lambda x: best[k][x] - DW * dev(total - nxt[x], lens[-1] * rate)
            if best[k][x] > INF else INF)
    picked = []
    for i in range(k, 0, -1):
        picked.append(sil[j - 1]); j = prev[i][j]
    gaps = sorted(picked)
    bounds, cur = [], lead
    for s, e in gaps:
        bounds.append((cur, s)); cur = e
    bounds.append((cur, total))
    return bounds, total


def tighten_voice(voice, bounds, out, gap=0.3, speed=1.08, pad=0.06, pitch=1.0):
    """Cho giọng gọn và nhanh hơn: cắt từng câu, nối lại với khoảng nghỉ ngắn `gap` giây,
    rồi tăng tốc `speed` lần (giữ nguyên cao độ giọng). Trả về mốc câu mới và độ dài mới."""
    total = duration(voice)
    segs = [(max(0.0, s - pad), min(total, e + pad)) for s, e in bounds]
    fil, labels = "", []
    for i, (s, e) in enumerate(segs):
        fil += f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS,aformat=sample_rates=44100:channel_layouts=mono[s{i}];"
        labels.append(f"[s{i}]")
        if i + 1 < len(segs):
            fil += f"anullsrc=r=44100:cl=mono,atrim=0:{gap}[g{i}];"
            labels.append(f"[g{i}]")
    fil += "".join(labels) + f"concat=n={len(labels)}:v=0:a=1," + (f"rubberband=tempo={speed}:pitch={pitch}:formant=preserved" if pitch != 1 and has_rubberband()
         else (f"asetrate={44100*pitch:.0f},aresample=44100,atempo={speed/pitch:.4f}" if pitch != 1 else f"atempo={speed}")) + "[out]"
    r = sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(voice), "-filter_complex", fil, "-map", "[out]", str(out)])
    if r.returncode != 0:
        sys.exit("Lỗi khi làm gọn giọng đọc: " + r.stderr[-500:])
    new, t = [], 0.0
    for s, e in segs:
        d = (e - s) / speed
        new.append((t + pad / speed, t + d - pad / speed))
        t += d + gap / speed
    return new, duration(out)


THEMES = {  # loại tin -> nhãn mặc định (màu nằm trong template.html / cover.html)
    "luat": "LUẬT MỚI", "thitruong": "THỊ TRƯỜNG", "hatang": "HẠ TẦNG", "hangsang": "HẠNG SANG",
}
NAME_MAIN, NAME_SUB = "Trung", "- Buôn chuyện nhà đất"   # khớp tên kênh TikTok @trungbuonchuyennhadat


def theme_of(spec):
    th = spec.get("theme", "hangsang")
    if th not in THEMES:
        sys.exit(f"theme '{th}' không hợp lệ, chọn một trong: {', '.join(THEMES)}")
    return th


def build_html(spec, base, lines, scene_times, total):
    tpl = (HERE / "template.html").read_text(encoding="utf-8")
    ava = spec.get("avatar")
    ava_path = (base / ava) if ava else None
    if ava_path and ava_path.exists():
        b64 = base64.b64encode(ava_path.read_bytes()).decode()
        tpl = tpl.replace("__AVATAR__", f'<img class="ava" src="data:image/png;base64,{b64}">').replace("__WHOCLASS__", "")
    else:
        if ava:
            print(f"! Không thấy ảnh chân dung {ava_path}, dựng không có ảnh.")
        tpl = tpl.replace("__AVATAR__", "").replace("__WHOCLASS__", "noava")
    th = theme_of(spec)
    hook = spec.get("hook", True)          # cảnh 1 là cảnh móc: chân dung lớn + câu móc chữ cực lớn
    ava_tag = ""
    if ava_path and ava_path.exists():
        ava_tag = f'<img class="hookava" src="data:image/png;base64,{base64.b64encode(ava_path.read_bytes()).decode()}">'
    parts = []
    for i, sc in enumerate(spec["scenes"]):
        cls = "scene hook" if (i == 0 and hook) else "scene"
        attrs = (f' data-trans="{sc["trans"]}"' if sc.get("trans") else "") + (f' data-step="{sc["step"]}"' if sc.get("step") else "")
        inner = sc["html"]
        if i == 0 and hook:
            name_sub = spec.get("name_sub", NAME_SUB).lstrip("- ").strip()
            inner = (f'<div class="hookwho">{ava_tag}<div class="hookname">{spec.get("name_main", NAME_MAIN)}'
                     f'<span>{name_sub}</span></div></div>' + inner)
        parts.append(f'<div class="{cls}"{attrs}>{inner}</div>')
    scenes_html = "\n".join(parts)
    rep = {
        "__THEME__": f"theme-{th}",
        "__NAME_MAIN__": spec.get("name_main", NAME_MAIN),
        "__NAME_SUB__": spec.get("name_sub", NAME_SUB),
        "__TAG__": spec.get("tag", THEMES[th]),
        "__DATE__": spec["date"],
        "__SOURCE__": spec["source"],
        "__SCENES__": scenes_html,
        "__LINES__": json.dumps(lines, ensure_ascii=False),
        "__SCENE_TIMES__": json.dumps(scene_times),
        "__TOTAL__": str(total),
        "__HIGHLIGHT__": json.dumps([re.escape(w) for w in spec.get("highlight", [])], ensure_ascii=False),
    }
    for k, v in rep.items():
        tpl = tpl.replace(k, v)
    return add_fonts(tpl)


def main():
    args = sys.argv[1:]
    spec_path = Path(args[0]).resolve()
    base = spec_path.parent
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    preview = [float(x) for x in args[args.index("--preview") + 1:]] if "--preview" in args else None

    voice = base / spec["voice"]
    texts = spec["lines"]
    bounds, vdur = line_timings(voice, texts, spec.get("line_breaks"))
    work = base / "_build"; work.mkdir(exist_ok=True)
    # Mặc định: rút khoảng nghỉ giữa câu còn 0,3 giây và đọc nhanh hơn 8% cho đỡ dềnh dàng.
    # Tắt bằng "voice_speed": 1.0 và "voice_gap": null trong spec.
    if spec.get("voice_gap", 0.3) is not None:
        tight = work / "voice_tight.wav"
        bounds, vdur = tighten_voice(voice, bounds, tight, gap=spec.get("voice_gap", 0.3),
                                     speed=spec.get("voice_speed", 1.08), pitch=spec.get("voice_pitch", 1.06))
        voice = tight
    lines = [{"start": round(s, 3), "dur": round(e - s, 3), "text": t} for (s, e), t in zip(bounds, texts)]
    total = round(vdur + spec.get("tail", 0.8), 2)

    # mỗi cảnh ứng với một hoặc nhiều câu (scene["lines"] là chỉ số câu, câu đầu tiên quyết định lúc vào cảnh)
    ins = []
    for i, sc in enumerate(spec["scenes"]):
        first = min(sc["lines"])
        ins.append(0.0 if i == 0 else max(0.0, round(bounds[first][0] - 0.15, 2)))
    scene_times = [{"in": ins[i], "out": ins[i + 1] if i + 1 < len(ins) else 999} for i in range(len(ins))]

    html = build_html(spec, base, lines, scene_times, total)
    page = work / "overlay.html"; page.write_text(html, encoding="utf-8")
    print("Mốc câu:", [(round(l["start"], 2), round(l["start"] + l["dur"], 2)) for l in lines])
    print("Mốc cảnh:", [s["in"] for s in scene_times], "tổng", total)
    if bounds[0][1] - bounds[0][0] > 4.0:
        print(f"! Câu móc dài {bounds[0][1] - bounds[0][0]:.1f}s, nên dưới 3,5s: rút câu 1 cho ngắn lại.")
    if total > 75:
        print(f"! Video dài {total}s, vượt mục tiêu 45–60s (tối đa 75s): cắt bớt ý.")

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = launch_browser(p)
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.goto(page.as_uri()); pg.evaluate("document.fonts.ready")

        if preview:
            for t in preview:
                pg.evaluate(f"render({t})")
                out = work / f"preview_{t:05.1f}.png"
                pg.screenshot(path=str(out)); print("Ảnh xem trước:", out)
            b.close(); return

        # ---- dựng một lượt: video nền + lớp chữ (pipe) + giọng + nhạc ----
        cmd = ["ffmpeg", "-y", "-loglevel", "error"]
        fil = ""
        n = len(spec["scenes"])
        for i, sc in enumerate(spec["scenes"]):
            ln = round(scene_times[i]["out"] - scene_times[i]["in"], 3) if i + 1 < n else round(total - scene_times[i]["in"], 3)
            cmd += ["-stream_loop", "-1", "-ss", str(sc.get("broll_offset", 0)), "-t", str(ln), "-i", str(base / sc["broll"])]
            fil += (f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},setsar=1,"
                    f"eq=saturation=0.85,trim=duration={ln},setpts=PTS-STARTPTS,"
                    f"zoompan=z='min(1.0+0.0007*on,1.08)':d=1:s={W}x{H}:fps={FPS}[v{i}];")
        fil += "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[bg];"
        cmd += ["-f", "image2pipe", "-framerate", str(FPS), "-i", "-"]
        fil += f"[{n}:v]format=rgba[ov];[bg][ov]overlay=0:0:format=auto[vid];"
        cmd += ["-i", str(voice)]
        vi = n + 1
        music = spec.get("music")
        if music:
            mpath = base / music
            if duration(mpath) < total + 1:
                # nhạc ngắn hơn video: nối bản nhạc với chính nó, chồng mờ 3 giây ở chỗ nối cho khỏi giật
                loop = work / "music_loop.wav"
                n_rep = int(total // max(1.0, duration(mpath) - 3)) + 1
                ins, chain = [], ""
                for r in range(n_rep):
                    ins += ["-i", str(mpath)]
                prev = "[0:a]"
                for r in range(1, n_rep):
                    chain += f"{prev}[{r}:a]acrossfade=d=3:c1=tri:c2=tri[x{r}];"
                    prev = f"[x{r}]"
                if n_rep > 1:
                    sh(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", chain.rstrip(";"),
                        "-map", prev, str(loop)])
                    if loop.exists():
                        mpath = loop
            cmd += ["-stream_loop", "-1", "-i", str(mpath)]
            # nhạc nền giữ âm lượng đều suốt video (không tự hạ khi có giọng)
            # giọng nén nhẹ cho đều và rõ, nhạc nền để thấp hẳn dưới giọng (âm lượng đều, không tự hạ)
            mv = spec.get("music_volume", 0.10)
            fil += (f"[{vi}:a]apad,aformat=sample_rates=44100:channel_layouts=stereo,"
                    f"highpass=f=80,acompressor=threshold=0.08:ratio=3:attack=5:release=150:makeup=2[vo];"
                    f"[{vi+1}:a]aformat=sample_rates=44100:channel_layouts=stereo,volume={mv},"
                    f"afade=t=out:st={max(0, total-3.5)}:d=3.5[mu];"
                    f"[vo][mu]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
        else:
            fil += f"[{vi}:a]apad,loudnorm=I=-14:TP=-1.5:LRA=11[aout]"
        out = base / spec["out"]
        cmd += ["-filter_complex", fil, "-map", "[vid]", "-map", "[aout]",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-t", str(total), "-movflags", "+faststart", str(out)]
        ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        for i in range(int(total * FPS)):
            pg.evaluate(f"render({i / FPS})")
            ff.stdin.write(pg.screenshot(type="png", omit_background=True))
        ff.stdin.close(); ff.wait()
        b.close()
        if ff.returncode != 0:
            sys.exit("ffmpeg lỗi khi dựng video")
        print("Xong:", out, f"({total}s)")


if __name__ == "__main__":
    main()
