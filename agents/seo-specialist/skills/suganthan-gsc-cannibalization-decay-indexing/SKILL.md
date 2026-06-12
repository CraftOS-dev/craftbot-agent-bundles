<!--
Source: https://suganthan.com/blog/google-search-console-mcp-server/
Source: https://developers.google.com/webmaster-tools/v1/searchanalytics/query
Source: https://developers.google.com/search/apis/indexing-api/v3/quickstart
Depth: cannibalization audit (mandatory pre-optimization) + decay + Indexing API depth
-->
# Suganthan GSC MCP — Cannibalization, Decay, Indexing

## When to use

This is the **mandatory first skill** for any optimization engagement. Reach for it when the user asks for: "cannibalization audit", "find pages competing", "what page should rank for X", "content decay analysis", "striking distance opportunities", "submit URLs to Google index", "indexing API", "Bing IndexNow via Suganthan", "GSC bulk export", "index coverage". The `cannibalisation` tool **BLOCKS** every other optimization recommendation — refuse to optimize titles/content/links until you've run it. Deeper than marketing-agent's GSC pull: this skill handles multi-property + multi-cluster batch mode + 90-day decay detection + Indexing API batch submission.

## Setup

```bash
# One-time install via npx (v2.2.2 = current stable as of June 2026)
npx suganthan-gsc-mcp@2.2.2 --help

# Or pin in claude-config.json MCP server list:
# "suganthan-gsc": {"command":"npx","args":["suganthan-gsc-mcp@2.2.2"],"env":{"GSC_OAUTH_CLIENT_ID":"...","GSC_OAUTH_CLIENT_SECRET":"..."}}

# First-run OAuth: opens browser
npx suganthan-gsc-mcp@2.2.2 auth
# Approve scopes: webmasters.readonly, indexing
```

Auth / API requirements:
- `GSC_OAUTH_CLIENT_ID` + `GSC_OAUTH_CLIENT_SECRET` — Google Cloud Console OAuth 2.0 Web app; enable **Search Console API** + **Indexing API** at https://console.cloud.google.com/apis/library
- GSC property must be verified (DNS / HTML file / Search Console tag)
- Indexing API quota: 200 URLs/day default; apply for higher at https://support.google.com/webmasters/contact/indexing-api-quota
- Free — both APIs no-cost

## Common recipes

### Recipe 1: Cannibalization audit (the mandatory pre-optimization step)
```bash
# Via Suganthan GSC MCP
mcp tool suganthan-gsc.cannibalisation \
  --site_url "sc-domain:example.com" \
  --days 90 \
  --min_clicks 5 \
  --min_impressions 100 \
  --output_format json
```
Returns a map of `{query: [{page, position, clicks, impressions, ctr}]}` where ≥2 pages rank for the same query. For each: assign **owner** (highest clicks page), then apply resolution plan (consolidate / redirect / rewrite / internal-link — see `role.md` "Cannibalization at scale playbook"). NEVER skip this step before optimizing anything.

### Recipe 2: Content decay detection (90-day downward trend)
```bash
mcp tool suganthan-gsc.content_decay \
  --site_url "sc-domain:example.com" \
  --window 90 \
  --decay_threshold -0.2 \
  --min_baseline_clicks 50
```
`decay_threshold=-0.2` means flag URLs with ≥20% click drop over the trailing 90 days. `min_baseline_clicks` filters out low-value noise. Output rows sorted by absolute click loss × original click magnitude.

### Recipe 3: Striking-distance opportunities (positions 4-20)
```bash
mcp tool suganthan-gsc.striking_distance \
  --site_url "sc-domain:example.com" \
  --min_position 4 \
  --max_position 20 \
  --min_impressions 200 \
  --days 28
```
Returns query+page rows where you rank in positions 4-20 (i.e., page 1 bottom or page 2 top — high-leverage with small CTR push). Prioritize by impressions × inverse position.

### Recipe 4: Submit URLs to Google Indexing API
```bash
# Single URL
mcp tool suganthan-gsc.submit_url \
  --url "https://example.com/new-post" \
  --type "URL_UPDATED"

# Batch submission (uses Indexing API batch endpoint — 200/day per property)
mcp tool suganthan-gsc.submit_batch \
  --urls_file "@/tmp/urls-to-index.txt" \
  --type "URL_UPDATED"
# urls-to-index.txt: one URL per line
```
`URL_UPDATED` for new or modified; `URL_DELETED` for removed (returns 410). Per Google docs the API is officially for Job/Livestream schema only — but Suganthan's wrapper handles general content via the same endpoint and Google accepts it in practice.

### Recipe 5: Submit sitemap
```bash
mcp tool suganthan-gsc.submit_sitemap \
  --site_url "sc-domain:example.com" \
  --sitemap_url "https://example.com/sitemap.xml"
```

### Recipe 6: Index coverage report
```bash
mcp tool suganthan-gsc.index_coverage \
  --site_url "sc-domain:example.com" \
  --status "valid,error,excluded,valid_with_warnings"
```
Returns counts + URL examples per status. Track week-over-week to detect indexing regressions during migrations.

### Recipe 7: Page ownership map (output for optimization team)
```bash
mcp tool suganthan-gsc.page_ownership_map \
  --site_url "sc-domain:example.com" \
  --days 90 \
  --top_query_per_page 5
```
Returns `{page: [{query, position, clicks}]}` — useful as a "this page already owns these queries" reference before recommending title/H1 changes.

### Recipe 8: SERP feature appearance tracking
```bash
mcp tool suganthan-gsc.serp_features \
  --site_url "sc-domain:example.com" \
  --features "featured_snippet,paa,image_pack,video_carousel,local_pack,knowledge_panel" \
  --days 28
```
For each page, returns which SERP features it appears in. Pair with `serp-analysis-intent-snippet-paa` skill for competitor feature ownership.

