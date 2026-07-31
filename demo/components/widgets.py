"""
components/widgets.py — Reusable UI building blocks.
Loads HTML from templates/ using string.Template.
No business logic — pure presentation.
"""
from __future__ import annotations

from pathlib import Path
from string import Template

import streamlit as st

from config import TEMPLATE_DIR


# ────────────────────────────────────────────────────────────────
# Template engine (private)
# ────────────────────────────────────────────────────────────────

_CACHE: dict[str, Template] = {}


def _load(name: str) -> Template:
    """Load and cache a Template from templates/<name>."""
    if name not in _CACHE:
        path = Path(TEMPLATE_DIR) / name
        _CACHE[name] = Template(path.read_text(encoding="utf-8"))
    return _CACHE[name]


def _render(name: str, **kwargs: object) -> str:
    """Render template with safe_substitute (unknown vars left as-is)."""
    return _load(name).safe_substitute(**kwargs)


# ────────────────────────────────────────────────────────────────
# Public widget API
# ────────────────────────────────────────────────────────────────

def ang_section(icon: str, title: str, subtitle: str = "") -> None:
    """Render an Angular-style section header with icon box."""
    st.markdown(
        _render("ang_section.html", icon=icon, title=title, subtitle=subtitle),
        unsafe_allow_html=True,
    )


def ang_divider() -> None:
    """Render a cyan gradient horizontal divider."""
    st.markdown('<div class="ang-divider"></div>', unsafe_allow_html=True)


def gls_alert(content: str, variant: str = "cyan") -> None:
    """
    Render a glassmorphism alert box.

    Parameters
    ----------
    content : HTML string for the alert body
    variant : 'red' | 'green' | 'amber' | 'cyan'
    """
    st.markdown(
        _render("alert.html", content=content, variant=variant),
        unsafe_allow_html=True,
    )


def glass_kpi(
    value: object,
    label: str,
    delta: str,
    color_class: str = "",
    accent_color: str = "rgba(0,188,212,0.5)",
) -> None:
    """Render a glassmorphism KPI metric card."""
    st.markdown(
        _render(
            "kpi_card.html",
            value=value,
            label=label,
            delta=delta,
            color_class=color_class,
            accent_color=accent_color,
        ),
        unsafe_allow_html=True,
    )


def sota_box(
    value: object,
    label: str,
    description: str,
    color: str = "#00BCD4",
) -> None:
    """Render a SOTA metric display box."""
    st.markdown(
        _render("sota_box.html", value=value, label=label,
                description=description, color=color),
        unsafe_allow_html=True,
    )


def pipeline_step(step_num: int, layer: str, description: str, file: str) -> None:
    """Render a numbered pipeline step card."""
    st.markdown(
        _render("pipeline_step.html", step_num=step_num, layer=layer,
                description=description, file=file),
        unsafe_allow_html=True,
    )


def ml_card(title: str, bullets: list[str], accent_color: str = "#00BCD4") -> None:
    """Render an ML algorithm description card with bullet list."""
    bullet_html = "".join(
        f'<div style="color:#546E7A;font-size:0.78rem;padding:2px 0;">· {b}</div>'
        for b in bullets
    )
    st.markdown(
        _render("ml_card.html", title=title, accent_color=accent_color,
                bullet_items=bullet_html),
        unsafe_allow_html=True,
    )


def gt_row(
    icon: str, incident: str, province_names: str,
    z_score_max: object, z_indicator: str, detected: bool,
) -> None:
    """Render one row of the Ground Truth table."""
    status = '<span class="ang-chip green"><i class="fa-solid fa-check" style="margin-right:4px;"></i>DETECTED</span>' if detected else '<span class="ang-chip red"><i class="fa-solid fa-xmark" style="margin-right:4px;"></i>MISSED</span>'
    st.markdown(
        _render(
            "gt_row.html",
            icon=icon, incident=incident, province_names=province_names,
            z_score_max=z_score_max, z_indicator=z_indicator, status=status,
        ),
        unsafe_allow_html=True,
    )
