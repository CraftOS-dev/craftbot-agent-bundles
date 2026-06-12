<!--
Source: https://developers.facebook.com/docs/marketing-api/conversions-api
Source: https://business-api.tiktok.com/portal/docs?id=1739585696931842
Source: https://developers.google.com/google-ads/api/docs/conversions/upload-clicks
Server-side conversion APIs: Meta CAPI + TikTok Events + Google Enhanced Conversions.
-->
# Meta CAPI + TikTok Events API + Google Enhanced Conversions — SKILL

The three conversion APIs that recover iOS-ATT / cookie-loss signal. Meta CAPI for Meta family. TikTok Events API for TikTok pixel signal. Google Enhanced Conversions for Web + Leads + Click Conversion Import. This skill ships exact payloads, event_id dedup, AEM 8-event priority on Meta, and the Google offline conversion import path.

## When to use this skill

- **Always** — every account in 2026 should have all three server-side CAPIs live.
- **Account audit** flagging "needs CAPI."
- **iOS signal recovery** — CAPI/server events recover 30-50% of conversions lost to ATT.
- **AEM (Aggregated Event Measurement) configuration** — Meta 8-event priority ranking.
- **Offline conversion import** — CRM-converted lead → Google Click Conversion Import.

**Do NOT use this skill when:**
- Server container not yet deployed (use `server-side-tracking-gtm-s-stape` first).
- App / mobile (use SKAN + MMP via `mobile-attribution-skan-appsflyer-adjust-branch`).

## Setup

### Tokens / IDs per platform

```bash
# Meta
export META_PIXEL_ID="1234567890"
export META_CAPI_TOKEN="<long-lived-system-user-token>"

# TikTok
export TT_PIXEL_CODE="CXXXX"
export TT_ACCESS_TOKEN="<long-lived>"

# Google
export GADS_DEVELOPER_TOKEN="<from-mcc>"
export GADS_OAUTH_TOKEN="<oauth>"
export GADS_CUSTOMER_ID="1234567890"
export CONVERSION_ID="AW-XXXX"
export CONVERSION_LABEL="abc123"
```

### Key endpoints

| Platform | Endpoint |
|---|---|
| Meta CAPI | `POST https://graph.facebook.com/v19.0/{pixel_id}/events` |
| TikTok Events API | `POST https://business-api.tiktok.com/open_api/v1.3/event/track/` |
| Google Click Conversion Import | `POST https://googleads.googleapis.com/v17/customers/{cid}:uploadClickConversions` |
| Google Enhanced Conversions for Web | `gtag('set','user_data',{...})` + Conversion Linker |
| Google Enhanced Conversions for Leads | `POST https://googleads.googleapis.com/v17/customers/{cid}/conversionAdjustments` |

### Event hashing

All user identifiers (email, phone) MUST be SHA-256 of lowercased + trimmed value. Lowercase hex string.

## Common recipes

### Recipe 1: Meta CAPI — Purchase event

```bash
curl -X POST "https://graph.facebook.com/v19.0/$META_PIXEL_ID/events" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [{
      "event_name": "Purchase",
      "event_time": '$(date +%s)',
      "event_id": "'$USER_ID'-purchase-'$(date +%s%3N)'",
      "event_source_url": "https://brand.com/checkout/complete",
      "action_source": "website",
      "user_data": {
        "em": ["'$EMAIL_SHA256'"],
        "ph": ["'$PHONE_SHA256'"],
        "client_ip_address": "'$CLIENT_IP'",
        "client_user_agent": "'$USER_AGENT'",
        "fbc": "'$FBC_COOKIE'",
        "fbp": "'$FBP_COOKIE'",
        "external_id": ["'$USER_ID_HASH'"]
      },
      "custom_data": {
        "currency": "USD",
        "value": 99.99,
        "content_ids": ["sku-abc"],
        "content_type": "product",
        "num_items": 1,
        "order_id": "'$ORDER_ID'"
      },
      "data_processing_options": [],
      "data_processing_options_country": 0,
      "data_processing_options_state": 0
    }],
    "access_token": "'$META_CAPI_TOKEN'",
    "test_event_code": null
  }'
```

### Recipe 2: Meta AEM 8-event priority ranking (post-ATT)

For iOS 14.5+ traffic, Meta enforces Aggregated Event Measurement: max 8 events per domain, ranked 1-8. Only the highest-priority event per user/conversion is reported.

```python
# Set priority via Meta MCP (or Events Manager UI)
priorities = [
  {"event_name": "Purchase",            "priority": 1},
  {"event_name": "InitiateCheckout",    "priority": 2},
  {"event_name": "AddToCart",           "priority": 3},
  {"event_name": "AddPaymentInfo",      "priority": 4},
  {"event_name": "Lead",                "priority": 5},
  {"event_name": "CompleteRegistration","priority": 6},
  {"event_name": "Subscribe",           "priority": 7},
  {"event_name": "ViewContent",         "priority": 8}
]
mcp_call("meta-ads.manage_aem_events", {
  "pixel_id": META_PIXEL_ID, "events": priorities
})
```

