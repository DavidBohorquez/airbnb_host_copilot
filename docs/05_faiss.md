# M4 — FAISS (approximate nearest neighbour)

**Goal:** index the same vectors in FAISS, verify it matches your NumPy result on a flat index, then try
an approximate index and measure the speed/recall tradeoff.

**Skills:** ANN, `IndexFlatIP` vs `IndexIVFFlat`/`IndexHNSWFlat`, recall vs speed, index persistence.

## Concepts

- **Why ANN?** Brute force is O(n) per query. ANN structures (IVF, HNSW) prune the search space to get
  ~100× speedups at the cost of *occasionally* missing the true nearest neighbour (**recall < 100%**).
- **IndexFlatIP** = exact inner-product search (same as your M3, but optimized C++). Use it as ground
  truth.
- **IndexIVFFlat** = clusters vectors into `nlist` cells, searches only the nearest `nprobe` cells.
  Higher `nprobe` → higher recall, slower. **HNSW** = graph-based, great recall/speed, more memory.

## Steps (implement in `src/host_copilot/vectorstore/faiss_store.py`)

1. `__init__(dim)` → start with `faiss.IndexFlatIP(dim)`.
2. `add(vectors, ids)` → FAISS uses integer positions; keep an `ids` list to map positions back. (Or use
   `IndexIDMap`.)
3. `search(query_vec, k)` → return `[(id, score)]`.
4. `save(path)` / `load(path)` → `faiss.write_index` / `read_index`.
5. Then swap in an `IndexIVFFlat` (needs `.train()` first) and expose `nprobe`.

## Experiment

- Compare FlatIP top-k vs your NumPy top-k → should be **identical**.
- Compare IVF (low `nprobe`) vs FlatIP → measure recall@10 (overlap of result sets) and the speed gain.
- Time queries vs M3. Record the numbers.

## Safe checkpoint

- FlatIP results == NumPy results on the same query.
- You can state your IVF recall@10 and speedup vs flat.
- Index round-trips through `save`/`load` and still returns the same results.

## Commit

```
feat(host_copilot): faiss index (flat + IVF) with persistence (M4)
```

Next → [`06_chroma.md`](06_chroma.md).
