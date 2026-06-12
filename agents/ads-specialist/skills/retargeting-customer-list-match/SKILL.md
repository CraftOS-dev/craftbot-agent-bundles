<!--
Source: https://www.facebook.com/business/help/170456843145568
Source: https://support.google.com/google-ads/answer/6379332
Retargeting via Customer Match (Google) / Custom Audiences (Meta) / Matched Audiences (LinkedIn).
-->
# Retargeting + Customer-List Match — SKILL

The highest-ROAS spend channel is people who already know you. **Customer Match** (Google), **Custom Audiences from Customer List** (Meta), **Matched Audiences** (LinkedIn) all share the pattern: hashed-email upload + auto-refresh + platform-native lookback / exclusion. This skill ships the upload pipeline, the weekly refresh cron, and the cart-abandonment audience exclusion design.

## When to use this skill

- **Customer list activation** — upload weekly to all platforms.
- **High-LTV LAL seed refresh** — top 25% LTV customers monthly.
- **Cart abandonment retargeting** — Meta DPA on cart-abandoners minus recent purchases.
- **Cross-sell / cross-pollinate** — past purchasers → complementary product campaign.
- **Win-back / lapsed-customer** — 90-365d inactive customers.
- **Email overlap exclusion** — exclude Klaviyo unsub / bounced to avoid burning.

**Do NOT use this skill when:**
- Pre-launch / no customer data yet — focus cold prospecting first.
- Pure cold prospecting test — exclude retargeting from cold campaign.

## Setup

### Hashing utility (cross-platform)

```bash
# Email: lowercase + trim + SHA-256 hex
hash_email() {
  echo -n "$1" | tr '[:upper:]' '[:lower:]' | tr -d '[:space:]' | sha256sum | awk '{print $1}'
}

# Phone: digits + leading + (E.164) + SHA-256 hex
hash_phone() {
  cleaned="+$(echo "$1" | tr -dc '0-9')"
  echo -n "$cleaned" | sha256sum | awk '{print $1}'
}

hash_email "Alice@Example.com"
# 2bd806c97f0e00af1a1fc3328fa763a9269723c8db8fac4f93af71db186d6e90
```

### Source list pipelines

| Source | Pipeline | Refresh |
|---|---|---|
| HubSpot CRM | hubspot-crm-marketing-mcp (marketing-agent) | weekly |
| Klaviyo | Klaviyo profiles export → CSV → hash | weekly |
| Shopify customers | Shopify Admin GraphQL → hash | weekly |
| PostgreSQL warehouse | SQL on `customers` table → hash | scheduled |
| Salesforce | Salesforce REST API → hash | daily for active campaigns |

### Customer list cohorts to maintain

- **CustomerList_All** — all active customers, weekly refresh
- **CustomerList_Top25_LTV** — top 25% LTV, monthly refresh
- **CustomerList_Lapsed_90_365d** — last purchase 90-365d ago
- **CartAbandoners_7d** — auto via Meta pixel (no upload)
- **Klaviyo_Bounced_Unsub** — exclude list

## Common recipes

### Recipe 1: Customer list export from PostgreSQL → hash

```sql
-- Pull customers from warehouse
SELECT 
  LOWER(TRIM(email)) AS email_norm,
  CONCAT('+', REGEXP_REPLACE(phone, '[^0-9]', '', 'g')) AS phone_e164,
  first_name, last_name, country_code
FROM customers
WHERE last_order_at >= NOW() - INTERVAL '180 days'
  AND email IS NOT NULL
ORDER BY total_lifetime_value DESC;
```

Pipe to CSV then hash:
```python
import csv, hashlib
with open("customers.csv") as f, open("hashed.json","w") as out:
    rows = csv.DictReader(f)
    hashed = []
    for r in rows:
        em = hashlib.sha256(r["email_norm"].encode()).hexdigest()
        ph = hashlib.sha256(r["phone_e164"].encode()).hexdigest() if r["phone_e164"] else None
        hashed.append({"em": em, "ph": ph, "fn": r["first_name"][:1].lower(), 
                       "ln": r["last_name"][:1].lower(), "country": r["country_code"]})
    import json; json.dump(hashed, out)
```

