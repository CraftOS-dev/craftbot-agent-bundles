# Hedra Character-3 — AI Lip-Synced Avatars

## When to use
- A talking-head visual when on-camera talent isn't available
- Foreign-language dubbing with matching mouth shapes
- Narrator overlay for explainer / educational content
- Batch-producing variants of the same script with different "presenters"

Per role.md: digital avatars are a **supplement, not replacement** — audiences trust real people more. Use Hedra when the alternative is no visual at all.

## Setup
- No MCP wrapper; use `cli-anything` + `curl`
- Auth: `X-API-KEY: $HEDRA_API_KEY`
- Base URL: `https://api.hedra.com`
- Get key at https://www.hedra.com — Studio tier ($35/mo) for typical agent use

## Quality vs alternatives (June 2026)
| Tool | Lip-sync quality | Cost | Notes |
|---|---|---|---|
| Hedra Character-3 | **9/10** | ~$0.30/sec | SOTA, best mouth shapes |
| Hedra Character-2 | 7/10 | ~$0.15/sec | Older, cheaper |
| HeyGen | 8/10 | $30+/mo + per-min | Polished avatars, less flexible |
| D-ID | 7/10 | $5+/mo | Quick, lower quality |
| Synthesia | 8/10 | $30/mo | Enterprise / corporate use |
| LipDub AI | 7/10 | $20/mo | Music + speech sync |

## Common recipes

### 1. Create avatar generation (audio + face image → video)
```bash
curl -X POST https://api.hedra.com/web-app/public/generations \
  -H "X-API-KEY: $HEDRA_API_KEY" \
  -F "audio=@narration.wav" \
  -F "image=@face.png" \
  -F "aspect_ratio=16:9" \
  -F "resolution=1080p" \
  -F "model_id=character-3"
```
Returns `{ "job_id": "...", "status": "queued" }`.

### 2. Poll job status
```bash
curl -H "X-API-KEY: $HEDRA_API_KEY" \
  "https://api.hedra.com/web-app/public/generations/$JOB_ID"
```
When `status=completed`, response includes `url`. Download the MP4.

### 3. Face image requirements
- Single subject, front-facing
- Eyes visible, neutral or slight expression
- Sharp focus, even lighting
- ≥1024px on shortest side
- PNG or JPG; transparent BG works for compositing

### 4. Audio requirements
- WAV / MP3 / M4A
- 16kHz+ sample rate
- Single speaker per generation
- ≤2 min per generation (split longer audio)
- Clean (run through ElevenLabs Voice Isolator first)

### 5. Aspect ratios
| AR | Use |
|---|---|
| `16:9` | YouTube long-form |
| `9:16` | TikTok / Reels / Shorts |
| `1:1` | Instagram feed |

### 6. Text-to-avatar (TTS chained → Hedra)
```bash
# Step 1: ElevenLabs TTS
curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/$VOICE_ID" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
  -d '{"text":"...","model_id":"eleven_multilingual_v2"}' --output vo.mp3

# Step 2: Convert mp3 → wav (Hedra prefers)
ffmpeg -i vo.mp3 -ar 24000 -ac 1 vo.wav

# Step 3: Hedra
curl -X POST https://api.hedra.com/web-app/public/generations \
  -H "X-API-KEY: $HEDRA_API_KEY" \
  -F "audio=@vo.wav" -F "image=@brand_face.png" -F "aspect_ratio=16:9"
```

### 7. Foreign-language dub workflow
1. ElevenLabs Dubbing endpoint → translate VO to target language.
2. Feed translated audio + original face image to Hedra.
3. Result: same face, mouth shapes matched to translated speech.

