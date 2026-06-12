# Product Manager — deep reference

This appends to `AGENT.md`. **Not** in the agent's default context. Grep when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "PRD playbook", "Roadmap playbook", "Research synthesis playbook", "Prioritization playbook", "Experiment design playbook", "Discovery to delivery playbook", "Stakeholder update playbook", "Launch coordination playbook", "OKR playbook", "Story mapping playbook", "JTBD framework", "Strategy doc framework", "Antipattern catalog", "PRD 1-pager template", "PRD full template", "Experiment doc template", "Stakeholder update template", "Launch checklist template", "SOTA tool reference", "SOTA execution playbook".

For provenance, see `SOURCES.md`.

---

## Capability reference

### PM artifact types this agent handles

- PRDs (1-pager + full)
- Roadmaps (now/next/later, quarterly, annual)
- Strategy docs (annual, with quarterly check-ins)
- OKR drafts and tracking
- User research repos (interview themes, NPS analysis, survey synthesis)
- Prioritization scorecards (RICE / ICE / Kano / MoSCoW / WSJF)
- Experiment docs (hypothesis + design + readout)
- Sprint plans and story breakdowns
- User story maps (Patton method)
- Discovery → delivery handoff packets
- Stakeholder updates (weekly / monthly / quarterly board)
- Release notes (user-facing + engineering changelog)
- Launch briefs and checklists
- Beta program plans
- Pricing + packaging experiments
- Competitive product teardowns
- Customer interview scripts + synthesis
- Voice-of-customer (VoC) aggregation

### Prioritization frameworks

- **RICE** — Reach × Impact × Confidence / Effort. Default for backlog ranking.
- **ICE** — Impact × Confidence × Ease. Default for experiment prioritization.
- **Kano** — Basic / Performance / Excitement / Indifferent / Reverse. Default for feature-set design.
- **MoSCoW** — Must / Should / Could / Won't. Default for scope cuts when shipping by deadline.
- **WSJF** — Cost of Delay / Job Size. Default in SAFe-adjacent shops.
- **Value vs Effort 2x2** — quick gut-check matrix when you have <30 items.
- **Opportunity scoring** (Ulwick) — Importance + Satisfaction → outcome opportunities.

### Discovery + research frameworks

- **JTBD outcome statements** — `<direction> + <unit of measure> + <object> + <context>` (Ulwick / Christensen)
- **Forces of progress** — push from current, pull to new, anxieties, habits (Christensen / ReWired Group)
- **5 Whys** — root-cause drill-down
- **Mom Test (Rob Fitzpatrick)** — interview questions that get real answers, not flattering ones
- **Continuous discovery (Teresa Torres)** — opportunity solution tree (OST) + weekly customer touchpoints
- **Discovery sprint (Marty Cagan)** — 1-2 weeks of problem validation before scoping a solution

### Product strategy frameworks

- **Rumelt kernel** — Diagnosis / Guiding policy / Coherent actions (`Good Strategy / Bad Strategy`)
- **Helmer 7 Powers** — Scale / Network economies / Counter-positioning / Switching costs / Branding / Cornered resource / Process power
- **Wardley mapping** — value chain x evolution (Genesis / Custom / Product / Commodity)
- **North Star Metric framework** — single metric that captures the value the product delivers (Sean Ellis)
- **HEART framework** (Google) — Happiness / Engagement / Adoption / Retention / Task success per feature
- **Pirate metrics AARRR** (Dave McClure) — Acquisition / Activation / Retention / Referral / Revenue
- **Pendo growth model** — Activation → Engagement → Retention as a flywheel

### Experimentation frameworks

- **Pre-registration** — hypothesis + metrics + sample size + MDE + duration + kill criteria documented before launch
- **Power analysis** — sample size = f(baseline rate, MDE, alpha, power); duration = sample size / daily traffic
- **Sequential testing** — when you peek mid-experiment; e.g., Optimizely's "Stats Engine", GrowthBook's sequential testing
- **Bandit allocation** — non-uniform traffic split that learns; Statsig + GrowthBook + Eppo support
- **Holdout / counterfactual cohort** — fraction never gets the feature; measures long-term effect
- **Switchback** — alternate variant on time intervals; for marketplace / two-sided experiments

### Product analytics primitives

- **Funnel** — sequential step conversion; drop-off per step
- **Retention** — D1/D7/D30/D90 cohort curves; rolling vs classic retention
- **Activation** — time-to-first-value; activation event = "first 3 actions within 7 days" (or product-specific)
- **Engagement** — DAU/MAU ratio; sessions per user; key action frequency
- **North Star** — single metric (engaged users × value per engaged user)
- **Cohort** — group of users defined by attribute (signup month, plan, segment)
- **Behavioral cohort** — group defined by action ("users who did X in last 7 days")

### Marketing/sales/support adjacent tools (defer when depth needed)

- **CRM**: HubSpot, Salesforce, Pipedrive — defer to `sales-agent` for pipeline analysis
- **Marketing automation**: HubSpot, Klaviyo, Marketo — defer to `marketing-agent` for lifecycle
- **Support**: Intercom, Zendesk, Front, HelpScout — defer to `customer-support-agent` for theme synthesis
- **Sales call recording**: Gong, Chorus, Fathom, Otter, tl;dv — for VoC aggregation, pull transcripts via API
- **Analytics warehouse**: Snowflake, BigQuery, Redshift — defer to `data-analyst` for deep SQL

---

## PRD playbook

### PRD 1-pager template

