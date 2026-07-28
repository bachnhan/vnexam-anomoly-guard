#!/usr/bin/env python3
"""
Export Web Dashboard JSON Data
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
        print("⚠️ Parquet files missing.")
        return
        
    prov_df = pd.read_parquet(prov_file)
    student_df = pd.read_parquet(student_file)
    
    # 1. Yearly Summary
    yearly = prov_df.groupby("nam_thi").agg(
        total_students=('total_students', 'sum'),
        avg_math_pct=('high_math_pct', 'mean')
    ).reset_index()
    yearly_dict = json.loads(yearly.to_json(orient="records"))
    
    # 2. Flagged Anomalies
    flagged = prov_df[prov_df['is_province_anomaly'] == True].sort_values('z_score', ascending=False).head(30)
    flagged_sub = flagged[['nam_thi', 'ma_tinh', 'total_students', 'high_math_pct', 'z_math', 'z_a00', 'z_bio', 'z_score', 'yoy_math_delta_pct']]
    flagged_dict = json.loads(flagged_sub.to_json(orient="records"))
    
    # 3. Student Outliers
    students = student_df[(student_df['toan'] >= 9.0) & ((student_df['vat_ly'] <= 2.0) | (student_df['hoa_hoc'] <= 2.0) | (student_df['ngoai_ngu'] <= 2.0))].head(20)
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
        
    print(f"✅ Đã xuất dữ liệu Dashboard ra {out_json}")

if __name__ == "__main__":
    export_json()
