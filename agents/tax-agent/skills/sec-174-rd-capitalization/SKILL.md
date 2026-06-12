<!--
Source: https://www.irs.gov/instructions/i4562
Source: https://www.fenwick.com/insights/publications/section-174-rd-capitalization-update-big-beautiful-bill
Source: https://www.aicpa.org/topic/tax/section-174-research-experimental
Source: https://www.law.cornell.edu/uscode/text/26/174
Reference role.md: "Section 174 R&D capitalization"
-->

# Section 174 — R&D capitalization (TCJA 2017 + OBBB 2025 reversal)

TCJA 2017 mandated Section 174 R&D capitalization + amortization (5-yr domestic, 15-yr foreign) starting 2022. **One Big Beautiful Bill Act July 2025** RESTORED IMMEDIATE EXPENSING for DOMESTIC R&D (retroactive to 2025); foreign R&D still 15-yr amortization. Track per-project allocation of Specified Research or Experimental (SRE) expenditures. Interplay with Section 41 R&D credit definitions (similar but not identical).

## When to use

- Annual Section 174 R&D capitalization (pre-OBBB or for foreign R&D).
- 2025 transition year: OBBB reversal for domestic R&D requires accounting method change.
- 2026+ planning: domestic R&D immediately expensed; foreign R&D 15-yr amortized.
- Form 3115 (Change in Accounting Method) for transition.
- Coordinate with Section 41 R&D credit (definitional overlap but not identical).
- Trigger phrases: "Section 174", "Sec 174", "R&D capitalization", "SRE expenditures", "specified research expenditures", "5-year amortization", "15-year foreign", "Form 3115", "method change", "OBBB Section 174", "Big Beautiful Bill R&D".

NOT for: Section 41 R&D credit (use `rd-tax-credit-form-6765-mainstreet-neo`); R&D ASC 730 book accounting (out of scope); deferred tax effects (use `asc-740-tax-provision-deferred`).

## Pre-OBBB vs Post-OBBB

| Item | Pre-OBBB (TY 2022-2024) | Post-OBBB (TY 2025+) |
|---|---|---|
| Domestic R&D treatment | 5-yr amortization | Immediate expensing |
| Foreign R&D treatment | 15-yr amortization | 15-yr amortization (unchanged) |
| Mid-year convention | Half-year first year | Full-year first year (when amortized) |
| Form 4562 | Required | Required for foreign only |
| Section 280C(c) interplay | Reduce credit OR reduce deduction | Reduce credit OR reduce deduction (unchanged) |
| Method change for 2025 | n/a | Form 3115 with auto-consent procedure |

OBBB enacted July 2025; retroactive to TY 2025.

## Setup

### Preparer software handling (Drake / ProConnect / UltraTax / CCH)

```bash
# All preparer software handle 174 amortization waterfall + transition
# UltraTax: dedicated 174 module since TY 2022
# CCH Axcess: 174 schedule in fixed asset / depreciation
```

### Form 3115 method change software

```bash
# Preparer software prepares Form 3115
# Bloomberg Tax + ONESOURCE include 3115 templates
```

### MainStreet / Neo Tax (R&D credit + 174 integration)

```bash
# MainStreet / Neo Tax cover R&D credit + 174 capitalization workpapers
export MAINSTREET_API_KEY="..."
curl -H "Authorization: Bearer $MAINSTREET_API_KEY" \
  https://api.mainstreet.com/v1/section_174
```

## What qualifies as SRE expenditure

Per Treas Reg 1.174-2 (revised 2024):

- **Wages** for employees performing SRE activities (incl. direct supervision + support)
- **Supplies + materials** consumed in SRE activities
- **Cost of obtaining a patent** (legal fees, application fees)
- **Software development costs** (per Rev Proc 2000-50 historical guidance; superseded by 2022 mandatory capitalization)
- **Contract research costs** paid to 3rd parties for SRE (full 100%, not 65% like Section 41)
- **Rent + utility** allocated to SRE facility
- **Depreciation of equipment** used in SRE

