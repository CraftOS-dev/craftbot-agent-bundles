<!--
Source: https://stripe.com/docs/api/subscriptions + https://developers.pandadoc.com/ + https://developers.docusign.com/ + https://help.mixmax.com/ + https://developers.outreach.io/api/
-->
# Renewal Management — 90-Day Prep — SKILL

T-90 / T-60 / T-30 / T-7 cadence pre-renewal. T-90: classify risk + forecast probability. T-60: QBR with renewal pricing intro. T-30: contract draft via PandaDoc + uplift pricing via xlsx. T-7: e-sign via DocuSign + Slack pin renewal status. T-0: subscription renewed in Stripe. Mixmax orchestrates touchpoint cadence. Notion board tracks pipeline status.

## When to use

- **Renewal date approaching** — 90 days out, classification + cadence kicks in.
- **Yellow/Red customer renewal** — extra care: save play kicks in alongside renewal prep.
- **Multi-year renewal** — bigger contract, more redlining, longer prep.
- **Tier-uplift renewal** — Growth -> Enterprise, includes price uplift + new SKU.
- **Auto-renew vs negotiated** — Auto-renew customers still get T-90 cadence (advance notice obligation).

This skill **integrates with** `customer-health-scoring-vitally-catalyst-churnzero` (T-90 risk classification), `expansion-opportunity-identification` (T-60 expansion packaging), `churn-save-motion-intervention` (T-90 save play if Red), and `nrr-grr-ownership-metrics` (forecast accuracy logging).

Trigger phrases: "renewal", "T-90", "T-60", "T-30", "T-7", "renewal cadence", "uplift", "PandaDoc", "DocuSign envelope", "contract send".

## Setup

```bash
# Stripe (subscription state)
# stripe-mcp wired in agent.yaml

# PandaDoc (SMB proposals)
export PANDADOC_API_KEY="<key>"

# DocuSign (enterprise e-sign)
export DOCUSIGN_BASE_URL="https://demo.docusign.net/restapi"
export DOCUSIGN_ACCOUNT_ID="<account-id>"
export DOCUSIGN_TOKEN="<jwt>"

# Ironclad (CLM)
export IRONCLAD_API_KEY="<key>"

# Mixmax (CSM cadence)
export MIXMAX_API_KEY="<key>"

# Outreach (alt cadence)
export OUTREACH_TOKEN="<oauth>"
```

Workspace prerequisites:
- Postgres view `renewals_upcoming_180d` joining `stripe_subscriptions.current_period_end` with `customers`.
- Notion "Renewal Board" DB with schema: Customer, Renewal Date, Risk (Green/Yellow/Red), Stage (T-90 / T-60 / T-30 / T-7 / Renewed / Churned), Owner, Forecast (probability + ARR), Notes.
- PandaDoc template "Renewal Proposal v3" with variables: `{{ customer.name }}`, `{{ pricing.base }}`, `{{ pricing.uplift_pct }}`, `{{ pricing.seats }}`.
- Slack channel `#renewals` + `#renewal-saves` (approval gate).

## Cadence at a glance

| T-X | Action | Tool | Output |
|---|---|---|---|
| T-90 | Risk classification (G/Y/R) | health + Stripe + CSP | Risk tag in renewal board |
| T-90 | Forecast probability | composite signal | NRR forecast |
| T-60 | QBR with renewal intro | `qbr-scheduling-facilitation` | Deck + customer buy-in |
| T-60 | Save play if Red | `churn-save-motion-intervention` | Exec outreach + offer |
| T-30 | Contract draft | `cli-anything` PandaDoc + `xlsx` pricing | Proposal sent |
| T-30 | Approval routing | Notion renewal board | Internal sign-off |
| T-7 | E-sign send | `cli-anything` DocuSign | Envelope sent |
| T-7 | Slack pin status | `slack-mcp` | CSM channel update |
| T-0 | Renewal closed | `stripe-mcp` + `notion-mcp` | Subscription renewed |
| T+1 | Handoff to expansion | `expansion-opportunity-identification` | Next-phase plan |

## Common recipes

### Recipe 1: Pull upcoming renewals from Stripe

