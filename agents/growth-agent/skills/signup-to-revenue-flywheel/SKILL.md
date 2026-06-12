<!--
Source: HubSpot flywheel framework + Reforge growth model + Brian Balfour 4-Fits
-->
# Signup-to-Revenue Flywheel SKILL

> Replace funnel-thinking with flywheel-thinking. Map current flywheel + velocity per stage + friction per stage. Identify 3 highest-leverage friction-reductions; ship experiments. Distinct from loop design — flywheel = whole-business; loop = specific compounding mechanism.

## When to use

Trigger phrases:
- "Map our flywheel"
- "Reduce friction in [stage]"
- "Velocity of growth motion"
- "Where are we losing momentum?"
- "Funnel vs flywheel"
- "HubSpot flywheel"

Pair: `growth-loop-design-5-types` (deeper loop view), `north-star-omtm-pirate-metrics-heart` (NSM at center), `growth-model-spreadsheet-compound-levers` (math), `plg-vs-sales-led-motion-decision` (motion fit).

## Setup

```bash
export POSTHOG_PERSONAL_API_KEY="phx_..."
export NOTION_TOKEN="ntn_..."
export POSTGRES_URL="postgresql://..."
```

## Funnel vs Flywheel mental model

```text
Funnel: linear, top-of-funnel-down, conversion-focused
  Visit → Signup → Activation → Trial → Paid → Churned (lost forever)

Flywheel: circular, energy-conserving, repeat
  Acquisition → Activation → Revenue → Expansion → Referral → back to Acquisition
  Each rotation reinforces the next; momentum compounds; friction is the enemy
```

Funnel: optimize step conversion. Flywheel: reduce friction; increase velocity per stage.

## Canonical 5-stage flywheel (HubSpot-style)

```text
                    Acquisition
                   /            \
              Referral        Activation
                 \              /
                  Expansion ← Revenue
```

Velocity per stage (the metric):

| Stage | Velocity definition | Friction examples |
|---|---|---|
| Acquisition | New signups / week | High CAC, slow channel ramp, low organic CTR |
| Activation | Time-to-activation; Activation rate | Long TTV, broken onboarding, unclear aha |
| Revenue | Trial-to-paid conversion time | Long trial, friction in upgrade flow, pricing confusion |
| Expansion | Time-to-first-expansion; expansion rate | No PQL signals, no AM handoff, no upgrade triggers |
| Referral | Time-to-first-referral; K coefficient | Hidden invite mechanic, no incentive, friction in share |

## Common recipes

### Recipe 1: Compute flywheel velocity per stage

```sql
-- 1. Acquisition velocity (new signups/week)
SELECT
  toStartOfWeek(timestamp) AS week,
  countDistinct(person_id) AS new_signups
FROM events WHERE event = 'User Signed Up'
GROUP BY week ORDER BY week DESC LIMIT 12

-- 2. Activation velocity (time signup → activation, p50)
SELECT
  quantile(0.5)(ttv_min) AS p50_min_to_activation
FROM (SELECT person_id, dateDiff('minute', signup_ts, activation_ts) AS ttv_min FROM ...)

-- 3. Revenue velocity (time activation → paid)
SELECT
  quantile(0.5)(dateDiff('day', activation_ts, paid_ts)) AS p50_days_to_paid
FROM cohort_with_paid_conversion

-- 4. Expansion velocity (time paid → first expansion)
SELECT
  quantile(0.5)(dateDiff('day', paid_ts, first_expansion_ts)) AS p50_days_to_expansion
FROM cohort_with_expansion

-- 5. Referral velocity (time signup → first referral)
SELECT
  quantile(0.5)(dateDiff('day', signup_ts, first_invite_sent_ts)) AS p50_days_to_first_invite
FROM cohort_with_invites
```

### Recipe 2: Friction audit per stage

For each stage, list current friction sources:

```text
Acquisition friction:
  ☐ Long page load times (target < 2s)
  ☐ Unclear value proposition
  ☐ Privacy / cookie modal blocking
  ☐ Form fields requested too early
  
Activation friction:
  ☐ Email verification required before app entry
  ☐ Multi-step onboarding (vs progressive)
  ☐ No defaults / templates
  ☐ Unclear next-action
  
Revenue friction:
  ☐ No PQL trigger for upgrade prompt
  ☐ Pricing page hidden / hard to find
  ☐ Multi-page checkout
  ☐ Coupon-required mindset
  
Expansion friction:
  ☐ No AM routing
  ☐ No usage-based trigger
  ☐ No cross-sell signals
  
Referral friction:
  ☐ Invite mechanic hidden in settings
  ☐ Generic invite copy
  ☐ Single share channel
  ☐ No incentive
```

