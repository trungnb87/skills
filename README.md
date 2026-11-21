# Skill bất động sản của Trung

Kho lưu skill Claude dùng cho công việc bất động sản:

| Skill | Việc làm |
|---|---|
| `video-diem-bao-bds` | Dựng video TikTok 9:16 dài tối đa 1 phút 30 có phân tích từ một tin BĐS, gửi kịch bản để anh duyệt trước khi dựng: giọng nhân bản của Trung (ElevenLabs), ảnh chân dung, video nền, phụ đề, 16 bản nhạc nền theo mood, bộ hiệu ứng chữ và chuyển cảnh đa dạng, ảnh cover |

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
skills/video-diem-bao-bds/scripts  script dựng video và cover
skills/video-diem-bao-bds/assets   ảnh chân dung và 16 bản nhạc nền
```
