<!--
Source: https://www.cubesoftware.com/blog/financial-modeling-software
Source: https://www.eaglerockcfo.com/blog/research/saas-finance-metrics-benchmarks
Source: https://www.bls.gov/oes/  (BLS occupation wages)
Source: https://www.levels.fyi/  (tech comp benchmarks)
-->

# Headcount planning + hiring budget

Driver-based hiring plan: revenue → required headcount by function → comp band → fully-loaded cost → P&L flow-through. Maintain Rule of 40 / burn multiple discipline while sequencing hires.

## When to use

- Annual budget cycle (typically Q4 for next year).
- Mid-year reforecast when growth deviates from plan.
- Pre-fundraise: how much runway extension does each hire cost.
- Department head requests for new headcount.
- Quarterly hiring plan refresh.
- Trigger phrases: "headcount plan", "hiring budget", "FTE plan", "comp bands", "loaded cost", "open req".

NOT for: comp negotiation per-candidate (HR / People function); cap-table impact of grants (use `carta-pulley-cap-table`).

## Setup

Reuses default + bundled skills:

```bash
# Data sources:
# - HRIS via cli-anything + Rippling/Gusto/Deel/Justworks/ADP REST
# - xero-mcp for current payroll cost
# - Levels.fyi for tech comp benchmarks (web research via firecrawl-mcp / web-search)
# - BLS / Glassdoor for non-tech roles

# Modeling:
# - xlsx (default skill) for the plan
# - causal-mosaic-financial-modeling for advanced driver models
```

## The driver-based hiring framework

```
Revenue plan (FY27)
  ↓
Required Headcount by Function = drivers per function
  - Engineering: based on product backlog + team velocity
  - S&M: based on quota carrying capacity × pipeline coverage
  - CS: based on customer count / CSM ratio (typical 30-60 customers per CSM)
  - G&A: based on overall org size (typical 8-12% of total headcount)
  ↓
Comp Band per Role × Geography
  - Levels.fyi for tech (US, UK, EU, Asia)
  - BLS / Glassdoor for non-tech
  ↓
Fully Loaded Cost = Base × Multiplier
  - 1.3 for US (benefits + payroll tax + equipment)
  - 1.4 for US + office (add rent / facilities allocation)
  - 1.2 for fully remote contractor-heavy
  - 1.25 for EU / UK (employer NI/social)
  - 1.15 for offshore contractor
  ↓
Sequenced over time (monthly hire start dates)
  ↓
P&L flow-through (per month + per quarter + annual)
  ↓
Validation: Rule of 40 + burn multiple still healthy
```

## Common recipes

### Recipe 1 — Pull current headcount + cost

```python
import requests, pandas as pd
hris = requests.get(
  "https://api.rippling.com/employees",  # or Gusto, Deel, etc.
  headers={"Authorization": f"Bearer {HRIS_TOKEN}"}
).json()

current = pd.DataFrame(hris)
current["fully_loaded"] = current["base_salary"] * 1.30
print(current.groupby("department").agg(
  count=("id","count"),
  base_total=("base_salary","sum"),
  loaded_total=("fully_loaded","sum")
))
```

### Recipe 2 — Functional headcount drivers

```python
# Engineering: backlog estimation
# Typically 1 SWE per ~4-8 features per quarter (varies by stack)
def eng_headcount_required(roadmap_features_per_q, swe_velocity_features_per_q=5):
    return roadmap_features_per_q / swe_velocity_features_per_q

# Sales: quota capacity
def ae_headcount_required(plan_arr, ae_ramped_quota_arr=900_000, ramp_factor=0.7):
    """ramp_factor accounts for 6-month ramp time"""
    return plan_arr / (ae_ramped_quota_arr * ramp_factor)

# Customer Success: customer:CSM ratio
def csm_headcount_required(customer_count, customers_per_csm=40):
    return customer_count / customers_per_csm

# G&A: percentage of total headcount
def ga_headcount_required(total_revenue_facing_hc, ga_pct=0.10):
    return total_revenue_facing_hc * ga_pct
```

### Recipe 3 — Comp bands by role + geography

