# Audiogram — Headliner Pro RSS Autopilot + ffmpeg Fallback

> Generate 60-90s audiograms per podcast episode via Headliner RSS autopilot or fully scriptable ffmpeg fallback.

## When to use

Trigger on: "make an audiogram", "audiogram from this episode", "promote my podcast on Instagram", "RSS audiogram", "Headliner this", "Wavve this", "ffmpeg audiogram". This skill owns: audio-content visual repurposing (waveform overlay + captions synced to voice). For long-video-to-short-clip conversion see `repurposing-pipeline-1-to-10` (OpusClip). For short-form video scripting see `short-form-video-script-reels-shorts-tiktok`. For full short-form caption polish see Submagic via that same skill.

## Setup

```bash
# Headliner Pro — RSS autopilot (no public API; GUI + RSS config)
# Setup once: Headliner dashboard → New Project → RSS feed → template → autopilot ON

# Wavve — alt manual tool (no public API; GUI workflow)
# Setup: Wavve account → upload audio → design → export

# ffmpeg + Whisper.cpp for fully scriptable fallback
brew install ffmpeg whisper-cpp
bash ./models/download-ggml-model.sh large-v3
```

Auth env vars:
- `HEADLINER_RSS_FEED` — your podcast RSS feed URL; Headliner monitors and auto-generates.
- `HEADLINER_YT_CHANNEL_ID` — optional; for auto-upload audiogram to YouTube.
- `WHISPER_MODEL_PATH` — for ffmpeg fallback caption generation.

## Common recipes

### Recipe 1: Headliner Pro RSS autopilot config (one-time)

```yaml
# In Headliner dashboard → New Project:
project_type: Audiogram (Auto)
rss_feed: <HEADLINER_RSS_FEED>
template:
  background: branded_background.png  # 1080x1920 (9:16) or 1080x1080 (1:1)
  waveform_position: bottom-center
  waveform_color: '#FFFFFF'
  caption_font: Inter
  caption_size: 56pt
  caption_color: '#FFFFFF'
  caption_position: middle-third
clip_strategy: AI-pick-best-90s-from-each-episode  # or first-60s / last-60s
auto_upload:
  youtube_channel: <HEADLINER_YT_CHANNEL_ID>
  visibility: public
  description_template: "Full episode: {{episode_link}}"
notification:
  email: you@example.com
  on: ready_for_review
```

Save once. Headliner auto-generates per new RSS episode. Pro plan = $9.99/mo.

### Recipe 2: Headliner export checklist

```markdown
## Before publishing a Headliner-generated audiogram:
- [ ] Hook in first 3 seconds (audible or visible)
- [ ] Vertical 9:16 for Reels / TikTok / Shorts; square 1:1 for X / LinkedIn / Facebook
- [ ] Branded colors + logo (subtle, not dominant)
- [ ] Captions burned in (verify Headliner's caption accuracy on your accent / industry terms)
- [ ] Voice at -6 dB peak, BGM at -24 dB (if BGM present)
- [ ] Total length 30-90s (60s SOTA default)
- [ ] CTA in last 3 seconds (Subscribe / Listen now / Link in bio)
```

### Recipe 3: ffmpeg audiogram (fully scriptable fallback)

```bash
# Inputs: podcast_clip.mp3 (60s), branded_background.png (1080×1920), captions.srt

# Step 1: Generate animated waveform overlay
ffmpeg -y -i podcast_clip.mp3 -i branded_background.png \
  -filter_complex "
    [0:a]showwaves=s=1080x200:colors=white:mode=line:rate=30,format=rgba[wave];
    [1:v]scale=1080:1920[bg];
    [bg][wave]overlay=0:1700[out]
  " \
  -map "[out]" -map 0:a \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 192k \
  -t 60 \
  audiogram_no_captions.mp4

# Step 2: Burn-in captions via Whisper-generated SRT
ffmpeg -y -i audiogram_no_captions.mp4 \
  -vf "subtitles=captions.srt:force_style='FontName=Inter,FontSize=20,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,BorderStyle=3,Outline=2,Alignment=2,MarginV=200'" \
  -c:a copy \
  audiogram_final.mp4
```

### Recipe 4: Auto-generate captions via Whisper for ffmpeg fallback

```bash
# Resample to 16kHz mono
ffmpeg -i podcast_clip.mp3 -ar 16000 -ac 1 -c:a pcm_s16le clip.wav

# Whisper SRT export
whisper-cli -m $WHISPER_MODEL_PATH -osrt -l en -ml 32 clip.wav
# Output: clip.wav.srt
mv clip.wav.srt captions.srt
```

`-ml 32` caps line length at 32 chars (mobile-readable).

### Recipe 5: Pick the best 60s clip from a 45-min episode

