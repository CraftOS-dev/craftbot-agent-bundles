# Video Creator — Use Cases

**Tier:** specialized (subset of marketing) · **Category:** creative / video
**Core job:** Direct video production for marketing — hooks, scripts, color/audio direction, multi-platform optimization, thumbnail concepts.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

> 🎬 **Execution status (June 2026):** unlike v0, this agent now ships with the full SOTA media + AI generation stack. With `replicate-mcp` (Sora 2 / Veo 3.1 / Flux 2 Pro / Kling / Runway), `elevenlabs-mcp` (voice), `ffmpeg-mcp-advanced` (editing/color/audio), `photoshop-mcp` (thumbnail composition), and `cli-anything` (Remotion / Whisper.cpp / DaVinci Python API / Pexels-Pixabay APIs), the agent can now **execute** end-to-end video production — not just direct it. See "Execution status (SOTA — June 2026)" below for per-use-case mechanisms.

---

## What this agent is supposed to do

### Script + pre-production
- Hooks (3-second rule short-form, 15-second long-form)
- Script structure (setup → conflict → resolution)
- Shot lists (scale, movement, description, duration)
- B-roll lists
- Storyboards (as text + decks)
- 3-5 title variations + 2-3 thumbnail concepts

### Editing direction
- 5-step workflow (requirements → rough cut → fine cut → color/audio/subs → export)
- Frame-accurate cut points
- Transition selection (7 transition types with rules)
- Speed ramping (constant vs curve, beat-synced)
- Multi-cam edit planning

### Color grading direction
- Technical LUT (if LOG footage) → primary correction → secondary correction → stylistic grade
- Primary (white balance, exposure, contrast, highlights/shadows)
- Secondary (HSL, curves, masks, skin tones on vectorscope)
- LUT opacity 60-80% (never 100%)
- 5 stylistic directions (cinematic / Japanese fresh / cyberpunk / vintage / Morandi)
- Consistency within video and across series

