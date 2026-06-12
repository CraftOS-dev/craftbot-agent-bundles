<!--
Source: https://www.irs.gov/forms-pubs/about-form-941
Source: https://www.irs.gov/forms-pubs/about-form-940
Source: https://docs.gusto.com/
Source: https://developer.rippling.com/
Source: https://www.irs.gov/payments/eftps-the-electronic-federal-tax-payment-system
Source: https://www.irs.gov/forms-pubs/about-form-1120-w
Reference role.md: "Payroll tax 940 / 941 / W-2"
-->

# Payroll tax — Form 941 (quarterly) + 940 (annual) + quarterly estimated tax

Quarterly + annual payroll tax filings handled automatically by Gusto / Rippling / Justworks / ADP / Paychex / Deel. Form 941 quarterly (federal income withholding + FICA + Medicare), Form 940 annual (FUTA), Form 1120-W quarterly estimated income tax (corporate), Form 1040-ES individual. EFTPS for all federal payments.

## When to use

- Quarterly Form 941 filings (April 30 / July 31 / October 31 / January 31).
- Annual Form 940 FUTA filing (January 31 for prior year).
- Quarterly federal estimated income tax (Form 1120-W corp; 1040-ES individual).
- State withholding + SUTA filings (varies by state).
- W-2 + W-3 annual reconciliation (January 31).
- 1099 + W-2 cross-reconciliation to Form 941 totals.
- Trigger phrases: "Form 941", "Form 940", "FUTA", "FICA", "payroll tax", "withholding", "EFTPS deposit", "1120-W", "estimated tax", "safe harbor", "Gusto", "Rippling", "ADP".

NOT for: 1099 contractor filings (use `1099-k-misc-nec-w2-filing`); equity comp tax timing (use `iso-nso-rsu-employee-tax-treatment`); R&D credit payroll tax offset (use `rd-tax-credit-form-6765-mainstreet-neo`); IRS notice response (use `irs-state-dor-notice-response`).

## Setup

### Gusto

```bash
# Gusto Embedded Payroll API
export GUSTO_API_KEY="..."
curl -H "Authorization: Bearer $GUSTO_API_KEY" \
  https://api.gusto.com/v1/companies
```

### Rippling

```bash
export RIPPLING_API_KEY="..."
curl -H "Authorization: Bearer $RIPPLING_API_KEY" \
  https://api.rippling.com/platform/api/v2/employees
```

### ADP RUN / Workforce Now

```bash
# ADP requires OAuth2 client credentials + cert auth
export ADP_CLIENT_ID="..."
export ADP_CLIENT_SECRET="..."
curl -H "Authorization: Bearer $ADP_TOKEN" \
  https://api.adp.com/hr/v2/workers
```

### Paychex Flex

```bash
export PAYCHEX_API_KEY="..."
curl -H "Authorization: Bearer $PAYCHEX_API_KEY" \
  https://api.paychex.com/employees
```

### Deel (international + US contractors)

```bash
export DEEL_API_KEY="..."
curl -H "Authorization: Bearer $DEEL_API_KEY" \
  https://api.letsdeel.com/rest/v2/people
```

### IRS EFTPS (federal tax deposits)

```bash
# Enroll at https://www.eftps.gov/eftps/
# PIN delivered via paper mail 7-10 business days
# Once enrolled, payments via web portal or IVR
# No public REST API; agent prepares schedule, recipient submits via EFTPS UI
```

## Key rates + thresholds (2026)

| Item | Rate / Threshold |
|---|---|
| FICA (Social Security) | 6.2% employee + 6.2% employer on wages up to $176,100 (2026 wage base) |
| Medicare | 1.45% employee + 1.45% employer (no cap) |
| Additional Medicare Tax | 0.9% on employee wages > $200,000 (employee only) |
| FUTA | 6.0% gross on first $7,000 per employee; reduced to 0.6% with state credit |
| Federal income withholding | Per Publication 15-T tables |
| 941 deposit schedule | Monthly (if PY tax < $50K) or Semi-weekly (if PY tax >= $50K) |
| 941 due date | Last day of month following quarter |
| 940 due date | January 31 for prior year (Feb 10 if all deposits on time) |

## Common recipes

### Recipe 1 — Form 941 quarterly reconciliation (via Gusto)

