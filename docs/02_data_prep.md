# M1 — Data foundation

**Goal:** clean listings into a tidy DataFrame, define the **peer group** key, and turn each listing into
one text **document** + metadata. This is the raw material RAG retrieves.

**Skills:** pandas cleaning, robust price parsing, feature bucketing, designing a retrieval document.

## The data (in `data_airbnb_bordeaux/` — see [`DATA.md`](DATA.md) to download)

- `listings.csv` — one row per listing. Key columns: `id, name, description, neighborhood_overview,
  amenities, price, room_type, accommodates, bedrooms, neighbourhood_cleansed, minimum_nights,
  review_scores_rating, review_scores_cleanliness, review_scores_location, review_scores_value,
  number_of_reviews, estimated_occupancy_l365d, estimated_revenue_l365d`. **Note multiline quoted
  descriptions** — let pandas handle quoting (default), don't split lines yourself.
- `price` is a string like `"$1,234.00"` → must parse to float.

## What is a "peer group"?

Comps must be *comparable*. Define the peer key as:
```
neighbourhood_cleansed | room_type | accommodates-band
```
Bands: 1-2, 3-4, 5-6, 7+. A 2-bedroom entire flat in Chartrons should only be compared to similar
capacity/type in the same area — otherwise the price advice is meaningless.

## Steps (implement in `src/host_copilot/data/loaders.py` + `documents.py`)

1. `parse_price("$1,234.00") -> 1234.0`; empty/NaN → `None`. Strip `$` and `,`.
2. `accommodates_band(n)` → `"1-2" | "3-4" | "5-6" | "7+"` using `ACCOMMODATES_BANDS`.
3. `peer_key(neigh, room_type, accommodates)` → `f"{neigh}|{room_type}|{band}"`.
4. `load_listings()` → read CSV, parse price, drop rows with no price or no description, add a `peer_key`
   column. Return the DataFrame.
5. `load_reviews()` → read `reviews.csv`, keep `listing_id, date, comments`, drop empty comments.
6. In `documents.py`: `listing_to_document(row)` concatenates name + description + amenities +
   neighbourhood + a short scores line into one passage. `listing_metadata(row)` returns a flat dict
   (`id, peer_key, price, room_type, neighbourhood_cleansed, review_scores_rating, ...`) — Chroma
   metadata must be str/int/float/bool only.

## Safe checkpoint

- Unskip the three tests in `tests/test_loaders.py` (remove the `@pytest.mark.skip` lines) → green.
- In a notebook: `load_listings().shape` looks sane (a few thousand rows), `peer_key` has no nulls,
  `price` is numeric.

## Commit

```
feat(host_copilot): data loaders, peer key, listing documents (M1)
```

Next → [`03_chunking_embeddings.md`](03_chunking_embeddings.md).
