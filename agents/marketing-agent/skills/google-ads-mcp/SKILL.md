<!--
Source: https://developers.google.com/google-ads/api/docs/developer-toolkit/mcp-server
Google Ads MCP: googleads/google-ads-mcp via npx @googleads/mcp-server
-->
# Google Ads MCP — SKILL

The official Google Ads MCP server (`googleads/google-ads-mcp`) exposes GAQL `search` for query-driven analysis and full mutation surface when `ADS_MCP_ENABLE_MUTATIONS=true`. This is the SOTA for programmatic search/display/PMax campaigns.

## When to use this skill

- **Search campaigns** — RSA (Responsive Search Ads), keyword themes, broad/phrase/exact matching.
- **Display + remarketing** — image creatives, audience lists.
- **Performance Max (PMax)** — Google's AI-driven cross-network campaign type.
- **Shopping / Merchant Center linked campaigns**.
- **Reporting via GAQL** — read-only queries on metrics, cost, conversions, ROAS.
- **Budget / bid adjustments** — automated optimization rules.

**Do NOT use this skill when:**
- **Non-Google ads** — see Meta, TikTok, LinkedIn, Reddit skills.
- **SEO / organic** — see Ahrefs / GSC skills.

## Setup

### Install

```bash
# Mutations DISABLED by default for safety
ADS_MCP_ENABLE_MUTATIONS=true npx -y @googleads/mcp-server@latest
```

### Auth — Google Ads API

```bash
# 1. GCP project with Google Ads API enabled
# 2. OAuth client (Desktop type)
# 3. Run auth flow once

google-ads-mcp auth --client-secret ./gcp-client-secret.json
# Token saved to ~/.google-ads-mcp/

export GOOGLE_ADS_CUSTOMER_ID="123-456-7890"  # without dashes for some endpoints
export GOOGLE_ADS_LOGIN_CUSTOMER_ID="987-654-3210"  # MCC if applicable
export GOOGLE_ADS_DEVELOPER_TOKEN="<from-mcc>"
export ADS_MCP_ENABLE_MUTATIONS=true  # CRITICAL for create/edit
```

Developer token (apply via MCC): https://ads.google.com/aw/apicenter

### Tools available

- `search` — GAQL query (read-only)
- `search_stream` — large result streaming
- `create_campaign` / `update_campaign` / `pause_campaign`
- `create_ad_group` / `update_ad_group`
- `create_keyword` / `update_keyword` / `add_negative_keyword`
- `create_responsive_search_ad` / `update_ad`
- `create_pmax_campaign` / `set_pmax_asset_groups`
- `create_audience_list` / `add_users_to_audience`
- `get_recommendations` — Google's auto-recommendations
- `apply_recommendation`

## Common recipes

### Recipe 1: GAQL — last 30 days campaign performance

```bash
mcp tool google-ads.search \
  --customer_id "$GOOGLE_ADS_CUSTOMER_ID" \
  --query "
    SELECT
      campaign.id,
      campaign.name,
      campaign.status,
      metrics.impressions,
      metrics.clicks,
      metrics.cost_micros,
      metrics.conversions,
      metrics.conversions_value,
      metrics.average_cpc,
      metrics.ctr,
      metrics.conversion_rate
    FROM campaign
    WHERE segments.date DURING LAST_30_DAYS
      AND campaign.status = 'ENABLED'
    ORDER BY metrics.cost_micros DESC
  "
```

GAQL note: `cost_micros` is cost × 1,000,000. Divide for actual currency.

### Recipe 2: Search-term insights (the "what queries did people search")

```bash
mcp tool google-ads.search \
  --customer_id "$GOOGLE_ADS_CUSTOMER_ID" \
  --query "
    SELECT
      search_term_view.search_term,
      ad_group.name,
      metrics.impressions,
      metrics.clicks,
      metrics.cost_micros,
      metrics.conversions
    FROM search_term_view
    WHERE segments.date DURING LAST_30_DAYS
      AND metrics.impressions > 50
    ORDER BY metrics.cost_micros DESC
    LIMIT 200
  "
```

For each search term: classify intent, add as negative if irrelevant, add as exact-match keyword if high-converting.

### Recipe 3: Create RSA search campaign

