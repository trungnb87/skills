---
name: video-diem-bao-bds
description: Dựng video TikTok dọc 9:16 (tối đa 1 phút 30, có phân tích) từ một tin bất động sản cho kênh TRUNG - BUÔN CHUYỆN BĐS của anh Trung, đọc bằng giọng nhân bản của anh, có ảnh chân dung, video nền, phụ đề, nhạc nền và ảnh cover TikTok. Dùng khi Trung đưa link bài báo và nhờ "dựng video", "làm video tin này", "video điểm báo".
---

# Video điểm báo BĐS

Người dùng: anh Trung, Giám đốc Kinh doanh BĐS hạng sang tại Hà Nội, kênh **TRUNG - BUÔN CHUYỆN BĐS**. Mọi chữ trong video, lời đọc và tin nhắn gửi anh đều bằng tiếng Việt.

Quy trình có **một bước duyệt bắt buộc**: viết xong kịch bản (Bước 2) thì gửi anh Trung duyệt (Bước 2b), anh OK mới tạo giọng và dựng.

Kết quả mỗi lần chạy:
1. `<ten-video>.mp4`: 1080×1920, 30 fps, **không quá 1 phút 30** (mục tiêu 1 phút 15 – 1 phút 30), âm lượng chuẩn TikTok (-14 LUFS).
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

(Nếu anh Trung đưa sẵn kịch bản đã kiểm chứng số liệu thì bỏ qua bước này; chỉ rút kịch bản đó thành bản đọc ở Bước 2.)


- Đọc bài gốc bằng WebFetch. Ghi lại ngày đăng, nguồn dữ liệu (ví dụ Knight Frank, Bộ Xây dựng) và mọi con số.
- Chỉ dùng số có trong bài. Phân biệt dự thảo, đề xuất, đã thông qua, đã có hiệu lực.
- Không dự báo giá tăng/giảm chắc chắn, không khuyên mua bán, không quảng cáo dự án cụ thể, không trích nguyên văn quá 15 từ.
- **Nhận định, dự báo, đề xuất của chuyên gia hay tổ chức phải nêu tên ngay trong lời đọc** ("theo ông…, Phó Chủ tịch…", "Knight Frank cảnh báo…", "theo đề xuất của HoREA…") và ghi tên đơn vị trên màn hình. Không viết lại thành câu khẳng định như thể đó là nhận định của anh Trung. Khi gửi kịch bản duyệt, đánh dấu câu nào là ý của ai.

## Bước 2 — Viết lời đọc: 10–12 câu, khoảng 1.200–1.400 ký tự (tối đa 1 phút 30)

Mỗi "câu" là một đoạn đọc liền mạch 1–2 câu văn, ứng với một cảnh (câu dài có thể chiếm cả cảnh). Khung chuẩn:
1. **HOOK** (≤ 5 giây): một con số hoặc nghịch lý gây tò mò.
2–4. **TIN**: chuyện gì xảy ra, ai quyết định, khi nào, con số chính.
5–7. **BỐI CẢNH / SỐ LIỆU**: so sánh trước–sau, với nước khác, với cùng kỳ; con số phụ giúp hiểu quy mô.
8–12. **PHÂN TÍCH TÁC ĐỘNG** (mỗi câu một ý, đánh số "Thứ nhất…"): người mua ở thực · nhà đầu tư · khu vực/phân khúc nào chịu ảnh hưởng (ưu tiên Hà Nội) · dòng tiền, lãi suất, pháp lý · rủi ro cần lưu ý.
13–14. **GÓC NHÌN** của anh Trung từ kinh nghiệm thị trường hạng sang: nên theo dõi gì tiếp, lời khuyên thận trọng cho người mua. Không tự dự báo thị trường, không phán giá, không khuyên mua bán.
15. **KẾT**: hẹn cập nhật + kêu gọi theo dõi kênh.

