<!--
Source: PostHog HogQL viral coefficient tutorial + Amplitude cohort formulas + Andrew Chen viral math
-->
# Viral Coefficient K — Measurement, Diagnosis, Optimization SKILL

> Measure, decompose, and optimize the viral coefficient K = invites_per_user × acceptance_rate, using PostHog HogQL or Amplitude formulas. Includes cohort weighting, cycle-time integration, and the K-> 1 lever decision tree.

## When to use

Use this when the user says:
- "What's our K?"
- "Is our product viral?"
- "How do we grow K?"
- "Should we add a referral program?" (K = self-driven viral; referral = incentivized — different math)
- "Why isn't our viral loop compounding?"
- "What is the value of an invite?"

Do NOT use for:
- Network effects (use `growth-loop-design-5-types` Loop type 4)
- Referral programs with monetary incentive (use `referral-program-referralcandy-friendbuy-growsurf`)
- Multi-touch attribution (use `attribution-last-multi-touch-mmm-meridian-robyn`)

## Setup

```bash
export POSTHOG_PERSONAL_API_KEY="phx_..."
export POSTHOG_PROJECT_ID="<id>"
export AMPLITUDE_OAUTH_TOKEN="amp_..."
export MIXPANEL_API_KEY="mx_..."
```

Required tracked events (in CDP / PostHog):
- `Invite Sent` (properties: `inviter_id`, `invite_channel`, `recipient_email_hash`)
- `Invite Accepted` (properties: `inviter_id`, `accepted_at`)
- `User Signed Up` (properties: `signup_source`, `referrer_id`)
- Optionally: `Invite Viewed` (open rate for invites)

Object-Action past-tense naming — required for cohort joins downstream.

## The K formula (canonical)

```
K = (invites_sent_per_user) × (acceptance_rate)

Where:
  invites_sent_per_user = total_invites / users_in_cohort   (not "inviting users" — see gotcha 1)
  acceptance_rate       = invites_accepted / invites_sent
```

Compound projection (geometric, K < 1):
```
users_at_saturation = N0 / (1 - K)
total_lift_factor   = 1 / (1 - K)

K = 0.10  → 1.11x lift
K = 0.30  → 1.43x lift
K = 0.50  → 2.00x lift
K = 0.80  → 5.00x lift
K = 0.95  → 20.0x lift
K ≥ 1.00  → exponential (no saturation)
```

## Common recipes

### Recipe 1: Canonical K query (PostHog HogQL)

```sql
WITH cohort AS (
  SELECT DISTINCT person_id
  FROM events
  WHERE event = 'User Signed Up'
    AND timestamp >= now() - INTERVAL 30 DAY
),
invites AS (
  SELECT
    person_id,
    countIf(event = 'Invite Sent') AS invites_sent,
    countIf(event = 'Invite Accepted'
            AND timestamp >= properties.invite_sent_at) AS accepted
  FROM events
  WHERE person_id IN (SELECT person_id FROM cohort)
    AND timestamp >= now() - INTERVAL 30 DAY
  GROUP BY person_id
)
SELECT
  count() AS cohort_size,
  sum(invites_sent) AS total_invites_sent,
  sum(accepted) AS total_accepted,
  sum(invites_sent) * 1.0 / count() AS invites_per_user,
  sum(accepted) * 1.0 / nullIf(sum(invites_sent), 0) AS acceptance_rate,
  (sum(invites_sent) * 1.0 / count()) *
    (sum(accepted) * 1.0 / nullIf(sum(invites_sent), 0)) AS K
FROM cohort
LEFT JOIN invites USING (person_id)
```

Run weekly. Track K trend, not single-week snapshot.

### Recipe 2: K decomposition (find the leak)

```sql
SELECT
  toStartOfWeek(timestamp) AS week,
  count(DISTINCT inviter_id) AS active_inviters,
  countDistinct(person_id) FILTER (WHERE event = 'User Signed Up') AS new_signups,
  active_inviters * 1.0 / new_signups AS pct_users_who_invite,
  count() FILTER (WHERE event = 'Invite Sent') * 1.0 / active_inviters AS invites_per_inviter,
  count() FILTER (WHERE event = 'Invite Sent') * 1.0 / new_signups AS invites_per_user,
  count() FILTER (WHERE event = 'Invite Accepted') * 1.0 /
    nullIf(count() FILTER (WHERE event = 'Invite Sent'), 0) AS acceptance_rate
FROM events
WHERE event IN ('Invite Sent','Invite Accepted','User Signed Up')
  AND timestamp >= now() - INTERVAL 12 WEEK
GROUP BY week
ORDER BY week
```

