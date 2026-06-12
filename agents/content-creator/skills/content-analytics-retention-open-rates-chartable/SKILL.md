# Content Analytics — CTR / Listen-Through / Retention / Chartable / Podtrac

> Roll up per-format analytics (newsletter CTR, podcast LTR, YouTube retention, social engagement) into a single dashboard.

## When to use

Trigger on: "audit my content analytics", "what's my CTR / LTR / retention", "Beehiiv analytics", "Chartable / Podtrac", "newsletter open rates lie", "podcast listen-through rate", "YouTube retention curve", "cross-platform reporting". This skill owns: per-format primary signal selection, tool chain for pulling stats, weekly + monthly + quarterly reporting cadence. Per-platform deep growth tactics live in `newsletter-subscriber-growth` (newsletter) and content-specific skills (podcast/video/carousel). For audience research surveys see `newsletter-audience-survey`.

## Setup

```bash
# Beehiiv MCP (read-only V1)
npx @beehiiv/mcp-server query --help

# YouTube Data API v3 via youtube-mcp
npx -y @youtube/mcp-server@latest --help

# Chartable / Podtrac — REST + dashboard exports
curl -H "Authorization: Bearer $CHARTABLE_API_KEY" \
  https://chartable.com/api/v1/podcasts

# Podtrac — measurement-only; dashboard CSV export
# https://analytics.podtrac.com/

# PostHog for funnel + cohort retention
npx @posthog/mcp-server --version

# Firecrawl for Substack stats scrape
npx @firecrawl/mcp --version

# Spotify for Podcasters + Apple Podcasts Connect — manual export only
```

Auth env vars:
- `BEEHIIV_API_KEY` + `BEEHIIV_PUBLICATION_ID`
- `YOUTUBE_API_KEY` or OAuth for `youtube-mcp`
- `CHARTABLE_API_KEY` — Chartable subscription tier needed
- `PODTRAC_API_KEY` — Podtrac Pro tier
- `POSTHOG_API_KEY` + `POSTHOG_PROJECT_ID`
- `SUBSTACK_SESSION_COOKIE` — for scrape

## Common recipes

### Recipe 1: Per-format primary signal map

```markdown
| Format | Primary signal | Good benchmark | Restructure if |
|---|---|---|---|
| Newsletter | CTR (clicks/sends) | >2% | <1% |
| Newsletter | CTOR (clicks/opens) | >10% | <5% |
| Newsletter | Revenue per recipient | >$0.50/issue | <$0.10/issue |
| Podcast | LTR at 25-min mark | >50% | <30% |
| Podcast | Avg listens per episode growth | +10% / quarter | flat or negative |
| YouTube long | Avg view duration | 50% retention at 3-min | <30% at 3-min |
| YouTube Shorts | Avg view duration + share rate | 75% completion + 2-3% share | <40% completion |
| LinkedIn carousel | Engagement rate | 6.6% | <3% |
| LinkedIn text | Engagement rate | 1.11% | <0.5% |
| X thread | Profile clicks + bookmark rate | 3% bookmark | <1% bookmark |
| TikTok | Completion rate + share rate | 30%+ + 2-3% | <15% |
| Reels | Completion rate + share rate | 30%+ + 2-3% | <15% |
| Blog post | Time on page + scroll depth + organic ranking | 2+ min ToP, 60%+ scroll, top 10 in 3 mo | <1 min, <30%, top 50 |
```

### Recipe 2: Newsletter analytics pull (Beehiiv)

```bash
# Per-post analytics
npx @beehiiv/mcp-server query \
  --tool get_post_analytics \
  --args '{"publication_id":"'"$BEEHIIV_PUBLICATION_ID"'","post_id":"<post_id>"}' \
  | jq '{title, sent_to, opens, clicks, ctr:.click_rate, ctor:.click_to_open_rate, revenue_per_recipient}'

# Aggregate last 30 days
npx @beehiiv/mcp-server query \
  --tool get_publication_analytics \
  --args '{"publication_id":"'"$BEEHIIV_PUBLICATION_ID"'","range":"last_30_days"}'
```

