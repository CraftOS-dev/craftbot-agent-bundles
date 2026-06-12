<!--
Source: https://monday.com/blog/project-management/gate-review/
Source: https://planisware.com/glossary/phase-gate-or-stage-gate
-->
# Stage-Gate Reviews (Phase 0 → Close) — SKILL

Formal go/kill/hold/recycle/conditional-go decision points between phases. Standard sequence: G0 concept → G1 feasibility → G2 planning → G3 execution → G4 launch → G5 close. Each gate has entry criteria + decision rubric + decision documented.

## When to use

- Scheduling and facilitating a stage-gate review (G0 through G5).
- Authoring entry criteria for a stage-gate.
- Capturing CCB decision: go / kill / hold / recycle / conditional go.
- Closing a project via G5 (cross-references closure checklist).
- Auditing gate compliance for governance / regulated industries.

Trigger phrases: "stage gate", "phase gate", "G0", "G1", "G2", "G3", "G4", "G5", "gate review", "go/no-go", "kill or continue", "phase review", "closure".

## Setup

```bash
# Notion DB for gate templates + decision log
mcp tool notion.search_pages --query "stage gate"

# Gmail for committee comms + decision capture
```

## Common recipes

### Recipe 1: Standard stage-gate sequence (Cooper-style)
```
G0 — CONCEPT (Idea screening)
  Question: "Is this problem worth solving?"
  Deliverables: 1-page brief, RICE score, strategic alignment
  Decision: pursue or shelve

G1 — FEASIBILITY (Scoping)
  Question: "Is it technically + economically feasible?"
  Deliverables: draft charter, high-level architecture, market evidence
  Decision: invest in detailed planning

G2 — PLANNING (Build the business case)
  Question: "Is it planned + chartered?"
  Deliverables: full charter, WBS, Gantt, RAID, budget, baseline locked
  Decision: commit to delivery

G3 — EXECUTION (Mid-build review)
  Question: "Is it on track mid-delivery?"
  Deliverables: status reports + EVM + risk burn-down + beta evidence
  Decision: continue / pivot / kill

G4 — LAUNCH READINESS
  Question: "Is it ready to ship?"
  Deliverables: UAT pass, launch plan, BAU handoff, training, support readiness
  Decision: go-live or hold

G5 — CLOSE (Post-launch)
  Question: "Is it complete + accepted? Did it achieve outcomes?"
  Deliverables: outcomes vs success criteria, lessons learned, archive
  Decision: formally close + schedule +30/60/90 PIR
```

### Recipe 2: Gate decision outcomes (Cooper)
```
GO              — proceed to next phase as planned
KILL            — terminate project (no value remaining)
HOLD            — pause; revisit at next gate or after named dependency
RECYCLE         — repeat current phase with named corrections
CONDITIONAL GO  — proceed with stated conditions / milestones

Don't add "approve with comments" — it's recycle if conditions are pre-phase work, otherwise it's conditional go.
```

### Recipe 3: Gate template (markdown)
```markdown
# Stage-Gate Review — G[X] [Phase Name] — [Project]

**Date:** [YYYY-MM-DD]
**Review committee:** [Names + roles]
**Facilitator:** [PM]
**Required attendees:** [Sponsor, Eng Lead, Design Lead, ...]
**Quorum:** [N of M required]

## 1. Entry criteria checklist
Each must be ✓ before review proceeds. If any ✗, recycle.

- [ ] [Deliverable 1 complete] — Owner: [Name] — Location: [Link]
- [ ] [Deliverable 2 reviewed] — Owner: [Name]
- [ ] [Sign-off captured from X] — Owner: [Name]
- [ ] [Acceptance Criteria validated] — Owner: [Name]

## 2. Review materials (pre-read)
- [Link to plan / status / RAID / budget]
- [Link to design / architecture / prototype]
- [Link to evidence / data / customer feedback]

## 3. Decision rubric
| Criterion | Threshold | Actual | Status |
|---|---|---|---|
| Scope clarity | Defined + signed | … | ✓/✗ |
| Schedule feasibility | Critical path computed | … | ✓/✗ |
| Budget within envelope | Within +10% | … | ✓/✗ |
| Risk level | No open RED-zone risks unmitigated | … | ✓/✗ |
| Resource availability | Plan reviewed | … | ✓/✗ |
| Strategic alignment | Score ≥ 75 | … | ✓/✗ |
| [Phase-specific criterion] | | | |

## 4. Open risks at this gate
[Top-3 from RAID]

## 5. Discussion notes
[Decisions raised, debate captured]

## 6. Decision
- Outcome: [GO / KILL / HOLD / RECYCLE / CONDITIONAL GO]
- Vote: [N approve / N reject / N abstain]
- Conditions (if any): [List]
- Next gate target date: [YYYY-MM-DD]
- Approvers (signed): [Names]
- Decision rationale: [Why]

## 7. Communication plan
- Stakeholders notified by: [date]
- RAID updated by: [date]
- Baseline impact: [if any, link to CR]
```

