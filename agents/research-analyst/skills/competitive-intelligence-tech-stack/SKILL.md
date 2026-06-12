<!--
Sources: Wappalyzer https://www.wappalyzer.com/
         python-Wappalyzer https://github.com/chorsley/python-Wappalyzer
         GitHub API https://docs.github.com/en/rest
Companion playbook: role.md → "Competitive intelligence playbook"
-->

# Competitive intelligence — tech-stack + financials + IP + pricing

Multi-source operationalization of the role.md competitive intelligence playbook. Composes Wappalyzer (tech stack), SEC EDGAR (financials), Lens.org/USPTO (IP), GitHub API (engineering signals), and playwright-mcp (pricing scrape) into a single competitor profile workflow. Ethical / public-source only.

## When to use this skill

- "What's our competitive position vs Y?"
- SWOT analysis of a named competitor
- Pricing benchmark across 5-10 competitors
- Detecting competitor technology choices (engineering blog signal)
- Tracking competitor engineering team size / hiring velocity
- Patent portfolio comparison
- Quarterly competitive review

## When NOT to use

- For private-information / insider-leak research → refuse; ethics rule
- For "find every competitor" mapping → use Crunchbase + Similarweb first to enumerate
- For market-sizing → use `sec-edgar-market-sizing` (this skill assumes competitors are already named)
- For pricing of products without public pricing pages → flag as unobtainable via public methods

## The composite profile (per competitor)

For each named competitor, produce:

| Dimension | Source |
|---|---|
| Financials (if public) | SEC EDGAR XBRL via `sec-edgar-mcp` |
| Tech stack (frontend) | Wappalyzer on landing page |
| Tech stack (backend hints) | Job posts + engineering blog + GitHub orgs |
| Engineering signal | GitHub org public repos, contributors, recent activity |
| IP portfolio | Lens.org + USPTO PatentsView |
| Pricing | playwright-mcp scrape of pricing page |
| Product features | Manual + screenshot of public docs |
| Customer reviews | G2, Capterra, App Store, public forums |
| Funding (if private) | Crunchbase via `crunchbase-market-research` |
| Marketing channels | SimilarWeb traffic-share + ad-library (Meta, Google) |

## Setup

```bash
pip install python-Wappalyzer beautifulsoup4 requests
# GitHub token (free)
export GITHUB_TOKEN="ghp_..."
# Lens.org token (from skills/patents-uspto-lens)
export LENS_API_TOKEN="..."
# SEC User-Agent (from skills/sec-edgar-market-sizing)
export EDGAR_USER_AGENT="Research Analyst name@example.com"
```

`github-api`, `playwright-mcp`, `firecrawl`, `sec-edgar-mcp`, `uspto-mcp` already in `agent.yaml`.

## Common recipes

### Recipe 1 — Wappalyzer tech detection

```python
from Wappalyzer import Wappalyzer, WebPage

wappalyzer = Wappalyzer.latest()
page = WebPage.new_from_url("https://example-competitor.com")
techs = wappalyzer.analyze_with_versions_and_categories(page)
# Returns: {"React": {"versions":["18.2.0"],"categories":["JavaScript framework"]}, ...}
```

Categories include: JavaScript framework, web server, CMS, e-commerce, analytics, advertising, payment processor, CDN, font scripts, marketing automation, etc.

### Recipe 2 — Wappalyzer via Playwright (for JS-rendered sites)

```javascript
// Inject Wappalyzer JS via playwright-mcp
// page.evaluate(wappalyzerJS) returns same JSON structure
// Useful when python-Wappalyzer misses JS-heavy SPAs
```

### Recipe 3 — Pricing-page scrape

```python
# Use playwright-mcp to render the pricing page (handles JS pricing tables)
# Then extract structured pricing into a comparison table:
# tier | price/mo | seats | features | notes

# Example output:
{
  "competitor": "Acme",
  "tiers": [
    {"name": "Free",   "price_mo": 0,    "seats": 1,    "features": ["basic search","limited storage"]},
    {"name": "Pro",    "price_mo": 49,   "seats": 5,    "features": ["unlimited search","SSO"]},
    {"name": "Enterprise","price_mo": None, "seats": "custom", "features": ["custom"]},
  ],
  "scrape_date": "2026-06-09",
  "url": "https://acme.example.com/pricing",
}
```

### Recipe 4 — GitHub engineering signal

```python
import requests
H = {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"}

# Find competitor's org
org = "anthropics"
r = requests.get(f"https://api.github.com/orgs/{org}", headers=H).json()

# Public repo activity (engineering velocity proxy)
repos = requests.get(f"https://api.github.com/orgs/{org}/repos?per_page=100&sort=updated", headers=H).json()
recent = [r for r in repos if r["pushed_at"] > "2026-03-01"]
print(f"{org}: {len(repos)} public repos, {len(recent)} active in last 3 mo")

# Top contributors (talent signal)
for repo in repos[:5]:
    contribs = requests.get(repo["contributors_url"] + "?per_page=20", headers=H).json()
    print(repo["name"], "→", len(contribs), "contributors")
```

### Recipe 5 — Job-posting signal (hiring velocity + tech reveals)

Engineering job posts reveal back-end tech, scale, and hiring velocity. Scrape competitor /careers via `firecrawl-mcp` or `playwright-mcp`:

