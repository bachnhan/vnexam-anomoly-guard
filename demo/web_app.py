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
import views.tong_quan_page
import views.thong_ke_page
import views.kmeans_page
import views.zscore_page

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

    kpi               = extra.get("kpi", {})
    ground_truth      = extra.get("ground_truth", [])
    top_chart         = extra.get("top_chart", [])
    sota              = extra.get("sota", {})
    yearly_subjects   = extra.get("yearly_subjects", [])
    student_specimens = extra.get("student_specimens", [])
    zscore_2018       = extra.get("zscore_2018", [])

    active_page = render_sidebar(kpi)
    render_appbar(src)

    st.markdown('<div class="main-body">', unsafe_allow_html=True)

    if active_page == "tong_quan":
        views.tong_quan_page.render(prov_df, kpi)
    elif active_page == "thong_ke":
        views.thong_ke_page.render(prov_df, yearly_subjects)
    elif active_page == "kmeans":
        views.kmeans_page.render(student_df, kpi, student_specimens)
    elif active_page == "zscore":
        views.zscore_page.render(prov_df, ground_truth, zscore_2018)

    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
