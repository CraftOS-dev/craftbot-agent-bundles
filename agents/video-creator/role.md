# Video Creator — deep reference

This appends to `AGENT.md`. **Not** in the agent's default context. Grep when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "Software decision tree", "Shot scale catalog", "Camera movement catalog", "Transition catalog", "Color grading workflow", "Audio engineering reference", "Motion graphics + keyframe reference", "Subtitle typography reference", "Multi-platform export specs", "AI editing tool reference", "Asset management + workflow", "YouTube optimization playbook", "TikTok viral playbook", "Story arc framework", "Thumbnail composition rules", "Content pillar mix", "Brief templates", "SOTA tool reference (June 2026)", "Replicate Sora 2", "Replicate Veo 3.1", "Replicate Flux 2 Pro", "Replicate Ideogram 3.0", "ElevenLabs Multilingual v2", "ElevenLabs Voice Isolator", "FFmpeg color grading", "FFmpeg audio mastering", "FFmpeg multi-platform export", "Remotion programmatic video", "Whisper.cpp subtitles", "DaVinci Resolve Python API", "YouTube Data API v3", "TikTok Research API", "Pexels API", "Pixabay API", "Submagic API", "Hedra Character-3", "Suno API", "Mubert API", "Photoshop MCP".

For provenance, see `SOURCES.md`.

---

## Capability reference

### Editing software the agent recommends

