# Repurposing Pipeline 1→10 — Castmagic + OpusClip + Submagic + Headliner + Buffer Cascade

> Take one tentpole (podcast / newsletter / video) and produce 10+ derivative assets in a single chained pipeline.

## When to use

Trigger on: "repurpose my podcast", "turn this episode into a week's worth of content", "1 to 10", "make derivatives from this video / newsletter / blog post", "build the repurposing pipeline", "cascade across platforms". This skill is the chain orchestrator — it calls into Castmagic for text derivatives, OpusClip for short-form video, Submagic for caption polish, Headliner for audiograms, Canva for graphics, Typefully for threads, Buffer for multi-platform schedule. Per-format detail lives in the format-specific skills (this one orchestrates).

## Setup

```bash
# Tools required across the chain
npx @castmagic/mcp-server@latest --help          # text derivatives
curl https://api.opus.pro/v1/projects -H "Authorization: Bearer $OPUSCLIP_API_KEY"   # video clips
curl https://api.submagic.co/v1/projects -H "Authorization: Bearer $SUBMAGIC_API_KEY" # caption / B-roll polish
# Headliner — no public API; RSS autopilot or manual export
npx @typefully/cli --version                      # thread cascade
npx @buffer/mcp-server                            # cross-platform schedule
```

Auth env vars (each format owns its own; this skill orchestrates):
- `CASTMAGIC_API_KEY`
- `OPUSCLIP_API_KEY` — OpusClip dashboard; Pro plan for API.
- `SUBMAGIC_API_KEY` — Business+ plan only.
- `HEADLINER_RSS_FEED` — RSS feed URL that Headliner Pro monitors for autopilot.
- `TYPEFULLY_API_KEY`
- `BUFFER_ACCESS_TOKEN`

## Common recipes

### Recipe 1: Podcast → 10+ derivatives chain

```bash
# Input: master.mp3, master.mp4, transcript.json

# 1. Castmagic text derivatives
curl -X POST https://api.castmagic.io/v1/uploads \
  -H "Authorization: Bearer $CASTMAGIC_API_KEY" \
  -F "file=@master.mp3"
# Returns upload_id; poll for ready, then request derivatives:
curl -X POST "https://api.castmagic.io/v1/uploads/$UPLOAD_ID/derivatives" \
  -d '{"types":["show_notes","newsletter_writeup","x_thread","blog_post","quotes","linkedin_carousel_outline"]}'

# 2. OpusClip video moments (long → 3-5 short clips)
curl -X POST https://api.opus.pro/v1/projects \
  -H "Authorization: Bearer $OPUSCLIP_API_KEY" \
  -F "video=@master.mp4" \
  -F "max_clips=5" \
  -F "aspect_ratio=9:16" \
  -F "include_captions=true" \
  -F "include_broll=true"
# Returns project_id; poll for ready

# 3. Submagic caption polish (each short clip → 99% accurate captions + B-roll polish)
for CLIP in clips/*.mp4; do
  curl -X POST https://api.submagic.co/v1/projects \
    -H "Authorization: Bearer $SUBMAGIC_API_KEY" \
    -F "video=@$CLIP" \
    -F "template=energetic" \
    -F "language=en"
done

# 4. Headliner audiogram via RSS autopilot (set once; runs on every new episode)
# Pro plan dashboard → RSS feed input → maps episodes to audiogram template

# 5. Canva quote graphics (3-5 cards from Castmagic 'quotes' derivative)
# See linkedin-carousel-authoring + infographic-canva-piktochart-visme skills for details

# 6. Typefully thread cascade
npx typefully send \
  --content "$(cat thread.txt)" \
  --schedule "2026-06-17T14:00:00Z" \
  --cross-publish "linkedin,threads,bluesky,mastodon"

# 7. Buffer cascade for everything else (LinkedIn post, IG carousel, FB, TikTok, Pinterest, Reddit)
npx @buffer/mcp-server schedule \
  --post-id "<post>" \
  --platforms "linkedin,instagram,tiktok,facebook,pinterest" \
  --scheduled-at "2026-06-17T14:00:00Z"
```

### Recipe 2: Newsletter → 10+ derivatives chain

