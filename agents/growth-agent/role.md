# Growth Agent — deep reference

This appends to `AGENT.md`. **Not** in the agent's default context. Grep when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "Growth loop playbook", "Activation funnel playbook", "Retention curve playbook", "Churn prediction playbook", "Time-to-value playbook", "Experimentation playbook", "PQL framework", "Attribution playbook", "Growth model spreadsheet", "North Star metric framework", "AARRR Pirate Metrics", "HEART framework", "PLG vs sales-led decision", "Cohort design", "CDP setup", "Reverse ETL", "Antipattern catalog", "Onboarding tool decision matrix", "Referral platform decision matrix", "In-app messaging tool decision matrix", "SOTA tool reference".

For provenance, see `SOURCES.md`. For per-use-case SOTA mapping + fulfillment math, see `reference/SOTA_USE_CASES.md`.

---

## Capability reference

### Growth motions covered
- **PLG (Product-Led Growth)** — self-serve signup, in-product activation, free→paid conversion, viral mechanics
- **Sales-led** — outbound + ABM (defer to `sales-agent` for execution; growth-agent covers PQL handoff)
- **Hybrid** — PLG-driven PQL → sales-assist for enterprise tier
- **Community-led** — content/SEO loop + Discord/Slack community + champion program
- **Content/SEO loop** — content begets traffic begets users begets content
- **Network-effect** — direct (more users = more value), indirect (two-sided), data (more users = better product)

### Metrics framework hierarchy
- **North Star Metric (NSM)** — single value-representing metric; predicts revenue
- **Input metrics** — 3-5 levers that move NSM (e.g., NSM = "weekly active users", inputs = activation rate, retention, K)
- **OMTM (One Metric That Matters)** — quarter-specific focus metric
- **AARRR (Pirate Metrics)** — Acquisition / Activation / Retention / Revenue / Referral
- **HEART (Google)** — Happiness / Engagement / Adoption / Retention / Task success
- **4-Fits (Brian Balfour)** — market-product / product-channel / channel-model / model-market

### Loop types (5 canonical)
1. **Viral / social** — invitation, creation, collaboration, social-proof
2. **Content / SEO** — user-generated content ranks, attracts new users
3. **Paid acquisition** — revenue funds more paid acquisition (sustainable when LTV:CAC > 3, payback < 12mo)
4. **Network-effect** — direct (Slack, WhatsApp), indirect (Uber, Airbnb), data (Google, Netflix)
5. **Sales-led** — revenue funds sales team that generates more revenue

### Retention curve shapes (4 canonical)
- **Smile** — retention drops, then climbs (rare — strong PMF + re-engagement loop)
- **J-curve** — retention drops, then asymptotes flat at >0 (PMF achieved)
- **Decay** — retention approaches 0 (pre-PMF or onboarding broken)
- **Flat-after-drop** — retention drops fast, then flat (expansion opportunity in surviving cohort)

### Activation framework
- **Aha moment** — emotional/qualitative; the felt-value instant
- **Activation event** — behavioral/quantitative; the measurable proxy (e.g., "3 documents shared")
- **Sean-Ellis Test** — survey: "How would you feel if you couldn't use [product]?" 40%+ "very disappointed" = PMF signal
- **TTV (time-to-value)** — signup → first value event; best-in-class < 5 min
- **Activation rate** — % cohort reaching activation in 7-14 days; B2B SaaS avg 37.5%, best-in-class 60%+

### Experimentation taxonomy
- **A/B test** — 1 control + 1 treatment, single primary metric
- **Multivariate (MVT)** — multiple variants, factorial; needs larger N
- **Holdout** — permanent X% holdout for long-term effect measurement
- **Switchback** — time-based randomization (when geo or user-level randomization impossible)
- **Bandits** — adaptive allocation; explore-exploit tradeoff

### PQL signal types
- **Limit proximity** — approaching free-tier cap (80-90% usage)
- **Feature depth** — interaction with premium features
- **Team activity** — multiple users from same account engaging
- **Frequency** — consistent return visits indicating habit formation
- **Engagement depth** — completing key activation milestones

### Attribution taxonomy
- **Last-touch** — credit to last interaction (baseline, biased to bottom-funnel)
- **First-touch** — credit to first interaction (biased to top-funnel)
- **Linear** — equal credit across all touches
- **Time-decay** — recent touches weighted more
- **U-shape / Position-based** — first + last weighted, middle distributed
- **Data-driven (GA4)** — algorithmic, model-fit per conversion path
- **Multi-touch (MTA)** — per-user journey reconstruction; B2B via Dreamdata / HockeyStack
- **Marketing Mix Modeling (MMM)** — aggregate spend → outcome regression; privacy-durable

---

## Growth loop playbook

### Step 1: Identify the output
What does the product produce that could bring in new users?
- Shared artifacts (designs, dashboards, reports, public profiles)
- Invitations (collaborate, view, comment, edit)
- Public content (UGC, published work, listings)
- External touchpoints (emails sent via product, links shared, embeds)

### Step 2: Classify against 5 types
- Output = invite → **viral loop**
- Output = SEO-ranking content → **content/SEO loop**
- Output = revenue funding more ads → **paid loop**
- Output = network value increase → **network-effect loop**
- Output = revenue funding sales → **sales-led loop**

### Step 3: Map the loop with metric per step
```
[Starting point] → [Action] → [Output] → [New user touchpoint] → [New user] → back to [Starting point]
       ↓             ↓           ↓                ↓                    ↓
    metric1       metric2     metric3          metric4              metric5
```

### Step 4: Find the constraint
The weakest step is the investment target.
- Low K → improve invite mechanism
- Low conversion on output → improve landing/first-experience
- Low activation of new users → improve onboarding
- High cycle time → speed up loop iteration

### Step 5: Measure loop efficiency

| Metric | Measures | Target |
|---|---|---|
| K (viral coefficient) | Users generated per existing user | K > 1 viral; K > 0.3 contributing |
| Cycle time | How long one loop turn takes | Days for SaaS, minutes for consumer |
| Conversion per step | Where the loop leaks | Step-specific |
| LTV:CAC (paid loop) | Loop sustainability | > 3:1 |
| Payback period (paid loop) | When loop pays back | < 12 months |

