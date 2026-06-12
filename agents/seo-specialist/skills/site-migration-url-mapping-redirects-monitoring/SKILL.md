<!--
Source: https://www.searchenginejournal.com/seo-website-migration-checklist/
Source: https://developers.google.com/search/docs/crawling-indexing/site-move-no-url-changes
Source: https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes
Depth: pre-migration baseline → URL map → 301 → 30-day post-migration monitoring
-->
# Site Migration — URL Mapping + Redirects + Monitoring

## When to use

Reach for this skill when the user asks for: "site migration", "domain migration", "URL restructure", "301 redirect plan", "platform migration", "SEO migration checklist", "post-migration monitoring", "redirect mapping", "migration impact analysis". This is the depth specialist for the full migration playbook — pre-migration baseline, 1:1 URL mapping for top traffic, 301-only redirect plan, post-migration daily monitoring for 30 days. Cannibalization audit BEFORE migration kicks off.

## Setup

```bash
# Screaming Frog for pre + post crawl
screamingfrogseospider --help

# Ahrefs MCP for top_pages baseline
export AHREFS_MCP_TOKEN="<oauth-token>"

# Suganthan GSC MCP for index_coverage + Indexing API
npx suganthan-gsc-mcp@2.2.2 --help

# PostHog/GA4 for organic traffic monitoring
export POSTHOG_API_KEY="<from posthog.com/project/settings>"
```

Auth requirements:
- SF license
- `AHREFS_MCP_TOKEN` for top_pages export
- GSC OAuth for `index_coverage` + Indexing API
- Analytics access (PostHog / GA4) for traffic monitoring

## Common recipes

### Recipe 1: Pre-migration baseline crawl
```bash
# Full SF crawl of OLD site
screamingfrogseospider \
  --crawl https://old-site.com \
  --headless \
  --save-crawl \
  --export-tabs "Internal:All,Internal:HTML,Page Titles:All,Meta Description:All,H1:All,Canonicals:All,Response Codes:All,Hreflang:All,Structured Data:All,Images:All" \
  --output-folder ./pre-migration-baseline \
  --timestamped-output
```
Save the `.seospider` binary too for later re-loading.

### Recipe 2: Top-traffic URL baseline
```bash
# Ahrefs top pages by organic traffic
mcp tool ahrefs.site_explorer \
  --target "old-site.com" \
  --mode "top_pages" \
  --limit 1000 \
  --sort "traffic_desc" \
  --include_metrics '["url","traffic","keywords","value","backlinks"]' > top_pages.json

# GSC top pages by clicks (12-month window)
mcp tool suganthan-gsc.top_pages \
  --site_url "sc-domain:old-site.com" \
  --days 365 \
  --metric "clicks" \
  --limit 1000 > gsc_top.json
```

### Recipe 3: Master URL list with traffic ranking
```python
import pandas as pd, json

ahrefs = pd.DataFrame(json.load(open('top_pages.json'))['data'])
gsc = pd.DataFrame(json.load(open('gsc_top.json'))['rows'])

# Combine
master = ahrefs.merge(gsc, left_on='url', right_on='page', how='outer', suffixes=('_ahrefs','_gsc'))
master['composite_score'] = master['traffic'].fillna(0) + master['clicks'].fillna(0) * 0.5
master = master.sort_values('composite_score', ascending=False)
master.to_csv('master-url-list.csv', index=False)

# Top 100 = MUST 1:1 map
# 101-1000 = strongly preferred 1:1
# 1001+ = 1:N acceptable (consolidate where logical)
```

