<!--
A/B testing email. Klaviyo native A/B + Customer.io split tests.
GrowthBook for multi-variant. Gate on CTR + revenue, not opens.
-->
# A/B Testing Email (Subject / Preview / Copy / CTA / Send Time) — SKILL

A/B test subject lines, preview text, copy, CTA, send time. Klaviyo + Customer.io native split tests; GrowthBook for multi-variant. Gate winners on click rate / revenue per recipient — never opens.

## When to use

- "A/B test the next campaign subject"
- "Run multi-variant test on preview text + CTA color"
- "Compare send-time hypothesis (Tuesday 10am vs Thursday 2pm)"
- "Statistical significance check on last A/B"
- "Set up bandit testing for evergreen welcome series"

## Setup

```bash
# Most ESPs have native A/B. For multi-variant:
npm i -g growthbook    # CLI for setup
pipx install statsig   # Statsig alternative
```

Auth:

```bash
export KLAVIYO_API_KEY="pk_<key>"
export CIO_APP_API_KEY="Bearer <key>"
export GROWTHBOOK_API_KEY="<key>"
```

## Common recipes

### Recipe 1: Sample size calculator (before any test)

Determine required sample per variant before running:

```python
import math
from scipy.stats import norm

def required_sample(baseline_rate, mde_relative, alpha=0.05, power=0.80):
    """
    baseline_rate: current CTR (e.g., 0.04 = 4%)
    mde_relative:  minimum detectable effect as fraction of baseline (e.g., 0.10 = 10% relative lift)
    """
    p1 = baseline_rate
    p2 = baseline_rate * (1 + mde_relative)
    pooled = (p1 + p2) / 2
    z_alpha = norm.ppf(1 - alpha/2)
    z_beta  = norm.ppf(power)
    n = ((z_alpha * math.sqrt(2 * pooled * (1 - pooled)) + z_beta * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2) / (p2 - p1) ** 2
    return math.ceil(n)

# Example: CTR 4%, want to detect 10% lift
print(required_sample(0.04, 0.10))    # ~12,200 per variant
print(required_sample(0.04, 0.25))    # ~2,000 per variant
print(required_sample(0.04, 0.50))    # ~510 per variant
```

If your list is < required, test bigger MDE (e.g., 25%, 50%) — small lifts won't reach significance.

### Recipe 2: Klaviyo subject A/B campaign

```bash
curl -X POST "https://a.klaviyo.com/api/campaigns" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"campaign","attributes":{
    "name":"June newsletter (A/B subject)",
    "audiences":{"included":["<segment-id>"]},
    "send_strategy":{
      "method":"smart_send_time"
    },
    "campaign_messages":{"data":[
      {"type":"campaign-message","attributes":{
        "label":"A",
        "channel":"email",
        "content":{"subject":"5 tips to level up","preview_text":"Quick reads, big impact","from_email":"hello@mail.brand.com","from_label":"Brand"},
        "template_id":"<template-id>"
      }},
      {"type":"campaign-message","attributes":{
        "label":"B",
        "channel":"email",
        "content":{"subject":"You wanted to grow — here is how","preview_text":"5 tips, ranked by impact","from_email":"hello@mail.brand.com","from_label":"Brand"},
        "template_id":"<template-id>"
      }}
    ]},
    "ab_test_settings":{
      "split_percentage":25,
      "winner_metric":"click_rate",
      "test_duration_hours":4
    }
  }}}'
```

Klaviyo sends 25% to variant A, 25% to variant B; after 4 hours of measurement, the winner (by `click_rate`) sends to remaining 75%.

Critical: set `winner_metric` to `click_rate` (or `placed_order_rate` for transactional flows). Default in Klaviyo is open_rate — change it.

### Recipe 3: Multi-variable test (subject + preview + CTA)

```bash
# Create 4 variants: 2x2 factorial
curl -X POST "https://a.klaviyo.com/api/campaigns" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"campaign","attributes":{
    "name":"4-variant: subject × CTA",
    "audiences":{"included":["<segment-id>"]},
    "campaign_messages":{"data":[
      {"type":"campaign-message","attributes":{
        "label":"S1-CTA1",
        "content":{"subject":"5 tips to level up","preview_text":"...","cta_text":"Read tips","cta_color":"#0066ff"},
        "template_id":"<t-1>"
      }},
      {"type":"campaign-message","attributes":{
        "label":"S1-CTA2",
        "content":{"subject":"5 tips to level up","preview_text":"...","cta_text":"Show me","cta_color":"#ff6600"},
        "template_id":"<t-2>"
      }},
      {"type":"campaign-message","attributes":{
        "label":"S2-CTA1",
        "content":{"subject":"You wanted to grow","preview_text":"...","cta_text":"Read tips","cta_color":"#0066ff"},
        "template_id":"<t-3>"
      }},
      {"type":"campaign-message","attributes":{
        "label":"S2-CTA2",
        "content":{"subject":"You wanted to grow","preview_text":"...","cta_text":"Show me","cta_color":"#ff6600"},
        "template_id":"<t-4>"
      }}
    ]},
    "ab_test_settings":{
      "split_percentage":20,
      "winner_metric":"conversion_rate",
      "test_duration_hours":24
    }
  }}}'
```

