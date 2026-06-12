<!--
Sources:
- RingCentral Events (Hopin): https://hopin.com/developers
- Brella WebRTC: https://brella.io
- Swapcard: https://www.swapcard.com
- Zoom Events: https://www.zoom.us/events
- Airmeet: https://www.airmeet.com
- Zuddl: https://www.zuddl.com
- WebRTC Standards: https://webrtc.org
- Slido API: https://www.slido.com/api
- Pigeonhole Live: https://www.pigeonhole.at
-->
# Hybrid Event Low-Latency Interaction — SKILL

WebRTC sub-second latency stack for hybrid events where in-room AND virtual attendees interact together. Standard HLS streaming (8-15 sec latency) breaks interactivity — by the time virtual asks a question, in-room moved on. WebRTC bridges both audiences in real time. Pair with platform-side Q&A (Slido / Pigeonhole) for moderated flow + recording.

## When to use this skill

- Hybrid conference with real-time Q&A across in-room + virtual audiences
- Hybrid customer summit with virtual breakout room participation
- Hybrid panel with mixed in-person + remote panelists
- Hybrid networking event where virtual + in-person attendees match + meet
- Hybrid town hall / all-hands with live polling + word cloud
- Sub-second latency requirement (gaming demos, music collab, code pair-program demos)

**Do NOT use this skill when:**
- Pure broadcast (no virtual interaction needed) → use `live-streaming-restream-obs-streamyard`
- Asynchronous virtual attendance (watch recording later) — same skill, normal latency OK
- Pure in-person event with optional virtual stream (low-stakes virtual = use HLS)
- Cost-sensitive event without WebRTC budget (use standard streaming + chat moderation gap)

## Setup

### Platform decision matrix

| Need | First-stop | Notes |
|---|---|---|
| Full hybrid event experience | RingCentral Events (Hopin) | Most mature WebRTC hybrid stack |
| Networking-first hybrid | Brella | AI matchmaking + 1:1 meetings + WebRTC video |
| B2B trade show hybrid | Swapcard | Combines experience + content + matchmaking |
| Enterprise hybrid + branded | Zoom Events | Enterprise security + branding |
| AI matchmaking + virtual networking | Airmeet | India-headquartered, virtual-native |
| Hybrid + enterprise focus | Zuddl | Hybrid + virtual, enterprise focus |
| Q&A integration on top | Slido (Cisco) or Pigeonhole | Moderated Q&A overlays |

### Tools

- `cli-anything` for RingCentral Events (Hopin) / Brella / Swapcard / Zoom Events REST API
- `zoom-mcp` for Zoom Events
- `slack-mcp` for day-of stream ops + virtual host channel
- `notion-mcp` for cross-audience speaker DB + run-of-show

### RingCentral Events (Hopin) API

```bash
export HOPIN_TOKEN="<api-key>"   # Hopin > Settings > Developer
# Base: https://hopin.com/api/v1/
```

### Brella API

```bash
export BRELLA_TOKEN="<api-key>"
# Base: https://api.brella.io/v1/
```

### Slido API (for Q&A overlays)

```bash
export SLIDO_TOKEN="<api-key>"   # Enterprise tier required
# Base: https://api.slido.com/v1/
```

## Common recipes

### Recipe 1: RingCentral Events (Hopin) full hybrid setup

