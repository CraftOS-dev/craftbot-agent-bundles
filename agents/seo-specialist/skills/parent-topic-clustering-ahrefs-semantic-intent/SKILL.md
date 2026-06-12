<!--
Source: https://ahrefs.com/blog/parent-topic/
Source: https://help.ahrefs.com/en/articles/13913559-getting-started-with-ahrefs-mcp
Depth: parent_topic clustering + semantic intent layering + Anchor Diversification Pattern
-->
# Parent-Topic Clustering — Ahrefs Semantic Intent + SERP Overlap

## When to use

Reach for this skill when the user asks for: "topic cluster", "parent_topic grouping", "should these merge or stay separate", "semantic cluster from keywords", "SERP overlap analysis", "consolidate or split URLs", "anchor diversification pattern". This is the SOTA cluster-architecture methodology — uses Ahrefs `parent_topic` as the first-pass semantic group, then SERP overlap % for borderline-pair resolution. Deeper than marketing-agent's "ahrefs keyword research" surface coverage: you decide WHICH keywords become one canonical pillar vs distinct cluster, AND you enforce Anchor Diversification Pattern on internal links between cluster members.

## Setup

```bash
# Ahrefs MCP — same auth as ahrefs-deep-keyword-cluster-research skill
open https://mcp.ahrefs.com/oauth?client=craftbot
export AHREFS_MCP_TOKEN="<oauth-token>"

# Python for cluster analysis
pip install pandas numpy
```

Auth requirements:
- `AHREFS_MCP_TOKEN` — see `ahrefs-deep-keyword-cluster-research` skill setup
- Ahrefs Lite ($129/mo) minimum for `parent_topic` field access; Standard ($249/mo) recommended

## Common recipes

### Recipe 1: First-pass cluster from `parent_topic` field
```bash
mcp tool ahrefs.keywords_explorer \
  --keyword "<seed term>" \
  --country "US" \
  --limit 500 \
  --include_metrics '["volume","difficulty","intent","parent_topic","serp_features"]' \
  --output_format json > kws.json
```

```python
import json, pandas as pd

kws = pd.DataFrame(json.load(open('kws.json'))['keywords'])

# Group by parent_topic
clusters = kws.groupby('parent_topic').agg({
    'keyword': lambda x: list(x),
    'volume': 'sum',
    'difficulty': 'mean',
    'intent': lambda x: x.value_counts().to_dict()
}).reset_index()

clusters = clusters.sort_values('volume', ascending=False)
print(clusters.head(20))
```
Output: ~10-30 clusters per 500 keywords. Each `parent_topic` row is a candidate pillar.

### Recipe 2: Borderline-pair SERP overlap resolution
```bash
# Two `parent_topic` groups feel like they should merge?
mcp tool ahrefs.serp_comparison \
  --keywords '["best running shoes","running shoe reviews"]' \
  --country "US" \
  --include_metrics '["overlap_count","overlap_percent","common_urls"]'
```
Decision rule:
- **≥40% overlap** → consolidate into one pillar (the higher-volume kw wins the URL)
- **<40% overlap** → keep separate (different intents despite semantic similarity)
- **20-40% overlap** → manual review (gray zone)

### Recipe 3: Intent layering across parent_topic clusters
```python
# For each cluster: classify dominant intent
def dominant_intent(kw_list):
    intents = kws[kws['keyword'].isin(kw_list)]['intent'].value_counts()
    if intents.iloc[0] / intents.sum() > 0.6:
        return intents.index[0]  # >60% one intent
    return 'Mixed'

clusters['intent_class'] = clusters['keyword'].apply(dominant_intent)
print(clusters[['parent_topic','intent_class','volume']].head(20))
```
Map intent → content format:
- Informational → guide / blog post / how-to
- Commercial → comparison / review / "best X" listicle
- Transactional → landing page / product page / pricing page
- Navigational → brand page (skip for SEO)

### Recipe 4: Pillar URL designation (one per cluster)
```python
# Pillar = highest-volume head term in the cluster
def pick_pillar(cluster_kws):
    candidates = kws[kws['keyword'].isin(cluster_kws)]
    # Prefer head term (fewer words) with high volume
    candidates = candidates.assign(word_count=candidates['keyword'].str.split().str.len())
    candidates = candidates.sort_values(['word_count','volume'], ascending=[True, False])
    return candidates.iloc[0]['keyword']

clusters['pillar_keyword'] = clusters['keyword'].apply(pick_pillar)
```

