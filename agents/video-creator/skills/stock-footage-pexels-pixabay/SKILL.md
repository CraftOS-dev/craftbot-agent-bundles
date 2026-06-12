# Stock Footage — Pexels + Pixabay (Free APIs)

## When to use
- B-roll for explainers / talking-head videos
- Background plates for compositing
- Quick mood-board sourcing
- Royalty-free commercial-cleared footage without licensing fees

## Setup
- **Pexels API:** free, 200 requests/hour. Get key at https://www.pexels.com/api/
- **Pixabay API:** free, unlimited (within fair use). Get key at https://pixabay.com/api/docs/
- Auth via `cli-anything` + `curl` (no MCP wrappers needed)

## License terms
- **Pexels License** — free for commercial + personal use, no attribution required (attribution appreciated)
- **Pixabay Content License** — free for commercial + personal use, no attribution required
- Both prohibit: redistribution as stock, derivative-only use, sensitive person imagery without consent

## Common recipes

### 1. Pexels — video search by keyword
```bash
curl -H "Authorization: $PEXELS_KEY" \
  "https://api.pexels.com/videos/search?query=ocean+waves&orientation=landscape&size=large&per_page=15&page=1"
```
Returns array with `id`, `width`, `height`, `duration`, `video_files[]` (multiple resolutions).

### 2. Pexels — get a specific quality file
```bash
RESP=$(curl -H "Authorization: $PEXELS_KEY" "https://api.pexels.com/videos/search?query=cafe&per_page=5")
echo $RESP | jq '.videos[0].video_files[] | select(.width==1920 and .file_type=="video/mp4") | .link'
```

### 3. Pexels — popular videos
```bash
curl -H "Authorization: $PEXELS_KEY" "https://api.pexels.com/videos/popular?per_page=20"
```

### 4. Pixabay — video search
```bash
curl "https://pixabay.com/api/videos/?key=$PIXABAY_KEY&q=mountain&min_width=1920&per_page=20"
```
Returns array with `videos.large.url`, `videos.medium.url`, `videos.small.url`, `videos.tiny.url`.

### 5. Pixabay — image search (for thumbnails when Flux/Ideogram is overkill)
```bash
curl "https://pixabay.com/api/?key=$PIXABAY_KEY&q=coffee&image_type=photo&min_width=1920&per_page=20"
```

### 6. Pexels — image search
```bash
curl -H "Authorization: $PEXELS_KEY" "https://api.pexels.com/v1/search?query=coffee&orientation=landscape&per_page=15"
```

### 7. Batch download
```bash
RESP=$(curl -H "Authorization: $PEXELS_KEY" "https://api.pexels.com/videos/search?query=city&per_page=10")
echo $RESP | jq -r '.videos[] | .video_files[] | select(.quality=="hd" and .file_type=="video/mp4") | .link' | head -10 | while read URL; do
  ID=$(basename $URL .mp4)
  curl -L "$URL" -o "broll/pexels_$ID.mp4"
done
```

### 8. Pexels orientation + size filters
- `orientation=`: `landscape`, `portrait`, `square`
- `size=`: `large` (4K), `medium` (Full HD), `small` (HD)
- `locale=`: `en-US`, `es-ES`, etc. (search language)

### 9. Pixabay video category filters
`video_type=`: `all`, `film`, `animation`. `category=`: backgrounds, fashion, nature, science, education, feelings, health, people, religion, places, animals, industry, computer, food, sports, transportation, travel, buildings, business, music.

### 10. Rate-limit handling (Pexels 200/hr)
```python
# Naive cap
RATE_BUDGET = 200
last_minute = []
def call():
    now = time.time()
    last_minute[:] = [t for t in last_minute if t > now - 3600]
    if len(last_minute) >= RATE_BUDGET: time.sleep(60); return call()
    last_minute.append(now)
    # ...make request
```

### 11. Pagination
Both APIs support `page=N&per_page=15`. Loop until `next_page` is null (Pexels) or `total_hits` reached (Pixabay).

### 12. Curated stock with brand-safety check
After download, check duration / resolution:
```bash
ffprobe -v error -show_entries stream=width,height,duration -of json file.mp4
```
Reject anything <1080p or <5s.

### 13. Search with multi-keyword OR/AND (Pixabay supports `+`)
```bash
curl "https://pixabay.com/api/videos/?key=$PIXABAY_KEY&q=ocean+sunset"  # AND
```
Pexels treats spaces as AND-ish (relevance ranked).

### 14. Auto-attribution (even when not required, good practice)
For each downloaded asset, write a sidecar:
```json
{ "file": "pexels_12345.mp4", "source": "Pexels", "url": "https://www.pexels.com/video/12345/", "photographer": "Jane Doe", "license": "Pexels License" }
```

### 15. Multi-source dedup
Run Pexels + Pixabay both, hash filenames, dedupe by perceptual hash (`pHash`) if you suspect overlap.

## Examples

### A. Build a 30-clip B-roll library for a "city life" video
1. Pexels: query `city`, `traffic`, `subway`, `street` → 8 each.
2. Pixabay: same queries.
3. Filter to ≥1080p, ≥6s duration.
4. Save w/ attribution sidecars.
5. Total cost: 0; total time: ~5 min.

### B. Background plates for green-screen comp
1. Search `nature 4k forest` on Pexels with `size=large`.
2. Filter to landscape, ≥10s.
3. Download top-5 → composite in Remotion / DaVinci.

### C. Photo-only thumbnail variants
1. Pexels image search `business meeting`.
2. Top 10 → pick best.
3. Pipe to Photoshop MCP for face cutout + text overlay.

### D. Search across niche → curated pack
1. List of 20 keywords from script ("coffee", "espresso", "barista", "latte art", "morning routine"...).
2. Loop Pexels + Pixabay.
3. Best 3 per keyword.
4. Output: 60 curated clips with metadata.

## Edge cases / gotchas

1. **Pexels free key = 200 req/hr.** For bulk research, contact for higher tier.
2. **Pixabay "unlimited"** means within fair-use — sustained 100/s will get rate-limited.
3. **License does NOT permit reuploading to other stock platforms.** Don't sell Pexels clips on Storyblocks.
4. **Pexels duration field is in seconds**, Pixabay duration is in seconds too.
5. **Some videos have audio**, most don't. Always check before relying.
6. **Resolution metadata** can lie — `width=3840` but actual is 1920. Verify with ffprobe.
7. **Watermark-free at source** but Pexels reserves right to add watermark to API responses if abused.
8. **Search relevance varies** — Pexels is generally better quality, Pixabay has more breadth.
9. **No moderation API.** Manually review NSFW-adjacent searches (e.g., "fitness model" can return suggestive results).
10. **Person consent** — even with license, get release for any recognizable person used commercially.
11. **Generic clips become overused** — top-5 results for "city" appear in thousands of YouTube videos. For unique brand work, dig pages 3+.
12. **Aspect ratio mismatch** — most stock is 16:9. For vertical work, filter `orientation=portrait` (Pexels) or accept center-crop.

## Sources
- https://www.pexels.com/api/documentation/
- https://pixabay.com/api/docs/
- https://www.pexels.com/license/
- https://pixabay.com/service/license/
