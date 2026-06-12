# Replicate AI Video Generation

## When to use
- You need a short cinematic clip (1–20s) and have no live footage
- You want Sora 2 / Veo 3.1 / Kling / Runway behind a single auth + billing surface
- You're prototyping a hook, B-roll insert, or animated transition shot
- You need camera-controllable shots (Runway Gen-4) or sync audio (Veo 3.1 native audio)

Skip this skill when: the brand requires real footage, the shot exceeds 20s (chain multiple generations), or budget cannot accommodate $0.10–$2/sec compute.

## Setup
- Auth via `replicate-mcp` (already wired in `agent.yaml`); user supplies `REPLICATE_API_TOKEN` in MCP env
- Direct REST (fallback via `cli-anything`): `Authorization: Bearer $REPLICATE_API_TOKEN`
- Base URL: `https://api.replicate.com/v1`

## Cost model (June 2026)

| Model | Slug | Cost | Notes |
|---|---|---|---|
| Sora 2 | `openai/sora-2` | ~$0.10/sec | Natural language; great prompt adherence |
| Sora 2 Pro | `openai/sora-2-pro` | ~$0.30/sec | Higher resolution, longer (up to 20s) |
| Veo 3.1 | `google/veo-3.1` | ~$0.75/sec | Native sync audio, photoreal |
| Veo 3.1 Fast | `google/veo-3.1-fast` | ~$0.40/sec | Faster, slightly lower fidelity |
| Kling 2.0 / 3.0 | `kwaivgi/kling-v2.0` / `v3.0` | ~$0.28/sec | Best motion quality at mid cost |
| Runway Gen-4 Turbo | `runwayml/gen-4-turbo` | ~$0.50/sec | Camera-controllable, image-to-video |
| Minimax Hailuo 02 | `minimax/hailuo-02` | ~$0.20/sec | Strong character consistency |
| Luma Ray 2 | `luma/ray-2` | ~$0.30/sec | Smooth motion, good for product |

## Common recipes

### 1. Sora 2 — natural-language prompt
```bash
curl -X POST https://api.replicate.com/v1/predictions \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "version": "openai/sora-2",
    "input": {
      "prompt": "A cinematic close-up of an espresso pour in slow motion, golden hour backlight, shallow depth of field, vertical 9:16",
      "duration": 8,
      "aspect_ratio": "9:16"
    }
  }'
```
Via MCP: `replicate-mcp predictions.create` with the same `version`/`input` body.

### 2. Veo 3.1 — sync audio (best for VO-free dialogue/SFX-driven shots)
```json
{
  "version": "google/veo-3.1",
  "input": {
    "prompt": "Cafe barista pulling an espresso shot, real cafe ambient sound, soft jazz playing faintly in the background",
    "duration": 8,
    "aspect_ratio": "16:9",
    "generate_audio": true
  }
}
```

### 3. Kling 3.0 — high motion (action / sports / dance)
```json
{
  "version": "kwaivgi/kling-v2.0",
  "input": {
    "prompt": "A skateboarder grinds a rail at sunset, camera dollies right tracking the subject",
    "duration": 5,
    "aspect_ratio": "9:16",
    "negative_prompt": "blurry, distorted, watermark"
  }
}
```

### 4. Runway Gen-4 Turbo — image-to-video w/ camera control
```json
{
  "version": "runwayml/gen-4-turbo",
  "input": {
    "image": "https://...hero.jpg",
    "prompt": "Camera slowly pushes in, subject's hair blows in soft wind",
    "duration": 10,
    "camera_motion": "push_in",
    "aspect_ratio": "16:9"
  }
}
```

### 5. Polling pattern (REST + MCP)
```bash
PRED_ID=$(curl -s ... | jq -r .id)
while true; do
  STATUS=$(curl -s -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
    https://api.replicate.com/v1/predictions/$PRED_ID | jq -r .status)
  [ "$STATUS" = "succeeded" ] && break
  [ "$STATUS" = "failed" ] && exit 1
  sleep 4
done
OUTPUT_URL=$(curl -s ... | jq -r .output)
curl -L "$OUTPUT_URL" -o clip.mp4
```
MCP path: call `predictions.create` returns ID; call `predictions.get(id)` in a loop.

