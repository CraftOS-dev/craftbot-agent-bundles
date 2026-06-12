<!--
Source: https://developers.asana.com/reference/createdependency
Source: https://developers.linear.app/docs/issue-relations
Source: https://networkx.org/documentation/stable/reference/algorithms/dag.html
-->
# Cross-Team Dependency Mapping — SKILL

Task-level deps (Linear `add_dependency` / Asana precedes-follows / Smartsheet predecessors) + team-level deps + network diagram + critical-chain identification. Visualize via Excalidraw / D2 / networkx.

## When to use

- Mapping cross-project / cross-team dependencies at kickoff or quarterly planning.
- Identifying critical chain (longest cross-team path) for slip-risk analysis.
- Building dependency network diagram for status report or sponsor brief.
- Detecting circular dependencies before they bite.
- Tracking dependency health weekly: on-track / at-risk / blocked.

Trigger phrases: "map dependencies", "cross-team dep", "critical chain", "dependency graph", "block by", "upstream blocker", "downstream impact", "dep network".

## Setup

```bash
# CraftBot ships linear-mcp, asana-api, excalidraw-diagram-generator
# Plus uvx --from networkx for graph analysis
uvx --from networkx python -c "import networkx as nx; print(nx.__version__)"
```

Auth: per-platform Linear, Asana, Smartsheet API keys.

## Common recipes

### Recipe 1: Task-level dep in Linear (issue relation)
```bash
mcp tool linear.add_dependency \
  --fromIssueId "<successor-id>" \
  --toIssueId "<predecessor-id>" \
  --relation "blocks"
# relation: blocks / blocked-by / related / duplicates
```

Issue relations available in Linear 2026:
- `blocks` — predecessor → successor
- `blocked_by` — reverse direction
- `related` — soft link
- `duplicates` — merge candidate

### Recipe 2: Project-level dep in Linear (initiative critical path)
```bash
mcp tool linear.add_dependency \
  --fromProjectId "<auth-revamp-project>" \
  --toProjectId "<onboarding-revamp-project>" \
  --note "Onboarding revamp blocked on auth-revamp shipping unified session"
```

### Recipe 3: Task-level dep in Asana
```bash
# Mark Task A as predecessor of Task B
curl -X POST "https://app.asana.com/api/1.0/tasks/<task-b-gid>/addDependencies" \
  -H "Authorization: Bearer $ASANA_PAT" \
  -d '{"data":{"dependencies":["<task-a-gid>"]}}'
```

### Recipe 4: Task-level dep in Smartsheet (predecessor cell)
```bash
# Smartsheet uses PREDECESSOR_LIST column; FS/SS/FF/SF + lag
curl -X PUT "https://api.smartsheet.com/2.0/sheets/<sheet-id>/rows" \
  -H "Authorization: Bearer $SMARTSHEET_TOKEN" \
  -d '[{
    "id":<row-b-id>,
    "cells":[{
      "columnId":<pred-col-id>,
      "objectValue":{
        "objectType":"PREDECESSOR_LIST",
        "predecessors":[{"rowId":<row-a-id>,"type":"FS","lag":"+0d"}]
      }
    }]
  }]'
```

### Recipe 5: Team-level dep tracking (Notion DB schema)
```yaml
Database: "Cross-team Dependencies — Q3"
Properties:
  ID:                    title          # D-001 ...
  Title:                 rich_text
  From_team:             select         # who depends on what
  To_team:               select         # who delivers
  Item:                  rich_text      # what is being depended on
  Type:                  select         # API / Data / Decision / Resource / Approval / Sign-off
  Direction:             select         # Upstream / Downstream
  Target_date:           date
  Status:                select         # On track / At risk / Blocked / Delivered
  Risk_score:            number         # 1-25 (P×I)
  Owner_from_side:       person
  Owner_to_side:         person
  Escalation_path:       rich_text
  Linked_RAID:           relation
  Linked_issues:         rich_text      # Linear/Asana IDs
  Last_review:           date
```

### Recipe 6: Dependency network diagram (Excalidraw)
```bash
mcp tool excalidraw.generate_diagram \
  --type "network" \
  --nodes '[
    {"id":"auth","label":"Auth team","group":"teams"},
    {"id":"onboarding","label":"Onboarding team","group":"teams"},
    {"id":"data","label":"Data team","group":"teams"},
    {"id":"design","label":"Design team","group":"teams"},
    {"id":"sso","label":"SSO unified session","group":"deliverables"},
    {"id":"events","label":"Activation event schema","group":"deliverables"},
    {"id":"mocks","label":"Onboarding mocks","group":"deliverables"},
    {"id":"refactor","label":"3.1.3 SSO refactor","group":"tasks"}
  ]' \
  --edges '[
    {"from":"auth","to":"sso"},
    {"from":"sso","to":"refactor","label":"blocks"},
    {"from":"data","to":"events","label":"delivers"},
    {"from":"design","to":"mocks","label":"delivers"},
    {"from":"events","to":"refactor","label":"blocks"},
    {"from":"mocks","to":"refactor","label":"informs"}
  ]'
```

