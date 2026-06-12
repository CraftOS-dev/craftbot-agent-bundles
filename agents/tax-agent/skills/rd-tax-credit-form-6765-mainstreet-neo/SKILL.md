<!--
Source: https://www.irs.gov/forms-pubs/about-form-6765
Source: https://mainstreet.com/
Source: https://neo.tax/
Source: https://striketax.com/
Source: https://www.irs.gov/forms-pubs/about-form-8974
Reference role.md: "R&D credit Form 6765"
-->

# R&D tax credit — Form 6765 + MainStreet / Neo Tax / Strike Tax

Section 41 federal R&D credit calculation + claim. Regular method or Alternative Simplified Credit (ASC = 14% of QREs > 50% of avg prior 3 yrs). Section 41(h) payroll-tax offset election for qualified small businesses (post-OBBB 2025: $500K cap, raised from $250K). State R&D credits in CA, MA, NY, TX, etc. Software: MainStreet (10-20% of QRE wages back, $300K min credit threshold), Neo Tax (AI-first), Strike Tax (managed), TaxRobot.

## When to use

- Annual R&D credit claim via Form 6765 attached to Form 1120 / 1065 / 1120-S.
- Section 41(h) payroll-tax offset election for QSB (gross receipts < $5M; < 5 years revenue history).
- ASC (Alternative Simplified Credit) calculation if regular method base year data unavailable.
- State R&D credit stacking (CA, MA, NY, TX, AZ, others).
- Multi-year R&D credit carryforward management.
- Section 174 R&D capitalization interplay (see also `sec-174-rd-capitalization`).
- Section 280C(c)(3) reduced credit election.
- Trigger phrases: "R&D credit", "Form 6765", "Section 41", "QRE", "MainStreet", "Neo Tax", "Strike Tax", "ASC method", "payroll-tax offset", "Form 8974", "Section 280C".

NOT for: Section 174 capitalization mechanics (use `sec-174-rd-capitalization`); R&D book vs tax temp diff (use `asc-740-tax-provision-deferred`); state R&D credit deep-dive (covered here).

## Setup

### MainStreet (most popular for startups)

```bash
# MainStreet: full-service automated R&D credit + claim
# https://mainstreet.com/
# Pricing: 20% of credit captured OR flat fee
# Pulls payroll from Gusto/Rippling, accounting from Xero/QBO
export MAINSTREET_API_KEY="..."
curl -H "Authorization: Bearer $MAINSTREET_API_KEY" \
  https://api.mainstreet.com/v1/companies
```

### Neo Tax (AI-first)

```bash
# Neo Tax: AI-driven R&D credit claim
# https://neo.tax/
export NEOTAX_API_KEY="..."
curl -H "Authorization: Bearer $NEOTAX_API_KEY" \
  https://api.neo.tax/v1/claims
```

### Strike Tax Advisory (managed service)

```bash
# Strike: white-glove R&D credit; managed CPA service
# https://striketax.com/
# No public API; engagement via account manager
```

### TaxRobot (DIY)

```bash
# https://www.taxrobot.com/
# DIY platform for R&D credit; cheaper than MainStreet/Neo
```

## Common recipes

### Recipe 1 — Qualified Research Expenses (QRE) identification

```python
# Four-part test (Section 41(d) qualified research):
#  1. Permitted purpose (new/improved product, process, software, formula)
#  2. Technological in nature (relies on hard sciences)
#  3. Elimination of technical uncertainty (capability, methodology, design)
#  4. Process of experimentation (systematic evaluation of alternatives)

# QRE categories (Section 41(b)):
#  - Wages for qualified services (Section 41(b)(2)(B) "qualified services"):
#    direct supervision, direct support, direct conduct of research
#  - Supplies used and consumed in research
#  - 65% of contract research expenses paid to 3rd parties
#  - 100% of contract research to qualified research consortia / universities

qualifying_employee_breakdown = {
    "engineer_alice": {
        "salary": 220_000,
        "rd_allocation_pct": 0.85,  # 85% time on qualifying R&D
        "qre_wages": 187_000,
    },
    "engineer_bob": {
        "salary": 180_000,
        "rd_allocation_pct": 1.00,
        "qre_wages": 180_000,
    },
    "ceo_carol": {
        "salary": 280_000,
        "rd_allocation_pct": 0.15,  # only direct supervision time
        "qre_wages": 42_000,
    },
}
```

### Recipe 2 — Alternative Simplified Credit (ASC) calculation

