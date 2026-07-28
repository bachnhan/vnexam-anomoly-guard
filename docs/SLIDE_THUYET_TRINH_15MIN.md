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
- **Nội dung:** Gian lận thi cử qua các thời kỳ (Bê bối 2018 Hà Giang/Sơn La, 2021 Sinh học, 2026 Tuyên Quang). Thách thức xử lý dữ liệu 1.01 GB trên máy đơn bị crash RAM.

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

### SLIDE 10: TỔNG QUAN BỘ 5 PHƯƠNG ÁN PHÁT HIỆN BẤT THƯỜNG
- **Nội dung:** 
  - *Tầng Pipeline Chính:* PA1 K-Means Outlier, PA2 Multi-Subject Z-Score, PA3 YoY Window Lag Delta.
  - *Tầng Forensic Audit SOTA:* PA4 Benford's Law Audit, PA5 Mahalanobis & Shannon Entropy.

### SLIDE 11: PHƯƠNG ÁN 1 - PYSPARK MLLIB K-MEANS OUTLIER ($D > 3\sigma$)
- **Nội dung:** Gom cụm 10.86M thí sinh ($K=4$), tính khoảng cách Euclidean tới tâm cụm để lọc thí sinh bất thường.

### SLIDE 12: PHƯƠNG ÁN 2 - MULTI-SUBJECT Z-SCORE ENGINE ($Z > 3.0$)
- **Nội dung:** Chuẩn hóa Z-Score động theo năm cho môn Toán, khối A00 và môn Sinh học ở cấp tỉnh thành.

### SLIDE 13: PHƯƠNG ÁN 3 - YEAR-OVER-YEAR (YoY) WINDOW LAG DELTA
- **Nội dung:** Sử dụng hàm PySpark `LAG` so sánh mức nhảy vọt chênh lệch giữa năm $T$ so với năm $T-1$ của cùng địa phương.

### SLIDE 14: PHƯƠNG ÁN 4 - BENFORD'S LAW CHI-SQUARE FORENSIC AUDIT
- **Nội dung:** Kiểm toán phân phối chữ số đầu tiên ($D_1$) bằng kiểm định $\chi^2 > 26.12$ để bẫy vết tẩy xóa / sửa điểm trắc nghiệm thủ công.

### SLIDE 15: PHƯƠNG ÁN 5 - MAHALANOBIS DISTANCE COVARIANCE OUTLIER
- **Nội dung:** Khoảng cách ma trận hiệp phương sai $\mathbf{\Sigma}$ phát hiện thí sinh đạt Toán 10.0 nhưng dính điểm liệt các môn còn lại.

### SLIDE 16: PHƯƠNG ÁN 6 - SHANNON ENTROPY AUDIT ($H(X)$)
- **Nội dung:** Đo độ hỗn loạn phổ điểm. Các cụm thi bị sửa điểm hàng loạt có Shannon Entropy thấp kỷ lục ($H < 2.9$ bits).

### SLIDE 17: KẾT QUẢ ĐỐI CHIẾU GROUND TRUTH (ĐỘ NHẠY 100%)
- **Nội dung:** Bẫy chính xác 100% các đại án 2018 (Hà Giang/Sơn La $Z=4.43$), 2021 (Lộ đề Sinh học $Z=4.03$), 2026 (Tuyên Quang $Z=3.09$).

### SLIDE 18: PHÁT HIỆN CÁC HIỆN TƯỢNG GIÁO DỤC BẤT THƯỜNG KHÁC
- **Nội dung:** 
  1. Cụm thi môn Sinh học kéo dài tại ĐBSCL (Tỉnh 55 $Z_{\text{Bio}} = 4.03 \rightarrow 4.90$).
  2. Nôi học tập Khối A00 Nam Định & Thái Bình ($Z_{\text{A00}} = 3.30 \rightarrow 3.71$).
  3. Lệch phổ điểm Cụm thi Đại học năm 2016 (`SPS`, `HDT`, `TDV`).

### SLIDE 19: DEMO CÔNG CỤ LIVE APP (`demo/app_demo.py`)
- **Nội dung:** Trình diễn ứng dụng Console App truy vấn Parquet cực nhanh dưới 1 giây.

### SLIDE 20: TỔNG KẾT & HƯỚNG PHÁT TRIỂN
- **Nội dung:** Tóm tắt đóng góp dự án và hướng nâng cấp tích hợp Apache Kafka kiểm toán theo thời gian thực.
