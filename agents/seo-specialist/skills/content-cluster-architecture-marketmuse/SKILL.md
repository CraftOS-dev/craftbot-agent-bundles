<!--
Source: https://genesysgrowth.com/blog/surfer-seo-vs-clearscope-vs-marketmuse
Source: https://www.marketmuse.com/api/
Source: https://surferseo.com/blog/content-planner/
Source: https://www.frase.io/blog/topic-model/
Depth: full topical-map architecture with pillar + supporting briefs from MarketMuse / Surfer / Frase
-->
# Content Cluster Architecture — MarketMuse / Surfer / Frase

## When to use

Reach for this skill when the user asks for: "build topical map", "topical authority plan", "content brief from MarketMuse", "Surfer content planner cluster", "Frase topic model", "pillar + supporting cluster with briefs", "what should I write next in this topic". This is the SOTA tool-driven cluster architecture path — where `parent-topic-clustering-ahrefs-semantic-intent` clusters keywords by SERP signal, this skill goes deeper: it generates per-page content briefs (topic-model term coverage, question coverage, word count targets, structure outline). Pick ONE vendor per engagement: MarketMuse (premium ~$1500/mo), Surfer ($89+/mo), or Frase ($45+/mo).

## Setup

```bash
# MarketMuse — REST API, Standard plan minimum
export MARKETMUSE_API_KEY="<from app.marketmuse.com/settings/api>"

# Surfer SEO — REST API, Essential plan minimum ($89/mo) but Advanced ($129/mo) needed for API
export SURFER_API_KEY="<from surferseo.com/app/settings>"

# Frase — REST API, Solo plan minimum ($45/mo)
export FRASE_API_KEY="<from app.frase.io/account>"

# All three plans require a credit card; recipient picks ONE
```

Auth / pricing:
- `MARKETMUSE_API_KEY` — Standard plan ~$1500/mo; best for enterprise, full topical authority scoring
- `SURFER_API_KEY` — Advanced $129/mo for API; mid-tier, AI-Outline + GEO scoring included
- `FRASE_API_KEY` — Solo $45/mo for API; cheapest, includes AEO/topic-model scoring

## Common recipes

### Recipe 1: MarketMuse — generate topic map for a seed topic
```bash
curl -X POST https://api.marketmuse.com/v3/topic-navigator \
  -H "Authorization: Bearer $MARKETMUSE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "term":"marketing automation",
    "language":"en",
    "country":"US"
  }'
```
Returns the topic's "Topical Map": pillar topic + ~30-50 related subtopics with `topic_authority_score` (Personalized DA), `volume`, `competition`, `relevance_score`, and recommended URL slug per subtopic.

### Recipe 2: MarketMuse — per-URL content brief
```bash
curl -X POST https://api.marketmuse.com/v3/content-brief \
  -H "Authorization: Bearer $MARKETMUSE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "term":"marketing automation tools",
    "url":"https://example.com/best-marketing-automation-tools",
    "competitors":["competitor1.com","competitor2.com"],
    "language":"en"
  }'
```
Returns: target Content Score, recommended word count (typically 1500-3500), 40-80 related terms with target mention counts, related questions (PAA + LLM-generated), recommended headings outline, internal link suggestions.

### Recipe 3: Surfer Content Planner — cluster generation
```bash
curl -X POST https://api.surferseo.com/v1/content-planner \
  -H "Authorization: Bearer $SURFER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "seed_keyword":"marketing automation",
    "country_code":"us",
    "topical_map_size":"large"
  }'
```
`large` = ~50 cluster keywords; `small` = ~15. Returns hierarchical pillar → supporting structure with per-keyword volume + difficulty.

### Recipe 4: Surfer — per-page Content Editor brief
```bash
curl -X POST https://api.surferseo.com/v1/content-editor \
  -H "Authorization: Bearer $SURFER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords":["marketing automation tools"],
    "secondary_keywords":["automation software","email automation","crm automation"],
    "location_code":2840,
    "competitors":["competitor1.com/page-a","competitor2.com/page-b"]
  }'
```
Returns: NLP-based term frequency targets (terms/sub-terms with use counts), header outline, word count target. Content Score updates as content drafted.

