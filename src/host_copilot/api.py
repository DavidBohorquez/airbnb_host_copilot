"""FastAPI service. Implement in M10 (docs/11_api.md)."""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Host Copilot")


class AskRequest(BaseModel):
    listing_id: int
    question: str


class AskResponse(BaseModel):
    advice: str
    evidence: dict


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest) -> AskResponse:
    # TODO M10: call pipeline.answer(req.listing_id, req.question) and map to AskResponse
    raise NotImplementedError
