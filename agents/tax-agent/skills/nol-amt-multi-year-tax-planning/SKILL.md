<!--
Source: https://www.irs.gov/forms-pubs/about-form-4626
Source: https://www.fenwick.com/insights/publications/section-382-overview
Source: https://www.irs.gov/instructions/i1120
Source: https://www.irs.gov/forms-pubs/about-publication-536
Reference role.md: "NOL + AMT + multi-year planning"
-->

# NOL waterfall + CAMT + Section 382 + multi-year planning

Post-TCJA NOL mechanics: indefinite carryforward, 80% taxable-income offset cap, no carryback (except farming + casualty). Section 382 ownership-change limitation triggered when >50% shift in 3-year testing window — caps annual NOL usage at FMV × long-term tax-exempt rate. Corporate AMT (CAMT) replaced under IRA 2022: 15% on Adjusted Financial Statement Income (AFSI) for $1B+ avg 3-yr AFSI corps. Multi-year tax model spans NOL waterfall, R&D credit waterfall, stock comp timing, QSBS holding, state nexus expansion, charitable stacking, DB plan funding.

## When to use

- C-corp NOL year — track waterfall + Section 382 risk.
- Fundraise round (3-year testing window for 382 may close 50%+ shift).
- M&A diligence: identify acquirer's NOL utilization risk under 382.
- Forecast multi-year tax model for board / planning purposes.
- CAMT applicability test if AFSI approaching $1B.
- Multi-year R&D credit utilization / general business credit limit planning.
- Trigger phrases: "NOL", "net operating loss", "Section 382", "ownership change", "CAMT", "AFSI", "Form 4626", "multi-year tax plan", "Form 2220", "Form 7004 extension".

NOT for: individual NOL (covered briefly here; refer to Pub 536); state-specific NOL (state by state — out of single-skill scope); ASC 740 deferred tax presentation (use `asc-740-tax-provision-deferred`).

## Setup

### Preparer software (Drake / ProConnect / UltraTax / CCH)

```bash
# All major preparer software handles NOL roll-forward + Section 382 limitation
# Most have NOL schedule built-in
export DRAKE_API_KEY="..."
# Build NOL workpaper externally in xlsx if preparer doesn't expose detailed roll
```

### Bloomberg Tax Provision (multi-year model)

```bash
# Bloomberg Tax Provision includes multi-year forecasting module
export BLOOMBERGTAX_API_KEY="..."
curl -H "Authorization: Bearer $BLOOMBERGTAX_API_KEY" \
  https://api.bloombergtax.com/v1/provision/forecast
```

### ONESOURCE Tax Provision (Thomson Reuters)

```bash
# Same capability
export ONESOURCE_API_KEY="..."
```

### Section 382 calculator (specialty)

```bash
# Section 382 limitation studies typically done by tax law firms
# Templates: Fenwick & West, Cooley, Wilson Sonsini
```

## Common recipes

### Recipe 1 — NOL waterfall by vintage year

```python
# Post-TCJA NOLs:
#  - Generated 2018+: indefinite carryforward; no carryback; offset 80% of TI
#  - Generated pre-2018: 2-yr carryback (mostly used); 20-yr carryforward
import pandas as pd

nol_waterfall = pd.DataFrame([
    {"vintage_yr": 2019, "generated": 2_400_000, "used": 800_000, "remaining": 1_600_000},
    {"vintage_yr": 2020, "generated": 3_100_000, "used": 0, "remaining": 3_100_000},
    {"vintage_yr": 2021, "generated": 1_850_000, "used": 0, "remaining": 1_850_000},
    {"vintage_yr": 2022, "generated": 985_000, "used": 0, "remaining": 985_000},
    {"vintage_yr": 2023, "generated": 0, "used": 0, "remaining": 0},  # profitable
    {"vintage_yr": 2024, "generated": 0, "used": 0, "remaining": 0},  # profitable
    {"vintage_yr": 2025, "generated": 1_240_000, "used": 0, "remaining": 1_240_000},
])

current_yr_pretax_income = 4_500_000
nol_available = nol_waterfall.remaining.sum()  # 8.775M
nol_usable_80pct = 0.80 * current_yr_pretax_income  # 3.6M
nol_used_this_year = min(nol_available, nol_usable_80pct)  # 3.6M
taxable_income_after_nol = current_yr_pretax_income - nol_used_this_year
print(f"Taxable income after NOL: ${taxable_income_after_nol:,.0f}")
# = $900K × 21% = $189K federal tax
```

