<!--
Source: https://temporal.day/blog/motion-vs-reclaim-vs-clockwise-vs-akiflow-vs-sunsama
Calendar protection: Motion / Reclaim / Sunsama / Akiflow (Clockwise EOL March 2026)
-->
# Calendar Time Protection — Motion / Reclaim / Sunsama / Akiflow

30-day calendar audit + rule-based time protection across the 2026 stack. **Clockwise shut down March 2026 (Salesforce acquisition).** Replacements: Motion (auto-rebuild day around new meetings — best for 20+ meetings/wk), Reclaim (focus-time + habit defense), Sunsama (calm morning ritual + pulls from Asana/Linear/Todoist/Gmail/Slack), Akiflow (command-bar power user). Calendar audit via `gcalcli-calendar` skill or `google-calendar-mcp`.

## When to use

- 30-day calendar audit on a CEO drowning in meetings.
- Setting up time-protection rules for a new exec.
- Killing recurring meetings that lost purpose.
- Defending deep-work blocks for strategy / writing.
- Switching tools after Clockwise EOL.

Trigger phrases: "audit my calendar", "too many meetings", "focus time", "Motion vs Reclaim", "kill recurring meetings", "deep work block".

## Setup

```bash
# Motion — auto-rebuild day
curl -fsSL "https://api.usemotion.com/v1/me" \
  -H "X-API-Key: $MOTION_API_KEY"

# Reclaim — focus-time + habits
curl -fsSL "https://api.app.reclaim.ai/api/users/current" \
  -H "Authorization: Bearer $RECLAIM_API_KEY"

# Sunsama — morning ritual
curl -fsSL "https://api.sunsama.com/v1/me" \
  -H "Authorization: Bearer $SUNSAMA_API_KEY"

# Akiflow — command bar
curl -fsSL "https://api.akiflow.com/v1/me" \
  -H "Authorization: Bearer $AKIFLOW_API_KEY"

# gcalcli for audit
gcalcli calw 4 --calendar primary
```

Auth / API key requirements:
- `MOTION_API_KEY` — Motion Settings → API ($19/mo+ Pro tier).
- `RECLAIM_API_KEY` — Reclaim Settings → Developer ($10/mo+ Lite tier).
- `SUNSAMA_API_KEY` — Sunsama Settings → API ($16/mo).
- `AKIFLOW_API_KEY` — Akiflow Settings → API ($12/mo+).
- `GOOGLE_OAUTH_TOKEN` — for calendar audit.

## Common recipes

### Recipe 1: 30-day calendar audit (gcalcli)

```bash
# Pull last 30 days
gcalcli --calendar primary agenda \
  "$(date -d '30 days ago' +%F)" "$(date +%F)" \
  --tsv > calendar-last-30d.tsv

# Aggregate stats
python3 <<'EOF'
import csv
from collections import defaultdict
totals = defaultdict(int)
counts = defaultdict(int)
recur = defaultdict(int)
with open('calendar-last-30d.tsv') as f:
    r = csv.DictReader(f, delimiter='\t')
    for row in r:
        dur_min = int((parse(row['end']) - parse(row['start'])).total_seconds() / 60)
        counts['total'] += 1
        totals['total'] += dur_min
        if 'recurring' in row.get('recurring', ''):
            recur[row['summary']] += 1

print(f"Total meetings: {counts['total']}")
print(f"Total meeting hours: {totals['total']/60:.1f}")
print(f"Avg per week: {counts['total']/4:.1f}")
print(f"Recurring meetings >6 months: {len([k for k,v in recur.items() if v>=8])}")
EOF
```

### Recipe 2: Audit checklist (targets per stage)

```markdown
## 30-day audit checklist (solo founder / small-team CEO)

- [ ] Total meetings: # per week (target < 25 solo founder, < 35 with leadership team)
- [ ] Focus-time ratio: contiguous ≥90-min blocks / total working hours (target ≥30%)
- [ ] 1:1 ratio: # of 1:1s / # of total meetings (target 25-40%)
- [ ] Recurring meeting count: # set up >6 months ago (kill candidates if no explicit value)
- [ ] No-meeting day: defended? (target 1 day/week)
- [ ] Meeting length default: 25/50 min (NOT 30/60 — Parkinson's law)
- [ ] Travel + commute: # hours/week (audit if >5h)
- [ ] Energy alignment: hardest work in personal-peak hours? (audit via self-report)
```

### Recipe 3: Motion — auto-rebuild day

