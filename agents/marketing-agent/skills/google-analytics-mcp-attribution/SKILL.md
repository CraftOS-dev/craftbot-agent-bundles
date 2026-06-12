<!--
Source: https://github.com/googleanalytics/google-analytics-mcp
Official GA4 MCP — 6 tools, run_report for last-touch attribution
-->
# Google Analytics MCP — Attribution — SKILL

The official Google Analytics MCP (`googleanalytics/google-analytics-mcp`) exposes 6 tools including `run_report` for GA4 last-touch attribution, `run_realtime_report`, and funnel analysis. Pairs with HubSpot deals to compute ROI per channel / campaign.

## When to use this skill

- **Last-touch attribution** — which campaign/source closed the conversion.
- **Multi-touch attribution** approximation via path reports.
- **Conversion funnels** — multi-step user journey conversion.
- **Realtime monitoring** — campaign launch monitoring (first 24h).
- **Channel performance comparison** — organic vs paid vs email vs direct.
- **UTM-based campaign reporting** — pair with `bitly-utm-campaign-tracking` skill.

**Do NOT use this skill when:**
- **Product-level analytics + cohort retention** — use `posthog-growth-loops` skill.
- **Email-specific metrics** (CTR, CTOR, revenue per recipient) — use `klaviyo-email-lifecycle` skill.
- **SEO performance** — use `suganthan-gsc-audit` skill.

## Setup

### Install

```bash
npx -y @googleanalytics/google-analytics-mcp@latest
```

### Auth — service account or OAuth

```bash
# Service account (recommended for automation)
export GA_SERVICE_ACCOUNT_JSON="./ga-service-account.json"
export GA_PROPERTY_ID="<numeric-property-id>"  # 9-digit number

# Or OAuth one-time
ga-mcp auth
```

Grant the service account "Viewer" on the GA4 property.

### 6 tools available

- `run_report` — core query, dimensions × metrics × filters × dateRange
- `run_realtime_report` — last 30 min, limited dimensions
- `run_pivot_report` — pivot table style
- `get_metadata` — list available dimensions / metrics
- `batch_run_reports` — up to 5 reports in one call
- `check_compatibility` — verify a query's dimension/metric combo is valid

## Common recipes

### Recipe 1: Last-touch attribution by source/medium/campaign

```bash
mcp tool google-analytics.run_report \
  --property "$GA_PROPERTY_ID" \
  --dateRanges '[{"startDate":"30daysAgo","endDate":"today"}]' \
  --dimensions '["sessionSource","sessionMedium","sessionCampaignName"]' \
  --metrics '["sessions","conversions","totalRevenue","userConversionRate"]' \
  --orderBys '[{"metric":{"metricName":"totalRevenue"},"desc":true}]' \
  --limit 100
```

Returns per source/medium/campaign:
- Sessions
- Conversions
- Total revenue
- Per-user conversion rate

### Recipe 2: Multi-touch attribution (path report approximation)

GA4 native attribution model in `run_report`:

```bash
mcp tool google-analytics.run_report \
  --property "$GA_PROPERTY_ID" \
  --dateRanges '[{"startDate":"30daysAgo","endDate":"today"}]' \
  --dimensions '["sessionSource","sessionMedium"]' \
  --metrics '["conversions","totalRevenue"]' \
  --metricAggregations '["TOTAL"]' \
  --comparisons '[
    {"name":"Data-driven","attribution":"DATA_DRIVEN"},
    {"name":"Last-touch","attribution":"LAST_CLICK"},
    {"name":"First-touch","attribution":"FIRST_CLICK"},
    {"name":"Linear","attribution":"LINEAR"},
    {"name":"U-shape","attribution":"POSITION_BASED"}
  ]'
```

Reveals model bias — if data-driven attributes 40% of revenue to organic but last-click only 10%, organic is under-credited.

### Recipe 3: Conversion funnel (multi-step)

```bash
mcp tool google-analytics.run_report \
  --property "$GA_PROPERTY_ID" \
  --dateRanges '[{"startDate":"30daysAgo","endDate":"today"}]' \
  --dimensions '["eventName"]' \
  --metrics '["eventCount","totalUsers"]' \
  --dimensionFilter '{"filter":{"fieldName":"eventName","inListFilter":{"values":["page_view","view_item","add_to_cart","begin_checkout","purchase"]}}}'
```

Or define an audience funnel:

