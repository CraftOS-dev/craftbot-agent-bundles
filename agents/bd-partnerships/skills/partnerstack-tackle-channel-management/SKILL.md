<!--
Source: https://partnerstack.com/api + https://tackle.io/api-documentation + https://www.allbound.com/api + https://www.impartner.com/
Partnerstack/Tackle/Allbound/Impartner PRM operations + integration health (June 2026 SOTA).
-->
# Partnerstack / Tackle / Allbound / Impartner Channel Management — SKILL

Run day-to-day operations across PRM platforms: partner CRUD, commission posting, payout scheduling, deal-reg lifecycle, MDF execution, certification tracking, integration health monitoring. **Partnerstack** = SOTA for referral+affiliate+reseller (SMB-mid). **Tackle.io** = cloud marketplace co-sell orchestrator. **Allbound** = LMS-strong PRM. **Impartner** = enterprise PRM. **Channeltivity** + **Magentrix** = mid-market alternates.

## When to use

- **Adding a partner to PRM** — onboarding mechanic.
- **Posting commission for closed-won** — manual or auto.
- **Scheduling partner payouts** — quarterly or monthly.
- **Running integration health monitor** — Sentry + PostHog + warehouse.
- **PRM CRM hygiene** — stale records, orphan deal-reg, expired certs.
- **Pulling per-partner performance for scorecards** — feeds `partner-scorecard-authoring`.
- **Trigger phrases**: "add partner to Partnerstack", "post commission", "schedule payout", "Tackle co-sell sync", "integration health dashboard", "partner hygiene cron".

Do NOT use this skill for: **the partner agreement itself** (use `referral-affiliate-channel-oem-agreement-structuring`); **commission accounting** (defer to `finance-controller`); **deal-reg workflow logic** (use `deal-registration-channel-conflict-resolution`); **MDF requests** (use `mdf-allocation-tracking`).

## Setup

```bash
export MATON_API_KEY="<key>"
export PARTNERSTACK_API_KEY="<key>"
export TACKLE_API_KEY="<key>"
export ALLBOUND_API_KEY="<key>"
export IMPARTNER_API_KEY="<key>"
# postgres warehouse for hygiene cron
# sentry-mcp for integration health
```

## Common recipes

### Recipe 1: Partnerstack — add partner

```bash
curl -X POST "https://gateway.maton.ai/partnerstack/v3/partners" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "company_name": "Acme Solutions",
    "primary_contact_email": "sarah@acme.com",
    "primary_contact_first_name": "Sarah",
    "primary_contact_last_name": "Lee",
    "groups": ["referral","mid-market"],
    "stripe_account_id": "acct_XXXXXX",
    "metadata": {"hubspot_company_id":"abc","tier":"silver","start_date":"2026-06-15"}
  }'
```

Reference: https://partnerstack.com/api.

### Recipe 2: Partnerstack — post commission for closed-won

```bash
curl -X POST "https://gateway.maton.ai/partnerstack/v3/transactions/commissions" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "partner_id": "acme-001",
    "amount_usd": 4500,
    "deal_id": "deal-globex-q3",
    "deal_amount_usd": 30000,
    "commission_pct": 15,
    "transaction_date": "2026-06-30",
    "description": "Q3 referral commission — Globex Corp closed-won",
    "metadata": {"hubspot_deal_id":"deal-12345"}
  }'
```

Auto-post via webhook from HubSpot/Salesforce on `closedwon`:

```python
def on_closed_won(deal):
    if deal["properties"].get("hs_lead_source") == "partner":
        partner_id = deal["properties"]["partner_id"]
        commission_pct = lookup_partner_tier(partner_id)["commission_pct"]
        amount = deal["properties"]["amount"] * commission_pct / 100
        post_commission(partner_id, amount, deal)
```

### Recipe 3: Partnerstack — schedule payout

```bash
curl -X POST "https://gateway.maton.ai/partnerstack/v3/payouts/schedule" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "partner_id": "acme-001",
    "amount_usd": 12500,
    "currency": "USD",
    "payment_method": "stripe_connect",
    "scheduled_for": "2026-07-15",
    "transaction_ids": ["txn-001","txn-002","txn-003"],
    "description": "Q2 commissions payout"
  }'
```