### Recipe 3: Velocity benchmark table

| Motion | Acquisition (signup/wk per $1K spend) | Activation TTV p50 | Trial → paid (days p50) | Expansion (days p50) | K |
|---|---|---|---|---|---|
| Consumer mobile | 50+ | < 5 min | n/a (free) | n/a | 0.5-1.5 |
| B2B SaaS PLG | 5-25 | < 30 min | 14-30 | 90-180 | 0.1-0.4 |
| B2B SaaS enterprise | 1-5 | 1-7 days | 30-180 | 90-365 | 0.0-0.2 |
| DTC e-com | 10-50 | < 5 min (first purchase) | n/a | 30-90 (repeat) | 0.1-0.3 |

### Recipe 4: PIE-score friction-reductions

```python
# Per-stage friction × potential reduction velocity × ease-of-fix
frictions = [
    {"stage": "activation", "issue": "Email verify required",
     "potential_velocity_gain": 0.40, "ease": 8, "impact": 9},
    {"stage": "revenue", "issue": "No PQL trigger",
     "potential_velocity_gain": 0.30, "ease": 7, "impact": 8},
    {"stage": "referral", "issue": "Invite mechanic hidden",
     "potential_velocity_gain": 0.50, "ease": 8, "impact": 7},
    # ...
]
for f in frictions:
    f["score"] = f["potential_velocity_gain"] * f["ease"] * f["impact"]
frictions.sort(key=lambda x: x["score"], reverse=True)
```

Top 3 by score → first sprint.

### Recipe 5: Map flywheel rotations (compounding)

```text
Year 1 baseline (1 rotation per user lifecycle):
  1000 new signups → 320 activated → 58 paid → ?expansion → ?referrals back to acq

If K = 0.3:
  58 paid × ? referrals = 18 new users via referral
  → 1018 next-period signups (1.8% compounding)

If activation +10pp (320 → 420), trial→paid +5pp (18% → 23%):
  420 activated × 0.23 = 97 paid
  97 × K × referral_velocity → next-period acquisition lift
```

Compute compounding multi-quarter (use `growth-model-spreadsheet-compound-levers` skill).

### Recipe 6: Flywheel diagram in Notion (or imagegen-mcp)

```python
# Use imagegen-mcp to render the flywheel visually
prompt = """A clean flywheel diagram with 5 stages: Acquisition (top), 
Activation (top-right), Revenue (right), Expansion (bottom-right), 
Referral (bottom). Each connected by curved arrows. Annotations: 
velocity metric + bottleneck per stage. Modern minimal design."""

imagegen.create(prompt=prompt, output="flywheel_q3_2026.png")
```

### Recipe 7: Stage-owner mapping

```text
| Stage | Velocity metric | Owner | Co-owner | Sprint cadence |
|---|---|---|---|---|
| Acquisition | new_signups_per_week | Marketing | Growth | bi-weekly |
| Activation | p50_ttv | Product | Eng | weekly |
| Revenue | trial_to_paid_days | Growth | Sales | bi-weekly |
| Expansion | expansion_rate, NRR | CSM / Growth | Product | monthly |
| Referral | K | Growth | Product | bi-weekly |
```

### Recipe 8: Friction-reduction sprint template

```markdown
# Sprint: Reduce Activation Friction (Q3 wk 1-4)

## Current state
- Activation rate: 31%
- TTV p50: 4h 12m

## Friction sources identified
1. Email verify required before app entry (estimated -15pp activation)
2. No template (blank canvas problem)
3. Onboarding step 3 (data import) unclear

## Hypotheses
H1: Magic-link signup → activation +5pp (Recipe per signup-activation-conversion-optimization)
H2: 3 starter templates → TTV -50%
H3: Inline guidance for step 3 → step pct +20pp

## Experiments
1. Magic-link A/B (GrowthBook, 2400/arm, 14d)
2. Template auto-load (no test; full rollout — low-risk)
3. Step 3 guidance A/B (GrowthBook, 1500/arm, 14d)

## Success criteria
- Activation rate 31% → 38%+ in 8 weeks
- TTV p50 4h → < 2h
```