NOT qualified:
- Routine engineering / quality control
- Market research, advertising
- Post-launch product maintenance
- Land + improvements

## Common recipes

### Recipe 1 — Identify SRE expenditures per project

```python
# Allocate by employee × project × time
import pandas as pd
employee_time = pd.read_sql("""
SELECT employee_id, project_id, hours, period
FROM time_tracking
WHERE period BETWEEN '2025-01-01' AND '2025-12-31'
""", db)

employee_wages = pd.read_sql("SELECT employee_id, annual_wages FROM payroll_2025", db)

sre_by_project = employee_time.merge(employee_wages, on="employee_id")
sre_by_project["wage_allocation"] = (
    sre_by_project.hours / 2080 * sre_by_project.annual_wages
)
project_sre_wages = (
    sre_by_project.groupby("project_id").wage_allocation.sum()
)
```

### Recipe 2 — Domestic vs foreign SRE split

```python
# Domestic = SRE conducted in US
# Foreign = SRE conducted outside US (15-yr amortization regardless of OBBB)
# "Located" = activity location, not employer location

sre_split = pd.DataFrame([
    {"project": "RD-2025-001", "domestic_wages": 425_000, 
     "domestic_supplies": 8_500, "domestic_contract": 35_000,
     "foreign_wages": 0, "foreign_supplies": 0, "foreign_contract": 0},
    {"project": "RD-2025-002", "domestic_wages": 380_000,
     "domestic_supplies": 12_500, "domestic_contract": 0,
     "foreign_wages": 0, "foreign_supplies": 0, "foreign_contract": 25_000},
    {"project": "RD-2025-003 (EU dev team)", "domestic_wages": 0,
     "domestic_supplies": 0, "domestic_contract": 0,
     "foreign_wages": 285_000, "foreign_supplies": 8_500, 
     "foreign_contract": 0},
])
sre_split["total_domestic_sre"] = (
    sre_split.domestic_wages + sre_split.domestic_supplies 
    + sre_split.domestic_contract
)
sre_split["total_foreign_sre"] = (
    sre_split.foreign_wages + sre_split.foreign_supplies 
    + sre_split.foreign_contract
)
total_domestic = sre_split.total_domestic_sre.sum()  # = 861K
total_foreign = sre_split.total_foreign_sre.sum()    # = 318.5K
```

### Recipe 3 — TY 2025+ treatment (post-OBBB)

```python
# Post-OBBB:
#  Domestic SRE: immediate expense at TY (no amortization)
#  Foreign SRE: 15-yr straight-line, half-year convention first year

domestic_sre_2025 = total_domestic
foreign_sre_2025 = total_foreign

# Domestic deduction = full amount immediately
domestic_deduction_2025 = domestic_sre_2025

# Foreign amortization
# Half-year convention: first year = 6/180 = 3.33%
foreign_2025_amortization = foreign_sre_2025 / 15 / 2  # half-year
foreign_capitalized_eoy = foreign_sre_2025 - foreign_2025_amortization
```

### Recipe 4 — Pre-OBBB amortization waterfall (TY 2022-2024)

```python
# Pre-OBBB capitalized SREs still amortize per original schedule
# Method change election doesn't accelerate; pre-2025 capitalizations continue

pre_obbb_capitalized = pd.DataFrame([
    {"vintage": 2022, "domestic_sre": 720_000, "foreign_sre": 180_000,
     "years_remaining_domestic": 2,  # 5-yr life, 3 yrs amortized through 2024
     "years_remaining_foreign": 12},
    {"vintage": 2023, "domestic_sre": 850_000, "foreign_sre": 220_000,
     "years_remaining_domestic": 3,
     "years_remaining_foreign": 13},
    {"vintage": 2024, "domestic_sre": 940_000, "foreign_sre": 250_000,
     "years_remaining_domestic": 4,
     "years_remaining_foreign": 14},
])

# Each vintage amortizes through its respective life
for vintage in pre_obbb_capitalized.itertuples():
    domestic_annual = vintage.domestic_sre / 5
    foreign_annual = vintage.foreign_sre / 15
    # 2025 deduction = annual amortization
```

