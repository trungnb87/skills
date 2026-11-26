---
name: video-diem-bao-bds
description: Dựng video TikTok dọc 9:16 (45–60 giây, tối đa 75 giây, công thức hiển thị 3–3–1) từ một tin bất động sản cho kênh TRUNG - buôn chuyện nhà đất của anh Trung, đọc bằng giọng nhân bản của anh, có ảnh chân dung, video nền, phụ đề, nhạc nền và ảnh cover TikTok. Dùng khi Trung đưa link bài báo và nhờ "dựng video", "làm video tin này", "video điểm báo".
---

# Video điểm báo BĐS

Người dùng: anh Trung, Giám đốc Kinh doanh BĐS hạng sang tại Hà Nội, kênh TikTok **TRUNG - buôn chuyện nhà đất** (@trungbuonchuyennhadat). Mọi chữ trong video, lời đọc và tin nhắn gửi anh đều bằng tiếng Việt.

Quy trình có **một bước duyệt bắt buộc**: viết xong kịch bản (Bước 2) thì gửi anh Trung duyệt (Bước 2b), anh OK mới tạo giọng và dựng.

Kết quả mỗi lần chạy:
1. `<ten-video>.mp4`: 1080×1920, 30 fps, **mục tiêu 45–60 giây, tối đa 75 giây**, âm lượng chuẩn TikTok (-14 LUFS).
2. `<ten-video>-cover.jpg`: ảnh cover TikTok 1080×1920.
3. Caption theo công thức ở Bước 8 + 4–5 hashtag, gửi trong tin nhắn.

## Công thức hiển thị 3–3–1 (bắt buộc)

Rút ra từ số liệu kênh 21–25/11/2026: video 56 giây về thuế đất bỏ hoang đạt 775 view; các video 68–87 giây kẹt ở khoảng 130 view; video 171–213 giây chỉ 19–37 view. Những video ăn khách đều nói thẳng vào **tiền của người xem**. Những video còn lại thì giống hệt nhau trên lưới kênh, mở đầu bằng thanh tiêu đề, và caption chỉ là tên file kèm #xuhuong.

- **3 giây móc**: cảnh 1 là *cảnh móc*, gồm chân dung lớn của anh Trung và một câu móc chữ cực lớn, hiện ngay từ khung hình đầu tiên. Không có thanh tiêu đề, nguồn hay phụ đề. Script tự hiện header từ cảnh 2.
- **3 ý**: thân video gồm đúng 3 ý, nói bằng lời "Thứ nhất…, Thứ hai…, Thứ ba…". **Trên màn hình không hiện bộ đếm hay chữ "Ý 1/3", "1/3"…** (anh Trung thấy quê); mỗi ý mở bằng một câu hỏi ngắn trong khối `kick`, ví dụ "Vì sao lại là Việt Nam?".
- **1 câu kết**: kết bằng một câu chốt mạnh, tích cực, đọng lại ý chính (khối `.ask`). **Không kêu gọi bình luận** (không "Bình luận nhé", "Để lại bình luận", "Cho biết ý kiến") và không kết bằng câu "theo dõi kênh".
- **Màu theo loại tin** (`"theme"`): `luat` đỏ · `thitruong` xanh lam · `hatang` xanh ngọc · `hangsang` vàng. Hai video đăng liền nhau không dùng cùng màu nếu khác loại tin, để lưới kênh không bị đồng một màu.
- **Câu móc** dưới 3,5 giây đọc (≤ 14 từ, khoảng 60 ký tự). Câu móc nói ai được hay mất, mất bao nhiêu, ví dụ: "Ai đang giữ đất bỏ hoang ở Hà Nội, từ năm sau mất gấp 7 lần tiền thuế!". Cấm mở bằng "Theo…", "Mới đây…", "Bản tin hôm nay…", hay tên luật hoặc nghị định.

## Thứ cần có

