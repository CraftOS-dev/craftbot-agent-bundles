<!--
Source: Conjoint.ly Van Westendorp + Gabor-Granger + Monetizely 2026 SaaS pricing
-->
# Price Experimentation — Van Westendorp + Gabor-Granger + Conjoint SKILL

> Run survey-based price research using Van Westendorp PSM (acceptable range), Gabor-Granger (demand curve + revenue-maximizing price), and choice-based conjoint (price-as-attribute). Free + paid execution paths. Python analysis snippets included.

## When to use

Trigger phrases:
- "What should we charge?"
- "Test our pricing"
- "Increase ARPU / price"
- "Van Westendorp / PSM"
- "Gabor-Granger / demand curve"
- "Pricing for new feature / tier"

Pair: `pql-product-qualified-leads-framework` (paid signals), `expansion-revenue-nrr-optimization` (tier upgrades), `growth-model-spreadsheet-compound-levers` (price → revenue model).

## Setup

```bash
# Survey fielding (pick one)
export TYPEFORM_TOKEN="tfp_..."        # free tier 10 questions
export SURVICATE_API_KEY="srv_..."     # cheaper alt
export CONJOINTLY_API_KEY="cnj_..."    # paid; native PSM + Gabor-Granger + conjoint
export QUALTRICS_TOKEN="qtr_..."       # enterprise; native conjoint

# Analysis
pip install numpy scipy pandas matplotlib
```

## Method choice (decision matrix)

| Method | When to use | Sample size needed | Output | Time to insight |
|---|---|---|---|---|
| **Van Westendorp PSM** | Early-stage; acceptable price range; B2B + B2C | ~250-400 ICP | Acceptable price band, optimal price point, point of marginal expensiveness | 1-2 weeks |
| **Gabor-Granger** | Direct demand curve; revenue maximization | 200-300 ICP | Demand curve; revenue curve; optimal price for revenue | 1-2 weeks |
| **Choice-based conjoint** | Multi-attribute (price + features) | 400-800 ICP | Utility scores per attribute incl price; willingness-to-pay per feature | 3-6 weeks |
| **Live A/B pricing** | Stable product, traffic > 5K/wk on pricing page | varies | Direct revenue lift evidence | 2-6 weeks |
| **Cohort price-change experiment** | Already-paying customers | full cohort | Long-term retention impact | 3-6 months |

Sequential use (Conjointly best practice):
1. Van Westendorp → acceptable price range
2. Gabor-Granger within that range → revenue-maximizing point
3. Conjoint → feature/price tradeoffs

## Common recipes

### Recipe 1: Van Westendorp PSM survey design

Four questions (always these four — order matters):

```text
Q1. At what price would you consider [PRODUCT] to be so EXPENSIVE that you would not consider buying it?
Q2. At what price would you consider [PRODUCT] starting to get EXPENSIVE, so that it is not out of the question, but you would have to give some thought to buying it?
Q3. At what price would you consider [PRODUCT] to be a BARGAIN — a great buy for the money?
Q4. At what price would you consider [PRODUCT] to be so INEXPENSIVE that you would feel the quality couldn't be very good?

(Optional Q5: open text on what features they expect at their bargain price)
```

Field via Typeform with input validation (numeric, currency).

### Recipe 2: Van Westendorp analysis (Python)

```python
import numpy as np
import pandas as pd

# Load survey responses
df = pd.read_csv("psm_responses.csv")
# Columns: too_expensive, expensive, bargain, too_cheap

# Build cumulative distributions
prices = np.linspace(df.min().min(), df.max().max(), 200)

# % saying "too expensive" at or below each price (cumulative ascending)
pct_too_expensive = np.array([(df.too_expensive <= p).mean() for p in prices])
# % saying "expensive" (descending complement for crossover with bargain)
pct_expensive = np.array([(df.expensive <= p).mean() for p in prices])
# % saying "bargain" (descending — above this price NOT a bargain)
pct_bargain = np.array([(df.bargain >= p).mean() for p in prices])
# % saying "too cheap" (descending — above this price NOT too cheap)
pct_too_cheap = np.array([(df.too_cheap >= p).mean() for p in prices])

# Key intersections
def find_crossover(a, b, prices):
    idx = np.argmin(np.abs(a - b))
    return prices[idx]

# Optimal Price Point (OPP) = too_cheap × too_expensive crossover
opp = find_crossover(pct_too_cheap, pct_too_expensive, prices)
# Indifference Price Point (IPP) = bargain × expensive crossover
ipp = find_crossover(pct_bargain, pct_expensive, prices)
# Point of Marginal Cheapness (PMC) = too_cheap × bargain crossover (lower bound)
pmc = find_crossover(pct_too_cheap, pct_bargain, prices)
# Point of Marginal Expensiveness (PME) = too_expensive × expensive crossover (upper bound)
pme = find_crossover(pct_too_expensive, pct_expensive, prices)

print(f"Acceptable range:  ${pmc:.0f} – ${pme:.0f}")
print(f"Optimal price (OPP): ${opp:.0f}")
print(f"Indifference price (IPP): ${ipp:.0f} (median acceptable)")
```

