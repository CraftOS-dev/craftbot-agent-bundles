<!--
Source: https://www.screamingfrog.co.uk/seo-spider/user-guide/general/#commandlineinterface
Source: https://sitebulb.com/hints/links/orphan-urls-from-other-sources/
Source: https://moz.com/learn/seo/anchor-text
Depth: orphan detection + hub-spoke verification + Anchor Diversification Pattern at URL-level
-->
# Internal Linking Strategy — Orphan + Hub-Spoke + Anchor Diversity

## When to use

Reach for this skill when the user asks for: "internal link audit", "find orphan pages", "hub-spoke check", "anchor diversity audit", "improve internal linking", "PageRank distribution", "site architecture review", "cluster cross-linking verification". This is the URL-level depth specialist — finds pages with zero inbound internal links (orphans), verifies every cluster page has ≥1 inbound from pillar (hub-spoke), checks anchor text distribution per URL (no >25% same anchor on inbound). Beyond marketing-agent's surface "use internal links": this enforces structural correctness.

## Setup

```bash
# Screaming Frog — primary inlinks export
screamingfrogseospider --help

# Sitebulb — hint-based orphan detection (alt)
sitebulb --help

# Python pandas for cross-join analysis
pip install pandas networkx
```

Auth requirements:
- SF license (free up to 500 URLs)
- Sitebulb license (Desktop $13.50+/mo or Server $35+/mo)

## Common recipes

### Recipe 1: SF crawl with inlinks + orphans export
```bash
screamingfrogseospider \
  --crawl https://example.com \
  --headless \
  --export-tabs "Internal:All,Internal:HTML,Internal:Inlinks,Internal:Outlinks" \
  --bulk-export "Links:All Inlinks,Links:All Outlinks,Links:All Anchor Text" \
  --output-folder ./internal-links-out \
  --timestamped-output

# For true orphan detection, SF needs sitemap + GSC sources:
# Config > Spider > Crawl > Check "XML Sitemaps" + "Crawl Linked XML Sitemaps"
# Config > API Access > Google Search Console (link account)
```
The "Inlinks" tab shows count of internal pages linking to each URL. The bulk export "All Inlinks" gives source URL + anchor text pairs.

### Recipe 2: Orphan page detection in pandas
```python
import pandas as pd

internal = pd.read_csv('./internal-links-out/internal_all.csv')

# Orphans = pages reachable via sitemap/GSC but with 0 internal inlinks
orphans = internal[(internal['Indexability'] == 'Indexable') &
                   (internal['Unique Inlinks'] == 0) &
                   (internal['Crawl Depth'] >= 0)]

print(f"Orphan pages: {len(orphans)}")
print(orphans[['Address','Source','Title 1']].to_string())
```

### Recipe 3: Hub-spoke verification (per cluster)
```python
# Cluster Notion DB: {pillar_url, supporting_urls[]}
clusters = [
    {'pillar': 'https://example.com/marketing-automation',
     'supporting': ['https://example.com/best-email-tools', 'https://example.com/crm-software', ...]},
    ...
]

inlinks = pd.read_csv('./internal-links-out/all_inlinks.csv')

for cluster in clusters:
    pillar = cluster['pillar']
    for supporting in cluster['supporting']:
        # Check: pillar → supporting?
        pillar_to_supp = inlinks[(inlinks['Source']==pillar) & (inlinks['Destination']==supporting)]
        # Check: supporting → pillar?
        supp_to_pillar = inlinks[(inlinks['Source']==supporting) & (inlinks['Destination']==pillar)]

        if pillar_to_supp.empty:
            print(f"MISSING: pillar→{supporting}")
        if supp_to_pillar.empty:
            print(f"MISSING: {supporting}→pillar")
```
Hub-spoke rule: pillar links to ALL supporting; every supporting links to pillar.

