<!--
Source: https://www.notion.so/templates/birthday-tracker + https://www.flexibits.com/cardhop + https://support.apple.com/en-us/HT204017
-->
# Birthday + Anniversary Tracking — SKILL

Never miss a birthday or anniversary. Lead-time reminders (2 weeks / 1 week / 3 days / day-of), gift fulfillment workflow, and a recipient log that gets smarter over time. Notion DB + recurring calendar events + automated nudges via `n8n-workflow-automation`.

## When to use this skill

- **"Don't let me forget bdays" / "track birthdays"** — direct trigger.
- **"Mom's birthday next month — remind me"** — single date.
- **Annual contact + bday import** — January 1 setup.
- **Wedding anniversary tracking** — different metadata than birthday.
- **Quarterly "who has bday soon"** — preventive review.

**Do NOT use this skill when:**
- The gift research itself — see `gift-research-shopping`.
- Contact management broadly — see `contact-book-maintenance-cardhop-notion`.
- Calendar protection — see `calendar-protection-motion-reclaim-sunsama`.

## Setup

### Notion Birthday/Anniversary DB schema

```
| Field | Type | Notes |
|---|---|---|
| Name | Title | |
| Relationship | Select | Family / Friend / Coworker / Partner |
| Date | Date | YYYY-MM-DD (year is optional but useful) |
| Occasion type | Select | Birthday / Anniversary / Other |
| Reminder days | Multi-select | 14, 7, 3, 0 |
| Gift budget | Number | $ |
| Last gift | Rollup → Gift Log | from gift-research-shopping |
| Card message draft | Text | annual template |
| Special notes | Text | e.g., loves chocolate, dietary, etc. |
| Address | Text | for shipped gifts |
```

### Required MCPs (in agent.yaml)

- `notion-mcp` — DB CRUD
- `google-calendar-mcp` — recurring events
- `n8n-workflow-automation` — automated nudges
- `gmail-mcp` — reminder emails
- `apple-reminders` — alt reminder backbone
- `twilio-mcp` — SMS reminders (optional)

### Optional: Cardhop / Apple Contacts birthday import

Apple Contacts has a "Birthday" field that auto-populates the iCloud "Birthdays" calendar (visible in Apple Calendar).

```bash
# Verify Apple Contacts birthdays
mcp tool icloud.list_contacts \
  --has-birthday true
```

## Common recipes

### Recipe 1: Add a contact's birthday to Notion DB

```bash
curl -X POST https://api.notion.com/v1/pages \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id":"<bday-db-id>"},
    "properties":{
      "Name":{"title":[{"text":{"content":"Mom"}}]},
      "Relationship":{"select":{"name":"Family"}},
      "Date":{"date":{"start":"1960-03-15"}},
      "Occasion type":{"select":{"name":"Birthday"}},
      "Reminder days":{"multi_select":[{"name":"14"},{"name":"7"},{"name":"3"},{"name":"0"}]},
      "Gift budget":{"number":150},
      "Address":{"rich_text":[{"text":{"content":"123 Main St, Anytown CA 94000"}}]}
    }
  }'
```

### Recipe 2: Annual recurring calendar event

```bash
mcp tool google-calendar.create_event \
  --summary "Mom's Birthday (65)" \
  --start "2026-03-15" \
  --end "2026-03-16" \
  --all-day true \
  --recurrence "RRULE:FREQ=YEARLY"
```

### Recipe 3: Multi-tier reminder events (lead-time milestones)

```bash
# T-14 days: research + decide
mcp tool google-calendar.create_event \
  --summary "T-14: Mom's bday — research + decide gift" \
  --start "2026-03-01" \
  --end "2026-03-01" \
  --all-day true \
  --recurrence "RRULE:FREQ=YEARLY"

# T-7 days: order
mcp tool google-calendar.create_event \
  --summary "T-7: Mom's bday — order gift" \
  --start "2026-03-08" \
  --end "2026-03-08" \
  --all-day true \
  --recurrence "RRULE:FREQ=YEARLY"

# T-3 days: card + reservation
mcp tool google-calendar.create_event \
  --summary "T-3: Mom's bday — card + dinner reservation" \
  --start "2026-03-12" \
  --end "2026-03-12" \
  --all-day true \
  --recurrence "RRULE:FREQ=YEARLY"

# Day-of: send + celebrate
mcp tool google-calendar.create_event \
  --summary "Mom's Birthday — call + send" \
  --start "2026-03-15T07:00:00-07:00" \
  --end "2026-03-15T08:00:00-07:00" \
  --recurrence "RRULE:FREQ=YEARLY"
```

