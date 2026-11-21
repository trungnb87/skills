---
name: video-diem-bao-bds
description: Dựng video TikTok dọc 9:16 (~50–60 giây) từ một tin bất động sản cho kênh TRUNGNB - BUÔN CHUYỆN BĐS của anh Trung, đọc bằng giọng nhân bản của anh, có ảnh chân dung, video nền, phụ đề, nhạc nền và ảnh cover TikTok. Dùng khi Trung đưa link bài báo và nhờ "dựng video", "làm video tin này", "video điểm báo", hoặc khi skill kich-ban-tiktok-bds gọi đến để dựng video cho bài gợi ý quay trước.
---

# Video điểm báo BĐS

Người dùng: anh Trung, Giám đốc Kinh doanh BĐS hạng sang tại Hà Nội, kênh **TRUNGNB - BUÔN CHUYỆN BĐS**. Mọi chữ trong video, lời đọc và tin nhắn gửi anh đều bằng tiếng Việt.

Kết quả mỗi lần chạy:
1. `<ten-video>.mp4`: 1080×1920, 30 fps, ~50–60 giây, âm lượng chuẩn TikTok (-14 LUFS).
2. `<ten-video>-cover.jpg`: ảnh cover TikTok 1080×1920.
3. Caption + 5 hashtag, gửi trong tin nhắn.

## Thứ cần có

| Thứ | Ở đâu |
|---|---|
| Giọng nhân bản "Trung BĐS" | ElevenLabs, `voice_id = LXjvSaudzF11FKObF2RB`, model `eleven_v4`. Cần kết nối ElevenLabs trong Claude. |
| Ảnh chân dung (đã cắt tròn, làm sáng) | `assets/avatar.png` (ảnh gốc `assets/chan-dung-goc.jpg`; làm lại bằng `scripts/make_avatar.py`) |
| 6 bản nhạc nền | `assets/nhac-nen/` (bảng chọn mood ở Bước 5) |
| Video nền | Pexels qua công cụ `vidiq_find_broll` (1 credit vidIQ/lần tìm). Nếu có thư mục `~/Movies/diem-bao-bds/broll-envato` trên máy anh thì ưu tiên lấy từ đó. |
| Phần mềm | ffmpeg, Google Chrome/Chromium, `pip install playwright --break-system-packages` |

Tên miền phải được cho phép trong claude.ai › Settings › Capabilities (thiếu cái nào thì tải sẽ báo 403, nhắc anh Trung thêm đúng tên miền đó):
`videos.pexels.com`, `api.elevenlabs.io`, `elevenlabsusercontent.com`, `assets.vidiq.com`, `ai-music-tracks.s3.us-east-1.amazonaws.com`.

## Bước 1 — Đọc tin và kiểm số liệu

(Bỏ qua bước này khi được gọi từ `kich-ban-tiktok-bds`: tin đã được kiểm chứng ở đó; chỉ rút kịch bản sẵn có thành bản đọc ở Bước 2.)


- Đọc bài gốc bằng WebFetch. Ghi lại ngày đăng, nguồn dữ liệu (ví dụ Knight Frank, Bộ Xây dựng) và mọi con số.
- Chỉ dùng số có trong bài. Phân biệt dự thảo, đề xuất, đã thông qua, đã có hiệu lực.
- Không dự báo giá tăng/giảm chắc chắn, không khuyên mua bán, không quảng cáo dự án cụ thể, không trích nguyên văn quá 15 từ.

## Bước 2 — Viết lời đọc: 6–8 câu, tổng dưới 1.000 ký tự

Mỗi "câu" là một đoạn đọc liền mạch, ứng với một cảnh hoặc một phần cảnh:
1. HOOK (≤ 5 giây): một con số hoặc nghịch lý gây tò mò.
2–5. TIN và VÌ SAO QUAN TRỌNG: mỗi câu một ý, có số.
6. Nhận định ngắn, không phán giá.
7. Kết: "Theo dõi kênh để cập nhật thị trường mỗi ngày." (hoặc câu tương tự).

Viết số bằng chữ số như văn viết (6.188, 48%). Giữ tổng dưới 1.000 ký tự: ~50 giây đọc và ~800 credit ElevenLabs.