| Thứ | Ở đâu |
|---|---|
| Giọng nhân bản "Trung BĐS" | ElevenLabs, `voice_id = LXjvSaudzF11FKObF2RB`, model `eleven_v4`. Cần kết nối ElevenLabs trong Claude. |
| Ảnh chân dung (đã cắt tròn, làm sáng) | `assets/avatar.png` (ảnh gốc `assets/chan-dung-goc.jpg`; làm lại bằng `scripts/make_avatar.py`) |
| 10 bản nhạc nền EPIC | `assets/nhac-nen/` (bảng chọn mood ở Bước 5) |
| Video nền | Pexels qua công cụ `vidiq_find_broll` (1 credit vidIQ/lần tìm). Nếu có thư mục `~/Movies/diem-bao-bds/broll-envato` trên máy anh thì ưu tiên lấy từ đó. |
| Phần mềm | ffmpeg, Google Chrome/Chromium, `pip install playwright --break-system-packages` |

Tên miền phải được cho phép trong claude.ai › Settings › Capabilities (thiếu cái nào thì tải sẽ báo 403, nhắc anh Trung thêm đúng tên miền đó):
`videos.pexels.com`, `api.elevenlabs.io`, `elevenlabsusercontent.com`, `assets.vidiq.com`, `ai-music-tracks.s3.us-east-1.amazonaws.com`.

## Bước 1 — Chọn tin, kiểm trùng, đọc tin và kiểm số liệu

- **Chọn tin chạm tiền**: ưu tiên tin trả lời được câu "người xem được gì, mất gì, bao nhiêu" (thuế, phí, cọc, giá thuê, lãi vay, quyền bán lại). Tin vĩ mô hay hạ tầng thuần thì phải tìm được góc ảnh hưởng tới túi tiền, không tìm được thì báo anh Trung trước khi viết.
- **Kiểm trùng**: xem các thư mục trong `~/Movies/diem-bao-bds/` (dùng `device_list_dir` nếu máy đang kết nối). Không dựng lại chủ đề đã có video. Cùng một luật thì tối đa 2 video trong 7 ngày, và mỗi video phải nói một khía cạnh khác.

(Nếu anh Trung đưa sẵn kịch bản đã kiểm chứng số liệu thì bỏ qua bước này; chỉ rút kịch bản đó thành bản đọc ở Bước 2.)


- Đọc bài gốc bằng WebFetch. Ghi lại ngày đăng, nguồn dữ liệu (ví dụ Knight Frank, Bộ Xây dựng) và mọi con số.
- Chỉ dùng số có trong bài. Phân biệt dự thảo, đề xuất, đã thông qua, đã có hiệu lực.
- Không dự báo giá tăng/giảm chắc chắn, không khuyên mua bán, không quảng cáo dự án cụ thể, không trích nguyên văn quá 15 từ.

## Bước 2 — Viết lời đọc: 6–8 câu, khoảng 750–950 ký tự (45–60 giây)

Mỗi "câu" là một đoạn đọc liền mạch 1–2 câu văn, ứng với một cảnh. Khung 3–3–1:
1. **MÓC** (≤ 3,5 giây, ≤ 60 ký tự): ai được, ai mất, mất bao nhiêu. Xem quy tắc câu móc ở trên.
2. **TIN** (1 câu): chuyện gì, ai quyết định, từ khi nào, con số chính. Ghi rõ là dự thảo, đã thông qua hay đã có hiệu lực.
3–5. **3 Ý** (mỗi câu một ý, mở bằng "Thứ nhất…", "Thứ hai…", "Thứ ba…"): ai chịu ảnh hưởng, ở đâu (ưu tiên Hà Nội), bao nhiêu tiền, cần làm gì hoặc theo dõi gì. Mỗi ý có ít nhất một con số hoặc ví dụ cụ thể.
6. **GÓC NHÌN** của anh Trung (1 câu, không bắt buộc): kinh nghiệm thị trường; không phán giá, không khuyên mua bán.
7. **CÂU KẾT**: một câu chốt tích cực, gói lại ý chính hoặc mốc cần theo dõi. Ví dụ: "Một cuộc sống mới, rộng rãi hơn, đang dần thành hình ở Thư Lâm!". **Không kêu gọi bình luận**, không hỏi người xem để họ trả lời; không dùng câu "theo dõi kênh để cập nhật".

