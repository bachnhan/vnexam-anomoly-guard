#!/usr/bin/env python3
import os
import glob
import pandas as pd

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "du-lieu-diem-thi")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
BY_YEAR_DIR = os.path.join(PROCESSED_DIR, "by_year")
METADATA_DIR = os.path.join(BASE_DIR, "data", "metadata")

os.makedirs(BY_YEAR_DIR, exist_ok=True)
os.makedirs(METADATA_DIR, exist_ok=True)

# Target Column Mapping for 2016-2026 datasets
COLUMN_MAPPING = {
    'SBD': 'sbd',
    'Nam': 'year',
    'Tinh': 'province_id',
    'SBD_New': 'sbd_new',
    'Toan': 'math',
    'NguVan': 'literature',
    'VatLy': 'physics',
    'HoaHoc': 'chemistry',
    'SinhHoc': 'biology',
    'LichSu': 'history',
    'DiaLy': 'geography',
    'GDCD': 'civics',
    'KinhTePhapLuat': 'econ_law',
    'TinHoc': 'informatics',
    'CongNgheCongNghiep': 'industrial_tech',
    'CongNgheNongNghiep': 'agri_tech',
    'NgoaiNgu': 'foreign_lang',
    'MaMonNgoaiNgu': 'foreign_lang_code',
    'TongDiem': 'total_score',
    'KhoiA': 'group_a',
    'KhoiA1': 'group_a1',
    'KhoiB': 'group_b',
    'KhoiC': 'group_c',
    'KhoiD': 'group_d',
    'KhoiA02': 'group_a02',
    'KhoiC01': 'group_c01',
    'KhoiD07': 'group_d07',
    'KHTN': 'khtn_avg',
    'KHXH': 'khxh_avg',
    'TongDiemKHTN': 'total_khtn',
    'TongDiemKHXH': 'total_khxh'
}

UNIFIED_COLUMNS = [
    'sbd', 'year', 'exam_session', 'province_id', 'sbd_new',
    'math', 'literature', 'physics', 'chemistry', 'biology',
    'history', 'geography', 'civics', 'econ_law', 'informatics',
    'industrial_tech', 'agri_tech', 'foreign_lang', 'foreign_lang_code',
    'total_score', 'group_a', 'group_a1', 'group_b', 'group_c', 'group_d',
    'group_a02', 'group_c01', 'group_d07', 'khtn_avg', 'khxh_avg',
    'total_khtn', 'total_khxh'
]

FILE_SPECS_2016_2026 = [
    ('du-lieu-diem-thi-2016-dh.csv', 2016, 'dh'),
    ('du-lieu-diem-thi-2016-dp.csv', 2016, 'dp'),
    ('du_lieu_diem_thi_2017.csv', 2017, 'chinh_thuc'),
    ('du_lieu_diem_thi_2018.csv', 2018, 'chinh_thuc'),
    ('du_lieu_diem_thi_2019.csv', 2019, 'chinh_thuc'),
    ('du_lieu_diem_thi_2020.csv', 2020, 'chinh_thuc'),
    ('du_lieu_diem_thi_2020_dot_2_da_nang.csv', 2020, 'dot_2_da_nang'),
    ('du_lieu_diem_thi_2021.csv', 2021, 'chinh_thuc'),
    ('du_lieu_diem_thi_2021_dot_2.csv', 2021, 'dot_2'),
    ('du_lieu_diem_thi_2022.csv', 2022, 'chinh_thuc'),
    ('du_lieu_diem_thi_2023.csv', 2023, 'chinh_thuc'),
    ('du_lieu_diem_thi_2024.csv', 2024, 'chinh_thuc'),
    ('du-lieu-diem-thi-2025-ct2006.csv', 2025, 'ct2006'),
    ('du-lieu-diem-thi-2025-ct2018.csv', 2025, 'ct2018'),
    ('du_lieu_diem_thi_2026.csv', 2026, 'chinh_thuc'),
]

