# YouTube Data API v3 — Competitor + Trending Research

## When to use
- Find trending videos in a niche / region
- Pull competitor channel performance (views, subs, upload cadence)
- Fetch top videos by keyword
- Get transcripts of high-performers for hook pattern analysis
- Calculate quota use before mass-querying

## Setup
- `youtube-mcp` and `youtube-mcp-transcript` (already wired in `agent.yaml`)
- User supplies `YOUTUBE_API_KEY` (Google Cloud Console → Credentials)
- Free tier: **10,000 quota units/day**

## Quota math (critical)
| Method | Cost |
|---|---|
| `videos.list` | 1 unit |
| `channels.list` | 1 unit |
| `playlistItems.list` | 1 unit |
| `search.list` | **100 units** |
| `videos.insert` | 1600 units |

A typical research session: 1 `search.list` (100) + 50 `videos.list` (50) + 10 `channels.list` (10) = **160 units**. → ~60 research sessions/day on free tier.

## Common recipes

### 1. Most popular videos (region + category)
```bash
curl "https://www.googleapis.com/youtube/v3/videos\
?part=snippet,contentDetails,statistics\
&chart=mostPopular\
&regionCode=US\
&videoCategoryId=22\
&maxResults=50\
&key=$YOUTUBE_API_KEY"
```
Categories: `1`=Film, `10`=Music, `20`=Gaming, `22`=People & Blogs, `23`=Comedy, `24`=Entertainment, `25`=News, `26`=Howto, `27`=Education, `28`=Science.

### 2. Search by keyword (newest, view-sorted)
```bash
curl "https://www.googleapis.com/youtube/v3/search\
?part=snippet\
&q=espresso+machine+review\
&type=video\
&order=viewCount\
&publishedAfter=2026-05-01T00:00:00Z\
&maxResults=25\
&key=$YOUTUBE_API_KEY"
```
Returns `videoId` array. Then fetch full stats with `videos.list`.

### 3. Hydrate search results with statistics
```bash
IDS=$(curl ".../search?..." | jq -r '.items | map(.id.videoId) | join(",")')
curl "https://www.googleapis.com/youtube/v3/videos\
?part=snippet,contentDetails,statistics\
&id=$IDS\
&key=$YOUTUBE_API_KEY"
```
Two calls cost: 100 (search) + 1 (videos) = 101 units. Up to 50 IDs per `videos.list` call.

### 4. Channel stats
```bash
curl "https://www.googleapis.com/youtube/v3/channels\
?part=snippet,statistics,contentDetails\
&id=$CHANNEL_ID\
&key=$YOUTUBE_API_KEY"
```
Returns subscriberCount, viewCount, videoCount, uploads playlist ID.

### 5. Channel's recent uploads (cheap path)
```bash
UPLOADS=$(curl ".../channels?id=$CHANNEL_ID&part=contentDetails" \
  | jq -r .items[0].contentDetails.relatedPlaylists.uploads)
curl "https://www.googleapis.com/youtube/v3/playlistItems\
?part=snippet,contentDetails\
&playlistId=$UPLOADS\
&maxResults=50\
&key=$YOUTUBE_API_KEY"
```
1 + 1 = 2 units. Way cheaper than `search.list` for same channel.

### 6. Trending hashtags (in titles + descriptions)
YouTube doesn't expose hashtag analytics. Workaround: pull top-100 videos in niche → grep `#\w+` from titles + descriptions → frequency count.

### 7. Competitor benchmarking workflow
```python
# Pseudocode
competitors = ["UCx123", "UCx456", "UCx789"]
for ch in competitors:
    stats = api.channels(id=ch).statistics
    uploads = api.playlistItems(playlistId=ch.uploads).items
    vids = api.videos(id=[u.contentDetails.videoId for u in uploads[:20]])
    # Calculate: avg views/video, views-to-sub ratio, upload cadence
```

### 8. Fetch transcripts (via youtube-mcp-transcript)
```python
# MCP call
result = youtube_mcp_transcript.get(video_id="dQw4w9WgXcQ", lang="en")
# Returns: [{"text": "...", "start": 0.5, "duration": 3.2}, ...]
```
Use to extract first-15s hook patterns from top-performing videos.

### 9. Quota check
The API returns headers `Quota-User` but not remaining quota. Track manually:
```python
QUOTA_BUDGET = 10000
QUOTA_USED = 0
def call(cost):
    global QUOTA_USED
    QUOTA_USED += cost
    if QUOTA_USED > QUOTA_BUDGET: raise QuotaExhausted()
    # ...make call
```

