# ElevenLabs Voice Production

## When to use
- AI VO for scripts (Multilingual v2 = best quality; Turbo v2.5 = real-time, lower latency)
- Voice cloning from a sample
- Voice isolation (better than FFmpeg afftdn for noisy production audio)
- Dubbing across languages while retaining speaker identity
- AI sound effects

## Setup
- Auth via `elevenlabs-mcp` (already wired in `agent.yaml`); user supplies `ELEVENLABS_API_KEY`
- Direct REST: `xi-api-key: $ELEVENLABS_API_KEY`, base `https://api.elevenlabs.io/v1`
- Pricing tier: Creator ($22/mo) covers most agent use cases; Pro ($99/mo) for >100k chars

## Model lineup (June 2026)

| Model | ID | Use | Cost |
|---|---|---|---|
| Eleven Multilingual v2 | `eleven_multilingual_v2` | Hero VO, dubbing — 29 languages | High |
| Eleven Turbo v2.5 | `eleven_turbo_v2_5` | Low-latency, real-time | Mid |
| Eleven Flash v2.5 | `eleven_flash_v2_5` | Ultra-fast (~75ms), draft VO | Low |
| Voice Isolator | (endpoint) | Noise removal | Per-second |
| Dubbing v2 | (endpoint) | Cross-language with speaker preservation | Per-minute |

## Common recipes

### 1. Text-to-speech (Multilingual v2)
```bash
curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/$VOICE_ID" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Today I want to talk about why your hook is failing in the first three seconds.",
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
      "stability": 0.5,
      "similarity_boost": 0.75,
      "style": 0.4,
      "use_speaker_boost": true
    }
  }' --output vo.mp3
```
Via MCP: `elevenlabs-mcp text_to_speech` with same params.

### 2. Voice settings cheat sheet
- **Stability** (0–1) — 0.3 = expressive/dramatic; 0.5 = balanced; 0.75 = consistent narrator
- **Similarity boost** (0–1) — 0.75+ keeps the cloned voice on-model
- **Style** (0–1) — 0.0 = neutral; 0.4 = emotive; 0.7 = theatrical (warning: artifacts above 0.5)
- **Speaker boost** — true for cloned voices to retain identity

### 3. Voice Isolator (post-production noise removal)
```bash
curl -X POST "https://api.elevenlabs.io/v1/audio-isolation" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -F "audio=@noisy_vo.wav" \
  --output clean_vo.wav
```
Strips room tone, traffic, HVAC, music bleed — keeps voice clean. Better than FFmpeg `afftdn` for noisy field recordings.

### 4. Voice cloning (Professional Voice Clone — IVC)
```bash
curl -X POST "https://api.elevenlabs.io/v1/voices/add" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -F "name=brand_narrator" \
  -F "files=@sample1.wav" -F "files=@sample2.wav" \
  -F "labels={\"accent\":\"american\",\"age\":\"adult\"}"
```
3 minutes of clean source → 95%+ similarity clone. Instant Voice Clone (IVC) for free tier; Professional (PVC) for higher fidelity at Pro tier.

### 5. Dubbing pipeline
```bash
curl -X POST "https://api.elevenlabs.io/v1/dubbing" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -F "file=@source_en.mp4" \
  -F "target_lang=es" \
  -F "source_lang=en" \
  -F "num_speakers=1" \
  -F "watermark=false"
```
Returns a `dubbing_id`. Poll `GET /v1/dubbing/{id}` until `status=dubbed`, then `GET /v1/dubbing/{id}/audio/{lang}` to fetch the dubbed file.

### 6. Sound effects generation
```bash
curl -X POST "https://api.elevenlabs.io/v1/sound-generation" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Thunderclap with distant rain on a window",
    "duration_seconds": 5,
    "prompt_influence": 0.4
  }' --output thunder.mp3
```

### 7. Pre-made voice library lookup
```bash
curl -H "xi-api-key: $ELEVENLABS_API_KEY" \
  "https://api.elevenlabs.io/v1/voices" | jq '.voices[] | {voice_id, name, category, labels}'
```
Filter for `category=premade` for the 30+ stock voices.

### 8. SSML-ish controls via punctuation + tags
Multilingual v2 doesn't accept SSML, but the model respects:
- `...` for pause
- Capitalized `WORDS` for emphasis
- `<break time="1s" />` (custom — some voices honor)
- Question marks for upward inflection
- Em dashes for thinking pauses

### 9. Streaming TTS (real-time)
```bash
curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/$VOICE_ID/stream" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
  -d '{"text":"...","model_id":"eleven_turbo_v2_5"}' --output -
```
Used for low-latency apps; for offline VO, the non-stream endpoint is fine.

