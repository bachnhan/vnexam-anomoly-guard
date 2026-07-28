#!/usr/bin/env python3
"""
Wrapper Script: src/01_ingestion.py
Chạy trực tiếp module Ingestion.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ingestion import create_spark_session, ingest_data

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_csv = os.path.join(base_dir, "data", "processed", "exam_scores_2016_2026.csv")
    if not os.path.exists(target_csv):
        target_csv = os.path.join(base_dir, "data", "exam_scores_2016_2026.csv")
        
    spark = create_spark_session()
    df = ingest_data(spark, target_csv)
    df.show(5)
    spark.stop()
