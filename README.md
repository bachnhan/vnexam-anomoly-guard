# VNExam-AnomalyGuard

> **Hệ Thống Phân Tích Phổ Điểm & Phát Hiện Gian Lận Điểm Thi THPT Quốc Gia (2016–2026) Trên Nền Tảng Apache Spark**  
> *Bài tập nhóm cuối kỳ môn Big Data Processing (BDA501)*

---

## 📊 Tập Dữ Liệu Kaggle (Dataset)

- **Kaggle Dataset Link:** [Vietnam National Examination Scores 2016–2026 (Kaggle)](https://www.kaggle.com/datasets/bchnhnnguynhunh/viet-name-national-exam-scores-2016-2026)
- **Quy mô tập dữ liệu:** **1.01 GB** (10,865,001 bản ghi / 33 thuộc tính).
- **Phạm vi dữ liệu:** Dữ liệu điểm thi THPT Quốc Gia Việt Nam liên tục trong **10 mùa thi (2016 – 2026)**.

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
│   └── etl_process.py                       # Script ETL tiền xử lý gộp các file dữ liệu thi 2016-2026
├── src/                                     # Mã nguồn PySpark Pipeline chuẩn hóa
│   ├── __init__.py
│   ├── ingestion.py                         # Step 01: Nạp dữ liệu 1.01GB với SparkSession tối ưu RAM
│   ├── cleaning.py                          # Step 02: Làm sạch, validate [0, 10] & tính điểm khối thi
│   ├── analytics.py                         # Step 03: Spark SQL Analytics phổ điểm & Tỉnh/Thành
│   ├── anomaly_ml.py                        # Step 04: MLlib K-Means, Multi-Subject Z-Score & YoY Delta
│   ├── export_results.py                    # Step 05: Xuất kết quả nén Parquet phân vùng theo năm
│   └── sota_audit.py                        # SOTA Forensic Audit (Benford Law, Mahalanobis & Entropy)
├── demo/                                    # Dashboard trực quan hoá kết quả (Streamlit & HTML5)
│   ├── web_app.py                           # Streamlit Web Application Dashboard (Port 8501)
│   ├── index.html                           # Executive HTML5/Tailwind Web Dashboard (Port 8080)
│   ├── export_web_data.py                   # Export JSON dataset cho Web Dashboard
│   ├── dashboard_data.json                  # Metadata: KPI, ground_truth, SOTA results
│   ├── styles/                              # CSS Styling
│   ├── components/                          # UI Components
│   └── views/                               # Modular Dashboard Pages
└── docs/
    ├── VNExam-AnomalyGuard-MASTER-ALL-IN-ONE.md # Tài liệu Master ALL-IN-ONE tổng hợp dự án
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

### 3. Khởi chạy Web Dashboard
```bash
# Web Dashboard HTML5/Tailwind (Port 8080)
python3 -m http.server 8080 --directory demo

# Hoặc Streamlit Dashboard (Port 8501)
streamlit run demo/web_app.py
```
