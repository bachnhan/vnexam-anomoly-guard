"""
views/thong_ke_page.py — Thống Kê Mô Tả bằng Spark SQL.
Req 1a: Bảng điểm TB các môn theo năm.
Req 1b: Top 10 tỉnh điểm Toán cao nhất (total_students >= 5000).
Req 2a: Biểu đồ đường điểm TB KHTN vs KHXH.
"""
import pandas as pd
import streamlit as st

from components.widgets import ang_section, ang_divider, gls_alert
from data.loader import style_z


def render(prov_df: pd.DataFrame, yearly_subjects: list = None) -> None:

    # ── 1a: Bảng điểm TB các môn theo năm ──────────────────────────────────────
    ang_section(
        "📋", "Điểm Trung Bình Các Môn Theo Năm",
        "Spark SQL: GROUP BY nam_thi · AVG(toan), AVG(ngu_van), ... · 10.86M records"
    )

    if yearly_subjects:
        ys_df = pd.DataFrame(yearly_subjects)
        col_map = {
            "nam_thi":      "Năm",
            "avg_toan":     "Toán",
            "avg_nguvan":   "Ngữ Văn",
            "avg_ngoaingu": "Ngoại Ngữ",
            "avg_vatly":    "Vật Lý",
            "avg_hoahoc":   "Hóa Học",
            "avg_sinhhoc":  "Sinh Học",
            "avg_lichsu":   "Lịch Sử",
            "avg_dialy":    "Địa Lý",
            "avg_gdcd":     "GDCD",
            "avg_khtn":     "TB KHTN",
            "avg_khxh":     "TB KHXH",
        }
        display_cols = [c for c in col_map if c in ys_df.columns]
        ys_display = ys_df[display_cols].rename(columns=col_map)

        def style_subject(val):
            if not isinstance(val, (int, float)) or pd.isna(val):
                return "color:#546E7A;"
            if val >= 7.0:
                return "background:rgba(0,200,83,0.15);color:#69F0AE;font-weight:700;"
            if val <= 5.0:
                return "background:rgba(239,83,80,0.12);color:#EF9A9A;"
            return "color:#E2E8F0;"

        styled = ys_display.style.map(
            style_subject,
            subset=[c for c in ys_display.columns if c != "Năm"]
        ).format(
            {c: "{:.2f}" for c in ys_display.columns if c != "Năm"},
            na_rep="—"
        )
        st.dataframe(styled, use_container_width=True, height=430)
        st.caption(
            "🟢 Xanh: TB ≥ 7.0 · 🔴 Đỏ: TB ≤ 5.0 · "
            "⚠ 2018: Toán tăng đột biến 7.22 — trùng vụ gian lận Hà Giang/Sơn La/Hòa Bình · "
            "⚠ 2017: Toán 4.93 — đề khó nhất thập kỷ"
        )
    else:
        gls_alert("Dữ liệu yearly_subjects chưa có — cần export từ Spark pipeline.", variant="amber")

    ang_divider()

    # ── 1b: Top 10 tỉnh điểm Toán cao nhất ─────────────────────────────────────
    ang_section(
        "🏆", "Top 10 Tỉnh — Điểm Toán Cao Nhất",
        "Spark SQL: HAVING SUM(total_students) ≥ 5,000 · ORDER BY AVG(avg_toan) DESC · LIMIT 10"
    )

    if not prov_df.empty and "avg_toan" in prov_df.columns:
        top10 = (
            prov_df[prov_df["total_students"] >= 5000]
            .groupby("ma_tinh", as_index=False)
            .agg(
                ten_tinh=("ten_tinh", "first") if "ten_tinh" in prov_df.columns else None,
                total_students=("total_students", "sum"),
                avg_toan=("avg_toan", "mean"),
                z_score=("z_score", "mean"),
            )
            .dropna(subset=["avg_toan"])
            .sort_values("avg_toan", ascending=False)
            .head(10)
            .reset_index(drop=True)
        )
        top10.index = top10.index + 1
        top10["avg_toan"]       = top10["avg_toan"].round(2)
        top10["z_score"]        = top10["z_score"].round(2)
        top10["total_students"] = top10["total_students"].astype(int)
        rename = {"ma_tinh": "Mã Tỉnh", "total_students": "Tổng TS (10yr)",
                  "avg_toan": "Điểm Toán TB", "z_score": "Z-Score TB"}
        if "ten_tinh" in top10.columns:
            rename["ten_tinh"] = "Tên Tỉnh"
        top10 = top10.rename(columns=rename)
        st.dataframe(top10, use_container_width=True, height=400)
        st.caption(
            "Xếp hạng tính trên trung bình đa năm (2016–2026). "
            "Tổng TS = tổng thí sinh 10 năm."
        )
    else:
        gls_alert("Cột avg_toan chưa có trong Parquet — cần teammate thêm khi export.", variant="amber")

    ang_divider()

    # ── 2a: Biểu đồ đường KHTN vs KHXH ─────────────────────────────────────────
    ang_section(
        "📈", "Biến Động Phổ Điểm — KHTN vs KHXH",
        "Điểm TB khối KHTN (Toán+Lý+Hóa) và KHXH (Văn+Sử+Địa) · 2016–2026"
    )

    if yearly_subjects:
        chart_df = pd.DataFrame(yearly_subjects).set_index("nam_thi")[
            ["avg_khtn", "avg_khxh"]
        ].rename(columns={
            "avg_khtn": "KHTN — Toán+Lý+Hóa",
            "avg_khxh": "KHXH — Văn+Sử+Địa"
        })
        st.line_chart(chart_df)
        col_a, col_b = st.columns(2)
        with col_a:
            gls_alert(
                "<b>2018:</b> KHTN đột biến 6.32 — trùng vụ gian lận "
                "Hà Giang / Sơn La / Hòa Bình",
                variant="red",
            )
        with col_b:
            gls_alert(
                "<b>2020:</b> Cả 2 khối tăng đồng thời — "
                "đề thi COVID-19 dễ hơn, Bộ GD&ĐT điều chỉnh",
                variant="cyan",
            )
    else:
        gls_alert("Dữ liệu yearly_subjects chưa có.", variant="amber")
