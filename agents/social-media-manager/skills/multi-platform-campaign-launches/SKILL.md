<!--
Source: https://buffer.com/resources/best-social-media-management-tools/
Campaign playbook: role.md "Multi-platform campaign playbook"
Buffer cascade + Notion brief
-->
# Multi-Platform Campaign Launches — SKILL

T-7 teaser cascade / T-0 main asset cross-channel within 2-hour window / T+1 to T+7 amplification with UGC + influencer + paid boost. Buffer scheduling + per-channel variants + Notion brief + Reddit AMA scheduled within 24-48 hrs of launch. Mid-flight pivot rules: hashtag death = swap; creator underdelivery = surface to `account-takeovers-creator-handoff`.

## When to use this skill

- **Product launch / brand re-launch / campaign kickoff**.
- **Major announcement** (funding, partnership, milestone).
- **Coordinated multi-channel push** with paid + influencer + UGC components.
- **Event-driven campaign** (conference, holiday, anniversary).

**Do NOT use this skill when:**
- Single-channel ad-hoc post — `community-engagement-comments-dms-at-scale`.
- Long-running evergreen content series — `platform-native-content-creation`.

## Setup

### Buffer team plan + cascade pre-configured

See `community-engagement-comments-dms-at-scale` setup.

### Notion Campaign DB

Columns: `Campaign / Status (planning/T-7/T-0/T+7/done) / Goal / KPI target / Kill criteria / Channels / Asset matrix / Influencer list / Paid budget / Owner / Start date / End date / Result`.

### Asset Notion DB (linked to Campaign)

Columns: `Asset ID / Campaign / Channel / Format / Variant ID / Status (draft/review/approved/scheduled/published) / Owner / Asset URL / Buffer ID / Published URL / Performance`.

### Pre-set UTM convention

Inherit from `bitly-utm-campaign-tracking` (marketing-agent):

```python
UTM = "?utm_source={platform}&utm_medium=social&utm_campaign={campaign}&utm_content={asset_id}"
```

## Common recipes

### Recipe 1: Campaign brief

Per role.md "Multi-platform campaign playbook":

```markdown
# Campaign: Summer Drop 2026

## Objective
- Primary: Conversions (online sales)
- Success metric: $250k GMV first 14 days
- Kill criteria: < $50k by day 7 = pause + rework

## Channels and mix
- LinkedIn: 20% budget — thought-leadership product story
- X: 15% — daily thread + reactive posts
- IG: 25% — Reels + carousel + Stories
- TikTok: 25% — daily creator drops + brand video
- Threads: 5%
- Reddit AMA: 5% — r/Entrepreneur + niche subs
- YouTube Shorts: 5%
- Pinterest: bonus — pin to product

## Asset matrix
| Asset ID | Channel | Format | Variant | Status | Owner |
|---|---|---|---|---|---|
| A1 | LinkedIn | Carousel | Authority | Draft | @editor |
| A2 | TikTok | Video | Trend-audio | In review | @creator1 |
| A3 | IG | Reel | Founder POV | Approved | @founder |
| A4 | X | Thread | Lessons | Approved | @cmo |
...

## Timeline
- T-7: Tease cascade (2-3 cryptic posts/platform)
- T-3: Influencer briefs sent + 1st creator teases
- T-1: Final asset polish + scheduling
- T-0: Launch (2-hr cascade window 14:00-16:00 UTC)
- T+1: First-day analytics check
- T+3: Reddit AMA
- T+7: UGC reposts + amplification refresh
- T+14: Retrospective

## Hashtag basket per platform
(see hashtag-strategy-trending-niche-branded for each)
- LinkedIn: [#summerdrop2026, #brand, #productlaunch, #saas]
- IG: 25-tag basket
- TikTok: [#summerdrop, #brand, #productlaunch, #trendingNow]

## Tracking
- UTM: utm_source/medium/campaign/content/term
- Attribution: PostHog + native platform analytics + Shopify referrer

## Budget
- Total: $50,000
- Channels: $20,000 organic (per-channel breakdown)
- Influencer: $20,000 (8 micro + 2 mid)
- Paid boost: $10,000 (Meta + TikTok)
```

### Recipe 2: T-7 teaser cascade

