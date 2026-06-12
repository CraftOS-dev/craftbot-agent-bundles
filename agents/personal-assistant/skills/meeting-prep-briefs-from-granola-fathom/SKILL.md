<!--
Source: https://granola.ai/ + https://docs.fathom.video/api/ + https://docs.fireflies.ai/api
-->
# Meeting Prep Briefs — Granola / Fathom / Fireflies / tl;dv — SKILL

Pull prior meeting transcripts, extract action items + open threads + commitments, compose a one-page brief, and deliver 15-30 min before the next session. Granola owns mind-share 2026 for AI native notes; Fathom is free + Zoom-native; Fireflies has multi-platform recorder + searchable knowledge graph; tl;dv is multilingual + free; Otter.ai legacy.

## When to use this skill

- **"Prep me for my 1:1 with X"** — most common trigger.
- **"What did we discuss last time with X?"** — transcript retrieval + summary.
- **"What did I commit to?"** — action item extraction across recent meetings.
- **Pre-board meeting / pre-pitch prep** — one-page brief on attendees + history.
- **Weekly review of all 1:1s** — Sunday-night planning.

**Do NOT use this skill when:**
- Composing follow-up emails after the meeting — see `follow-up-email-drafting`.
- Just scheduling a 1:1 — see `scheduling-calendly-cal-com-oncehub`.
- Recording the meeting itself — Granola / Fathom / Fireflies handle recording, agent only consumes transcripts.

## Pick the right transcript source

| User's tool | Pull mechanism |
|---|---|
| **Granola** | No public API yet; export-to-Notion / Slack integration → `notion-mcp` |
| **Fathom** | REST API: https://docs.fathom.video/api/ |
| **Fireflies** | GraphQL: https://docs.fireflies.ai/api |
| **tl;dv** | REST API: https://docs.tldv.io/ |
| **Otter.ai** | Limited API (subscription-tier); web-export fallback |
| **Zoom AI Companion** | Per-meeting export via Zoom REST |

## Setup

### Fathom

```bash
# Get API key: https://fathom.video/users/api
export FATHOM_API_KEY="<key>"

# Smoke
curl -s 'https://api.fathom.video/v1/meetings?limit=5' \
  -H "X-API-Key: $FATHOM_API_KEY"
```

Docs: https://docs.fathom.video/api/

### Fireflies (GraphQL)

```bash
# Get API key: https://app.fireflies.ai/integrations/custom/fireflies
export FIREFLIES_API_KEY="<key>"

curl -X POST https://api.fireflies.ai/graphql \
  -H "Authorization: Bearer $FIREFLIES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ user { name email } }"}'
```

Docs: https://docs.fireflies.ai/api

### tl;dv

```bash
export TLDV_API_KEY="<key>"
curl -s 'https://pasta.tldv.io/v1/meetings' \
  -H "Authorization: $TLDV_API_KEY"
```

Docs: https://docs.tldv.io/

### Granola

No public API as of Jun 2026. Use:
- Granola → Notion sync (Granola Settings → Integrations → Notion).
- Pull from Notion DB via `notion-mcp`.

## Common recipes

### Recipe 1: Fathom — list recent meetings by attendee

```bash
curl -s "https://api.fathom.video/v1/meetings?attendee=alex@company.com&limit=10" \
  -H "X-API-Key: $FATHOM_API_KEY" \
  | jq '.meetings[] | {id, title, date, duration}'
```

### Recipe 2: Fathom — pull a meeting transcript + summary

```bash
MEETING_ID="<meeting-id>"
curl -s "https://api.fathom.video/v1/meetings/$MEETING_ID" \
  -H "X-API-Key: $FATHOM_API_KEY" \
  | jq '{title, summary, action_items, transcript}'
```

### Recipe 3: Fathom — search across transcripts

```bash
curl -s "https://api.fathom.video/v1/search?q=Q3%20strategy" \
  -H "X-API-Key: $FATHOM_API_KEY"
```

