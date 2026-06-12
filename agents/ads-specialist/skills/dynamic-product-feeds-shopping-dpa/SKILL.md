<!--
Source: https://www.facebook.com/business/help/1670743469549027
Source: https://developers.google.com/shopping-content
Dynamic Product Ads + Shopping + Performance Max retail with Meta Catalog + Google Merchant Center.
-->
# Dynamic Product Feeds — Shopping / DPA / PMax Retail — SKILL

Dynamic product ads (DPA) on Meta + Shopping ads on Google + PMax retail are all fueled by **product feeds** — structured catalogs with id, title, price, image, availability, link. This skill ships feed authoring, **Meta Catalog** + **Google Merchant Center** sync, **Advantage+ Shopping** + **PMax retail** wiring, and the feed-error debugging path.

## When to use this skill

- **E-commerce DTC** with 10+ SKUs and ongoing Meta/Google paid spend.
- **DPA retargeting** of cart abandoners with product they viewed.
- **Advantage+ Shopping campaign** (Meta) — requires catalog.
- **Google Performance Max retail** — Merchant Center primary asset source.
- **Multi-market** catalog (currency / language / shipping per region).

**Do NOT use this skill when:**
- Pre-revenue or single-SKU — manual product ads simpler.
- Pure brand awareness — DPA underperforms for top-funnel.
- Service / digital-only (no physical product).

## Setup

### Feed source options

| Source | Path | Pros | Cons |
|---|---|---|---|
| **Shopify** | native Meta + Google channels | Auto-sync; catalog-as-code | Limited custom field control |
| **WooCommerce** | plugins | Free | Plugin maintenance |
| **Custom JSON / CSV** | `feed.json` URL on your CDN | Max control | Engineering required |
| **Pixel-source-of-truth** | Meta scrapes your product pages | Zero feed maintenance | Slow indexing |

### Required feed fields (Meta + Google common)

```
id              required, unique per product (e.g., shopify product ID + variant)
title           required, ≤150 chars, product name + variant
description     required, ≤5000 chars
link            required, full product URL with UTM
image_link      required, 1200x1200+ preferred
availability    in stock / out of stock / preorder
price           USD currency code: "99.99 USD"
brand           recommended
condition       new / refurbished / used
gtin OR mpn     recommended (UPC / EAN / MPN); strong Google ranking signal
google_product_category  recommended (Google taxonomy ID)
shipping        recommended (Google)
```

### Meta Catalog connections

- Meta Ads MCP: `manage_catalog` tool
- Shopify Meta channel app: auto-sync
- Feed URL: `manage_catalog --feed_url https://brand.com/feed.json --schedule daily_2am_utc`

### Google Merchant Center

- Content API for Shopping: `https://shoppingcontent.googleapis.com/content/v2.1/{merchant_id}/products`
- Shopify Google channel app: auto-sync
- Scheduled feed fetch: Merchant Center → Products → Feeds → primary feed URL

## Common recipes

### Recipe 1: Meta catalog feed creation (custom JSON)

```bash
# Feed file structure
cat > feed.json <<EOF
{
  "products": [
    {
      "id": "sku-abc-blue-m",
      "title": "Acme Cotton Tee — Blue Medium",
      "description": "100% organic cotton, fair trade certified.",
      "availability": "in stock",
      "condition": "new",
      "price": "29.99 USD",
      "link": "https://brand.com/products/acme-tee-blue-m?utm_source=meta&utm_medium=paid&utm_campaign=dpa",
      "image_link": "https://cdn.brand.com/products/acme-tee-blue.jpg",
      "additional_image_link": [
        "https://cdn.brand.com/products/acme-tee-blue-back.jpg",
        "https://cdn.brand.com/products/acme-tee-blue-detail.jpg"
      ],
      "brand": "Acme",
      "gtin": "0123456789012",
      "google_product_category": 1604,
      "color": "Blue",
      "size": "M",
      "material": "100% Organic Cotton"
    }
  ]
}
EOF

# Host at https://brand.com/feed.json (refreshed daily by your platform)

# Register with Meta Catalog via MCP
mcp tool meta-ads.manage_catalog \
  --action "create" \
  --name "Brand-Catalog-2026" \
  --feed_url "https://brand.com/feed.json" \
  --schedule "every_6_hours"

# Create product set for DPA targeting (e.g., "Bestsellers")
mcp tool meta-ads.create_product_set \
  --catalog_id "$CATALOG_ID" \
  --name "Bestsellers_TopLTV" \
  --filter '{
    "retailer_id":{"is_any":["sku-abc-blue-m","sku-abc-red-l","sku-def-green-s"]}
  }'
```

### Recipe 2: Google Merchant Center API — bulk insert products