### Recipe 4: G0 (Concept) entry criteria
```
- [ ] 1-page problem brief (problem, evidence, opportunity size)
- [ ] Initial RICE score
- [ ] Strategic alignment scoring (≥50 to pass)
- [ ] Sponsor identified + tentative
- [ ] No obvious deal-breakers (legal, IP, market)
- [ ] Cost of pursuing G1 (research, design spike) estimated
```

### Recipe 5: G1 (Feasibility) entry criteria
```
- [ ] Draft charter v0.x
- [ ] Architecture sketch + integration map
- [ ] Market evidence (≥1 customer ask OR data point)
- [ ] High-level cost estimate (BAC ±50%)
- [ ] Identified-risk count + top-3 risks
- [ ] Methodology hypothesis (waterfall / agile / hybrid)
- [ ] Required tech feasibility spike completed (if uncertain)
```

### Recipe 6: G2 (Planning / Baseline lock) entry criteria
```
- [ ] Charter signed (v1.0)
- [ ] WBS complete + dictionary
- [ ] Gantt + critical path identified
- [ ] Budget locked (BAC) + contingency justified
- [ ] RAID populated (≥5 risks scored)
- [ ] Stakeholder comms plan
- [ ] RACI matrix
- [ ] Methodology choice justified
- [ ] All baselines snapshot + archived
```

### Recipe 7: G3 (Execution mid-review) entry criteria
```
- [ ] Status report current (≤1 week old)
- [ ] EVM snapshot (CPI / SPI / EAC)
- [ ] Risk burn-down chart
- [ ] Top-5 risks reviewed + owned
- [ ] Beta evidence (if applicable) — design partners using
- [ ] Customer feedback synthesized
- [ ] CR queue health (% approved, cycle time)
```

### Recipe 8: G4 (Launch readiness) entry criteria
```
- [ ] UAT pass (≥X% of test cases)
- [ ] Acceptance criteria validated per WBS deliverable
- [ ] Launch plan signed (staged rollout, comms, rollback)
- [ ] BAU handoff plan (support, ops, training)
- [ ] Documentation complete (user docs, support runbooks, eng docs)
- [ ] Analytics instrumentation live + verified
- [ ] All RED-zone risks mitigated or accepted
- [ ] Sponsor sign-off captured
- [ ] Compliance check (security, legal, privacy)
- [ ] Rollback plan tested
```

### Recipe 9: G5 (Close) entry criteria
```
- [ ] Project launched + accepted by sponsor
- [ ] All deliverables accepted
- [ ] All vendor SOWs marked complete
- [ ] All invoices reconciled
- [ ] Team members deallocated
- [ ] Lessons learned doc captured
- [ ] Retro completed
- [ ] Decision log archived
- [ ] Project archive folder complete
- [ ] Final stakeholder report sent
- [ ] +30/60/90 PIR scheduled
```

