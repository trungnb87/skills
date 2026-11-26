#!/usr/bin/env python3
"""Dựng video TikTok ngay trên máy anh Trung, không tốn credit Claude.

Claude chỉ viết kịch bản và file spec.json (đặt trong một thư mục video).
Script này tự làm phần còn lại:
  1. Tạo giọng đọc bằng giọng nhân bản trên ElevenLabs (chỉ tạo 1 lần, có rồi thì dùng lại)
  2. Tìm và tải video nền miễn phí trên Pixabay (hoặc Pexels nếu có key) theo từ khóa "broll_query" của từng cảnh;
     cảnh nào có "ban_do" thì dựng bản đồ động có đường chạy (Remotion + OpenStreetMap)
  3. Chọn nhạc nền EPIC theo loại tin, xoay vòng để không trùng video trước
  4. Dựng video MP4, ảnh cover và file thong-tin.txt (caption, hashtag)

Dùng:
  python3 dung.py <thư-mục-video>              dựng một video
  python3 dung.py <thư-mục-video> --xem-truoc  chỉ xuất vài ảnh xem trước bố cục
  python3 dung.py --tat-ca                     dựng mọi thư mục có spec.json mà chưa có video
  python3 dung.py <thư-mục-video> --lam-lai-giong   xóa giọng cũ, tạo lại (TỐN credit ElevenLabs)
"""
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"
ASSETS = ROOT / "assets"
STATE = ROOT / ".trang-thai.json"
PY = sys.executable

# Nhạc ưu tiên theo loại tin (xem bảng mood trong SKILL.md); hết thì xoay sang các bản còn lại.
MUSIC_PREF = {
    "luat": ["01", "09", "04", "03"],
    "thitruong": ["02", "03", "06", "01"],
    "hatang": ["10", "06", "03", "02"],
    "hangsang": ["05", "10", "07", "08"],
}


# ---------- tiện ích ----------
def say(msg):
    print(msg, flush=True)


def fail(msg):
    say("\n✖ " + msg)
    sys.exit(1)


def load_env():
    env = {}
    f = ROOT / "cau-hinh.env"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    for k in ("ELEVENLABS_API_KEY", "PEXELS_API_KEY", "PIXABAY_API_KEY", "ELEVEN_VOICE_ID", "ELEVEN_MODEL", "THU_MUC_VIDEO"):
        if os.environ.get(k):
            env[k] = os.environ[k]
    env.setdefault("ELEVEN_VOICE_ID", "LXjvSaudzF11FKObF2RB")
    env.setdefault("ELEVEN_MODEL", "eleven_v4")
    env.setdefault("THU_MUC_VIDEO", "~/Movies/diem-bao-bds")
    return env


def load_state():
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except Exception:
        return {"music": [], "pexels": []}


def save_state(st):
    st["music"] = st.get("music", [])[-10:]
    st["pexels"] = st.get("pexels", [])[-400:]
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")


def slug(text):
    t = unicodedata.normalize("NFD", text.replace("đ", "d").replace("Đ", "D"))
    t = "".join(c for c in t if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:70] or "video"


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True).stdout.strip()
    return float(out) if out else 0.0


def http(url, headers=None, data=None, timeout=120):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": "trung-video/1.0", **(headers or {})})
    return urllib.request.urlopen(req, timeout=timeout)


def download(url, dest):
    tmp = dest.with_suffix(dest.suffix + ".part")
    with http(url, timeout=300) as r, open(tmp, "wb") as f:
        shutil.copyfileobj(r, f)
    tmp.rename(dest)


# ---------- 1. giọng đọc ----------
def voice_prompt(spec):
    if spec.get("voice_prompt"):
        return spec["voice_prompt"]
    lines = spec["lines"]
    out = []
    for i, t in enumerate(lines):
        t = t.strip()
        low = t.lower()
        if i == 0 or i == len(lines) - 1 or low.startswith(("thứ nhất", "thứ hai", "thứ ba", "tiếp theo", "cuối cùng")):
            tag = "[excited] [energetic]"
        elif low.startswith(("lưu ý", "cẩn thận", "cảnh báo")):
            tag = "[energetic]"
        else:
            tag = "[cheerful] [energetic]"
        if (i == 0 or i == len(lines) - 1) and t[-1:] not in "!?":
            t = t.rstrip(".") + "!"
        out.append(f"{tag} {t}" + (" [pause]" if i < len(lines) - 1 else ""))
    return "\n".join(out)


