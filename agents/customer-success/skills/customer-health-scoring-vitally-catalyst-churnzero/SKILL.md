<!--
Source: https://docs.vitally.io/reference + https://help.catalyst.io/ + https://help.churnzero.com/ + https://help.gainsight.com/ + https://posthog.com/docs/api/queries
-->
# Customer Health Scoring — Vitally / Catalyst / ChurnZero — SKILL

Composite customer health score: feed product-usage + survey + sentiment + sponsor-engagement + renewal-stage signals into Vitally / Catalyst / ChurnZero / Gainsight, read the CSP-computed score back, surface in HubSpot + Slack, fire CSM playbooks on threshold crossings. Differs from the support-agent's `customer-health-scoring-vitally-catalyst` skill (which only feeds support signals); this one owns the full composite + writeback + downstream automation.

## When to use

- **Recipient runs a CSP** — health score is the agent's primary read/write surface.
- **No-CSP shop** — fallback is HubSpot custom property + dbt nightly model + Slack alerting.
- **Threshold-crossing alerts** — score crosses 0.4 (at-risk gate) -> CSM Slack ping.
- **Renewal-readiness signal** — health > 0.7 sustained 90d -> renewal forecast Green.
- **Cohort distribution review** — monthly leadership rollup of health by tier/vertical/CSM.
- **Score validation** — quarterly correlation of score band vs actual churn.

This skill **takes over from** the customer-support-agent's read-only health view: this agent owns the full composite formula + signal ingestion + downstream actions (Slack, Linear save plan, Vitally Playbook trigger).

Trigger phrases: "health score", "compute health", "at-risk threshold", "health drop", "health trend", "Vitally playbook", "Catalyst health", "ChurnZero AI signal".

## Setup

```bash
# Vitally (modern SOTA)
export VITALLY_SUBDOMAIN="acme"
export VITALLY_API_KEY="<key>"

# Catalyst / Totango (enterprise)
export CATALYST_API_KEY="<key>"

# ChurnZero (retention-focused + AI)
export CHURNZERO_API_KEY="<key>"
export CHURNZERO_APP_KEY="<key>"

# Gainsight (enterprise heavy)
export GAINSIGHT_DOMAIN="acme.gainsightcloud.com"
export GAINSIGHT_TOKEN="<token>"

# Custify (SMB)
export CUSTIFY_API_KEY="<key>"

# HubSpot fallback (free)
export HUBSPOT_TOKEN="<pat>"
```

Workspace prerequisites:
- `customer_id` (CRM) mirrored as `external_id` in CSP.
- Slack channel `#cs-at-risk` for threshold alerts.
- Vitally/Catalyst/ChurnZero health model configured with custom traits (`adoption_score`, `nps_recent`, `support_sentiment_90d`, `sponsor_engagement_90d`, `renewal_stage_score`).
- PostHog event taxonomy stable enough to compute adoption_score (`user_action`, `key_feature_used`).

## Composite formula (Round 2 standard)

```
Health = 0.40 * adoption_score
       + 0.20 * csat_nps_recency_score
       + 0.15 * sentiment_score
       + 0.10 * (1 - support_ticket_volume_normalized)
       + 0.10 * exec_sponsor_engagement_score
       + 0.05 * renewal_stage_score
```

Each sub-score on 0-1 scale. Weights tuned by `Recipe 12` quarterly validation.

## Common recipes

### Recipe 1: Compute adoption_score from PostHog

```sql
-- per-customer adoption score (run nightly)
SELECT
  properties.customer_id AS customer_id,
  -- DAU/MAU
  (uniq(distinct_id) FILTER (WHERE timestamp >= now() - INTERVAL 1 DAY) * 1.0
   / nullif(uniq(distinct_id) FILTER (WHERE timestamp >= now() - INTERVAL 30 DAY), 0)) AS dau_mau,
  -- Feature breadth
  uniq(event) FILTER (WHERE event LIKE 'key_feature_%') AS feature_breadth,
  -- Login recency
  exp(- dateDiff('day', max(timestamp), now()) / 30.0) AS login_recency,
  -- Composite
  0.4 * least(1.0,
       (uniq(distinct_id) FILTER (WHERE timestamp >= now() - INTERVAL 1 DAY) * 1.0
        / nullif(uniq(distinct_id) FILTER (WHERE timestamp >= now() - INTERVAL 30 DAY), 0)) / 0.4)
  + 0.3 * least(1.0, uniq(event) FILTER (WHERE event LIKE 'key_feature_%') / 8.0)
  + 0.2 * exp(- dateDiff('day', max(timestamp), now()) / 30.0)
  AS adoption_score
FROM events
WHERE timestamp >= now() - INTERVAL 30 DAY
GROUP BY properties.customer_id;
```