### Recipe 5 — Form 3115 method change for 2025 OBBB transition

```python
# Auto-consent method change procedure under Rev Proc 2022-14 / 2025 update
# Election made on TY 2025 Form 1120 via Form 3115 attached

form_3115 = {
    "applicant": "Acme Inc",
    "tin": "12-3456789",
    "method_change_category": "Section 174 transition under OBBB Act 2025",
    "from_method": "5-yr amortization (pre-OBBB)",
    "to_method": "Immediate expensing for domestic SRE",
    "section_481_a_adjustment": 0,  # No catch-up; only prospective
    "effective_year": 2025,
    "form_3115_part_iv": "Method change description + transition rules cite",
}
# IRS expected to issue specific guidance Q3 2025; check IRS bulletins
```

### Recipe 6 — Section 280C(c) interaction (R&D credit)

```python
# Section 280C(c)(1): default — reduce R&D wage deduction by credit amount
# Section 280C(c)(3): election — take credit reduced by max corp rate (21%)
#                                instead of reducing deduction
# Election made on Form 6765 line 17

rd_credit_2025 = 280_000
sec_174_domestic_deduction = 861_000

# Default treatment:
sec_174_after_280c = sec_174_domestic_deduction - rd_credit_2025  # = 581K

# Section 280C(c)(3) election:
reduced_credit = rd_credit_2025 * (1 - 0.21)  # = 221,200
sec_174_after_election = sec_174_domestic_deduction  # full deduction

# Compare tax impact:
default_tax_impact = (sec_174_after_280c * 0.21) - rd_credit_2025
election_tax_impact = (sec_174_after_election * 0.21) - reduced_credit
# Typically equivalent if at 21% rate; differs if NOL or lower effective rate
```

### Recipe 7 — Software development specific rules

```python
# Pre-OBBB (TY 2022-2024): all software development = SRE under 174
# Post-OBBB (TY 2025+): domestic software dev immediate expense
#                       foreign software dev 15-yr amortization
# Rev Proc 2000-50 historical 3-yr software amortization superseded by 2022 mandatory cap

# Determine SRE vs non-SRE software activities:
software_activity_classification = {
    "new_software_development": "SRE",  # uncertainty in design / capability
    "major_feature_addition": "SRE if technical uncertainty",
    "ux_redesign": "Likely not SRE (no technical uncertainty)",
    "bug_fixes_post_launch": "Not SRE",
    "internal_tools_for_business_use": "SRE if novel tech; possibly excluded if "
                                       "Treas Reg 1.41-4(c)(6) internal-use test",
    "customer_onboarding": "Not SRE",
    "infrastructure_optimization": "SRE if performance / capability uncertainty",
}
```

### Recipe 8 — Coordinate with Section 41 R&D credit

```python
# Section 41 QRE definitions OVERLAP but NOT IDENTICAL to Section 174 SRE
# Differences:
#  - Section 174 SRE: broader; includes overhead allocation, supplies
#  - Section 41 QRE: narrower; tighter "qualified services" definition
#  - Section 41 contract research: 65% (Sec 174 = 100%)

# Often Section 41 QRE < Section 174 SRE
sec_174_sre = 861_000
sec_41_qre = 752_000  # subset of SRE meeting tighter Sec 41 four-part test
```

### Recipe 9 — State conformity to Section 174

```python
# States vary on Section 174 conformity:
STATE_174_CONFORMITY = {
    "CA": "Static — conforms to 2017 IRC; TCJA capitalization NOT adopted",
    "NY": "Rolling — conforms to current IRC; TCJA cap adopted",
    "TX": "No income tax; franchise margin tax follows IRS guidance",
    "WA": "No income tax",
    "FL": "Static — conforms to 2018; TCJA cap adopted",
    "PA": "Static; TCJA cap not adopted",
    "NJ": "Rolling; TCJA cap adopted",
    # ...
}
# CA: continue immediate expensing for state purposes; create state-federal diff
# NY: follows federal (cap pre-OBBB; expense post-OBBB)
```

