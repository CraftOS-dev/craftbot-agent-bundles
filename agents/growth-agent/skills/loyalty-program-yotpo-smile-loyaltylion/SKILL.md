<!--
Source: Yotpo Loyalty + Smile.io + LoyaltyLion + Klaviyo Loyalty 2026 docs
-->
# Loyalty Program — Platform Choice + Point Structure SKILL

> Pick loyalty platform (Yotpo / Smile.io / LoyaltyLion / Klaviyo Loyalty / Stamped) and design points + tiers + VIP structure. Drives repeat purchase, NRR, and CAC payback through retention.

## When to use

Trigger phrases:
- "Build a loyalty program"
- "Points + tiers system"
- "VIP tier design"
- "Yotpo vs Smile.io"
- "Increase repeat purchase rate"
- "DTC retention play"

Pair: `referral-program-referralcandy-friendbuy-growsurf` (often unified), `expansion-revenue-nrr-optimization`, `retention-curve-churn-diagnosis-j-smile`.

## Setup

```bash
export YOTPO_API_KEY="ypo_..."
export YOTPO_API_SECRET="..."
export SMILE_API_KEY="smile_..."
export LOYALTYLION_TOKEN="ll_..."
export KLAVIYO_API_KEY="pk_..."
export STAMPED_API_KEY="stp_..."
```

## Platform decision matrix (June 2026)

| Tool | E-com fit | Multi-channel | Native integrations | Pricing | Best for |
|---|---|---|---|---|---|
| **Yotpo Loyalty** (formerly Swell) | Best-in-class | Reviews + Loyalty + SMS unified | Shopify, Klaviyo, Attentive | $19-1700/mo, custom enterprise | Full Yotpo customer stack |
| **Smile.io** | Best-in-class for Shopify ease | Standalone | Shopify, BigCommerce, Klaviyo | $49-999/mo + Plus | Shopify SMB; setup speed > custom |
| **LoyaltyLion** | Best for points/tiers/VIP | Email + SMS via integrations | Shopify, Klaviyo, Attentive | $159-799/mo | Mid-market needing tier sophistication |
| **Klaviyo Loyalty** | Native to Klaviyo | Email + SMS native | Inside Klaviyo | Bundled w/ Klaviyo | Klaviyo-native shops; loop tightly w/ flows |
| **Stamped.io** | Good mid-market | Reviews + Loyalty | Shopify, BigCommerce | $79-499/mo | Mid-market budget |
| **Marsello** | Mid-market omnichannel | POS + Online | Shopify, Lightspeed, Square | $99-399/mo | Brick-and-mortar + online |
| **Annex Cloud** | Enterprise | Full enterprise stack | Salesforce, Adobe | Enterprise | Big retailers |

## Selection logic

```text
Q1: Already on Klaviyo?
   yes  → Klaviyo Loyalty (tight loop; avoid extra vendor)
   no   → continue

Q2: Need tiered VIP + complex rules?
   yes  → LoyaltyLion / Yotpo
   no   → Smile.io / Stamped

Q3: Reviews + loyalty + SMS unified?
   yes  → Yotpo (full stack)
   no   → Smile.io / LoyaltyLion

Q4: POS + online unified?
   yes  → Marsello / Annex Cloud
   no   → others
```

## Point structure design

### Earning rules (typical)

| Action | Points | Why |
|---|---|---|
| $1 spent | 1-10 pts | Base; calibrate vs reward redemption value |
| Account creation | 100-500 pts | Onboarding incentive |
| Birthday | 100-500 pts | Reactivation trigger |
| Review left | 50-200 pts | UGC for reviews skill |
| Social share | 25-100 pts | Light viral nudge |
| Refer friend (converted) | 500-2000 pts | Bridge to referral skill |
| Newsletter signup | 100 pts | Lead capture |
| First mobile purchase | 200 pts | Channel push |

### Redemption rules