### Recipe 4: Anchor diversity per target URL
```python
# For each high-value URL: anchor distribution
inlinks = pd.read_csv('./internal-links-out/all_inlinks.csv')

for target in important_urls:
    target_inlinks = inlinks[inlinks['Destination']==target]
    if target_inlinks.empty: continue

    anchor_dist = target_inlinks['Anchor'].value_counts(normalize=True)
    print(f"\n{target}:")
    print(anchor_dist.head(10))

    # Flag if any single anchor >25%
    over = anchor_dist[anchor_dist > 0.25]
    if not over.empty:
        print(f"  OVER-OPTIMIZED: {over.to_dict()}")
```

### Recipe 5: Anchor classification + diversification recommendation
```python
def classify_anchor(anchor, target_keyword, brand_name):
    a = anchor.lower().strip()
    if a == target_keyword.lower(): return 'exact_match'
    if any(w in a for w in target_keyword.lower().split()): return 'partial_match'
    if a == brand_name.lower(): return 'branded'
    if a in ['click here','read more','learn more','here','this','more info']: return 'generic'
    if a.startswith('http'): return 'naked_url'
    if a in ['image alt']: return 'image'
    return 'other'

# Healthy distribution for internal links (industry heuristic)
HEALTHY = {
    'exact_match': (0.10, 0.20),
    'partial_match': (0.25, 0.40),
    'branded': (0.15, 0.25),
    'generic': (0.10, 0.20),
    'naked_url': (0.05, 0.15),
    'image': (0.05, 0.15),
}

inlinks['anchor_type'] = inlinks['Anchor'].apply(lambda a: classify_anchor(a, 'marketing automation', 'Example'))
dist = inlinks['anchor_type'].value_counts(normalize=True).to_dict()
print(dist)
for t, (lo, hi) in HEALTHY.items():
    actual = dist.get(t, 0)
    if actual < lo: print(f"{t}: LOW ({actual:.2%} < {lo:.0%}) — add more")
    elif actual > hi: print(f"{t}: HIGH ({actual:.2%} > {hi:.0%}) — diversify")
```

### Recipe 6: PageRank-style internal link weight (networkx)
```python
import networkx as nx

# Build directed graph
G = nx.DiGraph()
for _, row in inlinks.iterrows():
    G.add_edge(row['Source'], row['Destination'])

# Compute PageRank
pr = nx.pagerank(G, alpha=0.85)

# Top + bottom — surface pages over/under-linked relative to importance
top = sorted(pr.items(), key=lambda x: -x[1])[:20]
bottom = sorted(pr.items(), key=lambda x: x[1])[:20]

# Cross with GSC clicks via suganthan-gsc to find:
# (a) high PR + low clicks = orphaned high-equity pages
# (b) low PR + high clicks = under-supported winners (add internal links!)
```

### Recipe 7: Find anchor-text spam (over-optimization)
```python
# Sites with >50% exact-match anchors on internal links = penalty risk
for target in inlinks['Destination'].unique():
    target_inlinks = inlinks[inlinks['Destination']==target]
    if len(target_inlinks) < 5: continue  # ignore low-inbound URLs
    exact_match_pct = (target_inlinks['anchor_type'] == 'exact_match').mean()
    if exact_match_pct > 0.5:
        print(f"{target}: {exact_match_pct:.0%} exact-match — over-optimized")
```

### Recipe 8: Sitebulb orphan + hint export
```bash
sitebulb crawl \
  --url https://example.com \
  --project "internal-link-audit" \
  --enable-javascript true \
  --include-xml-sitemap true \
  --include-gsc true \
  --hints "internal-links" \
  --export-format csv \
  --output ./sitebulb-out
```
Sitebulb's "Internal Backlinks" hint module gives orphan + low-link-count surfaces ranked by impact.

### Recipe 9: Build internal link recommendation list (output for content team)
```python
# For each orphan or under-linked page, recommend N pages to add links FROM
recommendations = []

for orphan in orphans['Address']:
    # Find topically-similar pages via shared parent_topic or h1 keywords
    # (simplified — production uses embedding similarity)
    candidates = find_similar_pages(orphan, k=3)
    for source in candidates:
        recommendations.append({
            'add_link_from': source,
            'add_link_to': orphan,
            'suggested_anchor': pick_anchor(orphan, anchor_type='partial_match'),
            'reason': 'orphan' if orphan in orphans else 'under-linked',
        })

# Output to Notion or CSV for content team execution
pd.DataFrame(recommendations).to_csv('internal-link-recommendations.csv', index=False)
```

