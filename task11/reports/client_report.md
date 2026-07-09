# Sales Performance & Business Insights Report - Meridian Home Goods

## Executive Summary
- Meridian Home Goods generated $508,199 in revenue across 938 orders and $33,476 in profit, leaving the business at 6.6% margin.
- Demand is clearly seasonal: March is the strongest month, while January is the weakest, so inventory and staffing should follow that rhythm.
- Premium Standing Desk leads revenue, while Smart LED Monitor leads profit. That split matters because the business is not simply winning on turnover; margin management still needs attention.
- The Central region is the most efficient market at 11.1% margin, while Furniture leads category revenue and Office Supplies leads category margin.
- Only 3 of 16 products drive 80% of revenue, which means the assortment is concentrated enough to reward tighter SKU management.

## Business Objective & Approach
This engagement focuses on the questions a real retail owner would ask before making a Monday-morning decision: where revenue comes from, which products actually create profit, which markets deserve more investment, and where discounting is quietly eroding margin.
The analysis uses 938 cleaned orders from a realistic synthetic dataset designed to behave like a small retail store with seasonal demand, mixed-margin products, and regional performance differences.

## Data Overview & Methodology
The raw file included mixed date formats, currency strings, duplicate orders, missing values, and invalid quantities. The cleaning process standardized those fields, removed invalid rows, and derived month-year, quarter, profit margin, revenue per unit, and discount impact.
Final cleaned dataset size: 938 order lines supporting the trend analysis, 16 unique products, 13 category/sub-category combinations, and 19 region/state combinations.

## Key Findings - Revenue Trends
Monthly revenue peaked in March and bottomed out in January. The monthly line chart shows that Q4 is the strongest stretch, which is consistent with holiday retail behavior.
Quarterly revenue growth should be monitored because the trend is not linear; it accelerates late in the year and slows materially at the start of the year.
Anomaly review flagged 11 month(s) that moved sharply away from trend and should be investigated instead of assumed to be normal seasonality.

## Key Findings - Product Performance
Top revenue product: Premium Standing Desk at $148,615. Top profit product: Smart LED Monitor at $23,243.
That difference matters because the most visible revenue item is not always the most valuable one after discounting and shipping are taken into account.
3 products fall into the high-sales, low-margin bucket and should be treated as discount-control candidates.
3 products account for about 77.1% of total revenue, which means the assortment is concentrated enough that SKU discipline will matter.
1 slow-moving products sit in the low-revenue, low-profit bucket and are candidates for repricing, bundling, or discontinuation.

## Key Findings - Category and Regional Profitability
Highest revenue category: Furniture. Highest margin category: Office Supplies.
Highest margin region: Central. The region/category matrix shows where the business should double down and where it should fix margin before trying to grow volume.

## Growth Opportunities
The quadrant chart separates the business into four actions: Double Down, Fix Margin, Build Demand, and Deprioritize. This keeps revenue problems distinct from margin problems, which is the key analytical mistake most beginner dashboards make.

## Actionable Recommendations
### Recommendation 1: Tighten discounting where revenue is strong but margins are lagging
- Action: Review pricing and discounts in East / Furniture. That pocket generated $83,701 in revenue but only -0.0% margin.
- Estimated impact: If that segment lifted margin to the portfolio median, annual profit would improve by roughly $13,059.

### Recommendation 2: Reduce discount leakage on the highest-volume low-margin product
- Action: Premium Standing Desk is producing $148,615 in revenue but only 0.8% margin. Cap promo depth and test a smaller bundle incentive instead of broad discounting.
- Estimated impact: A 3-point margin lift on this product alone would add about $4,458 in annual profit.

### Recommendation 3: Scale the best-performing growth pocket
- Action: Increase local marketing and inventory priority in West / Technology. It combines $62,240 of revenue with 17.9% margin.
- Estimated impact: A 10% revenue lift in this pocket would contribute about $1,114 of additional profit at the current margin.

### Recommendation 4: Deprioritize slow movers that tie up cash without creating profit
- Action: Modular Bookshelf sits in the low-revenue, low-profit bucket. Reprice it, replace it, or stop carrying excess stock.
- Estimated impact: Reducing inventory exposure on this item can free working capital and avoid roughly $59.95 of annual profit drag.

## Limitations & Next Steps
- This is a single-entity sales file, so profitability is observed at the order line level rather than with full customer lifetime value.
- The synthetic dataset is designed to be realistic, but a production engagement would also examine inventory turns, stockouts, customer cohorts, and acquisition channel performance.
- If more data were available, the next analysis would join marketing spend and inventory records to quantify true contribution margin by channel and stock position.

## Appendix
- Full monthly summary table exported to `assets/exports/monthly_summary.csv`.
- Full product, category, region, anomaly, and quadrant tables exported to `assets/exports/`.
- Dashboard screenshots and static charts saved to `assets/charts/`.

Headline KPIs: revenue $508,199, profit $33,476, margin 6.6%, orders 938, average order value $541.79.
