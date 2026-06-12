<!--
Source: https://apidocs.chargebee.com/docs/api
Source: https://www.maxio.com/asc-606
Source: https://developer.paddle.com/
Source: https://docs.lemonsqueezy.com/
Source: https://recurly.com/developers/
Source: https://www.solvimon.com/blog/best-subscription-billing-in-2026-decision-guide
-->

# Chargebee / Maxio / Paddle / Recurly / Lemon Squeezy — Stripe alternatives

When Stripe Billing isn't the right fit. Maxio for finance-led B2B with audit-grade ASC 606; Chargebee for mid-market subscription with complex pricing; Paddle / Lemon Squeezy as Merchant of Record (MoR) that handles global tax; Recurly for involuntary-churn focus.

## When to use

- Audit-grade ASC 606 needed AND Stripe Rev Rec isn't deep enough → Maxio.
- Complex pricing (tiered, volume, multi-currency, mid-market enterprise contracts) → Chargebee.
- Solo / micro-SaaS that wants to outsource global sales tax + VAT entirely → Paddle or Lemon Squeezy.
- High involuntary churn (failed cards, dunning recovery) → Recurly.
- Migrating off Stripe or building secondary billing rail.
- Trigger phrases: "Stripe isn't enough for ASC 606", "we sell globally", "MoR", "complex SaaS pricing", "billing for indie hacker".

NOT for: companies already on Stripe with simple pricing (`stripe-revenue-recognition-asc606` is enough). NOT for usage metering only (use Orb / Metronome).

## Setup

### Chargebee

```bash
# Auth: site-scoped API key
export CHARGEBEE_API_KEY="live_..."
export CHARGEBEE_SITE="yourcompany"   # subdomain: yourcompany.chargebee.com

# Test call
curl -u "$CHARGEBEE_API_KEY:" \
  "https://$CHARGEBEE_SITE.chargebee.com/api/v2/subscriptions?limit=5"
```

### Maxio (formerly SaaSOptics + Chargify)

```bash
# Maxio has Advanced Billing (Chargify) and Finance (SaaSOptics) modules
export MAXIO_API_KEY="..."
export MAXIO_SUBDOMAIN="yourcompany"

# Test
curl -u "$MAXIO_API_KEY:x" \
  "https://$MAXIO_SUBDOMAIN.chargify.com/subscriptions.json"
```

### Paddle

```bash
export PADDLE_API_KEY="pdl_live_apikey_..."
export PADDLE_ENVIRONMENT="production"   # or "sandbox"

curl -H "Authorization: Bearer $PADDLE_API_KEY" \
  "https://api.paddle.com/products?per_page=10"
```

Pricing: 5% + $0.50 per transaction (handles global VAT/GST/sales tax + chargebacks).

### Lemon Squeezy

```bash
export LEMONSQUEEZY_API_KEY="..."

curl -H "Authorization: Bearer $LEMONSQUEEZY_API_KEY" \
  -H "Accept: application/vnd.api+json" \
  "https://api.lemonsqueezy.com/v1/products"
```

Pricing: 5% + $0.50 per transaction (similar MoR model, smaller scale).

### Recurly

```bash
export RECURLY_API_KEY="..."

curl -H "Authorization: Basic $(echo -n $RECURLY_API_KEY: | base64)" \
  -H "Accept: application/vnd.recurly.v2021-02-25" \
  "https://v3.recurly.com/sites/subdomain-yourcompany/subscriptions"
```

## Platform selection matrix

| Need | Recommended | Why |
|---|---|---|
| Indie SaaS, global, want to outsource tax | Paddle / Lemon Squeezy | MoR; 5%+$0.50 buys tax+VAT+chargebacks |
| US-only SaaS, low complexity | Stripe (default) | Cheapest, MCP in catalog |
| Mid-market B2B, complex pricing | Chargebee | Multi-currency, hierarchical pricing |
| Finance-led B2B, audit-grade ASC 606 | Maxio | Audit-grade deferred-revenue waterfalls |
| High involuntary churn | Recurly | Best-in-class dunning + retry logic |
| Usage-based only | Orb / Metronome | (out of scope here) |

## Common recipes

### Recipe 1 — Pull MRR / ARR from Chargebee

```bash
curl -u "$CHARGEBEE_API_KEY:" \
  "https://$CHARGEBEE_SITE.chargebee.com/api/v2/subscriptions?limit=100&status[is]=active"

# Aggregate: sum(plan_amount_in_cents) / 100 → MRR
# ARR = MRR × 12
```

