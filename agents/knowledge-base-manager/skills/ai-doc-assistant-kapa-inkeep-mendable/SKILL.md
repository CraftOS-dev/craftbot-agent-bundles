---
name: ai-doc-assistant-kapa-inkeep-mendable
description: AI doc Q&A integration — Kapa.ai (verified citations, used by OpenAI/Reddit), Inkeep (search-first + chat fallback), Mendable (SDK for product), Markprompt (FOSS self-host). Ground-truth eval before launch (accuracy ≥90% / hallucination <5%). Use when adding AI assistant on top of KB.
---

# AI doc assistant — Kapa, Inkeep, Mendable, Markprompt

## When to use

User says "AI assistant for docs", "Kapa.ai", "Inkeep", "Mendable", "AI Q&A on KB", "self-hosted AI docs". Reach AFTER KB taxonomy + search + analytics are stable. NEVER launch without ground-truth eval — hallucination destroys trust.

## Setup

```bash
# Kapa.ai (paid; sign up: https://www.kapa.ai/)
# REST API key from dashboard
export KAPA_TOKEN=...
export KAPA_PROJECT_ID=...

# Inkeep (paid; https://inkeep.com/)
export INKEEP_API_KEY=...
export INKEEP_INTEGRATION_ID=...

# Mendable (paid; https://mendable.ai/)
npm i @mendable/sdk
export MENDABLE_ANON_KEY=...

# Markprompt (FOSS + cloud; https://markprompt.com/)
pip install markprompt   # client
# Self-host: clone https://github.com/motifland/markprompt
docker compose up -d
export MARKPROMPT_KEY=...

# Eval tooling
pip install anthropic langfuse
```

Auth / API key requirements:
- `KAPA_TOKEN` — Kapa dashboard → API access
- `INKEEP_API_KEY` — Inkeep dashboard
- `MENDABLE_ANON_KEY` + private key for ingestion
- `MARKPROMPT_KEY` — public + private (ingestion) keys

## Common recipes

### Recipe 1: Kapa — sync source

```bash
# Trigger reindex
curl -X POST "https://api.kapa.ai/query/v1/projects/${KAPA_PROJECT_ID}/sources/sync" \
  -H "Authorization: Bearer $KAPA_TOKEN"

# Add a sitemap source
curl -X POST "https://api.kapa.ai/query/v1/projects/${KAPA_PROJECT_ID}/sources" \
  -H "Authorization: Bearer $KAPA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"sitemap","url":"https://docs.acme.com/sitemap.xml"}'
```

### Recipe 2: Kapa — query the API

```bash
curl -X POST "https://api.kapa.ai/query/v1/projects/${KAPA_PROJECT_ID}/chat" \
  -H "Authorization: Bearer $KAPA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"How do I configure SSO with Okta?","stream":false}'
```

Returns JSON with `answer`, `relevant_sources[]`, `confidence`.

### Recipe 3: Kapa — embed widget

```html
<script src="https://widget.kapa.ai/kapa-widget.bundle.js"
  data-website-id="YOUR_WEBSITE_ID"
  data-project-name="Acme docs"
  data-project-color="#0078ff"
  data-project-logo="https://acme.com/logo.png"
  data-search-mode-enabled="true"
  async></script>
```

### Recipe 4: Inkeep — query

```bash
curl -X POST "https://api.inkeep.com/v0/chat_sessions/chat_results" \
  -H "Authorization: Bearer $INKEEP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "integration_id":"'$INKEEP_INTEGRATION_ID'",
    "chat_session":{"messages":[{"role":"user","content":"How do I retry webhooks?"}]}
  }'
```

### Recipe 5: Inkeep — search-first widget

```html
<script src="https://unpkg.com/@inkeep/cxkit-js/dist/embed.js"></script>
<script>
  Inkeep.SearchBar('#search', {
    baseSettings:{apiKey:'public-key', integrationId:'$INKEEP_INTEGRATION_ID'},
    aiChatSettings:{aiAssistantName:'Acme'}
  });
</script>
```

### Recipe 6: Mendable SDK — ingest + query

```javascript
import Mendable from '@mendable/sdk';
const m = new Mendable({ anonKey: process.env.MENDABLE_ANON_KEY });

// Query
const resp = await m.chat({ question: 'How do I configure SSO?' });
console.log(resp.answer, resp.sources);

// Ingest (server-side, with private key)
await m.ingest({
  sources: [{ type: 'sitemap', url: 'https://docs.acme.com/sitemap.xml' }],
});
```

### Recipe 7: Markprompt — self-host

```bash
# Self-hosted
git clone https://github.com/motifland/markprompt
cd markprompt
cp .env.example .env  # set OPENAI_API_KEY, SUPABASE_*, etc.
docker compose up -d

# Add source via API
curl -X POST "http://localhost:3000/api/sources" \
  -H "Authorization: Bearer $MARKPROMPT_KEY" \
  -d '{"type":"github","data":{"url":"github.com/acme/docs"}}'

# Query
curl -X POST "http://localhost:3000/api/v1/chat" \
  -H "Authorization: Bearer $MARKPROMPT_KEY" \
  -d '{"messages":[{"role":"user","content":"How do I configure SSO?"}]}'
```

### Recipe 8: Build ground-truth eval set

```python
# eval/ground-truth.jsonl  — 50-100 Q&A pairs
{"q":"How do I configure SSO with Okta?","expected_keywords":["SAML","metadata","app"],"expected_source":"/how-to/authentication/sso-okta"}
{"q":"Why are my webhooks not received?","expected_keywords":["retry","logs","signature"],"expected_source":"/troubleshooting/webhooks-not-received"}
```

