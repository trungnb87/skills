---
name: "diem-bao-bds"
description: "Điểm báo bất động sản Việt Nam: tổng hợp tin BĐS, luật, hạ tầng, quy hoạch từ các báo lớn thành bảng có lọc địa phương. Dùng khi Trung nhờ điểm báo, tổng hợp tin BĐS."
---

# Điểm báo bất động sản Việt Nam

Tổng hợp tin bất động sản **trên cả nước** thành một bảng tra cứu có **nút lọc theo địa phương**, kèm vài dòng điểm nhấn cho đội kinh doanh. Người dùng là Giám đốc Kinh doanh BĐS hạng sang ở Hà Nội (trọng tâm Tây Hồ, Ciputra, Starlake), làm việc bằng tiếng Việt và xưng "anh", Claude xưng "em".

## 1. Xác định phạm vi

- **Thời gian mặc định:** từ ngày 1 của tháng hiện tại đến hôm nay. Nếu người dùng nói "hôm nay", "tuần này", "từ ngày X" thì theo lời họ. Luôn lấy ngày hiện tại thật (công cụ thời gian) trước khi tìm.
- **Phạm vi:** toàn quốc. Nếu người dùng nêu tỉnh/thành, vẫn thu thập toàn quốc nhưng mở bảng ở sẵn bộ lọc địa phương đó.
- **Số lượng tối thiểu: 30 bài mỗi lần điểm báo theo ngày.** Đọc hết các trang chuyên mục ở mục 2 và tìm thêm cho đến khi đủ 30 bài hợp lệ. Nếu hôm nay báo chưa đăng đủ (thường gặp khi chạy buổi sáng hoặc đầu giờ chiều), lấy thêm tin của ngày hôm trước cho đủ 30. Khi đó tiêu đề trang ghi khoảng ngày (vd. "15–16/11/2026"), và câu trả lời nói rõ có bao nhiêu bài của hôm nay, bao nhiêu bài của hôm trước. Không thêm tin lạc đề hay tin quảng cáo chỉ để đủ số.
- Không hỏi lại khi yêu cầu đã rõ; bắt đầu ngay.

## 2. Nguồn và cách lấy tin

Ứu tiên các báo sau (đều là báo chính thống tiếng Việt):
VnExpress, CafeF, CafeLand, Tuổi Trẻ, Thanh Niên, Dân trí, VietnamNet, VnEconomy, Lao Động, Báo Xây dựng, Kinh tế & Đô thị, Znews, Người Lao Động, Báo Đầu tư, Hà Nội Mới, VietnamPlus, Báo Chính phủ.

