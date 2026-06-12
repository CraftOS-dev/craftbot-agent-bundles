<!--
Source: PostHog funnel analytics + Stackmatix PLG funnel metrics + GrowthBook MCP experiment patterns
-->
# Signup → Activation Conversion Optimization SKILL

> Diagnose funnel leaks (signup → verify → onboarding → activation), reduce friction, and ship A/B tests at each step. Distinct from retention curve diagnosis — this is the pre-aha funnel surgery.

## When to use

Trigger phrases:
- "Our signup-to-activation funnel is leaking"
- "Why aren't users finishing onboarding?"
- "Email verification step is killing conversion"
- "Magic-link / SSO experiments"
- "Reduce signup friction"

Pair: `activation-funnel-aha-moment` (defines the goal event), `time-to-value-ttv-optimization` (the speed metric), `onboarding-userpilot-appcues-chameleon` (delivery), `landing-page-cro-vwo-hotjar-maze` (page CRO).

## Setup

```bash
export POSTHOG_PERSONAL_API_KEY="phx_..."
export GROWTHBOOK_API_KEY="gb_..."
```

Required taxonomy:
- `User Signed Up` → `Email Verified` → `Onboarding Step N Completed` → `Activation Event Hit`
- Properties: `signup_source`, `signup_method` (email / magic / oauth), `icp_segment`

## The canonical funnel

```
Visit → Signup form viewed → Signup attempted → Account created → Email verified
  → Onboarding entered → Onboarding step 1 done → Step N done → Activation event
```

Track conversion at each step. The lowest-conversion step is the constraint.

Benchmarks (Stackmatix 2024):
- Visit → signup form viewed: ~10-25% (driven by landing page CRO)
- Signup form viewed → submit: 30-60% (form friction)
- Submit → account created: 90%+ (technical)
- Account created → email verified: 60-85% (verification UX)
- Verified → onboarding complete: 40-70%
- Onboarding → activation: 25-60%

## Common recipes

### Recipe 1: Full funnel measurement (PostHog funnel)

```bash
mcp tool posthog.funnel \
  --name "Signup → Activation Full Funnel" \
  --steps '[
    {"event": "$pageview", "properties": {"$pathname": "/signup"}},
    {"event": "User Signed Up"},
    {"event": "Email Verified"},
    {"event": "Onboarding Step 1 Completed"},
    {"event": "Onboarding Step N Completed"},
    {"event": "<activation_event>"}
  ]' \
  --conversion_window_seconds 604800 \
  --date_range "last_30_days" \
  --breakdown "properties.signup_method"
```

Output: step-by-step conversion + breakdown by signup method. Lowest pct = the leak.

### Recipe 2: Leak prioritization (which step to fix first)

```python
# Rank by lift potential = current_users_lost × industry_benchmark_lift
funnel = {
    "Visit → form_view": {"conv": 0.18, "benchmark": 0.20, "n_visits": 100_000},
    "form_view → submit": {"conv": 0.42, "benchmark": 0.50, "n_visits": 18_000},
    "submit → verified": {"conv": 0.71, "benchmark": 0.80, "n_visits": 7_560},
    "verified → onboarding": {"conv": 0.48, "benchmark": 0.60, "n_visits": 5_368},
    "onboarding → activation": {"conv": 0.33, "benchmark": 0.45, "n_visits": 2_577},
}

# Lift potential at each step
for step, data in funnel.items():
    gap_pp = data["benchmark"] - data["conv"]
    users_recovered = data["n_visits"] * gap_pp
    print(f"{step}: gap={gap_pp*100:.1f}pp; potential recovery={users_recovered:.0f} users")
```

Highest "potential recovery" wins. Often the verify step or onboarding entry.

### Recipe 3: Reduce email verification friction (most common leak)

```text
Tactics (ranked by typical lift):
1. Magic-link signup (no password)      → +15-25% verification rate
2. OAuth (Google/MS)                    → +20-35%; bypasses verify entirely
3. Magic-link as one-tap action         → +5-10% above plain
4. Reduce email-send latency (<30s)     → +5-10%
5. Resend button visible on every page → +3-7%
6. Skip-verify for some segments        → +20% but raises fraud risk
```

A/B test (one at a time):

```javascript
await growthbook.create_experiment({
  name: "signup-magic-link",
  variants: [
    { name: "control_password", weight: 0.5 },
    { name: "treatment_magic_link", weight: 0.5 }
  ],
  primary_metric: "verified_within_5min",
  secondary_metrics: ["activation_rate_7d", "fake_signup_rate"],
  guardrails: ["fake_signup_rate", "verification_failure_rate"],
  sample_size: 3500,
  mde: 0.10
});
```

### Recipe 4: Signup form friction reduction

```text
Tactics:
1. Single-field signup (email-only) + progressive profile     → +20-40%
2. Pre-filled fields from UTM (e.g., role from ad targeting) → +5-10%
3. Social proof above form (avatars / count)                → +3-8%
4. Inline error validation                                   → +5-15%
5. Remove "confirm password" → one password field            → +5-10%
6. Reduce captcha aggression (only on suspicion)             → +5-10%
```

### Recipe 5: Onboarding entry leak

If "verified → onboarding entry" is low: users verifying but bouncing.

```sql
SELECT
  properties.utm_source,
  count() AS users,
  countIf(reached_onboarding_within_1h) AS entered,
  entered * 100.0 / count() AS entry_rate
FROM cohort_after_verify
GROUP BY properties.utm_source
ORDER BY entry_rate DESC
```

Often: paid traffic users verify but don't return. Fix: ensure post-verify redirect → onboarding immediately (no logout).

### Recipe 6: Onboarding step-by-step leak