### Recipe 4: Partnerstack — performance read

```bash
curl "https://gateway.maton.ai/partnerstack/v3/partners/acme-001/performance?period=2026-q2" \
  -H "Authorization: Bearer $MATON_API_KEY" | jq '{
    leads_submitted, leads_accepted, opportunities_created,
    pipeline_amount, closed_won_count, closed_won_amount,
    commission_earned, commission_paid
  }'
```

Feeds `partner-scorecard-authoring`.

### Recipe 5: Tackle — push co-sell opportunity to AWS ACE

```bash
curl -X POST "https://gateway.maton.ai/tackle/v3/sync/ace-opportunity" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "buyer": {"company_name":"Globex Corp","duns":"123456789","aws_account_id":"123456789012"},
    "deal_amount_usd": 250000,
    "deal_stage": "qualified",
    "primary_contact": {"email":"buyer@globex.com","first_name":"Sam","last_name":"Lee"},
    "salesforce_opportunity_id":"006xxx",
    "co_sell_motion":"customer_introduction"
  }'
```

Tackle handles AWS ACE / Microsoft Co-Sell / Google Partner Advantage with the same JSON shape.

### Recipe 6: Tackle — list co-sell opportunities (status sync)

```bash
curl "https://gateway.maton.ai/tackle/v3/opportunities/co-sell?cloud=aws&status=in_progress" \
  -H "Authorization: Bearer $MATON_API_KEY" | jq '.opportunities[] | {
    id, buyer_name, aws_seller_engaged, stage, amount_usd, last_activity_at
  }'
```

### Recipe 7: Allbound / Impartner direct (no-Maton fallback)

```bash
# Allbound API — partner CRUD
curl -X POST "https://api.allbound.com/v2/partners" \
  -H "Authorization: Bearer $ALLBOUND_API_KEY" -H "Content-Type: application/json" \
  -d '{"name":"Acme Solutions","tier":"silver","status":"active"}'

# Impartner API — deal reg lookup
curl "https://your-tenant.impartner.com/api/v1/deal-registrations?partner_id=acme-001" \
  -H "Authorization: Bearer $IMPARTNER_API_KEY"
```

Reference: https://www.allbound.com/api ; https://www.impartner.com/.

### Recipe 8: Integration health — Sentry per-partner errors

```bash
# sentry-mcp issues query — tag by integration_partner_id
curl "https://sentry.io/api/0/organizations/your-org/issues/?query=tag:integration_partner_id:acme&statsPeriod=7d" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" | jq '.[] | {
    title, eventCount: .count, level, lastSeen
  }'
```

Weekly digest to Slack via `slack-mcp`.

### Recipe 9: Integration adoption — PostHog event query

```bash
curl -X POST "https://app.posthog.com/api/projects/<id>/insights/trend/" \
  -H "Authorization: Bearer $POSTHOG_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "events": [{"id":"integration_action_taken","math":"dau","name":"DAU"}],
    "breakdown": "integration_partner_id",
    "breakdown_type": "event",
    "date_from": "-30d"
  }'
```

`mixpanel-mcp` and `amplitude-mcp` have equivalent breakdown queries.

### Recipe 10: Weekly integration health digest

```python
def weekly_integration_health(partner_id):
    sentry_errors = query_sentry(partner_id, days=7)
    posthog_dau = query_posthog_dau(partner_id, days=7)
    error_rate = (sentry_errors["count"] / max(posthog_dau["events"], 1)) * 100
    joint_customers_active = query_warehouse(f"SELECT count(*) FROM joint_customers WHERE partner='{partner_id}' AND integration_active=true")

    digest = {
        "partner": partner_id,
        "joint_customers_active": joint_customers_active,
        "events_7d": posthog_dau["events"],
        "errors_7d": sentry_errors["count"],
        "error_rate_pct": round(error_rate, 2),
        "top_errors": sentry_errors["top_3"],
        "health": (
            "green" if error_rate < 0.5 else
            "yellow" if error_rate < 2 else
            "red"
        ),
    }
    post_to_slack("#integration-health", digest)
```

