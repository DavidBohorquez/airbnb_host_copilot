# M10 — FastAPI service

**Goal:** expose the pipeline over HTTP so it's a real service, not a notebook.

**Skills:** REST, pydantic request/response models, dependency injection, error handling.

## Steps (implement in `src/host_copilot/api.py`)

1. `/health` already returns `{"status": "ok"}` — keep it (used by Docker healthcheck + CI smoke test).
2. `POST /ask` → take `AskRequest{listing_id, question}`, call `pipeline.answer(...)`, return
   `AskResponse{advice, evidence}`.
3. Error handling: unknown `listing_id` → `404`; LLM/provider error → `503` with a clear message. Don't
   leak stack traces or API keys.
4. (Optional) load the embedder/Chroma client once at startup (FastAPI lifespan / a cached dependency) so
   each request doesn't reload the model.

## Run

```bash
make api      # uvicorn host_copilot.api:app --reload --port 8000
```

Then:
```bash
curl localhost:8000/health
curl -X POST localhost:8000/ask -H "content-type: application/json" \
     -d '{"listing_id": 12345, "question": "What price should I set?"}'
```

## Safe checkpoint

- `/health` → 200 `{"status":"ok"}`.
- `/ask` with a real id → JSON `{advice, evidence}`.
- `/ask` with a bogus id → 404, not a 500 stack trace.
- Add a test in `tests/` using FastAPI `TestClient` (httpx) hitting `/health`.

## Commit

```
feat(host_copilot): FastAPI /ask + /health (M10)
```

Next → [`12_docker.md`](12_docker.md).
