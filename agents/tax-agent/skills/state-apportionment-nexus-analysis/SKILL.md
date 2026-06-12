<!--
Source: https://www.avalara.com/us/en/learn/whitepapers/state-income-tax-apportionment.html
Source: https://www.vertexinc.com/products/income-tax
Source: https://www.taxnotes.com/research/federal/state-tax-treatment-corporate-income
Source: https://www.salt.com/ (Bloomberg State Tax Navigator)
Source: https://www.mtc.gov/the-commission/multistate-tax-compact (MTC compact)
Reference role.md: "State apportionment playbook" + "State income tax economic nexus thresholds (2026)"
-->

# State income tax apportionment + nexus analysis

Multi-state corporate / pass-through income tax: economic nexus thresholds (post-Wayfair adopted for income tax in many states), apportionment formulas (single-sales factor vs three-factor), sourcing methods (market-based vs cost-of-performance), throwback / throwout rules, and PTET (Pass-through Entity Tax) elections. Tools: Vertex Income Tax, Avalara Income Tax, Sphere (apportionment + nexus + filing), Bloomberg State Tax Navigator.

## When to use

- Multi-state C-corp / S-corp / partnership filing — apportion taxable income per state.
- Remote-employee expansion triggers physical nexus in new states.
- Crossing economic-nexus revenue threshold in a state (e.g., CA $735K 2026).
- Year-end state-by-state nexus footprint review (typically Q4 close).
- PTET (SALT cap workaround) election analysis per state.
- Throwback rule analysis: sales to non-taxing states throw back to origin.
- Trigger phrases: "state apportionment", "single-sales factor", "market-based sourcing", "throwback rule", "state nexus", "PTET election", "Wayfair", "cost-of-performance", "income tax nexus", "Form CT-3", "Form 1120-NJ".

NOT for: sales tax / use tax nexus (use `sales-tax-nexus-study-economic-physical` + `multistate-sales-tax-anrok-stripe-avalara`); transfer pricing (use `transfer-pricing-form-5471-8865-5472`); state notice response (use `irs-state-dor-notice-response`).

## Setup

### Vertex Income Tax — enterprise apportionment dashboard

```bash
export VERTEX_API_KEY="..."
curl -H "Authorization: Bearer $VERTEX_API_KEY" \
  https://api.vertexinc.com/income-tax/v1/apportionment
```

### Avalara Income Tax — state apportionment + filing

```bash
export AVALARA_API_KEY="..."
curl -H "Authorization: Bearer $AVALARA_API_KEY" \
  https://api.avalara.com/income-tax/v1/state-filings
```

### Sphere — apportionment + nexus + filing unified

```bash
export SPHERE_API_KEY="..."
curl -H "Authorization: Bearer $SPHERE_API_KEY" \
  https://api.sphere.co/v1/income-tax/apportionment
```

### Bloomberg State Tax Navigator — research subscription

```bash
# Web subscription; no public API
# https://www.salt.com/
# Use for state-by-state apportionment formula + sourcing rule research
```

### Source-data inputs (agent pulls from MCPs)

- Revenue by destination state: `stripe-mcp` (Sigma queries) + `xero-mcp`
- Headcount by state: HRIS (Gusto / Rippling / Deel) via `cli-anything`
- Property by state: fixed-asset register from `xero-mcp` / NetSuite

## Common recipes

### Recipe 1 — State economic nexus threshold check

```python
# 2026 state income tax economic nexus thresholds
income_tax_nexus_2026 = {
    "CA": {"sales": 735_019, "property": 86_000, "payroll": 86_000},  # CPI-adj
    "MA": {"sales": 500_000},
    "TX": {"sales": 500_000},      # margin tax
    "WA": {"sales": 100_000},      # B&O
    "NY": {"sales": 1_272_000},    # 2026 CPI-adj
    "IL": {"sales": 100_000, "txns": 200},
    "TN": {"sales": 500_000},      # F&E
    "HI": {"sales": 100_000, "txns": 200},
    "KS": {"sales": 250_000},
    "MI": {"sales": 350_000},
    "OH": {"sales": 150_000},      # CAT
    "PA": {"sales": 500_000},
    "RI": {"sales": 1_000_000},
    "VA": {"sales": 500_000},
    "WI": {"sales": 100_000, "txns": 200},
}

# Test recipient against each state
recipient_sales_by_state = {"CA": 825_000, "MA": 220_000, "TX": 690_000}
nexus_triggered = {
    state: data for state, data in income_tax_nexus_2026.items()
    if recipient_sales_by_state.get(state, 0) >= data.get("sales", float("inf"))
}
print(f"Income-tax nexus triggered: {list(nexus_triggered.keys())}")
```

### Recipe 2 — Single-sales-factor apportionment