### Recipe 2 — Section 382 ownership change test

```python
# Section 382 triggered when ownership of "5% shareholders" increases > 50% 
#   in any 3-year testing window
# Limits annual NOL usage post-change to: FMV × long-term tax-exempt rate (LTTER)
# LTTER published monthly by IRS; ~4.6% as of mid-2026

# Step 1: identify all 5% shareholders
# Step 2: compute "shift" for each 3-yr period ending today
# Step 3: if any window > 50% shift → ownership change

import pandas as pd
shareholders = pd.DataFrame([
    {"name": "Founder A", "ownership_t0": 0.40, "ownership_t1": 0.30, 
     "ownership_t2": 0.18, "ownership_t3": 0.12},  # diluted over rounds
    {"name": "Founder B", "ownership_t0": 0.40, "ownership_t1": 0.30,
     "ownership_t2": 0.18, "ownership_t3": 0.12},
    {"name": "Public group (<5% each)", "ownership_t0": 0.20, 
     "ownership_t1": 0.15, "ownership_t2": 0.10, "ownership_t3": 0.07},
    {"name": "Seed VC", "ownership_t0": 0, "ownership_t1": 0.25,
     "ownership_t2": 0.20, "ownership_t3": 0.15},
    {"name": "Series A VC", "ownership_t0": 0, "ownership_t1": 0,
     "ownership_t2": 0.34, "ownership_t3": 0.27},
    {"name": "Series B VC", "ownership_t0": 0, "ownership_t1": 0,
     "ownership_t2": 0, "ownership_t3": 0.27},
])
# Compute cumulative shift t0 → t3 for each 5% shareholder
# Section 382 considers MAX increase for each — "owner shift"
```

### Recipe 3 — Section 382 limitation calculation

```python
# If ownership change triggered:
# Annual NOL usage limit = FMV at change × LTTER
# Pre-change NOLs subject to limit; post-change NOLs unrestricted

fmv_at_change = 145_000_000   # equity FMV at ownership change date
ltter = 0.0465                 # 4.65% (current IRS rate)
section_382_annual_limit = fmv_at_change * ltter  # = $6.74M / year

pre_change_nol = 8_775_000
years_to_consume_at_limit = pre_change_nol / section_382_annual_limit  # = 1.3 yrs
# Most pre-change NOLs usable within ~2 years given limit > NOL

# If NIH (Net Unrealized Built-in Gain) > threshold (15% basis or $10M):
# Add NIH to limit for 5 years post-change
```

### Recipe 4 — CAMT (Corporate Alternative Minimum Tax) check

```python
# CAMT (IRA 2022) applies if:
#  3-yr average AFSI (Adjusted Financial Statement Income) > $1 billion
# Tax = 15% × AFSI (with adjustments)
# Form 4626

# AFSI = book income with adjustments:
#  - Add back: depreciation, financial losses
#  - Subtract: certain deferred income, etc.
#  - Foreign-parented MNE: $100M US AFSI test instead

avg_afsi_3yr = 850_000_000  # < $1B threshold → not CAMT
# Most SaaS / mid-cap recipients NOT subject
```

### Recipe 5 — Multi-year tax model (3-5 yr horizon)

