<!--
Source: https://developers.pendo.io/ + https://docs.userpilot.com/ + https://help.appcues.com/en/articles/123-appcues-rest-api + https://posthog.com/docs/product-analytics/cohorts + https://help.mixmax.com/hc/en-us + https://developers.klaviyo.com/
-->
# Feature Adoption Interventions — Pendo / Userpilot / Appcues + Cohorts + Follow-up — SKILL

Drive adoption of a specific feature when a cohort of eligible customers hasn't used it. Define the cohort (PostHog HogQL), enroll them into a Pendo / Userpilot / Appcues in-product nudge flow, follow up via email if no adoption in 7 days, and measure conversion against a control group. Designed for individual feature interventions, not full onboarding flows (that's `in-app-onboarding-userpilot-appcues-pendo`).

## When to use

- **Feature underused in eligible cohort** — Feature X built for Growth+ tier; only 18% adoption. Push the nudge.
- **New feature launched** — first 30 days, drive 50% adoption in first-eligible cohort.
- **Plan-upgrade unlocks** — customer upgraded to Enterprise but hasn't tried Enterprise-only feature; nudge.
- **Renewal-blocker feature** — Feature Y is a key value driver for renewal; if not used by D60, intervention fires.
- **Re-engagement of dormant power feature** — customer used Z weekly then stopped; nudge back.
- **Cross-feature dependency** — A unlocks B; customer using A, not B; introduce B in context.

This skill **complements** `in-app-onboarding-userpilot-appcues-pendo` (which builds the flow infrastructure; this skill targets the cohort and orchestrates follow-up) and **reads from** `adoption-metric-feature-usage` (cohort definitions). It **feeds** `voice-of-customer-reporting` (low-adoption signal -> product input).

Trigger phrases: "feature adoption", "Pendo nudge", "Userpilot nudge", "Appcues guide", "feature intervention", "underused feature", "drive adoption", "in-product nudge", "feature engagement", "cohort nudge".

## Setup

```bash
# Pendo (incumbent in-app onboarding)
export PENDO_API_KEY="<integration-key>"
export PENDO_APP_ID="<app-id>"

# Userpilot (modern alt)
export USERPILOT_API_KEY="<key>"

# Appcues (incumbent)
export APPCUES_API_KEY="<key>"
export APPCUES_ACCOUNT_ID="<account-id>"

# PostHog (cohort source) - via posthog-mcp
# Mixpanel (alt cohort) - via mixpanel-mcp
# Amplitude (alt cohort) - via amplitude-mcp

# Klaviyo (email follow-up if no adoption in 7d)
export KLAVIYO_API_KEY="<key>"

# Mixmax / Customer.io (alt email cadence)
export MIXMAX_API_TOKEN="<token>"
export CUSTOMERIO_API_KEY="<key>"

# Gmail (CSM personal follow-up) - via gmail-mcp
```

Workspace prerequisites:
- Feature instrumentation: `feature_X_used` event fires in PostHog reliably.
- Cohort definition rules in Notion CS playbook (who is "eligible," what counts as adoption).
- A/B test infrastructure: ability to hold out 10-20% as control.
- 14-day measurement window before declaring win/loss.
- Approval gate: VP CS approves any intervention pushing > 500 customers (avoid in-app fatigue).

## Intervention design schema

```json
{
  "intervention_id": "feature-x-adoption-q3-2026",
  "feature_event": "feature_x_used",
  "cohort": {
    "definition": "tier IN ('growth', 'enterprise') AND days_since_signup > 30 AND feature_x_used = false",
    "source": "posthog",
    "size_estimate": 412
  },
  "hold_out": 0.15,
  "nudge_channels": [
    {"channel": "pendo", "flow_id": "feature-x-tooltip", "start_day": 0},
    {"channel": "klaviyo", "flow_id": "feature-x-email-d7", "start_day": 7, "condition": "still_not_adopted"},
    {"channel": "csm_email", "start_day": 14, "condition": "still_not_adopted AND tier='enterprise'"}
  ],
  "success_event": "feature_x_used",
  "measurement_window_days": 14,
  "primary_metric": "feature_x_adoption_rate"
}
```