Run via `postgresql-mcp` cron Friday 9am.

### Recipe 11: PRM hygiene cron (monthly)

```sql
-- Find stale partner records (no activity 6+ months)
SELECT partner_id, partner_name, last_activity_at
FROM partners
WHERE last_activity_at < now() - interval '6 months'
  AND status = 'active'
ORDER BY last_activity_at;

-- Find orphan deal-reg records past 60-day window
SELECT dr.id, dr.partner_id, dr.registered_at, dr.expires_at
FROM deal_registrations dr
WHERE dr.expires_at < now() AND dr.status = 'registered'
  AND NOT EXISTS (SELECT 1 FROM deals d WHERE d.deal_reg_id = dr.id);

-- Find MDF requests without POP past deadline
SELECT mdf.id, mdf.partner_id, mdf.claim_period_end
FROM mdf_requests mdf
WHERE mdf.claim_period_end < now() - interval '14 days'
  AND mdf.status = 'approved' AND mdf.pop_submitted_at IS NULL;

-- Find expiring certifications (90-day window)
SELECT contact_email, level, cert_expires
FROM partner_certifications
WHERE cert_expires BETWEEN now() AND now() + interval '90 days'
  AND status = 'active';
```

Each query → email/Slack alert via `gmail-mcp`/`slack-mcp`.

### Recipe 12: Hygiene action handlers

```python
# Per-partner stale: archive after warning email
def handle_stale_partner(partner):
    if partner["last_warning_at"] is None:
        send_email(partner["contact_email"], "stale-partner-warning")
        update_partner(partner["id"], {"last_warning_at": now()})
    elif (now() - partner["last_warning_at"]).days > 30:
        update_partner(partner["id"], {"status": "archived"})
        send_email(partner["contact_email"], "partner-archived")

# Orphan deal-reg: expire
def handle_orphan_deal_reg(dr):
    update_deal_reg(dr["id"], {"status": "expired", "expired_at": now()})

# MDF without POP past deadline: escalate
def handle_missing_pop(mdf):
    post_slack("#mdf-issues", f"MDF {mdf['id']} expired without POP — escalating to BD")
    update_mdf(mdf["id"], {"status": "denied_pop"})

# Cert expiring: renewal sequence (cross to partner-enablement-certification-programs)
def handle_expiring_cert(cert):
    days_left = (cert["cert_expires"] - now()).days
    template = "renewal-30d" if days_left <= 30 else "renewal-60d" if days_left <= 60 else "renewal-90d"
    send_email(cert["contact_email"], template)
```

## Examples

### Example 1: New partner onboarded; auto-commission flow

**Goal:** Sarah at Acme just signed referral agreement; setup full commission pipeline.

**Steps:**
1. Recipe 1 — Add Acme to Partnerstack.
2. Stripe Connect account linked to Partnerstack.
3. HubSpot webhook configured: on `closedwon` with `lead_source=partner`, fire Recipe 2.
4. First deal closes 30 days later; commission auto-posts.
5. Quarter-end: Recipe 3 schedules consolidated payout.
6. Recipe 4 reads performance into scorecard.

**Result:** Hands-off commission pipeline; partner sees consistent monthly commission posting + quarterly payout.

### Example 2: AWS co-sell push for $250K deal

**Goal:** Joint deal with Globex Corp; want AWS seller engagement; co-sell motion.

**Steps:**
1. Sales-agent qualifies deal; flags "AWS Marketplace eligible + co-sell candidate."
2. Recipe 5 — Push to ACE via Tackle.
3. AWS seller picks up within 48h (ACE matchmaking).
4. Joint customer call scheduled.
5. Recipe 6 — Tackle status sync tracks AWS-side progress.
6. Closed via AWS Marketplace private offer (cross to `aws-azure-gcp-marketplace-listings`).

**Result:** Co-sell motion engaged; deal closes via marketplace with AWS seller co-pitch.