### 10. CTR proxy calculation (no direct CTR exposure)
YouTube doesn't expose CTR via public API. Proxy:
```
CTR_proxy = views / (channel_subs × 0.05)  # assumes 5% impression rate from subs
```
Better proxy: views per day = views / hours_since_upload. Compare across competitor videos of similar age.

### 11. Search filters cheat sheet
- `order=`: `date`, `rating`, `relevance`, `title`, `videoCount`, `viewCount`
- `type=`: `video`, `channel`, `playlist`
- `videoDuration=`: `short` (<4min), `medium` (4-20min), `long` (>20min)
- `videoDefinition=`: `high`, `standard`
- `regionCode=`: ISO 3166-1 alpha-2

### 12. Pagination
```bash
NEXT_TOKEN=$(curl "..." | jq -r .nextPageToken)
curl "...&pageToken=$NEXT_TOKEN"
```
Loop until `nextPageToken` is null.

### 13. Captions API (caption tracks, not transcripts)
```bash
curl "https://www.googleapis.com/youtube/v3/captions\
?part=snippet&videoId=$VID&key=$YOUTUBE_API_KEY"
```
Downloading the actual track requires OAuth (not just API key) per YouTube ToS.

### 14. Best time-to-publish analysis
1. Pull 100 top videos in niche.
2. Extract `snippet.publishedAt` timestamps.
3. Bin by hour-of-day + day-of-week.
4. Cross-reference with `viewCount` to find conversion-weighted optimal slot.

### 15. Topic clustering
Pull 200 top videos → embed titles via Claude → KMeans cluster → name clusters → recommend white-space topic to user.

## Examples

### A. "What's trending in fitness right now?"
```bash
# 100 units total
curl ".../search?q=fitness&order=viewCount&publishedAfter=$(date -d '7 days ago' -I)T00:00:00Z&type=video&maxResults=50" \
  | jq -r '.items | map(.id.videoId) | join(",")' \
  | xargs -I {} curl ".../videos?part=snippet,statistics&id={}"
```

### B. Competitor channel deep-dive
1. `channels.list` for stats (1 unit).
2. `playlistItems.list` for uploads playlist (1 unit).
3. `videos.list` (batched) for stats on 50 latest (1 unit).
4. Analyze: avg views, upload cadence, title patterns, retention proxy.

### C. Hook pattern mining (top 50 in niche → first 15s)
1. `search.list` for top 50 (100 units).
2. `videos.list` to hydrate (1 unit).
3. `youtube-mcp-transcript` for each: pull `start ≤ 15` seconds.
4. Cluster: question-hook vs claim-hook vs visual-hook patterns.

### D. Title A/B intelligence (which patterns convert)
Pull 200 top videos, score `views/(age_in_days * sub_count)`, regress against title features (length, ALL CAPS%, question mark, number presence) — identifies title patterns that outperform.

## Edge cases / gotchas

1. **`search.list` is 100 units** — design queries to use `videos.list` and `playlistItems.list` where possible.
2. **Quota resets at midnight Pacific Time** — not your local TZ.
3. **`maxResults` cap at 50.** Use pagination for >50.
4. **`publishedAfter`/`Before` requires ISO 8601 UTC** with `Z` suffix.
5. **Search returns may include older videos** that are "trending again" — filter by `publishedAt` explicitly.
6. **Statistics may be unavailable** for private/restricted/recent videos. Defensive: `.statistics?.viewCount ?? 0`.
7. **Trending = chart=mostPopular** is region-aware. Always pass `regionCode`.
8. **Caption text via captions API** requires OAuth + content-owner; use `youtube-mcp-transcript` (scrapes from frontend) for read-only.
9. **Channel ID vs handle** — modern API accepts both, but `@handle` requires `forHandle=` not `id=`.
10. **Filtering by language** — `search.list` supports `relevanceLanguage`, not strict `language`.
11. **Quota-exceeded returns 403** with `quotaExceeded` reason — code defensively.
12. **API keys can be IP-restricted** — confirm restrictions in Cloud Console when 403s appear unexpectedly.

## Sources
- https://developers.google.com/youtube/v3/docs/videos/list
- https://developers.google.com/youtube/v3/docs/search/list
- https://developers.google.com/youtube/v3/docs/channels/list
- https://developers.google.com/youtube/v3/getting-started#quota
- https://developers.google.com/youtube/v3/docs/captions
