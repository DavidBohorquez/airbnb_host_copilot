# Data

The CSVs are **not committed** — they are large (`calendar.csv` has ~4.5M rows, well over GitHub's
100 MB per-file limit) and `.gitignore`d. Download them yourself.

## Source

[Inside Airbnb](https://insideairbnb.com/get-the-data/) → city **Bordeaux**. Download the four files
and place them in `data_airbnb_bordeaux/` at the repo root:

```
data_airbnb_bordeaux/
├── listings.csv         # one row per listing (detailed)
├── reviews.csv          # listing_id, date, comments (FR/EN)
├── calendar.csv         # listing_id, date, available, price  (huge)
└── neighbourhoods.csv   # neighbourhood list
```

## Schema (columns used)

- **listings.csv**: `id, name, description, neighborhood_overview, amenities, price, room_type,
  accommodates, bedrooms, neighbourhood_cleansed, minimum_nights, review_scores_rating,
  review_scores_cleanliness, review_scores_location, review_scores_value, number_of_reviews,
  estimated_occupancy_l365d, estimated_revenue_l365d`. `price` is a string like `"$1,234.00"`.
- **reviews.csv**: `listing_id, id, date, reviewer_id, reviewer_name, comments`.
- **calendar.csv**: `listing_id, date, available (f/t), price, adjusted_price, minimum_nights`.
  Query with DuckDB — never load it whole into pandas.
- **neighbourhoods.csv**: `neighbourhood_group, neighbourhood`.

## Override the location

If you keep the data elsewhere, set `DATA_DIR` in `.env` to that path (absolute or relative to the
repo root). `config.py` resolves all data access through it.
