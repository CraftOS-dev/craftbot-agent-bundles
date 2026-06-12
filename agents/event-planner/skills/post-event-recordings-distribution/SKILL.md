<!--
Sources:
- OpenAI Whisper: https://openai.com/research/whisper
- YouTube Data API: https://developers.google.com/youtube/v3
- Vimeo API: https://developer.vimeo.com
- Descript API: https://www.descript.com
- SmugMug API: https://api.smugmug.com
- Pixieset: https://pixieset.com
- Buzzsprout API: https://www.buzzsprout.com/api
- Spotify for Podcasters: https://podcasters.spotify.com
- Captiwise / Rev API: https://www.rev.com/api
-->
# Post-Event Recordings Distribution — SKILL

End-to-end distribution pipeline: raw recording capture → transcription → editing → upload to platforms → notification to attendees + speakers + sponsors → analytics tracking. 80% of virtual ticket buyers watch recording, not live; 60% of in-person attendees rewatch favorite sessions. Distribution is half the event value, executed poorly.

## When to use this skill

- Post-event: distributing session recordings to attendees + public
- Generating transcripts for SEO + accessibility + post-event search
- Producing podcast episodes from session recordings
- Building a YouTube channel of past sessions (asset for marketing)
- Delivering photo + video galleries to attendees
- Building post-event content library for repurposing (blog, social, podcast)

**Do NOT use this skill when:**
- Recordings are private / sensitive (closed-door briefings; defer to manual handling)
- Live-broadcast already serves distribution need (rare)
- Long-form post-production beyond podcast (defer to specialist video editor)
- Pure podcast event (use podcast-specific skill in `marketing-agent`)

## Setup

### Tools

- `cli-anything` for Whisper / Descript / Rev / Buzzsprout REST APIs
- `youtube-mcp` for YouTube bulk upload + metadata
- `youtube-mcp-transcript` for verification
- `gmail-mcp` for distribution email to attendees + speakers + sponsors
- `notion-mcp` for recording archive + content library
- `posthog-mcp` for distribution funnel analytics

### Whisper install

```bash
# Via uvx (no install needed)
uvx openai-whisper recording.mp4 --model large-v3 --output_format srt

# Or pip install
pip install openai-whisper
whisper recording.mp4 --model large-v3 --output_format srt --output_dir transcripts/
```

### YouTube API

```bash
# Via youtube-mcp (already in agent.yaml)
# Setup once: OAuth flow to authorize channel
```

### Vimeo API

```bash
export VIMEO_TOKEN="<personal-access-token>"
# Base: https://api.vimeo.com/
```

### Descript API

```bash
export DESCRIPT_TOKEN="<api-key>"
# Base: https://api.descript.com/v1/
```

### Buzzsprout API (podcast hosting)

```bash
export BUZZSPROUT_TOKEN="<api-key>"
export BUZZSPROUT_PODCAST_ID="<podcast-id>"
```

## Common recipes

### Recipe 1: Whisper transcription per session

```bash
# Transcribe all session recordings in parallel
for f in recordings/*.mp4; do
  basename=$(basename "$f" .mp4)
  uvx openai-whisper "$f" \
    --model large-v3 \
    --output_format srt,txt,vtt,json \
    --output_dir "transcripts/$basename" \
    --language en \
    --word_timestamps True &
done
wait
```

Result per session:
- `recording.mp4` (video)
- `transcripts/<session>/<session>.srt` (subtitles for upload)
- `transcripts/<session>/<session>.txt` (full transcript for archive)
- `transcripts/<session>/<session>.json` (word-level timestamps for editing)

### Recipe 2: Speaker correction pass

Whisper accuracy on industry jargon needs human cleanup. Use Descript for text-based editing.

```bash
# Upload transcript to Descript for cleanup
curl -X POST https://api.descript.com/v1/transcripts \
  -H "Authorization: Bearer $DESCRIPT_TOKEN" \
  -F "audio=@recording.mp3" \
  -F "name=Sarah K. Keynote DevConf 2027"

# Descript opens in browser; speaker (or team) reads through, fixes jargon
# Export final transcript when done
```

