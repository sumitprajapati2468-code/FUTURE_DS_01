"""Interactive dashboard for Meridian Home Goods sales performance."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.sales_analysis import (
    EXPORTS_DIR,
    PROCESSED_DIR,
    REPORTS_DIR,
    build_category_summary,
    build_monthly_summary,
    build_product_summary,
    build_region_category_matrix,
    build_region_summary,
    calculate_kpis,
    clean_sales_data,
    ensure_project_directories,
    generate_synthetic_sales_data,
)


st.set_page_config(page_title="Meridian Home Goods | Sales Insights", layout="wide", page_icon="📈")

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    .hero {
        background: linear-gradient(135deg, #0f4c5c 0%, #173f5f 45%, #2a9d8f 100%);
        color: white;
        padding: 1.4rem 1.6rem;
        border-radius: 18px;
        margin-bottom: 1rem;
        box-shadow: 0 12px 30px rgba(15, 76, 92, 0.16);
    }
    .metric-card {
        background: #ffffff;
        padding: 1rem 1.1rem;
        border-radius: 16px;
        border: 1px solid #e5e9ef;
        box-shadow: 0 8px 18px rgba(15, 76, 92, 0.06);
    }
    .small-note {
        color: #5f6b7a;
        font-size: 0.88rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    """Load the cleaned dataset, generating it first if needed."""

    ensure_project_directories()
    cleaned_path = PROCESSED_DIR / "sales_cleaned.csv"
    if cleaned_path.exists():
        return pd.read_csv(cleaned_path, parse_dates=["order_date", "month_start"])

    raw_df = generate_synthetic_sales_data()
    cleaning_result = clean_sales_data(raw_df)
    cleaning_result.dataframe.to_csv(cleaned_path, index=False)
    return cleaning_result.dataframe


@st.cache_data(show_spinner=False)
def load_support_tables(cleaned_df: pd.DataFrame):
    """Create reusable summary tables for the dashboard."""

    kpis = calculate_kpis(cleaned_df)
    monthly = build_monthly_summary(cleaned_df)
    products = build_product_summary(cleaned_df)
    categories = build_category_summary(cleaned_df)
    regions = build_region_summary(cleaned_df)
    matrix = build_region_category_matrix(cleaned_df)
    return kpis, monthly, products, categories, regions, matrix


cleaned_data = load_data()
cleaned_data["order_date"] = pd.to_datetime(cleaned_data["order_date"])
cleaned_data["month_start"] = pd.to_datetime(cleaned_data["month_start"])

kpis, monthly_summary, product_summary, category_summary, region_summary, matrix_summary = load_support_tables(cleaned_data)

st.markdown(
    """
    <div class="hero">
        <h1 style="margin-bottom: 0.25rem;">Meridian Home Goods Sales Performance Dashboard</h1>
        <p style="margin: 0; opacity: 0.9;">Revenue, margin, product mix, and growth opportunity analysis for a local retail business.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.header("Filters")
min_date = cleaned_data["order_date"].min().date()
max_date = cleaned_data["order_date"].max().date()
selected_dates = st.sidebar.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
if isinstance(selected_dates, tuple):
    start_date, end_date = selected_dates
else:
    start_date, end_date = min_date, max_date

available_categories = sorted(cleaned_data["category"].dropna().unique())
available_regions = sorted(cleaned_data["region"].dropna().unique())
available_segments = sorted(cleaned_data["segment"].dropna().unique())
selected_categories = st.sidebar.multiselect("Category", available_categories, default=available_categories)
selected_regions = st.sidebar.multiselect("Region", available_regions, default=available_regions)
selected_segments = st.sidebar.multiselect("Segment", available_segments, default=available_segments)
timeframe = st.sidebar.radio("Trend view", ["Monthly", "Quarterly"], horizontal=True)

filtered = cleaned_data[
    (cleaned_data["order_date"].dt.date >= start_date)
    & (cleaned_data["order_date"].dt.date <= end_date)
    & (cleaned_data["category"].isin(selected_categories))
    & (cleaned_data["region"].isin(selected_regions))
    & (cleaned_data["segment"].isin(selected_segments))
].copy()

filtered_kpis = calculate_kpis(filtered) if not filtered.empty else {"total_revenue": 0.0, "total_profit": 0.0, "profit_margin": 0.0, "total_orders": 0, "avg_order_value": 0.0}