### Recipe 10 — Section 174 long-term amortization tracker

```python
# Even with OBBB domestic reversal, foreign SRE amortizes 15 yrs
# Pre-OBBB domestic capitalizations continue amortizing
# Build multi-year amortization waterfall

amortization_schedule = pd.DataFrame({
    "tax_year": list(range(2025, 2041)),
    "domestic_2022_vintage_amort": [0]*4 + [144_000]*2 + [0]*10,  # 5-yr cleanly
    "domestic_2023_vintage_amort": [0]*3 + [170_000]*2 + [0]*11,
    "domestic_2024_vintage_amort": [0]*3 + [188_000]*2 + [0]*11,
    "foreign_2022_vintage_amort": [12_000]*14 + [0]*2,
    "foreign_2023_vintage_amort": [14_667]*15 + [0]*1,
    "foreign_2024_vintage_amort": [16_667]*16,
    "foreign_2025_vintage_amort": [10_617] + [21_233]*14 + [10_617],  # half-year first
    # ...
})
```

## Examples

### Example 1: SaaS startup, $2M R&D wages, all domestic, TY 2025

**Goal:** TY 2025 R&D wages $2M all in US; pre-OBBB capitalized 2022-2024 also active.

**Steps:**

1. Recipe 1: identify SRE per employee × project.
2. Recipe 2: 100% domestic.
3. Recipe 3: TY 2025 domestic SRE = $2M immediate expense (per OBBB).
4. Recipe 4: pre-OBBB capitalizations continue amortizing:
   - 2022 vintage: $720K × 1/5 = $144K (2 yrs left)
   - 2023 vintage: $850K × 1/5 = $170K (3 yrs left)
   - 2024 vintage: $940K × 1/5 = $188K (4 yrs left)
   - Total pre-OBBB amortization 2025: $502K
5. Total 2025 R&D deduction = $2M (current) + $502K (legacy amortization) = $2.502M.
6. Recipe 5: Form 3115 with Form 1120 TY 2025 for method change.
7. ASC 740: large DTA reversal from immediate expensing acceleration.

**Result:** $2.5M R&D deduction; method change documented; significant deferred tax acceleration benefit.

### Example 2: Mid-stage company with offshore dev team, TY 2025

**Goal:** $5M total R&D; $3.5M domestic + $1.5M EU dev team.

**Steps:**

1. Recipe 2: domestic $3.5M + foreign $1.5M.
2. Recipe 3: domestic immediate expense = $3.5M; foreign 15-yr amortization with half-year.
3. Foreign 2025 amortization = $1.5M / 15 / 2 = $50K.
4. Foreign capitalized EOY = $1.5M − $50K = $1.45M.
5. Future 14 years: foreign 2025 amortizes $100K/yr.
6. Pre-OBBB foreign capitalizations continue per their own schedule.
7. Section 174 + Section 41 alignment: only $3.5M domestic counts toward Section 41 QRE.
8. Strategic question: relocate foreign R&D to US to capture immediate expensing benefit.

**Result:** $3.5M immediate expense + $50K foreign amortization = $3.55M 2025 deduction; $1.45M foreign DTA created.

### Example 3: Pre-OBBB capitalized DTAs reversal in TY 2025 (no new R&D)

**Goal:** Company spending no new R&D 2025; legacy capitalized SREs continue amortizing.

**Steps:**

1. Pre-OBBB capitalizations from 2022-2024 (Recipe 4).
2. 2025 amortization deduction: $502K total (Recipe 4).
3. No method change needed if no current-year SREs.
4. DTAs on remaining capitalized basis continue draining.
5. ASC 740: DTA balance EOY 2025 = current cumulative amortization × tax rate.

**Result:** $502K deduction from legacy R&D amortization; no Form 3115 needed.

## Edge cases / gotchas

