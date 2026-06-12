<!--
Source: https://business-api.tiktok.com/portal/docs?id=1739585377598978
TikTok Marketing API — campaigns, ad groups, ads, Spark Ads, Smart Performance Campaign.
-->
# TikTok Ads — Spark Ads + Smart Performance Campaign — SKILL

TikTok's signature lever is **Spark Ads** (boosted creator posts that look native + outperform in-house creative on CTR / CPM). **Smart Performance Campaign (SPC)** is TikTok's auto-optimization product — their PMax equivalent. This skill covers both plus standard In-Feed and the Events API hookup for iOS signal recovery.

## When to use this skill

- **TikTok-native creative test** — Spark Ads with a creator's organic post.
- **Scale a winning hook** — SPC for auto-optimization across audiences.
- **DTC e-commerce** — In-Feed Ads with TikTok Shop integration or product link.
- **App install** — In-Feed Ads with App Install objective (uses MMP attribution).
- **B2B with TikTok presence** — In-Feed targeting professional interests (smaller pool but growing).
- **Account audit** — pull campaign / ad group / ad reporting via Marketing API.

**Do NOT use this skill when:**
- Non-TikTok (see Meta / Google / LinkedIn / Reddit skills).
- Brand-safety sensitive vertical (financial / healthcare claims) without legal review.

## Setup

### MCP — community `tiktok-ads-mcp`

```bash
# OAuth + advertiser approval first at https://ads.tiktok.com/marketing_api/
export TT_ACCESS_TOKEN="<long-lived-token>"
export TT_ADVERTISER_ID="<numeric>"
export TT_PIXEL_CODE="<pixel>"
```

```json
// claude-config.json
{
  "tiktok-ads": {
    "command": "npx",
    "args": ["-y","tiktok-ads-mcp@latest"],
    "env": {
      "TT_ACCESS_TOKEN": "${TT_ACCESS_TOKEN}",
      "TT_ADVERTISER_ID": "${TT_ADVERTISER_ID}"
    }
  }
}
```

### Marketing API base + key endpoints

- Base: `https://business-api.tiktok.com/open_api/v1.3`
- Campaigns: `POST /campaign/create/`
- Ad groups: `POST /adgroup/create/`
- Ads: `POST /ad/create/`
- Spark Ads: `POST /ad/create/` with `identity_type: AUTH_CODE`
- Custom audiences: `POST /dmp/custom_audience/create/`
- Events API: `POST /event/track/`
- Reporting: `POST /report/integrated/get/`

### Spark Ads auth_code

Get from creator via:
1. **TikTok Creator Marketplace (TCM)** — formal whitelist with budget commitment.
2. **Creator self-serve TikTok app** — Creator Tools → Authorize Ads → generate code → share with advertiser.

`auth_code` valid 7 days; convert to `tiktok_item_id` permanent reference.

## Common recipes

### Recipe 1: SPC (Smart Performance Campaign) — DTC e-com

```bash
# Campaign — SPC objective + auto budget
curl -X POST "https://business-api.tiktok.com/open_api/v1.3/campaign/create/" \
  -H "Access-Token: $TT_ACCESS_TOKEN" \
  -d '{
    "advertiser_id": "'$TT_ADVERTISER_ID'",
    "campaign_name": "SPC-DTC-Q3",
    "objective_type": "CONVERSIONS",
    "budget_mode": "BUDGET_MODE_DAY",
    "budget": 300,
    "campaign_type": "SMART_PERFORMANCE_CAMPAIGN"
  }'

# Ad group — single per SPC; minimal targeting (TikTok decides)
curl -X POST "https://business-api.tiktok.com/open_api/v1.3/adgroup/create/" \
  -H "Access-Token: $TT_ACCESS_TOKEN" \
  -d '{
    "advertiser_id": "'$TT_ADVERTISER_ID'",
    "campaign_id": "'$CAMPAIGN_ID'",
    "adgroup_name": "SPC-DTC-AG",
    "promotion_type": "WEBSITE",
    "pixel_id": "'$TT_PIXEL_CODE'",
    "optimization_event": "COMPLETE_PAYMENT",
    "billing_event": "OCPM",
    "bid_type": "BID_TYPE_NO_BID",
    "location_ids": ["6252001"],
    "auto_targeting_enabled": true
  }'

# Ad — multiple creative concepts attached to single ad group
curl -X POST "https://business-api.tiktok.com/open_api/v1.3/ad/create/" \
  -H "Access-Token: $TT_ACCESS_TOKEN" \
  -d '{
    "advertiser_id": "'$TT_ADVERTISER_ID'",
    "adgroup_id": "'$ADGROUP_ID'",
    "creatives": [
      {"ad_name":"SPC-V1-HookA","ad_format":"SINGLE_VIDEO","video_id":"'$VIDEO_ID_1'",
       "ad_text":"Tap to shop the viral skincare routine","call_to_action":"SHOP_NOW",
       "landing_page_url":"https://brand.com/lp?utm_source=tiktok&utm_medium=paid&utm_campaign=spc-q3&utm_content=v1-hookA"},
      {"ad_name":"SPC-V2-HookB","ad_format":"SINGLE_VIDEO","video_id":"'$VIDEO_ID_2'",
       "ad_text":"This $19 product replaced my $200 routine","call_to_action":"LEARN_MORE",
       "landing_page_url":"https://brand.com/lp?utm_source=tiktok&utm_medium=paid&utm_campaign=spc-q3&utm_content=v2-hookB"}
    ]
  }'
```

