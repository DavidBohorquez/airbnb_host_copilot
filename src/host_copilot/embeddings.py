"""Multilingual encoder wrapper. Implement in M2 (docs/03_chunking_embeddings.md).

e5 models need prefixes: 'query: ...' for queries, 'passage: ...' for documents.
"""

from __future__ import annotations

import numpy as np


class Embedder:
    def __init__(self, model_name: str | None = None) -> None:
        # TODO M2: load SentenceTransformer(model_name or settings.embed_model)
        raise NotImplementedError

    def encode_passages(self, texts: list[str]) -> np.ndarray:
        """Batch-encode documents with the 'passage:' prefix; L2-normalized. TODO M2."""
        raise NotImplementedError

    def encode_query(self, text: str) -> np.ndarray:
        """Encode one query with the 'query:' prefix; L2-normalized. TODO M2."""
        raise NotImplementedError
