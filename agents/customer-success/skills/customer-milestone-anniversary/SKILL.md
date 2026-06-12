<!--
Source: https://docs.vitally.io/reference/customer-traits + https://help.catalyst.io/ + https://docs.sendoso.com/ + https://developers.reachdesk.com/ + https://help.postal.io/ + https://help.tremendous.com/ + https://developers.klaviyo.com/ + https://stripe.com/docs/api
-->
# Customer Milestone + Anniversary Celebrations — Sendoso / Reachdesk / Postal.io / Tremendous — SKILL

Detect customer milestone events (1yr / 2yr / 3yr anniversary, $1M ARR processed, 10k users, 100k API calls, first export to enterprise, etc.) and trigger celebratory motions: congrats email, physical gift via Sendoso / Reachdesk / Postal.io, advocacy invite, case study ask, and Notion log. Anniversary-trigger cron + threshold-trigger Postgres query are the two main drivers.

## When to use

- **Customer hits 1yr anniversary** — fire congrats motion + advocacy invite + (optional) physical gift.
- **Usage threshold crossed** — 1M records processed, 10k users in workspace, 100k API calls -> celebration nudge.
- **Plan upgrade anniversary** — 1yr on Enterprise tier -> CSM-led milestone QBR.
- **Customer-specific milestone** — they launched a major customer-facing feature using your product; congratulate.
- **First aha at scale** — completed onboarding, first full month at full usage -> celebrate.
- **Renewal anniversary** — auto-renewed for Y2/Y3 -> thank-you motion + QBR teaser.

This skill **reads from** `customer-health-scoring` (anniversary date in CSP), `adoption-metric-feature-usage` (usage thresholds), and Stripe subscription data. It **feeds** `customer-advocacy-case-study-reference` (anniversary triggers an advocacy ask) and `referral-programs` (active anniversary customers are referrer candidates).

Trigger phrases: "anniversary", "1yr milestone", "Sendoso gift", "Reachdesk", "Postal.io", "milestone celebration", "customer birthday", "10k users milestone", "annual celebration".

## Setup

```bash
# Vitally (anniversary trait)
export VITALLY_API_KEY="<key>"

# Catalyst (anniversary)
export CATALYST_API_KEY="<key>"

# Sendoso (physical + digital gift platform - enterprise)
export SENDOSO_API_KEY="<key>"
export SENDOSO_SENDER_ID="<id>"

# Reachdesk (corporate gifting)
export REACHDESK_API_TOKEN="<token>"

# Postal.io (gifting + direct mail)
export POSTAL_API_KEY="<key>"
export POSTAL_TEAM_ID="<id>"

# Tremendous (digital gift card fallback)
export TREMENDOUS_API_KEY="<key>"
export TREMENDOUS_FUNDING_SOURCE_ID="<id>"

# Klaviyo (congrats email lifecycle)
export KLAVIYO_API_KEY="<key>"

# Stripe (anniversary detected from subscription created date) - via stripe-mcp
# Postgres (threshold tracking) - via postgresql-mcp
# Notion (milestone log) - via notion-mcp
# Gmail (congrats template) - via gmail-mcp
```

Workspace prerequisites:
- Notion "Milestones" DB with: Customer, Milestone Type, Threshold Hit, Date, Gift Sent (yes/no), Gift Vendor, Tracking #, Advocacy Triggered (yes/no), CSM Note.
- Cron: nightly check for anniversaries (today vs `signup_date + N years`) + threshold queries.
- Gift budget approval: < $50 auto-send; $50-$250 CSM approval; > $250 VP CS approval.
- Customer address book in Postgres (shipping for physical gifts).
- Cooldown rule: don't double-touch within 14 days (anniversary + threshold can collide).

## Milestone catalog (reference)

