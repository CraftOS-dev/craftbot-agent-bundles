<!--
Source: https://pasqualepillitteri.it/en/news/1707/official-meta-ads-mcp-claude-29-tools-2026
Meta official Ads MCP: mcp.facebook.com/ads (GA April 29, 2026)
-->
# Meta Ads Official MCP — SKILL

The official Meta Ads MCP at `mcp.facebook.com/ads` went GA April 29, 2026 with 29 tools and crucially **does not require Meta Developer App approval** — OAuth-based, instant access. This replaces the `facebook-ads-mcp` community server as the recommended path.

## When to use this skill

- **Any Meta Ads work** — Facebook, Instagram, Audience Network, Messenger ad placements.
- **Programmatic campaign creation** with daily budget, optimization goal, targeting.
- **Catalog management** for DPA (Dynamic Product Ads) / Advantage+ Shopping campaigns.
- **Signal health checks** for CAPI (Conversions API) + pixel diagnostics.
- **Creative-level A/B testing** with multiple variants per ad set.
- **Bulk campaign edits** (pause / activate / budget changes) — much faster than Ads Manager UI.

**Do NOT use this skill when:**
- **Other ad platforms** (Google → `google-ads-mcp`, TikTok → `tiktok-ads-mcp`, LinkedIn → `linkedin-marketing-api`, Reddit → curl).
- **Pure analytics on Meta data** (use Meta Business Suite native exports).

## Setup

### Auth — OAuth at mcp.facebook.com/ads

```bash
# 1. Open browser to OAuth flow
# https://mcp.facebook.com/ads/oauth?redirect=<your_callback>
# 2. Grant scopes: ads_management, ads_read, business_management, catalog_management
# 3. Save the returned token

export META_ADS_MCP_TOKEN="<oauth-token>"
export META_AD_ACCOUNT_ID="act_<numeric>"
export META_BUSINESS_ID="<business-id>"
```

### MCP server connection

Meta hosts the MCP server — no `npx` install needed. Connect via remote MCP transport:

```json
// claude-config.json — mcpServers section
{
  "meta-ads": {
    "transport": "https",
    "url": "https://mcp.facebook.com/ads/v1",
    "auth": {"type":"bearer","token":"${META_ADS_MCP_TOKEN}"}
  }
}
```

### 29 tools available (June 2026)

**Campaign-level (6 tools):**
- `create_campaign` — name, objective, special_ad_categories, budget
- `update_campaign` — pause / activate / rename
- `list_campaigns` — filter by status, date
- `get_campaign` — full details
- `delete_campaign` — soft-delete
- `get_campaign_insights` — performance metrics

**Ad set-level (8 tools):**
- `create_adset` — campaign_id, targeting, daily_budget, optimization_goal, billing_event
- `update_adset` — budgets, targeting, bids
- `list_adsets` / `get_adset` / `delete_adset`
- `get_adset_insights` — performance per ad set
- `duplicate_adset` — clone with new audience for testing
- `pause_adsets_bulk` — bulk action

**Ad-level (7 tools):**
- `create_ad` — adset_id, creative, name
- `update_ad` / `list_ads` / `get_ad` / `delete_ad`
- `get_ad_insights`
- `duplicate_ad` — clone for creative A/B

**Creative (3 tools):**
- `create_ad_creative` — image, video, carousel, instant-experience
- `list_ad_creatives`
- `validate_creative` — pre-flight check for policy / format

**Catalog & diagnostics (5 tools):**
- `manage_catalog` — list, create, sync product catalogs
- `create_product_set` — for DPA targeting
- `check_signal_health` — CAPI + pixel + event coverage score
- `get_pixel_diagnostics` — issues + suggestions
- `get_capi_status` — server-side events flow

## Common recipes

### Recipe 1: Full-funnel new campaign (Awareness → Consideration → Conversion)

