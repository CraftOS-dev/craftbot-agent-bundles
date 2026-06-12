<!--
Source: https://www.irs.gov/forms-pubs/about-form-1065
Source: https://www.irs.gov/forms-pubs/about-form-1120-s
Source: https://www.irs.gov/forms-pubs/about-schedule-k-1-form-1065
Source: https://www.irs.gov/forms-pubs/about-form-2553
Source: https://www.drakesoftware.com/
Reference role.md: "Form 1120 / 1065 / 1120-S filing"
-->

# Form 1065 + 1120-S — Partnership + S-corp pass-through filing

K-1 generation per partner / shareholder, 704(b) book vs tax basis tracking, AAA (Accumulated Adjustments Account) for S-corps, Schedule K-2/K-3 international partner reporting, reasonable comp test for S-corp shareholder-employees.

## When to use

- Partnership / LLC taxed as partnership Form 1065 (calendar-year due March 15; fiscal-year 15th day of 3rd month after year-end).
- S-corp Form 1120-S (same due date).
- Form 2553 S-election filing (75 days post-incorporation OR by March 15 for current tax year).
- K-1 distribution to partners / shareholders (must be furnished by return due date or extended due date).
- Schedule K-2 / K-3 international partner reporting (mandatory 2022+).
- Capital-account roll-forward: 704(b) book basis, tax basis, GAAP book basis.
- S-corp AAA + OAA (Other Adjustments Account) + PTI (Previously Taxed Income).
- Reasonable comp benchmark for S-corp shareholder-employee (IRS audit focus).
- Trigger phrases: "Form 1065", "Form 1120-S", "K-1", "K-2", "K-3", "AAA", "704(b)", "S-election", "Form 2553", "partnership return", "reasonable comp".

NOT for: C-corp returns (use `form-1120-corp-income-tax-filing`); LLC taxed as C-corp (treat as C-corp); sole proprietorship Schedule C (out of scope — individual return); ASC 740 provision (use `asc-740-tax-provision-deferred`).

## Setup

### Drake Tax — partnership / S-corp module

```bash
# Drake handles 1065 + 1120-S in same product
export DRAKE_API_KEY="..."
curl -H "Authorization: Bearer $DRAKE_API_KEY" \
  https://api.drakesoftware.com/v1/returns?type=1065
```

### Intuit ProConnect Tax — partnership / S-corp

```bash
# ProConnect uses same key for all entity types
export PROCONNECT_API_KEY="..."
curl -H "Authorization: Bearer $PROCONNECT_API_KEY" \
  https://api.intuit.com/v1/proconnect/returns?formType=1065
```

### Thomson Reuters UltraTax CS

```bash
export ONVIO_API_KEY="..."
curl -H "Authorization: Bearer $ONVIO_API_KEY" \
  https://api.onvio.us/v1/firm/returns?entity=partnership
```

### CCH Axcess Tax

```bash
export CCH_API_KEY="..."
curl -H "Authorization: Bearer $CCH_API_KEY" \
  https://cchaxcess.com/api/v1/returns?type=1120S
```

### RCReports (S-corp reasonable comp benchmarking)

```bash
# RCReports = reasonable comp benchmark database
# https://rcreports.com/
export RCREPORTS_API_KEY="..."
curl -H "Authorization: Bearer $RCREPORTS_API_KEY" \
  https://api.rcreports.com/v1/reports
```

## Common recipes

### Recipe 1 — 704(b) capital-account roll-forward (partnership)

```python
# Three basis methods to track:
#  1. 704(b) book basis — economic capital account per partnership agreement
#  2. Tax basis — outside basis per Code Section 705
#  3. GAAP book basis — for financial reporting only
import pandas as pd

partners = pd.DataFrame([
    {"partner": "A", "contributed": 500_000, "share_income": 280_000,
     "share_loss": 0, "distributions": 120_000},
    {"partner": "B", "contributed": 300_000, "share_income": 168_000,
     "share_loss": 0, "distributions": 80_000},
    {"partner": "C", "contributed": 200_000, "share_income": 112_000,
     "share_loss": 0, "distributions": 50_000},
])

partners["ending_704b"] = (partners.contributed 
                           + partners.share_income 
                           - partners.share_loss 
                           - partners.distributions)
print(partners[["partner", "contributed", "share_income",
                "distributions", "ending_704b"]])
```

### Recipe 2 — Tax-basis vs 704(b) book basis reconciliation

