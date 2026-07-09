"""Core sales analysis utilities for the Meridian Home Goods project.

This module generates realistic synthetic sales data when no client dataset is
provided, cleans the raw extract, computes business metrics, and exports the
charts and report inputs used by the dashboard and PDF report.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
ASSETS_DIR = PROJECT_ROOT / "assets"
CHARTS_DIR = ASSETS_DIR / "charts"
EXPORTS_DIR = ASSETS_DIR / "exports"
REPORTS_DIR = PROJECT_ROOT / "reports"
SCRIPT_DIR = PROJECT_ROOT / "scripts"

PERSONA_NAME = "Meridian Home Goods"
PERSONA_DESCRIPTION = (
    "A neighborhood retail store that sells furniture, office essentials, and"
    " compact technology accessories."
)

CANONICAL_CATEGORY_MAP = {
    "electronics": "Technology",
    "tech": "Technology",
    "technology": "Technology",
    "furniture": "Furniture",
    "office supplies": "Office Supplies",
    "office-supplies": "Office Supplies",
}

CANONICAL_REGION_MAP = {
    "east": "East",
    "west": "West",
    "central": "Central",
    "south": "South",
}

CANONICAL_PRODUCT_MAP = {
    "premium standing desk": "Premium Standing Desk",
    "premium standing desk ": "Premium Standing Desk",
    "ergonomic office chair": "Ergonomic Office Chair",
    "smart led monitor": "Smart LED Monitor",
    "wireless keyboard": "Wireless Keyboard",
    "compact printer": "Compact Printer",
    "modular bookshelf": "Modular Bookshelf",
    "oak coffee table": "Oak Coffee Table",
    "desk organizer set": "Desk Organizer Set",
    "premium notebook bundle": "Premium Notebook Bundle",
    "ink cartridge pack": "Ink Cartridge Pack",
    "cordless phone dock": "Cordless Phone Dock",
    "led desk lamp": "LED Desk Lamp",
    "file cabinet": "File Cabinet",
}

SHIP_MODES = ["Standard Class", "Second Class", "First Class", "Same Day"]
SEGMENTS = ["Consumer", "Corporate", "Home Office"]

REGION_STATES = {
    "West": ["California", "Washington", "Oregon", "Nevada"],
    "East": ["New York", "Pennsylvania", "Massachusetts", "New Jersey"],
    "Central": ["Illinois", "Texas", "Colorado", "Minnesota"],
    "South": ["Florida", "Georgia", "North Carolina", "Tennessee"],
}

REGION_PROFILES = {
    "West": {"revenue_weight": 1.15, "margin_adjustment": 0.03, "discount_mean": 0.08, "shipping_surcharge": 1.2},
    "East": {"revenue_weight": 1.0, "margin_adjustment": 0.00, "discount_mean": 0.10, "shipping_surcharge": 1.5},
    "Central": {"revenue_weight": 0.88, "margin_adjustment": 0.04, "discount_mean": 0.07, "shipping_surcharge": 0.8},
    "South": {"revenue_weight": 1.06, "margin_adjustment": -0.05, "discount_mean": 0.15, "shipping_surcharge": 2.0},
}

PRODUCT_CATALOG = [
    {
        "product_name": "Smart LED Monitor",
        "category": "Technology",
        "sub_category": "Monitors",
        "unit_price": 229.0,
        "base_margin": 0.28,
        "shipping_cost": 4.0,
        "weight": 0.16,
    },
    {
        "product_name": "Premium Standing Desk",
        "category": "Furniture",
        "sub_category": "Tables",
        "unit_price": 449.0,
        "base_margin": 0.18,
        "shipping_cost": 18.0,
        "weight": 0.11,
    },
    {
        "product_name": "Ergonomic Office Chair",
        "category": "Furniture",
        "sub_category": "Chairs",
        "unit_price": 199.0,
        "base_margin": 0.20,
        "shipping_cost": 14.0,
        "weight": 0.17,
    },
    {
        "product_name": "Wireless Keyboard",
        "category": "Technology",
        "sub_category": "Accessories",
        "unit_price": 74.0,
        "base_margin": 0.41,
        "shipping_cost": 2.5,
        "weight": 0.14,
    },
    {
        "product_name": "Compact Printer",
        "category": "Technology",
        "sub_category": "Printers",
        "unit_price": 139.0,
        "base_margin": 0.12,
        "shipping_cost": 6.0,
        "weight": 0.09,
    },
    {
        "product_name": "Modular Bookshelf",
        "category": "Furniture",
        "sub_category": "Storage",
        "unit_price": 169.0,
        "base_margin": 0.15,
        "shipping_cost": 11.0,
        "weight": 0.07,
    },
    {
        "product_name": "Desk Organizer Set",
        "category": "Office Supplies",
        "sub_category": "Storage",
        "unit_price": 34.0,
        "base_margin": 0.52,
        "shipping_cost": 1.4,
        "weight": 0.08,
    },
    {
        "product_name": "Premium Notebook Bundle",
        "category": "Office Supplies",
        "sub_category": "Paper",
        "unit_price": 18.0,
        "base_margin": 0.59,
        "shipping_cost": 1.0,
        "weight": 0.06,
    },
    {
        "product_name": "Ink Cartridge Pack",
        "category": "Office Supplies",
        "sub_category": "Supplies",
        "unit_price": 59.0,
        "base_margin": 0.32,
        "shipping_cost": 2.0,
        "weight": 0.05,
    },
    {
        "product_name": "Cordless Phone Dock",
        "category": "Technology",
        "sub_category": "Accessories",
        "unit_price": 66.0,
        "base_margin": 0.34,
        "shipping_cost": 2.2,
        "weight": 0.03,
    },
    {
        "product_name": "LED Desk Lamp",
        "category": "Furniture",
        "sub_category": "Lighting",
        "unit_price": 48.0,
        "base_margin": 0.36,
        "shipping_cost": 3.0,
        "weight": 0.02,
    },
    {
        "product_name": "File Cabinet",
        "category": "Furniture",
        "sub_category": "Storage",
        "unit_price": 219.0,
        "base_margin": 0.10,
        "shipping_cost": 16.0,
        "weight": 0.02,
    },
]

MONTH_SEASONALITY = {
    1: 0.78,
    2: 0.82,
    3: 0.92,
    4: 0.98,
    5: 1.02,
    6: 1.00,
    7: 1.06,
    8: 1.04,
    9: 1.00,
    10: 1.10,
    11: 1.32,
    12: 1.58,
}


def ensure_project_directories() -> None:
    """Create the project folders used by the analysis pipeline."""

    for directory in [RAW_DIR, PROCESSED_DIR, CHARTS_DIR, EXPORTS_DIR, REPORTS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)


def _mixed_date_string(date_value: pd.Timestamp, rng: np.random.Generator) -> str:
    """Return a date string in one of several formats to simulate messy source data."""

    formats = ["%Y-%m-%d", "%m/%d/%Y", "%d-%b-%Y"]
    return date_value.strftime(rng.choice(formats))


def _maybe_currency(value: float, rng: np.random.Generator) -> str | float:
    """Return either a numeric value or a currency-formatted string."""

    if rng.random() < 0.18:
        return f"${value:,.2f}"
    return round(value, 2)


def _maybe_text_noise(value: str, rng: np.random.Generator) -> str:
    """Introduce casing and whitespace variation into categorical fields."""

    options = [value, value.lower(), value.upper(), f" {value} "]
    return rng.choice(options)


def generate_synthetic_sales_data(seed: int = 42) -> pd.DataFrame:
    """Generate a realistic raw sales dataset when no client file is provided.

    The output intentionally includes messy elements that mirror real client
    exports: mixed date formats, currency strings, duplicate rows, occasional
    missing values, and a small number of invalid quantities.
    """

    ensure_project_directories()
    rng = np.random.default_rng(seed)
    months = pd.period_range("2024-01", periods=24, freq="M")
    rows: list[dict[str, Any]] = []
    order_counter = 10000

    product_weights = np.array([item["weight"] for item in PRODUCT_CATALOG], dtype=float)
    product_weights = product_weights / product_weights.sum()
    region_weights = np.array([profile["revenue_weight"] for profile in REGION_PROFILES.values()], dtype=float)
    region_weights = region_weights / region_weights.sum()
    region_names = list(REGION_PROFILES.keys())

    for month_period in months:
        seasonal_multiplier = MONTH_SEASONALITY[month_period.month]
        monthly_orders = int(round(38 * seasonal_multiplier + rng.normal(0, 4)))

        if month_period == pd.Period("2025-03", freq="M"):
            monthly_orders += 18
        if month_period == pd.Period("2024-02", freq="M"):
            monthly_orders -= 6

        monthly_orders = max(22, monthly_orders)

        for _ in range(monthly_orders):
            product = PRODUCT_CATALOG[rng.choice(len(PRODUCT_CATALOG), p=product_weights)]
            region = rng.choice(region_names, p=region_weights)
            region_profile = REGION_PROFILES[region]
            state = rng.choice(REGION_STATES[region])

            quantity = int(rng.integers(1, 6))
            if product["product_name"] in {"Premium Standing Desk", "Ergonomic Office Chair", "Smart LED Monitor"}:
                quantity += int(rng.integers(0, 3))

            discount_mean = region_profile["discount_mean"]
            if product["category"] == "Furniture":
                discount_mean += 0.03
            elif product["category"] == "Office Supplies":
                discount_mean -= 0.01
            discount = float(np.clip(rng.normal(discount_mean, 0.035), 0.0, 0.32))

            unit_price = float(np.clip(rng.normal(product["unit_price"], product["unit_price"] * 0.04), 8.0, None))
            gross_sales = quantity * unit_price
            sales = gross_sales * (1 - discount)

            unit_cost = unit_price * (1 - product["base_margin"])
            shipping_cost = quantity * (product["shipping_cost"] + region_profile["shipping_surcharge"])
            profit = sales - (quantity * unit_cost) - shipping_cost

            year_month_end = month_period.to_timestamp(how="end")
            day_value = int(rng.integers(1, year_month_end.day + 1))
            order_date = pd.Timestamp(year=month_period.year, month=month_period.month, day=day_value)

            ship_mode = rng.choice(SHIP_MODES, p=[0.52, 0.22, 0.18, 0.08])
            segment = rng.choice(SEGMENTS, p=[0.48, 0.34, 0.18])

            row = {
                "order_id": f"ORD-{order_counter:06d}",
                "order_date": _mixed_date_string(order_date, rng),
                "customer_id": f"CUST-{int(rng.integers(1000, 9999))}",
                "product_name": _maybe_text_noise(product["product_name"], rng),
                "category": _maybe_text_noise(product["category"], rng),
                "sub_category": _maybe_text_noise(product["sub_category"], rng),
                "region": _maybe_text_noise(region, rng),
                "state": _maybe_text_noise(state, rng),
                "quantity": quantity,
                "unit_price": _maybe_currency(unit_price, rng),
                "discount": round(discount, 2),
                "sales": _maybe_currency(sales, rng),
                "profit": _maybe_currency(profit, rng),
                "ship_mode": _maybe_text_noise(ship_mode, rng),
                "segment": _maybe_text_noise(segment, rng),
            }
            rows.append(row)
            order_counter += 1

    raw_df = pd.DataFrame(rows)

    duplicate_rows = raw_df.sample(n=18, random_state=seed)
    raw_df = pd.concat([raw_df, duplicate_rows], ignore_index=True)

    missing_indices = raw_df.sample(n=14, random_state=seed + 1).index
    raw_df.loc[missing_indices[:4], "customer_id"] = np.nan
    raw_df.loc[missing_indices[4:7], "discount"] = np.nan
    raw_df.loc[missing_indices[7:10], "state"] = np.nan
    raw_df.loc[missing_indices[10:12], "product_name"] = np.nan
    raw_df.loc[missing_indices[12:], "region"] = np.nan

    invalid_indices = raw_df.sample(n=6, random_state=seed + 2).index
    raw_df.loc[invalid_indices[:3], "quantity"] = 0
    raw_df.loc[invalid_indices[3:], "quantity"] = -1

    raw_df.loc[raw_df.sample(n=8, random_state=seed + 3).index, "category"] = "electronics"
    raw_df.loc[raw_df.sample(n=6, random_state=seed + 4).index, "region"] = "west"

    return raw_df.reset_index(drop=True)


def _standardize_text(series: pd.Series, mapping: dict[str, str]) -> pd.Series:
    """Normalize text values using a mapping and title casing fallback."""

    cleaned = series.astype("string").str.strip().str.lower()
    normalized = cleaned.map(mapping)
    normalized = normalized.fillna(cleaned.str.replace("-", " ", regex=False).str.title())
    return normalized


def _parse_currency_series(series: pd.Series) -> pd.Series:
    """Convert currency-formatted text to numeric values."""

    cleaned = (
        series.astype("string")
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace("%", "", regex=False)
        .str.strip()
    )
    return pd.to_numeric(cleaned, errors="coerce")


@dataclass
class CleaningResult:
    """Container for the cleaned dataframe and the documented cleaning log."""

    dataframe: pd.DataFrame
    log_lines: list[str]


def clean_sales_data(raw_df: pd.DataFrame) -> CleaningResult:
    """Clean the raw sales extract and capture every cleaning decision.

    Decisions in this function are intentionally conservative. We keep rows when
    they can still support a reliable sales analysis and only drop records that
    lack critical analytical fields such as date, product, category, or region.
    """

    df = raw_df.copy()
    log_lines: list[str] = []
    initial_rows = len(df)
    log_lines.append(f"Initial rows received: {initial_rows}")

    df.columns = [column.strip().lower().replace(" ", "_") for column in df.columns]

    duplicate_count = int(df.duplicated().sum())
    if duplicate_count:
        df = df.drop_duplicates()
    log_lines.append(f"Removed {duplicate_count} duplicate rows copied from the raw extract.")

    if "order_id" in df.columns:
        duplicate_orders = int(df.duplicated(subset=["order_id"], keep="first").sum())
        if duplicate_orders:
            df = df.drop_duplicates(subset=["order_id"], keep="first")
        log_lines.append(f"Removed {duplicate_orders} duplicated order_id values.")

    for date_column in ["order_date"]:
        if date_column in df.columns:
            df[date_column] = pd.to_datetime(df[date_column], errors="coerce", format="mixed")
            parsed_missing = int(df[date_column].isna().sum())
            log_lines.append(f"Parsed mixed date formats in {date_column}; {parsed_missing} rows could not be interpreted.")

    for numeric_column in ["unit_price", "sales", "profit", "discount"]:
        if numeric_column in df.columns:
            df[numeric_column] = _parse_currency_series(df[numeric_column])

    if "quantity" in df.columns:
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    text_columns = ["product_name", "category", "sub_category", "region", "state", "ship_mode", "segment"]
    for text_column in text_columns:
        if text_column in df.columns:
            df[text_column] = df[text_column].astype("string").str.strip()

    if "product_name" in df.columns:
        df["product_name"] = _standardize_text(df["product_name"], CANONICAL_PRODUCT_MAP)
    if "category" in df.columns:
        df["category"] = _standardize_text(df["category"], CANONICAL_CATEGORY_MAP)
    if "region" in df.columns:
        df["region"] = _standardize_text(df["region"], CANONICAL_REGION_MAP)
    if "sub_category" in df.columns:
        df["sub_category"] = df["sub_category"].str.replace("_", " ", regex=False).str.title()
    if "state" in df.columns:
        df["state"] = df["state"].str.replace("_", " ", regex=False).str.title()
    if "ship_mode" in df.columns:
        df["ship_mode"] = df["ship_mode"].str.title()
    if "segment" in df.columns:
        df["segment"] = df["segment"].str.title()

    missing_customer_count = int(df["customer_id"].isna().sum()) if "customer_id" in df.columns else 0
    if "customer_id" in df.columns:
        df["customer_id"] = df["customer_id"].fillna("Unknown Customer")
    log_lines.append(f"Filled {missing_customer_count} missing customer_id values with 'Unknown Customer'.")

    if "discount" in df.columns:
        median_discount = df.groupby("category", dropna=False)["discount"].transform("median")
        missing_discount_count = int(df["discount"].isna().sum())
        df["discount"] = df["discount"].fillna(median_discount)
        df["discount"] = df["discount"].fillna(df["discount"].median())
        log_lines.append(f"Filled {missing_discount_count} missing discount values using category medians and overall median fallback.")

    if "state" in df.columns and "region" in df.columns:
        region_state_lookup = df.groupby("region")["state"].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else x.dropna().iloc[0] if not x.dropna().empty else "Unknown")
        missing_state_count = int(df["state"].isna().sum())
        df["state"] = df["state"].fillna(df["region"].map(region_state_lookup))
        df["state"] = df["state"].fillna("Unknown")
        log_lines.append(f"Filled {missing_state_count} missing state values from region-level modes.")

    invalid_quantity_mask = df["quantity"].isna() | (df["quantity"] <= 0)
    invalid_quantity_count = int(invalid_quantity_mask.sum())
    if invalid_quantity_count:
        df = df.loc[~invalid_quantity_mask].copy()
    log_lines.append(f"Removed {invalid_quantity_count} rows with zero or negative quantities.")

    critical_columns = [column for column in ["order_date", "product_name", "category", "region", "sales", "profit", "quantity", "unit_price"] if column in df.columns]
    missing_critical_mask = df[critical_columns].isna().any(axis=1)
    missing_critical_count = int(missing_critical_mask.sum())
    if missing_critical_count:
        df = df.loc[~missing_critical_mask].copy()
    log_lines.append(f"Removed {missing_critical_count} rows with missing critical analytical fields.")

    if "sales" in df.columns and "quantity" in df.columns and "unit_price" in df.columns:
        gross_sales = df["quantity"] * df["unit_price"]
        df["gross_sales"] = gross_sales
        df["discount_impact"] = gross_sales - df["sales"]
        df["revenue_per_unit"] = np.where(df["quantity"] != 0, df["sales"] / df["quantity"], np.nan)
    else:
        df["gross_sales"] = np.nan
        df["discount_impact"] = np.nan
        df["revenue_per_unit"] = np.nan

    df["profit_margin"] = np.where(df["sales"] != 0, (df["profit"] / df["sales"]) * 100, np.nan)
    df["month_year"] = df["order_date"].dt.to_period("M").astype(str)
    df["month_start"] = df["order_date"].dt.to_period("M").dt.to_timestamp()
    df["quarter"] = df["order_date"].dt.to_period("Q").astype(str)
    df["calendar_month"] = df["order_date"].dt.month_name()
    df["calendar_month_num"] = df["order_date"].dt.month

    final_rows = len(df)
    log_lines.append(f"Final rows retained after cleaning: {final_rows}")
    log_lines.append(f"Net rows removed during cleaning: {initial_rows - final_rows}")

    return CleaningResult(dataframe=df.reset_index(drop=True), log_lines=log_lines)


def calculate_kpis(cleaned_df: pd.DataFrame) -> dict[str, float]:
    """Calculate the headline KPIs required for the dashboard and report."""

    total_revenue = float(cleaned_df["sales"].sum())
    total_profit = float(cleaned_df["profit"].sum())
    total_orders = int(cleaned_df["order_id"].nunique())
    avg_order_value = float(cleaned_df.groupby("order_id")["sales"].sum().mean())
    profit_margin = float((total_profit / total_revenue) * 100) if total_revenue else 0.0

    return {
        "total_revenue": total_revenue,
        "total_profit": total_profit,
        "profit_margin": profit_margin,
        "total_orders": total_orders,
        "avg_order_value": avg_order_value,
    }


def build_monthly_summary(cleaned_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate revenue and profit by month for trend and anomaly analysis."""

    monthly = (
        cleaned_df.groupby(["month_start", "month_year"], as_index=False)
        .agg(
            revenue=("sales", "sum"),
            profit=("profit", "sum"),
            orders=("order_id", "nunique"),
        )
        .sort_values("month_start")
        .reset_index(drop=True)
    )
    monthly["aov"] = monthly["revenue"] / monthly["orders"]
    monthly["revenue_growth_pct"] = monthly["revenue"].pct_change() * 100
    monthly["profit_growth_pct"] = monthly["profit"].pct_change() * 100
    monthly["rolling_median_revenue"] = monthly["revenue"].rolling(window=3, center=True, min_periods=1).median()
    monthly["deviation_from_trend_pct"] = np.where(
        monthly["rolling_median_revenue"] != 0,
        ((monthly["revenue"] - monthly["rolling_median_revenue"]) / monthly["rolling_median_revenue"]) * 100,
        np.nan,
    )
    return monthly


