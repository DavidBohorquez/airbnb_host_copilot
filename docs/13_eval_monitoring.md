# M12 — CI/CD + Evaluation + Monitoring

**Goal:** prove it works automatically (CI), prove it works *well* (eval), and see what it does in
production (logging/metrics).

**Skills:** GitHub Actions, retrieval evaluation, price backtest, structured logging, basic metrics.

## CI/CD

`.github/workflows/ci.yml` (scaffolded) runs on push/PR: install via uv → `ruff check` → `pytest`.

- Confirm it's green on a PR. Add a smoke test that imports the app and hits `/health` with `TestClient`.
- (Stretch) add a build job that `docker build`s the image so a broken Dockerfile fails CI.

## Evaluation (`src/host_copilot/eval.py`)

You cannot improve what you don't measure. Two metrics:

1. **Retrieval relevance.** Build a small labeled set: queries → which listings *should* match. Report
   `recall@k` / `MRR`. Use it to compare semantic vs hybrid (M6) objectively.
2. **Price-advice backtest.** For listings with a known `price`, have the pipeline recommend a price using
   only the *peer comps* and compare to actual → report **MAE / median abs error**. This is the
   business-facing number from the spec's ROI section.

`make eval` prints both.

## Monitoring

- **Structured logging:** log per request `{listing_id, latency_ms, provider, n_comps, tool_errors}`. Use
  the stdlib `logging` with a JSON formatter.
- **Basic metrics:** count requests, average latency, error rate. Expose a `/metrics` endpoint or just log
  a rolling summary. Enough to answer "is it slow? is it erroring?".

## Safe checkpoint

- CI green on a PR (lint + tests).
- `make eval` prints retrieval recall@k **and** price-backtest MAE.
- Hitting `/ask` produces a structured log line with latency and comp count.

## Commit

```
feat(host_copilot): CI, eval (retrieval + price backtest), logging (M12)
```

## Done

You now have an end-to-end, tested, containerized RAG + analytics assistant — and the RAG + DevOps skills
that built it. Revisit `00_overview.md` to see how far the architecture came.
