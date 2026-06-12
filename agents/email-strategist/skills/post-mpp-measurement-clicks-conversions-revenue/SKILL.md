<!--
Source: https://www.klaviyo.com/blog/apple-mail-privacy-protection
Post-Apple-MPP measurement. Opens inflated 40-60% on Apple Mail.
Use CTR / CTOR / revenue per recipient / conversion rate.
-->
# Post-MPP Measurement (Clicks / Conversions / Revenue) — SKILL

Apple Mail Privacy Protection (iOS 15+, Sep 2021) pre-fetches images on receipt → 40-60% of Apple Mail users register as "opened." Opens are no longer a real signal. Measure CTR, CTOR, conversion rate, revenue per recipient. Cross-reference GA4 for full-funnel attribution.

## When to use

- "How do we measure email performance now that opens are broken"
- "Pull last 90d CTR / CTOR / revenue per email from Klaviyo"
- "Cross-reference Klaviyo data with GA4 for full-funnel attribution"
- "Compare campaign A vs B without opens"
- "Build executive email dashboard"
- "Detect MPP-only opens vs real opens"

## Setup

```bash
# Klaviyo MCP server (covers metric APIs)
npx -y @klaviyo/mcp-server@latest

# GA4 (Google Analytics Data API)
gcloud services enable analyticsdata.googleapis.com

# postgresql-mcp / amplitude-mcp / mixpanel-mcp for cross-channel
```

Auth:

```bash
export KLAVIYO_API_KEY="pk_<key>"
export GA4_PROPERTY_ID="<property-id>"      # e.g., 123456789
export GA4_SA_KEY="$HOME/ga4-key.json"      # service account
```

## Common recipes

### Recipe 1: The metrics that matter (post-MPP)

| Metric | Definition | Why | Target |
|---|---|---|---|
| **CTR** | clicks / sends | Unaffected by MPP; engagement signal | > 2% e-com, > 3% B2B |
| **CTOR** | clicks / opens | Engagement among "engaged"; MPP inflates denominator but ratios still informative | > 10% |
| **Conversion rate** | conversions / sends | Bottom-line impact | > 0.5% |
| **Revenue per recipient** | total revenue / unique recipients | Economic value per send | $0.50-$5+ depending on product |
| **Placed-order rate** | orders / sends (5d window) | Klaviyo native | varies by product |
| **Unsubscribe rate** | unsubs / sends | Audience health signal | < 0.5% |
| **Complaint rate** | spam complaints / sends | Reputation signal | < 0.10% (target 0.02%) |
| **Click depth** | avg clicks per unique opener | Content depth | varies |

Do NOT primary on:
- **Open rate** — MPP-inflated; comparing year-over-year is meaningless post-Sep 2021
- **Unique open rate** — same problem

### Recipe 2: Klaviyo — get_campaign_metrics (single campaign)

```bash
curl -X POST "https://a.klaviyo.com/api/campaign-values-reports" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" \
  -H "revision: 2024-10-15" \
  -d '{
    "data": {"type":"campaign-values-report","attributes":{
      "statistics":["delivered","clicks","clicks_unique","click_rate","click_to_open_rate","conversions","conversion_rate","conversion_value","conversion_uniques","conversion_value_per_recipient","revenue","spam_complaints","spam_complaint_rate","unsubscribes","unsubscribe_rate","bounced","bounce_rate"],
      "timeframe":{"key":"last_30_days"},
      "conversion_metric_id":"<placed-order-metric-id>",
      "filter":"and(equals(campaign_id,\"<campaign-id>\"))"
    }}
  }' | jq '.data.attributes.results[0]'
```

Returns:

```json
{
  "campaign_id": "<id>",
  "groupings": [{"send_channel": "email"}],
  "statistics": {
    "delivered": 12450,
    "clicks": 524,
    "clicks_unique": 489,
    "click_rate": 0.0421,
    "click_to_open_rate": 0.1853,
    "conversions": 67,
    "conversion_rate": 0.00539,
    "conversion_value": 4231.50,
    "conversion_value_per_recipient": 0.34,
    "spam_complaints": 1,
    "spam_complaint_rate": 0.00008,
    "unsubscribes": 4,
    "unsubscribe_rate": 0.000321
  }
}
```

