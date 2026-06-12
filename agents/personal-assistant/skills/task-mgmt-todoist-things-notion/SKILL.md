<!--
Source: https://developer.todoist.com/ + https://culturedcode.com/things/support/articles/2803573/ + https://developers.notion.com/
Comparison: https://www.zapier.com/blog/best-todo-list-apps
-->
# Task Management — Todoist / Things 3 / Notion / Apple Reminders — SKILL

Cross-platform task CRUD + daily/weekly planning. Todoist owns the largest GTD ecosystem with Natural Language; Things 3 is Apple-only single-purchase refinement; Notion Tasks is database-driven for cross-domain; Apple Reminders is the iOS-native voice-first default.

## When to use this skill

- **"Add a task" / "remind me to X"** — direct trigger.
- **"What's on my list today?"** — daily plan view.
- **"Move X to next week"** — reschedule.
- **Weekly review (GTD-style)** — Sunday planning ritual.
- **Cross-app task migration** — moving between Todoist, Things, Notion.

**Do NOT use this skill when:**
- Calendar event creation — see `google-calendar-mcp`.
- Project planning with deadlines that need scheduling — see `calendar-protection-motion-reclaim-sunsama` (Motion).
- Personal life recurring chores — overlap; pick this if user wants task-list, calendar-protection if user wants time-block.

## Pick the right tool

| User profile | Tool | Why |
|---|---|---|
| Cross-platform; largest GTD; Natural Language | **Todoist** | Web + mac + win + ios + android; REST API |
| Apple-only; single purchase ($50); zero subscription | **Things 3** | Mac/iOS only; URL scheme + AppleScript |
| Database-driven; cross-link to projects/companies | **Notion Tasks** | Relational; cross-domain integration |
| Apple ecosystem; voice-first ("Hey Siri…") | **Apple Reminders** | iOS native; shared lists; free |
| Pomodoro + habits + free tier | **TickTick** | Free; habit tracker |
| Engineering tracker for prosumers | **Linear** | Linear for life; some prosumers |
| Mac/iOS power-user GTD | **OmniFocus 4** | Subscription; deepest GTD |
| Microsoft ecosystem | **Microsoft To-Do** | M365 default |

## Setup

### Todoist (REST API v2)

```bash
# Get API token: https://todoist.com/app/settings/integrations/developer
export TODOIST_TOKEN="<token>"

curl -s https://api.todoist.com/rest/v2/projects \
  -H "Authorization: Bearer $TODOIST_TOKEN"
```

Docs: https://developer.todoist.com/rest/v2/

### Things 3 (URL scheme + AppleScript — Mac/iOS)

```bash
# Open Things and create task
open "things:///add?title=Q3+Strategy+Doc&when=tomorrow&list=Work&notes=See+brief"

# Full URL scheme docs:
# https://culturedcode.com/things/support/articles/2803573/
```

Things doesn't have REST. URL scheme is the official automation.

### Notion (REST)

```bash
# Internal integration token: https://www.notion.so/my-integrations
export NOTION_TOKEN="secret_..."

curl -s 'https://api.notion.com/v1/users/me' \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28"
```

### Apple Reminders (via `apple-reminders` skill — already in agent.yaml)

```bash
mcp tool apple-reminders.create \
  --list "Default" \
  --title "Pick up dry cleaning" \
  --due "2026-06-12 17:00"
```

### TickTick / Linear / OmniFocus

- TickTick: REST at https://developer.ticktick.com/
- Linear: GraphQL at https://developers.linear.app/
- OmniFocus: URL scheme `omnifocus://x-callback-url/add`

## Common recipes

### Recipe 1: Todoist — create task with natural language

```bash
curl -X POST https://api.todoist.com/rest/v2/tasks \
  -H "Authorization: Bearer $TODOIST_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Q3 strategy doc",
    "due_string": "tomorrow at 10am",
    "due_lang": "en",
    "priority": 3,
    "project_id": "<project-id>",
    "labels": ["@work","@focus"]
  }'
```

Priority 1=lowest, 4=highest. Natural language parses "every Monday", "next Friday at 5pm", etc.

### Recipe 2: Todoist — list today's tasks

