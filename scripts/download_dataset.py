#!/usr/bin/env python3
"""
scripts/download_dataset.py
Tự động mount và tải dataset từ Kaggle về thư mục data/processed/exam_scores_2016_2026.csv
sử dụng thư viện official kagglehub của Kaggle.

Cách dùng:
    python3 scripts/download_dataset.py
"""
import os
import sys
import shutil

KAGGLE_DATASET_HANDLE = "bchnhnnguynhunh/viet-name-national-exam-scores-2016-2026"

def ensure_dataset(target_csv=None):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not target_csv:
        target_csv = os.path.join(base_dir, "data", "processed", "exam_scores_2016_2026.csv")

    if os.path.exists(target_csv) and os.path.getsize(target_csv) > 100 * 1024 * 1024:
        print(f"✅ Dataset đã tồn tại sẵn tại: {target_csv} ({os.path.getsize(target_csv)/(1024**3):.2f} GB)")
        return target_csv

    print("\n========================================================")
    print("⬇️ BẮT ĐẦU TỰ ĐỘNG TẢI DATASET TỪ KAGGLE (KAGGLEHUB)")
    print("========================================================")
    print(f"📌 Kaggle Dataset Handle: {KAGGLE_DATASET_HANDLE}")

    try:
        import kagglehub
    except ImportError:
        print("📦 Đang tự động cài đặt thư viện 'kagglehub'...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "kagglehub"])
        import kagglehub

    print("📥 Đang tải xuống dữ liệu từ Kaggle...")
    downloaded_dir = kagglehub.dataset_download(KAGGLE_DATASET_HANDLE)
    print(f"📍 Kaggle cache directory: {downloaded_dir}")

    # Tìm file csv trong thư mục vừa tải về
    csv_files = [f for f in os.listdir(downloaded_dir) if f.endswith(".csv")]
    if not csv_files:
        raise FileNotFoundError(f"Không tìm thấy file CSV nào trong thư mục tải về {downloaded_dir}")

    source_csv = os.path.join(downloaded_dir, csv_files[0])
    os.makedirs(os.path.dirname(target_csv), exist_ok=True)

    print(f"🚚 Đang copy/link file {source_csv} -> {target_csv}...")
    shutil.copyfile(source_csv, target_csv)
    print(f"🎉 Tự động mount dataset thành công! Lưu tại: {target_csv}")
    return target_csv

if __name__ == "__main__":
    ensure_dataset()
