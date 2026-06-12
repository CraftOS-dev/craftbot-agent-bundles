<!--
Source: Google Meridian + Meta Robyn + PyMC-Marketing + improvado MMM vs MTA + Appier Meridian guide
-->
# Attribution — Last-Touch + Multi-Touch + MMM (Meridian / Robyn / PyMC) SKILL

> Multi-method attribution: last-touch (tactical), data-driven multi-touch (GA4 / HockeyStack / Dreamdata / Triple Whale), and MMM (Meta Robyn / Google Meridian May 2026 GeoX / PyMC-Marketing). Plus reallocation rules and lift-test validation.

## When to use

Trigger phrases:
- "What's our attribution model?"
- "Multi-touch attribution"
- "Marketing Mix Modeling / MMM"
- "Robyn or Meridian?"
- "Reallocate marketing budget"
- "How much did [channel] contribute?"
- "Geo-incrementality test"

Pair: `growth-model-spreadsheet-compound-levers` (CAC inputs), defer to `marketing-agent` for channel execution.

## Setup

```bash
# OSS Python MMM libs (via cli-anything uvx)
uvx --from robyn python -c "from robyn import Robyn"
uvx --from pymc-marketing python -c "import pymc_marketing"
git clone https://github.com/google/meridian && pip install -e meridian

# Multi-touch B2B
export HOCKEYSTACK_API_KEY="hs_..."
export DREAMDATA_API_KEY="dd_..."

# Multi-touch DTC
export TRIPLEWHALE_API_KEY="tw_..."
export NORTHBEAM_API_KEY="nb_..."

# GA4 attribution
export GA4_PROPERTY_ID="..."
export GA4_TOKEN="..."

# Data warehouse
export POSTGRES_URL="postgresql://..."
```

## Method decision matrix

| Method | Use when | Output | Strength | Limitation |
|---|---|---|---|---|
| **Last-touch** | Quick tactical | Channel: last % | Free, fast | Biased to bottom-funnel |
| **First-touch** | Awareness measurement | Channel: first % | Free | Biased top-funnel |
| **Linear** | Equal-credit baseline | Channel: equal % | Simple | Naive |
| **Time-decay** | Recency-weighted | Channel: weighted % | Better than last | Arbitrary decay rate |
| **U-shape / Position** | First+last weighted | First+last+rest | Common practice | Arbitrary weights |
| **Data-driven (GA4)** | Tactical default | Per-channel %; per-conv | Algorithmic | Cookieless decay; opaque |
| **Multi-touch (MTA)** | User-level B2B / DTC | Per-touchpoint % | Granular | Identity stitching required |
| **MMM (Robyn/Meridian)** | Strategic budget allocation | Response curves + budget alloc | Privacy-durable | Slow refresh (Q); aggregate |
| **Lift test (geo / hold-out)** | Validation of MMM/MTA | Causal incrementality | Causal | Expensive; limited per Q |
| **GeoX (Meridian May 2026)** | Geo-incrementality | Per-channel geo lift | Built-in to Meridian | New, less proven |

## Common recipes

### Recipe 1: GA4 data-driven attribution pull

```bash
curl -X POST "https://analyticsdata.googleapis.com/v1beta/properties/$GA4_PROPERTY_ID:runReport" \
  -H "Authorization: Bearer $GA4_TOKEN" \
  -d '{
    "dimensions": [{"name": "sessionSource"}, {"name": "sessionMedium"}],
    "metrics": [{"name": "conversions"}, {"name": "purchaseRevenue"}],
    "dateRanges": [{"startDate": "2026-03-01", "endDate": "2026-06-01"}],
    "metricAggregations": ["TOTAL"],
    "attributionSettings": {
      "reportingAttributionModel": "DATA_DRIVEN"
    }
  }'
```

Free; fast; tactical default. Use as baseline before deeper analysis.

### Recipe 2: Meta Robyn MMM (Python)

```python
from robyn import Robyn
import pandas as pd

# Load: weekly spend per channel + revenue + control vars
df = pd.read_csv("weekly_data.csv")
# Columns: week, revenue, spend_meta, spend_google, spend_tiktok, spend_youtube,
#          spend_content, control_holiday, control_promo, control_competitor_promo

r = Robyn(
    dt_input=df,
    dt_holidays=holidays_df,
    date_var="week",
    dep_var="revenue",
    dep_var_type="revenue",
    paid_media_spends=["spend_meta", "spend_google", "spend_tiktok", "spend_youtube"],
    organic_vars=["spend_content"],
    context_vars=["control_holiday", "control_promo", "control_competitor_promo"],
    window_start="2024-01-01",
    window_end="2026-06-01"
)

r.fit(iterations=5000, trials=5, nevergrad_algo="TwoPointsDE")
r.plot_response_curves()

# Output: response curves per channel + optimal budget allocation
optimal_budget = r.budget_allocator(target_value="total_revenue")
print(optimal_budget)
```

