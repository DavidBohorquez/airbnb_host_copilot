"""Multilingual encoder wrapper. M2 (docs/03_chunking_embeddings.md).

e5 models need prefixes: 'query: ...' for queries, 'passage: ...' for documents.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

from host_copilot.config import get_settings


class Embedder:
    def __init__(self, model_name: str | None = None) -> None:
        self.model = SentenceTransformer(model_name or get_settings().embed_model)

    def encode_passages(self, texts: list[str], cache_path: str | Path | None = None) -> np.ndarray:
        """Batch-encode documents with the 'passage:' prefix; L2-normalized.

        If cache_path exists, load it; otherwise encode and save (skips re-encoding on CPU).
        """
        if cache_path is not None and Path(cache_path).exists():
            return np.load(cache_path)
        vectors = self.model.encode(
            [f"passage: {t}" for t in texts],
            batch_size=32,
            normalize_embeddings=True,
            show_progress_bar=True,
            convert_to_numpy=True,
        )
        if cache_path is not None:
            Path(cache_path).parent.mkdir(parents=True, exist_ok=True)
            np.save(cache_path, vectors)
        return vectors

    def encode_query(self, text: str) -> np.ndarray:
        """Encode one query with the 'query:' prefix; L2-normalized (1-D vector)."""
        return self.model.encode(
            f"query: {text}",
            normalize_embeddings=True,
            convert_to_numpy=True,
        )