```markdown
# [Feature Name] — 1-pager PRD

**Author:** [PM] · **Date:** [YYYY-MM-DD] · **Status:** Draft / Reviewed / Approved

## Problem
[1 paragraph. What user pain are we solving + why now? Cite evidence: interview count + analytics signal + support ticket count.]

## Hypothesis
If we [build X], then [primary metric] will [direction] by [MDE] because [reason rooted in user job].

## Primary user
[Named segment: e.g., "Solo founders on the $29/mo plan who use feature Y weekly." Add JTBD if helpful.]

## Success criteria (measurable)
- Primary: [metric, baseline → target, time horizon]
- Secondary: [metric, baseline → target]
- Guardrail: [metric that must NOT degrade]

## Scope
- [User story or capability 1]
- [User story or capability 2]
- [3-7 items total]

## Non-goals (explicit)
- [What we're NOT doing 1]
- [What we're NOT doing 2]
- [≥3 items]

## Open questions
- [Question 1 — owner + deadline]
- [Question 2 — owner + deadline]

## Risks + mitigation
- [Risk 1 — mitigation]
- [Risk 2 — mitigation]

## GTM placeholder
[1 paragraph or "TBD — handed to marketing-agent"]

## Dependencies
- Design: [Figma link or "TBD"]
- Engineering: [estimate or "TBD"]
- Analytics: [tracking spec — events + properties]
```

### PRD full template (additional sections beyond 1-pager)

```markdown
## Context + background
[Why this matters now. Strategic alignment to OKRs. Market context. Internal context.]

## User research findings
[Interview themes with verbatims; analytics baseline; competitive notes.]

## Solution approach
[Sketch of the solution. Wireframes link. Alternative approaches considered and rejected — why?]

## Detailed user stories with acceptance criteria
[Given / When / Then format. Each story has measurable AC.]

## Technical considerations
[Notes for engineering. NOT a design spec. Constraints, dependencies, security/privacy/compliance flags.]

## Analytics + instrumentation spec
[Event names, properties, sample SQL/HogQL query. Tracking is part of "done."]

## Rollout plan
[Feature flag → beta → graduated rollout → GA. Kill criteria at each stage.]

## Open questions (extended)
[All questions + owners + deadlines.]

## Appendix
[Research, mocks, alternative solutions, references.]
```

### PRD review rubric (run before approving)

- [ ] **Problem clarity** — 1 paragraph, with a "why now" + evidence (interview count / analytics signal / ticket count)
- [ ] **Hypothesis** — if/then/because format; metric named with direction + MDE
- [ ] **Primary user named** — segment defined; "everyone" is not allowed
- [ ] **Success criteria measurable** — primary + secondary + guardrail; baseline + target + horizon
- [ ] **Scope bounded** — 3-7 items; not a wish list
- [ ] **Non-goals explicit** — ≥3; says what we're NOT doing
- [ ] **Open questions** — ≥2; each with owner + deadline
- [ ] **Risks** — ≥2; each with mitigation
- [ ] **Vague verbs stripped** — no "improve", "optimize", "leverage", "enhance", "streamline" without concrete action
- [ ] **Every claim cited** — analytics queries linked, interviews counted, tickets counted
- [ ] **Tracking spec** — event names + properties defined (part of "done")

### Antipatterns in PRDs

**BAD:** "Increase engagement on the home page"
**Why bad:** Engagement isn't a metric; home page isn't a user; no target.
**GOOD:** "Increase D7 retention among solo-founder accounts from 35% → 42% by Q3, by reducing onboarding friction in the first session."

**BAD:** "Build a notifications center"
**Why bad:** No user, no problem, no outcome.
**GOOD:** "Solo founders miss customer replies in email because the inbox is noisy. Hypothesis: a notifications center in-product surfaces replies within 1 minute, increasing reply-to-customer time from 12h median → 2h median."

**BAD:** "Q3 roadmap: build features A, B, C, D, E, F, G"
**Why bad:** Output list, not outcome. No prioritization. No hypothesis.
**GOOD:** "Q3 outcome: ship the activation revamp (target D7 retention 35% → 42%). Scoped work: A, B, C. Hypothesis-only for Q4: D, E."

---

## Roadmap playbook

### Now / Next / Later structure

- **Now** — committed to current quarter; scoped (PRDs done, engineering sized); shipping this cycle plan
- **Next** — planned for next quarter; light scope (problem validated, solution shape known); subject to refinement
- **Later** — explored only; hypothesis stage; problem identified but solution not scoped

### Quarterly roadmap one-pager template

```markdown
# Q[X] [YYYY] Roadmap — [Product]

**Hypothesis:** This is not a contract. We will ship the "now" column. The "next" column is our best current bet. The "later" column is intent only.

## OKR alignment
- O1: [Objective] → addressed by [items in this roadmap]
- O2: [Objective] → addressed by [items]

## Now (committed)
| Initiative | Outcome target | Owner | Status |
|---|---|---|---|
| ... | ... | ... | In progress / Discovery / Ready |

## Next (planned)
| Initiative | Outcome target | Owner | Discovery status |
|---|---|---|---|
| ... | ... | ... | Problem validated / Solution sized / Both |

## Later (explored)
| Theme | Outcome hypothesis | Discovery owner |
|---|---|---|
| ... | ... | ... |

## Won't (out of scope this period)
- [Explicit "no" items — usually loud asks deferred]

## Risks
- [Cross-team dependency 1]
- [Capacity risk]
- [External dependency]
```

### Roadmap communication tiers (audience-driven detail)

- **Exec / board** — OKR alignment + 5-7 themes + risks. Don't share epic-level work.
- **Engineering** — initiative + epic + ready-cycle for each. Linear roadmap shared link.
- **All-hands** — outcomes + themes + dates (with hypothesis caveat). Use `pptx` skill.
- **Customers (external)** — themes only, no dates. Productboard portal + "what's next" page.

---

## Research synthesis playbook

### Interview synthesis procedure

