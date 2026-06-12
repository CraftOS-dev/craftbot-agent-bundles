<!--
Source: https://carta.com/learn/equity/stock-options/iso-amt/
Source: https://carta.com/learn/equity/stock-options/83b-elections/
Source: https://www.irs.gov/forms-pubs/about-form-6251
Source: https://www.irs.gov/forms-pubs/about-form-3921
Source: https://www.irs.gov/forms-pubs/about-form-3922
Source: https://www.irs.gov/forms-pubs/about-publication-525
Reference role.md: "Equity comp tax playbook" + "How are our [ISO / NSO / RSU / ESPP] taxed?"
-->

# ISO / NSO / RSU / ESPP — employee equity tax treatment

Mechanics + tax timing for equity comp: ISO (Incentive Stock Options), NSO (Non-Qualified Stock Options), RSU (Restricted Stock Units), ESPP (Employee Stock Purchase Plan), and restricted stock with 83(b) elections. Surfaces AMT (Form 6251) exposure at ISO exercise, W-2 / FICA recognition timing, holding-period rules for LTCG, and the 30-day 83(b) filing window. Source-of-truth: Carta or Pulley cap table; W-2 entries via Gusto / Rippling.

## When to use

- Employee asks "How is my [ISO / NSO / RSU / ESPP] taxed?" at grant, exercise, vest, or sale.
- Founder receives restricted stock grant or early-exercises options — 30-day 83(b) decision.
- ISO exercise + AMT exposure modeling pre-exercise.
- W-2 box 12 / box 14 reconciliation for exercised options + vested RSUs.
- Disqualifying disposition recognition (ISO sold within 1yr post-exercise OR 2yr post-grant; ESPP sold within 1yr post-purchase or 2yr post-offering).
- Trigger phrases: "ISO exercise", "AMT bargain element", "83(b) election", "RSU vest", "NSO exercise", "Form 3921", "Form 3922", "Form 6251", "QSBS holding".

NOT for: equity grant administration (Carta / Pulley UI); cap-table modeling pre-409A; QSBS sale-side modeling (use `qsbs-section-1202-bbb-2025-expansion`); employer-side stock-comp deduction timing (ASC 718 vs Section 83(h)).

## Setup

### Carta — cap table + AMT calculator + 3921 generation

```bash
export CARTA_API_KEY="..."
# Pull grants per employee
curl -H "Authorization: Bearer $CARTA_API_KEY" \
  https://api.carta.com/v1/firms/{id}/securities?stakeholder_id={uid}
# Pull exercises
curl -H "Authorization: Bearer $CARTA_API_KEY" \
  https://api.carta.com/v1/firms/{id}/exercises
```

### Pulley — alt cap-table provider, similar API

```bash
export PULLEY_API_KEY="..."
curl -H "Authorization: Bearer $PULLEY_API_KEY" \
  https://api.pulley.com/v1/companies/{id}/grants
```

### Gusto / Rippling — W-2 supplemental wages for exercises + vests

```bash
export GUSTO_API_KEY="..."
curl -H "Authorization: Bearer $GUSTO_API_KEY" \
  https://api.gusto.com/v1/companies/{id}/supplemental_wages
```

### IRS forms (recipient self-files or via preparer)

- Form 6251 — AMT computation (ISO bargain element)
- Form 3921 — ISO exercise info return (employer files)
- Form 3922 — ESPP info return (employer files)
- 83(b) election — paper-filed certified mail to IRS within 30 days of grant

## Common recipes

### Recipe 1 — ISO AMT bargain element at exercise

```python
# AMT income = (FMV at exercise - strike) * shares exercised
# No regular tax at exercise; AMT only

grant = {
    "type": "ISO",
    "strike_price": 0.85,
    "shares_exercised": 12_000,
    "fmv_at_exercise": 4.20,  # 409A or recent fundraise PPS
}

bargain_element = (grant["fmv_at_exercise"] - grant["strike_price"]) * grant["shares_exercised"]
# = ($4.20 - $0.85) * 12,000 = $40,200 AMT preference income

# AMT exemption 2026 (single): $88,100; phaseout $626,350+
# Tentative AMT = (AMTI - exemption) * 26% (up to $232,600) + 28% above
amti = regular_taxable_income + bargain_element
tentative_amt = max(0, (amti - 88_100) * 0.26)  # simplified
amt_owed = max(0, tentative_amt - regular_tax)
print(f"ISO bargain element: ${bargain_element:,.0f} | AMT owed: ${amt_owed:,.0f}")
```