```bash
# Subscriptions with current_period_end in next 90 days
curl -sS "https://api.stripe.com/v1/subscriptions?status=active&limit=100" \
  -u "$STRIPE_SECRET_KEY:" | jq '.data[] | select(.current_period_end < (now + 90*86400)) | {
    customer,
    current_period_end: (.current_period_end | strftime("%Y-%m-%d")),
    mrr: ([.items.data[].plan.amount] | add / 100),
    interval: .items.data[0].plan.interval
  }'
```

Or via `stripe-mcp subscription_list` with filtering.

### Recipe 2: T-90 risk classification

```sql
WITH renewal_candidates AS (
  SELECT customer_id, current_period_end::date AS renewal_date,
         (current_period_end::date - CURRENT_DATE) AS days_to_renewal
  FROM stripe_subscriptions
  WHERE status = 'active'
    AND current_period_end::date BETWEEN CURRENT_DATE + INTERVAL '85 days' AND CURRENT_DATE + INTERVAL '95 days'
)
SELECT
  rc.customer_id, c.name, c.tier, c.arr,
  rc.renewal_date, rc.days_to_renewal,
  h.health_score,
  h.health_score_trend_30d,
  CASE
    WHEN h.health_score < 0.4 THEN 'Red'
    WHEN h.health_score < 0.6 AND h.health_score_trend_30d < -0.05 THEN 'Red'
    WHEN h.health_score < 0.7 THEN 'Yellow'
    WHEN h.health_score_trend_30d < -0.05 THEN 'Yellow'
    ELSE 'Green'
  END AS risk
FROM renewal_candidates rc
JOIN customers c USING (customer_id)
LEFT JOIN health_scores h USING (customer_id);
```

For each row, push to Notion renewal board + Slack `#renewals` summary.

### Recipe 3: Forecast probability

```python
# Logistic-style probability
def forecast(health, trend, sponsor_active, save_play_running):
    base = {"Green": 0.95, "Yellow": 0.70, "Red": 0.40}[risk]
    if save_play_running: base += 0.10
    if not sponsor_active: base -= 0.15
    return max(0.05, min(0.99, base))
```

Write to `renewal_forecasts` table; later compare to actuals via `nrr-grr-ownership-metrics` Recipe 11.

### Recipe 4: T-60 QBR positioning

Invoke `qbr-scheduling-facilitation` skill. Adjust slide 11 (renewal outlook): show forecast classification + 3 commercial options.

Three commercial options template:
- Option A: Renew flat (CPI uplift only, ~3-7%)
- Option B: Renew with multi-year discount (3-yr at -3%)
- Option C: Renew with seat expansion (current uplift + new seats)

### Recipe 5: T-60 Save play if Red

Invoke `churn-save-motion-intervention`. Save plan must be tracked in Notion renewal board + Linear "save plan" issue.

### Recipe 6: T-30 Build renewal pricing in xlsx

```
| Item | Current | Renewal | Delta | Notes |
| Base subscription | $50,000 | $53,500 | +7% | CPI uplift |
| Seat expansion | 50 -> 75 | +25 * $1,000 | +$25,000 | new headcount |
| Multi-product add | - | +$15,000 | +$15,000 | new SKU "Analytics" |
| Multi-year discount | - | -3% | -$2,805 | 3-yr commit |
| Total ACV | $50,000 | $90,695 | +$40,695 (+81%) | |
```

Use `xlsx` skill with template `renewal-pricing-v2.xlsx`.

### Recipe 7: T-30 Generate PandaDoc proposal

```bash
curl -sS -X POST "https://api.pandadoc.com/public/v1/documents" \
  -H "Authorization: API-Key $PANDADOC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Renewal 2027",
    "template_uuid": "'$RENEWAL_TEMPLATE_UUID'",
    "recipients": [
      {"email": "champion@acme.com", "first_name": "Jane", "last_name": "Doe", "role": "Signer"}
    ],
    "tokens": [
      {"name": "Customer.Name", "value": "Acme Corp"},
      {"name": "Pricing.Base", "value": "$53,500"},
      {"name": "Pricing.Seats", "value": "75"},
      {"name": "Pricing.MultiYear", "value": "3 years"},
      {"name": "Pricing.Total", "value": "$90,695"}
    ]
  }'
```