### Recipe 2: Spark Ad — boost creator post

```bash
# Creator authorizes via TikTok app → emails you the auth_code
# Step 1: Get tiktok_item_id from auth_code
curl "https://business-api.tiktok.com/open_api/v1.3/tt_user/info/?auth_code=$AUTH_CODE&advertiser_id=$TT_ADVERTISER_ID" \
  -H "Access-Token: $TT_ACCESS_TOKEN"

# Step 2: Use the creator's post as Spark Ad
curl -X POST "https://business-api.tiktok.com/open_api/v1.3/ad/create/" \
  -H "Access-Token: $TT_ACCESS_TOKEN" \
  -d '{
    "advertiser_id": "'$TT_ADVERTISER_ID'",
    "adgroup_id": "'$ADGROUP_ID'",
    "creatives": [{
      "ad_name": "Spark_Creator_HannahLee_HookA",
      "ad_format": "SINGLE_VIDEO",
      "identity_type": "AUTH_CODE",
      "identity_authorized_bc_id": "'$AUTH_CODE'",
      "tiktok_item_id": "'$POST_ID'",
      "call_to_action": "SHOP_NOW",
      "landing_page_url": "https://brand.com/lp?utm_source=tiktok&utm_medium=paid&utm_campaign=spark-jul26&utm_content=hannahlee-hookA"
    }]
  }'
```

### Recipe 3: TikTok Events API — server-side Purchase event

```bash
curl -X POST "https://business-api.tiktok.com/open_api/v1.3/event/track/" \
  -H "Access-Token: $TT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pixel_code": "'$TT_PIXEL_CODE'",
    "event": "CompletePayment",
    "event_id": "user123-purchase-'$(date +%s%3N)'",
    "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",
    "context": {
      "ad": {"callback": "'$TTCLID'"},
      "page": {"url": "https://brand.com/checkout/complete"},
      "user": {
        "email": "'$EMAIL_SHA256'",
        "phone_number": "'$PHONE_SHA256'",
        "ttp": "'$TTP_COOKIE'"
      },
      "ip": "'$CLIENT_IP'",
      "user_agent": "'$USER_AGENT'"
    },
    "properties": {
      "currency": "USD",
      "value": 99.99,
      "content_id": "sku-abc",
      "content_type": "product"
    }
  }'
```

### Recipe 4: Custom audience — hashed email upload

```bash
# Create custom audience
curl -X POST "https://business-api.tiktok.com/open_api/v1.3/dmp/custom_audience/create/" \
  -H "Access-Token: $TT_ACCESS_TOKEN" \
  -d '{
    "advertiser_id": "'$TT_ADVERTISER_ID'",
    "custom_audience_name": "CustomerList_TopLTV_2026Q3",
    "calculate_type": "EMAIL_SHA256",
    "file_paths": ["'$UPLOADED_FILE_PATH'"]
  }'

# Lookalike from custom audience
curl -X POST "https://business-api.tiktok.com/open_api/v1.3/dmp/custom_audience/lookalike/create/" \
  -H "Access-Token: $TT_ACCESS_TOKEN" \
  -d '{
    "advertiser_id": "'$TT_ADVERTISER_ID'",
    "custom_audience_id": "'$SEED_AUDIENCE_ID'",
    "lookalike_audience_name": "LAL_TopLTV_3pct",
    "lookalike_spec": {"location":["US"],"lookalike_extents":"NARROW"}
  }'
```

### Recipe 5: Reporting — last 7d ad performance

```bash
curl -X POST "https://business-api.tiktok.com/open_api/v1.3/report/integrated/get/" \
  -H "Access-Token: $TT_ACCESS_TOKEN" \
  -d '{
    "advertiser_id": "'$TT_ADVERTISER_ID'",
    "report_type": "BASIC",
    "data_level": "AUCTION_AD",
    "dimensions": ["ad_id","stat_time_day"],
    "metrics": ["spend","impressions","clicks","ctr","cpc","conversion","cost_per_conversion","roas"],
    "start_date": "'$(date -u -d "-7 days" +%Y-%m-%d)'",
    "end_date": "'$(date -u +%Y-%m-%d)'"
  }'
```