```python
# Most payroll platforms handle 941 automatically. Reconcile to source data.
import requests
gusto_payrolls = requests.get(
    "https://api.gusto.com/v1/companies/{cid}/payrolls"
    "?processing_status=processed&start_date=2026-04-01&end_date=2026-06-30",
    headers={"Authorization": f"Bearer {GUSTO_API_KEY}"}
).json()

import pandas as pd
totals = pd.DataFrame([
    {
        "wages": p["gross_pay"],
        "federal_withholding": p["taxes"]["federal_income_tax"],
        "social_security_employee": p["taxes"]["ss_employee"],
        "social_security_employer": p["taxes"]["ss_employer"],
        "medicare_employee": p["taxes"]["medicare_employee"],
        "medicare_employer": p["taxes"]["medicare_employer"],
        "additional_medicare": p["taxes"]["additional_medicare"],
    } for p in gusto_payrolls
]).sum()

# Form 941 line totals
print(f"Line 2 wages: {totals.wages}")
print(f"Line 3 fed withholding: {totals.federal_withholding}")
print(f"Line 5a SS wages × 12.4% = {totals.social_security_employee + totals.social_security_employer}")
print(f"Line 5c Medicare × 2.9% = {totals.medicare_employee + totals.medicare_employer}")
print(f"Line 5d Addl Medicare 0.9% = {totals.additional_medicare}")
```

### Recipe 2 — 941 deposit schedule determination

```python
# Lookback period = July 1 - June 30 of prior year
# If lookback period total tax < $50,000 → MONTHLY depositor (15th of next month)
# If lookback period total tax >= $50,000 → SEMI-WEEKLY depositor
#   - Wed/Thu/Fri payroll → following Wed deposit
#   - Sat/Sun/Mon/Tue payroll → following Fri deposit
# If next-day deposit threshold $100,000+ in any day → next-day deposit

lookback_total = 47_500
schedule = "monthly" if lookback_total < 50_000 else "semi-weekly"
print(f"Q2 2026 deposit schedule: {schedule}")
```

### Recipe 3 — Form 940 FUTA reconciliation

```python
# FUTA: 6.0% gross on first $7,000 per employee per year
# State credit: up to 5.4% if all SUTA paid on time → net 0.6%
# Credit-reduction states (where state borrowed from federal trust fund):
#   CA, NY are common in cycles; check current list
import requests
gusto_employees = requests.get(
    "https://api.gusto.com/v1/companies/{cid}/employees",
    headers={"Authorization": f"Bearer {GUSTO_API_KEY}"}
).json()

futa_taxable_per_emp = sum(
    min(emp["ytd_wages"], 7_000) for emp in gusto_employees
)
futa_gross_6pct = futa_taxable_per_emp * 0.06
futa_net_06pct = futa_taxable_per_emp * 0.006  # after 5.4% state credit
```

### Recipe 4 — Quarterly corporate estimated tax (Form 1120-W)

```python
# Safe harbor: lesser of
#  (a) 100% of prior-year tax liability
#  (b) 100% of current-year liability annualized
# Large corp ($1M+ in any of prior 3 years): no PY safe harbor

PY_tax = 425_000  # from prior Form 1120 line 31
quarterly_safe_harbor = PY_tax / 4

# Schedule via EFTPS
schedule_2026 = {
    "Q1 due 4/15": quarterly_safe_harbor,
    "Q2 due 6/15": quarterly_safe_harbor,
    "Q3 due 9/15": quarterly_safe_harbor,
    "Q4 due 12/15": quarterly_safe_harbor,
}
# Underpayment penalty calc via Form 2220
```

### Recipe 5 — Individual estimated tax (Form 1040-ES)

```python
# Safe harbor: lesser of
#  (a) 100% of prior-year tax (110% if AGI > $150K)
#  (b) 90% of current-year tax
# Required if expecting $1,000+ tax due after withholding/credits

PY_tax_individual = 92_000
agi = 240_000
safe_harbor_pct = 1.10 if agi > 150_000 else 1.00
quarterly_individual = (PY_tax_individual * safe_harbor_pct) / 4

# Pay via EFTPS or IRS Direct Pay
# Due 4/15 / 6/15 / 9/15 / 1/15 next year
```

### Recipe 6 — Reconcile 941 to W-2/W-3 annual

```python
# Annual reconciliation: 4 quarters of 941 should match W-3 totals
# IRS matches 941 (federal withholding box 2) to W-3 box 2.
# Mismatch triggers CP2100 notice.

annual_941_totals = sum(
    requests.get(
        f"https://api.gusto.com/v1/companies/{cid}/941/{q}",
        headers={"Authorization": f"Bearer {GUSTO_API_KEY}"}
    ).json()["totals"]
    for q in ["2026Q1", "2026Q2", "2026Q3", "2026Q4"]
)

w3_totals = requests.get(
    f"https://api.gusto.com/v1/companies/{cid}/w3/2026",
    headers={"Authorization": f"Bearer {GUSTO_API_KEY}"}
).json()

assert annual_941_totals["fed_withholding"] == w3_totals["box_2"]
assert annual_941_totals["ss_wages"] == w3_totals["box_3"]
assert annual_941_totals["medicare_wages"] == w3_totals["box_5"]
```