### Recipe 4: n8n workflow — auto-generate reminder events

Run weekly to scan upcoming 30 days:

```yaml
# n8n workflow
- trigger: cron 0 8 * * MON (Mondays 8am)
- step: notion.query_database
    filter: Date is within next 30 days
- foreach result:
    step: build T-14/-7/-3/0 events
    step: google-calendar.create_event (each tier)
```

### Recipe 5: Daily morning digest of upcoming birthdays

```python
# Pull next 30 days
upcoming = notion_query_db(filter={"Date":{"within_days":30}})

# Compose digest
digest = "Upcoming birthdays + anniversaries (next 30 days):\n\n"
for u in upcoming:
    days_out = (u['Date'] - today).days
    digest += f"- {u['Name']} ({u['Relationship']}): {u['Date']} ({days_out} days out)\n"

# Email at 8am
gmail.send(to="me@personal.com", subject="Upcoming birthdays", body=digest)
```

### Recipe 6: SMS reminder via Twilio

```bash
# Send 24h before
mcp tool twilio.send_sms \
  --to "+14155551234" \
  --message "Tomorrow is Mom's birthday. Card draft: <link>. Call her after 10am PT."
```

### Recipe 7: Annual import from Apple/Google Contacts

```python
# Pull all contacts with birthdays from Google
import requests
contacts = requests.get(
    "https://people.googleapis.com/v1/people/me/connections?personFields=names,birthdays&pageSize=1000",
    headers={"Authorization": f"Bearer {GOOGLE_TOKEN}"}).json()

for c in contacts.get('connections', []):
    if c.get('birthdays'):
        name = c['names'][0]['displayName']
        bday = c['birthdays'][0]['date']
        # Add to Notion DB via Recipe 1
        add_to_notion_bday_db(name, bday)
```

### Recipe 8: Card / message draft 3 days out

```python
person = "Mom"
relationship = "Family"
last_gift = "scented candle (Loved)"
upcoming_event = "65th birthday"

prompt = f"""Draft a warm birthday card message for {person} ({relationship}).
Last year's gift was {last_gift}.
This year is {upcoming_event}.
Tone: warm, sincere, references the milestone."""

# Surface 3 variations via Claude
```

### Recipe 9: Reservation booking trigger 3 days out

Connect to `restaurant-reservations-opentable-resy-tock`:

```bash
# T-3 trigger: birthday dinner
# Surface: search restaurants for the celebration; recipe 7 (calendar hold) + recipe 10 (anniversary note) in restaurant skill
```

### Recipe 10: Card-physical ship (Postable / Paperless Post / Hallmark)

For physical cards:

```bash
# Postable
echo "https://postable.com/create?recipient_address=$ADDRESS&message=$MESSAGE"

# Paperless Post (digital + physical option)
echo "https://www.paperlesspost.com/"

# Hallmark (chains, basics)
echo "https://www.hallmark.com/cards/"
```

### Recipe 11: Anniversary-specific workflow

Same DB; "Anniversary" occasion type. Differences:
- Card tone (romantic vs warm)
- Shared experiences references
- Both partners' shared gift consideration

```bash
# Update DB entry
curl -X PATCH "https://api.notion.com/v1/pages/<page-id>" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -d '{
    "properties": {
      "Occasion type":{"select":{"name":"Anniversary"}}
    }
  }'
```

### Recipe 12: After-occasion log + reaction

```python
# Day after birthday: nudge user "how did it go?"
gmail.send(to=user, subject="Mom's birthday recap",
    body="How did Mom like the gift? Update the log: <notion-link>")

# User updates Reaction in gift log; agent learns for next year
```

