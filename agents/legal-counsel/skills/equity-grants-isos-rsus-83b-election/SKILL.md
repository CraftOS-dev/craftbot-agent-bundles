---
name: equity-grants-isos-rsus-83b-election
description: Prepare equity grant docs — ISOs (IRC §422), NSOs, RSUs, restricted stock, ESPPs. 409A FMV strike, $100k ISO vesting limit, 83(b) election (30-day deadline, IRS Form 15620 or custom letter per Treasury Reg §1.83-2(e)). Pair with `founders-agreement-vesting-ip-assignment` for founder vesting + `safe-convertible-note-yc-template` for fundraising instruments.
---

# Equity Grants — ISOs / NSOs / RSUs + 83(b) Election

This is the most-error-prone area of startup law. The 30-day 83(b) deadline is the #1 mistake.

## When to use

User says:

- "Grant ISOs / NSOs / RSUs"
- "Prepare equity grants"
- "83(b) election"
- "409A valuation"
- "ISO $100k limit"
- "What's the tax treatment of [equity type]?"
- "Early exercise"
- "Post-termination exercise window"
- "AMT trigger from ISO"
- "RSU vesting / 83(i)"

Companion skills:
- `founders-agreement-vesting-ip-assignment` — founder restricted stock (sister case).
- `safe-convertible-note-yc-template` — fundraising instruments.
- `term-sheet-review-series-a-typical-terms` — investor terms.

## Setup

```bash
# IRS — 83(b) election + equity tax forms
# Form 15620 (model 83(b) election letter, 2024+): https://www.irs.gov/forms-pubs/about-form-15620
# Treasury Reg §1.83-2: https://www.law.cornell.edu/cfr/text/26/1.83-2
# IRS Pub 525 (Taxable Income): https://www.irs.gov/forms-pubs/about-publication-525
# IRS Pub 5528 (ISO basics): https://www.irs.gov/forms-pubs

# Cooley GO equity comp templates
# https://www.cooleygo.com/documents/equity-compensation/

# Stripe Atlas equity templates
# https://stripe.com/atlas

# Clerky equity issuance flow
# https://www.clerky.com/

# 409A valuation providers
# Carta: https://carta.com/409a-valuations/
# Pulley: https://pulley.com/
# AngelList Stack: https://www.angellist.com/stack
# Trica: https://www.tricaequity.com/
# Eqvista: https://eqvista.com/

# Python helpers
pip install pandas openpyxl
```

## Common recipes

### Recipe 1: Pick the right equity type
```text
Decision tree:

Recipient is employee + holder of company stock?
├── Founder (early stage, low FMV): Restricted stock + 83(b) election
├── Early employee (low FMV): Early-exercisable ISO + 83(b) on exercise
└── Later employee: ISO ($100k vesting limit) → NSO above

Recipient is NOT employee?
├── Contractor / consultant / advisor: NSO (ISO not available)
└── Board member: NSO (typically; ISO requires employment)

Public company employee?
├── Standard: RSU (taxed on vesting)
└── ESPP supplement (§423 qualified or non-qualified)

LLC structure?
└── Profits Interest (Rev. Proc. 93-27, 2001-43) — different tax treatment
```

### Recipe 2: ISO (Incentive Stock Option) — IRC §422 requirements
```text
- Holder: employee only (W-2)
- Plan approved by board AND shareholders within 12 months
- Term: 10 years max from grant (5 years for 10%+ shareholders)
- Strike price: ≥ FMV at grant (must be supported by 409A valuation)
  - 10%+ shareholders: ≥ 110% FMV
- $100k ISO vesting limit: aggregate FMV (at grant) of ISOs vesting in any one calendar year capped at $100k
  - Excess automatically becomes NSO
- Post-termination exercise: 90 days max (extension converts to NSO)
- Holding period for ISO tax treatment: 2 years from grant + 1 year from exercise
  - Disqualifying disposition: ordinary income on lesser of (spread at exercise) or (sale price - strike)
- AMT preference item: ISO spread at exercise is AMT income → may trigger AMT bill even if not sold
```