```python
# Sample: 2026 comp band table — adjust per current Levels.fyi / Glassdoor / Pave data
COMP_BANDS = {
  ("Engineer L4 — SF Bay",  "base"):   180_000,
  ("Engineer L4 — SF Bay",  "bonus"):  20_000,
  ("Engineer L4 — SF Bay",  "equity"): 75_000,   # annualized RSU value
  ("Engineer L4 — Remote-US","base"):  160_000,
  ("Engineer L4 — EMEA",    "base"):   95_000,
  ("Engineer L4 — Latam",   "base"):   60_000,
  ("Senior PMM — SF Bay",   "base"):   165_000,
  ("Account Executive — SF","base"):   140_000,
  ("Account Executive — SF","ote"):    280_000,  # 50/50 base/var
  ("Customer Success Mgr",  "base"):   110_000,
  ("Sr. Customer Success",  "base"):   135_000,
  ("Finance Manager",       "base"):   145_000,
  ("Controller",            "base"):   180_000,
  # ...
}
```

### Recipe 4 — Build the hire-by-month sheet

```python
import pandas as pd
from datetime import date

hires = pd.DataFrame([
  # Engineering
  {"role":"SWE L4",         "function":"R&D",  "geo":"Remote-US",  "start":"2026-08-01", "base":160_000, "loaded":208_000},
  {"role":"SWE L4",         "function":"R&D",  "geo":"Remote-US",  "start":"2026-09-15", "base":160_000, "loaded":208_000},
  {"role":"SWE L5",         "function":"R&D",  "geo":"SF Bay",     "start":"2026-10-01", "base":205_000, "loaded":266_500},
  {"role":"Sr. PM",         "function":"R&D",  "geo":"Remote-US",  "start":"2026-11-15", "base":175_000, "loaded":227_500},
  # S&M
  {"role":"AE",             "function":"S&M",  "geo":"SF Bay",     "start":"2026-08-01", "base":140_000, "loaded":368_000},  # OTE incl
  {"role":"AE",             "function":"S&M",  "geo":"NY",         "start":"2026-10-01", "base":140_000, "loaded":368_000},
  {"role":"BDR",            "function":"S&M",  "geo":"Remote-US",  "start":"2026-08-15", "base":75_000,  "loaded":135_000},
  {"role":"VP Marketing",   "function":"S&M",  "geo":"Remote-US",  "start":"2026-09-01", "base":210_000, "loaded":273_000},
  # CS
  {"role":"CSM",            "function":"S&M",  "geo":"Remote-US",  "start":"2026-08-15", "base":110_000, "loaded":143_000},
  {"role":"CSM",            "function":"S&M",  "geo":"Remote-US",  "start":"2026-11-01", "base":110_000, "loaded":143_000},
  # G&A
  {"role":"Finance Mgr",    "function":"G&A",  "geo":"Remote-US",  "start":"2026-09-01", "base":145_000, "loaded":188_500},
  {"role":"People Ops",     "function":"G&A",  "geo":"Remote-US",  "start":"2026-10-15", "base":120_000, "loaded":156_000},
])
hires["start"] = pd.to_datetime(hires["start"])
```

### Recipe 5 — Monthly cost flow to P&L

```python
months = pd.date_range("2026-07-01", "2027-06-30", freq="MS")
cost_by_month = pd.DataFrame(index=months, columns=["R&D","S&M","G&A"]).fillna(0)

for _, h in hires.iterrows():
    for m in months:
        if m >= h.start:
            cost_by_month.loc[m, h.function] += h.loaded / 12

# Add existing payroll
for func, existing_loaded in current_payroll_by_function.items():
    cost_by_month[func] = cost_by_month[func] + existing_loaded / 12

cost_by_month["Total"] = cost_by_month.sum(axis=1)
print(cost_by_month)
```

### Recipe 6 — Validate Rule of 40 + burn multiple

