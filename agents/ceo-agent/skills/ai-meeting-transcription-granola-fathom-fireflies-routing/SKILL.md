<!--
Source: https://www.granola.ai/blog/meeting-note-tool-pricing-granola-vs-fireflies-fathom-otter
AI meeting transcription routing: Granola / Fathom / Fireflies / Otter
-->
# AI Meeting Transcription — Routing by Meeting Type

Per-meeting-type router across the 2026 AI notetaker stack: Granola (bot-free macOS — solo founder strategy sessions); Fathom (best free unlimited — board minutes, internal meetings); Fireflies (100+ language multilingual — customer calls + CRM sync); Otter (95% accuracy general fallback); Fellow (enterprise team option). Transcripts land in a central Notion DB for searchable institutional memory.

## When to use

- Setting up notetaker defaults per meeting type.
- Pulling a specific meeting transcript for decisions / action items / minutes.
- Building a searchable institutional transcript DB.
- Switching notetaker tool after a free-tier limit hit.

Trigger phrases: "meeting notetaker", "transcript from board", "Granola export", "Fathom record", "Fireflies CRM", "central transcript".

## Setup

```bash
# Granola — bot-free macOS (no bot in meeting)
curl -fsSL "https://api.granola.ai/v1/me" \
  -H "Authorization: Bearer $GRANOLA_API_KEY"

# Fathom — best free unlimited
curl -fsSL "https://api.fathom.video/v1/me" \
  -H "Authorization: Bearer $FATHOM_API_KEY"

# Fireflies — multilingual + CRM
curl -fsSL "https://api.fireflies.ai/graphql" \
  -H "Authorization: Bearer $FIREFLIES_API_KEY" \
  -d '{"query":"{user{name}}"}'

# Otter — 95% accuracy general
curl -fsSL "https://otter.ai/forward/api/v1/profile" \
  -H "Authorization: Bearer $OTTER_API_KEY"
```

Auth / API key requirements:
- `GRANOLA_API_KEY` — Granola Settings → Integrations (Pro tier for API export, $14/mo).
- `FATHOM_API_KEY` — Fathom Settings → API (free + paid).
- `FIREFLIES_API_KEY` — Fireflies Settings → API (paid plan).
- `OTTER_API_KEY` — Otter Business → API.

## Common recipes

### Recipe 1: Meeting-type → notetaker router

```markdown
| Meeting type | Default notetaker | Why |
|---|---|---|
| Solo founder strategy session | Granola | Bot-free macOS; quiet capture |
| Board meeting | Fathom | Free unlimited; preserves retention |
| Customer call | Fireflies | CRM sync (HubSpot / SFDC) + multilingual |
| All-hands | Zoom native + Fathom | Recording + transcript both ways |
| Investor call | Fireflies | CRM contact log |
| 1:1 with direct report | Granola | Bot-free; private feel |
| QBR / planning | Fathom | Free unlimited; many participants |
| Cross-cultural / EU customers | Fireflies | 100+ languages |
| Quick internal sync | Otter | 95% accuracy fallback |
```

### Recipe 2: Set Granola as default for strategy sessions

```bash
# Granola auto-attends macOS calendar events with matching tags
mcp tool granola.update_settings \
  --auto-attend-tag "strategy" \
  --auto-attend-tag "1on1" \
  --no-bot true \
  --auto-export-notion true
```

### Recipe 3: Export Fathom transcript post-meeting

```bash
MEETING_ID="<fathom-meeting-id>"

# Pull transcript
TRANSCRIPT=$(curl -fsSL "https://api.fathom.video/v1/meetings/$MEETING_ID/transcript" \
  -H "Authorization: Bearer $FATHOM_API_KEY" \
  | jq -r '.transcript')

# Push to Notion
mcp tool notion.create_page \
  --parent '{"page_id":"<transcript-db>"}' \
  --properties '{
    "Title":[{"text":{"content":"Board meeting — Apr 8 2027"}}],
    "Date":{"date":{"start":"2027-04-08"}},
    "Type":{"select":{"name":"Board"}}
  }' \
  --children-markdown "$TRANSCRIPT"
```

