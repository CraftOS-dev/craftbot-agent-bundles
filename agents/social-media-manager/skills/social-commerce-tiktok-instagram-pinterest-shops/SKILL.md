<!--
Source: https://developers.tiktok.com/doc/research-api-specs-query-tiktok-shop-info
Instagram Graph (commerce): https://developers.facebook.com/docs/commerce-platform
Pinterest Catalogs / Shop: https://developers.pinterest.com/docs/api/v5/catalogs/
Shopify hub: https://shopify.dev/docs/api
Role.md "Social commerce setup"
-->
# Social Commerce — TikTok Shop + IG Shop + Pinterest Shop + Shopify Hub — SKILL

Shopify catalog as single source of truth → sync to Meta Commerce (IG / FB Shop), TikTok Seller Center, Pinterest Catalogs, YouTube Shopping. Product tag every commerce post. From July 2026, TikTok mandates 1.5-5% GMV Max ad budget per shop. Attribution via native shop dashboards + UTM via `bitly-utm-campaign-tracking` + PostHog UTM HogQL join.

## When to use this skill

- **Setting up TikTok Shop / IG Shop / Pinterest Shop** for first time.
- **Catalog sync** Shopify → all three from a single Shopify update.
- **Product-tagged content publishing** — IG Reel / TikTok video / Pinterest pin with shoppable tag.
- **Live shopping** — TikTok Live with shop module.
- **Shop performance reporting** — GMV / conversion / attribution per platform.

**Do NOT use this skill when:**
- Brand has no e-commerce — skip; promotion-only content via `platform-native-content-creation`.
- Affiliate creator commerce — uses Creator Marketplace; falls under `influencer-outreach-modash-aspire-grin`.

## Setup

### Shopify Admin API (catalog hub)

```bash
export SHOPIFY_SHOP="your-shop.myshopify.com"
export SHOPIFY_ADMIN_TOKEN="<token>"
# Endpoint: https://$SHOPIFY_SHOP/admin/api/2026-04/
```

Native MCP: `shopify-mcp`.

### Meta Commerce (IG + FB Shop)

```bash
export META_GRAPH_TOKEN="<token>"
export META_CATALOG_ID="<id>"
export META_BUSINESS_ID="<id>"
# Endpoint: https://graph.facebook.com/v20.0/
```

One-time: Meta Commerce Manager > Connect Catalog > Source = Shopify. Approval review 1-3 days.

### TikTok Shop Seller Center

```bash
# Apply: https://seller.tiktok.com/
# Approval window: 1-4 weeks
# Required: business docs, tax info, fulfillment plan, US sales tax (per state) or country VAT
export TIKTOK_SHOP_ACCESS_TOKEN="<oauth-token>"
export TIKTOK_SHOP_ID="<shop-id>"
# Endpoint: https://open-api.tiktokglobalshop.com/
```

Shopify app: TikTok Shop Shopify connector (free, official).

### Pinterest API v5 (Catalogs)

```bash
export PINTEREST_ACCESS_TOKEN="<oauth-token>"
export PINTEREST_AD_ACCOUNT_ID="<id>"
# Endpoint: https://api.pinterest.com/v5/
```

### YouTube Shopping (channel ≥ 10k subs)

```bash
# Configuration via Shopify YouTube Shopping app
# YouTube Studio → Earn → Shopping → Connect store
```

### Notion Catalog Sync Status DB

Columns: `Product ID / Shopify SKU / IG product ID / TikTok SPU ID / Pinterest product ID / Last sync / Sync status (synced/pending/error) / Error message`.

## Common recipes

### Recipe 1: Initial Shopify → Meta Catalog sync

```bash
# Meta Commerce Manager auto-syncs every 12 hrs when Shopify connected
# To force sync via API:
curl -X POST "https://graph.facebook.com/v20.0/$META_CATALOG_ID/external_event_sources" \
  -H "Authorization: Bearer $META_GRAPH_TOKEN" \
  -d "data_feed_url=https://$SHOPIFY_SHOP/products.json"
```