### Recipe 13: Suppress for deceased / estranged

Add "Active" boolean to DB; agent skips inactive entries.

```bash
curl -X PATCH "https://api.notion.com/v1/pages/<page-id>" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -d '{"properties":{"Active":{"checkbox":false}}}'
```

## Examples

### Example 1: New user onboarding

**Goal:** Import all family/friend bdays + set up reminder pattern.

**Steps:**
1. Recipe 7: pull birthdays from Google Contacts (auto-fill DB).
2. User adds/corrects in Notion.
3. Recipe 4: enable n8n weekly scan.
4. Recipe 5: schedule daily 8am digest.
5. Recipe 2 + 3: for each entry, create recurring events + lead-time milestones.

**Result:** Full year of reminders set; first digest tomorrow.

### Example 2: Mom's 65th — full workflow

**Goal:** Mom's 65th birthday March 15; full lead-time.

**Steps:**
1. T-14 (Mar 1): trigger gift research — `gift-research-shopping` workflow.
2. T-7 (Mar 8): order gift; verify ship date.
3. T-3 (Mar 12): Recipe 8 (card draft); Recipe 9 (book restaurant — Recipe 6 in restaurants skill).
4. Day-of (Mar 15): Recipe 6 (SMS reminder) at 9am.
5. T+1 (Mar 16): Recipe 12 (reaction log).

**Result:** Full bday workflow without dropped balls.

### Example 3: Multi-relationship audit

**Goal:** Q1 review of all relationships + bday data.

**Steps:**
1. Recipe 5: digest of upcoming + already-passed in Q1.
2. For passed: confirm reaction logged.
3. For upcoming Q2: scan budget + lead-time conflicts.
4. Flag overlapping bdays in same week (split-budget consideration).

**Result:** Clean quarterly view + budget plan.

## Edge cases / gotchas

- **Year-unknown bday**: Some folks don't share their birth year. Store with Year=null; Recipe 2 still works.
- **Lunar / Hijri calendar bdays**: Chinese New Year birthday, Hijri Eid anniversary, etc. Notion DB stores Gregorian date — convert annually. Use `n8n-workflow-automation` with calendar conversion library.
- **Time zone for global friends**: "Send at 9am" — whose 9am? Surface attendee TZ.
- **Calendar bloat**: 50 friends × 4 events each = 200 recurring annual events. Use a separate "Birthdays" calendar so it doesn't clutter primary.
- **Apple Birthday calendar auto-fill**: If using Apple Contacts birthday field, the iCloud "Birthdays" calendar auto-populates. Don't double-up.
- **Card-ship deadline**: Physical card via Postable needs 3-5 biz days. T-7 may be too late for printed/shipped.
- **Calling time-zones**: Mom in EST; user in PST — "call after 10am PT" = 1pm her time, safe.
- **Surprise considerations**: If gift is from couple (anniversary), don't reveal in shared family calendar.
- **Estranged / deceased**: Recipe 13 — set Active=false; agent skips.
- **Year-aware "milestone"**: 50th, 65th, etc. Surface as "milestone year" in T-14 nudge.
- **Shared partner gift**: For spouse anniversary, gift from "us" not "me." Use joint budget + log.
- **Date format**: ISO YYYY-MM-DD throughout. Avoid US M/D/Y to prevent ambiguity.
- **Card delivery vs gift delivery**: Don't conflate. Card ships separately if physical.
- **Wedding anniversary gift conventions**: 1=paper, 5=wood, 10=tin, 25=silver, 50=gold. Surface as suggestion, not rule.

## Sources

- [Notion Birthday Tracker template](https://www.notion.so/templates/birthday-tracker)
- [Apple Contacts birthdays → calendar](https://support.apple.com/en-us/HT204017)
- [Google Calendar Family Sharing](https://support.google.com/calendar/answer/37082)
- [Postable](https://postable.com/)
- [Paperless Post](https://www.paperlesspost.com/)
- [Cardhop](https://www.flexibits.com/cardhop)
- [Hallmark](https://www.hallmark.com/cards/)