### Audio engineering direction
- Voice: noise reduction + EQ (high-pass 80-120Hz, boost 2-5kHz clarity) + compressor (3:1-4:1) → -12 to -6 dB
- BGM beat-syncing on downbeats only
- Sound design (ambient / action / mood)
- Mix balance (voice priority #1)
- Final loudness -14 LUFS, peak ≤ -1 dBFS
- AI voice enhancement direction

### Motion graphics direction
- Keyframe animation (position, scale, rotation, opacity)
- Easing curves (linear feels mechanical)
- Text animation (5 styles, 0.3-0.5s duration)
- Particle effects
- Green screen / smart cutout direction
- Speed ramping (fast-slow-fast)

### Subtitle work
- AI auto-generation direction (CapCut, Whisper, ByteDance Volcano) → manual review
- Decorative text styling (stroke, shadow, gradient, texture)
- Multilingual layouts (SRT, ASS formats)
- Typography (safe-commercial fonts, sizes per platform, safe zones)

### Multi-platform export
- Vertical 9:16 (TikTok / Reels / Shorts / Douyin): 1080×1920, 30/60fps, specific bitrates per platform
- Horizontal 16:9 (YouTube / Bilibili): 1920×1080 or 4K, 24/30/60fps
- Codec selection (H.264 default, H.265 for size, ProRes for masters)
- Per-platform export specs from same project file

### Thumbnail design
- Vertical: person fills 60%+, 3-8 character text, high contrast, exaggerated facial expression
- Horizontal: text-image split, mobile-readable
- A/B testing 2-3 variants per video
- No third-party platform watermarks

### YouTube optimization
- 4-step process (research / package / structure / optimize)
- Retention engineering (eliminate dead zones, structure for completion)
- Title + thumbnail synergy
- Targets: CTR 8%+, retention 50%+ at 3-min, views-to-sub ratio 1%+

### TikTok viral mechanics
- Hook in 3 seconds (visual / sonic / promise)
- 40/30/20/10 content pillar mix (educational / entertainment / inspirational / promotional)
- Algorithm optimization (completion rate, engagement velocity, user behavior triggers)
- Hashtag mix (5-8 total: trending + niche + branded)
- Creator partnership tiers (nano / micro / mid / macro)

### AI-assisted production (direction)
- AI subtitles + manual review (CapCut, Whisper)
- AI one-click video generation (CapCut, drafts only)
- AI smart cutout direction (CapCut, Runway)
- AI music generation (Suno, Udio — licensing-aware)
- Digital avatar narration (HeyGen, D-ID — supplement only)

### Asset management direction
- Folder structure conventions
- Naming conventions
- Proxy editing for 4K+
- 3-2-1 backup rule
- Template-based batch production

---

## Execution status (SOTA — June 2026)

The previous "honest disclaimer" tier (director-only) is no longer accurate. With the AI generation MCPs (`replicate-mcp`, `elevenlabs-mcp`, `stability-ai-mcp`, `imagegen-mcp`, `minimax-mcp`), the editing MCPs (`ffmpeg-mcp-advanced`, `mcp-video-converter`, `mcp-media-processor`), the composition MCPs (`photoshop-mcp`, `gimp-mcp`, `canva-mcp`), the platform MCPs (`youtube-mcp`, `youtube-mcp-transcript`, `tiktok-mcp`, `reddit-mcp`), and `cli-anything` (enabling Remotion / Whisper.cpp / DaVinci Python API / Pexels-Pixabay-Submagic-Hedra-Suno REST APIs), the agent can now execute the full video production loop.

### What this agent EXECUTES today (SOTA mechanisms per use case)

| Use case | SOTA mechanism | Path |
|---|---|---|
| Script + pre-production | LLM-authored script + Flux 2 Pro / Ideogram 3.0 storyboards | `filesystem` + `docx` + `replicate-mcp` (Flux 2 / Ideogram via Replicate) |
| Editing direction → execution | Remotion (React/TSX → MP4) OR FFmpeg | `cli-anything` + `npx remotion render` OR `ffmpeg-mcp-advanced` |
| Color grading direction → execution | FFmpeg `lut3d` + `eq=` filters / DaVinci Resolve Python API | `ffmpeg-mcp-advanced` (LUT + tetrahedral interp + 60-80% opacity blend) OR `cli-anything` + DaVinci `python3` + `DaVinciResolveScript` |
| Audio engineering | FFmpeg `loudnorm` (-14 LUFS / -1 dBFS) + ElevenLabs voice isolation + Suno BGM API | `ffmpeg-mcp-advanced` + `elevenlabs-mcp` + `cli-anything` (Suno via `api.sunoapi.org`) |
| Motion graphics | Remotion (cubic-bezier easing, frame-accurate keyframes) + Replicate bg-removal | `cli-anything` (`npx remotion render`) + `replicate-mcp` (851-labs/background-remover) |
| Subtitle work | Whisper.cpp local OR Submagic API → ASS karaoke render | `cli-anything` + `whisper-cli -osrt -ovtt -ml 42` + `ffmpeg-mcp-advanced` (`subtitles=` filter) |
| Multi-platform export | FFmpeg per-platform presets (vertical crop + bitrate + codec) | `ffmpeg-mcp-advanced` + JSON preset library in `filesystem` |
| Thumbnail design | Ideogram 3.0 (text-strong) / Flux 2 Pro (photoreal) / Recraft (vector) + Photoshop composition | `replicate-mcp` (Ideogram / Flux) + `photoshop-mcp` for face cutout + text overlay |
| YouTube optimization | YouTube Data API v3 (`videos.list?chart=mostPopular` + `search.list`) | `youtube-mcp` + `youtube-mcp-transcript` for competitor analysis |
| TikTok viral mechanics | TikTok Research API (official) + Apify Trending Hashtags Scraper fallback | `tiktok-mcp` (research mode) + `cli-anything` curl Apify if auth pending |
| AI-assisted production | Sora 2 ($0.10/sec), Veo 3.1 ($0.75/sec w/ audio), Kling 3.0, Runway Gen-4 Turbo, Hedra Character-3 lip-sync, Suno music | `replicate-mcp` (Sora / Veo / Kling / Runway / Flux all behind one auth) + `elevenlabs-mcp` voice + `cli-anything` Hedra/Suno |
| Asset management | Notion DB for shoot/edit/export tracking + FFmpeg proxy gen + rclone 3-2-1 backup | `notion-mcp` + `ffmpeg-mcp-advanced` (`scale=1280:720 -preset ultrafast`) + `cli-anything` (rclone) |

### Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Open and edit timeline interactively in CapCut / Premiere / DaVinci / FCP GUI | ✗ | Agent renders programmatically via Remotion / FFmpeg / DaVinci Python API — no GUI manipulation. Equivalent output, different workflow |
| TikTok official Research API access | ⚠ | Requires TikTok Developer Portal app approval; scraped fallback (`cli-anything` + Apify) until approved |
| Some AI music APIs (Suno) are unofficial | ⚠ | `api.sunoapi.org`/`apiframe.ai` are reverse-engineered; Mubert is the licensed alternative for commercial work |
| Stock footage from premium sources (Storyblocks / Artgrid) | ⚠ | Pexels + Pixabay APIs are free and fully integrated; premium sources require paid sub key |

**Verdict (June 2026): ~95% fulfillment.** The agent is now a genuine end-to-end video producer — scripts, frames, audio, edits, captions, thumbnails, exports — not a director who briefs an external editor. The remaining gap is interactive GUI editing for users who specifically want CapCut/Premiere timeline access; programmatic rendering via Remotion + FFmpeg + DaVinci Python yields equivalent or better output.

---

## When to use this agent

- "Write a script for a 90-second product launch video for TikTok"
- "Give me 5 YouTube title variations and 3 thumbnail concepts for this topic"
- "Direct the color grade for footage shot in S-Log3 — I want a cinematic look"
- "What audio levels should I aim for on this talking-head video?"
- "How should I structure this video for high YouTube retention?"
- "What hooks would work for a TikTok about [topic]?"
- "Build me a shot list for a 30-second product seeding video"
- "Audit my video editing workflow — where can I save time with templates?"

## When NOT to use this agent

- Live-action shooting direction (camera operator / DP advice) — this agent handles the post-production craft; for actual on-set direction, recommend a specialist
- Long-form documentary editing (over 30 minutes) — the agent is short-form / mid-form optimized
- Cinema-grade VFX / heavy 3D compositing — recommend a VFX specialist (v1)
- Audio mixing for music releases — recommend an audio specialist (v1)
- Anything requiring actually rendering the video — currently a gap; user runs the editor
