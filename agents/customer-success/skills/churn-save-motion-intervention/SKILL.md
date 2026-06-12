<!--
Source: https://help.churnzero.com/ + https://www.sturdy.ai/ + https://posthog.com/docs/session-replay + https://docs.vitally.io/reference
-->
# Churn Save Motion — Early Warning + Intervention — SKILL

Composite churn signal (4-of-6 trigger gate) detects at-risk customers, fires structured save play: exec outreach drafted via Gmail, roadmap commitment registered via Linear, commercial offer through Slack approval gate, all status-tracked in Notion save plan. Vendor signals from ChurnZero AI / Sturdy / Vitally Health Decline; free fallback uses PostHog usage drop + Postgres ticket sentiment + Stripe subscription status.

## When to use

- **Composite at-risk score crosses 4-of-6 signals** — auto-trigger.
- **CSM-initiated save** — CSM manually flags customer; skill builds the save plan template.
- **Exec sponsor departure detected** — sponsor not seen 30d; multi-thread + save.
- **NPS detractor follow-up** — score <= 6 within 90d.
- **T-90 Red renewal** — `renewal-management-90-day-prep` invokes this.
- **Post-incident save** — major SLA breach -> save before churn signal hardens.

This skill is the **execution arm** of `at-risk-identification-escalation` (which detects + escalates). It coordinates with `renewal-management-90-day-prep` for T-90 Red customers and feeds `voice-of-customer-reporting` with churn-reason data.

Trigger phrases: "save play", "at-risk save", "churn save", "exec outreach", "save plan", "roadmap commitment", "commercial offer".

## Setup

```bash
# CSP signal sources
export VITALLY_SUBDOMAIN="acme"
export VITALLY_API_KEY="<key>"
export CHURNZERO_API_KEY="<key>"
export STURDY_API_KEY="<key>"

# Free fallback signals
# posthog-mcp + postgresql-mcp + stripe-mcp + slack-mcp + linear-mcp + gmail-mcp in agent.yaml
```

Workspace prerequisites:
- Postgres view `composite_risk_signals` with 6 signal columns (usage_drop_30, sponsor_silent_30d, nps_detractor_90d, sentiment_drop_30d, sla_breach_30d, renewal_red).
- Notion "Save Plans" DB with: Customer, Triggered Date, Signals (multi-select), Health Snapshot, ARR at Risk, Renewal Date, Diagnosis, Outreach Status, Save Call Date, Diagnosis, Commercial Offer, Roadmap Commit (Linear), Outcome (Recovered / Churned / Extended).
- Slack `#renewal-saves` channel with approval reactions.
- Linear "save plan" issue label + workflow.

## 4-of-6 trigger gate

| # | Signal | Definition | Source |
|---|---|---|---|
| 1 | Usage drop > 30% WoW | events_this_week / events_prev_week < 0.7 | PostHog HogQL |
| 2 | Sponsor not seen > 30d | last sponsor login / email / Slack reply > 30d ago | CRM + Gmail + Slack |
| 3 | NPS detractor 90d | NPS <= 6 within last 90d | Delighted API |
| 4 | Sentiment drop > 20% WoW | avg_ticket_sentiment / prev_week < 0.8 | customer-support-agent Postgres |
| 5 | SLA breaches > 3 in 30d | count(SLA breach) >= 3 | customer-support-agent Postgres |
| 6 | Renewal Red T-90 to T-30 | risk=Red AND days_to_renewal <= 90 | renewal-management |

>= 4 = fire save play.

## Common recipes

### Recipe 1: Compute composite signals nightly

