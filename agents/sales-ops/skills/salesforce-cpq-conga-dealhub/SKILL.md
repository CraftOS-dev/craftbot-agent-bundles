<!--
Source: https://developer.salesforce.com/docs/atlas.en-us.cpq_dev_api.meta/cpq_dev_api/ + https://docs.conga.com/ + https://docs.dealhub.io/
CPQ configuration — Salesforce CPQ + Conga CPQ + DealHub CPQ (June 2026 SOTA).
-->
# CPQ Configuration — Salesforce CPQ + Conga CPQ + DealHub CPQ — SKILL

Quote-to-cash configuration. **Salesforce CPQ** (Steelbrick) — native Salesforce add-on, `SBQQ__*` object family. **Conga CPQ** (Apttus heritage) — independent platform. **DealHub CPQ** — native UI with deal-desk module + CRM sync. Pricing rules (tiered, volume, geo, channel-partner), product bundles + dependency rules, approval rules, quote PDF generation, e-sign handoff.

## When to use

- **Deploy a CPQ pricing rule** — tiered, volume, multi-year, bundle discount.
- **Create a product bundle** — required/optional/recommended components.
- **Approval rule** — discount-tier routing to manager / VP / CRO.
- **Quote template** — PDF generation with branding + signature blocks.
- **Quote-to-cash chain** — quote → order → invoice → revenue rec (handoff).
- **Trigger phrases**: "CPQ pricing rule", "product bundle", "quote template", "approval rule", "ramp deal", "multi-year discount".

Do NOT use this skill for: **non-CPQ approval routing** (use `deal-desk-discount-approval`); **billing handoff** (use Stripe-mcp directly); **non-CPQ Salesforce fields** (use `salesforce-admin-custom-fields-flows`).

## Setup

```bash
# Salesforce CPQ — uses standard Salesforce auth + sf CLI
sf org login web --alias prod
# Confirm CPQ is installed
sf data query --target-org prod \
  --query "SELECT Id, Name FROM SBQQ__Quote__c LIMIT 1"

# Conga CPQ — API token (Admin → API Access)
export CONGA_API_KEY="<key>"
export CONGA_ORG_ID="<org>"

# DealHub CPQ — API key (Settings → API)
export DEALHUB_API_KEY="<key>"

# Or all via api-gateway
export MATON_API_KEY="<key>"
```

Required:
- Salesforce CPQ: managed package installed (~$75/user/mo)
- Conga CPQ: separate subscription (~$120/user/mo)
- DealHub CPQ: subscription (~$70/user/mo) + deal-desk module
- Admin role on the CPQ platform

## Common recipes

### Recipe 1: Salesforce CPQ — list pricing rules

```bash
sf data query --target-org prod --query \
  "SELECT Id, Name, SBQQ__Active__c, SBQQ__EvaluationEvent__c, SBQQ__ConditionsMet__c, SBQQ__LookupObject__c \
   FROM SBQQ__PriceRule__c WHERE SBQQ__Active__c = TRUE ORDER BY Name"
```

### Recipe 2: Tiered volume discount (Salesforce CPQ)

```bash
# Create a Discount Schedule for tiered seat pricing
sf data create record --target-org prod --sobject SBQQ__DiscountSchedule__c \
  --values "Name='Seat Volume Discount' SBQQ__Type__c='Range' SBQQ__AggregationScope__c='Quote'"

# Create tiers
# 1-50 seats: $200/seat (0% discount)
# 51-200: $175 (12.5% discount)
# 201-500: $150 (25%)
# 501+: $125 (37.5%)
sf data create record --target-org prod --sobject SBQQ__DiscountTier__c \
  --values "SBQQ__Schedule__c=<schedule_id> SBQQ__LowerBound__c=1 SBQQ__UpperBound__c=50 SBQQ__Discount__c=0"
sf data create record --target-org prod --sobject SBQQ__DiscountTier__c \
  --values "SBQQ__Schedule__c=<schedule_id> SBQQ__LowerBound__c=51 SBQQ__UpperBound__c=200 SBQQ__Discount__c=12.5"
sf data create record --target-org prod --sobject SBQQ__DiscountTier__c \
  --values "SBQQ__Schedule__c=<schedule_id> SBQQ__LowerBound__c=201 SBQQ__UpperBound__c=500 SBQQ__Discount__c=25"
sf data create record --target-org prod --sobject SBQQ__DiscountTier__c \
  --values "SBQQ__Schedule__c=<schedule_id> SBQQ__LowerBound__c=501 SBQQ__Discount__c=37.5"

# Attach schedule to product
sf data update record --target-org prod --sobject Product2 --record-id <product_id> \
  --values "SBQQ__DiscountSchedule__c=<schedule_id>"
```

