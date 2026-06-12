<!--
Sources:
Van Westendorp PSM — https://help.maze.co/hc/en-us/articles/van-westendorp-pricing
OpenView SaaS pricing — https://www.openviewpartners.com/blog/saas-pricing-tactics
-->
# Pricing + Packaging Experiments — SKILL

Van Westendorp Price Sensitivity Meter via Maze (4-question survey) for price discovery; JTBD outcome clustering for tier design; Statsig/GrowthBook for packaging A/B tests with revenue per visitor as the primary metric. This pack stitches them together.

## When to use

- Discovering the acceptable price range for a new tier or product.
- Designing tier structure (what goes in Free vs Pro vs Enterprise).
- Running an A/B test on different pricing pages or tier configurations.
- Validating a price hike with existing customers before announcing.
- Quarterly pricing review.

Trigger phrases: "test our pricing", "what should we charge", "Van Westendorp", "pricing experiment", "tier structure", "raise prices".

## Setup

```bash
# Three skills compose this:
# - maze-usertesting-user-research (for PSM survey)
# - statsig-growthbook-experiments (for A/B packaging test)
# - amplitude-mixpanel-posthog-product-analytics (for revenue metric)
```

Auth:
- `MAZE_API_KEY`, `STATSIG_CONSOLE_KEY` or `GROWTHBOOK_API_KEY`, analytics keys.

## Common recipes

### Recipe 1: Van Westendorp PSM (4 questions)

```bash
# Launch in Maze (see maze-usertesting-user-research Recipe 3)
curl -X POST "https://api.maze.co/v1/surveys" \
  -H "Authorization: Bearer $MAZE_API_KEY" \
  -d '{
    "name": "Van Westendorp PSM — Pro tier",
    "blocks": [
      {"type":"context","html":"Imagine the Pro tier offers unlimited projects, 10 seats, API access, priority support."},
      {"type":"number","question":"At what price would you consider this TOO EXPENSIVE to buy?"},
      {"type":"number","question":"At what price would you consider this EXPENSIVE but still consider buying?"},
      {"type":"number","question":"At what price would you consider this a GREAT BUY?"},
      {"type":"number","question":"At what price would you consider this SO CHEAP that you would question the quality?"}
    ],
    "sampleTarget": 150
  }'
```

### Recipe 2: Compute PSM intersection points

```python
# Per Recipe 8 of maze-usertesting-user-research, with full math:
import numpy as np

def vw_curves(responses):
    """Compute 4 cumulative curves and find intersection points."""
    too_exp = sorted(r["too_expensive"] for r in responses)
    exp = sorted(r["expensive"] for r in responses)
    cheap = sorted(r["bargain"] for r in responses)   # "great buy"
    too_cheap = sorted(r["too_cheap"] for r in responses)
    n = len(responses)

    def cdf(values, p): return sum(1 for v in values if v <= p) / n
    def survival(values, p): return 1 - cdf(values, p)

    # Test each price point
    prices = np.linspace(min(too_cheap), max(too_exp), 500)
    rows = []
    for p in prices:
        rows.append({
            "p": p,
            "too_exp_cdf": cdf(too_exp, p),
            "exp_cdf": cdf(exp, p),
            "cheap_sf": survival(cheap, p),
            "too_cheap_sf": survival(too_cheap, p)
        })

    # Intersections (approximate — find closest pair)
    def cross(rows, a, b):
        return min(rows, key=lambda r: abs(r[a] - r[b]))["p"]

    return {
        "OPP": cross(rows, "too_cheap_sf", "too_exp_cdf"),  # Optimal Price Point
        "IPP": cross(rows, "cheap_sf", "exp_cdf"),          # Indifference Price Point
        "PME": cross(rows, "too_cheap_sf", "exp_cdf"),      # Point of Marginal Cheapness (lower bound)
        "PMC": cross(rows, "too_exp_cdf", "cheap_sf")       # Point of Marginal Expensiveness (upper bound)
    }

# Acceptable range = PME → PMC
# Optimal = OPP
# Indifference = IPP (where equal % find it cheap vs expensive)
```

### Recipe 3: Plot PSM curves (for the pricing doc)

