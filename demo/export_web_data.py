#!/usr/bin/env python3
"""
Script: demo/export_web_data.py
Xuất dữ liệu từ Parquet sang dashboard_data.json cho Web Dashboard
Bao gồm đầy đủ 14 chỉ số Z-Score VÀ 14 chỉ số YoY Delta từng môn/khối thi
Sắp xếp mặc định: Năm thi TĂNG DẦN (nam_thi asc), Mã tỉnh TĂNG DẦN (ma_tinh asc)
"""
import os
import json
import pandas as pd

def export_json():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "output")
    
    prov_file = os.path.join(output_dir, "province_anomalies_parquet")
    student_file = os.path.join(output_dir, "student_anomalies_parquet")
    
    if not os.path.exists(prov_file) or not os.path.exists(student_file):
        print("❌ Chưa tìm thấy dữ liệu Parquet trong output/")
        return
        
    prov_df = pd.read_parquet(prov_file)
    student_df = pd.read_parquet(student_file)
    
    # 1. Yearly Summary
    yearly = prov_df.groupby("nam_thi").agg(
        avg_math_pct=('high_math_pct', 'mean'),
        total_candidates=('total_students', 'sum')
    ).reset_index().sort_values("nam_thi", ascending=True)
    yearly_dict = json.loads(yearly.to_json(orient="records"))
    
    # 2. Flagged Provinces (Sorted by nam_thi ASC, then ma_tinh ASC)
    flagged = prov_df[prov_df['is_province_anomaly'] == True].sort_values(['nam_thi', 'ma_tinh'], ascending=[True, True])
    
    available_cols = ['nam_thi', 'ma_tinh', 'total_students', 'high_math_pct', 'z_score', 'yoy_math_delta_pct', 'yoy_z_delta', 'is_yoy_spike']
    
    z_cols = ['z_math', 'z_van', 'z_anh', 'z_ly', 'z_hoa', 'z_bio', 'z_su', 'z_dia', 'z_gdcd', 'z_a00', 'z_a01', 'z_b00', 'z_c00', 'z_d01']
    yoy_z_cols = [f"yoy_{c}" for c in z_cols]
    
    for c in z_cols + yoy_z_cols:
        if c in flagged.columns:
            available_cols.append(c)
            
    flagged_sub = flagged[available_cols]
    flagged_dict = json.loads(flagged_sub.to_json(orient="records"))
    
    # 3. Student Outliers (Sorted by nam_thi ASC, then ma_tinh ASC)
    students = student_df[(student_df['toan'] >= 9.0) & ((student_df['vat_ly'] <= 2.0) | (student_df['hoa_hoc'] <= 2.0) | (student_df['ngoai_ngu'] <= 2.0))].sort_values(['nam_thi', 'ma_tinh'], ascending=[True, True]).head(50)
    students_sub = students[['sbd', 'nam_thi', 'ma_tinh', 'toan', 'vat_ly', 'hoa_hoc', 'ngoai_ngu', 'ngu_van']]
    students_dict = json.loads(students_sub.to_json(orient="records"))
    
    data = {
        "yearly": yearly_dict,
        "flagged_provinces": flagged_dict,
        "students": students_dict
    }
    
    out_json = os.path.join(base_dir, "demo", "dashboard_data.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"✅ Đã xuất dữ liệu Dashboard (Đầy đủ 14 Z-Score & 14 YoY Delta từng môn/khối) ra {out_json}")

if __name__ == "__main__":
    export_json()
