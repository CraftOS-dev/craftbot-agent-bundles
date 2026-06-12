<!--
Source: https://www.salestaxinstitute.com/resources/economic-nexus-state-guide
Source: https://www.numeral.com/blog/economic-nexus-thresholds-by-state
Source: https://www.salestaxhandbook.com/economic-nexus
Source: https://www.supremecourt.gov/opinions/17pdf/17-494_j4el.pdf
Reference role.md: "Sales tax nexus study"
-->

# Sales tax nexus study — economic + physical + marketplace facilitator

Comprehensive nexus mapping per state combining (a) economic thresholds post-Wayfair (typically $100K rev OR 200 txns; CA $500K), (b) physical presence (office, employee, inventory, contractor in-state), (c) marketplace facilitator laws (Amazon/Etsy/Shopify Marketplace absorb in some states), (d) trailing 12-month rolling tests, (e) product taxability per jurisdiction. Outputs: nexus heat-map + recommended registrations + VDA exposure estimate.

## When to use

- New market entry to a state (assessing nexus exposure).
- Post-Wayfair compliance audit (have we registered everywhere we have nexus).
- Pre-fundraise diligence on sales tax exposure.
- M&A diligence (target's nexus footprint).
- Adding employees / offices in new states (physical nexus).
- Marketplace facilitator law evaluation (Amazon / Etsy / Shopify Marketplace).
- Trigger phrases: "nexus", "nexus study", "Wayfair", "economic nexus", "physical nexus", "marketplace facilitator", "VDA", "voluntary disclosure", "back tax exposure".

NOT for: actual sales tax filing (use `multistate-sales-tax-anrok-stripe-avalara`); income tax nexus (use `state-apportionment-nexus-analysis`); state DOR notice response (use `irs-state-dor-notice-response`).

## Setup

### Anrok (nexus dashboard)

```bash
# Anrok built-in nexus monitoring
export ANROK_API_KEY="..."
curl -H "Authorization: Bearer $ANROK_API_KEY" \
  https://api.anrok.com/v1/jurisdictions/obligations
```

### Sphere (nexus + use tax + business licenses)

```bash
export SPHERE_API_KEY="..."
curl -H "Authorization: Bearer $SPHERE_API_KEY" \
  https://api.sphere.co/v1/nexus
```

### Numeral (AI nexus monitoring)

```bash
export NUMERAL_API_KEY="..."
curl -H "Authorization: Bearer $NUMERAL_API_KEY" \
  https://api.numeral.com/v1/nexus
```

### Avalara nexus assessment

```bash
export AVATAX_ACCOUNT="..."
export AVATAX_LICENSE_KEY="..."
curl -u "$AVATAX_ACCOUNT:$AVATAX_LICENSE_KEY" \
  https://rest.avatax.com/api/v2/nexus
```

## Economic nexus thresholds (2026)

| State | Revenue threshold | Transaction threshold | Both required? |
|---|---|---|---|
| Alabama | $250,000 | n/a | — |
| Alaska | $100,000 | 200 | OR |
| Arizona | $100,000 | n/a | — |
| Arkansas | $100,000 | 200 | OR |
| California | $500,000 | n/a | — |
| Colorado | $100,000 | n/a | — |
| Connecticut | $100,000 | 200 | AND |
| DC | $100,000 | 200 | OR |
| Florida | $100,000 | n/a | — |
| Georgia | $100,000 | 200 | OR |
| Hawaii | $100,000 | 200 | OR |
| Idaho | $100,000 | n/a | — |
| Illinois | $100,000 | 200 | OR |
| Indiana | $100,000 | n/a | — |
| Iowa | $100,000 | n/a | — |
| Kansas | $100,000 | n/a | (raised from $0 in 2024) |
| Kentucky | $100,000 | 200 | OR |
| Louisiana | $100,000 | 200 | OR |
| Maine | $100,000 | n/a | — |
| Maryland | $100,000 | 200 | OR |
| Massachusetts | $100,000 | n/a | — |
| Michigan | $100,000 | 200 | OR |
| Minnesota | $100,000 | 200 | OR |
| Mississippi | $250,000 | n/a | — |
| Missouri | $100,000 | n/a | (newest — Jan 2023) |
| Nebraska | $100,000 | 200 | OR |
| Nevada | $100,000 | 200 | OR |
| New Jersey | $100,000 | 200 | OR |
| New Mexico | $100,000 | n/a | — |
| New York | $500,000 | 100 | AND |
| North Carolina | $100,000 | 200 | OR |
| North Dakota | $100,000 | n/a | — |
| Ohio | $100,000 | 200 | OR |
| Oklahoma | $100,000 | n/a | — |
| Pennsylvania | $100,000 | n/a | — |
| Rhode Island | $100,000 | 200 | OR |
| South Carolina | $100,000 | n/a | — |
| South Dakota | $100,000 | n/a | — |
| Tennessee | $100,000 | n/a | — |
| Texas | $500,000 | n/a | — |
| Utah | $100,000 | 200 | OR |
| Vermont | $100,000 | 200 | OR |
| Virginia | $100,000 | 200 | OR |
| Washington | $100,000 | n/a | — |
| West Virginia | $100,000 | 200 | OR |
| Wisconsin | $100,000 | n/a | — |
| Wyoming | $100,000 | 200 | OR |

States WITHOUT sales tax: Delaware, Montana, New Hampshire, Oregon.

## Common recipes

### Recipe 1 — 12-month rolling revenue + transaction by state

```python
import pandas as pd
sales_by_state = pd.read_sql("""
SELECT shipping_state,
       SUM(amount_total) / 100 AS revenue_12mo,
       COUNT(*) AS transactions_12mo,
       MAX(created) AS last_sale_date,
       MIN(created) AS first_sale_date
FROM stripe_invoices
WHERE created BETWEEN NOW() - INTERVAL '12 months' AND NOW()
  AND paid = true
GROUP BY shipping_state
""", db)

THRESHOLDS = {
    "CA": (500_000, None, "OR"),
    "TX": (500_000, None, "OR"),
    "NY": (500_000, 100, "AND"),
    "AL": (250_000, None, "OR"),
    "MS": (250_000, None, "OR"),
    # default $100K OR 200
}

def nexus_triggered(row):
    rev_t, txn_t, mode = THRESHOLDS.get(row.shipping_state, (100_000, 200, "OR"))
    if mode == "AND":
        return (row.revenue_12mo >= rev_t) and (row.transactions_12mo >= (txn_t or 0))
    if rev_t and row.revenue_12mo >= rev_t: return True
    if txn_t and row.transactions_12mo >= txn_t: return True
    return False

sales_by_state["nexus"] = sales_by_state.apply(nexus_triggered, axis=1)
nexus_states = sales_by_state[sales_by_state.nexus].shipping_state.tolist()
```

### Recipe 2 — Threshold proximity alert

```python
# Identify states approaching but not yet over threshold
sales_by_state["pct_of_threshold"] = sales_by_state.apply(
    lambda r: r.revenue_12mo / THRESHOLDS.get(r.shipping_state, (100_000, 200, "OR"))[0],
    axis=1
)
approaching = sales_by_state[
    (sales_by_state.pct_of_threshold >= 0.70) 
    & (sales_by_state.pct_of_threshold < 1.00)
]
# Alert team to prepare registration in advance
```

### Recipe 3 — Physical nexus map

```python
# Physical nexus triggers (any of):
#  - Office or fixed place of business
#  - W-2 employee (even remote work-from-home)
#  - Inventory (incl. Amazon FBA fulfillment center)
#  - Contractor performing services in state
#  - Travel for sales calls in state (some states)
#  - Property ownership / lease

physical_nexus_by_state = {}

# Pull from HRIS (Gusto / Rippling)
employees_by_state = pull_from_hris()
for emp in employees_by_state:
    physical_nexus_by_state.setdefault(emp.state, []).append(
        {"trigger": "W-2 employee", "name": emp.name, "since": emp.hire_date}
    )

# Pull office locations
offices = entity_records["physical_locations"]
for o in offices:
    physical_nexus_by_state.setdefault(o.state, []).append(
        {"trigger": "Office", "address": o.address, "since": o.lease_start}
    )

# Pull Amazon FBA inventory (Amazon API)
fba_states = amazon_fba_inventory_states()
for s in fba_states:
    physical_nexus_by_state.setdefault(s, []).append(
        {"trigger": "FBA inventory", "warehouse": "Amazon"}
    )
```

### Recipe 4 — Combined nexus heat map

```python
# Merge economic + physical for full nexus map
all_states = set(sales_by_state.shipping_state).union(physical_nexus_by_state.keys())
heat_map = []
for state in all_states:
    economic = state in nexus_states
    physical = state in physical_nexus_by_state
    saas_taxable = SAAS_TAXABILITY[state]  # from multistate skill
    
    needs_registration = (economic or physical) and saas_taxable
    
    heat_map.append({
        "state": state,
        "economic_nexus": economic,
        "physical_nexus": physical,
        "saas_taxable": saas_taxable,
        "registration_required": needs_registration,
        "physical_trigger": physical_nexus_by_state.get(state, []),
    })

pd.DataFrame(heat_map).to_excel("nexus_heatmap_2026Q2.xlsx", index=False)
```

### Recipe 5 — Marketplace facilitator carve-out

```python
# 45+ states require marketplace facilitators (Amazon, Etsy, eBay, Shopify Mkt,
#   Walmart, DoorDash, Uber Eats) to collect+remit on behalf of 3rd-party sellers
# If you sell ONLY through marketplace → marketplace handles tax
# If you sell direct AND through marketplace → only direct sales count

# Pull marketplace settlement data
amazon_sales = amazon_settlement_report["sales"]
etsy_sales = etsy_payments_report["sales"]
shopify_marketplace_sales = shopify_pos_sales_marketplace_only

# Pull direct sales (your Stripe / direct checkout)
direct_sales = sales_by_state  # from Recipe 1

# For nexus test, use only DIRECT sales (marketplace excluded in mkt facilitator states)
direct_sales_post_mkt_carve_out = direct_sales.copy()
```

### Recipe 6 — VDA (Voluntary Disclosure Agreement) exposure estimate

```python
# If had nexus but didn't register → owe back tax + interest + penalties
# VDA negotiates: 3-4 yr lookback + waived penalties + reduced interest

import pandas as pd
back_period_exposure = pd.read_sql("""
SELECT shipping_state,
       SUM(amount_total) / 100 AS sales_4yr,
       COUNT(*) AS txns_4yr
FROM stripe_invoices
WHERE created BETWEEN NOW() - INTERVAL '4 years' AND NOW()
  AND paid = true
  AND shipping_state IN ('NY','PA','WA','TX')  -- nexus unregistered
GROUP BY shipping_state
""", db)

# Estimate back tax = sales × avg state+local rate × taxability ratio
back_period_exposure["estimated_back_tax"] = (
    back_period_exposure.sales_4yr 
    * back_period_exposure.shipping_state.map(STATE_AVG_RATE)
    * back_period_exposure.shipping_state.map(SAAS_TAXABLE_PCT)
)

# Plus interest @ ~6-8% per state, plus penalties (waivable via VDA)
# VDA typical cost via Anrok / Sphere: $1-3K per state
```

### Recipe 7 — Nexus look-back period by state

```python
# Most states' SOL = 3-4 yrs for collected-but-not-remitted; INDEFINITE for non-filed
STATE_LOOKBACK = {
    "CA": "8 years (no filing)",
    "NY": "3 years (filing) / unlimited (no filing)",
    "TX": "4 years",
    "FL": "3 years",
    "WA": "4 years",
    # ...
}

# VDA typical settles to 3-4 yr lookback regardless
```

### Recipe 8 — Click-through / affiliate nexus (legacy)

```python
# Pre-Wayfair (and still active in some states): click-through nexus 
#  if affiliate in state generates $10K+ sales
# Most states now obsoleted by economic nexus rules
# Still check: NY, IL, CT, RI, AR, NC, ME, MN, MO, OH, PA, VT

# Most modern SaaS scenarios = economic nexus dominates
```

### Recipe 9 — Prepare for state DOR audit

```python
# Substantiation file per nexus state:
audit_file = {
    "registration_date": "2025-06-15",
    "first_taxable_sale_date": "2025-05-22",
    "voluntary_disclosure": "Filed VDA with state DOR May 2025",
    "sales_data_extracts": ["stripe_export_2024.csv", "shopify_export_2024.csv"],
    "exemption_certificates_on_file": 12,
    "use_tax_returns_filed": ["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025"],
    "back_period_settlement_letter": "vda_settlement_2025-06.pdf",
}
```

### Recipe 10 — Multi-product taxability mix

```python
# If selling SaaS + services + physical goods + downloads:
# Taxability matrix per state × product
TAXABILITY_MATRIX = {
    "saas":               {"NY": True, "TX": True, "CA": False, "FL": False, ...},
    "professional_svc":   {"NY": False, "TX": True, "CA": False, "FL": False, ...},
    "digital_download":   {"NY": True, "TX": True, "CA": False, "FL": False, ...},
    "physical_book":      {"NY": True, "TX": True, "CA": True, "FL": True, ...},
    "training":           {"NY": True, "TX": False, "CA": False, "FL": False, ...},
}
# Allocate revenue per product per state for accurate nexus calc
```

## Examples

### Example 1: Series A SaaS doing nexus study pre-fundraise

**Goal:** $4.2M ARR, scattered across 30 states. Investors asking for sales tax compliance.

**Steps:**

1. Recipe 1: pull 12-mo revenue + txns by state → 14 states cross economic nexus.
2. Recipe 3: physical nexus → CA office, employees in TX/WA/NY/MA/CO/IL → 7 states.
3. Recipe 4: combined heat map → 17 states with nexus + 11 of those tax SaaS.
4. Currently registered: 4 of 11 → exposure in 7 states.
5. Recipe 6: VDA exposure: ~$285K back tax across 7 states (4-yr lookback).
6. Recommend: VDA via Anrok ($21K all-in, $1.5K + filing fees per state).
7. Recipe 9: build audit substantiation file per state.
8. Register prospectively via Anrok in all 7 + monitor remaining 6 non-SaaS-taxable states.

**Result:** Nexus mapped, VDA negotiated, registered, future filings automated.

### Example 2: Marketplace seller using Amazon FBA, evaluating direct sales risk

**Goal:** Amazon FBA inventory in 8 states + own DTC website with $80K/yr direct sales.

**Steps:**

1. Amazon FBA inventory triggers physical nexus in 8 states (NY, PA, WA, TN, NV, IN, FL, AZ).
2. Amazon marketplace facilitator laws: Amazon collects+remits on FBA sales.
3. Own direct sales $80K/yr — below $100K economic threshold; no economic nexus.
4. BUT physical nexus from FBA still triggers tax obligation on DIRECT sales in those 8 states.
5. Register in 8 FBA states; configure Anrok / Stripe Tax for direct sales calc.
6. Marketplace Amazon sales: no double-collection.

**Result:** Direct-sale tax obligation covered; marketplace sales handled by Amazon.

### Example 3: M&A target nexus diligence

**Goal:** Acquirer's tax diligence on target's sales tax exposure.

**Steps:**

1. Request target's 4-yr sales + tax data by state.
2. Recreate Recipe 1 + 3 + 4 from target data.
3. Identify nexus gaps (registered vs. should-have-been registered).
4. Estimate back-period exposure (Recipe 6).
5. Negotiate purchase price adjustment OR escrow holdback for exposure.
6. Post-close: VDA in newly identified states; allocate to seller's representations.

**Result:** Exposure quantified; price/escrow adjusted; post-close cleanup planned.

## Edge cases / gotchas

- **Wayfair thresholds change annually:** Kansas raised to $100K in 2024; Louisiana raised similarly. Monitor.
- **Marketplace facilitator carveout uneven:** check each state — some require marketplace seller to ALSO register (e.g., for reporting), some fully absorb.
- **Trailing 12 months vs calendar year:** most states use trailing 12-month rolling; some use calendar/fiscal year (CA, others). Read each state's rule.
- **Wholesale sales count toward threshold (some states):** WA, OH, NV use gross receipts including wholesale. Exempt sales DON'T trigger tax due, but count toward nexus.
- **Drop-shipping triggers nexus differently:** if vendor drop-ships from out-of-state warehouse to in-state customer, vendor's inventory location may not trip nexus, but vendor still has tax obligation in destination state.
- **Inventory in third-party warehouse:** Amazon FBA, ShipBob, etc. — your inventory creates nexus even though you don't own the warehouse.
- **Remote worker = physical nexus:** even one W-2 employee remote in state = physical nexus. Affects payroll registration too.
- **Trade show attendance:** in some states (KS, OK historically), attending trade shows triggered nexus. Mostly resolved post-Wayfair but watch state by state.
- **Affiliate marketing:** click-through nexus laws still active in some states; mostly subsumed by economic nexus.
- **Hawaii GET (General Excise Tax):** not a sales tax; applies to all gross receipts incl. services. Different rules.
- **B2B vs B2C:** some states tax SaaS B2C only (Connecticut). Allocate by customer.
- **Free trial periods:** generally not taxable. Confirm per state.
- **Refunds:** typically reduce taxable sales in period of refund.
- **Bundled transactions:** mixed-taxability bundles require allocation rule per state (some use "true object test", some "primary use").
- **VDA "voluntary":** if state has CONTACTED you (even informally), no longer voluntary; VDA option lost.
- **Streamlined Sales Tax (SST) member states:** simplified registration via SST CSP (Certified Service Provider). 24 member states.

> WARNING **This is informational guidance from an AI agent. Always consult a licensed CPA or tax attorney in your jurisdiction before filing returns, claiming credits, or implementing binding tax positions.**

## Sources

- Sales Tax Institute Economic Nexus State Guide: https://www.salestaxinstitute.com/resources/economic-nexus-state-guide
- Sales Tax Institute SaaS taxability map: https://www.salestaxinstitute.com/resources/sales-taxability-saas
- Numeral state nexus thresholds: https://www.numeral.com/blog/economic-nexus-thresholds-by-state
- Sales Tax Handbook economic nexus: https://www.salestaxhandbook.com/economic-nexus
- South Dakota v. Wayfair (2018): https://www.supremecourt.gov/opinions/17pdf/17-494_j4el.pdf
- Streamlined Sales Tax Agreement: https://www.streamlinedsalestax.org/
- Anrok nexus monitoring: https://anrok.com/product/nexus
- Avalara Sales Tax Risk Assessment: https://www.avalara.com/us/en/products/sales-and-use-tax/nexus-determination.html
- TaxJar nexus state guide: https://www.taxjar.com/sales-tax/nexus
- Marketplace facilitator laws by state: https://www.salestaxinstitute.com/resources/marketplace-facilitator-state-guidance

## Related skills

- `multistate-sales-tax-anrok-stripe-avalara` — filing, registration, remittance
- `state-apportionment-nexus-analysis` — income tax nexus separate
- `irs-state-dor-notice-response` — state DOR notice / inquiry response
- `tax-audit-prep-response-federal-state` — substantiation library