Need ≥ 2 years weekly data + minimum 3-4 paid channels for stable fit.

### Recipe 3: Google Meridian MMM (Python)

```python
from meridian import data, model, analyzer
import pandas as pd

# Load same shape as Robyn
df = load_meridian_data()

# Setup model
ml = model.Meridian(
    data=df,
    n_chains=4,
    n_warmup=1000,
    n_samples=2000
)

# Fit
ml.sample_posterior()

# Analyze
ana = analyzer.Analyzer(ml)
ana.plot_response_curves()
ana.plot_marginal_roi()

# May 2026 — GeoX for geo-incrementality
geox = ana.geox_test(
    paid_channel="spend_meta",
    holdout_geos=["CA", "TX", "FL"],
    test_duration_weeks=8
)
print(geox.incrementality_estimate)
```

Meridian is Google's OSS MMM. GeoX (May 2026) replaces lift-test consultancy.

### Recipe 4: PyMC-Marketing (Bayesian alternative)

```python
import pandas as pd
from pymc_marketing.mmm import MMM, GeometricAdstockTransformation, LogisticSaturationTransformation

df = pd.read_csv("weekly_data.csv")

mmm = MMM(
    date_column="week",
    target_column="revenue",
    channel_columns=["spend_meta", "spend_google", "spend_tiktok"],
    control_columns=["control_holiday", "control_promo"],
    adstock=GeometricAdstockTransformation(),
    saturation=LogisticSaturationTransformation()
)
mmm.fit(df, draws=2000, chains=4)
mmm.plot_components_contributions()
```

Strong for teams with PyMC familiarity; very expressive prior specification.

### Recipe 5: HockeyStack multi-touch B2B

```bash
curl -X GET "https://api.hockeystack.com/v1/attribution" \
  -H "Authorization: Bearer $HOCKEYSTACK_API_KEY" \
  -G \
  --data-urlencode "start_date=2026-03-01" \
  --data-urlencode "end_date=2026-06-01" \
  --data-urlencode "model=multi_touch_data_driven" \
  --data-urlencode "conversion_event=closed_won"
```

Returns per-channel per-touchpoint contribution to closed-won pipeline.

### Recipe 6: Triple Whale DTC multi-touch

```bash
curl -X GET "https://api.triplewhale.com/v1/attribution" \
  -H "Authorization: Bearer $TRIPLEWHALE_API_KEY" \
  -G \
  --data-urlencode "start_date=2026-03-01" \
  --data-urlencode "end_date=2026-06-01" \
  --data-urlencode "model=data_driven"
```

DTC-native; Shopify-deep.

### Recipe 7: Manual multi-touch via SQL (warehouse)

```sql
-- U-shape attribution (40% first + 40% last + 20% middle distributed)
WITH touchpoints AS (
  SELECT
    user_id,
    timestamp,
    channel,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY timestamp) AS pos,
    COUNT(*) OVER (PARTITION BY user_id) AS total_touches
  FROM marketing_touchpoints
)
SELECT
  channel,
  SUM(CASE
    WHEN pos = 1 AND total_touches = 1 THEN 1.0  -- single-touch = 100% credit
    WHEN pos = 1 THEN 0.40                        -- first 40%
    WHEN pos = total_touches THEN 0.40            -- last 40%
    ELSE 0.20 / (total_touches - 2)               -- middle 20% distributed
  END) AS attributed_conversions
FROM touchpoints t
JOIN conversions c ON c.user_id = t.user_id
WHERE c.converted_at IS NOT NULL
GROUP BY channel
ORDER BY attributed_conversions DESC
```

### Recipe 8: Reallocation decision rule

```python
def should_reallocate(channel, mmm_result, mta_result, lift_test_result=None):
    """Reallocate ONLY when 2+ methods agree."""
    mmm_direction = "scale" if mmm_result["incremental_lift"] > 0.10 else "cut"
    mta_direction = "scale" if mta_result["attributed_growth"] > 0.10 else "cut"
    
    if mmm_direction != mta_direction:
        return ("hold", "MMM and MTA disagree; investigate or lift-test")
    
    if abs(mmm_result["incremental_lift"]) < 0.10:
        return ("hold", "Below MDE (10% shift)")
    
    # If both agree + lift test confirms → reallocate
    if lift_test_result and lift_test_result["confirms_direction"]:
        return (mmm_direction, f"Reallocate by {mmm_result['incremental_lift']*100:.0f}%")
    
    return ("plan_lift_test", "Two methods agree; validate via lift test before reallocating")
```

### Recipe 9: Lift test design (geo-holdout)

```python
def design_lift_test(channel, total_spend, n_geos=4):
    """
    Hold paid channel out in N geos for 8 weeks.
    Measure incremental revenue.
    """
    return {
        "channel": channel,
        "treatment_geos": ["NY", "WA", "TX", "FL"],   # paid spend continues
        "holdout_geos": ["CA", "IL", "GA", "NC"],     # paid spend = 0
        "matched_pairs": True,                          # match treatment+holdout by similar baseline
        "test_duration_weeks": 8,
        "primary_metric": "incremental_revenue_per_geo",
        "min_significance": 0.10,
        "estimated_cost_in_lost_revenue": 0.08 * total_spend  # ~8% holdout
    }

# Use Meridian GeoX (May 2026) for automated execution
```