Via `posthog-mcp query`.

### Recipe 2: Push adoption_score trait to Vitally

```bash
curl -sS -X PUT "https://$VITALLY_SUBDOMAIN.rest.vitally.io/resources/accounts/external/$CUSTOMER_ID/traits" \
  -H "Authorization: Basic $(echo -n $VITALLY_API_KEY: | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "adoption_score": 0.62,
    "dau_30d": 18,
    "mau_30d": 47,
    "feature_adoption_score": 0.71,
    "nps_latest": 9,
    "support_tickets_90d": 12,
    "sentiment_90d": 0.78,
    "sponsor_last_seen_days": 6
  }'
```

Doc: https://docs.vitally.io/reference/accounts

### Recipe 3: Read back Vitally-computed health (with breakdown)

```bash
curl -sS "https://$VITALLY_SUBDOMAIN.rest.vitally.io/resources/accounts/external/$CUSTOMER_ID?include=healthScores,traits" \
  -H "Authorization: Basic $(echo -n $VITALLY_API_KEY: | base64)" | jq '{
    name,
    health: .healthScore.score,
    breakdown: [.healthScore.breakdown[] | {name, score, weight}]
  }'
```

### Recipe 4: Push traits to Catalyst

```bash
curl -sS -X PATCH "https://api.catalyst.io/v1/companies/$CUSTOMER_ID/properties" \
  -H "Authorization: Bearer $CATALYST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "adoption_score": 0.62,
      "sentiment_90d": 0.78,
      "support_tickets_90d": 12
    }
  }'
```

Doc: https://help.catalyst.io/

### Recipe 5: ChurnZero AI signal ingestion

```bash
# Push event for ChurnZero AI ingestion
curl -sS -X POST "https://$CHURNZERO_APP_KEY.events.churnzero.net/i" \
  -H "Content-Type: application/json" \
  -d '{
    "appKey": "'$CHURNZERO_APP_KEY'",
    "accountExternalId": "'$CUSTOMER_ID'",
    "eventName": "key_feature_used",
    "eventValue": 42,
    "description": "Aggregated daily key_feature_used count"
  }'

# Pull ChurnZero AI churn-risk score
curl -sS "https://api.churnzero.net/i/v1/accounts/$CUSTOMER_ID/risk_score" \
  -H "Authorization: Bearer $CHURNZERO_API_KEY" | jq '.risk_score, .signals[]'
```

Doc: https://help.churnzero.com/

### Recipe 6: Gainsight Scorecard read

```bash
curl -sS "https://$GAINSIGHT_DOMAIN/v1/api/customer-info/customer/$CUSTOMER_ID?include=health,scorecard" \
  -H "accesskey: $GAINSIGHT_TOKEN" | jq '.data | {
    name,
    health: .currentScorecardScore,
    breakdown: [.scorecardMeasures[] | {name: .measureName, score: .measureScore}]
  }'
```

Gainsight uses "Scorecards" not "Health Scores." Same model, different label.

### Recipe 7: HubSpot fallback (no-CSP shops)

```bash
# Push composite score to HubSpot company custom property
curl -sS -X PATCH "https://api.hubapi.com/crm/v3/objects/companies/$HUBSPOT_COMPANY_ID" \
  -H "Authorization: Bearer $HUBSPOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "cs_health_score": "0.72",
      "cs_health_score_breakdown": "adoption=0.65,survey=0.85,sentiment=0.78,support=0.70,sponsor=0.80,renewal=0.70",
      "cs_health_last_updated": "2026-06-11T02:00:00Z",
      "cs_at_risk": "false"
    }
  }'
```

Doc: https://developers.hubspot.com/docs/api/crm/companies

### Recipe 8: Threshold-crossing detection (nightly Postgres)

