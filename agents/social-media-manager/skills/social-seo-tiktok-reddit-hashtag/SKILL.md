<!--
Source: https://buffer.com/resources/best-social-media-apis/
Apify TikTok rank scraper: https://apify.com/clockworks/tiktok-scraper
Reddit search ranking: https://www.therankmasters.com/insights/brand-monitoring/best-reddit-brand-monitoring-tools
TikTok SEO: keyword in caption + on-screen text + alt text
-->
# Social SEO — TikTok / Reddit / Hashtag SEO — SKILL

TikTok SEO: keyword in caption (front-loaded 100-150 chars) + on-screen text (OCR signal) + alt text (2026 feature). Reddit SEO: title verbatim with target query, first comment with link, engage early for thread momentum. Hashtag SEO: long-tail + branded clustering. Track via Apify rank scrapers, `reddit-mcp`, Brand24 share-of-voice.

## When to use this skill

- **TikTok video optimization** for in-search discovery.
- **Reddit thread for Google rank** — Reddit pages rank high in SERP.
- **Branded hashtag share-of-voice** tracking over time.
- **Discovery audit** — which queries does our content rank for vs miss.

**Do NOT use this skill when:**
- Traditional SEO (website / blog) — `marketing-agent`'s `ahrefs-seo-mcp` + `pagespeed-cwv-audit`.
- AI search (LLM-attributed) — `aeo-geo-ai-search-tracking` (marketing-agent).

## Setup

### Apify TikTok scraper (rank monitoring)

```bash
export APIFY_TOKEN="<token>"
# Actor: clockworks/tiktok-scraper
# Cost: ~$0.10/profile or ~$0.05/search
```

### TikTok keyword-search rank check

```bash
curl -X POST "https://api.apify.com/v2/acts/clockworks~tiktok-scraper/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -d '{
    "searchQueries":["best face cream sensitive skin"],
    "resultsPerPage":50
  }'
```

### Reddit MCP

Already configured (see `reddit-strategy-ama-subreddit`). Used for:
- Search rank within subs
- Title performance audit
- First-hour engagement signal

### Brand24 MCP for branded-hashtag SoV

```bash
mcp tool brand24.get_share_of_voice \
  --project_id "$BRAND24_PROJECT_ID" \
  --tag "#yourbrand" \
  --period "30d"
```

### Notion SEO DB

Columns: `Query / Platform / Target rank / Current rank / Content URL / Hook / On-screen text / Alt text / Caption keyword / Date checked / Notes`.

## Common recipes

### Recipe 1: TikTok keyword research (search-volume signal)

```bash
# Pull top results for target query
curl -X POST "https://api.apify.com/v2/acts/clockworks~tiktok-scraper/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -d '{"searchQueries":["$QUERY"],"resultsPerPage":30}' \
  | jq '.[] | {handle: .authorUsername, views: .playCount, likes: .diggCount, comments: .commentCount, caption: .text, hashtags: .hashtags}'
```

Filter top 10; note common patterns: caption opening words, hashtag overlap, on-screen-text style.

### Recipe 2: TikTok caption template (SEO-optimized)

```python
def tiktok_caption(query, hook, brand_handle):
    # First 100-150 chars carry SEO weight
    seo_chunk = f"{query} — {hook}"  # query verbatim front-loaded
    body = f" {brand_handle} | tested for 30 days | honest review"
    hashtags = " #" + " #".join(['skincare','sensitiveskin','beautyreview','brandX'])
    return (seo_chunk + body + hashtags)[:300]
```

### Recipe 3: TikTok on-screen text spec (OCR signal)

TikTok's OCR scans on-screen text and uses for in-search ranking.

```yaml
on_screen_text_rules:
  - first_2s: visible keyword (matches caption)
  - text_size: large + bold (high-contrast)
  - text_duration: stays visible at least 0.5s
  - text_position: avoid bottom-third (cropped on some devices)
  - text_layers_max: 3 (avoid OCR noise)
```

### Recipe 4: TikTok alt text (2026 feature)

```bash
# Set alt text via Content Posting API
curl -X POST https://open.tiktokapis.com/v2/post/publish/video/init/ \
  -H "Authorization: Bearer $TIKTOK_ACCESS_TOKEN" \
  -d '{
    "post_info": {
      "title":"Best face cream for sensitive skin — 30-day review",
      "alt_text":"Person applying face cream, showing texture and results before/after",
      ...
    },
    ...
  }'
```