**Xưng hô trong lời đọc:** **không tự xưng** (không "em", "tôi", "Trung", không mở câu bằng "Theo tôi…"). Viết câu trung tính, nêu thẳng sự việc; gọi người xem là "anh chị" hoặc "cả nhà".

Viết số bằng chữ số như văn viết (6.188, 48%). Giọng anh sau khi script làm gọn nhịp đọc khoảng 16 ký tự/giây, nên **tổng lời đọc 750–950 ký tự, tuyệt đối không quá 1.150** (≈ 75 giây). Đếm ký tự trước khi gửi duyệt. Nếu vượt thì cắt chi tiết kỹ thuật và câu nhắc lại, giữ MÓC, con số chính, 3 ý và CÂU KẾT. Tin ít số liệu thì cứ để 40–45 giây, đừng kéo dài bằng câu chung chung. Tin quá nhiều ý thì tách thành 2 video, mỗi video một khía cạnh, đăng cách nhau.

## Bước 2b — BẮT BUỘC: gửi kịch bản cho anh Trung duyệt, chờ "OK" rồi mới dựng

Chưa được tạo giọng đọc, tìm video nền hay dựng gì khi anh Trung chưa duyệt kịch bản. Tạo giọng tốn ~700–1.000 credit ElevenLabs và không lấy lại được.

1. Gửi cho anh (SendUserMessage nếu đang giữa lượt làm việc) **một tin duy nhất**, gồm:
   - **Loại tin / màu** (`theme`), **câu móc** chữ lớn ở cảnh 1, tiêu đề ảnh cover và **caption** soạn sẵn theo Bước 8.
   - **Lời đọc** đánh số từng câu, đúng nguyên văn sẽ đọc, kèm tổng số ký tự (750–950, tối đa 1.150) và thời lượng ước tính (= số ký tự ÷ 16 giây, mục tiêu ≤ 60 giây).
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
- **Giọng cao, mạnh mẽ, tươi vui (bắt buộc, áp dụng cho mọi câu kể cả video dài):** đặt thẻ cảm xúc ở **đầu từng câu**, thiếu thẻ ở câu nào là câu đó tụt về giọng bình thường. Câu HOOK và KẾT: `[excited] [energetic]`; câu tin, số liệu, giải thích luật: `[cheerful] [energetic]`; câu chuyển phần ("Tiếp theo…", "Cuối cùng…"): `[excited] [energetic]`; câu lưu ý, cảnh báo, góc nhìn: `[energetic]`. **Không dùng `[confident]`** (làm giọng trầm và đều xuống), không dùng `[slowly]`, `[calm]`, `[serious]`. Câu HOOK, KẾT và câu nhấn mạnh kết thúc bằng `!`. Trước khi tạo giọng, rà lại prompt: câu nào không có `[energetic]` thì thêm vào.
- Nếu giọng mở đầu có tiếng cười hay tiếng thở trước câu HOOK, cắt bỏ đoạn đó khỏi voice.mp3 bằng ffmpeg trước khi dựng.
- Khi dựng, `build_video.py` tự rút khoảng nghỉ giữa các câu còn 0,3 giây và tăng tốc đọc 8% (giữ nguyên cao độ), cho video không bị dềnh dàng. Muốn chỉnh thì thêm vào spec `"voice_speed": 1.1` (nhanh hơn nữa, tối đa nên 1,15) hoặc `"voice_gap": 0.4`. Script cũng nâng cao độ giọng lên khoảng 1 cung (`"voice_pitch": 1.06` mặc định, giữ âm sắc) cho giọng cao, sáng và trẻ hơn theo yêu cầu của anh Trung; nếu vẫn thấy trầm thì đặt 1,08 (mức tối đa, cao hơn giọng bị méo). Không hạ dưới 1,06 trừ khi anh yêu cầu.
- Nhạc nền giữ âm lượng đều suốt video, không tự hạ khi anh nói; mức mặc định `music_volume` 0,10 (thấp hẳn dưới giọng), giọng được nén nhẹ cho đều và rõ. Bản nhạc nào vẫn lấn giọng thì đặt `"music_volume": 0.08`; muốn nhạc rõ hơn ở video ít lời thì nâng lên 0,14.