```bash
# Single product upsert
curl -X POST "https://shoppingcontent.googleapis.com/content/v2.1/$MERCHANT_ID/products" \
  -H "Authorization: Bearer $GMC_OAUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "kind": "content#product",
    "offerId": "sku-abc-blue-m",
    "title": "Acme Cotton Tee — Blue Medium",
    "description": "100% organic cotton, fair trade certified.",
    "link": "https://brand.com/products/acme-tee-blue-m",
    "imageLink": "https://cdn.brand.com/products/acme-tee-blue.jpg",
    "contentLanguage": "en",
    "targetCountry": "US",
    "channel": "online",
    "availability": "in stock",
    "condition": "new",
    "googleProductCategory": "Apparel & Accessories > Clothing > Shirts & Tops",
    "gtin": "0123456789012",
    "brand": "Acme",
    "price": {"value": "29.99", "currency": "USD"},
    "shipping": [{"country": "US", "service": "Standard", "price": {"value": "5.99", "currency": "USD"}}]
  }'

# Batch insert (up to 1000 products per call)
curl -X POST "https://shoppingcontent.googleapis.com/content/v2.1/$MERCHANT_ID/products/batch" \
  -H "Authorization: Bearer $GMC_OAUTH" \
  -d "@batch-products.json"
```

### Recipe 3: Advantage+ Shopping campaign (Meta DPA)

```bash
mcp tool meta-ads.create_campaign \
  --name "Advantage+-Shopping-2026Q3" \
  --objective "OUTCOME_SALES" \
  --advantage_plus_shopping true \
  --special_ad_categories "[]" \
  --daily_budget 10000

mcp tool meta-ads.create_adset \
  --campaign_id "$CAMPAIGN_ID" \
  --name "AdvantagePlus-AllProducts" \
  --daily_budget 0  # CBO controlled
  --optimization_goal "OFFSITE_CONVERSIONS" \
  --billing_event "IMPRESSIONS" \
  --product_set_id "$ALL_PRODUCTS_SET_ID" \
  --targeting '{"geo_locations":{"countries":["US","CA"]}}'

# DPA creative — template auto-populates from catalog
mcp tool meta-ads.create_ad_creative \
  --name "DPA-Catalog-Auto" \
  --product_set_id "$ALL_PRODUCTS_SET_ID" \
  --template_data '{
    "message": "{{product.name}} — {{product.price}}",
    "name": "{{product.name}}",
    "description": "{{product.description}}",
    "call_to_action": {"type":"SHOP_NOW","value":{"link":"{{product.url}}?utm_source=meta&utm_medium=paid&utm_campaign=advantage-plus-dpa"}}
  }'
```

### Recipe 4: Google PMax retail with Merchant Center

```bash
mcp tool google-ads.create_pmax_campaign \
  --customer_id "$GOOGLE_ADS_CUSTOMER_ID" \
  --name "PMax-Retail-2026Q3" \
  --budget_micros 15000000000 \
  --bidding_strategy '{"maximize_conversion_value":{"target_roas":4.0}}' \
  --merchant_center_id "$MERCHANT_ID" \
  --feed_label "US" \
  --customer_acquisition_optimization '{"optimization_mode":"BID_HIGHER_FOR_NEW_CUSTOMERS"}'

# Asset group with custom labels (filter products by custom_label_0 = "bestseller")
mcp tool google-ads.set_pmax_asset_groups \
  --campaign_id "$PMAX_CAMPAIGN_ID" \
  --asset_group '{
    "name":"AG-Bestsellers",
    "shopping_listing_group_filter":{
      "case_value":{"product_custom_attribute":{"value":"bestseller","index":"INDEX_0"}}
    },
    "headlines":["Best-sellers — back in stock","Free shipping over $50"],
    "descriptions":["Customer-loved products. Free returns."]
  }'
```

### Recipe 5: Feed validation — common errors

```python
import json
import requests

# Pull Meta catalog feed status
r = requests.get(
  f"https://graph.facebook.com/v19.0/{CATALOG_ID}/product_feeds",
  params={"access_token": META_ACCESS_TOKEN, "fields": "id,name,latest_upload"})
feeds = r.json()["data"]

# Pull feed errors
for f in feeds:
    errors = requests.get(
      f"https://graph.facebook.com/v19.0/{f['latest_upload']['id']}/errors",
      params={"access_token": META_ACCESS_TOKEN, "fields": "summary,severity,description,affected_surfaces"}
    ).json()["data"]
    for e in errors:
        print(f"{e['severity']}: {e['summary']} — {e['description']}")
```

### Recipe 6: Product set by performance — top-ROAS bestsellers

```python
# Query warehouse for SKUs with ROAS > 5
import sqlalchemy
engine = sqlalchemy.create_engine(os.environ["DATABASE_URL"])
top_skus = engine.execute("""
  SELECT sku FROM per_sku_roas
  WHERE roas > 5 AND last_30d_revenue > 1000
  ORDER BY revenue DESC LIMIT 50
""").fetchall()

# Create Meta product set with these
mcp_call("meta-ads.create_product_set", {
  "catalog_id": CATALOG_ID,
  "name": f"Bestsellers_AutoROAS5_{date.today()}",
  "filter": {"retailer_id": {"is_any": [s[0] for s in top_skus]}}
})
```

### Recipe 7: Google Merchant Center product feed via Shopify channel app

