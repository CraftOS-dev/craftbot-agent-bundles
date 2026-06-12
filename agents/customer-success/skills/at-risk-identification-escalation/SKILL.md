<!--
Source: https://docs.vitally.io/reference + https://posthog.com/docs/session-replay + https://api.slack.com/methods/chat.postMessage + https://developers.linear.app/
-->
# At-Risk Identification + Escalation — SKILL

Nightly composite risk model on Postgres warehouse: joins health score + sponsor activity + ticket sentiment + SLA breaches + renewal stage. Outputs ranked risk list, Slack alerts to CSM leads + auto-creates Linear "save plan" issues for >P0. Companion to `churn-save-motion-intervention` (detect vs execute distinction).

## When to use

- **Nightly risk run** — every account scored Red/Yellow/Green.
- **Real-time signal trigger** — single high-impact signal (e.g., sponsor departure) auto-escalates.
- **CSM team morning standup** — review last 24h flagged accounts.
- **Pre-QBR risk briefing** — risk classification rolls into QBR slide 11.
- **Renewal T-90 risk feed** — feeds `renewal-management-90-day-prep` Recipe 2.
- **Quarterly model recalibration** — validate flag accuracy.

This skill is the **detection + escalation** half; execution lives in `churn-save-motion-intervention`. Together they're the at-risk loop.

Trigger phrases: "at-risk", "at-risk list", "escalate", "risk model", "risk classification", "Red account", "Yellow account".

## Setup

```bash
# postgresql-mcp + slack-mcp + linear-mcp + gmail-mcp already in agent.yaml

# Twilio for SMS escalation on highest-tier
# twilio-mcp in agent.yaml

# PagerDuty for on-call rotation (rare; highest tier only)
export PAGERDUTY_API_KEY="<key>"

# CSP data source
export VITALLY_SUBDOMAIN="acme"
export VITALLY_API_KEY="<key>"
```

Workspace prerequisites:
- Postgres views: `health_scores`, `sponsor_activity`, `ticket_metrics`, `renewal_metrics`.
- Slack channels: `#cs-at-risk` (all Red), `#cs-leads` (Lead-level), `#cs-vip-escalations` (Enterprise Red).
- Linear team `Customer Success` with `save-plan` label + workflow.
- Notion "At-Risk Tracker" DB for human-curated overrides.

## Risk classification model

```
Red if any of:
  health_score < 0.4
  health_score_trend_30d < -0.15
  (health_score < 0.6 AND sponsor_last_seen_days > 30)
  4-of-6 composite signals firing (see churn-save-motion-intervention)

Yellow if any of:
  health_score < 0.7
  health_score_trend_30d < -0.05

Green otherwise.
```

## Common recipes

### Recipe 1: Materialize nightly risk view

```sql
CREATE OR REPLACE VIEW at_risk_accounts AS
SELECT
  c.customer_id, c.name, c.tier, c.arr, c.csm_owner,
  h.health_score, h.health_score_trend_30d,
  s.last_sponsor_activity_days_ago,
  t.ticket_count_30d, t.sentiment_avg_30d, t.sla_breaches_30d,
  r.days_to_renewal, r.renewal_stage_score,
  CASE
    WHEN h.health_score < 0.4 THEN 'Red'
    WHEN h.health_score_trend_30d < -0.15 THEN 'Red'
    WHEN h.health_score < 0.6 AND s.last_sponsor_activity_days_ago > 30 THEN 'Red'
    WHEN h.health_score < 0.7 THEN 'Yellow'
    WHEN h.health_score_trend_30d < -0.05 THEN 'Yellow'
    ELSE 'Green'
  END AS risk_flag,
  CASE
    WHEN h.health_score < 0.4 THEN 'low_health'
    WHEN h.health_score_trend_30d < -0.15 THEN 'sharp_decline_30d'
    WHEN h.health_score < 0.6 AND s.last_sponsor_activity_days_ago > 30 THEN 'sponsor_gone'
    WHEN h.health_score_trend_30d < -0.05 THEN 'soft_decline_30d'
    ELSE 'stable'
  END AS primary_signal
FROM customers c
LEFT JOIN health_scores h USING (customer_id)
LEFT JOIN sponsor_activity s USING (customer_id)
LEFT JOIN ticket_metrics t USING (customer_id)
LEFT JOIN renewal_metrics r USING (customer_id);
```

Refresh nightly via `postgresql-mcp`.

### Recipe 2: Identify newly Red (vs yesterday)

```sql
WITH today AS (
  SELECT customer_id, risk_flag FROM at_risk_accounts WHERE as_of = CURRENT_DATE
),
yesterday AS (
  SELECT customer_id, risk_flag FROM at_risk_accounts_history WHERE as_of = CURRENT_DATE - 1
)
SELECT t.customer_id, t.risk_flag AS today, y.risk_flag AS yesterday
FROM today t LEFT JOIN yesterday y USING (customer_id)
WHERE t.risk_flag = 'Red' AND (y.risk_flag IS NULL OR y.risk_flag != 'Red');
```