### Recipe 10: Attribution stack recommendation by motion

```text
DTC e-com (small):
  Tactical: GA4 data-driven + Triple Whale lite
  Strategic: PyMC-Marketing (free Bayesian)

DTC e-com (mid-large):
  Tactical: GA4 + Triple Whale
  Strategic: Meridian + GeoX validation
  Validation: quarterly Meta + Google lift studies

B2B PLG:
  Tactical: GA4 + HockeyStack OR Dreamdata
  Strategic: Robyn + Meridian
  Validation: holdout cohort by paid channel

B2B Enterprise:
  Tactical: HockeyStack OR Dreamdata
  Strategic: Robyn (long sales cycle modeled)
  Validation: pre/post analysis on territory tests
```

### Recipe 11: Cookieless decay handling

GA4 attribution degrades with cookie restrictions (Safari ITP, iOS 14.5+). 2026 typical decay: 30-50% conversion under-attribution.

Mitigations:
- Server-side tracking (Conversions API for Meta, sGTM for Google)
- First-party CDP identity stitch
- MMM doesn't rely on cookies (advantage 2026)

## Examples

### Example 1: DTC e-com $5M ARR, "Where should we spend?"

Tactical: GA4 says Meta = 35% of conversions; last-touch says 12%. Big gap.

Strategic: Robyn fit (2 years data) shows Meta incrementality = 28% of revenue, saturation curve flattening above $40K/wk.

Reallocation: shift $5K/wk from Meta → Google (which is below saturation).

Validation: schedule geo holdout (Recipe 9) Q3 to confirm direction.

### Example 2: B2B PLG, "Is content driving paid signups?"

Tactical: HockeyStack U-shape attributes 22% of closed-won to organic content.

Strategic: Robyn fit (with organic_var = published_content_count) shows content lag = 12 weeks; long-tail compounds.

Plan: keep content budget; don't cut even though tactical attribution is "middle of funnel".

### Example 3: Hybrid B2B + DTC

Use Dreamdata for B2B side (account-level identity) + Triple Whale for DTC side.

Quarterly: PyMC-Marketing Bayesian MMM combining all channels.

## Edge cases / gotchas

- **Last-touch reallocation antipattern** — last-touch is biased to bottom-funnel; cutting top-funnel "because it doesn't attribute" kills the loop. NEVER reallocate solely on last-touch.
- **MMM needs ≥ 2 years weekly data** — fewer years = unstable fit. If new business, can't yet do MMM; use MTA + lift tests.
- **Adstock + saturation choices matter** — geometric vs Weibull adstock; logistic vs Hill saturation. Try multiple; pick best fit (out-of-sample).
- **Multicollinearity in MMM** — if Meta + Google spend correlate (synced campaign launches), models can't separate; randomize launches.
- **MMM ≠ MTA** — MMM is aggregate; MTA is user-level. They answer different questions; both are valuable.
- **Cookieless DTC tactical attribution unreliable** — under-attribution 30-50% means tactical reports lie about big chunks. MMM corrects.
- **GeoX needs geo-level data** — Meridian's GeoX requires per-geo spend + outcome. Some businesses don't have it.
- **Lift tests expensive** — running a geo holdout = 8% revenue loss for 8 weeks in holdout geos. Limit per quarter.
- **Attribution chasing tail** — refining attribution to 2nd decimal doesn't unlock growth; spend energy on creative / new channels.
- **Channel-specific incentives gaming** — affiliate / influencer pays per attributed sale; the attribution model used affects payouts. Document the model contractually.
- **Multi-region complications** — different regions have different journey shapes; per-region MMM if scale warrants.
- **Bot traffic inflating MTA** — strip bot traffic before MTA analysis.

## Sources

- Google Meridian (OSS MMM): https://github.com/google/meridian
- Appier — Meridian guide: https://www.appier.com/en/blog/what-is-marketing-mix-modeling-mmm-a-complete-guide-to-meridian-and-how-it-revolutionizes-traditional-approaches
- Meta Robyn (OSS MMM): https://facebookexperimental.github.io/Robyn/
- PyMC-Marketing: https://github.com/pymc-labs/pymc-marketing
- HockeyStack PLG B2B attribution: https://www.hockeystack.com/
- Triple Whale DTC: https://www.triplewhale.com/
- Improvado — MMM vs MTA: https://improvado.io/blog/mmm-vs-multi-touch-attribution
- Xictron — Multi-touch attribution 2026: https://www.xictron.com/en/blog/marketing-attribution-multi-touch-2026/
- GA4 attribution docs: https://support.google.com/analytics/answer/10596866
- Dreamdata (B2B): https://dreamdata.io/