```bash
# Set Motion to auto-schedule tasks around meetings
curl -X PATCH "https://api.usemotion.com/v1/users/me/settings" \
  -H "X-API-Key: $MOTION_API_KEY" \
  -d '{
    "auto_schedule":true,
    "work_hours":{"start":"09:00","end":"18:00"},
    "deep_work_blocks":[{"days":["TUE","THU"],"start":"09:00","end":"12:00","label":"Strategy"}],
    "no_meeting_day":"FRI"
  }'
```

### Recipe 4: Reclaim — habit + focus time

```bash
# Create a focus-time habit
curl -X POST "https://api.app.reclaim.ai/api/habits" \
  -H "Authorization: Bearer $RECLAIM_API_KEY" \
  -d '{
    "name":"Deep work — strategy",
    "duration_minutes":120,
    "frequency":"DAILY",
    "preferred_times":["MORNING"],
    "buffer_minutes":15,
    "auto_decline":false,
    "block_meetings":true
  }'

# Defend a habit (e.g., gym, lunch)
curl -X POST "https://api.app.reclaim.ai/api/habits" \
  -H "Authorization: Bearer $RECLAIM_API_KEY" \
  -d '{
    "name":"Lunch",
    "duration_minutes":45,
    "frequency":"DAILY",
    "preferred_times":["12:00-14:00"],
    "block_meetings":true
  }'
```

### Recipe 5: Sunsama — morning planning ritual

```bash
# Sunsama pulls tasks from connected sources for today's plan
curl -X POST "https://api.sunsama.com/v1/today/plan" \
  -H "Authorization: Bearer $SUNSAMA_API_KEY" \
  -d '{
    "intention":"Lock Series B narrative + run 2 1:1s",
    "tasks":[
      {"source":"linear","id":"<linear-issue-id>"},
      {"source":"gmail","id":"<email-thread>"},
      {"source":"asana","id":"<task-id>"}
    ]
  }'
```

### Recipe 6: Kill recurring meetings >6 months without value

```bash
# Identify candidates
mcp tool google-calendar.list_events \
  --calendar primary \
  --recurring-only \
  --created-before "$(date -d '6 months ago' +%F)" \
| jq '.events[] | select(.recurrence != null) | {summary, recurrence, created}'

# For each candidate, ask 3 questions in a CEO review:
echo "1. What decision does this meeting enable?
2. What changes if we skip it next time?
3. Could a 5-line written update replace it?"

# Kill confirmed-dead ones
mcp tool google-calendar.delete_event --calendar primary --event-id "<recurring-event-id>"
```

### Recipe 7: 25/50 min defaults (Parkinson's law)

```bash
# Set default duration to 25 min for 30-min slots, 50 min for 60-min slots
mcp tool google-calendar.update_settings \
  --calendar primary \
  --default-event-duration 25

# Use Calendly speed-meeting setting
mcp tool calendly.update_event_type --type-id "<30-min-type>" --duration 25
```

### Recipe 8: No-meeting day — defend ruthlessly

```bash
# Block Friday all day as "Deep Work — No Meetings"
mcp tool google-calendar.create_event \
  --calendar primary \
  --summary "🚫 No-meeting day — Deep Work" \
  --start "2027-04-09T00:00:00" \
  --end "2027-04-09T23:59:59" \
  --recurrence "RRULE:FREQ=WEEKLY;BYDAY=FR" \
  --visibility public \
  --description "Defended day. Decline new meetings; suggest async or reschedule."
```

### Recipe 9: Akiflow — command bar for fast capture

```bash
# Akiflow's strength: cmd+space → "schedule 30min strategy review tomorrow"
# Pull tasks across Linear / Asana / Gmail / Slack into one keyboard-driven UI
curl -X POST "https://api.akiflow.com/v1/tasks" \
  -H "Authorization: Bearer $AKIFLOW_API_KEY" \
  -d '{
    "title":"Review Series B narrative",
    "source":"linear",
    "due_at":"2027-04-15T17:00:00Z",
    "schedule_at":"2027-04-15T14:00:00Z",
    "duration_minutes":90
  }'
```

### Recipe 10: Default-decline rules

```markdown
## Default-decline rules

Decline + reply with context if any:
- No agenda in invite
- You don't know why you're invited
- > 4 attendees and you're not deciding anything
- Recurring + 6 months old + no recent decision came out
- Conflict with focus-time block (Recipe 4)

Template reply:
"Thanks for the invite. Can you share the agenda + what decision you need from me? I might be able to async — happy to comment on a doc if so."
```

### Recipe 11: Calendar-audit dashboard (Notion)