### Recipe 2: Meta — Custom Audience from Customer List

```bash
mcp tool meta-ads.create_custom_audience \
  --name "CustomerList_Top25_LTV_2026Q3" \
  --subtype "CUSTOM" \
  --customer_file_source "USER_PROVIDED_ONLY" \
  --description "Top 25% LTV customers, refreshed weekly" \
  --users_file "@hashed.json"
```

Direct Graph API for `add_users`:
```bash
curl -X POST "https://graph.facebook.com/v19.0/$AUDIENCE_ID/users" \
  -H "Authorization: Bearer $META_ACCESS_TOKEN" \
  -d '{
    "schema": ["EMAIL","PHONE","FN","LN","COUNTRY"],
    "data": [
      ["'$EMAIL_HASH_1'","'$PHONE_HASH_1'","a","x","us"],
      ["'$EMAIL_HASH_2'","'$PHONE_HASH_2'","b","y","us"]
    ]
  }'
```

### Recipe 3: Google Customer Match — create + add users

```bash
# Create user list
list_id=$(mcp tool google-ads.create_audience_list \
  --customer_id "$GOOGLE_ADS_CUSTOMER_ID" \
  --name "CustomerList_Top25_LTV_2026Q3" \
  --type "CRM_BASED" \
  --upload_key_type "CONTACT_INFO" \
  --membership_life_span 540)

# Add hashed users (offline_user_data_jobs)
mcp tool google-ads.add_users_to_audience \
  --audience_list_id "$list_id" \
  --users_file "@google-format.json"
# Format: [{"hashedEmail":"<sha256>","hashedPhoneNumber":"<sha256>",
#           "addressInfo":{"hashedFirstName":"<sha>","hashedLastName":"<sha>","countryCode":"US","postalCode":"10001"}}]
```

Direct API for batch:
```bash
# Create offline user data job
curl -X POST "https://googleads.googleapis.com/v17/customers/$CID/offlineUserDataJobs:create" \
  -H "Authorization: Bearer $GADS_OAUTH" \
  -d '{
    "job": {
      "type": "CUSTOMER_MATCH_USER_LIST",
      "customerMatchUserListMetadata": {
        "userList": "customers/'$CID'/userLists/'$LIST_ID'"
      }
    }
  }'

# Add operations
curl -X POST "https://googleads.googleapis.com/v17/customers/$CID/offlineUserDataJobs/$JOB_ID:addOperations" \
  -d "@operations.json"

# Run
curl -X POST "https://googleads.googleapis.com/v17/customers/$CID/offlineUserDataJobs/$JOB_ID:run"
```

### Recipe 4: TikTok — Custom Audience

```bash
curl -X POST "https://business-api.tiktok.com/open_api/v1.3/dmp/custom_audience/create/" \
  -H "Access-Token: $TT_ACCESS_TOKEN" \
  -d '{
    "advertiser_id":"'$TT_ADVERTISER_ID'",
    "custom_audience_name":"CustomerList_Top25_LTV_2026Q3",
    "calculate_type":"EMAIL_SHA256",
    "file_paths":["'$UPLOADED_FILE'"]
  }'
```

### Recipe 5: LinkedIn — Matched Audience (covered in linkedin-ads-abm-campaigns)

```bash
curl -X POST "https://api.linkedin.com/rest/dmpSegments" \
  -H "Authorization: Bearer $LI_ACCESS_TOKEN" \
  -H "LinkedIn-Version: 202406" \
  -d '{
    "account":"urn:li:sponsoredAccount:'$LI_ACCOUNT_ID'",
    "destinations":[{"destination":"LINKEDIN"}],
    "name":"CustomerList_Top25_LTV_2026Q3",
    "type":"USER"
  }'
```

### Recipe 6: Cart abandonment audience design (Meta)

