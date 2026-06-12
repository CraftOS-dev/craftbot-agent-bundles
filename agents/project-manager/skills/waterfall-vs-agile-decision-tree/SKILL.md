<!--
Source: https://thecynefin.co/about-us/about-cynefin-framework
Source: https://www.axelos.com/certifications/propath/prince2-agile-project-management
-->
# Waterfall vs Agile vs Hybrid Decision Tree — SKILL

Cynefin classification + decision matrix (req stability / customer involvement / team size / regulatory / speed / uncertainty). Hybrid patterns: PRINCE2 Agile, Water-Scrum-Fall, DA, Scrum+Stage-Gate.

## When to use

- Selecting methodology at project kickoff or charter authoring.
- Justifying methodology choice in charter section 11.
- Migrating a project from one methodology to another (e.g., waterfall → agile after discovery).
- Diagnosing methodology fit when project is failing (wrong tool, not wrong execution).

Trigger phrases: "waterfall or agile", "methodology selection", "pick methodology", "hybrid", "Cynefin", "PRINCE2 Agile", "water-scrum-fall", "which framework".

## Setup

```bash
# No tooling — this is a decision-tree skill
# Output: Notion decision-tree page + charter section 11 rationale
```

## Common recipes

### Recipe 1: Cynefin domain classification
```
              KNOWN          │      KNOWABLE
                             │
       CLEAR                 │     COMPLICATED
   (cause-effect obvious)    │ (cause-effect knowable
                             │   with expertise)
   Best practice              │  Good practice
   → Sense-categorize-respond │  → Sense-analyze-respond
   FITS: Waterfall            │  FITS: PRINCE2 / Waterfall
─────────────────────────────┼─────────────────────────────
                             │
       CHAOTIC               │     COMPLEX
   (no cause-effect)         │ (cause-effect retrospective
                             │   only)
   Novel practice            │  Emergent practice
   → Act-sense-respond       │  → Probe-sense-respond
   FITS: Lean / triage       │  FITS: Agile / Scrum
                             │
              UNKNOWN         │     UNKNOWABLE

  + APORETIC / CONFUSED      (don't know which domain)
    → Diagnose first
```

### Recipe 2: Methodology decision matrix
```
Factor                    | Waterfall      | Agile        | Hybrid
─────────────────────────┼────────────────┼──────────────┼────────────────
Requirements stability   | Stable         | Volatile     | Mixed
Customer involvement     | Low-medium     | High         | Medium
Team size                | Any            | Small-medium | Large/coordinated
Regulatory environment   | Heavy          | Light        | Medium-heavy
Speed-to-value priority  | Medium         | High         | Medium-high
Uncertainty              | Low            | High         | Medium
Document-driven          | Yes            | Light        | Medium
Cynefin domain           | Clear/Complicated | Complex   | Complex+Complicated
Cycle length             | Months         | 1-4 weeks    | Phase-dependent
Change tolerance         | Low (CR-gated) | High         | CR for outer; agile inner
```

### Recipe 3: Decision-tree walkthrough
```
Q1: Are requirements likely to change >20% during project?
  YES → continue Q2 (agile-leaning)
  NO  → continue Q3 (waterfall-leaning)

Q2 (agile-leaning):
  Is the team co-located + small (<10) + autonomous?
    YES → Scrum (2-wk cycles)
    NO  → SAFe / LeSS / Nexus (scaled agile)

Q3 (waterfall-leaning):
  Is the project regulated (FDA, FAA, banking, gov)?
    YES → Waterfall + Stage-Gate
    NO  → continue Q4

Q4:
  Are early phases low-uncertainty (e.g., requirements known) but
  later phases high-uncertainty (e.g., novel UX)?
    YES → Water-Scrum-Fall (hybrid)
    NO  → PRINCE2 (process-driven waterfall)

Q5 (any path):
  Is sponsor governance heavy (steering committee, board oversight)?
    YES → add Stage-Gate decisions
    NO  → standard methodology
```

