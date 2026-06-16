# Run from the repo root (the host_copilot/ folder once it's its own repo).
# Thin wrappers around uv so the same commands work locally and in CI/Docker.

.PHONY: setup test lint fmt ingest api eval docker clean

setup:          ## install all deps (incl. dev group) into the uv env
	uv sync --all-groups

test:           ## run the test suite
	uv run pytest -q

lint:           ## static checks
	uv run ruff check src tests

fmt:            ## auto-format
	uv run ruff format src tests

ingest:         ## build embeddings + populate the vector store (implemented in M5)
	uv run python -m host_copilot.ingest

api:            ## serve the FastAPI app (implemented in M10)
	uv run uvicorn host_copilot.api:app --reload --port 8000

eval:           ## retrieval relevance + price backtest (implemented in M12)
	uv run python -m host_copilot.eval

docker:         ## build + start the full stack (implemented in M11)
	docker compose up --build

clean:
	rm -rf artifacts **/__pycache__