```bash
# Input: issue.md (Markdown source)

# 1. LinkedIn carousel from key insights
# Pull top 8-10 insights via Claude; pass to Postiv/Carosello (see linkedin-carousel-authoring)

# 2. X thread distilled to thesis tweets
# 8-12 tweet thread; cascade via Typefully

# 3. LinkedIn long-form post (re-cut for LinkedIn voice)

# 4. Audio version (ElevenLabs TTS read + RSS-private feed)
curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/<voice_id>" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -d '{"text":"<issue body>","model_id":"eleven_monolingual_v1"}' \
  > issue_audio.mp3

# 5. Blog post (same content, SEO header structure)

# 6. Canva quote graphics (3-5 from pull-quotes)

# 7. Instagram carousel (visual-first restructure)

# 8. Reddit cross-post (adapted to community norms)

# 9. Newsletter cross-promotion partners (Beehiiv Boosts or organic swaps)

# 10. Podcast monologue episode (if cadence allows)
```

### Recipe 3: YouTube long-form → 10+ derivatives chain

```bash
# Input: master.mp4 (12-min explainer)

# 1. OpusClip 3-5 YouTube Shorts
curl -X POST https://api.opus.pro/v1/projects \
  -H "Authorization: Bearer $OPUSCLIP_API_KEY" \
  -F "video=@master.mp4" \
  -F "max_clips=5" \
  -F "aspect_ratio=9:16"

# 2. TikTok / Reels same clips on different platforms (Buffer cascade)

# 3. LinkedIn video (60-90s top moment landscape 16:9)
ffmpeg -i clip_1.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1" linkedin.mp4

# 4. X thread (script-derived, written from video transcript)

# 5. Newsletter issue with embed

# 6. Blog post with embed + transcript (SEO + searchable)

# 7. Audiogram of audio-only excerpt (see audiogram-headliner-wavve)

# 8. Quote graphics 3-5 (Canva from script)

# 9. Email teaser to newsletter list

# 10. Pinterest pin (top frame + headline overlay)
```

### Recipe 4: Daily-schedule template (per tentpole)

| Day | Asset | Platform | Owner |
|---|---|---|---|
| Mon AM | Tentpole | Native + RSS | Author |
| Mon PM | LinkedIn carousel | LinkedIn | Buffer schedule |
| Tue AM | X thread | X / Threads / Bluesky / Mastodon | Typefully cascade |
| Tue PM | Short clip 1 | TikTok / Reels / Shorts | Buffer schedule |
| Wed AM | Audiogram | Instagram / LinkedIn | Headliner RSS |
| Wed PM | Quote graphic 1 | IG / X / LinkedIn | Buffer schedule |
| Thu AM | Short clip 2 | TikTok / Reels / Shorts | Buffer schedule |
| Thu PM | Blog post | Owned blog | Manual publish |
| Fri AM | LinkedIn long-form | LinkedIn | Buffer schedule |
| Fri PM | Reddit cross-post | r/<relevant> | Manual |
| Sun AM | Quote graphic 2 + Newsletter teaser | IG + email | Buffer + ESP |

### Recipe 5: Pipeline orchestrator (chain everything)

```bash
#!/bin/bash
# repurpose.sh <tentpole_file> <tentpole_type>
TENTPOLE=$1
TYPE=$2  # podcast | newsletter | video

case $TYPE in
  podcast)
    # 1. Castmagic
    UPLOAD_ID=$(curl -X POST https://api.castmagic.io/v1/uploads -H "Authorization: Bearer $CASTMAGIC_API_KEY" -F "file=@$TENTPOLE" | jq -r .id)
    sleep 60  # wait for processing
    curl -X POST "https://api.castmagic.io/v1/uploads/$UPLOAD_ID/derivatives" -d '{"types":["show_notes","newsletter_writeup","x_thread","blog_post","quotes"]}'
    # 2. OpusClip (if video version exists)
    if [ -f "${TENTPOLE%.*}.mp4" ]; then
      curl -X POST https://api.opus.pro/v1/projects -F "video=@${TENTPOLE%.*}.mp4" -F "max_clips=5"
    fi
    # 3. Headliner RSS autopilot fires automatically on new RSS episode
    ;;
  newsletter)
    # Reference issue.md, run Castmagic on the text directly
    curl -X POST https://api.castmagic.io/v1/uploads -F "text=$(cat $TENTPOLE)" -F "types=x_thread,linkedin_carousel_outline,quotes"
    ;;
  video)
    # OpusClip + ffmpeg audio extraction → Castmagic for text
    ffmpeg -i $TENTPOLE -vn -c:a libmp3lame -b:a 192k audio.mp3
    curl -X POST https://api.castmagic.io/v1/uploads -F "file=@audio.mp3"
    ;;
esac

# Then in all cases: queue Typefully + Buffer schedules
echo "Derivatives queued; review in Notion editorial DB"
```

