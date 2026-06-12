# Growth Agent — Use Cases

**Tier:** **general** · **Category:** growth
**Core job:** Compounding-side growth lead — loops, activation, retention, experimentation, PLG mechanics, attribution model design, behavioral cohorts.

Ships with the 2026 SOTA growth-operator stack (PostHog / Amplitude / Mixpanel MCPs for analytics; GrowthBook / Statsig MCPs for experimentation; Robyn / Meridian / PyMC-Marketing for MMM; lifelines for survival analysis; Hightouch / Census for reverse-ETL; `cli-anything` for the 20+ REST APIs not yet exposed as native MCPs). Executes end-to-end, not just direct. Distinct from `marketing-agent` (channel breadth) — pair, don't replace.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### Growth loop design
- Identify product output → classify against 5 loop types (viral / content-SEO / paid / network-effect / sales-led)
- Diagram loop with metric at each step (K, cycle time, conversion per step)
- Constraint analysis (weakest step)
- 2-3 ranked experiments per loop with hypothesis + sample size + MDE + primary/secondary metric + kill criteria

### Activation funnel + Aha Moment
- Find activation event via cohort-diff (Day 30 retained vs churned behaviors)
- Validate via Sean Ellis Test (40%+ "very disappointed" = PMF signal)
- Measure activation rate vs benchmark (B2B SaaS avg 37.5%, best-in-class 60%+)
- Diagnose aha → activation gap

### Time-to-value (TTV) optimization
- TTV p25/p50/p75 measurement (signup → value event)
- Best-in-class benchmark (<5 min self-serve, <24h complex)
- Reduction tactics (skip-able onboarding, templates, AI-assisted setup, magic-link signup, SSO)
- A/B experiment design

### Retention curve diagnosis
- Plot Day 0/1/7/30/90 retention (cohorted, not aggregate)
- Classify shape: smile / J-curve / decay / flat-after-drop
- Shape-prescribed fix (decay = activation problem, flat-after-drop = expansion opportunity)
- Slice by acquisition channel + persona + plan tier + cohort week

### Churn prediction
- Survival-analysis model (lifelines Cox PH, Kaplan-Meier, AFT)
- LLM-augmented signal extraction (tickets, NPS, calls per 2026 SOTA)
- At-risk cohort identification (30/60/90-day survival probability)
- Handoff to win-back / CSM / product team based on signal

### Viral coefficient (K) measurement + optimization
- K calculation via PostHog HogQL or Amplitude formula
- Cycle time + conversion per step
- K > 1 strategies (invite mechanism, incentive timing)
- A/B viral mechanic placement (pre-aha vs post-aha vs post-payment)

### Experimentation infrastructure
- Platform choice (Statsig / GrowthBook / Eppo / LaunchDarkly)
- Sample-size pre-calc + MDE
- Primary + ≤2 secondary metrics + kill criteria
- Holdout group design (5-10% permanent for long-term effect)
- Auto-stop on negative significance

### PLG / PQL framework
- Multi-signal PQL scoring (usage limits + feature depth + team activity + frequency)
- PQL → CRM handoff (HubSpot / Salesforce via curl)
- Slack alert at threshold (via `slack-mcp`)
- PQL → opportunity → closed-won tracking

### Free-to-paid + expansion
- PQL-triggered upgrade prompts
- Trial-end conversion flow (7-day pre-end → 1-day-out → trial-end day → 1-day post-end → 7-day reactivation)
- Cross-sell / upsell trigger design
- NRR measurement and optimization

### Onboarding optimization
- Platform choice (Userpilot / Appcues / Pendo / Chameleon / Whatfix)
- Checklist + progress-indicator design
- Tour spec (via `cli-anything` curl per platform)
- Activation-event-targeted milestones

### In-app messaging strategy
- Tool choice (Intercom + Fin AI / Customer.io / Pendo)
- Event-triggered message design (post-aha upgrade, churn-risk reach-out, feature-discovery)
- Triggered cohort design

### Referral program design
- Platform choice (ReferralCandy / GrowSurf / Friendbuy / Viral Loops / Talkable)
- Incentive structure (dual-sided, tiered, time-bound)
- Friction reduction (one-click share)
- A/B incentive value via GrowthBook

