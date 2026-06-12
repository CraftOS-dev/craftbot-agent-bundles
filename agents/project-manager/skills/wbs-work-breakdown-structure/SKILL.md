<!--
Source: https://www.pmi.org/learning/library/work-breakdown-structure-fundamentals-7138
Source: https://www.workamajig.com/blog/work-breakdown-structure
-->
# Work Breakdown Structure (WBS) — SKILL

100% rule decomposition + WBS coding + dictionary. The WBS is the deliverable spine of every project — every estimate, schedule, and budget flows from it.

## When to use

- Decomposing project scope into estimable work packages before Gantt construction.
- Building parent-child issue trees in Linear / Asana / Jira from a charter scope list.
- Validating a backlog: does every deliverable trace to scope, and does every leaf meet 8-80 hour rule?
- Recomposing scope after an approved CR (re-baseline WBS).

Trigger phrases: "build the WBS", "work breakdown", "decompose scope", "task tree", "100% rule", "WBS dictionary", "work packages".

## Setup

```bash
# WBS lives wherever the tasks live — Linear, Asana, Notion, or Excalidraw tree
# CraftBot ships linear-mcp, asana-api, excalidraw-diagram-generator
```

Auth: per-platform (see asana-monday-clickup-pm-platforms, linear-pm-software-projects skills).

No paid tooling required. Notion + Excalidraw + your PM tool of choice cover all cases.

## Common recipes

### Recipe 1: WBS construction procedure
```
1. Identify major deliverables (level 1) — 5-9 top-level items
2. Decompose each deliverable into sub-deliverables (level 2)
3. Continue decomposing until LEAF elements are estimable (8-80 hours)
4. Apply hierarchical WBS code (1.0, 1.1, 1.1.1, ...)
5. Write the WBS dictionary entry per LEAF
6. Validate:
   - 100% rule: parent scope == sum of children's scope
   - MECE: siblings mutually exclusive, no overlap
   - Estimability: leaves 8-80 hrs (PMBOK rule of thumb)
```

### Recipe 2: WBS template (Markdown outline)
```markdown
# [Project Name] — WBS v1.0

## 1.0 Discovery
### 1.1 User research
#### 1.1.1 5 user interviews — 16 hrs
#### 1.1.2 Funnel data pull (Amplitude) — 8 hrs
#### 1.1.3 Survey to 200 users — 12 hrs
### 1.2 Competitive analysis
#### 1.2.1 Top-3 competitor onboarding flows — 12 hrs
#### 1.2.2 Heuristic scorecard — 8 hrs

## 2.0 Design
### 2.1 Information architecture
#### 2.1.1 Onboarding flow map — 16 hrs
### 2.2 UI mocks
#### 2.2.1 Welcome modal v1 — 12 hrs
#### 2.2.2 Step-1 → step-3 mocks — 24 hrs
#### 2.2.3 Mobile parity (P1) — 16 hrs
### 2.3 Design system updates
#### 2.3.1 Checklist component — 16 hrs

## 3.0 Build
### 3.1 Backend
#### 3.1.1 Activation event schema — 8 hrs
#### 3.1.2 `/onboarding/state` endpoint — 24 hrs
#### 3.1.3 SSO unified session refactor — 40 hrs
### 3.2 Frontend
#### 3.2.1 Onboarding container — 24 hrs
#### 3.2.2 Step components (3) — 36 hrs
#### 3.2.3 Analytics integration — 16 hrs

## 4.0 Test & launch
### 4.1 QA
#### 4.1.1 E2E test scenarios (5) — 24 hrs
#### 4.1.2 Mobile regression — 16 hrs
### 4.2 Beta
#### 4.2.1 5-partner beta — 16 hrs
#### 4.2.2 Beta feedback synthesis — 8 hrs
### 4.3 GA launch
#### 4.3.1 Staged rollout 10/50/100% — 24 hrs
#### 4.3.2 Launch comms — 8 hrs

## 5.0 Close
### 5.1 +30d PIR — 8 hrs
### 5.2 Lessons learned doc — 4 hrs
### 5.3 Archive — 4 hrs

---

## WBS dictionary (per leaf)

### 1.1.1 5 user interviews
- **Description:** Recruit + run 5 30-min interviews with users in onboarding cohort
- **Deliverable:** Interview transcripts + theme synthesis doc
- **Owner:** Product researcher
- **AC:** 5 transcripts; ≥3 themes identified; insights doc reviewed by PM
- **Estimate:** 16 hrs (8 interview + 4 prep + 4 synthesis)
- **Dependencies:** None
- **WBS code:** 1.1.1
```

