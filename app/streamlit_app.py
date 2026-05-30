"""
Streamlit Dashboard — Customer Segmentation (RFM + KMeans)
==========================================================
Hiển thị kết quả phân cụm khách hàng dựa trên mô hình KMeans
đã train với dữ liệu RFM (Recency, Frequency, Monetary).

Chạy:
    cd <project_root>
    streamlit run app/streamlit_app.py
"""

import sys
from pathlib import Path

# ---------- path setup so `src.*` imports work ----------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.models.kmeans_segmentor import KMeansSegmentor

# ================================================================
# Constants & Configuration
# ================================================================
SEGMENTS_PATH = PROJECT_ROOT / "data" / "processed" / "rfm_segments.csv"
RFM_TABLE_PATH = PROJECT_ROOT / "data" / "processed" / "rfm_table.csv"

# Colour palette — one per segment (ordered by "value")
SEGMENT_COLORS = {
    "Champions": "#6C5CE7",
    "Loyal Customers": "#00B894",
    "Potential Loyalists": "#0984E3",
    "At Risk": "#FDCB6E",
    "Lost Customers": "#D63031",
}

# Fallback colours for extra segments
_EXTRA_COLORS = ["#E17055", "#74B9FF", "#A29BFE", "#55EFC4", "#FAB1A0"]


def _color_for(segment: str) -> str:
    if segment in SEGMENT_COLORS:
        return SEGMENT_COLORS[segment]
    idx = hash(segment) % len(_EXTRA_COLORS)
    return _EXTRA_COLORS[idx]


# ================================================================
# Page Config
# ================================================================
st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ================================================================
# Custom CSS — premium dark-mode look
# ================================================================
st.markdown(
    """
<style>
/* ---------- global ---------- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="st-"] {
    font-family: 'Inter', sans-serif;
}

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
}
section[data-testid="stSidebar"] * {
    color: #e0e0e0 !important;
}

/* ---------- metric cards ---------- */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #667eea11, #764ba211);
    border: 1px solid #667eea33;
    border-radius: 12px;
    padding: 16px 20px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
}
div[data-testid="stMetric"] label {
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-size: 0.75rem;
}

/* ---------- tabs ---------- */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0;
    padding: 10px 24px;
    font-weight: 600;
}

/* ---------- header ---------- */
.dashboard-header {
    text-align: center;
    padding: 1.5rem 0 0.5rem;
}
.dashboard-header h1 {
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
}
.dashboard-header p {
    opacity: 0.7;
    font-size: 1rem;
}

/* ---------- segment badge ---------- */
.segment-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.85rem;
    color: #fff;
}
</style>
""",
    unsafe_allow_html=True,
)

# ================================================================
# Data Loading (cached)
# ================================================================


@st.cache_data(show_spinner="Đang tải dữ liệu…")
def load_data() -> pd.DataFrame:
    """Load the pre-computed RFM + segment CSV."""
    df = pd.read_csv(SEGMENTS_PATH)
    return df


@st.cache_data(show_spinner="Đang tải bảng RFM…")
def load_rfm_table() -> pd.DataFrame | None:
    if RFM_TABLE_PATH.exists():
        return pd.read_csv(RFM_TABLE_PATH)
    return None


# ================================================================
# KMeans Model (cached)
# ================================================================


@st.cache_resource(show_spinner="Đang huấn luyện lại mô hình KMeans…")
def get_trained_model(n_clusters: int) -> KMeansSegmentor:
    """Re-fit the KMeans model so we can predict new customers."""
    df = load_data()
    X = df[["Recency", "Frequency", "Monetary"]].values
    segmentor = KMeansSegmentor(random_state=42)
    segmentor.fit(X, n_clusters)
    return segmentor


# ================================================================
# Header
# ================================================================
st.markdown(
    """
<div class="dashboard-header">
    <h1>🎯 Customer Segmentation Dashboard</h1>
    <p>Phân cụm khách hàng dựa trên mô hình KMeans — RFM Analysis</p>
</div>
""",
    unsafe_allow_html=True,
)