### Loop deliverable format
- Loop type classified (5-type taxonomy)
- Loop diagram with metric annotation per step
- Constraint analysis (weakest step + why)
- 2-3 ranked experiments with hypothesis + sample size + MDE + primary/secondary metric + kill criteria

---

## Activation funnel playbook

### Step 1: Find activation event candidates
Cohort-diff: behaviors of Day-30 retained users vs Day-30 churned users.

```sql
-- PostHog HogQL example
SELECT
  event,
  countIf(retained_day_30=1) as retained_did,
  countIf(retained_day_30=0) as churned_did,
  retained_did / churned_did as lift
FROM cohort_events
GROUP BY event
ORDER BY lift DESC
LIMIT 10
```

Top events with highest retained:churned lift = candidate activation events.

### Step 2: Validate via Sean Ellis Test

Survey: "How would you feel if you could no longer use [product]?"
- Very disappointed
- Somewhat disappointed
- Not disappointed
- N/A — no longer using

Score: % "very disappointed" ≥ 40% → PMF signal. Run only on users who have used the product 2+ times in last 2 weeks.

### Step 3: Measure activation rate

Activation rate = (cohort N who hit activation in 7-14 days) / cohort N.

Benchmarks:
- B2B SaaS average: 37.5%
- B2B SaaS best-in-class: 60%+
- Consumer apps: highly variable; aim for top decile in category

### Step 4: Reduce TTV

TTV = signup → activation event time (median + p25 + p75).
- Best-in-class: < 5 min self-serve
- Complex products: < 24h
- Enterprise setup: < 7 days

Reduction tactics:
- Skip-able onboarding
- Template / starter content
- AI-assisted setup (claude-powered)
- Passwordless / SSO / magic-link signup
- Pre-aha checklist with progress indicator

### Activation deliverable format
- Activation event spec (event name + property filters)
- Validation method (Sean Ellis 40%+ OR cohort-diff statistical significance)
- Current rate + benchmark
- TTV p25/p50/p75
- 2-3 reduction experiments with predicted lift

---

## Retention curve playbook

### Plotting the curve
Day 0 (signup) / Day 1 / Day 7 / Day 30 / Day 90 / Day 180.
Use cohorted (by acquisition week) — never aggregate.

### Shape interpretation

**Smile curve**
- Retention drops Day 0→7, then climbs Day 30→90
- Diagnosis: exceptional PMF + working re-engagement loop
- Action: amplify what's working; don't fix what's not broken
- Examples: Slack, Pinterest

**J-curve (asymptote >0)**
- Retention drops fast, then flattens at sustainable level (e.g., 25%)
- Diagnosis: PMF achieved for a segment
- Action: identify the surviving cohort; build for them
- Examples: Most healthy SaaS

**Decay**
- Retention approaches 0 — no asymptote
- Diagnosis: activation problem OR pre-PMF
- Action: fix activation first; expansion tactics will fail
- Common for: products without aha moment, products with onboarding broken

**Flat-after-drop**
- Retention drops fast, then flat
- Diagnosis: small loyal cohort; expansion opportunity
- Action: NRR expansion (cross-sell, upsell) on surviving cohort
- Common for: prosumer / power-user products

### Cohort slicing
Always slice retention by:
- Acquisition channel
- Acquisition cohort week
- Persona / ICP segment
- Plan tier
- Feature adoption (activated vs not)

---

## Churn prediction playbook

### Survival analysis with lifelines
```python
from lifelines import CoxPHFitter, KaplanMeierFitter, AcceleratedFailureTimeFitter

# Cohort + features + churn event
df = load_cohort_data()  # cols: tenure_days, churned, feature_1..N

# Cox PH (proportional hazards)
cph = CoxPHFitter()
cph.fit(df, duration_col='tenure_days', event_col='churned')
cph.print_summary()

# Output: hazard ratios per feature; print > 1.0 = increases churn risk
# Output: time-to-churn curves per segment
```

### LLM signal augmentation (2026 SOTA)
For each at-risk user:
1. Extract sentiment from support tickets (Claude)
2. Extract intent signals from NPS comments (Claude)
3. Extract call transcript red flags (Claude on Otter / Gong / Fathom)
4. Feed as binary/categorical features into survival model

### At-risk cohort handoff
- Predicted churn-within-30-days → trigger win-back sequence (Customer.io / Klaviyo)
- Predicted churn-within-90-days → trigger CSM check-in (HubSpot ticket via curl)
- Predicted churn-within-12-months → flag for product team (root-cause review)

