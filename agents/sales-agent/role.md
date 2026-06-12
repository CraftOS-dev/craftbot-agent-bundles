# Sales Agent — deep reference

This appends to `AGENT.md`. **Not** in the agent's default context. Grep when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "Sales technology categories", "Outbound sequence playbook", "Qualification framework reference", "MEDDIC scoring rubric", "MEDDPICC scoring rubric", "BANT scoring rubric", "SPIN question bank", "Challenger commercial conversation", "Discovery call brief template", "Demo prep template", "Deal coaching framework", "Next-best-action heuristics", "Multi-threading playbook", "Stakeholder map template", "Mutual action plan template", "MAP template", "Pipeline stage criteria", "Pipeline review template", "Forecasting methodology", "Commit accuracy", "Sequence design spec template", "Cold email deliverability checklist", "SPF DKIM DMARC validation", "Domain warmup schedule", "Lead enrichment waterfall", "Account research template", "Win/loss post-mortem template", "Battlecard template", "ROI calculator template", "Proposal template", "Sales success metrics", "AE benchmarks", "SDR benchmarks", "Signal intent monitoring", "Expansion playbook", "Renewal playbook", "SDR to AE handoff template", "Negotiation prep template", "Pricing strategy reference", "SOTA tool reference".

For provenance, see `SOURCES.md`.

---

## Capability reference

### Sales motions this agent handles

- Outbound cold email + LinkedIn + phone cadence
- Inbound lead qualification + scoring + routing
- Account-based motion (target list + multi-channel orchestration)
- Discovery + demo prep
- Deal coaching (per-opp next-best-action)
- Negotiation prep + pricing strategy
- Proposal generation + e-sign
- Multi-threading enterprise deals
- Win/loss post-mortem
- Forecasting + commit accuracy
- Pipeline review + hygiene
- Signal/intent monitoring (job changes, funding, tech-stack shifts)
- Customer expansion / upsell
- Renewal pipeline management
- SDR ↔ AE handoff
- Sales enablement (battlecards, ROI calculators, case studies)
- Sales reporting + dashboards

### Sales technology categories (for reference)

- **CRM:** HubSpot, Salesforce, Pipedrive, Attio, Folk, Copper, Zoho CRM, Zoho Bigin
- **Lead enrichment:** Apollo.io, Clay.com, Lusha, ZoomInfo, Cognism, Crunchbase
- **Intent / signal:** Common Room, Pocus, Koala, RB2B, Default, Bombora, G2 intent
- **Sequence engagement:** Outreach.io, Salesloft, lemlist, Reply.io, Instantly, Smartlead, La Growth Machine
- **LinkedIn outreach:** HeyReach, Phantombuster, TexAu, Expandi, Dripify
- **Email warmup:** Lemwarm, Mailwarm, Warmup Inbox, Instantly warmup, Smartlead warmup
- **Email deliverability tests:** mail-tester.com, Glock Apps, MXToolbox, GlockApps
- **Call intelligence:** Gong, Chorus.ai, Fathom, tl;dv, Fireflies, Otter.ai, Avoma, Salesken
- **Proposal / e-sign:** PandaDoc, DocuSign, Qwilr, Proposify, DealHub (CPQ)
- **Scheduling:** Calendly, Chili Piper, HubSpot Meetings, Cal.com
- **Forecasting:** Clari, Gong Forecast, BoostUp, InsightSquared, Aviso
- **Commission / spiff:** Spiff, CaptivateIQ, QuotaPath, Performio, Xactly
- **Sales enablement:** Highspot, Seismic, Showpad, Mindtickle, MindTickle (training)

---

## Outbound sequence playbook

### Sequence design spec template

```markdown
## [Sequence Name] — Design Spec

### Trigger
- Source: [cold ICP / inbound MQL / re-engagement / lost-deal-revive]
- Entry condition: [list signal]
- Exclusions: [already in active sequence / opted-out / customer]

### Segment
- ICP fit: [firmographic — size, vertical, geo, tech stack]
- Persona: [title, function, seniority]
- Volume: [accounts × contacts per account]

### Cadence (multi-channel — 12 to 16 days, 7-9 touches)
| Day | Channel | Touch | Subject (A/B) | Body focus | Exit If |
|---|---|---|---|---|---|
| 0 | Email | 1 | "A" / "B" | Pattern interrupt + value hypothesis | Reply / Unsub |
| 2 | LinkedIn | 2 | n/a | Connection request, no pitch | Accept + msg / Decline |
| 4 | Email | 3 | "A" / "B" | Reply-bump in same thread | Reply |
| 6 | LinkedIn | 4 | n/a | DM with relevant content gift | Reply |
| 7 | Phone | 5 | n/a | Voicemail script + follow-up email | Connect |
| 10 | Email | 6 | "A" / "B" | Customer proof / case study | Reply |
| 12 | Phone | 7 | n/a | Second call attempt | Connect |
| 14 | Email | 8 | "A" / "B" | Break-up + close-out | Reply / Cold |
| Day 14+ | — | — | — | Re-add to nurture in 90 days | — |

### A/B variants
- Subject A: ≤ 6 words, lowercase
- Subject B: question format
- First-line A: pattern-interrupt referencing specific trigger
- First-line B: customer-result anchor

### Targets
| Metric | Target | Alert if |
|---|---|---|
| Open rate (directional only post-MPP) | > 40% | < 25% |
| Reply rate | > 5% | < 2% |
| Positive reply rate | > 1% | < 0.3% |
| Bounce rate | < 2% | > 5% |
| Complaint rate | < 0.10% | > 0.30% |
| Meetings booked / 1000 sends | > 8 | < 3 |

### Compliance
- [ ] SPF + DKIM + DMARC validated (cold-outbound domain ≠ transactional)
- [ ] Sender warmup status confirmed (≥ 4 weeks for new domain)
- [ ] Daily volume per mailbox: 50-100 sends (cap until reply rate stable)
- [ ] CAN-SPAM / GDPR / CASL compliance — physical address + opt-out
- [ ] Suppression list applied (customers, opted-out, do-not-contact)
```

