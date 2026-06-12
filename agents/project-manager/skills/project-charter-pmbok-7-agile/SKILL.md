<!--
Source: https://www.pmi.org/standards/pmbok
Source: https://asana.com/templates/project-charter
Source: https://www.atlassian.com/work-management/project-management/project-charter
-->
# Project Charter (PMBOK 7 + Agile-Friendly) — SKILL

The PMBOK 7 charter authoring playbook + agile-lite variant + sign-off workflow. Charter is the single most leveraged PM artifact — it locks sponsor, problem, scope boundary, success criteria, and budget envelope BEFORE work starts.

## When to use

- Authoring a new project charter at G0/G1 stage-gate or sprint-zero of an agile project.
- Reviewing an existing charter against the PMBOK 7 quality rubric.
- Building agile-lite charter (one-page) for fast-cycle teams.
- Capturing sponsor sign-off + circulating for steering-committee approval.
- Restarting a stalled project — recharter when sponsor/scope/budget changes materially.

Trigger phrases: "write a project charter", "kickoff doc", "project brief", "PMBOK charter", "agile charter", "sponsor sign-off", "scope boundary", "recharter".

## Setup

```bash
# Charter lives in Notion (standard) or Asana project description
# Use notion-mcp to create from template

# Alt: Asana project notes
curl -X POST "https://app.asana.com/api/1.0/projects" \
  -H "Authorization: Bearer $ASANA_PAT" \
  -d '{"data":{"workspace":"<gid>","name":"Onboarding Revamp Q3","notes":"<charter markdown here>"}}'
```

Auth:
- `NOTION_TOKEN` — internal integration token from https://www.notion.so/my-integrations
- `ASANA_PAT` — fallback if Asana is the workspace SoT

No paid plan required; both Notion + Asana free tiers support charter storage.

## Common recipes

### Recipe 1: Full PMBOK 7 charter template (markdown)
```markdown
# [Project Name] — Project Charter

**Author:** [PM] · **Date:** [YYYY-MM-DD] · **Status:** Draft / Reviewed / Approved
**Sponsor:** [Name + role] · **Project Manager:** [Name]
**Charter version:** v1.0

## 1. Problem / opportunity statement
[1 paragraph. What is the problem we're solving or opportunity we're chasing. Why now. What does failure look like. Evidence: ≥1 data point.]

## 2. Project objectives (outcome-led, 3-5)
- Objective 1: [outcome]
- Objective 2: [outcome]
- Objective 3: [outcome]

## 3. Success criteria (measurable)
| Criterion | Baseline | Target | Horizon | Owner |
|---|---|---|---|---|
| D7 activation | 35% | 42% | 2026-Q3 end | PM |
| NPS (onboarded users) | 12 | 30 | 2026-Q4 +30d | Product |
| Cost per acquisition | $48 | $42 | 2026-Q3 end | Marketing |

## 4. Scope
### In scope
- [Item 1]
- [Item 2]
- [3-7 items, deliverable-focused]

### Out of scope (explicit non-goals)
- [Item 1]
- [Item 2]
- [3+ items — protects against creep]

## 5. High-level milestones
| Milestone | Target date | Owner |
|---|---|---|
| Kickoff complete | 2026-06-15 | PM |
| Discovery complete (G1) | 2026-06-30 | Product |
| Design sign-off (G2) | 2026-07-10 | Design |
| Beta launch (G3) | 2026-08-01 | Eng |
| GA launch (G4) | 2026-08-30 | Eng |
| Closure + PIR (G5) | 2026-09-30 | PM |

## 6. Budget envelope
| Category | Amount | Notes |
|---|---|---|
| Personnel | $128,000 | 3 eng × 4 mo × $8k loaded; 0.5 PM; 0.5 Design |
| Vendor / contract | $24,000 | Onboarding video, copy review |
| Tooling / licenses | $4,000 | Amplitude, Fullstory upgrade |
| Contingency (15%) | $23,400 | |
| **Total** | **$179,400** | |

## 7. Stakeholders
- **Sponsor:** [Name, role] — accountable for outcomes + funds
- **Steering committee:** [Names + roles] — major decisions
- **Delivery team lead:** [Name]
- **Adjacent teams to coordinate:** [Names + dependencies]
- **End users / customers impacted:** [Segment + count]

## 8. Risks at chartering (top-5)
| ID | Risk | P (1-5) | I (1-5) | Score | Mitigation | Owner |
|---|---|---|---|---|---|---|
| R-001 | SSO vendor cert renewal late | 3 | 4 | 12 | Pre-emptive renewal Jul 1 | Eng Lead |
| R-002 | Design capacity constrained | 4 | 3 | 12 | Contract designer for mock review | PM |
| R-003 | Activation metric not instrumented | 3 | 3 | 9 | Tracking spec sign-off week 1 | Data |
| R-004 | Competing Q3 initiative pulls eng | 2 | 5 | 10 | Sponsor priority lock at kickoff | Sponsor |
| R-005 | UAT with design partners delayed | 3 | 3 | 9 | Confirm 5 partners pre-kickoff | PM |

## 9. Assumptions
- Eng team retains 3 FTE through Q3 (no attrition planned)
- Sponsor approves contingency draws ≤ $10k without CCB
- Design partner contracts signed by Jun 30

## 10. Constraints
- Q3-end hard deadline (board-committed)
- $180k budget cap (no overrun authorized)
- Cannot touch billing flow (legal hold)

## 11. Methodology
[Waterfall / agile / hybrid. Why this choice. Reference Cynefin classification if complex domain.]

Selected: **Hybrid** — waterfall for discovery + design (low ambiguity); scrum 2-wk cycles for implementation; stage-gates at G1/G2/G3/G4/G5.

## 12. Approvals
| Role | Name | Signature | Date |
|---|---|---|---|
| Sponsor | [VP Product] | _________ | _________ |
| PM | [PM] | _________ | _________ |
| Eng Lead | [Name] | _________ | _________ |
| Design Lead | [Name] | _________ | _________ |
| Finance approver | [Name] | _________ | _________ |
```