```bash
curl -s "https://api.todoist.com/rest/v2/tasks?filter=today" \
  -H "Authorization: Bearer $TODOIST_TOKEN" \
  | jq '.[] | {id, content, due: .due.string, priority}'
```

Filters: `today`, `tomorrow`, `next 7 days`, `overdue`, `p1`, `@label`.

### Recipe 3: Todoist — complete a task

```bash
TASK_ID="<id>"
curl -X POST "https://api.todoist.com/rest/v2/tasks/$TASK_ID/close" \
  -H "Authorization: Bearer $TODOIST_TOKEN"
```

### Recipe 4: Todoist — reschedule a task

```bash
TASK_ID="<id>"
curl -X POST "https://api.todoist.com/rest/v2/tasks/$TASK_ID" \
  -H "Authorization: Bearer $TODOIST_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"due_string":"next Monday"}'
```

### Recipe 5: Todoist — recurring task

```bash
curl -X POST https://api.todoist.com/rest/v2/tasks \
  -H "Authorization: Bearer $TODOIST_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Take out garbage",
    "due_string": "every Sunday at 8pm",
    "labels": ["@home"]
  }'
```

### Recipe 6: Things — add via URL scheme

```bash
# Mac
open "things:///add?title=Buy+groceries&when=today&list=Errands&tags=Home&notes=Costco%20list%20attached"

# Multi-line URL scheme example with checklist
open "things:///add?title=Pack+for+trip&when=2026-07-14&checklist-items=Passport,Toiletries,Charger,Phone%20cable"
```

URL scheme full reference: https://culturedcode.com/things/support/articles/2803573/

### Recipe 7: Notion — add task to a database

```bash
curl -X POST https://api.notion.com/v1/pages \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id":"<db-id>"},
    "properties":{
      "Name":{"title":[{"text":{"content":"Q3 strategy doc"}}]},
      "Due":{"date":{"start":"2026-08-15"}},
      "Status":{"select":{"name":"Not Started"}},
      "Priority":{"select":{"name":"P2"}}
    }
  }'
```

### Recipe 8: Notion — query open tasks

```bash
curl -X POST https://api.notion.com/v1/databases/<db-id>/query \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "filter":{"and":[
      {"property":"Status","select":{"does_not_equal":"Done"}},
      {"property":"Due","date":{"on_or_before":"2026-06-15"}}
    ]},
    "sorts":[{"property":"Due","direction":"ascending"}]
  }'
```

### Recipe 9: Apple Reminders — voice-first via MCP

```bash
mcp tool apple-reminders.create \
  --list "Groceries" \
  --title "Almond milk" \
  --notes "Costco brand"

mcp tool apple-reminders.list --list "Groceries" --include-completed false
```

### Recipe 10: Cross-app daily plan

```python
import requests
# Pull from Todoist (work)
work = requests.get("https://api.todoist.com/rest/v2/tasks?filter=today",
    headers={"Authorization":f"Bearer {TODOIST}"}).json()
# Pull from Notion (cross-domain)
notion = requests.post(f"https://api.notion.com/v1/databases/{NOTION_DB}/query",
    headers={"Authorization":f"Bearer {NOTION_TOKEN}","Notion-Version":"2022-06-28"},
    json={"filter":{"property":"Due","date":{"equals":TODAY}}}).json()

plan = []
for t in work: plan.append((t['content'], t.get('due',{}).get('string'), 'work'))
for n in notion['results']:
    title = n['properties']['Name']['title'][0]['text']['content']
    plan.append((title, 'today', 'personal'))

print("Today:")
for item in plan: print(f"  - [{item[2]}] {item[0]}")
```

### Recipe 11: Bulk-import from meeting action items

After `meeting-prep-briefs-from-granola-fathom`, push commitments:

```python
for ai in my_action_items:
    requests.post("https://api.todoist.com/rest/v2/tasks",
        headers={"Authorization":f"Bearer {TODOIST}"},
        json={"content": ai['task'],
              "due_string": ai.get('due', 'this Friday'),
              "description": f"From: {ai['meeting']} ({ai['date']})",
              "labels":["@meeting-action"]})
```

### Recipe 12: GTD weekly review