```python
# Required disclosure on Schedule K-1 Item L (2020+)
# Tax basis must use Tax Basis Method (no longer allows GAAP/704(b)/Other)

# Diff sources:
#  - Section 704(c) built-in gain at contribution
#  - Depreciation: book straight-line vs tax MACRS+bonus
#  - Section 743(b) basis adjustments (special bases)
#  - Section 754 election downstream effects

tax_basis_walk = pd.DataFrame([
    {"line": "Beginning tax basis", "amount": 500_000},
    {"line": "Capital contributed", "amount": 0},
    {"line": "Share of partnership income (tax)", "amount": 245_000},
    {"line": "Share of nondeductible expenses", "amount": -8_500},
    {"line": "Withdrawals / distributions", "amount": -120_000},
    {"line": "Ending tax basis", "amount": 616_500},
])
```

### Recipe 3 — Schedule K-1 generation (Form 1065)

```python
# K-1 distribution: 11 boxes of pass-through items per partner
# Box 1: Ordinary business income/loss
# Box 2: Net rental real estate income
# Box 3: Other net rental income
# Box 4a: Guaranteed payments for services
# Box 5: Interest income
# Box 6a-c: Dividends
# Box 7: Royalties
# Box 8/9a: Net STCG/LTCG
# Box 13: Other deductions (Section 179, charitable, etc.)
# Box 14: Self-employment earnings
# Box 17: Alternative minimum tax (AMT) items
# Box 18: Tax-exempt income / nondeductible expenses
# Box 19: Distributions
# Box 20: Other (Section 199A QBI, GILTI, etc.)

# Generate K-1 PDFs via preparer software, then distribute via gmail-mcp
from gmail_mcp import send_email  # import inside function
for partner in partners.itertuples():
    send_email(
        to=partner.email,
        subject=f"Your 2025 Schedule K-1 from {entity_name}",
        body="Your K-1 is attached for inclusion in your individual return.",
        attachment=f"K1_{partner.partner}_TY2025.pdf"
    )
```

### Recipe 4 — Schedule K-2 / K-3 international reporting

```python
# K-2 = partnership-level international items (5 parts)
# K-3 = partner-level pass-through of K-2 items (11 parts)
# Required for partnerships with international activity, foreign partners,
# OR partners requesting K-3 for their FTC claim.

# 2024+ EXEMPTION: domestic-only partnership with all-US partners and 
# < $300 of foreign income MAY skip K-2/K-3 IF partners certify in writing
# they don't need them for their own returns.

# Parts of K-2:
#  Part I: Partnership's other current year international info
#  Part II: Foreign tax credit limitation
#  Part III: Information on partners' allocations
#  Part IV: Information for partners' Section 250 deduction (FDII)
#  Part V: Distributions from foreign corp to partnership
```

### Recipe 5 — S-corp AAA / OAA / PTI roll-forward

```python
# S-corp distinct accounts:
#  AAA (Accumulated Adjustments Account) — post-S-election retained earnings
#  OAA (Other Adjustments Account) — tax-exempt income (e.g., muni interest)
#  PTI (Previously Taxed Income) — pre-S-election C-corp E&P consumed
#  AE&P (Accumulated Earnings & Profits) — C-corp era retained earnings
#                                          (only if was C-corp before S)

aaa_walk = pd.DataFrame([
    {"line": "Beginning AAA", "amount": 845_000},
    {"line": "Ordinary income (loss)", "amount": 280_000},
    {"line": "Separately stated income items", "amount": 12_000},
    {"line": "Separately stated deduction items", "amount": -8_500},
    {"line": "Nondeductible expenses (50% meals etc.)", "amount": -15_000},
    {"line": "Distributions (in excess reduces AAA last to zero)",
     "amount": -150_000},
    {"line": "Ending AAA", "amount": 963_500},
])

# Distribution ordering (Section 1368):
#  1. From AAA — non-taxable to extent of shareholder's basis
#  2. From AE&P — taxable as dividend
#  3. From OAA — non-taxable to extent of basis
#  4. From basis — non-taxable return of capital
#  5. Excess of basis — taxable capital gain
```

### Recipe 6 — S-corp shareholder basis tracking

```python
# IRS now requires Form 7203 (S-corp shareholder basis) attached to 1040
# for any shareholder who: claims loss, receives non-dividend distribution,
# disposes of stock, OR loaned to corp.

basis_walk = pd.DataFrame([
    {"line": "Beginning stock basis", "amount": 100_000},
    {"line": "Capital contributed", "amount": 0},
    {"line": "Share of ordinary income (Box 1)", "amount": 45_000},
    {"line": "Share of separately stated income items", "amount": 2_000},
    {"line": "Share of tax-exempt income", "amount": 0},
    {"line": "Share of ordinary loss (Box 1 negative)", "amount": 0},
    {"line": "Share of nondeductible expenses", "amount": -2_500},
    {"line": "Distributions (Box 16D)", "amount": -25_000},
    {"line": "Ending stock basis", "amount": 119_500},
])

# Loan basis tracked separately; restored after stock basis exhausted
```

