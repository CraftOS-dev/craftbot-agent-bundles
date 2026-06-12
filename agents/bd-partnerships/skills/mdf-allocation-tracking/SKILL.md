<!--
Source: https://partnerstack.com/blog/mdf-management + https://www.impartner.com/blog/mdf-best-practices + https://www.allbound.com/
MDF allocation + Proof of Performance + payout workflow (June 2026 SOTA).
-->
# MDF Allocation + Tracking — SKILL

Run Market Development Fund (MDF) lifecycle end-to-end: **request → approval → execution → Proof of Performance (POP) → payout**. MDF = vendor-funded co-marketing budget paid to partners against approved activities. Typical activities: events, paid ads, content production, BDR campaigns. SOTA platforms: Partnerstack (referral + MDF), Allbound, Impartner, Channeltivity, Channel Mechanics.

## When to use

- **Approving a partner MDF request** — apply approval matrix.
- **Tracking active MDF spend** — per-partner, per-quarter rollup.
- **Reviewing POP submissions** — receipts + screenshots + attendance + UTM analytics.
- **Filing partner payouts** — via Partnerstack or direct to AP.
- **Quarterly MDF reconciliation** — per-partner utilization → next-quarter allocation.
- **Trigger phrases**: "MDF request from X", "approve MDF for event", "POP review", "MDF payout", "MDF rollup", "MDF utilization".

Do NOT use this skill for: **the actual marketing activity** (use `co-marketing-campaign-design`); **commission accounting** (defer to `finance-controller`); **MDF accounting** (defer to `finance-controller`).

## Setup

```bash
export MATON_API_KEY="<key>"        # for Partnerstack / HubSpot / DocuSign
export PARTNERSTACK_API_KEY="<key>" # alt: direct
export STRIPE_SECRET_KEY="<key>"    # for Stripe Connect payouts (alternative)
# Notion for MDF request DB
# Slack channels for approval routing
```

## Common recipes

### Recipe 1: MDF request form (Notion DB schema)

```yaml
mdf_request:
  id: "MDF-2026-Q3-0042"
  partner: "Acme Solutions"
  partner_id: "acme-resel-eu"
  partner_tier: "Gold"
  submitted_by: "sarah@acme.com"
  submitted_at: "2026-06-15"
  amount_requested: 12000
  currency: "USD"
  activity_type: "event"             # event | paid_ads | content | bdr_campaign | webinar | other
  activity_description: "Sponsor 'SaaS Mid-Market Summit' London Sept 18-19, booth + 1 speaking slot"
  start_date: "2026-09-18"
  end_date: "2026-09-19"
  expected_pipeline: 350000
  expected_meetings: 30
  expected_leads: 200
  target_audience: "VP Sales + RevOps at UK/EU SaaS 100-500 employees"
  claim_period_end: "2026-10-19"     # 30 days post-event to file POP
  status: "submitted"                # submitted | approved | declined | executed | pop_received | paid | denied_pop
  approver: null
  approved_at: null
  approval_notes: null
```

### Recipe 2: MDF approval matrix (decision tree)

```yaml
mdf_approval_matrix:
  by_tier_and_amount:
    authorized:
      max_per_request: 2500
      max_per_quarter: 5000
      auto_approve_under: 1000
    silver:
      max_per_request: 7500
      max_per_quarter: 20000
      auto_approve_under: 2500
    gold:
      max_per_request: 25000
      max_per_quarter: 75000
      auto_approve_under: 5000
  required_inputs:
    - "Business case (expected pipeline + meetings + leads)"
    - "Target audience match to ICP"
    - "Claim period max 30 days post-activity"
    - "Activity start date ≥ 14 days from approval"
  escalation:
    if amount > tier_max: "VP Partnerships review"
    if amount > 50000:    "CFO sign-off"
    if activity_type=='other': "BD director review"
```

### Recipe 3: Approval routing (Slack)