### Recipe 4: Fireflies GraphQL — recent meetings with action items

```bash
curl -X POST https://api.fireflies.ai/graphql \
  -H "Authorization: Bearer $FIREFLIES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query($limit: Int) { transcripts(limit: $limit) { id title date attendees { email } summary { action_items overview } } }",
    "variables": {"limit": 10}
  }'
```

### Recipe 5: Fireflies — search by participant

```bash
curl -X POST https://api.fireflies.ai/graphql \
  -H "Authorization: Bearer $FIREFLIES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query($email: String!) { transcripts(participants: [$email], limit: 5) { id title date summary { action_items } } }",
    "variables": {"email":"alex@company.com"}
  }'
```

### Recipe 6: tl;dv — list + extract

```bash
curl -s "https://pasta.tldv.io/v1/meetings?limit=10" \
  -H "Authorization: $TLDV_API_KEY" | jq '.meetings[]'

# Get one
curl -s "https://pasta.tldv.io/v1/meetings/<id>/transcript" \
  -H "Authorization: $TLDV_API_KEY"
```

### Recipe 7: Granola via Notion sync

```bash
# Assuming Granola → Notion DB configured
mcp tool notion.query_database \
  --database-id <granola-notes-db-id> \
  --filter '{"property":"Attendees","contains":"alex@company.com"}' \
  --sorts '[{"property":"Date","direction":"descending"}]'
```

### Recipe 8: Compose the brief (template)

Once data pulled, format using `concise-planning` skill pattern:

```markdown
# 1:1 Brief — [Date] [Time TZ]
## Attendee: [Name, role, last interaction]

## Action items from last session ([Date])
- **They committed:** [Item] — [status / outcome]
- **We committed:** [Item] — [status / outcome]

## Open threads
- [Topic]: [status]

## Their context
- [Recent news / projects / life event — 2 lines]

## Suggested topics for this session
1. [...]
2. [...]
3. [...]

## Logistics
- Zoom: [link]
- Prep doc: [link]
```

### Recipe 9: Deliver brief 30 min before

Once brief composed, set up calendar reminder + email digest:

```bash
mcp tool google-calendar.create_event \
  --summary "PREP: 1:1 with Alex" \
  --start "2026-06-12T13:30:00-07:00" \
  --end   "2026-06-12T14:00:00-07:00" \
  --description "$(cat brief.md)" \
  --reminders '[{"method":"popup","minutes":15}]'

# OR drop into Notion + send Gmail digest 30min before
mcp tool gmail.draft \
  --to "<user-email>" \
  --subject "Brief: 1:1 with Alex @ 2pm PT" \
  --body "$(cat brief.md)"
```

### Recipe 10: Extract action items across all recent meetings

```python
import requests, os
r = requests.get("https://api.fathom.video/v1/meetings?limit=20",
                 headers={"X-API-Key": os.environ["FATHOM_API_KEY"]})
all_actions = []
for m in r.json().get('meetings', []):
    detail = requests.get(f"https://api.fathom.video/v1/meetings/{m['id']}",
                          headers={"X-API-Key": os.environ["FATHOM_API_KEY"]}).json()
    for ai in detail.get('action_items', []):
        all_actions.append({
            "meeting": m['title'], "date": m['date'],
            "owner": ai.get('owner'), "task": ai.get('text'), "due": ai.get('due')
        })

mine = [a for a in all_actions if a['owner'] == 'me@company.com']
print(f"My open commitments: {len(mine)}")
```

### Recipe 11: Cross-link action items into Todoist

```python
for a in mine:
    requests.post("https://api.todoist.com/rest/v2/tasks",
        headers={"Authorization": f"Bearer {os.environ['TODOIST_TOKEN']}"},
        json={"content": a['task'], "due_string": a['due'],
              "description": f"From meeting: {a['meeting']} on {a['date']}"})
```

