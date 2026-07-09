# Data Cleaning Log

- Initial rows received: 966
- Removed 18 duplicate rows copied from the raw extract.
- Removed 0 duplicated order_id values.
- Parsed mixed date formats in order_date; 0 rows could not be interpreted.
- Filled 4 missing customer_id values with 'Unknown Customer'.
- Filled 3 missing discount values using category medians and overall median fallback.
- Filled 3 missing state values from region-level modes.
- Removed 6 rows with zero or negative quantities.
- Removed 4 rows with missing critical analytical fields.
- Final rows retained after cleaning: 938
- Net rows removed during cleaning: 28
