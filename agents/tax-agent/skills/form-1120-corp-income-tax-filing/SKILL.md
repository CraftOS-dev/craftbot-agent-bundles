<!--
Source: https://www.irs.gov/forms-pubs/about-form-1120
Source: https://www.drakesoftware.com/
Source: https://accountants.intuit.com/proconnect/
Source: https://tax.thomsonreuters.com/en/cs-professional-suite/ultratax-cs
Source: https://www.wolterskluwer.com/en/solutions/cch-axcess
Source: https://www.irs.gov/payments/eftps-the-electronic-federal-tax-payment-system
Reference role.md: "Form 1120 / 1065 / 1120-S filing"
-->

# Form 1120 — C-corp federal income tax filing

Book-to-tax reconciliation (Schedule M-1 / M-3), tax-return preparation, e-file via IRS MeF, quarterly estimated tax via EFTPS. Preparer software: Drake Tax (SMB / firm leader), Intuit ProConnect / Lacerte (cloud), Thomson Reuters UltraTax CS, CCH Axcess (Wolters Kluwer enterprise), Bloomberg Tax Provision / CorpTax (large corp).

## When to use

- C-corp federal income tax filing (calendar-year due April 15; fiscal-year 15th day of 4th month after year-end).
- Quarterly estimated tax preparation (Form 1120-W) — due April 15 / June 15 / September 15 / December 15.
- Schedule M-1 (under $10M assets) or Schedule M-3 (over $10M assets) book-to-tax reconciliation.
- Schedule UTP (Uncertain Tax Positions) for $10M+ asset corps with FIN 48 reserves.
- Schedule L balance sheet + Schedule K (other information).
- Extension request via Form 7004 (automatic 6-month extension).
- Trigger phrases: "Form 1120", "C-corp tax return", "Schedule M-1", "M-3 reconciliation", "1120-W estimated", "MeF e-file", "EFTPS deposit".

NOT for: S-corp returns (use `form-1065-1120s-passthrough-filing`); partnership returns (same); state corporate income tax filing (use `state-apportionment-nexus-analysis`); R&D credit claim (use `rd-tax-credit-form-6765-mainstreet-neo`).

## Setup

### Drake Tax (SMB / firm leader, ~$1,825-$2,395 / year unlimited returns)

```bash
# Drake API access requires Drake Software license + API enablement
# Drake Tax Desktop has data export/import via XML packet
# Drake Documents API: https://drakesoftware.com/api/

export DRAKE_API_KEY="..."
curl -H "Authorization: Bearer $DRAKE_API_KEY" \
  https://api.drakesoftware.com/v1/returns
```

### Intuit ProConnect Tax Online (~$549 / return for 1120)

```bash
# Tax Data Connect: Intuit API for pulling/pushing client data
export PROCONNECT_API_KEY="..."
curl -H "Authorization: Bearer $PROCONNECT_API_KEY" \
  https://api.intuit.com/v1/proconnect/clients
```

### Thomson Reuters UltraTax CS (~$2,500-$10,000 / year by tier)

```bash
# UltraTax CS API + Onvio integration
export ONVIO_API_KEY="..."
curl -H "Authorization: Bearer $ONVIO_API_KEY" \
  https://api.onvio.us/v1/firm/returns
```

### CCH Axcess Tax (Wolters Kluwer, enterprise cloud)

```bash
# CCH Cloud API
export CCH_API_KEY="..."
curl -H "Authorization: Bearer $CCH_API_KEY" \
  https://cchaxcess.com/api/v1/returns
```

### IRS EFTPS — federal tax payment system

```bash
# EFTPS is web-only enrollment (https://www.eftps.gov/eftps/)
# Once enrolled, payments scheduled via the EFTPS web portal or batch IVR
# Initial PIN delivered via paper mail (7-10 business days)
# No public REST API; agent prepares the payment schedule, recipient submits
```

## Common recipes

### Recipe 1 — Schedule M-1 reconciliation (small C-corp, <$10M assets)

