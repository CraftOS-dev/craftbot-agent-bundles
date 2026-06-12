# Podcast Editing Brief — Descript / Riverside

> Hand off a fully scoped editing brief to Descript (timeline edits, transitions, levels, chapters) after pulling source media from Riverside.

## When to use

Trigger on: "edit my podcast", "write an editing brief for Descript", "fetch the Riverside session", "import to Descript", "set my podcast audio levels", "cut filler from the episode", "make chapter markers". This skill owns: source fetch from Riverside, AI editing brief authored to spec, Descript media-import API handoff, level/loudness targets (-16 LUFS), chapter markers, transition specs. Editing GUI operations in Descript itself remain manual; the brief gets you 80% of the way and the editor does the timeline ops. For trailers see `podcast-scripting-show-notes` Recipe 7; for repurposing handoff see `repurposing-pipeline-1-to-10`.

## Setup

```bash
# Riverside Business plan API
curl -H "Authorization: Bearer $RIVERSIDE_API_KEY" \
  https://api.riverside.fm/v1/recordings

# Descript media-import + edit-in-partner API
curl -H "Authorization: Bearer $DESCRIPT_API_KEY" \
  https://api.descript.com/v1/projects

# ffmpeg for any manual cuts / loudness normalization
brew install ffmpeg
```

Auth env vars:
- `RIVERSIDE_API_KEY` — Business plan only. Contact sales to enable; not self-serve.
- `DESCRIPT_API_KEY` — Descript settings → integrations → bearer token. Pro+ plan.
- `DESCRIPT_DRIVE_ID` — Descript drive (workspace) ID where projects land.

## Common recipes

### Recipe 1: Fetch a Riverside recording session + per-track exports

```bash
# List recent recordings
curl -H "Authorization: Bearer $RIVERSIDE_API_KEY" \
  "https://api.riverside.fm/v1/recordings?limit=10&order=desc" \
  | jq '.data[] | {id, title, created_at, participants:.participants|length}'

# Pull the specific recording with per-participant tracks
RIV_REC_ID="rec_xyz"
curl -H "Authorization: Bearer $RIVERSIDE_API_KEY" \
  "https://api.riverside.fm/v1/recordings/$RIV_REC_ID" \
  | jq '.tracks[] | {participant, format, download_url}'

# Download each track locally
curl -L -o host.wav "<host_track_download_url>"
curl -L -o guest.wav "<guest_track_download_url>"
```

Riverside's API supports `get_recordings`, `get_transcripts`, `delete_recording`. It does NOT support timeline edits — that's the Descript handoff.

### Recipe 2: Pull Riverside transcript (timestamped)

```bash
curl -H "Authorization: Bearer $RIVERSIDE_API_KEY" \
  "https://api.riverside.fm/v1/recordings/$RIV_REC_ID/transcript" \
  > transcript.json

# Convert to timestamped markdown for the brief
jq -r '.segments[] | "[\(.start_seconds | tostring | tonumber | floor / 60 | floor):\(.start_seconds % 60 | floor)] \(.speaker): \(.text)"' transcript.json > transcript.md
```

### Recipe 3: Import media into Descript via API

```bash
# Create a Descript project
curl -X POST https://api.descript.com/v1/projects \
  -H "Authorization: Bearer $DESCRIPT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Episode 042 — edit",
    "drive_id": "'"$DESCRIPT_DRIVE_ID"'"
  }'
# Returns {"id":"proj_abc"}

# Import each track
for TRACK in host.wav guest.wav; do
  curl -X POST https://api.descript.com/v1/projects/proj_abc/media \
    -H "Authorization: Bearer $DESCRIPT_API_KEY" \
    -F "file=@$TRACK" \
    -F "type=audio"
done

# Generate edit-in-partner URL (opens Descript with media loaded)
curl -X POST "https://api.descript.com/v1/projects/proj_abc/edit_url" \
  -H "Authorization: Bearer $DESCRIPT_API_KEY" \
  -d '{"return_url":"https://yoursite.com/post-edit-callback"}' \
  | jq -r .edit_url
```