### Recipe 2: Agile-lite one-page charter
```markdown
# [Project] — Agile Charter v1

**PM:** [Name] · **Sponsor:** [Name] · **Date:** [YYYY-MM-DD]

**WHY (problem statement, 2 sentences):** [...]

**WHAT (outcome metrics, max 3):**
- [Metric 1: baseline → target by date]
- [Metric 2: baseline → target by date]
- [Metric 3: baseline → target by date]

**IN scope:** [3-5 bullets, outcomes not features]
**OUT of scope:** [3-5 bullets]

**WHO (team + RACI for chartering):**
- A: [Sponsor]
- R: [PM]
- C: [Eng / Design / Data leads]
- I: [Stakeholders]

**WHEN (milestones — quarter granularity):**
- Q3-week-1: Discovery
- Q3-week-4: Beta to design partners
- Q3-week-10: GA
- Q3-week-12: Retro + closure

**RISK BUDGET ($):** [contingency $]
**TOTAL BUDGET ($):** [total $]

**METHODOLOGY:** 2-wk Linear cycles + monthly stage-gate.

**Sponsor sign-off:** ________ Date: ________
```

### Recipe 3: Create charter page in Notion via MCP
```bash
mcp tool notion.create_page \
  --parent '{"database_id":"<charter-db-id>"}' \
  --properties '{
    "Name":{"title":[{"text":{"content":"Onboarding Revamp Q3"}}]},
    "Status":{"select":{"name":"Draft"}},
    "Sponsor":{"people":[{"id":"<user-id>"}]},
    "Budget":{"number":179400},
    "Target Date":{"date":{"start":"2026-09-30"}}
  }' \
  --children "$(cat charter-template.md)"
```

### Recipe 4: Mirror charter to Asana project description
```bash
curl -X PUT "https://app.asana.com/api/1.0/projects/<project-gid>" \
  -H "Authorization: Bearer $ASANA_PAT" \
  -d "{\"data\":{\"notes\":\"$(jq -Rs . < charter.md)\"}}"
```

### Recipe 5: Capture sponsor sign-off via gmail-mcp
```bash
mcp tool gmail.send_message \
  --to "vp-product@company.com" \
  --cc "pm@company.com,eng-lead@company.com" \
  --subject "Action: Approve Onboarding Revamp Q3 charter (v1.0)" \
  --body "$(cat <<EOF
Charter v1.0 attached: [link]

Decisions needed by Friday EOD:
1. Approve scope (in/out)
2. Approve $179.4k budget envelope (incl. $23.4k contingency)
3. Confirm sponsor decision authority ≤$10k contingency draws

Reply APPROVE to lock baseline; REJECT with comments to revise.

Sign-off captured in Notion charter DB.
EOF
)"
```

### Recipe 6: Charter quality rubric checker
```python
# rubric.py — run as `uvx python rubric.py charter.md`
import sys, re, pathlib

CHECKS = {
    "sponsor_named": r"(?im)^\s*\*\*Sponsor:\*\*\s+\S+",
    "problem_stated": r"(?im)^##.*[Pp]roblem",
    "why_now_evidence": r"(?im)why now|evidence|data point",
    "measurable_criterion": r"(?im)baseline|target|horizon",
    "in_out_scope_explicit": r"(?im)## .*[Ii]n scope.*\n.*\n.*## .*[Oo]ut of scope",
    "milestones_with_dates": r"(?im)\| [^|]+ \| \d{4}-\d{2}-\d{2}",
    "budget_with_contingency": r"(?im)[Cc]ontingency.*\$",
    "risks_with_pi": r"(?im)\| R-\d+",
    "methodology_justified": r"(?im)## .*[Mm]ethodology",
    "approvals_section": r"(?im)## .*[Aa]pprovals",
}

charter = pathlib.Path(sys.argv[1]).read_text()
score = 0
for name, pat in CHECKS.items():
    ok = bool(re.search(pat, charter))
    score += 1 if ok else 0
    print(f"{'OK ' if ok else 'MISS'}  {name}")
print(f"\nScore: {score}/{len(CHECKS)} — {'pass' if score >= 8 else 'FAIL — revise before sign-off'}")
```

