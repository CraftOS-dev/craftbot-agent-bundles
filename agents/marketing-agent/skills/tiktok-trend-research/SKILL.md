<!--
Source: TikTok Research API (https://developers.tiktok.com/products/research-api/)
Apify TikTok Trending Hashtags scraper: https://apify.com/clockworks/tiktok-trending
Phyllo Creator Economy API: https://www.getphyllo.com/
-->
# TikTok Trend Research — SKILL

TikTok's official Research API requires Developer Portal app approval (manual, 5-15 days). Until approved, Apify's `clockworks/tiktok-trending` actor and Phyllo's creator economy API provide immediate scraped data. The agent uses approved Research API where available; scraped fallback otherwise.

## When to use this skill

- **Trending sounds, hashtags, effects discovery** for content planning.
- **Hashtag mix** — trending + niche + branded for each post.
- **Creator research** — find micro-influencers in your vertical.
- **Competitor TikTok analysis** — top videos, posting cadence.
- **Sound trend cycle** — which sounds are rising / peaking / declining.

**Do NOT use this skill when:**
- **Publishing TikTok content** — use `tiktok-mcp` (publishing) or `buffer-cross-platform-publishing` (cascade).
- **TikTok Ads** — use `tiktok-ads-mcp`.

## Setup

### Option A: TikTok Research API (preferred)

```bash
# 1. Apply at https://developers.tiktok.com/products/research-api/
#    Requires: research purpose, university affiliation OR enterprise approval
# 2. Once approved, OAuth-based access

export TIKTOK_RESEARCH_TOKEN="<token>"
```

Endpoints:
- `/research/video/query/` — search videos by keyword/hashtag
- `/research/user/info/` — public profile data
- `/research/hashtag/info/` — hashtag volume + recent videos

### Option B: Apify TikTok Trending Hashtags (fallback)

```bash
# Apify account, then API token
export APIFY_TOKEN="<token>"

# Run actor
curl -X POST "https://api.apify.com/v2/acts/clockworks~tiktok-trending/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"region":"US","limit":50}'
```

Returns: trending hashtags + view counts + per-hashtag top videos.

### Option C: Phyllo creator API

```bash
# Phyllo for creator-level data
export PHYLLO_CLIENT_ID="<id>"
export PHYLLO_CLIENT_SECRET="<secret>"

# Search creators by topic
curl -X POST https://api.staging.getphyllo.com/v1/social/profiles/search \
  -H "Authorization: Basic <base64>" \
  -d '{"work_platform_id":"<tiktok-platform-id>","topic":["marketing"],"follower_count_min":10000,"follower_count_max":500000}'
```

## Common recipes

### Recipe 1: Trending hashtags daily snapshot

```bash
# Apify actor
curl -X POST "https://api.apify.com/v2/acts/clockworks~tiktok-trending/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -d '{"region":"US","limit":100}' \
| jq '.[] | {hashtag: .name, views: .view_count, video_count: .video_count, growth_rate: .growth_24h}'
```

Filter for relevant hashtags (overlap with brand keywords + emerging trends).

### Recipe 2: Hashtag mix strategy per post

Construct hashtag set per TikTok post:

```python
def hashtag_mix(brand_topic, trending_today):
    branded = ['#yourbrand']
    niche = [f'#{brand_topic}-tips', f'#{brand_topic}-hacks']
    trending = [h for h in trending_today if relevant_to(h, brand_topic)][:3]
    base = ['#fyp', '#foryoupage']
    return branded + niche + trending + base[:1]  # ~7 hashtags total
```

TikTok algorithm rewards 3-5 hashtags max — going overboard hurts reach.

### Recipe 3: Trending sounds research

Research API:

```bash
curl -X POST "https://open.tiktokapis.com/v2/research/video/query/" \
  -H "Authorization: Bearer $TIKTOK_RESEARCH_TOKEN" \
  -d '{
    "query": {
      "and": [
        {"operation":"IN","field_name":"region_code","field_values":["US"]},
        {"operation":"GTE","field_name":"create_date","field_values":["20260601"]}
      ]
    },
    "fields": ["music_id","music_title","music_author","view_count"],
    "max_count":100
  }'
```

Aggregate by `music_id`, count usage, sort by recent growth = trending sounds.

### Recipe 4: Competitor analysis

```bash
# Apify actor for competitor's videos
curl -X POST "https://api.apify.com/v2/acts/clockworks~tiktok-scraper/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -d '{
    "profiles":["competitor1","competitor2"],
    "resultsPerPage":50
  }'
```

Returns: posts + views + likes + comments. Analyze:
- Top-performing posts (study format, hook, sound)
- Posting cadence
- Hashtag patterns
- Engagement rate trends

### Recipe 5: Creator discovery for influencer program

Phyllo search:

```bash
curl -X POST https://api.staging.getphyllo.com/v1/social/profiles/search \
  -H "Authorization: Basic <auth>" \
  -d '{
    "work_platform_id":"<tiktok-id>",
    "topic":["marketing","saas"],
    "follower_count_min":10000,
    "follower_count_max":250000,
    "engagement_rate_min":0.04,
    "country":["US","CA","UK"],
    "language":"en"
  }'
```

Filter to:
- Engagement rate > 4% (industry baseline ~2%)
- Follower count 10K-250K (sweet spot for B2B)
- Recent posting (last 7 days)

Pipe to Notion CRM for outreach.

### Recipe 6: Hashtag overlap with branded content

```python
# Check which hashtags drove the most views on your own TikTok
own_posts = apify.scrape('@yourbrand', limit=100)
hashtag_perf = {}
for post in own_posts:
    for tag in post['hashtags']:
        hashtag_perf.setdefault(tag, []).append(post['views'])

# Avg views per hashtag
ranked = sorted(hashtag_perf.items(), key=lambda x: -sum(x[1])/len(x[1]))[:20]
```

Top performing = your "branded niche" hashtags to use consistently.

### Recipe 7: Sound trend cycle prediction

```python
# Track sound usage week-over-week
weeks = ['2026-W22','2026-W23','2026-W24']
sound_id = '<id>'
counts = []
for week in weeks:
    res = tiktok_research.query_videos(music_id=sound_id, create_date_week=week)
    counts.append(res['video_count'])

# Growth: if count[2] / count[1] > 1.5 = rising; if < 0.7 = declining
if counts[2] / counts[1] > 1.5: print('Rising — use now')
elif counts[2] / counts[1] < 0.7: print('Declining — skip')
else: print('Peaked — use cautiously')
```

Catch rising sounds early; they peak fast then drop.

## Examples — weekly TikTok content plan

```yaml
weekly_research:
  monday:
    - pull trending hashtags (Apify)
    - filter to brand-relevant (manual review)
    - pull trending sounds (Research API)
    - identify 2-3 sounds in "rising" phase
  tuesday-wednesday:
    - record 3-5 videos using rising sound + branded narrative
  thursday-friday:
    - publish via tiktok-mcp or Buffer
    - hashtag mix: 1 branded + 2 niche + 2 trending + #fyp
  weekend:
    - analyze previous week's performance
    - double down on top-3 patterns next week
```

## Edge cases

### Research API approval
- Approval rate: ~50% for first-time applicants
- Approval favors: academic / nonprofit / large-enterprise use cases
- Approval rejects: marketing automation / influencer brokerage explicit purpose

If rejected, Apify + Phyllo cover ~85% of needs.

### Apify rate limits / cost
- Apify free tier: $5 credit/mo
- Trending actor: ~$0.01-0.05 per run
- Scraping single profile: ~$0.10
- 200 profile scrapes/day = ~$20/day = $600/mo

Set budget alerts.

### Region-specific trends
TikTok trends differ wildly by region (US vs UK vs ID vs BR). Always query per target region. Brand may need separate strategy per market.

### Hashtag saturation
A hashtag at 1B+ views = saturated, your video lost in noise. Sweet spot: 1M-50M views per hashtag — relevant but not commodity.

### Trending sound copyright
Commercial accounts can only use sounds from TikTok's Commercial Music Library. Trending pop songs are typically NOT in CML — using them risks audio-mute on commercial videos.

Workaround: use original audio + viral concept structure, skip the literal sound.

### Algorithm changes
TikTok's algorithm evolves quarterly. Patterns that worked Q1 may not Q3. Don't over-fit to past performance.

### Engagement rate calculation
- Phyllo / Apify report different ER formulas
- Standard: (likes + comments + shares) / followers × 100
- TikTok-native: (likes + comments + shares + saves) / views × 100

Use TikTok-native for content quality assessment; standard for cross-platform comparison.

### Niche hashtags > generic
Generic (`#marketing`, `#business`) get lost. Niche (`#saasstartup`, `#growthhacks`) reach actual target audience even if smaller volume.

### Trending vs evergreen
70% of TikTok strategy should be evergreen (your brand's POV / tutorial / story). 30% trending injection (rising sounds, formats, jokes). Pure trend-chasing wears out and dilutes brand voice.

## Sources

- **TikTok Research API**: https://developers.tiktok.com/products/research-api/
- **Apify TikTok Trending actor**: https://apify.com/clockworks/tiktok-trending
- **Apify TikTok Scraper**: https://apify.com/clockworks/tiktok-scraper
- **Phyllo creator API**: https://www.getphyllo.com/
- **TikTok Commercial Music Library**: https://www.tiktok.com/business/library/CML.html
- **Algorithm overview**: https://newsroom.tiktok.com/en-us/how-tiktok-recommends-content