Send the edit URL to the human editor (or yourself). It auto-loads Descript with media + transcript ready.

### Recipe 4: Editing brief template (the actual deliverable)

```markdown
# Editing Brief: Episode 042 — "Tuesday-6am beats Sunday-night"

## Source files
- Host track: host.wav (Riverside export, 48kHz/24bit, 47:32 duration)
- Guest track: guest.wav (Riverside export, 48kHz/24bit, 47:32 duration)
- Reference transcript: transcript.md (timestamped)
- Pre-write outline: episodes/ep042/brief.md

## Episode target
- Final length: 32-36 min (down from 47:32 raw)
- Final format: MP3 192kbps stereo (podcast), MP4 1080p (YouTube)
- Loudness: -16 LUFS integrated, peak ≤ -1 dBFS

## Cuts (timestamped to source)
- 00:00:00 - 00:01:30 — intro music + host greeting (KEEP, level music to -22 LUFS under voice)
- 00:01:30 - 00:02:15 — false start, guest mic check (CUT)
- 00:02:15 - 00:03:00 — actual cold open hook (KEEP, becomes 00:00 in edit)
- 00:03:00 - 00:05:30 — Pillar 1 setup (KEEP, tighten "um" + "you know")
- 00:08:42 - 00:09:18 — guest off-topic tangent on cooking (CUT)
- 00:23:15 - 00:24:00 — topic turn (KEEP, add 1s dissolve at 00:23:15)
- 00:32:00 - 00:34:20 — hot take (KEEP — DO NOT TRIM, this is the pull-quote moment)
- 00:42:00 - 00:43:30 — sponsor read (KEEP, BGM to -22 LUFS, voice at -16)
- 00:46:00 - 00:47:32 — CTA + outro (KEEP, fade music 2s at end)

## Filler word policy
- Strip: "um", "uh", "like" (when used as filler, NOT when grammatical)
- Keep: "you know", "I mean" — host's verbal cadence; cutting kills personality
- Use Descript's "Filler Word Removal" feature with manual review of every cut

## Levels
- Host voice: -16 LUFS integrated, -1 dBFS peak
- Guest voice: -16 LUFS integrated (normalize to match host)
- BGM intro: -22 LUFS under voice
- Sponsor read BGM: -24 LUFS under voice
- Final integrated: -16 LUFS (Apple Podcasts + Spotify standard)

## Transitions
- Hard cuts default
- One dissolve at the topic turn (00:23:15 → 00:23:16) — 1s crossfade
- BGM fade-out 2s at end of intro music
- BGM fade-in 1s at sponsor break
- Hard music cut at outro end

## Studio Sound processing
- Apply Descript Studio Sound to both tracks at "Medium" setting
- DO NOT use "Strong" — over-processes and removes natural room tone

## Chapter markers (for RSS + Google Key Moments + listener nav)
- 00:00 — Cold open hook
- 02:30 — Sponsor read: <Sponsor>
- 05:00 — Topic 1: Why Tuesday morning
- 12:00 — Topic 2: The Sunday-night trap
- 18:00 — Guest backstory
- 25:00 — Hot take: open rates lie
- 28:00 — Listener Q&A
- 31:00 — CTA + outro

## Outputs to render
- master.wav (archive — 48kHz/24bit, stereo)
- master.mp3 (podcast distribution — 192kbps stereo, ID3 tags populated)
- master.mp4 (YouTube — 1080p, audio-only with branded waveform)
- master_pull-quote-1.mp3 (00:32:00-00:32:45, the hot-take moment)
- master_pull-quote-2.mp3 (00:18:30-00:19:10, the guest-backstory beat)

## ID3 / metadata tags
- title: "Episode 042: Tuesday-6am beats Sunday-night"
- artist: "<Show Name>"
- album: "<Show Name> Season 4"
- track: 42
- comment: "Show notes: <URL>"
- chapter: <embed via Descript chapter export>
```

### Recipe 5: ffmpeg loudness normalization (Descript-independent fallback)