```python
# ASC method = 14% × (QRE_current_year - 50% × avg_QRE_prior_3_years)
# If no QREs in prior 3 years: ASC = 6% × QRE_current_year
import pandas as pd

current_year_qre = 1_240_000
prior_3yr_qre = [892_000, 750_000, 615_000]  # 3 yrs back to most recent
avg_prior_3 = sum(prior_3yr_qre) / 3 if all(prior_3yr_qre) else 0

if avg_prior_3 == 0:
    asc_credit = 0.06 * current_year_qre
else:
    base_amount = 0.50 * avg_prior_3
    asc_credit = max(0, 0.14 * (current_year_qre - base_amount))

print(f"ASC credit: ${asc_credit:,.0f}")
```

### Recipe 3 — Regular method (rare; complex base-period requirement)

```python
# Regular method = 20% × (current QRE − base amount)
# Base amount = fixed-base % × avg gross receipts (most recent 4 yrs)
# Fixed-base % = QRE/gross receipts ratio for 1984-1988 (or first 5 yrs)
# Most modern startups use ASC for simplicity.

fixed_base_pct = 0.045  # only meaningful if you have 1984-1988 records
avg_gross_receipts_4yr = 18_500_000
base_amount = fixed_base_pct * avg_gross_receipts_4yr
regular_credit = max(0, 0.20 * (current_year_qre - base_amount))
```

### Recipe 4 — Section 41(h) payroll-tax offset election (QSB)

```python
# Qualified Small Business (QSB) requirements (Section 41(h)):
#  - Gross receipts < $5M for current year
#  - 5 or fewer years of gross receipts > $0 (history)
# Election made on TIMELY-filed (incl ext) Form 1120/1065/1120-S Form 6765

# OBBB 2025: cap raised to $500K (was $250K under IRA 2022)
gross_receipts_2025 = 4_200_000
years_with_receipts = 4  # since first $1 of revenue
qsb_eligible = gross_receipts_2025 < 5_000_000 and years_with_receipts <= 5

if qsb_eligible:
    rd_credit_total = 365_000
    payroll_offset_election = min(rd_credit_total, 500_000)  # post-OBBB
    # Applied via Form 8974 each quarter on Form 941 line 11a
```

### Recipe 5 — Form 8974 quarterly payroll offset

```python
# Election effective starting first quarter AFTER 1120 filing
# Example: file 1120 in October 2026 → first offset quarter = Q4 2026 941
# Filed late March 2027.

form_8974 = {
    "rd_credit_elected": 200_000,
    "quarter": "2026Q4",
    "form_941_line_11a_offset": min(quarterly_employer_ss_portion, 200_000),
    "remaining_balance_carryforward": 200_000 - 11a_used_qtr,
}

# Carries forward indefinitely until consumed
# Cannot reduce employer SS below zero
```

### Recipe 6 — Section 280C(c)(3) reduced credit election

```python
# Default: must reduce R&D wage deduction (Section 174) by credit amount
#   (eliminates double-benefit)
# Election under 280C(c)(3): take credit reduced by max corp tax rate
#   instead of reducing wage deduction
# Reduced credit = credit × (1 - 0.21) = credit × 0.79

full_credit = 365_000
section_280c_reduced_credit = full_credit * (1 - 0.21)  # = 288,350
# Net benefit: take reduced credit, keep full wage deduction
# Better than full credit + reduced deduction in some cases
# (depends on whether already in NOL)
```

### Recipe 7 — State R&D credit stacking

```python
# Major state R&D credits (2026):
STATE_RD_CREDITS = {
    "CA": {
        "rate_above_base": 0.15,  # 15% incremental
        "asc_alt": 0.0124,  # 1.24% on QRE (basic credit)
        "refundable": False,
        "carryforward_yrs": "indefinite",
    },
    "MA": {
        "rate": 0.10,  # 10% on QRE > 50% prior 3 yr avg
        "refundable": False,
        "carryforward_yrs": 15,
    },
    "NY": {
        "rate_qetc": 0.09,  # Qualified Emerging Tech Companies
        "rate_standard": 0.06,
        "refundable": True,  # NY refundable up to $200K
    },
    "TX": {
        "rate": 0.05,  # franchise tax credit
        "refundable": False,
        "carryforward_yrs": 20,
    },
    "AZ": {
        "rate_first_2_5m": 0.24,  # 24% first $2.5M
        "rate_above": 0.15,
        "refundable": True,  # if Univ ASU collab
    },
}
```

### Recipe 8 — Project log + nexus to QRE

```python
# IRS scrutinizes "what's the project, what was the uncertainty"
# Build project log per qualifying R&D project:
projects = [
    {
        "project_id": "RD-2025-001",
        "name": "Real-time ML inference pipeline",
        "uncertainty": "Could distributed inference achieve <100ms p99 latency"
                        " across heterogeneous GPU types?",
        "experimentation": "Tested 4 architectures, measured latency / cost,"
                            " iterated on quantization, ablated kernel fusion",
        "engineers_allocated": ["alice", "bob"],
        "wages_allocated": 245_000,
        "contractors": 30_000 * 0.65,  # 65% of contract research
        "supplies": 8_400,
    },
    # ...
]
```

