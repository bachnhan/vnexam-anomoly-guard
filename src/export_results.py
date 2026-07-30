#!/usr/bin/env python3
"""
Module: src/export_results.py (Step 05 Export Results)
Xuất kết quả phân tích phổ điểm và danh sách bất thường ra định dạng lưu trữ cột nén Parquet,
phân vùng theo năm (partitionBy("nam_thi")) để tối ưu hóa hiệu năng truy vấn downstream.
"""
import os
import time
import pyspark.sql.functions as F

def export_results(student_anomalies_df, province_anomalies_df, output_dir="output"):
    """
    Xuất các Spark DataFrame ra thư mục Parquet.
    """
    print("\n========================================================")
    print("[Step 05] BẮT ĐẦU XUẤT KẾT QUẢ SẢN PHẨM RA PARQUET")
    print("========================================================")
    start_time = time.time()
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Xuất danh sách Thí sinh bị dán nhãn bất thường ra Parquet phân vùng theo năm
    student_parquet_path = os.path.join(output_dir, "student_anomalies_parquet")
    print(f"Đang ghi kết quả Student Anomalies ra: {student_parquet_path}...")
    
    selected_student_cols = [
        "sbd", "nam_thi", "ma_tinh", "toan", "ngu_van", "ngoai_ngu",
        "vat_ly", "hoa_hoc", "sinh_hoc", "cluster", "anomaly_score",
        "anomaly_pattern", "is_student_anomaly"   # anomaly_pattern: nhãn cho dashboard
    ]
    cols_to_write = [c for c in selected_student_cols if c in student_anomalies_df.columns]
    
    student_anomalies_df.select(cols_to_write) \
        .write \
        .mode("overwrite") \
        .partitionBy("nam_thi") \
        .parquet(student_parquet_path)
        
    print(f"Đã ghi thành công Parquet Student Anomalies!")

    # 2. Xuất danh sách Z-Score Tỉnh thành ra Parquet
    if province_anomalies_df is not None:
        prov_parquet_path = os.path.join(output_dir, "province_anomalies_parquet")
        print(f"Đang ghi kết quả Province Z-Score Anomalies ra: {prov_parquet_path}...")
        province_anomalies_df.write \
            .mode("overwrite") \
            .parquet(prov_parquet_path)
        print(f"Đã ghi thành công Parquet Province Anomalies!")

    elapsed = time.time() - start_time
    print(f"Ghi dữ liệu kết quả hoàn tất trong {elapsed:.2f} giây! Lưu trữ tại: '{output_dir}/'")

    # 3. Export yearly_subjects.json — điểm TB từng môn theo năm (Req 1a + 2a dashboard)
    print("\nĐang export yearly_subjects.json...")
    try:
        yearly_df = student_anomalies_df.groupBy("nam_thi").agg(
            F.round(F.avg("toan"),      2).alias("avg_toan"),
            F.round(F.avg("ngu_van"),   2).alias("avg_nguvan"),
            F.round(F.avg("ngoai_ngu"), 2).alias("avg_ngoaingu"),
            F.round(F.avg("vat_ly"),    2).alias("avg_vatly"),
            F.round(F.avg("hoa_hoc"),   2).alias("avg_hoahoc"),
            F.round(F.avg("sinh_hoc"),  2).alias("avg_sinhhoc"),
            F.count("*").alias("total_candidates"),
        ).orderBy("nam_thi")

        # Tính thêm TB khối KHTN và KHXH cho Req 2a (chart đường)
        yearly_df = yearly_df \
            .withColumn("avg_khtn", F.round(
                (F.col("avg_toan") + F.col("avg_vatly") + F.col("avg_hoahoc")) / 3, 2
            )) \
            .withColumn("avg_khxh", F.round(
                (F.col("avg_nguvan") + F.col("avg_sinhhoc")) / 2, 2
            ))

        yearly_path = os.path.join(os.path.dirname(output_dir), "demo", "yearly_subjects.json")
        yearly_df.toPandas().to_json(yearly_path, orient="records", indent=2, force_ascii=False)
        print(f"Đã export yearly_subjects.json → {yearly_path}")
    except Exception as e:
        print(f"Không thể export yearly_subjects.json: {e}")
