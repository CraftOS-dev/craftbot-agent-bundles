<!--
Source: Aakash Gupta "Mastering Metrics for PM 2026" + Amplitude NSM framework + Google HEART + Dave McClure AARRR
-->
# Metrics Frameworks — North Star / OMTM / AARRR / HEART SKILL

> Choose, define, and validate a metrics framework (NSM + AARRR + HEART + OMTM). Tests NSM correlation to revenue, maps inputs to owners, ships a one-page metrics decision doc.

## When to use

Trigger phrases:
- "Define our North Star metric"
- "AARRR vs HEART vs NSM"
- "What's our OMTM for Q3?"
- "Map product metrics"
- "Stakeholder alignment on growth metric"

Pair: `growth-model-spreadsheet-compound-levers` (NSM at top of model), `signup-to-revenue-flywheel` (NSM lives at center), `viral-coefficient-k-measurement` (K as input metric).

## Setup

```bash
export POSTHOG_PERSONAL_API_KEY="phx_..."
export AMPLITUDE_OAUTH_TOKEN="amp_..."
export POSTGRES_URL="postgresql://..."   # for MRR correlation
export NOTION_TOKEN="ntn_..."             # output destination
```

## Framework decision matrix

| Framework | Best for | Granularity | When to use |
|---|---|---|---|
| **NSM (North Star Metric)** | Whole-business alignment | Single metric | Org-wide focus; predicts revenue |
| **AARRR (Pirate Metrics)** | Funnel mental model | 5 stages | Simple full-funnel; early-stage |
| **HEART** | Feature / UX | 5 dimensions | Feature launches; UX research |
| **OMTM (One Metric That Matters)** | Quarterly focus | 1 metric | Sprint or quarterly OKR |
| **4-Fits (Brian Balfour)** | Strategy / motion | 4 fit checks | PLG vs sales-led decisions |
| **Counter-metric** | Goodhart prevention | Pair with primary | Prevent gaming |

Hybrid (most teams 2026): NSM at top + AARRR for org alignment + HEART for feature teams + OMTM for quarterly focus + counter-metrics for safety.

## NSM definition criteria

1. **Measurable** — daily/weekly trackable in real time
2. **Value-aligned** — moves when users get value (not just activity)
3. **Lead-indicator** — predicts revenue by ≤ quarter lag
4. **Single number** — not a basket; org can rally on one

## NSM examples by motion

| Motion | NSM | Input metrics |
|---|---|---|
| Consumer social | Weekly active users (DAU/MAU > 50%) | Activation, content creation rate, retention |
| B2B SaaS PLG | Weekly active teams ≥ N seats | Activation rate, team-size growth, 7-day retention |
| B2B SaaS enterprise | Logo NRR (or net new ARR) | Expansion %, churn %, CSM activity |
| Marketplace | Monthly transactions | Supply-demand match, seller activation, repeat buyer rate |
| DTC e-com | LTV-weighted active customers | Repeat purchase rate, AOV, retention |
| Media | Weekly minutes consumed | DAU, sessions per user, content depth |
| Edtech | Course completions / week | Lesson completion, retention, learner engagement |
| Fintech | Monthly active deposits | Onboarding completion, transaction frequency |

## Common recipes

### Recipe 1: Validate NSM via correlation to revenue

```sql
-- PostHog HogQL or postgres
SELECT
  toStartOfWeek(timestamp) AS week,
  countDistinct(person_id) FILTER (WHERE event = 'core_action') AS nsm_value,
  -- Join MRR (from billing system)
  (SELECT SUM(mrr) FROM subscriptions WHERE start_date <= week AND end_date > week) AS mrr
FROM events
WHERE timestamp >= now() - INTERVAL 12 MONTH
GROUP BY week
ORDER BY week
```

```python
import pandas as pd
import scipy.stats

df = pd.read_sql(query, db)
corr_pearson = scipy.stats.pearsonr(df.nsm_value, df.mrr)
corr_spearman = scipy.stats.spearmanr(df.nsm_value, df.mrr)
# Pearson > 0.8 + Spearman > 0.8 → strong NSM
# < 0.6 → vanity; pick another candidate
```

Lag check: correlate NSM(week_t) with MRR(week_t+4..t+13). If NSM lags MRR by months → not a true NSM.

### Recipe 2: Input metric design (3-5 levers per NSM)

