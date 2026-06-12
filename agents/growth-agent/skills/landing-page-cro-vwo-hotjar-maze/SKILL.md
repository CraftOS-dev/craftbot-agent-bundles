<!--
Source: GrowthBook experimentation MCP + Microsoft Clarity 2026 free + VWO + Maze testing + Hotjar
-->
# Landing Page CRO — Experiments + Heatmaps SKILL

> Diagnose, hypothesize, A/B-test, and validate landing-page changes. Uses GrowthBook MCP for experiment orchestration (OSS, free), Microsoft Clarity for free heatmaps/replay, Maze for prototype testing, and a statistical-rigor checklist to prevent the "we saw lift" antipattern.

## When to use

Trigger phrases:
- "Improve landing page conversion"
- "A/B test [hero / CTA / pricing page]"
- "Heatmap our landing page"
- "Session replay / where users drop off"
- "Prototype test before code"
- "CRO sprint"

Pair: `signup-activation-conversion-optimization` (signup leak), `price-experimentation-van-westendorp-conjoint` (pricing pages), `signup-to-revenue-flywheel` (full funnel).

## Setup

```bash
# Experimentation
export GROWTHBOOK_API_KEY="gb_..."

# Free heatmap + replay (2026 SOTA free)
# Microsoft Clarity — no API key for collection; script install
# Install script via Clarity dashboard → snippet → embed

# Hotjar (paid alt)
export HOTJAR_API_TOKEN="hj_..."

# Maze (prototype testing)
export MAZE_API_TOKEN="mz_..."

# VWO (full CRO platform)
export VWO_API_TOKEN="vwo_..."
```

## Tool stack (2026)

| Tool | Cost | Use for | Best when |
|---|---|---|---|
| **GrowthBook** | Free (OSS) or Cloud | A/B testing, feature flags | Default — has MCP server, statistical rigor built-in |
| **Microsoft Clarity** | Free | Heatmap + session replay | Always (free!) |
| **Hotjar** | Free starter / $32-171/mo | Heatmap + replay + survey | Use when Clarity insufficient (filters, integration depth) |
| **FullStory** | Enterprise | Replay + analytics | Big org; deep replay forensics |
| **Maze** | Free starter / $99-499/mo | Prototype/usability test before code | Pre-launch validation |
| **VWO** | $200-3000/mo | Full CRO suite (test + heatmap + survey) | Want one-vendor stack |
| **Convert.com** | $99-1099/mo | A/B alt to VWO | Bootstrapped to mid |
| **Statsig** | Free starter / Enterprise | Experimentation + MCP (Knowledge Graph 2026) | Enterprise infosec |

## Common recipes

### Recipe 1: Install Microsoft Clarity (free heatmap)

```html
<!-- Embed in <head> -->
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "CLARITY_PROJECT_ID");
</script>
```

Free, unlimited. Tracks heatmaps + 30-day session replays.

### Recipe 2: GrowthBook MCP — create landing page A/B

```javascript
await growthbook.create_experiment({
  name: "homepage-hero-v3",
  hypothesis: "Headline emphasizing time-savings will lift signup conversion by 8% vs feature-listing headline",
  variants: [
    { name: "control_features", weight: 0.5, content: {headline: "All-in-one analytics suite"} },
    { name: "treatment_outcome", weight: 0.5, content: {headline: "Get to insights in 3 minutes"} }
  ],
  primary_metric: "signup_started",
  secondary_metrics: ["scroll_depth_50pct", "demo_video_played"],
  guardrails: ["bounce_rate"],
  sample_size_calc: {
    baseline_rate: 0.04,
    mde: 0.005,  // 0.5pp absolute
    power: 0.8,
    alpha: 0.05
  },
  kill_criteria: {
    primary_negative_significance: 0.01,
    guardrail_threshold: { bounce_rate: 0.10 }  // +10pp = kill
  },
  auto_stop_on_significance: true
});
```

### Recipe 3: Sample-size calculator (do it before launching)