### Recipe 3: NSO (Non-Qualified Stock Option) basics
```text
- Holder: anyone (employee, contractor, advisor, board)
- Strike price: ≥ FMV at grant (409A required — IRC §409A violations: immediate income + 20% penalty + interest)
- Tax on exercise: ordinary income on spread (FMV at exercise − strike), W-2 income for employees (withholding) or 1099 for contractors
- Subsequent sale: capital gain/loss on (sale price − FMV at exercise)
- No $100k limit, no holding period requirements for tax benefit (because no special tax benefit)
```

### Recipe 4: RSU (Restricted Stock Unit) basics
```text
- Promise of stock on vesting (no exercise; no strike)
- Tax on vesting: ordinary income on FMV at vest (employer withholds via sell-to-cover or net-issuance)
- Subsequent sale: capital gain/loss on (sale price − FMV at vest)
- Private-company RSU problem: traditional double-trigger (vesting + liquidity event) for tax efficiency
- §83(i) election (TCJA 2017): eligible private-company employees can defer income up to 5 years post-vesting
  - Eligibility: 80%+ of US employees granted same eligible equity at minimum rates
  - Not widely adopted (complexity)
- Public company default: quarterly vest, no §83(i)
```

### Recipe 5: Restricted Stock + 83(b) — the founder/early-employee path
```text
SETUP:
- Recipient buys stock at par or low FMV (e.g., $0.0001/share × 1M shares = $100)
- Stock subject to vesting (company repurchase right at cost if recipient departs)

TAX WITHOUT 83(b):
- Each vesting tranche → ordinary income on (FMV at vest − purchase price)
- Catastrophic if company grows fast (e.g., 250k shares vest at $1 FMV = $249,975 ordinary income)

TAX WITH 83(b):
- 30-day window from grant
- Ordinary income on (FMV at grant − purchase price) at GRANT
  - For founders/early employees with FMV ≈ purchase price, often $0 income
- All future appreciation = capital gain (long-term if held > 1 year from purchase)
```

### Recipe 6: 83(b) election — STRICT 30-day deadline
```text
Trigger: Restricted stock purchase OR early exercise of unvested options into restricted stock

Deadline: 30 days from grant date (strict — NO extensions, NO postmark grace beyond same-day delivery)
- File certified mail with return receipt to IRS service center where you file your tax return
- Postmark date counts but cutting it close is risky

Content (Treasury Reg §1.83-2(e)):
1. Taxpayer name + address + SSN/TIN
2. Description of property
3. Date of transfer (grant date)
4. Tax year
5. Nature of restrictions
6. FMV at time of transfer (without considering restrictions)
7. Amount paid for property
8. Statement that copies were furnished to person for whom services performed

Recipients:
1. IRS service center where taxpayer files own return — CERTIFIED MAIL + RETURN RECEIPT
2. Person for whom services performed (employer) — copy
3. Taxpayer retains copy for records

As of 2024+: IRS Form 15620 is a model 83(b) election letter (optional — custom letter still acceptable if meets §1.83-2(e) content).
As of 2025+: IRS pilot e-filing for 83(b) via business.irs.gov for some cases.

No IRS receipt confirmation — keep return receipt as proof.
```

