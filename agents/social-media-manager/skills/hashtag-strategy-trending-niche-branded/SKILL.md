<!--
Source: https://www.tiktok.com/business/creativecenter/inspiration/popular/hashtag
Brand24 hashtag tracking: https://brand24.com/blog/hashtag-tracking/
RiteTag: https://ritetag.com/
Role.md "Hashtag basket spec"
-->
# Hashtag Strategy — Trending + Niche + Branded + Community — SKILL

Build platform-specific 30-tag baskets (5 trending + 15 niche + 5 branded + 5 community for Instagram, 3-5 total for TikTok / LinkedIn / X). Pull trending from TikTok Creative Center + Brand24 co-occurrence. Never repeat the same basket twice in a week (algorithmic-pattern flag).

## When to use this skill

- **Pre-publish hashtag set** for any IG / TikTok / LinkedIn / X / Threads post.
- **Campaign hashtag launch** — branded hashtag with companion baskets.
- **Hashtag refresh** — weekly rotation per role.md "Never repeat the same basket twice in a week".
- **Hashtag performance audit** — which tags drove reach in last 30 days.

**Do NOT use this skill when:**
- Reddit — no hashtags, subreddit choice is the discovery vector.
- Trend monitoring (sounds, formats, broad cultural trends) — `social-trend-monitoring-tiktok-sounds-reels`.

## Setup

### TikTok Creative Center (public, no key)

```bash
# Trending hashtags scraper
curl -s "https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en" \
  -H "User-Agent: Mozilla/5.0" \
  | python parse_creative_center.py
```

Or via `brave-search` / `firecrawl-mcp` for structured pull. Or Apify `clockworks/tiktok-trending` actor (paid, $0.01-0.05/run).

### Brand24 hashtag co-occurrence

```bash
export BRAND24_API_KEY="<key>"
export BRAND24_PROJECT_ID="<id>"
mcp tool brand24.get_co_occurrence --project_id "$BRAND24_PROJECT_ID" --tag "#yourbrand" --period "30d"
```

### Notion Hashtag DB

Columns: `Tag / Platforms (multi-select) / Category (trending/niche/branded/community) / Reach last 30d / Engagement rate last 30d / Last used / Performance score / Status (active/cooling/banned)`.

### RiteTag (cross-platform suggestions, optional)

```bash
export RITETAG_KEY="<key>"
curl "https://api.ritetag.com/v2/auto?postText=Your+post+text" \
  -H "Authorization: Bearer $RITETAG_KEY"
```

## Common recipes

### Recipe 1: Instagram 25-tag basket builder

```python
def build_ig_basket(topic, brand_tags, count=25):
    trending = fetch_trending_tiktok(region='US', limit=10)
    trending_relevant = [t for t in trending if relevance_score(t, topic) > 0.5][:5]
    
    niche = fetch_niche_tags(topic, range_min=10_000, range_max=500_000, limit=15)
    
    branded = brand_tags[:5]  # #yourbrand, #yourbrandCampaign, etc.
    
    community = COMMUNITY_BANK.get(topic_category(topic), [])[:5]
    # e.g. fitness → ['#fitfam', '#fitlife', '#workoutmotivation', '#fitnessjourney', '#getfit']
    
    basket = trending_relevant + niche + branded + community
    return basket[:count]
```

### Recipe 2: TikTok 4-tag basket (3-5 total)

```python
def build_tiktok_basket(topic, brand_tag):
    # 1 trending TikTok Creative Center top 20 last 7 days
    trending = top_trending_tiktok(region='US', period='7d')[0]
    
    # 1-2 niche
    niche = fetch_niche_tags(topic, range_min=10_000, range_max=500_000, limit=2)
    
    # 1 branded
    branded = [brand_tag]
    
    # 0-1 challenge / community if relevant
    challenge = relevant_challenge(topic) if challenge_active(topic) else None
    
    basket = [trending] + niche + branded + ([challenge] if challenge else [])
    # NEVER include #fyp — TikTok algorithm ignores it (per role.md)
    return basket[:4]
```

### Recipe 3: LinkedIn 3-5 tag basket

```python
def build_linkedin_basket(topic, brand_tag):
    industry = INDUSTRY_TAGS.get(topic_industry(topic), [])[:2]  # ['#marketing','#saas']
    niche_pro = fetch_professional_niche(topic, limit=2)         # ['#contentstrategy','#b2bsaas']
    branded = [brand_tag]
    return industry + niche_pro + branded
```

### Recipe 4: X 1-2 tag basket

```python
def build_x_basket(topic, brand_tag, has_active_campaign=False):
    primary = high_relevance_tag(topic)
    if has_active_campaign:
        return [primary, brand_tag]
    return [primary]
```

