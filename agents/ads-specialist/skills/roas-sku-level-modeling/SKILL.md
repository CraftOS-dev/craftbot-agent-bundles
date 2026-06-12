<!--
Source: https://www.triplewhale.com/blog/sku-level-attribution
Per-SKU ROAS via Triple Whale or PostgreSQL warehouse with Shopify line-item join.
-->
# ROAS Modeling at SKU Level — SKILL

Account-blended ROAS hides product economics. A 4.0x blended hides 12 SKUs at 6x and 8 SKUs at 0.5x. This skill ships the per-SKU ROAS pipeline — either **Triple Whale** (Shopify-native paid SaaS) or **self-built PostgreSQL warehouse** join — and the threshold rules for product mix decisions.

## When to use this skill

- **DTC e-com with 5+ SKUs** — blended ROAS hides the economics.
- **Product-mix decisions** — which SKUs to feature in campaigns, which to drop.
- **Catalog ad creative** — DPA / PMax retail asset performance per SKU.
- **Inventory + ads coordination** — don't scale spend on out-of-stock SKUs.
- **Margin-aware optimization** — high-revenue ≠ high-margin SKU.

**Do NOT use this skill when:**
- Pre-revenue / single SKU — blended ROAS is fine.
- Account spend <$5K/month — noise floor too high for per-SKU read.
- Subscription / SaaS (different math — use cohort LTV, not SKU).

## Setup

### Path A — Triple Whale (Shopify-native)

```bash
export TW_API_KEY="<api-key>"   # Settings → API → Generate
export TW_SHOP_ID="<shop-id>"
```

Triple Whale auto-joins Shopify orders + Meta / Google / TikTok / Klaviyo. Per-SKU view in "Lighthouse" tab. API: `https://api.triplewhale.com/api/v2/willy/query` (natural language) or REST endpoints.

### Path B — PostgreSQL warehouse self-build

Required data flows:
- Shopify orders + line items → warehouse via Stitch / Fivetran / native sync
- Meta / Google / TikTok / LinkedIn / Reddit spend → warehouse via Funnel.io / Improvado
- UTM-stamped destination URLs (use `bitly-utm-campaign-tracking` skill)

```bash
export DATABASE_URL="postgresql://..."   # warehouse connection
```

### Required schema

```sql
-- ads_warehouse.platform_daily_spend
CREATE TABLE platform_daily_spend (
  date DATE,
  platform TEXT,           -- 'meta','google','tiktok','linkedin','reddit'
  campaign_id TEXT,
  ad_set_id TEXT,
  ad_id TEXT,
  spend NUMERIC,
  impressions INT,
  clicks INT,
  conversions INT,
  PRIMARY KEY (date, platform, ad_id)
);

-- shopify.orders + shopify.line_items (Stitch / Fivetran schemas)
-- Already in standard Shopify replication: orders.id, orders.created_at, 
-- line_items.order_id, line_items.sku, line_items.price * line_items.quantity
```

## Common recipes

### Recipe 1: Per-SKU ROAS via warehouse SQL (last 30d, UTM-attributed)

```sql
WITH ads_spend AS (
  SELECT date, platform, campaign_id, ad_set_id, SUM(spend) AS spend
  FROM ads_warehouse.platform_daily_spend
  WHERE date BETWEEN CURRENT_DATE - 30 AND CURRENT_DATE - 1
  GROUP BY 1,2,3,4
),
shopify_attr AS (
  SELECT
    o.id AS order_id,
    o.created_at::date AS date,
    li.sku,
    li.price * li.quantity AS revenue,
    o.note_attributes ->> 'utm_source' AS utm_source,
    o.note_attributes ->> 'utm_medium' AS utm_medium,
    o.note_attributes ->> 'utm_campaign' AS utm_campaign,
    o.note_attributes ->> 'utm_content' AS utm_content
  FROM shopify.orders o
  JOIN shopify.line_items li ON li.order_id = o.id
  WHERE o.created_at >= CURRENT_DATE - 30
    AND o.financial_status = 'paid'
),
joined AS (
  SELECT
    s.sku, a.platform, a.campaign_id, a.ad_set_id,
    SUM(s.revenue) AS revenue,
    SUM(a.spend) AS spend
  FROM shopify_attr s
  JOIN ads_spend a 
    ON s.utm_content = a.ad_set_id
   AND s.date BETWEEN a.date - INTERVAL '7 days' AND a.date
  GROUP BY 1,2,3,4
)
SELECT
  sku, platform, ad_set_id,
  revenue, spend,
  ROUND(revenue / NULLIF(spend, 0), 2) AS roas,
  RANK() OVER (PARTITION BY platform ORDER BY revenue / NULLIF(spend,0) DESC NULLS LAST) AS roas_rank
FROM joined
ORDER BY revenue DESC;
```

