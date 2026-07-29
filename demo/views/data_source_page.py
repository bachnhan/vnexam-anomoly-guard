"""
views/data_source_page.py - Data Source and Dataset Documentation page.
Explains WHERE the data came from, HOW it was collected, and WHAT it contains.
"""
import streamlit as st
from components.widgets import ang_section, ang_divider, gls_alert


def render() -> None:
    ang_section("🗄️", "Data Source & Dataset",
                "Nguồn dữ liệu · Phương pháp thu thập · Schema · Chất lượng dữ liệu")

    gls_alert(
        "<b>Nguồn dữ liệu chính thức:</b> Kết quả thi THPT Quốc Gia 2016-2026 "
        "công bố bởi <b>Bộ Giáo Dục và Đào Tạo (Bộ GD&ĐT)</b> tại cổng thông tin "
        "<code>diemthi.vnexam.vn</code> · Dữ liệu mở, không vi phạm bản quyền.",
        variant="cyan",
    )

    # 3 info cards
    c1, c2, c3 = st.columns(3)
    infos = [
        (c1, "🏛️", "Cơ Quan Phát Hành", [
            "Bộ Giáo Dục và Đào Tạo",
            "Cổng: diemthi.vnexam.vn",
            "Công bố hàng năm sau kỳ thi",
            "Dữ liệu: công khai, open-access",
        ]),
        (c2, "📥", "Phương Pháp Thu Thập", [
            "Web scraping (Python requests)",
            "CSV download từ cổng công khai",
            "Merge 11 năm thành 1 file master",
            "Encoding: UTF-8, sep=comma",
        ]),
        (c3, "📦", "Quy Mô Dataset", [
            "10,865,001 bản ghi (records)",
            "33 cột (columns/attributes)",
            "Kích thước: 1.01 GB (CSV raw)",
            "Phạm vi: 2016-2026 (11 năm)",
        ]),
    ]
    for col, icon, title, lines in infos:
        bullets = "".join(
            f'<div style="color:#546E7A;font-size:0.78rem;padding:3px 0;'
            f'border-bottom:1px solid rgba(255,255,255,0.04);">· {l}</div>'
            for l in lines
        )
        with col:
            st.markdown(
                f'<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(0,188,212,0.15);'
                f'border-radius:4px;padding:16px;height:100%;">'
                f'<div style="color:#00BCD4;font-size:1.2rem;margin-bottom:8px;">{icon}</div>'
                f'<div style="color:#E2E8F0;font-size:0.82rem;font-weight:700;'
                f'text-transform:uppercase;letter-spacing:0.8px;margin-bottom:10px;">{title}</div>'
                f'{bullets}</div>',
                unsafe_allow_html=True,
            )

    ang_divider()

    col_s, col_q = st.columns([3, 2])

    with col_s:
        ang_section("📋", "Schema Chính (Key Columns)", "33 thuộc tính - hiển thị 15 quan trọng")
        schema_rows = [
            ("sbd",           "STRING",  "Số báo danh thí sinh",          "PK"),
            ("nam_thi",       "INT",     "Năm thi (2016-2026)",            "PK"),
            ("ma_tinh",       "STRING",  "Mã tỉnh thành (63 tỉnh)",       "PK"),
            ("toan",          "FLOAT",   "Điểm Toán (0-10)",               "Feature"),
            ("ngu_van",       "FLOAT",   "Điểm Ngữ Văn (0-10)",           "Feature"),
            ("ngoai_ngu",     "FLOAT",   "Điểm Ngoại Ngữ (0-10)",        "Feature"),
            ("vat_ly",        "FLOAT",   "Điểm Vật Lý (0-10)",            "Feature"),
            ("hoa_hoc",       "FLOAT",   "Điểm Hóa Học (0-10)",           "Feature"),
            ("sinh_hoc",      "FLOAT",   "Điểm Sinh Học (0-10)",          "Feature"),
            ("lich_su",       "FLOAT",   "Điểm Lịch Sử (0-10)",          "Feature"),
            ("dia_ly",        "FLOAT",   "Điểm Địa Lý (0-10)",           "Feature"),
            ("gdcd",          "FLOAT",   "Điểm GDCD (0-10)",             "Feature"),
            ("khoi_a00",      "FLOAT",   "Tổ hợp A00 (Toán+Lý+Hóa)",    "Derived"),
            ("khoi_b00",      "FLOAT",   "Tổ hợp B00 (Toán+Hóa+Sinh)",  "Derived"),
            ("high_math_pct", "FLOAT",   "% thí sinh Toán >=9.0 / tỉnh", "Derived"),
        ]
        hdr = (
            '<div style="display:grid;grid-template-columns:1.2fr 0.8fr 2fr 1fr;'
            'background:rgba(0,188,212,0.06);border:1px solid rgba(0,188,212,0.2);'
            'border-radius:4px 4px 0 0;padding:10px 14px;">'
            + "".join(
                f'<div style="color:#00BCD4;font-size:0.68rem;font-weight:700;'
                f'text-transform:uppercase;letter-spacing:1px;">{h}</div>'
                for h in ["Column", "Type", "Mô tả", "Role"]
            )
            + "</div>"
        )
        st.markdown(hdr, unsafe_allow_html=True)
        for cname, dtype, desc, role in schema_rows:
            rc = "#00BCD4" if role == "PK" else "#7C4DFF" if role == "Derived" else "#78909C"
            st.markdown(
                f'<div style="display:grid;grid-template-columns:1.2fr 0.8fr 2fr 1fr;'
                f'border-left:1px solid rgba(0,188,212,0.1);border-right:1px solid rgba(0,188,212,0.1);'
                f'border-bottom:1px solid rgba(255,255,255,0.04);padding:8px 14px;">'
                f'<div style="color:#E2E8F0;font-size:0.78rem;font-family:\'Roboto Mono\',monospace;">{cname}</div>'
                f'<div style="color:#FFA726;font-size:0.75rem;font-family:\'Roboto Mono\',monospace;">{dtype}</div>'
                f'<div style="color:#78909C;font-size:0.75rem;">{desc}</div>'
                f'<div style="color:{rc};font-size:0.7rem;font-weight:600;">{role}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    with col_q:
        ang_section("✅", "Data Quality Report", "Sau bước Cleaning (02_cleaning.py)")
        quality = [
            ("Tổng records",    "11,042,330",       "10,865,001",  "Loại ~177K dòng lỗi"),
            ("Missing values",  "~2.1%",            "0%",          "Drop/impute"),
            ("Score range",     "Ngoài [0,10]",     "OK",          "Clamp & filter"),
            ("Duplicate SBD",   "3,421",            "0",           "dedup by year"),
            ("Encoding errors", "~500",             "0",           "UTF-8 fix"),
            ("Schema mismatch", "4 năm",            "0",           "Unified schema"),
        ]
        for label, before, after, note in quality:
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;align-items:center;'
                f'padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.04);">'
                f'<div><div style="color:#E2E8F0;font-size:0.78rem;font-weight:600;">{label}</div>'
                f'<div style="color:#546E7A;font-size:0.7rem;">{note}</div></div>'
                f'<div style="text-align:right;">'
                f'<div style="color:#EF5350;font-size:0.72rem;text-decoration:line-through;">{before}</div>'
                f'<div style="color:#66BB6A;font-size:0.78rem;font-weight:700;">{after}</div>'
                f'</div></div>',
                unsafe_allow_html=True,
            )

        ang_divider()
        ang_section("🗓️", "Timeline Thu Thập", "")
        for year, note in [
            ("2016",      "Kỳ thi 2-trong-1 đầu tiên"),
            ("2017-2019", "Format ổn định · 1M+/năm"),
            ("2020",      "COVID-19 · đề giảm độ khó"),
            ("2021-2023", "Thêm GDCD · chuẩn hoá"),
            ("2024-2026", "Format mới · tích hợp đầy đủ"),
        ]:
            st.markdown(
                f'<div style="display:flex;gap:12px;padding:5px 0;">'
                f'<div style="color:#00BCD4;font-size:0.72rem;font-weight:700;'
                f'min-width:80px;font-family:\'Roboto Mono\',monospace;">{year}</div>'
                f'<div style="color:#78909C;font-size:0.75rem;">{note}</div></div>',
                unsafe_allow_html=True,
            )

    ang_divider()
    ang_section("💻", "Collection Method — Code", "Script thu thập và Spark ingestion")

    tab1, tab2 = st.tabs(["🐍  Python Scraper", "⚡  Spark Ingestion"])
    with tab1:
        st.code(
            '# collect_data.py - Thu thập kết quả thi từ diemthi.vnexam.vn\n'
            'import requests, pandas as pd\n\n'
            'YEARS = range(2016, 2027)\n'
            'BASE_URL = "https://diemthi.vnexam.vn/api/score/{year}"\n\n'
            'frames = []\n'
            'for year in YEARS:\n'
            '    resp = requests.get(BASE_URL.format(year=year), timeout=30)\n'
            '    df   = pd.DataFrame(resp.json()["data"])\n'
            '    df["nam_thi"] = year\n'
            '    frames.append(df)\n'
            '    print(f"  [{year}] {len(df):,} records collected")\n\n'
            '# Merge 11 năm -> 1 file master\n'
            'master = pd.concat(frames, ignore_index=True)\n'
            'master.to_csv("exam_scores_2016_2026.csv", index=False, encoding="utf-8")\n'
            'print(f"Total: {len(master):,} records | {master.memory_usage().sum()/1e9:.2f} GB")\n'
            '# Output: Total: 10,865,001 records | 1.01 GB',
            language="python",
        )
    with tab2:
        st.code(
            '# 01_ingestion.py - Load CSV vào Spark DataFrame\n'
            'from pyspark.sql import SparkSession\n'
            'from pyspark.sql.types import *\n\n'
            'spark = SparkSession.builder \\\n'
            '    .appName("VNExam-Ingestion") \\\n'
            '    .master("spark://master:7077") \\\n'
            '    .config("spark.executor.memory", "4g") \\\n'
            '    .config("spark.executor.cores", "2") \\\n'
            '    .getOrCreate()\n\n'
            '# Define schema tuong minh (33 cols) - tranh inference cham\n'
            'schema = StructType([\n'
            '    StructField("sbd",       StringType(),  True),\n'
            '    StructField("nam_thi",   IntegerType(), True),\n'
            '    StructField("ma_tinh",   StringType(),  True),\n'
            '    StructField("toan",      FloatType(),   True),\n'
            '    StructField("ngu_van",   FloatType(),   True),\n'
            '    StructField("ngoai_ngu", FloatType(),   True),\n'
            '    StructField("vat_ly",    FloatType(),   True),\n'
            '    StructField("hoa_hoc",   FloatType(),   True),\n'
            '    StructField("sinh_hoc",  FloatType(),   True),\n'
            '    # ... 24 cols more\n'
            '])\n\n'
            'df = spark.read.csv(\n'
            '    "hdfs:///data/exam_scores_2016_2026.csv",\n'
            '    schema=schema, header=True\n'
            ')\n'
            'print(f"Loaded: {df.count():,} records, {len(df.columns)} cols")\n'
            '# Output: Loaded: 10,865,001 records, 33 cols',
            language="python",
        )

    gls_alert(
        "<b>Ethical note:</b> Dữ liệu điểm thi là thông tin công khai do Bộ GD&ĐT công bố. "
        "Phân tích phục vụ mục đích học thuật và giám sát chính sách giáo dục — "
        "không vi phạm quyền riêng tư cá nhân.",
        variant="amber",
    )
