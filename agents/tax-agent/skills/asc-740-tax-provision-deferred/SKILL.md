<!--
Source: https://www.fasb.org/page/PageContent?pageId=/standards/asc740.html
Source: https://www.bloombergtax.com/tax-provision/
Source: https://tax.thomsonreuters.com/en/onesource/tax-provision
Source: https://www.irs.gov/forms-pubs/about-schedule-utp-form-1120
Reference role.md: "ASC 740 tax provision"
-->

# ASC 740 — Income tax provision (current + deferred + UTP)

Five-step ASC 740 process: (1) book → taxable income (Schedule M-1/M-3); (2) current tax payable; (3) deferred tax assets/liabilities per temp diff; (4) valuation allowance assessment; (5) uncertain tax positions (FIN 48 / ASC 740-10). Software: Bloomberg Tax Provision (CorpTax), ONESOURCE Tax Provision, Longview Tax, Tax Prodigy (SMB). Effective Tax Rate (ETR) reconciliation. Pillar 2 disclosure (post-2024).

## When to use

- Quarterly or annual book tax provision for GAAP / IFRS reporting.
- Year-end deferred tax schedule preparation.
- Valuation allowance assessment for NOLs / R&D credit DTAs.
- Uncertain Tax Position (UTP / FIN 48) reserve documentation.
- ETR roll-forward for board / audit committee reporting.
- Stock comp deferred tax impact (ASC 718 + ASU 2016-09 windfall accounting).
- Pillar 2 ASC 740 disclosure (post-2024).
- Trigger phrases: "ASC 740", "tax provision", "deferred tax", "DTA", "DTL", "valuation allowance", "VA", "UTP", "FIN 48", "ETR", "effective tax rate", "Schedule M-1", "Schedule M-3", "Bloomberg Tax Provision", "ONESOURCE Tax Provision".

NOT for: actual tax return filing (use `form-1120-corp-income-tax-filing`); R&D credit calculation (use `rd-tax-credit-form-6765-mainstreet-neo`); Section 174 mechanics (use `sec-174-rd-capitalization`); CAMT calculation (use `nol-amt-multi-year-tax-planning`).

## Setup

### Bloomberg Tax Provision (formerly CorpTax)

```bash
# Enterprise market leader
export BLOOMBERGTAX_API_KEY="..."
curl -H "Authorization: Bearer $BLOOMBERGTAX_API_KEY" \
  https://api.bloombergtax.com/v1/provision/companies
```

### ONESOURCE Tax Provision (Thomson Reuters)

```bash
export ONESOURCE_API_KEY="..."
curl -H "Authorization: Bearer $ONESOURCE_API_KEY" \
  https://onesource.thomsonreuters.com/api/v1/tax-provision
```

### Longview Tax (insightsoftware)

```bash
# Enterprise multi-entity consolidated provision
# https://insightsoftware.com/longview/
```

### Tax Prodigy (SMB)

```bash
# Cost-effective for sub-enterprise corps
# https://www.taxprodigy.com/
export TAXPRODIGY_API_KEY="..."
curl -H "Authorization: Bearer $TAXPRODIGY_API_KEY" \
  https://api.taxprodigy.com/v1/provisions
```

## Common recipes

### Recipe 1 — Book → taxable income (Schedule M-1)

```python
# Step 1 of ASC 740: identify permanent + temporary differences
import pandas as pd

book_pretax = 6_200_000  # from GL P&L

m1_perm = pd.DataFrame([
    {"line": "50% meals disallowed", "amount": 18_500},
    {"line": "Entertainment 100% disallowed", "amount": 4_200},
    {"line": "Fines + penalties", "amount": 8_500},
    {"line": "Tax-exempt muni interest", "amount": -12_000},
    {"line": "Federal income tax per books (added back)", "amount": 0},
])

m1_temp = pd.DataFrame([
    {"line": "Stock comp book vs tax", "amount": 385_000},
    {"line": "Depreciation book vs tax", "amount": -125_000},
    {"line": "Sec 174 R&D capitalization", "amount": -240_000},
    {"line": "Accrued PTO", "amount": 28_000},
    {"line": "Bad debt reserve", "amount": 15_000},
    {"line": "Deferred revenue book vs tax (ASC 606)", "amount": -180_000},
])

taxable_income = book_pretax + m1_perm.amount.sum() + m1_temp.amount.sum()
```

### Recipe 2 — Current tax provision

