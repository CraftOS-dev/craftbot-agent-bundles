<!--
Source: ProductLed NRR math + Pocus PQL guide + Reforge expansion playbook
-->
# Expansion Revenue + NRR Optimization SKILL

> Design cross-sell / upsell triggers, measure Net Revenue Retention, identify expansion opportunities. The single best growth lever in established SaaS — best-in-class NRR > 120% means business compounds without new acquisition.

## When to use

Trigger phrases:
- "Increase NRR / net revenue retention"
- "Cross-sell upsell"
- "Expansion revenue"
- "Account-based growth"
- "Tier upgrade triggers"
- "Increase ARPU"

Pair: `pql-product-qualified-leads-framework` (expansion = positive PQL signal), `free-to-paid-upgrade-prompts` (in-app delivery), `behavioral-cohort-design` (audience), `retention-curve-churn-diagnosis-j-smile` (J-curve = expansion-ready cohort).

## Setup

```bash
export POSTGRES_URL="postgresql://..."
export HUBSPOT_TOKEN="hb_..."
export INTERCOM_TOKEN="dG9rOi..."
export POSTHOG_PERSONAL_API_KEY="phx_..."
```

## NRR math (canonical)

```
NRR = (Starting MRR + Expansion - Contraction - Churn) / Starting MRR

Where:
  Expansion = upgrades + cross-sells + seat additions (this cohort, this period)
  Contraction = downgrades + seat reductions
  Churn = lost revenue from cancellations

Benchmarks (2026):
  Best-in-class B2B SaaS: NRR > 120%
  Healthy: 100-120%
  Sub-100% = leaky bucket; new ARR fights churn

GRR (Gross Revenue Retention) = (Start - Contraction - Churn) / Start
  No expansion. Pure leak rate.
  Healthy: > 90%
```

## Expansion lever taxonomy

| Lever | When applicable | Typical lift on NRR |
|---|---|---|
| **Seat expansion** | Multi-seat SaaS | +5-25 pp |
| **Tier upgrade** | Tiered pricing | +10-30 pp |
| **Cross-sell adjacency** | Multi-product portfolio | +15-40 pp |
| **Usage expansion** | Usage-based pricing | +20-60 pp |
| **Add-on / module** | Modular product | +5-20 pp |
| **Multi-year + price escalator** | Enterprise | +5-15 pp |
| **Geo / multi-region** | Global product | +5-15 pp |

## Common recipes

### Recipe 1: NRR calculation (SQL)

```sql
-- Monthly NRR by cohort
WITH cohort AS (
  SELECT
    customer_id,
    DATE_TRUNC('month', subscription_started_at) AS cohort_month
  FROM subscriptions
),
revenue_by_month AS (
  SELECT
    c.cohort_month,
    DATE_TRUNC('month', s.start_date) AS revenue_month,
    SUM(s.mrr) AS mrr
  FROM cohort c
  JOIN subscriptions_history s ON s.customer_id = c.customer_id
  GROUP BY c.cohort_month, DATE_TRUNC('month', s.start_date)
)
SELECT
  cohort_month,
  revenue_month,
  SUM(mrr) AS month_mrr,
  FIRST_VALUE(SUM(mrr)) OVER (PARTITION BY cohort_month ORDER BY revenue_month) AS starting_mrr,
  SUM(mrr) / FIRST_VALUE(SUM(mrr)) OVER (PARTITION BY cohort_month ORDER BY revenue_month) AS nrr_ratio
FROM revenue_by_month
GROUP BY cohort_month, revenue_month
ORDER BY cohort_month, revenue_month
```

### Recipe 2: Decompose NRR (expansion vs churn)

```sql
SELECT
  DATE_TRUNC('month', evt_date) AS month,
  SUM(CASE WHEN evt_type = 'new_mrr' THEN amount END) AS new_mrr,
  SUM(CASE WHEN evt_type = 'expansion' THEN amount END) AS expansion_mrr,
  SUM(CASE WHEN evt_type = 'contraction' THEN -amount END) AS contraction_mrr,
  SUM(CASE WHEN evt_type = 'churn' THEN -amount END) AS churn_mrr,
  -- NRR (excludes new logos)
  (start_mrr + expansion_mrr + contraction_mrr + churn_mrr) / start_mrr AS nrr,
  -- GRR (no expansion)
  (start_mrr + contraction_mrr + churn_mrr) / start_mrr AS grr
FROM mrr_movements
GROUP BY month
ORDER BY month DESC
```

### Recipe 3: Identify expansion triggers (PostHog cohort)

