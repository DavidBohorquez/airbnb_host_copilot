# App image. Built and wired up in M11 (docs/12_docker.md).
FROM python:3.13-slim

# uv for fast, reproducible installs
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Dependency layer (cached unless pyproject/lock change)
COPY pyproject.toml uv.lock ./
COPY src ./src
RUN uv sync --frozen --no-dev

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "host_copilot.api:app", "--host", "0.0.0.0", "--port", "8000"]