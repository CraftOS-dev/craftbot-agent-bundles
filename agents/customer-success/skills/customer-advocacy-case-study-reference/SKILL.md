<!--
Source: https://docs.influitive.com/ + https://help.slapfive.com/ + https://help.userevidence.com/ + https://app.delighted.com/docs/api + https://help.tremendous.com/
-->
# Customer Advocacy — Case Study / Reference / G2 — SKILL

Trigger advocacy on Delighted-fed promoter list (NPS >= 9 or CSAT 5/5 or 1yr+ anniversary). Invite via Gmail templated outreach. Book reference calls via Calendly. Draft case studies via docx skill from Fathom transcripts. Track in Influitive (paid) or Notion advocacy tracker (free). Reward via Stripe credit, Tremendous gift card, or service credit.

## When to use

- **Active sales opp needs reference** — book reference call within 5 business days.
- **Promoter signal detected** — NPS 9-10 -> invite within 7 days.
- **Marketing wants new case studies** — pull 3-month promoter cohort + match to ICP.
- **G2 review push** — quarterly drive 10+ G2 reviews from happy customers.
- **CAB member ask** — CAB customers often advocate beyond reference.
- **Anniversary milestone** — customer hits 1yr/2yr; invite to share their story.

This skill **reads from** `nps-csat-ces-tracking` (promoter list) and `customer-milestone-anniversary` (milestone triggers). It **feeds** marketing-agent (case study assets) and sales-agent (reference call inventory).

Trigger phrases: "advocacy", "case study", "reference call", "G2 review", "promoter", "customer story", "Influitive challenge".

## Setup

```bash
# Influitive (paid, AdvocateHub)
export INFLUITIVE_API_TOKEN="<token>"
export INFLUITIVE_SUBDOMAIN="acme"

# Slapfive (case studies + reference)
export SLAPFIVE_API_KEY="<key>"

# UserEvidence (customer evidence)
export USEREVIDENCE_API_KEY="<key>"

# Champion (alt advocacy)
export CHAMPION_API_KEY="<key>"

# Delighted (promoter list source)
export DELIGHTED_API_KEY="<key>"

# Tremendous (reward fulfillment)
export TREMENDOUS_API_KEY="<key>"

# Stripe credit fallback - via stripe-mcp
```

Workspace prerequisites:
- Notion "Advocacy Tracker" DB with: Customer, Promoter Name, Promoter Email, Source (NPS / CSAT / Anniversary), Last Asked, Ask Type (G2 / Reference / Case Study / Speaking), Status (Invited / Accepted / Completed / Declined), Reward, Reward Status, Outcome Asset (URL).
- 6-month cooldown rule on per-customer asks.
- Approval rules for rewards (CSM Lead approves > $100 reward).

## Ask priority

1. **G2 / Capterra review** — easiest ask, high SEO + sales collateral value.
2. **Reference call** — for active sales opps; book via Calendly.
3. **Case study** — higher commitment; full draft via docx.
4. **Conference speaking** — opt-in only; highest commitment.

## Reward tier

| Ask | Reward |
|---|---|
| G2 review | $50 Tremendous gift card OR 1-month credit |
| Reference call | $100 gift card OR 1-month credit |
| Case study | $250 gift card OR 3-month credit + 5% renewal discount |
| Speaking | Travel + custom acknowledgement |

## Common recipes

### Recipe 1: Pull promoter list from Delighted

```bash
# Last 30 days NPS responses, score 9-10
curl -sS "https://api.delighted.com/v1/responses?score=9..10&since=$(date -u -d '30 days ago' +%s)&expand=person" \
  -u "$DELIGHTED_API_KEY:" | jq '.[] | {
    email: .person.email,
    name: .person.name,
    score,
    comment,
    created_at: (.created_at | strftime("%Y-%m-%d"))
  }'
```

Doc: https://app.delighted.com/docs/api

### Recipe 2: Filter to eligible promoters (cooldown check)

```sql
SELECT p.email, p.name, p.comment, p.score, p.created_at
FROM delighted_promoters p
LEFT JOIN advocacy_tracker a ON a.promoter_email = p.email
WHERE p.score >= 9
  AND p.created_at >= now() - INTERVAL '14 days'
  AND (a.last_asked IS NULL OR a.last_asked < now() - INTERVAL '6 months')
ORDER BY p.created_at DESC;
```

6-month cooldown prevents asking the same person every quarter.

### Recipe 3: Draft personalized advocacy invite

```python
prompt = f"""
Draft a 5-sentence advocacy invite email.

Promoter: {p.name} ({p.email})
Score: {p.score}/10
Their NPS comment: "{p.comment}"

Asks (combined in one email):
1. G2 review (5 min, link below).
2. Open to a 30-min conversation about their use case for a customer story?

Rules:
- Reference their specific comment.
- No "Hope you're doing well." No "Just touching base."
- Sign-off as {csm.name}.
- Calendly link: {calendly_url}
- G2 review link: {g2_link}
"""
body = claude.generate(prompt)
gmail.send_email(to=[p.email], subject=f"{p.name} - 5 min thanks", body=body)
```

