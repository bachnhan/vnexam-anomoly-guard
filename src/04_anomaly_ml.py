#!/usr/bin/env python3
"""
Wrapper Script: src/04_anomaly_ml.py
Chạy trực tiếp module PySpark MLlib & Z-Score Anomaly Detector Engine.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ingestion import create_spark_session, ingest_data
from src.cleaning import clean_and_transform
from src.anomaly_ml import detect_student_level_anomalies, detect_province_level_anomalies

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_csv = os.path.join(base_dir, "data", "processed", "exam_scores_2016_2026.csv")
    
    spark = create_spark_session()
    raw_df = ingest_data(spark, target_csv)
    cleaned_df = clean_and_transform(raw_df)
    student_anomalies, _ = detect_student_level_anomalies(spark, cleaned_df)
    province_anomalies = detect_province_level_anomalies(spark, cleaned_df)
    spark.stop()
