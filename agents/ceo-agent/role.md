# CEO Agent — deep reference

This appends to `AGENT.md`. **Not** in the agent's default context. Grep when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "Strategy doc playbook", "Board pack playbook", "Investor update playbook", "Executive hiring playbook", "OKR cascade playbook", "Decision frameworks playbook", "All-hands playbook", "QBR playbook", "Annual planning playbook", "Calendar audit playbook", "KPI dashboard playbook", "Crisis comms playbook", "M&A framework playbook", "Operating cadence playbook", "Sibling agent hand-off matrix", "SOTA tool reference", "Strategy doc template", "Board pack template", "Investor update template", "Outcomes scorecard template", "Decision journal entry template", "QBR template", "Operating rhythm template", "Antipattern catalog".

For provenance, see `SOURCES.md`.

---

## Capability reference

### Strategy frameworks this agent uses

- **Rumelt kernel** — diagnosis / guiding policy / coherent actions (the spine)
- **OGSM** — objectives / goals / strategies / measures (operating format)
- **V2MOM** (Salesforce) — vision / values / methods / obstacles / measures (operating format)
- **Wardley Mapping** — value chain × evolution (genesis → custom → product → commodity) for landscape + gameplays
- **Porter's 5 Forces** — industry structural analysis (when M&A or repositioning is on the table)
- **Blue Ocean** — value innovation / strategy canvas / four-actions framework (when defending margins)
- **Jobs-to-be-Done** — for product strategy framing (deeper depth: hand to `product-manager`)
- **Hamilton Helmer 7 Powers** — moat analysis (scale / network / brand / IP / switching / cornered / counter-positioning)
- **AARRR (Pirate Metrics)** — Acquisition / Activation / Retention / Referral / Revenue (for growth strategy)
- **Christensen Disruption** — sustaining vs disruptive innovation framing

### Decision frameworks this agent uses

- **DACI** (Atlassian) — Driver / Approver / Contributors / Informed (single Approver — load-bearing). Strategic decisions.
- **RACI** — Responsible / Accountable / Consulted / Informed. Execution tasks.
- **DRI** (Apple) — Directly Responsible Individual. Cross-functional initiatives.
- **RAPID** (Bain) — Recommend / Agree / Perform / Input / Decide. Legacy alternative to DACI.
- **Decision journal** (Annie Duke) — date / decision / alternatives / chosen / confidence / kill-criteria / review-date.
- **Pre-mortem** (Gary Klein) — assume the project failed, list why. ~30% better risk identification per Wharton study.
- **2-way door vs 1-way door** (Bezos) — reversibility-based decision speed sorting.
- **Eisenhower matrix** — urgent / important sorting for CEO calendar audits.

### Capital allocation frameworks

- **DCF (discounted cash flow)** — for M&A targets, capital investment
- **NPV / IRR** — investment ranking
- **Payback period** — for paid-acquisition decisions and capital investments
- **Real options** — for staged investment decisions under uncertainty
- **LTV:CAC** — for paid-growth allocation (defer ratio depth to `growth-agent`)

### Board governance references

- **NVCA Model Legal Documents** — Series Seed / Series A model docs (free, lawyer-vetted)
- **Cooley GO Board templates** — board consent, written consents, board minutes
- **Sequoia Pitch Deck template** — for board updates and fundraising
- **Carta governance docs** — for cap table + 409A integration

### Industries/contexts this agent calibrates for

- **SaaS / B2B subscription** — primary calibration (most VC-backed companies)
- **Consumer / DTC** — secondary (different metric stack — D2C-specific GM, CAC by channel)
- **Marketplace** — two-sided dynamics, take-rate strategy
- **Hardware / deeptech** — long product cycles, capital-intensive
- **Fintech / regtech** — regulated environments (defer regulatory to `legal-counsel`)
- **Healthtech** — regulated environments (defer to `legal-counsel`)

---

## Sibling agent hand-off matrix

| User asks for | Defer to | What you do first |
|---|---|---|
| PRD, roadmap, RICE prioritization, user research, A/B design | `product-manager` | Confirm strategic priority + DRI; pass to PM |
| Positioning, brand voice, campaigns, social, SEO, email lifecycle, ads | `marketing-agent` | Confirm objective + budget + audience; pass to marketer |
| Sales pipeline, playbook, demos, sales hiring depth, comp design | `sales-agent` | Confirm ICP + pipeline targets; pass to sales |
| Bookkeeping, AR/AP, monthly close, audit prep | `finance-controller` | Confirm scope + close date; pass to controller |
| Fundraising mechanics, scenario modeling depth, captable mechanics | `finance-agent` | Confirm round size + target investor list; pass to finance |
| Term sheets, employment law, IP, M&A docs, regulatory | `legal-counsel` | Frame the question; recommend legal as binding answer |
| Hiring + vendor ops, HR ops, comp banding, benefits admin | `operations-agent` | Confirm role + level; pass to ops |
| Customer issues, support playbook, CSAT improvement | `customer-support-agent` | Frame impact + urgency; pass to support |
| Activation experiments, retention work, growth loops | `growth-agent` | Confirm hypothesis + metric; pass to growth |
| Warehouse analytics, dbt models, cohort SQL | `data-analyst` | Confirm KPI definition; pass to analyst |
| Video production (script + edit + render) | `video-creator` | Confirm format + platform; pass to video |
| Technical documentation, ADRs, API docs | `technical-writer` | Confirm audience + depth; pass to writer |
| Python engineering, code review, debugging | `senior-python-engineer` | Frame the eng problem; pass to engineer |

---

## Strategy doc playbook

### Rumelt kernel — the 3-question test

A strategy is valid if and only if all three answer "yes":

1. **Is the diagnosis named and unflinching?** What's the actual challenge? Not "competition is fierce" — "we're losing 40% of trials at Day 2 because activation is broken." Specificity. Discomfort. No fluff.
2. **Is the guiding policy a real choice?** Excludes alternatives. Says no to as much as it says yes to. "Focus on enterprise" implies declining SMB; "speed over completeness" implies declining quality bar in v1.
3. **Are the actions coherent and resourced?** Mutually reinforcing. People-and-budget-mapped. Sequenced. Not a list of unrelated initiatives.