### Recipe 3: WBS dictionary template (per leaf)
```yaml
wbs_code: "1.1.1"
title: "5 user interviews"
description: >
  Recruit + run 5 30-min interviews with users in onboarding cohort
deliverable: "Interview transcripts + theme synthesis doc"
owner: "Product researcher"
acceptance_criteria:
  - "5 transcripts uploaded to Notion"
  - "≥3 themes identified"
  - "Insights doc reviewed by PM"
estimate_hours: 16
estimate_breakdown:
  interview: 8
  prep: 4
  synthesis: 4
dependencies: []
artifacts:
  - "Interview transcript template (Notion)"
  - "Synthesis doc template (Notion)"
risks:
  - "Recruiting <5 users in 1 week → R-007"
```

### Recipe 4: Bulk-create WBS in Linear (parent-child tree)
```bash
# Linear MCP bulk_create with parentTitle preserves hierarchy
mcp tool linear.bulk_create_issues \
  --teamKey "PROD" \
  --projectId "<project-id>" \
  --issues '[
    {"title":"1.0 Discovery","labels":["wbs-l1"]},
    {"title":"1.1 User research","parentTitle":"1.0 Discovery","labels":["wbs-l2"]},
    {"title":"1.1.1 5 user interviews","parentTitle":"1.1 User research","estimate":2,"labels":["wbs-leaf"]},
    {"title":"1.1.2 Funnel data pull","parentTitle":"1.1 User research","estimate":1},
    {"title":"2.0 Design","labels":["wbs-l1"]},
    {"title":"2.1 IA","parentTitle":"2.0 Design","labels":["wbs-l2"]},
    {"title":"2.1.1 Onboarding flow map","parentTitle":"2.1 IA","estimate":2}
  ]'
```

### Recipe 5: Bulk-create WBS in Asana
```bash
# Asana uses `parent` for sub-tasks (3-level deep max as of 2026)
for wbs_node in $(jq -c '.nodes[]' wbs.json); do
  parent=$(echo $wbs_node | jq -r '.parent_gid // empty')
  title=$(echo $wbs_node | jq -r '.title')
  est=$(echo $wbs_node | jq -r '.estimate_hours // 0')

  curl -s -X POST "https://app.asana.com/api/1.0/tasks" \
    -H "Authorization: Bearer $ASANA_PAT" \
    -d "{\"data\":{\"projects\":[\"<gid>\"],\"parent\":\"$parent\",\"name\":\"$title\",\"custom_fields\":{\"estimate_hours\":$est}}}"
done
```

### Recipe 6: Render WBS as Excalidraw tree
```bash
mcp tool excalidraw.generate_diagram \
  --type "tree" \
  --root "Onboarding Revamp Q3" \
  --nodes '[
    {"id":"1.0","label":"Discovery","parent":"root"},
    {"id":"1.1","label":"User research","parent":"1.0"},
    {"id":"1.1.1","label":"5 user interviews","parent":"1.1"},
    {"id":"1.1.2","label":"Funnel data pull","parent":"1.1"},
    {"id":"2.0","label":"Design","parent":"root"},
    {"id":"3.0","label":"Build","parent":"root"},
    {"id":"4.0","label":"Test & launch","parent":"root"},
    {"id":"5.0","label":"Close","parent":"root"}
  ]'
```

### Recipe 7: Validate 100% rule programmatically
```python
# wbs-validate.py — check sum-of-children == parent scope
import yaml, sys

wbs = yaml.safe_load(open(sys.argv[1]))
errors = []

def walk(node, path=""):
    code = node.get("wbs_code", "?")
    title = node.get("title", "?")
    children = node.get("children", [])
    leaf_est = node.get("estimate_hours")

    if children and leaf_est is not None:
        errors.append(f"{code} {title}: has both children AND leaf estimate — pick one")

    if not children:
        if leaf_est is None:
            errors.append(f"{code} {title}: leaf missing estimate")
        elif leaf_est < 8:
            errors.append(f"{code} {title}: estimate {leaf_est}h < 8h (too granular)")
        elif leaf_est > 80:
            errors.append(f"{code} {title}: estimate {leaf_est}h > 80h (decompose further)")

    for c in children:
        walk(c, f"{path}/{code}")

walk(wbs)

if errors:
    print(f"WBS FAIL — {len(errors)} issues:")
    for e in errors: print(f"  - {e}")
    sys.exit(1)
print("WBS PASS — 100% rule + 8-80h check passed")
```

### Recipe 8: WBS code convention
```
Format: {level1}.{level2}.{level3}.{level4} ...
Example:
  1.0         Major deliverable
  1.1         Sub-deliverable
  1.1.1       Work package (leaf)
  1.1.1.1     Activity (rare; only if needed for tracking)

Rules:
- Always include the trailing .0 at L1 for visual alignment
- Never re-use codes; renumber instead of skipping
- After CR-driven additions, append to end (1.4 added after 1.3 stays as 1.4)
- Don't go beyond 5 levels — sign of poor parent decomposition
```