```bash
# Step 1: Awareness campaign — reach optimization
mcp tool meta-ads.create_campaign \
  --name "Q3-Launch-Awareness" \
  --objective "OUTCOME_AWARENESS" \
  --status "PAUSED" \
  --special_ad_categories "[]" \
  --buying_type "AUCTION"

# Step 2: Ad set — broad lookalike + interest stack
mcp tool meta-ads.create_adset \
  --campaign_id "<id>" \
  --name "Awareness-LAL3-Tier1" \
  --daily_budget 5000 \
  --optimization_goal "REACH" \
  --billing_event "IMPRESSIONS" \
  --targeting '{
    "geo_locations":{"countries":["US","CA","UK"]},
    "custom_audiences":[{"id":"<lal-3pct-id>"}],
    "interests":[{"id":"6003107902433","name":"Online shopping"}],
    "age_min":25,"age_max":55,
    "publisher_platforms":["facebook","instagram"],
    "facebook_positions":["feed","video_feeds"],
    "instagram_positions":["stream","reels"]
  }' \
  --start_time "2026-06-15T00:00:00Z"

# Step 3: Creative
mcp tool meta-ads.create_ad_creative \
  --name "Hero-VideoV1" \
  --object_story_spec '{
    "page_id":"<page>",
    "video_data":{
      "video_id":"<uploaded-video-id>",
      "title":"<headline>",
      "message":"<primary-text>",
      "call_to_action":{"type":"LEARN_MORE","value":{"link":"https://brand.com/lp?utm=meta-aware-v1"}}
    }
  }'

# Step 4: Ad
mcp tool meta-ads.create_ad \
  --adset_id "<adset>" \
  --creative_id "<creative>" \
  --name "Aware-Hero-V1"

# Repeat 2-4 for Consideration (TRAFFIC objective) and Conversion (OUTCOME_SALES)
```

### Recipe 2: Advantage+ Shopping campaign (DPA-style)

```bash
mcp tool meta-ads.create_campaign \
  --name "Advantage+-Q3" \
  --objective "OUTCOME_SALES" \
  --special_ad_categories "[]" \
  --advantage_plus_shopping true

mcp tool meta-ads.create_adset \
  --campaign_id "<id>" \
  --name "Advantage+-AllProducts" \
  --daily_budget 10000 \
  --optimization_goal "OFFSITE_CONVERSIONS" \
  --billing_event "IMPRESSIONS" \
  --product_set_id "<set-id>" \
  --targeting '{"geo_locations":{"countries":["US"]}}'

mcp tool meta-ads.create_ad_creative \
  --name "DPA-Catalog-Auto" \
  --product_set_id "<set-id>" \
  --template_data '{
    "message":"{{product.name}} — {{product.price}}",
    "call_to_action":{"type":"SHOP_NOW","value":{"link":"{{product.url}}?utm=meta-dpa"}}
  }'
```

### Recipe 3: Signal health check (CAPI + pixel)

```bash
mcp tool meta-ads.check_signal_health
# Returns:
# {
#   "pixel_id":"...",
#   "event_match_quality":7.8,   // 0-10, > 8 ideal
#   "capi_status":"healthy",
#   "missing_parameters":["em","ph"],  // hash these for better match
#   "deduplication_status":"good",
#   "recommendations":["Add hashed email and phone to CAPI events"]
# }
```

If quality < 7, the agent should:
1. Flag missing params (email, phone, ext_id, click_id).
2. Suggest CAPI integration if pixel-only.
3. Verify dedupe via `event_id` shared between browser + server.

### Recipe 4: Catalog sync from Shopify / Klaviyo

```bash
mcp tool meta-ads.manage_catalog \
  --action "create" \
  --name "Brand-Catalog-2026" \
  --feed_url "https://brand.com/feed.xml" \
  --schedule "every_6_hours"

# Or via Klaviyo MCP product export:
# klaviyo.list_products() → format as Meta product feed → manage_catalog --action sync
```

### Recipe 5: Creative A/B test (4 variants, $200 budget)

```bash
# One ad set, 4 ads with different creatives
adset_id=$(mcp tool meta-ads.create_adset --daily_budget 20000 ...)

for v in V1 V2 V3 V4; do
  cid=$(mcp tool meta-ads.create_ad_creative --name "Hero-$v" --image_hash "<img_$v>" ...)
  mcp tool meta-ads.create_ad --adset_id "$adset_id" --creative_id "$cid" --name "Test-$v"
done

# After 72h, fetch insights and pick winner
mcp tool meta-ads.get_adset_insights \
  --adset_id "$adset_id" \
  --breakdowns '["ad_id"]' \
  --metrics '["cpa","ctr","conversions","spend"]' \
  --date_preset "last_3_days"

# Pause losers
for losing_ad in $(...); do
  mcp tool meta-ads.update_ad --ad_id "$losing_ad" --status PAUSED
done
```

