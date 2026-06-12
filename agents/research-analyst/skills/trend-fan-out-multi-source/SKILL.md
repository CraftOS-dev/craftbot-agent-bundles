<!--
Sources: pytrends https://github.com/GeneralMills/pytrends
         HN Algolia https://hn.algolia.com/api
         PRAW https://praw.readthedocs.io/
         GDELT 2.0 DOC https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
         arXiv API https://info.arxiv.org/help/api/user-manual.html
Companion playbook: role.md → "Trend analysis playbook"
-->

# Trend fan-out — 8-source weak-signal detection

Operationalizes the role.md trend analysis playbook by fanning a single research question out across **8 independent source types** in parallel, then triangulating which signals appear in ≥3 sources before declaring a trend. Single weak signals are not trends — patterns are trends.

## When to use this skill

- "Identify 3 emerging trends in [industry]"
- Weak-signal detection (early-stage technologies, behaviors, business models)
- Pattern validation (is this real or noise?)
- Pre-investment / pre-pivot due diligence
- Quarterly trend report generation

## When NOT to use

- For known, mainstream trends → use Perplexity Sonar Deep Research
- For pure news monitoring → use `gdelt-news-monitoring` standalone
- For corporate-R&D-specific trends → `patents-uspto-lens` is the leading indicator

## The 8 source types (from role.md playbook)

| # | Source type | Tool | Signal type |
|---|---|---|---|
| 1 | Search trends | pytrends (Google) + Baidu Index | Consumer demand |
| 2 | Social media | PRAW (Reddit), YouTube MCP | Community / sentiment |
| 3 | Tech discourse | HN Algolia | Developer / early-adopter |
| 4 | Patents | USPTO + Lens.org | Corporate R&D direction (lagging 2-5y) |
| 5 | Academic research | arXiv + OpenAlex via Paper Search MCP | Leading indicator (5-10y to market) |
| 6 | News | GDELT 2.0 (65 langs) + ai-news-collectors | Event-driven |
| 7 | Expert opinions | Targeted search + interview synthesis | Domain expertise |
| 8 | Consumer behavior | App store reviews, POS data, search queries | Behavioral validation |

## Setup

```bash
pip install pytrends praw gdeltdoc requests
export REDDIT_CLIENT_ID="..."
export REDDIT_CLIENT_SECRET="..."
export REDDIT_USER_AGENT="trend-research by /u/yourname"
```

`reddit-mcp`, `youtube-mcp`, `uspto-mcp`, `ai-news-collectors` already in `agent.yaml`.

## Common recipes

### Recipe 1 — Parallel fan-out (the core pattern)

```python
import concurrent.futures, datetime as dt

topic = "GLP-1 weight loss drugs"
five_yrs_back = (dt.date.today() - dt.timedelta(days=5*365)).isoformat()

def search_trends():
    from pytrends.request import TrendReq
    pytrends = TrendReq()
    pytrends.build_payload([topic], timeframe="today 5-y")
    return pytrends.interest_over_time()

def hn_signal():
    import requests
    r = requests.get(f"https://hn.algolia.com/api/v1/search?query={topic}&tags=story")
    return r.json()["hits"]

def reddit_signal():
    import praw
    reddit = praw.Reddit(client_id=os.environ["REDDIT_CLIENT_ID"],
                        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
                        user_agent=os.environ["REDDIT_USER_AGENT"])
    return [(p.title, p.subreddit.display_name, p.score, p.created_utc)
            for p in reddit.subreddit("all").search(topic, sort="top", time_filter="year", limit=50)]

def gdelt_signal():
    from gdeltdoc import GdeltDoc, Filters
    f = Filters(keyword=topic, start_date=five_yrs_back, end_date=str(dt.date.today()))
    return GdeltDoc().article_search(f)

def patents_signal():
    # via uspto-mcp or direct API
    import requests
    r = requests.get("https://api.patentsview.org/patents/query",
                     params={"q": f'{{"_text_phrase":{{"patent_title":"{topic}"}}}}',
                             "f":'["patent_number","patent_title","patent_date","assignee_organization"]',
                             "o":'{"per_page":100,"sort":[{"patent_date":"desc"}]}'},
                     headers={"User-Agent":"trend-research name@example.com"})
    return r.json()["patents"]

def arxiv_signal():
    import requests, xml.etree.ElementTree as ET
    r = requests.get(f"http://export.arxiv.org/api/query?search_query=all:{topic}&max_results=50&sortBy=submittedDate&sortOrder=descending")
    return r.text  # parse XML

# Fan out in parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
    futures = {
        "search_trends": ex.submit(search_trends),
        "hn":            ex.submit(hn_signal),
        "reddit":        ex.submit(reddit_signal),
        "gdelt":         ex.submit(gdelt_signal),
        "patents":       ex.submit(patents_signal),
        "arxiv":         ex.submit(arxiv_signal),
    }
    signals = {k: f.result() for k, f in futures.items()}
```

### Recipe 2 — Velocity / volume calculation per source

A trend = derivative is positive AND the magnitude is non-trivial. For each source:

