<!--
Source: https://www.tiktok.com/business/creativecenter
Tokchart: https://tokchart.com/
Buffer trending sounds: https://buffer.com/resources/trending-songs-tiktok/
48-hour adoption window: role.md "Trend monitoring playbook"
-->
# Social Trend Monitoring — TikTok Sounds + Reels + X Discourse — SKILL

Daily snapshot of accelerating sounds, hashtags, and formats. TikTok Creative Center (top 20 sounds + hashtags + creators by region). Tokchart for daily chart with delta. Buffer's weekly curated trending list as cross-check. 48-hour adoption window for 3-5x algorithmic push. Output: `3 accelerating / 3 declining / 1 unusual` per day with ship-by deadlines.

## When to use this skill

- **Daily 9am trend brief** — what to ship in next 48 hrs.
- **Trend opportunism** — when a sound matches brand voice + audience.
- **Format opportunism** — new TikTok format / Reel transition / Threads conversation pattern.
- **Tracking trend decay** — when a sound is past peak (skip).
- **Weekly trend retrospective** — what worked, what we missed.

**Do NOT use this skill when:**
- Branded hashtag tracking — `hashtag-strategy-trending-niche-branded` + Brand24.
- Crisis monitoring (negative trends) — `social-listening-brandwatch-mention-talkwalker` + `social-crisis-comms`.

## Setup

### TikTok Creative Center (public, no auth)

```bash
# Trending sounds endpoint (public dashboard scraping)
BASE="https://ads.tiktok.com/business/creativecenter/inspiration/popular"
curl -s "$BASE/music/pc/en?region=US&period=7" -H "User-Agent: Mozilla/5.0"

# Or via Apify
curl -X POST "https://api.apify.com/v2/acts/clockworks~tiktok-trending/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -d '{"region":"US","limit":100,"section":"music"}'
```

### Tokchart (daily trending songs, free + paid)

```bash
# Tokchart public endpoint
curl -s "https://tokchart.com/api/trending?country=US&date=$(date +%Y-%m-%d)"
```

### Buffer trending sounds (curated)

```bash
# Buffer publishes a weekly trending-sounds list (no API, scraped weekly)
curl -s "https://buffer.com/resources/trending-songs-tiktok/" \
  | python extract_weekly_list.py
```

### Brave Search / Firecrawl fallback

```bash
mcp tool brave_search.search --query "trending TikTok sounds week of $(date +%Y-%m-%d)" --count 10
```

### Notion Trend DB

Columns: `Sound name / TikTok sound ID / Hashtag / First seen / Use count today / Use count yesterday / Delta % / Phase (rising/peak/declining) / Brand fit (1-10) / Ship-by deadline / Adopted? (yes/no) / Adopted post URL / Performance lift`.

## Common recipes

### Recipe 1: Daily 9am cron — pull top 20 sounds

```bash
#!/bin/bash
# Top 20 sounds, last 7 days, US region
mcp tool brave_search.search --query "site:tiktok.com/business/creativecenter inspiration popular music" --count 5

# Or scrape directly
curl -s "$TIKTOK_CC_BASE/music/pc/en?region=US&period=7" \
  | python parse_tiktok_cc.py > /tmp/tiktok-sounds-today.json

# Tokchart cross-check
curl -s "https://tokchart.com/api/trending?country=US" > /tmp/tokchart-today.json
```

### Recipe 2: Delta calculation (today vs yesterday)

```python
import json
today = json.load(open('/tmp/tiktok-sounds-today.json'))
yesterday = json.load(open('/tmp/tiktok-sounds-yesterday.json'))

deltas = []
y_map = {s['sound_id']: s['use_count'] for s in yesterday}
for s in today:
    y = y_map.get(s['sound_id'], 0)
    delta_pct = ((s['use_count'] - y) / max(y, 1)) * 100
    s['delta_pct'] = delta_pct
    s['phase'] = phase_from_delta(s['use_count'], delta_pct)
    deltas.append(s)

# Phase logic per role.md "Trending audio 48-hour rule":
# rising  → use_count < 100k AND delta > 30%
# peak    → use_count 100k-500k AND delta 5-30%
# decline → use_count > 500k AND delta < 5%
```

### Recipe 3: Brand-fit scoring

```python
def brand_fit_score(sound, brand_voice):
    # Genre / tone / lyric matching
    genre_match = 1 if sound['genre'] in brand_voice['acceptable_genres'] else 0
    tone_match = compute_tone_similarity(sound['vibe_tags'], brand_voice['tone_tags'])
    lyric_safe = 0 if any(b in sound.get('lyrics','').lower() for b in BANNED_TERMS) else 1
    return (genre_match * 4 + tone_match * 5 + lyric_safe * 1)

for s in deltas:
    s['brand_fit'] = brand_fit_score(s, BRAND_VOICE)
```

