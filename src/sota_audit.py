#!/usr/bin/env python3
"""
Module: src/sota_audit.py
Kiểm thử 3 Kỹ thuật SOTA Nâng cao trong Trắc lượng học (Psychometrics & Big Data Forensics):
1. Benford's Law Chi-Square Audit (First Digit Analysis)
2. Mahalanobis Distance Covariance Outlier Detection (Student Multivariates)
3. Shannon Entropy Score Distribution Audit (Low Entropy Anomalies)
"""
import os
import sys
import math
import time
import pandas as pd
import numpy as np

# BENFORD THEORETICAL FREQUENCIES (First Digit 1..9)
BENFORD_P = [math.log10(1 + 1/d) for d in range(1, 10)]

def run_benford_law_audit(df):
    """
    Kỹ thuật 1: Kiểm toán Định luật Benford bằng kiểm định Chi-Square (chi^2).
    """
    print("\n========================================================")
    print("🔬 [METHOD 1] THỰC THI KIỂM TOÁN ĐỊNH LUẬT BENFORD (BENFORD'S LAW CHI-SQUARE AUDIT)")
    print("========================================================")
    start_time = time.time()
    
    # Cột điểm Toán
    score_col = 'toan' if 'toan' in df.columns else 'math'
    scores = df[df[score_col].notnull() & (df[score_col] > 0)][score_col] * 10
    first_digits = scores.astype(str).str[0].astype(int)
    first_digits = first_digits[first_digits.between(1, 9)]
    
    total_count = len(first_digits)
    counts = first_digits.value_counts().reindex(range(1, 10), fill_value=0)
    obs_pct = counts / total_count
    
    chi_square = sum(((counts[d] - total_count * BENFORD_P[d-1]) ** 2) / (total_count * BENFORD_P[d-1]) for d in range(1, 10))
    
    print(f"📊 Tổng số mẫu phân tích chữ số đầu tiên: {total_count:,}")
    print("📌 Tần suất Chữ số Đầu tiên (Observed vs Benford Theoretical):")
    b_table = pd.DataFrame({
        'Chữ số (Digit)': range(1, 10),
        'Thực tế (Observed %)': [round(obs_pct[d]*100, 2) for d in range(1, 10)],
        'Benford Lý thuyết (%)': [round(BENFORD_P[d-1]*100, 2) for d in range(1, 10)]
    })
    print(b_table.to_string(index=False))
    print(f"\n🎯 Chi-Square Score (\u03c7\u00b2): {chi_square:.2f}")
    if chi_square > 26.12:
        print("🚨 CẢNH BÁO BENFORD: Chỉ số \u03c7\u00b2 > 26.12 (p < 0.001)! Phổ điểm có dấu vết bị bóp méo nhân tạo.")
    else:
        print("✅ Dữ liệu tuân theo Phân phối Benford tự nhiên.")
    print(f"⏱️ Hoàn tất kiểm toán Benford trong {time.time() - start_time:.2f} giây.")

def run_mahalanobis_distance_audit(df, sample_size=50000):
    """
    Kỹ thuật 2: Khoảng cách Đa chiều Mahalanobis (Mahalanobis Covariance Outliers).
    """
    print("\n========================================================")
    print("📐 [METHOD 2] THỰC THI KHOẢNG CÁCH MAHALANOBIS ĐA CHIỀU (MAHALANOBIS DISTANCE)")
    print("========================================================")
    start_time = time.time()
    
    cols = ["toan", "vat_ly", "hoa_hoc", "sinh_hoc", "ngoai_ngu", "ngu_van"]
    avail_cols = [c for c in cols if c in df.columns]
    
    sample_df = df[avail_cols].dropna().sample(n=min(sample_size, len(df)), random_state=42)
    
    X = sample_df.values
    mu = np.mean(X, axis=0)
    cov = np.cov(X, rowvar=False)
    inv_cov = np.linalg.inv(cov)
    
    diff = X - mu
    md_sq = np.sum(np.dot(diff, inv_cov) * diff, axis=1)
    md = np.sqrt(md_sq)
    
    cutoff_sq = 18.55
    anomalies = sample_df[md_sq > cutoff_sq]
    
    print(f"📊 Phân tích mẫu {len(sample_df):,} thí sinh trên không gian {len(avail_cols)} môn thi...")
    print(f"📍 Trung bình Mahalanobis Distance: {np.mean(md):.2f}")
    print(f"📍 Max Mahalanobis Distance: {np.max(md):.2f}")
    print(f"🎯 Ngưỡng Chi-Square Critical Threshold (\u03c7\u00b2 df=6, p<0.005): {cutoff_sq:.2f}")
    print(f"🚨 Phát hiện {len(anomalies):,} thí sinh có phổ điểm lệch ma trận tương quan (Mahalanobis Outliers).")
    
    if len(anomalies) > 0:
        print("\n📌 Mẫu 5 Thí sinh có khoảng cách Mahalanobis cao nhất (Bất thường lệch môn):")
        sample_df['mahalanobis_dist'] = md
        print(sample_df.sort_values('mahalanobis_dist', ascending=False).head(5))
        
    print(f"⏱️ Hoàn tất Mahalanobis Audit trong {time.time() - start_time:.2f} giây.")

