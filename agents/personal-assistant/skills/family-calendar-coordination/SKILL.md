<!--
Source: https://support.google.com/calendar/answer/37082 + https://www.cozi.com/ + https://timetreeapp.com/
-->
# Family Calendar Coordination — SKILL

One shared family calendar (Google Family Sharing / Apple Family / Cozi); per-member individual calendars subscribing to shared; anchor events tagged; chore-rotation matrix; conflict detection. Cozi adds meal-plan + shopping-list + chore-chart in one app. TimeTree handles multi-region. Skylight is the kitchen-display tablet.

## When to use this skill

- **"Sync our family calendar"** — initial setup.
- **"Why am I double-booked?"** — conflict detection.
- **"Whose turn is X chore?"** — rotation matrix.
- **"Family event next Sat"** — add anchor event.
- **Annual school calendar import** — beginning-of-school-year setup.

**Do NOT use this skill when:**
- Personal calendar only — see `calendar-protection-motion-reclaim-sunsama`.
- Travel/vacation planning — see `vacation-planning-end-to-end`.
- Birthday tracking specifically — see `birthday-anniversary-tracking`.

## Pick the right tool

| Profile | Tool | Why |
|---|---|---|
| Most universal; Google ecosystem | **Google Family Sharing** | Free; works on all devices via iCal subscribe |
| Apple ecosystem (all family on iOS/Mac) | **Apple Calendar Family Sharing** | Native iCloud; voice via Siri |
| Family-specific (cal + meal + shop + chore) | **Cozi** | Integrated household OS |
| Multi-region / extended family | **TimeTree** | Locking, multi-cal merge |
| Kitchen display + paper calendar replacement | **Skylight** | Hardware tablet + cloud sync |

## Setup

### Google Family Sharing

```bash
# Family group setup: https://families.google.com/families
# Shared calendar appears under "Family" calendar in each member's Google Calendar
mcp tool google-calendar.list_calendars
```

Look for calendar with `accessRole: family`.

### Apple Family Sharing

```bash
# iCloud Family Sharing: Settings > [Your Name] > Family Sharing
# Shared "Family" calendar auto-created
mcp tool icloud.list_calendars
```

### Cozi (no public API)

```bash
# Web: https://www.cozi.com/
# Cozi has its own iCal subscription + family-app UI
echo "https://my.cozi.com/Public/Calendar.aspx?u=<id>"
```

### TimeTree

```bash
# REST API for personal use: https://timetreeapp.com/developers
export TIMETREE_TOKEN="<token>"
curl -s "https://timetreeapis.com/calendars" \
  -H "Authorization: Bearer $TIMETREE_TOKEN"
```

### Notion family-coordination DB

For chore matrix + meal plan + family wiki.

## Common recipes

### Recipe 1: Identify shared family calendar in Google

```bash
mcp tool google-calendar.list_calendars
# Look for calendars labeled "Family" or with accessRole=family
```

Get the calendar ID for shared.

### Recipe 2: Create a family anchor event

Anchor = non-movable, family-wide visible.

```bash
mcp tool google-calendar.create_event \
  --calendarId "<family-calendar-id>" \
  --summary "School Recital — Sophie (Anchor)" \
  --location "Hudson Middle School Auditorium" \
  --start "2026-06-15T18:00:00-07:00" \
  --end "2026-06-15T20:00:00-07:00" \
  --reminders '[{"method":"popup","minutes":2880}]'  # 2 days
```

### Recipe 3: Color-code per family member

Google Calendar: each person color-codes shared events.

```bash
mcp tool google-calendar.update_event \
  --calendarId "<family-id>" \
  --eventId "<event-id>" \
  --colorId 7  # 7=peacock for "Mom"; per Google color enum
```

Color IDs: https://developers.google.com/calendar/api/v3/reference/colors

### Recipe 4: Subscribe each member to shared

Each family member's individual calendar app subscribes to the shared.

Google Calendar:
- Settings → Add calendar → Subscribe → enter shared calendar address

Apple Calendar:
- File → New Calendar Subscription → URL

iCal feeds usually at: `https://calendar.google.com/calendar/ical/<calendar-id>/public/basic.ics`

### Recipe 5: Conflict detection (anchor vs work)

```python
import requests
# Pull next 14 days from family calendar
fam = google_calendar.list_events(calendar_id=family_id, time_min=today, time_max=today+14d)
anchors = [e for e in fam if 'Anchor' in e['summary']]

# Pull each member's work calendar
for member in members:
    work = google_calendar.list_events(calendar_id=member['email'], time_min=today, time_max=today+14d)
    for a in anchors:
        conflicts = [w for w in work if overlaps(w, a)]
        if conflicts:
            print(f"CONFLICT: {member['name']} has '{conflicts[0]['summary']}' during anchor '{a['summary']}'")
```

### Recipe 6: Chore rotation matrix in Notion

```bash
curl -X POST https://api.notion.com/v1/pages \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -d '{
    "parent":{"database_id":"<chore-db-id>"},
    "properties":{
      "Chore":{"title":[{"text":{"content":"Garbage night"}}]},
      "Cadence":{"select":{"name":"Weekly"}},
      "Member A days":{"multi_select":[{"name":"Mon"},{"name":"Wed"}]},
      "Member B days":{"multi_select":[{"name":"Tue"},{"name":"Thu"}]},
      "Member C days":{"multi_select":[{"name":"Fri"}]}
    }
  }'
```

### Recipe 7: Recurring chore reminder to specific member

