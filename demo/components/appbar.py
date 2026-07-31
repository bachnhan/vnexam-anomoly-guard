"""
components/appbar.py — Application top bar renderer.
Single responsibility: render header + data source badge.
"""
import streamlit as st

from config import APP_TITLE, APP_SUBTITLE
from components.widgets import _render


def render_appbar(src: str) -> None:
    """Render the Angular-style app bar and data-source chip."""
    st.markdown(
        _render("appbar.html", app_title=APP_TITLE, app_subtitle=APP_SUBTITLE),
        unsafe_allow_html=True,
    )
    chip_html = (
        '<div style="text-align:right;padding:8px 0 0 0;">'
        '<span class="ang-chip green"><i class="fa-solid fa-check" style="margin-right:4px;"></i>Parquet Pipeline</span>'
        '</div>'
        if src == "parquet"
        else '<span class="ang-chip">◈ JSON Demo Mode</span>'
    )
    st.markdown(chip_html, unsafe_allow_html=True)
    st.write("")
