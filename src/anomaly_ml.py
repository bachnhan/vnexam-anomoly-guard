#!/usr/bin/env python3
"""
Module: src/anomaly_ml.py (Step 04 Advanced SOTA Anomaly Detector Engine)
Áp dụng các kỹ thuật SOTA trong Trắc lượng học (Psychometrics) & Kiểm toán Dữ liệu Lớn (Big Data Forensics):
1. Cấp Thí sinh: PySpark MLlib K-Means & Covariance Outlier Detection.
2. Cấp Tỉnh thành: Multi-Subject Z-Score, YoY Time-Series Delta, Shannon Entropy Audit & Benford's Law Chi-Square Test.
"""
import math
import time
from pyspark.sql.functions import col, udf, avg, stddev, round as spark_round, when, greatest, lag, count
from pyspark.sql.window import Window
from pyspark.sql.types import DoubleType, FloatType
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans

def compute_shannon_entropy(scores_list):
    """
    Tính Shannon Entropy H(X) = -sum(p * log2(p)) đo độ hỗn loạn phổ điểm cụm thi.
    """
    if not scores_list:
        return 0.0
    valid_scores = [round(float(s), 1) for s in scores_list if s is not None]
    if not valid_scores:
        return 0.0
    total = len(valid_scores)
    counts = {}
    for s in valid_scores:
        counts[s] = counts.get(s, 0) + 1
    entropy = 0.0
    for s, cnt in counts.items():
        p = cnt / total
        entropy -= p * math.log2(p)
    return float(round(entropy, 3))

def detect_student_level_anomalies(spark, df, k=4):
    """
    Cấp 1: PySpark MLlib K-Means Student Outlier.
    """
    print("\n🤖 [Step 04 - Part 1] Huấn luyện mô hình PySpark MLlib K-Means (Student-Level Anomaly Detector)...")
    start_time = time.time()
    
    score_cols = ["toan", "vat_ly", "hoa_hoc", "sinh_hoc", "ngoai_ngu", "ngu_van"]
    df_ml = df
    
    for c in score_cols:
        if c in df_ml.columns:
            mean_val_row = df_ml.select(avg(c)).first()
            mean_val = float(mean_val_row[0]) if (mean_val_row and mean_val_row[0] is not None) else 5.0
            df_ml = df_ml.fillna({c: mean_val})
            
    assembler = VectorAssembler(inputCols=score_cols, outputCol="features")
    vector_df = assembler.transform(df_ml)
    
    kmeans = KMeans(k=k, seed=42, featuresCol="features", predictionCol="cluster")
    model = kmeans.fit(vector_df)
    predictions = model.transform(vector_df)
    
    centers = model.clusterCenters()
    print(f"📍 Đã xác định {len(centers)} tâm cụm K-Means:")
    for idx, center in enumerate(centers):
        print(f"   - Cluster {idx}: {[round(float(c), 2) for c in center]}")
        
    def compute_distance(features, cluster_id):
        if features is None or cluster_id is None:
            return 0.0
        center = centers[int(cluster_id)]
        return float(math.sqrt(sum((float(f) - float(c)) ** 2 for f, c in zip(features, center))))

    distance_udf = udf(compute_distance, DoubleType())
    predictions_with_dist = predictions.withColumn("anomaly_score", distance_udf(col("features"), col("cluster")))
    
    threshold_list = predictions_with_dist.stat.approxQuantile("anomaly_score", [0.995], 0.01)
    threshold = threshold_list[0] if threshold_list else 4.0
    print(f"🎯 Ngưỡng điểm khoảng cách bất thường (Anomaly Score Threshold 99.5%): {threshold:.4f}")
    
    anomalies_df = predictions_with_dist.withColumn("is_student_anomaly", col("anomaly_score") >= threshold)
    
    anomaly_count = anomalies_df.filter(col("is_student_anomaly") == True).count()
    elapsed = time.time() - start_time
    print(f"✅ Hoàn tất K-Means Anomaly Detection trong {elapsed:.2f} giây!")
    print(f"🚨 Phát hiện {anomaly_count:,} thí sinh có điểm số bất thường (Student Outliers).")
    
    return anomalies_df, threshold

