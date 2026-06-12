<!--
Sources: Ahrefs https://ahrefs.com/
         SEMrush https://www.semrush.com/
         Similarweb https://www.similarweb.com/
         DataForSEO https://dataforseo.com/
         SEMrush vs Similarweb https://www.stylefactoryproductions.com/blog/semrush-vs-similarweb
         OnlySearch competitive intel sources https://onlysearch.ai/blog/competitive-intel-data-sources
Companion playbook: role.md → "SOTA tool reference" → Ahrefs / SEMrush / Similarweb / DataForSEO
-->

# Competitor SEO intelligence (Ahrefs / SEMrush / Similarweb / DataForSEO)

Organic-search competitive intel. Ahrefs (strongest backlink + organic, ~15-25% accurate on 100k+ session sites). SEMrush (best keyword research depth + Top Pages for LP analysis + share-of-voice). Similarweb (high-level traffic share; ~40-70% off for small sites). DataForSEO (pay-per-task SERP, most flexible). Free fallback: multi-engine SERP via brave / duckduckgo / tavily + DataForSEO pay-per-task.

## When to use

- "Compare our SEO position to [competitor]'s"
- "What keywords are they ranking on?"
- "Their backlink profile vs ours?"
- "Their top organic landing pages"
- "Their share-of-voice in our category"
- Pre-content-strategy: keyword gap analysis
- Pre-LP-rebuild: their highest-traffic LPs and what's working
- Competitive share-of-voice trending (quarterly)

## When NOT to use

- Paid search keywords → use `competitor-ad-pathmatics-spyfu-semrush`
- Brand sentiment / social mentions → social-listening (Brandwatch class)
- Mobile app store SEO → use `competitor-app-intel-sensor-tower-data-ai`
- Internal site search analytics → out of scope

## Setup

```bash
# Ahrefs ($500+/mo Lite; API on Standard+)
export AHREFS_API_KEY="..."
export AHREFS_API_BASE="https://api.ahrefs.com/v3"

# SEMrush ($130+/mo Pro; .Trends from $289/mo for traffic intel)
export SEMRUSH_API_KEY="..."

# Similarweb ($500+/mo minimum; usually $2-10k+/mo)
export SIMILARWEB_API_KEY="..."

# DataForSEO (pay-per-task, very cheap)
export DATAFORSEO_LOGIN="..."
export DATAFORSEO_PASSWORD="..."

# Free fallback: search-engine MCPs (brave, duckduckgo, tavily)
export BRAVE_API_KEY="..."
export TAVILY_API_KEY="..."
```

MCPs in `agent.yaml`: `firecrawl-mcp`, `playwright-mcp`, `brave-search`, `tavily-search`, `duckduckgo-search`, `slack-mcp`, `notion-mcp`.

## Common recipes

### Recipe 1: Ahrefs — competitor organic keywords overlap

```bash
curl -H "Authorization: Bearer $AHREFS_API_KEY" \
  "$AHREFS_API_BASE/site-explorer/organic-keywords?\
target=acme.example.com&\
country=us&\
limit=1000&\
order_by=traffic:desc"
```

Returns: keywords, position, search volume, traffic, URL ranking.

### Recipe 2: Ahrefs — backlink gap (us vs them)

```bash
curl -H "Authorization: Bearer $AHREFS_API_KEY" \
  "$AHREFS_API_BASE/site-explorer/link-intersect?\
targets=acme.example.com,beta.example.com&\
exclude_target=us.example.com"
```

Returns: domains linking to competitors but not us — backlink-acquisition prospect list.

### Recipe 3: Ahrefs — Top Pages

```bash
curl -H "Authorization: Bearer $AHREFS_API_KEY" \
  "$AHREFS_API_BASE/site-explorer/top-pages?\
target=acme.example.com&\
limit=100&\
order_by=traffic:desc"
```

### Recipe 4: SEMrush — Top Pages + keyword overlap

```bash
# Top Pages
curl "https://api.semrush.com/?\
type=domain_organic_organic&\
key=$SEMRUSH_API_KEY&\
domain=acme.example.com&\
database=us&\
display_limit=100"
```

### Recipe 5: SEMrush — keyword gap (5-domain)

```bash
curl "https://api.semrush.com/?\
type=domain_organic_unique&\
key=$SEMRUSH_API_KEY&\
domain=acme.example.com&\
database=us&\
display_filter=%2B%7CPo%7CLt%7C10"
# +Po Lt 10 = position less than 10 (i.e., page 1)
```

