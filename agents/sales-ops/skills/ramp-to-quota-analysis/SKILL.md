<!--
Source: https://www.gong.io/blog/sales-ramp/ + https://www.saleshood.com/blog/sales-ramp/ + https://www.mindtickle.com/
Ramp-to-quota analysis — new-hire cohort + Mindtickle/Lessonly training (June 2026 SOTA).
-->
# Ramp-to-Quota Analysis — Cohort + Training Correlation — SKILL

New-hire ramp tracking. Weeks 0-2 product training (**Mindtickle** / **Lessonly** / Brainshark), weeks 3-6 shadowing, weeks 7-12 ramp quota (50% target), full quota by month 4-6. Time from start → first $X closed; ongoing attainment % per quarter post-ramp. Compare cohorts (hire month, experience tier).

## When to use

- **Quarterly ramp-to-quota review** — how is the latest cohort performing?
- **Identify slow rampers** — cohort outliers below median curve.
- **Training completion correlation** — does Mindtickle completion predict ramp speed?
- **Onboarding playbook revision** — what works for fast rampers?
- **New-hire forecast** — when does this AE hit full quota?
- **Trigger phrases**: "ramp curve", "new hire cohort", "ramp-to-quota", "Mindtickle completion", "ramp tier", "first close days".

Do NOT use this skill for: **rep performance dashboards** (use `rep-performance-dashboards`); **commission ramp tier** (use `commission-spiff-quotapath-captivateiq`); **win/loss analysis** (use `win-loss-reporting-at-scale`); **forecasting** (use `forecasting-clari-boostup-aviso`).

## Setup

```bash
# CRM via api-gateway
export MATON_API_KEY="<key>"

# Mindtickle
export MINDTICKLE_TOKEN="<token>"
export MINDTICKLE_BASE="https://api.mindtickle.com/v1"

# Lessonly (now Seismic Learning)
export LESSONLY_TOKEN="<token>"
export LESSONLY_BASE="https://learn.lessonly.com/api/v2"

# Warehouse for cohort analysis
export PG_URI="postgresql://..."

# Python deps
pip install pandas matplotlib numpy
```

Required:
- CRM (Salesforce/HubSpot) with start_date on User
- Training tool API access (Mindtickle/Lessonly)
- Quota source-of-truth per AE per quarter

## Common recipes

### Recipe 1: Ramp framework (canonical)

```yaml
week_0_2_product_training:
  expectation: complete Mindtickle / Lessonly product modules
  measure: % course completion
  target: 100% by end of week 2

week_3_6_shadowing:
  expectation: shadow 5 senior AE calls, 3 manager calls
  measure: calls logged + post-call reflection note
  target: 8 total shadows

week_7_12_ramp_quota:
  expectation: 50% of full quota per quarter
  measure: closed-won amount / ramp quota
  target: > 80% of ramp quota attainment

month_4_6_full_quota:
  expectation: 80-100% of full quota
  measure: closed-won amount / full quota
  target: > 70% of full quota by month 6

cohort_definitions:
  experience_tier:
    - junior: 0-2 yr B2B sales
    - mid: 3-5 yr
    - senior: 6+ yr
  segment:
    - enterprise
    - mid_market
    - smb
```

### Recipe 2: Pull rep cohort data

```bash
# Salesforce
sf data query --target-org prod --query \
  "SELECT Id, Name, Email, Start_Date__c, Segment__c, \
          Prior_Years_Experience__c, Manager.Name, Title \
   FROM User \
   WHERE Profile.Name LIKE '%Account Executive%' \
     AND Start_Date__c >= 2024-01-01 \
   ORDER BY Start_Date__c"
```

### Recipe 3: Compute days-to-first-close

```python
import pandas as pd

reps = pd.read_csv("reps_with_start_date.csv")
deals = pd.read_csv("closed_won_deals.csv")  # columns: deal_id, owner_id, close_date, amount

# First closed-won per rep
first_close = deals.sort_values("close_date").groupby("owner_id").first().reset_index()
first_close = first_close[["owner_id","close_date","amount"]].rename(
    columns={"close_date":"first_close_date","amount":"first_close_amount"})

reps = reps.merge(first_close, left_on="id", right_on="owner_id", how="left")
reps["days_to_first_close"] = (pd.to_datetime(reps["first_close_date"]) -
                                pd.to_datetime(reps["Start_Date__c"])).dt.days

# Cohort by hire month
reps["hire_cohort"] = pd.to_datetime(reps["Start_Date__c"]).dt.to_period("M")

cohort_summary = reps.groupby("hire_cohort").agg(
    n_reps=("id", "count"),
    median_days_to_first_close=("days_to_first_close", "median"),
    p25=("days_to_first_close", lambda s: s.quantile(0.25)),
    p75=("days_to_first_close", lambda s: s.quantile(0.75))
).reset_index()
print(cohort_summary)
```