```python
import math
from scipy.stats import norm

def sample_size_per_arm(baseline_rate, mde_absolute, power=0.8, alpha=0.05):
    """Two-tailed test, equal allocation."""
    z_alpha = norm.ppf(1 - alpha/2)
    z_beta = norm.ppf(power)
    p1 = baseline_rate
    p2 = baseline_rate + mde_absolute
    p_bar = (p1 + p2) / 2
    numerator = (z_alpha * math.sqrt(2 * p_bar * (1 - p_bar)) +
                 z_beta * math.sqrt(p1*(1-p1) + p2*(1-p2)))**2
    return math.ceil(numerator / (mde_absolute**2))

# Example: baseline 4% conversion, want to detect 0.5pp lift
n = sample_size_per_arm(0.04, 0.005)
# n ~= 5400 per arm; 10,800 total; at 10K visits/day = ~1 day
# But run min 2 weeks for novelty + day-of-week
```

### Recipe 4: Heatmap diagnostic decision (Clarity → hypothesis)

```text
Clarity insight              → Hypothesis to test
─────────────────────────────────────────────────
Low scroll depth (< 30%)     → Above-fold copy not compelling; test new hero
Click on non-interactive     → Users expecting more; add CTA or interactivity there
Rage clicks                  → Broken interaction; fix bug first
Dead clicks                  → Misleading copy; clarify language
High exit on pricing tier    → Pricing tier presentation issue → price-experimentation skill
Session length < 15s         → Pre-aha drop; landing page mismatched to ad copy
```

### Recipe 5: Maze — prototype test before code

```bash
curl -X POST "https://api.maze.co/v1/projects" \
  -H "Authorization: Bearer $MAZE_API_TOKEN" \
  -d '{
    "name": "Hero variant test",
    "type": "first_click",
    "prototype_url": "https://figma.com/file/abc",
    "tasks": [
      {"prompt": "Click where you would sign up for the product", "expected_click": "#signup-btn"},
      {"prompt": "Rate how clear the value proposition is", "type": "rating", "scale": 5}
    ],
    "target_n_participants": 50
  }'
```

Maze validates pre-build. 50 participants @ $1-5 each.

### Recipe 6: Funnel-aware experiment (avoid local-optimum trap)

```javascript
// BAD: optimize CTR on homepage button
// → may increase clicks from unqualified users → kill downstream conversion

// GOOD: primary metric is downstream
{
  primary_metric: "signup_completed",  // not button_clicked
  secondary_metrics: ["button_clicked", "form_started"],
  guardrails: ["activation_rate_7d"]    // protect downstream
}
```

### Recipe 7: Multi-page CRO sprint (90-day plan)

```text
Week 1-2: Audit + diagnose
  - Install Clarity if not present
  - Pull funnel from PostHog (homepage → /signup → /verify → activation)
  - Identify top 3 leak pages

Week 3-4: Hypothesize + prioritize
  - Generate 10-15 hypotheses
  - PIE-score (Potential / Importance / Ease)
  - Pick top 5 for next 60 days

Week 5-12: Run experiments (3-5 in flight)
  - GrowthBook for each
  - 2-week minimum runtime
  - Auto-stop on negative significance

Week 13: Document + iterate
  - Log results in Notion
  - Promote winners
  - Plan next sprint
```

### Recipe 8: PIE scoring (prioritization)

```python
# PIE = Potential × Importance × Ease, all 1-10
hypotheses = [
    {"name": "Hero outcome-focused", "P": 8, "I": 9, "E": 7, "score": 8*9*7},
    {"name": "Pricing tier-collapse", "P": 6, "I": 7, "E": 9, "score": 6*7*9},
    # ...
]
hypotheses.sort(key=lambda x: x["score"], reverse=True)
```

### Recipe 9: VWO multivariate (when > 4 variants)

```bash
curl -X POST "https://app.vwo.com/api/v2/campaigns" \
  -H "Authorization: Bearer $VWO_API_TOKEN" \
  -d '{
    "name": "Hero MVT",
    "type": "mvt",
    "factors": [
      {"name": "headline", "variations": ["A", "B"]},
      {"name": "subhead", "variations": ["A", "B"]},
      {"name": "CTA_color", "variations": ["red", "blue"]},
      {"name": "image", "variations": ["product", "people"]}
    ],
    "primary_goal": "signup",
    "sample_size_per_combo": 2500
  }'
```

