<!--
Sources: https://buffer.com/library/social-media-calendar/ + https://help.circle.so/p/scheduled-posts + https://discord.com/developers/docs/resources/channel#create-message + https://api.slack.com/methods/chat.scheduleMessage
-->
# Engagement Programming — Themed Days + AMAs — SKILL

Editorial calendar with recurring formats (Monday motivation / Tuesday tactics / Wednesday wins / Thursday discussion / Friday wrap) + monthly AMAs + quarterly town halls. AMA mechanics: announce 7d out → Q&A submission form → live 60-min session → top-Qs digest post. Outputs Notion editorial DB + scheduled posts across Discord / Slack / Circle / Discourse.

## When to use

- New community needs a posting rhythm (avoid the "ghost town" effect first 30 days).
- Existing community with sparse activity (<3 member posts/day for 1k member group).
- Pre-launch / product-launch coordination — AMA + town hall format.
- Quarterly cycle — town hall, roadmap update, ambassador AMA.
- Expanding into a new content surface (e.g., adding video AMAs in Discord Stage).
- Editorial calendar gap — running out of post ideas.

Trigger phrases: "themed days", "AMA", "town hall", "editorial calendar", "engagement programming", "weekly threads", "Monday motivation".

## Setup

```bash
# Notion editorial DB
mcp tool notion.create_database --parent_id $COMM_PAGE \
  --title "Editorial Calendar" \
  --properties '{"Title":{"title":{}},"Channel":{"select":{}},"Status":{"select":{}},"Type":{"select":{}},"Author":{"people":{}},"Scheduled":{"date":{}}}'

# Discord scheduled message
mcp tool discord-mcp-full.schedule_message \
  --channel_id $CH --content "Monday Motivation: what win are you chasing this week?" \
  --send_at "2026-06-15T14:00:00Z"

# Slack scheduled
mcp tool slack.chat_scheduleMessage \
  --channel '#general' --text "Tactical Tuesday — share one tactic" \
  --post_at $(date -d "2026-06-16 09:00" +%s)

# Circle scheduled via cli-anything
curl -X POST -H "Authorization: Bearer $CIRCLE_TOKEN" \
  https://app.circle.so/api/v1/spaces/$SPACE_ID/posts \
  -d '{"name":"Win Wednesday","body":"What shipped?","publish_at":"2026-06-17T13:00:00Z"}'
```

Workspace prerequisites:
- Notion DB `Editorial Calendar`.
- Notion DB `AMA Briefs` for upcoming AMAs.
- One thread channel per format (`#monday-motivation`, `#tactical-tuesday`, ...).
- Discord Stage / Slack Huddle / Zoom for live AMAs.

## Common recipes

### Recipe 1: 4-week themed-day calendar

| Day | Theme | Format | Owner |
|---|---|---|---|
| Mon | Monday motivation | "What win are you chasing?" thread | Bot |
| Tue | Tactical Tuesday | "Share one tactic that worked" | Rotating member |
| Wed | Win Wednesday | "What shipped?" thread | Bot |
| Thu | Thursday discussion | Curated provocative topic | Mod team |
| Fri | Friday wrap | "Best post of week" + emoji vote | Bot |
| Sat | Off-topic Saturday | `#off-topic` permission opens | n/a |
| Sun | Sunday brief | "Top 3 reads from the week" digest | Bot |

### Recipe 2: Auto-schedule a month at a time

```python
from datetime import datetime, timedelta

START = datetime(2026, 6, 15)
WEEKS = 4
TEMPLATES = {
  0: ("Monday motivation", "monday-motivation", "What's your big focus this week?"),
  1: ("Tactical Tuesday", "tactical-tuesday", "Share one tactic that worked last week"),
  2: ("Win Wednesday", "win-wednesday", "What shipped or progressed?"),
  3: ("Thursday discussion", "thursday-discussion", "$ROTATING_PROVOCATIVE_PROMPT"),
  4: ("Friday wrap", "friday-wrap", "Best post of the week — vote"),
}

for w in range(WEEKS):
  for day, (title, ch, body) in TEMPLATES.items():
    when = START + timedelta(weeks=w, days=day)
    # Notion
    notion.create_page("Editorial Calendar", {"Title": title, "Channel": ch, "Scheduled": when.isoformat()})
    # Discord schedule
    discord_full.schedule_message(channel_id=ch_id[ch], content=body, send_at=when.isoformat())
```

