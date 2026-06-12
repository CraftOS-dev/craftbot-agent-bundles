# AI Music — Suno (unofficial) + Mubert (licensed)

## When to use
- BGM scoring when stock libraries don't fit the brief
- Avoiding copyright claims on YouTube / TikTok / Reels
- Custom-vibed background music in seconds vs hours of stock search
- Beat-synced cues for video edits

## Provider landscape

| Provider | License | Commercial-clean? | Cost (June 2026) | Best for |
|---|---|---|---|---|
| Suno (official site) | Pro tier covers commercial | ✓ at Pro tier | $10–$30/mo | Vocal songs + complex arrangements |
| sunoapi.org (unofficial) | Reverse-engineered wrapper | ⚠ ToS-gray | ~$10/mo | Quick programmatic gen |
| apiframe.ai (alt unofficial) | Same caveat | ⚠ ToS-gray | $10–$20/mo | Suno alternative |
| **Mubert API** | Licensed, official | ✓ Fully commercial-cleared | $14–$199/mo | Production-safe BGM |
| Beatoven.ai | Licensed | ✓ | $20–$120/mo | Mood-based instrumental |
| AIVA | Licensed | ✓ | Free–$33/mo | Cinematic / orchestral |
| Soundraw | Licensed | ✓ | $17–$30/mo | Customizable stems |

**Rule:** for commercial / brand work, use **Mubert / Beatoven / AIVA / Soundraw**. Use Suno only when license-clean equivalents fail and the user accepts the risk.

## Setup
- All providers via `cli-anything` + `curl` (no MCPs); just API keys

## Common recipes — Suno (sunoapi.org wrapper)

### 1. Generate a song
```bash
curl -X POST "https://api.sunoapi.org/api/v1/generate" \
  -H "Authorization: Bearer $SUNO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Upbeat synthwave instrumental, 120 BPM, energetic, suitable for fitness vlogs",
    "make_instrumental": true,
    "model": "chirp-v4",
    "wait_audio": false
  }'
```
Returns `{ "ids": ["abc-123", "def-456"] }` — 2 variants per request.

### 2. Poll for completion
```bash
curl -H "Authorization: Bearer $SUNO_API_KEY" \
  "https://api.sunoapi.org/api/v1/feed?ids=abc-123,def-456"
```
When `status=complete`, the response has `audio_url` field. Download:
```bash
curl -L "$AUDIO_URL" -o bgm.mp3
```

### 3. Custom-mode (lyrics + style)
```bash
curl -X POST "https://api.sunoapi.org/api/v1/custom_generate" \
  -d '{
    "title": "City Rain",
    "tags": "lo-fi hip hop, jazz, instrumental, mellow, study music",
    "prompt": "[instrumental]",
    "make_instrumental": true,
    "wait_audio": false
  }'
```

### 4. Extend a song
```bash
curl -X POST "https://api.sunoapi.org/api/v1/extend" \
  -d '{"audio_id":"abc-123","continue_at":120,"prompt":"keep same vibe"}'
```

## Common recipes — Mubert (licensed)

### 5. Mubert generate (Render Tracks API)
```bash
curl -X POST "https://api-b2b.mubert.com/v2/RecordTrack" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "RecordTrack",
    "params": {
      "pat": "'$MUBERT_PAT'",
      "duration": 60,
      "intensity": "medium",
      "format": "mp3",
      "bitrate": 320,
      "mode": "track",
      "tags": ["chill", "ambient", "hopeful"]
    }
  }'
```
Returns `result.session_id`. Poll status, then download.

### 6. Mubert mood + genre options
- `mode`: `track`, `loop`, `mixin`
- `intensity`: `low`, `medium`, `high`
- `format`: `mp3`, `wav`, `ogg`
- Tags from Mubert taxonomy: `cinematic`, `dance`, `chill`, `lofi`, `rock`, `hip_hop`, `ambient`, `corporate`, `epic`, `meditation`, plus emotion: `hopeful`, `dark`, `triumphant`, `sad`, `energetic`

### 7. Beat-synced BGM workflow
1. Calculate target BPM from video edit's average cut interval (e.g., cuts every 0.5s → 120 BPM).
2. Prompt: `"120 BPM, downbeats clear, ${mood} instrumental"`.
3. Mubert returns; ffmpeg analyze BPM (`ffmpeg -i bgm.mp3 -af aubionotes`) to confirm.
4. Time-stretch via `ffmpeg atempo=` if BPM is off.