## Bước 3 — Tạo giọng đọc bằng giọng nhân bản

Gọi `creative_generate_speech` (ElevenLabs) với:
- `voice_id`: `LXjvSaudzF11FKObF2RB`, `model_id`: `eleven_v4`, `generations_count`: 1.
- `prompt`: các câu nối nhau, **thêm ` [pause]` ở cuối mỗi câu trừ câu cuối và xuống dòng**. Script dựng dựa vào các khoảng nghỉ này để căn hình.
- **Giọng tươi, nhịp nhanh:** mở đầu `prompt` bằng `[cheerful] [energetic]` (thẻ giữ hiệu lực cho cả bài). Câu HOOK và câu KẾT kết thúc bằng dấu `!` thay cho dấu chấm. Không dùng `[slowly]`.
- Khi dựng, `build_video.py` tự rút khoảng nghỉ giữa các câu còn 0,3 giây và tăng tốc đọc 8% (giữ nguyên cao độ), cho video không bị dềnh dàng. Muốn chỉnh thì thêm vào spec `"voice_speed": 1.1` (nhanh hơn nữa, tối đa nên 1,15) hoặc `"voice_gap": 0.4`.

Chờ ~20–30 giây rồi gọi `creative_get_generations` (flow_id + generation_id) để lấy `full_res_url`, tải bằng `curl -o voice.mp3 "<url>"`. Không gọi tạo giọng lần hai để "thử lại": mỗi lần đều trừ credit.

## Bước 4 — Chọn video nền cho từng cảnh

Mỗi cảnh một đoạn, dọc (`orientation: portrait`), đúng chủ đề cảnh: thành phố nhắc trong tin, tòa căn hộ, ký hợp đồng, nội thất sang trọng, công trường, cầu đường, metro... Tìm bằng `vidiq_find_broll` (tiếng Anh, ví dụ "Hanoi skyline aerial", "luxury apartment interior city view"), lấy link MP4 bản 1080×1920 và tải vào `broll/`. Không dùng cảnh có người nói thẳng vào camera hoặc có logo, chữ lớn.

## Bước 5 — Chọn nhạc nền theo mood của tin

| File | Mood | Dùng cho |
|---|---|---|
| `01-tin-tuc-chuyen-nghiep.mp3` | chuyên nghiệp, chắc chắn | số liệu thị trường, báo cáo (mặc định) |
| `02-vui-tuoi.mp3` | tươi sáng, năng động | mở bán, ưu đãi, tin tích cực |
| `03-sang-trong-lounge.mp3` | jazz lounge sang trọng | dự án, phân khúc hạng sang |
| `04-truyen-cam-hung.mp3` | điện ảnh, lạc quan | hạ tầng, quy hoạch, cơ hội |
| `05-kich-tinh-tin-nong.mp3` | khẩn trương, nghiêm túc | luật mới, siết tín dụng, biến động |
| `06-thu-gian-lofi.mp3` | nhẹ nhàng | kiến thức, mẹo, nội dung cuối tuần |

Muốn thêm mood: `vidiq_generate_music` (25 credit vidIQ, `instrumental: true`, `durationSeconds: 60`), lưu vào `assets/nhac-nen/`.

## Bước 6 — Viết spec JSON

Chuẩn bị thư mục làm việc:
```
mkdir -p work/broll work/nhac-nen && cd work
cp <skill>/assets/avatar.png . && cp <skill>/assets/nhac-nen/*.mp3 nhac-nen/
```
Viết `spec.json` theo mẫu `examples/knight-frank.json`:
- `date` (dd.mm.yyyy hôm nay), `source` ("Nguồn: … · Tên báo dd/mm/yyyy"), `voice`, `music`, `avatar`, `out`.
- `lines`: đúng các câu ở Bước 2, cùng thứ tự (dùng làm phụ đề).
- `highlight`: từ khóa tô vàng trong phụ đề (số được tô tự động).
- `scenes`: mỗi cảnh có `lines` (chỉ số câu cảnh đó bao phủ), `broll`, `broll_offset` (giây bắt đầu trong clip), `html`.
- `cover`: `title` (in hoa tự động, `<em>` tô vàng, ≤ 9 từ, gây tò mò), `kicker`, `number`, `number_label`.

