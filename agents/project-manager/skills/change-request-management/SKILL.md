<!--
Source: https://www.projectmanager.com/blog/change-request-management
Source: https://monday.com/blog/project-management/scope-change/
-->
# Change Request Management (CCB Workflow) — SKILL

CR lifecycle: submit → impact assess → CCB decision → communicate → implement → close. Notion CR DB + Gmail-driven CCB approval chain. The gate that prevents "death by 1000 small adds."

## When to use

- Capturing a formal scope / schedule / budget / quality change request mid-project.
- Routing CR through impact assessment + CCB (Change Control Board) approval.
- Updating baseline (scope + schedule + budget + RAID) after CR approved.
- Auditing CR queue health: count, approval cycle time, % approved/rejected.

Trigger phrases: "submit a change request", "CR", "scope change", "CCB", "change control board", "baseline update", "scope addition", "approved CR".

## Setup

```bash
# Notion CR DB (default storage)
mcp tool notion.search_pages --query "Change Request"

# Gmail for CCB approval thread
mcp tool gmail.send_message --to "<ccb-list>" --subject "..." --body "..."
```

Auth: same as Notion + Gmail defaults. No paid tooling required.

## Common recipes

### Recipe 1: CR DB schema (Notion)
```yaml
Database: "Change Requests — [Project]"
Properties:
  ID:                    title          # CR-001, CR-002 ...
  Title:                 rich_text
  Requester:             person
  Date_submitted:        date
  Description:           rich_text
  Justification:         rich_text      # why this change
  Scope_impact:          rich_text
  Schedule_impact_days:  number         # +/- days on critical path
  Budget_impact:         number         # $ delta
  Quality_impact:        rich_text
  Risk_impact:           rich_text      # net P×I delta
  Status:                select         # Submitted / Under review / Approved / Rejected / Deferred / Implemented / Closed
  Decision_date:         date
  Approvers:             multi_select   # Sponsor / VP Eng / Steering / Legal
  CCB_decision_rationale: rich_text
  Conditions:            rich_text      # if conditional approval
  Linked_baseline:       relation       # → baseline DB
  Linked_RAID:           relation       # → RAID items affected
  Implementation_owner:  person
  Implementation_due:    date
  Closed_date:           date
```

### Recipe 2: CR submission template
```markdown
# CR-[ID] — [Title]

**Requester:** [Name]
**Date submitted:** [YYYY-MM-DD]
**Status:** Submitted

## 1. Description
[What is being requested. Be specific — "Add dark mode" not "Improve UI."]

## 2. Justification (why)
[Customer ask? Compliance? Risk mitigation? Strategic shift? Provide ≥1 data point or stakeholder source.]

## 3. Alternative considered
[What was rejected and why. Forces the requester to think before submitting.]

## 4. Impact assessment

### 4a. Scope impact
- New work added: [list]
- Existing work removed: [list]
- Net deliverable change: [+/- items]

### 4b. Schedule impact
- Critical-path tasks affected: [list]
- Net schedule delta: [+N / -N days]
- Milestone(s) affected: [list]
- New critical path (if changed): [list]

### 4c. Budget impact
- Cost delta: [+/- $X]
- Source of funds: [contingency / new ask / scope trade]
- Forecast impact on EAC: [new EAC $]

### 4d. Quality impact
- New NFR implications: [list]
- Risk to tests / UAT: [list]

### 4e. Risk impact
- New risks introduced: [list with P×I score]
- Risks closed by this change: [list]
- Net P×I delta: [+/-]

## 5. Recommendation (by PM)
[ ] Approve — [rationale]
[ ] Reject — [rationale]
[ ] Defer — [conditions for re-consideration]

## 6. Required approvers
- [ ] Sponsor: [Name]
- [ ] VP Eng: [Name]  (if engineering impact)
- [ ] Finance: [Name]  (if >$10k delta)
- [ ] Legal: [Name]  (if scope touches terms / compliance)

## 7. CCB decision
- Decision: [Approve / Reject / Defer]
- Decision date: [YYYY-MM-DD]
- Approvers signed: [Names]
- Rationale: [Why]
- Conditions: [List if conditional]

## 8. Implementation plan (if approved)
- Baseline update by: [date] — [PM]
- Charter update version: v[X.Y]
- Communication plan: [stakeholders + when + how]
- RAID update by: [date] — [PM]
- Linked tasks created: [list]
```

