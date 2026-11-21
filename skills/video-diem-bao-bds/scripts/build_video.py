#!/usr/bin/env python3
"""Dựng video dọc 9:16 cho kênh TRUNGNB - BUÔN CHUYỆN BĐS từ một file spec JSON.

Dùng:
  python3 build_video.py spec.json                  # xuất MP4
  python3 build_video.py spec.json --preview 3 20   # chỉ chụp khung hình tại giây 3 và 20 (kiểm tra bố cục)

Cần: ffmpeg, Google Chrome hoặc Chromium, Python playwright (pip install playwright --break-system-packages).
Xem examples/knight-frank.json để biết cấu trúc spec.
"""
import base64, json, os, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FPS = 30
W, H = 1080, 1920


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def duration(path):
    out = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]).stdout
    return float(out.strip())


def line_timings(voice, n_lines):
    """Tìm n_lines-1 khoảng nghỉ dài nhất trong giọng đọc để biết mỗi câu bắt đầu/kết thúc lúc nào."""
    total = duration(voice)
    err = sh(["ffmpeg", "-i", str(voice), "-af", "silencedetect=n=-35dB:d=0.3", "-f", "null", "-"]).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    sil = list(zip(starts, ends))
    lead = 0.0
    if sil and sil[0][0] < 0.05:          # khoảng lặng đầu file
        lead = sil[0][1]; sil = sil[1:]
    sil = [s for s in sil if s[1] < total - 0.05]   # bỏ khoảng lặng cuối file
    if len(sil) < n_lines - 1:
        sys.exit(f"Chỉ tìm thấy {len(sil)} khoảng nghỉ cho {n_lines} câu. Tạo lại giọng đọc với [pause] giữa các câu.")
    gaps = sorted(sorted(sil, key=lambda s: s[1] - s[0], reverse=True)[: n_lines - 1])
    bounds, cur = [], lead
    for s, e in gaps:
        bounds.append((cur, s)); cur = e
    bounds.append((cur, total))
    return bounds, total


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
    scenes_html = "\n".join(f'<div class="scene">{sc["html"]}</div>' for sc in spec["scenes"])
    rep = {
        "__NAME_MAIN__": spec.get("name_main", "Trungnb"),
        "__NAME_SUB__": spec.get("name_sub", "- Buôn chuyện BĐS"),
        "__TAG__": spec.get("tag", "BẢN TIN BĐS"),
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
    return tpl


def main():
    args = sys.argv[1:]
    spec_path = Path(args[0]).resolve()
    base = spec_path.parent
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    preview = [float(x) for x in args[args.index("--preview") + 1:]] if "--preview" in args else None

    voice = base / spec["voice"]
    texts = spec["lines"]
    bounds, vdur = line_timings(voice, len(texts))
    lines = [{"start": round(s, 3), "dur": round(e - s, 3), "text": t} for (s, e), t in zip(bounds, texts)]
    total = round(vdur + spec.get("tail", 0.8), 2)

    # mỗi cảnh ứng với một hoặc nhiều câu (scene["lines"] là chỉ số câu, câu đầu tiên quyết định lúc vào cảnh)
    ins = []
    for i, sc in enumerate(spec["scenes"]):
        first = min(sc["lines"])
        ins.append(0.0 if i == 0 else max(0.0, round(bounds[first][0] - 0.15, 2)))
    scene_times = [{"in": ins[i], "out": ins[i + 1] if i + 1 < len(ins) else 999} for i in range(len(ins))]

    html = build_html(spec, base, lines, scene_times, total)
    work = base / "_build"; work.mkdir(exist_ok=True)
    page = work / "overlay.html"; page.write_text(html, encoding="utf-8")
    print("Mốc câu:", [(round(l["start"], 2), round(l["start"] + l["dur"], 2)) for l in lines])
    print("Mốc cảnh:", [s["in"] for s in scene_times], "tổng", total)

    from playwright.sync_api import sync_playwright
    chrome = next((p for p in ["/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"] if os.path.exists(p)), None)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=chrome) if chrome else p.chromium.launch()
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
            cmd += ["-stream_loop", "-1", "-i", str(base / music)]
            mv = spec.get("music_volume", 0.32)
            fil += (f"[{vi}:a]apad,aformat=sample_rates=44100:channel_layouts=stereo,asplit=2[vo][sc];"
                    f"[{vi+1}:a]aformat=sample_rates=44100:channel_layouts=stereo,volume={mv},"
                    f"afade=t=out:st={max(0, total-3.5)}:d=3.5[mu];"
                    f"[mu][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[duck];"
                    f"[vo][duck]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
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
