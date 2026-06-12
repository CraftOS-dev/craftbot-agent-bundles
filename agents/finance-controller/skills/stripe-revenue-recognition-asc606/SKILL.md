<!--
Source: https://docs.stripe.com/revenue-recognition
Source: https://docs.stripe.com/revenue-recognition/configuration/products
Source: https://www.solvimon.com/blog/best-subscription-billing-in-2026-decision-guide
-->

# Stripe Revenue Recognition — ASC 606 deferred-revenue waterfall

Auto-generates audit-grade ASC 606 schedules from Stripe Billing data. 0.25% fee on top of standard processing. Replaces manual deferred-revenue spreadsheets when 80%+ of revenue flows through Stripe.

## When to use

- Any company on Stripe Billing that issues annual / multi-month invoices or has setup fees.
- Generate monthly recognized revenue + deferred revenue balance for the close package.
- Produce ASC 606 schedules for first-time audit (Big 4, regional, or quality of earnings).
- Identify performance obligations across complex SaaS contracts (subscription + implementation + services).
- Trigger phrases: "recognize this contract", "deferred revenue waterfall", "ASC 606 schedule", "rev rec".

NOT for: companies without Stripe (use Maxio / Chargebee — see `chargebee-maxio-paddle-billing`). NOT for usage-based-only revenue with no upfront billing (recognize as usage occurs, no deferred revenue exists).

## Setup

```bash
# Stripe Revenue Recognition product enabled at dashboard:
# https://dashboard.stripe.com/revenue-recognition
# Fee: 0.25% of revenue passed through the product (in addition to 2.9%+30¢ standard).

# API access — uses standard Stripe secret key with `rev_rec_*` permissions
export STRIPE_API_KEY="sk_live_..."   # or sk_test_... for sandbox

# CraftBot MCP path:
# stripe-mcp is in catalog; Maton gateway already ships in default `stripe-api`
# skill. No per-recipient OAuth setup beyond Stripe Dashboard activation.
```

Auth: standard Stripe restricted API key; create one limited to `rev_rec_reports:read` + `rev_rec_configurations:write` if delegating to junior staff.

## The five-step ASC 606 model (reference)

1. **Identify the contract** — written / oral / implied; must have commercial substance and identify rights + payment terms.
2. **Identify performance obligations** — distinct goods/services in the contract.
3. **Determine the transaction price** — fixed + variable consideration (estimated and constrained).
4. **Allocate the transaction price** — to performance obligations by relative standalone selling price (SSP).
5. **Recognize revenue** — when (or as) each performance obligation is satisfied.

## Common recipes

### Recipe 1 — Configure recognition rule for SaaS subscription

```bash
# Set ratable recognition over subscription term for all `prod_saas_*` products
curl https://api.stripe.com/v1/billing/rev_rec_configurations \
  -u $STRIPE_API_KEY: \
  -d "product=prod_saas_pro" \
  -d "method=ratable_over_term" \
  -d "term_source=subscription_billing_period"
```

Standard: monthly subscriptions recognize ratably each day; annual upfront recognize $1,000/mo for $12,000 paid upfront.

### Recipe 2 — Configure setup fee (distinct vs not distinct)

```bash
# Distinct setup fee — recognize at completion of setup
curl https://api.stripe.com/v1/billing/rev_rec_configurations \
  -u $STRIPE_API_KEY: \
  -d "product=prod_setup_distinct" \
  -d "method=point_in_time" \
  -d "trigger=invoice_paid"

# Not distinct (only useful with the subscription) — recognize over subscription term
curl https://api.stripe.com/v1/billing/rev_rec_configurations \
  -u $STRIPE_API_KEY: \
  -d "product=prod_setup_bundled" \
  -d "method=ratable_over_term" \
  -d "term_source=related_subscription"
```

Determination rule: distinct if customer can benefit from the good/service on its own or with other readily available resources, AND the promise is separately identifiable.

### Recipe 3 — Export monthly recognition waterfall

```bash
# Generate revenue summary report for June 2026
curl -G https://api.stripe.com/v1/billing/rev_rec/reports \
  -u $STRIPE_API_KEY: \
  -d "report_type=revenue_summary" \
  -d "interval_start=1717200000"  \
  -d "interval_end=1719792000"

# Returns: recognized_revenue, deferred_revenue_opening, deferred_revenue_closing,
# new_invoices, recognition_period_data
```

### Recipe 4 — Export deferred revenue schedule (waterfall by month)

```bash
curl -G https://api.stripe.com/v1/billing/rev_rec/reports \
  -u $STRIPE_API_KEY: \
  -d "report_type=deferred_revenue_by_period" \
  -d "as_of=2026-06-30" \
  -d "future_periods=24"
```