```python
# Most common formula 2026: single-sales-factor (~32 states)
# Apportionment % = state sales / total sales

total_sales = 12_500_000
state_sales = {
    "CA": 2_400_000,
    "NY": 1_850_000,
    "TX": 1_100_000,
    "FL": 980_000,
    "WA": 720_000,
    "IL": 650_000,
    "MA": 540_000,
    # ...
}

apportionment = {
    state: sales / total_sales
    for state, sales in state_sales.items()
}
# E.g., CA: 19.2%; NY: 14.8%; ...
```

### Recipe 3 — Three-factor apportionment (legacy / minority states)

```python
# Three-factor formula: (property + payroll + sales) / 3
# 2026 three-factor states: AK, AR, FL (corp), HI, ID, KS (option), MA (manufactr),
# MT, NM, ND (3F service), TX (margin), WY

state = "TX"
factors = {
    "property": state_property_value / total_property_value,
    "payroll": state_payroll / total_payroll,
    "sales": state_sales / total_sales,
}
apportionment_pct = sum(factors.values()) / 3

# Some states double-weight sales (effectively 4-factor with sales weighted 2x):
# E.g., MA double-weighted: (property + payroll + 2*sales) / 4
ma_double_weighted = (factors["property"] + factors["payroll"] 
                      + 2 * factors["sales"]) / 4
```

### Recipe 4 — Market-based sourcing vs cost-of-performance for services / SaaS

```python
# Market-based: source revenue to BUYER's state
# Cost-of-performance: source revenue to state where MOST cost incurred (often HQ)
# Critical for SaaS — different sourcing → wildly different apportionment

# Market-based states 2026:
market_based_states = {
    "AL", "CA", "CT", "DC", "GA", "IL", "IA", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MO", "NE", "NJ", "NY", "NC", "OH", "OK", "OR",
    "PA", "RI", "TN", "UT", "VT", "WA", "WI",
}
# Cost-of-performance states 2026:
cop_states = {
    "AK", "AZ", "AR", "CO", "FL", "HI", "ID", "IN", "KS", "MT", "NV",
    "NH", "NM", "ND", "SC", "SD", "TX", "VA", "WV", "WY",
}

# For SaaS revenue $X to CA buyer:
# - CA (market-based): source $X to CA → CA apportionment factor includes
# - TX (cost-of-perf): source $X to TX if dev team in TX

# Some "primary benefit" gray area — engage state-tax advisor for ambiguous services
```

### Recipe 5 — Throwback + throwout rules

```python
# Throwback rule: sales to states where NO income-tax nexus
# → "thrown back" to origin state for apportionment
# Throwout rule: alternative — EXCLUDE such sales from denominator

throwback_states_2026 = {
    "AL", "AR", "AK", "CA", "HI", "ID", "IL", "IN", "KS", "LA", "ME",
    "MA", "MS", "MO", "NE", "NH", "NM", "ND", "OK", "OR", "PA", "RI",
    "UT", "VT", "WI",
}
throwout_states_2026 = {"ME", "NJ", "OR"}  # OR partial

# E.g., CA seller, $300K sales to a state where no nexus
# → throwback adds $300K to CA numerator
recipient_origin = "CA"
nowhere_sales = 300_000
if recipient_origin in throwback_states_2026:
    # add $300K to CA apportionment numerator
    ca_throwback_addition = nowhere_sales
```

### Recipe 6 — PTET (Pass-through Entity Tax) election analysis

```python
# PTET workaround for $10K SALT cap (TCJA + OBBB-extended)
# Pass-through pays state tax at ENTITY level → fully deductible federally
# Owner gets credit on individual state return

# 2026 PTET-electing states (~36): NY, NJ, CA, CT, MD, MA, GA, IL, ...

# Example: CA PTET (Form 3804)
qbi_apportioned_ca = 850_000
ca_tax_rate = 0.093  # individual top rate
ptet_at_entity = qbi_apportioned_ca * ca_tax_rate  # $79,050
# Entity deducts $79K federally (no SALT cap)
# Owner receives CA PTE credit of $79K on Form 540

# Cost-benefit analysis:
fed_marginal = 0.37
ptet_federal_savings = ptet_at_entity * fed_marginal  # $29,249/yr
# Election typically beneficial for >$200K state-apportioned QBI
```

### Recipe 7 — State NOL coordination

```python
# Most states allow NOL but rules vary:
# - Pre-apportionment NOL (CA, NJ): apply NOL before apportionment
# - Post-apportionment NOL (NY, IL): apportion taxable income first, then NOL

# State-by-state NOL carryforward periods (2026):
state_nol_periods = {
    "CA": "indefinite",   # 80% limit
    "NY": 20,             # post-2015
    "IL": 12,             # post-2003
    "MA": 5,
    "GA": "indefinite",
    "NJ": 20,             # post-2018
    "PA": 20,             # 40% limit per yr
}
# Track separately in xlsx per-state NOL register
```

