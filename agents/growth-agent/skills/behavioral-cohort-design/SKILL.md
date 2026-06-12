<!--
Source: PostHog cohorts + Amplitude behavioral cohorts + Mixpanel cohort spec
-->
# Behavioral Cohort Design SKILL

> Define, build, and activate behavioral cohorts (multi-attribute, time-windowed). Static vs dynamic. PostHog, Amplitude, Mixpanel APIs + Hightouch activation. Foundation for every downstream growth action.

## When to use

Trigger phrases:
- "Define a cohort of users who..."
- "Behavioral segment"
- "Multi-attribute audience"
- "Time-windowed cohort"
- "Static vs dynamic cohort"
- "Sync cohort to [Klaviyo / Customer.io / HubSpot / Facebook]"

Pair: `cdp-segment-rudderstack-mparticle` (event source), `reverse-etl-hightouch-census-growth` (downstream activation), `pql-product-qualified-leads-framework`, `win-back-campaigns` (cohort-driven actions).

## Setup

```bash
export POSTHOG_PERSONAL_API_KEY="phx_..."
export AMPLITUDE_OAUTH_TOKEN="amp_..."
export MIXPANEL_API_KEY="mx_..."
export HIGHTOUCH_API_KEY="ht_..."
```

## Cohort design rules

```text
1. Single-attribute cohorts are vanity ("Users from organic search")
2. Multi-attribute cohorts are actionable ("Users from organic + signed up Q1 + Pro plan + 3+ active days last week")
3. Always time-window — events without time bound are meaningless
4. Define dynamic vs static at creation
5. Document purpose + intended action per cohort
```

## Cohort taxonomy

| Type | Example | When to use |
|---|---|---|
| **Static** | Signups week of Mar 6, 2026 | Historical analysis; retention |
| **Dynamic** | Users active in last 7 days | Ongoing campaigns; real-time |
| **Acquisition-based** | UTM source = google + medium = paid | Channel quality analysis |
| **Behavioral** | Used premium feature ≥ 2x in last 14 days | PQL handoff, upgrade prompt |
| **Lifecycle stage** | Signed up 30d ago + not activated | Win-back campaigns |
| **Firmographic** | Company size 100-500 + industry SaaS | ICP segmentation |
| **Predictive** | Churn risk > 60% per Cox PH | At-risk handoff (see `churn-prediction-modeling`) |
| **Multi-event sequence** | Did A → then B within 7d | Funnel analysis |

## Common recipes

### Recipe 1: PostHog dynamic cohort (HogQL)

```bash
mcp tool posthog.cohorts_create \
  --name "Power Users + Approaching Limit" \
  --is_static false \
  --filters '{
    "type": "AND",
    "conditions": [
      {
        "type": "event",
        "event": "core_action",
        "operator": ">=",
        "value": 10,
        "window_days": 14
      },
      {
        "type": "property",
        "property": "usage_pct",
        "operator": "gte",
        "value": 0.80
      },
      {
        "type": "event_not",
        "event": "Subscription Started",
        "window_days": null  // never
      }
    ]
  }'
```

### Recipe 2: Amplitude behavioral cohort

```javascript
await amplitude.create_cohort({
  name: "Activated + High Frequency + Multi-Seat",
  definition: {
    type: "AND",
    conditions: [
      {event: "activation_event", count: ">=", value: 1, time_window: "first_7_days_after_signup"},
      {event: "session_started", count: ">=", value: 5, time_window: "last_14_days"},
      {user_property: "team_size", operator: "gte", value: 3}
    ]
  },
  is_dynamic: true
});
```

### Recipe 3: Mixpanel cohort definition

```bash
curl -X POST "https://mixpanel.com/api/2.0/cohort/create" \
  -u "$MIXPANEL_API_KEY:" \
  -d '{
    "project_id": "...",
    "name": "Win-back candidates",
    "behavioral_filters": [
      {
        "event": "Session Started",
        "operator": "<",
        "value": 1,
        "window": {"days": 30}
      },
      {
        "event": "Subscription Started",
        "operator": ">=",
        "value": 1,
        "window": "ever"
      }
    ]
  }'
```