### Recipe 7: 83(b) election letter template
```markdown
# Election to Include in Gross Income in Year of Transfer of Property Pursuant to Section 83(b) of the Internal Revenue Code

In accordance with Section 83(b) of the Internal Revenue Code of 1986, as amended, and the Treasury Regulations promulgated thereunder (Treas. Reg. §1.83-2), the undersigned hereby makes an election with respect to the property described below:

1. **Name of taxpayer:** <Full Legal Name>
   **Address:** <Full Address>
   **SSN / TIN:** <XXX-XX-XXXX>

2. **Description of property:** <Number> shares of common stock of <Company Name>, a Delaware corporation (the "Company").

3. **Date of transfer:** <YYYY-MM-DD>

4. **Tax year for which election is made:** <YYYY>

5. **Nature of restrictions:** The shares are subject to a 4-year vesting schedule with a 1-year cliff, beginning <Start Date>. Unvested shares are subject to repurchase by the Company at the original purchase price upon termination of the taxpayer's service relationship with the Company.

6. **FMV at time of transfer (disregarding restrictions):** $<X> per share × <Number> shares = $<Total>

7. **Amount paid for property:** $<Y> per share × <Number> shares = $<Total>

8. **Amount to be included in gross income:** $<FMV - Amount Paid>

A copy of this election has been furnished to the Company (the person for whom services were performed).

Date: <YYYY-MM-DD>
Signature: __________
Print name: <Full Legal Name>

---
**Disclaimer:** This is a template prepared by an AI agent. Always consult a licensed attorney + CPA before filing an 83(b) election. The 30-day deadline is strict.
```

### Recipe 8: 409A valuation requirement
```text
IRC §409A requires options/SARs to have strike ≥ FMV at grant.
"Safe harbor" 409A valuation = independent third-party appraisal that USPS will respect for 12 months (refresh on material event — fundraise, M&A, financial milestone).

Providers (2026):
- Carta — bundled with cap-table
- Pulley — competitive pricing
- AngelList Stack — free for AngelList portfolio
- Trica — boutique
- Eqvista — cheaper alternative

Cost: $1.5k-5k per valuation; refresh every 12 months OR on material event.

Material events triggering 409A refresh:
- Priced equity round (Seed, Series A+)
- Significant secondary transaction
- Bona fide M&A offer
- Material change in business model / financial projections
- 12 months elapsed

Penalty for §409A violation: immediate income recognition + 20% federal penalty + interest. State penalties may also apply.
```

### Recipe 9: $100k ISO vesting limit calculation
```python
# iso_limit.py
# Aggregate FMV (at grant) of ISOs vesting in any one calendar year capped at $100k.

import datetime
grants = [
    {"grant_date": "2026-01-15", "shares": 50_000, "fmv_at_grant": 1.50, "vesting_schedule": "4yr/1yr cliff"},
    {"grant_date": "2026-06-01", "shares": 30_000, "fmv_at_grant": 2.00, "vesting_schedule": "4yr/1yr cliff"},
]

# Year-by-year calculation:
# 2027 vest: 12,500 (from 1st grant) × $1.50 = $18,750 ISO
#         + 7,500 (from 2nd grant) × $2.00 = $15,000 ISO
#         Total = $33,750 ISO
# Within $100k → all ISO

# If a year would push above $100k, the excess converts to NSO at the grant terms.
```

### Recipe 10: Disqualifying disposition (ISO)
```text
Holding periods for ISO tax treatment:
- 2 years from grant date AND
- 1 year from exercise date

If sold before BOTH: disqualifying disposition
- Ordinary income on LESSER of:
  (a) FMV at exercise − strike price (the spread), OR
  (b) Sale price − strike price
- Any additional gain = capital gain
- W-2 reportable; employer withholds (or should)

Common founder mistake: exercise + sell same year (cashless exercise) = disqualifying.
```

### Recipe 11: AMT (Alternative Minimum Tax) on ISO exercise
```text
ISO exercise creates AMT preference item:
- AMT income includes (FMV at exercise − strike price) — even if not sold

For shares NOT sold in same calendar year as exercise → potential AMT tax bill on phantom income.

Mitigation:
- Exercise + sell same year (creates disqualifying disposition but no AMT preference item)
- Spread exercises over years to stay under AMT exemption ($87,500 single / $130k+ joint 2024 thresholds)
- Calculate AMT before exercising → projection tool: https://www.amt-isocalculator.com/

This is the #1 ISO trap — employees exercise + hold for ISO benefit, then face surprise AMT bill.
```