### Recipe 8 — Combined / unitary vs separate filing

```python
# Combined / unitary: file consolidated state return for unitary group
# (related entities sharing functional integration, centralized management, economies of scale)
# States requiring combined: CA, IL, KS, MA, MI, NH, NY, OR, UT, WI, ...
# Separate-return states: AL, AR, CT, DC, FL, GA, IN, IA, KY, LA, MD,
#   MS, MO, MT, NE, NM, NC, ND, OH, OK, PA, RI, SC, TN, TX, VA, WV

# Worldwide vs water's-edge election:
# Worldwide combined: include all foreign affiliates (CA / ND option)
# Water's edge: exclude foreign affiliates with limited US activity (default)
```

### Recipe 9 — State-level filing portal map

```python
state_filing_portals = {
    "CA": "https://www.ftb.ca.gov/file/business/index.html",  # CA FTB
    "NY": "https://www.tax.ny.gov/online/bus.htm",
    "TX": "https://comptroller.texas.gov/taxes/franchise/",
    "FL": "https://floridarevenue.com/taxes/eservices",
    "MA": "https://mtc.dor.state.ma.us/mtc/_/",
    "GA": "https://gtc.dor.ga.gov/",
    "IL": "https://mytax.illinois.gov/",
    "NJ": "https://www.state.nj.us/treasury/taxation/",
    "PA": "https://mypath.pa.gov/",
    "OH": "https://gateway.ohio.gov/",  # OH CAT
    # all: register, file, pay
}
```

### Recipe 10 — Apportionment factor pull from data sources

```python
# Build per-state factors from MCP / API data
import pandas as pd

# Revenue by destination state (Stripe Sigma + Xero)
revenue_by_state = stripe_sigma.query("""
    SELECT customer_address_state, SUM(amount) AS revenue
    FROM charges WHERE created BETWEEN '2026-01-01' AND '2026-12-31'
    GROUP BY 1
""")

# Headcount + payroll by state (Gusto)
payroll_by_state = gusto_client.get_payroll_by_state(year=2026)

# Property by state (fixed-asset register from Xero)
property_by_state = xero_client.get_fixed_assets_by_location()

# Combine
factors = pd.merge(revenue_by_state, payroll_by_state, on="state", how="outer")
factors = pd.merge(factors, property_by_state, on="state", how="outer")
factors.fillna(0, inplace=True)
```

## Examples

### Example 1: 5-state SaaS apportionment

**Goal:** $12.5M revenue SaaS C-corp. Customers in CA, NY, TX, IL, FL. HQ in CA (15 employees), remote in NY (3), TX (4), IL (2), FL (1).

**Steps:**
1. Recipe 1: nexus check → CA, NY, TX, IL, FL all triggered (sales > thresholds + physical presence via remote employees).
2. Recipe 2 single-sales factor states (CA, NY, IL): apportion by sales only.
   - CA: $4.2M / $12.5M = 33.6%
   - NY: $3.1M / $12.5M = 24.8%
   - IL: $1.4M / $12.5M = 11.2%
3. TX margin tax (Recipe 3): three-factor; tax base = lesser of (70% revenue, 100% revenue − COGS, 100% revenue − compensation).
4. FL three-factor (Recipe 3): include property + payroll + sales for FL.
5. Recipe 4 market-based sourcing for CA / NY / IL → customer-state sourcing.
6. Total state tax: ~$425K aggregate across 5 states (CA $182K, NY $116K, IL $48K, TX $52K, FL $27K).

**Result:** State returns filed CA (Form 100), NY (CT-3), TX (05-158-A), IL (IL-1120), FL (F-1120). Estimated payments configured for 2027.

### Example 2: PTET election for $1.2M LLC profits

**Goal:** LLC taxed as partnership, $1.2M operating income. Two members: 70% CA resident, 30% NY resident. Considering CA + NY PTET elections to bypass SALT cap.

**Steps:**
1. Recipe 6 cost-benefit:
   - CA portion: $840K * 9.3% PTET = $78,120 entity tax → $28,904 fed deduction savings.
   - NY portion: $360K * 10.9% PTE = $39,240 entity tax → $14,519 fed deduction savings.
2. Both elections beneficial — total fed savings ~$43,000.
3. Election deadlines: CA Form 3804 due original due date (Mar 15) for tax year; NY irrevocable election due Mar 15.
4. Recipe 9 portals: CA FTB online + NY DTF.
5. Q1 + Q2 PTET estimates due Q3/Q4 prior year (CA) or with return (NY).