```python
# Build driver-based tax model in xlsx (use xlsx skill)
import pandas as pd
multi_year = pd.DataFrame({
    "year": [2025, 2026, 2027, 2028, 2029],
    "book_pretax_income": [2_400_000, 4_800_000, 8_500_000, 12_000_000, 16_000_000],
    "m1_perm_adjs": [85_000, 92_000, 105_000, 120_000, 138_000],
    "m1_temp_adjs_depr": [(120_000), (95_000), (45_000), 25_000, 75_000],
    "m1_temp_adjs_stock_comp": [380_000, 420_000, 465_000, 510_000, 555_000],
    "m1_temp_adjs_sec_174": [(75_000), (65_000), (55_000), (45_000), 35_000],
})
multi_year["taxable_income_pre_nol"] = (
    multi_year.book_pretax_income 
    + multi_year.m1_perm_adjs 
    + multi_year.m1_temp_adjs_depr
    + multi_year.m1_temp_adjs_stock_comp
    + multi_year.m1_temp_adjs_sec_174
)
# NOL waterfall consumed FIFO
# R&D credit waterfall consumed FIFO
# Compute federal + state tax per year
# Add sensitivity table on key drivers
```

### Recipe 6 — General business credit limit (Section 38)

```python
# General Business Credit (GBC) includes R&D credit + others
# Limit: Net tax above $25K, less than 25% of excess; ie GBC capped
# Carryback 1 yr; Carryforward 20 yrs

net_regular_tax = 1_800_000
amt = 0
gbc_limit = (net_regular_tax + amt - max(25_000, 0.25 * (net_regular_tax + amt - 25_000)))
# Excess credits carryforward

gbc_components = {
    "rd_credit": 480_000,
    "wotc": 18_000,  # Work Opportunity Credit
    "disabled_access": 5_000,
}
total_gbc_claimed = min(sum(gbc_components.values()), gbc_limit)
```

### Recipe 7 — Pre-fundraise Section 382 planning

```python
# Before closing a round that may trigger 50%+ shift:
#  - Snapshot ownership ledger pre-close
#  - Run shift simulation
#  - If trigger inevitable: maximize current-year NOL usage by accelerating income
#  - If close to but not over: consider structure adjustments (warrant strikes, 
#    delayed issuance)

# Snapshot:
ownership_snapshot = {
    "founder_a": 0.18, "founder_b": 0.18,
    "seed_vc": 0.15, "series_a_vc": 0.27,
    "common_pool": 0.12, "future_pool": 0.10
}

# Proposed Series B raise:
new_b_vc_pct = 0.22
post_dilution = {k: v * (1 - new_b_vc_pct) for k, v in ownership_snapshot.items()}
post_dilution["series_b_vc"] = new_b_vc_pct

# Check Section 382 cumulative shift over 3-yr window
# If borderline 50% → 51%, even 1% can be significant given limit math
```

### Recipe 8 — Form 2220 (corporate underpayment penalty)

```python
# Form 2220 calculates penalty for underpaid quarterly estimates
# Safe harbor (Recipe 4 in payroll skill)
# Large corp ($1M+ TI in prior 3 yrs) has NO PY safe harbor — must use CY actual

# Penalty rates: federal short-term rate + 3% (varies quarterly)
# Compounded daily

# Calculation per quarter:
quarterly_required = 425_000  # safe harbor
quarterly_paid = 100_000      # underpaid
underpayment = quarterly_required - quarterly_paid
days_late = 92  # days from due to payment
penalty_rate_annual = 0.083  # 8.3% (short-term + 3%)
penalty = underpayment * penalty_rate_annual * (days_late / 365)
```

### Recipe 9 — NOL acquisition diligence

```python
# Target company has $8M NOL; acquirer wants to use against future income
# Section 382: change of ownership triggers limit
# Plus continuity of business enterprise (COBE) requirement for 2 yrs post-change
# Plus 5-yr lookback for built-in losses (RBIL/RBIG)

target_nol = 8_000_000
target_fmv_at_acquisition = 22_000_000
ltter = 0.0465

annual_limit_post_change = target_fmv_at_acquisition * ltter  # = $1.02M/yr
years_to_consume = target_nol / annual_limit_post_change  # = 7.8 yrs
# After Section 382, NOLs may be impaired — discount in deal valuation
# Continuity-of-business required for 2 years; severe restructure can eliminate NOL entirely
```

### Recipe 10 — Section 163(j) interest limitation interaction

