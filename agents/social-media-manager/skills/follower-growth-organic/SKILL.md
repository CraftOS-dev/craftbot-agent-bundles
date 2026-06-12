<!--
Source: https://www.gpt.social/blog/how-to-find-trending-sounds-tiktok-reels-2026
Buffer best-time-to-post: https://buffer.com/library/best-time-to-post-on-social-media/
Collab posts: IG Collab feature, TikTok Duet/Stitch
-->
# Follower Growth — Organic Tactics — SKILL

Trending-audio first-mover (3-5x algorithmic push in 48hr window) + consistent posting cadence per platform + genuine community participation (engagement-pod replacement) + collab posts (IG Collab, TikTok Duet/Stitch). Brand24 / Sprout cohort analytics show which content compounds. Quarterly trend-adoption queue from `social-trend-monitoring-tiktok-sounds-reels`.

## When to use this skill

- **Brand or creator wants organic follower growth** (not paid).
- **Plateau diagnosis** — stagnant follower curve, what to do.
- **New account launch** — first 90 days cadence and tactics.
- **Cadence audit** — too much / too little / wrong-time posting.

**Do NOT use this skill when:**
- Already running paid ads — augment via `facebook-ads-mcp` / `tiktok-ads-mcp`.
- Vanity-metric chasing — refer to role.md success-metrics; growth-only without retention is hollow.

## Setup

### Buffer analytics for cadence audit

```bash
mcp tool buffer.get_analytics \
  --channelIds '["all"]' \
  --since "$(date -u -d '90 days ago' +%Y-%m-%d)" \
  --metrics '["follower_growth","posts","engagement_rate","reach"]'
```

### TikTok Creative Center / Tokchart for trend feeds

Pre-configured in `social-trend-monitoring-tiktok-sounds-reels`.

### Notion Growth DB

Columns: `Week / Platform / Posts shipped / Avg reach / Avg ER / Follower delta / Top post / Top post type / Trends adopted / Collab posts shipped`.

### Instagram Collab Posts API

```bash
# Via insta-business-mcp
mcp tool insta_business.create_collab \
  --media_id "<id>" \
  --collaborator_handle "<partner>"
```

### TikTok Duet / Stitch via `tiktok-mcp`

```bash
mcp tool tiktok.create_duet --video_id "<original>" --duet_video_url "<your_video>"
mcp tool tiktok.create_stitch --video_id "<original>" --stitch_video_url "<your_video>"
```

## Common recipes

### Recipe 1: Per-platform posting cadence (90-day plan)

```yaml
linkedin:
  weekday: 1-2 posts (Tue / Wed / Thu best per role.md)
  weekend: 0
  format: 60% long-form text, 30% carousel, 10% video
  goal_followers_per_post: 50-200 in first 90 days
x:
  weekday: 3-5 posts + 5-10 reply-engagements
  weekend: 1-2 posts
  format: 50% original, 30% reply / quote-reply, 20% thread
tiktok:
  daily: 1-2 videos
  format: 70% trend-adoption + 30% evergreen brand voice
instagram:
  reels: 4-5 per week
  feed: 2-3 per week
  stories: daily 3-5 frames
threads:
  daily: 2-3 posts (conversation-first)
bluesky:
  daily: 2-3 posts + 5-10 reply chains
```

### Recipe 2: Trending-audio adoption queue

Pull from `social-trend-monitoring-tiktok-sounds-reels`:

```python
# Each morning, top 3 rising sounds with brand-fit ≥ 6 → adopt today
trending = mcp.trend.get_brief(date=today)
for sound in trending['accelerating'][:3]:
    if sound['brand_fit'] >= 6 and sound['ship_by'] >= now + 36h:
        notion.create(content_queue_db, {
            'Sound ID': sound['sound_id'],
            'Hook idea': sound['hook_idea'],
            'Ship-by': sound['ship_by'],
            'Status': 'queued'
        })
```

### Recipe 3: Engagement pod replacement (genuine community engagement)

Instead of pod-swapping, build real community engagement habit:

```python
# Daily 30-min engagement block per platform
schedule = {
    'instagram': '10am-10:30am — engage 50 posts in niche hashtags',
    'tiktok':    '11am-11:30am — engage 30 niche videos',
    'linkedin':  '12pm-12:30pm — engage 20 posts in niche feed',
    'x':         'rolling — 10 thoughtful replies/day',
    'threads':   'rolling — 5 conversation starters/day',
}
# Genuine adds: 1-2 sentence value comment, NOT generic "love this"
```

