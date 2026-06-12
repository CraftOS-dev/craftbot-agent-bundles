<!--
Source: https://developers.linear.app
Source: https://linear.app/docs/cycles
Source: https://linear.app/docs/initiatives  (initiatives Feb 2026)
-->
# Linear PM for Software Projects — SKILL

Linear is the 2026 default PM workspace for software shops. This pack covers cycles, projects, initiatives, dependency mapping, and velocity tracking from a PROJECT MANAGEMENT angle (not product discovery — see `product-manager` for that).

## When to use

- Standing up cycles (2-week sprints), projects (scoped delivery), and initiatives (cross-project outcomes) for software engineering work.
- Tracking velocity / throughput / cycle progress for status reports + EVM `% complete` input.
- Mapping cross-team and cross-project dependencies; computing critical chain.
- Bulk-loading a WBS into Linear as a parent-child issue tree.
- Wiring Linear issues to GitHub PRs for engineering traceability.

Trigger phrases: "set up Linear cycle", "linear sprint", "initiative", "linear velocity", "create issue from WBS", "cross-project dependency", "linear roadmap".

## Setup

```bash
# CraftBot ships linear-mcp; standalone GraphQL fallback:
curl -fsSL "https://api.linear.app/graphql" \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ viewer { id name } }"}'
```

Auth:
- `LINEAR_API_KEY` — from https://linear.app/settings/api (personal API key, free)
- OAuth available for multi-workspace; scopes needed: `Issues:Write`, `Projects:Write`, `Cycles:Read`

MCP tools (`linear-mcp`):
- `create_issue` / `update_issue` / `bulk_create_issues`
- `create_cycle` / `list_cycles`
- `create_project` / `update_project` / `list_projects`
- `create_initiative` / `list_initiatives` (Feb 2026)
- `add_dependency` (project + issue level)
- `list_issues` (filter by state, cycle, project, label, assignee, custom field)
- `create_project_milestone` / `create_project_update` (Feb 2026)

## Common recipes

### Recipe 1: Create a cycle and seed it from WBS
```bash
# Cycle = sprint, 2-week default
mcp tool linear.create_cycle \
  --teamKey "ENG" \
  --name "Cycle 27 — Activation push" \
  --startsAt "2026-06-15" \
  --endsAt "2026-06-29"

# Bulk-create the WBS as issues in the new cycle
mcp tool linear.bulk_create_issues \
  --teamKey "ENG" \
  --issues '[
    {"title":"1.1 Sign-up refactor","labels":["wbs","sprint-27"],"estimate":5,"cycleId":"<cycle-id>"},
    {"title":"1.1.1 Email/pw form","parentTitle":"1.1 Sign-up refactor","estimate":2},
    {"title":"1.1.2 SSO Google","parentTitle":"1.1 Sign-up refactor","estimate":3}
  ]'
```

### Recipe 2: Build a quarterly initiative + child projects
```bash
mcp tool linear.create_initiative \
  --name "Q3 — Lift D7 activation 35% → 42%" \
  --description "OKR-linked. Three projects across now/next/later." \
  --targetDate "2026-09-30"

# Now / Next / Later as projects under the initiative
mcp tool linear.create_project \
  --teamIds '["ENG"]' \
  --name "Onboarding revamp (NOW)" \
  --initiativeId "<init-id>" \
  --targetDate "2026-07-15"

mcp tool linear.create_project \
  --teamIds '["ENG"]' \
  --name "In-product checklist (NEXT)" \
  --initiativeId "<init-id>" \
  --targetDate "2026-08-30"
```

### Recipe 3: Add project milestones (Feb 2026 feature)
```bash
mcp tool linear.create_project_milestone \
  --projectId "<project-id>" \
  --name "Beta to 5 design partners" \
  --targetDate "2026-07-01" \
  --description "Activation funnel instrumented; 5 design partners onboarded"

mcp tool linear.create_project_milestone \
  --projectId "<project-id>" \
  --name "GA launch" \
  --targetDate "2026-07-15"
```