### Recipe 10: Cluster cross-linking pattern enforcement
```
Within-cluster: hub-spoke (pillar ←→ supporting). Mandatory.
Cross-cluster: only when topically adjacent. Pillar A → pillar B if cluster A is prerequisite for cluster B.
Supporting → supporting: occasional, when content naturally references. Never every-to-every.
```

## Examples

### Example 1: Initial internal link audit for 25K URL site
**Goal:** Find orphans, verify hub-spoke, score anchor diversity.

**Steps:**
1. Recipe 1: SF crawl with inlinks + sitemap + GSC connected → exports.
2. Recipe 2: pandas orphan detection → list of orphan pages.
3. Recipe 6: networkx PageRank → cross with GSC clicks for high-equity + low-clicks pairs.
4. Recipe 3: hub-spoke verification per cluster (cluster DB from `parent-topic-clustering-ahrefs-semantic-intent`).
5. Recipe 4 + 5: anchor diversity check on top-20 URLs.
6. Recipe 9: generate recommendation CSV.
7. Deliver via `docx` audit report.

**Result:** Audit report + actionable link recommendations.

### Example 2: Reclaim under-linked traffic winner
**Goal:** Page has 50K impressions but only 2 internal inlinks — boost equity via internal links.

**Steps:**
1. Identify via Recipe 6 (low PR + high GSC clicks).
2. Find 5-10 topically related pages with high authority (pillar pages, sidebar nav, top-traffic pages).
3. Add internal links with diversified anchors (Recipe 5 distribution).
4. Track via Ahrefs `internal_links(target=<url>)` weekly → confirm new inbound + position lift.

**Result:** Position improvement on the boosted page in 2-6 weeks.

## Edge cases / gotchas

- **SF "Inlinks" count is page-level, not link-count** — 5 links from one source page = 1 unique inlink. Use Bulk Export "All Inlinks" for true link-count.
- **Sitemap inclusion required for orphan detection** — without sitemap connected to SF, you only find pages reachable from start URL.
- **GSC connection adds discovered URLs** — pages getting clicks but not in sitemap will surface in SF's "Orphan URLs" tab when GSC API connected.
- **Anchor classification heuristic** — `partial_match` detection requires the target keyword; without it, you can't classify properly. Run per-URL with its primary keyword.
- **25% anchor concentration threshold is heuristic** — not a Google-stated rule. Industry consensus from Moz / Ahrefs / Backlinko.
- **PageRank computation slow on >100K-node graphs** — use `nx.pagerank` `tol=1e-4` to speed up; or use Botify's pre-computed `internal_pagerank` field.
- **Recipe 9 "find_similar_pages"** — production version uses sentence-embedding cosine similarity (via huggingface-mcp). Stub above uses keyword overlap.
- **Sitewide nav links inflate inlinks** — header/footer nav links count as inlinks everywhere. Filter source pages to "in-body" only for accurate analysis. SF distinguishes via "Link Position" column.
- **Image-link anchors** — image alt text becomes the anchor text. Optimize image alt = optimize anchor. Don't double-count if image alt = adjacent text anchor.
- **Cross-domain internal links (subdomains)** — `blog.example.com → example.com` counts as external in SF unless configured. Adjust crawl settings if using subdomains.

## Sources

- [Screaming Frog inlinks export guide](https://www.screamingfrog.co.uk/seo-spider/user-guide/general/#commandlineinterface)
- [Sitebulb orphan URL hint](https://sitebulb.com/hints/links/orphan-urls-from-other-sources/)
- [Moz — anchor text optimization](https://moz.com/learn/seo/anchor-text)
- [Ahrefs — internal linking guide](https://ahrefs.com/blog/internal-links-for-seo/)
- [Cyrus Shepard — over-optimization penalty](https://zyppy.com/seo/internal-links/)
- [Brian Dean — hub and spoke model](https://backlinko.com/hub/seo/topic-clusters)
- [Google Search Central — make your links crawlable](https://developers.google.com/search/docs/crawling-indexing/links-crawlable)