Configure value optimization on Purchase → enable revenue-weighted prioritization.

### Recipe 3: TikTok Events API — CompletePayment

```bash
curl -X POST "https://business-api.tiktok.com/open_api/v1.3/event/track/" \
  -H "Access-Token: $TT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pixel_code": "'$TT_PIXEL_CODE'",
    "event": "CompletePayment",
    "event_id": "'$USER_ID'-purchase-'$(date +%s%3N)'",
    "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",
    "context": {
      "ad": {"callback": "'$TTCLID'"},
      "page": {"url": "https://brand.com/checkout/complete","referrer": "https://brand.com/cart"},
      "user": {
        "email": "'$EMAIL_SHA256'",
        "phone_number": "'$PHONE_SHA256'",
        "ttp": "'$TTP_COOKIE'",
        "external_id": "'$USER_ID_HASH'"
      },
      "ip": "'$CLIENT_IP'",
      "user_agent": "'$USER_AGENT'"
    },
    "properties": {
      "currency": "USD",
      "value": 99.99,
      "content_type": "product",
      "content_id": "sku-abc",
      "quantity": 1
    },
    "test_event_code": null
  }'
```

### Recipe 4: Google Enhanced Conversions for Web (client-side gtag)

```javascript
// On purchase confirmation page
gtag('event', 'conversion', {
  'send_to': 'AW-CONVERSION_ID/CONVERSION_LABEL',
  'value': 99.99,
  'currency': 'USD',
  'transaction_id': 'order-12345'
});

// Provide user data for enhanced match (hashed by gtag automatically when configured)
gtag('set', 'user_data', {
  'email': 'alice@example.com',          // gtag will hash
  'phone_number': '+12025550100',
  'address': {
    'first_name': 'Alice',
    'last_name': 'Example',
    'street': '123 Main St',
    'city': 'NYC',
    'region': 'NY',
    'postal_code': '10001',
    'country': 'US'
  }
});
```

Enable in Google Ads → Tools → Conversions → Enhanced Conversions → Set up via Google Tag.

### Recipe 5: Google Click Conversion Import (API-based, offline)

For CRM-converted leads or any post-click conversion that happens off-site.

```bash
curl -X POST "https://googleads.googleapis.com/v17/customers/$GADS_CUSTOMER_ID:uploadClickConversions" \
  -H "Authorization: Bearer $GADS_OAUTH_TOKEN" \
  -H "developer-token: $GADS_DEVELOPER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "conversions": [{
      "gclid": "'$GCLID'",
      "conversion_action": "customers/'$GADS_CUSTOMER_ID'/conversionActions/'$CONVERSION_ACTION_ID'",
      "conversion_date_time": "'$(date -u +%Y-%m-%dT%H:%M:%S%z)'",
      "conversion_value": 99.99,
      "currency_code": "USD",
      "user_identifiers": [
        {"hashed_email": "'$EMAIL_SHA256'"},
        {"hashed_phone_number": "'$PHONE_SHA256'"}
      ],
      "user_agent": "'$USER_AGENT'",
      "order_id": "'$ORDER_ID'"
    }],
    "partial_failure": true
  }'
```

### Recipe 6: Google Enhanced Conversions for Leads (offline upload)

For leads captured via form → converted via sales pipeline.

```bash
curl -X POST "https://googleads.googleapis.com/v17/customers/$GADS_CUSTOMER_ID/conversionAdjustments:uploadConversionAdjustments" \
  -H "Authorization: Bearer $GADS_OAUTH_TOKEN" \
  -H "developer-token: $GADS_DEVELOPER_TOKEN" \
  -d '{
    "conversion_adjustments": [{
      "gclid_date_time_pair": {
        "gclid": "'$GCLID'",
        "conversion_date_time": "'$ORIGINAL_CONVERSION_DATETIME'"
      },
      "adjustment_type": "ENHANCEMENT",
      "user_identifiers": [
        {"hashed_email": "'$EMAIL_SHA256'"}
      ],
      "conversion_action": "customers/'$GADS_CUSTOMER_ID'/conversionActions/'$ACTION_ID'"
    }]
  }'
```

### Recipe 7: Dedup check — event_id flowing pixel + server

```python
# Send paired test event with same event_id from both pixel + CAPI
event_id = f"dedup-test-{int(time.time())}"

# Pixel side via headless browser (mock)
# fbq('track', 'Purchase', {...}, {eventID: event_id})

# CAPI side
requests.post(
  f"https://graph.facebook.com/v19.0/{META_PIXEL_ID}/events",
  json={"data": [{"event_name": "Purchase", "event_id": event_id, ...}],
        "access_token": META_CAPI_TOKEN})

# Wait 60s, query Meta Test Events
# Should see 1 deduped event with event_id. If 2 → dedup broken; fix template.
```

