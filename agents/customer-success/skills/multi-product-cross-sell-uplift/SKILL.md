<!--
Source: https://developers.klaviyo.com/ + https://customer.io/docs/api/ + https://api.iterable.com/api/docs + https://developers.outreach.io/api/ + https://developers.salesloft.com/api.html + https://developers.hubspot.com/docs/api/crm/sequences + https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/ + https://help.mixmax.com/hc/en-us
-->
# Multi-Product Cross-Sell + Uplift — Klaviyo / Customer.io / Outreach / HubSpot / Salesforce — SKILL

Cross-sell secondary SKUs (modules, add-ons, new products) and uplift existing-SKU expansion to customers who hit usage / adoption / health signals. Cohort identification via PostHog + CSP; sequence orchestration via Klaviyo (product-led email), Customer.io (in-product lifecycle), Outreach / Salesloft (sales-engagement multi-touch), HubSpot/Salesforce sequences (CRM-native). Co-owns motion with `expansion-opportunity-identification` and AE-led close.

## When to use

- **Customer hit feature-limit / multi-workspace / integration adoption** — usage signal -> cross-sell sequence.
- **Multi-product launch** — new SKU/module is available; eligible existing customers get a sequence.
- **Plan-upgrade nudge** — Growth-tier customer with usage > 80% of cap -> Enterprise upgrade sequence.
- **Re-bundling motion** — customer on 2 SKUs; offer bundle pricing for 3.
- **Vertical-specific expansion** — Finance vertical, 3 high-fit customers on base SKU + 1 new finance-module SKU.
- **Renewal cycle uplift** — T-90 from renewal, customer is expansion-ready -> sequence runs through renewal.

This skill **reads from** `expansion-opportunity-identification` (composite expansion signal) and `customer-health-scoring` (health gate). It **feeds** `sales-agent` (AE-led close handoff for > $50k uplift) and `renewal-management-90-day-prep` (commit numbers fed into renewal pricing).

Trigger phrases: "cross-sell", "multi-product", "expansion sequence", "Klaviyo flow", "Customer.io campaign", "Outreach sequence", "Salesloft cadence", "HubSpot sequence", "uplift", "upsell sequence", "Iterable flow".

## Setup

```bash
# Klaviyo (product-led lifecycle email - SOTA for SaaS expansion)
export KLAVIYO_API_KEY="<key>"

# Customer.io (in-product trigger-based)
export CUSTOMERIO_SITE_ID="<site-id>"
export CUSTOMERIO_API_KEY="<key>"
export CUSTOMERIO_REGION="us"  # or "eu"

# Iterable (enterprise lifecycle)
export ITERABLE_API_KEY="<key>"

# Outreach (multi-touch sales engagement)
export OUTREACH_API_TOKEN="<token>"
export OUTREACH_ORG_ID="<org-id>"

# Salesloft (alt sales engagement)
export SALESLOFT_API_KEY="<key>"

# HubSpot (CRM-native sequences)
export HUBSPOT_TOKEN="<token>"

# Salesforce (CRM-native cadence + tasks)
export SF_INSTANCE_URL="https://acme.my.salesforce.com"
export SF_ACCESS_TOKEN="<bearer>"

# Mixmax (CSM-led personalized cadence)
export MIXMAX_API_TOKEN="<token>"

# PostHog (cohort) - via posthog-mcp
# CSP (Vitally / Catalyst) - via cli-anything curl
# Gmail (CSM 1:1 outreach) - via gmail-mcp
```

Workspace prerequisites:
- Cross-sell catalog defined in Notion: per-SKU eligibility rules, target ARR, sequence ID, AE owner.
- Klaviyo / Customer.io profile properties wired (tier, current_skus, usage_score, expansion_score).
- Outreach / Salesloft sequences pre-built by RevOps; this skill enrolls + reports.
- Approval gate: > $50k uplift = AE-led; $10-50k = CSM-led with AE FYI; < $10k = CSM-only.
- Suppression list: Recent objections, churn risk Red, marketing-opt-out customers.