### Recipe 2 — Pull ASC 606 deferred revenue waterfall from Maxio

```bash
# Maxio Finance — revenue schedule export
curl -u "$MAXIO_API_KEY:x" \
  "https://$MAXIO_SUBDOMAIN.saasoptics.com/api/v1/exports/revenue_schedule?\
period_start=2026-06-01&period_end=2026-06-30&format=csv"
```

Output: per-invoice × per-month recognition matrix — audit-grade.

### Recipe 3 — Create a Chargebee subscription

```bash
curl -u "$CHARGEBEE_API_KEY:" \
  -X POST "https://$CHARGEBEE_SITE.chargebee.com/api/v2/customers/$CUST_ID/subscription_for_items" \
  -d "subscription_items[item_price_id][0]=pro-plan-USD-monthly" \
  -d "subscription_items[quantity][0]=1" \
  -d "auto_collection=on"
```

### Recipe 4 — Paddle: create checkout for global B2C

```bash
# Paddle handles tax calculation at checkout — no per-jurisdiction nexus work
curl -X POST "https://api.paddle.com/transactions" \
  -H "Authorization: Bearer $PADDLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [{ "price_id": "pri_01jx...", "quantity": 1 }],
    "collection_mode": "automatic",
    "currency_code": "USD"
  }'
```

### Recipe 5 — Recurly dunning configuration

```bash
# Configure smart retry intervals — Recurly's stronger area vs Stripe
curl -X PUT "https://v3.recurly.com/sites/subdomain-yourcompany/dunning_campaigns/$ID" \
  -H "Authorization: Basic $(echo -n $RECURLY_API_KEY: | base64)" \
  -H "Accept: application/vnd.recurly.v2021-02-25" \
  -H "Content-Type: application/json" \
  -d '{ "cycles": [{ "interval_unit":"days","interval":3 },
                   { "interval_unit":"days","interval":5 },
                   { "interval_unit":"days","interval":7 }] }'
```

### Recipe 6 — Lemon Squeezy: fetch sales for tax filing

```bash
curl -H "Authorization: Bearer $LEMONSQUEEZY_API_KEY" \
  -H "Accept: application/vnd.api+json" \
  "https://api.lemonsqueezy.com/v1/orders?filter[created_at_gte]=2026-06-01&filter[created_at_lte]=2026-06-30"
# Lemon Squeezy / Paddle handle remittance — you get net payout + tax-already-handled record
```

### Recipe 7 — Migrate customers Stripe → Chargebee

```bash
# Pull from Stripe
stripe customers list --limit 100 > stripe_customers.json
# Push to Chargebee (script loop)
jq -c '.data[]' stripe_customers.json | while read c; do
  email=$(echo "$c" | jq -r .email)
  name=$(echo "$c" | jq -r .name)
  curl -u "$CHARGEBEE_API_KEY:" \
    -X POST "https://$CHARGEBEE_SITE.chargebee.com/api/v2/customers" \
    -d "email=$email" -d "first_name=$name"
done
```

### Recipe 8 — Maxio: pull NRR / GRR / churn metrics

```bash
curl -u "$MAXIO_API_KEY:x" \
  "https://$MAXIO_SUBDOMAIN.saasoptics.com/api/v1/metrics/retention?\
cohort_start=2025-06-01&cohort_end=2026-06-01"

# Returns: starting MRR, expansion, contraction, churn, ending MRR per cohort
```

### Recipe 9 — Paddle: reconcile MoR payouts

```bash
# Paddle pays out net of tax + fees → reconcile to Xero/QBO
curl -H "Authorization: Bearer $PADDLE_API_KEY" \
  "https://api.paddle.com/payouts?per_page=50"

# Each payout has gross_amount, fee_amount, tax_amount, net_payout_amount
# Book:
#   Dr Cash (net)
#   Dr Payment Processing Fees (fee_amount)
#   Dr Sales Tax Remitted (tax_amount)
#   Cr Revenue (gross_amount - tax_amount)
```

### Recipe 10 — Chargebee usage-based subscription

```bash
# Push usage records mid-cycle
curl -u "$CHARGEBEE_API_KEY:" \
  -X POST "https://$CHARGEBEE_SITE.chargebee.com/api/v2/usages" \
  -d "subscription_id=$SUB_ID" \
  -d "usage_quantity=1500" \
  -d "usage_date=$(date +%s)" \
  -d "item_price_id=usage-api-call-tier1"
```

