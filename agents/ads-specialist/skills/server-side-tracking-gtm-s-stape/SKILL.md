<!--
Source: https://developers.google.com/tag-platform/tag-manager/server-side
Source: https://stape.io/blog/google-tag-manager-server-side-setup
GTM Server-side container on Stape (managed) or self-host. CAPI forwarding + event dedup.
-->
# Server-side Tracking (GTM-S + Stape) — SKILL

Server-side tracking is the 2026 default. Browser pixels lose 30-50% of signal to iOS ATT, Safari ITP, ad blockers, and brittle GTM web containers. **GTM Server-side (GTM-S)** on **Stape** (managed) or self-hosted on Cloud Run / Fly.io fixes this by routing browser events through your domain → server → ad platforms with first-party cookies and per-event dedup.

## When to use this skill

- **New account / new property** — set up GTM-S before scaling spend.
- **Pixel signal health < 7/10** — CAPI Gateway via GTM-S is the standard fix.
- **CAPI dedup broken** — `event_id` must flow consistently web → server → platform.
- **Custom-domain mandate** (Safari ITP) — `sgtm.brand.com` for first-party cookies.
- **Multi-platform fan-out** — single event → Meta + TikTok + Google + GA4 in one container.

**Do NOT use this skill when:**
- Pre-tracking setup (configure GTM web client + pixels first).
- Pure mobile-app tracking (use MMP + SKAN postbacks; see `mobile-attribution-skan-appsflyer-adjust-branch`).
- Single-platform / sub-$5K/month — overhead exceeds payoff.

## Setup

### Path A — Stape (managed, recommended for SMB)

```bash
export STAPE_API_KEY="<api-key>"
export STAPE_CONTAINER_ID="<numeric>"
```

Stape pricing: $20-$200/mo. Custom-domain CNAME + 99% uptime + CAPI gateway templates pre-built.

### Path B — Self-host (Cloud Run / Fly.io)

```bash
# Google's official GTM Server image
docker run gcr.io/cloud-tagging-10302018/server:latest \
  -e CONTAINER_CONFIG="<base64-container-config>" \
  -e PORT=8080

# Deploy to Cloud Run
gcloud run deploy gtm-server \
  --image=gcr.io/cloud-tagging-10302018/server:latest \
  --set-env-vars="CONTAINER_CONFIG=$(cat container-config.b64)" \
  --region=us-central1 --platform=managed
```

### Custom domain DNS

```
sgtm.brand.com  CNAME  <stape-host>.stape.io       # Stape
sgtm.brand.com  CNAME  ghs.googlehosted.com         # Cloud Run via Cloud DNS
```

### Architecture

```
Browser → gtag.js / GTM web client → sgtm.brand.com/g/collect
                                          ↓
                              GTM-S Server Container
                                          ↓
              Meta CAPI / TikTok Events / Google EC / GA4 / Custom
```

### Key endpoints

- Server container collect: `https://sgtm.brand.com/g/collect` (GA4 default path)
- Custom endpoint: `https://sgtm.brand.com/{custom-path}`
- Stape API base: `https://api.stape.io/v1`
- Stape container API: `POST /containers`, `GET /containers/{id}`

## Common recipes

### Recipe 1: Create Stape container via API

```bash
curl -X POST "https://api.stape.io/v1/containers" \
  -H "Authorization: Bearer $STAPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "brand-prod-sgtm",
    "url": "sgtm.brand.com",
    "gtm_config_id": "GTM-XXXXXXX",
    "region": "us-central1",
    "tier": "starter"
  }'
```

### Recipe 2: GTM-S container config — CAPI gateway pattern

```yaml
# Saved in GTM Server container (editable in GTM UI; document for repro)
clients:
  - name: GA4 client
    type: gtm-ga4-client
    path: /g/collect

triggers:
  - name: Purchase event
    type: client_event
    filter: event_name == "purchase"

tags:
  - name: Facebook Conversions API
    type: stape-fb-capi-tag
    config:
      pixel_id: "1234567890"
      access_token: "{{Constant - Meta CAPI Token}}"
      event_name: "Purchase"
      event_id: "{{Event Data - event_id}}"
      currency: "{{Event Data - currency}}"
      value: "{{Event Data - value}}"
      user_data:
        em: "{{Event Data - user_data.em}}"
        ph: "{{Event Data - user_data.ph}}"
        client_ip: "{{IP Address}}"
        client_user_agent: "{{User Agent}}"
        fbc: "{{Cookie - _fbc}}"
        fbp: "{{Cookie - _fbp}}"
    triggers: [Purchase event]
  
  - name: TikTok Events API
    type: stape-tiktok-events-tag
    config:
      pixel_code: "{{Constant - TT Pixel}}"
      access_token: "{{Constant - TT Token}}"
      event: "CompletePayment"
      event_id: "{{Event Data - event_id}}"
      value: "{{Event Data - value}}"
      user:
        email: "{{Event Data - user_data.em}}"
        ttp: "{{Cookie - _ttp}}"
    triggers: [Purchase event]
  
  - name: Google Ads Enhanced Conversions
    type: google-ads-conversion
    config:
      conversion_id: "AW-1234567890"
      conversion_label: "abc"
      transaction_id: "{{Event Data - transaction_id}}"
      value: "{{Event Data - value}}"
      currency: "{{Event Data - currency}}"
      user_data: 
        sha256_email_address: "{{Event Data - user_data.em}}"
    triggers: [Purchase event]
  
  - name: GA4 Forward
    type: ga4-server
    config:
      measurement_id: "G-XXXX"
      api_secret: "{{Constant - GA4 API Secret}}"
    triggers: [Purchase event]
```

