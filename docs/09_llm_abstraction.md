# M8 — LLM abstraction

**Goal:** one interface, three interchangeable backends (Ollama / Anthropic / OpenAI), chosen by
`LLM_PROVIDER` in `.env`. Swap models without touching the pipeline.

**Skills:** the provider/adapter pattern, prompt templates, structured output, secrets handling.

## Concepts

- **Why abstract?** You want to prototype locally (Ollama, free, offline) and ship with a strong API model
  (Claude/OpenAI) without rewriting the pipeline. Code against an interface, not a vendor.
- **Tool-calling:** all three support function/tool calling, but with different schemas. The adapter hides
  that difference behind one `complete(system, user, tools)`.

## Steps (implement in `src/host_copilot/llm.py`)

1. Define the `LLM` Protocol: `complete(system, user, tools=None) -> dict` returning at least
   `{text, tool_calls}`.
2. Implement three adapters:
   - **Ollama** → `ollama.Client(host=settings.ollama_host).chat(model=settings.llm_model, ...)`.
   - **Anthropic** → `anthropic.Anthropic(api_key=settings.anthropic_api_key).messages.create(...)`.
   - **OpenAI** → `openai.OpenAI(api_key=settings.openai_api_key).chat.completions.create(...)`.
3. `get_llm()` reads `settings.llm_provider` and returns the matching adapter. Raise a clear error if the
   required key is missing.

## Secrets

Keys come only from `.env` via `config.py`. Never hardcode. `.env` is gitignored. If a key is blank for
the selected provider, fail fast with a readable message.

## Safe checkpoint

- With `LLM_PROVIDER=ollama` (and a model pulled, e.g. `ollama pull llama3.1`), `get_llm().complete("You
  are terse.", "Say hi in French.")` returns text.
- Switching `LLM_PROVIDER=anthropic` (key set) returns text from the same call — **no other code changes**.

## Commit

```
feat(host_copilot): pluggable LLM backends via env (M8)
```

Next → [`10_agentic_rag.md`](10_agentic_rag.md).
