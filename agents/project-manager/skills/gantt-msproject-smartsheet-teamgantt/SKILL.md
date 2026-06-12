<!--
Source: https://smartsheet.redoc.l
Source: https://api-docs.teamgantt.com
Source: https://learn.microsoft.com/en-us/answers/questions/401702/is-it-possible-to-fetch-project-online-tasks-using
-->
# Gantt: MS Project / Smartsheet / TeamGantt — SKILL

The Gantt construction stack for 2026. Smartsheet is the API-first SOTA (CPM native, `inCriticalPath` flag per row). TeamGantt + GanttPRO are clean REST alternatives. MS Project for the Web stores data in Dataverse only (NOT standard Graph API) as of June 2026 — important for MS-stack shops.

## When to use

- Building a Gantt timeline with predecessors, durations, milestones, and resource assignment.
- Computing critical path (Smartsheet native) or exporting dep data for networkx-based CPM.
- Maintaining the timeline as plan changes; baseline + variance reporting.
- Cross-stack data export (MS Project → Smartsheet, TeamGantt → reports).

Trigger phrases: "build a Gantt", "timeline plan", "critical path", "Smartsheet sheet", "TeamGantt project", "predecessor chain", "schedule baseline".

## Setup

```bash
# Smartsheet — REST API
curl -fsSL "https://api.smartsheet.com/2.0/users/me" \
  -H "Authorization: Bearer $SMARTSHEET_TOKEN"

# TeamGantt — REST API
curl -fsSL "https://api.teamgantt.com/v1/current_user" \
  -H "Authorization: Bearer $TEAMGANTT_TOKEN"

# MS Project for the Web — Dataverse Web API (NOT Graph)
# Endpoint pattern: https://<org>.crm.dynamics.com/api/data/v9.2/msdyn_projects
# Requires Azure AD app registration + Dataverse service principal
```

Auth:
- `SMARTSHEET_TOKEN` — from https://app.smartsheet.com/b/home → Personal Settings → API Access (Pro/Business plan)
- `TEAMGANTT_TOKEN` — from https://app.teamgantt.com/settings/api (paid plans)
- MS Project for the Web — Azure AD app + `https://<org>.crm.dynamics.com/.default` scope; admin enrollment required

## Common recipes

### Recipe 1: Smartsheet — create a sheet with Gantt template
```bash
curl -X POST "https://api.smartsheet.com/2.0/sheets" \
  -H "Authorization: Bearer $SMARTSHEET_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Onboarding Revamp Q3 — Gantt",
    "columns": [
      {"title":"WBS","type":"TEXT_NUMBER","primary":true},
      {"title":"Task Name","type":"TEXT_NUMBER"},
      {"title":"Duration","type":"DURATION"},
      {"title":"Start","type":"DATE"},
      {"title":"Finish","type":"DATE"},
      {"title":"Predecessors","type":"PREDECESSOR"},
      {"title":"% Complete","type":"PERCENT","format":",,,,,,,,,2,2,1,2,2"},
      {"title":"Assigned To","type":"CONTACT_LIST"},
      {"title":"Status","type":"PICKLIST","options":["Not Started","In Progress","Complete","At Risk"]}
    ]
  }'
```

### Recipe 2: Smartsheet — enable Gantt + CPM on the sheet
```bash
# Project settings (enable Critical Path)
curl -X PUT "https://api.smartsheet.com/2.0/sheets/<sheet-id>" \
  -H "Authorization: Bearer $SMARTSHEET_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"projectSettings": {"workingDays":["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY"],"nonWorkingDays":["2026-07-04"],"lengthOfDay":8}}'
```

### Recipe 3: Smartsheet — add tasks with predecessor chain
```bash
curl -X POST "https://api.smartsheet.com/2.0/sheets/<sheet-id>/rows" \
  -H "Authorization: Bearer $SMARTSHEET_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[
    {"toBottom":true,"cells":[
      {"columnId":1111,"value":"1.0"},
      {"columnId":2222,"value":"Discovery"},
      {"columnId":3333,"value":"5d"},
      {"columnId":4444,"value":"2026-06-15"}
    ]},
    {"toBottom":true,"cells":[
      {"columnId":1111,"value":"2.0"},
      {"columnId":2222,"value":"Design"},
      {"columnId":3333,"value":"10d"},
      {"columnId":7777,"objectValue":{"objectType":"PREDECESSOR_LIST","predecessors":[{"rowId":"<row1-id>","type":"FS","lag":"0d"}]}}
    ]}
  ]'
```

Predecessor types: `FS` (finish-to-start, default), `SS`, `FF`, `SF`. Lag in days (`+3d` / `-2d`).

