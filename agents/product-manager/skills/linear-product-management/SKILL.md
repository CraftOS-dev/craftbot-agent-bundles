<!--
Source: https://developers.linear.app
Linear API + MCP, GA 2026
-->
# Linear Product Management — SKILL

Linear (linear.app) is the 2026 default PM workspace. This pack covers issues, cycles, projects, initiatives, roadmaps, custom fields, and automations — the surface a PM hits daily.

## When to use

- Creating, updating, or querying Linear issues from PRDs, discovery handoffs, or sprint planning.
- Building cycles (2-week sprints), projects (PRD-scoped scope), initiatives (cross-project outcomes), and roadmaps (now/next/later).
- Writing RICE / ICE scores back to Linear custom fields.
- Aggregating customer feedback in Linear (label-driven views).
- Querying velocity / throughput / cycle status for stakeholder updates.

Trigger phrases: "create Linear issue", "spin up cycle", "build the Q3 roadmap", "what's in the current cycle", "ship a project", "bulk-create stories from this map".

## Setup

```bash
# CraftBot ships linear-mcp by default. To run standalone, use the Linear GraphQL API:
curl -fsSL "https://api.linear.app/graphql" \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ viewer { id name email } }"}'
```

Auth:
- `LINEAR_API_KEY` — personal API key from https://linear.app/settings/api. OAuth available for multi-workspace setups.

MCP tools available (`linear-mcp`):
- `create_issue` / `update_issue` / `archive_issue`
- `bulk_create_issues` (for story-map sync)
- `create_cycle` / `list_cycles` / `update_cycle`
- `create_project` / `update_project` / `list_projects`
- `create_initiative` / `update_initiative` / `list_initiatives`
- `add_dependency` (project- and issue-level)
- `list_issues` (with filters: state, assignee, cycle, project, label, custom field)
- `create_label` / `add_label_to_issue`
- `create_comment` / `list_comments`

## Common recipes

### Recipe 1: Create PRD-anchored issue with full template

```bash
mcp tool linear.create_issue \
  --teamKey "PROD" \
  --title "Onboarding revamp — first-session activation" \
  --description "$(cat <<'EOF'
**Parent PRD:** https://www.notion.so/onboarding-revamp-prd

## User story
As a solo-founder trial user, I want a guided first-session flow so that I activate within 7 days.

## Acceptance criteria
- [ ] Given a brand-new user, When they sign up, Then a 3-step in-product checklist appears
- [ ] Given a user mid-checklist, When they complete step 2, Then `activation_step_2_done` event fires
- [ ] Given the user leaves mid-flow, When they return, Then the checklist resumes

## Analytics
- Events: `onboarding_started`, `onboarding_step_completed`, `onboarding_dismissed`
- Properties: `step_index`, `time_since_signup_seconds`

## Out of scope
- Mobile parity (P1 follow-up)
- Personalized template selection

## Dependencies
- Design spec sign-off: see Figma frame
- Tracking spec review with data-eng
EOF
)" \
  --labels '["prd","activation","Q3-roadmap"]' \
  --priority 1 \
  --estimate 5
```

### Recipe 2: Create a 2-week cycle and assign issues

```bash
# Step 1 — create the cycle
mcp tool linear.create_cycle \
  --teamKey "PROD" \
  --name "Cycle 27 — Activation push" \
  --startsAt "2026-06-15" \
  --endsAt "2026-06-29"

# Step 2 — bulk-assign open issues with `Q3-roadmap` label to the new cycle
mcp tool linear.list_issues \
  --filter '{"labels":{"name":{"eq":"Q3-roadmap"}},"state":{"type":{"eq":"backlog"}}}' \
  --first 50 \
| jq -r '.nodes[].id' \
| while read issueId; do
    mcp tool linear.update_issue \
      --id "$issueId" \
      --cycleId "<new-cycle-id>"
  done
```

### Recipe 3: Build a quarterly initiative (now / next / later)