### Recipe 12: Early exercise election
```text
Some plans allow early exercise of UNVESTED options:
- Convert option to restricted stock at exercise
- File 83(b) within 30 days
- Vesting continues; company repurchase right at exercise price

Pros:
- Reset capital gain clock NOW (10x lower FMV vs later)
- Avoid AMT on later exercise (already exercised at low FMV)

Cons:
- Capital outlay upfront
- Risk of losing money if company fails
- 83(b) required → strict 30-day deadline

Common at very early-stage startups (Year 1-2). Less common after Series A.
```

### Recipe 13: Post-termination exercise window
```text
ISO: 90 days max post-termination
- Extension beyond 90 days converts unexercised ISOs to NSOs

NSO: any window the plan specifies (commonly 90 days; some plans extend to 10 years for retirement / death / disability)

Modern progressive plans (Pinterest, Quora, Asana popularized) extend ISO window to 7-10 years for vested options:
- Better for departing employees
- Converts to NSO but employee gets time to exercise
```

### Recipe 14: Grant package
```markdown
# Equity Grant — <Recipient Name>

## Plan
<Company> 2026 Stock Incentive Plan (board + shareholder approved <date>)

## Grant
- Recipient: <Name>
- Recipient type: Employee / Contractor / Advisor / Board
- Equity type: ISO / NSO / RSU / Restricted Stock
- Total shares: <N>
- Strike price (if option): $<FMV per 409A valuation dated <date>>
- Vesting schedule: 4 years, 1-year cliff, monthly thereafter
- Vesting start: <date>
- Term: 10 years from grant (ISO max)
- Post-termination exercise: 90 days (ISO) / <X> days (NSO)
- Acceleration: <single/double trigger on CoC>

## Documents (drafts attached)
- Stock Plan (master plan document)
- Notice of Grant + Grant Agreement
- 83(b) election letter (if early exercise OR restricted stock)
- Stock Purchase Agreement (if restricted stock)
- Equity Incentive Plan Summary

## Required action by recipient
- [ ] Sign Grant Agreement
- [ ] If restricted stock: file 83(b) within 30 days of <grant date> — DEADLINE <date + 30 days>
- [ ] If early exercise of options: file 83(b) within 30 days of exercise
- [ ] Confirm tax-withholding setup (employee)

## Required action by company
- [ ] Board approval (or pursuant to delegation)
- [ ] Update cap table
- [ ] Issue stock certificate (or DRS book-entry)
- [ ] Record on Schedule of Outstanding Equity

---
**Disclaimer:** This is informational guidance prepared by an AI agent. Always consult a licensed attorney + CPA before signing or filing equity grant documents. The 30-day 83(b) deadline is strict.
```

## Examples

### Example 1: Series A startup granting ISO to senior engineer
**Goal:** Grant 50k ISO with 4-year vest at current 409A FMV.
**Steps:**
1. Confirm 409A valuation current (refresh if >12 months or material event since).
2. Recipe 2 verify ISO eligibility (employee status, plan approved).
3. Recipe 9 calculate $100k vesting limit (likely within).
4. Draft grant package (Recipe 14).
5. Board approval (or delegation).
6. Deliver grant + walk recipient through Recipe 11 AMT awareness.
7. Add disclaimer; send to user's licensed attorney for sign-off.

**Result:** ISO grant executed with proper documentation.

### Example 2: Founder restricted stock + 83(b)
**Goal:** Founder receives 1M restricted shares; files 83(b).
**Steps:**
1. Founder purchases shares at par (e.g., $0.0001 × 1M = $100).
2. Stock Purchase Agreement signed; vesting schedule.
3. Within 30 days: Recipe 7 letter prepared.
4. Recipe 6 file via certified mail + return receipt.
5. Copy to company.
6. Retain certified mail receipt forever (tax document).

**Result:** 83(b) filed; founder locks in capital-gain treatment.