Per role.md: "Alt text (2026 feature): TikTok SEO signal — populate it."

### Recipe 5: Reddit title optimization

```python
# Reddit titles up to 300 chars; front-load query verbatim
def reddit_title(query, value_prop):
    return f"{query} — {value_prop} (case study with numbers)"[:300]

# Example
title = reddit_title("how to scale a SaaS to $1M ARR",
                     "the 3-channel playbook we used at PowerBrand")
# Output: "how to scale a SaaS to $1M ARR — the 3-channel playbook we used at PowerBrand..."
```

Reddit threads rank high in Google when title matches search query — this is the SEO unlock.

### Recipe 6: Reddit first-hour amplification

```python
# Post to relevant subs ASAP after publishing for first-hour engagement boost
subs = ['Entrepreneur', 'SaaS', 'startups']
for sub in subs:
    if subreddit_health_ok(sub) and follows_80_20_rule(sub, BRAND_USER):
        mcp.reddit.submit_post(subreddit=sub, title=title, selftext=body)

# Drop own first-comment with link 60s later
sleep(60)
mcp.reddit.add_comment(thing_id=thread_id,
                       text="OP here — full deck + chart: <link>")

# Encourage team members + close friends to upvote + comment within first hour
slack.post('#growth', f"Reddit post live: {thread_url} — please upvote/comment if relevant")
```

### Recipe 7: Subreddit search-rank check

```bash
# Search within sub for target query
mcp tool reddit.search_subreddit \
  --subreddit "Entrepreneur" \
  --query "scale SaaS $1M ARR" \
  --sort "relevance" \
  --time "year"
```

Track current rank vs target; if no result in top 10, schedule republish (after 90-day cool-down) with refined title.

### Recipe 8: Branded hashtag share-of-voice tracking

```python
# Weekly: per branded hashtag, total reach + use count
tags = ['#yourbrand', '#yourbrandX', '#yourbrandcommunity']
for tag in tags:
    sov = mcp.brand24.get_share_of_voice(project_id=BRAND24_PROJECT_ID,
                                          tag=tag, period='7d')
    notion.upsert(hashtag_sov_db, {
        'Tag': tag,
        'Week': week_start,
        'Use count': sov['mention_count'],
        'Reach': sov['total_reach'],
        'Sentiment ratio': sov['positive_pct'],
        'SoV vs competitor 1': sov['vs_competitors']['comp1']
    })
```

### Recipe 9: Discovery audit — what we rank for vs target

```python
# Quarterly
for target_query in TARGET_QUERIES:
    tt_rank = check_tiktok_rank(target_query, brand_handle=BRAND_HANDLE)
    reddit_serp = google_search(f"site:reddit.com {target_query}", brand_user=BRAND_USER)
    notion.upsert(seo_db, {
        'Query': target_query,
        'TikTok rank': tt_rank,
        'Reddit (Google SERP)': reddit_serp,
        'Date checked': today()
    })
```

### Recipe 10: Long-tail hashtag clustering

```python
# Cluster branded hashtags by topic for content-mapping
def cluster_branded_tags(tags):
    clusters = defaultdict(list)
    for tag in tags:
        topic = classify_topic(tag)  # e.g. #yourbrandAPI → "api", #yourbrandUX → "ux"
        clusters[topic].append(tag)
    return clusters
# Use to plan content covering each cluster proportional to brand priority
```

## Examples

### Example A: TikTok video for "best face cream sensitive skin"

```yaml
video:
  caption: "best face cream sensitive skin — my honest 30-day review #skincare #sensitive #honestreview #brandX"
  on_screen_text:
    - second 0-2: "BEST FACE CREAM FOR SENSITIVE SKIN" (large, top-third)
    - second 8: "Day 1 vs Day 30"
    - second 22: "$24, brand link below"
  alt_text: "Person applying face cream and showing before/after skin texture"
  hashtags: 4 (1 trending + 2 niche + 1 branded)
  hook_first_3s: "POV: you tried 5 face creams and only this one didn't irritate"
result_target: rank top 10 on "best face cream sensitive skin" query within 30 days
```

### Example B: Reddit thread targeting "scale SaaS to $1M ARR"

