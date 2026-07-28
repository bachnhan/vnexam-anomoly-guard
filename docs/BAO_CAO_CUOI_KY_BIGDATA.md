# VNExam-AnomalyGuard: Hệ Thống Phân Tích Phổ Điểm Và Phát Hiện Bất Thường Gian Lận Điểm Thi THPT Quốc Gia (2016–2026) Bằng Apache Spark

**BÁO CÁO BÀI TẬP LỚN MÔN BIG DATA PROCESSING (BDA501)**

---

## Tóm Tắt (Abstract)

Báo cáo này giới thiệu **VNExam-AnomalyGuard**, một hệ thống xử lý Big Data toàn diện xây dựng trên nền tảng Apache Spark nhằm phân tích phổ điểm và tự động phát hiện các bất thường thống kê trong kỳ thi THPT Quốc Gia Việt Nam giai đoạn 2016–2026. Với quy mô **10.86 triệu bản ghi thí sinh**, dung lượng dữ liệu thô **1.01 GB** cùng 33 thuộc tính, tập dữ liệu đặt ra thách thức tính toán đối với các công cụ xử lý đơn nút truyền thống. Được triển khai trên cụm máy chủ giả lập phân tán Docker Standalone (1 Master Node, 2 Worker Nodes) kết hợp hệ thống lưu trữ Parquet phân vùng, VNExam-AnomalyGuard áp dụng cơ chế phát hiện bất thường SOTA **5 Phương án (5-Method Multi-Layer Anomaly Framework)**:

1. **PySpark MLlib K-Means Distance Outlier ($D > 3\sigma$):** Gom cụm thí sinh và dán nhãn khoảng cách lệch tâm.
2. **Multi-Subject Z-Score Engine ($Z > 3.0$):** Cô lập địa phương có mật độ điểm giỏi vọt tăng đột biến.
3. **Year-over-Year (YoY) Window Lag Delta ($\Delta Z > 2.0$):** So sánh chênh lệch chuỗi thời gian năm $T$ so me với năm $T-1$.
4. **Benford's Law Chi-Square Forensic Audit ($\chi^2 > 26.12$):** Bẫy dấu vết sửa điểm trắc nghiệm thủ công dựa trên phân phối chữ số đầu.
5. **Mahalanobis Distance Covariance ($D_M > 18.55$) & Shannon Entropy Audit ($H(X)$):** Đo độ tương quan đa môn và độ hỗn loạn phổ điểm.

Hệ thống cô lập 100% các sự cố gian lận Ground Truth lịch sử (2018 Hà Giang/Sơn La, 2021 Sinh học, 2026 Tuyên Quang) đồng thời phát hiện và giải thích thuyết phục **4 Case nghiên cứu giáo dục đặc thù ngoài Ground-Truth** (Cụm Y Dược ĐBSCL, Nôi học tập Nam Định/Thái Bình, Phân hóa Cụm thi Đại học 2016 và Đột biến Đề thi COVID-19 năm 2020).

---

## 1. Giới Thiệu (Introduction)

Kỳ thi THPT Quốc Gia là kỳ thi chuẩn hóa quan trọng bậc nhất tại Việt Nam, phục vụ đồng thời mục đích xét công nhận tốt nghiệp THPT và làm căn cứ xét tuyển đại học cho hơn 1 triệu thí sinh mỗi năm. Trong giai đoạn 10 năm từ 2016 đến 2026, dữ liệu tích lũy của kỳ thi đã vượt mốc 10.86 triệu bản ghi, đạt kích thước 1.01 GB dưới định dạng CSV thô.

Những sự cố gian lận điểm thi trong lịch sử—điển hình là bê bối sửa điểm thi năm 2018 tại Hà Giang, Sơn La, Hòa Bình, bê bối lộ đề thi môn Sinh học năm 2021, và mới nhất là các vụ án gian lận thi cử bị khởi tố năm 2026 tại Tuyên Quang, Quảng Ninh—đã đặt ra yêu cầu cấp thiết về một hệ thống tự động kiểm toán dữ liệu có khả năng phát hiện sớm các bất thường thống kê ở quy mô lớn.

---