### Recipe 9: Cross-stage interaction tracking

Sometimes velocity at one stage hurts another:

```text
"Reduce activation friction by skipping verification"
  → +5pp activation rate
  → -20% verification rate (security risk)
  → +50% fake-signup rate
  
Net = ?

Guardrail metric per experiment must protect against cross-stage harm.
```

### Recipe 10: NSM at the center of the flywheel

```text
NSM ("Weekly active teams ≥ 3 seats") in center.
Each stage of flywheel = input to NSM.

Stage velocity improvements → NSM growth.

Each stage owner reports velocity weekly + impact on NSM.
```

### Recipe 11: 4-Fits flywheel check (Brian Balfour)

```text
Flywheel rotates faster when 4 Fits align:
  1. Market ↔ Product (solves real problem)
  2. Product ↔ Channel (matches channel format)
  3. Channel ↔ Model (CAC fits LTV)
  4. Model ↔ Market (price fits willingness-to-pay)

Audit flywheel quarterly against 4 Fits. If any broken → fix that before optimizing velocity.
```

## Examples

### Example 1: B2B SaaS PLG, "Why aren't we compounding?"

Audit (Recipe 1 + 2):
- Acquisition velocity: 240 signups/wk (steady)
- Activation: 28%, p50 TTV 3h (below benchmark)
- Revenue: trial-to-paid 12% (low); avg 22 days (slow)
- Expansion: 1.2% per month per active account
- Referral: K = 0.08 (very weak)

Constraint analysis: weakest stages are activation + referral. Trial-to-paid weak because few users reach aha.

Plan (Recipe 4 PIE):
1. Activation: magic-link + templates (sprint 1; Recipe 8)
2. Referral: surface invite mechanic + dual-sided reward (sprint 2)
3. Expansion: PQL triggers (sprint 3)

Expected: 6 months → activation 28% → 42%, K 0.08 → 0.25, NRR 102% → 115%.

### Example 2: DTC e-com "Funnel optimization plateaued"

Reframe: switch from funnel-optimization to flywheel-velocity.

New focus: increase repeat-purchase rate (Revenue stage velocity) — currently 24% → target 32%.

Lever: lifecycle email + loyalty program (hand off to `loyalty-program-yotpo-smile-loyaltylion`).

### Example 3: Early-stage startup

Skip flywheel until PMF (use `activation-funnel-aha-moment` instead).
Once PMF achieved → start flywheel mapping.

## Edge cases / gotchas

- **Flywheel = metaphor, not engine** — the math underneath is still loops + funnels. Don't let visualization replace measurement.
- **Single-stage focus blindness** — fixing acquisition while activation broken → wasted spend. Audit all 5 stages.
- **"Reduce friction" as cargo-cult** — friction-reduction without measurement is theater. Quantify before + after.
- **Cross-stage tradeoffs** — accelerating one stage may damage another. Always check guardrails.
- **Velocity ≠ outcome** — fast trial-to-paid that immediately churns isn't success. Measure post-conversion retention.
- **Owner conflict at stage boundaries** — who owns "activation → revenue"? Product or Growth? Define before sprint.
- **NSM disconnection** — if stage velocity improves but NSM doesn't, the metric chain is broken; investigate.
- **Flywheel for sales-led** — adapt: stages become Lead Gen → Sales-Qualified → Demo → Close → Expand → Refer. Same structure.
- **Pre-PMF flywheel theater** — flywheel mapping pre-PMF distracts from product-market-fit work.
- **4-Fits violation overlooked** — if Model ↔ Market is broken (overpriced), no flywheel speed-up will compound.

## Sources

- HubSpot flywheel framework: https://www.hubspot.com/flywheel
- Reforge growth model frameworks: https://www.reforge.com/
- Brian Balfour 4-Fits: https://brianbalfour.com/four-fits-growth-framework
- Andrew Chen — flywheel: https://andrewchen.com/
- Lenny Rachitsky — growth math: https://www.lennysnewsletter.com/
- Aakash Gupta — metrics: https://www.aakashg.com/metrics-for-product-managers/
- ProductLed PLG metrics: https://www.productled.org/foundations/product-led-growth-metrics
- ProductLed — flywheel adaptation: https://www.productled.org/