## Routing decision

| Signal strength | Tier | ARR potential | Owner | Channel |
|---|---|---|---|---|
| ExpansionScore > 0.85 + sponsor active | Enterprise | > $50k | AE (CSM hands off) | Outreach + 1:1 CSM intro |
| ExpansionScore 0.7-0.85 | Enterprise | $10-50k | CSM | Mixmax + Klaviyo nurture |
| ExpansionScore 0.7-0.85 | Growth | $5-30k | CSM | Klaviyo flow + Calendly invite |
| ExpansionScore 0.5-0.7 | Growth/Starter | $1-10k | Automated | Customer.io / Klaviyo only |
| ExpansionScore < 0.5 | All | < $5k | None | Skip; revisit Q+1 |

## Common recipes

### Recipe 1: Cohort identification from expansion signals (PostHog)

```sql
-- Customers hitting cross-sell trigger events in last 30d
SELECT
  properties.customer_id,
  properties.tier,
  properties.email,
  count(*) FILTER (WHERE event = 'feature_limit_hit') AS limit_hits,
  count(*) FILTER (WHERE event = 'integration_adopted') AS integrations,
  countDistinct(properties.workspace_id) AS workspaces,
  max(properties.expansion_score) AS expansion_score
FROM events
WHERE timestamp >= now() - INTERVAL 30 DAY
  AND properties.tier IN ('growth', 'enterprise')
GROUP BY properties.customer_id, properties.tier, properties.email
HAVING limit_hits >= 3 OR workspaces >= 2 OR integrations >= 2;
```

Via `posthog-mcp query`. Cross-reference with CSP health score and CRM deal stage. Output -> Recipe 4 / 6 / 8.

### Recipe 2: Klaviyo profile upsert + property enrichment

```bash
# Update Klaviyo profile with expansion signals
curl -sS -X PATCH "https://a.klaviyo.com/api/profiles/$KLAVIYO_PROFILE_ID/" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" \
  -H "revision: 2024-10-15" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "type": "profile",
      "id": "'$KLAVIYO_PROFILE_ID'",
      "attributes": {
        "properties": {
          "tier": "growth",
          "expansion_score": 0.78,
          "current_skus": ["core", "analytics"],
          "target_sku": "automation",
          "feature_limit_hits_30d": 5
        }
      }
    }
  }'
```

Doc: https://developers.klaviyo.com/en/reference/api_overview

### Recipe 3: Klaviyo - add to cross-sell list -> flow triggers

```bash
# Add profile to the cross-sell list; the Klaviyo flow attached to the list auto-fires
curl -sS -X POST "https://a.klaviyo.com/api/lists/$LIST_ID/relationships/profiles/" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" \
  -H "revision: 2024-10-15" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [{"type": "profile", "id": "'$KLAVIYO_PROFILE_ID'"}]
  }'
```

The Klaviyo flow (pre-built in Klaviyo UI by lifecycle team) sends a 4-email nurture:
- D+0: ROI calculator for target SKU
- D+3: Customer story / video walkthrough
- D+7: Live demo invite
- D+14: Limited-time pricing offer

### Recipe 4: Customer.io - in-product trigger campaign

```bash
# Identify customer + fire campaign trigger event
curl -sS -X PUT "https://track.customer.io/api/v1/customers/$CUSTOMER_ID" \
  -u "$CUSTOMERIO_SITE_ID:$CUSTOMERIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "'$EMAIL'",
    "tier": "growth",
    "expansion_score": 0.78,
    "target_sku": "automation",
    "current_skus": ["core", "analytics"]
  }'

# Fire the cross-sell event - matching campaign triggers
curl -sS -X POST "https://track.customer.io/api/v1/customers/$CUSTOMER_ID/events" \
  -u "$CUSTOMERIO_SITE_ID:$CUSTOMERIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "cross_sell_eligible",
    "data": {"target_sku": "automation", "trigger_signal": "limit_hit_3x"}
  }'
```