### Recipe 5: Niche-tag discovery (sweet spot 10k-500k uses)

```python
def fetch_niche_tags(topic, range_min, range_max, limit):
    # Brand24 co-occurrence with brand mentions
    co = brand24.get_co_occurrence(project_id=BRAND24_PROJECT_ID, tag=f'#{topic}', period='30d')
    candidates = [c for c in co if range_min <= c['volume'] <= range_max]
    return sorted(candidates, key=lambda x: -x['relevance'])[:limit]
```

### Recipe 6: Branded-hashtag campaign launch

```bash
# 1. Reserve campaign hashtag
# Check current usage to avoid collision
curl -s "https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/?keyword=$CAMPAIGN_TAG"
# Also check Brand24 mention search for last 90 days

# 2. Create Brand24 monitoring project for the tag
curl -X POST https://api.brand24.com/v3/projects \
  -H "Authorization: Bearer $BRAND24_API_KEY" \
  -d "{\"name\":\"$CAMPAIGN_TAG monitoring\",\"keywords\":[\"$CAMPAIGN_TAG\"]}"

# 3. Seed: post + influencer drops + UGC contest with the tag
# 4. Track: daily Brand24 volume + sentiment + top creators using
```

### Recipe 7: Weekly basket rotation (anti-pattern detection avoidance)

```python
# Per platform, track last-3-basket history; ensure no 3+ exact-match repeats
def get_next_basket(platform, topic, last_baskets):
    candidate = build_basket(platform, topic)
    overlap = set(candidate) & set(last_baskets[-1])
    if len(overlap) / len(candidate) > 0.7:
        # Force diversification
        candidate = swap_30pct(candidate, replacements=fetch_trending_tiktok())
    return candidate
```

### Recipe 8: Hashtag performance audit (30-day rolling)

```python
# Pull per-tag reach + engagement from native analytics + Brand24
for tag in active_tags:
    posts_using = ig_business.search_posts(tag=tag, limit=30)
    avg_reach = mean(p['reach'] for p in posts_using)
    avg_er = mean(p['engagement_rate'] for p in posts_using)
    notion.upsert_page(hashtag_db, {'Tag': tag,
        'Reach last 30d': avg_reach,
        'Engagement rate last 30d': avg_er,
        'Performance score': compute_score(avg_reach, avg_er),
        'Last used': last_use_date(tag)
    })

# Top 20% retire never; bottom 20% cool down 2 weeks
```

### Recipe 9: Community tag bank (per niche)

```python
COMMUNITY_BANK = {
    'fitness':   ['#fitfam', '#fitlife', '#workoutmotivation', '#fitnessjourney', '#getfit'],
    'food':      ['#foodie', '#foodporn', '#instafood', '#foodphotography', '#yum'],
    'beauty':    ['#beautyblogger', '#makeupaddict', '#beautygram', '#mua', '#beautycommunity'],
    'gaming':    ['#gamer', '#gamingcommunity', '#twitchstreamer', '#esports', '#gameplay'],
    'saas':      ['#saascommunity', '#buildinpublic', '#indiehackers', '#productivity', '#nocode'],
    'pets':      ['#catsofinstagram', '#dogsofinstagram', '#petstagram', '#fluffy', '#adoptdontshop'],
    'fashion':   ['#ootd', '#fashionblogger', '#styleinspo', '#streetstyle', '#sustainablefashion'],
    'travel':    ['#travelgram', '#wanderlust', '#instatravel', '#travelphotography', '#travelblogger'],
}
```

### Recipe 10: Anti-pattern checks

```python
BLACKLIST = [
    '#followforfollow', '#likeforlike', '#l4l', '#f4f', '#instafollow',
    '#fyp',  # TikTok algorithm explicitly ignores
    '#shadowban', '#instagood',  # too generic to discover; saturated
]
def check_basket(basket):
    bad = set(basket) & set(BLACKLIST)
    if bad: raise ValueError(f"Blacklist hits: {bad}")
    if len(basket) != len(set(basket)): raise ValueError("Duplicates in basket")
    return True
```

## Examples

### Example A: Fitness brand IG post on Tuesday

