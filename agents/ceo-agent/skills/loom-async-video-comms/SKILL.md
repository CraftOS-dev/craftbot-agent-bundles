<!--
Source: https://zight.com/blog/best-loom-alternatives-2026/
Async video: Tella / Vidyard / Zight / Berrycast (Loom softening post-Atlassian)
-->
# Loom-Style Async Video Comms

Loom usage softened post-Atlassian acquisition (free tier capped at 25 videos / 5 min). 2026 alternatives: Tella (polished branded recordings — external comms), Vidyard (sales-CRM-integrated), Zight (screenshot + video unified), Berrycast (free unlimited). For CEO async: Tella outward, Vidyard sales-aligned. Speaker-notes script + distribution via Slack/email is the agent-driven path.

## When to use

- 3-min CEO update to the team (faster than typing, more human than email).
- Strategy explainer for the board ahead of a meeting.
- Customer-facing async update (Tella branded).
- Onboarding video for a new hire.
- Recap when a meeting absentee needs the gist.

Trigger phrases: "record a Loom", "async video", "Tella recording", "video update", "CEO video", "speaker notes for video".

## Setup

```bash
# Tella — for polished external recordings
curl -fsSL "https://api.tella.video/v1/me" \
  -H "Authorization: Bearer $TELLA_API_KEY"

# Vidyard — sales-CRM integration
curl -fsSL "https://api.vidyard.com/dashboard/v1/me" \
  -H "Authorization: Bearer $VIDYARD_API_KEY"

# Zight — screenshot + video
curl -fsSL "https://api.zight.com/v1/me" \
  -H "Authorization: Bearer $ZIGHT_API_KEY"

# Berrycast — free unlimited
curl -fsSL "https://api.berrycast.com/v1/me" \
  -H "Authorization: Bearer $BERRYCAST_TOKEN"
```

Auth / API key requirements:
- `TELLA_API_KEY` — Tella Settings → API (paid plan, $19/mo+).
- `VIDYARD_API_KEY` — Vidyard Settings → API access (free + paid tiers).
- `ZIGHT_API_KEY` — Zight Settings → Integrations.
- `BERRYCAST_TOKEN` — Berrycast Settings → API.

## Common recipes

### Recipe 1: Tool routing — which tool when

```markdown
| Use case | Tool | Why |
|---|---|---|
| CEO update to team (internal) | Berrycast (free) or Tella (branded) | Quick + watchable |
| Customer-facing async | Tella | Polished + brand controls |
| Sales follow-up with prospect | Vidyard | CRM integration (HubSpot / SFDC) |
| Bug repro / quick screenshot | Zight | Unified screenshot + video |
| Board pre-read explainer | Tella | Polished + analytics |
| Internal meeting recap | Berrycast / Tella | Free if frequent; Tella if polished |
| Sales prospecting (cold) | Vidyard | Sequenced + tracked |
```

### Recipe 2: Speaker notes script template (3-min video)

```markdown
## [Topic] — 3-min CEO update

### Hook (0:00-0:15)
"[Name], CEO here. Quick 3-min update on [topic]. Watch end-to-end — there's an ask at the end."

### Context (0:15-0:45)
- What's the situation?
- Why now?
- Who's affected?

### What's new (0:45-2:15)
- Decision / change / launch
- 2-3 specifics
- What people should do differently

### Ask (2:15-2:45)
- Specific action requested
- Deadline
- How to respond

### Close (2:45-3:00)
"Slack me with questions. Talk soon."
```

### Recipe 3: Record + upload via Tella API

```bash
# Tella supports both manual record (in-app) and API upload
TELLA_VIDEO_ID=$(curl -X POST "https://api.tella.video/v1/videos" \
  -H "Authorization: Bearer $TELLA_API_KEY" \
  -F "file=@./ceo-update-2027-04.mp4" \
  -F "title=CEO update — April 2027" \
  -F "description=$(cat ./speaker-notes.md)" \
  | jq -r '.id')

# Get the share URL
SHARE_URL=$(curl -fsSL "https://api.tella.video/v1/videos/$TELLA_VIDEO_ID" \
  -H "Authorization: Bearer $TELLA_API_KEY" \
  | jq -r '.share_url')

echo "Share: $SHARE_URL"
```

### Recipe 4: Vidyard sales-personalized video

```bash
curl -X POST "https://api.vidyard.com/dashboard/v1/videos" \
  -H "Authorization: Bearer $VIDYARD_API_KEY" \
  -d '{
    "title":"Sarah from Acme — quick demo for you",
    "personalized":true,
    "viewer_token":"acme-sarah",
    "auto_play":true
  }'

# Get tracking link
curl -fsSL "https://api.vidyard.com/dashboard/v1/videos/<video-id>/sharing_links" \
  -H "Authorization: Bearer $VIDYARD_API_KEY"
```

### Recipe 5: Distribute via Slack

```bash
mcp tool slack.send \
  --channel "#all-hands" \
  --message ":movie_camera: *3-min CEO update on Series B announcement*

$SHARE_URL

Speaker notes: [Notion link]
Read time: 3 min
Ask at the end. Watch end-to-end."
```

### Recipe 6: Distribute via email (board / external)

```bash
mcp tool gmail.send \
  --to "board@company.com" \
  --subject "3-min video: where we are on Series B" \
  --body "Board,

3-min Tella recording with my view on Series B timing + market:
$SHARE_URL

Speaker notes attached. We'll discuss at Thursday's board meeting."
```

### Recipe 7: Pull engagement analytics

