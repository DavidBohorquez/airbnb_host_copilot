# M7 — Analytics tools

**Goal:** the functions that compute hard numbers the LLM cannot eyeball. Each returns a typed dict; no
prose (the LLM writes prose in M9).

**Skills:** turning data into callable "tools", DuckDB over a huge CSV, lightweight sentiment.

## The three tools

### `tools/pricing.py::price_position(listing_id)`
- Gather the peer group's prices (from the listings DataFrame, same `peer_key`).
- Return `{p25, p50, p75, listing_price, percentile}` — where the listing sits among comps.

### `tools/occupancy.py::occupancy_stats(listing_id)`
- `calendar.csv` is **4.5M rows** — do **not** `pd.read_csv` it whole. Query it with DuckDB:
  ```python
  duckdb.sql("SELECT listing_id, AVG(available='f') AS occ FROM 'calendar.csv' GROUP BY listing_id")
  ```
  (`available='f'` means booked/unavailable → proxy for demand.)
- Return `{listing_occupancy, peer_median_occupancy}`.

### `tools/sentiment.py::area_sentiment(neighbourhood)`
- Pull a sample of reviews for listings in that neighbourhood.
- Classify polarity (start simple: a multilingual sentiment pipeline from `transformers`, or a lexicon).
- Extract recurring complaint themes (noise, cleanliness, check-in...). Return
  `{positive_pct, top_complaints}`.

## Why typed dicts?

In M9 the LLM calls these as tools and must **cite** the numbers. Structured output keeps it grounded and
prevents hallucinated prices.

## Safe checkpoint

- Each function runs standalone for a real `listing_id` / neighbourhood and returns the documented keys.
- The DuckDB occupancy query returns in a few seconds, not minutes, and never loads the full file into RAM.

## Commit

```
feat(host_copilot): pricing, occupancy (duckdb), sentiment tools (M7)
```

Next → [`09_llm_abstraction.md`](09_llm_abstraction.md).
