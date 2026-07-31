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
YEARLY_SUBJECTS_PATH = DEMO_DIR / "yearly_subjects.json"
SPARK_META_PATH = DEMO_DIR / "spark_computed_meta.json"
TEMPLATE_DIR = DEMO_DIR / "templates"
CSS_PATH     = DEMO_DIR / "styles" / "theme.css"

# ── App Meta ──────────────────────────────────────────────────────────────────
APP_TITLE    = "VNExam AnomalyGuard"
APP_ICON     = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
APP_SUBTITLE = (
    "Hệ thống phân tích phổ điểm & phát hiện bất thường "
    "thi THPT Quốc Gia (2016–2026) · Apache Spark Pipeline"
)
PAGE_TITLE   = "VNExam AnomalyGuard — Kiểm Toán Thi THPT"

# ── Navigation items: (page_key, icon_material_key, display_label) ───────────
NAV_ITEMS = [
    ("tong_quan", ":material/space_dashboard:", "Tổng Quan"),
    ("thong_ke",  ":material/query_stats:", "Thống Kê Mô Tả"),
    ("zscore",    ":material/map:", "Multi-Subject Z-Score"),
    ("kmeans",    ":material/person_search:", "K-Means Thí Sinh"),
]

DEFAULT_PAGE = NAV_ITEMS[0][0]  # mặc định vào Tổng Quan

# ── ML / Analytics thresholds ─────────────────────────────────────────────────
Z_SCORE_THRESHOLD   = 3.0
KMEANS_K            = 4
KMEANS_PERCENTILE   = 99.5

# ── Scandal ground-truth years & provinces ────────────────────────────────────
SCANDAL_2018_PROVINCES = {"15", "26", "36"}