## Common recipes

### Recipe 1: Define cohort via PostHog HogQL

```sql
-- Eligible customers who haven't used feature_x
SELECT
  properties.customer_id,
  properties.user_id,
  properties.email,
  properties.tier,
  min(timestamp) AS signup_at
FROM events
WHERE properties.tier IN ('growth', 'enterprise')
  AND timestamp >= now() - INTERVAL 365 DAY
GROUP BY properties.customer_id, properties.user_id, properties.email, properties.tier
HAVING dateDiff('day', min(timestamp), now()) > 30
   AND not has((
     SELECT groupArray(properties.customer_id)
     FROM events
     WHERE event = 'feature_x_used'
   ), properties.customer_id);
```

Via `posthog-mcp query`. Output: cohort list -> Recipe 3 / 4 / 5.

Doc: https://posthog.com/docs/product-analytics/cohorts

### Recipe 2: Hold out 15% as control (random hash)

```python
import hashlib

def is_treatment(customer_id, hold_out=0.15):
    h = int(hashlib.md5(customer_id.encode()).hexdigest(), 16)
    return (h % 100) >= int(hold_out * 100)

treatment_cohort = [c for c in eligible if is_treatment(c.customer_id)]
control_cohort = [c for c in eligible if not is_treatment(c.customer_id)]
```

Treatment gets the nudge; control gets nothing. Compare conversion at D+14.

### Recipe 3: Push cohort into Pendo segment + activate guide

```bash
# Create a Pendo segment for the treatment cohort
curl -sS -X POST "https://app.engage.pendo.io/api/v1/segments" \
  -H "X-Pendo-Integration-Key: $PENDO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Feature X Adoption - Treatment Q3 2026",
    "filter": {
      "type": "and",
      "filters": [
        {"type": "operator", "field": "metadata.account.tier", "operator": "IN", "value": ["growth", "enterprise"]},
        {"type": "operator", "field": "metadata.visitor.days_since_signup", "operator": ">", "value": 30},
        {"type": "operator", "field": "metadata.visitor.feature_x_used", "operator": "=", "value": false}
      ]
    }
  }'

# Attach the existing guide to the segment + publish
curl -sS -X PATCH "https://app.engage.pendo.io/api/v1/guide/$GUIDE_ID" \
  -H "X-Pendo-Integration-Key: $PENDO_API_KEY" \
  -d '{"segmentId": "'$SEGMENT_ID'", "state": "published"}'
```

Doc: https://developers.pendo.io/

### Recipe 4: Userpilot cohort enrollment

```bash
# Add cohort to a Userpilot audience
for customer_id in $(cat treatment_cohort.txt); do
  curl -sS -X POST "https://api.userpilot.io/v1/companies/$customer_id/groups" \
    -H "X-API-KEY: $USERPILOT_API_KEY" \
    -d '{"group_id": "feature_x_adoption_treatment"}'
done

# Verify flow audience targeting
curl -sS "https://api.userpilot.io/v1/flows/$FLOW_ID" \
  -H "X-API-KEY: $USERPILOT_API_KEY" | jq '.audience'
```

Doc: https://docs.userpilot.com/

### Recipe 5: Appcues audience targeting

```bash
# Update flow audience rules
curl -sS -X PATCH "https://api.appcues.com/v2/accounts/$APPCUES_ACCOUNT_ID/flows/$FLOW_ID" \
  -H "Authorization: Bearer $APPCUES_API_KEY" \
  -d '{
    "audience": {
      "rules": [
        {"property": "tier", "comparator": "IN", "value": ["growth", "enterprise"]},
        {"property": "days_since_signup", "comparator": ">", "value": 30},
        {"property": "feature_x_used", "comparator": "EQUALS", "value": false}
      ]
    },
    "published": true
  }'
```

Doc: https://help.appcues.com/en/articles/123-appcues-rest-api

### Recipe 6: Pendo nudge content (modal + tooltip 2-step)

