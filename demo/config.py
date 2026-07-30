"""
config.py — Centralized configuration for VNExam AnomalyGuard Dashboard.
All paths, constants, and navigation items are defined here.
"""
import os
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
DEMO_DIR     = Path(__file__).parent
BASE_DIR     = DEMO_DIR.parent
OUTPUT_DIR   = BASE_DIR / "output"
JSON_PATH    = DEMO_DIR / "dashboard_data.json"
TEMPLATE_DIR = DEMO_DIR / "templates"
CSS_PATH     = DEMO_DIR / "styles" / "theme.css"

# ── App Meta ──────────────────────────────────────────────────────────────────
APP_TITLE    = "VNExam AnomalyGuard"
APP_ICON     = "🛡️"
APP_SUBTITLE = (
    "Hệ thống phân tích phổ điểm & phát hiện bất thường "
    "thi THPT Quốc Gia (2016–2026) · Apache Spark Pipeline"
)
PAGE_TITLE   = "VNExam AnomalyGuard — Kiểm Toán Thi THPT"

# ── Navigation items: (page_key, icon_emoji, display_label) ──────────────────
NAV_ITEMS = [
    ("tong_quan", "📊", "Tổng Quan"),
    ("thong_ke",  "📋", "Thống Kê Mô Tả"),
    ("kmeans",    "👤", "K-Means Thí Sinh"),
    ("zscore",    "🗺️", "Z-Score Tỉnh Thành"),
]

DEFAULT_PAGE = NAV_ITEMS[0][0]  # mặc định vào Tổng Quan

# ── ML / Analytics thresholds ─────────────────────────────────────────────────
Z_SCORE_THRESHOLD   = 3.0
KMEANS_K            = 4
KMEANS_PERCENTILE   = 99.5

# ── Scandal ground-truth years & provinces ────────────────────────────────────
SCANDAL_2018_PROVINCES = {"15", "26", "36"}