Doc: https://customer.io/docs/api/track/

### Recipe 5: Iterable list-based campaign (enterprise lifecycle)

```bash
curl -sS -X POST "https://api.iterable.com/api/users/update" -H "Api-Key: $ITERABLE_API_KEY" \
  -d '{"email": "'$EMAIL'", "dataFields": {"tier": "enterprise", "expansion_score": 0.81, "target_sku": "ai-pack"}}'

curl -sS -X POST "https://api.iterable.com/api/workflows/triggerWorkflow" -H "Api-Key: $ITERABLE_API_KEY" \
  -d '{"workflowId": '$WORKFLOW_ID', "email": "'$EMAIL'"}'
```

Doc: https://api.iterable.com/api/docs

### Recipe 6: Outreach sequence enrollment (sales-engagement)

```bash
# 1. Look up or create the prospect in Outreach
curl -sS "https://api.outreach.io/api/v2/prospects?filter[emails]=$EMAIL" \
  -H "Authorization: Bearer $OUTREACH_API_TOKEN" \
  -H "Accept: application/vnd.api+json" | jq '.data[0].id'

# 2. Enroll prospect into the cross-sell sequence
curl -sS -X POST "https://api.outreach.io/api/v2/sequenceStates" \
  -H "Authorization: Bearer $OUTREACH_API_TOKEN" \
  -H "Content-Type: application/vnd.api+json" \
  -d '{
    "data": {
      "type": "sequenceState",
      "relationships": {
        "prospect": {"data": {"type": "prospect", "id": "'$PROSPECT_ID'"}},
        "sequence": {"data": {"type": "sequence", "id": "'$SEQUENCE_ID'"}},
        "mailbox": {"data": {"type": "mailbox", "id": "'$MAILBOX_ID'"}}
      }
    }
  }'
```

Doc: https://developers.outreach.io/api/reference/

### Recipe 7: Salesloft cadence enrollment

```bash
curl -sS -X POST "https://api.salesloft.com/v2/cadence_memberships.json" \
  -H "Authorization: Bearer $SALESLOFT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "person_id": '$PERSON_ID',
    "cadence_id": '$CADENCE_ID',
    "user_id": '$SDR_USER_ID'
  }'
```

Doc: https://developers.salesloft.com/api.html

### Recipe 8: HubSpot sequence enrollment (CRM-native)

```bash
# Note: HubSpot sequences enrollment is per-user-mailbox (not API for some pricing tiers)
# Workflow approach (more API-friendly): enroll in a workflow that emails out

curl -sS -X POST "https://api.hubapi.com/crm/v3/objects/contacts/$CONTACT_ID/associations/workflow/$WORKFLOW_ID/contact_to_workflow" \
  -H "Authorization: Bearer $HUBSPOT_TOKEN" \
  -X PUT
```

Or via Sequences API (where available):

```bash
curl -sS -X POST "https://api.hubapi.com/crm/v3/sequences/$SEQUENCE_ID/enrollments" \
  -H "Authorization: Bearer $HUBSPOT_TOKEN" \
  -d '{"contactId": "'$CONTACT_ID'", "senderId": "'$SENDER_ID'"}'
```

Doc: https://developers.hubspot.com/docs/api/crm/sequences

### Recipe 9: Salesforce sales cadence + task creation

```bash
# Create a follow-up task linked to a Salesforce opportunity (CSM-as-action)
curl -sS -X POST "$SF_INSTANCE_URL/services/data/v60.0/sobjects/Task" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "Subject": "Cross-sell: Automation module to Acme.Corp",
    "WhoId": "'$CONTACT_ID'",
    "WhatId": "'$ACCOUNT_ID'",
    "ActivityDate": "2026-06-25",
    "Priority": "High",
    "Description": "ExpansionScore 0.78; limit_hits=5; target SKU=automation; AE = Mark"
  }'
```

For Salesforce Sales Cadences (HVS):