### Cold email deliverability checklist

```markdown
## Pre-Launch Deliverability Audit — [Domain]

### Authentication
- [ ] SPF record: `v=spf1 include:[esp].com ~all`
- [ ] DKIM: enabled, 2048-bit key, DNS record verified
- [ ] DMARC: `p=quarantine` minimum (preferably `p=reject`), `rua=` reporting configured
- [ ] Return-Path: aligned with From domain (`bounce.brand.com`)
- [ ] Domain age: ≥ 30 days (cold-outbound domain should age 30+ days before first send)

### Sender Warmup
- [ ] Warmup tool active: Lemwarm / Instantly built-in / Smartlead warmup
- [ ] Warmup duration: ≥ 4 weeks before first cold campaign
- [ ] Daily volume ramp:
  - Week 1: 10-20 sends/day per mailbox
  - Week 2: 30-50 sends/day
  - Week 3: 50-80 sends/day
  - Week 4+: 100-150 sends/day (cap and hold)
- [ ] Reply rate from warmup > 30% before first cold launch

### Reputation Checks
- [ ] Complaint rate: __% (target < 0.10%, max 0.30%)
- [ ] Hard bounce rate: __% (target < 1%)
- [ ] Blocklist status: clean on SBL/CBL/Spamhaus (check via MXToolbox)
- [ ] Google Postmaster Tools: configured, monitored
- [ ] mail-tester.com score: ≥ 9/10
- [ ] Glock Apps placement: inbox > 80% across major providers (Gmail, Outlook, Yahoo)

### Send-time Hygiene
- [ ] Suppression list applied (customers, opt-outs, hard bounces, do-not-contact)
- [ ] No more than 1 link in first email (raises spam score)
- [ ] No tracking pixels on first email (raises spam score)
- [ ] Plain-text-only first email; HTML acceptable from Touch 3 onwards
- [ ] Sending hours align with recipient timezone (8am-5pm local)
```

### Domain warmup schedule

| Week | Daily volume per mailbox | Recipient mix | Reply-rate target |
|---|---|---|---|
| 1 | 10-20 | 100% warmup peers | > 80% |
| 2 | 30-50 | 90% warmup, 10% real engaged | > 60% |
| 3 | 50-80 | 70% warmup, 30% real engaged | > 50% |
| 4 | 80-100 | 50% warmup, 50% real cold | > 40% |
| 5+ | 100-150 | 30% warmup, 70% real cold | > 30% (cap and hold) |

### Lead enrichment waterfall

```
Account candidates →
  1. Apollo people_search (filters: title, function, seniority, company size)
  2. For missing emails: Clay multi-source enrichment (Apollo + Hunter + RocketReach + Dropcontact)
  3. For missing phones: Lusha (mobile-rich) → ZoomInfo (enterprise)
  4. For EU-only compliance: Cognism (GDPR-clean)
  5. Tech-stack via Clay (BuiltWith + Wappalyzer)
  6. Recent triggers via Apollo "company news" + Crunchbase funding webhook
  7. Final filter: ICP fit score ≥ 70/100 to enter sequence
```

---

## Qualification framework reference

### When to use which

| Framework | Use for | Letters / Steps |
|---|---|---|
| MEDDIC | Complex B2B > $25K ACV, multiple stakeholders | Metrics, Economic buyer, Decision criteria, Decision process, Identify pain, Champion |
| MEDDPICC | Enterprise B2B > $100K ACV | MEDDIC + Paper process + Competition |
| BANT | Transactional / SMB / inbound | Budget, Authority, Need, Timeline |
| SPIN | Discovery call structure | Situation, Problem, Implication, Need-payoff |
| Challenger | Commercial conversation framing | Teach, Tailor, Take control |
| GPCT(BA/C&I) | HubSpot's variant for inbound | Goals, Plans, Challenges, Timeline (+ Budget/Authority + Consequences/Implications) |

### MEDDIC scoring rubric

Each field scored 0-3:
- **0** = Empty / unknown
- **1** = Hypothesis (not validated by prospect)
- **2** = Validated by prospect, not documented in CRM
- **3** = Validated by prospect AND documented with evidence in CRM

**Field definitions:**
- **Metrics:** What measurable business outcome will the prospect own? (e.g., "reduce CAC by 20% in 6 months")
- **Economic buyer:** Named individual with budget authority. Must be EB, not influencer.
- **Decision criteria:** What criteria will the buying committee use? (technical, business, vendor-stability, security)
- **Decision process:** What are the steps from current state → signed contract? (demo, security review, procurement, legal, exec approval)
- **Identify pain:** What specific business pain is felt by named people? Quantified if possible.
- **Champion:** Named individual who is actively advocating internally. Documented advocacy moment required.

**Roll-up:** Sum of 6 fields = score out of 18. ≥ 14 = Commit-bucket eligible. 10-13 = Best Case. < 10 = Pipeline only.

### MEDDPICC scoring rubric

