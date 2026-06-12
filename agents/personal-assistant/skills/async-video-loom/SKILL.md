<!--
Source: https://dev.loom.com/
-->
# Async Video — Loom — SKILL

Draft the script + outline, surface the recording flow (user-side, camera/mic), and after recording: pull metadata + share-link via REST + deliver via email. Loom owns async exec/team comms mind-share. Vidyard (sales) and Tella (creative) are alternatives.

## When to use this skill

- **"Send a Loom to X"** — direct trigger.
- **"Draft a 2-min explainer"** — pre-record script + outline.
- **"Share my last Loom"** — retrieve + send.
- **"Async standup video"** — recurring async update.
- **Post-meeting follow-up via video instead of email** — async exec.

**Do NOT use this skill when:**
- Long-form YouTube — out of scope.
- Live video / meeting — use `zoom-mcp`.
- Screen-share within a meeting — Zoom AI Companion.
- Editing post-record — Loom has basic edit; for serious editing use Descript / Final Cut.

## Setup

### Loom REST API

```bash
# Get key: https://www.loom.com/looms/settings/integrations/api
export LOOM_API_KEY="<key>"

curl -s "https://www.loom.com/api/v1/me" \
  -H "Authorization: Bearer $LOOM_API_KEY"
```

Docs: https://dev.loom.com/

### Loom app install (user-side)

```bash
# macOS
brew install --cask loom

# Windows
# Download from https://www.loom.com/download

# Chrome extension
echo "https://chrome.google.com/webstore/detail/loom-free-screen-recorder/liecbddmkiiihnedobmlmillhodjkdmb"
```

### Agent's recording boundary

Recording itself is user-side (Loom app accesses camera/mic). Agent:
1. Drafts script + outline pre-record.
2. Pulls metadata + share-link post-record.
3. Composes the "here's the video" email.

## Common recipes

### Recipe 1: Draft a video script

```python
TOPIC = "Q3 planning update — 2 min"
AUDIENCE = "Direct reports"
GOAL = "Surface 3 key changes + 1 ask"

script = f"""
**Intro (15s)**
Hey team — quick async update on Q3 planning. 2 min, no need to reply.

**Body (90s)**
Three updates:
1. [Update 1 with context]
2. [Update 2 with context]
3. [Update 3 with context]

**Ask (15s)**
One ask: [specific action + deadline].

**Outro (10s)**
Let me know if you have questions. Thanks.
"""
```

Surface to user as outline + delivery cues (pause, smile, etc.).

### Recipe 2: List recent Loom videos

```bash
curl -s "https://www.loom.com/api/v1/videos?limit=10&sort=-created_at" \
  -H "Authorization: Bearer $LOOM_API_KEY" \
  | jq '.videos[] | {id, name, duration, share_url, created_at}'
```

### Recipe 3: Get video metadata

```bash
VIDEO_ID="<id>"
curl -s "https://www.loom.com/api/v1/videos/$VIDEO_ID" \
  -H "Authorization: Bearer $LOOM_API_KEY" \
  | jq '{name, duration, share_url, status, thumbnail_url, transcript_url}'
```

### Recipe 4: Pull transcript

```bash
curl -s "https://www.loom.com/api/v1/videos/$VIDEO_ID/transcript" \
  -H "Authorization: Bearer $LOOM_API_KEY"
```

Returns text + timestamps.

### Recipe 5: Update video metadata (name + description)

```bash
curl -X PATCH "https://www.loom.com/api/v1/videos/$VIDEO_ID" \
  -H "Authorization: Bearer $LOOM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Q3 Planning Update — 2026-06-09",
    "description": "Async update on Q3 priorities + 1 ask"
  }'
```

### Recipe 6: Set sharing / privacy

```bash
curl -X PATCH "https://www.loom.com/api/v1/videos/$VIDEO_ID" \
  -H "Authorization: Bearer $LOOM_API_KEY" \
  -d '{
    "privacy": "team_only",  # or "public", "private", "password_protected"
    "password": "<if-password-protected>"
  }'
```

### Recipe 7: Workspace-level video search

```bash
curl -s "https://www.loom.com/api/v1/videos/search?q=Q3" \
  -H "Authorization: Bearer $LOOM_API_KEY"
```

### Recipe 8: Compose share-to email

```bash
# After recording, agent composes
VIDEO_ID="<id>"
VIDEO=$(curl -s "https://www.loom.com/api/v1/videos/$VIDEO_ID" -H "Authorization: Bearer $LOOM_API_KEY")
SHARE_URL=$(echo "$VIDEO" | jq -r .share_url)

mcp tool gmail.draft \
  --to "alex@team.com" \
  --subject "2-min update on Q3 planning" \
  --body "Hey Alex — recorded a quick 2-min walkthrough of the Q3 plan: $SHARE_URL

Key points are in the transcript if you'd rather skim:
- [Point 1]
- [Point 2]
- [Point 3]

No reply needed unless questions.

— [User]"
```

### Recipe 9: Insert chapters / timestamps

