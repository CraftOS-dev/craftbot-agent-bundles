<!--
Sources: https://www.reforge.com/blog/community-led-growth + https://www.commonroom.io/blog/measuring-community-roi/ + https://openviewpartners.com/blog/community-led-growth/ + https://docs.getdbt.com/ + https://posthog.com/docs
-->
# Community ROI (Retention + Expansion + Advocacy + Deflection + Brand Love) — SKILL

Five-dimensional ROI model per Reforge CLG framework: (1) Retention lift (members vs non-members LTV delta), (2) Expansion lift (member NRR vs non-member NRR), (3) Advocacy lift (referral conversion vs paid), (4) Support deflection (community-answered % of would-be tickets), (5) Brand love (NPS / share-of-positive-sentiment). dbt model joining Common Room members → HubSpot/Salesforce deals → product retention cohorts → CSAT. Quarterly board-grade slide with explicit assumptions + comparison cohort + statistical significance.

## When to use

- Quarterly community business review.
- Annual board-grade community impact deck.
- Building business case to expand community team / budget.
- Defending community spend in budget cuts.
- Migrating from vanity-metric reporting to revenue-grounded ROI.
- Pricing-tier impact analysis (do community members convert higher?).
- CAC-blended-with-community calculation.
- Cross-link to `community-led-growth-measurement` (input metrics) and `community-led-plg-motion` (PLG instrumentation).

Trigger phrases: "community ROI", "community business case", "board deck community", "retention lift", "expansion lift", "advocacy lift", "support deflection", "NRR community", "CAC community", "CLG measurement", "Reforge community", "community ROI calculator".

## Setup

```bash
# Warehouse access (community signals + CRM + product + support)
export DB_URL=$(op item get warehouse --fields connection_string)
psql $DB_URL -c "\dt"  # expect: members, community_events, deals, product_events, tickets

# dbt for transformations
pip install dbt-core dbt-postgres
dbt init community_roi
cd community_roi
# Configure profiles.yml with $DB_URL

# Common Room API for member roster
mcp tool cli-anything.curl \
  --url "https://app.commonroom.io/api/v1/members?limit=1000" \
  --headers "Authorization: Bearer $COMMON_ROOM_TOKEN"

# PostHog for product retention
mcp tool posthog-mcp.query \
  --hogql "SELECT count(distinct person_id) FROM events WHERE event = 'feature_used'"

# HubSpot for deal expansion
mcp tool hubspot.deals_list --properties amount,closedate,community_member

# Statsmodels / SciPy for significance testing
pip install scipy statsmodels
```

Auth + env:
- `DB_URL` — warehouse Postgres / Snowflake / BigQuery.
- `COMMON_ROOM_TOKEN` — member roster source.
- `HUBSPOT_TOKEN` — CRM deals + contacts.
- `POSTHOG_PROJECT_API_KEY` — product retention.
- `STRIPE_SECRET_KEY` — revenue source-of-truth.
- `ZENDESK_TOKEN` / `INTERCOM_TOKEN` — support deflection.

Workspace prerequisites:
- Warehouse with `members`, `community_events`, `deals`, `product_events`, `tickets` tables.
- Member-to-CRM join key (email hash or canonical email).
- 6+ months historical data for trailing comparison.
- Comparison cohort selection criteria (matched on ICP + signup-cohort).

## Common recipes

### Recipe 1: Define cohort (the critical decision)

Community ROI calculations stand or fall on cohort selection. Naive: "community members vs everyone else" → confounded by tenure, plan, segment.

Use **matched cohorts**:

```sql
-- Identify community members
WITH community_members AS (
  SELECT DISTINCT m.email, m.first_seen_at
  FROM members m
  WHERE m.platform IN ('discord','slack','circle','discourse')
    AND m.is_employee = false
    AND m.first_seen_at < now() - interval '90 days'  -- mature enough
),
-- Matched non-members: same ICP + signup window + plan
matched_non_members AS (
  SELECT DISTINCT c.email, c.signup_at
  FROM customers c
  LEFT JOIN community_members cm USING(email)
  WHERE cm.email IS NULL
    AND c.icp = 'mid-market'  -- match on ICP
    AND c.signup_at BETWEEN '2025-09-01' AND '2025-12-31'  -- match window
    AND c.plan_tier IN ('member','vip')  -- match plan
)
SELECT * FROM community_members  -- N cohort A
UNION ALL SELECT * FROM matched_non_members;  -- N cohort B
```

Avoid: comparing community members to all-customers. Confounding kills credibility.

### Recipe 2: dim 1 — Retention lift

