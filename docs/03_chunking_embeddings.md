# M2 — Embeddings & chunking

**Goal:** turn text into vectors with a multilingual model, and understand chunking.

**Skills:** what an embedding is, tokenization vs chunking, multilingual models, e5 prefixes, batching,
caching vectors to disk.

## Concepts

- **Embedding** = a fixed-length vector capturing meaning. Similar text → nearby vectors. Similarity is
  measured by cosine (M3).
- **Why multilingual?** Bordeaux reviews are French *and* English. `intfloat/multilingual-e5-small`
  handles both in one space, so an English query can match a French review.
- **e5 prefixes (important):** e5 models expect `"query: ..."` for search queries and `"passage: ..."`
  for stored documents. Forgetting the prefix quietly hurts quality.
- **Chunking:** listings are short → embed the whole document as one passage. **Reviews** can be long and
  many → chunk/aggregate (e.g. embed per review, or concatenate a sample). Don't stuff thousands of
  reviews into one vector; you lose signal.

## Steps (implement in `src/host_copilot/embeddings.py`)

1. In `__init__`, load `SentenceTransformer(model_name or get_settings().embed_model)`.
2. `encode_passages(texts)` → prepend `"passage: "`, encode in batches, return **L2-normalized**
   `np.ndarray` (normalize so dot product == cosine in M3).
3. `encode_query(text)` → prepend `"query: "`, return one normalized vector.
4. Add a small disk cache: save passage vectors to `artifacts/listings.npy` so you don't re-encode every
   run (encoding thousands of docs takes time on CPU).

## Safe checkpoint

- Encode 20 listing documents → shape `(20, 384)` for e5-small.
- `cosine(encode_query("appartement calme à Chartrons"), <a quiet-Chartrons passage>)` is clearly higher
  than against a random noisy-listing passage.
- Vectors are unit-norm: `np.linalg.norm(v) ≈ 1`.

## Commit

```
feat(host_copilot): multilingual embedder with passage/query prefixes + cache (M2)
```

Next → [`04_search_numpy.md`](04_search_numpy.md).
