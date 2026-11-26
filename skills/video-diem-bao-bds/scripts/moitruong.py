"""Phần dùng chung để các script chạy được cả trên Mac lẫn Linux."""
import functools, os, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "fonts"

INTER = {"Regular": 400, "Medium": 500, "SemiBold": 600, "Bold": 700, "ExtraBold": 800, "Black": 900}


def font_css():
    """@font-face trỏ tới font đi kèm bộ công cụ, để máy nào cũng hiện đúng Inter và Montserrat."""
    if not FONTS.exists():
        return ""
    css = []
    m = FONTS / "Montserrat.ttf"
    if m.exists():
        css.append(f'@font-face{{font-family:"Montserrat";src:url("{m.as_uri()}");font-weight:100 900}}')
    for name, w in INTER.items():
        f = FONTS / f"Inter-{name}.otf"
        if f.exists():
            css.append(f'@font-face{{font-family:"Inter";src:url("{f.as_uri()}");font-weight:{w}}}')
    return "<style>" + "".join(css) + "</style>"


def add_fonts(html):
    return html.replace("<head>", "<head>" + font_css(), 1)


def launch_browser(p):
    """Ưu tiên Chromium của Playwright; không có thì dùng Chrome/Chromium cài sẵn trên máy."""
    try:
        return p.chromium.launch()
    except Exception as first:
        for path in ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                     "/Applications/Chromium.app/Contents/MacOS/Chromium",
                     "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"]:
            if os.path.exists(path):
                return p.chromium.launch(executable_path=path)
        raise SystemExit("Không mở được trình duyệt để vẽ chữ. Chạy lại CAI-DAT.command. Chi tiết: " + str(first)[:300])


@functools.lru_cache(None)
def has_rubberband():
    out = subprocess.run(["ffmpeg", "-hide_banner", "-filters"], capture_output=True, text=True).stdout
    return " rubberband " in out
