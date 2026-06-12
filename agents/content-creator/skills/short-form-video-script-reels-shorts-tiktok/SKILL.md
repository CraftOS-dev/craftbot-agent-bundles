# Short-Form Video Script — Reels / TikTok / YouTube Shorts + Submagic

> Write 3-second-hook scripts, polish captions via Submagic, and ship to TikTok / Reels / Shorts.

## When to use

Trigger on: "write a TikTok script", "Reels script", "Shorts script", "short-form video script", "hook variation for short-form", "make me a 30-second script", "Submagic this clip". This skill owns: hook-first script writing, 40/30/20/10 pillar mix, Submagic auto-edit handoff, per-platform format tweaks. For long-form-to-short-form video conversion see `repurposing-pipeline-1-to-10` (OpusClip handles the AI moment selection). For deep video craft (color grading, FFmpeg color science, AI video gen) defer to `video-creator`.

## Setup

```bash
# Submagic Business+ API
curl -H "Authorization: Bearer $SUBMAGIC_API_KEY" https://api.submagic.co/v1/me

# Buffer for cross-platform schedule
npx @buffer/mcp-server --version

# TikTok MCP for native publishing
npx -y @tiktok/mcp-server@latest

# Instagram MCP for Reels publishing
npx -y @insta-business/mcp-server@latest
```

Auth env vars:
- `SUBMAGIC_API_KEY` — Submagic Business+ plan ($69/mo) settings → API. Pro plan doesn't expose API.
- `TIKTOK_ACCESS_TOKEN` — TikTok for Business API.
- `INSTAGRAM_ACCESS_TOKEN` — Meta Business API access token.
- `BUFFER_ACCESS_TOKEN`

## Common recipes

### Recipe 1: 3-second-hook script template

```markdown
# Script: <working title>
**Platform:** TikTok | Reels | YouTube Shorts | All
**Length:** 15-30s | 30-45s | 45-60s | 60-90s
**Format:** Talking head | Voiceover B-roll | Demo | Reaction | Listicle | Storytelling

## Hook (0-3s)
<single pattern interrupt — must stop the thumb-scroll>
Options:
- Surprising stat: "85% of <thing> is <unexpected>"
- Contrarian: "Everyone's wrong about <X>"
- Specific outcome: "How I went from <A> to <B> in <time>"
- Visual pattern interrupt: zoom-in on object, before/after, hand gesture

## Setup / context (3-8s)
<one sentence to ground the viewer in the problem>

## Body (8-25s)
<the actual content — 3-5 beats max>
- Beat 1
- Beat 2
- Beat 3
- Beat 4 (optional)

## Payoff (25-30s)
<the punchline, the lesson, the reveal>

## CTA (last 2-5s)
<single explicit ask>
- "Follow for more"
- "Save this for later"
- "Comment <X> for the link"
- "Link in bio"

## Captions (read on screen)
<keep punchy; mobile-readable; under 32 chars/line>
```

### Recipe 2: Pillar mix (40/30/20/10)

```markdown
**Educational (40%):** teach a specific skill or concept
- How-to walkthroughs
- Tool tutorials
- Concept explainers
- Case study breakdowns

**Entertainment (30%):** make them feel something
- Storytelling
- Reactions
- Trends
- Humor

**Inspirational (20%):** make them want to be/do something
- Behind-the-scenes
- Origin stories
- Vision/mission posts

**Promotional (10%):** explicit business ask
- New product/episode/newsletter
- Direct CTA to lead magnet
- Sale or launch
```

Flipping the ratio kills the algo. Track in Notion: `Pillar` property per video.

### Recipe 3: Submagic caption + B-roll polish

```bash
# Upload raw clip; Submagic returns polished version with captions + B-roll
curl -X POST https://api.submagic.co/v1/projects \
  -H "Authorization: Bearer $SUBMAGIC_API_KEY" \
  -F "video=@raw.mp4" \
  -F "template=energetic" \
  -F "language=en" \
  -F "remove_dead_air=true" \
  -F "auto_broll=true" \
  -F "auto_zoom=true" \
  -F "punctuation=auto"

# Returns {"project_id":"sm_xxx","status":"processing"}

# Poll for ready
curl -H "Authorization: Bearer $SUBMAGIC_API_KEY" \
  "https://api.submagic.co/v1/projects/sm_xxx" | jq .status

# Download polished output
curl -L -o polished.mp4 "<download_url_from_project_response>"
```

