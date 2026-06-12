<!--
Source: https://buffer.com/developers/api
Vale: https://vale.sh/
Platform char limits and format specs: role.md "Platform format spec"
-->
# Platform-Native Content Creation — SKILL

One brief → fan out to platform-native variants. Each channel gets its own copy, hashtag basket, media variant, posting time. This skill is the orchestrator that calls `buffer-cross-platform-publishing` (cascade), `brand-voice-consistency-platforms` (Vale lint per channel), `hashtag-strategy-trending-niche-branded` (per-platform basket), and `format-specific-reels-tiktok-shorts-x-thread` (format primitives).

## When to use this skill

- **One topic → multiple platforms** with content that doesn't read as copy-paste.
- **Editorial calendar fill** for a week or campaign.
- **Repurposing flagship content** — blog → LinkedIn post + X thread + IG carousel + TikTok + Threads.
- **Pre-publish QA** — Vale per platform, character-limit checks, image-spec validation.

**Do NOT use this skill when:**
- A single-channel ad-hoc post — call native MCP directly.
- The piece is video-first long-form — hand to `video-creator`.
- Pure trend-jacking on TikTok — use `social-trend-monitoring-tiktok-sounds-reels` directly.

## Setup

### Per-platform style packs (Vale)

See `brand-voice-consistency-platforms` skill. Required files:

```
styles/Brand/
├── LinkedIn.yml
├── X.yml
├── TikTok.yml
├── Threads.yml
├── Instagram.yml
├── Reddit.yml
├── Bluesky.yml
└── Common.yml
.vale.ini
```

### Notion editorial calendar DB

Columns: `Topic / Brief / Channels (multi-select) / Hero asset URL / Variants (per-channel rich-text) / Scheduled at / Vale status / Approval status (draft/review/approved) / Buffer update ID / Published URLs / Performance`.

### Buffer channel mapping

```bash
mcp tool buffer.list_channels > .buffer-channels.json
```

## Common recipes

### Recipe 1: Brief → variants generation

Given a topic brief, produce per-platform copy:

```python
TOPIC = "We just launched X — solves problem Y for audience Z"
PLATFORMS = ['linkedin', 'x', 'instagram', 'tiktok', 'threads', 'bluesky', 'reddit']

variants = {}
for p in PLATFORMS:
    variants[p] = generate_platform_copy(TOPIC, platform=p, voice='styles/Brand/'+p.title()+'.yml')

# Each variant respects platform format spec (role.md "Platform format spec")
# linkedin: 1300-1900 chars, hook in first 210, 3-5 hashtags
# x: 280 chars, 1-2 hashtags, hook in first 7 words
# instagram: 138-150 chars first chunk, 20-30 hashtags in first comment
# tiktok: 100-150 char caption keyword-front-loaded, 3-5 hashtags (no #fyp)
# threads: 500 chars, conversational, 0-3 hashtags
# bluesky: 300 chars, tech-savvy tone
# reddit: choose subreddit; title 300 chars keyword-front-loaded
```

### Recipe 2: Hashtag baskets per platform

Pull from `hashtag-strategy-trending-niche-branded`:

```python
from hashtag_strategy import build_basket

baskets = {
    'instagram': build_basket(topic=TOPIC, platform='instagram', count=25),  # 5T + 15N + 5B
    'tiktok':    build_basket(topic=TOPIC, platform='tiktok',    count=4),   # 1T + 2N + 1B
    'linkedin':  build_basket(topic=TOPIC, platform='linkedin',  count=4),
    'x':         build_basket(topic=TOPIC, platform='x',         count=2),
    'threads':   build_basket(topic=TOPIC, platform='threads',   count=2),
    'bluesky':   build_basket(topic=TOPIC, platform='bluesky',   count=2),
}
```

### Recipe 3: Media variants

Each format needs its own media:

| Channel | Aspect | Spec |
|---|---|---|
| LinkedIn feed image | 1.91:1 | 1200x627 |
| LinkedIn carousel doc | 1:1 or 4:5 | PDF up to 100 pages |
| X image | 16:9 | 1200x675 |
| Instagram feed | 1:1 or 4:5 | 1080x1080 / 1080x1350 |
| Instagram Reel | 9:16 | 1080x1920 |
| TikTok | 9:16 | 1080x1920 |
| YouTube Shorts | 9:16 | 1080x1920 |
| Pinterest pin | 2:3 | 1000x1500 |
| Threads | 1:1 or 16:9 | 1080x1080+ |