### Recipe 10: Capture gate decision in Notion DB
```bash
mcp tool notion.create_page \
  --parent '{"database_id":"<gate-decision-db>"}' \
  --properties '{
    "Name":{"title":[{"text":{"content":"G3 — Onboarding Revamp — 2026-07-15"}}]},
    "Project":{"relation":[{"id":"<project-id>"}]},
    "Gate":{"select":{"name":"G3"}},
    "Date":{"date":{"start":"2026-07-15"}},
    "Decision":{"select":{"name":"CONDITIONAL GO"}},
    "Conditions":{"rich_text":[{"text":{"content":"1) Resolve R-007 by Jul 22; 2) Mobile parity CR-009 finalized"}}]},
    "Approvers":{"multi_select":[{"name":"Sponsor"},{"name":"VP Eng"},{"name":"Steering"}]},
    "Rationale":{"rich_text":[{"text":{"content":"Project on track; 1 critical risk in flight with mitigation; sponsor wants weekly tighter cadence until risk closes."}}]}
  }'
```

### Recipe 11: Committee comms via gmail
```bash
mcp tool gmail.send_message \
  --to "vp-product@company.com,vp-eng@company.com,steering@company.com" \
  --cc "pm@company.com" \
  --subject "G3 Stage-Gate Review — Onboarding Revamp — Friday 2026-07-15 10:00" \
  --body "$(cat <<EOF
Committee,

G3 review scheduled Friday 10:00am.

Entry criteria status: 7/7 ✓ (full status report attached)

Review materials (pre-read by Thu EOD):
- Status report: <notion-link>
- EVM snapshot: <link>
- Risk burn-down + top-3: <link>
- Customer feedback synthesis: <link>

Decision framework (Recipe 3):
- Go: proceed to G4 launch
- Conditional go: continue with stated conditions
- Hold: pause; named dependency to resolve
- Recycle: defects must be addressed in current phase
- Kill: terminate (no business case remaining)

PM recommendation: CONDITIONAL GO (mitigations on R-007).

— PM
EOF
)"
```

### Recipe 12: Gate decision audit / compliance log
```sql
-- For regulated industries (FDA, FAA, banking):
SELECT
  project_name,
  gate,
  decision_date,
  decision,
  approvers_count,
  conditions,
  rationale
FROM gate_decisions
WHERE project_id = X
ORDER BY decision_date;

-- Audit trail: every gate has documented decision + approvers + rationale.
```

### Recipe 13: Gate review meeting agenda (60 min)
```
00-05 min | Confirm quorum + entry criteria status
05-15 min | Project overview (PM) — recap goals, current phase
15-30 min | Status review — RAG / EVM / risks
30-40 min | Discussion (decision rubric)
40-50 min | Decision deliberation + vote
50-55 min | Conditions / next-gate plan
55-60 min | Captures (Recipe 10) + comms (Recipe 11)
```

### Recipe 14: Quarterly gate compliance check
```python
# gate-compliance.py
import json
gates = json.load(open("gates.json"))  # all gate records
projects = json.load(open("projects.json"))

for proj in projects:
    proj_gates = [g for g in gates if g["project_id"] == proj["id"]]
    expected_through_phase = {"G0":1,"G1":2,"G2":3,"G3":4,"G4":5,"G5":6}.get(proj["phase"], 0)
    actual = len(proj_gates)
    if actual < expected_through_phase:
        print(f"COMPLIANCE GAP: {proj['name']} in phase {proj['phase']} but only {actual} gates recorded (expected {expected_through_phase})")
```

## Examples

### Example 1: G2 baseline-lock review
**Goal:** Charter, WBS, Gantt, budget done; lock baseline at G2.

**Steps:**
1. Pre-meeting: verify Recipe 6 entry criteria.
2. Schedule meeting + send Recipe 11 invite.
3. Run Recipe 13 agenda.
4. Decision: GO to execution.
5. Recipe 10 capture decision.
6. Recipe 11 follow-up comms.
7. Baseline locked in Notion + Smartsheet (cross-link scope-creep-prevention).

