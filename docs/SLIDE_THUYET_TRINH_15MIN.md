# SLIDE VÀ KỊCH BẢN THUYẾT TRÌNH 15 PHÚT (VNExam-AnomalyGuard)

---

## 📌 PHÂN CÔNG THUYẾT TRÌNH (6 THÀNH VIÊN)
- **Thành viên 1:** Slide 1 - 3 (Giới thiệu bài toán, Mục tiêu & Tập dữ liệu 10.86M)
- **Thành viên 2:** Slide 4 - 6 (Kiến trúc Docker Cluster Spark & Ingestion/Cleaning)
- **Thành viên 3:** Slide 7 - 9 (Spark SQL Analytics & Xu hướng phổ điểm 10 năm)
- **Thành viên 4:** Slide 10 - 13 (Bộ 5 Phương án Phát hiện Bất thường & MLlib K-Means/Z-Score/YoY Delta)
- **Thành viên 5:** Slide 14 - 17 (Kiểm toán SOTA: Benford Law Audit, Mahalanobis & Shannon Entropy)
- **Thành viên 6:** Slide 18 - 20 (Đối chiếu Ground Truth, Hiện tượng Giáo dục & Demo/Kết luận)

---

## 📽️ NỘI DUNG CHI TIẾT 20 SLIDE

### SLIDE 1: TIÊU ĐỀ DỰ ÁN
- **Tiêu đề:** VNExam-AnomalyGuard: Hệ Thống Phân Tích Phổ Điểm & Phát Hiện Bất Thường Gian Lận Thi THPT Quốc Gia (2016–2026) Bằng Apache Spark.
- **Kịch bản (Member 1):** "Kính chào Thầy và các bạn! Hôm nay nhóm xin trình bày dự án VNExam-AnomalyGuard xử lý Big Data 10.86 triệu bản ghi thi cử trong 10 năm qua..."

### SLIDE 2: BỐI CẢNH & TÍNH CẤP THIẾT
- **Nội dung:** Gian lận thi cử qua các thời kỳ (Bê bối 2018 Hà Giang/Sơn La/Hòa Bình, 2021 Sinh học). Thách thức xử lý dữ liệu 1.01 GB trên máy đơn bị crash RAM.

### SLIDE 3: TẬP DỮ LIỆU THI CỬ (DATASET 10.86M)
- **Nội dung:** 10,865,001 thí sinh, 33 thuộc tính điểm số từ 2016 đến 2026.

### SLIDE 4: KIẾN TRÚC DOCKER SPARK CLUSTER
- **Nội dung:** 1 Master Node, 2 Worker Nodes. Cấu hình Driver 4GB, Executor 2GB RAM, Arrow Optimization.

### SLIDE 5: PIPELINE TIỀN XỬ LÝ (CLEANING & FEATURE ENGINEERING)
- **Nội dung:** Lọc điểm sai phạm $[0.0, 10.0]$, tự động tính toán điểm 5 khối thi chính (A00, A01, B00, C00, D01).

### SLIDE 6: TỐI ƯU HÓA LƯU TRỮ PARQUET PHÂN VÙNG
- **Nội dung:** Lưu trữ nén Snappy Parquet `partitionBy("nam_thi")` giúp giảm 85% dung lượng đĩa đệm và tăng tốc truy vấn gấp 5 lần.

### SLIDE 7: SPARK SQL ANALYTICS ENGINE
- **Nội dung:** Thống kê phổ điểm trung bình toàn quốc Toán/Văn/Anh qua 11 mùa thi.

### SLIDE 8: CHUỖI BIẾN ĐỘNG ĐIỂM GIỎI & ĐIỂM LIỆT 10 NĂM
- **Nội dung:** Phân tích điểm Giỏi ($\ge 9.0$) và điểm Liệt ($\le 1.0$) môn Toán từ năm 2016 đến 2026.

### SLIDE 9: TOP TỈNH THÀNH DẪN ĐẦU CẢ NƯỚC
- **Nội dung:** Bảng xếp hạng Top 10 tỉnh thành có điểm Toán & khối A00 trung bình cao nhất.

### SLIDE 10: TỔNG QUAN KHUNG PHƯƠNG ÁN PHÁT HIỆN BẤT THƯỜNG
- **Nội dung:** Tư duy kiểm toán Top-Down (Từ Vĩ mô Cấp Tỉnh đến Vi mô Cấp Thí Sinh):
  - *Tầng 1 (Macro Audit):* Multi-Subject Z-Score Engine ($Z > 3.0$) — Phát hiện bất thường diện rộng cấp Tỉnh thành dựa trên 4 Đại án Ground-Truth.
  - *Tầng 2 (Micro Audit):* PySpark MLlib K-Means Outlier ($D \ge 11.03$) — Sàng lọc danh sách thí sinh dị biệt cá thể cần chấm thẩm định.