```python
# Business interest deduction limited to 30% of ATI (post-TCJA)
# Small business exception: avg 3-yr gross receipts < $30M (2026 indexed)
# Disallowed interest carries forward indefinitely
# Combined with NOL limit can compound

ati = 5_200_000  # Adjusted Taxable Income (~EBITDA pre-2022; ~EBIT 2022+)
business_interest = 3_500_000
sec_163j_limit = 0.30 * ati  # = 1.56M
deductible_interest = min(business_interest, sec_163j_limit)  # = 1.56M
disallowed_interest = business_interest - deductible_interest  # = 1.94M
# Carries forward; reduces future deductions stacking with NOL
```

## Examples

### Example 1: Series B SaaS with $8.5M cumulative NOL, no 382 yet

**Goal:** Profitable Year 1, $4.2M pretax book income. Forecast 5-yr NOL utilization.

**Steps:**

1. Build NOL waterfall by vintage (Recipe 1).
2. Section 382 check: pre-Series B ownership snapshot; no change yet (under 50%).
3. Forecast taxable income years 1-5 ($4.2M, $7.8M, $12M, $18M, $24M).
4. NOL usage per year capped at 80% of TI; full $8.5M consumed by year 3.
5. Federal tax: yr 1 $840K × 21% × 20% = $176K; yr 2 fully NOL-shielded $1.56M; yr 3 partial; yr 4-5 full tax.
6. R&D credit waterfall: $1.2M cumulative; consume against post-NOL liability.
7. Multi-year cash tax forecast for treasury planning.

**Result:** 3-yr tax model; ~$2.3M cash tax cumulative; NOL fully utilized year 3.

### Example 2: Pre-Series B fundraise with 382 risk

**Goal:** Founders + Seed + Series A = 100% pre-B; Series B will buy 32%; concern about 50%+ shift cumulative over 3 yrs (Seed buy at t-2 was 25%; Series A at t-1 was 30%).

**Steps:**

1. Compute cumulative ownership shift for last 3 years (Recipe 2).
2. Aggregate shift in 5% shareholders: Seed (25%) + Series A (30%) + projected B (32%) = 87% net shift over 3-yr window.
3. >> 50% → Section 382 triggered upon Series B close.
4. Compute Section 382 limit: FMV at close $185M × 4.65% = $8.6M/yr.
5. Pre-change NOL $8.5M → consumed in 1 year at limit.
6. Continue using R&D credits subject to Section 383 (separate but parallel limit).
7. Document 5%-shareholder ledger + 382 study for ASC 740 valuation allowance assessment.

**Result:** Series B closes; NOL fully usable within 1 year under new limit; future NOLs unrestricted.

### Example 3: Acquirer diligencing target with $12M NOL

**Goal:** $25M acquisition; target has $12M NOL + $1.8M R&D credit carryforward.

**Steps:**

1. Section 382 ownership change at closing (100% acquired).
2. Annual limit: $25M FMV × 4.65% = $1.16M/yr.
3. $12M NOL utilization = 10+ years.
4. Discount NOL value for time-value-of-money + utilization uncertainty.
5. NUBIG (net unrealized built-in gain) test: target has $4M built-in gains in IP → can recognize over 5 yrs to increase limit.
6. R&D credit carryforward Section 383: parallel 382 limit application.
7. Continuity of Business Enterprise (COBE): acquirer must continue target's historic business for 2 yrs.
8. ASC 805 / 740 in business combination: record DTA on acquired NOL × utilization probability.

**Result:** NOL worth ~$1.4M PV (heavily discounted from face $12M × 21%); R&D credit carry similarly impaired.

## Edge cases / gotchas

