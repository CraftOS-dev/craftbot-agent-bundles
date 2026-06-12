---
name: grant-deadline-calendar-management
description: Build and maintain a grant deadline calendar — Instrumentl for orgs with ≥10 active grants, Google Calendar + Notion/Airtable for <10. Track LOI / full proposal / decision / report dates. Use when the user says "set up our deadlines" / "build a grant calendar" / "we keep missing deadlines".
---

# Grant deadline calendar management

Missed deadlines = lost revenue. The right calendar tool depends on org size: ≥10 active grants → Instrumentl's pipeline tracker is SOTA; <10 → Google Calendar + Notion/Airtable scales beautifully. Either way: every grant has 5+ key dates and ALL of them belong on the calendar from day 1.

## When to use

- Org has missed a deadline and wants process fix
- Org is scaling fundraising and grant count is growing
- New grant writer onboarding and needs to see the deadline picture
- Annual grant cycle planning at the start of fiscal year
- Periodic refresh as new prospects move into pipeline

Do NOT use this skill for:
- Multi-grant pipeline status + win-rate analytics (→ `multi-grant-pipeline-mgmt`)
- Foundation cultivation cadence (touches with PO) (→ `foundation-cultivation-program-officer`)
- Individual deadline reminder ("remind me in 2 days") — use Google Calendar directly

## Setup

```bash
# For <10 grants — Google Calendar + Notion (recommended)
# No install — both via MCP

# For ≥10 grants — Instrumentl
# Recipient subscription required ($299/mo)
export INSTRUMENTL_API_KEY="..."

# For org spreadsheet adoption — Airtable
# Free tier sufficient up to 1200 records/base
export AIRTABLE_API_KEY="..."
```

Auth / API key requirements:
- Google Calendar MCP — OAuth (free)
- Notion MCP — integration token (free)
- Instrumentl — paid subscription
- Airtable — free or paid

## Common recipes

### Recipe 1: Five dates per grant — calendar all of them

```markdown
For EVERY grant in pipeline, calendar:

1. LOI deadline (if applicable)
2. Full proposal deadline
3. Expected decision date (from funder's published cycle)
4. Award acceptance window (if invited)
5. Report due dates (interim quarterly + annual + final + closeout)
6. Renewal LOI / next-cycle outreach date (1-2 months before close of grant period)
```

### Recipe 2: Google Calendar setup for <10 grants

```bash
# Create dedicated "Grants" calendar in Google Calendar
# Via google-calendar-mcp
gcal_create_calendar name="Grants" timezone="America/Los_Angeles"

# Add event per deadline
gcal_create_event \
  calendar="Grants" \
  title="LOI DUE: Hewlett ECE — $50K" \
  start="2026-09-15T17:00:00" \
  end="2026-09-15T18:00:00" \
  description="Funder: Hewlett Foundation\nProgram: Education\nAmount: $50K\nPO: Maria Hernandez\nLink to draft: <Notion URL>\nOwner: SC" \
  reminders='[{"method":"email","minutes":1440},{"method":"popup","minutes":120}]'
```

Color-code:
- Red = LOI/proposal due in <14 days
- Yellow = LOI/proposal due in 14-60 days
- Green = report due
- Blue = decision date / cultivation touchpoint

### Recipe 3: Notion pipeline DB schema

```markdown
| Property | Type | Notes |
|---|---|---|
| Funder | Title | |
| Project | Text | |
| Type | Select | Federal / State / Foundation / Corp / DAF |
| Amount requested | Number | USD |
| Stage | Select | Research / Cultivate / Drafting / Submitted / Decision / Awarded / Declined / Reporting / Renewal |
| LOI deadline | Date | |
| Full proposal deadline | Date | |
| Expected decision date | Date | |
| Award date | Date | |
| Reports due | Rollup | Linked Reports DB |
| Owner | Person | |
| PO name | Text | |
| Notes | Text | |
| Status color | Formula | Red <14 days, Yellow <60, Green else |
```

### Recipe 4: Notion → Google Calendar sync

```bash
# Notion + Google Calendar 2-way sync via Notion automation
# Settings → Integrations → Google Calendar → enable sync

# OR via webhook to Zapier / Make.com:
# Trigger: Notion record created/updated
# Action: Create Google Calendar event
```

### Recipe 5: Instrumentl pipeline (≥10 grants)

```bash
# Instrumentl has built-in pipeline tracker — no separate calendar setup
curl -H "Authorization: Bearer $INSTRUMENTL_API_KEY" \
  "https://api.instrumentl.com/v1/pipeline?status=open" \
  | jq '.[] | {funder, deadline, amount, stage}'

# Sync Instrumentl deadlines to Google Calendar
# Via Instrumentl Settings → Calendar Integrations → Google Calendar
```

### Recipe 6: Airtable schema for org-wide visibility

```markdown
## Base: "Grants"
### Table: "Pipeline"
| Field | Type |
|---|---|
| Funder | Single line text |
| Project | Single line text |
| Type | Single select |
| Amount | Currency |
| Stage | Single select |
| LOI deadline | Date |
| Full proposal deadline | Date |
| Decision date | Date |
| Owner | Collaborator |
| Funder Profile | Link to "Funders" table |
| Reports | Link to "Reports" table |

### Table: "Reports"
| Funder | Link to Pipeline |
| Report type | Single select (SF-425, SF-PPR, narrative, financial, final) |
| Due date | Date |
| Status | Single select |
| Owner | Collaborator |
```

