<!--
Source: https://genesysgrowth.com/blog/surfer-seo-vs-clearscope-vs-marketmuse
MarketMuse Topical Map API
-->
# MarketMuse Topic Clustering — SKILL

MarketMuse's Topical Map API generates pillar pages + supporting topic clusters with built-in authority scores, intent classification, and content briefs. SOTA for content strategy when paid-API budget is available. Surfer SEO Content Planner is the close alternative.

## When to use this skill

- **Pillar + cluster architecture** for a new topic area or content vertical.
- **Topical authority gap analysis** — where the brand has authority overlap with audience demand.
- **Content brief generation** at scale — MarketMuse outputs per-page briefs with target word count, related topics, questions to answer.
- **Pillar page optimization** — check coverage score against ideal topic set.
- **Cluster maintenance** — quarterly check that cluster still reflects current SERP.

**Do NOT use this skill when:**
- **Single-keyword research** — use `ahrefs-seo-mcp` skill.
- **No paid API budget** — fall back to Claude + Ahrefs `parent_topic` field.
- **Pure content brief** with no clustering — use internal role.md template.

## Setup

### Auth

```bash
export MARKETMUSE_API_KEY="<key>"
# Standard plan minimum required for Topical Map API
```

### Endpoints

- `https://api.marketmuse.com/v3/topic-research` — topic deep dive
- `https://api.marketmuse.com/v3/topic-navigator` — pillar + cluster suggestion
- `https://api.marketmuse.com/v3/content-brief` — per-page brief generation
- `https://api.marketmuse.com/v3/page-analyzer` — score existing content vs ideal

## Common recipes

### Recipe 1: Generate pillar + cluster from seed topic

```bash
curl -X POST https://api.marketmuse.com/v3/topic-navigator \
  -H "X-Api-Key: $MARKETMUSE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "marketing automation",
    "language": "en-US",
    "country": "US",
    "max_pages": 20,
    "intent_mix": ["informational","commercial"]
  }'
```

Returns:

```json
{
  "pillar": {
    "topic": "marketing automation",
    "search_volume": 22000,
    "difficulty": 78,
    "intent": "Commercial",
    "authority_score": 64,
    "ideal_word_count": 4500,
    "related_topics": [...]
  },
  "supporting": [
    {
      "topic": "marketing automation for small business",
      "volume": 1800,
      "difficulty": 42,
      "intent": "Commercial",
      "ideal_word_count": 2200
    },
    {
      "topic": "marketing automation vs crm",
      "volume": 950,
      "difficulty": 35,
      "intent": "Informational",
      "ideal_word_count": 1800
    },
    ...
  ]
}
```

### Recipe 2: Per-page content brief

```bash
curl -X POST https://api.marketmuse.com/v3/content-brief \
  -H "X-Api-Key: $MARKETMUSE_API_KEY" \
  -d '{
    "topic": "marketing automation for small business",
    "target_url": "/blog/marketing-automation-small-business"
  }'
```

Returns:

```json
{
  "topic": "...",
  "target_word_count": 2200,
  "key_topics_to_cover": [
    {"topic":"workflow automation","ideal_mentions":5},
    {"topic":"email triggers","ideal_mentions":4},
    {"topic":"lead scoring","ideal_mentions":3}
  ],
  "questions_to_answer": [
    "What is marketing automation?",
    "How does marketing automation work for small business?",
    "What's the difference between marketing automation and CRM?"
  ],
  "outline_suggestion": [
    {"h2":"What is marketing automation?","h3":["Definition","Examples"]},
    {"h2":"Why small businesses need it","h3":["Time savings","Personalization"]}
  ],
  "related_questions_from_paa": [...]
}
```

Hand this brief to Claude for generation, run Vale pass, publish.

### Recipe 3: Topical authority gap analysis

```bash
curl -X POST https://api.marketmuse.com/v3/topic-research \
  -H "X-Api-Key: $MARKETMUSE_API_KEY" \
  -d '{
    "domain": "yourbrand.com",
    "topic": "marketing automation",
    "include_competitors": true
  }'
```

Returns:

```json
{
  "your_authority": 47,
  "competitors": [
    {"domain":"hubspot.com","authority":92},
    {"domain":"klaviyo.com","authority":78},
    {"domain":"mailchimp.com","authority":71}
  ],
  "your_coverage_pages": 12,
  "competitor_avg_coverage": 47,
  "missing_topics": [
    "drip campaigns",
    "lead nurturing best practices",
    "marketing automation roi"
  ],
  "weak_topics": [
    {"topic":"segmentation strategy","your_score":12,"ideal":80}
  ]
}
```

### Recipe 4: Page analyzer (existing content scoring)

```bash
curl -X POST https://api.marketmuse.com/v3/page-analyzer \
  -H "X-Api-Key: $MARKETMUSE_API_KEY" \
  -d '{
    "url": "https://yourbrand.com/blog/marketing-automation-guide",
    "target_topic": "marketing automation"
  }'
```

Returns:

```json
{
  "current_score": 58,
  "ideal_score": 80,
  "word_count": 1800,
  "ideal_word_count": 4500,
  "missing_topics": [...],
  "underused_topics": [...],
  "recommendations": [
    "Add 1700 more words covering: lead scoring, workflow triggers, attribution",
    "Restructure H2/H3 to match top SERP outline"
  ]
}
```

### Recipe 5: Full cluster export to Notion