```python
# Pull all open tasks; categorize
open_tasks = requests.get("https://api.todoist.com/rest/v2/tasks",
    headers={"Authorization":f"Bearer {TODOIST}"}).json()
overdue = [t for t in open_tasks if is_overdue(t)]
this_week = [t for t in open_tasks if is_this_week(t)]
nothing_scheduled = [t for t in open_tasks if not t.get('due')]
```

Surface: review overdue, batch-reschedule, schedule unscheduled.

### Recipe 13: Migrate Todoist → Things

```bash
# Export Todoist (full list, JSON)
curl -s "https://api.todoist.com/rest/v2/tasks?project_id=<>" \
  -H "Authorization: Bearer $TODOIST_TOKEN" > export.json

# Convert each to Things URL scheme
python -c "
import json, urllib.parse, subprocess
for t in json.load(open('export.json')):
  url = f\"things:///add?title={urllib.parse.quote(t['content'])}\"
  if t.get('due'): url += f\"&when={t['due']['date']}\"
  subprocess.run(['open', url])
"
```

## Examples

### Example 1: Capture-from-voice → daily plan

**Goal:** User dictates "remind me Q3 doc tomorrow 10am" + 3 more.

**Steps:**
1. Recipe 1: 4 tasks created in Todoist.
2. Recipe 2: list "today" + "tomorrow" — verify they land.
3. Surface today's plan.

**Result:** Tasks captured + planned in <30s.

### Example 2: GTD Sunday review

**Goal:** Weekly review ritual; clear overdue + plan upcoming.

**Steps:**
1. Recipe 12: pull overdue + open + unscheduled.
2. For each overdue: reschedule (Recipe 4) or complete (Recipe 3).
3. For unscheduled: assign due date.
4. Recipe 11: pull this-week meeting action items.
5. Recipe 10: surface daily plan for Monday.

**Result:** Inbox-zero for tasks; week ahead planned.

### Example 3: Apple-only user

**Goal:** Power-user on Mac/iOS wants Things 3 + Apple Reminders for chores.

**Steps:**
1. Things for projects + tasks (Recipe 6).
2. Apple Reminders for voice-first chores (Recipe 9).
3. Avoid Todoist (cross-platform overhead they don't need).

**Result:** Native Apple stack; no friction.

## Edge cases / gotchas

- **Todoist Pro tier**: REST API free; some features (reminders, themes) require Pro ($4/mo). Source: https://todoist.com/pricing
- **Todoist natural language**: Parses dates in user locale. Set `due_lang` if non-English.
- **Things URL scheme limits**: Max URL length ~2k chars on iOS Safari. For longer task details, use `notes` field.
- **Things on iOS — Shortcuts**: Best automation is via Apple Shortcuts → URL scheme; not via curl.
- **Notion API rate**: 3 req/sec; bulk imports need throttling.
- **Notion DB schema lock**: Adding new properties via API requires DB-level edit permission — verify Internal integration is shared with the DB.
- **Apple Reminders sharing**: Shared lists work great across family; not great across companies (iCloud per-account).
- **Recurring task semantics**: Todoist "every Sunday" vs "every 7 days" differs — first respects DOW, second respects relative.
- **Completion vs archive**: Todoist complete = removed from active. Notion archive = different prop. Be explicit.
- **Cross-app sync drift**: If using both Todoist + Notion, agent must pick source-of-truth or risk dup.
- **iCloud Apple Reminders MCP**: Read/write requires iCloud auth; behavior changes after macOS upgrade.
- **TickTick free**: Capable; ads. Premium $28/yr. Source: https://www.ticktick.com/pricing
- **OmniFocus 4 subscription**: $10/mo or buy ($75 Mac + $50 iOS). Source: https://www.omnigroup.com/omnifocus
- **Linear for personal**: Works but tracks issues not GTD; overkill unless user already there.

## Sources

- [Todoist REST API](https://developer.todoist.com/rest/v2/)
- [Things URL scheme](https://culturedcode.com/things/support/articles/2803573/)
- [Notion API](https://developers.notion.com/)
- [Apple Reminders Help](https://support.apple.com/guide/reminders/welcome/mac)
- [TickTick API](https://developer.ticktick.com/)
- [Best to-do list apps 2026 (Zapier)](https://www.zapier.com/blog/best-todo-list-apps)
- [OmniFocus 4](https://www.omnigroup.com/omnifocus)