### Recipe 4: Static cohort (point-in-time snapshot)

```sql
-- Snapshot, then freeze
INSERT INTO cohorts (cohort_name, user_id, created_at)
SELECT
  'Q1 2026 Signups',
  user_id,
  now()
FROM users
WHERE signup_date BETWEEN '2026-01-01' AND '2026-03-31'
  AND signup_source = 'organic'
```

Static = doesn't change. Useful for cohort retention curves.

### Recipe 5: Multi-event sequence cohort

```sql
-- Users who did A → then B within 7 days
SELECT DISTINCT a.person_id
FROM events a
JOIN events b ON b.person_id = a.person_id
WHERE a.event = 'Premium Feature Attempted'
  AND b.event = 'Subscription Started'
  AND b.timestamp BETWEEN a.timestamp AND a.timestamp + INTERVAL 7 DAY
```

PostHog HogQL handles this in cohort builder; Amplitude has "Cohorts > Sequence".

### Recipe 6: Negative event cohort

```text
"Users who signed up but did NOT activate within 14 days"

PostHog:
  - Event: User Signed Up >= 14 days ago
  - AND Event Not: activation_event in 14 days after signup

Amplitude:
  Same; supports "did not" predicate
```

### Recipe 7: Cohort with firmographic enrichment

```python
# 1. Behavioral cohort in PostHog/Amplitude
# 2. Sync to warehouse via reverse-PostHog (or just query PostHog API)
# 3. Join with Clearbit/Apollo firmographics
# 4. Re-filter by ICP fit

enriched = pd.merge(
    cohort_users,
    firmographics,
    on='email'
)
icp_fit = enriched[
    (enriched.employees >= 50) & (enriched.employees <= 500) &
    (enriched.industry.isin(['SaaS', 'Fintech', 'Marketing']))
]
```

### Recipe 8: Tier the cohort by score

```sql
-- Quintile-tier the cohort by PQL score
SELECT
  user_id,
  pql_score,
  NTILE(5) OVER (ORDER BY pql_score DESC) AS pql_quintile,
  CASE WHEN pql_quintile = 1 THEN 'critical'
       WHEN pql_quintile = 2 THEN 'high'
       WHEN pql_quintile = 3 THEN 'medium'
       ELSE 'low' END AS tier
FROM cohort_pql_high
```

Different tier = different downstream action (Slack alert vs in-app vs email).

### Recipe 9: Activate cohort to downstream tool

```text
Via Hightouch:
  PostHog cohort export → warehouse view → Hightouch model → destination

Via Customer.io direct:
  Customer.io supports its own segment definitions; create cohort within CIO.

Via Klaviyo:
  Hightouch sync → Klaviyo list, OR
  Klaviyo's own segment definitions

Via Intercom:
  Sync user attributes → Intercom segments based on attributes
```

### Recipe 10: Cohort intersection / union

```sql
-- Users in BOTH cohort A AND cohort B (intersection)
SELECT a.user_id
FROM cohort_a a
INNER JOIN cohort_b b ON a.user_id = b.user_id

-- Users in A OR B (union)
SELECT user_id FROM cohort_a
UNION
SELECT user_id FROM cohort_b

-- A NOT in B (exclusion)
SELECT user_id FROM cohort_a
WHERE user_id NOT IN (SELECT user_id FROM cohort_b)
```

### Recipe 11: Cohort lifecycle (auto-archive)

```text
Dynamic cohorts can grow infinitely. Strategies:

1. Cap at 90 days: members who don't qualify within 90d are removed
2. Auto-archive after action: once user gets the message, remove from cohort
3. Cool-down: re-include same user only after N days
4. Suppression list: never include unsubscribed
```

### Recipe 12: Cohort doc template (Notion)