### Recipe 7: networkx — find critical chain
```python
# critical-chain.py
import json, networkx as nx

deps = json.load(open("dependencies.json"))
# [{"from":"refactor","to":"sso","duration":40},
#  {"from":"refactor","to":"events","duration":8},
#  ...]
# (from = successor, to = predecessor; duration on predecessor)

G = nx.DiGraph()
for d in deps:
    G.add_edge(d["to"], d["from"], weight=d.get("duration", 0))

# Longest path = critical chain
chain = nx.dag_longest_path(G)
length = nx.dag_longest_path_length(G)
print(f"Critical chain: {' → '.join(chain)}")
print(f"Total duration: {length} days")
```

### Recipe 8: Detect circular dependencies
```python
import networkx as nx
G = nx.DiGraph()
# ... build from deps ...

try:
    cycle = nx.find_cycle(G)
    print(f"CIRCULAR DEP DETECTED: {cycle}")
    print("Break the cycle before proceeding — pick one edge to remove or relax")
except nx.NetworkXNoCycle:
    print("No circular dependencies — DAG is valid")
```

### Recipe 9: Dependency health audit (weekly)
```bash
# Pull cross-team deps from Notion DB
mcp tool notion.query_database \
  --database_id "<deps-db-id>" \
  --filter '{"property":"Status","select":{"does_not_equal":"Delivered"}}' \
  --sorts '[{"property":"Target_date","direction":"ascending"}]' \
| jq '.results[] | {
    id: .properties.ID.title[0].plain_text,
    item: .properties.Item.rich_text[0].plain_text,
    from: .properties.From_team.select.name,
    to: .properties.To_team.select.name,
    target: .properties.Target_date.date.start,
    status: .properties.Status.select.name,
    days_to_target: ((.properties.Target_date.date.start | fromdateiso8601 - now) / 86400 | floor)
  }'
```

### Recipe 10: Cross-team dependency matrix (CSV / Markdown)
```csv
from_team,to_team,item,target_date,status,risk_score,owner_from,owner_to
Onboarding,Auth,Unified session middleware,2026-06-25,At risk,12,Eng Lead (Onboarding),Auth PM
Onboarding,Data,Activation event schema,2026-06-22,Delivered,0,Data Lead,Data eng
Onboarding,Design,Onboarding mocks,2026-06-23,On track,4,Design Lead,Designer
Marketing,Onboarding,Launch comms talk-track,2026-08-15,On track,3,Marketing PM,PM
CSM,Onboarding,Training docs,2026-08-22,On track,4,CSM Lead,PM
```

### Recipe 11: Cross-team dependency status report block
```markdown
## Cross-team dependencies

### Status summary
- Total open: 7
- Delivered this week: 2 (D-001 events, D-005 mocks)
- At risk: 1 (D-002 SSO unified session)
- Blocked: 0

### At-risk dep (D-002)
- From: Onboarding team
- To: Auth team
- Item: Unified session middleware
- Target: 2026-06-25 (4 days)
- Risk: Auth team's R-003 (vendor cert) impacts our 3.1.3
- Owner (their side): Auth PM
- Escalation: VP Eng (if not resolved by Tue)
- Mitigation: 2d buffer in our plan; fast-track 4.1.1 if dep slips ≥2d

### Upcoming dep deliveries (next 2 weeks)
| Item | From | Target | Status |
|---|---|---|---|
| D-002 SSO | Auth | 2026-06-25 | At risk |
| D-006 Tracking spec | Data | 2026-06-29 | On track |
| D-007 Design system v3 | Design | 2026-07-05 | On track |
```

### Recipe 12: Dependency type → handling pattern
```
Type            | Handling pattern
API             | Contract-first; integration tests; vendor mock
Data            | Schema lock; sample dataset; ETL ready
Decision        | Sponsor 1:1; CR if delayed
Resource (hire) | Backfill plan; contractor in flight
Approval        | Async sign-off; SLA defined
Sign-off        | Stage-gate review; multi-approver workflow
Sequential FS   | Pure dependency; slip cascades
Parallel SS     | Coordinated start; comms needed
Soft (informs)  | Useful but not blocking; document
```

### Recipe 13: Dependency slip cascade analysis
```python
# cascade.py — if dep X slips Y days, downstream impact?
import networkx as nx
G = nx.DiGraph()
# ... build from project graph ...

def cascade_impact(G, slip_node, slip_days):
    descendants = nx.descendants(G, slip_node)
    impacts = []
    for d in descendants:
        # Compute earliest possible start before vs after slip
        # Simplified: assumes longest path through node
        paths = list(nx.all_simple_paths(G, slip_node, d))
        if paths:
            max_path = max(paths, key=lambda p: sum(G.nodes[n].get("duration", 0) for n in p))
            impacts.append((d, slip_days))
    return impacts

impact = cascade_impact(G, "sso", 3)
for node, days in impact:
    print(f"  Downstream {node}: +{days}d slip")
```

