#!/usr/bin/env python3
"""Cắt ảnh chân dung thành hình tròn 400x400, làm sáng và hồng hào nhẹ.

Dùng: python3 make_avatar.py anh-goc.jpg avatar.png [x0 y0 x1 y1]
Vùng cắt mặc định hợp với ảnh chân dung bán thân 1215x1620 (khung vuông quanh đầu và vai).
"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance

src, dst = sys.argv[1], sys.argv[2]
box = tuple(int(v) for v in sys.argv[3:7]) if len(sys.argv) >= 7 else None
im = Image.open(src).convert("RGB")
if box is None:
    w, h = im.size
    s = int(w * 0.56)
    cx, top = w // 2 - int(w * 0.02), int(h * 0.06)
    box = (cx - s // 2, top, cx + s // 2, top + s)
c = im.crop(box).resize((400, 400), Image.LANCZOS)
c = ImageEnhance.Brightness(c).enhance(1.13)
c = ImageEnhance.Contrast(c).enhance(1.04)
c = ImageEnhance.Color(c).enhance(1.15)
a = np.asarray(c).astype(float)
a[..., 0] = a[..., 0] * 1.05 + 6   # ấm, hồng nhẹ
a[..., 1] = a[..., 1] * 0.99
a[..., 2] = a[..., 2] + 2
c = Image.fromarray(np.clip(a, 0, 255).astype("uint8"))
m = Image.new("L", (400, 400), 0)
ImageDraw.Draw(m).ellipse((0, 0, 399, 399), fill=255)
out = Image.new("RGBA", (400, 400))
out.paste(c, (0, 0), m)
out.save(dst)
print("Đã lưu", dst)
