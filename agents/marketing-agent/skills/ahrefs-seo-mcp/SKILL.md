<!--
Source: https://help.ahrefs.com/en/articles/13913559-getting-started-with-ahrefs-mcp
Ahrefs remote MCP: mcp.ahrefs.com (OAuth, Lite plan and up)
-->
# Ahrefs SEO MCP — SKILL

Ahrefs remote MCP at `mcp.ahrefs.com` is the SOTA path for keyword research, backlinks, intent classification, and broken-link reclamation. Lite plan and above. OAuth-based, no API key juggling.

## When to use this skill

- **Keyword research with intent** — Ahrefs Keywords Explorer with built-in intent classification (informational / commercial / transactional / navigational).
- **Backlink analysis + monitoring** — referring domains, new/lost backlinks, broken backlinks.
- **Broken-link reclamation** — surfaces dead inbound links for outreach.
- **Unlinked brand mention** — Ahrefs Content Explorer with mentions filter.
- **Competitor gap analysis** — keywords competitors rank for that you don't.
- **Site audit triggers** — schedule audits, fetch latest issues.

**Do NOT use this skill when:**
- **GSC-specific data** (impressions, CTR, position by query) → use `suganthan-gsc-audit` skill.
- **Core Web Vitals lab data** → use `pagespeed-cwv-audit` skill.
- **Cannibalization audit** → use Suganthan GSC `cannibalisation` tool (Ahrefs doesn't have this).
- **Free / cheap alternative** → DataForSEO at $0.0006/SERP (use `cli-anything` curl).

## Setup

### Auth — OAuth at mcp.ahrefs.com

```bash
# Browser flow
open https://mcp.ahrefs.com/oauth?client=craftbot
# Grant scopes: read:keywords, read:backlinks, read:content, write:projects

export AHREFS_MCP_TOKEN="<oauth-token>"
```

### MCP server connection

```json
// claude-config.json
{
  "ahrefs": {
    "transport": "https",
    "url": "https://mcp.ahrefs.com/v1",
    "auth": {"type":"bearer","token":"${AHREFS_MCP_TOKEN}"}
  }
}
```

### Tools available

- `keywords_explorer` — search volume, KD, intent, SERP features, parent topic
- `site_explorer` — domain backlinks, referring domains, organic keywords
- `content_explorer` — content + mentions search
- `backlinks_new_lost` — daily delta for monitoring
- `referring_domains` — DR/UR weighted
- `broken_backlinks` — for reclamation outreach
- `keyword_difficulty_bulk` — bulk KD for 100s of keywords
- `content_gap` — keywords competitors rank, you don't
- `rank_tracker` — historical position tracking
- `site_audit_trigger` / `site_audit_results`

## Common recipes

### Recipe 1: Keyword research with intent (single seed)

```bash
mcp tool ahrefs.keywords_explorer \
  --keyword "marketing automation" \
  --country "US" \
  --limit 100 \
  --include_metrics '["volume","difficulty","intent","cpc","parent_topic","serp_features"]'
```

Output:

```json
{
  "keywords": [
    {
      "keyword": "marketing automation",
      "volume": 22000,
      "difficulty": 78,
      "intent": "Commercial",  // <-- THIS is the intent classification
      "cpc": 14.20,
      "parent_topic": "marketing automation",
      "serp_features": ["FeaturedSnippet","PAA","TopStories"],
      "global_volume": 53000
    },
    ...
  ]
}
```

### Recipe 2: Intent-mapped content plan (info / commercial / transactional / nav)

```python
# Pseudo-flow
keywords = ahrefs.keywords_explorer(keyword=seed, country='US', limit=200)
intent_buckets = {
    'Informational': [],   # → Blog posts, guides, how-tos
    'Commercial': [],      # → Comparisons, reviews, alternatives
    'Transactional': [],   # → Landing pages, product pages
    'Navigational': [],    # → Brand pages (skip for SEO)
}
for kw in keywords:
    intent_buckets[kw['intent']].append(kw)

# Map to content brief format
for intent, kws in intent_buckets.items():
    if intent == 'Navigational': continue
    for kw in kws[:20]:  # top 20 per bucket
        notion.create_page(
            db_id=editorial_db,
            properties={
                'Keyword': kw['keyword'],
                'Intent': intent,
                'Volume': kw['volume'],
                'KD': kw['difficulty'],
                'Format': format_for_intent(intent),
                'Status': 'Backlog',
            }
        )
```

### Recipe 3: Competitor gap analysis

```bash
mcp tool ahrefs.content_gap \
  --your_domain "yourbrand.com" \
  --competitor_domains '["competitor1.com","competitor2.com","competitor3.com"]' \
  --intersect "any_competitor_ranks" \
  --min_volume 100 \
  --max_kd 50 \
  --limit 200
```

Returns keywords any competitor ranks top 20 for, that you don't rank for at all. Filter to KD < 50 + Volume > 100 = winnable opportunities.

### Recipe 4: Broken-link reclamation

```bash
# Find inbound links pointing to 404s on our domain
mcp tool ahrefs.broken_backlinks \
  --target "yourbrand.com" \
  --mode "domain" \
  --limit 500

# Output: list of [source_url, target_dead_url, anchor_text, dr]
# For each: identify closest live URL on your site → outreach via gmail-mcp
```

Outreach script template:

```text
Subject: Broken link on {source_url}

Hi {author},

I was reading {source_url} and noticed the link to {dead_url} returns a 404.
We've published an updated piece at {live_url} that covers the same topic.

Would you be open to updating the link? Happy to send anything else useful.

Thanks,
{name}
```

### Recipe 5: Unlinked brand mention conversion

```bash
# Find pages mentioning our brand without linking
mcp tool ahrefs.content_explorer \
  --query "\"yourbrand\"" \
  --filter '{"links_to":"-yourbrand.com","language":"en","dr":">30"}' \
  --limit 200 \
  --sort "dr_desc"
```

For each: confirm the mention via Firecrawl scrape, then `gmail-mcp` outreach.

### Recipe 6: Backlink monitoring (daily delta)

```bash
mcp tool ahrefs.backlinks_new_lost \
  --target "yourbrand.com" \
  --date "yesterday" \
  --include '["new","lost"]'
```

Run daily; lost links from DR > 50 referrers → priority reclamation queue.

### Recipe 7: Keyword difficulty bulk score (100s)

```bash
mcp tool ahrefs.keyword_difficulty_bulk \
  --keywords_file "@keywords.txt" \
  --country "US"
# Returns one row per keyword: volume, KD, intent
```

### Recipe 8: Rank tracking (set-up)

```bash
mcp tool ahrefs.rank_tracker \
  --action "add_keywords" \
  --project_id "<proj>" \
  --keywords '["primary kw","supporting kw1",...]' \
  --frequency "weekly" \
  --countries '["US","UK","CA"]'

# Pull historical positions
mcp tool ahrefs.rank_tracker \
  --action "get_history" \
  --project_id "<proj>" \
  --date_range "last_90_days"
```

## Examples — full SEO opportunity audit

```python
# Run end-to-end for a new client engagement
domain = 'client.com'
competitors = ['comp1.com','comp2.com','comp3.com']

# 1. Site Explorer overview
overview = ahrefs.site_explorer(target=domain, metrics=['dr','ur','organic_keywords','organic_traffic','referring_domains'])

# 2. Content gap (top 200 winnable)
gaps = ahrefs.content_gap(
    your_domain=domain,
    competitor_domains=competitors,
    intersect='any_competitor_ranks',
    min_volume=100, max_kd=50, limit=200
)

# 3. Striking distance (currently positions 4-20)
striking = ahrefs.site_explorer(
    target=domain,
    mode='organic_keywords',
    filter={'position':{'between':[4,20]}, 'volume':{'>=':100}},
    limit=200
)

# 4. Broken backlinks
broken = ahrefs.broken_backlinks(target=domain, mode='domain', limit=500)

# 5. Unlinked mentions
mentions = ahrefs.content_explorer(
    query=f'"{client_brand}"',
    filter={'links_to':f'-{domain}','dr':'>30'},
    limit=200
)

# 6. Build prioritized opportunity Notion DB
notion.create_db(name='SEO Opportunities — ' + domain, rows=[
    *[{'type':'content_gap', ...} for kw in gaps],
    *[{'type':'striking_distance', ...} for kw in striking],
    *[{'type':'broken_link', ...} for link in broken],
    *[{'type':'unlinked_mention', ...} for m in mentions],
])
```

## Edge cases

### Ahrefs plan limits
| Plan | Monthly Cost | API Credits | Keyword Lookups |
|---|---|---|---|
| Lite | $129 | 500 | 750/day |
| Standard | $249 | 1500 | 4000/day |
| Advanced | $449 | 5000 | 15,000/day |

For agent automation, Standard minimum recommended. Each `keywords_explorer` call ~= 1-5 credits depending on rows returned.

### Rate limits
- 100 req/min per token
- Bulk endpoints (`keyword_difficulty_bulk`) consume fewer credits per keyword
- Cache responses for 24h — Ahrefs data refreshes weekly so daily caching is safe

### Intent classification accuracy
Ahrefs intent is heuristic — ~80% accuracy. For high-stakes decisions (paid landing page mapping), the agent should cross-check via SERP feature analysis: if SERP shows shopping ads + product listings = transactional; if PAA dominates = informational.

### "Volume" vs "Global volume"
- `volume` = country-specific (e.g., US)
- `global_volume` = sum across all tracked countries
- For multi-region brands, use `global_volume` for total opportunity sizing

### Difficulty (KD) caveat
KD 0-30 = winnable for new sites; 30-60 = need DR > 40; 60+ = need DR > 60 and topical authority. The agent's "low-hanging fruit" filter: KD < 30 AND volume > 100.

### When Ahrefs data conflicts with GSC
GSC is ground truth for impressions / clicks. Ahrefs estimates volume; GSC reports actual impressions for the queries Google attributes. Always validate top opportunities against GSC via `suganthan-gsc-audit` skill.

### Cheap alternative: DataForSEO
If Ahrefs paid tier isn't available:

```bash
curl -X POST https://api.dataforseo.com/v3/keywords_data/google/search_volume/live \
  -H "Authorization: Basic <base64(login:pass)>" \
  -d '[{"keywords":["marketing automation"],"location_code":2840,"language_code":"en"}]'
# ~$0.0006 per keyword
```

DataForSEO doesn't auto-classify intent — let Claude classify from SERP features.

## Sources

- **Ahrefs MCP getting started**: https://help.ahrefs.com/en/articles/13913559-getting-started-with-ahrefs-mcp
- **Ahrefs API reference**: https://docs.ahrefs.com/
- **Intent classification methodology**: https://ahrefs.com/blog/search-intent/
- **DataForSEO fallback**: https://github.com/Skobyn/dataforseo-mcp-server
