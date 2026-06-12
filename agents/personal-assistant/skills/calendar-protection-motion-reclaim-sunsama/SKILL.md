<!--
Source: https://docs.usemotion.com/ + https://reclaim.ai/api + https://www.sunsama.com/
Comparison: https://reclaim.ai/blog/motion-vs-reclaim-2026 + https://www.sunsama.com/blog/best-daily-planner-2026
-->
# Calendar Protection — Motion / Reclaim.ai / Sunsama — SKILL

AI-driven calendar protection + time blocking. Pick the right tool for the user, set up the defense pattern (focus blocks, family dinner, gym, recovery), and let the system reshuffle when meetings shift. Motion owns scheduling for power-users; Reclaim defends Google Calendar with Habits + Smart 1:1s; Sunsama runs morning/evening rituals with multi-source task pull.

## When to use this skill

- **"Block my calendar" / "protect my focus" / "stop the meeting bloat"** — user asking for AI-defended time.
- **"Set up Motion / Reclaim / Sunsama"** — direct platform request.
- **Onboarding a new EA / chief-of-staff workflow** — recommend the right protector by user style.
- **Weekly calendar audit** — Sunday review where protected blocks should be re-confirmed.
- **Cross-team focus defense** — Reclaim's Smart 1:1s find mutually-defended windows without back-and-forth.

**Do NOT use this skill when:**
- Single ad-hoc meeting creation — call `google-calendar-mcp` directly.
- The user already has a paid Calendly setup and just needs scheduling links — see `scheduling-calendly-cal-com-oncehub`.
- Family calendar coordination specifically — see `family-calendar-coordination`.

## Pick the right tool

| User profile | Recommendation | Why |
|---|---|---|
| Power-user; wants one app for tasks + projects + calendar | **Motion** | Auto-schedules tasks into the day, reshuffles on conflict, projects + deadlines |
| Already on Google Calendar; needs focus defense + 1:1s | **Reclaim.ai** | Sits on top of GCal; Habits defend blocks; Smart 1:1s |
| Loves morning + evening rituals; wants task pull from Todoist / Linear / Asana | **Sunsama** | Daily-ritual layer; multi-source aggregate; calm-aware design |
| Universal inbox feel for tasks | **Akiflow** | 30+ source consolidation |

## Setup

### Motion (API access — Business + Enterprise tiers)

```bash
# Motion CLI does not exist; use REST via cli-anything.
export MOTION_API_KEY="<from-app.usemotion.com/web/settings/api>"

# Smoke test
curl -s https://api.usemotion.com/v1/users/me \
  -H "X-API-Key: $MOTION_API_KEY"
```

Motion REST docs: https://docs.usemotion.com/

### Reclaim.ai (REST API + Google Calendar OAuth)

```bash
# Reclaim does not publish a CLI; use cli-anything.
export RECLAIM_TOKEN="<from-app.reclaim.ai/settings/integrations>"

# Smoke test
curl -s https://api.app.reclaim.ai/api/users/current \
  -H "Authorization: Bearer $RECLAIM_TOKEN"
```

### Sunsama (no public REST API as of 2026)

Sunsama exposes Zapier triggers + Make.com hooks but not a direct REST. Use:
- `n8n-workflow-automation` skill for any automation that wraps Sunsama.
- Manual ritual configuration via app — agent provides the recommended ritual structure but the user owns the click-through.

## Common recipes

### Recipe 1: Audit the next 4 weeks of calendar load

Before recommending a tool, surface the user's actual ratio of focus / meeting / family / dead-time.

```bash
# Pull events via google-calendar-mcp, then categorize
mcp tool google-calendar.list_events \
  --calendarId primary \
  --timeMin "$(date -u +%Y-%m-%dT00:00:00Z)" \
  --timeMax "$(date -u -d '+28 days' +%Y-%m-%dT00:00:00Z)" \
  --maxResults 500 \
  > calendar_audit.json
```

Then categorize in Python (illustrative):

```python
buckets = {'focus':0, 'meeting':0, 'family':0, 'personal':0, 'dead':0}
for evt in events:
    title = evt['summary'].lower()
    if 'focus' in title or 'deep work' in title: buckets['focus'] += duration
    elif 'family' in title or 'dinner' in title: buckets['family'] += duration
    elif evt.get('attendees', []): buckets['meeting'] += duration
    else: buckets['personal'] += duration
```