### 10. Output format selection
Query param `output_format`:
- `mp3_44100_128` — small, default
- `mp3_44100_192` — better quality
- `pcm_44100` — uncompressed (for further FFmpeg processing)
- `pcm_24000` — 16-bit, 24kHz (legacy)
Use PCM for downstream FFmpeg mastering.

### 11. Pronunciation control
For names / acronyms: provide phonetic spelling: `"M-I-T"` or `"em-eye-tee"` → `MIT`. For Mandarin, ElevenLabs supports pinyin: `nǐ hǎo`.

### 12. Multi-speaker dialogue
Use different `voice_id` per speaker. Concatenate the resulting MP3s with FFmpeg `concat` demuxer.

### 13. Batch VO from a script file
```bash
while IFS= read -r LINE; do
  ID=$(echo $LINE | jq -r .id)
  TEXT=$(echo $LINE | jq -r .text)
  curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/$VOICE_ID" \
    -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
    -d "{\"text\":\"$TEXT\",\"model_id\":\"eleven_multilingual_v2\"}" \
    --output "vo_$ID.mp3"
done < script.jsonl
```

### 14. Voice Isolator → FFmpeg mastering chain
1. Voice Isolator returns clean WAV.
2. Pipe into `ffmpeg-audio-mastering` voice chain (highpass + clarity EQ + compander).
3. Then 2-pass loudnorm.
Result: broadcast-grade VO from a phone recording.

### 15. Character count / quota check
```bash
curl -H "xi-api-key: $ELEVENLABS_API_KEY" "https://api.elevenlabs.io/v1/user/subscription"
```
Returns `character_count`, `character_limit`. Use to avoid mid-render quota fails.

## Examples

### A. 60-second YouTube VO from script
1. Write script → ~150 words.
2. POST to `/text-to-speech/$VOICE_ID` with `eleven_multilingual_v2`, `stability: 0.5`, `style: 0.3`.
3. Receive MP3 → run through FFmpeg loudnorm → mux into Remotion video.

### B. Clean a noisy field interview
1. Voice Isolator (`/audio-isolation`) on raw `interview.wav` → `interview_clean.wav`.
2. FFmpeg highpass + de-ess → master.
3. Subtitle gen via Whisper.cpp on the clean track (better WER).

### C. 4-language dubbed campaign
1. Master video (English).
2. POST `/dubbing` for each target: `es`, `pt-BR`, `de`, `ja`.
3. Poll until each completes.
4. Mux each dubbed track back into the master video via FFmpeg.

### D. Cloned brand-narrator voice
1. Collect 3 min clean studio recording of internal narrator.
2. POST `/voices/add` (Professional Voice Clone if Pro tier).
3. Use returned `voice_id` for all subsequent VO.

## Edge cases / gotchas

1. **Voice cloning consent required.** ElevenLabs ToS requires the speaker's consent for cloning. Document it.
2. **Quota is character-based, not duration.** 10,000 chars ≈ 12 min of speech. Watch the quota meter on Creator tier.
3. **`stability` too low** = chaotic/voice-cracking output. Too high = monotone. 0.4–0.6 is the sweet spot for VO.
4. **`style` > 0.5** causes audible artifacts on most voices. Keep 0.3–0.4 unless you want theatrical.
5. **Multilingual v2 is slower than Turbo** by ~3×. Use Turbo for drafts, Multilingual for final.
6. **Dubbing watermarks free tier.** Add `watermark=false` (requires Pro tier).
7. **MP3 → MP3 quality loss.** When chaining (TTS → FFmpeg → final), prefer PCM intermediates.
8. **Long inputs** (>1000 chars) — split into sentences to avoid prosody drift.
9. **Numbers spelled out vs numeric.** "2025" sometimes reads as "two zero two five." Force: "twenty twenty-five."
10. **Voice ID changes when you re-clone.** Pin IDs in your config; don't re-clone in scripts without updating refs.
11. **Sound generation max duration 22s.** Chain for longer ambient beds.
12. **API rate limits** (Creator): 2 concurrent requests. Plan batch loops accordingly.

## Sources
- https://elevenlabs.io/docs/api-reference/introduction
- https://elevenlabs.io/docs/api-reference/text-to-speech
- https://elevenlabs.io/docs/api-reference/audio-isolation
- https://elevenlabs.io/docs/api-reference/dubbing
- https://elevenlabs.io/docs/api-reference/sound-generation
- https://github.com/elevenlabs/elevenlabs-mcp