### Recipe 4: Smartsheet — query rows with critical-path flag
```bash
curl -s "https://api.smartsheet.com/2.0/sheets/<sheet-id>?include=rowPermalink,crossSheetReferences&columnIds=2222,3333,4444,5555&pageSize=500" \
  -H "Authorization: Bearer $SMARTSHEET_TOKEN" \
| jq '.rows[] | select(.inCriticalPath == true) | {
    wbs: .cells[0].value,
    name: .cells[1].value,
    duration: .cells[2].value,
    start: .cells[3].value,
    finish: .cells[4].value
  }'
```

### Recipe 5: Smartsheet — set baseline (snapshot for variance)
```bash
# Capture current Start/Finish into Baseline Start/Baseline Finish columns
# (Custom columns Baseline Start, Baseline Finish must exist on the sheet)
curl -s "https://api.smartsheet.com/2.0/sheets/<sheet-id>" -H "Authorization: Bearer $SMARTSHEET_TOKEN" \
| jq '.rows[] | {rowId: .id, start: .cells[3].value, finish: .cells[4].value}' \
> baseline-snapshot.json

# Loop and write to baseline columns
jq -c '.[]' baseline-snapshot.json | while read row; do
  rowId=$(echo $row | jq -r '.rowId')
  curl -X PUT "https://api.smartsheet.com/2.0/sheets/<sheet-id>/rows" \
    -H "Authorization: Bearer $SMARTSHEET_TOKEN" \
    -d "[{\"id\":$rowId,\"cells\":[{\"columnId\":8888,\"value\":$(echo $row | jq '.start')},{\"columnId\":9999,\"value\":$(echo $row | jq '.finish')}]}]"
done
```

### Recipe 6: TeamGantt — create a project + tasks with deps
```bash
# Create project
curl -X POST "https://api.teamgantt.com/v1/projects" \
  -H "Authorization: Bearer $TEAMGANTT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Onboarding Revamp Q3","start_date":"2026-06-15","end_date":"2026-09-30","color":"#5b9bd5"}'

# Add a group (level-1 WBS deliverable)
curl -X POST "https://api.teamgantt.com/v1/projects/<project-id>/groups" \
  -H "Authorization: Bearer $TEAMGANTT_TOKEN" \
  -d '{"name":"1.0 Discovery","color":"#fff2cc"}'

# Add a task within the group
curl -X POST "https://api.teamgantt.com/v1/projects/<project-id>/tasks" \
  -H "Authorization: Bearer $TEAMGANTT_TOKEN" \
  -d '{"name":"1.1 User interviews","group_id":<group-id>,"start_date":"2026-06-15","end_date":"2026-06-20"}'

# Add a dependency (FS — predecessor)
curl -X POST "https://api.teamgantt.com/v1/dependencies" \
  -H "Authorization: Bearer $TEAMGANTT_TOKEN" \
  -d '{"parent_task_id":<predecessor-id>,"child_task_id":<successor-id>}'
```

### Recipe 7: TeamGantt — assign people with hourly allocation
```bash
curl -X POST "https://api.teamgantt.com/v1/tasks/<task-id>/people" \
  -H "Authorization: Bearer $TEAMGANTT_TOKEN" \
  -d '{"user_id":12345,"hours":4}'
```

### Recipe 8: MS Project for the Web — query tasks via Dataverse
```bash
# Bearer from Azure AD token endpoint
TOKEN=$(curl -X POST "https://login.microsoftonline.com/<tenant>/oauth2/v2.0/token" \
  -d "client_id=<app-id>&client_secret=$AZ_SECRET&grant_type=client_credentials&scope=https://<org>.crm.dynamics.com/.default" \
  | jq -r '.access_token')

curl -s "https://<org>.crm.dynamics.com/api/data/v9.2/msdyn_projecttasks?\$filter=_msdyn_project_value eq <project-guid>&\$select=msdyn_subject,msdyn_scheduledstart,msdyn_scheduledend,msdyn_duration" \
  -H "Authorization: Bearer $TOKEN" \
  -H "OData-Version: 4.0" \
| jq '.value[]'
```

### Recipe 9: Smartsheet → JSON export for networkx CPM
```bash
# Pull rows + deps; emit edge list
curl -s "https://api.smartsheet.com/2.0/sheets/<sheet-id>" -H "Authorization: Bearer $SMARTSHEET_TOKEN" \
| jq '[.rows[] | {
    id: .id,
    name: .cells[1].value,
    duration: .cells[2].value,
    deps: (.cells[5].objectValue.predecessors // [] | map(.rowId))
  }]' > sheet-tasks.json

# Compute CPM via networkx (see critical-path-method-cpm skill)
```

