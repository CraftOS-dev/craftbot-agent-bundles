<!--
Source: https://www.irs.gov/publications/p15b
Source: https://www.irs.gov/pub/irs-drop/n-21-25.pdf
Source: https://www.irs.gov/businesses/section-274-meals-entertainment
Source: https://www.irs.gov/forms-pubs/about-publication-463
Reference role.md: "Section 132 fringe benefit exclusions" + "Section 274 meals + entertainment"
-->

# Fringe benefit tax — Section 132 exclusions + Section 274 limits

Section 132 exclusions (transit / parking / dependent care / educational assistance / de minimis / working condition fringes) from W-2 wages. Section 274 deduction limits on meals (50%), entertainment (0% — fully disallowed), and Section 132 employer-side disallowance for parking. Mapping expense categories from Ramp / Brex / Xero to M-1 add-back lines for tax-return book-to-tax adjustment.

## When to use

- Year-end book-to-tax adjustment: identify M-1 add-back lines for non-deductible meals, entertainment, fringe benefits.
- Founder asks "is this expense deductible?" — country club dues, sports tickets, employee-event catering, transit pass reimbursement, gym memberships.
- 2026 employer payroll set-up: assigning Section 132 limits (transit/parking $315/mo) to benefits plan.
- Cannabis Section 280E overlay: which fringe categories are STILL disallowed (most) vs allocable to COGS.
- Trigger phrases: "Section 274", "50% meals", "entertainment deductible", "Section 132", "transit benefit", "de minimis fringe", "parking deduction", "qualified transportation fringe", "M-1 meals add-back".

NOT for: payroll tax mechanics on imputed-income inclusions (use `payroll-tax-940-941-quarterly-annual`); 280E full-business disallowance scope (use `entity-structure-c-vs-s-vs-llc`); commuting reimbursement plan design (HR / `legal-counsel`).

## Setup

### Ramp / Brex — category-tagged expense data

```bash
export RAMP_API_KEY="..."
curl -H "Authorization: Bearer $RAMP_API_KEY" \
  "https://api.ramp.com/developer/v1/transactions?from_date=2026-01-01"

export BREX_API_KEY="..."
curl -H "Authorization: Bearer $BREX_API_KEY" \
  https://platform.brexapis.com/v2/transactions
```

### Xero GL mapping — Meals / Entertainment / Travel accounts

```bash
export XERO_TENANT_ID="..."
# Pull "Meals & Entertainment", "Travel", "Office Snacks", "Gifts" account balances
curl -H "xero-tenant-id: $XERO_TENANT_ID" \
  https://api.xero.com/api.xro/2.0/Reports/ProfitAndLoss
```

### Mapping rule library (xlsx workpaper)

```bash
pip install openpyxl pandas
```

## Common recipes

### Recipe 1 — Section 274 mapping rules (deductible %)

```python
# 2026 deduction percentages by category (post-TCJA + IRS Notice 2021-25)
sec_274_rules = {
    # Meals
    "client_meals_business":            0.50,  # 274(n)(1)
    "employee_travel_meals":            0.50,  # 274(n)(1)
    "office_snacks_coffee":             0.50,  # 274(o) phase-down; 0% post-2025 unless extended
    "employee_meals_on_premises":       0.50,  # 119/132 + 274(n) — 50% to employer
    "annual_holiday_party_all_staff":   1.00,  # 274(e)(4) all-employee
    "employee_birthday_lunch_dept":     0.50,  # not all-employee
    "promotional_event_open_public":    1.00,  # 274(e)(7) public promo

    # Entertainment (FULLY DISALLOWED post-TCJA)
    "sports_tickets_clients":           0.00,  # 274(a)(1)
    "concert_tickets_clients":          0.00,  # 274(a)(1)
    "country_club_dues":                0.00,  # 274(a)(3)
    "golf_outing_clients":              0.00,  # 274(a)(1)
    "theater_tickets_clients":          0.00,  # 274(a)(1)

    # Other
    "commuting_to_office":              0.00,  # 274(a)(4) employer parking + commute disallowed
    "qualified_transit_315mo":          0.00,  # 274(a)(4) employer; excluded from wages 132(f)
    "gifts_per_recipient":              "Section 274(b) — $25/person/yr deduction cap",
    "fines_penalties":                  0.00,  # Section 162(f)
    "political_contributions":          0.00,  # Section 162(e)(1)
    "lobbying":                         0.00,  # Section 162(e)(1)(A)
}
```