### Recipe 3: Newsletter analytics pull (Substack scrape)

```bash
# Substack has no public API; scrape stats page via firecrawl
npx @firecrawl/mcp scrape \
  --url "https://yoursub.substack.com/publish/stats" \
  --headers '{"Cookie":"substack.sid='"$SUBSTACK_SESSION_COOKIE"'"}' \
  --output substack_stats.json

jq '.posts[]|{title, sends, opens, clicks, paid_conversions}' substack_stats.json
```

### Recipe 4: Newsletter analytics pull (Ghost)

```bash
# Ghost native email stats
curl -H "Authorization: Ghost $TOKEN" \
  "$GHOST_ADMIN_URL/ghost/api/admin/posts/<post_id>/email/" \
  | jq '{subject, opened_count, opened_rate, delivered_count, failed_count}'

# Member counts
curl -H "Authorization: Ghost $TOKEN" \
  "$GHOST_ADMIN_URL/ghost/api/admin/stats/members/total/"
```

### Recipe 5: Podcast LTR + downloads via Chartable

```bash
# Chartable cross-platform stats
curl -H "Authorization: Bearer $CHARTABLE_API_KEY" \
  "https://chartable.com/api/v1/podcasts/<podcast_id>/episodes?per_page=20" \
  | jq '.data[] | {title, downloads, listen_through_rate_25min, geo_breakdown}'

# Per-episode deep retention
curl -H "Authorization: Bearer $CHARTABLE_API_KEY" \
  "https://chartable.com/api/v1/episodes/<episode_id>/retention" \
  | jq '.retention_curve'
```

### Recipe 6: Podcast Spotify + Apple manual export

```markdown
## Spotify for Podcasters
- Dashboard → Analytics → Export CSV
- Pull: streams_started, listeners_unique, listen_through_rate, geo, demo
- Frequency: weekly manual export → upload to Notion DB or PostgreSQL

## Apple Podcasts Connect
- Dashboard → Analytics → Export CSV
- Pull: listeners, plays, engaged_listeners (>1 min), avg_consumed
- Frequency: weekly
```

### Recipe 7: YouTube retention via youtube-mcp

```bash
# Per-video stats
npx @youtube/mcp-server videos_list \
  --video-id "<vid_id>" \
  --part "statistics,contentDetails" \
  | jq '{title, views:.statistics.viewCount, likes:.statistics.likeCount, comments:.statistics.commentCount}'

# Retention curve (requires YouTube Studio Reporting API)
# Use videoanalytics endpoint:
curl "https://youtubeanalytics.googleapis.com/v2/reports" \
  -H "Authorization: Bearer $YOUTUBE_OAUTH_TOKEN" \
  -d "ids=channel==MINE&startDate=2026-05-01&endDate=2026-06-10&metrics=averageViewPercentage,averageViewDuration&dimensions=video&filters=video==<vid_id>"
```

### Recipe 8: Cross-format UTM roll-up (the master analytics)

```bash
# UTM-tag every URL across formats:
# - utm_source=newsletter|podcast|youtube|linkedin|tiktok|x|threads
# - utm_medium=email|podcast-show-notes|video-description|carousel|thread
# - utm_campaign=<issue/episode/series slug>
# - utm_content=<cta-name>

# Roll up via PostHog
npx @posthog/mcp-server query \
  --hogql "SELECT properties.utm_source, count() as conversions FROM events WHERE event = '\$pageview' AND properties.utm_campaign = 'ep042' GROUP BY properties.utm_source"
```

### Recipe 9: PostHog cohort retention (newsletter funnel)

```bash
# HogQL for newsletter funnel retention
npx @posthog/mcp-server query \
  --hogql "
SELECT
  date_trunc('week', timestamp) as week,
  countIf(event = '\$pageview' and properties.\$current_url like '%newsletter-signup%') as signups,
  countIf(event = '\$pageview' and properties.\$current_url like '%dashboard%') as activated,
  activated / signups as activation_rate
FROM events
WHERE timestamp > now() - INTERVAL 90 DAY
GROUP BY week
ORDER BY week DESC
LIMIT 12
"
```

