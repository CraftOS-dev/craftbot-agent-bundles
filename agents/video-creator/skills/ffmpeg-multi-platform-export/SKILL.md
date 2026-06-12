# FFmpeg Multi-Platform Export Presets

## When to use
- Same master → exports for TikTok / Reels / Shorts / YouTube / Bilibili / Douyin
- Vertical re-crop from a horizontal master (or vice versa)
- Codec selection (H.264 default, H.265 for size, ProRes for masters)
- Proxy generation for 4K+ workflows
- `-movflags +faststart` for streamable MP4s

## Setup
- `ffmpeg-mcp-advanced` MCP primary
- Direct CLI via `cli-anything`
- Optional: presets stored as JSON in `presets/*.json` — agent reads, expands into args

## Per-platform spec table (June 2026)

| Platform | Aspect | Resolution | fps | Video bitrate | Codec | Audio | Notes |
|---|---|---|---|---|---|---|---|
| TikTok | 9:16 | 1080×1920 | 30 | 10 Mbps | H.264 | AAC 256k stereo | Sound on; 7-15s entertainment, 60s+ educational |
| TikTok 4K vertical | 9:16 | 2160×3840 | 30 | 25 Mbps | H.264/H.265 | AAC 256k | Premium creators |
| Instagram Reels | 9:16 | 1080×1920 | 30 | 12 Mbps | H.264 | AAC 256k | ≤90s |
| YouTube Shorts | 9:16 | 1080×1920 | 30/60 | 10–15 Mbps | H.264 | AAC 256k | ≤60s |
| YouTube 1080p | 16:9 | 1920×1080 | 30 | 12 Mbps | H.264 | AAC 384k | Standard upload |
| YouTube 4K60 | 16:9 | 3840×2160 | 60 | 45 Mbps | H.264 | AAC 384k | Premium |
| YouTube HDR | 16:9 | 3840×2160 | 60 | 60 Mbps | H.265 | AAC 384k | 10-bit |
| Bilibili | 16:9 | 1920×1080 | 30/60 | 15 Mbps | H.264 | AAC 320k | 4K+120fps = "High Quality" badge |
| Douyin | 9:16 | 1080×1920 | 30 | 10 Mbps | H.264 | AAC 256k | Chinese TikTok |
| LinkedIn | 16:9 or 1:1 | 1920×1080 | 30 | 10 Mbps | H.264 | AAC 256k | ≤10min, B2B |
| Master (archival) | source | source | source | 80–150 Mbps | ProRes 422 HQ | PCM 24-bit | Apple ecosystem master |

## Common recipes

### 1. TikTok vertical export
```bash
ffmpeg -i master.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" \
  -c:v libx264 -preset slow -b:v 10M -maxrate 12M -bufsize 20M \
  -c:a aac -b:a 256k -ar 48000 \
  -movflags +faststart \
  tiktok.mp4
```

### 2. YouTube Shorts (same as TikTok but 30 or 60 fps)
```bash
ffmpeg -i master.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30" \
  -c:v libx264 -preset slow -b:v 12M \
  -c:a aac -b:a 256k -ar 48000 -movflags +faststart \
  shorts.mp4
```

### 3. YouTube 1080p horizontal
```bash
ffmpeg -i master.mp4 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
  -c:v libx264 -preset slow -b:v 12M \
  -c:a aac -b:a 384k -ar 48000 -movflags +faststart \
  yt1080.mp4
```

### 4. YouTube 4K60
```bash
ffmpeg -i master_4k.mov \
  -c:v libx264 -preset slow -b:v 45M -maxrate 60M -bufsize 90M -r 60 \
  -c:a aac -b:a 384k -ar 48000 -movflags +faststart \
  yt4k60.mp4
```

### 5. H.265 (smaller files, premium devices)
```bash
ffmpeg -i master.mp4 \
  -c:v libx265 -crf 23 -preset slow -tag:v hvc1 \
  -c:a aac -b:a 256k -movflags +faststart \
  h265.mp4
```
`-tag:v hvc1` makes the file QuickTime/Apple compatible. Without it, Apple devices refuse to play.

### 6. ProRes master
```bash
ffmpeg -i edit.mp4 \
  -c:v prores_ks -profile:v 3 -vendor apl0 -pix_fmt yuv422p10le \
  -c:a pcm_s24le -ar 48000 \
  master.mov
```
Profiles: `0`=Proxy, `1`=LT, `2`=Std, `3`=HQ, `4`=4444.

### 7. Bilibili (sub-100MB target for free upload)
```bash
ffmpeg -i master.mp4 \
  -c:v libx264 -preset slow -b:v 15M -r 60 \
  -c:a aac -b:a 320k \
  -movflags +faststart \
  bili.mp4
```

### 8. Proxy generation (mandatory for 4K+ editing per role.md)
```bash
ffmpeg -i RAW.mov -vf "scale=1280:720" \
  -c:v dnxhd -b:v 36M -c:a pcm_s16le -ar 48000 \
  proxy.mov
```
Or H.264 proxy:
```bash
ffmpeg -i RAW.mov -vf "scale=1280:720" \
  -c:v libx264 -preset ultrafast -crf 28 -c:a aac -b:a 128k \
  proxy.mp4
```