### Recipe 3: YouTube bulk upload via youtube-mcp

```python
# For each session
sessions = notion.query_db('devconf-2027-recordings')

for s in sessions:
    mcp_tool('youtube.upload_video',
        title=f"{s['speaker']}: {s['title']} — DevConf 2027",
        description=f"""
{s['abstract']}

Recorded at DevConf 2027 in Chicago.

Speaker: {s['speaker']}
Bio: {s['speaker_bio']}
LinkedIn: {s['speaker_linkedin']}

Slides: {s['slides_url']}
Transcript: {s['transcript_url']}

00:00 - Intro
{generate_chapter_timestamps(s['transcript'])}

Subscribe to our channel for more talks.
        """,
        tags=[s['track'], 'DevConf', 'DevConf 2027'] + s['tags'],
        category='Science & Technology',
        playlist=f'DevConf 2027 - {s["track"]}',
        privacy='public',
        thumbnail_url=s['thumbnail_url'],
        subtitles_file=s['srt_path'],
        recorded_date=s['session_date'],
        publish_at=s['publish_date']  # schedule embargo
    )
```

### Recipe 4: Vimeo upload (premium / gated)

For premium content or sponsor-gated recordings:

```bash
curl -X POST https://api.vimeo.com/me/videos \
  -H "Authorization: Bearer $VIMEO_TOKEN" \
  -d '{
    "upload": {"approach": "tus", "size": $(stat -c%s recording.mp4)},
    "name": "Sarah K. Keynote DevConf 2027",
    "description": "...",
    "privacy": {"view": "password", "password": "DEVCONF2027"},
    "embed": {"playbar": true, "color": "#0066CC", "logos": {"vimeo": false}}
  }'
```

### Recipe 5: Photo gallery delivery (SmugMug / Pixieset)

```bash
# SmugMug
curl -X POST https://api.smugmug.com/api/v2/album! \
  -H "Authorization: OAuth $SMUGMUG_TOKEN" \
  -d '{
    "Title": "DevConf 2027 — Day 1 Photos",
    "Privacy": "Unlisted",
    "Password": "DEVCONF2027"
  }'

# Bulk upload photos
for photo in photos/*.jpg; do
  curl -X POST https://upload.smugmug.com/ \
    -H "X-Smug-AlbumUri: /api/v2/album/$ALBUM_ID" \
    -H "X-Smug-Title: $(basename $photo)" \
    --data-binary @"$photo"
done

# Pixieset alt (cleaner client gallery UX)
# Login → New Gallery → Drop photos → Set client password → Share URL
```

### Recipe 6: Podcast episode generation per session

```bash
# Extract audio + chapters
ffmpeg -i recording.mp4 -vn -acodec mp3 -ab 192k audio/$session.mp3

# Generate chapter markers from Whisper timestamps
python generate_chapters.py transcripts/$session/$session.json > chapters/$session.txt

# Upload to Buzzsprout
curl -X POST https://www.buzzsprout.com/api/$BUZZSPROUT_PODCAST_ID/episodes \
  -H "Authorization: Token token=$BUZZSPROUT_TOKEN" \
  -F "title=$EPISODE_TITLE" \
  -F "description=$EPISODE_DESC" \
  -F "audio_file=@audio/$session.mp3" \
  -F "tags=DevConf,AI,Engineering" \
  -F "published_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Buzzsprout auto-distributes to Spotify / Apple Podcasts / Google Podcasts
```

### Recipe 7: Attendee distribution email (Day 7)