### Recipe 4: IG Collab post setup

```bash
# Step 1: invite collaborator on post creation
curl -X POST "https://graph.facebook.com/v20.0/$IG_BUSINESS_ID/media" \
  -d "media_type=REELS" \
  -d "video_url=$URL" \
  -d "caption=Caption" \
  -d "collaborators=collaborator_business_id_or_handle" \
  -d "access_token=$META_GRAPH_TOKEN"

# Step 2: collaborator accepts via IG app (manual)
# Post appears on both feeds, shares follower base
```

### Recipe 5: TikTok Duet / Stitch for collab leverage

```python
# Find collab targets: creators with overlapping audience but no direct overlap
# Use Modash or HypeAuditor to identify
collab_targets = modash.search(
    audience_country='US', engagement_rate_min=3.0,
    follower_range=(20_000, 100_000),
    niche='same_as_brand'
)
# Duet their viral content (with permission) — drives discovery to your account
for c in collab_targets:
    viral_videos = mcp.tiktok.get_user_top_videos(c['handle'], limit=5)
    # DM the creator: would you mind if we duet'd this with a takeaway?
    mcp.tiktok.send_dm(c['handle'], DUET_REQUEST_TEMPLATE)
```

### Recipe 6: Best-time-to-post per platform (audit)

```python
# Per platform, pull last 90 days of own posts; analyze reach/engagement by hour
for platform in PLATFORMS:
    posts = mcp.buffer.get_analytics_per_post(channel=platform, since='90d')
    by_hour = defaultdict(list)
    for p in posts:
        by_hour[p['scheduled_at'].hour].append(p['engagement_rate'])
    optimal = sorted(by_hour.items(), key=lambda x: -mean(x[1]))[:3]
    notion.upsert(growth_db, {'Platform': platform,
                              'Best hours': [h for h, _ in optimal]})
```

### Recipe 7: Follow-back / unfollow audit

```python
# Quarterly: remove inactive followers (low ER drag)
# IG / X audit via API
inactive = mcp.insta_business.get_inactive_followers(threshold_days=180, limit=500)
# DO NOT mass-unfollow (rate-limit risk); review manually
# Better: don't auto-follow back; quality > quantity
```

### Recipe 8: Cohort-engagement analysis (Sprout / Brand24)

```python
# Identify content patterns that compound
all_posts = mcp.buffer.get_analytics_per_post(channel='all', since='90d')
clusters = cluster_by_format_topic_hook(all_posts)
top_clusters = sorted(clusters, key=lambda c: c['avg_engagement_rate'])[-3:]
for c in top_clusters:
    notion.create(growth_insight_db, {
        'Pattern': c['name'],
        'Avg ER': c['avg_engagement_rate'],
        'Posts in cluster': c['post_count'],
        'Recommendation': f"Double down — 30% of next quarter's content"
    })
```

### Recipe 9: Repost-stack for top performers

```python
# A post that outperforms by 3x baseline = repost template
top = [p for p in last_90d_posts if p['engagement_rate'] > 3 * baseline_er]
for p in top:
    derivative = {
        'instagram_reel': create_reel_from(p),
        'twitter_thread': create_thread_from(p),
        'tiktok': adapt_for_tiktok(p),
        'youtube_short': vertical_cut(p),
    }
    # Stagger across 60 days
```

### Recipe 10: Quarterly growth retro

```python
# Per platform, 90-day delta
for platform in PLATFORMS:
    start_followers = notion.get(growth_db, week=q_start)['Followers']
    end_followers = notion.get(growth_db, week=q_end)['Followers']
    growth_pct = (end_followers - start_followers) / max(start_followers, 1) * 100
    # Per role.md: 5-10% MoM organic = healthy; 20%+ = on fire
    if growth_pct < 5 * 3:  # 5%/mo × 3 mo = 15% quarter
        slack.post('#growth', f"{platform}: only {growth_pct:.1f}% growth — diagnose")
```

## Examples

### Example A: New account launch — first 30 days

```yaml
day_1: bio + 5 foundational posts (pinned: brand intro)
day_1-7: 2 posts/day per platform; engagement block 30 min/day
day_8-14: trending-audio adoption × 3 on TikTok; 2 collab DMs sent
day_15-21: first IG Collab post live (if collab accepted)
day_22-30: cohort review; double down on top-3 patterns
target: 500-1k followers per platform from zero in first 30 days
```