### 8. Batch script → N avatar videos
```python
import requests, time
script_lines = [...]  # list of strings
for i, line in enumerate(script_lines):
    # 1. TTS
    audio = elevenlabs_tts(line)
    # 2. Hedra
    job = requests.post("https://api.hedra.com/web-app/public/generations",
        headers={"X-API-KEY": HEDRA_KEY},
        files={"audio": audio, "image": open(f"faces/{i}.png", "rb")},
        data={"aspect_ratio": "9:16"})
    job_id = job.json()["job_id"]
    # 3. Poll
    while True:
        s = requests.get(f"https://api.hedra.com/web-app/public/generations/{job_id}",
            headers={"X-API-KEY": HEDRA_KEY}).json()
        if s["status"] == "completed": break
        time.sleep(5)
    # 4. Download
    requests.get(s["url"], stream=True)
```

### 9. Background swap (Hedra outputs match input image's background)
Pre-process face image: use Replicate `851-labs/background-remover` → transparent PNG → composite onto desired background → feed to Hedra.

### 10. Multi-shot narration video
1. Split long VO into 30s chunks (Hedra has 2-min cap, but 30s renders faster).
2. Each chunk + same face → individual avatar clips.
3. FFmpeg `concat` to stitch.

### 11. Embed avatar as overlay (PIP)
Hedra output → FFmpeg overlay:
```bash
ffmpeg -i main_video.mp4 -i avatar.mp4 -filter_complex \
  "[1]scale=480:-1[av];[0][av]overlay=W-w-30:H-h-30" \
  pip.mp4
```
Lower-right corner picture-in-picture, common for tutorial videos.

### 12. Vertical avatar for Shorts/TikTok
Generate at `aspect_ratio=9:16` directly — Hedra handles framing better than post-crop.

### 13. Static-frame loop fallback (if quality fails)
If Hedra output has artifacts, fall back to: subtle still-frame Ken Burns zoom + voiceover (no lip-sync, no risk).

### 14. Consent + IP gates
Never feed faces of real people without explicit written consent + commercial-use rights. Use AI-generated faces (Flux 2 Pro) for risk-free brand narrators.

### 15. Custom AI face workflow
1. Flux 2 Pro: `"Studio portrait of a 30yo female business presenter, friendly smile, neutral grey background, professional"`.
2. Save the seed.
3. Use this face for the brand's "AI narrator" across all videos → series consistency.

## Examples

### A. 30-second educational narration
1. Script → ElevenLabs Multilingual v2 → `vo.mp3`.
2. Brand face → Hedra at 9:16, 1080p.
3. ~2 min compute time → 30s avatar MP4.
4. Composite with B-roll cutaways for visual variety.

### B. 4-language dubbed campaign
1. Master script in English → ElevenLabs Dubbing → es/pt/de/ja audio tracks.
2. Same brand face + each audio → 4 Hedra renders.
3. Result: 4 language SKUs with consistent on-screen presenter.

### C. Talking-head with cutaway B-roll
1. Hedra avatar at 9:16, full duration.
2. FFmpeg overlay alternates between full-screen avatar and full-screen B-roll based on edit cues (mask + crossfade).

### D. AI narrator series consistency
1. Generate brand face via Flux 2 Pro, seed-locked.
2. Use for every episode of the series.
3. Audience builds familiarity with the AI presenter (and you control "casting").

## Edge cases / gotchas

1. **Hedra rejects multi-face images.** Crop to single face before upload.
2. **Side profiles fail.** Front-3/4 view only.
3. **Sunglasses / heavy occlusion** → low-quality lip-sync.
4. **Background motion in source image** can confuse the model. Use static-background portraits.
5. **Output is ~24fps by default.** FFmpeg `-r 30` to upsample for vertical platforms.
6. **2-min cap per generation** — chain for longer.
7. **Cost adds up fast.** A 30-min narrator = ~$540 at $0.30/sec. Plan budget.
8. **Brand consistency** requires reusing the SAME face image across all generations.
9. **Audio with music in BG** confuses lip-sync. Use voice-isolated audio only.
10. **Female vs male voice** — choice your face to match.
11. **Watermarks** — some free trials add Hedra watermark; paid tiers remove.
12. **Latency** typically 1–3 min for a 30s clip; webhook support not yet available — poll.

## Sources
- https://www.hedra.com/docs
- https://docs.hedra.com/api-reference/
- https://www.hedra.com/character-3 (model details)
