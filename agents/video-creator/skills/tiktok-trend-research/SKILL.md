# TikTok Trend Research

## When to use
- Identify trending hashtags / sounds in a region
- Pull top-performing videos for a niche to mine hook patterns
- Analyze "Hook in 3 seconds" patterns from successful posts
- Find micro/nano creators in a niche for partnership outreach

## Auth landscape (June 2026)

| Source | Status | Cost | Notes |
|---|---|---|---|
| TikTok Research API (official) | Requires Developer Portal app approval | Free | 5–10 business days for approval; academic + commercial use |
| TikTok Commercial Content API | Requires brand account | Free | For ads creative search |
| Apify TikTok Trending Hashtags Scraper | Public scraper, paid | ~$30/mo (50K results) | Fallback while official auth pending |
| Phyllo | Enterprise contract | Quote-based | Creator analytics + audience demo |
| RapidAPI TikTok endpoints | Various community wrappers | $5–$50/mo | Quality varies |

## Setup
- `tiktok-mcp` (already wired in `agent.yaml`) — primary
- `cli-anything` for Apify / RapidAPI fallback

## Common recipes

### 1. TikTok Research API — query videos by hashtag
```bash
curl -X POST "https://open.tiktokapis.com/v2/research/video/query/" \
  -H "Authorization: Bearer $TIKTOK_RESEARCH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "and": [{"operation":"IN","field_name":"hashtag_name","field_values":["fitness","gym"]}]
    },
    "max_count": 50,
    "start_date": "20260501",
    "end_date": "20260530",
    "fields": "id,create_time,username,video_description,view_count,like_count,share_count,hashtag_names,music_id,duration"
  }'
```

### 2. Apify fallback — trending hashtags
```bash
curl -X POST "https://api.apify.com/v2/acts/clockworks~tiktok-trending-hashtags-scraper/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"countryCode":"us","limit":50}'
```
Returns list of `{ hashtag, video_views, posts_count }`.

### 3. Apify — videos by hashtag
```bash
curl -X POST "https://api.apify.com/v2/acts/clockworks~tiktok-scraper/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -d '{
    "hashtags": ["fitness"],
    "resultsPerPage": 50,
    "shouldDownloadVideos": false,
    "shouldDownloadCovers": false
  }'
```

### 4. Hook-in-3 analysis pipeline
```python
# Pseudocode
videos = research_api.query_top(hashtag="fitness", limit=50, min_views=1_000_000)
for v in videos:
    # Download video (research API provides download URL for approved apps)
    # Extract first 3 seconds
    # Whisper.cpp transcribe first 3s
    # Classify hook: question / claim / visual / sonic
hooks = cluster_hooks(videos)
# Output: "82% of top fitness videos use a 'shocking claim' hook in seconds 0-2"
```

### 5. Trending sound discovery
TikTok Commercial Content API:
```bash
curl -X POST "https://open.tiktokapis.com/v2/research/commercial_content/library/" \
  -H "Authorization: Bearer $TIKTOK_RESEARCH_TOKEN" \
  -d '{"query":{"and":[{"operation":"EQ","field_name":"country_code","field_values":["US"]}]},"max_count":100}'
```

### 6. Phyllo creator analytics (enterprise)
```bash
curl -X POST "https://api.staging.getphyllo.com/v1/social/profiles" \
  -H "Authorization: Basic $PHYLLO_BASIC_AUTH" \
  -d '{"work_platform_id":"...","identifier":"creator_handle"}'
```
Returns audience demos, engagement rates, brand-safety flags.

### 7. Daily-trending-hashtags polling loop
```bash
# Cron: daily 8am UTC
HASHTAGS=$(curl -X POST ".../tiktok-trending-hashtags-scraper" -d '{"countryCode":"us","limit":20}' --token $APIFY_TOKEN)
echo $HASHTAGS | jq -r '.[] | "\(.hashtag): \(.video_views)"' > daily-trends.log
```

### 8. Niche-vs-trending hashtag mix (5–8 total per role.md)
For each upload: 2 trending (broad reach) + 3 niche (target audience) + 1 branded (yours). Trending pulled from Apify daily-trends; niche from internal whitelist.