### Recipe 4: URL mapping template (CSV)
```csv
Old URL,New URL,Migration Type,Owner,Status,Notes
https://old-site.com/products/widget-1,https://new-site.com/widgets/widget-1,1:1,@alice,Mapped,Direct migration
https://old-site.com/blog/2020/post-1,https://new-site.com/blog/post-1,1:1,@bob,Mapped,URL simplification
https://old-site.com/category/electronics,https://new-site.com/shop/electronics,1:1,@alice,Mapped,
https://old-site.com/old-product-page,https://new-site.com/products/replacement-widget,1:N->1,@alice,Mapped,Consolidation - old product discontinued
https://old-site.com/seasonal-2023-page,https://new-site.com/seasonal,N:1,@bob,Mapped,Consolidating all year pages into evergreen
```
**Migration types:**
- `1:1` — direct one-to-one mapping (preferred for top traffic)
- `1:N->1` — old page mapped to most-relevant new (when 1:N, pick the most relevant, NEVER homepage as catch-all)
- `N:1` — multiple old → one new (acceptable for consolidation)
- `Removed` — old page genuinely gone (returns 410)
- `Kept` — no URL change (rare; usually only path stays identical)

### Recipe 5: Redirect rules per stack
```apache
# Apache .htaccess — pattern-based 301
RewriteEngine On
RewriteRule ^products/widget-1$ /widgets/widget-1 [R=301,L]
RewriteRule ^blog/(\d{4})/(.+)$ /blog/$2 [R=301,L]
RewriteRule ^category/(.+)$ /shop/$1 [R=301,L]
```

```nginx
# Nginx
rewrite ^/products/widget-1$ /widgets/widget-1 permanent;
rewrite ^/blog/(\d{4})/(.+)$ /blog/$1 permanent;
rewrite ^/category/(.+)$ /shop/$1 permanent;
```

```javascript
// Cloudflare Workers
addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  const redirects = {
    '/products/widget-1': '/widgets/widget-1',
    '/old-page': '/new-page',
  };
  if (redirects[url.pathname]) {
    return event.respondWith(Response.redirect(new URL(redirects[url.pathname], url.origin), 301));
  }
});
```

```json
// vercel.json
{
  "redirects": [
    {"source":"/products/widget-1","destination":"/widgets/widget-1","permanent":true},
    {"source":"/blog/:year(\\d{4})/:slug","destination":"/blog/:slug","permanent":true},
    {"source":"/category/:slug","destination":"/shop/:slug","permanent":true}
  ]
}
```

```javascript
// next.config.js
module.exports = {
  async redirects() {
    return [
      {source: '/products/widget-1', destination: '/widgets/widget-1', permanent: true},
      {source: '/blog/:year(\\d{4})/:slug', destination: '/blog/:slug', permanent: true},
    ];
  }
};
```

### Recipe 6: 301 verification post-deploy
```python
import requests

mapping = pd.read_csv('master-url-list.csv')

issues = []
for _, row in mapping.iterrows():
    r = requests.head(row['Old URL'], allow_redirects=False, timeout=10)

    # Must be 301
    if r.status_code != 301:
        issues.append({'old': row['Old URL'], 'issue': f'Status {r.status_code} — not 301'})
        continue

    location = r.headers.get('Location','')
    if location != row['New URL']:
        issues.append({'old': row['Old URL'], 'issue': f'Redirect target mismatch: {location} != {row["New URL"]}'})

print(f"Migration issues: {len(issues)}")
for i in issues[:20]: print(i)
```

### Recipe 7: Redirect chain detection (multi-hop = bad)
```python
import requests

def follow_redirects(url, max_hops=10):
    hops = []
    current = url
    for _ in range(max_hops):
        r = requests.head(current, allow_redirects=False, timeout=5)
        hops.append((current, r.status_code))
        if r.status_code not in [301, 302, 307, 308]:
            break
        current = r.headers.get('Location')
        if current is None: break
    return hops

# Check sample
for old_url in mapping['Old URL'].sample(50):
    chain = follow_redirects(old_url)
    if len(chain) > 2:  # > 1 hop = chain
        print(f"CHAIN: {chain}")
```
**Rule: no chains > 1 hop.** Each hop loses signal; Google may stop following after 5 hops.

