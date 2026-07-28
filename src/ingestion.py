#!/usr/bin/env python3
"""
Module: src/ingestion.py (Step 01 Ingestion)
Nạp tập dữ liệu 1.01GB (10.86 triệu bản ghi) vào PySpark DataFrame với cấu hình bộ nhớ tối ưu.
"""
import os
import time
from pyspark.sql import SparkSession

def create_spark_session(master_url=None, app_name="VNExam-AnomalyGuard-01-Ingestion"):
    """
    Khởi tạo hoặc kết nối SparkSession với các cấu hình tối ưu bộ nhớ.
    """
    builder = SparkSession.builder \
        .appName(app_name) \
        .config("spark.driver.memory", "4g") \
        .config("spark.executor.memory", "4g") \
        .config("spark.sql.shuffle.partitions", "200") \
        .config("spark.sql.execution.arrow.pyspark.enabled", "true")
    
    if master_url:
        builder = builder.master(master_url)
    else:
        builder = builder.master("local[*]")
        
    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark

def ingest_data(spark, file_path):
    """
    Nạp dữ liệu từ file CSV 1.01GB vào PySpark DataFrame.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ Không tìm thấy tệp dữ liệu tại path: {file_path}")
        
    print(f"🚀 [Step 01] Bắt đầu nạp tập dữ liệu Big Data: {file_path}")
    start_time = time.time()
    
    df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv(file_path)
        
    elapsed = time.time() - start_time
    total_count = df.count()
    
    print(f"✅ Nạp dữ liệu hoàn tất trong {elapsed:.2f} giây!")
    print(f"📊 Tổng số bản ghi (rows): {total_count:,}")
    print(f"📐 Số lượng cột (columns): {len(df.columns)}")
    print(f"🧩 Số lượng partitions: {df.rdd.getNumPartitions()}")
    
    return df
