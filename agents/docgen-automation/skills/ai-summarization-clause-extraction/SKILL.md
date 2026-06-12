---
name: ai-summarization-clause-extraction
description: Summarize long contracts (MSA, customer T&C, 100+ page agreements) and extract named clauses (parties, term, fees, indemnity, IP, LoL, governing law, termination) using long-context LLMs (Claude Sonnet 4.5+, Gemini 2.0 Pro), CLM AI (Evisort, LinkSquares, Ironclad AI, Lexion AI), or local NER + few-shot prompting. Use when the user says "summarize this contract", "extract indemnity clause", "find LoL caps", "Evisort search", "LinkSquares clause", "AI contract review".
---

# AI summarization + clause extraction — Claude / Gemini long-context + CLM AI

This skill ships the "what's in this contract" pipeline. For 1-100 docs: long-context LLM via filesystem. For 1K+ docs: CLM-native AI (Evisort, LinkSquares).

## When to use

User says:

- "Summarize this MSA / SaaS T&C / 80-page agreement"
- "Extract indemnity / LoL / governing law / term / IP clauses"
- "What are the auto-renewal terms across our top 50 customers?"
- "Find every contract with weak indemnity caps"
- "Evisort semantic search"
- "LinkSquares clause library"

Companion skills:
- `clm-ironclad-contractworks-integration` — for >1K-doc corpora.
- `contract-redlining-automation` — apply extracted findings as redlines.
- `audit-trail-e-sign-versioning` — link extracted clauses back to executed env.
- `ocr-paper-doc-extraction` — pre-process scans.

## Setup

```bash
# Claude API (long-context summarization)
pip install anthropic
# Required env: ANTHROPIC_API_KEY

# Gemini (alt long-context)
pip install google-generativeai
# Required env: GOOGLE_API_KEY

# Local NER + classification (for SLA + private deploys)
pip install spacy transformers
python -m spacy download en_core_web_lg

# CLM AI (Evisort / LinkSquares / Ironclad AI)
# Use clm-ironclad-contractworks-integration skill

# Helpers
pip install python-docx pypdf PyPDF2 tiktoken
```

## Common recipes

### Recipe 1: Pick the engine

| Engine | Best for | Cost | Notes |
|---|---|---|---|
| Claude Sonnet 4.5+ | Single-doc deep summary | API ($/M tokens) | 1M-token context |
| Claude Opus | Very high accuracy on complex contracts | Higher API | Slowest, most expensive |
| Gemini 2.0 Pro | Free-tier alt | Free / API | 1M-token context |
| GPT-4 / 5 | OpenAI-resident | API | 128K-200K context |
| Evisort AI | Bulk semantic search across repo | Per-seat license | Best-in-class clause AI |
| LinkSquares AI | Post-exec analytics + extraction | License | Clause library + dashboards |
| Ironclad AI Assist | Pre-exec workflow | License | Negotiation assistance |
| Local NER (spaCy + few-shot LLM) | Private / air-gapped | Compute | Latency low; accuracy medium |

Default for single contracts: Claude long-context. For 1K+ docs: pair with CLM AI. For air-gapped: local NER + small LLM.

### Recipe 2: Standard clause taxonomy

```python
STANDARD_CLAUSES = [
    "parties",                # who is contracting
    "effective_date",
    "term_length",
    "auto_renewal",
    "termination_for_cause",
    "termination_for_convenience",
    "payment_terms",
    "fees_structure",          # flat / per-unit / hybrid
    "late_payment",
    "limitation_of_liability",
    "indemnity",
    "warranties",
    "ip_assignment",
    "ip_license_grant",
    "confidentiality",
    "data_processing",
    "data_security",
    "governing_law",
    "venue_forum",
    "dispute_resolution",      # arbitration / litigation
    "force_majeure",
    "assignment",
    "amendment",
    "notices",
    "severability",
    "entire_agreement",
    "counterparts",
    "service_levels",
    "non_compete",
    "non_solicit"
]
```

### Recipe 3: Claude — summarize a contract

```python
import anthropic
from pypdf import PdfReader

def read_pdf(path):
    return "\n".join(p.extract_text() for p in PdfReader(path).pages)

text = read_pdf("acme-msa.pdf")
client = anthropic.Anthropic()
resp = client.messages.create(
    model="claude-sonnet-4-7",
    max_tokens=4000,
    system="You are a senior commercial contracts lawyer. Output factual, citation-anchored summaries; refuse to draft legal advice; flag ambiguity.",
    messages=[{"role":"user","content": f"""Summarize this MSA. For each section below, give 1-3 bullet findings + the section number cited from the doc:

Parties, Effective date, Term + renewal, Fees, Payment terms,
Limitation of Liability, Indemnity, IP assignment, Warranties,
Confidentiality, Data processing, Governing law, Venue, Termination, SLA.

Then list 5 unusual or risky terms with a one-line risk rating (low/medium/high).

Contract:
{text}"""}]
)
print(resp.content[0].text)
```

Hand off binding interpretation to `legal-counsel`.

### Recipe 4: Claude — structured JSON extraction

