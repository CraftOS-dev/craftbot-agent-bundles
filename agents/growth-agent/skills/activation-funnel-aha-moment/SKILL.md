<!--
Source: Stackmatix PLG onboarding+activation playbook + Sean Ellis test + Casey Winters Reforge activation framework
-->
# Activation Funnel + Aha Moment SKILL

> Identify, validate, and improve the activation event (behavioral, measurable) and aha moment (emotional, qualitative). Uses cohort-diff statistical analysis, Sean Ellis Test, and percentile TTV windowing. The single most-leveraged growth lever — activation predicts retention.

## When to use

Trigger phrases:
- "What's our activation event?"
- "Find our aha moment"
- "Why are users churning?" (likely activation, not retention)
- "Day 30 retention is decay" → activation is broken
- "How do we know if we have PMF?" (Sean Ellis Test)
- "Our funnel is leaking after signup"

Do NOT use for:
- Pure conversion optimization (use `signup-activation-conversion-optimization`)
- Lifecycle re-engagement (use `win-back-campaigns`)
- Retention curve diagnosis (use `retention-curve-churn-diagnosis-j-smile` — but activation feeds retention)

## Setup

```bash
export POSTHOG_PERSONAL_API_KEY="phx_..."
export AMPLITUDE_OAUTH_TOKEN="amp_..."
export TYPEFORM_TOKEN="tfp_..."   # for Sean Ellis test survey
export NOTION_TOKEN="ntn_..."     # cohort + activation spec storage
```

Required event taxonomy:
- `User Signed Up` (canonical entry event)
- Candidate activation events (track widely — 8-15 candidates)
- `Activated` (computed event written back via PostHog `identify` once defined)

## The activation framework (canonical)

| Concept | Definition | Tool |
|---|---|---|
| **Aha moment** | Emotional / qualitative: "I finally have X solved" | Sean Ellis Test, jobs-to-be-done interviews |
| **Activation event** | Behavioral / quantitative proxy for aha | PostHog cohort, Amplitude funnel |
| **Activation rate** | % of new users hitting activation event in 7-14d | Cohort analysis |
| **TTV (time-to-value)** | Signup → activation event, p25/p50/p75 | HogQL percentile query |
| **Magic moment N** | Specific count threshold (e.g., 3 documents created) | Cohort-diff regression |

Benchmarks (Userpilot 2024, 547 SaaS):
- B2B SaaS avg activation rate (7d): 37.5%
- Best-in-class: 60%+
- Consumer apps: highly variable
- TTV best-in-class: < 5 minutes
- TTV median: ~36 hours

## Common recipes

### Recipe 1: Cohort-diff to identify activation event candidates

```sql
-- PostHog HogQL — find behaviors that predict Day-30 retention
WITH signup_cohort AS (
  SELECT DISTINCT person_id, min(timestamp) AS signup_ts
  FROM events
  WHERE event = 'User Signed Up'
    AND timestamp >= '2026-04-01' AND timestamp < '2026-05-01'
  GROUP BY person_id
),
retained_d30 AS (
  SELECT DISTINCT s.person_id
  FROM signup_cohort s
  JOIN events e ON e.person_id = s.person_id
  WHERE e.event IN ('Session Started', 'core_action')
    AND e.timestamp BETWEEN s.signup_ts + INTERVAL 30 DAY
                        AND s.signup_ts + INTERVAL 37 DAY
),
candidate_actions AS (
  SELECT
    e.event,
    e.person_id,
    s.person_id IN (SELECT person_id FROM retained_d30) AS retained
  FROM signup_cohort s
  JOIN events e ON e.person_id = s.person_id
  WHERE e.timestamp BETWEEN s.signup_ts AND s.signup_ts + INTERVAL 7 DAY
)
SELECT
  event,
  countDistinctIf(person_id, retained) AS did_retained,
  countDistinctIf(person_id, NOT retained) AS did_churned,
  did_retained * 1.0 / (SELECT countDistinct(person_id) FROM retained_d30) AS pct_retained_did,
  did_churned * 1.0 / (SELECT countDistinct(person_id) FROM signup_cohort
                         WHERE person_id NOT IN (SELECT person_id FROM retained_d30)) AS pct_churned_did,
  pct_retained_did / nullIf(pct_churned_did, 0) AS lift_ratio
FROM candidate_actions
GROUP BY event
HAVING did_retained + did_churned >= 50
ORDER BY lift_ratio DESC
LIMIT 20
```

Interpretation:
- `lift_ratio` > 2.0 and `pct_retained_did` > 60% → strong activation candidate
- Test 3-5 top candidates; choose the one that's BOTH predictive AND attainable in TTV window

### Recipe 2: Magic-number-N estimation

For an event (e.g., `Document Created`), find the threshold N at which retention asymptotes.