```bash
# 1. Create event
curl -X POST https://hopin.com/api/v1/events \
  -H "Authorization: Bearer $HOPIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "DevConf 2027 — Hybrid Edition",
    "startTime": "2027-09-15T08:00:00-05:00",
    "endTime": "2027-09-17T18:00:00-05:00",
    "timezone": "America/Chicago",
    "description": "Mid-tier dev conference, in-person + virtual.",
    "format": "hybrid",
    "venue": {
      "name": "Hilton Chicago",
      "address": "720 S Michigan Ave"
    },
    "branding": {
      "logoUrl": "https://devconf.io/logo.svg",
      "primaryColor": "#0066CC"
    },
    "ticketing": {
      "tiers": [
        {"name": "In-Person", "price": 899, "limit": 600},
        {"name": "Virtual", "price": 199, "limit": 5000}
      ]
    }
  }'

# 2. Configure stages (one per parallel track)
curl -X POST https://hopin.com/api/v1/events/$EVENT_ID/stages \
  -d '{
    "name": "Main Stage",
    "streamUrl": "rtmp://venue-encoder.local/live/devconf",  # from OBS
    "audience": "both",  # in-person + virtual see
    "webrtcEnabled": true,
    "qaSource": "slido",
    "slidoSessionId": "ABC123"
  }'

# 3. Configure expo (sponsor booths) — virtual + in-person sponsors
curl -X POST https://hopin.com/api/v1/events/$EVENT_ID/expo \
  -d '{
    "sponsors": [
      {"name": "Datadog", "boothType": "virtual", "videoChat": true},
      {"name": "Linear", "boothType": "hybrid", "inPersonBooth": "Lobby 1"}
    ]
  }'

# 4. Networking config (Brella-like matchmaking)
curl -X POST https://hopin.com/api/v1/events/$EVENT_ID/networking \
  -d '{
    "enabled": true,
    "videoChatDuration": 5,    # 5 min speed networking
    "interests": ["AI/ML", "Infra", "Frontend", "DevOps"]
  }'
```

### Recipe 2: Q&A bridge (Slido) overlaid on RingCentral Events

```bash
# Slido session integrates across in-room and virtual audiences
# Both audiences submit + upvote via slido.com/<event-code>
# Moderator queue managed by virtual host

# Create Slido session
curl -X POST https://api.slido.com/v1/events/$EVENT_ID/sessions \
  -H "Authorization: Bearer $SLIDO_TOKEN" \
  -d '{
    "name": "DevConf Main Stage Q&A — Day 1",
    "code": "DEVCONF1",
    "qa": {"moderation": "review_before_publish"},
    "polls": [
      {"type": "multiple_choice", "question": "How do you deploy LLMs?",
       "options": ["Bedrock", "Anthropic API", "OpenAI", "Self-hosted"]}
    ]
  }'

# Embed Slido URL in:
# - Main stage slide deck (lower-third URL)
# - In-room signage (printed QR + URL)
# - Hopin / RingCentral virtual portal (auto-embedded via slidoSessionId)
```

### Recipe 3: WebRTC video bridge (virtual audience member joins on-stage)

For hybrid panel with virtual audience question via webcam:

```bash
# 1. Virtual attendee raises hand in Hopin chat
# 2. Producer approves; promotes attendee to "presenter" role temporarily
curl -X POST https://hopin.com/api/v1/events/$EVENT_ID/promotions \
  -d '{
    "attendeeId": "att_abc123",
    "role": "presenter",
    "duration": 300,  # 5 min
    "stage": "main-stage"
  }'

# 3. Attendee's webcam + audio now appear on main stage stream
# 4. In-room MC + on-stage panelists hear/see them via venue audio + monitor
# 5. After 5 min OR on producer cue, promotion auto-revokes
```

### Recipe 4: Zoom Events for enterprise hybrid

```bash
mcp tool zoom.create_event \
  --topic "Acme Customer Summit 2027 Hybrid" \
  --type "hub_event" \
  --start "2027-09-15T08:00:00-05:00" \
  --duration 480 \
  --hybrid true \
  --in-person-venue "San Francisco" \
  --virtual-cap 2000 \
  --branding-theme "acme" \
  --webinar-features '{"qa": true, "polls": true, "raise_hand": true}'
```

### Recipe 5: Brella for networking-first hybrid

For events where 1:1 video chats matter more than broadcast:

```bash
# Configure WebRTC video chat slots (5-15 min)
curl -X POST https://api.brella.io/v1/events/$EVENT_ID/meetings \
  -d '{
    "videoChatEnabled": true,
    "slotDuration": 10,  # minutes
    "modalities": ["video", "audio_only", "text"],
    "matchmaking": {
      "interests": ["AI/ML", "Hiring", "Investing"],
      "suggestedMeetings": 8  # per attendee
    }
  }'
```

### Recipe 6: Run-of-show with cross-audience cue triggers

```markdown
# Cross-Audience Run-of-Show

| Time | Item | In-Room MC Cue | Virtual Host Cue | A/V |
|------|------|----------------|-------------------|-----|
| 9:00 | Welcome (in-room) | "Welcome to DevConf 2027 in-person..." | Mute mic; type intro in chat | Stream to YouTube Live |
| 9:02 | Welcome (virtual) | Yield to virtual host | "And welcome virtual attendees from 47 countries..." | Switch camera to "virtual host" cam |
| 9:05 | Keynote intro | "Welcome Sarah K." | (silent, monitoring chat) | Lower-third + music in |
| 9:36 | Q&A (in-room first) | "First question from the room..." | Pre-screen 2 virtual questions in Slido | Wide audience cam |
| 9:42 | Q&A (virtual bridge) | Yield to virtual host | "Maya from London asks..." (read from Slido) OR "Maya, can you turn on camera?" | WebRTC promote Maya |
| 9:45 | Transition | "Quick break, back in 5" | "Virtual attendees: check the lounge for networking" | Music in, stream to break slide |
```

### Recipe 7: Captioning across audiences

```bash
# Hybrid events MUST have captioning visible to both in-room (overlay on stream) and virtual (caption track)
# CART (human captioning) via Aberdeen / 3PlayMedia provides real-time
# AI fallback: Otter.ai or AWS Transcribe (2-5 sec delay)

# Configure caption overlay on stream
mcp tool ai-media.start_caption_stream \
  --event-id "devconf-2027" \
  --content-brief "https://us.com/content-brief.md" \
  --display-mode "overlay" \
  --stream-url "rtmp://venue.local/live"

# See accessibility-ada-captioning-interpretation for full setup
```

### Recipe 8: Multi-region virtual hubs (hybrid + multi-city)

For multi-city hybrid (e.g., "in-person hubs in NYC + London + Tokyo + virtual"):

```bash
# Each hub has local in-room + local virtual host
# Hubs sync via Zoom Events / Hopin for synchronized stream
# Time-zone-aware scheduling per hub

curl -X POST https://hopin.com/api/v1/events/$EVENT_ID/hubs \
  -d '{
    "hubs": [
      {"name": "NYC", "venue": "Brooklyn Navy Yard", "timezone": "America/New_York"},
      {"name": "London", "venue": "Tobacco Dock", "timezone": "Europe/London"},
      {"name": "Tokyo", "venue": "Roppongi Academy", "timezone": "Asia/Tokyo"}
    ],
    "sharedKeynote": "2027-09-15T14:00:00Z"  # UTC anchor
  }'
```

### Recipe 9: Speed networking (WebRTC video round-robin)

```bash
# 5-min speed networking blocks where attendees auto-paired
curl -X POST https://hopin.com/api/v1/events/$EVENT_ID/speed-networking \
  -d '{
    "duration": 60,  # total session
    "matchDuration": 5,  # per match
    "matchingMethod": "interest_based"
  }'
```

## Examples

### Example A: 600-attendee + 2000-virtual hybrid conference

```
Platform: RingCentral Events (Hopin)
In-room: OBS multi-cam → Hopin ingest (RTMP)
Virtual viewer experience: Hopin web/app
Latency: WebRTC sub-second on stage + 8-15 sec HLS to YouTube backup
Q&A: Slido (works for both audiences)
Networking: Brella (WebRTC 1:1 video chat)
Sponsor expo: Hopin sponsor booths (virtual) + in-person booth layout
Recording: native Hopin + OBS local
Cost: $20K-$50K all-in
```