```python
resp = client.messages.create(
    model="claude-sonnet-4-7",
    max_tokens=4000,
    system="Extract contract clauses. Return strict JSON only.",
    messages=[{"role":"user","content": f"""Extract the following clauses from the contract below. Return JSON:
{{
  "parties": [{{"name":"","role":""}}],
  "effective_date": "ISO",
  "term_months": 0,
  "auto_renewal": {{"present": false, "notice_days":0}},
  "limitation_of_liability": {{"cap_type":"","cap_value":"","exclusions":[]}},
  "indemnity": {{"customer_indemnifies": false, "vendor_indemnifies": false, "covered_claims":[]}},
  "governing_law": {{"state":"","country":""}},
  "venue": "",
  "termination_for_convenience": {{"present": false, "notice_days":0}},
  "raw_text_refs": {{ "section_name":"section_n.n" }}
}}

Use null where uncertain; do not invent.

Contract:
{text}"""}]
)
import json
clauses = json.loads(resp.content[0].text)
```

### Recipe 5: Compare two contracts (rev vs prior)

```python
prior_text = read_pdf("acme-msa-v1.pdf")
new_text = read_pdf("acme-msa-v2.pdf")
resp = client.messages.create(
    model="claude-sonnet-4-7",
    max_tokens=4000,
    system="You are reviewing contract changes between versions. Be precise about what changed.",
    messages=[{"role":"user","content": f"""Compare versions of this MSA. For each of the standard clauses (parties, term, LoL, indemnity, ...), state whether it changed and quote the before/after key lines.

V1:
{prior_text}

V2:
{new_text}"""}]
)
```

### Recipe 6: Bulk summarize 100+ contracts (corpus)

```python
import pathlib, json
from concurrent.futures import ThreadPoolExecutor

results = []
def process_one(path):
    text = read_pdf(path)
    # Recipe 4 for structured JSON
    return {"path": str(path), "clauses": extract_clauses(text)}

with ThreadPoolExecutor(max_workers=4) as ex:
    for r in ex.map(process_one, pathlib.Path("contracts/").glob("*.pdf")):
        results.append(r)

# Persist
with open("clauses.jsonl","w") as f:
    for r in results:
        f.write(json.dumps(r) + "\n")
```

Pricing/rate-limit aware: parallelism 4-8 for Claude API.

### Recipe 7: Evisort — semantic clause search

```bash
curl -X POST https://api.evisort.com/v1/search \
  -H "Authorization: Bearer $EVISORT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "limitation of liability cap less than 12 months fees",
    "agreement_types": ["MSA","SaaS"]
  }'
```

Returns ranked list of contracts + clause snippets matching natural query.

### Recipe 8: LinkSquares — pull all clauses for a contract

```bash
curl https://api.linksquares.com/v1/contracts/$ID/clauses \
  -H "Authorization: Bearer $LINKSQUARES_API_KEY"
```

Returns extracted clauses + confidence scores for ~30 standard categories.

### Recipe 9: Hybrid — local NER pre-pass + LLM verification

```python
import spacy
nlp = spacy.load("en_core_web_lg")
doc_text = read_pdf("acme-msa.pdf")
doc = nlp(doc_text)
# Pull obvious entities (parties, dates, money)
candidates = {
    "parties":   [e.text for e in doc.ents if e.label_ == "ORG"],
    "dates":     [e.text for e in doc.ents if e.label_ == "DATE"],
    "money":     [e.text for e in doc.ents if e.label_ == "MONEY"]
}
# Then LLM verifies + categorizes
verified = llm_verify(candidates, doc_text)
```

Cheaper at scale because the LLM only sees flagged spans.

### Recipe 10: Chunking for >1M-token contracts (rare)

```python
# Most contracts fit; treaties/master agreements might not
import tiktoken
enc = tiktoken.encoding_for_model("gpt-4o")
tokens = enc.encode(text)
CHUNK = 200_000
chunks = [enc.decode(tokens[i:i+CHUNK]) for i in range(0, len(tokens), CHUNK)]
# Summarize each chunk, then meta-summarize
chunk_summaries = [summarize(c) for c in chunks]
final = summarize("\n".join(chunk_summaries))
```

### Recipe 11: Citation-anchored output (page + section)

```python
# Provide page+section context in prompt
resp = client.messages.create(
    model="claude-sonnet-4-7",
    max_tokens=4000,
    messages=[{"role":"user","content": f"""For each finding, cite the section number (e.g., "§4.2") and page (if visible).

{text_with_page_markers}"""}]
)
```

Pre-process the PDF to inject `[Page 12]` markers between page contents.

### Recipe 12: Risk-tier grading

```python
RISK_TIERS = {
    "low": "Standard market terms",
    "medium": "Acceptable with negotiation",
    "high": "Material business risk; require legal review"
}
resp = client.messages.create(
    model="claude-sonnet-4-7",
    max_tokens=2000,
    system="Rate each clause: low / medium / high risk relative to typical SaaS T&C 2026 market. Cite reasoning.",
    messages=[{"role":"user","content": f"...{text}"}]
)
```

Always hand off high-risk findings to `legal-counsel`.

