#!/usr/bin/env python3
"""Trình sửa video trên Mac (kiểu CapCut thu gọn) cho các video đã dựng bằng dung.py.

Bấm đúp SUA-VIDEO.command: mở trình duyệt ở http://localhost:8765
  - chọn video, xem trước có giọng + nhạc + video nền + chữ y như bản dựng
  - sửa chữ trên màn hình, hiệu ứng, lúc hiện, cỡ chữ; thêm/xóa khối chữ
  - đổi video nền, đoạn bắt đầu, chuyển cảnh; bỏ câu để rút ngắn video
  - chỉnh tốc độ đọc, khoảng nghỉ, nhạc nền, âm lượng nhạc, màu loại tin, cover, caption
  - Lưu (spec.json, có bản sao lưu) rồi Dựng lại video ngay trong trang
Không tốn credit: không tạo lại giọng, chỉ dựng lại hình.
"""
import json
import mimetypes
import os
import re
import subprocess
import sys
import threading
import time
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"
ASSETS = ROOT / "assets"
PY = sys.executable
PORT = int(os.environ.get("SUA_PORT", "8765"))
JOBS = {}   # tên thư mục -> Popen của lần dựng lại
ASSET_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".otf", ".ttf", ".woff", ".woff2", ".mp3", ".wav", ".mp4", ".mov"}


def video_root():
    env = {}
    f = ROOT / "cau-hinh.env"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"')
    d = os.environ.get("THU_MUC_VIDEO") or env.get("THU_MUC_VIDEO") or "~/Movies/diem-bao-bds"
    return Path(os.path.expanduser(d)).resolve()


def folder(name):
    base = (video_root() / name).resolve()
    if base.parent != video_root() or not (base / "spec.json").exists():
        raise FileNotFoundError(name)
    return base