### Recipe 3: Client-side event with event_id

```javascript
// In your purchase confirmation page (gtag.js)
const eventId = `${user_id}-purchase-${Date.now()}`;

// Pixel-side (Meta)
fbq('track', 'Purchase', {
  value: 99.99, currency: 'USD',
  content_ids: ['sku-abc'], content_type: 'product'
}, { eventID: eventId });

// Pixel-side (TikTok)
ttq.track('CompletePayment', {
  value: 99.99, currency: 'USD', content_id: 'sku-abc',
  event_id: eventId
});

// Server-side via GTM-S (gtag.js fires through sgtm.brand.com)
gtag('event', 'purchase', {
  transaction_id: 'order-12345',
  value: 99.99, currency: 'USD',
  event_id: eventId,
  items: [{item_id: 'sku-abc', price: 99.99, quantity: 1}],
  user_data: {
    email_address: sha256(email),
    phone_number: sha256(phone)
  }
});
```

### Recipe 4: Test event end-to-end

```bash
EVENT_ID="qa-test-$(date +%s)"

curl -X POST "https://sgtm.brand.com/g/collect" \
  -H "Content-Type: application/json" \
  -d '{
    "event_name": "purchase",
    "event_id": "'$EVENT_ID'",
    "currency": "USD", "value": 99.99,
    "user_data": {
      "em": "'$(echo -n test@brand.com | sha256sum | awk "{print \$1}")'"
    },
    "items": [{"item_id":"sku-abc","price":99.99,"quantity":1}]
  }'

# Verify:
# 1. Meta Events Manager → Test Events → search $EVENT_ID → 1 record
# 2. GA4 DebugView → event purchase with event_id
# 3. TikTok Events Manager → real-time test events
# 4. Google Ads Conversions → recent conversions list
```

### Recipe 5: First-party cookie strategy

```javascript
// GTM-S sets first-party cookies that survive Safari ITP
// Configure "Cookie Sync" template in Stape:
// - Cookie name: _ga, _fbp, _ga_<id>, _ttp
// - SameSite: Lax
// - Domain: .brand.com (top-level)
// - Path: /
// - Max-Age: 31536000 (1 year)
// - HttpOnly: false (needed for client JS)
```

### Recipe 6: Stape API — fetch container config / metrics

```bash
# Container info
curl "https://api.stape.io/v1/containers/$STAPE_CONTAINER_ID" \
  -H "Authorization: Bearer $STAPE_API_KEY"

# Last 24h request volume
curl "https://api.stape.io/v1/containers/$STAPE_CONTAINER_ID/stats?period=24h" \
  -H "Authorization: Bearer $STAPE_API_KEY"
```

### Recipe 7: Custom event forwarding — Slack alert from server

```yaml
# GTM-S tag: HTTP Request → Slack webhook on high-value purchase
tags:
  - name: Slack — high-value purchase
    type: http-request
    config:
      url: "{{Constant - Slack webhook}}"
      method: POST
      body_format: json
      body: |
        {
          "text": ":moneybag: High-value purchase: ${{Event Data - value}} | order={{Event Data - transaction_id}} | email_hash={{Event Data - user_data.em}}"
        }
    triggers:
      - name: high_value_purchase
        filter: event_name == "purchase" AND value > 500
```

### Recipe 8: Cloud Run self-host with auto-scaling

```bash
gcloud run deploy gtm-server \
  --image=gcr.io/cloud-tagging-10302018/server:latest \
  --region=us-central1 --platform=managed \
  --set-env-vars="CONTAINER_CONFIG=$CONTAINER_CONFIG_B64,RUN_AS_PREVIEW_SERVER=false" \
  --memory=512Mi --cpu=1 --concurrency=80 \
  --min-instances=1 --max-instances=10 \
  --allow-unauthenticated
```

