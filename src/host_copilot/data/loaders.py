"""CSV loading + cleaning. Implement in M1 (docs/02_data_prep.md)."""

from __future__ import annotations

import pandas as pd

from host_copilot.config import get_settings

ACCOMMODATES_BANDS = [(1, 2), (3, 4), (5, 6), (7, 99)]

_KEY_COLS = ["price", "description", "neighbourhood_cleansed", "room_type", "accommodates"]


def parse_price(raw: str | float) -> float | None:
    """'$1,234.00' -> 1234.0 ; '' / NaN / unparseable -> None."""
    if isinstance(raw, (int, float)):
        return None if pd.isna(raw) else float(raw)
    if raw is None:
        return None
    s = str(raw).strip().replace("$", "").replace(",", "")
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def accommodates_band(n: int) -> str:
    """Map a capacity to a band label, e.g. 3 -> '3-4', 9 -> '7+'."""
    n = int(n)
    for lo, hi in ACCOMMODATES_BANDS:
        if lo <= n <= hi:
            return f"{lo}+" if hi >= 99 else f"{lo}-{hi}"
    return f"{ACCOMMODATES_BANDS[-1][0]}+"


def peer_key(neighbourhood: str, room_type: str, accommodates: int) -> str:
    """Stable comp-group key: neighbourhood | room_type | band."""
    return f"{neighbourhood}|{room_type}|{accommodates_band(accommodates)}"


def load_listings() -> pd.DataFrame:
    """Read listings.csv, clean price, drop dead rows, add peer_key column."""
    df = pd.read_csv(get_settings().data_path / "listings.csv", encoding="utf-8")
    df["price"] = df["price"].map(parse_price)
    df = df.dropna(subset=_KEY_COLS)
    df = df[df["description"].str.strip() != ""]
    df["peer_key"] = df.apply(
        lambda r: peer_key(r["neighbourhood_cleansed"], r["room_type"], r["accommodates"]),
        axis=1,
    )
    return df.reset_index(drop=True)


def load_reviews() -> pd.DataFrame:
    """Read reviews.csv (listing_id, date, comments)."""
    df = pd.read_csv(
        get_settings().data_path / "reviews.csv",
        usecols=["listing_id", "date", "comments"],
    )
    df = df.dropna(subset=["comments"])
    df = df[df["comments"].str.strip() != ""]
    return df.reset_index(drop=True)
