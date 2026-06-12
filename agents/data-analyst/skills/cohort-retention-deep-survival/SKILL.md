<!--
lifelines: https://lifelines.readthedocs.io/
lifetimes (BG/NBD): https://github.com/CamDavidsonPilon/lifetimes
Companion: role.md → "Cohort retention playbook" + research-analyst sibling skill
-->

# Cohort retention — N-day, rolling, Kaplan-Meier, Cox PH, BG/NBD LTV

Build N-day + rolling retention tables in SQL, fit Kaplan-Meier survival curves with confidence intervals, run log-rank tests to compare cohorts, fit Cox PH for covariate-adjusted hazard, and compute LTV via BG/NBD + Gamma-Gamma. Includes Aha Moment identification.

## When to use

- "Compute Day-30 / Week-12 / Month-6 retention for the Jan cohort"
- "Compare two cohorts — is the new onboarding flow improving retention?"
- "Survival curve with confidence bands"
- "What behavior predicts long-term retention (Aha Moment)"
- "Compute customer LTV with uncertainty"
- "Hazard regression with covariates (plan, channel, country)"

Defer A/B test math to `ab-test-significance-mde-sequential`. Defer pure SQL warehouse patterns to `snowflake-bigquery-databricks-warehousing`. Defer segmentation to `customer-segmentation-rfm-behavioral-ml`.

## Setup

```bash
pip install lifelines lifetimes pandas numpy matplotlib scipy
```

No external auth. Warehouse credentials needed for source events; otherwise CSV/Parquet works.

## Concept cheat sheet

| Metric | Definition | Use for |
|---|---|---|
| **N-day retention** | % of cohort active on day N | Daily-use products (social, news, fitness) |
| **Rolling retention** | % active any day after day N | Weekly/monthly use (SaaS, finance, e-com) |
| **Unbounded retention** | active in [N, ∞) | Lifetime engagement |
| **Survival curve** | P(active at time t) | Continuous-time view + CIs |
| **Aha Moment** | behavior most correlated with retention | Onboarding optimization |
| **LTV** | E[total revenue | active] × P(active) | Pricing / CAC payback |

## Common recipes

### Recipe 1 — N-day retention table (SQL)

```sql
-- Snowflake / BigQuery / Databricks (adjust DATE_DIFF for dialect)
WITH cohorts AS (
  SELECT
    user_id,
    DATE_TRUNC('month', signup_at) AS cohort_month
  FROM users
),
events AS (
  SELECT user_id, event_at
  FROM product_events
  WHERE event_type IN ('login', 'core_action')      -- definition of "active"
),
joined AS (
  SELECT
    c.cohort_month,
    DATEDIFF('day', c.cohort_month, e.event_at) AS days_since_signup,
    c.user_id
  FROM cohorts c
  LEFT JOIN events e USING (user_id)
)
SELECT
  cohort_month,
  days_since_signup,
  COUNT(DISTINCT user_id) AS active_users
FROM joined
WHERE days_since_signup BETWEEN 0 AND 90
GROUP BY 1, 2
ORDER BY 1, 2;
```

Pivot to wide cohort table client-side:

```python
import pandas as pd
table = df.pivot(index="cohort_month", columns="days_since_signup", values="active_users")
retention_pct = table.div(table[0], axis=0) * 100      # % of Day-0 size
print(retention_pct.round(1))
```

### Recipe 2 — Rolling (unbounded) retention

```sql
WITH cohorts AS (
  SELECT user_id, DATE_TRUNC('week', signup_at) AS cohort_week
  FROM users
),
last_active AS (
  SELECT user_id, MAX(event_at) AS last_event_at
  FROM product_events GROUP BY 1
)
SELECT
  c.cohort_week,
  DATEDIFF('week', c.cohort_week, l.last_event_at) AS weeks_active,
  COUNT(*) AS users
FROM cohorts c
JOIN last_active l USING (user_id)
GROUP BY 1, 2;
```

A user counts as "retained at week W" if their last activity is on or after week W.

### Recipe 3 — Kaplan-Meier survival curve

```python
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt
import pandas as pd

# Per-user durations + event flag
# duration       = days from signup to last activity (or 'now' if still active)
# event_observed = 1 if user has CHURNED (no activity in last 28 days); 0 if censored
df = pd.read_sql("""
    SELECT
        user_id,
        DATEDIFF('day', signup_at, COALESCE(last_event_at, current_date)) AS duration,
        CASE WHEN last_event_at < CURRENT_DATE - INTERVAL '28 days' THEN 1 ELSE 0 END AS churned,
        plan_tier
    FROM users LEFT JOIN (
        SELECT user_id, MAX(event_at) AS last_event_at FROM product_events GROUP BY 1
    ) USING (user_id)
""", con)

kmf = KaplanMeierFitter()
kmf.fit(df["duration"], df["churned"], label="All users")
ax = kmf.plot_survival_function(ci_show=True)
ax.set_xlabel("Days since signup")
ax.set_ylabel("P(still active)")
plt.savefig("survival.png", dpi=150)

# Read off milestones
print("P(active at day 30):", kmf.survival_function_at_times([7, 14, 30, 60, 90]).round(3))
print("Median survival:", kmf.median_survival_time_)
print("Survival CI at 30 days:\n", kmf.confidence_interval_survival_function_.loc[30])
```

