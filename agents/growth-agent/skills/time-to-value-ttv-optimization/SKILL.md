<!--
Source: Lenny's PLG Handbook TTV chapter + Stackmatix PLG onboarding + Userpilot 2024 547-SaaS TTV benchmarks
-->
# Time-to-Value (TTV) Optimization SKILL

> Measure, decompose, and reduce TTV (signup → first value event). Best-in-class < 5 minutes self-serve. Uses HogQL percentile queries, step-decomposition, and a ranked reduction tactic table.

## When to use

Trigger phrases:
- "How long does signup-to-value take?"
- "Reduce time-to-value"
- "Onboarding takes too long"
- "Our trial isn't converting" (often TTV problem)
- "Why do users drop off post-signup?" (TTV step-decomposition)

Pair: `activation-funnel-aha-moment` (defines the value event), `signup-activation-conversion-optimization` (funnel diagnosis), `onboarding-userpilot-appcues-chameleon` (delivery).

## Setup

```bash
export POSTHOG_PERSONAL_API_KEY="phx_..."
export AMPLITUDE_OAUTH_TOKEN="amp_..."
```

Required events:
- `User Signed Up` (entry)
- Step events (`Email Verified`, `Account Setup Started`, `First Action Taken`, ... )
- `<value_event>` (the activation event defined per `activation-funnel-aha-moment`)

## TTV math + benchmarks

```
TTV = time(<value_event>) - time(User Signed Up)
Track p25, p50, p75, p95.
```

Userpilot 2024 baseline across 547 SaaS:
- All-segment median TTV: ~36 hours
- AI/ML products: 1-4 hours
- HR/finance products: days
- DevTools: hours-days
- Marketing tools: 1-2 days
- Best-in-class self-serve: < 5 minutes
- Enterprise w/ implementation: < 7 days

## Common recipes

### Recipe 1: TTV percentiles + segmentation

```sql
SELECT
  properties.icp_segment AS segment,
  count() AS users,
  quantile(0.25)(ttv_min) AS p25_min,
  quantile(0.5)(ttv_min) AS p50_min,
  quantile(0.75)(ttv_min) AS p75_min,
  quantile(0.95)(ttv_min) AS p95_min
FROM (
  SELECT
    person_id,
    properties.icp_segment,
    dateDiff('minute',
      minIf(timestamp, event = 'User Signed Up'),
      minIf(timestamp, event = '<value_event>')
    ) AS ttv_min
  FROM events
  WHERE event IN ('User Signed Up', '<value_event>')
    AND timestamp >= now() - INTERVAL 60 DAY
  GROUP BY person_id, properties.icp_segment
  HAVING ttv_min > 0
)
GROUP BY segment
ORDER BY p50_min ASC
```

### Recipe 2: Step decomposition — where is time spent?

```sql
SELECT
  step,
  quantile(0.5)(seconds_to_step) AS p50_sec,
  quantile(0.75)(seconds_to_step) AS p75_sec,
  count() AS users_reached_step
FROM (
  SELECT
    person_id,
    'signup_to_verify' AS step,
    dateDiff('second',
      minIf(timestamp, event = 'User Signed Up'),
      minIf(timestamp, event = 'Email Verified')
    ) AS seconds_to_step
  FROM events GROUP BY person_id
  UNION ALL
  SELECT
    person_id,
    'verify_to_first_action',
    dateDiff('second',
      minIf(timestamp, event = 'Email Verified'),
      minIf(timestamp, event = 'First Action Taken')
    )
  FROM events GROUP BY person_id
  UNION ALL
  SELECT
    person_id,
    'first_action_to_value',
    dateDiff('second',
      minIf(timestamp, event = 'First Action Taken'),
      minIf(timestamp, event = '<value_event>')
    )
  FROM events GROUP BY person_id
)
WHERE seconds_to_step > 0
GROUP BY step
ORDER BY p50_sec DESC
```

Whichever step has the highest p50 = the TTV bottleneck. Often: email verification (10-60min), workspace setup (5-30min), data import (10-120min).

### Recipe 3: TTV reduction tactics — ranked by typical impact

| Tactic | Typical reduction | Effort | Apply when |
|---|---|---|---|
| **Passwordless / magic-link signup** | -2 to -10 min | Low | Long signup-to-verify |
| **OAuth (Google/GitHub/MS)** | -30s to -3 min | Low | B2B SaaS |
| **Skip onboarding for power users** | -5 to -30 min | Low | Long-tail TTV (p95) |
| **AI-assisted setup (Claude)** | -10 to -60 min | Medium | Complex config |
| **Pre-populated templates** | -5 to -30 min | Low | Blank canvas problem |
| **Defaults that demonstrate value** | -3 to -10 min | Low | Most products |
| **Progress checklist + visual** | -2 to -8 min | Low | Multi-step setup |
| **In-app tour (only if complex)** | -1 to -5 min OR +5 min | Med | Genuinely complex |
| **Concierge / DFY for top 1-5%** | -hours | High | High-ACV PLG |
| **Setup wizard branching** | -3 to -15 min | Med | Multi-persona |

### Recipe 4: A/B test TTV reduction via GrowthBook

```javascript
await growthbook.create_experiment({
  name: "ttv-magic-link-signup",
  hypothesis: "Magic-link signup reduces p50 TTV by 30% by removing email/password friction",
  variants: [
    { name: "control_password", weight: 0.5 },
    { name: "magic_link", weight: 0.5 }
  ],
  primary_metric: "p50_ttv_minutes",
  secondary_metrics: ["signup_completion_rate", "activation_rate_7d"],
  sample_size_calc: { mde: 0.15, baseline: 28, power: 0.80, alpha: 0.05 },
  guardrails: ["d7_retention", "fake_signup_rate"],
  kill_criteria: {
    fake_signup_rate_increase: 0.05,
    p_value_negative: 0.01
  }
});
```

