<!--
Source: https://developers.google.com/google-ads/api/docs/developer-toolkit/mcp-server
Source: https://support.google.com/google-ads/answer/10724817
Google Ads MCP via @googleads/mcp-server. PMax = Google's cross-network AI campaign.
-->
# Google Ads — Performance Max + Standard Search — SKILL

Performance Max (PMax) is Google's AI campaign serving across Search, Display, YouTube, Discover, Gmail, Maps with a single asset pool. Standard Search still owns brand + high-intent non-brand keyword control. This skill ships both, plus GAQL reporting, audience signals, and the conversion-tracking prerequisites.

## When to use this skill

- **Retail / e-com** that needs Shopping + Display + YouTube product mentions in one budget — PMax with Merchant Center feed.
- **Lead generation** — PMax for Lead-gen objective once conversion tracking is rock-solid.
- **Brand defense** — Standard Search exact-match on brand terms (PMax exclude brand).
- **High-intent non-brand** — Standard Search with strict phrase + exact match types.
- **App installs** — App campaigns (different code path; see Google Ads MCP `create_app_campaign`).
- **Account audit** — pull GAQL across campaigns / ad groups / keywords / search terms.

**Do NOT use this skill when:**
- Pure brand awareness on YouTube only (use Video campaigns explicitly).
- Single-keyword test isolated from ecosystem (use Search campaigns).
- Non-Google ads (see Meta / TikTok / LinkedIn / Reddit skills).

## Setup

### Install MCP server

```bash
ADS_MCP_ENABLE_MUTATIONS=true npx -y @googleads/mcp-server@latest
```

### Auth

```bash
# GCP project with Google Ads API enabled, OAuth Desktop client
google-ads-mcp auth --client-secret ./gcp-client-secret.json

export GOOGLE_ADS_CUSTOMER_ID="1234567890"
export GOOGLE_ADS_LOGIN_CUSTOMER_ID="9876543210"   # MCC
export GOOGLE_ADS_DEVELOPER_TOKEN="<from-mcc>"
export ADS_MCP_ENABLE_MUTATIONS=true
```

Developer token application: https://ads.google.com/aw/apicenter

### Tools exposed

- `search`, `search_stream` — GAQL queries
- `create_campaign`, `update_campaign`, `pause_campaign`
- `create_pmax_campaign`, `set_pmax_asset_groups`
- `create_ad_group`, `create_keyword`, `add_negative_keyword`
- `create_responsive_search_ad`, `update_ad`
- `create_audience_list`, `add_users_to_audience`
- `get_recommendations`, `apply_recommendation`

### PMax prerequisites (hard requirements)

1. Conversion tracking working (gtag.js OR GTM-S OR Enhanced Conversions). Use `meta-capi-tiktok-events-google-enhanced-conversions` skill if not.
2. For retail PMax — linked Merchant Center account with approved products.
3. Single primary conversion goal at account level + secondary goals per campaign if needed.
4. Brand exclusion list — exclude your own brand terms so PMax doesn't cannibalize Search Brand.

## Common recipes

### Recipe 1: GAQL — campaign performance last 30d

```bash
mcp tool google-ads.search \
  --customer_id "$GOOGLE_ADS_CUSTOMER_ID" \
  --query "
    SELECT campaign.id, campaign.name, campaign.status,
           metrics.impressions, metrics.clicks, metrics.cost_micros,
           metrics.conversions, metrics.conversions_value
    FROM campaign
    WHERE segments.date DURING LAST_30_DAYS
      AND campaign.status = 'ENABLED'
    ORDER BY metrics.cost_micros DESC"
```
`cost_micros` is currency × 1,000,000. ROAS = `conversions_value / (cost_micros/1e6)`.

### Recipe 2: PMax campaign — retail, tROAS

