# Skill bất động sản của Trung

Kho lưu các skill Claude dùng cho công việc bất động sản:

| Skill | Việc làm |
|---|---|
| `diem-bao-bds` | Điểm báo BĐS cả nước, tối thiểu 50 bài mỗi lần, lọc theo địa phương và phân khúc, có cột mức độ quan trọng; chỉ lấy bài trực tiếp từ 23 báo |
| `kich-ban-tiktok-bds` | Viết kịch bản TikTok BĐS Hà Nội từ đúng 5 tin nóng nhất 24–48 giờ qua, rồi dựng sẵn video cho bài gợi ý quay trước (qua `video-diem-bao-bds`) |
| `video-diem-bao-bds` | Dựng video TikTok 9:16 dài ~2 phút có phân tích từ một tin BĐS: giọng nhân bản của Trung (ElevenLabs), ảnh chân dung, video nền, phụ đề, 16 bản nhạc nền theo mood, bộ hiệu ứng chữ và chuyển cảnh đa dạng, ảnh cover |

## Cài vào Claude Code (một lần)

Trong Claude Code, gõ:

```
/plugin marketplace add trungnb87/skills
/plugin install bds-trung@trungnb87-skills
```

Muốn tự nhận bản mới mỗi khi repo cập nhật: gõ `/plugin`, vào tab **Marketplaces**, chọn `trungnb87-skills`, bấm **Enable auto-update**.

## Dùng trong ứng dụng Claude (web, máy tính, điện thoại)

Ứng dụng Claude không đọc skill trực tiếp từ GitHub. Nén thư mục của skill (ví dụ `skills/diem-bao-bds`) thành file ZIP, rồi vào **Customize > Skills > + > Upload a skill**.

## Cấu trúc

```
.claude-plugin/marketplace.json   khai báo kho plugin
.claude-plugin/plugin.json        khai báo plugin bds-trung (có số phiên bản)
skills/<tên-skill>/SKILL.md       nội dung từng skill
skills/video-diem-bao-bds/scripts  script dựng video và cover
skills/video-diem-bao-bds/assets   ảnh chân dung và 16 bản nhạc nền
```