Viết số bằng chữ số như văn viết (6.188, 48%). Giọng anh sau khi script làm gọn nhịp đọc khoảng 16 ký tự/giây, nên **tổng lời đọc không quá 1.400 ký tự** (≈ 1 phút 25 cả phần đuôi). Đếm ký tự trước khi gửi duyệt; vượt thì cắt bớt ý phụ (chi tiết kỹ thuật, câu nhắc lại), giữ HOOK, số liệu chính, 2–3 ý phân tích và KẾT. Phần TIN gọn trong 4–5 câu, PHÂN TÍCH và GÓC NHÌN 3–4 câu. Tin ít số liệu thì cứ để video 1 phút, đừng kéo dài bằng câu chung chung.

## Bước 2b — BẮT BUỘC: gửi kịch bản cho anh Trung duyệt, chờ "OK" rồi mới dựng

Chưa được tạo giọng đọc, tìm video nền hay dựng gì khi anh Trung chưa duyệt kịch bản. Tạo giọng tốn ~1.200–1.400 credit ElevenLabs và không lấy lại được.

1. Gửi cho anh (SendUserMessage nếu đang giữa lượt làm việc) **một tin duy nhất**, gồm:
   - **Tiêu đề TikTok** (IN HOA) và tiêu đề ảnh cover.
   - **Lời đọc** đánh số từng câu, đúng nguyên văn sẽ đọc, kèm tổng số ký tự (≤ 1.400) và thời lượng ước tính (= số ký tự ÷ 16 giây, phải ≤ 90 giây).
   - **Kế hoạch cảnh** ngắn gọn: mỗi cảnh một dòng (câu nào · hiển thị gì · video nền định dùng).
   - **Nhạc nền** định dùng, **nguồn** đã đối chiếu, và các **lưu ý** (số liệu chỉ có 1 nguồn, ví dụ minh họa, chỗ còn băn khoăn).
   - Dòng cuối: *"Anh nhắn OK để em dựng, hoặc ghi chỗ cần sửa."*
2. **Dừng lại và kết thúc lượt**, chờ anh trả lời. Không chạy trước Bước 3 "cho nhanh".
3. Anh sửa thì cập nhật kịch bản, gửi lại phần đã đổi và chờ OK lần nữa. Chỉ coi là duyệt khi chính anh nhắn đồng ý ("OK", "duyệt", "dựng đi", "được"…) cho đúng bản kịch bản mới nhất.
4. Chạy theo lịch hoặc không có ai trả lời: chỉ gửi kịch bản chờ duyệt, **không dựng video**. Khi anh nhắn OK ở lượt sau thì làm tiếp từ Bước 3.

Ngoại lệ duy nhất: anh nói rõ trong chính yêu cầu là không cần duyệt (ví dụ "dựng luôn, không cần gửi kịch bản"), hoặc chỉ nhờ sửa hình, nhạc, bố cục của một video mà lời đọc đã được duyệt trước đó.

## Bước 3 — Tạo giọng đọc bằng giọng nhân bản

