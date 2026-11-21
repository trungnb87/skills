#!/usr/bin/env python3
"""Tạo ảnh cover TikTok 1080x1920 (JPG) cho một video, dùng chung file spec với build_video.py.

Dùng: python3 make_cover.py spec.json
Đọc mục "cover" trong spec:
  "cover": {
    "title":  "NGƯỜI HÀN <em>ÔM</em> GẦN NỬA CĂN HỘ KHÁCH NGOẠI",   (bắt buộc, <em> tô vàng)
    "kicker": "Knight Frank 2026",                                  (nhãn vàng trên tiêu đề)
    "number": "48%",                                                (con số lớn, có thể bỏ)
    "number_label": "căn hộ khách ngoại mua là của người Hàn",      (dòng dưới con số)
    "background": "broll/abc.mp4", "background_at": 3               (mặc định: video nền cảnh 1)
  }
Ảnh nền lấy một khung hình từ video nền. Xuất ra <tên video>-cover.jpg cạnh file video.
"""
import base64, json, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    spec_path = Path(sys.argv[1]).resolve()
    base = spec_path.parent
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    cv = spec["cover"]
    sc0 = spec["scenes"][0]
    bg_src = base / cv.get("background", sc0["broll"])
    at = cv.get("background_at", sc0.get("broll_offset", 0) + 1)
    tmp = Path(tempfile.mkdtemp())
    bg = tmp / "bg.jpg"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(at), "-i", str(bg_src), "-frames:v", "1",
                    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920", "-q:v", "3", str(bg)], check=True)
    if not bg.exists():
        sys.exit(f"Không lấy được khung hình nền từ {bg_src}")

    html = (HERE / "cover.html").read_text(encoding="utf-8")
    ava = base / spec.get("avatar", "avatar.png")
    ava_tag = (f'<img class="ava" src="data:image/png;base64,{base64.b64encode(ava.read_bytes()).decode()}">'
               if ava.exists() else "")
    num = cv.get("number")
    numblock = (f'<div class="num">{num}</div><div class="numlab">{cv.get("number_label", "")}</div>' if num else "")
    rep = {
        "__BG__": "data:image/jpeg;base64," + base64.b64encode(bg.read_bytes()).decode(),
        "__TAG__": spec.get("tag", "BẢN TIN BĐS"),
        "__NUMBLOCK__": numblock,
        "__KICKER__": cv.get("kicker", spec.get("tag", "BẢN TIN BĐS")),
        "__KICKBOTTOM__": "900",
        "__TITLE__": cv["title"],
        "__AVATAR__": ava_tag,
        "__NAME_MAIN__": spec.get("name_main", "Trung"),
        "__NAME_SUB__": spec.get("name_sub", "- Buôn chuyện BĐS").lstrip("- ").strip(),
        "__DATE__": spec["date"],
    }
    for k, v in rep.items():
        html = html.replace(k, v)
    page = tmp / "cover.html"
    page.write_text(html, encoding="utf-8")

    out = base / (Path(spec["out"]).stem + "-cover.jpg")
    from playwright.sync_api import sync_playwright
    import os
    chrome = next((p for p in ["/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"] if os.path.exists(p)), None)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=chrome) if chrome else p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto(page.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
        pg.screenshot(path=str(out), type="jpeg", quality=92)
        b.close()
    print("Cover:", out)


if __name__ == "__main__":
    main()
