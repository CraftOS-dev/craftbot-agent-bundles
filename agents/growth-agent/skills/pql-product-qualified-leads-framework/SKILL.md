<!--
Source: Pocus definitive PQL guide + syncgtm Koala review + HockeyStack PLG playbook + Stackmatix PLG metrics
-->
# PQL — Product Qualified Lead Framework SKILL

> Multi-signal PQL scoring model (limit-proximity + feature-depth + team-activity + frequency), CRM/Slack handoff workflow, platform choice (Pocus / Koala / HockeyStack / in-house). The bridge between PLG and sales-led for hybrid motions.

## When to use

Trigger phrases:
- "Build PQL framework"
- "Score product-qualified leads"
- "Pocus vs Koala vs in-house"
- "PQL → pipeline handoff"
- "When to hand off to sales from PLG"
- "Sales-assist on PLG users"

Pair: `free-to-paid-upgrade-prompts` (self-serve path), `expansion-revenue-nrr-optimization` (expansion analog), `plg-vs-sales-led-motion-decision` (motion fit), `behavioral-cohort-design` (audience).

## Setup

```bash
export POSTHOG_PERSONAL_API_KEY="phx_..."
export HUBSPOT_TOKEN="hb_..."
export SALESFORCE_TOKEN="sf_..."
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
export POCUS_API_KEY="pcs_..."
export KOALA_API_KEY="koala_..."
```

## Platform decision matrix (June 2026)

| Tool | PQL scoring | CRM sync | Slack alerts | Intent + Visitor ID | Pricing | Best for |
|---|---|---|---|---|---|---|
| **Pocus** | Best-in-class | HubSpot + SF deep | Yes | Yes | $$$$ (custom enterprise) | Full PLG platform; enterprise |
| **Koala** | Lightweight | HubSpot + SF | Yes | **Best-in-class** intent | $$$ ($1500-3500/mo) | Lighter setup; intent-first |
| **HockeyStack** | + Multi-touch attribution | HubSpot + SF | Yes | Account-level | $$$$ ($3K+/mo) | B2B PLG + attribution unified |
| **In-house (PostHog + curl)** | Custom | Custom curl | Custom | None | Free | Bootstrapped / engineering-rich |
| **Vendr** | Limited | Limited | No | No | Free | Procurement-focused |
| **MadKudu** | ML-driven | HubSpot + SF | Yes | Yes | $$$ | Custom ML scoring fit |
| **Endgame** | PLG full | HubSpot + SF | Yes | Yes | $$$$ | PLG playbook automation |

## PQL signal taxonomy

| Signal type | Examples | Weight (typical, 0-100) |
|---|---|---|
| **Limit proximity** | 80%+ of free-tier cap used | 20-35 |
| **Feature depth** | Premium feature interactions in last 30d | 15-25 |
| **Team activity** | Multiple users from same account active | 15-30 |
| **Frequency** | Active 7+ days / last 30 | 10-20 |
| **Firmographic fit** | ICP match (industry, headcount) | 10-20 |
| **Intent (external)** | Pricing page visits, demo request, competitor research (Koala/Bombora) | 10-20 |
| **Engagement depth** | Activated + advanced features used | 10-15 |

## Common recipes

### Recipe 1: PQL scoring model (HogQL)

```sql
-- Score formula
SELECT
  account_id,
  -- Signal components
  countDistinctIf(person_id, event = 'session_started'
                  AND timestamp >= now() - INTERVAL 7 DAY) AS active_users_7d,
  countIf(event = 'Premium Feature Attempted'
          AND timestamp >= now() - INTERVAL 30 DAY) AS premium_attempts,
  max(properties.usage_pct) AS max_usage_pct,
  countDistinctIf(event = 'Integration Connected'
                  AND timestamp >= now() - INTERVAL 90 DAY) AS integrations_connected,
  -- Weighted score (0-100)
  least(100,
    (max_usage_pct >= 80) * 25 +
    least(premium_attempts * 5, 25) +
    least(active_users_7d * 8, 30) +
    least(integrations_connected * 4, 20)
  ) AS pql_score
FROM events
WHERE timestamp >= now() - INTERVAL 90 DAY
GROUP BY account_id
HAVING pql_score >= 50
ORDER BY pql_score DESC
```

### Recipe 2: Weight tuning via Cox PH on past closed-won

