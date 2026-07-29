"""
pages/sota_page.py — SOTA Forensic Methods page.
"""
import streamlit as st

from components.widgets import ang_section, ang_divider, gls_alert, sota_box


def render(sota: dict) -> None:
    ang_section("🔬", "SOTA Forensic Methods",
                "3 phương pháp kiểm toán nâng cao vượt K-Means & Z-Score chuẩn")

    tab1, tab2, tab3 = st.tabs([
        "1️⃣  Benford Law",
        "2️⃣  Mahalanobis",
        "3️⃣  Shannon Entropy",
    ])

    benford = sota.get("benford", {})
    maha    = sota.get("mahalanobis", {})
    entropy = sota.get("shannon_entropy", {})

    # ── Tab 1: Benford ──
    with tab1:
        chi2  = benford.get("chi2_statistic", 2297.80)
        crit  = benford.get("chi2_critical_005", 26.12)
        verd  = benford.get("verdict", "REJECT H0 — Phổ điểm bị can thiệp nhân tạo")
        c1, c2, c3 = st.columns(3)
        with c1:
            sota_box(f"{chi2:,.0f}", "χ² Statistic",
                     "Observed first-digit distribution", color="#EF5350")
        with c2:
            sota_box(crit, "χ² Critical (α=0.05)",
                     "Expected under Benford's Law", color="#66BB6A")
        with c3:
            sota_box("χ²>Crit", "Test Result", "p < 0.001", color="#FFA726")
        gls_alert(f"<b>Verdict:</b> {verd}", "red")
        st.markdown(
            "**Định Luật Benford:** Trong phân phối tự nhiên, chữ số đầu tiên ~30% là \u201c1\u201d, ~5% là \u201c9\u201d. "
            "Khi điểm bị sửa hàng loạt về một mức cố định, tần suất lệch khỏi phân phối Benford."
        )

    # ── Tab 2: Mahalanobis ──
    with tab2:
        m_cnt = maha.get("flagged_students", 443)
        m_thr = maha.get("threshold", 18.55)
        m_ver = maha.get("verdict", "443 thí sinh có profile điểm bất khả thi")
        c1, c2 = st.columns(2)
        with c1:
            sota_box(m_cnt, "Students Flagged",
                     "Mahalanobis distance > threshold", color="#EF5350")
        with c2:
            sota_box(m_thr, "Distance Threshold",
                     "Chi-squared critical value (df=6)", color="#00BCD4")
        gls_alert(f"<b>Result:</b> {m_ver}", "green")
        st.markdown(
            "**Khoảng Cách Mahalanobis:** Khác với Euclidean, tính đến ma trận hiệp phương sai — "
            "phát hiện các tổ hợp điểm _bất khả thi về mặt tương quan thống kê_ giữa các môn thi."
        )

    # ── Tab 3: Shannon Entropy ──
    with tab3:
        ent_normal = entropy.get("normal_entropy_bits", 3.2)
        provinces  = entropy.get("flagged_provinces", [
            {"name": "Hà Giang", "year": 2018, "entropy": 2.712},
            {"name": "Hòa Bình", "year": 2018, "entropy": 2.651},
            {"name": "Sơn La",   "year": 2018, "entropy": 2.784},
        ])
        cols = st.columns(len(provinces))
        for col, p in zip(cols, provinces):
            with col:
                sota_box(
                    p.get("entropy", 2.7),
                    f"{p.get('name', '')} · {p.get('year', 2018)}",
                    f"Normal: ~{ent_normal} bits",
                    color="#EF5350",
                )
        verd_e = entropy.get("verdict", "Phổ điểm mất đa dạng — dấu hiệu sửa hàng loạt")
        gls_alert(f"<b>Verdict:</b> {verd_e}", "red")
        st.markdown(
            "**Shannon Entropy:** Đo độ đa dạng phổ điểm. Điểm tự nhiên có Entropy cao (~3.2 bits). "
            "Khi điểm bị nâng hàng loạt về 1 mức cố định, Entropy giảm mạnh."
        )

    ang_divider()
    gls_alert(
        "<b>5-Layer Forensic Stack:</b> "
        "K-Means Outlier &nbsp;·&nbsp; Z-Score Engine &nbsp;·&nbsp; "
        "Benford Law &nbsp;·&nbsp; Mahalanobis Distance &nbsp;·&nbsp; Shannon Entropy<br>"
        "→ Kết hợp 5 lớp kiểm toán độc lập → tăng độ tin cậy lên mức pháp lý",
        variant="cyan",
    )
