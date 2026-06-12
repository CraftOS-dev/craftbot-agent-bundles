<!--
Source: https://anrok.com/
Source: https://docs.stripe.com/tax
Source: https://www.avalara.com/
Source: https://www.numeral.com/
Source: https://sphere.co/
Source: https://www.taxjar.com/
Reference role.md: "Sales tax / VAT compliance"
-->

# Multi-state sales tax — Anrok + Stripe Tax + Avalara + Numeral + Sphere

Full sales/use tax compliance stack: nexus monitoring, registration, calculation at checkout, periodic filing, remittance, VDA negotiation. Anrok ($100/mo Starter, SaaS-specific, 200+ jurisdictions); Stripe Tax (embedded with Stripe); Avalara (enterprise); Numeral (AI-first); Sphere (modern, also use tax + business licenses); TaxJar ($90/mo, e-com).

## When to use

- Multi-state sales tax registration + filing for SaaS / e-com / digital products.
- Post-Wayfair economic nexus monitoring (typically $100K rev OR 200 txns).
- Use tax self-assessment for out-of-state purchases.
- Voluntary Disclosure Agreement (VDA) for back-period exposure.
- Exemption certificate management (resellers, non-profits).
- Trigger phrases: "sales tax", "use tax", "nexus", "Anrok", "Stripe Tax", "Avalara", "Numeral", "Sphere", "remit", "VDA", "register", "Wayfair".

NOT for: corporate income tax (use `form-1120-corp-income-tax-filing`); state nexus for income tax (use `state-apportionment-nexus-analysis`); 1099 issuance (use `1099-k-misc-nec-w2-filing`); EU VAT-only without US footprint (use Quaderno / Paddle MoR).

## Platform selection matrix

| Need | Recommended | Cost |
|---|---|---|
| 100% Stripe customer, < 5 states | Stripe Tax | $0.50/txn after 50 free |
| SaaS-specific, multi-state, < $50M | Anrok | $100-$1000/mo by volume |
| Enterprise ERP (NetSuite, Sage) | Avalara | Custom, ~$1K/mo+ |
| AI-first, full registration + filing | Numeral | ~$500-2K/mo by volume |
| Sales + use + business licenses | Sphere | Custom |
| E-com physical goods | TaxJar | $90/mo Complete |
| Want full outsource (MoR) | Paddle / Lemon Squeezy | 5% + $0.50/txn |
| EU VAT | Quaderno or Avalara | $79+/mo |

## Setup

### Anrok

```bash
# Dashboard app.anrok.com → API keys
export ANROK_API_KEY="..."
curl -H "Authorization: Bearer $ANROK_API_KEY" \
  https://api.anrok.com/v1/transactions
```

### Stripe Tax

```bash
# Enable at dashboard.stripe.com/tax
# Uses standard Stripe API key
curl -X POST https://api.stripe.com/v1/tax/calculations \
  -u $STRIPE_API_KEY: \
  -d "currency=usd" \
  -d "line_items[0][amount]=10000" \
  -d "line_items[0][reference]=L1" \
  -d "customer_details[address][country]=US" \
  -d "customer_details[address][state]=NY" \
  -d "customer_details[address][postal_code]=10001"
```

### Avalara AvaTax

```bash
export AVATAX_ACCOUNT="..."
export AVATAX_LICENSE_KEY="..."
curl -u "$AVATAX_ACCOUNT:$AVATAX_LICENSE_KEY" \
  https://rest.avatax.com/api/v2/accounts/$AVATAX_ACCOUNT/companies
```

### Numeral

```bash
export NUMERAL_API_KEY="..."
curl -H "Authorization: Bearer $NUMERAL_API_KEY" \
  https://api.numeral.com/v1/nexus
```

### Sphere

```bash
export SPHERE_API_KEY="..."
curl -H "Authorization: Bearer $SPHERE_API_KEY" \
  https://api.sphere.co/v1/registrations
```

## SaaS taxability map (2026)

- **Taxes SaaS as standard rule:** NY, PA, TX, WA, SC, TN, UT, OH, IA, AZ, DC, KY, MS, NM, RI, SD, WV; CT B2C only.
- **Does NOT tax SaaS:** CA, FL, NV, MO, IL (most), MD (most), NJ, OR, NH, MT, AK.
- **Tax with caveats:** MA (specific software types), CO (varies), VA (specific).

Source: https://www.salestaxinstitute.com/resources/sales-taxability-saas

## Economic nexus thresholds (2026)