```python
def velocity(series, periods=4):
    """Compute trailing-N-period growth rate."""
    if len(series) < periods + 1:
        return None
    recent = series.iloc[-periods:].mean()
    prior  = series.iloc[-2*periods:-periods].mean()
    return (recent / prior - 1) if prior else None

# Example: HN posts/month for the topic
hn_monthly = pd.DataFrame(signals["hn"]).assign(
    month=lambda d: pd.to_datetime(d["created_at"]).dt.to_period("M")
).groupby("month").size()

v = velocity(hn_monthly, periods=3)
print(f"HN velocity (last 3 months vs prior 3): {v:+.0%}")
```

### Recipe 3 — Cross-source validation (the triangulation rule)

```python
trend_signals = {
    "search_trends": velocity(signals["search_trends"][topic], periods=3),
    "hn":            velocity(hn_monthly, periods=3),
    "reddit":        velocity(reddit_monthly, periods=3),
    "gdelt":         velocity(gdelt_monthly, periods=3),
    "patents":       velocity(patents_quarterly, periods=2),
    "arxiv":         velocity(arxiv_quarterly, periods=2),
}

# Trend strength = number of sources with positive velocity ≥ +20%
positive = [k for k, v in trend_signals.items() if v is not None and v > 0.20]

if len(positive) >= 3:
    print(f"VALID TREND. Confirmed by {len(positive)} sources: {positive}")
elif len(positive) == 2:
    print(f"WEAK SIGNAL. Watch list: {positive}")
else:
    print(f"NOISE. Only {len(positive)} source(s) positive.")
```

### Recipe 4 — Leading-vs-lagging source layering

Order sources by lead time to assess where in the trend lifecycle we are:

```
Leading (5-10y out)       Lagging (already mainstream)
   ↓                                       ↓
arXiv → patents → HN → reddit → search trends → news → consumer behavior

Stage 1: arXiv only           = "research-stage"
Stage 2: arXiv + patents      = "corporate-investing stage"
Stage 3: + HN + reddit        = "early-adopter discourse"
Stage 4: + search trends      = "consumer awareness"
Stage 5: + news + behavior    = "mainstream adoption"
```

Report which stage the trend is in — this drives the timing estimate in the trend report.

### Recipe 5 — Scenario branching (best / base / worst / wildcard)

Per role.md playbook:

```python
trend_brief = {
    "headline": "<one-sentence trend statement>",
    "confidence": "<High/Moderate/Low>",
    "stage": "<1-5 from Recipe 4>",
    "timing": "<next quarter / year / decade>",
    "scenarios": {
        "best":     "Trend accelerates if [conditions]; reaches mainstream in X years",
        "base":     "Trend continues at current velocity; mainstream in Y years",
        "worst":    "Trend stalls if [conditions]; remains niche",
        "wildcard": "Discontinuity if [black-swan event]",
    },
    "early_indicators": ["<what to watch monthly>"],
    "tipping_points": ["<events that would invalidate or accelerate>"],
    "monitoring_plan": "<who/what/how often>",
}
```

### Recipe 6 — Cross-impact matrix (how trends interact)

When user asks "what are the top 3 trends," produce a 3×3 matrix:

```
              | Trend A | Trend B | Trend C
   Trend A   |   —     |  amp    |  sub
   Trend B   |  amp    |   —     |  neut
   Trend C   |  sub    |  neut   |   —

   amp = amplifies (B accelerates A)
   sub = substitutes (B replaces A)
   neut = independent
```

Use Claude extended thinking to populate. The matrix surfaces strategic implications a single-trend analysis would miss.

## Edge cases

- **pytrends rate limit + IP bans:** Google sometimes blocks pytrends after a burst. Sleep 5s between queries; rotate User-Agent. Consider PyTrends-API-Wrapper for resilience.
- **PRAW 60 rpm limit:** Reddit caps at 60 requests per minute (auth'd). For deep searches, scope to specific subreddits, not `r/all`.
- **HN Algolia 200-result cap per query:** paginate with `numericFilters=created_at_i>X` to walk older results.
- **arXiv 1 req / 3s rate limit:** schedule arXiv last in the fan-out; cache aggressively.
- **Topic ambiguity:** "GLP-1" matches drug research and gene papers. Pre-disambiguate with Claude before running fan-out.
- **Language coverage:** pytrends, HN, and Reddit are English-heavy. Pair with GDELT (65 languages) + Baidu Index for global validity.
- **Survivor bias in trends:** the trends you remember are the ones that succeeded. Always include a "what trends fizzled?" reverse search to calibrate.
- **Velocity vs absolute volume:** a topic going from 10 → 30 mentions is +200% but trivially small. Set a minimum-absolute-volume floor before declaring growth meaningful.

## Sources

- pytrends: https://github.com/GeneralMills/pytrends
- HN Algolia API: https://hn.algolia.com/api
- PRAW docs: https://praw.readthedocs.io/
- GDELT DOC 2.0: https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/ · https://api.gdeltproject.org/api/v2/doc/doc
- arXiv user manual: https://info.arxiv.org/help/api/user-manual.html
- role.md → Trend analysis playbook (this bundle)

## Related skills

- `gdelt-news-monitoring` — deeper dive on the news-signal source
- `patents-uspto-lens` — deeper dive on patent-signal source
- `paper-search-mcp` — deeper dive on the academic-signal source
- `data-storytelling-plotly-altair` — visualization for the trend report
