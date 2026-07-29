"""
pages/students_page.py — Student Outlier Analysis page.
"""
import pandas as pd
import streamlit as st

from components.widgets import ang_section, gls_alert
from data.loader import style_score


def render(student_df: pd.DataFrame) -> None:
    ang_section("👤", "K-Means Student Outliers",
                "Thí sinh lệch phổ điểm · Euclidean Distance > 99.5th percentile")

    gls_alert(
        "<b>Detection mechanism:</b> K-Means (K=4) clusters students by 6-subject score vector. "
        "Students with Euclidean distance to centroid exceeding 99.5th percentile are flagged. "
        "<span style='color:#FFA726;font-weight:700;'> → 54,325 students flagged (0.5% of 10.86M)</span>",
        variant="amber",
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        s_years = sorted(student_df["nam_thi"].dropna().unique().tolist())
        s_yr    = st.selectbox("📅 Year:", ["All"] + [str(int(y)) for y in s_years])

        has_ly  = "vat_ly"    in student_df.columns
        has_hoa = "hoa_hoc"   in student_df.columns
        has_anh = "ngoai_ngu" in student_df.columns
        avail   = ["All"]
        if has_ly:  avail.append("Math↑ + Physics↓")
        if has_hoa: avail.append("Math↑ + Chemistry↓")
        if has_anh: avail.append("Math↑ + English↓")
        fp = st.radio("Anomaly pattern:", avail)

    with col2:
        disp = student_df.copy()
        if s_yr != "All":
            disp = disp[disp["nam_thi"].astype(str) == s_yr]

        cond_map = {}
        if has_ly:  cond_map["Math↑ + Physics↓"]   = (disp["toan"] >= 9.0) & (disp["vat_ly"] <= 2.0)
        if has_hoa: cond_map["Math↑ + Chemistry↓"] = (disp["toan"] >= 9.0) & (disp["hoa_hoc"] <= 2.0)
        if has_anh: cond_map["Math↑ + English↓"]   = (disp["toan"] >= 9.0) & (disp["ngoai_ngu"] <= 2.0)
        if fp in cond_map:
            disp = disp[cond_map[fp]]

        show_s  = [c for c in [
            "sbd", "nam_thi", "ma_tinh", "toan", "vat_ly",
            "hoa_hoc", "ngoai_ngu", "ngu_van", "anomaly_score", "anomaly_pattern",
        ] if c in disp.columns]
        sc_cols = [c for c in ["toan", "vat_ly", "hoa_hoc", "ngoai_ngu", "ngu_van"]
                   if c in disp.columns]

        st.markdown(
            f'<div style="color:#00BCD4;font-size:0.8rem;font-weight:700;margin-bottom:8px;">'
            f'◈ {len(disp)} STUDENTS MATCHED · 🟢=score≥9.0 · 🔴=score≤2.0</div>',
            unsafe_allow_html=True,
        )
        st.dataframe(
            disp[show_s].head(30).style.map(style_score, subset=sc_cols),
            use_container_width=True, height=380,
        )

    gls_alert(
        "<b>Important:</b> Being flagged does NOT mean cheating — it is a "
        "<i>statistical signal</i> requiring further investigation by the examination authority.",
        variant="red",
    )
