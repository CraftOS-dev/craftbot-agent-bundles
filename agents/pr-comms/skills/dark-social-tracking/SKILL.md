<!--
Source: https://sparktoro.com/blog/audience-research-tools/
SparkToro: https://sparktoro.com/
Common Room: https://www.commonroom.io/
Discord MCP: discord-mcp-full
role.md SOTA tool reference (dark social): internal
-->
# Dark Social Tracking — SparkToro + Common Room + Discord/Slack Communities — SKILL

Dark social = brand conversations happening in channels that don't show up in standard mention monitoring: Slack/Discord communities, private Substack threads, podcast in-show shoutouts, WhatsApp/Telegram groups, LinkedIn DMs, share-via-copy-link traffic. SparkToro for audience attribution, Common Room for community-led signal capture, `discord-mcp-full` for permitted server monitoring, `firecrawl-mcp` + `youtube-mcp-transcript` for podcast/video shoutouts.

## When to use this skill

- **PR attribution gap** — coverage exists but referral traffic is "Direct" in analytics; need to find where the link is being shared.
- **Audience hangouts research** — pre-pitch question: where do our buyers actually talk? (Slack groups / Discords / podcasts / Substacks).
- **Community-led signal capture** — Common Room aggregates intent signals from members across Slack/Discord/GitHub/X/LinkedIn.
- **Pre-launch buzz audit** — is the product being whispered about in private channels before launch?
- **Crisis early warning** — many crises start in Discord/Slack before they hit Twitter/Reddit/press.
- **Influencer + podcast discovery** — find category podcasts + LinkedIn voices via SparkToro behavioral data.

**Do NOT use this skill when:**
- Monitoring is public-only (news/blog/social) — use `brand-reputation-monitoring-brandwatch-meltwater`.
- You're tracking public Reddit/HN — use `reddit-hn-ama-show-and-tell`.
- The community is yours and you want analytics on it — defer to `community-agent` (if exists) or product analytics.

## Setup

### SparkToro API + UI

```bash
# https://sparktoro.com — $50-$225/mo plans. Free 5-search/mo tier.
# Audience research: "people who follow X also follow / read / listen to / hang out at..."
export SPARKTORO_API_KEY="<key>"
export SPARKTORO_API_BASE="https://api.sparktoro.com/v2"
```

SparkToro indexes ~120M social profiles + cross-references followed accounts, websites visited, podcasts listened to, hashtags used, YouTube channels watched. The default attribution-research tool for dark-social discovery.

### Common Room API

```bash
# https://www.commonroom.io — community-led growth platform. Plans start ~$0 free → enterprise.
# Aggregates Slack + Discord + GitHub + X + LinkedIn + Reddit + product activity per member.
export COMMONROOM_API_KEY="<key>"
export COMMONROOM_API_BASE="https://api.commonroom.io/community/v1"
```