### Example B: Plateau diagnosis (X stagnant at 5k)

```yaml
diagnosis:
  - audit cadence: posting 1/day, optimal 3-5/day
  - audit reply ratio: 5% reply, optimal 50-70% replies
  - audit thread cadence: 1 thread/week, optimal 3/week
  - audit topic mix: 90% brand promo, optimal 70% value / 30% promo
prescription:
  - increase to 3 posts/day + 10 replies/day
  - 3 threads/week minimum
  - shift to 70% value / 30% promo split
expected: 10-20% follower growth in 60 days
```

### Example C: TikTok 0 → 50k in 6 months

```yaml
months_1-2: 1 video/day, 80% trend-adoption, build follow-feedback signal
months_3-4: 2 videos/day, identify 3 evergreen formats that work, repeat
months_5-6: 1-2 videos/day evergreen + 2-3/week trending
collaborations:
  - duet 2 viral creators/week (with permission)
  - cross-promote with 3 similar-tier creators
metrics:
  - month 1: 1k followers
  - month 3: 12k
  - month 6: 50k
gates:
  - if videos not hitting 5k reach by month 2, fundamental hook/sound problem
  - if videos hitting reach but no follow conversion, weak profile + bio
```

## Edge cases

### Engagement-pod ban risk
IG / TikTok shadowban accounts in pod-rings. Don't join pods. Genuine community engagement is slower but durable.

### Follow-for-follow penalty
Algorithms detect coordinated follow-spree from brand accounts. Don't mass-follow. Don't request follow-back DM-spam.

### Trend chasing wears voice thin
Pure trend adoption = brand-vacuum. Cap 30% of posts as trend; 70% evergreen brand-voice. Stay anchored.

### Cadence too aggressive
Posting 10x/day signals bot to algorithm. Per-platform sustainable cadence (recipe 1) is the gate. Quality > volume.

### Cadence too sparse
< 3 posts/week per platform → cold-account signal; algorithm de-prioritizes. Maintain minimum even on slow weeks.

### Collab partner fit
A collab with a much bigger account skews audience — could dilute brand. Pair with similar-size for clean overlap, or accept dilution as awareness play.

### Cross-platform same-content trap
Same exact post across all → algorithm flags as low-effort cross-poster. Per-platform variant + native voice (see `platform-native-content-creation`).

### Vanity-follower drag
Bought followers / pod followers don't engage. ER drops. Algorithm de-prioritizes future content. Don't buy.

### Algorithm changes
Platforms tweak quarterly. What worked Q1 may not Q3. Treat your cohort-engagement analysis (Recipe 8) as living doc.

### Seasonal slumps
December / July often quiet. Don't over-react to 2-week dip. Compare YoY.

### Reach vs followers
A post can reach 1M and add 0 followers (drive-by viewers). Profile-clarity (bio, pinned, recent feed) converts reach → follow. Audit profile UX quarterly.

### Algorithm vs platform-fit
A brand on the wrong platform won't grow even with perfect execution. B2B SaaS on TikTok faces uphill battle vs LinkedIn. Acknowledge platform-brand fit.

### Audience fatigue
Same hook every post = audience tunes out. Vary format / tone / topic within brand-voice envelope.

### Public-engagement vs DM-engagement
Replying in DMs builds 1:1 trust but doesn't grow public. Balance: 70% public engagement, 30% DM.

### Algorithmic ranking opacity
You can't reverse-engineer perfectly. Test, measure, iterate. Patterns of what works compound; chase data, not theories.

## Sources

- **Trending sounds 2026 (gpt.social)**: https://www.gpt.social/blog/how-to-find-trending-sounds-tiktok-reels-2026
- **Buffer — best-time-to-post**: https://buffer.com/library/best-time-to-post-on-social-media/
- **Sprout Social — social media metrics**: https://sproutsocial.com/insights/social-media-metrics/
- **IG Collab Posts**: https://help.instagram.com/268523068844180
- **TikTok Duet / Stitch (Content API)**: https://developers.tiktok.com/doc/content-posting-api-get-started/
- **Role.md "Success metrics"**: per-platform growth thresholds
- **Spicy Creator Tips — best APIs 2026**: https://www.spicycreatortips.com/the-best-social-media-apis-for-developers-in-2026/
