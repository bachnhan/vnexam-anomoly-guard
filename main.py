#!/usr/bin/env python3
"""
VNExam-AnomalyGuard Main Pipeline Script
Script điều phối các bước nạp, xử lý dữ liệu và phát hiện bất thường bằng PySpark.

Cách dùng:
    python3 main.py --mode local
    python3 main.py --mode cluster --master spark://localhost:7077
"""
import os
import sys
import argparse
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ingestion import create_spark_session, ingest_data
from src.cleaning import clean_and_transform
from src.analytics import run_spark_sql_analytics
from src.anomaly_ml import detect_student_level_anomalies, detect_province_level_anomalies
from src.export_results import export_results

def main():
    parser = argparse.ArgumentParser(description="VNExam-AnomalyGuard Spark Pipeline")
    parser.add_argument("--mode", choices=["local", "cluster"], default="local", help="Chế độ chạy (local / cluster)")
    parser.add_argument("--master", type=str, default=None, help="Spark Master URL (ví dụ: spark://spark-master:7077)")
    parser.add_argument("--input", type=str, default=None, help="Đường dẫn file CSV dữ liệu đầu vào")
    parser.add_argument("--output", type=str, default="output", help="Thư mục xuất kết quả")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    if args.input:
        input_csv = args.input
    else:
        input_csv = os.path.join(base_dir, "data", "processed", "exam_scores_2016_2026.csv")
        if not os.path.exists(input_csv):
            from scripts.download_dataset import ensure_dataset
            input_csv = ensure_dataset(input_csv)

    print("\n==========================================================================")
    print("🚀 CHẠY PIPELINE VNEXAM-ANOMALYGUARD (SPARK PIPELINE)")
    print("==========================================================================")
    print(f"📌 Chế độ chạy: {args.mode}")
    print(f"📌 File dữ liệu đầu vào: {input_csv}")
    print(f"📌 Thư mục xuất kết quả: {args.output}")
    print("==========================================================================")
    
    overall_start = time.time()
    
    master_url = args.master if args.master else ("local[*]" if args.mode == "local" else "spark://spark-master:7077")
    spark = create_spark_session(master_url=master_url, app_name="VNExam-AnomalyGuard-Full-Pipeline")
    
    try:
        # Bước 1: Nạp dữ liệu
        raw_df = ingest_data(spark, input_csv)
        
        # Bước 2: Làm sạch và biến đổi dữ liệu
        cleaned_df = clean_and_transform(raw_df)
        
        # Bước 3: Phân tích thống kê bằng Spark SQL
        run_spark_sql_analytics(spark, cleaned_df)
        
        # Bước 4: Phát hiện bất thường cấp Thí sinh và Tỉnh thành
        student_anomalies = detect_student_level_anomalies(spark, cleaned_df)
        province_anomalies = detect_province_level_anomalies(spark, cleaned_df)
        
        # Bước 5: Xuất kết quả ra Parquet, CSV và JSON
        export_results(student_anomalies, province_anomalies, output_dir=args.output)
        
        total_time = time.time() - overall_start
        print("\n==========================================================================")
        print(f"✅ Hoàn tất pipeline trong {total_time:.2f} giây ({total_time/60:.2f} phút).")
        print("==========================================================================\n")
        
    except Exception as e:
        print(f"\n❌ Có lỗi xảy ra trong quá trình thực thi: {e}")
        import traceback
        traceback.print_exc()
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