```text
NSM: Weekly active teams ≥ 3 seats

Input 1: Activation rate (% new signups → 3-seat team within 14 days)
Input 2: 7-day retention of activated teams
Input 3: Team-size growth rate (seats added per active team per month)
Input 4: Re-engagement rate of dormant teams (returned within 30 days of dormancy)
Input 5: Cross-team activation (teams using ≥ 2 product surfaces)

Each input has:
  - Owner (PM/engineering/marketing)
  - Current value + benchmark
  - Quarterly target
  - 2-3 experiments running
```

### Recipe 3: AARRR mapping (5-stage funnel)

| Stage | Definition | Metric | Tool |
|---|---|---|---|
| **Acquisition** | First touch | New visitors / new signups | GA4, PostHog `web_analytics` |
| **Activation** | First aha | Activation rate (7d) | PostHog cohort, Amplitude funnel |
| **Retention** | Comes back | Day 7/30/90 retention | PostHog `retention` |
| **Revenue** | Pays | MRR, ARPU, paid conversion % | Stripe + DB |
| **Referral** | Brings others | K (viral coefficient) | HogQL invite query |

```python
aarrr = {
    "Acquisition": {"weekly_new_signups": 1200, "target": 1500, "owner": "Marketing"},
    "Activation": {"rate_7d": 0.32, "target": 0.45, "owner": "Product"},
    "Retention": {"d30": 0.27, "target": 0.35, "owner": "Product"},
    "Revenue": {"mrr": 412000, "target": 500000, "owner": "Growth"},
    "Referral": {"K": 0.18, "target": 0.35, "owner": "Growth"}
}
```

### Recipe 4: HEART mapping (Google UX framework)

| Dimension | Metric | Use |
|---|---|---|
| **Happiness** | NPS, CSAT, satisfaction | UX quality |
| **Engagement** | DAU/MAU, session duration | Stickiness |
| **Adoption** | New feature adoption % | New launch |
| **Retention** | Day 30 retention | Product health |
| **Task success** | Funnel completion, error rate | Specific tasks |

Use HEART for feature-level decisions; AARRR/NSM for org-level.

### Recipe 5: OMTM selection (quarterly focus)

```text
OMTM = One Metric That Matters for this quarter.

Criteria:
  - Movable in 90 days
  - Sub-component of NSM (not the NSM itself)
  - Highest current leverage point
  - Org can rally on one

Examples:
  Q1: "Reduce TTV p50 from 4h to 1h"
  Q2: "Lift activation from 32% to 45%"
  Q3: "Push K from 0.18 to 0.35"
  Q4: "Increase NRR from 102% to 115%"
```

### Recipe 6: Counter-metric (Goodhart prevention)

Every primary metric needs a counter-metric so it can't be gamed.

| Primary | Counter | Why |
|---|---|---|
| DAU | DAU per user (engagement depth) | DAU can rise via shallow opens |
| Activation rate | D30 retention of activated | Cheap activation rate → users drop fast |
| Signup rate | Activation rate of signups | Cheap signups = junk |
| MRR | NRR | MRR can grow via leaky-bucket new |
| K (viral) | Invitee activation rate | High K with low invitee activation = empty calories |
| Trial-to-paid conv | 60-day post-conversion retention | Pushy conversion = early churn |

### Recipe 7: One-page metrics doc (Notion via notion-mcp)

```markdown
# [Product] Metrics — June 2026

## North Star
**Weekly active teams ≥ 3 seats:** 1,847 (target 2,200 by Q3 end)

## Input metrics (3-5 levers)
1. Activation rate: 31% (target 45%; owner: Product)
2. 7-day retention: 64% (target 70%; owner: Product)
3. Team-size growth: 1.4 seats/active-team/mo (target 1.8; owner: Growth)
4. Re-engagement: 11% (target 18%; owner: Marketing)

## OMTM Q3
**Reduce TTV p50 from 4h to 1h.** Drives input #1.

## Counter-metrics
- D30 retention of activated (prevent activation-gaming)
- NPS (prevent revenue-gaming)
- Unsubscribe rate (prevent message-gaming)

## Cadence
- NSM: weekly review (Monday standup)
- Inputs: bi-weekly review
- OMTM: weekly
- HEART (per-feature): launch + week 4 + week 12

## Owner alignment
| Metric | Owner | Co-owner |
|---|---|---|
| NSM | Growth lead | CEO |
| Activation | PM (onboarding) | Eng lead |
| ...
```

### Recipe 8: Avoid common NSM mistakes