```yaml
title: "Scaled our SaaS to $1M ARR in 14 months — full breakdown with numbers"
subreddit: SaaS
body_outline:
  - month-by-month MRR chart
  - 3 channels we doubled down on
  - 2 things that didn't work
  - the one decision that mattered most
  - Q&A pinned at bottom
first_comment: "Full chart + raw spreadsheet: <link>"
target_serp: "scale SaaS $1M ARR" Google top 5
amplification:
  - 5 team upvotes in first 5 min
  - 2 cross-posts to /r/Entrepreneur, /r/startups (24-72 hr lag)
  - LinkedIn promo of the thread (drives Reddit votes from outside)
```

### Example C: Quarterly hashtag SoV report

```yaml
quarter: Q2 2026
branded_tags:
  '#powerbrand': use_count_30d=2,847 reach_30d=1.2M positive_pct=78%
  '#powerbrandX': use_count_30d=412 reach_30d=180k positive_pct=82%
  '#powerbrandlive': use_count_30d=89 reach_30d=24k positive_pct=91%
vs_competitor_avg_SoV: 47% (you) vs 31% (comp1) vs 22% (comp2)
trend: 'powerbrandlive' growing 30% MoM — invest more in Live programming
```

## Edge cases

### TikTok algorithm opacity
TikTok hasn't publicly documented SEO ranking factors; signal is empirical. Patterns shift quarterly. Re-test top performers; don't assume 2024 tactics work 2026.

### Reddit Google ranking volatility
Google's Reddit weighting changed mid-2024 + Q4 2025. Old high-ranking threads can drop overnight. Refresh top performers annually with comments + new info.

### Hashtag saturation kills SEO
Generic high-volume tags (#beauty 500M+ uses) bury your content. SEO sweet spot: long-tail, 10k-500k uses.

### TikTok caption length cap
2200 chars max; 100-150 chars carries SEO weight. Stuff long captions = noise; algorithm de-prioritizes keyword density beyond 5% of first chunk.

### On-screen text OCR quality
Hand-written / animated / decorative fonts → OCR misses. Use sans-serif bold, white-on-contrast background, static text duration ≥ 0.5s per element.

### Alt text rollout
TikTok alt text added 2026. Adoption is sparse; early movers get disproportionate SEO benefit. Always populate.

### Reddit shadow-ranking
A thread may appear live to OP but be removed from sub-feed / search. Verify via incognito Google search for thread title verbatim — if not indexed in 24-48 hr, sub may have flagged.

### Cross-post duplicate-content penalty
Posting near-identical content to 5+ subs in 24 hr — Reddit detects + penalizes. Stagger; vary intro paragraph + title.

### Brand24 SoV calculation
Brand24's SoV is mention-count-based, not unique-user-based. Adjust mentally if a single power-user accounts for 80% of mentions.

### Apify rate / cost
Scraping 100 queries/week = $5-20/week. Budget alerts at $100/mo cap.

### TikTok keyword cannibalization
Posting 5 videos all targeting "best face cream sensitive skin" — algorithm splits views. Cluster: target the head term once, target long-tail variants for the others.

### Reddit's noindex flag on some posts
NSFW + quarantined + manually-flagged threads get noindex. Google doesn't surface. Audit thread headers if SERP rank doesn't appear despite engagement.

### Influencer-led SEO
Mid-tier creator posting for your brand sometimes outranks branded content for query — leverage via UGC repost + co-create coordinated SEO push.

### Multi-language SEO
TikTok + Reddit search localized. Native-language content beats translated. For multi-market brand, run per-language SEO audit.

### Hashtag drift over time
A hashtag's connotation can change (e.g., #sustainability used to be brand-safe → now politically loaded in some markets). Quarterly audit + retire compromised tags.

## Sources

- **Apify TikTok scraper**: https://apify.com/clockworks/tiktok-scraper
- **Buffer — best social APIs (SEO context)**: https://buffer.com/resources/best-social-media-apis/
- **Reddit search + SEO (TheRankMasters)**: https://www.therankmasters.com/insights/brand-monitoring/best-reddit-brand-monitoring-tools
- **TikTok SEO 2026 (Spicy Creator Tips)**: https://www.spicycreatortips.com/the-best-social-media-apis-for-developers-in-2026/
- **TikTok Content Posting API (alt text)**: https://developers.tiktok.com/doc/content-posting-api-get-started/
- **Brand24 share-of-voice**: https://brand24.com/blog/share-of-voice/
- **Reddit API**: https://www.reddit.com/dev/api
