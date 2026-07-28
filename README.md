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
├── demo/
│   └── app_demo.py                          # Live Demo App cho buổi bảo vệ thuyết trình 15 phút
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

### 4. Khởi chạy Live Demo App
```bash
python3 demo/app_demo.py
```
