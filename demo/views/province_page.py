"""
pages/province_page.py — Province Z-Score Analysis page.
"""
import pandas as pd
import streamlit as st

from components.widgets import ang_section, ang_divider, gls_alert
from data.loader import style_z


def render(prov_df: pd.DataFrame, top_chart: list) -> None:
    ang_section("🗺️", "Province Z-Score Alerts",
                "Cảnh báo bất thường cấp tỉnh thành · Z-Score Engine")

    col_f, col_t = st.columns([1, 3])
    with col_f:
        years   = sorted(prov_df["nam_thi"].dropna().unique().tolist())
        sel_yr  = st.selectbox("📅 Năm thi:", ["All"] + [str(int(y)) for y in years])
        z_thr   = st.slider("Z-Score threshold:", 2.0, 5.0, 3.0, 0.1)
        gls_alert(
            "<b>Legend</b><br>"
            "🔴 Z ≥ 4.0 Critical<br>"
            "🟠 Z ≥ 3.0 Warning<br>"
            "YoY = % change vs prev year",
            variant="cyan",
        )

    with col_t:
        filtered = prov_df[prov_df["z_score"] >= z_thr].copy()
        if sel_yr != "All":
            filtered = filtered[filtered["nam_thi"].astype(str) == sel_yr]
        filtered = filtered.sort_values("z_score", ascending=False)

        st.markdown(
            f'<div style="color:#00BCD4;font-size:0.8rem;font-weight:700;margin-bottom:8px;">'
            f'◈ {len(filtered)} PROVINCE CLUSTERS FLAGGED (Z ≥ {z_thr})</div>',
            unsafe_allow_html=True,
        )
        if filtered.empty:
            st.info("No data matching filter.")
        else:
            show_cols = [c for c in [
                "nam_thi", "ma_tinh", "total_students", "high_math_pct",
                "z_math", "z_a00", "z_bio", "z_score", "yoy_math_delta_pct",
            ] if c in filtered.columns]
            z_cols = [c for c in ["z_math", "z_a00", "z_bio", "z_score"] if c in filtered.columns]
            st.dataframe(
                filtered[show_cols].style.map(style_z, subset=z_cols),
                use_container_width=True, height=340,
            )

    ang_divider()
    ang_section("📊", "Top 15 Clusters — Z-Score Ranking")
    if top_chart:
        tc_df = pd.DataFrame(top_chart).set_index("label")[["z_score"]]
        st.bar_chart(tc_df)
    else:
        tp  = prov_df.sort_values("z_score", ascending=False).head(15)
        bd  = tp.set_index(tp["nam_thi"].astype(str) + "_" + tp["ma_tinh"].astype(str))[["z_score"]]
        st.bar_chart(bd)
    st.caption("2018: Hà Giang(15) Z=3.76 · Sơn La(26) Z=4.13 · Hòa Bình(36) Z=4.43")