```sql
WITH today AS (
  SELECT customer_id, health FROM csp_health_snapshot WHERE snapshot_date = CURRENT_DATE
),
yesterday AS (
  SELECT customer_id, health FROM csp_health_snapshot WHERE snapshot_date = CURRENT_DATE - 1
),
month_ago AS (
  SELECT customer_id, health FROM csp_health_snapshot WHERE snapshot_date = CURRENT_DATE - 30
)
SELECT
  t.customer_id,
  t.health AS today,
  y.health AS yesterday,
  m.health AS month_ago,
  (t.health - m.health) AS trend_30d,
  CASE
    WHEN y.health >= 0.4 AND t.health < 0.4 THEN 'crossed_below_atrisk'
    WHEN (t.health - m.health) <= -0.15 THEN 'sharp_decline_30d'
    WHEN (t.health - m.health) <= -0.05 THEN 'soft_decline_30d'
    WHEN y.health < 0.85 AND t.health >= 0.85 THEN 'crossed_advocate'
    ELSE NULL
  END AS event
FROM today t
LEFT JOIN yesterday y USING(customer_id)
LEFT JOIN month_ago m USING(customer_id)
WHERE CASE
        WHEN y.health >= 0.4 AND t.health < 0.4 THEN TRUE
        WHEN (t.health - m.health) <= -0.05 THEN TRUE
        WHEN y.health < 0.85 AND t.health >= 0.85 THEN TRUE
        ELSE FALSE
      END;
```

For each row, route via Recipe 9.

### Recipe 9: Slack alert with breakdown

```python
# slack-mcp chat_postMessage
text = f"""
:warning: At-risk crossing: {customer_name}
Health: {today:.2f} (was {yesterday:.2f}, {month_ago:.2f} 30d ago)
Trend 30d: {trend_30d:+.2f}
ARR: ${arr:,.0f}
Top drivers down:
- {top_driver_1}
- {top_driver_2}
Renewal: T-{days_to_renewal} days
Owner: {csm_owner}
Save plan: [Linear ENG-{ticket} or "draft via /save"]
"""
slack.chat_postMessage(channel="#cs-at-risk", text=text)
```

### Recipe 10: Cohort distribution report

```sql
SELECT
  tier,
  count(*) AS accounts,
  round(avg(health)::numeric, 2) AS avg_health,
  count(*) FILTER (WHERE health < 0.4) AS red,
  count(*) FILTER (WHERE health BETWEEN 0.4 AND 0.7) AS yellow,
  count(*) FILTER (WHERE health > 0.7) AS green,
  round(100.0 * count(*) FILTER (WHERE health < 0.4) / count(*)::numeric, 1) AS red_pct
FROM csp_health_snapshot
WHERE snapshot_date = CURRENT_DATE
GROUP BY tier
ORDER BY avg_health ASC;
```

Surface in monthly executive report via `xlsx` + `pptx`.

### Recipe 11: Bulk export Vitally accounts to warehouse

```bash
NEXT=""
while true; do
  RESP=$(curl -sS "https://$VITALLY_SUBDOMAIN.rest.vitally.io/resources/accounts?limit=100${NEXT:+&from=$NEXT}&include=healthScores" \
    -H "Authorization: Basic $(echo -n $VITALLY_API_KEY: | base64)")
  echo "$RESP" | jq -c '.results[] | {customer_id: .externalId, name, health: .healthScore.score, snapshot_date: "'$(date -u +%F)'"}' >> snapshot.jsonl
  NEXT=$(echo "$RESP" | jq -r '.next // empty')
  [ -z "$NEXT" ] && break
done
psql -c "\\COPY csp_health_snapshot FROM 'snapshot.jsonl' WITH (FORMAT json)"
```

### Recipe 12: Quarterly score-vs-churn validation

```sql
SELECT
  round(h.health::numeric, 1) AS health_band,
  count(*) AS n,
  count(*) FILTER (WHERE c.churned_at BETWEEN h.snapshot_date AND h.snapshot_date + INTERVAL '90 days') AS churned_90d,
  round(100.0 * count(*) FILTER (WHERE c.churned_at BETWEEN h.snapshot_date AND h.snapshot_date + INTERVAL '90 days') / count(*)::numeric, 1) AS churn_pct
FROM csp_health_snapshot h
LEFT JOIN customers c USING (customer_id)
WHERE h.snapshot_date = CURRENT_DATE - INTERVAL '90 days'
GROUP BY 1 ORDER BY 1;
```

Expected: monotonically decreasing churn_pct as health_band rises. If not, weights need re-tuning.