Output rows: each invoice × each future month → recognition $ in that month. Sum down columns = monthly recognized. Sum across rows = invoice total.

### Recipe 5 — Manual ASC 606 waterfall in xlsx (no Stripe)

```python
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

# Inputs: invoice df with columns [invoice_id, customer, amount, service_start, service_end]
invoices = pd.read_csv("invoices_2026.csv", parse_dates=["service_start", "service_end"])

def monthly_recognition(row):
    months = (row.service_end.year - row.service_start.year) * 12 + \
             (row.service_end.month - row.service_start.month) + 1
    monthly = row.amount / months
    return [(row.invoice_id,
             date(row.service_start.year, row.service_start.month, 1) + relativedelta(months=i),
             monthly) for i in range(months)]

waterfall = pd.DataFrame(
    [r for _, inv in invoices.iterrows() for r in monthly_recognition(inv)],
    columns=["invoice_id", "month", "recognized"]
)
pivot = waterfall.pivot_table(index="invoice_id", columns="month",
                              values="recognized", aggfunc="sum", fill_value=0)
pivot.to_excel("deferred_revenue_waterfall_2026-06.xlsx")
```

### Recipe 6 — Adjust transaction price for variable consideration

```bash
# E.g., volume rebate estimated at 8% — constrain to 5% (most likely amount,
# constrained for collection uncertainty)
curl https://api.stripe.com/v1/billing/rev_rec_adjustments \
  -u $STRIPE_API_KEY: \
  -d "invoice=in_xxx" \
  -d "type=variable_consideration_constraint" \
  -d "amount=-2500" \
  -d "rationale=Q3 2026 volume rebate estimate"
```

### Recipe 7 — Allocate price across multiple performance obligations

Multi-element bundle: $20K = $15K SaaS subscription + $5K implementation services.

Standalone selling prices (SSP):
- SaaS: $12K/yr standalone
- Implementation: $8K standalone

Allocation:
- SaaS allocated: $20K × ($12K / $20K) = $12K → recognize ratably
- Implementation allocated: $20K × ($8K / $20K) = $8K → recognize at completion (distinct)

```bash
curl https://api.stripe.com/v1/billing/rev_rec_allocations \
  -u $STRIPE_API_KEY: \
  -d "invoice=in_yyy" \
  -d "allocations[0][line]=il_saas" -d "allocations[0][allocated_amount]=1200000" \
  -d "allocations[1][line]=il_impl" -d "allocations[1][allocated_amount]=800000"
# Amounts in cents
```

### Recipe 8 — Pull recognized revenue for journal entries

```bash
# For close month: total recognized = revenue per BS
# Net deferred change = deferred_revenue_closing − deferred_revenue_opening

# Standard close journal:
# Dr Deferred Revenue   $X (decrease)
# Cr Revenue            $X
```

### Recipe 9 — Reconcile Stripe rev rec → Xero / QBO GL

```python
# Stripe says June recognized $87,432
# Xero GL Revenue account 4000 should match within $50 (immaterial) or be reconciled
import stripe, requests
stripe.api_key = STRIPE_KEY

rev_rec = requests.get(
  "https://api.stripe.com/v1/billing/rev_rec/reports",
  params={"report_type":"revenue_summary",
          "interval_start": 1717200000, "interval_end": 1719792000},
  auth=(STRIPE_KEY, "")
).json()
stripe_revenue = rev_rec["recognized_revenue"] / 100  # cents → dollars

# Pull GL from Xero
xero_revenue = xero.reports.profit_and_loss(
  fromDate="2026-06-01", toDate="2026-06-30"
)["Reports"][0]["Rows"][0]["Cells"][1]["Value"]

variance = stripe_revenue - float(xero_revenue)
print(f"Stripe Rev Rec: ${stripe_revenue} | Xero GL: ${xero_revenue} | Variance: ${variance}")
```

### Recipe 10 — Identify performance obligations (decision tree)

```
Is the promise a good/service that the customer can benefit from on its own
or with other readily available resources?
├── NO → bundle with another promise; combined PO
└── YES → Is the promise separately identifiable from other promises in the contract?
            ├── NO → combined PO
            └── YES → distinct → standalone PO
```

Typical SaaS contract:
- Software subscription = distinct → ratable PO
- Setup / onboarding = distinct only if customer could get setup elsewhere
- Customer success / training = usually NOT distinct (only useful with subscription)
- Professional services = distinct if separately negotiated

## Examples

### Example 1: $24K annual SaaS deal, paid upfront, 1-year term