```bash
# Two-pass EBU R128 loudness normalization to -16 LUFS
ffmpeg -i master_raw.wav -af "loudnorm=I=-16:TP=-1:LRA=11:print_format=json" -f null - 2> measure.txt
INPUT_I=$(grep input_i measure.txt | tr -dc '0-9.-')
INPUT_TP=$(grep input_tp measure.txt | tr -dc '0-9.-')
INPUT_LRA=$(grep input_lra measure.txt | tr -dc '0-9.-')
INPUT_THRESH=$(grep input_thresh measure.txt | tr -dc '0-9.-')

ffmpeg -i master_raw.wav -af "loudnorm=I=-16:TP=-1:LRA=11:measured_I=$INPUT_I:measured_TP=$INPUT_TP:measured_LRA=$INPUT_LRA:measured_thresh=$INPUT_THRESH:linear=true" -ar 48000 master.wav

ffmpeg -i master.wav -c:a libmp3lame -b:a 192k master.mp3
```

### Recipe 6: Filler-word strip via Whisper + ffmpeg

```bash
# Transcribe with word timestamps
whisper-cli -m $WHISPER_MODEL_PATH -ow -oj master.wav

# Generate ffmpeg select filter that drops "um" / "uh" words (within 200ms boundaries)
python3 - <<'EOF' > drops.txt
import json
data = json.load(open('master.wav.json'))
fillers = {"um", "uh", "umm", "uhh"}
selects = []
for seg in data['transcription']:
    for w in seg.get('words', []):
        if w['text'].strip().lower() in fillers:
            t0 = w['t0'] / 100  # cs to seconds
            t1 = w['t1'] / 100
            selects.append((t0, t1))
# Build inverse selection
print(selects)
EOF
```

Manual review recommended — Whisper transcribes "um" inconsistently; missed fillers are common.

### Recipe 7: Export Descript chapter markers → RSS `<podcast:chapter>`

```bash
# Export chapters from Descript via API (after editor saves)
curl -H "Authorization: Bearer $DESCRIPT_API_KEY" \
  "https://api.descript.com/v1/projects/proj_abc/chapters" \
  | jq '.chapters[] | {start: .startTime, title: .title}'

# Convert to RSS chapter XML for embed (see podcast-seo-titles-descriptions-chapters skill)
```

### Recipe 8: Sponsor BGM ducking via ffmpeg

```bash
ffmpeg -i sponsor_voice.wav -i sponsor_bgm.wav \
  -filter_complex "[1:a]volume=0.2[bgm];[0:a][bgm]amix=inputs=2:duration=longest" \
  sponsor_full.wav
# BGM at 20% volume under voice; voice at full
```

### Recipe 9: Render YouTube version (audio over branded waveform)

```bash
ffmpeg -i master.wav -i branded_background.png \
  -filter_complex "
    [0:a]showwaves=s=1920x300:colors=white:mode=line:rate=30,format=rgba[wave];
    [1:v]scale=1920:1080[bg];
    [bg][wave]overlay=0:780[out]
  " \
  -map "[out]" -map 0:a \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 192k \
  master.mp4
```

### Recipe 10: Pull-quote clip extraction

```bash
# Cut a 30-45s pull-quote clip from the master
ffmpeg -i master.wav -ss 00:32:00 -t 00:00:45 -c copy pull_quote_1.wav
ffmpeg -i pull_quote_1.wav -c:a libmp3lame -b:a 192k pull_quote_1.mp3
```

Hand off to `audiogram-headliner-wavve` for audiogram rendering, or to `repurposing-pipeline-1-to-10` for shorts.

## Examples

### Example 1: Interview episode end-to-end

**Goal:** Edit a 47-min raw interview down to 33-min publish-ready episode.