### Recipe 3: Klaviyo — flow metrics

```bash
curl -X POST "https://a.klaviyo.com/api/flow-values-reports" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" \
  -H "revision: 2024-10-15" \
  -d '{"data":{"type":"flow-values-report","attributes":{
    "statistics":["delivered","clicks_unique","click_rate","conversions","conversion_value","conversion_value_per_recipient"],
    "timeframe":{"key":"last_90_days"},
    "conversion_metric_id":"<placed-order-metric-id>",
    "filter":"and(equals(flow_id,\"<flow-id>\"))"
  }}}' | jq '.data.attributes.results[]'
```

### Recipe 4: Klaviyo — sort campaigns by revenue per recipient

```python
import requests, os
from datetime import datetime, timedelta

KEY = os.environ['KLAVIYO_API_KEY']
HDRS = {'Authorization': f'Klaviyo-API-Key {KEY}', 'revision': '2024-10-15'}

r = requests.post(
    'https://a.klaviyo.com/api/campaign-values-reports',
    headers=HDRS,
    json={'data':{'type':'campaign-values-report','attributes':{
        'statistics':['delivered','click_rate','conversion_rate','conversion_value','conversion_value_per_recipient','spam_complaint_rate','unsubscribe_rate'],
        'timeframe':{'key':'last_90_days'},
        'conversion_metric_id':'<placed-order-id>',
        'filter':'and(equals(send_channel,"email"))'
    }}}
).json()

# Rank by revenue per recipient
results = r['data']['attributes']['results']
ranked = sorted(results, key=lambda x: -x['statistics']['conversion_value_per_recipient'])
for c in ranked[:20]:
    s = c['statistics']
    print(f"{c['groupings']['campaign_name']:40s}  RPR=${s['conversion_value_per_recipient']:.2f}  CR={s['conversion_rate']:.2%}  CTR={s['click_rate']:.2%}")
```

### Recipe 5: GA4 — email-sourced conversions

```bash
# Generate access token
GA4_TOKEN=$(gcloud auth application-default print-access-token --scopes=https://www.googleapis.com/auth/analytics.readonly)

# Run report: conversions from utm_medium=email
curl -X POST "https://analyticsdata.googleapis.com/v1beta/properties/${GA4_PROPERTY_ID}:runReport" \
  -H "Authorization: Bearer $GA4_TOKEN" \
  -d '{
    "dateRanges":[{"startDate":"30daysAgo","endDate":"yesterday"}],
    "metrics":[{"name":"sessions"},{"name":"conversions"},{"name":"totalRevenue"}],
    "dimensions":[{"name":"sessionCampaignName"},{"name":"sessionSource"}],
    "dimensionFilter":{"filter":{"fieldName":"sessionMedium","stringFilter":{"value":"email"}}},
    "orderBys":[{"metric":{"metricName":"totalRevenue"},"desc":true}],
    "limit":100
  }' | jq '.rows[] | {campaign: .dimensionValues[0].value, source: .dimensionValues[1].value, sessions: .metricValues[0].value, conversions: .metricValues[1].value, revenue: .metricValues[2].value}'
```

### Recipe 6: UTM convention for email

Standardize UTMs at link-injection:

```
?utm_source=klaviyo
&utm_medium=email
&utm_campaign={{ campaign_name | url_encode }}
&utm_content={{ link_position }}
&utm_term={{ profile_segment_id | default: "broad" }}
```

In Klaviyo, set per-flow UTM tagging in template editor → "Link Tracking":

