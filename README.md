# VNExam-AnomalyGuard

> **Hệ Thống Phân Tích Phổ Điểm & Phát Hiện Gian Lận Điểm Thi THPT Quốc Gia (2016–2026) Trên Nền Tảng Apache Spark**  
> *Bài tập nhóm cuối kỳ môn Big Data Processing (BDA501)*

---

## 📊 Tập Dữ Liệu

- **Kaggle Dataset:** [Vietnam National Examination Scores 2016–2026](https://www.kaggle.com/datasets/bchnhnnguynhunh/viet-name-national-exam-scores-2016-2026)
- **Quy mô:** **1.01 GB** · 10,865,001 bản ghi · 33 thuộc tính
- **Phạm vi:** Điểm thi THPT Quốc Gia Việt Nam · 10 mùa thi (2016–2026)

---

## 📁 Cấu Trúc Thư Mục

```text
vnexam-anomoly-guard/
├── README.md
├── docker-compose.yml                    # Spark Standalone Cluster (1 Master + 2 Workers)
├── requirements.txt
├── main.py                               # Entrypoint chính điều phối toàn bộ pipeline
│
├── data/
│   ├── metadata/
│   │   └── ma_tinh.csv                   # Bảng mã tỉnh/thành
│   └── processed/
│       └── exam_scores_2016_2026.csv     # Dataset gốc 1.01 GB (cần tải từ Kaggle)
│
├── scripts/
│   └── etl_process.py                    # ETL tiền xử lý gộp file dữ liệu
│
├── src/                                  # PySpark Pipeline (5 bước)
│   ├── ingestion.py                      # Step 01: Nạp dữ liệu, tạo SparkSession
│   ├── cleaning.py                       # Step 02: Làm sạch, validate [0,10], tính khối thi
│   ├── analytics.py                      # Step 03: Spark SQL — điểm TB, top tỉnh, biến động
│   ├── anomaly_ml.py                     # Step 04: K-Means (cấp thí sinh) + Z-Score (cấp tỉnh)
│   ├── export_results.py                 # Step 05: Xuất Parquet + yearly_subjects.json
│   └── sota_audit.py                     # SOTA Forensic Audit (Benford, Mahalanobis, Entropy)
│
├── output/                               # Kết quả pipeline (tự tạo khi chạy)
│   ├── province_anomalies_parquet/       # Z-Score tỉnh thành (65 tỉnh × 11 năm)
│   └── student_anomalies_parquet/        # K-Means thí sinh bị gắn cờ
│
├── demo/                                 # Streamlit Dashboard
│   ├── web_app.py                        # Entry point — chạy: streamlit run demo/web_app.py
│   ├── dashboard_data.json               # Metadata: KPI, ground_truth, fallback data
│   ├── yearly_subjects.json              # Điểm TB môn theo năm (tự tạo khi chạy pipeline)
│   ├── config.py                         # Cấu hình, NAV_ITEMS, paths
│   ├── data/loader.py                    # Đọc Parquet / JSON fallback
│   ├── styles/theme.css                  # Glassmorphism UI
│   ├── components/                       # Sidebar, Appbar, Widgets
│   ├── views/
│   │   ├── tong_quan_page.py             #  Tổng Quan — KPI pipeline
│   │   ├── thong_ke_page.py              #  Thống Kê Mô Tả — bảng TB môn, top tỉnh, chart
│   │   ├── kmeans_page.py                #  K-Means Thí Sinh — outlier count, specimen
│   │   └── zscore_page.py                #  Z-Score Tỉnh Thành — filter, 2018 validation
│   └── templates/                        # HTML templates cho widgets
│
└── docs/
    ├── VNExam-AnomalyGuard-MASTER-ALL-IN-ONE.md # Tài liệu Master ALL-IN-ONE tổng hợp dự án
    ├── BAO_CAO_CUOI_KY_BIGDATA.md # Luận văn báo cáo cuối kỳ chuẩn IMRaD (Tiếng Việt)
    └── SLIDE_THUYET_TRINH_15MIN.md # Kịch bản 20 Slide thuyết trình & Bộ 10 câu hỏi Q&A
```

---

##  Hướng Dẫn Chạy Pipeline

### 1. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 2. Chạy toàn bộ pipeline (local mode)
```bash
python src/05_export_results.py
```

Pipeline tự động tạo 3 output:
```
output/province_anomalies_parquet/   ← Z-Score tỉnh thành
output/student_anomalies_parquet/    ← K-Means thí sinh
demo/yearly_subjects.json            ← Điểm TB môn theo năm (dùng cho dashboard)
```

### 3. Khởi chạy Dashboard
```bash
streamlit run demo/web_app.py
```
Mở trình duyệt: **http://localhost:8501**

---

## 📋 Data Contract — Schema Bắt Buộc

### `output/province_anomalies_parquet`

| Cột | Kiểu | Mô tả |
|---|---|---|
| `nam_thi` | int | Năm thi (2016–2026) |
| `ma_tinh` | string | Mã tỉnh/thành |
| `ten_tinh` | string | Tên tỉnh/thành |
| `total_students` | int | Tổng thí sinh năm đó |
| `avg_toan` | float | Điểm TB môn Toán *(dùng Req 1b)* |
| `high_math_pct` | float | % điểm Toán ≥ 9.0 |
| `z_math` | float | Z-Score môn Toán |
| `z_a00` | float | Z-Score khối A00 |
| `z_bio` | float | Z-Score môn Sinh |
| `z_score` | float | Z-Score tổng hợp (max các môn) |
| `is_province_anomaly` | bool | True nếu Z ≥ 3.0 hoặc YoY spike |
| `yoy_math_delta_pct` | float | % thay đổi so với năm trước |

### `output/student_anomalies_parquet`

| Cột | Kiểu | Mô tả |
|---|---|---|
| `sbd` | string | Số báo danh |
| `nam_thi` | int | Năm thi |
| `ma_tinh` | string | Mã tỉnh |
| `toan` | float | Điểm Toán |
| `ngu_van` | float | Điểm Ngữ Văn |
| `ngoai_ngu` | float | Điểm Ngoại Ngữ |
| `vat_ly` | float | Điểm Vật Lý |
| `hoa_hoc` | float | Điểm Hóa Học |
| `sinh_hoc` | float | Điểm Sinh Học |
| `cluster` | int | Cluster K-Means (0–3) |
| `anomaly_score` | float | Khoảng cách Euclidean tới centroid |
| `anomaly_pattern` | string | VD: "Toán cao + Lý liệt" |
| `is_student_anomaly` | bool | True = vượt ngưỡng 99.5th percentile |

### `demo/yearly_subjects.json`

| Cột | Kiểu | Mô tả |
|---|---|---|
| `nam_thi` | int | Năm thi |
| `avg_toan` | float | Điểm TB Toán toàn quốc |
| `avg_nguvan` | float | Điểm TB Ngữ Văn |
| `avg_ngoaingu` | float | Điểm TB Ngoại Ngữ |
| `avg_vatly` | float | Điểm TB Vật Lý |
| `avg_hoahoc` | float | Điểm TB Hóa Học |
| `avg_sinhhoc` | float | Điểm TB Sinh Học |
| `avg_khtn` | float | TB khối KHTN = (Toán+Lý+Hóa)/3 |
| `avg_khxh` | float | TB khối KHXH = (Văn+Sinh)/2 |

---

##  Cách Ráp Output Vào Dashboard

Dashboard (`demo/data/loader.py`) đọc theo thứ tự ưu tiên:

```
1. output/province_anomalies_parquet  → Trang Z-Score Tỉnh Thành (filter, bảng 2018)
2. output/student_anomalies_parquet   → Trang K-Means Thí Sinh (count, specimen, bảng)
3. demo/yearly_subjects.json          → Trang Thống Kê (bảng TB môn, chart KHTN/KHXH)
4. demo/dashboard_data.json           → Fallback nếu Parquet chưa có (demo mode)
```

**Khi có đủ 3 output từ pipeline → dashboard tự động hiển thị data thật, không cần sửa code.**

---

##  Nội Dung Dashboard (4 trang)

| Trang | Yêu cầu | Nội dung |
|---|---|---|
|  **Tổng Quan** | Req 3a, 4a | 5 KPI cards: tổng records, dataset size, province alerts, student outliers, recall |
|  **Thống Kê Mô Tả** | Req 1a, 1b, 2a | Bảng điểm TB 9 môn/năm · Top 10 tỉnh Toán (≥5000 TS) · Chart KHTN vs KHXH |
|  **K-Means Thí Sinh** | Req 4a, 4b | Tổng + % thí sinh bị cờ · 2 specimen cards · Bảng outliers |
|  **Z-Score Tỉnh Thành** | Req 3b, 5a | Filter Z > 3.0 · Ground-truth 3/3 · Bảng Z-Score 2018 |