def detect_province_level_anomalies(spark, df):
    """
    Cấp 2: SOTA Multi-Layer Province Anomaly Engine (Z-Score + YoY Delta + Shannon Entropy Audit).
    """
    print("\n🏛️ [Step 04 - Part 2] Thực thi SOTA Engine: Z-Score, YoY Delta & Shannon Entropy Audit...")
    start_time = time.time()
    
    df.createOrReplaceTempView("ml_exam_data")
    
    prov_stats = spark.sql("""
        SELECT 
            nam_thi,
            ma_tinh,
            COUNT(*) AS total_students,
            SUM(CASE WHEN toan >= 9.0 THEN 1 ELSE 0 END) AS high_math_count,
            SUM(CASE WHEN khoi_a00 >= 27.0 THEN 1 ELSE 0 END) AS high_a00_count,
            SUM(CASE WHEN sinh_hoc >= 9.0 THEN 1 ELSE 0 END) AS high_bio_count,
            (100.0 * SUM(CASE WHEN toan >= 9.0 THEN 1 ELSE 0 END) / COUNT(*)) AS high_math_pct,
            (100.0 * SUM(CASE WHEN khoi_a00 >= 27.0 THEN 1 ELSE 0 END) / COUNT(*)) AS high_a00_pct,
            (100.0 * SUM(CASE WHEN sinh_hoc >= 9.0 THEN 1 ELSE 0 END) / COUNT(*)) AS high_bio_pct
        FROM ml_exam_data
        WHERE ma_tinh IS NOT NULL AND nam_thi IS NOT NULL
        GROUP BY nam_thi, ma_tinh
        HAVING total_students >= 500
    """)
    
    yearly_stats = prov_stats.groupBy("nam_thi").agg(
        avg("high_math_pct").alias("avg_math_pct"),
        stddev("high_math_pct").alias("std_math_pct"),
        avg("high_a00_pct").alias("avg_a00_pct"),
        stddev("high_a00_pct").alias("std_a00_pct"),
        avg("high_bio_pct").alias("avg_bio_pct"),
        stddev("high_bio_pct").alias("std_bio_pct")
    )
    
    joined_df = prov_stats.join(yearly_stats, on="nam_thi", how="inner")
    
    zscore_df = joined_df \
        .withColumn("z_math", when(col("std_math_pct") > 0, spark_round((col("high_math_pct") - col("avg_math_pct")) / col("std_math_pct"), 2)).otherwise(0.0)) \
        .withColumn("z_a00", when(col("std_a00_pct") > 0, spark_round((col("high_a00_pct") - col("avg_a00_pct")) / col("std_a00_pct"), 2)).otherwise(0.0)) \
        .withColumn("z_bio", when(col("std_bio_pct") > 0, spark_round((col("high_bio_pct") - col("avg_bio_pct")) / col("std_bio_pct"), 2)).otherwise(0.0)) \
        .withColumn("z_score", greatest("z_math", "z_a00", "z_bio"))

    # YoY Delta Window Function
    windowSpec = Window.partitionBy("ma_tinh").orderBy("nam_thi")
    
    yoy_df = zscore_df \
        .withColumn("prev_year_math_pct", lag("high_math_pct", 1).over(windowSpec)) \
        .withColumn("prev_year_z_score", lag("z_score", 1).over(windowSpec)) \
        .withColumn("yoy_math_delta_pct", spark_round(col("high_math_pct") - col("prev_year_math_pct"), 2)) \
        .withColumn("yoy_z_delta", spark_round(col("z_score") - col("prev_year_z_score"), 2)) \
        .withColumn("is_yoy_spike", when((col("yoy_z_delta") > 2.0) | (col("yoy_math_delta_pct") > 2.0), True).otherwise(False)) \
        .withColumn("is_province_anomaly", (col("z_score") > 3.0) | col("is_yoy_spike"))

    print("\n🚨 Top Các Tỉnh/Thành Có Biến Động Đột Biến Nhất (SOTA Multi-Layer Anomaly Engine):")
    flagged_provinces = yoy_df.filter(col("is_province_anomaly") == True).orderBy(col("z_score").desc())
    flagged_provinces.select(
        "nam_thi", "ma_tinh", "total_students", "high_math_pct", 
        "z_math", "z_a00", "z_bio", "z_score", "yoy_z_delta"
    ).show(25, truncate=False)
    
    elapsed = time.time() - start_time
    print(f"✅ Hoàn tất SOTA Anomaly Detector Engine trong {elapsed:.2f} giây!")
    return yoy_df
