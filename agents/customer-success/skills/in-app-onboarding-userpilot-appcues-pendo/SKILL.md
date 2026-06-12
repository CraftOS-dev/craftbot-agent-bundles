<!--
Source: https://developers.pendo.io/ + https://docs.userpilot.com/ + https://help.appcues.com/en/articles/123-appcues-rest-api + https://help.chameleon.io/
-->
# In-App Onboarding — Userpilot / Appcues / Pendo / Chameleon / Whatfix — SKILL

Design + ship in-product onboarding flows (modals, tooltips, checklists, walkthroughs) across the major platforms (Pendo, Userpilot, Appcues, Chameleon, Whatfix, ProductFruits). Author flow schema; CRUD via REST API; A/B test variants; track exit-event conversion. Free fallback: ProductFruits free tier or custom-built nudges in product code.

## When to use

- **New onboarding flow needed** — TTFV slipping; build Day 0-7 in-product card series.
- **Feature launch nudge** — new SKU/feature, drive adoption in first 30 days.
- **Re-engagement** — dormant user returns; in-product welcome-back tour.
- **A/B test flow variant** — copy A vs copy B; checklist 3-step vs 5-step.
- **Pendo / Userpilot / Appcues admin** — CRUD flows programmatically (not via UI clicks).
- **Free fallback build** — ProductFruits free tier or in-product custom code.

This skill **complements** `customer-onboarding-day-0-90` (which enrolls customers into flows; this skill builds the flows themselves) and `feature-adoption-interventions` (cohort -> nudge -> follow-up).

Trigger phrases: "Pendo flow", "Userpilot tour", "Appcues guide", "in-app nudge", "tooltip", "checklist", "in-product onboarding", "Chameleon".

## Setup

```bash
# Pendo (incumbent)
export PENDO_API_KEY="<integration-key>"

# Userpilot (modern alt)
export USERPILOT_API_KEY="<key>"

# Appcues (incumbent)
export APPCUES_API_KEY="<key>"
export APPCUES_ACCOUNT_ID="<id>"

# Chameleon
export CHAMELEON_API_KEY="<key>"

# Whatfix (enterprise)
export WHATFIX_API_KEY="<key>"

# ProductFruits (freemium)
export PRODUCTFRUITS_API_KEY="<key>"
```

Workspace prerequisites:
- Standardized flow schema (see "Flow design schema" below).
- Audience segmentation rules wired in your product (tier, days_since_signup, role).
- Exit-event taxonomy stable enough to measure flow conversion (`first_aha_event`, `feature_first_used`).
- pptx/figma source for flow visual spec.

## Flow design schema (vendor-neutral)

```json
{
  "flow_id": "onboarding-day-7-aha",
  "trigger": {
    "type": "event",
    "event_name": "workspace_setup_complete"
  },
  "audience": {
    "filter": "tier IN ('starter', 'growth') AND days_since_signup BETWEEN 5 AND 10"
  },
  "steps": [
    {"type": "modal", "title": "Welcome - let's get you to your first aha", "body": "..."},
    {"type": "tooltip", "target": "#create-button", "body": "Create your first [thing]"},
    {"type": "checklist", "items": ["Create [thing]", "Invite teammate", "Run first [workflow]"]}
  ],
  "exit": {
    "type": "event",
    "event_name": "first_aha_event"
  },
  "metric": "first_aha_rate_within_7d"
}
```

## Common recipes

### Recipe 1: Create Pendo guide

```bash
curl -sS -X POST "https://app.engage.pendo.io/api/v1/guide" \
  -H "X-Pendo-Integration-Key: $PENDO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Day 7 First Aha",
    "appId": "'$PENDO_APP_ID'",
    "audienceUiHint": "tier IN ('starter', 'growth')",
    "steps": [
      {"type": "lightbox", "name": "Welcome", "title": "Lets get you to your first aha"},
      {"type": "tooltip", "name": "Create CTA", "elementPathRule": "#create-button"},
      {"type": "checklist", "name": "3-step checklist"}
    ],
    "state": "draft"
  }'
```

Doc: https://developers.pendo.io/

### Recipe 2: Create Pendo segment + activate

```bash
# Define segment of eligible audience
curl -sS -X POST "https://app.engage.pendo.io/api/v1/segments" \
  -H "X-Pendo-Integration-Key: $PENDO_API_KEY" \
  -d '{
    "name": "Onboarding D5-D10",
    "filter": {
      "type": "and",
      "filters": [
        {"type": "operator", "field": "metadata.account.tier", "operator": "IN", "value": ["starter", "growth"]},
        {"type": "operator", "field": "metadata.visitor.days_since_signup", "operator": "between", "value": [5, 10]}
      ]
    }
  }'

# Attach segment to guide
curl -sS -X PATCH "https://app.engage.pendo.io/api/v1/guide/$GUIDE_ID" \
  -H "X-Pendo-Integration-Key: $PENDO_API_KEY" \
  -d '{"segmentId": "'$SEGMENT_ID'", "state": "published"}'
```