- **Most states:** $100K OR 200 transactions in 12-month period.
- **California:** $500K (no transaction count).
- **Texas:** $500K.
- **New York:** $500K AND 100 transactions (both required).
- **Kansas (recently raised):** $100K.
- **Tennessee:** $100K.

Full state list: https://www.salestaxinstitute.com/resources/economic-nexus-state-guide

## Common recipes

### Recipe 1 — Nexus footprint map (sales tax)

```python
# Pull 12-month revenue + txn count by ship-to state
import pandas as pd
sales_by_state = pd.read_sql("""
SELECT shipping_state AS state,
       SUM(amount_total) / 100 AS revenue,
       COUNT(*) AS transactions
FROM stripe_invoices
WHERE created >= NOW() - INTERVAL '12 months'
  AND paid = true
GROUP BY shipping_state
""", db)

THRESHOLDS = {
    "CA": (500_000, None), "TX": (500_000, None),
    "NY": (500_000, 100),  # both required
    # others default $100K OR 200 txns
}
def nexus_triggered(row):
    rev_t, txn_t = THRESHOLDS.get(row.state, (100_000, 200))
    if row.state == "NY":
        return row.revenue >= rev_t and row.transactions >= txn_t
    if rev_t and row.revenue >= rev_t: return True
    if txn_t and row.transactions >= txn_t: return True
    return False

sales_by_state["nexus"] = sales_by_state.apply(nexus_triggered, axis=1)
print(sales_by_state[sales_by_state.nexus])
```

### Recipe 2 — Anrok nexus monitoring

```bash
curl -H "Authorization: Bearer $ANROK_API_KEY" \
  https://api.anrok.com/v1/jurisdictions/obligations
# Returns: {state: {nexus_status, threshold_progress, days_until_register}}
```

### Recipe 3 — Calculate tax at checkout (Anrok)

```bash
curl -X POST https://api.anrok.com/v1/transactions \
  -H "Authorization: Bearer $ANROK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "inv_2026_001",
    "transaction_date": "2026-06-15",
    "customer": {
      "address": {"line1":"123 Main","city":"Austin","state":"TX",
                  "zip":"78701","country":"US"}
    },
    "line_items": [{
      "id": "l1",
      "product_id": "saas_pro_monthly",
      "amount": 9900,
      "quantity": 1
    }]
  }'
```

### Recipe 4 — Calculate tax (Stripe Tax)

```bash
# SaaS product tax code = txcd_10000000
curl -X POST https://api.stripe.com/v1/tax/calculations \
  -u $STRIPE_API_KEY: \
  -d "currency=usd" \
  -d "line_items[0][amount]=9900" \
  -d "line_items[0][tax_code]=txcd_10000000" \
  -d "customer_details[address][country]=US" \
  -d "customer_details[address][state]=TX" \
  -d "customer_details[address][postal_code]=78701"
```

Tax codes: https://docs.stripe.com/tax/tax-codes

### Recipe 5 — Register for sales tax in a new state (no direct API)

```python
# State registration mostly manual via state DOR portal
# Anrok / Sphere / Numeral provide "Registration Service" ($499-799 each)
# Direct registration cost: $0-$50 fee, 1-4 weeks processing

# Required info checklist:
required = {
    "ein": "12-3456789",
    "legal_name": "Acme SaaS Inc",
    "formation_state": "DE",
    "formation_date": "2024-03-15",
    "responsible_party_ssn": "...",  # owner SSN/ITIN
    "naics": "541512",
    "projected_revenue_in_state": 250_000,
    "products": "SaaS subscriptions",
    "first_sale_date": "2025-08-04",  # critical for back-period
}

# State-by-state registration links: https://www.taxadmin.org/state-tax-agencies
```

### Recipe 6 — Auto-file + remit (Anrok)

```bash
curl -H "Authorization: Bearer $ANROK_API_KEY" \
  https://api.anrok.com/v1/filings?status=upcoming
# Returns: {jurisdiction, period, due_date, projected_amount}
```

Anrok auto-files in all 200+ jurisdictions on the right cadence; recipient funds the remittance ACH.

### Recipe 7 — Reconcile sales tax payable to GL

```python
# Month-end reconciliation
import requests
anrok_collected = requests.get(
    f"https://api.anrok.com/v1/transactions/summary"
    f"?from=2026-05-01&to=2026-05-31",
    headers={"Authorization": f"Bearer {ANROK_API_KEY}"}
).json()["total_tax_collected"]

xero_payable = (xero_client.reports.balance_sheet(date="2026-05-31")
                .get_account("2200").balance)
diff = anrok_collected - xero_payable
assert abs(diff) < 5, f"Anrok-to-Xero variance: ${diff}"
```