| Milestone | Trigger | Gift tier | Motion |
|---|---|---|---|
| 1yr anniversary (signup) | `signup_date + 365d` | $50 Sendoso swag or Tremendous gift | Congrats email + advocacy invite |
| 2yr anniversary | `signup_date + 2*365d` | $100 gift or branded merch | Congrats email + QBR teaser |
| 3yr+ anniversary | `signup_date + N*365d` | $150 hand-written card + gift | Personal note from VP CS |
| First $1M ARR processed | `cumulative_arr >= 1000000` | $250 gift + CSM call | Congrats email + case study ask |
| 10k users in workspace | `users_count >= 10000` | $100 gift | Congrats email + expansion convo |
| 100M API calls served | `api_call_cumulative >= 100M` | $100 gift + technical-blog ask | Engineering+CS dual outreach |
| Customer launched their product using ours | manually flagged | $250 + custom card | CSM-Lead + VP CS sign |
| Plan upgrade 1yr anniversary | `plan_upgrade_date + 365d` | $50 gift | Congrats + renewal teaser |

## Common recipes

### Recipe 1: Daily anniversary detection (cron)

```sql
-- All customers hitting an exact 1yr / 2yr / 3yr today
SELECT
  c.id AS customer_id,
  c.name,
  c.primary_contact_email,
  c.signup_date,
  date_part('year', age(now(), c.signup_date))::int AS years_elapsed,
  CASE
    WHEN date_part('day', age(now(), c.signup_date)) = 0
     AND date_part('month', age(now(), c.signup_date)) = 0
     AND date_part('year', age(now(), c.signup_date)) IN (1, 2, 3, 4, 5)
    THEN 'milestone'
    ELSE NULL
  END AS milestone_flag
FROM customers c
WHERE c.subscription_status = 'active'
  AND c.signup_date <= now() - INTERVAL '1 year'
HAVING milestone_flag = 'milestone';
```

Run via cron 09:00 local each weekday. Output -> Recipe 4 / 5 / 6.

### Recipe 2: Usage threshold detection (nightly)

```sql
-- Customers crossing the 1M ARR processed threshold today
WITH cumulative AS (
  SELECT
    customer_id,
    sum(amount_processed) AS cumulative_arr
  FROM transactions
  GROUP BY customer_id
)
SELECT c.id, c.name, c.primary_contact_email, cu.cumulative_arr
FROM cumulative cu
JOIN customers c ON c.id = cu.customer_id
LEFT JOIN milestone_log m ON m.customer_id = c.id AND m.milestone_type = '1M_ARR_processed'
WHERE cu.cumulative_arr >= 1000000
  AND m.id IS NULL;  -- not yet celebrated
```

Apply same pattern to `users_count`, `api_call_cumulative`, etc.

### Recipe 3: Vitally trait read (anniversary already tracked)

```bash
curl -sS "https://api.vitally.io/resources/customers/$CUSTOMER_ID" \
  -H "Authorization: Basic $(echo -n $VITALLY_API_KEY: | base64)" | jq '.traits.signup_anniversary_days'
```

Doc: https://docs.vitally.io/reference/customer-traits

### Recipe 4: Draft personalized congrats email

```python
prompt = f"""
Draft a 5-sentence anniversary congratulations email.

Customer: {customer.name}
Milestone: {milestone.label}
Specific outcome they achieved in the past year: {customer.success_outcome}
Their CSM: {csm.name}

Rules:
- Acknowledge the specific outcome (not generic "you've been with us for a year!").
- Mention one specific use case detail.
- No "Excited to share" / "Thrilled to celebrate" - cut all of that.
- Sign as {csm.name}.
- One CTA: 30-min thank-you call OR advocacy invite (don't include both in one email).
"""
body = claude.generate(prompt)
gmail.send_email(to=[customer.primary_email], subject=f"{customer.name} - 1 year together", body=body)
```

### Recipe 5: Send Sendoso physical gift