### Recipe 3: Multi-year ramp deal (price action rule)

```bash
# Year 1: 100% list, Year 2: 95%, Year 3: 90%
# Salesforce CPQ via Price Action on SBQQ__PriceAction__c

sf data create record --target-org prod --sobject SBQQ__PriceRule__c \
  --values "Name='Multi-Year Ramp Discount' SBQQ__Active__c=true SBQQ__EvaluationEvent__c='On Calculate'"

# Add Price Conditions: subscription term >= 24
sf data create record --target-org prod --sobject SBQQ__PriceCondition__c \
  --values "SBQQ__Rule__c=<rule_id> SBQQ__Field__c='SBQQ__SubscriptionTerm__c' SBQQ__Operator__c='>=' SBQQ__Value__c='24'"

# Add Price Action: apply 5% discount Year 2, 10% Year 3
sf data create record --target-org prod --sobject SBQQ__PriceAction__c \
  --values "SBQQ__Rule__c=<rule_id> SBQQ__Field__c='SBQQ__AdditionalDiscount__c' SBQQ__Formula__c='IF(SBQQ__ProrateMultiplier__c < 1, 5, 10)'"
```

### Recipe 4: Bundle dependency rule (required + recommended)

```bash
# Product A (Platform) → REQUIRE Product B (Support); RECOMMEND Product E (Onboarding)
# Salesforce CPQ uses SBQQ__ProductFeature__c + SBQQ__ProductOption__c

# Create feature for Platform bundle
sf data create record --target-org prod --sobject SBQQ__ProductFeature__c \
  --values "Name='Platform Bundle' SBQQ__ConfiguredSKU__c=<platform_id> SBQQ__Number__c=1 SBQQ__OptionSelectionMethod__c='Click'"

# Add required option
sf data create record --target-org prod --sobject SBQQ__ProductOption__c \
  --values "SBQQ__Feature__c=<feature_id> SBQQ__OptionalSKU__c=<support_id> SBQQ__Required__c=true SBQQ__Bundled__c=true"

# Add recommended option
sf data create record --target-org prod --sobject SBQQ__ProductOption__c \
  --values "SBQQ__Feature__c=<feature_id> SBQQ__OptionalSKU__c=<onboarding_id> SBQQ__Required__c=false SBQQ__Bundled__c=false"
```

### Recipe 5: Discount approval rule

```bash
# Trigger Salesforce Approval Process when discount > 20%
# Defined as SBQQ__ApprovalRule__c

sf data create record --target-org prod --sobject SBQQ__ApprovalRule__c \
  --values "Name='Discount > 20% — VP Approval' SBQQ__Active__c=true \
            SBQQ__ApprovalCondition__c='Editing' SBQQ__ApprovalType__c='Manager Approval'"

# Add condition: AverageCustomerDiscount > 20
sf data create record --target-org prod --sobject SBQQ__ApprovalCondition__c \
  --values "SBQQ__Rule__c=<rule_id> SBQQ__Field__c='SBQQ__AverageCustomerDiscount__c' \
            SBQQ__Operator__c='>' SBQQ__Value__c='20'"
```

### Recipe 6: Conga CPQ — create quote

```bash
curl -X POST "https://api.conga.com/v1/quotes" \
  -H "Authorization: Bearer $CONGA_API_KEY" \
  -H "X-Org-Id: $CONGA_ORG_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "opportunity_id": "006XX0000123ABC",
    "currency": "USD",
    "term_months": 12,
    "billing_frequency": "Annual",
    "line_items": [
      {"product_id": "prod_plat_01", "quantity": 100, "list_price": 200, "discount_pct": 12.5},
      {"product_id": "prod_supp_01", "quantity": 1, "list_price": 5000, "discount_pct": 0}
    ]
  }'
```

### Recipe 7: DealHub CPQ — create quote

```bash
curl -X POST "https://api.dealhub.io/v1/quotes" \
  -H "Authorization: Bearer $DEALHUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "deal_room_id": "dr_xyz789",
    "name": "Q3 2026 — Acme Corp",
    "products": [
      {"sku": "PLAT-ENT", "quantity": 250, "list_price": 200, "discount_pct": 25, "term_months": 36},
      {"sku": "SUPP-PREM", "quantity": 1, "list_price": 10000}
    ],
    "currency": "USD",
    "validity_days": 30
  }'
```