```sql
CREATE OR REPLACE VIEW composite_risk_signals AS
WITH
usage_drop AS (
  SELECT customer_id,
         (cur - prev) * 1.0 / nullif(prev, 0) AS usage_change_wow
  FROM (
    SELECT customer_id,
           count() FILTER (WHERE ts >= now() - INTERVAL '7 days') AS cur,
           count() FILTER (WHERE ts BETWEEN now() - INTERVAL '14 days' AND now() - INTERVAL '7 days') AS prev
    FROM events
    GROUP BY customer_id
  ) x
),
sponsor_silent AS (
  SELECT customer_id,
         current_date - last_sponsor_activity::date AS days_silent
  FROM sponsor_activity
),
nps_detractor AS (
  SELECT customer_id, min(score) AS min_score_90d
  FROM delighted_responses
  WHERE created_at >= now() - INTERVAL '90 days'
  GROUP BY customer_id
),
sentiment_drop AS (
  SELECT customer_id,
         (cur_sentiment - prev_sentiment) AS sentiment_change_wow
  FROM ticket_sentiment_weekly
),
sla AS (
  SELECT customer_id, count(*) AS breaches_30d
  FROM sla_breaches
  WHERE breached_at >= now() - INTERVAL '30 days'
  GROUP BY customer_id
),
renewal AS (
  SELECT customer_id, risk_classification, days_to_renewal
  FROM renewal_pipeline
)
SELECT
  c.customer_id, c.name, c.arr, c.csm_owner,
  CASE WHEN ud.usage_change_wow < -0.30 THEN 1 ELSE 0 END AS sig_usage_drop,
  CASE WHEN ss.days_silent > 30 THEN 1 ELSE 0 END AS sig_sponsor_silent,
  CASE WHEN np.min_score_90d <= 6 THEN 1 ELSE 0 END AS sig_nps_detractor,
  CASE WHEN sd.sentiment_change_wow < -0.20 THEN 1 ELSE 0 END AS sig_sentiment_drop,
  CASE WHEN sla.breaches_30d > 3 THEN 1 ELSE 0 END AS sig_sla,
  CASE WHEN r.risk_classification = 'Red' AND r.days_to_renewal BETWEEN 30 AND 90 THEN 1 ELSE 0 END AS sig_renewal_red,
  (CASE WHEN ud.usage_change_wow < -0.30 THEN 1 ELSE 0 END +
   CASE WHEN ss.days_silent > 30 THEN 1 ELSE 0 END +
   CASE WHEN np.min_score_90d <= 6 THEN 1 ELSE 0 END +
   CASE WHEN sd.sentiment_change_wow < -0.20 THEN 1 ELSE 0 END +
   CASE WHEN sla.breaches_30d > 3 THEN 1 ELSE 0 END +
   CASE WHEN r.risk_classification = 'Red' AND r.days_to_renewal BETWEEN 30 AND 90 THEN 1 ELSE 0 END) AS signals_firing
FROM customers c
LEFT JOIN usage_drop ud USING (customer_id)
LEFT JOIN sponsor_silent ss USING (customer_id)
LEFT JOIN nps_detractor np USING (customer_id)
LEFT JOIN sentiment_drop sd USING (customer_id)
LEFT JOIN sla USING (customer_id)
LEFT JOIN renewal r USING (customer_id);
```

### Recipe 2: ChurnZero AI risk score

```bash
curl -sS "https://api.churnzero.net/i/v1/accounts/$CUSTOMER_ID/risk_score" \
  -H "Authorization: Bearer $CHURNZERO_API_KEY" | jq '.risk_score, .top_signals'
```

If ChurnZero shows score > 70 (high risk), surface alongside Recipe 1 composite.

Doc: https://help.churnzero.com/

### Recipe 3: Sturdy AI signals

```bash
curl -sS "https://api.sturdy.ai/v1/signals?customer_id=$CUSTOMER_ID&since=30d&type=churn_risk" \
  -H "Authorization: Bearer $STURDY_API_KEY" | jq '.signals[]'
```

Sturdy extracts churn signals from Slack/email/Zoom conversations.

Doc: https://www.sturdy.ai/

### Recipe 4: Fire save play (composite >= 4)

```python
# Nightly job
for row in postgres.query("SELECT * FROM composite_risk_signals WHERE signals_firing >= 4"):
    create_save_plan(row)
```

### Recipe 5: Create save plan in Notion

