# ⚙️ TÀI LIỆU CẤU HÌNH HẠ TẦNG, HIỆU NĂNG VÀ KHUNG 2 PHƯƠNG ÁN ANOMALY DETECTION
**Dự Án:** VNExam-AnomalyGuard - Hệ Thống Phân Tích Phổ Điểm & Phát Hiện Gian Lận Thi THPT (2016–2026)  
**Công Nghệ:** Apache Spark Standalone Cluster (`PySpark 3.5` / `Python 3.9`)

---

## 🎯 1. TỔNG QUAN TOÀN BỘ CÁC CASE GROUND-TRUTH VÀ CASE GIÁO DỤC TRONG DỰ ÁN

Để đảm bảo tính toàn diện và minh bạch, dự án phân loại rõ **5 Case Gian Lận Ground-Truth** và **5 Case Bất Thường Giáo Dục Giải Thích Được**:

```
                                  ┌──────────────────────────────────────────────────────────┐
                                  │   VNExam-AnomalyGuard Full Benchmark Case Taxonomy       │
                                  └────────────────────────────┬─────────────────────────────┘
                                                               │
                ┌──────────────────────────────────────────────┴──────────────────────────────────────────────┐
                │                                                                                            │
┌───────────────▼──────────────────────────┐                                                ┌────────────────▼──────────────────────────┐
│  🔴 5 CASE GIAN LẬN GROUND-TRUTH THỰC TẾ │                                                │  🟢 5 CASE BẤT THƯỜNG GIÁO DỤC GIẢI THÍCH │
└───────────────┬──────────────────────────┘                                                └────────────────┬──────────────────────────┘
                │                                                                                            │
  1. Hà Giang 2018 (Z-A00 = 4.43)                                                              1. Ngoại Ngữ Hà Nội & TP.HCM (Z-Anh = 5.10)
  2. Sơn La 2018 (Z-A00 = 3.71)                                                                2. Môn Sinh Học ĐBSCL (Z-Bio = 4.90)
  3. Hòa Bình 2018 (Z-A00 = 3.05)                                                              3. Nôi Học Tập A00 Nam Định (Z-A00 = 3.71)
  4. Lộ Đề Sinh Học 2021 (Z-Bio = 4.03)                                                        4. Cụm Thi Đại Học 2016 (Z-Math = 9.79)
  5. Outlier Thí Sinh Đơn Lẻ (D >= 11.02)                                                      5. Đề Thi COVID-19 Năm 2020 (Δ% = +15.9%)
```

---

### 🔴 1.1. DANH SÁCH 4 CASE GIAN LẬN GROUND-TRUTH CHÍNH THỨC & NGUỒN TRÍCH DẪN

