<!--
Source: https://www.lennysnewsletter.com/p/how-to-write-a-great-weekly-update
All-hands prep: weekly + monthly format, Gamma deck, distribution
-->
# All-Hands Prep — Weekly + Monthly

Lenny Rachitsky weekly-update format (Wins / Lowlights / Asks / Plans / Metrics) for content; Gamma Generate API for decks (Tome dead since March 2025 — Beautiful.ai backup for PPT-compat); Zoom for hosting; transcript pull post-meeting. Cadence: weekly 30-min, monthly 60-min, same day same time every week. Pre-read 24h ahead; recap with Loom/Tella for absentees.

## When to use

- Weekly 30-min all-hands.
- Monthly 60-min all-hands with theme.
- Quarterly all-hands (after QBR).
- Annual kickoff / mid-year refresh.

Trigger phrases: "all-hands prep", "weekly all-hands", "monthly all-hands", "company update", "pre-read", "all-hands deck".

## Setup

```bash
# Gamma Generate API
curl -fsSL "https://api.gamma.app/v1/me" \
  -H "Authorization: Bearer $GAMMA_API_KEY"

# Beautiful.ai (PPT-compat fallback)
curl -fsSL "https://api.beautiful.ai/v1/me" \
  -H "Authorization: Bearer $BEAUTIFUL_API_KEY"

# Zoom for hosting
mcp tool zoom.list_meetings --user me
```

Auth / API key requirements:
- `GAMMA_API_KEY` — Gamma Settings → API Access (paid Plus tier).
- `BEAUTIFUL_API_KEY` — Beautiful.ai team tier.
- `ZOOM_API_KEY` — Zoom Marketplace OAuth app.
- `NOTION_API_KEY` — for pre-read.

## Common recipes

### Recipe 1: Weekly all-hands pre-read (Notion, 24h ahead)

```bash
mcp tool notion.create_page \
  --parent '{"page_id":"<all-hands-db>"}' \
  --properties '{
    "Title":[{"text":{"content":"All-hands — Apr 8, 2027"}}],
    "Date":{"date":{"start":"2027-04-08"}},
    "Type":{"select":{"name":"Weekly"}}
  }' \
  --children-markdown '# All-Hands — Apr 8, 2027

## TL;DR
Strong week. MRR $54k (+4% WoW). VP Eng started Mon. Activation v2 ships Wed.

## Wins (3-5)
- VP Eng (Jordan) started Monday — meet at all-hands
- 3 enterprise pilots closed (Acme, Beta, Gamma — $90k ARR)
- Activation v2 ships Wed; A/B test live by Fri
- Customer NPS 54 (+2 WoW)
- D7 retention 21% (+3pp from last week)

## Lowlights (2-3)
- Sales pipeline coverage 2.4x (target 3x) — SDR offer out Tue
- 1 customer ($12k ARR) churned to in-house build — post-mortem Thu

## Asks
- Engineering: 2 volunteers for activation v2 office hours Mon-Wed
- Sales: introductions to fintech CIOs (3 needed by EOM)
- All: customer story submissions for monthly all-hands

## Plans (next 7 days)
- Activation v2 ship + monitor
- VP Eng onboarding plan execution
- Series B banker selection finalize

## Metrics (1 chart)
[D7 retention trend chart link]
'
```

### Recipe 2: Generate the weekly deck (Gamma, 5-8 slides)

```bash
curl -X POST "https://api.gamma.app/v1/generate" \
  -H "Authorization: Bearer $GAMMA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input_text":"All-hands — Apr 8, 2027. Topics: Welcome (1), Wins (1), Lowlights (1), Activation v2 update (1), Customer story (1), Asks (1), Q&A (1).",
    "format":"presentation",
    "theme":"professional",
    "num_cards":8
  }' \
  | jq -r '.url'
```

Gamma's Agent API auto-generates layout + visuals. Pull URL for the deck.

### Recipe 3: Beautiful.ai PPT-export variant

```bash
# When you need PPT for distribution to board / external
curl -X POST "https://api.beautiful.ai/v1/presentations" \
  -H "Authorization: Bearer $BEAUTIFUL_API_KEY" \
  -d '{
    "title":"All-hands April 8, 2027",
    "template":"corporate",
    "slides":[
      {"title":"Welcome","content":"Welcome Jordan — new VP Eng"},
      {"title":"Wins","content":"MRR $54k +4%, 3 enterprise pilots, D7 21%"}
    ]
  }'
```