### Recipe 9 — Form 6765 Section G (mandatory 2025+ for $1.5M+ QRE)

```python
# IRS Form 6765 revised 2024 (effective TY 2024+):
# Section G: project-level reporting MANDATORY for credit claims $1.5M+
# Required disclosures per project:
#  - Project ID
#  - Information sought
#  - Officer(s) involved
#  - Methodologies tested
#  - Types of evidence retained
#  - Functions performed
# For < $1.5M credit: optional but recommended

# Most preparer software (MainStreet, Neo) auto-populates Section G
```

### Recipe 10 — Multi-year R&D credit carryforward

```python
# Federal R&D credit carries forward 20 years (Section 39)
# State varies (CA, MA, TX = indefinite or 15-20 yrs)
import pandas as pd

carryforward_register = pd.DataFrame([
    {"vintage_year": 2021, "remaining": 84_500, "expires": 2041},
    {"vintage_year": 2022, "remaining": 142_000, "expires": 2042},
    {"vintage_year": 2023, "remaining": 215_000, "expires": 2043},
    {"vintage_year": 2024, "remaining": 248_000, "expires": 2044},
    {"vintage_year": 2025, "remaining": 365_000, "expires": 2045},
])
# Use FIFO (oldest first)
# Net out current-year credit against current-year tax first, then carryforward
```

## Examples

### Example 1: Pre-revenue Seed startup, $1.8M payroll, electing payroll offset

**Goal:** $0 revenue (pre-product), $1.8M total payroll, $1.4M to engineers.

**Steps:**

1. Qualifying R&D: 8 engineers × avg 90% time R&D = ~$1.26M QRE wages.
2. Supplies + cloud / GPU spend allocable to R&D: $185K (segregated lab/dev).
3. Contract research (offshore dev): $80K × 65% = $52K.
4. Total QRE = $1,497,000.
5. ASC method (no prior 3-yr QRE since first-year revenue scenario): 6% × $1,497K = $89,820.
6. QSB eligible (< $5M revenue, < 5 yr history) → elect Section 41(h) payroll offset.
7. Cap = $89,820 (well under $500K cap).
8. Form 6765 + Form 8974 attached to 1120; first offset quarter Q3 2026.
9. MainStreet engagement fee 20% = $17,964.

**Result:** $89,820 R&D credit offsetting employer SS payroll tax; net cash recovery ~$72K after fees.

### Example 2: Series A SaaS, $3.5M revenue, $4.5M R&D spend

**Goal:** Established R&D process, 22 engineers, established prior 3-yr QRE base.

**Steps:**

1. Project log: 6 projects with documented uncertainty + experimentation (Recipe 8).
2. Wages: $2,580K (22 × $145K avg salary × 81% R&D avg).
3. Supplies: $290K (cloud infra used in dev/test).
4. Contracts: $620K × 65% = $403K.
5. Total QRE = $3,273K.
6. ASC: prior 3-yr avg = $2.6M; base = 50% × $2.6M = $1.3M; credit = 14% × ($3.273M − $1.3M) = $276K.
7. QSB ($3.5M < $5M; 3-yr revenue history) → elect payroll offset for $276K.
8. Form 6765 Section G required (>$1.5M QRE) → project-level reporting.
9. State CA R&D credit: 15% on incremental + 1.24% on QRE = ~$45K state credit.
10. Total federal + state = $321K.

**Result:** $276K federal payroll offset (3-4 quarters of Form 8974) + $45K CA credit.

### Example 3: Mature C-corp, $80M revenue, full federal income tax credit

**Goal:** Profitable C-corp, R&D credit reduces income tax (not payroll offset; not QSB).

**Steps:**

1. R&D credit $1.2M qualifying.
2. NOT QSB ($80M revenue > $5M).
3. Apply as general business credit against federal tax line 5(a) Form 1120.
4. Section 280C election: reduced credit $1.2M × 0.79 = $948K (keeps full wage deduction).
5. Compare: full credit $1.2M but reduce wage deduction by $1.2M; impact on taxable income = $1.2M × 21% = $252K... reduced credit $948K net = +$948K vs full $1.2M − $252K = $948K. Same.
6. Section 280C wash: typically wash if at top corp rate.
7. Credit limited to general business credit limit (25% of net tax over $25K).

**Result:** $1.2M credit reducing federal corp tax liability.

