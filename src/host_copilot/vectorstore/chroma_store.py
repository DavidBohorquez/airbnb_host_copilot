"""Persistent Chroma store with metadata filtering. Implement in M5 (docs/06_chroma.md).

Teaching goal: production vector DB — collections, upsert, persistence, where-filtering by peer_key.
"""

from __future__ import annotations

import numpy as np

COLLECTION = "listings"


class ChromaStore:
    def __init__(self, persist_dir: str | None = None) -> None:
        # TODO M5: chromadb.PersistentClient(path=persist_dir) + get_or_create_collection
        raise NotImplementedError

    def upsert(self, ids: list, vectors: np.ndarray, metadatas: list[dict], documents: list[str]) -> None:
        raise NotImplementedError

    def query(self, query_vec: np.ndarray, k: int = 8, where: dict | None = None) -> list[dict]:
        """Top-k filtered by metadata (e.g. {'peer_key': ...}). TODO M5."""
        raise NotImplementedError