```bash
# 2-3 cryptic posts/platform over 7 days pre-launch
TEASES=(
  "Something's coming. Something we've been quietly building. June 18."
  "20 prototypes. 4 pivots. 1 product. Almost there."
  "If you're on this list, you'll hear it first: <email opt-in link>"
)

for i in "${!TEASES[@]}"; do
  DAY=$((6 - i))  # T-6, T-5, T-4
  mcp tool buffer.create_update \
    --channelIds '["linkedin_company","twitter","instagram","threads","tiktok"]' \
    --text "${TEASES[$i]}" \
    --channelData "$(per_channel_voice "${TEASES[$i]}")" \
    --scheduledAt "$(date -u -d "$DAY days, 14:00:00 UTC" +%Y-%m-%dT%H:%M:%SZ)"
done
```

### Recipe 3: T-3 influencer brief send

Inherit from `influencer-outreach-modash-aspire-grin`. T-3 brief send window:

```python
campaign = notion.get(campaign_db, 'summer_drop_2026')
creators = notion.query(creator_crm_db, filter={'Campaign': campaign['id'], 'Status': 'signed'})

for c in creators:
    brief = generate_creator_brief(campaign, c)
    mcp.gmail.send(
        to=c['Email'],
        subject=f"Brief — {campaign['Campaign']} — {c['Handle']}",
        body=brief
    )
    notion.update(c['id'], {'Brief sent': now(), 'Status': 'shipping'})
```

### Recipe 4: T-0 cascade execution

```bash
# 2-hour cascade window
mcp tool buffer.create_update \
  --channelIds '["linkedin_company","twitter","instagram","tiktok","threads","bluesky","facebook"]' \
  --text "$MAIN_POST_DEFAULT" \
  --channelData "$VARIANTS_JSON" \
  --mediaUrls "$MEDIA_PER_CHANNEL" \
  --scheduledAt "2026-06-18T14:00:00Z" \
  --needsApproval false  # pre-approved by T-1

# Stories / ephemeral content (separate from feed)
mcp tool insta_business.create_story \
  --account_id "$IG_BUSINESS_ID" \
  --media_url "$STORY_URL" \
  --link_sticker "$PRODUCT_URL"

# YouTube Community Post
mcp tool youtube.create_community_post \
  --channel_id "$YT_CHANNEL_ID" \
  --text "Launching today: <link>" \
  --image "$HERO_IMG"

# Reddit posts (no Buffer; native)
mcp tool reddit.submit_post --subreddit "Entrepreneur" \
  --title "We just shipped X — here's the story" \
  --selftext "$LAUNCH_BODY"
```

### Recipe 5: T+0 to T+1 monitoring

```python
# Real-time tracking hour-by-hour first 24 hrs
for hour in range(24):
    metrics = {}
    for ch in CHANNELS:
        analytics = mcp.buffer.get_update_analytics(channel=ch, since=launch_time)
        metrics[ch] = {
            'reach': analytics['reach'],
            'engagement': analytics['engagement'],
            'click_through': analytics['clicks']
        }
    
    # Conversion via PostHog
    sessions = mcp.posthog.query("""
        SELECT properties.utm_source, count(*) AS sessions, sum(properties.revenue) AS gmv
        FROM events WHERE event='purchase' AND timestamp > %s
        GROUP BY properties.utm_source
    """, launch_time)
    
    notion.upsert(campaign_metrics_db, {
        'Campaign': 'summer_drop_2026',
        'Hour': hour, 'Per-channel reach': metrics, 'Sessions': sessions
    })
    
    slack.post('#campaign-watch', f"Hour {hour}: total reach {sum(m['reach'] for m in metrics.values()):,} | GMV ${sum(s['gmv'] for s in sessions):,}")
    time.sleep(3600)
```

### Recipe 6: T+3 Reddit AMA

Hand to `reddit-strategy-ama-subreddit`:

```python
mcp.reddit_strategy.host_ama(
    subreddit='IAmA',
    title="Just launched X — founder AMA",
    body=AMA_INTRO,
    schedule_time=launch_time + 3*24*3600,
    seed_questions=PRE_PREPARED_QUESTIONS
)
```

### Recipe 7: T+1 to T+7 UGC discovery + amplification

