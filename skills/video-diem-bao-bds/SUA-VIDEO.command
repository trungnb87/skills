#!/bin/bash
# Bấm đúp để mở TRÌNH SỬA VIDEO trong trình duyệt: sửa chữ, hiệu ứng, video nền, độ dài, nhạc rồi dựng lại.
cd "$(dirname "$0")" || exit 1
for b in /opt/homebrew/bin/brew /usr/local/bin/brew; do [ -x "$b" ] && eval "$("$b" shellenv)"; done
if [ ! -x .venv/bin/python ]; then echo "Chưa cài. Bấm đúp CAI-DAT.command trước."; read -r -p "Nhấn Enter để đóng"; exit 1; fi
caffeinate -i .venv/bin/python sua.py
