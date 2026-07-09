"""Command-line entry point for the sales performance project pipeline."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.sales_analysis import (
    DATA_DIR,
    ASSETS_DIR,
    PROCESSED_DIR,
    RAW_DIR,
    REPORTS_DIR,
    build_report_markdown,
    build_report_pdf,
    clean_sales_data,
    ensure_project_directories,
    export_analysis_bundle,
    export_data_notes,
    export_summary_artifacts,
    generate_synthetic_sales_data,
    save_dataframe,
)


def main() -> None:
    """Run the complete end-to-end sales analysis workflow."""

    ensure_project_directories()
    export_data_notes(REPORTS_DIR / "data_notes.md")

    raw_path = RAW_DIR / "sales_raw.csv"
    if raw_path.exists():
        raw_df = pd.read_csv(raw_path)
    else:
        raw_df = generate_synthetic_sales_data()
        save_dataframe(raw_df, raw_path)

    cleaning_result = clean_sales_data(raw_df)
    cleaned_df = cleaning_result.dataframe

    save_dataframe(cleaned_df, PROCESSED_DIR / "sales_cleaned.csv")
    save_dataframe(cleaned_df, DATA_DIR / "sales_cleaned_export.csv")

    analysis_bundle = export_analysis_bundle(cleaned_df, ASSETS_DIR)
    analysis_bundle["cleaning_log"] = cleaning_result.log_lines
    export_summary_artifacts(cleaned_df, analysis_bundle)
    build_report_markdown(analysis_bundle, REPORTS_DIR / "client_report.md")
    build_report_pdf(analysis_bundle, REPORTS_DIR / "client_report.pdf")

    print("Pipeline completed successfully.")
    print(f"Raw data: {raw_path}")
    print(f"Cleaned data: {PROCESSED_DIR / 'sales_cleaned.csv'}")
    print(f"Report: {REPORTS_DIR / 'client_report.md'}")


if __name__ == "__main__":
    main()