```bash
curl -X PATCH "https://a.klaviyo.com/api/flows/<flow-id>" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"flow","attributes":{
    "tracking_options":{
      "is_add_utm":true,
      "utm_params":[
        {"name":"utm_source","value":"klaviyo"},
        {"name":"utm_medium","value":"email"},
        {"name":"utm_campaign","value":"{{ flow.name }}"}
      ]
    }
  }}}'
```

### Recipe 7: MPP open de-noising

Klaviyo classifies "Machine Open" (MPP pre-fetch) via heuristics: open within < 1s of send, repeated open in same second from Apple IP ranges, no subsequent click.

```bash
# Klaviyo metric breakdown — actual vs Apple-pre-fetched opens
curl -X POST "https://a.klaviyo.com/api/campaign-values-reports" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"campaign-values-report","attributes":{
    "statistics":["opens","opens_unique","opens_unique_machine","opens_unique_real"],
    "timeframe":{"key":"last_30_days"},
    "filter":"and(equals(campaign_id,\"<id>\"))"
  }}}' | jq '.data.attributes.results[0].statistics'
```

`opens_unique_real = opens_unique - opens_unique_machine` — closer to reality but still flawed (not all MPP captured by heuristics).

### Recipe 8: Build executive email dashboard (warehouse + viz)

```sql
-- Postgres / warehouse
CREATE TABLE campaign_perf AS
SELECT
  date_trunc('week', sent_at) AS week,
  send_channel,
  COUNT(*) AS campaigns_sent,
  SUM(delivered) AS total_delivered,
  SUM(clicks_unique) AS total_clicks_unique,
  ROUND(SUM(clicks_unique)::numeric / SUM(delivered), 4) AS click_rate,
  SUM(conversion_value) AS total_revenue,
  ROUND(SUM(conversion_value)::numeric / SUM(delivered), 2) AS revenue_per_recipient,
  ROUND(SUM(spam_complaints)::numeric / SUM(delivered), 6) AS spam_complaint_rate
FROM klaviyo_campaign_metrics
GROUP BY 1, 2
ORDER BY 1 DESC;
```

Dashboard panels:
- Weekly revenue per recipient (trend)
- Spam complaint rate (alert if > 0.001)
- Top 10 campaigns by RPR last quarter
- Bottom 10 campaigns by RPR last quarter (kill / iterate list)
- Flow-vs-campaign revenue split

### Recipe 9: Cohort analysis (RPR by RFM tier × campaign type)

```sql
WITH campaign_lift AS (
  SELECT
    p.rfm_band,
    c.campaign_type,
    AVG(cm.conversion_value_per_recipient) AS avg_rpr,
    COUNT(*) AS sample_size
  FROM klaviyo_campaign_metrics cm
  JOIN profiles p ON p.id = cm.profile_id
  JOIN campaigns c ON c.id = cm.campaign_id
  WHERE cm.sent_at > NOW() - INTERVAL '6 months'
  GROUP BY 1, 2
)
SELECT * FROM campaign_lift ORDER BY rfm_band, avg_rpr DESC;
```

Insights: which campaign types resonate with which RFM band. e.g., Champions respond best to early-access; At-Risk responds best to free shipping.

### Recipe 10: A/B test analysis — never use opens

```python
# A/B test result analyzer — gates on CTR + revenue, not opens
import math
from scipy import stats

def ab_winner(a_sends, a_clicks, a_revenue, b_sends, b_clicks, b_revenue, alpha=0.05):
    # Click rate proportion test
    a_p = a_clicks / a_sends
    b_p = b_clicks / b_sends
    pool_p = (a_clicks + b_clicks) / (a_sends + b_sends)
    se = math.sqrt(pool_p * (1 - pool_p) * (1/a_sends + 1/b_sends))
    z = (b_p - a_p) / se if se else 0
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    # Revenue per recipient ratio
    a_rpr = a_revenue / a_sends
    b_rpr = b_revenue / b_sends

    return {
        'a_ctr': a_p, 'b_ctr': b_p, 'ctr_lift': (b_p - a_p) / a_p,
        'a_rpr': a_rpr, 'b_rpr': b_rpr, 'rpr_lift': (b_rpr - a_rpr) / a_rpr if a_rpr else 0,
        'p_value': p_value,
        'significant': p_value < alpha,
        'winner': 'B' if b_rpr > a_rpr and p_value < alpha else ('A' if a_rpr > b_rpr and p_value < alpha else 'TIE')
    }

print(ab_winner(5000, 220, 1842.50, 5000, 265, 2238.10))
```