### Recipe 4: Post a weekly project update (Feb 2026 feature)
```bash
mcp tool linear.create_project_update \
  --projectId "<project-id>" \
  --health "onTrack" \
  --body "Wins: checklist UX merged. Risks: SSO vendor cert renewal Friday. Decisions needed: confirm staged rollout schedule."
```

### Recipe 5: Cross-project dependency (initiative-level critical path)
```bash
mcp tool linear.add_dependency \
  --fromProjectId "<auth-revamp-project>" \
  --toProjectId "<onboarding-project>" \
  --note "Onboarding blocked on auth's unified session ship"
```

### Recipe 6: Issue-level dependency (predecessor)
```bash
mcp tool linear.add_dependency \
  --fromIssueId "<successor-id>" \
  --toIssueId "<predecessor-id>" \
  --relation "blocks"
```

### Recipe 7: Query cycle velocity for status report
```bash
curl -s "https://api.linear.app/graphql" \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"query($id:String!){ cycle(id:$id){ name startsAt endsAt progress completedScopeHistory scopeHistory issues { nodes { id title state { name } estimate completedAt } } } }","variables":{"id":"<cycle-id>"}}' \
| jq '.data.cycle | {
    name,
    progress,
    scope: ([.issues.nodes[].estimate | numbers] | add),
    completed: ([.issues.nodes[] | select(.state.name=="Done") | .estimate | numbers] | add),
    velocity_pts_per_day: (([.issues.nodes[] | select(.state.name=="Done") | .estimate | numbers] | add) / 10)
  }'
```

### Recipe 8: Cycle throughput trend (last 6 cycles)
```bash
curl -s "https://api.linear.app/graphql" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query":"{ team(id:\"<team-id>\"){ cycles(orderBy:updatedAt, first:6){ nodes{ name endsAt issues(filter:{completedAt:{null:false}}){ nodes{ estimate } } } } } }"}' \
| jq '.data.team.cycles.nodes[] | {name, endsAt, throughput: ([.issues.nodes[].estimate | numbers] | add)}'
```

### Recipe 9: Map cross-project dep graph (for critical chain analysis)
```bash
# Pull all active projects + their relations, output a JSON edge list networkx can consume
curl -s "https://api.linear.app/graphql" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query":"{ projects(filter:{state:{eq:\"started\"}}){ nodes { id name targetDate dependencies { nodes { dependedOnProject { id name } } } } } }"}' \
| jq '[.data.projects.nodes[] | {id, name, deps: [.dependencies.nodes[].dependedOnProject.id]}]' \
> linear-projects-graph.json

# Pipe to networkx for critical chain (see critical-path-method-cpm skill)
uvx --from networkx python -c "
import json, networkx as nx
G = nx.DiGraph()
data = json.load(open('linear-projects-graph.json'))
for p in data:
    G.add_node(p['id'], name=p['name'])
    for d in p['deps']:
        G.add_edge(d, p['id'])
print('Topological order:', list(nx.topological_sort(G)))
print('Longest chain:', nx.dag_longest_path(G))
"
```

### Recipe 10: Link Linear issue → GitHub PR (auto-close on merge)
```bash
# In the GitHub PR body, add: "Closes ENG-123"
# Linear auto-syncs via GitHub integration; or manually:
mcp tool linear.update_issue \
  --id "ENG-123" \
  --description "$(cat <<EOF
$(curl -s https://api.github.com/repos/org/repo/pulls/456 | jq -r '.body')

**PR:** https://github.com/org/repo/pull/456
EOF
)"
```

### Recipe 11: Roll an incomplete cycle forward
```bash
# Get current + next cycle IDs
mcp tool linear.list_cycles --teamKey "ENG" --first 2 \
| jq -r '{current: .nodes[0].id, next: .nodes[1].id}'

# Move started/backlog issues from current → next
mcp tool linear.list_issues \
  --filter '{"cycle":{"id":{"eq":"<current-id>"}},"state":{"type":{"in":["started","backlog"]}}}' \
| jq -r '.nodes[].id' \
| xargs -I{} mcp tool linear.update_issue --id {} --cycleId "<next-id>"
```

