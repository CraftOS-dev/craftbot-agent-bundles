<!--
Source: https://suganthan.com/blog/google-search-console-mcp-server/
Suganthan GSC MCP: npx suganthan-gsc-mcp v2.2.2 (April 2026, 20 tools)
-->
# Suganthan GSC Audit — SKILL

`suganthan-gsc-mcp` v2.2.2 (April 2026) is the SOTA Google Search Console wrapper with 20 tools — most importantly the `cannibalisation` tool (the only MCP that automates the mandatory pre-optimization audit), content decay analysis, and the Indexing API for `submit_url` / `submit_batch` / `submit_sitemap`.

## When to use this skill

- **Cannibalization audit** (MANDATORY before any SEO optimization — per role.md SEO playbook).
- **Content decay tracking** — find pages losing organic clicks month-over-month.
- **Indexing API** — push priority URLs / batches for re-crawl after launch / migration.
- **Query → page mapping** — which pages own which queries; foundation for content ownership.
- **Striking distance analysis** — queries ranking positions 4-20 with high CTR upside.
- **Coverage / crawl error reports** — index coverage status, sitemap submission errors.

**Do NOT use this skill when:**
- **Backlink data** — GSC's link reports are weak; use Ahrefs (`ahrefs-seo-mcp` skill).
- **Keyword volume / KD** — GSC reports actuals only, not opportunity volume; use Ahrefs.
- **Core Web Vitals lab data** — use `pagespeed-cwv-audit` skill.

## Setup

### Install

```bash
# v2.2.2 is the April 2026 release with all 20 tools
npx -y suganthan-gsc-mcp@2.2.2
```

### Auth — GSC OAuth

```bash
# One-time setup
# 1. Enable Search Console API + Indexing API in GCP console
# 2. Download OAuth client secret JSON from GCP
# 3. Run the auth flow once
suganthan-gsc-mcp auth --client-secret ./gcp-client-secret.json
# Saves token to ~/.suganthan-gsc/credentials.json

export GSC_PROPERTY="sc-domain:yourbrand.com"  # or https://yourbrand.com/
```

### 20 tools available (April 2026 release)

**Query analysis:**
- `search_analytics` — base query (date range, dimensions)
- `query_position_distribution` — histogram of query ranks
- `serp_features` — which SERP features (PAA, snippet, video) each query triggers
- `striking_distance` — queries in positions 4-20 (high CTR opportunity)
- `cannibalisation` — multi-page overlap analysis ★ THE MANDATORY AUDIT
- `branded_vs_non_branded` — separate organic streams
- `query_intent_inferred` — heuristic intent classification

**Page / content analysis:**
- `top_pages` — by clicks, impressions, CTR
- `content_decay` — pages losing clicks MoM ★
- `query_per_page` — top queries per landing page
- `page_ownership_map` — query → owner page recommendation

**Indexing:**
- `index_coverage` — coverage states (Valid, Excluded, Error, Warning)
- `crawl_errors` — types + counts
- `submit_url` — Indexing API single URL
- `submit_batch` — Indexing API up to 100 URLs
- `submit_sitemap` — sitemap submission
- `sitemap_status` — last fetch + index status

**Performance:**
- `core_web_vitals_summary` — CrUX data via GSC
- `mobile_usability` — mobile-friendly status
- `rich_results_status` — structured data eligibility

## Common recipes

### Recipe 1: Cannibalization audit (MANDATORY)

```bash
mcp tool suganthan-gsc.cannibalisation \
  --property "$GSC_PROPERTY" \
  --date_range "last_90_days" \
  --minImpressions 100 \
  --minOverlapQueries 3

# Output: list of {query, [pages], [positions], [clicks], conflict_severity}
```

Example output:

```json
[
  {
    "query": "marketing automation",
    "pages": [
      {"url":"/blog/marketing-automation","position":8.2,"clicks":124,"impressions":1500},
      {"url":"/product/marketing-automation","position":15.4,"clicks":18,"impressions":1200}
    ],
    "conflict_severity": "HIGH",
    "recommended_owner": "/blog/marketing-automation",
    "action": "consolidate"
  }
]
```

The agent then writes the resolution plan (per role.md cannibalization template):
- Designated owner per query
- Internal links from non-owner → owner
- Title / H1 deconfliction
- Canonical verification

### Recipe 2: Content decay analysis

```bash
mcp tool suganthan-gsc.content_decay \
  --property "$GSC_PROPERTY" \
  --comparePeriod "last_90_days_vs_previous_90" \
  --minPriorClicks 100 \
  --threshold -0.2

# Pages losing 20%+ clicks MoM
```

For each declining page:
1. Pull GSC `query_per_page` for the URL
2. Check for ranking drops (positions worse than previous period)
3. Cross with Ahrefs `referring_domains` — lost backlinks?
4. Refresh content if rankings dropped on commercial queries

### Recipe 3: Striking distance opportunity

```bash
mcp tool suganthan-gsc.striking_distance \
  --property "$GSC_PROPERTY" \
  --date_range "last_28_days" \
  --positionMin 4 \
  --positionMax 20 \
  --minImpressions 200 \
  --sort "impressions_desc" \
  --limit 100
```

For each: optimize on-page for that query (title, H1, internal links). Highest impact = position 4-10 with > 500 impressions.

### Recipe 4: Indexing API — push new content

```bash
# Single URL (e.g., new product page launch)
mcp tool suganthan-gsc.submit_url \
  --url "https://yourbrand.com/products/new-thing" \
  --type "URL_UPDATED"

# Batch up to 100 URLs (e.g., after sitemap regen)
mcp tool suganthan-gsc.submit_batch \
  --urls_file "@new-urls.txt" \
  --type "URL_UPDATED"

# Sitemap
mcp tool suganthan-gsc.submit_sitemap \
  --sitemap_url "https://yourbrand.com/sitemap.xml"
```

Note: Indexing API officially only for `JobPosting` and `BroadcastEvent` per Google's guidance — but in practice works for any URL update. Use sparingly to avoid quota burn.

### Recipe 5: Index coverage report

```bash
mcp tool suganthan-gsc.index_coverage \
  --property "$GSC_PROPERTY" \
  --groupBy "state"

# Returns counts per state: Valid, Excluded (canonical/redirect/noindex), Error (4xx/5xx)
```

Alert if:
- `Valid` < 80% of submitted sitemap URLs
- `Error` > 5% of crawled URLs

### Recipe 6: Query → page ownership map (foundation)

```bash
mcp tool suganthan-gsc.page_ownership_map \
  --property "$GSC_PROPERTY" \
  --date_range "last_90_days" \
  --minClicksThreshold 10

# Output: {query: owner_url} mapping for all queries with >= 10 clicks
```

Store as JSON, ref'd by cannibalization audit + content brief workflow (the brief's "Cannibalization check" field reads from this).

### Recipe 7: Branded vs non-branded organic split

```bash
mcp tool suganthan-gsc.branded_vs_non_branded \
  --property "$GSC_PROPERTY" \
  --brand_terms '["yourbrand","your brand","yourbrand.com"]' \
  --date_range "last_90_days"

# Output: {branded:{clicks,impressions,ctr,position}, non_branded:{...}}
```

Always report these separately — branded organic isn't a marketing win, it's customer service.

### Recipe 8: Rich results / schema status

```bash
mcp tool suganthan-gsc.rich_results_status \
  --property "$GSC_PROPERTY"

# Returns: per schema type {Article, Product, FAQ, HowTo, BreadcrumbList} → {valid, invalid, warnings}
```

Cross with `schema-org-structured-data` skill to fix invalid markup.

## Examples — full SEO audit workflow