def process_2013_2014():
    filename = "du-lieu-diem-thi-2013-2014.csv"
    filepath = os.path.join(RAW_DIR, filename)
    if not os.path.exists(filepath):
        print(f"Skipping {filename}: file not found.")
        return

    print(f"Processing {filename}...")
    df = pd.read_csv(filepath, low_memory=False)
    
    # Rename columns
    rename_dict = {
        'Nam': 'year_short',
        'Tinh': 'province_id',
        'KyThi': 'exam_type',
        'DH': 'uni_code',
        'Khoi': 'group_code',
        'SBD': 'sbd',
        'HovaTen': 'full_name',
        'NgaySinh': 'dob',
        'Mon1': 'subject_1',
        'Mon2': 'subject_2',
        'Mon3': 'subject_3',
        'TongDiem': 'total_score'
    }
    df.rename(columns=rename_dict, inplace=True)
    
    # Convert year_short (13 -> 2013, 14 -> 2014)
    df['year'] = df['year_short'].apply(lambda x: 2000 + int(x) if pd.notnull(x) and str(x).isdigit() else x)
    df.drop(columns=['year_short'], inplace=True, errors='ignore')
    
    # Scale scores from x100 to scale 10.0
    for col in ['subject_1', 'subject_2', 'subject_3', 'total_score']:
        df[col] = pd.to_numeric(df[col], errors='coerce') / 100.0

    # Save per year
    for yr in [2013, 2014]:
        sub_df = df[df['year'] == yr]
        out_path = os.path.join(BY_YEAR_DIR, f"exam_scores_{yr}.csv")
        sub_df.to_csv(out_path, index=False)
        print(f"Saved {out_path} ({len(sub_df):,} rows)")

def process_2016_2026():
    master_csv_path = os.path.join(PROCESSED_DIR, "exam_scores_2016_2026.csv")
    first_file = True

    for filename, default_year, session in FILE_SPECS_2016_2026:
        filepath = os.path.join(RAW_DIR, filename)
        if not os.path.exists(filepath):
            print(f"Skipping {filename}: file not found.")
            continue

        print(f"Processing {filename} (year={default_year}, session={session})...")
        df = pd.read_csv(filepath, low_memory=False)
        
        # Rename columns according to mapping
        df.rename(columns=COLUMN_MAPPING, inplace=True)
        
        # Ensure year column is 4 digits
        if 'year' in df.columns:
            df['year'] = df['year'].apply(lambda x: 2000 + int(x) if pd.notnull(x) and (isinstance(x, int) or str(x).isdigit()) and int(x) < 100 else default_year)
        else:
            df['year'] = default_year
            
        df['exam_session'] = session

        # Reindex to match unified columns
        for col in UNIFIED_COLUMNS:
            if col not in df.columns:
                df[col] = None

        df_unified = df[UNIFIED_COLUMNS]

        # Save to per-file / per-year output
        year_out_name = f"exam_scores_{default_year}"
        if session not in ['chinh_thuc', 'dh']:
            year_out_name += f"_{session}"
        by_year_path = os.path.join(BY_YEAR_DIR, f"{year_out_name}.csv")
        df_unified.to_csv(by_year_path, index=False)
        print(f"Saved {by_year_path} ({len(df_unified):,} rows, {os.path.getsize(by_year_path) / 1024 / 1024:.2f} MB)")

        # Append to Master CSV (> 500 MB target)
        mode = 'w' if first_file else 'a'
        header = first_file
        df_unified.to_csv(master_csv_path, mode=mode, header=header, index=False)
        first_file = False

    print(f"\nMaster dataset created at: {master_csv_path}")
    print(f"Master file size: {os.path.getsize(master_csv_path) / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    print("=== STARTING ETL PROCESS ===")
    process_2013_2014()
    process_2016_2026()
    print("=== ETL PROCESS COMPLETED SUCCESSFULLY ===")