### Recipe 5: Identify long-tail users (p95+) and intervene

```sql
SELECT
  person_id,
  properties.email,
  properties.icp_segment,
  ttv_min,
  status_at_intervention
FROM (
  SELECT
    person_id,
    properties.email,
    properties.icp_segment,
    dateDiff('minute', signup_ts, COALESCE(value_ts, now())) AS ttv_min,
    CASE WHEN value_ts IS NOT NULL THEN 'activated_late'
         ELSE 'stalled' END AS status_at_intervention
  FROM user_journey
  WHERE signup_ts <= now() - INTERVAL 2 DAY
    AND signup_ts >= now() - INTERVAL 14 DAY
)
WHERE ttv_min > 1440  -- > 24h
ORDER BY ttv_min DESC
LIMIT 100
```

Pipe stalled users to:
- Customer.io concierge email: "Setup help"
- Slack channel (`#growth-stuck`) for high-ACV cases

### Recipe 6: AI-assisted setup pattern (Claude-powered)

```python
# When user enters setup wizard, Claude pre-fills based on their goal
def ai_setup_assist(user_input):
    """User describes goal in 1 sentence; Claude generates initial config."""
    config = claude.generate(
        prompt=f"""Generate initial config JSON for a user whose goal is:
        "{user_input}"
        
        Config schema: {{
            'workspace_name': str,
            'starter_template': str,  // one of: blog, docs, project, dashboard
            'initial_collaborators': list[str],
            'preset_integrations': list[str]
        }}
        """,
        model="claude-sonnet-4-5"
    )
    return config

# Cuts setup from 8 min average → < 90 sec average
```

### Recipe 7: TTV monitoring + alerting

```python
# Weekly cron — alert on regression
weekly_ttv = posthog.query(ttv_percentile_sql)
if weekly_ttv['p50_min'] > prev_week['p50_min'] * 1.20:
    slack.send(
        channel="#growth-alerts",
        text=f"TTV p50 regression: {prev_week['p50_min']:.1f}m -> {weekly_ttv['p50_min']:.1f}m"
    )
```

### Recipe 8: Compare TTV across acquisition channels

```sql
SELECT
  properties.utm_source AS source,
  count() AS users,
  quantile(0.5)(ttv_min) AS p50,
  quantile(0.75)(ttv_min) AS p75,
  avg(activated_7d) AS activation_rate
FROM cohort_with_ttv_and_activation
GROUP BY source
HAVING users >= 50
ORDER BY activation_rate DESC
```

Inverse correlation: channels with high TTV usually have low activation. Either fix channel-specific onboarding OR reduce paid spend on slow-converting channels.

## Examples

### Example 1: Project management SaaS, TTV p50 = 4h 12m

Step decomposition:
- signup → email_verified: p50 = 12min
- verify → first_project_created: p50 = 3h 22m  ← bottleneck
- first_project → first_value_event (3 tasks added): p50 = 28min

Diagnosis: users sit on the empty-project view, don't know where to start.

Plan:
1. Pre-populate first project with 3 starter tasks (template).
2. Onboarding modal: "Try our 30-second demo project."
3. AI-assisted: user enters team goal → Claude generates 5 starter tasks + project structure.
4. Re-measure in 4 weeks; target p50 < 1h.

### Example 2: AI dev tool, TTV p50 = 28 min, p95 = 12h

p95 driven by users who don't have an API key handy.

Plan:
1. Demo-only mode: explore product without API key.
2. Inline API-key generation flow (no leaving the product).
3. Magic-link signup → reduce verification overhead.

Result: p50 -> 9 min, p95 -> 2h.

## Edge cases / gotchas

- **TTV needs a denominator** — never report "TTV = 30 min" without saying "of activated users". Stalled users have undefined TTV; report % activated alongside.
- **Bimodal distributions** — power users finish in 3 min; novices take 4 hours. Report percentiles, not average.
- **Watch user-class proxies** — segmenting by ICP often shows the long-tail is one persona; tailor onboarding accordingly.
- **Email verification can be 30+ min just for delivery** — measure verification-mechanism latency separately from user choice.
- **TTV improvements can hurt conversion** — if shortcut bypasses educational moments, users churn later. Always track activation_rate as secondary metric.
- **Survivorship bias** — measuring TTV only on users who activated hides the long-tail churners. Use "censored TTV" with right-censoring at 72h or longer.
- **Holiday + weekend artifacts** — TTV spikes around weekends. Filter to weekdays for cleaner trends.
- **Mobile vs desktop TTV differ wildly** — segment by platform; mobile signup often 2-3x faster but lower activation.
- **Premature optimization** — if D30 retention is decay, TTV isn't your problem; activation IS your problem. Diagnose retention curve first via `retention-curve-churn-diagnosis-j-smile`.

## Sources

- Lenny's PLG Handbook — Time to Value: https://plghandbook.com/time-to-value/
- Stackmatix — PLG Onboarding & Activation: https://www.stackmatix.com/blog/plg-onboarding-activation
- Userpilot — Time to Value Stats 2024: https://userpilot.com/blog/time-to-value/
- Digital Applied — 2026 SaaS TTV framework: https://www.digitalapplied.com/blog/customer-onboarding-time-to-value-2026-saas-metrics-framework
- Appcues — Activation rate + TTV: https://www.appcues.com/blog/product-led-growth-metrics
- Reforge — Casey Winters activation: https://www.reforge.com/blog/why-activation-is-the-most-important-metric
- PostHog HogQL: https://posthog.com/docs/hogql