```python
property = 'sc-domain:client.com'

# 1. Cannibalization (MANDATORY first)
cannib = gsc.cannibalisation(property=property, date_range='last_90_days', minImpressions=100)
# Write resolution plan to Notion + GitHub issue

# 2. Content decay
decay = gsc.content_decay(property=property, comparePeriod='last_90_days_vs_previous_90', threshold=-0.2)
# Refresh queue in Notion editorial calendar

# 3. Striking distance
striking = gsc.striking_distance(property=property, positionMin=4, positionMax=20, minImpressions=200)
# On-page optimization queue

# 4. Index coverage
coverage = gsc.index_coverage(property=property)
# Alert on Error/Excluded anomalies

# 5. Mobile usability
mobile = gsc.mobile_usability(property=property)
# CTO ticket if issues > 0

# 6. Rich results status
rich = gsc.rich_results_status(property=property)
# Schema fix queue

# 7. Branded vs non-branded
split = gsc.branded_vs_non_branded(property=property, brand_terms=['client','client.com'])
# Attribution report shows non-branded as marketing-attributable

# Aggregate all into a single audit doc
audit_report = {
    'cannibalization_conflicts': len([c for c in cannib if c['conflict_severity']=='HIGH']),
    'pages_decaying': len(decay),
    'striking_opportunities': len(striking),
    'index_errors': coverage['Error'],
    'mobile_issues': mobile['issues'],
    'schema_errors': sum(r['invalid'] for r in rich.values()),
    'non_branded_clicks': split['non_branded']['clicks'],
}
notion.create_page(db_id='seo-audits', properties=audit_report)
```

## Edge cases

### Property type
- `sc-domain:yourbrand.com` — Domain property (preferred, covers all subdomains + protocols)
- `https://www.yourbrand.com/` — URL-prefix property (single protocol + subdomain)

The agent should use Domain property when available.

### Data freshness
GSC data has 2-3 day lag. For week-over-week comparisons, use `last_7_days_excluding_recent_3`.

### Quota — Search Analytics API
- 1,200 queries/min default
- 50,000 queries/day for free tier
- Each `search_analytics` call = 1 query

For bulk audits, batch and cache.

### Quota — Indexing API
- 200 requests / day default
- Increase via Google Cloud quota page

Don't burn on infrequent pages — prioritize launches, migrations, time-sensitive content.

### Cannibalization severity logic
The `cannibalisation` tool's severity scoring:
- **HIGH**: > 3 queries overlap with both pages in top 20, neither dominates
- **MEDIUM**: > 1 query overlap, one page > 70% clicks
- **LOW**: 1 query overlap, one page dominates > 90%

Only HIGH demands action; MEDIUM = monitor; LOW = ignore.

### Branded search filtering
The `branded_vs_non_branded` tool uses string contains. Include:
- Brand name
- Brand domain
- Common misspellings (e.g., "yourbrand" + "ur brand")
- Brand + common product names

If brand has acronym overlap with common words, filter carefully.

### Indexing API "best practices"
- Use `URL_UPDATED` for new/updated pages
- Use `URL_DELETED` to request de-indexing (faster than waiting for Google to re-crawl 404)
- Don't spam — Google de-prioritizes accounts with low signal-to-noise

### Sitemap submission
Sitemaps should be:
- < 50MB / 50K URLs each
- Properly XML-formatted
- Linked from robots.txt
- Submitted via `submit_sitemap` after launch / weekly thereafter

### Mobile vs desktop split
Always pull `device='MOBILE'` and `device='DESKTOP'` separately for performance reports. Mobile typically lower position, higher impressions, lower CTR.

## Sources

- **Suganthan GSC MCP blog**: https://suganthan.com/blog/google-search-console-mcp-server/
- **GSC API reference**: https://developers.google.com/webmaster-tools/v1/api_reference_index
- **Indexing API**: https://developers.google.com/search/apis/indexing-api/v3/quickstart
- **Cannibalization methodology**: https://suganthan.com/blog/google-search-console-mcp-server/#cannibalisation
