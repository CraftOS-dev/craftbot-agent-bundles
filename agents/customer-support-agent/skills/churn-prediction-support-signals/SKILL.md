<!--
Source: https://docs.vitally.io/reference + https://help.catalyst.io/api + Totango
-->
# Churn Prediction — Support Signals — SKILL

Feed support signals (ticket volume, sentiment trend, SLA breaches, last bug-encounter) into CSPs (Vitally / Catalyst / ChurnZero / Gainsight / Totango) so a declining health score fires a CSM playbook. Free fallback: HubSpot custom property + dbt model.

## When to use

- **Recipient has a paid CSP** — Vitally / Catalyst / ChurnZero / Totango / Gainsight / Custify / Velaris.
- **Free-tier shop** — falls back to HubSpot or Salesforce custom properties + warehouse-computed scores.
- **At-risk flagging** — push thresholds (score < 0.4, declining > 0.1 in 30d, > 3 SLA breaches in 30d) into CSP triggers.
- **Per-customer support metrics push** — `support_tickets_90d`, `avg_csat`, `sla_breach_count`, `last_bug_at`, `sentiment_trend_30d`.
- **Bidirectional sync** — read CSP-computed health score back; surface in CRM.

Trigger phrases: "churn risk", "at-risk customers", "push support metrics to Vitally", "health score export", "customer success feed".

## Setup

```bash
# Vitally
curl -sS "https://$VITALLY_SUBDOMAIN.rest.vitally.io/resources/accounts" \
  -H "Authorization: Basic $(echo -n $VITALLY_API_KEY: | base64)"

# Catalyst (Totango)
curl -sS https://api.totango.com/api/v1/accounts \
  -H "app-token: $TOTANGO_APP_TOKEN"

# ChurnZero
curl -sS https://api1.churnzero.net/i \
  -H "Content-Type: application/json"

# HubSpot fallback
curl -sS https://api.hubapi.com/crm/v3/properties/companies \
  -H "Authorization: Bearer $HUBSPOT_TOKEN"
```

Auth + env:
- `VITALLY_SUBDOMAIN` + `VITALLY_API_KEY` — at `Settings > API`. Uses basic auth (`api_key:` with trailing colon).
- `TOTANGO_APP_TOKEN` — at `Settings > Integrations > API`. Catalyst is now part of Totango (June 2026).
- `CHURNZERO_APP_KEY` + `CHURNZERO_API_KEY` — at `Application Settings > Integrations`.
- `GAINSIGHT_TOKEN` — at `Administration > Connectors > Connector 2.0`.
- `HUBSPOT_TOKEN` — for free fallback.

Workspace prerequisites:
- CSP customer records keyed on a stable ID (Stripe customer ID, internal account ID).
- Custom traits / properties defined: `support_tickets_90d` (int), `avg_csat_90d` (float), `sla_breach_count_90d` (int), `last_bug_at` (date), `sentiment_trend_30d` (float — delta).

## Common recipes

### Recipe 1: Push support traits to Vitally

```bash
curl -sS -X PUT "https://$VITALLY_SUBDOMAIN.rest.vitally.io/resources/accounts/external/$EXTERNAL_ID" \
  -H "Authorization: Basic $(echo -n $VITALLY_API_KEY: | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Acme Corp",
    "traits":{
      "support_tickets_90d":18,
      "avg_csat_90d":3.8,
      "sla_breach_count_90d":2,
      "last_bug_at":"2026-06-03T14:00:00Z",
      "sentiment_trend_30d":-0.08
    }
  }'
```

Vitally uses `traits` for custom fields. `external/$EXTERNAL_ID` looks up by your CRM's account ID.

### Recipe 2: Read account health score back from Vitally

```bash
curl -sS "https://$VITALLY_SUBDOMAIN.rest.vitally.io/resources/accounts/external/$EXTERNAL_ID?include=healthScores" \
  -H "Authorization: Basic $(echo -n $VITALLY_API_KEY: | base64)" | jq '{
    name: .name,
    overall_health: .healthScore.score,
    drivers: .healthScore.breakdown[] | {name, score}
  }'
```

`healthScore.score` is 0-10 (NOT 0-100). Drivers show which sub-scores contributed.

### Recipe 3: Push customer to Totango / Catalyst

```bash
curl -sS -X POST "https://api.totango.com/api/v1/accounts/$ACCOUNT_ID" \
  -H "app-token: $TOTANGO_APP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "service_id":"svc_main",
    "account_id":"acc_acme",
    "attributes":{
      "Support Tickets 90d":18,
      "Avg CSAT":3.8,
      "SLA Breaches":2,
      "Last Bug Encounter":"2026-06-03"
    }
  }'
```

Totango attribute names are case- and space-sensitive — exact match to dashboard definitions.

### Recipe 4: Push event to ChurnZero (for activity-based scoring)

```bash
curl -sS -X POST "https://api1.churnzero.net/i" \
  -H "Content-Type: application/json" \
  -d "{
    \"appKey\":\"$CHURNZERO_APP_KEY\",
    \"accountExternalId\":\"acc_acme\",
    \"contactExternalId\":\"user_jane\",
    \"action\":\"track\",
    \"eventName\":\"Support Ticket Escalated\",
    \"description\":\"Bug ENG-1234 escalated\"
  }"
```