```python
# Book income → Taxable income via M-1 add-backs / subtractions
import pandas as pd

# Pull GL trial balance from Xero
from xero_python.accounting import AccountingApi  # imports inside function
book_pretax = xero_client.get_account_balance("4000")  # P&L net income

# Common M-1 adjustments
m1_adjustments = pd.DataFrame([
    {"line": "Income per books", "amount": book_pretax},
    {"line": "Federal income tax per books", "amount": 0},  # add back
    {"line": "Excess capital losses over gains", "amount": 0},
    {"line": "Income subject to tax not on books", "amount": 0},
    {"line": "Expenses on books not deductible (e.g., 50% meals)",
     "amount": meals_50pct_disallowed},
    {"line": "Section 274 entertainment (100% disallowed)",
     "amount": entertainment_total},
    {"line": "Fines + penalties", "amount": fines_total},
    {"line": "Stock-based comp book vs tax", "amount": sbc_book_tax_diff},
    {"line": "Depreciation book vs tax", "amount": depreciation_diff},
    {"line": "Income on books not subject to tax (e.g., muni interest)",
     "amount": -muni_interest},
    {"line": "Deductions on tax not on books (e.g., bonus depr)",
     "amount": -bonus_depr},
])

taxable_income = m1_adjustments.amount.sum()
federal_tax_21pct = taxable_income * 0.21
print(f"Taxable income: ${taxable_income:,.0f} | Federal tax 21%: ${federal_tax_21pct:,.0f}")
```

### Recipe 2 — Schedule M-3 (large C-corp, >$10M assets)

```python
# M-3 is a 3-page reconciliation with separate columns:
# Col (a) Income/loss per income stmt
# Col (b) Temp diffs
# Col (c) Perm diffs
# Col (d) Income/loss per tax return

# Part I (Reconciliation of consolidated book income to includible book income)
# Part II (Income/loss items)
# Part III (Expense/deduction items)

# Most preparer software (Drake / ProConnect / UltraTax / CCH) auto-populates
# M-3 from a chart-of-accounts mapping table
```

### Recipe 3 — Form 1120-W quarterly estimated tax

```python
# Safe harbor: pay lesser of
#  (a) 100% of prior-year tax liability (if PY > $0 and 12-month tax year)
#  (b) 100% of current-year liability annualized
# Large corp ($1M+ taxable income in any of prior 3 years): no safe harbor
# protection on prior-year — must use current-year actual.

prior_year_tax = 425_000  # from PY Form 1120 line 31
quarterly_safe_harbor = prior_year_tax / 4

# Schedule via EFTPS
print(f"Q1 due 4/15: ${quarterly_safe_harbor:,.0f}")
print(f"Q2 due 6/15: ${quarterly_safe_harbor:,.0f}")
print(f"Q3 due 9/15: ${quarterly_safe_harbor:,.0f}")
print(f"Q4 due 12/15: ${quarterly_safe_harbor:,.0f}")
```

### Recipe 4 — E-file via IRS MeF (Modernized e-File)

Direct MeF e-file requires an IRS-issued EFIN (Electronic Filing Identification Number). Most preparer software bundles MeF submission. Manual MeF API is restricted to authorized e-file providers.

```bash
# Via Drake
# 1. Validate return: Drake → Form Validation → run all checks
# 2. Sign with Form 8879-C (corporate e-file signature authorization)
# 3. Transmit: Drake → EF → Transmit returns
# 4. Status: Drake → EF → Status (Accepted / Rejected / Pending)

# Via CCH Axcess
# 1. CCH Axcess → Workstreams → Transmit
# 2. Acknowledgment retrieval within 24-48 hours
```

### Recipe 5 — Extension via Form 7004

```python
# Automatic 6-month extension; due original filing date (typically April 15)
# Must pay estimated balance due with the extension to avoid late-payment penalty

extension_payment = (current_year_projected_tax 
                     - prior_quarterly_estimates_paid 
                     - credits_applied)

# File Form 7004 via preparer software OR via IRS Direct Pay portal
# (https://www.irs.gov/payments/direct-pay)
```

### Recipe 6 — Schedule UTP (Uncertain Tax Positions)