### Recipe 8 — Voluntary Disclosure Agreement (VDA) for back-period

```python
# If you had nexus but didn't register, state can pursue back tax + penalties.
# VDA = limited lookback (typically 3-4 years) + waived penalties.
# Anonymous initial negotiation through tax practitioner / VDA provider.
# Anrok, Numeral, Sphere all offer VDA service: $1-3K per state typical.

vda_eligibility = {
    "no_prior_nexus_contact": True,    # state hasn't contacted you yet
    "voluntary_disclosure": True,
    "back_period_estimable": True,
    "willing_to_register_prospective": True,
}
# Estimate exposure:
exposure_per_state = pd.read_sql("""
SELECT shipping_state, SUM(amount) * 0.06 AS estimated_back_tax
FROM stripe_invoices
WHERE shipping_state IN ('NY','PA','WA','TX')  -- nexus states unregistered
  AND created >= NOW() - INTERVAL '4 years'
GROUP BY shipping_state
""", db)
```

### Recipe 9 — Exemption certificate management

```bash
# Resellers, non-profits exempt with valid certificate
curl -X POST https://api.anrok.com/v1/customers/$CUST_ID/exemptions \
  -H "Authorization: Bearer $ANROK_API_KEY" \
  -d '{
    "jurisdiction":"NY",
    "exemption_type":"reseller",
    "certificate_url":"https://docs.example.com/cert.pdf",
    "valid_through":"2027-06-30"
  }'

# Multi-state SST certificate (Streamlined Sales Tax Agreement)
# accepted in 24 SST member states with one form
```

### Recipe 10 — Use tax compliance

```python
# Use tax = self-assessed sales tax on out-of-state purchases
# without sales tax paid. Common for SaaS purchases from out-of-state vendors.

# Pull AP from Xero + corporate card transactions
ap_transactions = xero_client.get_invoices(account_type="payable")
use_tax_obligations = []
for inv in ap_transactions:
    if inv.tax_amount == 0 and inv.vendor_state != entity_home_state:
        if entity_state_taxes_category(inv.category):
            use_tax_obligations.append({
                "vendor": inv.vendor,
                "amount": inv.total,
                "use_tax_rate": state_use_tax_rate(entity_home_state),
                "use_tax_owed": inv.total * state_use_tax_rate(entity_home_state),
            })

# File via state DOR use tax return (annual or quarterly)
```

### Recipe 11 — Multi-jurisdiction filing calendar

```python
CADENCE = {
    ("CA", "low_volume"):    "annual",
    ("CA", "med_volume"):    "quarterly",
    ("CA", "high_volume"):   "monthly",
    ("TX", "low_volume"):    "quarterly",
    ("TX", "high_volume"):   "monthly",
    ("NY", "low_volume"):    "quarterly",
    ("NY", "high_volume"):   "monthly",
    # ...
}
# Generate forward-looking filing schedule
from datetime import date
calendar_2026 = []
for state in nexus_states:
    cadence = CADENCE.get((state, volume_tier(state)), "monthly")
    if cadence == "monthly":
        calendar_2026.extend([date(2026, m, 20) for m in range(1, 13)])
    elif cadence == "quarterly":
        calendar_2026.extend([date(2026, q, 31) for q in [4, 7, 10]])
```

### Recipe 12 — Marketplace facilitator handling

```python
# Marketplace facilitators (Amazon, Etsy, eBay, Shopify Marketplace, etc.)
# now required to collect+remit sales tax on behalf of 3rd-party sellers
# in 45+ states. Don't double-remit!

# Pull marketplace settlement reports (Amazon, Etsy CSV exports)
# Exclude these from your own sales-tax-collected revenue
marketplace_sales = amazon_settlement_report["total_marketplace_sales"]
your_direct_sales = stripe_invoices_filter(
    exclude_referral_source=["amazon", "etsy"]
)
# Only collect+file on your direct sales
```

## Examples

### Example 1: Series A SaaS triggering nexus in 12 new states

**Goal:** $4.2M ARR, ship-to addresses span 18 states. Identify + register + file.

**Steps:**

1. Pull sales-by-state (Recipe 1) → 12 states cross nexus thresholds.
2. Prioritize: 8 of 12 tax SaaS; CA, FL, NV, IL don't.
3. Engage Anrok for managed registration: 8 × $499 = $4K.
4. Configure Anrok at checkout for all states going forward.
5. VDA for back-period exposure: ~$1.5K/state × 4 states with material exposure = $6K (Recipe 8).
6. Reconcile monthly via Recipe 7.

**Result:** Registered everywhere required; back-period mitigated via VDA; future tax auto-filed.

