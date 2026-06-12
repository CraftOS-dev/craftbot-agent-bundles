<!--
Source: https://help.ahrefs.com/en/articles/13913559-getting-started-with-ahrefs-mcp
Source: https://www.semrush.com/kb/12-keyword-gap-comparison-report
Source: https://www.marketmuse.com/api/
Depth: content gap vs N competitors + topical-cluster coverage gap with MarketMuse cross-check
-->
# Content Gap Analysis — Competitive

## When to use

Reach for this skill when the user asks for: "content gap vs competitors", "what keywords are competitors winning", "what should I write next", "competitive content audit", "topic gap analysis", "where am I missing coverage". This is the depth specialist — uses Ahrefs `content_gap` (keywords any competitor ranks for, you don't) joined with MarketMuse Topical Map for cluster-level gap detection. Beyond marketing-agent's "find some competitor keywords": this is the full pipeline — competitor selection → keyword universe diff → topical cluster coverage → prioritized opportunity backlog.

## Setup

```bash
# Ahrefs MCP — primary content gap source
open https://mcp.ahrefs.com/oauth?client=craftbot
export AHREFS_MCP_TOKEN="<oauth-token>"

# SEMrush API — alt; Keyword Gap report
export SEMRUSH_API_KEY="<from semrush.com/api>"

# MarketMuse — topical cluster gap
export MARKETMUSE_API_KEY="<from app.marketmuse.com/settings/api>"
```

Auth requirements:
- `AHREFS_MCP_TOKEN` — Lite plan minimum
- `SEMRUSH_API_KEY` — Business plan ($499/mo) for API
- `MARKETMUSE_API_KEY` — Standard plan ~$1500/mo

## Common recipes

### Recipe 1: Identify the right 3-5 competitors first
```bash
mcp tool ahrefs.site_explorer \
  --target "yourbrand.com" \
  --mode "competing_domains" \
  --limit 20 \
  --filter '{"common_keywords":{">=":50}}'
```
Returns domains ranking for the most overlapping keywords with you. Pick top 3-5 by `common_keywords × competitor_traffic` for analysis. Don't pick competitors with massively different DR (10× difference = unfair benchmark).

### Recipe 2: Ahrefs content_gap — primary tool
```bash
mcp tool ahrefs.content_gap \
  --your_domain "yourbrand.com" \
  --competitor_domains '["competitor1.com","competitor2.com","competitor3.com"]' \
  --intersect "any_competitor_ranks" \
  --min_volume 100 \
  --max_kd 50 \
  --max_position_competitor 20 \
  --limit 1000
```
`intersect=any_competitor_ranks` returns kws where ANY competitor ranks (broader); `all_competitors_rank` returns intersect (narrower, higher-confidence opportunity). Filter: KD ≤ 50, volume ≥ 100, competitor positions 1-20.

### Recipe 3: Score opportunities by traffic potential
```python
import pandas as pd

gaps = pd.read_json('content-gap.json')

# Estimated traffic potential per keyword
# Formula: volume × CTR(competitor_position) — Ahrefs uses similar
CTR_BY_POSITION = {1:0.30, 2:0.18, 3:0.11, 4:0.07, 5:0.05, 6:0.04, 7:0.03, 8:0.025, 9:0.02, 10:0.018}

def potential(row):
    pos = row['best_competitor_position']
    ctr = CTR_BY_POSITION.get(pos, 0.01)
    return row['volume'] * ctr

gaps['potential_traffic'] = gaps.apply(potential, axis=1)
gaps['ease_score'] = (50 - gaps['kd']) / 50  # 0-1, easier = higher
gaps['opportunity_score'] = gaps['potential_traffic'] * gaps['ease_score']

print(gaps.sort_values('opportunity_score', ascending=False).head(30))
```

### Recipe 4: Cluster gaps by parent_topic
```python
# Group keyword-level gaps into cluster-level gaps
import collections

cluster_gaps = collections.defaultdict(lambda: {'keywords': [], 'total_volume': 0, 'avg_kd': 0})

for _, gap in gaps.iterrows():
    pt = gap.get('parent_topic') or gap['keyword']  # fallback if no parent_topic
    cluster_gaps[pt]['keywords'].append(gap['keyword'])
    cluster_gaps[pt]['total_volume'] += gap['volume']
    cluster_gaps[pt]['avg_kd'] = (cluster_gaps[pt]['avg_kd'] * (len(cluster_gaps[pt]['keywords']) - 1) + gap['kd']) / len(cluster_gaps[pt]['keywords'])

# Top cluster opportunities
sorted_clusters = sorted(cluster_gaps.items(), key=lambda x: -x[1]['total_volume'])
print("Top cluster gaps:")
for pt, data in sorted_clusters[:10]:
    print(f"  {pt}: {len(data['keywords'])} kws, MSV {data['total_volume']:,}, avg KD {data['avg_kd']:.0f}")
```

### Recipe 5: MarketMuse topical gap (you have a cluster but it's weak)
```bash
# For an existing cluster, check what subtopics MarketMuse identifies that you don't cover
curl -X POST https://api.marketmuse.com/v3/topic-research \
  -H "Authorization: Bearer $MARKETMUSE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "term":"marketing automation",
    "language":"en",
    "country":"US"
  }'

# Returns subtopics with relevance_score + your current coverage (need integrated MM project)
```

### Recipe 6: SEMrush Keyword Gap (alt to Ahrefs)
```bash
curl "https://api.semrush.com/?type=domain_organic_kdi&key=$SEMRUSH_API_KEY&domain=yourbrand.com&database=us&display_limit=10000&export_columns=Ph,Po,Nq,Cp,Co,Nr,Td,Kd"
```
Returns your organic keywords; cross-compare with competitor exports to find gaps.

### Recipe 7: Filter content gap by business relevance
```python
# Not every gap matters — filter to keywords aligned with business
def is_business_relevant(keyword, target_personas):
    kw_lower = keyword.lower()
    # Examples of negative filters
    if 'jobs' in kw_lower or 'salary' in kw_lower: return False  # we don't hire for this topic
    if 'free' in kw_lower and 'free' not in target_personas: return False
    if 'login' in kw_lower or 'sign in' in kw_lower: return False  # branded/nav
    # Positive filters
    if any(persona_keyword in kw_lower for persona_keyword in target_personas):
        return True
    return True  # default include

target_personas = ['marketing manager','b2b','enterprise','crm','automation']
gaps['business_relevant'] = gaps['keyword'].apply(lambda k: is_business_relevant(k, target_personas))
relevant_gaps = gaps[gaps['business_relevant']]
```

### Recipe 8: Cross-check intent before commitment
```python
# Use SERP analysis to confirm intent matches your content format
from serp_skill import serp_analysis, classify_intent_from_serp

for _, gap in relevant_gaps.head(20).iterrows():
    serp = serp_analysis(gap['keyword'])
    intent = classify_intent_from_serp(serp)
    gap['confirmed_intent'] = intent

# Only act on gaps where confirmed_intent matches your business goal
# E.g., for B2B SaaS: target Informational + Commercial; skip Navigational + Transactional (paid handles)
```

### Recipe 9: Competitor-by-competitor breakdown
```python
# Per-competitor view: who owns what
breakdown = []
for _, gap in gaps.iterrows():
    for comp in competitors:
        pos = gap.get(f'position_{comp}')
        if pos and pos <= 20:
            breakdown.append({'keyword': gap['keyword'], 'competitor': comp, 'position': pos, 'volume': gap['volume']})

df = pd.DataFrame(breakdown)
print(df.groupby('competitor').agg({'keyword':'count','volume':'sum'}).rename(columns={'keyword':'gap_count','volume':'total_msv'}))
```

### Recipe 10: Prioritized content backlog output
```python
# Top-50 gaps → Notion editorial DB
top_gaps = relevant_gaps.sort_values('opportunity_score', ascending=False).head(50)

for _, gap in top_gaps.iterrows():
    notion.create_page(
        db_id=editorial_db,
        properties={
            'Title (working)': gap['keyword'],
            'Primary Keyword': gap['keyword'],
            'Volume': gap['volume'],
            'KD': gap['kd'],
            'Intent': gap.get('confirmed_intent', gap.get('intent','Mixed')),
            'parent_topic': gap.get('parent_topic',''),
            'Opportunity Score': gap['opportunity_score'],
            'Competitors Ranking': [c for c in competitors if gap.get(f'position_{c}',999) <= 20],
            'Status': 'Backlog',
            'Source': 'content-gap-analysis',
        }
    )
```

## Examples

### Example 1: Enterprise SaaS content gap audit
**Goal:** Identify top 50 content opportunities vs 3 main competitors.

**Steps:**
1. Recipe 1: confirm competitors (mix of similar DR, ≥50 common keywords).
2. Recipe 2: Ahrefs `content_gap` with `any_competitor_ranks`, KD ≤ 50, vol ≥ 100.
3. Recipe 3: score by potential traffic × ease.
4. Recipe 4: cluster by `parent_topic` to surface multi-keyword opportunities.
5. Recipe 7: filter to business-relevant keywords (negative-filter jobs/login/free).
6. Recipe 8: confirm intent via SERP analysis for top 30.
7. Recipe 10: write top 50 to Notion editorial DB.

**Result:** Production-ready content backlog with 50 prioritized opportunities; pair with `content-cluster-architecture-marketmuse` for briefs.

### Example 2: New cluster topical gap (you have 5 articles, MarketMuse says cluster needs 20)
**Goal:** Identify missing supporting articles within an existing cluster.

**Steps:**
1. Recipe 5: MarketMuse topic research on cluster pillar term.
2. List MarketMuse-recommended subtopics; cross with your existing URLs.
3. Identify the 10-15 subtopics you don't cover.
4. Score by MarketMuse `relevance_score × volume`.
5. Generate briefs via `content-cluster-architecture-marketmuse` skill.

**Result:** Complete cluster vs partial cluster — topical authority gain.

### Example 3: Competitor pivot analysis (competitor launched new product category)
**Goal:** Track competitor's new keyword acquisition over 90 days; react.

**Steps:**
1. Ahrefs `site_explorer mode=organic_keywords filter={first_seen:{after:'2026-03-01'}}` for competitor.
2. Identify new keyword themes (cluster by `parent_topic`).
3. Run Recipe 2 with the new themes as filters → confirm gaps for you.
4. Prioritize via Recipe 3 + 10.

**Result:** Defensive content backlog responding to competitor pivot.

## Edge cases / gotchas

- **Competitor selection bias** — picking competitors way larger than you = unwinnable gaps. Filter to ±2× DR range.
- **`any_competitor_ranks` vs `all_competitors_rank`** — `any` is broader (more opportunities, lower confidence); `all` is narrower (higher confidence). Default to `any` for ideation; `all` for "must-cover".
- **CTR-by-position estimates rough** — varies by SERP features. Featured-Snippet-present SERPs cut #1 CTR ~40%; PAA-heavy SERPs cut #1 ~20%.
- **Business-relevance manual filter required** — automated filters miss nuance. Have a human review top 50 before commit.
- **Intent classification via SERP > Ahrefs heuristic** — Ahrefs intent ~80% accurate; SERP-derived (Recipe 8) ~95%.
- **`parent_topic` null for new keywords** — cluster grouping (Recipe 4) falls back to keyword itself; clean up manually.
- **MarketMuse cluster gap requires integrated project** — without your domain configured in MarketMuse, Recipe 5 gives generic recommendations not your-coverage gap.
- **SEMrush API expensive at scale** — Business $499/mo entry. Use Ahrefs `content_gap` primary; SEMrush only if recipient already has plan.
- **Don't ignore long-tail at scale** — KD 50-70 with 50-volume keywords can collectively produce significant traffic if you target 50+ of them.
- **Refresh quarterly** — gaps shift as competitors publish + you cover. Re-run every 90 days.
- **Cross with content decay** — refreshing existing decay-affected pages (`content-decay-detection-refresh`) often higher ROI than new content; allocate effort accordingly.

## Sources

- [Ahrefs content gap tool](https://help.ahrefs.com/en/articles/13913559-getting-started-with-ahrefs-mcp)
- [Ahrefs blog — content gap analysis](https://ahrefs.com/blog/content-gap/)
- [SEMrush Keyword Gap report](https://www.semrush.com/kb/12-keyword-gap-comparison-report)
- [MarketMuse Topic Research API](https://www.marketmuse.com/api/)
- [Backlinko — CTR by position study](https://backlinko.com/google-ctr-stats)
- [Advanced Web Ranking — CTR study](https://www.advancedwebranking.com/ctrstudy/)