### Recipe 4 — Compare two cohorts (log-rank)

```python
from lifelines.statistics import logrank_test, multivariate_logrank_test

# Two cohorts
jan = df[df.cohort_month == "2025-01"]
feb = df[df.cohort_month == "2025-02"]

result = logrank_test(
    jan["duration"], feb["duration"],
    event_observed_A=jan["churned"], event_observed_B=feb["churned"],
)
print(f"Log-rank chi² = {result.test_statistic:.3f}, p = {result.p_value:.4f}")

# Many cohorts at once
multi = multivariate_logrank_test(df["duration"], df["cohort_month"], df["churned"])
print(multi.summary)
```

### Recipe 5 — Cox PH regression (covariate-adjusted hazard)

```python
from lifelines import CoxPHFitter

# Prepare covariates: tenure, plan_tier (one-hot), acquisition_channel
features = pd.get_dummies(df[["duration", "churned", "plan_tier", "acquisition_channel"]],
                          columns=["plan_tier", "acquisition_channel"], drop_first=True)

cph = CoxPHFitter(penalizer=0.01)
cph.fit(features, duration_col="duration", event_col="churned")
cph.print_summary()

# Hazard ratios
print("Premium vs Basic HR:", cph.hazard_ratios_["plan_tier_Premium"])
print("Concordance:", cph.concordance_index_)        # discriminative power

# Predict survival curves per user
cph.predict_survival_function(features.head(5))
```

Interpretation: `HR=0.5` → premium users have half the hazard (twice the retention).

### Recipe 6 — Retention curve health diagnosis

```python
import numpy as np

# Compute slope in the tail (days 30-60)
late = retention_pct.iloc[:, 30:60].mean(axis=0).values
slope_per_day = (late[-1] - late[0]) / (len(late) - 1)
floor = late[-1]

if floor < 5:
    diagnosis = "DYING — approaches zero. PMF problem. More acquisition won't fix."
elif slope_per_day > -0.05:
    diagnosis = f"HEALTHY — flattens at {floor:.1f}%."
else:
    diagnosis = f"DECLINING — still falling at {slope_per_day:.2f}%/day at day 60."
print(diagnosis)
```

### Recipe 7 — Aha Moment analysis

```python
from scipy.stats import chi2_contingency

# Did the user perform behavior X in their first 7 days?
df["retained_d30"] = (df["duration"] >= 30) & (df["churned"] == 0)

candidates = ["sent_message_w1", "invited_friend_w1", "completed_profile_w1", "used_feature_X_w1"]
results = []

for behavior in candidates:
    crosstab = pd.crosstab(df[behavior], df["retained_d30"])
    chi2, p, _, _ = chi2_contingency(crosstab)
    lift = (df[df[behavior] == True]["retained_d30"].mean()
            - df[df[behavior] == False]["retained_d30"].mean())
    results.append({"behavior": behavior, "lift_pp": lift*100, "chi2": chi2, "p": p})

results_df = pd.DataFrame(results).sort_values("lift_pp", ascending=False)
print(results_df)
# Top behavior with statistically significant lift = Aha candidate
```

**Validate causation**: A/B test the recommendation against a nudge group. Correlation alone doesn't prove the behavior *causes* retention — high-engagement users may simply do everything.

### Recipe 8 — Time-to-Value (median activation)

```python
# Days from signup to first "valuable" event
df_ttv = pd.read_sql("""
    SELECT
        u.user_id,
        DATEDIFF('day', u.signup_at, MIN(e.event_at)) AS days_to_first_action
    FROM users u
    JOIN product_events e USING (user_id)
    WHERE e.event_type = 'completed_first_project'
    GROUP BY 1
""", con)

print("Median TTV:", df_ttv["days_to_first_action"].median(), "days")
print("75th percentile:", df_ttv["days_to_first_action"].quantile(0.75))
```

### Recipe 9 — BG/NBD + Gamma-Gamma LTV

