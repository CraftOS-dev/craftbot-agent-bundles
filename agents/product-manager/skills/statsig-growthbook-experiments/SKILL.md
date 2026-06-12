<!--
Statsig docs: https://docs.statsig.com
GrowthBook MCP: https://blog.growthbook.io/introducing-the-first-mcp-server-for-experimentation-and-feature-management
-->
# Statsig + GrowthBook Experiments — SKILL

Statsig (statsig.com) and GrowthBook (growthbook.io) cover the full A/B + multi-variant + sample-size + holdout + bandit + sequential-testing surface. This pack picks between them, pre-registers experiments, computes sample size, and reads results.

## When to use

- Designing an A/B test (hypothesis, MDE, sample size, duration).
- Running multi-variant (3+ arms) or holdout tests.
- Pre-registering an experiment with auto-stop on significance.
- Running a bandit allocation for fast learning.
- Pulling experiment results for ship/kill/iterate decisions.
- Switchback tests for marketplace/two-sided products.

Trigger phrases: "design an A/B test", "what sample size for X", "is the experiment significant yet", "ship or kill the experiment", "bandit test", "pre-register".

## Setup

### Statsig (Console + Server)

```bash
# Statsig console API for experiment management
curl -fsSL "https://statsigapi.net/console/v1/experiments" \
  -H "STATSIG-API-KEY: $STATSIG_CONSOLE_KEY"
```

Auth:
- `STATSIG_CONSOLE_KEY` — console API key from https://console.statsig.com/api_keys. Free tier supports 1M events/mo.

### GrowthBook (MCP)

```bash
# GrowthBook MCP — first-class experimentation MCP, 14 tools
npx -y growthbook-mcp@latest
```

Auth:
- `GROWTHBOOK_API_KEY` — from your GrowthBook instance Settings → API Keys. Open-source self-host = free.
- `GROWTHBOOK_API_HOST` — defaults to `https://api.growthbook.io` (cloud); self-host points to your URL.

### Which to pick

- **Statsig** if: you need holdouts + bandit + sequential testing + are okay with SaaS.
- **GrowthBook** if: you want open-source self-host, OR you already use feature flags via GrowthBook.
- **Both** work for vanilla A/B; default to whichever the team has.

## Common recipes

### Recipe 1: Sample size calculator (binary metric)

```python
import math

def sample_size_binary(baseline_rate, mde, alpha=0.05, power=0.8):
    """Per-arm sample size for a binary metric (e.g., conversion rate)."""
    from scipy.stats import norm
    z_alpha = norm.ppf(1 - alpha / 2)
    z_beta = norm.ppf(power)
    p1 = baseline_rate
    p2 = baseline_rate + mde   # absolute MDE
    p_bar = (p1 + p2) / 2
    numerator = (z_alpha * math.sqrt(2 * p_bar * (1 - p_bar)) +
                 z_beta * math.sqrt(p1*(1-p1) + p2*(1-p2)))**2
    denom = (p2 - p1)**2
    return math.ceil(numerator / denom)

# Example: 5% baseline conversion, want to detect +1% absolute lift
n = sample_size_binary(0.05, 0.01)
print(f"Need {n} per arm = {2*n} total")  # ~7,830 per arm
```

### Recipe 2: Quick formula (rough sanity check)

```
Binary metric:    n ≈ 16 × p × (1-p) / MDE²   (per arm, alpha 0.05, power 0.8)
Continuous:       n ≈ 16 × σ² / MDE²
```

```python
def quick_n_binary(p, mde): return int(16 * p * (1 - p) / mde**2)
print(quick_n_binary(0.05, 0.01))   # ~7,600 per arm — same ballpark as Recipe 1
```

### Recipe 3: Statsig — pre-register an experiment

```bash
curl -X POST "https://statsigapi.net/console/v1/experiments" \
  -H "STATSIG-API-KEY: $STATSIG_CONSOLE_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "onboarding_revamp_v1",
    "description": "Hypothesis: 3-step checklist lifts D7 retention 35% → 42%",
    "hypothesis": "If we replace freeform onboarding with a guided checklist, D7 retention rises by ≥5pp because friction-to-first-value drops.",
    "primaryMetric": "d7_retention",
    "secondaryMetrics": ["activation_step_2_done", "time_to_first_value"],
    "guardrailMetrics": ["error_rate","crash_rate"],
    "variants": [
      {"name":"control","size":0.5,"description":"current freeform onboarding"},
      {"name":"variant_a","size":0.5,"description":"3-step guided checklist"}
    ],
    "allocationSize": 1.0,
    "duration": 14,
    "minimumDetectableEffect": 0.05,
    "sequentialTesting": true,
    "autoStopOnSignificance": true
  }'
```

