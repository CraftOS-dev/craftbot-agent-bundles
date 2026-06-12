<!--
Sources:
- Restream API: https://developers.restream.io
- StreamYard: https://streamyard.com
- Riverside Studio: https://riverside.fm
- OBS Studio: https://obsproject.com
- vMix: https://www.vmix.com
- Wirecast: https://www.telestream.net/wirecast
- LiveU LU800: https://liveu.tv/products/lu800
- YouTube Live: https://support.google.com/youtube/answer/2474026
- Vimeo Live: https://vimeo.com/live
- Demio: https://demio.com
- Livestorm: https://livestorm.co
- Zoom Events: https://www.zoom.us/events
- MS Teams Live Events: https://learn.microsoft.com/en-us/microsoftteams/teams-live-events
- Webex Events: https://www.webex.com/webinars
-->
# Live Streaming (Restream / OBS / StreamYard / Riverside) — SKILL

End-to-end live streaming for virtual + hybrid events: platform decision → stream setup → multi-platform broadcast → recording + transcript → distribution. Choose by event size, multi-cam need, interactive Q&A latency, post-event distribution plan. SOTA 2026: WebRTC sub-second latency for interactive Q&A; multi-platform broadcast via Restream; OBS for hybrid multi-cam.

## When to use this skill

- Virtual event with single-cam keynote OR webinar
- Hybrid event with in-person + virtual streaming layered
- Multi-platform broadcast (YouTube + LinkedIn + Twitter simultaneously)
- Webinar production for marketing-led events
- Conference recording for post-event distribution + podcast
- Internal company all-hands (single internal platform)

**Do NOT use this skill when:**
- Pure in-person event with no virtual layer (skip streaming setup; just record)
- Closed-door customer summit (no public broadcast; private recording only)
- B2C festival entertainment streaming (different platform tier — Twitch / TikTok Live)
- For low-latency interactive networking, see `hybrid-event-low-latency-interaction`

## Setup

### Platform decision matrix

| Need | First-stop | Notes |
|---|---|---|
| Multi-platform broadcast (YouTube + LinkedIn + Twitter) | Restream | 1 upload → 30+ destinations |
| Browser-based, no install | StreamYard | Simplest for non-tech speakers |
| Separate local tracks per speaker (podcast-grade) | Riverside Studio | Best audio quality, post-edit ready |
| Hybrid multi-cam production | OBS Studio (free) | Custom scenes, transitions, per-track audio |
| Pro multi-cam paid | vMix or Wirecast | Full broadcast control, expensive |
| Remote venue with unreliable internet | OBS + LiveU LU800 (4G/5G bonded) | Hardware encoder |
| Marketing webinar | Demio or Livestorm | No-download for attendees |
| Enterprise hybrid + branded | Zoom Events | Best for enterprise + branding |
| Internal company all-hands | MS Teams Live Events | Free for M365 tenants |
| Enterprise alt | Webex Events | Cisco ecosystem |
| Evergreen webinar | Livestorm | Best on-demand replay UX |

### Tools

- `cli-anything` for Restream / Riverside / YouTube Live REST API
- `youtube-mcp` for YouTube Live broadcast config + post-event upload
- `zoom-mcp` for Zoom Events
- `ms-teams-mcp` for MS Teams Live Events
- `slack-mcp` for day-of stream ops channel
- `notion-mcp` for stream key DB (do NOT commit keys to git)

### Restream API

```bash
export RESTREAM_TOKEN="<oauth-bearer>"   # https://restream.io/developer
# Base: https://api.restream.io/v2/
```

### Riverside Studio API

```bash
export RIVERSIDE_TOKEN="<api-key>"
# Base: https://api.riverside.fm/v1/
```

### YouTube Live (via youtube-mcp)

```bash
# YouTube Live needs >50 subscriber threshold for mobile; otherwise approval cycle
# Pre-event: enable live streaming on channel 24-48 hours prior
```

### OBS Studio install

```bash
# macOS
brew install --cask obs

# Linux
sudo apt install obs-studio

# Windows: download installer from obsproject.com
```

## Common recipes

### Recipe 1: Restream multi-platform broadcast

```bash
# 1. Get channels (which destinations are connected)
curl -X GET https://api.restream.io/v2/user/channel/all \
  -H "Authorization: Bearer $RESTREAM_TOKEN"

# 2. Set stream metadata for current event
curl -X PUT https://api.restream.io/v2/user/stream-key \
  -H "Authorization: Bearer $RESTREAM_TOKEN" \
  -d '{
    "title": "DevConf 2027 — Day 1 Live",
    "description": "Live from Chicago — keynote, panels, breakouts."
  }'

# 3. Get stream key + RTMP URL (push from OBS or hardware encoder)
curl -X GET https://api.restream.io/v2/user/stream-key \
  -H "Authorization: Bearer $RESTREAM_TOKEN"
# Response: {"streamKey": "re_...", "rtmpUrl": "rtmp://live.restream.io/live"}

# 4. OBS Stream Settings:
# Server: rtmp://live.restream.io/live
# Stream key: re_xyz123...
```