```python
import matplotlib.pyplot as plt
import numpy as np

def plot_psm(responses, save_path="psm.png"):
    prices = np.linspace(0, max(r["too_expensive"] for r in responses), 200)
    too_cheap = [sum(1 for r in responses if r["too_cheap"] >= p)/len(responses) for p in prices]
    cheap = [sum(1 for r in responses if r["bargain"] >= p)/len(responses) for p in prices]
    exp = [sum(1 for r in responses if r["expensive"] <= p)/len(responses) for p in prices]
    too_exp = [sum(1 for r in responses if r["too_expensive"] <= p)/len(responses) for p in prices]

    plt.figure(figsize=(10,6))
    plt.plot(prices, too_cheap, label="Too cheap")
    plt.plot(prices, cheap, label="Cheap (bargain)")
    plt.plot(prices, exp, label="Expensive")
    plt.plot(prices, too_exp, label="Too expensive")
    plt.xlabel("Price ($)")
    plt.ylabel("% of respondents")
    plt.legend()
    plt.title("Van Westendorp Price Sensitivity Meter")
    plt.grid(True)
    plt.savefig(save_path)
```

### Recipe 4: Packaging A/B test design

```bash
# Test: 2-tier vs 3-tier pricing structure
mcp tool statsig.create_experiment \
  --name "pricing_tier_count" \
  --hypothesis "3-tier (Free / Pro / Business) outperforms 2-tier (Free / Pro) on revenue per visitor" \
  --primaryMetric "revenue_per_visitor" \
  --secondaryMetrics '["conversion_rate","arpu"]' \
  --guardrailMetrics '["trial_signups"]' \
  --variants '[
    {"name":"control_2tier","size":0.5,"description":"Free + Pro $29"},
    {"name":"variant_3tier","size":0.5,"description":"Free + Pro $29 + Business $99"}
  ]' \
  --duration 21
```

### Recipe 5: JTBD-driven tier design

```python
# Group features by outcome → tier; each tier serves a distinct job
TIERS = {
    "Free": {
        "job": "Try the product solo",
        "features": ["1 project","2 seats","Community support","Basic templates"]
    },
    "Pro": {
        "job": "Run my team's work on it",
        "features": ["unlimited projects","10 seats","API access","Email support","Premium templates","Custom domains"]
    },
    "Business": {
        "job": "Get my org standardized",
        "features": ["SSO","Audit log","SOC2 compliance","Dedicated CSM","SLA","Custom integrations"]
    }
}

# Validate: do users in each segment see the matching tier features as differentiators?
```

### Recipe 6: Price elasticity test (revenue impact of a price change)

```bash
# Statsig — show control 50% the old price, variant 50% the new price
mcp tool statsig.create_experiment \
  --name "pro_tier_price_hike" \
  --hypothesis "Raising Pro from $29 to $39 lifts ARPU >25% without hurting conversion >10%" \
  --primaryMetric "arpu" \
  --secondaryMetrics '["conversion_rate","trial_to_paid"]' \
  --guardrailMetrics '["churn_rate"]' \
  --variants '[
    {"name":"control_29","size":0.5,"description":"Pro $29/mo"},
    {"name":"variant_39","size":0.5,"description":"Pro $39/mo"}
  ]' \
  --duration 30 \
  --sequentialTesting true
```

### Recipe 7: Existing-customer price-hike consultation

```bash
# Before announcing, survey existing Pro customers
mcp tool maze.create_survey \
  --name "Existing-customer pricing feedback" \
  --blocks '[
    {"type":"context","html":"We are considering moving Pro from $29 to $39/mo. Existing customers like you would keep $29 for 6 months as a thank-you, then move to $39."},
    {"type":"likert","question":"How would you feel about this change?","scale":5},
    {"type":"open_text","question":"What would make this change feel fair to you?"},
    {"type":"multiple_choice","question":"If we made no changes, would you stay on the current plan?","options":["Definitely yes","Probably yes","Unsure","Probably no","Definitely no"]}
  ]'
```

### Recipe 8: Feature-by-tier packaging matrix

```markdown
# Packaging — Pro vs Business breakdown

| Feature | Free | Pro $29 | Business $99 | Reason |
|---|---|---|---|---|
| Projects | 1 | Unlimited | Unlimited | Pro unlocks core utility |
| Seats | 2 | 10 | Unlimited | Pro fits small teams |
| API access | — | ✓ | ✓ | Differentiator from Free |
| SSO | — | — | ✓ | Enterprise-only need |
| Audit log | — | — | ✓ | Compliance signal |
| SLA | — | — | ✓ | Enterprise contract requirement |
| Dedicated CSM | — | — | ✓ | High-touch ROI |
| Priority support | — | Email | Slack channel | Tier signal |
```

