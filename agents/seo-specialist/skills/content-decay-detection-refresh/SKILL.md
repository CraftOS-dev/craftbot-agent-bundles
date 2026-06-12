<!--
Source: https://suganthan.com/blog/google-search-console-mcp-server/
Source: https://ahrefs.com/blog/content-decay/
Source: https://www.animalz.co/blog/content-decay/
Depth: 90-day decay detection + competitive SERP comparison + refresh workflow
-->
# Content Decay Detection + Refresh

## When to use

Reach for this skill when the user asks for: "content decay", "old content losing traffic", "refresh declining posts", "content audit for decay", "find pages losing rankings", "what posts to update", "evergreen content maintenance". This is the depth specialist — uses Suganthan GSC `content_decay` for 90-day trend detection, cross-references with Ahrefs `organic_keywords_changes` for ranking drops, prioritizes refresh by traffic-loss × ease-of-fix. Refresh playbook + post-refresh reindex via Indexing API.

## Setup

```bash
# Suganthan GSC MCP for decay detection
npx suganthan-gsc-mcp@2.2.2 --help

# Ahrefs MCP for ranking change confirmation
export AHREFS_MCP_TOKEN="<oauth-token>"

# DataForSEO for current SERP scrape (competitor diff)
export DFS_LOGIN="<login>"
export DFS_PASS="<password>"
```

Auth: see related skills.

## Common recipes

### Recipe 1: Suganthan GSC content_decay tool
```bash
mcp tool suganthan-gsc.content_decay \
  --site_url "sc-domain:example.com" \
  --window 90 \
  --decay_threshold -0.2 \
  --min_baseline_clicks 100 \
  --output_format json > decay.json
```
`decay_threshold=-0.2` = flag URLs with ≥20% click drop over trailing 90 days. `min_baseline_clicks=100` filters noise from low-traffic URLs.

### Recipe 2: Ranking-change confirmation via Ahrefs
```bash
# Cross-reference: declining clicks should correlate with position drops
mcp tool ahrefs.site_explorer \
  --target "example.com/declining-post" \
  --mode "organic_keywords_changes" \
  --period "90_days" \
  --include_metrics '["keyword","previous_position","current_position","volume","change"]'
```
Position drops + click drops = real decay (not seasonal). Click drops without position drops = SERP feature stolen or zero-click answers (AEO erosion).

### Recipe 3: Decay severity scoring
```python
import pandas as pd, json

decay = pd.DataFrame(json.load(open('decay.json'))['urls'])
# Columns: url, baseline_clicks, current_clicks, click_loss_pct, baseline_position, current_position

# Severity score = absolute click loss × baseline relative weight
decay['absolute_loss'] = decay['baseline_clicks'] - decay['current_clicks']
decay['severity'] = decay['absolute_loss'] * (decay['baseline_clicks'] / decay['baseline_clicks'].max())
decay = decay.sort_values('severity', ascending=False)
print(decay.head(20))
```

### Recipe 4: Refresh-vs-retire decision matrix
```python
def refresh_or_retire(row):
    # Retire if:
    # - Page topic no longer relevant (manual flag)
    # - 6+ month linear decline with no spike
    # - No backlinks worth preserving (Ahrefs URL Rating < 5)
    # - Position dropped from top 20 to >50 (severe ranking loss = topic shift or quality issue)
    if row['current_position'] > 50 and row['baseline_position'] < 20:
        return 'RETIRE'  # Lost the rankings entirely

    # Refresh if:
    # - Position 4-20 (striking distance) and recoverable
    # - Has decent baseline traffic and backlinks
    # - Topic still relevant
    if row['current_position'] >= 4 and row['current_position'] <= 20 and row['baseline_clicks'] >= 200:
        return 'REFRESH'

    # Consolidate if:
    # - Cannibalizing with another URL (see cannibalisation tool)
    return 'EVALUATE'

decay['action'] = decay.apply(refresh_or_retire, axis=1)
```