### Recipe 2 — ISO $100K rule check (annual cap on first-time exercisable)

```python
# Section 422(d): aggregate FMV (at grant) of shares becoming first-time 
# exercisable in any one calendar year cannot exceed $100,000
# Excess = treated as NSO

iso_grants_vesting_2026 = [
    {"date": "2026-02-15", "shares": 8_000, "strike": 1.20, "fmv_at_grant": 1.20},
    {"date": "2026-08-15", "shares": 12_000, "strike": 1.20, "fmv_at_grant": 1.20},
]
total_fmv_at_grant = sum(g["shares"] * g["fmv_at_grant"] for g in iso_grants_vesting_2026)
# = 20,000 * $1.20 = $24,000 → under $100K cap, all stay ISO

# If above $100K, the EXCESS portion (chronologically later vesting) reclassifies to NSO
# Employer must track + report
```

### Recipe 3 — NSO exercise (ordinary income at exercise)

```python
# NSO: bargain element = ordinary W-2 income at exercise
# Employer withholds federal (22% supplemental or 37% if YTD > $1M) + FICA + Medicare
# Reported in W-2 box 1 + box 12 code V

shares_exercised = 5_000
strike = 0.50
fmv_at_exercise = 8.00
ordinary_income = (fmv_at_exercise - strike) * shares_exercised  # $37,500

# Employer withholding
federal_supplemental = ordinary_income * 0.22
ss_tax = min(ordinary_income, 176_100 - ytd_wages) * 0.062  # 2026 SS wage base
medicare = ordinary_income * 0.0145
addl_medicare = ordinary_income * 0.009 if ytd_wages > 200_000 else 0

# Tax basis for future sale = FMV at exercise (NOT strike)
new_basis = fmv_at_exercise * shares_exercised
```

### Recipe 4 — RSU vest (ordinary income at vest)

```python
# RSU: ordinary W-2 income at vest on FMV
# Net-share withholding: employer sells ~22-37% of vested shares to cover taxes

shares_vested = 250
fmv_at_vest = 35.40
ordinary_income = shares_vested * fmv_at_vest  # $8,850

# Net-share withholding
withhold_pct = 0.22  # 0.37 if YTD comp > $1M
shares_withheld = int(shares_vested * withhold_pct)
shares_delivered = shares_vested - shares_withheld

# Holding period for capital gain starts AT VEST (not at grant)
# Basis per share = FMV at vest
```

### Recipe 5 — 83(b) election (30-day clock — CRITICAL)

```python
from datetime import date, timedelta

# 83(b) election: pay ordinary tax NOW on spread between FMV and price paid
# at grant date, rather than at each vest date
# Window: 30 calendar days from grant — STATUTORY (cannot extend)

grant_date = date(2026, 3, 15)
deadline = grant_date + timedelta(days=30)  # 2026-04-14

# File 83(b) by certified mail to IRS service center where 1040 is filed
# Required content per Treas Reg 1.83-2(e):
#   1. Taxpayer name + SSN + address
#   2. Description of property (e.g., "500,000 shares common stock of XYZ Inc")
#   3. Date of grant
#   4. Tax year of election
#   5. Restrictions (vesting schedule)
#   6. FMV at grant
#   7. Amount paid for property
#   8. Statement: "Election under Section 83(b)..."

# Agent action: schedule `remindme` day 25 to confirm filing
```

### Recipe 6 — ISO disqualifying disposition

```python
# ISO holding rules: 1 yr post-exercise + 2 yr post-grant for ISO LTCG treatment
# Sold BEFORE either threshold = DISQUALIFYING DISPOSITION
# Result: bargain element at exercise becomes ORDINARY W-2 income (current year)
#         + appreciation since exercise = capital gain (ST or LT based on hold post-exercise)

exercise_date = "2025-06-15"
sale_date = "2026-04-30"
grant_date = "2023-08-01"

# Sold 10 mo post-exercise → < 1 yr → DISQUALIFYING
exercise_fmv = 6.50
strike = 1.10
sale_price = 9.80
shares = 4_000

ordinary_income_disq = (exercise_fmv - strike) * shares  # $21,600
st_capital_gain = (sale_price - exercise_fmv) * shares   # $13,200 ST
# Employer must issue W-2c if disposition discovered after W-2 finalized
```