### Recipe 2: IG Reel with product tag

```bash
# Step 1: list catalog products
curl -G "https://graph.facebook.com/v20.0/$IG_BUSINESS_ID/catalog_product_search" \
  -d "catalog_id=$META_CATALOG_ID" \
  -d "q=brand new sneakers" \
  -d "access_token=$META_GRAPH_TOKEN"

# Step 2: create Reel container with product_tags
curl -X POST "https://graph.facebook.com/v20.0/$IG_BUSINESS_ID/media" \
  -d "media_type=REELS" \
  -d "video_url=https://cdn.example.com/reel.mp4" \
  -d "caption=Just dropped: my new sneakers" \
  -d "product_tags=[{\"product_id\":\"$PROD_ID\",\"x\":0.5,\"y\":0.8}]" \
  -d "access_token=$META_GRAPH_TOKEN"

# Step 3: publish
curl -X POST "https://graph.facebook.com/v20.0/$IG_BUSINESS_ID/media_publish" \
  -d "creation_id=<container>" \
  -d "access_token=$META_GRAPH_TOKEN"
```

### Recipe 3: TikTok Shop product upload

```bash
# Upload single product (SPU)
curl -X POST "https://open-api.tiktokglobalshop.com/product/202309/products/save_draft" \
  -H "x-tts-access-token: $TIKTOK_SHOP_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Premium Sneakers",
    "description": "<html>...</html>",
    "category_id": "601226",
    "brand_id": "<brand_id>",
    "main_images": [{"uri":"<tiktok_image_uri>"}],
    "skus": [{
      "seller_sku":"SHOE-001-RED-9",
      "price":{"amount":"99.99","currency":"USD"},
      "inventory":[{"warehouse_id":"<wh_id>","quantity":50}],
      "sales_attributes":[{"name":"Color","value_name":"Red"},
                          {"name":"Size","value_name":"9"}]
    }]
  }'

# Submit for review
curl -X POST "https://open-api.tiktokglobalshop.com/product/202309/products/$PRODUCT_ID/listings/listing" \
  -H "x-tts-access-token: $TIKTOK_SHOP_ACCESS_TOKEN"
```

### Recipe 4: TikTok video with Shop product tag

```bash
# After Recipe 3 / Recipe 1 of format-specific skill, attach product
curl -X POST "https://open-api.tiktokglobalshop.com/content/202405/videos/$VIDEO_ID/products" \
  -H "x-tts-access-token: $TIKTOK_SHOP_ACCESS_TOKEN" \
  -d '{"product_ids":["<tiktok_product_id>"]}'
```

### Recipe 5: Pinterest pin → product

```bash
# Create product pin (catalog-linked)
curl -X POST https://api.pinterest.com/v5/pins \
  -H "Authorization: Bearer $PINTEREST_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "board_id":"<board_id>",
    "media_source": {
      "source_type":"image_url",
      "url":"https://cdn.example.com/pin.jpg"
    },
    "title":"Premium Sneakers — fall collection",
    "description":"Hand-stitched. Vegan leather. Ships free over $50.",
    "link":"https://yourshop.com/products/sneakers-001?utm_source=pinterest&utm_medium=organic_pin",
    "product_metadata":{"sku":"SHOE-001-RED-9","item_id":"SHOE-001"}
  }'
```

### Recipe 6: Pinterest catalog feed via Shopify

Pinterest auto-discovers Shopify product feed at `https://$SHOP/.well-known/pinterest-tag.txt` once connected. Approval typically 24-72 hrs.

```bash
# Trigger manual feed refresh
curl -X POST "https://api.pinterest.com/v5/catalogs/feeds" \
  -H "Authorization: Bearer $PINTEREST_ACCESS_TOKEN" \
  -d '{
    "name":"shopify-feed",
    "format":"XML",
    "location":"https://$SHOPIFY_SHOP/admin/feeds/pinterest.xml",
    "country":"US",
    "language":"EN"
  }'
```

### Recipe 7: Live shopping (TikTok Live with shop module)

