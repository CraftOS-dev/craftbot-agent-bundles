<!--
Sources: Crunchbase API https://data.crunchbase.com/docs/using-the-api
         Similarweb-free-API https://github.com/DaWe35/Similarweb-free-API
-->

# Crunchbase + Similarweb — private-company market research

For private-company data (funding, exec teams, employee count, traffic), Crunchbase and Similarweb are the SOTA. Both have paid + free tiers; the agent uses what the user provides.

- **Crunchbase API** — Basic $49/mo, Pro $99/mo; primary source for company / funding / exec data on private companies
- **Similarweb-free-API** — community-maintained free wrapper around Similarweb; limited but useful traffic-share signal

## When to use this skill

- Sizing private-company complement to SEC EDGAR (TAM bottom-up)
- Funding rounds + valuation tracking (signal of investor confidence)
- Founding-team / exec background (signal of execution capability)
- Acquisition history (M&A landscape)
- Traffic-share comparison (Similarweb for market-share-by-eyeballs)
- Detecting stealth / under-the-radar competitors

## When NOT to use

- For public companies → use `sec-edgar-market-sizing` (better data, free)
- Without a Crunchbase API key → fall back to scraping the public Crunchbase pages via `firecrawl-mcp` (limited fields)
- For deep traffic analytics → free Similarweb is shallow; paid Similarweb Pro starts $14k+/yr

## Setup

```bash
export CB_API_KEY="..."         # https://data.crunchbase.com/docs/getting-started
# No setup for Similarweb-free-API; install on demand:
pip install requests beautifulsoup4
```

## Crunchbase recipes

### Recipe 1 — Organization search

```bash
curl -X POST "https://api.crunchbase.com/api/v4/searches/organizations" \
  -H "X-cb-user-key: $CB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "field_ids": ["identifier","name","short_description","categories","founded_on","operating_status","funding_total","employee_count"],
    "query": [
      {"type":"predicate","field_id":"categories","operator_id":"includes","values":["c4d8caf3-5fe7-359b-f9f2-2d708378e4ee"]},
      {"type":"predicate","field_id":"founded_on","operator_id":"between","values":["2020-01-01","2026-01-01"]}
    ],
    "limit": 50,
    "order": [{"field_id":"funding_total","sort":"desc"}]
  }'
```

### Recipe 2 — Organization detail (single company)

```bash
curl "https://api.crunchbase.com/api/v4/entities/organizations/anthropic?field_ids=name,founded_on,location_identifiers,description,operating_status,categories,funding_total,num_employees_enum,website,linkedin,twitter,facebook,permalink&card_ids=founders,headquarters_address,investors,parent_organization,founders,acquirees,acquirers" \
  -H "X-cb-user-key: $CB_API_KEY"
```

### Recipe 3 — Funding round tracking

```bash
curl -X POST "https://api.crunchbase.com/api/v4/searches/funding_rounds" \
  -H "X-cb-user-key: $CB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "field_ids": ["identifier","funded_organization_identifier","announced_on","money_raised","investment_type","lead_investor_identifiers"],
    "query": [
      {"type":"predicate","field_id":"announced_on","operator_id":"gte","values":["2026-01-01"]},
      {"type":"predicate","field_id":"investment_type","operator_id":"includes","values":["series_a","series_b","series_c"]}
    ],
    "limit": 100
  }'
```

### Recipe 4 — Investor / fund tracking

```bash
curl "https://api.crunchbase.com/api/v4/entities/principals/sequoia-capital?card_ids=investments,founded_organization,partners" \
  -H "X-cb-user-key: $CB_API_KEY"
```

### Recipe 5 — Acquisition signal

```bash
curl -X POST "https://api.crunchbase.com/api/v4/searches/acquisitions" \
  -H "X-cb-user-key: $CB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "field_ids": ["acquirer_identifier","acquiree_identifier","announced_on","price","categories"],
    "query": [
      {"type":"predicate","field_id":"announced_on","operator_id":"gte","values":["2026-01-01"]}
    ],
    "order": [{"field_id":"price","sort":"desc"}],
    "limit": 50
  }'
```

Useful for "what categories are buyers consolidating into?"

### Recipe 6 — Geographic / category market scan

