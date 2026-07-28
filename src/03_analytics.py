#!/usr/bin/env python3
"""
Wrapper Script: src/03_analytics.py
Chạy trực tiếp module Spark SQL Analytics.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ingestion import create_spark_session, ingest_data
from src.cleaning import clean_and_transform
from src.analytics import run_spark_sql_analytics

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_csv = os.path.join(base_dir, "data", "processed", "exam_scores_2016_2026.csv")
    
    spark = create_spark_session()
    raw_df = ingest_data(spark, target_csv)
    cleaned_df = clean_and_transform(raw_df)
    run_spark_sql_analytics(spark, cleaned_df)
    spark.stop()