Interpretation:
- Price below PMC → seen as cheap, quality concern
- PMC to OPP → mass-market sweet spot
- OPP to IPP → premium positioning still acceptable
- Above PME → unacceptable to most

### Recipe 3: Gabor-Granger survey design

```text
Show prices in random order:
"Would you buy [PRODUCT] at $X per month?"
Yes / No

Test 5-7 price points spanning hypothesized range.
e.g., $9, $19, $29, $49, $79, $99, $149

Optionally show context: feature list, competitor price.
```

### Recipe 4: Gabor-Granger analysis (revenue-maximizing price)

```python
import numpy as np
import pandas as pd

# Survey responses: each row = (price_offered, would_buy 0/1, respondent_id)
df = pd.read_csv("gg_responses.csv")

# % willing to buy at each price
prices_tested = sorted(df.price.unique())
demand = []
for p in prices_tested:
    pct = df[df.price == p].would_buy.mean()
    demand.append(pct)

# Compute expected revenue per respondent at each price
revenue = [p * d for p, d in zip(prices_tested, demand)]

# Revenue-maximizing price
opt_price = prices_tested[np.argmax(revenue)]
opt_revenue = max(revenue)

print(f"Demand curve: {list(zip(prices_tested, demand))}")
print(f"Revenue curve: {list(zip(prices_tested, revenue))}")
print(f"Revenue-maximizing price: ${opt_price} (expected ${opt_revenue:.2f}/respondent)")

# Elasticity at each point
elasticity = []
for i in range(1, len(prices_tested)):
    pct_change_q = (demand[i] - demand[i-1]) / demand[i-1]
    pct_change_p = (prices_tested[i] - prices_tested[i-1]) / prices_tested[i-1]
    elasticity.append(pct_change_q / pct_change_p)
```

### Recipe 5: Conjoint analysis design (choice-based)

```text
Show respondent N choice sets (8-12 typical). Each set has 3-4 product profiles.
Each profile = bundle of attributes (price + 3-5 features).

Example profile:
  Plan: Pro
  Price: $39/mo
  Features:
    - 10 GB storage
    - Email support
    - Mobile app: yes
    - Integrations: 50+

"Which would you choose?"
A / B / C / None

Use Conjointly or Qualtrics to generate orthogonal design.
```

### Recipe 6: Conjoint analysis (utility extraction, Python)

```python
# Hierarchical Bayes is standard; here's a simple multinomial logit
from sklearn.linear_model import LogisticRegression
import pandas as pd

df = pd.read_csv("conjoint_responses.csv")
# Columns: respondent_id, choice_set, profile_features (dummied), chosen (0/1)

# Fit MNL
X = df.drop(columns=["respondent_id", "choice_set", "chosen"])
y = df.chosen
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# Utility per attribute level
utilities = dict(zip(X.columns, model.coef_[0]))

# Willingness-to-pay for a feature
# WTP = utility_of_feature / (utility_per_dollar of price)
price_coef = utilities["price"]  # negative
wtp_for_feature = -utilities["feature_X"] / price_coef
print(f"WTP for feature_X: ${wtp_for_feature:.2f}/month")
```

For production: use Sawtooth Software or Conjointly's built-in HB.

### Recipe 7: Conjoint.ly — paid platform shortcut

```bash
curl -X POST "https://app.conjointly.com/api/v1/studies" \
  -H "X-API-Key: $CONJOINTLY_API_KEY" \
  -d '{
    "type": "psm_gabor_granger",
    "product_name": "Acme Pro Plan",
    "ranges": {"psm_min": 5, "psm_max": 200, "gg_levels": [9, 19, 29, 49, 79, 99, 149]},
    "currency": "USD",
    "target_n_responses": 300,
    "ICP_filter": {"country": ["US","CA","UK"], "role": ["pm","engineer","designer"]}
  }'
```

Conjointly handles fielding, sampling, analysis automatically.

### Recipe 8: Live A/B pricing test (when traffic permits)

