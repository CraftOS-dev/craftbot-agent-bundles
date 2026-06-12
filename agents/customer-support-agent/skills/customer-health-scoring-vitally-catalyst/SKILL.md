<!--
Source: https://docs.vitally.io/reference + https://help.catalyst.io/
-->
# Customer Health Scoring — Vitally + Catalyst — SKILL

Bidirectional integration with a CSP for health-score-driven workflows. Push support signals in, read CSP-computed health back, surface in HubSpot / Slack, fire CSM playbooks on threshold crossings. Covers Vitally (modern SaaS), Catalyst/Totango (enterprise), Gainsight (enterprise complex), Custify (SMB), with HubSpot-only fallback.

## When to use

- **Recipient runs a CSP** and needs support signals woven into their health model.
- **Cross-tool surfacing** — health score written back to HubSpot/Salesforce so sales sees it on the deal.
- **Threshold-driven Slack alerts** — health crosses 0.4 → CSM ping.
- **Per-cohort segmentation** — enterprise-tier health distribution this week.
- **Validation** — score correlation with churn outcomes (model quality).

This skill **complements** `churn-prediction-support-signals` — that skill defines support-trait push; this skill defines the bidirectional read + threshold orchestration.

Trigger phrases: "health score", "Vitally playbook", "Catalyst health", "at-risk threshold", "CSP integration".

## Setup

```bash
# Vitally (primary modern)
export VITALLY_SUBDOMAIN="acme"
export VITALLY_API_KEY="<key>"

# Totango / Catalyst (enterprise)
export TOTANGO_APP_TOKEN="<token>"

# Gainsight (enterprise complex)
export GAINSIGHT_DOMAIN="acme.gainsightcloud.com"
export GAINSIGHT_TOKEN="<token>"

# Custify (SMB)
export CUSTIFY_API_KEY="<key>"

# HubSpot fallback
export HUBSPOT_TOKEN="<pat>"
```

Workspace prerequisites:
- Per-account stable ID: `account_id` from CRM, mirrored as `external_id` in CSP.
- Health model configured in CSP (Vitally Health Scores; Totango Health Adoption; Gainsight Scorecards).
- A `Slack` integration / webhook for CSP playbook actions.

## Common recipes

### Recipe 1: Read account health from Vitally

```bash
curl -sS "https://$VITALLY_SUBDOMAIN.rest.vitally.io/resources/accounts/external/$EXTERNAL_ID?include=healthScores,traits" \
  -H "Authorization: Basic $(echo -n $VITALLY_API_KEY: | base64)" | jq '{
    name: .name,
    health: .healthScore.score,
    breakdown: [.healthScore.breakdown[] | {name, score, weight}]
  }'
```

`breakdown` shows sub-score components (e.g., adoption, support, sentiment). Useful for "why did this customer drop?"

### Recipe 2: List at-risk accounts (Vitally)

```bash
# Vitally exposes pre-filtered segments
curl -sS "https://$VITALLY_SUBDOMAIN.rest.vitally.io/resources/segments/$AT_RISK_SEGMENT_ID/accounts" \
  -H "Authorization: Basic $(echo -n $VITALLY_API_KEY: | base64)" | jq '.results[] | {name, healthScore: .healthScore.score, mrr}'
```

Define the segment once in Vitally UI; pull membership via API.

### Recipe 3: Read health from Totango / Catalyst

```bash
curl -sS "https://api.totango.com/api/v3/accounts/$ACCOUNT_ID?fields=health,total_health_score,health_drivers" \
  -H "app-token: $TOTANGO_APP_TOKEN" | jq '.'
```

Totango health is 0-100 (vs Vitally 0-10). Normalize before comparing.

### Recipe 4: Read health from Gainsight

```bash
# Gainsight uses Connector 2.0 with Bearer auth + GraphQL surface
curl -sS "https://$GAINSIGHT_DOMAIN/v1/api/customer-info/customer/$ACCOUNT_ID?include=health" \
  -H "accesskey: $GAINSIGHT_TOKEN" | jq '.data | {name, health: .currentScorecardScore, breakdown: .scorecardMeasures[]}'
```

Gainsight uses "Scorecards" not "Health Scores" — terminology shift.

### Recipe 5: Write health back to HubSpot