### Recipe 3: Create Userpilot flow

```bash
curl -sS -X POST "https://api.userpilot.io/v1/flows" \
  -H "X-API-KEY: $USERPILOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Day 7 First Aha",
    "trigger": {"event": "workspace_setup_complete"},
    "audience": {"company_attribute_filter": {"tier": ["starter", "growth"]}},
    "steps": [
      {"type": "modal", "content": "..."},
      {"type": "tooltip", "selector": "#create-button"},
      {"type": "checklist", "items": [...]}
    ]
  }'
```

Doc: https://docs.userpilot.com/

### Recipe 4: Userpilot audience enrollment

```bash
curl -sS -X POST "https://api.userpilot.io/v1/companies/$COMPANY_ID/groups" \
  -H "X-API-KEY: $USERPILOT_API_KEY" \
  -d '{"group_id": "onboarding_d5_d10"}'
```

### Recipe 5: Create Appcues flow

```bash
curl -sS -X POST "https://api.appcues.com/v2/accounts/$APPCUES_ACCOUNT_ID/flows" \
  -H "Authorization: Bearer $APPCUES_API_KEY" \
  -d '{
    "name": "Day 7 First Aha",
    "type": "modal_flow",
    "steps": [...]
  }'
```

Doc: https://help.appcues.com/en/articles/123-appcues-rest-api

### Recipe 6: Appcues audience targeting

```bash
curl -sS -X PATCH "https://api.appcues.com/v2/accounts/$APPCUES_ACCOUNT_ID/flows/$FLOW_ID" \
  -H "Authorization: Bearer $APPCUES_API_KEY" \
  -d '{
    "audience": {
      "rules": [
        {"property": "tier", "comparator": "EQUALS", "value": "growth"},
        {"property": "days_since_signup", "comparator": "BETWEEN", "value": [5, 10]}
      ]
    }
  }'
```

### Recipe 7: Chameleon tour CRUD

```bash
curl -sS -X POST "https://api.trychameleon.com/v3/tours" \
  -H "X-Account-Secret: $CHAMELEON_API_KEY" \
  -d '{
    "name": "Day 7 First Aha",
    "steps": [...],
    "audience_filter": "..."
  }'
```

Chameleon is SDK-first; REST is best for read/admin. Most setup happens via web UI; REST for cohort enrollment.

### Recipe 8: ProductFruits flow (free tier fallback)

```bash
curl -sS -X POST "https://api.productfruits.com/v2/tours" \
  -H "Authorization: Bearer $PRODUCTFRUITS_API_KEY" \
  -d '{...}'
```

### Recipe 9: A/B test pattern

Build flow variant A + variant B (different copy, order, or exit event). Audience split 50/50 via either:
- Native A/B test feature (Userpilot supports natively; Pendo does too).
- Custom: write variant-A flow + variant-B flow + segment audience by random hash of customer_id (even/odd) -> assign each segment to a different flow.

```python
# Random hash assignment
import hashlib
variant = "a" if int(hashlib.md5(customer_id.encode()).hexdigest(), 16) % 2 == 0 else "b"
```

Run for 14 days. Compare exit-event rate per variant:

```sql
SELECT
  variant,
  count(*) AS exposed,
  count(*) FILTER (WHERE exit_event_fired) AS converted,
  100.0 * count(*) FILTER (WHERE exit_event_fired) / count(*)::numeric AS conversion_pct
FROM flow_exposures
WHERE flow_id IN ('flow-a', 'flow-b')
  AND exposed_at >= now() - INTERVAL '14 days'
GROUP BY variant;
```

Promote winner; archive loser.

### Recipe 10: Pendo guide metrics

```bash
curl -sS "https://app.engage.pendo.io/api/v1/guide/$GUIDE_ID/metrics" \
  -H "X-Pendo-Integration-Key: $PENDO_API_KEY" | jq '.'
```

Returns views, completions, dismissals per step. Use to find drop-off points.

### Recipe 11: Userpilot flow analytics

```bash
curl -sS "https://api.userpilot.io/v1/flows/$FLOW_ID/analytics?period=14d" \
  -H "X-API-KEY: $USERPILOT_API_KEY"
```

### Recipe 12: Audience cohort sync from PostHog

