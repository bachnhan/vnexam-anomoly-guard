"""
data/loader.py — Data Access Layer.
Single responsibility: load data from Parquet or JSON, return typed DataFrames.
No Streamlit UI, no HTML, no CSS here.
"""
from __future__ import annotations

import json
import os
import random

import pandas as pd
import streamlit as st

from config import OUTPUT_DIR, JSON_PATH, Z_SCORE_THRESHOLD, BASE_DIR

# Bảng tra tên tỉnh đúng UTF-8 — dùng để fix Parquet bị lỗi encoding
_MATINH_CSV = BASE_DIR / "data" / "metadata" / "ma_tinh.csv"

def _load_tinh_lookup() -> dict:
    """Load ma_tinh → ten_tinh mapping từ CSV chuẩn, bổ sung fallback đầy đủ 63 tỉnh."""
    # Fallback đầy đủ 63 tỉnh/thành — dùng khi CSV thiếu
    _FALLBACK = {
        "01": "Hà Nội",        "02": "Hồ Chí Minh",   "03": "Hải Phòng",
        "04": "Đà Nẵng",       "05": "Hà Giang",       "06": "Cao Bằng",
        "07": "Lai Châu",      "08": "Lào Cai",         "09": "Tuyên Quang",
        "10": "Lạng Sơn",      "11": "Bắc Kạn",        "12": "Thái Nguyên",
        "13": "Yên Bái",       "14": "Sơn La",          "15": "Phú Thọ",
        "16": "Vĩnh Phúc",     "17": "Quảng Ninh",     "18": "Bắc Giang",
        "19": "Bắc Ninh",      "20": "Hải Dương",       "21": "Hưng Yên",
        "22": "Hòa Bình",      "23": "Hà Nam",          "24": "Nam Định",
        "25": "Thái Bình",     "26": "Ninh Bình",       "27": "Thanh Hóa",
        "28": "Nghệ An",       "29": "Hà Tĩnh",         "30": "Quảng Bình",
        "31": "Quảng Trị",     "32": "Thừa Thiên Huế", "33": "Quảng Nam",
        "34": "Quảng Ngãi",    "35": "Bình Định",       "36": "Phú Yên",
        "37": "Khánh Hòa",     "38": "Ninh Thuận",     "39": "Bình Thuận",
        "40": "Kon Tum",       "41": "Gia Lai",          "42": "Đắk Lắk",
        "43": "Lâm Đồng",      "44": "Bình Phước",      "45": "Tây Ninh",
        "46": "Bình Dương",    "47": "Đồng Nai",        "48": "Bà Rịa - Vũng Tàu",
        "49": "Long An",       "50": "Đồng Tháp",       "51": "An Giang",
        "52": "Tiền Giang",    "53": "Bến Tre",          "54": "Vĩnh Long",
        "55": "Trà Vinh",      "56": "Cần Thơ",          "57": "Sóc Trăng",
        "58": "Kiên Giang",    "59": "Bạc Liêu",        "60": "Cà Mau",
        "61": "Điện Biên",     "62": "Đắk Nông",        "63": "Hậu Giang",
        "64": "Hậu Giang",     "65": "Bộ Quốc Phòng",
        # Mã thực tế từ Parquet (có thể khác chuẩn hành chính)
        "66": "Gia Lai",       "68": "Đắk Lắk",         "72": "Bình Phước",
        "74": "Bình Dương",    "75": "Đồng Nai",        "77": "Bà Rịa - Vũng Tàu",
        "79": "TP. HCM",       "80": "Long An",          "82": "Tiền Giang",
        "83": "Bến Tre",       "84": "Trà Vinh",         "86": "Vĩnh Long",
        "87": "Đồng Tháp",     "89": "An Giang",         "91": "Kiên Giang",
        "92": "Cần Thơ",       "93": "Hậu Giang",        "94": "Sóc Trăng",
        "95": "Bạc Liêu",      "96": "Cà Mau",
    }
    try:
        df = pd.read_csv(_MATINH_CSV, encoding="utf-8", dtype={"ma_tinh": str})
        df["ma_tinh"] = df["ma_tinh"].str.strip().str.zfill(2)
        df["ten_tinh"] = (
            df["ten_tinh"]
            .str.replace(r"^Thành phố\s+", "", regex=True)
            .str.replace(r"^Tỉnh\s+", "", regex=True)
            .str.strip()
        )
        csv_lookup = dict(zip(df["ma_tinh"], df["ten_tinh"]))
        # Fallback bổ sung những mã CSV không có
        return {**_FALLBACK, **csv_lookup}
    except Exception:
        return _FALLBACK

_TINH_LOOKUP: dict = {}  # lazy-loaded once


# ────────────────────────────────────────────────────────────────
# Public API
# ────────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, str, dict]:
    """
    Load pipeline data.

    Returns
    -------
    prov_df    : province anomalies DataFrame
    student_df : student outlier DataFrame
    yearly_df  : yearly aggregation DataFrame
    source     : 'parquet' | 'json' | 'none'
    extra      : dict with kpi, ground_truth, top_chart, sota, yearly_extended
    """
    result = _try_parquet()
    if result is not None:
        return result
    return _load_json()