## Examples

### Example 1: Indie SaaS launching globally — choose Paddle

**Goal:** Solo founder selling $19/mo product to customers in 40 countries; doesn't want to deal with VAT in 27 EU states.

**Steps:**

1. Sign up at paddle.com → set up products.
2. Pricing: $19/mo with `currency_code=USD`; Paddle auto-converts at checkout per country.
3. Embed Paddle checkout via JS SDK.
4. Paddle collects tax at checkout, remits to each jurisdiction.
5. Monthly: pull payouts (Recipe 9), reconcile to Xero/QBO. Gross revenue + Paddle fee + tax remitted = three book entries.
6. No nexus registration work; Paddle is the MoR.

**Result:** $0 tax compliance work, 5% + $0.50 transaction fee, global ready in 1 day.

### Example 2: Series B B2B SaaS upgrading from Stripe → Maxio for audit

**Goal:** $30M ARR company prepping for first Big 4 audit; ASC 606 deferred revenue needs to be defensible.

**Steps:**

1. Sign up at maxio.com → Maxio Finance module.
2. Connect Stripe (Maxio reads invoice + subscription data from Stripe API).
3. Configure recognition rules per product:
   - SaaS subscription: ratable over term.
   - Implementation: point-in-time at milestone.
   - Multi-year discount: ratable over full term, including discount.
4. Backfill 24 months of historical data → Maxio generates retroactive schedules.
5. Reconcile each historical month to GL — book any restatements.
6. Generate audit-ready PDFs: monthly recognized + monthly deferred + waterfall by invoice.
7. Auditors review Maxio configuration + sample contracts → sign off.

**Result:** Clean ASC 606 audit; ~2 weeks setup; ~$2-5K/mo Maxio cost (vs $50K+ manual audit prep).

## Edge cases / gotchas

- **MoR exclusivity:** Paddle / Lemon Squeezy are the merchant of record — they show up on customer card statements. If you want your brand on statements, MoR isn't right.
- **Chargebee site limits:** test site = different from production; data is segregated. Migrate via Chargebee's data import service for >10K customers.
- **Maxio dual-module pricing:** Advanced Billing (Chargify) + Finance (SaaSOptics) are priced separately. Most controllers want just Finance + connect to Stripe; confirm before signing.
- **Paddle currency conversion:** Paddle settles to you in your default currency; FX spread ~2-3% on top of fee. Set settlement currency carefully.
- **Recurly volume minimum:** Recurly historically required minimum spend (~$200/mo); confirm current.
- **Webhook reliability:** all four send webhooks for subscription events; if you build automation on these, handle dedup + retries. Stripe is the most reliable; Recurly and Chargebee have occasional delays.
- **Tax reciprocity:** if you switch from MoR (Paddle) back to self-managed (Stripe + Anrok), you become responsible retroactively only if you had nexus during the MoR period — you didn't (MoR was seller of record). Going forward, you do.
- **API versioning:** Chargebee v2 stable; Maxio Chargify still on classic endpoints; Recurly bumped to v2021-02-25; Paddle moved to "Billing" API in 2023 (old "Classic" deprecated). Always specify version header.
- **Free trial accounting:** none of these auto-defer trial-period revenue (it's $0). Watch when trial converts to paid — the contract date is conversion date, not trial-start.
- **Refunds + revenue rec:** all platforms handle refunds; in Maxio, ensure the refund hits the same revenue stream as original recognition (auditor flag if mis-routed).

## Sources

- Solvimon — best subscription billing 2026: https://www.solvimon.com/blog/best-subscription-billing-in-2026-decision-guide
- Chargebee API: https://apidocs.chargebee.com/docs/api
- Maxio: https://www.maxio.com/ · https://www.maxio.com/asc-606
- Paddle docs: https://developer.paddle.com/
- Lemon Squeezy docs: https://docs.lemonsqueezy.com/
- Recurly developers: https://recurly.com/developers/
- Paddle vs Stripe comparison: https://www.paddle.com/compare/stripe

## Related skills

- `stripe-revenue-recognition-asc606` — sister skill for Stripe-first approach
- `monthly-close-procedure` — uses Recipe 8 / Recipe 9 outputs in close
- `anrok-stripe-tax-sales-tax-compliance` — when staying self-managed instead of MoR
- `audit-prep-big4-checklist` — Maxio Finance is the audit-grade backbone
