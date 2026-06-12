<!--
Source: Stackscored referral marketing pricing 2026 + GrowSurf alternatives + Viral Loops referral factory alternatives
-->
# Referral Program — Platform Choice + Incentive Design SKILL

> Pick a referral platform (ReferralCandy / GrowSurf / Friendbuy / Viral Loops / Talkable) and design the program: dual-sided incentive structure, friction-reduction, A/B testable mechanics. Distinct from viral coefficient K (intrinsic loop) — referral = explicit monetary incentive.

## When to use

Trigger phrases:
- "Build a referral program"
- "Refer-a-friend campaign"
- "Which referral platform should we use?"
- "Pre-launch waitlist with virality" (Viral Loops)
- "B2B referral program"
- "Tiered rewards / VIP referral"

Distinct from:
- `viral-coefficient-k-measurement` (intrinsic, no monetary reward)
- `loyalty-program-yotpo-smile-loyaltylion` (post-purchase loyalty, often paired)

## Setup

```bash
export REFERRALCANDY_API_KEY="rc_..."
export GROWSURF_API_KEY="gs_..."
export FRIENDBUY_MERCHANT_KEY="fb_..."
export VIRALLOOPS_API_TOKEN="vl_..."
export TALKABLE_API_KEY="tk_..."
```

## Platform decision matrix (June 2026)

| Tool | E-com fit | SaaS fit | Pricing (2026) | Integrations | Best for |
|---|---|---|---|---|---|
| **ReferralCandy** | Best-in-class | ✗ | $39-799/mo + 0.25-10.5% commission on referred sales | Shopify (deep), Klaviyo, Mailchimp | Shopify e-com |
| **GrowSurf** | ✗ | Best-in-class | $0-custom (participant-based) | Webhooks, Stripe, Segment | SaaS w/ programmatic API |
| **Friendbuy** | ✓ | ✓ | Enterprise revenue-tier, 12-mo contracts | Klaviyo, HubSpot, Salesforce | Enterprise; referral + loyalty unified |
| **Viral Loops** | Mixed | Mixed | $34-499+/mo by contacts | Light integration set | Pre-launch waitlist; viral campaign |
| **Talkable** | Enterprise e-com | ✗ | Enterprise pricing (call) | Shopify Plus, Salesforce, Klaviyo | Enterprise DTC; advanced rules |
| **InviteReferrals** | ✓ | ✓ | $0-499/mo | Shopify, WooCommerce | SMB with multi-channel |
| **Mention Me** | ✓ | Limited | Enterprise | Salesforce, Klaviyo | UK + EU enterprise DTC |

## Selection logic

```text
Q1: Primary use case?
   E-com (Shopify)            → ReferralCandy / Friendbuy / Talkable
   SaaS (subscription)        → GrowSurf / Friendbuy
   Pre-launch / waitlist     → Viral Loops
   Enterprise unified loyalty → Friendbuy / Talkable

Q2: Stack integration?
   Klaviyo-native            → ReferralCandy / Friendbuy
   HubSpot-native            → Friendbuy
   Webhook-only / custom     → GrowSurf

Q3: Budget?
   Bootstrapped              → GrowSurf free / ReferralCandy starter $39
   Mid-market                → ReferralCandy / Viral Loops $200-500/mo
   Enterprise                → Friendbuy / Talkable / Mention Me
```

## Incentive structure design (the deliverable)

### Single-sided vs dual-sided

| Structure | When to use | Typical lift |
|---|---|---|
| Single-sided (referrer gets reward) | Low-friction sharing OK | Baseline |
| Dual-sided (give + get) | Most contexts; ↑ conversion | 2-4x vs single-sided |
| Tiered (refer 5, get bonus) | Power-referrers reward | +30% volume from top 10% |
| Milestone (refer 1, 5, 10) | Gamification + retention | +25% repeat referrals |

### Reward type vs ACV

```text
ACV (1st year value) < $50           → discount 10-30% off / store credit
ACV $50-500                           → free month / cash $25-50
ACV $500-5,000                        → cash $100-500 / extension of contract
ACV $5,000+                           → cash $1,000+ / tier upgrade / partnership ramp
SaaS B2B                              → free seats / credit / extension
E-com                                 → discount / store credit / free product
```