If any answer is "no" → that's **bad strategy** (Rumelt's term). Don't ship. Send it back for diagnosis.

### Bad-strategy checklist (Rumelt's four signatures)

1. **Fluff** — vague abstractions ("synergize value across the ecosystem") masquerading as insight
2. **Failure to face the challenge** — declaring goals without naming what's hard
3. **Mistaking goals for strategy** — "grow to $100M ARR" is a goal, not a strategy
4. **Bad strategic objectives** — too many, disconnected, or impossible to resource

### Strategy doc template

```markdown
# [Company] Strategy — [Period, e.g., FY2026]

## 1. Diagnosis
What's the challenge? What changed? What's the data?
- [Specific, unflinching, evidence-cited]

## 2. Guiding policy
The choice we're making. What we're saying YES to. What we're saying NO to.
- YES: [...]
- NO: [...]

## 3. Coherent actions
Mutually reinforcing initiatives, sequenced and resourced.

| Initiative | Owner | KR | Resources | Sequence | Kill criteria |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

## 4. OGSM (operating format)
| Objective | Goal (measurable) | Strategy | Measure |
|---|---|---|---|
| ... | ... | ... | ... |

## 5. Risks + mitigations
| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|

## 6. Bad-strategy checklist
- [ ] No fluff
- [ ] Challenge named
- [ ] Goals not confused with strategy
- [ ] Objectives focused + resourced
```

### V2MOM (Salesforce) format — alternative operating spine

```markdown
- **Vision** — what we want to achieve (1-2 sentences)
- **Values** — what's important in pursuing it (3-5)
- **Methods** — how we're going to get there (5-8 actions)
- **Obstacles** — what's in the way (3-5)
- **Measures** — how we'll know we succeeded (3-5)
```

---

## Wardley mapping playbook

### The map

- **Y axis (value chain)** — visible (user need) → invisible (commodity infrastructure)
- **X axis (evolution)** — Genesis → Custom Built → Product (+rental) → Commodity (+utility)
- **Components** — boxes at intersections
- **Dependencies** — arrows from user down through value chain
- **Inertia** — circles marking components likely to resist evolution
- **Anchors** — user needs at the top

### Build vs buy vs partner gameplay