Decomposition table (track over time):

| Metric | Definition | If low… |
|---|---|---|
| pct_users_who_invite | Users sending ≥ 1 invite / total users | Invite CTA discoverability / placement |
| invites_per_inviter | Avg invites per inviter (conditional) | Friction in invite UX; one-at-a-time forces |
| acceptance_rate | Accepted / sent | Invite copy, sender clarity, landing-page friction |
| invitee_activation_rate | Activated / accepted (downstream) | Onboarding (different skill: activation-funnel-aha-moment) |

### Recipe 3: Cohort-weighted K (per acquisition cohort)

K varies wildly by user cohort source. Compute per-source.

```sql
SELECT
  properties.signup_source AS source,
  count() AS cohort_size,
  avg(invites_sent_per_user) AS avg_invites,
  avg(K) AS K_per_cohort
FROM (
  SELECT
    person_id,
    properties.signup_source,
    countIf(event = 'Invite Sent') AS invites_sent_per_user,
    countIf(event = 'Invite Accepted') * 1.0 /
      nullIf(countIf(event = 'Invite Sent'), 0) AS per_user_acceptance,
    invites_sent_per_user * per_user_acceptance AS K
  FROM events
  WHERE person_id IN (
    SELECT person_id FROM events
    WHERE event = 'User Signed Up'
      AND timestamp >= now() - INTERVAL 90 DAY
  )
  GROUP BY person_id, properties.signup_source
)
GROUP BY source
ORDER BY K_per_cohort DESC
```

Insight: users from an existing invite usually have K 2-4x higher (they grok the loop). Identify your highest-K source and double down on acquisition there.

### Recipe 4: Amplitude formula equivalent

```javascript
// Amplitude — using cohort + behavioral cohort
// 1. Create cohort: users who signed up in last 30d
// 2. Create event metric: total Invite Sent / cohort size = invites_per_user
// 3. Create event metric: Invite Accepted / Invite Sent = acceptance_rate
// 4. K = product of the two

await amplitude.create_cohort({
  name: "Last 30d Signups",
  definition: {
    event: "User Signed Up",
    timeframe: "last_30_days"
  }
});
// Then chart: behavioral_metric_a × behavioral_metric_b
```

### Recipe 5: Mixpanel JQL equivalent

```javascript
// Mixpanel JQL
function main() {
  return Events({
    from_date: "2026-05-10",
    to_date: "2026-06-09",
    event_selectors: [
      { event: "Invite Sent" },
      { event: "Invite Accepted" },
      { event: "User Signed Up" }
    ]
  })
  .groupBy(["distinct_id"], mixpanel.reducer.count_by("name"))
  .reduce(function(accum, items) {
    let invites = 0, accepted = 0, users = 0;
    items.forEach(i => {
      if (i.key[1] === "Invite Sent") invites += i.value;
      if (i.key[1] === "Invite Accepted") accepted += i.value;
      if (i.key[1] === "User Signed Up") users += 1;
    });
    return { invites, accepted, users, K: (invites/users) * (accepted/invites) };
  });
}
```

### Recipe 6: K-> 1 lever decision tree

```text
Current K < 0.10   → Invite mechanic discoverability is the problem.
                     Fix: surface invite CTA in main flow + post-aha empty states.
                     Expected lift: K 5-10x in 4-8 weeks.

K = 0.10 - 0.30    → Acceptance rate is the leak.
                     Fix: invite copy A/B, sender name personalization, landing-page rebuild.
                     Expected lift: 1.5-2x acceptance.

K = 0.30 - 0.60    → Invites-per-user too low.
                     Fix: bulk invite (CSV upload, contact sync), invite-for-feature-unlock gating.
                     Expected lift: 2-3x invites/user.

K = 0.60 - 0.95    → Activation of invited users is the leak.
                     Fix: hand off to activation-funnel-aha-moment skill.
                     Optimize invitee-specific onboarding.

K ≥ 0.95           → Diminishing returns; protect against regression.
                     Hold steady; double down on retention + revenue per user instead.
```