### Recipe 13: Term-sheet style summary output

```markdown
# Contract Summary — Acme MSA

**Parties:** Widget Co (Vendor) ↔ Acme Corp (Customer)
**Effective:** 2026-07-01    **Term:** 36 months    **Auto-renew:** Yes, 60-day notice
**Fees:** $240K/yr fixed; annual escalator 3%
**LoL Cap:** 12 months fees paid    **Mutual cap:** No (vendor only)
**Indemnity:** Vendor IP infringement; Customer breach of confidentiality
**Governing law:** Delaware    **Venue:** Delaware Court of Chancery
**SLA:** 99.9% uptime    **Service credits:** Cap 10% monthly fees
**Notable / risk:**
- §8.3 — uncapped liability for breach of confidentiality (HIGH)
- §11 — exclusive forum (MEDIUM — usability)
- §12 — IP indemnity excludes open-source claims (LOW)
```

## Examples

### Example 1: One-contract due-diligence summary

**Goal:** Acquirer needs MSA summary for diligence.
**Steps:**
1. Recipe 3 — Claude summary.
2. Recipe 4 — structured JSON for cap-table-style row.
3. Recipe 12 — risk tier.
4. Recipe 13 — term-sheet style markdown for partners.

**Result:** Standard-format diligence row per contract.

### Example 2: Quarterly clause audit across 200 contracts

**Goal:** Find weak indemnity caps; renegotiate top 10.
**Steps:**
1. Recipe 6 — bulk extract via Claude.
2. Filter rows where `limitation_of_liability.cap_value < 6 months fees`.
3. Rank by deal value.
4. Hand off top 10 to `legal-counsel` for redline strategy.

**Result:** Risk-prioritized renegotiation list.

### Example 3: Enterprise — Evisort + LinkSquares hybrid

**Goal:** 5K-contract repo; need natural-language search.
**Steps:**
1. Recipe 7 — Evisort for "find all contracts with weak indemnity."
2. Recipe 8 — pull clauses for the top 50 results.
3. Recipe 5 — diff vs the org's template to spot deviations.

**Result:** AI-assisted contract intelligence with auditable extraction.

## Edge cases / gotchas

- **Hallucinated clauses.** Always require the LLM to quote the source section; null if uncertain.
- **Image-heavy PDFs.** Run `ocr-paper-doc-extraction` first; LLM can't read pixels via API.
- **Token budget.** 1M-context Claude / Gemini handle ~700 pages; longer use chunking (Recipe 10).
- **Privacy.** Cloud LLM sees contract; if confidential, use local LLM (Llama 3.1+ 70B, Qwen 2.5) on-prem.
- **JSON parse failures.** LLMs sometimes wrap JSON in markdown fence; strip ```` ```json ```` blocks.
- **Numeric extraction precision.** "twelve months" vs "12 months" vs "annual" — LLM may confuse units. Re-validate.
- **Pages with two-column layout.** Text extraction order can scramble; use layout-aware OCR or PDF text extractors.
- **Defined terms.** Contracts use capitalized Defined Terms — LLM may miss them; provide glossary in prompt.
- **Multi-document agreements.** MSA + SOWs + Order Forms — analyze together; clauses may cross-reference.
- **Side letters.** Override main agreement; ask LLM explicitly to flag them.
- **Encoded PDFs.** Some PDFs have characters in wrong order or with custom encodings; OCR the PDF as image.
- **Conflicts of law / multi-jurisdiction.** Risk grading depends on jurisdiction; surface it always.
- **CLM AI vs LLM.** CLM AI trained on millions of contracts → calibrated risk tiers; LLM more verbose but less calibrated.
- **Confidence calibration.** Always present LLM output with hedged language; final calls = `legal-counsel`.
- **Boilerplate skew.** Bonterms / Common Paper / NVCA templates are common; flag deviations.
- **Token cost at scale.** 200 contracts × 80 pages × 500 tokens/page ≈ 8M input tokens / call set; plan budget.
- **Refusal on adversarial prompts.** If asked "draft binding legal opinion", LLM refuses; reinforce in system prompt.

## Sources

- [Anthropic Claude docs](https://docs.anthropic.com/) — long-context API.
- [Anthropic prompt-engineering for legal](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — best practices.
- [Google Gemini docs](https://ai.google.dev/docs) — long-context alt.
- [OpenAI structured outputs](https://platform.openai.com/docs/guides/structured-outputs) — JSON-schema-enforced extraction.
- [Evisort Contract Intelligence](https://www.evisort.com/contract-intelligence) — semantic search + extraction.
- [LinkSquares API](https://help.linksquares.com/) — clause library + dashboards.
- [Ironclad AI Assist](https://ironcladapp.com/products/ai/) — pre-exec workflow.
- [spaCy NER](https://spacy.io/usage/linguistic-features) — local NER fallback.
- [tiktoken](https://github.com/openai/tiktoken) — token counting / chunking.
- Sister skills: `clm-ironclad-contractworks-integration`, `contract-redlining-automation`, `audit-trail-e-sign-versioning`, `ocr-paper-doc-extraction`.
