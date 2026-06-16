"""LLM provider abstraction. Implement in M8 (docs/09_llm_abstraction.md).

One interface, three backends selected by settings.llm_provider: ollama | anthropic | openai.
"""

from __future__ import annotations

from typing import Protocol


class LLM(Protocol):
    def complete(self, system: str, user: str, tools: list | None = None) -> dict: ...


def get_llm() -> LLM:
    """Factory: read settings.llm_provider, return the matching client. TODO M8."""
    raise NotImplementedError
