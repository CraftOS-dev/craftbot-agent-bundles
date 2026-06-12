<!--
Source: https://www.appsflyer.com/resources/guides/skadnetwork-4/
SKAN 4.0 conversion-value schema + MMP integration (AppsFlyer / Adjust / Branch / Singular).
-->
# Mobile Attribution — SKAN 4.0 + AppsFlyer / Adjust / Branch / Singular — SKILL

iOS 14.5+ broke mobile attribution. **SKAN 4.0** (SKAdNetwork) is Apple's privacy-preserving alternative — 3 postback windows (0-2d, 3-7d, 8-35d) with coarse/fine conversion values, crowd-anonymity threshold. **MMPs** (AppsFlyer, Adjust, Branch, Singular) decode raw SKAN postbacks + add deterministic cross-channel attribution. This skill ships the SKAN schema design + the MMP API integration.

## When to use this skill

- **Mobile app** advertising — iOS or Android.
- **App install** campaigns on Meta / TikTok / Google.
- **Cross-channel deduplication** for installs.
- **Post-install event tracking** (purchase, retention, LTV).
- **Android Privacy Sandbox** preparation.

**Do NOT use this skill when:**
- Web-only DTC e-com (see CAPI / GTM-S skills).
- Pre-MMP setup — pick MMP first (see vendor comparison below).
- App without iOS — Android privacy sandbox different (see edge cases).

## Setup

### MMP vendor comparison

| MMP | Pros | Cons | Pricing |
|---|---|---|---|
| **AppsFlyer** | Market leader, $0 free up to 50K installs, broad integrations | Premium tier for advanced features ($1K+/mo) | Free → custom |
| **Adjust** | Strong fraud detection + incrementality, Universal Links deep-link | Pricey | $100-$10K+/mo |
| **Branch** | Best deep linking + people-based attribution | Less SKAN feature depth | $0 free + paid |
| **Singular** | Strong SKAN postback decoding + cost aggregation | Smaller integration catalog | $0 free up to 50K |
| **Kochava** | Gaming + CTV (Roku) | Gaming-focused | Custom |
| **Tenjin** | Gaming, low-cost | Limited scope | $0-$1K/mo |

### Tokens / IDs

```bash
# AppsFlyer
export APPSFLYER_DEV_KEY="<dev-key>"
export APPSFLYER_APP_ID_IOS="id1234567890"
export APPSFLYER_APP_ID_ANDROID="com.brand.app"
export APPSFLYER_API_TOKEN="<api-token>"   # for Pull API

# Adjust
export ADJUST_APP_TOKEN="<app-token>"
export ADJUST_API_TOKEN="<api-token>"
```

### SKAN 4.0 postback windows

- **Window 1 (0-2 days)**: coarse OR fine conversion value
- **Window 2 (3-7 days)**: fine conversion value
- **Window 3 (8-35 days)**: fine conversion value
- Crowd anonymity threshold determines coarse vs fine. Low-volume campaign → coarse only.

### SKAN conversion value encoding

- Coarse: 4 values (low / medium / high / very-high)
- Fine: 6 bits (0-63 values) per window

## Common recipes

### Recipe 1: SKAN 4.0 schema design (DTC e-com app)

```yaml
schema_v1:
  window_1_0_2d:
    type: COARSE
    values:
      low:        Install only
      medium:     Install + tutorial complete OR login
      high:       Install + add-to-cart
      very_high:  Install + purchase (any value)
  
  window_2_3_7d:
    type: FINE
    bits: 6   # 64 distinct values
    encoding:
      bit_0_1: retention (0=none, 1=day-3, 2=day-7, 3=both)
      bit_2_5: purchase value bracket
        0: 0 purchases
        1: $0.01-$10
        2: $10-$25
        3: $25-$50
        ...
        15: $500+
  
  window_3_8_35d:
    type: FINE
    bits: 6
    encoding: LTV-day-30 bracket
      0:  $0
      1:  $0-$25
      2:  $25-$50
      ...
      63: $1000+
```

Configure in MMP (AppsFlyer Conversion Value mapping UI) OR via API.

### Recipe 2: AppsFlyer conversion value config (via API)

```bash
curl -X POST "https://api2.appsflyer.com/inappevent/$APPSFLYER_APP_ID_IOS/conversion_values" \
  -H "Authorization: Bearer $APPSFLYER_API_TOKEN" \
  -d '{
    "schema_version": "skan4",
    "windows": [
      {
        "window_index": 0,
        "duration_days": 2,
        "type": "COARSE",
        "values": {
          "LOW":       [{"event":"af_install"}],
          "MEDIUM":    [{"event":"af_tutorial_completion"},{"event":"af_login"}],
          "HIGH":      [{"event":"af_add_to_cart"}],
          "VERY_HIGH": [{"event":"af_purchase"}]
        }
      },
      {
        "window_index": 1,
        "duration_days": 7,
        "type": "FINE",
        "bits": 6
      },
      {
        "window_index": 2,
        "duration_days": 35,
        "type": "FINE",
        "bits": 6
      }
    ]
  }'
```