Use `canva-mcp` or `figma-mcp` to pull templates; `imagegen-mcp` for AI-gen.

### Recipe 4: Vale lint per variant

```bash
for platform in linkedin x instagram tiktok threads bluesky reddit; do
  echo "$variants[$platform]" > /tmp/variant-$platform.md
  uvx vale --config=.vale.ini \
    --output=JSON \
    --filter='.Level=="error"' \
    /tmp/variant-$platform.md > /tmp/vale-$platform.json
done

# Block publish if any errors
for f in /tmp/vale-*.json; do
  if [ "$(jq 'map(length) | add' $f)" != "0" ]; then
    echo "Vale errors in $f — revise before publishing"
    exit 1
  fi
done
```

### Recipe 5: Length + spec validation

```python
SPECS = {
    'linkedin': {'max_chars': 3000, 'recommended': (1300, 1900), 'first_line_hook': 210},
    'x': {'max_chars': 280, 'first_line_hook': 50},  # Premium 25k but algorithm prefers <280
    'instagram': {'max_chars': 2200, 'first_visible': 138, 'hashtag_count': (20, 30)},
    'tiktok': {'max_chars': 2200, 'recommended': (100, 150), 'hashtag_count': (3, 5)},
    'threads': {'max_chars': 500, 'hashtag_count': (0, 3)},
    'bluesky': {'max_chars': 300, 'hashtag_count': (0, 3)},
    'reddit': {'title_max': 300, 'body_max': 40000},
}

def validate(variant, platform):
    spec = SPECS[platform]
    errors = []
    if len(variant['text']) > spec['max_chars']:
        errors.append(f"Over {spec['max_chars']} chars")
    if 'first_visible' in spec and len(variant['hook_line']) > spec['first_visible']:
        errors.append(f"Hook line too long for above-fold visibility")
    if 'hashtag_count' in spec:
        lo, hi = spec['hashtag_count']
        actual = variant['text'].count('#')
        if not (lo <= actual <= hi):
            errors.append(f"Hashtag count {actual} outside {lo}-{hi}")
    return errors
```

### Recipe 6: Schedule cascade via Buffer

```bash
mcp tool buffer.create_update \
  --channelIds '["linkedin_company","twitter","instagram","tiktok","threads","bluesky"]' \
  --text "$DEFAULT_TEXT" \
  --channelData "$(jq -n --argjson v "$VARIANTS_JSON" '$v')" \
  --mediaUrls "$(jq -n --argjson m "$MEDIA_PER_CHANNEL" '$m')" \
  --scheduledAt "2026-06-14T14:00:00Z"
```

Per-platform optimal posting times (from role.md "Platform format spec"):
- LinkedIn: Tue-Thu 8-10am or 12-1pm local
- X: weekday 9am or 1-3pm
- IG: weekday 11am-1pm or 7-9pm
- TikTok: Tue-Thu 6-10am or 7-11pm
- Threads: less time-bound; rhythm > time-of-day
- Reddit: 8-10am ET weekdays for /r/business; per-sub varies

### Recipe 7: A/B variant testing

```python
# Two variants per channel; ship A first, ship B 4 hrs later
# Track engagement per via Buffer analytics; pick winning template for next round
for ch in channels:
    a, b = generate_variant_pair(topic, ch)
    schedule_a = buffer.create_update(channelIds=[ch], text=a, scheduledAt=base_time)
    schedule_b = buffer.create_update(channelIds=[ch], text=b, scheduledAt=base_time + 4h)
    notion.create_row(ab_test_db, {'channel':ch, 'var_a_id':schedule_a['id'], 'var_b_id':schedule_b['id']})
```

### Recipe 8: Cross-platform UTM convention

```python
# Inherit from marketing-agent's bitly-utm-campaign-tracking skill
UTM = "?utm_source={platform}&utm_medium=social&utm_campaign={campaign}&utm_content={asset_id}"
for ch, text in variants.items():
    if '{LINK}' in text:
        variants[ch] = text.replace('{LINK}', BRAND_LINK + UTM.format(platform=ch, campaign='spring26', asset_id='A1'))
```

## Examples

### Example A: Blog post → 6-platform fan-out

Source: 1500-word blog "5 lessons from scaling X".