```python
# Required for $10M+ asset C-corps with audited financials
# Disclose tax positions where reserves recorded under FIN 48 / ASC 740-10

utp_positions = [
    {
        "position_id": "UTP-2026-01",
        "issue": "R&D credit qualification - cloud infra dev wages",
        "irc_section": "Section 41",
        "facts": "Allocated 65% of cloud platform team wages to QREs",
        "reserve_amount": 142_000,  # FIN 48 reserve
        "ranked_by_size": True,
    },
    # ...
]
```

### Recipe 7 — Book-to-tax fixed assets reconciliation

```python
# Book depreciation: GAAP straight-line
# Tax depreciation: MACRS + Section 179 + bonus depreciation
# Section 168(k) bonus depreciation: 60% in 2024, 40% in 2025, 20% in 2026
#   (phasing out under TCJA; OBBB 2025 did NOT restore 100% bonus)

book_depr = 245_000  # straight-line over 5-yr life
tax_depr = 391_000   # MACRS 5-yr + 40% bonus on $250K placed in service
m1_depr_diff = book_depr - tax_depr  # negative = subtraction on M-1
```

### Recipe 8 — Reconcile estimated tax payments to ledger

```python
# Pull EFTPS payment history (manual export from eftps.gov)
# Cross-reference to Xero "Federal Tax Payable" account
eftps_payments = pd.read_csv("eftps_payments_2026.csv")  # confirmation #, amount, date
xero_payments = xero_client.get_transactions("2400")  # Federal Tax Payable
diff = eftps_payments.amount.sum() - xero_payments.amount.sum()
assert abs(diff) < 5, f"EFTPS to Xero variance: ${diff}"
```

## Examples

### Example 1: First-time Form 1120 for VC-backed SaaS, year 2 of ops

**Goal:** $8M revenue, $2.1M book pretax loss, Delaware C-corp, 32 employees. Drake Tax preparer; recipient owns Drake license.

**Steps:**

1. Pull Xero P&L + balance sheet (Recipe 1 setup).
2. Compute M-1 adjustments:
   - Add back $0 fed tax per books (loss year).
   - Add back 50% meals ($18,000 of $36,000 spent).
   - Add back entertainment ($4,200 — Section 274 disallowed).
   - Add stock-comp book-tax diff ($235,000 — book vs tax timing).
   - Depreciation diff: book $145K vs MACRS+40% bonus $238K → ($93K) subtraction.
3. Taxable loss = $2.1M book − $93K depr + $22K addbacks = $2.17M loss.
4. No federal tax liability; full NOL carryforward.
5. R&D credit: $375K Form 6765 credit, can be used against payroll tax up to $250K (post-OBBB 2025) or carried forward.
6. File Form 1120 via Drake; signature via Form 8879-C; e-file.
7. Document NOL waterfall + Section 382 ownership change check.

**Result:** Form 1120 filed; $2.17M NOL added to carryforward register; R&D credit elected for payroll-tax offset.

### Example 2: $45M revenue C-corp, Schedule M-3, multi-state

**Goal:** Mature C-corp, $45M revenue, $6.2M pretax book income, files in 14 states.

**Steps:**

1. Pull GL via `xero-mcp` + `postgresql-mcp`.
2. M-3 Part I: reconcile consolidated book income to includible book income.
3. M-3 Part II/III: line-item temp diff (depreciation, accruals, NOLs, R&D capitalization) + perm diff (50% meals, entertainment, fines, muni interest).
4. Tax-prep via CCH Axcess.
5. State apportionment via Vertex (single-sales factor in 11 states; three-factor in 3).
6. Federal tax: $6.2M book + $850K M-3 adjustments = $7.05M taxable × 21% = $1,480,500.
7. State tax: aggregate $545,000 across 14 states.
8. CAMT check: AFSI < $1B, not subject to Corporate Alternative Minimum Tax.
9. E-file via CCH; ACK retrieved.

**Result:** Federal + state returns filed; total tax $2.025M; quarterly estimates for next year configured in EFTPS.

## Edge cases / gotchas