```python
# After hiring plan: simulate financial impact
def validate_hiring_plan_impact(hires, revenue_plan, gross_margin=0.78):
    annual_revenue = revenue_plan.sum()
    annual_loaded_cost_new = (cost_by_month.sum() - current_run_rate * 12)
    # Project new EBITDA
    rev_growth = revenue_plan[-1]*12 / revenue_plan[0]*12 - 1
    new_total_opex = total_opex_current + annual_loaded_cost_new + non_payroll_opex
    new_ebitda = annual_revenue * gross_margin - new_total_opex
    new_ebitda_margin = new_ebitda / annual_revenue
    rule_of_40 = rev_growth * 100 + new_ebitda_margin * 100

    new_burn = -new_ebitda / 12  # assume EBITDA ≈ cash burn (rough)
    new_arr_growth = (revenue_plan[-1]*12 - revenue_plan[0]*12)
    burn_multiple = new_burn * 12 / new_arr_growth

    return {
      "rule_of_40": rule_of_40,
      "burn_multiple_yearly": burn_multiple,
      "runway_impact_months": -annual_loaded_cost_new / current_cash * 12 if annual_loaded_cost_new > 0 else 0
    }
```

If Rule of 40 drops below 40 or burn multiple goes above 1.5x, surface as flag.

### Recipe 7 — Sequenced ramp (revenue-aware)

```python
# Don't hire ahead of revenue; phase hires after key milestones
def sequence_hires_by_revenue_trigger(hires, monthly_arr):
    sequenced = []
    for _, h in hires.iterrows():
        # Hold S&M hires until ARR > $3M; hold G&A until ARR > $5M
        if h.function == "S&M" and monthly_arr.get(h.start.strftime("%Y-%m-01"), 0) < 250_000:
            h.start = monthly_arr[monthly_arr >= 250_000].index[0]
        if h.function == "G&A" and monthly_arr.get(h.start.strftime("%Y-%m-01"), 0) < 416_000:
            h.start = monthly_arr[monthly_arr >= 416_000].index[0]
        sequenced.append(h)
    return pd.DataFrame(sequenced)
```

### Recipe 8 — ARR per FTE benchmark

```python
def arr_per_fte(arr_now, headcount_now):
    return arr_now / headcount_now

# 2026 benchmarks (Bessemer):
# Seed:     $150-$200K ARR/FTE — too early to measure
# Series A: $250-$350K ARR/FTE
# Series B: $300-$500K ARR/FTE
# Series C+: $500K+/FTE
# Best-in-class public SaaS: $750K-$1.5M/FTE

current_arr_per_fte = arr_per_fte(4_200_000, 45)
print(f"Current ARR/FTE: ${current_arr_per_fte:,.0f}")
# If below stage benchmark: efficiency problem, slow hiring
```

### Recipe 9 — Open req tracking

```python
opens = pd.DataFrame([
  {"req":"SWE L4","function":"R&D","posted":"2026-06-01","target_start":"2026-08-01","status":"interviewing"},
  {"req":"AE","function":"S&M","posted":"2026-06-15","target_start":"2026-08-01","status":"sourcing"},
  # ...
])

opens["days_open"] = (pd.Timestamp.today() - pd.to_datetime(opens["posted"])).dt.days
opens["slip_risk"] = (pd.to_datetime(opens["target_start"]) - pd.Timestamp.today()).dt.days < 30

# Surface to founder: any reqs at risk of slipping start date
at_risk = opens[opens.slip_risk]
print(f"{len(at_risk)} open reqs at risk of slipping start date")
```

### Recipe 10 — Backfill vs growth signal

```python
# Track replacement vs net new hires
def hiring_mix(hires_period, departures_period):
    backfills = min(len(hires_period), len(departures_period))
    net_new = len(hires_period) - backfills
    return {
      "total_hires": len(hires_period),
      "backfills": backfills,
      "net_new": net_new,
      "backfill_rate": backfills / len(hires_period) if hires_period else 0
    }
# Healthy: backfill rate ~30%, net new dominant (=growth)
# Concern: backfill rate > 60% (= attrition or no growth)
```

## Examples

### Example 1: Build FY27 hiring plan

**Goal:** Translate FY27 revenue plan ($5M → $9M ARR) into hiring schedule.

**Steps:**