### Recipe 2 — Section 132 exclusion limits 2026

```python
# Excludable from employee W-2 wages if under cap
sec_132_2026 = {
    "qualified_transit_pass":        315,    # /mo (CPI-adjusted)
    "qualified_parking":             315,    # /mo (CPI-adjusted)
    "qualified_bicycle_commuting":   0,      # suspended through 2025; check 2026 status
    "adoption_assistance":           17_280, # 2026 est
    "dependent_care_fsa":            5_000,  # $2,500 MFS
    "education_assistance_127":      5_250,  # /yr; OBBB extended through 2025+
    "achievement_award_qualified":   1_600,  # /yr; non-qual $400 max
    "athletic_facility":             0,      # on-premises excludable; no $ cap
    "no_addl_cost_service":          0,      # excludable; e.g. airline empl flying standby
    "qualified_employee_discount":   0,      # services 20% off / goods at cost
    "working_condition_fringe":      0,      # e.g. company phone/laptop
    "de_minimis_fringe":             0,      # occasional + small (typically <$100/event)
    "moving_expenses":               0,      # SUSPENDED 2018-2025; only military
    "qualified_retirement_planning": 0,      # excludable
}
```

### Recipe 3 — M-1 add-back computation from Ramp / Brex

```python
import pandas as pd

# Pull tagged transactions
txns = pd.read_csv("ramp_2026_export.csv")

# Apply Section 274 deduction percentages
def m1_disallowed(row):
    pct = sec_274_rules.get(row["sk_category"], 1.00)
    if isinstance(pct, str):  # gift cap rule
        return row["amount"] - min(row["amount"], 25)
    return row["amount"] * (1 - pct)

txns["m1_addback"] = txns.apply(m1_disallowed, axis=1)
m1_summary = txns.groupby("sk_category")["m1_addback"].sum()
print(m1_summary)
```

### Recipe 4 — Office snacks Section 274(o) phase-out

```python
# Section 274(o) (post-TCJA): "employer-provided meals at on-premises eating facility"
# 50% deductible 2018-2025
# 0% post-2025 UNLESS extended (check current Congressional action)

# As of 2026, OBBB July 2025 did NOT restore office-snack deductibility
# Recommend: track separately; if Congress extends, retroactive adjustment

office_snacks_2026 = 38_500  # Q1 actual
office_snacks_deductible = 0 if year >= 2026 else office_snacks_2026 * 0.50
m1_addback_snacks = office_snacks_2026 - office_snacks_deductible
```

### Recipe 5 — Transit + parking benefit setup (W-2 exclusion)

```python
# Employer-paid qualified transit / parking up to $315/mo (2026) excluded from W-2
# Excess = W-2 box 1 + box 12 inclusion
# Employer-side: post-TCJA Section 274(a)(4) DISALLOWS deduction for qualified transit / parking

employee_monthly_transit = 380  # exceeds $315 cap
excluded_w2 = min(employee_monthly_transit, 315)
included_w2 = employee_monthly_transit - excluded_w2  # $65/mo W-2 imputed income

# Employer side: full $380 = M-1 add-back (no deduction)
m1_addback_transit_per_ee_per_mo = employee_monthly_transit
```

### Recipe 6 — Holiday party 100% deductibility test

```python
# Section 274(e)(4): expenses for recreational, social, or similar activities
# for the benefit of EMPLOYEES are 100% deductible IF primarily for non-HCEs
# (rank-and-file employees)
# HCE 2026 = $160K compensation prior year

annual_holiday_party_cost = 22_400
employee_count_attending = 85
hce_count_attending = 12  # 14% — non-HCE majority

if hce_count_attending / employee_count_attending < 0.50:
    deductible_pct = 1.00  # all-employee event
else:
    deductible_pct = 0.50  # treated as standard business meal
m1_addback_party = annual_holiday_party_cost * (1 - deductible_pct)
```

