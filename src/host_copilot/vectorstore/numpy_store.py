"""Brute-force cosine search from scratch. Implement in M3 (docs/04_search_numpy.md).

Teaching goal: understand exact search and the cosine/dot/L2 relationship before using a library.
"""

from __future__ import annotations

import numpy as np


class NumpyStore:
    def __init__(self, vectors: np.ndarray, ids: list) -> None:
        self.vectors = vectors  # (n, d), assumed L2-normalized
        self.ids = ids

    def search(self, query_vec: np.ndarray, k: int = 8) -> list[tuple]:
        """Return [(id, score)] top-k by cosine similarity. TODO M3."""
        raise NotImplementedError