```bash
# A focused 2-step guide: intro modal + spotlight tooltip on the feature button
curl -sS -X POST "https://app.engage.pendo.io/api/v1/guide" \
  -H "X-Pendo-Integration-Key: $PENDO_API_KEY" \
  -d '{
    "name": "Feature X Adoption Nudge",
    "appId": "'$PENDO_APP_ID'",
    "steps": [
      {
        "type": "lightbox",
        "name": "Intro",
        "title": "Try Feature X",
        "body": "Save ~30 min/week by automating your [thing] with Feature X. Want to try it now?",
        "primaryButton": {"label": "Show me", "action": "advance"},
        "secondaryButton": {"label": "Not now", "action": "dismiss"}
      },
      {
        "type": "tooltip",
        "name": "Feature X CTA",
        "elementPathRule": "[data-feature=\"x\"]",
        "title": "Click here to start",
        "body": "Takes 30 seconds."
      }
    ],
    "state": "draft"
  }'
```

### Recipe 7: D+7 email follow-up via Klaviyo flow

```bash
# Fire Klaviyo event - triggers the D+7 email flow
curl -sS -X POST "https://a.klaviyo.com/api/events/" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" \
  -H "revision: 2024-10-15" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "type": "event",
      "attributes": {
        "properties": {
          "intervention_id": "feature-x-adoption-q3-2026",
          "feature_name": "Feature X",
          "csm": "'$CSM_NAME'",
          "deep_link": "'$FEATURE_DEEP_LINK'"
        },
        "metric": {"data": {"type": "metric", "attributes": {"name": "Feature Adoption Nudge D7"}}},
        "profile": {"data": {"type": "profile", "attributes": {"email": "'$RECIPIENT_EMAIL'"}}}
      }
    }
  }'
```

Klaviyo flow filter: only send if `feature_x_used` event has NOT fired since the nudge started.

### Recipe 8: D+14 CSM-led email (enterprise tier only)

```python
# After D+14 with no adoption, for enterprise tier, CSM-led personal email
cohort_d14 = posthog.query("""
SELECT properties.customer_id, properties.email, properties.tier
FROM events
WHERE properties.intervention_id = 'feature-x-adoption-q3-2026'
  AND properties.feature_x_used = false
  AND properties.tier = 'enterprise'
  AND properties.nudge_started_at <= now() - INTERVAL 14 DAY
""")

for customer in cohort_d14:
    prompt = f"""
Draft a 5-sentence CSM follow-up email about Feature X.

Customer: {customer.name}
Tier: Enterprise
What you know: They were enrolled in the Feature X nudge 14 days ago; haven't tried it.
Their use case from success plan: {customer.use_case}

Rules:
- Specific: tie Feature X to their stated outcome.
- Offer a 15-min walkthrough call.
- Calendly link: {csm.calendly_url}
- Don't apologize for nudging. Don't say "circling back."
"""
    body = claude.generate(prompt)
    gmail.send_email(to=[customer.email], subject=f"{customer.name} - 15 min on Feature X?", body=body)
```

### Recipe 9: Mixmax CSM cadence as alt to Klaviyo

```bash
# Enroll into a Mixmax sequence for personalized cadence
curl -sS -X POST "https://api.mixmax.com/v1/sequences/$SEQUENCE_ID/enrollments" \
  -H "X-API-Token: $MIXMAX_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": {"email": "'$RECIPIENT_EMAIL'", "firstName": "'$FIRST_NAME'"},
    "variables": {"feature_name": "Feature X", "deep_link": "'$FEATURE_DEEP_LINK'"}
  }'
```

Doc: https://help.mixmax.com/hc/en-us

### Recipe 10: Measure intervention conversion (treatment vs control)

```sql
WITH cohort AS (
  SELECT
    properties.customer_id,
    properties.is_treatment,
    min(timestamp) FILTER (WHERE event = 'intervention_enrolled') AS enrolled_at,
    bool_or(event = 'feature_x_used' AND timestamp > min(timestamp) FILTER (WHERE event = 'intervention_enrolled')) AS adopted
  FROM events
  WHERE properties.intervention_id = 'feature-x-adoption-q3-2026'
  GROUP BY properties.customer_id, properties.is_treatment
),
results AS (
  SELECT
    is_treatment,
    count(*) AS cohort_size,
    sum(case when adopted then 1 else 0 end) AS adopted_count,
    100.0 * sum(case when adopted then 1 else 0 end) / count(*)::numeric AS adoption_pct
  FROM cohort
  WHERE enrolled_at <= now() - INTERVAL '14 days'
  GROUP BY is_treatment
)
SELECT * FROM results;
```