```python
import requests, json

# Step 1: pillar + supporting
nav = requests.post('https://api.marketmuse.com/v3/topic-navigator', json={'topic':'marketing automation','max_pages':20}).json()

# Step 2: brief for each
all_pages = [nav['pillar']] + nav['supporting']
notion_db_id = '<cluster-db>'
for page in all_pages:
    brief = requests.post('https://api.marketmuse.com/v3/content-brief', json={'topic':page['topic']}).json()
    notion.create_page(db_id=notion_db_id, properties={
        'Topic': page['topic'],
        'Type': 'Pillar' if page == nav['pillar'] else 'Supporting',
        'Volume': page['volume'],
        'KD': page['difficulty'],
        'Intent': page['intent'],
        'Target Word Count': brief['target_word_count'],
        'Status': 'Backlog',
        'Brief': json.dumps(brief),
    })
```

### Recipe 6: Quarterly cluster refresh

```bash
# Pull current cluster
curl -X POST https://api.marketmuse.com/v3/topic-navigator -d '{"topic":"<pillar>"}' > new_cluster.json

# Diff against stored Notion DB
python3 - <<'EOF'
import json
new = json.load(open('new_cluster.json'))
existing = notion.query(cluster_db, filter={'Pillar':'<pillar>'})

new_topics = {p['topic'] for p in new['supporting']}
existing_topics = {p['Topic'] for p in existing}

# Topics to add
to_add = new_topics - existing_topics
# Topics removed (potentially obsolete)
to_review = existing_topics - new_topics

for t in to_add: notion.create_page(... topic=t, status='Backlog')
for t in to_review: notion.update_page(t, status='Review for sunset')
EOF
```

## Examples — content strategy for new vertical

```yaml
new_vertical: SaaS Marketing Automation
total_content_pieces: 20
target_publishing_pace: 2/week (10 weeks total)

step_1_topic_navigator:
  seed: "saas marketing automation"
  output: 1 pillar + 19 supporting
  total_volume: ~120k/mo combined
  avg_difficulty: 38

step_2_briefs:
  per_piece: 1500-4500 words depending on intent
  format: blog post, comparison, listicle, definitive guide
  briefs_generated: 20

step_3_editorial:
  pillar_first: weeks 1-2 (pillar = 4500 words)
  supporting_in_priority_order: weeks 3-12

step_4_internal_linking:
  - all supporting → pillar (canonical hub)
  - pillar → supporting (table of contents)
  - sibling supporting → relevant supporting (semantic clusters)

step_5_promotion:
  - email newsletter weekly (klaviyo-email-lifecycle)
  - linkedin executive amplification (linkedin-marketing-api)
  - paid amplification (meta-ads-official-mcp) on top 3 performers
```

## Edge cases

### MarketMuse plan tiers
- **Free**: 5 queries/mo — useless for production
- **Standard ($149/mo)**: 100 queries/mo, Topical Map + Brief APIs
- **Team ($399/mo)**: 1k queries/mo, multi-user
- **Premium**: custom, deep integrations

For agent automation, Standard minimum.

### Query consumption
- Topic Navigator: 1 query
- Content Brief: 1 query
- Page Analyzer: 1 query
- Topic Research: 2 queries (deeper)

A 20-page cluster = ~25 queries.

### Country / language
MarketMuse supports EN (US/UK/CA/AU), ES, FR, DE, PT, IT. For other languages, use Ahrefs + Claude clustering as fallback.

### Authority score interpretation
- 0-30: low — needs significant content investment
- 30-60: building — keep publishing
- 60+: strong — defend and refresh existing

Your score reflects topical-keyword coverage relative to top-ranking competitors, not link authority.

### "Ideal word count" reality
MarketMuse averages top-ranking competitors. Take as guideline, not law — sometimes a tight 1200-word answer outranks a bloated 4500-word competitor (esp. for transactional intent).

### Intent mix — defaults
By default Topic Navigator includes mixed intent. For commercial-focused vertical (B2B SaaS), filter to `commercial + informational` only — skip transactional (those are landing pages, not blog) and navigational (brand pages).

### Cluster sizing
- Tight cluster (5-10 supporting): faster to publish, easier to maintain, lower total reach
- Wide cluster (20-30 supporting): comprehensive authority, slower to ramp, harder to maintain

Default to 15-20 for new verticals.

### Surfer SEO alternative
Surfer Content Planner is the closest competitor:

```bash
# Surfer API
curl https://api.surferseo.com/v2/content_planner \
  -H "Authorization: Bearer $SURFER_API_KEY" \
  -d '{"keyword":"marketing automation","location":"United States","language":"en-us"}'
```

Differences:
- MarketMuse: stronger on topical authority metrics
- Surfer: stronger on per-page on-page scoring + SERP analyzer

If both available, use MarketMuse for strategy + Surfer for per-page optimization.

### Free fallback (no paid tool)
Claude + Ahrefs `parent_topic` field can approximate clustering:

```python
seed_kws = ahrefs.keywords_explorer(keyword='marketing automation', limit=500)
clusters = {}
for kw in seed_kws:
    pt = kw['parent_topic']
    clusters.setdefault(pt, []).append(kw)

# Now manually pick pillar topic + assign supporting from each cluster
```

Quality: 70% of MarketMuse — acceptable for budget-constrained teams.

## Sources

- **MarketMuse vs Surfer vs Clearscope comparison**: https://genesysgrowth.com/blog/surfer-seo-vs-clearscope-vs-marketmuse
- **MarketMuse API docs**: https://developer.marketmuse.com/
- **Topical authority methodology**: https://blog.marketmuse.com/topical-authority/
- **Surfer SEO Content Planner**: https://surferseo.com/content-planner/
- **Cluster best practices**: https://moz.com/blog/topic-clusters