### Recipe 3: Slack alert per newly-Red account

```python
for row in newly_red_today:
    text = f"""
:warning: At-risk crossing: *{row.name}* now Red
Health: {row.health_score:.2f} (trend 30d: {row.health_score_trend_30d:+.2f})
ARR: ${row.arr:,.0f}
Renewal: T-{row.days_to_renewal} days
Primary signal: {row.primary_signal}
Owner: <@{slack_user_id_for_csm(row.csm_owner)}>
Save plan: [Draft via /save {row.customer_id}]
"""
    channel = "#cs-vip-escalations" if row.tier == "Enterprise" else "#cs-at-risk"
    slack.chat_postMessage(channel=channel, text=text)
```

### Recipe 4: Auto-create Linear save-plan issue

```python
for row in newly_red_today:
    linear.create_issue(
        title=f"[Save Plan] {row.name} ({row.tier}, ${row.arr:,.0f} ARR)",
        description=f"""
Customer: {row.name}
Tier: {row.tier}
ARR: ${row.arr:,.0f}
Renewal: T-{row.days_to_renewal} days
Risk classified: Red (primary: {row.primary_signal})

Health: {row.health_score:.2f}
Trend 30d: {row.health_score_trend_30d:+.2f}

Save plan template: [Notion link]
""",
        team_id=CS_TEAM_ID,
        assignee_id=row.csm_owner_linear_id,
        labels=["save-plan", "at-risk"],
        priority=1 if row.tier == "Enterprise" else 2,
    )
```

### Recipe 5: SMS escalation for VIP Enterprise (Twilio)

```python
# Only for Enterprise tier > $250k ARR Red customers
if row.tier == "Enterprise" and row.arr > 250000:
    twilio.send_sms(
        to=row.csm_lead.phone,
        body=f"[Urgent] {row.name} crossed Red. ${row.arr/1000:.0f}k ARR. Renewal T-{row.days_to_renewal}. Slack thread above.",
    )
```

### Recipe 6: PagerDuty trigger for highest-tier

```bash
# > $500k ARR Red customer with renewal within 60d -> PagerDuty
curl -sS "https://events.pagerduty.com/v2/enqueue" \
  -H "Content-Type: application/json" \
  -d '{
    "routing_key": "'$PD_KEY'",
    "event_action": "trigger",
    "payload": {
      "summary": "VIP at-risk: '$NAME' ($'$ARR_K'k ARR, renewal T-'$DAYS')",
      "source": "craftbot-cs-at-risk",
      "severity": "critical"
    }
  }'
```

Doc: https://developer.pagerduty.com/api-reference/

### Recipe 7: Yellow weekly review queue

Yellow accounts roll up to CSM weekly review. Recipe 1 list filter `risk_flag = 'Yellow'` -> Notion page in CSM's "My Yellow Queue".

### Recipe 8: Risk trend dashboard

```sql
SELECT
  date_trunc('day', as_of) AS day,
  count(*) FILTER (WHERE risk_flag = 'Red') AS red,
  count(*) FILTER (WHERE risk_flag = 'Yellow') AS yellow,
  count(*) FILTER (WHERE risk_flag = 'Green') AS green,
  sum(arr) FILTER (WHERE risk_flag = 'Red') AS arr_at_risk
FROM at_risk_accounts_history
WHERE as_of >= now() - INTERVAL '90 days'
GROUP BY day
ORDER BY day;
```

Render via `xlsx` skill for monthly leadership review.

### Recipe 9: Per-CSM risk load

```sql
SELECT
  csm_owner,
  count(*) FILTER (WHERE risk_flag = 'Red') AS red,
  count(*) FILTER (WHERE risk_flag = 'Yellow') AS yellow,
  count(*) AS total,
  sum(arr) FILTER (WHERE risk_flag = 'Red') AS arr_red
FROM at_risk_accounts
WHERE as_of = CURRENT_DATE
GROUP BY csm_owner
ORDER BY red DESC;
```

CSMs with overweight risk loads = book rebalance signal.

### Recipe 10: Manual risk override

CSM Lead can override via Notion "At-Risk Tracker":
- Insert: `customer_id, override_flag, reason, expires_at`.
- Recipe 1 modified to honor override:

```sql
SELECT *,
  COALESCE(override.override_flag, computed.risk_flag) AS final_risk_flag
FROM at_risk_accounts computed
LEFT JOIN risk_overrides override
  ON override.customer_id = computed.customer_id
  AND override.expires_at > now();
```

Override expires 30d default; CSM Lead documented reason.