```bash
mcp tool google-ads.create_pmax_campaign \
  --customer_id "$GOOGLE_ADS_CUSTOMER_ID" \
  --name "PMax-Retail-Q3" \
  --budget_micros 10000000000 \
  --bidding_strategy '{"maximize_conversion_value":{"target_roas":4.0}}' \
  --merchant_center_id "<merchant-id>" \
  --feed_label "US" \
  --customer_acquisition_optimization '{"optimization_mode":"BID_HIGHER_FOR_NEW_CUSTOMERS"}'

# Asset group with audience signal
mcp tool google-ads.set_pmax_asset_groups \
  --campaign_id "$PMAX_CAMPAIGN_ID" \
  --asset_group '{
    "name":"AG-Shopping-Intent-Women-25-45",
    "headlines":["Free shipping over $50","Try risk-free 30 days","Trusted by 50K+ customers",
                 "Best sellers — back in stock","Customer-loved skin care","Eco-conscious formulas"],
    "long_headlines":["Discover what 50,000+ customers love about our line"],
    "descriptions":["Risk-free trial. Free returns within 30 days.","Sustainable, dermatologist-tested formulas."],
    "marketing_images":["<asset_id_image1>","<asset_id_image2>","<asset_id_image3>"],
    "logo_images":["<logo_asset_id>"],
    "youtube_videos":["<youtube_video_id>"],
    "audience_signals":{
      "custom_audiences":["<audience_id_in_market>"],
      "user_lists":["<customer_match_list_id>"]
    }
  }'

# Brand exclusion at campaign level
mcp tool google-ads.add_campaign_negative_keyword \
  --campaign_id "$PMAX_CAMPAIGN_ID" \
  --text "yourbrand" \
  --match_type "PHRASE"
```

### Recipe 3: Standard Search — brand defense

```bash
# Campaign
campaign_id=$(mcp tool google-ads.create_campaign \
  --customer_id "$GOOGLE_ADS_CUSTOMER_ID" \
  --name "Search-Brand-Defense" \
  --advertising_channel_type "SEARCH" \
  --budget_micros 5000000000 \
  --bidding_strategy '{"target_impression_share":{"location":"ABSOLUTE_TOP_OF_PAGE","cpc_bid_ceiling_micros":2000000,"location_fraction_micros":900000}}')

# Ad group + exact-match keywords
ag=$(mcp tool google-ads.create_ad_group --campaign_id "$campaign_id" --name "Brand-Exact" --cpc_bid_micros 1500000)

for kw in "yourbrand" "yourbrand.com" "your brand login" "your brand reviews"; do
  mcp tool google-ads.create_keyword --ad_group_id "$ag" --text "$kw" --match_type "EXACT"
done

# RSA — 11+ headlines, 4+ descriptions for full asset rotation
mcp tool google-ads.create_responsive_search_ad \
  --ad_group_id "$ag" \
  --final_urls '["https://yourbrand.com/?utm_source=google&utm_medium=cpc&utm_campaign=brand-defense"]' \
  --headlines '["Yourbrand — Official Site","Yourbrand.com — Login","Try Yourbrand Free","Yourbrand Reviews",
                "Trusted by 50K+","Risk-Free 30-Day Trial","Free Shipping","No Credit Card",
                "Best-in-Class Service","Award-winning","Save 20% Today"]' \
  --descriptions '["Official site. Free shipping over $50.","Try risk-free for 30 days. No credit card.","Trusted by 50,000+ customers. 4.9 star average.","Award-winning support, free returns."]' \
  --path1 "official" --path2 "free-trial"
```

### Recipe 4: Search term mining — add negatives + new exact keywords

```bash
mcp tool google-ads.search --customer_id "$GOOGLE_ADS_CUSTOMER_ID" --query "
  SELECT search_term_view.search_term, ad_group.name,
         metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions
  FROM search_term_view
  WHERE segments.date DURING LAST_30_DAYS AND metrics.impressions > 50
  ORDER BY metrics.cost_micros DESC LIMIT 500" > search_terms.json

# Classify (LLM or rules)
# Add negatives:
for term in $(jq -r '.[] | select(.intent=="irrelevant") | .search_term' classified.json); do
  mcp tool google-ads.add_negative_keyword --campaign_id "$CAMPAIGN_ID" --text "$term" --match_type "PHRASE"
done

# Add high-converting as exact:
for term in $(jq -r '.[] | select(.conversions > 3) | .search_term' classified.json); do
  mcp tool google-ads.create_keyword --ad_group_id "$AG_ID" --text "$term" --match_type "EXACT"
done
```

### Recipe 5: Customer Match for PMax audience signal

```bash
list_id=$(mcp tool google-ads.create_audience_list \
  --customer_id "$GOOGLE_ADS_CUSTOMER_ID" \
  --name "Top-25pct-LTV-Customers" \
  --type "CRM_BASED" --upload_key_type "CONTACT_INFO" --membership_life_span 540)

# Hash SHA-256 of lowercased + trimmed email/phone, upload
mcp tool google-ads.add_users_to_audience \
  --audience_list_id "$list_id" \
  --users_file "@hashed-users.json"
```

