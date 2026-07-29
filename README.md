# VNExam-AnomalyGuard

> **Hệ Thống Phân Tích Phổ Điểm & Phát Hiện Gian Lận Điểm Thi THPT Quốc Gia (2016–2026) Trên Nền Tảng Apache Spark**  
> *Bài tập nhóm cuối kỳ môn Big Data Processing (BDA501)*

---

## 📁 Cấu Trúc Thư Mục Dự Án (Project Structure)

```text
final_project/
├── README.md                                # Hướng dẫn sử dụng & Tổng quan dự án
├── docker-compose.yml                       # Cấu hình Spark Standalone Cluster (1 Master + 2 Workers)
├── requirements.txt                         # Danh sách thư viện Python phụ thuộc
├── main.py                                  # Entrypoint chính điều phối PySpark Pipeline (Input -> Output)
├── data/
│   └── processed/
│       └── exam_scores_2016_2026.csv        # Tập dữ liệu Big Data 1.01 GB (10,865,001 bản ghi)
├── scripts/
│   └── etl_process.py                      # Script ETL tiền xử lý gộp các file dữ liệu thi 2016-2026
├── src/                                     # Mã nguồn PySpark Pipeline chuẩn hóa
│   ├── __init__.py
│   ├── ingestion.py                         # Step 01: Nạp dữ liệu 1.01GB với SparkSession tối ưu RAM
│   ├── cleaning.py                          # Step 02: Làm sạch, validate [0, 10] & tính điểm khối thi
│   ├── analytics.py                         # Step 03: Spark SQL Analytics phổ điểm & Tỉnh/Thành
│   ├── anomaly_ml.py                        # Step 04: MLlib K-Means & Statistical Z-Score Engine
│   ├── export_results.py                    # Step 05: Xuất kết quả nén Parquet phân vùng theo năm
│   ├── 01_ingestion.py                      # [Wrapper] Thực thi riêng lẻ Step 01
│   ├── 02_cleaning.py                       # [Wrapper] Thực thi riêng lẻ Step 02
│   ├── 03_analytics.py                      # [Wrapper] Thực thi riêng lẻ Step 03
│   ├── 04_anomaly_ml.py                     # [Wrapper] Thực thi riêng lẻ Step 04
│   └── 05_export_results.py                 # [Wrapper] Thực thi riêng lẻ Step 05
├── demo/                                    # Dashboard trực quan hoá kết quả (Streamlit)
│   ├── web_app.py                           # Entry point — router duy nhất (~70 dòng)
│   ├── config.py                            # Centralized config: paths, nav, constants
│   ├── dashboard_data.json                  # Metadata: KPI, ground_truth, SOTA results
│   ├── styles/
│   │   ├── theme.css                        # CSS thuần — Angular Material + Glassmorphism
│   │   └── theme.py                         # inject_css() đọc theme.css vào Streamlit
│   ├── templates/                           # HTML template files (string.Template)
│   │   ├── appbar.html, kpi_card.html ...   # 10 file HTML thuần
│   ├── data/
│   │   └── loader.py                        # load_data(): đọc Parquet → fallback JSON
│   ├── components/
│   │   ├── widgets.py                       # glass_kpi, gls_alert, ang_section, ...
│   │   ├── sidebar.py                       # render_sidebar() → trả về page key
│   │   └── appbar.py                        # render_appbar()
│   └── views/                               # Mỗi file = 1 trang (render function)
│       ├── data_source_page.py              # Nguồn dữ liệu, schema, collection method
│       ├── kpi_page.py                      # KPI tổng quan + Spark code snippets
│       ├── province_page.py                 # Z-Score analysis theo tỉnh
│       ├── students_page.py                 # K-Means student outliers
│       ├── ground_truth_page.py             # Validate 3 vụ gian lận thật
│       └── sota_page.py                     # Benford / Mahalanobis / Shannon Entropy
├── output/                                  # OUTPUT của Spark pipeline (tạo sau khi chạy)
│   ├── province_anomalies_parquet/          # ← Dashboard đọc file này
│   └── student_anomalies_parquet/           # ← Dashboard đọc file này
└── docs/
    ├── VNExam-AnomalyGuard-MASTER-ALL-IN-ONE.md # Tài liệu Master tổng hợp dự án
    ├── BAO_CAO_CUOI_KY_BIGDATA.md           # Luận văn báo cáo cuối kỳ chuẩn IMRaD (Tiếng Việt)
    └── SLIDE_THUYET_TRINH_15MIN.md          # Kịch bản 20 Slide thuyết trình & Bộ 10 câu hỏi Q&A
```

---

## 🚀 Hướng Dẫn Vận Hành (Quick Start)

### 1. Cài đặt Thư viện
```bash
pip install -r requirements.txt
```

