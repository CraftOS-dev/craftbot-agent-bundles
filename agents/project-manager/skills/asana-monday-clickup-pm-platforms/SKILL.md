<!--
Source: https://developers.asana.com/docs/mcp-server (Asana MCP v2, GA Feb 2026)
Source: https://developer.monday.com/apps/docs/monday-apps-mcp
Source: https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server
Source: https://developers.wrike.com
-->
# Asana / Monday / ClickUp / Wrike PM Platforms — SKILL

The four leading general-purpose PM platforms in 2026. All four now ship official MCP servers; this pack covers cross-platform workspace operations — projects, tasks, portfolios, goals, automations.

## When to use

- Setting up a cross-functional project workspace (not software-only — Linear is the better default for code shops).
- Creating tasks/projects/portfolios programmatically from a charter, WBS, or PRD.
- Migrating between platforms or running side-by-side comparisons during platform selection.
- Pulling cross-project status into Notion / status reports.
- Configuring automations (status rollups, due-date escalations, RAID alerts).

Trigger phrases: "create Asana project", "set up monday board", "spin up ClickUp space", "Wrike folder", "compare PM platforms", "PM tool migration", "portfolio dashboard".

## Setup

```bash
# Asana MCP v2 (GA Feb 2026, 42 tools — remote MCP at mcp.asana.com/v2/mcp)
# Connect via Claude Desktop / Cursor: paste https://mcp.asana.com/v2/mcp + OAuth flow

# Monday MCP (free on all plans)
npx -y @mondaydotcomorg/monday-api-mcp
# or remote:  https://mcp.monday.com/sse

# ClickUp MCP (Official, 49 tools across 14 categories)
# Connect via remote MCP at https://mcp.clickup.com or local:
npx -y @clickup/mcp-server

# Wrike — uses REST API v4 (no official MCP yet; cli-anything pattern)
curl -fsSL "https://www.wrike.com/api/v4/contacts" \
  -H "Authorization: bearer $WRIKE_TOKEN"
```

Auth:
- `ASANA_PAT` — personal access token from https://app.asana.com/0/my-apps (free) or OAuth via MCP install
- `MONDAY_API_TOKEN` — from monday.com Admin → API (free on all plans)
- `CLICKUP_API_KEY` — from ClickUp Settings → Apps → Generate API Token (free tier)
- `WRIKE_TOKEN` — permanent access token from Wrike → Apps → API (Business plan and above)

## Common recipes

### Recipe 1: Create an Asana project from charter
```bash
curl -X POST "https://app.asana.com/api/1.0/projects" \
  -H "Authorization: Bearer $ASANA_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "workspace": "<workspace-gid>",
      "team": "<team-gid>",
      "name": "Onboarding Revamp Q3",
      "notes": "Charter: https://notion.so/.../charter\nSponsor: VP Product\nSuccess criteria: D7 retention 35% → 42%",
      "default_view": "list",
      "color": "dark-green"
    }
  }'
```

### Recipe 2: Asana — bulk-create tasks from a WBS outline
```bash
# Each task gets the project_id and an optional parent task for hierarchy
for line in $(jq -c '.[]' wbs.json); do
  title=$(echo $line | jq -r '.title')
  parent=$(echo $line | jq -r '.parent // empty')
  estimate=$(echo $line | jq -r '.hours // 0')

  curl -s -X POST "https://app.asana.com/api/1.0/tasks" \
    -H "Authorization: Bearer $ASANA_PAT" \
    -d "{\"data\":{\"projects\":[\"<project-gid>\"],\"parent\":\"$parent\",\"name\":\"$title\",\"custom_fields\":{\"estimate_hours\":$estimate}}}"
done
```

### Recipe 3: Asana — add task dependency (predecessor)
```bash
# successor.add_dependencies → predecessor
curl -X POST "https://app.asana.com/api/1.0/tasks/<successor-gid>/addDependencies" \
  -H "Authorization: Bearer $ASANA_PAT" \
  -d '{"data":{"dependencies":["<predecessor-gid>"]}}'
```

### Recipe 4: Asana — Portfolio roll-up status
```bash
# List all projects in a portfolio with current status
curl -s "https://app.asana.com/api/1.0/portfolios/<portfolio-gid>/items?opt_fields=name,current_status_update.text,due_on" \
  -H "Authorization: Bearer $ASANA_PAT" \
| jq '.data[] | {name, status: .current_status_update.text, due: .due_on}'
```