Compare treatment vs control. Significance test: chi-squared or 2-proportion z-test. Typical SaaS sample needs > 200 per arm for reliable signal.

### Recipe 11: Drop-off analysis (where in the funnel customers fall out)

```sql
-- For treatment cohort: did they see the nudge? click it? open the feature? complete the feature?
SELECT
  count(*) AS enrolled,
  count(*) FILTER (WHERE saw_nudge) AS saw_nudge,
  count(*) FILTER (WHERE clicked_nudge_cta) AS clicked,
  count(*) FILTER (WHERE opened_feature) AS opened,
  count(*) FILTER (WHERE used_feature) AS adopted,
  100.0 * count(*) FILTER (WHERE saw_nudge) / count(*) AS saw_rate,
  100.0 * count(*) FILTER (WHERE clicked_nudge_cta) / nullif(count(*) FILTER (WHERE saw_nudge), 0) AS click_through_rate,
  100.0 * count(*) FILTER (WHERE used_feature) / nullif(count(*) FILTER (WHERE opened_feature), 0) AS open_to_use_rate
FROM intervention_funnel
WHERE intervention_id = 'feature-x-adoption-q3-2026';
```

If saw_rate < 50%, the audience filter is broken. If click_through_rate < 10%, the copy/visual is weak. Iterate.

### Recipe 12: Suppress intervention for opt-outs

```python
# Honor in-product nudge opt-out flag
suppression_list = posthog.query("""
SELECT properties.customer_id FROM events
WHERE properties.in_app_nudges_opt_out = true
""")

treatment_cohort_filtered = [c for c in treatment_cohort if c.id not in suppression_list]
```

### Recipe 13: Cross-feed low-adoption signal to product

```python
# If after 28 days adoption < 25% in treatment cohort, file Linear issue
adoption_rate = recipe_10_results.treatment.adoption_pct

if adoption_rate < 25:
    linear.create_issue(
        title=f"Feature X adoption stuck at {adoption_rate}% in eligible Growth+ cohort",
        description=f"After nudge + email + CSM follow-up, adoption is still {adoption_rate}% in treatment cohort of {cohort_size}. Suggest product review of: discoverability, copy, friction in first-use.",
        labels=["voice-of-customer", "feature-adoption", "product-review"],
    )
```

## Examples

### Example 1: Feature X launched 30 days ago, 18% adoption in eligible cohort

**Goal:** Drive adoption from 18% to 35% in next 28 days.

**Steps:**
1. Day 0: Recipe 1 defines cohort (412 eligible). Recipe 2 holds out 62 (15%) as control.
2. Day 0: Recipe 3 (or 4 / 5 depending on platform) enrolls 350 treatment.
3. Day 0: Recipe 6 publishes Pendo guide.
4. Day 7: Recipe 7 fires Klaviyo D+7 email for non-adopters.
5. Day 14: Recipe 8 CSM follow-up for enterprise non-adopters (~28 customers).
6. Day 28: Recipe 10 measures. Treatment 36% adoption; control 19%. +17pp lift, statistically significant.
7. Recipe 11 funnel: saw_rate 78%, click_through 22%, open_to_use 88% - the click_through is the weak link.
8. Iterate copy in Pendo guide; re-run on residual non-adopters.

**Result:** Adoption ~doubled in treatment cohort; learning captured for next intervention.

### Example 2: Renewal-blocker feature unused at D60

**Goal:** Enterprise customer Acme.Corp hasn't used Feature Y; renewal in 30 days.

**Steps:**
1. CSM flags in standup.
2. Skip cohort logic - single-customer intervention.
3. Recipe 5 enrolls Acme in Appcues feature-Y guide.
4. Recipe 8 CSM follow-up: "Saw the renewal coming; thought we should walk through Feature Y. 30-min call?"
5. CSM books call; runs walkthrough; documents in Notion success plan.
6. Cross-check `customer-health-scoring` health-score trend - should bump.