## Examples — full deployment

```yaml
stack:
  hosting: Stape Starter ($20/mo)
  custom_domain: sgtm.brand.com
  cname_target: <stape-host>.stape.io
  ssl: auto-provision (Stape handles)

container:
  GTM_id: GTM-ABC123 (existing web)
  GTM_server: GTM-XYZ789 (new server)
  
forwarding:
  meta_capi:
    pixel_id: 1234567890
    capi_token: stored in GCP Secret Manager
    events: [Purchase, AddToCart, InitiateCheckout, Lead]
    event_id_template: "{{user_id}}-{{event_name}}-{{timestamp_ms}}"
  
  tiktok_events_api:
    pixel_code: CXXXX
    access_token: stored in Stape Constants
    events: [CompletePayment, AddToCart, ViewContent]
  
  google_enhanced_conversions:
    conversion_id: AW-1234567890
    conversion_label: abc
    user_data_fields: [sha256_email, sha256_phone]
  
  ga4:
    measurement_id: G-XXXX
    api_secret: stored in Stape Constants

cookies:
  first_party: [_ga, _ga_<id>, _fbp, _ttp, _gcl_aw]
  expiry: 1 year (vs ~7d default in Safari)

qa_pre_launch:
  - run Recipe 4 with $EVENT_ID per platform
  - confirm Meta Events Manager test event arrives
  - confirm GA4 DebugView receives
  - confirm TikTok real-time events visible
  - confirm Google Ads conversion log entry
  - confirm event_id matches across all 4
```

## Edge cases

### Dedup requires matching event_id
Meta CAPI dedup requires the same `event_id` from pixel (browser) AND CAPI (server). Without matching, you get 2x conversions reported. Format: stable hash like `{user_id}-{event_name}-{timestamp_ms}`.

### Stape vs self-host cost
Stape: $20-$200/mo, no DevOps, CAPI templates pre-built. Self-host on Cloud Run: $5-$20/mo runtime + your engineering time. SMB default Stape; enterprise prefers self-host for compliance.

### Custom domain mandatory for ITP
Without `sgtm.brand.com`, Safari treats GTM as 3rd-party → cookies truncated to 7d → Meta `_fbp` cookie loss → CAPI match degrades. The domain is non-optional in 2026.

### Container preview / publish workflow
GTM-S preview mode at `?preview=true` shows traffic in GTM UI. Publish via GTM workspace promote. Stape ships publish-via-API capability too.

### Server CPU / memory sizing
GTM Server on Cloud Run: 512MB / 1 vCPU handles ~500 req/s. At 1000+ req/s, scale to 1GB / 2 vCPU + min-instances 2.

### GA4 server-side measurement protocol
Direct server → GA4 via Measurement Protocol:
```bash
curl "https://www.google-analytics.com/mp/collect?measurement_id=G-XXXX&api_secret=XXX" \
  -d '{
    "client_id":"<gtag_cid>",
    "events":[{"name":"purchase","params":{"transaction_id":"x","value":99.99,"currency":"USD"}}]
  }'
```

### CAPI Cloudbridge (alternative to GTM-S)
Meta's own server-side via WordPress / Shopify direct integration. Easier setup, less flexible than GTM-S. Use Cloudbridge for tiny accounts without engineering team.

### Multi-region / latency
For global audiences, deploy GTM-S in multiple regions (Cloud Run multi-region or Stape's geo distribution). Latency > 500ms degrades client UX.

### iOS 17 Link Tracking Protection
Strips known tracking params (`fbclid`, `gclid`, `_kx`) from copied URLs in Mail/Safari. Mitigation: server-side cookie set from URL params on first hit.

### Privacy Sandbox topics
Chrome Privacy Sandbox phases out 3rd-party cookies. GTM-S + first-party cookies are the migration path.

## Sources

- GTM Server-side setup: https://developers.google.com/tag-platform/tag-manager/server-side
- GTM Server architecture: https://developers.google.com/tag-platform/tag-manager/server-side/intro
- Stape blog setup guide: https://stape.io/blog/google-tag-manager-server-side-setup
- Stape API docs: https://stape.io/api
- Meta CAPI dedup: https://developers.facebook.com/docs/marketing-api/conversions-api/deduplicate-pixel-and-server-events
- GA4 Measurement Protocol: https://developers.google.com/analytics/devguides/collection/protocol/ga4
- Cloud Run deploy: https://cloud.google.com/run/docs/quickstarts/deploy-container
- Safari ITP: https://webkit.org/tracking-prevention/
- Privacy Sandbox: https://privacysandbox.com/
