# M11 — Containerize

**Goal:** run the whole stack with `docker compose up` — the app, the Chroma DB, and an Ollama server —
with persistent volumes.

**Skills:** Dockerfile (uv-based), multi-service docker-compose, volumes, service networking, healthchecks.

## Concepts

- **Dockerfile** packages the app into a reproducible image. We use the `uv` base for fast installs and a
  cached dependency layer (copy `pyproject.toml` + `uv.lock` first, then source).
- **docker-compose** runs multiple services on one network. Services reach each other by name:
  the app talks to `http://ollama:11434` and to the `chroma` service — not `localhost`.
- **Volumes** persist data across restarts (the Chroma collection, Ollama models, artifacts).

## Steps

1. Review `host_copilot/Dockerfile` (already scaffolded) — confirm `PYTHONPATH` and the uvicorn CMD.
2. Review `host_copilot/docker-compose.yml` — three services (`app`, `chroma`, `ollama`) + named volumes.
3. Add a **healthcheck** to the `app` service hitting `/health`.
4. Decide ingest strategy: run `make ingest` against the mounted volume once (e.g. a one-shot compose run
   or an entrypoint check that ingests if the collection is empty).
5. If using local LLM: `docker compose exec ollama ollama pull llama3.1`.

## Run

```bash
docker compose -f host_copilot/docker-compose.yml up --build
curl localhost:8000/health
```

## Safe checkpoint

- `docker compose up` brings all services healthy; `/health` returns 200 from the container.
- `/ask` works end-to-end inside Docker.
- `docker compose down && up` again → vector store **persists** (no re-ingest), proving volumes work.

## Commit

```
feat(host_copilot): dockerfile + compose stack with volumes (M11)
```

Next → [`13_eval_monitoring.md`](13_eval_monitoring.md).