- **OBBB 2025 enacted July 2025; retroactive to TY 2025:** preparers issued guidance Q3-Q4 2025. Watch for additional IRS revenue procedures.
- **Domestic vs foreign location-of-activity:** activity location, not employer location. US employee performing work physically in Europe = foreign SRE.
- **Method change Form 3115 auto-consent:** Rev Proc 2022-14 expected to be amended for OBBB transition; auto-consent likely.
- **Section 481(a) adjustment:** prospective only (no catch-up) for OBBB transition; pre-OBBB capitalizations continue.
- **Foreign R&D still 15-yr:** OBBB did NOT change foreign R&D treatment. Strategic incentive to onshore R&D.
- **Section 41 R&D credit QRE vs Section 174 SRE definitional gap:** Section 41 has tighter "four-part test" (permitted purpose, technological in nature, eliminate technical uncertainty, process of experimentation). Section 174 broader.
- **Internal-use software Treas Reg 1.41-4(c)(6):** Section 41 high-threshold-of-innovation test for IUS. Section 174 = all software dev historically SRE per Rev Proc 2000-50 (now mandatory cap).
- **Allocated overhead:** Section 174 allows reasonable overhead allocation; Section 41 narrower.
- **Section 280C(c) interplay:** must elect (3) reduced credit OR reduce 174 deduction by credit. Both same net at 21% rate.
- **State conformity is patchwork:** CA / FL / PA static; NY / NJ rolling. Plan separately for state.
- **R&D-related fixed assets:** depreciation of equipment used in R&D = 174 SRE; not separately tracked under MACRS.
- **Patent legal fees:** qualify as SRE; both before and after grant.
- **Reverse engineering competitor product:** typically NOT SRE (no novel technical uncertainty for the engineer).
- **Quality control + market research:** explicitly excluded by Treas Reg 1.174-2(a)(6).
- **Acquired R&D in M&A:** stepped-up basis treated as IPR&D — separately amortized under Section 197 (15-yr) or capitalized per ASC 805 + 350.
- **Foreign tax credit on Subpart F GILTI inclusion** of CFC R&D expenses: complex interaction; CFC follows its own deduction rules but US shareholder bears GILTI ETR.
- **State 174 add-back: for static-conformity states** (CA, FL, PA), federal capitalized amount may differ; tax basis differs from federal.

> WARNING **This is informational guidance from an AI agent. Always consult a licensed CPA or tax attorney in your jurisdiction before filing returns, claiming credits, or implementing binding tax positions.**

## Sources

- IRC Section 174: https://www.law.cornell.edu/uscode/text/26/174
- Treas Reg 1.174-2: https://www.law.cornell.edu/cfr/text/26/1.174-2
- IRS Notice 2023-63 (Sec 174 guidance): https://www.irs.gov/pub/irs-drop/n-23-63.pdf
- IRS Rev Proc 2022-14 (method change auto-consent): https://www.irs.gov/pub/irs-drop/rp-22-14.pdf
- IRS Form 4562: https://www.irs.gov/forms-pubs/about-form-4562
- IRS Form 3115 (method change): https://www.irs.gov/forms-pubs/about-form-3115
- Fenwick & West — Section 174 OBBB update: https://www.fenwick.com/insights/publications/section-174-rd-capitalization-update-big-beautiful-bill
- AICPA Section 174 R&E: https://www.aicpa.org/topic/tax/section-174-research-experimental
- One Big Beautiful Bill Act: https://www.congress.gov/bill/119th-congress/house-bill/1
- TCJA 2017 Section 13206 (original Sec 174 amendment): https://www.congress.gov/bill/115th-congress/house-bill/1
- Rev Proc 2000-50 (software historical): https://www.irs.gov/pub/irs-tege/rp_2000-50.pdf

## Related skills

- `rd-tax-credit-form-6765-mainstreet-neo` — Section 41 R&D credit
- `form-1120-corp-income-tax-filing` — M-1/M-3 + Form 4562 + Form 3115
- `asc-740-tax-provision-deferred` — Sec 174 deferred tax
- `transfer-pricing-form-5471-8865-5472` — foreign R&D + cost sharing
- `nol-amt-multi-year-tax-planning` — NOL impact from Sec 174 reversal