### Recipe 2: Triple Whale — natural language query

```bash
curl -X POST "https://api.triplewhale.com/api/v2/willy/query" \
  -H "Authorization: Bearer $TW_API_KEY" \
  -d '{
    "shop_id": "'$TW_SHOP_ID'",
    "query": "Per-SKU ROAS last 30 days, ranked, with attribution from Meta",
    "format": "json"
  }'
```

Triple Whale returns ranked SKU table with platform breakdown.

### Recipe 3: Per-SKU margin-adjusted ROAS

```sql
WITH per_sku_roas AS (
  SELECT sku, revenue, spend FROM joined  -- from Recipe 1
),
costs AS (
  SELECT sku, gross_margin_pct
  FROM shopify_meta.product_costs   -- your product cost source
)
SELECT
  p.sku,
  p.revenue,
  ROUND(p.revenue * c.gross_margin_pct, 2) AS gross_profit,
  p.spend,
  ROUND(p.revenue / NULLIF(p.spend, 0), 2) AS roas,
  ROUND((p.revenue * c.gross_margin_pct) / NULLIF(p.spend, 0), 2) AS margin_roas
FROM per_sku_roas p
LEFT JOIN costs c ON p.sku = c.sku
ORDER BY margin_roas DESC NULLS LAST;
```

`margin_roas < 1.0` = paid is unprofitable for that SKU even at top-line break-even.

### Recipe 4: Threshold rule — kill underperforming SKU on ad set

```sql
-- SKUs with <80% of account-blended ROAS after 4 weeks of attribution
WITH account_blended AS (
  SELECT SUM(revenue) / NULLIF(SUM(spend), 0) AS blended_roas
  FROM joined
  WHERE created_at >= CURRENT_DATE - 28
),
per_sku AS (
  SELECT sku, platform, ad_set_id, SUM(revenue) AS rev, SUM(spend) AS spend,
         SUM(revenue) / NULLIF(SUM(spend), 0) AS sku_roas
  FROM joined
  WHERE created_at >= CURRENT_DATE - 28
  GROUP BY sku, platform, ad_set_id
)
SELECT s.*, b.blended_roas, ROUND(s.sku_roas / b.blended_roas * 100, 1) AS pct_of_blended
FROM per_sku s, account_blended b
WHERE s.sku_roas < b.blended_roas * 0.80
  AND s.spend > 200
ORDER BY pct_of_blended;
```

### Recipe 5: DPA / catalog SKU exposure via Meta

```bash
# Pull per-SKU ad performance in DPA campaign
mcp tool meta-ads.get_campaign_insights \
  --campaign_id "$DPA_CAMPAIGN" \
  --level "ad" \
  --breakdowns '["product_id"]' \
  --metrics '["impressions","clicks","spend","conversions","purchase_roas","action_values"]' \
  --date_preset "last_30d" > sku-perf.json

jq '.data | sort_by(.purchase_roas)' sku-perf.json
```

### Recipe 6: Per-SKU report to xlsx weekly

```python
import pandas as pd, sqlalchemy
engine = sqlalchemy.create_engine(os.environ["DATABASE_URL"])
df = pd.read_sql("""... Recipe 1 query ...""", engine)
df["margin_roas"] = df["revenue"] * df["margin_pct"] / df["spend"]

with pd.ExcelWriter("sku-roas-weekly.xlsx") as xl:
    df.to_excel(xl, sheet_name="per_sku_roas", index=False)
    df.groupby("sku").agg({"revenue":"sum","spend":"sum"}).sort_values("revenue", ascending=False).to_excel(xl, sheet_name="ranked")
```