### Recipe 7: Compute the value of an invite

```python
# Value of an invite = (acceptance_rate × invitee_activation_rate × invitee_LTV)
invite_value = acceptance_rate * invitee_activation_rate * invitee_LTV

# Example: 30% acceptance × 40% activation × $360 LTV = $43.2 per invite sent
# Compare to invite cost (e.g., free for self-serve, $5-25 for cash incentive)
# Margin per invite informs incentive budget
```

### Recipe 8: K trend regression detection

```sql
-- Detect K weekly regression > 15% WoW
WITH weekly_k AS (
  -- (use Recipe 2 query, by week)
)
SELECT
  week,
  K,
  lag(K) OVER (ORDER BY week) AS prev_K,
  (K - prev_K) / prev_K * 100.0 AS pct_change
FROM weekly_k
WHERE prev_K IS NOT NULL
ORDER BY week DESC
```

Alert on `pct_change < -15`. Pipe to `slack-mcp` (`#growth-alerts`).

## Examples

### Example 1: B2B SaaS, "Our viral loop is dead"

Discovery: K = 0.06.

Decomposition:
- pct_users_who_invite = 4% → very low
- invites_per_inviter = 2.3 → fine
- acceptance_rate = 65% → great

Diagnosis: discoverability problem. Users don't know they can invite.

Plan:
1. A/B test: invite CTA in empty-state of shared-workspace tab (Treatment) vs settings-only (Control). Primary metric: pct_users_who_invite (Day 14). MDE = 5pp absolute. Sample size 1200/arm.
2. Add post-document-share modal: "Share with teammate?" (separate test).
3. Re-measure K monthly; target K = 0.25 in 12 weeks.

### Example 2: Consumer social, "K = 1.2 but DAU not growing"

Diagnosis: K is per-cycle, but cycle time is 21 days. New-user activation rate among invitees = 15%. Effective compounding rate is much lower.

Plan:
1. Compute "effective K" = K × invitee_activation_rate = 1.2 × 0.15 = 0.18.
2. The real bottleneck is invitee activation, not invite virality.
3. Switch focus to `activation-funnel-aha-moment` skill for invitees specifically.

## Edge cases / gotchas

- **Denominator confusion** — invites_per_user uses *all* users in cohort, not just those who invited. Using "inviters" as denominator inflates K artificially.
- **Acceptance window** — must specify time window. "Accepted within 30 days of sent" is standard; broader windows skew low.
- **Re-invite double-count** — same recipient invited multiple times. Deduplicate by `recipient_email_hash` before computing acceptance rate.
- **Invitee = same person** — sometimes a user invites themselves (testing). Filter `inviter_id != recipient_id`.
- **Cycle time matters as much as K** — K=0.8 with 14-day cycles compounds 26x/year; K=1.5 with 365-day cycles barely compounds in 2 years. Always pair K with cycle time.
- **Network maturity dampens K** — as TAM saturates, acceptance rates fall (recipient already user). Adjust forecasts.
- **"K" terminology confusion** — Reforge defines K as `invites × accept`. Some define as `invitees who become users / inviter`. Same math when invitee_activation_rate = 1. Always state your formula.
- **Confidence intervals** — for cohorts < 100 inviters, K wobbles. Report ± 1 SE. Use bootstrap if rigorous.
- **Don't conflate viral and referral** — viral = no monetary incentive, intrinsic. Referral = monetary. Track separately; referral has additional cost/incentive math.

## Sources

- PostHog — Viral coefficient tutorial: https://posthog.com/tutorials/viral-coefficient
- Andrew Chen — "The most important growth equation": https://andrewchen.com/the-most-important-growth-equation/
- Reforge — Viral loops + K: https://www.reforge.com/blog/viral-loops
- Amplitude — Cohort analysis for K: https://amplitude.com/explore/analytics/cohort-retention-analysis
- Stackmatix PLG funnel: https://www.stackmatix.com/blog/plg-funnel-metrics
- ProductLed PLG metrics (K-factor): https://www.productled.org/foundations/product-led-growth-metrics
- Lenny's PLG Handbook (viral mechanics): https://plghandbook.com/
