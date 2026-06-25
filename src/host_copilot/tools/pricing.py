"""Price analytics vs comps. Implement in M7 (docs/08_analytics_tools.md).

Returns a typed dict the LLM can cite (no prose here — that's the LLM's job).
"""

from __future__ import annotations

from functools import lru_cache

import numpy as np
import pandas as pd

from host_copilot.data.loaders import load_listings


@lru_cache
def _listings() -> pd.DataFrame:
    return load_listings()


def price_position(listing_id: int) -> dict:
    """Price percentiles of the listing's peer group + where this listing sits (percentile = % of comps at or below)."""
    df = _listings()
    row = df[df["id"] == listing_id]
    if row.empty:
        raise KeyError(listing_id)
    pk = row.iloc[0]["peer_key"]
    listing_price = float(row.iloc[0]["price"])

    peers = df[df["peer_key"] == pk]["price"].astype(float)
    p25, p50, p75 = (float(x) for x in np.percentile(peers, [25, 50, 75]))
    percentile = float((peers <= listing_price).mean() * 100)

    return {
        "peer_key": pk,
        "n_comps": int(len(peers)),
        "p25": round(p25, 2),
        "p50": round(p50, 2),
        "p75": round(p75, 2),
        "listing_price": round(listing_price, 2),
        "percentile": round(percentile, 1),
    }