```yaml
# Shopify → Google channel app config (UI-driven, document for repro)
shopify_google_channel:
  merchant_center_id: $MERCHANT_ID
  target_countries: [US, CA, UK]
  sync_frequency: hourly
  product_filters:
    - status: active
    - inventory > 0
  custom_label_0_mapping: shopify_tag "bestseller" → "bestseller"
  custom_label_1_mapping: shopify_collection name
  custom_label_2_mapping: margin_pct bracket (high / med / low)
```

Then PMax `shopping_listing_group_filter` uses `custom_label_0=bestseller`.

### Recipe 8: Multi-market catalog

```bash
# Meta — separate catalog per market
mcp tool meta-ads.manage_catalog --action create --name "Brand-Catalog-EU" --vertical "commerce" --currency "EUR"
mcp tool meta-ads.manage_catalog --action create --name "Brand-Catalog-UK" --vertical "commerce" --currency "GBP"

# Google Merchant Center — multi-country target
# Add additional country to feed via "Target country" config in MC UI OR API:
curl -X POST "https://shoppingcontent.googleapis.com/content/v2.1/$MERCHANT_ID/datafeeds" \
  -d '{
    "name": "feed_uk",
    "contentType": "products",
    "fileName": "feed_uk.xml",
    "targets": [{"country": "GB", "language": "en", "feedLabel": "UK"}],
    "fetchSchedule": {"hour": 2, "minuteOfHour": 0, "timeZone": "Europe/London", "weekday": "monday"}
  }'
```

## Examples — Shopify-native DTC

```yaml
stack:
  ecommerce: Shopify
  meta_channel: Shopify Facebook + Instagram channel app (auto-sync)
  google_channel: Shopify Google channel app (auto-sync to Merchant Center)
  catalog_meta_id: catalog-id-from-mcp-create
  merchant_center_id: numeric-from-google
  
feed_refresh:
  shopify_native_meta: real-time on inventory / price change
  shopify_native_google: hourly
  manual_feed_url: not used

product_sets_meta:
  AllProducts: filter "all"
  Bestsellers_TopROAS: filter custom_label_0=bestseller
  NewArrivals_30d: filter created_at within 30d
  HighMargin: filter custom_label_2=high
  
campaigns:
  meta_advantage_plus_shopping:
    catalog: AllProducts
    budget: $300/day
    bid: min_roas 2.5
  
  meta_dpa_retargeting:
    catalog: AllProducts
    audience: ViewContent_30d minus Purchase_7d
    budget: $100/day
    bid: lowest_cost
  
  google_pmax_retail:
    merchant_center: linked
    asset_groups: [bestsellers, new_arrivals, high_margin]
    budget: $400/day
    bid: tROAS 4.0
```

## Edge cases

### Feed error severity
- ERROR: product disapproved, won't serve
- WARNING: product serves but with reduced quality
- INFO: cosmetic

### Meta catalog approval lag
New catalog: 24-72h approval. Plan launch with buffer.

### Image quality
Meta requires 1200x1200 minimum; Google prefers 1500x1500. Lower → reduced impressions on premium placements.

### GTIN / MPN
Required by Google for branded products. Without it, Shopping ads may not serve. Use brand's GTIN database OR retailer-assigned MPN.

### Currency mismatch
Feed currency must match Merchant Center target country currency. UK feed in USD → disapproved.

### Out-of-stock handling
`availability: out of stock` pauses serving but keeps in catalog. `out of stock` for >30d: archive instead.

### Price format
Meta: `"99.99 USD"`. Google: nested `{"value":"99.99","currency":"USD"}`. Sync utility normalizes.

### Catalog rate limits
Meta: 200 product updates/hour at default tier. Bulk via single upload (manage_catalog) — counts as 1 call.

### Tax + shipping (Google specific)
Configure account-level tax + shipping rules in Merchant Center. Per-product overrides via feed `shipping` and `tax` fields.

### Variant handling
Each variant (size, color) = separate `id`. Parent / child relationship via `item_group_id`. Meta also recognizes `item_group_id` for variant carousel.

### Custom labels (Google)
5 custom_label slots (0-4). Use for ROAS tier / margin / seasonality / brand-tier — enables PMax `listing_group_filter` segmentation.

### Performance Max with feed-only
PMax retail does NOT require additional creative assets if catalog is rich (image_link, title). Asset group can be feed-only.

## Sources

- Meta Catalog overview: https://www.facebook.com/business/help/1670743469549027
- Meta Commerce Manager: https://www.facebook.com/business/help/1275400645914358
- Meta product feed format: https://developers.facebook.com/docs/marketing-api/catalog/reference
- Meta Advantage+ Shopping: https://www.facebook.com/business/help/2204418216254220
- Google Content API for Shopping: https://developers.google.com/shopping-content
- Google Merchant Center product specs: https://support.google.com/merchants/answer/7052112
- Google Performance Max retail: https://support.google.com/google-ads/answer/12022530
- Google taxonomy IDs: https://www.google.com/basepages/producttype/taxonomy.en-US.txt
- Shopify Google channel: https://help.shopify.com/en/manual/online-sales-channels/google
- Shopify Meta channel: https://help.shopify.com/en/manual/online-sales-channels/facebook