### SLIDE 11: PHƯƠNG ÁN 1 (MACRO) - MULTI-SUBJECT Z-SCORE ENGINE ($Z > 3.0$)
- **Nội dung:** Chuẩn hóa Z-Score động cho 9 môn thi & 5 khối thi cấp tỉnh thành. Bẫy trực tiếp 100% 4 đại án lịch sử (Hà Giang, Sơn La, Hòa Bình 2018, Lộ đề Sinh 2021).

### SLIDE 12: PHƯƠNG ÁN 2 (MICRO) - PYSPARK MLLIB K-MEANS OUTLIER ($D \ge 11.03$)
- **Nội dung:** Gom cụm 10.86M thí sinh ($K=4$), tính khoảng cách Euclidean xa tâm cụm để sàng lọc 58,870 thí sinh dị biệt cá thể (0.54% toàn quốc) phục vụ rà soát thủ công.

### SLIDE 13: KHUNG KIỂM TOÁN VÀ FORENSIC SOTA
- **Nội dung:** Benford's Law Chi-Square ($\chi^2$), Mahalanobis Distance ($D_M$) và Shannon Entropy ($H(X)$) để minh chứng đa chiều.

### SLIDE 14: KẾT QUẢ ĐỐI CHIẾU 4 ĐẠI ÁN GROUND TRUTH (RECALL 100%)
- **Nội dung:** Bẫy chính xác 100% (4/4) các đại án gian lận lịch sử ở cả 2 cấp độ vĩ mô và vi mô:
  - *GT 1 (Hà Giang 2018):* Macro $Z_{\text{A00}}=4.43$ (Top 1) · Micro bẫy cụm thí sinh xa tâm cụm · Nguồn: [Báo Chính Phủ](https://baochinhphu.vn/vu-gian-lan-diem-thi-tai-ha-giang-102263435.htm)
  - *GT 2 (Sơn La 2018):* Macro $Z_{\text{A00}}=4.13$ (Top 2) · Micro bẫy 181 thí sinh dị biệt $D \ge 5.0$ · Nguồn: [VnExpress](https://vnexpress.net/tuyen-an-12-bi-cao-vu-gian-lan-diem-thi-o-son-la-4103603.html)
  - *GT 3 (Hòa Bình 2018):* Macro $Z_{\text{Math}}=3.75$ (Top 3) · Micro bẫy mẫu điểm bất thường Toán/KHTN · Nguồn: [VnExpress](https://vnexpress.net/tuyen-an-15-bi-cao-trong-vu-gian-lan-diem-thi-o-hoa-binh-4103130.html)
  - *GT 4 (Lộ đề Sinh 2021):* Macro $Z_{\text{Bio}}=4.03$ · Micro bẫy cụm điểm lệch Sinh ĐBSCL · Nguồn: [Báo Chính Phủ](https://baochinhphu.vn/khoi-to-2-cui-giang-vien-li-lien-quan-den-de-thi-mon-sinh-hoc-102220610174003264.htm)

### SLIDE 18: PHÁT HIỆN CÁC HIỆN TƯỢNG GIÁO DỤC BẤT THƯỜNG KHÁC
- **Nội dung:** 
  1. Cụm thi môn Sinh học kéo dài tại ĐBSCL (Tỉnh 55 $Z_{\text{Bio}} = 4.03 \rightarrow 4.90$).
  2. Nôi học tập Khối A00 Nam Định & Thái Bình ($Z_{\text{A00}} = 3.30 \rightarrow 3.71$).
  3. Lệch phổ điểm Cụm thi Đại học năm 2016 (`SPS`, `HDT`, `TDV`).

### SLIDE 19: DEMO CÔNG CỤ LIVE APP (`demo/app_demo.py`)
- **Nội dung:** Trình diễn ứng dụng Console App truy vấn Parquet cực nhanh dưới 1 giây.

### SLIDE 20: TỔNG KẾT & HƯỚNG PHÁT TRIỂN
- **Nội dung:** Tóm tắt đóng góp dự án và hướng nâng cấp tích hợp Apache Kafka kiểm toán theo thời gian thực.
