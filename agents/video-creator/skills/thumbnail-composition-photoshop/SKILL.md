# Thumbnail Composition — AI gen + Photoshop MCP

## When to use
- You generated a Flux 2 Pro / Ideogram 3.0 hero and need final composition
- Vertical (9:16) thumbnail per role.md rule: person 60%+, 3–8 char text, exaggerated expression
- Horizontal (16:9) YouTube thumbnail: text-image split, mobile-readable
- A/B variant generation
- Brand watermark insertion

## Setup
- `photoshop-mcp` (already wired in `agent.yaml`) — bridges to Adobe Photoshop UXP API
- Alt: `gimp-mcp` for open-source path
- Auth: Photoshop must be running locally (UXP plugin), or use cloud Adobe Express API if user opts in

## Common recipes

### 1. AI gen → Photoshop import
```python
# via photoshop-mcp
ps.open(path="C:/thumbs/raw_ideogram.png")
ps.select_subject()                      # AI subject mask
ps.refine_edge(radius=2, shift_edge=-5)  # tighten edge
ps.export(format="png", path="cutout.png", transparent=True)
```

### 2. Text overlay
```python
ps.add_text_layer(
  text="WAIT FOR IT",
  font="Impact",
  size=180,
  color="#FFFFFF",
  position=(540, 200),
  stroke_color="#000000",
  stroke_width=8,
  drop_shadow={"distance": 6, "blur": 10, "opacity": 0.7}
)
```

### 3. Brand color background fill
```python
ps.new_layer(below="subject")
ps.fill(color="#FFEE00")  # neon yellow
```

### 4. A/B variant from 4 Ideogram seeds
1. Generate 4 backgrounds at `seed=1,2,3,4`.
2. For each, composite the SAME subject + SAME text.
3. Export 4 candidates → A/B test.

### 5. Vertical (9:16) layout (TikTok / Shorts / Reels thumbnail)
- Canvas: 1080×1920
- Subject: fills 60%+ of frame (per role.md)
- Text: 3–8 chars, anchored top or bottom third
- Stroke: 6–10px black on white text (mobile-readable)
- Drop shadow: blur 10, offset 6

### 6. Horizontal (16:9) layout (YouTube thumbnail)
- Canvas: 1280×720 (standard) or 1920×1080 (premium)
- Composition options:
  - text-left/image-right
  - text-top/image-bottom
  - text-center w/ subject behind
- Key info center-or-slightly-above
- Text: large, ≤6 words, high-contrast

### 7. Save-for-web export
```python
ps.export(format="jpg", path="thumb_final.jpg", quality=85, progressive=True)
```
Target file size: <2 MB for YouTube upload.

### 8. Mobile readability check
Render a 200×356 (9:16) preview — if text is readable at that size, you're good for phones.

### 9. Face cutout fallback (no Photoshop, use Replicate)
```bash
curl -X POST https://api.replicate.com/v1/predictions \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" -H "Content-Type: application/json" \
  -d '{"version":"851-labs/background-remover","input":{"image":"https://...face.jpg"}}'
```
Returns transparent PNG. Then composite via FFmpeg `overlay` filter or GIMP.

### 10. FFmpeg-only thumbnail composition (when Photoshop unavailable)
```bash
ffmpeg -i background.png -i subject.png -i text.png -filter_complex "
  [0:v][1:v]overlay=(W-w)/2:H-h[bg_sub];
  [bg_sub][2:v]overlay=0:50
" -frames:v 1 thumb.png
```

### 11. Bulk thumbnail generation (one template, N data points)
```python
# Pseudocode — apply same Photoshop action to N rows of data
for row in csv.reader(open("titles.csv")):
    ps.set_text("HEADLINE", row["title"])
    ps.replace_image("HERO", row["hero_path"])
    ps.export(f"thumbs/{row['id']}.jpg", quality=85)
```

### 12. Title + thumbnail synergy rule
Don't repeat the title text in the thumbnail. Title = context; thumbnail = visual hook. They should complement.
- Title: "I tried 5 espresso machines so you don't have to"
- Thumb text: "$50 vs $5,000"
- Thumb subject: shocked face holding two cups

### 13. Watermark-aware composition
- Vertical thumbnails: leave 15% top + bottom padding (platform UI hides those zones)
- No third-party platform logos (role.md: TikTok logo on YouTube thumb = guaranteed throttling)

### 14. Color palette extraction (match thumbnail to brand)
```python
ps.select_color_range(image="hero.jpg", n_colors=5)
# Returns top-5 dominant hex codes; use as accent color choices
```

### 15. CTR-optimization heuristics (per `msitarzewski-video-optimization-specialist`)
- Person face with strong emotion (surprise, joy, confusion) — neutral doesn't convert
- High contrast — use complementary colors, not analogous
- 3-color rule — 1 dominant + 1 accent + 1 neutral; more = visual noise
- Mobile preview test — readability at 200px width is the gate

## Examples

### A. Vertical TikTok thumbnail (CapCut replacement)
1. Ideogram 3.0: `"Vertical 9:16, neon yellow background, large white text 'WAIT FOR IT'"`, seeds 1–4.
2. Pick best seed → Photoshop MCP open.
3. `select_subject()` on a separately-generated hero shot.
4. Composite onto Ideogram bg.
5. Text layer override (font + stroke + shadow tuned).
6. Export 4 variants → A/B.

### B. YouTube horizontal CTR-optimized
1. Flux 2 Pro photoreal subject (`aspect_ratio: 16:9`).
2. Photoshop subject cutout.
3. Place on punchy gradient background.
4. Impact font headline left, subject right.
5. Brand logo bottom-right corner (small, ≤8% of frame).
6. Export 3 variants for A/B.

### C. Series-consistent thumbnails
Define a Photoshop action recording the template. Apply same action to N hero images → series-uniform thumbnails.

### D. No-Photoshop path (Replicate bg-remover + FFmpeg overlay)
1. Replicate `851-labs/background-remover` on raw face shot → transparent PNG.
2. Ideogram generates bg + text.
3. FFmpeg `overlay` composites them.
Works headless; lower polish than Photoshop but reasonable.

## Edge cases / gotchas

1. **Photoshop MCP requires Photoshop running locally with UXP plugin.** No headless path; use GIMP MCP or FFmpeg overlay for CI.
2. **`select_subject` mis-fires** on busy backgrounds — verify mask before committing.
3. **JPEG artifacts on text edges.** Export PNG for crisp text, or JPEG at quality≥90.
4. **YouTube reject thumbnails >2 MB.** Lower JPEG quality or downscale.
5. **Aspect ratio mismatch with platform.** TikTok strictly 9:16; uploading 1:1 gets center-cropped.
6. **Faces of minors / public figures** — moderation rules apply. Get release/consent.
7. **Bold typography requires font installed.** Impact / Bebas Neue / Anton — confirm in PS font list before scripting.
8. **Transparent PNGs** with shadow may show outline halo — use `refine_edge(shift_edge=-3)` to suppress.
9. **Hand-drawn variants** via Recraft (vector) can be a CTR differentiator vs everyone else's photoreal.
10. **A/B test cadence** — give each variant 48–72 hrs before swap; YouTube has a built-in test tool for this.
11. **Brand-mandated colors** sometimes lose to high-contrast neon. If brand allows, lean toward conversion.
12. **Avoid clickbait that mismatches content** (role.md) — burns trust and tanks retention.

## Sources
- https://developer.adobe.com/photoshop/uxp/2022/uxp-api/
- https://replicate.com/851-labs/background-remover
- https://creatoracademy.youtube.com/page/lesson/thumbnails (YouTube thumbnail guidelines)