### Recipe 9: Run eval via Claude judge

```python
# scripts/eval-ai-docs.py
import json, requests, anthropic
client = anthropic.Anthropic()
RUBRIC = """You are evaluating a docs AI assistant.
Score 0-1 on each axis:
- Accuracy: does the answer match the source article?
- Citation: does it cite the source URL?
- Hallucination: any invented facts? (1=none, 0=many)
- Completeness: does it cover the full answer?
Return JSON: {accuracy, citation, hallucination, completeness, notes}"""

results = []
for case in open('eval/ground-truth.jsonl'):
    case = json.loads(case)
    # Call your AI assistant
    ans = requests.post('https://api.kapa.ai/query/v1/projects/x/chat',
        headers={"Authorization":f"Bearer {os.environ['KAPA_TOKEN']}"},
        json={"query":case['q']}).json()
    # Judge with Claude
    judge = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        messages=[{"role":"user","content":
            f"{RUBRIC}\n\nQuestion: {case['q']}\nAnswer: {ans['answer']}\nExpected source: {case['expected_source']}\nReturned sources: {ans['relevant_sources']}"
        }])
    results.append(json.loads(judge.content[0].text))

avg = lambda k: sum(r[k] for r in results)/len(results)
print(f"Accuracy: {avg('accuracy'):.0%}  Citation: {avg('citation'):.0%}  Hallucination: {avg('hallucination'):.0%}")
```

### Recipe 10: CI eval gate

```yaml
# .github/workflows/ai-eval.yml
on:
  schedule: [{cron: '0 6 * * *'}]
  workflow_dispatch:
jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install anthropic
      - run: python scripts/eval-ai-docs.py | tee result.txt
      - run: |
          ACC=$(grep -oP 'Accuracy: \K[0-9]+' result.txt)
          [ "$ACC" -lt 90 ] && exit 1
```

### Recipe 11: Add feedback collector to AI answers

```javascript
// On thumbs-down, send to PostHog + open Linear ticket
function onFeedback(answer, query, feedback) {
  posthog.capture('ai_docs_feedback', {query, answer_id:answer.id, feedback});
  if (feedback === 'down') {
    fetch('/api/linear', {method:'POST', body: JSON.stringify({
      title: `AI docs: bad answer for "${query}"`,
      description: answer.text,
      teamId: 'docs',
    })});
  }
}
```

### Recipe 12: Restrict ingestion (exclusion list)

```bash
# Kapa: exclude archived
curl -X PATCH "https://api.kapa.ai/query/v1/projects/${KAPA_PROJECT_ID}/sources/${SOURCE_ID}" \
  -H "Authorization: Bearer $KAPA_TOKEN" \
  -d '{"exclude_patterns":["/_archived/*","/internal/*"]}'
```

## Examples

### Example 1: Add Kapa to public docs

**Goal:** Cut "where do I find" support tickets by 30%.

**Steps:**
1. Sign up Kapa; index docs.acme.com via sitemap (Recipe 1).
2. Exclude archived (Recipe 12).
3. Build 75-Q ground truth (Recipe 8) covering top-search + edge cases.
4. Eval baseline (Recipe 9) — measure accuracy + citation + hallucination.
5. Tune system prompt + retraining loop until accuracy ≥90%, hallucination <5%.
6. Embed widget (Recipe 3) — beta to 10% first.
7. CI eval gate per release (Recipe 10).

**Result:** Ticket deflection +30%; AI answers cited in SCRM.

### Example 2: Markprompt self-host for FOSS-friendly org

**Goal:** AI docs without SaaS lock-in.

**Steps:**
1. `docker compose up` self-host (Recipe 7).
2. Ingest GitHub repo source.
3. Embed widget snippet in MkDocs.
4. Eval per release.

**Result:** $0/mo; full data ownership.

## Edge cases / gotchas

- **Launch without eval = trust killer** — one wrong billing answer = "AI is broken". Always eval first.
- **Citation requirement** — answers without source links erode trust. All 4 platforms support this; verify.
- **Stale ingestion** — Kapa/Inkeep sync schedule defaults to hourly/daily; force resync after content changes.
- **Markprompt requires OpenAI / Claude key** — paid LLM calls underneath; budget.
- **Mendable embedding rate-limited** on free; bulk ingestion needs paid.
- **PII in source docs** — internal docs shouldn't power public AI. Restrict ingestion via patterns.
- **Hallucination at edges** — questions outside the KB scope hallucinate. System prompt: "If not in the KB, say 'I'm not certain — could you...'"
- **Pricing scales with queries** — Kapa $200+/mo; budget vs deflection $ saved.
- **Inkeep search-first mode** is the right default — chat fallback for ambiguous Q.
- **A/B test old search vs AI** for 2-4 weeks before sunset.

## Sources

- Kapa.ai docs: https://docs.kapa.ai/
- Kapa REST API: https://docs.kapa.ai/integrations/api
- Inkeep docs: https://docs.inkeep.com/
- Mendable docs: https://docs.mendable.ai/
- Markprompt (FOSS): https://github.com/motifland/markprompt
- Markprompt docs: https://markprompt.com/docs
- Anthropic Claude API: https://docs.anthropic.com/en/api/getting-started
- Langfuse (eval observability): https://langfuse.com/docs
- RAG eval rubric (RAGAS): https://docs.ragas.io/