```bash
curl -sS -X POST "$SF_INSTANCE_URL/services/data/v60.0/sobjects/CadenceAssignment" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN" \
  -d '{
    "TargetId": "'$LEAD_OR_CONTACT_ID'",
    "CadenceId": "'$CADENCE_ID'"
  }'
```

Doc: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/

### Recipe 10: Mixmax CSM-led personalized cadence

```bash
curl -sS -X POST "https://api.mixmax.com/v1/sequences/$SEQUENCE_ID/enrollments" \
  -H "X-API-Token: $MIXMAX_API_TOKEN" \
  -d '{
    "recipient": {"email": "'$EMAIL'", "firstName": "'$FIRST_NAME'"},
    "variables": {
      "current_sku": "core",
      "target_sku": "automation",
      "savings_estimate": "$3,200/yr",
      "calendly_url": "'$CSM_CALENDLY'"
    }
  }'
```

Doc: https://help.mixmax.com/hc/en-us

### Recipe 11: Draft personalized cross-sell email (Claude)

```python
prompt = f"""
Draft a 6-sentence personalized cross-sell email.

Customer: {customer.name}
Tier: {customer.tier}
Current SKUs: {", ".join(customer.current_skus)}
Target SKU: {target_sku.name} - {target_sku.value_prop}
Concrete signal: {signal_text}  # e.g., "Your team hit the limit on automation runs 5 times last month"
CSM: {csm.name}

Asks (one only):
- 20-min call to walk through {target_sku.name}
- Calendly: {csm.calendly_url}

Rules:
- Lead with the concrete signal (not a pitch).
- Reference one specific use case detail.
- No "Hope you're doing well." No "Just touching base." No "Excited to share."
- Don't say "for a limited time" unless there's a real pricing window.
"""
body = claude.generate(prompt)
gmail.send_email(to=[customer.primary_email], subject=f"{customer.name} - 20 min on {target_sku.name}", body=body)
```

### Recipe 12: AE handoff for high-value uplift

```python
# When uplift potential > $50k, hand off to sales-agent
from sales_agent import handoff_expansion

handoff_expansion(
    customer_id=customer.id,
    ae_user_id=customer.ae_user_id,
    expansion_score=0.84,
    arr_potential=78000,
    target_sku="enterprise_ai_pack",
    signal_summary="Multi-workspace usage doubled in 30d; feature-limit hits 8x in last week",
    csm_context_note="Sponsor is VP Eng; champion has used product 18 months; budget cycle Q3.",
    next_steps="Book intro call this week; CSM joins to vouch.",
)
```

Sales-agent picks up via Outreach sequence (Recipe 6) or direct Salesforce task (Recipe 9).

### Recipe 13: Sequence conversion measurement

```sql
WITH enrolled AS (
  SELECT customer_id, sequence_id, min(enrolled_at) AS enrolled_at
  FROM sequence_enrollments
  WHERE enrolled_at >= now() - INTERVAL '90 days'
  GROUP BY customer_id, sequence_id
),
converted AS (
  SELECT
    e.customer_id,
    e.sequence_id,
    e.enrolled_at,
    bool_or(d.stage IN ('closed_won') AND d.closed_at > e.enrolled_at) AS converted,
    sum(d.amount) FILTER (WHERE d.stage = 'closed_won' AND d.closed_at > e.enrolled_at) AS arr_added
  FROM enrolled e
  LEFT JOIN deals d ON d.customer_id = e.customer_id AND d.product_sku = e.target_sku
  GROUP BY e.customer_id, e.sequence_id, e.enrolled_at
)
SELECT
  sequence_id,
  count(*) AS enrolled,
  count(*) FILTER (WHERE converted) AS converted,
  100.0 * count(*) FILTER (WHERE converted) / count(*) AS conversion_pct,
  sum(arr_added) FILTER (WHERE converted) AS total_arr_added,
  sum(arr_added) FILTER (WHERE converted) / nullif(count(*) FILTER (WHERE converted), 0) AS avg_deal
FROM converted
GROUP BY sequence_id
ORDER BY conversion_pct DESC;
```

