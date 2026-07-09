# FUTURE_DS_01
# Meridian Home Goods Sales Performance & Business Insights

A client-ready sales analytics project for **Meridian Home Goods**, a fictional local retail shop that sells furniture, office supplies, and compact technology products. The project answers the questions a business owner actually cares about: what drives revenue, which items create profit, which regions and categories are worth scaling, and where discounting is quietly eroding margin.

## Project Structure

- `data/raw` - raw input data or synthetic raw extract
- `data/processed` - cleaned dataset used for analysis and dashboarding
- `notebooks` - exploratory notebook version of the analysis
- `scripts` - reusable cleaning, analysis, and report-generation code
- `dashboard` - Streamlit dashboard application
- `reports` - client-ready report, data notes, and cleaning log
- `assets/charts` - exported charts for the report and README
- `assets/exports` - tables and dashboard-ready extracts

## Tech Stack

- Python
- pandas and numpy for data preparation and analysis
- matplotlib for static report charts
- Plotly and Streamlit for the interactive dashboard
- reportlab for the PDF report

## How To Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Build the full analysis pipeline:

```bash
python scripts/run_pipeline.py
```

3. Launch the dashboard:

```bash
streamlit run dashboard/streamlit_app.py
```

## Business Context

Persona: **Meridian Home Goods**, a local retail shop.

The dashboard and report are written as if they were prepared for the owner of this business. The analysis is intentionally focused on revenue, profit margin, seasonality, product mix, and growth opportunities rather than generic charting.

## Key Results Summary

Meridian Home Goods generated **$508,199** in revenue across **938 orders** with **$33,476** in profit, for a **6.6%** overall margin.

- Peak month: **March**; weakest month: **January**.
- Top revenue product: **Premium Standing Desk** at **$148,615**.
- Top profit product: **Smart LED Monitor** at **$23,243**.
- Best region by margin: **Central** at **11.1%**.
- Best category by margin: **Office Supplies**.
- Only **3 of 16 products** drive about **80% of revenue**, so SKU focus matters.

Artifacts produced by the pipeline:

- Cleaned dataset: `data/processed/sales_cleaned.csv`
- Cleaning log: `reports/data_cleaning_log.md`
- Client report: `reports/client_report.pdf`
- Report source: `reports/client_report.md`
- Dashboard screenshot: `assets/charts/dashboard_screenshot.png`
- Static charts: `assets/charts/`
- Dashboard-ready extracts: `assets/exports/`

## Outputs

- Full report PDF: `reports/client_report.pdf`
- Full report source: `reports/client_report.md`
- Data notes: `reports/data_notes.md`
- Cleaning log: `reports/data_cleaning_log.md`
- Dashboard screenshots/charts: `assets/charts/`

## Notes

If no client dataset is provided, the project generates a realistic synthetic sales dataset that mimics a Superstore-style retail file with seasonal demand, top-performing products, and margin variation across regions and categories.
