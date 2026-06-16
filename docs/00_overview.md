# 00 — Overview

## What you are building

**Host Copilot**: a chatbot that advises Airbnb *hosts* about their listing, grounded in real Bordeaux
data. It answers questions like *"what price should I set?"* by retrieving comparable listings (**RAG**)
and computing analytics (price percentiles, occupancy, review sentiment), then letting an LLM turn that
evidence into advice.

This is the harder of two assistant designs (the other is a guest-facing search bot) because it combines
retrieval **and** analytics **and** tool-calling — which is exactly why it teaches more.

## What you will learn

- **RAG**: documents & chunking, multilingual embeddings, vector similarity (cosine/dot/L2), exact vs
  approximate search, vector databases (FAISS, Chroma), metadata filtering, hybrid search.
- **AI engineering**: LLM provider abstraction, prompt design, agentic tool-calling, grounding & citation.
- **DevOps**: uv envs, testing, FastAPI, Docker + docker-compose, GitHub Actions CI, evaluation & logging.

## How the tutorial works

13 milestones (M0–M12), one doc each (`00`–`13`). Every milestone has the same shape:

- **Goal** — what works at the end.
- **Skills** — what you learn.
- **Steps** — what to implement (in the matching stub file under `src/host_copilot/`).
- **Safe checkpoint** — a concrete test/command that must pass *before you move on*. Never advance on a
  broken base.
- **Commit** — what to commit.

You write the logic; the stubs give you the signatures and a `TODO Mx` marker. I assist at each checkpoint.

## The big picture (architecture)

```
listings.csv ─┐
reviews.csv ──┼─► clean (M1) ─► documents (M1) ─► embeddings (M2)
calendar.csv ─┘                                        │
                                                       ▼
              NumPy search (M3) ─► FAISS (M4) ─► Chroma persistent (M5)
                                                       │
                                          retrieval: comps + hybrid (M6)
                                                       │
                analytics tools (M7): pricing · occupancy · sentiment
                                                       │
                            LLM abstraction (M8) ─► agentic pipeline (M9)
                                                       │
                          FastAPI (M10) ─► Docker (M11) ─► CI + eval (M12)
```

## Order of attack

Do them in order. M3→M5 deliberately builds the *same* search three ways (from scratch → FAISS → Chroma)
so you understand what the database does for you before you depend on it.

Next → [`01_setup.md`](01_setup.md).