def make_voice(spec, base, env):
    voice = base / spec["voice"]
    if voice.exists() and voice.stat().st_size > 1000:
        say(f"• Giọng đọc: dùng lại {voice.name} (không tốn credit)")
        return 0
    key = env.get("ELEVENLABS_API_KEY", "")
    if not key or key.startswith("dan-"):
        fail("Chưa có ELEVENLABS_API_KEY trong file cau-hinh.env (xem HUONG-DAN.txt, mục 2).")
    text = voice_prompt(spec)
    (base / "loi-doc.txt").write_text(text, encoding="utf-8")
    plain = sum(len(t) for t in spec["lines"])
    say(f"• Tạo giọng đọc ({plain} ký tự lời đọc, khoảng {round(plain * 0.9)}–{plain} credit ElevenLabs)…")
    models = [env["ELEVEN_MODEL"]] + [m for m in ("eleven_v3",) if m != env["ELEVEN_MODEL"]]
    url = (f"https://api.elevenlabs.io/v1/text-to-speech/{env['ELEVEN_VOICE_ID']}"
           "?output_format=mp3_44100_128")
    for model in models:
        body = json.dumps({"text": text, "model_id": model}).encode()
        try:
            with http(url, {"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
                      body, timeout=300) as r:
                voice.write_bytes(r.read())
            say(f"  ✓ Đã lưu {voice.name} (model {model}, {duration(voice):.1f} giây)")
            return plain
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "ignore")[:400]
            if e.code == 401:
                fail("ElevenLabs từ chối API key. Kiểm tra lại ELEVENLABS_API_KEY trong cau-hinh.env.")
            if "model" in msg.lower() and model != models[-1]:
                say(f"  ! Model {model} không dùng được qua API, thử {models[-1]}…")
                continue
            if "quota" in msg.lower() or "credits" in msg.lower():
                fail("ElevenLabs báo hết credit tháng này: " + msg)
            fail(f"ElevenLabs lỗi {e.code}: {msg}")
        except urllib.error.URLError as e:
            fail(f"Không kết nối được ElevenLabs ({e.reason}). Kiểm tra mạng rồi chạy lại.")
    return 0


# ---------- 2. video nền ----------
def pick_file(video):
    files = [f for f in video.get("video_files", []) if f.get("width") and f.get("height") and f["height"] > f["width"]]
    if not files:
        return None
    # ưu tiên đúng 1080x1920, rồi bản gần 1920 chiều cao nhất (không lấy bản 4K cho nhẹ)
    files.sort(key=lambda f: (f["width"] != 1080, abs(f["height"] - 1920), f["height"] > 2200))
    return files[0]


def pexels_search(query, key, page=1):
    q = urllib.parse.urlencode({"query": query, "orientation": "portrait", "per_page": 30, "page": page})
    with http(f"https://api.pexels.com/videos/search?{q}", {"Authorization": key}) as r:
        return json.loads(r.read())


def pixabay_search(query, key, page=1):
    q = urllib.parse.urlencode({"key": key, "q": query[:100], "video_type": "film", "safesearch": "true",
                                "per_page": 50, "page": page})
    with http(f"https://pixabay.com/api/videos/?{q}") as r:
        data = json.loads(r.read())
    vids = []
    for h in data.get("hits", []):
        best = None
        for name, f in (h.get("videos") or {}).items():
            w, hh, url = f.get("width") or 0, f.get("height") or 0, f.get("url")
            if not url or not w:
                continue
            # dọc 9:16 là tốt nhất; ngang thì phải đủ cao (4K) để cắt dọc vẫn nét
            if hh > w and hh >= 1280:
                score = 0 + abs(hh - 1920) / 1e4
            elif hh >= 2000:
                score = 1 + abs(hh - 2160) / 1e4
            elif hh >= 1080:
                score = 2
            else:
                continue
            if best is None or score < best[0]:
                best = (score, {"width": w, "height": hh, "link": url})
        if best:
            vids.append((best[0], {"id": f"px{h['id']}", "duration": h.get("duration", 0), "file": best[1]}))
    vids.sort(key=lambda x: x[0])
    return [v for _, v in vids]