### Loyalty program design
- Platform choice (Yotpo Loyalty / Smile.io / LoyaltyLion / Klaviyo Loyalty)
- Point structure + redemption rules + VIP tier thresholds
- Integration with email + SMS lifecycle

### Landing page CRO
- A/B test design via GrowthBook
- Heatmap + session replay diagnostics (Microsoft Clarity free / Hotjar paid / FullStory enterprise)
- Statistical-significance gating before declaring winners

### Pricing experimentation
- Van Westendorp PSM (price-sensitivity meter)
- Gabor-Granger demand curve
- Conjoint analysis (price as one attribute)
- Sequential PSM → Gabor-Granger for SaaS

### Win-back campaigns
- Dormant-user reactivation sequence (30/60/90-day inactivity triggers)
- Escalating incentive (insight → social proof → discount/feature)
- Exit conditions (click / hard-suppress at 21 days no-engage)

### Attribution architecture
- Multi-touch attribution (GA4 data-driven, HockeyStack / Dreamdata B2B, Triple Whale / Northbeam DTC)
- Marketing Mix Modeling (Meta Robyn / Google Meridian / PyMC-Marketing)
- Lift test validation (geo-incrementality via Meridian GeoX)
- Reallocation rule (only when MMM + MTA agree)

### CDP setup + event taxonomy
- Platform choice (Segment / RudderStack / mParticle / Hightouch CDP / Tealium)
- Event taxonomy (Object-Action past-tense)
- Tracking plan documented in Notion

### Reverse ETL for growth
- Warehouse → growth tooling sync (Hightouch / Census / Polytomic / RudderStack Reverse ETL)
- Audience activation (Klaviyo / Customer.io / Facebook Custom Audiences / HubSpot)
- CRM enrichment from warehouse

### Behavioral cohort design
- Multi-attribute cohort definition (mandatory ≥2 attributes)
- Dynamic vs static
- Cohort sync from PostHog/Amplitude/Mixpanel → downstream via reverse-ETL

### Growth model spreadsheet
- Sequoia/Reforge format (CAC × conversion × LTV × payback × NRR)
- 3 scenarios (base / upside / downside)
- Sensitivity analysis per lever
- Quarterly refresh with actuals

### North Star / metric frameworks
- North Star Metric definition + 3-5 input metrics
- AARRR (Pirate Metrics) implementation
- HEART framework (Google) for feature-launch design
- 4-Fits (Brian Balfour) for motion fit
- OMTM (One Metric That Matters) quarterly focus

### PLG vs sales-led decision
- ACV / aha time / buyer count / setup complexity decision matrix
- Hybrid signal patterns
- Motion transition planning (85% of forced transitions fail — diagnose 4-Fits first)

### Feature adoption tracking
- Cohort × time-bucket adoption %
- Adoption funnel (Discovery → Trial → Habit)
- Per-cohort retention after feature adoption

### SMS / push notification strategy
- SMS lifecycle (Attentive / Postscript / Klaviyo SMS) — defer detail to `email-strategist`
- Push platform choice (OneSignal free, Braze enterprise, Iterable mid-market, Customer.io Push unified)

### Signup-to-revenue flywheel
- Flywheel velocity per stage
- Friction reduction at highest-leverage stage
- HubSpot flywheel framework adaptation

---

## Execution status (SOTA — June 2026)

### What this agent EXECUTES today (SOTA mechanisms per use case)