```python
from lifelines import CoxPHFitter
import pandas as pd

# Load: features + days_to_closed_won + closed_won_event
df = pd.read_sql("""
  SELECT
    account_id,
    DATEDIFF('day', became_pql_at, COALESCE(closed_won_at, CURRENT_DATE)) AS tenure_days,
    CASE WHEN closed_won_at IS NOT NULL THEN 1 ELSE 0 END AS closed_won,
    usage_pct,
    premium_attempts,
    active_users_7d,
    integrations_connected,
    firmographic_fit_score,
    intent_score
  FROM pql_history
""", db)

cph = CoxPHFitter()
cph.fit(df, duration_col='tenure_days', event_col='closed_won')
cph.print_summary()

# Use hazard ratios as weights for PQL formula
# HR > 1 (positive coef) → feature predicts faster close → higher weight
```

### Recipe 3: PQL threshold tuning

```python
# Try multiple thresholds; pick one with best precision × recall × volume
for threshold in [50, 60, 70, 80]:
    pqls = df[df.pql_score >= threshold]
    precision = pqls.closed_won.mean()
    recall = pqls.closed_won.sum() / df.closed_won.sum()
    volume = len(pqls)
    print(f"T={threshold}: precision={precision:.2f}, recall={recall:.2f}, n={volume}")
```

Choose threshold where precision > 30% (AE time is finite) AND volume manageable (< 50/wk per AE typical).

### Recipe 4: PQL → CRM handoff (HubSpot)

```bash
# When score crosses threshold, create HubSpot contact + deal
curl -X POST "https://api.hubapi.com/crm/v3/objects/contacts" \
  -H "Authorization: Bearer $HUBSPOT_TOKEN" \
  -d '{
    "properties": {
      "email": "user@acme.com",
      "company": "Acme",
      "pql_score": "78",
      "pql_signals": "limit_90pct,5_users_active,3_premium_attempts",
      "hubspot_owner_id": "<AE_id>",
      "lifecyclestage": "marketingqualifiedlead"
    }
  }'

curl -X POST "https://api.hubapi.com/crm/v3/objects/deals" \
  -H "Authorization: Bearer $HUBSPOT_TOKEN" \
  -d '{
    "properties": {
      "dealname": "Acme PQL Inbound",
      "pipeline": "default",
      "dealstage": "qualifiedtobuy",
      "amount": "12000",
      "closedate": "2026-09-15"
    }
  }'
```

### Recipe 5: Slack alert to AE

```bash
curl -X POST "$SLACK_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "New PQL: Acme Corp",
    "blocks": [
      {"type": "header", "text": {"type": "plain_text", "text": "PQL Alert: Acme Corp"}},
      {"type": "section", "text": {"type": "mrkdwn",
        "text": "*Score:* 78\n*Signals:* 90% usage, 5 active users, 3 premium attempts\n*Assigned AE:* @jane"}},
      {"type": "actions", "elements": [
        {"type": "button", "text": {"type": "plain_text", "text": "View in HubSpot"},
         "url": "https://app.hubspot.com/contacts/123/deal/45"}
      ]}
    ]
  }'
```

### Recipe 6: Pocus integration (managed)

```bash
# Pocus pulls product data + scores + syncs to CRM/Slack
curl -X POST "https://api.pocus.com/v1/playbooks" \
  -H "Authorization: Bearer $POCUS_API_KEY" \
  -d '{
    "name": "High-fit PQL outreach",
    "audience": {
      "signals": {"and": [
        {"signal": "approached_usage_limit", "min_strength": "high"},
        {"signal": "multi_user_activity", "min_count": 3},
        {"signal": "premium_feature_interest", "min_count": 2}
      ]}
    },
    "actions": [
      {"type": "create_deal_hubspot", "owner": "AE_assignment_rules"},
      {"type": "slack_alert", "channel": "#sales-pql"},
      {"type": "enrich_clearbit"}
    ]
  }'
```

### Recipe 7: Koala (visitor + intent first)

```bash
# Koala identifies anonymous visitors via reverse-lookup IP → account
curl -X POST "https://api.getkoala.com/v1/identify" \
  -H "Authorization: Bearer $KOALA_API_KEY" \
  -d '{
    "user_id": "u_abc",
    "traits": {"email": "user@acme.com"},
    "session_data": {"visited_pages": ["/pricing", "/security"]}
  }'

# Koala enriches; sync visit signals to PostHog as cohort properties
```

### Recipe 8: ICP firmographic enrichment

```python
# Enrich user → account → firmographics (Clearbit / Apollo)
import requests
def enrich_user(email):
    resp = requests.get(
        f"https://person.clearbit.com/v2/people/find?email={email}",
        headers={"Authorization": f"Bearer {CLEARBIT_TOKEN}"}
    )
    person = resp.json()
    return {
        "company": person.get("employment", {}).get("name"),
        "headcount": person.get("employment", {}).get("company", {}).get("metrics", {}).get("employees"),
        "industry": person.get("employment", {}).get("company", {}).get("category", {}).get("industry"),
        "country": person.get("location")
    }

# Multiply PQL behavioral score by firmographic fit (0-1.0)
# Final PQL = behavioral × firmographic_fit
```