```python
# Federal current tax
federal_taxable = taxable_income  # = 6,084,000
federal_rate = 0.21
federal_current = federal_taxable * federal_rate  # = 1,277,640

# State current tax (apportioned)
state_taxable_apportioned = {
    "CA": federal_taxable * 0.35 * 0.0884,   # 35% sales-factor apportion, 8.84% rate
    "NY": federal_taxable * 0.15 * 0.0725,   # 15% / 7.25%
    "TX": federal_taxable * 0.20 * 0.00375,  # 20% / 0.375% franchise margin
    "WA": federal_taxable * 0.10 * 0.00484,  # 10% / 0.484% B&O
}
state_current = sum(state_taxable_apportioned.values())

# Foreign current tax (CFCs from Form 5471 inclusions)
foreign_current = 0  # GILTI / Subpart F at federal level
```

### Recipe 3 — Deferred tax schedule per temp diff

```python
# DTA / DTL per temp diff × statutory rate
# Federal 21% + blended state rate

blended_state_rate = 0.045  # weighted-avg post-federal-benefit
combined_rate = 0.21 + blended_state_rate * (1 - 0.21)  # = 25.6%

temp_diffs_at_eoy = pd.DataFrame([
    {"item": "Stock comp", "boy_tax_basis": 1_200_000, 
     "eoy_tax_basis": 1_585_000, "boy_book_basis": 0, 
     "eoy_book_basis": 0, "type": "DTA"},
    {"item": "Sec 174 R&D unamortized", "boy_tax_basis": 950_000,
     "eoy_tax_basis": 1_140_000, "boy_book_basis": 0,
     "eoy_book_basis": 0, "type": "DTA"},
    {"item": "Depreciation (book < tax)", "boy_tax_basis": 2_400_000,
     "eoy_tax_basis": 2_525_000, "boy_book_basis": 2_700_000,
     "eoy_book_basis": 2_945_000, "type": "DTA"},
    {"item": "NOL carryforward", "boy_tax_basis": 0,
     "eoy_tax_basis": 1_240_000, "boy_book_basis": 0,
     "eoy_book_basis": 0, "type": "DTA"},
    {"item": "Deferred revenue book < tax", "boy_tax_basis": 0,
     "eoy_tax_basis": 0, "boy_book_basis": 180_000,
     "eoy_book_basis": 280_000, "type": "DTA"},
    {"item": "Accrued PTO", "boy_tax_basis": 0,
     "eoy_tax_basis": 0, "boy_book_basis": 95_000,
     "eoy_book_basis": 123_000, "type": "DTA"},
])

temp_diffs_at_eoy["temp_diff_eoy"] = (
    temp_diffs_at_eoy.eoy_book_basis - temp_diffs_at_eoy.eoy_tax_basis
)
temp_diffs_at_eoy["dta_dtl_eoy"] = (
    temp_diffs_at_eoy.temp_diff_eoy * combined_rate
)

gross_dta = temp_diffs_at_eoy[temp_diffs_at_eoy.dta_dtl_eoy < 0].dta_dtl_eoy.sum() * -1
gross_dtl = temp_diffs_at_eoy[temp_diffs_at_eoy.dta_dtl_eoy > 0].dta_dtl_eoy.sum()
```

### Recipe 4 — Valuation allowance assessment

```python
# ASC 740-10-30-18: record VA against DTA if "more likely than not" 
# (>50%) cannot realize.
# Four sources of taxable income to consider:
#  1. Future reversals of taxable temp differences
#  2. Future taxable income exclusive of reversals
#  3. Taxable income in carryback period (limited; mostly N/A post-TCJA)
#  4. Tax planning strategies (must be PRUDENT + FEASIBLE)

# Cumulative loss in 3-year window = significant negative evidence
# Section 382 limit = significant negative evidence

cumulative_pretax_loss_3yr = -2_400_000 + 850_000 + 4_200_000  # = +2.65M
# Cumulative income → less negative evidence

projected_future_income_5yr = [4_500_000, 5_200_000, 6_000_000, 6_800_000, 7_500_000]
gross_dta_eoy = 1_240_000

# NOL DTA expected to be realized via projected income → no VA
va_required = 0

if gross_dta_eoy > sum(projected_future_income_5yr) * combined_rate:
    va_required = gross_dta_eoy - sum(projected_future_income_5yr) * combined_rate
```

### Recipe 5 — UTP (Uncertain Tax Position) FIN 48 reserve