```bash
# Step 1: Campaign
campaign_id=$(mcp tool google-ads.create_campaign \
  --customer_id "$GOOGLE_ADS_CUSTOMER_ID" \
  --name "Q3-Search-Brand" \
  --advertising_channel_type "SEARCH" \
  --status "PAUSED" \
  --budget_micros 5000000000 \
  --bidding_strategy '{
    "target_cpa": {"target_cpa_micros": 50000000}
  }' \
  --geo_targets '["1023191"]' \
  --language_targets '["en"]')

# Step 2: Ad group
ag_id=$(mcp tool google-ads.create_ad_group \
  --customer_id "$GOOGLE_ADS_CUSTOMER_ID" \
  --campaign_id "$campaign_id" \
  --name "Brand-Exact" \
  --cpc_bid_micros 2000000)

# Step 3: Keywords (exact match for brand)
for kw in "yourbrand" "your brand" "yourbrand.com"; do
  mcp tool google-ads.create_keyword \
    --ad_group_id "$ag_id" \
    --text "$kw" \
    --match_type "EXACT"
done

# Step 4: RSA — 15 headlines, 4 descriptions max
mcp tool google-ads.create_responsive_search_ad \
  --ad_group_id "$ag_id" \
  --final_urls '["https://yourbrand.com"]' \
  --headlines '[
    "Brand Official Site",
    "yourbrand — Official",
    "yourbrand.com — Start Free",
    "Brand — Try Free Today",
    ...
  ]' \
  --descriptions '[
    "Official site — try free for 14 days. No credit card.",
    "Trusted by 10,000+ teams. Start your free trial now.",
    ...
  ]' \
  --path1 "free-trial" \
  --path2 "no-cc"
```

### Recipe 4: Performance Max campaign

```bash
mcp tool google-ads.create_pmax_campaign \
  --customer_id "$GOOGLE_ADS_CUSTOMER_ID" \
  --name "PMax-Q3" \
  --budget_micros 10000000000 \
  --bidding_strategy '{"maximize_conversion_value": {"target_roas": 4.0}}' \
  --merchant_center_id "<merchant-id>"

# Asset group (creative input)
mcp tool google-ads.set_pmax_asset_groups \
  --campaign_id "<id>" \
  --asset_group '{
    "name": "PMax-AG-1",
    "headlines": ["..."],
    "descriptions": ["..."],
    "long_headlines": ["..."],
    "marketing_images": ["<image-asset-id>"],
    "logo_images": ["<logo-asset-id>"],
    "youtube_videos": ["<video-id>"],
    "audience_signals": {"custom_audiences": ["<audience-id>"]}
  }'
```

### Recipe 5: Add negative keywords (cleaner search-term lists)

```bash
# After running search-term insights, add irrelevant terms as negatives
mcp tool google-ads.add_negative_keyword \
  --customer_id "$GOOGLE_ADS_CUSTOMER_ID" \
  --campaign_id "<id>" \
  --text "free" \
  --match_type "PHRASE"

# Bulk:
for term in $(cat negative-terms.txt); do
  mcp tool google-ads.add_negative_keyword --campaign_id "<id>" --text "$term" --match_type "PHRASE"
done
```

### Recipe 6: Customer Match audience upload (for remarketing)

```bash
# Create user list
list_id=$(mcp tool google-ads.create_audience_list \
  --customer_id "$GOOGLE_ADS_CUSTOMER_ID" \
  --name "Q3-CRM-Customers" \
  --type "CRM_BASED" \
  --upload_key_type "CONTACT_INFO" \
  --membership_life_span 540)

# Hash + upload (SHA256 of normalized email)
mcp tool google-ads.add_users_to_audience \
  --audience_list_id "$list_id" \
  --users_file "@hashed-users.json"  # [{"hashed_email": "...", "hashed_phone_number": "..."}]
```

### Recipe 7: GAQL — ROAS by ad group

```bash
mcp tool google-ads.search \
  --customer_id "$GOOGLE_ADS_CUSTOMER_ID" \
  --query "
    SELECT
      ad_group.id,
      ad_group.name,
      campaign.name,
      metrics.cost_micros,
      metrics.conversions_value,
      metrics.value_per_conversion
    FROM ad_group
    WHERE segments.date DURING LAST_30_DAYS
      AND metrics.cost_micros > 100000000
    ORDER BY metrics.value_per_conversion DESC
  "
```

Compute ROAS = conversions_value / (cost_micros / 1e6). Pause if ROAS < 1; scale if ROAS > target.