### Recipe 4: Customer.io split test

```bash
curl -X POST "https://api.customer.io/v1/campaigns/<id>/split_test" \
  -H "Authorization: $CIO_APP_API_KEY" \
  -d '{
    "variants":[
      {"label":"A","template_id":"<t-a>","subject":"5 tips"},
      {"label":"B","template_id":"<t-b>","subject":"You asked for tips"}
    ],
    "split_percentage":50,
    "winner_metric":"clicked",
    "winner_threshold_hours":48
  }'
```

### Recipe 5: Send-time test (cohort-level)

Test whether 10am Tuesday vs 2pm Thursday performs better for engaged segment:

```bash
# Wave 1: Tuesday 10am
curl -X POST "https://a.klaviyo.com/api/campaigns" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"campaign","attributes":{
    "name":"Send-time test: Tue 10am",
    "audiences":{"included":["<segment-half-1>"]},
    "send_strategy":{"method":"static","datetime":"2026-06-09T10:00:00-04:00"},
    "campaign_messages":{"data":[...]}
  }}}'

# Wave 2: Thursday 2pm — same template, same segment-half-2 (random partition)
curl -X POST "https://a.klaviyo.com/api/campaigns" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"campaign","attributes":{
    "name":"Send-time test: Thu 2pm",
    "audiences":{"included":["<segment-half-2>"]},
    "send_strategy":{"method":"static","datetime":"2026-06-11T14:00:00-04:00"},
    "campaign_messages":{"data":[...]}
  }}}'
```

### Recipe 6: Smart Send Time on/off test

```bash
# Control: static send (cohort optimal)
# Treatment: Smart Send Time (per-profile)
# Same template, random 50/50 split of engaged cohort, observe CTR + RPR
```

### Recipe 7: From-name test

```bash
# Variant A: "Brand"
# Variant B: "Sam at Brand"
# Variant C: "Sam Smith"

# Same campaign body; just from_label differs
```

Often "Sam at Brand" wins for first-name recall; pure name "Sam Smith" wins for B2B / B2B-feel.

### Recipe 8: GrowthBook for multi-variant + holdouts

```bash
# Create experiment in GrowthBook
curl -X POST "https://api.growthbook.io/api/v1/experiments" \
  -H "Authorization: Bearer $GROWTHBOOK_API_KEY" \
  -d '{
    "name":"Welcome series subject test",
    "hypothesis":"Personalized subject beats generic",
    "variations":[
      {"name":"Generic","weight":0.5},
      {"name":"Personalized","weight":0.5}
    ],
    "metrics":["click_rate","placed_order_rate"],
    "ownerName":"Email team"
  }'

# Inject variant assignment into Klaviyo via custom property
# When user enters welcome flow, assign variant via API; route accordingly
```

### Recipe 9: Bandit / multi-armed bandit for evergreen flows

For long-running flows where you want to continuously optimize:

```python
# Thompson sampling — simple bandit
import random
from collections import defaultdict

class BanditTest:
    def __init__(self, variants):
        self.variants = variants
        self.successes = defaultdict(int)
        self.failures = defaultdict(int)

    def pick(self):
        # Beta distribution per variant
        samples = {v: random.betavariate(self.successes[v]+1, self.failures[v]+1) for v in self.variants}
        return max(samples, key=samples.get)

    def record(self, variant, success):
        if success: self.successes[variant] += 1
        else: self.failures[variant] += 1

# Use in welcome flow
bandit = BanditTest(['A','B','C','D'])
for new_subscriber in get_new_subscribers():
    variant = bandit.pick()
    send_welcome(new_subscriber, variant)
    # On click event, bandit.record(variant, True); on no-click 48h, bandit.record(variant, False)
```

### Recipe 10: Significance check on completed test