ChurnZero is event-stream-oriented (vs Vitally's trait-snapshot). Use Recipe 4 for high-frequency events; Recipe 1-3 for nightly rollups.

### Recipe 5: HubSpot fallback — push to custom company property

```bash
# 1. Ensure properties exist (one-time)
curl -sS -X POST https://api.hubapi.com/crm/v3/properties/companies \
  -H "Authorization: Bearer $HUBSPOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"support_health_score",
    "label":"Support Health Score",
    "type":"number",
    "groupName":"customersuccessinformation"
  }'

# 2. Update per-company
curl -sS -X PATCH "https://api.hubapi.com/crm/v3/objects/companies/$COMPANY_ID" \
  -H "Authorization: Bearer $HUBSPOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "properties":{
      "support_health_score":0.78,
      "support_tickets_90d":18,
      "support_sla_breaches_90d":2
    }
  }'
```

Costs $0 incremental beyond your HubSpot subscription.

### Recipe 6: Compute support-driven health score (dbt model)

```sql
-- models/support_health.sql
WITH per_account AS (
  SELECT
    account_id,
    COUNT(*) FILTER (WHERE created_at >= NOW() - INTERVAL '90 days') AS tickets_90d,
    AVG(score) FILTER (WHERE survey_type='csat' AND responded_at >= NOW() - INTERVAL '90 days') AS avg_csat,
    COUNT(*) FILTER (WHERE breached_at IS NOT NULL AND created_at >= NOW() - INTERVAL '90 days') AS sla_breaches,
    MAX(created_at) FILTER (WHERE topic_tag = 'topic-bug') AS last_bug_at,
    AVG(sentiment_score) FILTER (WHERE scored_at >= NOW() - INTERVAL '30 days') -
      AVG(sentiment_score) FILTER (WHERE scored_at >= NOW() - INTERVAL '60 days' AND scored_at < NOW() - INTERVAL '30 days') AS sentiment_trend
  FROM support.unified_tickets
  GROUP BY account_id
)
SELECT
  account_id,
  tickets_90d,
  avg_csat,
  sla_breaches,
  last_bug_at,
  sentiment_trend,
  -- composite per role.md formula (support-only subscore)
  GREATEST(0, LEAST(1,
    0.40 * COALESCE(avg_csat/5, 0.5)
    + 0.30 * (1 - LEAST(sla_breaches::float/5, 1))
    + 0.20 * (1 - LEAST(tickets_90d::float/30, 1))
    + 0.10 * CASE WHEN sentiment_trend > 0 THEN 1 WHEN sentiment_trend < -0.1 THEN 0 ELSE 0.5 END
  )) AS support_health_score
FROM per_account;
```

Run dbt nightly; pushes to Vitally / HubSpot via Recipes 1+5.

### Recipe 7: Risk-flag detection query

```sql
-- At-risk customers per role.md thresholds
SELECT
  account_id,
  support_health_score,
  sla_breaches,
  sentiment_trend
FROM support_health
WHERE support_health_score < 0.4
   OR sla_breaches > 3
   OR sentiment_trend < -0.1
ORDER BY support_health_score ASC;
```

### Recipe 8: Slack alert for new at-risk

```bash
# Daily cron — diff today's at-risk list against yesterday's, alert on additions
NEW=$(psql -tA <<SQL
SELECT account_id FROM support_health WHERE support_health_score < 0.4
EXCEPT
SELECT account_id FROM support_health_snapshot_yesterday;
SQL
)
if [ -n "$NEW" ]; then
  mcp tool slack.chat_postMessage \
    --channel '#csm-at-risk' \
    --text "New at-risk customers today: $NEW. Run \`gcp account <id>\` for context."
fi
```

### Recipe 9: Bulk batch push (nightly)

```bash
# All account traits in one cron pass
psql -tA -c "SELECT row_to_json(t) FROM (SELECT * FROM support_health) t" | while read row; do
  EXT_ID=$(echo "$row" | jq -r '.account_id')
  TRAITS=$(echo "$row" | jq '{
    support_tickets_90d: .tickets_90d,
    avg_csat_90d: .avg_csat,
    sla_breach_count_90d: .sla_breaches,
    sentiment_trend_30d: .sentiment_trend,
    support_health_score: .support_health_score
  }')
  curl -sS -X PUT "https://$VITALLY_SUBDOMAIN.rest.vitally.io/resources/accounts/external/$EXT_ID" \
    -H "Authorization: Basic $(echo -n $VITALLY_API_KEY: | base64)" \
    -H "Content-Type: application/json" \
    -d "{\"traits\":$TRAITS}"
done
```

Rate-limit pace: 5 req/sec to Vitally; 10 to HubSpot.

### Recipe 10: Configure Vitally Playbook trigger

Vitally Playbooks fire when traits cross thresholds. Configure once at `Settings > Playbooks > New > Trigger: account.healthScore < 5`. The agent's job is to push the trait — Vitally fires the CSM action.

### Recipe 11: Per-tier risk segmentation

```sql
SELECT
  CASE
    WHEN tier = 'enterprise' THEN 'enterprise'
    WHEN tier = 'growth' THEN 'growth'
    ELSE 'other'
  END AS segment,
  COUNT(*) FILTER (WHERE support_health_score < 0.4) AS at_risk,
  COUNT(*) AS total,
  ROUND(100 * COUNT(*) FILTER (WHERE support_health_score < 0.4)::float / COUNT(*), 1) AS pct
FROM support_health
JOIN crm.customers USING (account_id)
GROUP BY 1;
```

If enterprise at-risk pct > growth at-risk pct → escalate to leadership (enterprise churn is existential).

### Recipe 12: Read churn outcome back (for model validation)

```sql
-- Did flagged at-risk customers churn at higher rates?
SELECT
  CASE WHEN s.support_health_score < 0.4 THEN 'at_risk' ELSE 'healthy' END AS bucket,
  COUNT(*) AS n,
  SUM(CASE WHEN c.churned_at IS NOT NULL THEN 1 ELSE 0 END)::float / COUNT(*) AS churn_rate
FROM support_health s
JOIN crm.customers c USING (account_id)
WHERE s.computed_at < NOW() - INTERVAL '90 days'
GROUP BY 1;
```

If at-risk churn rate isn't materially higher than healthy → model is broken; retune weights.

## Examples

### Example 1: Nightly support-health → Vitally push

**Goal:** Vitally always has fresh support metrics within 24h.

**Steps:**
1. dbt model runs at 02:00 UTC, recomputing `support_health` (Recipe 6).
2. Loop pushes traits to Vitally via Recipe 9.
3. Vitally health score updates within minutes.
4. Vitally Playbook (Recipe 10) fires for newly-crossed accounts.
5. CSMs see at-risk in their morning queue.

**Result:** Support signals integrated into CSM workflows zero-touch.

### Example 2: Free-tier shop with HubSpot only

**Goal:** Shop has no CSP budget; surface at-risk in HubSpot.

**Steps:**
1. dbt model computes `support_health_score` (Recipe 6).
2. Push to HubSpot company property via Recipe 5 (nightly).
3. HubSpot workflow: when `support_health_score < 0.4` AND `lifecycle_stage = customer` → notify owner.
4. Recipe 8 daily Slack alert on new at-risk.

**Result:** Same outcome (CSM sees at-risk in workflow) without paying for a CSP.

## Edge cases / gotchas

- **Vitally subdomain matters** — `$VITALLY_SUBDOMAIN.rest.vitally.io` is per-tenant. Common 401 if you use a wrong subdomain.
- **Trait naming conflicts** — pushing `support_tickets_90d` overwrites whatever was there. Coordinate trait schema with the CSP owner.
- **Vitally / Totango / ChurnZero / Gainsight all model health DIFFERENTLY** — Vitally uses 0-10 weighted-average; Totango uses 0-100; ChurnZero is event-driven; Gainsight is config-heavy. Don't expect parity across CSPs.
- **Catalyst is Totango (2024 acquisition)** — Catalyst's old API still works (with `help.catalyst.io` docs); new development happens on the Totango surface.
- **HubSpot deal-stage tied to score is misleading** — a customer in `renewal` stage with health 0.3 is at-risk; a customer in `discovery` with health 0.3 is normal. Filter on `lifecycle_stage`.
- **External ID stability** — if Stripe IDs change (rare but happens), match-by-email becomes the safety net. Maintain both.
- **Rate limits** — Vitally: 100 req/min; Totango: 60 req/min; ChurnZero: 1000 events/min; HubSpot: 100 req/10s (free), 250 (paid).
- **Backfilling churn is bidirectional** — push score → CSP, read CSP-computed health back. Both should match within 0.05 if you implemented correctly.
- **Sentiment trend can flip noisily** — small ticket-count cohorts (n<5) give noisy sentiment_trend. Apply n-threshold gating.
- **Support-only signal ≠ full health** — product usage matters more than support volume for predicting churn. Don't claim "we predict churn from support signals" without product-usage signals layered in.
- **Don't game the health score** — if a CSM dashboards on "health score", agents may stop tagging bugs to keep counts low. Watch for behavioral distortion.

## Sources

- [Vitally REST API — Accounts](https://docs.vitally.io/en/articles/9880654-rest-api-accounts)
- [Vitally Health Scores docs](https://docs.vitally.io/en/articles/9901284-health-scores)
- [Catalyst (now Totango) API](https://help.catalyst.io/)
- [Totango Activity API](https://www.totango.com/docs/api/)
- [ChurnZero Tracking API](https://help.churnzero.com/hc/en-us/articles/360004683652-Tracking-API-Reference)
- [HubSpot CRM v3 — Properties](https://developers.hubspot.com/docs/api/crm/properties)
- [Best customer health score software 2026 (Vitally)](https://www.vitally.io/post/the-best-customer-health-tracking-software)