### 8. Stem-aware mixing (if provider supports)
Soundraw + AIVA return separate stems (drums / bass / lead). FFmpeg multi-track mix lets you duck individual stems under VO.

### 9. Ducking generated BGM under VO
After Suno/Mubert returns `bgm.mp3`, run the FFmpeg sidechain-compress recipe from `ffmpeg-audio-mastering` (recipe 4).

### 10. Length matching to video
Mubert: pass `duration` exact (e.g., 87 seconds). Suno: generate 2-min track then trim with FFmpeg.

### 11. Multi-variant generation
Suno generates 2 variants per request. Submit 3 requests → 6 candidates. Score on fit, pick winner.

### 12. License audit per file
For each track, store:
```json
{
  "file": "bgm_123.mp3",
  "provider": "Mubert",
  "license_id": "sub_2026_05",
  "commercial_use": true,
  "stream_platforms_cleared": ["youtube","tiktok","instagram","spotify"]
}
```

### 13. Track regenerate / variation
Mubert: same prompt + different `seed` (param if exposed) for variations on a theme.

### 14. Vocal sample removal (when you only want instrumental)
Suno auto-vocal can leak even with `make_instrumental: true`. Run through ElevenLabs Voice Isolator inverse, or `spleeter`/`demucs`:
```bash
demucs --two-stems vocals bgm.mp3
# Output: separated/htdemucs/bgm/no_vocals.wav
```

### 15. Style transfer / reference track
Mubert doesn't support reference upload. Suno: in custom mode, paste lyrical + style tags matching the reference mood.

## Examples

### A. 60-second TikTok fitness BGM
1. Mubert RecordTrack: `tags=["energetic","dance","powerful"], duration=60, intensity=high`.
2. Wait 30–60s, download.
3. FFmpeg loudnorm to -14 LUFS + sidechain duck under VO.

### B. YouTube long-form ambient bed
1. Mubert mode=`loop`, tags=`["ambient","chill","lofi"], duration=600`.
2. Bake into video as background bed.
3. SFX overlays + VO on top.

### C. Quick prototype (Suno, accept risk for non-commercial)
1. Suno API: `prompt="lo-fi hip hop study beats, instrumental"`, `make_instrumental=true`.
2. 2 variants returned in ~90s.
3. Pick → use for draft. Replace with Mubert before publish.

### D. Beat-matched cuts
1. Generate BGM at 120 BPM.
2. In Remotion / Premiere, place cuts on 0.5s intervals (= downbeats).
3. Result: visually beat-synced edit, satisfying tension/release.

## Edge cases / gotchas

1. **sunoapi.org is unofficial.** Suno can revoke at any time; budget for migration to Mubert if API breaks.
2. **Commercial use of Suno output** is allowed only at Pro tier on official site; unclear via unofficial wrappers — assume risk.
3. **TikTok Music Rights** can still flag AI-generated tracks if they resemble copyrighted material. Mubert + AIVA carry indemnification.
4. **YouTube Content ID** sometimes flags AI tracks. Mubert offers Content ID whitelist process.
5. **Output is lossy MP3** by default. Request WAV / 320kbps MP3 for masters.
6. **Generation latency** Mubert: 10–30s. Suno: 60–120s.
7. **Same prompt → different output every time.** No seed in most APIs; lock variations by saving the audio asset.
8. **Loop crossfades** need work. Mubert "loop mode" produces clean loops; Suno requires manual FFmpeg crossfade.
9. **Long durations** sometimes split into chunks needing concat. Check output length matches request.
10. **Vocal-instrumental separation** isn't perfect — re-run with `demucs` if leakage matters.
11. **Stem provider tiers** — Soundraw + AIVA charge more for stems; Mubert standard doesn't expose stems.
12. **BPM detection on AI tracks** can be unreliable; pre-spec BPM in prompt.

## Sources
- https://sunoapi.org/api-docs
- https://mubert.com/api
- https://docs.mubert.com/
- https://www.aiva.ai/
- https://soundraw.io/api
- https://www.beatoven.ai/