### Recipe 7 — Reasonable compensation test (S-corp)

```python
# IRS attacks "low salary + high distribution" structures
# Reasonable comp = what unrelated employer would pay for same services
# Sources: RCReports, BLS OEWS, ERI Salary Calculator

# RCReports report cost: ~$120-180 per analysis
# Inputs: role, hours, geography, experience, industry NAICS
import requests
resp = requests.post(
    "https://api.rcreports.com/v1/reports",
    headers={"Authorization": f"Bearer {RCREPORTS_API_KEY}"},
    json={
        "role": "CEO of $5M revenue SaaS",
        "hours_per_week": 50,
        "metro_area": "Austin, TX",
        "naics": "541512",
    }
)
reasonable_comp_range = resp.json()  # e.g., $185K-$245K

# Rule of thumb if defending: salary should be > 30-40% of distributions
```

### Recipe 8 — Form 2553 S-election

```python
# Late S-election rescue under Rev Proc 2013-30 (within 3yr+75days of intended
# effective date) by attaching reasonable cause statement.
# Late election filed via preparer software OR paper-mail to IRS service ctr.

# Standard S-election timing:
#  - For NEW entity: within 75 days of formation
#  - For EXISTING entity wanting S for current year: by March 15
#  - Otherwise effective next tax year

election_date = "2026-01-01"
formation_date = "2025-12-15"
days_to_file = (date.fromisoformat(election_date) 
                - date.fromisoformat(formation_date)).days
assert days_to_file <= 75, "Within 75-day window"

# Each shareholder must sign Form 2553 consent
```

### Recipe 9 — Partner BBA centralized audit (Partnership)

```python
# BBA (Bipartisan Budget Act 2015) = default partnership audit at entity level
# Partnership designates "Partnership Representative" (replaces TMP)
# Partnership pays imputed underpayment (or pushes out to partners via 6226)

# Most small partnerships elect OUT of BBA via Form 1065 Schedule B-2:
#  - 100 or fewer partners
#  - Only eligible partners (no partnership, trust, disregarded entity)
#  - Election made annually on timely-filed return
```

### Recipe 10 — Section 754 election + 743(b) basis adjustment

```python
# Section 754 election (one-time, irrevocable) lets partnership step up
# basis of partnership assets on:
#   - Death of partner (743(b))
#   - Sale of partnership interest (743(b))
#   - Liquidating distribution (734(b))

# Made on timely-filed Form 1065. Attach statement.
# Beneficial when stepped-up basis > book basis.
```

## Examples

### Example 1: Multi-member LLC, $3.4M revenue, 4 partners, first 1065

**Goal:** Tech consulting LLC, 4 members, $3.4M revenue, $980K distributable income. K-2/K-3 required (one foreign-resident partner).

**Steps:**

1. Pull Xero GL + capital contributions log.
2. Compute book → tax M-1 adjustments (50% meals, accrued vacation timing).
3. Allocate income per partnership agreement (50/25/15/10 by capital).
4. Build 704(b) capital roll for each partner (Recipe 1).
5. Build tax-basis roll for K-1 Item L (Recipe 2).
6. Generate K-2 (partnership-level international) + K-3 per partner.
7. Distribute K-1 PDFs via gmail-mcp by March 15.
8. File Form 1065 via Drake; e-file via MeF.
9. Set Form 7004 extension if not ready (auto 6-month).

**Result:** 1065 filed; 4 K-1s distributed; foreign-partner K-3 includes FTC limitation calc.

### Example 2: S-corp founder, $480K W-2, $325K distribution, IRS audit risk

**Goal:** Solo S-corp consultant; $805K net income; $480K W-2 to founder; $325K distribution. Validate reasonable comp.

**Steps:**

1. Pull RCReports analysis: role = Senior Consultant / Founder, $800K rev, Austin TX → range $385K-$575K (Recipe 7).
2. $480K is within range → defensible.
3. Build AAA roll: prior $245K + $805K income − $325K distribution = $725K ending AAA.
4. Compute shareholder basis on Form 7203 for individual 1040.
5. File Form 1120-S via ProConnect.
6. Distribute K-1 to shareholder (single shareholder = no email distribution; just attach to 1040).

**Result:** 1120-S filed; comp position defensible; basis tracked for future distribution / loss claims.

### Example 3: Late S-election rescue, missed 75-day window