## Edge cases / gotchas

- **Section 174 capitalization interplay:** R&D credit (Section 41) qualifying activities largely overlap Section 174 R&E expenditures. Section 174 mandates capitalization+amortization 2022+. OBBB 2025 restored immediate expensing for DOMESTIC R&D only; foreign R&D still 15-yr.
- **Form 6765 Section G project reporting:** mandatory for credit claims $1.5M+ starting TY 2024. Big shift — auditors now demand project-level granularity.
- **Section 41(h) QSB election:** must be made on TIMELY (incl ext) original return. Cannot amend later.
- **OBBB 2025 raises payroll offset cap to $500K** (was $250K under IRA 2022); previously $250K; pre-IRA (2016+) was $250K.
- **Section 280C reduced-credit election:** elect on Form 6765 line 17. Without election, must reduce R&D wage deduction by credit (creates phantom income, same net effect at 21% corp rate).
- **General business credit limit (Section 38):** R&D credit + other GBC capped at sum of net regular tax + AMT minus $25K, but no less than 25% of tax above $25K. Excess carries forward.
- **AMT release Section 38(c)(4):** post-2015, R&D credit can offset AMT for eligible small businesses (< $50M avg gross receipts).
- **Form 6765 Section A vs B:** Section A = Regular Method; Section B = ASC. Can't elect both same year — pick best.
- **Direct supervision wages:** CEO/VP overseeing R&D engineers qualify but allocate only direct supervision time. IRS skeptical of 100% allocations.
- **Routine engineering NOT qualifying:** bug fixes, routine maintenance, post-launch tweaks do NOT qualify. Only resolving technical uncertainty in design phase.
- **Funded research exclusion:** if research is "funded" (paid for by customer or grant), it's the FUNDER's research, not yours. Look at contract terms — risk + rights determine.
- **Software for internal use** (Treas Reg 1.41-4(c)(6)): 3-part high-threshold-of-innovation test → most SaaS / internal-tools R&D excluded UNLESS for sale/license to 3rd parties.
- **Contract research 65% rule:** only 65% of payments to third-party contractors count as QRE. 100% for qualified research consortia / 501(c)(3) universities.
- **State R&D credit refundability:** CA, NY (QETC) partially refundable; most others non-refundable carryforward.
- **Section 41(c)(7) controlled group aggregation:** all members of controlled group (>50% common ownership) aggregate QREs + gross receipts for QSB test + credit calc.
- **IRS sampling methodology:** IRS scrutinizes wage allocation methodologies. Surveys vs contemporaneous timekeeping; project-level rather than role-level allocation preferred.
- **R&D capitalization audit risk** (Section 174): IRS will increasingly examine Section 174 amortization schedules; OBBB 2025 reversal added complexity.

> WARNING **This is informational guidance from an AI agent. Always consult a licensed CPA or tax attorney in your jurisdiction before filing returns, claiming credits, or implementing binding tax positions.**

## Sources

- IRS Form 6765: https://www.irs.gov/forms-pubs/about-form-6765
- IRS Form 8974: https://www.irs.gov/forms-pubs/about-form-8974
- IRS Section 41 R&D credit: https://www.irs.gov/businesses/research-credit
- IRS Form 6765 2024 revision: https://www.irs.gov/newsroom/irs-revised-form-6765
- IRC Section 41: https://www.law.cornell.edu/uscode/text/26/41
- IRC Section 280C(c)(3) reduced credit election: https://www.law.cornell.edu/uscode/text/26/280C
- Treas Reg 1.41-4: https://www.law.cornell.edu/cfr/text/26/1.41-4
- MainStreet: https://mainstreet.com/
- Neo Tax: https://neo.tax/
- Strike Tax Advisory: https://striketax.com/
- TaxRobot: https://www.taxrobot.com/
- Fenwick — Section 174 update OBBB: https://www.fenwick.com/insights/publications/section-174-rd-capitalization-update-big-beautiful-bill
- OBBB Act Section 41(h) payroll offset $500K cap: https://www.congress.gov/bill/119th-congress/house-bill/1 (One Big Beautiful Bill)
- IRS QSB election guidance: https://www.irs.gov/businesses/small-businesses-self-employed/qualified-small-business-payroll-tax-credit-for-increasing-research-activities

## Related skills

- `sec-174-rd-capitalization` — Section 174 amortization (interplay)
- `payroll-tax-940-941-quarterly-annual` — Form 8974 quarterly offset
- `form-1120-corp-income-tax-filing` — R&D credit on Form 1120
- `asc-740-tax-provision-deferred` — R&D credit deferred tax effects
- `tax-audit-prep-response-federal-state` — R&D credit substantiation file
