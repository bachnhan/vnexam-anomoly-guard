#!/usr/bin/env python3
"""
web_app.py — VNExam AnomalyGuard Dashboard entry point.

Single responsibility: configure Streamlit, load data, dispatch to page.
Contains zero HTML, zero CSS, zero business logic.
"""
import sys
from pathlib import Path

import streamlit as st

# — ensure demo/ is on sys.path so relative imports work —
_DEMO_DIR = Path(__file__).parent
if str(_DEMO_DIR) not in sys.path:
    sys.path.insert(0, str(_DEMO_DIR))

from config import APP_ICON, PAGE_TITLE
from data.loader import load_data
from styles.theme import inject_css
from components.appbar import render_appbar
from components.sidebar import render_sidebar
import views.data_source_page
import views.kpi_page
import views.province_page
import views.students_page
import views.ground_truth_page
import views.sota_page

# ── Page config (must be first Streamlit call) ─────────────────────────────────
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    inject_css()

    with st.spinner(""):
        prov_df, student_df, yearly_df, src, extra = load_data()

    if src == "none":
        st.error("❌ Không tìm thấy dữ liệu. Kiểm tra dashboard_data.json.")
        return

    kpi          = extra.get("kpi", {})
    ground_truth = extra.get("ground_truth", [])
    top_chart    = extra.get("top_chart", [])
    sota         = extra.get("sota", {})

    render_appbar(src)
    page = render_sidebar(kpi)

    # ── Strategy / Page Dispatch ─────────────────────────────────────────────
    PAGE_MAP = {
        "datasource": lambda: views.data_source_page.render(),
        "kpi":        lambda: views.kpi_page.render(prov_df, yearly_df, kpi, top_chart),
        "province":   lambda: views.province_page.render(prov_df, top_chart),
        "students":   lambda: views.students_page.render(student_df),
        "ground":     lambda: views.ground_truth_page.render(prov_df, ground_truth),
        "sota":       lambda: views.sota_page.render(sota),
    }
    PAGE_MAP.get(page, PAGE_MAP["kpi"])()


if __name__ == "__main__":
    main()