### Recipe 4: Common hybrids
```
PRINCE2 Agile
  - PRINCE2 governance + stage management
  - Scrum/Kanban delivery within stages
  - Used in regulated industries with agile teams
  - AXELOS certified

Water-Scrum-Fall
  - Waterfall requirements + architecture
  - Scrum delivery (sprints)
  - Waterfall release + ops handoff
  - Common in enterprise IT

Disciplined Agile (DA)
  - Context-driven scaling
  - Lifecycle picker per team
  - PMI-backed (since 2019)

Scrum + Stage-Gate
  - Sprint within phase
  - Stage-gate decisions between phases
  - Common: G0-G2 waterfall planning + G3 scrum delivery + G4-G5 waterfall launch/close
```

### Recipe 5: Methodology charter section 11 template
```markdown
## 11. Methodology

**Selected:** [Waterfall / Scrum / Kanban / SAFe / PRINCE2 / PRINCE2 Agile / Water-Scrum-Fall / Hybrid]

**Cynefin domain classification:**
- Discovery phase: [Complicated — req known, design discoverable]
- Build phase: [Complex — UX iterative, integration unknowns]
- Launch phase: [Complicated — staged rollout sequence known]

**Decision factor scoring:**
| Factor | Score (1-5) | Notes |
|---|---|---|
| Requirements stability | 3 | Core scope locked; UX detail iterative |
| Customer involvement | 4 | 5 design partners in beta cohort |
| Team size | 2 | 6 contributors |
| Regulatory environment | 2 | Light (data-privacy basics) |
| Speed-to-value priority | 4 | Q3 hard deadline |
| Uncertainty | 3 | Mid — known goal, unknown UX |

**Rationale:** Hybrid (Water-Scrum-Fall + Stage-Gate).
- Waterfall discovery (4 weeks) — requirements + design + WBS lock at G2.
- Scrum delivery (8 weeks, 4 × 2-wk cycles) — sprint goal singular outcome; Linear cycles.
- Waterfall launch (1 week) — staged rollout 10/50/100%, signed BAU handoff.
- Stage-gates G0/G1/G2/G3/G4/G5 (cross-link stage-gate-reviews-phase-zero-to-close).

**Alternatives considered:**
- Pure Scrum: rejected — sponsor needs predictable Q3 ship date (cycle-based forecasting too noisy).
- Pure Waterfall: rejected — UX uncertainty makes 12-week up-front design risky.
- SAFe: rejected — single team; framework overhead exceeds project size.
```

### Recipe 6: Cynefin self-diagnostic questions
```
For your project, answer:

1. Can a domain expert predict the outcome of "if we do X, then Y will happen"?
   Always → Clear (waterfall)
   With study → Complicated (PRINCE2/waterfall)
   Only after the fact → Complex (agile)
   No predictability → Chaotic (triage)

2. How often do requirements change?
   Rarely → Clear / Complicated
   Often → Complex
   Daily → Chaotic

3. Customer feedback cycle?
   Asynchronous review at phase end → Waterfall fits
   Continuous (every 1-2 weeks) → Agile fits
   Real-time → Continuous deployment / DevOps

4. Outcome measurement?
   Pre-defined at start (clear KPIs) → Waterfall / hybrid
   Discovered through iteration → Agile
   Defined retrospectively → Complex / Lean
```

### Recipe 7: Methodology selection sponsor brief
```markdown
# Methodology Recommendation — [Project]

## TL;DR
Recommend: Water-Scrum-Fall with Stage-Gate G0/G2/G4
Confidence: 85%

## Why
- Q3 hard deadline + measurable success criteria → waterfall plan
- UX iteration needed → scrum delivery
- Sponsor governance + cross-team coords → stage-gates

## Tradeoffs
- Slightly heavier than pure scrum (overhead: stage-gate prep ~1 day each)
- Slightly lighter than pure waterfall (no 12-wk design up front; iterative)

## Alternatives rejected
1. Pure scrum — sponsor needs commitment date; velocity noisy on new team
2. Pure waterfall — UX iteration would require 3-5 CR cycles

## Decision needed
[ ] Approve Water-Scrum-Fall hybrid
[ ] Approve pure scrum
[ ] Approve pure waterfall
[ ] Discuss tradeoffs further

— PM, [date]
```