# ────────────────────────────────────────────────────────────────
# Style helpers (pure functions — no Streamlit/HTML dependency)
# ────────────────────────────────────────────────────────────────

def style_z(val: float) -> str:
    """Return CSS style string for a Z-Score cell."""
    if isinstance(val, (int, float)):
        if val >= 4.0:
            return "background-color:rgba(239,83,80,0.25);color:#FFCDD2;font-weight:700;"
        if val >= Z_SCORE_THRESHOLD:
            return "background-color:rgba(239,83,80,0.12);color:#EF9A9A;font-weight:600;"
    return "color:#90A4AE;"


def style_score(val: float) -> str:
    """Return CSS style string for a subject score cell."""
    if isinstance(val, (int, float)):
        if val >= 9.0:
            return "background-color:rgba(0,200,83,0.2);color:#69F0AE;font-weight:700;"
        if val <= 2.0:
            return "background-color:rgba(239,83,80,0.2);color:#FF8A80;font-weight:700;"
    return "color:#90A4AE;"


# ────────────────────────────────────────────────────────────────
# Private helpers
# ────────────────────────────────────────────────────────────────

def _try_parquet():
    """Attempt to load from Parquet output. Returns None on failure."""
    global _TINH_LOOKUP
    prov_file    = os.path.join(OUTPUT_DIR, "province_anomalies_parquet")
    student_file = os.path.join(OUTPUT_DIR, "student_anomalies_parquet")
    if not (os.path.exists(prov_file) and os.path.exists(student_file)):
        return None
    try:
        prov_df    = pd.read_parquet(prov_file)
        student_df = pd.read_parquet(student_file)

        # Fix ten_tinh bị lỗi encoding — dùng bảng tra ma_tinh.csv
        if not _TINH_LOOKUP:
            _TINH_LOOKUP = _load_tinh_lookup()
        if _TINH_LOOKUP and "ma_tinh" in prov_df.columns:
            prov_df["ma_tinh_key"] = prov_df["ma_tinh"].astype(str).str.strip().str.zfill(2)
            prov_df["ten_tinh"]    = prov_df["ma_tinh_key"].map(_TINH_LOOKUP).fillna(prov_df.get("ten_tinh", ""))
            prov_df.drop(columns=["ma_tinh_key"], inplace=True)

        yearly_df  = prov_df.groupby("nam_thi").agg(
            total_students=("total_students", "sum"),
            avg_math_pct=("high_math_pct", "mean"),
        ).reset_index()
        extra = _parse_json_extra()
        return prov_df, student_df, yearly_df, "parquet", extra
    except Exception:
        return None


def _load_json():
    """Load from dashboard_data.json fallback."""
    if not JSON_PATH.exists():
        return None, None, None, "none", {}

    with JSON_PATH.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    yearly_df = pd.DataFrame(raw.get("yearly", []))
    prov_df   = pd.DataFrame(raw.get("flagged_provinces", []))
    if "is_province_anomaly" not in prov_df.columns:
        prov_df["is_province_anomaly"] = prov_df["z_score"] >= Z_SCORE_THRESHOLD

    if "student_anomalies" in raw:
        student_df = pd.DataFrame(raw["student_anomalies"])
    elif "students" in raw:
        student_df = pd.DataFrame(raw["students"])
    else:
        student_df = _mock_students()

    return prov_df, student_df, yearly_df, "json", _parse_extra(raw)


def _parse_json_extra() -> dict:
    """Load only the extra meta sections from JSON (used alongside Parquet)."""
    if not JSON_PATH.exists():
        return {}
    with JSON_PATH.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    return _parse_extra(raw)


def _parse_extra(raw: dict) -> dict:
    return {
        "kpi":               raw.get("kpi", {}),
        "ground_truth":      raw.get("ground_truth", []),
        "top_chart":         raw.get("top_provinces_chart", []),
        "yearly_extended":   raw.get("yearly_extended", []),
        "sota":              raw.get("sota_results", {}),
        "yearly_subjects":   raw.get("yearly_subjects", []),
        "student_specimens": raw.get("student_specimens", []),
        "zscore_2018":       raw.get("zscore_2018", []),
    }


def _mock_students() -> pd.DataFrame:
    """Generate synthetic student outlier data for demo fallback."""
    random.seed(42)
    rows = []
    for _ in range(20):
        rows.append({
            "sbd":             f"1{random.randint(1_000_000, 9_999_999)}",
            "nam_thi":         random.choice([2018, 2021]),
            "ma_tinh":         random.choice(["15", "26", "36"]),
            "toan":            round(random.uniform(9.0, 10.0), 2),
            "vat_ly":          round(random.uniform(0.0, 2.0), 2),
            "hoa_hoc":         round(random.uniform(3.0, 7.0), 2),
            "ngoai_ngu":       round(random.uniform(5.0, 9.0), 2),
            "ngu_van":         round(random.uniform(5.0, 8.0), 2),
            "anomaly_score":   round(random.uniform(3.5, 6.2), 3),
            "anomaly_pattern": "Toán cao + Lý liệt",
            "is_student_anomaly": True,
        })
    return pd.DataFrame(rows)