### Recipe 10: Social analytics (per platform)

```bash
# LinkedIn carousel stats (linkedin-marketing-api)
curl -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  "https://api.linkedin.com/rest/posts/<post_urn>/analytics"

# X thread stats (twitter-mcp)
npx @twitter/mcp-server get_tweet_metrics --tweet-id <id>

# TikTok stats (tiktok-mcp)
npx @tiktok/mcp-server get_video_stats --video-id <id>

# Instagram Reels stats (insta-business-mcp)
npx @insta-business/mcp-server get_reel_stats --reel-id <id>
```

### Recipe 11: Weekly report rollup

```python
from datetime import datetime, timedelta

# Pull all primary signals for last 7 days
week_data = {
    'newsletter': {
        'issues_sent': 1,
        'avg_ctr': pull_beehiiv_avg_ctr_last_7d(),
        'subscribers_net_new': pull_beehiiv_net_new_subs_last_7d(),
        'revenue_per_recipient': pull_beehiiv_revenue_per_recipient(),
    },
    'podcast': {
        'episodes_published': 1,
        'avg_ltr_25min': pull_chartable_ltr(),
        'avg_downloads': pull_chartable_avg_downloads(),
    },
    'youtube': {
        'videos_published': 0,
        'shorts_published': 5,
        'total_views': pull_youtube_views(),
        'avg_view_duration': pull_youtube_avg_duration(),
    },
    'linkedin': {
        'carousels_published': 2,
        'avg_engagement_rate': pull_linkedin_engagement(),
    },
    'x_threads': {
        'threads_published': 2,
        'avg_bookmark_rate': pull_x_bookmarks(),
    },
}

# Push to Notion dashboard
notion.create_page(NOTION_ANALYTICS_DB, properties={
    'Week': datetime.now().strftime('%Y-W%V'),
    'Newsletter CTR': week_data['newsletter']['avg_ctr'],
    'Podcast LTR 25min': week_data['podcast']['avg_ltr_25min'],
    'YouTube avg duration': week_data['youtube']['avg_view_duration'],
    # ...
})
```

### Recipe 12: Quarterly content audit

```markdown
# Quarterly Content Audit — <Q?> <Year>

## Top performers (top 10% of pieces)
- <piece 1> — <format> — <primary signal: e.g. CTR 7.2%, LTR 65%>
- ...

## Bottom performers (bottom 10%)
- <piece 1> — <format> — <signal>
- ...

## Format-level ROI
| Format | # produced | Avg signal | Hours-per | Reach / Hour |
|---|---|---|---|---|
| Newsletter | 13 | 3.1% CTR | 8 | 1,200 sent |
| Podcast | 13 | 48% LTR | 12 | 3,500 listens |
| LinkedIn carousel | 12 | 7.1% engagement | 2 | 8,200 impressions |
| X thread | 12 | 2.8% bookmark | 1.5 | 12,000 impressions |
| Reels | 25 | 35% completion | 1 | 1,800 views |

## Recommendations
- Double down on: <format with best ROI/hr>
- Cut: <format with bottom-quartile signal>
- Test: <new format hypothesis>
```

## Examples

### Example 1: Weekly Tuesday roll-up

**Goal:** Every Tuesday, pull all primary signals for past week into Notion dashboard.

**Steps:**
1. Recipe 11: cron job runs Tuesday 7am ET.
2. Pulls Beehiiv (newsletter), Chartable (podcast), YouTube (video), LinkedIn / X / TikTok (social).
3. Writes Notion dashboard row.
4. Sends Slack notification with anomaly callouts.
5. Operator reviews + takes action.

**Result:** Weekly state-of-channels at a glance.

### Example 2: Quarterly content audit + format ROI