```sql
-- 12-month survival (still subscribed) at month N
WITH cohort AS (
  SELECT email, signup_at,
         CASE WHEN email IN (SELECT email FROM community_members) THEN 'community' ELSE 'control' END AS arm
  FROM customers
  WHERE signup_at BETWEEN '2025-06-01' AND '2025-08-31'
),
survival AS (
  SELECT c.arm, c.email, c.signup_at,
         MAX(CASE WHEN s.month = 12 AND s.is_active THEN 1 ELSE 0 END) AS retained_12mo
  FROM cohort c
  JOIN subscription_status s ON c.email = s.email
  GROUP BY 1,2,3
)
SELECT arm,
       COUNT(*) AS n,
       AVG(retained_12mo::numeric) AS retention_rate,
       AVG(retained_12mo::numeric) - LAG(AVG(retained_12mo::numeric)) OVER (ORDER BY arm) AS delta
FROM survival
GROUP BY arm;
```

Multiply retention_lift × avg_LTV × cohort_size = **retention dollars**.

### Recipe 3: dim 2 — Expansion lift (NRR)

```sql
-- NRR = (Starting MRR + expansion - downgrade - churn) / Starting MRR
WITH cohort_mrr AS (
  SELECT c.arm,
         c.email,
         FIRST_VALUE(d.mrr) OVER (PARTITION BY c.email ORDER BY d.month) AS start_mrr,
         MAX(d.mrr) FILTER (WHERE d.month = 12) AS end_mrr,
         MAX(d.mrr) FILTER (WHERE d.month = 12) - FIRST_VALUE(d.mrr) OVER (PARTITION BY c.email ORDER BY d.month) AS delta_mrr
  FROM cohort c
  JOIN deal_mrr_monthly d USING(email)
  WHERE d.month <= 12
)
SELECT arm,
       SUM(start_mrr) AS start_mrr_total,
       SUM(end_mrr) AS end_mrr_total,
       SUM(end_mrr) / NULLIF(SUM(start_mrr), 0) AS nrr
FROM cohort_mrr
GROUP BY arm;
```

NRR lift = community arm NRR – control arm NRR.

### Recipe 4: dim 3 — Advocacy lift (referral)

```sql
-- Referrals: signups attributed to a community member's referral link
SELECT
  CASE WHEN referrer_email IN (SELECT email FROM community_members) THEN 'community' ELSE 'other' END AS referrer_arm,
  COUNT(*) AS referrals,
  COUNT(*) FILTER (WHERE converted_at IS NOT NULL) AS converted,
  COUNT(*) FILTER (WHERE converted_at IS NOT NULL)::numeric / NULLIF(COUNT(*), 0) AS conversion_rate
FROM referral_attributions
WHERE created_at > now() - interval '90 days'
GROUP BY 1;

-- Compare community referral CR vs paid-ad CR
SELECT 'paid_ad' AS source, COUNT(*) AS leads, COUNT(*) FILTER (WHERE converted_at IS NOT NULL) AS conv FROM ad_leads
UNION ALL
SELECT 'community_referral', COUNT(*), COUNT(*) FILTER (WHERE converted_at IS NOT NULL) FROM referral_attributions WHERE referrer_email IN (SELECT email FROM community_members);
```

Multiply (community_referral_volume × LTV) – (community_program_cost) = **advocacy dollars**.

### Recipe 5: dim 4 — Support deflection

```sql
-- Tickets that would have been opened, but weren't (deflected via community)
WITH community_resolved_threads AS (
  -- threads where original asker thanked / problem solved in community, never opened ticket
  SELECT thread_id, asker_email, channel, resolved_at
  FROM community_threads
  WHERE marked_resolved = true
    AND asker_email NOT IN (
      SELECT requester_email FROM tickets WHERE created_at BETWEEN resolved_at - interval '24 hours' AND resolved_at + interval '24 hours'
    )
)
SELECT COUNT(*) AS deflected_count,
       COUNT(*) * (SELECT AVG(cost_per_ticket) FROM ticket_cost_model) AS deflected_dollars
FROM community_resolved_threads
WHERE resolved_at > now() - interval '90 days';
```

Cost-per-ticket = (support_team_cost / annual_tickets). Multiply by deflected count = **deflection dollars**.

### Recipe 6: dim 5 — Brand love (NPS + sentiment)

```sql
-- Community member NPS vs non-member NPS
SELECT
  CASE WHEN email IN (SELECT email FROM community_members) THEN 'community' ELSE 'control' END AS arm,
  COUNT(*) AS n,
  AVG(score) AS avg_nps,
  COUNT(*) FILTER (WHERE score >= 9) AS promoters,
  COUNT(*) FILTER (WHERE score <= 6) AS detractors,
  (COUNT(*) FILTER (WHERE score >= 9) - COUNT(*) FILTER (WHERE score <= 6))::numeric / COUNT(*) * 100 AS nps
FROM nps_responses
WHERE created_at > now() - interval '90 days'
GROUP BY arm;
```

