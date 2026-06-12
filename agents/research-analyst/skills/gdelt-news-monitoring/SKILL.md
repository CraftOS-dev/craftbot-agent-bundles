<!--
Source: https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
        https://api.gdeltproject.org/api/v2/doc/doc
Python wrapper: pip install gdeltdoc
Coverage: 65 languages, 3-month rolling window
-->

# GDELT 2.0 DOC API — multilingual news monitoring

GDELT (Global Database of Events, Language, and Tone) monitors news media in 65+ languages with continuous updates. The DOC 2.0 API exposes a queryable interface to the rolling 3-month window of article-level data including tone analysis, theme tagging, and geographic enrichment.

## When to use this skill

- News-signal source in trend fan-out (one of the 8 source types)
- Multilingual event monitoring (the only free tool covering 65 languages)
- Sentiment / tone tracking over time on a topic
- Theme detection (GDELT's GKG taxonomy: ECON_BANKRUPTCY, EPU_ECONOMY, HEALTH, etc.)
- Geographic localization of news interest (which countries are covering this?)
- Volume-over-time graphs (article counts per topic per day)
- Cross-language coverage comparison (US vs EU vs China coverage divergence)

## When NOT to use

- For coverage > 3 months back → GDELT 2.0 DOC API is rolling 3-month only; for historical use the GDELT BigQuery dataset
- For full article text → DOC API returns metadata + snippets; for full text use `firecrawl-mcp` on the URLs
- For paywalled-source monitoring → GDELT indexes only what it can crawl publicly
- For social media → GDELT is news-only; use `reddit-mcp` / X API

## Setup

```bash
pip install gdeltdoc
# No API key required, no rate limit documented (be polite)
```

## Common recipes

### Recipe 1 — Article search

```python
from gdeltdoc import GdeltDoc, Filters

f = Filters(
    keyword="\"GLP-1\" OR \"semaglutide\"",
    start_date="2025-12-01",
    end_date="2026-06-01",
    country=["US","GB","CA"],
    language=["English"],
)
gd = GdeltDoc()
articles = gd.article_search(f)
# Returns DataFrame: url, url_mobile, title, seendate, socialimage, domain, language, sourcecountry
```

### Recipe 2 — Volume over time (the "is this trending" signal)

```python
f = Filters(keyword="quantum computing breakthrough", start_date="2026-03-01", end_date="2026-06-01")
volume = gd.timeline_search("timelinevol", f)
# Returns DataFrame indexed by datetime with volume column (% of total daily news mentions)
```

### Recipe 3 — Tone analysis

GDELT scores each article on tone (-100 = very negative, +100 = very positive):

```python
tone = gd.timeline_search("timelinetone", f)
# Average tone of articles mentioning the keyword over time
# Useful: detect when sentiment shifts (e.g., positive → negative on a company)
```

### Recipe 4 — Theme detection (GKG taxonomy)

GDELT tags every article with one or more themes from its Global Knowledge Graph:

```python
f = Filters(
    keyword="Tesla layoffs",
    start_date="2026-01-01",
    end_date="2026-06-01",
    theme=["ECON_BANKRUPTCY","ECON_LAYOFFS"],
)
articles = gd.article_search(f)
```

Common GKG themes:

| Theme | Use |
|---|---|
| `ECON_BANKRUPTCY` | Bankruptcies / restructuring |
| `ECON_LAYOFFS` | Layoff announcements |
| `EPU_ECONOMY` | Economic policy uncertainty |
| `HEALTH_PANDEMIC` | Pandemic-related |
| `TECH_AUTOMATION` | Automation / AI |
| `MEDIA_SOCIAL` | Social media events |
| `LEGISLATION` | Bills / regulatory |

Full list: https://blog.gdeltproject.org/the-gdelt-global-knowledge-graph-gkg-data-format-codebook-v2-1/

### Recipe 5 — Country coverage divergence

```python
# Same topic, different countries — where is it getting traction?
for country in ["US","DE","FR","JP","BR","IN"]:
    f = Filters(keyword="carbon tax", start_date="2026-01-01", end_date="2026-06-01",
                country=[country])
    df = gd.article_search(f)
    print(f"{country}: {len(df)} articles, top domain: {df.domain.value_counts().head(3).to_dict()}")
```

### Recipe 6 — Image search

GDELT also indexes the dominant image per article (the "social image"). Useful for visualization of how a story is being framed:

```python
# Articles with their lead images
articles[["title", "domain", "socialimage"]]
```

### Recipe 7 — Cross-language news monitoring

For a global topic:

```python
for lang in ["English","Spanish","Chinese","Arabic","Russian","French","Japanese","Portuguese"]:
    f = Filters(keyword="renewable energy storage", start_date="2026-03-01", end_date="2026-06-01",
                language=[lang])
    df = gd.article_search(f)
    print(f"{lang}: {len(df)} articles")
```

Then use `deepl-mcp` to translate non-English snippets for synthesis.

## Edge cases

- **Rolling 3-month window:** the DOC 2.0 API only goes back 3 months from today. For longer history, query the GDELT 2.0 BigQuery public dataset (`gdelt-bq.gdeltv2`) — free up to 1 TB/month with a Google Cloud account.
- **Keyword OR-grouping syntax:** GDELT uses spaces as implicit AND; OR must be uppercase between quoted phrases: `"climate" OR "carbon"`. NOT operator: `-keyword`.
- **Volume is normalized:** `timelinevol` returns *% of total daily news* — small absolute changes can amplify the % if total daily news drops. Cross-check with raw article counts.
- **Tone is noisy:** GDELT tone is computed lexically (positive/negative word frequency), not semantically. Use as directional signal, not absolute truth.
- **Domain noise:** GDELT crawls everything — some "news" sites are content farms. Pre-filter by domain reputation (cross-check with NewsGuard / Media Bias Fact Check if available, or whitelist authoritative domains).
- **Geographic enrichment lag:** GDELT's CAMEO-coded geographic location is ~95% accurate; spot-check before claiming country-level trends.
- **Themes are coarse:** GKG themes are useful for filtering but not for fine-grained classification. For deeper categorization, run zero-shot classification on titles via Claude / local LLM.

## Sources

- GDELT 2.0 DOC API blog: https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
- DOC API reference: https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
- gdeltdoc Python package: https://github.com/alex9smith/gdelt-doc-api
- GKG theme codebook: https://blog.gdeltproject.org/the-gdelt-global-knowledge-graph-gkg-data-format-codebook-v2-1/
- BigQuery dataset (history > 3 months): https://www.gdeltproject.org/data.html#googlebigquery

## Related skills

- `trend-fan-out-multi-source` — GDELT as one of 8 trend sources
- `ai-news-collectors` (default skill) — supplementary news coverage
- `perplexity-deep-research` — synthesizes; GDELT enumerates