### Recipe 3: AMA brief template

```markdown
# AMA Brief — $GUEST_NAME ($DATE)

## Guest
- Role:
- Why they're interesting:
- Hot-take they hold:

## Pre-AMA (D-7 to D-1)
- D-7: Announce post + Q&A submission Google Form
- D-3: Mid-week reminder + 3 questions sneak-peek
- D-1: 24h reminder + calendar reminder
- D-0: 1h reminder

## Host script (60min)
- 5min welcome + 30s guest intro
- 10min curated submitted-Qs (5 best)
- 35min live Q&A
- 5min wrap + "where to find them"
- 5min plug + next AMA tease

## Post-AMA (D+1 to D+7)
- D+1: Top-Qs digest post in community + recording link
- D+3: Pull quotes for social
- D+7: Round-up of guest's content
```

### Recipe 4: Discord Stage for live AMA

```bash
# Create scheduled Stage event
mcp tool discord-mcp-full.create_scheduled_event \
  --guild_id $GUILD_ID \
  --name "AMA with Jane Doe" \
  --scheduled_start_time "2026-06-22T18:00:00Z" \
  --scheduled_end_time "2026-06-22T19:00:00Z" \
  --entity_type 1 \
  --channel_id $STAGE_CH_ID \
  --description "$AMA_BRIEF_URL"
```

Members get a clickable RSVP reminder.

### Recipe 5: Q&A submission form

Google Form fields:
- Question (text)
- Your handle (text, optional)
- Topic (dropdown: product / industry / personal / other)

```bash
# Pre-AMA, share form in:
mcp tool discord-mcp-full.create_message \
  --channel_id $AMA_CH \
  --content "AMA with @Jane is next Thursday! Submit Qs: $FORM_URL"
```

### Recipe 6: Slack town hall recurring

```bash
mcp tool slack.chat_scheduleMessage \
  --channel '#town-hall' \
  --text "Quarterly town hall TODAY at 4pm — Zoom: $ZOOM_LINK" \
  --post_at $(date -d "2026-06-30 14:00" +%s)
```

Town hall = quarterly; AMA = monthly; themed days = daily.

### Recipe 7: Twitch / YouTube Live AMA

```bash
# Twitch — schedule via API
curl -X POST -H "Authorization: Bearer $TWITCH_TOKEN" \
  -H "Client-Id: $TWITCH_CLIENT_ID" \
  -H "Content-Type: application/json" \
  "https://api.twitch.tv/helix/schedule/segment?broadcaster_id=$ID" \
  -d '{"start_time":"2026-06-22T18:00:00Z","timezone":"UTC","duration":"60","title":"AMA: Jane Doe","category_id":"509670"}'

# YouTube Live AMA — `youtube-mcp` schedule
mcp tool youtube.liveBroadcasts_insert \
  --title "Community AMA: Jane" \
  --scheduledStartTime "2026-06-22T18:00:00Z"
```

### Recipe 8: Top-Q digest auto-generate post-AMA

```python
# Capture transcript (youtube-mcp-transcript / Zoom transcript)
transcript = youtube_transcript.fetch(video_id)
# Cluster questions
prompt = """
From this AMA transcript, extract the top 7 questions asked
and the guest's answer in 2 sentences. Output as markdown.
"""
digest = claude.generate(prompt + transcript)
# Post to community
discord_full.send_message(channel_id=AMA_CH, content=f"# Top-Qs from yesterday's AMA\n\n{digest}\n\nFull recording: $URL")
```

