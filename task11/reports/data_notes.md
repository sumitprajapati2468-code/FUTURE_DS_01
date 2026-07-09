# Data Notes

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