### Recipe 4: Monthly attainment curve

```python
import pandas as pd

# For each rep + month_offset_from_start: % of quota attained
records = []
for _, rep in reps.iterrows():
    start = pd.to_datetime(rep["Start_Date__c"])
    monthly_quota = rep["Full_Quota__c"] / 12  # simplified
    rep_deals = deals[deals["owner_id"] == rep["id"]]
    for m in range(1, 19):  # 18 months tracking
        m_start = start + pd.DateOffset(months=m-1)
        m_end = start + pd.DateOffset(months=m)
        in_month = rep_deals[(pd.to_datetime(rep_deals["close_date"]) >= m_start) &
                             (pd.to_datetime(rep_deals["close_date"]) < m_end)]
        records.append({
            "rep_id": rep["id"],
            "experience_tier": rep["Prior_Years_Experience__c"],
            "segment": rep["Segment__c"],
            "month_offset": m,
            "attainment_pct": min(100, 100 * in_month["amount"].sum() / monthly_quota)
        })

attainment_df = pd.DataFrame(records)

# Median curve overall
median_curve = attainment_df.groupby("month_offset")["attainment_pct"].median()
# Per-tier curves
per_tier = attainment_df.groupby(["experience_tier","month_offset"])["attainment_pct"].median().reset_index()
```

### Recipe 5: Plot ramp curve

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))
for tier in ["junior","mid","senior"]:
    sub = per_tier[per_tier["experience_tier"] == tier]
    ax.plot(sub["month_offset"], sub["attainment_pct"], marker="o", label=tier.capitalize())

ax.axhline(y=80, color="gray", linestyle="--", label="Full quota target")
ax.axhline(y=50, color="orange", linestyle="--", label="Ramp quota (months 3-6)")
ax.set_xlabel("Months from start")
ax.set_ylabel("Median % of full quota attained")
ax.set_title("Ramp-to-Quota by Experience Tier")
ax.set_ylim(0, 110)
ax.set_xticks(range(1, 19))
ax.legend(loc="lower right")
plt.tight_layout()
plt.savefig("ramp_curve.png", dpi=144)
```

### Recipe 6: Mindtickle completion pull

```bash
curl "$MINDTICKLE_BASE/users/learning-progress" \
  -H "Authorization: Bearer $MINDTICKLE_TOKEN" \
  -G --data-urlencode "user_emails=alice@co.com,bob@co.com" \
  | jq '.data[] | {user_email, courses_assigned, courses_completed, completion_pct, last_active_date}'
```

### Recipe 7: Training completion vs ramp correlation

```python
# Cross-reference Mindtickle completion with attainment
training = pd.read_csv("mindtickle_completion.csv")
# columns: user_email, courses_completed_pct, days_to_complete

ramp_with_training = reps.merge(training, left_on="Email", right_on="user_email", how="left")
ramp_with_training["fast_ramper"] = ramp_with_training["days_to_first_close"] < 45

# Correlation
corr = ramp_with_training[["courses_completed_pct","days_to_first_close"]].corr().iloc[0,1]
print(f"Correlation: completion% vs days_to_first_close = {corr:.3f}")

# Cohort: fast rampers had X% completion by week 2
fast = ramp_with_training[ramp_with_training["fast_ramper"] == True]
slow = ramp_with_training[ramp_with_training["fast_ramper"] == False]
print(f"Fast rampers median Mindtickle completion: {fast['courses_completed_pct'].median()}%")
print(f"Slow rampers median Mindtickle completion: {slow['courses_completed_pct'].median()}%")
```

### Recipe 8: Identify slow rampers (intervention)

```python
# Cohort outliers — > 1.5x median days-to-first-close
median_days = reps["days_to_first_close"].median()
threshold = median_days * 1.5

