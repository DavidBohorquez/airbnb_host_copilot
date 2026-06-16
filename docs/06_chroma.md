# M5 — Chroma (persistent store + metadata filtering)

**Goal:** move to a real vector database. Persist all listing vectors once, and query with a **metadata
filter** so you only ever compare within a peer group. Wire up `make ingest`.

**Skills:** production vector DB, collections, upsert, persistence, `where=` metadata filtering.

## Why a database, not just FAISS?

FAISS is an index in memory. A vector DB adds: persistence, metadata stored next to vectors, filtering,
upsert, and a query API. For Host Copilot, **metadata filtering is the whole point** — comps must share a
`peer_key`. Chroma does `vector search WHERE peer_key = ...` in one call.

## Steps (implement in `src/host_copilot/vectorstore/chroma_store.py` + `ingest.py`)

1. `__init__` → `chromadb.PersistentClient(path=get_settings().chroma_path)` and
   `get_or_create_collection("listings", metadata={"hnsw:space": "cosine"})`.
2. `upsert(ids, vectors, metadatas, documents)` → `collection.upsert(...)`. ids must be strings.
3. `query(query_vec, k, where)` → `collection.query(query_embeddings=[vec], n_results=k, where=where)`;
   return a list of dicts `{id, score, metadata, document}`.
4. `ingest.py::main()` → `load_listings()` → build documents + metadata → `Embedder.encode_passages` →
   `ChromaStore.upsert`. Run **once**.

## Steps

```bash
make ingest          # builds + persists the collection (slow first time)
```

## Safe checkpoint

- `make ingest` completes; `artifacts/chroma/` exists and survives a restart (re-opening the client finds
  the data — no re-ingest).
- A query with `where={"peer_key": "<some real key>"}` returns **only** listings from that peer group.
- Count in the collection ≈ number of listings ingested.

## Commit

```
feat(host_copilot): persistent chroma store + ingest pipeline (M5)
```

Next → [`07_retrieval.md`](07_retrieval.md).