Gọi `creative_generate_speech` (ElevenLabs) với:
- `voice_id`: `LXjvSaudzF11FKObF2RB`, `model_id`: `eleven_v4`, `generations_count`: 1.
- `prompt`: các câu nối nhau, **thêm ` [pause]` ở cuối mỗi câu trừ câu cuối và xuống dòng**. Script dựng dựa vào các khoảng nghỉ này để căn hình.
- **Giọng tươi vui, mạnh mẽ, nhiều năng lượng (bắt buộc):** đặt thẻ cảm xúc ở **đầu từng câu**, không chỉ đầu bài, vì thiếu thẻ thì giọng bị nhạt. Câu HOOK và KẾT: `[excited] [energetic]`; câu tin và số liệu: `[energetic]`; câu "Thứ nhất/Thứ hai…": `[cheerful] [energetic]`; câu lưu ý, cảnh báo: `[confident]`. Câu HOOK, KẾT và các câu nhấn mạnh kết thúc bằng `!`. Không dùng `[slowly]`, `[calm]`.
- Nếu giọng mở đầu có tiếng cười hay tiếng thở trước câu HOOK, cắt bỏ đoạn đó khỏi voice.mp3 bằng ffmpeg trước khi dựng.
- Khi dựng, `build_video.py` tự rút khoảng nghỉ giữa các câu còn 0,3 giây và tăng tốc đọc 8% (giữ nguyên cao độ), cho video không bị dềnh dàng. Muốn chỉnh thì thêm vào spec `"voice_speed": 1.1` (nhanh hơn nữa, tối đa nên 1,15) hoặc `"voice_gap": 0.4`. Script cũng nâng cao độ giọng lên khoảng 0,7 cung (`"voice_pitch": 1.04`, giữ âm sắc) cho giọng sáng và trẻ hơn; muốn cao hơn nữa thì đặt 1,06, không vượt 1,08 để giọng không bị méo.
- Nhạc nền giữ âm lượng đều suốt video, không tự hạ khi anh nói; mức mặc định `music_volume` 0,10 (thấp hẳn dưới giọng), giọng được nén nhẹ cho đều và rõ. Bản nhạc nào vẫn lấn giọng thì đặt `"music_volume": 0.08`; muốn nhạc rõ hơn ở video ít lời thì nâng lên 0,14.

Chờ ~20–30 giây rồi gọi `creative_get_generations` (flow_id + generation_id) để lấy `full_res_url`, tải bằng `curl -o voice.mp3 "<url>"`. Không gọi tạo giọng lần hai để "thử lại": mỗi lần đều trừ credit.

Sau khi tải giọng, chạy `build_video.py spec.json --preview 1` và đọc dòng "Mốc cảnh … tổng". **Tổng phải ≤ 90 giây.** Nếu lố, tăng `"voice_speed"` lên tối đa 1,15. Vẫn lố thì bỏ bớt câu khỏi `lines` và `scenes`, đồng thời cắt đoạn đó khỏi voice.mp3 bằng ffmpeg theo mốc câu script in ra (không tạo lại giọng, vì tốn credit).

Kiểm tra dòng "Mốc cảnh": cảnh nào ngắn bất thường (dưới ~3 giây cho câu dài) là script ngắt câu sai, thường gặp khi câu có dấu hỏi giữa câu. Khi đó dò khoảng lặng bằng `ffmpeg -i voice.mp3 -af silencedetect=n=-35dB:d=0.1 -f null -`, chọn đúng điểm cuối mỗi câu (giây trong file giọng gốc) và ghi vào spec `"line_breaks": [6.06, 16.27, …]` (đủ số câu trừ 1).

## Bước 4 — Chọn video nền cho từng cảnh

Video 1 phút 30 có 8–10 cảnh, mỗi cảnh 7–10 giây và một đoạn video nền riêng (không lặp lại clip giữa các cảnh). Mỗi cảnh một đoạn, dọc (`orientation: portrait`), đúng chủ đề cảnh: thành phố nhắc trong tin, tòa căn hộ, ký hợp đồng, nội thất sang trọng, công trường, cầu đường, metro... Tìm bằng `vidiq_find_broll` (tiếng Anh, ví dụ "Hanoi skyline aerial", "luxury apartment interior city view"), lấy link MP4 bản 1080×1920 và tải vào `broll/`. Không dùng cảnh có người nói thẳng vào camera hoặc có logo, chữ lớn.

## Bước 5 — Chọn nhạc nền theo mood của tin

Bản 07–16 dài ~2 phút, đủ cho cả video (script tự mờ dần nhạc ở cuối). Bản 01–06 dài ~1 phút, script tự nối vòng có chồng mờ 3 giây nên vẫn dùng được.