### Recipe 9: Pricing-page A/B test (copy + layout)

```bash
mcp tool growthbook.create_experiment \
  --name "pricing_page_v2" \
  --hypothesis "New comparison-table layout + simplified copy lifts trial signup 15%" \
  --variations '[
    {"key":"control","name":"Current 3-column tier cards","weight":0.5},
    {"key":"v2","name":"Comparison table + outcome-led headers","weight":0.5}
  ]' \
  --goalMetrics '["trial_started"]' \
  --datasource "<datasource-id>"
```

### Recipe 10: Pricing experiment doc template

```markdown
# Pricing Experiment — [Name]

## Hypothesis
[If we change X, then [metric] will improve by Y because [user-rooted reason]]

## PSM data (if applicable)
- OPP: $X
- IPP: $Y
- Acceptable range (PME → PMC): $A → $B
- Sample: N=150

## Tier design
[Recipe 8 matrix]

## A/B test design
- Primary metric: revenue per visitor
- Guardrails: trial_started, churn_rate
- Duration: 21 days
- Sample size: 10k visitors per arm

## Decision rule
- Ship if primary >+10% AND guardrails maintained
- Iterate if primary +5-10% or unclear
- Kill if primary <0% OR guardrail breached

## Readout
[Filled at end]
```

## Examples

### Example 1: New tier launch
**Goal:** Validate a new Business tier at $99/mo before announcing.

**Steps:**
1. Define tier (Recipe 5) — what JTBD does Business serve.
2. Run PSM survey (Recipe 1) targeting current Pro users + enterprise prospects.
3. Compute PSM points (Recipe 2); confirm $99 is within PME → PMC.
4. Set up A/B on the pricing page (Recipe 4) — show 50% old 2-tier, 50% new 3-tier.
5. Wait for sample target; readout (Recipe 10).
6. If ship: announce via the marketing-agent skills.

**Result:** Data-backed Business tier launch.

### Example 2: Price hike consultation
**Goal:** Move Pro from $29 → $39 without churn spike.

**Steps:**
1. Survey existing customers first (Recipe 7) — sentiment baseline.
2. Test new-customer impact (Recipe 6) — A/B at signup.
3. If conversion drops <10% AND ARPU rises >25% → proceed.
4. Grandfather existing customers for 6 months (kindness + churn defence).
5. Announce 60 days ahead via email + in-app.

**Result:** Price hike with managed churn.

## Edge cases / gotchas

- **PSM sample size.** ≥120 responses for stable intersection points.
- **PSM context matters.** Respondents anchor to whatever description you give. Show realistic feature list, not just tier name.
- **Self-report vs revealed preference.** PSM is stated; A/B is revealed. Use PSM for range discovery, A/B for the actual decision.
- **Revenue per visitor variance.** Revenue metrics are high-variance; expect 5-10x the sample size of conversion metrics. Plan duration.
- **Price hike + churn.** Existing-customer churn after price hike usually peaks at 3-6 months post-change; A/B can't capture this — survey + cohort tracking.
- **Don't optimize for short-term revenue.** A price A/B might lift ARPU 25% but degrade trial→paid which compounds. Watch full funnel.
- **Tier proliferation.** 5+ tiers confuse buyers; 3-tier is the SOTA default (Free / Pro / Business) for SaaS.
- **Grandfather clause politics.** Some customers expect free price-locking. Be explicit on contracts.
- **Geographical pricing.** Same $29 hits different in EU vs LATAM. PSM should segment by region for global products.
- **Annual vs monthly framing.** Annual discount (often 17% off) acts as a packaging lever; A/B test annual-default vs monthly-default.

## Sources

- [Van Westendorp PSM — Maze guide](https://help.maze.co/hc/en-us/articles/van-westendorp-pricing)
- [Van Westendorp 1976 original paper (summary)](https://en.wikipedia.org/wiki/Van_Westendorp%27s_Price_Sensitivity_Meter)
- [OpenView — SaaS pricing tactics](https://www.openviewpartners.com/blog/saas-pricing-tactics)
- [Patrick Campbell — ProfitWell pricing strategy](https://www.profitwell.com/blog)
- [Madhavan Ramanujam — Monetizing Innovation](https://www.amazon.com/Monetizing-Innovation-Companies-Design-Around/dp/1119240867)
- [Statsig experiments docs](https://docs.statsig.com)
- [Reforge — Pricing tracks](https://www.reforge.com)