### 9. Batch export all platforms from one master
```bash
PRESETS=("tiktok" "shorts" "reels" "yt1080" "yt4k60" "bili")
for P in "${PRESETS[@]}"; do
  bash presets/$P.sh master.mp4 out/$P.mp4
done
```
Each `presets/<name>.sh` calls FFmpeg with platform args.

### 10. JSON preset library template
```json
{
  "name": "tiktok",
  "video": {
    "scale": "1080:1920:force_original_aspect_ratio=increase",
    "crop": "1080:1920",
    "codec": "libx264",
    "bitrate": "10M",
    "preset": "slow",
    "fps": 30
  },
  "audio": { "codec": "aac", "bitrate": "256k", "ar": 48000 },
  "muxing": { "movflags": "+faststart" }
}
```
Agent reads JSON, builds ffmpeg arg list, executes via `ffmpeg-mcp-advanced`.

### 11. Vertical crop with subject tracking
FFmpeg cannot auto-track. For static center-crop:
`crop=1080:1920:in_w/2-540:0`. For face-tracked crop, use Adobe Sensei or DaVinci's Smart Reframe (DaVinci Python API skill).

### 12. Letterbox/pillarbox padding instead of crop (preserve full frame)
```bash
ffmpeg -i in.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black" out.mp4
```

### 13. Two-pass H.264 (smallest file at target quality)
```bash
ffmpeg -y -i in.mp4 -c:v libx264 -b:v 10M -pass 1 -an -f mp4 /dev/null && \
ffmpeg -i in.mp4 -c:v libx264 -b:v 10M -pass 2 -c:a aac -b:a 256k out.mp4
```

### 14. Burn-in subtitles + export in one pass
```bash
ffmpeg -i master.mp4 \
  -vf "subtitles=captions.ass:force_style='FontName=Inter,Outline=2',scale=1080:1920" \
  -c:v libx264 -preset slow -b:v 10M \
  -c:a aac -b:a 256k -movflags +faststart \
  tiktok_subbed.mp4
```

### 15. Hardware acceleration (NVENC / VideoToolbox / QSV)
```bash
# NVIDIA
ffmpeg -hwaccel cuda -i in.mp4 -c:v h264_nvenc -preset slow -b:v 12M -c:a aac out.mp4
# Apple Silicon
ffmpeg -i in.mp4 -c:v h264_videotoolbox -b:v 12M -c:a aac out.mp4
```
5–10× faster than libx264, slightly larger files at same bitrate.

## Examples

### A. Single edit → 5 platform deliverables
```bash
MASTER=master.mp4
for P in tiktok shorts reels yt1080 bili; do
  bash presets/$P.sh "$MASTER" "out/$P.mp4"
done
```
Result: 5 platform-perfect files in one run.

### B. 4K-to-1080p downscale for slow viewers
```bash
ffmpeg -i 4k.mov -vf "scale=1920:1080:flags=lanczos" -c:v libx264 -crf 18 -preset slow -c:a copy 1080.mp4
```

### C. Proxy editing workflow
1. Generate 720p DNxHD proxies (recipe 8) for all 4K source files.
2. Edit on proxies in NLE / Remotion.
3. Final pass: relink to 4K sources, run export presets.

### D. Faststart fix on existing MP4
```bash
ffmpeg -i in.mp4 -c copy -movflags +faststart out.mp4
```
Moves the moov atom to file head — required for browser streaming. Lossless re-mux.

## Edge cases / gotchas

1. **`scale` order matters.** `scale=W:H:force_original_aspect_ratio=increase,crop=W:H` for fill; `decrease,pad=` for letterbox. Mixing them up produces stretched output.
2. **`-c:v copy`** skips re-encode (fast) but breaks if filters are applied. Use only for trimming/remuxing.
3. **Aspect ratio mismatches in `crop`** silently produce black bars. Verify with `ffprobe`.
4. **YouTube re-encodes everything.** Don't over-compress your upload; YT prefers slightly higher bitrate for transcode quality.
5. **TikTok caps uploads at ~4 GB.** 4K vertical can hit this for long-form.
6. **`-movflags +faststart` requires a second pass internally** — slight extra time but mandatory for web streaming.
7. **H.265 fragmentation.** Some Android devices, older browsers, and Premiere Pro can't play `hvc1` reliably; ship H.264 for max compat.
8. **`fps=` filter forces** — pads or drops frames. For temporal accuracy, match source.
9. **`-preset slow` doubles encode time** vs `medium`; `veryslow` quadruples. `slow` is the sweet spot for delivery.
10. **Audio sample rate.** Some platforms transcode 44.1k → 48k poorly. Always `-ar 48000` for video deliverables.
11. **`-shortest`** stops at shortest stream when muxing audio + video; without it you get trailing silence.
12. **Subtitle filter font path.** `force_style='FontName=Inter'` only works if Inter is system-installed; otherwise falls back to default sans.

## Sources
- https://ffmpeg.org/ffmpeg-filters.html#scale-1
- https://ffmpeg.org/ffmpeg-filters.html#crop
- https://trac.ffmpeg.org/wiki/Encode/H.264
- https://trac.ffmpeg.org/wiki/Encode/H.265
- https://support.google.com/youtube/answer/1722171 (YouTube upload encoding settings)
- https://creators.tiktok.com/help/article?aid=10042422 (TikTok upload specs)