Submagic templates: `energetic`, `clean`, `modern`, `corporate`, `karaoke`. Pick `energetic` for TikTok/Reels; `clean` for LinkedIn video.

### Recipe 4: Submagic language config (48 langs)

```bash
# Auto-detect language
curl -X POST https://api.submagic.co/v1/projects \
  -F "video=@raw.mp4" \
  -F "language=auto"

# Force specific language (use ISO 639-1 code)
curl -X POST https://api.submagic.co/v1/projects \
  -F "video=@raw.mp4" \
  -F "language=es"

# Translate audio to English (AI Video Translator — 100+ langs)
curl -X POST https://api.submagic.co/v1/projects \
  -F "video=@raw_japanese.mp4" \
  -F "language=ja" \
  -F "translate_to=en"
```

Submagic claims 99% caption accuracy in 48 languages natively + 100+ langs for AI Video Translator.

### Recipe 5: Hook variation (write 10, ship best 3)

```python
# Use brainstorming skill or Claude generation to spit 10 hook variations
prompts = [
    "Surprising stat hook for 'Tuesday-6am beats Sunday-night newsletter sends'",
    "Contrarian hook for the same topic",
    "Specific-outcome hook",
    "Question hook",
    "Story hook (start mid-action)",
    "Pattern interrupt visual hook",
    "Direct-address hook ('If you...')",
    "Stakes hook ('Most people lose...')",
    "Authority hook ('I tested 30 ESPs...')",
    "Reframe hook ('It's not X — it's Y')"
]

# A/B test top 3 on the same content; the algo signals which hook style works for your audience
```

### Recipe 6: TikTok native publishing

```bash
# TikTok MCP publish
npx @tiktok/mcp-server create_video \
  --video-file polished.mp4 \
  --caption "$(cat caption.txt)" \
  --hashtags "creator,newsletter,operator" \
  --privacy public \
  --allow-comments true \
  --allow-duet true \
  --allow-stitch true
```

### Recipe 7: Instagram Reels publishing

```bash
npx @insta-business/mcp-server create_reel \
  --video-file polished.mp4 \
  --caption "$(cat caption.txt)" \
  --location-id "<optional>" \
  --share-to-feed true \
  --hashtags-first-comment true
```

### Recipe 8: YouTube Shorts publishing

```bash
# Via youtube-mcp
npx @youtube/mcp-server videos_insert \
  --video-file polished.mp4 \
  --title "Why Tuesday-6am wins (60s)" \
  --description "Hook + 3 beats + CTA. Full episode → link in bio. #Shorts" \
  --tags "newsletter,operator,creator,shorts" \
  --privacy public \
  --made-for-kids false
```

`#Shorts` in title or description signals YouTube to surface in Shorts feed.

### Recipe 9: Cross-platform Buffer cascade

```bash
# After polished.mp4 + per-platform caption variants ready
for PLATFORM in tiktok instagram youtube; do
  CAPTION=$(cat caption_$PLATFORM.txt)
  npx @buffer/mcp-server create_post \
    --platform $PLATFORM \
    --content "$CAPTION" \
    --media-file polished.mp4 \
    --scheduled-at "2026-06-17T17:00:00Z"
done
```

### Recipe 10: Performance audit (cut formats not working)

```bash
# 72h after publish, pull stats per platform
TIKTOK_VIEWS=$(npx @tiktok/mcp-server get_video_stats --video-id <id> | jq .views)
REELS_VIEWS=$(npx @insta-business/mcp-server get_reel_stats --reel-id <id> | jq .plays)
SHORTS_VIEWS=$(npx @youtube/mcp-server videos_list --video-id <id> | jq .statistics.viewCount)

# Push to Notion editorial DB row for analysis
# If view count < 500 across 5 consecutive videos in a format → format isn't working; iterate hook style
```

### Recipe 11: TikTok trend integration

```bash
# Use marketing-agent's tiktok-trend-research skill to identify trending sounds + formats
# Then write a script that integrates a trending element while keeping your core insight
```

### Recipe 12: First-comment hashtag pinning

```bash
# Hashtags in the first comment (not the caption) keep caption clean
# All three platforms support; auto-flag via Buffer:
npx @buffer/mcp-server create_post \
  --content "$(cat caption.txt)" \
  --first-comment "#newsletter #creator #operator #marketing"
```

## Examples

