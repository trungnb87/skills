# Ghi chú cho Claude khi sửa repo này

- Mỗi skill nằm ở `skills/<tên-skill>/SKILL.md`. Thêm skill mới thì tạo thư mục mới cùng dạng và bổ sung vào bảng trong README.md.
- Mỗi lần thay đổi nội dung skill, tăng `version` trong `.claude-plugin/plugin.json` (1.0.0 → 1.0.1 khi sửa nhỏ, 1.1.0 khi thêm skill). Claude Code chỉ nhận bản cập nhật khi số phiên bản đổi.
- Chạy `claude plugin validate .` trước khi commit.
- Làm trên nhánh riêng rồi mở pull request vào `main` để anh Trung bấm Merge.
- Viết commit, README và mô tả PR bằng tiếng Việt.
