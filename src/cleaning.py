#!/usr/bin/env python3
"""
Module: src/cleaning.py
Tiền xử lý dữ liệu: làm sạch, kiểm tra miền giá trị điểm [0, 10], 
chuẩn hóa kiểu dữ liệu và tính tổng điểm các khối thi (A00, A01, B00, C00, D01).
"""
import time
from pyspark.sql.functions import col, when, round as spark_round

def clean_and_transform(df):
    """
    Hàm làm sạch và biến đổi dữ liệu điểm thi.
    """
    print("🧹 [Step 02] Tiến hành làm sạch và chuẩn hóa dữ liệu...")
    start_time = time.time()
    
    raw_count = df.count()
    print(f"📊 [Log] Số dòng trước xử lý: {raw_count:,}")
    
    cleaned_df = df
    
    # 1. Đổi tên cột từ tiếng Anh sang tiếng Việt nếu cần
    print("   🔹 [Step 02.1] Chuẩn hóa tên cột Anh -> Việt...")
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
    print("      -> Hoàn tất đổi tên cột.")
            
    # 2. Kiểm tra miền giá trị [0.0, 10.0] cho các môn thi
    print("   🔹 [Step 02.2] Kiểm tra miền giá trị điểm [0, 10] và ép kiểu Float...")
    score_cols = ["toan", "ngu_van", "ngoai_ngu", "vat_ly", "hoa_hoc", "sinh_hoc", "lich_su", "dia_ly", "gdcd"]
    for c in score_cols:
        if c in cleaned_df.columns:
            cleaned_df = cleaned_df.withColumn(
                c,
                when((col(c) >= 0.0) & (col(c) <= 10.0), col(c).cast("float")).otherwise(None)
            )
    print("      -> Hoàn tất lọc điểm hợp lệ.")
            
    # 3. Chuẩn hóa kiểu dữ liệu cho năm thi và mã tỉnh
    print("   🔹 [Step 02.3] Chuẩn hóa kiểu dữ liệu cho năm thi và mã tỉnh...")
    if "nam_thi" in cleaned_df.columns:
        cleaned_df = cleaned_df.withColumn("nam_thi", col("nam_thi").cast("integer"))
    if "ma_tinh" in cleaned_df.columns:
        cleaned_df = cleaned_df.withColumn("ma_tinh", col("ma_tinh").cast("string"))
    print("      -> Hoàn tất ép kiểu định danh.")

    # 4. Tính điểm tổng cho các tổ hợp khối thi chính
    print("   🔹 [Step 02.4] Tính điểm tổng các tổ hợp khối thi (A00, A01, B00, C00, D01)...")
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
    print("      -> Hoàn tất tạo các cột khối thi.")

    cleaned_count = cleaned_df.count()
    elapsed = time.time() - start_time
    print(f"📊 [Log] Số dòng sau xử lý: {cleaned_count:,}")
    print(f"✅ Làm sạch dữ liệu hoàn tất ({elapsed:.2f}s)")
    return cleaned_df