### Recipe 6: SEMrush — share-of-voice

```bash
# Position Tracking endpoint — share of voice for a tracked keyword set
curl "https://api.semrush.com/reports/v1/projects/$PROJECT_ID/tracking/?\
key=$SEMRUSH_API_KEY&\
action=report&\
type=tracking_overview_organic"
```

### Recipe 7: Similarweb — traffic share

```bash
curl -H "api-key: $SIMILARWEB_API_KEY" \
  "https://api.similarweb.com/v1/website/acme.example.com/total-traffic-and-engagement/visits?\
country=us&\
granularity=monthly&\
start_date=2026-01&\
end_date=2026-05&\
main_domain_only=false"
```

### Recipe 8: DataForSEO — SERP pull pay-per-task

```bash
# Cheap SERP for any keyword
curl -u "$DATAFORSEO_LOGIN:$DATAFORSEO_PASSWORD" \
  -X POST "https://api.dataforseo.com/v3/serp/google/organic/live/advanced" \
  -H "Content-Type: application/json" \
  -d '[{
    "keyword": "best sales engagement platform",
    "location_code": 2840,
    "language_code": "en",
    "depth": 30
  }]'
```

Pay-per-task ~$0.001-$0.01 per query. Cheapest way to monitor SERPs for a 200-keyword target set.

### Recipe 9: Free fallback — multi-engine SERP via Brave/Tavily/DDG

```python
# When budget-constrained
from search_mcps import brave, tavily, duckduckgo
keyword = "best sales engagement platform"
serps = {
    "brave":      brave.search(keyword, count=20),
    "tavily":     tavily.search(keyword, max_results=20),
    "duckduckgo": duckduckgo.search(keyword, max_results=20),
}
# Union → ranked by appearance frequency = approximate "page 1 consensus"
```

### Recipe 10: Keyword-gap matrix

```python
import pandas as pd
us   = set([k["keyword"] for k in ahrefs_keywords("us.example.com")])
them = set([k["keyword"] for k in ahrefs_keywords("acme.example.com")])
gap_them_only = them - us
gap_us_only   = us - them
shared        = us & them
# Build CSV of high-volume gap keywords for content strategy
df = pd.DataFrame({
    "keyword": list(gap_them_only),
    "their_position": [...],
    "their_traffic": [...],
})
df.sort_values("their_traffic", ascending=False).head(50).to_csv("acme_keyword_gap.csv")
```

### Recipe 11: Top-page LP analysis

```python
# Pair Recipe 4 with Playwright to capture the actual LP DOM + Lighthouse score
from playwright.sync_api import sync_playwright
top_pages = semrush_top_pages("acme.example.com", limit=20)
for p in top_pages:
    with sync_playwright() as pw:
        page = pw.chromium.launch().new_page()
        page.goto(p["url"])
        page.screenshot(path=f"acme_lp_{slug(p['url'])}.png", full_page=True)
        # Extract H1, CTA copy, form fields, social proof
        print(p["url"], page.title(), page.query_selector("h1").text_content())
```

### Recipe 12: Share-of-voice tracking

```python
# For each keyword in your target set, who's on page 1?
import pandas as pd
keywords = open("target_keywords.txt").read().splitlines()
sov = {c: 0 for c in ["us","acme","beta","gamma","delta","epsilon"]}
for kw in keywords:
    serp = dataforseo_serp(kw)
    for r in serp[:10]:
        for c in sov:
            if c in r["domain"]:
                sov[c] += 1
print("Share of voice (page 1):", sov)
```

### Recipe 13: Quarterly diff digest

```python
# Compare current quarter's SoV / keyword count / traffic estimate to prior
delta = {
    "us":   {"sov": +4,  "keywords": +120, "traffic": +18000},
    "acme": {"sov": -2,  "keywords": -45,  "traffic": -8000},
}
# Render into QBR slide; Slack to #ci-digest
```

## Examples

### Example 1: Keyword-gap content strategy

**Goal:** Find 30 keywords where Acme ranks page 1 but we don't.

**Steps:**
1. Recipe 1 → Ahrefs organic keywords for both.
2. Recipe 10 → set-diff; sort by Acme's traffic.
3. Filter: search volume > 500/mo, intent = commercial.
4. Output CSV → marketing content strategy backlog.