### Churn diagnostic decision tree
- Retention curve = decay → activation problem (don't predict, fix activation)
- Retention curve = J + churn within 90 days → expansion opportunity (win-back works)
- Retention curve = J + churn within 12 months → product fit decline (root-cause review)

---

## Time-to-value playbook

### TTV measurement (PostHog HogQL)
```sql
SELECT
  quantile(0.25)(time_to_value_minutes) as p25,
  quantile(0.5)(time_to_value_minutes) as p50,
  quantile(0.75)(time_to_value_minutes) as p75
FROM (
  SELECT
    person_id,
    dateDiff('minute', signup_time, value_event_time) as time_to_value_minutes
  FROM events
)
```

### TTV reduction tactics (ranked by typical impact)
1. **Skip-able onboarding** — let power users skip; novice users see full
2. **Pre-populated templates** — no blank-canvas problem
3. **AI-assisted setup** — Claude generates initial config from user goal
4. **Magic-link signup** — remove password friction
5. **SSO** — remove signup friction for B2B
6. **Checklist + progress** — surface next-best step
7. **In-app tour** — only for genuinely-complex flows; can hurt TTV if overdone
8. **Defaults that ship value** — preset values that demonstrate aha

### TTV benchmarks (Userpilot 2024 baseline across 547 SaaS)
- Median TTV across all: ~1 day 12 hours
- AI/ML products: hours
- HR products: days
- Best-in-class: < 5 min

---

## Experimentation playbook

### Experiment brief template
```markdown
# Experiment: [Name]

## Hypothesis
If we [change], then [metric] will [direction] by [magnitude] because [mechanism].

## Variants
- Control: [current]
- Treatment A: [variant]
- Treatment B: [optional]

## Audience
- Inclusion: [cohort definition]
- Exclusion: [exclusions]
- Allocation: [50/50 or 33/33/33]

## Sample size + MDE
- Sample size required: [N per arm] (calc via GrowthBook or Statsig)
- Minimum detectable effect: [%]
- Power: 80%
- Significance level: 95% (α=0.05)

## Metrics
- Primary: [metric] (NOT a downstream proxy)
- Secondary: [metric 1, metric 2] (≤ 2)
- Guardrail: [metric that must NOT degrade]

## Kill criteria
- Primary metric drops > [X%] at p < 0.01 → kill immediately
- Guardrail drops > [Y%] → kill immediately
- Inconclusive after [N weeks] → kill

## Monitoring
- Cadence: [daily / weekly]
- Auto-stop: GrowthBook / Statsig configured
- Owner: [name]

## Expected duration
- [N weeks based on sample-size + traffic]
```

### Experiment quality bar
- Sample size pre-calc (not "let's see")
- MDE explicit (what's the smallest worth-detecting effect?)
- One primary metric (multiple = multiple-comparisons inflation)
- ≤ 2 secondary metrics
- Kill criteria explicit
- Statistical significance auto-stop on negative significance (`p < 0.01`)

### Statistical-rigor gotchas
- **Peeking** — checking results mid-experiment inflates false-positive rate; auto-stop only via Bayesian or sequential methods
- **Multiple comparisons** — N metrics × α=0.05 → at least 1 will hit significance by chance; Bonferroni-correct
- **Novelty effect** — new variants get lift in week 1, regress by week 4; run experiments ≥ 2 full business cycles
- **Sample ratio mismatch** — if traffic split isn't 50/50 (or whatever specified), randomization is broken; check via χ²
- **Survivorship bias** — measuring only "users who stayed" hides activation problem

---

## PQL framework

### PQL signal scoring (multi-signal — never single-signal)

```
PQL Score = w1 × LimitProximity + w2 × FeatureDepth + w3 × TeamActivity + w4 × Frequency

Where:
- LimitProximity: 0-100, % of free-tier usage cap consumed
- FeatureDepth: count of distinct premium-feature interactions in last 30d
- TeamActivity: count of distinct users from account active in last 7d
- Frequency: distinct active days in last 30d / 30

Weights tuned via Cox PH on past PQL→closed-won data
```

### PQL→pipeline handoff workflow
1. Score user via PostHog HogQL cron (hourly or daily)
2. Write score back to user profile (PostHog `identify` or Segment `Identify`)
3. Threshold check (typically 70+ / 100)
4. CRM action: create opportunity in HubSpot/Salesforce via curl
5. Slack alert via `slack-mcp` to assigned AE
6. Track conversion: PQL created → opportunity opened → closed-won

### Pocus / Koala / HockeyStack alternatives
- **Pocus** — full PQL platform, deep CRM sync, Slack/Teams alerts, opportunity routing
- **Koala** — intent signals + visitor ID; lighter touch, faster to set up
- **HockeyStack** — full B2B revenue platform; PQL + multi-touch attribution

---

## Attribution playbook

### When to use which method

| Method | Use when | Limitations |
|---|---|---|
| Last-touch | Quick tactical view | Biased to bottom-funnel |
| First-touch | Awareness measurement | Biased to top-funnel |
| Data-driven (GA4) | Default tactical | Cookieless decay |
| Multi-touch (MTA) | B2B, user-level journeys | Requires identity stitching |
| MMM | Strategic budget allocation | Slow refresh (quarterly), aggregate |
| Lift tests | Validation of MMM/MTA | Expensive, limited per quarter |

### Recommended attribution stack (2026 SOTA)

1. **Tactical**: GA4 data-driven (free, fast)
2. **B2B journey**: HockeyStack OR Dreamdata (multi-touch, account-level)
3. **DTC e-com**: Triple Whale OR Northbeam (Triple Whale stronger for Shopify)
4. **Strategic**: Robyn (Meta OSS) OR Meridian (Google OSS, May 2026 GeoX) OR PyMC-Marketing
5. **Validation**: Quarterly lift tests (geo-incrementality via Meridian GeoX, paid platform lift studies)

### MMM workflow (Robyn / Meridian)

```bash
# Robyn (Meta OSS)
cli-anything install: pip install robyn
input: 2+ years weekly spend per channel + revenue + control vars
output: response curves per channel + budget allocation recommendation

# Meridian (Google OSS, May 2026 GeoX)
git clone https://github.com/google/meridian
input: same as Robyn, optionally geo-level data for GeoX
output: response curves + GeoX geo-incrementality estimate
```

### Reallocation rule
Only reallocate budget when:
1. MMM and MTA agree on direction
2. Reallocation > MDE (typically 10%+ shift)
3. Lift test scheduled to validate within next quarter

---

## Growth model spreadsheet

### Sequoia / Reforge model structure

```
Inputs (per quarter)
- New visitors
- Visit → signup conversion %
- Signup → activation %
- Activation → paid %
- ARPU
- Monthly churn %
- NRR

Calculations
- New paid customers per quarter
- Total customers (with churn)
- MRR (with NRR)
- LTV (1 / churn × ARPU)
- CAC (paid spend / new paid)
- LTV:CAC ratio
- CAC payback (months)
- Cohort MRR retention (by acquisition cohort)

Outputs (3 scenarios)
- Base: current actuals projected
- Upside: improve activation 10pp + reduce churn 1pp
- Downside: churn +2pp + conversion -5pp

Sensitivity per lever (1pp lever change → output delta)
- Activation rate
- Trial → paid conversion
- NRR
- Churn
- ARPU
```

### Update cadence
- Actuals: monthly (auto-populate from PostHog / postgres / Klaviyo)
- Scenarios: quarterly
- Major refactor: annually or when motion changes (PLG ↔ sales-led)

---

## North Star metric framework

### Choosing an NSM
Criteria:
- **Measurable** — daily/weekly trackable
- **Value-aligned** — moves when users get value
- **Lead-indicator** — predicts revenue (lags revenue by ≤ quarter)
- **Single number** — one metric, not a basket

### NSM examples by motion
- **Consumer social**: weekly active users
- **B2B SaaS PLG**: weekly active teams with ≥ N seats
- **Marketplace**: monthly transactions
- **DTC e-com**: monthly orders or LTV-weighted active customers
- **Media**: weekly minutes consumed

### Validation: NSM lifts → revenue lifts
Run correlation analysis (PostHog HogQL or Amplitude):
- Plot NSM weekly vs MRR weekly
- Correlation > 0.8 → strong NSM
- Correlation < 0.6 → NSM is a vanity metric; pick another

### Input metrics (3-5 levers per NSM)
For "weekly active teams":
- Activation rate (lever 1)
- 7-day retention (lever 2)
- Team-size growth rate (lever 3)
- Re-engagement of dormant (lever 4)

Each lever has an owner + experiment roadmap.

---

## AARRR Pirate Metrics

| Stage | Metric | Tool |
|---|---|---|
| Acquisition | New visitors / week | GA4, PostHog `web_analytics` |
| Activation | Activation rate (7d) | PostHog cohort, Amplitude funnel |
| Retention | Day 7 / 30 / 90 retention | PostHog `retention`, Amplitude `retention` |
| Revenue | MRR, ARPU, NRR | Stripe / Klaviyo / postgres |
| Referral | K (viral coefficient) | PostHog HogQL invite query |

Use AARRR when: simple full-funnel view, early-stage growth team, alignment across functions.

---

## HEART framework (Google)

| Dimension | Metric | Use |
|---|---|---|
| Happiness | NPS, CSAT, satisfaction surveys | UX quality |
| Engagement | DAU/MAU, session duration, depth | Product stickiness |
| Adoption | Feature adoption % | New-feature launch |
| Retention | 30-day retention | Product health |
| Task success | Funnel completion, error rate | Specific user task |

Use HEART when: feature-launch design, UX research focus, granular tracking.

---

## PLG vs sales-led decision

### Decision matrix

| Factor | PLG | Sales-led | Hybrid |
|---|---|---|---|
| ACV | < $5K | > $25K | $5-25K |
| Buyer count | 1-3 | 5+ stakeholders | 2-5 |
| Setup complexity | Self-serve | Implementation services | Mixed |
| Time-to-aha | < 1h | Days/weeks | Hours |
| Distribution | Mass-market / wide | Targeted ICP | Mid-market |
| Network effects | Strong | Weak | Mixed |

### Hybrid signal patterns
- PLG signup → individual user activates → team grows → PQL fires → sales-assist for enterprise upgrade
- Sales-led demo → trial → in-product activation → expansion (sales-assist for procurement)

### Brian Balfour 4-Fits
1. **Market ↔ Product** — does product solve the market's problem?
2. **Product ↔ Channel** — does product fit the channel's content/format/intent?
3. **Channel ↔ Model** — does channel CAC fit the model's LTV?
4. **Model ↔ Market** — does pricing/packaging fit the market's willingness-to-pay?

Most PLG transitions fail (85%) because one of these 4 fits is broken.

---

## Cohort design

### Multi-attribute cohort definition (mandatory)
- "Users from organic search" — too broad
- "Users from organic search + signed up Q1 + Pro plan" — actionable

### Dynamic vs static cohorts
- **Static** — set at point-in-time (e.g., "signups week of Mar 6, 2026")
- **Dynamic** — re-evaluated continuously (e.g., "users active in last 7 days")

### Cohort sync (activation to downstream tools)
- Behavioral cohort defined in PostHog/Amplitude/Mixpanel
- Synced to ESP (Klaviyo/Customer.io) via reverse-ETL (Hightouch/Census)
- Used as audience for in-app message (Intercom/Userpilot)
- Used as targeting for paid ads (Facebook Custom Audiences via Hightouch)

---

## CDP setup

### Platform choice
- **Segment** — default; 20K+ customers, 350+ integrations
- **RudderStack** — OSS, 50-80% cost savings, warehouse-native
- **mParticle** — mobile-first
- **Hightouch CDP** — composable, warehouse-native (no separate data store)
- **Tealium** — 1,300+ integrations (largest), enterprise

### Event taxonomy (Object-Action past-tense)
- "Subscription Started" — not "subscribe" or "subscription"
- "Document Created" — not "create_document"
- "Team Member Invited" — not "invite_member"

### Tracking plan structure (document in Notion via `notion-mcp`)
```
| Event | When | Properties | Source | Status |
|-------|------|------------|--------|--------|
| Signup Completed | After verify | email, plan, source | Web | Live |
| Document Created | On save | document_id, type, team_id | Web, Mobile | Live |
```

---

## Reverse ETL

### Use cases
- **Audience activation** — warehouse cohort → Klaviyo email audience
- **Ad-platform custom audiences** — warehouse cohort → Facebook / Google Custom Audiences
- **CRM enrichment** — warehouse user attributes → HubSpot / Salesforce contacts
- **In-product personalization** — warehouse cohort → in-app message audience (Intercom / Userpilot)

### Platform choice
- **Hightouch** — Gartner MQ Leader; $1.2B valuation; deepest destination catalog
- **Census** — acquired by Fivetran May 2025; now part of unified data movement
- **Polytomic** — strong for embedded use cases
- **RudderStack Reverse ETL** — bundled with RudderStack CDP

### Activation pattern
```sql
-- In warehouse (BigQuery/Snowflake/Redshift)
SELECT
  user_id,
  email,
  CASE WHEN pql_score > 70 THEN 'high' ELSE 'low' END as pql_tier
FROM analytics.user_features
WHERE last_active_at > current_date - 7
```
Sync via Hightouch model → Klaviyo "PQL High" list → triggered email flow.

---

## Onboarding tool decision matrix

| Tool | Web | Mobile | Analytics | Pricing | Best for |
|---|---|---|---|---|---|
| Pendo | ✓ | ✓ (SDKs) | Best-in-class | $15K-140K/yr | Unified analytics + guidance + replay |
| Userpilot | ✓ | ✓ | Funnels + cohorts built-in | $249/mo+ | Mid-market mid-budget |
| Appcues | ✓ | ✓ (iOS/Android) | Basic | $299/mo+ | Mobile-native focus |
| Chameleon | ✓ | ✗ web-only | External (Amplitude/Mixpanel) | Custom | Pixel-perfect web design |
| Whatfix | ✓ | ✓ | Enterprise DAP | Enterprise | Internal apps + complex enterprise |
| Userflow | ✓ | ✗ | Basic | Mid-market | Dev-friendly setup |

---

## In-app messaging tool decision matrix

| Tool | PLG product tours | In-app chat | Fin AI agent | Best for |
|---|---|---|---|---|
| Intercom | ✓ best-in-class | ✓ | ✓ Fin (50-70% inbound auto-resolve) | PLG + B2B SaaS |
| Customer.io | ✗ | ✓ | Limited | Logic-heavy event-triggered journeys |
| Pendo Resource Center | ✓ | ✗ | ✗ | Pendo customer using guidance + analytics |
| Userpilot | ✓ | ✗ | ✗ | Userpilot customer |
| 1mind (Drift successor March 2026) | ✓ | ✓ | ✓ | Drift refugees |

---

## Referral platform decision matrix

| Tool | E-com | SaaS | Pricing | Integrations |
|---|---|---|---|---|
| ReferralCandy | ✓ best-in-class | ✗ | $39-799/mo + 0.25-10.5% commission | Shopify, Klaviyo |
| GrowSurf | ✗ | ✓ best-in-class | $0-custom (participant-based) | Webhooks, Stripe |
| Friendbuy | ✓ | ✓ | Enterprise revenue-tier, 12-mo contracts | Klaviyo, HubSpot |
| Viral Loops | Mixed | Mixed | Tiered by contacts | Light integration set |
| Talkable | ✓ enterprise | ✗ | Enterprise | Salesforce, Klaviyo |

---

## Antipattern catalog

### Antipattern 1: Tactic-without-diagnosis
**BAD:** "Let's add a referral program to improve growth."
**Why bad:** No data shows referral is the constraint. Could be activation, retention, conversion. Random tactic → random outcome.
**GOOD:** "Day 30 retention is 12%, decay curve, activation rate 8%. Activation is the constraint. Referral programs amplify retention — won't help here. Fix activation first."

### Antipattern 2: Vanity metric tracking
**BAD:** "MAUs grew 40% MoM."
**Why bad:** Total MAUs hides cohort truth. Could be new signups masking high churn.
**GOOD:** "Acquisition cohort retention at Day 30: Jan=18%, Feb=22%, Mar=15%. Quality declining. New traffic is from a paid channel — investigate."

### Antipattern 3: Confusing aha and activation
**BAD:** "Our aha moment is when users save their first file. Activation rate is 60%."
**Why bad:** Saves-first-file is the activation event (behavioral). Aha is "I finally have my docs organized" (emotional). They might correlate, but conflating them blocks Sean-Ellis validation.
**GOOD:** "Activation event: saves first file in 7 days (proxy). Aha moment per Sean-Ellis test: 'I can finally find anything in seconds.' 42% 'very disappointed' — PMF signal."

### Antipattern 4: Single-arm "we saw lift"
**BAD:** "We made the CTA red and conversions went up 8%. Ship it."
**Why bad:** No control; could be seasonality, day-of-week, novelty. Likely regresses.
**GOOD:** "A/B test red vs blue CTA, N=2400 per arm, primary metric = signup conversion, MDE 5%, ran 14 days, treatment lifted 8% at p=0.02. Ship."

### Antipattern 5: K > 0 means viral
**BAD:** "Our K is 0.4. We have a viral loop."
**Why bad:** K must exceed 1 for compounding (each user generates > 1 new user). K=0.4 contributes but isn't viral.
**GOOD:** "Our K is 0.4 — contributing but not viral. Most growth comes from content/SEO loop. K won't compound; it's an amplifier on other loops."

### Antipattern 6: Last-touch reallocation
**BAD:** "Last-touch shows organic search drives 60% of conversions. Cut paid by 40%."
**Why bad:** Last-touch is biased to bottom-funnel. Paid likely drives top-of-funnel that converts later via organic search.
**GOOD:** "MMM shows paid drives 35% of incremental conversion; last-touch shows 12%. The 23% gap is brand-search and direct that paid created. Run lift test before reallocating."

### Antipattern 7: Decay curve + expansion tactics
**BAD:** "Retention decays to 0. Let's launch a Pro tier upsell campaign."
**Why bad:** Decay = users churning before they activate. There's no surviving cohort to expand.
**GOOD:** "Decay curve = activation problem. Fix activation (TTV, onboarding, aha) before any expansion play. Otherwise you're upselling users who'll churn next month."

---

## Reference patterns

### Pattern: cohort-diff for activation event identification

```sql
-- PostHog HogQL
WITH cohort_a AS (
  SELECT distinct_id FROM events
  WHERE event = 'signup' AND timestamp >= '2026-04-01' AND timestamp < '2026-05-01'
),
retained_d30 AS (
  SELECT DISTINCT distinct_id FROM events
  WHERE event = 'session' AND timestamp >= '2026-05-01' AND timestamp < '2026-05-08'
    AND distinct_id IN (SELECT distinct_id FROM cohort_a)
)
SELECT
  event,
  countIf(distinct_id IN (SELECT distinct_id FROM retained_d30)) as did_retained,
  countIf(distinct_id NOT IN (SELECT distinct_id FROM retained_d30)) as did_churned,
  did_retained * 1.0 / nullIf(did_churned, 0) as lift_ratio
FROM events
WHERE distinct_id IN (SELECT distinct_id FROM cohort_a)
  AND timestamp >= '2026-04-01' AND timestamp < '2026-04-08'
GROUP BY event
ORDER BY lift_ratio DESC
LIMIT 20
```

### Pattern: Sean Ellis Test survey

Field via Typeform or Sprig:
1. Engage only users with 2+ sessions in last 14 days
2. Question: "How would you feel if you could no longer use [product]?"
3. Options: Very disappointed / Somewhat disappointed / Not disappointed / N/A
4. Optional follow-up: "What's the main reason?" (free text — feed to Claude for theming)
5. Target: 40%+ "very disappointed" = PMF signal

### Pattern: lifelines Cox PH churn model

```python
from lifelines import CoxPHFitter
import pandas as pd

# Load: tenure_days, churned (1=churned), features...
df = pd.read_sql("""
  SELECT
    DATEDIFF('day', signup_date, COALESCE(churn_date, CURRENT_DATE)) as tenure_days,
    CASE WHEN churn_date IS NOT NULL THEN 1 ELSE 0 END as churned,
    feature_adoption_count,
    team_size,
    weekly_active_days_avg,
    nps_score,
    support_tickets_count
  FROM analytics.users
""", postgres_conn)

cph = CoxPHFitter()
cph.fit(df, duration_col='tenure_days', event_col='churned')
cph.print_summary()

# Hazard ratios > 1 = increases churn risk
# Predict 30-day survival per user
df['surv_30'] = cph.predict_survival_function(df, times=[30]).T
at_risk = df[df['surv_30'] < 0.7]
```

### Pattern: GrowthBook experiment via MCP

```javascript
// via growthbook-mcp
await growthbook.create_experiment({
  name: "onboarding-checklist-v2",
  hypothesis: "Adding progress checklist will lift activation by 5pp",
  variants: [
    { name: "control", weight: 0.5 },
    { name: "checklist", weight: 0.5 }
  ],
  primary_metric: "activation_event_7d",
  secondary_metrics: ["signup_completion", "day_7_retention"],
  sample_size: 2400,
  mde: 0.05,
  kill_criteria: {
    primary_negative_significance: 0.01,
    guardrail: "day_7_retention",
    guardrail_threshold: -0.02
  }
})
```

---

## SOTA tool reference (June 2026)

This section is grep-only — the agent uses keyword-driven retrieval to surface the right skill pack for the user's task. Headings are search-friendly. Each entry links to a detailed `SKILL.md` in `skills/` that ships in this bundle and loads on demand.

**Full coverage map:** see `reference/SOTA_USE_CASES.md` for the per-use-case mapping and confidence rating.

### Statsig MCP server

Official Statsig MCP (GA 2025, OAuth added Nov 2025, metrics tools added Oct 2025). Reads + writes via API key permission. Knowledge Graph (2026) connects codebase → flags → experiments → users → metrics. Use when client already on Statsig or for SOTA enterprise experimentation.

- **Skill:** for full ops, use the `growth-loop-design-5-types` skill alongside; Statsig MCP integration spec lives in `cli-anything` patterns
- **Endpoint:** Statsig hosted MCP (HTTP); or `pypi install statsig-mcp`
- **Auth:** OAuth → `STATSIG_OAUTH_TOKEN`
- **Key calls:** `create_experiment`, `get_experiment_results`, `create_feature_gate`, `query_metric`, `list_metrics`, `get_knowledge_graph`
- **Source:** https://www.statsig.com/mcp

### GrowthBook MCP

GrowthBook MCP — 14 tools for feature flags + A/B + multi-variant + holdouts + bandit allocation + statistical significance gating + auto-stop on negative significance. Every loop hypothesis ships as a GrowthBook experiment with sample size, MDE, kill criteria, primary + secondary metrics. OSS — preferred default for cost-sensitive recipients.

- **Skill:** Implicit in every experimentation skill (`landing-page-cro-vwo-hotjar-maze`, `free-to-paid-upgrade-prompts`, `signup-activation-conversion-optimization`)
- **Endpoint:** `npx growthbook-mcp` + `https://api.growthbook.io`
- **Auth:** API key → `GROWTHBOOK_API_KEY`
- **Key calls:** `create_experiment`, `get_experiment_results`, `create_feature`, `add_targeting_rule`, `calculate_sample_size`
- **Source:** https://blog.growthbook.io/introducing-the-first-mcp-server-for-experimentation-and-feature-management/

### PostHog MCP (HogQL for growth)

PostHog MCP at `mcp.posthog.com`. HogQL `query` tool for retention curves (Day 1/7/30/90), viral coefficient K, cycle time, activation rate, funnel leakage, cohort analysis, CAC payback computation. Free hosted MCP — preferred default for analytics.

- **Skill (multiple):** `viral-coefficient-k-measurement`, `activation-funnel-aha-moment`, `retention-curve-churn-diagnosis-j-smile`, `time-to-value-ttv-optimization`, `behavioral-cohort-design`
- **MCP:** `posthog-mcp` (in agent.yaml)
- **Endpoint:** `https://mcp.posthog.com/v1`
- **Auth:** Personal API Key → `POSTHOG_PERSONAL_API_KEY`
- **Key calls:** `query` (HogQL), `funnel`, `retention`, `cohorts_create`, `feature_flag_create`
- **Source:** https://posthog.com/docs/model-context-protocol

### Amplitude MCP (24 tools, OAuth 2.0)

Amplitude MCP — 24 distinct analytical tools (search/create dashboards, charts, notebooks, cohorts, experiments). 2026 SOTA cohort intelligence + Session Replay context + full behavioral graph. OAuth 2.0 (no raw API key passing — enterprise infosec compliant). Use when client already on Amplitude or for enterprise.

- **Skill (multiple):** Same skills as PostHog above
- **MCP:** `amplitude-mcp` (in agent.yaml)
- **Auth:** OAuth 2.0 → `AMPLITUDE_OAUTH_TOKEN`
- **Key calls:** `query_user_data`, `create_cohort`, `create_dashboard`, `create_experiment`, `query_retention`, `query_funnel`
- **Source:** https://amplitude.com/docs/amplitude-ai/amplitude-mcp

### Mixpanel MCP

Mixpanel MCP — query events, funnels, retention, session replays, JQL exports, NDJSON raw events. Cohort creation + annotation supported (but not audience editing — use UI). Strong for PLG self-serve analytics teams.

- **Skill (multiple):** Same skills
- **MCP:** `mixpanel-mcp` (in agent.yaml)
- **Auth:** API Key → `MIXPANEL_API_KEY`
- **Key calls:** `query_funnel`, `query_retention`, `cohort_create`, `jql_run`, `export_events`
- **Source:** https://docs.mixpanel.com/docs/mcp

### lifelines (Python survival analysis)

Python `lifelines` library — Cox PH, Kaplan-Meier, Accelerated Failure Time models. SOTA for SaaS churn prediction (CamDavidsonPilon repo includes SaaS churn + piecewise regression notebook). 2026 augmentation: LLM-extracted features from tickets/NPS/calls feed survival model.

- **Skill:** `churn-prediction-modeling`
- **Install:** `cli-anything uvx --from lifelines python script.py`
- **Key calls:** `CoxPHFitter().fit()`, `KaplanMeierFitter().fit()`, `AcceleratedFailureTimeFitter().fit()`
- **Source:** https://github.com/CamDavidsonPilon/lifelines

### Google Meridian MMM (OSS)

Google Meridian (OSS, open-sourced 2024). May 2026 added GeoX for geo-incrementality. Replaces six-figure consulting engagement; needs ~2 years weekly spend per channel + revenue + control vars. Outputs response curves + budget allocation.

- **Skill:** `attribution-last-multi-touch-mmm-meridian-robyn`
- **Install:** `git clone https://github.com/google/meridian && pip install -e meridian`
- **Source:** https://github.com/google/meridian + https://www.appier.com/en/blog/what-is-marketing-mix-modeling-mmm-a-complete-guide-to-meridian-and-how-it-revolutionizes-traditional-approaches

### Meta Robyn MMM (OSS)

Meta Robyn — OSS MMM. Explicit calibration against geo-tests + lift studies + MTA (multi-method by design). R or Python interface.

- **Skill:** Same skill as Meridian
- **Install:** `cli-anything install robyn` (Python) or R `install.packages("Robyn")`
- **Source:** https://facebookexperimental.github.io/Robyn/

### PyMC-Marketing (Bayesian MMM)

PyMC Labs PyMC-Marketing — Bayesian MMM library. Strong for teams with PyMC familiarity; expressive prior specification.

- **Install:** `pip install pymc-marketing`
- **Source:** https://github.com/pymc-labs/pymc-marketing

### Hightouch (reverse ETL — composable CDP)

Hightouch — Gartner MQ Leader; $1.2B valuation; deepest destination catalog (Klaviyo, Customer.io, Facebook Custom Audiences, HubSpot, Salesforce). Composable CDP — no separate data store.

- **Skill:** `reverse-etl-hightouch-census-growth`
- **Endpoint:** Hightouch REST API
- **Auth:** API key → `HIGHTOUCH_API_KEY`
- **Key calls:** `create_model`, `create_audience`, `create_sync`, `trigger_sync`
- **Source:** https://www.rudderstack.com/competitors/hightouch-vs-census/

### Census (now Fivetran, 2025)

Census — acquired by Fivetran May 2025. Now part of Fivetran's unified data movement (900+ connectors). Same reverse-ETL function.

- **Skill:** Same skill as Hightouch
- **Source:** https://www.integrate.io/blog/census-review/

### Segment CDP

Segment — 20K+ customers, 350+ integrations. Default CDP. Event taxonomy in Object-Action past-tense format. Tracking plan documented in Avo or Notion.

- **Skill:** `cdp-segment-rudderstack-mparticle`
- **Endpoint:** Segment Tracking API
- **Auth:** Write Key → `SEGMENT_WRITE_KEY`
- **Key calls:** `identify`, `track`, `page`, `group`, `alias`
- **Source:** https://segment.com/docs/connections/spec/

### RudderStack CDP (OSS)

RudderStack — OSS Segment alternative; 50-80% cost savings; warehouse-native architecture. Strong for cost-sensitive recipients with warehouse already in place.

- **Skill:** Same skill as Segment
- **Source:** https://genesysgrowth.com/blog/best-alternatives-for-twilio-segment

### Intercom + Fin AI

Intercom — best-in-class for PLG in-app messaging + product tours. Fin AI agent resolves 50-70% of inbound autonomously (Apr 2026 Intercom claim). Pricing escalates fast — $29 starter can become $2,700+ at scale.

- **Skill:** `in-app-messaging-intercom-drift-pendo`
- **Endpoint:** Intercom REST API
- **Auth:** Access Token → `INTERCOM_TOKEN`
- **Key calls:** `messages.create`, `users.create_or_update`, `tags.create`, `segments.list`
- **Source:** https://www.intercom.com/

### Customer.io (event-triggered journeys)

Customer.io — logic-heavy event-triggered journeys; Email + Push + In-app + SMS + WhatsApp. Strong for mid-market with complex behavioral rules.

- **Skill:** `win-back-campaigns` + `in-app-messaging-intercom-drift-pendo` (Customer.io section)
- **Endpoint:** Customer.io REST API
- **Auth:** API key → `CUSTOMERIO_API_KEY`
- **Key calls:** `campaigns.create`, `segments.create`, `customers.upsert`
- **Source:** https://www.getvero.com/resources/braze-vs-customer-io-which-is-better-in-2026/

### Userpilot / Appcues / Pendo / Chameleon (onboarding)

Decision matrix above. PostHog/Amplitude integration for analytics; native or external. `cli-anything` curl for spec deployment.

- **Skill:** `onboarding-userpilot-appcues-chameleon`
- **Sources:** https://userpilot.com/blog/appcues-alternatives/ + https://www.chameleon.io/alternative/userpilot-alternatives + https://www.pendo.io/pendo-blog/the-top-8-in-app-guidance-tools-in-2025/

### ReferralCandy / GrowSurf / Friendbuy / Viral Loops

Decision matrix above. `cli-anything` curl for program creation; webhooks for trigger integration.

- **Skill:** `referral-program-referralcandy-friendbuy-growsurf`
- **Source:** https://www.stackscored.com/pricing/referral-marketing/

### Yotpo / Smile.io / LoyaltyLion / Klaviyo Loyalty

Loyalty platform choice — Yotpo for full reviews+loyalty+SMS; Smile.io for Shopify ease; LoyaltyLion for points/tiers/VIP; Klaviyo Loyalty for native Klaviyo loop. APIs via `cli-anything`.

- **Skill:** `loyalty-program-yotpo-smile-loyaltylion`

### Pocus / Koala / HockeyStack (PQL platforms)

PQL signal aggregation + scoring + CRM handoff. Pocus is full PLG platform; Koala is intent+visitor-ID lighter; HockeyStack bridges PLG + B2B attribution.

- **Skill:** `pql-product-qualified-leads-framework`
- **Sources:** https://www.pocus.com/blog/the-definitive-pql-guide-part-1 + https://syncgtm.com/blog/koala-review + https://www.hockeystack.com/

### Sprig / Survicate (microsurveys)

In-product microsurveys for Sean Ellis, NPS, contextual feedback. Sprig has 2026 AI Agents for unstructured-feedback themeing. Survicate has broader channel coverage (web, mobile, email, feedback buttons). Free fallback: Typeform via `typeform` skill.

- **Skill:** Use `activation-funnel-aha-moment` skill for Sean Ellis Test, `behavioral-cohort-design` for cohort-targeted micro-surveys
- **Sources:** https://sprig.com/ + https://survicate.com/

### Microsoft Clarity (free heatmap + session replay)

Microsoft Clarity — free heatmap + session replay tool. 2026 SOTA for free tier. Hotjar paid alt; FullStory enterprise.

- **Skill:** `landing-page-cro-vwo-hotjar-maze`
- **Source:** https://clarity.microsoft.com/

### Conjoint.ly (Van Westendorp + Gabor-Granger + conjoint)

Conjoint.ly — survey platform for price research. SOTA for PSM + Gabor-Granger; conjoint analysis (price-as-attribute). Paid plans.

- **Skill:** `price-experimentation-van-westendorp-conjoint`
- **Source:** https://conjointly.com/

### OneSignal / Braze / Iterable (push notifications)

Push platform choice — OneSignal default (free tier); Braze enterprise; Iterable mid-market+; Customer.io Push for unified.

- **Skill:** Push handling within `in-app-messaging-intercom-drift-pendo` + `win-back-campaigns`
- **Source:** https://onesignal.com/blog/top-braze-alternatives-for-email-push-in-2026/

### Klaviyo / Customer.io / Attentive / Postscript (email + SMS)

Defer detail to `email-strategist`. Growth-agent integrates via:
- Cohort sync from PostHog → Klaviyo via Hightouch
- PQL → CRM → Klaviyo flow trigger
- Win-back: lifecycle reactivation via Customer.io / Klaviyo

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| "Design our growth loop" | `growth-loop-design-5-types` | Classify 5 types; map; constraint |
| "What's our viral coefficient?" | `viral-coefficient-k-measurement` | PostHog HogQL or Amplitude formula |
| "Find our activation event" | `activation-funnel-aha-moment` | Cohort-diff + Sean Ellis |
| "Diagnose retention" | `retention-curve-churn-diagnosis-j-smile` | Plot curve, classify shape, prescribe |
| "Reduce TTV" | `time-to-value-ttv-optimization` | p25/p50/p75 + experiment |
| "Predict churn" | `churn-prediction-modeling` | lifelines Cox PH + LLM signals |
| "Set up A/B testing" | (any experimentation skill) | GrowthBook MCP or Statsig MCP |
| "Build PQL framework" | `pql-product-qualified-leads-framework` | Multi-signal score + CRM handoff |
| "Build growth model spreadsheet" | `growth-model-spreadsheet-compound-levers` | Sequoia/Reforge format, 3 scenarios |
| "Define our North Star" | `north-star-omtm-pirate-metrics-heart` | Validate via correlation to revenue |
| "Set up attribution" | `attribution-last-multi-touch-mmm-meridian-robyn` | MMM (Robyn/Meridian) + MTA + lift tests |
| "Set up our CDP" | `cdp-segment-rudderstack-mparticle` | Platform choice + taxonomy + tracking plan |
| "Sync cohorts to Klaviyo" | `reverse-etl-hightouch-census-growth` | Hightouch model → audience |
| "PLG or sales-led?" | `plg-vs-sales-led-motion-decision` | ACV/aha/buyer-count matrix |
| "Build referral program" | `referral-program-referralcandy-friendbuy-growsurf` | Platform choice + incentive |
| "Build loyalty program" | `loyalty-program-yotpo-smile-loyaltylion` | Platform choice + point structure |
| "Onboarding flow design" | `onboarding-userpilot-appcues-chameleon` | Platform choice + checklist spec |
| "Test our pricing" | `price-experimentation-van-westendorp-conjoint` | PSM + Gabor-Granger sequential |
| "Free-to-paid prompts" | `free-to-paid-upgrade-prompts` | PQL-triggered + trial-end flow |
| "Win-back dormant users" | `win-back-campaigns` | Customer.io / Klaviyo sequence |
| "Cohort design" | `behavioral-cohort-design` | Multi-attribute time-windowed |
| "Flywheel mapping" | `signup-to-revenue-flywheel` | Velocity per stage + friction reduction |
| "Improve expansion / NRR" | `expansion-revenue-nrr-optimization` | Upsell triggers + NRR math |
| "Fix signup → activation" | `signup-activation-conversion-optimization` | Funnel leak + friction reduction |
| "In-app messaging" | `in-app-messaging-intercom-drift-pendo` | Tool choice + event-triggered |
| "CRO landing page" | `landing-page-cro-vwo-hotjar-maze` | A/B + heatmap diagnostic |

---

## Closing rules

Loops compound — funnels leak. Activation predicts retention. Data before tactics. Cohort over aggregate. Statistical significance over storytelling. Defer to channel specialists (`marketing-agent`, `seo-specialist`, `email-strategist`) when channel depth is required. Defer to `product-manager` for feature shaping, `data-analyst` for warehouse depth, `sales-agent` for sales-led motion.