**Result:** CA + NY PTET elections filed; entity-level tax payments scheduled; partner K-1s reflect PTE credit for state returns.

### Example 3: Throwback rule penalty avoidance

**Goal:** CA-headquartered manufacturer ships to AZ, NV, OR. NV has no income tax. CA = throwback state.

**Steps:**
1. Recipe 5: NV sales ($380K) THROWN BACK to CA apportionment numerator.
2. Without throwback: CA apportionment % = $2.1M / $4.5M = 46.7%.
3. With throwback: ($2.1M + $380K) / $4.5M = 55.1% — 8.4 ppt higher CA apportionment.
4. Restructure consideration:
   - Establish NV nexus voluntarily (open NV office) → escapes throwback.
   - OR move HQ out of CA to non-throwback state (UT or AZ).

**Result:** Documented throwback impact $400K CA taxable income; restructure economic analysis prepared for management.

## Edge cases / gotchas

- **PL 86-272 federal protection erosion:** MTC revised Statement of Information August 2021 — "Internet-based" customer service activities (FAQ pages, online help) may now constitute non-protected activity. CA + NY adopted aggressive interpretation. SaaS often outside PL 86-272 entirely.
- **Wayfair adoption for income tax** varies — many states still phasing in. CA $735K threshold ≠ Wayfair sales-tax $500K threshold.
- **Multistate Tax Commission (MTC) compact** members use UDITPA (Uniform Division of Income for Tax Purposes Act) formulas. Non-members (e.g., NY, IL) diverge.
- **Single-sales-factor traps:** in market-based states, low-revenue ≠ low-apportionment. Heavy product sales to CA + light presence still creates CA apportionment.
- **Throwback rules apply only to TANGIBLE PROPERTY sales** in most states. Services / SaaS less commonly subject.
- **Cost-of-performance "majority" vs "preponderance":** legacy COP states diverge — some use "majority" (>50%), some "preponderance" (largest portion).
- **PTET elections often IRREVOCABLE:** NY (annual irrevocable by Mar 15), CA (annually pre-payment due). Late elections may not be accepted.
- **K-1 attachments for PTET:** owners need PTET credit info from K-1 supplement to claim on individual state returns. Software (Drake, ProConnect, etc.) handles.
- **Combined-group filing requires unitary determination:** facts-and-circumstances. Centralized management, functional integration, economies of scale tests.
- **State-source income tax for foreign-resident shareholders:** S-corp non-US-resident shareholder = automatic S-election termination + state-level mess.
- **Composite returns** — partnerships file ONE consolidated state return for non-resident partners (some states; e.g., NY IT-203-S; CA 540-NR composite).
- **Estimated tax safe harbor** varies state-by-state — most use 100% of prior-year liability OR 90% of current. CA: 30/40/0/30 quarterly weighting.
- **Mobile workforce + state withholding:** employer must withhold for state where work performed (not residency). > 30-day rule in many states triggers withholding.
- **Single-tax-paid credit rules:** state credits for tax paid to other states often capped at home-state rate; complex with PTET.

> WARNING **This is informational guidance from an AI agent. Always consult a licensed CPA or tax attorney in your jurisdiction before filing returns, claiming credits, or implementing binding tax positions.**

## Sources

- Avalara State Income Tax Apportionment whitepaper: https://www.avalara.com/us/en/learn/whitepapers/state-income-tax-apportionment.html
- Vertex Income Tax: https://www.vertexinc.com/products/income-tax
- Bloomberg State Tax Navigator (SALT): https://www.salt.com/
- Multistate Tax Commission (MTC): https://www.mtc.gov/the-commission/multistate-tax-compact
- MTC PL 86-272 Statement (Aug 2021 revised): https://www.mtc.gov/uploadedFiles/Multistate_Tax_Commission/Uniformity_Projects/A_-_Z/Public_Law_86-272/Statement-of-Information-Concerning-Practices-of-Multistate-Tax-Commission-and-Signatory-States.pdf
- Tax Notes State research: https://www.taxnotes.com/research/federal/state-tax-treatment-corporate-income
- AICPA State Tax Resources: https://www.aicpa.org/topic/tax/state-tax
- Sphere (apportionment + nexus): https://sphere.co/

## Related skills

- `sales-tax-nexus-study-economic-physical` — sales tax vs income tax nexus differences
- `multistate-sales-tax-anrok-stripe-avalara` — companion sales tax filing
- `form-1120-corp-income-tax-filing` — federal apportionment companion
- `form-1065-1120s-passthrough-filing` — PTET pass-through election
- `transfer-pricing-form-5471-8865-5472` — intercompany pricing across states
- `irs-state-dor-notice-response` — state DOR notice handling