### Recipe 7 — State withholding + SUTA setup per state

```python
# Each state has own DOR + UI agency
STATE_REGISTRATION = {
    "CA": {
        "withholding": "EDD (https://edd.ca.gov)",
        "sui_rate_new_employer": 0.034,
        "sdi_rate": 0.011,  # CA-specific State Disability
        "ett_rate": 0.001,  # Employment Training Tax
    },
    "NY": {
        "withholding": "NY DTF (https://www.tax.ny.gov)",
        "sui_rate_new_employer": 0.0425,
        "metro_commuter_mobility_tax": 0.0034,  # MCTMT for NYC employees
    },
    "TX": {
        "withholding": None,  # no state income tax
        "sui_rate_new_employer": 0.027,
    },
    "WA": {
        "withholding": None,  # no state income tax
        "sui_rate_new_employer": 0.0144,
        "paid_family_medical_leave": 0.0058,  # split employer/employee
    },
}
```

### Recipe 8 — R&D credit payroll-tax offset election

```python
# Qualified small business (< $5M gross receipts + <5yr revenue history)
# can elect Section 41(h) to offset R&D credit against employer FICA
# Post-OBBB 2025: cap raised to $500K (was $250K under IRA 2022)

rd_credit_payroll_offset = min(rd_credit_form_6765, 500_000)

# Election on Form 6765 attached to TIMELY (incl ext) Form 1120
# Offset applied via Form 8974 each quarter on Form 941 line 11a
# Max $500K/year used; carryforward unused balance to following quarters
```

### Recipe 9 — Form 945 (annual non-payroll withholding)

```python
# Form 945 for withholding on non-payroll items:
#   - Pensions, IRAs, gambling, backup withholding
#   - NOT for W-2 wages (that's 941)
# Due January 31; e-file via EFTPS
```

### Recipe 10 — Form 944 (annual for small employers)

```python
# Form 944 = annual 941 for very small employers
# Threshold: Annual liability < $1,000
# Must be IRS-notified to use 944 instead of 941
# Once notified, use it until IRS notifies otherwise
```

## Examples

### Example 1: Series A startup, 35 employees, Gusto + Stripe-paid R&D credit

**Goal:** $2.8M payroll, R&D credit $200K, elect payroll-tax offset.

**Steps:**

1. Confirm < $5M gross receipts + < 5 yr revenue history for Section 41(h) eligibility.
2. File R&D credit Form 6765 (via MainStreet — see `rd-tax-credit-form-6765-mainstreet-neo`).
3. Elect Section 41(h) payroll offset on Form 6765 line 44.
4. Form 8974 attached to Form 941 each quarter starting Q3 (after 1120 filed).
5. Q3 Form 941: Total tax $42,000 − $42,000 (R&D credit offset Form 8974) = $0 federal payroll deposit owed.
6. Q4 + into Q1 next year: continue offset until $200K consumed.
7. Reconcile via Recipe 6 annually.

**Result:** Cash-flow savings $200K spread across 5 quarters; offsetting employer Social Security on Form 941.

### Example 2: Mid-stage company, $80M revenue, 320 employees, ADP

**Goal:** Establish 941 + 940 + multi-state withholding for 320 employees in 14 states.

**Steps:**

1. ADP Workforce Now configured per state SUTA + SIT rates.
2. Semi-weekly depositor (PY liability > $50K).
3. EFTPS auto-deposit configured on payroll processing.
4. Q1 2026 941: $1.8M wages, $185K withholding, $112K SS+Medicare; file by April 30.
5. Annual 940: 320 employees × $7K FUTA wage base × 0.6% = $13,440 net FUTA.
6. State SUTA filings via ADP in each state.
7. CA + NY mid-year credit-reduction monitoring (FUTA add-back if state in credit-reduction status).

**Result:** Multi-state payroll tax compliance automated via ADP; reconciliation monthly.

### Example 3: Solo S-corp founder, $480K salary

**Goal:** Single shareholder-employee S-corp; reasonable comp $480K W-2 + $325K distribution.

**Steps:**

