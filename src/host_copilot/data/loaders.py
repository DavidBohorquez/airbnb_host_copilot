"""CSV loading + cleaning. Implement in M1 (docs/02_data_prep.md)."""

from __future__ import annotations

import pandas as pd

ACCOMMODATES_BANDS = [(1, 2), (3, 4), (5, 6), (7, 99)]


def parse_price(raw: str | float) -> float | None:
    """'$1,234.00' -> 1234.0 ; '' / NaN -> None. TODO M1."""
    raise NotImplementedError


def accommodates_band(n: int) -> str:
    """Map a capacity to a band label, e.g. 3 -> '3-4'. TODO M1."""
    raise NotImplementedError


def peer_key(neighbourhood: str, room_type: str, accommodates: int) -> str:
    """Stable comp-group key: neighbourhood | room_type | band. TODO M1."""
    raise NotImplementedError


def load_listings() -> pd.DataFrame:
    """Read listings.csv, clean price, drop dead rows, add peer_key column. TODO M1."""
    raise NotImplementedError


def load_reviews() -> pd.DataFrame:
    """Read reviews.csv (listing_id, date, comments). TODO M1."""
    raise NotImplementedError
