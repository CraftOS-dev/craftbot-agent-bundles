<!--
Source: https://www.numeral.com/blog/avalara-vs-anrok
Source: https://docs.stripe.com/tax
Source: https://taxcloud.com/blog/anrok-vs-stripe-tax-comparison/
Source: https://anrok.com/
Reference role.md: "Sales tax / VAT playbook"
-->

# Anrok + Stripe Tax — multi-state sales tax / VAT compliance

Nexus mapping, product taxability per state, registration, calculation at checkout, filing, and remittance. Anrok ($100/mo Starter, SaaS-specific, 200+ jurisdictions); Stripe Tax (embedded with Stripe); Avalara (enterprise); TaxJar ($90/mo Tax Complete).

## When to use

- New state revenue triggers economic nexus (typically $100K rev OR 200 txns).
- Adding employees / offices in new states (physical nexus).
- Setting up taxability for a new product / SKU.
- Pre-fundraise diligence: have we registered everywhere we have nexus.
- Post-Wayfair compliance audit.
- Trigger phrases: "sales tax", "nexus", "Anrok", "Stripe Tax", "Avalara", "register", "VAT", "remit".

NOT for: income tax / corporate tax (use CPA); 409A valuation (use `carta-pulley-cap-table`); EU VAT-only without US footprint (use Quaderno / Paddle MoR — see `chargebee-maxio-paddle-billing`).

## Nexus types

- **Physical nexus** — office, employee, warehouse, inventory in state. Triggered on day one.
- **Economic nexus** (post South Dakota v. Wayfair 2018) — usually $100K revenue OR 200 transactions in 12-month period. Varies:
  - **California: $500K** (no transaction count)
  - **Texas: $500K** revenue
  - **NY: $500K + 100 txns** (both required)
  - **Most others: $100K OR 200 txns** (one or other)
- **Click-through / affiliate nexus** — rare for SaaS; relevant if you have affiliates.

## SaaS taxability map (2026)

Whether SaaS is taxable varies wildly:

- **Taxes SaaS as standard rule:** NY, PA, TX, WA, SC, TN, UT, OH, IA, AZ, CT (B2C only), DC, KY, MS, NM, RI, SD, WV
- **Does NOT tax SaaS:** CA, FL, NV, MO, IL (most), MD (most), NJ, OR, NH, MT, AK
- **Tax with caveats:** MA (specific software types), CO (varies), TN (yes since 2015), VA (specific cases)

Source of truth: https://www.salestaxinstitute.com/resources/sales-taxability-saas

## Platform selection matrix

| Need | Recommended | Cost |
|---|---|---|
| 100% Stripe + < 5 states | Stripe Tax | $0.50 / txn after 50 free |
| SaaS-specific, multi-state, < $50M | Anrok | $100-$1000/mo by volume |
| Enterprise ERP (NetSuite, Sage Intacct) | Avalara | Custom pricing, ~$1K/mo+ |
| E-com physical goods | TaxJar or Avalara | TaxJar $90/mo, Avalara custom |
| Want full outsource (MoR) | Paddle / Lemon Squeezy | 5% + $0.50/txn |
| EU-focused VAT | Quaderno or Avalara | Quaderno $79+/mo |

## Setup

### Anrok

```bash
# Dashboard at app.anrok.com → API keys
export ANROK_API_KEY="..."

# Test
curl -H "Authorization: Bearer $ANROK_API_KEY" \
  https://api.anrok.com/v1/transactions
```

### Stripe Tax

```bash
# Enable at dashboard.stripe.com/tax
# No separate API key; uses standard Stripe key
# Embedded in invoice/checkout endpoints

curl -X POST https://api.stripe.com/v1/tax/calculations \
  -u $STRIPE_API_KEY: \
  -d "currency=usd" \
  -d "line_items[0][amount]=10000" \
  -d "line_items[0][reference]=L1" \
  -d "customer_details[address][line1]=1 Main St" \
  -d "customer_details[address][city]=New York" \
  -d "customer_details[address][state]=NY" \
  -d "customer_details[address][postal_code]=10001" \
  -d "customer_details[address][country]=US"
```

### Avalara AvaTax

```bash
# REST or SOAP. REST preferred.
export AVATAX_ACCOUNT="..."
export AVATAX_LICENSE_KEY="..."

curl -u "$AVATAX_ACCOUNT:$AVATAX_LICENSE_KEY" \
  https://rest.avatax.com/api/v2/accounts/$AVATAX_ACCOUNT/companies
```

### TaxJar

```bash
export TAXJAR_API_KEY="..."
curl -H "Authorization: Bearer $TAXJAR_API_KEY" \
  https://api.taxjar.com/v2/categories
```

## Common recipes

### Recipe 1 — Nexus footprint map

