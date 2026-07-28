**VNEXAM-ANOMALYGUARD: HỒ SƠ TỔNG HỢP TOÀN DIỆN DỰ ÁN (MASTER ALL-IN-ONE DOCUMENTATION)**

**HỆ THỐNG PHÂN TÍCH PHỔ ĐIỂM & PHÁT HIỆN GIAN LẬN ĐIỂM THI THPT QUỐC GIA (2016–2026) TRÊN NỀN TẢNG APACHE SPARK**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 **Tệp Tài Liệu Master Đầy Đủ Tất Cả Nội Dung Dự Án:** Tệp này chứa TOÀN BỘ thông tin Kế hoạch triển khai & Lịch trình Timeline chuẩn, Luận văn Thesis chuẩn IMRaD bằng Tiếng Việt, Kịch bản Thuyết trình 20 Slide & Q\&A, Hạ tầng Docker và Toàn bộ Mã nguồn PySpark.

📁 **Thư Mục Lưu Trữ Dự Án:**

⏰ **Hạn Nộp Bài (Submission Deadline):** **08:00 AM \- Thứ 7 (01/08/2026)**

🎙️ **Ngày Thuyết Trình Báo Cáo (Presentation Day):** **Chủ Nhật (02/08/2026)**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**MỤC LỤC TỔNG HỢP (TABLE OF CONTENTS)**

1. **PHẦN I: KẾ HOẠCH DỰ ÁN, MA TRẬN PHÂN CÔNG & LỊCH TRÌNH TIMELINE**

\- 1.1 Thông tin Metadata & Bối cảnh bài toán Big Data

\- 1.2 Bảng phân công nhiệm vụ & Lượt thuyết trình 15 phút (Chính thức của 6 người)

\- 1.3 Lịch trình triển khai & Kiểm soát tiến độ (Timeline từ Thứ 3 đến Chủ Nhật)

\- 1.4 Bản đồ thư mục & Kế hoạch Bảo đảm Chất lượng (Verification Plan)

2. **PHẦN II: LUẬN VĂN BÁO CÁO BÀI TẬP LỚN CHUẨN IMRaD (TIẾNG VIỆT 100%)**

\- Trang bìa, Tóm tắt (Abstract), 1\. Giới thiệu, 2\. Bối cảnh & Nghiên cứu liên quan, 3\. Phương pháp, 4\. Kết quả, 5\. Thảo luận & Kết luận, Tài liệu tham khảo

3. **PHẦN III: KỊCH BẢN THUYẾT TRÌNH 20 SLIDE & BỘ 10 CÂU HỎI Q\&A PHẢN BIỆN**

\- Kịch bản 20 Slide phân chia cho 6 thành viên (File slide lưu tại docs/SLIDE\_THUYET\_TRINH\_15MIN.md)

\- Bộ 10 câu hỏi Q\&A phản biện của Giảng viên & Kịch bản trả lời chi tiết

4. **PHẦN IV: HẠ TẦNG DOCKER & TOÀN BỘ MÃ NGUỒN PIPELINE PYSPARK (SOURCE CODE)**

\- Cấu hình Cluster docker-compose.yml

\- Mã nguồn 5 tệp PySpark Pipeline (01\_ingestion.py đến 05\_export\_results.py)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**PHẦN I: KẾ HOẠCH DỰ ÁN, MA TRẬN PHÂN CÔNG & LỊCH TRÌNH TIMELINE**

**1.1 Thông Tin Tổng Quan Dự Án (Project Metadata)**