```bash
# Auto-route based on Recipe 2
TIER="gold"
AMOUNT=12000
APPROVER_CHANNEL="#mdf-approvals-gold"

curl -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer $SLACK_TOKEN" -H "Content-Type: application/json" \
  -d "{
    \"channel\": \"$APPROVER_CHANNEL\",
    \"text\": \":bell: MDF request MDF-2026-Q3-0042 — Acme Solutions (Gold) — \$$AMOUNT for London Summit\",
    \"blocks\": [
      {\"type\": \"section\", \"text\": {\"type\": \"mrkdwn\", \"text\": \"*MDF Request* — MDF-2026-Q3-0042\nPartner: Acme Solutions (Gold)\nAmount: \$$AMOUNT\nActivity: London Summit booth + speaking\nExpected pipeline: \$350K\"}},
      {\"type\": \"actions\", \"elements\": [
        {\"type\":\"button\",\"text\":{\"type\":\"plain_text\",\"text\":\"Approve\"},\"value\":\"approve_MDF-2026-Q3-0042\",\"style\":\"primary\"},
        {\"type\":\"button\",\"text\":{\"type\":\"plain_text\",\"text\":\"Request Info\"},\"value\":\"info_MDF-2026-Q3-0042\"},
        {\"type\":\"button\",\"text\":{\"type\":\"plain_text\",\"text\":\"Decline\"},\"value\":\"decline_MDF-2026-Q3-0042\",\"style\":\"danger\"}
      ]}
    ]
  }"
```

Approver clicks → webhook → update Notion DB status.

### Recipe 4: Approval letter to partner

```bash
# Email partner with approval details
curl -X POST "https://gateway.maton.ai/gmail/v1/users/me/messages/send" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "raw": "<base64-mime-encoded-email>"
  }'

# Email body template
cat <<'EOF'
Subject: MDF Approved — London Summit Sept 18-19 ($12,000)

Hi Sarah,

Approved! Details:
- MDF reference: MDF-2026-Q3-0042
- Amount: $12,000 USD
- Activity: London Summit booth + speaking slot
- Claim period: complete by Oct 19, 2026
- POP requirements: see attached checklist

Reminder: spend tracked by partner; we reimburse against approved POP.

— Pat (Partnerships Lead)
EOF
```

### Recipe 5: Partnerstack MDF allocation

```bash
# Allocate MDF in Partnerstack
curl -X POST "https://gateway.maton.ai/partnerstack/v3/mdf/allocations" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "partner_id": "acme-resel-eu",
    "amount_usd": 12000,
    "activity_type": "event",
    "activity_description": "London Summit booth Sept 18-19, 2026",
    "expiration_date": "2026-10-19",
    "reference_id": "MDF-2026-Q3-0042"
  }'
```

Reference: https://partnerstack.com/api.

### Recipe 6: Proof of Performance (POP) submission requirements

```yaml
pop_requirements_by_activity:
  event:
    required:
      - "Invoices (sponsorship, booth, travel)"
      - "Booth photos (≥3, must include partner+vendor logos)"
      - "Attendee/registration list (CSV)"
      - "Lead-capture export from scanner"
      - "Speaking slot proof (event agenda + recording link if available)"
      - "Post-event summary: meetings booked, qualified leads count, follow-up plan"

  paid_ads:
    required:
      - "Ad-platform invoice (LinkedIn Ads / Google Ads / Meta)"
      - "Screenshot of campaign settings showing co-branded creative"
      - "Performance metrics: impressions, clicks, CTR, conversions"
      - "UTM-tagged landing page traffic"
      - "Leads generated + CRM source attribution"

  content:
    required:
      - "Content URL (blog post, whitepaper, video)"
      - "Co-branded asset proof"
      - "Distribution metrics: views, downloads, syndication"
      - "Lead capture: downloads with form data"
      - "Production invoice (writer, designer)"

  bdr_campaign:
    required:
      - "Target list (CSV with ICP scoring)"
      - "Sequence content (email templates, scripts)"
      - "Outreach metrics: sends, opens, replies, meetings booked"
      - "Meeting attendance + qualification outcomes"
      - "BDR salary/contractor cost allocation"

  webinar:
    required:
      - "Webinar recording (cross to partner-led-webinars-events)"
      - "Registration list + attendance"
      - "Co-branded promotional asset"
      - "Post-webinar SQLs sourced"
      - "Platform invoice (Zoom Webinars, Goldcast, etc.)"
```

### Recipe 7: POP collection (email + drop-in)

```yaml
pop_collection:
  partner_self_serve_form: "https://brand.com/partner-portal/pop-submission?ref=MDF-2026-Q3-0042"
  required_uploads:
    - "Invoices (PDF)"
    - "Photos (PNG/JPG)"
    - "Lead list (CSV)"
    - "Metrics summary (PDF or text)"
  reviewer_assignment:
    auto: "BD team rotational queue"
    sla: "5 business days from submission"
  status:
    pop_received -> pop_under_review -> approved (pay) | revisions_requested | declined
```

### Recipe 8: POP review checklist