**Result:** Prioritized 30-keyword content backlog; 12-week sprint plan.

### Example 2: Backlink-acquisition prospect list

**Goal:** Identify domains linking to Acme + Beta but not us.

**Steps:**
1. Recipe 2 → Ahrefs link-intersect endpoint.
2. Filter: domain rating > 40, in our vertical, contact info available.
3. Output CSV → outreach team.

**Result:** 184-domain backlink-acquisition list.

### Example 3: Free-path SoV tracking (no paid SEO tool)

**Goal:** Track quarterly SoV for $100/quarter via DataForSEO.

**Steps:**
1. Recipe 8 → DataForSEO SERP for 200 keywords quarterly. ~$2 per run.
2. Recipe 12 → calculate SoV.
3. Recipe 13 → quarterly delta digest.

**Result:** Workable SoV trend on a tight budget.

### Example 4: LP teardown of competitor's top 20 pages

**Goal:** Understand what messaging is driving Acme's organic traffic.

**Steps:**
1. Recipe 4 → SEMrush Top Pages for Acme.
2. Recipe 11 → Playwright + screenshot + DOM extract for top 20.
3. LLM theme extraction → cluster into messaging archetypes.
4. Pair with `competitor-messaging-tracking-diff` historical archive.

**Result:** Messaging insights feeding our LP strategy + battlecard pane 6 (kill-shots).

## Edge cases / gotchas

- **Accuracy decay below 100k sessions** — Ahrefs ~15-25% off above 100k; below, much worse. Similarweb ~40-70% off for small sites. Use as directional, not absolute, for small competitors.
- **SEMrush vs Ahrefs database differences** — different crawl coverage; sometimes keyword shown in one but not the other. Use union if budget allows.
- **SEMrush units** — API consumes units per call; "lines" returned. Heavy multi-domain comparisons burn through quota fast.
- **Ahrefs API tiers** — Lite has no API; Standard ($500/mo) limits. Plan calls.
- **Similarweb min spend** — $500+/mo enterprise floor.
- **Free fallback bias** — Brave/DDG/Tavily SERPs personalize less than Google but still have bias (date, geo). Test multiple times.
- **DataForSEO consistency** — pay-per-task model; pricing changes; check current pricing.
- **JavaScript-rendered content invisible to crawlers** — Ahrefs may miss content behind JS. Use Playwright + Lighthouse for our pages to verify.
- **Localization** — UK / DE / FR rankings differ from US; specify country code explicitly in every call.
- **Featured-snippet stealing** — Position 0 (featured snippet) skews "rank" — Ahrefs and SEMrush handle this differently.
- **Brand-keyword inflation** — competitor's branded keywords (`acme login`) inflate their "traffic"; filter brand keywords out of gap analyses.
- **Backlink quality vs quantity** — raw backlink count meaningless; use Domain Rating (DR) / referring-domains-with-DR>X.
- **Don't scrape SEMrush / Ahrefs HTML** — ToS violation. Use the paid API only.
- **PROACTIVE.md cadence** — monthly default for SEO snapshots; weekly during content sprints.
- **Provenance footer** — cite Ahrefs/SEMrush/DataForSEO API + retrieval date; mark Similarweb as "directional" for small-site claims.

## Sources

- Ahrefs — https://ahrefs.com/
- Ahrefs API v3 — https://ahrefs.com/api/documentation
- SEMrush API — https://developer.semrush.com/api/
- Similarweb — https://www.similarweb.com/
- DataForSEO — https://dataforseo.com/
- SEMrush vs Similarweb — https://www.stylefactoryproductions.com/blog/semrush-vs-similarweb
- OnlySearch CI data sources — https://onlysearch.ai/blog/competitive-intel-data-sources
- role.md → "SOTA tool reference" → Ahrefs / SEMrush / Similarweb / DataForSEO

## Related skills

- `competitor-ad-pathmatics-spyfu-semrush` — paired paid + organic via SEMrush
- `competitor-messaging-tracking-diff` — LP messaging analysis paired with Top Pages
- `competitor-tech-stack-builtwith-wappalyzer` — infrastructure inference for site speed / SEO
- `continuous-competitor-monitoring-klue-kompyte-crayon` — monthly SoV snapshot in fan-out
- `feature-parity-tracking` — content-feature parity (their guides / docs vs ours)