```bash
# Sendoso eGift or physical send
curl -sS -X POST "https://app.sendoso.com/api/v3/sends" \
  -H "Authorization: Bearer $SENDOSO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "sender_id": "'$SENDOSO_SENDER_ID'",
    "template_id": "'$SENDOSO_1YR_TEMPLATE_ID'",
    "recipients": [{
      "email": "'$RECIPIENT_EMAIL'",
      "first_name": "'$RECIPIENT_FIRST_NAME'",
      "last_name": "'$RECIPIENT_LAST_NAME'",
      "shipping_address": {
        "address1": "'$ADDRESS1'",
        "city": "'$CITY'",
        "state": "'$STATE'",
        "postal_code": "'$ZIP'",
        "country": "US"
      }
    }],
    "note": "Happy 1 year with us! - " + "'$CSM_NAME'"
  }'
```

Doc: https://docs.sendoso.com/

### Recipe 6: Send Reachdesk gift

```bash
curl -sS -X POST "https://api.reachdesk.com/v1/sends" \
  -H "Authorization: Bearer $REACHDESK_API_TOKEN" \
  -d '{
    "campaign_id": "'$REACHDESK_1YR_CAMPAIGN_ID'",
    "recipient": {
      "email": "'$RECIPIENT_EMAIL'",
      "first_name": "'$RECIPIENT_FIRST_NAME'",
      "address": {
        "line1": "'$ADDRESS1'",
        "city": "'$CITY'",
        "postal_code": "'$ZIP'",
        "country": "US"
      }
    },
    "personalization": {"message": "Happy 1 year!"}
  }'
```

Doc: https://developers.reachdesk.com/

### Recipe 7: Send Postal.io gift

```bash
curl -sS -X POST "https://api.postal.io/api/v1/items/orders" \
  -H "X-API-Key: $POSTAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "teamId": "'$POSTAL_TEAM_ID'",
    "approvedItemId": "'$POSTAL_ITEM_ID'",
    "contact": {
      "emailAddress": "'$RECIPIENT_EMAIL'",
      "firstName": "'$RECIPIENT_FIRST_NAME'",
      "lastName": "'$RECIPIENT_LAST_NAME'",
      "address": {
        "address1": "'$ADDRESS1'",
        "city": "'$CITY'",
        "state": "'$STATE'",
        "postalCode": "'$ZIP'",
        "country": "US"
      }
    },
    "messageHTML": "<p>Happy 1 year together!</p>"
  }'
```

Doc: https://help.postal.io/

### Recipe 8: Tremendous gift card fallback (digital-only)

```bash
curl -sS -X POST "https://www.tremendous.com/api/v2/orders" \
  -H "Authorization: Bearer $TREMENDOUS_API_KEY" \
  -d '{
    "external_id": "milestone-1yr-'$CUSTOMER_ID'",
    "payment": {"funding_source_id": "'$TREMENDOUS_FUNDING_SOURCE_ID'"},
    "rewards": [{
      "value": {"denomination": 50, "currency_code": "USD"},
      "campaign_id": "'$TREMENDOUS_CAMPAIGN_ID'",
      "recipient": {"email": "'$RECIPIENT_EMAIL'", "name": "'$RECIPIENT_NAME'"}
    }]
  }'
```

Doc: https://help.tremendous.com/

### Recipe 9: Klaviyo lifecycle event for anniversary

```bash
# Fire a Klaviyo event; matching flow sends the templated congrats email
curl -sS -X POST "https://a.klaviyo.com/api/events/" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" \
  -H "revision: 2024-10-15" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "type": "event",
      "attributes": {
        "properties": {"milestone": "1yr_anniversary", "csm": "'$CSM_NAME'"},
        "metric": {"data": {"type": "metric", "attributes": {"name": "Customer Milestone Hit"}}},
        "profile": {"data": {"type": "profile", "attributes": {"email": "'$RECIPIENT_EMAIL'"}}}
      }
    }
  }'
```

Doc: https://developers.klaviyo.com/en/reference/events_api_overview

### Recipe 10: Log milestone in Notion + Postgres