## Examples

### Example 1: Quarterly email performance review

**Goal:** show stakeholders email is moving the business; identify what to amplify / cut.

**Steps:**

1. Pull last 90d campaign metrics (Recipe 4). Rank by revenue per recipient.
2. Pull last 90d flow metrics (Recipe 3). Same ranking.
3. Cross-reference GA4 (Recipe 5). Validate Klaviyo attribution against site analytics.
4. Build deck:
   - Total revenue from email (Klaviyo + GA4 cross-check)
   - Revenue per send trend (weekly chart)
   - Top 5 campaigns + top 5 flows by RPR
   - Spam complaint trend (must be < 0.001)
   - "What we'd kill" — bottom decile RPR, < $0.05/recipient → replace or cut
5. Use Klaviyo MPP-de-noised metrics (Recipe 7) if execs ask about opens.

### Example 2: Diagnose "engagement dropping" complaint

**Goal:** exec sees open rate falling 5% MoM; "engagement is dropping."

**Steps:**

1. Show MPP context — open rate has been distorted since Sep 2021.
2. Pull CTR trend (Recipe 4). Is CTR dropping?
3. If CTR steady or rising → engagement is fine; opens declining is noise.
4. If CTR falling → real concern. Drill into:
   - Segment definition shifts?
   - Frequency change?
   - Content / subject style change?
   - Deliverability issue (Postmaster trend)?
5. Recommend: stop reporting opens to execs; replace with CTR + RPR.

## Edge cases

- **Klaviyo opens_unique_machine heuristic is imperfect** — Apple Mail without MPP (older iOS) also pre-fetches sometimes. Treat all opens as soft signal.
- **GA4 attribution window** differs from Klaviyo's. GA4 default 30d click-through; Klaviyo default 5d. Reconcile with care.
- **Conversion metric must be defined in Klaviyo** — "Placed Order" is default for e-com; for SaaS, define a custom metric (e.g., "Upgraded to Paid").
- **Revenue currency** — Klaviyo aggregates in account default currency; if multi-currency, normalize via FX rates daily.
- **MPP-only-opened profiles are still "subscribers"** — don't suppress just because they didn't truly open. Engagement signal is clicks / orders / site visits.
- **CTR is also affected by clients that show images** — image-only emails have artificial CTR from "show images" clicks. Track unique clicks per profile.
- **B2B emails have low CTR (1-2%)** because audiences read but don't click. Compensate with engagement signal from product (logged in, used feature).
- **Open-rate ad-tech tracking pixels are pre-fetched** — your pixel firing != user opened. Use as cohort-level directional only.
- **Yahoo + Outlook image proxies** also pre-fetch but at smaller scale than Apple. Some "open" signal from those is still inflated.

## Sources

- [Klaviyo MPP guide](https://www.klaviyo.com/blog/apple-mail-privacy-protection)
- [Klaviyo campaign-values-reports API](https://developers.klaviyo.com/en/reference/query_campaign_values)
- [Klaviyo flow-values-reports API](https://developers.klaviyo.com/en/reference/query_flow_values)
- [Litmus: post-MPP measurement](https://www.litmus.com/blog/the-impact-of-apple-mail-privacy-protection-on-email-marketing/)
- [Google Analytics 4 Data API](https://developers.google.com/analytics/devguides/reporting/data/v1)
- [GA4 reportApi runReport](https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runReport)
- [UTM convention spec (Google)](https://support.google.com/analytics/answer/10917952)