### Recipe 5: Competitor SERP diff (why are competitors winning?)
```python
# For each refresh candidate: what do top-3 competitors do differently?
from serp_skill import serp_analysis

def competitor_diff(target_keyword, our_url):
    serp = serp_analysis(target_keyword)
    top_3 = [r for r in serp['organic'][:3] if our_url not in r['url']]

    # Pull content from top 3 via firecrawl
    competitor_data = [firecrawl.scrape(r['url']) for r in top_3]

    # What do they have that we don't?
    our_content = firecrawl.scrape(our_url)

    analysis = {
        'our_word_count': len(our_content['markdown'].split()),
        'competitor_avg_word_count': sum(len(c['markdown'].split()) for c in competitor_data) // 3,
        'our_h2_count': our_content['markdown'].count('\n## '),
        'competitor_avg_h2_count': sum(c['markdown'].count('\n## ') for c in competitor_data) // 3,
        'our_year_mentioned': '2026' in our_content['markdown'],
        'competitor_year_mentioned': all('2026' in c['markdown'] for c in competitor_data),
        'features_present': serp['features'],
    }
    return analysis
```

### Recipe 6: Refresh brief generator
```python
def refresh_brief(url, decay_row, competitor_analysis):
    return {
        'url': url,
        'baseline_clicks': decay_row['baseline_clicks'],
        'current_clicks': decay_row['current_clicks'],
        'loss': f"{decay_row['click_loss_pct']:.0%}",
        'recommended_actions': [
            f"Update word count from {competitor_analysis['our_word_count']} to ~{competitor_analysis['competitor_avg_word_count']}",
            f"Add {max(0, competitor_analysis['competitor_avg_h2_count'] - competitor_analysis['our_h2_count'])} more H2 sections",
            "Update year references to 2026" if not competitor_analysis['our_year_mentioned'] else None,
            "Add Featured Snippet target (40-60 word answer)" if 'featured_snippet' in competitor_analysis['features_present'] else None,
            "Add FAQPage section + schema" if 'people_also_ask' in competitor_analysis['features_present'] else None,
            "Refresh statistics with 2025/2026 data",
            "Add 2-3 new examples from last 12 months",
            "Update dateModified",
            "Re-link internal supporting articles",
        ],
        'priority': decay_row['severity'],
    }

# Generate briefs for top 20 decay candidates
briefs = [refresh_brief(row['url'], row, competitor_diff(row['target_keyword'], row['url']))
          for _, row in decay[decay['action']=='REFRESH'].head(20).iterrows()]
```

### Recipe 7: Post-refresh reindex submission
```bash
# After content team publishes refresh
mcp tool suganthan-gsc.submit_url \
  --url "https://example.com/refreshed-post" \
  --type "URL_UPDATED"

# Mirror to IndexNow for Bing
curl -X POST "https://www.bing.com/indexnow?url=https://example.com/refreshed-post&key=$INDEXNOW_KEY"
```

### Recipe 8: Post-refresh tracking (14 days)
```python
# Snapshot pre-refresh + post-refresh at days 7 and 14
pre_refresh = {
    'url': 'https://example.com/refreshed-post',
    'date': '2026-06-09',
    'clicks_7d': 35,
    'impressions_7d': 850,
    'avg_position': 9.4,
}

# After refresh published 2026-06-10
# Day 7 check
day_7 = pull_gsc_metrics(url='https://example.com/refreshed-post', date_range=('2026-06-10','2026-06-17'))
# Day 14 check
day_14 = pull_gsc_metrics(url='https://example.com/refreshed-post', date_range=('2026-06-10','2026-06-24'))

# Refresh succeeded if day 14 clicks > pre_refresh.clicks_7d × 2 (doubled)
```

### Recipe 9: Bulk refresh planning (quarterly batch)
```python
# Quarterly: identify top-20 decay candidates, generate briefs, hand off to writers
decay_q = pd.DataFrame(json.load(open('decay-q.json'))['urls'])

# Filter to refreshable
refreshable = decay_q[decay_q['action'] == 'REFRESH'].head(20)

# Cross with content cluster (don't refresh non-strategic URLs)
strategic = refreshable[refreshable['url'].isin(strategic_cluster_urls)]

# Notion handoff
for _, row in strategic.iterrows():
    brief = refresh_brief(row['url'], row, competitor_diff(row['target_keyword'], row['url']))
    notion.create_page(db_id=editorial_db, properties={
        'URL': brief['url'],
        'Type': 'Refresh',
        'Priority': brief['priority'],
        'Brief': '\n'.join(brief['recommended_actions']),
        'Status': 'Backlog',
    })
```