**Result:** Baseline locked; G3 target set; team starts execution Mon.

### Example 2: G3 mid-execution review surfaces problems
**Goal:** Week 4 of execution; status RED 2 weeks running.

**Steps:**
1. Recipe 7 entry criteria — 4/7 ✓; recycle considered.
2. Committee discussion: kill / recycle / conditional go.
3. Decision: CONDITIONAL GO with conditions (mitigation timeline, weekly tighter cadence).
4. Recipe 10 capture; Recipe 11 comms.
5. Conditions tracked in RAID + status reports.

**Result:** Project not killed but on probation; next G3 review in 4 weeks.

### Example 3: G5 close review
**Goal:** Project shipped 3 weeks ago; close formally.

**Steps:**
1. Recipe 9 entry criteria all ✓.
2. Final stakeholder report (Lessons learned + outcomes vs criteria).
3. Recipe 13 agenda — short (30 min).
4. Decision: CLOSED.
5. +30/60/90 PIR scheduled (cross-link closure playbook in role.md).
6. Archive complete; team deallocated.

**Result:** Clean closure; lessons captured; PIR pipeline.

## Edge cases / gotchas

- **Skipping a gate.** "We don't have time" → leads to surprise at next gate. Lightweight gates fine; skipped gates not.
- **Rubber-stamp gates.** If every gate is GO, committee isn't engaged. Healthy gates produce KILLs and HOLDs.
- **Conditional GO drift.** Conditions need owner + due date; otherwise they vaporize.
- **Recycle vs Hold confusion.** Recycle = redo current phase with fixes. Hold = pause; revisit at next gate.
- **Kill is healthy.** Some projects should be killed at G1/G3 — it's the gate working as intended.
- **Sunk-cost bias.** "We've invested $80k; can't kill now." Sunk cost is sunk; decide on future value.
- **Sponsor pressure to GO.** Sponsor wants to see progress; gate committee independent of sponsor pressure (ideally).
- **Quorum rules matter.** Define upfront; otherwise decisions get questioned later.
- **Audit trail in regulated industries.** Must keep decision + approvers + rationale for compliance.
- **Lightweight gates for small projects.** A 2-person 3-week project doesn't need 6 formal gates; tailor to risk + size.
- **Heavy gates for capital projects.** $1M+ projects warrant heavy stage-gate process; even with overhead.
- **Gate review ≠ status meeting.** Status meeting is operational; gate review is governance.
- **CR vs Gate decision.** CR = scope/budget/schedule change. Gate decision = phase transition. Different artifacts.
- **Gate decisions linked to RAID.** Conditions become RAID items; CRs become baseline updates.
- **Cross-project gates.** Multi-project programs may have program-level gates atop project gates.
- **Documentation overhead.** Heavy templates discourage rigor. Use Recipe 3 as full version; Recipe 4-9 for lightweight specifics.
- **Phase-gate vs Stage-gate.** Same concept; "Stage-Gate" is Cooper's trademarked term.
- **G4 launch criteria vary.** Hardware/regulated/SaaS each have different launch readiness. Tailor Recipe 8.
- **G5 not "end of work."** PIR (post-implementation review) at +30/60/90 days is part of G5.

## Sources

- [Monday.com gate review guide](https://monday.com/blog/project-management/gate-review/)
- [Planisware phase-gate glossary](https://planisware.com/glossary/phase-gate-or-stage-gate)
- [Stage-Gate International (Cooper)](https://www.stage-gate.com/)
- [PMI stage-gate research](https://www.pmi.org/learning/library/stage-gate-systems-product-development-7098)
- [Planview phase-gate process](https://www.planview.com/resources/articles/stage-gate-process/)
- [Atlassian project phases](https://www.atlassian.com/work-management/project-management/phases)
- [PMBOK 7th Edition: project lifecycle](https://www.pmi.org/standards/pmbok)
- [Cooper R.G. Winning at New Products](https://stage-gate.com/wp-content/uploads/2020/09/Winning-at-New-Products-Cooper-2017.pdf)