### Recipe 8: Salesforce CPQ — quote PDF generation

```bash
# CPQ has a built-in PDF generator (Quote Template + Quote Document)
sf data create record --target-org prod --sobject SBQQ__QuoteDocument__c \
  --values "SBQQ__Quote__c=<quote_id> SBQQ__DocumentName__c='Acme Corp Quote Q3 2026.pdf'"

# Trigger generation via REST custom endpoint
curl -X POST "https://gateway.maton.ai/salesforce/services/apexrest/sbqq/generateQuoteDocument" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -d '{"quoteId": "a0XXX0000123", "templateId": "a1XXX0000456"}'
```

### Recipe 9: CPQ + Stripe billing handoff (quote-to-cash)

```python
# On quote acceptance: create Stripe subscription
import requests, os, stripe

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

# Pull approved quote
q = requests.get(f"https://gateway.maton.ai/salesforce/services/data/v60.0/sobjects/SBQQ__Quote__c/<quote_id>",
                 headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"}).json()

# Create Stripe customer if not exists
customer = stripe.Customer.create(
    email=q["SBQQ__PrimaryContact__r"]["Email"],
    name=q["SBQQ__Account__r"]["Name"]
)

# Create subscription with line items
subscription = stripe.Subscription.create(
    customer=customer.id,
    items=[{"price": stripe_price_id, "quantity": q_line["SBQQ__Quantity__c"]} for q_line in q["lines"]],
    metadata={"sf_opportunity_id": q["SBQQ__Opportunity__c"]}
)

# Write subscription ID back to Opportunity
requests.patch(f"https://gateway.maton.ai/salesforce/services/data/v60.0/sobjects/Opportunity/{q['SBQQ__Opportunity__c']}",
               headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
                        "Content-Type": "application/json"},
               json={"Stripe_Subscription_Id__c": subscription.id})
```

### Recipe 10: Channel partner discount override

```bash
# Auto-apply 15% partner discount on all products if Partner_Tier__c = 'Gold'
sf data create record --target-org prod --sobject SBQQ__PriceRule__c \
  --values "Name='Gold Partner Auto Discount' SBQQ__Active__c=true SBQQ__EvaluationEvent__c='On Calculate' \
            SBQQ__ConditionsMet__c='All'"

sf data create record --target-org prod --sobject SBQQ__PriceCondition__c \
  --values "SBQQ__Rule__c=<rule_id> SBQQ__Object__c='Quote' SBQQ__Field__c='SBQQ__Account__r.Partner_Tier__c' \
            SBQQ__Operator__c='equals' SBQQ__Value__c='Gold'"

sf data create record --target-org prod --sobject SBQQ__PriceAction__c \
  --values "SBQQ__Rule__c=<rule_id> SBQQ__Object__c='Quote Line' \
            SBQQ__Field__c='SBQQ__PartnerDiscount__c' SBQQ__Value__c='15'"
```

### Recipe 11: Test quote (edge cases)

```python
# Build 5 test quotes to validate new pricing rule
test_cases = [
    {"name": "Min seats", "seats": 10, "term": 12, "expected_per_seat": 200},
    {"name": "Tier boundary", "seats": 50, "term": 12, "expected_per_seat": 200},
    {"name": "Tier 2", "seats": 51, "term": 12, "expected_per_seat": 175},
    {"name": "Ramp deal", "seats": 100, "term": 36, "expected_y1": 200, "expected_y3": 180},
    {"name": "Bundle discount", "products": ["platform","analytics","ai"], "expected_total": 35000}
]

for tc in test_cases:
    quote_id = create_test_quote(tc)
    result = fetch_calculated_quote(quote_id)
    if abs(result['per_seat'] - tc['expected_per_seat']) > 0.01:
        print(f"FAIL: {tc['name']} — got ${result['per_seat']}, expected ${tc['expected_per_seat']}")
    else:
        print(f"PASS: {tc['name']}")
```

### Recipe 12: Sandbox-to-prod CPQ deployment

```bash
# CPQ config lives in records, not metadata. Use Composite API for batch.
sf data query --target-org sandbox \
  --query "SELECT Id, Name FROM SBQQ__PriceRule__c WHERE Last_Modified > LAST_N_DAYS:30" \
  --result-format csv > new_rules.csv

# Bulk upsert to prod (via Composite API or sf data import)
sf data upsert bulk --target-org prod --sobject SBQQ__PriceRule__c \
  --external-id Name --file new_rules.csv --wait 30
```

## Examples

### Example 1: Tiered volume discount rollout