### Recipe 6: Creative refresh cadence (weekly)

```python
# TikTok burns creative ~2x faster than Meta. Weekly cadence.
import requests, json, os
from datetime import datetime, timedelta

# Pull last 7d frequency / CTR
yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
week_ago = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")

r = requests.post(
  "https://business-api.tiktok.com/open_api/v1.3/report/integrated/get/",
  headers={"Access-Token": os.environ["TT_ACCESS_TOKEN"]},
  json={
    "advertiser_id": os.environ["TT_ADVERTISER_ID"],
    "report_type": "BASIC",
    "data_level": "AUCTION_AD",
    "dimensions": ["ad_id"],
    "metrics": ["spend","impressions","clicks","ctr","frequency"],
    "start_date": week_ago, "end_date": yesterday})

# Pause ads with frequency > 2.5 OR CTR drop > 25% week-over-week
for ad in r.json()["data"]["list"]:
    if ad["metrics"]["frequency"] > 2.5:
        requests.post(
          "https://business-api.tiktok.com/open_api/v1.3/ad/update/status/",
          headers={"Access-Token": os.environ["TT_ACCESS_TOKEN"]},
          json={"advertiser_id": os.environ["TT_ADVERTISER_ID"],
                "ad_ids": [ad["dimensions"]["ad_id"]],
                "operation_status": "DISABLE"})
```

## Examples — DTC creator-led launch

```yaml
strategy:
  total_budget: $500/day
  phase_1_creator_validation:
    duration: 14d
    budget: $200/day
    creative: 5 Spark Ads from 5 mid-tier creators (10K-100K followers)
    objective: Conversions
    targeting: minimal (TikTok auto)
    success_signal: ROAS > 1.8 at day-14
  phase_2_scale:
    triggered_when: phase 1 ROAS > 1.8
    budget: $500/day
    creative: Top 2 Spark Ads + 2 in-house variants
    structure: SPC campaign with all winners
    objective: Conversions
  phase_3_diversify:
    triggered_when: phase 2 sustains ROAS > 2.0 for 7d
    budget: $800/day
    creative: New creator cohort + DPA from TikTok Shop catalog
```

## Edge cases

### Spark Ads auth_code expiry
`auth_code` valid 7 days. After expiry, ad keeps running BUT can't be cloned. Save `tiktok_item_id` for permanent reference.

### Optimization event volume
Need ≥50 events/week for the optimization event to learn. If conversion volume is too low, use Add-to-Cart or ViewContent as proxy and re-aim at Purchase when volume permits.

### SPC vs manual creative testing
SPC auto-optimizes across creative — clean reads impossible. For testing, use standard campaigns with Reach + Frequency objective or split-test API.

### iOS attribution post-ATT
TikTok pixel signal drops 30-50% on iOS without Events API. Always pair pixel with server-side Events API for `event_id` dedup.

### TikTok Shop integration
For sellers — connect TikTok Shop catalog → DPA-style ads. Requires TikTok Shop merchant approval (US, UK, SEA markets primarily).

### Min bid + min budget
$20/day per ad group floor for Conversion objective. Smaller blocks delivery in SPC.

### Rate limits
600 calls / minute / advertiser. Bulk endpoints lower the cost.

### Identity type for Spark vs regular
`identity_type: AUTH_CODE` = Spark Ads (creator account). `identity_type: CUSTOMIZED_USER` = brand-account-owned post. `identity_type: TT_USER` = unbranded organic.

### CTR benchmarks 2026
TikTok In-Feed: 1.0-2.5% typical, 3%+ winning. Spark Ads: 2.5-4.5% typical (creator UGC outperforms). Below 0.5% — kill.

### Frequency cap
TikTok DOES NOT honor frequency caps the way Meta does. Use ad rotation by pausing and swapping rather than relying on caps.

## Sources

- TikTok Marketing API portal: https://business-api.tiktok.com/portal/docs?id=1739585377598978
- Spark Ads: https://ads.tiktok.com/help/article?aid=10000357
- Smart Performance Campaign: https://ads.tiktok.com/help/article/smart-performance-campaign
- TikTok Events API: https://business-api.tiktok.com/portal/docs?id=1739585696931842
- Custom audiences: https://business-api.tiktok.com/portal/docs?id=1739940572493825
- Reporting API: https://business-api.tiktok.com/portal/docs?id=1738864897074690
- TikTok Creator Marketplace: https://creatormarketplace.tiktok.com/