```yaml
fan_out:
  linkedin_company:
    text: |
      5 lessons from scaling X to $1M ARR ↓
      
      (1) {lesson 1 with anecdote}
      (2) {lesson 2}
      ...
      
      Full write-up: {bitly-link}
      
      What's #6 from your experience?
    hashtags: ['#saas', '#growth', '#startups']
  x:
    text: |
      5 lessons from scaling to $1M ARR:
      
      1/ {one-liner}
      2/ {one-liner}
      3/ {one-liner}
      4/ {one-liner}
      5/ {one-liner}
      
      Full thread + write-up ↓ {link}
  instagram:
    format: carousel
    cards: 6   # 1 cover + 5 lesson cards
    caption: |
      5 lessons from going $0 → $1M ARR. Swipe →
      Tap the link in bio for the full breakdown.
    hashtags: [25-tag basket]
  tiktok:
    format: video
    hook_line: "What 5 things would I tell past-me about scaling SaaS?"
    on_screen_text: |
      Lesson 1: {one-liner}
      Lesson 2: {one-liner}
      ...
    caption: "5 lessons from scaling SaaS to $1M ARR"
    hashtags: ['#saas', '#startup', '#founderlife', '#brandX']
  threads:
    text: |
      5 lessons from $0 → $1M ARR. The one nobody talks about:
      
      {one specific lesson + story}
      
      Threads: write the unfiltered backstory of one lesson per day this week.
  bluesky:
    text: "$0 → $1M ARR. 5 lessons. Tldr: <one line>. Full notes: {link}"
```

### Example B: Approval flow integration

```python
# Draft + variants ready → Notion status = 'review'
# Approver clicks Slack button to mark 'approved'
# Webhook triggers Buffer create_update with needsApproval=false
slack.send_interactive('#social-review', message_card_with_buttons(variants, approve_url, reject_url))
```

## Edge cases

### Repurposing tone drift
LinkedIn corporate-formal → TikTok casual: don't translate the LinkedIn post verbatim. Re-write from scratch in target voice. Vale per platform catches drift.

### Hero asset vs platform asset
Single 16:9 hero doesn't work on 9:16 TikTok / Reels. Crop / re-shoot. `canva-mcp` template flow: hero asset → 5 platform-specific variants.

### URL preview cards
LinkedIn / Threads render Open Graph preview if URL is in body. X renders only if no media attached. For X, post link in a follow-up reply to avoid card-strip.

### Mention etiquette per platform
LinkedIn: tag 1-3 people maximum, only when relevant. X: tag conversationally. IG: tag sparingly in caption, more freely in image-tags. Spam-tagging gets accounts flagged.

### Emoji density per platform
LinkedIn 1-3 / X 1-2 / TikTok 3-5 / Threads 2-4 / IG 2-4 / Reddit 0. Enforced via Vale `Brand/<Platform>.yml`.

### Character-count truncation
Buffer respects per-platform limits; truncates silently if `channelData[platform].text` exceeds. Always validate before send (Recipe 5).

### Reddit per-subreddit rules
Subreddits enforce flair / title format / posting frequency. Always read `r/<sub>/wiki/rules` first. See `reddit-strategy-ama-subreddit`.

### Different platforms, different ideal posting times
A single 2pm cascade is sub-optimal. Use Buffer per-channel schedule (Recipe 6) staggered to each platform's best window.

### Media-spec mismatch
Buffer accepts media but doesn't auto-resize. If asset is 1080x1080 and channel needs 1080x1920, image will be cropped/letterboxed by platform. Pre-resize via `canva-mcp` / `imagegen-mcp` / sharp CLI.

### Threads + Bluesky reach asymmetry
Threads + Bluesky reach is smaller; don't over-invest variant effort. Use a 1-line distilled version; Threads loves conversation, Bluesky loves links.

### Vale false positives on platform-specific slang
TikTok variants might use "no cap" / "lowkey" / etc. — keep TikTok-specific vocab allowed in `styles/Brand/TikTok.yml` vocab list.

### Approval lag
If approval gate adds > 2 hr lag, primary posting windows drift. Either pre-build approvals into editorial calendar 24-48 hr ahead, OR fast-track with predefined templates.

## Sources

- **Buffer Developers API**: https://buffer.com/developers/api
- **Vale prose linter**: https://vale.sh/
- **Platform format specs**: role.md "Platform format spec" section
- **Buffer — best social media APIs**: https://buffer.com/resources/best-social-media-apis/
- **Sprout Social — best practices**: https://sproutsocial.com/insights/social-media-best-practices/
- **LinkedIn Marketing API (carousel doc post)**: https://learn.microsoft.com/en-us/linkedin/marketing/
- **Instagram Graph API**: https://developers.facebook.com/docs/instagram-platform/