```bash
# Cart abandoners = ATC events 7d minus Purchase events 7d
mcp tool meta-ads.create_custom_audience \
  --name "CartAbandoners_7d_excl_Purchase_7d" \
  --subtype "WEBSITE" \
  --rule '{
    "inclusions":{"operator":"or","rules":[
      {"event_sources":[{"id":"'$PIXEL_ID'","type":"pixel"}],"retention_seconds":604800,
       "filter":{"operator":"and","filters":[
         {"field":"event","operator":"eq","value":"AddToCart"}]}}
    ]},
    "exclusions":{"operator":"or","rules":[
      {"event_sources":[{"id":"'$PIXEL_ID'","type":"pixel"}],"retention_seconds":604800,
       "filter":{"operator":"and","filters":[
         {"field":"event","operator":"eq","value":"Purchase"}]}}
    ]}
  }'
```

### Recipe 7: Klaviyo overlap exclusion

```python
# Pull Klaviyo bounced/unsubscribed list
import requests
klaviyo_bounced = requests.get(
  "https://a.klaviyo.com/api/lists/$BOUNCED_LIST_ID/profiles/",
  headers={"Authorization": f"Klaviyo-API-Key {KLAVIYO_API_KEY}"}).json()

# Hash + upload as exclusion audience on Meta
hashed = [hashlib.sha256(p["email"].lower().strip().encode()).hexdigest() 
          for p in klaviyo_bounced["data"]]

mcp_call("meta-ads.create_custom_audience", {
  "name": "Klaviyo_Bounced_Unsub_2026Q3",
  "subtype": "CUSTOM",
  "customer_file_source": "USER_PROVIDED_ONLY",
  "users": [{"em": h} for h in hashed]
})

# Add as excluded_custom_audiences on retargeting adsets
mcp_call("meta-ads.update_adset", {
  "adset_id": RETARGETING_ADSET,
  "targeting": {
    "custom_audiences": [{"id": CART_ABANDONER_AUD}],
    "excluded_custom_audiences": [{"id": KLAVIYO_BOUNCED_AUD}, {"id": CUSTOMER_LIST_RECENT}]
  }
})
```

### Recipe 8: Weekly refresh cron — all platforms

```bash
#!/bin/bash
# Run weekly from crontab: 0 5 * * 1 /scripts/refresh-customer-lists.sh

# 1. Pull from warehouse
psql "$DATABASE_URL" -c "
  COPY (
    SELECT LOWER(TRIM(email)) FROM customers
    WHERE last_order_at >= NOW() - INTERVAL '180 days'
  ) TO STDOUT WITH CSV HEADER
" > customers-this-week.csv

# 2. Hash
python /scripts/hash_emails.py customers-this-week.csv > hashed.json

# 3. Push to each platform
mcp_call meta-ads.update_custom_audience --id "$META_AUD_ID" --replace_users "@hashed.json"
mcp_call google-ads.add_users_to_audience --audience_list_id "$GOOGLE_LIST_ID" --replace true --users_file "@hashed-google.json"
curl -X POST "https://business-api.tiktok.com/open_api/v1.3/dmp/custom_audience/update/" \
  -H "Access-Token: $TT_ACCESS_TOKEN" \
  -d '{"advertiser_id":"'$TT_ADVERTISER_ID'","custom_audience_id":"'$TT_AUD_ID'","action":"REPLACE","file_paths":["'$UPLOAD'"]}'
curl -X POST "https://api.linkedin.com/rest/dmpSegments/$LI_SEGMENT_ID/users" \
  -H "Authorization: Bearer $LI_ACCESS_TOKEN" -d "@li-replace-payload.json"

# 4. Notify
curl -X POST "$SLACK_WEBHOOK" -d '{"text":":white_check_mark: Customer-list refresh complete across Meta + Google + TikTok + LinkedIn. List size: '$(wc -l < hashed.json)'"}'
```

## Examples — DTC retargeting structure

