#!/bin/bash
# Cài các phần mềm cần để dựng video trên Mac. Chỉ cần chạy 1 lần (chạy lại cũng không sao).
cd "$(dirname "$0")" || exit 1
chmod +x ./*.command 2>/dev/null
echo "=== CÀI BỘ DỰNG VIDEO TRUNG - BUÔN CHUYỆN NHÀ ĐẤT ==="

# 1. Homebrew (trình cài phần mềm cho Mac)
if ! command -v brew >/dev/null 2>&1; then
  for b in /opt/homebrew/bin/brew /usr/local/bin/brew; do [ -x "$b" ] && eval "$("$b" shellenv)"; done
fi
if ! command -v brew >/dev/null 2>&1; then
  echo
  echo ">> Máy chưa có Homebrew. Sắp cài Homebrew: máy sẽ hỏi MẬT KHẨU ĐĂNG NHẬP MAC (gõ không hiện chữ, gõ xong nhấn Enter)."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" || { echo "Cài Homebrew lỗi."; read -r -p "Nhấn Enter để đóng"; exit 1; }
  for b in /opt/homebrew/bin/brew /usr/local/bin/brew; do [ -x "$b" ] && eval "$("$b" shellenv)"; done
  grep -q "brew shellenv" ~/.zprofile 2>/dev/null || echo 'eval "$(/opt/homebrew/bin/brew shellenv 2>/dev/null || /usr/local/bin/brew shellenv)"' >> ~/.zprofile
fi

# 2. Python, ffmpeg (dựng video), Node.js (bản đồ động và plugin PDF của Claude)
echo; echo ">> Cài Python, ffmpeg, Node.js (lần đầu mất 5–15 phút)…"
brew install python ffmpeg node || { echo "Cài bằng Homebrew lỗi."; read -r -p "Nhấn Enter để đóng"; exit 1; }

# 3. Môi trường Python riêng + trình duyệt vẽ chữ
PY="$(brew --prefix)/bin/python3"
echo; echo ">> Cài Playwright (vẽ chữ, hiệu ứng)…"
"$PY" -m venv .venv && .venv/bin/pip install --quiet --upgrade pip playwright && .venv/bin/python -m playwright install chromium \
  || { echo "Cài Playwright lỗi."; read -r -p "Nhấn Enter để đóng"; exit 1; }

# 4. File cấu hình API key
if [ ! -f cau-hinh.env ]; then cp cau-hinh.mau.env cau-hinh.env; fi
echo
echo "=== CÀI XONG ==="
python3 --version; node --version; ffmpeg -version | head -1
if grep -q "dan-key" cau-hinh.env; then
  echo
  echo ">> Bước cuối: dán 2 API key vào file cau-hinh.env (đang mở bằng TextEdit), lưu lại (Cmd+S)."
  echo "   Cách lấy key: xem HUONG-DAN.txt, mục 2."
  open -e cau-hinh.env
fi
read -r -p "Nhấn Enter để đóng"
