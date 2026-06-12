<!--
Source: https://developers.klaviyo.com/en/docs/klaviyo_mcp_server
Klaviyo MCP GA Feb 2026. Predictive AI on Klaviyo Plus / Advanced.
This skill goes DEEPER than marketing-agent's klaviyo-email-lifecycle:
predictive AI segments, custom RFM bands, churn-risk scoring, dynamic
dunning, smart send time on flows, multi-list orchestration.
-->
# Klaviyo Deep Lifecycle + Predictive AI — SKILL

Senior depth on Klaviyo: not "create a welcome flow" (parent agent covers that), but **predictive-AI segmentation with custom RFM band overlays**, **per-profile churn-risk scoring driving dunning escalation**, **Smart Send Time at flow-step granularity**, and **multi-list / multi-currency orchestration**. Treat opens as advisory only; `get_campaign_metrics` clicks + revenue is gospel.

## When to use

- "Build predictive-AI churn-risk dunning flow for high-CLV customers"
- "Overlay predicted_clv bands on RFM segments and route per band to different incentive tiers"
- "Turn on Smart Send Time on existing flow step-by-step (not campaign-level)"
- "Pull CTR + CTOR + revenue_per_recipient from last 90d campaigns and rank by net revenue lift"
- "Update profile's `churn_risk` from external warehouse model and trigger a flow"