### Recipe 5: Supporting URL designation (each long-tail kw → its own URL)
```python
# Each non-pillar kw with volume ≥ threshold gets a supporting URL
threshold_volume = 200

for _, cluster in clusters.iterrows():
    pillar = cluster['pillar_keyword']
    supporting = [k for k in cluster['keyword']
                  if k != pillar and kws.set_index('keyword').loc[k,'volume'] >= threshold_volume]
    print(f"Pillar: {pillar} | Supporting: {supporting}")
```

### Recipe 6: SERP feature opportunity per cluster
```python
# Identify clusters with Featured Snippet / PAA / Video opportunities
import collections

cluster_features = {}
for _, cluster in clusters.iterrows():
    feature_counter = collections.Counter()
    for kw in cluster['keyword']:
        features = kws[kws['keyword']==kw]['serp_features'].iloc[0]
        if isinstance(features, list):
            feature_counter.update(features)
    cluster_features[cluster['parent_topic']] = dict(feature_counter)

# Sort by Featured Snippet opportunity
fs_opps = [(t, f.get('FeaturedSnippet',0)) for t, f in cluster_features.items()]
fs_opps.sort(key=lambda x: -x[1])
print("Top Featured Snippet clusters:", fs_opps[:10])
```

### Recipe 7: Anchor Diversification Pattern (internal links between cluster members)
```python
# Healthy anchor distribution for a pillar URL receiving internal links from supporting pages
# Rule: no single anchor text >25% of inbound internal links to one URL

import pandas as pd

# Pull internal inbound from Ahrefs
inbound = ahrefs.internal_links(target='example.com/pillar', mode='inbound', limit=1000)
df = pd.DataFrame(inbound)

# Anchor distribution
anchor_dist = df['anchor_text'].value_counts(normalize=True)
print(anchor_dist.head(10))

# Categorize anchors
def classify_anchor(a):
    if a == 'marketing automation': return 'exact_match'
    if 'marketing' in a.lower(): return 'partial_match'
    if a.lower() in ['example','example.com']: return 'branded'
    if a.lower() in ['click here','read more','learn more','here']: return 'generic'
    if a.startswith('http'): return 'naked_url'
    return 'other'

df['anchor_type'] = df['anchor_text'].apply(classify_anchor)
print(df['anchor_type'].value_counts(normalize=True))

# Healthy distribution:
# exact_match: 10-20%
# partial_match: 25-40%
# branded: 15-25%
# generic: 10-20%
# naked_url: 5-15%
# other: 5-15%
```

### Recipe 8: Sibling-cluster cross-linking strategy
```
Pattern: pillar A ←→ pillar B (cross-link only when topically adjacent, not identical)
Supporting A1 → pillar A (always, hub-spoke)
Supporting A1 → supporting B1 (occasional, when content references each other naturally)

Avoid: every supporting page linking to every other supporting page (anchor-text spam pattern)
```

### Recipe 9: Notion DB schema for cluster architecture deliverable
```python
# Schema (matches role.md "Cluster architecture deliverable")
schema = {
    'Pillar URL': 'url',
    'Supporting URLs': 'multi_url',
    'Primary Keyword': 'text',
    'Supporting Keywords': 'multi_text',
    'parent_topic': 'text',
    'Intent': 'select',  # Informational / Commercial / Transactional / Navigational
    'Total MSV': 'number',  # head + sum of supporting
    'KD': 'number',  # head term
    'SERP Features': 'multi_select',
    'Current Position': 'number',
    'Status': 'select',  # published / in-progress / planned / declining
    'Notes': 'rich_text',
}

# Create via notion-mcp
notion.create_database(name='Cluster Architecture', schema=schema)
```

### Recipe 10: Cluster maturity score (track progress quarter-over-quarter)
```python
# Score each cluster 0-5
def cluster_maturity(cluster_id):
    score = 0
    if pillar_published(cluster_id): score += 1
    if all_supporting_published(cluster_id): score += 1
    if internal_links_hub_spoke_complete(cluster_id): score += 1
    if any_top_3_ranking(cluster_id): score += 1
    if pillar_owns_featured_snippet(cluster_id): score += 1
    return score
```