```python
notion.create_page(
    parent={"database_id": MILESTONES_DB_ID},
    properties={
        "Customer": {"title": [{"text": {"content": customer.name}}]},
        "Milestone Type": {"select": {"name": "1yr Anniversary"}},
        "Date": {"date": {"start": today_iso}},
        "Gift Sent": {"checkbox": True},
        "Gift Vendor": {"select": {"name": "Sendoso"}},
        "Tracking #": {"rich_text": [{"text": {"content": tracking_id}}]},
        "Advocacy Triggered": {"checkbox": True},
        "CSM Note": {"rich_text": [{"text": {"content": csm_note}}]},
    },
)

# Postgres dedupe lock
psql.execute(
    "INSERT INTO milestone_log(customer_id, milestone_type, fired_at, gift_vendor, tracking_id) VALUES (%s, %s, now(), %s, %s)",
    [customer.id, "1yr_anniversary", "Sendoso", tracking_id]
)
```

Postgres lock is the SOT to prevent double-fire.

### Recipe 11: Cross-trigger advocacy invite

```python
# After anniversary congrats sent (D+0), wait 7 days then trigger advocacy ask if NPS >= 8 and health >= 0.7
import time
from advocacy_skill import invite_promoter

if customer.nps_latest >= 8 and customer.health_score >= 0.7:
    schedule_at = today_iso_plus_7days
    invite_promoter.schedule(
        customer_id=customer.id,
        ask_type="case_study_anniversary",
        scheduled_at=schedule_at,
        source="1yr_anniversary"
    )
```

This dovetails into `customer-advocacy-case-study-reference` Recipe 3.

### Recipe 12: Threshold trigger - 1M ARR processed celebration

```python
# Detected via Recipe 2; assemble multi-channel celebration
csm_note = f"{customer.name} just processed $1M lifetime. Big moment."

# 1. Email VP CS to send personal note
gmail.send_email(
    to=[vp_cs.email],
    subject=f"$1M milestone - {customer.name}",
    body=f"{customer.name} just crossed $1M ARR processed. Send personal note?",
)

# 2. Send physical gift via Sendoso ($250 tier)
sendoso_send(template_id=SENDOSO_BIG_MILESTONE_TEMPLATE_ID, recipient=customer.exec_sponsor)

# 3. Notion + Postgres log (Recipe 10)
```

### Recipe 13: Quarterly milestone report

```sql
SELECT
  milestone_type,
  count(*) AS count,
  sum(CASE WHEN gift_vendor IS NOT NULL THEN 1 ELSE 0 END) AS gifts_sent,
  sum(CASE WHEN advocacy_triggered THEN 1 ELSE 0 END) AS advocacy_triggered,
  sum(CASE WHEN advocacy_outcome = 'completed' THEN 1 ELSE 0 END) AS advocacy_completed
FROM milestone_log
WHERE fired_at >= now() - INTERVAL '90 days'
GROUP BY milestone_type
ORDER BY count DESC;
```

Output to `xlsx` skill -> CS leadership monthly review.

## Examples

### Example 1: 1yr signup anniversary - end-to-end

**Goal:** Acme.Inc signed up exactly 365 days ago; celebrate.

**Steps:**
1. 09:00 UTC daily cron: Recipe 1 returns Acme.
2. Check budget + CSM Lead pre-approval (auto if < $50, none needed).
3. Recipe 4 drafts congrats email referencing Acme's specific outcome ("60% support ticket reduction").
4. Recipe 5 sends $50 Sendoso swag to primary contact (CSM-prefilled address).
5. Recipe 10 logs in Notion + Postgres.
6. Recipe 11 schedules a D+7 advocacy invite (Acme is NPS 9; health 0.78).
7. Gmail send goes out 14:00 UTC.

**Result:** Acme primary contact gets warm acknowledgment + swag arrives 2 days later + advocacy ask follows up next week without overwhelming.

### Example 2: 10k users milestone (usage threshold)

**Goal:** Globex.Corp just crossed 10k users in their workspace.