```python
import math
from scipy.stats import norm

def proportion_test(a_n, a_x, b_n, b_x, alpha=0.05):
    """a_n = sends, a_x = clicks for A; same for B"""
    p1, p2 = a_x/a_n, b_x/b_n
    pool = (a_x + b_x) / (a_n + b_n)
    se = math.sqrt(pool * (1 - pool) * (1/a_n + 1/b_n))
    z = (p2 - p1) / se if se else 0
    p_value = 2 * (1 - norm.cdf(abs(z)))
    # Confidence interval for lift
    lift = p2 - p1
    se_lift = math.sqrt(p1*(1-p1)/a_n + p2*(1-p2)/b_n)
    ci_low = lift - 1.96 * se_lift
    ci_high = lift + 1.96 * se_lift
    return {
        'a_rate': p1, 'b_rate': p2,
        'absolute_lift': lift, 'relative_lift': lift/p1,
        'ci_95': (ci_low, ci_high),
        'z': z, 'p_value': p_value, 'significant': p_value < alpha
    }

print(proportion_test(5000, 200, 5000, 234))
# {'a_rate': 0.04, 'b_rate': 0.0468, 'absolute_lift': 0.0068, 'relative_lift': 0.17,
#  'ci_95': (0.0015, 0.012), 'z': 2.47, 'p_value': 0.014, 'significant': True}
```

### Recipe 11: Don't fall for these patterns

| Pattern | Why it's wrong |
|---|---|
| "A vs B run for 2h, A won by 8%" | 2h sample is opens not clicks; insufficient sample |
| Winner picked on open rate | Opens are MPP-inflated; meaningless |
| "Discount test: 30% off won" | At what revenue cost? Lift × AOV - 30% of every order; often net-negative |
| "Send-time test inconclusive after 1 send" | Need ≥ 4 waves to capture day-of-week variance |
| "Subject A won by 12% on 200 sends" | 200 is far below required sample for any real lift detection |
| "Multi-variant 6-arm with no Bonferroni correction" | Higher arm count = higher false-positive risk; correct alpha |

## Examples

### Example 1: Subject A/B for weekly newsletter

**Goal:** newsletter CTR has plateaued; test subject variants.

**Steps:**

1. Determine required sample (Recipe 1). Current CTR 3%; want to detect 15% lift → ~5,000/variant.
2. Engaged segment has 30,000 → easily covers test.
3. Create A/B campaign with 25% split (Recipe 2). Set winner_metric = click_rate, duration 4h.
4. Klaviyo auto-picks winner and sends to remaining 75%.
5. Post-send, pull metrics (Recipe 10). Compute confidence interval.
6. If significant: adopt winning pattern for next 4 weeks; then retest variant.
7. If not significant: try a bigger contrast (different style, not just different words).

### Example 2: Send-time optimization for B2B nurture

**Goal:** B2B audience — when's best send time?

**Steps:**

1. Hypothesis: Tuesday 10am ET (industry default) beats Wednesday 2pm.
2. Split engaged B2B segment 50/50 randomly.
3. Send same content at two times (Recipe 5).
4. Repeat for 4 weeks (each week, re-randomize split).
5. Aggregate week-over-week. Compute CTR + RPR per send time.
6. Run significance test (Recipe 10).
7. If Tue 10am consistently wins: lock as default; consider Smart Send Time for additional per-profile lift.

## Edge cases

- **Insufficient sample size** is the #1 A/B failure. Always calculate (Recipe 1) before running.
- **Multiple-comparison correction** — running 6 variants requires alpha ÷ 6 (Bonferroni) OR FDR correction.
- **Novelty effects** — first test of a new style may pop; sustain 4+ weeks to confirm.
- **Klaviyo default winner metric is open_rate** — ALWAYS override to click_rate or conversion_rate.
- **A/B testing within flows** — Klaviyo supports it; Customer.io supports it; same caveats apply.
- **Holdout group missing** — for "did this campaign drive revenue beyond baseline?", you need a holdout (no-send) cohort. Klaviyo doesn't natively support; use GrowthBook + warehouse.
- **Confounding variable: time of day for transactional vs marketing** — send-time test for marketing must use marketing-eligible cohorts only.
- **Send time × MPP interaction** — Apple Mail's pre-fetch happens at various times based on when the mailbox is checked. Doesn't change CTR analysis materially.
- **Don't A/B test layout in welcome flow first** — too many variables (new subscriber experience). Establish baseline first.
- **Cumulative lift compounds** — small lifts (5% each) over 10 tests = 60%+ cumulative. Run tests continually.

## Sources

- [Klaviyo A/B testing](https://help.klaviyo.com/hc/en-us/articles/115005075928)
- [Customer.io split tests](https://customer.io/docs/journeys/campaigns/split-test-campaign/)
- [GrowthBook](https://docs.growthbook.io/)
- [Statsig](https://docs.statsig.com/)
- [Statistical significance — Evan Miller calculator](https://www.evanmiller.org/ab-testing/sample-size.html)
- [Bandit algorithms — UCB / Thompson](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/)
- [Litmus subject line guide](https://www.litmus.com/blog/best-practices-for-email-subject-lines/)