### Recipe 8: Migration trigger criteria
```
Switch waterfall → agile WHEN:
- Discovery phase reveals high UX uncertainty
- Customer feedback contradicts charter assumption
- Velocity / progress slower than waterfall plan suggests

Switch agile → waterfall WHEN:
- Sponsor needs commit date for board / partner
- Regulatory phase enters (e.g., security review with fixed gate)
- Scope crystallizes after 2-3 sprints of discovery

Switch standalone → hybrid WHEN:
- Multi-phase project (discovery + build + launch) with different uncertainty
- Cross-team coordination needs structured handoffs
- Stage-gate review process required by org

Trigger criteria checklist:
- [ ] Two consecutive RED status weeks without recovery
- [ ] Stakeholder satisfaction below threshold
- [ ] Velocity unpredictable (>30% sprint variance)
- [ ] Charter assumptions invalidated
```

### Recipe 9: SAFe vs LeSS vs Nexus (for scaled environments)
```
Need scaled agile (multi-team coordinated)?

SAFe — heaviest, most prescriptive
  - PI planning (10-week)
  - ARTs (Agile Release Trains)
  - LACE (Lean-Agile Center of Excellence)
  - Fits: 50-200+ contributors; enterprise
  - Overhead: high

LeSS — lighter
  - One product owner across teams
  - Common backlog
  - Fits: 2-8 scrum teams
  - Overhead: low

Nexus — Scrum.org's scaling pattern
  - 3-9 scrum teams
  - Nexus Integration Team coordinates
  - Fits: tightly coupled product work
  - Overhead: medium
```

### Recipe 10: PRINCE2 vs PMBOK 7 (for governance-heavy)
```
PRINCE2 — process-driven (UK origin)
  - 7 principles, 7 themes, 7 processes
  - Stage management mandatory
  - Strong documentation discipline
  - AXELOS certified
  - Fits: gov, regulated, audit-heavy environments

PMBOK 7 — principles-based (PMI)
  - 12 principles + 8 performance domains
  - Tailoring built in
  - More flexible than PRINCE2
  - PMP certified
  - Fits: most enterprise projects

PRINCE2 Agile — hybrid
  - PRINCE2 governance + agile delivery
  - Used when org needs PRINCE2 audit + team wants scrum

Don't pick PRINCE2 just because team has PMP — pick by governance needs.
```

### Recipe 11: Methodology choice red flags
```
PICK ANOTHER METHODOLOGY WHEN:

For Waterfall:
- "We don't have requirements yet but want to start building" → use agile
- "We need to show progress every 2 weeks" → use agile
- "Customer involvement is high" → use agile

For Agile:
- "Sponsor needs ship date guaranteed 6 months out" → use hybrid or waterfall
- "Compliance requires fixed phases with audit" → use waterfall or PRINCE2
- "Team is distributed across 3 continents with no overlap" → use modified async-scrum or scrumban

For SAFe:
- "We're 1 team of 5" → use scrum (don't add SAFe overhead)
- "We hate process" → use Kanban
```

### Recipe 12: Methodology decision flowchart (Excalidraw)
```bash
mcp tool excalidraw.generate_diagram \
  --type "flowchart" \
  --nodes '[
    {"id":"start","label":"Methodology choice","shape":"oval"},
    {"id":"q1","label":"Req stability >20% change?","shape":"diamond"},
    {"id":"q2","label":"Regulated industry?","shape":"diamond"},
    {"id":"q3","label":"Team co-located <10?","shape":"diamond"},
    {"id":"q4","label":"Multi-phase mixed uncertainty?","shape":"diamond"},
    {"id":"waterfall","label":"WATERFALL","shape":"rect","color":"blue"},
    {"id":"prince2","label":"PRINCE2 (or PRINCE2 Agile)","shape":"rect","color":"navy"},
    {"id":"scrum","label":"SCRUM","shape":"rect","color":"green"},
    {"id":"safe","label":"SAFe / LeSS / Nexus","shape":"rect","color":"orange"},
    {"id":"hybrid","label":"WATER-SCRUM-FALL","shape":"rect","color":"purple"}
  ]' \
  --edges '[
    {"from":"start","to":"q1"},
    {"from":"q1","to":"q3","label":"yes"},
    {"from":"q1","to":"q2","label":"no"},
    {"from":"q3","to":"scrum","label":"yes"},
    {"from":"q3","to":"safe","label":"no (>10 or distributed)"},
    {"from":"q2","to":"prince2","label":"yes"},
    {"from":"q2","to":"q4","label":"no"},
    {"from":"q4","to":"hybrid","label":"yes"},
    {"from":"q4","to":"waterfall","label":"no"}
  ]'
```

