# Video Creator — Source Attribution

Section-to-source map. **Not** loaded into context — for human verification.

Raw downloads in `reference/agents/`. URLs in `agent.yaml → sources` and `reference/INVENTORY.md`.

---

## soul.md → source map

| Section | Source(s) |
|---|---|
| Opening identity + 3 convictions | `msitarzewski-short-video-editing-coach.md` (Critical Rules — Editing Mindset Over Software Skills) |
| Purpose | composition synthesizing the four references' purposes around the video specialist niche |
| When invoked — Script + pre-production | `msitarzewski-visual-storyteller.md` (Story Arc Creation + Emotional Journey Mapping) + `msitarzewski-tiktok-strategist.md` (Hook in 3 Seconds) + `msitarzewski-video-optimization-specialist.md` (Package step) |
| When invoked — Editing direction | `msitarzewski-short-video-editing-coach.md` (Workflow Process — 5 steps) |
| When invoked — Color grading direction | `msitarzewski-short-video-editing-coach.md` (Color Grading & Correction section) |
| When invoked — Audio direction | `msitarzewski-short-video-editing-coach.md` (Audio Engineering section) |
| When invoked — Thumbnail + title (YouTube) | `msitarzewski-video-optimization-specialist.md` (Visual Strategy + Package + Optimize) + `msitarzewski-short-video-editing-coach.md` (Thumbnail design) |
| When invoked — Trend / viral (TikTok / Reels / Shorts) | `msitarzewski-tiktok-strategist.md` (entire file — hook, content pillars, viral formulas, algorithm, hashtag strategy) |
| When invoked — Multi-platform adaptation | `msitarzewski-short-video-editing-coach.md` (Multi-Platform Export Optimization) + `msitarzewski-visual-storyteller.md` (Cross-Platform Adaptation) |
| Core operating rules | merged: `msitarzewski-short-video-editing-coach.md` (every Critical Rule), `msitarzewski-tiktok-strategist.md` (Hook in 3 seconds, Trend integration), `msitarzewski-visual-storyteller.md` (Visual Storytelling Standards), `msitarzewski-video-optimization-specialist.md` (thumbnail decides 80% of CTR) |
| Mode-specific decisions | one entry per mode keyed to the matching reference |
| Content pillar mix | `msitarzewski-tiktok-strategist.md` (40/30/20/10 pillar mix) |
| Quality gates | `msitarzewski-short-video-editing-coach.md` (Success Metrics) + `msitarzewski-video-optimization-specialist.md` (Success Targets) + `msitarzewski-tiktok-strategist.md` (Performance Analytics) |
| Output format | composition synthesizing the templates and direction styles from references |
| Communication style | `msitarzewski-short-video-editing-coach.md` (Communication Style — direct examples lifted verbatim where useful) |
| When to push back | composition synthesis informed by Critical Rules in `msitarzewski-short-video-editing-coach.md` (e.g., LUT opacity, BGM > voice refusal, thumbnail watermark refusal) |
| When to defer | composition synthesis informed by Integration sections in references |
| First-conversation routine questions | standard PROACTIVE.md self-init pattern (PROGRESS.md decision #3); questions adapted to video-creator workflows |
| Closing rule | distilled from `msitarzewski-short-video-editing-coach.md` (narrative > software + every frame must earn its place) |

---

## role.md → source map

| Section | Source(s) |
|---|---|
| Capability reference → Editing software + decision tree | `msitarzewski-short-video-editing-coach.md` (Editing Software Mastery section) |
| Capability reference → Production capabilities | composition synthesizing the references' capability surfaces |
| Shot scale catalog | `msitarzewski-short-video-editing-coach.md` (Composition & Camera Language — Shot scales) |
| Camera movement catalog | `msitarzewski-short-video-editing-coach.md` (Camera movements) |
| Transition catalog | `msitarzewski-short-video-editing-coach.md` (Transition design) |
| Color grading workflow (primary + secondary + LUT + stylistic) | `msitarzewski-short-video-editing-coach.md` (Color Grading & Correction — entire section) |
| Audio engineering reference (noise + BGM + sound design + mix balance + voice enhancement) | `msitarzewski-short-video-editing-coach.md` (Audio Engineering — entire section) |
| Motion graphics + keyframe reference | `msitarzewski-short-video-editing-coach.md` (Motion Graphics & VFX section) |
| Subtitle typography reference | `msitarzewski-short-video-editing-coach.md` (Subtitles & Typography section) |
| Multi-platform export specs | `msitarzewski-short-video-editing-coach.md` (Multi-Platform Export Optimization) |
| Thumbnail composition rules | `msitarzewski-short-video-editing-coach.md` (Thumbnail design) + `msitarzewski-video-optimization-specialist.md` (Visual Strategy) |
| YouTube optimization playbook | `msitarzewski-video-optimization-specialist.md` (entire file — Four-step process, algorithm mastery, retention engineering, cross-platform syndication, success targets) |
| TikTok viral playbook | `msitarzewski-tiktok-strategist.md` (entire file — hook in 3 seconds, content pillar mix, viral formulas, algorithm mastery, hashtag strategy, creator tiers, success targets) |
| Story arc framework | `msitarzewski-visual-storyteller.md` (Visual Narrative Development — Story Arc Creation + Character Development + Conflict + Resolution + Emotional Journey Mapping + Visual Pacing) |
| Asset management + workflow | `msitarzewski-short-video-editing-coach.md` (Editing Workflow & Efficiency section — Asset management, Template-based batch production, Team collaboration, Keyboard shortcuts) |
| Five-step workflow | `msitarzewski-short-video-editing-coach.md` (Workflow Process) |
| AI editing tool reference | `msitarzewski-short-video-editing-coach.md` (AI-Assisted Editing section) |
| Common platform constraint reference | composition synthesizing platform spec details from `msitarzewski-short-video-editing-coach.md` (Export Optimization) + `msitarzewski-tiktok-strategist.md` (TikTok specifics) + general platform knowledge |
| Brief templates (video brief, shot list, editing direction) | composition synthesizing structure from `msitarzewski-short-video-editing-coach.md` (Workflow Process) + `msitarzewski-visual-storyteller.md` (Story arc development) + `msitarzewski-video-optimization-specialist.md` (Four-step process) |

---

## Notes on "authored from synthesis"

A few sections include composition synthesis on top of referenced material:

- **Opening three convictions in soul.md** — distills three load-bearing principles from `msitarzewski-short-video-editing-coach.md` into a memorable triad. Each principle comes from the reference; the triad framing is composed.
- **Production capabilities list** — synthesizes capability surfaces across all four references into a single list. Each capability is named in at least one reference.
- **Brief templates (video brief, shot list, editing direction)** — combines structure elements from the references into reusable templates. The sections come from references; the template format is composed.
- **Common platform constraint reference table** — combines platform-specific details from references with industry-standard platform constraints (which are public facts, not invented).
- **First-conversation routine questions** — standard PROACTIVE.md pattern adapted with video-creator-specific routines.

No domain claims, technical specs, or performance benchmarks were invented. Numeric targets (dB levels, LUFS, bitrate, CTR %, retention %) all come from references.

---

## How to update this agent

1. Re-fetch source files listed in `reference/INVENTORY.md` and overwrite `reference/agents/*.md` in place
2. Diff against previous versions
3. Update corresponding sections of `soul.md` and `role.md`
4. Update this `SOURCES.md` if section names or source URLs changed
5. Re-run `build.py` to regenerate `dist/video-creator.craftbot`

---

## SOTA tool sources (June 2026)

These citations back the `reference/SOTA_USE_CASES.md` matrix, the `## SOTA tool reference (June 2026)` section of `role.md`, and the bundled `skills/<name>/SKILL.md` packs.

| Tool | Source URL | Used for |
|---|---|---|
| Replicate MCP | https://replicate.com/docs/reference/mcp | One-auth access to Sora 2, Veo 3.1, Flux 2 Pro, Ideogram 3.0, Kling 3.0, Runway Gen-4 Turbo |
| Replicate HTTP API | https://replicate.com/docs/reference/http | REST fallback via `cli-anything`; polling pattern |
| Sora 2 | https://replicate.com/openai/sora-2 | Natural-language video generation ($0.10/sec) |
| Veo 3.1 | https://replicate.com/google/veo-3.1 | Photoreal video with native sync audio ($0.75/sec) |
| Kling 3.0 | https://replicate.com/kwaivgi/kling-v2.0 | High-motion video generation ($0.28/sec) |
| Runway Gen-4 Turbo | https://replicate.com/runwayml/gen-4-turbo | Image-to-video with camera-motion control ($0.50/sec) |
| Flux 2 Pro | https://replicate.com/black-forest-labs/flux-2-pro | Photoreal image gen (storyboards, product, thumbnails) |
| Ideogram 3.0 | https://replicate.com/ideogram-ai/ideogram-v3 | Typography-strong image gen (thumbnails) |
| Recraft v3 | https://replicate.com/recraft-ai/recraft-v3 | Vector/illustration image gen |
| 851-labs background remover | https://replicate.com/851-labs/background-remover | AI background removal → transparent PNG |
| ElevenLabs MCP | https://github.com/elevenlabs/elevenlabs-mcp | MCP wrapper for ElevenLabs API |
| ElevenLabs TTS API | https://elevenlabs.io/docs/api-reference/text-to-speech | Multilingual v2 + Turbo v2.5 + Flash v2.5 VO |
| ElevenLabs Voice Isolator | https://elevenlabs.io/docs/api-reference/audio-isolation | Noise removal (SOTA, beats FFmpeg afftdn) |
| ElevenLabs Dubbing v2 | https://elevenlabs.io/docs/api-reference/dubbing | Cross-language dubbing with speaker preservation |
| ElevenLabs Sound Generation | https://elevenlabs.io/docs/api-reference/sound-generation | AI SFX generation |
| FFmpeg `lut3d` filter | https://ffmpeg.org/ffmpeg-filters.html#lut3d | 3D LUT application (tetrahedral interp) |
| FFmpeg `eq` filter | https://ffmpeg.org/ffmpeg-filters.html#eq | Primary color correction |
| FFmpeg `colorbalance` filter | https://ffmpeg.org/ffmpeg-filters.html#colorbalance | White balance + tint per tonal range |
| FFmpeg `curves` filter | https://ffmpeg.org/ffmpeg-filters.html#curves | Per-channel tone curves |
| FFmpeg `blend` filter | https://ffmpeg.org/ffmpeg-filters.html#blend | LUT opacity blend (60–80%) |
| FFmpeg `loudnorm` filter | https://ffmpeg.org/ffmpeg-filters.html#loudnorm | Broadcast loudness norm (-14 LUFS / -1 dBFS) |
| FFmpeg `compand` filter | https://ffmpeg.org/ffmpeg-filters.html#compand | Voice compression chain |
| FFmpeg `sidechaincompress` | https://ffmpeg.org/ffmpeg-filters.html#sidechaincompress | BGM ducking under voice |
| FFmpeg `afftdn` filter | https://ffmpeg.org/ffmpeg-filters.html#afftdn | Spectral noise reduction |
| FFmpeg `subtitles` filter | https://ffmpeg.org/ffmpeg-filters.html#subtitles | Subtitle burn-in (SRT/ASS) |
| FFmpeg `xfade` filter | https://ffmpeg.org/ffmpeg-filters.html#xfade | Crossfade / transition between clips |
| FFmpeg `scale` + `crop` | https://ffmpeg.org/ffmpeg-filters.html#scale-1 | Vertical re-crop for TikTok/Reels/Shorts |
| FFmpeg H.264 encode wiki | https://trac.ffmpeg.org/wiki/Encode/H.264 | Codec settings reference |
| FFmpeg H.265 encode wiki | https://trac.ffmpeg.org/wiki/Encode/H.265 | HEVC settings reference |
| YouTube upload specs | https://support.google.com/youtube/answer/1722171 | Resolution / bitrate / codec targets |
| YouTube loudness norm | https://support.google.com/youtube/answer/9890749 | -14 LUFS normalization target |
| Spotify loudness norm | https://artists.spotify.com/en/help/article/loudness-normalization | Cross-platform loudness reference |
| TikTok upload specs | https://creators.tiktok.com/help/article?aid=10042422 | 9:16 1080×1920 spec |
| Remotion docs | https://www.remotion.dev/docs/renderer | React/TSX programmatic video |
| Remotion animation | https://www.remotion.dev/docs/animating-properties | Keyframe animation, `interpolate`, `Easing` |
| Remotion easing | https://www.remotion.dev/docs/easing | Cubic-bezier / preset easing curves |
| Remotion three | https://www.remotion.dev/docs/three | Particle FX / 3D via `@remotion/three` |
| Remotion Lambda | https://www.remotion.dev/docs/lambda | Cloud parallel render |
| Whisper.cpp | https://github.com/ggerganov/whisper.cpp | Local STT for SRT/VTT/ASS w/ word-level timestamps |
| ASS subtitle format spec | http://www.tcax.org/docs/ass-specs.htm | Karaoke `\k` tags + styling |
| Photoshop UXP API | https://developer.adobe.com/photoshop/uxp/2022/uxp-api/ | `photoshop-mcp` bridge target |
| DaVinci Resolve developer download | https://www.blackmagicdesign.com/products/davinciresolve | Scripting manual at `Support/Developer/Scripting/` |
| Resolve user manual | https://documents.blackmagicdesign.com/UserManuals/DaVinciResolve19-Documentation.pdf | Color page + Fusion reference |
| YouTube Data API videos.list | https://developers.google.com/youtube/v3/docs/videos/list | Trending + competitor stats |
| YouTube Data API search.list | https://developers.google.com/youtube/v3/docs/search/list | Keyword-based search |
| YouTube Data API channels.list | https://developers.google.com/youtube/v3/docs/channels/list | Channel stats |
| YouTube Data API quota | https://developers.google.com/youtube/v3/getting-started#quota | 10,000 units/day budget math |
| TikTok Research API | https://developers.tiktok.com/doc/research-api-specs-query-videos | Official trending query API |
| TikTok Research API overview | https://developers.tiktok.com/doc/about-research-api | App approval + scopes |
| Apify TikTok Trending Hashtags | https://apify.com/clockworks/tiktok-trending-hashtags-scraper | Fallback scraper while official auth pending |
| Apify TikTok Scraper | https://apify.com/clockworks/tiktok-scraper | Per-hashtag video pulls |
| Phyllo | https://docs.getphyllo.com/ | Creator analytics + audience demos |
| Pexels API docs | https://www.pexels.com/api/documentation/ | Free stock video API (200 req/hr) |
| Pexels License | https://www.pexels.com/license/ | Commercial-use license terms |
| Pixabay API docs | https://pixabay.com/api/docs/ | Free stock video + image API |
| Pixabay License | https://pixabay.com/service/license/ | Commercial-use license terms |
| Submagic API | https://submagic.co/api-docs | Viral animated captions ($69/mo) |
| Hedra docs | https://www.hedra.com/docs | Character-3 lip-sync API |
| Hedra API reference | https://docs.hedra.com/api-reference/ | Generation endpoint + polling |
| Suno (unofficial wrapper) | https://sunoapi.org/api-docs | AI music gen (ToS-gray) |
| Mubert API | https://mubert.com/api | Licensed AI music for commercial work |
| Mubert docs | https://docs.mubert.com/ | RecordTrack + tags taxonomy |
| AIVA | https://www.aiva.ai/ | Cinematic / orchestral AI music |
| Soundraw | https://soundraw.io/api | Stem-aware AI music |
| Beatoven | https://www.beatoven.ai/ | Mood-based AI music |
| Notion API | https://www.notion.so/help/api-and-integrations | Asset / pipeline tracking via `notion-mcp` |
| rclone docs | https://rclone.org/docs/ | 3-2-1 backup automation via `cli-anything` |

**Provenance note:** every cost figure, model slug, endpoint URL, filter syntax, and quota number above is sourced from the linked documentation as of June 2026. Re-verify before publishing material to brand customers; vendor pricing and quotas drift.
