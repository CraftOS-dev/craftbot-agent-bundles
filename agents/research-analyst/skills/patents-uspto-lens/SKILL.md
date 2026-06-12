<!--
Source: https://data.uspto.gov/apis/getting-started (USPTO PatentsView)
        https://docs.api.lens.org/ (Lens.org Patent API)
MCP: uspto-mcp (already enabled)
-->

# Patents — USPTO PatentsView + Lens.org

Patent landscapes are a leading indicator of corporate R&D priorities (2-5 year lead time on shipped products) and a key competitive-intelligence signal. Two SOTA sources:

- **USPTO PatentsView** — free, US-only, JSON REST API. Strong for citation graphs and detailed claim-level metadata.
- **Lens.org Patent API** — free *non-commercial*, global coverage (USPTO + EPO + WIPO + others), more permissive query DSL. Requires bearer token.

## When to use this skill

- Trend analysis (patent filings as a leading indicator of corporate R&D direction)
- Competitive intelligence (what is competitor X investing in?)
- IP positioning (whose patents block our path? whose can we license?)
- Citation networks (which patents are foundational to a tech area?)
- Inventor / assignee tracking (where is the talent? what are they working on?)
- Family expansion (one PCT filed in N countries = serious commercial intent)

## When NOT to use

- For trade-secret-protected innovation (not in any patent DB by definition)
- For very-recent filings (USPTO publishes 18 months after filing date)
- For software / SaaS where patents are rare — supplement with `competitive-intelligence-tech-stack` (Wappalyzer, GitHub)

## Setup

```bash
# USPTO PatentsView — no key, just descriptive User-Agent
export USPTO_USER_AGENT="Research Analyst name@example.com"

# Lens.org — free non-commercial token
# Sign up at https://www.lens.org/lens/user/subscriptions then request API access
export LENS_API_TOKEN="..."
```

`uspto-mcp` is already enabled in `agent.yaml`.

## Common recipes — USPTO PatentsView

### Recipe 1 — Search by assignee (competitor)

```bash
curl -G "https://api.patentsview.org/patents/query" \
  -A "$USPTO_USER_AGENT" \
  --data-urlencode 'q={"assignee_organization":"Anthropic"}' \
  --data-urlencode 'f=["patent_number","patent_title","patent_date","cpc_section_id"]' \
  --data-urlencode 'o={"per_page":50}'
```

### Recipe 2 — Search by CPC classification (tech area)

```bash
# CPC G06N — AI/ML; G06N3 — neural networks; G06N20 — machine learning
curl -G "https://api.patentsview.org/patents/query" \
  -A "$USPTO_USER_AGENT" \
  --data-urlencode 'q={"_and":[{"cpc_subgroup_id":"G06N20/00"},{"_gte":{"patent_date":"2024-01-01"}}]}' \
  --data-urlencode 'f=["patent_number","patent_title","assignee_organization","patent_date"]' \
  --data-urlencode 'o={"per_page":100,"sort":[{"patent_date":"desc"}]}'
```

### Recipe 3 — Citation graph (forward + backward)

```bash
# Patents that cite a foundational patent (forward citations = downstream usage)
curl -G "https://api.patentsview.org/patents/query" \
  -A "$USPTO_USER_AGENT" \
  --data-urlencode 'q={"cited_patent_number":"8762892"}' \
  --data-urlencode 'f=["patent_number","patent_title","assignee_organization"]'

# Patents that THIS patent cites (backward = prior art)
# Use the patent detail endpoint, then the "cited_patents" field
```

### Recipe 4 — Inventor tracking

```bash
curl -G "https://api.patentsview.org/inventors/query" \
  -A "$USPTO_USER_AGENT" \
  --data-urlencode 'q={"inventor_first_name":"Jane","inventor_last_name":"Doe"}' \
  --data-urlencode 'f=["inventor_id","patent_number","patent_title","assignee_organization"]'
```

## Common recipes — Lens.org (global coverage)

### Recipe 5 — Lens.org search (cross-jurisdiction)

```bash
curl -X POST "https://api.lens.org/patent/search" \
  -H "Authorization: Bearer $LENS_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "bool": {
        "must": [
          {"match": {"abstract": "transformer language model"}},
          {"range": {"date_published": {"gte": "2024-01-01"}}}
        ]
      }
    },
    "size": 50,
    "include": ["lens_id","biblio.publication_reference","biblio.application_reference","biblio.invention_title","biblio.parties.applicants","biblio.classifications_cpc"]
  }'
```

