"""Comp retrieval: peer-group filter + top-k + hybrid. Implement in M6 (docs/07_retrieval.md)."""

from __future__ import annotations


def get_comps(listing_id: int, k: int = 8) -> list[dict]:
    """Find comparable listings: same peer_key, nearest by embedding, excluding self. TODO M6."""
    raise NotImplementedError


def hybrid_search(query: str, peer_key: str, k: int = 8) -> list[dict]:
    """Combine semantic (vector) + keyword (BM25) scores, then rerank. TODO M6."""
    raise NotImplementedError
