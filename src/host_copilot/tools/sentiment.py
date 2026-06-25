"""Review sentiment / complaint mining for an area. Implement in M7 (docs/08_analytics_tools.md)."""

from __future__ import annotations

from functools import lru_cache

import pandas as pd


from host_copilot.data.loaders import load_reviews
from host_copilot.tools.pricing import _listings

_POSITIVE = {
    "great", "perfect", "clean", "comfortable", "lovely", "recommend", "excellent", "amazing",
    "parfait", "propre", "génial", "agréable", "idéal", "recommande", "superbe", "calme",
}
_NEGATIVE = {
    "dirty", "noisy", "noise", "bad", "broken", "rude", "disappointed", "smell", "cold",
    "sale", "bruit", "bruyant", "déçu", "froid", "problème", "cassé", "odeur",
}
_THEMES = {
    "noise": {"noise", "noisy", "loud", "bruit", "bruyant"},
    "cleanliness": {"dirty", "clean", "smell", "sale", "propre", "odeur"},
    "check-in": {"checkin", "check-in", "keys", "arrival", "clés", "arrivée", "code"},
    "location": {"location", "far", "street", "quartier", "loin", "rue"},
    "value": {"expensive", "price", "cher", "prix", "value"},
    "amenities": {"wifi", "heating", "kitchen", "chauffage", "cuisine", "shower", "douche"},
}


@lru_cache
def _review_with_neigh() -> pd.DataFrame:
    reviews = load_reviews()
    listings = _listings()[["id", "neighbourhood_cleansed"]]
    return reviews.merge(listings, left_on="listing_id", right_on="id", how="inner")


def area_sentiment(neighbourhood: str, limit: int = 200) -> dict:
    """Polarity + top complaint themes from a sample of reviews in a neighbourhood."""
    df = _review_with_neigh()
    area = df[df["neighbourhood_cleansed"] == neighbourhood].head(limit)
    if area.empty:
        raise KeyError(neighbourhood)

    pos = 0
    theme_counts = dict.fromkeys(_THEMES, 0)
    for comment in area["comments"].astype(str):
        words = set(comment.lower().split())
        p, n = len(words & _POSITIVE), len(words & _NEGATIVE)
        if p >= n:
            pos += 1
        else:
            for theme, cues in _THEMES.items():
                if words & cues:
                    theme_counts[theme] += 1

    top = sorted(theme_counts.items(), key=lambda kv: kv[1], reverse=True)
    return {
        "n_reviews": int(len(area)),
        "positive_pct": round(pos / len(area) * 100, 1),
        "top_complaints": [t for t, c in top if c > 0][:3],
    }