```markdown
# Cohort: Power Users Approaching Limit

**Purpose:** Trigger upgrade prompt for users likely to convert.

**Definition (PostHog cohort_id: 12345):**
- AND
  - Did `core_action` ≥ 10 times in last 14 days
  - `usage_pct` ≥ 0.80
  - Did NOT `Subscription Started`

**Type:** Dynamic.

**Refresh:** Real-time.

**Size:** ~340 users at any moment (varies daily).

**Downstream actions:**
- Hightouch sync to Customer.io segment "approaching_limit" (every 15 min)
- Customer.io campaign "Upgrade prompt" auto-triggers
- Slack alert to AE if account ARR > $5K (Recipe 9 in PQL skill)

**Owner:** Growth lead.

**Review cadence:** Weekly metrics check.

**Success metric:** Upgrade rate within 14 days of entering cohort.
```

## Examples

### Example 1: PQL Cohort

Definition:
- `usage_pct >= 0.8` (limit-proximity signal)
- AND ≥ 5 `Premium Feature Attempted` in 30d (depth)
- AND ≥ 3 active team members in 7d (team)
- AND NOT `Subscription Started`

Action: per `pql-product-qualified-leads-framework` skill — sync to CRM + Slack AE.

### Example 2: Win-back cohort

Definition:
- Last `session_started` was 30-90 days ago
- AND lifetime `core_action` count ≥ 5 (was activated; not pre-PMF dropout)
- AND email_engagement_status != 'unsubscribed'

Action: per `win-back-campaigns` skill — Customer.io sequence.

### Example 3: Activated power-users for advocate program

Definition:
- Lifetime `core_action` ≥ 30
- AND NPS score ≥ 9 (promoter)
- AND `Invite Sent` ≥ 2 (already advocating naturally)

Action: ship advocate program invitation; tracked via `referral-program-referralcandy-friendbuy-growsurf`.

## Edge cases / gotchas

- **Cohort drift over time** — definition unchanged but population shifts (product features change → users behave differently). Re-validate quarterly.
- **Dynamic cohort size explosion** — too-loose definition includes everyone; useless. Tighten until size is actionable.
- **Time window too short** — "active last 24h" misses weekly users; too long → cohort is stale.
- **Cohort intersection complexity** — A ∩ B ∩ C ∩ NOT D = small noisy set; verify size > 30 before acting.
- **Property-based filters and event-based filters confused** — "Users with plan=Pro" is property; "Users who upgraded" is event. Use the right one.
- **Cohort vs segment terminology** — Amplitude says "cohort"; Mixpanel says "cohort"; Segment says "audience"; CIO says "segment". All mean similar things.
- **Privacy + consent state** — EU users without consent can't be cohorted by behavior; verify consent before activation.
- **Suppression list** — always respect global unsub / opt-out; suppress before sync.
- **Cohort definition versioning** — changing definition mid-campaign distorts metrics; version cohorts (`v1`, `v2`) when updating.
- **Sync latency for cohorts** — reverse-ETL is not real-time; for time-sensitive cohorts (lapsed-cart 1h), use event-triggered campaigns instead.
- **Anonymous user inclusion** — cohorts default to identified; anonymous users invisible. Identify ASAP per CDP skill.
- **Cohort cost in vendor pricing** — large cohorts = MTU cost in destination. Filter tightly.

## Sources

- PostHog cohorts: https://posthog.com/docs/data/cohorts
- Amplitude behavioral cohorts: https://amplitude.com/explore/analytics/cohort-retention-analysis
- Mixpanel cohorts: https://docs.mixpanel.com/docs/users-cohorts/cohorts
- Hightouch cohort activation patterns: https://hightouch.com/blog/data-activation
- Customer.io segments: https://customer.io/docs/journeys/segments/
- Klaviyo segments: https://help.klaviyo.com/hc/en-us/categories/360000058311-Segments-Lists
- Intercom segments: https://www.intercom.com/help/en/articles/152-segment-your-users
- ProductLed PLG metrics (cohort): https://www.productled.org/foundations/product-led-growth-metrics
