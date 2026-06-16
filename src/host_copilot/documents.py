"""Turn a listing row into one embeddable text document + metadata. Implement in M1/M2."""

from __future__ import annotations

import pandas as pd


def listing_to_document(row: pd.Series) -> str:
    """Compose name + description + amenities + neighbourhood + scores into one passage. TODO M1."""
    raise NotImplementedError


def listing_metadata(row: pd.Series) -> dict:
    """Metadata stored alongside the vector: id, peer_key, price, room_type, scores... TODO M1."""
    raise NotImplementedError
