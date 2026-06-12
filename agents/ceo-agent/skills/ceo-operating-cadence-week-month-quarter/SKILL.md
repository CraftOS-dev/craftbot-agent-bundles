<!--
Source: https://www.capitaly.vc/blog/david-sacks-operating-cadence-weekly-metrics-okrs-ceo-dashboard
CEO operating cadence: David Sacks rhythm doc + calendar + initiative tracking
-->
# CEO Operating Cadence — Week / Month / Quarter

David Sacks operating cadence — weekly metrics + 1:1s, monthly roadmap + forecast + budget variances, quarterly OKR + priority reset + QBR, annual strategy + capital + hiring plan. Documented operating rhythm doc in Notion so the company knows when decisions get made and where to surface inputs. Calendar locked. Initiative tracking in Linear.

## When to use

- Onboarding leadership team to the operating rhythm.
- New CEO setting up their first cadence.
- Mid-year refresh after major change (new exec, market shift).
- Annual cadence relock (after planning offsite).

Trigger phrases: "operating rhythm", "weekly cadence", "monthly cadence", "operating cadence", "weekly metrics", "cadence doc", "operating system".

## Setup

```bash
# Notion for the operating rhythm doc
mcp tool notion.search --query "Operating rhythm"

# Google Calendar for recurring blocks
mcp tool google-calendar.list_calendars

# Linear for initiative tracking
mcp tool linear.search --query "initiative"
```

Auth / API key requirements:
- `NOTION_API_KEY` — for operating rhythm doc + cadence calendar.
- `GOOGLE_OAUTH_TOKEN` — for recurring calendar blocks.
- `LINEAR_API_KEY` — for cadence-driven initiatives.

## Common recipes

### Recipe 1: Operating rhythm doc template

```bash
mcp tool notion.create_page \
  --parent '{"page_id":"<exec-hub>"}' \
  --properties '{"title":[{"text":{"content":"[Company] Operating Rhythm — 2027"}}]}' \
  --children-markdown '# Operating Rhythm — 2027

## Weekly (every Monday 9-10am PT)
- Metrics review (CEO + leads)
- Unblock issues
- Decisions (DACI-driven)
Pre-read: Sunday EOD. Owner: CEO.

## Weekly (Friday 1-5pm PT)
- 1:1s with direct reports (rotating slots — 45 min each)
- Coaching + KR check-ins
Owner: CEO. Tool: Lattice 1:1s.

## Monthly (last Thursday)
- Roadmap review (60 min)
- Forecast + budget variances (60 min)
- Hiring plan check-in (30 min)
Pre-read: 48h ahead. Owner: CEO + CFO + leads.

## Quarterly (first Thursday of quarter)
- QBR (60 min, 5-component, 60% decisions)
- OKR setting (in dedicated 1-day session)
- Strategy update
Pre-read: 48h ahead. Owner: CEO + leadership.

## Annual (Dec 15-16)
- Strategy + capital + hiring plan (2-day offsite)
- Wardley refresh
- Operating rhythm relock
Pre-work: pre-mortem + bottom-up team plans T-14. Owner: CEO + leadership + board chair.

## Board (every 8 weeks)
- Board pack delivered 72h ahead
- 2-hour meeting + 30-min closed session
- Minutes published within 48h
Owner: CEO + board ops.

## All-hands (weekly + monthly)
- Weekly 30-min (Thu 10am PT)
- Monthly 60-min (1st Thu) with theme
Owner: CEO + leaders.
'
```

### Recipe 2: Calendar lock — recurring blocks

```bash
# Weekly metrics review
mcp tool google-calendar.create_event \
  --calendar leadership@company.com \
  --summary "Weekly Metrics Review" \
  --start "2027-01-06T09:00:00" --end "2027-01-06T10:00:00" \
  --recurrence "RRULE:FREQ=WEEKLY;BYDAY=MO;COUNT=52"

# Monthly variance review
mcp tool google-calendar.create_event \
  --calendar leadership@company.com \
  --summary "Monthly Variance Review" \
  --start "2027-01-30T10:00:00" --end "2027-01-30T11:30:00" \
  --recurrence "RRULE:FREQ=MONTHLY;BYDAY=-1TH;COUNT=12"

# Quarterly QBR
mcp tool google-calendar.create_event \
  --calendar leadership@company.com \
  --summary "QBR" \
  --start "2027-01-08T09:00:00" --end "2027-01-08T10:00:00" \
  --recurrence "RRULE:FREQ=QUARTERLY;COUNT=4"

# Annual offsite
mcp tool google-calendar.create_event \
  --calendar leadership@company.com \
  --summary "Annual Planning Offsite — FY28" \
  --start "2027-12-15T09:00:00" --end "2027-12-16T18:00:00"

# Board meetings (8-week cadence)
mcp tool google-calendar.create_event \
  --calendar leadership@company.com \
  --summary "Board Meeting" \
  --start "2027-02-04T09:00:00" --end "2027-02-04T11:30:00" \
  --recurrence "RRULE:FREQ=WEEKLY;INTERVAL=8;COUNT=7"
```

