<!--
Source: https://www.projectmanager.com/blog/5-ways-to-avoid-scope-creep
Source: https://clickup.com/blog/scope-management-tools/
-->
# Scope Creep Prevention — SKILL

Baseline lock at kickoff + CR gating + requirements traceability + weekly scope review + drift detection (tasks added since baseline). Stops the death-by-1000-cuts failure mode where the project drifts past its purpose.

## When to use

- Locking baseline scope at G2 stage-gate.
- Weekly scope drift detection ("what tasks got added without a CR?").
- Building requirements-to-deliverable traceability.
- Sponsor or stakeholder pushing for "one more small thing."
- Project running over by 10%+ — diagnose if scope drove it.

Trigger phrases: "scope creep", "baseline drift", "we keep adding things", "scope review", "traceability matrix", "scope lock", "creep detection".

## Setup

```bash
# Linear / Asana queries for "tasks added since X"
# Notion CR DB for cross-reference
```

Auth: same as Linear, Notion, Asana defaults.

## Common recipes

### Recipe 1: Baseline lock procedure
```markdown
## Baseline lock at kickoff (G2)

### Locked artifacts (snapshot all to version v1.0)
- [ ] Charter (in scope + out of scope lists)
- [ ] WBS (full deliverable hierarchy)
- [ ] Gantt with critical path
- [ ] Budget with BAC
- [ ] RAID log (top-5 risks)
- [ ] Stakeholder list + RACI

### Storage
- Notion: charter page → save as v1.0; pin
- Smartsheet: set Baseline Start/Finish columns (cross-link gantt skill Recipe 5)
- Linear: tag all baseline issues with `baseline-v1.0` label
- Asana: archive baseline scope into a "Baseline Reference" section

### Communication
- Email all stakeholders: "Baseline locked v1.0; changes require CR"
- Pin baseline policy in Slack channel
- Include in next 4 weekly status reports
```

### Recipe 2: Requirements traceability matrix
```csv
req_id,requirement,source,charter_section,wbs_code,owner,status
REQ-001,"User completes activation in 7 days","Sponsor charter S3",3.0,3.2.1,Eng,Met
REQ-002,"D7 retention 35%→42%","OKR-Q3","S3",3.2.3,Data,Tracking
REQ-003,"Mobile parity",Sponsor charter S4 (CR-009: deferred),"S4 (was)","-","-",Deferred
REQ-004,"SSO unified session",Tech ADR-12,"S4",3.1.3,Eng,In progress
REQ-005,"Activation event schema",Data charter S4,"S4",3.1.1,Data,Met
REQ-006,"Onboarding feedback loop","Beta partner ask CR-005",5.0,4.2.2,Product,In progress
```
**Rule:** Every WBS leaf traces to a charter requirement OR an approved CR. Anything else = creep.

### Recipe 3: Drift detection — tasks added since baseline
```bash
# Linear — issues created after baseline date (Jun 15) NOT tagged with approved-CR
mcp tool linear.list_issues \
  --filter '{"createdAt":{"gte":"2026-06-15"},"labels":{"name":{"nin":["baseline-v1.0","CR-005","CR-007","CR-009"]}}}' \
  --first 100 \
| jq '.nodes[] | {id, title, createdAt, creator: .creator.name}'
```

Output: tasks added without CR linkage = creep candidates → investigate.

### Recipe 4: Asana drift detection
```bash
# Tasks created after baseline date in project
curl -s "https://app.asana.com/api/1.0/tasks?project=<gid>&created_since=2026-06-15T00:00:00&opt_fields=name,created_at,custom_fields,permalink_url" \
  -H "Authorization: Bearer $ASANA_PAT" \
| jq '.data[] | select((.custom_fields | map(.name=="CR_link" and .display_value != null) | any) | not) | {name, created_at, url: .permalink_url}'
```

### Recipe 5: Scope-creep flag in weekly status
```markdown
## Scope drift report — Week of [YYYY-MM-DD]

### Tasks added since baseline
- 3 new tasks created this week
- 2 traced to CR-009 (approved); 1 ungated → INVESTIGATE

### Ungated tasks (creep candidates)
| Task | Created | Creator | Action |
|---|---|---|---|
| "Add onboarding video" | 2026-06-23 | Eve | Flag; convert to CR-010 or remove |

### Total since baseline
- Baseline tasks: 47
- Added via CR: 8 (CR-005, CR-009)
- Added ungated: 1 (above)
- Net scope: +9 tasks (19% over baseline)

### Recommendation
- File CR-010 for "Add onboarding video" or remove from sprint
- Sponsor sync if creep trend continues
```