| File | Mood | Dùng cho |
|---|---|---|
| `01-tin-tuc-chuyen-nghiep.mp3` | chuyên nghiệp, chắc chắn | số liệu thị trường, báo cáo |
| `02-vui-tuoi.mp3` | tươi sáng, năng động | mở bán, ưu đãi, tin tích cực |
| `03-sang-trong-lounge.mp3` | jazz lounge sang trọng | dự án, phân khúc hạng sang |
| `04-truyen-cam-hung.mp3` | điện ảnh, lạc quan | hạ tầng, quy hoạch, cơ hội |
| `05-kich-tinh-tin-nong.mp3` | khẩn trương, nghiêm túc | luật mới, siết tín dụng, biến động |
| `06-thu-gian-lofi.mp3` | nhẹ nhàng | kiến thức, mẹo, nội dung cuối tuần |
| `07-ban-tin-tai-chinh.mp3` | bản tin tài chính, chắc chắn | báo cáo thị trường, số liệu quý (mặc định) |
| `08-phan-tich-kinh-te.mp3` | tò mò, thông minh | giải thích chính sách, phân tích vĩ mô |
| `09-tang-truong-cong-nghe.mp3` | lạc quan, tiến lên | tăng trưởng, FDI, khu công nghiệp, công nghệ |
| `10-deep-house-sang-trong.mp3` | sang, hiện đại về đêm | hạng sang, căn hộ hàng hiệu, Tây Hồ |
| `11-dieu-tra-rui-ro.mp3` | nghiêm, hồi hộp | cảnh báo rủi ro, sai phạm, pháp lý dự án |
| `12-so-lieu-toi-gian.mp3` | tối giản, chính xác | tin nhiều biểu đồ, so sánh số liệu |
| `13-ban-tin-sang-soi-dong.mp3` | sôi động, tích cực | điểm tin sáng, tin tốt ngắn |
| `14-ha-tang-do-thi.mp3` | hoành tráng, hy vọng | metro, cầu, vành đai, quy hoạch đô thị |
| `15-neo-soul-chuyen-gia.mp3` | thư thả, tự tin | góc nhìn chuyên gia, kinh nghiệm mua nhà |
| `16-kinh-te-a-dong.mp3` | Á Đông hiện đại | Việt Nam – Hàn – Trung – Nhật, dòng vốn châu Á |

Đổi bản nhạc giữa các video liên tiếp, đừng dùng một bản nhiều ngày liền. Muốn thêm mood: `vidiq_generate_music` (25 credit vidIQ, `instrumental: true`, `durationSeconds: 100`), lưu vào `assets/nhac-nen/`.

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

**Thành phần dùng trong `html` của cảnh** (vùng an toàn rộng 780px, cao 780px, đã đo theo giao diện TikTok trên iPhone):
- `<div class="kick">` nhãn nhỏ vàng · `<div class="h1">` / `h2` tiêu đề · `<div class="body">` đoạn văn · `<span class="gold">` tô vàng
- `<div class="huge">48%</div>` số cực lớn · `<div class="big" data-count="6188" data-dur="2.2">0</div>` số chạy đếm
- Thanh so sánh: `<div class="row"><div class="lab">Tên <b>48%</b></div><div class="track"><div class="fill" style="--w:1" data-fx="grow" data-at="0.5"></div></div></div>` (`--w` = tỷ lệ so với thanh dài nhất; `row dim` cho thanh xám)
- `<div class="stat"><div class="n">158</div><div class="t">mô tả</div></div>` con số kèm chú thích
- `<div class="rank">` / `rank me` (dòng nổi bật) với `<span class="no">1</span>` bảng xếp hạng
- `<div class="chips"><div class="chip"><div class="k">nhãn</div><div class="v">7,5/10</div><div class="s">ghi chú</div></div>…</div>`
- `<div class="badge">` khung kết luận
- Hiệu ứng: thêm `data-fx` và `data-at="<giây tính từ đầu cảnh>"`. Đặt `data-at` theo lúc giọng đọc nhắc tới ý đó (ước theo tỷ lệ ký tự trong câu, nhân 0,9 vì script đọc nhanh hơn 8%).