**Steps:**
1. Recipe 1: pull Riverside session, both tracks.
2. Recipe 2: pull Riverside transcript for the brief reference.
3. Author Recipe 4 brief with explicit cuts referenced to transcript timestamps.
4. Recipe 3: create Descript project, import both tracks, generate edit URL.
5. Send edit URL to the editor (or yourself); editor executes timeline ops.
6. After save: Recipe 7 export chapters; Recipe 9 render YouTube version.
7. Recipe 5 verify loudness compliance before publishing.
8. Hand off to `podcast-scripting-show-notes` Recipe 2 for Castmagic show notes.

**Result:** 33-min episode + YouTube video + chapter markers + pull-quote clips, all to spec.

### Example 2: Solo monologue with no Descript subscription

**Goal:** Edit a 22-min solo episode using ffmpeg-only (no Descript).

**Steps:**
1. Author Recipe 4 brief with cuts in seconds (not Descript timecodes).
2. Recipe 6 generates filler-strip drops list; manual review.
3. ffmpeg cut + concat per the brief's cut list.
4. Recipe 5 loudness-normalize.
5. Recipe 9 render YouTube version.

**Result:** Edited episode without Descript, slightly more manual.

### Example 3: Trailer cut from 5 episodes for season launch

**Goal:** Cut a 75s trailer pulling clips from 5 different episodes.

**Steps:**
1. Identify 5 best 10-15s pull-quotes across episodes via transcript search.
2. Recipe 10: extract each clip as standalone WAV.
3. Pre-write trailer per `podcast-scripting-show-notes` Recipe 7 (3-act).
4. Recipe 3: create Descript project, import all 5 clips + host VO tracks.
5. Editor arranges per the script.
6. Recipe 5 loudness-normalize the trailer master.

**Result:** Algorithm-bait 75s trailer for season launch.

## Edge cases / gotchas

- **Riverside API is Business plan ONLY.** Pro and below = no API. If you can't get Business, manual download from Riverside dashboard is the only path.
- **Riverside API can't do timeline edits.** Only fetch + delete. All editing is in Descript or ffmpeg.
- **Descript Studio Sound "Strong" over-processes.** Sounds AI. Use "Medium" or hand-tune.
- **Descript filler-word removal can chop mid-sentence.** Always review every auto-cut; trust nothing.
- **-16 LUFS is the podcast standard** for Apple Podcasts + Spotify. Other targets (-23 EBU R128 for broadcast, -14 LUFS for streaming) will sound wrong on podcast platforms.
- **Two-pass loudness normalization is non-negotiable** for compliance. Single-pass approximates and drifts.
- **Chapter markers >7 per episode dilute** — aim for 5-8 with descriptive titles (not "Topic 1").
- **Don't normalize music separately**. Process the full mix or BGM-under-voice ducking breaks.
- **48kHz/24bit master, 192kbps MP3 publish.** Anything below 128kbps sounds compressed; above 192k bloats file size without listener gain.
- **YouTube video version benefits from chapters too** — YouTube auto-detects time-coded chapters in the description.
- **Descript edit URL expires in 24h.** Re-mint if editor doesn't open within the window.
- **Backup the Riverside source** before deleting via API — once gone, irretrievable.
- **Speaker labels in Riverside transcripts are best-effort.** Always cross-check before publishing transcript on the episode page.

## Sources

- [Descript vs Riverside 2026](https://speakwiseapp.com/blog/descript-vs-riverside)
- [Descript vs Riverside (AI Productivity)](https://aiproductivity.ai/blog/descript-vs-riverside-2026/)
- [Riverside API review (Business plan)](https://cleanvoice.ai/blog/riverside-api-review/)
- [Cleanvoice — Best podcast APIs 2026](https://cleanvoice.ai/blog/best-podcast-api/)
- [Descript API docs](https://help.descript.com/hc/en-us/articles/4419537558539)
- [Riverside API docs](https://riverside.fm/help/api)
- [EBU R128 loudness standard](https://tech.ebu.ch/docs/r/r128.pdf)
- [Apple Podcasts audio specs](https://podcasters.apple.com/support/893-audio-requirements)
- [ffmpeg loudnorm filter](https://ffmpeg.org/ffmpeg-filters.html#loudnorm)