1. **Source the transcripts.** Fathom / Otter / tl;dv / Gong / manual notes. Aim for ≥5 interviews on the same JTBD before claiming a theme.
2. **First-pass tag.** Read each transcript; tag quotes with theme labels. Dovetail v3 does this with AI-assist + manual cleanup.
3. **Cluster tags into themes.** 3-7 themes max. If you have 12, you're not done clustering.
4. **Pull 2-3 verbatims per theme.** With source (interviewee identifier + timestamp).
5. **Count theme occurrences.** "8 of 11 founders mentioned the inbox-overload pain" beats "founders are overwhelmed."
6. **Recommend next steps.** Per theme: more research / scope a feature / monitor / deprioritize.

### Research repo entry template

```markdown
# Research: [Topic]

**Date:** [YYYY-MM-DD] · **Researcher:** [Name] · **Sample:** N=X [segment]

## Method
[How: interviews, surveys, analytics, support tickets, sales calls. Recruitment criteria.]

## Sample
- N = [count]
- Segment: [description]
- Recruitment: [how sourced]

## Themes
### Theme 1: [Name] (mentioned by X of Y)
[1-2 sentence summary.]

**Verbatims:**
> "Quote 1." — [P3]
> "Quote 2." — [P7]
> "Quote 3." — [P11]

**Implication:** [What this suggests.]

### Theme 2: ...

## Recommended next steps
- [Per theme: more research / scope / monitor / deprioritize — with rationale]

## Open questions
- [Things we still don't know]

## Appendix
- Interview guide: [link]
- Transcripts: [Dovetail project link]
- Tag taxonomy: [link]
```

### JTBD interview structure

1. **The "what" moment.** "Walk me through the day you bought / signed up / started using X."
2. **The "before" forces.** "What was happening that made you start looking for a solution?" (push)
3. **The "alternative" set.** "What other options did you consider? What turned you off?"
4. **The "during" experience.** "What got you to commit? What almost stopped you?" (pull, anxieties)
5. **The "after" outcome.** "What did you hope would change? What actually did?"
6. **The "habit" check.** "Why didn't you switch to something else later?" (habits)

Outcome statement format: `<direction> the <unit of measure> of <object> when <context>`.
Example: `minimize the time it takes to find a customer's last reply when checking the inbox at start of day`.

---

## Prioritization playbook

### RICE (default backlog)

```
Score = (Reach × Impact × Confidence) / Effort
```

- **Reach** — # of users affected per quarter (real number, not 1-10)
- **Impact** — effect per user when they encounter (3 = massive, 2 = high, 1 = medium, 0.5 = low, 0.25 = minimal)
- **Confidence** — % confidence in estimates (100% = data-backed; 80% = some evidence; 50% = gut)
- **Effort** — person-months (or person-weeks)

### ICE (default experiments)

```
Score = Impact × Confidence × Ease (each 1-10)
```

Faster + scrappier than RICE; use for experiment intake.

### Kano model

Each feature is one of:
- **Must-have (basic)** — absence causes dissatisfaction; presence doesn't delight
- **Performance** — more is better, linearly
- **Excitement (delighter)** — unexpected; high satisfaction; absence not missed
- **Indifferent** — users don't care
- **Reverse** — some users want, others actively dislike

Run via Maze survey: 2 questions per feature (functional / dysfunctional). Tag answers by Kano cell.

### MoSCoW (scope cuts)

- **Must** — without this, the release fails
- **Should** — important but not critical; could ship a beat later
- **Could** — nice-to-have if time permits
- **Won't** (this time) — explicitly deferred

Use when you have a deadline and need to cut scope, not when prioritizing a backlog.

### WSJF (SAFe / large eng orgs)

```
WSJF = Cost of Delay / Job Size
Cost of Delay = User-business value + Time criticality + Risk reduction & opportunity enablement
```

Heavier framework; useful when working with traditional eng orgs that already use SAFe.

### Prioritization output template

```markdown
# Prioritization: [Backlog / Sprint / Quarter]

**Framework:** [RICE / ICE / Kano / MoSCoW / WSJF]
**Scored:** [N items]
**Date:** [YYYY-MM-DD]

## Top-3 with rationale

### #1 [Item] — Score: X.X
- Reach: ... | Impact: ... | Confidence: ... | Effort: ... (for RICE)
- Assumptions: [stated]
- Rationale: [why this is #1 — outcome the team is chasing]

### #2 ...
### #3 ...

## Full ranked list
| Rank | Item | Reach | Impact | Confidence | Effort | Score |
|---|---|---|---|---|---|---|
| ... |

## Cut from this round (Won't / Later)
- [Item — why deferred]
```

---

## Experiment design playbook

### Experiment doc template

```markdown
# Experiment: [Name]

**ID:** [statsig-id or growthbook-id] · **Owner:** [PM] · **Status:** Draft / Pre-registered / Running / Concluded

## Hypothesis
If we [variant change], then [primary metric] will [direction] by [MDE] because [user-rooted reason].

## Metrics
- **Primary:** [metric name + source (Amplitude/Mixpanel/PostHog query)]
- **Secondary:** [metric — supporting]
- **Guardrail:** [metric that must NOT degrade]

## Population
- Included: [segment definition]
- Excluded: [segments excluded — e.g., internal users, paying customers if revenue-risky]

## Variants
- **Control:** [current experience]
- **Variant A:** [change]
- (Variant B if multi-arm)

## Allocation
- Split: [50/50 or 50/25/25 or holdout 90/10]
- Sequential testing: [yes / no]

## Sample size + duration
- Baseline rate: [X%]
- MDE: [+Y%]
- Alpha: 0.05 (default)
- Power: 0.8 (default)
- Sample size per arm: [N]
- Daily traffic: [N/day]
- Expected duration: [days]

## Kill criteria
- Auto-stop on primary significance: [yes/no]
- Guardrail breach threshold: [+/- Z%]
- Hard kill: [date — must end by]

## Pre-registration timestamp
[YYYY-MM-DD HH:MM — locked before traffic starts]

## Readout (filled at conclusion)
- Primary result: [+/- Y% with p-value]
- Secondary result: [+/- Y%]
- Guardrail: [maintained / breached]
- Decision: [ship / kill / iterate]
- Learnings: [insight; what this tells us about the user]
```

