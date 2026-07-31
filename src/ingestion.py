#!/usr/bin/env python3
"""
Module: src/ingestion.py
Khởi tạo SparkSession và đọc dữ liệu điểm thi từ file CSV.
"""
import os
import time
from pyspark.sql import SparkSession

def create_spark_session(master_url=None, app_name="VNExam-AnomalyGuard-Ingestion"):
    """
    Khởi tạo hoặc lấy SparkSession hiện tại với các thông số cấu hình cơ bản.
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
    Đọc file CSV điểm thi THPT vào Spark DataFrame.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu tại: {file_path}")
        
    print(f"🚀 [Step 01] Nạp dữ liệu từ file: {file_path}")
    start_time = time.time()
    
    df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv(file_path)
        
    elapsed = time.time() - start_time
    total_count = df.count()
    
    print(f"✅ Đọc dữ liệu thành công ({elapsed:.2f}s)")
    print(f"   - Số dòng: {total_count:,}")
    print(f"   - Số cột: {len(df.columns)}")
    print(f"   - Số partition: {df.rdd.getNumPartitions()}")
    
    return df