**Goal:** Reduce manual approval friction — auto-apply volume discount on seats.

**Steps:**
1. Recipe 2 — create Discount Schedule with 4 tiers in sandbox.
2. Attach to Platform Seat product.
3. Recipe 11 — build 5 test quotes covering tier boundaries.
4. Validate calculated prices match expected per-seat.
5. Recipe 12 — promote schedule + tier records to production via Composite API.
6. Notify AEs in Slack: "Volume discount now auto-applies on seats > 50."

**Result:** ~30% of quotes auto-discounted; manager approvals reduced.

### Example 2: 3-year ramp deal configuration

**Goal:** Sales wants to offer 3-year deals with declining per-year price.

**Steps:**
1. Recipe 3 — create Price Rule with subscription_term >= 24 condition.
2. Add Price Action that adjusts per-year discount via formula.
3. Test with: 12-mo (no discount), 24-mo (5% Y2), 36-mo (5% Y2 + 10% Y3).
4. Add validation rule: term >= 24 requires CFO approval.
5. Deploy to prod.

**Result:** Multi-year deals close 2× faster; CFO gates against runaway commitments.

### Example 3: CPQ → Stripe quote-to-cash

**Goal:** Approved quote auto-creates Stripe subscription; no manual data entry.

**Steps:**
1. Build Approval Process: quote status → Approved.
2. Approval triggers Flow → invokes Recipe 9 (via Apex callout or Operations Hub workflow).
3. Stripe subscription created; subscription ID written back to Opportunity.
4. Stripe webhook on payment → updates Opportunity to "Closed Won".
5. Handoff to `finance-controller` for revenue rec.

**Result:** Quote → revenue with zero manual handoff; CFO sees consistent SF + Stripe data.

## Edge cases / gotchas

- **CPQ price calculation is event-driven** — `On Calculate`, `Before Calculate`, `After Calculate`, `On Initialization`. Wrong event = rule doesn't fire when expected.
- **Discount stacking** — Volume + multi-year + partner discounts can compound to absurd levels. Pre-test with extreme inputs.
- **CPQ Quote Lines aren't auto-created** — adding a product to a Quote requires Quote Line + correct Bundle structure.
- **Bundles vs Options** — confusing. Bundle = parent product with options. Option = child SKU under a bundle. Wrong choice breaks calculator.
- **Salesforce CPQ "Edit Lines" page is server-side rendered** — heavy queries can time out for quotes > 200 lines.
- **Approval rules vs validation rules** — approval rules block submit (require approver action); validation rules block save. Different UX.
- **Quote Templates are XML-defined** — complex to author. UI editor is limited; admin reads XML via Tooling API for tweaks.
- **Currency rounding** — different rounding modes (HALF_UP, HALF_EVEN). USD: 2 decimals. JPY: 0 decimals. Configure per currency.
- **Conga CPQ vs Conga Composer** — different products. Composer is doc generation; CPQ is quoting. Don't mix.
- **DealHub deal-room concept** — quote lives inside a "deal room"; different mental model from Salesforce/Conga.
- **Subscription term vs initial term** — ramp deals: SBQQ__SubscriptionTerm__c is total; SBQQ__InitialTerm__c is opening commit.
- **Quote → Order → Asset chain** — order generates from quote on close-won; asset tracks subscriptions. Skipped steps break renewals.
- **CPQ + LWC + Lightning Pages** — older orgs use Aura; newer use LWC. Different config patterns.
- **API governor limits** — Salesforce CPQ heavy on SOQL; batch operations hit limits. Use Bulk API.
- **CPQ price book consistency** — multiple price books for different segments/regions; wrong assignment yields wrong prices.

## Sources

- [Salesforce CPQ Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.cpq_dev_api.meta/cpq_dev_api/)
- [Salesforce CPQ Object Reference](https://help.salesforce.com/s/articleView?id=sf.cpq_objects.htm)
- [SBQQ__PriceRule__c Reference](https://help.salesforce.com/s/articleView?id=sf.cpq_price_rules_parent.htm)
- [Conga CPQ documentation](https://docs.conga.com/cpq)
- [DealHub CPQ documentation](https://docs.dealhub.io/)
- [Salesforce CPQ + Stripe Integration](https://stripe.com/docs/billing/migration/salesforce)
- [CPQ Specialist Trailhead](https://trailhead.salesforce.com/users/strailhead/trailmixes/get-started-with-salesforce-cpq)
- [Salesforce Revenue Cloud Overview](https://www.salesforce.com/products/revenue-cloud/overview/)