Output -> `xlsx` skill for monthly RevOps review.

### Recipe 14: Suppression - exclude unhealthy / churn-risk customers

```python
# Don't sell more to a customer who's at-risk
suppressed = postgres.query("""
SELECT customer_id FROM customers
WHERE health_score < 0.5
   OR risk_flag = 'Red'
   OR marketing_opt_out = true
   OR last_objection_date >= now() - INTERVAL '60 days'
""")

eligible_for_sequence = [c for c in cohort if c.id not in suppressed]
```

### Recipe 15: Stop sequence on reply or conversion

```bash
# Klaviyo: remove from list
curl -sS -X DELETE "https://a.klaviyo.com/api/lists/$LIST_ID/relationships/profiles/" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data": [{"type": "profile", "id": "'$KLAVIYO_PROFILE_ID'"}]}'

# Customer.io: fire suppression event
curl -sS -X POST "https://track.customer.io/api/v1/customers/$CUSTOMER_ID/events" \
  -u "$CUSTOMERIO_SITE_ID:$CUSTOMERIO_API_KEY" \
  -d '{"name": "cross_sell_exit", "data": {"reason": "replied"}}'

# Outreach: finish sequence early
curl -sS -X PATCH "https://api.outreach.io/api/v2/sequenceStates/$SEQUENCE_STATE_ID" \
  -H "Authorization: Bearer $OUTREACH_API_TOKEN" \
  -d '{"data": {"type": "sequenceState", "id": "'$SEQUENCE_STATE_ID'", "attributes": {"state": "finished"}}}'
```

## Examples

### Example 1: Growth-tier customer hits limit 5x - CSM-led Klaviyo sequence

**Goal:** Acme.Inc hit `feature_limit_hit` 5 times last week; surface automation SKU; convert to expansion.

**Steps:**
1. Recipe 1 nightly query surfaces Acme; ExpansionScore = 0.74; tier = Growth.
2. Routing table: CSM-led; channel = Klaviyo flow + Calendly invite.
3. Recipe 2 enriches Acme's Klaviyo profile.
4. Recipe 3 adds to Cross-Sell list -> flow starts.
5. D+7: no reply; Recipe 11 drafts personalized CSM 1:1.
6. D+10: reply -> CSM book call.
7. D+30: closed-won; +$8k ARR. Recipe 13 records.

**Result:** Mixed-channel (automated nurture + CSM 1:1) converted; $8k uplift.

### Example 2: Enterprise expansion with AE handoff

**Goal:** Globex.Corp shows ExpansionScore 0.87; potential $78k AI-pack upsell.

**Steps:**
1. Recipe 1 surfaces Globex; tier Enterprise; ExpansionScore 0.87.
2. Routing table: AE-led.
3. Recipe 12 handoff to sales-agent with full context.
4. Recipe 6 sales-agent enrolls Globex contacts in Outreach sequence (10-touch over 21 days).
5. Recipe 9 Salesforce task on AE: "Intro call by Friday."
6. CSM joins the first call; provides product context + customer history.
7. AE closes; +$78k ARR over 12-month commit.

**Result:** Clean handoff; CSM credit + AE close; large uplift.

### Example 3: Suppression saves a relationship

**Goal:** Customer in Churn Save plan + cross-sell signal hit; don't sell more.

**Steps:**
1. Recipe 1 surfaces customer.
2. Recipe 14 suppression check: health_score = 0.41 (Red).
3. Skip the cross-sell sequence.
4. Cross-feed back to `churn-save-motion-intervention` - this is a save play, not sell play.

**Result:** Avoided tone-deaf sell motion; CSM keeps trust.

## Edge cases / gotchas