### Recipe 4: Schedule the Zoom + send invite

```bash
mcp tool zoom.create_meeting \
  --topic "All-hands — Apr 8, 2027" \
  --start "2027-04-08T10:00:00" \
  --duration 30 \
  --recurrence '{"type":1,"repeat_interval":1,"weekly_days":"3"}' \
  --settings '{"auto_recording":"cloud","mute_upon_entry":true,"meeting_authentication":true}'
```

### Recipe 5: Send pre-read 24h ahead

```bash
mcp tool slack.send \
  --channel "#all-hands" \
  --message ":calendar: *All-hands tomorrow 10am PT*
Pre-read: [Notion link]
Deck: [Gamma link]
Zoom: [link]

Read the pre-read before. We'll spend the live time on Q&A + connection — not status."

mcp tool gmail.send \
  --to "everyone@company.com" \
  --subject "All-hands tomorrow 10am — pre-read inside" \
  --body "Read this before tomorrow: [Notion link]"
```

### Recipe 6: Live agenda — Lenny format (30 min)

```markdown
## Weekly all-hands — 30 min agenda

| Time | Topic |
|---|---|
| 0-3 | Welcome + new hires + shoutouts |
| 3-13 | Metrics walk-through (limit to 3-5 KPIs, no charts >2) |
| 13-23 | Wins + lowlights (5 min each, lowlights are honest) |
| 23-30 | Q&A — open floor, CEO + leadership respond |

NOT in live time:
- Status updates (those are in pre-read)
- Long product demos (separate forum)
- Strategic announcements (separate slide-up with DACI)
```

### Recipe 7: Monthly format (60 min, theme-led)

```markdown
## Monthly all-hands — 60 min agenda

| Time | Topic | Owner |
|---|---|---|
| 0-5 | Welcome + new hires (round-robin intros) | CEO |
| 5-20 | Theme presentation (strategy update / customer story / launch) | DRI |
| 20-30 | Metrics review (more depth than weekly) | CEO |
| 30-45 | Functional updates (1 leader per function, 3 min each) | Leaders |
| 45-60 | Q&A | CEO + leaders |
```

### Recipe 8: Post-meeting recap (4h SLA)

```bash
# Pull Zoom transcript
TRANSCRIPT_URL=$(mcp tool zoom.get_recording --meeting-id "$ZOOM_MEETING_ID" | jq -r '.recording_files[] | select(.file_type=="TRANSCRIPT") | .download_url')

curl -s "$TRANSCRIPT_URL" > all-hands-transcript-apr8.txt

# Summarize via Gemini → post to Slack
SUMMARY=$(gemini --prompt "Summarize the attached all-hands transcript in 5 bullets. Cover: top 2 wins, top 2 lowlights, 3 Q&A questions and answers. Use bullet points." --file all-hands-transcript-apr8.txt)

mcp tool slack.send --channel "#all-hands" --message "All-hands recap (Apr 8):

$SUMMARY

Full recording: [Zoom link]"
```

### Recipe 9: Loom/Tella recap for absentees

```bash
# Tella for polished branded recap
curl -X POST "https://api.tella.video/v1/videos" \
  -H "Authorization: Bearer $TELLA_API_KEY" \
  -d '{"title":"All-hands recap — Apr 8","source_url":"<zoom-recording-url>"}' \
  | jq -r '.share_url'

mcp tool slack.send --channel "#all-hands" --message "If you missed: 3-min recap by CEO [Tella link]"
```

### Recipe 10: Speaker notes generator

```bash
gemini --prompt "Given this pre-read [Notion link], generate speaker notes for a 30-min all-hands. Be tight; CEO will speak 50% of the time, leaders the other 50%. Include 2-3 wins to celebrate by name, 2 lowlights to address honestly, and 3 Q&A questions likely to come up with talking points." \
  --output ./speaker-notes-apr8.md
```

### Recipe 11: All-hands DB schema

