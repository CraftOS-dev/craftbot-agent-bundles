<!--
Source: https://blog.growthbook.io/introducing-the-first-mcp-server-for-experimentation-and-feature-management/
GrowthBook MCP: 14 tools
-->
# GrowthBook Experiments — SKILL

GrowthBook MCP is the SOTA experimentation + feature-flag automation layer. 14 tools for A/B + multi-variant + holdouts + Bayesian or Frequentist stat significance. Pairs with PostHog (data warehouse), Meta Ads / Google Ads (channel allocation), and Klaviyo (template variants).

## When to use this skill

- **A/B / multi-variant tests** — pricing, copy, layout, onboarding flow.
- **Feature flags** — gradual rollout, kill switches, region targeting.
- **Holdouts** — measure the holistic impact of multiple experiments combined.
- **Bandit / multi-armed allocation** — automatically shift traffic to winners.
- **Statistical significance gating** — auto-stop on `p < 0.01` negative or `> 0.95` positive.
- **Email subject A/B at scale** — variant per Klaviyo flow.

**Do NOT use this skill when:**
- **Pure analytics** with no experiment — use `posthog-growth-loops` skill.
- **Klaviyo subject A/B** — Klaviyo has native AB; only use GrowthBook for cross-channel experiments.

## Setup

### Install

```bash
npx -y growthbook-mcp@latest
```

### Auth — API key + project

```bash
# Get key at https://app.growthbook.io/settings/api-keys
export GROWTHBOOK_API_KEY="<key>"
export GROWTHBOOK_PROJECT_ID="<project>"  # optional
export GROWTHBOOK_API_HOST="https://api.growthbook.io"  # or self-hosted
```

### 14 tools available

**Feature flags (5):**
- `create_feature` — flag name, type (boolean / string / number / JSON), default
- `update_feature` — change default / add rule
- `add_targeting_rule` — % rollout, attribute targeting, force value
- `toggle_feature` — environment-level enable/disable
- `list_features`

**Experiments (6):**
- `create_experiment` — hypothesis, variants, metrics, segments
- `start_experiment` / `stop_experiment` / `archive_experiment`
- `get_experiment_results` — variant performance + significance
- `list_experiments`

**Metrics & data sources (3):**
- `create_metric` — query against data warehouse
- `update_metric`
- `list_data_sources`

## Common recipes

### Recipe 1: A/B test on pricing page (binary feature flag)

```bash
# Step 1: Define the metric (revenue per visitor) — once
mcp tool growthbook.create_metric \
  --name "Revenue Per Visitor (RPV)" \
  --type "revenue" \
  --datasource_id "<warehouse-id>" \
  --sql "SELECT user_id, sum(amount) AS revenue FROM events WHERE event = 'purchase' GROUP BY user_id" \
  --denominator_sql "SELECT DISTINCT user_id FROM events WHERE event = 'page_view' AND properties.path = '/pricing'"

# Step 2: Define hypothesis-driven experiment
mcp tool growthbook.create_experiment \
  --name "Pricing-Page-Annual-Discount-V1" \
  --hypothesis "Showing 20% annual-discount badge above the fold increases RPV by 5%+" \
  --variants '[
    {"name":"control","weight":50,"key":"control"},
    {"name":"annual-badge","weight":50,"key":"variant-annual"}
  ]' \
  --primary_metric_id "<rpv-metric-id>" \
  --secondary_metrics '["<conv-rate>","<aov>"]' \
  --segments '[]' \
  --status "running" \
  --start_date "2026-06-15" \
  --target_sample_size 5000 \
  --auto_stop '{"min_sample_size":1000,"alpha":0.05,"power":0.80}'
```

### Recipe 2: Multi-variant test (4 variants)

```bash
mcp tool growthbook.create_experiment \
  --name "Onboarding-CTA-MultiVar" \
  --hypothesis "Action-oriented CTAs outperform passive" \
  --variants '[
    {"name":"control","key":"Get started","weight":25},
    {"name":"v1","key":"Try free for 14 days","weight":25},
    {"name":"v2","key":"See it in action","weight":25},
    {"name":"v3","key":"Show me how","weight":25}
  ]' \
  --primary_metric_id "<activation-metric>" \
  --target_sample_size 10000
```

GrowthBook auto-corrects for multiple comparisons (Bonferroni or Holm adjustment).

### Recipe 3: Gradual rollout (10% → 100%)

```bash
# Create feature
mcp tool growthbook.create_feature \
  --key "new-checkout-flow" \
  --type "boolean" \
  --default false

# Add gradual rollout rule
mcp tool growthbook.add_targeting_rule \
  --feature_key "new-checkout-flow" \
  --environment "production" \
  --rule '{"type":"rollout","value":true,"percent":10,"hashAttribute":"user_id"}'

# After 1 week, increase
mcp tool growthbook.update_feature \
  --key "new-checkout-flow" \
  --rule_index 0 \
  --rule_update '{"percent":50}'

# Full rollout
mcp tool growthbook.update_feature \
  --key "new-checkout-flow" \
  --rule_update '{"percent":100}'
```

### Recipe 4: Targeted feature (geo + plan)

```bash
mcp tool growthbook.add_targeting_rule \
  --feature_key "premium-onboarding" \
  --environment "production" \
  --rule '{
    "type":"force",
    "value":true,
    "condition":{
      "country":{"$in":["US","CA","UK"]},
      "plan":{"$eq":"premium"}
    }
  }'
```

### Recipe 5: Holdout group (measure compound impact of all experiments)

```bash
# Holdout = 10% of users who see NO experiments
mcp tool growthbook.create_experiment \
  --name "Q3-Holdout-Group" \
  --variants '[
    {"name":"holdout","key":"holdout","weight":10},
    {"name":"normal","key":"normal","weight":90}
  ]' \
  --primary_metric_id "<revenue-per-user-metric>" \
  --status "running"

# All other experiments check: if user is in holdout, force control
```