def make_maps(spec, base):
    """Cảnh nào có "ban_do" (mô tả như ban-do.json, xem scripts/ban-do/make_map.py) thì dựng bản đồ động bằng Remotion."""
    jobs = [(i, sc) for i, sc in enumerate(spec["scenes"]) if sc.get("ban_do")]
    if not jobs:
        return
    env = dict(os.environ)
    env["PATH"] = "/opt/homebrew/bin:/usr/local/bin:" + env.get("PATH", "")
    if not shutil.which("npx", path=env["PATH"]):
        fail("Chưa có Node.js để dựng bản đồ. Bấm đúp CAI-DAT.command để cài lại.")
    (base / "broll").mkdir(exist_ok=True)
    for i, sc in jobs:
        rel = f"broll/bando-{i + 1}.mp4"
        sc["broll"], sc["broll_offset"], sc["clear"] = rel, 0, True
        sc.setdefault("html", "")
        if (base / rel).exists():
            continue
        say(f"• Dựng bản đồ động cho cảnh {i + 1} (lần đầu tự cài Remotion, ~2–4 phút)…")
        m = dict(sc["ban_do"]); m["out"] = rel; m.setdefault("seconds", 12)
        mj = base / f"ban-do-{i + 1}.json"
        mj.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
        r = subprocess.run([PY, str(SCRIPTS / "ban-do" / "make_map.py"), str(mj)], env=env)
        if r.returncode or not (base / rel).exists():
            fail(f"Dựng bản đồ cảnh {i + 1} lỗi (xem dòng phía trên). Chụp màn hình gửi Claude.")


def get_broll(spec, base, env, st):
    used_now = set()
    need = [sc for sc in spec["scenes"] if not (sc.get("broll") and (base / sc["broll"]).exists())]
    if not need:
        say("• Video nền: đã đủ")
        return
    key = env.get("PEXELS_API_KEY", "")
    key = "" if key.startswith("dan-") else key
    pxb = env.get("PIXABAY_API_KEY", "")
    pxb = "" if pxb.startswith("dan-") else pxb
    if not key and not pxb:
        fail("Chưa có PIXABAY_API_KEY (hoặc PEXELS_API_KEY) trong cau-hinh.env (miễn phí, xem HUONG-DAN.txt mục 2).")
    (base / "broll").mkdir(exist_ok=True)
    for sc in spec["scenes"]:
        if sc.get("broll") and (base / sc["broll"]).exists():
            used_now.add(Path(sc["broll"]).name)
    say(f"• Tìm video nền cho {len(need)} cảnh ({'Pexels' if key else 'Pixabay'})…")
    for sc in need:
        queries = sc.get("broll_query") or spec.get("broll_query") or "Hanoi city skyline aerial"
        queries = [queries] if isinstance(queries, str) else list(queries)
        chosen = None
        for q in queries:
            for page in (1, 2):
                if not key:
                    try:
                        cands = pixabay_search(q, pxb, page)
                    except urllib.error.HTTPError as e:
                        fail("Pixabay từ chối API key, kiểm tra PIXABAY_API_KEY." if e.code in (400, 401, 403) else f"Pixabay lỗi {e.code}")
                    except urllib.error.URLError as e:
                        fail(f"Không kết nối được Pixabay ({e.reason}).")
                    for v in cands:
                        if v["id"] in st["pexels"] or f"{v['id']}.mp4" in used_now or v["duration"] < 6:
                            continue
                        chosen = (v["id"], v["file"], q)
                        break
                    if chosen:
                        break
                    continue
                try:
                    res = pexels_search(q, key, page)
                except urllib.error.HTTPError as e:
                    if e.code in (401, 403):
                        fail("Pexels từ chối API key. Kiểm tra PEXELS_API_KEY trong cau-hinh.env.")
                    fail(f"Pexels lỗi {e.code}")
                except urllib.error.URLError as e:
                    fail(f"Không kết nối được Pexels ({e.reason}).")
                for v in res.get("videos", []):
                    vid = str(v["id"])
                    if vid in st["pexels"] or f"pexels-{vid}.mp4" in used_now or v.get("duration", 0) < 6:
                        continue
                    f = pick_file(v)
                    if f:
                        chosen = (vid, f, q)
                        break
                if chosen:
                    break
            if chosen:
                break
        if not chosen:
            fail(f"Không tìm được video nền dọc mới cho từ khóa {queries}. Thêm từ khóa khác vào broll_query.")
        vid, f, q = chosen
        dest = base / "broll" / (f"{vid}.mp4" if vid.startswith("px") else f"pexels-{vid}.mp4")
        say(f"  ↓ \"{q}\" → {vid} ({f['width']}x{f['height']})")
        download(f["link"], dest)
        sc["broll"] = f"broll/{dest.name}"
        sc.setdefault("broll_offset", 0)
        used_now.add(dest.name)
        st["pexels"].append(vid)