- **CAMT (Corporate Alternative Minimum Tax):** 15% on Adjusted Financial Statement Income (AFSI) for C-corps with $1B+ 3-year average AFSI (post-IRA 2022). Form 4626. Most SaaS / startup recipients = no.
- **Section 163(j) interest limitation:** business interest expense capped at 30% of ATI (Adjusted Taxable Income). Small business exception under $30M average gross receipts (2026 indexed). Carry forward indefinitely.
- **Section 382 ownership change:** if >50% ownership shift in any 3-year window, NOLs subject to annual limitation (FMV at change × long-term tax-exempt rate). Common at fundraise rounds.
- **Section 174 R&D capitalization:** TCJA mandated 5-yr domestic / 15-yr foreign amortization (2022+). OBBB 2025 restored immediate expensing for domestic R&D (retroactive to 2025). Foreign R&D still 15-yr.
- **Schedule M-3 vs M-1 threshold:** $10M total assets at year-end or any partner / related party with $10M+ trips M-3. Once M-3, always M-3 unless drop below for 3 consecutive years.
- **R&D credit + Section 280C(c)(3):** must reduce R&D wage deduction by credit amount OR elect reduced credit. Most preparer software auto-elects.
- **Federal corporate rate:** flat 21% post-TCJA. No graduated brackets.
- **NOL post-2017:** indefinite carryforward; no carryback (except farming + casualty). Can offset only 80% of taxable income.
- **PTET (Pass-through Entity Tax) workaround:** doesn't apply to C-corps; only S-corp / partnership.
- **Form 8879-C signature:** must be signed BEFORE transmitting return; perjury statement requires officer signature.
- **Late filing penalty:** 5% per month, max 25%. Late payment: 0.5% per month. Both compound.
- **Year-end book-to-tax cutoff:** ASC 606 deferred revenue + accrued PTO + stock comp expense often book-vs-tax timing diffs. Document each in M-1/M-3 workpaper.
- **Disregarded LLC + C-corp parent:** include disregarded entity in consolidated return; no separate filing.
- **Section 199A QBI:** does NOT apply to C-corps; only pass-through entities.

> WARNING **This is informational guidance from an AI agent. Always consult a licensed CPA or tax attorney in your jurisdiction before filing returns, claiming credits, or implementing binding tax positions.**

## Sources

- IRS Form 1120 instructions: https://www.irs.gov/forms-pubs/about-form-1120
- IRS Schedule M-3 (Form 1120): https://www.irs.gov/forms-pubs/about-schedule-m-3-form-1120
- IRS Form 1120-W (quarterly estimated): https://www.irs.gov/forms-pubs/about-form-1120-w
- IRS Form 7004 (extension): https://www.irs.gov/forms-pubs/about-form-7004
- IRS Form 8879-C (e-file authorization): https://www.irs.gov/forms-pubs/about-form-8879-c
- IRS Form 4626 (CAMT): https://www.irs.gov/forms-pubs/about-form-4626
- IRS Schedule UTP: https://www.irs.gov/forms-pubs/about-schedule-utp-form-1120
- Drake Tax: https://www.drakesoftware.com/
- Intuit ProConnect: https://accountants.intuit.com/proconnect/
- Thomson Reuters UltraTax CS: https://tax.thomsonreuters.com/en/cs-professional-suite/ultratax-cs
- CCH Axcess: https://www.wolterskluwer.com/en/solutions/cch-axcess
- IRS EFTPS: https://www.irs.gov/payments/eftps-the-electronic-federal-tax-payment-system
- IRS Direct Pay: https://www.irs.gov/payments/direct-pay
- IRS MeF system: https://www.irs.gov/e-file-providers/modernized-e-file-mef

## Related skills

- `form-1065-1120s-passthrough-filing` — partnership + S-corp returns
- `asc-740-tax-provision-deferred` — book-to-tax deferred tax provision
- `nol-amt-multi-year-tax-planning` — NOL waterfall + Section 382 + CAMT
- `state-apportionment-nexus-analysis` — multi-state apportionment
- `sec-174-rd-capitalization` — Section 174 R&D capitalization mechanics
- `rd-tax-credit-form-6765-mainstreet-neo` — R&D credit Form 6765