### Recipe 3: Submit a CR via Notion MCP
```bash
mcp tool notion.create_page \
  --parent '{"database_id":"<cr-db-id>"}' \
  --properties '{
    "ID":{"title":[{"text":{"content":"CR-009"}}]},
    "Title":{"rich_text":[{"text":{"content":"Defer mobile parity to P2"}}]},
    "Requester":{"people":[{"id":"<pm-id>"}]},
    "Date_submitted":{"date":{"start":"2026-06-24"}},
    "Description":{"rich_text":[{"text":{"content":"Move 2.4.x (Mobile parity) from Q3 scope to P2; original scope assumed iOS-only; engineering capacity reveals 80hr undocumented Android work."}}]},
    "Schedule_impact_days":{"number":-3},
    "Budget_impact":{"number":-5600},
    "Status":{"select":{"name":"Submitted"}}
  }' \
  --children "$(cat cr-009.md)"
```

### Recipe 4: CCB email approval workflow
```bash
mcp tool gmail.send_message \
  --to "vp-product@company.com,vp-eng@company.com,cfo@company.com" \
  --cc "pm@company.com" \
  --subject "CCB approval needed: CR-009 — Defer mobile parity to P2" \
  --body "$(cat <<EOF
CCB,

CR-009 submitted today. Summary:

WHAT: Defer mobile parity (2.4.x) from Q3 scope → P2
WHY: Engineering capacity reveals undocumented Android work (+80hr); critical-path conflict with SSO refactor recovery
IMPACT:
  Schedule: -3d (recover 3 days)
  Budget: -$5,600
  Risk: closes R-002 (capacity); opens R-009 (P2 commitment ambiguity)
  Quality: no immediate impact; mobile users on web-mobile until P2

PM RECOMMENDATION: Approve

Full CR doc: <notion-link>

DECISION NEEDED BY FRI EOD. Reply APPROVE / REJECT / DEFER (with comments).

— PM
EOF
)"
```

### Recipe 5: CCB decision capture
```bash
# After approval thread settles, log to CR DB
mcp tool notion.update_page \
  --page_id "<cr-009-page-id>" \
  --properties '{
    "Status":{"select":{"name":"Approved"}},
    "Decision_date":{"date":{"start":"2026-06-26"}},
    "Approvers":{"multi_select":[{"name":"Sponsor"},{"name":"VP Eng"},{"name":"Finance"}]},
    "CCB_decision_rationale":{"rich_text":[{"text":{"content":"Approved unanimously. Mobile-web baseline acceptable for Q3 GA. Re-baseline triggered."}}]},
    "Implementation_due":{"date":{"start":"2026-06-30"}}
  }'
```

### Recipe 6: Baseline update procedure (after approval)
```markdown
## Baseline update after CR-009 approval

### 1. Charter
- Update charter to v1.1 (in/out scope list)
- Out-of-scope additions: "Mobile parity (deferred to P2 — see CR-009)"

### 2. WBS
- Remove WBS leaves 2.4.1, 2.4.2, 2.4.3 (or mark "DELETED - CR-009")
- Recompute parent estimates if any

### 3. Gantt
- Remove tasks; re-run CPM (cross-link critical-path-method-cpm)
- New ship date locked

### 4. Budget
- Recompute BAC: $180,000 - $5,600 = $174,400
- Re-baseline EVM PV curve

### 5. RAID
- Close R-002 (capacity) — mitigated by CR-009
- Open R-009 (P2 commitment) — owner: PM, score 4
- Update affected D-XXX

### 6. PM tool
- Linear: cancel/archive issues 2.4.1-2.4.3; tag CR-009
- Tag charter version v1.1 in Notion

### 7. Comms
- Email all stakeholders: "CR-009 approved; mobile parity deferred to P2"
- Slack post in #proj-onboarding-revamp
- Update sponsor brief next Fri

### 8. CR closure
- Status → Implemented (when 1-7 done)
- Status → Closed (next week after no objections)
```