### Recipe 7 — ESPP qualifying vs disqualifying

```python
# Section 423 ESPP: 15% discount + 6-month lookback typical
# Qualifying: held >= 1 yr post-purchase AND >= 2 yr post-offering
#   → ordinary income = LESSER of (discount on offering date) or (FMV sale - purchase price)
#   → LTCG on remainder
# Disqualifying: ordinary income = FMV at purchase - purchase price
#   → ST or LT capital gain on (sale - FMV at purchase)

offering_start_fmv = 22.00
purchase_date_fmv = 28.00
purchase_price = 22.00 * 0.85  # = $18.70 (15% off offering price under lookback)
shares = 320
sale_price = 35.00

# Qualifying
ord_qual = min(offering_start_fmv * 0.15, sale_price - purchase_price) * shares
ltcg_qual = (sale_price - purchase_price) * shares - ord_qual

# Disqualifying
ord_disq = (purchase_date_fmv - purchase_price) * shares  # $2,976
```

### Recipe 8 — Form 3921 / 3922 issuance (employer)

```python
# Form 3921 = ISO exercise info return; due Jan 31 to employee, Feb 28 paper / Mar 31 e-file
# Form 3922 = ESPP info return; same deadlines
# Generated by Carta / Pulley + filed via Track1099 or preparer

# Carta API to fetch ISO exercises for 3921 generation
import requests
exercises = requests.get(
    "https://api.carta.com/v1/firms/{id}/exercises",
    headers={"Authorization": f"Bearer {CARTA_API_KEY}"},
    params={"year": 2026, "type": "ISO"}
).json()

# Each exercise → one 3921: stakeholder, grant date, exercise date, 
# shares, strike, FMV at exercise
```

### Recipe 9 — AMT credit recovery (subsequent year)

```python
# AMT paid in year of ISO exercise → AMT credit carryforward
# Recovered in years AMT < regular tax (Section 53)
# Track via Form 8801

prior_amt_paid = 18_500
current_regular_tax = 95_000
current_amt = 72_000

amt_credit_allowed = min(prior_amt_paid, current_regular_tax - current_amt)
# Track residual carryforward on Form 8801
```

## Examples

### Example 1: Engineer exercises 8,000 ISOs at $1.50 strike, $9.00 FMV

**Goal:** Senior engineer wants to exercise + hold for QSBS-LTCG. Filed earlier 409A shows FMV $9.00.

**Steps:**
1. Recipe 1 AMT calc: bargain = (9.00 - 1.50) * 8,000 = $60,000 AMT income.
2. Recipe 2 $100K rule check: only 8,000 shares ISO exercising; under cap.
3. Tentative AMT estimate at single filer $200K base income: ~$15,600 AMT owed.
4. ISO holding clock: 1 yr post-exercise + 2 yr post-grant for ISO LTCG.
5. Form 3921 issued by employer next Jan 31.
6. If sold post-1-yr-post-exercise AND 2-yr-post-grant: full LTCG; bargain becomes QSBS-eligible if entity + 5-yr hold qualify.

**Result:** Pay $15,600 AMT 2026; Form 8801 carries forward; sale planned >= 2026 + 12 mo for ISO LTCG + 5 yr post-grant for QSBS exclusion.

### Example 2: Founder gets restricted stock — 83(b) decision

**Goal:** Founder receives 4,000,000 restricted shares at $0.0001/share FMV (immediately post-incorporation). Vests over 4 years cliff-1-year.

**Steps:**
1. FMV at grant: 4,000,000 * $0.0001 = $400.
2. Amount paid: $400 (par value purchase).
3. 83(b) spread: $0. No tax owed.
4. File 83(b) certified mail within 30 days (Recipe 5).
5. Schedule `remindme` day 25 for filing confirmation.
6. Without 83(b): each vest tranche taxed at then-current FMV — catastrophic if company appreciates.

**Result:** 83(b) filed day 12; no tax owed; holding clock for LTCG + QSBS starts grant date.

### Example 3: Employee disqualifying ISO disposition mid-year

**Goal:** Employee exercised 2,500 ISOs in June 2025; sold all in March 2026 (10 months post-exercise — disqualifying).