```bash
mcp tool notion.create_page \
  --parent '{"page_id":"<ceo-hub>"}' \
  --children-markdown "## Calendar Audit — $(date +%F)

Total meetings last 30d: 87
Avg per week: 21.8
Total meeting hours: 52.3
Focus-time hours: 31.2 (target 40+)
Focus-time ratio: 37%

Recurring meetings to kill (3):
- 'PM weekly review' (set up 9 months ago; replaced by Linear updates)
- 'Brand sync' (set up 14 months ago; no decisions in 4 months)
- 'CS weekly' (overlaps with all-hands; merge)

Rules applied:
- Default to 25/50 min (was 30/60)
- Friday no-meeting day defended
- Reclaim: Strategy focus 9-11 Tue + Thu

Next audit: $(date -d '30 days' +%F)"
```

### Recipe 12: Routing — which tool when

```markdown
| CEO style | Pick |
|---|---|
| Heavy meeting load (20+/wk), wants auto-rebuild | Motion |
| Wants focus-time + habit defense | Reclaim |
| Reflective planner, morning ritual | Sunsama |
| Command-bar power user pulling tasks from everywhere | Akiflow |
| Unified calendar + tasks single tool | Morgen |
| Free fallback | gcalcli + manual rules |
```

## Examples

### Example 1: New CEO 30-day calendar audit

**Goal:** First audit; identify wins.

**Steps:**
1. Pull 30-day data (Recipe 1).
2. Run checklist (Recipe 2). Note target gaps.
3. Audit recurring meetings (Recipe 6) — kill 2-3.
4. Set 25/50 defaults (Recipe 7).
5. Defend 1 no-meeting day (Recipe 8).
6. Pick a tool (Recipe 12). Subscribe + configure.
7. Apply rules (Recipe 4 or 3).
8. Set 30-day re-audit (Recipe 11).

**Result:** Meeting hours down 20-30%; focus-time ratio up 10pp.

### Example 2: Migrate off Clockwise (EOL March 2026)

**Goal:** Clockwise sunset; transition team to Reclaim.

**Steps:**
1. Identify Clockwise habits + focus blocks per user.
2. Recreate in Reclaim (Recipe 4) — habits + focus time + meeting-block.
3. Set team-wide default templates in Reclaim.
4. Communicate transition + train via Loom (`loom-async-video-comms` skill).
5. Sunset Clockwise after 2-week parallel run.

**Result:** No focus-time regression during transition.

## Edge cases / gotchas

- **Clockwise gone March 2026.** Salesforce acquired and shut down. Reclaim is closest 1:1 replacement.
- **Motion's auto-rebuild can confuse colleagues.** Their meeting got moved without notice. Educate the team or use "reschedule with notification."
- **Reclaim's habits block sneakily.** Sometimes blocks for habits aren't visible to others; check share settings.
- **Sunsama is intentional.** Morning ritual is the value; without it, you're paying for a worse Todoist.
- **Akiflow keyboard-first.** Power users love it; non-keyboard users won't get the value.
- **Free tiers limited.** Motion / Reclaim / Sunsama all have free trials; paid tiers ($10-19/mo) needed for sustained use.
- **No-meeting day = political.** Educate team; otherwise people book and you decline → tension. Make Friday no-meeting the company policy.
- **25/50 min defaults compound.** Each 5-min recovery × 10 meetings/day = 50 min back. Easiest win.
- **Calendar audit quarterly.** Without re-audit, meetings creep back.
- **Travel + commute counted.** Don't double-book time when you're physically moving.
- **Tool fragmentation risk.** Don't use Motion + Reclaim + Sunsama all at once. Pick ONE primary.
- **Personal calendar separation.** Personal commitments visible-busy but private-detail. Use a separate calendar layered into main view.
- **Defended doesn't mean blocked-from-bookers.** Use "ask before scheduling" rather than full block where possible.

## Sources

- [Motion vs Reclaim vs Clockwise vs Akiflow vs Sunsama](https://temporal.day/blog/motion-vs-reclaim-vs-clockwise-vs-akiflow-vs-sunsama)
- [Best time-blocking apps 2026 — Arahi](https://arahi.ai/blog/best-time-blocking-apps-and-planners-2026)
- [Motion API docs](https://docs.usemotion.com)
- [Reclaim API docs](https://reclaim.ai/api)
- [Sunsama API docs](https://api.sunsama.com)
- [Akiflow API docs](https://docs.akiflow.com)
- [Clockwise EOL announcement (Salesforce)](https://salesforce.com/news/) (March 2026)