```python
# Daily UGC sweep for campaign hashtag
for day in range(7):
    ugc = mcp.brand24.get_mentions(project_id=BRAND24_PROJECT_ID,
                                    keywords=[f'#{CAMPAIGN_HASHTAG}', f'#{BRAND_TAG}'],
                                    since=launch_time + day*24*3600)
    rights_pending = [m for m in ugc if m['Brand-fit'] >= 7 and not m['rights_granted']]
    for m in rights_pending:
        # Hand to ugc-reposting-policy-workflow
        mcp.ugc_workflow.request_rights(mention_id=m['id'], creator_handle=m['author'])
```

### Recipe 8: Mid-flight pivot detection

```python
# T+3 check: if KPI off-target by > 50%, pivot
kpi_status = notion.get(campaign_db, 'summer_drop_2026')['KPI status']
if kpi_status < 0.50:
    slack.post('#campaign-watch', f"⚠ Off-target at T+3: {kpi_status*100:.0f}% of pace")
    # Pivot options
    pivot_review = {
        'Top performing channel': identify_top_channel(),
        'Worst performing channel': identify_worst(),
        'Hashtag swap candidate': identify_hashtag_swap(),
        'Creator underperformance': identify_underperforming_creators(),
        'Paid amp budget reallocation': suggest_budget_shift()
    }
    notion.create(pivot_log_db, pivot_review)
```

### Recipe 9: T+14 retrospective

```python
def campaign_retro(campaign_id):
    c = notion.get(campaign_db, campaign_id)
    posts = notion.query(asset_db, filter={'Campaign': campaign_id, 'Status':'published'})
    
    retro = {
        'Campaign': campaign_id,
        'Duration_days': (c['End date'] - c['Start date']).days,
        'Total posts shipped': len(posts),
        'Total reach': sum(p['Performance']['reach'] for p in posts),
        'Total engagement': sum(p['Performance']['engagement'] for p in posts),
        'KPI target': c['KPI target'],
        'KPI actual': measure_kpi(c),
        'KPI ratio': measure_kpi(c) / c['KPI target'],
        'Budget spent': measure_spend(c),
        'ROI': (measure_kpi(c) - measure_spend(c)) / max(measure_spend(c), 1),
        'Top-3 posts by performance': top_3_posts(posts),
        'Worst-3 posts': worst_3_posts(posts),
        'Channel ROI': per_channel_roi(c),
        'Lessons': '<populate>'
    }
    notion.create(campaign_retro_db, retro)
    slack.post('#leadership', format_campaign_retro(retro))
```

### Recipe 10: Kill-criteria evaluation

```python
# T+7 check
if measure_kpi(c) / c['KPI target'] < c['Kill criteria']['ratio']:
    slack.post('#campaign-watch', f"""🛑 KILL CRITERIA HIT — {c['Campaign']}
KPI at {measure_kpi(c)/c['KPI target']*100:.0f}% of target.
Threshold: {c['Kill criteria']['ratio']*100:.0f}%.
Pausing organic + paid. Switch to post-mortem.""")
    pause_campaign(c['id'])
```

## Examples

### Example A: SaaS feature launch — 14-day campaign

```yaml
campaign: ai_lead_scoring_GA
objective: 200 new trial signups in 14 days
budget: $30,000 total
channels: [LinkedIn (60%), X (15%), Threads (5%), TikTok (10%), Reddit (5%), YouTube Shorts (5%)]

T-7: hand-picked customer testimonials, 3 X polls, 2 LinkedIn essays
T-3: customer beta-tester program reveals via Twitter Spaces
T-0:
  LinkedIn: 1500-word post + carousel (12 slides)
  X: 12-tweet thread + 3 quote-tweets
  TikTok: founder explainer 90s
  Threads: launch chain (5 posts)
  Reddit r/SaaS: launch thread "AMA on Thursday"
T+3: Reddit AMA + LinkedIn live event
T+7: customer-success story carousel + email-to-LinkedIn cross-promo
T+14: retrospective + plan next iteration

Result tracking: trial signups via UTM + PostHog
```

### Example B: D2C product drop — 21-day campaign

