#!/usr/bin/env python3
"""
Module: src/export_results.py (Step 05 Export Results)
Xuất kết quả phân tích phổ điểm và danh sách bất thường ra định dạng lưu trữ cột nén Parquet,
phân vùng theo năm (partitionBy("nam_thi")) để tối ưu hóa hiệu năng truy vấn downstream.
"""
import os
import time

def export_results(student_anomalies_df, province_anomalies_df, output_dir="output"):
    """
    Xuất các Spark DataFrame ra thư mục Parquet.
    """
    print("\n========================================================")
    print("💾 [Step 05] BẮT ĐẦU XUẤT KẾT QUẢ SẢN PHẨM RA PARQUET")
    print("========================================================")
    start_time = time.time()
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Xuất danh sách Thí sinh bị dán nhãn bất thường ra Parquet phân vùng theo năm
    student_parquet_path = os.path.join(output_dir, "student_anomalies_parquet")
    print(f"📦 Đang ghi kết quả Student Anomalies ra: {student_parquet_path}...")
    
    selected_student_cols = [
        "sbd", "nam_thi", "ma_tinh", "toan", "ngu_van", "ngoai_ngu", 
        "vat_ly", "hoa_hoc", "sinh_hoc", "cluster", "anomaly_score", "is_student_anomaly"
    ]
    cols_to_write = [c for c in selected_student_cols if c in student_anomalies_df.columns]
    
    student_anomalies_df.select(cols_to_write) \
        .write \
        .mode("overwrite") \
        .partitionBy("nam_thi") \
        .parquet(student_parquet_path)
        
    print(f"✅ Đã ghi thành công Parquet Student Anomalies!")

    # 2. Xuất danh sách Z-Score Tỉnh thành ra Parquet
    if province_anomalies_df is not None:
        prov_parquet_path = os.path.join(output_dir, "province_anomalies_parquet")
        print(f"📦 Đang ghi kết quả Province Z-Score Anomalies ra: {prov_parquet_path}...")
        province_anomalies_df.write \
            .mode("overwrite") \
            .parquet(prov_parquet_path)
        print(f"✅ Đã ghi thành công Parquet Province Anomalies!")

    elapsed = time.time() - start_time
    print(f"🎉 Ghi dữ liệu kết quả hoàn tất trong {elapsed:.2f} giây! Lưu trữ tại: '{output_dir}/'")