```python
topic = 'home workout 20 min full body'
brand_tags = ['#powerbrand', '#powerbrandcommunity', '#powerbrandHQ']

basket = build_ig_basket(topic, brand_tags, count=25)
# Output (one possible draft):
# trending: ['#summerfitchallenge', '#15minworkout', '#mobilityjune', '#powermoves26', '#fitafter40']
# niche:    ['#homeworkout', '#hiit', '#bodyweighttraining', '#dumbbellworkout', '#functionalfitness',
#            '#progressiveoverload', '#fullbodyworkout', '#workoutathome', '#fitnessmotivation',
#            '#trainerlife', '#programdesign', '#hypertrophy', '#metcon', '#mobility', '#deload']
# branded:  ['#powerbrand', '#powerbrandcommunity', '#powerbrandHQ', '#PB20min', '#PBmoves']
# community:['#fitfam', '#fitlife', '#workoutmotivation', '#fitnessjourney', '#getfit']
```

### Example B: Branded campaign hashtag launch

```yaml
campaign: pb_summer_strength_2026
hashtag: '#PBSummerStrong'
launch:
  T-7: monitor with Brand24 project to baseline (typically zero)
  T-3: 3 influencers tease the tag in Stories
  T-0: brand post uses + first creator drops
  T+1 to T+7: UGC reposts using the tag with 80/20 attribution
  T+14: retrospective — total uses, top creators, conversions
```

### Example C: Hashtag-mix recommendation per platform from a single brief

```yaml
brief: "Promoting our new B2B SaaS feature: AI lead scoring"
recommended_baskets:
  linkedin: ['#b2bsaas', '#leadgeneration', '#salestech', '#powerbrand', '#aileadscoring']
  x: ['#salestech', '#powerbrand']
  threads: ['#saas', '#salestech', '#powerbrand']
  instagram_business: [25-tag basket with mix]
  tiktok_business: ['#salestips', '#salestech', '#powerbrand', '#leadgenstrategies']
```

## Edge cases

### Tag volume vs reach
1B+ usage = saturated; your post lost. 1M-50M = sweet spot. 10k-500k = niche-discovery gold.

### Banned / restricted hashtags
IG silently shadow-bans some tags (e.g. #sundayfunday at times). Check via IG hashtag search — if recent posts hidden, tag is restricted. Brand24 also flags.

### Algorithm changes
TikTok claimed in 2024 that #fyp does nothing; reaffirmed 2026. Don't include. IG / LinkedIn don't have explicit banned-from-discovery tags but penalize spammy patterns.

### Trending tag relevance
A tag trending for unrelated topic isn't help. Always filter trending by relevance to topic (Recipe 1's `relevance_score`).

### Hashtag in comment vs caption (Instagram)
Same algorithmic value either place. Comment placement keeps caption cleaner; cohort of accounts test both. Pick one convention and stick.

### Cross-platform tag reuse
A tag that works on IG may be silent on LinkedIn (#fitlife). Always build per-platform basket; don't copy IG basket to LinkedIn.

### Branded-tag squatting
Before launching `#campaign`, verify no existing high-volume off-topic usage. Common collisions: generic two-word combos. Pick something brand-specific.

### Hashtag fatigue
Same 25-tag basket weekly = algorithm pattern flag. Rotate 30% / week. Track in Notion `Last used` column.

### Reach-vs-engagement tradeoff
Trending tags drive reach but low engagement rate (many drive-by viewers). Niche tags drive higher engagement. Balance per campaign goal — awareness leans trending, conversion leans niche.

### Influencer-spec hashtags
If creator drops a campaign post, mandate the branded campaign tag + #ad / #sponsored. Disclosure tag is non-negotiable (FTC).

### Hashtag SEO on TikTok
TikTok now uses hashtag + caption keyword for in-search ranking. Caption keyword > hashtag for SEO. Don't load all weight on hashtags.

### Hashtag SEO on LinkedIn
LinkedIn 2026: hashtags weakly influence discovery vs. comment + reaction engagement. Use 3-5 hashtags as supplementary; don't stuff.

### Multi-language tags
Brand on US + Spain + Brazil: separate baskets per market. `#fitlife` (en) ≠ `#vidafit` (es) audience.

### Hashtag analytics gaps
Native IG / TikTok analytics show per-post reach attributed to hashtags only at top-tier business plans. Use Brand24 / Hootsuite for cross-tag reach attribution.

## Sources

- **TikTok Creative Center — popular hashtags**: https://www.tiktok.com/business/creativecenter/inspiration/popular/hashtag
- **Brand24 — hashtag tracking**: https://brand24.com/blog/hashtag-tracking/
- **RiteTag**: https://ritetag.com/
- **Hashtagify**: https://hashtagify.me/
- **Role.md "Hashtag basket spec"**: per-platform 30-tag composition
- **Sprout Social — hashtag strategy 2026**: https://sproutsocial.com/insights/hashtag-strategy/
- **Apify TikTok Trending Hashtags**: https://apify.com/clockworks/tiktok-trending
