# FFmpeg Color Grading (LUT 3D + Primary/Secondary)

## When to use
- You have a creative LUT (`.cube`) and want it applied at 60–80% opacity (per role.md rule)
- You need primary correction (white balance, exposure, contrast) without booting an NLE
- You need batch grading across a folder of clips with one recipe
- You want one of the 5 stylistic looks (cinematic / Japanese fresh / cyberpunk / vintage / Morandi)

Skip when the user wants interactive scopes (vectorscope, waveform) → use DaVinci Resolve Python API instead.

## Setup
- `ffmpeg-mcp-advanced` MCP is the primary execution path
- Direct shell fallback via `cli-anything` + system `ffmpeg`
- LUT files: `.cube` format (Adobe / Resolve / Premiere compatible). Source: Lutify.me, FreshLUTs, IWLTBAP (free + commercial)
- Ensure ffmpeg was built with `--enable-gpl --enable-libfreetype` (most distros' default)

## Common recipes

### 1. Apply a LUT (tetrahedral interp, default opacity)
```bash
ffmpeg -i in.mp4 -vf "lut3d=cinematic.cube:interp=tetrahedral" graded.mp4
```
Interpolation modes: `nearest` (fast, blocky), `trilinear` (default, ok), `tetrahedral` (best, recommended for hero shots).

### 2. LUT at 60-80% opacity (proper blend)
```bash
ffmpeg -i in.mp4 -filter_complex "
  [0:v]split[a][b];
  [b]lut3d=cinematic.cube:interp=tetrahedral[graded];
  [a][graded]blend=all_mode=normal:all_opacity=0.7
" -c:a copy graded70.mp4
```
This produces a 70%-strength LUT — the role.md sweet spot.

### 3. Primary correction with `eq` filter
```bash
ffmpeg -i in.mp4 -vf "eq=brightness=0.05:contrast=1.15:saturation=0.9:gamma=1.05" out.mp4
```
- `brightness`: -1.0 to 1.0
- `contrast`: 0.0 (none) to 2.0 (heavy)
- `saturation`: 0.0 (B&W) to 3.0
- `gamma`: 0.1 to 10.0; 1.0 = none; >1 lifts midtones

### 4. White balance — colorbalance filter
```bash
ffmpeg -i in.mp4 -vf "colorbalance=rs=-0.1:gs=0:bs=0.1:rm=0:gm=0:bm=0:rh=0:gh=0:bh=0" wb.mp4
```
`rs/gs/bs` = shadows R/G/B (-1..1), `rm/gm/bm` = midtones, `rh/gh/bh` = highlights. To cool the shadows + warm the highlights: `rs=-0.1:bs=0.1:rh=0.1:bh=-0.1`.

### 5. Curves filter (per-channel tone curves)
```bash
ffmpeg -i in.mp4 -vf "curves=red='0/0 0.5/0.6 1/1':blue='0/0.1 0.5/0.5 1/0.9'" curves.mp4
```
Preset curves available: `vintage`, `negative`, `lighter`, `darker`, `increase_contrast`, `medium_contrast`, `strong_contrast`, `none`.

### 6. Secondary correction — HSL via hue
```bash
ffmpeg -i in.mp4 -vf "hue=h=10:s=1.05" hue.mp4
```
- `h`: hue shift in degrees (-180..180)
- `s`: saturation multiplier
For targeted color shift (sky only), use a masked filter chain — see recipe 12.

### 7. Technical LUT (S-Log3 → Rec.709)
Apply BEFORE creative grade.
```bash
ffmpeg -i slog3.mp4 -vf "lut3d=slog3_to_rec709.cube:interp=tetrahedral" rec709.mp4
```
Then layer a creative LUT on `rec709.mp4`.

### 8. Full pipeline (LOG → Rec.709 → primary → creative LUT 70%)
```bash
ffmpeg -i raw_slog3.mp4 -filter_complex "
  [0:v]lut3d=slog3_to_rec709.cube:interp=tetrahedral,
       eq=contrast=1.1:saturation=0.95:gamma=1.0,
       colorbalance=bs=0.05:rh=0.05[base];
  [base]split[primary][forlut];
  [forlut]lut3d=cinematic.cube:interp=tetrahedral[creative];
  [primary][creative]blend=all_mode=normal:all_opacity=0.7
" -c:a copy final.mp4
```

### 9. Skin tone protection — vibrance over saturation
FFmpeg has no direct `vibrance` filter; closest is `eq=saturation=` + curves protecting orange-yellow band:
```bash
ffmpeg -i in.mp4 -vf "curves=psfile='skin_protect.acv',eq=saturation=1.1" out.mp4
```
Use ACV preset exported from Photoshop.

### 10. Stylistic preset library (5 looks from role.md)

**Cinematic (teal-orange):**
```
lut3d=cinematic_teal_orange.cube:interp=tetrahedral
+ eq=saturation=0.85:contrast=1.2:gamma=1.05
+ colorbalance=rs=-0.05:bs=0.08:rh=0.1:bh=-0.05
+ noise=alls=2:allf=t          # subtle grain
```

**Japanese fresh:**
```
eq=brightness=0.05:saturation=0.85:contrast=0.95:gamma=1.1
+ colorbalance=gs=0.05:bs=0.05:gh=-0.03
+ curves=preset=lighter
```

**Cyberpunk:**
```
lut3d=cyberpunk.cube + eq=saturation=1.3:contrast=1.3 + curves=preset=strong_contrast
```

**Vintage film:**
```
curves=preset=vintage + eq=saturation=0.7 + colorbalance=rs=0.1:gs=0.05 + noise=alls=8:allf=t
```

**Morandi (low-sat lifestyle):**
```
eq=saturation=0.6:contrast=0.95:gamma=1.05 + colorbalance=rs=0.05:bs=0.05:rh=0.03
```

### 11. Custom LUT export (export your grade as a `.cube`)
FFmpeg can identify-test, not author. Use DaVinci Resolve to export a `.cube` from your color page, then use it in FFmpeg.

### 12. Targeted sky enhancement (mask + filter chain)
```bash
ffmpeg -i in.mp4 -filter_complex "
  [0:v]colorkey=color=0x6BAEDB:similarity=0.3:blend=0.2[sky];
  [0:v][sky]overlay,
  eq=saturation=1.15
" sky.mp4
```
This is rough — DaVinci's qualifier tool is much better for surgical secondary correction.

### 13. Batch grade a folder
```bash
for F in raw/*.mp4; do
  OUT="graded/$(basename $F)"
  ffmpeg -i "$F" -vf "lut3d=cinematic.cube:interp=tetrahedral,eq=saturation=0.85:contrast=1.15" -c:a copy "$OUT"
done
```

### 14. Color match between clips (histogram-based)
FFmpeg has no native color match. Workaround: extract frame from clip A, derive its LUT via DaVinci or `colour-science` Python, apply to clip B.

### 15. Verify with vectorscope / waveform
```bash
ffplay -i graded.mp4 -vf "split=4[a][b][c][d];[a]waveform=m=column:c=7[a];[b]vectorscope=m=color3[b];[c]histogram[c];[c][d]hstack=inputs=2"
```
Real-time scopes in ffplay window.

## Examples

### A. S-Log3 to delivery with cinematic look
```bash
ffmpeg -i sony_a7s3.mp4 -filter_complex "
  [0:v]lut3d=sony_slog3_to_rec709.cube:interp=tetrahedral,
       eq=contrast=1.1:saturation=0.9[base];
  [base]split[p][c];
  [c]lut3d=cinematic_teal_orange.cube:interp=tetrahedral[lut];
  [p][lut]blend=all_mode=normal:all_opacity=0.7,noise=alls=3:allf=t
" -c:v libx264 -crf 18 -preset slow -c:a copy delivery.mp4
```

### B. Match-grade a 5-clip sequence
1. Pick "hero" clip (the best-exposed one) → derive look manually.
2. Apply same filter chain to all 5 with `for F in clips/*.mp4`.
3. Output: visually consistent set ready for editing.

### C. Quick Morandi look for a lifestyle reel
```bash
ffmpeg -i in.mp4 -vf "eq=saturation=0.6:contrast=0.95:gamma=1.05,colorbalance=rs=0.05:rh=0.03" -c:a copy morandi.mp4
```

### D. Per-clip LUT opacity for hero vs B-roll
- Hero shots: LUT at 50% (preserve more skin tone fidelity)
- B-roll: LUT at 80% (push the look harder)
- Title cards: LUT at 100% (full stylization)

## Edge cases / gotchas

1. **`lut3d` with `nearest` looks blocky.** Always `tetrahedral` for delivery; `trilinear` only when speed matters.
2. **`-c copy` skips video re-encode**, so filters require explicit `-c:v libx264` (or similar).
3. **`blend=all_opacity=0.7` requires identical-format inputs.** Both must be same pixel format; use `format=yuv420p` upstream.
4. **`.cube` files must be UTF-8, LF line endings.** Windows-CRLF cubes silently fail or load wrong.
5. **`eq=saturation=0`** is true black-and-white but `hue=s=0` is too — pick one.
6. **`colorbalance` is linear, not perceptual.** Small values (±0.05–0.1) go a long way.
7. **Bit depth.** For 10-bit HDR, use `format=yuv420p10le` and `-c:v libx265 -pix_fmt yuv420p10le`.
8. **`curves=preset=`** values are baked in — to tune, supply explicit `red=`/`green=`/`blue=` strings.
9. **`noise=alls=N`** — N=2–4 is "tasteful grain", N=8+ is "old film", N>15 is unwatchable.
10. **Audio passthrough.** Always `-c:a copy` (or specify `-c:a aac -b:a 256k`) — otherwise FFmpeg re-encodes to default and you lose quality.
11. **CRF varies by codec.** libx264 CRF 18 = visually lossless. libx265 CRF 23 ≈ libx264 CRF 18.
12. **`-preset slow`** = ~2× slower than `medium`, but 10–20% smaller files for delivery.

## Sources
- https://ffmpeg.org/ffmpeg-filters.html#lut3d
- https://ffmpeg.org/ffmpeg-filters.html#eq
- https://ffmpeg.org/ffmpeg-filters.html#colorbalance
- https://ffmpeg.org/ffmpeg-filters.html#curves
- https://ffmpeg.org/ffmpeg-filters.html#blend
- https://trac.ffmpeg.org/wiki/Encode/H.264