### Recipe 3: AppsFlyer Pull API — install + event report

```bash
# Installs (last 30d)
curl "https://hq.appsflyer.com/export/$APPSFLYER_APP_ID_IOS/installs_report/v5?\
api_token=$APPSFLYER_API_TOKEN&\
from=$(date -u -d '-30 days' +%Y-%m-%d)&\
to=$(date -u +%Y-%m-%d)&\
additional_fields=match_type,att_status,skadn_campaign_id,skadn_conversion_value"

# In-app events
curl "https://hq.appsflyer.com/export/$APPSFLYER_APP_ID_IOS/in_app_events_report/v5?\
api_token=$APPSFLYER_API_TOKEN&\
from=$(date -u -d '-30 days' +%Y-%m-%d)&\
to=$(date -u +%Y-%m-%d)&\
event_name=af_purchase"

# SKAN postbacks raw
curl "https://hq.appsflyer.com/export/$APPSFLYER_APP_ID_IOS/skadnetwork_postbacks_report/v5?\
api_token=$APPSFLYER_API_TOKEN&\
from=$(date -u -d '-7 days' +%Y-%m-%d)&\
to=$(date -u +%Y-%m-%d)"
```

### Recipe 4: Adjust API — cohort report

```bash
curl "https://api.adjust.com/kpis/v1/$ADJUST_APP_TOKEN?\
user_token=$ADJUST_API_TOKEN&\
start_date=$(date -u -d '-30 days' +%Y-%m-%d)&\
end_date=$(date -u +%Y-%m-%d)&\
kpis=installs,sessions,revenue,ltv_d1,ltv_d7,ltv_d30&\
grouping=network,campaign&\
sandbox=false"
```

### Recipe 5: Raw SKAN postback decode (no MMP)

```python
# Apple sends SKAN postback to NSAdvertisingAttributionReportEndpoint URL
# Format (SKAN 4.0):
postback = {
  "version": "4.0",
  "ad-network-id": "facebook.com",
  "campaign-id": 12345,
  "source-app-id": 1234567890,
  "transaction-id": "abc-def-ghi",
  "postback-sequence-index": 0,           # window 1, 2, or 3
  "fine-conversion-value": 42,            # 0-63
  "coarse-conversion-value": "medium",
  "did-win": true,
  "redownload": false,
  "source-domain": "brand.com",
  "attribution-signature": "MEUCIH..."     # verify cryptographically
}

# Verify signature
import requests
pubkey = requests.get(f"https://api.skadnetwork.apple.com/keys/{postback['ad-network-id']}").json()
# ... verify with ECDSA P-256 ...

# Decode conversion value via schema (Recipe 1)
def decode_value(fcv, window):
    if window == 0:
        return SCHEMA["coarse"][postback["coarse-conversion-value"]]
    elif window == 1:
        retention = fcv & 0b11
        revenue_bracket = (fcv >> 2) & 0b1111
        return {"retention": retention, "revenue_bracket": REVENUE_BRACKETS[revenue_bracket]}
    elif window == 2:
        return {"ltv_d30_bracket": LTV_BRACKETS[fcv]}
```

### Recipe 6: Privacy Sandbox (Android) Attribution Reporting

```javascript
// Web-to-app attribution via ARA on Chrome Android
fetch('https://brand.com/click', {
  attributionReporting: {
    eventSourceEligible: true,
    triggerEligible: false
  },
  headers: {
    "Attribution-Reporting-Eligible": "event-source"
  }
});

// Server response sets attribution source
res.headers["Attribution-Reporting-Register-Source"] = JSON.stringify({
  "source_event_id": "12345",
  "destination": "android-app://com.brand.app",
  "expiry": "604800",
  "priority": "100"
});
```

### Recipe 7: MMP → warehouse pipeline

```bash
# Daily cron: AppsFlyer Pull → S3 → Snowflake
APPSFLYER_PULL_URL="https://hq.appsflyer.com/export/$APP_ID/installs_report/v5?api_token=$APPSFLYER_API_TOKEN&from=$YESTERDAY&to=$YESTERDAY"

curl "$APPSFLYER_PULL_URL" | \
  aws s3 cp - "s3://brand-mmp-raw/appsflyer/installs/$YESTERDAY.csv"

# Snowflake COPY INTO
snowsql -q "COPY INTO mmp_installs FROM '@s3_stage/appsflyer/installs/$YESTERDAY.csv' FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1);"
```

### Recipe 8: SKAN postback campaign mapping

