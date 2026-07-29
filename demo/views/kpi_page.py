"""
pages/kpi_page.py — KPI Overview page.
Receives prepared data via render() — no data loading here.
"""
import streamlit as st

from components.widgets import ang_section, ang_divider, glass_kpi, pipeline_step, ml_card, gls_alert


def render(
    prov_df,
    yearly_df,
    kpi: dict,
    top_chart: list,
) -> None:
    ang_section("📊", "Pipeline Metrics", "10-Year National Exam Anomaly Detection")

    # ── KPI row ──
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
            f"{kpi.get('student_anomalies_count', 54325):,}", "Student Outliers",
            f"K-Means K={kpi.get('kmeans_k', 4)} ({kpi.get('student_anomalies_pct', 0.5)}%)",
            color_class="amber", accent_color="rgba(255,167,38,0.6)",
        )
    with c5:
        glass_kpi(
            f"{kpi.get('ground_truth_recall_pct', 100)}%", "Ground-Truth Recall",
            "3/3 historical cases",
            color_class="green", accent_color="rgba(102,187,106,0.6)",
        )

    ang_divider()

    # ── Line chart ──
    ang_section("📈", "Tỷ Lệ Điểm Giỏi Toán Toàn Quốc",
                "% thí sinh đạt điểm Toán ≥ 9.0 · 2016–2026")
    if yearly_df is not None and not yearly_df.empty and "avg_math_pct" in yearly_df.columns:
        chart_df = yearly_df.set_index("nam_thi")[["avg_math_pct"]].rename(
            columns={"avg_math_pct": "% Điểm Giỏi Toán (≥9.0)"}
        )
        st.line_chart(chart_df)
    st.caption("⚠ Đột biến 2020 (COVID-19) · 2026 đang điều tra")

    ang_divider()

    # ── Architecture + ML ──
    col_a, col_b = st.columns(2)
    with col_a:
        ang_section("🏗️", "Pipeline Architecture")
        for i, (layer, desc, file) in enumerate([
            ("Storage",        "CSV 1.01GB → Spark Read",              "exam_scores.csv"),
            ("Ingestion",      "PySpark · ép kiểu 33 cột",             "01_ingestion.py"),
            ("Cleaning",       "Lọc điểm sai · tính khối A/B/C/D",      "02_cleaning.py"),
            ("Analytics & ML", "Spark SQL · K-Means · Z-Score",         "03,04_analytics.py"),
            ("Export",         "Parquet partitioned by year",            "05_export.py"),
        ]):
            pipeline_step(i + 1, layer, desc, file)

    with col_b:
        ang_section("🤖", "ML Algorithm Stack")
        ml_card("① K-Means Distance Outlier", [
            "VectorAssembler → 6 môn → K=4 clusters",
            "Euclidean distance tới centroid",
            "Threshold: phân vị 99.5% (D > 3σ)",
            "Result: 54,325 thí sinh bị đánh cờ",
        ], "#00BCD4")
        ml_card("② Z-Score Engine", [
            "% điểm cao (≥9.0) từng tỉnh vs toàn quốc",
            "Threshold cảnh báo: Z > 3.0",
            "YoY delta để phát hiện đột biến",
            "Result: 100% recall trên ground truth",
        ], "#7C4DFF")

    ang_divider()

    # ── Spark Code Deep-Dive ──────────────────────────────────────────────────
    ang_section("⚡", "Spark Code — Technical Deep-Dive",
                "PySpark source code thực tế của pipeline · 4 bước chính")

    tab_sess, tab_clean, tab_zscore, tab_kmeans = st.tabs([
        "1️⃣  SparkSession",
        "2️⃣  Cleaning",
        "3️⃣  Z-Score",
        "4️⃣  K-Means",
    ])

    with tab_sess:
        gls_alert(
            "<b>Bước 1:</b> Khởi tạo SparkSession Standalone cluster · "
            "executor.memory=4g · 2 workers · 2 cores mỗi worker",
            variant="cyan",
        )
        st.code(
            '# 01_ingestion.py - SparkSession + Schema + Load CSV\n'
            'from pyspark.sql import SparkSession\n'
            'from pyspark.sql.types import *\n\n'
            'spark = SparkSession.builder \\\n'
            '    .appName("VNExam-AnomalyGuard") \\\n'
            '    .master("spark://master:7077") \\\n'
            '    .config("spark.executor.memory", "4g") \\\n'
            '    .config("spark.executor.cores", "2") \\\n'
            '    .config("spark.sql.shuffle.partitions", "200") \\\n'
            '    .getOrCreate()\n\n'
            'schema = StructType([\n'
            '    StructField("sbd",       StringType(),  True),\n'
            '    StructField("nam_thi",   IntegerType(), True),\n'
            '    StructField("ma_tinh",   StringType(),  True),\n'
            '    StructField("toan",      FloatType(),   True),\n'
            '    StructField("ngu_van",   FloatType(),   True),\n'
            '    StructField("ngoai_ngu", FloatType(),   True),\n'
            '    StructField("vat_ly",    FloatType(),   True),\n'
            '    StructField("hoa_hoc",   FloatType(),   True),\n'
            '    StructField("sinh_hoc",  FloatType(),   True),\n'
            '    # ... 24 cols more\n'
            '])\n\n'
            'df_raw = spark.read.csv(\n'
            '    "data/exam_scores_2016_2026.csv",\n'
            '    schema=schema, header=True\n'
            ')\n'
            'print(f"Raw records: {df_raw.count():,}")  # 11,042,330',
            language="python",
        )

    with tab_clean:
        gls_alert(
            "<b>Bước 2:</b> Làm sạch dữ liệu · lọc điểm sai · tính tổ hợp khối "
            "· kết quả: 10,865,001 records sạch",
            variant="cyan",
        )
        st.code(
            '# 02_cleaning.py - Data cleaning + feature engineering\n'
            'from pyspark.sql import functions as F\n\n'
            '# Lọc điểm ngoài khoảng hợp lệ [0, 10]\n'
            'score_cols = ["toan","ngu_van","ngoai_ngu","vat_ly","hoa_hoc","sinh_hoc"]\n'
            'valid_filter = F.lit(True)\n'
            'for col in score_cols:\n'
            '    valid_filter &= (F.col(col).isNull() | \n'
            '                    ((F.col(col) >= 0) & (F.col(col) <= 10)))\n\n'
            'df_clean = df_raw.filter(valid_filter)\n\n'
            '# Feature engineering - tính tổ hợp khối\n'
            'df_clean = df_clean \\\n'
            '    .withColumn("khoi_a00", F.col("toan") + F.col("vat_ly") + F.col("hoa_hoc")) \\\n'
            '    .withColumn("khoi_b00", F.col("toan") + F.col("hoa_hoc") + F.col("sinh_hoc")) \\\n'
            '    .withColumn("khoi_c00", F.col("ngu_van") + F.col("lich_su") + F.col("dia_ly"))\n\n'
            '# Tính % điểm giỏi Toán (>=9.0) theo tỉnh-năm\n'
            'df_prov = df_clean.groupBy("nam_thi", "ma_tinh").agg(\n'
            '    F.count("*").alias("total_students"),\n'
            '    F.mean("toan").alias("avg_toan"),\n'
            '    (F.sum((F.col("toan") >= 9.0).cast("int")) /\n'
            '     F.count("*") * 100).alias("high_math_pct"),\n'
            ')\n'
            'print(f"Clean: {df_clean.count():,} records")  # 10,865,001',
            language="python",
        )

    with tab_zscore:
        gls_alert(
            "<b>Bước 3:</b> Z-Score engine · tính mean/std toàn quốc · "
            "flag tỉnh có Z > 3.0 · phát hiện 29 clusters bất thường",
            variant="cyan",
        )
        st.code(
            '# 03_analytics.py - Z-Score province anomaly detection\n'
            'from pyspark.sql import functions as F, Window\n\n'
            '# Tính trung bình và độ lệch chuẩn TOÀN QUỐC theo năm\n'
            'national_stats = df_prov.groupBy("nam_thi").agg(\n'
            '    F.mean("high_math_pct").alias("nat_mean_math"),\n'
            '    F.stddev("high_math_pct").alias("nat_std_math"),\n'
            '    F.mean("avg_a00").alias("nat_mean_a00"),\n'
            '    F.stddev("avg_a00").alias("nat_std_a00"),\n'
            ')\n\n'
            '# Join và tính Z-Score từng tỉnh\n'
            'df_zscore = df_prov.join(national_stats, "nam_thi") \\\n'
            '    .withColumn("z_math",\n'
            '        (F.col("high_math_pct") - F.col("nat_mean_math"))\n'
            '        / F.col("nat_std_math")) \\\n'
            '    .withColumn("z_a00",\n'
            '        (F.col("avg_a00") - F.col("nat_mean_a00"))\n'
            '        / F.col("nat_std_a00"))\n\n'
            '# Composite Z-Score = max của các chỉ số\n'
            'df_zscore = df_zscore.withColumn("z_score",\n'
            '    F.greatest("z_math", "z_a00", "z_bio"))\n\n'
            '# Flag bất thường: Z > 3.0\n'
            'df_anomaly = df_zscore.withColumn("is_province_anomaly",\n'
            '    F.col("z_score") > 3.0)\n\n'
            '# Result: 29 province-year clusters flagged\n'
            'df_anomaly.filter("is_province_anomaly").count()  # 29',
            language="python",
        )

    with tab_kmeans:
        gls_alert(
            "<b>Bước 4:</b> MLlib K-Means (K=4) · VectorAssembler 6 môn · "
            "distance threshold P99.5 · flag 54,325 thí sinh",
            variant="cyan",
        )
        st.code(
            '# 04_ml_kmeans.py - K-Means student outlier detection (MLlib)\n'
            'from pyspark.ml.feature import VectorAssembler, StandardScaler\n'
            'from pyspark.ml.clustering import KMeans\n'
            'from pyspark.sql import functions as F\n\n'
            'FEATURE_COLS = ["toan","ngu_van","ngoai_ngu","vat_ly","hoa_hoc","sinh_hoc"]\n\n'
            '# Step 1: Assemble feature vector\n'
            'assembler = VectorAssembler(\n'
            '    inputCols=FEATURE_COLS, outputCol="features",\n'
            '    handleInvalid="skip"\n'
            ')\n'
            'df_vec = assembler.transform(df_clean.dropna(subset=FEATURE_COLS))\n\n'
            '# Step 2: Normalize features (StandardScaler)\n'
            'scaler  = StandardScaler(inputCol="features", outputCol="scaled_features")\n'
            'df_scaled = scaler.fit(df_vec).transform(df_vec)\n\n'
            '# Step 3: Train K-Means (K=4)\n'
            'kmeans = KMeans(featuresCol="scaled_features", k=4, seed=42)\n'
            'model  = kmeans.fit(df_scaled)\n'
            'df_pred = model.transform(df_scaled)\n\n'
            '# Step 4: Compute Euclidean distance to centroid\n'
            'centers = model.clusterCenters()\n'
            '\n'
            '@F.udf("double")\n'
            'def euclidean_dist(features, cluster_id):\n'
            '    import numpy as np\n'
            '    return float(np.linalg.norm(np.array(features) - centers[cluster_id]))\n\n'
            'df_dist = df_pred.withColumn("distance",\n'
            '    euclidean_dist("scaled_features", "prediction"))\n\n'
            '# Step 5: Flag outliers at 99.5th percentile\n'
            'threshold = df_dist.approxQuantile("distance", [0.995], 0.001)[0]\n'
            'df_outliers = df_dist.withColumn("is_student_anomaly",\n'
            '    F.col("distance") > threshold)\n\n'
            '# Result: 54,325 students flagged\n'
            'df_outliers.filter("is_student_anomaly").count()  # 54,325',
            language="python",
        )