### Recipe 9: "Best post of the week" emoji vote

```bash
# Friday: post a thread of week's top 5 candidate posts
# Members react with 1️⃣–5️⃣ on the parent message
# Monday: count reactions, winner gets pinned + member-of-week role

REACTIONS=$(mcp tool discord-mcp-full.get_message --channel_id $FRI_CH --message_id $FRI_MSG)
WINNER=$(echo "$REACTIONS" | jq -r '.reactions | max_by(.count) | .emoji.name')
```

### Recipe 10: Cadence + KPI table

| Format | Cadence | KPI | Target |
|---|---|---|---|
| Themed daily | 7x/week | Replies/thread | ≥3 |
| Member spotlight | 1-2x/week | Reactions/post | ≥10 |
| Monthly AMA | 1x/month | Live attendees | ≥10% of MAU |
| Town hall | 1x/quarter | Attendance + Q-survey | ≥20% of MAU |
| Newsletter recap | 1x/week | Open rate | ≥40% |

## Examples

### Example 1: New SaaS community first 90 days

**Goal:** Spin up rhythm — 500 members joining over 90 days, need daily activity.

**Steps:**
1. Generate 4-week calendar (Recipe 1).
2. Auto-schedule 90 days via Python loop (Recipe 2).
3. First AMA at Day 30 with founder; brief from Recipe 3.
4. Friday emoji-vote (Recipe 9).

**Result:** Avg posts/day = 8.3 by week 6; AMA hits 18% MAU live.

### Example 2: Quarterly town hall on Zoom

**Goal:** 50 design partners on Slack; quarterly product town hall.

**Steps:**
1. Schedule via Slack (Recipe 6) + Zoom calendar.
2. Pre-event: roadmap doc shared 3 days prior.
3. Live: founder presents 20min + 40min Q&A.
4. Post: digest post + recording.

**Result:** 30 attendees; 8 partners book follow-up calls; NPS +12.

## Edge cases / gotchas

- **Themed-day fatigue** — after 8 weeks of identical prompts, engagement decays. Rotate prompts; member-suggested themes.
- **Schedule-message timezone** — Discord/Slack APIs need UTC; convert from member-local.
- **Bot-driven posts feel hollow** — alternate bot-scheduled with hand-crafted/founder posts; 70/30 is healthy.
- **AMA no-show** — always have a backup question batch + a co-host. Single-host AMAs fail hard if guest is late.
- **Q-submission form abandonment** — if you require a Google Form, drop-off is high. Allow inline DMs as backup.
- **Discord Stage limits** — only 1k concurrent speakers; for larger AMAs use voice channel + reactions.
- **Town hall vs AMA confusion** — town hall = company → members (1-way + Q&A); AMA = member → guest. Mix is fine; label clearly.
- **Recording consent** — pre-AMA, post in channel "this will be recorded"; mute Stage attendees who don't consent.
- **Cross-timezone AMA equity** — rotate AMA time slots (EU-friendly / APAC-friendly / US-friendly) over the year.
- **Notion sync drift** — schedule-the-post and update-Notion-status are 2 separate steps; bot must do both.
- **Top-Q digest LLM hallucination** — always cite the original Q + answer; never paraphrase the guest's words.

## Sources

- [Buffer social media calendar](https://buffer.com/library/social-media-calendar/)
- [Circle scheduled posts](https://help.circle.so/p/scheduled-posts)
- [Discord scheduled events API](https://discord.com/developers/docs/resources/guild-scheduled-event)
- [Discord create-message API](https://discord.com/developers/docs/resources/channel#create-message)
- [Slack chat.scheduleMessage](https://api.slack.com/methods/chat.scheduleMessage)
- [Twitch schedule API](https://dev.twitch.tv/docs/api/reference#create-channel-stream-schedule-segment)
- [Common Room engagement funnel](https://www.commonroom.io/blog/community-engagement-funnel/)