### Recipe 4: Statsig — start traffic + monitor

```bash
EXP_ID="<from Recipe 3>"
curl -X POST "https://statsigapi.net/console/v1/experiments/$EXP_ID/start" \
  -H "STATSIG-API-KEY: $STATSIG_CONSOLE_KEY"

# Poll results
curl -fsSL "https://statsigapi.net/console/v1/experiments/$EXP_ID/results" \
  -H "STATSIG-API-KEY: $STATSIG_CONSOLE_KEY" \
| jq '{primary: .primaryMetric, lift: .lift, pValue: .pValue, significant: .significant, sampleSize: .totalUsers}'
```

### Recipe 5: GrowthBook MCP — create experiment

```bash
mcp tool growthbook.create_experiment \
  --name "onboarding_revamp_v1" \
  --hypothesis "3-step checklist lifts D7 retention 35% → 42%" \
  --variations '[
    {"key":"control","name":"current","weight":0.5},
    {"key":"variant_a","name":"3-step checklist","weight":0.5}
  ]' \
  --goalMetrics '["d7_retention"]' \
  --guardrailMetrics '["error_rate"]' \
  --datasource "<datasource-id>"
```

### Recipe 6: GrowthBook — sample size endpoint

```bash
# Built-in calculator
mcp tool growthbook.calculate_sample_size \
  --baselineRate 0.05 \
  --minimumDetectableEffect 0.01 \
  --power 0.8 \
  --alpha 0.05
```

### Recipe 7: Bandit allocation (Statsig)

```bash
curl -X POST "https://statsigapi.net/console/v1/experiments" \
  -H "STATSIG-API-KEY: $STATSIG_CONSOLE_KEY" \
  -d '{
    "name":"cta_copy_bandit",
    "type":"bandit",
    "primaryMetric":"signup_clicked",
    "variants":[
      {"name":"control","description":"Get started"},
      {"name":"v1","description":"Try free for 14 days"},
      {"name":"v2","description":"See it in action"},
      {"name":"v3","description":"Join 10,000+ founders"}
    ],
    "banditAlgorithm":"thompson_sampling",
    "explorationRate":0.1
  }'
```

### Recipe 8: Holdout cohort (long-term effect measurement)

```bash
# 10% holdout — never sees the new experience; measures cumulative long-term effect
curl -X POST "https://statsigapi.net/console/v1/holdouts" \
  -H "STATSIG-API-KEY: $STATSIG_CONSOLE_KEY" \
  -d '{
    "name":"q3_holdout",
    "size":0.1,
    "experiments":["onboarding_revamp_v1","new_navigation","checkout_v2"]
  }'
```

### Recipe 9: Pre-experiment doc (the agent always generates this)

```markdown
# Experiment: onboarding_revamp_v1

**ID:** statsig-exp-1234 · **Owner:** [PM] · **Status:** Pre-registered

## Hypothesis
If we replace the freeform onboarding with a 3-step guided checklist, then D7 retention will rise from 35% to 40-42% because the documented blocker is friction-to-first-value.

## Metrics
- **Primary:** d7_retention (Amplitude funnel — see /charts/abc)
- **Secondary:** activation_step_2_done, time_to_first_value (median)
- **Guardrail:** error_rate (must not increase), crash_rate (must not increase)

## Population
- Included: new sign-ups in last 24 hours
- Excluded: internal users, paid customers

## Variants
- **Control (50%):** current freeform onboarding
- **Variant A (50%):** 3-step guided checklist

## Sample size
- Baseline: 35%
- MDE: +5pp absolute
- Sample size per arm: ~6,200 (Recipe 1)
- Daily traffic: ~800
- Expected duration: 14-16 days

## Kill criteria
- Auto-stop on primary significance: YES
- Guardrail breach threshold: error_rate +0.5%
- Hard kill: 28 days (memorial budget)

## Pre-registration timestamp
2026-06-09 14:00 UTC — locked in Statsig
```

