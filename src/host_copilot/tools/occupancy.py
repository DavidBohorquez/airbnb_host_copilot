"""Occupancy / demand from the 4.5M-row calendar. Implement in M7 (docs/08_analytics_tools.md).

Use DuckDB to query calendar.csv directly — never load it fully into pandas.
"""

from __future__ import annotations

from functools import lru_cache

import duckdb
import pandas as pd


from host_copilot.config import get_settings
from host_copilot.tools.pricing import _listings


@lru_cache
def _occupancy_by_listing() -> pd.DataFrame:
    path = str(get_settings().data_path / "calendar.csv")
    return duckdb.sql(
        f"""
        SELECT listing_id,
                AVG(CASE WHEN available = 'f' THEN 1.0 ELSE 0.0 END) AS occ
        FROM read_csv_auto('{path}')
        GROUP BY listing_id
        """
    ).df()


def occupancy_stats(listing_id: int) -> dict:
    """Booked-night ratio for the listing vs its peer-group median, from calendar availability."""
    occ = _occupancy_by_listing()
    listings = _listings()[["id", "peer_key"]]
    merged = occ.merge(listings, left_on="listing_id", right_on="id", how="inner")

    row = merged[merged["listing_id"] == listing_id]
    if row.empty:
        raise KeyError(listing_id)
    pk = row.iloc[0]["peer_key"]
    peer_median = float(merged[merged["peer_key"] == pk]["occ"].median())

    return {
        "listing_occupancy": round(float(row.iloc[0]["occ"]), 3),
        "peer_median_occupancy": round(peer_median, 3),
    }
