<!--
Source: https://docs.kapa.ai/api/reference
Kapa.ai deflection rates: https://docs.kapa.ai/integrations/support-form-deflector/deflection-rates
-->
# Kapa AI Doc Q&A — SKILL

Kapa.ai is the SOTA paid AI doc-Q&A service. Trained on a project's docs + ticket corpus, it answers technical questions, exposes deflection analytics, and surfaces content gaps (zero-result + low-confidence queries). Use this skill for doc-AI workflows, deflection metrics, and content-gap audits.

## When to use

- **Recipient deploys Kapa widget on docs / Help Center / Slack** and wants programmatic access to ask / log queries.
- **Generating an FAQ** from recurring unanswered questions (`get_zero_result_queries`).
- **Deflection metrics dashboard** — pull `deflected / answered / unanswered` rates for weekly review.
- **Content-gap audit** — cross-reference low-confidence answers with KB articles.
- **AI-first support cascade** — Kapa answer first, escalate to human if `confidence < threshold`.

Trigger phrases: "Kapa deflection rate", "what's our top unanswered question", "ask Kapa", "Kapa content gap", "Kapa analytics".

## Setup

```bash
# Kapa is API-first; no MCP server required. Direct curl works.
curl -sS https://api.kapa.ai/query/v1/projects \
  -H "X-API-Key: $KAPA_API_KEY" | jq '.[] | {id, name}'
```

Auth + env:
- `KAPA_API_KEY` — at `Project Settings > API Keys > Create`. Project-scoped. Separate keys for production and staging projects.
- `KAPA_PROJECT_ID` — UUID of the project you'll query.
- Pricing: paid (Pro ~$999/mo as of 2026); contact sales for enterprise. Free trial 14d.

Workspace prerequisites:
- Project trained on at least one knowledge source (docs site URL, Notion, Confluence, public GitHub). Training takes minutes-to-hours depending on corpus.
- Slack / Intercom / Zendesk integrations configured for full deflection tracking.

## Common recipes

### Recipe 1: Ask Kapa a question (the `query` endpoint)

```bash
curl -sS -X POST "https://api.kapa.ai/query/v1/projects/$KAPA_PROJECT_ID/chat" \
  -H "X-API-Key: $KAPA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query":"How do I configure SSO with Okta?",
    "user_session_id":"u_abc123",
    "include_sources":true
  }' | jq '.answer, .confidence, .sources[].url'
```

`confidence` returned 0-1. Gate human escalation on `confidence < 0.7` per `role.md` guidance.

### Recipe 2: Stream chat response (for in-product widget)

```bash
curl -sS -N -X POST "https://api.kapa.ai/query/v1/projects/$KAPA_PROJECT_ID/chat/stream" \
  -H "X-API-Key: $KAPA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"How do I rotate the API key?","stream":true}'
```

Returns Server-Sent Events. For terminal use, prefer Recipe 1.

### Recipe 3: Pull deflection metrics for last 30 days

```bash
curl -sS "https://api.kapa.ai/analytics/v1/projects/$KAPA_PROJECT_ID/deflection?period=30d" \
  -H "X-API-Key: $KAPA_API_KEY" | jq '{
    total_queries: .total_queries,
    deflected: .deflected_count,
    rate: .deflection_rate,
    escalated_to_human: .escalation_count
  }'
```

Deflection rate is `deflected / total_queries`. Industry benchmark: 30-50% on a mature docs corpus.

### Recipe 4: Top zero-result / unanswered queries

```bash
curl -sS "https://api.kapa.ai/analytics/v1/projects/$KAPA_PROJECT_ID/queries/unanswered?period=30d&limit=20" \
  -H "X-API-Key: $KAPA_API_KEY" | jq '.queries[] | {query, count, last_asked_at}'
```

Use as the seed list for new KB articles or FAQ entries. Filter for `count >= 5` as the cluster threshold.

### Recipe 5: Low-confidence answers (content needs improving)

```bash
curl -sS "https://api.kapa.ai/analytics/v1/projects/$KAPA_PROJECT_ID/queries/low-confidence?period=30d&threshold=0.6&limit=20" \
  -H "X-API-Key: $KAPA_API_KEY" | jq '.queries[] | {query, confidence, top_source}'
```

Queries where Kapa answered but the agent was unsure. These mean an existing doc is incomplete / outdated / poorly indexed.

### Recipe 6: Sync feedback (thumbs up / down)

```bash
curl -sS -X POST "https://api.kapa.ai/feedback/v1/projects/$KAPA_PROJECT_ID/feedback" \
  -H "X-API-Key: $KAPA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"thread_id":"th_abc","rating":"thumbs_up","comment":"Resolved my question."}'
```

Drives Kapa's model retraining loop. Pipe widget feedback through this for continuous improvement.

### Recipe 7: List configured knowledge sources

```bash
curl -sS "https://api.kapa.ai/management/v1/projects/$KAPA_PROJECT_ID/sources" \
  -H "X-API-Key: $KAPA_API_KEY" | jq '.[] | {id, type, url, last_indexed_at}'
```

Check `last_indexed_at` weekly — if a source hasn't re-indexed in >14d, Kapa is serving stale answers.

### Recipe 8: Trigger re-index of a source

```bash
curl -sS -X POST "https://api.kapa.ai/management/v1/projects/$KAPA_PROJECT_ID/sources/$SOURCE_ID/reindex" \
  -H "X-API-Key: $KAPA_API_KEY"
```