### Recipe 2: Create a Reclaim Habit (defended focus block)

```bash
curl -X POST https://api.app.reclaim.ai/api/habits \
  -H "Authorization: Bearer $RECLAIM_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Deep Focus AM",
    "durationMin": 120,
    "windowStart": "09:00",
    "windowEnd": "12:00",
    "days": ["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY"],
    "priority": "P1",
    "defenseLevel": "HARD"
  }'
```

`defenseLevel: HARD` = cannot be overridden by external bookings. `SOFT` = can be reshuffled.

### Recipe 3: Create a Reclaim Smart 1:1 (mutually-defended window)

```bash
curl -X POST https://api.app.reclaim.ai/api/one-on-ones \
  -H "Authorization: Bearer $RECLAIM_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "1:1 with Alex",
    "attendeeEmail": "alex@company.com",
    "durationMin": 30,
    "cadence": "WEEKLY",
    "preferredDayOfWeek": "WEDNESDAY",
    "preferredTime": "14:00"
  }'
```

Reclaim asks both calendars and lands on a mutually free window.

### Recipe 4: Create a Motion task with auto-scheduling

```bash
curl -X POST https://api.usemotion.com/v1/tasks \
  -H "X-API-Key: $MOTION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Q3 Strategy Doc",
    "workspaceId": "<workspace-id>",
    "duration": 360,
    "dueDate": "2026-08-15T23:59:00Z",
    "priority": "HIGH",
    "autoScheduled": {
      "startDate": "2026-08-01",
      "schedule": "Work Hours"
    }
  }'
```

Motion auto-splits a 6h estimate into multiple sessions before the deadline.

### Recipe 5: List Motion-scheduled blocks for the next 7 days

```bash
curl -s https://api.usemotion.com/v1/tasks \
  -H "X-API-Key: $MOTION_API_KEY" \
  -G --data-urlencode 'scheduledStart_gte=2026-06-10T00:00:00Z' \
     --data-urlencode 'scheduledStart_lte=2026-06-17T23:59:59Z' \
  | jq '.tasks[] | {name, scheduledStart, scheduledEnd, status}'
```

### Recipe 6: Reclaim — pull defended-time analytics

```bash
curl -s https://api.app.reclaim.ai/api/analytics/time-spent \
  -H "Authorization: Bearer $RECLAIM_TOKEN" \
  -G --data-urlencode 'startDate=2026-06-01' \
     --data-urlencode 'endDate=2026-06-30'
```

Returns breakdown by category (focus, meetings, personal, habits).

### Recipe 7: Configure Sunsama daily ritual (recommended structure)

Sunsama doesn't auto-configure via API. Surface the recommended structure for user to set up:

```markdown
**Morning ritual (Sunsama)**
1. Review yesterday's incomplete tasks (auto-rollover)
2. Pull from sources: Todoist + Linear + Notion + Gmail starred
3. Time-box each task (Sunsama enforces "this fits in your day?")
4. Set a daily goal + 1 ritual
5. Start the day

**Evening ritual (Sunsama)**
1. Mark done / push tomorrow
2. Reflect: what went well / what didn't
3. Pre-plan tomorrow's anchors
4. Close laptop
```

### Recipe 8: Defend family-dinner block in Google Calendar (universal)

If user doesn't use Motion/Reclaim, create a hard recurring block directly via `google-calendar-mcp`:

```bash
mcp tool google-calendar.create_event \
  --calendarId primary \
  --summary "Family Dinner — DO NOT BOOK" \
  --start "2026-06-10T18:00:00-07:00" \
  --end   "2026-06-10T19:30:00-07:00" \
  --recurrence "RRULE:FREQ=DAILY;BYDAY=MO,TU,WE,TH,FR,SA,SU" \
  --transparency opaque \
  --visibility private
```

## Examples

### Example 1: New user onboarding — pick + set up protection

**Goal:** User says "my calendar is out of control; help me protect focus time."