### Recipe 10: Detect AEO-only decay (clicks down, position stable)
```python
# Click drop without position drop = AI surface stealing clicks (zero-click answers)
aeo_decay = decay[
    (decay['click_loss_pct'] < -0.2) &
    (abs(decay['current_position'] - decay['baseline_position']) < 1)
]

# For these: AEO content optimization push, not traditional content refresh
# See aeo-content-optimization-entity-rich skill
print(f"AEO decay candidates: {len(aeo_decay)}")
```

## Examples

### Example 1: Quarterly content refresh planning
**Goal:** Identify top-20 decay candidates and produce refresh briefs.

**Steps:**
1. Recipe 1: Suganthan GSC `content_decay` for 90-day window, threshold -20%.
2. Recipe 2: cross-confirm with Ahrefs ranking changes (filter out seasonal/algorithm fluctuations).
3. Recipe 3: severity scoring → top 30 candidates.
4. Recipe 4: refresh-vs-retire-vs-consolidate per URL.
5. Recipe 5 + 6: per-URL competitor diff + refresh brief.
6. Recipe 9: Notion DB handoff.
7. Hand off to `technical-writer` for content production.
8. After publish: Recipe 7 reindex; Recipe 8 14-day tracking.

**Result:** 20 refreshed URLs/quarter; ~30-50% click recovery on refreshed URLs typical.

### Example 2: AEO erosion diagnosis
**Goal:** Top article positions stable but clicks dropped 30% — what changed?

**Steps:**
1. Recipe 10: identify AEO decay (clicks down, position stable).
2. Confirm AI Overview present on target query (DataForSEO SERP `ai_overview` field).
3. Confirm article cited in AI Overview but click-through reduced.
4. Action: AEO content optimization (`aeo-content-optimization-entity-rich` skill) — strengthen direct-answer block to compete for citation that drives click-through vs zero-click consumption.

**Result:** AEO push instead of traditional refresh.

### Example 3: Bulk evergreen content audit
**Goal:** 200-article blog, audit which need annual refresh.

**Steps:**
1. Recipe 1 with `window=180, decay_threshold=-0.1` for slower-decay detection.
2. Filter by article cluster (strategic vs supporting vs orphan).
3. Strategic decay: refresh immediately.
4. Supporting decay: refresh during quarterly cycle.
5. Orphan decay + retire if no backlinks + low traffic.

**Result:** Tiered refresh cadence; aligned with content strategy.

## Edge cases / gotchas

- **Seasonal decay confounding** — 90-day window may overlap with seasonal lows. Compare year-over-year for high-seasonality topics.
- **Algorithm-update decay vs natural decay** — check Sistrix / Semrush Sensor for confirmed Google updates near decay start date.
- **`content_decay` doesn't distinguish AEO erosion** — Recipe 10 manually classifies via position vs click delta.
- **dateModified update alone doesn't trigger reindex** — actual content change required. Google detects "just date updates" as gaming.
- **Refresh frequency too high** — refreshing every 30 days looks gamey; quarterly cadence safer.
- **Don't refresh top-3 ranked articles** — risk regression. Reserve refresh for striking-distance (positions 4-20) URLs.
- **Refresh with substantial changes — ≥30% content delta minimum** — minor tweaks insufficient signal.
- **Cross with cannibalization first** — if decay is from cannibalization (new page eating clicks), refresh wrong page. Run cannibalization audit first.
- **Backlink retention** — refresh doesn't break backlinks (unless URL changes). Don't change URL during refresh.
- **Reindex doesn't accelerate ranking recovery** — Indexing API submission speeds discovery only. Ranking recovery takes 2-6 weeks regardless.
- **`baseline_clicks` window size matters** — `window=90` baseline = prior 90 days vs current 90 days. For longer-term decay use `window=180`.

## Sources

- [Suganthan GSC MCP — content_decay tool](https://suganthan.com/blog/google-search-console-mcp-server/)
- [Ahrefs blog — content decay](https://ahrefs.com/blog/content-decay/)
- [Animalz — content decay studies](https://www.animalz.co/blog/content-decay/)
- [Backlinko — content refresh case study](https://backlinko.com/content-refresh)
- [Google Search Central — Helpful Content System](https://developers.google.com/search/docs/appearance/helpful-content-system)
- [Google Search Central — request indexing](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl)