### Recipe 6: Bulk pause campaigns at end-of-month

```bash
mcp tool meta-ads.list_campaigns --filter '{"end_time":{"<=":"2026-06-30"}}' | \
  jq -r '.[].id' | \
  while read id; do mcp tool meta-ads.update_campaign --campaign_id "$id" --status PAUSED; done
```

### Recipe 7: Daily performance pull → Notion dashboard

```python
# Run via cli-anything python -c
campaigns = meta_ads.list_campaigns(status='ACTIVE')
for c in campaigns:
    metrics = meta_ads.get_campaign_insights(
        campaign_id=c['id'],
        date_preset='yesterday',
        metrics=['spend','impressions','clicks','ctr','cpc','conversions','cost_per_conversion','roas']
    )
    notion.update_page(
        c['notion_page_id'],
        properties={'spend': metrics['spend'], 'roas': metrics['roas'], ...}
    )
```

## Examples — full launch checklist

For a $50K Q3 product launch:

| Phase | Objective | Daily Budget | Targeting | Creative Variants |
|---|---|---|---|---|
| Awareness | OUTCOME_AWARENESS, REACH | $5K | LAL 3% + broad interest | 4 (video hero) |
| Consideration | OUTCOME_TRAFFIC | $3K | Retarget engagers 30d | 3 (carousel + UGC) |
| Conversion (DPA) | OUTCOME_SALES, OFFSITE_CONVERSIONS | $7K | Advantage+ Shopping all products | DPA catalog |
| Retargeting | OUTCOME_SALES | $2K | Past 30d site visitors, no purchase | 2 (offer + social proof) |

## Edge cases

### Special ad categories (housing, employment, credit)
Required if ads relate to these — limits targeting (no detailed demographics):

```bash
--special_ad_categories '["HOUSING"]'
```

If missing, ads run but at risk of takedown.

### Policy violations
Always pre-flight `validate_creative`:

```bash
mcp tool meta-ads.validate_creative --creative_id "<id>"
# Returns: {policy_check:'passed'/'failed', issues:[...]}
```

Common rejections:
- Before/after images
- Personal attributes claims ("Are you struggling with...")
- "Click here" CTAs in body (use the formal CTA button)
- Profanity / shock content

### Budget limits
- Daily budget min: $1 (low) / $5 (recommended)
- Lifetime budget: requires `end_time`
- Account spending limit: set at account level; bulk-set via `update_ad_account`

### Audience size thresholds
- Custom audience: min 100 to deliver, recommended 1,000+
- Lookalike: source must be 100+, 1% LAL most similar / 10% most reach

### CAPI required from 2025+
Pixel-only setup is deprecated. CAPI dedup with `event_id`:

```json
{
  "event_name":"Purchase",
  "event_time":1718000000,
  "event_id":"<uuid-shared-with-browser-pixel>",
  "user_data":{
    "em":["<sha256-email>"],
    "ph":["<sha256-phone>"],
    "fbc":"<click-id-cookie>",
    "fbp":"<browser-id-cookie>"
  },
  "custom_data":{"value":99.99,"currency":"USD"}
}
```

### Rate limits
- 200 calls / hour / ad account (default)
- Bulk endpoints (`bulk_*`) consume less; use them.
- `bulk_pause`: 500 entities per call.

### Bidding strategy default
- Auction → `lowest_cost_without_cap` (default)
- For ROAS: `lowest_cost_with_min_roas` — min_roas required
- Cost cap: `lowest_cost_with_bid_cap` for predictable CPA

## Sources

- **Meta Ads MCP announcement**: https://pasqualepillitteri.it/en/news/1707/official-meta-ads-mcp-claude-29-tools-2026
- **Meta Marketing API reference**: https://developers.facebook.com/docs/marketing-apis
- **Advantage+ Shopping**: https://www.facebook.com/business/help/2204418216254220
- **CAPI implementation**: https://developers.facebook.com/docs/marketing-api/conversions-api