### Recipe 5: Monday — create a board from a WBS
```bash
# Boards in monday.com use GraphQL
curl -X POST "https://api.monday.com/v2" \
  -H "Authorization: $MONDAY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"mutation { create_board(board_name: \"Onboarding Revamp\", board_kind: public, template_id: 12345) { id } }"}'

# Then add items with column values (status, person, date, dependency)
curl -X POST "https://api.monday.com/v2" \
  -H "Authorization: $MONDAY_API_TOKEN" \
  -d '{"query":"mutation { create_item(board_id: 1234567890, item_name: \"1.1.1 Sign-up flow refactor\", column_values: \"{\\\"status\\\":\\\"Working on it\\\",\\\"person\\\":{\\\"personsAndTeams\\\":[{\\\"id\\\":12345,\\\"kind\\\":\\\"person\\\"}]},\\\"date4\\\":{\\\"date\\\":\\\"2026-07-15\\\"}}\") { id } }"}'
```

### Recipe 6: Monday — set up automation (status change → notify)
```bash
# Automations use GraphQL via the automations API
curl -X POST "https://api.monday.com/v2" \
  -H "Authorization: $MONDAY_API_TOKEN" \
  -d '{"query":"mutation { create_automation(board_id: 1234567890, trigger: { type: \"status_change\", config: { column_id: \"status\", value: \"Stuck\" } }, action: { type: \"notify\", config: { person: 12345, message: \"Item stuck — please escalate\" } }) { id } }"}'
```

### Recipe 7: ClickUp — create a space + folder + list structure
```bash
# Space (top-level container)
curl -X POST "https://api.clickup.com/api/v2/team/<team-id>/space" \
  -H "Authorization: $CLICKUP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"Onboarding Revamp","multiple_assignees":true,"features":{"due_dates":{"enabled":true},"time_tracking":{"enabled":true},"dependencies":{"enabled":true},"sprints":{"enabled":true}}}'

# Folder inside space
curl -X POST "https://api.clickup.com/api/v2/space/<space-id>/folder" \
  -H "Authorization: $CLICKUP_API_KEY" \
  -d '{"name":"Sprints"}'

# List inside folder
curl -X POST "https://api.clickup.com/api/v2/folder/<folder-id>/list" \
  -H "Authorization: $CLICKUP_API_KEY" \
  -d '{"name":"Cycle 27","content":"Active sprint backlog","due_date":1721174400000,"priority":2}'
```

### Recipe 8: ClickUp — create task with custom fields + time estimate
```bash
curl -X POST "https://api.clickup.com/api/v2/list/<list-id>/task" \
  -H "Authorization: $CLICKUP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"1.2.1 Welcome modal copy",
    "description":"Acceptance: < 7 word headline, CTA passes accessibility",
    "assignees":[12345],
    "status":"to do",
    "priority":2,
    "due_date":1721174400000,
    "time_estimate":14400000,
    "custom_fields":[{"id":"<rice-field-id>","value":28.5}]
  }'
```

### Recipe 9: ClickUp — dashboard data export for status report
```bash
# Pull all tasks from a list with status, time tracked, due
curl -s "https://api.clickup.com/api/v2/list/<list-id>/task?include_closed=true&subtasks=true" \
  -H "Authorization: $CLICKUP_API_KEY" \
| jq '.tasks[] | {name, status: .status.status, due: .due_date, time_tracked: .time_spent}'
```

### Recipe 10: Wrike — create folder + task with custom field
```bash
# Folder
curl -X POST "https://www.wrike.com/api/v4/folders/<parent-id>/folders" \
  -H "Authorization: bearer $WRIKE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Onboarding Revamp","description":"Q3 activation initiative"}'

# Task with RAID custom field
curl -X POST "https://www.wrike.com/api/v4/folders/<folder-id>/tasks" \
  -H "Authorization: bearer $WRIKE_TOKEN" \
  -d '{"title":"Risk: SSO vendor SLA","description":"P=3 I=4 score=12","customFields":[{"id":"<raid-type-cf>","value":"Risk"},{"id":"<probability-cf>","value":"3"}]}'
```

### Recipe 11: Cross-platform portfolio export (Asana + Monday + ClickUp → Notion)
```bash
# Pull active projects from each platform, normalize, then post to Notion roll-up DB
asana_projects=$(curl -s "https://app.asana.com/api/1.0/portfolios/<gid>/items?opt_fields=name,current_status_update.text" -H "Authorization: Bearer $ASANA_PAT" | jq '.data')
monday_boards=$(curl -s -X POST "https://api.monday.com/v2" -H "Authorization: $MONDAY_API_TOKEN" -d '{"query":"{ boards(workspace_ids: [12345]) { name state } }"}' | jq '.data.boards')
clickup_spaces=$(curl -s "https://api.clickup.com/api/v2/team/<team-id>/space" -H "Authorization: $CLICKUP_API_KEY" | jq '.spaces')

jq -n --argjson a "$asana_projects" --argjson m "$monday_boards" --argjson c "$clickup_spaces" \
  '[($a[] | {platform:"asana",name:.name,status:.current_status_update.text}),
    ($m[] | {platform:"monday",name:.name,status:.state}),
    ($c[] | {platform:"clickup",name:.name,status:"active"})]'
```