### Recipe 6 — Patent family expansion (commercial-intent signal)

```bash
# Same invention filed in multiple jurisdictions = serious commercial intent
curl -G "https://api.lens.org/patent/families" \
  -H "Authorization: Bearer $LENS_API_TOKEN" \
  --data-urlencode 'lens_id=XXX-XXX-XXX'
# Returns all family members across USPTO, EPO, WIPO, JPO, KIPO, CNIPA
```

### Recipe 7 — Scholarly–patent linkage (academic-to-IP pipeline)

Lens.org uniquely links scholarly papers ↔ patents that cite them:

```bash
curl -G "https://api.lens.org/patent/search" \
  -H "Authorization: Bearer $LENS_API_TOKEN" \
  --data-urlencode 'query={"match":{"references_cited.npl_count":{"gte":5}}}'
```

Useful for "which academic papers spawned the most patents?" trend signal.

## Common recipes — analysis pipelines

### Recipe 8 — Competitor R&D heatmap

```python
import pandas as pd, requests

competitors = ["OpenAI", "Anthropic", "Google LLC", "Microsoft", "Meta"]
rows = []
for c in competitors:
    r = requests.get("https://api.patentsview.org/patents/query",
                     params={"q": f'{{"assignee_organization":"{c}"}}',
                             "f": '["patent_number","cpc_subgroup_id","patent_date"]',
                             "o": '{"per_page":1000}'},
                     headers={"User-Agent": os.environ["USPTO_USER_AGENT"]})
    for p in r.json()["patents"]:
        rows.append({"company": c,
                     "cpc": (p["cpcs"][0]["cpc_subgroup_id"] if p["cpcs"] else None),
                     "year": p["patent_date"][:4]})

df = pd.DataFrame(rows)
heatmap = pd.crosstab(df.cpc, [df.company, df.year])
# → heatmap shows which competitor is investing where, by year
```

### Recipe 9 — Filing-velocity trend (weak signal)

```python
# Filings per quarter in a tech area — a sharp uptick = emerging trend
df["q"] = pd.PeriodIndex(df["patent_date"], freq="Q")
velocity = df.groupby("q").size()
# If velocity has doubled in last 4 quarters → strong trend signal
```

## Edge cases

- **18-month publication delay:** USPTO publishes filings ~18 months after filing date. To catch the leading edge, use the *application* number search (pre-publication) which has limited coverage. Lens.org sometimes has earlier WIPO PCT publications.
- **Assignee name variants:** "Apple Inc.", "Apple Computer Inc.", "Apple Inc". Always grep across variants with `_or` query operator.
- **Pending vs granted:** PatentsView's `/patents/` endpoint returns granted patents; for pending applications use the SEPARATE `/patent_applications/` endpoint or Lens.org with `document_type:patent_application`.
- **CPC vs IPC vs USPC:** USPTO supports CPC (current) and USPC (legacy). EPO uses IPC + CPC. Lens.org accepts all three. Default to CPC for modern filings.
- **NPL (non-patent literature) citations:** Patents cite academic papers too. Lens.org's `npl_count` is the best signal of "this patent is grounded in academic research."
- **Lens.org commercial use:** the free tier is **non-commercial**. For a commercial deliverable, the user must obtain a commercial license — flag this in limitations.
- **Rate limits:** PatentsView ~45 req/min; Lens.org tier-dependent (free typically 100/day).
- **Continuation chains:** Apple files many continuations of the same base patent. Use family search (`document_kind` filtering) to deduplicate.

## Sources

- USPTO PatentsView: https://data.uspto.gov/apis/getting-started · https://patentsview.org/apis/api-endpoints
- Lens.org Patent API: https://docs.api.lens.org/
- CPC classification scheme: https://www.cooperativepatentclassification.org/
- IPC classification: https://www.wipo.int/classifications/ipc/en/

## Related skills

- `competitive-intelligence-tech-stack` — patents + financials + tech stack composite
- `trend-fan-out-multi-source` — patents as one of 8 trend source types
- `semantic-scholar-openalex` — academic-to-patent linkage