```text
100 pts  = $5 off    (1pt = $0.05; 5% cost)
500 pts  = $30 off   (1pt = $0.06; 6% cost)
1000 pts = $75 off + free shipping (escalating value)

Conversion ratio: keep redemption rate ~3-7% of revenue
   Too generous (>10%) → margin destruction
   Too stingy (<2%) → no engagement; points hoarded
```

### VIP tier design (3-tier canonical)

| Tier | Spend threshold (12mo) | Perks | % of customers (typical) | % of revenue (typical) |
|---|---|---|---|---|
| Member (free) | $0 | 1 pt/$ | 80% | 35% |
| Silver | $250-500 spent | 2 pts/$, free shipping, early access | 15% | 35% |
| Gold | $1,000+ spent | 3 pts/$, free returns, exclusive products, dedicated support | 5% | 30% |

Adjust thresholds per industry: luxury = higher; mass-market = lower.

## Common recipes

### Recipe 1: Smile.io — create program + earning rule

```bash
curl -X POST "https://api.smile.io/v1/earn_actions" \
  -H "Authorization: Bearer $SMILE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "place_order",
    "points_per_currency_amount": 1,
    "currency_amount": 1,
    "description": "Earn 1 point per $1 spent"
  }'

# Reward: $5 off for 100 points
curl -X POST "https://api.smile.io/v1/rewards" \
  -H "Authorization: Bearer $SMILE_API_KEY" \
  -d '{
    "type": "fixed_amount_discount",
    "points_cost": 100,
    "discount_value": 5,
    "discount_value_type": "fixed_amount"
  }'
```

### Recipe 2: LoyaltyLion — create tier

```bash
curl -X POST "https://api.loyaltylion.com/v2/tiers" \
  -H "Authorization: Bearer $LOYALTYLION_TOKEN" \
  -d '{
    "name": "Gold",
    "qualification": {
      "type": "annual_spend",
      "threshold_cents": 100000
    },
    "perks": ["3x_points", "free_shipping", "early_access", "free_returns"]
  }'
```

### Recipe 3: Yotpo Loyalty — create campaign

```bash
curl -X POST "https://loyalty.yotpo.com/api/v2/campaigns" \
  -H "x-guid: $YOTPO_API_KEY" \
  -H "x-api-key: $YOTPO_API_SECRET" \
  -d '{
    "name": "Earn for review",
    "type": "earn",
    "action": "leave_review",
    "points": 100,
    "max_per_customer": 5
  }'
```

### Recipe 4: Klaviyo Loyalty — native flow trigger

```javascript
// Klaviyo flow on tier-up
trigger: {
  metric: "Loyalty Tier Upgraded",
  filter: {new_tier: "Gold"}
}
actions: [
  {type: "email", template: "tier_upgrade_welcome"},
  {type: "sms", template: "Welcome to Gold! Enjoy free shipping."}
]
```

### Recipe 5: Track program ROI

```sql
-- DTC e-com loyalty ROI
SELECT
  CASE WHEN is_member THEN 'member' ELSE 'non-member' END AS segment,
  count(DISTINCT customer_id) AS customers,
  avg(annual_purchase_count) AS avg_orders,
  avg(annual_spend) AS avg_spend,
  sum(annual_spend) AS total_revenue,
  sum(redemption_cost) AS total_redemption_cost,
  (sum(annual_spend) - sum(redemption_cost)) / sum(annual_spend) AS net_margin
FROM customers
GROUP BY segment
```

Members should show 2-3x higher avg_spend than non-members, AOV +15-30%, repeat rate +50-100%.

### Recipe 6: Identify high-redeemers (anti-fraud)

```sql
SELECT
  customer_id,
  count() AS redemptions_in_30d,
  sum(reward_value) AS total_reward_value,
  sum(order_value) AS total_order_value,
  total_reward_value / total_order_value AS reward_share
FROM redemption_table
WHERE created_at > now() - INTERVAL 30 DAY
GROUP BY customer_id
HAVING reward_share > 0.15
ORDER BY reward_share DESC
LIMIT 50
```