### Recipe 6: Charter out-of-scope reinforcement template
```markdown
## Out of scope — Q3 (LOCKED v1.0)

Anything below requires a CR + CCB approval to re-enter scope:

1. Mobile parity (CR-009 deferred to P2)
2. International / i18n (not in Q3 scope)
3. Personalized onboarding by segment (P2)
4. Email re-engagement campaigns (Marketing owns separately)
5. Admin / settings UI redesign (separate project)
6. Custom branding for enterprise (P3)
7. Onboarding video production (sponsor declined budget)

If a stakeholder asks for any of the above:
1. Refer to this list
2. If they want it: submit CR
3. If they don't want to CR: it's not happening this Q3
```

### Recipe 7: "Just one more thing" deflection script
```
Stakeholder: "Hey, can we also add X to this sprint?"

PM: "Let's check — what's the outcome you're trying to hit?"
[If aligns with existing scope: refactor existing task; no CR]
[If new outcome: "That's not in baseline; let's file a CR"]

PM: "I'll log CR-NNN. Impact assessment by Tue. CCB decision Wed-Thu. If approved, in-flight by Mon."

[If urgent: emergency CR template (cross-link change-request-management Recipe 10)]
```

### Recipe 8: Weekly scope review meeting agenda (15 min)
```markdown
## Scope review — [date] 15 min

1. Drift detection results (Recipe 3 / 4) — 3 min
2. Any ungated tasks? Why? (2 min)
3. Open CRs requiring decision — 5 min
4. Baseline vs current health (% over) — 2 min
5. Risk of further creep next week — 3 min
```

### Recipe 9: Scope drift trend chart
```python
# drift-trend.py
import json, matplotlib.pyplot as plt
data = json.load(open("weekly-scope-snapshot.json"))
# [{"week":"W24","baseline_tasks":47,"cr_added":3,"ungated_added":1}]

weeks = [d["week"] for d in data]
plt.bar(weeks, [d["baseline_tasks"] for d in data], label="Baseline", color="#5b9bd5")
plt.bar(weeks, [d["cr_added"]      for d in data], bottom=[d["baseline_tasks"] for d in data], label="CR-added", color="#70ad47")
plt.bar(weeks, [d["ungated_added"] for d in data],
        bottom=[d["baseline_tasks"]+d["cr_added"] for d in data], label="Ungated (creep)", color="#c00000")
plt.legend(); plt.ylabel("Task count"); plt.xticks(rotation=45); plt.tight_layout()
plt.savefig("scope-drift.png")
```

### Recipe 10: Sponsor scope-discipline reminder (gentle)
```bash
# Send monthly to sponsor when creep candidates detected
mcp tool gmail.send_message \
  --to "vp-product@company.com" \
  --subject "Q3 scope discipline — monthly snapshot" \
  --body "$(cat <<EOF
Hi Alice,

Quick monthly scope check on Onboarding Revamp:

- Baseline (v1.0): 47 tasks
- Approved CR additions: 11 tasks (CR-005, CR-009)
- Net scope: 58 tasks (+23% from baseline)
- Ungated candidates this month: 2 (flagged + converted to CRs)

CRs pending decision (need you):
- CR-011 — "Add referral nudge in onboarding" — $3k, +2d

If you'd like to tighten scope discipline (slow CR approvals, defer non-essential), let me know. Otherwise current pace projects 30%+ scope expansion by GA.

— PM
EOF
)"
```

### Recipe 11: Per-stage scope-creep tolerance
```
By stage-gate:
G2 (Planning) → 0% drift  (baseline freshly locked; any add = CR)
G3 (Execution) → ≤10% drift  (some CR additions expected)
G4 (Launch ready) → 0% drift  (scope lock for ship; no adds without recharter)
G5 (Close) → N/A (done)

Drift % = (current_tasks - baseline_tasks) / baseline_tasks
```

### Recipe 12: Project type → scope-creep risk matrix
```
Project type           |  Creep risk  |  Defense
Greenfield SaaS        |  HIGH        |  Tight charter; weekly drift; 0% buffer for adds
Internal tooling       |  HIGH        |  Sponsor co-owns out-of-scope list
Compliance / regulated |  LOW         |  Audit trail already enforces
Vendor integration     |  MED         |  Vendor SOW limits scope mechanically
Migration              |  MED         |  Source/target locked at start
Research / discovery   |  LOW         |  Time-boxed; outcome bounded
```