- **Post-TCJA NOLs (2018+):** indefinite carryforward; NO carryback; 80% taxable income offset cap. Pre-2018 NOLs: 2-yr carryback + 20-yr carryforward (mostly already used).
- **Section 382 5% shareholder rules:** "owner shift" measured per 5% shareholder. Multiple < 5% holders aggregated into "public group" (one shareholder).
- **Continuity of Business Enterprise (COBE):** must continue target's historic business or use significant target assets for 2 yrs post-change. Severe restructure → NOL impaired.
- **Reverse merger / SPAC:** if private company merges into public shell, Section 382 limit based on FMV at close — can be very low for cash-shell SPACs, severely impairing usability.
- **Section 383:** parallels Section 382 for capital loss carryovers, foreign tax credits, R&D credits, GBC. Same annual limit, separate basket.
- **NUBIG / NUBIL:** Net Unrealized Built-in Gain / Loss. If RBIG > threshold (15% of basis or $10M), can accelerate NOL usage; if RBIL > threshold, limits NOL usage for 5 years.
- **Sec 163(j) ATI:** post-2022 calculation uses EBIT (not EBITDA). Materially reduces deduction for capital-intensive businesses.
- **Form 2220 large-corp exception:** $1M+ TI in any of prior 3 yrs disqualifies PY safe harbor; must use CY actual. Pay attention to first-year-of-profitability transitions.
- **CAMT applicability:** 3-yr average AFSI > $1B. Excludes most SaaS / mid-cap. Foreign-parented MNE: $100M US AFSI test.
- **CAMT FTC:** foreign tax credit allowed against CAMT, mitigating for MNEs.
- **State NOL deviations:** states adopt different NOL rules. NY: 80% cap matches federal; CA: 80% cap, no carryback most years; NJ: 20-yr carryforward, no carryback. Track state NOLs separately.
- **Section 172(b)(1) farming / casualty 2-yr carryback exception:** narrow exceptions to no-carryback rule.
- **Net interest carryforward (Sec 163(j)):** indefinite carryforward; reset on Section 382 change too.
- **R&D credit carryforward + 280C(c)(3) election:** election binding for life of credit; matters for multi-year modeling.
- **NOL DTA valuation allowance under ASC 740:** record VA against NOL DTA if "more likely than not" cannot utilize. Section 382 limit + projected future income drive VA.
- **NOL transferability:** NOLs not transferable except via merger / acquisition (constrained by 382). Cannot sell NOL standalone.

> WARNING **This is informational guidance from an AI agent. Always consult a licensed CPA or tax attorney in your jurisdiction before filing returns, claiming credits, or implementing binding tax positions.**

## Sources

- IRC Section 172 (NOL): https://www.law.cornell.edu/uscode/text/26/172
- IRC Section 382: https://www.law.cornell.edu/uscode/text/26/382
- IRC Section 383: https://www.law.cornell.edu/uscode/text/26/383
- IRC Section 163(j): https://www.law.cornell.edu/uscode/text/26/163
- IRS Form 4626 (CAMT): https://www.irs.gov/forms-pubs/about-form-4626
- IRS Form 2220 (underpayment): https://www.irs.gov/forms-pubs/about-form-2220
- IRS Form 8990 (interest limit): https://www.irs.gov/forms-pubs/about-form-8990
- IRS Publication 536 (NOL for individuals): https://www.irs.gov/publications/p536
- Fenwick & West — Section 382 overview: https://www.fenwick.com/insights/publications/section-382-overview
- Fenwick & West — Section 382 ownership change rules: https://www.fenwick.com/insights/publications/section-382-ownership-change-rules
- IRS Long-term tax-exempt rate: https://www.irs.gov/applicable-federal-rates
- Treas Reg 1.382-2 / 1.382-2T: https://www.law.cornell.edu/cfr/text/26/1.382-2T
- AICPA — CAMT guidance: https://www.aicpa.org/topic/tax/corporate-alternative-minimum-tax

## Related skills

- `form-1120-corp-income-tax-filing` — NOL deduction line 29 + Section 382 disclosure
- `asc-740-tax-provision-deferred` — NOL DTA + valuation allowance assessment
- `rd-tax-credit-form-6765-mainstreet-neo` — Section 383 R&D credit limit
- `qsbs-section-1202-bbb-2025-expansion` — multi-year QSBS planning
- `iso-nso-rsu-employee-tax-treatment` — stock comp temp diff