**Steps:**
1. Recipe 2 nightly query detects the threshold + no prior log.
2. CSM sees Slack alert via `slack-mcp` (custom alert from Recipe 2 output).
3. CSM-Lead approves $100 gift; Recipe 6 (Reachdesk) sends Visa gift card + branded card to admin contact.
4. Recipe 9 fires Klaviyo event -> congrats email auto-sent via flow.
5. Recipe 10 logs.
6. CSM schedules a 30-min expansion-conversation call via `calendly-api` since 10k users = expansion signal.

**Result:** Customer feels seen; expansion conversation triggered organically.

### Example 3: Coordination with existing congrats (deduplication)

**Goal:** Customer's 1yr anniversary + a renewal-T-30 ping are both today.

**Steps:**
1. Cron detects both events.
2. Dedupe rule: within 14 days, only the higher-priority (anniversary > renewal-prep) fires.
3. Add a renewal-pricing teaser at the end of the anniversary email.
4. Renewal cadence in `renewal-management-90-day-prep` records skipped touch + plans T-23 follow-up.

**Result:** No spam; customer gets one warm touch covering both motions.

## Edge cases / gotchas

- **Anniversary date collision with renewal T-30** — same week conflicts; use dedup window (Recipe Example 3).
- **Customer churned but signup still in DB** — `subscription_status = 'cancelled'` filter critical; don't send congrats to former customers.
- **Recipient on PTO / left company** — gift bounces; track via Sendoso webhook -> reroute via Recipe 7 / 8.
- **Physical gift shipping cost** — Sendoso/Reachdesk include shipping in cost; international shipping can 2-3x the budget. Set per-region tier (US $50; intl $100).
- **No shipping address on file** — fallback to Tremendous digital gift (Recipe 8) or skip physical gift; don't ask the customer for their address (kills the surprise).
- **Customer-facing tracking number** — if it's a surprise gift, don't send tracking info via Klaviyo lifecycle event (would spoil surprise). Only show tracking internally in Notion.
- **Gift tax compliance** — some industries (gov, banking, healthcare) forbid gifts > $25; check Customer Compliance flag in Notion before sending physical gift.
- **Threshold double-counting** — `cumulative_arr >= 1M` can fire multiple days in a row if dedup is missing. Postgres `milestone_log` unique constraint on `(customer_id, milestone_type)` is required.
- **Anniversary year edge case (Feb 29)** — leap year customer; cron either skips Feb 29 in non-leap years or uses Feb 28. Coordinate with team; document.
- **Advocacy fatigue** — anniversary + NPS + CSAT triggers can all fire at once. The `customer-advocacy-case-study-reference` cooldown (6mo) deduplicates.
- **Sendoso template vs custom note** — template congrats can feel generic. For $250+ gifts, draft a custom note + handwritten card option in Sendoso.
- **VIP customer hand-handled motion** — strategic accounts (top 20 by ARR) should be flagged in Notion and motion handled by CSM-Lead + VP CS personally - not automated.
- **Tier-2 lifecycle conflicts** — Klaviyo lifecycle flow might also send a generic "thanks for being with us" - rate-limit + tag to avoid double touch.
- **CSM out of office** — congrats email signed by CSM but CSM is out; replace signature with CSM-Lead or VP CS automatically.
- **Customer requested no marketing comms** — `marketing_opt_out = true` excludes from anniversary motion too. Honor; CSM personal email only.

## Sources

- [Vitally customer traits](https://docs.vitally.io/reference/customer-traits)
- [Catalyst (Totango) properties](https://help.catalyst.io/)
- [Sendoso API docs](https://docs.sendoso.com/)
- [Reachdesk Developer docs](https://developers.reachdesk.com/)
- [Postal.io API reference](https://help.postal.io/en/articles/3984568-postal-api)
- [Tremendous Orders API](https://help.tremendous.com/hc/en-us/categories/360002107552-API)
- [Klaviyo Events API](https://developers.klaviyo.com/en/reference/events_api_overview)
- [Stripe Subscriptions API](https://stripe.com/docs/api/subscriptions)
- [Notion Database API](https://developers.notion.com/reference/database)
- [PostgreSQL date_part anniversary patterns](https://www.postgresql.org/docs/current/functions-datetime.html)
