# Skill bất động sản của Trung

Kho lưu skill Claude dùng cho công việc bất động sản:

| Skill | Việc làm |
|---|---|
| `kich-ban-tiktok-bds` | Viết kịch bản TikTok BĐS Hà Nội để Trung tự đọc: 5 tin nóng 24–48 giờ, hoặc 1 bài phân tích vĩ mô – vi mô – luật pháp tác động tới BĐS Việt Nam, Hà Nội và 4 phân khúc (thấp, trung, cao cấp, hạng sang). Kiểm chứng số liệu, có mốc so sánh, viết văn nói. Chỉ viết kịch bản, không tự dựng video |
| `video-diem-bao-bds` | Dựng video TikTok 9:16 dài 45–60 giây theo công thức hiển thị 3–3–1 (3 giây móc có chân dung, 3 ý đánh số, 1 câu hỏi kết; màu theo loại tin) từ một tin BĐS, gửi kịch bản để anh duyệt trước khi dựng: giọng nhân bản của Trung (ElevenLabs), ảnh chân dung, video nền, phụ đề, 10 bản nhạc nền EPIC theo mood, bộ hiệu ứng chữ và chuyển cảnh đa dạng, ảnh cover |

## Cài vào Claude Code (một lần)

Trong Claude Code, gõ:

```
/plugin marketplace add trungnb87/skills
/plugin install bds-trung@trungnb87-skills
```

Muốn tự nhận bản mới mỗi khi repo cập nhật: gõ `/plugin`, vào tab **Marketplaces**, chọn `trungnb87-skills`, bấm **Enable auto-update**.

## Dùng trong ứng dụng Claude (web, máy tính, điện thoại)

Ứng dụng Claude không đọc skill trực tiếp từ GitHub. Nén thư mục của skill (ví dụ `skills/video-diem-bao-bds`) thành file ZIP, rồi vào **Customize > Skills > + > Upload a skill**.

## Cấu trúc

```
.claude-plugin/marketplace.json   khai báo kho plugin
.claude-plugin/plugin.json        khai báo plugin bds-trung (có số phiên bản)
skills/<tên-skill>/SKILL.md       nội dung từng skill
skills/kich-ban-tiktok-bds        skill viết kịch bản TikTok
skills/video-diem-bao-bds/scripts  script dựng video và cover
skills/video-diem-bao-bds/assets   ảnh chân dung và 10 bản nhạc nền EPIC
```