### Example 3: Departing employee + 90-day exercise window
**Goal:** Employee leaves with 30k vested ISO; needs to decide exercise.
**Steps:**
1. Recipe 11 AMT projection if exercise + hold.
2. Recipe 10 disqualifying disposition if exercise + sell same year.
3. Calculate cash needed for strike + tax.
4. Decision: exercise (cash outlay + AMT risk) vs forfeit.
5. If extended window in plan: ISO → NSO conversion documentation.

**Result:** Informed exercise / forfeit decision.

## Edge cases / gotchas

- **30-day 83(b) deadline is STRICT.** No extensions; postmark date counts. File certified mail return receipt the day of grant if possible. The #1 founder mistake.
- **Form 15620 is OPTIONAL** (released 2024). Custom letters still acceptable if meeting §1.83-2(e) requirements.
- **AMT trigger on ISO exercise + hold.** Project AMT BEFORE exercising. Phantom-income tax is the classic surprise.
- **$100k ISO limit calculated on FMV AT GRANT** (not at vest). Easy miscalculation when FMV jumps.
- **ISO holding period = 2 years grant + 1 year exercise.** BOTH required. Selling at 1 year + 364 days from exercise + 2 years 1 day from grant = disqualifying.
- **409A refresh on material event.** Closing a Series A is the most common trigger. Old 409A → §409A violations.
- **§409A violations carry 20% penalty + interest** on top of tax. Catastrophic. Make sure all option strikes are at or above 409A FMV.
- **ISO becomes NSO if post-termination exercise window > 90 days.** Plans with extended windows automatically convert.
- **Board approval required for each grant** OR delegation (must be in writing). Unauthorized grants can fail.
- **State tax on equity.** CA + NY are aggressive; CA has 2.5%+ "Mental Health Services Tax" surcharge on high income; NY follows residency rules.
- **International recipients.** Each country has its own tax + securities laws. Don't grant US-only ISOs to a UK employee without local advice.
- **Securities Act §701 / Rule 701.** Federal exemption for compensatory issuances; state Blue Sky compliance still required.
- **Cap table mistakes compound.** Use Carta / Pulley / AngelList Stack to model BEFORE granting.
- **Spousal consent** required in community property states (CA, AZ, ID, LA, NV, NM, TX, WA, WI) for restricted stock + early-exercise transactions.
- **TCJA 2017 §83(i) election rarely used** despite enabling 5-year deferral for private RSU vesting. Complex eligibility (80% rule). Most companies skip.

> Warning: **This is informational guidance from an AI agent. Always consult a licensed attorney + CPA before signing, filing, or executing equity grants or 83(b) elections. The 30-day 83(b) deadline is non-negotiable and any error invalidates the election.**

## Sources

- [IRS Form 15620 — Model 83(b) Election Letter](https://www.irs.gov/forms-pubs/about-form-15620) — 2024+ template.
- [Treasury Reg §1.83-2 — Election to include in gross income](https://www.law.cornell.edu/cfr/text/26/1.83-2) — 83(b) content requirements.
- [IRC §422 — Incentive Stock Options](https://www.law.cornell.edu/uscode/text/26/422) — ISO rules.
- [IRC §409A](https://www.law.cornell.edu/uscode/text/26/409A) — strike price + nonqualified deferred comp.
- [IRC §83(i) — TCJA private RSU deferral](https://www.law.cornell.edu/uscode/text/26/83) — §83(i) election.
- [Cooley GO Equity Compensation](https://www.cooleygo.com/documents/equity-compensation/) — template library.
- [Stripe Atlas Equity Templates](https://stripe.com/atlas) — incorporation + equity bundle.
- [Clerky](https://www.clerky.com/) — cap-table + equity issuance.
- [Carta 409A](https://carta.com/409a-valuations/) — valuation provider.
- [Pulley](https://pulley.com/) — alternative cap-table + 409A.
- [IRS Publication 525 (Taxable Income)](https://www.irs.gov/forms-pubs/about-publication-525) — equity compensation tax.
- Sister skills: `founders-agreement-vesting-ip-assignment`, `safe-convertible-note-yc-template`, `term-sheet-review-series-a-typical-terms`.