1. Recipe 1 → current state: 28 FTE, $4.7M annualized loaded cost.
2. Recipe 2 → required adds:
   - R&D: 4 SWE + 1 PM (backlog growth + AI investments)
   - S&M: 2 AE + 1 BDR + VP Marketing (capacity for $4M new ARR)
   - CS: 2 CSM (customer growth from 80 → 140 logos)
   - G&A: 1 Finance Mgr + 1 People Ops (scale ops)
3. Recipe 3 → assign comp bands per role + geo.
4. Recipe 4 → build hire-by-month sheet (sequenced).
5. Recipe 5 → monthly cost flow to P&L.
6. Recipe 6 → validate Rule of 40 (target ≥45 by year-end) + burn multiple (target ≤1.5x).
7. Recipe 7 → sequence so S&M hires follow first $3M ARR milestone.
8. Recipe 8 → check ARR/FTE trajectory ($170K → $185K — improving = good signal).
9. Issue plan to founder; iterate.

**Result:** 11 hires sequenced over 12 months; cost flow validated against Rule of 40; FY27 ends at 39 FTE.

### Example 2: Hire freeze during runway crunch

**Goal:** Cash $2.1M, burn $200K = 10 months runway. Cannot hire.

**Steps:**

1. Cancel all open reqs not yet at offer stage.
2. Recipe 9 → 5 reqs paused.
3. For 2 reqs in final interviews: complete the interviews, make decision case-by-case.
4. Build "hire freeze" memo: explanation + criteria for unfreeze.
5. Communicate to leadership team + via all-hands.
6. Track open reqs as "frozen" status; unfreeze gated on fundraise milestone.

**Result:** Saved $40-60K/mo in run-rate avoided cost; runway extends 2 months.

## Edge cases / gotchas

- **Fully loaded cost is country-specific:** US 1.3-1.4x; EU 1.25-1.35x; UK 1.20-1.30x; offshore contractors 1.10-1.15x.
- **Equity is comp:** include annualized equity grant value in candidate's total comp; don't think of it as free.
- **Ramp time:** AEs typically ramp 6 months; engineers 3-4 months. Apply ramp factor to capacity.
- **Backfill cost > new hire cost:** replacing a departing employee costs 0.5-2x annual salary (recruiting, ramp, lost productivity). Model this.
- **Department head pressure:** every department head wants more headcount. Apply driver-based discipline; don't add by request alone.
- **Sequencing matters more than total:** 12 hires in Q1 = 4x burn impact of 12 hires in Q4. Always sequence.
- **Geographic mix shifts effective cost:** moving from 100% US to 60% US + 40% LATAM cuts blended loaded cost ~25%.
- **Office vs remote:** office means rent + facilities + IT support — add to loaded cost factor.
- **Comp inflation:** US tech comp inflated ~8%/yr in 2021-2022, normalized 2023-2025 to 3-5%. Plan annual increases.
- **Hiring efficiency:** if recruiter pipeline can't fill the plan, the plan is fiction. Validate with recruiting capacity.
- **Counter-offer math:** when key employee gets external offer, counter-offer < 1 yr typically fails. Decide upfront whether to engage in counter-offers.
- **Severance budget:** include severance accrual for departures; typical 4-12 weeks pay.

## Sources

- Cube — financial modeling software: https://www.cubesoftware.com/blog/financial-modeling-software
- Eagle Rock — SaaS benchmarks 2026: https://www.eaglerockcfo.com/blog/research/saas-finance-metrics-benchmarks
- BLS occupational wages: https://www.bls.gov/oes/
- Levels.fyi (tech comp): https://www.levels.fyi/
- Pave (compensation data): https://www.pave.com/
- Bessemer Atlas (ARR/FTE benchmarks): https://www.bvp.com/atlas/

## Related skills

- `causal-mosaic-financial-modeling` — sequenced cost flow into 3-statement model
- `runway-burn-analysis` — hire freeze decision driven by runway state
- `unit-economics-saas-metrics` — ARR/FTE + Rule of 40 + burn multiple
- `monthly-close-procedure` — actual cost ties back to plan
