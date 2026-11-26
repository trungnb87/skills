#!/bin/bash
# Cài Remotion (dựng bản đồ động) vào bộ công cụ. Chỉ cần chạy 1 lần; chạy lại để cập nhật cũng được.
cd "$(dirname "$0")/scripts/ban-do" || exit 1
for b in /opt/homebrew/bin/brew /usr/local/bin/brew; do [ -x "$b" ] && eval "$("$b" shellenv)"; done
echo "=== CÀI REMOTION CHO BẢN ĐỒ ĐỘNG ==="
if ! command -v npm >/dev/null 2>&1; then
  echo ">> Máy chưa có Node.js, đang cài bằng Homebrew…"
  brew install node || { echo "Cài Node.js lỗi."; read -r -p "Nhấn Enter để đóng"; exit 1; }
fi
echo ">> Node.js $(node --version)"
echo ">> Cài Remotion (1–3 phút)…"
npm install --no-audit --no-fund || { echo "Cài Remotion lỗi."; read -r -p "Nhấn Enter để đóng"; exit 1; }
echo ">> Tải trình duyệt dựng hình của Remotion…"
npx remotion browser ensure || { echo "Tải trình duyệt lỗi."; read -r -p "Nhấn Enter để đóng"; exit 1; }
echo
echo "=== CÀI XONG. Remotion $(node -p "require('remotion/package.json').version") ==="
read -r -p "Nhấn Enter để đóng"