```bash
# All AI startups in San Francisco founded 2023+
curl -X POST "https://api.crunchbase.com/api/v4/searches/organizations" \
  -H "X-cb-user-key: $CB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "field_ids": ["name","founded_on","funding_total","num_employees_enum"],
    "query": [
      {"type":"predicate","field_id":"location_identifiers","operator_id":"includes","values":["san-francisco-california-united-states"]},
      {"type":"predicate","field_id":"categories","operator_id":"includes","values":["artificial-intelligence"]},
      {"type":"predicate","field_id":"founded_on","operator_id":"gte","values":["2023-01-01"]}
    ],
    "limit": 200
  }'
```

## Similarweb recipes (free)

### Recipe 7 — Domain traffic snapshot

```python
# Using DaWe35/Similarweb-free-API approach (scrapes public Similarweb pages)
import requests
from bs4 import BeautifulSoup

def similarweb_snapshot(domain):
    r = requests.get(f"https://www.similarweb.com/website/{domain}/",
                     headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")
    # Extract: global rank, visits, avg duration, bounce rate, pages/visit
    # Schema changes; pin to current selectors and re-verify periodically
    return {"domain": domain, "rank": ..., "visits": ..., "bounce": ...}
```

For automated reliability, use `playwright-mcp` (real browser) instead of raw requests.

### Recipe 8 — Traffic share across competitors

```python
domains = ["anthropic.com", "openai.com", "mistral.ai", "cohere.com"]
results = [similarweb_snapshot(d) for d in domains]
df = pd.DataFrame(results)
df["traffic_share"] = df["visits"] / df["visits"].sum()
```

The shape of this distribution (top-heavy power law vs even split) signals market concentration.

### Recipe 9 — Traffic source breakdown

The free Similarweb page also shows traffic source breakdown (direct, search, social, referral, paid). Useful for "is this competitor SEO-led or paid-acquisition-led?"

## Combining Crunchbase + Similarweb + public sources

```python
# Composite profile for a private competitor
profile = {
    "name": "Acme AI",
    "founded": "2023-04",         # Crunchbase
    "hq": "San Francisco",         # Crunchbase
    "employees_band": "51-100",    # Crunchbase
    "total_funding_usd": 28e6,     # Crunchbase
    "last_round": {"type":"Series A","date":"2024-09","amount":18e6,"lead":"Sequoia"},  # CB
    "tech_stack": {...},           # Wappalyzer (competitive-intelligence-tech-stack)
    "monthly_visits": 850_000,     # Similarweb
    "traffic_sources": {"direct":0.45,"search":0.30,"referral":0.10,"social":0.10,"paid":0.05},  # Similarweb
    "github_active": True,         # GitHub API
    "patents_5y": 0,               # USPTO (often 0 for early startups)
}
```

This profile + the role.md SWOT framework + benchmark table = a competitive intelligence section for the report.

## Edge cases

- **Crunchbase free tier killed (2025):** The previously-free Crunchbase API is now paid-only. Without a key, fall back to `firecrawl-mcp` scrape of public profile pages — fields are limited (no funding rounds detail, no team).
- **Crunchbase data freshness:** funding rounds typically appear within 24h of press announcement; team / employee counts can be 3-12 months stale.
- **Similarweb anti-bot:** Similarweb blocks aggressive scrapers. Rate-limit to ≤10 requests/day per IP; use `playwright-mcp` for browser realism.
- **Similarweb data accuracy:** free Similarweb is panel-based; small sites have noisy / inflated estimates. Treat as directional, not precise.
- **API rate limits:** Crunchbase 200 req/min Basic, 600 req/min Pro. Paginate large queries.
- **Predicate / field ID format:** Crunchbase v4 uses opaque category UUIDs (`c4d8caf3-...`). Look them up first via `/searches/categories` or the docs.
- **Operating status filter:** for competitive landscapes, filter by `operating_status:active` to exclude shut-down companies.
- **Stealth-mode startups:** are often missing or have skeletal Crunchbase entries. Triangulate with LinkedIn employee count, GitHub org, news mentions.

## Sources

- Crunchbase API docs: https://data.crunchbase.com/docs/using-the-api
- Crunchbase API tutorial: https://data.crunchbase.com/docs/getting-started
- Similarweb-free-API: https://github.com/DaWe35/Similarweb-free-API
- Similarweb public: https://www.similarweb.com/

## Related skills

- `competitive-intelligence-tech-stack` — composes with this skill for full competitor profile
- `sec-edgar-market-sizing` — public-company complement
- `trend-fan-out-multi-source` — multi-signal trend / market context
