#!/usr/bin/env python3
"""
Module: src/anomaly_ml.py (Step 04 Anomaly Detector Engine)
Khung 3 Phương Án Bất Thường Phân Tán Trên Apache Spark:
1. Cấp Thí Sinh: PySpark MLlib K-Means Student Outlier Detection (D > 3σ).
2. Cấp Tỉnh Thành: Multi-Subject & Multi-Block Z-Score Engine (Z > 3.0) cho 9 Môn & 5 Khối.
3. Cấp Chuỗi Thời Gian: Year-over-Year (YoY) Window Lag Delta Engine (ΔZ > 2.0) TÍNH RIÊNG THEO TỪNG MÔN VÀ KHỐI THI CỐ ĐỊNH.
"""
import math
import time
from pyspark.sql.functions import col, udf, avg, stddev, round as spark_round, when, greatest, lag, count, coalesce, lit
from pyspark.sql.window import Window
from pyspark.sql.types import DoubleType, FloatType
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans

def detect_student_level_anomalies(spark, df, k=4):
    """
    Phương án 1 (Cấp Thí sinh): PySpark MLlib K-Means Student Outlier (D > 3σ).
    """
    print("\n🤖 [Step 04 - Phương Án 1] Huấn luyện mô hình PySpark MLlib K-Means (Student Outliers)...")
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
    Phương án 2 & 3 (Cấp Tỉnh thành & Chuỗi thời gian):
    - Phương án 2: Multi-Subject & Multi-Block Z-Score Engine (Z > 3.0) cho 9 môn & 5 khối thi.
    - Phương án 3: YoY Window Lag Delta Engine (ΔZ > 2.0) TÍNH CHUẨN XÁC THEO TỪNG MÔN VÀ KHỐI THI CỐ ĐỊNH.
    """
    print("\n🏛️ [Step 04 - Phương Án 2 & 3] Thực thi Z-Score Engine & YoY Window Lag Delta (Chuẩn hóa theo từng môn/khối)...")
    start_time = time.time()
    
    df.createOrReplaceTempView("ml_exam_data")
    
    prov_stats = spark.sql("""
        SELECT 
            nam_thi,
            ma_tinh,
            COUNT(*) AS total_students,
            
            -- Tỷ lệ % điểm giỏi 9 môn thi (>= 9.0)
            (100.0 * SUM(CASE WHEN toan >= 9.0 THEN 1 ELSE 0 END) / COUNT(*)) AS high_math_pct,
            (100.0 * SUM(CASE WHEN ngu_van >= 9.0 THEN 1 ELSE 0 END) / COUNT(*)) AS high_van_pct,
            (100.0 * SUM(CASE WHEN ngoai_ngu >= 9.0 THEN 1 ELSE 0 END) / COUNT(*)) AS high_anh_pct,
            (100.0 * SUM(CASE WHEN vat_ly >= 9.0 THEN 1 ELSE 0 END) / COUNT(*)) AS high_ly_pct,
            (100.0 * SUM(CASE WHEN hoa_hoc >= 9.0 THEN 1 ELSE 0 END) / COUNT(*)) AS high_hoa_pct,
            (100.0 * SUM(CASE WHEN sinh_hoc >= 9.0 THEN 1 ELSE 0 END) / COUNT(*)) AS high_bio_pct,
            (100.0 * SUM(CASE WHEN lich_su >= 9.0 THEN 1 ELSE 0 END) / COUNT(*)) AS high_su_pct,
            (100.0 * SUM(CASE WHEN dia_ly >= 9.0 THEN 1 ELSE 0 END) / COUNT(*)) AS high_dia_pct,
            (100.0 * SUM(CASE WHEN gdcd >= 9.0 THEN 1 ELSE 0 END) / COUNT(*)) AS high_gdcd_pct,
            
            -- Tỷ lệ % điểm giỏi 5 Khối thi đại học chính (>= 27.0)
            (100.0 * SUM(CASE WHEN khoi_a00 >= 27.0 THEN 1 ELSE 0 END) / COUNT(*)) AS high_a00_pct,
            (100.0 * SUM(CASE WHEN khoi_a01 >= 27.0 THEN 1 ELSE 0 END) / COUNT(*)) AS high_a01_pct,
            (100.0 * SUM(CASE WHEN khoi_b00 >= 27.0 THEN 1 ELSE 0 END) / COUNT(*)) AS high_b00_pct,
            (100.0 * SUM(CASE WHEN khoi_c00 >= 27.0 THEN 1 ELSE 0 END) / COUNT(*)) AS high_c00_pct,
            (100.0 * SUM(CASE WHEN khoi_d01 >= 27.0 THEN 1 ELSE 0 END) / COUNT(*)) AS high_d01_pct
        FROM ml_exam_data
        WHERE ma_tinh IS NOT NULL AND nam_thi IS NOT NULL
        GROUP BY nam_thi, ma_tinh
        HAVING total_students >= 500
    """)
    
    yearly_stats = prov_stats.groupBy("nam_thi").agg(
        avg("high_math_pct").alias("avg_math_pct"), stddev("high_math_pct").alias("std_math_pct"),
        avg("high_van_pct").alias("avg_van_pct"), stddev("high_van_pct").alias("std_van_pct"),
        avg("high_anh_pct").alias("avg_anh_pct"), stddev("high_anh_pct").alias("std_anh_pct"),
        avg("high_ly_pct").alias("avg_ly_pct"), stddev("high_ly_pct").alias("std_ly_pct"),
        avg("high_hoa_pct").alias("avg_hoa_pct"), stddev("high_hoa_pct").alias("std_hoa_pct"),
        avg("high_bio_pct").alias("avg_bio_pct"), stddev("high_bio_pct").alias("std_bio_pct"),
        avg("high_su_pct").alias("avg_su_pct"), stddev("high_su_pct").alias("std_su_pct"),
        avg("high_dia_pct").alias("avg_dia_pct"), stddev("high_dia_pct").alias("std_dia_pct"),
        avg("high_gdcd_pct").alias("avg_gdcd_pct"), stddev("high_gdcd_pct").alias("std_gdcd_pct"),
        
        avg("high_a00_pct").alias("avg_a00_pct"), stddev("high_a00_pct").alias("std_a00_pct"),
        avg("high_a01_pct").alias("avg_a01_pct"), stddev("high_a01_pct").alias("std_a01_pct"),
        avg("high_b00_pct").alias("avg_b00_pct"), stddev("high_b00_pct").alias("std_b00_pct"),
        avg("high_c00_pct").alias("avg_c00_pct"), stddev("high_c00_pct").alias("std_c00_pct"),
        avg("high_d01_pct").alias("avg_d01_pct"), stddev("high_d01_pct").alias("std_d01_pct")
    )
    
    joined_df = prov_stats.join(yearly_stats, on="nam_thi", how="inner")
    
    def calc_z(pct_col, avg_col, std_col):
        return coalesce(
            when((col(std_col) > 0) & col(pct_col).isNotNull() & col(avg_col).isNotNull(),
                 spark_round((col(pct_col) - col(avg_col)) / col(std_col), 2)
            ).otherwise(0.0),
            lit(0.0)
        )

    # Phương án 2: Tính toán Z-Score cho 9 Môn & 5 Khối Thi
    zscore_df = joined_df \
        .withColumn("z_math", calc_z("high_math_pct", "avg_math_pct", "std_math_pct")) \
        .withColumn("z_van", calc_z("high_van_pct", "avg_van_pct", "std_van_pct")) \
        .withColumn("z_anh", calc_z("high_anh_pct", "avg_anh_pct", "std_anh_pct")) \
        .withColumn("z_ly", calc_z("high_ly_pct", "avg_ly_pct", "std_ly_pct")) \
        .withColumn("z_hoa", calc_z("high_hoa_pct", "avg_hoa_pct", "std_hoa_pct")) \
        .withColumn("z_bio", calc_z("high_bio_pct", "avg_bio_pct", "std_bio_pct")) \
        .withColumn("z_su", calc_z("high_su_pct", "avg_su_pct", "std_su_pct")) \
        .withColumn("z_dia", calc_z("high_dia_pct", "avg_dia_pct", "std_dia_pct")) \
        .withColumn("z_gdcd", calc_z("high_gdcd_pct", "avg_gdcd_pct", "std_gdcd_pct")) \
        .withColumn("z_a00", calc_z("high_a00_pct", "avg_a00_pct", "std_a00_pct")) \
        .withColumn("z_a01", calc_z("high_a01_pct", "avg_a01_pct", "std_a01_pct")) \
        .withColumn("z_b00", calc_z("high_b00_pct", "avg_b00_pct", "std_b00_pct")) \
        .withColumn("z_c00", calc_z("high_c00_pct", "avg_c00_pct", "std_c00_pct")) \
        .withColumn("z_d01", calc_z("high_d01_pct", "avg_d01_pct", "std_d01_pct")) \
        .withColumn("z_score", greatest(
            col("z_math"), col("z_van"), col("z_anh"), col("z_ly"), col("z_hoa"), col("z_bio"),
            col("z_su"), col("z_dia"), col("z_gdcd"), col("z_a00"), col("z_a01"), col("z_b00"),
            col("z_c00"), col("z_d01")
        ))

    # Phương án 3: YoY Window Lag Delta Function (TÍNH CHUẨN XÁC THEO TỪNG MÔN VÀ KHỐI THI CỐ ĐỊNH)
    windowSpec = Window.partitionBy("ma_tinh").orderBy("nam_thi")
    
    all_z_cols = ['z_math', 'z_van', 'z_anh', 'z_ly', 'z_hoa', 'z_bio', 'z_su', 'z_dia', 'z_gdcd', 'z_a00', 'z_a01', 'z_b00', 'z_c00', 'z_d01']
    
    yoy_df = zscore_df
    for z_c in all_z_cols:
        yoy_col = f"yoy_{z_c}"
        prev_col = f"prev_{z_c}"
        yoy_df = yoy_df \
            .withColumn(prev_col, lag(z_c, 1).over(windowSpec)) \
            .withColumn(yoy_col, when(col(prev_col).isNotNull(), spark_round(col(z_c) - col(prev_col), 2)).otherwise(lit(None)))

    # Tính yoy_z_delta = LẤY MAX MỨC TĂNG VỌT CHÊNH LỆCH CỦA CÙNG MÔN/KHỐI ĐÓ SO VỚI NĂM TRƯỚC
    yoy_z_cols = [col(f"yoy_{z_c}") for z_c in all_z_cols]
    
    yoy_df = yoy_df \
        .withColumn("prev_year_math_pct", lag("high_math_pct", 1).over(windowSpec)) \
        .withColumn("yoy_math_delta_pct", when(col("prev_year_math_pct").isNotNull(), spark_round(col("high_math_pct") - col("prev_year_math_pct"), 2)).otherwise(lit(None))) \
        .withColumn("yoy_z_delta", greatest(*yoy_z_cols)) \
        .withColumn("is_yoy_spike", when(col("yoy_z_delta") >= 2.0, True).otherwise(False)) \
        .withColumn("is_province_anomaly", (col("z_score") >= 3.0) | col("is_yoy_spike"))

    print("\n🚨 Top Các Tỉnh/Thành Cảnh Báo Bất Thường (Khung 3 Phương Án Spark Engine - YoY Chuẩn Hóa Theo Môn/Khối):")
    flagged_provinces = yoy_df.filter(col("is_province_anomaly") == True).orderBy(col("z_score").desc())
    flagged_provinces.select(
        "nam_thi", "ma_tinh", "total_students", "z_math", "z_van", "z_anh", "z_ly", "z_hoa", "z_bio", "z_a00", "z_b00", "z_c00", "z_d01", "z_score", "yoy_z_delta"
    ).show(25, truncate=False)
    
    elapsed = time.time() - start_time
    print(f"✅ Hoàn tất Anomaly Detector Engine trong {elapsed:.2f} giây!")
    return yoy_df
