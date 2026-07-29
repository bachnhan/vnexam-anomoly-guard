"""
components/sidebar.py — Angular Material Navigation Sidebar.
Single responsibility: render the sidebar and return the active page key.
"""
import streamlit as st

from config import NAV_ITEMS, DEFAULT_PAGE
from components.widgets import _render


def render_sidebar(kpi: dict) -> str:
    """
    Render the Angular Material nav list in the sidebar.

    Returns
    -------
    str : active page key (e.g. 'kpi', 'province', ...)
    """
    # Brand / Logo
    st.sidebar.markdown(
        _render("nav_brand.html"),
        unsafe_allow_html=True,
    )

    # Session state init
    if "page" not in st.session_state:
        st.session_state.page = DEFAULT_PAGE

    # Navigation buttons (styled as Angular nav list items via CSS)
    for key, icon, label in NAV_ITEMS:
        is_active = st.session_state.page == key
        btn_text  = f"{icon}  {'▸ ' if is_active else ''}{label}"
        if st.sidebar.button(btn_text, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.rerun()

    # System info footer
    proc_t  = kpi.get("processing_time_sec", 71)
    nodes   = kpi.get("cluster_nodes", 3)
    data_gb = kpi.get("data_size_gb", 1.01)
    st.sidebar.markdown(
        '<hr style="border:none;border-top:1px solid rgba(0,188,212,0.1);margin:12px 0;">',
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        _render("sidebar_info.html", workers=nodes - 1,
                data_gb=data_gb, proc_t=proc_t),
        unsafe_allow_html=True,
    )

    return st.session_state.page