## Examples

### Example 1: Pick methodology at charter time
**Goal:** Onboarding revamp Q3 — what methodology?

**Steps:**
1. Walk Recipe 3 decision tree → Water-Scrum-Fall.
2. Score Recipe 2 matrix.
3. Fill Recipe 5 charter section 11.
4. Sponsor brief (Recipe 7) — approve.
5. Generate Recipe 12 flowchart for charter.

**Result:** Methodology locked + justified in charter.

### Example 2: Migrate methodology mid-project
**Goal:** Pure scrum, 4 sprints in; sponsor needs ship date guarantee.

**Steps:**
1. Recipe 8 trigger criteria — yes.
2. Propose migration to Water-Scrum-Fall (lock scope at next stage-gate).
3. Sponsor brief (Recipe 7) — approve.
4. CCB approve change in process (CR via change-request-management).
5. Re-baseline charter v2.0; insert stage-gate G3 → G4 → G5.
6. Communicate to team.

**Result:** Methodology change documented; ship date locked.

### Example 3: Justify rejecting SAFe on a small project
**Goal:** VP suggests SAFe; PM thinks overkill.

**Steps:**
1. Score Recipe 2 — team size = 6, single product, no PI planning needed.
2. Recipe 9 — SAFe overhead doesn't fit < 50 contributors.
3. Recipe 7 brief — recommend scrum; explain SAFe alternatives rejected.
4. VP signs off.

**Result:** Saved 2-3 weeks of SAFe ramp + recurring PI planning overhead.

## Edge cases / gotchas

- **"Agile" ≠ "no plan."** Agile has plans; they just evolve. Anti-pattern is "we're agile so we don't need a charter."
- **"Waterfall" ≠ "no iteration."** Waterfall can iterate within phases; the boundary is phase-to-phase, not no-iteration.
- **Methodology religion.** Team loyalty to a methodology can outweigh fit. Discuss at retro.
- **Cynefin domains are fluid.** A project can move from Complex → Complicated as discovery reveals knowables.
- **Hybrid is the modal answer.** Most real projects are hybrids; pure forms rare.
- **Hybrid without governance discipline = chaos.** Stage-gates need real entry criteria; sprints need real DoR.
- **PMBOK vs PRINCE2 isn't methodology vs methodology.** PMBOK = body of knowledge; PRINCE2 = specific process. PMBOK + Scrum is fine.
- **SAFe is heavy.** Adopting SAFe requires LACE + PI planning + training. Don't add for <30 contributors.
- **Stage-gate ≠ waterfall.** Stage-gates can wrap any methodology, including agile.
- **Cynefin "aporetic" domain.** When you don't know the domain, diagnose before picking methodology.
- **Org constraint ≠ methodology choice.** "We use Jira" doesn't decide waterfall vs agile.
- **Speed of change.** A project changing methodology mid-flight needs recharter, not just process tweaks.
- **Methodology debt.** Wrong methodology compounds. Cost of switching at month 3 < cost of finishing wrong.
- **Team capability.** Team may need training (Scrum, SAFe certs) before methodology works. Factor in ramp cost.
- **Customer maturity.** Customers used to waterfall (RFP / contract / acceptance) may resist agile (continuous deliveries).

## Sources

- [Cynefin framework explained](https://thecynefin.co/about-us/about-cynefin-framework)
- [PRINCE2 Agile (AXELOS)](https://www.axelos.com/certifications/propath/prince2-agile-project-management)
- [SAFe framework](https://www.scaledagileframework.com)
- [LeSS (Large-Scale Scrum)](https://less.works)
- [Nexus framework](https://www.scrum.org/resources/scaling-scrum)
- [Disciplined Agile (PMI DA)](https://www.pmi.org/disciplined-agile)
- [Scrum Guide](https://www.scrum.org/resources/scrum-guide)
- [PMBOK 7th Edition (PMI)](https://www.pmi.org/standards/pmbok)
- [Water-Scrum-Fall (Forrester)](https://www.forrester.com/blogs/water-scrum-fall-is-the-reality-of-agile-for-most-organizations/)
- [Project management methodology guide (Atlassian)](https://www.atlassian.com/agile/project-management/methodologies)
