<!--
Source: Reforge growth loops framework + Andrew Chen "The 5 Loops" + VoltAgent growth-loops doc
Use this skill when the user asks to design, classify, or constraint-analyze a growth loop.
-->
# Growth Loop Design — 5-Type Taxonomy SKILL

> Classify, diagram, and find the constraint in a product's growth loop using the canonical 5-type taxonomy (Reforge / Andrew Chen). Funnels leak — loops compound. This is the foundational skill for the agent's loop-centric worldview.

## When to use

Reach for this skill when the user says any of:
- "Design our growth loop" / "What's our loop?"
- "Why isn't [product] growing?" (likely no loop, or loop has a broken step)
- "Is our growth scalable?" (loops compound; channels don't)
- "Pick a growth motion" (paid vs viral vs content vs network vs sales-led)
- "Where should we invest engineering hours for growth?"

Pair with `viral-coefficient-k-measurement` (Loop type 1), `signup-to-revenue-flywheel` (whole-business view), `plg-vs-sales-led-motion-decision` (motion fit). Do NOT use this skill for funnel-only diagnosis — that's `signup-activation-conversion-optimization`.

## Setup

```bash
# No install — this is a thinking framework + analytics queries.
# Reference: load PostHog/Amplitude/Mixpanel MCPs to measure each step.
export POSTHOG_PERSONAL_API_KEY="phx_..."
export AMPLITUDE_OAUTH_TOKEN="amp_..."
export NOTION_TOKEN="ntn_..."   # for writing the loop diagram + spec
```

Required reading before recommending:
- `reference/SOTA_USE_CASES.md` rows 1-2 (loop classification + constraint).
- `role.md` "Growth loop playbook" section (Step 1-5).

## 5 canonical loop types

| # | Loop type | Output that brings new users | K-equivalent metric | Compounding signal | Best examples |
|---|---|---|---|---|---|
| 1 | **Viral / social** | Invitation, share, collaboration | `K = invites × acceptance` | K > 1 = exponential | Slack, Notion, Figma, WhatsApp |
| 2 | **Content / SEO** | UGC ranking on SERPs, public listings | Pages indexed × CTR × signup-conv | Pages compound | Pinterest, Quora, Glassdoor, Stack Overflow |
| 3 | **Paid acquisition** | Revenue funds more ads | `LTV:CAC > 3` AND `payback < 12mo` | LTV growing > CAC | DTC e-com, BeReal early, Hims |
| 4 | **Network effect (direct/indirect/data)** | Network value increases with users | Engagement per user grows with network N | Engagement curves up with N | Slack, Uber, OpenTable, Google |
| 5 | **Sales-led** | Revenue funds more sales hires | NRR × ACV × rep capacity | Rep payback < 18mo | Workday, ServiceNow, Salesforce |

Notes:
- A product may run multiple loops simultaneously (HubSpot = content + sales; Notion = viral + content).
- The dominant loop drives ≥ 60% of new users. Sub-loops amplify.

## Common recipes

### Recipe 1: 5-question discovery → classify the loop

Run this before any tactic recommendation.

```text
Q1: What does your product PRODUCE that could attract a new user?
   (artifacts / invites / public content / external touchpoints / revenue)
Q2: How does that output REACH non-users?
   (shared link, SERP rank, ad impression, network value increase, sales meeting)
Q3: What % of new users come from this output today?
   (if < 30%, you don't have a loop yet — you have a channel)
Q4: What is the metric per step? Where's the leak?
Q5: How long is one loop turn? (cycle time)
```

If Q1 = "an invite" → viral. If Q1 = "a public listing" → content/SEO. If Q1 = "more revenue funding ads" → paid. If Q1 = "more users = more value per user" → network. If Q1 = "revenue funds sales" → sales-led.

### Recipe 2: Map the loop diagram (5-step canonical)

```text
[Starting point: existing user]
        ↓ metric: WAU
[Action: produces output X]
        ↓ metric: output_creation_rate (e.g., invites_sent/user)
[Output: X reaches non-users]
        ↓ metric: reach (impressions, SERP rank, opens)
[New user touchpoint]
        ↓ metric: click-through / acceptance rate
[New user: signup → activation]
        ↓ metric: signup_conv × activation_rate
[Back to starting point — now they produce output X too]
```

Write the diagram into Notion via `notion-mcp` with metrics annotated per step. Use the `imagegen-mcp` skill to render a flywheel image for decks.

### Recipe 3: Find the constraint (weakest step = investment target)

```sql
-- PostHog HogQL — per-step conversion (viral loop example)
SELECT
  countDistinct(person_id) FILTER (WHERE event = 'user signed up') AS users,
  countDistinct(person_id) FILTER (WHERE event = 'invite sent') AS inviters,
  inviters * 1.0 / users AS invite_rate,
  countIf(event = 'invite sent') AS invites_sent,
  countIf(event = 'invite accepted') AS invites_accepted,
  invites_accepted * 1.0 / invites_sent AS acceptance_rate,
  countDistinct(person_id) FILTER (WHERE event = 'invitee signed up') AS new_users,
  new_users * 1.0 / invites_accepted AS post_acceptance_signup_rate
FROM events
WHERE timestamp >= now() - INTERVAL 30 DAY
```

Constraint diagnosis:
- `invite_rate` low (< 10%) → invite mechanism placement (pre-aha, friction, no incentive)
- `acceptance_rate` low (< 30%) → invite copy / landing page / sender clarity
- `post_acceptance_signup_rate` low (< 50%) → landing-page friction / signup form
- `activation_rate` low (< 25%) → onboarding broken → use `activation-funnel-aha-moment` skill

### Recipe 4: Loop type decision matrix (when to invest in which)

| If… | Then build… | Why |
|---|---|---|
| Output is shareable & multi-player | Viral loop | Each user = ~1 invite avg; K > 0.3 contributes meaningfully |
| Users create public content with search intent | Content/SEO loop | Pages compound; no per-marginal-page CAC |
| LTV:CAC > 3:1 + payback < 12mo | Paid loop | Sustainable; reinvest profits in CAC |
| Multi-sided + value(user_i) = f(N) | Network-effect loop | Engagement compounds with N; defensive moat |
| ACV > $25K + multi-stakeholder buy | Sales-led loop | Rep economics work; PLG won't fit |

### Recipe 5: Cycle time measurement (loop iteration length)

```sql
-- Cycle time = time from new-user-activated → producing-output
SELECT
  quantile(0.25)(cycle_hours) AS p25,
  quantile(0.5)(cycle_hours) AS p50,
  quantile(0.75)(cycle_hours) AS p75
FROM (
  SELECT
    person_id,
    dateDiff('hour',
      minIf(timestamp, event = 'activation_event'),
      minIf(timestamp, event = 'output_produced')
    ) AS cycle_hours
  FROM events
  WHERE event IN ('activation_event', 'output_produced')
  GROUP BY person_id
  HAVING cycle_hours > 0
)
```

Cycle time targets:
- Consumer viral: < 1 hour (TikTok, Snap)
- B2B SaaS viral: < 7 days (Notion, Slack)
- Content/SEO: weeks-to-months (each page takes time to rank)
- Paid: tied to attribution window
- Sales-led: 30-180 day enterprise sales cycle

### Recipe 6: Compound math — loop output projection

For a viral loop with K = 0.5, cycle time = 14 days, starting users = 1000:

```python
# Geometric series: total = N0 / (1 - K)  when K < 1
N0 = 1000
K = 0.5
cycles_per_year = 365 / 14  # ~26
# After many cycles: saturates at N0 / (1 - K) = 2000
total_at_saturation = N0 / (1 - K)
# K = 0.4 → 1667. K = 0.7 → 3333. K = 0.95 → 20000. K = 1.0 → infinite.

# For K > 1 (rare, true viral)
# users(t) = N0 * K**(t / cycle_time)  → exponential
```

Use this for stakeholder buy-in on which loop investment pays back fastest.

### Recipe 7: Multi-loop attribution — when product has 2+ active loops

```sql
-- PostHog — new users by first-touch source bucket
SELECT
  CASE
    WHEN properties.utm_source = 'invite' THEN 'viral_loop'
    WHEN properties.utm_medium = 'organic' THEN 'content_seo_loop'
    WHEN properties.utm_medium = 'paid' THEN 'paid_loop'
    WHEN properties.utm_source = 'partner' THEN 'partner_loop'
    ELSE 'unknown'
  END AS loop_type,
  countDistinct(person_id) AS new_users,
  countDistinct(person_id) * 100.0 /
    sum(countDistinct(person_id)) OVER () AS pct_of_total
FROM events
WHERE event = 'user signed up'
  AND timestamp >= now() - INTERVAL 90 DAY
GROUP BY loop_type
ORDER BY new_users DESC
```

If one loop > 60% → dominant; rest are amplifiers. If no loop > 40% → no loop has emerged; investigate why none compounds.

## Examples

### Example 1: B2B SaaS, "We're growing but want compounding"

**Discovery:** Q1=collaboration invites (multi-player tool). Q3=22% new users from invites. K=0.18.

**Diagnosis:** Viral loop weak but present. K=0.18 means 1 user produces 0.18 new users; need ~5x improvement for K > 1. Saturation projection at K=0.18 → cap at 1.22 × N₀.

**Constraint:** PostHog query shows `invite_rate` = 12% (very low). Users not aware they can invite. Acceptance rate fine at 47%.

**Plan:**
1. A/B move invite CTA from settings page → post-first-document-shared empty-state (via `growthbook-experiments`).
2. Add invite-to-unlock-feature gate (e.g., "Invite 1 teammate to enable shared workspace").
3. Measure K-weekly. Target K > 0.35 within Q2.
4. While viral matures, double down on content-SEO loop (currently 38% of new users).

### Example 2: DTC e-com, "Our CAC is rising"

**Discovery:** Q1 = revenue funds more Meta/TikTok ads. Q3=78% paid. LTV:CAC = 1.8:1 (worsening).

**Diagnosis:** Paid loop unsustainable. Need LTV:CAC ≥ 3:1.

**Constraint:** Either CAC rising (channel saturation) or LTV falling (retention / AOV).

**Plan:**
1. Run MMM via `attribution-last-multi-touch-mmm-meridian-robyn` skill — likely Meta saturation.
2. Build secondary loops: referral (`referral-program-referralcandy-friendbuy-growsurf`), loyalty (`loyalty-program-yotpo-smile-loyaltylion`), email-driven repeat.
3. Diagnose retention curve via `retention-curve-churn-diagnosis-j-smile` — if decay shape, fix LTV via repeat purchase.

## Edge cases / gotchas

- **K < 1 ≠ no loop** — K=0.3 still amplifies other loops (a +30% multiplier on retained users producing output). Don't kill sub-K=1 loops; just don't expect them to drive standalone growth.
- **"Loop" without measurement is theater** — every step must have an instrumented metric in PostHog/Amplitude/Mixpanel. If you can't measure it, the loop doesn't exist for ops purposes.
- **Channel ≠ loop** — Facebook Ads is a channel; "revenue funds more Facebook Ads" is a paid loop. Don't confuse these in stakeholder discussions.
- **Cycle time matters as much as K** — K=0.8 with 14-day cycle beats K=1.5 with 365-day cycle in any practical 2-year horizon. Compute both.
- **Content/SEO loop AEO/GEO risk (2025-2026)** — LLM answers reduce SERP CTR; UGC SEO loops (Quora, Stack Overflow style) degraded 15-40% across categories. Adjust assumptions; consider AEO via `seo-specialist` handoff.
- **Network-effect loop falsely claimed** — "we have network effects" is over-claimed. True test: plot avg engagement per user vs N. If flat or down, no network effect.
- **Paid loop death spiral** — When CAC rises 20%+ MoM and LTV stable, your paid loop is dying. Diversify before LTV:CAC drops below 1.

## Sources

- VoltAgent — "Growth Loops" (5 loop types reference): https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/08-business-product/growth-loops.md
- Reforge — "Growth Loops are the New Funnels" (Brian Balfour): https://www.reforge.com/blog/growth-loops
- Andrew Chen — "Growth's eternal question: What's your loop?": https://andrewchen.com/whats-your-growth-loop/
- ProductLed.org — PLG metrics + growth loops: https://www.productled.org/foundations/product-led-growth-metrics
- Lenny's PLG Handbook (loop section): https://plghandbook.com/
- Stackmatix PLG funnel metrics: https://www.stackmatix.com/blog/plg-funnel-metrics
- PostHog MCP: https://posthog.com/docs/model-context-protocol
