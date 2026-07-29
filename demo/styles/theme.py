"""
styles/theme.py — Injects Angular Material + Glassmorphism CSS into Streamlit.
Reads pure CSS from theme.css — Python contains zero styling rules.
"""
import streamlit as st
from config import CSS_PATH


def inject_css() -> None:
    """Read theme.css and inject into Streamlit page."""
    css_text = CSS_PATH.read_text(encoding="utf-8")
    st.markdown(f"<style>{css_text}</style>", unsafe_allow_html=True)