### Recipe 4: Extract decisions + actions from transcript

```python
import re
# Heuristic patterns most notetakers normalize
decisions = re.findall(r"(?:Decision|DECIDED|Approver decision):\s*(.+?)(?:\n|$)", transcript)
actions = re.findall(r"(?:Action|AI|TODO|FOLLOW.UP):\s*(.+?)(?:\n|$)", transcript)

for d in decisions:
    print(f"DECISION: {d}")
for a in actions:
    print(f"ACTION: {a}")
```

### Recipe 5: Fireflies CRM sync (customer call)

```bash
# Fireflies syncs call summary + sentiment to HubSpot deal record
curl -X POST "https://api.fireflies.ai/graphql" \
  -H "Authorization: Bearer $FIREFLIES_API_KEY" \
  -d '{
    "query":"mutation SyncToHubspot($meetingId: ID!) { syncToHubspot(meetingId: $meetingId) { success } }",
    "variables":{"meetingId":"<meeting-id>"}
  }'
```

### Recipe 6: Granola → Notion auto-sync

```bash
# Granola has native Notion integration; one-time setup
mcp tool granola.connect_notion \
  --workspace-id "<notion-workspace>" \
  --database-id "<transcript-db>" \
  --enable-auto-sync true
```

### Recipe 7: Central transcript DB schema

```bash
mcp tool notion.create_database \
  --parent '{"page_id":"<exec-hub>"}' \
  --title '[{"text":{"content":"Meeting Transcripts"}}]' \
  --properties '{
    "Title":{"title":{}},
    "Date":{"date":{}},
    "Type":{"select":{"options":[{"name":"Board"},{"name":"Investor"},{"name":"Customer"},{"name":"1:1"},{"name":"All-hands"},{"name":"QBR"},{"name":"Strategy"}]}},
    "Tool":{"select":{"options":[{"name":"Granola"},{"name":"Fathom"},{"name":"Fireflies"},{"name":"Otter"}]}},
    "Decisions":{"rich_text":{}},
    "Action items":{"rich_text":{}},
    "Sentiment":{"select":{"options":[{"name":"Positive"},{"name":"Neutral"},{"name":"Tense"},{"name":"Concerning"}]}},
    "Participants":{"multi_select":{}}
  }'
```

### Recipe 8: Search across all transcripts

```bash
# Find all decisions mentioning "Series B" in last 90 days
mcp tool notion.query_database \
  --database-id "<transcript-db>" \
  --filter '{
    "and":[
      {"property":"Date","date":{"on_or_after":"2027-01-08"}},
      {"property":"Decisions","rich_text":{"contains":"Series B"}}
    ]
  }'
```

### Recipe 9: Cross-tool transcript normalization

```python
# Different tools format speaker labels differently
# Normalize to common format: "[HH:MM] Speaker: text"
def normalize_granola(t):
    return re.sub(r'\n([A-Z][a-z]+)\s+(\d{1,2}:\d{2})\s*\n', r'\n[\2] \1: ', t)
def normalize_fathom(t):
    return re.sub(r'\n(\d{1,2}:\d{2})\s+(\w+):\s*', r'\n[\1] \2: ', t)
def normalize_fireflies(t):
    # Fireflies uses "Speaker A:" prefix; map to actual names from participant list
    return t  # implement mapping
```

### Recipe 10: Per-meeting-type minutes template generation

```bash
# Board minutes via Fathom + Notion
MINUTES=$(curl -fsSL "https://api.fathom.video/v1/meetings/$MEETING_ID/summary" \
  -H "Authorization: Bearer $FATHOM_API_KEY" \
  | jq -r '.summary')

mcp tool notion.create_page \
  --parent '{"page_id":"<board-minutes-db>"}' \
  --children-markdown "# Board Minutes — $(date +%F)

## Attendees
[Auto-pulled]

## Decisions
$MINUTES

## Action items (pushed to Linear)
[Auto-extracted]"
```

### Recipe 11: Cost / coverage check (monthly)