### 9. Creator partnership tier filter
```python
nano   = creators_with(followers_between=(1_000, 10_000))
micro  = creators_with(followers_between=(10_000, 100_000))
mid    = creators_with(followers_between=(100_000, 1_000_000))
macro  = creators_with(followers__gt=1_000_000)
```
Engagement rate (Phyllo) typically inverse to follower count — nano/micro often >5%, macro often <2%.

### 10. Content pillar (40/30/20/10) audit
Pull last 50 own uploads via `tiktok-mcp` → classify each as educational/entertainment/inspirational/promotional → compare to 40/30/20/10 mix → flag gaps.

### 11. Optimal post time analysis
Pull own analytics → bin engagement by hour → identify top-3 windows. TikTok Research API exposes `view_count` per video + `create_time` for own posts via Display API.

### 12. Sound trajectory analysis
A trending sound's lifecycle is 5–10 days. Catching it on day 2–4 maximizes reach. Daily-trend snapshot → diff yesterday vs today → identify sounds rising.

### 13. Brand-safety filter (avoid problematic hashtags)
Phyllo content-safety + maintain internal blocklist of categories (gambling, alcohol, political, controversial topics) for brand campaigns.

### 14. Competitor uploads tracker
Apify's `tiktok-scraper` with `profiles: ["@competitor"]` pulls their last N uploads with view counts.

### 15. Cross-platform sound check
If a TikTok sound is also licensed on Spotify (most are), confirm before reusing on YouTube Shorts / Reels — copyright claim risk.

## Examples

### A. "What hooks are working in fitness right now?"
1. Apify trending-hashtags US → identify `#75hard #pushup #miketyson` as top.
2. Apify tiktok-scraper for each → top 30 videos per tag.
3. Pull captions / first-3s transcripts via Whisper.cpp.
4. Cluster: "shocking claim" vs "question" vs "before/after reveal".
5. Output: hook taxonomy ranked by engagement velocity.

### B. Find 10 micro-creators in beauty for partnership
1. Phyllo search: `followers_between=(10000, 100000)`, `category=beauty`, `country=US`, `engagement_rate>0.05`.
2. Filter by brand-safety + recent posting activity.
3. Output: 10 candidates w/ engagement-rate-weighted score.

### C. Should I jump on a sound?
1. Pull current top-100 sounds.
2. For each sound on rising trajectory (day 2–4): get example videos.
3. Heuristic: avg engagement velocity in first 48h > niche median → green-light.

### D. Content-pillar mix audit
1. `tiktok-mcp` → own last 30 uploads.
2. LLM classifier on captions: educational/entertainment/inspirational/promotional.
3. Current mix: 60/15/10/15 → over-indexing on educational, under on entertainment.
4. Recommend: add 5 entertainment posts next month to rebalance.

## Edge cases / gotchas

1. **TikTok Research API approval takes 5–10 days.** Plan ahead. Fallback to Apify for time-sensitive work.
2. **Apify scrapers** can break when TikTok changes its frontend. Monitor the actor's last-updated date.
3. **Rate limits** on Research API: ~1000 requests/day. Cache aggressively.
4. **Trending hashtags are region-locked.** Always pass `countryCode`.
5. **Sounds with copyright restrictions** sometimes vanish from trending lists mid-trend.
6. **Phyllo data freshness** — audience demographics update weekly, not real-time.
7. **Hashtag stuffing** (>8 tags per post) is algorithmically downranked since 2024.
8. **Banned categories** vary by region; some hashtags trending in MX banned in DE.
9. **TikTok "Creator Marketplace"** is separate from Research API — for brand-creator matching.
10. **Phyllo charges per profile fetch** in some tiers — budget query patterns.
11. **First-3s analysis requires video download.** Research API provides download URL; Apify provides `videoUrl` field.
12. **Sound IDs change** when TikTok re-uploads under different ID — always cross-reference by audio fingerprint when persisting across days.

## Sources
- https://developers.tiktok.com/doc/research-api-specs-query-videos
- https://developers.tiktok.com/doc/about-research-api
- https://apify.com/clockworks/tiktok-trending-hashtags-scraper
- https://apify.com/clockworks/tiktok-scraper
- https://docs.getphyllo.com/