```sql
WITH steps AS (
  SELECT 'step_1' AS step UNION ALL SELECT 'step_2' UNION ALL SELECT 'step_3' UNION ALL SELECT 'step_4'
)
SELECT
  step,
  countDistinctIf(person_id, started) AS started,
  countDistinctIf(person_id, completed) AS completed,
  completed * 100.0 / started AS step_pct
FROM onboarding_step_table
GROUP BY step
```

Lowest step_pct = fix target. Common culprits:
- Step asks for data user doesn't have (API key, integration credentials)
- Step requires email confirmation of teammate
- Step is unclear / wrong order

### Recipe 7: Slice by signup source (channel-quality)

```sql
SELECT
  properties.utm_source,
  countDistinct(person_id) AS signups,
  countDistinctIf(person_id, verified) AS verified,
  countDistinctIf(person_id, activated_7d) AS activated,
  verified * 100.0 / signups AS verify_pct,
  activated * 100.0 / signups AS activation_pct,
  activated * 100.0 / verified AS verified_to_activated_pct
FROM cohort_with_status
GROUP BY properties.utm_source
HAVING signups >= 100
ORDER BY activation_pct DESC
```

If a channel has high signups + low activation → low-quality signups. Cut paid spend or rework ads to attract right users.

### Recipe 8: Segment by ICP — different funnel per persona

```sql
SELECT
  properties.icp_segment,
  step,
  countDistinct(person_id) AS users,
  countDistinctIf(person_id, completed_step) AS completed,
  completed * 100.0 / users AS step_pct
FROM cohort_funnel_segmented
GROUP BY properties.icp_segment, step
ORDER BY properties.icp_segment, step
```

If one persona drops at step 3 (e.g., "Connect data source"), that step doesn't fit their workflow.

### Recipe 9: Cycle-time analysis — how slow is each step?

```sql
SELECT
  step,
  quantile(0.5)(minutes_in_step) AS p50_min,
  quantile(0.75)(minutes_in_step) AS p75_min
FROM step_timing_table
GROUP BY step
ORDER BY p50_min DESC
```

p50 > 30 min suggests user paused / left / returned. Save state aggressively; allow resume.

### Recipe 10: PostHog feature-flag-gated experiments

```javascript
// GrowthBook + PostHog combo for full instrumentation
// 1. GrowthBook controls variant
// 2. PostHog tracks events with $feature_flag_response

posthog.capture('User Signed Up', {
  $feature_flag_response: variant,  // automatic if integrated
  signup_method: 'magic_link'
});

// 3. Analyze via PostHog query
SELECT
  properties.$feature_flag_response,
  countDistinct(person_id) AS users,
  countDistinctIf(person_id, verified) AS verified,
  verified * 100.0 / users AS verify_pct
FROM events
WHERE properties.$feature_flag = 'signup-magic-link'
GROUP BY properties.$feature_flag_response
```

## Examples

### Example 1: Project mgmt SaaS, total signup → activation = 8%

Funnel:
- Visit → form_view: 22%
- Form_view → submit: 31% ← leak
- Submit → verify: 78%
- Verify → onboarding: 64%
- Onboarding → activation: 38%

Diagnosis: form_view → submit gap (31% vs 50% benchmark). 19pp gap × 22K monthly form views = 4180 users lost.

Plan:
1. Reduce form fields (8 → 3).
2. Test magic-link path.
3. Inline error validation.

Expected: 31% → 45%; recover ~3000 signups/mo.

### Example 2: B2B SaaS, paid channel low activation

Funnel by channel:
- Organic: signup → activation = 41%
- Paid (Google): 14%
- Paid (LinkedIn): 32%

Diagnosis: Google paid traffic doesn't match ICP; ads attract curious browsers.

Plan:
1. Tighten Google ad targeting (ICP keywords only).
2. Add qualification step on signup form (role, team size).
3. Slow ramp budget while iterating.

### Example 3: Verify step at 52% (B2B)

Diagnosis: email delivery latency p50 = 4 min (users bounce).

Plan:
1. Switch transactional email provider (Postmark / SES).
2. Add magic-link path.
3. Verification reminder via Customer.io if not done in 1 hour.

## Edge cases / gotchas

- **Funnel definition matters** — "any session" vs "specific event" gives different conversion. Pick meaningful events.
- **Conversion window** — too short (1h) undercounts; too long (30d) inflates (includes lapsed re-signups). 7d standard.
- **Channel quality inversion** — high-CTR ads sometimes attract worst signups. Always tie back to activation.
- **Email deliverability is invisible — instrument it** — track verification email sent_at vs verified_at; latency > 2 min loses 20% of users.
- **Cohort drift mid-experiment** — if you ship a homepage change while running a signup-form test, cohort changes; experiment is contaminated.
- **Survivorship in onboarding** — users who finish step 3 self-select for being more engaged; don't assume linear improvement at later steps.
- **Form re-render = false-drop signal** — multi-page forms may show "step 1 abandoned" when users just hit refresh. Track URL changes vs form re-renders carefully.
- **Mobile vs desktop signup very different** — different forms, different friction. Analyze separately.
- **Bot signup inflation** — sudden conversion lift may be bots. Track verification rate + activation rate; bots verify low.
- **OAuth dependency on provider availability** — Google sign-in outages tank verification; have fallback path.

## Sources

- PostHog Funnels: https://posthog.com/docs/product-analytics/funnels
- PostHog MCP: https://posthog.com/docs/model-context-protocol
- Stackmatix PLG funnel metrics: https://www.stackmatix.com/blog/plg-funnel-metrics
- GrowthBook MCP: https://blog.growthbook.io/introducing-the-first-mcp-server-for-experimentation-and-feature-management/
- Lenny's PLG Handbook (signup friction): https://plghandbook.com/
- Reforge — signup conversion frameworks: https://www.reforge.com/blog/