### Example 3: Monthly hygiene cron catches expiring certs + orphan deal-reg

**Goal:** Quarterly close approaching; need clean PRM state.

**Steps:**
1. Recipe 11 — Hygiene queries run.
2. 18 stale partners flagged; 6 archived after 30-day warning silence.
3. 4 orphan deal-reg expired; partners notified.
4. 2 MDF without POP past deadline → escalated.
5. 35 expiring certs in 90-day window → renewal sequence triggered.
6. Q-end PRM is clean.

**Result:** Disciplined cron prevents pipeline pollution + commission disputes.

## Edge cases / gotchas

- **Partnerstack vs PRM choice** — Partnerstack is the SOTA for referral/affiliate/reseller commission + payout; not a full PRM (no LMS, lighter deal-reg). Allbound/Impartner are full PRMs but heavier. Choose based on motion mix.
- **Tackle's $30k-100k+/yr** — for pre-$1M marketplace ARR, direct AWS Catalog + Azure Partner Center + GCP Producer Portal may be cheaper (Recipe 1 in `aws-azure-gcp-marketplace-listings`).
- **Commission attribution dispute** — "this deal was partner-sourced AND direct-team-influenced"; first-touch vs last-touch matters. Set policy + document in `referral-affiliate-channel-oem-agreement-structuring`.
- **Stripe Connect KYC** — partner must complete Stripe onboarding before payouts; otherwise payouts queue indefinitely. Track Stripe `details_submitted=true` before scheduling payout.
- **Currency conversion for international partners** — Stripe handles; FX float in your AP forecasting.
- **Tax reporting** — US 1099 for partners > $600/yr commissions; international varies; defer to `finance-controller`.
- **Webhook delivery reliability** — Partnerstack webhooks have 99.5% delivery; for AP-critical events (commission posts), idempotent processing + reconciliation cron.
- **ACE sync failures** — Tackle abstracts but doesn't fix bad data; ACE rejects opportunities with missing DUNS or malformed company name. Pre-validate.
- **Co-sell motion misuse** — partner pushes ACE opportunities they barely qualify; AWS sellers ignore; quality bar drops. Gate by sales-stage in CRM.
- **Allbound vs Impartner UI vs API** — both have decent APIs but UI-first workflows. Plan for hybrid (Recipe-7-direct API + portal for human review).
- **Integration health digest fatigue** — weekly Slack message ignored after 4 weeks. Surface only red+yellow; let green roll up in monthly digest.
- **Cross-cloud co-sell sync** — Tackle handles each cloud; opportunity IDs differ per cloud. Maintain mapping table.
- **PRM hygiene at quarter-end vs month-end** — quarter-end is too late for some actions. Run monthly; QBR uses quarterly snapshot.
- **Orphan deal-reg expiration** can surprise partner if they assumed protected. Notify 7 days before expiration as a friendly nudge.
- **Sentry tag discipline** — engineering must always set `integration_partner_id` tag for the per-partner breakdown to work. Add to integration code review checklist.
- **Multi-partner-influenced deals** — same deal touched by 2 partners; split commission per agreement; default 60/40 first-touch / last-touch.
- **Self-serve partner portal** — Allbound/Impartner have one; Partnerstack has one. Self-serve cuts BD support load 30-50%.

## Sources

- Partnerstack API: https://partnerstack.com/api
- Tackle.io API: https://tackle.io/api-documentation
- Allbound API: https://www.allbound.com/api
- Impartner: https://www.impartner.com/
- Channeltivity: https://www.channeltivity.com/
- Magentrix: https://www.magentrix.com/
- AWS ACE: https://aws.amazon.com/partners/programs/ace/
- Microsoft Co-Sell Ready: https://learn.microsoft.com/en-us/partner-center/marketplace/co-sell-overview
- Sentry API: https://docs.sentry.io/api/
- PostHog API: https://posthog.com/docs/api
- Stripe Connect: https://docs.stripe.com/connect
- PRM hygiene patterns — Partnerstack: https://partnerstack.com/blog/partner-program-hygiene