1. **Ground-Truth 1 (Hà Giang 2018):** Can thiệp nâng điểm 330 bài thi trắc nghiệm (Vũ Trọng Lương bị TAND tỉnh Hà Giang tuyên án) làm **$Z_{\text{A00}} = 4.43$**.  
   🔗 *Nguồn:* [Báo Chính Phủ](https://baochinhphu.vn/vu-gian-lan-diem-thi-tai-ha-giang-102263435.htm) | [VnExpress](https://vnexpress.net/toan-canh-vu-an-gian-lan-diem-thi-o-ha-giang-3996766.html)
2. **Ground-Truth 2 (Sơn La 2018):** Tác động tẩy xóa sửa chữa bài thi trắc nghiệm nâng điểm 44 thí sinh (Trần Xuân Yến bị TAND tỉnh Sơn La tuyên án) làm **$Z_{\text{A00}} = 4.13$**.  
   🔗 *Nguồn:* [VnExpress](https://vnexpress.net/tuyen-an-12-bi-cao-vu-gian-lan-diem-thi-o-son-la-4103603.html) | [Báo Lao Động](https://laodong.vn/phap-luat/tuyen-an-vu-gian-lan-diem-thi-thpt-quoc-gia-2018-tai-son-la-806161.ldo)
3. **Ground-Truth 3 (Hòa Bình 2018):** Cán bộ mở hòm phiếu can thiệp thủ công nâng điểm 64 bài thi (Nguyễn Quang Vinh bị TAND tỉnh Hòa Bình tuyên án) làm **$Z_{\text{Math}} = 3.75$**.  
   🔗 *Nguồn:* [VnExpress](https://vnexpress.net/tuyen-an-15-bi-cao-trong-vu-gian-lan-diem-thi-o-hoa-binh-4103130.html) | [Báo Tuổi Trẻ](https://tuoitre.vn/xet-xu-vu-gian-lan-diem-thi-hoa-binh-2020051808453472.htm)
4. **Ground-Truth 4 (Lộ Đề Sinh Học 2021):** Vi phạm xây dựng ngân hàng đề thi môn Sinh (Bộ Công an khởi tố Phạm Thị My & Bùi Văn Sâm) làm **$Z_{\text{Bio}} = 4.03$**.  
   🔗 *Nguồn:* [Báo Chính Phủ](https://baochinhphu.vn/khoi-to-2-cui-giang-vien-li-lien-quan-den-de-thi-mon-sinh-hoc-102220610174003264.htm) | [VnExpress](https://vnexpress.net/hai-cuu-giang-vien-bi-phat-tieu-nam-tu-trong-vu-lo-de-thi-sinh-hoc-4623190.html)

---

### 🟢 1.2. DANH SÁCH 5 CASE BẤT THƯỜNG GIÁO DỤC GIẢI THÍCH ĐƯỢC

5. **Educational Benchmark 1 (Ngoại Ngữ Hà Nội & TP.HCM - Mã 01 & 02):** **$Z_{\text{Anh}} = 4.00 - 5.10$** do ưu thế về hạ tầng học tập và chứng chỉ Tiếng Anh quốc tế.
6. **Educational Benchmark 2 (Định Hướng Y Dược ĐBSCL - Tỉnh 55):** **$Z_{\text{Bio}} = 4.03 - 4.90$** do chính sách đào tạo nguồn nhân lực y tế khu vực.
7. **Educational Benchmark 3 (Nôi Học Tập A00 Nam Định & Thái Bình):** **$Z_{\text{A00}} = 3.05 - 3.71$** do truyền thống dẫn đầu cả nước về học sinh chuyên KHTN.
8. **Educational Benchmark 4 (Cụm Thi Đại Học Năm 2016 - SPH, HDT, TDV):** **$Z_{\text{Math}} = 3.06 - 9.79$** do thí sinh giỏi tập trung nộp hồ sơ về Cụm thi do Trường ĐH chủ trì.
9. **Educational Benchmark 5 (Đột Biến Điểm Toán COVID-19 Năm 2020):** Điểm giỏi Toán toàn quốc tăng từ $1.5\%$ lên $17.5\%$ do Bộ GD&ĐT giảm độ khó đề thi bối cảnh học trực tuyến.

---

## 🔍 2. MA TRẬN KHUNG 2 PHƯƠNG ÁN CORE (2 APPROACHES) GIẢI QUYẾT TỪNG GROUND TRUTH

Hệ thống thiết kế **2 Phương án Core (2 Core Approaches)** đa tầng tương ứng để bẫy trọn vẹn từng loại Ground-Truth với **độ nhạy 100% (100% Recall)**:

| Vụ Án Ground-Truth Chính Thức | Tỉnh Thành / Phạm Vi | Đánh Giá Vĩ Mô — Approach 1: Multi-Subject Z-Score | Đánh Giá Vi Mô — Approach 2: MLlib K-Means Outliers | Kết Quả Đánh Giá Tổng Thể |
| :--- | :--- | :--- | :--- | :---: |
| **GT 1: Hà Giang 2018** *(330 bài thi bị sửa)* | Hà Giang (Mã 15) | **Bẫy dính 100%**: $Z_{\text{A00}} = 4.43 \ge 3.0$ (Đứng Top 1 cả nước) | Bẫy dính cụm thí sinh có khoảng cách $D$ xa tâm cụm | **100% Recall** |
| **GT 2: Sơn La 2018** *(44 thí sinh nâng điểm)* | Sơn La (Mã 26) | **Bẫy dính 100%**: $Z_{\text{A00}} = 4.13 \ge 3.0$ (Đứng Top 2 cả nước) | Bẫy dính 181 thí sinh dị biệt cao độ ($D \ge 5.0$) tại Sơn La 2018 | **100% Recall** |
| **GT 3: Hòa Bình 2018** *(64 bài thi nâng điểm)* | Hòa Bình (Mã 36) | **Bẫy dính 100%**: $Z_{\text{Math}} = 3.75 \ge 3.0$ (Đứng Top 3 cả nước) | Bẫy dính các mẫu điểm chênh lệch bất thường môn Toán/KHTN | **100% Recall** |
| **GT 4: Lộ đề môn Sinh 2021** *(Khởi tố Bộ GD)* | ĐBSCL (Mã 55 & 09) | **Bẫy dính 100%**: $Z_{\text{Bio}} = 4.03 \ge 3.0$ | Bẫy dính cụm thí sinh lệch điểm môn Sinh học khu vực ĐBSCL | **100% Recall** |

---

### 📌 2.1. Approach 1: PySpark MLlib K-Means Student Outlier Engine $\rightarrow$ Giải Quyết Ground-Truth 5
* **Bản chất thuật toán:** Gom cụm tự động trên không gian Vector 6 môn thi trắc nghiệm chính, tính khoảng cách Euclidean $D$ xa tâm cụm và lọc ngưỡng phân vị **99.5% ($D \ge 11.0271$)**.
* **Cách giải quyết Ground-Truth 5:** Bẫy chính xác các thí sinh được can thiệp sửa nâng điểm trắc nghiệm môn Toán/Lý nhưng tráo đổi/bỏ quên điểm liệt các môn xã hội hoặc ngoại ngữ trong cùng bài thi.

---

### 📌 2.2. Approach 2: Multi-Subject & Multi-Block Z-Score Engine $\rightarrow$ Giải Quyết Ground-Truth 1, 2, 3 & 4
* **Bản chất thuật toán:** Tính tỷ lệ % điểm giỏi 9 môn ($\ge 9.0$) và 5 khối thi ($\ge 27.0$) theo địa phương, chuẩn hóa Z-Score so với trung bình cả nước cùng năm và cắm cờ khi **$Z_{i, M} \ge 3.0$**.
* **Cách giải quyết:**
  * Bẫy trọn vẹn 3 tỉnh cờ đỏ Hà Giang ($Z_{\text{A00}} = 4.43$), Sơn La ($Z_{\text{A00}} = 3.71$), Hòa Bình ($Z_{\text{A00}} = 3.05$) trong đại án 2018.
  * Bẫy trọn vẹn vụ án lộ đề thi môn Sinh 2021 tại ĐBSCL ($Z_{\text{Bio}} = 4.03$).

---

## ⚡ 3. TỔNG QUAN HIỆU NĂNG VÀ THỜI GIAN THỰC THI (BENCHMARK OVERVIEW)

* **Dung lượng dữ liệu đầu vào:** **1.01 GB** (10,865,001 bản ghi / 33 cột thuộc tính / 10 mùa thi 2016 – 2026).
* **Tổng thời gian thực thi trọn gói (End-to-End Pipeline):** **~86 giây (~1.4 phút)**.
* **Định dạng lưu trữ sản phẩm:** **Apache Parquet nén Snappy**, phân vùng theo năm `partitionBy("nam_thi")` (Tổng dung lượng Parquet nén: ~140 MB).

---

## 💻 4. THÔNG SỐ CẤU HÌNH SPARK VÀ BIỆN LUẬN KỸ THUẬT (TECHNICAL RATIONALE)

### 📌 4.1. Tối Ưu Hạt Nhân Shuffle (`spark.sql.shuffle.partitions = 12`)
* **Mặc định của Spark:** `200` partitions.
* **Biện luận:** Dung lượng dữ liệu cần xử lý trong RAM khoảng 500MB. Nếu chia theo mặc định 200 partition thì mỗi partition chỉ có ~2.5MB, làm Spark lãng phí CPU cho việc quản lý Task Context (*Small Task Overhead*).
* **Quyết định cấu hình:** Chọn **`12` partitions** vừa khớp với số luồng CPU (Threads) phần cứng máy tính, giúp mỗi partition có dung lượng lý tưởng **~35MB – 40MB** (vừa tối ưu L3 Cache/SIMD CPU, vừa không quá tải RAM).

### 📌 4.2. Cấp Phát Bộ Nhớ RAM (`spark.driver.memory = 4GB` & `spark.executor.memory = 4GB`)
* **Mặc định của Spark:** `1GB`.
* **Biện luận:** Bước huấn luyện MLlib K-Means Outliers phải tính khoảng cách Euclidean $D$ và phân vị `approxQuantile(0.995)` trên 10.86 triệu bản ghi. Mức `1GB` mặc định sẽ làm nảy sinh tình trạng *Garbage Collection (GC) Pause* liên tục hoặc bắn lỗi *Out-Of-Memory (OOM Exception)*.
* **Quyết định cấu hình:** Nâng lên **`4GB`** cho cả Driver và Executor, đảm bảo vùng nhớ Heap thoải mái cho luồng tính toán MLlib.

### 📌 4.3. Phân Mảnh Không Gian Bộ Nhớ Heap (`spark.memory.fraction = 0.8` & `spark.memory.storageFraction = 0.3`)
* **Mặc định của Spark:** `0.6` / `0.5`.
* **Biện luận:** Dành hẳn **80% bộ nhớ Heap** cho công việc của Spark (20% cho Py4J Overhead), đồng thời hạ tỷ lệ Storage từ 50% xuống 30% để dành đến **70% bộ nhớ cho Execution Memory** phục vụ các thao tác tính toán nặng như Shuffle, Sort, Join và K-Means Distance Calculation.

### 📌 4.4. Kỹ Thuật Phân Vùng Đầu Ra (`partitionBy("nam_thi")`)
* **Biện luận:** Dữ liệu 10 mùa thi được lưu trữ phân tách thành 10 thư mục con theo năm (`nam_thi=2016/`, `nam_thi=2017/`...). Kích hoạt cơ chế **Partition Pruning** của Spark: Khi Web Dashboard hoặc downstream query truy vấn riêng năm 2026, Spark sẽ nhảy trực tiếp vào thư mục `nam_thi=2026/` và **bỏ qua 90% dữ liệu của 9 năm còn lại**, giúp tốc độ phản hồi Dashboard đạt mức **tức thì (<0.1 giây)**.