Doc: https://developers.pandadoc.com/reference/document-from-template

### Recipe 8: T-30 Internal approval routing

```python
# Notion update + Slack approval thread
slack.chat_postMessage(
    channel="#renewal-approvals",
    text=f"""
:scroll: Renewal approval needed: {customer_name}
ACV: ${acv:,.0f} ({pct_change:+.0%} vs current)
Multi-year: {multi_year}
Health: {risk} ({health:.2f})
Owner: {csm_owner}
PandaDoc preview: {pandadoc_url}
React :white_check_mark: to approve / :x: to reject.
"""
)
```

Track approver in Notion renewal board.

### Recipe 9: T-7 Send DocuSign envelope

```bash
# Create envelope
curl -sS -X POST "$DOCUSIGN_BASE_URL/v2.1/accounts/$DOCUSIGN_ACCOUNT_ID/envelopes" \
  -H "Authorization: Bearer $DOCUSIGN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "emailSubject": "Acme Renewal 2027 - Signature requested",
    "documents": [{"documentBase64": "'$(base64 contract.pdf)'", "name": "Renewal.pdf", "fileExtension": "pdf", "documentId": "1"}],
    "recipients": {
      "signers": [{
        "email": "signer@acme.com",
        "name": "Jane Doe",
        "recipientId": "1",
        "tabs": {
          "signHereTabs": [{"anchorString": "/sig1/", "anchorYOffset": "10"}]
        }
      }]
    },
    "status": "sent"
  }'
```

Doc: https://developers.docusign.com/docs/esign-rest-api/

### Recipe 10: Mixmax cadence enrollment

```bash
# Enroll customer champion into "Renewal T-30 Cadence"
curl -sS -X POST "https://api.mixmax.com/v1/sequences/$SEQUENCE_ID/enrollments" \
  -H "X-API-Token: $MIXMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"recipient": {"email": "champion@acme.com", "name": "Jane Doe"}, "variables": {"renewal_date": "2026-09-15", "acv": "$90,695"}}'
```

Doc: https://help.mixmax.com/

Outreach equivalent:
```bash
curl -sS -X POST "https://api.outreach.io/api/v2/sequenceStates" \
  -H "Authorization: Bearer $OUTREACH_TOKEN" \
  -d '{"data": {"type": "sequenceState", "relationships": {"sequence": {"data": {"type": "sequence", "id": "'$SEQ_ID'"}}, "prospect": {"data": {"type": "prospect", "id": "'$PROSPECT_ID'"}}}}}'
```

### Recipe 11: T-7 Slack pin renewal status

```python
slack.chat_postMessage(
    channel="#renewals",
    text=f"""
:lock: T-7 status: {customer_name}
Stage: Envelope sent (DocuSign #{envelope_id})
Signer: {signer_name}
ACV: ${acv:,.0f}
Forecast: {forecast_pct:.0%} probability
"""
)
# Pin the message
slack.pins_add(channel=channel_id, timestamp=message_ts)
```

### Recipe 12: T-0 Close + handoff

```bash
# Stripe webhook customer.subscription.updated triggers
# Verify subscription renewed
curl -sS "https://api.stripe.com/v1/subscriptions/$SUB_ID" \
  -u "$STRIPE_SECRET_KEY:" | jq '.current_period_end, .status'

# Update Notion
notion.update_page(page_id=renewal_page, properties={
    "Stage": {"status": {"name": "Renewed"}},
    "Renewed Date": {"date": {"start": today}},
    "ACV (Final)": {"number": final_acv},
})

# Handoff to next-cycle expansion plan
# Fire expansion-opportunity-identification reset for this customer
```

### Recipe 13: Forecast accuracy logging

After every renewal closed, write to `renewal_forecasts`:
- Forecast at T-90, T-60, T-30 (was forecast Green/Yellow/Red with what probability)
- Actual outcome (Renewed / Churned / Extended)
- Final ACV
- Time to close (vs estimated)

Recipe 11 in `nrr-grr-ownership-metrics` reads this.

## Examples

### Example 1: Green renewal happy path