```javascript
// GrowthBook feature flag controls pricing page tier
await growthbook.create_experiment({
  name: "tier-2-pricing",
  variants: [
    { name: "control_$29", weight: 0.5, attributes: {tier_2_price: 29} },
    { name: "treatment_$39", weight: 0.5, attributes: {tier_2_price: 39} }
  ],
  primary_metric: "revenue_per_visitor",
  secondary_metrics: ["tier_2_signup_rate", "downgrade_to_tier_1"],
  guardrails: ["total_signup_rate"],
  sample_size: 8000,
  mde_revenue_pct: 0.10
});
```

Treat customers fairly: if priced higher, honor original price for any signed-up. Some teams use price-segmentation (geo, market) to avoid this.

### Recipe 9: Cohort price-change for existing customers

```text
1. Define cohort: paying customers on plan X
2. Notify 30+ days in advance of price change
3. Hold-out 10% (grandfather) for control
4. Measure: churn, expansion, NRR, support tickets
5. Compare cohort vs control over 6 months
```

Don't change prices < 30 days notice (legal + reputation risk).

### Recipe 10: Plan tier collapse / split decision

```python
# Tier-collapse signal
if low_tier_users / total_users > 0.7 and low_tier_revenue / total_revenue < 0.2:
    print("Consider tier-collapse — low tier consuming attention disproportionate to revenue")

# Tier-split signal (add new tier above current top)
if top_tier_NRR > 1.30 and top_tier_users > 50:
    print("Consider tier-split — top tier shows expansion appetite; introduce 'enterprise' tier")
```

## Examples

### Example 1: B2B SaaS, "What should we charge for Pro plan?"

Sample size: 280 respondents (ICP = PM, eng manager, design lead at SMB-MM).

Van Westendorp results:
- PMC = $19; PME = $89; OPP = $39; IPP = $52

Gabor-Granger within $19-89:
- Prices: 19, 29, 39, 49, 59, 79, 89
- Demand: 0.71, 0.62, 0.51, 0.38, 0.28, 0.15, 0.08
- Revenue/respondent: 13.5, 18.0, 19.9, 18.6, 16.5, 11.9, 7.1

Recommendation: Pro at $39 (PSM-optimal + GG revenue-max). Test live A/B before committing to $49.

### Example 2: New feature pricing (conjoint)

Conjoint study on bundling "AI insights" into Pro tier.

WTP for AI insights = $14/mo. Recommendation: increase Pro from $39 to $49 with AI bundled, or charge $9 as add-on (capturing some value while keeping conversion).

### Example 3: DTC e-com price test

Use live A/B on landing page price. Traffic > 50K/wk pricing page = feasible in 2 weeks.

Treatment: $69 vs $89 (control). Measure: AOV, conversion rate, revenue per visitor, return rate.

## Edge cases / gotchas

- **Stated preference ≠ revealed preference** — survey respondents overstate willingness to pay 30-50%. Discount accordingly.
- **Sample size for PSM** — < 150 = noisy; 250-400 best practice; > 500 diminishing returns.
- **ICP filter critical** — surveying everyone surveys nobody. Tight ICP filter > broad panel.
- **Anchor bias** — if you show competitor prices first, anchors responses. Either show no anchor or show consistent anchor.
- **Currency + market** — $100 in US ≠ $100 in EU emotionally. Field per-market with PPP adjustment.
- **Existing customer survey ≠ prospect survey** — existing pay for sunk cost reasons; ask prospects.
- **Conjoint design errors** — orthogonality + level balance matter; use Conjointly / Qualtrics to generate.
- **Live A/B pricing — fairness** — show same price to same user across sessions; price-test only new visitors.
- **Holiday/season** — prices test poorly around BFCM, holiday, summer slumps; pick stable weeks.
- **GDPR — sample sourcing** — panel providers must consent participants; verify before fielding.

## Sources

- Conjointly — Van Westendorp PSM: https://conjointly.com/products/van-westendorp/
- Conjointly — Gabor-Granger: https://conjointly.com/products/gabor-granger/
- Conjointly — PSM vs Gabor-Granger choice guide: https://conjointly.com/blog/gabor-granger-or-van-westendorp/
- Monetizely — Van Westendorp vs Gabor-Granger for SaaS: https://www.getmonetizely.com/articles/van-westendorp-vs-gabor-granger-for-saas-which-pricing-methodology-to-choose
- Sawtooth Software (conjoint standard): https://sawtoothsoftware.com/
- GrowthBook MCP (live A/B): https://blog.growthbook.io/introducing-the-first-mcp-server-for-experimentation-and-feature-management/
- Patrick Campbell — SaaS pricing benchmarks: https://www.priceintelligently.com/