### Recipe 7 — Section 274(d) substantiation requirements

```python
# Section 274(d) requires CONTEMPORANEOUS records for:
# - Travel (incl. meals + lodging)
# - Gifts
# - Vehicle / listed property
# Required elements: amount, time, place, business purpose, business relationship
# Without substantiation = full deduction disallowance

# Use Ramp / Brex receipt-capture + memo enforcement
unsubstantiated_txns = txns[txns["receipt_url"].isna() | txns["memo"].isna()]
m1_addback_unsubstantiated = unsubstantiated_txns["amount"].sum()
```

### Recipe 8 — Gift Section 274(b) $25/recipient cap

```python
# Section 274(b)(1): business gift deduction capped at $25/recipient/year
# Excludes: incidental items <$4 (e.g. branded pen)
# Excludes: promotional items distributed for general advertising

gifts = pd.DataFrame([
    {"recipient": "Client A — VP Sales", "amount": 180, "type": "wine"},
    {"recipient": "Client B — CFO",      "amount": 45,  "type": "branded notebook"},
    {"recipient": "Partner C",           "amount": 22,  "type": "candy"},
])
gifts["deductible"] = gifts["amount"].apply(lambda a: min(a, 25))
gifts["m1_addback"] = gifts["amount"] - gifts["deductible"]
```

### Recipe 9 — Educational assistance Section 127 limit

```python
# $5,250/yr employer-paid education excludable from W-2
# Includes graduate-level courses
# OBBB July 2025 extended to cover student loan principal/interest through 2025+
# (check current statute for 2026+ status)

employee_education_paid = 7_400
excluded_w2 = min(employee_education_paid, 5_250)
included_w2 = employee_education_paid - excluded_w2  # $2,150 imputed income

# Employer side: 100% deductible business expense
```

## Examples

### Example 1: Year-end M-1 meals + entertainment add-back

**Goal:** SaaS startup $2.8M opex; "Meals & Entertainment" GL account $186,000 + "Office Snacks" $42,000. Compute M-1 add-back for Form 1120.

**Steps:**
1. Pull Ramp tags (Recipe 3): client meals $98K, employee travel meals $54K, holiday party $22K, office snacks $42K, sports tickets $12K.
2. Apply Section 274 rules:
   - Client meals 50%: $49K deductible; $49K add-back.
   - Employee travel meals 50%: $27K deductible; $27K add-back.
   - Holiday party 100% (all-employee — Recipe 6): $0 add-back.
   - Office snacks 0% (Recipe 4 — post-2025): $42K add-back.
   - Sports tickets 0% (entertainment): $12K add-back.
3. Total M-1 add-back: $130K.

**Result:** M-1 line "Expenses on books not deductible" = $130K; documented in workpaper with category-level detail; cross-tied to Ramp transactions for audit substantiation.

### Example 2: Employee transit benefit setup

**Goal:** Company offers $400/mo NYC transit reimbursement to 45 employees. Tax + payroll setup.

**Steps:**
1. Recipe 2 cap: $315/mo excludable from W-2.
2. Recipe 5: $85/mo excess included in each employee's W-2 box 1 + box 12.
3. Gusto pre-tax transit deduction set to $315; excess $85 processed as taxable wage.
4. Employer side: full $400/mo = M-1 add-back (Section 274(a)(4) disallows).
5. Annual employer disallowance: 45 ees * $400 * 12 = $216K M-1 add-back.

**Result:** Payroll configured; year-end M-1 add-back computed; documented in fringe-benefit workpaper.

### Example 3: 280E + Section 132 overlay for cannabis dispensary

**Goal:** Cannabis retail (plant-touching) provides employee parking, holiday party, dependent care FSA. Which are STILL deductible under 280E?

