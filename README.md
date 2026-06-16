# Host Copilot — Bordeaux Airbnb

Conversational **decision-support assistant for Airbnb hosts**, built on the Bordeaux dataset.
A host asks a question about their listing; the assistant answers using **RAG** (retrieval of
comparable listings + reviews) combined with **analytics tools** (price percentiles, occupancy,
sentiment), then a configurable LLM turns the evidence into advice.

Example questions:
- *"What price should I set for my 2-bedroom in Chartrons?"*
- *"Why do similar places book more than mine?"*
- *"What do guests complain about in my area?"*

## This repo is a guided tutorial

The code is delivered as **stubs + a milestone-by-milestone tutorial** in [`docs/`](docs/). You
implement the RAG/AI logic yourself, learning as you go. Each milestone ends in a runnable, tested
state so you never build on a broken base.

Start here → [`docs/00_overview.md`](docs/00_overview.md).

## Quickstart

```bash
uv sync --all-groups          # install deps into the uv env
cp .env.example .env          # then fill in keys
uv run pytest -q              # run the test suite
# data: see docs/DATA.md to fetch the CSVs (not committed)
make ingest                   # build embeddings + vector store (after M5)
make api                      # serve the FastAPI app (after M10)
docker compose up             # full stack: app + chroma + ollama (after M11)
```

## Layout

```
src/host_copilot/   the package (config is written; the rest are stubs you implement)
docs/               the tutorial, one file per milestone (00 → 13) + DATA.md
tests/              pytest suite, grows with each milestone
notebooks/          scratch exploration
data_airbnb_bordeaux/   the CSVs you download (gitignored)
```

## Stack

sentence-transformers (multilingual e5) · NumPy → FAISS → Chroma · DuckDB · LangChain ·
Ollama / Anthropic / OpenAI (configurable) · FastAPI · Docker · GitHub Actions.

## Data

Not committed (the calendar file alone exceeds GitHub's limits). See
[`docs/DATA.md`](docs/DATA.md) to download `listings.csv`, `reviews.csv`, `calendar.csv`,
`neighbourhoods.csv` into `data_airbnb_bordeaux/`.