### Recipe 3: David Sacks framework — focus per cadence

```markdown
| Cadence | Focus | What's decided |
|---|---|---|
| Weekly | Metrics + unblock + tactical decisions | This-week DRIs, escalations |
| Monthly | Roadmap + forecast variances + hiring | Pipeline reset, headcount commits |
| Quarterly | OKR set + strategy refresh + QBR | KRs, top initiatives |
| Annual | Strategy + capital + hiring plan + risk register | YES/NO, next round, kill criteria |

Rule: don't push weekly decisions to monthly. Don't push monthly decisions to quarterly.
```

### Recipe 4: Weekly metrics review template (60 min)

```markdown
## Agenda (60 min)

| Time | Topic | Owner |
|---|---|---|
| 0-5 | Last week actions check (who did what they said) | All leads |
| 5-20 | Metrics walk (north star + 4 KPIs) | CEO |
| 20-35 | Exception report (red items + recovery) | DRIs |
| 35-50 | Decisions this week (DACI items) | CEO |
| 50-60 | Asks + unblock | All leads |

Pre-read: Sunday EOD. KPI dashboard URL pinned in #leadership.
```

### Recipe 5: Monthly variance review template (90 min)

```markdown
## Agenda (90 min)

| Time | Topic | Owner |
|---|---|---|
| 0-30 | Roadmap review (top 5 initiatives status) | PMs |
| 30-60 | Forecast + budget variances (actual vs plan) | CFO |
| 60-75 | Hiring plan progress (vs FY plan) | CEO + Ops |
| 75-90 | Decisions: re-allocate / re-prioritize? | CEO |

Pre-read: 48h ahead. Variance table required.
```

### Recipe 6: Initiative tracking in Linear

```bash
# Top 5-7 initiatives per quarter
mcp tool linear.create_project \
  --team "EXEC" \
  --name "Q2 2027 — Activation v2" \
  --description "DRI: PM Sara. KR: D7 11% → 25%. Kill criteria: D7 <18% by EOQ.
Sponsoring OKR: [Mooncamp link]" \
  --target-date "2027-06-30"
```

### Recipe 7: Cadence-driven document templates

```markdown
## What gets written when

| Frequency | Document | Skill pack |
|---|---|---|
| Weekly | Pre-read for metrics review | `weekly-monthly-all-hands-prep` |
| Weekly | Investor update KPI ping (Series B+) | `investor-update-monthly-quarterly-visible` |
| Monthly | Investor update | `investor-update-monthly-quarterly-visible` |
| Monthly | Variance memo | `concise-planning` default skill |
| Monthly | All-hands deck | `weekly-monthly-all-hands-prep` |
| Quarterly | QBR deck + pre-read | `qbr-quarterly-business-review` |
| Quarterly | Board pack + pre-read | `board-meeting-prep-deck-minutes` |
| Annual | Strategy doc | `vision-strategy-doc-rumelt-ogsm-v2mom` |
| Annual | Annual plan (8-section) | `annual-planning-cycle-cadence` |
```

### Recipe 8: Cadence calendar — communicate to org

```bash
# Publish to whole company so they know when decisions happen
mcp tool slack.send --channel "#general" --message "*Operating Rhythm 2027*
Our cadence is locked. See full doc: [Notion link]

Quick reference:
- Mon 9am: Weekly metrics review (decisions land here)
- 1st Thu: Monthly all-hands
- Last Thu: Monthly variance review
- Quarterly first week: QBR + OKR setting
- 8-weekly: Board meetings

Where to surface input:
- Tactical issue → bring to next weekly metrics review
- Forecast issue → bring to monthly variance review
- Strategic / OKR issue → bring to quarterly QBR
- Big bet → bring to annual planning
"
```

### Recipe 9: Skip-level cadence (quarterly per skip)

```bash
# 1-2 skip-level 1:1s per quarter per direct report's team
mcp tool google-calendar.create_event \
  --calendar primary \
  --summary "Skip-level — CEO + <name>" \
  --start "2027-02-15T15:00:00" \
  --recurrence "RRULE:FREQ=QUARTERLY;COUNT=4"
```

### Recipe 10: Cadence health check (annual)