```sql
-- HogQL: customers eligible for Day 7 flow
SELECT
  properties.customer_id,
  properties.user_id,
  min(timestamp) AS signup_at
FROM events
WHERE event = 'signup'
  AND timestamp >= now() - INTERVAL 14 DAY
  AND properties.tier IN ('starter', 'growth')
GROUP BY properties.customer_id, properties.user_id
HAVING dateDiff('day', min(timestamp), now()) BETWEEN 5 AND 10;
```

Via `posthog-mcp query`. Output -> Recipe 2 / 4 / 6 to enroll into flow audience.

### Recipe 13: Flow exit-event conversion measurement

```sql
-- Per-customer: did they see the flow AND fire exit event within window?
SELECT
  fe.customer_id,
  fe.flow_id,
  fe.exposed_at,
  MIN(ev.timestamp) FILTER (WHERE ev.event = exit_event_name AND ev.timestamp > fe.exposed_at) AS exit_at,
  CASE
    WHEN MIN(ev.timestamp) FILTER (WHERE ev.event = exit_event_name AND ev.timestamp > fe.exposed_at)
         <= fe.exposed_at + INTERVAL '7 days' THEN TRUE
    ELSE FALSE
  END AS converted_within_7d
FROM flow_exposures fe
LEFT JOIN events ev ON ev.customer_id = fe.customer_id
GROUP BY fe.customer_id, fe.flow_id, fe.exposed_at;
```

## Examples

### Example 1: New Day 7 first-aha flow (from spec to live in 3 days)

**Goal:** TTFV slipping; ship a 3-step in-product nudge flow for Starter/Growth tier.

**Steps:**
1. Day 1: Spec via pptx + Figma; define exit event = `first_aha_event`.
2. Day 1: Recipe 2 segment created; Recipe 1 guide draft via Pendo.
3. Day 2: QA on staging; minor copy tweaks; activate.
4. Day 3-17: Recipe 10 metrics review; Recipe 13 conversion measurement.

**Result:** Flow live; first cohort measured at day 14.

### Example 2: A/B test - 3-step vs 5-step checklist

**Goal:** Test if a shorter checklist improves completion.

**Steps:**
1. Build variant A (3 steps) + variant B (5 steps).
2. Recipe 9 audience split.
3. Run 14 days.
4. Variant A conversion = 38%; Variant B = 31%. Promote A; archive B.
5. Document learning in Notion CS playbook.

**Result:** Iterative improvement; ~7pp lift baked in.

## Edge cases / gotchas

- **Selector drift** — `#create-button` element renames in product code -> tooltip breaks silently. Use Pendo tag-based targeting (not CSS) where possible.
- **Audience filter on stale traits** — `tier` synced nightly; signup-day-1 customer has `tier=NULL`. Fallback rule: NULL -> include or exclude explicitly.
- **Trigger event not firing** — if `workspace_setup_complete` is mis-instrumented, no one sees the flow. Verify event in PostHog before launch.
- **Multi-language customers** — flow copy in English only; Spanish customers see English popups. Use DeepL via deepl-mcp + per-locale variants.
- **Flow stacking** — multiple flows fire on same trigger -> annoying. Vendors usually have priority; set explicitly.
- **Dismissal rate too high** — users hammering X on first popup. A/B test smaller modal or move to tooltip; don't blast.
- **Mobile vs web** — Pendo/Userpilot have separate mobile SDKs; flow built for web doesn't auto-port. Plan per-surface.
- **GDPR / consent for tracking** — Pendo events require consent in EU. Verify consent flow before flow ships.
- **A/B test sample size** — flows for low-volume cohorts (< 200 exposures) = noisy. Need 500+ for meaningful conversion delta.
- **Vendor lock-in** — switching Pendo -> Userpilot = re-build flows. Keep flow schema in a vendor-neutral format in Notion for portability.
- **ProductFruits free tier hard caps** — < 1000 MAU sometimes; check before relying on free for production.
- **Flow self-targeting on internal users** — your team sees flows in production. Exclude team domains from audience.

## Sources

- [Pendo Engage API docs](https://developers.pendo.io/)
- [Pendo guide creation](https://help.pendo.io/resources/support-library/in-app-guides/index)
- [Userpilot REST API docs](https://docs.userpilot.com/article/195-userpilot-rest-api)
- [Userpilot flow management](https://docs.userpilot.com/)
- [Appcues REST API](https://help.appcues.com/en/articles/123-appcues-rest-api)
- [Chameleon API docs](https://help.chameleon.io/en/articles/3402836-chameleon-api)
- [Whatfix API](https://docs.whatfix.com/)
- [ProductFruits API](https://help.productfruits.com/en/article/api-reference)
- [PostHog HogQL Query API](https://posthog.com/docs/api/queries)
- [A/B testing pattern (Userpilot blog)](https://userpilot.com/blog/ab-testing-onboarding/)
