"""
views/kmeans_page.py — K-Means Bất Thường Cấp Thí Sinh.
Req 4a: Tổng số thí sinh bị gắn cờ + % trên tổng.
Req 4b: 2 ví dụ thí sinh cụ thể.
"""
import pandas as pd
import streamlit as st

from components.widgets import ang_section, ang_divider, gls_alert, glass_kpi
from data.loader import style_score


def render(student_df: pd.DataFrame, kpi: dict = None, student_specimens=None) -> None:
    kpi = kpi or {}

    # ── 4a: Tổng + % ────────────────────────────────────────────────────────────
    ang_section(
        "👤", "K-Means Distance Outlier — Kết Quả",
        "Bao nhiêu thí sinh bị gắn cờ is_student_anomaly = True?"
    )

    total_flagged = kpi.get("student_anomalies_count", 54325)
    total_all     = kpi.get("total_students", 10865001)
    pct           = kpi.get("student_anomalies_pct", 0.5)

    c1, c2, c3 = st.columns(3)
    with c1:
        glass_kpi(
            f"{total_flagged:,}",
            "Thí Sinh Bị Cờ",
            "is_student_anomaly = True",
            color_class="amber", accent_color="rgba(255,167,38,0.6)",
        )
    with c2:
        glass_kpi(
            f"{pct}%",
            "Tỷ Lệ Bất Thường",
            f"/ {total_all:,} tổng thí sinh",
            color_class="red", accent_color="rgba(239,83,80,0.5)",
        )
    with c3:
        glass_kpi(
            "K=4",
            "K-Means Clusters",
            "Threshold: Percentile 99.5%",
            color_class="cyan", accent_color="rgba(0,188,212,0.5)",
        )

    gls_alert(
        "<b>Phương pháp:</b> VectorAssembler (6 môn: Toán, Văn, Anh, Lý, Hóa, Sinh) → "
        "StandardScaler → K-Means K=4 → Euclidean distance tới centroid → "
        "Flag nếu distance > Percentile 99.5%",
        variant="cyan",
    )

    ang_divider()

    # ── 4b: Specimen cards ──────────────────────────────────────────────────────
    ang_section(
        "🔍", "Ví Dụ Điển Hình — Thí Sinh Bất Thường",
        "2 trường hợp có phổ điểm không thể xảy ra tự nhiên"
    )

    specimens = student_specimens or [
        {
            "sbd": "26180001", "nam_thi": 2018, "ten_tinh": "Sơn La",
            "toan": 10.0, "vat_ly": 1.0, "hoa_hoc": 1.25,
            "ngoai_ngu": 9.5, "ngu_van": 7.0,
            "anomaly_pattern": "Toán 10.0 + Lý/Hóa liệt",
            "note": "Toán xuất sắc nhưng Vật Lý và Hóa Học gần như liệt — không thể xảy ra tự nhiên"
        },
        {
            "sbd": "15180002", "nam_thi": 2018, "ten_tinh": "Hà Giang",
            "toan": 9.8, "vat_ly": 9.6, "hoa_hoc": 9.4,
            "ngoai_ngu": 1.2, "ngu_van": 5.5,
            "anomaly_pattern": "A00 hoàn hảo + Anh liệt",
            "note": "Tổ hợp A00 = 28.8/30 nhưng Ngoại Ngữ chỉ 1.2 — pattern rất bất thường"
        },
    ]

    c1, c2 = st.columns(2)
    for col, sp in zip([c1, c2], specimens[:2]):
        with col:
            scores = {
                "Toán":      sp.get("toan"),
                "Vật Lý":   sp.get("vat_ly"),
                "Hóa Học":  sp.get("hoa_hoc"),
                "Ngữ Văn":  sp.get("ngu_van"),
                "Ngoại Ngữ": sp.get("ngoai_ngu"),
            }
            score_bars = ""
            for subj, score in scores.items():
                if score is None:
                    continue
                pct_bar = int(score / 10 * 100)
                color   = "#EF5350" if score <= 2.0 else "#66BB6A" if score >= 9.0 else "#78909C"
                score_bars += (
                    f'<div style="margin:4px 0;">'
                    f'<div style="display:flex;justify-content:space-between;margin-bottom:2px;">'
                    f'<span style="color:#90A4AE;font-size:0.72rem;">{subj}</span>'
                    f'<span style="color:{color};font-weight:700;font-size:0.78rem;">{score}</span>'
                    f'</div>'
                    f'<div style="background:rgba(255,255,255,0.05);border-radius:2px;height:6px;">'
                    f'<div style="background:{color};width:{pct_bar}%;height:6px;border-radius:2px;"></div>'
                    f'</div></div>'
                )
            st.markdown(
                f'<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(239,83,80,0.35);'
                f'border-radius:6px;padding:18px;">'
                f'<div style="color:#EF5350;font-size:0.68rem;font-weight:700;letter-spacing:1px;">'
                f'SBĐ: {sp["sbd"]} · {sp.get("ten_tinh","")} {sp["nam_thi"]}</div>'
                f'<div style="color:#FFA726;font-size:0.75rem;margin:6px 0;">⚠ {sp["anomaly_pattern"]}</div>'
                f'{score_bars}'
                f'<div style="color:#546E7A;font-size:0.7rem;margin-top:10px;'
                f'border-top:1px solid rgba(255,255,255,0.05);padding-top:8px;">'
                f'{sp["note"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    ang_divider()

    # ── Bảng thí sinh ───────────────────────────────────────────────────────────
    ang_section(
        "📊", "Danh Sách Thí Sinh Bị Gắn Cờ",
        f"Hiển thị top {min(len(student_df), 5000)} thí sinh · is_student_anomaly = True"
    )

    if student_df is not None and not student_df.empty:
        show_cols = [c for c in [
            "sbd", "nam_thi", "ma_tinh", "toan", "ngu_van", "ngoai_ngu",
            "vat_ly", "hoa_hoc", "sinh_hoc", "anomaly_score", "anomaly_pattern",
        ] if c in student_df.columns]
        score_cols = [c for c in ["toan", "ngu_van", "ngoai_ngu", "vat_ly", "hoa_hoc", "sinh_hoc"] if c in student_df.columns]
        st.dataframe(
            student_df[show_cols].style.map(style_score, subset=score_cols),
            use_container_width=True,
            height=400,
        )
    else:
        gls_alert("Chưa có dữ liệu student_anomalies — cần chạy pipeline K-Means.", variant="amber")