```sql
-- Map SKAN campaign-id → Meta / TikTok / Google campaign for ROAS join
SELECT 
  p.network,
  p.skadn_campaign_id,
  m.campaign_name,
  COUNT(*) AS install_count,
  AVG(p.fine_conversion_value) AS avg_cv
FROM mmp_skan_postbacks p
LEFT JOIN ads_warehouse.meta_campaign_map m 
  ON p.skadn_campaign_id::int = m.skan_campaign_id
WHERE p.window_index = 0
  AND p.postback_date >= CURRENT_DATE - 30
GROUP BY p.network, p.skadn_campaign_id, m.campaign_name
ORDER BY install_count DESC;
```

## Examples — full stack

```yaml
app: brand-shopping-ios + brand-shopping-android
mmp: AppsFlyer (free tier, <50K installs/mo)

skan_schema:
  window_1: COARSE (install / install+tutorial / install+ATC / install+purchase)
  window_2: FINE 6-bit (retention + purchase bracket)
  window_3: FINE 6-bit (LTV-day-30 bracket)

mmp_integrations:
  meta_ads_connected: true
  google_ads_connected: true
  tiktok_ads_connected: true
  applovin: true
  reddit_ads: manual postback config
  
android:
  privacy_sandbox_ARA: configured for Chrome Android
  google_play_install_referrer: enabled

reporting:
  daily_install_pull: AppsFlyer Pull API → Snowflake
  weekly_skan_decode: raw postbacks → conversion-value mapping → warehouse
  monthly_LTV: cohort LTV-d30 vs install spend per campaign

attribution_setup:
  click_window_default: 7d
  view_window_default: 1d
  deterministic_match: IDFA opt-in users only
  probabilistic_match: enabled where allowed (not for SKAN-only)
```

## Edge cases

### Crowd anonymity threshold
Apple won't return fine conversion values if campaign volume is too low. Result: coarse postback only. Solution: aggregate campaign structures into broader "ad network campaign IDs" (max 100 per network in SKAN 4.0).

### SKAN campaign-id mapping
Meta / Google / TikTok each allocate SKAN campaign IDs differently. Maintain a mapping table per platform. Meta uses one SKAN ID per "value-optimized" campaign group.

### Schema lock-in
SKAN conversion value schema changes invalidate prior window data. Plan quarterly schema review; document version + freeze for 90d.

### Self-attribution networks (SAN)
Meta / TikTok / Google self-report installs (deterministic when ATT opted in OR via their own click-id chain). MMP merges SAN + SKAN postbacks; can double-count if not deduped.

### Android Play Install Referrer
Google's android equivalent — pass through MMP for deterministic install attribution. Doesn't need SKAN logic.

### Postback delay
Window 1 fires 0-2d after install + random 24-48h randomization. Window 2: 24-144h after window 1. Window 3: another delay. Total: real-time reporting impossible.

### Source app ID required
Apple SKAN 4.0 requires source app ID (the app that drove the install). Web-to-app via ARA on iOS instead.

### Free tier limits
AppsFlyer free: 50K installs/mo. Singular free: 50K. Beyond → paid. Branch free tier includes deep linking but limited attribution.

### iOS 17.4 source domain
iOS 17.4+ supports "web-to-app" source domain — your domain in postback for first-touch attribution from web → install.

### Probabilistic vs deterministic
Probabilistic (fingerprint-based) is banned by Apple for SKAN; some MMPs use it for non-SKAN traffic (Android, opted-in iOS). Document policy.

### SKAN 5.0 horizon
Apple announced future SKAN changes — track via Apple dev forum + MMP vendor newsletter.

### LAT (Limit Ad Tracking) vs ATT
Pre-iOS 14.5 was LAT (binary opt-out). Post-iOS 14.5 is ATT (per-app opt-in). All MMP logic must handle both eras gracefully.

## Sources

- AppsFlyer SKAN 4.0 guide: https://www.appsflyer.com/resources/guides/skadnetwork-4/
- AppsFlyer Pull API: https://support.appsflyer.com/hc/en-us/articles/207034366
- Apple SKAdNetwork docs: https://developer.apple.com/documentation/storekit/skadnetwork
- Apple postback verification: https://developer.apple.com/documentation/storekit/skadnetwork/verifying_an_install-validation_postback
- Adjust API docs: https://help.adjust.com/en/article/kpi-service
- Branch SDK / postback docs: https://help.branch.io/developers-hub/docs/skadnetwork
- Singular SKAN guide: https://www.singular.net/blog/skadnetwork-guide/
- Privacy Sandbox (Android) ARA: https://developer.android.com/design-for-safety/privacy-sandbox/attribution
- Apple ad attribution policy: https://developer.apple.com/app-store/app-privacy-details/
- Google Play Install Referrer: https://developer.android.com/google/play/installreferrer
