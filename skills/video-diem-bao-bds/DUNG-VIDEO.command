#!/bin/bash
# Bấm đúp để dựng mọi video đang chờ trong ~/Movies/diem-bao-bds (thư mục có spec.json mà chưa có video).
cd "$(dirname "$0")" || exit 1
for b in /opt/homebrew/bin/brew /usr/local/bin/brew; do [ -x "$b" ] && eval "$("$b" shellenv)"; done
if [ ! -x .venv/bin/python ]; then echo "Chưa cài. Bấm đúp CAI-DAT.command trước."; read -r -p "Nhấn Enter để đóng"; exit 1; fi
caffeinate -i .venv/bin/python dung.py --tat-ca
read -r -p "Nhấn Enter để đóng"