```python
import pandas as pd
# Pull last 12mo revenue + transactions by ship-to state
sales_by_state = pd.read_sql("""
SELECT shipping_state AS state,
       SUM(amount) / 100 AS revenue,
       COUNT(*) AS transactions
FROM stripe_invoices
WHERE paid_at >= NOW() - INTERVAL '12 months'
GROUP BY state
""", db)

# Add economic nexus thresholds
THRESHOLDS = {
  "CA": (500_000, None), "TX": (500_000, None), "NY": (500_000, 100),
  # Most: $100K OR 200 txns
}
def nexus_triggered(row):
    state = row.state
    rev_t, txn_t = THRESHOLDS.get(state, (100_000, 200))
    if state in ("NY",) and rev_t and txn_t:
        return row.revenue >= rev_t and row.transactions >= txn_t
    if rev_t and row.revenue >= rev_t: return True
    if txn_t and row.transactions >= txn_t: return True
    return False

sales_by_state["nexus"] = sales_by_state.apply(nexus_triggered, axis=1)
print(sales_by_state[sales_by_state.nexus])
```

### Recipe 2 — Anrok obligation monitoring

```bash
# Anrok auto-monitors nexus + alerts on threshold approach
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
      "address": {"line1":"123 Main","city":"Austin","state":"TX","zip":"78701","country":"US"},
      "exemption": null
    },
    "line_items": [{
      "id": "l1",
      "product_id": "saas_pro_monthly",
      "amount": 9900,    // cents
      "quantity": 1
    }]
  }'
```

### Recipe 4 — Calculate tax (Stripe Tax)

```bash
# Tax-included calculation
curl -X POST https://api.stripe.com/v1/tax/calculations \
  -u $STRIPE_API_KEY: \
  -d "currency=usd" \
  -d "line_items[0][amount]=9900" \
  -d "line_items[0][tax_code]=txcd_10000000" \
  -d "customer_details[address][country]=US" \
  -d "customer_details[address][state]=TX" \
  -d "customer_details[address][postal_code]=78701"
```

Stripe tax codes: https://docs.stripe.com/tax/tax-codes (SaaS subscription = `txcd_10000000`).

### Recipe 5 — Register for sales tax in a new state

State registration is manual (no API). Anrok provides a "Register me" service per state ($499 one-time per state typical).

Direct registration:
- Most states: ~$0-$50 fee, 1-4 week processing.
- Online at state DOR (Department of Revenue) website.
- Required info: business EIN, formation docs, owner SSN, projected revenue.

### Recipe 6 — Auto-file + remit (Anrok)

```bash
# Anrok runs scheduled filings per jurisdiction cadence
curl -H "Authorization: Bearer $ANROK_API_KEY" \
  https://api.anrok.com/v1/filings?status=upcoming

# Returns: {jurisdiction, period, due_date, projected_amount}
```

Anrok auto-files in all 200+ jurisdictions on the right cadence; recipient just funds the remittance.

### Recipe 7 — Reconcile sales tax payable to GL

```python
# Month-end:
# Anrok says sales tax collected June = $7,432
# Xero sales tax payable account should match within $5
anrok_collected = requests.get(
  "https://api.anrok.com/v1/transactions/summary?from=2026-06-01&to=2026-06-30",
  headers={"Authorization": f"Bearer {ANROK_API_KEY}"}
).json()["total_tax_collected"]

xero_payable = xero.reports.balance_sheet(date="2026-06-30").get_account("2200").balance
print(f"Anrok: ${anrok_collected} | Xero: ${xero_payable} | Diff: ${anrok_collected - xero_payable}")
```

### Recipe 8 — Product taxability per state

```python
# For each product/SKU × each nexus state, determine taxability
TAXABILITY_MATRIX = {
  ("saas_pro", "NY"): "taxable",
  ("saas_pro", "TX"): "taxable",
  ("saas_pro", "CA"): "not_taxable",     # CA does not tax SaaS
  ("saas_pro", "WA"): "taxable",
  ("professional_services", "NY"): "not_taxable",
  # ...
}
```

Anrok / Avalara maintain this matrix automatically; bake it in if rolling DIY.

### Recipe 9 — Exemption certificate management

```bash
# Some customers (resellers, non-profits) are exempt. Track + verify certificates.
curl -X POST https://api.anrok.com/v1/customers/$CUST_ID/exemptions \
  -H "Authorization: Bearer $ANROK_API_KEY" \
  -d '{
    "jurisdiction":"NY",
    "exemption_type":"reseller",
    "certificate_url":"https://docs.example.com/cert.pdf",
    "valid_through":"2027-06-30"
  }'
```

### Recipe 10 — Multi-jurisdiction filing calendar

```python
# Filing cadence varies by state + volume
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

# Generate forward-looking filing calendar
import calendar
from datetime import date
for state in nexus_states:
    cadence = CADENCE.get((state, volume_tier(state)), "monthly")
    if cadence == "monthly":
        due_dates = [date(2026, m, 20) for m in range(7, 13)]
    elif cadence == "quarterly":
        due_dates = [date(2026, 7, 31), date(2026, 10, 31), date(2027, 1, 31)]
    # ...
```