Cách lấy, theo thứ tự:
1. **WebFetch các trang chuyên mục** (liệt kê tiêu đề, URL, ngày nếu có, tóm tắt 1 câu):
   - https://vnexpress.net/bat-dong-san , https://vnexpress.net/bat-dong-san/chinh-sach , https://vnexpress.net/chu-de/bat-dong-san-ha-noi-6883 , https://vnexpress.net/chu-de/giao-thong-ha-noi-8554
   - https://cafef.vn/bat-dong-san.chn
   - https://cafeland.vn/chu-de-nong/bat-dong-san-ha-noi-66/ (có ngày giờ từng bài), https://cafeland.vn/thong-tin-quy-hoach/ ; nếu lỗi thì lấy qua WebSearch giới hạn domain cafeland.vn
   - https://batdongsan.baoxaydung.vn/chinh-sach.htm , https://batdongsan.baoxaydung.vn/du-an.htm (URL có mã ngày dạng 192YYMMDD…)
   - Dân trí, Tuổi Trẻ, Thanh Niên, VietnamNet, VnEconomy, Lao Động thường chặn WebFetch: tìm bài qua WebSearch với `allowed_domains` của từng báo. Ngày của Dân trí nằm trong URL (…2026MMDD…), của Thanh Niên dạng 185YYMMDD…
   - Có thể đọc RSS (vd. https://vnexpress.net/rss/bat-dong-san.rss, https://cafef.vn/bat-dong-san.rss, https://thanhnien.vn/rss/kinh-te/dia-oc.rss, https://vneconomy.vn/dia-oc.rss) khi fetch được.
2. **WebSearch** (gửi nhiều truy vấn cùng lượt, dùng `allowed_domains` cho từng báo khi cần) với các chủ đề: thị trường BĐS, chung cư, giá nhà, Luật Đất đai / Luật Nhà ở / Luật Kinh doanh BĐS, bảng giá đất, thuế BĐS, nhà ở xã hội, đấu giá đất, quy hoạch, metro, vành đai, cầu, cao tốc, sân bay; thêm tên tháng/năm hiện tại. Bổ sung riêng cho Hà Nội (Tây Hồ, Ciputra, Starlake, sông Hồng, cầu Tứ Liên, metro Hà Nội) và TP.HCM.
3. Nếu phiên có trình duyệt và trang báo không fetch được, có thể đọc trang chuyên mục của chính báo đó qua trình duyệt.

**Không dùng Bing News, Google News hay trang gom tin làm nguồn.** Mọi dòng phải là bài của chính báo, với link gốc trên tên miền của báo; cột Báo ghi tên báo đăng bài.

Quy tắc giữ / bỏ tin:
- Giữ tin về: thị trường, giá, nguồn cung, dự án, chủ đầu tư, đất đai, đấu giá, pháp lý, thuế, tín dụng BĐS, nhà ở xã hội, hạ tầng giao thông và quy hoạch có tác động đến BĐS.
- Bỏ: tin BĐS nước ngoài (Trung Quốc, Mỹ, Singapore…) không liên quan Việt Nam; bài quảng cáo thuần túy không có thông tin; tin thời sự không liên quan BĐS (cháy nổ, thời tiết…).
- Bỏ trùng: cùng một sự kiện đăng ở nhiều báo thì giữ một dòng (ưu tiên bài có tóm tắt rõ nhất, link gốc của báo).
- Không bịa: mọi dòng phải có URL thật đã thấy trong kết quả tìm/fetch. Ngày không chắc chắn thì ghi kèm dấu "~" (ước tính). Tóm tắt viết lại bằng lời của mình, ngắn (1 câu), không chép nguyên văn.

## 3. Phân loại từng tin

**Nhóm** (chọn một, theo tiêu đề trước, rồi đến tóm tắt):
- Luật & chính sách: luật, nghị định, nghị quyết, thông tư, đề xuất, thuế, sổ đỏ/sổ hồng, bảng giá đất, thu hồi, xử phạt, thanh tra, bồi thường, chuyển mục đích, tiền sử dụng đất.
- Hạ tầng & quy hoạch: metro, đường sắt, vành đai, cầu, cao tốc, quốc lộ, sân bay, nút giao, quy hoạch, TOD, thông xe.
- Nhà ở xã hội.
- Đấu giá & đất: đấu giá, đất vàng, giá khởi điểm.
- Doanh nghiệp: lợi nhuận, BCTC, cổ phiếu, trái phiếu.
- Dự án: mở bán, khởi công, chủ đầu tư, khu đô thị, bàn giao.
- Thị trường: còn lại.

**Địa phương** (một tin có thể thuộc nhiều nơi; không nhắc tỉnh nào → "Toàn quốc"). Dùng 34 tỉnh, thành sau sáp nhập 2025, nhận cả tên cũ và địa danh quen thuộc:

| Địa phương | Nhận diện thêm (tên cũ, địa danh) |
|---|---|
| Hà Nội | các quận/huyện cũ, Tây Hồ, Hồ Tây, Ciputra, Nam Thăng Long, Starlake, Mỹ Đình, Đông Anh, Gia Lâm, Mê Linh, Hòa Lạc, Sóc Sơn, Vinhomes Ocean Park, sông Hồng, Tứ Liên, Nhật Tân |
| TP.HCM | Sài Gòn, Thủ Đức, Thủ Thiêm, Bình Dương, Thủ Dầu Một, Dĩ An, Thuận An, Vũng Tàu, Bà Rịa, Côn Đảo, Cần Giờ, Phú Mỹ Hưng, Hồ Tràm |
| Hải Phòng | Hải Dương, Đồ Sơn, Cát Bà, Thủy Nguyên |
| Đà Nẵng | Quảng Nam, Hội An, Tam Kỳ, Chu Lai |
| Cần Thơ | Sóc Trăng, Hậu Giang |
| Huế | Thừa Thiên Huế, Chân Mây, Lăng Cô |
| Quảng Ninh | Hạ Long, Vân Đồn, Móng Cái, Cẩm Phả |
| Bắc Ninh | Bắc Giang, Từ Sơn, Gia Bình |
| Hưng Yên | Thái Bình, Văn Giang, Ecopark |
| Ninh Bình | Hà Nam, Nam Định, Phủ Lý |
| Phú Thọ | Vĩnh Phúc, Hòa Bình, Việt Trì, Tam Đảo |
| Thái Nguyên | Bắc Kạn |
| Lào Cai | Yên Bái, Sa Pa |
| Tuyên Quang | Hà Giang |
| Thanh Hóa | Sầm Sơn, Nghi Sơn |
| Nghệ An | TP Vinh, Cửa Lò |
| Quảng Trị | Quảng Bình, Đồng Hới |
| Quảng Ngãi | Kon Tum, Dung Quất |
| Gia Lai | Bình Định, Quy Nhơn, Nhơn Hội |
| Khánh Hòa | Ninh Thuận, Nha Trang, Cam Ranh, Phan Rang |
| Đắk Lắk | Phú Yên, Buôn Ma Thuột, Tuy Hòa |
| Lâm Đồng | Đắk Nông, Bình Thuận, Đà Lạt, Bảo Lộc, Phan Thiết, Mũi Né |
| Đồng Nai | Bình Phước, Biên Hòa, Long Thành, Nhơn Trạch |
| Tây Ninh | Long An, Bến Lức, Đức Hòa |
| Đồng Tháp | Tiền Giang, Mỹ Tho |
| Vĩnh Long | Bến Tre, Trà Vinh |
| An Giang | Kiên Giang, Phú Quốc, Rạch Giá |
| Cà Mau | Bạc Liêu |
| Còn lại | Hà Tĩnh, Lạng Sơn, Cao Bằng, Sơn La, Điện Biên, Lai Châu |

**Dấu ★** cho tin sát mối quan tâm của người dùng: Tây Hồ, Hồ Tây, Ciputra, Nam Thăng Long, Starlake, Nhật Tân, Tứ Liên, sông Hồng, phân khúc cao cấp / hạng sang / hàng hiệu (branded residences), biệt thự, người nước ngoài mua nhà, metro Hà Nội, và các luật BĐS đang sửa.

## 4. Sản phẩm giao

**a) Bảng tra cứu dạng artifact** (trang HTML một file, xuất bản qua công cụ Artifact; tải skill `artifact-design` trước khi viết). Lần cập nhật sau trong cùng cuộc trò chuyện thì xuất bản lại cùng file để giữ link.
- Tiêu đề trang: "Điểm báo BĐS <khoảng ngày>" (vd. "Điểm báo BĐS 01–16/11/2026").
- Dữ liệu đặt trong một mảng JS: ngày, ngày ước tính (có/không), báo, địa phương (mảng), nhóm, ★, tiêu đề, tóm tắt, URL.
- **Hàng nút lọc địa phương** ngay trên bảng: Tất cả · Hà Nội · TP.HCM · Toàn quốc (mỗi nút kèm số bài) + ô chọn "Tỉnh, thành khác…" liệt kê các địa phương đang có tin, xếp theo số bài.
- Thanh lọc: ô tìm kiếm, chọn báo, chọn nhóm, "Chỉ tin ★", "Đặt lại lọc".
- Cột: #, Ngày, Báo, Địa phương, Nhóm (nhãn màu; Luật & chính sách và Hạ tầng & quy hoạch có màu riêng), Tiêu đề (link mở bài gốc, tab mới), Nội dung chính.
- Sắp xếp mới nhất trước. Trên điện thoại (≤640px) mỗi bài hiển thị thành thẻ gọn, không cuộn ngang. Hỗ trợ sáng/tối.
- Ghi chú cuối trang: dấu "~" là ngày ước tính; tóm tắt do Claude viết lại, nên mở bài gốc trước khi trích dẫn.

**b) Trả lời trong chat** (ngắn, không lặp lại bảng):
- Tổng số bài, số báo, phân bố chính theo địa phương.
- 3–5 điểm nhấn đáng chú ý nhất cho đội kinh doanh hạng sang Hà Nội (luật/chính sách mới, hạ tầng ảnh hưởng Tây Hồ – Ciputra, diễn biến giá/thanh khoản, dự án cạnh tranh). Mỗi điểm 1–2 câu, nêu nguồn.
- Lưu ý ngắn nếu có nguồn không truy cập được hoặc ngày ước tính.
- Kết thúc bằng mục "Sources:" liệt kê các trang chuyên mục / bài chính đã dùng.

## 5. Lưu ý

- Không trình bày tin đồn hay số liệu chưa có nguồn như sự thật; trích con số thì ghi rõ báo nào đưa.
- Không đưa lời khuyên đầu tư cụ thể; điểm nhấn là thông tin để người dùng tự đánh giá.
- Nếu người dùng muốn tự động hằng ngày, đề xuất tạo scheduled task chạy skill này vào giờ họ chọn và cập nhật lại cùng artifact.