### Example 1: 30-second TikTok with 3-second hook, 99% captions, cross-platform

**Goal:** Publish a 30-second educational TikTok about "newsletter open rates lie" — also publish to Reels + Shorts.

**Steps:**
1. Recipe 1: write script (hook: "Open rates are the most lied-about metric in newsletters" / setup / 3 beats / payoff / CTA).
2. Recipe 5: write 10 hook variations; pick top 3.
3. Record raw clip in 9:16 vertical.
4. Recipe 3: upload to Submagic with `template=energetic`, `language=en`, `remove_dead_air=true`.
5. Pull polished.mp4.
6. Write per-platform captions: TikTok (irreverent), Reels (visual hook callout), Shorts (educational framing).
7. Recipe 9: Buffer cascade — schedule all three for Tuesday 5pm ET.
8. Recipe 10 at +72h: pull stats; if any platform <500 views, iterate hook.

**Result:** 1 clip → 3 platforms → 1 script → measured.

### Example 2: 60-second Reels with B-roll auto-search

**Goal:** Talking-head Reel that needs B-roll to break up the visual monotony.

**Steps:**
1. Recipe 1: 60s talking-head script.
2. Record raw with you on camera.
3. Recipe 3: Submagic with `auto_broll=true` — Submagic searches for relevant B-roll and inserts at sentence transitions.
4. Manual review of B-roll picks (Submagic occasionally picks unrelated stock).
5. Publish to Reels + Shorts (skip TikTok for talking-head; TikTok algorithm rewards face-first content).

**Result:** Talking-head Reel that doesn't bore viewers visually.

### Example 3: Multilingual version for ES audience

**Goal:** Publish a Spanish version of your English short to a Spanish-speaking audience.

**Steps:**
1. Recipe 4: Submagic AI Video Translator — input English clip, `translate_to=es`.
2. Submagic dubs voice + regenerates captions in Spanish.
3. Manual review: native speaker check (Submagic is 90% accurate but idioms drift).
4. Publish to ES TikTok / Reels / Shorts.

**Result:** Same content reaches Spanish-speaking audience without re-recording.

## Edge cases / gotchas

- **3-second hook is non-negotiable.** TikTok / Reels / Shorts all kill watch time when first 3s don't grab. If average watch time <3s → 0 distribution.
- **Pillar mix discipline.** Flipping 10% promo → 50% promo kills algorithm reach within a week.
- **Captions visible without sound** — 80%+ of mobile users watch sound-off. Burned-in captions non-negotiable.
- **9:16 aspect ratio for vertical.** TikTok / Reels / Shorts. Don't repurpose 16:9 with letterboxes — algorithm down-ranks.
- **Submagic auto-zoom can over-zoom faces.** Disable `auto_zoom=false` if filming close.
- **Submagic Business+ plan ($69/mo)** for API access. Pro plan only has the GUI.
- **TikTok algorithm rewards posting 1-3x/day** on consistent times.
- **YouTube Shorts <60s required**; over 60s = treated as regular video and de-prioritized in Shorts shelf.
- **Reels algorithm 2026** prefers vertical, 15-30s, sound-on (but captions still needed for mobile).
- **Posting same clip to all 3 platforms without per-platform tweaks** signals "low effort cross-poster" to algos. Always vary caption + hashtags + scheduled time.
- **First-comment hashtags work better** than caption hashtags on Reels and TikTok (cleaner UX + same algo signal).
- **Don't hashtag-bomb** — 4-7 niche hashtags >> 20 spammy hashtags.
- **CTA timing** — last 2-5s; not at start. Front-loading the ask reduces hook power.
- **Submagic English caption accuracy = 99%; other langs slightly lower (94-97%).** Always proofread.
- **Defer color grading / FFmpeg color science** to `video-creator` agent.

## Sources

- [Submagic](https://www.submagic.co/)
- [Submagic review 2026](https://max-productive.ai/ai-tools/submagic/)
- [TikTok for Business API](https://business-api.tiktok.com/portal/docs)
- [Instagram Reels API (Meta Business)](https://developers.facebook.com/docs/instagram-api/guides/content-publishing)
- [YouTube Shorts API](https://developers.google.com/youtube/v3/docs/videos/insert)
- [3-second hook research](https://www.thoughtleaders.io/blog/podcast-trends-2026)
- [TikTok trending sounds (research skill)](https://www.tiktok.com/creators/creator-portal/en-us/)