def build_quarterly_summary(cleaned_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate revenue and profit by quarter for period-over-period review."""

    quarterly = (
        cleaned_df.groupby("quarter", as_index=False)
        .agg(
            revenue=("sales", "sum"),
            profit=("profit", "sum"),
            orders=("order_id", "nunique"),
        )
        .sort_values("quarter")
        .reset_index(drop=True)
    )
    quarterly["revenue_growth_pct"] = quarterly["revenue"].pct_change() * 100
    quarterly["profit_growth_pct"] = quarterly["profit"].pct_change() * 100
    return quarterly


def build_seasonality_summary(cleaned_df: pd.DataFrame) -> pd.DataFrame:
    """Summarize seasonal patterns by calendar month."""

    seasonality = (
        cleaned_df.groupby(["calendar_month_num", "calendar_month"], as_index=False)
        .agg(revenue=("sales", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique"))
        .sort_values("calendar_month_num")
        .reset_index(drop=True)
    )
    seasonality["revenue_index"] = seasonality["revenue"] / seasonality["revenue"].mean()
    seasonality["profit_index"] = seasonality["profit"] / seasonality["profit"].mean()
    return seasonality


def build_product_summary(cleaned_df: pd.DataFrame) -> pd.DataFrame:
    """Build product-level revenue, profit, and margin summaries."""

    product_summary = (
        cleaned_df.groupby(["product_name", "category", "sub_category"], as_index=False)
        .agg(
            revenue=("sales", "sum"),
            profit=("profit", "sum"),
            orders=("order_id", "nunique"),
            avg_discount=("discount", "mean"),
            avg_margin=("profit_margin", "mean"),
        )
        .sort_values("revenue", ascending=False)
        .reset_index(drop=True)
    )
    product_summary["profit_margin"] = np.where(product_summary["revenue"] != 0, (product_summary["profit"] / product_summary["revenue"]) * 100, np.nan)
    product_summary["cumulative_revenue_share"] = product_summary["revenue"].cumsum() / product_summary["revenue"].sum()
    product_summary["revenue_rank"] = product_summary["revenue"].rank(method="dense", ascending=False).astype(int)
    product_summary["profit_rank"] = product_summary["profit"].rank(method="dense", ascending=False).astype(int)
    return product_summary


def build_category_summary(cleaned_df: pd.DataFrame) -> pd.DataFrame:
    """Summarize revenue and profit by category and sub-category."""

    category_summary = (
        cleaned_df.groupby(["category", "sub_category"], as_index=False)
        .agg(
            revenue=("sales", "sum"),
            profit=("profit", "sum"),
            orders=("order_id", "nunique"),
            avg_discount=("discount", "mean"),
        )
        .sort_values(["category", "revenue"], ascending=[True, False])
        .reset_index(drop=True)
    )
    category_summary["profit_margin"] = np.where(category_summary["revenue"] != 0, (category_summary["profit"] / category_summary["revenue"]) * 100, np.nan)
    return category_summary


def build_region_summary(cleaned_df: pd.DataFrame) -> pd.DataFrame:
    """Summarize revenue and profit by region and state."""

    region_summary = (
        cleaned_df.groupby(["region", "state"], as_index=False)
        .agg(
            revenue=("sales", "sum"),
            profit=("profit", "sum"),
            orders=("order_id", "nunique"),
            avg_discount=("discount", "mean"),
        )
        .sort_values("revenue", ascending=False)
        .reset_index(drop=True)
    )
    region_summary["profit_margin"] = np.where(region_summary["revenue"] != 0, (region_summary["profit"] / region_summary["revenue"]) * 100, np.nan)
    return region_summary


def build_region_category_matrix(cleaned_df: pd.DataFrame) -> pd.DataFrame:
    """Combine region and category to support the quadrant analysis."""

    matrix = (
        cleaned_df.groupby(["region", "category"], as_index=False)
        .agg(
            revenue=("sales", "sum"),
            profit=("profit", "sum"),
            orders=("order_id", "nunique"),
        )
        .sort_values("revenue", ascending=False)
        .reset_index(drop=True)
    )
    matrix["profit_margin"] = np.where(matrix["revenue"] != 0, (matrix["profit"] / matrix["revenue"]) * 100, np.nan)

    revenue_threshold = matrix["revenue"].median()
    margin_threshold = matrix["profit_margin"].median()

    def classify(row: pd.Series) -> str:
        if row["revenue"] >= revenue_threshold and row["profit_margin"] >= margin_threshold:
            return "Double Down"
        if row["revenue"] >= revenue_threshold and row["profit_margin"] < margin_threshold:
            return "Fix Margin"
        if row["revenue"] < revenue_threshold and row["profit_margin"] >= margin_threshold:
            return "Build Demand"
        return "Deprioritize"

    matrix["quadrant"] = matrix.apply(classify, axis=1)
    return matrix


def identify_anomalies(monthly_summary: pd.DataFrame) -> pd.DataFrame:
    """Flag sudden spikes or drops that warrant business investigation."""

    anomaly_mask = monthly_summary["deviation_from_trend_pct"].abs() >= 18
    growth_mask = monthly_summary["revenue_growth_pct"].abs() >= 22
    anomalies = monthly_summary.loc[anomaly_mask | growth_mask].copy()
    if not anomalies.empty:
        anomalies["reason"] = np.where(
            anomalies["deviation_from_trend_pct"].abs() >= 18,
            np.where(
                anomalies["revenue_growth_pct"].abs() >= 22,
                "Large deviation from trend and sharp month-over-month change",
                "Large deviation from trend",
            ),
            "Sharp month-over-month change",
        )
    return anomalies[["month_year", "revenue", "profit", "revenue_growth_pct", "deviation_from_trend_pct", "reason"]]


def identify_high_sales_low_margin_products(product_summary: pd.DataFrame) -> pd.DataFrame:
    """Find products that are generating revenue but eroding profit margin."""

    revenue_cutoff = product_summary["revenue"].quantile(0.70)
    margin_cutoff = product_summary["profit_margin"].quantile(0.35)
    high_sales_low_margin = product_summary.loc[
        (product_summary["revenue"] >= revenue_cutoff) & (product_summary["profit_margin"] <= margin_cutoff)
    ].copy()
    return high_sales_low_margin.sort_values(["revenue", "profit_margin"], ascending=[False, True]).reset_index(drop=True)


def identify_slow_movers(product_summary: pd.DataFrame) -> pd.DataFrame:
    """Flag products that are low revenue and low profit candidates for repricing or discontinuation."""

    revenue_cutoff = product_summary["revenue"].quantile(0.30)
    profit_cutoff = product_summary["profit"].quantile(0.30)
    slow_movers = product_summary.loc[
        (product_summary["revenue"] <= revenue_cutoff) & (product_summary["profit"] <= profit_cutoff)
    ].copy()
    return slow_movers.sort_values(["revenue", "profit"], ascending=[True, True]).reset_index(drop=True)


def calculate_pareto_threshold(product_summary: pd.DataFrame) -> dict[str, Any]:
    """Estimate how many products drive 80% of total revenue."""

    sorted_products = product_summary.sort_values("revenue", ascending=False).reset_index(drop=True)
    sorted_products["cumulative_share"] = sorted_products["revenue"].cumsum() / sorted_products["revenue"].sum()
    products_to_80 = int((sorted_products["cumulative_share"] <= 0.80).sum())
    if products_to_80 == 0 and len(sorted_products) > 0:
        products_to_80 = 1
    revenue_share_top_products = float(sorted_products.loc[: products_to_80 - 1, "revenue"].sum() / sorted_products["revenue"].sum()) if products_to_80 else 0.0
    return {
        "products_to_80_revenue": products_to_80,
        "revenue_share_top_products": revenue_share_top_products,
        "total_products": int(len(sorted_products)),
    }


def export_cleaning_log(log_lines: list[str], output_path: Path) -> None:
    """Persist the cleaning log as a client-readable markdown file."""

    output_path.write_text("\n".join(["# Data Cleaning Log", "", *[f"- {line}" for line in log_lines]]) + "\n", encoding="utf-8")


def export_data_notes(output_path: Path) -> None:
    """Document the synthetic-data design so the submission is transparent."""

    notes = """# Data Notes

This project uses a realistic synthetic sales dataset because no client file was
provided in the workspace.

## Generation logic
- 24 months of order-line data were generated from January 2024 through December 2025.
- Demand follows a seasonal pattern with stronger revenue in Q4 and softer demand in January and February.
- Product mix intentionally includes clear revenue leaders and lower-margin items so the analysis surfaces real tradeoffs.
- Regional behavior varies by region:
  - West: strongest margin profile
  - East: balanced but discount-sensitive
  - Central: lower volume, better efficiency
  - South: high sales pressure with weaker margins due to heavier discounting
- A small number of duplicate rows, mixed date formats, currency strings, missing values, and invalid quantities were inserted so the cleaning phase reflects a real client file.
- One mild spike was introduced in March 2025 to support anomaly detection.

## Business persona
- Meridian Home Goods, a local retail shop selling furniture, office supplies, and compact technology products.
"""
    output_path.write_text(notes, encoding="utf-8")


def save_dataframe(df: pd.DataFrame, output_path: Path) -> None:
    """Save a dataframe to CSV with a stable encoding."""

    df.to_csv(output_path, index=False)


def _format_currency(value: float) -> str:
    """Format numeric values for report and README text."""

    return f"${value:,.0f}" if abs(value) >= 1000 else f"${value:,.2f}"


def build_report_narrative(
    kpis: dict[str, float],
    monthly_summary: pd.DataFrame,
    quarterly_summary: pd.DataFrame,
    seasonality_summary: pd.DataFrame,
    product_summary: pd.DataFrame,
    category_summary: pd.DataFrame,
    region_summary: pd.DataFrame,
    matrix_summary: pd.DataFrame,
    anomalies: pd.DataFrame,
    high_sales_low_margin: pd.DataFrame,
    slow_movers: pd.DataFrame,
    pareto: dict[str, Any],
) -> dict[str, Any]:
    """Turn the analytical outputs into concise executive-ready narratives."""

    peak_month_row = seasonality_summary.loc[seasonality_summary["revenue"].idxmax()]
    low_month_row = seasonality_summary.loc[seasonality_summary["revenue"].idxmin()]
    top_revenue_product = product_summary.iloc[0]
    top_profit_product = product_summary.sort_values("profit", ascending=False).iloc[0]
    if top_revenue_product["product_name"] == top_profit_product["product_name"]:
        product_comparison = (
            f"{top_revenue_product['product_name']} leads both revenue and profit, which is a healthy sign that demand and margin are aligned."
        )
    else:
        product_comparison = (
            f"{top_revenue_product['product_name']} leads revenue, while {top_profit_product['product_name']} leads profit."
            " That split matters because the business is not simply winning on turnover; margin management still needs attention."
        )

    region_rollup = region_summary.groupby("region", as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
    region_rollup["profit_margin"] = np.where(region_rollup["revenue"] != 0, (region_rollup["profit"] / region_rollup["revenue"]) * 100, np.nan)
    category_rollup = category_summary.groupby("category", as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
    category_rollup["profit_margin"] = np.where(category_rollup["revenue"] != 0, (category_rollup["profit"] / category_rollup["revenue"]) * 100, np.nan)

    highest_margin_region = region_rollup.sort_values("profit_margin", ascending=False).iloc[0]
    highest_revenue_category = category_rollup.sort_values("revenue", ascending=False).iloc[0]
    highest_margin_category = category_rollup.sort_values("profit_margin", ascending=False).iloc[0]
    double_down = matrix_summary.loc[matrix_summary["quadrant"] == "Double Down"].sort_values("revenue", ascending=False)
    fix_margin = matrix_summary.loc[matrix_summary["quadrant"] == "Fix Margin"].sort_values("revenue", ascending=False)

    recommendations: list[dict[str, str]] = []
    if not fix_margin.empty:
        focus_row = fix_margin.iloc[0]
        recommendations.append(
            {
                "title": "Tighten discounting where revenue is strong but margins are lagging",
                "action": (
                    f"Review pricing and discounts in {focus_row['region']} / {focus_row['category']}. "
                    f"That pocket generated {_format_currency(focus_row['revenue'])} in revenue but only {focus_row['profit_margin']:.1f}% margin."
                ),
                "impact": (
                    f"If that segment lifted margin to the portfolio median, annual profit would improve by roughly {_format_currency(focus_row['revenue'] * (matrix_summary['profit_margin'].median() - focus_row['profit_margin']) / 100)}."
                ),
            }
        )
    if not high_sales_low_margin.empty:
        product_row = high_sales_low_margin.iloc[0]
        recommendations.append(
            {
                "title": "Reduce discount leakage on the highest-volume low-margin product",
                "action": (
                    f"{product_row['product_name']} is producing {_format_currency(product_row['revenue'])} in revenue but only {product_row['profit_margin']:.1f}% margin. "
                    "Cap promo depth and test a smaller bundle incentive instead of broad discounting."
                ),
                "impact": (
                    f"A 3-point margin lift on this product alone would add about {_format_currency(product_row['revenue'] * 0.03)} in annual profit."
                ),
            }
        )
    if not double_down.empty:
        focus_row = double_down.iloc[0]
        recommendations.append(
            {
                "title": "Scale the best-performing growth pocket",
                "action": (
                    f"Increase local marketing and inventory priority in {focus_row['region']} / {focus_row['category']}. "
                    f"It combines {_format_currency(focus_row['revenue'])} of revenue with {focus_row['profit_margin']:.1f}% margin."
                ),
                "impact": (
                    f"A 10% revenue lift in this pocket would contribute about {_format_currency(focus_row['revenue'] * 0.10 * focus_row['profit_margin'] / 100)} of additional profit at the current margin." 
                ),
            }
        )

    if slow_movers.shape[0] > 0:
        slow_row = slow_movers.iloc[0]
        recommendations.append(
            {
                "title": "Deprioritize slow movers that tie up cash without creating profit",
                "action": (
                    f"{slow_row['product_name']} sits in the low-revenue, low-profit bucket. Reprice it, replace it, or stop carrying excess stock."
                ),
                "impact": (
                    f"Reducing inventory exposure on this item can free working capital and avoid roughly {_format_currency(abs(min(slow_row['profit'], 0.0)))} of annual profit drag."
                ),
            }
        )

    executive_summary = [
        f"Meridian Home Goods generated {_format_currency(kpis['total_revenue'])} in revenue across {int(kpis['total_orders'])} orders and {_format_currency(kpis['total_profit'])} in profit, leaving the business at {kpis['profit_margin']:.1f}% margin.",
        f"Demand is clearly seasonal: {peak_month_row['calendar_month']} is the strongest month, while {low_month_row['calendar_month']} is the weakest, so inventory and staffing should follow that rhythm.",
        product_comparison,
        f"The {highest_margin_region['region']} region is the most efficient market at {highest_margin_region['profit_margin']:.1f}% margin, while {highest_revenue_category['category']} leads category revenue and {highest_margin_category['category']} leads category margin.",
        f"Only {pareto['products_to_80_revenue']} of {pareto['total_products']} products drive 80% of revenue, which means the assortment is concentrated enough to reward tighter SKU management.",
    ]

    methodology = {
        "clean_rows": len(monthly_summary),
        "anomaly_count": int(len(anomalies)),
        "pareto_products": pareto["products_to_80_revenue"],
        "top_margin_region": highest_margin_region["region"],
        "top_margin_category": highest_margin_category["category"],
    }

    return {
        "executive_summary": executive_summary,
        "recommendations": recommendations,
        "monthly_summary": monthly_summary,
        "quarterly_summary": quarterly_summary,
        "seasonality_summary": seasonality_summary,
        "product_summary": product_summary,
        "category_summary": category_summary,
        "region_summary": region_summary,
        "matrix_summary": matrix_summary,
        "anomalies": anomalies,
        "high_sales_low_margin": high_sales_low_margin,
        "slow_movers": slow_movers,
        "pareto": pareto,
        "methodology": methodology,
    }


def create_matplotlib_charts(
    monthly_summary: pd.DataFrame,
    top_revenue_products: pd.DataFrame,
    top_profit_products: pd.DataFrame,
    category_summary: pd.DataFrame,
    region_summary: pd.DataFrame,
    matrix_summary: pd.DataFrame,
    output_dir: Path,
) -> dict[str, Path]:
    """Create static PNG charts for the PDF report and README screenshots."""

    output_dir.mkdir(parents=True, exist_ok=True)
    chart_paths: dict[str, Path] = {}

    plt.style.use("seaborn-v0_8-whitegrid")
    base_color = "#0f4c5c"
    accent_color = "#d1495b"
    green_color = "#2a9d8f"

    fig, ax = plt.subplots(figsize=(12, 6), dpi=180)
    ax.plot(monthly_summary["month_start"], monthly_summary["revenue"], color=base_color, linewidth=2.8, marker="o", label="Revenue")
    ax.plot(monthly_summary["month_start"], monthly_summary["profit"], color=accent_color, linewidth=2.2, marker="o", label="Profit")
    ax.set_title("Monthly Revenue and Profit", fontsize=16, weight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Value ($)")
    ax.legend(frameon=False)
    fig.autofmt_xdate()
    fig.tight_layout()
    path = output_dir / "monthly_revenue_profit.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    chart_paths["monthly_revenue_profit"] = path

    fig, ax = plt.subplots(figsize=(12, 7), dpi=180)
    revenue_df = top_revenue_products.sort_values("revenue", ascending=True)
    ax.barh(revenue_df["product_name"], revenue_df["revenue"], color=base_color)
    ax.set_title("Top 10 Products by Revenue", fontsize=16, weight="bold")
    ax.set_xlabel("Revenue ($)")
    ax.set_ylabel("Product")
    fig.tight_layout()
    path = output_dir / "top_products_revenue.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    chart_paths["top_products_revenue"] = path

    fig, ax = plt.subplots(figsize=(12, 7), dpi=180)
    profit_df = top_profit_products.sort_values("profit", ascending=True)
    ax.barh(profit_df["product_name"], profit_df["profit"], color=green_color)
    ax.set_title("Top 10 Products by Profit", fontsize=16, weight="bold")
    ax.set_xlabel("Profit ($)")
    ax.set_ylabel("Product")
    fig.tight_layout()
    path = output_dir / "top_products_profit.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    chart_paths["top_products_profit"] = path

    category_plot = category_summary.groupby("category", as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum"), margin=("profit_margin", "mean"))
    fig, ax = plt.subplots(figsize=(11, 6), dpi=180)
    x = np.arange(len(category_plot))
    width = 0.35
    ax.bar(x - width / 2, category_plot["revenue"], width=width, label="Revenue", color=base_color)
    ax.bar(x + width / 2, category_plot["profit"], width=width, label="Profit", color=accent_color)
    ax.set_xticks(x)
    ax.set_xticklabels(category_plot["category"])
    ax.set_title("Category Revenue vs Profit", fontsize=16, weight="bold")
    ax.set_ylabel("Value ($)")
    ax.legend(frameon=False)
    fig.tight_layout()
    path = output_dir / "category_performance.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    chart_paths["category_performance"] = path

    region_plot = region_summary.groupby("region", as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum"), margin=("profit_margin", "mean"))
    fig, ax = plt.subplots(figsize=(11, 6), dpi=180)
    x = np.arange(len(region_plot))
    ax.bar(x - width / 2, region_plot["revenue"], width=width, label="Revenue", color="#355c7d")
    ax.bar(x + width / 2, region_plot["profit"], width=width, label="Profit", color="#6c5b7b")
    ax.set_xticks(x)
    ax.set_xticklabels(region_plot["region"])
    ax.set_title("Regional Revenue vs Profit", fontsize=16, weight="bold")
    ax.set_ylabel("Value ($)")
    ax.legend(frameon=False)
    fig.tight_layout()
    path = output_dir / "regional_performance.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    chart_paths["regional_performance"] = path

    fig, ax = plt.subplots(figsize=(10.5, 7.5), dpi=180)
    colors = {"Double Down": "#2a9d8f", "Fix Margin": "#e76f51", "Build Demand": "#f4a261", "Deprioritize": "#8d99ae"}
    for quadrant, subset in matrix_summary.groupby("quadrant"):
        ax.scatter(
            subset["revenue"],
            subset["profit_margin"],
            s=subset["orders"] * 7,
            alpha=0.75,
            label=quadrant,
            color=colors.get(quadrant, "#264653"),
            edgecolors="white",
            linewidth=1.0,
        )
        for _, row in subset.iterrows():
            ax.annotate(f"{row['region']} / {row['category']}", (row["revenue"], row["profit_margin"]), textcoords="offset points", xytext=(6, 5), fontsize=8)
    ax.axvline(matrix_summary["revenue"].median(), color="#666666", linestyle="--", linewidth=1)
    ax.axhline(matrix_summary["profit_margin"].median(), color="#666666", linestyle="--", linewidth=1)
    ax.set_title("Revenue vs Profit Margin Quadrant View", fontsize=16, weight="bold")
    ax.set_xlabel("Revenue ($)")
    ax.set_ylabel("Profit Margin (%)")
    ax.legend(frameon=False, loc="best")
    fig.tight_layout()
    path = output_dir / "quadrant_view.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    chart_paths["quadrant_view"] = path

    return chart_paths


def export_analysis_bundle(cleaned_df: pd.DataFrame, output_dir: Path) -> dict[str, Any]:
    """Compute all analytical tables and build the downstream deliverables."""

    ensure_project_directories()
    kpis = calculate_kpis(cleaned_df)
    monthly_summary = build_monthly_summary(cleaned_df)
    quarterly_summary = build_quarterly_summary(cleaned_df)
    seasonality_summary = build_seasonality_summary(cleaned_df)
    product_summary = build_product_summary(cleaned_df)
    category_summary = build_category_summary(cleaned_df)
    region_summary = build_region_summary(cleaned_df)
    matrix_summary = build_region_category_matrix(cleaned_df)
    anomalies = identify_anomalies(monthly_summary)
    high_sales_low_margin = identify_high_sales_low_margin_products(product_summary)
    slow_movers = identify_slow_movers(product_summary)
    pareto = calculate_pareto_threshold(product_summary)
    narrative = build_report_narrative(
        kpis,
        monthly_summary,
        quarterly_summary,
        seasonality_summary,
        product_summary,
        category_summary,
        region_summary,
        matrix_summary,
        anomalies,
        high_sales_low_margin,
        slow_movers,
        pareto,
    )

    chart_paths = create_matplotlib_charts(
        monthly_summary,
        product_summary.head(10),
        product_summary.sort_values("profit", ascending=False).head(10),
        category_summary,
        region_summary,
        matrix_summary,
        output_dir / "charts",
    )

    return {
        "kpis": kpis,
        "monthly_summary": monthly_summary,
        "quarterly_summary": quarterly_summary,
        "seasonality_summary": seasonality_summary,
        "product_summary": product_summary,
        "category_summary": category_summary,
        "region_summary": region_summary,
        "matrix_summary": matrix_summary,
        "anomalies": anomalies,
        "high_sales_low_margin": high_sales_low_margin,
        "slow_movers": slow_movers,
        "pareto": pareto,
        "narrative": narrative,
        "chart_paths": chart_paths,
    }


def export_summary_artifacts(cleaned_df: pd.DataFrame, analysis_bundle: dict[str, Any]) -> None:
    """Write the key datasets and narrative files that support the submission."""

    ensure_project_directories()
    save_dataframe(cleaned_df, PROCESSED_DIR / "sales_cleaned.csv")
    save_dataframe(cleaned_df, EXPORTS_DIR / "dashboard_data.csv")
    save_dataframe(analysis_bundle["monthly_summary"], EXPORTS_DIR / "monthly_summary.csv")
    save_dataframe(analysis_bundle["quarterly_summary"], EXPORTS_DIR / "quarterly_summary.csv")
    save_dataframe(analysis_bundle["product_summary"], EXPORTS_DIR / "product_summary.csv")
    save_dataframe(analysis_bundle["category_summary"], EXPORTS_DIR / "category_summary.csv")
    save_dataframe(analysis_bundle["region_summary"], EXPORTS_DIR / "region_summary.csv")
    save_dataframe(analysis_bundle["matrix_summary"], EXPORTS_DIR / "matrix_summary.csv")
    save_dataframe(analysis_bundle["anomalies"], EXPORTS_DIR / "anomalies.csv")
    save_dataframe(analysis_bundle["high_sales_low_margin"], EXPORTS_DIR / "high_sales_low_margin.csv")
    save_dataframe(analysis_bundle["slow_movers"], EXPORTS_DIR / "slow_movers.csv")

    export_cleaning_log(analysis_bundle.get("cleaning_log", []), REPORTS_DIR / "data_cleaning_log.md")


def build_report_markdown(analysis_bundle: dict[str, Any], output_path: Path) -> str:
    """Create a polished markdown report that can be exported to PDF or reviewed directly."""

    kpis = analysis_bundle["kpis"]
    narrative = analysis_bundle["narrative"]
    monthly_summary = analysis_bundle["monthly_summary"]
    quarterly_summary = analysis_bundle["quarterly_summary"]
    seasonality_summary = analysis_bundle["seasonality_summary"]
    product_summary = analysis_bundle["product_summary"]
    category_summary = analysis_bundle["category_summary"]
    region_summary = analysis_bundle["region_summary"]
    matrix_summary = analysis_bundle["matrix_summary"]
    anomalies = analysis_bundle["anomalies"]
    high_sales_low_margin = analysis_bundle["high_sales_low_margin"]
    slow_movers = analysis_bundle["slow_movers"]
    pareto = analysis_bundle["pareto"]

    top_revenue_product = product_summary.iloc[0]
    top_profit_product = product_summary.sort_values("profit", ascending=False).iloc[0]
    peak_month = seasonality_summary.loc[seasonality_summary["revenue"].idxmax()]
    low_month = seasonality_summary.loc[seasonality_summary["revenue"].idxmin()]
    category_rollup = category_summary.groupby("category", as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
    category_rollup["profit_margin"] = np.where(category_rollup["revenue"] != 0, (category_rollup["profit"] / category_rollup["revenue"]) * 100, np.nan)
    region_rollup = region_summary.groupby("region", as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
    region_rollup["profit_margin"] = np.where(region_rollup["revenue"] != 0, (region_rollup["profit"] / region_rollup["revenue"]) * 100, np.nan)

    lines = [
        f"# Sales Performance & Business Insights Report - {PERSONA_NAME}",
        "",
        "## Executive Summary",
        *[f"- {item}" for item in narrative["executive_summary"]],
        "",
        "## Business Objective & Approach",
        f"This engagement focuses on the questions a real retail owner would ask before making a Monday-morning decision: where revenue comes from, which products actually create profit, which markets deserve more investment, and where discounting is quietly eroding margin.",
        f"The analysis uses {int(kpis['total_orders'])} cleaned orders from a realistic synthetic dataset designed to behave like a small retail store with seasonal demand, mixed-margin products, and regional performance differences.",
        "",
        "## Data Overview & Methodology",
        f"The raw file included mixed date formats, currency strings, duplicate orders, missing values, and invalid quantities. The cleaning process standardized those fields, removed invalid rows, and derived month-year, quarter, profit margin, revenue per unit, and discount impact.",
        f"Final cleaned dataset size: {int(kpis['total_orders'])} order lines supporting the trend analysis, {len(product_summary)} unique products, {len(category_summary)} category/sub-category combinations, and {len(region_summary)} region/state combinations.",
        "",
        "## Key Findings - Revenue Trends",
        f"Monthly revenue peaked in {peak_month['calendar_month']} and bottomed out in {low_month['calendar_month']}. The monthly line chart shows that Q4 is the strongest stretch, which is consistent with holiday retail behavior.",
        f"Quarterly revenue growth should be monitored because the trend is not linear; it accelerates late in the year and slows materially at the start of the year.",
        f"Anomaly review flagged {len(anomalies)} month(s) that moved sharply away from trend and should be investigated instead of assumed to be normal seasonality.",
        "",
        "## Key Findings - Product Performance",
        f"Top revenue product: {top_revenue_product['product_name']} at ${top_revenue_product['revenue']:,.0f}. Top profit product: {top_profit_product['product_name']} at ${top_profit_product['profit']:,.0f}.",
        f"That difference matters because the most visible revenue item is not always the most valuable one after discounting and shipping are taken into account.",
        f"{len(high_sales_low_margin)} products fall into the high-sales, low-margin bucket and should be treated as discount-control candidates.",
        f"{pareto['products_to_80_revenue']} products account for about {pareto['revenue_share_top_products'] * 100:.1f}% of total revenue, which means the assortment is concentrated enough that SKU discipline will matter.",
        f"{len(slow_movers)} slow-moving products sit in the low-revenue, low-profit bucket and are candidates for repricing, bundling, or discontinuation.",
        "",
        "## Key Findings - Category and Regional Profitability",
        f"Highest revenue category: {category_rollup.sort_values('revenue', ascending=False).iloc[0]['category']}. Highest margin category: {category_rollup.sort_values('profit_margin', ascending=False).iloc[0]['category']}.",
        f"Highest margin region: {region_rollup.sort_values('profit_margin', ascending=False).iloc[0]['region']}. The region/category matrix shows where the business should double down and where it should fix margin before trying to grow volume.",
        "",
        "## Growth Opportunities",
        f"The quadrant chart separates the business into four actions: Double Down, Fix Margin, Build Demand, and Deprioritize. This keeps revenue problems distinct from margin problems, which is the key analytical mistake most beginner dashboards make.",
        "",
        "## Actionable Recommendations",
    ]

    for index, recommendation in enumerate(narrative["recommendations"], start=1):
        lines.extend([
            f"### Recommendation {index}: {recommendation['title']}",
            f"- Action: {recommendation['action']}",
            f"- Estimated impact: {recommendation['impact']}",
            "",
        ])

    lines.extend([
        "## Limitations & Next Steps",
        "- This is a single-entity sales file, so profitability is observed at the order line level rather than with full customer lifetime value.",
        "- The synthetic dataset is designed to be realistic, but a production engagement would also examine inventory turns, stockouts, customer cohorts, and acquisition channel performance.",
        "- If more data were available, the next analysis would join marketing spend and inventory records to quantify true contribution margin by channel and stock position.",
        "",
        "## Appendix",
        "- Full monthly summary table exported to `assets/exports/monthly_summary.csv`.",
        "- Full product, category, region, anomaly, and quadrant tables exported to `assets/exports/`.",
        "- Dashboard screenshots and static charts saved to `assets/charts/`.",
        "",
        f"Headline KPIs: revenue ${kpis['total_revenue']:,.0f}, profit ${kpis['total_profit']:,.0f}, margin {kpis['profit_margin']:.1f}%, orders {int(kpis['total_orders'])}, average order value ${kpis['avg_order_value']:,.2f}.",
    ])

    markdown = "\n".join(lines) + "\n"
    output_path.write_text(markdown, encoding="utf-8")
    return markdown


def build_report_pdf(analysis_bundle: dict[str, Any], output_path: Path) -> Path:
    """Render a polished PDF report for client submission."""

    kpis = analysis_bundle["kpis"]
    narrative = analysis_bundle["narrative"]
    chart_paths = analysis_bundle["chart_paths"]
    monthly_summary = analysis_bundle["monthly_summary"]
    product_summary = analysis_bundle["product_summary"]
    category_summary = analysis_bundle["category_summary"]
    region_summary = analysis_bundle["region_summary"]
    matrix_summary = analysis_bundle["matrix_summary"]
    anomalies = analysis_bundle["anomalies"]
    high_sales_low_margin = analysis_bundle["high_sales_low_margin"]
    slow_movers = analysis_bundle["slow_movers"]
    pareto = analysis_bundle["pareto"]

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TitleCenter", parent=styles["Title"], alignment=TA_CENTER, textColor=colors.HexColor("#0f4c5c"), spaceAfter=12))
    styles.add(ParagraphStyle(name="SectionHeading", parent=styles["Heading2"], textColor=colors.HexColor("#173f5f"), spaceBefore=8, spaceAfter=6))
    styles.add(ParagraphStyle(name="Body", parent=styles["BodyText"], leading=13, spaceAfter=6))
    styles.add(ParagraphStyle(name="BulletBody", parent=styles["BodyText"], leftIndent=12, bulletIndent=0, leading=13, spaceAfter=3))

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
    )

    elements: list[Any] = []
    elements.append(Paragraph("Sales Performance & Business Insights Report", styles["TitleCenter"]))
    elements.append(Paragraph(f"Prepared for {PERSONA_NAME}", styles["Heading3"]))
    elements.append(Paragraph(PERSONA_DESCRIPTION, styles["Body"]))
    elements.append(Spacer(1, 0.12 * inch))

    kpi_table = Table(
        [
            ["Total Revenue", "Total Profit", "Profit Margin", "Orders", "Avg Order Value"],
            [
                f"${kpis['total_revenue']:,.0f}",
                f"${kpis['total_profit']:,.0f}",
                f"{kpis['profit_margin']:.1f}%",
                f"{int(kpis['total_orders']):,}",
                f"${kpis['avg_order_value']:,.2f}",
            ],
        ],
        colWidths=[1.3 * inch] * 5,
    )
    kpi_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f4c5c")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#f4f7f9")),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c9d4df")),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ]
        )
    )
    elements.append(kpi_table)
    elements.append(Spacer(1, 0.16 * inch))

    elements.append(Paragraph("Executive Summary", styles["SectionHeading"]))
    for bullet in narrative["executive_summary"]:
        elements.append(Paragraph(bullet, styles["BulletBody"], bulletText="-"))

    elements.append(Spacer(1, 0.08 * inch))
    elements.append(Paragraph("Revenue Trend", styles["SectionHeading"]))
    elements.append(Image(str(chart_paths["monthly_revenue_profit"]), width=6.9 * inch, height=3.2 * inch))
    elements.append(Paragraph(f"Peak month: {monthly_summary.sort_values('revenue', ascending=False).iloc[0]['month_year']}. The chart shows the year-end lift that Meridian Home Goods should staff and stock for.", styles["Body"]))

    elements.append(Paragraph("Product Performance", styles["SectionHeading"]))
    elements.append(Image(str(chart_paths["top_products_revenue"]), width=6.9 * inch, height=3.9 * inch))
    elements.append(Spacer(1, 0.05 * inch))
    elements.append(Image(str(chart_paths["top_products_profit"]), width=6.9 * inch, height=3.9 * inch))
    elements.append(Paragraph(
        f"Top revenue product: {product_summary.iloc[0]['product_name']}; top profit product: {product_summary.sort_values('profit', ascending=False).iloc[0]['product_name']}. "
        f"{len(high_sales_low_margin)} products are high-volume but low-margin, which makes discount control a profit lever.",
        styles["Body"],
    ))

    elements.append(PageBreak())
    elements.append(Paragraph("Category and Regional Profitability", styles["SectionHeading"]))
    elements.append(Image(str(chart_paths["category_performance"]), width=6.9 * inch, height=3.3 * inch))
    elements.append(Spacer(1, 0.06 * inch))
    elements.append(Image(str(chart_paths["regional_performance"]), width=6.9 * inch, height=3.3 * inch))

    category_rollup = category_summary.groupby("category", as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
    category_rollup["profit_margin"] = np.where(category_rollup["revenue"] != 0, (category_rollup["profit"] / category_rollup["revenue"]) * 100, np.nan)
    region_rollup = region_summary.groupby("region", as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
    region_rollup["profit_margin"] = np.where(region_rollup["revenue"] != 0, (region_rollup["profit"] / region_rollup["revenue"]) * 100, np.nan)
    elements.append(Paragraph(
        f"Highest category revenue comes from {category_rollup.sort_values('revenue', ascending=False).iloc[0]['category']}, while {region_rollup.sort_values('profit_margin', ascending=False).iloc[0]['region']} leads on margin.",
        styles["Body"],
    ))

    elements.append(Paragraph("Growth Opportunity Quadrant", styles["SectionHeading"]))
    elements.append(Image(str(chart_paths["quadrant_view"]), width=6.9 * inch, height=4.8 * inch))
    elements.append(Paragraph(
        f"The quadrant analysis shows {int((matrix_summary['quadrant'] == 'Double Down').sum())} Double Down opportunities and {int((matrix_summary['quadrant'] == 'Fix Margin').sum())} Fix Margin pockets. That distinction is the practical guide for next-month planning.",
        styles["Body"],
    ))

    elements.append(Paragraph("Anomalies and Margin Risk", styles["SectionHeading"]))
    if anomalies.empty:
        elements.append(Paragraph("No material anomalies were detected in the monthly revenue series.", styles["Body"]))
    else:
        for _, row in anomalies.iterrows():
            elements.append(Paragraph(f"{row['month_year']}: {row['reason']}.", styles["BulletBody"], bulletText="-"))
    elements.append(Paragraph(f"{len(slow_movers)} slow movers were identified for repricing or discontinuation review.", styles["Body"]))
    elements.append(Paragraph(f"Pareto check: {pareto['products_to_80_revenue']} products drive roughly {pareto['revenue_share_top_products'] * 100:.1f}% of revenue.", styles["Body"]))

    elements.append(Paragraph("Actionable Recommendations", styles["SectionHeading"]))
    for recommendation in narrative["recommendations"]:
        elements.append(Paragraph(recommendation["title"], styles["Heading4"]))
        elements.append(Paragraph(recommendation["action"], styles["Body"]))
        elements.append(Paragraph(recommendation["impact"], styles["Body"]))

    elements.append(Paragraph("Limitations & Next Steps", styles["SectionHeading"]))
    elements.append(Paragraph("This analysis is based on sales orders only. To make the next planning cycle stronger, Meridian Home Goods should connect inventory, supplier cost, and marketing data so the team can compare revenue growth with true contribution margin.", styles["Body"]))
    elements.append(Paragraph("If more data becomes available, the next analysis should isolate stockouts, customer retention, and channel-level acquisition cost.", styles["Body"]))

    doc.build(elements)
    return output_path