```bash
mcp tool google-calendar.create_event \
  --calendarId "<family-id>" \
  --summary "Garbage night — Member A" \
  --start "2026-06-09T19:00:00-07:00" \
  --end "2026-06-09T19:15:00-07:00" \
  --recurrence "RRULE:FREQ=WEEKLY;BYDAY=MO,WE" \
  --reminders '[{"method":"popup","minutes":30}]'
```

### Recipe 8: Cozi import — household tasks

Cozi has its own UI; no direct API. Surface deep-link:

```bash
echo "https://my.cozi.com/Public/Calendar.aspx?u=<id>"
```

Or: pull Cozi shared iCal → import to Notion + Google Calendar.

### Recipe 9: Weekly family meeting agenda

```markdown
**Family Sunday Meeting — Weekly**

1. Review last week (5 min)
   - What worked / didn't
2. Next week anchor events (5 min)
   - School / activities / family
3. Chore check (5 min)
4. Meal plan (10 min)
5. Family fun this week (5 min)
6. Anyone needs anything? (5 min)
```

Schedule via Google Calendar; surface in `notion-mcp`.

### Recipe 10: School calendar import

```bash
# Most schools publish ICS feeds; subscribe
SCHOOL_ICS="https://school.edu/calendar.ics"

mcp tool google-calendar.import_ics \
  --url "$SCHOOL_ICS" \
  --calendarId "<family-id>"
```

If no ICS, scrape via `firecrawl-mcp` and create events.

### Recipe 11: Pickup/dropoff coordination

For school pickups, create recurring per-parent:

```bash
mcp tool google-calendar.create_event \
  --calendarId "<family-id>" \
  --summary "Pickup — Sophie — Mom" \
  --start "2026-06-10T15:00:00-07:00" \
  --end "2026-06-10T15:30:00-07:00" \
  --recurrence "RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR;UNTIL=20260620T000000Z"
```

### Recipe 12: Travel-affecting-household

When one parent travels, surface family impact:

```bash
mcp tool google-calendar.create_event \
  --calendarId "<family-id>" \
  --summary "Mom traveling Jul 15-21 (return Sun PM)" \
  --start "2026-07-15" \
  --end "2026-07-21" \
  --all-day true \
  --description "Dad solo parenting; school pickups shift to Dad Mon-Fri"
```

### Recipe 13: Shared shopping list via Notion / Apple Reminders

```bash
mcp tool apple-reminders.create \
  --list "Groceries (Shared)" \
  --title "Almond milk"

# All family members can read + write the shared list
```

### Recipe 14: Skylight kitchen-display sync

Skylight subscribes to family calendar via Skylight Cloud app. Setup once; auto-syncs.

## Examples

### Example 1: New family — set up shared calendar

**Goal:** Mom + Dad + 2 kids; need one shared calendar.

**Steps:**
1. Recipe 1: identify family calendar (set up via Google Family if not).
2. Recipe 4: each member subscribes on own device.
3. Recipe 6 + 7: chore matrix + recurring chore reminders.
4. Recipe 10: school calendar ICS import.
5. Recipe 11: pickup/dropoff per parent.
6. Recipe 9: schedule weekly Sunday family meeting.

**Result:** Family calendar live; nobody double-books.

### Example 2: Conflict detection — work vs school recital

**Goal:** Mom's work has 6pm meeting on day of Sophie's recital.

**Steps:**
1. Recipe 5: detect conflict 2 days out.
2. Surface to Mom for resolution (reschedule meeting OR delegate recital coverage).
3. If reschedule meeting: open Calendly link / direct email to participants.
4. Update family calendar with resolution note.

**Result:** Anchor event not missed.

### Example 3: Travel impact week

**Goal:** Mom flying Jul 15-21; need to update pickup schedule.

**Steps:**
1. Recipe 12: add travel block to family calendar.
2. Recipe 7: update recurring pickup to Dad-only for that week.
3. Notify family via `gmail-mcp` digest.

**Result:** Household coverage handled.

## Edge cases / gotchas

- **Permission levels**: Google Family / Apple Family share by default. Be careful before sharing private events.
- **Color confusion**: Don't auto-color; let each member pick their color.
- **Time zone gotcha**: For families across time zones, set TZ explicitly on each event. Default-local can confuse.
- **iCloud + Google interop**: Cross-platform iCloud → Google sync via ICS subscribe works but has 1-24h delay.
- **Cozi paid tier**: Cozi Gold $39.99/yr for ad-free + extras. Free version has ads.
- **TimeTree free vs Premium**: Free for personal use; Premium $39.99/yr.
- **Recurring + holidays**: Recurring chore on a holiday — surface to user for "skip or do?".
- **Kids on iCloud Family**: < 13 needs parent setup of Apple ID. Different sharing rules.
- **School ICS quality**: Some schools' ICS feeds have wrong TZ or all-day. Verify before import.
- **Skylight setup**: Skylight needs wifi + paid plan ($39/yr) for full features.
- **Privacy of shared events**: Don't share medical / mental health / sensitive without consent.
- **Cozi vs Google Family — pick one**: Don't run both. Migrate fully.
- **Chore guilt**: Don't auto-publicly call out missed chores. Soft nudges, not public failure log.
- **Family-meeting cadence**: Sunday 6pm common. Don't run more than weekly.
- **Adult children**: Sharing slightly different — opt-in subscription, not auto.

## Sources

- [Google Family Shared Calendar](https://support.google.com/calendar/answer/37082)
- [Apple Family Sharing](https://www.apple.com/family-sharing/)
- [Cozi](https://www.cozi.com/)
- [TimeTree](https://timetreeapp.com/)
- [Skylight](https://www.skylightframe.com/)
- [Google Calendar Color IDs](https://developers.google.com/calendar/api/v3/reference/colors)