After 90 days, the holdout group's revenue vs normal users' revenue tells you the cumulative impact of every other experiment.

### Recipe 6: Auto-stop on negative significance

```bash
mcp tool growthbook.create_experiment \
  --name "Risky-Test" \
  --auto_stop '{
    "min_sample_size":1000,
    "alpha":0.01,
    "power":0.80,
    "stop_on_negative":true,
    "stop_on_positive":true,
    "negative_threshold":-0.05
  }' \
  ...
```

If variant performs 5%+ worse with p<0.01, GrowthBook auto-archives and reverts to control.

### Recipe 7: Get results + decide

```bash
mcp tool growthbook.get_experiment_results --experiment_id "<id>"
```

Returns:

```json
{
  "experiment_id": "...",
  "status": "running",
  "sample_size": 4200,
  "variants": [
    {
      "name": "control",
      "users": 2100,
      "primary_metric_value": 12.40,
      "primary_metric_ci": [11.20, 13.60]
    },
    {
      "name": "annual-badge",
      "users": 2100,
      "primary_metric_value": 14.10,
      "primary_metric_ci": [12.85, 15.35],
      "lift": 0.137,
      "chance_to_win": 0.973,
      "p_value": 0.041,
      "significant": true
    }
  ],
  "recommendation": "Ship annual-badge — 13.7% lift, 97.3% chance to win"
}
```

Ship if `chance_to_win > 0.95` AND lift > minimum-effect (set per experiment, typically 2-5%).

### Recipe 8: Variant-driven Klaviyo subject A/B

```python
# Use GrowthBook for cross-channel experiment that drives both website AND email
gb.create_experiment(
    name='Q3-Messaging-Frame',
    variants=[
        {'name':'control','key':'control'},
        {'name':'outcome-led','key':'outcome'},
    ],
    primary_metric='activation_rate',
)

# In Klaviyo template, use variant key as conditional:
# {% if person.gb_variant == 'outcome' %}
#   Subject: "By end of week, you'll have X"
# {% else %}
#   Subject: "Welcome to <product>"
# {% endif %}
```

### Recipe 9: Bandit traffic allocation

```bash
# For long-running tests with no time pressure: shift traffic to winners
mcp tool growthbook.create_experiment \
  --analysis_type "bayesian_bandit" \
  --variants '[...]' \
  --reallocation_frequency "weekly"
```

Bandit converges faster than fixed-split A/B but costs interpretability. Use for ongoing optimization, not hypothesis tests.

## Examples — full experiment program

```yaml
quarterly_experiment_plan:
  q3_2026:
    - id: PRICING-001
      hypothesis: "20% annual badge increases RPV"
      type: A/B
      target_metric: RPV
      duration: 4 weeks
      sample_size_needed: 5000
    - id: ONBOARD-002
      hypothesis: "Skipping email verification increases activation 7d"
      type: A/B
      target_metric: activation_7d
      sample_size_needed: 8000
    - id: CTA-003
      hypothesis: "Outcome-led CTAs > feature-led on landing pages"
      type: multi-variant (4)
      target_metric: signup_conversion
      sample_size_needed: 12000
    - id: HOLDOUT-Q3
      type: holdout (10%)
      target_metric: revenue_per_user
      duration: 90d
```

Cadence: 10+ experiments per month per role.md targets. Winner rate ~30% (per role.md success metrics).

## Edge cases

### Sample size calculation
GrowthBook has built-in calculator: `mcp tool growthbook.calculate_sample_size --baseline 0.05 --mde 0.02 --power 0.80 --alpha 0.05`. Returns users per variant needed.

For low-baseline metrics (< 1% conversion), you need huge samples (50K+). Consider:
- Bigger MDE (3-5% relative lift) instead of 1%
- Proxy metric (engaged session) instead of conversion

### Multiple comparison correction
For >2 variants, apply Bonferroni: `alpha_adj = alpha / num_comparisons`. GrowthBook handles automatically.

### Sequential testing pitfalls
Don't peek before sample size hit + significance threshold. GrowthBook's `auto_stop` uses always-valid sequential bounds — safe to peek.

### Novelty effect
New variants get artificial lift in first 1-2 weeks (curiosity). Don't ship before 2 weeks of data even if significant.

### Survivorship bias
If experiment ran during holidays / atypical period, results don't generalize. Note context in result analysis.

### Identity stitching
Anonymous → identified handoff: GrowthBook uses `anonymousId` until login, then merges. Make sure `anonymousId` cookie persists 6+ months.

### Stat significance is binary; effect size is continuous
"Significant" doesn't mean "important". A 0.5% lift can be significant with 1M users but operationally meaningless. Always check both p-value AND lift magnitude.

### Frequentist vs Bayesian
- **Frequentist** (default): p-value < 0.05, 95% confidence interval. Familiar to most analysts.
- **Bayesian**: chance-to-win probability, credible intervals. More intuitive for stakeholders.

Pick one per project — don't mix.

### Data source latency
GrowthBook pulls metrics from your warehouse (BigQuery, Snowflake, Postgres). Latency 1-24h. Don't expect real-time decisions.

### Holdout group ethics
Holdout users see NO experiments for the duration. Document this if user-facing communications mention "new features."

## Sources

- **GrowthBook MCP announcement**: https://blog.growthbook.io/introducing-the-first-mcp-server-for-experimentation-and-feature-management/
- **GrowthBook docs**: https://docs.growthbook.io/
- **Sample size calculator**: https://docs.growthbook.io/statistics/sample-size
- **Sequential testing math**: https://docs.growthbook.io/statistics/cuped