Chờ ~20–30 giây rồi gọi `creative_get_generations` (flow_id + generation_id) để lấy `full_res_url`, tải bằng `curl -o voice.mp3 "<url>"`. Không gọi tạo giọng lần hai để "thử lại": mỗi lần đều trừ credit.

Sau khi tải giọng, chạy `build_video.py spec.json --preview 1` và đọc dòng "Mốc cảnh … tổng". **Tổng nên ≤ 60 giây, bắt buộc ≤ 75 giây** (script in cảnh báo khi vượt 75 giây hoặc câu móc dài hơn 4 giây). Nếu lố, tăng `"voice_speed"` lên tối đa 1,15. Vẫn lố thì bỏ bớt câu khỏi `lines` và `scenes`, đồng thời cắt đoạn đó khỏi voice.mp3 bằng ffmpeg theo mốc câu script in ra (không tạo lại giọng, vì tốn credit).

Kiểm tra dòng "Mốc cảnh": cảnh nào ngắn bất thường (dưới ~3 giây cho câu dài) là script ngắt câu sai, thường gặp khi câu có dấu hỏi giữa câu. Khi đó dò khoảng lặng bằng `ffmpeg -i voice.mp3 -af silencedetect=n=-35dB:d=0.1 -f null -`, chọn đúng điểm cuối mỗi câu (giây trong file giọng gốc) và ghi vào spec `"line_breaks": [6.06, 16.27, …]` (đủ số câu trừ 1).

## Bước 4 — Chọn video nền cho từng cảnh

Video 45–60 giây có 5–7 cảnh (móc · tin · 3 ý · câu kết), mỗi cảnh 5–10 giây và một đoạn video nền riêng (không lặp lại clip giữa các cảnh). Mỗi cảnh một đoạn, dọc (`orientation: portrait`), đúng chủ đề cảnh: thành phố nhắc trong tin, tòa căn hộ, ký hợp đồng, nội thất sang trọng, công trường, cầu đường, metro... Tìm bằng `vidiq_find_broll` (tiếng Anh, ví dụ "Hanoi skyline aerial", "luxury apartment interior city view"), lấy link MP4 bản 1080×1920 và tải vào `broll/`. Không dùng cảnh có người nói thẳng vào camera hoặc có logo, chữ lớn.

## Bước 5 — Chọn nhạc nền theo mood của tin

**Nhạc nền chỉ dùng dòng EPIC, đúng phong cách bản mẫu anh Trung chọn** (video thuế Mỹ 35%, 26/11/2026): nhịp đều ~118 BPM, giọng Mi thứ, vòng hợp âm Em – C – G – D; dàn dây hoặc synth chạy liên tục nốt móc kép (16th) ngay từ giây đầu; bass rất sâu (sub ~35–45 Hz) đập đều nốt móc đơn; trống điện ảnh trầm, thưa nhưng to, nhịp chấm dôi; kèn đồng và hợp xướng ngân dài phía trên; cường độ giữ đều suốt bài, không có đoạn chùng. Không dùng nhạc lounge, lofi, jazz, deep house hay các kiểu chậm, nhẹ.

Kho có 10 bản theo công thức trên, đã cắt dạo đầu nhỏ (vào mạnh ngay giây đầu); bản nào bass mỏng đã được tăng sub-bass. Bản 02 dài ~50 giây (script tự nối vòng), các bản còn lại 2–2,5 phút.