```bash
mcp tool notion.create_database \
  --parent '{"page_id":"<exec-hub>"}' \
  --title '[{"text":{"content":"All-Hands History"}}]' \
  --properties '{
    "Title":{"title":{}},
    "Date":{"date":{}},
    "Type":{"select":{"options":[{"name":"Weekly"},{"name":"Monthly"},{"name":"Quarterly"},{"name":"Annual"}]}},
    "Pre-read":{"url":{}},
    "Deck":{"url":{}},
    "Recording":{"url":{}},
    "Attendance":{"number":{}},
    "Q&A items":{"rich_text":{}}
  }'
```

### Recipe 12: Q&A backlog (questions you didn't get to)

```bash
mcp tool notion.create_page \
  --parent '{"page_id":"<qa-backlog-db>"}' \
  --properties '{
    "Question":[{"text":{"content":"What's the plan for parental leave policy?"}}],
    "Asked":{"date":{"start":"2027-04-08"}},
    "Owner":{"people":[{"id":"<ops-lead-id>"}]},
    "Status":{"select":{"name":"Pending"}},
    "Due":{"date":{"start":"2027-04-15"}}
  }'
```

Surface backlog in next all-hands — shows you actually read every question.

## Examples

### Example 1: Weekly all-hands prep cycle

**Goal:** Run a tight 30-min weekly all-hands.

**Steps:**
1. **T-48h:** Pull metrics. Update pre-read draft (Recipe 1).
2. **T-24h:** Finalize pre-read, send to team (Recipe 5).
3. **T-12h:** Generate deck (Recipe 2). Get speaker notes (Recipe 10).
4. **T-1h:** Review wins + lowlights with leadership team in #leadership.
5. **T-0:** Run meeting (Recipe 6). Stick to time.
6. **T+4h:** Post recap (Recipe 8). Tella recap for absentees (Recipe 9).
7. **T+24h:** Address Q&A backlog (Recipe 12).

**Result:** Predictable cadence; team feels informed; CEO not overworking the cycle.

### Example 2: Monthly all-hands with launch theme

**Goal:** Activation v2 launch is the monthly theme.

**Steps:**
1. **T-2 weeks:** Decide theme. Identify DRI for theme presentation.
2. **T-1 week:** DRI drafts 10-min theme presentation.
3. **T-48h:** Pre-read covers theme + standard wins/lowlights.
4. **T-24h:** Send pre-read.
5. **T-0:** Run meeting (Recipe 7). DRI presents theme.
6. **T+4h:** Post recap + theme deck for reference.

**Result:** Monthly cadence drives feature/initiative awareness; team sees how their work matters.

## Edge cases / gotchas

- **All-hands ≠ status update.** Most common failure. Status belongs in pre-read; live time is energy + decisions + connection.
- **Pre-read late = meeting becomes status.** If you can't send 24h ahead, defer or shorten the meeting.
- **Lowlights honest = trust.** Skipping lowlights or sugar-coating signals you're hiding things. Be specific.
- **One Q&A question per leader.** Don't let the CEO answer everything; demonstrates team depth.
- **No more than 5 KPIs in metrics walk.** More than that and it's a dashboard tour, not a story.
- **New hires intro round-robin.** Don't skip. Cheap reminder that the company is growing.
- **Cadence is sacred.** Same day, same time. Skipping breaks the rhythm.
- **Recording posted same day.** Absentees catch up; remote/async teams stay aligned.
- **Tome dead.** Don't try to integrate Tome (shutdown March 2025; brand sold to AngelList). Default to Gamma; Beautiful.ai for PPT compat.
- **Gamma free tier has watermark.** Plus tier ($10/mo) removes for company-branded decks.
- **Loom alternatives matter (2026).** Loom free tier capped at 25 videos / 5 min. Tella / Vidyard / Zight / Berrycast as alternatives.
- **Don't read the deck.** Speaker notes are notes, not script. Eye contact > slide-reading.
- **Q&A backlog visible.** Public DB. Shows team you respect their questions.
- **All-hands fatigue is real.** If weekly + monthly + quarterly + annual stacks, kill the weekly to monthly cadence after Year 2. Read the room.

## Sources

- [Lenny Rachitsky — How to write a great weekly update](https://www.lennysnewsletter.com/p/how-to-write-a-great-weekly-update)
- [Best AI presentation makers 2026 (Gamma + Beautiful.ai)](https://posteverywhere.ai/blog/15-best-ai-presentation-makers)
- [Gamma API docs](https://gamma.app/docs/api)
- [Zoom developer docs](https://developers.zoom.us/)
- [Tella API docs](https://tella.video/api)