if filtered.empty:
    st.warning("No records match the current filters. Expand the selected date range, category, region, or segment.")
    st.stop()

col1, col2, col3, col4, col5 = st.columns(5)
metric_values = [
    ("Total Revenue", f"${filtered_kpis['total_revenue']:,.0f}"),
    ("Total Profit", f"${filtered_kpis['total_profit']:,.0f}"),
    ("Profit Margin", f"{filtered_kpis['profit_margin']:.1f}%"),
    ("Total Orders", f"{filtered_kpis['total_orders']:,}"),
    ("Avg Order Value", f"${filtered_kpis['avg_order_value']:,.2f}"),
]
for column, (label, value) in zip([col1, col2, col3, col4, col5], metric_values):
    with column:
        st.markdown(f"<div class='metric-card'><div class='small-note'>{label}</div><h2 style='margin: 0.15rem 0 0 0;'>{value}</h2></div>", unsafe_allow_html=True)

st.markdown("### Revenue Trend")
if timeframe == "Monthly":
    trend = (
        filtered.groupby(pd.Grouper(key="order_date", freq="MS"), as_index=False)
        .agg(revenue=("sales", "sum"), profit=("profit", "sum"))
        .sort_values("order_date")
    )
    x_axis = "order_date"
else:
    trend = (
        filtered.groupby(filtered["order_date"].dt.to_period("Q").astype(str), as_index=False)
        .agg(revenue=("sales", "sum"), profit=("profit", "sum"))
        .rename(columns={"order_date": "quarter"})
    )
    x_axis = "quarter"

trend_melted = trend.melt(id_vars=[x_axis], value_vars=["revenue", "profit"], var_name="metric", value_name="value")
trend_fig = px.line(
    trend_melted,
    x=x_axis,
    y="value",
    color="metric",
    markers=True,
    color_discrete_map={"revenue": "#0f4c5c", "profit": "#d1495b"},
)
trend_fig.update_layout(legend_title_text="Metric", margin=dict(l=10, r=10, t=10, b=10), hovermode="x unified")
st.plotly_chart(trend_fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.markdown("### Top 10 Products by Revenue")
    revenue_products = product_summary.head(10).sort_values("revenue", ascending=True)
    fig = px.bar(revenue_products, x="revenue", y="product_name", orientation="h", color="category", color_discrete_sequence=px.colors.qualitative.Safe)
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), legend_title_text="Category")
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.markdown("### Top 10 Products by Profit")
    profit_products = product_summary.sort_values("profit", ascending=False).head(10).sort_values("profit", ascending=True)
    fig = px.bar(profit_products, x="profit", y="product_name", orientation="h", color="category", color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), legend_title_text="Category")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.markdown("### Category Performance")
    category_rollup = category_summary.groupby("category", as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum"), margin=("profit_margin", "mean"))
    fig = px.treemap(category_rollup, path=["category"], values="revenue", color="margin", color_continuous_scale="Viridis")
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.markdown("### Regional Performance")
    region_rollup = region_summary.groupby("region", as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
    region_rollup["profit_margin"] = (region_rollup["profit"] / region_rollup["revenue"]) * 100
    fig = px.bar(region_rollup.sort_values("profit_margin", ascending=False), x="region", y="profit_margin", color="profit_margin", color_continuous_scale="Tealgrn", text_auto=".1f")
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("### Revenue vs Profit Margin Quadrant View")
fig = px.scatter(
    matrix_summary,
    x="revenue",
    y="profit_margin",
    size="orders",
    color="quadrant",
    hover_name="region",
    text="category",
    size_max=40,
    color_discrete_map={"Double Down": "#2a9d8f", "Fix Margin": "#e76f51", "Build Demand": "#f4a261", "Deprioritize": "#8d99ae"},
)
fig.update_traces(textposition="top center")
fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig, use_container_width=True)

st.markdown("### Business Notes")
notes = [
    "High-revenue, low-margin pockets should be treated as pricing problems first, not demand problems.",
    "The strongest seasonal months should receive earlier inventory ordering and tighter labor planning.",
    "SKU concentration means the business can improve profit quickly by fixing only a handful of products.",
]
for note in notes:
    st.markdown(f"- {note}")

st.caption(f"Source files: {PROCESSED_DIR / 'sales_cleaned.csv'} and {REPORTS_DIR / 'client_report.md'}")