### Recipe 7: Recharter trigger criteria checklist
```markdown
## Recharter when ANY of:
- [ ] Sponsor changes
- [ ] Scope materially shifts (>20% effort delta)
- [ ] Budget envelope breached (>10% over)
- [ ] Methodology changes (waterfall → agile or vice versa)
- [ ] Strategic context changes (OKR shift, market pivot)
- [ ] Two consecutive RED status weeks unresolved
- [ ] Critical-path lengthens >2 weeks vs baseline
```

### Recipe 8: Charter → kickoff deck (pptx skill handoff)
```bash
# Extract charter sections; feed to pptx skill as outline
jq -n --rawfile c charter.md '{
  title: "Onboarding Revamp Q3 — Kickoff",
  slides: [
    {h1:"Problem", body:"<problem section>"},
    {h1:"Objectives & success criteria", body:"<obj+criteria>"},
    {h1:"Scope (in/out)", body:"<scope>"},
    {h1:"Timeline & milestones", body:"<milestones>"},
    {h1:"Budget & resources", body:"<budget>"},
    {h1:"Risks at chartering", body:"<risks>"},
    {h1:"Decisions needed today", body:"<approvals>"}
  ]
}'
```

## Examples

### Example 1: Author a charter from a 2-page brief
**Goal:** Sponsor handed PM a 2-page brief. Charter needed by Wednesday.

**Steps:**
1. Extract problem + objectives from brief; flag missing baseline metrics → query Amplitude.
2. Draft Recipe 1 template; PM owns scope boundaries + risks.
3. Run Recipe 6 rubric checker → 9/10 (missing measurable horizon).
4. Add target date to success criterion #2 → 10/10.
5. Create Notion page (Recipe 3); circulate via gmail (Recipe 5).
6. Capture signatures Friday; lock as v1.0 baseline.

**Result:** Charter signed, baseline locked, kickoff Monday.

### Example 2: Recharter a stalled project
**Goal:** Project went 3 weeks RED on schedule + budget. Sponsor wants reset.

**Steps:**
1. Run recharter checklist (Recipe 7) — 4 of 7 criteria triggered.
2. Sponsor 1:1: confirm new scope boundary + budget ceiling.
3. Author v2.0 charter (Recipe 1) marking changed sections.
4. Run rubric (Recipe 6).
5. CCB approval (cross-link to change-request-management skill).
6. New baseline locked; project re-enters G2 stage-gate.

**Result:** Clean reset with sponsor accountability + revised baseline.

## Edge cases / gotchas

- **Charter ≠ PRD.** Charter = sponsor-facing, locks scope/time/budget. PRD = team-facing, specifies what to build. Don't conflate; PRD lives under product-manager.
- **Approval ≠ "looks good"** — capture explicit YES/NO in writing. Verbal nods don't survive scope debates 6 weeks later.
- **Sponsor name a role, not a committee.** "Steering committee" is consulted; one sponsor is accountable. Multiple sponsors = no sponsor.
- **Success criteria must be measurable.** "Improve UX" fails the rubric. "D7 activation 35% → 42% by Q3 end" passes.
- **In-scope items are outcomes, not features.** "Onboarding revamp" not "Sign-up form refactor + welcome modal + checklist UI."
- **Out-of-scope is the load-bearing list.** Most scope creep comes from "we didn't say no." Explicit non-goals close that door.
- **Budget contingency 10-20%.** Less than 10% = denial; more than 20% = padding. Sponsor will negotiate.
- **Methodology justified, not asserted.** "Agile because we're agile" fails. "Hybrid: discovery low-uncertainty (waterfall) + delivery high-iteration (scrum) per Cynefin complicated/complex domains." passes.
- **Charter version it.** v1.0 at sign-off. CR-driven changes → v1.1 / v2.0. Never edit v1.0 in place.
- **Asana notes field has size cap.** ~65k chars. For >2-page charters, keep canonical in Notion; Asana stores link + 1-page summary.
- **PMBOK 7 principles applied as final review pass.** Not a section in the charter — used to sanity-check sections 1-12.
- **Storage policy.** Charter PDF (signed) → SharePoint or Google Drive `/projects/<name>/charter/v1.0/`. Editable markdown → Notion. Permalink both.

## Sources

- [PMBOK 7th Edition (PMI)](https://www.pmi.org/standards/pmbok)
- [Asana project charter template](https://asana.com/templates/project-charter)
- [Atlassian charter guide](https://www.atlassian.com/work-management/project-management/project-charter)
- [Smartsheet charter examples](https://www.smartsheet.com/content/project-charter-templates)
- [PMI charter best practices](https://www.pmi.org/learning/library/charter-foundation-project-success-9081)
- [Project management institute principles](https://www.pmi.org/learning/library/disciplined-agile-pmbok-7th-foundation-9924)