| File | Sắc thái | Dùng cho |
|---|---|---|
| `01-epic-ban-tin-dan-day.mp3` | dàn dây dồn, kèn đồng, hợp xướng (sát bản mẫu nhất) | **mặc định**: luật mới, thuế, tin nóng |
| `02-epic-synth-arp.mp3` | synth arpeggio dồn + dàn dây | tin ngắn, thị trường biến động |
| `03-epic-taiko-horn.mp3` | taiko, horn Pháp, cello dồn | phân tích chính sách, vĩ mô |
| `04-epic-toi-cang-thang.mp3` | tối, căng, sub-bass rất nặng | cảnh báo rủi ro, siết tín dụng, sai phạm |
| `05-epic-hy-vong.mp3` | violin sáng, hy vọng | tin tích cực, người mua nhà |
| `06-epic-dien-tu-hien-dai.mp3` | synth bass, trống điện tử, kèn | công nghệ, FDI, đô thị mới |
| `07-epic-piano-dan-day.mp3` | piano dồn + dàn dây | góc nhìn, câu chuyện xã hội |
| `08-epic-a-dong.mp3` | taiko, koto, nhị | Việt Nam – Trung – Hàn – Nhật, dòng vốn châu Á |
| `09-epic-dem-nguoc.mp3` | tích tắc, va đập trầm | hạn chót, luật sắp hiệu lực |
| `10-epic-khai-hoan.mp3` | khải hoàn, kèn fanfare | tăng trưởng, hạ tầng, cơ hội lớn |

Đổi bản nhạc giữa các video liên tiếp (xoay vòng cả 10 bản, không dùng một bản 2 video liền). Muốn thêm bản mới: `vidiq_generate_music` (25 credit vidIQ, `instrumental: true`, `durationSeconds: 160`), prompt giữ nguyên công thức: "Epic cinematic hybrid news music at a steady 118 BPM in E minor, chord loop Em – C – G – D. Relentless sixteenth-note string ostinato from the first second, deep pulsing eighth-note sub-bass, big low cinematic toms in a syncopated dotted rhythm, sustained heroic brass and choir pads. Constant full intensity, no breakdown." rồi chỉ đổi nhạc cụ hoặc sắc thái. Nhạc tạo ra thường có 10–40 giây dạo đầu nhỏ: đo RMS và cắt bỏ đoạn đó (bắt đầu đúng phách, fade-in 0,05 giây); nếu bass mỏng thì tăng sub-bass (`bass=g=5:f=60`) trước khi lưu vào `assets/nhac-nen/`.

## Bước 6 — Viết spec JSON

Chuẩn bị thư mục làm việc:
```
mkdir -p work/broll work/nhac-nen && cd work
cp <skill>/assets/avatar.png . && cp <skill>/assets/nhac-nen/*.mp3 nhac-nen/
```
Viết `spec.json` theo mẫu `examples/knight-frank.json`:
- `theme`: `luat` | `thitruong` | `hatang` | `hangsang` (màu nhấn + nhãn mặc định "LUẬT MỚI", "THỊ TRƯỜNG", "HẠ TẦNG", "HẠNG SANG"; đổi nhãn bằng `tag`).
- `hook`: mặc định `true`, khi đó cảnh 1 là cảnh móc. Script tự chèn chân dung lớn và tên kênh lên đầu cảnh. Trong `html` cảnh 1 chỉ cần:
  `<div class="h0">Đất bỏ hoang: thuế <span class="gold">gấp 7 lần</span></div><div class="hooksub" data-fx="up" data-at="0.8">Ai đang giữ đất ở Hà Nội cần nghe ngay</div>`
  Khối `h0` (≤ 8 từ, in hoa tự động) **không gắn `data-fx`**, để chữ có ngay ở khung hình đầu tiên (TikTok lấy khung này làm ảnh xem trước trên bảng tin). Cảnh 1 chỉ bao câu MÓC.