```python
notion.create_page(
    parent={"database_id": SAVE_PLANS_DB_ID},
    properties={
        "Customer": {"title": [{"text": {"content": row.name}}]},
        "Triggered Date": {"date": {"start": today}},
        "Signals": {"multi_select": [
            {"name": s} for s in ["Usage drop", "Sponsor silent", "NPS detractor"][:signals_firing]
        ]},
        "ARR at Risk": {"number": row.arr},
        "Renewal Date": {"date": {"start": row.renewal_date}},
        "Outreach Status": {"status": {"name": "Draft"}},
        "Outcome": {"status": {"name": "In progress"}},
    },
    children=[
        # Save plan template body (from role.md)
    ],
)
```

### Recipe 6: Draft exec outreach email

```python
# gmail-mcp draft_email - DON'T send, draft for CSM Lead review
prompt = f"""
Draft an exec outreach email for {customer.name}.

Context:
- Health dropped from {prev_health:.2f} to {cur_health:.2f} over 30 days.
- Signals firing: {', '.join(signals_firing_list)}.
- Specific event: {primary_signal_specific_event}.

Rules:
- 4 sentences max.
- Acknowledge specifically (not generically).
- Take ownership ("That's on us") for our side.
- Ask for 30-min save call. Calendly link below.
- No "hope you're doing well." No "circling back."

Sender: {csm_lead.name}, {csm_lead.title}.
"""
draft = claude.generate(prompt)
gmail.draft_email(to=[exec_sponsor.email], subject=f"30 min - {customer.name}", body=draft.body, attachments=[calendly_url])
```

### Recipe 7: Slack ping CSM Lead + VP CS

```python
slack.chat_postMessage(
    channel="#renewal-saves",
    text=f"""
:rotating_light: Save play triggered: {customer.name}
ARR at risk: ${row.arr:,.0f}
Renewal: T-{row.days_to_renewal}
Signals firing (4-of-6): {', '.join(signals_firing_list)}
Owner: {csm_owner} (cc {csm_lead}, {vp_cs})
Notion: [Save plan]({notion_url})
Exec outreach: drafted in Gmail; review + send by EOD.
""",
)
```

### Recipe 8: Log commercial offer through approval gate

```python
slack.chat_postMessage(
    channel="#renewal-saves-approvals",
    text=f"""
:moneybag: Commercial offer requested: {customer.name}
Offer: 1-month free service credit
Rationale: SLA breaches in March-April; usage rebuilding
Approver: {vp_cs.name}
React :white_check_mark: to approve.
"""
)
# Wait for reaction
# Once approved, log in Notion save plan; issue Stripe credit
```

```bash
# stripe-mcp customer_balance_transactions_create
curl -sS -X POST "https://api.stripe.com/v1/customers/$STRIPE_CUSTOMER_ID/balance_transactions" \
  -u "$STRIPE_SECRET_KEY:" \
  -d "amount=-50000" \
  -d "currency=usd" \
  -d "description=Save play credit: 1-month service Q3 2026"
```

### Recipe 9: Register roadmap commitment in Linear

```python
# Required if save call promises product change
linear.create_issue(
    team_id=PRODUCT_TEAM,
    title=f"[Save] {customer.name}: {feature_request}",
    description=f"""
Customer: {customer.name} (${row.arr:,.0f} ARR, renewal T-{days})
Asked for: {feature_request}
Promised to: {champion.name} on {commitment_date}
ETA promised: {eta_promised}
Save plan: {notion_url}
""",
    labels=["save-play", "voice-of-customer"],
    assignee=PM_OWNER,
)
```

### Recipe 10: Save call agenda template

```markdown
# Save call: {customer.name}
Date: {date}
Attendees: {csm.name} ({title}), {customer_champion.name}, {exec_sponsor.name}

## Agenda (30 min)
1. (3 min) Acknowledge specifically:
   "{specific_acknowledgement}"
2. (10 min) Listen - diagnose what changed
3. (5 min) Commercial offer if appropriate (per approval gate)
4. (5 min) Roadmap commitment (Linear ticket reference)
5. (5 min) Joint plan refresh

## Rules
- No generic empathy
- Don't promise what's not in Linear
- Document everything in Fathom + Notion immediately after
```

### Recipe 11: 30-day check-in