### Recipe 7: 30/60/90-day deadline scan

```bash
# Weekly Monday scan: what's due in next 30/60/90 days
# Via notion-mcp
notion_query database="Grants_Pipeline" \
  filter='{"property":"deadline","date":{"next_30_days":true}}' \
  sort='[{"property":"deadline","direction":"ascending"}]'

# Output to Slack channel
slack_post channel="#grants" message="<30/60/90-day deadline summary>"
```

### Recipe 8: Reverse-plan from deadline

```markdown
## Working-backward template
**Deadline:** <date>
**Draft 1 due to ED for review:** Deadline - 14 days
**Differential review meeting:** Deadline - 10 days
**Final revisions:** Deadline - 5 days
**Sign-off:** Deadline - 2 days
**Submission day:** Deadline - 1 day (buffer for portal issues)
```

Don't submit on deadline day. Federal portals slow under deadline-day load; foundation portals occasionally time out.

### Recipe 9: Annual + quarterly planning rhythm

```markdown
## Annual (Q1 of fiscal year)
- Review prior FY grant pipeline (won/lost/declined patterns)
- Identify funder cycles for the year (LOI windows)
- Set fundraising goal by quarter

## Quarterly
- Refresh prospect research (skill: grant-prospect-research-...)
- Update foundation profile cards
- Move stale prospects out of pipeline

## Monthly
- Pipeline review with ED + Finance + Program leads
- 30/60/90-day deadline scan
- Reporting schedule check (any overdue?)

## Weekly
- Monday: deadline scan + day-of-week task list
- Friday: progress check + roll forward
```

### Recipe 10: Backup + audit trail

```bash
# Monthly export of Notion DB as CSV (backup against accidental delete)
notion_export database="Grants_Pipeline" format="csv" \
  output="backups/grants_pipeline_$(date +%Y%m).csv"

# Quarterly: archive completed grants (Awarded + Reported + Closed) to "Archive" view
```

## Examples

### Example 1: Org with 6 active grants — set up Google Calendar + Notion

**Goal:** Org with 6 grants needs a calendar that the ED, finance, and program lead can all see.

**Steps:**
1. Create "Grants" calendar in Google Workspace; share with ED + Finance + Program leads.
2. Build Notion pipeline DB with schema from Recipe 3.
3. Enter all 6 grants with all 5+ dates each.
4. Enable Notion + Google Calendar sync (Recipe 4).
5. Color-code Google Calendar events.
6. Configure email reminders 14 days + 2 hours before each deadline.
7. Add weekly Monday 9am recurring "30/60/90 deadline scan" calendar event.

**Result:** All deadlines visible to leadership; reminders in place; weekly scan ritual established.

### Example 2: Scaling to 15+ active grants — migrate to Instrumentl

**Goal:** Org grew to 15 active grants; manual Notion isn't scaling.

**Steps:**
1. Subscribe to Instrumentl ($299/mo).
2. Import existing pipeline from Notion CSV.
3. Configure deadline sync to Google Calendar.
4. Keep Notion as documents library; Instrumentl as live pipeline.
5. Train staff on Instrumentl dashboard.
6. Set Slack notifications via Instrumentl's Slack integration for <14-day deadlines.

**Result:** Scaled to Instrumentl's purpose-built tracker; Notion archived as docs library.

## Edge cases / gotchas

- **Time zone gotcha:** Federal portals use Eastern Time. A 5pm ET deadline = 2pm PT. Calendar in deadline's TZ, not yours.
- **Funder cycle dates ≠ written deadline.** Many foundations publish "rolling" or "two cycles per year" without exact dates. Calendar BOTH the prior year's actual decision date AND the published window.
- **Decision dates slip:** Federal can take 3-6 months past stated decision date. Calendar both the stated and a +6 month "follow-up" date.
- **Report deadlines are 90 days post-end-of-period for most federal.** Calendar 60 days out to start drafting + 90 days out to confirm GL ready.
- **Notion + Google Calendar sync delays.** Sync may lag 1-5 minutes. Don't rely on it for last-minute alerts.
- **Instrumentl's "deadline" field is the proposal deadline, NOT LOI deadline.** Add LOI separately or use the custom field.
- **Reminders only work if calendar shared with the right people.** Solo calendar = solo accountability; shared = team accountability.
- **Holiday + federal closure days affect deadlines.** Verify deadline is not on a federal holiday (rare auto-extension; usually no extension).
- **Closeout report 90 days post end-of-period.** Often missed because the project feels "done." Calendar at award start.
- **Multi-funder same-day deadlines.** Federal has predictable end-of-quarter spikes; foundations cluster around fiscal-year-end. Pace cultivation cycle to avoid jam.

## Sources

- Grants.com — Step-by-step Grant Calendar 2026: https://grants.com/step-by-step-guide-to-building-a-grant-calendar-that-maximizes-your-funding-chances-in-2026
- Grant Ready KY — Grant Calendar without Expensive Software: https://www.grantreadyky.org/learn/resources/how-to-build-a-grant-calendar-without-expensive-software
- Instrumentl Grant Management Software: https://www.instrumentl.com/blog/best-grant-management-software
- Notion templates for grants: https://www.notion.com/templates
- Google Calendar API: https://developers.google.com/calendar
- Airtable for nonprofits: https://www.airtable.com/solutions/nonprofits