### Recipe 9: Measure PQL→pipeline→closed-won funnel

```sql
SELECT
  pql_month,
  COUNT(*) AS pqls_created,
  COUNT(deal_id) AS deals_opened,
  COUNT(deal_id) FILTER (WHERE deal_stage = 'closedwon') AS closed_won,
  SUM(deal_amount) FILTER (WHERE deal_stage = 'closedwon') AS revenue
FROM pql_to_pipeline
GROUP BY pql_month
ORDER BY pql_month DESC
```

Track:
- PQL → opportunity rate (good: > 60%)
- Opportunity → closed-won (good: > 30%)
- Time-to-close from PQL (good: < 45 days)
- Revenue per PQL (use to justify investment in PQL system)

### Recipe 10: AE assignment + SLA

```python
# Round-robin or territory-based AE assignment
def assign_ae(pql):
    # ICP match wins; round-robin if multiple match
    if pql.firmographic_fit_score > 0.7:
        return ae_pool.get_by_territory(pql.country, pql.industry)
    return ae_pool.round_robin()

# SLA: first-touch within 1 business hour for high-score PQLs
# Slack alert + 60-min escalation if untouched
```

### Recipe 11: PQL feedback loop

```text
1. AE works the PQL → wins or loses.
2. Mark in CRM: pql_won=true OR pql_lost_reason='bad_fit'/'no_budget'/'competitor'/'timing'
3. Quarterly: retrain PQL scoring weights using Cox PH on past 90 days of outcomes (Recipe 2).
4. Continuously improve precision.
```

## Examples

### Example 1: B2B SaaS PLG, want sales-assist on enterprise tier

Plan:
1. Define PQL signal set (Recipe 1) — limit, premium, team, integrations.
2. Threshold at 65 (tune via Recipe 3 once baseline data).
3. Pocus for full management OR in-house (PostHog → HubSpot curl + Slack).
4. AE SLA: 1 business hour first touch.
5. Track funnel Recipe 9. Iterate quarterly.

### Example 2: Bootstrapped startup

In-house, no vendor. PostHog HogQL scoring (Recipe 1) → HubSpot curl (Recipe 4) → Slack webhook (Recipe 5).

Cost: $0 incremental.

### Example 3: Hybrid motion (PLG + sales-led for enterprise)

Tier 1 (small accounts < $500/mo) → automated free-to-paid via `free-to-paid-upgrade-prompts`.
Tier 2 (mid > $500/mo signal) → PQL → AE-assist for upgrade.
Tier 3 (enterprise > $5K/mo signal) → PQL → AE-owned + custom proposal.

## Edge cases / gotchas

- **PQL ≠ MQL** — MQL = marketing-generated signals (downloaded ebook). PQL = product behavior. Different funnel; don't blend.
- **Single-signal PQL is bad** — "user hit limit" alone is too noisy. Multi-signal scoring is required.
- **PQL score inflation** — easy threshold = AE drowning in low-quality. Tighten until precision > 30%.
- **AE-buy-in matters** — if AE doesn't trust PQL signals, they ignore. Train + share outcome data.
- **Same user multiple accounts** — dedupe by email + company; PQL is per-account, not per-user.
- **PQL score decay** — score should drop if signals not refreshed. Recompute daily.
- **Privacy + GDPR — visitor identification** — Koala / Clearbit have legal requirements; check region.
- **Firmographic fit not predictive at all sizes** — for small-business tools, headcount irrelevant. Validate per-product.
- **Owner not present for handoff** — if user is buyer, hand to AE; if user is end-user, find buyer in account first.
- **In-house Slack alert noise** — too many alerts → ignored. Threshold high; daily digest for mid-tier.
- **Bot-driven false positives** — usage from bots inflates limit signals. Filter bot UAs.

## Sources

- Pocus — Definitive PQL guide: https://www.pocus.com/blog/the-definitive-pql-guide-part-1
- syncgtm — Koala review: https://syncgtm.com/blog/koala-review
- HockeyStack PLG manual: https://www.hockeystack.com/resources/manual/plg-product-led-growth
- Pocus: https://www.pocus.com/
- Koala: https://www.getkoala.com/
- MadKudu: https://www.madkudu.com/
- Endgame: https://endgame.io/
- HubSpot deals API: https://developers.hubspot.com/docs/api/crm/deals
- Salesforce REST API: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/
- Stackmatix PLG metrics: https://www.stackmatix.com/blog/plg-funnel-metrics