```python
# Two-step recognition:
#  Step 1: more-likely-than-not (>50%) that position will be sustained
#          on examination based on technical merits
#  Step 2: measure at largest amount with >50% likelihood of being realized
#          upon ultimate settlement

utp_positions = [
    {
        "id": "UTP-2026-001",
        "description": "R&D credit qualification — cloud infrastructure team",
        "irc_section": "Sec 41(d)",
        "tax_benefit_claimed": 165_000,
        "step_1_more_likely_than_not": True,  # >50% on merits
        "step_2_settlement_likely": 0.65,     # 65% of claimed amount
        "fin_48_reserve": 165_000 * (1 - 0.65),  # = 57,750
        "expected_resolution": "On audit / by 2028",
        "interest_at_eoy": 4_200,
        "penalty_at_eoy": 0,
    },
    # ...
]
# Schedule UTP (Form 1120 Schedule UTP) discloses positions ranked by size 
# for $10M+ asset corps
```

### Recipe 6 — Effective Tax Rate (ETR) reconciliation

```python
# ETR = total tax expense / pretax book income
# Reconcile to statutory rate

statutory_rate = 0.21
etr_recon = pd.DataFrame([
    {"line": "Federal statutory rate", "rate": 0.21,
     "amount": book_pretax * 0.21},
    {"line": "State tax (net of federal benefit)", "rate": 0.045,
     "amount": book_pretax * 0.045},
    {"line": "R&D credit (permanent benefit)", "rate": -0.02,
     "amount": -127_000},
    {"line": "Foreign rate differential (GILTI)", "rate": 0.005,
     "amount": 32_000},
    {"line": "Stock comp shortfall / windfall", "rate": -0.008,
     "amount": -48_000},
    {"line": "50% meals + other perm diffs", "rate": 0.001,
     "amount": 8_500},
    {"line": "Change in VA", "rate": 0.000, "amount": 0},
    {"line": "UTP reserve increase", "rate": 0.001,
     "amount": 12_000},
])

total_tax_expense = etr_recon.amount.sum()
etr = total_tax_expense / book_pretax
print(f"Total tax expense: ${total_tax_expense:,.0f} | ETR: {etr:.1%}")
```

### Recipe 7 — Stock comp deferred tax (ASC 718 + ASU 2016-09)

```python
# Book: Expense FV at grant; recognize over vesting period (ASC 718)
# Tax: Deduction = intrinsic value at exercise (NSO) OR at vesting (RSU)
# Pre-ASU 2016-09: APIC pool tracked windfalls/shortfalls
# Post-ASU 2016-09 (2017+): all windfalls/shortfalls hit P&L

# Calculation per grant:
grant = {
    "type": "RSU",
    "shares": 5_000,
    "grant_date_fv": 8_000_000,    # FV at grant per ASC 718
    "vest_date_fv": 11_500_000,    # FV at vesting (tax deduction)
    "book_expense_cumulative": 8_000_000,
    "tax_deduction_at_vest": 11_500_000,
}
windfall_at_vest = (grant["tax_deduction_at_vest"] 
                    - grant["book_expense_cumulative"]) * combined_rate
# Windfall = 11.5M - 8.0M = 3.5M × 25.6% = 896K tax benefit (current-year P&L)
```

### Recipe 8 — Foreign provision (GILTI / Subpart F / FDII)

```python
# GILTI: included in US TI; Section 250 deduction 50% (37.5% post-2025)
# Subpart F: included in US TI; full inclusion (no deduction)
# FDII: 37.5% deduction (21.875% post-2025) — special deduction for foreign sales

gilti_inclusion = 765_000
sec_250_gilti_deduction = gilti_inclusion * 0.50  # = 382,500
gilti_taxable = gilti_inclusion - sec_250_gilti_deduction  # = 382,500
gilti_federal_tax = gilti_taxable * 0.21  # = 80,325
# FTC for foreign tax paid on GILTI (80% with haircut)

# Year-end Section 250 deduction sunset alert:
# Post-2025: GILTI deduction 37.5%; FDII deduction 21.875%
# Build deferred tax impact of rate change
```

### Recipe 9 — Pillar 2 ASC 740 disclosure (post-2024)