```sql
-- Users showing expansion signals
SELECT person_id, email, expansion_score
FROM (
  SELECT
    person_id,
    countDistinctIf(team_member_invited) AS new_invites_30d,
    countIf(event = 'Premium Feature Attempted') AS premium_attempts,
    countIf(event = 'Limit Approached' AND properties.usage_pct >= 90) AS limit_hits,
    countDistinctIf(event = 'Integration Connected') AS integrations,
    (new_invites_30d * 5 +
     premium_attempts * 3 +
     limit_hits * 4 +
     integrations * 2) AS expansion_score
  FROM events
  WHERE timestamp >= now() - INTERVAL 30 DAY
  GROUP BY person_id
)
WHERE expansion_score >= 15
ORDER BY expansion_score DESC
LIMIT 200
```

Top scorers → AM outreach for AE-led expansion; mid scorers → in-app upgrade prompts.

### Recipe 4: Seat-expansion trigger

```sql
-- Accounts with high seat utilization
SELECT
  account_id,
  current_seats_paid,
  current_seats_active,
  current_seats_active * 1.0 / current_seats_paid AS utilization,
  days_above_80pct_utilization
FROM account_seat_metrics
WHERE current_seats_active * 1.0 / current_seats_paid > 0.85
  AND days_above_80pct_utilization >= 14
ORDER BY current_seats_paid DESC
```

For these accounts: trigger in-app modal "Add seats?" + AE outreach if multi-month sustained.

### Recipe 5: Cross-sell decision (which product to offer)

```python
# Score adjacency probability based on usage pattern + cohort lift
adjacency_score = {
    "core_product_X_usage_high": True,  # qualifies
    "feature_use_signals_Y_need": True,  # behavior matches Y need
    "similar_accounts_adopted_Y": 0.42,  # 42% of accounts like this bought Y
    "Y_LTV_vs_X_LTV": 0.5  # Y is 50% of X LTV (meaningful)
}

# Trigger cross-sell if all 3 first signals + Y_LTV > $100/mo equivalent
if adjacency_score["core_product_X_usage_high"] and adjacency_score["similar_accounts_adopted_Y"] > 0.3:
    trigger_cross_sell(product='Y', method='in-app + email + AM-task')
```

### Recipe 6: Usage-based upsell prompt

```text
Usage > free-tier 80%:    soft email + in-app banner
Usage > free-tier 95%:    modal + email + AM-task
Usage at cap, blocked:    modal + immediate upgrade flow + AE intervene (if high-value)

Same for tiered:
  Tier-1 80% of tier-2-threshold:  show comparison + upgrade nudge
```

### Recipe 7: HubSpot deal create from PQL trigger

```bash
# When expansion_score >= 15 → create HubSpot deal
curl -X POST "https://api.hubapi.com/crm/v3/objects/deals" \
  -H "Authorization: Bearer $HUBSPOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "dealname": "Expansion: Acme Co (auto)",
      "pipeline": "expansion_pipeline",
      "dealstage": "appointmentscheduled",
      "amount": 12000,
      "closedate": "2026-09-01",
      "expansion_signal_score": "23",
      "expansion_signal_breakdown": "seats_at_limit,multiple_integrations,premium_feature_interest"
    },
    "associations": [{"to": {"id": "ACCOUNT_HUBSPOT_ID"}, "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 3}]}]
  }'
```

### Recipe 8: Multi-year discount escalator (enterprise)

```text
Year 1: $50K ACV
Year 2: $60K (20% expansion or 10% escalator + 10% expansion)
Year 3: $72K (20% YoY)

Contractual escalator clause: pre-commit 8-12% YoY raises.
Combined with usage expansion, supports 130%+ NRR.
```

### Recipe 9: NRR cohort by segment

```sql
-- NRR varies wildly by ICP; segment.
SELECT
  icp_segment,
  COUNT(DISTINCT account_id) AS accounts,
  SUM(start_mrr) AS start_mrr,
  SUM(expansion_mrr) AS expansion,
  SUM(churn_mrr + contraction_mrr) AS losses,
  (SUM(start_mrr) + SUM(expansion_mrr) - SUM(churn_mrr + contraction_mrr))
    / SUM(start_mrr) AS nrr
FROM nrr_metrics
WHERE month = '2026-05-01'
GROUP BY icp_segment
ORDER BY nrr DESC
```

Identify segments with NRR > 120% — invest acquisition there. Sub-100% segments — investigate or deprioritize.

### Recipe 10: Anti-cannibalization check