### Recipe 7: CR queue health audit
```bash
# Count by status; cycle time for approved
mcp tool notion.query_database \
  --database_id "<cr-db-id>" \
| jq '{
    total: (.results | length),
    submitted: ([.results[] | select(.properties.Status.select.name=="Submitted")] | length),
    under_review: ([.results[] | select(.properties.Status.select.name=="Under review")] | length),
    approved: ([.results[] | select(.properties.Status.select.name=="Approved")] | length),
    rejected: ([.results[] | select(.properties.Status.select.name=="Rejected")] | length),
    avg_cycle_days: (
      [.results[] | select(.properties.Status.select.name=="Approved") |
        ((.properties.Decision_date.date.start | fromdateiso8601) - (.properties.Date_submitted.date.start | fromdateiso8601)) / 86400
      ] | add / length
    )
  }'
```

### Recipe 8: CR-by-impact categorization
```
Impact tier classification (decides CCB level required):

TIER 1 (PM-approves):
  - <$2k budget delta
  - <2 days schedule delta
  - No scope addition (cosmetic / clarification)
  - No new risk created
  → PM logs as CR but auto-approves; informs sponsor

TIER 2 (Sponsor-approves):
  - $2k-$10k budget delta OR
  - 2-7 days schedule delta OR
  - 1 scope item added/removed
  → CCB email thread; sponsor decides

TIER 3 (Steering-approves):
  - >$10k budget delta OR
  - >7 days schedule OR
  - Multiple scope items / methodology change
  → Steering meeting; multi-approver decision; rebaseline mandatory

TIER 4 (Recharter required):
  - >20% effort delta from baseline
  - Methodology change
  - Sponsor change
  → New charter v2.0; project rebaselines from scratch
```

### Recipe 9: Defer (conditional) CR template
```markdown
## Conditional approval

DECISION: Defer (with conditions)

Conditions for approval at next CCB:
1. [Eng team provides 2-day spike to confirm 80hr Android estimate]
2. [Finance confirms $5.6k savings can be reallocated to contingency]
3. [CSM team confirms P2 commitment date won't trigger contract clauses]

Re-review: Next CCB meeting [date]
PM owns: gathering conditions evidence
```

### Recipe 10: CR template for emergency/urgent (24h SLA)
```markdown
# CR-[ID] — URGENT — [Title]

**Emergency:** Critical-path blocker requires immediate scope change
**SLA:** Decision in 24 hours

[Skip alternative-considered + recommendation sections]
[Direct to TL;DR + impact + ask]
```

### Recipe 11: CR analytics for monthly steering
```python
# cr-analytics.py
import json, statistics
crs = json.load(open("cr-export.json"))
print(f"Total CRs this month: {len(crs)}")
print(f"Approved: {sum(1 for c in crs if c['status'] == 'Approved')}")
print(f"Rejected: {sum(1 for c in crs if c['status'] == 'Rejected')}")
print(f"Deferred: {sum(1 for c in crs if c['status'] == 'Deferred')}")
print(f"% approved: {sum(1 for c in crs if c['status'] == 'Approved') / len(crs):.0%}")
print(f"Median cycle time (submit→decision): {statistics.median([c['cycle_days'] for c in crs]):.1f} days")
print(f"Net schedule impact: {sum(c['schedule_days'] for c in crs)} days")
print(f"Net budget impact: ${sum(c['budget_delta'] for c in crs):,}")
```

## Examples

### Example 1: Submit Tier 2 CR for scope cut
**Goal:** Mobile parity proving harder than scoped; want to defer to P2.

