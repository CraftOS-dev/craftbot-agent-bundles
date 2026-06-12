# Replicate AI Image Generation (Flux 2 Pro / Ideogram 3.0 / Recraft)

## When to use
- Thumbnails (vertical 9:16 or horizontal 16:9)
- Storyboard panels for pre-production decks
- Title cards with embedded typography
- Photoreal product hero stills (then feed to Runway Gen-4 for image-to-video)
- A/B variant generation via `seed=` permutation

## Setup
- Auth via `replicate-mcp` (same `REPLICATE_API_TOKEN` as video gen)
- Direct REST fallback via `cli-anything` + `curl`

## Model lineup (June 2026)

| Model | Slug | Strength | Cost/image | Notes |
|---|---|---|---|---|
| Flux 2 Pro | `black-forest-labs/flux-2-pro` | Photoreal, depth, lighting | ~$0.04 | Top choice for hero / product |
| Flux 2 Dev | `black-forest-labs/flux-2-dev` | Faster, slightly lower fidelity | ~$0.025 | Bulk variants |
| Ideogram 3.0 | `ideogram-ai/ideogram-v3` | **Typography in image** | ~$0.05 | Best for any text-on-image (thumbnails, posters) |
| Recraft v3 | `recraft-ai/recraft-v3` | Vector + raster + brand styles | ~$0.04 | Iconography, illustration, logo-friendly |
| Imagen 4 | `google/imagen-4` | Photoreal alt to Flux | ~$0.04 | Different aesthetic bias |
| SD 3.5 Large | `stability-ai/stable-diffusion-3.5-large` | Open weights tradition | ~$0.03 | Local-runnable too |

## Common recipes

### 1. Flux 2 Pro — photoreal hero
```json
POST https://api.replicate.com/v1/predictions
{
  "version": "black-forest-labs/flux-2-pro",
  "input": {
    "prompt": "Studio portrait of a 30yo woman, soft window light from left, neutral grey backdrop, Kodak Portra 400 film, shallow depth of field, sharp eye focus",
    "aspect_ratio": "9:16",
    "output_format": "png",
    "output_quality": 95,
    "seed": 42
  }
}
```

### 2. Ideogram 3.0 — typography-strong thumbnail
```json
{
  "version": "ideogram-ai/ideogram-v3",
  "input": {
    "prompt": "YouTube thumbnail: bold headline 'I QUIT MY JOB' in white impact font with thick black stroke, shocked male face on right, neon yellow background, high contrast, 16:9",
    "aspect_ratio": "16:9",
    "style_type": "design",
    "magic_prompt_option": "on"
  }
}
```

### 3. Seed-locked A/B variants (4-up grid)
Run same `prompt`, vary `seed` across `[1, 2, 3, 4]`. Returns 4 distinct compositions sharing style. Used for thumbnail A/B testing.

### 4. Recraft — vector iconography
```json
{
  "version": "recraft-ai/recraft-v3",
  "input": {
    "prompt": "Flat vector icon set: rocket, gear, lightbulb, target — single colour line art, brand orange #FF6B35",
    "style": "vector_illustration",
    "aspect_ratio": "1:1"
  }
}
```

### 5. Image-to-image refine (Flux 2 redux)
```json
{
  "version": "black-forest-labs/flux-2-pro",
  "input": {
    "image": "https://...rough.jpg",
    "prompt": "Same composition, change lighting to golden hour, add warm rim light",
    "prompt_strength": 0.6
  }
}
```

### 6. Storyboard batch — six panels
Loop `prompt` over 6 narrative beats with shared prefix (`"Storyboard frame: pencil sketch, monochrome, ..."`). Save to `01-assets/storyboards/`.

### 7. Aspect ratios cheat sheet
- YouTube thumbnail: `16:9` (1280×720, 1920×1080)
- Vertical thumbnail / cover: `9:16`
- Square (Instagram feed, Spotify cover): `1:1`
- LinkedIn cover: `4:1` (rare, fallback to crop)