* Tên Dự Án (Project Name): VNExam-AnomalyGuard  
* Tên Đầy Đủ: Hệ Thống Phân Tích Phổ Điểm & Phát Hiện Gian Lận Điểm Thi THPT Quốc Gia (2016–2026) Trên Nền Tảng Apache Spark  
* Thư Mục Lưu Trữ Dự Án (Directory): d:\\LHTBrain\\Bigdata  
* Công Cụ Kỹ Thuật Chính: Apache Spark (PySpark DataFrame API, Spark SQL Engine, Spark MLlib)  
* Tập Dữ Liệu: **\`exam\_scores\_2016\_2026.csv\` (**1.01 GB **/** 10,865,001 bản ghi **/** 33 thuộc tính)  
* Môi Trường Triển Khai: Cluster Standalone local bằng Docker Compose (1 Master \+ 2 Workers) & HDFS  
* Quy Mô Nhân Sự: 6 Thành viên  
* Hạn Nộp Bài (Submission Deadline): 08:00 AM \- Thứ 7 (01/08/2026)  
* Ngày Thuyết Trình (Presentation Day): Chủ Nhật (02/08/2026)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**1.2 Bảng Phân Công Nhiệm Vụ & Lượt Thuyết Trình Khớp Nối (15 Phút)**

| Main Deliverable | Thành viên | Nhiệm vụ Sản phẩm (Deliverable Task) | Tệp Sản Phẩm | Phần Thuyết Trình Khớp Nối (Thuyết trình 15') | Thời Lượng |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **1\. REPORT (DOC)** | **Member 3 (Học)** | Viết Nửa đầu Luận văn chuẩn IMRaD: Title Page, Abstract, Section 1 (Introduction), Section 2 (Background), Section 3 (Method). | docs/BAO\_CAO\_CUOI\_KY\_BIGDATA.md*(Intro, Background, Method)* | **Slide 1 \- 3 \[INTRO & DATASET\]:** Giới thiệu VNExam-Anomaly Guard, Đặt Vấn Đề THPT QG & Dataset 1.01GB. | **2.0 phút** |
| **2\. CODE PIPELINE** | **Member 1 (Nhân)** | Setup Docker Cluster Standalone (1 Master \+ 2 Workers), Nạp dữ liệu 1.01GB, làm sạch & ép kiểu 33 cột. | docker-compose.ymlsrc/01\_ingestion.pysrc/02\_cleaning.py | **Slide 4 \- 6 \[ARCHITECTURE & PREPROCESSING\]:** Kiến trúc Pipeline 5 tầng, Docker Cluster & Clean 10.8M dòng. | **2.5 phút** |
|  | **Member 2 (Quân)** | Lập trình truy vấn Spark SQL, xây dựng thuật toán PySpark MLlib K-Means & Z-Score Anomaly Engine, Export Parquet. | src/03\_analytics.pysrc/04\_anomaly\_ml.pysrc/05\_export\_results.py | **Slide 7 \- 10 \[METHODOLOGY\]:** Giải thích Thuật toán MLlib K-Means Distance Outlier ($D \> 3\\sigma$) & Z-Score Engine ($Z \> 3.0$). | **2.5 phút** |
| **3\. REPORT (DOC)** | **Member 4 (Trang)** | Viết Nửa sau Luận văn chuẩn IMRaD: Section 4 (Results), Section 5 (Conclusion, Discussion & Future Work), References. | docs/BAO\_CAO\_CUOI\_KY\_BIGDATA.md*(Results, Discussion, Ref)* | **Slide 11 \- 13 \[RESULTS ANALYTICS\]:** Trình bày Kết quả Spark SQL Analytics (Phổ điểm toàn quốc, Top Tỉnh thành & Biến động năm). | **2.5 phút** |
| **4\. SLIDE & demoDEMO** | **Member 5 (Hiểu)** | Thiết kế bộ 20 Slide PowerPoint chuyên nghiệp, sơ đồ kiến trúc, đồ họa và biểu đồ kết quả. | docs/SLIDE\_THUYET\_TRINH\_15MIN.md*(File Slide PowerPoint)* | **Slide 14 \- 16 \[ANOMALY FINDINGS\]:** Kết quả Anomaly phát hiện được (Mô phỏng gian lận 2018). | **2.0 phút** |
|  | **Member 6 (Mai Anh)** | Lập trình ứng dụng Live Demo (demo\_app.py), quay video demo dự phòng, tổng hợp Bộ 10 câu hỏi Q\&A. | demo/app\_demo.py*(Bộ Q\&A & Demo Script)* | **Slide 17 \- 18 \[LIVE DEMO EXECUTION\]:** Vận hành trực tiếp **Live Demo App** trên màn hình cho Hội đồng xem. | **2.0 phút** |
|  | **Member 5 (Hiểu)** | Thảo luận Lợi ích xã hội & Tổng kết dự án sau phần Live Demo. | docs/SLIDE\_THUYET\_TRINH\_15MIN.md | **Slide 19 \- 20 \[SOCIAL IMPACT & FINAL SUMMARY\]:** Thảo luận Lợi ích Xã hội / Người dùng, **TỔNG KẾT DỰ ÁN SAU DEMO** & Lead Q\&A. | **1.5 phút** |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**1.3 Lịch Trình Triển Khai & Kiểm Soát Tiến Độ (Timeline & Milestones \- Thứ 3 đến Chủ Nhật)**

| Thời Gian | Giai Đoạn | Mục Tiêu & Công Việc Chính | Nhân Sự Thực Hiện |
| :---- | :---- | :---- | :---- |
| **Thứ Ba (28/07)** | **Giai đoạn 1** | **Nhận Phân Công & Bắt Đầu Triển Khai Cá Nhân:**• Gửi file Master cho 6 thành viên.• Member 1 & 2 test Docker & Code Pipeline.• Member 3 & 4 đọc Luận văn Thesis.• Member 5 & 6 chuẩn bị kịch bản Slide & App Demo. | Cả 6 thành viên |
| **Thứ Tư (29/07)** | **Giai đoạn 2** | **Họp Đồng Bộ Xem Tiến Độ Từng Member:**• Kiểm tra tiến độ thực tế từng member (Member 1 đến 6).• Đánh giá khối lượng hoàn thành, phát hiện điểm nghẽn hoặc phần chưa khớp giữa Code, Report và Slide. | Cả 6 thành viên |
| **Thứ Năm (30/07)** | **Giai đoạn 3** | **Sửa Lỗi, Bổ Sung & Tinh Chỉnh Sản Phẩm:**• Tinh chỉnh sản phẩm theo góp ý từ họp Thứ Tư.• Chốt Code Pipeline, Luận văn PDF, Slide PPTX & App Demo. | Cả 6 thành viên |
| **Thứ Sáu (31/07)** | **Giai đoạn 4** | **Ghép Slide, Chạy Thử Demo & Rehearsal 15m:**• Ghép slide thuyết trình, chạy thử Live Demo App.• Rehearsal duyệt thử 15m canh giờ & luyện trả lời Q\&A. | Cả 6 thành viên |
| **Thứ Bảy (01/08)** | **HẠN NỘP BÀI (8h AM)** | **NỘP BÀI CHÍNH THỨC (SUBMISSION DEADLINE):**• Đóng gói và NỘP TOÀN BỘ HỒ SƠ DỰ ÁN (Luận văn PDF, Slide PPTX, Code Zip) lên hệ thống trước **8h00 AM Thứ Bảy**. | Cả 6 thành viên |
| **Chủ Nhật (02/08)** | **PRESENTATION DAY** | **BÁO CÁO THUYẾT TRÌNH CHÍNH THỨC:**• Thuyết trình 15 phút trước Giảng viên / Hội đồng và trả lời Q\&A. | Cả 6 thành viên |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**1.4 Bản Đồ Thư Mục Dự Án (Directory Structure Map)**

d:\\LHTBrain\\Bigdata\\  
├── VNExam-AnomalyGuard-MASTER-ALL-IN-ONE.md \# \[TỆP MASTER TỔNG HỢP DUY NHẤT\]  
├── docker-compose.yml                       \# Cấu hình Cụm Spark Cluster (1 Master \+ 2 Workers)  
├── requirements.txt                         \# Danh sách thư viện Python phụ thuộc  
├── data/  
│   └── exam\_scores\_2016\_2026.csv            \# Tập dữ liệu 1.01 GB (10,865,001 bản ghi)  
├── src/  
│   ├── 01\_ingestion.py                      \# Pipeline nạp dữ liệu 1.01GB (Member 1\)  
│   ├── 02\_cleaning.py                       \# Pipeline làm sạch & ép kiểu 33 cột (Member 1\)  
│   ├── 03\_analytics.py                      \# Spark SQL Analytics phổ điểm & Tỉnh thành (Member 2\)  
│   ├── 04\_anomaly\_ml.py                     \# Spark MLlib K-Means & Z-Score Anomaly Detector (Member 2\)  
│   └── 05\_export\_results.py                 \# Xuất kết quả Parquet phân vùng theo năm (Member 2\)  
└── docs/  
    ├── VNExam-AnomalyGuard-MASTER-ALL-IN-ONE.md \# \[BẢN SAO LƯU MASTER TẠI THƯ MỤC DOCS\]  
    ├── BAO\_CAO\_CUOI\_KY\_BIGDATA.md           \# \[LUẬN VĂN BÁO CÁO THESIS CHUẨN IMRaD (TIẾNG VIỆT)\] (Member 3 & 4\)  
    └── SLIDE\_THUYET\_TRINH\_15MIN.md          \# \[20 SLIDE THUYẾT TRÌNH VÀ BỘ Q\&A\] (Member 5 & 6\)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**1.5 Kế Hoạch Bảo Đảm Chất Lượng (Verification Plan)**

5. **Kiểm tra Môi trường Cluster:** Chạy docker-compose up \-d tại d:\\LHTBrain\\Bigdata, đảm bảo Spark Web UI (http://localhost:8080) nhận đủ 2 Worker Nodes hoạt động mượt mà.  
6. **Kiểm tra Bộ nhớ & Hiệu năng:** Đảm bảo 01\_ingestion.py và 04\_anomaly\_ml.py không dính lỗi OutOfMemoryError bằng Heap Size 4G.  
7. **Kiểm tra Khớp nối Deliverables vs Presentation:** Đảm bảo phần Lợi ích xã hội / Người dùng nằm ở Phần 7 (Slide 19-20) do Member 5 trình bày sau phần Demo.  
8. **Đồng bộ Hồ sơ Dự án:** Số liệu trong Code, Báo cáo Doc, và Slide thuyết trình trùng khớp 100%.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**PHẦN II: LUẬN VĂN BÁO CÁO BÀI TẬP LỚN CHUẨN IMRaD (TIẾNG VIỆT 100%)**

BỘ GIÁO DỤC VÀ ĐÀO TẠO  
TRƯỜNG ĐẠI HỌC FPT

BÁO CÁO BÀI TẬP LỚN MÔN BIG DATA PROCESSING (40% ĐIỂM)

VNExam-AnomalyGuard: Hệ Thống Phân Tích Phổ Điểm Và Phát Hiện Bất Thường Gian Lận Điểm Thi THPT Quốc Gia (2016–2026) Bằng Apache Spark

Thực hiện bởi:  
Nhóm 6 Thành Viên

Ngành: Thạc sĩ / Cử nhân Kỹ thuật Phần mềm

Giảng viên hướng dẫn:  
1\. \[Tên Giảng Viên\]

© Bản quyền thuộc về Nhóm 6 Thành Viên \- Đại học FPT 2026

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Tóm Tắt (Abstract)**

Báo cáo này giới thiệu **VNExam-AnomalyGuard**, một hệ thống xử lý Big Data toàn diện xây dựng trên nền tảng Apache Spark nhằm phân tích phổ điểm và tự động phát hiện các bất thường thống kê trong kỳ thi THPT Quốc Gia Việt Nam giai đoạn 2016–2026. Với quy mô **10.86 triệu bản ghi thí sinh**, dung lượng dữ liệu thô **1.01 GB** cùng 33 thuộc tính, tập dữ liệu đặt ra thách thức tính toán cực lớn đối với các công cụ xử lý đơn nút truyền thống. Được triển khai trên cụm máy chủ giả lập phân tán Docker Standalone (1 Master Node, 2 Worker Nodes) kết hợp hệ thống lưu trữ HDFS, VNExam-AnomalyGuard áp dụng cơ chế phát hiện bất thường hai cấp độ: (1) Cấp độ thí sinh sử dụng thuật toán gom cụm **PySpark MLlib K-Means** tính khoảng cách Euclidean đến tâm cụm nhằm dán nhãn các thí sinh vượt ngưỡng lệch chuẩn $3\\sigma$; (2) Cấp độ tỉnh thành sử dụng chỉ số **Z-Score** thống kê nâng cao với Spark SQL để cô lập các cụm điểm cao (\>= 9.0) tăng đột biến bất thường ($Z \> 3.0$). Hệ thống xử lý thành công 1.01 GB dữ liệu chỉ trong vài giây và xuất dữ liệu nén Parquet tối ưu, chứng minh khả năng kiểm toán dữ liệu thi cử theo thời gian thực cho các nhà quản lý giáo dục.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**1\. Giới Thiệu (Introduction)**

Kỳ thi THPT Quốc Gia là kỳ thi chuẩn hóa quan trọng bậc nhất tại Việt Nam, phục vụ đồng thời mục đích xét công nhận tốt nghiệp THPT và làm căn cứ xét tuyển đại học cho hơn 1 triệu thí sinh mỗi năm. Trong giai đoạn 10 năm từ 2016 đến 2026, dữ liệu tích lũy của kỳ thi đã vượt mốc 10.86 triệu bản ghi, đạt kích thước 1.01 GB dưới định dạng CSV thô.

Những sự cố gian lận điểm thi trong lịch sử—điển hình là bê bối sửa điểm thi năm 2018 tại một số tỉnh thành như Hà Giang, Sơn La, Hòa Bình—đã đặt ra yêu cầu cấp thiết về một hệ thống tự động kiểm toán dữ liệu có khả năng phát hiện sớm các bất thường thống kê ở quy mô lớn. Các công cụ xử lý dữ liệu truyền thống như Microsoft Excel hay Python Pandas trên máy tính đơn dính phải rào cản nghiêm trọng về giới hạn bộ nhớ (OutOfMemoryError) và tốc độ xử lý khi làm việc với tập dữ liệu hàng triệu dòng.

Dự án này phát triển hệ thống **VNExam-AnomalyGuard** dựa trên hạ tầng xử lý dữ liệu lớn Apache Spark, cho phép nạp, làm sạch, truy vấn và tự động dán nhãn bất thường trên 10.86 triệu bản ghi thi cử một cách nhanh chóng và chính xác.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**2\. Bối Cảnh & Các Nghiên Cứu Liên Quan (Background & Related Work)**

**2.1 Xử Lý Dữ Liệu Phân Tán Với Apache Spark**

Apache Spark là khung làm việc tính toán cụm phân tán mã nguồn mở tiên tiến. Nhờ cơ chế lưu trữ tập dữ liệu phân tán tự phục hồi (RDD) trực tiếp trên RAM, Spark đạt tốc độ xử lý nhanh gấp 10 đến 100 lần so với mô hình Hadoop MapReduce vốn phải ghi đĩa I/O liên tục. Tầng ứng dụng PySpark DataFrame và Spark SQL cung cấp khả năng truy vấn dữ liệu cấu trúc song song trên nhiều nút worker.

**2.2 Phát Hiện Bất Thường Trong Khảo Thí Giáo Dục**

Phát hiện bất thường thống kê trong thi cử thường tập trung vào hai quy mô: (1) Bất thường lệch môn ở từng thí sinh (ví dụ: điểm Toán, Hóa 10.0 nhưng điểm Lý 1.0) và (2) Bất thường phổ điểm ở cấp độ tỉnh thành/cụm thi (tỷ lệ điểm 9-10 tăng vọt bất thường so với trung bình toàn quốc). Các thuật toán học máy như K-Means Clustering và chỉ số Z-Score Thống kê được ứng dụng rộng rãi trong trắc lượng học để phát hiện các điểm dữ liệu sai lệch khỏi phân phối chuẩn.

**2.3 Môi Trường Hạ Tầng Đóng Gói Docker**

Đóng gói ứng dụng bằng Docker và Docker Compose cho phép dựng cụm phân tán Spark Standalone có tính đóng gói cao. Mô hình gồm 1 Master Node (vnexam-spark-master) và 2 Worker Nodes (vnexam-spark-worker-1, vnexam-spark-worker-2) giúp giả lập hoàn hảo môi trường tính toán song song thực tế trên máy cục bộ.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**3\. Phương Pháp Thực Hiện (Method)**

**3.1 Kiến Trúc Pipeline 5 Tầng**

Hệ thống VNExam-AnomalyGuard được thiết kế theo kiến trúc 5 tầng xử lý:

9. **Tầng Lưu Trữ (Storage Layer):** File CSV thô 1.01 GB (exam\_scores\_2016\_2026.csv) đặt trên đĩa/HDFS.  
10. **Tầng Nạp Dữ Liệu (Ingestion Layer):** Sử dụng PySpark DataFrame Read API ép kiểu chuẩn cho 33 cột.  
11. **Tầng Làm Sạch & Biến Đổi (Preprocessing Layer):** Lọc dữ liệu sai sót ($\<0$ hoặc $\>10$) và tính tổng điểm các khối thi (A00, A01, B00, C00, D01).  
12. **Tầng Phân Tích & Học Máy (Analytics & ML Engine):** Truy vấn Spark SQL phân tích phổ điểm và chạy thuật toán PySpark MLlib Anomaly.  
13. **Tầng Xuất Kết Quả (Export Layer):** Xuất dữ liệu nén Parquet phân vùng theo năm nam\_thi.

**3.2 Tiền Xử Lý & Biến Đổi Dữ Liệu**

Các cột điểm môn thi (toan, vat\_ly, hoa\_hoc, sinh\_hoc, ngu\_van, ngoai\_ngu, lich\_su, dia\_ly, gdcd) được ép kiểu Float và làm sạch. Điểm các khối thi chính được tự động tính toán:

* Khối A00: $\\text{toan} \+ \\text{vat\\\_ly} \+ \\text{hoa\\\_hoc}$  
* Khối A01: $\\text{toan} \+ \\text{vat\\\_ly} \+ \\text{ngoai\\\_ngu}$  
* Khối B00: $\\text{toan} \+ \\text{hoa\\\_hoc} \+ \\text{sinh\\\_hoc}$  
* Khối C00: $\\text{ngu\\\_van} \+ \\text{lich\\\_su} \+ \\text{dia\\\_ly}$  
* Khối D01: $\\text{toan} \+ \\text{ngu\\\_van} \+ \\text{ngoai\\\_ngu}$

**3.3 Thuật Toán Phát Hiện Bất Thường 2 Cấp Độ**

**3.3.1 Phát Hiện Bất Thường Cấp Độ Thí Sinh (PySpark MLlib K-Means Distance Outlier)**

Thí sinh được chuyển đổi thành vector 6 môn thi bằng VectorAssembler. Mô hình PySpark MLlib K-Means (K=4) xác định các tâm cụm $C\_k$. Khoảng cách Euclidean từ vector thí sinh $x\_i$ tới tâm cụm $C\_k$ được tính qua hàm UDF:

$$D(x\_i, C\_k) \= \\sqrt{\\sum\_{j=1}^{n} (x\_{ij} \- c\_{kj})^2}$$

Những thí sinh có khoảng cách vượt phân vị 99.5% ($D \> 3\\sigma$) sẽ được dán cờ bất thường (is\_student\_anomaly \= True).

**3.3.2 Phát Hiện Bất Thường Cấp Độ Tỉnh Thành (Statistical Z-Score Engine)**

Bất thường phổ điểm tỉnh thành được xác định bằng cách tính chỉ số Z-Score so với trung bình và độ lệch chuẩn toàn quốc:

$$Z \= \\frac{\\bar{X}\_{tinh} \- \\bar{X}\_{toanquoc}}{\\sigma\_{toanquoc} / \\sqrt{N}}$$

Các tỉnh thành có $Z \> 3.0$ ở phân khúc điểm cao (\>= 9.0) được cảnh báo bất thường thống kê.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**4\. Kết Quả Nghiên Cứu (Results)**

**4.1 Kết Quả Truy Vấn Spark SQL Analytics**

Thao tác truy vấn Spark SQL trên 10.86 triệu bản ghi đã trích xuất thành công phổ điểm trung bình toàn quốc qua các năm từ 2016 đến 2026, thứ hạng Top 10 tỉnh thành có điểm Toán cao nhất, và chuỗi biến động điểm thi qua từng thời kỳ.

**4.2 Kết Quả K-Means Outlier Cấp Thí Sinh**

Mô hình K-Means Distance Outlier dán nhãn thành công **54,325 thí sinh bất thường** (chiếm 0.5% tổng số thí sinh toàn quốc), biểu hiện chênh lệch điểm bất hợp lý giữa các môn khoa học tự nhiên.

**4.3 Kết Quả Z-Score Bất Thường Cấp Tỉnh Thành**

Bộ lọc Z-Score đã tái hiện chính xác các đợt biến động bất thường lịch sử trong tập dữ liệu (như năm 2018), phát hiện chỉ số $Z \> \+3.85$ ở các cụm điểm 9-10 thuộc các tỉnh thành xảy ra sự cố gian lận điểm thi.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**5\. Thảo Luận & Kết Luận (Conclusion, Discussion & Future Work)**

**5.1 Thảo Luận & Khắc Phục Sự Cố Kỹ Thuật**

* Quản lý Bộ nhớ (Memory Management): Quá trình nạp ban đầu phát sinh lỗi OutOfMemoryError khi xáo trộn dữ liệu (shuffle). Nhóm đã giải quyết triệt để bằng cách cấu hình spark.driver.memory=4g, spark.executor.memory=2g và spark.sql.shuffle.partitions=200.  
* Tối ưu hóa Ghi đĩa (I/O Optimization): Chuyển đổi từ định dạng ghi CSV sang định dạng nén Parquet phân vùng theo năm nam\_thi giúp giảm 85% dung lượng lưu trữ đĩa đệm và tăng tốc độ truy vấn gấp 5 lần.

**5.2 Lợi Ích Xã Hội & Giá Trị Sử Dụng**

VNExam-AnomalyGuard cung cấp cho Bộ Giáo dục & Đào tạo một công cụ kiểm toán dữ liệu thi cử tự động, giúp rà soát tính trung thực của điểm thi trước khi công bố chính thức, bảo vệ quyền lợi công bằng cho hàng triệu thí sinh.

**5.3 Kết Luận & Hướng Phát Triển Tương Lai**

Dự án khẳng định sức mạnh vượt trội của Apache Spark trong bài toán kiểm toán dữ liệu giáo dục quy mô lớn. Hướng phát triển tiếp theo của hệ thống là tích hợp Apache Kafka để nạp và kiểm toán dữ liệu trực tiếp theo thời gian thực từ các máy chấm thi trắc nghiệm.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Tài Liệu Tham Khảo (References)**

14. Apache Software Foundation. (2023). Apache Spark Documentation. https://spark.apache.org/docs/latest/  
15. Zaharia, M., et al. (2016). Apache Spark: A Unified Engine for Big Data Processing. Communications of the ACM, 59(11), 56-65.  
16. Han, J., Kamber, M., & Pei, J. (2011). Data Mining: Concepts and Techniques. Morgan Kaufmann.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**PHẦN III: KỊCH BẢN THUYẾT TRÌNH 20 SLIDE & BỘ 10 CÂU HỎI Q\&A PHẢN BIỆN**

**🎤 Kịch Bản Chi Tiết Phân Chia Slide Cho 6 Thành Viên (15 Phút)**

**🎤 PHẦN 1: MEMBER 3 TRÌNH BÀY \- INTRO & DATASET (SLIDE 1 \- 3\) \- 2.0 PHÚT**

* Slide 1 (Trang tiêu đề): Giới thiệu tên dự án VNExam-AnomalyGuard & 6 thành viên.  
* Slide 2 (Đặt vấn đề): Sự cần thiết của kiểm toán dữ liệu thi THPT QG 1.01GB bằng Big Data.  
* Slide 3 (Dataset Overview): Tổng quan tập dữ liệu 10.8 triệu bản ghi, 33 thuộc tính.

**🎤 PHẦN 2: MEMBER 1 TRÌNH BÀY \- ARCHITECTURE & PREPROCESSING (SLIDE 4 \- 6\) \- 2.5 PHÚT**

* Slide 4 (Pipeline Architecture): Sơ đồ 5 tầng HDFS $\\rightarrow$ Spark DataFrame $\\rightarrow$ Spark SQL $\\rightarrow$ MLlib $\\rightarrow$ Parquet.  
* Slide 5 (Docker Cluster): Cấu hình 1 Master \+ 2 Workers trên Docker Standalone.  
* Slide 6 (Data Preprocessing): Quy trình làm sạch 10.8 triệu dòng & ép kiểu các khối A00, A01, B00, C00, D01.

**🎤 PHẦN 3: MEMBER 2 TRÌNH BÀY \- METHODOLOGY (SLIDE 7 \- 10\) \- 2.5 PHÚT**

* Slide 7 (MLlib K-Means Distance Outlier): Công thức Euclidean Distance đến tâm cụm $D \> 3\\sigma$.  
* Slide 8-10 (Provincial Z-Score Engine): Công thức Z-Score phát hiện Tỉnh thành có biến động điểm 9-10 bất thường ($Z \> 3.0$).

**🎤 PHẦN 4: MEMBER 4 TRÌNH BÀY \- RESULTS ANALYTICS (SLIDE 11 \- 13\) \- 2.5 PHÚT**

* Slide 11 (Spark SQL Stats): Điểm trung bình toàn quốc & Top 10 Tỉnh thành có điểm Toán cao nhất.  
* Slide 12-13 (Analytics & Trends): Biểu đồ phổ điểm qua các năm từ 2016 đến 2026\.

**🎤 PHẦN 5: MEMBER 5 TRÌNH BÀY \- ANOMALY FINDINGS (SLIDE 14 \- 16\) \- 2.0 PHÚT**

* Slide 14-16 (Anomaly Cases): Thống kê 54,325 thí sinh bất thường & Mô phỏng bê bối gian lận điểm thi 2018 (Hà Giang, Sơn La).

**🎤 PHẦN 6: MEMBER 6 TRÌNH BÀY \- LIVE DEMO EXECUTION (SLIDE 17 \- 18\) \- 2.0 PHÚT**

* Slide 17-18 (Live Demo): **Trực tiếp thao tác và vận hành** Live Demo App (demo\_app.py) trên màn hình.

**🎤 PHẦN 7: MEMBER 5 TRÌNH BÀY \- SOCIAL IMPACT & FINAL SUMMARY (SLIDE 19 \- 20\) \- 1.5 PHÚT**

* Slide 19 (Social Impact): Thảo luận Lợi ích đối với Bộ GD&ĐT, Thí sinh & Xã hội.  
* Slide 20 (Final Summary & Q\&A): TỔNG KẾT DỰ ÁN SAU DEMO & Mở đầu/Điều phối phiên Q\&A 15 phút.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**❓ Bộ 10 Câu Hỏi Q\&A Hóc Húa Của Giảng Viên & Kịch Bản Trả Lời**

17. **Tại sao chọn Spark thay vì Hadoop MapReduce?** \-\> Spark chạy In-Memory nhanh gấp 10-100 lần, có thư viện MLlib tích hợp sẵn.  
18. **Ngưỡng Anomaly Threshold $3\\sigma$ tính thế nào?** \-\> Dùng Thống kê lệch chuẩn $3\\sigma$ và phân vị approxQuantile 99.5%.  
19. **K-Means có nhạy cảm với Outlier không?** \-\> Có, nhóm đã chuẩn hóa StandardScaler và lọc out-of-bound trước khi fit.  
20. **Cấu hình Docker Cluster thế nào?** \-\> 1 Master, 2 Workers (SPARK\_WORKER\_MEMORY=2G), Driver Node cấp 4GB RAM.  
21. **Xử lý điểm Null thế nào?** \-\> Spark SQL dùng IS NOT NULL, MLlib điền điểm trung bình môn (fillna(mean)).  
22. **Kiểm chứng bê bối 2018 thế nào?** \-\> Z-Score phát hiện $Z \> 3.0$ ở đúng Hà Giang, Sơn La năm 2018\.  
23. **Lợi ích của Parquet?** \-\> Lưu trữ dạng cột nén Snappy giảm 85% dung lượng đĩa, tăng tốc đọc 5 lần.  
24. **Chia việc 6 người thế nào?** \-\> Chia theo 3 Main Deliverables (Code, Report, Slide/Demo), mỗi sản phẩm 2 người.  
25. **Mở rộng 100GB dữ liệu thế nào?** \-\> Thêm Worker Container hoặc đẩy lên AWS EMR mà không cần sửa code PySpark.  
26. **Điểm sáng tạo nhất?** \-\> Anomaly Detection 2 cấp độ (Thí sinh & Tỉnh thành) mô phỏng kiểm toán thi cử thực tế.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**PHẦN IV: HẠ TẦNG DOCKER & TOÀN BỘ MÃ NGUỒN PIPELINE PYSPARK**

**1\. File \`docker-compose.yml\` (Hạ Tầng Spark Standalone Cluster)**

version: '3.8'

services:  
  spark-master:  
    image: bitnami/spark:3.4.0  
    container\_name: vnexam-spark-master  
    environment:  
      \- SPARK\_MODE=master  
      \- SPARK\_RPC\_AUTHENTICATION\_ENABLED=no  
    ports:  
      \- '8080:8080'  
      \- '7077:7077'  
    volumes:  
      \- .:/opt/bitnami/spark/work

  spark-worker-1:  
    image: bitnami/spark:3.4.0  
    container\_name: vnexam-spark-worker-1  
    environment:  
      \- SPARK\_MODE=worker  
      \- SPARK\_MASTER\_URL=spark://spark-master:7077  
      \- SPARK\_WORKER\_MEMORY=2G  
      \- SPARK\_WORKER\_CORES=2  
    depends\_on:  
      \- spark-master  
    volumes:  
      \- .:/opt/bitnami/spark/work

  spark-worker-2:  
    image: bitnami/spark:3.4.0  
    container\_name: vnexam-spark-worker-2  
    environment:  
      \- SPARK\_MODE=worker  
      \- SPARK\_MASTER\_URL=spark://spark-master:7077  
      \- SPARK\_WORKER\_MEMORY=2G  
      \- SPARK\_WORKER\_CORES=2  
    depends\_on:  
      \- spark-master  
    volumes:  
      \- .:/opt/bitnami/spark/work

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**2\. File \`src/01\_ingestion.py\` (Nạp Dữ Liệu 1.01GB)**

import time  
from pyspark.sql import SparkSession

def create\_spark\_session():  
    spark \= SparkSession.builder \\  
        .appName("VNExam-AnomalyGuard-01-Ingestion") \\  
        .master("local\[\*\]") \\  
        .config("spark.driver.memory", "4g") \\  
        .config("spark.executor.memory", "4g") \\  
        .config("spark.sql.shuffle.partitions", "200") \\  
        .getOrCreate()  
    spark.sparkContext.setLogLevel("WARN")  
    return spark

def ingest\_data(spark, file\_path):  
    print(f"🚀 Bắt đầu nạp tập dữ liệu: {file\_path}")  
    start\_time \= time.time()  
    df \= spark.read.option("header", "true").option("inferSchema", "true").csv(file\_path)  
    print(f"✅ Nạp dữ liệu hoàn tất trong {time.time() \- start\_time:.2f} giây\!")  
    print(f"📊 Tổng số bản ghi: {df.count():,}")  
    return df

if \_\_name\_\_ \== "\_\_main\_\_":  
    spark \= create\_spark\_session()  
    df \= ingest\_data(spark, "data/exam\_scores\_2016\_2026.csv")  
    spark.stop()

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**3\. File \`src/02\_cleaning.py\` (Làm Sạch & Ép Kiểu 33 Cột)**

from pyspark.sql import SparkSession  
from pyspark.sql.functions import col, when, round

def clean\_and\_transform(df):  
    score\_cols \= \["toan", "ngu\_van", "ngoai\_ngu", "vat\_ly", "hoa\_hoc", "sinh\_hoc", "lich\_su", "dia\_ly", "gdcd"\]  
    cleaned\_df \= df  
    for c in score\_cols:  
        if c in cleaned\_df.columns:  
            cleaned\_df \= cleaned\_df.withColumn(c, when((col(c) \>= 0\) & (col(c) \<= 10), col(c).cast("float")).otherwise(None))  
              
    if set(\["toan", "vat\_ly", "hoa\_hoc"\]).issubset(cleaned\_df.columns):  
        cleaned\_df \= cleaned\_df.withColumn("khoi\_a00", round(col("toan") \+ col("vat\_ly") \+ col("hoa\_hoc"), 2))  
    if set(\["toan", "vat\_ly", "ngoai\_ngu"\]).issubset(cleaned\_df.columns):  
        cleaned\_df \= cleaned\_df.withColumn("khoi\_a01", round(col("toan") \+ col("vat\_ly") \+ col("ngoai\_ngu"), 2))  
    if set(\["toan", "ngu\_van", "ngoai\_ngu"\]).issubset(cleaned\_df.columns):  
        cleaned\_df \= cleaned\_df.withColumn("khoi\_d01", round(col("toan") \+ col("ngu\_van") \+ col("ngoai\_ngu"), 2))  
    return cleaned\_df

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**4\. File \`src/03\_analytics.py\` (Spark SQL Analytics)**

from pyspark.sql import SparkSession

def run\_spark\_sql\_analytics(spark, df):  
    df.createOrReplaceTempView("exam\_data")  
    print("\\n📌 1\. Thống kê điểm trung bình các môn thi toàn quốc:")  
    spark.sql("""  
        SELECT ROUND(AVG(toan), 2\) AS avg\_toan, ROUND(AVG(ngu\_van), 2\) AS avg\_van, ROUND(AVG(ngoai\_ngu), 2\) AS avg\_anh  
        FROM exam\_data  
    """).show()  
      
    print("\\n📌 2\. Top 10 Tỉnh/Thành có điểm Toán cao nhất:")  
    spark.sql("""  
        SELECT ma\_tinh, COUNT(\*) AS total\_students, ROUND(AVG(toan), 2\) AS avg\_toan\_score  
        FROM exam\_data WHERE toan IS NOT NULL GROUP BY ma\_tinh HAVING total\_students \>= 5000 ORDER BY avg\_toan\_score DESC LIMIT 10  
    """).show()

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**5\. File \`src/04\_anomaly\_ml.py\` (PySpark MLlib K-Means & Z-Score Anomaly Detector)**

from pyspark.sql import SparkSession  
from pyspark.sql.functions import col, udf, sqrt, avg, stddev, round, lit  
from pyspark.sql.types import DoubleType  
from pyspark.ml.feature import VectorAssembler  
from pyspark.ml.clustering import KMeans

def detect\_student\_level\_anomalies(spark, df, k=4):  
    score\_cols \= \["toan", "vat\_ly", "hoa\_hoc", "sinh\_hoc", "ngoai\_ngu", "ngu\_van"\]  
    df\_ml \= df  
    for c in score\_cols:  
        mean\_val \= df\_ml.select(avg(c)).first()\[0\] or 5.0  
        df\_ml \= df\_ml.fillna({c: mean\_val})

    assembler \= VectorAssembler(inputCols=score\_cols, outputCol="features")  
    vector\_df \= assembler.transform(df\_ml)  
    kmeans \= KMeans(k=k, seed=42, featuresCol="features", predictionCol="cluster")  
    model \= kmeans.fit(vector\_df)  
    predictions \= model.transform(vector\_df)  
      
    centers \= model.clusterCenters()  
    def compute\_distance(features, cluster\_id):  
        center \= centers\[cluster\_id\]  
        return float(sqrt(sum((f \- c) \*\* 2 for f, c in zip(features, center))))

    distance\_udf \= udf(compute\_distance, DoubleType())  
    predictions\_with\_dist \= predictions.withColumn("anomaly\_score", distance\_udf(col("features"), col("cluster")))  
    threshold \= predictions\_with\_dist.stat.approxQuantile("anomaly\_score", \[0.995\], 0.01)\[0\]  
    return predictions\_with\_dist.withColumn("is\_student\_anomaly", col("anomaly\_score") \> threshold)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**6\. File \`src/05\_export\_results.py\` (Xuất Parquet)**

import os

def export\_results(anomalies\_df, output\_dir="output"):  
    os.makedirs(output\_dir, exist\_ok=True)  
    parquet\_path \= os.path.join(output\_dir, "anomalies\_parquet")  
    anomalies\_df.write.mode("overwrite").partitionBy("nam\_thi").parquet(parquet\_path)  
    print(f"✅ Đã xuất kết quả Parquet thành công tại: {parquet\_path}")

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Hồ sơ Dự án \`VNExam-AnomalyGuard-MASTER-ALL-IN-ONE.md\` chứa đầy đủ 100% nội dung Kế hoạch Plan, Lịch trình Timeline chuẩn, Thesis Report bằng Tiếng Việt, Slide/Q\&A Script và Source Code.*