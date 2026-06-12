<!--
Source: https://ads-api.reddit.com/docs/v3/
Reddit Ads API + Reddit Conversion API. No public MCP yet — via cli-anything curl.
-->
# Reddit Ads — Subreddit Targeting + Conversion API — SKILL

Reddit Ads' signature lever is **subreddit targeting** — direct distribution to a hyper-engaged niche community. Conversion API (CAPI) is required for iOS signal recovery. This skill ships subreddit hunt → campaign create → CAPI server-side events end-to-end.

## When to use this skill

- **Niche-vertical DTC / SaaS** with strong subreddit presence (programming, gaming, hobbyist, health/wellness, finance).
- **Cold prospecting** to highly relevant audiences (small but converting).
- **Brand engagement** with Conversation Ads in comment threads.
- **Promoted Posts** for content distribution in target subreddits.
- **iOS signal recovery** via Reddit CAPI.

**Do NOT use this skill when:**
- Mass-market consumer (Reddit reach lower than Meta / TikTok / Google).
- B2B enterprise — LinkedIn ABM cheaper per qualified lead.
- Sensitive subreddits without moderator goodwill (don't burn the community).

## Setup

### Reddit Ads API access

```bash
# OAuth via Reddit Ads → Settings → API Access
export REDDIT_ACCESS_TOKEN="<oauth-token>"
export REDDIT_AD_ACCOUNT_ID="<a2_xxxxx>"
export REDDIT_PIXEL_ID="<pixel-id>"
export REDDIT_CAPI_TOKEN="<capi-server-token>"
```

### API base + key endpoints (v3)

- Base: `https://ads-api.reddit.com`
- Campaigns: `POST /api/v3/ad_accounts/{id}/campaigns`
- Ad groups: `POST /api/v3/ad_accounts/{id}/ad_groups`
- Ads: `POST /api/v3/ad_accounts/{id}/ads`
- Conversion API: `POST /api/v3/conversions/events`
- Reporting: `POST /api/v3/ad_accounts/{id}/reports`
- Custom Audiences: `POST /api/v3/ad_accounts/{id}/custom_audiences`

### Organic subreddit research via `reddit-mcp`

Before paid: identify 5-15 target subreddits with `reddit-mcp` (organic context tool):

```bash
mcp tool reddit.search_subreddits --query "indie hacker" --min_subscribers 5000
mcp tool reddit.get_subreddit_info --subreddit "sideproject"
# Look for: subscriber count > 5K, posts/day > 5, ICP language in top posts
```

## Common recipes

### Recipe 1: Subreddit-targeted campaign — Promoted Post

```bash
# Step 1: Campaign
curl -X POST "https://ads-api.reddit.com/api/v3/ad_accounts/$REDDIT_AD_ACCOUNT_ID/campaigns" \
  -H "Authorization: Bearer $REDDIT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "Cold-Niche-Subreddits-Q3",
      "objective": "CONVERSIONS",
      "configured_status": "PAUSED",
      "spend_cap": 100000,
      "funding_instrument_id": "'$FUNDING_ID'"
    }
  }'

# Step 2: Ad group with subreddit targeting
curl -X POST "https://ads-api.reddit.com/api/v3/ad_accounts/$REDDIT_AD_ACCOUNT_ID/ad_groups" \
  -H "Authorization: Bearer $REDDIT_ACCESS_TOKEN" \
  -d '{
    "data": {
      "name": "Subreddits-Tier1",
      "campaign_id": "'$CAMPAIGN_ID'",
      "configured_status": "ACTIVE",
      "bid_strategy_type": "AUTOBID",
      "goal_type": "PURCHASE",
      "goal_value": 10000,
      "start_time": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",
      "targeting": {
        "geolocations": ["US","CA","UK"],
        "communities": ["t5_2qh33","t5_2qh23","t5_2qhx4"],
        "devices": ["MOBILE","DESKTOP"],
        "interests": []
      },
      "bid_amount": 200,
      "daily_budget": 5000
    }
  }'

# Step 3: Ad — Promoted Post
curl -X POST "https://ads-api.reddit.com/api/v3/ad_accounts/$REDDIT_AD_ACCOUNT_ID/ads" \
  -H "Authorization: Bearer $REDDIT_ACCESS_TOKEN" \
  -d '{
    "data": {
      "name": "Promoted-V1-IndieHook",
      "ad_group_id": "'$AD_GROUP_ID'",
      "configured_status": "ACTIVE",
      "type": "IMAGE",
      "post_url": "https://reddit.com/r/'$YOUR_SUBREDDIT'/comments/'$POST_ID'/",
      "destination_url": "https://brand.com/lp?utm_source=reddit&utm_medium=paid&utm_campaign=cold-niche-q3&utm_content=v1-indiehook",
      "click_url": "https://brand.com/lp"
    }
  }'
```

### Recipe 2: Reddit Conversion API — server-side Purchase

```bash
curl -X POST "https://ads-api.reddit.com/api/v3/conversions/events" \
  -H "Authorization: Bearer $REDDIT_CAPI_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "events": [{
      "event_at": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",
      "event_type": {
        "tracking_type": "Purchase"
      },
      "event_id": "user123-purchase-'$(date +%s%3N)'",
      "click_id": "'$RDT_CID'",
      "event_metadata": {
        "value_decimal": 99.99,
        "currency": "USD",
        "item_count": 1,
        "products": [{
          "id": "sku-abc",
          "name": "Acme Widget",
          "category": "Tools"
        }]
      },
      "user": {
        "email": "'$EMAIL_SHA256'",
        "external_id": "'$USER_ID_SHA256'",
        "ip_address": "'$CLIENT_IP'",
        "user_agent": "'$USER_AGENT'",
        "screen_dimensions": {"width": 1920, "height": 1080}
      }
    }]
  }'
```

### Recipe 3: Custom Audience — hashed-email upload

```bash
# Step 1: Create audience
curl -X POST "https://ads-api.reddit.com/api/v3/ad_accounts/$REDDIT_AD_ACCOUNT_ID/custom_audiences" \
  -H "Authorization: Bearer $REDDIT_ACCESS_TOKEN" \
  -d '{
    "data": {
      "name": "Customer_List_Top_LTV_2026Q3",
      "type": "CUSTOMER_LIST"
    }
  }'

# Step 2: Add hashed users (SHA-256 of lowercased + trimmed email)
curl -X POST "https://ads-api.reddit.com/api/v3/ad_accounts/$REDDIT_AD_ACCOUNT_ID/custom_audiences/$AUD_ID/users" \
  -H "Authorization: Bearer $REDDIT_ACCESS_TOKEN" \
  -d '{
    "data": {
      "users": [
        {"hashed_email": "'$EMAIL_HASH_1'"},
        {"hashed_email": "'$EMAIL_HASH_2'"}
      ]
    }
  }'
```

### Recipe 4: Conversation Ads — comment-thread placement

```bash
curl -X POST "https://ads-api.reddit.com/api/v3/ad_accounts/$REDDIT_AD_ACCOUNT_ID/ads" \
  -H "Authorization: Bearer $REDDIT_ACCESS_TOKEN" \
  -d '{
    "data": {
      "name": "Conversation-V1",
      "ad_group_id": "'$AD_GROUP_ID'",
      "type": "CONVERSATION",
      "configured_status": "ACTIVE",
      "post_url": "https://reddit.com/r/'$YOUR_SUBREDDIT'/comments/'$POST_ID'/",
      "destination_url": "https://brand.com/lp"
    }
  }'
```

### Recipe 5: Subreddit ID lookup

```bash
# Reddit's "communities" field expects subreddit fullnames (t5_<id>)
# Lookup via Reddit API:
curl "https://oauth.reddit.com/r/sideproject/about" \
  -H "Authorization: Bearer $REDDIT_USER_TOKEN" \
  -H "User-Agent: AdsAgent/1.0" | jq '.data.name'
# Returns "t5_2qhx4"
```

### Recipe 6: Reporting — last-7d performance

```bash
curl -X POST "https://ads-api.reddit.com/api/v3/ad_accounts/$REDDIT_AD_ACCOUNT_ID/reports" \
  -H "Authorization: Bearer $REDDIT_ACCESS_TOKEN" \
  -d '{
    "data": {
      "breakdowns": ["AD_ID","DATE"],
      "fields": ["SPEND","IMPRESSIONS","CLICKS","CTR","CPC","CONVERSIONS","ROAS"],
      "starts_at": "'$(date -u -d "-7 days" +%Y-%m-%d)'",
      "ends_at": "'$(date -u +%Y-%m-%d)'",
      "time_zone_id": "America/Los_Angeles"
    }
  }' | jq '.data.reports[]'
```

### Recipe 7: Subreddit performance breakdown

```bash
curl -X POST "https://ads-api.reddit.com/api/v3/ad_accounts/$REDDIT_AD_ACCOUNT_ID/reports" \
  -H "Authorization: Bearer $REDDIT_ACCESS_TOKEN" \
  -d '{
    "data": {
      "breakdowns": ["AD_GROUP_ID","COMMUNITY"],
      "fields": ["SPEND","CONVERSIONS","COST_PER_CONVERSION","ROAS"],
      "starts_at": "'$(date -u -d "-30 days" +%Y-%m-%d)'",
      "ends_at": "'$(date -u +%Y-%m-%d)'"
    }
  }'
```

Use this to identify which subreddits drive conversions vs which just spend.

## Examples — niche DTC SaaS launch

```yaml
audience_research:
  primary_subreddits:
    - r/sideproject (94K subs, 3 posts/day, indie hackers)
    - r/SaaS (190K subs, builder-buyer audience)
    - r/Entrepreneur (4.2M subs, broad)
    - r/smallbusiness (2.1M subs, ICP overlap)
    - r/digitalnomad (2.0M subs, lifestyle match)
  exclude:
    - r/StartupBusiness (low engagement)
    - r/marketing (heavy self-promo noise)

campaigns:
  cold_subreddit:
    name: "Cold-Niche-Sub-Q3"
    budget: $100/day
    targeting:
      communities: [t5_sideproject, t5_saas, t5_entrepreneur, t5_smallbusiness]
      geolocations: ["US","CA","UK","AU"]
    bid: AUTOBID with goal_type CONVERSIONS
    creative: Reddit-native post (text + image), no salesy CTA
  
  retargeting:
    name: "Hot-Site-Visitor"
    budget: $40/day
    targeting:
      custom_audiences: [site_visitors_30d]
      exclusion: [customer_list]
    creative: case study / testimonial format
```

## Edge cases

### Subreddit ID encoding
Use `t5_<id>` (the "fullname") not the subreddit's display name. Look up via Reddit JSON API or community tools.

### Native-style creative wins
Reddit users hate ads that feel like ads. Use text-heavy, no-stock-photo, conversational copy. Hire native Reddit copywriters or repurpose your own organic Reddit posts.

### Subreddit moderator goodwill
Some subreddits ban brand promotion outright. Lurk first, contribute organically, then ad-promote. Burning a subreddit's goodwill kills your reach forever.

### Minimum spend / bid
Daily budget min $5. AUTOBID floors at ~$0.50 CPC for most verticals; expect $1.50-$5 typical CPC.

### Conversion event lookback
Reddit defaults 7-day-click + 1-day-view. Configure via `attribution_setting` per campaign if needed.

### Click ID handling
`rdt_cid` cookie set by pixel; pass through to server side for CAPI event match. Without it, deterministic attribution drops.

### Frequency / fatigue
Reddit users see the same ad in feed repeatedly within a session. Set a sane frequency cap via `frequency_cap_lifetime` (e.g., 5 / 7d).

### CAPI dedup
`event_id` shared between pixel + CAPI events deduplicates. Without it, double-counting inflates reported conversions 30-50%.

### Verticals frequently rejected
Heavy promotion of crypto / gambling / supplements may be policy-blocked. Pre-review with Reddit ads team.

### Audience overlap with Meta
Customer Match / interest overlap with Meta Custom Audience is high. Use exclusions to avoid double-burning.

## Sources

- Reddit Ads API v3 docs: https://ads-api.reddit.com/docs/v3/
- Reddit Conversion API: https://ads-api.reddit.com/docs/v3/#tag/Conversions
- Targeting reference (communities, interests): https://business.reddithelp.com/s/article/targeting-with-reddit-ads
- Reddit Pixel install: https://ads.reddit.com/help/c/pixel
- Campaign objectives: https://business.reddithelp.com/s/article/campaign-objectives
- Custom Audiences: https://ads.reddit.com/help/c/custom-audiences
