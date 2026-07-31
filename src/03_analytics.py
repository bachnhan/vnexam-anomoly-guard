#!/usr/bin/env python3
"""
Script: src/03_analytics.py
Thực hiện tiền xử lý dữ liệu và chạy Analytics.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyspark.sql.functions import col, when, avg, round as spark_round
from pyspark.sql.window import Window

from src.ingestion import create_spark_session, ingest_data
from src.analytics import run_spark_sql_analytics

def preprocess_data(df):
    """
    Tiền xử lý dữ liệu:
    - Ép kiểu điểm sang Float
    - Lọc điểm trong khoảng [0, 10]
    - Điền giá trị missing bằng trung bình của môn thi trong cùng năm
    - Tính điểm khối thi nếu đủ 3 môn
    """
    print("🧹 Bắt đầu tiền xử lý dữ liệu...")
    
    # 1. Chuẩn hóa tên cột nếu có tiếng Anh
    col_mapping = {
        'math': 'toan', 'literature': 'ngu_van', 'foreign_lang': 'ngoai_ngu',
        'physics': 'vat_ly', 'chemistry': 'hoa_hoc', 'biology': 'sinh_hoc',
        'history': 'lich_su', 'geography': 'dia_ly', 'civics': 'gdcd',
        'year': 'nam_thi'
    }
    for eng, vn in col_mapping.items():
        if eng in df.columns and vn not in df.columns:
            df = df.withColumn(vn, col(eng))
            
    score_cols = ["toan", "ngu_van", "ngoai_ngu", "vat_ly", "hoa_hoc", "sinh_hoc", "lich_su", "dia_ly", "gdcd"]
    available_scores = [c for c in score_cols if c in df.columns]
    
    # 2. Ép kiểu sang Float và lấy điểm trong khoảng 0-10
    for c in available_scores:
        # Ép sang float trước
        df = df.withColumn(c, col(c).cast("float"))
        # Lọc trong khoảng 0 - 10, ngoài khoảng thì gán Null
        df = df.withColumn(c, when((col(c) >= 0.0) & (col(c) <= 10.0), col(c)).otherwise(None))
        
    # 3. Tính điểm trung bình của môn học theo từng năm và điền khuyết (Imputation)
    if "nam_thi" in df.columns:
        window_spec = Window.partitionBy("nam_thi")
        for c in available_scores:
            mean_col = avg(col(c)).over(window_spec)
            df = df.withColumn(c, when(col(c).isNull(), mean_col).otherwise(col(c)))
            
    # 4. Tính điểm theo khối thi (chỉ khi có điểm của 3 môn)
    if set(["toan", "vat_ly", "hoa_hoc"]).issubset(df.columns):
        df = df.withColumn("khoi_a00", spark_round(col("toan") + col("vat_ly") + col("hoa_hoc"), 2))
        
    if set(["toan", "vat_ly", "ngoai_ngu"]).issubset(df.columns):
        df = df.withColumn("khoi_a01", spark_round(col("toan") + col("vat_ly") + col("ngoai_ngu"), 2))

    if set(["toan", "hoa_hoc", "sinh_hoc"]).issubset(df.columns):
        df = df.withColumn("khoi_b00", spark_round(col("toan") + col("hoa_hoc") + col("sinh_hoc"), 2))
        
    if set(["ngu_van", "lich_su", "dia_ly"]).issubset(df.columns):
        df = df.withColumn("khoi_c00", spark_round(col("ngu_van") + col("lich_su") + col("dia_ly"), 2))
        
    if set(["toan", "ngu_van", "ngoai_ngu"]).issubset(df.columns):
        df = df.withColumn("khoi_d01", spark_round(col("toan") + col("ngu_van") + col("ngoai_ngu"), 2))

    print("✅ Đã xử lý xong!")
    return df

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_csv = os.path.join(base_dir, "data", "processed", "exam_scores_2016_2026.csv")
    
    # Nếu file chưa xử lý nằm ngoài processed:
    if not os.path.exists(target_csv):
        target_csv = os.path.join(base_dir, "data", "exam_scores_2016_2026.csv")
    
    spark = create_spark_session()
    
    try:
        raw_df = ingest_data(spark, target_csv)
        
        # Gọi hàm preprocess vừa viết thay vì clean_and_transform mặc định
        processed_df = preprocess_data(raw_df)
        
        # Chạy analytics
        run_spark_sql_analytics(spark, processed_df)
    except Exception as e:
        print(f"❌ Lỗi: {e}")
    finally:
        spark.stop()