### Recipe 6: PMax insights — asset performance

```bash
mcp tool google-ads.search --customer_id "$GOOGLE_ADS_CUSTOMER_ID" --query "
  SELECT asset_group.name, asset_group_asset.field_type, asset.id,
         metrics.impressions, metrics.clicks, metrics.conversions, metrics.conversions_value
  FROM asset_group_asset
  WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
    AND segments.date DURING LAST_30_DAYS"
```

### Recipe 7: Recommendations API — auto-apply low-risk

```bash
mcp tool google-ads.get_recommendations --customer_id "$GOOGLE_ADS_CUSTOMER_ID" > recs.json

# Apply only safe types: KEYWORD adds, NEGATIVE_KEYWORD, AD_ASSET adds
for rid in $(jq -r '.[] | select(.type | IN("KEYWORD","KEYWORD_NEGATIVE","CALLOUT_ASSET")) | .id' recs.json); do
  mcp tool google-ads.apply_recommendation --recommendation_id "$rid"
done
```

## Examples — full account structure

```yaml
account:
  primary_conversion: purchase (value = revenue)
  enhanced_conversions: enabled (Web + Leads)
  gtm_server_url: sgtm.brand.com
  brand_exclusion_list: ["yourbrand","yourbrand reviews","yourbrand login"]

campaigns:
  search_brand:
    type: SEARCH
    budget: $50/day
    bid: target_impression_share absolute_top_of_page 90%
  search_competitor:
    type: SEARCH
    budget: $40/day
    bid: target_cpa $40
  search_non_brand_high_intent:
    type: SEARCH
    budget: $200/day
    bid: maximize_conversions
  pmax_retail:
    type: PMAX
    budget: $300/day
    bid: maximize_conversion_value, target_roas 4.0
    asset_groups: [shopping_intent_women, gift_giving_holiday, eco_conscious_buyers]
  pmax_lead_gen:
    type: PMAX
    budget: $150/day
    bid: maximize_conversions, target_cpa $60
  youtube_view:
    type: VIDEO
    budget: $80/day
    bid: target_cpm
```

## Edge cases

### Mutations gate
`ADS_MCP_ENABLE_MUTATIONS=true` required. Default read-only.

### PMax keyword targeting impossible
PMax has no keyword targeting — only audience signals (hints). Use Standard Search if you need keyword control.

### PMax search-term reporting limited
PMax does NOT expose individual search terms (unlike Standard Search). Workaround: scrape "Insights" tab via UI OR query `campaign_search_term_insight` view (limited).

### Min budget for PMax to learn
$50/day floor. Below this, PMax doesn't accumulate enough signal. Recommended $100/day per campaign for meaningful results.

### RSA constraints
3-15 headlines (≤30 chars), 2-4 descriptions (≤90 chars). 11+1+4 minimum for asset rotation health.

### tROAS too aggressive
Setting tROAS = 8.0 on a new PMax campaign starves delivery. Start with `maximize_conversion_value` (no tROAS) for 2-3 weeks, then layer tROAS based on observed ROAS.

### Quality Score impact
GAQL: `ad_group_criterion.quality_info.quality_score`. <7 = ad relevance / LP issue. Pull weekly:

```sql
SELECT ad_group_criterion.keyword.text, ad_group_criterion.quality_info.quality_score
FROM keyword_view
WHERE ad_group_criterion.quality_info.quality_score <= 6
  AND ad_group_criterion.status = 'ENABLED'
```

### Rate limits
15,000 ops/day default for non-test accounts. Use `search_stream` for >100K-row queries.

### Customer Match minimums
List size minimum 1,000 users. Hash SHA-256 of lowercased + trimmed email/phone.

### Brand exclusion vs negative keyword
Brand exclusion (PMax feature) suppresses serving on brand searches. Negative keywords work for Search campaigns. Use brand exclusion at PMax level.

## Sources

- Google Ads MCP: https://developers.google.com/google-ads/api/docs/developer-toolkit/mcp-server
- GAQL reference: https://developers.google.com/google-ads/api/docs/query/overview
- PMax overview: https://support.google.com/google-ads/answer/10724817
- RSA best practices: https://support.google.com/google-ads/answer/7684791
- Customer Match: https://support.google.com/google-ads/answer/6379332
- Bid strategies: https://support.google.com/google-ads/answer/2390939
- Recommendations API: https://developers.google.com/google-ads/api/docs/recommendations
