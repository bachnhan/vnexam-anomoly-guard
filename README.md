# VNExam-AnomalyGuard

> **Hệ Thống Phân Tích Phổ Điểm & Phát Hiện Gian Lận Điểm Thi THPT Quốc Gia (2016–2026) Trên Nền Tảng Apache Spark**  
> *Bài tập nhóm cuối kỳ môn Big Data Processing (BDA501)*

---

## 📊 Tập Dữ Liệu

- **Kaggle Dataset:** [Vietnam National Examination Scores 2016–2026](https://www.kaggle.com/datasets/bchnhnnguynhunh/viet-name-national-exam-scores-2016-2026)
- **Quy mô:** **1.01 GB** · 10,865,001 bản ghi · 33 thuộc tính
- **Phạm vi:** Điểm thi THPT Quốc Gia Việt Nam · 10 mùa thi (2016–2026)
- **Tự động Mount/Tải dữ liệu:** Tự động kết nối với Kaggle API qua `kagglehub` để tải về nếu máy chưa có dữ liệu thô.

---

## 📁 Cấu Trúc Thư Mục

```text
vnexam-anomoly-guard/
├── README.md
├── docker-compose.yml                    # Spark Standalone Cluster (1 Master + 2 Workers)
├── requirements.txt
├── main.py                               # Entrypoint chính điều phối toàn bộ PySpark pipeline
│
├── data/
│   ├── metadata/
│   │   └── ma_tinh.csv                   # Bảng tra cứu mã tỉnh/thành & cụm thi chuẩn
│   └── processed/
│       └── exam_scores_2016_2026.csv     # Dataset gốc 1.01 GB (tự động mount từ Kaggle)
│
├── scripts/
│   ├── etl_process.py                    # ETL tiền xử lý gộp file dữ liệu
│   └── download_dataset.py               # Script tự động mount/download dataset từ Kaggle
│
├── src/                                  # PySpark Pipeline (2 Phương Án Core)
│   ├── ingestion.py                      # Step 01: Nạp dữ liệu, tạo SparkSession
│   ├── cleaning.py                       # Step 02: Làm sạch, validate [0,10], tính khối thi
│   ├── analytics.py                      # Step 03: Spark SQL — điểm TB, top tỉnh, biến động
│   ├── anomaly_ml.py                     # Step 04: K-Means (thí sinh) + Z-Score (tỉnh thành)
│   └── export_results.py                 # Step 05: Xuất Parquet + CSV UTF-8 + JSON
│
├── output/                               # Kết quả pipeline (tự động sinh khi chạy)
│   ├── province_anomalies_parquet/       # Z-Score tỉnh thành (Parquet)
│   ├── student_anomalies_parquet/        # K-Means thí sinh bị dán nhãn bất thường (Parquet)
│   ├── province_anomalies_top15.csv      # Báo cáo Top 15 tỉnh Z-Score (UTF-8 BOM cho Excel)
│   └── province_anomalies_full.csv       # Báo cáo toàn bộ tỉnh Z-Score (UTF-8 BOM cho Excel)
│
└── demo/                                 # Streamlit Dashboard
    ├── web_app.py                        # Entry point — chạy: python3 -m streamlit run demo/web_app.py
    ├── dashboard_data.json               # Metadata: KPI, ground_truth, fallback data
    ├── spark_computed_meta.json          # Metadata tính toán 100% từ Spark
    ├── yearly_subjects.json              # Điểm TB môn theo năm (tự động xuất khi chạy pipeline)
    ├── config.py                         # Cấu hình, NAV_ITEMS, paths
    ├── data/loader.py                    # Đọc Parquet / JSON fallback
    ├── styles/theme.css                  # Glassmorphism UI
    ├── components/                       # Sidebar, Appbar, Widgets
    └── views/
        ├── tong_quan_page.py             # 🎯 Tổng Quan — KPI pipeline
        ├── thong_ke_page.py              # 📊 Thống Kê Mô Tả — bảng TB môn, top tỉnh, chart
        ├── kmeans_page.py                # 🔍 K-Means Thí Sinh — outlier count, specimen
        └── zscore_page.py                # 🏛️ Z-Score Tỉnh Thành — filter Z >= 3.0, 2018 validation
```

---

## 🚀 Hướng Dẫn Chạy Pipeline

### 1. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 2. Tải/Mount Dataset từ Kaggle (Tùy chọn)
Nếu máy bạn chưa có file dữ liệu 1.01GB, bạn có thể tải tự động bằng lệnh:
```bash
python3 scripts/download_dataset.py
```
*(Nếu bỏ qua bước này, `main.py` sẽ tự động phát hiện và tải từ Kaggle giúp bạn khi chạy pipeline).*

### 3. Chạy toàn bộ pipeline (Local Mode)
```bash
python3 main.py --mode local
```

Pipeline tự động sinh các file kết quả tại `output/`:
```
output/province_anomalies_parquet/   ← Z-Score tỉnh thành (Parquet)
output/student_anomalies_parquet/    ← K-Means thí sinh (Parquet)
output/province_anomalies_top15.csv  ← Báo cáo Top 15 Z-Score (Mở Excel không lỗi font)
output/province_anomalies_full.csv   ← Báo cáo đầy đủ Z-Score (Mở Excel không lỗi font)
demo/yearly_subjects.json            ← Điểm TB môn theo năm (dùng cho dashboard)
demo/spark_computed_meta.json        ← Chỉ số KPI tính toán từ Spark
```

### 4. Khởi chạy Dashboard
```bash
python3 -m streamlit run demo/web_app.py
```
Mở trình duyệt: **http://localhost:8501** (hoặc port khả dụng).

---

## 📋 Data Contract — Schema Bắt Buộc

### `output/province_anomalies_parquet`

| Cột | Kiểu | Mô tả |
|---|---|---|
| `nam_thi` | int | Năm thi (2016–2026) |
| `ma_tinh` | string | Mã tỉnh / mã cụm thi |
| `ten_tinh` | string | Tên tỉnh / tên cụm thi chuẩn tiếng Việt |
| `total_students` | int | Tổng thí sinh cụm đó |
| `avg_toan` | float | Điểm TB môn Toán |
| `high_math_pct` | float | % điểm Toán ≥ 9.0 |
| `z_math` | float | Z-Score môn Toán |
| `z_a00` | float | Z-Score khối A00 |
| `z_bio` | float | Z-Score môn Sinh |
| `z_score` | float | Z-Score tổng hợp (max các môn/khối) |
| `is_province_anomaly` | bool | True nếu Z ≥ 3.0 (vượt ngưỡng 3σ) |

### `output/student_anomalies_parquet`

| Cột | Kiểu | Mô tả |
|---|---|---|
| `sbd` | string | Số báo danh |
| `nam_thi` | int | Năm thi |
| `ma_tinh` | string | Mã tỉnh / mã cụm thi |
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

---

## 🔄 Cách Ráp Output Vào Dashboard

Dashboard ([demo/data/loader.py](file:///Users/cation/big-data/final_project/demo/data/loader.py)) tự động đọc theo thứ tự ưu tiên:

```
1. output/province_anomalies_parquet  → Trang Z-Score Tỉnh Thành
2. output/student_anomalies_parquet   → Trang K-Means Thí Sinh
3. demo/yearly_subjects.json          → Trang Thống Kê Mô Tả
4. demo/spark_computed_meta.json      → KPI & Specimen Thí Sinh
5. demo/dashboard_data.json           → Fallback tự động khi chưa có Parquet (demo mode)
```

---

## 💻 Nội Dung Dashboard (4 trang)

| Trang | Nội dung |
|---|---|
| 🎯 **Tổng Quan** | 5 KPI cards: tổng records, dataset size, province alerts, student outliers, recall 100% |
| 📊 **Thống Kê Mô Tả** | Bảng điểm TB 9 môn/năm · Top 10 tỉnh Toán (≥500 TS) · Chart KHTN vs KHXH |
| 🔍 **K-Means Thí Sinh** | Tổng + % thí sinh bị cờ · 2 specimen cards · Bảng outliers |
| 🏛️ **Z-Score Tỉnh Thành** | Filter Z ≥ 3.0 · Ground-truth Hà Giang/Sơn La/Hòa Bình (3/3 = 100% Recall) · Bảng Z-Score 2018 |