**Goal:** Acme is Green; T-90 cadence to T-0 close, hands-off.

**Steps:**
1. T-90: Recipe 2 - Green. Recipe 3 - 95% probability. Recipe 10 - enrolled in Green cadence.
2. T-60: Recipe 4 - QBR with renewal slide. Recipe 6 - pricing previewed.
3. T-30: Recipe 7 - PandaDoc proposal sent. Recipe 8 - internal approval thread.
4. T-7: Recipe 9 - DocuSign envelope. Recipe 11 - Slack pin.
5. T-0: Recipe 12 - Stripe confirms; Notion updated; renewal closed.
6. T+1: Recipe 13 - forecast accuracy logged. Expansion handoff fired.

**Result:** Hands-off renewal; forecast accuracy maintained.

### Example 2: Yellow customer rescued mid-cycle

**Goal:** Acme classified Yellow T-90; T-60 save play recovers them.

**Steps:**
1. T-90: Recipe 2 - Yellow (health 0.55, trend -0.08). Forecast 70%.
2. T-90: `churn-save-motion-intervention` fired alongside Recipe 4.
3. T-60: QBR + save call combined. Exec sponsor engaged. Roadmap commitment (Linear ticket) made.
4. T-30: Save play log shows health rebounded to 0.71. Reclassify Green; forecast 90%.
5. T-30: Recipe 7 - PandaDoc; Recipe 10 - cadence enrollment.
6. T-7 - T-0: standard close.

**Result:** Save play surfaced at T-90 prevented a late T-30 surprise.

## Edge cases / gotchas

- **Auto-renew customers still need T-90 cadence** — many contracts require advance notice; failing to send T-90 email may constitute auto-renewal in legalese the customer didn't consent to. Risk.
- **Renewal date not in Stripe** — enterprise customers on NetSuite/Zuora; Stripe doesn't have current_period_end. Pull from CPQ or contract source-of-truth.
- **Multi-product customer one renewal date** — bundle into one envelope; multiple line items.
- **Customer on a calendar-year renewal** — Q4 renewal volume is brutal; staff CSM team accordingly.
- **PandaDoc template drift** — if Legal updates terms, every template needs update; otherwise old terms send. Quarterly template audit.
- **DocuSign envelope expired** — 60-day default expiry. If customer sits on it past 60d, re-send.
- **Approval thread goes cold** — Slack approver out of office. Force escalation rule: 24h no response -> auto-ping VP.
- **Mixmax/Outreach cadence collision** — if customer is also on a marketing nurture, double-touched. Coordinate with marketing-agent before enroll.
- **Forecast accuracy < 95%** — model needs re-tuning; consult validation in `customer-health-scoring`.
- **Churn at T-7 (after envelope sent)** — customer pulls out. Pause envelope; route to `churn-save-motion-intervention` final-week save play.
- **Multi-year discount negotiation** — finance-controller may have a floor (e.g., min discount -3%); don't promise -10% without approval gate.
- **CSP renewal date drift** — if Vitally has 2026-09-15 and Stripe has 2026-09-22, sync to Stripe (source-of-truth for billing).

## Sources

- [Stripe Subscriptions API](https://stripe.com/docs/api/subscriptions)
- [Stripe webhooks customer.subscription.updated](https://stripe.com/docs/api/events/types#event_types-customer.subscription.updated)
- [PandaDoc API - document from template](https://developers.pandadoc.com/reference/document-from-template)
- [PandaDoc docs](https://developers.pandadoc.com/)
- [DocuSign eSignature REST API](https://developers.docusign.com/docs/esign-rest-api/)
- [DocuSign create envelope](https://developers.docusign.com/docs/esign-rest-api/reference/envelopes/envelopes/create/)
- [Ironclad CLM API](https://developer.ironcladapp.com/)
- [Mixmax API sequences](https://help.mixmax.com/hc/en-us/categories/360000056772-API)
- [Outreach Sequence States API](https://developers.outreach.io/api/reference/SequenceState)
- [Salesforce CPQ docs](https://developer.salesforce.com/docs/atlas.en-us.cpq_dev_api.meta/cpq_dev_api/)
- [Zuora Subscription API](https://www.zuora.com/developer/api-references/)