### Recipe 12: WIP enforcement query
```bash
# Find anyone with > 3 in-progress issues across all teams (kanban-style WIP limit)
curl -s "https://api.linear.app/graphql" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query":"{ users { nodes { name assignedIssues(filter:{state:{type:{eq:\"started\"}}}){ totalCount } } } }"}' \
| jq '.data.users.nodes[] | select(.assignedIssues.totalCount > 3) | {name, wip: .assignedIssues.totalCount}'
```

## Examples

### Example 1: Spin up a new project from a charter
**Goal:** PRD approved Friday; charter signed; need Linear scaffold ready Monday.

**Steps:**
1. `create_initiative` with the OKR-link target date.
2. `create_project` with description = charter URL + sponsor + success criteria.
3. `create_project_milestone` for each major milestone (kickoff, beta, GA, +30 PIR).
4. `bulk_create_issues` for the kickoff sprint backlog (from WBS leaves).
5. `add_dependency` for any cross-project blockers (e.g., depends on auth-revamp).
6. `create_project_update` with health=onTrack + body "Kickoff complete; cycle 27 scoped."

**Result:** Linear project workspace ready for sprint planning Monday standup.

### Example 2: End-of-cycle stakeholder digest
**Goal:** Generate "what shipped" for the weekly status email.

**Steps:**
1. Query cycle: completed issues with estimate + project tag.
2. Group by project; total story-points per project.
3. Pull each project's current `update` for context.
4. Format as Lenny-style: Wins / Lowlights / Asks / Plans / Metrics.
5. Pipe into `gmail-mcp` weekly send to stakeholders list.

**Result:** Outcome-led digest with velocity numbers, no manual aggregation.

### Example 3: Critical-path computation across initiative
**Goal:** Identify the longest cross-project chain for an initiative; flag schedule risk.

**Steps:**
1. Pull all projects in initiative + their `dependencies`.
2. Build directed graph (predecessor → successor).
3. Compute `dag_longest_path` via networkx.
4. Output chain + cumulative target-date slip if any predecessor late.
5. Flag in status report.

**Result:** "Critical chain: auth-revamp → onboarding → checklist; 4-day buffer; if auth slips > 4d, Q3 GA at risk."

## Edge cases / gotchas

- **Pagination defaults.** Lists default to 50; pass `first: 250, after: $cursor` for larger queries. `> 1000` always batched.
- **Initiatives are Feb 2026.** Workspaces created before may need feature flag; verify with `viewer.organization.features`.
- **Custom field writes require schema lookup.** `update_issue --customFields` rejects unknown field IDs — query `team.issueCustomFields` first.
- **Rate limit 1500 / hour / token.** Bulk create chunks of 50 with 1-2s pacing. Backoff on `RATE_LIMITED`.
- **State transitions are team-scoped.** Can't move an issue to a state from another team's workflow. Use `team.states` lookup.
- **Archived issues excluded by default.** `list_issues` adds `includeArchived: true` for historicals.
- **OAuth scopes narrower than personal keys.** App OAuth needs explicit `Issues:Write` / `Projects:Write`.
- **Webhooks beat polling.** For Notion sync or status report auto-refresh, subscribe to `Issue`, `Project`, `ProjectUpdate`, `Cycle` event types.
- **Project vs Initiative vs Cycle.** Initiative = outcome (quarter+). Project = scoped delivery (weeks to months). Cycle = time-box (2 weeks). Issues live in cycles + optionally projects.
- **Health enum.** `create_project_update --health` accepts `onTrack` / `atRisk` / `offTrack` only. Spell exactly.
- **MCP vs API parity.** linear-mcp covers ~95% of GraphQL; complex GraphQL queries (custom field schema, webhook config) still need direct curl.

## Sources

- [Linear API docs](https://developers.linear.app)
- [Linear GraphQL reference](https://developers.linear.app/docs/graphql/working-with-the-graphql-api)
- [Linear MCP setup](https://linear.app/docs/mcp)
- [Linear cycles](https://linear.app/docs/cycles)
- [Linear initiatives (Feb 2026)](https://linear.app/docs/initiatives)
- [Linear project updates + milestones](https://linear.app/docs/projects)
- [Linear changelog Feb 2026](https://linear.app/changelog)
