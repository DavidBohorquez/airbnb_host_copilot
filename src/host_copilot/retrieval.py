"""Comp retrieval: peer-group filter + top-k + hybrid. Implement in M6 (docs/07_retrieval.md)."""

from __future__ import annotations

from functools import lru_cache

import numpy as np
from rank_bm25 import BM25Okapi

from host_copilot.embeddings import Embedder
from host_copilot.vectorstore.chroma_store import ChromaStore

RRF_K = 60

@lru_cache
def _embedder() -> Embedder:
    return Embedder()


@lru_cache
def _store() -> ChromaStore:
    return ChromaStore()


def get_comps(listing_id: int, k: int = 8) -> list[dict]:
    """Find comparable listings: same peer_key, nearest by embedding, excluding self. TODO M6."""
    store = _store()
    rec = store.get(listing_id)
    pk = rec["metadata"]["peer_key"]
    res = store.query(rec["embedding"], k=k + 1, where={"peer_key": pk})
    comps = [r for r in res if str(r["id"]) != str(listing_id)]
    return comps[:k]


def hybrid_search(query: str, peer_key: str, k: int = 8) -> list[dict]:
    """Combine semantic (vector) + keyword (BM25) scores, then rerank. TODO M6."""
    store = _store()
    group = store.get_group(peer_key)
    ids, docs, metas = group["ids"], group["documents"], group["metadatas"]
    if not ids:
        return []
    meta_by_id = dict(zip(ids, metas))

    # semantic ranking (position in the vector-search result = rank)
    sem = store.query(_embedder().encode_query(query), k=len(ids), where={"peer_key": peer_key})
    sem_rank = {r["id"]: i for i, r in enumerate(sem)}

    # keyword ranking
    bm = BM25Okapi([d.lower().split() for d in docs])
    order = np.argsort(-bm.get_scores(query.lower().split()))
    bm_rank = {ids[idx]: rank for rank, idx in enumerate(order)}

    def rrf(_id: str) -> float:
        score = 0.0
        if _id in sem_rank:
            score += 1.0 / (RRF_K + sem_rank[_id])
        if _id in bm_rank:
            score += 1.0 / (RRF_K + bm_rank[_id])
        return score

    top = sorted(ids, key=rrf, reverse=True)[:k]
    return [{"id": i, "score": rrf(i), "metadata": meta_by_id[i]} for i in top]