```bash
curl -sS -X PATCH "https://api.hubapi.com/crm/v3/objects/companies/$HUBSPOT_COMPANY_ID" \
  -H "Authorization: Bearer $HUBSPOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "properties":{
      "csp_health_score":7.5,
      "csp_health_score_drivers":"adoption=8,support=6,sentiment=8",
      "csp_health_last_updated":"2026-06-09T02:00:00Z"
    }
  }'
```

Surface in HubSpot deals/companies; sales sees on hover.

### Recipe 6: Threshold-crossing alert (Vitally → Slack via dbt model)

```sql
-- Daily snapshot of crossings
WITH today AS (
  SELECT account_id, health FROM csp_health_snapshot WHERE snapshot_date = CURRENT_DATE
),
yesterday AS (
  SELECT account_id, health FROM csp_health_snapshot WHERE snapshot_date = CURRENT_DATE - 1
)
SELECT t.account_id, y.health AS yesterday_health, t.health AS today_health
FROM today t JOIN yesterday y USING(account_id)
WHERE y.health >= 4.0 AND t.health < 4.0;  -- crossed below the at-risk gate
```

For each row, `slack-mcp chat_postMessage` to `#csm-at-risk` with the account name + drivers.

### Recipe 7: Bulk export health snapshot to warehouse

```bash
# Iterate Vitally accounts in pages of 100
NEXT=""
while true; do
  RESP=$(curl -sS "https://$VITALLY_SUBDOMAIN.rest.vitally.io/resources/accounts?limit=100${NEXT:+&from=$NEXT}&include=healthScores" \
    -H "Authorization: Basic $(echo -n $VITALLY_API_KEY: | base64)")
  echo "$RESP" | jq -c '.results[] | {account_id: .externalId, health: .healthScore.score, name}' >> snapshot.jsonl
  NEXT=$(echo "$RESP" | jq -r '.next // empty')
  [ -z "$NEXT" ] && break
done

# Bulk load into Postgres
psql -c "\\COPY csp_health_snapshot FROM 'snapshot.jsonl' WITH (FORMAT json)"
```

Schedule daily. Enables trending + cohort analysis in BI.

### Recipe 8: Vitally Playbook trigger (CSP-side config)

```yaml
# Set in Vitally UI under Playbooks > New:
trigger:
  field: account.healthScore
  operator: <
  value: 4.0
  duration: persistent_24h   # avoids flapping
actions:
  - create_task:
      assignee: account.csm
      title: "[At-risk] {{account.name}} dropped below 4.0"
      due_in_days: 1
  - slack_message:
      channel: "#csm-at-risk"
      template: "Account {{account.name}} ({{account.mrr}} MRR) crossed the at-risk gate."
```

This lives in Vitally — the agent's job is to push traits + read drivers, not to manage Playbooks via API.

### Recipe 9: Per-cohort distribution (BI query)

```sql
SELECT
  tier,
  ROUND(AVG(health), 2) AS avg_health,
  COUNT(*) AS total,
  SUM(CASE WHEN health < 4.0 THEN 1 ELSE 0 END) AS at_risk,
  ROUND(100.0 * SUM(CASE WHEN health < 4.0 THEN 1 ELSE 0 END) / COUNT(*), 1) AS at_risk_pct
FROM csp_health_snapshot
JOIN crm.accounts USING (account_id)
WHERE snapshot_date = CURRENT_DATE
GROUP BY tier;
```

Use for monthly leadership review.

### Recipe 10: Health-by-CSM (workload + outcome)

```sql
SELECT
  c.csm_owner,
  COUNT(*) AS accounts,
  ROUND(AVG(h.health), 2) AS avg_health,
  SUM(CASE WHEN h.health < 4.0 THEN 1 ELSE 0 END) AS at_risk
FROM csp_health_snapshot h
JOIN crm.accounts c USING (account_id)
WHERE snapshot_date = CURRENT_DATE
GROUP BY c.csm_owner
ORDER BY avg_health ASC;
```

CSMs with lowest avg health may need book balance, not blame. Use as workload signal.

### Recipe 11: Validation — score vs churn outcome (90d lookback)

```sql
SELECT
  ROUND(h.health, 0) AS health_band,
  COUNT(*) AS n,
  SUM(CASE WHEN c.churned_at BETWEEN h.snapshot_date AND h.snapshot_date + INTERVAL '90 days' THEN 1 ELSE 0 END) AS churned_within_90d,
  ROUND(100.0 * SUM(CASE WHEN c.churned_at BETWEEN h.snapshot_date AND h.snapshot_date + INTERVAL '90 days' THEN 1 ELSE 0 END) / COUNT(*), 1) AS churn_pct
FROM csp_health_snapshot h
LEFT JOIN crm.accounts c USING (account_id)
WHERE h.snapshot_date = CURRENT_DATE - INTERVAL '90 days'
GROUP BY 1 ORDER BY 1;
```