### Recipe 9: WBS dictionary CSV schema for Smartsheet
```csv
wbs_code,title,deliverable,owner,acceptance_criteria,estimate_hours,dependencies,artifacts,risks
1.1.1,5 user interviews,Transcripts + theme doc,Product researcher,"5 transcripts uploaded; ≥3 themes; insights doc reviewed",16,,Interview template;Synthesis doc,R-007
1.1.2,Funnel data pull,Amplitude funnel report,Data analyst,"Funnel covers 30d; drop-off ≥3 steps identified",8,1.1.1,Amplitude dashboard,
2.1.1,Onboarding flow map,Lucid flow diagram,Designer,"All 3 user paths mapped; reviewed by PM+Eng",16,1.1.1;1.2.1,Lucid template,
3.1.3,SSO unified session refactor,Refactored session middleware,Eng,"Single session token across SSO providers; 100% test coverage",40,1.0;2.0,Auth ADR-12,R-001
```

### Recipe 10: Rolling-wave WBS planning
```
Near-term (next 30d): decompose to leaves (8-80 hr each)
Mid-term (30-90d):    decompose to L3 deliverables only
Far-term (90d+):      L2 only; re-decompose at next planning cycle
```

## Examples

### Example 1: Decompose a charter scope list into WBS
**Goal:** Charter's in-scope has 6 items. Need a Gantt-ready WBS.

**Steps:**
1. Promote each scope item to L1 deliverable in WBS outline.
2. For each L1, brainstorm sub-deliverables (L2) via Recipe 1.
3. Decompose L2 items into L3 work packages, sizing 8-80h.
4. Write WBS dictionary entry per leaf (Recipe 3).
5. Run Recipe 7 validator → fix 3 oversized leaves.
6. Load into Linear via Recipe 4.
7. Hand off to Gantt construction (`gantt-msproject-smartsheet-teamgantt` skill).

**Result:** 47-leaf WBS, all leaves 8-80h, parent-child preserved in Linear, ready for Gantt.

### Example 2: Recompose WBS after approved CR
**Goal:** Approved CR adds "mobile parity" to scope.

**Steps:**
1. Find affected L1 (Design or Build).
2. Add new L2: 2.4 Mobile design.
3. Decompose to L3: 2.4.1 iOS mocks (16h), 2.4.2 Android mocks (16h), 2.4.3 Mobile checklist component (24h).
4. Add WBS dictionary entries.
5. Update Linear (Recipe 4) for new tasks; link to CR ID.
6. Re-baseline Gantt + budget (cross-link change-request-management skill).

**Result:** WBS v1.1, baseline re-locked, 56-hour expansion accounted for.

## Edge cases / gotchas

- **100% rule is non-negotiable.** If parent scope ≠ sum of children's scope, either parent is wrong or children are incomplete. Re-check before sign-off.
- **MECE siblings.** Overlapping siblings double-count work or double-bill budget. Reorganize or rename.
- **Activity vs deliverable.** WBS is deliverable-focused. "Conduct review meeting" is an activity; "Reviewed mock signed off" is a deliverable. Refactor activity-named leaves.
- **8-80 hour rule.** PMBOK rule of thumb. <8h = noise (track in cycle); >80h = decompose. Exceptions: rolling-wave far-term placeholder L2 entries.
- **Don't exceed 5 levels.** If you need L6, your L3 decomposition was too shallow.
- **WBS code stability.** Once baseline is locked, never renumber existing codes. Append (1.5 after 1.4); deleted items keep their code archived ("DELETED — see CR-014").
- **Estimate format.** Hours (not days, not story points) at WBS level — story points belong on backlog issues. Convert story-point velocity to hours separately for EVM.
- **Notion DB sub-pages.** Notion's relational sub-page is a fine WBS storage option but breaks if you try to bulk-edit hierarchy mid-project.
- **Linear's hierarchy depth.** Linear supports issue → sub-issue (2 levels) as of 2026. For L3+, use projects as L1 and parent-issue chains for L2/L3.
- **Asana sub-task depth.** Asana supports 5 levels but UI gets messy past 3. Use sections for L1 split.
- **Smartsheet rows are flat with indent.** Hierarchy via row indent level — easy to lose if you sort by another column. Lock sort to WBS code.
- **WBS dictionary is mandatory for sign-off.** A WBS without dictionary is just a tree; the dictionary is what's auditable.
- **Cost ≠ effort.** WBS dictionary captures estimate_hours; budget skill multiplies by loaded rate × overhead for cost.

## Sources

- [PMI WBS fundamentals](https://www.pmi.org/learning/library/work-breakdown-structure-fundamentals-7138)
- [Workamajig WBS guide](https://www.workamajig.com/blog/work-breakdown-structure)
- [Wrike WBS tutorial](https://www.wrike.com/blog/foolproof-guide-to-creating-a-work-breakdown-structure/)
- [Smartsheet WBS templates](https://www.smartsheet.com/free-work-breakdown-structure-templates)
- [PMBOK 7th Edition (PMI) — Performance Domains, "Delivery"](https://www.pmi.org/standards/pmbok)
- [PMI WBS practice standard 2nd Edition](https://www.pmi.org/standards/wbs)