### Recipe 12: Platform comparison decision matrix
| Capability | Asana | Monday | ClickUp | Wrike |
|---|---|---|---|---|
| MCP server | v2 (42 tools, Feb 2026) | yes (free all plans) | yes (49 tools, 14 cat) | no (REST v4) |
| Free tier users | 10 | 2 | unlimited (limited storage) | 5 |
| Time tracking native | no (Asana Time Tracking add-on) | no (column widget) | yes | yes |
| Gantt / Timeline | Premium plan | all plans | all plans | Business plan |
| Portfolios | Business plan | Pro plan | Business plan | Business plan |
| Dependencies | yes | yes (via column) | yes | yes |
| AI agents | Asana AI Studio | monday AI | ClickUp Brain | Wrike Work Intelligence |
| Goals | Asana Goals (Business+) | monday Goals | Goals native | Wrike Goals |
| Best for | cross-functional ops | visual ops/CRM | all-in-one (PM + docs + chat) | enterprise with workflow approvals |

## Examples

### Example 1: Migrate a Wrike portfolio to ClickUp
**Goal:** Move 15 active projects + 400 tasks from Wrike to ClickUp without losing dependencies or custom fields.

**Steps:**
1. Export Wrike folders: `curl ... /api/v4/folders -H bearer $WRIKE_TOKEN > wrike-export.json`
2. Map Wrike custom-field IDs → ClickUp custom-field IDs in a translation YAML
3. Create ClickUp space + folder structure mirroring Wrike folder tree
4. Loop tasks: translate fields, POST `/api/v2/list/<list-id>/task` per task
5. Loop dependencies: POST `/api/v2/task/<task-id>/dependency` after all tasks created
6. Diff: count tasks per side, sample-verify 10 randomly

**Result:** ClickUp workspace with full portfolio + dependency graph; Wrike archived read-only.

### Example 2: Set up a multi-team Asana portfolio with status rollup
**Goal:** VP wants 1 portfolio rolling up 6 cross-functional projects every Friday.

**Steps:**
1. Create portfolio: `POST /portfolios` named "Q3 Strategic Initiatives"
2. Add 6 projects: `POST /portfolios/<gid>/addItem` per project
3. Configure custom fields on portfolio: Health (single-select RAG), Owner, Due
4. Schedule automation via Asana Rules: every Friday 9am, pull `current_status_update` per project → Slack #q3-rollup channel
5. Mirror the rollup as a Notion DB sync via `notion-mcp`

**Result:** Live portfolio dashboard with auto-Friday-Slack-post.

## Edge cases / gotchas

- **Asana rate limits.** 1500 requests / minute per token (free plan: 150). Bulk creates should batch in chunks of 100 with 2s sleep.
- **Asana MCP scope.** v2 (GA Feb 2026) replaces the older Zapier-style integration; old Zapier flows may break — confirm with admin.
- **Monday API token format.** Authorization header is the bare token (no `Bearer` prefix). Documented but easy to miss.
- **Monday GraphQL string escaping.** Inner JSON for `column_values` must be JSON-string-escaped (double backslash). Use a real GraphQL client when possible.
- **ClickUp time estimates in ms.** `time_estimate` is milliseconds — 14400000 = 4 hours. Easy to off-by-1000.
- **ClickUp due_date in unix ms.** Not seconds. Convert: `date -d "2026-07-15" +%s%3N`.
- **ClickUp free tier.** Unlimited users but tasks lose Gantt + Workload after 100 task limit per space. For PMO-scale, paid plan required.
- **Wrike permanent tokens vs OAuth.** Permanent tokens lack revocation UI. For shared org use, OAuth via Wrike's app marketplace flow is safer.
- **Wrike custom field types.** Strings only via API; numbers stored as strings. Type-cast in client code.
- **Migration fidelity.** Asana custom fields don't 1:1 map to Monday columns or ClickUp custom fields. Always pre-build a translation table; expect to manually reconcile ~10% post-migration.
- **AI agent licensing.** Asana AI Studio, monday AI, ClickUp Brain, Wrike Work Intelligence are all paid add-ons even on enterprise tiers as of June 2026.

## Sources

- [Asana MCP server docs (v2, GA Feb 2026)](https://developers.asana.com/docs/mcp-server)
- [Asana REST API reference](https://developers.asana.com/reference)
- [Monday MCP getting started](https://support.monday.com/hc/en-us/articles/28588158981266-Get-started-with-monday-MCP)
- [Monday GraphQL API](https://developer.monday.com/api-reference/docs)
- [ClickUp MCP server](https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server)
- [ClickUp REST API v2](https://developer.clickup.com/reference)
- [Wrike API v4](https://developers.wrike.com)
- [PM platform comparison 2026 (Asana vs Monday vs ClickUp vs Wrike)](https://www.smartsheet.com/content/best-project-management-software)