**Bộ hiệu ứng chữ** (`data-fx`):

| Nhóm | Giá trị | Hợp với |
|---|---|---|
| Hiện cả khối | `up` · `left` · `right` · `drop` (rơi xuống, nảy nhẹ) · `flip` (lật) · `fade` | nhãn, khối `stat`, `chip`, `rank`, `badge` |
| Lộ dần | `wipe` (quét từ trái) · `wipeup` (lộ từ dưới) | dòng tiêu đề phụ, thanh, chip |
| Gây chú ý | `zoom` (phóng to rồi nét lại) · `blur` (mờ thành nét) · `pop` | số lớn `huge`, `big` |
| Theo chữ | `words` (từng chữ nhô lên, chỉnh `data-stagger`) · `type` (gõ từng ký tự) | `h1`, `h2`, câu nhận định; `type` cho `kick` |
| Tô sáng | `marker` (bút dạ vàng tô dưới chữ): đặt trên một `<span>` nằm trong khối chữ, ví dụ `<div class="body"><span data-fx="marker" data-at="1.5">ý chính</span></div>` | ý quan trọng nhất của cảnh |
| Thanh | `grow` | `.fill` trong thanh so sánh |

Nhấn mạnh sau khi hiện (`data-emph`): `pulse` (đập nhẹ) hoặc `shine` (ánh sáng lướt qua chữ vàng), dùng cho con số chủ chốt.

Chuyển cảnh (`data-trans` trên cảnh, khai báo bằng `"trans"` trong spec nếu cần): `slide` · `zoom` · `wipe` · `rise` · `blur` · `fade`. Bỏ trống thì script tự xoay vòng, cảnh nào cũng khác cảnh trước; mỗi lần sang cảnh có vạch vàng quét ngang.

**Quy tắc để video không đơn điệu:**
- Mỗi cảnh dùng ít nhất 2 kiểu hiệu ứng khác nhau; hai cảnh liền nhau không mở đầu bằng cùng một hiệu ứng.
- Mỗi kiểu `words`, `type`, `zoom`, `marker` xuất hiện ít nhất 1 lần trong video; không dùng một kiểu quá 3 cảnh.
- Số liệu chủ chốt của video (thường ở HOOK và cảnh tin chính) dùng `zoom` hoặc `blur` kèm `data-emph`.
- Đổi dạng thông tin giữa các cảnh: số lớn → thanh so sánh → chip → xếp hạng → câu nhận định, tránh 3 cảnh liền chỉ có chữ.

Tối đa ~3 khối thông tin mỗi cảnh, tổng chiều cao không quá 780px (ví dụ 3 khối `stat`, hoặc `huge` + 1 dòng `h2` + `badge`); chữ phải đọc được trên điện thoại. Không đặt chữ sát mép: TikTok cắt khoảng 55px mỗi bên, thanh tìm kiếm che ~230px trên cùng, cột nút che bên phải từ giữa màn hình xuống.

## Bước 7 — Xem trước, rồi dựng

```
python3 <skill>/scripts/build_video.py spec.json --preview 3 15 30 45 60 75 90 105   # ảnh trong _build/, xem bằng Read
python3 <skill>/scripts/build_video.py spec.json                        # ~5 phút cho video 1 phút 30
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

## Chi phí mỗi video (1 phút 30)

- ElevenLabs: ~1.200–1.400 credit (khoảng 900 credit/1.000 ký tự). Gói Starter 40.000 credit/tháng ≈ 28–30 video, đủ đăng gần như mỗi ngày. Báo anh Trung khi credit tháng còn dưới 5.000.
- vidIQ: ~8–10 credit tìm video nền (gói 2.000 credit/tháng).
- Nhạc nền: dùng lại thư viện, không tốn thêm.