### Recipe 8: Post-migration daily monitoring (30-day playbook)
```python
# Day 0 (deploy day)
# 1. Recipe 6: 301 verification
# 2. Indexing API: submit all new URLs
mcp tool suganthan-gsc.submit_batch --urls_file "@new-urls.txt" --type URL_UPDATED

# Day 1-7 (daily SF crawl of new site)
def daily_crawl_check(day):
    # SF crawl
    subprocess.run([
        'screamingfrogseospider', '--crawl', 'https://new-site.com',
        '--headless', '--export-tabs', 'Internal:All,Response Codes:All',
        '--output-folder', f'./day-{day}-crawl'
    ])
    # Check 4xx
    internal = pd.read_csv(f'./day-{day}-crawl/internal_all.csv')
    errors = internal[internal['Status Code'].between(400,599)]
    return len(errors)

# Day 1-30 (daily GSC Coverage)
def daily_coverage_check(day):
    r = mcp.call('suganthan-gsc.index_coverage', site_url='sc-domain:new-site.com')
    return r['valid'] / r['total']

# Day 1-30 (daily organic traffic delta vs baseline)
def daily_traffic_check(day):
    baseline = get_pre_migration_baseline()
    current = get_current_traffic()
    delta = (current - baseline) / baseline
    return delta

# Alert if traffic drops >20%
if daily_traffic_check(day) < -0.20:
    gmail.send(to='seo-team@example.com', subject=f'ALERT: Traffic drop {delta:.0%} day {day}')
```

### Recipe 9: Indexing API ramp for new URLs
```bash
# Day 0: submit top 200 new URLs
head -200 new-urls.txt > /tmp/batch-0.txt
mcp tool suganthan-gsc.submit_batch --urls_file "@/tmp/batch-0.txt" --type URL_UPDATED

# Day 1-N: 200/day until all submitted (or request quota increase)
# IndexNow mirror for Bing
while read url; do
  curl -X POST "https://www.bing.com/indexnow?url=$url&key=$INDEXNOW_KEY"
done < /tmp/batch-0.txt
```

### Recipe 10: Old sitemap retention (3-6 months post-migration)
```
Keep old sitemap accessible at old domain for 3-6 months post-migration:
- Old domain returns 301 for individual URLs
- Old sitemap URL returns 301 to new sitemap
- This signals Google to discover the mapping

After 6 months: retire old domain. Risk: link equity loss to deeply-cached old URLs if old domain expires.
```

### Recipe 11: Pre-migration crawl ETL
```python
# Before migration, snapshot:
# (a) All URLs + canonicals + status codes + word count
# (b) Top 1000 by traffic with metadata
# (c) Inbound link profile (Ahrefs site_explorer all_backlinks)
# (d) Schema markup per URL
# (e) GSC top queries + impressions per URL

snapshot = {
    'crawl_urls': pre_crawl_df,
    'top_traffic_urls': master_url_list_df,
    'backlink_profile': ahrefs.site_explorer(target='old-site.com', mode='backlinks', limit=10000),
    'schema_per_url': pre_crawl_df[['Address','Structured Data']],
    'gsc_top_queries': gsc_query_export
}

# Persist for post-migration comparison
import pickle
pickle.dump(snapshot, open('pre-migration-snapshot.pkl','wb'))
```

### Recipe 12: Migration retrospective (Day 30 + Day 90)
```python
# Day 30 + Day 90 comparison vs baseline
pre = pickle.load(open('pre-migration-snapshot.pkl','rb'))

day_30 = {
    'organic_traffic': get_current_traffic(),
    'indexed_count': get_index_coverage(),
    'top_traffic_urls': get_current_top_pages(),
    'backlink_count': ahrefs.site_explorer(target='new-site.com', mode='backlinks', limit=10000),
}

# Report
print(f"Traffic delta: {(day_30['organic_traffic'] - pre['baseline_traffic']) / pre['baseline_traffic']:.1%}")
print(f"Indexed delta: {day_30['indexed_count'] - pre['indexed_count']}")
print(f"Backlink retention: {len(set(b['url'] for b in day_30['backlink_count']) & set(b['url'] for b in pre['backlink_profile']))} / {len(pre['backlink_profile'])}")
```

## Examples

### Example 1: Platform migration (Wordpress → Next.js)
**Goal:** Migrate without traffic loss.