### Recipe 11: Save plan progress tracking

```sql
-- Per-save-plan Linear status
SELECT
  l.customer_id,
  l.linear_issue_id,
  l.status,
  l.created_at,
  now() - l.created_at AS time_open,
  c.name
FROM save_plan_issues l
JOIN customers c USING (customer_id)
WHERE l.status NOT IN ('Done', 'Cancelled')
ORDER BY time_open DESC;
```

Save plans open > 14d without status update = ping CSM Lead.

### Recipe 12: Quarterly model validation

```sql
-- Did Red accounts churn at higher rates than Green?
SELECT
  risk_flag_at_t_minus_90,
  count(*) AS n,
  count(*) FILTER (WHERE c.churned_at BETWEEN a.as_of AND a.as_of + INTERVAL '90 days') AS churned_90d,
  100.0 * count(*) FILTER (WHERE c.churned_at BETWEEN a.as_of AND a.as_of + INTERVAL '90 days') / count(*)::numeric AS churn_pct
FROM at_risk_accounts_history a
LEFT JOIN customers c USING (customer_id)
WHERE a.as_of = CURRENT_DATE - INTERVAL '90 days'
GROUP BY risk_flag_at_t_minus_90;
```

Expected: Red >> Yellow > Green churn rates. If not, model needs re-tuning.

## Examples

### Example 1: Nightly at-risk pipeline (zero-touch)

**Goal:** Every morning 06:00 UTC, CSM team has fresh at-risk list + alerts already sent.

**Steps:**
1. 02:00 UTC: Recipe 1 materializes view.
2. 02:30 UTC: snapshot to `at_risk_accounts_history`.
3. 03:00 UTC: Recipe 2 identifies newly Red.
4. 03:30 UTC: Recipe 3 Slack alerts; Recipe 4 Linear save-plan issues; Recipe 5 SMS for VIP.
5. 06:00 UTC: Recipe 9 per-CSM rollup -> Notion CSM books.
6. 09:00 UTC: CSM team standup uses fresh data.

**Result:** Detection + escalation runs hands-off.

### Example 2: Single signal manual escalation

**Goal:** Champion at Acme posted negative tweet about product. Not in nightly model.

**Steps:**
1. CSM types `/escalate acme reason="negative-public-mention"` in Slack.
2. Skill creates Notion override at_risk_accounts entry with override_flag=Red, reason="negative-public-mention".
3. Recipe 4 fires Linear save-plan issue immediately.
4. Recipe 5 fires SMS if Enterprise tier.

**Result:** Manual override path for human-detected risk.

## Edge cases / gotchas

- **Flag flapping** — same account Red one day, Yellow next, Red again. Use 24h persistent classification before firing escalation (don't alert daily).
- **CSM-Lead alert fatigue** — 30 Red accounts in one push = nobody acts. Cap escalations to top 5 by ARR.
- **Override misuse** — CSM Lead marks all Reds as Green to clean dashboard. Audit overrides quarterly.
- **Newly Red same customer as existing save plan open** — don't double-alert. Recipe 4 idempotency check.
- **Twilio SMS deliverability** — international Enterprise customers; SMS may fail. Fallback: email.
- **PagerDuty over-trigger** — wakes CSM Lead at 3am for $250k account. Set $500k threshold; document.
- **Trend lookback** — 30d trend on customer with 14d tenure = noise. Filter by tenure >= 30d.
- **Model interpretability** — `primary_signal` column is best-effort; CSMs need explanation. Recipe 12 validation matters.
- **Tier-vary thresholds** — Red threshold for Enterprise might be different from Starter. Document; don't hide tier-specific logic.
- **Override expiry without re-evaluation** — override expires; next morning account still Red. Communicate before expiry.
- **Linear issue without assignee** — CSM out of office, assignee_id = vacant -> nothing happens. Auto-fallback to CSM Lead.
- **Risk model recall vs precision** — model with 90% recall flags lots of False Positives (Yellow noise). Tune to org tolerance.

## Sources

- [Vitally Health Score docs](https://docs.vitally.io/en/articles/9901284-health-scores)
- [PostHog Session Replay](https://posthog.com/docs/session-replay)
- [Slack chat.postMessage](https://api.slack.com/methods/chat.postMessage)
- [Linear API issues](https://developers.linear.app/docs/graphql/working-with-the-graphql-api)
- [Twilio Messaging API](https://www.twilio.com/docs/messaging/api)
- [PagerDuty Events API v2](https://developer.pagerduty.com/api-reference/)
- [Notion database query](https://developers.notion.com/reference/post-database-query)
- [PostgreSQL views best practices](https://www.postgresql.org/docs/current/sql-createview.html)
- [Customer health composite (Gainsight blog)](https://www.gainsight.com/blog/customer-health-score/)
