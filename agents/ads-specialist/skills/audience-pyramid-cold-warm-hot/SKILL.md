<!--
Source: https://www.facebook.com/business/help/164749007013531
Source: https://support.google.com/google-ads/answer/6379332
Audience pyramid (cold / warm / hot + LAL seeds) — platform-by-platform spec.
-->
# Audience Pyramid — Cold / Warm / Hot + LAL — SKILL

The pyramid is the unifying targeting framework across Meta, Google, TikTok, LinkedIn, Reddit. Build the source audience set once, then upload to each platform with platform-native format. This skill specifies the layers, the % budget allocation, the seed selection, the refresh cadence, and the exclusion rules that prevent double-burning.

## When to use this skill

- **Account onboarding** — establish the pyramid before campaign creation.
- **Quarterly audience refresh** — re-seed lookalikes from updated LTV cohort.
- **Customer list refresh** — weekly hashed-email upload across platforms.
- **Cross-platform launch** — same pyramid, different platform format.
- **Audit finding** — accounts running broad-only or LAL-only structures need pyramid.

**Do NOT use this skill when:**
- Pure brand awareness ($0 conversion intent) — pyramid overkill.
- Single-audience guerrilla test — define just that audience.
- Server-side conversion (see `meta-capi-tiktok-events-google-enhanced-conversions`).

## Setup

### Source data — where seed audiences live

| Layer | Seed source | Storage | Refresh |
|---|---|---|---|
| Cold — LAL-1% | Top 25% LTV purchasers (last 180d) | Shopify / CRM warehouse | Monthly |
| Cold — LAL-3-5% | All purchasers (last 365d) | Shopify / CRM warehouse | Monthly |
| Cold — Interest Stack | Manual interest research | Platform UI | Quarterly |
| Cold — Broad / Advantage+ | Platform-decided | Platform | N/A |
| Warm — Engagers | Platform-native lookback (30-90d) | Platform pixel | Auto |
| Warm — Video viewers | Platform-native (50%-75% complete) | Platform | Auto |
| Hot — ATC / Initiated Checkout | Platform-native (7-30d) | Platform pixel | Auto |
| Hot — Customer Match | Hashed-email customer file | Platform | Weekly |

### Hashing utility

```bash
# Normalize + SHA-256 for email
hash_email() {
  echo -n "$1" | tr '[:upper:]' '[:lower:]' | tr -d '[:space:]' | sha256sum | awk '{print $1}'
}
hash_email "Alice@Example.com"
# 2bd806c97f0e00af1a1fc3328fa763a9269723c8db8fac4f93af71db186d6e90

# For phone (E.164 format)
hash_phone() {
  echo -n "$(echo "$1" | tr -dc '0-9+')" | sha256sum | awk '{print $1}'
}
```

### Default budget allocation

| Layer | % budget (DTC) | % budget (B2B) | % budget (App install) |
|---|---|---|---|
| Cold — LAL 1-3% | 35% | 20% | 40% |
| Cold — LAL 5-10% | 15% | 10% | 15% |
| Cold — Interest Stack | 10% | 25% (job-title) | 15% |
| Cold — Broad / Advantage+ | 15% | 5% | 20% |
| Warm — Engagers | 10% | 20% | 5% |
| Hot — Retargeting | 10% | 15% | 3% |
| Hot — Customer Match cross-sell | 5% | 5% | 2% |

## Common recipes

### Recipe 1: LAL seed — top 25% LTV from PostgreSQL warehouse

```sql
WITH ltv AS (
  SELECT customer_id, email,
         SUM(order_total) AS lifetime_value,
         COUNT(*) AS order_count
  FROM shopify.orders
  WHERE created_at >= NOW() - INTERVAL '365 days'
  GROUP BY customer_id, email
),
ranked AS (
  SELECT *, NTILE(4) OVER (ORDER BY lifetime_value DESC) AS quartile
  FROM ltv
)
SELECT email, lifetime_value
FROM ranked
WHERE quartile = 1   -- top 25%
ORDER BY lifetime_value DESC;
```

Pipe to CSV, hash, upload.

### Recipe 2: Meta — create LAL from customer list

```bash
# Step 1: Create custom audience from customer file
mcp tool meta-ads.create_custom_audience \
  --name "Seed_Top25_LTV_2026Q3" \
  --subtype "CUSTOM" \
  --customer_file_source "USER_PROVIDED_ONLY" \
  --users_file "@hashed-top25-ltv.json"
# JSON: [{"em": "<sha256>"}, ...] or schema=["EMAIL"], data=[["<sha256>"], ...]

# Step 2: Create LAL 1% from seed
mcp tool meta-ads.create_lookalike_audience \
  --name "LAL_1pct_US_Top25_LTV" \
  --origin_audience_id "$SEED_ID" \
  --country "US" \
  --ratio 0.01   # 0.01 = 1%, 0.05 = 5%, 0.10 = 10%
```

