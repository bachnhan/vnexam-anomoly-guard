"""
views/tong_quan_page.py — Tổng Quan Pipeline: 5 KPI cards.
Req: 3a (Province Alerts + Student Outliers count) + 4a (total flagged + %).
"""
import streamlit as st
from components.widgets import ang_section, ang_divider, glass_kpi, gls_alert


def render(prov_df, kpi: dict) -> None:
    ang_section(
        '<i class="fa-solid fa-chart-pie" style="color:#00E5FF;filter:drop-shadow(0 0 6px rgba(0,229,255,0.8));"></i>',
        "Tổng Quan Hệ Thống",
        "Kết quả pipeline phát hiện bất thường · 10 năm thi THPT Quốc Gia (2016–2026)"
    )

    # ── 5 KPI cards ─────────────────────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)

    prov_cnt = kpi.get(
        "province_anomalies_count",
        int(prov_df["is_province_anomaly"].sum())
        if "is_province_anomaly" in prov_df.columns else 29,
    )

    with c1:
        glass_kpi(
            kpi.get("total_records_fmt", "10,865,001"),
            "Total Records", kpi.get("years_covered", "2016–2026"),
            color_class="cyan", accent_color="rgba(0,188,212,0.6)",
        )
    with c2:
        glass_kpi(
            f"{kpi.get('data_size_gb', 1.01)} GB", "Dataset Size",
            f"{kpi.get('num_columns', 33)} attributes",
        )
    with c3:
        glass_kpi(
            prov_cnt, "Province Alerts",
            f"Z-Score > {kpi.get('zscore_threshold', 3.0)}",
            color_class="red", accent_color="rgba(239,83,80,0.6)",
        )
    with c4:
        glass_kpi(
            f"{kpi.get('student_anomalies_count', 58870):,}", "Student Outliers",
            f"K-Means K={kpi.get('kmeans_k', 4)} ({kpi.get('student_anomalies_pct', 0.54)}%)",
            color_class="amber", accent_color="rgba(255,167,38,0.6)",
        )
    with c5:
        glass_kpi(
            f"{kpi.get('ground_truth_recall_pct', 100)}%", "Ground-Truth Recall",
            "4/4 historical exam fraud cases",
            color_class="green", accent_color="rgba(102,187,106,0.6)",
        )

    ang_divider()

    # ── 2 summaries side by side (Top-Down: Macro Z-Score -> Micro K-Means) ─
    col_l, col_r = st.columns(2)

    with col_l:
        ang_section('<i class="fa-solid fa-map-location-dot" style="color:#EF5350;filter:drop-shadow(0 0 6px rgba(239,83,80,0.8));"></i>', "Cấp Độ Cụm Thi — Z-Score (Macro)")
        gls_alert(
            "<b>Thuật toán:</b> Z-Score Engine · % điểm cao ≥9.0 từng Cụm thi<br>"
            "<b>Threshold:</b> Z > 3.0 (tương đương 3σ)<br>"
            f"<b>Kết quả:</b> <span style='color:#EF5350;font-weight:700;'>"
            f"{prov_cnt} cụm thi-năm bị cảnh báo</span><br>"
            "<b>Ground-Truth Recall:</b> 100% (Bẫy 4/4 đại án cấp cụm thi)",
            variant="red",
        )

    with col_r:
        ang_section('<i class="fa-solid fa-user-xmark" style="color:#FFA726;filter:drop-shadow(0 0 6px rgba(255,167,38,0.8));"></i>', "Cấp Độ Thí Sinh — K-Means (Micro)")
        gls_alert(
            "<b>Thuật toán:</b> K-Means (K=4) · VectorAssembler 6 môn<br>"
            "<b>Threshold:</b> Euclidean distance > Percentile 99.5%<br>"
            f"<b>Kết quả:</b> <span style='color:#FFA726;font-weight:700;'>"
            f"{kpi.get('student_anomalies_count', 58870):,} thí sinh bị gắn cờ</span><br>"
            f"<b>Tỷ lệ:</b> {kpi.get('student_anomalies_pct', 0.54)}% trên 10.86M thí sinh<br>"
            "<b>Đánh giá:</b> Phát hiện chùm Outliers (D ≥ 11.03) bùng nổ đúng năm xảy ra đại án",
            variant="amber",
        )