### 2. Thực thi Pipeline PySpark (Local Mode)
```bash
python3 main.py --mode local
```

### 3. Triển khai Docker Cluster & Submit Job
```bash
docker-compose up -d
python3 main.py --mode cluster --master spark://localhost:7077
```

### 4. Khởi chạy Dashboard Demo
```bash
cd demo
streamlit run web_app.py --server.port 8501
```
Mở browser: **http://localhost:8501**

> - Badge **"✓ Parquet Pipeline"** → đang đọc data thật từ `output/`
> - Badge **"◈ JSON Demo Mode"** → chưa có Parquet, dùng data mẫu từ `dashboard_data.json`

---

## 📋 Data Contract — Schema Parquet bắt buộc

> Dashboard (`demo/data/loader.py`) tự động đọc Parquet nếu tồn tại.  
> Spark pipeline phải export **đúng tên cột** sau:

### `output/province_anomalies_parquet` — mỗi row = 1 cặp (tỉnh, năm)

| Cột | Kiểu | Bắt buộc | Mô tả |
|-----|------|:--------:|---------|
| `nam_thi` | int | ✅ | Năm thi: 2016–2026 |
| `ma_tinh` | string | ✅ | Mã tỉnh: "15", "26", "36"... |
| `total_students` | int | ✅ | Tổng thí sinh tỉnh đó năm đó |
| `high_math_pct` | float | ✅ | % thí sinh Toán ≥ 9.0 |
| `z_math` | float | ✅ | Z-Score của high_math_pct so cả nước |
| `z_score` | float | ✅ | Z-Score tổng hợp (max các chỉ số) |
| `is_province_anomaly` | bool | ✅ | True nếu z_score ≥ 3.0 |
| `z_a00` | float | ⚠️ | Z-Score khối A00 |
| `z_bio` | float | ⚠️ | Z-Score Sinh học |
| `yoy_math_delta_pct` | float | ⚠️ | % thay đổi so năm trước |

### `output/student_anomalies_parquet` — mỗi row = 1 thí sinh bị đánh cờ

| Cột | Kiểu | Bắt buộc | Mô tả |
|-----|------|:--------:|---------|
| `sbd` | string | ✅ | Số báo danh |
| `nam_thi` | int | ✅ | Năm thi |
| `ma_tinh` | string | ✅ | Mã tỉnh |
| `toan` | float | ✅ | Điểm Toán |
| `ngu_van` | float | ✅ | Điểm Ngữ Văn |
| `ngoai_ngu` | float | ✅ | Điểm Ngoại Ngữ |
| `vat_ly` | float | ⚠️ | Điểm Vật Lý |
| `hoa_hoc` | float | ⚠️ | Điểm Hóa Học |
| `sinh_hoc` | float | ⚠️ | Điểm Sinh Học |
| `anomaly_score` | float | ✅ | Khoảng cách Euclidean tới centroid |
| `is_student_anomaly` | bool | ✅ | Luôn = True (chỉ export outliers) |
| `anomaly_pattern` | string | ⚠️ | VD: "Toán cao + Lý liệt" |

### Code export Spark (thêm vào cuối `05_export_results.py`)

```python
# ── Export Province Anomalies ──────────────────────────────────
df_province_anomalies \
    .write \
    .mode("overwrite") \
    .parquet("output/province_anomalies_parquet")

# ── Export Student Anomalies (chỉ outliers) ────────────────────
df_student_outliers \
    .filter("is_student_anomaly = true") \
    .write \
    .mode("overwrite") \
    .parquet("output/student_anomalies_parquet")

print("Export done!")
```

---

## 🔗 Cách ráp Output vào Dashboard

### Bước 1 — Copy 2 folder Parquet vào đúng chỗ

```
vnexam-anomoly-guard/
└── output/
    ├── province_anomalies_parquet/    ← copy folder này vào
    │   ├── part-00000-xxxx.parquet
    │   └── _SUCCESS
    └── student_anomalies_parquet/     ← copy folder này vào
        ├── part-00000-xxxx.parquet
        └── _SUCCESS
```

### Bước 2 — Kiểm tra data trước khi demo

```python
import pandas as pd

prov = pd.read_parquet("output/province_anomalies_parquet")
stud = pd.read_parquet("output/student_anomalies_parquet")

print(f"Provinces : {len(prov):,} rows | Flagged: {prov['is_province_anomaly'].sum()}")
print(f"Students  : {len(stud):,} rows")
print(f"Cols OK   : {{'nam_thi','ma_tinh','z_score','is_province_anomaly'}.issubset(prov.columns)}")
```

### Bước 3 — Chạy dashboard, refresh browser

```bash
cd demo
streamlit run web_app.py
```

Nếu thấy badge **"✓ Parquet Pipeline"** trên app bar → dashboard đang đọc data thật ✅