## Examples

### Example 1: Series A SaaS triggering nexus in 12 new states

**Goal:** $4.2M ARR, ship-to addresses span 18 states. Identify + register where needed.

**Steps:**

1. Pull sales-by-state (Recipe 1).
2. Identify 12 states crossing economic nexus thresholds.
3. Prioritize: states where SaaS is taxable (8 of 12); other 4 are CA, FL, NV, IL (no SaaS tax, no register required).
4. Engage Anrok ($499 × 8 = $4,000) for managed registration.
5. Configure Anrok for tax calculation at checkout going forward.
6. Determine voluntary disclosure agreements (VDAs) for back-period exposure:
   - For each state, estimate uncollected back-tax owed.
   - VDA = state agrees to limit lookback (typically 3-4 years) + waive penalties.
   - Anrok / Avalara handle VDA negotiation per state ($1-3K each typical).
7. Reconcile and book sales tax payable in Xero (Recipe 7) monthly.

**Result:** Registered in all required states; back-period exposure mitigated via VDAs; future tax calculated + filed automatically.

### Example 2: First time using Stripe Tax (simple US-only)

**Goal:** Solo SaaS founder, $200K ARR US-only, wants minimum-touch.

**Steps:**

1. Enable Stripe Tax in dashboard.
2. Confirm tax codes per product (Recipe 4 endpoint).
3. Add ship-to address collection in checkout.
4. Stripe Tax: calculates per transaction, files in NY / TX / WA / PA only (where nexus triggered).
5. Stripe Tax fee: $0.50/txn after first 50/month free.
6. Monthly reconcile to Xero (Recipe 7 with Stripe Tax endpoint).

**Result:** End-to-end automated; ~$30/mo fee at this volume.

## Edge cases / gotchas

- **Wayfair thresholds change:** states adjust thresholds. Anrok / Avalara track; if DIY, audit annually.
- **Back-period exposure (VDA):** if you've had nexus but not registered, you owe back tax + penalties. Voluntary disclosure agreements (VDAs) negotiate this down. Anrok does VDA for ~$1-3K/state.
- **Marketplace facilitator laws:** if you sell through Amazon / Etsy / etc., they may remit on your behalf. Don't double-remit. Apps Stripe / Anrok handle this.
- **Origin-based vs destination-based:** most states are destination-based (ship-to). Origin states: TX, OH, MO, PA, NM, etc. Affects rate calculation.
- **Address validation:** wrong zip = wrong rate. Use validated addresses; reject if zip+state mismatch.
- **Bundled products:** if SaaS bundled with non-SaaS (e.g., professional services), allocation matters in mixed-taxability states.
- **EU VAT:** if selling to EU consumers, VAT applies regardless of physical presence. Threshold = €10K/yr (post 2021 reform). Use OSS (One Stop Shop) for EU-wide registration or stay under threshold.
- **Marketplace + MoR distinction:** Paddle / Lemon Squeezy are MoR — they're the seller of record. You're not liable for tax on those sales.
- **Filing zero-returns:** in some states, once registered, you MUST file even at $0 revenue. Missing zero-returns = penalty.
- **Tax-included vs tax-exclusive pricing:** B2B almost always exclusive (line item plus tax). B2C may be inclusive in EU/UK. Configure correctly.
- **Free trial periods:** typically not taxable until first paid invoice. Confirm per state.
- **Refund tax handling:** when refunding, tax is also refunded; state may need refund filing. Anrok handles.
- **Pricing display compliance:** some EU jurisdictions require tax-inclusive display; some US states don't allow surcharges.

## Sources

- Anrok vs Stripe Tax: https://taxcloud.com/blog/anrok-vs-stripe-tax-comparison/
- Avalara vs Anrok (Numeral): https://www.numeral.com/blog/avalara-vs-anrok
- Stripe Tax docs: https://docs.stripe.com/tax
- Stripe tax codes: https://docs.stripe.com/tax/tax-codes
- Anrok: https://anrok.com/
- South Dakota v. Wayfair (2018): https://www.supremecourt.gov/opinions/17pdf/17-494_j4el.pdf
- Sales tax SaaS map: https://www.salestaxinstitute.com/resources/sales-taxability-saas
- EU OSS (One Stop Shop): https://taxation-ec.europa.eu/business/vat/oss_en

## Related skills

- `stripe-revenue-recognition-asc606` — invoice flow integrates with tax
- `xero-quickbooks-bookkeeping` — sales tax payable account in CoA
- `monthly-close-procedure` — Recipe 7 in close
- `chargebee-maxio-paddle-billing` — Paddle / Lemon Squeezy MoR alternative