### Recipe 12: Person-context refresh

For each upcoming meeting attendee, run mini-research:

```bash
# Their company news
mcp tool brave-search.search \
  --query "site:linkedin.com Alex Johnson Acme"

# Their recent activity
mcp tool tavily-search.search \
  --query "\"Alex Johnson\" Acme Corp"
```

Append 2-line summary to brief.

## Examples

### Example 1: Standard 1:1 prep — 5 min before

**Goal:** Brief for 2pm 1:1 with Alex; meeting at 2pm; trigger at 1:30pm.

**Steps:**
1. Recipe 1: pull Fathom meetings with Alex → most recent = "2026-06-05 1:1 with Alex".
2. Recipe 2: pull transcript + summary + action_items.
3. Recipe 8: format into brief.
4. Recipe 12: 1-line LinkedIn context refresh.
5. Recipe 9: drop into Gmail draft → user receives at 1:30pm.

**Result:** Brief in inbox 30min before; user walks in prepared.

### Example 2: Weekly review of all 1:1s

**Goal:** Sunday 8pm; review all action items from this week's meetings.

**Steps:**
1. Recipe 10: cross-meeting action item pull (last 7 days).
2. Filter to user's own commitments.
3. Recipe 11: push open items to Todoist.
4. Email summary: "12 commitments closed; 5 open going into next week."

**Result:** Action-item integrity check + task hygiene.

### Example 3: Board meeting prep

**Goal:** Quarterly board meeting; want brief on each board member's positions from last session.

**Steps:**
1. Recipe 5 (Fireflies) — pull last board meeting transcript.
2. Per board member, extract what they said + asked + committed.
3. Recipe 8: per-attendee mini-brief.
4. Bundle into `notion-mcp` page; share with chair before meeting.

**Result:** Board chair has per-member context entering Q3 meeting.

## Edge cases / gotchas

- **Granola has no public API yet**: Recommend Granola → Notion sync as workaround. Do NOT promise direct Granola integration. Source: https://granola.ai/
- **Fathom free tier**: Unlimited recordings, AI summaries on Pro ($24/mo). API access requires Pro. Source: https://fathom.video/pricing
- **Fireflies GraphQL pagination**: `limit` cap at 100; for full pull use cursor-based pagination.
- **Fireflies AI Apps**: Fireflies has built-in "AI Apps" (templates) — agent can call those for pre-formatted briefs.
- **Otter.ai API gating**: Limited to Otter Business + Enterprise. Otter for Teams = no API.
- **Transcript accuracy**: All tools struggle with technical jargon, accents, cross-talk. Pre-clarify with user if transcript-extracted action items look off.
- **PII in transcripts**: Customer / candidate names, financial details, etc. Treat as sensitive — don't archive to public Notion / Slack.
- **Attendee email mismatch**: User's company email vs personal email; same person may have different identifiers across meetings. Normalize before search.
- **Action item ownership**: "We need to follow up" — who's "we"? Sometimes ambiguous; surface uncertain ones for user review.
- **Recurring 1:1 amalgam**: If user has weekly 1:1 with Alex × 6 weeks, pull last 3 to capture multi-meeting context, not just last 1.
- **Granola → Notion sync delay**: ~5-15 min after meeting ends. If meeting just finished, transcript may not be in Notion yet.
- **Zoom AI Companion vs Fathom**: If user runs both, dedup before extract; Fathom typically wins on quality.
- **TZ in meeting date**: Always confirm meeting TZ vs user TZ vs attendee TZ before scheduling next session.

## Sources

- [Granola](https://granola.ai/)
- [Fathom API](https://docs.fathom.video/api/)
- [Fireflies API](https://docs.fireflies.ai/api)
- [tl;dv API](https://docs.tldv.io/)
- [Otter.ai for Business](https://otter.ai/business)
- [Zoom AI Companion REST](https://developers.zoom.us/docs/api/rest/reference/ai/companion/)