**Steps:**
1. Audit (Recipe 1): pull next 4 weeks, surface ratio (e.g., "65% meetings, 12% focus, 8% family, 15% dead-time").
2. Ask 3 qualifying questions:
   - "Do you want one app to own tasks + calendar (Motion) or sit on top of Google Calendar (Reclaim)?"
   - "Do you value a morning + evening ritual (Sunsama as a layer)?"
   - "Family time blocks — daily 6-8pm OK?"
3. Recommend tool based on answers + set up first 3 protected blocks:
   - Deep Focus AM (Mon-Fri 9-11am, HARD)
   - Family Dinner (daily 6-7:30pm, HARD)
   - Gym (Mon/Wed/Fri 7am, SOFT)
4. Create via Recipe 2 (Reclaim) or Recipe 4 (Motion).
5. Schedule Sunday 8pm "Weekly Calendar Audit" recurring via `google-calendar-mcp`.

**Result:** User has 3 defended blocks live + weekly audit ritual scheduled.

### Example 2: Cross-team 1:1 setup

**Goal:** EA needs to set up weekly 1:1 between the boss + 5 direct reports without back-and-forth.

**Steps:**
1. For each direct report, run Recipe 3 with `cadence: WEEKLY` + preferred day.
2. Reclaim finds mutually-defended windows for each pair.
3. Verify all 5 land before the next week's start.
4. Add `meeting-prep-briefs-from-granola-fathom` skill as the prep step.

**Result:** 5 recurring 1:1s scheduled + auto-defended.

### Example 3: Motion deadline-driven project block

**Goal:** Q3 strategy doc due Aug 15, est. 6h effort, must fit before deadline.

**Steps:**
1. Recipe 4: create Motion task with `duration: 360`, `dueDate: 2026-08-15`.
2. Motion auto-schedules 3 × 2h sessions in available Deep Focus windows.
3. Recipe 5: verify blocks land on calendar.
4. If meeting added later that conflicts, Motion reshuffles automatically.

**Result:** 3 protected work sessions for the doc — agent doesn't have to manage shuffle.

## Edge cases / gotchas

- **Motion tier**: Motion REST API requires Business plan ($19/mo) or higher. Personal plan ($34/mo legacy) does NOT include API access. Verify before promising.
- **Reclaim free tier**: Free plan limits to 2 Habits + 2 Smart 1:1s. Recommend Pro ($10/mo) for full defense pattern. Source: https://reclaim.ai/pricing
- **Defense level vs reality**: HARD defense in Reclaim still respects "decline-and-propose" meetings if the inviter overrides. Set up a Gmail filter to flag override attempts.
- **Sunsama lacks public REST**: Use Zapier or n8n wrappers; do NOT promise direct API access. Recommend `n8n-workflow-automation` for any automation that touches Sunsama.
- **Motion + Reclaim conflict**: Don't run both on the same calendar — they each try to own scheduling and will fight. Pick one.
- **Calendar OAuth scope**: Reclaim + Motion both need full Google Calendar read/write. If user is on Workspace with admin restrictions, OAuth may fail — escalate to IT.
- **TZ handling**: All three tools default to user-profile TZ; when user travels, Reclaim auto-adjusts, Motion auto-adjusts, Sunsama requires manual TZ swap.
- **Recurring habit drift**: Reclaim Habits drift if user keeps overriding; surface drift via Recipe 6 analytics monthly.
- **Motion mobile-only flows**: Some Motion features (project Kanban) are desktop-only; iOS/Android limited. Don't recommend Motion as primary if user is mobile-first.
- **Sunsama 14-day trial**: After trial ends, $20/mo. No free tier. Source: https://www.sunsama.com/pricing
- **API rate limits**: Motion ~60 req/min per key; Reclaim ~120 req/min. Batch Habit/1:1 creation rather than per-event.

## Sources

- [Motion docs](https://docs.usemotion.com/)
- [Reclaim API](https://reclaim.ai/api)
- [Sunsama](https://www.sunsama.com/)
- [Motion vs Reclaim 2026 comparison](https://reclaim.ai/blog/motion-vs-reclaim-2026)
- [Best daily planner 2026](https://www.sunsama.com/blog/best-daily-planner-2026)
- [Akiflow (alternative)](https://akiflow.com/)
