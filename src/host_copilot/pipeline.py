"""Agentic RAG orchestration. Implement in M9 (docs/10_agentic_rag.md).

Flow: question + listing_id -> retrieve comps -> call analytics tools -> LLM composes grounded advice.
"""

from __future__ import annotations


def answer(listing_id: int, question: str) -> dict:
    """Return {'advice': str, 'evidence': {...}}. Grounded in comps + tool outputs. TODO M9."""
    raise NotImplementedError