```yaml
campaign: summer_skincare_drop
objective: $500k GMV in 21 days
budget: $80,000 total
channels:
  TikTok: 30% (creator-led)
  IG: 25% (Reel + Story-driven shop)
  Pinterest: 15% (shop-pin discovery)
  Threads: 10%
  YouTube Shorts: 10%
  Reddit r/SkincareAddiction: 5% (10:1 community-to-promo)
  Email: 5% (inherited from marketing-agent)

T-7: 12 creator teasers (none branded yet)
T-3: founder LinkedIn post + first creator big-reveals
T-0: branded launch + 12 creator posts in 24-hr window
T+1-T+7: TikTok Shop GMV Max paid amp + UGC discovery
T+8-T+14: bestseller-promo cycle + retargeting
T+15-T+21: retention focus + email re-engagement
T+22: retro
```

### Example C: B2B event-driven (conference)

```yaml
campaign: dreamforce_2026
window: T-30 to T+14
T-30 to T-7: thought-leadership runway (CEO LinkedIn posts, founder X threads)
T-7 to T-1: booth tease, sponsorship reveal, conference-specific hashtag launch
T-0 (during conference): live-stream highlights, talk recap, attendee meetup
T+1 to T+7: full recap (LinkedIn post, X thread, Threads chain, Reddit r/saas)
T+8 to T+14: lessons + next-year preview
```

## Edge cases

### Channel collision
Buffer's schedule windows may collide with native MCPs scheduled independently. Use single source-of-truth (Notion campaign DB) to coordinate.

### Time-zone confusion
Buffer's UTC scheduling vs creator-local time. Always use UTC in Notion DB; convert for human review.

### Approval-lag at T-0
2-hr cascade window assumes pre-approval done by T-1. If approval slips, cascade window slides; sub-optimal posting times. Build T-2 review buffer.

### Creator under-delivery
If creator doesn't post by agreed time, fall through:
- Polite 24-hr DM nudge
- Direct fall-back content (pre-approved alternative)
- Escalate via `account-takeovers-creator-handoff` if pattern

### Hashtag death
Sometimes a campaign hashtag fails to gain traction (< 100 uses in T+3). Pivot:
- Combine with broader trending hashtag
- Influencer doubling (more creators using tag)
- Reframe in next-wave content

### Paid amp leakage
GMV-Max / Meta Ads boost some posts unpredictably. Track per-channel boost lift vs organic baseline. Adjust budget if one channel disproportionately wins.

### Reddit AMA timing
T+3 default may collide with mid-week Reddit cycles. Validate via subreddit moderation team and posting-time data.

### Campaign-hashtag squat / abuse
After launch, bad-actors may use hashtag for unrelated content. Monitor via Brand24; ignore unless brand-safety flag.

### Cross-platform UTM mishandling
Some platforms strip UTM (LinkedIn, IG in-app). Use Linktree / short-link redirect to capture before strip.

### Kill-criteria recovery
Sometimes ROI dips before recovering. Don't kill at T+3 if T+1 was high-noise; wait for T+7 signal.

### Influencer post timing collision
Multiple creators posting same hour = audience overlap saturated. Coordinate via shared calendar; stagger.

### Asset variant drift
Per-platform variants may drift from approved version mid-edit. Lock variant once approved; require re-approval on edit.

### Crisis during campaign
If `social-crisis-comms` triggers mid-campaign, pause organic cascade; recommit only after crisis resolved (or pivot campaign messaging).

### Multi-language campaign
For multi-region brand, per-language variant + per-language hashtag basket. `deepl-mcp` first-pass; native-speaker review.

### After-launch silence
Common: T+1 to T+3 organic spike, T+4 to T+7 dip. Plan amplification refresh (UGC, paid, influencer second-wave) for T+4.

### Long-tail conversion lag
Some campaigns convert weeks later. Don't kill on T+7 if KPI is multi-month consideration cycle. Adjust kill window.

## Sources

- **Buffer — best social media management tools**: https://buffer.com/resources/best-social-media-management-tools/
- **Sprout Social — campaign management**: https://sproutsocial.com/insights/social-media-campaigns/
- **Hootsuite — multi-platform campaign**: https://blog.hootsuite.com/multi-channel-marketing/
- **Buffer Developers API**: https://buffer.com/developers/api
- **Role.md "Multi-platform campaign playbook"**: T-7 / T-0 / T+7 framework
- **Role.md campaign brief template**
- **PostHog UTM attribution**: https://posthog.com/docs/data/utm-segmentation