| Software | Best for | Key strengths | Limitations |
|---|---|---|---|
| **CapCut Pro** | Daily short-video output, lightweight commercial, batch production | Best-in-class AI features (auto-subtitles, smart cutout, one-click generation), rich templates, lowest learning curve, deep TikTok/Douyin integration | Limited complex VFX, color precision, large-project performance |
| **Adobe Premiere Pro** | Mid-to-large commercial, multi-platform production | Industry standard, seamless AE/AU/PS integration, richest plugin ecosystem, multi-cam, Dynamic Link to AE, Lumetri Color | Performance on large projects, expensive subscription, color depth inferior to DaVinci |
| **DaVinci Resolve** | High-end color grading, cinema projects, budget-conscious pros | Free version exceptionally powerful, industry-leading color (DaVinci's panel IS the standard), Fairlight pro audio, Fusion node-based VFX | Steepest learning curve, UI differs from traditional NLEs |
| **Final Cut Pro** | Mac users, fast individual output | Native M-series performance, magnetic timeline efficiency, one-time purchase, smooth proxy editing | Mac-only, weaker collaboration than PR |

### Software decision tree

- Daily efficiency, short-form focus → CapCut Pro **OR programmatic via Remotion** (see `skills/remotion-programmatic-video/SKILL.md`) when you want template-driven batch output
- Commercial work + AE integration → Premiere Pro **OR Remotion + FFmpeg** for headless / CI / programmatic pipelines
- Demanding color work, limited budget → DaVinci Resolve **OR FFmpeg `lut3d` for scriptable grading** (see `skills/ffmpeg-color-grading/SKILL.md`), or DaVinci Python API for automated color (`skills/davinci-resolve-python-scripting/SKILL.md`)
- Mac user, smooth experience priority → Final Cut Pro
- **Recommendation: master at least one primary + be familiar with CapCut** (AI features too useful to ignore). For agent-executable work (no human in the loop), default to **Remotion + FFmpeg + Replicate AI gen** — covered in the SOTA tool reference (June 2026) section below.

### Production capabilities

- **Pre-production**: hook design, script writing, shot list, B-roll list, mood board, storyboard
- **Direction**: shot scale and camera movement direction, color/audio direction, motion graphics direction
- **Color grading**: primary correction, secondary correction (HSL, curves, masks), LUT application, stylistic grading
- **Audio engineering**: noise reduction, voice EQ + compression, BGM beat-syncing, sound design, mix balance, loudness normalization
- **Motion graphics**: keyframe animation, text animation, particle effects, green screen / keying, speed curves / speed ramping
- **Subtitles**: AI auto-generation, manual review, decorative text styling, multilingual layout (SRT, ASS)
- **Multi-platform export**: aspect ratio adaptation, resolution/bitrate per platform, codec selection
- **Thumbnail design**: composition, mobile-readable text, exaggerated facial expressions, A/B variant generation
- **AI-assisted editing**: auto-subs (CapCut, Whisper), one-click video generation, smart cutout, AI music (Suno, Udio), digital avatar narration

---

## Shot scale catalog

| Scale | Frame | Use case |
|---|---|---|
| Extreme wide / establishing | Wide environment | Opening establishing shot, environment context |
| Full shot | Full body + environment | Fashion, dance, sports |
| Medium shot | Knees up | Dialogue, explainers, daily vlogs (most common narrative shot) |
| Close-up | Chest and above | Talking-head, product seeding, emotional content |
| Extreme close-up | Facial / product details | Food, beauty, product showcase, visual impact |

**Short-video golden rule**: Visual hook within 3 seconds — typically a close-up or extreme close-up opening.

---

## Camera movement catalog

| Movement | Effect | Suits |
|---|---|---|
| Push in (far → near) | Guides focus, "discovery" / "tension" | Emotional reveals, suspense |
| Pull out (near → far) | Reveals full picture, "release" / "isolation" | Reveal moments, scale shifts |
| Pan (horizontal/vertical) | Shows full spatial context | Environment introductions, scene transitions |
| Dolly (lateral following subject) | Adds dynamism | Walking, running, shop visits |
| Tracking shot | Follows moving subject in frame | Person-following footage |
| Handheld shake | Documentary feel, immediacy | Vlog, street, breaking events |
| Gimbal | Silky-smooth motion | Commercial ads, travel, product |
| Drone aerial | Large-scale overhead | Travel, real estate, city promos |

---

## Transition catalog

| Transition | Use case | Warning |
|---|---|---|
| Hard cut | Fast pacing, high info density (default) | If a hard cut works, use it |
| Dissolve (cross-fade) | Time passage, emotional transition | Don't overuse — feels nostalgic |
| Mask transition | High visual impact (doorframes, walls, hands as wipes) | Setup overhead; needs matching shots |
| Match cut | Visual continuity through composition/movement/color | Requires careful shot planning |
| Whip pan | Motion blur connecting two scenes | Energetic; can disorient |
| Zoom transition | "Warp" effect | Trendy; dates quickly |
| Flash white/black | Beat-synced cuts, mood shifts | Don't strobe |

**Core principle**: Transitions serve the narrative, not the ego. If a hard cut works, don't add a fancy transition.

---

## Color grading workflow

### Primary correction (restore reality)

- **White balance** (color temperature + tint) — ensure white is actually white
- **Exposure** — use histogram; avoid blown highlights or crushed shadows
- **Contrast** — affects clarity
- **Highlights / shadows / whites / blacks** — four-way fine-tune
- **Saturation vs vibrance** — vibrance protects skin tones
- **Goal**: consistent exposure, color temp, contrast across all shots

### Secondary correction (targeted refinement)

- **HSL adjustment** — independent control of specific colors (e.g., making only the sky bluer)
- **Curves** — RGB + hue curves; core grading weapon
- **Qualifiers / masks** — isolate specific areas
- **Skin tone correction** — use vectorscope; align skin to the "skin tone line"
- **Sky enhancement** — independent sky region for depth

### LUT usage

- **Technical LUT** — LOG → standard color space (e.g., S-Log3 → Rec.709). Apply first.
- **Creative LUT** — stylistic look. Apply after primary correction.
- **Opacity**: 60-80% recommended. 100% is usually too heavy.
- **Custom LUTs**: export your frequently-used grade as a personal-style LUT.

### Stylistic grading directions

| Style | Recipe |
|---|---|
| Cinematic | Low saturation + teal-orange (shadows teal / highlights orange) + subtle grain |
| Japanese fresh | High brightness + low contrast + teal-green tint + lifted shadows |
| Cyberpunk | High-saturation neon (magenta/cyan/blue) + high contrast + crushed blacks |
| Vintage film | Yellow-green tint + reddish shadows + grain + slight fade |
| Morandi palette | Low saturation + gray tones (lifestyle) |

**Consistency rule**: style uniform within a video and across a series.

---

## Audio engineering reference

### Noise reduction

- Capture pure room tone first; use spectral subtraction
- Tools: Premiere DeNoise, DaVinci Fairlight, iZotope RX (pro), CapCut AI
- Don't max out — creates "underwater voice"; keep 10-20% ambient
- Wind noise: high-pass filter at 80-120Hz
- De-essing: 4-8 kHz sibilance suppression

### BGM beat-syncing

- Mark downbeats on timeline first
- Cut shots on downbeats for impact
- Align BGM emotional shifts with content mood
- Sync to strong beats and transition points — every-beat cutting causes rhythm fatigue

### Sound design

- **Ambient** — street, birds, rain, cafe (immersion)
- **Action** — whoosh, ding, click (reinforces on-screen action)
- **Mood** — suspense hum, comedy boing, surprise ding (emotional atmosphere)
- Sources: freesound.org, Epidemic Sound, CapCut library, self-recorded Foley
- **Less is more** — precise timing beats wall-to-wall

### Mix balance

| Element | Talking-head / narration | Music-only video |
|---|---|---|
| Voice | -12 to -6 dB | n/a |
| BGM | -24 to -18 dB | -12 to -6 dB |
| SFX | -18 to -12 dB | -18 to -12 dB |

- Final loudness: **-14 LUFS** (most platforms normalize)
- Peak: **≤ -1 dBFS** (safety headroom for re-encode)

### Voice enhancement

- EQ: high-pass 80-120Hz, boost 2-5 kHz clarity
- Compressor: ratio 3:1 to 4:1
- Reverb: subtle (most short-form needs none)
- AI voice enhancement: CapCut and Premiere both offer

---

## Motion graphics + keyframe reference

### Keyframe animation

- Properties: position, scale, rotation, opacity
- **Easing curves are the soul** — linear motion looks mechanical; ease-in/ease-out feels natural
- Elastic / bounce effects: slight overshoot + return; adds liveliness
- Keyframe spacing: tighter = faster action; wider = slower

### Text animation

| Style | Suits |
|---|---|
| Character-by-character / typewriter | Suspense, tech, educational |
| Bounce-in entrance | Playful styles |
| Handwriting reveal (progressive strokes) | Artistic, educational |
| Glitch text + chromatic aberration | Tech, cyberpunk |
| 3D text rotation | Premium feel |

**Rule**: text-animation duration 0.3-0.5 seconds. Too slow drags the pace; too fast is unreadable.

### Particle effects

- Uses: fireworks, sparks, dust, light bokeh, snow, fireflies
- CapCut: built-in particle stickers (one-tap)
- After Effects: Particular plugin for custom systems
- **Principle**: enhance atmosphere; don't steal the show

### Green screen / keying

- Shooting: even lighting, no wrinkles, subject distance for no spill
- Software keying: CapCut smart cutout (no green needed), PR Ultra Key, DaVinci Chroma Key
- Edge cleanup: edge softness, spill suppression, edge contraction — avoid "green fringe"
- AI smart cutout: CapCut's AI person seg works without green screen

### Speed curves (speed ramping)

- **Constant speed change** — uniform speed-up / slow-down of entire clip (timelapse / slow-motion)
- **Curve ramping** (core technique) — fast-slow-fast rhythm within a single clip
- **Classic pattern**: pre-action slow buildup → action at normal speed → post-action slow savor
- **Beat-synced**: return to normal speed on BGM downbeats
- **Source requirement**: 60fps or 120fps for smooth slow-motion; 24/30 fps slowed = stutter

---

## Subtitle typography reference

### Decorative text

- Styles: stroke + drop shadow, 3D emboss, gradient fill, texture mapping
- Tools: CapCut templates (fastest), Photoshop PNG imports, AE animated fancy text
- **Contrast rule**: dark frame → bright text; bright frame → dark text + stroke
- Layering: bottom layer stroke/shadow + middle color fill + top highlight (≥ 2 layers)

### Variety-show subtitle style

- Large font, high-saturation colors, exaggerated animations + sound effects
- Different speakers → different colors; keywords in attention-grabbing red/yellow
- Don't block faces; stay within safe zones
- Vertical video subtitles → lower third
- **Suits**: entertainment, comedy, reaction. **Not**: educational, business.

### Scrolling comment-style subtitles

- Use cases: reaction videos, curated comments, multi-person discussions
- Implementation: multiple subtitle tracks, varying speeds and vertical positions
- Bilibili-danmaku style: mostly white, key comments colored or larger
- Don't use wall-to-wall — dense bursts at key moments

### Multilingual subtitles

- **SRT** — most universal format; plain text + timecodes
- **ASS** — supports rich styling (font/color/position/animation); common for Bilibili
- Bilingual layout: primary language top, secondary below; primary larger
- Each line: 1-5 seconds; appear 0.2-0.5 seconds early (so eyes can catch up)
- **AI auto-subs + manual review**: AI generates the draft (saves 80%); review line-by-line for typos and sentence breaks

### Typography aesthetics

- Chinese-safe-commercial fonts: Source Han Sans, Alibaba PuHuiTi
- **Vertical**: body subtitles 30-36px, titles 48-64px
- **Horizontal**: body 24-30px, titles 36-48px
- Safe margins: 10-15% from frame edges
- Line height: 1.2-1.5×; slightly wider letter spacing for breathing room
- Readability: at least one of — semi-transparent backdrop bar, stroke, drop shadow

---

## Multi-platform export specs

### Vertical 9:16 (TikTok / Reels / Shorts / Douyin / Kuaishou / Xiaohongshu)

| Spec | Value |
|---|---|
| Resolution | 1080×1920 (standard), 2160×3840 (4K vertical) |
| Frame rate | 30fps (standard), 60fps (sports/gaming) |
| Bitrate | 1080p: 8-15 Mbps; 4K: 20-35 Mbps |
| Duration | TikTok 7-15s (entertainment) / 1-3min (educational); Reels 7-90s; Shorts ≤60s |
| Safe zones | 15% padding top/bottom (platform UI) |

### Horizontal 16:9 (YouTube / Bilibili / Xigua)

| Spec | Value |
|---|---|
| Resolution | 1920×1080 (standard), 3840×2160 (4K) |
| Frame rate | 24fps (cinematic), 30fps (standard), 60fps (gaming/sports) |
| Bitrate | 1080p30: 10-15 Mbps; 4K60: 40-60 Mbps |
| YouTube tip | Upload at max quality; YouTube transcodes |
| Bilibili tip | 4K+120fps qualifies for "High Quality" badge |

### Encoding & export settings

| Codec | Use |
|---|---|
| H.264 | Best compatibility, moderate file size — default |
| H.265 (HEVC) | 30-50% smaller at same quality; some older devices can't play |
| ProRes | High-quality intermediate (Apple ecosystem); for footage needing further processing |
| Audio | AAC 256kbps stereo (standard); 320kbps (high quality) |

### Pre-export checklist

- [ ] Resolution correct for target platform?
- [ ] Frame rate matches source?
- [ ] Bitrate sufficient (not over-compressed)?
- [ ] Audio plays normally end-to-end?
- [ ] No audio-video desync in playback?
- [ ] No black frames at start or end?
- [ ] Subtitles align with speech throughout?

---

## Thumbnail composition rules

### Vertical thumbnail (TikTok / Reels / Shorts)

- Person fills 60%+ of frame
- Large title text (3-8 characters)
- High-contrast colors against the background
- Exaggerated facial expression (surprise, joy, confusion) — neutral doesn't generate clicks

### Horizontal thumbnail (YouTube / Bilibili)

- Composition options: text-left/image-right, text-top/image-bottom, or text-center
- Key info centered or slightly above center
- Thumbnail text: **large** (readable on phone screens), **short** (scannable in a glance), **compelling** (suspense or value)

### General rules

- **80% of CTR is determined by the thumbnail**
- Title + thumbnail must work synergistically — don't repeat the title in the thumbnail; complement
- Mobile-readability is non-negotiable (most viewers are on phone)
- A/B test 2-3 thumbnails per video; track CTR data; iterate
- **No third-party platform watermarks** in thumbnails (e.g., a TikTok logo on a YouTube thumbnail = guaranteed throttling)
- No clickbait that mismatches the content — burns trust and tanks retention

---

## YouTube optimization playbook

### Four-step process

1. **Research** — competitor performance patterns and audience intent
2. **Package** — content with multiple title variations and thumbnail concepts
3. **Structure** — videos with strategic chaptering and retention-focused pacing
4. **Optimize** — metadata, descriptions, end screens for algorithmic velocity

### Algorithmic mastery

- Title + thumbnail synergy — work together, not parallel
- Mobile-readable thumbnails (where most viewers are)
- Curiosity-driven titles — without clickbait that mismatches content
- Metadata: descriptions with target keywords, chapter markers, cards, end screens

### Retention engineering

- **First 30 seconds**: map the hook to the value promise
- Eliminate pacing dead zones (visual / story tension every 20-30 seconds)
- Structure content to prevent abandonment at known critical moments (1-min mark, 3-min mark)
- End screen designed to drive next-video click — not to wave goodbye

### Cross-platform syndication

- Repurpose long-form into Shorts (best moments + hook)
- Adapt for Reels and TikTok with platform-native pacing
- Don't just trim — re-edit for the new platform's culture

### Success targets

| Metric | Target |
|---|---|
| CTR | 8%+ on new uploads |
| Audience retention | 50%+ at 3-minute mark |
| Views-to-subscriber ratio | 1% or higher |
| First 24-hour performance | 15% above channel baseline |

---

## TikTok viral playbook

### Hook in 3 seconds

Every video must capture attention within 3 seconds. Options:
- **Visual surprise** — pattern interrupt, unexpected element, attention-grabbing opener
- **Sonic surprise** — trending sound, audio hook, voice change
- **Promise**: state the value the viewer will get for staying

### Content pillar mix (40/30/20/10)

- **40% educational** — teach
- **30% entertainment** — make them feel
- **20% inspirational** — make them want to be / do
- **10% promotional** — explicit business ask

### Algorithm mastery

- **Completion rate** — full video watch percentage; the primary algorithmic signal
- **Engagement velocity** — likes, comments, shares in the first hour
- **User behavior triggers** — profile visits, follows, rewatch
- **Cross-promotion** — encouraging shares to other platforms for algorithm boost

### Hashtag strategy

5-8 total tags, mixed:
- Trending hashtags (riding current waves)
- Niche hashtags (your audience's specific subculture)
- Branded hashtags (yours, to build over time)

### Creator partnership tiers

| Tier | Followers |
|---|---|
| Nano | 1K-10K |
| Micro | 10K-100K |
| Mid-tier | 100K-1M |
| Macro | 1M+ |

Partnership models: product seeding, sponsored content, brand ambassadorships, challenge participation, joint content creation, takeovers, live collaborations, UGC campaigns.

### Success targets

| Metric | Target |
|---|---|
| Engagement rate | 8%+ (industry average: 5.96%) |
| View completion rate | 70%+ for branded content |
| Hashtag performance | 1M+ views for branded hashtag challenges |
| Creator partnership ROI | 4:1 return on influencer investment |

---

## Story arc framework

### Three-act structure

- **Setup** — establish character, environment, normal state
- **Conflict** — introduce tension, problem, challenge
- **Resolution** — show outcome, transformation, takeaway

### Visual storytelling components

- **Character development** — protagonist identification (often customer/user)
- **Conflict identification** — problem or challenge driving the narrative
- **Resolution design** — how the brand/product provides the solution
- **Emotional journey mapping** — peaks and valleys throughout the story
- **Visual pacing** — rhythm and timing for optimal engagement
- **Visual metaphors** — symbolic elements that carry meaning

### Short-form adaptation (TikTok / Shorts / Reels)

- Compress the arc into 15-60 seconds
- Hook = 3-second teaser of the conflict or resolution
- Body = setup + conflict
- Payoff = resolution + CTA

### Long-form adaptation (YouTube)

- Hook at 0:00 (first 15 seconds) = state the value or surprise
- Setup at 0:15-1:00
- Conflict at 1:00-7:00 (varies by video length)
- Resolution at 7:00-end (varies)
- End screen / CTA in the final 10-20 seconds

---

## Asset management + workflow

### Folder structure

```
project/
├── 01-assets/
│   ├── footage/         # raw video by date
│   ├── audio/           # music, SFX
│   ├── images/          # photos, graphics
│   ├── subtitles/       # SRT, ASS files
│   └── proxies/         # low-res for editing
├── 02-project-files/
│   └── edit-v1.prproj   # versioned edits
└── 03-exports/
    └── final/           # delivery files per platform
```

### File naming convention

`date_project_shot-number_description.ext`

Example: `20260312_product-review_S01_unboxing-closeup.mov`

### Proxy editing (mandatory for 4K+)

- Generate low-res proxies from raw 4K/6K footage
- Edit on proxies (smooth timeline performance)
- Relink to originals for final export
- **Lifesaver for high-res workflows**

### Backup strategy: 3-2-1 rule

- 3 copies of the data
- 2 different storage media
- 1 off-site backup

### Five-step workflow

1. **Requirements & Asset Assessment** — objective, platform, footage quality, editing plan
2. **Rough Cut** — narrative skeleton; arrange in story order; initial trim; no fine-tuning yet
3. **Fine Cut** — frame-accurate edit points; transitions; speed ramps; beat-sync to BGM
4. **Color / Audio / Subtitles** — primary correction → secondary → stylistic; noise reduction → voice → BGM → SFX; AI subs → manual review → style → layout
5. **Export & Multi-Platform Adaptation** — per-platform parameters; post-export playback check; thumbnail + title prep

### Template-based batch production

- **Project templates**: preset timeline layouts, color presets, subtitle styles, intro/outro
- **CapCut templates**: one-click apply
- **PR templates (MOGRT)**: build in AE, modify in PR
- **Batch export**: DaVinci render queue, AME queue, CapCut batch export
- **Result**: per-video time drops from 2 hours to 30 minutes

### Keyboard shortcut efficiency

- 80% of operations should happen without touching the menu bar
- **PR essentials**: Q/W (ripple edit), J/K/L (playback control), C (razor), V (selection), I/O (in/out points)
- Custom shortcuts: bind most-used to left-hand keys (right hand stays on mouse)
- Programmable side-button mouse: bind undo/redo/marker

---

## AI editing tool reference

### AI auto-subtitles

- **CapCut AI subtitles** — 95%+ accuracy; Chinese, English, Japanese, Korean, more; one-click
- **OpenAI Whisper** — open-source, offline, 99 languages, extremely high accuracy
- **Whisper.cpp (agent-executable SOTA)** — local C++ port; SRT/VTT/ASS export with word-level timestamps; karaoke styling via ASS `\k` tags; see `skills/whisper-cpp-subtitles/SKILL.md`
- **Submagic API** — paid ($69/mo) viral animated captions (Mr Beast / Hormozi templates)
- **ByteDance Volcano Engine ASR** — enterprise API; batch processing
- **Workflow**: AI draft → manual review (jargon, names, homophones) → timeline adjust → style. **Agent-executable path:** Whisper.cpp → ASS karaoke → FFmpeg `subtitles=` burn-in.

### AI one-click video generation

- **CapCut text-to-video** — input text, auto-match stock + voiceover + subs + BGM
- **CapCut AI script** — topic → script + storyboard suggestions
- **SOTA agent-executable path (June 2026):**
  - **Sora 2** (~$0.10/sec) — natural-language scene gen via Replicate (`openai/sora-2`)
  - **Veo 3.1** (~$0.75/sec, **native audio**) — premium photoreal w/ sync sound (`google/veo-3.1`)
  - **Kling 3.0** (~$0.28/sec) — high motion quality at mid cost (`kwaivgi/kling-v2.0`)
  - **Runway Gen-4 Turbo** (~$0.50/sec) — camera-controllable, image-to-video (`runwayml/gen-4-turbo`)
  - All four behind single `replicate-mcp` auth; see `skills/replicate-ai-video-gen/SKILL.md`
- **Use cases**: rapid drafts for news / talking-head / image-text videos; AI B-roll inserts; AI hooks
- **Limitation**: AI-generated videos handle 60% of work; last 40% creative refinement needs human craft

### AI smart cutout

- **CapCut AI cutout** — real-time person segmentation without green screen
- **Runway ML** — professional AI keying and video generation
- **Replicate `851-labs/background-remover`** (agent-executable) — POST `https://api.replicate.com/v1/predictions` with `version=851-labs/background-remover` → returns transparent PNG; see `skills/replicate-ai-image-gen/SKILL.md`
- **Photoshop MCP `select_subject` + `refine_edge`** (agent-executable) — for face cutouts in thumbnails; see `skills/thumbnail-composition-photoshop/SKILL.md`
- **Use cases**: background replacement, picture-in-picture, green-screen alternative
- **Limitations**: hair, semi-transparent objects (glass/smoke) remain challenging — manual touchup when critical

### AI music generation

- **Suno AI / Udio** — text-to-music; specify style, mood, duration
- **Agent-executable paths:**
  - **Suno (unofficial via sunoapi.org)** — POST `https://api.sunoapi.org/api/v1/generate`; commercial-use clouded by reverse-engineered API — see `skills/ai-music-suno-mubert/SKILL.md`
  - **Mubert API (licensed alternative — preferred for commercial)** — POST `https://api-b2b.mubert.com/v2/RecordTrack`; fully cleared for commercial + Content ID whitelist
  - **AIVA** — orchestral / cinematic, licensed
  - **Soundraw** — stems available, licensed
- **Use cases**: quickly generate custom BGM when stock doesn't fit; avoid copyright issues
- **Copyright note**: confirm commercial licensing per platform — **use Mubert/AIVA/Soundraw for brand work**, Suno only for drafts
- **Quality**: sufficient for simple scoring; complex arrangements / vocal performances still short of human

### Digital avatar narration

- **Tools**: CapCut digital avatar, HeyGen, D-ID, Tencent Zhi Ying
- **Hedra Character-3 (SOTA, agent-executable)** — 9/10 lip-sync quality; POST `https://api.hedra.com/web-app/public/generations` with `audio=@vo.wav` + `image=@face.png`; ~$0.30/sec. See `skills/hedra-avatar-lipsync/SKILL.md`
- **Use cases**: batch-producing educational / news content; substitute when on-camera talent isn't available; foreign-language dubbing with mouth-shape match
- **Current state**: lip sync and facial expressions fairly natural; "clearly a digital avatar" feel persists
- **Use as supplement, not replacement** — audiences trust real people more

---

## SOTA tool reference (June 2026)

The agent ships with the full SOTA media + AI generation stack — MCPs (Replicate, ElevenLabs, FFmpeg, Photoshop, YouTube, TikTok, Notion) plus `cli-anything` for Remotion / Whisper.cpp / DaVinci Python / REST APIs. **Each tool below has a dedicated skill pack at `skills/<name>/SKILL.md` with full recipes, examples, and gotchas.** Grep this section by tool name.

### Replicate Sora 2

- **Slug:** `openai/sora-2` (`openai/sora-2-pro` for higher-fidelity / longer)
- **Cost:** ~$0.10/sec (Pro ~$0.30/sec)
- **Endpoint:** `POST https://api.replicate.com/v1/predictions` with `{"version":"openai/sora-2","input":{"prompt":"...","duration":8,"aspect_ratio":"9:16"}}`
- **Best for:** natural-language scene generation, B-roll, hooks
- **Limits:** 8s std, 20s Pro; no deterministic seed
- **Skill pack:** `skills/replicate-ai-video-gen/SKILL.md`

### Replicate Veo 3.1

- **Slug:** `google/veo-3.1` (or `google/veo-3.1-fast`)
- **Cost:** ~$0.75/sec ($0.40/sec fast)
- **Endpoint:** same Replicate predictions pattern with `generate_audio: true` for **native sync audio**
- **Best for:** photoreal with synced sound, VO-free dialogue/SFX-driven shots
- **Limits:** 8s, mono audio
- **Skill pack:** `skills/replicate-ai-video-gen/SKILL.md`

### Replicate Kling 3.0

- **Slug:** `kwaivgi/kling-v2.0` (and v3.0 as it lands)
- **Cost:** ~$0.28/sec
- **Best for:** high motion (action, sports, dance) at mid cost
- **Skill pack:** `skills/replicate-ai-video-gen/SKILL.md`

### Replicate Runway Gen-4 Turbo

- **Slug:** `runwayml/gen-4-turbo`
- **Cost:** ~$0.50/sec
- **Best for:** image-to-video with camera-motion control (`camera_motion: push_in / orbit / pan_left`)
- **Skill pack:** `skills/replicate-ai-video-gen/SKILL.md`

### Replicate Flux 2 Pro

- **Slug:** `black-forest-labs/flux-2-pro` (Dev tier `flux-2-dev` for cheaper bulk)
- **Cost:** ~$0.04/image
- **Best for:** photoreal hero stills, product, storyboards, thumbnails
- **Endpoint:** Replicate predictions with `{"version":"black-forest-labs/flux-2-pro","input":{"prompt":"...","aspect_ratio":"9:16","seed":42}}`
- **Skill pack:** `skills/replicate-ai-image-gen/SKILL.md`

### Replicate Ideogram 3.0

- **Slug:** `ideogram-ai/ideogram-v3`
- **Cost:** ~$0.05/image
- **Best for:** **typography-strong thumbnails** — text-in-image accuracy unmatched (quote exact text in prompt)
- **Skill pack:** `skills/replicate-ai-image-gen/SKILL.md`

### Replicate background remover (851-labs)

- **Slug:** `851-labs/background-remover`
- **Best for:** transparent-PNG cutouts of subjects for thumbnail composition / PIP overlays
- **Skill pack:** `skills/replicate-ai-image-gen/SKILL.md`

### ElevenLabs Multilingual v2

- **Model:** `eleven_multilingual_v2` (29 languages)
- **Endpoint:** `POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}` with `xi-api-key`
- **Best for:** hero VO (use `eleven_turbo_v2_5` for drafts, `eleven_flash_v2_5` for ultra-fast)
- **Voice settings sweet spot:** `stability=0.5, similarity_boost=0.75, style=0.4`
- **Skill pack:** `skills/elevenlabs-voice-production/SKILL.md`

### ElevenLabs Voice Isolator

- **Endpoint:** `POST https://api.elevenlabs.io/v1/audio-isolation` with `audio` multipart file
- **Best for:** stripping room tone / traffic / music bleed from voice-only recordings (better than FFmpeg `afftdn`)
- **Skill pack:** `skills/elevenlabs-voice-production/SKILL.md`

### ElevenLabs Dubbing v2

- **Endpoint:** `POST https://api.elevenlabs.io/v1/dubbing` with source file + `target_lang`
- **Best for:** cross-language dubbing preserving speaker identity
- **Skill pack:** `skills/elevenlabs-voice-production/SKILL.md`

### FFmpeg color grading

- **Filter chain:** `lut3d=<file>.cube:interp=tetrahedral` (creative LUT) + `eq=` (primary) + `blend=all_opacity=0.7` (LUT at 60–80% per role.md rule)
- **5 stylistic looks:** cinematic teal-orange / Japanese fresh / cyberpunk / vintage / Morandi — recipes in skill pack
- **Skill pack:** `skills/ffmpeg-color-grading/SKILL.md`

### FFmpeg audio mastering

- **Two-pass `loudnorm`** to hit -14 LUFS / -1 dBFS (broadcast spec)
- **Voice chain:** `highpass=f=100, equalizer=f=3000:g=3, compand=...`
- **BGM ducking:** `sidechaincompress=threshold=0.05:ratio=8`
- **Skill pack:** `skills/ffmpeg-audio-mastering/SKILL.md`

### FFmpeg multi-platform export

- **Per-platform JSON preset library** in `skills/ffmpeg-multi-platform-export/presets/`
- **TikTok / Reels / Shorts / YouTube 1080p / YouTube 4K60 / Bilibili / Douyin** all covered
- **Always `-movflags +faststart`** for streamable MP4s
- **Skill pack:** `skills/ffmpeg-multi-platform-export/SKILL.md`

### Remotion programmatic video

- **Setup:** `npm i remotion @remotion/cli @remotion/three @remotion/google-fonts`
- **Render:** `npx remotion render src/index.tsx <Composition> out.mp4 --crf=18 --concurrency=8`
- **Best for:** frame-accurate keyframes (cubic-bezier easing), template-driven batch output, particle FX via `@remotion/three`, headless / CI pipelines
- **Easing rule:** never `Easing.linear` — use `Easing.bezier(0.25,0.1,0.25,1)` or `Easing.out(Easing.exp)`
- **Skill pack:** `skills/remotion-programmatic-video/SKILL.md`

### Whisper.cpp subtitles

- **Binary:** `whisper-cli` (built from `github.com/ggerganov/whisper.cpp`)
- **Recipe:** `whisper-cli -m models/ggml-large-v3.bin -osrt -ovtt -ow -oj -ml 42 -l en input.wav`
- **Karaoke ASS:** convert word-level JSON to ASS with `\k` tags → FFmpeg `subtitles=` burn-in
- **Skill pack:** `skills/whisper-cpp-subtitles/SKILL.md`

### DaVinci Resolve Python API

- **Module:** `DaVinciResolveScript` (ships in Resolve install at `Support/Developer/Scripting/Modules/`)
- **Best for:** scopes-accurate primary/secondary node grading, render queue automation, batch-applying `.drx` color presets, LUT per node
- **Skill pack:** `skills/davinci-resolve-python-scripting/SKILL.md`

### YouTube Data API v3

- **Endpoints:** `videos.list?chart=mostPopular&regionCode=US` (1 unit), `search.list?q=...&order=viewCount` (100 units), `playlistItems.list` (1 unit cheap path for channel uploads)
- **Free quota:** 10,000 units/day
- **Hook-mining workflow:** search top → `videos.list` hydrate → `youtube-mcp-transcript` for first-15s pattern extraction
- **Skill pack:** `skills/youtube-data-api-v3/SKILL.md`

### TikTok Research API

- **Endpoint:** `POST https://open.tiktokapis.com/v2/research/video/query/` (requires app approval via Developer Portal)
- **Fallback while pending:** Apify `clockworks/tiktok-trending-hashtags-scraper` (paid ~$30/mo for 50K)
- **Workflow:** trending hashtags → Apify scraper for top videos → Whisper.cpp on first-3s → cluster hooks
- **Skill pack:** `skills/tiktok-trend-research/SKILL.md`

### Pexels API

- **Endpoint:** `GET https://api.pexels.com/videos/search?query=X&orientation=landscape&size=large` with `Authorization` header
- **Quota:** free, 200 req/hr
- **License:** commercial-clean, no attribution required
- **Skill pack:** `skills/stock-footage-pexels-pixabay/SKILL.md`

### Pixabay API

- **Endpoint:** `GET https://pixabay.com/api/videos/?key=...&q=X`
- **Quota:** free, fair-use (unlimited within reason)
- **License:** commercial-clean, no attribution required
- **Skill pack:** `skills/stock-footage-pexels-pixabay/SKILL.md`

### Submagic API

- **Endpoint:** `POST https://api.submagic.co/v1/projects -F video=@in.mp4 -F template=hormozi`
- **Cost:** $69/mo Business tier
- **Best for:** viral animated captions (Mr Beast / Hormozi templates) without coding the ASS by hand
- **Alternative:** Whisper.cpp + ASS karaoke + FFmpeg `subtitles=` (free, covered in `skills/whisper-cpp-subtitles/SKILL.md`)

### Hedra Character-3

- **Endpoint:** `POST https://api.hedra.com/web-app/public/generations -F audio=@vo.wav -F image=@face.png -F aspect_ratio=9:16 -F model_id=character-3`
- **Cost:** ~$0.30/sec
- **Quality:** 9/10 lip-sync (SOTA in June 2026)
- **Use case:** AI talking-head narrator when on-camera talent unavailable; foreign-language dub w/ mouth-shape match
- **Skill pack:** `skills/hedra-avatar-lipsync/SKILL.md`

### Suno API (unofficial)

- **Endpoint:** `POST https://api.sunoapi.org/api/v1/generate` (reverse-engineered wrapper)
- **Cost:** ~$10/mo
- **Status:** ToS-gray; **use Mubert for brand/commercial work**
- **Skill pack:** `skills/ai-music-suno-mubert/SKILL.md`

### Mubert API

- **Endpoint:** `POST https://api-b2b.mubert.com/v2/RecordTrack` with `params.pat`, `duration`, `intensity`, `tags`
- **Cost:** $14–$199/mo
- **License:** fully cleared for commercial + Content ID whitelist process available
- **Skill pack:** `skills/ai-music-suno-mubert/SKILL.md`

### Photoshop MCP

- **Calls:** `ps.open()`, `ps.select_subject()`, `ps.refine_edge()`, `ps.add_text_layer()`, `ps.export()`
- **Best for:** thumbnail face cutout + text overlay composition after AI bg generation
- **Requires:** Photoshop running locally with UXP plugin installed
- **Skill pack:** `skills/thumbnail-composition-photoshop/SKILL.md`

### Cross-tool playbooks

- **End-to-end AI vertical reel:** Sora 2 hook + Kling 3.0 B-roll → FFmpeg `xfade` stitch → ElevenLabs VO + FFmpeg loudnorm → Whisper.cpp karaoke ASS → FFmpeg burn-in + TikTok export preset. See `reference/SOTA_USE_CASES.md` for per-use-case fulfillment matrix.
- **Brand-narrator series:** Flux 2 Pro seed-locked face + ElevenLabs cloned voice + Hedra Character-3 → series-consistent AI presenter.
- **Color-graded YouTube long-form:** Pexels B-roll + FFmpeg `lut3d` (or DaVinci Python) at 70% opacity + ElevenLabs VO + Whisper.cpp SRT (soft) + FFmpeg YouTube 1080p export.

---

## Brief templates

### Video brief template

```markdown
# Video Brief: [Working Title]

## Objective
- Primary: [subscribe / click / buy / share / awareness]
- Success metric: [specific KPI with target]

## Platform(s)
- Primary: [YouTube long-form / YouTube Shorts / TikTok / Reels / ad]
- Secondary (adaptation targets): [list]

## Audience
- Persona: [link to persona doc]
- Stage of journey: [awareness / consideration / decision / retention]

## Hook (first 3 seconds for short-form, first 15s for long-form)
- Type: [visual surprise / sonic surprise / promise / pattern interrupt]
- Content: [the actual hook]

## Story Arc
- Setup: [...]
- Conflict / tension: [...]
- Resolution: [...]

## Shot List
| Shot # | Scale | Movement | Description | Est. duration |
|--------|-------|----------|-------------|---------------|
| 1      | ...   | ...      | ...         | ...           |

## B-Roll List
- [list of supplementary footage]

## Brand Voice / Style
- Voice: [formal / conversational / playful]
- Color grade direction: [cinematic / Japanese fresh / cyberpunk / vintage / custom]
- Editing pacing: [fast / medium / slow]

## Music / SFX
- BGM mood: [...]
- Licensing source: [platform library / Epidemic Sound / Suno custom]

## Deliverables
- Master file (highest quality): [resolution / codec / bitrate]
- Platform exports: [list per platform with specs]
- Thumbnail variations: [3 concepts]
- Title variations: [5 options]

## Timeline
- Pre-production: [dates]
- Shoot: [dates]
- Edit: [dates]
- Review + revisions: [dates]
- Delivery: [date]
```

### Shot list template

```markdown
| Shot # | Scale | Movement | Description | Audio cue | Est. duration |
|--------|-------|----------|-------------|-----------|---------------|
| S01    | CU    | static   | Opening hook — face reacting to surprise | BGM downbeat | 3s |
| S02    | MS    | dolly L  | Walking through environment, looking | Voice-over narration | 8s |
| ...    | ...   | ...      | ...         | ...       | ...           |
```

### Editing direction template

```markdown
## Edit Direction: [Project Name]

### Software
- Editor: [CapCut / PR / DaVinci / FCP]
- Project file: [link]

### Workflow status
- [ ] Rough cut complete (narrative skeleton)
- [ ] Fine cut complete (frame-accurate edit points + transitions + speed ramps)
- [ ] Color correction complete (primary)
- [ ] Color grading complete (secondary + stylistic)
- [ ] Audio mix complete (voice + BGM + SFX + master loudness)
- [ ] Subtitles complete (AI gen + manual review + style + layout)
- [ ] Multi-platform exports complete

### Color targets
- Footage shoot mode: [LOG / standard]
- Technical LUT: [applied / not needed]
- Primary correction targets: [white balance / exposure / contrast notes]
- Stylistic direction: [cinematic / etc.]
- LUT opacity: [60-80%]

### Audio targets
- Voice level: [-12 to -6 dB]
- BGM level: [-24 to -18 dB for talking-head]
- SFX level: [-18 to -12 dB]
- Master loudness: -14 LUFS
- Peak: ≤ -1 dBFS

### Export specs
| Platform | Aspect | Resolution | fps | Bitrate | Codec |
|----------|--------|------------|-----|---------|-------|
| YouTube  | 16:9   | 1920×1080  | 30  | 12 Mbps | H.264 |
| Shorts   | 9:16   | 1080×1920  | 30  | 10 Mbps | H.264 |
```

---

## Common platform constraint reference

| Platform | Aspect | Max length | Notes |
|---|---|---|---|
| YouTube (long-form) | 16:9 | 12 hours | Optimize for CTR + retention; chapter markers |
| YouTube Shorts | 9:16 | 60s | Sound on, vertical native |
| TikTok | 9:16 | 10 min (some accounts), 60s typical | Trending sound integration |
| Instagram Reels | 9:16 | 90s | Sound on, vertical |
| Instagram Stories | 9:16 | 15s per slide | Stickers, links if eligible |
| LinkedIn video | 16:9 or 1:1 | 10 min | Professional context, B2B angle |
| X / Twitter video | 16:9 or 9:16 | 2:20 (most accounts) | Auto-play, sound off by default |
