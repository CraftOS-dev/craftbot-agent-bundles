<!--
Source: https://www.irs.gov/credits-deductions/opportunity-zones
Source: https://www.irs.gov/forms-pubs/about-form-8824
Source: https://www.irs.gov/forms-pubs/about-form-8997
Source: https://www.irs.gov/forms-pubs/about-form-8949
Source: https://www.law.cornell.edu/uscode/text/26/1400Z-2
Source: https://www.law.cornell.edu/uscode/text/26/1031
Reference role.md: "Section 1031 + Opportunity Zone playbook"
-->

# Opportunity Zones (Section 1400Z) + Section 1031 like-kind exchanges

QOF (Qualified Opportunity Fund) investment tracking — defer capital gain via QOF within 180 days, tiered basis step-up at 5/7/10 years, post-OBBB extension through 2033. Section 1031 like-kind real-property exchanges — 45/180-day identification + closing windows, qualified intermediary, boot recognition. Forms: 8824 (1031), 8997 (annual QOF reporting), 8949 (gain deferral election).

## When to use

- Recipient sold appreciated asset (stock, real estate, crypto) and wants to defer capital gain via QOF investment.
- Real-estate investor selling investment property + replacing with like-kind property (Section 1031).
- Tracking 45-day identification + 180-day closing windows for active 1031 exchange.
- QOF annual reporting (Form 8997) for each tax year QOF investment is held.
- Modeling 5/7/10-year QOF step-ups for tax-planning exit timing.
- Trigger phrases: "QOF investment", "opportunity zone", "1031 exchange", "like-kind", "45-day identification", "qualified intermediary", "Form 8824", "Form 8997", "boot", "reverse 1031".