```python
# ASC 740-10-50 (amended for Pillar 2):
# Required disclosures:
#  - Description of Pillar 2 legislation enacted in jurisdictions
#  - Estimated top-up tax exposure (or statement that it's not material)
#  - Material elections (transitional CbCR safe harbor, SBIE, etc.)

pillar_2_disclosure = """
The OECD's Pillar Two model rules have been enacted in [Ireland, Germany, UK, 
Singapore] effective January 1, 2024. The Company's effective tax rate in 
[Ireland] is below the 15% global minimum, resulting in estimated top-up tax 
of $X.X million for the year ended December 31, 2026. The Company applies 
the transitional CbCR safe harbor in [Germany, France, UK] for this period.
"""

# Deferred tax exception under ASC 740-10-30-25(b):
# No deferred tax accounting for Pillar 2 (similar to IAS 12 amendment)
```

### Recipe 10 — Roll-forward + reconciliation packet for auditors

```python
# Year-end tax provision packet (auditor PBC):
audit_packet = {
    "1_book_to_tax_recon": "Schedule M-1 / M-3 workpaper",
    "2_current_tax_calc": "Federal + state + foreign",
    "3_deferred_tax_schedule": "Per temp diff × rate × VA",
    "4_va_assessment": "Memo + positive/negative evidence",
    "5_utp_log": "FIN 48 positions with technical analysis + reserves",
    "6_etr_recon": "Statutory to effective + variance commentary",
    "7_pillar_2_assessment": "If applicable",
    "8_stock_comp_dt": "ASC 718 windfall / shortfall",
    "9_apportionment": "State apportionment workpaper",
    "10_disclosure_footnote": "10-K / 10-Q income tax footnote draft",
}
```

## Examples

### Example 1: Profitable mid-stage SaaS, first-year provision

**Goal:** $45M revenue C-corp, $6.2M book pretax, first ASC 740 provision.

**Steps:**

1. Recipe 1: M-1 reconciliation → taxable income $6.084M.
2. Recipe 2: federal current $1.28M + state current $215K = $1.49M current.
3. Recipe 3: build deferred tax schedule:
   - Stock comp DTA: $385K × 25.6% = $98K
   - Sec 174 DTA: $1.14M × 25.6% = $292K
   - Depr DTA: $420K × 25.6% = $108K
   - NOL DTA (from prior $2.17M loss carryforward): $554K
   - PTO DTA: $123K × 25.6% = $31K
   - Total gross DTA: $1.08M
4. Recipe 4: VA assessment → projected future income $20M+ → no VA.
5. Recipe 5: UTP — none material (no aggressive positions).
6. Recipe 6: ETR recon → 23.5% effective vs 21% statutory.
7. Recipe 10: PBC packet for Big4 auditor.

**Result:** Current + deferred tax recorded; ETR 23.5%; clean audit.

### Example 2: Pre-revenue loss-stage startup with VA on NOL DTA

**Goal:** Series A startup, $8M cumulative NOLs, no near-term profitability.

**Steps:**

1. Recipe 1: M-1 → taxable loss $2.5M.
2. Recipe 2: current tax = 0.
3. Recipe 3: NOL DTA = $8M × 25.6% = $2.05M; stock comp DTA = $150K; total $2.2M.
4. Recipe 4: VA assessment:
   - Cumulative 3-yr loss = significant negative evidence
   - Projected 3-yr profitability uncertain
   - No tax planning strategy → full VA on NOL DTA
5. Net DTA = $0; total tax expense = $0.
6. Recipe 6: ETR = 0% (vs 21% statutory); reconciled via VA establishment.
7. Future: each year reassess VA; partial release once cumulative profitability achieved.

**Result:** Full VA on NOL DTA; $0 net tax expense; clean disclosure.

### Example 3: Mature pre-IPO, partial VA release year

**Goal:** $35M revenue, third consecutive profitable year, $4M NOLs remaining.

**Steps:**

1. Recipe 1-3: standard provision; NOL DTA $1.02M (4M × 25.6%).
2. Recipe 4: VA assessment:
   - Cumulative income last 3 years positive
   - Projected 3-yr income covers DTA recovery
   - Release VA: $1.02M VA → $0
3. Tax expense includes $1.02M benefit from VA release (one-time).
4. Recipe 6: ETR drops materially due to VA release; disclose as discrete item.
5. PBC packet documents VA release rationale (positive evidence outweighs negative).

**Result:** VA released; one-time benefit to ETR; reconciliation discloses driver.

## Edge cases / gotchas