### Recipe 10: Readout decision (ship / kill / iterate)

```python
def decide(result):
    pri = result["primaryLift"]
    pv = result["primaryPValue"]
    gr_breach = any(r["delta"] > r["threshold"] for r in result["guardrails"])

    if gr_breach:
        return "KILL — guardrail breached"
    if pv < 0.05 and pri > 0:
        return f"SHIP — +{pri:.1%} lift (p={pv:.3f})"
    if pv < 0.05 and pri < 0:
        return f"KILL — primary degraded {pri:.1%} (p={pv:.3f})"
    if pv > 0.10 and result["sampleSize"] > result["targetSize"] * 1.5:
        return "KILL — null result, sample exhausted"
    return "CONTINUE — not yet significant"
```

## Examples

### Example 1: From hypothesis to pre-registered experiment
**Goal:** Stand up a clean A/B test for the onboarding revamp.

**Steps:**
1. Run sample size calc (Recipe 1 or 2 or 6).
2. Write pre-experiment doc (Recipe 9) in Notion.
3. Create experiment (Recipe 3 for Statsig or Recipe 5 for GrowthBook).
4. Start traffic (Recipe 4).
5. Monitor weekly until auto-stop OR hard kill date.

**Result:** A pre-registered experiment with documented hypothesis, MDE, sample size, kill criteria — defensible at the readout.

### Example 2: Readout and decision
**Goal:** Decide ship/kill at experiment conclusion.

**Steps:**
1. Pull results (Recipe 4 or `growthbook.get_experiment_results`).
2. Apply decision logic (Recipe 10).
3. Write readout to the experiment doc (Recipe 9 fills "Readout" section).
4. If SHIP: ramp traffic to 100% via feature flag, follow `release-notes-changelog-automation` for the customer comms.
5. If KILL: archive variant code; document learnings in Notion research repo.

**Result:** Audit-trailed decision; the team learns whether the hypothesis held.

## Edge cases / gotchas

- **Peeking.** Without sequential testing enabled, mid-experiment peeking inflates false positives. Enable sequential testing OR commit to wait-until-end.
- **MDE must be absolute, not relative.** "5pp lift" is absolute; "5% relative lift" is much smaller. Sample size formulas use absolute MDE.
- **Confounded variants.** A/B test with multiple changes confounds — you can't tell which change drove the lift. Test one thing at a time OR use factorial design.
- **Novelty effect.** First week often shows inflated lift from novelty; treat short experiments skeptically.
- **Self-selection bias.** Don't filter by behavior post-randomization (e.g., "users who clicked the variant"). Always analyze by assignment.
- **Sequential testing tradeoffs.** Statsig's "always-valid" inference + GrowthBook's CUPED both reduce required sample size; they're worth turning on for low-traffic surfaces.
- **Holdouts cost reach.** A 10% holdout means 10% of users never get any new features — useful for long-term measurement but politically tricky.
- **Bandit assumes stationarity.** Bandit underperforms if metric varies by time (e.g., weekday/weekend); use scheduled bandits or switchback.
- **Guardrails are non-optional.** Always include error_rate / crash_rate / latency as guardrails — a "ship" on primary that breaks guardrails is a kill.
- **Sample-size for revenue metrics is HUGE.** Revenue per visitor has high variance; expect 10x the sample size of a binary metric. Consider switching to conversion + AOV separately.

## Sources

- [Statsig API + experiment docs](https://docs.statsig.com)
- [Statsig sequential testing](https://docs.statsig.com/experiments-plus/sequential-testing)
- [GrowthBook MCP announcement](https://blog.growthbook.io/introducing-the-first-mcp-server-for-experimentation-and-feature-management)
- [GrowthBook docs](https://docs.growthbook.io)
- [Sample size formulas — Evan Miller](https://www.evanmiller.org/ab-testing/sample-size.html)
- [CUPED variance reduction (Microsoft Research)](https://www.microsoft.com/en-us/research/group/experimentation-platform-exp/articles/improving-the-sensitivity-of-online-controlled-experiments-by-utilizing-pre-experiment-data)
- [Pre-registration in industry — Ron Kohavi](https://www.kdd.org/exploration_files/19-1-Article6.pdf)
