#!/usr/bin/env python3
"""
Module: src/analytics.py
Thực thi các truy vấn Spark SQL để phân tích mô tả phổ điểm,
thống kê trung bình theo tỉnh thành và biến động các năm.
"""
import time

def run_spark_sql_analytics(spark, df):
    """
    Tạo TempView 'exam_data' và chạy các truy vấn thống kê mô tả.
    """
    print("\n========================================================")
    print("📈 [Step 03] PHÂN TÍCH THỐNG KÊ SPARK SQL")
    print("========================================================")
    start_time = time.time()
    
    # 1. Đăng ký TempView
    df.createOrReplaceTempView("exam_data")
    
    # Query 1: Điểm trung bình và độ lệch chuẩn các môn bắt buộc
    print("\n📌 1. Điểm trung bình các môn bắt buộc toàn quốc:")
    spark.sql("""
        SELECT 
            ROUND(AVG(toan), 2) AS avg_toan,
            ROUND(STDDEV(toan), 2) AS std_toan,
            ROUND(AVG(ngu_van), 2) AS avg_van,
            ROUND(STDDEV(ngu_van), 2) AS std_van,
            ROUND(AVG(ngoai_ngu), 2) AS avg_anh,
            ROUND(STDDEV(ngoai_ngu), 2) AS std_anh
        FROM exam_data
    """).show()
    
    # Query 2: Top 10 tỉnh có điểm môn Toán trung bình cao nhất (>= 5000 thí sinh)
    print("\n📌 2. Top 10 tỉnh/thành có điểm Toán trung bình cao nhất:")
    top_provinces = spark.sql("""
        SELECT 
            ma_tinh,
            COUNT(*) AS total_students,
            ROUND(AVG(toan), 2) AS avg_toan_score,
            ROUND(AVG(khoi_a00), 2) AS avg_a00_score
        FROM exam_data
        WHERE toan IS NOT NULL AND ma_tinh IS NOT NULL
        GROUP BY ma_tinh
        HAVING total_students >= 5000
        ORDER BY avg_toan_score DESC
        LIMIT 10
    """)
    top_provinces.show()

    # Query 3: Thống kê số thí sinh đạt điểm giỏi (>= 9.0) và điểm liệt (<= 1.0) môn Toán theo năm
    print("\n📌 3. Thống kê tỷ lệ điểm giỏi (>= 9.0) và điểm liệt (<= 1.0) môn Toán theo năm:")
    high_low_stats = spark.sql("""
        SELECT 
            nam_thi,
            COUNT(*) AS total_candidates,
            SUM(CASE WHEN toan >= 9.0 THEN 1 ELSE 0 END) AS high_score_count,
            ROUND(100.0 * SUM(CASE WHEN toan >= 9.0 THEN 1 ELSE 0 END) / COUNT(*), 2) AS high_score_pct,
            SUM(CASE WHEN toan <= 1.0 THEN 1 ELSE 0 END) AS fail_score_count,
            ROUND(100.0 * SUM(CASE WHEN toan <= 1.0 THEN 1 ELSE 0 END) / COUNT(*), 2) AS fail_score_pct
        FROM exam_data
        WHERE toan IS NOT NULL AND nam_thi IS NOT NULL
        GROUP BY nam_thi
        ORDER BY nam_thi ASC
    """)
    high_low_stats.show(15)

    # Query 4: Top 10 tỉnh có điểm trung bình khối A00 cao nhất
    print("\n📌 4. Top 10 tỉnh có điểm trung bình khối A00 cao nhất:")
    spark.sql("""
        SELECT 
            ma_tinh,
            COUNT(khoi_a00) AS total_a00_candidates,
            ROUND(AVG(khoi_a00), 2) AS avg_a00,
            ROUND(MAX(khoi_a00), 2) AS max_a00
        FROM exam_data
        WHERE khoi_a00 IS NOT NULL AND ma_tinh IS NOT NULL
        GROUP BY ma_tinh
        HAVING total_a00_candidates >= 1000
        ORDER BY avg_a00 DESC
        LIMIT 10
    """).show()

    elapsed = time.time() - start_time
    print(f"✅ Hoàn tất phân tích thống kê ({elapsed:.2f}s)")
    return top_provinces