### Recipe 9: Raw GSC search analytics query (when MCP tools don't expose what you need)
```bash
curl -X POST "https://www.googleapis.com/webmasters/v3/sites/sc-domain%3Aexample.com/searchAnalytics/query" \
  -H "Authorization: Bearer $GSC_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "startDate":"2026-03-01",
    "endDate":"2026-06-01",
    "dimensions":["query","page"],
    "rowLimit":25000,
    "dataState":"final"
  }'
```
Direct GSC API for max flexibility. `rowLimit` max 25000/request; paginate with `startRow` for full export.

### Recipe 10: Bulk export to Notion via notion-mcp
```python
# After Recipe 1 cannibalization output
import json
cannibalization = json.load(open('cannibalization.json'))

for query, pages in cannibalization.items():
    if len(pages) < 2: continue
    owner = max(pages, key=lambda p: p['clicks'])
    losers = [p for p in pages if p['page'] != owner['page']]

    notion.create_page(
        db_id=cannibalization_db,
        properties={
            'Query': query,
            'Owner Page': owner['page'],
            'Owner Clicks': owner['clicks'],
            'Losers': [l['page'] for l in losers],
            'Action': 'TBD',  # Consolidate / Redirect / Rewrite / Internal-Link
            'Status': 'Triage',
        }
    )
```

## Examples

### Example 1: Pre-engagement cannibalization audit for new client
**Goal:** Map all cannibalization conflicts before any optimization recommendation.

**Steps:**
1. Verify GSC property: `mcp tool suganthan-gsc.list_sites` — confirm `sc-domain:client.com` appears.
2. Run cannibalization: Recipe 1 with `days=90, min_clicks=5`.
3. For each conflict (output rows): apply ownership rules from `role.md` "Cannibalization at scale playbook → Ownership assignment".
4. Output Notion DB via Recipe 10 with action column per row.
5. Block all other optimization work until Notion shows every row has assigned `Action`.

**Result:** Ownership map + resolution plan. Deliverable: shared Notion DB + 1-page summary.

### Example 2: Programmatic SEO launch indexing rollout
**Goal:** Submit 8000 new programmatic pages to Google Index over 40 days (200/day quota).

**Steps:**
1. Split URL list into 40 chunks of 200: `split -l 200 urls.txt urls-chunk-`.
2. Daily cron: `mcp tool suganthan-gsc.submit_batch --urls_file @urls-chunk-aa --type URL_UPDATED`.
3. Mirror to IndexNow for Bing/Yandex (see `indexing-api-indexnow-google-bing` skill).
4. Day 7+14+30: Recipe 6 to confirm index coverage growth.
5. Day 30: cross-check sitemap-vs-indexed ratio; if <70%, escalate to `frontend-engineer` for canonical / robots issues.

**Result:** All 8000 URLs indexed within 45-60 days (vs 90-180 days passive crawl).

### Example 3: Quarterly content-decay refresh batch
**Goal:** Identify top-20 decaying URLs and refresh them.

**Steps:**
1. Recipe 2 with `decay_threshold=-0.3, min_baseline_clicks=100, window=90`.
2. For each: pull current SERP via DataForSEO (`serp-analysis-intent-snippet-paa` skill) → identify what top-3 competitors do that you don't.
3. Hand off refresh briefs to `technical-writer` agent.
4. After publish: Recipe 4 `submit_url --type URL_UPDATED` for each refreshed URL.
5. 14-day post-refresh: re-run Recipe 2 → confirm decay reversed.

**Result:** Recovered clicks on declining content. Cycle quarterly.

## Edge cases / gotchas

- **GSC property type matters** — use `sc-domain:example.com` for domain properties; `https://example.com/` for URL-prefix properties. Mismatch returns empty data.
- **Indexing API 200/day quota is per property** — multi-property sites stack quotas. Apply for 1000/day at https://support.google.com/webmasters/contact/indexing-api-quota with use-case justification.
- **`URL_UPDATED` vs `URL_DELETED`** — `URL_DELETED` sends a 410 signal. Don't use for unpublished pages still living at URL.
- **Cannibalization false positives** — generic queries like "login" may legitimately surface multiple pages. Manually filter the cannibalization output before action.
- **OAuth token expiry** — Suganthan MCP refreshes automatically if refresh token persisted. If you re-clone the auth cache, redo `auth` step.
- **GSC dataState="final" lag** — final data lags 2-3 days. For real-time monitoring use `dataState="all"` (includes fresh-but-imprecise data).
- **`searchAnalytics/query` 25K row limit** — paginate via `startRow`. For 100K+ row pulls use Looker Studio / BigQuery export (set up GSC → BigQuery bulk export in Search Console settings).
- **Indexing API non-job/livestream content** — Google's docs say job/livestream only, but the API accepts general URLs in practice (and Suganthan + the SEO community use it that way). Risk-averse recipients should use sitemap + crawl request via UI instead.
- **Sitemap submission via API doesn't replace robots.txt sitemap reference** — both should exist.
- **`min_baseline_clicks` in `content_decay`** — set ≥50 to avoid noise from low-traffic URLs.

## Sources

- [Suganthan GSC MCP v2.2.2 documentation](https://suganthan.com/blog/google-search-console-mcp-server/)
- [Google Search Console API reference](https://developers.google.com/webmaster-tools/v1/api_reference_index)
- [Google Search Analytics query API](https://developers.google.com/webmaster-tools/v1/searchanalytics/query)
- [Google Indexing API quickstart](https://developers.google.com/search/apis/indexing-api/v3/quickstart)
- [Google Indexing API quota request form](https://support.google.com/webmasters/contact/indexing-api-quota)
- [Google Search Central — request indexing](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl)