```bash
mcp tool notion.query_database \
  --database-id "<transcript-db>" \
  --filter '{"property":"Date","date":{"on_or_after":"2027-04-01"}}' \
| jq -r '[group_by(.properties.Tool.select.name) | .[] | {tool: .[0].properties.Tool.select.name, count: length}]'

# Free tier check:
# Fathom — free unlimited
# Otter — 1200 min/mo free
# Granola — paid only ($14/mo)
# Fireflies — 800 min/mo free, then $10/seat
```

### Recipe 12: Per-meeting privacy mode

```markdown
## Privacy flags

| Meeting | Auto-record | Auto-sync to DB | Notes |
|---|---|---|---|
| Board exec session (last 30 min) | NO | NO | Confidential to investors+founders |
| Customer NDA call | YES | private folder | Restricted access |
| Investor diligence | YES (Fireflies) | private folder | Watermarked |
| All other | YES | public-internal | Default |

Configure per-tool:
- Granola: "Do not capture" flag per meeting
- Fathom: "Private" toggle in Pre-meeting settings
- Fireflies: "Pause" command mid-meeting via Slack bot
```

## Examples

### Example 1: Set up notetaker stack for new CEO

**Goal:** Founder onboarding their notetaker stack.

**Steps:**
1. Choose by meeting type (Recipe 1).
2. Subscribe: Fathom (free), Granola ($14/mo), Fireflies (if multilingual customer calls).
3. Set Granola defaults for strategy / 1:1 (Recipe 2).
4. Connect Granola → Notion (Recipe 6).
5. Build central transcript DB (Recipe 7).
6. Set privacy flags (Recipe 12).

**Result:** Every meeting captured, searchable, with privacy guardrails.

### Example 2: Board meeting transcript → minutes + actions

**Goal:** 90-min board meeting → published minutes within 48h.

**Steps:**
1. Fathom records (bot joins).
2. T+1h: Export transcript (Recipe 3).
3. T+2h: Extract decisions + actions (Recipe 4).
4. T+4h: Generate minutes (Recipe 10).
5. T+24h: Push action items to Linear with DRIs.
6. T+48h: Publish minutes + distribute (`board-meeting-prep-deck-minutes` skill).

**Result:** Minutes in 48h with auto-extracted decisions; institutional memory preserved.

## Edge cases / gotchas

- **Bot vs bot-free.** Some participants object to "another bot in the meeting." Granola bot-free is the win for sensitive 1:1s.
- **macOS-only Granola.** Windows / Linux participants need a different tool (Fathom is the universal fallback).
- **Free tier limits.** Otter caps at 1200 min/mo; Fireflies at 800 min/mo. Fathom is best free unlimited.
- **Transcription accuracy varies by accent.** Test with your team's accents before standardizing.
- **Multilingual = Fireflies.** 100+ languages; others top out at ~20.
- **CRM auto-sync for sales = Fireflies / Vidyard / Otter Business.** Granola/Fathom don't push to CRM by default.
- **Compliance (HIPAA, SOC 2).** Each tool varies; check before recording sensitive calls.
- **Recording consent.** EU + 2-party-consent US states require explicit "this call is being recorded" announcement.
- **Sensitive sessions skip recording.** Board exec session, comp discussions, layoff conversations.
- **Storage cost compounds.** 100 hrs of transcripts in Notion is fine. Tooling DB itself stores videos; check retention policy.
- **Search across tools fragmented.** Central Notion DB (Recipe 7) is the source of truth; tool-specific search is limited.
- **Action item extraction is heuristic.** Always human-review before auto-pushing to Linear. Wrong action assigned to wrong person = trust erosion.

## Sources

- [Granola vs Fireflies vs Fathom vs Otter — Granola blog](https://www.granola.ai/blog/meeting-note-tool-pricing-granola-vs-fireflies-fathom-otter)
- [Best AI notetakers 2026 — Meetingnotes.com](https://meetingnotes.com/blog/best-ai-note-takers)
- [Granola API](https://granola.ai/docs/api)
- [Fathom API docs](https://help.fathom.video/en/articles/9088373-api)
- [Fireflies GraphQL API](https://docs.fireflies.ai/)
- [Otter API](https://otter.ai/api)
