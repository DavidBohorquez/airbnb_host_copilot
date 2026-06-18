"""Brute-force cosine search from scratch. M3 (docs/04_search_numpy.md).

Teaching goal: understand exact search and the cosine/dot/L2 relationship before using a library.
"""

from __future__ import annotations

import numpy as np


class NumpyStore:
    def __init__(self, vectors: np.ndarray, ids: list) -> None:
        self.vectors = vectors  # (n, d), assumed L2-normalized
        self.ids = ids

    def search(self, query_vec: np.ndarray, k: int = 8) -> list[tuple]:
        """Return [(id, score)] top-k by cosine similarity (higher = closer)."""
        scores = self.vectors @ query_vec  # normalized vectors -> dot == cosine
        return self._topk(scores, k, largest=True)

    def search_l2(self, query_vec: np.ndarray, k: int = 8) -> list[tuple]:
        """Return [(id, distance)] top-k by L2 distance (lower = closer).

        For unit vectors the ranking matches cosine; only the scores differ.
        """
        dists = np.linalg.norm(self.vectors - query_vec, axis=1)
        return self._topk(dists, k, largest=False)

    def _topk(self, values: np.ndarray, k: int, largest: bool) -> list[tuple]:
        k = min(k, len(self.ids))
        order = -values if largest else values
        idx = np.argpartition(order, k - 1)[:k]
        idx = idx[np.argsort(order[idx])]
        return [(self.ids[i], float(values[i])) for i in idx]