## Examples

### Example 1: Cluster a 200-keyword seed into 8-12 clusters
**Goal:** Take a 200-keyword export and produce a cluster Notion DB with pillar + supporting per cluster.

**Steps:**
1. Recipe 1 with seed term → 200-500 kws with `parent_topic` field.
2. Recipe 1 Python groupby → ~15-25 first-pass clusters.
3. For each cluster pair with volume ≥ 1000 each, Recipe 2: SERP comparison.
4. Apply 40% rule → merge pairs that exceed; keep separate otherwise.
5. Recipe 3: classify dominant intent per cluster.
6. Recipe 4 + 5: designate pillar + supporting URLs.
7. Recipe 9: write to Notion DB via `notion-mcp`.

**Result:** 8-12 production-ready clusters with pillar URL + 5-15 supporting URLs each.

### Example 2: Borderline pair resolution
**Goal:** User asks "should `running shoes review` and `best running shoes` be one page or two?"

**Steps:**
1. Recipe 2: SERP comparison for the two keywords.
2. Output: `overlap_percent=62%` → ≥40% → consolidate.
3. Higher-volume kw (`best running shoes` 18K vs `running shoes review` 4K) wins the URL.
4. Add internal link from the loser-kw URL to the winner-kw URL (anchor: branded or partial-match).
5. If a page already exists for the loser-kw: redirect 301 (per `role.md` "Resolution plan templates → Consolidate").

**Result:** One canonical pillar URL; 301 from the consolidated URL.

### Example 3: Anchor Diversification audit on existing cluster
**Goal:** Cluster pillar is over-optimized — too many exact-match internal anchors.

**Steps:**
1. Recipe 7: pull inbound internal anchors via Ahrefs.
2. Classify by anchor type.
3. Identify exact_match count >25% → over-optimized.
4. Generate rewrite plan: change top 10 exact-match anchors to mix of partial / branded / generic per healthy distribution.
5. Hand off to `frontend-engineer` or content team for HTML updates.

**Result:** Healthier anchor distribution; reduces over-optimization risk.

## Edge cases / gotchas

- **`parent_topic` null for new keywords** — Ahrefs needs ~30 days of SERP data to assign `parent_topic`. New trending kws may show null.
- **Volume-based pillar pick can fail** — sometimes the highest-volume kw is too head-term (e.g., "shoes") to be the pillar focus. Manual override when needed.
- **SERP overlap of 40% threshold is a heuristic** — for B2B / niche topics use 30%; for broad consumer topics use 50%.
- **Intent "Mixed" cluster** — split into sub-clusters by intent or pick the dominant intent + accept the long tail.
- **Anchor diversification has no Google-officially-stated threshold** — 25% rule is industry heuristic from Cyrus Shepard / Brian Dean. Use as guidance, not hard rule.
- **Internal anchor distribution differs from external** — focus this skill on INTERNAL anchors. External backlink anchor diversification is the linking site's responsibility.
- **`parent_topic` doesn't equal cluster pillar** — `parent_topic` is Ahrefs' semantic group label, not necessarily the URL keyword. Use it for grouping, then pick pillar URL separately.
- **Cluster size cap** — pillars supporting >25 long-tail URLs become unwieldy; split into sub-clusters.
- **Cross-language cluster mapping** — `parent_topic` is country-scoped. For hreflang, re-cluster per country (overlap is typically high but not 100%).

## Sources

- [Ahrefs parent_topic methodology](https://ahrefs.com/blog/parent-topic/)
- [Ahrefs MCP API reference](https://help.ahrefs.com/en/articles/13913559-getting-started-with-ahrefs-mcp)
- [Ahrefs search intent classification](https://ahrefs.com/blog/search-intent/)
- [Cyrus Shepard — anchor text optimization](https://moz.com/learn/seo/anchor-text)
- [Brian Dean — topic clusters](https://backlinko.com/hub/seo/topic-clusters)
- [Ahrefs blog — topic clusters](https://ahrefs.com/blog/topic-clusters/)