- Ở 3 cảnh ý: **không** thêm `"step"` (không hiện bộ đếm); mở cảnh bằng khối `kick` là câu hỏi ngắn của ý đó.
- Cảnh cuối: `<div class="kick" …>Góc nhìn của Trung</div><div class="ask" data-fx="pop" data-at="0.3">Câu chốt ngắn!</div>`.
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
python3 <skill>/scripts/build_video.py spec.json --preview 0 2 8 18 28 38 48 58   # ảnh trong _build/, xem bằng Read
python3 <skill>/scripts/build_video.py spec.json                        # ~3 phút cho video 1 phút
python3 <skill>/scripts/make_cover.py spec.json                         # ra <out>-cover.jpg
```
Kiểm tra ảnh xem trước: ảnh giây 0 phải thấy ngay chân dung và câu móc (không trống), chữ không tràn, không chồng lên nhau, khối thông tin không đè phụ đề. Sau khi dựng, rút vài khung hình bằng ffmpeg để xem lại và xem ảnh cover. Script báo lỗi "không đủ khoảng nghỉ" thì tạo lại giọng với `[pause]` rõ hơn giữa các câu.

## Bước 8 — Giao cho anh Trung

- Mỗi video có **một thư mục riêng** trong `~/Movies/diem-bao-bds/`, đặt tên `YYYY-MM-DD-<ten-video>` (ngày dựng + tên không dấu, ví dụ `2026-11-21-xang-giam-30-nha-dat-duoc-loi-gi`). Trong thư mục có đủ:
  - `<ten-video>.mp4`: video
  - `<ten-video>-cover.jpg`: ảnh cover
  - `thong-tin.txt`: tiêu đề TikTok, caption, hashtag, dòng "Video nền: Pexels", nguồn bài báo, credit đã dùng
  Các bản sửa của cùng một video (v2, v3…) để chung thư mục đó, không để file lẻ ở ngoài thư mục `diem-bao-bds`.
- Gửi video, cover và `thong-tin.txt` bằng SendUserFile. Nếu máy anh đang kết nối, lưu cả ba vào thư mục riêng ở trên bằng `device_commit_files` (dùng `fileUuid` từ SendUserFile, `devicePath` = `~/Movies/diem-bao-bds/<thu-muc>/<ten-file>`; công cụ tự tạo thư mục). Nếu máy không kết nối, báo anh rằng file chỉ có trong chat.
- **Caption** (đặt lên đầu `thong-tin.txt` và tin nhắn để anh copy dán thẳng; **không bao giờ dùng tên file hay slug làm caption**):
  - Dòng 1: nhắc lại câu móc, có con số.
  - Dòng 2: một câu nói rõ người xem được gì khi xem hết ("3 nhóm bị ảnh hưởng, nhóm thứ 3 nhiều người không biết").
  - Dòng 3: câu chốt, giống câu cuối trong video (không kêu gọi bình luận).
  - Hashtag: 4–5 thẻ đúng chủ đề, luôn có `#batdongsanhanoi` và `#buonchuyennhadat`, cộng 2–3 thẻ theo tin (ví dụ `#luatdatdai` `#thuedat` `#chungcuhanoi`). **Không dùng** `#xuhuong`, `#xuhuongtiktok`, `#trendingnow`: các thẻ này không giúp TikTok hiểu video thuộc chủ đề nào.
- Kèm trong tin nhắn: tiêu đề TikTok (IN HOA), caption ở trên, dòng "Video nền: Pexels", nguồn bài báo, và gợi ý giờ đăng (11h30–12h30 hoặc 19h30–21h30, tối đa 2 video/ngày, cách nhau ít nhất 4 tiếng).
- Chạy tự động theo lịch: báo ngắn tiêu đề video đã dựng, credit đã dùng và lỗi nếu có.

## Chi phí mỗi video (45–60 giây)

- ElevenLabs: ~700–1.000 credit (khoảng 900 credit/1.000 ký tự). Gói Starter 40.000 credit/tháng ≈ 40–50 video. Báo anh Trung khi credit tháng còn dưới 5.000.
- vidIQ: ~5–7 credit tìm video nền (gói 2.000 credit/tháng).
- Nhạc nền: dùng lại thư viện, không tốn thêm.