Required after major docs releases. Returns a job ID; poll `/jobs/$id` for completion.

### Recipe 9: Get usage by source (which docs Kapa cites most)

```bash
curl -sS "https://api.kapa.ai/analytics/v1/projects/$KAPA_PROJECT_ID/sources/usage?period=30d" \
  -H "X-API-Key: $KAPA_API_KEY" | jq '.[] | {url, citation_count, helpfulness_rate}'
```

High-citation + high-helpfulness = winning content. Low-helpfulness + high citation = doc is needed but unhelpful — rewrite candidate.

### Recipe 10: Webhook on new question (real-time analytics)

```bash
curl -sS -X POST "https://api.kapa.ai/management/v1/projects/$KAPA_PROJECT_ID/webhooks" \
  -H "X-API-Key: $KAPA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url":"https://your-agent.example.com/webhooks/kapa",
    "events":["query.answered","query.unanswered","feedback.submitted"]
  }'
```

Wire low-confidence answers to immediately log a Notion task for the technical-writer agent.

### Recipe 11: Search the knowledge base directly (semantic search, no LLM)

```bash
curl -sS -X POST "https://api.kapa.ai/search/v1/projects/$KAPA_PROJECT_ID/search" \
  -H "X-API-Key: $KAPA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"SSO Okta setup","limit":10}' | jq '.results[] | {title, url, score}'
```

Faster + cheaper than `/chat` if you only need top-K relevant docs (e.g., for ticket-deflection suggestion at compose-time).

### Recipe 12: Free fallback (Markprompt) when Kapa not available

```bash
# Markprompt OSS — drop-in alternative
curl -sS https://api.markprompt.com/v1/chat/completions \
  -H "X-API-Key: $MARKPROMPT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"How do I rotate the API key?"}],"projectKey":"$PROJECT_KEY","stream":false}'
```

Markprompt is OSS / freemium; covers the basic /chat + sources surface. Less polished analytics but usable when Kapa budget is unavailable.

## Examples

### Example 1: Weekly content-gap report → Notion drafts

**Goal:** Auto-draft KB articles for top 5 unanswered queries each week.

**Steps:**
1. `GET /analytics/v1/projects/$id/queries/unanswered?period=7d&limit=10`.
2. Filter for `count >= 5`.
3. For each query: Claude drafts a KB article using the article template from `role.md`.
4. `notion-mcp` `create_page` in the "KB drafts" DB with status="needs review".
5. Email technical-writer agent: "5 new drafts await review."

**Result:** KB drift detected and addressed weekly without manual triage.

### Example 2: Deflection-cascade — Kapa first, human second

**Goal:** Pre-screen Help Center submit-form questions; let Kapa answer; only escalate the ones Kapa is unsure on.

**Steps:**
1. Customer submits a question in the in-product help widget.
2. Agent calls Recipe 1; reads `answer` + `confidence`.
3. If `confidence >= 0.7`: surface the answer to the customer with a "Was this helpful?" follow-up.
4. If `confidence < 0.7` OR customer says "Talk to a human": create Zendesk / Intercom ticket with the original question + Kapa's draft as an internal note (so the agent doesn't start from scratch).

**Result:** 40%+ deflection; agents inherit context on the ones that escalate.

## Edge cases / gotchas

- **Kapa is paid** — Pro tier $999/mo (2026); without an API key the only fallback is Markprompt (OSS) or Inkeep (paid alt).
- **Pricing scales with queries** — bulk-loading 100k queries through `/chat` to backfill analytics will run a bill. Use `/search` (cheaper) or `/feedback` to ingest historical data.
- **Confidence threshold is opinion** — Kapa's default cutoff is 0.5 for "answered" vs "unanswered". The `role.md` guidance of 0.7 is *for human-handoff gating*. Don't confuse the two.
- **Indexing latency** — docs updates take 1-24h to propagate after re-index trigger. For critical updates, force re-index via Recipe 8 and verify by querying.
- **Project scoping** — `KAPA_PROJECT_ID` is a UUID. If the API key is workspace-scoped, you must pass project id in URL. If project-scoped, the key implies the project.
- **Rate limits** — `/chat`: 60 rpm per project; `/search`: 300 rpm. `/analytics`: 10 rpm. Cache analytics responses for weekly digests.
- **Source authentication** — Kapa needs read access to private knowledge sources (Notion, Confluence). Set up OAuth at Project Settings; rotating tokens breaks ingestion.
- **Multi-tenant data leakage risk** — if you have shared docs across projects, Kapa may surface them. Use source-level access controls or separate projects per audience.
- **Sentiment / multilingual** — Kapa's English-tuned model. For non-English support, route through `deepl-mcp` first, then query.
- **Webhook signatures** — Kapa uses HMAC-SHA256 in `X-Kapa-Signature`. Verify before trusting payloads.

## Sources

- [Kapa.ai API reference overview](https://docs.kapa.ai/api/reference)
- [Kapa Search endpoint](https://docs.kapa.ai/api/reference/search)
- [Deflection rates docs](https://docs.kapa.ai/integrations/support-form-deflector/deflection-rates)
- [Dashboard / analytics overview](https://docs.kapa.ai/analytics/dashboard)
- [Kapa.ai 2026 features + pricing review (AI Agents List)](https://aiagentslist.com/agents/kapaai)
- [Markprompt OSS alternative](https://markprompt.com/docs)
