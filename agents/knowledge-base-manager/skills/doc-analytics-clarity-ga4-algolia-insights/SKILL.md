---
name: doc-analytics-clarity-ga4-algolia-insights
description: KB analytics stack — Microsoft Clarity (free heatmaps/replays), GA4 Data API (sessions/exit/time-on-page), Algolia DocSearch Insights (top-searched/no-result/CTR). Use when measuring "what to write next" and "what to fix first".
---

# Doc analytics — Clarity + GA4 + Algolia Insights

## When to use

User says "wire up KB analytics", "what should we write next", "what pages are bad", "session replays for docs", "top-searched terms", "high-exit pages". Reach BEFORE deciding content roadmap or fix priorities — instrument first, opine after.

Defer product-analytics overlays (PostHog/Mixpanel) to `data-agent` if KB is downstream of product events.

## Setup

```bash
# Microsoft Clarity — add tag to KB site, then wire MCP
# https://clarity.microsoft.com/ → projects → settings → install code

# GA4 Data API SDK
pip install google-analytics-data

# Algolia Insights (already part of DocSearch)
# Use the Analytics-only API key from Algolia dashboard

# Useful glue
pipx install duckdb  # cross-source SQL joins
```

Auth / API key requirements:
- Clarity: `CLARITY_API_TOKEN` from project settings → Data Export (Enterprise tier only — free fallback is the dashboard UI)
- GA4: service-account JSON via Google Cloud → APIs & Services → Credentials; grant Viewer on GA4 property
- Algolia: `ALGOLIA_APP_ID` + `ALGOLIA_ANALYTICS_KEY` (analytics-only ACL)

## Common recipes

### Recipe 1: Install Clarity on docs site

```html
<!-- before </head> -->
<script type="text/javascript">
  (function(c,l,a,r,i,t,y){
    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
  })(window, document, "clarity", "script", "YOUR_PROJECT_ID");
</script>
```

Verify in Clarity dashboard → Sessions (≤2h propagation).

### Recipe 2: Clarity Data Export API (Enterprise)

```bash
# Pull last 1d project metrics + filtered URL
curl -X GET "https://www.clarity.ms/export-data/api/v1/project-live-insights?numOfDays=1&dimension1=URL" \
  -H "Authorization: Bearer $CLARITY_API_TOKEN" \
  | jq '.[] | select(.URL | contains("/docs/")) | {URL, RageClickPercentage, DeadClickPercentage, ExcessiveScrollPercentage}'
```

For free tier: export CSV from dashboard manually (Filters → Date range → Export).

### Recipe 3: GA4 — top exit pages from KB

```python
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange, Dimension, Metric, RunReportRequest, FilterExpression, Filter,
)
client = BetaAnalyticsDataClient()
req = RunReportRequest(
    property=f"properties/{PROPERTY_ID}",
    dimensions=[Dimension(name="pagePath")],
    metrics=[Metric(name="screenPageViews"), Metric(name="exits"), Metric(name="userEngagementDuration")],
    date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
    dimension_filter=FilterExpression(filter=Filter(field_name="pagePath", string_filter=Filter.StringFilter(value="/docs/", match_type=Filter.StringFilter.MatchType.BEGINS_WITH))),
    limit=200,
)
resp = client.run_report(req)
for row in resp.rows:
    path = row.dimension_values[0].value
    views = int(row.metric_values[0].value)
    exits = int(row.metric_values[1].value)
    if views > 100:
        print(f"{path}\t{views}\t{exits/views:.1%}\t{row.metric_values[2].value}")
```

### Recipe 4: Algolia Insights — top-searched + no-result

```bash
# Top-searched (with CTR)
curl -G "https://analytics.algolia.com/2/searches" \
  -H "X-Algolia-Application-Id: $ALGOLIA_APP_ID" \
  -H "X-Algolia-API-Key: $ALGOLIA_ANALYTICS_KEY" \
  --data-urlencode "index=docs" \
  --data-urlencode "startDate=$(date -d '7 days ago' +%F)" \
  --data-urlencode "limit=50" \
  | jq -r '.searches[] | [.count, .search, .clickThroughRate] | @tsv' > top-search-7d.tsv

# No-result-found
curl -G "https://analytics.algolia.com/2/searches/noResults" \
  -H "X-Algolia-Application-Id: $ALGOLIA_APP_ID" \
  -H "X-Algolia-API-Key: $ALGOLIA_ANALYTICS_KEY" \
  --data-urlencode "index=docs" \
  --data-urlencode "startDate=$(date -d '7 days ago' +%F)" \
  | jq -r '.searches[] | [.count, .search] | @tsv' > no-result-7d.tsv
```

### Recipe 5: Algolia — CTR per page (find bad snippets)

```bash
curl -G "https://analytics.algolia.com/2/clicks/positions" \
  -H "X-Algolia-Application-Id: $ALGOLIA_APP_ID" \
  -H "X-Algolia-API-Key: $ALGOLIA_ANALYTICS_KEY" \
  --data-urlencode "index=docs" \
  --data-urlencode "startDate=$(date -d '30 days ago' +%F)"
```

Position 1 + CTR <40% = title/snippet mismatch. Rewrite title + meta.

### Recipe 6: Join via DuckDB