slow = reps[reps["days_to_first_close"] > threshold]
print(f"Slow rampers (> {threshold:.0f} days to first close): {len(slow)}")
for _, r in slow.iterrows():
    print(f"- {r['Name']} ({r['Email']}) — {r['days_to_first_close']:.0f} days, manager {r['Manager.Name']}")
```

### Recipe 9: Quarterly cohort comparison

```sql
-- Compare Q3 2025 hires vs Q3 2024 hires (same role + segment)
WITH cohorts AS (
  SELECT
    DATE_TRUNC('quarter', start_date) AS hire_quarter,
    user_id,
    full_quota
  FROM dim_users
  WHERE role = 'AE' AND segment = 'enterprise'
    AND start_date >= '2024-07-01'
),
ramp_metrics AS (
  SELECT
    c.hire_quarter,
    c.user_id,
    MIN(o.close_date) - MIN(u.start_date) AS days_to_first_close,
    SUM(CASE WHEN o.close_date BETWEEN c.start_date AND c.start_date + INTERVAL '6 months'
             THEN o.amount ELSE 0 END) AS month_1_6_won,
    c.full_quota
  FROM cohorts c
  JOIN dim_users u USING (user_id)
  LEFT JOIN fct_opportunities o ON o.owner_id = c.user_id AND o.is_won = TRUE
  GROUP BY 1, 2, c.full_quota
)
SELECT
  hire_quarter,
  COUNT(*) AS n_reps,
  ROUND(AVG(days_to_first_close), 0) AS avg_days_first_close,
  ROUND(AVG(month_1_6_won / NULLIF(full_quota/2, 0)), 2) AS avg_6m_attainment_vs_half_quota
FROM ramp_metrics
GROUP BY 1
ORDER BY 1 DESC;
```

### Recipe 10: Forecast new-hire trajectory

```python
# Given a new AE start_date + experience_tier, project quarter-by-quarter attainment
def project_attainment(start_date, experience_tier, segment):
    """Returns projected % of full quota for next 6 quarters."""
    # Use historical cohort median for similar profile
    similar = ramp_with_training[
        (ramp_with_training["Prior_Years_Experience__c"] == experience_tier) &
        (ramp_with_training["Segment__c"] == segment)
    ]
    projection = []
    for q in range(1, 7):
        month_window = range((q-1)*3 + 1, q*3 + 1)
        attainment_in_q = attainment_df[
            (attainment_df["month_offset"].isin(month_window)) &
            (attainment_df["rep_id"].isin(similar["id"]))
        ]
        proj_q_attainment = attainment_in_q["attainment_pct"].median()
        projection.append({"quarter_from_start": q, "projected_attainment_pct": proj_q_attainment})
    return projection

print(project_attainment("2026-06-15", "junior", "mid_market"))
```

### Recipe 11: Notion dashboard render

```python
import requests, os

# Per-cohort summary doc in notion
cohort_data = cohort_summary.to_dict("records")
for c in cohort_data:
    requests.post("https://api.notion.com/v1/pages",
                  headers={"Authorization": f"Bearer {os.environ['NOTION_TOKEN']}",
                           "Notion-Version": "2022-06-28"},
                  json={"parent": {"database_id": os.environ['RAMP_COHORTS_DB']},
                        "properties": {
                          "Cohort": {"title": [{"text": {"content": str(c["hire_cohort"])}}]},
                          "Reps": {"number": c["n_reps"]},
                          "Median Days to First Close": {"number": c["median_days_to_first_close"]},
                          "P25": {"number": c["p25"]},
                          "P75": {"number": c["p75"]}
                        }})
```

### Recipe 12: Slack weekly ramp digest

```python
# Weekly Monday: new hire updates, slow ramper alerts
# For AEs in months 1-6: progress vs cohort median