Common Room identifies who in your community is showing intent signals (visited pricing, asked about a feature, shared a competitor's blog) — bridges dark-social conversation to identified contact.

### Discord MCP

```bash
# discord-mcp-full already in agent.yaml
# Requires bot token + invitation to each server you monitor
export DISCORD_BOT_TOKEN="<token>"
```

Only monitors servers where you've been invited as a member or bot. Do NOT scrape private servers without permission.

### Slack monitoring

```bash
# Slack has NO public scraping API. Options:
# 1. Be invited to the community Slack + use a bot user with read scope
# 2. Common Room ingests Slack workspaces you've connected
# 3. Manual: members of the team report mentions back to comms
```

### Notion dark-social DB schema

Per signal:
- `signal_id` (text, dedup)
- `source_type` (select: discord, slack, podcast_shoutout, substack_dm, linkedin_dm, share_via_copy, sparktoro, common_room)
- `community_name` (text)
- `channel_or_thread` (text)
- `date_observed` (datetime)
- `signal_strength` (select: weak, medium, strong)
- `mentioned_by` (text — username/handle)
- `mention_context` (rich text)
- `permission_to_engage` (checkbox — server rules permit DM)
- `commonroom_member_id` (text, optional)
- `attribution_link` (URL — back to product/blog)
- `action_taken` (select: none, public_reply, dm_outreach, internal_note, crisis_escalate)

## Common recipes

### Recipe 1: SparkToro audience research for dark-social discovery

```bash
# "Where do people who follow @CompetitorX actually hang out?"
curl "$SPARKTORO_API_BASE/audience-search" \
  -H "Authorization: Bearer $SPARKTORO_API_KEY" \
  -d '{
    "filters": [
      {"type": "follows", "value": "@CompetitorX"},
      {"type": "follows", "value": "@CategoryThoughtLeader"}
    ],
    "results": [
      "podcasts", "youtube_channels", "websites_visited",
      "subreddits", "hashtags", "newsletter_subscriptions"
    ],
    "min_overlap_pct": 5
  }' \
| jq '{
    top_podcasts: .podcasts[0:20],
    top_youtube: .youtube_channels[0:20],
    top_subreddits: .subreddits[0:20],
    top_newsletters: .newsletters[0:20]
  }' > sparktoro_audience.json
```

Feed into `notion-mcp` audience-research DB. Top podcasts become podcast-tour targets (hand off to `podcast-tour-booking-for-execs`). Top subreddits become AMA targets. Top newsletters become op-ed / sponsored-mention targets.

### Recipe 2: SparkToro behavioral influencer discovery

```bash
# Find category-relevant micro-influencers (5-50K followers, high engagement)
curl "$SPARKTORO_API_BASE/influencer-search" \
  -H "Authorization: Bearer $SPARKTORO_API_KEY" \
  -d '{
    "topic": "developer tooling AI",
    "follower_range": [5000, 50000],
    "engagement_min": 0.03,
    "platforms": ["twitter", "linkedin", "youtube"],
    "limit": 100
  }' \
| jq '.influencers[] | {
    handle, platform, follower_count, engagement_rate,
    bio, recent_posts_snippet, audience_overlap_with_brand
  }' > microinfluencers.json
```

Pair with `twitter-mcp` / `linkedin` outreach (hand off to thought-leadership skill).

### Recipe 3: Common Room intent signal pull

```bash
# Pull members who showed intent signals in last 7 days
curl "$COMMONROOM_API_BASE/members/activities?\
period=7d&\
activity_types=visited_pricing,asked_about_competitor,shared_company_link,joined_relevant_channel" \
  -H "X-API-Key: $COMMONROOM_API_KEY" \
| jq '.results[] | {
    member_id, name, email, company,
    signal_type, signal_strength, signal_context,
    source_platform: .source,
    last_active
  }' > intent_signals.json

# Sync to Notion + alert sales on strong signals
jq -c '.[]' intent_signals.json | while read m; do
  strength=$(echo "$m" | jq -r '.signal_strength')
  if [ "$strength" = "strong" ]; then
    slack-mcp send --channel "#sales-intent" \
      --text "Strong signal: $(echo $m | jq -r '.name') ($(echo $m | jq -r '.company')) — $(echo $m | jq -r '.signal_context')"
  fi
  notion-mcp create_page --db dark_social_signals --properties "$m"
done
```

### Recipe 4: Common Room community-led signal capture

```bash
# Common Room "Signals" — flag when members from target accounts engage
curl "$COMMONROOM_API_BASE/signals/configure" \
  -H "X-API-Key: $COMMONROOM_API_KEY" \
  -d '{
    "name": "Tier-1 prospect Slack activity",
    "filters": {
      "company_in": ["Acme Co", "Beta Inc", "Gamma LLC"],
      "channels": ["our-public-slack", "our-discord"],
      "activity": ["post", "react", "share_link"]
    },
    "alert_webhook": "https://alerts.us.example.com/commonroom"
  }'
```

Webhook handler pushes to `slack-mcp` + `notion-mcp` dark-social DB.

### Recipe 5: Discord community monitoring (permitted servers only)

```python
# discord-mcp-full — only on servers you're invited to
# Daily cron: pull brand-keyword mentions across permitted servers

permitted_servers = [
    "TechCommunity-Discord",
    "AISaaSFounders-Discord",
    "DevTools-Discord",
]

brand_keywords = ["Acme", "Acme product", "our-product-name"]

for server in permitted_servers:
    for kw in brand_keywords:
        results = discord_mcp.search_messages(
            server=server,
            query=kw,
            since="24h"
        )
        for msg in results:
            # Classify signal strength
            strength = classify_signal(msg.content, kw)
            notion_mcp.create_page(
                db="dark_social_signals",
                properties={
                    "source_type": "discord",
                    "community_name": server,
                    "channel_or_thread": msg.channel.name,
                    "date_observed": msg.timestamp,
                    "signal_strength": strength,
                    "mentioned_by": msg.author.username,
                    "mention_context": msg.content[:500],
                    "permission_to_engage": check_server_dm_rules(server),
                }
            )
```

### Recipe 6: Podcast shoutout discovery

```bash
# Many brand conversations happen mid-podcast and never get tagged
# Pull transcripts of category-relevant podcasts, search for brand mentions

category_podcasts=$(jq -r '.top_podcasts[].rss_url' sparktoro_audience.json)

for podcast_rss in $category_podcasts; do
  # Get last 5 episodes
  episodes=$(curl "$podcast_rss" | xq -x '//item/enclosure/@url' | head -5)
  for ep_url in $episodes; do
    transcript=$(youtube-mcp-transcript fetch --url "$ep_url" 2>/dev/null \
      || firecrawl-mcp scrape "$ep_url" --include-audio-transcript)
    
    for kw in "Acme" "our-product"; do
      if echo "$transcript" | grep -qi "$kw"; then
        context=$(echo "$transcript" | grep -B 2 -A 2 -i "$kw" | head -5)
        notion-mcp create_page --db dark_social_signals \
          --properties "{
            source_type: 'podcast_shoutout',
            community_name: '$podcast_rss',
            mention_context: '$context',
            signal_strength: 'medium'
          }"
      fi
    done
  done
done
```

### Recipe 7: Share-via-copy-link attribution via UTM + PostHog

```bash
# "Direct" traffic in analytics = dark social share-via-copy
# Auto-tag all owned links with UTM + use PostHog session replay to identify pattern

# Add UTM to every press release / blog URL
canonical_url="https://acme.com/blog/launch-x"
tagged_url="${canonical_url}?utm_source=share&utm_medium=darksocial"

# PostHog: pull sessions where landing_page = tagged_url AND referrer = ""
# These are dark-social shares
posthog-mcp query --filter "
  event = '\$pageview' AND
  properties.\$current_url contains 'utm_medium=darksocial' AND
  properties.\$referrer = ''
" --since "7d"
```

### Recipe 8: SparkToro vs Common Room workflow

```yaml
sparktoro_use_cases:
  - audience research (where do X buyers hang out?)
  - influencer discovery (who do X buyers follow?)
  - pre-launch channel selection (which podcasts/newsletters reach X?)
  - competitive audience analysis (CompetitorX audience overlap with us?)

common_room_use_cases:
  - identified-member signal capture (who in our community showed intent?)
  - source-aggregation (Slack + Discord + GitHub + X + LinkedIn unified view)
  - intent scoring per member
  - sales/PR hand-off (warm intro request when target-account member engages)

combination_pattern:
  - sparktoro discovers where the audience hangs out
  - we join those communities (Discord/Slack)
  - common room ingests those communities  
  - common room flags identified intent signals
  - pr/sales engage warmly
```

## Examples — full dark-social monitoring program

```yaml
day_1_setup:
  - sparktoro account; run initial audience research for top 3 competitors
  - common room account; connect company Slack + Discord
  - discord-mcp-full bot invited to top 10 category Discords (with mod permission)
  - notion dark-social DB initialized with schema
  - posthog UTM tagging on all owned share links
  - weekly cron: sparktoro re-pulls audience snapshot (track drift)

daily_cadence:
  - 0800 ET: discord-mcp pull from permitted servers (24h window)
  - 0900 ET: common room webhook digest (any signals overnight)
  - 1000 ET: claude classify signal strength + dedupe
  - 1100 ET: strong signals → slack-mcp #pr-dark-social channel
  - 1700 ET: end-of-day summary to comms team

weekly_cadence:
  - mon 0900: SparkToro behavioral re-check (new podcasts/newsletters in category)
  - wed 1400: dark-social digest to PR lead (top conversations, sentiment, action items)
  - fri 1500: hand-off list to sales for warm intent signals

monthly_cadence:
  - sparktoro audience overlap re-run vs 3 competitors
  - common room "intent signal source" ROI: which sources produced most converted contacts
  - prune low-value community monitoring (drop Discord servers with 0 signals/month)
```

## Edge cases

### Permission discipline on private communities
NEVER scrape private Slack / Discord / WhatsApp without explicit permission. Trust + relationships are the value; one violation kills future access. Discord ToS + Slack ToS prohibit unauthorized scraping. Common Room ingests workspaces only with admin connection consent.

### Dark social is unattributed by design
The whole premise: people share via copy-link, DM, private channel. Analytics shows "Direct" traffic. Don't try to perfectly attribute; estimate via SparkToro audience research + UTM-tagged owned-link campaigns + PostHog session-replay sampling.

### SparkToro snapshot lag
SparkToro audience data refreshes ~quarterly. Use for strategic direction, not real-time decisions. Combine with `twitter-mcp` real-time monitoring for trending signals.

### Common Room sales-PR overlap
Common Room signals are valuable to both PR (community advocacy, AMA-able members) and sales (warm-intent identified contacts). Route by signal type: `signal_context contains "asked_about_competitor" OR "visited_pricing"` → sales. `signal_context contains "shared_content" OR "joined_relevant_channel"` → PR/community.

### Podcast shoutout volume
Podcast transcripts are noisy. Brand mention in a 60-minute episode might be a 5-second drive-by. Weight by context: "X is the only one solving Y" vs "I think we use X for invoicing" — wildly different signal value. Claude classification helps.

### Discord server ToS varies
Each Discord server has its own rules + culture. Mod outreach before any bot deployment. Some categories (web3, gaming, AI) are bot-tolerant; others (private communities, support groups) are not. Read the rules before joining.

### Crisis early-warning signals from dark social
Many crises (security incident, exec controversy, feature backlash) start in Discord/Slack 24-72h before hitting Twitter/Reddit/press. Configure Common Room + `discord-mcp-full` for crisis-keyword alerts (incident, breach, broken, scam, lawsuit, fired). Hand off to `crisis-comms-24-48-72-hour-playbook` if signals correlate.

### Substack DM + email reply tracking
Substack offers DM thread + comment + email reply data via dashboard. No public API. Manual review of high-engagement comment threads + DM list weekly. Add insights to dark-social DB.

### LinkedIn DM monitoring
LinkedIn DMs are technically dark social — and there's no DM API. Manually log noteworthy mentions (received from sales/PR/exec team). Look for patterns (recurring topics, recurring senders).

### WhatsApp + Telegram groups
WhatsApp Business API exists but doesn't expose group messages. Telegram has group-bot APIs but ToS-sensitive. Generally: be invited as member, manually log mentions, do not bot-scrape.

### SparkToro vs Audiense vs SimilarWeb (alternates)
- **SparkToro** — best for cross-platform behavioral audience (followers + listens + reads + visits).
- **Audiense** — best for Twitter-only psychographic segmentation.
- **SimilarWeb** — best for web traffic + referral source attribution.

Default to SparkToro for dark-social research. Audiense if Twitter is the primary audience. SimilarWeb for paid-attribution gap-filling.

### Common Room is identified, SparkToro is anonymized
- Common Room → "Jane Doe at Acme Co engaged in our community channel."
- SparkToro → "people in your audience hang out in r/SaaS / listen to TechPod / follow @ThoughtLeader."

Use Common Room for sales/PR routing; SparkToro for strategy.

### Hand-off back to brand monitoring
When dark-social signals get loud enough to surface in public mentions, hand back to `brand-reputation-monitoring-brandwatch-meltwater`. Dark social is pre-public signal; public mentions are post-public.

### Free fallback Day 1
If no SparkToro / Common Room budget Day 1: use `brave-search`, `firecrawl-mcp` to monitor public-listed Discord servers (Disboard.org index), `youtube-mcp-transcript` for podcast brand mentions, manual mod outreach for permission. Less accurate, but functional.

### Tracking ROI of dark social
Hard. Proxies: identified leads from Common Room signals + UTM-tagged share-via-copy clicks + sentiment-positive mention growth in private communities + brand-search lift (Google Trends + GA). Triangulate; don't expect clean attribution.

## Sources

- **SparkToro audience research**: https://sparktoro.com/blog/audience-research-tools/
- **SparkToro features**: https://sparktoro.com/features
- **Common Room community-led growth**: https://www.commonroom.io/
- **Common Room API**: https://www.commonroom.io/docs/api
- **Discord developer docs**: https://discord.com/developers/docs
- **Dark social attribution**: https://sparktoro.com/blog/the-state-of-dark-social/
- **SimilarWeb dark social blog**: https://www.similarweb.com/corp/blog/research/audience/dark-social/
- **role.md SOTA tool reference (dark social)**: internal `agent_bundle/agents/pr-comms/role.md`