- **Realizability "more likely than not" >50%:** subjective; requires weighing positive (income trends, contracts, tax planning) vs negative (cumulative loss, expiring NOL, Section 382 limit).
- **Cumulative loss in 3-year window = significant negative evidence** for VA. Strong rebuttal needed (e.g., known turnaround event).
- **Section 382 limit drives VA on pre-change NOLs:** if annual limit × remaining life < gross NOL → partial VA.
- **Stock comp ASU 2016-09 windfall/shortfall:** all in income tax expense, not equity. Volatility in ETR.
- **Bargain Element ISO vs DT:** ISO no deduction at exercise → no DT until disqualifying disposition (NSO treatment).
- **GILTI rate change post-2025:** Section 250 deduction drops from 50% to 37.5%; deferred tax impact of rate change accrues in year of enactment.
- **R&D credit deferred tax:** carryforward = DTA; usable subject to GBC limit + statute.
- **FIN 48 / ASC 740-10:** reserve = tax benefit claimed × (1 − probability of sustainment). Interest + penalties added at applicable rate.
- **Schedule UTP (Form 1120):** required for $10M+ asset C-corps with FIN 48 reserves; rank positions by size.
- **Indefinite reinvestment assertion (APB 23):** if asserting permanent reinvestment of foreign sub earnings, no DT on outside basis. Hard to support post-TCJA territorial regime.
- **Pillar 2 deferred tax exception:** ASC 740-10-30-25(b) (and IAS 12 amendment) exempt Pillar 2 from deferred tax recognition.
- **Tax rate change in enacted legislation:** revalue DTAs/DTLs in period of enactment. Hits ETR in that period.
- **Interim period (quarterly) provision:** use estimated annual ETR applied to YTD pretax income; discrete items recorded in period.
- **Change in VA = discrete or estimated annual ETR item:** ASC 740-270 paragraph 25 nuances.
- **Net operating loss carryforward useful life vs realizability:** indefinite NOLs (post-2018) easier to support realizability if reasonable taxable income projected.
- **Section 174 capitalization creates large DTAs:** TCJA 2017 R&D capitalization → 5-yr amortization → temp diff. OBBB 2025 reversed for domestic → reversing DTAs at enactment.
- **Equity-classified vs liability-classified stock comp:** different DT treatments.
- **PTET (Pass-Through Entity Tax) workaround:** state PTE tax paid at entity level — DT not applicable but reduce ETR.
- **Audit-ready M-1 / M-3 reconciliation** documents temp + perm diffs per line; Big4 always asks.

> WARNING **This is informational guidance from an AI agent. Always consult a licensed CPA or tax attorney in your jurisdiction before filing returns, claiming credits, or implementing binding tax positions.**

## Sources

- FASB ASC 740: https://www.fasb.org/page/PageContent?pageId=/standards/asc740.html
- FASB ASC 740-10 (FIN 48 / UTP): https://asc.fasb.org/740/740-10
- FASB ASU 2016-09 (Stock Comp): https://www.fasb.org/page/PageContent?pageId=/standards/list-of-asus/asu-2016-09.html
- IRS Schedule UTP: https://www.irs.gov/forms-pubs/about-schedule-utp-form-1120
- Bloomberg Tax Provision: https://www.bloombergtax.com/tax-provision/
- ONESOURCE Tax Provision: https://tax.thomsonreuters.com/en/onesource/tax-provision
- Longview Tax: https://insightsoftware.com/longview/
- Tax Prodigy: https://www.taxprodigy.com/
- IFRS IAS 12 Income Taxes: https://www.ifrs.org/issued-standards/list-of-standards/ias-12-income-taxes/
- ASC 740 Pillar 2 amendment: https://www.fasb.org/page/PageContent?pageId=/news-and-meetings/news-releases/asc-740-pillar-two-amendment.html
- AICPA Income Tax Accounting: https://www.aicpa.org/topic/audit/accounting-for-income-taxes

## Related skills

- `form-1120-corp-income-tax-filing` — M-1/M-3 + return preparation
- `nol-amt-multi-year-tax-planning` — NOL waterfall + Section 382 + CAMT
- `rd-tax-credit-form-6765-mainstreet-neo` — R&D credit DTA
- `sec-174-rd-capitalization` — Section 174 capitalization DTA mechanics
- `iso-nso-rsu-employee-tax-treatment` — Stock comp deferred tax
- `pillar-2-globe-cbcr-international` — Pillar 2 ASC 740 disclosure
- `state-apportionment-nexus-analysis` — state tax current + DT
