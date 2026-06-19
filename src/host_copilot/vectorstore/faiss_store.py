"""FAISS index (approximate NN). Implement in M4 (docs/05_faiss.md).

Teaching goal: ANN vs exact, IndexFlatIP vs IVF/HNSW, recall/speed tradeoff, persistence.
"""

from __future__ import annotations

import faiss
import numpy as np


class FaissStore:
    def __init__(self, dim: int, index_type: str = "flat", nlist: int = 100) -> None:
        self.dim = dim
        self.ids: list = []
        if index_type == "ivf":
            quantizer = faiss.IndexFlatIP(dim)
            self.index = faiss.IndexIVFFlat(quantizer, dim, nlist, faiss.METRIC_INNER_PRODUCT)
        else:
            self.index = faiss.IndexFlatIP(dim)

    @property
    def nprobe(self) -> int:
        return getattr(self.index, "nprobe", 1)

    @nprobe.setter
    def nprobe(self, value: int) -> None:
        self.index.nprobe = value

    def add(self, vectors: np.ndarray, ids: list) -> None:
        v = np.ascontiguousarray(vectors, dtype="float32")
        if not self.index.is_trained:
            self.index.train(v)
        self.index.add(v)
        self.ids.extend(list(ids))

    def search(self, query_vec: np.ndarray, k: int = 8) -> list[tuple]:
        """Return [(id, score)] top-k (inner product == cosine)."""
        q = np.ascontiguousarray(query_vec, dtype="float32").reshape(1, -1)
        scores, idx = self.index.search(q, k)
        return [(self.ids[i], float(s)) for s, i in zip(scores[0], idx[0]) if i != -1]

    def save(self, path: str) -> None:
        path = str(path)
        faiss.write_index(self.index, path)
        np.save(path + ".ids.npy", np.array(self.ids))

    @classmethod
    def load(cls, path: str) -> "FaissStore":
        path = str(path)
        index = faiss.read_index(path)
        store = cls.__new__(cls)
        store.dim = index.d
        store.index = index
        store.ids = np.load(path + ".ids.npy", allow_pickle=True).tolist()
        return store