Adds two fields to MEDDIC:
- **Paper process:** Vendor onboarding, security review, MSA negotiation timeline. Maps to expected close date realism.
- **Competition:** Named competitors in the deal + their position. "No competition" is usually a red flag (means buyer hasn't decided to buy at all).

Roll-up: Sum of 8 fields out of 24. ≥ 19 = Commit. 14-18 = Best Case. < 14 = Pipeline.

### BANT scoring rubric

- **Budget:** Confirmed $ amount + fiscal-year alignment
- **Authority:** Named decision-maker has agreed to evaluate
- **Need:** Specific pain articulated by prospect (not vendor-suggested)
- **Timeline:** Trigger event + target purchase date

All 4 = qualified. 3 = qualified-with-risk. 2 or fewer = nurture.

### SPIN question bank

Use 5-7 questions per discovery call, mixing the four types:

**Situation (1-2 questions):** Establish baseline. "Walk me through your current [process / setup / team structure]."

**Problem (2-3 questions):** Surface pain. "Where does that process break down? What costs you the most time / money / customer trust?"

**Implication (2-3 questions):** Magnify pain. "If that problem persists for another 6 months, what's the downstream impact on [revenue / retention / team morale]? Who else feels it?"

**Need-payoff (1-2 questions):** Buyer articulates value. "If we solved [specific pain], what would that be worth to you / your team / the business?"

**Anti-pattern:** All Situation questions. Buyers feel interrogated, not understood.

### Challenger commercial conversation

Three moves:
- **Teach** — Bring an insight the buyer didn't have. Not a feature pitch; a perspective on their business.
- **Tailor** — Make the insight specific to their company / team / industry / stage.
- **Take control** — Hold the line on price, scope, and timeline. Don't capitulate at the first pushback.

Use when: commercial conversation has stalled, buyer is shopping multiple vendors, or buyer's stated criteria don't match their real pain.

---

## Discovery call brief template

```markdown
# Discovery Brief — [Account Name] × [Date]

## Attendees
- [Their] Name 1 (Title, Role in evaluation)
- [Their] Name 2
- [Us] Name 1, Name 2

## Account snapshot
- Industry / size / geo / stage
- Tech stack (from BuiltWith / Clay enrichment)
- Recent triggers (funding event / leadership change / job posting / tech adoption)
- LinkedIn profile highlights for attendees

## Hypothesis
- Pain we suspect: ___
- Value we offer: ___
- ICP fit score: __/100

## Discovery questions (5-7, SPIN-balanced)
- S1: ___
- P1: ___
- P2: ___
- I1: ___
- I2: ___
- NP1: ___

## MEDDIC checklist (fill during/after call)
- [ ] Metrics: ___
- [ ] Economic buyer: ___
- [ ] Decision criteria: ___
- [ ] Decision process: ___
- [ ] Identified pain: ___
- [ ] Champion: ___

## Objection rehearsal (top-5 likely)
1. "We don't have budget." → Response: ___
2. "We're happy with current vendor." → Response: ___
3. "We just signed [competitor]." → Response: ___
4. "Send me info, we'll review internally." → Response: ___
5. "Pricing seems high." → Response: ___

## Agenda (30 min)
- 0-3 min: rapport + agenda confirm
- 3-20 min: discovery (5-7 questions)
- 20-25 min: hypothesis + relevant proof point
- 25-30 min: agreed next step + calendar slot

## Agreed next step
- Action: ___
- Owner: ___
- Date: ___
```

---

## Demo prep template

```markdown
# Demo Prep — [Account] × [Date]

## Discovery recap
- Pain: ___
- Stakeholders attending: ___
- MEDDIC gaps to close: ___

## Demo storyline (3 acts, 25 min)
- Act 1 (5 min): "Here's what we heard you're trying to solve."
- Act 2 (15 min): "Here's how we'd solve it — 3 features tied to your pain."
- Act 3 (5 min): "Here's how we'd roll this out at [Account] — proposed mutual action plan."

## Feature → pain mapping
| Feature shown | Maps to pain | Proof point |
|---|---|---|
| Feature A | "Reduce manual reconciliation time" | Customer X saved 12hr/week |
| Feature B | "Audit trail compliance" | SOC 2 + customer Y compliance story |

## Objection rehearsal (top-5)
1. ___
2. ___

## Battlecard (if competitor named)
- Competitor: ___
- Their strength: ___
- Our differentiation: ___
- Trap question to ask: ___

## Agreed next step before demo ends
- ___
```

---

## Deal coaching framework

### Next-best-action heuristics

For each open deal, compute these signals:

1. **MEDDIC completeness** (or BANT). Score < 14/18 (MEDDIC) or < 3/4 (BANT) → NBA = "Close criteria gaps."
2. **Age-in-stage vs median.** If > 1.5× median → NBA = "Diagnose stall — call champion this week."
3. **Multi-thread depth.** < 3 stakeholders engaged for deal > $50K → NBA = "Multi-thread to EB."
4. **Last meaningful activity.** > 14 days since prospect-initiated touch → NBA = "Reactivation outreach with new angle."
5. **Sentiment trajectory** (from Gong). Declining tone → NBA = "Direct conversation about deal status."
6. **Champion silence.** Champion non-responsive > 7 days → NBA = "Send champion ammunition (1-pager, ROI calc, case study) + check in."
7. **Decision date drift.** Promised close date pushed twice → NBA = "Mutual action plan with signed close-date commitment."

### Pick the single highest-value NBA. Provide:

- The literal email/message/talking-point copy
- The deadline
- The trigger to escalate if NBA fails (e.g., "if champion doesn't reply by Friday → escalate to AE+manager joint call")

---

## Multi-threading playbook

### Stakeholder map template

```markdown
# Stakeholder Map — [Account]

| Stakeholder | Title | Role in eval | Last engaged | Engagement depth | Influence | Sentiment |
|---|---|---|---|---|---|---|
| Name 1 | VP Eng | Champion | 2026-06-02 | 5 touches / 2 meetings | High | Positive |
| Name 2 | CTO | Economic buyer | 2026-05-15 | 1 touch / 0 meetings | Critical | Unknown |
| Name 3 | Dir Platform | Technical evaluator | 2026-05-28 | 3 touches / 1 meeting | Medium | Neutral |
| Name 4 | CFO | Approver | Not engaged | 0 | Critical (price) | Unknown |
| Name 5 | Sr Eng | End-user voice | 2026-05-20 | 2 touches | Low | Positive |

## Engagement targets by deal size
- Deal < $25K: 1 stakeholder sufficient (champion = decision-maker)
- Deal $25-50K: 2-3 stakeholders engaged
- Deal $50-150K: 4+ stakeholders, including EB confirmed
- Deal > $150K: 5-7 stakeholders, exec sponsor on both sides

## Multi-thread tactics
- LinkedIn "thanks for connecting" message to silent stakeholders
- Content gift ungated to silent EB (industry report, ROI study)
- Champion-driven intro request to peer stakeholders
- Joint AE + champion-led meeting to bring EB in
- Executive sponsor outreach (your CEO/CRO to their counterpart)
```

---

## Mutual action plan template

```markdown
# Mutual Action Plan — [Account] × [Vendor]
**Mutually committed:** [Champion name] × [AE name] · **Target close:** [Date]

## Joint objective
[One sentence — what both parties commit to accomplishing by close date]

## Decision criteria (validated)
1. ___
2. ___
3. ___

## Steps to close
| # | Step | Owner | Due date | Status |
|---|---|---|---|---|
| 1 | Discovery call with EB | Champion | 2026-06-15 | ☐ |
| 2 | Security review packet shared | Vendor | 2026-06-20 | ☐ |
| 3 | Procurement intake form submitted | Champion | 2026-06-25 | ☐ |
| 4 | Legal redlines exchanged | Vendor + Champion legal | 2026-07-05 | ☐ |
| 5 | MSA + Order Form signed | EB | 2026-07-15 | ☐ |
| 6 | Kickoff scheduled | Both | 2026-07-22 | ☐ |

## Risks + mitigations
- Risk: [name]. Mitigation: [action].
- ___

## Communication cadence
- Weekly 15-min sync: [day, time]
- Slack/email check-ins: [day]
- Escalation path: [name → name]
```

---

## Pipeline review template

```markdown
# Pipeline Review — Week of [Date]

## Coverage
- Quarterly quota: $___
- Pipeline value (sum of open opp amounts): $___
- Coverage ratio: __× (target: 3-4×)

## Forecast buckets
| Bucket | Count | Sum amount | % of quota |
|---|---|---|---|
| Commit (>80% confidence) | __ | $__ | __% |
| Best Case (50-80%) | __ | $__ | __% |
| Pipeline (<50%) | __ | $__ | __% |
| Total | __ | $__ | __% |

## Slip-risk deals (top 5)
| Deal | Amount | Stage | Days-in-stage | Reason at risk | NBA |
|---|---|---|---|---|---|
| Account A | $50K | Negotiation | 45 | Champion silent 14d | Send ammunition + EB intro request |
| ... |

## Stalled deals (in stage > 1.5× median, no recent activity)
| Deal | Amount | Last activity | NBA |
|---|---|---|---|

## Per-AE breakdown
| AE | Pipeline $ | Commit $ | Coverage × | Forecast accuracy (last 4 wks) |
|---|---|---|---|---|

## This-week movement
- New opportunities created: __
- Stage advancements: __
- Closed-won: __ ($__)
- Closed-lost: __ ($__)
- Reasons closed-lost: [top 3]

## Decisions
- ___
```

---

## Pipeline stage criteria

Each stage has explicit entry + exit criteria. Deals don't advance without meeting exit criteria.

| Stage | Entry criteria | Exit criteria | Typical days |
|---|---|---|---|
| 1. Prospect | Account on ICP list; first touch sent | Reply or meaningful engagement (open + click) | 0-14 |
| 2. Discovery | Discovery call scheduled or completed | MEDDIC: metrics + pain identified; champion candidate named | 7-21 |
| 3. Evaluation | Demo completed; technical eval underway | Decision criteria validated; EB named | 14-45 |
| 4. Proposal | Proposal sent; MAP signed | All MEDDIC fields ≥ 2; competitor position known | 7-30 |
| 5. Negotiation | Verbal commit; legal/procurement engaged | Redlines resolved; verbal close confirmed | 7-21 |
| 6. Closed-won | Contract signed | Implementation kickoff scheduled | — |
| 6. Closed-lost | Prospect disqualified or moved to competitor | Win/loss post-mortem completed | — |

---

## Forecasting methodology

### Three buckets

- **Commit (>80% confidence):** All MEDDIC fields ≥ 2, MAP signed, verbal close confirmed, close date this period. AE accountable to deliver.
- **Best Case (50-80%):** Most MEDDIC fields validated, champion confirmed, EB engaged, close date this period. AE working active risks.
- **Pipeline (<50%):** Discovery complete, qualification in progress. Counts toward coverage, not commit.

### Commit accuracy tracking

- Per AE per quarter: (commit-bucket deals that actually closed) / (total commit-bucket deals).
- Target: > 80%. < 70% = retraining; < 60% = ride-along on next forecast call.
- Track slippage (commit deals that miss close date) + pull-ins (best-case deals that close ahead of date).

### Forecast cadence

- **Weekly:** AE forecast roll-up, slip-risk review.
- **Bi-weekly:** Manager-level commit review.
- **Monthly:** Pipeline coverage check (3-4× quota).
- **Quarterly:** Commit accuracy review + win/loss rollup.

---

## Account research template

```markdown
# Account Research — [Company Name]

## Firmographic
- Industry / sub-industry: ___
- Employee count: ___ (range from LinkedIn / Apollo)
- Revenue: $__ (Crunchbase / D&B)
- HQ + key regions: ___
- Funding stage + last round: ___ + $__ raised [date]
- Investors: ___

## Tech stack (from BuiltWith / Clay / job postings)
- Cloud: AWS / GCP / Azure / hybrid
- CRM: ___
- Engineering tools: ___
- Adjacent tools that imply they need ours: ___

## Recent triggers (last 90 days)
- Leadership change: ___ (LinkedIn job-change alerts)
- Funding event: ___ (Crunchbase webhook)
- Product launch / news: ___ (Apollo news / brave-search)
- Hiring signals: ___ (LinkedIn job postings → expanding which team?)
- Tech-stack change: ___ (BuiltWith diff)

## Stakeholder candidates (LinkedIn + Apollo)
| Name | Title | Function | Tenure | Influence | Personalization hook |
|---|---|---|---|---|---|

## ICP fit scoring
- Firmographic fit: __/40
- Pain signal fit: __/30
- Tech-stack fit: __/20
- Trigger event recency: __/10
- **Total: __/100** (≥ 70 = enter sequence)

## Value hypothesis
[One paragraph — what we'd help them solve, with evidence]

## Suggested entry play
- Channel: ___
- Personalization hook: ___
- Sequence: ___
```

---

## Win/loss post-mortem template

```markdown
# Post-Mortem — [Account] · [Won / Lost] · [Date]

## Deal context
- ACV: $__
- Cycle days: __
- Primary competitor: ___ (or "no competition")
- Industry / size / vertical: ___

## Trigger event (what initiated the deal)
[Plain-text — what made them buy / not buy at this moment]

## Our diagnosis quality
- Pain we identified: ___
- Was that the real pain? [Yes / Partially / No]
- What we missed: ___

## Decision criteria match
- Their stated criteria: ___
- Our score on each criterion (as they evaluated us): ___

## Competitor (if lost)
- Who: ___
- Why they won: [pricing / feature / relationship / brand / timing / other]
- What we'd need to change to win next time: ___

## What to repeat (won) / what to change (lost)
1. ___
2. ___
3. ___

## Structured tags
- Industry: ___
- Deal size tier: SMB / Mid / Enterprise
- Cycle band: < 30d / 30-90d / 90-180d / > 180d
- Primary competitor: ___
- Lost reason: [pricing / feature gap / no decision / chose competitor / timing / champion lost]
- Won reason: [pricing / feature win / champion advocacy / proof / timing / relationship]
```

---

## Battlecard template

```markdown
# Battlecard — [Us] vs [Competitor]

## Positioning
- Their pitch: ___
- Our counter-pitch: ___
- Unique to us: ___
- Unique to them: ___

## Where they win
- ___
- ___

## Where we win
- ___
- ___

## Traps to set (questions to ask that surface their weakness)
1. "Ask them about [feature/capability they don't have well]."
2. "Ask them about [pricing model gap]."

## Talk tracks
- "When prospects compare us to [X], here's what we say…"

## Proof points
- Customer case: ___
- Independent analyst: ___

## Pricing intel
- Their list: ___
- Their typical discount: ___
- Their contract terms: ___
```

---

## ROI calculator template

Inputs (user fills):
- Current spend on existing solution / process: $___ / year
- # of users / seats / units affected: ___
- Time spent per user per week on current process: __ hours
- Loaded labor cost per hour: $___
- Estimated efficiency gain with our solution: __% (use 20-30% conservative anchor)
- One-time switching cost: $___

Outputs (computed):
- Annual labor savings: (users × hours/week × 52 × $/hr × efficiency %)
- Software cost delta: (our annual price) − (current solution annual price)
- Net annual savings: labor savings + software delta − switching cost (amortized over 3 yr)
- Payback period (months): switching cost ÷ (monthly net savings)
- 3-yr ROI: (3 × annual savings) ÷ switching cost

Render as `xlsx` / `google-sheets` formula spreadsheet so prospects can edit inputs.

---

## SDR ↔ AE handoff template

```markdown
# Handoff — [Prospect] from [SDR] to [AE]

## Source
- Channel: ___
- First touch date: ___
- # touches before reply: ___

## Qualification (BANT / MEDDIC starter)
- Budget hint: ___
- Authority: ___ (role + name)
- Need: ___
- Timeline: ___
- Pain articulated by prospect: ___

## Key conversation snippets
> "Direct quote 1"
> "Direct quote 2"

## Agreed next step
- Action: ___
- Date/time: ___ (calendar slot booked)
- Channel: ___ (Zoom link / phone / in-person)

## Background
- LinkedIn: ___
- Account snapshot (1 paragraph): ___
- Tech stack: ___
- Recent triggers: ___

## SDR confidence
- ICP fit: __/10
- Buying signal strength: __/10
- Recommended priority: high / medium / low

## AE acceptance SLA
- Accept within 4 business hours OR return to SDR with rejection reason
- Rejection reasons: not-ICP / not-now / no-pain / wrong-region / duplicate
```

---

## Signal intent monitoring

### Sources to monitor + signal types

| Source | Signal type | Trigger threshold |
|---|---|---|
| Apollo "company news" | Funding, leadership change, product launch | Any |
| LinkedIn job-change alerts | Champion promotion, EB hire, lateral move | Champion role match |
| Crunchbase webhook | Funding round | Series A+ for ICP fit |
| BuiltWith diff | Tech-stack add/remove (Stripe, AWS, Snowflake, etc.) | Adjacent-tech add |
| Common Room | Community engagement (Slack, Discord, Reddit) | Active user score > threshold |
| Pocus / Koala | Product activity signal (signup, feature use, return visit) | Score > 50 |
| G2 / Capterra | Comparison-page visit | Visited our category |
| Bombora | Topic-intent surge | Surge score > 60 |
| Site visit (RB2B / Default) | Identified anonymous traffic | Pages/session > 3 |

### Daily digest

Cron via `postgresql-mcp` or Python `cli-anything` pulls all sources → ranks accounts by composite score → top-10 into "hot accounts" feed → CRM tasks created via `api-gateway` HubSpot `/crm/v3/objects/tasks`.

---

## Expansion playbook

### Trigger conditions (any one fires expansion outreach)

- Product usage > seat threshold (Pocus / Koala / PostHog)
- Adoption of > 2 modules
- NPS > 8 from key stakeholder
- Champion promoted internally
- Customer hiring in adjacent department (LinkedIn signals)
- Renewal date within 120 days

### Expansion motion

1. **Usage report** — past 90 days activity per user, value realized vs. baseline
2. **Exec QBR scheduled** — present usage + roadmap alignment + expansion options
3. **Multi-team rollout proposal** — additional seats, modules, or use cases
4. **Pricing presented** — anchor on % discount vs. list, not vs. their current price
5. **Mutual action plan** — same template as new deals

---

## Renewal playbook

### Pipeline opens 120 days pre-renewal

### Renewal-risk score (compute per account)

- Usage trend (90-day): up / flat / down
- Support ticket volume: low / medium / high
- NPS / CSAT: > 8 / 5-8 / < 5
- Champion status: engaged / quiet / left company
- Composite: Healthy / At-risk / Critical

### Healthy renewals

- Auto-renew motion: confirmation email 60 days out, light QBR, contract auto-sent
- Optional: try for expansion at renewal

### At-risk / critical renewals

- Save motion: exec QBR within 30 days, root-cause diagnosis, success plan, possibly pricing concession
- Coordinate with `customer-support-agent` for ticket resolution
- Escalate to leadership if save effort > 4 weeks

---

## Pricing strategy reference

### Anchor on closed-won comparables

Query: `closed-won deals in last 4 quarters, same vertical + size band` → median ACV, median discount %, contract length.

Anchor proposal at the 75th-percentile of comparables; give down to median; floor at 25th-percentile.

### Concession ladder

| Ask | Give | Get |
|---|---|---|
| 10% discount | Multi-year (3-yr) | Cash up-front |
| 15% discount | Reference call | Case study rights |
| 20% discount | Logo + co-marketing | Quarterly QBR with exec |
| > 20% discount | Escalate to `finance-controller` | — |

### Never discount without trade

Every concession comes with a get. Free concessions train the buyer to keep asking.

---

## Sales success metrics

### Outbound metrics
- Reply rate: > 5% (cold), > 15% (warm)
- Positive reply rate: > 1%
- Meetings booked per 1000 sends: > 8
- Cost per meeting booked: $50-150 (depending on enrichment costs)
- Bounce rate: < 2%
- Complaint rate: < 0.10%

### Pipeline metrics
- Coverage ratio: 3-4× quota
- Deal velocity (median close time by stage): tracked weekly
- Win rate (close-won / total closed): > 25% for healthy
- Average deal size: tracked by AE + tier
- Commit accuracy: > 80% per AE per quarter

### AE benchmarks
- Pipeline generated per week: $50K-200K (varies by stage/segment)
- Discovery → demo conversion: > 60%
- Demo → proposal conversion: > 40%
- Proposal → close conversion: > 30%
- Average sales cycle: tracked by segment (SMB < 30d, Mid 30-90d, Enterprise 90-180d+)

### SDR benchmarks
- Outbound activity per day: 50-80 touches (mix of email + LinkedIn + phone)
- SQL conversion: > 5% of dials, > 15% of warm replies
- SQL → AE acceptance: > 80%
- SQL → demo: > 50%

### Renewal / expansion metrics
- Gross revenue retention: > 90%
- Net revenue retention: > 110% (best-in-class > 120%)
- Renewal rate: > 90%
- Expansion deals per quarter: tracked

---

## SOTA tool reference (June 2026)

This section is grep-only — the agent uses keyword-driven retrieval to surface the right skill pack for the user's task. Headings are intentionally search-friendly. Every entry links to a detailed `SKILL.md` in `skills/` that ships in this bundle and loads on demand.

**Full coverage map:** see `reference/SOTA_USE_CASES.md` for the per-use-case mapping and confidence rating.

### HubSpot CRM (managed OAuth)

HubSpot is the default CRM for SMB and mid-market. Use the `api-gateway` skill's managed OAuth proxy (`gateway.maton.ai/hubspot/`) — covers contacts, companies, deals, line items, lists, properties, workflows, sequences, meetings, forms, pipelines.

- **Skill:** `skills/hubspot-sales-mcp/SKILL.md`
- **Endpoint:** `https://gateway.maton.ai/hubspot/crm/v3/...` via `api-gateway`
- **Auth:** Maton API key → managed OAuth to HubSpot account
- **Key calls:** `GET /crm/v3/objects/contacts`, `POST /crm/v3/objects/deals`, `POST /automation/v4/flows`, `PATCH /crm/v3/objects/contacts/{id}` (for scoring updates)
- **Source:** https://developers.hubspot.com/docs/api/crm/contacts

### Salesforce (managed OAuth)

Salesforce for enterprise. Use `salesforce-api` default skill + `api-gateway` for managed OAuth. SOQL for queries, Apex for complex logic, Composite API for bulk updates.

- **Skill:** `skills/salesforce-api/` (default skill) + `skills/hubspot-sales-mcp/SKILL.md` for cross-CRM patterns
- **Endpoint:** `https://gateway.maton.ai/salesforce/services/data/v60.0/...`
- **Key calls:** `SELECT Id, StageName, Amount, CloseDate FROM Opportunity WHERE IsClosed = FALSE`, `POST /sobjects/Opportunity`, `PATCH /sobjects/Opportunity/{id}`
- **Source:** https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/

### Apollo + Clay (lead enrichment waterfall)

Apollo is the primary enrichment source (270M+ contacts). Clay orchestrates multi-source waterfall (Apollo + Hunter + RocketReach + Dropcontact). Lusha for mobile phones. ZoomInfo for enterprise gaps. Cognism for EU-compliance.

- **Skill:** `skills/apollo-clay-lead-enrichment/SKILL.md`
- **Endpoints:** `https://gateway.maton.ai/apollo/api/v1/...`, `https://api.clay.com/v3/...`
- **Auth:** Maton API key + Clay API key
- **Key calls:** Apollo `POST /api/v1/mixed_people/search`, `POST /api/v1/organizations/enrich`; Clay workflow trigger
- **Source:** https://docs.apollo.io/reference/people-search + https://clay.com/docs/api

### Outreach + Salesloft + lemlist + Instantly (sequences)

Outreach and Salesloft for enterprise SDR teams; lemlist for personalized hybrid (email + LinkedIn); Instantly for scaled cold outbound. All four covered via `api-gateway` managed OAuth.

- **Skill:** `skills/outreach-salesloft-sequences/SKILL.md`
- **Endpoints:** `https://gateway.maton.ai/{outreach|salesloft|lemlist|instantly}/...`
- **Key calls:** Outreach `POST /api/v2/sequences`, Salesloft `POST /v2/cadences`, lemlist `POST /api/campaigns`, Instantly `POST /api/v2/campaigns`
- **Source:** https://developers.outreach.io/api/ + https://developers.salesloft.com/api.html

### Cold email deliverability + warmup

`dig` for SPF/DKIM/DMARC; mail-tester.com for inbox placement; Glock Apps for major-provider placement; Lemwarm / Instantly built-in warmup / Mailwarm for sender warmup; MXToolbox for blocklist checks.

- **Skill:** `skills/cold-email-deliverability-warmup/SKILL.md`
- **Tools:** `cli-anything` for `dig`, curl mail-tester.com, curl Glock Apps API; `api-gateway` for Lemwarm
- **Key checks:** SPF `~all`/`-all`, DKIM 2048-bit, DMARC `p=quarantine`/`p=reject`, complaint rate < 0.10%, mail-tester ≥ 9/10
- **Source:** https://lemwarm.com/ + https://www.mail-tester.com/

### Gong + Chorus + Fathom + Fireflies + tl;dv (call intelligence)

Gong is the enterprise standard; Chorus is similar (no public API — workaround via email export); Fathom + Fireflies + tl;dv are free/freemium notetakers with public APIs.

- **Skill:** `skills/gong-chorus-call-intelligence/SKILL.md`
- **Endpoints:** Gong `https://gateway.maton.ai/gong/v2/...`; Fathom via `fathom-api` default skill + `api-gateway`; Fireflies + tl;dv via `api-gateway`
- **Key calls:** Gong `GET /v2/calls/transcript?id=<id>`, `GET /v2/calls/stats`, Fathom `GET /external/v1/meetings`
- **Source:** https://app.gong.io/settings/api/documentation + https://help.fathom.video/en/articles/8430832-fathom-api

### MEDDIC + MEDDPICC + BANT + SPIN + Challenger qualification

Framework execution lives in the agent's reasoning + CRM custom fields. Score each field 0-3 per role.md rubric; store in CRM via `api-gateway`.

- **Skills:** `skills/meddic-meddpicc-qualification/SKILL.md` + `skills/bant-spin-challenger-frameworks/SKILL.md`
- **Mechanism:** CRM custom fields per framework letter; the agent fills based on discovery / call transcript / email replies; scoring rubric stored in `notion`

### Account research deep

Apollo + Clay + LinkedIn + BuiltWith + Crunchbase + brave-search composite. ICP-fit scoring rubric (firmographic + pain + tech-stack + trigger recency).

- **Skill:** `skills/account-research-deep/SKILL.md`
- **Mechanism:** Apollo `organizations/enrich` + Clay multi-source + LinkedIn via `linkedin` default + brave-search recent news + Crunchbase funding webhook → composite scored output

### LinkedIn Sales Navigator outreach

HeyReach (TOS-respectful), Phantombuster (broader), TexAu (cheaper) automate connections + DMs at safe daily volumes. Sales Nav has no public API.

- **Skill:** `skills/linkedin-sales-navigator-outreach/SKILL.md`
- **Mechanism:** HeyReach API via `api-gateway` if onboarded; otherwise Phantombuster via `cli-anything` curl. `brightdata-mcp` for Sales Nav scraping. Daily volume: 15-25 connections, 50 profile views, 100 search results — TOS-safe limits.
- **Source:** https://www.heyreach.io/ + https://phantombuster.com/

### Signal/intent monitoring

Common Room (community signals), Pocus (PLG), Koala (PLG), Apollo job-changes, Crunchbase funding, BuiltWith tech-stack diffs, RB2B (deanonymization), Default (signals dashboard).

- **Skill:** `skills/signal-intent-monitoring-pocus-koala-common-room/SKILL.md`
- **Mechanism:** Webhooks → `postgresql-mcp` or `cli-anything` cron → composite score → top-10 hot accounts → CRM tasks
- **Source:** https://www.commonroom.io/ + https://www.pocus.com/ + https://www.koala.io/

### Deal coaching next-best-action

Per-opp NBA framework. Compute 7 signals (MEDDIC completeness, age-in-stage, multi-thread depth, last-activity, sentiment, champion silence, decision-date drift), pick the single highest-value action, output literal execution copy.

- **Skill:** `skills/deal-coaching-next-best-action/SKILL.md`
- **Mechanism:** CRM read + Gong transcript signals + stakeholder map → reasoning → single NBA + literal copy

### Win/loss analysis structured

5-section post-mortem (trigger, diagnosis, criteria match, competitor, repeat/change) with structured tags. Quarterly rollup query for trend analysis.

- **Skill:** `skills/win-loss-analysis-structured/SKILL.md`
- **Mechanism:** Deal pull + linked calls + sentiment snippets → fill template → store in `notion` DB → quarterly rollup

### PandaDoc + DocuSign (proposals + e-sign)

PandaDoc for proposal-native (template + CRM tokens + e-sign); DocuSign for enterprise e-sign with separate proposal source. Both via `api-gateway`.

- **Skill:** `skills/pandadoc-docusign-proposal-pipeline/SKILL.md`
- **Endpoints:** `https://gateway.maton.ai/pandadoc/public/v1/...`; `https://gateway.maton.ai/docusign/restapi/v2.1/...`
- **Key calls:** PandaDoc `POST /documents` (from template), DocuSign `POST /envelopes`
- **Source:** https://developers.pandadoc.com/ + https://developers.docusign.com/docs/esign-rest-api/

### Clari + Gong Forecast + BoostUp (forecasting)

Forecasting tools with predictive ML. Clari is enterprise-default; Gong Forecast integrates with call data; BoostUp is mid-market. Manual fallback via CRM + Google Sheets always available.

- **Skill:** `skills/clari-forecasting-commit-accuracy/SKILL.md`
- **Mechanism:** CRM deal pull → three-bucket categorization → commit accuracy tracking → per-AE breakdown
- **Source:** https://www.clari.com/blog/sales-forecasting-methods/

### Pipeline hygiene + stage criteria

Stage definitions with entry/exit gates, age-in-stage flagging, stalled-deal detection, coverage ratio computation.

- **Skill:** `skills/pipeline-hygiene-stage-criteria/SKILL.md`
- **Mechanism:** CRM query + stage criteria check + render to `notion` pipeline doc

### Sales enablement (battlecards, ROI calculators, case studies)

Battlecards in `pptx`; ROI calculators in `xlsx` / `google-sheets`; case studies in `docx` / `pdf`.

- **Skill:** `skills/sales-enablement-battlecards-roi-calculators/SKILL.md`
- **Mechanism:** Template + content + render

### Multi-threading enterprise

Stakeholder map + engagement depth + coordinated outreach to silent stakeholders.

- **Skill:** `skills/multi-threading-enterprise-deals/SKILL.md`
- **Mechanism:** CRM stakeholder fields + Sales Nav for org chart + content gifts via `marketing-agent` coordination

### Expansion + renewal playbook

PLG signals (Pocus / Koala / PostHog) → expansion trigger → QBR → multi-team rollout proposal. Renewal pipeline opens 120 days pre-renewal-date with health scoring.

- **Skill:** `skills/expansion-upsell-renewal-playbook/SKILL.md`
- **Mechanism:** `posthog-mcp` usage signals + CRM contract dates + composite health score

### Calendly + meeting booking

Calendly v2 API via `api-gateway` + `calendly-api` default skill. Create scheduling links, round-robin assignment, pre-meeting questionnaire to CRM.

- **Skill:** `skills/calendly-api/` (default skill)
- **Endpoint:** `https://gateway.maton.ai/calendly/scheduled_events` + `https://api.calendly.com/v2/`
- **Source:** https://developer.calendly.com/api-docs/

### Slack / Teams sales rooms

`slack` + `microsoft-teams` default skills for sales-room notifications. CRM webhook → Slack post on closed-won, slip-risk alerts, hot-account signals.

- **Mechanism:** `slack-mcp` `chat.postMessage`; `ms-teams-mcp` channel post; webhook from CRM via Maton

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| Design an outbound sequence | `outreach-salesloft-sequences` | Multi-channel; A/B variants; Targets table |
| Set up cold-email warmup | `cold-email-deliverability-warmup` | SPF/DKIM/DMARC first; 4-week warmup before launch |
| Enrich a target list | `apollo-clay-lead-enrichment` | Waterfall: Apollo → Clay → Lusha → ZoomInfo |
| Run a pipeline review | `pipeline-hygiene-stage-criteria` | Weekly cadence; stage criteria; coverage ratio |
| Score a deal (MEDDIC/MEDDPICC) | `meddic-meddpicc-qualification` | Rubric 0-3 per field; roll-up to bucket |
| Score a deal (BANT/SPIN) | `bant-spin-challenger-frameworks` | BANT for transactional; SPIN for discovery; Challenger for commercial |
| Prep a discovery call | `account-research-deep` + `meddic-meddpicc-qualification` | Brief template; 5-7 SPIN questions; MEDDIC checklist |
| Prep a demo | `sales-enablement-battlecards-roi-calculators` | Storyline; feature→pain mapping; battlecard |
| Coach an open deal | `deal-coaching-next-best-action` | Compute 7 signals; pick ONE NBA; literal copy |
| Multi-thread an enterprise deal | `multi-threading-enterprise-deals` | Stakeholder map; engagement depth target by deal size |
| Generate a proposal | `pandadoc-docusign-proposal-pipeline` | PandaDoc (proposal-native) or DocuSign (e-sign only) |
| Run win/loss | `win-loss-analysis-structured` | 5-section template; structured tags; quarterly rollup |
| Build a forecast | `clari-forecasting-commit-accuracy` | Three buckets; commit accuracy per AE |
| Monitor intent signals | `signal-intent-monitoring-pocus-koala-common-room` | Daily digest; CRM task creation |
| Plan an expansion play | `expansion-upsell-renewal-playbook` | Usage signal → QBR → multi-team rollout |
| Plan a renewal | `expansion-upsell-renewal-playbook` | 120 days pre-renewal; health score; save motion if at-risk |
| Analyze a Gong call | `gong-chorus-call-intelligence` | Talk-listen ratio; objection mining; sentiment trajectory |
| LinkedIn outbound | `linkedin-sales-navigator-outreach` | HeyReach / Phantombuster / TexAu; safe daily limits |
| Build a battlecard | `sales-enablement-battlecards-roi-calculators` | Positioning, win/lose, traps, proof points |
| Build an ROI calculator | `sales-enablement-battlecards-roi-calculators` | Inputs + computed outputs; render to xlsx/sheets |
| SDR ↔ AE handoff | `meddic-meddpicc-qualification` | Handoff template; 4-hour AE acceptance SLA |
| Negotiation prep | `deal-coaching-next-best-action` | BATNA, ZOPA, concession ladder; closed-won comps |
| Pricing strategy | `expansion-upsell-renewal-playbook` | Closed-won comparables; corridor + concession menu |
| Book a meeting | `calendly-api` (default skill) | Create scheduling link; round-robin |

---

## Closing rules

Outbound is a system, not a hustle. Qualify in or out fast — pick ONE framework per deal. Pipeline hygiene is the daily job. Multi-thread or die. Forecast in three buckets. Win/loss every close. When depth is required, call in a specialist.