```python
attendees = notion.query_db('devconf-2027-attendees', filter={'attended': True})
for a in attendees:
    body = render_template('attendee_recording_email.md',
        attendee=a,
        attended_sessions=get_attended(a),
        gallery_url='https://pixieset.com/devconf-2027/?p=DEVCONF2027',
        youtube_playlist='https://youtube.com/playlist?list=devconf-2027'
    )
    mcp_tool('gmail.send_email',
             to=a['email'],
             subject='DevConf 2027 recordings + photos + slides',
             body=body)
```

```markdown
# Email template — attendee_recording_email.md

Hi [first name],

Recordings from DevConf 2027 are ready. We've also put together the photo gallery and slide decks.

## Your sessions
- [Session 1: Sarah K. Keynote — watch](youtube://...)
- [Session 2: Building Frontier Teams panel — watch](youtube://...)
- [Session 3: ...]

## All recordings (YouTube playlist)
[Full playlist](https://youtube.com/playlist?list=devconf-2027)

## Photo gallery
[View + download](https://pixieset.com/devconf-2027/?p=DEVCONF2027)

## Slide decks
- [Sarah K. — AI Infrastructure at Scale](pdf://...)
- [...]

## Podcast version
We've also released audio-only episodes for podcast listeners.
[Listen on Spotify](spotify://...) | [Apple Podcasts](apple://...)

## Year-over-year content
Browse past DevConf talks: [youtube.com/devconf](https://youtube.com/devconf)

Thanks for being part of DevConf 2027.

[Team]
```

### Recipe 8: Sponsor branded post-event distribution

For sponsors, custom report + recording link:

```python
for sponsor in sponsors:
    body = render_template('sponsor_recording_email.md',
        sponsor=sponsor,
        sponsor_session_url=sponsor.get('session_recording_url'),
        leads_summary=cvent.get_lead_summary(sponsor_id=sponsor.id),
        full_recording_playlist='https://youtube.com/playlist?list=devconf-2027'
    )
    mcp_tool('gmail.send_email',
             to=sponsor['contact_email'],
             subject=f'{sponsor["name"]} @ DevConf 2027 — recordings + leads',
             body=body,
             attachment=f'sponsor-{sponsor["id"]}-leads.csv')
```

### Recipe 9: Speaker recording + assets package

```python
for speaker in speakers:
    body = render_template('speaker_recording_email.md',
        speaker=speaker,
        recording_url=speaker['recording_url'],
        recording_views_7d=youtube.get_views(speaker['video_id']),
        attendance_count=session_attendance.get(speaker['session_id']),
        nps_score=session_nps.get(speaker['session_id']),
        verbatim_quotes=top_verbatims(speaker['session_id'])
    )
    mcp_tool('gmail.send_email',
             to=speaker['email'],
             subject=f'Your DevConf 2027 talk is live — recording + analytics',
             body=body)
```

### Recipe 10: Post-event content repurposing (handoff to marketing)

```python
# Identify top sessions for marketing repurposing
top_sessions = postgres.query("""
    SELECT s.session_id, s.title, s.speaker, 
           sa.attendance_pct, sr.avg_rating, yt.views_7d
    FROM sessions s
    JOIN session_attendance sa USING(session_id)
    JOIN session_ratings sr USING(session_id)
    JOIN youtube_recordings yt USING(session_id)
    WHERE s.event_id = 'devconf-2027'
    ORDER BY sa.attendance_pct DESC, sr.avg_rating DESC
    LIMIT 5
""")

# Hand off to marketing-agent
mcp_tool('agent_call.marketing-agent',
         payload={'top_sessions': top_sessions,
                  'task': 'Build blog series + social cascade from top 5 sessions',
                  'transcripts': {s.id: s.transcript for s in top_sessions}})
```

## Examples

### Example A: 25-session conference distribution timeline

```
T+0 (event ends): Stop recordings
T+1d: Photographer uploads photos to Pixieset; raw photos available
T+2d: Bulk Whisper transcription kicked off (parallel; ~30 min total)
T+3d: Speaker QC pass on transcripts via Descript
T+4d: Bulk YouTube upload (scheduled publish T+7d)
T+5d: Audio-only podcast episodes generated + uploaded to Buzzsprout
T+6d: Attendee distribution email drafted + reviewed
T+7d: Public release — YouTube playlist live + podcast live + attendee email sent
T+10d: Sponsor branded reports sent
T+14d: Speaker recording + analytics emails sent
T+21d: Top-5 sessions handed to marketing for blog cascade
```

