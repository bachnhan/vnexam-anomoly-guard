#!/usr/bin/env python3
"""
Module: src/cleaning.py (Step 02 Cleaning & Transformation)
Làm sạch dữ liệu thi THPT, kiểm tra phạm vi điểm hợp lệ [0.0, 10.0],
ép kiểu dữ liệu chuẩn và tính toán điểm tổng các khối thi đại học (A00, A01, B00, C00, D01).
"""
import time
from pyspark.sql.functions import col, when, round as spark_round

def clean_and_transform(df):
    """
    Làm sạch dữ liệu và tạo cột tổng khối thi.
    """
    print("🧹 [Step 02] Bắt đầu làm sạch dữ liệu & chuẩn hóa kiểu dữ liệu 33 thuộc tính...")
    start_time = time.time()
    
    cleaned_df = df
    
    # 1. Map English column names to Vietnamese standard aliases if needed
    col_mapping = {
        'math': 'toan',
        'literature': 'ngu_van',
        'foreign_lang': 'ngoai_ngu',
        'physics': 'vat_ly',
        'chemistry': 'hoa_hoc',
        'biology': 'sinh_hoc',
        'history': 'lich_su',
        'geography': 'dia_ly',
        'civics': 'gdcd',
        'province_id': 'ma_tinh',
        'year': 'nam_thi'
    }
    
    for eng_col, vn_col in col_mapping.items():
        if eng_col in cleaned_df.columns and vn_col not in cleaned_df.columns:
            cleaned_df = cleaned_df.withColumn(vn_col, col(eng_col))
            
    # 2. Chuẩn hóa & Validate phạm vi điểm [0.0, 10.0] cho các môn thi
    score_cols = ["toan", "ngu_van", "ngoai_ngu", "vat_ly", "hoa_hoc", "sinh_hoc", "lich_su", "dia_ly", "gdcd"]
    for c in score_cols:
        if c in cleaned_df.columns:
            cleaned_df = cleaned_df.withColumn(
                c,
                when((col(c) >= 0.0) & (col(c) <= 10.0), col(c).cast("float")).otherwise(None)
            )
            
    # 3. Ép kiểu cột năm thi & mã tỉnh
    if "nam_thi" in cleaned_df.columns:
        cleaned_df = cleaned_df.withColumn("nam_thi", col("nam_thi").cast("integer"))
    if "ma_tinh" in cleaned_df.columns:
        cleaned_df = cleaned_df.withColumn("ma_tinh", col("ma_tinh").cast("string"))

    # 4. Tính toán điểm tổng các khối thi tuyển sinh Đại Học chính
    if set(["toan", "vat_ly", "hoa_hoc"]).issubset(cleaned_df.columns):
        cleaned_df = cleaned_df.withColumn(
            "khoi_a00",
            when(col("toan").isNotNull() & col("vat_ly").isNotNull() & col("hoa_hoc").isNotNull(),
                 spark_round(col("toan") + col("vat_ly") + col("hoa_hoc"), 2)
            ).otherwise(None)
        )
        
    if set(["toan", "vat_ly", "ngoai_ngu"]).issubset(cleaned_df.columns):
        cleaned_df = cleaned_df.withColumn(
            "khoi_a01",
            when(col("toan").isNotNull() & col("vat_ly").isNotNull() & col("ngoai_ngu").isNotNull(),
                 spark_round(col("toan") + col("vat_ly") + col("ngoai_ngu"), 2)
            ).otherwise(None)
        )

    if set(["toan", "hoa_hoc", "sinh_hoc"]).issubset(cleaned_df.columns):
        cleaned_df = cleaned_df.withColumn(
            "khoi_b00",
            when(col("toan").isNotNull() & col("hoa_hoc").isNotNull() & col("sinh_hoc").isNotNull(),
                 spark_round(col("toan") + col("hoa_hoc") + col("sinh_hoc"), 2)
            ).otherwise(None)
        )

    if set(["ngu_van", "lich_su", "dia_ly"]).issubset(cleaned_df.columns):
        cleaned_df = cleaned_df.withColumn(
            "khoi_c00",
            when(col("ngu_van").isNotNull() & col("lich_su").isNotNull() & col("dia_ly").isNotNull(),
                 spark_round(col("ngu_van") + col("lich_su") + col("dia_ly"), 2)
            ).otherwise(None)
        )

    if set(["toan", "ngu_van", "ngoai_ngu"]).issubset(cleaned_df.columns):
        cleaned_df = cleaned_df.withColumn(
            "khoi_d01",
            when(col("toan").isNotNull() & col("ngu_van").isNotNull() & col("ngoai_ngu").isNotNull(),
                 spark_round(col("toan") + col("ngu_van") + col("ngoai_ngu"), 2)
            ).otherwise(None)
        )

    elapsed = time.time() - start_time
    print(f"✅ Làm sạch và biến đổi dữ liệu thành công trong {elapsed:.2f} giây!")
    return cleaned_df