After save call, schedule a Day-30 follow-up (via Calendly + Notion task).
- Day 0: save call held
- Day 7: check health score - climbing?
- Day 14: check usage rebound
- Day 30: book follow-up with champion; mark outcome (Recovered / Churned / Extended)

### Recipe 12: Outcome logging

```python
# After 30d follow-up
notion.update_page(
    page_id=save_plan_id,
    properties={
        "Outcome": {"status": {"name": "Recovered"}},  # or "Churned" or "Extended"
        "Outcome ARR": {"number": final_arr},
        "Outcome Notes": {"rich_text": [{"text": {"content": outcome_summary}}]},
    },
)
# Feed to voice-of-customer-reporting churn-reason taxonomy
```

## Examples

### Example 1: Composite trigger fires; save play executes

**Goal:** Acme hits 4-of-6 signals overnight; save play armed by 09:00 UTC.

**Steps:**
1. 02:00 UTC: Recipe 1 computes signals; Acme = 5-of-6 firing.
2. 03:00 UTC: Recipe 5 creates Notion save plan.
3. 03:30 UTC: Recipe 6 drafts exec outreach in CSM Lead's Gmail (drafts not sent).
4. 04:00 UTC: Recipe 7 Slack ping to CSM Lead + VP CS.
5. 09:00 UTC: CSM Lead reviews draft, sends. Calendly link triggers booking.
6. T+7: Save call held. Recipe 9 Linear ticket + Recipe 8 commercial offer approval.
7. T+30: Recipe 11 follow-up; Recipe 12 outcome logged.

**Result:** Save play executed; outcome captured for VOC.

### Example 2: CSM-initiated save (no auto-trigger)

**Goal:** CSM senses churn from a 1:1 vibe; signal hasn't hit threshold yet.

**Steps:**
1. CSM types "/save acme" in Slack.
2. Skill creates Notion save plan with manual trigger flag.
3. Recipe 6 drafts outreach.
4. CSM Lead reviews; same flow as Example 1 from step 5.

**Result:** Human-triggered save play follows same structure as auto-triggered.

## Edge cases / gotchas

- **4-of-6 threshold may be too aggressive** — calibrate quarterly. If save plans churn anyway, threshold may be too late; lower to 3-of-6 for Enterprise tier.
- **Exec outreach drafts must be reviewed** — never auto-send. AI-slop check (role.md) + human review.
- **Commercial offer approval gate** — never bypass. Equal treatment across customers preserves credibility.
- **Roadmap commitment without Linear ticket = fabricated** — refuse to draft "we're working on it" without a ticket. Hard rule from role.md.
- **Save call no-show** — customer ghosted. 48h follow-up; if still ghost, escalate to VP CS.
- **Save play succeeds but customer churns later** — outcome != commitment honored. Log as "Recovered then Churned" in 90-day lookback.
- **Multiple save plans for same customer** — collapse to one active plan; don't fire new save play if one open.
- **CSM and AE both think they own the save** — explicit owner in Notion; one driver, others support.
- **Health rebounds without intervention** — sometimes signals self-resolve (e.g., team came back from vacation). Wait 7d before firing; reduces noise.
- **PII in save plan notes** — Notion has access controls; CSM team only. Don't paste customer-team org chart with personal contact info.
- **Sturdy / ChurnZero AI mis-flags** — vendor models hallucinate. Validate against Recipe 1 composite before acting.
- **Stripe credit issuance permission** — restrict who can call Recipe 8 in production; require Slack reaction proof + audit log.

## Sources

- [ChurnZero AI + Plays](https://help.churnzero.com/)
- [Sturdy AI signal extraction](https://www.sturdy.ai/)
- [Vitally Health Decline events](https://docs.vitally.io/reference)
- [PostHog HogQL Query API](https://posthog.com/docs/api/queries)
- [Stripe customer balance transactions](https://stripe.com/docs/api/customer_balance_transactions)
- [Linear API create issue](https://developers.linear.app/docs/graphql/working-with-the-graphql-api)
- [Notion API create page](https://developers.notion.com/reference/post-page)
- [Calendly API single-use links](https://developer.calendly.com/api-docs/)
- [Gainsight Save Play patterns](https://www.gainsight.com/customer-success/save-play/)