```python
# Pseudocode
job_posts = firecrawl.scrape("https://competitor.com/careers/engineering")
techs = extract_keywords(job_posts, dictionary=["Kubernetes","Postgres","Kafka","Rust","Go","Snowflake","Databricks","BigQuery","React","Vue","Svelte"])
hire_rate = len(job_posts) / 90  # postings per day, 90-day window
```

A spike in Rust / Go / Kubernetes job posts ≈ migration in progress. Track over time.

### Recipe 6 — Patent portfolio summary

```python
# See skills/patents-uspto-lens for full detail
# Quick summary for competitor "Acme Corp":
acme_patents = uspto_search(assignee="Acme Corp", date_from="2020-01-01")
cpc_counts = pd.Series([p["cpc_subgroup_id"] for p in acme_patents]).value_counts()
# Top 5 CPC subgroups = competitor's R&D focus areas
```

### Recipe 7 — Customer review aggregation

```bash
# G2 / Capterra / TrustRadius / App stores via firecrawl-mcp or playwright-mcp
# Extract: rating, review count, common pain points (NLP), common praise

# Or use Google Places API for B2C reviews of physical locations
```

### Recipe 8 — Composite SWOT generation

After collecting the data above, use Claude to synthesize per the role.md SWOT format:

```
[Per competitor]
STRENGTHS
  - <distinctive capability> — evidence: <tech stack / patent / financial>
  - ...
WEAKNESSES
  - <capability gap> — evidence: <missing tech / customer complaint / financial>
  - ...
OPPORTUNITIES
  - <adjacent market they could enter> — evidence: <patent direction / hiring>
  - ...
THREATS
  - <substitute / new entrant / regulatory> — evidence: <signal>
  - ...
```

Cite each bullet to a source artifact (tech-stack scan date, 10-K filing, patent number, job-posting URL).

### Recipe 9 — Benchmark table (cross-competitor)

```python
benchmark = pd.DataFrame({
    "Competitor": ["Acme","Beta","Gamma"],
    "Revenue (latest FY)": [124e6, 87e6, None],   # None for private
    "Employees": [340, 220, 180],
    "Public repos": [42, 18, 95],
    "Active recent": [15, 6, 38],
    "Pricing tier 1": [49, 39, 0],
    "Pricing tier 2": [149, 119, 50],
    "Patent count (5y)": [12, 4, 31],
    "G2 rating": [4.5, 4.2, 4.6],
    "G2 review count": [340, 120, 510],
    "Funding total (CB)": [None, None, 110e6],  # None for public
}).set_index("Competitor")
```

This becomes the "Benchmark" section of the competitive intelligence report.

### Recipe 10 — Monitoring system setup

After the initial CI report, set up monitoring triggers:

```python
# Triggers (handed off to a scheduled job, NOT this skill):
# - New 10-K / 10-Q filed → re-run financial summary
# - New patent published (>5 per quarter) → patent landscape diff
# - Pricing page changed (compare hash) → re-scrape + diff
# - GitHub org adds >3 repos / month → engineering update
# - New negative review batch on G2 → sentiment alert
```

The role.md playbook specifies "recurring quarterly competitive reviews"; the monitoring catches material changes between cycles.

## Edge cases

- **Ethical guardrails:** never include data from leaks, breach dumps, scraping of authenticated areas, or insider sources. Document the source URL of every claim — if you can't, drop the claim.
- **Bot blocking:** competitors increasingly block scrapers. Use `playwright-mcp` with stealth headers when `firecrawl-mcp` fails; if both fail, accept the gap and note it.
- **Pricing-page changes:** competitors A/B test pricing. Scrape multiple times over 2 weeks before drawing conclusions about "current" pricing.
- **GitHub org coverage:** competitor's internal repos are not public. Public repo activity is a sample, not the full picture. Triangulate with job-posting tech mentions.
- **Patent assignee variants:** "Acme Corp", "Acme Corporation", "Acme Inc". Always search with `_or` operator across spellings.
- **International competitors:** SEC EDGAR is US-only. For EU competitors use the EU Transparency Register + national equivalents (Companies House UK, Bundesanzeiger DE). Asian competitors: CNINFO (CN), JFSA (JP), DART (KR).
- **Customer review bias:** G2 / Capterra reviews skew positive (incentivized). For unfiltered signal, check Reddit, X, Hacker News mentions.
- **Confirmation bias:** the analyst hypothesizes a competitor is weak → finds evidence confirming. Force the SWOT to include ≥3 of each (S, W, O, T) before signing off.

## Sources

- Wappalyzer: https://www.wappalyzer.com/
- python-Wappalyzer: https://github.com/chorsley/python-Wappalyzer
- GitHub REST API: https://docs.github.com/en/rest
- SEC EDGAR: https://www.sec.gov/edgar/sec-api-documentation (see `sec-edgar-market-sizing` skill)
- Lens.org Patents: https://docs.api.lens.org/ (see `patents-uspto-lens` skill)
- role.md → "Competitive intelligence playbook" (this bundle)

## Related skills

- `sec-edgar-market-sizing` — financial benchmarks
- `patents-uspto-lens` — IP portfolio analysis
- `crunchbase-market-research` — private-company financials / funding
- `trend-fan-out-multi-source` — when CI question shades into trend research