### Recipe 2: OBS scenes for hybrid multi-cam

```
Scenes:
1. "Pre-show" — pre-event slide + sponsor loop + countdown timer
2. "Welcome" — wide stage shot + lower-third "DevConf 2027"
3. "Keynote Sarah" — tight on speaker + lower-third name + side-by-side slides
4. "Audience Q&A" — wide of audience + Q&A graphic overlay
5. "Panel" — multi-cam quad split (4 panelists) + lower-thirds
6. "Break" — break graphic + sponsor loop + music
7. "Sponsor spotlight" — sponsor video clip + logo
8. "Post-show" — thank-you slide + recording-available message

Transitions: 5-sec fade between scenes
```

### Recipe 3: OBS audio mix

```
Audio sources:
- Mic 1 (speaker lapel) → channel 1
- Mic 2 (handheld backup) → channel 2
- Mic 3 (audience Q&A) → channel 3
- Music + stinger → channel 4 (ducked under voices)
- Slide audio (videos in deck) → channel 5

Master output: -14 LUFS for streaming (broadcast standard)
```

### Recipe 4: Hardware encoder (LiveU) for unreliable venue internet

```bash
# LiveU LU800 bonds 4G/5G cellular for streaming when venue wifi is bad
# Configure stream output to Restream RTMP URL:
# - SDI input from venue switcher
# - Bonded cellular output (4 cards minimum)
# - Latency: 1-2 sec
# - Bitrate: 8-12 Mbps adaptive
```

### Recipe 5: Riverside Studio for separate-track podcast capture

```bash
# Schedule session
curl -X POST https://api.riverside.fm/v1/sessions \
  -H "Authorization: Bearer $RIVERSIDE_TOKEN" \
  -d '{
    "title": "DevConf 2027 — Sarah Khan Keynote",
    "scheduledAt": "2027-09-15T14:00:00Z",
    "participants": [
      {"name": "Sarah Khan", "email": "sarah@linear.com", "role": "guest"},
      {"name": "Alex Rodriguez", "email": "alex@us.com", "role": "host"}
    ],
    "recordingOptions": {
      "audio": "wav",         // separate per participant
      "video": "mp4",         // separate per participant
      "resolution": "1080p"
    }
  }'

# Post-session: download separate tracks per participant
# Edit in Descript (text-based editing) + transcript export
```

### Recipe 6: StreamYard (browser-based, simplest for non-tech)

```
1. Speakers click invite link → browser opens to studio
2. No install required
3. Banners + lower-thirds + screen share built in
4. Direct broadcast to YouTube / LinkedIn / Twitter / Facebook
5. Best for: webinars + interview panels + 1-2 speaker formats
```

### Recipe 7: YouTube Live broadcast setup

```bash
# Pre-event: enable live streaming on channel
# Via youtube-mcp
mcp tool youtube.create_live_broadcast \
  --title "DevConf 2027 — Day 1 Live Stream" \
  --description "Live from Chicago. Schedule + recordings at devconf.io" \
  --scheduled-start "2027-09-15T14:00:00Z" \
  --privacy "public" \
  --enable-dvr true \
  --enable-auto-start false \
  --enable-monetization false \
  --thumbnail-url "https://devconf.io/youtube-thumb.png"

# Returns broadcast ID + RTMP URL + stream key
# Push from OBS to YouTube RTMP URL
```

### Recipe 8: Multi-track recording (per session)

```python
# For each session, record separately for post-event distribution
sessions = notion.query_db('devconf-2027-agenda')
for s in sessions:
    obs.start_recording(filename=f"{s['title']}_{s['date']}.mp4")
    # ... session plays out ...
    obs.stop_recording()
    # Whisper transcript (separate skill)
    # Upload to YouTube via youtube-mcp
```

### Recipe 9: Demio webinar setup (marketing)

```bash
curl -X POST https://api.demio.com/v1/events \
  -d '{
    "name": "How to Scale LLM Infrastructure",
    "date": "2027-04-15T18:00:00Z",
    "duration": 45,
    "type": "live",
    "registration": {
      "url_slug": "scale-llm-infra",
      "form_fields": ["name", "email", "company", "title"],
      "redirect_url": "https://us.com/thanks"
    }
  }'
```

### Recipe 10: Zoom Events (enterprise hybrid)

```bash
mcp tool zoom.create_event \
  --topic "Acme Customer Summit 2027" \
  --type "hub_event" \
  --start "2027-09-15T08:00:00-05:00" \
  --duration 480 \
  --webinar-type "broadcast" \
  --attendee-cap 5000 \
  --branding-url "https://acme.com/zoom-events-theme"
```

### Recipe 11: MS Teams Live Events (internal company)

```bash
# Best for internal all-hands; free with M365 enterprise license
mcp tool ms-teams.create_live_event \
  --title "Q3 All-Hands" \
  --start "2027-04-20T16:00:00Z" \
  --duration 60 \
  --attendee-cap 10000 \
  --producers "ceo-office@us.com" \
  --presenters "ceo@us.com,cfo@us.com" \
  --recording true
```