```bash
mcp tool google-analytics.run_report \
  --property "$GA_PROPERTY_ID" \
  --funnel '{
    "steps":[
      {"name":"Landed","filter":{"eventName":"page_view","page":"/lp"}},
      {"name":"Engaged","filter":{"eventName":"scroll","percent":">=75"}},
      {"name":"CTA Click","filter":{"eventName":"click","cta_id":"primary"}},
      {"name":"Form Submit","filter":{"eventName":"form_submit"}},
      {"name":"Convert","filter":{"eventName":"purchase"}}
    ]
  }' \
  --dateRanges '[{"startDate":"30daysAgo","endDate":"today"}]'
```

### Recipe 4: Realtime — campaign launch monitoring

```bash
mcp tool google-analytics.run_realtime_report \
  --property "$GA_PROPERTY_ID" \
  --dimensions '["sessionSource","sessionMedium","sessionCampaignName","pageTitle"]' \
  --metrics '["activeUsers","screenPageViews","conversions"]' \
  --minuteRanges '[{"name":"last-5","startMinutesAgo":5,"endMinutesAgo":0}]'
```

Run on a 5-min cron for the first 4 hours after launch. Alert on:
- Conversions = 0 after 1h (tracking broken?)
- Source = unexpected (organic, when only paid launched)
- Page errors spike

### Recipe 5: Pair with HubSpot for full ROI

```python
# Per-channel ROI = revenue / cost
# GA4 gives revenue; HubSpot gives deal amount (B2B); ad MCPs give cost

# Step 1: pull GA4 revenue by source/medium
ga_report = ga.run_report(
    dimensions=['sessionSource','sessionMedium','sessionCampaignName'],
    metrics=['totalRevenue','conversions'],
    dateRange='last_30_days',
)

# Step 2: pull HubSpot deals
deals = hubspot.list_deals(filter={'stage':'closedwon','closedate':'>=30daysAgo'})
deal_attribution = {}
for d in deals:
    c = hubspot.get_contact(d['primary_contact_id'])
    campaign = c['properties'].get('hs_analytics_first_url_utm_campaign')
    deal_attribution.setdefault(campaign, 0)
    deal_attribution[campaign] += d['amount']

# Step 3: pull ad spend
meta_spend = meta_ads.get_campaign_insights(date_preset='last_30_days')
google_spend = google_ads.search(query="SELECT campaign.name, metrics.cost_micros FROM campaign WHERE segments.date DURING LAST_30_DAYS")

# Step 4: compute ROI per campaign
for row in ga_report:
    campaign = row['sessionCampaignName']
    revenue = row['totalRevenue'] + deal_attribution.get(campaign, 0)
    cost = meta_spend.get(campaign, 0) + google_spend.get(campaign, 0)
    roi = (revenue - cost) / cost if cost else None
    print(f"{campaign}: revenue ${revenue}, cost ${cost}, ROI {roi:.2f}")
```

### Recipe 6: Audience segments (acquisition cohort × behavior)

```bash
mcp tool google-analytics.run_report \
  --property "$GA_PROPERTY_ID" \
  --dimensions '["firstUserSource","firstUserMedium","newVsReturning"]' \
  --metrics '["activeUsers","sessions","engagedSessions","engagementRate","averageSessionDuration"]' \
  --dateRanges '[{"startDate":"30daysAgo","endDate":"today"}]' \
  --limit 50
```

Reveals acquisition channel quality — high engagement = quality traffic; low engagement = source over-reports volume.

### Recipe 7: Page-level conversion (landing page analytics)

```bash
mcp tool google-analytics.run_report \
  --property "$GA_PROPERTY_ID" \
  --dimensions '["landingPage"]' \
  --metrics '["sessions","conversions","totalRevenue","userConversionRate","engagedSessions"]' \
  --orderBys '[{"metric":{"metricName":"sessions"},"desc":true}]' \
  --limit 20 \
  --dateRanges '[{"startDate":"30daysAgo","endDate":"today"}]'
```

Find:
- High traffic + low conversion = LP optimization opportunity
- High conversion + low traffic = scale opportunity (paid amplification)

### Recipe 8: Event-based custom conversions

For e-commerce / SaaS, mark events as conversions in GA4 UI, then:

```bash
mcp tool google-analytics.run_report \
  --property "$GA_PROPERTY_ID" \
  --dimensions '["eventName"]' \
  --metrics '["eventCount","conversions","totalRevenue"]' \
  --dimensionFilter '{"filter":{"fieldName":"eventName","stringFilter":{"value":"sign_up","matchType":"EXACT"}}}'
```

Common SaaS conversions:
- `sign_up`
- `start_trial`
- `subscribe`
- `add_payment_info`
- `complete_onboarding`

## Examples — monthly marketing performance report

```markdown
# Marketing Performance — June 2026

## Channel performance (last 30d, last-touch)
| Channel | Sessions | Conversions | Revenue | CVR | Rev/Session |
|---|---|---|---|---|---|
| Organic Search | 45,200 | 412 | $42,140 | 0.91% | $0.93 |
| Paid Search | 12,800 | 386 | $38,600 | 3.02% | $3.02 |
| Direct | 8,200 | 78 | $7,820 | 0.95% | $0.95 |
| Email | 6,500 | 245 | $18,400 | 3.77% | $2.83 |
| Social Organic | 5,400 | 41 | $4,100 | 0.76% | $0.76 |
| Paid Social | 3,800 | 92 | $9,800 | 2.42% | $2.58 |

## Campaign ROI (last 30d)
| Campaign | Channel | Spend | Revenue | ROI |
|---|---|---|---|---|
| Q3-launch-paidsearch | Paid Search | $4,200 | $14,800 | 252% |
| Q3-launch-paidsocial | Paid Social | $3,100 | $9,800 | 216% |
| evergreen-newsletter | Email | $0 | $18,400 | ∞ |

## Funnel — Q3 landing page
| Step | Users | % from prior |
|---|---|---|
| Landed on LP | 12,800 | — |
| Engaged (scroll 75%+) | 6,400 | 50% |
| CTA click | 2,560 | 40% |
| Form submit | 768 | 30% |
| Purchase | 92 | 12% |

## Attribution model comparison
- Last-click attributes 12% of revenue to organic; data-driven attributes 28%. Organic is under-credited 16 pts.
- Recommend reporting both side-by-side.
```

## Edge cases

### GA4 vs UA legacy
GA4 only. Universal Analytics fully sunset 2024. Don't accept "UA-XXX" property IDs.

### Sampling
Reports with > 10M events may be sampled. The response includes `samplingMetadatas` — check `samplesRead` vs `samplingSpaceSizes`. For unsampled, use `BigQuery export` (separate GA4 setup).

### Quotas
- 200,000 tokens/day per property
- 50 concurrent requests
- Token cost varies by query complexity

### Conversion vs event
GA4 has no `goals` — every event can be marked as a "conversion" in UI. The MCP queries by event name; ensure the event is marked as conversion or filter manually.

### Attribution model availability
- Data-driven attribution requires ≥300 conversions / 50 conversion paths in last 30d
- Below threshold, fall back to last-click

### UTM normalization
GA4 normalizes some sources (`google` + `cpc` = "Paid Search"). For exact UTM matching, use `sessionCampaignSource` not `defaultChannelGroup`.

### Custom dimensions / metrics
If you've defined custom dimensions in GA4 (e.g., `user_plan_tier`), query them with `customEvent:user_plan_tier` syntax.

### Date ranges
- `7daysAgo` / `30daysAgo` / `yesterday` / `today` — relative
- `2026-06-01` — absolute
- Mixing: `[{startDate:'30daysAgo',endDate:'today'}, {startDate:'60daysAgo',endDate:'31daysAgo'}]` for period-over-period

### Realtime limitations
Realtime supports fewer dimensions than standard. Check `get_metadata --type realtime` for available fields.

### Cross-domain tracking
If marketing site → app at different domain, set up cross-domain in GA4 admin. Otherwise sessions split.

### Bot traffic
GA4 filters known bots by default but doesn't filter aggressive scrapers / monitoring tools. Add IP exclusions for known internal/external scanners.

### Consent mode
If using Google Consent Mode v2 (required in EU), denied-consent users show as modeled — accuracy ±5%. Note this in reports.

## Sources

- **GA4 MCP**: https://github.com/googleanalytics/google-analytics-mcp
- **GA Data API reference**: https://developers.google.com/analytics/devguides/reporting/data/v1
- **Dimension & metric list**: https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema
- **Attribution model docs**: https://support.google.com/analytics/answer/10596866
- **BigQuery export**: https://support.google.com/analytics/answer/9358801