| Use case | SOTA mechanism | Path |
|---|---|---|
| Growth loop design (5 types) | Reforge taxonomy + Notion DB | `notion-mcp` |
| Loop diagram + constraint + experiments | PostHog HogQL + GrowthBook MCP | `posthog-mcp` + `cli-anything` |
| Viral coefficient K | PostHog HogQL / Amplitude formula | `posthog-mcp` / `amplitude-mcp` |
| Activation event identification | Cohort-diff (PostHog) + Sean Ellis (Typeform) | `posthog-mcp` + `typeform` |
| Activation rate benchmark | PostHog/Amplitude/Mixpanel cohort | MCPs |
| Retention curve shape | PostHog `retention` / Amplitude `retention` | MCPs |
| Survival-analysis churn | lifelines (Python) via `cli-anything uvx` | `cli-anything` |
| LLM-augmented churn signals | Claude + lifelines features | direct + `cli-anything` |
| TTV measurement | PostHog HogQL percentiles | `posthog-mcp` |
| TTV reduction A/B | GrowthBook MCP | `cli-anything` |
| Onboarding platform choice | Decision matrix + Userpilot/Appcues/Pendo/Chameleon APIs | `cli-anything` curl |
| In-app messaging tool choice | Decision matrix + Intercom/Customer.io APIs | `cli-anything` curl |
| Referral platform choice | Decision matrix + GrowSurf/ReferralCandy APIs | `cli-anything` curl |
| Loyalty platform choice | Decision matrix + Yotpo/Smile.io APIs | `cli-anything` curl |
| Landing page A/B | GrowthBook MCP + Microsoft Clarity heatmap | `cli-anything` + Clarity install |
| Pricing — Van Westendorp PSM | Typeform survey + Python numpy intersections | `typeform` + `cli-anything` |
| Pricing — Gabor-Granger | Same | `typeform` + `cli-anything` |
| Pricing — Conjoint | Conjoint.ly / Qualtrics survey + Python utility analysis | `cli-anything` (paid) |
| PQL-triggered upgrade prompts | PostHog cohort + Intercom message | `posthog-mcp` + `cli-anything` |
| Trial-end conversion sequence | Klaviyo / Customer.io flow | `cli-anything` |
| Churn prediction model | lifelines (Python) | `cli-anything uvx` |
| Win-back sequence | Customer.io / Klaviyo + cohort sync via Hightouch | `cli-anything` |
| Cross-sell / upsell triggers | PostHog cohort + CRM curl | `posthog-mcp` + `cli-anything` |
| NRR measurement | postgres + Klaviyo/HubSpot revenue join | `postgresql-mcp` |
| PQL scoring | PostHog HogQL + score writeback | `posthog-mcp` |
| PQL → pipeline handoff | CRM API + Slack alert | `cli-anything` + `slack-mcp` |
| Growth model spreadsheet | xlsx + PostHog actuals | `xlsx` + `posthog-mcp` |
| North Star metric | Validation via PostHog correlation | `posthog-mcp` |
| AARRR Pirate Metrics | Framework + PostHog stage mapping | `posthog-mcp` |
| HEART framework | Framework + PostHog feature mapping | `posthog-mcp` |
| 4-Fits assessment | Discovery framework | direct |
| Multi-touch attribution (B2B) | HockeyStack / Dreamdata API curl | `cli-anything` (paid) |
| Multi-touch attribution (DTC) | Triple Whale / Northbeam API curl | `cli-anything` (paid) |
| Multi-touch attribution (general) | GA4 data-driven via curl | `cli-anything` (free) |
| Marketing Mix Modeling | Robyn (Meta OSS) / Meridian (Google OSS) / PyMC-Marketing | `cli-anything uvx` |
| CDP event taxonomy + tracking plan | Segment / RudderStack spec → Notion | `notion-mcp` |
| CDP install + activation | Platform-side snippet install (recipient deploys) | spec |
| Reverse ETL — Hightouch | Hightouch model SQL + audience destination | `cli-anything` (paid) |
| Reverse ETL — Census | Census model + sync (now Fivetran) | `cli-anything` (paid) |
| Behavioral cohort definition | PostHog `cohorts_create` / Amplitude / Mixpanel | MCPs |
| Cohort → ESP sync | Hightouch / Census | `cli-anything` (paid) |
| Signup-to-revenue flywheel | Reforge flywheel + PostHog velocity metrics | `posthog-mcp` |
| PLG vs sales-led decision | Brian Balfour 4-Fits + discovery | direct |
| Feature adoption tracking | PostHog / Amplitude / Mixpanel | MCPs |
| Experimentation platform choice | Statsig / GrowthBook / Eppo / LaunchDarkly matrix | MCPs |
| Holdout group design | GrowthBook / Statsig holdout config | `cli-anything` |
| SMS lifecycle | Attentive / Postscript / Klaviyo SMS curl | `cli-anything` |
| Push notifications | OneSignal / Braze / Iterable / Customer.io Push curl | `cli-anything` |
| Heatmap diagnostics | Microsoft Clarity (free) | install script |
| Microsurvey (NPS, contextual) | Typeform / Sprig / Survicate | `typeform` + `cli-anything` |
| Competitor landing-page diff | Firecrawl scrape + Claude analysis | `firecrawl-mcp` |

### Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Conjoint.ly / Qualtrics paid pricing tier | ⚠ | Required for conjoint analysis; PSM + Gabor-Granger work with Typeform alone |
| HockeyStack / Dreamdata (B2B attribution) | ⚠ | Paid SaaS; GA4 data-driven is the free fallback |
| Triple Whale / Northbeam (DTC attribution) | ⚠ | Paid SaaS; GA4 data-driven is the free fallback |
| Hightouch / Census (reverse ETL) | ⚠ | Paid SaaS; RudderStack Reverse ETL OSS is the alternative |
| Pocus / Koala / HockeyStack (PQL platforms) | ⚠ | Paid SaaS; in-house PQL via PostHog HogQL + CRM curl is the free path |
| Statsig / Eppo / LaunchDarkly experiments | ⚠ | Paid SaaS; GrowthBook MCP is the OSS default |
| Userpilot / Appcues / Pendo / Chameleon (onboarding) | ⚠ | Paid SaaS; spec design works regardless of platform |
| Intercom / Customer.io / Klaviyo (no native MCP) | ⚠ | REST API via `cli-anything` curl works; agent specs the messages |
| ReferralCandy / GrowSurf / Yotpo (no native MCP) | ⚠ | REST API via `cli-anything` curl; spec design + program structure works regardless |
| Microsoft Clarity / Hotjar (heatmap install) | ⚠ | Recipient-side script install; agent specs the install |
| CDP install (Segment / RudderStack snippet) | ⚠ | Recipient-side install; agent specs the event taxonomy + tracking plan |

**Verdict (June 2026): ~95% fulfillment.** Every documented use case has a concrete execution path. The PostHog / Amplitude / Mixpanel / GrowthBook MCPs cover the analytics + experimentation surface natively. lifelines / Robyn / Meridian / PyMC-Marketing cover the modeling surface via `cli-anything uvx`. The 20+ growth-tooling APIs not yet exposed as native MCPs (Intercom, Customer.io, Klaviyo, Userpilot, ReferralCandy, Hightouch, Census, etc.) are all reachable via `cli-anything` curl — the agent specs the action, the recipient provides the API key. The only true friction is paid SaaS keys the recipient owns.

---

## When to use this agent

- "Diagnose our growth — retention curve and constraint"
- "Find our activation event from cohort behavior"
- "Design a growth loop for our product"
- "What's our viral coefficient and is it sustainable?"
- "Predict 30-day churn risk per user"
- "Set up our experimentation infrastructure"
- "Build our growth model spreadsheet"
- "Should we go PLG, sales-led, or hybrid?"
- "Set up multi-touch attribution + MMM"
- "Design our PQL framework and CRM handoff"
- "Reduce our time-to-value"
- "Build a referral program"
- "Why is retention dropping? (curve shape diagnosis)"

## When NOT to use this agent

- Channel breadth (SEO content, social posts, ad copy, brand voice) — hand off to `marketing-agent`
- Deep technical or content SEO — hand off to `seo-specialist`
- Deep email lifecycle + deliverability — hand off to `email-strategist`
- Product feature design + roadmap shaping — hand off to `product-manager`
- Deep SQL + warehouse modeling beyond growth metrics — hand off to `data-analyst`
- Sales sequence, ABM, outbound — hand off to `sales-agent`
- Customer support strategy + ticket ops — hand off to `customer-support-agent`
- Brand strategy / positioning — defer to `marketing-agent` (first) then a brand specialist (v1)