Combine with `sentiment-monitoring-in-community` Recipe 5 share-of-positive sentiment over total mentions.

### Recipe 7: Statistical significance

```python
# t-test for retention rate lift
from scipy.stats import ttest_ind_from_stats, proportions_ztest

# Two-proportion z-test for retention
community_retained = 850
community_n = 1000
control_retained = 760
control_n = 1000

stat, pval = proportions_ztest(
    count=[community_retained, control_retained],
    nobs=[community_n, control_n],
)
print(f"Retention lift: {(community_retained/community_n - control_retained/control_n)*100:.1f}pp")
print(f"p-value: {pval:.4f}")
print(f"Significant at α=0.05: {'YES' if pval < 0.05 else 'NO'}")
```

Report on slide: "+9pp retention lift (p=0.003, n=1k+1k, matched cohort)". Without p < 0.05, label as "directional".

### Recipe 8: ROI calc with explicit assumptions

```python
# Output: total community ROI dollars
def calculate_community_roi(metrics: dict, assumptions: dict) -> dict:
    """
    metrics: from queries above
    assumptions: business-side inputs (LTV, cost-per-ticket, program-cost)
    """
    retention_dollars = (
        metrics["retention_lift_pp"] / 100
        * assumptions["avg_LTV"]
        * metrics["community_cohort_size"]
    )
    expansion_dollars = (
        metrics["nrr_lift_pp"] / 100
        * metrics["community_starting_mrr_annualized"]
    )
    advocacy_dollars = (
        metrics["community_referral_volume"]
        * assumptions["avg_LTV"]
        - assumptions["referral_program_cost"]
    )
    deflection_dollars = (
        metrics["deflected_ticket_count"]
        * assumptions["cost_per_ticket"]
    )
    brand_love_proxy = (
        metrics["nps_lift_pts"]
        * assumptions["nps_revenue_multiplier"]
    )

    total = retention_dollars + expansion_dollars + advocacy_dollars + deflection_dollars + brand_love_proxy
    return {
        "retention": retention_dollars,
        "expansion": expansion_dollars,
        "advocacy": advocacy_dollars,
        "deflection": deflection_dollars,
        "brand_love": brand_love_proxy,
        "total": total,
        "community_team_cost": assumptions["community_team_cost"],
        "net_roi": total - assumptions["community_team_cost"],
        "roi_multiple": total / assumptions["community_team_cost"],
    }
```

Print assumptions box on slide; numbers without assumptions are not credible.

### Recipe 9: Board slide template

```markdown
# Community ROI — Q3 2026

## Headline
**5.2x ROI** on community investment ($420k spend → $2.2M attributed impact)

## Five dimensions
| Dimension | Lift | Dollars | Confidence |
|---|---|---|---|
| Retention | +9pp (p=0.003) | $1.1M | ✓ High (n=2k, matched cohort) |
| Expansion (NRR) | +12pp (p=0.018) | $480k | ✓ Significant |
| Advocacy | 4.1x conv vs paid | $390k | ⚠ Directional (small n) |
| Support deflection | 1,800 tickets/qtr | $135k | ✓ High |
| Brand love (NPS) | +7 pts | $95k proxy | ⚠ Estimated |

## Assumptions (the gates we made)
- Avg LTV: $4,400 (Stripe 24mo cohort avg, Q2)
- Cost per ticket: $75 (support team cost / annual ticket volume)
- NPS revenue multiplier: $0.5M per NPS-point (Bain industry benchmark)
- Community team cost: $420k/yr (3 FTE + tooling)

## Comparison cohort design
- Community (n=1,127): joined H1 2025, posted ≥ 1 message
- Control (n=1,089): same H1 2025 signup window, ICP-matched, no community activity
- Tracked from signup → 12 months

## Caveats / what we don't claim
- Self-selection bias: community joiners may differ pre-join in unobservable ways.
- Half of "advocacy" dollars rely on UTM attribution; some referral signal is lost.
- Brand love → revenue multiplier is industry-average; not internally calibrated.

## What this funds
+$1M to community team in 2027 → 2 more FTE + Bevy + Common Room Enterprise.
```

### Recipe 10: dbt model structure

```yaml
# models/community_roi.sql
version: 2

models:
  - name: dim_members
    description: Community member roster with first_seen + tenure
    columns:
      - name: email
        tests: [unique, not_null]
  - name: dim_customers
    description: All paying customers
  - name: fct_subscription_states
    description: Monthly active/inactive per customer per month
  - name: fct_referrals
    description: Attributed referrals with conversion
  - name: fct_tickets_deflected
    description: Tickets that did not open due to community resolution
  - name: mart_community_roi_quarterly
    description: Final ROI table powering board slide
```