### Example 2: Solo founder $200K ARR, US-only, Stripe-native

**Goal:** Minimum-touch sales tax for small SaaS.

**Steps:**

1. Enable Stripe Tax in dashboard.
2. Confirm tax codes per product (Recipe 4).
3. Add ship-to address collection in checkout.
4. Stripe Tax calculates + files in NY/TX/WA/PA only (nexus triggered).
5. Stripe Tax fee: $0.50/txn after 50/mo free.
6. Monthly reconcile (Recipe 7 with Stripe Tax endpoint).

**Result:** End-to-end automated; ~$30/mo fee at this volume.

### Example 3: Enterprise transition to Avalara

**Goal:** $80M revenue, NetSuite ERP, 28 nexus states, custom tax codes.

**Steps:**

1. Avalara AvaTax integration with NetSuite (out-of-box connector).
2. Map custom NetSuite product categories to Avalara tax codes.
3. Configure Avalara Returns for auto-file in 28 states.
4. Configure Avalara CertCapture for exemption certificates.
5. Monthly use tax accrual via Avalara.
6. Annual Avalara health check + cert audit.

**Result:** Fully automated multi-state sales/use tax at enterprise scale.

## Edge cases / gotchas

- **Wayfair thresholds shift:** states adjust thresholds (Kansas raised to $100K in 2024). Anrok/Avalara track; if DIY, audit annually.
- **Back-period exposure (VDA):** if you've had nexus but not registered, you owe back tax + penalties. VDA negotiates limited lookback. Anrok / Sphere / Numeral handle.
- **Marketplace facilitator laws:** if sold through Amazon/Etsy/etc., they may remit. Don't double-remit (Recipe 12).
- **Origin-based vs destination-based:** most states destination-based (ship-to). Origin states: TX, OH, MO, PA, NM. Affects rate calc.
- **Address validation:** wrong zip = wrong rate. Use validated addresses; reject if zip+state mismatch.
- **Bundled products:** mixed SaaS + professional services in mixed-taxability states require allocation.
- **EU VAT:** if selling to EU consumers, VAT applies regardless of physical presence. Threshold €10K/yr post-2021. Use OSS (One Stop Shop) for EU-wide reg.
- **Marketplace + MoR distinction:** Paddle / Lemon Squeezy are MoR — they're seller of record. You're not liable.
- **Filing zero-returns:** once registered, you MUST file even at $0 revenue. Missing zero-returns = penalty.
- **Free trial periods:** typically not taxable until first paid invoice. Verify per state.
- **Refund tax handling:** refunding requires refund filing in some states. Anrok / Stripe Tax handle.
- **Tax-included vs tax-exclusive pricing:** B2B almost always exclusive (line item plus tax). B2C may be inclusive in EU/UK.
- **Wholesale vs retail tax:** wholesale to resellers = exempt with valid cert; retail = tax due.
- **Out-of-state remote workers create physical nexus** (W-2 employee or even some contractor relationships). One developer in WA = nexus.
- **Hawaii GET (General Excise Tax)** is NOT a sales tax — it's a tax on gross receipts incl. service revenue not normally taxed elsewhere.
- **Local + district taxes:** Texas + CA + WA + others stack city/county/special-district taxes on top of state. ~13,000 US jurisdictions total.

> WARNING **This is informational guidance from an AI agent. Always consult a licensed CPA or tax attorney in your jurisdiction before filing returns, claiming credits, or implementing binding tax positions.**

## Sources

- Anrok: https://anrok.com/
- Stripe Tax docs: https://docs.stripe.com/tax
- Stripe tax codes: https://docs.stripe.com/tax/tax-codes
- Avalara: https://www.avalara.com/
- Numeral: https://www.numeral.com/
- Sphere: https://sphere.co/
- TaxJar: https://www.taxjar.com/
- South Dakota v. Wayfair (2018): https://www.supremecourt.gov/opinions/17pdf/17-494_j4el.pdf
- Sales Tax Institute SaaS map: https://www.salestaxinstitute.com/resources/sales-taxability-saas
- Sales Tax Institute economic nexus: https://www.salestaxinstitute.com/resources/economic-nexus-state-guide
- EU OSS: https://taxation-customs.ec.europa.eu/business/vat/oss_en
- Streamlined Sales Tax Agreement: https://www.streamlinedsalestax.org/

## Related skills

- `sales-tax-nexus-study-economic-physical` — detailed nexus analysis
- `state-apportionment-nexus-analysis` — income tax nexus
- `form-1120-corp-income-tax-filing` — federal corp tax
- `irs-state-dor-notice-response` — state DOR notice response