NOT for: choice of QOF sponsor / fund (recipient consults financial advisor); state-conformity check for QOF gain deferral (most states conform; CA, NC, MA, MS don't — escalate to `legal-counsel`); 1031 mechanics for personal property (TCJA eliminated — only real property now).

## Setup

### `remindme` scheduler — 45/180-day window alerts

```bash
# Schedule calendar reminders at:
# - Day 30 (15 days to identification deadline)
# - Day 44 (1 day before)
# - Day 165 (15 days to closing)
# - Day 179 (1 day before)
remindme --date "2026-08-29" --message "1031 IDENTIFICATION DEADLINE — Property XYZ"
```

### QOF tracker spreadsheet (xlsx)

```python
import pandas as pd
# Tracker columns: investment_date, defer_until_date, qof_name, 
# original_gain, basis, step_up_milestone_5yr, step_up_milestone_7yr, exit_10yr
```

### IRS Forms (no public API)

- Form 8824 — Section 1031 like-kind exchange
- Form 8997 — annual QOF investment reporting (each year held)
- Form 8949 + Schedule D — gain deferral election checkbox
- Form 8996 — QOF self-certification (sponsor-side)

### State-conformity check (Tax Notes / Bloomberg Tax)

```bash
# Most states conform; CA, NC, MA, MS don't conform with QOF gain deferral
# Confirm state-by-state for filing year via Bloomberg State Tax Navigator
```

## Common recipes

### Recipe 1 — Section 1031 timeline + Qualified Intermediary

```python
from datetime import date, timedelta

sale_date = date(2026, 4, 15)
id_deadline = sale_date + timedelta(days=45)     # 2026-05-30
closing_deadline = sale_date + timedelta(days=180)  # 2026-10-12

# 1031 mechanics:
# 1. Sale of relinquished property — proceeds CANNOT touch seller (constructive receipt)
# 2. Qualified Intermediary (QI) holds proceeds
# 3. Seller identifies replacement property(s) within 45 days — WRITTEN to QI
# 4. Seller closes on replacement within 180 days OR due date of return
#    (whichever earlier)
# 5. QI transfers proceeds to seller of replacement at closing

# Identification rules (must use ONE):
# - 3-property rule: identify up to 3 properties (any value)
# - 200% rule: identify any # of properties up to 200% of relinquished FMV
# - 95% rule: identify any # but must close on 95% of identified value

# Schedule reminders
for days in [30, 44, 165, 179]:
    print(f"Reminder day {days}: {sale_date + timedelta(days=days)}")
```

### Recipe 2 — Section 1031 boot recognition

```python
# "Boot" = any non-like-kind consideration received
# Cash boot, mortgage boot (debt relief), personal property = TAXABLE
# Recognized gain = lesser of REALIZED gain OR boot received

relinquished_property = {
    "fmv": 1_800_000,
    "adjusted_basis": 650_000,
    "mortgage_assumed_by_buyer": 950_000,
    "cash_received": 50_000,
}
replacement_property = {
    "fmv": 1_700_000,
    "mortgage_assumed": 850_000,
    "cash_paid": 0,
}

realized_gain = relinquished_property["fmv"] - relinquished_property["adjusted_basis"]
# = $1.15M

mortgage_boot = (relinquished_property["mortgage_assumed_by_buyer"] 
                 - replacement_property["mortgage_assumed"])  # $100K
cash_boot = relinquished_property["cash_received"]  # $50K
total_boot = mortgage_boot + cash_boot  # $150K

recognized_gain = min(realized_gain, total_boot)  # $150K
deferred_gain = realized_gain - recognized_gain   # $1M
new_basis = relinquished_property["adjusted_basis"] + cash_paid + recognized_gain - cash_boot
```

### Recipe 3 — QOF investment 180-day window

```python
from datetime import date, timedelta

# Capital gain recognized → invest realized gain in QOF within 180 days → defer
gain_realized_date = date(2026, 3, 20)
qof_invest_deadline = gain_realized_date + timedelta(days=180)  # 2026-09-16

# Sec 1.1400Z2(a)-1: 180 days runs from
# - Date of sale (general)
# - Last day of tax year (for K-1 reported gains)
# - 180 days from due date for installment-sale gains

# Election: Form 8949 + box marked "Z" + Form 8997 attached
```

### Recipe 4 — QOF tiered step-up schedule (5/7/10-yr)

```python
# Pre-OBBB rules (legacy investments):
# - 5-yr hold: 10% basis step-up on deferred gain
# - 7-yr hold: additional 5% (total 15%)
# - Held through 12/31/2026: deferred gain recognized
# - 10-yr hold: post-acquisition appreciation 100% excluded (basis = FMV at sale)

# Post-OBBB July 2025 (extended to 2033):
# - Deferred gain recognition date PUSHED to 12/31/2033
# - 5/7/10-yr step-ups preserved
# - New QOF investments made by 12/31/2028 fully eligible

investment_date = date(2026, 9, 1)
deferred_gain = 450_000

milestones = {
    "5yr_step_up": (investment_date.replace(year=investment_date.year + 5), 0.10),
    "7yr_step_up": (investment_date.replace(year=investment_date.year + 7), 0.05),
    "gain_recognition": (date(2033, 12, 31), None),  # OBBB-extended
    "10yr_appreciation_exclusion": (investment_date.replace(year=investment_date.year + 10), 1.00),
}

for ms_name, (ms_date, pct) in milestones.items():
    print(f"{ms_date}: {ms_name}")
```

### Recipe 5 — QOF gain recognition on 12/31/2033

```python
# Deferred gain recognized on EARLIER of:
# - Investment sale date
# - 12/31/2033 (post-OBBB; was 12/31/2026)

original_deferred_gain = 850_000
step_up_5yr = 0.10  # held through 5-yr
step_up_7yr = 0.05  # held through 7-yr

basis_step_up_pct = step_up_5yr + step_up_7yr  # 0.15
recognized_on_2033 = original_deferred_gain * (1 - basis_step_up_pct)  # $722,500
# Reported on 2033 Schedule D
```

### Recipe 6 — QOF 10-year exit (basis = FMV)

```python
# Hold QOF investment >= 10 years AND sell BEFORE 12/31/2047:
# Elect FMV basis on sale → 100% exclude POST-ACQUISITION appreciation
# (Original deferred gain still recognized at 2033 recognition event)

qof_purchase_2026 = 850_000  # rolled-in deferred gain amount
qof_fmv_at_sale_2036 = 2_100_000

original_deferred_recognized_2033 = 850_000 * 0.85  # $722,500
fmv_basis_election_2036 = qof_fmv_at_sale_2036  # 100% exclude appreciation
post_acq_appreciation_excluded = qof_fmv_at_sale_2036 - 850_000  # $1.25M excluded
```

### Recipe 7 — Form 8997 annual reporting

```python
# REQUIRED each year QOF investment held (Form 8997)
# Parts:
# I. Initial / aggregate QOF holdings
# II. Current-year capital gains deferred
# III. Inclusion events / sales during year
# IV. End-of-year holdings

# Filed with Form 1040 / 1120 / 1065

import pandas as pd
qof_holdings = pd.DataFrame([
    {"qof_name": "Riverbend QOF I LP", "ein": "92-3456789",
     "investment_date": "2026-09-01", "deferred_gain": 450_000,
     "initial_basis": 0},
])
# Form 8997 Part I populated from this
```

### Recipe 8 — Reverse 1031 (parking arrangement)

```python
# Reverse 1031: acquire REPLACEMENT property BEFORE selling relinquished
# Use Exchange Accommodation Titleholder (EAT) under Rev Proc 2000-37
# 45/180-day windows still apply (from EAT acquisition date)

eat_acquisition_date = date(2026, 5, 1)
sale_id_deadline = eat_acquisition_date + timedelta(days=45)  # identify property to SELL
sale_closing_deadline = eat_acquisition_date + timedelta(days=180)  # close on sale

# Recommended for buyer with strong replacement-property opportunity 
# and weak relinquished-property market
```

### Recipe 9 — QOF self-certification (Form 8996, sponsor side)

```python
# QOF sponsor self-certifies on Form 8996 attached to Form 1065 / 1120
# 90% asset test: 90% of QOF assets = Qualified Opportunity Zone Business (QOZB) property
# Tested semi-annually (6 mo + year-end)

qof_total_assets_jun = 12_500_000
qoz_property_jun = 11_700_000
test_jun = qoz_property_jun / qof_total_assets_jun  # 0.936 — passes 90%

# Penalty for failure: monthly penalty per Sec 1400Z-2(f)
# Reasonable-cause exception available
```

## Examples

### Example 1: Founder sells secondary stock $850K gain → QOF

**Goal:** Series-D founder sells $850K of secondary stock April 2026; deferred gain via QOF investment.

**Steps:**
1. Recipe 3: gain realized 2026-04-20; QOF invest deadline 2026-10-17.
2. Diligence QOFs (sponsor lists at Novogradac, Origin Investments, Caliber).
3. Invest $850K (matching realized gain) by 2026-09-15.
4. Form 8949: report sale + check box "Z" deferral election.
5. Form 8997 Part I + II filed with 2026 1040.
6. Schedule `remindme` for 5-yr (2031), 7-yr (2033), 10-yr (2036) milestones.
7. Per OBBB 2025: deferred gain recognized 12/31/2033 (not 2026).

**Result:** $850K capital gain deferred; basis step-up modeled; 2033 recognition reminder scheduled; Form 8997 tracker built.

### Example 2: Real-estate investor 1031 swap

**Goal:** Investor sells Atlanta duplex $2.4M / $950K basis; identifies Phoenix 4-unit replacement.

**Steps:**
1. Recipe 1 timeline: sale 2026-04-15; ID deadline 5-30; closing 10-12.
2. Engage QI (Asset Preservation Inc / IPX1031 / Exeter) BEFORE sale closing.
3. ID 3 properties by 5-30 (3-property rule).
4. Recipe 2 boot analysis: replacement $2.3M + $100K cash returned to seller → $100K cash boot taxable.
5. Realized gain $1.45M; recognized $100K; deferred $1.35M.
6. Close on Phoenix property 2026-09-01.
7. Form 8824 attached to 2026 Form 1040.

**Result:** $1.35M deferred to next exchange or step-up at death; $100K recognized ordinary basis carryover.

### Example 3: Crypto gain rollover to QOF

**Goal:** Trader realizes $325K ST capital gain on ETH sale 2026-02-12; explores QOF deferral.

**Steps:**
1. Recipe 3: 180-day window = 2026-08-11.
2. Verify QOF eligibility: crypto gain IS eligible (Section 1400Z-2 covers "capital gain").
3. Invest $325K in QOF by 8-11 deadline.
4. Even short-term capital gain qualifies for deferral.
5. Form 8949 + 8997 + Schedule D 2026.
6. Track 5/7/10-yr milestones.

**Result:** $325K ST gain deferred (had been ordinary-rate taxable now); 10-yr exit + FMV basis election preserves QOF appreciation tax-free.

## Edge cases / gotchas

- **TCJA 2017 eliminated 1031 for personal property:** only real property (held for investment / business use) qualifies. Equipment, vehicles, art, crypto DO NOT qualify for 1031.
- **1031 "like-kind" liberal for real estate:** raw land → apartment building → industrial warehouse all "like-kind." Different state OK. US property → foreign property NOT like-kind.
- **Constructive receipt destroys 1031:** seller cannot touch proceeds. QI must hold throughout. Even seller's attorney holding = constructive receipt. Direct deeding allowed but rare.
- **45-day identification rule is strict:** written ID to QI; received by midnight day 45. Email timestamp safe; paper certified mail dated by day 45.
- **QI fraud risk:** in 2008 Hanover QI failure, $400M+ exchanger funds lost. Verify QI bonding + segregated accounts.
- **QOF gain DEFERRAL not EXCLUSION (pre-10-yr):** original gain still recognized at 2033 (post-OBBB); only 5/7/10% basis step-ups reduce recognition. 10-yr exit excludes post-acquisition appreciation only.
- **State conformity:** CA, NC, MA, MS DO NOT conform to QOF gain deferral. CA: must recognize gain currently for state purposes. Confirm state-by-state.
- **QOF must be invested in QOZ Business Property (QOZBP):** raw QOZ land not qualifying alone — substantial improvement required (doubles basis within 30 months) OR original use of property by QOF.
- **OBBB July 2025 changes:** extended OZ program through 2033 (was 2026); preserved 5/7/10-yr step-ups; new investments through 12/31/2028 fully eligible.
- **Form 8997 must be filed EACH YEAR** QOF held — not just acquisition / disposition years.
- **Section 1400Z "qualified opportunity zone" census tract list** fixed at TCJA designation (2017-18). No new tracts added; some expirations possible 2028+.
- **Mixed-funds investment:** investing MORE than realized gain creates two interests — qualifying (matches gain) + non-qualifying (no deferral / step-up). Track separately.
- **Inclusion events:** sale, redemption, partial sale, GRAT funding, gift to charity — most trigger gain recognition before 10-yr. Carve-outs: death, divorce.
- **1031 related-party rule (Section 1031(f)):** 2-year hold required if exchanging with related party. Violation → recognition + interest.

> WARNING **This is informational guidance from an AI agent. Always consult a licensed CPA or tax attorney in your jurisdiction before filing returns, claiming credits, or implementing binding tax positions.**

## Sources

- IRS Opportunity Zones: https://www.irs.gov/credits-deductions/opportunity-zones
- IRS Form 8824 (1031): https://www.irs.gov/forms-pubs/about-form-8824
- IRS Form 8997 (QOF reporting): https://www.irs.gov/forms-pubs/about-form-8997
- IRS Form 8996 (QOF self-certification): https://www.irs.gov/forms-pubs/about-form-8996
- IRS Form 8949: https://www.irs.gov/forms-pubs/about-form-8949
- IRC Section 1400Z-2: https://www.law.cornell.edu/uscode/text/26/1400Z-2
- IRC Section 1031: https://www.law.cornell.edu/uscode/text/26/1031
- Treas Reg 1.1400Z2 final regs: https://www.federalregister.gov/d/2019-27846
- Rev Proc 2000-37 (reverse 1031): https://www.irs.gov/irb/2000-40_IRB
- Novogradac OZ resources: https://www.novoco.com/resource-centers/opportunity-zones-resource-center

## Related skills

- `form-1120-corp-income-tax-filing` — corporate QOF / 1031 reporting
- `state-apportionment-nexus-analysis` — state-conformity check
- `nol-amt-multi-year-tax-planning` — coordination with NOL utilization
- `qsbs-section-1202-bbb-2025-expansion` — QSBS vs QOF deferral comparison