# ---------- 3. nhạc nền ----------
def pick_music(spec, st):
    lib = sorted((ASSETS / "nhac-nen").glob("*.mp3"))
    if not lib:
        fail("Không thấy nhạc nền trong assets/nhac-nen.")
    m = spec.get("music")
    if m and m != "auto":
        p = Path(m)
        for cand in (p, ASSETS / "nhac-nen" / p.name):
            if cand.is_absolute() and cand.exists():
                return str(cand)
        if (ASSETS / "nhac-nen" / p.name).exists():
            return str(ASSETS / "nhac-nen" / p.name)
    pref = MUSIC_PREF.get(spec.get("theme", "hangsang"), [])
    order = [f for code in pref for f in lib if f.name.startswith(code)] + lib
    recent = st.get("music", [])[-3:]
    for f in order:
        if f.name not in recent:
            return str(f)
    return str(order[0])


# ---------- 4. thông tin đăng ----------
def write_info(spec, base, out, chars):
    cap = spec.get("caption", "")
    cap = "\n".join(cap) if isinstance(cap, list) else cap
    tags = spec.get("hashtags", [])
    tags = " ".join(t if t.startswith("#") else "#" + t for t in tags) if isinstance(tags, list) else tags
    title = spec.get("tiktok_title") or re.sub(r"<[^>]+>", "", spec.get("cover", {}).get("title", "")).upper()
    parts = [
        f"TIÊU ĐỀ: {title}", "",
        "CAPTION (copy dán thẳng):", cap + ("\n\n" + tags if tags else ""), "",
        ("Video nền: Pexels" if any("pexels-" in str(sc.get("broll", "")) for sc in spec["scenes"]) else "Video nền: Pixabay"),
        spec.get("source", ""),
        *(["Bản đồ: © OpenStreetMap contributors"] if any(sc.get("ban_do") for sc in spec["scenes"]) else []),
        f"Nhạc nền: {Path(spec['music']).name}",
        f"Credit ElevenLabs dùng lần này: ~{chars} ký tự" if chars else "Giọng đọc: dùng lại file có sẵn",
        "Gợi ý giờ đăng: 11h30–12h30 hoặc 19h30–21h30, tối đa 2 video/ngày, cách nhau ít nhất 4 tiếng.",
    ]
    (base / "thong-tin.txt").write_text("\n".join(parts) + "\n", encoding="utf-8")