### Recipe 6: Pull-quote → 5 quote graphics

```bash
# From Castmagic 'quotes' output, hand to Canva MCP
QUOTES=$(curl -H "Authorization: Bearer $CASTMAGIC_API_KEY" "https://api.castmagic.io/v1/uploads/$UPLOAD_ID/derivatives" | jq -r '.quotes[]')

while IFS= read -r QUOTE; do
  npx @canva/mcp create_design \
    --template_id "$CANVA_QUOTE_TEMPLATE" \
    --customizations '[{"name":"quote_text","value":"'"$QUOTE"'"}]' \
    --output "quote_$(date +%s).png"
done <<< "$QUOTES"
```

### Recipe 7: Submagic batch polish (after OpusClip)

```bash
# OpusClip produces decent captions; Submagic polishes for native short-form quality
for CLIP in opusclip_output/*.mp4; do
  curl -X POST https://api.submagic.co/v1/projects \
    -H "Authorization: Bearer $SUBMAGIC_API_KEY" \
    -F "video=@$CLIP" \
    -F "template=energetic" \
    -F "language=en" \
    -F "remove_dead_air=true" \
    -F "auto_broll=true"
done
# Poll for renders; download polished outputs
```

### Recipe 8: Cascade scheduling (Buffer + Typefully)

```bash
# Typefully — thread-first (X / LinkedIn / Threads / Bluesky / Mastodon)
npx typefully draft \
  --content-file thread.txt \
  --cross-publish "x,linkedin,threads,bluesky,mastodon" \
  --schedule "2026-06-17T14:00:00Z"

# Buffer — everything else
for PLATFORM in linkedin instagram tiktok facebook pinterest; do
  npx @buffer/mcp-server create_post \
    --platform $PLATFORM \
    --content-file "platform_$PLATFORM.md" \
    --media-file "media_$PLATFORM.mp4" \
    --scheduled-at "2026-06-17T15:00:00Z"
done
```

### Recipe 9: Per-derivative KPI tracking

```bash
# 24h after each derivative publishes, pull stats into Notion editorial DB
# Per-platform:
# - LinkedIn (linkedin-marketing-api skill)
# - X (twitter-mcp)
# - YouTube (youtube-mcp)
# - TikTok (tiktok-mcp)
# - Instagram (insta-business-mcp)
# Roll up into the Tentpole row as "Total reach" + "Best-performing derivative"
```

### Recipe 10: Repurposing audit

```python
# Weekly: which derivative formats drive the most ROI?
formats = ["LinkedIn carousel", "X thread", "Reels", "TikTok", "Shorts", "Audiogram", "Blog", "Newsletter writeup", "Quote graphic", "LinkedIn long-form"]
for f in formats:
    rows = notion_query(NOTION_EDITORIAL_DB, filter={'Format': {'select': {'equals': f}}})
    reach = sum(r.get('KPI actual', 0) for r in rows)
    count = len(rows)
    avg_reach = reach / max(count, 1)
    hours_per = AVG_HOURS_PER_FORMAT[f]
    roi = avg_reach / hours_per
    print(f"{f}: avg reach {avg_reach:.0f}, ROI {roi:.0f} reach/hour")
```

Cut formats with bottom-quartile ROI; double down on top-quartile.

## Examples

### Example 1: Podcast Tuesday → 10+ derivatives Mon-Sun

**Goal:** Podcast publishes Tuesday morning; all 10+ derivatives queued and scheduled by Friday.

**Steps:**
1. Tuesday AM: tentpole publishes via RSS.
2. Tuesday AM: Recipe 5 runs (manual or scheduled) — Castmagic + OpusClip kick off.
3. Tuesday PM: Castmagic derivatives ready; OpusClip clips ready; Submagic polish queued.
4. Wednesday AM: Headliner audiogram auto-publishes per RSS autopilot.
5. Wednesday: queue all derivatives in Notion editorial DB per Recipe 4 schedule.
6. Wednesday: Recipe 8 schedules everything in Buffer + Typefully.
7. Mon next week: Recipe 9 + 10 pulls stats; identifies best-performing derivative; informs next episode planning.