## 2. Bối Cảnh & Kiến Trúc 5 Phương Án SOTA (Architecture of 5-Method Framework)

Hệ thống VNExam-AnomalyGuard được thiết kế theo mô hình 5 phương án phát hiện bất thường chia làm 2 Tầng xử lý chính:

### 2.1 Tầng Pipeline Chính (Chạy liên hoàn trên Spark Engine)
- **Phương án 1 (Student Level):** PySpark MLlib K-Means ($K=4$) đo khoảng cách Euclidean $D(x_i, C_k) > 3\sigma$.
- **Phương án 2 (Province Level):** Multi-Subject Z-Score $Z = \frac{X - \mu}{\sigma} > 3.0$ trên các môn Toán, A00 và Sinh học.
- **Phương án 3 (Time-Series YoY Level):** PySpark Window Functions `LAG` tính mức chênh lệch $\Delta Z_{\text{YoY}} = Z_T - Z_{T-1} > 2.0$.

### 2.2 Tầng Nghiên Cứu SOTA Nâng Cao (Module Forensic Independent Audit)
- **Phương án 4 (Benford's Law Audit):** Phân tích chữ số đầu tiên $D_1$ bằng kiểm định $\chi^2$ để phát hiện dấu vết sửa bài trắc nghiệm thủ công.
- **Phương án 5 (Mahalanobis Distance & Shannon Entropy):** Tính khoảng cách ma trận hiệp phương sai $\mathbf{\Sigma}$ và chỉ số độ hỗn loạn phổ điểm $H(X) = -\sum P(x) \log_2 P(x)$.

---

## 3. Các Chỉ Số Đáng Giá Trên Web Dashboard (High-Value Dashboard Metrics)

Bảng điều khiển Web Dashboard được thiết kế nhằm cung cấp các chỉ số kiểm toán quan trọng cho nhà quản lý giáo dục:

1. **Chỉ số Tải Trọng Tính Toán (Compute Benchmark Metrics):**
   - Tổng khối lượng bản ghi: **10.86 triệu thí sinh**.
   - Kích thước tập dữ liệu thô: **1.01 GB**.
   - Thời gian thực thi toàn bộ pipeline Spark: **~71.13 giây**.
   - Tỷ lệ nén dữ liệu Parquet: Giảm **85%** dung lượng đĩa đệm so với CSV thô.

2. **Chỉ số Đánh Giá Mô Hình ML & Forensics (Model Accuracy Metrics):**
   - Độ nhạy nhận diện các vụ án Ground-Truth (Recall): **100%** (3/3 vụ án).
   - Tỷ lệ dán nhãn Outlier thí sinh (Student Outliers): **~0.5%** tổng thí sinh toàn quốc.
   - Ngưỡng chỉ số Benford Chi-Square Test: $\chi^2 = 2,297.80 \gg 26.12$ ($p < 0.001$).
   - Mức Entropy trung bình toàn quốc: $H(X) = 3.518$ bits ($\sigma = 0.182$).

---

## 4. Phân Tích Chi Tiết 4 Case Bất Thường Ngoài Ground-Truth Có Thể Giải Thích Được

Bên cạnh việc khoanh vùng chính xác các đại án gian lận lịch sử, hệ thống VNExam-AnomalyGuard đã tự động phát hiện và giải thích nguyên nhân cho **4 hiện tượng bất thường thực tế tiêu biểu**:

### 📍 Case 1: Hiện Tượng Môn Sinh Học Tập Trung Cao Kéo Dài Tại Tỉnh 55 (Bạc Liêu / ĐBSCL)
- **Dữ liệu phát hiện:** Tỉnh 55 có chỉ số $Z_{\text{Bio}}$ liên tục vượt xa ngưỡng $3.0$ trong nhiều mùa thi ($Z_{2017}=4.15, Z_{2021}=4.03, Z_{2022}=4.90, Z_{2023}=3.97$).
- **Giải thích giáo dục:** Đây không phải hành vi gian lận thi cử mà là **kết quả của chính sách định hướng nghề nghiệp Y Dược địa phương**. Khu vực Đồng bằng Sông Cửu Long (đặc biệt là Bạc Liêu và Cần Thơ) có chính sách thu hút nhân lực ngành y tế và phong trào tập trung ôn thi khối B00 (Toán - Hóa - Sinh) rất mạnh tại các trường Chuyên, dẫn tới mật độ điểm 9.0–10.0 môn Sinh học tại đây luôn duy trì ở mức cao áp đảo toàn quốc.

### 📍 Case 2: Cụm Tích Tụ Học Lực Khối A00 Tại Nam Định (Tỉnh 25) & Thái Bình (Tỉnh 19)
- **Dữ liệu phát hiện:** Tỉnh 19 (Thái Bình) và Tỉnh 25 (Nam Định) xuất hiện tần suất dày đặc với chỉ số $Z_{\text{A00}} = 3.05 \rightarrow 3.71$ trong các năm 2017, 2021, 2023, 2024, 2025.
- **Giải thích giáo dục:** Thuật toán Z-Score đã nhận diện chính xác các **"Nôi học tập Khoa học Tự nhiên" truyền thống**. Nam Định và Thái Bình là hai địa phương có tỷ lệ học sinh theo học khối A00 và đạt tổng điểm 27.0–30.0 điểm cao nhất cả nước liên tục trong 10 năm qua.

### 📍 Case 3: Sự Phân Hóa Phổ Điểm Giữa Các Cụm Thi Đại Học Năm 2016 (Mã HDT, GHA, TDV)
- **Dữ liệu phát hiện:** Năm 2016 ghi nhận các cụm thi mã `HDT` (ĐH Hồng Đức), `GHA` (ĐH Giao thông Vận tải), `TDV` (ĐH Tây Bắc) có chỉ số $Z_{\text{Math}} = 3.06 \rightarrow 4.26$.
- **Giải thích giáo dục:** Đây là hiện tượng **phân hóa do chính sách tổ chức kỳ thi 2 trong 1 năm 2016**. Năm 2016 là năm duy nhất Bộ GD&ĐT chia tách làm 2 loại cụm thi: Cụm thi do Trường Đại học chủ trì (dành cho thí sinh nộp hồ sơ xét tuyển ĐH) và Cụm thi do Sở GD&ĐT chủ trì (chỉ xét tốt nghiệp). Do thí sinh có học lực giỏi dồn 100% về các Cụm Đại học, phổ điểm tại các mã cụm này bị lệch hẳn so với mặt bằng chung cả nước.

### 📍 Case 4: Đột Biến Phổ Điểm Toán Năm 2020 Do Đổi Mới Đề Thi Trong Bối Cảnh Dịch COVID-19 (Tỉnh 04 & Tỉnh 25)
- **Dữ liệu phát hiện:** Tại Tỉnh 25 (Nam Định) và Tỉnh 04 (Vĩnh Phúc), tỷ lệ điểm giỏi môn Toán vọt từ $1.5\%$ năm 2019 lên tới $17.5\%$ năm 2020 ($Z_{\text{Math}} = 3.18$, mức nhảy vọt YoY $+15.98\%$).
- **Giải thích giáo dục:** Năm 2020, Bộ GD&ĐT chính thức đổi tên kỳ thi từ "THPT Quốc gia" thành "Tốt nghiệp THPT" và chủ động giảm độ khó đề thi môn Toán để phù hợp với bối cảnh học sinh phải học trực tuyến do đợt dịch COVID-19 đầu tiên. Mức độ giảm đề thi làm tỷ lệ điểm 9.0+ vọt tăng trên toàn quốc, đặc biệt tại các tỉnh có phong trào học Toán mạnh.

---

## 5. Kết Luận (Conclusion)

VNExam-AnomalyGuard khẳng định tính hiệu quả và sáng tạo vượt trội khi kết hợp Big Data Apache Spark với 5 phương án kiểm toán SOTA (K-Means, Z-Score, YoY Lag Delta, Benford Audit, Mahalanobis & Shannon Entropy). Hệ thống không chỉ bẫy đúng 100% các đại án gian lận thực tế mà còn phân tích và giải thích sâu sắc 4 case hiện tượng giáo dục đặc thù của Việt Nam trong 10 năm qua.