```bash
# Q3 outcome-level initiative
mcp tool linear.create_initiative \
  --name "Q3 — Activation revamp (D7 retention 35% → 42%)" \
  --description "Quarterly outcome: lift activation. Now: onboarding revamp. Next: in-product checklist. Later: personalized templates." \
  --targetDate "2026-09-30" \
  --status "active"

# Attach projects as "now" / "next" / "later"
mcp tool linear.create_project \
  --teamIds '["PROD"]' \
  --name "Onboarding revamp (NOW)" \
  --initiativeId "<initiative-id>" \
  --targetDate "2026-07-15" \
  --description "Committed cycle work; PRD + design done."

mcp tool linear.create_project \
  --teamIds '["PROD"]' \
  --name "In-product checklist (NEXT)" \
  --initiativeId "<initiative-id>" \
  --targetDate "2026-08-30" \
  --description "Problem validated; solution sized; PRD in draft."
```

### Recipe 4: Bulk-create stories from a story map

```bash
mcp tool linear.bulk_create_issues \
  --teamKey "PROD" \
  --projectId "<onboarding-project-id>" \
  --issues '[
    {"title":"Backbone: Sign up","labels":["story-map","activity"]},
    {"title":"Story: Email + password signup form","parentTitle":"Backbone: Sign up","estimate":2},
    {"title":"Story: SSO via Google","parentTitle":"Backbone: Sign up","estimate":3},
    {"title":"Backbone: Onboarding tour","labels":["story-map","activity"]},
    {"title":"Story: Step 1 welcome modal","parentTitle":"Backbone: Onboarding tour","estimate":1},
    {"title":"Story: Step 2 first-action prompt","parentTitle":"Backbone: Onboarding tour","estimate":3}
  ]'
```

### Recipe 5: Add a cross-project dependency (initiative-level critical path)

```bash
mcp tool linear.add_dependency \
  --fromProjectId "<auth-revamp-project>" \
  --toProjectId "<onboarding-revamp-project>" \
  --note "Onboarding revamp blocked on auth-revamp shipping the unified session"
```

### Recipe 6: Query cycle velocity for stakeholder update

```bash
# Linear GraphQL is the cleanest velocity source. The cycle resource exposes
# `progress`, `scopeHistory`, `completedScopeHistory`.
curl -s "https://api.linear.app/graphql" \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"query($id: String!){ cycle(id:$id){ name startsAt endsAt progress completedScopeHistory scopeHistory issues { nodes { title state { name } estimate } } } }","variables":{"id":"<cycle-id>"}}' \
| jq '.data.cycle | {name, progress, completed: ([.issues.nodes[] | select(.state.name=="Done") | .estimate] | add), scope: ([.issues.nodes[].estimate] | add)}'
```

### Recipe 7: Write a RICE score to a custom field

```bash
# Assumes the Linear team has a custom field `RICE Score` configured.
mcp tool linear.update_issue \
  --id "<issue-id>" \
  --customFields '[{"name":"RICE Score","value":28.5},{"name":"Reach","value":1200},{"name":"Impact","value":2},{"name":"Confidence","value":0.8},{"name":"Effort","value":3.5}]'
```

### Recipe 8: Aggregate customer feedback into a Linear view

```bash
# Create a label-driven view for customer feedback intake
mcp tool linear.create_label \
  --teamKey "PROD" \
  --name "customer-feedback" \
  --color "#ff6b6b"

# Triage: query last-7-day feedback for the weekly synthesis
mcp tool linear.list_issues \
  --filter '{"labels":{"name":{"eq":"customer-feedback"}},"createdAt":{"gte":"2026-06-02"}}' \
  --first 100 \
| jq '.nodes[] | {title, description, url, source: .labels.nodes[].name}'
```

### Recipe 9: Initiative-level roadmap export for the all-hands deck