# ================================================================
# Load Data
# ================================================================
try:
    df = load_data()
except FileNotFoundError:
    st.error(
        f"❌ Không tìm thấy file `{SEGMENTS_PATH}`.\n\n"
        "Hãy chạy pipeline trước:\n```bash\npython -m src.run_rfm\n```"
    )
    st.stop()

segments = sorted(df["Segment"].unique())
n_clusters = df["Cluster"].nunique()

# ================================================================
# Sidebar
# ================================================================
with st.sidebar:
    st.markdown("## ⚙️ Bộ lọc")

    selected_segments = st.multiselect(
        "Chọn Segment",
        options=segments,
        default=segments,
        help="Lọc theo nhóm khách hàng",
    )

    recency_range = st.slider(
        "Recency (ngày)",
        int(df["Recency"].min()),
        int(df["Recency"].max()),
        (int(df["Recency"].min()), int(df["Recency"].max())),
    )

    monetary_range = st.slider(
        "Monetary ($)",
        float(df["Monetary"].min()),
        float(df["Monetary"].max()),
        (float(df["Monetary"].min()), float(df["Monetary"].max())),
    )

    st.markdown("---")
    st.markdown("### 📊 Thông tin dữ liệu")
    st.caption(f"**File:** `rfm_segments.csv`")
    st.caption(f"**Tổng:** {len(df):,} khách hàng")
    st.caption(f"**Clusters:** {n_clusters}")

# Apply filters
mask = (
    df["Segment"].isin(selected_segments)
    & df["Recency"].between(*recency_range)
    & df["Monetary"].between(*monetary_range)
)
filtered = df[mask].copy()

if filtered.empty:
    st.warning("⚠️ Không có khách hàng nào phù hợp với bộ lọc. Hãy điều chỉnh lại.")
    st.stop()

# ================================================================
# KPI Metrics Row
# ================================================================
st.markdown("### 📈 Tổng quan")
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.metric("Tổng khách hàng", f"{len(filtered):,}")
with kpi2:
    st.metric("Recency TB", f"{filtered['Recency'].mean():.0f} ngày")
with kpi3:
    st.metric("Frequency TB", f"{filtered['Frequency'].mean():.1f}")
with kpi4:
    st.metric("Monetary TB", f"${filtered['Monetary'].mean():,.0f}")
with kpi5:
    champions_pct = (
        (filtered["Segment"] == "Champions").sum() / len(filtered) * 100
        if "Champions" in filtered["Segment"].values
        else 0
    )
    st.metric("Champions", f"{champions_pct:.1f}%")

st.markdown("")

# ================================================================
# Tabs
# ================================================================
tab_overview, tab_scatter, tab_rfm, tab_data, tab_predict = st.tabs(
    ["📊 Phân bố Segment", "🔬 3D Scatter Plot", "🧮 RFM Analysis", "📋 Dữ liệu chi tiết", "🔮 Dự đoán mới"]
)