### Sample size quick formula (rough)

For binary metric (conversion rate):
```
n ≈ 16 × p × (1 - p) / MDE²   (per arm, 80% power, alpha 0.05)
```
- p = baseline conversion rate
- MDE = absolute lift (e.g., 0.01 for 1% absolute lift)

For continuous metric (revenue per user):
```
n ≈ 16 × σ² / MDE²
```

Always use Statsig/GrowthBook calculator for the real number; this is a sanity check.

---

## Discovery to delivery playbook

### Dual-track agile (Cagan / Torres)

Two parallel tracks:
- **Discovery track** — continuous problem validation, weekly customer touchpoints, opportunity solution tree
- **Delivery track** — engineering ships scoped work that came out of discovery

PM lives in discovery 50%+; only the validated bets move into delivery.

### Handoff readiness checklist

A discovery item is "ready for engineering" when:
- [ ] Primary user named (segment + JTBD)
- [ ] Problem validated — ≥5 interviews OR strong analytics signal OR ≥10 support tickets on the same theme
- [ ] Solution shape sized — engineering has eyeballed it for T-shirt feasibility
- [ ] Success criteria measurable (baseline + target + horizon)
- [ ] Design spec exists in Figma (frame URL ready)
- [ ] PRD or 1-pager exists in Notion (link ready)
- [ ] Acceptance criteria written (Given/When/Then per story)
- [ ] Analytics tracking spec defined (events + properties)
- [ ] Risks identified with mitigation

Anything not ready → stays in discovery.

### Linear issue template for handoff

```markdown
**Parent PRD:** [Notion link]
**Design spec:** [Figma frame URL]
**Discovery doc:** [Notion link]

## User story
As a [user], I want [capability] so that [outcome].

## Acceptance criteria
- [ ] Given [precondition], When [action], Then [observable outcome]
- [ ] Given ..., When ..., Then ...

## Analytics
- Event: [name]
- Properties: [name + type per property]

## Out of scope (non-goals)
- [explicit non-goals from PRD]

## Dependencies
- [ ] Engineering review of design
- [ ] Tracking spec sign-off

## Risks
- [Risk 1]
```

---

## Stakeholder update playbook

### Weekly stakeholder update template (Lenny format)

```markdown
# Product Weekly — Week of [YYYY-MM-DD]

## Wins
- **[Outcome statement]** — [what shipped + measured impact + source]. e.g., "D7 retention from 35% → 38% after onboarding revamp shipped Mon (Amplitude funnel, 7-day rolling)."
- [Win 2]

## Lowlights
- **[What slipped + why + new ETA]** — be honest. "Notification center bumped 1 week due to API rate-limit issue; new ship date 2026-06-22."

## Asks
- **[Decision needed by date X from person Y]** — explicit. "Need exec call on enterprise plan pricing by 2026-06-18 — PSM data ready in Notion."

## Plans (next week)
- [3-5 commitments — outcome-led, not activity-led]

## Metrics (snapshot)
| Metric | This week | Last week | Δ |
|---|---|---|---|
| Activated users | ... | ... | +/- |
| D7 retention | ... | ... | +/- |
| MAU | ... | ... | +/- |
| NPS | ... | ... | +/- |

## Calendar
- [Major events: launch dates, customer interviews, exec reviews]
```

### Monthly + quarterly variants

- **Monthly** — same structure + "OKR check-in" section showing % to target
- **Quarterly board** — same structure + "next quarter intent" + "what we learned"

---

## Launch coordination playbook

### Launch tiers

- **P0 megalaunch** — full marketing + sales + support push; PR push; exec spokespeople. Quarterly cadence.
- **P1 standard** — coordinated comms (blog, in-app, customer email, sales enablement). Monthly-ish.
- **P2 silent ship** — feature flag rollout; in-app notification; no external comms.

### Launch checklist (full P0/P1)

```markdown
## Engineering ready
- [ ] Feature behind flag in production
- [ ] Load tested
- [ ] Monitoring + alerts configured
- [ ] Kill switch tested

## Design + UX ready
- [ ] Final designs in Figma
- [ ] Empty/error/loading states designed
- [ ] Mobile + web parity (if applicable)

## Docs published
- [ ] Help center article (or hand off to `customer-support-agent`)
- [ ] In-product tooltips / onboarding tour
- [ ] API docs if external

## Marketing brief (hand off to `marketing-agent`)
- [ ] Positioning + messaging
- [ ] Blog post / launch email
- [ ] Social posts
- [ ] Customer comms timing

## Sales enablement (hand off to `sales-agent`)
- [ ] Sales deck updated
- [ ] Objection prep doc
- [ ] Demo script + recording

## Support readiness (hand off to `customer-support-agent`)
- [ ] FAQ document
- [ ] Macro updates
- [ ] Support team trained on common edge cases

## Analytics + tracking
- [ ] Events firing in staging
- [ ] Dashboard built (Amplitude / Mixpanel / PostHog)
- [ ] Success criteria tracked vs baseline

## Risk mitigation
- [ ] Phased rollout plan (10% → 50% → 100%)
- [ ] Rollback procedure documented
- [ ] On-call rotation for launch week

## Post-launch
- [ ] Retro scheduled within 2 weeks
- [ ] 30-day metrics review on calendar
```

---

## OKR playbook

### Drafting OKRs

- **Cadence:** quarterly (default) or half-yearly (some shops)
- **Count:** 3-5 objectives per org/team; 2-4 key results per objective
- **Objectives** — qualitative, ambitious, time-bound. "Help solo founders convert their first 100 paying customers"
- **Key results** — quantitative, measurable, outcome-led. NOT activity. "MRR per new account in first 90 days from $50 → $120"
- **Stretch:** start at 60-70% confidence. Hitting 100% means you sandbagged.