**Steps:**
1. 280E disallows ALL Section 162 ordinary business deductions for trafficking.
2. Section 132 EXCLUSIONS from W-2 still apply (employee-side benefit).
3. But Section 162 deduction at entity level disallowed under 280E:
   - Parking $315/mo per employee: excluded from W-2; not deductible (already disallowed by 274(a)(4) AND 280E).
   - Holiday party: 280E disallowed; not deductible.
   - Dependent care FSA: excluded from W-2 (Section 129); employer match disallowed under 280E.
   - Health insurance: excludable from W-2 (Section 105); 280E disallowed.
4. Only allocable-to-COGS portion of employee meals/snacks for production-floor workers may be COGS-deductible.

**Result:** Full M-1 add-back of all fringe-benefit costs at entity level; W-2 exclusions preserved for employees.

## Edge cases / gotchas

- **Section 274(o) office snacks 0% post-2025:** OBBB July 2025 did NOT restore deductibility. Confirm any year-end legislative extension before booking deduction.
- **All-employee meal/party 100% deductibility (274(e)(4))** requires NON-HCE majority. Check guest list. Department-level lunch likely FAILS.
- **Section 274(d) substantiation** is contemporaneous (within reasonable time of expense). After-the-fact reconstruction generally disallowed.
- **Gift $25 cap (Section 274(b))** is PER RECIPIENT PER YEAR. Spouses count separately. Promotional items <$4 don't count.
- **Section 132(f) transit/parking $315/mo** is CPI-indexed. Confirm 2026 figure via IRS Rev Proc inflation adjustments (typically issued November of prior year).
- **Bicycle commuting Section 132(f)(1)(D)** suspended 2018-2025 by TCJA. Unclear 2026+ status — OBBB silent.
- **De minimis fringe** has no statutory dollar cap; IRS informal "$100/event" guidance. Frequent + significant = NOT de minimis.
- **Employer-provided cell phones** — Notice 2011-72: 100% excludable from W-2 + 100% deductible if "primarily for non-compensatory business purposes."
- **Country club dues fully disallowed** (Section 274(a)(3)) even if "business" use predominant. Lunch AT club may be 50% if substantiated.
- **Meals at sporting events** — separate from entertainment. If meal cost SEPARATELY STATED on invoice, 50% deductible. Bundled = 0%.
- **Per diem meal rates (M&IE)** — IRS Pub 1542 / GSA rates. 50% deductible regardless of per diem method.
- **Spouse / family member travel** — disallowed unless bona fide employee of taxpayer with bona fide business purpose (Section 274(m)(3)).
- **Section 274(a)(4) employer-paid commuting disallowance** is INDEPENDENT of Section 132 W-2 exclusion. Employer takes the M-1 add-back; employee still gets the exclusion.

> WARNING **This is informational guidance from an AI agent. Always consult a licensed CPA or tax attorney in your jurisdiction before filing returns, claiming credits, or implementing binding tax positions.**

## Sources

- IRS Pub 15-B (Employer's Tax Guide to Fringe Benefits): https://www.irs.gov/publications/p15b
- IRS Notice 2021-25 (Meals 100% temporary COVID rule): https://www.irs.gov/pub/irs-drop/n-21-25.pdf
- IRS Section 274 Meals + Entertainment guidance: https://www.irs.gov/businesses/section-274-meals-entertainment
- IRS Pub 463 (Travel, Gift, Car Expenses): https://www.irs.gov/forms-pubs/about-publication-463
- IRS Pub 535 (Business Expenses): https://www.irs.gov/forms-pubs/about-publication-535
- Notice 2011-72 (Cell phones): https://www.irs.gov/pub/irs-drop/n-11-72.pdf
- Treas Reg 1.274-12 (Meals + entertainment final regs): https://www.federalregister.gov/d/2020-21990
- AICPA Section 274 resource: https://www.aicpa.org/topic/tax/meals-entertainment

## Related skills

- `entity-structure-c-vs-s-vs-llc` — 280E full disallowance overlay
- `form-1120-corp-income-tax-filing` — M-1 add-back line population
- `payroll-tax-940-941-quarterly-annual` — W-2 imputed income on excess transit
- `1099-k-misc-nec-w2-filing` — W-2 box 12 / box 14 codes for fringe items
- `asc-740-tax-provision-deferred` — permanent differences for tax provision
