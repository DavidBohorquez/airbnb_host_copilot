# M0 — Setup & DevOps base

**Goal:** a working, tested skeleton. `make setup` installs everything, settings load from `.env`,
`make test` is green.

**Skills:** uv environment management, src layout, secrets via `.env`, Makefile, git hygiene.

## Steps

1. **Install deps.** From the repo root:
   ```bash
   uv sync --all-groups
   ```
   This installs the RAG/LLM/service deps (added to root `pyproject.toml`) plus the dev group
   (pytest, ruff, httpx).

2. **Create your env file.**
   ```bash
   cp host_copilot/.env.example host_copilot/.env
   ```
   Leave keys blank for now (M0 uses none). `.env` is gitignored — never commit it.

3. **Understand `config.py`.** It is the one module written for you. `get_settings()` returns a cached
   `Settings` object; `settings.data_path` / `chroma_path` resolve paths against the repo root. Every
   later module imports from here — no hardcoded paths anywhere else.

4. **Run the suite.**
   ```bash
   uv run pytest -q
   ```
   `test_config.py` must pass. `test_loaders.py` is all `@pytest.mark.skip` until M1 — that's expected.

5. **Lint.**
   ```bash
   uv run ruff check host_copilot/src host_copilot/tests
   ```

## Safe checkpoint

- `uv run pytest -q` → `test_config.py` passes, loaders tests skipped, **0 failures**.
- `python -c "from host_copilot.config import get_settings; print(get_settings().embed_model)"` prints the
  model name.

## Commit

```
feat(host_copilot): scaffold + config + DevOps base (M0)
```

Next → [`02_data_prep.md`](02_data_prep.md).