## Examples

### Example 1: Map deps at kickoff
**Goal:** 4 teams contributing to onboarding revamp; cross-team deps unclear.

**Steps:**
1. Brainstorm session with leads (45 min) — surface 12 deps.
2. Drop into Notion DB (Recipe 5).
3. Classify per type (Recipe 12) — assign owners both sides.
4. Generate Excalidraw network diagram (Recipe 6).
5. Run networkx critical chain (Recipe 7) — chain: auth SSO → events → 3.1.3 → 3.2.2.
6. Check for cycles (Recipe 8) — none.
7. Embed diagram in kickoff deck + status archive.

**Result:** 12 deps mapped, critical chain identified, slip-risk pre-flagged in RAID.

### Example 2: Investigate cascade when dep slips
**Goal:** Auth team's SSO unified session slipped 3 days. Net impact?

**Steps:**
1. Run Recipe 13 cascade analysis from SSO node.
2. Output: 3.1.3 (eng) +3d, 3.2.2 (ui) +3d, 4.1.1 (qa) +3d → critical path +3d.
3. Check fast-track options (cross-link critical-path-method-cpm Recipe 7).
4. Mitigation: parallelize 4.1.1 prep with 3.1.3 final → -2d recovery → net +1d.
5. Update RAID R-002 + status report.

**Result:** Quantified impact + recovery plan in 2 hours.

### Example 3: Detect circular dep
**Goal:** Weekly review of new deps logged this week.

**Steps:**
1. Pull cross-team deps from Notion (Recipe 9).
2. Run Recipe 8 cycle detection.
3. Cycle found: A → B → C → A (data team needs design specs that need data schema).
4. Break: relax C → A to "soft (informs)" — design can proceed with assumed schema; reconcile when data ships.
5. Document tradeoff in RAID + status.

**Result:** Cycle resolved; both teams unblocked; risk documented.

## Edge cases / gotchas

- **Dep direction confusion.** "A blocks B" means B can't start without A. Linear's `blocks` = predecessor blocks successor. Always double-check.
- **Cycles silently kill projects.** A → B → C → A means nobody can start. networkx detects; act fast.
- **Soft vs hard deps.** "Informs" (soft) doesn't block; "blocks" (hard) does. Mixing them in critical-chain analysis inflates duration.
- **Cross-team deps need owners both sides.** "Auth team owes us" without a named human = nobody owns it.
- **Escalation path defined upfront.** When the dep slips, knowing who to call (their PM, their VP) saves a day.
- **Updates from the upstream team.** Don't wait — request standing async check-in (Slack thread or weekly 5-min sync).
- **Cross-stack tooling.** If Auth is in Jira and Onboarding is in Linear, deps cross tools. Maintain shadow dep in Notion DB.
- **Hidden deps via shared infra.** Both teams using same staging env = implicit resource dep. Document.
- **Approval as dep.** Sign-offs are deps. Treat as Decision type; SLA them.
- **Vendor as dep.** External vendor is hardest to manage. SOW + escalation clause matter.
- **Mid-project new deps.** Discovery often surfaces new deps. Log immediately; route through team-lead pair sync.
- **Dep status drift.** "On track" stays on track until day-of when it's actually blocked. Active probing weekly.
- **Compound deps.** Some deps depend on other deps. Critical-chain visualization helps surface.
- **Same-team deps ≠ cross-team.** Don't pollute cross-team DB with internal sequencing — use task-level deps.
- **Asana 3-level subtask hierarchy.** Cross-task deps can span; cross-project deps need Asana Portfolios + custom field.
- **Smartsheet predecessor lag.** `+3d` is a 3-day buffer; `-2d` is lead (start before pred finishes — risky).

## Sources

- [Linear issue relations](https://developers.linear.app/docs/issue-relations)
- [Asana create dependency](https://developers.asana.com/reference/createdependency)
- [Smartsheet predecessor types](https://help.smartsheet.com/articles/2476176-task-dependencies)
- [networkx DAG algorithms](https://networkx.org/documentation/stable/reference/algorithms/dag.html)
- [Atlassian Jira issue links](https://confluence.atlassian.com/jira/configuring-issue-linking-185729645.html)
- [PMI dependency management](https://www.pmi.org/learning/library/dependency-management-9981)
- [Cross-team coordination patterns (SAFe)](https://www.scaledagileframework.com/dependency-management/)
- [Excalidraw API + diagrams](https://github.com/excalidraw/excalidraw)