**Goal:** Schedule recognition + journal entries for one customer.

**Steps:**

1. Customer signs contract 2026-06-15, service 2026-06-15 → 2027-06-14.
2. Stripe issues invoice $24,000, customer pays 2026-06-15.
3. At June close: 16 days of service delivered (2026-06-15 to 2026-06-30).
   - Daily rate: $24,000 / 365 = $65.75
   - June recognized: $65.75 × 16 = $1,052
4. Journal (auto-generated by Stripe Rev Rec):
   ```
   Dr Cash           $24,000   (already booked at payment)
   Cr Deferred Rev   $24,000   (initial)
   --- close ---
   Dr Deferred Rev   $1,052
   Cr Revenue        $1,052
   ```
5. Verify Stripe report matches GL revenue account movement.

**Result:** June P&L shows $1,052 recognized; June BS deferred revenue = $22,948.

### Example 2: Bundled contract with services and subscription

**Goal:** Allocate $50K contract: $40K SaaS + $10K implementation.

**Steps:**

1. Identify performance obligations: SaaS (distinct), Implementation (distinct, completes by 2026-07-31).
2. Compute SSPs: SaaS $40K standalone; Implementation $12K standalone.
3. Allocate: SaaS = $50K × ($40K/$52K) = $38,462; Implementation = $50K × ($12K/$52K) = $11,538.
4. Configure Stripe (Recipe 7).
5. Recognize SaaS ratably over 12 months: $3,205/month.
6. Recognize Implementation at completion 2026-07-31: $11,538.
7. June close (assume contract starts 2026-06-15 to 2027-06-14):
   - SaaS: 16 days × ($38,462 / 365) = $1,685
   - Implementation: still in progress, $0 recognized.

**Result:** June P&L recognizes $1,685 from this contract; July recognizes $3,205 SaaS + $11,538 implementation = $14,743.

## Edge cases / gotchas

- **0.25% fee on top of processing:** budget this. On $5M ARR through Stripe = $12,500/yr Rev Rec product fee.
- **Sandbox vs production data drift:** sandbox is wiped periodically; never store production schedules there.
- **Mid-term contract modifications:** prospective vs cumulative-catch-up depends on whether modification adds distinct goods/services. Stripe handles common cases; complex amendments may need CPA review.
- **Non-Stripe invoices:** Stripe Rev Rec only covers Stripe-billed revenue. Anything invoiced outside (wire-paid annuals, partner billing) needs manual waterfall (Recipe 5) — surface this explicitly.
- **Variable consideration constraint:** ASC 606 requires constraining variable consideration to amount "highly probable" of no significant reversal. Stripe doesn't auto-constrain — controller sets `rev_rec_adjustments` (Recipe 6).
- **Contract cost capitalization (ASC 340-40):** sales commissions for contracts >1yr should be capitalized + amortized over expected customer life. Stripe Rev Rec does NOT handle this. Capture separately.
- **Refund timing:** refunds reduce recognized revenue in the period the refund is granted, not the original period. Stripe handles this.
- **Multi-currency:** Stripe Rev Rec uses your settlement currency. Foreign-currency contracts get FX-translated at recognition date.
- **Audit-trail export:** download monthly schedules as immutable PDFs at close; auditors will request the same as-of-date snapshots.
- **First-time audit:** plan for 2-week conversion: configure all SKUs, run historical waterfall back to founding, reconcile each month to GL, document any reclasses. Maxio is sometimes recommended over Stripe Rev Rec when historical data is messy.

## Sources

- Stripe Revenue Recognition docs: https://docs.stripe.com/revenue-recognition
- Configuration / products: https://docs.stripe.com/revenue-recognition/configuration/products
- Reports API: https://docs.stripe.com/revenue-recognition/reports
- ASC 606 PwC handbook (free): https://viewpoint.pwc.com/dt/us/en/pwc/accounting_guides/revenue_from_contrac/revenue_from_contrac_US/chapter_1_executive__US.html
- Solvimon — subscription billing decision guide 2026: https://www.solvimon.com/blog/best-subscription-billing-in-2026-decision-guide
- Maxio alternative (audit-grade ASC 606): https://www.maxio.com/asc-606

## Related skills

- `chargebee-maxio-paddle-billing` — when Stripe Rev Rec doesn't fit (Maxio for audit-grade)
- `monthly-close-procedure` — uses Recipe 8 + Recipe 9 in the close pipeline
- `audit-prep-big4-checklist` — auditors request Recipe 3 + Recipe 4 outputs
- `xero-quickbooks-bookkeeping` — book the journals from Recipe 8