```bash
# Option A: human-pick — review transcript, identify hot-take moment, cut with ffmpeg
ffmpeg -i master.mp3 -ss 00:32:00 -t 60 -c copy clip.mp3

# Option B: use Castmagic 'quotes' derivative to identify viral moments
QUOTES=$(curl -H "Authorization: Bearer $CASTMAGIC_API_KEY" \
  "https://api.castmagic.io/v1/uploads/$UPLOAD_ID/derivatives" | jq -r '.quotes[]')
# Find quote in transcript, get timestamp, cut

# Option C: OpusClip API on the video version (see repurposing-pipeline-1-to-10)
```

### Recipe 6: Square (1:1) audiogram for X / LinkedIn / Facebook

```bash
ffmpeg -i podcast_clip.mp3 -i background_square.png \
  -filter_complex "
    [0:a]showwaves=s=1080x150:colors=white:mode=line:rate=30,format=rgba[wave];
    [1:v]scale=1080:1080[bg];
    [bg][wave]overlay=0:900[out]
  " \
  -map "[out]" -map 0:a \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 192k \
  -t 60 \
  audiogram_square.mp4
```

### Recipe 7: Bouncing bars waveform (alt visualization)

```bash
# 'showspectrum' or 'showfreqs' for spectrum-style animation
ffmpeg -i podcast_clip.mp3 -i background.png \
  -filter_complex "
    [0:a]showfreqs=s=1080x200:mode=bar:cmode=combined,format=rgba[wave];
    [1:v]scale=1080:1920[bg];
    [bg][wave]overlay=0:1700[out]
  " \
  -map "[out]" -map 0:a \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 192k \
  -t 60 \
  audiogram_bars.mp4
```

### Recipe 8: Multi-platform export from one source

```bash
SOURCE_MP3=clip.mp3
BG=background.png

# 9:16 for Reels / TikTok / Shorts
ffmpeg -i $SOURCE_MP3 -i $BG -filter_complex "[0:a]showwaves=s=1080x200:colors=white:mode=line:rate=30,format=rgba[w];[1:v]scale=1080:1920[bg];[bg][w]overlay=0:1700[o]" -map "[o]" -map 0:a -c:v libx264 -crf 23 -c:a aac -b:a 192k -t 60 audiogram_vertical.mp4

# 1:1 for X / LinkedIn / Facebook
ffmpeg -i $SOURCE_MP3 -i $BG -filter_complex "[0:a]showwaves=s=1080x150:colors=white:mode=line:rate=30,format=rgba[w];[1:v]scale=1080:1080[bg];[bg][w]overlay=0:900[o]" -map "[o]" -map 0:a -c:v libx264 -crf 23 -c:a aac -b:a 192k -t 60 audiogram_square.mp4

# 16:9 for YouTube
ffmpeg -i $SOURCE_MP3 -i $BG -filter_complex "[0:a]showwaves=s=1920x300:colors=white:mode=line:rate=30,format=rgba[w];[1:v]scale=1920:1080[bg];[bg][w]overlay=0:780[o]" -map "[o]" -map 0:a -c:v libx264 -crf 23 -c:a aac -b:a 192k -t 60 audiogram_landscape.mp4
```

### Recipe 9: Loudness compliance for social platforms

```bash
# Normalize voice loudness for social platforms (-14 LUFS streaming standard)
ffmpeg -i podcast_clip.mp3 -af "loudnorm=I=-14:TP=-1:LRA=11" -ar 48000 clip_normalized.mp3
```

-14 LUFS is the Spotify / Instagram / YouTube streaming target. Don't ship audiograms at -16 LUFS (podcast standard) — they'll sound quiet vs other social content.

### Recipe 10: Publish + schedule via Buffer

```bash
# After audiogram rendered, schedule cross-platform
for PLATFORM in instagram linkedin twitter facebook; do
  case $PLATFORM in
    instagram|tiktok|youtube) MEDIA=audiogram_vertical.mp4 ;;
    linkedin|facebook|twitter) MEDIA=audiogram_square.mp4 ;;
  esac
  npx @buffer/mcp-server create_post \
    --platform $PLATFORM \
    --content "$(cat caption_$PLATFORM.md)" \
    --media-file $MEDIA \
    --scheduled-at "2026-06-19T15:00:00Z"
done
```

### Recipe 11: Wavve for hand-crafted promotional clip

```markdown
Wavve workflow (manual, no API):
1. wavve.co dashboard → New project
2. Upload clip.mp3
3. Select template (15+ pre-designed)
4. Customize colors, font, logo
5. AI Moment Identification (Wavve has built-in viral-moment picker)
6. Caption tuning (Wavve's caption editor)
7. Export 9:16 / 1:1 / 16:9

Better for hand-crafted hero clips; Headliner is better for autopilot volume.
```