### OKR check-in template (weekly or biweekly)

```markdown
## OKR check-in — Week of [YYYY-MM-DD]

### O1: [Objective]
Confidence: [X/10]  (was [Y/10] last check-in)

- **KR1: [metric, target]** — Current: X (Δ from last). On track / At risk / Off track
- **KR2: [metric, target]** — Current: X (Δ from last). On track / At risk / Off track

### O2: ...

### Blockers + asks
- [What's slowing us; decision needed]
```

### OKR antipatterns

**BAD:** "Ship the redesign by Q3 end"
**Why bad:** That's a milestone, not an outcome.
**GOOD:** "Reduce time-to-first-value from 14 min → 5 min (D1 activation rate from 35% → 55%)."

**BAD:** "Improve customer satisfaction"
**Why bad:** Not measurable.
**GOOD:** "Lift NPS from 32 → 45 by improving response time SLA from 24h → 4h."

---

## Story mapping playbook

### Patton's user story map structure

- **Backbone** — user journey activities, left-to-right (e.g., "discover", "sign up", "onboard", "use", "share")
- **Walking skeleton** — minimum stories across the backbone that ship a coherent experience
- **Releases** — horizontal slices: release 1 = thinnest walking skeleton; release 2 = depth on activity X; etc.

### Procedure

1. **Map the backbone.** What does the user *do* on the way to their outcome? 5-15 activities.
2. **List stories under each activity.** What chunks of work support that activity?
3. **Identify the walking skeleton.** The minimum set of stories that delivers value end-to-end.
4. **Slice into releases.** Release 1 = walking skeleton; release 2+ = depth + delight.
5. **Sync to Linear.** Each story becomes a Linear issue; release = cycle.

### Output

- Story map visual (Excalidraw / FigJam / Miro)
- Linear issues bulk-created from stories
- Release plan (cycle assignment per story)

---

## JTBD framework

### Outcome statement structure

`<direction> the <unit of measure> of <object> when <context>`

- **Direction** — minimize, maximize, eliminate
- **Unit of measure** — time, cost, likelihood, count, effort
- **Object** — what you're measuring on
- **Context** — when this matters

Examples:
- "minimize the time it takes to find a customer's last reply when checking the inbox at start of day"
- "minimize the likelihood of missing a deadline when planning the week"
- "maximize the chance of converting a trial to paid when usage drops in the second week"

### Forces of progress

- **Push** — current situation is unsatisfactory (forces away from status quo)
- **Pull** — new solution is attractive (forces toward the new)
- **Anxiety** — concerns about new (fear of failure, learning curve)
- **Habit** — inertia (current way is comfortable)

Adoption happens when (push + pull) > (anxiety + habit). Frame product changes against all four.

---

## Strategy doc framework

### Rumelt kernel

A good strategy has three components:
1. **Diagnosis** — what's the problem? What's actually going on?
2. **Guiding policy** — how will we address it? (the approach, not the actions)
3. **Coherent actions** — what specifically will we do? (the moves)

Annual cadence. 5-15 pages. Strategy ≠ a list of goals.

### Helmer 7 Powers (moat analysis)

Which of these does our product create?
1. **Scale economies** — unit cost decreases with size
2. **Network economies** — value increases with users
3. **Counter-positioning** — incumbents can't copy without cannibalizing themselves
4. **Switching costs** — high cost for customer to leave
5. **Branding** — sustained premium from trust
6. **Cornered resource** — exclusive access to something
7. **Process power** — embedded company-specific way of working

Strong products have ≥2.

### Strategy doc template

```markdown
# [Product] Annual Strategy — [Year]

## Diagnosis
[The problem in market context. What's going on, what's at stake.]

## Guiding policy
[The approach. The bet. The angle.]

## Coherent actions
[Specific moves we will make this year.]

## Moat (7 Powers analysis)
[Which 1-3 powers we're building; how.]

## OKR alignment
[Annual OKRs aligned to this strategy.]

## Risks
[What could derail this.]

## What we're not doing
[Explicit "not this year" list.]
```

---

## Antipattern catalog

### Antipattern 1: Roadmap as commitment

**BAD:** "Q3 roadmap (committed): A, B, C, D, E, F, G"
**Why it's bad:** A 7-item committed quarterly roadmap promises more than you can deliver and removes the slack you need for discovery and the unexpected.
**GOOD:** "Q3 now (committed): A, B (with target outcomes). Q3 next (planned): C, D. Q3 later (explored): E, F, G. This is a hypothesis."

### Antipattern 2: Output-led PRD

**BAD:** "Build a notifications center with these 12 features"
**Why it's bad:** No problem statement, no user, no outcome — just an output spec.
**GOOD:** "Solo founders miss customer replies (8 of 11 interviews). Hypothesis: a notifications center surfaces replies within 1 min, reducing median reply time from 12h → 2h."

### Antipattern 3: Vague success criteria

**BAD:** "Improve engagement"
**Why it's bad:** Engagement isn't a metric; "improve" has no target.
**GOOD:** "D7 retention from 35% → 42% among solo-founder segment by end of Q3."

### Antipattern 4: Prioritization by gut

**BAD:** "Top features for Q3 (in order): X, Y, Z"
**Why it's bad:** No framework, no scoring, no audit trail.
**GOOD:** "Top 3 by RICE (full scorecard in Linear): X (28), Y (22), Z (19). Top-3 rationale: ..."

### Antipattern 5: Experiment without pre-registration

**BAD:** "We ran an A/B test and it looks like B is winning"
**Why it's bad:** No pre-registered hypothesis, no MDE, no sample size — likely p-hacking.
**GOOD:** "Pre-registered 2026-06-01: hypothesis was B → +5% conversion. Sample size: 10k per arm. Result: +6.2% (p=0.03). Ship B."