```bash
# Tella analytics
curl -fsSL "https://api.tella.video/v1/videos/$TELLA_VIDEO_ID/views" \
  -H "Authorization: Bearer $TELLA_API_KEY" \
| jq '.views[] | {viewer_email, watched_pct, drop_off_at_sec, watched_at}'

# Use drop-off insight for the next video — when did people stop watching?
```

### Recipe 8: Berrycast for free unlimited

```bash
# Berrycast = free unlimited, simple
curl -X POST "https://api.berrycast.com/v1/upload" \
  -H "Authorization: Bearer $BERRYCAST_TOKEN" \
  -F "video=@./quick-update.webm" \
  -F "title=Internal quick update"
```

### Recipe 9: Zight screenshot + video for bug reports

```bash
# Quick screen + audio
curl -X POST "https://api.zight.com/v1/recordings" \
  -H "Authorization: Bearer $ZIGHT_API_KEY" \
  -d '{"type":"screen_video","duration_sec":60,"audio":true}'
```

### Recipe 10: Async video routing for the org

```markdown
## Team async video defaults

| Sender | Audience | Tool |
|---|---|---|
| CEO | Internal team | Berrycast (free, unlimited) |
| CEO | Board / external | Tella |
| Sales | Prospect | Vidyard |
| Eng / Product | Bug repro | Zight |
| Customer Success | Customer | Tella |
| Marketing | Public | Tella + YouTube |

Doc this in onboarding so team doesn't fragment to 5 different tools.
```

### Recipe 11: Video catalog DB

```bash
mcp tool notion.create_database \
  --parent '{"page_id":"<ceo-hub>"}' \
  --title '[{"text":{"content":"CEO Async Videos"}}]' \
  --properties '{
    "Title":{"title":{}},
    "Date":{"date":{}},
    "Audience":{"select":{"options":[{"name":"Team"},{"name":"Board"},{"name":"Investors"},{"name":"Customers"}]}},
    "URL":{"url":{}},
    "Avg watch %":{"number":{}},
    "Notes":{"rich_text":{}}
  }'
```

### Recipe 12: Loom legacy migration (if you still use it)

```bash
# Loom still works for short internal use, but free tier 25 videos / 5 min
# If migrating: export library via Loom API, import to Tella
LOOM_VIDEOS=$(curl -fsSL "https://www.loom.com/api/v1/videos" -H "Authorization: Bearer $LOOM_API_KEY" | jq -r '.[] | .id')
for V in $LOOM_VIDEOS; do
  DL_URL=$(curl -fsSL "https://www.loom.com/api/v1/videos/$V" -H "Authorization: Bearer $LOOM_API_KEY" | jq -r '.download_url')
  curl -fsSL "$DL_URL" -o "$V.mp4"
  # Re-upload to Tella
  curl -X POST "https://api.tella.video/v1/videos" -H "Authorization: Bearer $TELLA_API_KEY" -F "file=@./$V.mp4"
done
```

## Examples

### Example 1: 3-min CEO update — Series B announcement

**Goal:** Announce Series B close to the team async (some are in different timezones).

**Steps:**
1. Draft speaker notes (Recipe 2) — hook / context / what's new / ask / close.
2. Record in Tella (or Berrycast for free) — 1 take, edit minor.
3. Upload (Recipe 3).
4. Distribute via Slack + email (Recipe 5-6).
5. T+7 days: pull engagement (Recipe 7). If avg watch % < 50% → next video is shorter or hook is weak.

**Result:** Team aligned without a meeting; engagement measured.

### Example 2: Sales prospecting video sequence

**Goal:** Sales team needs Vidyard videos for top-100 outbound list.

**Steps:**
1. Each rep records a 60-sec personalized video (Recipe 4).
2. Vidyard generates per-prospect tracked link.
3. CRM-integrated send (HubSpot / Salesforce).
4. Engagement triggers next-touch automation.

**Result:** Higher open + reply rate vs text-only outbound.

## Edge cases / gotchas

- **Tool sprawl risk.** 5 people on 5 different tools = no shared library. Standardize via Recipe 10.
- **Free tier ceilings.** Loom 25 videos / 5 min, Vidyard free tier limited to public sharing. Plan for paid if frequent use.
- **Engagement falls off after 90s.** Force discipline — under 3 min unless it's a deep dive.
- **No script = rambling.** 1-min speaker notes prep saves 5x the watching frustration.
- **Public vs private sharing.** Vidyard / Loom default to public-link; lock to email-required for sensitive content.
- **Captions matter.** Auto-captioned videos get 40%+ more watch-through. Use Tella / Vidyard auto-caption.
- **Mobile recording = noisy + shaky.** For external comms, use desktop + decent mic.
- **Tella + branded watermark.** Set company brand template once; everyone uses it.
- **Vidyard CRM scoping.** Sales videos need consent for tracking in EU (GDPR).
- **Don't replace meetings entirely.** Some decisions need real-time discussion. Async = updates + explainers, not negotiations.
- **Loom is fine for quick internal.** If your team likes it and free tier covers, don't migrate. Migrate when free tier hurts.
- **Video files are heavy.** Don't try to email .mp4. Always send the share link.

## Sources

- [Loom alternatives 2026 — Zight](https://zight.com/blog/best-loom-alternatives-2026/)
- [Tella API docs](https://tella.video/api)
- [Vidyard API docs](https://knowledge.vidyard.com/hc/en-us/articles/360042316194)
- [Berrycast home](https://berrycast.com)
- [Loom API legacy docs](https://www.loom.com/developers)