def list_videos():
    out = []
    for d in sorted(video_root().iterdir(), reverse=True):
        if d.is_dir() and (d / "spec.json").exists() and not d.name.startswith(("_", ".")):
            mp4 = [p.name for p in d.glob("*.mp4") if not p.name.startswith(".")]
            out.append({"name": d.name, "mp4": mp4[0] if mp4 else None,
                        "ready": (d / "voice.mp3").exists() or any(d.glob("voice.*"))})
    return out


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    # ---------- trả dữ liệu ----------
    def send_json(self, obj, code=200):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def send_file(self, path):
        path = Path(path)
        if not path.exists() or not path.is_file():
            return self.send_error(404)
        size = path.stat().st_size
        ctype = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        if path.suffix == ".html":
            ctype = "text/html; charset=utf-8"
        rng = self.headers.get("Range")
        start, end = 0, size - 1
        if rng and rng.startswith("bytes="):
            a, _, b = rng[6:].partition("-")
            start = int(a) if a else max(0, size - int(b))
            end = int(b) if (a and b) else size - 1
            self.send_response(206)
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        else:
            self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(end - start + 1))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        with open(path, "rb") as f:
            f.seek(start)
            left = end - start + 1
            while left > 0:
                chunk = f.read(min(1 << 20, left))
                if not chunk:
                    break
                try:
                    self.wfile.write(chunk)
                except (BrokenPipeError, ConnectionResetError):
                    return
                left -= len(chunk)

    def body(self):
        n = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(n).decode() or "{}")

    # ---------- định tuyến ----------
    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = {k: v[0] for k, v in urllib.parse.parse_qs(u.query).items()}
        try:
            if u.path in ("/", "/index.html"):
                return self.send_file(SCRIPTS / "editor" / "index.html")
            if u.path == "/edit":
                return self.send_file(SCRIPTS / "editor" / "editor.html")
            if u.path == "/api/videos":
                return self.send_json(list_videos())
            if u.path == "/api/spec":
                base = folder(q["d"])
                spec = json.loads((base / "spec.json").read_text(encoding="utf-8"))
                broll = sorted(str(p.relative_to(base)) for p in (base / "broll").glob("*.mp4")) if (base / "broll").exists() else []
                music = [str(p) for p in sorted((ASSETS / "nhac-nen").glob("*.mp3"))]
                mp4 = [p.name for p in base.glob("*.mp4")]
                return self.send_json({"spec": spec, "broll": broll, "music": music, "mp4": mp4[0] if mp4 else None})
            if u.path == "/api/file":
                base = folder(q["d"])
                p = Path(urllib.parse.unquote(q["p"]))
                p = (p if p.is_absolute() else base / p).resolve()
                inside = str(p).startswith(str(base)) or str(p).startswith(str(ROOT))
                # ảnh báo, font do lớp chữ tham chiếu bằng file:// có thể nằm ngoài thư mục video
                if not inside and p.suffix.lower() not in ASSET_EXT:
                    return self.send_error(403)
                if p.suffix == ".html" and p.exists():
                    # trang lớp chữ: đổi file:///… thành đường dẫn qua máy chủ này (trình duyệt chặn file:// trong http)
                    html = p.read_text(encoding="utf-8")
                    d = urllib.parse.quote(q["d"])
                    html = re.sub(r"file://(/[^)\"'\s]+)", lambda m: f"/api/file?d={d}&p={urllib.parse.quote(m.group(1))}", html)
                    b = html.encode()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Length", str(len(b)))
                    self.send_header("Cache-Control", "no-store")
                    self.end_headers()
                    return self.wfile.write(b)
                return self.send_file(p)
            if u.path == "/api/status":
                name = q["d"]
                job = JOBS.get(name)
                log = (folder(name) / "_edit" / "dung-lai.log")
                tail = log.read_text(encoding="utf-8", errors="replace")[-3000:] if log.exists() else ""
                return self.send_json({"running": bool(job and job.poll() is None),
                                       "code": None if not job else job.poll(), "log": tail})
            return self.send_error(404)
        except (KeyError, FileNotFoundError):
            return self.send_error(404)

    def do_POST(self):
        u = urllib.parse.urlparse(self.path)
        q = {k: v[0] for k, v in urllib.parse.parse_qs(u.query).items()}
        try:
            base = folder(q["d"])
        except (KeyError, FileNotFoundError):
            return self.send_error(404)
        if u.path == "/api/prep":
            # bản nháp -> giọng gọn + lớp chữ trong _edit/, không đụng spec.json thật
            draft = base / ".spec-nhap.json"
            draft.write_text(json.dumps(self.body(), ensure_ascii=False, indent=1), encoding="utf-8")
            r = subprocess.run([PY, str(SCRIPTS / "build_video.py"), str(draft), "--prep"], capture_output=True, text=True)
            if r.returncode or not (base / "_edit" / "meta.json").exists():
                return self.send_json({"error": (r.stderr or r.stdout)[-1500:]}, 500)
            meta = json.loads((base / "_edit" / "meta.json").read_text(encoding="utf-8"))
            meta["warn"] = [l for l in r.stdout.splitlines() if l.startswith("!")]
            return self.send_json(meta)
        if u.path == "/api/save":
            spec = self.body()
            (base / "_edit").mkdir(exist_ok=True)
            old = base / "spec.json"
            if old.exists():
                (base / "_edit" / f"spec-{time.strftime('%Y%m%d-%H%M%S')}.json").write_text(old.read_text(encoding="utf-8"), encoding="utf-8")
            old.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
            return self.send_json({"ok": True})
        if u.path == "/api/render":
            name = base.name
            if JOBS.get(name) and JOBS[name].poll() is None:
                return self.send_json({"ok": True, "running": True})
            (base / "_edit").mkdir(exist_ok=True)
            log = open(base / "_edit" / "dung-lai.log", "w", encoding="utf-8")
            env = dict(os.environ, PYTHONUNBUFFERED="1")
            JOBS[name] = subprocess.Popen([PY, str(ROOT / "dung.py"), str(base)], stdout=log, stderr=subprocess.STDOUT, env=env)
            return self.send_json({"ok": True})
        return self.send_error(404)


def main():
    if not video_root().exists():
        sys.exit(f"Không thấy thư mục video {video_root()}")
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), H)
    url = f"http://localhost:{PORT}/"
    print(f"Trình sửa video đang chạy: {url}\n(Giữ cửa sổ này mở trong lúc sửa; đóng cửa sổ để tắt.)")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