```bash
# Get all initiatives + their child projects in one shot for the pptx skill
curl -s "https://api.linear.app/graphql" \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ initiatives(filter:{status:{type:{eq:\"active\"}}}){ nodes { name targetDate description projects { nodes { name targetDate state } } } } }"}' \
> roadmap-export.json
```

### Recipe 10: Auto-close cycle and roll over

```bash
# Linear closes cycles automatically at endsAt; the rollover behavior is per-team.
# To force-roll an issue out of an ending cycle into the next:
mcp tool linear.list_cycles --teamKey "PROD" --filter '{"endsAt":{"gte":"now"}}' --first 2 \
| jq -r '.nodes[0:2] | {current: .[0].id, next: .[1].id}'

# Move every Started issue forward
mcp tool linear.list_issues \
  --filter '{"cycle":{"id":{"eq":"<current-id>"}},"state":{"type":{"in":["started","backlog"]}}}' \
| jq -r '.nodes[].id' \
| xargs -I{} mcp tool linear.update_issue --id {} --cycleId "<next-id>"
```

## Examples

### Example 1: Sprint planning for the next cycle
**Goal:** Plan cycle 28 from the backlog scored by RICE.

**Steps:**
1. Query the backlog with `RICE Score` populated and unassigned to a cycle.
   ```bash
   mcp tool linear.list_issues \
     --filter '{"state":{"type":{"eq":"backlog"}},"cycle":{"null":true}}' \
     --orderBy '{"field":"customField:RICE Score","direction":"desc"}' \
     --first 30
   ```
2. Pick the top-N issues whose estimate sum fits team velocity (e.g., team has 35 story-points/cycle).
3. `create_cycle` for the new sprint window.
4. Bulk update issues to point at the new cycle.

**Result:** A scoped, prioritized, velocity-fit cycle in Linear with a publishable URL.

### Example 2: End-of-cycle stakeholder digest
**Goal:** Generate the "what shipped" digest for the weekly update.

**Steps:**
1. List issues completed in the cycle: `list_issues --filter '{"completedAt":{"gte":"<cycle-start>","lte":"<cycle-end>"}}'`.
2. Group by project; pull project names + outcomes.
3. Feed the JSON into the `stakeholder-update-format` skill for the Wins section.

**Result:** "This cycle: 12 issues, 28 story-points done. Onboarding revamp shipped. Activation funnel instrumentation live in Amplitude."

## Edge cases / gotchas

- **GraphQL pagination.** Lists default to 50 nodes; use `first: 250, after: $cursor` for larger queries. Issues > 1000 require batching.
- **Custom field schema drift.** `update_issue` rejects unknown custom-field names — query `team.issueCustomFields` first if writing scores programmatically.
- **Rate limits.** Linear API enforces 1500 requests / hour / token. Bulk operations should batch in chunks of 50; back off on `RATE_LIMITED`.
- **State machine.** Issue states are team-scoped; you cannot move an issue to a state from a different team's workflow. Resolve via `team.states` lookup before `update_issue`.
- **Initiative vs project vs cycle.** Don't conflate. Initiative = outcome (quarter+). Project = scoped chunk of work (1-3 months). Cycle = sprint (2 weeks). Issues belong to cycles and optionally projects.
- **Archived issues.** `list_issues` excludes archived by default; pass `includeArchived: true` if querying historical work.
- **OAuth scopes.** App-installed OAuth grants narrower scopes than personal API keys; verify `Issues:Write` for bulk-create.
- **Webhooks vs polling.** For real-time roadmap-to-Notion sync, use Linear webhooks (`Issue`, `Project`, `Cycle` event types) — polling burns rate limit.

## Sources

- [Linear API docs](https://developers.linear.app)
- [Linear GraphQL reference](https://developers.linear.app/docs/graphql/working-with-the-graphql-api)
- [Linear MCP setup](https://linear.app/docs/mcp)
- [Linear cycles documentation](https://linear.app/docs/cycles)
- [Linear initiatives](https://linear.app/docs/initiatives)
- [Linear roadmaps](https://linear.app/docs/roadmaps)