```bash
# 1. Schedule TikTok Live (manual via Seller Center or API)
curl -X POST "https://open-api.tiktokglobalshop.com/live/202405/sessions/create" \
  -H "x-tts-access-token: $TIKTOK_SHOP_ACCESS_TOKEN" \
  -d '{
    "title":"Summer Drop Live",
    "scheduled_at":"2026-06-20T19:00:00Z",
    "product_ids":["<id1>","<id2>","<id3>"]
  }'
```

### Recipe 8: GMV Max ads (mandatory from July 2026)

```bash
# Create GMV Max campaign — TikTok's auto-bidding shop ads
curl -X POST "https://business-api.tiktok.com/open_api/v1.3/gmv_max/campaign/create/" \
  -H "Access-Token: $TIKTOK_ADS_TOKEN" \
  -d '{
    "advertiser_id":"<id>",
    "campaign_name":"Summer-Drop-GMV-Max",
    "objective_type":"GMV_MAX",
    "budget_mode":"BUDGET_MODE_DAY",
    "budget":150.00,
    "shop_id":"<TIKTOK_SHOP_ID>"
  }'
```

Budget rule: 1.5-5% of shop GMV (mandatory threshold). $100k GMV/mo shop = $1.5k-$5k/mo GMV Max budget.

### Recipe 9: Attribution — UTM + native dashboard

```python
# Per platform, per shop post, append UTM
UTM = "?utm_source={platform}&utm_medium={medium}&utm_campaign={campaign}&utm_content={asset_id}"
# Pinterest organic = utm_medium=organic_pin
# IG shop tap = native source (Shopify shows "Instagram Shop" referrer)
# TikTok organic shop = native source

# Join attribution via PostHog HogQL
query = """
SELECT properties.utm_source, count(*) AS sessions, sum(properties.revenue) AS gmv
FROM events
WHERE event = 'purchase' AND timestamp > now() - INTERVAL 30 DAY
GROUP BY properties.utm_source
ORDER BY gmv DESC
"""
mcp tool posthog.query --hogql "$query"
```

### Recipe 10: Daily catalog-sync watchdog

```python
for product in shopify.get_products():
    meta_match = meta_catalog.get_product(retailer_id=product['id'])
    tt_match = tiktok_shop.search_products(seller_sku=product['variants'][0]['sku'])
    pin_match = pinterest.search_products(sku=product['variants'][0]['sku'])
    
    sync_state = {
        'product_id': product['id'],
        'shopify_sku': product['variants'][0]['sku'],
        'ig_product_id': meta_match['id'] if meta_match else None,
        'tiktok_spu_id': tt_match[0]['id'] if tt_match else None,
        'pinterest_id': pin_match[0]['id'] if pin_match else None,
        'sync_status': 'synced' if all([meta_match, tt_match, pin_match]) else 'pending',
        'last_sync': datetime.utcnow()
    }
    notion.upsert(catalog_sync_db, sync_state)
```

## Examples

### Example A: TikTok Shop launch checklist

```yaml
week_-4: apply at seller.tiktok.com
week_-3: business verification (docs, tax, EIN/VAT)
week_-2: connect Shopify via TikTok Shop Shopify app
week_-1: upload product catalog (50-100 SKUs)
week_-1: test product page rendering on TikTok shop tab
week_-1: schedule launch GMV Max campaign with $50/day budget
launch_day: brand TikTok video with product tag + creator drops
post_launch: daily GMV check; bid up GMV Max if ROAS > 3x
```

### Example B: IG Shop weekly content cadence

```yaml
mon: Reel — product demo with tag
tue: Carousel — product story with multi-tag (max 5 products per slide)
wed: Story — poll about product preference + product tag
thu: Reel — UGC repost with product tag
fri: Static post — product hero shot with tag
sat-sun: Stories only (organic awareness)
```

### Example C: Pinterest seasonal campaign

```yaml
campaign: fall_drop_2026
prep: 50 pins designed (1000x1500); each links to product page with UTM
seed: post 10 pins/day for 5 days
ads: Shopping Ads on top-performer pins after 7-day organic test
target: 8% click-through to product page (above 2-3% benchmark)
```