### Recipe 10: Smartsheet → PPM Control Center blueprint deploy
```bash
# Control Center (enterprise) deploys a sheet/dashboard set from a template
# Trigger via Smartsheet Connector API
curl -X POST "https://control-api.smartsheet.com/blueprint/<blueprint-id>/deploy" \
  -H "Authorization: Bearer $SMARTSHEET_TOKEN" \
  -d '{"projectName":"Onboarding Revamp Q3","metadata":{"sponsor":"VP Product","budget":"180000"}}'
```

## Examples

### Example 1: Build a Gantt from a WBS in Smartsheet
**Goal:** WBS is finalized (12 deliverables, 47 work packages). Need a Gantt with critical path before Friday kickoff.

**Steps:**
1. Create sheet with Gantt template + CPM enabled (Recipes 1, 2).
2. Loop WBS leaves: POST rows with WBS code, name, duration, predecessors (Recipe 3).
3. Pull rows with `inCriticalPath == true` (Recipe 4).
4. Generate baseline snapshot (Recipe 5) and lock in Notion.
5. Export Gantt PNG via Smartsheet UI (no API export in 2026) for kickoff deck.

**Result:** Live Gantt in Smartsheet with critical path highlighted, baseline stored, 12-deliverable timeline ready.

### Example 2: Track schedule variance week-of
**Goal:** Weekly status: how far behind/ahead of baseline?

**Steps:**
1. Pull current rows: actual Start/Finish (or `% Complete` × duration estimate of EV).
2. Compare to baseline columns set at kickoff.
3. Compute variance per row: `actual_finish - baseline_finish` (negative = ahead).
4. Sum variance for critical-path rows only → schedule variance days.
5. Embed table in weekly status report.

**Result:** "On critical path: 2 tasks ahead by 1d, 1 task behind by 3d. Net SV = -2d. Mitigation in RAID-027."

## Edge cases / gotchas

- **Smartsheet `inCriticalPath` requires CPM enabled.** Dependencies + duration alone don't compute CPM — must set `projectSettings.workingDays` first.
- **Smartsheet `PREDECESSOR_LIST` lag format.** `+3d` for 3-day lag, `-2d` for lead. Hours: `+8h`. No mixed units.
- **Smartsheet rate limit: 300 req/min/token.** Bulk row writes use `POST /sheets/{id}/rows` with array up to 500 rows.
- **Smartsheet date format ISO-8601 only.** `2026-06-15`, not `06/15/2026`. Times are sheet-timezone-local.
- **TeamGantt deps are FS only.** No SS/FF/SF support as of 2026; if you need them, use Smartsheet.
- **TeamGantt date inclusive.** `end_date` is the last working day, NOT the day after. Off-by-one with Smartsheet semantics.
- **MS Project for the Web Dataverse-only.** Graph API does NOT expose msdyn_project entities as of June 2026. If your script uses Graph, it will fail — switch to Dataverse Web API + Azure AD client credentials.
- **MS Project Desktop ≠ MS Project for the Web.** Desktop .mpp files require XML export or 3rd-party converters (e.g., Office Add-in or `python-pptx-xml` parsers); no first-class API.
- **Baseline columns are custom.** Smartsheet doesn't ship Baseline Start/Finish columns by default; create them as DATE columns on the sheet.
- **Currency in Smartsheet.** Cost columns are TEXT_NUMBER; format via `format` string (codepoint sequence — copy from a working sheet).
- **Working days vs calendar days.** Default 5-day week. Holidays via `nonWorkingDays`. Forgetting to set holidays drifts the critical path silently.
- **GanttPRO REST API.** Available on Business plan; surface similar to TeamGantt. No CPM auto-flag — compute client-side.
- **% Complete for EV.** Pull `% Complete` column × planned budget per row for the EV input in `earned-value-management-ev-pv-eac-cpi-spi` skill.

## Sources

- [Smartsheet API reference](https://smartsheet.redoc.ly)
- [Smartsheet Project Settings (CPM)](https://help.smartsheet.com/articles/765650-enable-dependencies-other-advanced-project-settings)
- [Smartsheet inCriticalPath in API](https://community.smartsheet.com/discussion/79798/gantt-view-data-for-sheet-via-api)
- [TeamGantt API docs](https://api-docs.teamgantt.com)
- [GanttPRO REST API](https://ganttpro.com/help/api)
- [MS Project for the Web via Dataverse](https://learn.microsoft.com/en-us/dynamics365/project-operations/prod-pma/projects-overview)
- [Dataverse Web API reference](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/overview)
- [Project Online vs Project for the Web 2026 comparison](https://learn.microsoft.com/en-us/project-for-the-web/projectforweb-administrator-guide)