**Steps:**
1. Recipe 1: pre-migration SF crawl of WP site.
2. Recipe 2 + 3: top-1000 URL list ranked by traffic.
3. Recipe 4: URL mapping CSV — 1:1 for top 200, 1:N for long tail.
4. Recipe 5: Generate next.config.js redirects.
5. Pre-deploy QA: stage environment + Recipe 6 verification on staging.
6. Deploy.
7. Recipe 6: production 301 verification immediately post-deploy.
8. Recipe 9: Indexing API submit top 200 day 0.
9. Recipe 8: 30-day daily monitoring.
10. Day 30: Recipe 12 retrospective.

**Result:** Migration with <10% temporary traffic dip, recovered by day 14.

### Example 2: Domain migration (brand.com → new-brand.com)
**Goal:** Domain change with URL preservation.

**Steps:**
1. Recipe 1: full crawl of old domain.
2. Mapping CSV: every old URL → same path on new domain.
3. Recipe 5: server-level wildcard 301 (Nginx `rewrite ^(.*)$ https://new-brand.com$1 permanent;`).
4. Recipe 9: Indexing API submit ALL new URLs (apply for quota increase to 1000/day; 50K URLs takes 50 days passive).
5. Search Console: configure change-of-address tool.
6. Recipe 8: monitoring for 60+ days (domain migrations take longer to recover than URL changes).

**Result:** Brand transition; full recovery 60-90 days.

## Edge cases / gotchas

- **Always 301, never 302** — 302 = temporary; doesn't pass full link equity. Google reaffirmed 2024.
- **No redirect chains > 1 hop** — update all redirects to point to FINAL destination directly.
- **Never redirect to homepage as catch-all** — loses query-relevance signal. Use most-relevant URL or 410.
- **Top-100 traffic URLs require 1:1 mapping** — anything else risks significant traffic loss.
- **Cannibalization audit BEFORE migration** — migration is a perfect time to consolidate cannibalizing URLs. Run `suganthan-gsc-cannibalization-decay-indexing` first.
- **301 doesn't pass 100% of link equity (~85-95%)** — minor decay is normal. >20% drop indicates 301 issues, not normal decay.
- **Search Console "Change of Address" tool** — only for domain migrations (not URL restructures). Configure within 90 days of switch.
- **Robots.txt + sitemap.xml on new domain immediately** — without these, Google may not discover new URLs.
- **Hreflang updates required** — if multi-region, every alternate URL must update simultaneously. Reciprocity check (Recipe 5 in `hreflang-i18n-implementation-verification` skill).
- **Backlink retention** — Google preserves backlink signal across 301s but external sites linking to old URLs still point at 301-source. After migration, optionally reach out to top linking sites to update to new URLs directly.
- **Internal link updates** — replace internal links with new URLs (don't rely on 301 chains internally).
- **Wildcard redirects too broad** — `RewriteRule ^(.*)$ /new$1 [R=301,L]` can break specific pages that need custom mapping. Specific rules first, wildcard last.
- **Mobile vs desktop URL differences** — m.example.com → www.example.com migration requires hreflang + mobile-first signals.
- **Crawl-budget shock** — Googlebot may slow crawl when seeing massive 301 changes. Submit via Indexing API to compensate.

## Sources

- [Search Engine Journal — SEO website migration checklist](https://www.searchenginejournal.com/seo-website-migration-checklist/)
- [Google Search Central — site move with URL changes](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes)
- [Google Search Central — site move without URL changes](https://developers.google.com/search/docs/crawling-indexing/site-move-no-url-changes)
- [Google Search Central — change of address tool](https://support.google.com/webmasters/answer/9370220)
- [Google Search Central — 301 vs 302](https://developers.google.com/search/docs/crawling-indexing/301-redirects)
- [Ahrefs blog — site migration](https://ahrefs.com/blog/site-migration/)
- [Aleyda Solis — migration guide](https://www.aleydasolis.com/english/blog/seo-website-migration-guide/)
- [Vercel redirects documentation](https://vercel.com/docs/edge-network/redirects)
- [Next.js redirects in config](https://nextjs.org/docs/app/api-reference/next-config-js/redirects)