- **Sell-then-save anti-pattern** — selling more to a Red-risk customer is tone-deaf and worsens churn. Recipe 14 suppression is mandatory.
- **Multi-channel collision** — Klaviyo + Outreach + Mixmax all firing = 6 emails in a week. Set primary channel per customer; suppress the rest. RevOps owns the rule.
- **Sequence overlap with renewal cadence** — `renewal-management-90-day-prep` already running for the same customer. Combine into a single thread; don't run parallel cadences.
- **AE / CSM ownership conflict** — both want credit. Pre-agreed comp split via RevOps; document in the Salesforce opportunity ownership team.
- **HubSpot Sequences API gating** — HubSpot Sequences API requires Sales Hub Enterprise. Use Workflows API (Recipe 8 alt) on lower tiers.
- **Outreach mailbox attribution** — sequence emails are sent from the SDR/CSM mailbox; throttle per-mailbox limits (300/day soft, 500/day hard for most providers).
- **Klaviyo flow filter staleness** — flow checks `target_sku` at trigger time; if you change `target_sku` mid-flow, emails reference the old SKU. Re-add to the list.
- **Localization** — sequence is English-only; non-English customers get awkward copy. Maintain per-locale sequences; route via `deepl-mcp` for translation if no localized sequence exists.
- **Sales-cycle length mismatch** — Enterprise cross-sell takes 60-90 days; Klaviyo flow ends at D+14. Use Outreach (longer) for Enterprise; Klaviyo for Growth.
- **Conversion attribution** — closed-won deal attributed to last-touch sequence by default; multi-touch attribution needs UTM + RevOps attribution model.
- **Sender reputation** — too many cold cross-sell emails -> spam folder. Warm up the sending mailbox; cap per-day send.
- **CRM contact role missing** — sequence emails the wrong person (procurement, not champion). Audit contact roles before enrollment.
- **Marketing-opt-out vs lifecycle-opt-out** — customers opt out of marketing but stay on lifecycle / transactional. Cross-sell sequences are lifecycle; check that legal interpretation matches.
- **Customer.io campaign trigger event drift** — event name changed in product code; campaign no longer fires. Smoke-test trigger events monthly.
- **Iterable workflow webhook reliability** — webhooks can drop; verify enrollment via Iterable user lookup, don't trust the POST response alone.
- **Salesforce cadence API rate limits** — Salesforce Sales Cadence (HVS) has lower limits than core REST; batch enrollments.
- **Multi-product bundle pricing** — sequence assumes single-SKU upsell; bundling needs CPQ (Salesforce CPQ / Zuora) for accurate quote; redirect Mixmax/Outreach to "AE will follow up with quote" and let AE drive.
- **No reply but converted via direct sales** — customer ignored the sequence but talked to AE directly. Stop the sequence (Recipe 15) once `stage=closed_won` to avoid follow-up after close.
- **Sequence email caps duplicate sends** — same customer in 2 lists fires 2 emails. Maintain a master suppression check before enrollment.

## Sources

- [Klaviyo API overview](https://developers.klaviyo.com/en/reference/api_overview)
- [Klaviyo Lists + Profiles](https://developers.klaviyo.com/en/reference/get_lists)
- [Customer.io Track API](https://customer.io/docs/api/track/)
- [Customer.io Campaign triggers](https://customer.io/docs/journeys/triggered-broadcasts/)
- [Iterable API docs](https://api.iterable.com/api/docs)
- [Outreach API reference](https://developers.outreach.io/api/reference/)
- [Outreach Sequence States](https://developers.outreach.io/api/reference/tag/sequenceState/)
- [Salesloft API](https://developers.salesloft.com/api.html)
- [Salesloft cadence memberships](https://developers.salesloft.com/api.html#!/Cadence_Memberships/index)
- [HubSpot Sequences API](https://developers.hubspot.com/docs/api/crm/sequences)
- [HubSpot Workflows API](https://developers.hubspot.com/docs/api/automation/workflows-v3)
- [Salesforce REST API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/)
- [Salesforce Sales Cadence (HVS)](https://help.salesforce.com/s/articleView?id=sf.hvs_cadence.htm)
- [Mixmax sequence enrollment](https://help.mixmax.com/hc/en-us)
- [PostHog cohorts](https://posthog.com/docs/product-analytics/cohorts)