Do **not** use for: simple welcome flow (use marketing-agent's klaviyo skill); transactional receipts (use resend-postmark skill); B2B nurture (use customer-io-b2b skill).

## Setup

```bash
# Klaviyo MCP server (GA Feb 2026)
npx -y @klaviyo/mcp-server@latest

# Verify
npx -y @klaviyo/mcp-server --version
```

Auth:

```bash
export KLAVIYO_API_KEY="pk_<your_private_key>"   # https://www.klaviyo.com/account#api-keys-tab
export KLAVIYO_REVISION="2024-10-15"             # pin to a stable revision
```

Scopes (Klaviyo private key permissions):
- `accounts:read`, `lists:*`, `segments:*`, `flows:*`, `campaigns:*`, `events:read`, `metrics:read`, `profiles:*`, `templates:*`, `data-privacy:write`

**Tier requirement:** Predictive AI properties (`predicted_clv`, `churn_risk`, `expected_date_of_next_order`, `expected_number_of_orders`, `predicted_aov`) require **Klaviyo Plus** or **Advanced** tier. Free / standard tier does NOT expose these fields. Confirm with the customer before designing flows that depend on them.

## Common recipes

### Recipe 1: Predictive AI churn-risk segment (high-CLV at risk)

```bash
curl -s -X POST "https://a.klaviyo.com/api/segments" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" \
  -H "revision: 2024-10-15" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "type": "segment",
      "attributes": {
        "name": "High-CLV Churn Risk (Predictive)",
        "definition": {
          "condition_groups": [{
            "conditions": [
              {"type": "profile-predictive-analytics",
               "predictive_analytic": "predicted_clv",
               "comparison_type": "greater-than",
               "value": 500},
              {"type": "profile-predictive-analytics",
               "predictive_analytic": "churn_risk",
               "comparison_type": "equals",
               "value": "high"},
              {"type": "profile-marketing-consent",
               "consent": "subscribed"}
            ]
          }]
        }
      }
    }
  }'
```

### Recipe 2: Custom RFM band overlay (warehouse → Klaviyo profile property)

```sql
-- Step 1: compute RFM in Postgres (via postgresql-mcp)
WITH rfm AS (
  SELECT
    customer_id, email,
    NTILE(5) OVER (ORDER BY MAX(order_date) DESC) AS R,
    NTILE(5) OVER (ORDER BY COUNT(*) ASC) AS F,
    NTILE(5) OVER (ORDER BY SUM(total_value) ASC) AS M
  FROM orders WHERE order_date > NOW() - INTERVAL '24 months'
  GROUP BY customer_id, email
)
SELECT
  email,
  CASE
    WHEN R>=4 AND F>=4 AND M>=4 THEN 'Champions'
    WHEN R>=4 AND F<=2 THEN 'New'
    WHEN R>=3 AND F>=3 THEN 'Loyal'
    WHEN R<=2 AND F>=4 AND M>=5 THEN 'Cant Lose Best'
    WHEN R<=2 AND F>=4 AND M>=4 THEN 'At Risk High Value'
    WHEN R<=1 AND F>=3 THEN 'Hibernating'
    WHEN R<=2 AND F<=2 THEN 'About To Sleep'
    ELSE 'Other'
  END AS rfm_band
FROM rfm;
```

```bash
# Step 2: bulk push to Klaviyo via update_profile loop
while IFS=, read -r email band; do
  curl -s -X PATCH "https://a.klaviyo.com/api/profiles/$(curl -s -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" "https://a.klaviyo.com/api/profiles?filter=equals(email,\"$email\")" | jq -r '.data[0].id')" \
    -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" \
    -H "revision: 2024-10-15" \
    -H "Content-Type: application/json" \
    -d "{\"data\":{\"type\":\"profile\",\"attributes\":{\"properties\":{\"rfm_band\":\"$band\"}}}}"
done < rfm_export.csv
```

### Recipe 3: Dynamic dunning flow (escalating incentive by churn risk)

Flow triggered when `churn_risk == high AND predicted_clv > 500`:

```bash
curl -s -X POST "https://a.klaviyo.com/api/flows" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" \
  -H "revision: 2024-10-15" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "type": "flow",
      "attributes": {
        "name": "Dynamic Dunning — High-CLV At Risk",
        "trigger": {"type": "segment", "segment_id": "<churn-risk-segment-id>"},
        "status": "draft",
        "steps": [
          {"type": "email", "delay_seconds": 0,
           "template_id": "<dun-1>",
           "subject_variants": [{"text": "We miss you — here is 10% back"}],
           "smart_send_time": true},
          {"type": "conditional_split",
           "condition": {"type": "metric", "name": "Placed Order", "since": "now-168h"},
           "yes_branch": "exit",
           "no_branch": "continue"},
          {"type": "email", "delay_seconds": 604800,
           "template_id": "<dun-2>",
           "subject_variants": [{"text": "20% off — final invitation"}],
           "smart_send_time": true},
          {"type": "conditional_split",
           "condition": {"type": "profile-property", "property": "predicted_clv", "op": "gt", "value": 1000},
           "yes_branch": "concierge_email",
           "no_branch": "exit"},
          {"type": "email", "delay_seconds": 0,
           "template_id": "<dun-vip>",
           "subject_variants": [{"text": "Personal note from our team"}]}
        ],
        "exit_conditions": ["Placed Order", "Unsubscribed", "Spam Complained"]
      }
    }
  }'
```

### Recipe 4: Smart Send Time at flow-step (not campaign-level)

Smart Send Time per-profile is **disabled by default** on flows. Enable per-step:

```bash
curl -s -X PATCH "https://a.klaviyo.com/api/flow-actions/<flow-action-id>" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" \
  -H "revision: 2024-10-15" \
  -H "Content-Type: application/json" \
  -d '{"data":{"type":"flow-action","attributes":{"smart_send_time":true,"smart_send_time_evaluation_window_hours":24}}}'
```

Klaviyo computes optimal send hour per profile using 12+ months of open/click history. New profiles (< 30d) fall back to global cohort optimal hour.

### Recipe 5: Get post-MPP campaign metrics

```bash
# Klaviyo reporting API — query metrics_aggregation
curl -s -X POST "https://a.klaviyo.com/api/campaign-values-reports" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" \
  -H "revision: 2024-10-15" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "type": "campaign-values-report",
      "attributes": {
        "statistics": ["clicks","click_rate","click_to_open_rate","conversions","conversion_rate","conversion_value","revenue_per_recipient","spam_complaints","spam_complaint_rate","unsubscribe_rate"],
        "timeframe": {"key": "last_90_days"},
        "conversion_metric_id": "<placed-order-metric-id>",
        "filter": "and(equals(send_channel,\"email\"))"
      }
    }
  }' | jq '.data.attributes.results'
```

Alert thresholds (your monitoring layer):
- `spam_complaint_rate > 0.001` (0.10%) → P0 Slack alert
- `click_rate < 0.01` → P1 — content/segment refresh
- `unsubscribe_rate > 0.005` → P1 — frequency/relevance audit
- `revenue_per_recipient` ranking → top-of-list = repeat the format

### Recipe 6: Predictive next-order date → replenishment trigger

```bash
# Segment: profiles with predicted next-order date in next 7 days (consumables)
curl -s -X POST "https://a.klaviyo.com/api/segments" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" \
  -H "revision: 2024-10-15" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {"type":"segment","attributes":{
      "name": "Replenishment Window — Next 7d",
      "definition": {"condition_groups":[{"conditions":[
        {"type":"profile-predictive-analytics",
         "predictive_analytic":"expected_date_of_next_order",
         "comparison_type":"in-the-next",
         "value":7,
         "unit":"days"},
        {"type":"has-placed-order",
         "comparison_type":"at-least","value":2}
      ]}]}
    }}}'
```

### Recipe 7: Predicted-AOV-tiered incentive

```bash
# Three branches: $0-50 AOV → free shipping, $50-150 → 10%, $150+ → 15% + gift
curl -s -X POST "https://a.klaviyo.com/api/flows" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" \
  -H "revision: 2024-10-15" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {"type":"flow","attributes":{
      "name":"AOV-Tiered Cart Recovery",
      "trigger":{"type":"metric","metric_name":"Started Checkout"},
      "steps":[
        {"type":"conditional_split",
         "condition":{"type":"profile-predictive-analytics",
                      "predictive_analytic":"predicted_aov","op":"lt","value":50},
         "yes_branch":"free_ship_email","no_branch":"check_mid"},
        {"type":"conditional_split","id":"check_mid",
         "condition":{"type":"profile-predictive-analytics",
                      "predictive_analytic":"predicted_aov","op":"between","values":[50,150]},
         "yes_branch":"ten_pct_email","no_branch":"fifteen_pct_email"}
      ]
    }}}'
```

### Recipe 8: Webhook ingest of external churn score

If your data team builds a custom churn model (XGBoost on warehouse), push to Klaviyo as a custom profile property:

```python
# python — runs daily as cron / Airflow DAG
import requests, os
from datetime import datetime

API = "https://a.klaviyo.com/api"
HDRS = {
    "Authorization": f"Klaviyo-API-Key {os.environ['KLAVIYO_API_KEY']}",
    "revision": "2024-10-15",
    "Content-Type": "application/json",
}

def upsert(email, churn_score):
    body = {"data": {"type": "profile", "attributes": {
        "email": email,
        "properties": {
            "external_churn_score": churn_score,
            "external_churn_score_updated_at": datetime.utcnow().isoformat()
        }
    }}}
    r = requests.post(f"{API}/profile-import", headers=HDRS, json=body)
    r.raise_for_status()

# Then trigger flow when external_churn_score > 0.7
```

### Recipe 9: Multi-list / multi-currency orchestration

For brands with EU + US + UK lists (different currencies, different consent regimes):

```bash
# Segment by list + currency + locale
curl -s -X POST "https://a.klaviyo.com/api/segments" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" \
  -H "revision: 2024-10-15" \
  -d '{"data":{"type":"segment","attributes":{
    "name":"EU GDPR-compliant subscribers",
    "definition":{"condition_groups":[{"conditions":[
      {"type":"profile-group-membership","group_id":"<eu-list-id>","comparison_type":"is-in"},
      {"type":"profile-property","property":"gdpr_consent","comparison_type":"equals","value":true},
      {"type":"profile-property","property":"currency","comparison_type":"equals","value":"EUR"}
    ]}]}}}}'
```

Per-currency campaigns → render product prices in local currency via Klaviyo template variables `{{ event.line_items.0.price | currency: profile.currency }}`.

## Examples

### Example 1: Build predictive dunning for $2M ARR DTC brand

**Goal:** reduce churn among customers with `predicted_clv > $1000`.

**Steps:**

1. Verify Klaviyo Plus / Advanced tier active:
   ```bash
   curl -s "https://a.klaviyo.com/api/accounts" -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" | jq '.data[0].attributes.subscription'
   ```
2. Create churn-risk segment (Recipe 1).
3. Build flow with conditional escalation (Recipe 3).
4. Enable Smart Send Time per step (Recipe 4).
5. Set 14d revenue attribution window (longer for high-LTV cohorts):
   ```bash
   curl -X PATCH "https://a.klaviyo.com/api/flows/<flow-id>" \
     -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
     -d '{"data":{"type":"flow","attributes":{"revenue_attribution_window_days":14}}}'
   ```
6. After 30d, pull `get_campaign_metrics` per step (Recipe 5). Target: `revenue_per_recipient` of step 3 (VIP branch) > 10× step 1.

**Result:** dunning flow segments by predicted-CLV, escalates incentive only for high-value customers, tracks revenue per step.

### Example 2: Replenishment window for consumables

**Goal:** trigger refill reminder 7d before customer's predicted next purchase.

**Steps:**

1. Create replenishment-window segment (Recipe 6).
2. Build flow with single email + product recommendation block (use `{{ person | predicted_recommendations }}`).
3. Track conversion via `get_campaign_metrics` filtering on `Placed Order` metric.

## Edge cases

- **Predictive properties null for new profiles** — Klaviyo requires ~5 orders OR 6+ months of history per profile before predictive values populate. Always include a fallback branch.
- **Klaviyo revision header is mandatory** — omit `revision: 2024-10-15` and the API returns a 400. Pin the date in your code.
- **Smart Send Time skips profiles with < 30d history** — those fall back to send-now. Don't promise SST for new lists.
- **Profile property updates lag** — `update_profile` writes are eventually consistent. A flow triggered milliseconds after `update_profile` may not see the new value. Add a 60-300s delay step OR use `event` triggers instead.
- **Revenue attribution clobbering** — if multiple flows touch the same profile within attribution window, last-touched wins by default. Override to first-touch per flow:
  ```bash
  curl -X PATCH "https://a.klaviyo.com/api/flows/<id>" -d '{"data":{"type":"flow","attributes":{"revenue_attribution":"first_touch"}}}'
  ```
- **Rate limits** — Klaviyo APIs: 75 req/s burst, 700/min steady for most endpoints. Use `429 Retry-After` header; honor it.
- **Apple MPP inflated `opened_rate`** — 40-60% of Apple Mail users register as "opened" regardless. Never gate flow logic on `opened_rate`; gate on `clicked` instead.

## Sources

- [Klaviyo MCP Server (official)](https://developers.klaviyo.com/en/docs/klaviyo_mcp_server)
- [Klaviyo Predictive Analytics](https://help.klaviyo.com/hc/en-us/articles/360054384451)
- [Klaviyo API reference](https://developers.klaviyo.com/en/reference/api_overview)
- [Klaviyo Smart Send Time](https://help.klaviyo.com/hc/en-us/articles/360050287831)
- [RFM segmentation guide](https://www.klaviyo.com/marketing-resources/rfm-segmentation-guide)
- [Apple Mail Privacy Protection — Klaviyo](https://www.klaviyo.com/blog/apple-mail-privacy-protection)