# ------------------------------------------------------------------
# TAB 1: Segment Distribution
# ------------------------------------------------------------------
with tab_overview:
    col_pie, col_bar = st.columns(2)

    seg_counts = filtered["Segment"].value_counts().reset_index()
    seg_counts.columns = ["Segment", "Count"]
    colors = [_color_for(s) for s in seg_counts["Segment"]]

    with col_pie:
        fig_pie = px.pie(
            seg_counts,
            values="Count",
            names="Segment",
            title="Tỷ lệ phân bố khách hàng theo Segment",
            color="Segment",
            color_discrete_map={s: _color_for(s) for s in seg_counts["Segment"]},
            hole=0.45,
        )
        fig_pie.update_traces(
            textposition="inside",
            textinfo="percent+label",
            textfont_size=13,
        )
        fig_pie.update_layout(
            font=dict(family="Inter"),
            legend=dict(orientation="h", y=-0.15),
            margin=dict(t=50, b=50),
            height=450,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_bar:
        # Average RFM per segment
        seg_avg = (
            filtered.groupby("Segment")[["Recency", "Frequency", "Monetary"]]
            .mean()
            .round(1)
            .reset_index()
        )
        fig_bar = go.Figure()
        for metric, color in [
            ("Recency", "#667eea"),
            ("Frequency", "#00b894"),
            ("Monetary", "#fd79a8"),
        ]:
            fig_bar.add_trace(
                go.Bar(
                    name=metric,
                    x=seg_avg["Segment"],
                    y=seg_avg[metric],
                    marker_color=color,
                    opacity=0.85,
                )
            )
        fig_bar.update_layout(
            title="Giá trị trung bình RFM theo Segment",
            barmode="group",
            font=dict(family="Inter"),
            height=450,
            margin=dict(t=50, b=50),
            xaxis_tickangle=-25,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Segment summary table
    st.markdown("#### 📝 Tổng kết từng Segment")
    summary = (
        filtered.groupby("Segment")
        .agg(
            Số_lượng=("CustomerID", "count"),
            Recency_TB=("Recency", "mean"),
            Frequency_TB=("Frequency", "mean"),
            Monetary_TB=("Monetary", "mean"),
            Monetary_Tổng=("Monetary", "sum"),
        )
        .round(1)
        .sort_values("Monetary_TB", ascending=False)
    )
    summary["Monetary_Tổng"] = summary["Monetary_Tổng"].apply(lambda x: f"${x:,.0f}")
    summary["Monetary_TB"] = summary["Monetary_TB"].apply(lambda x: f"${x:,.0f}")
    st.dataframe(summary, use_container_width=True)

# ------------------------------------------------------------------
# TAB 2: 3D Scatter Plot
# ------------------------------------------------------------------
with tab_scatter:
    st.markdown("#### 🔬 Không gian RFM 3 chiều")
    st.caption("Mỗi điểm là 1 khách hàng. Trục: Recency × Frequency × Monetary")

    # Sample if too many points
    plot_df = filtered if len(filtered) <= 5000 else filtered.sample(5000, random_state=42)

    fig_3d = px.scatter_3d(
        plot_df,
        x="Recency",
        y="Frequency",
        z="Monetary",
        color="Segment",
        color_discrete_map={s: _color_for(s) for s in segments},
        opacity=0.7,
        hover_data=["CustomerID", "RFM_Score"],
        title="Phân bố KMeans Clusters trong không gian RFM",
    )
    fig_3d.update_layout(
        font=dict(family="Inter"),
        height=650,
        scene=dict(
            xaxis_title="Recency (ngày)",
            yaxis_title="Frequency (lần)",
            zaxis_title="Monetary ($)",
        ),
        legend=dict(
            orientation="h",
            y=-0.05,
        ),
    )
    fig_3d.update_traces(marker=dict(size=4))
    st.plotly_chart(fig_3d, use_container_width=True)

    # 2D projections
    st.markdown("#### 📐 Chiếu 2D")
    proj1, proj2 = st.columns(2)

    with proj1:
        fig_rf = px.scatter(
            plot_df,
            x="Recency",
            y="Frequency",
            color="Segment",
            color_discrete_map={s: _color_for(s) for s in segments},
            opacity=0.6,
            title="Recency vs Frequency",
            hover_data=["CustomerID"],
        )
        fig_rf.update_layout(height=400, font=dict(family="Inter"))
        fig_rf.update_traces(marker=dict(size=5))
        st.plotly_chart(fig_rf, use_container_width=True)

    with proj2:
        fig_fm = px.scatter(
            plot_df,
            x="Frequency",
            y="Monetary",
            color="Segment",
            color_discrete_map={s: _color_for(s) for s in segments},
            opacity=0.6,
            title="Frequency vs Monetary",
            hover_data=["CustomerID"],
        )
        fig_fm.update_layout(height=400, font=dict(family="Inter"))
        fig_fm.update_traces(marker=dict(size=5))
        st.plotly_chart(fig_fm, use_container_width=True)

# ------------------------------------------------------------------
# TAB 3: RFM Score Analysis
# ------------------------------------------------------------------
with tab_rfm:
    col_treemap, col_heatmap = st.columns(2)

    with col_treemap:
        st.markdown("#### 🌳 Treemap — Phân bổ giá trị theo Segment")
        treemap_data = (
            filtered.groupby("Segment")
            .agg(Count=("CustomerID", "count"), Total_Monetary=("Monetary", "sum"))
            .reset_index()
        )
        fig_tree = px.treemap(
            treemap_data,
            path=["Segment"],
            values="Total_Monetary",
            color="Count",
            color_continuous_scale="Viridis",
            title="Tổng doanh thu theo Segment",
        )
        fig_tree.update_layout(height=500, font=dict(family="Inter"))
        st.plotly_chart(fig_tree, use_container_width=True)

    with col_heatmap:
        st.markdown("#### 🔥 Heatmap — RFM Score trung bình")
        heatmap_data = (
            filtered.groupby("Segment")[["R_Score", "F_Score", "M_Score"]]
            .mean()
            .round(2)
        )
        fig_heat = px.imshow(
            heatmap_data.values,
            x=["R_Score", "F_Score", "M_Score"],
            y=heatmap_data.index.tolist(),
            color_continuous_scale="RdYlGn",
            text_auto=".2f",
            title="RFM Score trung bình theo Segment",
            aspect="auto",
        )
        fig_heat.update_layout(height=500, font=dict(family="Inter"))
        st.plotly_chart(fig_heat, use_container_width=True)

    # Distribution of RFM scores
    st.markdown("#### 📊 Phân phối RFM Scores")
    score_col1, score_col2, score_col3 = st.columns(3)

    for col_widget, metric, color in [
        (score_col1, "R_Score", "#667eea"),
        (score_col2, "F_Score", "#00b894"),
        (score_col3, "M_Score", "#fd79a8"),
    ]:
        with col_widget:
            fig_hist = px.histogram(
                filtered,
                x=metric,
                color="Segment",
                color_discrete_map={s: _color_for(s) for s in segments},
                barmode="stack",
                title=f"Phân phối {metric}",
                nbins=10,
            )
            fig_hist.update_layout(
                height=350,
                font=dict(family="Inter"),
                showlegend=False,
            )
            st.plotly_chart(fig_hist, use_container_width=True)

# ------------------------------------------------------------------
# TAB 4: Detailed Data Table
# ------------------------------------------------------------------
with tab_data:
    st.markdown("#### 📋 Bảng dữ liệu chi tiết")
    st.caption(f"Hiển thị {len(filtered):,} khách hàng (đã lọc)")

    # Search by CustomerID
    search_id = st.text_input(
        "🔍 Tìm theo CustomerID",
        placeholder="Ví dụ: 12748",
    )

    display_df = filtered.copy()
    if search_id:
        display_df = display_df[
            display_df["CustomerID"].astype(str).str.contains(search_id, na=False)
        ]

    # Sort options
    sort_col = st.selectbox(
        "Sắp xếp theo",
        options=["Monetary", "Frequency", "Recency", "RFM_Score", "CustomerID"],
        index=0,
    )
    sort_asc = st.checkbox("Tăng dần", value=False)
    display_df = display_df.sort_values(sort_col, ascending=sort_asc)

    st.dataframe(
        display_df.style.format(
            {
                "CustomerID": "{:.0f}",
                "Monetary": "${:,.2f}",
                "Recency": "{:.0f}",
                "Frequency": "{:.0f}",
            }
        ),
        use_container_width=True,
        height=500,
    )

    # Download button
    csv_data = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Tải xuống CSV",
        data=csv_data,
        file_name="filtered_segments.csv",
        mime="text/csv",
    )

# ------------------------------------------------------------------
# TAB 5: Predict New Customer
# ------------------------------------------------------------------
with tab_predict:
    st.markdown("#### 🔮 Dự đoán Segment cho khách hàng mới")
    st.caption(
        "Nhập giá trị RFM của khách hàng → mô hình KMeans sẽ gán vào segment phù hợp."
    )

    with st.form("predict_form"):
        pcol1, pcol2, pcol3 = st.columns(3)

        with pcol1:
            pred_recency = st.number_input(
                "Recency (ngày)",
                min_value=0,
                max_value=1000,
                value=30,
                help="Số ngày kể từ lần mua gần nhất",
            )
        with pcol2:
            pred_frequency = st.number_input(
                "Frequency (lần)",
                min_value=1,
                max_value=500,
                value=5,
                help="Số lần mua hàng",
            )
        with pcol3:
            pred_monetary = st.number_input(
                "Monetary ($)",
                min_value=0.0,
                max_value=500000.0,
                value=1000.0,
                step=100.0,
                help="Tổng giá trị chi tiêu",
            )

        submitted = st.form_submit_button(
            "🚀 Dự đoán Segment",
            use_container_width=True,
        )

    if submitted:
        segmentor = get_trained_model(n_clusters)
        X_new = np.array([[pred_recency, pred_frequency, pred_monetary]])
        cluster_label = segmentor.predict(X_new)[0]

        # Build a mini dataframe to get the segment name
        temp_df = pd.DataFrame(
            {"Recency": [pred_recency], "Frequency": [pred_frequency], "Monetary": [pred_monetary]}
        )

        # We need to map the cluster to a segment name using the same logic
        full_df = load_data()
        centroids = full_df.groupby("Cluster")[["Recency", "Frequency", "Monetary"]].mean()
        centroids["Score"] = centroids["Frequency"] * centroids["Monetary"] / (centroids["Recency"] + 1)
        rank_map = (centroids["Score"].rank(ascending=False).astype(int) - 1).to_dict()

        segment_names = ["Champions", "Loyal Customers", "Potential Loyalists", "At Risk", "Lost Customers"]
        while len(segment_names) < n_clusters:
            segment_names.append(f"Segment {len(segment_names) + 1}")

        predicted_segment = segment_names[rank_map[cluster_label]]
        seg_color = _color_for(predicted_segment)

        st.markdown("---")

        # Result card
        res1, res2 = st.columns([1, 2])
        with res1:
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(135deg, {seg_color}22, {seg_color}44);
                    border: 2px solid {seg_color};
                    border-radius: 16px;
                    padding: 30px;
                    text-align: center;
                ">
                    <p style="font-size: 0.9rem; opacity: 0.7; margin-bottom: 8px;">Kết quả dự đoán</p>
                    <h2 style="color: {seg_color}; margin: 0;">{predicted_segment}</h2>
                    <p style="font-size: 0.85rem; margin-top: 8px;">Cluster #{cluster_label}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with res2:
            st.markdown("**📊 So sánh với trung bình segment:**")

            seg_data = full_df[full_df["Segment"] == predicted_segment]
            comparison = pd.DataFrame(
                {
                    "Chỉ số": ["Recency", "Frequency", "Monetary"],
                    "Khách hàng mới": [pred_recency, pred_frequency, f"${pred_monetary:,.0f}"],
                    f"TB {predicted_segment}": [
                        f"{seg_data['Recency'].mean():.0f}",
                        f"{seg_data['Frequency'].mean():.1f}",
                        f"${seg_data['Monetary'].mean():,.0f}",
                    ],
                }
            )
            st.table(comparison)

# ================================================================
# Footer
# ================================================================
st.markdown("---")
st.markdown(
    """
<div style="text-align: center; opacity: 0.5; font-size: 0.8rem; padding: 10px 0;">
    Customer Segmentation Dashboard • RFM + KMeans • AIO OIA Project 01
</div>
""",
    unsafe_allow_html=True,
)