## Examples

### Example 1: Nightly health pipeline (zero-touch)

**Goal:** Every morning, leadership + CSMs see fresh health distributions and threshold alerts.

**Steps:**
1. 02:00 UTC: Recipe 1 PostHog adoption_score computed.
2. 02:30 UTC: Recipe 2 traits pushed to Vitally.
3. 03:00 UTC: Vitally recomputes health.
4. 03:30 UTC: Recipe 11 bulk export to Postgres `csp_health_snapshot`.
5. 04:00 UTC: Recipe 8 threshold detection.
6. 04:30 UTC: Recipe 9 Slack alerts; Linear save-plan issues auto-created for Red.
7. 08:00 UTC: Recipe 10 morning digest via `gmail-mcp` to leadership.

**Result:** Health-driven workflow runs without manual ops.

### Example 2: Why did Acme drop?

**Goal:** CSM asks "Acme dropped from 0.72 to 0.42 - why?"

**Steps:**
1. Recipe 3 - breakdown shows adoption=0.31 (was 0.68), sentiment=0.42 (was 0.78).
2. Cross-reference PostHog: Recipe 1 - dau_mau crashed from 0.45 to 0.12 starting 2026-05-15.
3. Cross-reference support tickets: 8 SLA-breach tickets 2026-05-12 to 2026-05-20.
4. Hypothesis: post-3.2-release incident hurt usage + sentiment.
5. Auto-create Linear save-plan issue with hypothesis; fire `churn-save-motion-intervention`.

**Result:** Specific diagnosis -> actionable save play.

## Edge cases / gotchas

- **Score scales differ across CSPs** — Vitally 0-1 (or 0-10 depending on workspace), Catalyst 0-100, Gainsight customizable, Custify 0-100. Normalize before cross-tool dashboards.
- **Trait push -> health recompute latency** — Vitally 5-15 min; Catalyst 1-24h; Gainsight nightly. Don't read immediately after push.
- **External ID mismatch** — pushing to `external_id = stripe_cus_abc` only works if CSP has that exact ID. Sync from CRM -> CSP first; audit weekly.
- **Health flapping at threshold** — accounts crossing 0.4 daily. Add 24h persistent debounce on alerts to avoid alert fatigue.
- **Composite formula tuning is not free** — re-weighting changes everyone's score; communicate before deploying.
- **HubSpot fallback assumes CSM lives in CRM** — if CSM team lives in Notion/Slack instead, write to that surface; HubSpot becomes the data sink.
- **Trait override risk** — multiple skills pushing same trait clobber each other. Coordinate: only this skill owns the `adoption_score` trait; only `nps-csat-ces-tracking` owns `nps_latest`.
- **CSP rate limits at scale** — Vitally 100 req/min; Catalyst 1000/hr. Bulk endpoints exist (Recipe 11); use them.
- **Sponsor engagement is hard to measure** — requires login events tagged with role. Without that, fall back to email-reply recency from `gmail-mcp` Send/Reply tracking.
- **Don't show internal score to customer verbatim** — internal 0.42 vs customer-facing "your team's usage dropped 35% after the org change." Translation layer required.
- **CSP score broke its own model** — Recipe 12 validation < 70% correlation -> push back on CSP vendor, re-weight.
- **No CSP, no ChurnZero AI** — composite from Recipes 1 + Stripe + HubSpot + Postgres is genuinely good enough for SMB shops.

## Sources

- [Vitally REST API reference](https://docs.vitally.io/reference)
- [Vitally Health Scores docs](https://docs.vitally.io/en/articles/9901284-health-scores)
- [Catalyst / Totango docs](https://help.catalyst.io/)
- [Totango API v3](https://www.totango.com/docs/api)
- [ChurnZero Plays + AI](https://help.churnzero.com/)
- [Gainsight Connector 2.0](https://support.gainsight.com/gainsight_nxt/Connectors)
- [Gainsight Scorecards](https://support.gainsight.com/gainsight_nxt/Scorecards)
- [Custify API](https://docs.custify.com/)
- [HubSpot Companies API](https://developers.hubspot.com/docs/api/crm/companies)
- [PostHog HogQL Query API](https://posthog.com/docs/api/queries)
- [Vitally - best health score software 2026](https://www.vitally.io/post/the-best-customer-health-tracking-software)