### 8. Prompt engineering for typography
Ideogram is strongest when you:
- Quote the exact text (`"I QUIT MY JOB"`)
- Specify font style (`impact font`, `serif handwritten`, `condensed sans`)
- Specify stroke / shadow (`thick black stroke`, `drop shadow`)
- Specify color contrast (`white text on neon yellow`)
- Set `style_type: design` for poster/thumb output

### 9. Magic prompt expansion (Ideogram)
Set `magic_prompt_option: "on"` and Ideogram auto-expands your terse prompt. Useful when iterating. Turn off (`"off"`) when you have an already-detailed prompt you want literal.

### 10. Batch download + organize
```bash
PROMPTS=("hero shot" "B-roll 1" "B-roll 2")
for i in "${!PROMPTS[@]}"; do
  RESP=$(curl -X POST https://api.replicate.com/v1/predictions \
    -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"version\":\"black-forest-labs/flux-2-pro\",\"input\":{\"prompt\":\"${PROMPTS[$i]}\",\"seed\":$i}}")
  PRED_ID=$(echo $RESP | jq -r .id)
  # poll then curl -L $URL -o thumb_$i.png
done
```

## Examples

### A. Vertical TikTok thumbnail
1. Ideogram 3.0: `"Vertical 9:16 thumbnail, large white text 'WAIT FOR IT' top half, shocked person face bottom half, neon green background"` → `seed=1`.
2. Generate variants `seed=2,3,4` for A/B testing.
3. Hand off best variant to `thumbnail-composition-photoshop` for face cleanup + brand watermark.

### B. YouTube horizontal thumbnail
1. Ideogram 3.0 first pass: `"YouTube thumbnail 16:9: 'I BUILT THIS IN 24H' on left in impact font, hero shot of product on right"`.
2. Pick best of 4 seeds.
3. Photoshop MCP: cut out face/subject, drop on punchier background, increase text weight.

### C. Photoreal product hero → Runway image-to-video
1. Flux 2 Pro: `"Studio product shot: matte black headphones on grey background, studio rim light, 4K commercial photography"`, `aspect_ratio: 16:9`, `output_quality: 100`.
2. Pipe URL into Runway Gen-4: `camera_motion: orbit`, `duration: 10` → 360° product turn clip.

### D. 6-panel storyboard for pre-prod deck
Loop 6 narrative beats with prefix `"Storyboard sketch, pencil on paper, monochrome:"`. Compose into PPTX via `pptx` skill, one frame per slide + voiceover notes.

## Edge cases / gotchas

1. **Ideogram text accuracy degrades past ~10 words.** For long titles, generate the background separately and overlay text in Photoshop.
2. **Flux 2 Pro can refuse named real people.** Use generic descriptors ("a 30-something businessman") not "Steve Jobs".
3. **Aspect ratio in prompt vs param.** Prompt-level "vertical 9:16" + `aspect_ratio: "16:9"` param → undefined behavior. Match them.
4. **PNG vs WebP.** `output_format: webp` is ~3× smaller but Photoshop MCP can struggle — stick to PNG for downstream editing.
5. **Seeds aren't perfectly reproducible across model versions.** Pin `version` slug to a digest when consistency matters.
6. **Magic prompt rewrites your text.** If you need exact text, set `magic_prompt_option: "off"`.
7. **Recraft style names matter.** `vector_illustration`, `realistic_image`, `digital_illustration` — check docs; wrong name silently falls back.
8. **Output URLs expire in ~24h.** Always re-host immediately.
9. **Thumbnail platforms compress hard.** Generate at 1.5× target res for clarity post-compression.
10. **For 4-up grid A/B test, varying `seed` is faster than varying `prompt`** — same model state, different randomness.

## Sources
- https://replicate.com/black-forest-labs/flux-2-pro
- https://replicate.com/ideogram-ai/ideogram-v3
- https://replicate.com/recraft-ai/recraft-v3
- https://replicate.com/docs/reference/http