### Recipe 3: Google Customer Match — upload + LAL

```bash
# Create user list
list_id=$(mcp tool google-ads.create_audience_list \
  --customer_id "$GOOGLE_ADS_CUSTOMER_ID" \
  --name "Seed_Top25_LTV_2026Q3" \
  --type "CRM_BASED" \
  --upload_key_type "CONTACT_INFO" \
  --membership_life_span 540)

# Add hashed users
mcp tool google-ads.add_users_to_audience \
  --audience_list_id "$list_id" \
  --users_file "@hashed-top25-ltv.json"
# Format: [{"hashed_email":"<sha256>"},{"hashed_phone_number":"<sha256>"}]

# Create similar audience (auto-generated, Google calls it "Customer Match optimization")
# Reference in PMax asset group as audience signal:
mcp tool google-ads.set_pmax_asset_groups \
  --asset_group '{"audience_signals":{"user_lists":["'$list_id'"]}}'
```

### Recipe 4: TikTok — custom audience + lookalike

```bash
# Step 1: Create custom audience
curl -X POST "https://business-api.tiktok.com/open_api/v1.3/dmp/custom_audience/create/" \
  -H "Access-Token: $TT_ACCESS_TOKEN" \
  -d '{
    "advertiser_id":"'$TT_ADVERTISER_ID'",
    "custom_audience_name":"Seed_Top25_LTV_2026Q3",
    "calculate_type":"EMAIL_SHA256",
    "file_paths":["'$UPLOADED_FILE'"]
  }'

# Step 2: Lookalike
curl -X POST "https://business-api.tiktok.com/open_api/v1.3/dmp/custom_audience/lookalike/create/" \
  -H "Access-Token: $TT_ACCESS_TOKEN" \
  -d '{
    "advertiser_id":"'$TT_ADVERTISER_ID'",
    "custom_audience_id":"'$SEED_ID'",
    "lookalike_audience_name":"LAL_Top25_LTV_NARROW",
    "lookalike_spec":{"location":["US"],"lookalike_extents":"NARROW"}
  }'
```

### Recipe 5: LinkedIn — Matched Audience from CRM company list

```bash
# Already covered in linkedin-ads-abm-campaigns; reuse:
curl -X POST "https://api.linkedin.com/rest/dmpSegments" \
  -H "Authorization: Bearer $LI_ACCESS_TOKEN" \
  -H "LinkedIn-Version: 202406" \
  -d '{
    "account":"urn:li:sponsoredAccount:'$LI_ACCOUNT_ID'",
    "destinations":[{"destination":"LINKEDIN"}],
    "name":"Seed_TopAccounts_FY26",
    "type":"COMPANY"
  }'
```

### Recipe 6: Warm-layer adset on Meta — video viewers 50%+

```bash
# Create video-viewer custom audience
mcp tool meta-ads.create_custom_audience \
  --name "Warm_VideoViewer50pct_30d" \
  --subtype "VIDEO" \
  --rule '{
    "events":[{"name":"video_view","retention_seconds":2592000,
               "rule":{"percentage_viewed":">=50"}}]
  }'
```

### Recipe 7: Cross-platform cold campaign launch with pyramid

```yaml
campaign_set:
  source: hashed-top25-ltv.csv (refreshed weekly)
  
  meta:
    cold_LAL_1pct:
      seed: Top25_LTV_US
      ratio: 0.01
      exclusions: [past_purchasers_90d, current_customer_list]
    cold_LAL_3pct: { ratio: 0.03 }
    cold_LAL_5pct: { ratio: 0.05 }
    cold_interest_stack:
      interests: [Online shopping, Skincare, Eco-friendly products, Yoga]
    cold_advantage_plus:
      use_advantage_plus_audience: true
  
  google:
    pmax_audience_signal:
      user_lists: [customer_match_top25_ltv]
      custom_audiences: [in_market_skincare]
  
  tiktok:
    spc_targeting:
      custom_audiences: [seed_top25_ltv]
      lookalike: NARROW
      auto_targeting_enabled: true   # Let SPC explore
```

### Recipe 8: Hot-layer hashed-list exclusion across platforms

Common: cart-abandoners but exclude very-recent purchasers.

```bash
# Meta — flexible spec via Custom Audience exclusions
mcp tool meta-ads.create_adset \
  --campaign_id "$HOT_CAMPAIGN" \
  --name "Hot_ATC_7d_Excl_Pur_7d" \
  --targeting '{
    "custom_audiences":[{"id":"<atc-7d-id>"}],
    "excluded_custom_audiences":[{"id":"<pur-7d-id>"},{"id":"<customer-list-id>"}],
    "geo_locations":{"countries":["US"]}
  }'
```