### Example B: Single keynote distribution (smaller event)

```
T+1d: Recording cut from main camera (no multi-cam edit)
T+2d: Whisper transcript + speaker review
T+3d: YouTube upload (public)
T+4d: Attendee email + LinkedIn announcement
T+7d: Podcast episode released
T+14d: Blog post repurposing transcript
```

### Example C: Gated premium content (Vimeo password)

```
T+1d: Recording uploaded to Vimeo with password
T+2d: Transcript not made public; archived in Notion only
T+3d: Email to paid-attendees with Vimeo URL + password
T+30d: Recordings removed from Vimeo (limited-window value)
T+60d: Highlight clips (1-2 min) shared on social as teaser
```

## Edge cases

### Multi-language transcription
Whisper supports 99 languages. For multi-language events, use `--language auto` and Whisper detects per session. For DeepL post-translation, see `deepl-mcp`.

### Speaker rights conflict
Some speakers (especially keynote bureau) restrict recording distribution. Check speaker agreement (see `speaker-management-sourcing-prep`). For restricted recordings: gated only, no public YouTube.

### Sponsor branded content
Some sponsors want their session's recording behind their own gated portal. Provide private Vimeo link + transcript + slides; sponsor distributes from their side.

### YouTube copyright strike
Royalty-free music in recording (intro/outro) sometimes triggers Content ID. Pre-event: use Epidemic Sound / Artlist with declared license. If strike: dispute via YouTube Studio.

### Transcript SEO
Embed transcript on event website page per session for SEO ranking. Use schema.org `VideoObject` markup. Increases organic traffic 3-5x.

### Audio quality on remote speakers
Virtual speakers sometimes have poor audio (built-in mic, noisy room). Use Descript Studio Sound to enhance. For unfixable audio: caption-only release.

### Recording lengths
Trim recordings to actual session duration (avoid 30 min of "speaker setup" pre-talk). Use ffmpeg + transcript timestamps.

### YouTube thumbnail
Default YouTube thumbnail is auto-generated frame. Custom thumbnails (per speaker headshot + session title) increase CTR 2-3x. Generate via `canva-mcp` template.

### Attribution in transcripts
Multi-speaker sessions need speaker labels in transcript. Whisper alone doesn't speaker-diarize; use pyannote-audio OR Riverside's built-in diarization for separate-track audio.

### Distribution privacy
For internal-only events, do NOT upload to public YouTube. Use Vimeo private + password, OR self-hosted via S3 + signed URLs.

### Recording archive in event hub
Archive all recordings in `notion-mcp` event hub with full metadata. Searchable for future reuse + cross-event reference.

### GDPR right to be forgotten
If an attendee or speaker requests removal post-publish, comply within 30 days. Pull from YouTube + Vimeo + transcript archive.

### Recording quality variance
Multi-cam events have varied recording quality. Designate "lead camera" per session for canonical recording; other cams are backup.

## Sources

- **OpenAI Whisper**: https://openai.com/research/whisper | GitHub: https://github.com/openai/whisper
- **YouTube Data API**: https://developers.google.com/youtube/v3
- **Vimeo API**: https://developer.vimeo.com
- **Descript**: https://www.descript.com | API: https://api.descript.com
- **SmugMug API**: https://api.smugmug.com
- **Pixieset**: https://pixieset.com
- **Buzzsprout API**: https://www.buzzsprout.com/api
- **Rev (paid transcription)**: https://www.rev.com/api
- **Spotify for Podcasters**: https://podcasters.spotify.com
- **Epidemic Sound (royalty-free music)**: https://www.epidemicsound.com