```python
def review_pop(pop):
    checks = []

    # 1. Total spend ≤ approved amount
    if pop["spend_actual"] > pop["amount_approved"]:
        checks.append(("over_budget", "Reduce payout to approved cap"))

    # 2. All required artifacts present
    required = REQUIREMENTS[pop["activity_type"]]
    missing = [r for r in required if r not in pop["artifacts"]]
    if missing:
        checks.append(("missing_artifacts", f"Request: {missing}"))

    # 3. Co-branding visible in artifacts
    if not pop["co_branding_visible"]:
        checks.append(("no_co_branding", "Partner did not include vendor logo — decline or 50% payout"))

    # 4. Expected outcomes vs actual
    actual_pipeline = pop["leads_count"] * AVG_DEAL_SIZE
    if actual_pipeline < pop["expected_pipeline"] * 0.5:
        checks.append(("under_perform", "Under 50% of expected pipeline — flag for trend, do not block payout"))

    # 5. Claim within claim period
    if pop["submitted_at"] > pop["claim_period_end"]:
        checks.append(("late", "Past claim period — decline unless extension granted"))

    if any(c[0] in ["over_budget","missing_artifacts","no_co_branding","late"] for c in checks):
        return ("blocked", checks)
    return ("approved", checks)
```

### Recipe 9: Payout via Partnerstack

```bash
curl -X POST "https://gateway.maton.ai/partnerstack/v3/payouts/schedule" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "partner_id": "acme-resel-eu",
    "amount_usd": 12000,
    "currency": "USD",
    "reference": "MDF-2026-Q3-0042",
    "description": "MDF reimbursement — London Summit Sept 2026",
    "payment_method": "stripe_connect",
    "scheduled_for": "2026-11-01"
  }'
```

Defer accounting reconciliation to `finance-controller` via cross-agent hand-off.

### Recipe 10: Stripe Connect direct payout (no Partnerstack)

```bash
# If you don't use Partnerstack, pay directly via Stripe Connect
curl -X POST "https://api.stripe.com/v1/transfers" \
  -H "Authorization: Bearer $STRIPE_SECRET_KEY" \
  -d "amount=1200000" \
  -d "currency=usd" \
  -d "destination=acct_XXXXXX" \
  -d "description=MDF MDF-2026-Q3-0042 — Acme London Summit" \
  -d "metadata[mdf_id]=MDF-2026-Q3-0042"
```

### Recipe 11: Per-partner MDF utilization rollup (warehouse)

```sql
-- postgresql-mcp warehouse query
SELECT
  partner_name,
  partner_tier,
  SUM(amount_approved) FILTER (WHERE status IN ('approved','executed','pop_received','paid')) AS allocated,
  SUM(amount_paid) AS paid,
  SUM(amount_approved) FILTER (WHERE status='approved' AND claim_period_end < now() AND NOT status='paid') AS expired_unclaimed,
  COUNT(*) FILTER (WHERE status='paid') AS paid_count,
  ROUND(SUM(actual_pipeline_generated) / NULLIF(SUM(amount_paid),0), 2) AS pipeline_per_mdf_dollar
FROM mdf_requests
WHERE quarter='2026-Q3'
GROUP BY partner_name, partner_tier
ORDER BY paid DESC;
```

Healthy MDF ROI: $3-5 of pipeline per MDF dollar; below $2 = activity not working.

### Recipe 12: Quarterly MDF allocation rebalance

```python
# At quarter-end, recalculate next-quarter MDF pool per partner
def next_quarter_mdf(partner):
    base = TIER_BASE[partner["tier"]]    # Authorized $5K, Silver $20K, Gold $75K
    perf_multiplier = 1.0

    # Performance multiplier from prior 2 quarters
    pipeline_per_dollar = partner["last_2q_pipeline"] / max(partner["last_2q_mdf_spent"], 1)
    if pipeline_per_dollar > 5: perf_multiplier += 0.20
    elif pipeline_per_dollar > 3: perf_multiplier += 0.10
    elif pipeline_per_dollar < 1: perf_multiplier -= 0.30

    # Penalize unclaimed allocations
    unclaim_rate = partner["unclaimed_dollars"] / max(partner["allocated_dollars"], 1)
    if unclaim_rate > 0.30: perf_multiplier -= 0.20

    return round(base * perf_multiplier)
```

## Examples

### Example 1: Standard event-MDF request

**Goal:** Gold-tier reseller requests $12K for London Summit; approve + execute + pay.