### Recipe 4: Push to Influitive as a challenge invitation

```bash
curl -sS -X POST "https://acme.influitive.com/api/v1/members/$MEMBER_ID/challenges/$CHALLENGE_ID/activities" \
  -H "Authorization: Token token=$INFLUITIVE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "completed": false,
    "metadata": {"source": "nps_promoter", "score": 10}
  }'
```

Doc: https://docs.influitive.com/

### Recipe 5: Slapfive case study workflow

```bash
# Create case study project
curl -sS -X POST "https://api.slapfive.com/v1/projects" \
  -H "Authorization: Bearer $SLAPFIVE_API_KEY" \
  -d '{
    "customer_id": "'$CUSTOMER_ID'",
    "project_type": "case_study",
    "champion_email": "'$PROMOTER_EMAIL'"
  }'
```

Doc: https://help.slapfive.com/

### Recipe 6: UserEvidence quote collection

```bash
curl -sS -X POST "https://api.userevidence.com/v1/quotes" \
  -H "X-API-Key: $USEREVIDENCE_API_KEY" \
  -d '{
    "customer_email": "'$PROMOTER_EMAIL'",
    "campaign_id": "'$CAMPAIGN_ID'",
    "context": "NPS 10 - {{quote from NPS comment}}"
  }'
```

### Recipe 7: Book reference call via Calendly

```bash
curl -sS -X POST "https://api.calendly.com/scheduling_links" \
  -H "Authorization: Bearer $CALENDLY_TOKEN" \
  -d '{
    "max_event_count": 1,
    "owner": "https://api.calendly.com/event_types/'$REFERENCE_CALL_EVENT_TYPE'",
    "owner_type": "EventType"
  }' | jq -r '.resource.booking_url'
```

For active sales opps, the prospect company's contact (not the customer's) books the slot.

### Recipe 8: Draft case study from Fathom transcript

```bash
# Pull customer interview transcript
curl -sS "https://api.fathom.video/external/v1/meetings/$MEETING_ID/transcript" \
  -H "X-Api-Key: $FATHOM_API_KEY" > interview.txt
```

```python
# Claude drafts case study from transcript
prompt = f"""
Draft a 1-page customer case study from this interview transcript.

Customer: {customer.name}
Industry: {customer.industry}
Use case: {customer.use_case}

Structure:
- Challenge (problem before adopting product)
- Solution (how product addressed it)
- Results (3 specific metrics with numbers)
- Verbatim quote from champion (most powerful one in transcript)

Tone: customer voice, not vendor voice. Reuse customer's own language.
"""
draft = claude.generate(prompt, attachments=["interview.txt"])
docx.write("case-study-acme-2026Q2.docx", content=draft)
```

### Recipe 9: Send G2 review reminder (no response 7d)

If invited but didn't review, gentle nudge after 7d:

```python
gmail.send_email(
    to=[p.email],
    subject=f"5 min for {p.name}?",
    body=f"""
Hi {p.name},

Quick nudge - any chance you have 5 min for a G2 review? Means a lot.

{g2_link}

Either way, no follow-up after this.

- {csm.name}
"""
)
```

One nudge only. Don't pester.

### Recipe 10: Issue reward (Tremendous gift card)

```bash
curl -sS -X POST "https://testflight.tremendous.com/api/v2/orders" \
  -H "Authorization: Bearer $TREMENDOUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "external_id": "advocacy-'$ADVOCACY_ID'",
    "payment": {"funding_source_id": "'$FUNDING_SOURCE_ID'"},
    "rewards": [{
      "value": {"denomination": 100, "currency_code": "USD"},
      "campaign_id": "'$CAMPAIGN_ID'",
      "recipient": {"email": "'$PROMOTER_EMAIL'", "name": "'$PROMOTER_NAME'"}
    }]
  }'
```

Doc: https://help.tremendous.com/

### Recipe 11: Issue Stripe service credit (free reward path)

```bash
# 1-month service credit for reference call
curl -sS -X POST "https://api.stripe.com/v1/customers/$STRIPE_CUSTOMER_ID/balance_transactions" \
  -u "$STRIPE_SECRET_KEY:" \
  -d "amount=-10000" \
  -d "currency=usd" \
  -d "description=Advocacy reward: G2 review credit"
```

### Recipe 12: Track in Notion advocacy tracker