**Result:** Direct touch + nudge combination; renewal risk reduced.

### Example 3: Holdout reveals null effect - kill the program

**Goal:** Tested Feature Z nudge; measurement shows no lift.

**Steps:**
1. Day 0-14: same as Example 1.
2. Day 28: Recipe 10 measures. Treatment 22%; control 21%. No effect.
3. Recipe 11 funnel: saw_rate 85%; click_through 15%; open_to_use 35%. The open_to_use is the bottleneck - feature itself isn't engaging.
4. Recipe 13 files Linear issue describing the funnel - product owns next step.
5. Pause the intervention; don't waste in-app real estate.

**Result:** Saved CS team from continuing a low-ROI program; surfaced product issue for fix.

## Edge cases / gotchas

- **No control group = no learning** — without a holdout, you can't tell if the lift is from the nudge or from baseline growth. Always hold out 10-20%.
- **Audience filter broken** — `feature_x_used = false` only works if the trait is fresh. If trait sync is nightly + cohort built mid-day, you'll target users who already used the feature 2 hours ago. Use real-time event check, not stale trait.
- **In-app fatigue** — same user enrolled in 4 simultaneous interventions sees 4 nudges per session. Set max-1-active-intervention-per-user policy; queue the rest.
- **Wrong success event** — measuring `feature_x_button_clicked` when real adoption needs `feature_x_completed_with_success`. Define success at outcome level, not click level.
- **Cohort drift during measurement** — customer signs up + becomes eligible on Day 5 of a 14-day measurement window. Include in next cohort, not current.
- **Survivorship in control** — if control customers churn at higher rate than treatment, the measured adoption_pct of control is inflated (only the engaged ones remain). Use intent-to-treat math.
- **Platform priority conflict** — Pendo + Appcues + Userpilot in the same product = one suppresses the others. Pick one for in-app, use email for the rest.
- **Customer in trial vs paid** — adoption math should split by stage; trial-stage adoption rates ≠ paid.
- **Mobile vs web exposure** — nudge built for web won't show to mobile-only users; cohort needs `last_session_platform` filter or the nudge will show 0 exposures.
- **Internal team in cohort** — your own employees signed up for testing; exclude `email LIKE '@yourdomain.com'` from cohort.
- **Multi-user accounts** — feature usage by 1 admin counts as adoption; do you want that, or do you want power-user adoption (3+ users)? Define explicitly.
- **Long-tail revisit** — customer ignores nudge 14d window but adopts at day 30. Include in extended-window measurement; report separately.
- **Klaviyo flow conflict** — flow filter "did not use feature X" needs Klaviyo profile sync of that property; if sync lags, you'll send to people who already adopted.
- **CSM-Lead overrides** — VP CS may want to skip an Enterprise-tier nudge if there's a sensitive ongoing negotiation. Allow per-customer suppression flag.
- **Feature deprecated mid-program** — product team kills Feature X mid-test. Halt intervention immediately; reroute cohort to the replacement.

## Sources

- [Pendo Engage API + guides](https://developers.pendo.io/)
- [Pendo segment API](https://help.pendo.io/resources/support-library/segmentation/index)
- [Userpilot REST API](https://docs.userpilot.com/article/195-userpilot-rest-api)
- [Userpilot flow targeting](https://docs.userpilot.com/)
- [Appcues REST API](https://help.appcues.com/en/articles/123-appcues-rest-api)
- [Appcues audience targeting docs](https://docs.appcues.com/en_US/articles/targeting-flows-to-the-right-users)
- [PostHog cohorts](https://posthog.com/docs/product-analytics/cohorts)
- [PostHog HogQL query API](https://posthog.com/docs/api/queries)
- [Klaviyo events API](https://developers.klaviyo.com/en/reference/events_api_overview)
- [Klaviyo flows + filters](https://developers.klaviyo.com/en/reference/api_overview)
- [Customer.io transactional API](https://customer.io/docs/api/)
- [Mixmax sequence API](https://help.mixmax.com/hc/en-us)
- [A/B testing for product adoption (CXL)](https://cxl.com/blog/ab-testing-statistics/)