**Steps:**
1. Recipe 6: disqualifying → bargain element ($14,000) becomes 2026 W-2 ordinary income.
2. ST capital gain on appreciation since exercise.
3. Original 2025 Form 6251 AMT preference REVERSES (Section 56(b)(3)): adjust prior-year AMT credit basis.
4. Employer issues W-2c for 2026 reporting additional ordinary wages.
5. No FICA on disqualifying disposition (per Rev Rul 71-52 + Notice 2002-47 — narrow rule; ISOs/ESPPs exempt from FICA at exercise/sale).

**Result:** 2026 W-2c issued for $14K additional ordinary wages; $8,250 ST gain reported on Schedule D; AMT credit basis adjusted via Form 8801.

## Edge cases / gotchas

- **83(b) 30-day window is statutory + non-extendable:** missed = no election ever. Includes weekends/holidays in count. File certified mail RETURN-RECEIPT-REQUESTED + retain proof for 7+ years.
- **ISO $100K rule applies at GRANT FMV (not exercise FMV):** total FMV of shares first-time exercisable in calendar year capped at $100K. Software (Carta / Pulley) tracks automatically.
- **ISO 10-year max term + 90-day post-termination exercise window:** standard plan; some plans extend post-termination window but exceeding 90 days disqualifies ISO status.
- **AMT exemption phaseout 2026:** single $626,350; MFJ $1,252,700 (CPI-adjusted). Above phaseout, exemption reduced by 25% of excess.
- **Net-share withholding for RSUs uses 22% supplemental rate** until YTD supplemental wages exceed $1M; above $1M, mandatory 37%. Often UNDERWITHHELDS high-bracket employees — recommend additional W-4 withholding.
- **ISO/ESPP exempt from FICA at exercise/purchase per Notice 2002-47.** Narrow rule — RSU + NSO are FICA-taxable.
- **State AMT** varies; CA has its own AMT (CA Form 540 Sch P) — ISO exercise often triggers CA AMT too.
- **Section 409A penalty:** strike below FMV at grant = 20% federal penalty tax + interest + employer withholding obligation. Always tie ISO/NSO strike to current 409A valuation.
- **Early exercise of options + 83(b):** if plan permits early exercise of unvested ISOs/NSOs, 83(b) election covers entire grant — same 30-day clock from exercise date.
- **ISO disqualification reverses AMT preference (Section 56(b)(3)):** subsequent-year adjustment via Form 6251 + 8801. Easy to miss.
- **Section 162(m) $1M cap** applies to public-company top 5 executives; private-company exempt.
- **Carta / Pulley 3921 + 3922 e-file deadline:** Form 3921/3922 must be e-filed if >= 10 returns (post-Treasury Reg 301.6011-2). Most cap-table providers handle.
- **State-source AMT for relocated employees:** if employee moved between states during exercise + vest, allocate W-2 / AMT preference per state-source rules.

> WARNING **This is informational guidance from an AI agent. Always consult a licensed CPA or tax attorney in your jurisdiction before filing returns, claiming credits, or implementing binding tax positions.**

## Sources

- Carta ISO + AMT primer: https://carta.com/learn/equity/stock-options/iso-amt/
- Carta 83(b) elections: https://carta.com/learn/equity/stock-options/83b-elections/
- IRS Form 6251 (AMT): https://www.irs.gov/forms-pubs/about-form-6251
- IRS Form 3921 (ISO info return): https://www.irs.gov/forms-pubs/about-form-3921
- IRS Form 3922 (ESPP info return): https://www.irs.gov/forms-pubs/about-form-3922
- IRS Form 8801 (AMT credit): https://www.irs.gov/forms-pubs/about-form-8801
- IRS Pub 525 (Taxable + Nontaxable Income): https://www.irs.gov/forms-pubs/about-publication-525
- Treas Reg 1.83-2 (83(b) election): https://www.law.cornell.edu/cfr/text/26/1.83-2
- IRS Notice 2002-47 (FICA on ISO/ESPP): https://www.irs.gov/pub/irs-drop/n-02-47.pdf

## Related skills

- `qsbs-section-1202-bbb-2025-expansion` — QSBS sale-side after exercise
- `1099-k-misc-nec-w2-filing` — W-2 box 12 codes (V for NSO, etc.)
- `payroll-tax-940-941-quarterly-annual` — supplemental wage withholding on RSU vests
- `entity-structure-c-vs-s-vs-llc` — equity comp requires C-corp
- `nol-amt-multi-year-tax-planning` — AMT credit carryforward + recovery planning