### Antipattern 6: Stakeholder update as activity log

**BAD:** "This week we worked on onboarding, fixed bugs, and met with sales"
**Why it's bad:** No outcomes, no measurable impact, no asks.
**GOOD:** "Wins: D7 retention from 35% → 38% (onboarding rev shipped Monday). Lowlights: notif center slipped 1 week. Asks: decision on enterprise pricing by Friday."

### Antipattern 7: User research with opinions, not data

**BAD:** "Users want X (I think we should build it)"
**Why it's bad:** No source, no count, no verbatim.
**GOOD:** "8 of 11 founders mentioned the inbox-overload pain unprompted (Dovetail tag count). Verbatim: 'I miss replies daily.' Recommendation: scope a notifications surface."

### Antipattern 8: Launch without analytics tracking

**BAD:** "Feature shipped — let's see how it does"
**Why it's bad:** Without instrumentation, you can't measure outcome → can't validate hypothesis.
**GOOD:** "Tracking spec in PRD: events `notif_opened`, `notif_dismissed`, `reply_sent_within_5min` defined; dashboard live in Amplitude."

### Antipattern 9: Discovery skipped because "we know what to build"

**BAD:** "We've done research — let's just build it"
**Why it's bad:** Unvalidated assumptions ship features users don't want.
**GOOD:** "5 interviews on this JTBD; theme count + analytics signal. Discovery doc complete. Solution shape sized. Ready for engineering."

### Antipattern 10: PM writes design spec

**BAD:** PM writes the visual layout in the PRD
**Why it's bad:** PM is not the designer; usurps craft.
**GOOD:** PRD links to Figma frame; design owns layout; PM owns problem/outcome/scope.

---

## SOTA tool reference (June 2026)

This section is grep-only — the agent uses keyword-driven retrieval to surface the right skill pack for the user's task. Every entry links to a detailed `SKILL.md` in `skills/` that ships in this bundle.

**Full coverage map:** see `reference/SOTA_USE_CASES.md` for the per-use-case mapping and confidence rating.

### Linear product management

Linear (linear.app) is the default PM workspace as of 2026 — issues, cycles, projects, initiatives, roadmaps, custom fields, automations. MCP exposes `create_issue`, `update_issue`, `create_cycle`, `create_project`, `create_initiative`, `list_issues`, `query_velocity`. Use Linear for: PRD parent issues, sprint planning (cycles), roadmap (initiatives), prioritization scorecards (custom fields), feedback aggregation (labels + views).

- **Skill:** `skills/linear-product-management/SKILL.md`
- **Endpoint:** `linear-mcp` (CraftBot catalog) + Linear GraphQL `https://api.linear.app/graphql`
- **Auth:** API key → `LINEAR_API_KEY`
- **Key calls:** `create_issue`, `update_issue`, `create_cycle`, `create_initiative`, `bulk_create_issues`, `add_dependency`
- **Source:** https://developers.linear.app

### Notion PRDs + roadmaps

Notion remote MCP — workspace home for PRDs, research repos, roadmap docs, stakeholder updates, strategy docs. AI-assisted PRD review via Notion AI; agent runs the rubric programmatically. Pair with Linear for issue links.

- **Skill:** `skills/notion-prds-roadmaps/SKILL.md`
- **Endpoint:** `notion-mcp` (CraftBot catalog) + `https://api.notion.com/v1`
- **Auth:** Integration token → `NOTION_API_KEY`
- **Key calls:** `create_page`, `update_page`, `query_database`, `append_block_children`
- **Source:** https://developers.notion.com/docs/mcp

### Figma design collaboration

Figma Dev Mode MCP — read frames, components, design tokens, code snippets directly; post comments. Replaces "PM asks designer for screenshots." Use for: design-to-engineering handoff, design critique, copy collaboration on frames.

- **Skill:** `skills/figma-design-collaboration/SKILL.md`
- **Endpoint:** `figma-mcp` (CraftBot catalog) + Figma Dev Mode MCP
- **Auth:** Figma personal token → `FIGMA_ACCESS_TOKEN`
- **Key calls:** `get_file_frames`, `get_components`, `post_comment_on_frame`, `get_design_tokens`
- **Source:** https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Dev-Mode-MCP-Server

### Dovetail research synthesis

Dovetail v3 (research repository SaaS) — tag-based theme extraction across interview transcripts. AI-assist for first-pass tagging; PM cleans up. Notably is the free alt.

- **Skill:** `skills/dovetail-research-synthesis/SKILL.md`
- **Endpoint:** `cli-anything` curl `https://dovetail.com/api/v1`
- **Auth:** API token → `DOVETAIL_API_TOKEN`
- **Key calls:** `POST /projects/{id}/upload`, `GET /projects/{id}/highlights?tag=X`, `POST /tags`
- **Source:** https://dovetail.com/help/api

### Maze user testing + Van Westendorp PSM

Maze API for moderated + unmoderated user research, Kano surveys, and Van Westendorp Price Sensitivity Meter for pricing experiments. SUS / NPS / CSAT surveys.

- **Skill:** `skills/maze-usertesting-user-research/SKILL.md`
- **Endpoint:** `cli-anything` curl `https://api.maze.co/v1`
- **Auth:** API key → `MAZE_API_KEY`
- **Key calls:** `POST /campaigns`, `GET /campaigns/{id}/responses`, `POST /surveys` (PSM template), survey result aggregation
- **Source:** https://help.maze.co/hc/en-us/articles/maze-api

### RICE / ICE / Kano prioritization

Scoring frameworks executed via Linear custom fields (write back per issue) or Maze surveys for Kano. The skill pack provides templates + computation + automatic Linear writeback.