```markdown
## Cadence health check (do at annual planning)

- [ ] Are we using weekly metrics review for tactical decisions? (yes = working; no = drifting to status)
- [ ] Are monthly variance reviews changing forecasts? (yes = working; no = ceremonial)
- [ ] Do QBRs actually make decisions? (60% time on decisions; not status)
- [ ] Is annual plan still the operating plan or has it become decorative?
- [ ] Are we maintaining 1:1 cadence? (skipped 1:1s = signal)
- [ ] Is the board pack standard or do we redo each time? (standard = mature)
- [ ] Do new hires understand the cadence by end of Week 1?

If 4+ are "no" → cadence needs refresh. Run at annual planning.
```

### Recipe 11: Initiative status pull (for monthly)

```python
import requests, os
H = {"Authorization": os.environ["LINEAR_API_KEY"]}
query = '''
query {
  projects(filter: {state: {type: {in: ["started"]}}}) {
    nodes {
      id name description state {name} progress
      lead {name} targetDate
      issues { nodes {id title state {name}} }
    }
  }
}
'''
data = requests.post("https://api.linear.app/graphql", headers=H, json={"query":query}).json()
for p in data["data"]["projects"]["nodes"]:
    print(f"\n## {p['name']} (DRI: {p['lead']['name']})")
    print(f"Progress: {p['progress']*100:.0f}% — Target: {p['targetDate']}")
    open_issues = [i for i in p['issues']['nodes'] if i['state']['name'] != 'Done']
    print(f"Open: {len(open_issues)} / {len(p['issues']['nodes'])}")
```

### Recipe 12: Sample week — CEO calendar

```markdown
## A typical CEO week (Series A SaaS)

| Day | AM | PM |
|---|---|---|
| Mon | Weekly metrics review (9-10) + strategy block (10-12) | Customer call + investor catch-up |
| Tue | 1:1 VP Eng (9-9:45) + product review (10-12) | Strategy block (1-4) |
| Wed | All-hands (10-10:30) + customer call (11-12) | 1:1 CFO (1-1:45) + recruiting (3-5) |
| Thu | 1:1 VP Sales + VP Product (9-11) | Board prep (1-3) or board meeting (1-3) |
| Fri | NO MEETINGS (deep work) | Sometimes 1:1 carry-over (4-5) |

Targets:
- 60 min/day max meeting in AM
- 4+ hours deep work weekly
- 1 no-meeting day defended
```

## Examples

### Example 1: New CEO sets up first cadence

**Goal:** Founder-CEO hits 30 employees; needs operating rhythm.

**Steps:**
1. Write rhythm doc (Recipe 1).
2. Calendar lock all recurrings (Recipe 2).
3. Publish to org (Recipe 8).
4. Set up initiative tracking (Recipe 6).
5. Run first weekly review (Recipe 4).
6. Iterate after 4 weeks based on what's working.

**Result:** Company knows when decisions happen; CEO not constantly improvising calendar.

### Example 2: Annual cadence refresh

**Goal:** After Q4 offsite, relock cadence for next year.

**Steps:**
1. Run cadence health check (Recipe 10).
2. Update rhythm doc (Recipe 1) — incorporate learnings.
3. Refresh calendar locks (Recipe 2).
4. Publish refreshed doc (Recipe 8).

**Result:** Cadence matched to current org reality.

## Edge cases / gotchas

- **Cadence skipped = signal.** Skipping weekly metrics review tells the team it doesn't matter. Don't skip.
- **Pre-reads non-negotiable.** Without pre-reads, meetings become status updates.
- **Weekly review = decisions.** If status dominates, you're not running the meeting; the meeting is running you.
- **Monthly variance = action.** Variance memo without "what we're changing" = ceremony.
- **Cap initiatives.** 5-7 top initiatives in Linear at any time. More = unclear focus.
- **Cadence drift after 6 months.** Reset at annual planning + mid-year health check.
- **New hires learn cadence in Week 1.** Document in onboarding so they know where decisions get made.
- **Don't conflate weekly + monthly + quarterly.** Each has a purpose. Mixing = neither works.
- **Calendar lock for the leadership team.** Don't reschedule based on one person's conflict. Defended.
- **1:1 cadence sacred.** 45 min weekly per direct report. Skipping = "not a priority."
- **Annual cadence health check is the work.** Most teams skip this; it's how you avoid drift.
- **Cadence reflects values.** Time is the only finite resource — what we cadence is what we believe.

## Sources

- [David Sacks operating cadence](https://www.capitaly.vc/blog/david-sacks-operating-cadence-weekly-metrics-okrs-ceo-dashboard)
- [HashiCorp — How we work (operating cadence)](https://www.hashicorp.com/en/how-hashicorp-works/articles/operating-cadence)
- [High Output Management — Andy Grove](https://www.amazon.com/High-Output-Management-Andrew-Grove/dp/0679762884)
- [Notion operating rhythm template](https://www.notion.so/templates/operating-rhythm)
- [Lenny Rachitsky — weekly updates](https://www.lennysnewsletter.com/p/how-to-write-a-great-weekly-update)