```sql
SELECT
  CASE
    WHEN n_docs = 0 THEN '0'
    WHEN n_docs = 1 THEN '1'
    WHEN n_docs = 2 THEN '2'
    WHEN n_docs BETWEEN 3 AND 5 THEN '3-5'
    WHEN n_docs BETWEEN 6 AND 10 THEN '6-10'
    ELSE '11+'
  END AS doc_bucket,
  count() AS users,
  avg(retained_d30) AS retention_rate
FROM (
  SELECT
    person_id,
    countIf(event = 'Document Created' AND timestamp <= signup_ts + INTERVAL 7 DAY) AS n_docs,
    -- 1/0 retention flag
    countIf(event = 'core_action' AND timestamp >= signup_ts + INTERVAL 30 DAY) > 0 AS retained_d30
  FROM events_with_signup_ts
  GROUP BY person_id, signup_ts
)
GROUP BY doc_bucket
ORDER BY doc_bucket
```

The bucket where retention jumps and asymptotes = your magic-number. E.g., "3 documents in 7 days" → 78% retention vs 12% at 0 docs.

### Recipe 3: Sean Ellis Test survey (validates aha moment)

```bash
# Field via Typeform (typeform skill)
# Trigger: users with 2+ sessions in last 14d (engaged but new enough to remember pre-product)

# Question 1 (the one):
# "How would you feel if you could no longer use [product]?"
# Options: Very disappointed / Somewhat disappointed / Not disappointed / N/A (no longer using)

# Question 2 (theming follow-up):
# "What's the primary benefit you receive from [product]?"  (free text)

# Question 3 (segmentation):
# "What type of person do you think would most benefit from [product]?" (free text)
```

Analysis:
- Score % "Very disappointed" / (total non-NA responses)
- ≥ 40% → PMF signal
- 25-40% → close to PMF; iterate
- < 25% → not yet PMF; product investment needed

Feed Q2 free-text responses to Claude for theming:
```python
themes = claude.summarize_themes(
    responses=q2_responses,
    n_themes=5,
    prompt="Extract distinct benefit themes; report frequency"
)
```

### Recipe 4: Activation rate measurement (PostHog cohort)

```sql
WITH signup_cohort AS (
  SELECT person_id, min(timestamp) AS signup_ts
  FROM events WHERE event = 'User Signed Up'
    AND timestamp >= now() - INTERVAL 60 DAY
    AND timestamp < now() - INTERVAL 14 DAY  -- exclude users not yet 14d old
  GROUP BY person_id
)
SELECT
  toStartOfWeek(signup_ts) AS signup_week,
  count() AS cohort_size,
  countIf(activated) AS activated,
  activated * 100.0 / cohort_size AS activation_rate_pct
FROM (
  SELECT
    s.person_id, s.signup_ts,
    exists(SELECT 1 FROM events e
           WHERE e.person_id = s.person_id
             AND e.event = '<activation_event_name>'
             AND e.timestamp BETWEEN s.signup_ts AND s.signup_ts + INTERVAL 14 DAY) AS activated
  FROM signup_cohort s
)
GROUP BY signup_week
ORDER BY signup_week DESC
```

### Recipe 5: TTV percentiles (p25/p50/p75)

```sql
SELECT
  quantile(0.25)(ttv_minutes) AS p25,
  quantile(0.5)(ttv_minutes) AS p50,
  quantile(0.75)(ttv_minutes) AS p75,
  quantile(0.95)(ttv_minutes) AS p95
FROM (
  SELECT
    person_id,
    dateDiff('minute',
      minIf(timestamp, event = 'User Signed Up'),
      minIf(timestamp, event = '<activation_event>')
    ) AS ttv_minutes
  FROM events
  WHERE event IN ('User Signed Up', '<activation_event>')
    AND timestamp >= now() - INTERVAL 30 DAY
  GROUP BY person_id
  HAVING ttv_minutes > 0
)
```

### Recipe 6: Slice activation by ICP segment

```sql
SELECT
  properties.icp_segment,
  countDistinct(person_id) AS cohort,
  countDistinctIf(person_id, activated_within_7d) AS activated,
  activated * 100.0 / cohort AS rate
FROM cohort_with_activation_flag
GROUP BY properties.icp_segment
ORDER BY rate DESC
```

ICPs with rate < 30% may indicate wrong-fit — exclude from paid acquisition.

### Recipe 7: Activation event-to-feature map (write spec to Notion)

```python
# Generate activation spec doc via notion-mcp
spec = {
    "Aha moment (qualitative)": "I can find anything in my docs in seconds",
    "Activation event (behavioral)": "search_used",
    "Magic number": "≥ 2 searches in first 7 days",
    "Activation window": "7 days post-signup",
    "Current activation rate": "31%",
    "Benchmark": "B2B SaaS avg 37.5%, BIC 60%+",
    "TTV p50": "2h 14m",
    "TTV p25": "8m",
    "TTV p75": "1d 6h",
    "Sean Ellis Test": "37% very disappointed (close to PMF)",
    "Constraint": "Search discoverability — only 41% of activated users found the search bar",
    "Top 3 experiments": [
        "Inline search prompt after first doc creation",
        "Onboarding step that demonstrates search",
        "Empty-state CTA pointing to search"
    ]
}
notion.create_page(parent_id=growth_db_id, properties=spec)
```