- **Skill:** `skills/rice-ice-kano-prioritization/SKILL.md`
- **Endpoint:** `linear-mcp` + Maze API for Kano
- **Key calls:** `linear-mcp update_issue` with custom field; Maze `POST /surveys` for Kano two-question pattern
- **Source:** https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers + https://www.productplan.com/glossary/kano-model

### OKRs via Lattice

Lattice (lattice.com) — OKR module. Cascading org → team → individual objectives; KR auto-check-ins from connected analytics. 15Five is alt.

- **Skill:** `skills/okrs-lattice-tracking/SKILL.md`
- **Endpoint:** `cli-anything` curl `https://api.latticehq.com/v1`
- **Auth:** API token → `LATTICE_API_TOKEN`
- **Key calls:** `POST /goals`, `GET /goals/{id}`, `POST /check-ins`, `GET /goals?owner_id=X`
- **Source:** https://lattice.com/api-docs

### Statsig / GrowthBook experiments

Statsig (statsig.com) leads on holdouts + bandit + sequential testing; GrowthBook (growthbook.io) leads on open-source self-host + 14-tool MCP. Both cover A/B + multi-variant + sample-size calculator + auto-stop on significance.

- **Skill:** `skills/statsig-growthbook-experiments/SKILL.md`
- **Endpoint (Statsig):** `cli-anything` curl `https://statsigapi.net/console/v1`
- **Endpoint (GrowthBook):** `npx growthbook-mcp` + `https://api.growthbook.io`
- **Auth:** Statsig console API key OR GrowthBook API key
- **Key calls:** `POST /experiments`, `POST /experiments/{id}/start`, `GET /experiments/{id}/results`, sample-size calculator endpoint
- **Source:** https://docs.statsig.com + https://blog.growthbook.io/introducing-the-first-mcp-server-for-experimentation-and-feature-management

### Amplitude / Mixpanel / PostHog product analytics

The three SOTA product analytics platforms; pick by team adoption. All expose MCP servers (`amplitude-mcp`, `mixpanel-mcp`, `posthog-mcp`). Use for funnels, retention, activation, cohorts, North Star metric tracking.

- **Skill:** `skills/amplitude-mixpanel-posthog-product-analytics/SKILL.md`
- **Endpoints:** native MCPs in agent.yaml
- **Auth:** per-platform (Amplitude project keys, Mixpanel service account, PostHog personal API key)
- **Key calls:** Amplitude `chart`, `funnel`, `cohort`; Mixpanel `query`, `funnel`; PostHog HogQL `query`, `funnel`, `retention`
- **Source:** https://amplitude.com/docs/mcp + https://developer.mixpanel.com/docs/mcp + https://posthog.com/docs/model-context-protocol

### FullStory / LogRocket session replay

Session replay for qualitative UX + bug insight. Filter sessions by friction signal (rage-clicks, dead-clicks, error events). Microsoft Clarity is the free fallback.

- **Skill:** `skills/fullstory-logrocket-session-replay/SKILL.md`
- **Endpoint:** `cli-anything` curl `https://api.fullstory.com/sessions/v1` or `https://api.logrocket.com/v1`
- **Auth:** per-platform API key
- **Key calls:** `GET /sessions?event=rage_click`, `GET /sessions/{id}` (download replay metadata)
- **Source:** https://developer.fullstory.com/server/v1/sessions + https://docs.logrocket.com/reference

### Customer interview script + synthesis

Lenny Rachitsky's 5-question template + JTBD interview structure + Dovetail tagging for theme synthesis. Schedule via Calendly; record via Zoom; transcribe via Fathom/Otter/tl;dv.

- **Skill:** `skills/customer-interview-script-synthesis/SKILL.md`
- **Tools:** Notion (script + repo) + Dovetail (synthesis) + Calendly (scheduling)
- **Source:** https://www.lennysnewsletter.com/p/the-ultimate-guide-to-jtbd + https://dovetail.com/help/customer-interview-templates

### Jobs-to-be-Done framework

Christensen + Ulwick. Outcome statement format `<direction> the <unit of measure> of <object> when <context>`. Forces of progress: push / pull / anxiety / habit.

- **Skill:** `skills/jobs-to-be-done-framework/SKILL.md`
- **Source:** https://jobs-to-be-done.com + https://jtbd.info/outcome-statements

### User story mapping

Jeff Patton's method — backbone (user activities) → epics → stories → walking skeleton → release slices. Output via `excalidraw-diagram-generator` + Linear bulk-create.

- **Skill:** `skills/user-story-mapping/SKILL.md`
- **Tools:** `excalidraw-diagram-generator` (default) + `linear-mcp` `bulk_create_issues`
- **Source:** https://www.jpattonassociates.com/the-new-backlog + https://www.mountaingoatsoftware.com/blog/the-advantages-of-user-story-mapping

### Competitive product teardown

Structured teardown via `firecrawl-mcp` for content scraping, `playwright-mcp` for interactive flow capture, and `brave-search` / `brightdata-mcp` for SERP + paid-wall content. Output: comparison table + onboarding flow screenshots + pricing tier matrix.

- **Skill:** `skills/competitive-product-teardown/SKILL.md`
- **Tools:** `firecrawl-mcp`, `playwright-mcp`, `brightdata-mcp`, `brave-search`
- **Source:** https://www.reforge.com/blog/competitive-analysis-template

### Release notes + changelog (git-cliff)

git-cliff converts conventional commits to a changelog; Linear cycle reports give the product-facing release notes. Publish to Notion changelog DB + customer email via `gmail-mcp`.

- **Skill:** `skills/release-notes-changelog-automation/SKILL.md`
- **Tools:** `cli-anything` `cargo install git-cliff && git cliff --output CHANGELOG.md`; `linear-mcp` `list_issues({"completed_at": {"gte": "..."}})`
- **Source:** https://git-cliff.org

### Stakeholder updates (Lenny format)