### Friction reduction in share UX

1. One-click share via native iOS/Android share sheet
2. Pre-filled message ("Hey, I love Acme — get $20 here: {link}")
3. Multi-channel: email, SMS, WhatsApp, X, copy-link
4. Personalized link (no signup required from referrer)
5. Track which channel drove most acceptances → tune copy

## Common recipes

### Recipe 1: ReferralCandy — create campaign

```bash
curl -X POST "https://my.referralcandy.com/api/v2/campaigns" \
  -H "Authorization: Bearer $REFERRALCANDY_API_KEY" \
  -d '{
    "name": "Q3 2026 dual-sided",
    "referrer_reward": {"type": "store_credit", "amount": 20, "currency": "USD"},
    "friend_reward": {"type": "discount", "amount_pct": 15, "minimum_order": 50},
    "trigger_event": "first_purchase",
    "minimum_purchase_for_credit": 50
  }'
```

### Recipe 2: GrowSurf — create SaaS referral campaign

```bash
curl -X POST "https://api.growsurf.com/v2/campaigns" \
  -H "Authorization: Bearer $GROWSURF_API_KEY" \
  -d '{
    "name": "SaaS dual-sided",
    "rewards": [
      {"trigger": "referee_signup", "to": "referrer", "type": "free_month"},
      {"trigger": "referee_signup", "to": "referee", "type": "discount", "value": 20}
    ],
    "tiers": [
      {"min_referrals": 1, "reward": "$25 credit"},
      {"min_referrals": 5, "reward": "annual upgrade"},
      {"min_referrals": 10, "reward": "lifetime + branded swag"}
    ]
  }'
```

### Recipe 3: Friendbuy — create enterprise dual program

```bash
curl -X POST "https://api.fbot.me/v1/campaigns" \
  -H "Authorization: Bearer $FRIENDBUY_MERCHANT_KEY" \
  -d '{
    "name": "Enterprise referral",
    "channels": ["email", "sms", "social", "embed_widget"],
    "rewards": {
      "advocate": {"type": "stripe_credit", "amount": 50},
      "friend": {"type": "discount_code", "percent": 20}
    },
    "anti_fraud": {
      "ip_match_block": true,
      "device_fingerprint_match_block": true,
      "min_days_between_referrals": 1
    }
  }'
```

### Recipe 4: Viral Loops — pre-launch waitlist

```bash
curl -X POST "https://app.viral-loops.com/api/v2/campaign" \
  -H "X-API-Key: $VIRALLOOPS_API_TOKEN" \
  -d '{
    "campaignType": "milestone",
    "milestones": [
      {"position": 100, "reward": "Skip the line"},
      {"position": 25, "reward": "First access + branded merch"},
      {"position": 5, "reward": "Lifetime free"}
    ],
    "rewardTrigger": "absolute_position",
    "shareChannels": ["twitter", "linkedin", "facebook", "email", "copy_link"]
  }'
```

### Recipe 5: Track referral via PostHog

```sql
-- Per-referrer K analysis
SELECT
  inviter_id,
  count() AS referrals_sent,
  countIf(referee_signed_up) AS accepted,
  countIf(referee_first_purchase) AS converted,
  accepted * 1.0 / referrals_sent AS accept_rate,
  converted * 1.0 / accepted AS post_signup_conv
FROM events
WHERE event = 'referral_link_used'
GROUP BY inviter_id
ORDER BY converted DESC
LIMIT 100
```

Top 10% of referrers usually drive 60-80% of referrals. Identify; engage with premium tier.

### Recipe 6: A/B test incentive value via GrowthBook

```javascript
await growthbook.create_experiment({
  name: "referral-incentive-value",
  variants: [
    { name: "control_$10/$10", weight: 0.34 },
    { name: "treatment_$20/$20", weight: 0.33 },
    { name: "treatment_$10/$30", weight: 0.33 }
  ],
  primary_metric: "referrals_per_active_user_30d",
  secondary_metrics: ["accept_rate", "ltv_of_referred_user"],
  guardrails: ["cost_per_acquisition"],
  sample_size: 4500
});
```