```text
BAD NSM examples + why:
- "MAU" — vanity; doesn't represent value
- "Pageviews" — surface metric; users browse without value
- "Total signups" — top-of-funnel; ignores quality
- "Revenue" — output, not lead-indicator; can't act on it directly

GOOD NSM examples:
- "Weekly active teams" — value-aligned, weekly trackable, predicts revenue
- "Monthly minutes consumed" (media) — value-aligned, predicts ad rev
- "Course completions / week" (edtech) — value-aligned, predicts retention
- "Repeat purchase rate" (DTC) — value-aligned, predicts LTV
```

### Recipe 9: Test framework selection

```python
def recommend_framework(org_stage, motion, team_size):
    if org_stage == "pre-PMF":
        return ["AARRR", "Sean Ellis Test"]
    if motion == "PLG" and team_size > 20:
        return ["NSM + AARRR + HEART"]
    if motion == "sales-led":
        return ["NSM + AARRR + ARR-based metrics"]
    if org_stage == "feature-launch":
        return ["HEART (per-feature) + AARRR-stage feature"]
    return ["NSM + AARRR"]
```

### Recipe 10: 4-Fits (Brian Balfour) — motion-level check

```text
1. Market ↔ Product — does product solve the market's problem?
2. Product ↔ Channel — does product fit channel's content/format/intent?
3. Channel ↔ Model — does channel CAC fit model's LTV?
4. Model ↔ Market — does pricing/packaging fit market's willingness-to-pay?

If any of the 4 fits is broken → growth stalls regardless of tactics.
85% of forced PLG-to-sales transitions fail because of 4-fits mismatch.
```

## Examples

### Example 1: B2B SaaS PLG, 50-person org

Output (Notion doc):
- NSM: Weekly active teams ≥ 3 seats
- Inputs: activation, retention, team-growth, re-engagement
- OMTM Q3: TTV reduction
- HEART for new features (resource center, analytics dashboard)

Correlation check (Recipe 1): NSM ↔ MRR Pearson 0.87 → confirmed.

### Example 2: DTC e-com

NSM: LTV-weighted active customers (LTV per cohort × customers active in last 90d)
Inputs: repeat purchase rate, AOV, lifecycle email engagement
OMTM Q3: increase 60-day repeat rate from 24% → 30%

### Example 3: Pre-PMF startup

Skip NSM (too early). Use AARRR + Sean Ellis Test.
Focus on activation (`activation-funnel-aha-moment` skill).

## Edge cases / gotchas

- **NSM gaming** — incentivizing NSM growth without counter-metric → quality collapse. Always pair counter-metric.
- **Picking the wrong NSM** — survival bias from "MAU worked for Facebook" doesn't mean MAU works for B2B.
- **NSM that lags** — if NSM moves AFTER revenue, it's not lead-indicator; pick another.
- **OMTM rotation chaos** — changing OMTM mid-quarter destroys focus. Commit to 12-13 weeks.
- **AARRR + HEART overlap** — both have retention; use HEART for feature-specific, AARRR for org.
- **Framework theater** — having metrics doc ≠ acting on metrics. Cadence + ownership matter.
- **Single NSM during platform-vs-product transition** — when product becomes platform, NSM definition may shift; re-validate annually.
- **NSM that's an output, not behavior** — "revenue" isn't an NSM; revenue is what NSM predicts.
- **Multi-product orgs** — one NSM works for single-product; multi-product portfolios need per-product NSMs + portfolio dashboard.
- **Geo / region-specific NSMs** — global products may need per-region NSM if dynamics differ.

## Sources

- Aakash Gupta — Mastering Metrics for PM 2026: https://www.aakashg.com/metrics-for-product-managers/
- Amplitude — North Star framework: https://amplitude.com/north-star
- Google HEART framework (UX): https://research.google.com/pubs/archive/36299.pdf
- Dave McClure — AARRR Pirate Metrics: https://500hats.typepad.com/500blogs/2007/09/startup-metrics.html
- Brian Balfour — 4 Fits framework: https://brianbalfour.com/four-fits-growth-framework
- Product Compass — AARRR: https://www.productcompass.pm/p/aarrr-pirate-metrics
- HyperAct — Product metrics frameworks: https://www.hyperact.co.uk/blog/product-metrics-frameworks
- Gust de Backer — NSM definition: https://gustdebacker.com/north-star-metric/
- Sean Ellis — PMF survey: https://www.startup-marketing.com/the-startup-pyramid/