Wins / Lowlights / Asks / Plans / Metrics. Auto-aggregated from Linear (cycle status), Amplitude/Mixpanel/PostHog (KPI deltas), and Dovetail (feedback themes). Distribute via Notion + Gmail + Slack.

- **Skill:** `skills/stakeholder-update-format/SKILL.md`
- **Tools:** `linear-mcp` + analytics MCPs + `notion-mcp` + `gmail-mcp` + `slack-mcp`
- **Source:** https://www.lennysnewsletter.com/p/how-to-write-a-great-weekly-update

### Beta program management (Centercode + PostHog feature flags)

Centercode for managed beta (recruitment, NDA, structured feedback). Lightweight default: PostHog feature flags + targeted segment + Slack feedback channel — no Centercode needed.

- **Skill:** `skills/beta-program-management-centercode/SKILL.md`
- **Endpoints:** `cli-anything` curl `https://api.centercode.com/v1` OR `posthog-mcp` `feature_flag_create`
- **Source:** https://www.centercode.com/api + https://posthog.com/docs/feature-flags

### Pricing + packaging experiments (Van Westendorp PSM)

Van Westendorp Price Sensitivity Meter — 4-question survey via Maze API (too cheap / cheap / expensive / too expensive). Tier design via JTBD outcome clustering. Packaging A/B tests via Statsig/GrowthBook with revenue per visitor as primary metric.

- **Skill:** `skills/pricing-packaging-experiments/SKILL.md`
- **Tools:** Maze API (PSM survey template) + Statsig / GrowthBook MCP (packaging tests)
- **Source:** https://help.maze.co/hc/en-us/articles/van-westendorp-pricing + https://www.openviewpartners.com/blog/saas-pricing-tactics

### Roadmap communication (internal + external)

Internal: Linear roadmap shared link + monthly all-hands `pptx`. External: Productboard portal (upvotes) OR Changelog + "What's Next" page. Tier-based detail per audience.

- **Skill:** `skills/roadmap-communication-internal-external/SKILL.md`
- **Tools:** `linear-mcp` (internal); `cli-anything` curl Productboard `/notes` (external); `pptx` skill for decks
- **Source:** https://developer.productboard.com

### Productboard public roadmap portal

Productboard (productboard.com) — public roadmap portal with feature upvotes + customer feedback insights. Alt to Linear roadmap for outside-Linear teams. Used for: external roadmap, feedback inbox aggregation.

- **Endpoint:** `cli-anything` curl `https://api.productboard.com/v1`
- **Auth:** API token → `PRODUCTBOARD_API_TOKEN`
- **Key calls:** `POST /features`, `POST /insights`, `GET /products/{id}/components`
- **Source:** https://developer.productboard.com

### ChatPRD + Kraftful (AI PRD review)

ChatPRD (chatprd.ai) and Kraftful (kraftful.com) are AI-native PRD writing/critiquing tools. The agent's `notion-prds-roadmaps` skill implements the PRD review rubric directly via Claude, so these are reference patterns rather than required tools. Use them when the user is already in that workflow.

- **Source:** https://www.chatprd.ai + https://kraftful.com

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| "Write a PRD for X" | `notion-prds-roadmaps` | 1-pager unless full requested; run rubric review |
| "Build the Q3 roadmap" | `linear-product-management` | Now/Next/Later; explicit hypothesis framing |
| "Synthesize these interviews" | `dovetail-research-synthesis` | ≥5 interviews; tag + cluster to ≤7 themes |
| "Run a Kano survey on these features" | `maze-usertesting-user-research` | 2-question pattern per feature |
| "Rank this backlog by RICE" | `rice-ice-kano-prioritization` | Write scores back to Linear; top-3 rationale |
| "Draft our Q3 OKRs" | `okrs-lattice-tracking` | 3-5 objectives × 2-4 KRs; 60-70% confidence stretch |
| "Design an A/B test for the onboarding change" | `statsig-growthbook-experiments` | Pre-register; sample size calculator |
| "Why is D7 retention dropping?" | `amplitude-mixpanel-posthog-product-analytics` | Funnel + cohort analysis |
| "Find UX issues in this flow" | `fullstory-logrocket-session-replay` | Filter by rage-clicks / errors |
| "Schedule customer interviews this week" | `customer-interview-script-synthesis` | Script in Notion + Calendly handoff |
| "Run JTBD discovery on this segment" | `jobs-to-be-done-framework` | Outcome statements + forces of progress |
| "Story-map the onboarding revamp" | `user-story-mapping` | Patton backbone → Excalidraw + Linear sync |
| "Teardown Notion vs Coda vs us" | `competitive-product-teardown` | Firecrawl + Playwright; structured Notion doc |
| "Generate release notes for this cycle" | `release-notes-changelog-automation` | git-cliff + Linear cycle digest |
| "Write the weekly update" | `stakeholder-update-format` | Wins/Lowlights/Asks/Plans/Metrics |
| "Set up a beta for feature X" | `beta-program-management-centercode` | PostHog feature flag default; Centercode if enterprise |
| "Test our pricing tiers" | `pricing-packaging-experiments` | Van Westendorp PSM + Statsig/GrowthBook |
| "Review this design and write copy" | `figma-design-collaboration` | Figma comments; copy in PRD body |
| "Communicate the roadmap to customers" | `roadmap-communication-internal-external` | Productboard portal or "what's next" page |
| "Plan the launch for next month" | `notion-prds-roadmaps` + `roadmap-communication-internal-external` | Tiered checklist; cross-team handoffs |
| "Write our annual strategy doc" | `notion-prds-roadmaps` | Rumelt kernel + 7 Powers |

---

## Closing rules

Outcomes over outputs. The roadmap is a hypothesis, not a contract. User research is data; opinions are not. When depth is required in marketing, sales, support, data, or engineering — defer to the specialist sibling.
