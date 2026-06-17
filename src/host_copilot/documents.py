"""Turn a listing row into one embeddable text document + metadata. Implement in M1/M2."""

from __future__ import annotations

import pandas as pd

_SCORE_COLS = [
    "review_scores_rating",
    "review_scores_cleanliness",
    "review_scores_location",
    "review_scores_value",
]


def listing_to_document(row: pd.Series) -> str:
    """Compose name + description + amenities + neighbourhood + scores into one passage."""
    scores = ", ".join(f"{c.replace('review_scores_', '')}: {row.get(c)}" for c in _SCORE_COLS)
    parts = [
        str(row.get("name", "")),
        str(row.get("description", "")),
        f"Amenities: {row.get('amenities', '')}",
        f"Neighbourhood: {row.get('neighbourhood_cleansed', '')}",
        f"Scores - {scores}",
    ]
    return "\n".join(p for p in parts if p and p.strip() and p != "nan")


def listing_metadata(row: pd.Series) -> dict:
    """Flat, Chroma-safe metadata (str/int/float/bool only; None values dropped)."""
    meta = {
        "id": int(row["id"]),
        "peer_key": str(row["peer_key"]),
        "price": float(row["price"]),
        "room_type": str(row["room_type"]),
        "neighbourhood_cleansed": str(row["neighbourhood_cleansed"]),
        "accommodates": int(row["accommodates"]),
        "review_scores_rating": row.get("review_scores_rating"),
        "review_scores_cleanliness": row.get("review_scores_cleanliness"),
    }
    return {k: v for k, v in meta.items() if v is not None and not pd.isna(v)}