### Recipe 12: Audiogram thumbnail variant for static social

```bash
# Extract a single frame for a static thumbnail post
ffmpeg -ss 00:00:03 -i audiogram_vertical.mp4 -vframes 1 -q:v 2 thumbnail.jpg
```

Useful when posting just to Instagram feed (not Reels) — static image + caption with "tap to listen" CTA.

## Examples

### Example 1: Per-episode audiogram via Headliner RSS autopilot

**Goal:** New podcast episode publishes Tuesday; audiogram lives on Instagram / LinkedIn by Wednesday.

**Steps:**
1. One-time Recipe 1 setup: Headliner Pro RSS autopilot configured.
2. Tuesday: podcast episode publishes; RSS updates.
3. Tuesday +1h: Headliner detects RSS update, generates audiogram, uploads to YouTube (if configured), emails review notification.
4. Tuesday PM: review audiogram per Recipe 2 checklist.
5. Wednesday: Recipe 10 Buffer schedule for Wed 5pm ET.

**Result:** Per-episode audiogram on autopilot with minimal manual touch.

### Example 2: ffmpeg fallback when Headliner subscription canceled

**Goal:** Generate 60s vertical audiogram from a specific episode quote without Headliner.

**Steps:**
1. Recipe 5: cut 60s clip from master.mp3 (00:32:00-00:33:00 was the hot-take).
2. Recipe 4: Whisper generates captions.srt.
3. Recipe 3: ffmpeg waveform + background + caption burn-in → audiogram_final.mp4.
4. Recipe 9: loudness-normalize for social.
5. Recipe 10: Buffer cross-platform schedule.

**Result:** Equivalent audiogram via ffmpeg only, no Headliner needed.

### Example 3: Multi-platform variants from one clip

**Goal:** Single 60s clip publishes as 9:16 (Reels / TikTok / Shorts) + 1:1 (X / LinkedIn / Facebook) + 16:9 (YouTube).

**Steps:**
1. Cut clip.mp3 via Recipe 5.
2. Recipe 8: render all three aspect ratios in one ffmpeg loop.
3. Per-platform captions (Recipe 4 once; same SRT for all 3 aspect ratios).
4. Recipe 10: Buffer schedule each variant to its native platform.

**Result:** 3-aspect audiogram cascade from one source clip.

## Edge cases / gotchas

- **Headliner has NO public API.** RSS autopilot is the workaround for automation.
- **Headliner Pro = $9.99/mo** (cheapest of the three paid plans).
- **ffmpeg `showwaves` `rate=30`** matches social-platform expected fps. Higher rates = smoother but larger file; lower = visible stutter.
- **Caption burn-in size of 20pt at 1080×1920** = mobile-readable. Larger sizes (32pt+) for older audiences.
- **Whisper-generated captions occasionally hallucinate** in long silences. Pre-trim silences with `silenceremove`.
- **Vertical 9:16 vs square 1:1 vs landscape 16:9** — match the platform's native aspect or get cropped/letterboxed by the platform.
- **Don't burn captions in landscape 16:9 versions for YouTube** — let YouTube generate its own captions (better accessibility).
- **Loudness target -14 LUFS for social platforms** vs -16 LUFS for podcast platforms. Don't ship social audiograms at podcast loudness.
- **Headliner's AI moment-picker** sometimes picks the wrong moment. Always review (Recipe 2).
- **Audiogram >90s tanks completion rate** on Instagram / TikTok. 30-60s is sweet spot.
- **Brand logo too prominent** = distracts from voice. Keep at 10-15% of screen real estate max.
- **First 3 seconds determines scroll-stop** — start the audio mid-claim, not at "welcome to..."
- **Pre-trim silences** with `ffmpeg -af silenceremove` before the audiogram clip cut. Silent gaps tank engagement.
- **Don't auto-upload Headliner audiograms to YouTube as Shorts** without `#Shorts` tag — YouTube algorithm needs the tag to surface in Shorts feed.
- **Wavve is more design-flexible than Headliner** but slower; use Wavve for hero/launch audiograms.

## Sources

- [Headliner](https://www.headliner.app/)
- [Best podcast audiogram tools 2026 (Podosphere)](https://www.thepodosphere.com/blog/podcast-audiogram-tools-2026)
- [Wavve](https://wavve.co/)
- [Submagic — alt caption polish](https://www.submagic.co/)
- [ffmpeg showwaves filter](https://ffmpeg.org/ffmpeg-filters.html#showwaves)
- [ffmpeg subtitles filter](https://ffmpeg.org/ffmpeg-filters.html#subtitles)
- [ffmpeg loudnorm filter](https://ffmpeg.org/ffmpeg-filters.html#loudnorm)
- [Whisper.cpp](https://github.com/ggerganov/whisper.cpp)