# ---------- chạy một thư mục ----------
def run_job(base, env, preview=False, redo_voice=False):
    base = base.expanduser().resolve()
    spec_path = base / "spec.json"
    if not spec_path.exists():
        fail(f"Không thấy spec.json trong {base}")
    try:
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"spec.json bị lỗi cú pháp ở dòng {e.lineno}: {e.msg}. Gửi lỗi này cho Claude để sửa.")
    for k in ("lines", "scenes"):
        if not spec.get(k):
            fail(f"spec.json thiếu mục \"{k}\".")
    say(f"\n=== {base.name} ===")
    st = load_state()
    st.setdefault("music", []); st.setdefault("pexels", [])

    spec.setdefault("voice", "voice.mp3")
    spec.setdefault("date", dt.date.today().strftime("%d.%m.%Y"))
    spec.setdefault("source", "")
    if not spec.get("out"):
        spec["out"] = slug(re.sub(r"^\d{4}-\d{2}-\d{2}-", "", base.name)) + ".mp4"
    if not spec.get("avatar") or not (base / spec["avatar"]).exists():
        spec["avatar"] = str(ASSETS / "avatar.png")
    spec["music"] = pick_music(spec, st)
    if redo_voice and (base / spec["voice"]).exists():
        (base / spec["voice"]).unlink()

    chars = make_voice(spec, base, env)
    make_maps(spec, base)
    get_broll(spec, base, env, st)
    say(f"• Nhạc nền: {Path(spec['music']).name}")
    spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
    save_state(st)

    if preview:
        r = subprocess.run([PY, str(SCRIPTS / "build_video.py"), str(spec_path), "--preview",
                            *[str(t) for t in (0, 2, 8, 16, 24, 32, 40, 48, 56)]])
        if r.returncode:
            fail("Lỗi khi xuất ảnh xem trước (xem dòng phía trên).")
        if sys.platform == "darwin":
            subprocess.run(["open", *map(str, sorted((base / "_build").glob("preview_*.png")))])
        say("\n✓ Ảnh xem trước nằm trong thư mục _build. Ổn thì chạy lại không có --xem-truoc để dựng.")
        return

    say("• Dựng video (khoảng 3–6 phút cho video 1 phút)…")
    t0 = time.time()
    r = subprocess.run([PY, str(SCRIPTS / "build_video.py"), str(spec_path)])
    if r.returncode:
        fail("Dựng video lỗi (xem dòng phía trên). Chụp màn hình gửi Claude.")
    r = subprocess.run([PY, str(SCRIPTS / "make_cover.py"), str(spec_path)])
    if r.returncode:
        say("! Lỗi khi làm ảnh cover, video vẫn dùng được.")
    write_info(spec, base, spec["out"], chars)
    st = load_state(); st.setdefault("music", []).append(Path(spec["music"]).name); save_state(st)
    shutil.rmtree(base / "_build", ignore_errors=True)
    say(f"\n✓ XONG sau {int(time.time() - t0)} giây: {base / spec['out']}")
    say("  Có thêm ảnh cover và thong-tin.txt (caption, hashtag) cùng thư mục.")
    if sys.platform == "darwin":
        subprocess.run(["open", str(base)])


def main():
    args = sys.argv[1:]
    env = load_env()
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            fail(f"Máy chưa có {tool}. Bấm đúp CAI-DAT.command trước.")
    if not args or args[0] in ("-h", "--help"):
        print(__doc__); return
    preview = "--xem-truoc" in args
    redo = "--lam-lai-giong" in args
    if "--tat-ca" in args:
        root = Path(env["THU_MUC_VIDEO"]).expanduser()
        jobs = []
        for d in sorted(root.iterdir() if root.exists() else []):
            if (d / "spec.json").exists():
                try:
                    out = json.loads((d / "spec.json").read_text(encoding="utf-8")).get("out")
                except Exception:
                    out = None
                if not (out and (d / out).exists()):
                    jobs.append(d)
        if not jobs:
            say(f"Không có video nào đang chờ dựng trong {root}."); return
        say(f"Có {len(jobs)} video chờ dựng: " + ", ".join(j.name for j in jobs))
        for j in jobs:
            run_job(j, env, preview, redo)
        return
    run_job(Path([a for a in args if not a.startswith("--")][0]), env, preview, redo)


if __name__ == "__main__":
    main()
