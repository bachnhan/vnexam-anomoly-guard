#!/usr/bin/env python3
"""
Wrapper Script: src/02_cleaning.py
Chạy trực tiếp module Cleaning & Transformation.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ingestion import create_spark_session, ingest_data
from src.cleaning import clean_and_transform

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_csv = os.path.join(base_dir, "data", "processed", "exam_scores_2016_2026.csv")
    
    spark = create_spark_session()
    raw_df = ingest_data(spark, target_csv)
    cleaned_df = clean_and_transform(raw_df)
    cleaned_df.select("sbd", "nam_thi", "toan", "ngu_van", "ngoai_ngu", "khoi_a00", "khoi_d01").show(5)
    spark.stop()