**Steps:**
1. Day 0 — Partner submits Recipe 1 form in Notion.
2. Day 0 — Auto-route to `#mdf-approvals-gold` Slack (Recipe 3); business case checked.
3. Day 1 — Approved by VP Partnerships in Slack thread.
4. Day 1 — Recipe 4 approval email + Recipe 5 Partnerstack allocation.
5. Sept 18-19 — Event runs; partner collects POP.
6. Oct 5 — Partner submits POP via Recipe 7 form.
7. Oct 8 — Recipe 8 POP review by BD team; approved.
8. Oct 15 — Recipe 9 payout scheduled for Nov 1.
9. Oct 30 — Recipe 11 quarterly rollup shows 18x ROI ($220K pipeline / $12K MDF).

**Result:** Clean lifecycle; partner sees consistent process; finance reconciles cleanly.

### Example 2: POP declined for missing artifacts

**Goal:** Partner submits POP missing booth photo + lead list.

**Steps:**
1. Recipe 8 review flags `missing_artifacts`.
2. Notion status → `revisions_requested`; auto-email partner with specific gaps.
3. Partner re-submits within 7 days with full artifacts.
4. Re-review → approved.
5. Payout scheduled.

**Result:** Standard process keeps quality bar; partner learns rigor for next cycle.

### Example 3: Mid-quarter MDF reallocation

**Goal:** Gold partner has $30K unspent at Q-mid; reallocate to higher-performing Silver partner.

**Steps:**
1. Recipe 11 rollup shows Gold partner pipeline-per-dollar = 1.2 (under-performing).
2. Silver partner #2 has pipeline-per-dollar = 6.8 (over-performing) but hit tier-quarter cap.
3. VP Partnerships approves discretionary reallocation: $15K from Gold to Silver #2.
4. Recipe 5 amends both allocations in Partnerstack.
5. Both partners notified.

**Result:** Dollars flow to where they generate pipeline; budget not wasted.

## Edge cases / gotchas

- **POP without co-branding is a discipline failure** — partner used MDF to promote themselves only. Pay 50% or decline; address in next QBR.
- **Auto-approval under $1K creates over-allocation risk** — set a partner-level cap to prevent spam.
- **Currency conversion** for non-USD requests: use approved date FX rate (not POP date). Document in approval letter.
- **Tax treatment**: in some jurisdictions, MDF reimbursement is taxable income to partner. Issue 1099 (US) or equivalent; defer to `finance-controller`.
- **Lead-attribution dispute** — partner claims pipeline that vendor's direct team already had. Require lead-source attribution in POP CRM data.
- **Claim period extension** — sometimes legitimate (event date slipped). Document approval; max 30-day extension.
- **POP under partner control** — partner may inflate metrics. Spot-check 10% of POPs via direct CRM query against the partner-claimed leads.
- **Late POP submissions** — common during Q-end crunch. Standard SLA: decline if past claim period. Exception only with VP approval.
- **Over-budget actual spend** — partner pays the delta; vendor never reimburses above approved amount.
- **Refunded/cancelled events** — pro-rate POP and claw back MDF for the cancelled portion.
- **Multi-party events** — three partners co-sponsor; MDF split = each pays their share + claims pro-rata.
- **MDF for "soft" outcomes** (brand awareness, evangelism) is hard to POP-verify — require concrete metric proxies (impressions, content downloads, follow-up demos).
- **MDF and commissions are separate** — same partner can claim MDF AND commission on resulting deal. Don't conflate.
- **Partnerstack vs direct AP** — small partner count (<10), direct AP via Stripe Connect cheaper; >20 partners, Partnerstack saves time.
- **Audit trail** — every MDF request + approval + POP + payout link must persist in Notion AND finance system. Cross-reference IDs (Recipe 1's `id` propagates).
- **Tier downgrade mid-quarter** — partner approved at Gold tier MDF but downgraded to Silver mid-quarter. Honor prior approvals; reallocate forward.
- **No-show event** — partner paid for sponsorship but didn't attend (force majeure). Pro-rate POP for tangible deliverables (booth setup, materials).

## Sources

- Partnerstack MDF management blog: https://partnerstack.com/blog/mdf-management
- Partnerstack API: https://partnerstack.com/api
- Impartner MDF best practices: https://www.impartner.com/blog/mdf-best-practices
- Allbound PRM: https://www.allbound.com/
- Channel Mechanics: https://www.channelmechanics.com/
- Stripe Connect payouts: https://docs.stripe.com/connect
- MDF program design — Forrester: https://www.forrester.com/blogs/category/channel-partner-programs/
- Canalys channel research — MDF benchmarks: https://www.canalys.com/insights/
