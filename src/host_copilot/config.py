"""Central settings. Reads .env at the repo root. Fully implemented — used by every module."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Repo root = two levels up from this file (src/host_copilot/config.py -> repo root).
REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=REPO_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LLM
    llm_provider: str = "ollama"  # ollama | anthropic | openai
    llm_model: str = "llama3.1"
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    ollama_host: str = "http://localhost:11434"

    # Embeddings
    embed_model: str = "intfloat/multilingual-e5-small"

    # Paths (stored relative; resolved against REPO_ROOT)
    data_dir: str = "data_airbnb_bordeaux"
    artifacts_dir: str = "artifacts"
    chroma_dir: str = "artifacts/chroma"

    # Retrieval
    top_k: int = 8

    @property
    def data_path(self) -> Path:
        return REPO_ROOT / self.data_dir

    @property
    def artifacts_path(self) -> Path:
        return REPO_ROOT / self.artifacts_dir

    @property
    def chroma_path(self) -> Path:
        return REPO_ROOT / self.chroma_dir


@lru_cache
def get_settings() -> Settings:
    return Settings()