**Result:** 1 tentpole → 12 derivatives across 6 platforms, scheduled across the week.

### Example 2: Newsletter → cross-platform burst on send day

**Goal:** Newsletter sends Tuesday 6am; LinkedIn carousel + X thread + IG carousel + blog post all live within 24h.

**Steps:**
1. Tuesday 6am: Newsletter sends.
2. Tuesday 8am: Recipe 2 runs — Castmagic on issue text, returns X thread + LinkedIn carousel outline + quotes.
3. Tuesday 9am: Postiv generates LinkedIn carousel from outline.
4. Tuesday 10am: Buffer schedules LinkedIn carousel for Tuesday 8pm.
5. Tuesday 11am: Typefully cascades X thread for Wednesday 10am across X + LinkedIn + Threads + Bluesky + Mastodon.
6. Tuesday 12pm: Blog post auto-publishes (same body, SEO restructured headers).
7. Wednesday: Reddit cross-post to r/<relevant>.

**Result:** Newsletter compounds across 6 platforms within 30h.

### Example 3: YouTube long-form → 12 derivatives in 48h

**Goal:** 14-min YouTube tutorial published Friday; all derivatives shipped by Sunday night.

**Steps:**
1. Friday AM: YouTube uploads via `youtube-mcp`.
2. Friday PM: OpusClip extracts 5 Shorts.
3. Saturday AM: Submagic polishes Shorts.
4. Saturday: Castmagic on audio → blog + newsletter + thread.
5. Saturday PM: Buffer schedules TikTok + Reels + LinkedIn video across Mon-Wed.
6. Sunday: Typefully cascades X thread for Mon 8am ET.
7. Sunday: Audiogram of audio-only excerpt for podcast feed.

**Result:** 14-min YouTube → 12 derivatives shipped + scheduled in 48h.

## Edge cases / gotchas

- **Castmagic + OpusClip overlap** — both can do captions; OpusClip is better for video, Castmagic for text. Don't double-process.
- **Submagic Business+ plan ($69/mo)** is required for API. Pro tier doesn't expose API.
- **Headliner has no public API.** Pro plan RSS autopilot is the workaround; you can't programmatically pull audiograms.
- **OpusClip "viral moment" detection is heuristic.** Always review picks — sometimes it grabs a flat moment because it has high audio energy.
- **Submagic auto-edit can cut mid-thought.** Use `remove_dead_air=true` for short-form (Reels), turn off for longer-form (5+ min videos).
- **Typefully cross-publish to LinkedIn collapses the thread** into a single long post. This is correct for LinkedIn audience but check the result before scheduling.
- **Buffer GraphQL is rate-limited** — 60 req/min. Bulk-schedule = chunk into batches with `sleep 1` between requests.
- **Don't ship all 10+ derivatives at once.** Stagger 1-2/day to avoid algo penalty for spammy mass-post.
- **Per-platform text variants matter** — LinkedIn audience is professional, TikTok is irreverent. Buffer cascade defaults to identical copy; pre-write per-platform variants for top 3 channels.
- **Sub-2% engagement on derivatives** = cut that format; the funnel isn't there.
- **Track best-performing derivative per tentpole** in Notion — informs next tentpole's repurposing priority.
- **Don't repurpose evergreen content into the same channel twice** — Reddit will ban for duplicate posts; LinkedIn will algorithm-suppress.

## Sources

- [Castmagic Stormy AI repurposing 2026](https://stormy.ai/blog/best-gpt-repurposing-tools-2026-opusclip-munch-castmagic)
- [Blotato — Best AI content repurposing tools 2026](https://www.blotato.com/blog/ai-content-repurposing-tools)
- [Submagic](https://www.submagic.co/)
- [OpusClip](https://www.opus.pro/)
- [Headliner](https://www.headliner.app/)
- [Typefully + agent CLI](https://typefully.com/x-twitter)
- [Buffer GraphQL + MCP](https://mcpmarket.com/server/buffer)
- [Castmagic API](https://docs.castmagic.io/)
