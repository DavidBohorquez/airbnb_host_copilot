"""Persistent Chroma store with metadata filtering. Implement in M5 (docs/06_chroma.md).

Teaching goal: production vector DB — collections, upsert, persistence, where-filtering by peer_key.
"""

from __future__ import annotations

import chromadb
import numpy as np

from host_copilot.config import get_settings

COLLECTION = "listings"


class ChromaStore:
    def __init__(self, persist_dir: str | None = None) -> None:
        path = str(persist_dir or get_settings().chroma_path)
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(
            COLLECTION, metadata={"hnsw:space": "cosine"}
        )

    def upsert(
        self,
        ids: list,
        vectors: np.ndarray,
        metadatas: list[dict],
        documents: list[str],
        batch_size: int = 5000,
    ) -> None:
        str_ids = [str(i) for i in ids]
        vecs = np.asarray(vectors)
        for s in range(0, len(str_ids), batch_size):  # Chroma caps batch size
            e = s + batch_size
            self.collection.upsert(
                ids=str_ids[s:e],
                embeddings=vecs[s:e].tolist(),
                metadatas=list(metadatas[s:e]),
                documents=list(documents[s:e]),
            )

    def query(self, query_vec: np.ndarray, k: int = 8, where: dict | None = None) -> list[dict]:
        """Top-k filtered by metadata (e.g. {'peer_key': ...}). Cosine score = 1 - distance."""
        res = self.collection.query(
            query_embeddings=[np.asarray(query_vec).tolist()],
            n_results=k,
            where=where,
        )
        out = []
        for i in range(len(res["ids"][0])):
            out.append(
                {
                    "id": res["ids"][0][i],
                    "score": 1.0 - res["distances"][0][i],
                    "metadata": res["metadatas"][0][i],
                    "document": res["documents"][0][i],
                }
            )
        return out

    def get(self, listing_id) -> dict:
        got = self.collection.get(
            ids=[str(listing_id)], include=["embeddings", "metadatas", "documents"]
        )
        if not got["ids"]:
            raise KeyError(listing_id)
        return {
            "id": got["ids"][0],
            "embedding": np.asarray(got["embeddings"][0]),
            "metadata": got["metadatas"][0],
            "document": got["documents"][0],
        }

    def get_group(self, peer_key: str) -> dict:
        return self.collection.get(where={"peer_key": peer_key}, include=["documents", "metadatas"])

    def count(self) -> int:
        return self.collection.count()
