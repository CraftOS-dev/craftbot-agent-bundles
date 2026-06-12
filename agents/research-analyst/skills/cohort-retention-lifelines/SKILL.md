<!--
Source: https://lifelines.readthedocs.io/ (Kaplan-Meier survival analysis)
PostHog cohorts API: https://posthog.com/docs/api/cohorts
MCPs: posthog-mcp (already enabled), postgresql-mcp (raw events)
Companion playbook: role.md → "Cohort analysis playbook"
-->

# Cohort retention with PostHog + lifelines

End-to-end pipeline for cohort retention analysis: pull cohorts from PostHog (or raw events from PostgreSQL), build N-day and rolling retention tables, fit Kaplan-Meier survival curves with confidence intervals, identify the activation ("Aha") metric, and ship a deliverable that follows the role.md cohort analysis playbook.

## When to use this skill

- Acquisition cohort analysis (sign-up week / month groupings, N-day retention)
- Rolling retention for weekly / monthly-use products (vs N-day for daily-use)
- Survival analysis with confidence bands (lifelines Kaplan-Meier)
- Activation analysis — identifying the behavior that predicts long-term retention
- Comparing two cohorts statistically (log-rank test for survival-curve equality)
- Detecting product-market-fit health: does retention asymptote at a positive floor, or does it slope toward zero?

## When NOT to use

- Aggregate DAU / MAU only (no per-user data) → not a cohort analysis; use a simpler time-series
- Anonymized counts only → can't fit survival curves; recommend the user supply event-level data
- Real-time / streaming retention → use PostHog dashboards instead of a one-shot Python pipeline

## Setup

```bash
# Behavioral analytics platform
export POSTHOG_API_KEY="phc_..."
export POSTHOG_PROJECT_ID="123"
# OR raw events
export DATABASE_URL="postgresql://..."

# Statistical tooling
pip install lifelines pandas numpy matplotlib
```

The `posthog-mcp` and `postgresql-mcp` are already in `agent.yaml`. lifelines runs via `cli-anything`.

## Core concepts (recap from role.md)

- **N-day retention:** "what % of Day-0 sign-ups are active on Day N?" Used for daily-use products.
- **Rolling retention:** "what % of cohort X is active in week Y *or any week after*?" Used for weekly / monthly-use products.
- **Survival curve:** P(user is still active at time t) — fitted with Kaplan-Meier, includes a confidence band.
- **Activation behavior:** the action correlated with high 30/90-day retention. Examples: Facebook "7 friends in 10 days", Slack "2,000 team messages", Twitter "follow 30 users".

## Common recipes

### Recipe 1 — Pull a cohort from PostHog

```bash
# List existing cohorts
curl -H "Authorization: Bearer $POSTHOG_API_KEY" \
  "https://app.posthog.com/api/projects/$POSTHOG_PROJECT_ID/cohorts/"

# Fetch persons in cohort 42
curl -H "Authorization: Bearer $POSTHOG_API_KEY" \
  "https://app.posthog.com/api/projects/$POSTHOG_PROJECT_ID/cohorts/42/persons/"

# Or create a new cohort via HogQL
curl -X POST -H "Authorization: Bearer $POSTHOG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"signed_up_jan_2025","groups":[{"properties":[{"key":"signup_date","value":"2025-01","operator":"icontains"}]}]}' \
  "https://app.posthog.com/api/projects/$POSTHOG_PROJECT_ID/cohorts/"
```

### Recipe 2 — Build the N-day retention table

```python
import pandas as pd

# events: per-row event_user_id, signup_date, event_date
df = pd.read_sql("""
  SELECT
    u.user_id,
    DATE_TRUNC('month', u.signup_at) AS cohort_month,
    DATE_PART('day', e.event_at - u.signup_at)::int AS days_since_signup
  FROM events e JOIN users u USING (user_id)
  WHERE e.event_at <= u.signup_at + INTERVAL '90 days'
""", con=engine)

# Pivot: cohort × N-day → unique users active at day N
table = (df.groupby(["cohort_month", "days_since_signup"])["user_id"]
           .nunique()
           .reset_index()
           .pivot(index="cohort_month", columns="days_since_signup", values="user_id"))

# Convert to % retained vs Day 0 (cohort size)
retention_pct = table.div(table[0], axis=0) * 100
```

Output matches the role.md playbook's cohort retention table format.

### Recipe 3 — Kaplan-Meier survival curve

```python
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt

# Per-user durations + event flag
# duration = days from signup to last activity (or now if still active)
# event_observed = 1 if churned (no activity in last 28 days), 0 if censored
df_users = pd.read_sql("""
  SELECT user_id,
         DATE_PART('day', last_activity_at - signup_at)::int AS duration,
         CASE WHEN last_activity_at < NOW() - INTERVAL '28 days' THEN 1 ELSE 0 END AS churned
  FROM users
""", con=engine)

kmf = KaplanMeierFitter()
kmf.fit(durations=df_users.duration, event_observed=df_users.churned, label="All users")
kmf.plot_survival_function(ci_show=True)
plt.title("User Survival Curve (Kaplan-Meier)")
plt.xlabel("Days since signup")
plt.ylabel("P(still active)")
plt.savefig("survival_curve.png", dpi=150)

# Read off key milestones
print("P(active at day 30):", kmf.survival_function_at_times(30).values[0])
print("Median survival:    ", kmf.median_survival_time_)
```

