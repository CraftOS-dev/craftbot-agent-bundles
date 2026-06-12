<!--
Source: https://podpitch.com/
Castfox 2026 buyer guide: https://www.castfox.net/blog/best-podcast-outreach-tools-2026
Podchaser: https://www.podchaser.com/
MatchMaker: https://matchmaker.fm/
-->
# Podcast Tour Booking for Execs — SKILL

PodPitch (3.85M podcast DB, daily-refreshed, AI pitch generation citing host's recent episodes) is the default. Podchaser Pro = "IMDB of podcasts" with audience metrics. MatchMaker.fm = guest-host match-making. PodPitch pricing $199-$299/mo. Pair with `youtube-mcp-transcript` for episode research and `mcp-tts` for spokesperson drill.

## When to use this skill

- **Quarterly podcast tour** — 2-4 appearances/month for a CEO or domain-expert exec.
- **Book launch / Series B / major launch** — burst of 8-12 podcasts in a 4-week window.
- **New exec personal-brand build** — sustained 12-month cadence to grow audience.
- **Vertical-specific outreach** — niche industry podcasts where exec is genuinely expert.
- **Cross-promote owned podcast** — invite hosts of larger pods as guests on yours.

**Do NOT use this skill when:**
- The "podcast" is a single Spotify-exclusive episode for branded content (use marketing-agent).
- The exec is unprepared (high-stakes appearances need `media-training-spokesperson-prep` first).
- The pod has <1K listeners and no platform value (waste of exec time).

## Setup

### PodPitch API

```bash
# Sign up at https://podpitch.com — $199-$299/mo per guest profile
export PODPITCH_API_KEY="<key>"
export PODPITCH_API_BASE="https://api.podpitch.com/v1"
export PODPITCH_GUEST_ID="<guest-profile-id>"
```

### Podchaser Pro API (audience metrics)

```bash
# https://www.podchaser.com/pro — $299/mo for API access
export PODCHASER_API_KEY="<key>"
export PODCHASER_API_BASE="https://api.podchaser.com/graphql"
```

### MatchMaker.fm

Free tier available; mostly UI-driven, limited API. Profile-based matching.

### Notion outreach DB schema

Per podcast row:
- `pod_name` (text)
- `host` (text)
- `pod_rss_url` (url)
- `pod_apple_url` (url)
- `pod_spotify_url` (url)
- `episode_count` (number)
- `avg_downloads_per_episode` (number)
- `audience_demo` (rich text)
- `recent_guests` (multi-text — last 10)
- `host_recurring_topics` (multi-text)
- `pitch_date` (date)
- `pitch_status` (select: pitched, accepted, declined, no-reply, recorded, published)
- `recording_date` (date)
- `publish_date` (date)
- `episode_url` (url)
- `youtube_transcript_url` (url)

### youtube-mcp-transcript

Used to pull host's last 3 episode transcripts for pitch research.

```bash
mcp tool youtube-mcp-transcript.get_transcript --url "https://youtube.com/watch?v=<id>"
```

## Common recipes

### Recipe 1: Discover podcasts via PodPitch filtered search

```bash
# Brief: "Tech-focused podcasts, US/UK, 5K-100K downloads/episode, with founder/exec guests in past 6 months"

curl -X POST "$PODPITCH_API_BASE/podcasts/search" \
  -H "Authorization: Bearer $PODPITCH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "categories": ["technology","business","entrepreneurship"],
      "regions": ["US","UK"],
      "downloads_per_episode_min": 5000,
      "downloads_per_episode_max": 100000,
      "guest_type_recent_180_days": ["founder","ceo","cto","executive"],
      "episode_count_min": 50,
      "publishes_monthly_min": 2
    },
    "limit": 100
  }' \
| jq '.podcasts[] | {pod_id, name, host, downloads_avg, last_3_episodes: [.recent_episodes[0:3] | .[] | {title, date, guest}], topical_keywords}' > pod_targets.json
```

### Recipe 2: Cross-check audience metrics in Podchaser Pro

```bash
# GraphQL query for audience signals
curl -X POST "$PODCHASER_API_BASE" \
  -H "Authorization: Bearer $PODCHASER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query { podcast(identifier: { id: \"'$pod_id'\", type: PODCHASER }) { title host listenerEstimate audienceCountry audienceGender averageReviewScore numberOfReviews episodeCount recentEpisodes(first: 5) { title airDate guests { name } } } }"
  }'
```

Use `listenerEstimate` for audience size ground-truth (PodPitch sometimes inflates).

### Recipe 3: Host episode research via youtube-mcp-transcript

```bash
# Find host's YouTube channel
host_yt=$(podchaser query "host=$host_name" | jq -r .youtube_channel)

# Pull last 3 episodes' transcripts
for ep in $(curl -s "https://www.googleapis.com/youtube/v3/search?channelId=$host_yt&order=date&maxResults=3&type=video&key=$YT_API_KEY" | jq -r '.items[].id.videoId'); do
  mcp tool youtube-mcp-transcript.get_transcript --videoId "$ep" > "transcripts/${ep}.txt"
done

# Claude identifies cite-able moments
prompt="Read these 3 podcast transcripts. Identify:
1. Recurring questions the host asks
2. Topics the host repeated across episodes
3. A specific moment that connects to our exec's POV ({exec_pov})
4. Any guest the host invited that overlaps with our space

Output as JSON with episode_url + cite_quote + cite_connection."
analysis=$(claude --files transcripts/ --prompt "$prompt")
```

### Recipe 4: Personalized pitch draft (PodPitch AI or Claude direct)

```python
# Option A: PodPitch AI (faster, baseline quality)
curl -X POST "$PODPITCH_API_BASE/pitches/generate" \
  -H "Authorization: Bearer $PODPITCH_API_KEY" \
  -d "{
    \"guest_id\": \"$PODPITCH_GUEST_ID\",
    \"target_pod_id\": \"$pod_id\",
    \"talking_points\": [
      \"Our exec just shipped X solving Y\",
      \"Recent data point: Z grew 40% in Q1\",
      \"Customer story: Acme reduced cost 60%\"
    ]
  }"

# Option B: Claude direct (higher quality, cites specific episode moments)
prompt = f"""
Draft a podcast pitch for {exec['name']} to appear on {pod['name']} (host: {pod['host']}).

EPISODE RESEARCH: {episode_analysis}
SPECIFIC MOMENT TO REFERENCE: {episode_analysis['cite_quote']}
EXEC'S POV: {exec['core_pov']}
EXEC RECENT SHIPS: {exec['recent_outputs']}

Format:
- Subject (under 49 chars): "<pod_name> guest pitch: <our angle>"
- Line 1: cite specific moment from a recent episode by URL
- Line 2: connect to our exec's POV
- Line 3: propose specific topic gap
- Line 4: 50-word bio + 2 prior podcast links (recent_media)
- Line 5: 15-min preview call CTA

Total under 200 words. No banned openers. No buzzwords.
"""
pitch = claude(prompt)
```

### Recipe 5: Send pitch via gmail-mcp

```bash
host_email=$(podchaser query "pod_id=$pod_id" | jq -r .host_email)

# Some hosts use producers; check first
if [[ -z "$host_email" ]]; then
  host_email=$(echo "$pod" | jq -r .producer_email)
fi

gmail-mcp send \
  --to "$host_email" \
  --subject "$subject" \
  --body "$pitch"

# Log to Notion
notion-mcp update_row --filter "pod_name=$pod_name" \
  --pitch_date "$(date -I)" \
  --pitch_status "pitched"
```

### Recipe 6: Booking calendar workflow

```bash
# On acceptance reply
google-calendar-mcp create_event \
  --title "$exec name on $pod_name (recording)" \
  --start_time "$recording_dt" \
  --duration_min 60 \
  --description "Pod: $pod_name | Host: $host | Topic: $topic | Episode URL: TBD" \
  --attendees "$host_email,$exec_email,$pr_lead_email"

# Schedule prep (1 week before)
google-calendar-mcp create_event \
  --title "PREP: $pod_name (1hr)" \
  --start_time "$(date -d "$recording_dt - 7 days" -I)" \
  --duration_min 60 \
  --description "Listen to host's last 3 eps via youtube-mcp-transcript. Mock interview via media-training-spokesperson-prep."
```

### Recipe 7: Pre-appearance prep (hand off to media-training skill)

```bash
# Call media-training-spokesperson-prep skill for full prep
# Inputs:
# - pod['name'], pod['host'], pod['recent_episodes']
# - exec key messages
# - mcp-tts audio drill

# Specific to podcasts:
# 1. Listen to host's last 3 episodes for cadence + style
# 2. Note host's verbal tics, common pivots, what triggers them
# 3. Identify host's "go-to" follow-up question pattern
# 4. Have exec practice in same audio format (sit-down, headphones, recorded)
```

### Recipe 8: Post-appearance repurposing

```bash
# 1. Pull recording transcript
mcp tool youtube-mcp-transcript.get_transcript --url "$episode_url" > transcript.txt

# 2. Claude identifies quotable moments
prompt="Read this podcast transcript. Pull 5-8 quotable moments (15-60 seconds each).
For each: timestamp + transcript snippet + why it's quotable + recommended channel (LinkedIn / Twitter / Substack)."
quotables=$(claude --file transcript.txt --prompt "$prompt")

# 3. Generate LinkedIn post per quotable
for q in $(echo "$quotables" | jq -c '.[]'); do
  linkedin_post=$(claude --prompt "Draft LinkedIn post from this podcast quote: $q. Include timestamp + episode link.")
  notion-mcp create_page --db editorial_calendar --properties "linkedin_post=$linkedin_post"
done

# 4. Generate clipped video segments (hand to video-creator agent if exists)
# OR: render 60-sec audio clip via ffmpeg
ffmpeg -i full_episode.mp3 -ss $start -to $end -c copy clip.mp3

# 5. Thank-you note to host (relationship-building)
gmail-mcp send --to $host_email \
  --subject "Thank you — $pod_name episode" \
  --body "Loved the conversation about [specific topic]. Sharing on LinkedIn this week. If your audience would ever benefit from a follow-up, my door's open."

# 6. Offer host as guest on company podcast if applicable
```

## Examples — quarterly podcast tour

```yaml
exec: Jane Smith, CEO Acme
goal: 12 appearances in Q3 (4/month)
target_audience: 5K-50K downloads/episode, tech / SaaS / AI / entrepreneurship

week_-12 (pre-tour):
  - PodPitch search for 60 candidate podcasts
  - Podchaser audience-cross-check; cut to 30
  - Claude episode research per top 30 via youtube-mcp-transcript
  - Rank by topical fit + audience demo + host responsiveness

week_-10 to -8:
  - Send 30 personalized pitches via gmail-mcp (5/week)
  - Track acceptance + decline + no-reply

week_-6 to -4:
  - Follow up no-reply pods with fresh hook
  - Confirm bookings for Q3 (typically 12-15 accepts from 30 pitches)
  - Schedule recordings via google-calendar-mcp

week_0 to +12 (during tour):
  - Per appearance: 1hr prep + 1hr recording + 30-min post-recording debrief
  - Mock interview 24-48 hrs before each
  - mcp-tts drill morning-of

post_each:
  - Pull transcript via youtube-mcp-transcript
  - Repurpose to LinkedIn + Substack + X
  - Thank-you note to host
  - Update Notion: published episode_url + initial download trajectory

quarterly_review:
  - Top-performing topics (which episodes earned most repurpose engagement)
  - Top-performing hosts (which led to follow-on opportunities)
  - Pods to re-pitch in Q4
```

## Edge cases

### Sweet-spot audience size
- <5K downloads/episode → low ROI for exec time
- 5K-100K → sweet spot, accept-rate high, audience quality good
- 100K-1M → harder to land, more competitive, worth pursuing for top 3-5/quarter
- >1M (Joe Rogan, Lex Fridman, Tim Ferriss tier) → year-long landing strategy, separate skill

### Host's last 3 episodes = mandatory research
Don't pitch a host you haven't listened to. Generic pitches die. The first line MUST cite a specific moment.

### Producer vs host pitch routing
Bigger podcasts have producers handling booking. Smaller podcasts: pitch host directly. Mid-tier: try producer first, fallback to host if no response in 7 days.

### Decline ≠ permanent no
A "not now" is "ask again in 6 months." Track in Notion `pitch_status=declined` + `re_pitch_after: 6mo`.

### Topical fit > audience size
A 10K-download podcast where 100% of listeners are your buyer persona beats a 100K-download general podcast. Filter by topical fit FIRST, audience second.

### Recording prep is mandatory
Don't ship execs to recordings unprepared. 1 hour of prep saves 60 minutes of cringe in playback. Use `media-training-spokesperson-prep` skill end-to-end before any tier-1 podcast.

### Recording quality matters
Audio quality = listener retention. Brief exec:
- Quiet room
- Wired headphones (Bluetooth = audio dropouts)
- USB condenser mic (Yeti, Shure MV7) — never laptop mic
- Test 3 days before
- Tech check 30 min before recording

### What if exec is bad on audio?
- After first appearance, listen back and identify weaknesses
- Schedule more drills via `mcp-tts` before next appearance
- If unfixable: route exec to print interviews, not podcasts
- Or: train another exec who's better on audio

### MatchMaker.fm vs PodPitch decision
- **PodPitch**: best for outbound — agent does the work
- **MatchMaker.fm**: best for inbound — exec creates profile, hosts find them
- Use both. PodPitch for proactive booking, MatchMaker for inbound opportunities.

### Recording time zones
Cross-timezone podcasts (US ↔ UK ↔ APAC) — be careful with morning brain on exec side. Best window: 9-11am exec local time.

### Cross-podcast repurposing consistency
Same key message across all podcast appearances. Different angles, same core story. Listeners who hear exec on 3 different shows in a month should hear consistent POV.

### Owned podcast bilateral
If Acme has its own podcast, offer the host of every show exec appears on as a guest on Acme's pod. Bidirectional relationship doubles future opportunity.

### Video vs audio-only
Many podcasts now record video too (YouTube + Spotify Video). Brief exec on visual presentation:
- Lighting (window-facing or ring light)
- Backdrop (clean, branded, no laundry)
- Camera at eye level
- Eye contact with camera, not screen

### Sponsor disclosure
If exec mentions Acme product/customer in the conversation, ensure host knows it's not a sponsored placement (unless it is and is disclosed). FTC requires clear disclosure of paid sponsorship.

### After-action podcast metrics
30-day post-publish:
- Download trajectory (host shares)
- Comments / engagement
- Web traffic referrals (UTM tag any links shared in episode notes)
- New email subscribers from episode CTA
- Tag in `posthog-mcp` to track post-podcast site visits

Use these to rank pods for re-pitch next year.

## Sources

- **PodPitch**: https://podpitch.com/
- **Castfox 2026 podcast outreach guide**: https://www.castfox.net/blog/best-podcast-outreach-tools-2026
- **Podchaser Pro API**: https://www.podchaser.com/api
- **MatchMaker.fm**: https://matchmaker.fm/
- **YouTube Data API**: https://developers.google.com/youtube/v3
- **role.md podcast booking playbook**: internal