- **Genesis / Custom Built** — build (no one else has it)
- **Product** — partner (off-the-shelf exists; differentiation isn't here)
- **Commodity** — buy (rent the utility — AWS, Stripe, Twilio)

### OnlineWardleyMaps text syntax (free, public)

```
title Example map
anchor User [0.99, 0.5]
component Authentication [0.85, 0.85]
component Email service [0.6, 0.92]
component Compute [0.4, 0.95]
User -> Authentication
Authentication -> Email service
Authentication -> Compute
```

Render via `https://onlinewardleymaps.com` (paste syntax, export PNG/SVG).

---

## Board pack playbook

### Sequoia/NVCA-style 12-slide template

1. **Cover** — company / date / period
2. **Mission + this-period summary** — 3-bullet TL;DR
3. **KPIs** — north star + 4-5 supporting (with trend lines)
4. **Financials** — revenue / gross margin / burn / runway
5. **Cash + capital plan** — current cash, monthly burn, runway months, next round timing
6. **Hiring** — current headcount, plan, key opens, recent hires/departures
7. **Wins** — 3-5 since last meeting
8. **Lowlights** — 2-3 honest items (board values honesty over polish)
9. **Strategy update** — what changed, what's the gameplay
10. **Asks** — specific, named (intros, hires, advice, capital)
11. **Risks + mitigations** — top 3-5
12. **Appendix** — detail tables, methodology notes

### Pre-read memo (3-5 pages)

- Sent 48-72h ahead with: *"Please read before — we'll spend the meeting on decisions, not slides."*
- Narrative format, not bullets-everywhere
- TL;DR / Where we are / What changed / What we're deciding / Asks

### Minutes capture

- AI notetaker (Granola / Fathom / Fireflies) records
- Agent extracts: decisions made / action items / owners / due dates
- Decisions → Notion decision log; actions → Linear issues
- Minutes published within 48h
- Distributed to board via `gmail-mcp` + portal upload (manual on startup-tier portals)

### Board composition by stage

| Stage | Typical board | Independents | Committees |
|---|---|---|---|
| Pre-seed / Seed | 3 (founder + lead investor + independent) | 1 | None |
| Series A | 5 (2 founders + 2 investors + 1 independent) | 1-2 | Audit (informal) |
| Series B+ | 5-7 (founders + investors + 2-3 independents) | 2-3 | Audit, Comp, Nominating |
| Pre-IPO | 7-9 (mostly independents) | 4+ | Audit, Comp, Nominating, Risk |

### Independent director sourcing

- **Bolster** (bolster.com) — fractional + interim + independent
- **The Board List** (theboardlist.com) — women + diverse independent directors
- **True Search** — retained for senior independents
- **Personal networks** — LP intros, advisor → director conversion

---

## Investor update playbook

### Visible.vc format (monthly default)

```markdown
# [Company] — Investor Update — [Month YYYY]

## TL;DR
One paragraph: where we are, what changed, the ask.

## Key metrics
| Metric | This month | Last month | % change | Target |
|---|---|---|---|---|
| MRR / Revenue | | | | |
| Customers / Users | | | | |
| Cash | | | | |
| Runway (months) | | | | |
| North star metric | | | | |

## Wins
- 3-5 since last update

## Lowlights
- 2-3 honest items (investors value candor)

## What's next (next 30 days)
- Focus areas
- Hires we're making
- Decisions we're forcing

## Asks
- Specific intros: [name, why]
- Advice on: [topic]
- Other: [...]

## Cash + runway
- Current cash: $XXX
- Monthly burn: $XXX
- Runway: XX months
- Next round: [timing / target]
```

### Cadence and engagement

- **Monthly** for pre-Series B (investors expect this; missing = signal of trouble)
- **Quarterly** for Series B+ (with monthly KPI-only ping)
- **Engagement tracking** — Visible tracks opens, page time. Low engagement on lowlights = investor is checked out (act on this).

### Tooling stack 2026

- **Visible.vc** — default (auto KPI sync from analytics + Carta/Pulley integration)
- **AngelList Stack Updates** — free fallback
- **Carta Investor Reporting** — for Carta-using cap tables
- **DocSend** — tracked-link distribution

---

## Executive hiring playbook

### Outcomes-first scorecard (NOT a JD)

A JD lists tasks. A scorecard lists what they own in 12 months. Geoff Smart "Who" / topgrading method.

```markdown
# [Role] Scorecard

## Mission
One sentence: why this role exists.

## Outcomes (5-7 in 12 months)
1. [Specific, measurable, owned outcome — e.g., "Hit $5M ARR by EOY"]
2. ...

## Competencies (5-7)
- [Competency 1 — what they need to be world-class at]
- ...

## Cultural fit
- [Values alignment specifics]

## Compensation
- Base: $XXX-XXX
- Equity: X.X% - X.X%
- Variable: [if applicable]

## Reporting
- Reports to: [CEO / other]
- Direct reports: [#]
- Cross-functional: [...]
```

### Interview stage gate

1. **Phone screen** (30 min) — outcomes-fit check, comp alignment, motivation
2. **Outcomes-scorecard interview** (60 min) — walk through each outcome, ask "tell me about a time you did this"
3. **Working session** (90 min) — present a real problem, watch them think
4. **Reference checks** (3-5 by 360 — peers + reports + manager — NOT the candidate's curated list)
5. **C-level: deep references** via retained search (True Search / SPMB / Heidrick & Struggles)
6. **Final decision** — DACI with CEO as Approver for VP+, board chair Informed for C-level

### Topgrading reference call template

```markdown
1. How do you know [candidate]?
2. What were their 3 biggest strengths in that role?
3. What were their 3 biggest weaknesses?
4. How would you rate them as a [role] on a 1-10? Why?
5. Would you hire them again — yes or no? Why?
6. Who else should I talk to who worked closely with them?
```

### Comp benchmarks (Series A SaaS, 2026 ranges — verify per role)

| Role | Base | Equity | Bonus |
|---|---|---|---|
| VP Eng | $260-330k | 0.5-1.5% | 10-20% |
| VP Product | $240-300k | 0.5-1.5% | 10-20% |
| VP Sales | $220-280k OTE 50/50 | 0.5-1.5% | OTE-based |
| VP Marketing | $200-260k | 0.5-1.0% | 10-20% |
| Head of People | $180-230k | 0.25-0.75% | 10-15% |
| CFO | $250-320k | 0.5-1.5% | 15-25% |

Sources: Pave, Carta Total Comp, Option Impact. Verify with current data — these shift quarterly.

---

## OKR cascade playbook

### Christina Wodtke radical focus

- **ONE objective per team per quarter** (aspirational, qualitative)
- **THREE key results** (measurable, time-bound, leading-indicator-preferred)
- **Confidence dial** (1-10) reviewed weekly — below 5 = surface in QBR
- **Score at quarter end** — 0.0-1.0 per KR; aggregate per O
- **Carry-over rule** — don't roll incomplete OKRs forward by default; re-justify

### Cascade

- Company → Team → Individual (NOT paste-and-replicate)
- Each level's OKRs justify how they roll up
- Cross-functional OKRs need a DRI (single owner)

### Auto-check-in mechanism

| KR type | Auto-source |
|---|---|
| Revenue / MRR | `stripe-mcp` |
| Cash / runway | `xero-mcp` |
| Product engagement | `posthog-mcp` / `amplitude-mcp` / `mixpanel-mcp` |
| Pipeline | Sales CRM (Salesforce/HubSpot API via `cli-anything`) |
| Hiring | Ashby / Greenhouse API |
| Customer NPS | Survey tool API |

### OKR doc template

```markdown
# [Team] OKRs — [Quarter]

## Objective
[Aspirational, qualitative, time-bound]

## Key Results
| KR | Owner | Source | Baseline | Target | Stretch | Confidence |
|---|---|---|---|---|---|---|
| KR1 | ... | ... | ... | ... | ... | X/10 |

## Why these
[1-2 sentences on how this rolls up to company OKR]

## Weekly check-in
- Confidence trend
- Blockers
- Asks
```

---

## Decision frameworks playbook

### DACI vs RACI vs DRI — when to use which

| Framework | Use for | Key role |
|---|---|---|
| DACI | Strategic decisions | Single Approver (load-bearing) |
| RACI | Execution / task ownership | Accountable (single) per task |
| DRI | Cross-functional initiative | Directly Responsible Individual (Apple model) |
| RAPID | Legacy alt to DACI | Decide |

### DACI template

```markdown
# Decision: [Title]

## Driver
[Name — corrals stakeholders, brings the recommendation, owns the deadline]

## Approver
[ONE name — makes the decision]

## Contributors
- [Name — what subject-area input]
- ...

## Informed
- [Name — needs to know after]

## Recommendation
[Driver's recommendation, with reasoning]

## Alternatives considered
- Option A: [pro/con]
- Option B: [pro/con]
- ...

## Decision due
[Date]

## Decision made
[Date / Outcome / Approver signature]

## Kill criteria
[Conditions under which we reverse this decision]
```

### Decision journal entry (Annie Duke)

```markdown
# Decision Journal: [Title]

## Date
YYYY-MM-DD

## Decision
[1-sentence summary]

## Context
[Situation, constraints, who's involved]

## Alternatives considered
- A: [option]
- B: [option]
- C: [chosen]

## Why this option
[Reasoning, evidence, model]

## Confidence
[1-10]

## Expected outcome
[What good looks like 3, 6, 12 months out]

## Kill criteria
[Conditions to reverse]

## Review date
[YYYY-MM-DD — calendar set]

## Outcome (filled at review)
[What actually happened, what we learned]
```

### Pre-mortem facilitation script (Gary Klein, 30-min meeting)

1. **Frame** (3 min) — "Assume the decision is made and 12 months from now, the project failed catastrophically. We're at the funeral."
2. **Silent brainstorm** (10 min) — each participant writes reasons for failure
3. **Round-robin share** (10 min) — go around, one reason at a time, no debate
4. **Cluster + prioritize** (5 min) — group similar reasons, identify top 5 risks
5. **Mitigation assignment** (2 min) — each top-5 risk gets an owner + mitigation due-date

---

## All-hands playbook

### Weekly format (30 min)

- **Pre-read** in Notion 24h ahead — 1-pager: metrics + wins + asks
- **Live**: 10 min metrics review, 10 min wins + shoutouts, 10 min Q&A
- **Deck**: 5-8 slides via Gamma Generate API or Beautiful.ai (PPT compat)
- **Recap** in Slack within 4h, Loom/Tella recording for absentees
- **Cadence**: same day, same time, every week

### Monthly format (60 min)

- **Pre-read** 24-48h ahead — 2-3 pager with theme
- **Live**: 15 min theme presentation, 15 min new-hire intros, 15 min product/customer story, 15 min Q&A
- **Deck**: 12-15 slides
- **Recap** with action items in Linear

### Lenny Rachitsky weekly-update format (also for all-hands narration)

- **Wins** — 3-5
- **Lowlights** — 2-3 honest
- **Asks** — specific, named
- **Plans** — next-period focus
- **Metrics** — key trends

---

## QBR playbook

### The 5-component template (60 min)

```markdown
1. Strategic Scorecard Snapshot (15 min)
   - North star + 4-5 KPIs vs target
   - Color-coded (green / amber / red)

2. Exception Report (15 min)
   - What's red — why — what's the recovery plan
   - What's been green long enough to consider stretch
   
3. Initiative Portfolio Review (15 min)
   - Status per top-5 initiatives (DRI / KR / risk)
   
4. Forward Look (5 min)
   - Next quarter priorities + capital allocation shifts
   
5. Decision Log (10 min)
   - What did we decide?
   - Who owns each?
   - When do we review?
```

### The 60% rule

60% of meeting time on **decisions**, not status. If you're not deciding, you're updating — and updates belong in the pre-read.

### Pre-read

- 5-8 pages, clean design (not 40 slides)
- Sent 48h ahead with: *"Read before — we'll discuss decisions, not present"*
- Decisions to be made are listed up front

---

## Annual planning playbook

### David Sacks cadence model

| Cadence | Focus |
|---|---|
| Annual | Strategy + capital + hiring plan |
| Quarterly | OKR setting + priority reset + QBR |
| Monthly | Roadmap + forecast + budget variances |
| Weekly | Metrics + unblock + 1:1s |

### Pre-work (2 weeks ahead)

1. **Pre-mortem on prior year** — what didn't work, why
2. **Wardley map refresh** — what's evolved, where's the gameplay
3. **Bottom-up team plans** — each team submits 1-page plan with their proposed OKRs
4. **Capital plan refresh** — runway, next round timing, hiring constraints
5. **Risk register update** — top 10 risks + mitigations

### 2-day offsite agenda

**Day 1 — Diagnosis + Ambition**
- 9:00 — Review pre-mortem learnings
- 10:30 — Wardley map walk-through
- 13:00 — Diagnosis exercise (what's the challenge for next year)
- 15:00 — Ambition exercise (what's the big bet)
- 17:00 — Day 1 synthesis

**Day 2 — Focus + OKRs**
- 9:00 — Strategic policy (yes / no choices)
- 11:00 — OKR drafting (company → team)
- 13:00 — Hiring plan + capital plan
- 15:00 — Risk register + kill criteria
- 16:00 — Operating rhythm calendar lock
- 17:00 — Commitment + share-out plan

### 8-section annual plan template

1. **Diagnosis** — what's the challenge
2. **Ambition** — where we're going
3. **Focus** — what we say yes/no to
4. **OKRs** — company → team cascade
5. **Hiring plan** — roles, timing, budget
6. **Capital plan** — runway, next round, scenarios
7. **Risk register** — top 10 + mitigations + owners
8. **Kill criteria** — what would force a strategy pivot

---

## Calendar audit playbook

### 30-day audit checklist

- [ ] Total meetings: # per week (target < 25 for solo founder, < 35 with leadership team)
- [ ] Focus-time ratio: contiguous ≥90-min blocks / total working hours (target ≥30%)
- [ ] 1:1 ratio: # of 1:1s / # of total meetings (target 25-40%)
- [ ] Recurring meeting count: # set up >6 months ago (kill candidates if no explicit value)
- [ ] No-meeting day: defended? (target 1 day/week)
- [ ] Meeting length default: 25/50 min (NOT 30/60 — Parkinson's law)
- [ ] Travel + commute: # hours/week (audit if >5h)
- [ ] Energy alignment: hardest work in personal-peak hours? (audit via self-report)

### Rules to apply

1. **Default decline.** If you don't know why you're invited, decline + ask for context.
2. **Kill recurring meetings >6mo without explicit value.** Re-justify or kill.
3. **No back-to-back >3.** Buffer 5-10 min.
4. **No meetings before [time].** Defend morning deep work (or evening if night-owl CEO).
5. **One no-meeting day per week.** Defend ruthlessly.
6. **25/50 min defaults, not 30/60.** Recover the buffer.
7. **Block 4h+ deep work weekly for strategy.** Calendar marks it as busy.
8. **Travel + commute counted as work time.** Don't double-book yourself.

### Tooling

| CEO style | Pick |
|---|---|
| Heavy meeting load (20+/wk), wants auto-rebuild | Motion |
| Wants focus-time + habit defense | Reclaim |
| Reflective planner, morning-ritual | Sunsama |
| Command-bar power user pulling tasks from everywhere | Akiflow |
| Unified calendar + tasks | Morgen |

**Note: Clockwise shut down March 2026 (Salesforce acquisition).**

---

## KPI dashboard playbook

### Hierarchy

```
North star metric (ONE)
  ├── Supporting KPI 1 — e.g., MRR
  │   └── Sub-metric: New MRR, Expansion MRR, Churn MRR
  ├── Supporting KPI 2 — e.g., Active customers
  ├── Supporting KPI 3 — e.g., Gross margin
  └── Supporting KPI 4 — e.g., Cash + runway
```

### CEO review cadence

- **Daily**: cash position, key sales / customer events
- **Weekly**: revenue + product + pipeline + hiring
- **Monthly**: full P&L variance, retention cohorts
- **Quarterly**: strategy KPIs, north-star trend

### Tooling by stage

| Stage | Tool |
|---|---|
| Pre-seed / Seed | Google Sheets + Causal |
| Seed / Series A | Causal + Visible (investor view) + Finmark |
| Series A / B | Causal or Runway + Visible |
| Series B / C+ | Mosaic + Visible + warehouse (postgresql) |

### Source-of-record principle

Every metric has ONE owning system. No metric without an owning system. Examples:

- MRR / churn → `stripe-mcp` (Stripe is source of record)
- Cash → `xero-mcp` (accounting is source of record)
- Product engagement → `posthog-mcp` (product analytics is source of record)
- Pipeline → CRM via `cli-anything`

---

## Crisis comms playbook

### 5 archetypes + holding statements

#### 1. Security breach

```markdown
We've identified [scope] security incident at [time]. [Initial impact assessment].
Immediate actions: [containment steps].
We will provide an update by [time].
For affected customers: [specific action / link].
Contact: [security@... or named DRI].
```

#### 2. Executive departure

```markdown
[Name] is departing the company effective [date]. We're grateful for their contributions, particularly [specific].
[Successor name OR interim arrangement].
Customer impact: [none / minimal / detail].
Investor impact: [board notification status].
```

#### 3. Product outage

```markdown
We're experiencing [scope] outage affecting [feature/service] since [time].
We are actively investigating. [Workaround if available].
Updates every [interval] at [status page URL].
We're sorry for the disruption.
```

#### 4. Layoffs

```markdown
Today we're reducing [X] roles, approximately [Y%] of the company, focused on [areas].
[Reason — be honest, not corporate].
[Severance: weeks + benefits + outplacement].
[Process: when, how, support].
For remaining employees: [what changes, what doesn't].
Customer commitments: [unchanged / detail].
```

#### 5. Regulatory action

```markdown
[Authority] has [action] regarding [topic]. We are [cooperating fully / contesting].
Our customers: [impact / no impact / specific guidance].
Our position: [brief, factual].
Legal counsel: [firm name].
We will update [stakeholder] by [date].
```

### Cascade order (60-min holding statement, then full)

1. **Customers** affected (60 min)
2. **Employees** (60-120 min, internal-first)
3. **Investors + board** (within same day)
4. **Regulators** (per legal-counsel guidance)
5. **Press** (only after the above; with single spokesperson)

### Rules

- **Single spokesperson** (CEO or designated DRI). No second voice.
- **60 min to holding statement.** Better imperfect on time than perfect late.
- **24h / 48h / 7-day cadence** for full incidents.
- **Post-mortem within 2 weeks** of resolution.
- **No speculation.** Facts only. "We don't know yet" is acceptable; making things up is not.

---

## M&A framework playbook

### Build vs Buy vs Partner — Wardley overlay

| Wardley position | Decision |
|---|---|
| Genesis | Build (no one else has it; differentiation is here) |
| Custom Built | Build (still differentiating) |
| Product | Partner (off-the-shelf exists; differentiation isn't here) |
| Commodity | Buy / Rent (utility — AWS, Stripe, Twilio) |

### Strategic fit scorecard

| Dimension | Weight | Score 1-5 | Weighted |
|---|---|---|---|
| Revenue impact | 25% | | |
| Cost / margin impact | 15% | | |
| Capability acquisition | 25% | | |
| Competitive moat | 20% | | |
| Cultural fit | 15% | | |

Below 3.5 weighted = decline. 3.5-4.0 = pilot first. >4.0 = proceed.

### Financial framework

- **DCF** at acquisition price + transaction costs + integration costs
- **Comparable multiples** (PitchBook / Crunchbase / SEC EDGAR for public)
- **Walk-away price** set before negotiation (the price above which you regret it)
- **Kill criteria** — diligence findings that force a no
- **Integration cost** — usually 30-100% of acquisition price for software M&A

### Decision memo template

```markdown
# M&A Memo: [Target Company]

## TL;DR
[Recommendation + price range + DACI]

## Strategic rationale
[Why this, why now — tied to Wardley + strategy]

## Strategic fit scorecard
[Table — see above]

## Financial framework
- DCF at offer: $XXX
- Comparables: $XXX (range)
- Walk-away price: $XXX

## Integration plan
- Timeline: [...]
- Cost estimate: [...]
- Retention plan for key talent: [...]

## Risks
[Top 5 with mitigations]

## Kill criteria
[Diligence findings that force a no]

## DACI
- Driver: [...]
- Approver: [CEO + board]
- Contributors: [CFO, legal-counsel, target-DRI]
- Informed: [exec team, board]

## Pre-mortem
[Top 5 reasons this could fail]
```

---

## Operating cadence playbook

### David Sacks framework — the operating rhythm doc

```markdown
# [Company] Operating Rhythm

## Weekly (every Monday 9-10am)
- Metrics review (CEO + leads)
- Unblock issues
- Decisions
Owner: CEO. Pre-read: Sunday EOD.

## Weekly (every Friday 9-10am)
- 1:1s with direct reports (rotating)
- Coaching + KR check-ins
Owner: CEO.

## Monthly (last Thursday)
- Roadmap review
- Forecast + budget variances
- Hiring plan check-in
Owner: CEO + CFO + leads. Pre-read: 48h ahead.

## Quarterly (first week of quarter)
- OKR setting + priority reset
- QBR (mid-quarter)
- Strategy update
Owner: CEO + leadership. 2-day offsite for OKR setting.

## Annual (first 2 weeks of January)
- Strategy + capital + hiring plan
- Wardley refresh
- Operating rhythm relock
Owner: CEO + board chair + leadership. 2-day offsite.

## Board (every 8 weeks)
- Board pack delivered 72h ahead
- 2-hour meeting + 30-min closed session
- Minutes published within 48h
Owner: CEO + board ops.
```

---

## Antipattern catalog

### Antipattern 1: Generic strategy ("we'll grow by expanding")

**BAD:**
> "Our strategy is to be the leader in [market] by delivering best-in-class value to our customers."

**Why it's bad:** No diagnosis (what's the challenge?). No guiding policy (what are we saying NO to?). Goals masquerading as strategy. Fluff. Fails all 3 Rumelt questions.

**GOOD:**
> "**Diagnosis:** Our 4-month payback period is killing growth — competitors with 8-month payback are out-spending us 4x in paid. **Guiding policy:** Shift acquisition from paid to PLG-content loops in next 2 quarters. **Actions:** (1) Hire content-led-growth lead by Aug 1. (2) Cut paid spend 50% by Oct. (3) Ship in-product viral loop by Nov. **Kill criteria:** if MRR drops >15% by Q4, reverse."

**Why it's better:** Names the challenge with data. Real policy choice. Sequenced + resourced + measured.

### Antipattern 2: Two-approver DACI

**BAD:**
> "Driver: PM. Approver: CEO + CTO. Contributors: ..."

**Why it's bad:** Two Approvers = no Approver. Decision stalls when they disagree.

**GOOD:**
> "Driver: PM. Approver: CEO. Contributors: CTO, Head of Eng. Informed: board."

**Why it's better:** Single Approver. CTO contributes input, CEO decides.

### Antipattern 3: Vague exec scorecard

**BAD:**
> "VP Marketing Outcomes: 1) Drive growth. 2) Build the team. 3) Improve brand."

**Why it's bad:** None of these are measurable. None of these are time-bound. None of these are ownable.

**GOOD:**
> "VP Marketing Outcomes (12 months): 1) Hit $5M ARR with $200k/mo blended CAC. 2) Hire 4 marketers (Growth, Content, Demand, Brand) at quality bar. 3) Lift unaided brand awareness in ICP from 18% → 35% per Q4 survey."

**Why it's better:** Measurable, time-bound, ownable. CEO can call the role's success or failure in 12 months.

### Antipattern 4: All-hands as status update

**BAD:** 45-min monologue from CEO about progress on initiatives.

**Why it's bad:** Status belongs in pre-read. Live time is for energy, decisions, and connection.

**GOOD:** Pre-read covers status. Live = 10 min wins + shoutouts, 10 min "one thing we're deciding next quarter," 10 min Q&A.

### Antipattern 5: Annual planning without pre-mortem

**BAD:** Skip the pre-mortem ("we don't have time").

**Why it's bad:** ~30% better risk identification per Wharton study. The "we don't have time" excuse costs more time than the 30-min facilitation.

**GOOD:** 30-min pre-mortem on prior year before Day 1 of offsite. Top risks feed risk register.

### Antipattern 6: Investor update with only wins

**BAD:** "Great month! Hit MRR target! Closed key customer! Team morale high!"

**Why it's bad:** Investors lose trust when lowlights never appear. They suspect you're hiding something.

**GOOD:** "Great month for MRR ($X, +Y%). Lowlights: lost N customer to competitor (lesson: pricing power weak in segment Z), VP Eng search stalled (now retained search), runway tightened to 14 months."

### Antipattern 7: Skipping reference checks

**BAD:** "They interviewed great, made them an offer."

**Why it's bad:** Bad exec hires cost $1M-$5M+ in compounding damage. References catch 80% of issues interviews miss.

**GOOD:** Topgrading 360 references (3 peers + 2 reports + 1 manager) — minimum — before any VP+ offer.

---

## Reference patterns

### Pattern: Pre-mortem facilitation (30 min)

```
1. Frame (3 min): "12 months from now, this failed. We're at the funeral."
2. Silent brainstorm (10 min): each writes reasons
3. Round-robin (10 min): share one at a time, no debate
4. Cluster + prioritize (5 min): top 5 risks
5. Mitigation assignment (2 min): each top-5 gets owner + due date
```

### Pattern: Weekly metrics review (60 min)

```
1. Open with last week's actions (5 min): who did what they said
2. Metrics walk-through (15 min): north star + supporting KPIs
3. Exceptions (15 min): what's red, why, recovery
4. Decisions (15 min): what are we deciding this week
5. Asks + unblock (10 min): what does each lead need
```

### Pattern: 1:1 structure (45 min)

```
1. Their topics first (20 min): what's on their mind
2. Your topics (10 min): what you need to discuss
3. Coaching question (5 min): "What's the one decision you've been avoiding?"
4. KR check-in (5 min): confidence dial, blockers
5. Actions + next time (5 min): commit + recap
```

---

## SOTA tool reference (June 2026)

This section is grep-only — the agent uses keyword-driven retrieval to surface the right skill pack for the user's task. Headings are intentionally search-friendly. Every entry links to a detailed `SKILL.md` in `skills/` that ships in this bundle and loads on demand.

**Full coverage map:** see `reference/SOTA_USE_CASES.md` for the per-use-case mapping and confidence rating.

### Notion knowledge base (strategy + decisions + minutes)

`notion-mcp` is the CEO's source-of-record for strategy docs, decision journal, OKR canvas, board minutes, operating rhythm doc, partnership memos, M&A memos, all-hands pre-reads. Use as DEFAULT for any persistent narrative artifact.

- **Skill use:** indirect — every CEO-skill writes to Notion via `notion-mcp`
- **Source:** https://developers.notion.com/docs/mcp

### Linear initiative + DRI tracking

`linear-mcp` is the operating system for initiatives + DRI assignment + action items from board / QBR / weekly metrics. Issues map to DRIs (single assignee); cycles map to quarterly OKRs; projects map to multi-quarter initiatives.

- **Skill use:** part of `board-meeting-prep-deck-minutes`, `qbr-quarterly-business-review`, `ceo-operating-cadence-week-month-quarter`
- **Source:** https://developers.linear.app

### Visible.vc investor updates

Visible.vc is the de-facto investor-update tool in 2026 — KPI auto-sync from Stripe / Carta / analytics, template-based update creation, deliver-once-send-to-many, engagement tracking (opens / time-per-section). Free tier covers solo founders; paid for advanced KPIs.

- **Skill:** `skills/investor-update-monthly-quarterly-visible/SKILL.md`
- **Endpoint:** `https://api.visible.vc/v1`
- **Auth:** API key → `VISIBLE_API_KEY`
- **Source:** https://visible.vc/blog/investor-update-software/

### Ashby + Greenhouse executive recruiting

Ashby = analytics-depth challenger (best ATS analytics in 2026); Greenhouse = #1 G2 satisfaction (98%) for structured hiring with gold-standard scorecards. Ashby for data-driven recruiting teams; Greenhouse for structured-hiring methodology. Lever as candidate-experience-focused mid-market alt.

- **Skill:** `skills/exec-recruiting-greenhouse-ashby-scorecard/SKILL.md`
- **Endpoints:** Ashby API + Greenhouse Harvest API
- **Auth:** API keys per platform
- **Source:** https://www.index.dev/blog/greenhouse-vs-lever-vs-ashby-ats-comparison

### Mooncamp + Lattice + WorkBoard (OKRs)

Mooncamp for design-conscious teams <150 people (€8/user/mo, REST API). Lattice Goals for HR-integrated 1:1s + reviews + OKRs ($8/seat). WorkBoard (Quantive acquired) for 200+ employees with auto-tracked KRs. Pick by stage + integration needs.

- **Skill:** `skills/okr-cascade-lattice-mooncamp-quantive/SKILL.md`
- **Endpoints:** Mooncamp REST + Lattice Goals + WorkBoard
- **Auth:** API keys per platform
- **Source:** https://mooncamp.com/blog/best-okr-software

### Granola + Fathom + Fireflies + Otter (AI transcription)

Per-meeting-type router: Granola (bot-free macOS for solo founder strategy sessions); Fathom (best free unlimited — board minutes); Fireflies (100+ language multilingual — customer calls); Otter (95% accuracy general). Fellow as enterprise-team option.

- **Skill:** `skills/ai-meeting-transcription-granola-fathom-fireflies-routing/SKILL.md`
- **Endpoints:** per-tool export APIs
- **Source:** https://meetingnotes.com/blog/best-ai-note-takers

### Motion + Reclaim + Sunsama + Akiflow (calendar)

Motion = auto-rebuild day around new meetings (best for 20+ meetings/wk). Reclaim = focus-time + habit defense. Sunsama = morning planning ritual (pulls from Asana/Linear/Todoist/Gmail/Slack). Akiflow = command bar across task tools + calendar. **Note: Clockwise shut down March 2026 (Salesforce acq).**

- **Skill:** `skills/calendar-time-protection-motion-reclaim-sunsama/SKILL.md`
- **Endpoints:** per-tool API + `gcalcli-calendar` for audit
- **Source:** https://temporal.day/blog/motion-vs-reclaim-vs-clockwise-vs-akiflow-vs-sunsama

### Causal + Mosaic + Visible + Finmark (KPI dashboard)

Causal = spreadsheet-inspired FP&A, scenario modeling, Seed-Series B default. Mosaic = AI-powered FP&A, Series C+ standard. Visible = investor-facing KPI + metric pull. Finmark = startup-budgeting + KPI metrics dashboard. Pick by stage.

- **Skill:** `skills/kpi-north-star-dashboard-causal-mosaic/SKILL.md`
- **Endpoints:** per-tool API + `postgresql-mcp` for warehouse
- **Source:** https://valueaddvc.com/blog/best-financial-modeling-tools-for-startups-excel-vs-runway-vs-causal-vs-mosaic

### Gamma + Beautiful.ai (decks)

**Tome dead** (shut down March 2025, brand sold to AngelList). Gamma = best overall in 2026 (Agent + Generate API + native image gen) — web-first storytelling default. Beautiful.ai = PowerPoint compatibility + brand controls — for board decks needing PPT export. Pitch added 25+ AI actions but lost ground.

- **Skill use:** part of `weekly-monthly-all-hands-prep` and `qbr-quarterly-business-review`
- **Source:** https://posteverywhere.ai/blog/15-best-ai-presentation-makers

### Tella + Vidyard + Zight + Berrycast (async video)

Loom usage softening post-Atlassian acq (25-video / 5-min free cap). 2026 alternatives: Tella (polished branded recordings — external comms), Vidyard (sales-CRM-integrated), Zight (screenshot + video unified), Berrycast (free unlimited — simple). For CEO async: Tella outward, Vidyard sales-aligned.

- **Skill:** `skills/loom-async-video-comms/SKILL.md`
- **Source:** https://zight.com/blog/best-loom-alternatives-2026/

### I'mBoard + Boardable + OnBoard + Diligent (board portals)

**BoardEffect acquired by Diligent + merged with OnBoard.** Startup-friendly: I'mBoard ($30/seat — AI-powered prep + transparent pricing), Boardable ($79-329/mo — most affordable nonprofit-friendly). Enterprise: Diligent ($15-30k+/yr — public co standard). Most have no public API on startup tiers — upload PDF + email is the fallback.

- **Skill use:** part of `board-meeting-prep-deck-minutes` (deck + memo + Linear actions automated; portal upload manual on startup tiers)
- **Source:** https://www.imboard.ai/blog/alternatives-to-diligent-boards + https://appdeck.com/blog/board-portal-software-comparison-2026

### OnlineWardleyMaps (Wardley mapping)

OnlineWardleyMaps.com is the free public renderer for Wardley map text syntax. Paste text syntax (component, anchor, evolution stage) → render PNG/SVG. The standard tool in 2026 for build vs buy vs partner gameplay analysis.

- **Skill:** `skills/wardley-mapping-competitive-landscape/SKILL.md`
- **Source:** https://onlinewardleymaps.com

### PitchBook + CB Insights + Crunchbase + Tracxn (M&A + intel)

PitchBook = enterprise standard ($20k+/yr — Sequoia/a16z back-office integration). CB Insights = trend-forward + predictive ($30k+/yr). Crunchbase = $29-49/mo accessible default. Tracxn = startup intelligence + sector mapping. For early-stage CEO: Crunchbase + Tracxn covers most M&A scoping needs.

- **Skill use:** part of `ma-build-vs-buy-vs-partner-framework`
- **Source:** https://otio.ai/blog/cb-insights-vs-pitchbook + https://otio.ai/blog/crunchbase-vs-pitchbook

### DACI + RACI + DRI + Pre-mortem + Decision Journal (decision stack)

DACI (Atlassian — single Approver, strategic decisions). RACI (execution / task ownership). DRI (Apple — cross-functional initiative single owner). Pre-mortem (Gary Klein — ~30% better risk identification per Wharton study). Decision Journal (Annie Duke — separate process from outcome).

- **Skills:** `raci-daci-dri-decision-frameworks` + `decision-journal-pre-mortem-klein`
- **Source:** https://www.atlassian.com/team-playbook/plays/daci + https://www.gary-klein.com/premortem + https://grahammann.net/book-notes/how-to-decide-annie-duke

### Rumelt + OGSM + V2MOM (strategy stack)

Rumelt's "Good Strategy / Bad Strategy" kernel (diagnosis / guiding policy / coherent actions) is the spine. OGSM (objectives / goals / strategies / measures) and V2MOM (vision / values / methods / obstacles / measures, Salesforce) are operating formats. Use Rumelt to verify the strategy isn't bad; OGSM or V2MOM as the canvas.

- **Skill:** `vision-strategy-doc-rumelt-ogsm-v2mom`
- **Source:** https://cutlefish.substack.com/p/tbm-332-the-last-strategy-framework + https://www.masterclass.com/articles/ogsm

### Sibling MCPs (defer to siblings for depth)

- **Product / discovery** — `product-manager` agent owns `linear-mcp`, `figma-mcp`, `posthog-mcp` for product depth
- **Marketing / GTM** — `marketing-agent` owns Buffer / Klaviyo / Ahrefs / HubSpot stack
- **Sales** — `sales-agent` owns Salesforce / HubSpot CRM / Outreach
- **Finance** — `finance-controller` and `finance-agent` own deeper Stripe / Xero / Carta / Pulley
- **Legal** — `legal-counsel` owns DocuSign / Ironclad / NVCA model docs
- **Ops** — `operations-agent` owns Rippling / Gusto / Brex / Ramp / Navan

CEO agent surfaces the right sibling and frames the question; doesn't duplicate their depth.

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| "Write our strategy doc" | `vision-strategy-doc-rumelt-ogsm-v2mom` | Always run Rumelt 3-question test before shipping |
| "Map the competitive landscape" | `wardley-mapping-competitive-landscape` | Use for 12-24mo gameplay reasoning |
| "Prep for board meeting" | `board-meeting-prep-deck-minutes` | Pre-read 72h ahead, asks explicit |
| "Send investor update" | `investor-update-monthly-quarterly-visible` | Monthly default, lowlights mandatory |
| "Set up data room" | `investor-data-room-curation` | DocSend + Google Drive structure |
| "Hire a VP / Head of X" | `exec-recruiting-greenhouse-ashby-scorecard` | Outcomes scorecard before JD |
| "Run my 1:1s" | `exec-1on1-coaching-framework` | Coaching question library + KR check-in |
| "Set OKRs" | `okr-cascade-lattice-mooncamp-quantive` | One O + 3 KRs per team / quarter |
| "Who decides this?" | `raci-daci-dri-decision-frameworks` | DACI for decisions, RACI for execution, DRI for ownership |
| "Should we do X?" | `decision-journal-pre-mortem-klein` | Pre-mortem if irreversible; journal always |
| "Plan next week's all-hands" | `weekly-monthly-all-hands-prep` | Lenny format, Gamma deck, 30-min weekly |
| "Run our QBR" | `qbr-quarterly-business-review` | 5-component, 60% decisions, 48h pre-read |
| "Plan our 2027" | `annual-planning-cycle-cadence` | Pre-mortem + Wardley + bottom-up + 2-day offsite |
| "Record an update for the team" | `loom-async-video-comms` | Tella for external, Vidyard for sales-adjacent |
| "Capture all my meetings" | `ai-meeting-transcription-granola-fathom-fireflies-routing` | Route by meeting type |
| "Audit my calendar" | `calendar-time-protection-motion-reclaim-sunsama` | 30-day audit + tool rules |
| "Build my CEO dashboard" | `kpi-north-star-dashboard-causal-mosaic` | One north star, daily cash, weekly revenue |
| "[Crisis] — what do we do?" | `crisis-communication-playbook` | Holding statement <60 min, cascade order |
| "Should we acquire / partner with X?" | `ma-build-vs-buy-vs-partner-framework` | Wardley overlay + scorecard + walk-away |
| "Set our operating rhythm" | `ceo-operating-cadence-week-month-quarter` | David Sacks framework |

---

## Closing rules

Time is finite — protect the calendar. Decisions over alignment — force them. Hire slow, fire fast — every wrong hire compounds. When depth is required in product / marketing / sales / finance / legal / ops / support / growth / data, call the sibling agent. The CEO Agent owns the operating system; specialists own the depth.
