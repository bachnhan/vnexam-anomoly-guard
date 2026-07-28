#!/usr/bin/env python3
"""
VNExam-AnomalyGuard Main Orchestrator Script
Entrypoint điều phối toàn bộ PySpark Data Pipeline từ Input (CSV 1.01GB) đến Output (Parquet & Anomaly Reports).

Cách dùng:
    python3 main.py --mode local
    python3 main.py --mode cluster --master spark://localhost:7077
"""
import os
import sys
import argparse
import time

# Thêm thư mục hiện tại vào sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ingestion import create_spark_session, ingest_data
from src.cleaning import clean_and_transform
from src.analytics import run_spark_sql_analytics
from src.anomaly_ml import detect_student_level_anomalies, detect_province_level_anomalies
from src.export_results import export_results

def main():
    parser = argparse.ArgumentParser(description="VNExam-AnomalyGuard PySpark Main Pipeline")
    parser.add_argument("--mode", choices=["local", "cluster"], default="local", help="Chế độ thực thi (local / cluster)")
    parser.add_argument("--master", type=str, default=None, help="Spark Master URL (VD: spark://spark-master:7077)")
    parser.add_argument("--input", type=str, default=None, help="Đường dẫn file CSV dữ liệu thi")
    parser.add_argument("--output", type=str, default="output", help="Thư mục đầu ra kết quả Parquet")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    if args.input:
        input_csv = args.input
    else:
        input_csv = os.path.join(base_dir, "data", "processed", "exam_scores_2016_2026.csv")
        if not os.path.exists(input_csv):
            input_csv = os.path.join(base_dir, "data", "exam_scores_2016_2026.csv")

    print("\n==========================================================================")
    print("🚀 BẮT ĐẦU THỰC THI PIPELINE VNEXAM-ANOMALYGUARD (APACHE SPARK PIPELINE)")
    print("==========================================================================")
    print(f"📌 Chế độ thực thi (Execution Mode): {args.mode}")
    print(f"📌 Tập dữ liệu đầu vào (Input CSV): {input_csv}")
    print(f"📌 Thư mục xuất kết quả (Output Dir): {args.output}")
    print("==========================================================================")
    
    overall_start = time.time()
    
    master_url = args.master if args.master else ("local[*]" if args.mode == "local" else "spark://spark-master:7077")
    spark = create_spark_session(master_url=master_url, app_name="VNExam-AnomalyGuard-Full-Pipeline")
    
    try:
        # Step 01: Ingestion
        raw_df = ingest_data(spark, input_csv)
        
        # Step 02: Cleaning & Transformation
        cleaned_df = clean_and_transform(raw_df)
        
        # Step 03: Spark SQL Analytics
        run_spark_sql_analytics(spark, cleaned_df)
        
        # Step 04: Anomaly Detection (Student Level & Province Level)
        student_anomalies, threshold = detect_student_level_anomalies(spark, cleaned_df)
        province_anomalies = detect_province_level_anomalies(spark, cleaned_df)
        
        # Step 05: Export Results to Parquet
        export_results(student_anomalies, province_anomalies, output_dir=args.output)
        
        total_time = time.time() - overall_start
        print("\n==========================================================================")
        print(f"🎉 TỔNG KẾT PIPELINE THÀNH CÔNG RỰC RỠ TRONG {total_time:.2f} GIÂY ({total_time/60:.2f} PHÚT)!")
        print("==========================================================================\n")
        
    except Exception as e:
        print(f"\n❌ LỖI TRONG QUÁ TRÌNH THỰC THI PIPELINE: {e}")
        import traceback
        traceback.print_exc()
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