### Recipe 7: Anti-fraud setup (mandatory for cash incentives)

```python
fraud_rules = {
    "ip_match_block": True,           # Same IP referrer/referee → block
    "device_fingerprint_block": True, # Same device → block
    "email_domain_block": ["mailinator", "tempmail"],
    "max_referrals_per_user_per_day": 5,
    "min_referee_lifetime_days_before_reward": 7,  # Pre-empt instant-cancel
    "manual_review_threshold_dollars": 250
}
```

### Recipe 8: Compute referral ROI

```python
# Referral payback calc
incentive_cost = referrer_reward + referee_reward  # e.g., $20 + $15 = $35
ltv_of_referred = compute_ltv_segmented(source='referral')
margin_on_ltv = ltv_of_referred * gross_margin_pct

if margin_on_ltv > incentive_cost * 3:
    print("Referral economics work; expand")
else:
    print("Tune incentive value down OR find higher-LTV channels")
```

Healthy: referral CAC ≤ 0.5x paid CAC.

## Examples

### Example 1: Shopify DTC ($5M ARR), "Add referral"

Decision: ReferralCandy.

Program:
- Dual-sided: 15% off referee + $20 store credit referrer
- Trigger: post-first-purchase email + Klaviyo flow
- 7-day delay before reward credit (anti-fraud)

Expected: 4-7% referral attribution to total revenue at 90 days.

### Example 2: B2B SaaS PLG ($2M ARR), "Tiered referral"

Decision: GrowSurf.

Program:
- Referrer reward: free month per referee converted
- Tier 5 refs: annual upgrade
- Tier 10 refs: lifetime + swag
- Friend reward: 25% off first 3 months

Expected: 10-15% of new paid users from referral by Q3.

### Example 3: Pre-launch consumer app

Decision: Viral Loops.

Program:
- Position-based waitlist (Robinhood-style)
- Top 100 → early access. Top 25 → branded merch. Top 5 → lifetime.
- Multi-channel share with auto-prefilled copy.

Expected: 5-20x list growth vs no-virality.

## Edge cases / gotchas

- **Fraud at scale** — cash incentives attract bot networks. Mandatory: IP block, device fingerprint, min-tenure before payout.
- **Friction in share UX > incentive size** — increasing reward $5→$20 may lift 10%; reducing share steps from 4→1 lifts 50%+.
- **CAC ≠ incentive value** — many founders forget the operational cost (vendor fees, fraud review, accounting). Calc fully-loaded.
- **Referral attribution overlap** — if a user clicks referral link then Googles brand, last-touch attribution gives credit to organic. Use first-touch or platform attribution.
- **Tax + 1099 reporting for cash rewards > $600/yr/person** — plan for it; Talkable + Friendbuy handle; ReferralCandy doesn't.
- **GDPR + share-this-link friction** — EU users can't see referrer name without consent; design accordingly.
- **Referral program death by neglect** — needs ongoing promotion (post-purchase email, in-app, social) to drive participation. Set up automation, monitor monthly.
- **Cannibalization risk** — referees may have signed up anyway via organic; lift testing required. Geo-holdout (no program in N markets) for 30-60 days.
- **Stacking with discounts** — referral + sitewide promo = margin destruction. Set rules: no stack on items already on sale.
- **Multi-tenant SaaS confusion** — referrer is org admin; referee is the org. Reward goes to admin or org? Decide upfront.

## Sources

- StackScored — referral marketing pricing 2026: https://www.stackscored.com/pricing/referral-marketing/
- GrowSurf alternatives: https://growsurf.com/alternatives/
- Viral Loops — referral factory alternatives: https://viral-loops.com/blog/referral-factory-alternatives/
- ReferralCandy: https://www.referralcandy.com/
- Friendbuy: https://www.friendbuy.com/
- Talkable: https://www.talkable.com/
- Customer.io / Klaviyo integration patterns: https://www.getvero.com/resources/braze-vs-customer-io-which-is-better-in-2026/