### Recipe 8: Auto-apply recommendations

```bash
# List recommendations
mcp tool google-ads.get_recommendations --customer_id "$GOOGLE_ADS_CUSTOMER_ID"

# Apply specific (e.g., KEYWORD additions)
mcp tool google-ads.apply_recommendation --recommendation_id "<id>"
```

Auto-apply rules:
- ENABLED for: KEYWORD (add) when from search terms with > 10 conversions
- DISABLED for: CAMPAIGN_BUDGET (we control budgets), MAXIMIZE_CLICKS (we control bidding)

## Examples — full search account setup

```yaml
account_structure:
  campaign_brand:
    type: SEARCH
    budget: $50/day
    bidding: target_cpa $20
    ad_groups:
      - brand_exact
      - brand_phrase
      - brand_misspellings
  campaign_competitor:
    type: SEARCH
    budget: $30/day
    bidding: target_cpa $40
    ad_groups: [competitor_1, competitor_2]
  campaign_non_brand_high_intent:
    type: SEARCH
    budget: $100/day
    bidding: target_cpa $60
    ad_groups:
      - solution_category
      - product_specific
      - pricing_intent
  campaign_pmax:
    type: PMAX
    budget: $150/day
    bidding: maximize_conversion_value, target_roas 4
  campaign_youtube_remarketing:
    type: VIDEO
    budget: $30/day
    audiences: ["customer-match-30d","website-visitors-30d"]
```

## Edge cases

### Mutations gate
`ADS_MCP_ENABLE_MUTATIONS=true` MUST be set or all create/update calls return 403. Default is read-only.

### MCC vs single account
Use `login_customer_id` for MCC operations:
```bash
export GOOGLE_ADS_LOGIN_CUSTOMER_ID="<mcc-id>"
```

### Customer ID format
Some endpoints accept dashes (`123-456-7890`), some require no dashes (`1234567890`). The MCP tool normalizes.

### GAQL date ranges
Predefined: `TODAY`, `YESTERDAY`, `LAST_7_DAYS`, `LAST_14_DAYS`, `LAST_30_DAYS`, `LAST_90_DAYS`, `THIS_MONTH`, `LAST_MONTH`.
Custom: `segments.date BETWEEN '2026-01-01' AND '2026-03-31'`.

### RSA constraints
- 3-15 headlines, max 30 chars each
- 2-4 descriptions, max 90 chars each
- Google's recommended minimum: 11 headlines + 4 descriptions for full asset rotation

### PMax limitations
- No keyword targeting (audience signals only)
- No control over individual ad creative — Google mixes assets
- Reporting limited (no search term report at PMax level)
- Min budget: $50/day for meaningful learning

### Conversion tracking required
PMax + Maximize Conversion Value bidding REQUIRE conversion tracking configured. Use:
- Google Ads conversion tag (gtag.js)
- Enhanced conversions (hash email + phone in event)
- Server-side via Google Tag Manager Server-side container

### Quality Score
GAQL exposes `ad_group_criterion.quality_info.quality_score` (1-10). Sub-7 keywords need ad relevance / landing page work. Pull weekly:

```sql
SELECT ad_group_criterion.keyword.text,
       ad_group_criterion.quality_info.quality_score,
       ad_group_criterion.quality_info.creative_quality_score,
       ad_group_criterion.quality_info.search_predicted_ctr,
       ad_group_criterion.quality_info.post_click_quality_score
FROM keyword_view
WHERE ad_group_criterion.status = 'ENABLED'
  AND ad_group_criterion.quality_info.quality_score <= 6
```

### Rate limits
- 15,000 ops/day default for non-test accounts
- Streaming reports for large datasets
- Cache: account structure rarely changes; query daily, not per-call

### Customer Match minimums
- Min list size: 1,000 users
- Hashing: SHA-256 of lowercased + trimmed email/phone

## Sources

- **Google Ads MCP docs**: https://developers.google.com/google-ads/api/docs/developer-toolkit/mcp-server
- **GAQL reference**: https://developers.google.com/google-ads/api/docs/query/overview
- **API field reference**: https://developers.google.com/google-ads/api/fields/v17/overview
- **RSA best practices**: https://support.google.com/google-ads/answer/7684791
- **PMax overview**: https://support.google.com/google-ads/answer/10724817
