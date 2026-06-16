# M3 — Vector search from scratch (NumPy)

**Goal:** implement exact top-k similarity search yourself, before any library. This is the single most
important conceptual milestone.

**Skills:** cosine vs dot vs Euclidean (L2), exact/brute-force search, why it doesn't scale.

## Concepts

- **Cosine similarity** = angle between vectors, range [-1, 1]. For **L2-normalized** vectors,
  `cosine(a,b) == dot(a,b)` — so search becomes one matrix multiply.
- **L2 distance** = straight-line distance. For unit vectors it is monotonic with cosine, so ranking is
  equivalent — but the scores differ. Knowing this prevents confusion later (FAISS `IndexFlatIP` uses
  inner product; `IndexFlatL2` uses distance).
- **Brute force** = compare the query to *every* vector. Exact, simple, O(n·d) per query. Fine for a few
  thousand listings; hopeless for millions → motivates ANN in M4.

## Steps (implement in `src/host_copilot/vectorstore/numpy_store.py`)

1. Store the `(n, d)` normalized matrix and the parallel `ids` list.
2. `search(query_vec, k)`:
   - scores = `vectors @ query_vec` (since both normalized → cosine).
   - take top-k indices (`np.argpartition` then sort), return `[(id, score)]` descending.

## Experiment (do this, it builds intuition)

- Run the same query with cosine (dot of normalized) and with raw L2 distance. Confirm the **ranking** is
  the same but scores differ.
- Time a search over all listings. Note it in your notebook — you'll compare against FAISS in M4.

## Safe checkpoint

- Query "appartement lumineux proche tramway" returns plausibly matching listings in the top 5.
- Self-query (a document's own vector) returns that document as rank 1 with score ≈ 1.0.

## Commit

```
feat(host_copilot): brute-force cosine search in numpy (M3)
```

Next → [`05_faiss.md`](05_faiss.md).
