<!--
Source: https://exa.ai/ · https://docs.exa.ai/
SDK: pip install exa-py
Free tier: 1k requests / month
-->

# Exa.ai — neural semantic web search

Exa is a neural-embedding-based web search engine. Queries by *semantic similarity* rather than keyword overlap — sub-200ms responses, 1k free requests/month. Use when you want results that are conceptually about your topic, not just lexically matching it.

## When to use this skill

- "Find me articles *similar to this one*" (link-based seed)
- Finding edge / niche sources keyword search misses (small blogs, obscure papers, podcast transcripts)
- Domain-whitelisted search for high-precision topics ("only nature.com / science.org / nejm.org")
- Domain-blacklisted search to exclude content farms ("not pinterest, not quora, not low-quality SEO mills")
- When `useAutoprompt: true` improves a naive query into a well-formed one
- Pairing with Perplexity: Exa finds the *right* URLs; Perplexity synthesizes the *answer*

## When NOT to use

- For exact-phrase / Boolean queries → use Brave or DDG
- For raw academic papers → use `paper-search-mcp` (Exa's academic coverage is partial)
- When you need to see the LLM's reasoning trace → use Perplexity Sonar Reasoning
- For multilingual news event detection → use `gdelt-news-monitoring`

## Setup

```bash
pip install exa-py
export EXA_API_KEY="..."
# Free tier: 1k requests/month at https://dashboard.exa.ai/
```

## Common recipes

### Recipe 1 — Basic neural search

```python
from exa_py import Exa
exa = Exa(api_key=os.environ["EXA_API_KEY"])

results = exa.search(
    query="practical advice on building product-market fit for B2B SaaS",
    type="neural",
    num_results=20,
    use_autoprompt=True,  # rewrites query for better neural retrieval
)
for r in results.results:
    print(r.url, r.title, r.score)
```

### Recipe 2 — Search + full content (single round-trip)

```python
results = exa.search_and_contents(
    query="latest research on GLP-1 drugs and cardiovascular outcomes",
    type="neural",
    num_results=10,
    text={"max_characters": 4000, "include_html_tags": False},
    highlights={"num_sentences": 3, "highlights_per_url": 3},
)
for r in results.results:
    print(r.url)
    print("HIGHLIGHTS:", r.highlights)
    print("TEXT:", r.text[:500])
```

The `text` + `highlights` combo replaces the typical "search → scrape each URL" two-step.

### Recipe 3 — Domain whitelisting (high precision)

```python
# Only authoritative biomed venues
results = exa.search_and_contents(
    query="ozempic semaglutide cardiovascular trial results",
    type="neural",
    num_results=15,
    include_domains=[
        "nejm.org", "thelancet.com", "nature.com", "science.org",
        "jamanetwork.com", "bmj.com", "fda.gov", "nih.gov",
    ],
    start_published_date="2024-01-01",
)
```

### Recipe 4 — Domain blacklisting (cleanup low-quality results)

```python
results = exa.search(
    query="climate policy 2024 carbon tax",
    type="neural",
    exclude_domains=[
        "pinterest.com", "quora.com", "reddit.com",
        "facebook.com", "medium.com",  # exclude if low quality is suspected
    ],
)
```

### Recipe 5 — "Find similar" (URL-seeded)

```python
# User has one great article; find 20 more like it
similar = exa.find_similar(
    url="https://www.nature.com/articles/s41586-024-08145-x",
    num_results=20,
    exclude_source_domain=False,  # set True to find sources OUTSIDE nature.com
)
for r in similar.results:
    print(r.url, r.title)
```

### Recipe 6 — Combining with Perplexity

Two-step pattern for high-precision, high-quality research:

```python
# Step 1: Exa finds the right URLs with domain whitelist
candidate_urls = exa.search(
    query="my research question",
    include_domains=["..."],
    num_results=30,
).results
# Step 2: Send URLs to Perplexity for synthesis
# (use Perplexity's search_domain_filter or paste URL list in the prompt)
```

### Recipe 7 — Recent-only filter for trend work

```python
from datetime import date, timedelta
six_months_ago = (date.today() - timedelta(days=180)).isoformat()

results = exa.search(
    query="emerging LLM evaluation benchmarks",
    type="neural",
    start_published_date=six_months_ago,
    num_results=30,
    use_autoprompt=True,
)
```

## Edge cases

- **Neural ≠ semantic perfect:** "What's the best CRM?" returns articles *about* "best CRMs" (often listicles). For *answer*, use Perplexity. Exa returns *sources*, not answers.
- **Date-filter accuracy:** Exa's `start_published_date` relies on each page's published-date metadata, which is often missing or wrong. Cross-check the actual content date for time-critical work.
- **Free-tier exhaustion:** 1k req/mo. Cache results, batch by topic; route low-priority queries to `brave-search` first.
- **`use_autoprompt=False`** when the user's query is already well-formed (technical jargon, exact phrase). Autoprompt may dilute precision.
- **`type='keyword'`** mode is also available for traditional keyword search via Exa — use when the user requests exact-phrase matching.
- **Highlights vs text:** highlights return ~3 sentences each; text returns the full extracted body. Use highlights when speed matters, text when you need to quote.

## Sources

- Exa docs: https://docs.exa.ai/
- Pricing / dashboard: https://dashboard.exa.ai/
- Python SDK: https://github.com/exa-labs/exa-py

## Related skills

- `perplexity-deep-research` — Exa finds URLs; Perplexity synthesizes answers
- `paper-search-mcp` — academic-paper-specific retrieval