If reward_share > 15%, customer is likely gaming. Apply spend-minimum-per-redemption rule.

### Recipe 7: Trigger campaigns from loyalty data

```python
# 1. Customer about to tier-down (within 60 days of qualification expiry)
sql_at_risk_tier_down = """
SELECT customer_id, current_tier, days_to_tier_down
FROM loyalty_tier_table
WHERE current_tier IN ('Silver','Gold')
  AND days_to_tier_down BETWEEN 0 AND 60
"""

# Pipe to Klaviyo: "Keep your Gold status — make 1 more purchase to qualify"

# 2. Idle members (no activity 90+ days)
# Send 500-pt bonus to reactivate
```

### Recipe 8: Reward inflation prevention

Periodically (annually) reset point earning ratio to reflect AOV inflation. Avoid breakage cliff by giving multi-month notice.

```python
# Reward expiry mechanic
expiry_policy = {
    "points_expire_after_months": 12,
    "warning_days_before_expiry": 30,
    "trigger_message": "Your 1,500 points expire in 30 days. Redeem now!"
}
```

## Examples

### Example 1: DTC ($2M ARR), Shopify + Klaviyo

Decision: Klaviyo Loyalty (native tight loop) OR Smile.io if Klaviyo Loyalty doesn't fit point ladder.

Program:
- 1 pt per $1
- 100 pts = $5 off
- 500 pts = $30 + free shipping
- Silver $250, Gold $750 thresholds
- Birthday + signup bonuses
- 12-month expiry

Expected: repeat purchase rate +30% in 6 months; LTV +25%.

### Example 2: Mid-market beauty DTC ($15M ARR), wants reviews + loyalty unified

Decision: Yotpo (Reviews + Loyalty + SMS).

Program: same point structure + auto-prompt for review post-delivery (200 pts).

### Example 3: SaaS — "Loyalty for subscription"

Note: loyalty platforms above are e-com-first. For SaaS, use:
- Referral via GrowSurf instead (per `referral-program-referralcandy-friendbuy-growsurf`)
- Account-based credit ladders via in-house code
- HubSpot/Salesforce loyalty add-ons

## Edge cases / gotchas

- **Breakage = bad** — unredeemed points sit on the balance sheet as liability. Use 12-month expiry; warn at 30d.
- **Margin destruction at 8%+ redemption rate** — calibrate point cost vs reward value tightly. Track quarterly.
- **VIP tier inflation** — too-easy Gold tier = perks meaningless. Should be 5-10% of customers, not 30%.
- **Stacking with sitewide discount** — block stacking by default; explicit campaign opt-in for combo.
- **Klaviyo Loyalty only if Klaviyo customer** — don't double-stack a separate loyalty vendor.
- **Tax implications on reward value** — high-value rewards may need 1099 reporting in US (consult accounting).
- **GDPR — point balance is PII** — secure storage; right-to-delete includes points.
- **Mobile UX neglect** — Smile.io / Yotpo widgets work on mobile but designs need test. Many widgets render poorly on small screens.
- **Loyalty program ROI is multi-quarter** — don't kill at 60 days; need 2+ purchase cycles.
- **Loyalty vs membership confusion** — paid membership (Amazon Prime) is different model; loyalty is earn-based. Don't conflate in stakeholder communication.

## Sources

- Smile.io: https://smile.io/
- Yotpo Loyalty: https://www.yotpo.com/platform/loyalty/
- LoyaltyLion: https://loyaltylion.com/
- Klaviyo Loyalty: https://www.klaviyo.com/products/loyalty
- Stamped.io: https://stamped.io/
- Customer.io vs Braze 2026 (referenced for retention math): https://www.getvero.com/resources/braze-vs-customer-io-which-is-better-in-2026/
- ProductLed PLG metrics (LTV / repeat purchase): https://www.productled.org/foundations/product-led-growth-metrics