### Recipe 4 — Compare two cohorts (log-rank test)

```python
from lifelines.statistics import logrank_test

# Did the Feb cohort retain better than the Jan cohort (significance test)?
jan = df_users[df_users.cohort_month == "2025-01"]
feb = df_users[df_users.cohort_month == "2025-02"]

result = logrank_test(
    jan.duration, feb.duration,
    event_observed_A=jan.churned, event_observed_B=feb.churned
)
print(f"p-value: {result.p_value:.4f}")  # < 0.05 → curves differ significantly
```

### Recipe 5 — Activation ("Aha Moment") analysis

```python
# Define: a user is "retained" if active on day 30
df_users["retained_d30"] = (df_users["duration"] >= 30) & (df_users["churned"] == 0)

# For each candidate first-week behavior, compute the retention lift
candidates = ["sent_first_message", "invited_teammate", "completed_onboarding", "used_feature_X"]
for behavior in candidates:
    behavior_users = df_users[df_users[behavior] == True]
    no_behavior   = df_users[df_users[behavior] == False]
    lift = behavior_users.retained_d30.mean() - no_behavior.retained_d30.mean()
    print(f"{behavior:30s}  lift={lift:+.1%}   p={ttest(behavior_users.retained_d30, no_behavior.retained_d30).pvalue:.3g}")
```

The behavior with the largest *and* statistically significant retention lift is the candidate activation metric. Validate by checking that users who did the behavior in week 1 but *not* week 0 also retain (rules out reverse causation).

### Recipe 6 — Retention curve health diagnosis

```python
# Tail behavior: does retention flatten or slope toward zero?
late_curve = retention_pct.iloc[:, 30:60].mean(axis=0)  # avg across cohorts, days 30-60
slope = (late_curve.iloc[-1] - late_curve.iloc[0]) / (late_curve.index[-1] - late_curve.index[0])

if late_curve.iloc[-1] < 5:
    diagnosis = "DYING — approaching zero. Product-market fit problem; more acquisition won't fix."
elif slope > -0.1:
    diagnosis = "HEALTHY — flattens asymptotically at {:.1f}%.".format(late_curve.iloc[-1])
else:
    diagnosis = "DECLINING — still sloping at {:.2%}/day; watch tail.".format(slope/100)
```

### Recipe 7 — Deliverable assembly

Use the playbook structure from `role.md → Cohort analysis playbook → Cohort deliverable`:

```
1. Cohort retention table (Recipe 2 output)
2. Retention curve shape diagnosis (Recipe 6 output)
3. Kaplan-Meier survival plot with CI (Recipe 3 output → PNG)
4. Drop-off points (where the curve has biggest slope changes — np.diff on retention_pct)
5. Activation metric hypothesis + lift table (Recipe 5 output)
6. Product recommendations ranked by expected retention impact
```

Then hand off to `data-storytelling-plotly-altair` for the visual layer and `pandoc-branded-deliverables` for the DOCX.

## Edge cases

- **Right-censoring:** users active today haven't churned *yet*. Lifelines handles this correctly via the `event_observed` flag (0 = censored, 1 = observed event). Do **not** drop censored users — that's survivorship bias.
- **Cohort size variance:** small cohorts have wide CI bands. Set `min_cohort_size=100` and exclude smaller cohorts from comparison tables.
- **Activity threshold sensitivity:** the definition of "active" (logged in? completed action? minutes of use?) shifts the curve. State the definition explicitly in the deliverable.
- **Aha-moment causation:** correlation between behavior B and retention does NOT prove causation. A/B test the recommendation before declaring "Behavior B causes retention" — use `lifelines` to power-analyze the test.
- **Selection bias:** "users who did X in week 1" is partially self-selecting on engagement. Cross-check by analyzing within-engagement-tier (top quintile of engagement only).
- **Rolling retention edge case:** for monthly-use apps, rolling retention is the right metric; N-day will look catastrophic and mislead.
- **PostHog cohort caching:** the cohorts endpoint serves cached membership lists; for real-time freshness, use HogQL query endpoint.
- **PRIVACY:** when pulling user-level data, never log PII outside the analysis sandbox. Hash user IDs in any intermediate file.

## Sources

- lifelines (Kaplan-Meier, log-rank): https://lifelines.readthedocs.io/
- PostHog cohorts API: https://posthog.com/docs/api/cohorts
- PostHog HogQL: https://posthog.com/docs/hogql
- Classic activation references: Andrew Chen, "the only metric that matters" — https://andrewchen.com/
- role.md → Cohort analysis playbook (this bundle's authoritative spec)

## Related skills

- `kpi-dashboard-design` (existing) — for surfacing the activation metric on dashboards
- `data-storytelling-plotly-altair` — for the survival-curve visual
- `pandoc-branded-deliverables` — for the report wrap