1. Quarterly Form 941: wages $120K Q1, fed withholding $25K, FICA $14.9K (capped at $176,100 wage base for SS), Medicare $3.5K.
2. Reach SS wage base April: no more SS withholding for rest of year (until 2027).
3. Q1 Form 941 due April 30: total $50.3K.
4. Quarterly 1040-ES if expecting additional individual tax beyond W-2 withholding: not needed if W-2 withholding sufficient.
5. Annual 940: $7,000 × 1 emp × 0.6% = $42 net FUTA.
6. Annual W-2 due January 31; W-3 transmittal.

**Result:** Compliant single-employee S-corp payroll tax.

## Edge cases / gotchas

- **Trust Fund Recovery Penalty (TFRP) Section 6672:** 100% personal liability on responsible persons for unpaid Trust Fund taxes (income withholding + employee FICA). IRS aggressively pursues officers, controllers, even bookkeepers.
- **CP2100 / CP2100A notices** for W-2 mismatch (SSN/name mismatch). Must obtain corrected W-9 / SSN verification within 30 days.
- **Backup withholding** (24%): triggered if payee provides invalid SSN/ITIN/EIN or fails W-9. Track via 945.
- **Section 530 relief from misclassification:** if treated worker as contractor in good-faith reliance on industry practice / prior IRS exam / professional advice, may avoid retroactive employment tax assessment.
- **State-specific surcharges:**
  - CA SDI (1.1% employee) + ETT (0.1% employer)
  - NY MCTMT (0.34% on employer wages in NYC metro)
  - WA Paid Family Medical Leave (split)
  - OR Statewide Transit Tax (0.1%)
- **Credit-reduction states for FUTA:** if state borrowed from federal UI trust fund and didn't repay, employers in that state lose part of the 5.4% state credit, raising effective FUTA. Refreshed annually.
- **Lookback period for deposit schedule:** July 1 - June 30 of prior year. New employers default monthly.
- **Form 941-X correction:** amend Form 941 within 3 years of filing. ERTC claw-backs common 2024-2026.
- **ERC (Employee Retention Credit) audit risk:** IRS aggressively auditing 2020-2021 ERC claims. Withdrawal program available; document substantiation rigorously.
- **One-day rule (next-day deposit):** if accumulated tax liability is $100,000+ in any day, deposit next business day; become semi-weekly the rest of year.
- **Section 3402(p) voluntary withholding agreements** allow withholding on non-wage payments (independent contractors). Rare but possible.
- **R&D credit payroll offset under OBBB 2025:** cap raised to $500K (was $250K under IRA 2022); applied to employer SS portion of Form 941 line 11a via Form 8974.
- **Tipped employee FICA tip credit Form 8846:** can credit employer share of FICA on tips reported above minimum wage.
- **Group term life > $50K (Sec 79):** imputed income includible in W-2 box 1, 3, 5; not box 2.

> WARNING **This is informational guidance from an AI agent. Always consult a licensed CPA or tax attorney in your jurisdiction before filing returns, claiming credits, or implementing binding tax positions.**

## Sources

- IRS Form 941: https://www.irs.gov/forms-pubs/about-form-941
- IRS Form 940: https://www.irs.gov/forms-pubs/about-form-940
- IRS Form 944: https://www.irs.gov/forms-pubs/about-form-944
- IRS Form 945: https://www.irs.gov/forms-pubs/about-form-945
- IRS Form 8974 (R&D payroll offset): https://www.irs.gov/forms-pubs/about-form-8974
- IRS Publication 15 (Circular E - Employer's Tax Guide): https://www.irs.gov/publications/p15
- IRS Publication 15-T (Federal Income Tax Withholding Methods): https://www.irs.gov/publications/p15t
- IRS EFTPS: https://www.irs.gov/payments/eftps-the-electronic-federal-tax-payment-system
- IRS Form 1120-W: https://www.irs.gov/forms-pubs/about-form-1120-w
- Gusto API: https://docs.gusto.com/
- Rippling API: https://developer.rippling.com/
- ADP API: https://developers.adp.com/
- Paychex API: https://developer.paychex.com/
- Deel API: https://developer.deel.com/

## Related skills

- `1099-k-misc-nec-w2-filing` — W-2 + 1099 reconciliation
- `rd-tax-credit-form-6765-mainstreet-neo` — R&D payroll-tax offset election
- `iso-nso-rsu-employee-tax-treatment` — equity comp imputed income
- `irs-state-dor-notice-response` — CP2100 / 941 notice response
- `fringe-benefit-tax-sec-132-274` — imputed income for fringe benefits