```bash
# Chapter markers (for long videos)
curl -X POST "https://www.loom.com/api/v1/videos/$VIDEO_ID/chapters" \
  -H "Authorization: Bearer $LOOM_API_KEY" \
  -d '{
    "chapters":[
      {"timestamp":0,"title":"Intro"},
      {"timestamp":15,"title":"Update 1: X"},
      {"timestamp":45,"title":"Update 2: Y"},
      {"timestamp":75,"title":"Ask"}
    ]
  }'
```

### Recipe 10: Bulk-send a video to a list

```python
RECIPIENTS = ["alex@", "blake@", "casey@"]
VIDEO_URL = "<share-url>"

for r in RECIPIENTS:
    gmail.send(to=r, subject="Quick async update",
        body=f"Hi {r.split('@')[0]}, here's a 2-min update: {VIDEO_URL}")
```

Note: Loom share-link tracks views by viewer email if signed in to Loom.

### Recipe 11: Stitch transcript → action items

```python
# Recipe 4 to pull transcript
import requests
transcript = requests.get(f"https://www.loom.com/api/v1/videos/{vid}/transcript",
    headers={"Authorization":f"Bearer {LOOM_API_KEY}"}).text

# Use Claude / NLP to extract action items
actions = extract_action_items(transcript)
# Push to Todoist via task-mgmt-todoist-things-notion skill
```

### Recipe 12: Schedule send via Gmail

```bash
mcp tool gmail.schedule_send \
  --draft-id "<draft-id>" \
  --send-at "2026-06-10T08:00:00-07:00"
```

### Recipe 13: Async standup pattern

```markdown
**Weekly async standup video (Loom)**
- Cadence: Monday 8am
- Duration: 90 seconds
- Outline:
  1. Last week: 1-2 wins (20s)
  2. This week: top 3 priorities (40s)
  3. Blockers / asks (15s)
  4. Anything else (15s)
- Share to: team Slack #async-standups
```

## Examples

### Example 1: Async update to direct reports

**Goal:** User wants to share Q3 plan changes async to 5 reports.

**Steps:**
1. Recipe 1: script outline; 2 min target.
2. User records via Loom app.
3. Recipe 5: rename "Q3 Planning Update — 2026-06-09".
4. Recipe 6: set privacy to team_only.
5. Recipe 9: add chapters.
6. Recipe 8: gmail draft to each report.
7. Surface drafts for user review.

**Result:** 5 personalized "here's the video" emails ready.

### Example 2: Loom retrieval

**Goal:** User asks "send my Loom from yesterday to my CEO."

**Steps:**
1. Recipe 2: list recent, find yesterday's.
2. Recipe 3: get metadata + share-url.
3. Recipe 8: compose email to CEO.

**Result:** Sent in 30s.

### Example 3: Vidyard alt for sales

**Goal:** Sales user wants Vidyard async outreach.

**Steps:**
1. Recommend Vidyard (sales-focused; CTAs + tracking).
2. Vidyard API: https://api.vidyard.com/v1/
3. Same pattern: draft script + post-record metadata + email.

**Result:** Vidyard workflow for sales context.

## Edge cases / gotchas

- **Loom Free vs Paid**: Free = 25 videos / 5min max each. Pro $15/mo unlimited. Source: https://www.loom.com/pricing
- **Workspace API limits**: 100 req/min per workspace.
- **Transcript availability**: ~30s post-record; may not be ready immediately.
- **Privacy = team_only requires workspace**: Personal Loom can't team-share.
- **Password-protected sharing**: Add deterrent for sensitive videos.
- **Video naming**: Default "New Loom 2026-06-09" — always rename (Recipe 5) for searchability.
- **Recording length**: > 10 min loses async benefit. Cap at 3 min for daily updates; 5 min for explainers.
- **First impression**: First 5 seconds need hook. Recipe 1 templates start with "Hey team — quick update" not "Hi everyone, today I'm going to talk about…"
- **No public API for editing**: Trim/edit must happen in Loom app.
- **Recording itself is user-side**: Agent can't initiate. Always surface the click-to-record path.
- **Chrome extension scope**: Chrome ext records browser tab; desktop app records full screen + camera.
- **Auto-emoji reactions**: Loom auto-shows viewer emoji reactions. Recommend turning off for serious / exec videos.
- **Comments threading**: Loom comments live on video, not in email. Surface to user for engagement.
- **Loom AI features**: Auto-titles, summaries, chapters on Pro+. Reduces post-record work.
- **Vidyard vs Loom positioning**: Vidyard sales-CTA-heavy; Loom team-collab-friendly. Pick by use case.
- **Tella**: Creative-oriented (multi-clip, transitions); for podcaster / educator. Source: https://www.tella.tv/

## Sources

- [Loom Developer](https://dev.loom.com/)
- [Loom Pricing](https://www.loom.com/pricing)
- [Vidyard API](https://api.vidyard.com/v1/)
- [Tella](https://www.tella.tv/)
- [Berrycast](https://berrycast.com/)