```sql
-- Are cross-sells reducing core product revenue?
SELECT
  customer_id,
  pre_cross_sell_arpu,
  post_cross_sell_arpu,
  post_cross_sell_arpu - pre_cross_sell_arpu AS delta
FROM cross_sell_analysis
WHERE cross_sell_date >= now() - INTERVAL 6 MONTH
```

If delta_avg ≤ 0 → cross-sell is cannibalizing, not expanding.

### Recipe 11: NRR projection scenarios

```python
def project_nrr_scenarios(starting_arr, monthly_movements):
    """
    monthly_movements = {expansion_rate, contraction_rate, churn_rate}
    """
    scenarios = {
        "base":     {"e": 0.02, "c": -0.005, "ch": -0.015},   # 1.0 NRR -> 100%
        "upside":   {"e": 0.04, "c": -0.003, "ch": -0.010},   # 130% NRR
        "downside": {"e": 0.01, "c": -0.010, "ch": -0.025},   # 80% NRR
    }
    for name, params in scenarios.items():
        monthly_factor = 1 + params["e"] + params["c"] + params["ch"]
        annual_nrr = monthly_factor ** 12
        print(f"{name}: monthly factor {monthly_factor:.4f}, annual NRR {annual_nrr*100:.1f}%")
        print(f"   Starting ARR ${starting_arr/1e6:.1f}M -> Year 1 ARR ${starting_arr*annual_nrr/1e6:.1f}M")
```

## Examples

### Example 1: B2B SaaS, NRR = 102% (healthy but unimpressive)

Decompose (Recipe 2):
- Expansion: 8%
- Contraction: -2%
- Churn: -4%

Diagnose: low expansion. Account has seats but no expansion triggers in product.

Plan:
1. Seat-utilization trigger (Recipe 4) — likely 25% of accounts at > 85% utilization, untouched.
2. Premium-feature attempt cohort → upgrade prompts (Recipe 6).
3. Cross-sell module identified via Recipe 5.
4. Target NRR 102% → 115% in 6 months.

### Example 2: Enterprise, NRR = 135% — what's working?

Audit drivers:
- 60% seat expansion (high-utilization accounts auto-buy)
- 25% multi-year escalators
- 15% cross-sell of analytics add-on

Plan:
1. Productize escalator into all new contracts.
2. Train AE on cross-sell timing (post-renewal + 3 months).
3. Target NRR 135% → 145%.

### Example 3: PLG, NRR = 95% (sub-100, leaky)

J-shape retention but tier-1 churn high.

Plan:
1. Tier-1 friction reduction (`activation-funnel-aha-moment`).
2. In-app prompts to upgrade at usage limits (`free-to-paid-upgrade-prompts`).
3. NRR by segment (Recipe 9) — likely tier-1 = 70% NRR; tier-2 = 130%. Strategy: acquire fewer tier-1 OR auto-upgrade.

## Edge cases / gotchas

- **NRR ≠ net new ARR** — NRR is cohort-based; doesn't include new logos. Don't conflate in board metrics.
- **NRR for sub-1-year cohorts is meaningless** — too little time for expansion/contraction movement. Report ≥12-month cohorts.
- **Expansion at the cost of churn** — pushing upgrades on unfit users → churn next month. Track post-expansion retention.
- **Discounts inflate apparent NRR** — discount renewal at $0 expansion may look fine until you net the cost of incentive.
- **Multi-product accounting** — cross-product revenue movement complicates; track per-product NRR + total NRR.
- **Seat metric confusion** — "active seats" vs "paid seats". Paid is the billing metric; active is the engagement metric.
- **Annual billing skews monthly NRR** — annual contracts show big one-month spikes; use trailing-12-month for stability.
- **Cohort comparability** — comparing Q1-2025 cohort NRR vs Q1-2026 cohort NRR after equal time elapsed.
- **Free-to-paid is acquisition, not expansion** — keep these separate in reporting; only paid-to-higher-paid counts as expansion.
- **NRR vs LTV** — different math; LTV averages across cohort + assumes churn rate; NRR observed.

## Sources

- ProductLed PLG metrics (NRR): https://www.productled.org/foundations/product-led-growth-metrics
- Pocus PQL guide (expansion signals): https://www.pocus.com/blog/the-definitive-pql-guide-part-1
- Reforge — Casey Winters expansion playbook: https://www.reforge.com/blog/
- HockeyStack — NRR + multi-touch: https://www.hockeystack.com/resources/manual/plg-product-led-growth
- HubSpot deals API: https://developers.hubspot.com/docs/api/crm/deals
- Patrick Campbell — SaaS metrics: https://www.priceintelligently.com/
- ChartMogul NRR cookbook: https://chartmogul.com/blog/net-revenue-retention/