## Examples

### Example A: 600-attendee hybrid conference, Day 1 setup

```
Equipment:
- 3 cameras (wide / tight / audience reaction)
- 4 mics (2 lapel for speakers + 1 handheld backup + 1 audience Q&A runner)
- OBS workstation (MacBook Pro M3 Max + Atem Mini Extreme switcher)
- LiveU LU800 backup (in case venue wifi fails)
- Push: Restream → YouTube Live + LinkedIn Live + Twitter

Pre-show: 30 min countdown + sponsor loop + lo-fi music
Latency: 8-15 sec (HLS to YouTube)
Captioning overlay: AI-Media Ai-Live integration
```

### Example B: Virtual-only conference (single-cam StreamYard)

```
Speakers join StreamYard browser studio
Host (MC) controls scenes + lower-thirds
Direct broadcast to YouTube Live + LinkedIn Live
Q&A via Slido (embedded URL on screen)
Recording: StreamYard auto-records; download MP4 post-event
Cost: $39/mo Pro plan (vs vMix at $1,200 one-time + OBS $0)
```

### Example C: Internal all-hands (MS Teams Live Events)

```
Producer: HR ops lead
Presenters: CEO + CFO + Engineering VP
Attendees: 8,000 employees globally
Recording: auto-saved to SharePoint
Captions: live AI captions (Microsoft Stream)
Q&A: integrated chat moderation
Cost: included in M365 enterprise
```

## Edge cases

### Venue wifi failure
Always plan: ethernet primary + venue wifi backup + cellular backup (LiveU OR phone hotspot). Test 24h before with full stream rehearsal.

### Stream key leakage
If stream key is committed to git or shared in Slack public channel, anyone can hijack stream. Rotate key day-of; store in `notion-mcp` private DB + share via 1Password.

### YouTube auto-monetization on copyrighted music
YouTube Content ID auto-flags copyrighted music. Use royalty-free music (Epidemic Sound / Artlist / `mcp-tts` generation). Document source.

### Latency mismatch in hybrid Q&A
Standard YouTube Live: 8-15 sec latency. Virtual audience asks question; in-room audience already moved on. For interactive Q&A, use WebRTC platform (RingCentral Events) — see `hybrid-event-low-latency-interaction`.

### Audio sync drift
Multi-cam setups can drift between camera audio and mic audio. Use SMPTE timecode (Tentacle Sync) OR pre-record audio separately + sync in post.

### Stream resolution + bitrate
1080p @ 30fps @ 6 Mbps is standard. 4K is overkill for most events (audience devices throttle to 1080p anyway). Increase bitrate to 8-12 Mbps for high-motion content (live sports, action).

### Speaker forgets to share screen
Most webinar platforms auto-prompt. For OBS, speaker shares via Discord / Zoom video call as input source — OBS captures it as scene.

### Recording vs streaming separately
Always record locally (OBS Save Local) IN ADDITION to streaming. If stream dies, you still have recording. Local recording at higher quality than stream.

### Copyright on background music
Pre-show music should be royalty-free. Spotify / Apple Music streams will be muted on YouTube. Use Epidemic Sound / Artlist.

### Captioning sync
AI captions (Otter.ai, AWS Transcribe) have 2-5 sec delay. CART (human) is real-time. Use CART for production; AI fallback. See `accessibility-ada-captioning-interpretation`.

### Multi-track download
Some streaming platforms (StreamYard) only export single combined recording. For post-event editing flexibility, use Riverside Studio (separate tracks) OR OBS (record each scene to file).

### Streaming on cellular only
If venue forbids wifi, LiveU LU800 with 4-card bonded cellular = 8-12 Mbps stable. Single-card 5G = 50-100 Mbps but variable.

### Stream falling behind
If encoder can't keep up (CPU bottleneck), reduce resolution/bitrate. Monitor OBS stats panel during stream.

### Backup stream URL
Some platforms allow backup stream key (failover). Restream supports auto-failover from primary to backup URL.

## Sources

- **Restream**: https://restream.io | API: https://developers.restream.io
- **StreamYard**: https://streamyard.com
- **Riverside Studio**: https://riverside.fm | API: https://riverside.fm/api
- **OBS Studio**: https://obsproject.com | docs: https://obsproject.com/wiki
- **vMix**: https://www.vmix.com
- **Wirecast**: https://www.telestream.net/wirecast
- **LiveU LU800**: https://liveu.tv/products/lu800
- **YouTube Live**: https://support.google.com/youtube/answer/2474026
- **Vimeo Live**: https://vimeo.com/live
- **Demio**: https://demio.com
- **Livestorm**: https://livestorm.co
- **Zoom Events**: https://www.zoom.us/events
- **MS Teams Live Events**: https://learn.microsoft.com/en-us/microsoftteams/teams-live-events
- **Webex Events**: https://www.webex.com/webinars