**Thành phần dùng trong `html` của cảnh** (vùng an toàn rộng 820px, cao 1000px):
- `<div class="kick">` nhãn nhỏ vàng · `<div class="h1">` / `h2` tiêu đề · `<div class="body">` đoạn văn · `<span class="gold">` tô vàng
- `<div class="huge">48%</div>` số cực lớn · `<div class="big" data-count="6188" data-dur="2.2">0</div>` số chạy đếm
- Thanh so sánh: `<div class="row"><div class="lab">Tên <b>48%</b></div><div class="track"><div class="fill" style="--w:1" data-fx="grow" data-at="0.5"></div></div></div>` (`--w` = tỷ lệ so với thanh dài nhất; `row dim` cho thanh xám)
- `<div class="stat"><div class="n">158</div><div class="t">mô tả</div></div>` con số kèm chú thích
- `<div class="rank">` / `rank me` (dòng nổi bật) với `<span class="no">1</span>` bảng xếp hạng
- `<div class="chips"><div class="chip"><div class="k">nhãn</div><div class="v">7,5/10</div><div class="s">ghi chú</div></div>…</div>`
- `<div class="badge">` khung kết luận
- Hiệu ứng: thêm `data-fx="up|pop|fade|grow"` và `data-at="<giây tính từ đầu cảnh>"`. Đặt `data-at` theo lúc giọng đọc nhắc tới ý đó (ước theo tỷ lệ ký tự trong câu).

Tối đa ~3 khối thông tin mỗi cảnh; chữ phải đọc được trên điện thoại.

## Bước 7 — Xem trước, rồi dựng

```
python3 <skill>/scripts/build_video.py spec.json --preview 3 15 30 45   # ảnh trong _build/, xem bằng Read
python3 <skill>/scripts/build_video.py spec.json                        # ~3 phút cho video 55 giây
python3 <skill>/scripts/make_cover.py spec.json                         # ra <out>-cover.jpg
```
Kiểm tra ảnh xem trước: chữ không tràn, không chồng lên nhau, khối thông tin không đè phụ đề. Sau khi dựng, rút vài khung hình bằng ffmpeg để xem lại và xem ảnh cover. Script báo lỗi "không đủ khoảng nghỉ" thì tạo lại giọng với `[pause]` rõ hơn giữa các câu.

## Bước 8 — Giao cho anh Trung

- Mỗi video có **một thư mục riêng** trong `~/Movies/diem-bao-bds/`, đặt tên `YYYY-MM-DD-<ten-video>` (ngày dựng + tên không dấu, ví dụ `2026-11-21-xang-giam-30-nha-dat-duoc-loi-gi`). Trong thư mục có đủ:
  - `<ten-video>.mp4`: video
  - `<ten-video>-cover.jpg`: ảnh cover
  - `thong-tin.txt`: tiêu đề TikTok, caption, hashtag, dòng "Video nền: Pexels", nguồn bài báo, credit đã dùng
  Các bản sửa của cùng một video (v2, v3…) để chung thư mục đó, không để file lẻ ở ngoài thư mục `diem-bao-bds`.
- Gửi video, cover và `thong-tin.txt` bằng SendUserFile. Nếu máy anh đang kết nối, lưu cả ba vào thư mục riêng ở trên bằng `device_commit_files` (dùng `fileUuid` từ SendUserFile, `devicePath` = `~/Movies/diem-bao-bds/<thu-muc>/<ten-file>`; công cụ tự tạo thư mục). Nếu máy không kết nối, báo anh rằng file chỉ có trong chat.
- Kèm trong tin nhắn: tiêu đề TikTok (IN HOA), caption 2–3 câu, 5 hashtag (luôn có `#batdongsanhanoi` và `#trungbds`), dòng "Video nền: Pexels", nguồn bài báo.
- Chạy tự động theo lịch: báo ngắn tiêu đề video đã dựng, credit đã dùng và lỗi nếu có.

## Chi phí mỗi video

- ElevenLabs: ~800 credit/1.000 ký tự lời đọc (gói Starter 40.000 credit/tháng ≈ 45–50 video).
- vidIQ: ~5–6 credit tìm video nền (gói 2.000 credit/tháng).
- Nhạc nền: dùng lại thư viện, không tốn thêm.