## Edge cases

### TikTok Shop seller approval delays
Common: tax-document mismatch, fulfillment-address gap, bank verification stall. Pre-flight checklist: EIN/VAT confirmed, business address verified, bank account in business name, sales tax registered per state if US.

### GMV Max mandatory threshold (July 2026 onward)
Skipping GMV Max may result in suppressed organic shop reach. Budget 1.5-5% GMV minimum. Below 1.5%, no enforcement; 0% spend, organic shop visibility drops ~40% (TikTok internal data).

### Meta Commerce review queue
Commerce eligibility review 3-10 business days. Common rejections: prohibited categories (CBD, supplements with health claims, weapons), policy text issues (no shipping/returns policy on product page).

### Product spec mismatch
TikTok Shop requires `main_images` min 800x800; Meta requires 500x500; Pinterest requires 1000x1500. Use highest spec (Pinterest 2:3 vertical) and platform auto-crops.

### Catalog feed XML errors
Pinterest most strict on feed validation. Required fields: `g:id`, `g:title`, `g:description`, `g:link`, `g:image_link`, `g:availability`, `g:price`, `g:condition`, `g:brand`. Shopify feed auto-generates; manual feeds need explicit fields.

### Currency mismatch
TikTok Shop seller account is locale-specific. US seller = USD-only. EU sellers can multi-currency via TikTok Shop EU. Don't mix currencies in single catalog feed.

### Product variant explosion
A product with 10 colors × 10 sizes = 100 SKU variants. TikTok Shop caps at 100 SKUs per SPU. Meta catalog handles up to 200 variants. Pinterest doesn't differentiate variants in pin metadata.

### Live shopping prep
TikTok Live Shopping requires verified seller + ≥ 1k followers + commerce permission. Live session must have product gallery loaded pre-go-live; can't add mid-stream.

### IG shop tap attribution loss
"Tap to view on website" carries Instagram referrer but loses UTM after redirect on some old Safari. Use server-side first-party tracking (PostHog) + Meta Conversions API for cross-domain.

### YouTube Shopping eligibility
Requires channel ≥ 10k subs, monetization enabled, Shopify integration. Smaller channels can't unlock Shopping shelf.

### Shopify shop policies + page
Connect via Shopify to Meta / TikTok / Pinterest requires return policy, shipping policy, contact info on storefront. Audit before connecting.

### Cross-platform inventory sync race
If a SKU sells on TikTok Shop, Shopify inventory updates may not propagate to IG / Pinterest immediately. Set Shopify as inventory authority; force re-sync via Recipe 1 for stockouts.

### TikTok Shop cookie window
TikTok attributes purchases within a 14-day click window. IG Shop default 7-day click + 1-day view. Pinterest 30-day click + 1-day view. Use platform-specific attribution windows for ROAS reporting.

### Sales tax / VAT compliance
Each marketplace handles differently. TikTok Shop US: TikTok collects + remits in states with marketplace facilitator laws (most). EU: VAT seller-of-record per country. Pinterest / IG Shop: seller responsible.

## Sources

- **TikTok Shop API**: https://developers.tiktok.com/doc/research-api-specs-query-tiktok-shop-info
- **TikTok Seller Center**: https://seller.tiktok.com/
- **Instagram Commerce (Graph API)**: https://developers.facebook.com/docs/commerce-platform
- **Meta Commerce Manager**: https://www.facebook.com/commerce_manager/
- **Pinterest Catalogs API**: https://developers.pinterest.com/docs/api/v5/catalogs/
- **Shopify Admin API**: https://shopify.dev/docs/api/admin
- **YouTube Shopping**: https://support.google.com/youtube/answer/12120292
- **Social commerce 2026 market**: https://blog.lueurexterne.com/en/blog/social-commerce-in-2026-how-to-sell-on-instagram-tiktok-pinterest/
- **TikTok GMV Max launch (July 2026)**: https://www.keyapi.ai/blog/tiktok-shop-api-integration-guide-sellers/