```sql
-- models/marts/mart_community_roi_quarterly.sql
{{ config(materialized='table') }}

WITH retention AS (
  {{ ref('int_retention_lift') }}
), expansion AS (
  {{ ref('int_expansion_lift') }}
), advocacy AS (
  {{ ref('int_advocacy_lift') }}
), deflection AS (
  {{ ref('int_support_deflection') }}
), brand_love AS (
  {{ ref('int_brand_love') }}
)
SELECT
  '2026-Q3' AS quarter,
  retention.dollars AS retention_dollars,
  expansion.dollars AS expansion_dollars,
  advocacy.dollars AS advocacy_dollars,
  deflection.dollars AS deflection_dollars,
  brand_love.dollars AS brand_love_dollars,
  ...
FROM retention CROSS JOIN expansion CROSS JOIN advocacy CROSS JOIN deflection CROSS JOIN brand_love;
```

## Examples

### Example 1: First-time ROI calc

**Goal:** Pre-budget season; community lead needs business case to grow team from 2 → 4.

**Steps:**
1. dbt repo scaffolded; warehouse access checked.
2. Cohort selection (Recipe 1) — matched cohorts validated with product analyst.
3. 5-dim queries (Recipes 2-6) run against trailing 12 months.
4. Statistical significance (Recipe 7) — only dims with p < 0.05 reported as "high confidence".
5. ROI calc with explicit assumptions (Recipe 8).
6. Board slide (Recipe 9) reviewed by CFO + product head.

**Result:** $2.2M attributed → 5.2x ROI. Approved: $1M increment.

### Example 2: Quarterly reconciliation

**Goal:** Make community ROI a recurring board input, not a one-off.

**Steps:**
1. dbt repo (Recipe 10) productionized.
2. CI/CD: dbt build on merge, output to mart_community_roi_quarterly.
3. Metabase dashboard reads from mart; published at start of each quarter.
4. Quarterly review meeting: community lead + product analyst review numbers + tweak assumptions.
5. Annual recalibration: refresh LTV / cost-per-ticket / NPS multiplier per Stripe data.

**Result:** Community ROI integrated into board reporting alongside marketing CAC + product retention.

### Example 3: Defending budget under cost cuts

**Goal:** Executive review cutting community team; need defensible numbers.

**Steps:**
1. Pull latest mart_community_roi_quarterly.
2. Stress-test assumptions: cut LTV 30%; cut deflection 50%. Does ROI still net positive?
3. Worst-case ROI ≥ 1.5x → kept as evidence; show full sensitivity table.
4. Counter-pitch: "If we cut team in half, projected impact = $2.2M → $0.9M (deflection drops + advocacy drops). Net = -$1.3M revenue at -$210k cost saved. Net negative."

**Result:** Team retained; budget held.

## Edge cases / gotchas

- **Self-selection bias** — members chose to join; they may be inherently higher-engagement. Acknowledge openly.
- **Cohort matching** — naive match on signup-date alone is weak. Match on plan, ICP, geo, signup-source for credibility.
- **Attribution decay** — referrals from 18-month-old shares hard to track. Set 90-day attribution window.
- **Survivorship in advocacy** — only converted referrals visible; UTM-stripped credits underestimate.
- **NPS sample bias** — only opinionated members respond. Triangulate with share-of-positive-sentiment.
- **Deflection double-count** — if member opens ticket *and* asks in community, don't count both as deflected.
- **Revenue lag** — retention lift in H1 cohort takes ≥12 months to materialize.
- **Reverse causality** — "people who churn less are happier" vs "community causes retention". Treat community as one of N inputs.
- **Bot / employee pollution** — exclude is_employee + is_bot from "community member" definition.
- **No control group** — if community is universal, use historical pre-launch baseline.
- **CFO skepticism** — every dollar will be questioned. Always lead with assumptions; never report just "$2.2M".
- **Confidence intervals over point estimates** — present "$2.0M – $2.4M, 95% CI". Single number invites bike-shedding.

## Sources

- [Reforge — Community-Led Growth](https://www.reforge.com/blog/community-led-growth)
- [Common Room — Measuring Community ROI](https://www.commonroom.io/blog/measuring-community-roi/)
- [OpenView — CLG framework](https://openviewpartners.com/blog/community-led-growth/)
- [Bain — NPS revenue link](https://www.bain.com/insights/introducing-the-net-promoter-system-loyalty-insights/)
- [dbt project docs](https://docs.getdbt.com/)
- [SciPy stats reference](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [statsmodels proportions_ztest](https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportions_ztest.html)