**Goal:** End of quarter, identify which formats to double down on / cut.

**Steps:**
1. Recipe 12: build audit doc.
2. Compute format ROI per Recipe 12 table.
3. Identify top 10% + bottom 10% pieces.
4. Decide: keep / iterate / cut next-quarter cadence.
5. Update agent.yaml `content-series-multi-format-arcs` skill default per insights.

**Result:** Resource reallocation toward highest-ROI formats.

### Example 3: Newsletter funnel cohort retention

**Goal:** Are new subs retaining? Or are they ghosting after issue 2?

**Steps:**
1. Recipe 9: HogQL cohort retention query — weekly cohorts × engagement at week 4, 8, 12.
2. Identify cohort drop-off pattern.
3. If cold by week 4 → improve welcome sequence (Recipe 8 in `newsletter-subscriber-growth`).
4. If cold by week 12 → newsletter content needs fresh angle.

**Result:** Targeted retention intervention based on cohort signal.

## Edge cases / gotchas

- **Open rate is the most-lied-about metric.** Apple MPP inflates Beehiiv / Substack opens to 60%+. Always quote CTR or CTOR instead.
- **Substack has no public API** — firecrawl scrape only, brittle to DOM changes.
- **Spotify + Apple podcast analytics are manual-export-only.** No public API for either as of June 2026. Build the manual export into your weekly workflow.
- **Listen-through rate (LTR) at 25-min mark is the podcast professional benchmark.** Below 30% = restructure.
- **YouTube retention curve >50% at 3-min** is the long-form pro benchmark; >75% completion is the Shorts benchmark.
- **LinkedIn carousel engagement rate of 6.6%** is the carousel-format benchmark, NOT text-post (which is 1.11%).
- **X bookmark rate of 3%+** is the high-quality thread signal — bookmarks are a stronger ICP signal than likes/reposts.
- **TikTok share rate of 2-3%** = algorithm-friendly content; below 1% won't compound.
- **Don't quote opens as success.** Quote CTR + CTOR. Mention "we don't track opens as a primary metric" if asked.
- **UTM hygiene is the lever** — without consistent UTMs, you can't roll up cross-format ROI.
- **PostHog funnel queries require event-tracking discipline** on landing pages. If you don't have it set up, that's prerequisite work.
- **Chartable + Podtrac give CROSS-PLATFORM podcast reach** (Spotify + Apple + others combined) — critical for sponsor-facing audience data.
- **Beehiiv MCP V1 read-only** — analytics yes, writing/sending no. For automated sending see Recipe 2-3 in `long-form-newsletter`.
- **Revenue per recipient is the truer-than-CTR metric** for monetized newsletters. CTR + tier conversion = revenue per recipient. Track quarterly.
- **Geographic distribution often surprises** — podcasts especially. Check Chartable geo breakdown quarterly; may reveal sponsorship opportunities.
- **Don't roll up too frequently.** Weekly is the meaningful unit; daily is noise.
- **Notion dashboards drift** — schedule a quarterly clean-up of stale rows + property updates.

## Sources

- [Beehiiv MCP](https://product.beehiiv.com/p/beehiiv-mcp)
- [Cleanvoice — Best podcast APIs 2026](https://cleanvoice.ai/blog/best-podcast-api/)
- [Chartable](https://chartable.com/)
- [Podtrac](https://analytics.podtrac.com/)
- [YouTube Data API v3](https://developers.google.com/youtube/v3)
- [PostHog HogQL](https://posthog.com/docs/hogql)
- [Apple Podcasts Connect Analytics](https://podcasters.apple.com/support/analytics)
- [Spotify for Podcasters Analytics](https://podcasters.spotify.com/)
- [Beehiiv Analytics API](https://developers.beehiiv.com/)
- [Apple MPP impact on email metrics](https://www.litmus.com/blog/the-ultimate-guide-to-apple-mail-privacy-protection)
- [LinkedIn carousel engagement (Supergrow)](https://www.supergrow.ai/blog/linkedin-carousel-generators)