### Recipe 4: Daily trend brief output

```python
BRIEF_TEMPLATE = """
# Trend Brief — {date}

## Top accelerating (3)
{accelerating}

## Declining (3) — avoid late adoption
{declining}

## Unusual / Watch (1)
{unusual}

## Recommended actions
{actions}
"""

accelerating = [s for s in deltas if s['phase']=='rising' and s['brand_fit'] >= 6]
declining   = [s for s in deltas if s['phase']=='decline'][:3]
unusual     = pick_unusual(deltas)
actions     = [{
    'sound_id': s['sound_id'],
    'ship_by': now + timedelta(hours=48),
    'hook_idea': suggest_hook(s, BRAND_TOPIC),
} for s in accelerating[:3]]

brief = BRIEF_TEMPLATE.format(date=today, accelerating=fmt(accelerating[:3]),
                              declining=fmt(declining), unusual=fmt(unusual), actions=fmt(actions))
slack.post('#social-trends', brief)
notion.create_page(trend_brief_db, {'Date': today, 'Brief': brief})
```

### Recipe 5: 48-hour ship-by tracking

```python
# Each adopted trend has a 48-hr clock; if not shipped, flag
for trend in notion.query(trend_db, filter={'Ship-by deadline__lte': now + 12h, 'Adopted?': 'no'}):
    slack.post('#social-trends',
        f"⏰ 12 hrs left: '{trend['Sound name']}' — ship-by {trend['Ship-by deadline']} or skip")
```

### Recipe 6: Reels trends (cross-platform overlap)

TikTok sounds spill to Reels with 1-3 day lag. Track both:

```python
# IG Reels trending audio via Meta Graph (limited data, mostly internal IG dashboards)
# Fallback: scrape IG explore Reels via brightdata-mcp
mcp tool brightdata.scrape --url "https://www.instagram.com/explore/reels/" \
  --selector "audio_used" --limit 50
```

### Recipe 7: X discourse trends (different mechanic)

X trends = topical, not sonic.

```bash
# X API trending topics endpoint
curl -G "https://api.twitter.com/2/trends/by/woeid/2459115" \
  -H "Authorization: Bearer $X_BEARER_TOKEN"
# 2459115 = NYC; other WOEIDs for other regions

# Or Brandwatch / Trends24
curl -s "https://trends24.in/united-states/"
```

Filter relevance, brand-safety. X trends spike + decay in hours; ship within 1-3 hrs of detection or skip.

### Recipe 8: Reddit discourse trends

```bash
# Pull r/all top from last 6 hrs as discourse pulse
mcp tool reddit.get_subreddit_top --subreddit "all" --time "hour" --limit 50
# Filter to niche-relevant subs
mcp tool reddit.get_subreddit_top --subreddit "marketing" --time "day" --limit 25
```

### Recipe 9: Hook suggestion from sound metadata

```python
def suggest_hook(sound, brand_topic):
    if sound['format_archetype'] == 'pov':
        return f"POV: you're the founder of a {brand_topic} startup at 11pm"
    if sound['format_archetype'] == 'before_after':
        return f"My {brand_topic} workflow before vs after"
    if sound['format_archetype'] == 'tutorial':
        return f"How I {brand_topic_verb} in 60 seconds"
    return f"{brand_topic_one_liner} (using trending sound)"
```

### Recipe 10: Trend adoption performance lift measurement

```python
# 7 days after adoption, compare reach vs baseline
baseline_reach = avg(p['reach'] for p in last_30_posts() if not p['used_trending_sound'])
adopted_reach  = adopted_post['reach']
lift = (adopted_reach / baseline_reach) - 1
notion.update_page(trend['id'], {'Performance lift': f"{lift*100:+.0f}%"})
```

## Examples

### Example A: Tuesday morning trend brief

```
Trend Brief — 2026-06-11

## Top accelerating (3)
1. "Glimpse of Us" remix v3 (id 7287654321) — Source: TikTok CC — Delta: +42% — Brand fit: 7/10 — Ship-by: 2026-06-13 09:00 UTC — Hook: "POV: your tab count after launch week"
2. #MorningRoutineDecoded — Delta: +35% — Brand fit: 8/10 — Ship-by: 2026-06-13 09:00 UTC — Hook: "My founder morning vs my "post-Series-A" morning"
3. "Carrying That Weight" snippet — Delta: +28% — Brand fit: 6/10 — Ship-by: 2026-06-13 09:00 UTC — Hook: "Three tasks I should've delegated yesterday"

## Declining (3)
- "Aesthetic Coffee Shop" (peaked Sat) — skip
- #ItsGirlMath (now overused) — skip
- "Ratatouille Remix" (post-peak) — skip

## Unusual / Watch (1)
- Niche-format growth in /r/Entrepreneur: "screenshot dump" posts gaining traction — watch for cross-platform spillover

## Recommended actions
- Brief @creator-A for "Glimpse of Us" workflow video by EOD Tue
- Schedule #MorningRoutineDecoded brand TikTok for Wed 7am ET
```