```python
from lifetimes import BetaGeoFitter, GammaGammaFitter
from lifetimes.utils import summary_data_from_transaction_data

# Convert transaction data to RFM-like summary
summary = summary_data_from_transaction_data(
    transactions, "user_id", "transaction_date", monetary_value_col="amount",
    observation_period_end="2026-06-09"
)
# Columns: frequency, recency, T, monetary_value

# BG/NBD: predict number of future transactions
bgf = BetaGeoFitter(penalizer_coef=0.001)
bgf.fit(summary["frequency"], summary["recency"], summary["T"])

# Probability user is alive
summary["p_alive"] = bgf.conditional_probability_alive(
    summary["frequency"], summary["recency"], summary["T"]
)

# Expected purchases in next 90 days
summary["pred_txn_90d"] = bgf.conditional_expected_number_of_purchases_up_to_time(
    90, summary["frequency"], summary["recency"], summary["T"]
)

# Gamma-Gamma: predict expected purchase value (uncorrelated with frequency)
returning = summary[summary["frequency"] > 0]
ggf = GammaGammaFitter(penalizer_coef=0.01)
ggf.fit(returning["frequency"], returning["monetary_value"])

# 12-month LTV
summary["ltv_12mo"] = ggf.customer_lifetime_value(
    bgf, summary["frequency"], summary["recency"], summary["T"], summary["monetary_value"],
    time=12, freq="M", discount_rate=0.01
)
```

### Recipe 10 — PostHog cohort fetch + survival

```python
import requests
import os

# Fetch a PostHog cohort
r = requests.get(
    f"https://app.posthog.com/api/projects/{os.environ['POSTHOG_PROJECT_ID']}/cohorts/42/persons/",
    headers={"Authorization": f"Bearer {os.environ['POSTHOG_API_KEY']}"},
)
persons = r.json()["results"]
user_ids = [p["distinct_ids"][0] for p in persons]

# Then join to warehouse for durations + churn flag and feed to lifelines as above.
```

## Example end-to-end

**Goal:** Diagnose retention health and find an Aha Moment for the Jan 2026 cohort.

1. Pull cohort + events from warehouse (Recipe 1 SQL).
2. Build N-day retention table; pivot wide; visualize as heatmap.
3. Diagnose curve health (Recipe 6) — output: "DECLINING".
4. Fit Kaplan-Meier (Recipe 3); save PNG.
5. Log-rank vs Dec 2025 cohort (Recipe 4): p=0.03 → cohorts differ.
6. Aha-moment scan (Recipe 7): "invited_friend_w1" has +18pp lift on D30 retention, p<0.001.
7. Cox PH (Recipe 5) confirms HR=0.42 for invited_friend even after controlling for plan + channel.
8. Recommend A/B test of in-app nudge for new users to "invite a friend in week 1".
9. Compose deliverable per role.md → "Cohort analysis report" template.

## Edge cases / gotchas

- **Right-censoring** — users active today haven't churned *yet*. Lifelines handles via `event_observed=0`. Dropping censored users is survivorship bias.
- **Definition of "active"** — opening the app? completing an action? minutes of usage? Document explicitly; results shift with the definition.
- **Cohort size variance** — small cohorts produce wide CI bands; exclude cohorts <100 users from comparisons or use Bayesian smoothing.
- **Aha causation vs correlation** — engaged users do *everything*. Validate via A/B test of an onboarding nudge before claiming causation.
- **Reverse causation in Aha analysis** — "users who used feature X retain better" may be because retainers stay long enough to discover X. Restrict to behaviors in week 1.
- **Daily vs weekly granularity for rolling retention** — daily-use products use daily; SaaS use weekly/monthly. Don't apply N-day to weekly products (looks catastrophic).
- **BG/NBD assumptions** — non-contractual setting; users churn silently. Doesn't fit subscription businesses; use survival models there.
- **CoxPH proportional hazards assumption** — test via `cph.check_assumptions(df)`; if violated, stratify or use time-varying covariates.
- **PostHog cohort caching** — cohorts API serves cached membership; for real-time use HogQL query endpoint.
- **PII** — when shipping user-level analysis, hash user IDs in intermediate files; never log raw PII outside the analysis sandbox.
- **Log-rank power** — needs sufficient events (churns) in both arms; with few churns, switch to permutation test.

## Sources

- [lifelines documentation](https://lifelines.readthedocs.io/)
- [lifelines Kaplan-Meier intro](https://lifelines.readthedocs.io/en/latest/Quickstart.html)
- [lifelines Cox PH](https://lifelines.readthedocs.io/en/latest/Survival%20Regression.html#cox-s-proportional-hazard-model)
- [lifetimes library (BG/NBD)](https://lifetimes.readthedocs.io/)
- [Andrew Chen — Aha moment](https://andrewchen.com/)
- [PostHog cohorts API](https://posthog.com/docs/api/cohorts)
- [Amplitude — Aha Moment guide](https://amplitude.com/blog/aha-moment)
- role.md → "Cohort retention playbook"
