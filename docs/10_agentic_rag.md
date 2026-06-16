# M9 — Agentic RAG pipeline

**Goal:** the brain. Given `(listing_id, question)`, retrieve comps, call the analytics tools, and let the
LLM compose grounded advice that cites the evidence.

**Skills:** tool-calling loop, grounding, evidence citation, prompt design for advisory output.

## Flow (implement in `src/host_copilot/pipeline.py::answer`)

```
question + listing_id
   │
   ├─ retrieval.get_comps(listing_id)        # comparable listings
   ├─ tools.pricing.price_position(...)      # where price sits
   ├─ tools.occupancy.occupancy_stats(...)   # demand vs peers
   └─ tools.sentiment.area_sentiment(...)    # area complaints
        │
        ▼
   build a context block from comps + tool dicts
        │
        ▼
   LLM.complete(system="You are a host advisor. Use ONLY the evidence.
                        Cite numbers.", user=question + context)
        │
        ▼
   {"advice": <text>, "evidence": {comps, pricing, occupancy, sentiment}}
```

## Two ways to wire tools

1. **Orchestrated (recommended first):** *you* call the tools, stuff results into the prompt, ask the LLM
   to summarize. Deterministic, easy to debug.
2. **Agentic tool-calling (stretch):** expose the tools to the LLM (M8 `tools=`) and let it decide which to
   call. More flexible, harder to control. Build #1 first; upgrade to #2.

## Grounding rules (put in the system prompt)

- Use only the provided evidence; if data is missing, say so — never invent a price.
- Always cite the numbers (e.g. "comparable 3-4 person flats in Chartrons sit at 95–130€, median 110€").

## Safe checkpoint

- `answer(<id>, "What price should I set?")` returns advice referencing the real `price_position`
  percentiles and at least one comp, plus an `evidence` dict.
- Asking about a listing with sparse data yields an honest "not enough data" rather than a fabricated
  number.

## Commit

```
feat(host_copilot): agentic RAG pipeline (retrieve + tools + LLM) (M9)
```

Next → [`11_api.md`](11_api.md).