### 6. Webhook pattern (preferred when CI/long runs)
Pass `"webhook": "https://your-host/cb"` in the body; Replicate POSTs back when status flips. Skips polling loop.

### 7. Chaining clips into a scene
Generate N short clips (each ≤8s) with consistent style prompts + matching seeds where supported. Then stitch with FFmpeg `xfade` (see `ffmpeg-multi-platform-export`).

### 8. Image-to-video for product B-roll
Start with a Flux 2 Pro photoreal still (see `replicate-ai-image-gen`), feed to Runway Gen-4 with `camera_motion: orbit` for 360° product turn.

### 9. Aspect ratio + duration constraints
| Model | Supported ARs | Max duration |
|---|---|---|
| Sora 2 | 16:9, 9:16, 1:1 | 20s (Pro), 8s (std) |
| Veo 3.1 | 16:9, 9:16 | 8s |
| Kling 3.0 | 16:9, 9:16, 1:1 | 10s |
| Runway Gen-4 Turbo | 16:9, 9:16, 4:3 | 10s |

### 10. Cost-control wrapper
Cap per-request: `duration <= 8 && estimated_cost < $5`. For a 60s vertical TikTok, **6× 10s Kling clips + xfade** = ~$17 (vs ~$45 with Veo 3.1).

## Examples

### A. 6-second TikTok hook
**Goal:** Cinematic close-up open for fashion vertical.
1. POST Sora 2 with `prompt: "Macro slow-motion of a silk fabric falling onto wood floor, golden hour"`, `duration: 6`, `aspect_ratio: 9:16` → ~$0.60.
2. Poll → download → pipe to FFmpeg loudnorm if Sora returned silent audio, or layer ElevenLabs SFX.

### B. 30-second product showcase (image-to-video chain)
1. Flux 2 Pro generates 3 photoreal product stills (different angles), seed-locked.
2. Each still → Runway Gen-4 Turbo with `camera_motion=orbit` (10s each).
3. FFmpeg `xfade=fade:duration=0.5` stitches the 3 clips → 30s output.
4. ElevenLabs VO laid over. Total cost: ~$15.

### C. Veo 3.1 talking-head w/ native audio
1. Single prompt: `"A 30-something developer at a coffee shop, talking to camera explaining a startup pivot, natural cafe ambience"`, `duration: 8`, `generate_audio: true`.
2. Output ships with sync audio — no separate VO pass needed.

### D. Hook + B-roll chain for a YouTube intro
Sora 2 first 3s (face close-up reveal) → FFmpeg `xfade` whip-pan → Kling 3.0 next 5s (action B-roll) → ElevenLabs VO over both.

## Edge cases / gotchas

1. **No deterministic seed on Sora 2.** Same prompt → different output each run. Lock style via specific descriptor language ("Kodak Portra 400 film stock, anamorphic"). Kling/Runway expose `seed`.
2. **Veo 3.1 audio includes speech.** If you want music-only, set `generate_audio=false` and add VO separately.
3. **Aspect ratio = ratio, not pixels.** Output dimensions vary by model — always FFmpeg `scale=` post-gen if you need exact 1080×1920.
4. **Cost spikes on `duration` mis-typing.** A typo of `80` instead of `8` for Veo 3.1 = $60. Wrap with input validation.
5. **Polling intervals < 2s are rate-limited.** Use 3–5s, or webhooks.
6. **`black-forest-labs` vs `bfl-labs` naming.** Check the exact `version` slug on `replicate.com/<model>/api` — they change.
7. **NSFW / IP filters** vary per model. Sora 2 is strict; Kling allows more. Be ready for `failed` status with safety-flagged input.
8. **Prediction objects retain output URLs for ~24h.** Always download immediately or re-host to S3/Cloudflare R2.
9. **Veo 3.1 native audio is mono.** If you need stereo BGM later, leave it silent and add stereo BGM in FFmpeg.
10. **Replicate sometimes returns array of outputs** (e.g., multiple frames). Check `.output[0]` vs `.output` — keep code defensive.

## Sources
- https://replicate.com/docs/reference/mcp
- https://replicate.com/docs/reference/http
- https://replicate.com/openai/sora-2
- https://replicate.com/google/veo-3.1
- https://replicate.com/kwaivgi/kling-v2.0
- https://replicate.com/runwayml/gen-4-turbo
