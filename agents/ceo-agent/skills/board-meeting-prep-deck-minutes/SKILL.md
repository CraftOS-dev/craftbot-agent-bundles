<!--
Source: https://www.imboard.ai/blog/alternatives-to-diligent-boards
Board meeting prep: Sequoia/NVCA-style 12-slide template + AI minutes + action sync
-->
# Board Meeting Prep — Deck, Pre-read, Minutes, Actions

The Sequoia/NVCA-style 12-slide template + AI notetaker minutes + Linear action sync. Generates board deck (`pptx`) + pre-read memo (Notion) + distributes (`gmail-mcp` + Google Drive), captures minutes via Granola/Fathom, and pushes action items to Linear with DRIs. Board portal upload (I'mBoard / Boardable / OnBoard) is manual on startup-tier plans — agent emails the PDF instead.

## When to use

- Preparing for an upcoming board meeting (8-week cadence typical Series A+).
- Capturing minutes + actions from a board meeting that just happened.
- Onboarding a new independent director (needs prior board pack + charter).
- Refresh of the standing board template (annual).

Trigger phrases: "prep board meeting", "board pack", "board pre-read", "board minutes", "board action items", "independent director onboarding".

**Note on portals (2026):** BoardEffect was acquired by Diligent and merged with OnBoard. Startup-friendly: I'mBoard ($30/seat — AI prep), Boardable ($79-329/mo). Enterprise: Diligent ($15-30k/yr). Most have no public API on startup tiers — PDF + email is the working fallback.

## Setup

```bash
# Granola / Fathom / Fireflies — pick one as board default
# Granola (bot-free macOS): https://granola.ai
# Fathom (free unlimited): https://fathom.video
# Fireflies (multilingual): https://fireflies.ai

# pptx skill (CraftBot built-in)
pip show python-pptx

# Linear MCP for action items
mcp tool linear.search --query "Board action"
```

Auth / API key requirements:
- `GRANOLA_API_KEY` — for transcript export (Granola Pro tier).
- `FATHOM_API_KEY` — free tier export.
- `LINEAR_API_KEY` — required scope `issues:create`.
- `NOTION_API_KEY` — for pre-read + minutes docs.

## Common recipes

### Recipe 1: Generate the 12-slide deck (Sequoia/NVCA-style)

```python
# Use CraftBot pptx skill
from pptx import Presentation
prs = Presentation()
sections = [
    "Cover — Company / Date / Period",
    "Mission + this-period TL;DR (3 bullets)",
    "KPIs — North star + 4-5 supporting (trend lines)",
    "Financials — Revenue / Gross margin / Burn / Runway",
    "Cash + capital plan — runway months, next round timing",
    "Hiring — Headcount / plan / key opens / departures",
    "Wins — 3-5 since last meeting",
    "Lowlights — 2-3 honest items",
    "Strategy update — what changed, what's the gameplay",
    "Asks — specific, named (intros / hires / advice / capital)",
    "Risks + mitigations — top 3-5",
    "Appendix — detail tables, methodology",
]
for title in sections:
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = title
prs.save("board-pack-2027-Q2.pptx")
```

### Recipe 2: Pre-read memo in Notion (3-5 pages)

```bash
mcp tool notion.create_page \
  --parent '{"page_id":"<board-hub>"}' \
  --properties '{"title":[{"text":{"content":"Board Pre-read — Q2 2027"}}]}' \
  --children-markdown './board-preread-template.md'
```

Template structure:
```markdown
## TL;DR (1 paragraph)
[Where we are, what changed, what we're deciding.]

## Where we are
[2-3 paragraphs — narrative not bullets.]

## What changed since last meeting
[Material shifts; tied to specifics.]

## What we're deciding this meeting
1. [Decision 1 with DACI link]
2. [Decision 2]

## Asks
- Specific intros: [name, why]
- Advice on: [topic]
- Other: [...]
```

Distribute 48-72h ahead with note: *"Please read before — we'll spend the meeting on decisions, not slides."*

### Recipe 3: Distribute the board pack

```bash
# Email + Drive folder
mcp tool google-drive.create_folder \
  --parent "<board-folder-id>" \
  --name "Board — 2027 Q2"

mcp tool google-drive.upload --folder "<board-folder-id>" --file "./board-pack-2027-Q2.pptx"

mcp tool gmail.send \
  --to "board@company.com" \
  --subject "Board pre-read — Q2 2027 (read 48h ahead please)" \
  --body "Pre-read: [Notion link]. Deck: [Drive link]. Meeting Thursday 9am PT.
Decisions on the docket:
1. Series B timing
2. VP Eng search format
3. ICP focus

Please add questions in the pre-read comments by Wed 5pm."
```

### Recipe 4: Wire up Granola/Fathom for the meeting

```bash
# Granola — captures macOS meeting audio with no bot
# Fathom — joins as bot (cheaper, board may prefer in-room mic)
# Set as default board notetaker once chosen
mcp tool granola.set_default --calendar-event "<board-meeting-event-id>"
```

### Recipe 5: Pull transcript post-meeting + extract decisions/actions

```bash
TRANSCRIPT=$(mcp tool fathom.export_transcript --meeting-id "$MEETING_ID" --format markdown)

mcp tool notion.create_page \
  --parent '{"page_id":"<board-hub>"}' \
  --properties '{"title":[{"text":{"content":"Board Minutes — 2027 Q2"}}]}' \
  --children-markdown "## Transcript

$TRANSCRIPT

## Decisions
- [extracted automatically — review before publish]

## Action items
- [extracted automatically — assigned in Linear]"
```

### Recipe 6: Auto-extract action items → Linear

```python
import re, os, requests
# Heuristic: lines starting with "AI:" / "Action:" / "TODO:" in transcript
actions = re.findall(r"(?:AI|Action|TODO):\s*(.+?)(?:\n|$)", transcript)
H = {"Authorization": f"Bearer {os.environ['LINEAR_API_KEY']}"}
for action in actions:
    requests.post("https://api.linear.app/graphql", headers=H, json={
        "query": "mutation { issueCreate(input: { teamId: \"BOARD\", title: \"%s\", labels: [\"board-action\"], dueDate: \"2027-04-01\" }) { issue { id url } } }" % action
    })
```

### Recipe 7: Publish minutes within 48h

```bash
mcp tool notion.update_page --page-id "<minutes-page>" \
  --properties '{"Status":{"select":{"name":"Final"}}}'

mcp tool gmail.send \
  --to "board@company.com" \
  --subject "Board minutes — 2027 Q2 — final" \
  --body "Minutes: [Notion link]. Action items in Linear ([link]). Next meeting: [date]."
```

### Recipe 8: Board portal upload (manual fallback)

```bash
# I'mBoard / Boardable / OnBoard — no public API on startup tier
# Convert pptx → pdf and prompt CEO to upload manually
mcp tool file-format.convert --in "./board-pack-2027-Q2.pptx" --out "./board-pack-2027-Q2.pdf"

echo "ACTION: Upload ./board-pack-2027-Q2.pdf + Notion minutes export to I'mBoard portal manually (30 sec)."
```

### Recipe 9: Onboard a new independent director

```bash
mcp tool google-drive.create_folder --parent "<board-folder>" --name "Director onboarding — <name>"

mcp tool google-drive.share \
  --folder "<onboarding-folder>" \
  --email "<new-director-email>" \
  --role reader

# Populate with: charter, last 4 board packs, cap table, strategy doc, KPI dashboard URL
```

### Recipe 10: Board calendar setup (8-week cadence)

```bash
mcp tool google-calendar.create_event \
  --calendar-id board@company.com \
  --summary "Board meeting — Q2 2027" \
  --start "2027-05-01T09:00:00" \
  --end "2027-05-01T11:30:00" \
  --recurrence "RRULE:FREQ=WEEKLY;INTERVAL=8;COUNT=8" \
  --description "Pre-read 72h ahead. Decisions list at top. 30-min closed session at end."
```

### Recipe 11: Pre-meeting decision tracker

```bash
mcp tool notion.create_database \
  --parent '{"page_id":"<board-hub>"}' \
  --title '[{"text":{"content":"Board Decision Log"}}]' \
  --properties '{
    "Decision":{"title":{}},
    "Meeting":{"select":{"options":[{"name":"Q1 2027"},{"name":"Q2 2027"}]}},
    "Status":{"select":{"options":[{"name":"Pending"},{"name":"Decided"},{"name":"Deferred"}]}},
    "Outcome":{"rich_text":{}},
    "Owner":{"people":{}},
    "Review date":{"date":{}}
  }'
```

### Recipe 12: Independent director sourcing checklist

```markdown
- Bolster (bolster.com) — fractional + interim + independent
- The Board List (theboardlist.com) — women + diverse independent directors
- True Search — retained for senior independents
- Personal networks — LP intros, advisor → director conversion

Process:
1. Define independent director scorecard (Geoff Smart outcomes-first)
2. Source 10-15 candidates
3. CEO + board chair intro calls (30 min)
4. 360 references (3 peers + 2 reports)
5. Board interview (60 min)
6. Offer with equity grant + D&O insurance
```

## Examples

### Example 1: Full board prep cycle (T-2 weeks → T+2 days)

**Goal:** Quarterly board meeting prep end-to-end.

**Steps:**
1. **T-14 days:** Pull KPIs from `stripe-mcp` + `posthog-mcp` + `xero-mcp`. Update Visible KPI sheet.
2. **T-10 days:** Draft pre-read in Notion (Recipe 2). Review with CFO.
3. **T-7 days:** Generate deck (Recipe 1). Iterate with team leads on lowlights.
4. **T-3 days:** Distribute (Recipe 3). Set Granola as notetaker (Recipe 4).
5. **T-0:** Board meeting. Use deck as talking points, not script.
6. **T+1 day:** Pull transcript (Recipe 5). Extract decisions + actions (Recipe 6).
7. **T+2 days:** Publish minutes (Recipe 7). Linear actions assigned with DRIs.

**Result:** Board members read pre-read, meeting on decisions, minutes within 48h.

### Example 2: New independent director onboarding

**Goal:** Bring a new board director up to speed in 2 weeks.

**Steps:**
1. Create onboarding folder (Recipe 9).
2. Add: last 4 board packs, strategy doc, cap table, charter, KPI dashboard URL.
3. Schedule three 1:1s: CEO, board chair, CFO.
4. Send Q&A doc 3 days before first board meeting.

**Result:** Director shows up to first meeting fluent in the company.

## Edge cases / gotchas

- **Pre-read late = meeting becomes status update.** If you can't send 48h ahead, defer the meeting. Decisions need pre-read time.
- **Lowlights mandatory.** Skipping lowlights signals dishonesty. Board values candor over polish.
- **DACI on every decision.** Each decision in pre-read should have Driver / Approver / Contributors / Informed.
- **Two Approvers = no decision.** Force single Approver per decision before the meeting.
- **Asks must be specific.** "Need intros to enterprise buyers" is fluff. "Need intros to CIOs at 3 healthcare $1B+ orgs by May 15" is an ask.
- **Granola is macOS-only.** On Windows board director laptops, fall back to Fathom or Fireflies.
- **Closed session is non-negotiable.** Last 30 min of every board meeting is investor-directors only (no founder). Used for sensitive feedback.
- **No public API on startup-tier portals.** I'mBoard / Boardable / OnBoard upload is manual. Build the workflow assuming PDF + email is primary.
- **NVCA model docs change.** Refresh charter annually against NVCA latest version (nvca.org).
- **Action items without DRIs decay.** Single owner per action in Linear. Multi-owner = no owner.
- **Director D&O insurance non-optional.** Source via Embroker / Founder Shield before first meeting. CEO often forgets this.

## Sources

- [I'mBoard — 2026 board portal alternatives](https://www.imboard.ai/blog/alternatives-to-diligent-boards)
- [Board portal software comparison 2026](https://appdeck.com/blog/board-portal-software-comparison-2026)
- [Granola vs Fireflies vs Fathom vs Otter](https://www.granola.ai/blog/meeting-note-tool-pricing-granola-vs-fireflies-fathom-otter)
- [NVCA Model Legal Documents](https://nvca.org/model-legal-documents/)
- [Sequoia pitch + board templates](https://www.sequoiacap.com/article/writing-a-business-plan/)
