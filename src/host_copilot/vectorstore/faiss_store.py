"""FAISS index (approximate NN). Implement in M4 (docs/05_faiss.md).

Teaching goal: ANN vs exact, IndexFlatIP vs IVF/HNSW, recall/speed tradeoff, persistence.
"""

from __future__ import annotations

import numpy as np


class FaissStore:
    def __init__(self, dim: int) -> None:
        # TODO M4: build a faiss index (start with IndexFlatIP, then try IVF/HNSW)
        raise NotImplementedError

    def add(self, vectors: np.ndarray, ids: list) -> None:
        raise NotImplementedError

    def search(self, query_vec: np.ndarray, k: int = 8) -> list[tuple]:
        """Return [(id, score)] top-k. TODO M4."""
        raise NotImplementedError

    def save(self, path: str) -> None:
        raise NotImplementedError

    @classmethod
    def load(cls, path: str) -> "FaissStore":
        raise NotImplementedError