def run_shannon_entropy_audit(df):
    """
    Kỹ thuật 3: Kiểm toán Độ hỗn loạn Shannon Entropy (Shannon Entropy Audit per Province).
    """
    print("\n========================================================")
    print("🌀 [METHOD 3] THỰC THI KIỂM TOÁN ĐỘ HỖN LOẠN SHANNON ENTROPY (SHANNON ENTROPY AUDIT)")
    print("========================================================")
    start_time = time.time()
    
    score_col = 'toan' if 'toan' in df.columns else 'math'
    prov_col = 'ma_tinh' if 'ma_tinh' in df.columns else 'province_id'
    year_col = 'nam_thi' if 'nam_thi' in df.columns else 'year'
    
    def calc_entropy(series):
        valid = series.dropna().round(1)
        if len(valid) == 0:
            return 0.0
        counts = valid.value_counts()
        probs = counts / len(valid)
        return float(-np.sum(probs * np.log2(probs)))

    entropy_df = df[df[score_col].notnull() & df[prov_col].notnull() & df[year_col].notnull()] \
        .groupby([year_col, prov_col])[score_col] \
        .agg(total='count', entropy=calc_entropy) \
        .reset_index()

    entropy_df = entropy_df[entropy_df['total'] >= 1000]
    
    mean_h = entropy_df['entropy'].mean()
    std_h = entropy_df['entropy'].std()
    entropy_df['h_z_score'] = (mean_h - entropy_df['entropy']) / std_h
    
    print(f"📊 Số lượng cụm thi/tỉnh thành phân tích Entropy: {len(entropy_df)}")
    print(f"📍 Entropy trung bình toàn quốc: {mean_h:.3f} bits")
    print(f"📍 Độ lệch chuẩn Entropy: {std_h:.3f} bits")
    
    low_entropy = entropy_df.sort_values('entropy', ascending=True).head(10)
    print("\n🚨 Top 10 Cụm thi có Shannon Entropy THẤP NHẤT (Phổ điểm bị nén / can thiệp hàng loạt):")
    print(low_entropy[[year_col, prov_col, 'total', 'entropy', 'h_z_score']].to_string(index=False))
    
    print(f"⏱️ Hoàn tất Shannon Entropy Audit trong {time.time() - start_time:.2f} giây.")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_csv = os.path.join(base_dir, "data", "processed", "exam_scores_2016_2026.csv")
    
    print(f"🚀 Nạp tập dữ liệu để thực thi 3 Kỹ thuật SOTA Audit: {target_csv}")
    t0 = time.time()
    df = pd.read_csv(target_csv, low_memory=False)
    
    # Map English column names to Vietnamese standard aliases
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
    df.rename(columns=col_mapping, inplace=True)
    print(f"✅ Nạp dữ liệu hoàn tất trong {time.time() - t0:.2f} giây! ({len(df):,} bản ghi)")
    
    run_benford_law_audit(df)
    run_mahalanobis_distance_audit(df)
    run_shannon_entropy_audit(df)
    
    print("\n========================================================")
    print("🎉 HOÀN THÀNH KIỂM THỬ THÀNH CÔNG 3 KỸ THUẬT SOTA ANOMALY DETECTORS!")
    print("========================================================\n")

if __name__ == "__main__":
    main()