**Goal:** LLC formed 2025-08-01, intended S-corp from inception, never filed Form 2553. Discovered May 2026.

**Steps:**

1. Confirm eligibility for Rev Proc 2013-30 late election (within 3 yr 75 days).
2. Draft Form 2553 with effective date 2025-08-01 + reasonable cause statement ("relied on incorrect advice / clerical oversight").
3. All shareholders sign consent.
4. Mail to IRS service center for entity's state.
5. Wait for IRS acceptance letter (CP261, ~6-12 weeks).
6. If approved, file 1120-S for TY 2025 (extension may be needed).

**Result:** S-election accepted retroactively to 2025-08-01; LLC files 1120-S for partial-year 2025.

## Edge cases / gotchas

- **K-1 must be furnished by return due date** (March 15 calendar-year) OR by extended due date if 7004 filed. Late K-1 = $290/partner penalty per month (max 12 months).
- **Schedule K-2/K-3 domestic-only exception:** can skip if partners certify in writing they don't need them; document the certifications.
- **S-corp 100-shareholder cap:** family members count as one. Non-resident aliens, partnerships, C-corps, most trusts disqualify S-election.
- **Single class of stock:** S-corp can't issue prefs or class B with different distribution rights. Voting differences OK.
- **Form 2553 75-day window:** late election rescue under Rev Proc 2013-30. Don't form an LLC and "wait" — file election timely.
- **PTET (Pass-Through Entity Tax) workaround:** ~33 states now allow partnership/S-corp to pay state income tax at entity level (deductible at federal level), bypassing SALT cap. Track elections per state.
- **Section 199A QBI 20% deduction:** pass-through entities ONLY. Wage limit + UBIA limit for high-income earners. Specified Service Trade or Business (SSTB — consulting, health, law, finance) phases out above $245,200 (single) / $490,400 (MFJ) in 2025.
- **Form 7203 mandatory for S-corp shareholders 2022+:** any shareholder claiming loss, receiving distribution, or transferring stock must attach.
- **Built-in gains tax for S-corps converted from C-corp:** 5-year recognition period; tax on appreciated assets at conversion.
- **Excess net passive investment income (S-corp from C-corp):** 25%+ passive income for 3 consecutive years → S-election terminates.
- **AAA can go negative ONLY for losses, not distributions.** Distribution to negative AAA = E&P dividend if AE&P exists.
- **Guaranteed payments to partners:** NOT subject to SE tax under Sec 1402(a)(13) for limited partner GP receiving for services; settled-but-watch IRS guidance.
- **LLC + C-corp election (Form 8832 + 2553):** "check the box" to C-corp, then S-corp. Multi-step.
- **Audit window:** 3 years from filing date OR due date if later. Statute does NOT run on un-filed K-1s.
- **R&D credit allocation to partners:** flows through K-1 box 13M (Sec 41 credit); partners use on Form 6765.

> WARNING **This is informational guidance from an AI agent. Always consult a licensed CPA or tax attorney in your jurisdiction before filing returns, claiming credits, or implementing binding tax positions.**

## Sources

- IRS Form 1065 instructions: https://www.irs.gov/forms-pubs/about-form-1065
- IRS Form 1120-S instructions: https://www.irs.gov/forms-pubs/about-form-1120-s
- IRS Schedule K-1 (Form 1065): https://www.irs.gov/forms-pubs/about-schedule-k-1-form-1065
- IRS Schedule K-1 (Form 1120-S): https://www.irs.gov/forms-pubs/about-schedule-k-1-form-1120-s
- IRS Schedule K-2/K-3: https://www.irs.gov/forms-pubs/about-schedule-k-2-form-1065
- IRS Form 2553 S-election: https://www.irs.gov/forms-pubs/about-form-2553
- IRS Form 7203 (shareholder basis): https://www.irs.gov/forms-pubs/about-form-7203
- Rev Proc 2013-30 (late election relief): https://www.irs.gov/pub/irs-irbs/irb13-36.pdf
- BBA partnership audit: https://www.irs.gov/businesses/partnerships/bba-centralized-partnership-audit-regime
- RCReports: https://rcreports.com/
- Drake Tax: https://www.drakesoftware.com/

## Related skills

- `form-1120-corp-income-tax-filing` — C-corp returns
- `iso-nso-rsu-employee-tax-treatment` — equity comp through K-1 box 13
- `state-apportionment-nexus-analysis` — multi-state pass-through PTET
- `asc-740-tax-provision-deferred` — pass-through doesn't book deferred tax
- `nol-amt-multi-year-tax-planning` — at-risk + passive activity limits