### Example B: Weekly trend retrospective

```python
# Sunday review
trends_adopted_this_week = notion.query(trend_db, filter={'Adopted?': 'yes', 'Date__gte': week_start})
total_lift = sum(t['Performance lift'] for t in trends_adopted_this_week)
slack.post('#social-trends',
    f"Weekly trend retro: adopted {len(trends_adopted_this_week)}, avg lift {total_lift/len(trends_adopted_this_week)*100:.0f}%. "
    f"Top performer: {max(trends_adopted_this_week, key=lambda t: t['Performance lift'])}")
```

### Example C: Trend miss audit

```python
# Of accelerating trends from 2 weeks ago, which ones did our competitors adopt that we missed?
two_wks_ago_trends = notion.query(trend_db, filter={'Date': two_wks_ago, 'Phase':'rising'})
for t in two_wks_ago_trends:
    if not t['Adopted?']:
        # Search competitor posts for the sound
        comp_uses = scrape_competitor_uses(sound_id=t['Sound ID'], competitor_handles=COMPETITORS)
        if comp_uses:
            notion.update_page(t['id'], {'Notes': f"Missed: competitors {comp_uses} adopted"})
```

## Edge cases

### TikTok Creative Center region locking
Different regions show different trends. Always specify `region=US` (or target). For multi-market brand, run per-region cron.

### Sound copyright (commercial use)
Most pop / hit songs are NOT in TikTok Commercial Music Library. If posting as Business account, sound auto-mutes. Workaround: use original audio + viral concept structure ("audio sponsor with original sound matching viral format").

### Buffer's weekly list lag
Buffer aggregates Sun-Sat; published Tue. May be 3-4 days stale by adoption window standards. Use as cross-check, not primary signal.

### Tokchart API availability
Tokchart has free public chart + paid API. Free has rate limits (100 req/day). Paid $19/mo for higher cap.

### Apify cost at scale
Apify charges per actor run. Daily TikTok-trending pull: ~$0.10-0.50/day. Budget alert at 80%.

### Brand-fit override
A trending sound with low brand fit can still work if the concept is genuinely funny / on-brand. Don't be rigid; flag for human review when fit-score 4-6.

### Trend exhaustion
Same brand riding trend after trend dilutes voice. Cap: 30% of weekly posts as trend-adoption, 70% evergreen brand-voice.

### Algorithm seasonality
December / January trends differ from summer. New Year cleanse / resolution trends spike Q1; summer travel / beach trends Q3. Adjust brand-fit list seasonally.

### Late adoption penalty
Posting a trend at peak hurts reach worse than not posting at all (looks dated, low-effort). Be ruthless about 48-hr window.

### Format archetype mapping
Sounds have implicit format archetypes (POV / before-after / day-in-life / tutorial / reaction). Match hook to archetype; otherwise the sound feels random.

### Cross-platform timing
TikTok → Reels: 1-3 day lag. TikTok → YouTube Shorts: 2-5 day lag. Post on TikTok first, then re-cut for Reels/Shorts 2 days later.

### Niche trends within niches
Within /r/Programming, a meme format trends differently from /r/Entrepreneur. Recipe 8 handles surface; deeper nesting requires monitoring 5-10 target subs daily.

### Bilibili / Douyin / Xiaohongshu trends
APAC trends are separate ecosystem. Use `bilibili-mcp` + `brightdata-mcp` for Xiaohongshu scraping. Don't assume Western trend signals translate.

### Influencer-driven trend
Some sounds blow up because one mega-creator used them; brand riding the same sound 24 hrs later may look derivative. Check sound's seed-user; if it's a single creator's signature, avoid.

## Sources

- **TikTok Creative Center**: https://www.tiktok.com/business/creativecenter
- **TikTok CC popular music**: https://www.tiktok.com/business/creativecenter/inspiration/popular/music
- **Tokchart**: https://tokchart.com/
- **Buffer trending TikTok sounds**: https://buffer.com/resources/trending-songs-tiktok/
- **Apify TikTok Trending actor**: https://apify.com/clockworks/tiktok-trending
- **48-hour trend adoption window**: https://www.gpt.social/blog/how-to-find-trending-sounds-tiktok-reels-2026
- **X trends by WOEID**: https://docs.x.com/x-api/trends/
- **Trends24**: https://trends24.in/
- **TikTok Commercial Music Library**: https://www.tiktok.com/business/library/CML.html