Expected pattern: monotonically decreasing churn_pct as health_band increases. If not, the CSP model is broken.

### Recipe 12: Surface in CRM workflow (HubSpot)

```bash
# Inside HubSpot, configure a Workflow:
#   Trigger: companies where csp_health_score < 4 AND lifecycle_stage = customer
#   Action 1: Send Slack to CSM-owner
#   Action 2: Create task "Health check call within 48h"
#   Action 3: Update deal stage if renewal-quarter
```

The agent doesn't operate HubSpot Workflows but should know they exist and surface the configuration via runbook.

## Examples

### Example 1: End-to-end nightly health pipeline

**Goal:** Every morning, leadership + CSMs see fresh health distributions.

**Steps:**
1. 02:00 UTC: dbt model computes support traits (separate `churn-prediction-support-signals` skill).
2. 02:30 UTC: traits pushed to Vitally (Recipe 1 in that skill).
3. 03:00 UTC: Vitally recomputes health. Agent reads back (Recipe 7).
4. 03:30 UTC: snapshot stored in `csp_health_snapshot`.
5. 04:00 UTC: Recipe 6 detects threshold crossings; Recipe 9 prepares cohort summary.
6. 08:00 UTC: morning digest emailed to leadership (`gmail-mcp`); Slack alerts posted (`slack-mcp`).

**Result:** Health-driven workflow zero-touch each day.

### Example 2: Quarterly model validation

**Goal:** Confirm CSP health predicts churn.

**Steps:**
1. Recipe 11 — bucket-by-health vs 90d churn outcome.
2. If pattern holds (lower health → higher churn): publish CSM dashboard.
3. If pattern doesn't hold: schedule meeting with CSP vendor; re-weight inputs.

**Result:** Health score is calibrated, defended.

## Edge cases / gotchas

- **Score scales differ** (Vitally 0-10, Totango 0-100, Gainsight customizable, Custify 0-100). Always normalize before cross-tool comparison.
- **Latency between trait push and health recompute** — Vitally: 5-15 min; Totango: 1-24h; Gainsight: nightly. Don't read immediately after push.
- **External ID mismatch** — pushing to `external_id = stripe_cus_abc` only works if Vitally has that exact ID. Sync from CRM → CSP first.
- **Health flapping** — accounts crossing back-and-forth across 4.0 daily. Add `persistent_24h` debounce on alerts to avoid alert fatigue.
- **CSMs disable Playbooks they find annoying** — without governance, alerting decays. Quarterly Playbook review.
- **Per-driver visibility is uneven** — Vitally shows breakdown by driver clearly; Totango does too; Gainsight requires drilling into measures one-by-one.
- **CSP read rate limits matter at scale** — listing 10k+ accounts via API exceeds quotas. Use the segment endpoint or daily exports (CSV from CSP) instead.
- **Bulk export from Gainsight** — requires Rule (admin-managed) to push CSV to S3; not a single API call.
- **Permissions** — most CSP API keys are admin-equivalent. Rotate annually; audit usage quarterly.
- **HubSpot fallback assumes CRM is your CSP** — if your CSM team doesn't live in HubSpot, this fallback fails. Map to their actual workflow tool (sometimes Linear, Notion, even a Slack channel).
- **Don't push health to CSP if you compute it elsewhere** — pick one source of truth. Bidirectional mirror leads to drift.

## Sources

- [Vitally REST API reference](https://docs.vitally.io/en/articles/9880654-rest-api-accounts)
- [Vitally Health Scores](https://docs.vitally.io/en/articles/9901284-health-scores)
- [Catalyst Help Center (now Totango)](https://help.catalyst.io/)
- [Totango docs API](https://www.totango.com/docs/api)
- [Gainsight Connector 2.0](https://support.gainsight.com/gainsight_nxt/Connectors)
- [Vitally — best customer health score software 2026](https://www.vitally.io/post/the-best-customer-health-tracking-software)
- [Get an Account's Health Score (Postman)](https://www.postman.com/solution-architects-4700/request/29415260-b5500b9e-3d03-4b6c-ba6d-b4fb9e54ae5d)
