<!--
Source: https://docs.perplexity.ai/docs/sonar/models/sonar-deep-research
Endpoint: https://api.perplexity.ai/chat/completions
Models: sonar, sonar-pro, sonar-reasoning, sonar-deep-research
Factuality benchmark: F=0.858 SimpleQA (Sonar Deep Research)
-->

# Perplexity Sonar — synthesized web research

Perplexity's Sonar API exposes web-grounded LLM search with multi-step retrieval + synthesis. Sonar Deep Research achieves **F=0.858 on SimpleQA** — state-of-the-art factuality among synthesized-answer systems. Use when the deliverable needs an *answer* (with citations), not raw search results.

## When to use this skill

- **Sonar Pro** — fast (~3s), one-shot synthesized answer with 5-10 citations. Use for the standard "what's the current state of X" question. $3/M-input, $15/M-output tokens.
- **Sonar Deep Research** — multi-step (~30-90s), agentic retrieval across 50+ sources with reasoning trace + bibliography. Use for full-fledged research reports the user would otherwise read 20 tabs to write. $5/M-input, $25/M-output + reasoning tokens.
- **Sonar Reasoning** — Sonar Pro with explicit chain-of-thought. Use when the user wants to see the reasoning steps, not just the answer.
- **Plain Sonar** — cheapest ($1/M-in, $1/M-out); use for high-volume routine queries.

## When NOT to use

- For raw academic papers → `paper-search-mcp` (Perplexity synthesizes; doesn't return paper objects)
- For neural / semantic search by topic similarity → `exa-neural-search`
- For Boolean / site-restricted precision queries → `brave-search` + Exa
- For pure news monitoring → `gdelt-news-monitoring` (Perplexity won't expose 65-language event detection)
- When deterministic / reproducible search results matter → Perplexity's multi-step retrieval is non-deterministic; prefer Brave/Exa

## Setup

```bash
export PERPLEXITY_API_KEY="pplx-..."
# Free tier: limited monthly credits; paid usage-based after
# See: https://docs.perplexity.ai/docs/pricing
```

## Common recipes

### Recipe 1 — Sonar Pro: fast triangulated answer

```bash
curl https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sonar-pro",
    "messages": [
      {"role": "system", "content": "Be precise and cite sources."},
      {"role": "user", "content": "What is the SOTA accuracy on the MMLU benchmark as of June 2026, and which models hold the top 3 positions?"}
    ],
    "search_recency_filter": "month",
    "return_citations": true
  }'
```

Response includes `citations: [...]` array. Re-validate each citation by spot-checking URL accessibility before quoting.

### Recipe 2 — Sonar Deep Research: full investigative report

```bash
curl https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sonar-deep-research",
    "messages": [
      {"role": "user", "content": "Produce a research brief on the lithium iron phosphate (LFP) battery market for stationary storage 2025-2030: top 5 producers by capacity, capex trends, cost-per-kWh trajectory, regulatory drivers in US/EU/China, and three credible bear-case risks. Cite all numerical claims."}
    ],
    "search_recency_filter": "month",
    "return_citations": true,
    "return_related_questions": false
  }'
```

Expect a 30-90s round trip. The response includes a citation bibliography (typically 30-80 sources) and reasoning trace. **Always** spot-check at least 3 numerical claims against the cited primary source before quoting in a deliverable — Perplexity can hallucinate numbers even with grounded search.

### Recipe 3 — Domain-restricted search

```bash
# Restrict to authoritative domains only (best for medical, legal, regulatory)
curl https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -d '{
    "model": "sonar-pro",
    "messages": [{"role":"user","content":"Latest FDA guidance on AI/ML medical devices"}],
    "search_domain_filter": ["fda.gov", "nih.gov", "nejm.org", "thelancet.com"],
    "search_recency_filter": "month"
  }'
```

### Recipe 4 — Multi-step retrieval flow (manual, for full control)

When you need cheaper-than-Deep-Research multi-step retrieval:

1. **Decompose** the question into 3-5 sub-questions (use Claude / `concise-planning`).
2. **Fan out** Sonar Pro calls in parallel — one per sub-question.
3. **Synthesize** the responses into a single brief using Claude. Track citations.
4. **Validate** numerical / load-bearing claims by spot-checking primary sources.

Cost: ~3-5× Sonar Pro = still cheaper than Sonar Deep Research at scale, and you control the decomposition.

### Recipe 5 — Cost management

| Workload | Recommended model | Why |
|---|---|---|
| High-volume routine lookups | `sonar` | $1/M tokens; good enough for "what's X" |
| Standard research question | `sonar-pro` | Best quality/price for one-shot answers |
| Full research brief (5+ sub-questions) | `sonar-deep-research` | Pays for itself vs manual fan-out |
| Reasoning-trace-required | `sonar-reasoning` | When the user wants to see the steps |

Track monthly spend; route the next-tier-up only when the cheaper tier returned low confidence or single-source citations.

## When to use vs Exa vs Brave

| Need | Use |
|---|---|
| "Give me an answer with citations" | **Perplexity Sonar Pro / Deep Research** |
| "Find me papers about X" | **Exa neural** (semantic similarity) + `paper-search-mcp` |
| "Find pages matching exact Boolean query" | **Brave / DuckDuckGo** (keyword) |
| "Domain whitelist with semantic relevance" | **Exa** (`includeDomains`) |
| "65-language global news event monitoring" | **GDELT** |
| "Reproducible / deterministic retrieval" | **Brave / DuckDuckGo** (Perplexity is non-deterministic) |

## Edge cases

- **Citation hallucination on numbers:** Sonar will occasionally cite a real source for a fabricated number. Always re-verify load-bearing numerical claims against the cited URL.
- **Recency filter precision:** `search_recency_filter` of `month` includes anything within 30 days but doesn't guarantee Sonar uses *only* recent sources. To force, add "as of <date>, ignore pre-<date> sources" in the prompt.
- **Reasoning tokens billed separately:** Sonar Deep Research bills reasoning tokens at the output rate. A 90s deep research call can be 50k+ tokens of internal reasoning.
- **`search_domain_filter` cap:** max ~10 domains. For wider whitelists, use Exa.
- **Streaming:** Sonar supports SSE streaming for long Deep Research calls — use to surface partial progress.
- **Non-English queries:** Sonar handles non-English well but tends to translate sources to English; use `deepl-mcp` if you need the original-language quote preserved.

## Sources

- Sonar Deep Research overview: https://docs.perplexity.ai/docs/sonar/models/sonar-deep-research
- Pricing: https://docs.perplexity.ai/docs/pricing
- API reference: https://docs.perplexity.ai/api-reference/chat-completions
- SimpleQA benchmark methodology: https://openai.com/index/introducing-simpleqa/

## Related skills

- `exa-neural-search` — semantic search by topic similarity (complement)
- `paper-search-mcp` — when you need papers, not synthesized answers
- `gdelt-news-monitoring` — multilingual news event monitoring