## Examples — three audience-set templates

### DTC e-com (Shopify)

```yaml
seeds:
  top25_ltv: SQL NTILE(4) on lifetime_value
  all_purchasers_365d: SELECT email FROM orders WHERE created_at >= -365d
  cart_abandoners_30d: ATC events minus Purchase events

pyramid_meta:
  cold:
    LAL_1pct_Top25LTV: 40% budget
    LAL_3pct_AllPurchasers: 15%
    InterestStack_NicheVertical: 10%
    AdvantagePlusAudience: 10%
  warm:
    VideoViewer50_30d: 10%
    PageEngagers_30d: 5%
  hot:
    ATC_7d_minus_Pur_7d: 7%
    InitiatedCheckout_3d_minus_Pur_3d: 3%

exclusions_per_layer:
  cold: [purchasers_90d, customer_list_all]
  warm: [purchasers_30d]
  hot: [purchasers_7-14d depending on AOV/repeat cycle]
```

### B2B SaaS

```yaml
seeds:
  customer_list: hashed emails of active customers
  abm_tier1_companies: target-account list (company domains)
  high_intent_pages: viewed /pricing or /demo 30d

pyramid_linkedin:
  cold:
    ABM_Tier1_Companies + Director+ seniority: 50% budget
    JobTitle_DataEngineer + Senior+ seniority: 15%
    InterestStack_DataEngineering: 5%
  warm:
    SponsoredContent_Engagers_30d: 15%
    VideoViewer50_30d: 5%
  hot:
    SiteVisitors_30d_excl_customers: 10%
```

### Mobile app install

```yaml
seeds:
  high_LTV_paid_users: from analytics warehouse
  free_to_paid_converters: events where free→paid trigger fired

pyramid_meta:
  cold:
    LAL_1pct_HighLTV: 40%
    LAL_5pct_AllInstallers: 20%
    AdvantagePlusAudience: 15%
  warm:
    SiteVisitors_30d_NotInstalled: 15%
  hot:
    InstalledButInactive_7d: 5%
    PaidUsers_CrossPromo: 5%
```

## Edge cases

### Audience overlap > 30%
Meta Audience Overlap Tool. Two cold adsets with 30%+ overlap cannibalize. Add hard exclusion: cold-LAL-1% excludes cold-LAL-3% (cleaner pyramid steps).

### Minimum sizes per platform
- Meta Custom Audience: 100+ to deliver, 1K+ recommended
- Meta LAL: source 100+, 1% similar / 10% reach
- Google Customer Match: 1K+ minimum
- TikTok Custom: 1K+ minimum
- LinkedIn DMP: 300 members min

### Hashing format
ALL platforms require SHA-256 of lowercased + trimmed email/phone. Lowercase hex string output (NOT base64). Phone in E.164 format (e.g., `+12025550100`).

### Customer list staleness
60d unrefreshed = match rate drops 20%+. Schedule weekly auto-refresh via cron + warehouse query + platform upload.

### LAL seed quality
Don't seed LAL from "all purchasers" — too broad. Seed from top 25% LTV OR best-converting acquisition channel cohort. Better seed = better LAL.

### Privacy regulation
GDPR / CCPA: customer-list upload requires consent basis. EU residents must opt-in to marketing-list use. Document consent source per record.

### Audience exhaustion
Cold pool finite. After 6-8 weeks of heavy cold-LAL spend, frequency climbs + ROAS drops. Refresh seed; expand to LAL-5%; layer broad/Advantage+; add new platforms.

### Exclusion ladder
Always exclude:
- Past purchasers (window depends on AOV / repeat cycle)
- Current customer list
- Bounced/unsubscribed contacts (from ESP) to avoid double-burning

### LAL country limitation
LAL is country-bounded. LAL-1% US is different from LAL-1% UK. Create per-country LAL audience.

### Advantage+ Audience disables LAL
On Meta, enabling Advantage+ Audience overrides your LAL targeting (Meta auto-decides). Mutually exclusive within an adset.

## Sources

- Meta Custom Audiences: https://www.facebook.com/business/help/164749007013531
- Meta Lookalike Audiences: https://www.facebook.com/business/help/164749007013531
- Meta Advantage+ Audience: https://www.facebook.com/business/help/644904207708731
- Google Customer Match: https://support.google.com/google-ads/answer/6379332
- TikTok Custom Audiences: https://business-api.tiktok.com/portal/docs?id=1739940572493825
- LinkedIn Matched Audiences: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/advertising-targeting/create-and-manage-segments
- SHA-256 hashing format: https://developers.facebook.com/docs/marketing-api/audiences/guides/customer-list-audiences#hash