### Example B: Single keynote hybrid (executive briefing, 100 in-room + 500 virtual)

```
Platform: Zoom Events (enterprise tier)
In-room: single-cam + lapel mic
Virtual: web embed
Q&A: Zoom native Q&A
Latency: 1-2 sec WebRTC native
Recording: auto-saved to Zoom cloud
Cost: $5K + Zoom Events license ($1K/yr)
```

### Example C: Multi-city virtual hub conference (4 cities)

```
Platform: Hopin (multi-hub support)
Each city: local AV team + local in-room MC
Shared keynote: broadcast from "lead" city (NYC) to all others
Local breakouts: parallel content per city
Synchronized Q&A: Slido per session, attendees from any city can ask
Networking: Brella with city tag filter (find matches locally OR globally)
Cost: $100K-$200K (4 venues + AV teams + central tech)
```

## Edge cases

### WebRTC behind corporate firewall
Many corporate firewalls block WebRTC TURN/STUN. Pre-event, send IT briefing to attendee companies with required ports. Fallback: HLS-only viewing for those who can't WebRTC.

### Virtual attendee's webcam not working
When promoting virtual attendee to on-stage role, their camera may not initialize. Have audio-only fallback ("Maya is audio only — go ahead Maya").

### Audio echo with in-room speakers
If virtual attendee's audio plays from venue speakers, their mic picks it up + echoes. Use noise-canceling headphones for virtual attendees on-stage; monitor for echo.

### Mic feedback during virtual handoff
When in-room MC hands to virtual host (or vice versa), both can be unmuted briefly. Producer manages mute cues actively.

### Caption delay between audiences
CART captions appear instantly for in-room (LED display); virtual audience sees them in stream with stream latency. Acceptable but document.

### Sponsor virtual booth abandonment
Virtual sponsor booths underperform vs in-person (lower foot traffic, lower stickiness). Set expectations: virtual booth value is asynchronous + scheduled meetings, NOT walk-up traffic.

### Time-zone-friendly programming
For multi-region hybrid, run keynote at compromise time (NYC 9am = London 2pm = Tokyo 10pm). Repeat keynote for APAC if needed.

### Virtual attendee fatigue
Virtual attendance falls off after 2-3 hours. Build in shorter sessions + more breaks for virtual track. Consider running shorter virtual-only day.

### Asynchronous "virtual attendees" who watch recording
80%+ of virtual ticket buyers watch recording, not live. Plan post-event distribution accordingly. See `post-event-recordings-distribution`.

### Bandwidth at venue
For hybrid, venue needs ≥500 Mbps wired uplink reserved for stream + WebRTC. Test 72 hours before. Cellular backup via LiveU LU800.

### Latency mismatch between Q&A platforms
Slido Q&A appears nearly instant to both audiences. Native platform Q&A (Hopin chat) has 1-2 sec lag. Choose one Q&A source per stage; don't mix.

### Privacy / consent for promoted virtual attendees
When promoting attendee to on-stage role, get explicit consent + name pronunciation. Some attendees prefer text-only Q&A.

### Cost spike from WebRTC overrun
WebRTC consumes more bandwidth than HLS. Multi-cam + many virtual attendees = high egress cost. Budget for $0.05-$0.10 per attendee-hour of WebRTC.

## Sources

- **RingCentral Events (Hopin)**: https://hopin.com | API: https://hopin.com/developers
- **Brella**: https://brella.io
- **Swapcard**: https://www.swapcard.com | API: https://developers.swapcard.com
- **Zoom Events**: https://www.zoom.us/events
- **Airmeet**: https://www.airmeet.com
- **Zuddl**: https://www.zuddl.com
- **WebRTC**: https://webrtc.org
- **Slido API**: https://www.slido.com/api
- **Pigeonhole Live**: https://www.pigeonhole.at
- **AI-Media (Ai-Live captioning)**: https://www.ai-media.tv