### Recipe 7: Google Merchant Center per-product insights

```bash
# Google Ads PMax product-level performance
mcp tool google-ads.search --customer_id "$CUSTOMER_ID" --query "
  SELECT segments.product_item_id, segments.product_title,
         metrics.cost_micros, metrics.conversions_value, metrics.impressions
  FROM shopping_performance_view
  WHERE segments.date DURING LAST_30_DAYS
    AND campaign.advertising_channel_type = 'PERFORMANCE_MAX'
  ORDER BY metrics.conversions_value DESC"
```

## Examples — DTC skincare brand, 18 SKUs

```yaml
weekly_report:
  cohort: last 30d
  top_5_skus_by_roas:
    - vitamin_c_serum_30ml: 6.8x (37% margin)
    - retinol_25ml: 5.9x (42% margin)
    - eye_cream_15ml: 5.1x (38% margin)
    - cleansing_balm_100ml: 4.7x (45% margin)
    - mask_50ml: 4.2x (52% margin)
  
  bottom_3_skus:
    - face_mist_120ml: 0.8x (28% margin) — kill
    - gift_set_basic: 1.1x (15% margin) — kill 
    - travel_set: 1.9x (22% margin) — pause until refresh
  
  actions:
    - Move face_mist out of broad DPA; gift it as bundle add-on only
    - Pause travel_set; re-launch in Q4 with holiday-bundle creative
    - Concentrate prospecting budget on top-3 SKU lineup
    - Test retinol_25ml standalone campaign — highest margin × strong ROAS
```

## Edge cases

### UTM-content = ad_set_id convention
Requires UTM hygiene (`attribution-debugging-utm-hygiene` skill). If `utm_content` is blank or set to creative name, join fails. Enforce convention.

### Multi-SKU orders attribution split
An order with 3 SKUs from one ad click — how to split revenue? Default: line-item revenue (full price × qty). Alternative: distribute order total proportionally by SKU value.

### Time decay
A click on Day 1 → purchase Day 5. Attribution window. SQL uses `s.date BETWEEN a.date - INTERVAL '7 days' AND a.date` (7d-click). Adjust per platform.

### Subscription SKUs
For subscription products, ROAS = first-order revenue / spend underestimates. Use 90-day LTV in numerator instead.

### Bundle / variant aliasing
Shopify allows variant SKUs (size, color). Collapse via base SKU OR maintain variant-level. Decide upfront.

### Out-of-stock blocking
Don't scale spend on SKUs at risk of stockout. Add inventory-aware exclusion:
```sql
WHERE sku NOT IN (SELECT sku FROM shopify.inventory WHERE quantity < 50)
```

### Promo / discount distortion
Sale period inflates ROAS (revenue per click rises). Compare against same-promo prior period, not normal baseline.

### Catalog refresh lag
Meta catalog feed lag = 24h. Today's order line items may not yet appear in MCP attribution data.

### Last-click bias
Per-SKU ROAS via last-click UTM ignores upper-funnel exposure. Compare to MTA (Triple Whale / Northbeam) or MMM for upper-funnel SKUs.

### Currency normalization
Multi-currency: convert all to USD via FX table for cross-market reporting.

## Sources

- Triple Whale SKU attribution: https://www.triplewhale.com/blog/sku-level-attribution
- Triple Whale API: https://docs.triplewhale.com/
- Shopify GraphQL Admin API (orders + line items): https://shopify.dev/docs/api/admin-graphql
- Meta DPA product_id breakdown: https://developers.facebook.com/docs/marketing-api/insights/breakdowns
- Google Shopping performance view (GAQL): https://developers.google.com/google-ads/api/fields/v17/shopping_performance_view
- Funnel.io connectors: https://funnel.io/connectors
- Improvado: https://improvado.io/integrations
- Stitch Shopify integration: https://www.stitchdata.com/integrations/shopify/
- Fivetran Shopify connector: https://fivetran.com/docs/connectors/applications/shopify