### Recipe 5: Surfer GEO score (AEO content scoring)
```bash
curl -X POST https://api.surferseo.com/v1/geo-score \
  -H "Authorization: Bearer $SURFER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content":"<full markdown>",
    "target_query":"marketing automation tools",
    "competitors":["competitor1.com/page-a"]
  }'
```
Returns AI-surface readiness score (entity density, structured Q&A presence, source citation count, direct-answer block detection). See `aeo-content-optimization-entity-rich` skill for full AEO play.

### Recipe 6: Frase Topic Model
```bash
curl -X POST https://api.frase.io/v1/topic-model \
  -H "X-Api-Key: $FRASE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query":"marketing automation",
    "lang":"en",
    "country":"us"
  }'
```
Returns top-20 SERP URLs + extracted topics + related questions + recommended outline. Cheaper than MarketMuse, faster than Surfer (~3-5s vs 30-60s).

### Recipe 7: Frase Content Brief
```bash
curl -X POST https://api.frase.io/v1/content-brief \
  -H "X-Api-Key: $FRASE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query":"marketing automation tools",
    "lang":"en"
  }'
```

### Recipe 8: Cluster maturity scoring via topical authority
```python
# MarketMuse personalized DA per topic — track quarter-over-quarter
import requests

topics = ['marketing automation','crm','sales enablement']
for topic in topics:
    r = requests.post(
        'https://api.marketmuse.com/v3/topic-research',
        headers={'Authorization': f'Bearer {MARKETMUSE_API_KEY}'},
        json={'term': topic}
    )
    data = r.json()
    print(f"{topic}: PDA={data['personalized_authority']}, content_score={data['site_content_score']}")

# Track over time → topical authority growth
```

### Recipe 9: Multi-tool consensus brief (when high-stakes)
```python
# Run all 3 tools for the same target keyword, merge for high-confidence brief
target_kw = "marketing automation tools"

mm_brief = call_marketmuse_brief(target_kw)
surfer_brief = call_surfer_brief(target_kw)
frase_brief = call_frase_brief(target_kw)

# Consensus headings — heading appears in ≥2 briefs
consensus_h2 = set(mm_brief['headings']) & set(surfer_brief['headings']) | \
               set(surfer_brief['headings']) & set(frase_brief['headings']) | \
               set(mm_brief['headings']) & set(frase_brief['headings'])

# Consensus terms (target word frequencies)
consensus_terms = {t: max(mm_brief['terms'].get(t,0), surfer_brief['terms'].get(t,0), frase_brief['terms'].get(t,0))
                   for t in set(mm_brief['terms']) | set(surfer_brief['terms']) | set(frase_brief['terms'])}

# Word count target — median of three
wc_target = sorted([mm_brief['wc'], surfer_brief['wc'], frase_brief['wc']])[1]
```

### Recipe 10: Hand off to technical-writer
```python
# Notion brief schema for handoff to technical-writer agent
brief = {
    'Target URL Slug': 'best-marketing-automation-tools',
    'Primary Keyword': 'marketing automation tools',
    'Secondary Keywords': ['automation software','best marketing automation'],
    'Word Count Target': 2800,
    'Content Score Target': 75,
    'Outline (H2s)': ['What is marketing automation?', 'How to choose tools', 'Top 10 tools 2026', ...],
    'Term Targets': {'marketing automation': 12, 'CRM': 8, 'email': 15, ...},
    'PAA / Questions to Answer': ['What is marketing automation?', 'How much does it cost?', ...],
    'Internal Links': ['/marketing-automation-pillar', '/crm-comparison'],
    'External Citations': ['https://www.gartner.com/...', 'https://hbr.org/...'],
    'Schema Type': 'Article + FAQPage',
    'Brief Source': 'MarketMuse + Surfer consensus',
}
notion.create_page(db_id=editorial_db, properties=brief)
```

## Examples

### Example 1: Full cluster + briefs for new content pillar
**Goal:** Topic = "B2B marketing automation". Need pillar + 12 supporting page briefs.