## Examples

### Example 1: Lock baseline at G2
**Goal:** Charter signed Wed; Gantt + WBS done Thu; lock baseline by Fri.

**Steps:**
1. Charter v1.0 saved in Notion + PDF in /baselines/.
2. WBS frozen; all leaves tagged `baseline-v1.0` in Linear.
3. Gantt baseline columns set (cross-link gantt skill).
4. BAC locked; budget v1.0 archived.
5. RAID v1.0 archived.
6. Email to all stakeholders + Slack pin.

**Result:** Baseline locked Fri; CR policy in force from Mon.

### Example 2: Catch a creep candidate mid-sprint
**Goal:** Sprint 27 day 4: dev added "Add onboarding video" task without CR.

**Steps:**
1. Run Recipe 3 Linear drift query — task surfaces.
2. PM 5-min check with dev: "Who asked? When? Is there a CR?"
3. No CR; sponsor's offhand comment in 1:1.
4. Either: file CR-010 + put on next sprint OR remove task.
5. Dev opts to remove (mid-sprint trade-off not worth).
6. Reminder to all team: route additions via PM (creep prevention norm).

**Result:** Creep blocked at day 4; team learns norm.

### Example 3: Monthly scope-discipline review with sponsor
**Goal:** 30 days into 90-day project; check creep trajectory.

**Steps:**
1. Generate Recipe 9 drift trend chart.
2. Pull CR queue health (cross-link change-request-management Recipe 7).
3. Calculate drift %: 47 baseline + 11 approved CRs + 2 ungated = +28%.
4. Sponsor email Recipe 10.
5. Sponsor decision: tighten CR approvals for remaining 60 days; target ≤+15% total drift.

**Result:** Sponsor co-owns scope discipline; trajectory adjusted.

## Edge cases / gotchas

- **Approved CR ≠ creep.** Creep = ungated additions. Approved CRs are intentional scope changes.
- **0% creep is unrealistic for >90-day projects.** Discovery reveals legitimate additions; the goal is CR-gated, not zero.
- **Creep often signals charter ambiguity.** Repeated "this was implied" CRs = charter scope was unclear → recharter.
- **Drift detection requires baseline labels.** Tag every baseline issue at lock-time; otherwise drift detection has no anchor.
- **Sponsor-initiated creep is the hardest.** "It's just one thing" from sponsor still needs CR — the norm matters.
- **"Refactor existing task" isn't creep.** Adjusting an in-scope task's approach is fine; changing its outcome is creep.
- **Bug fixes are in-scope by default.** Defect work doesn't require CRs unless it expands scope beyond original requirement.
- **Tech debt creep.** Devs sneak in refactors. Either CR them as their own work or constrain to acceptance criteria.
- **Hidden creep via "stretch goals."** Stretch items in sprint planning that became commitments. Track separately; never auto-promote.
- **Antipattern: scope-cut as creep antidote.** Aggressive scope cutting kills morale + outcomes. CR for cuts too.
- **Late-project creep is worst.** G4-stage creep destroys ship dates. Lock scope hard at G4.
- **Customer-driven creep.** Customer asks during beta. Triage: in scope (do), CR (decide), backlog (defer). Don't silently absorb.
- **Documentation creep.** "Just add this to the doc" — still scope. Charter usually doesn't cover docs unless explicit.
- **Out-of-scope list maintenance.** Update charter v1.X with new "explicitly rejected" items as CRs are rejected.
- **Cross-team creep.** Sister teams' work bleeding into yours. Refer to RACI; deflect via Eng Lead.

## Sources

- [ProjectManager: 5 ways to avoid scope creep](https://www.projectmanager.com/blog/5-ways-to-avoid-scope-creep)
- [ClickUp scope management tools](https://clickup.com/blog/scope-management-tools/)
- [PMI scope management](https://www.pmi.org/learning/library/scope-management-essentials-1980)
- [Smartsheet scope creep guide](https://www.smartsheet.com/content/scope-creep-management)
- [Atlassian project scope management](https://www.atlassian.com/work-management/project-management/scope)
- [PMBOK 7th Edition: scope performance domain](https://www.pmi.org/standards/pmbok)
- [Asana scope baseline templates](https://asana.com/templates/scope-statement)