```python
notion.create_page(
    parent={"database_id": ADVOCACY_DB_ID},
    properties={
        "Customer": {"title": [{"text": {"content": customer.name}}]},
        "Promoter": {"rich_text": [{"text": {"content": p.name}}]},
        "Promoter Email": {"email": p.email},
        "Source": {"select": {"name": "NPS"}},
        "Ask Type": {"multi_select": [{"name": "G2"}, {"name": "Case Study"}]},
        "Status": {"status": {"name": "Invited"}},
        "Last Asked": {"date": {"start": today}},
        "Outcome Asset": {"url": ""},
        "Reward": {"select": {"name": "$50 Tremendous"}},
        "Reward Status": {"status": {"name": "Pending completion"}},
    },
)
```

### Recipe 13: Quarterly advocacy reporting

```sql
SELECT
  ask_type,
  count(*) AS invited,
  count(*) FILTER (WHERE status = 'Completed') AS completed,
  100.0 * count(*) FILTER (WHERE status = 'Completed') / count(*)::numeric AS completion_pct,
  count(*) FILTER (WHERE outcome_asset_url IS NOT NULL) AS assets_published
FROM advocacy_tracker
WHERE invited_date >= now() - INTERVAL '90 days'
GROUP BY ask_type;
```

## Examples

### Example 1: NPS 10 -> G2 review within 14 days

**Goal:** Customer scored 10 on NPS Tuesday; reviewed on G2 by next Friday.

**Steps:**
1. Tuesday 23:00 UTC: Recipe 1 pulls scores; Acme.Jane scored 10 with great comment.
2. Wednesday 06:00 UTC: Recipe 2 confirms cooldown met (Jane last asked 18 months ago).
3. Wednesday 09:00 UTC: Recipe 3 drafts personalized invite; Recipe 12 logs in Notion.
4. Wednesday 14:00 UTC: CSM reviews + sends.
5. Wednesday + 7d: no response, Recipe 9 nudge.
6. Wednesday + 14d: G2 review published. Recipe 10 issues $50 Tremendous gift card.

**Result:** New G2 review, happy customer rewarded, asset captured.

### Example 2: Sales opp needs Tier-1 reference next week

**Goal:** Sales has a $200k deal needing a Tier-1 reference call by next Tuesday.

**Steps:**
1. Slack: "/reference acme-style enterprise SaaS finance vertical"
2. Skill queries Notion advocacy tracker for: tier=Enterprise, vertical=Finance, last_reference > 90d ago, status=Completed.
3. Returns top 5 candidates.
4. CSM Lead picks one (say, Acme); Recipe 7 generates reference Calendly link.
5. Recipe 3 outreach to Acme champion: "Quick favor - have a customer who'd benefit from your story. 30 min next Tue/Wed?"
6. Customer accepts; reference call held; Recipe 12 logs.

**Result:** Reference inventory used efficiently; sales opp supported.

## Edge cases / gotchas

- **Promoter cooldown** — 6 months minimum between asks per person; otherwise advocate fatigue.
- **Reward tax implications** — gift cards > $600/yr per US recipient = 1099. Track via Tremendous; consult finance.
- **G2 / Capterra review policies** — incentivized reviews must be disclosed; check current G2 ToS before paying for reviews.
- **Customer NDA constraints** — some customers can't publicly share. Track "anonymous reference OK?" in Notion; respect at every step.
- **Case study draft must go through customer approval** — never publish without explicit sign-off. Build approval step into Recipe 8.
- **Champion left customer org** — promoter no longer at the company. Verify before reaching out; otherwise embarrassing.
- **Speaking opt-in** — never auto-invite to conference speaking. Only follow up if customer raised it.
- **AE/CSM friction on reference inventory** — AEs hoard references; CSMs guard relationships. Notion advocacy tracker is shared SOT; rule = first-come-first-served-on-availability.
- **Reward fulfillment delay** — Tremendous can take 24h to deliver; manage expectations ("Gift card on its way!").
- **Slapfive/Influitive cost** — for low-volume programs (<5 case studies/year), Notion + Calendly + Tremendous is enough.
- **Influitive challenge friction** — adds points game layer; some customers love it, some find it cringe. Survey CAB members before deploying.
- **Anniversary milestone bot collisions** — customer-milestone-anniversary skill may also send congrats email; coordinate via Notion to avoid double-touch.

## Sources

- [Influitive Advocate API](https://docs.influitive.com/)
- [Slapfive help](https://help.slapfive.com/)
- [UserEvidence docs](https://help.userevidence.com/)
- [Champion advocacy platform](https://www.championhq.io/)
- [Delighted Responses API](https://app.delighted.com/docs/api)
- [Calendly scheduling links](https://developer.calendly.com/api-docs/)
- [Fathom API](https://help.fathom.video/en/articles/8430832-fathom-api)
- [Tremendous Orders API](https://help.tremendous.com/hc/en-us/categories/360002107552-API)
- [Stripe customer balance transactions](https://stripe.com/docs/api/customer_balance_transactions)
- [G2 Customer Reviews policy](https://documentation.g2.com/)