**Steps:**
1. PM drafts CR (Recipe 2 markdown).
2. Create in Notion DB (Recipe 3).
3. Email CCB (Recipe 4) with TL;DR + impact + recommendation.
4. CCB approves Fri (Recipe 5).
5. Run Recipe 6 baseline update — charter v1.1, WBS purge, RAID update.
6. Status report Fri: callout CR-009 approved + new baseline.

**Result:** Clean baseline; $5.6k savings; 3d schedule recovered; mobile deferred with paper trail.

### Example 2: Reject creep-style CR
**Goal:** Stakeholder asks for "small extra feature."

**Steps:**
1. PM logs CR — captures even rejections.
2. Impact assessment: +40 hrs, +$5k, +3d critical path.
3. PM recommendation: REJECT — does not trace to charter success criteria; defer to backlog.
4. CCB rejects unanimously.
5. Status → Rejected; communicated to requester.
6. Backlog issue created tagged "CR-rejected-2026-Q3" for portfolio context next quarter.

**Result:** Creep blocked at the gate; requester has paper trail of decision.

### Example 3: Emergency CR for production incident
**Goal:** Prod incident requires diverting 1 sprint to incident response.

**Steps:**
1. Recipe 10 emergency template.
2. Same-day sponsor brief + Slack.
3. Approval inside 4 hours.
4. Implementation: reassign 2 eng × 1 sprint; defer 2 sprint-27 issues to sprint-28.
5. Baseline update + comms blast.
6. Status report week-of: special section for incident response.

**Result:** Fast pivot with sponsor sign-off; no scope-creep aftermath.

## Edge cases / gotchas

- **Every change is a CR.** Even small ones — Tier 1 auto-approves, but it's logged.
- **No CR = no traceability.** Scope changes done verbally come back as "I never agreed to that" in 6 weeks.
- **Approval ≠ implementation.** Approved CR with no baseline update is technical debt for the project.
- **Email approval threads disappear.** Always capture decision + rationale in Notion CR DB. Email is evidence, not source of truth.
- **CCB SLA mismatched to project tempo.** Weekly CCB on a 2-week project = bottleneck. Tier-1 auto-approve threshold prevents.
- **Tier escalation drift.** Sponsors who delegate Tier 2 to PM "for speed" undermine governance. Document delegation explicitly in charter.
- **Conditional approval = unfinished decision.** Set re-review date; otherwise it stalls.
- **Net schedule impact misleading.** A CR that nets to 0 days schedule but trades stable work for risky work increases risk — call out.
- **Budget impact must include contingency draw.** If draw > sponsor's pre-approved threshold, escalate.
- **Risk impact often forgotten.** Every CR opens or closes risks. Update RAID.
- **Rejections aren't free.** Stakeholder unhappy with rejection may re-route — document rejection rationale clearly.
- **Defer ≠ accept-eventually.** Deferred CRs need re-review date or they become zombies.
- **Linked baseline relation in Notion.** Don't skip — without it, you can't audit "what was the baseline when CR-009 approved?"
- **Multi-project CR.** Cross-project CRs need each project's CCB to approve; track in both.
- **Recharter as escape valve.** When CR volume + impact exceeds 20% of baseline, stop CRing and recharter (Tier 4).
- **CR template too heavy.** If it's so heavy nobody submits, scope creep happens informally. Tier-1 light template + Tier 2/3 full template.
- **Approval thread can leak confidentiality.** For sensitive CRs (e.g., layoff-driven scope cuts), use Notion + role-based access, not email.

## Sources

- [ProjectManager.com change request guide](https://www.projectmanager.com/blog/change-request-management)
- [Monday scope change blog](https://monday.com/blog/project-management/scope-change/)
- [PMBOK 7th Edition: change performance domain](https://www.pmi.org/standards/pmbok)
- [Atlassian change control template](https://www.atlassian.com/templates/change-control)
- [Notion CR template](https://www.notion.com/templates/change-request-tracker)
- [Smartsheet CR templates](https://www.smartsheet.com/free-change-management-templates)
- [PMI change control board guide](https://www.pmi.org/learning/library/establishing-change-control-board-9961)