```bash
duckdb << 'EOF'
CREATE TABLE search AS SELECT * FROM read_csv('top-search-7d.tsv', delim='\t', columns={'count':'INTEGER','query':'VARCHAR','ctr':'DOUBLE'});
CREATE TABLE noresult AS SELECT * FROM read_csv('no-result-7d.tsv', delim='\t', columns={'count':'INTEGER','query':'VARCHAR'});
CREATE TABLE exits AS SELECT * FROM read_csv('ga4-exits.tsv', delim='\t', columns={'path':'VARCHAR','views':'INTEGER','exit_rate':'DOUBLE'});

-- Find: high-traffic + high-exit (FIX FIRST)
SELECT path, views, exit_rate FROM exits WHERE views > 500 AND exit_rate > 0.7 ORDER BY views DESC LIMIT 20;

-- Find: top no-result (WRITE NEXT)
SELECT * FROM noresult ORDER BY count DESC LIMIT 20;
EOF
```

### Recipe 7: Weekly report markdown

```python
# kb_weekly.py
import datetime, json, subprocess
def algolia(endpoint, params):
    r = subprocess.check_output(['curl','-sG',f'https://analytics.algolia.com/2/{endpoint}',
        '-H',f'X-Algolia-Application-Id: $ALGOLIA_APP_ID',
        '-H',f'X-Algolia-API-Key: $ALGOLIA_ANALYTICS_KEY',
        *[f'--data-urlencode={k}={v}' for k,v in params.items()]])
    return json.loads(r)

date = datetime.date.today().isocalendar()
print(f"# KB Analytics Weekly — {date.year}-W{date.week}\n")
# ... assemble markdown report ...
```

### Recipe 8: PostHog overlay (if recipient uses it)

```bash
# PostHog query for kb_view + ticket_open join
curl -X POST "https://app.posthog.com/api/projects/$PROJECT_ID/query" \
  -H "Authorization: Bearer $POSTHOG_KEY" \
  -d '{"query":{"kind":"HogQLQuery","query":"SELECT properties.article_id, count() FROM events WHERE event=\"kb_view\" AND timestamp > now() - INTERVAL 7 DAY GROUP BY properties.article_id ORDER BY count() DESC LIMIT 20"}}'
```

### Recipe 9: Clarity smart events (rage click bookmark)

In Clarity UI: Settings → Smart Events → create "Rage Click on /docs/" → enables filtering. Export via CSV (free tier).

### Recipe 10: Algolia Insights API events from client

```javascript
// Track click events for search analytics
import { insights } from '@algolia/client-search';
insights('clickedObjectIDsAfterSearch', {
  index: 'docs',
  eventName: 'Article clicked',
  queryID: lastQueryID,
  objectIDs: [articleID],
  positions: [position],
});
```

## Examples

### Example 1: Weekly "Write Next / Fix First" report

**Goal:** Stand up a recurring report for the docs team.

**Steps:**
1. Pull Algolia no-result + top-search (Recipes 4, 5).
2. Pull GA4 high-exit (Recipe 3).
3. Pull Clarity rage clicks (Recipe 2 or dashboard export).
4. Join via DuckDB (Recipe 6).
5. Output markdown (Recipe 7).
6. Schedule via cron + post to Slack via webhook.

**Result:**

```markdown
# KB Analytics Weekly — 2026-W23

## Write next (no-result-found 7d)
| Query | Count | Owner |
|---|---|---|
| webhook retry strategy | 47 | @alice |
| sso group sync | 38 | @bob |

## Fix first (high-traffic + high-exit)
| Page | Views | Exit | Rage% | Owner |
|---|---|---|---|---|
| /get-started/quickstart | 8420 | 76% | 14% | @alice |
```

### Example 2: Find broken search-result snippets

**Goal:** Pages that rank #1 but get few clicks have mismatched titles.

**Steps:**
1. Pull Algolia CTR per page (Recipe 5).
2. Filter: position ≤ 3 AND ctr < 40%.
3. For each, open Clarity session replays for that URL.
4. Rewrite title + meta description.
5. Re-check after 14d.

**Result:** CTR rises 15-30 pts on rewritten pages.

## Edge cases / gotchas

- **Clarity Data Export API** is Enterprise-only; free tier limited to dashboard + CSV export.
- **GA4 quotas** — 200 reports/day default property quota. Cache.
- **Algolia analytics-only key** is mandatory; do NOT use admin key for read-only analytics.
- **Cookie consent** — GDPR / CCPA blocks Clarity / GA4 for users who decline. Coverage <100%; document the gap.
- **Cross-source joins need a common key** — use UTM or hash-of-path. Different tools normalize URLs differently (trailing slash, query strings).
- **"No-result" counts include bots** — filter user-agents on serve.
- **GA4 path normalization** — `pagePath` strips query; if your KB uses query-string params for versions, use `pagePathPlusQueryString`.
- **Don't use sampled data for content decisions** — GA4 samples above 10M events; use the unsampled Data API.
- **Insights API has 30-day retention on free** — archive weekly to S3 or DuckDB.

## Sources

- Microsoft Clarity: https://clarity.microsoft.com/
- Clarity Data Export API: https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-data-export-api
- GA4 Data API: https://developers.google.com/analytics/devguides/reporting/data/v1
- Algolia Analytics API: https://www.algolia.com/doc/rest-api/analytics/
- Algolia Insights: https://www.algolia.com/doc/guides/sending-events/getting-started/
- DuckDB: https://duckdb.org/
- PostHog HogQL: https://posthog.com/docs/hogql
