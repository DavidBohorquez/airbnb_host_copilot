# M6 — Retrieval logic

**Goal:** the retrieval layer Host Copilot actually calls: given a `listing_id`, return its valid comps;
given a free-text need, run hybrid (semantic + keyword) search.

**Skills:** peer-group filtering, top-k comp selection, hybrid search, the idea of reranking.

## Concepts

- **Comps for a listing** = nearest neighbours *within the same `peer_key`*, excluding the listing itself.
  This is where M5's metadata filter pays off.
- **Hybrid search** = combine **semantic** (embeddings — captures meaning, handles synonyms/translation)
  with **keyword/BM25** (exact terms — catches "rooftop", "parking", proper nouns the embedding may blur).
  Score = weighted sum or Reciprocal Rank Fusion (RRF). Hybrid usually beats either alone.
- **Reranking** (optional stretch) = take top-N from hybrid, rescore with a cross-encoder for precision.

## Steps (implement in `src/host_copilot/retrieval.py`)

1. `get_comps(listing_id, k)`:
   - look up the listing's `peer_key` + its stored vector,
   - `ChromaStore.query(vec, k+1, where={"peer_key": pk})`,
   - drop the listing itself, return up to `k` comps with metadata.
2. `hybrid_search(query, peer_key, k)`:
   - semantic: `encode_query` → Chroma query (filtered by `peer_key`),
   - keyword: BM25 over the same peer-group documents (use `rank_bm25` or a simple TF-IDF),
   - fuse the two rankings (RRF), return top-k.

## Experiment

Pick a query with a specific term (e.g. "parking gratuit"). Compare pure-semantic vs hybrid top-5 — hybrid
should surface the listings that literally mention it.

## Safe checkpoint

- `get_comps(<id>)` returns only same-peer-group listings, never the listing itself.
- On a keyword-specific query, hybrid ranks the literal-match listing above pure semantic does.

## Commit

```
feat(host_copilot): comp retrieval + hybrid search (M6)
```

Next → [`08_analytics_tools.md`](08_analytics_tools.md).