### Recipe 8: Validate activation event via inverse correlation

The chosen activation event should:
1. Predict retention (lift_ratio > 2.0)
2. Be ATTAINABLE in TTV window (p50 < window)
3. Be FREQUENT enough to measure (≥ 30% of cohort attempt it)
4. Be UPSTREAM of revenue (correlates with paid conversion)

```sql
SELECT
  activated AS act,
  countDistinct(person_id) AS users,
  countDistinctIf(person_id, paid_conversion) AS paid,
  paid * 1.0 / users AS paid_conversion_rate
FROM cohort_with_activation_and_revenue
GROUP BY activated
```

Activated users should have 3-5x the paid conversion rate of non-activated. If not, your activation event is downstream of value, not predictive.

## Examples

### Example 1: SaaS dashboard product

Cohort-diff results:
| Event | Day-30 retained pct | Day-30 churned pct | Lift |
|---|---|---|---|
| `dashboard_created` | 82% | 11% | 7.5x |
| `data_source_connected` | 91% | 18% | 5.1x |
| `dashboard_shared` | 71% | 5% | 14.2x |
| `report_scheduled` | 44% | 8% | 5.5x |

Best candidate: `data_source_connected` (highest pct_retained_did + attainable in TTV window).

Magic number test: 1 data source → 64% retention; 2 → 81%; 3+ → 87%. Magic number = 1.

Sean Ellis Test (n=240 engaged users): 43% very disappointed → PMF signal.

Activation rate: 28% → below B2B SaaS avg of 37.5%. Constraint: data-source connection is the choke point. TTV p50 = 22 minutes (above best-in-class 5-min).

Plan: reduce data-source-connection friction (OAuth presets, common-DB starter templates). Target TTV p50 < 10 min, activation rate > 40% within Q2.

### Example 2: Consumer note-taking app

Cohort-diff top events:
- `note_created` lift 2.1x
- `note_tagged` lift 4.8x
- `share_link_generated` lift 6.9x

But `share_link_generated` p50 TTV = 6 days (most users don't share that fast).

Choose `note_tagged` (lift good + p50 = 4 hours). Magic number = 3 tags.

Sean Ellis Test: 31% very disappointed → not yet PMF; iterate. Theme analysis: most "very disappointed" mention "search across all my notes" → product investment area.

## Edge cases / gotchas

- **Picking activation that's downstream of value, not upstream** — `purchase_completed` predicts retention because purchasers retain; it's not an activation event because it's outcome, not cause. Pick events that *cause* value-realization.
- **Survivorship bias** — cohort-diff trained on "users who lived to Day 30" inflates lift for any event correlated with being alive. Mitigate with full cohort + censoring (use Cox PH per `churn-prediction-modeling`).
- **Single-event activation in multi-jobs products** — a product serving 3 personas may have 3 activation events. Don't force one. Track persona-specific activation rates.
- **Aha moment ≠ activation event** — confused often. Aha is emotional ("I get it now"); activation is behavioral ("did event X N times"). Sean Ellis Test surfaces aha; cohort-diff surfaces activation.
- **TTV percentile spread > 100x** — p25 vs p75 spread > 100x means TTV distribution is bimodal; segment cohorts before optimizing.
- **Survey selection bias** — Sean Ellis Test only on engaged users (2+ sessions in 14d). Including dormant users skews "not disappointed" upward and breaks the PMF threshold.
- **Activation window timing** — too short (3d) penalizes complex products; too long (60d) conflates activation with retention. 7d for simple, 14d for moderate, 30d for enterprise/setup-heavy.
- **Changing activation event mid-quarter** — destroys historical trend comparability. Document changes; ideally re-baseline last 90d on new event.

## Sources

- Stackmatix — PLG onboarding & activation: https://www.stackmatix.com/blog/plg-onboarding-activation
- Reforge — Casey Winters on activation: https://www.reforge.com/blog/why-activation-is-the-most-important-metric
- Sean Ellis — The PMF survey: https://www.startup-marketing.com/the-startup-pyramid/
- Userpilot — Activation rate benchmarks 2024: https://userpilot.com/blog/product-led-growth-metrics/
- PostHog — Activation event tutorial: https://posthog.com/tutorials/activation-rate
- Amplitude — North Star activation: https://amplitude.com/explore/analytics/activation-rate
- Lenny's PLG Handbook (TTV): https://plghandbook.com/time-to-value/
- Appcues — PLG metrics: https://www.appcues.com/blog/product-led-growth-metrics