### Recipe 8: GA4 Measurement Protocol — server event

```bash
curl "https://www.google-analytics.com/mp/collect?measurement_id=G-XXXX&api_secret=$GA4_API_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "'$GA4_CLIENT_ID'",
    "user_id": "'$USER_ID'",
    "events": [{
      "name": "purchase",
      "params": {
        "transaction_id": "'$ORDER_ID'",
        "value": 99.99,
        "currency": "USD",
        "items": [{"item_id":"sku-abc","item_name":"Acme Widget","quantity":1,"price":99.99}]
      }
    }]
  }'
```

## Examples — full deployment

```yaml
event_taxonomy:
  client_events_fired:
    - ViewContent (pixel + tag)
    - AddToCart (pixel + tag)
    - InitiateCheckout (pixel + tag)
    - AddPaymentInfo (pixel + tag)
    - Purchase (pixel + tag)
  
  server_events_fired:
    - same as client, via GTM-S → all 4 CAPIs
  
  event_id_format: "${user_id}-${event_name}-${timestamp_ms}"

meta_aem_priorities:
  1: Purchase (value-optimized)
  2: InitiateCheckout
  3: AddToCart
  4: AddPaymentInfo
  5: Lead
  6: CompleteRegistration
  7: Subscribe
  8: ViewContent

google_enhanced_conversions:
  web: enabled (gtag + Conversion Linker)
  leads: enabled (offline import via API, daily cron)
  click_conversion_import: enabled (CRM → API)

tiktok_events_api:
  events_mapped:
    - Purchase → CompletePayment
    - AddToCart → AddToCart
    - InitiateCheckout → InitiateCheckout
  advanced_matching: email + phone + ttp cookie

qa_routine_weekly:
  - run paired pixel+server test event per platform
  - verify event_id dedup in each Events Manager
  - check signal-health score (Meta) > 7
  - check match-rate (TikTok) > 60%
  - check Enhanced Conversions impact (Google Ads → Conversions)
```

## Edge cases

### event_id mismatch
Pixel-side gtag sends `eventID` (camelCase); CAPI sends `event_id` (snake_case). Different field names — but both must produce the SAME string. Common bug: pixel uses `Date.now()` (ms), server uses `int(time.time())` (s) → mismatch.

### Hashing whitespace / case
SHA-256 must be of lowercased + whitespace-trimmed value. `"Alice@Example.com "` and `"alice@example.com"` hash differently. Normalize before hashing.

### Phone format
E.164 international format: `+12025550100`. Local format (`(202) 555-0100`) does not match.

### IP / UA from server
For server-side events, capture `client_ip_address` and `client_user_agent` from the request that triggered the conversion. Meta uses these for match.

### Cookie passing (fbc/fbp/ttp)
Pass cookies in CAPI payload to enable Meta's first-party cookie match. Read from request cookies on server.

### AEM 8-event slot
After exceeding 8, any new event is silently dropped on iOS. Audit before adding new events.

### Value optimization requires CAPI
Meta's value-based bid (Min ROAS) requires CAPI sending purchase value with high signal-quality.

### Google offline conversion gclid lifetime
Click `gclid` valid 90 days for Click Conversion Import. After expiry, conversion can't be uploaded → use Enhanced Conversions for Leads instead.

### TikTok event names differ
TikTok uses `CompletePayment` not `Purchase`. `ClickButton` not `ContentClick`. See TikTok docs for full mapping.

### Test event lag
Meta Test Events: ~30s delay. TikTok: ~60s. Google: ~5 min for Enhanced Conversions to surface in dashboard.

### Data Processing Options (CCPA / GDPR)
For California residents: `data_processing_options: ["LDU"]`. Limits Meta's ability to use the data per CCPA. EU: GDPR consent required — pass via `data_processing_options_country`.

### Rate limits
Meta CAPI: 200 calls/hour/pixel (default); request quota increase if higher. TikTok: 600/minute. Google: 15K ops/day/account.

## Sources

- Meta Conversions API: https://developers.facebook.com/docs/marketing-api/conversions-api
- Meta CAPI parameters: https://developers.facebook.com/docs/marketing-api/conversions-api/parameters
- Meta AEM (Aggregated Event Measurement): https://www.facebook.com/business/help/721422165168319
- TikTok Events API: https://business-api.tiktok.com/portal/docs?id=1739585696931842
- TikTok event mapping: https://business-api.tiktok.com/portal/docs?id=1701890979375106
- Google Enhanced Conversions: https://support.google.com/google-ads/answer/9888656
- Google Click Conversion Import: https://developers.google.com/google-ads/api/docs/conversions/upload-clicks
- Google Conversion Adjustments: https://developers.google.com/google-ads/api/docs/conversions/upload-adjustments
- GA4 Measurement Protocol: https://developers.google.com/analytics/devguides/collection/protocol/ga4
- Meta CAPI dedup: https://developers.facebook.com/docs/marketing-api/conversions-api/deduplicate-pixel-and-server-events