msg = "Ramp digest — week of {date}:\n\n"
new_hires_in_ramp = reps[(pd.Timestamp.now() - pd.to_datetime(reps["Start_Date__c"])).dt.days <= 180]
for _, rep in new_hires_in_ramp.iterrows():
    months_in = ((pd.Timestamp.now() - pd.to_datetime(rep["Start_Date__c"])).days // 30) + 1
    expected_pct = median_curve.get(months_in, 0)
    actual_pct = attainment_df[(attainment_df["rep_id"]==rep["id"]) &
                                (attainment_df["month_offset"]==months_in)]["attainment_pct"].mean() or 0
    delta = actual_pct - expected_pct
    status = "✓" if delta >= -10 else "⚠"
    msg += f"{status} {rep['Name']} (M{months_in}): {actual_pct:.0f}% vs cohort median {expected_pct:.0f}%\n"

requests.post("https://slack.com/api/chat.postMessage",
              headers={"Authorization": f"Bearer {os.environ['SLACK_TOKEN']}"},
              json={"channel": "#sales-leadership", "text": msg})
```

## Examples

### Example 1: Quarterly ramp review

**Goal:** End of Q3 — how is the Q1 hiring cohort tracking?

**Steps:**
1. Recipe 2 — pull all AE start dates.
2. Recipe 3 — compute days-to-first-close per rep.
3. Recipe 4 + 5 — generate ramp curve per experience tier.
4. Recipe 9 — compare Q1 cohort vs prior cohorts.
5. Recipe 8 — identify slow rampers (1.5× median).
6. Recipe 7 — check Mindtickle completion correlation.
7. Recipe 11 — render to notion.

**Result:** Hiring + onboarding decisions backed by cohort data.

### Example 2: Training-completion intervention

**Goal:** Sales VP suspects new hires aren't completing training.

**Steps:**
1. Recipe 6 — pull Mindtickle completion for all new hires.
2. Identify: 30% haven't completed by week 4 (target: 100% by week 2).
3. Recipe 7 — correlate with days-to-first-close.
4. If correlation: launch manager-led completion enforcement.
5. Track next cohort; verify completion lift → ramp lift.

**Result:** Training compliance + ramp speed both improve.

### Example 3: Forecast new-hire quota trajectory

**Goal:** Hire 3 new enterprise AEs in July; project their FY revenue contribution.

**Steps:**
1. Recipe 10 — project per quarter for 6 quarters.
2. Sum across 3 hires + apply ramp curve from historical cohort.
3. Compare to "fully ramped 3 AEs" baseline.
4. Identify ramp gap (e.g., $400K in Q3, $800K in Q4) — flag to CFO.

**Result:** Capacity planning is honest about ramp lag; revenue forecast accurate.

## Edge cases / gotchas

- **Start date isn't always day 1** — sometimes AE counted from "ramp end" (post-training). Define consistently.
- **Quota mid-year change** — annual quota changes destroy ramp comparisons unless quotas snapshotted.
- **Segment changes** — AE moves enterprise → MM mid-ramp; ramp data resets contextually.
- **First close on inherited deal** — new AE inherits open opp; first close isn't truly net-new. Flag inheritance.
- **Backfill cohort** — small cohorts (1-2 reps) → high variance. Combine quarters.
- **Training completion gaming** — Mindtickle click-through doesn't mean learning. Pair with quiz scores.
- **External hires vs internal promotion** — different ramp curves. Tag in cohort definition.
- **Pre-existing accounts** — AE assigned to dormant book of business closes "easy" deal fast. Adjust for book quality.
- **Sandbox vs production user IDs** — careful in dev environments; doesn't matter for production analysis.
- **Manager support correlation** — fast rampers often have engaged managers. Anecdotal but worth tracking.
- **Onboarding playbook drift** — if onboarding changes mid-year, old + new cohorts incomparable.
- **Ramp tier in commission plan** — separate from ramp analysis. Don't conflate "ramped quota" (comp) with "post-ramp" (capacity).
- **6-month ramp doesn't fit all roles** — SMB SDR ramp faster (2-3 mo); enterprise AE longer (6-9 mo). Define per role.
- **Macroeconomic confounds** — Q3 2025 hires ramped slow due to market downturn. Annotate context.
- **Survivor bias** — terminated low-performers exit cohort; remaining median is rosier. Track attrition.

## Sources

- [Gong — Sales Ramp benchmark 2026](https://www.gong.io/blog/sales-ramp/)
- [SalesHood ramp framework](https://www.saleshood.com/blog/sales-ramp/)
- [Mindtickle Sales Readiness platform](https://www.mindtickle.com/)
- [Mindtickle API docs](https://help.mindtickle.com/hc/en-us/articles/360024720113)
- [Lessonly (Seismic Learning) API](https://learn.lessonly.com/help/developers)
- [Pavilion ramp benchmarks 2026](https://www.joinpavilion.com/insights/ae-ramp)
- [Bridge Group SaaS AE benchmarks](https://www.bridgegroupinc.com/insidesales/saas-ae)
- [Cohort analysis fundamentals](https://amplitude.com/blog/cohort-analysis)