16 cells. Needs higher traffic. Use only when ≥ 50K weekly sessions.

### Recipe 10: Bayesian + sequential testing (peek-safe)

```javascript
// GrowthBook native Bayesian
{
  statistical_engine: "bayesian",
  decision_threshold: 0.95,  // 95% prob of being winner
  prior: "non_informative",
  // No peeking penalty — can check anytime
}
```

Vs frequentist (default), which inflates false-positive rate if peeked. Bayesian for fast iteration; frequentist for rigorous winners.

## Examples

### Example 1: SaaS homepage, signup conv = 2.8% (low)

Diagnose:
- Clarity: 71% bounce, scroll depth p50 = 28% (most users don't see below fold)
- PostHog funnel: 64% bounce, 12% scroll, 4% CTA click, 2.8% signup

Hypothesis: hero copy too feature-heavy; users don't see value in 3 sec.

Plan:
1. GrowthBook A/B: outcome-headline vs feature-headline (Recipe 2).
2. Sample size: 5400/arm × 2 = 10,800.
3. Runtime: 14 days minimum (avoid novelty + DoW).
4. Maze pre-test: 50 participants rate clarity of 3 candidate headlines.

Result: outcome headline +18% signup conv, p = 0.003. Ship.

### Example 2: DTC pricing page, high exit

Diagnose: Clarity rage-clicks on "Compare plans" tooltip; PostHog funnel shows tier-2 → checkout = 8% (low).

Hypothesis 1: comparison table unclear.
Hypothesis 2: tier-2 overpriced vs tier-1.

Plan:
1. Fix rage-click bug first (tooltip → modal).
2. Run pricing test via `price-experimentation-van-westendorp-conjoint` skill.
3. Then A/B test tier presentation.

### Example 3: B2B, pre-launch landing page

Use Maze for prototype test (no traffic yet).
- 100 participants from target ICP via Maze panels
- Test message-clarity, signup-intent, pricing perception
- Iterate based on quant + qual

Then launch and run GrowthBook experiments post-traffic.

## Edge cases / gotchas

- **Peeking inflates FP rate** — checking mid-experiment with frequentist test multiplies false positives. Use Bayesian or sequential, or commit to fixed sample size.
- **Novelty effect** — new variants get a 1-2 week lift, regress to baseline. Run experiments ≥ 2 weeks; ideally 2 business cycles.
- **Day-of-week confound** — Tuesday traffic differs from Saturday. Always run ≥ 7 days.
- **Sample ratio mismatch** — if 50/50 split returns 55/45 traffic, randomization is broken. Check via chi-squared; abort if SRM.
- **Multiple testing inflation** — testing 5 metrics at α=0.05 → ~22% chance of false positive somewhere. Bonferroni-correct OR pre-register primary metric.
- **Local-optimum trap** — optimizing button clicks ≠ optimizing signups. Always pick downstream primary metric.
- **GDPR — heatmap PII** — Clarity / Hotjar can record form input; mask sensitive fields via CSS class.
- **Mobile vs desktop separately** — combined results hide major shape differences. Run separate experiments for high-traffic platforms.
- **Bot traffic skews** — filter known bot UAs + suspicious IPs before analysis.
- **Holiday traffic distortion** — Black Friday lifts everything; can't reliably measure landing-page CRO during it.
- **Sample size > traffic capacity** — if calc shows N = 50K/arm but you have 8K/week, runtime is months. Increase MDE or pick a higher-baseline metric.

## Sources

- GrowthBook MCP intro: https://blog.growthbook.io/introducing-the-first-mcp-server-for-experimentation-and-feature-management/
- Microsoft Clarity (free): https://clarity.microsoft.com/
- Hotjar: https://www.hotjar.com/
- Maze (prototype testing): https://maze.co/
- VWO: https://vwo.com/
- Convert.com: https://www.convert.com/
- Statsig MCP (Knowledge Graph 2026): https://www.statsig.com/mcp
- Andrew Chen — CRO antipatterns: https://andrewchen.com/cro-pitfalls/
- Reforge — experimentation rigor: https://www.reforge.com/blog/the-experimentation-framework