**Steps:**
1. Recipe 1: MarketMuse topic map for "B2B marketing automation" → 30-50 subtopic candidates.
2. Filter to top 12 by `topic_authority_score × volume / competition`.
3. Recipe 2: per-URL content brief for pillar + 12 supporting.
4. Designate pillar = highest authority + head-term (e.g., "b2b marketing automation guide").
5. Recipe 10: write briefs to Notion editorial DB.
6. Hand off to `technical-writer` agent for content production.

**Result:** 13 production-ready briefs (pillar + 12 supporting); content team can start without further research.

### Example 2: Compete with an authority site on tight budget
**Goal:** SMB client, $200/mo cap. Use Frase instead of MarketMuse.

**Steps:**
1. Recipe 6: Frase topic model for seed keyword.
2. Manually cluster Frase topics into pillar + 5-8 supporting (no AI-driven cluster like MarketMuse).
3. Recipe 7: Frase brief per page.
4. Cross-check with Ahrefs `parent_topic` clustering (`parent-topic-clustering-ahrefs-semantic-intent` skill) for SERP signal validation.
5. Recipe 10: brief handoff.

**Result:** Reasonable cluster + briefs at 1/30th the MarketMuse cost.

### Example 3: Surfer GEO + content score loop for AEO push
**Goal:** Rewrite existing article to also win AI-surface citations.

**Steps:**
1. Recipe 4: Surfer Content Editor for the existing target keyword.
2. Recipe 5: Surfer GEO score on current content draft.
3. Iterate: rewrite intro with direct-answer block, add entity-rich markup, add FAQPage schema (see `aeo-content-optimization-entity-rich` + `schema-org-deep-jsonld-eeat` skills).
4. Re-run Recipe 5 → confirm GEO score >75.
5. Submit reindex via `suganthan-gsc-cannibalization-decay-indexing` → `submit_url`.

**Result:** Article scoring for both organic + AEO.

## Edge cases / gotchas

- **MarketMuse cost vs ROI** — at $1500/mo, justify only for clusters with ≥$50K projected annual organic revenue. Sub that, use Surfer or Frase.
- **Surfer Content Score gameable** — purely NLP frequency matching; can over-stuff terms. Don't optimize past Content Score 75 — diminishing return + readability risk.
- **Frase topic model 20-URL ceiling** — only top 20 SERP URLs analyzed. For deep niches Frase may miss long-tail signal MarketMuse captures.
- **Three-tool consensus diminishing returns** — Recipe 9 expensive (3× API cost + 3× analysis time). Reserve for $20K+ articles.
- **No tool replaces editorial judgment** — briefs are inputs, not orders. Override term targets if they hurt readability.
- **Content Score / GEO score not in Google's algo** — these are proxies. Final test = SERP performance + AEO citation share after publish.
- **MarketMuse "Personalized DA"** is Moz Domain Authority + their personalization layer — not Google PageRank or Ahrefs DR. Don't compare directly across tools.
- **Surfer API rate limit** — 100 req/min on Advanced plan; 500 req/min on Enterprise.
- **Frase API rate limit** — 60 req/min; bulk endpoints not exposed.
- **All three depend on SERP scraping** — outage at SerpAPI / DataForSEO (their backends) can break briefs. Have manual outline ready as fallback.

## Sources

- [MarketMuse API documentation](https://www.marketmuse.com/api/)
- [Surfer SEO API docs](https://docs.surferseo.com/)
- [Surfer SEO Content Planner](https://surferseo.com/blog/content-planner/)
- [Frase API documentation](https://docs.frase.io/api)
- [Frase Topic Model](https://www.frase.io/blog/topic-model/)
- [GenesysGrowth — Surfer vs Clearscope vs MarketMuse comparison](https://genesysgrowth.com/blog/surfer-seo-vs-clearscope-vs-marketmuse)
- [Surfer GEO optimization](https://surferseo.com/blog/geo-optimization/)
- [Ahrefs blog — topical authority](https://ahrefs.com/blog/topical-authority/)