```yaml
audiences:
  CustomerList_All:
    refresh: weekly
    purpose: cross-sell + win-back
    platforms: [meta, google, tiktok]
  
  CustomerList_Top25_LTV:
    refresh: monthly
    purpose: LAL seed + VIP retargeting
    platforms: [meta, google, tiktok]
  
  CartAbandoners_7d_excl_Purchase_7d:
    refresh: auto (pixel-based)
    purpose: hot retargeting DPA
    platform: meta
  
  Lapsed_90_365d:
    refresh: weekly
    purpose: win-back campaign
    platforms: [meta, google]
  
  Klaviyo_Bounced_Unsub:
    refresh: weekly
    purpose: exclusion list
    platforms: [meta, google, tiktok]

campaigns:
  hot_retarget_dpa:
    audience: CartAbandoners_7d_excl_Purchase_7d
    exclusion: [Klaviyo_Bounced, CustomerList_recent_purchase_7d]
    creative: DPA catalog template
    bid: min_roas 3.0
    budget: $80/day
  
  cross_sell_top_ltv:
    audience: CustomerList_Top25_LTV
    exclusion: [recent_purchase_30d]
    creative: complementary-product carousel
    bid: lowest_cost
    budget: $40/day
  
  win_back_lapsed:
    audience: Lapsed_90_365d
    exclusion: [CustomerList_recent_purchase_60d, Klaviyo_Bounced]
    creative: "we miss you" + 20% off
    bid: cost_cap CPA $25
    budget: $30/day
```

## Edge cases

### Stale lists drop match rate
60+ days unrefreshed = match rate drops 20%+. Weekly refresh keeps match rate above 70%.

### Match rate by platform
- Meta: 60-80% typical (email + phone + name + country)
- Google: 50-70% typical (email mostly)
- TikTok: 50-65%
- LinkedIn: 30-50% (smaller user base)

### Customer Match minimums
- Meta: 100 to deliver, 1K+ recommended
- Google: 1K minimum
- TikTok: 1K minimum
- LinkedIn: 300 minimum

### Hashing format checklist
All platforms: SHA-256 hex of lowercased + trimmed email/phone. Phone in E.164.

### Consent + privacy
GDPR / CCPA require lawful basis to upload customer data to ad platforms. Document consent type (transactional opt-in vs explicit marketing opt-in). EU residents need marketing-explicit consent.

### Klaviyo overlap exclusion
Bounced / unsubscribed from email = signal they don't want to hear from you. Excluding from paid retargeting avoids burning the relationship.

### Customer Match for cold prospecting
Customer Match audiences are warm/hot by definition (they already converted). Don't use for cold prospecting — use LAL seeded from customer list instead.

### Email-only vs phone+email
Match rate is higher with multi-identifier (email + phone + name + country). Always upload all available identifiers.

### Audience expiration
- Meta: audience persists indefinitely; refresh users via add/remove
- Google: `membership_life_span` defaults 30 days; max 540 days (extend!)
- TikTok: 180 days default

### Suppression list workflow
Track unsubscribes immediately; add to exclusion audiences within 24h. Otherwise unsubscribers see paid ads = brand reputation hit.

### LAL refresh impact
LAL automatically updates as seed audience changes — but only at platform's refresh cadence (weekly typically). Don't expect real-time.

### B2B account-based retargeting (LinkedIn)
Company domain match (not email) for account-based. Maximum 100K companies per segment.

## Sources

- Meta Custom Audiences from Customer List: https://www.facebook.com/business/help/170456843145568
- Meta hashing format: https://developers.facebook.com/docs/marketing-api/audiences/guides/customer-list-audiences
- Google Customer Match: https://support.google.com/google-ads/answer/6379332
- Google Customer Match API: https://developers.google.com/google-ads/api/docs/remarketing/audience-types/customer-match
- Google offline user data jobs: https://developers.google.com/google-ads/api/docs/conversions/upload-customer-match
- TikTok Custom Audiences: https://business-api.tiktok.com/portal/docs?id=1739940572493825
- LinkedIn DMP Segments: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/advertising-targeting/create-and-manage-segments
- Klaviyo Profiles API: https://developers.klaviyo.com/en/reference/get_profiles
- GDPR consent for marketing data: https://gdpr.eu/checklist/
