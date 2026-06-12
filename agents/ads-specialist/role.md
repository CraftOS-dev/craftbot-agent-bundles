# Performance Ads Specialist — deep reference

This appends to `AGENT.md`. **Not** in the agent's default context. Grep when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "Meta campaign structure playbook", "Google Ads PMax playbook", "TikTok Ads playbook", "LinkedIn Ads ABM playbook", "Reddit Ads playbook", "Audience pyramid playbook", "Creative testing matrix playbook", "Ad fatigue rotation playbook", "ROAS at SKU playbook", "Attribution debugging playbook", "Server-side tracking playbook", "Conversion APIs playbook", "MMM playbook", "Mobile attribution SKAN playbook", "Dynamic product feeds playbook", "Retargeting playbook", "Geo + dayparting playbook", "Account audit playbook", "Competitor ad spying playbook", "AI creative generation playbook", "Landing page CRO playbook", "Antipattern catalog", "Reference patterns", "SOTA tool reference", "SOTA execution playbook", "Brief templates", "Output templates".

For provenance, see `SOURCES.md`.

---

## Capability reference

### Ad platforms supported

- **Meta** (Facebook + Instagram + Messenger + Audience Network) — primary surface, official MCP, full automation
- **Google Ads** (Search + Display + YouTube + PMax + Shopping + App + Discovery + Demand Gen) — official MCP
- **TikTok Ads** (In-Feed + Spark Ads + TopView + Brand Takeover + Smart Performance Campaign) — community MCP + Marketing API
- **LinkedIn Ads** (Sponsored Content + Message Ads + Lead Gen Forms + Dynamic Ads + Conversation Ads) — Marketing API via `cli-anything`
- **Reddit Ads** (Promoted Posts + Conversation Ads + Display) — Ads API via `cli-anything`
- **Pinterest Ads** (Promoted Pins + Shopping Ads + Idea Pins) — Ads API via `cli-anything`
- **Microsoft Ads / Bing Ads** (Search + Audience Network) — Microsoft Advertising API via `cli-anything`
- **Snap Ads** (Snap Ads + Story Ads + Collection Ads + AR Lenses) — Marketing API via `cli-anything`
- **Amazon Ads** (Sponsored Products + Sponsored Brands + Sponsored Display + DSP) — Amazon Advertising API via `cli-anything`
- **X (Twitter) Ads** (Promoted Tweets + Takeover + Trend) — X Ads API via `cli-anything`
- **Spotify Ad Studio** — REST API via `cli-anything`
- **Quora Ads** — Quora Ads Manager API via `cli-anything`
- **AppLovin** (mobile UA) — AppDiscovery API via `cli-anything`

### Bid strategies supported

**Meta:** Lowest Cost (no cap), Lowest Cost with Bid Cap, Cost Cap, Bid Cap, Highest Value (auto-bid), Minimum ROAS (Advantage+ Shopping), Manual Bid (Reach campaigns).

**Google:** Maximize Conversions, Target CPA, Maximize Conversion Value, Target ROAS, Maximize Clicks, Manual CPC, Enhanced CPC, Target Impression Share, Target CPM (Display).

**TikTok:** Cost Cap, Minimum ROAS, Maximize Delivery, Lowest Cost, Highest Value.

**LinkedIn:** Maximum Delivery, Cost Cap, Manual Bidding (CPC / CPM / CPS).

**Reddit:** Auto-bid (Conversions / Clicks / Impressions), Manual CPC, Manual CPM.

### Conversion APIs / server-side endpoints

- **Meta Conversions API (CAPI)** — `POST https://graph.facebook.com/v19.0/{pixel_id}/events`
- **TikTok Events API** — `POST https://business-api.tiktok.com/open_api/v1.3/event/track/`
- **Google Enhanced Conversions for Web (gtag)** — `gtag('set', 'user_data', {...})` + Conversion Linker
- **Google Enhanced Conversions for Leads / Offline Conversion Import** — `POST https://www.googleadservices.com/pagead/conversion/upload` (GCLID-based) OR Click Conversion API
- **Reddit Conversion API (CAPI)** — `POST https://ads-api.reddit.com/api/v3/events`
- **LinkedIn Conversions API** — `POST https://api.linkedin.com/rest/conversionEvents`
- **Pinterest Conversions API** — `POST https://api.pinterest.com/v5/events`
- **Snap Conversions API** — `POST https://tr.snapchat.com/v2/conversion`
- **GA4 Measurement Protocol** — `POST https://www.google-analytics.com/mp/collect`

### Attribution windows (default 2026)

| Platform | Default click | Default view | Max click | Max view |
|---|---|---|---|---|
| Meta (post-ATT) | 1d | 1d | 7d | 1d |
| Google Ads (Search/Shopping) | 30d | n/a | 90d | n/a |
| Google Ads (YouTube/Display) | 30d | 1d | 90d | 30d |
| TikTok | 7d | 1d | 28d | 7d |
| LinkedIn | 30d | 7d | 90d | 30d |
| Reddit | 7d | 1d | 30d | 7d |
| Pinterest | 30d | 1d | 60d | 30d |

### Mobile MMP options

- **AppsFlyer** — market leader, $0 free tier up to ~50K installs; SKAN 4.0 + Privacy Sandbox supported
- **Adjust** — strong incrementality + fraud detection; deep linking via Universal Links
- **Branch** — strong deep linking + people-based attribution
- **Singular** — strong SKAN postback decoding + cost aggregation; Free tier up to 50K installs
- **Kochava** — gaming-focused; supports Roku / CTV
- **Tenjin** — gaming-focused; low-cost MMP

### MMM tooling

- **Google Meridian** (May 2026 SOTA) — Bayesian with GeoX geo-incrementality, reach/frequency response curves
- **Meta Robyn** (R) — Bayesian + hyperparameter tuning + budget allocator + Prophet seasonality
- **Recast.ai** — managed MMM-as-a-service (paid)
- **lightweight_mmm** (Python) — Google-built Bayesian, slower than Meridian, simpler API
- **PyMC-Marketing** (Python) — Bayesian MMM + customer lifetime value modeling

### Multi-touch attribution SaaS

- **Triple Whale** — Shopify-native, blended-ROAS, SKU-level
- **Northbeam** — DTC multi-touch + channel incrementality
- **Wicked Reports** — long-cycle B2C + B2B path analysis
- **Hyros** — info-product DTC heavy
- **Rockerbox** — enterprise MTA
- **Polar Analytics** — managed-data DTC

### Cross-platform reporting + warehouse pipes

- **Funnel.io** — 500+ connectors, daily warehouse export
- **Improvado** — 300+ connectors, enterprise
- **Supermetrics** — Google Sheets connector default, low-cost
- **Whatagraph** — agency reporting templates
- **Glew** — Shopify analytics
- **Bullets** — DTC daily-digest reporting

### Creative tooling

- **Smartly.io** — cross-platform programmatic creative + auto-optimization (enterprise)
- **AdCreative.ai** — AI banner / carousel generator ($29/mo)
- **Bannerbear** — templated programmatic static ($49/mo)
- **Creatify** — AI video ads
- **Vidico** — video creative production service
- **MotionDen** — AI video gen with avatars
- **Magic Hour** — AI video gen with character animation

### Server-side tagging tools

- **Google Tag Manager Server-side** — self-host (Cloud Run / Fly.io / GCP App Engine)
- **Stape.io** — managed GTM-S hosting ($20/mo entry tier)
- **Snowplow** — enterprise event pipeline (self-host or managed)

### Competitor intel tools

- **Meta Ad Library API** — free, public, commercial-open
- **Google Ads Transparency Center** — public web (scrape via `firecrawl-mcp`)
- **Pathmatics** — enterprise paid
- **WhatRunsWhere** — display ad intel
- **SpyFu** — Google Ads intel
- **SimilarWeb** — traffic + paid-channel mix intel

---

## Meta campaign structure playbook

1. **Set objective** at campaign level. Defaults: Sales (DTC e-com), Leads (B2B), App Install (mobile), Engagement (only for brand awareness / nurture).
2. **CBO vs ABO decision.**
   - CBO (Advantage Campaign Budget) = default for spend ≥$500/day, 2-5 adsets. Meta optimizes across.
   - ABO (manual adset budgets) = use when you need clean reads per audience for testing, OR when one audience is so different (e.g., LAL-1% vs broad-Advantage+) that CBO will under-spend the smaller pool.
3. **Audience pyramid per campaign** (one campaign per pyramid layer where possible):
   - **Cold:** 1% Lookalike, 2-5% Lookalike, Interest Stack (broad), Advantage+ Audience (let Meta decide)
   - **Warm:** 25%-50%-75% video viewers, page engagers 365d, IG profile visitors, lead-form openers
   - **Hot:** Add-to-cart 7d / 14d / 30d, Initiated-Checkout 7d / 14d, customer list (excluded if recently purchased)
4. **Bid strategy by layer.** Cold = Lowest Cost without cap (volume). Warm = Cost Cap at target CPA. Hot = Cost Cap or ROAS goal (Advantage+ Shopping).
5. **Placement.** Default Advantage+ Placements. Force-feed exclusions only when budget or asset constraint demands (e.g., no Reels asset → exclude Reels).
6. **Frequency cap** at ad-set level for prospecting (cold) campaigns: 2/7d default. Hot retargeting: no cap (let Meta optimize).
7. **Creative variants per ad set:** 3-5 ad creatives per adset minimum for Meta's optimization phase to read.

### Meta campaign structure template

```markdown
## Meta Campaign Structure — [Brand] [Month/Year]

### Account-level
- Pixel ID: <id>
- CAPI status: <good / needs work>
- AEM priority (8 events): <list ranked>
- Default attribution: 1d-click (post-ATT 2026)

### Campaign 1: Cold prospecting (CBO)
- Objective: Sales (or Leads)
- Budget: $X/day
- Bid: Lowest Cost no cap (or Cost Cap at $Y)
- Ad sets:
  - LAL-1% (purchasers 180d): $-
  - LAL-2% (cart-adders 180d): $-
  - Interest Stack (top 5 interests OR'd): $-
  - Advantage+ Audience (broad): $-
- Creative per adset: 3-5 variants
- Frequency cap: 2/7d
- Exclusions: Past purchasers 90d, current customer list

### Campaign 2: Warm retargeting (CBO or ABO)
- Objective: Sales
- Budget: $X/day
- Bid: Cost Cap at target CPA
- Ad sets:
  - Video viewers 50-75% (30d)
  - Page engagers 30d
  - Add-to-cart 7d (excluded purchase 7d)
- Creative: testimonial / social proof / discount offer
- Frequency cap: none

### Campaign 3: Hot retargeting (ABO)
- Objective: Sales
- Budget: $X/day
- Bid: Minimum ROAS (Advantage+ Shopping) OR Cost Cap
- Ad sets:
  - Initiated-Checkout 7d (excl purchase 7d)
  - Add-to-cart 14d (excl purchase 14d)
  - Customer list "abandoned cart > $X" (excl recent purchase)
- Creative: cart reminder / urgency / discount / free shipping
```

---

## Google Ads PMax playbook

1. **PMax for retail / lead-gen / app** — uses all Google inventory (Search / Display / YouTube / Discover / Gmail / Maps) with Google's optimization. tROAS or Maximize Conversion Value (with tROAS).
2. **Standard Search** for brand + high-intent non-brand keywords where you want explicit query control. Match type: Phrase + Exact. No Broad without a strong negative list.
3. **Asset groups** (PMax) — theme per audience signal. Each group needs: 5+ headlines, 5+ descriptions, 1+ long headline, 5+ images (min 1200x628), 1+ logo, 1+ video. Audience signal = your hypothesis about who the group serves.
4. **Audience signals** in PMax — Customer Match (CRM), Website Visitors, Custom Audience (in-market keywords). Signals are hints, not hard targeting — Google may serve outside.
5. **Conversion goals** — set at customer level. PMax optimizes to ALL conversion goals unless you specify per-campaign goal override.
6. **Negative keywords** at account level (centralized list) — PMax respects account-level negatives.
7. **Brand exclusion** in PMax — exclude your own brand terms so PMax doesn't cannibalize Search Brand.
8. **Recommendations API** — `get_recommendations` weekly, apply low-risk ones (negative keyword, bid adjustment, asset rotation), review high-risk ones (campaign restructure, budget shift).

### Google Ads campaign structure template

```markdown
## Google Ads Account Structure — [Brand] [Month/Year]

### Account-level
- Conversion goals: <list with primary + secondary>
- Enhanced Conversions for Web: enabled
- GTM-S container: <url> + CAPI forwarding to Meta / Google EC
- Default attribution: data-driven (DDA)
- Account negative list: <list 50+ negatives>

### Campaign 1: Search — Brand
- Match types: Phrase + Exact (no Broad)
- Budget: $X/day (low — brand searches are cheap)
- Bid: Manual CPC or Target Impression Share (top of page)
- Ad groups: <brand variants + brand + product>

### Campaign 2: Search — Non-brand (high-intent)
- Match types: Phrase + Exact
- Budget: $X/day
- Bid: Target CPA at $Y OR Maximize Conversions w/ portfolio bid strategy
- Ad groups: <by theme — buyer-intent keyword groups>

### Campaign 3: Performance Max — Retail
- Objective: Sales / Lead-gen / App install
- Budget: $X/day
- Bid: Maximize Conversion Value, tROAS at Z%
- Asset groups:
  - Group A: hypothesis = "shopping-intent women 25-45"
    - Audience signal: Customer Match (purchasers 365d) + Custom Audience (in-market keywords)
    - Assets: 5+ headlines, 5+ descriptions, 1 long, 5+ images, 1 logo, 1 video
  - Group B: hypothesis = "..."
- Brand exclusion: ON (your brand terms)

### Campaign 4: YouTube — Awareness or View
- Format: In-Stream (skippable) + In-Feed
- Budget: $X/day
- Bid: Target CPM or Maximum CPV
- Audiences: custom audience based on YouTube channels + keywords
```

---

## TikTok Ads playbook

1. **Smart Performance Campaign** = TikTok's PMax equivalent. Budget level: campaign. Creative: video ads. Bid: Lowest Cost / Cost Cap.
2. **Spark Ads** = whitelisted creator post boosted as ad. Higher CTR + lower CPM than in-house creative because it looks native. Get auth_code from creator via TikTok Creator Marketplace or manual whitelist.
3. **In-Feed Ads** (standard) — 9-15s vertical video, 9:16 ratio, sound-on assumption.
4. **TopView / Brand Takeover** = brand awareness premium spots; rarely cost-effective for performance.
5. **Audience targeting:** interests + behaviors + Custom Audiences (hashed email upload via Audience Manager) + Lookalikes (1-10%).
6. **Optimization event** — choose carefully. Conversions = revenue (best for DTC); Add-to-Cart = mid-funnel (for accounts with weak conversion volume).
7. **Pixel + Events API** = required. Server-side via TikTok Events API for ATT-recovery on iOS.
8. **Creative cadence:** TikTok burns creative faster than Meta. Refresh top creative weekly, not monthly.

### TikTok Spark Ads recipe

```bash
# 1. Get auth_code from creator (via TTAM Creator Marketplace OR manual)
# 2. Use TikTok Marketing API to create Spark Ad
curl -X POST https://business-api.tiktok.com/open_api/v1.3/ad/create/ \
  -H "Access-Token: $TT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "advertiser_id": "$ADVERTISER_ID",
    "adgroup_id": "$ADGROUP_ID",
    "creatives": [{
      "ad_name": "Spark_Creator123_HookA",
      "ad_format": "SINGLE_VIDEO",
      "identity_type": "AUTH_CODE",
      "identity_authorized_bc_id": "$AUTH_CODE",
      "tiktok_item_id": "$TIKTOK_POST_ID",
      "call_to_action": "SHOP_NOW",
      "landing_page_url": "https://brand.com/lp?utm_source=tiktok&utm_medium=paid&utm_campaign=spark-jan26&utm_content=creator123-hookA"
    }]
  }'
```

---

## LinkedIn Ads ABM playbook

1. **Matched Audiences from CRM list** — upload hashed-email or company-domain list via `/rest/dmpSegments`. Min audience size: 300 members for delivery.
2. **Sponsored Content** — single image, video, carousel, document — defaults for ABM nurture.
3. **Message Ads** (formerly Sponsored InMail) — 1-to-1 inbox delivery; high engagement but expensive ($0.50-$2.00 per send).
4. **Lead Gen Forms** — pre-filled by LinkedIn profile data; 5-15% conversion typical. Default for B2B form fills.
5. **Conversation Ads** — interactive Q&A flow in DMs. Higher engagement than Message Ads for mid-funnel.
6. **Audience size for delivery** — 50K+ for cold prospecting; 1K+ for hot retargeting.
7. **Bid strategy** — Maximum Delivery (auto) for awareness; Cost Cap for performance; Manual CPC for testing.

### LinkedIn ABM curl recipe

```bash
# 1. Upload ABM target list (hashed-email)
curl -X POST "https://api.linkedin.com/rest/dmpSegments" \
  -H "Authorization: Bearer $LI_ACCESS_TOKEN" \
  -H "LinkedIn-Version: 202406" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -H "Content-Type: application/json" \
  -d '{
    "account": "urn:li:sponsoredAccount:$ACCOUNT_ID",
    "destinations": [{"destination": "LINKEDIN"}],
    "name": "ABM_Tier1_FY26",
    "sourcePlatform": "API",
    "sourceSegmentId": "abm_tier1_fy26",
    "type": "USER"
  }'

# 2. Add hashed members
curl -X POST "https://api.linkedin.com/rest/dmpSegments/{segmentId}/users" \
  -H "Authorization: Bearer $LI_ACCESS_TOKEN" \
  -H "LinkedIn-Version: 202406" \
  -d '{
    "elements": [
      {"action": "ADD", "userIds": [{"idType": "SHA256_EMAIL", "idValue": "$HASHED_EMAIL_1"}]}
    ]
  }'

# 3. Create Sponsored Content campaign
curl -X POST "https://api.linkedin.com/rest/adCampaigns" \
  -H "Authorization: Bearer $LI_ACCESS_TOKEN" \
  -d '{
    "account": "urn:li:sponsoredAccount:$ACCOUNT_ID",
    "campaignGroup": "urn:li:sponsoredCampaignGroup:$GROUP_ID",
    "name": "ABM_Tier1_Awareness_Q1",
    "type": "SPONSORED_UPDATES",
    "costType": "CPM",
    "dailyBudget": {"amount": "100", "currencyCode": "USD"},
    "targeting": {"matchedAudience": "urn:li:dmpSegment:$SEGMENT_ID"}
  }'
```

---

## Reddit Ads playbook

1. **Subreddit targeting** is Reddit's signature lever. Find 5-15 subreddits where your ICP lives via `reddit-mcp` (organic context) + Reddit search.
2. **Interest targeting** as secondary layer (broader audiences).
3. **Conversation Ads** — appear in comment threads; native feel, higher CTR.
4. **Promoted Posts** — appear in feed; default format.
5. **Reddit Conversion API (CAPI)** — required for iOS signal recovery. Server-side event via `POST https://ads-api.reddit.com/api/v3/events`.
6. **Bid strategy** — Auto-bid (conversions) for performance; Manual CPC for testing.

---

## Audience pyramid playbook

| Layer | Definition | Default % budget | Bid strategy | Creative |
|---|---|---|---|---|
| Cold — LAL 1% | Lookalike of purchasers 180d | 30-40% | Lowest Cost | Hook + problem framing |
| Cold — LAL 2-5% | Broader lookalike | 10-15% | Lowest Cost | Hook + variant |
| Cold — Interest Stack | Top 5 interests OR'd | 10-15% | Lowest Cost or Cost Cap | Hook + variant |
| Cold — Broad / Advantage+ | Let Meta decide | 10-20% | Lowest Cost | Best-performing creative |
| Warm — Engagers / Viewers | Page eng 30d / Video 50%+ / IG profile | 10-15% | Cost Cap | Testimonial + social proof |
| Hot — Cart Abandoners | ATC 7d, IC 7d minus PUR 7d | 10-15% | Min ROAS / Cost Cap | Cart reminder + urgency |
| Hot — Customer Match | Past customers (cross-sell) OR high-LTV LAL | 5-10% | Min ROAS | Cross-sell / loyalty |

### Pyramid exclusion rules

- **Cold campaign excludes:** all past purchasers 90d, all hot+warm audiences (avoid double-burn)
- **Warm campaign excludes:** past purchasers 30d
- **Hot campaign excludes:** past purchasers 7-14d (depending on AOV / repeat cycle)
- **Customer Match lookalike:** seed = top 25% LTV customers (not all customers)

---

## Creative testing matrix playbook

1. **Matrix size.** Cells = creative concepts × audiences × offers. Typical: 5 creatives × 3 audiences × 2 offers = 30 cells.
2. **Cell budget.** Minimum $25-50/day per cell at target CPA ≤$50 — gives ~100 conversions per cell in 7-14d.
3. **Power calc.** For CTR delta 0.5%-1.0% significance, need ~10K impressions per cell at p=0.05.
4. **Significance test.**
   - CTR: z-test on impressions × clicks per cell, p<0.05 to declare
   - CPA: t-test on per-cell CPA distribution OR direct comparison with confidence interval
   - CVR: z-test on clicks × conversions per cell
5. **Mode A — Advantage+ Dynamic Creative (Meta).** All variants in one ad creative; Meta serves combinations. Fast, noisy reads. Use for early concept hunt.
6. **Mode B — ABO split.** One ad set per cell. Clean reads but slow. Use for winner confirmation.

### Creative testing matrix template

```markdown
| Cell # | Hook concept | Audience | Offer | Budget/day | Impressions target | Z-test pass? | Winner? |
|---|---|---|---|---|---|---|---|
| C1 | Problem-aware question | LAL-1% | 20% off | $50 | 10000 | TBD | TBD |
| C2 | Problem-aware question | LAL-1% | Free ship | $50 | 10000 | TBD | TBD |
| C3 | Founder UGC | LAL-1% | 20% off | $50 | 10000 | TBD | TBD |
| C4 | Founder UGC | LAL-1% | Free ship | $50 | 10000 | TBD | TBD |
| C5 | Testimonial montage | Interest Stack | 20% off | $50 | 10000 | TBD | TBD |
...
```

### Creative significance Z-test (CTR)

```
z = (p1 - p2) / sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
p_pool = (clicks_1 + clicks_2) / (impressions_1 + impressions_2)
Reject H0 (no difference) if |z| > 1.96 (p < 0.05) or |z| > 2.576 (p < 0.01)
```

---

## Ad fatigue rotation playbook

| Signal | Threshold | Action |
|---|---|---|
| Frequency (7d window) | > 2.5 | Rotate creative within 48h |
| CPM week-over-week | +30% rise | Investigate audience exhaustion; consider expansion + rotation |
| CTR week-over-week | -25% drop | Rotate creative within 48h |
| Hook retention (3s view rate, video) | -20% drop | Test new hook variant |
| CPA week-over-week | +20% rise | Combined diagnosis — could be creative OR audience OR offer |

### Madgicx / Revealbot rule recipe (Meta)

```
IF (Frequency > 2.5 AND CPM_delta_7d > +30%)
   OR (CTR_delta_7d < -25%)
THEN
   PAUSE all ads in adset
   NOTIFY Slack channel #ads-alerts with adset_id + diagnosis
   QUEUE creative refresh task in Asana/Linear
```

---

## ROAS at SKU playbook

1. **Data sources.** Shopify (orders + line items + customer) → warehouse via Shopify Webhook + Stitch / Fivetran. Meta / Google / TikTok / etc spend → warehouse via Funnel.io / Improvado.
2. **Attribution join.**
   - Last-click: latest UTM-stamped session → order. Easy, biased toward bottom-funnel.
   - Data-driven (GA4): use GA4 DDA on `purchase` event with `items[]` array.
   - Multi-touch (Triple Whale / Northbeam): paid SaaS handles the join.
3. **Per-SKU formula:** `roas_sku = sum(line_item_revenue WHERE sku = X AND attributed_to = ad_set_Y) / sum(spend WHERE ad_set = Y)`
4. **Output:** Per-SKU ROAS per ad set, weekly. Threshold for action: if a SKU has < 80% of account-blended-ROAS on a given ad set after 4 weeks → either kill the ad set or swap creative.

### ROAS @ SKU SQL recipe (PostgreSQL warehouse)

```sql
WITH ads_spend AS (
  SELECT date, platform, campaign_id, ad_set_id, spend
  FROM ads_warehouse.platform_daily_spend
  WHERE date BETWEEN '2026-05-01' AND '2026-05-31'
),
shopify_attr AS (
  SELECT
    o.order_id,
    li.sku,
    li.revenue,
    o.utm_source,
    o.utm_medium,
    o.utm_campaign,
    o.utm_content,
    o.utm_term
  FROM shopify.orders o
  JOIN shopify.line_items li ON li.order_id = o.order_id
  WHERE o.created_at BETWEEN '2026-05-01' AND '2026-05-31'
),
joined AS (
  SELECT
    s.sku,
    a.platform,
    a.campaign_id,
    a.ad_set_id,
    SUM(s.revenue) AS revenue,
    SUM(a.spend) AS spend
  FROM shopify_attr s
  JOIN ads_spend a ON s.utm_content = a.ad_set_id::text
  GROUP BY 1, 2, 3, 4
)
SELECT
  sku,
  platform,
  ad_set_id,
  revenue,
  spend,
  ROUND(revenue / NULLIF(spend, 0), 2) AS roas
FROM joined
ORDER BY revenue DESC;
```

---

## Attribution debugging playbook

1. **UTM trace.** Pull all active ad destination URLs via Meta/Google/TikTok MCPs. Diff against Bitly registry. Diff against Funnel.io / Improvado normalized log. Flag missing params + casing inconsistencies + duplicate campaigns.
2. **Pixel / CAPI dedup check.** Meta Events Manager → "Test events" view. Send a test event with `event_id="dedup-test-123"`. Verify only 1 event registered (not 2). Repeat for TikTok / Google EC.
3. **View-through vs click-through windows.** Confirm platform default vs reported window in dashboards. Meta default is 1d-click post-ATT — anyone reporting 7d-click numbers needs to flag the window.
4. **Cross-platform reconciliation.** Last-click GA4 vs last-click platform-reported vs MTA (Triple Whale / Northbeam) vs MMM. Document the gap; pick one model for the quarter.

### Attribution debugging memo template

```markdown
# Attribution Debugging Memo — [Brand] [Month/Year]

## Current stack
- Pixel: Meta + TikTok + Google EC
- CAPI: Meta CAPI Gateway (Stape), TikTok Events API, Google EC Web
- GTM client: <id> (gtag.js)
- GTM server: sgtm.brand.com on Stape
- GA4: <property_id>, attribution = data-driven
- MTA: Triple Whale (Shopify-native)
- MMP (mobile): AppsFlyer

## Findings

### P0 (revenue-impact this week)
- [issue with $/week estimate]

### P1 (revenue-impact this month)
- [issue with $/month estimate]

### P2 (data hygiene)
- [naming / convention issues]

## Remediation checklist
- [ ] Fix CAPI dedup on Meta ($X/wk impact)
- [ ] Add UTM params to 14 ads missing utm_content
- [ ] Normalize UTM casing to kebab-case (currently mixed)
- [ ] Update GTM-S container to forward TikTok Events API

## Recommended attribution model for Q1
- Primary: Data-driven (GA4)
- Shadow: Triple Whale MTA (cross-check, not anchor)
- Revisit at QBR
```

---

## Server-side tracking playbook (GTM-S / Stape)

1. **Decision: Stape (managed) vs self-host (Cloud Run / Fly.io).** Stape from $20/mo, no DevOps. Self-host = free + max control. Default to Stape for SMB; self-host for enterprise.
2. **Custom domain mandatory.** `sgtm.brand.com` via CNAME to Stape OR your Cloud Run. Without custom domain, first-party cookies fail Safari ITP.
3. **Container architecture.**
   - **Web Container (client):** gtag.js or GTM client → events to `sgtm.brand.com/g/collect`
   - **Server Container:** receives → distributes to Meta CAPI / TikTok Events / Google EC / GA4 / custom
4. **Event ID for dedup.** Every event MUST carry `event_id = {user_id}-{event_name}-{timestamp_ms}`. CAPI dedup uses this to merge with pixel-side event. Without it, double-counting.
5. **First-party cookie strategy.** Stape's "GA4 Cookie Stitch" tag (or self-host equivalent) sets `_ga` server-side → resists ITP/ETP.
6. **QA before go-live.** Send 10 test events from staging URL → verify Meta Events Manager test-events view + Google Ads conversion log + GA4 DebugView all show within 60s + show `event_id` (no dedup conflict).

### GTM-S container deployment recipe (Stape API)

```bash
# 1. Create container via Stape API
curl -X POST "https://api.stape.io/v1/containers" \
  -H "Authorization: Bearer $STAPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "brand-prod-sgtm",
    "url": "sgtm.brand.com",
    "gtm_config_id": "GTM-XXXXXXX"
  }'

# 2. Configure CAPI gateway tag in GTM web UI:
#    - Tag: "Facebook Conversions API Tag" (Stape template)
#    - Pixel ID: 1234567890
#    - Access Token: $META_CAPI_TOKEN
#    - Event Name: dynamic from incoming event
#    - Event ID: dynamic from {{event.event_id}}
#    - User Data: hashed email/phone from {{user.email_hash}}

# 3. Test with staging URL
curl -X POST "https://sgtm.brand.com/g/collect" \
  -H "Content-Type: application/json" \
  -d '{
    "event_name": "purchase",
    "event_id": "test-user-purchase-1717000000000",
    "user_data": {"em": "<sha256-hash>"},
    "custom_data": {"currency": "USD", "value": 99.99}
  }'

# 4. Verify in Meta Events Manager → Test Events → seeing event_id
```

---

## Conversion APIs playbook

### Meta CAPI

```bash
curl -X POST "https://graph.facebook.com/v19.0/$PIXEL_ID/events" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [{
      "event_name": "Purchase",
      "event_time": '$(date +%s)',
      "event_id": "user123-purchase-1717000000000",
      "event_source_url": "https://brand.com/checkout/complete",
      "action_source": "website",
      "user_data": {
        "em": "'$EMAIL_SHA256'",
        "ph": "'$PHONE_SHA256'",
        "client_ip_address": "'$CLIENT_IP'",
        "client_user_agent": "'$USER_AGENT'",
        "fbc": "'$FBC_COOKIE'",
        "fbp": "'$FBP_COOKIE'"
      },
      "custom_data": {
        "currency": "USD",
        "value": 99.99,
        "content_ids": ["sku-abc"],
        "content_type": "product"
      }
    }],
    "access_token": "'$META_CAPI_TOKEN'"
  }'
```

### TikTok Events API

```bash
curl -X POST "https://business-api.tiktok.com/open_api/v1.3/event/track/" \
  -H "Access-Token: $TT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pixel_code": "$TT_PIXEL_CODE",
    "event": "CompletePayment",
    "event_id": "user123-purchase-1717000000000",
    "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",
    "context": {
      "ad": {"callback": "'$TTCLID'"},
      "page": {"url": "https://brand.com/checkout/complete"},
      "user": {"email": "'$EMAIL_SHA256'", "phone_number": "'$PHONE_SHA256'"}
    },
    "properties": {
      "currency": "USD",
      "value": 99.99,
      "content_id": "sku-abc"
    }
  }'
```

### Google Enhanced Conversions for Web (gtag client-side)

```javascript
gtag('event', 'conversion', {
  'send_to': 'AW-CONVERSION_ID/CONVERSION_LABEL',
  'value': 99.99,
  'currency': 'USD',
  'transaction_id': 'order-12345'
});

gtag('set', 'user_data', {
  'sha256_email_address': '<sha256-hash>',
  'sha256_phone_number': '<sha256-hash>'
});
```

### Google Click Conversion Import (offline / API-based)

```bash
# Upload click conversions via Google Ads API
# Endpoint: customers/{customer_id}/conversionUploads:uploadClickConversions
# Payload includes gclid OR gbraid OR wbraid + conversion_action + conversion_date_time + conversion_value
```

### Reddit Conversion API

```bash
curl -X POST "https://ads-api.reddit.com/api/v3/events" \
  -H "Authorization: Bearer $REDDIT_ACCESS_TOKEN" \
  -d '{
    "events": [{
      "event_at": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",
      "event_type": "Purchase",
      "event_metadata": {
        "value_decimal": 99.99,
        "currency": "USD",
        "item_count": 1,
        "products": [{"id": "sku-abc"}]
      },
      "user": {
        "email": "$EMAIL_SHA256",
        "rdt_cid": "$RDT_CID_COOKIE"
      },
      "click_id": "$RDT_CID"
    }]
  }'
```

---

## MMM playbook

1. **Spend threshold:** Below $50K/month total paid, MMM is noise. Use platform-attribution + UTM + last-click warehouse view instead.
2. **Data input.** ≥1 year weekly spend × channel × KPI. Add control vars: seasonality (week-of-year), promo flags, holidays (per-region calendar), macro (Google Trends index), competitor share-of-voice (Pathmatics / SimilarWeb).
3. **Tool choice.**
   - **Google Meridian + GeoX** — SOTA 2026. Bayesian + geo-incrementality + reach/frequency curves.
   - **Meta Robyn** — R-based, mature, includes budget allocator.
   - **PyMC-Marketing** — Python, Bayesian, customer-LTV integration.
   - **Recast.ai** — managed; paid; faster to results for non-Python teams.
   - **lightweight_mmm** — Google's older Python lib; slower than Meridian, simpler API.
4. **Output.** Response curves per channel (spend vs incremental revenue) + budget allocation recommendation + ROI ranking + confidence intervals.

### Meridian quickstart (Python)

```bash
# Install
uvx pip install google-meridian

# Prepare CSV: date | channel | spend | revenue | seasonality | promo | holiday
# Run model (Python script)
python -c "
from meridian.model import Meridian
import pandas as pd

df = pd.read_csv('mmm_input.csv')
m = Meridian(data=df, geo_col='geo', kpi_col='revenue', spend_cols=['meta','google','tiktok','linkedin','reddit'])
m.sample()
budget_alloc = m.optimize_budget(total_budget=500_000)
m.save_report('mmm_report.html')
"
```

### Robyn quickstart (R via cli-anything)

```bash
# Install R + Robyn via uvx OR system R
R -e "install.packages('Robyn')"
R -e "library(Robyn); robyn_inputs(...); robyn_run(...); robyn_allocator(...)"
```

---

## Mobile attribution SKAN playbook

1. **SKAN 4.0 anatomy.** 3 postback windows (0-2d, 3-7d, 8-35d). Each postback returns: 4 coarse-grained conversion values (low/medium/high/very-high) OR 6 fine-grained values (depending on crowd anonymity threshold).
2. **Conversion value schema.** Design once per app, revisit quarterly. Map to revenue ladder + retention bracket.
   - Window 1 (0-2d): coarse — install / install + tutorial-complete / install + first purchase / install + purchase value bracket
   - Window 2 (3-7d): fine — purchase value bracket × retention day-3 OR day-7
   - Window 3 (8-35d): fine — LTV-day-30 bracket
3. **MMP layer.** AppsFlyer / Adjust / Branch / Singular decodes raw postbacks + provides cross-platform deterministic attribution (where IDFA opted in).
4. **Privacy Sandbox (Android).** Attribution Reporting API (ARA) for web→app and app→web; FLEDGE for retargeting (audiences); Topics API for interests.

### SKAN 4.0 conversion value schema template

```markdown
| Postback | Window | Type | Value | Definition |
|---|---|---|---|---|
| 1 | 0-2d | Coarse | low | Install only |
| 1 | 0-2d | Coarse | medium | Install + tutorial complete |
| 1 | 0-2d | Coarse | high | Install + add to cart |
| 1 | 0-2d | Coarse | very-high | Install + purchase |
| 2 | 3-7d | Fine | 0 | No additional events |
| 2 | 3-7d | Fine | 1 | Retained day-3 |
| 2 | 3-7d | Fine | 2-5 | Purchase value bracket × retention |
| 3 | 8-35d | Fine | 0-63 | LTV-day-30 bracket (6-bit encoding) |
```

---

## Dynamic product feeds playbook

1. **Source feed.** Shopify / WooCommerce / Magento → JSON or CSV. Required fields: id, title, description, link, image_link, availability, price, brand, condition, gtin/mpn (recommended).
2. **Meta Commerce Catalog.** Upload via API OR Pixel-source-of-truth OR feed file. Use `manage_catalog` from Meta Ads MCP.
3. **Google Merchant Center.** Upload via Content API for Shopping OR scheduled feed file fetch. Required: product approval + tax + shipping.
4. **Dynamic Product Ads (DPA) — Meta.** Connect catalog to ad set; use creative template that auto-populates product fields. Audience = website visitors who viewed/added-to-cart.
5. **PMax Retail (Google).** Use Merchant Center as primary asset source; PMax serves Shopping ads, Display retargeting, YouTube product mentions.

### Meta Catalog feed upload (via MCP)

```python
# Pseudocode via facebook-ads-mcp
result = mcp_call("facebook-ads-mcp", "manage_catalog", {
    "catalog_id": "$CATALOG_ID",
    "operation": "upload_feed",
    "feed_url": "https://brand.com/feed.json",
    "schedule": "daily_2am_utc"
})
```

---

## Retargeting playbook

| Source list | Definition | Platform format | Refresh cadence |
|---|---|---|---|
| Customer list | Past customers (purchased ≥1) | Hashed SHA-256 email/phone CSV | Weekly minimum |
| High-LTV LAL seed | Top 25% LTV customers | Hashed CSV → LAL on platform | Monthly |
| Cart abandoners | ATC 7d minus PUR 7d | Custom audience on platform | Auto-updating |
| Site visitors | All pageviews 30d | Custom audience on platform | Auto-updating |
| Engaged on platform | Page eng / video viewer / IG profile visitor | Custom audience on platform | Auto-updating |

### Customer Match upload (Google Ads)

```bash
curl -X POST "https://googleads.googleapis.com/v15/customers/$CUSTOMER_ID/offlineUserDataJobs:create" \
  -H "Authorization: Bearer $GADS_OAUTH_TOKEN" \
  -H "developer-token: $GADS_DEV_TOKEN" \
  -d '{
    "job": {
      "type": "CUSTOMER_MATCH_USER_LIST",
      "customerMatchUserListMetadata": {
        "userList": "customers/'$CUSTOMER_ID'/userLists/'$USER_LIST_ID'"
      }
    }
  }'

# Then add operations: hashed_email, hashed_phone_number, address_info
```

### Meta Custom Audience from Customer List (via MCP)

```python
result = mcp_call("facebook-ads-mcp", "create_custom_audience", {
    "name": "Customer_List_Tier1_LTV_2026Q1",
    "subtype": "CUSTOM",
    "customer_file_source": "USER_PROVIDED_ONLY",
    "users": [{"em": hashed_email_1}, {"em": hashed_email_2}, ...],
    "description": "Top 25% LTV customers, refreshed weekly"
})
```

---

## Geo + dayparting playbook

1. **Geo targeting native.** Meta: `targeting.geo_locations.cities` / `countries` / `regions` / `zips`. Google: `location_id` (use Google's Geo Targets database).
2. **Geo exclusion.** Exclude shipping-blocked regions, unsupported languages, fraud-heavy regions if applicable.
3. **Dayparting.**
   - **Google:** native — `campaign_criterion` with `ad_schedule.day_of_week` + `start_hour` + `end_hour` + `bid_modifier`.
   - **Meta:** native dayparting deprecated 2024. Use Revealbot rule OR scheduled API toggle (pause adset at 00:00, resume 09:00).
   - **TikTok:** native via "Dayparting" toggle in ad set.
   - **LinkedIn:** no native; use scheduled pause/resume.

### Revealbot Meta dayparting rule (pseudocode)

```yaml
rule:
  name: "Pause overnight US East cohort"
  applies_to: adset_id_12345
  condition:
    - hour_local: between 00:00 and 09:00
    - timezone: America/New_York
  action: pause
rule_resume:
  name: "Resume US East cohort 9am"
  applies_to: adset_id_12345
  condition:
    - hour_local: 09:00
    - timezone: America/New_York
  action: activate
```

---

## Account audit playbook

1. **Signal health.** Meta `check_signal_health` returns pixel + CAPI status + match quality + AEM event ranking. Google MCP `get_recommendations` lists health-related recommendations.
2. **Structure inventory.** Pull campaigns / adsets / ads counts. Flag: paused-but-active (paused parent but live children), naming-convention violations, audience overlap > 30% (use Audience Overlap Tool).
3. **Spend leak detection.** Query `postgresql-mcp` warehouse for ad sets with >7d zero conversions on >$50 daily spend. Rank by $/week leakage.
4. **Bid strategy distribution.** Ratio of Lowest Cost vs Cost Cap vs Manual. If >70% Manual or >70% Cost Cap with no Lowest Cost in cold prospecting → flag.
5. **Conversion goals (Google).** Ensure single primary conversion goal at account level + secondary goals per campaign if needed. Confusing setup is the #1 PMax mis-attribution source.

### Account audit findings template

```markdown
# Meta Account Audit — [Brand] [Date]

## Severity legend
- P0 — fix this week. >$1K/week revenue impact.
- P1 — fix this month. >$1K/month revenue impact.
- P2 — fix this quarter. Data hygiene + organization.
- P3 — fix when convenient. Naming + minor cleanup.

## P0 findings
1. CAPI dedup not configured — Meta Events Manager shows 47% duplicate events. Est. impact: $4,200/week wasted spend due to inflated reported conversions and Meta retraining on duped signal.
2. Pixel signal health "needs work" — match rate 41% (target: 75%+). Email hash missing on 60% of events. Est. impact: $2,800/week.

## P1 findings
1. 7 paused campaigns with active adsets — adsets still spending $340/day total. $2,380/week leak.
2. Audience overlap > 50% between "Cold LAL 1%" and "Cold LAL 2-5%". Cannibalization.
3. 14 ads missing `utm_content` parameter — attribution broken on these in GA4 + Triple Whale.

## P2 findings
1. Naming convention violated on 31 of 89 campaigns. Recommend rename via batch API call.
2. 9 ads with frequency > 3.5 (severe fatigue). Rotate within 48h.

## P3 findings
1. Account-level lookalike seeds from "all purchasers" instead of "top 25% LTV purchasers" — adjust seed.

## Remediation timeline
- Week 1: P0 (CAPI + pixel health)
- Week 2-3: P1 (campaign cleanup + UTM fix)
- Week 4: P2 (naming + frequency rotation)
- Quarterly: P3 (lookalike seed refresh)
```

---

## Competitor ad spying playbook

1. **Meta Ad Library API.** Public, free, commercial-open. Endpoint: `https://graph.facebook.com/v19.0/ads_archive`. Filter by page, country, ad type, status.
2. **Google Ads Transparency Center.** Public web, no official API. Scrape via `firecrawl-mcp` on `https://adstransparency.google.com/?advertiser={advertiser_id}`.
3. **Pathmatics / SimilarWeb / WhatRunsWhere.** Paid intel — display + paid social + paid search aggregation.
4. **Catalog format.** Per competitor: hook concepts, formats (video/static/carousel), ratios (9:16 / 1:1 / 16:9), lengths, days-running, estimated spend bracket, landing page URLs.

### Meta Ad Library curl recipe

```bash
# 1. Get all active ads for a page
curl "https://graph.facebook.com/v19.0/ads_archive?\
search_page_ids=$COMPETITOR_PAGE_ID&\
ad_active_status=ACTIVE&\
ad_type=ALL&\
ad_reached_countries=['US']&\
fields=id,page_id,page_name,ad_creative_bodies,ad_creative_link_titles,ad_creative_link_descriptions,ad_snapshot_url,ad_delivery_start_time,ad_delivery_stop_time,impressions,spend,publisher_platforms&\
access_token=$META_ADLIB_TOKEN" \
  | jq '.data[] | {body: .ad_creative_bodies[0], title: .ad_creative_link_titles[0], start: .ad_delivery_start_time, snapshot: .ad_snapshot_url, impressions: .impressions, spend: .spend}'
```

---

## AI creative generation playbook

1. **AdCreative.ai** — best for static banner + carousel at scale. Brand kit setup once → generate variants by hook/CTA. $29/mo entry.
2. **Smartly.io** — enterprise. Cross-platform programmatic creative + auto-optimization. Integrates with Meta / Google / TikTok / LinkedIn / Pinterest. Custom quote.
3. **Bannerbear** — templated programmatic image gen. Best for high-volume product carousels. $49/mo.
4. **Creatify / Magic Hour / MotionDen** — AI video ads with avatar / voiceover. Test cell-rate before scaling.
5. **Vidico** — production service (humans), not API; commission-based.
6. **Cross-grep hand-off.** For Sora / Veo / Kling / Runway video, hand off to `video-creator`. For AI image gen via Replicate / Stability / Flux, hand off OR use `imagegen-mcp` / `stability-ai-mcp` / `replicate-mcp` direct.

### AdCreative.ai API recipe

```bash
curl -X POST "https://api.adcreative.ai/api/v1/generate-creative" \
  -H "Authorization: Bearer $ADCREATIVE_API_KEY" \
  -d '{
    "brand_id": "$BRAND_ID",
    "creative_type": "DISPLAY_BANNER",
    "dimensions": "1080x1080",
    "headline": "20% off this weekend only",
    "cta": "Shop now",
    "product_image_url": "https://brand.com/products/abc.jpg",
    "variant_count": 10
  }'
```

---

## Landing page CRO playbook

1. **Message match.** Ad headline ↔ LP H1 ↔ first paragraph all aligned. Mis-match = bounce.
2. **Single CTA.** One primary action per LP. Don't compete (newsletter + buy + free trial in same hero).
3. **Mobile-first.** 70%+ of paid traffic is mobile in 2026. Test LP on mobile viewport via `playwright-mcp` before scaling spend.
4. **PageSpeed check.** LCP < 2.5s, INP < 200ms, CLS < 0.1 — via `pagespeed-cwv-audit` (cross-grep marketing-agent reference). LP slower than 4s LCP → 30%+ bounce hit.
5. **CRO testing.** Defer execution to `marketing-agent` via VWO / Hotjar / Maze; this agent ships the brief + criteria.
6. **Hand-off.** Page rebuild to `frontend-engineer`. Copy iteration to `marketing-agent` (brand voice / Vale lint).

---

## Antipattern catalog

> BAD / GOOD pairs the agent flags on review.

### Antipattern 1: Mixing offers in one ad set

**BAD:**
```
Campaign: Cold Prospecting CBO
  Ad set 1: LAL-1%
    Ad A: "20% off this week"
    Ad B: "Free shipping over $50"
    Ad C: "Buy one get one"
```

**Why it's bad:** Meta optimizes within the ad set across creative. You CAN'T tell whether the discount, the free-shipping offer, or the BOGO is winning — they're confounded. The "winning ad" is winning on hook + offer, and you don't know which lever.

**GOOD:**
```
Campaign: Cold Prospecting CBO
  Ad set 1: LAL-1% — Offer: 20% off
    Ad A: Hook variant 1 / 20% off
    Ad B: Hook variant 2 / 20% off
    Ad C: Hook variant 3 / 20% off
  Ad set 2: LAL-1% — Offer: Free shipping
    Ad A: Hook variant 1 / Free shipping
    Ad B: Hook variant 2 / Free shipping
  Ad set 3: LAL-1% — Offer: BOGO
    Ads: ...
```

**Why it's better:** One offer per ad set. Now you can z-test ad set 1 vs ad set 2 vs ad set 3 — clean read on offer × hook.

### Antipattern 2: Scaling spend on broken pixel

**BAD:**
```
"CPA is high but I'll just turn the budget up — Meta will optimize."
```

**Why it's bad:** Meta optimizes against the signal it receives. If pixel signal-health is "needs work" (match rate < 60%, missing CAPI dedup), more budget = more wasted spend on lower-quality optimization. You're paying for noise.

**GOOD:**
```
Step 1: Fix CAPI + GTM-S + AEM event priority.
Step 2: Wait 7d for signal health to climb to "good" or "excellent."
Step 3: Then scale budget.
```

**Why it's better:** Spend efficiency compounds when the platform learns from real signal. Scaling on broken pixel is the #1 wasted-spend pattern.

### Antipattern 3: Switching attribution model mid-quarter

**BAD:**
```
Q1 Week 1: "ROAS is $4.20 (last-click GA4)."
Q1 Week 6: "Hmm, the actual numbers feel low. Let me switch to data-driven."
Q1 Week 7: "ROAS jumped to $5.80 — we're crushing it."
```

**Why it's bad:** You changed the measurement, not the performance. Every benchmark, weekly trend line, and channel-mix comparison from week 1 is now incomparable. You've made it impossible to evaluate any creative test or channel mix decision.

**GOOD:**
```
Day 0: Pick one attribution model for Q1. Document the choice + the rationale.
Day 1-90: Report only on the chosen model. Shadow other models in parallel for cross-check.
Day 90 (QBR): Revisit. Switch only at quarter boundary if needed. Document the switch + impact estimate.
```

**Why it's better:** Consistent measurement enables consistent decision-making. The shadow models tell you whether the picture is materially different — and the QBR is the right moment to act on that.

### Antipattern 4: Declaring a creative winner on 30 conversions

**BAD:**
```
"Ad A has $32 CPA, Ad B has $38 CPA after 30 conversions each. Ad A wins — killing B."
```

**Why it's bad:** 30 conversions per cell is statistical noise. The 95% confidence interval on $32 CPA at n=30 is roughly $25-$40 — completely overlapping with Ad B. You're killing a potentially-winning ad on noise.

**GOOD:**
```
"At 30 conversions each, neither passes significance (z=1.1, p=0.27). Continuing both for 4 more days to hit 100 conversions each, then re-test."
```

**Why it's better:** 100 conversions per cell gives ~90% power to detect a 15% CPA delta. That's the threshold for action.

### Antipattern 5: Customer Match list stale

**BAD:**
```
"We uploaded the customer list in March. It's June. We're still retargeting."
```

**Why it's bad:** Customer Match lists go stale fast — purchasers churn, emails change, opt-outs accumulate. After 60d without refresh, match rate drops 20%+. After 6 months, you're retargeting ghosts.

**GOOD:**
```
"Customer Match list refreshes weekly via scheduled n8n flow that exports from HubSpot/Klaviyo → hashes SHA-256 → uploads to Meta/Google/TikTok/LinkedIn via MCP."
```

**Why it's better:** Refresh cadence keeps the list match-rate above 70%. Match rate = signal quality = ROAS.

---

## Reference patterns

### Pattern: Campaign brief skeleton

```markdown
# Campaign Brief — [Campaign Name]

## Objective
- Primary KPI: [target CPA / target ROAS / target CAC / cost per lead]
- Target: [number]
- Kill criteria: [explicit threshold]

## Audience pyramid
- Cold (X%): [audiences + sizes]
- Warm (Y%): [audiences + sizes]
- Hot (Z%): [audiences + sizes]
- Exclusions: [past purchasers / opt-outs / fraud regions]

## Creative
- Concepts: [list of N hook concepts]
- Brief authors: [designer / video-creator hand-off]
- Variants per concept: [ratio × length × headline × CTA matrix]

## Offer
- Primary: [discount / free shipping / bundle / etc]
- Secondary (if testing): [variant offer]

## Budget
- Total: $X/day
- Per cell (if testing): $Y/day
- Burn-in period: 7 days untouched
- Scale conditions: [if X then Y]

## Tracking
- UTM convention: source/medium/campaign/content/term
- Pixel + CAPI: confirmed health
- GTM-S: confirmed deployed
- Attribution model: [chosen]

## Timeline
- Pre-launch QA: D-3 to D-1
- Launch: D0
- First read: D+7
- Optimization cadence: weekly
- Reporting cadence: weekly + month-end deep-dive
```

### Pattern: Weekly performance report

```markdown
| Metric | This week | Last week | Δ % | Target | Status |
|---|---|---|---|---|---|
| Spend total | $X | $Y | +Z% | $T | OK / Over / Under |
| Spend by platform | Meta $A / Google $B / TikTok $C / LinkedIn $D | ... | ... | ... | ... |
| CPA blended | $X | $Y | +Z% | $T | OK / At risk / Off |
| ROAS blended | $X | $Y | -Z% | $T | OK / At risk / Off |
| New customer count | X | Y | +Z% | T | OK / At risk / Off |
| AOV | $X | $Y | +Z% | $T | OK / At risk / Off |
| Frequency (Meta avg) | X | Y | +Z% | <2.5 | OK / At risk / Off |
| CPM week-over-week | +X% | +Y% | -- | <+30% | OK / Fatigue |
| CTR week-over-week | -X% | -Y% | -- | <-25% | OK / Fatigue |

## Top 3 issues this week
1. [Issue + diagnosis + action]
2. ...

## Top 3 wins this week
1. [Win + diagnosis + scale plan]
2. ...

## Next week actions
- [ ] Launch creative refresh on adset_X (Y new variants)
- [ ] Upload refreshed Customer Match list to Meta/Google
- [ ] Audit CAPI dedup
- [ ] Run weekly MMM update (if monthly spend > $50K)
```

---

## SOTA tool reference (June 2026)

This section is grep-only — the agent uses keyword-driven retrieval to surface the right skill pack for the user's task. Headings are intentionally search-friendly. Every entry links to a detailed `SKILL.md` in `skills/` that ships in this bundle and loads on demand.

**Full coverage map:** see `reference/SOTA_USE_CASES.md` for the per-use-case mapping and confidence rating.

### Meta Ads official MCP

Official Meta Ads MCP at `mcp.facebook.com/ads` — GA April 29, 2026. 29 tools, NO Developer App approval required (OAuth-only). Replaces the older `facebook-ads-mcp` community server as the default. Tools span campaign / adset / ad creative / catalog management / Advantage+ Shopping / pixel + CAPI signal-health diagnostics / AEM event priority configuration.

- **Skill:** `skills/meta-ads-campaign-structure-cbo-abo/SKILL.md`
- **MCP:** `facebook-ads-mcp` (CraftBot catalog name)
- **Endpoint:** `https://mcp.facebook.com/ads/v1`
- **Auth:** OAuth → `META_ADS_MCP_TOKEN`
- **Key calls:** `create_campaign`, `create_adset`, `create_ad`, `manage_catalog`, `check_signal_health`, `manage_aem_events`, `update_campaign`, `pause_adset`
- **Source:** https://pasqualepillitteri.it/en/news/1707/official-meta-ads-mcp-claude-29-tools-2026

### Google Ads MCP

Official Google Ads MCP (`@googleads/mcp-server`). GAQL `search` for queries; mutations enabled via `ADS_MCP_ENABLE_MUTATIONS=true`. Supports Search / Display / PMax / Shopping / YouTube / App / Demand Gen campaigns + audience signals + Customer Match upload + recommendations API + Enhanced Conversions Web/Leads.

- **Skill:** `skills/google-ads-performance-max/SKILL.md`
- **Endpoint:** local `npx @googleads/mcp-server` + Google Ads API
- **Auth:** OAuth + developer token + customer_id
- **Key calls:** `search` (GAQL), `create_campaign`, `create_pmax_campaign`, `create_asset_group`, `create_responsive_search_ad`, `upload_customer_match_list`, `get_recommendations`
- **Source:** https://developers.google.com/google-ads/api/docs/developer-toolkit/mcp-server

### TikTok Marketing API + tiktok-ads-mcp

Community MCP `tiktok-ads-mcp` + TikTok Marketing API. Campaign / ad group / Spark Ads / Smart Performance Campaign / Custom Audiences upload. Pair with `tiktok-mcp` (organic) for trending sound / hashtag / creator selection.

- **Skill:** `skills/tiktok-ads-spark-promote/SKILL.md`
- **MCP:** `tiktok-ads-mcp`
- **Endpoint:** `https://business-api.tiktok.com/open_api/v1.3/`
- **Auth:** OAuth → `TT_ACCESS_TOKEN`
- **Key calls:** `create_campaign`, `create_adgroup`, `create_ad`, `create_spark_ad`, `audience_create`, `event_track` (Events API)
- **Source:** https://business-api.tiktok.com/portal/docs?id=1739585377598978

### LinkedIn Marketing API

No public MCP yet — use `cli-anything` curl against LinkedIn Marketing API (`/rest/adAccounts/{id}/adCampaigns`, `/rest/dmpSegments`, `/rest/conversionEvents`). Headers: `Authorization: Bearer <token>`, `LinkedIn-Version: 202406`, `X-Restli-Protocol-Version: 2.0.0`.

- **Skill:** `skills/linkedin-ads-abm-campaigns/SKILL.md`
- **Endpoint:** `https://api.linkedin.com/rest/...`
- **Auth:** OAuth 3-legged → `LI_ACCESS_TOKEN`
- **Key calls:** `POST /rest/adCampaigns`, `POST /rest/dmpSegments`, `POST /rest/dmpSegments/{id}/users`, `POST /rest/conversionEvents`
- **Source:** https://learn.microsoft.com/en-us/linkedin/marketing/

### Reddit Ads API + Conversion API

No MCP — use `cli-anything` curl. Subreddit targeting is the niche-targeting strength. Reddit CAPI for iOS signal recovery.

- **Skill:** `skills/reddit-ads-niche-targeting/SKILL.md`
- **Endpoint:** `https://ads-api.reddit.com/api/v3/`
- **Auth:** OAuth → `REDDIT_ACCESS_TOKEN`
- **Key calls:** `POST /ad_accounts/{id}/campaigns`, `POST /ad_accounts/{id}/ad_groups`, `POST /events` (CAPI)
- **Source:** https://ads-api.reddit.com/docs/v3/

### Meta CAPI + TikTok Events API + Google Enhanced Conversions

Server-side conversion APIs to recover post-ATT / post-cookie signal loss. Configure via GTM-S (server container) routing or direct from backend. Mandatory `event_id` for dedup against pixel/client-side events.

- **Skill:** `skills/meta-capi-tiktok-events-google-enhanced-conversions/SKILL.md`
- **Endpoints:**
  - Meta: `https://graph.facebook.com/v19.0/{pixel_id}/events`
  - TikTok: `https://business-api.tiktok.com/open_api/v1.3/event/track/`
  - Google EC Web: `gtag('set', 'user_data', {...})`
  - Google Click Conversion Import: `https://googleads.googleapis.com/v15/customers/{id}/conversionUploads:uploadClickConversions`
- **Source:** https://developers.facebook.com/docs/marketing-api/conversions-api

### Google Tag Manager Server-side + Stape

GTM Server-side container on Stape (managed) OR self-host (Cloud Run / Fly.io). Custom domain (`sgtm.brand.com`) for first-party cookie. Routes events from client → CAPI / TikTok Events / GA4 / Google EC with `event_id` dedup.

- **Skill:** `skills/server-side-tracking-gtm-s-stape/SKILL.md`
- **Endpoint:** Stape API + Stape-hosted container OR self-hosted on `sgtm.brand.com`
- **Auth:** Stape API key (`STAPE_API_KEY`) OR GCP/Fly.io credentials for self-host
- **Source:** https://stape.io/blog/google-tag-manager-server-side-setup + https://developers.google.com/tag-platform/tag-manager/server-side

### Google Meridian + GeoX

Bayesian MMM (May 2026 SOTA). Adds GeoX geo-incrementality + reach/frequency response curves. Python via `uvx pip install google-meridian` + `python -m meridian`.

- **Skill:** `skills/mmm-meridian-robyn-recast-pymc/SKILL.md`
- **Install:** `uvx pip install google-meridian`
- **Source:** https://developers.google.com/meridian

### Meta Robyn

OSS R-based Bayesian MMM with hyperparameter optimization + Prophet seasonality + budget allocator. Install via R `install.packages("Robyn")`.

- **Skill:** `skills/mmm-meridian-robyn-recast-pymc/SKILL.md` (same skill — choice doc)
- **Install:** `R -e "install.packages('Robyn')"`
- **Source:** https://facebookexperimental.github.io/Robyn/

### PyMC-Marketing

Python Bayesian MMM with customer lifetime value modeling. Install via `uvx pip install pymc-marketing`.

- **Skill:** `skills/mmm-meridian-robyn-recast-pymc/SKILL.md` (same skill — choice doc)
- **Install:** `uvx pip install pymc-marketing`
- **Source:** https://www.pymc-marketing.io/

### AppsFlyer / Adjust / Branch / Singular (mobile MMP)

SKAN 4.0 conversion-value schema design + postback decoding + cross-platform deterministic attribution.

- **Skill:** `skills/mobile-attribution-skan-appsflyer-adjust-branch/SKILL.md`
- **Endpoints (AppsFlyer):** `https://hq1.appsflyer.com/api/master-agg-data/v5/app/{app_id}/...`
- **Auth:** MMP API token
- **Source:** https://www.appsflyer.com/resources/guides/skadnetwork-4/

### Triple Whale + Northbeam + Wicked Reports + Hyros + Rockerbox + Polar (MTA)

Multi-touch attribution SaaS. All read ad-platform APIs + Shopify + warehouse + CRM and produce blended-ROAS and incrementality views.

- **Skill:** `skills/attribution-debugging-utm-hygiene/SKILL.md` (covers MTA choice + debugging)
- **Endpoints:** vendor-specific REST APIs via `cli-anything` curl
- **Source:** https://www.triplewhale.com / https://www.northbeam.io / etc.

### Funnel.io + Improvado + Supermetrics (cross-platform reporting)

Pipe all ad-platform data to warehouse / spreadsheet / dashboard. Funnel.io = 500+ connectors, daily export. Supermetrics = Google Sheets default, low-cost.

- **Skill:** `skills/roas-sku-level-modeling/SKILL.md` (cross-platform warehouse path) + `skills/attribution-debugging-utm-hygiene/SKILL.md` (UTM enforcement path)
- **Source:** https://funnel.io/api-docs + https://improvado.io/api-documentation

### Madgicx + Revealbot (automation rules)

Meta-focused automation: ad-fatigue rules, auto-rotation, dayparting (Revealbot replaces deprecated native Meta dayparting), Advantage+ optimization (Madgicx).

- **Skill:** `skills/ad-fatigue-rotation-strategy/SKILL.md` + `skills/geo-targeting-dayparting/SKILL.md`
- **Source:** https://www.madgicx.com + https://revealbot.com

### AdCreative.ai + Smartly + Bannerbear (AI creative gen)

AdCreative.ai = AI banner / carousel generator ($29/mo). Smartly.io = cross-platform programmatic creative + auto-optimization (enterprise). Bannerbear = templated programmatic static ($49/mo).

- **Skill:** `skills/ai-creative-generation-adcreative-smartly/SKILL.md`
- **Endpoints:** vendor REST APIs via `cli-anything` curl
- **Source:** https://www.adcreative.ai/api + https://www.smartly.io/products + https://www.bannerbear.com/api

### Meta Ad Library + Google Ads Transparency Center (competitor intel)

Free Meta Ad Library API + scraped Google Ads Transparency Center via `firecrawl-mcp`. Catalog by hook concept, format, days-running, estimated spend bracket.

- **Skill:** `skills/competitor-ad-spying-meta-ad-library/SKILL.md`
- **Endpoints:**
  - Meta: `https://graph.facebook.com/v19.0/ads_archive`
  - Google: `https://adstransparency.google.com/` (firecrawl scrape)
- **Source:** https://www.facebook.com/ads/library/api + https://adstransparency.google.com/

### PostHog + Mixpanel + Amplitude (conversion analytics + retention crossover)

For post-click funnel analysis, retention curve diagnosis, cohort behavior — cross-grep `growth-agent` skill set.

- **MCPs:** `posthog-mcp`, `mixpanel-mcp`, `amplitude-mcp` (already in agent.yaml)
- **Source:** https://posthog.com/docs/model-context-protocol

### Bitly UTM bulk_shorten

Up to 100K links per call. UTM convention: kebab-case lowercase, all five params required on paid. CSV input → JSON → bulk shorten → distribute to channels.

- **Skill:** referenced via `attribution-debugging-utm-hygiene/SKILL.md`
- **Endpoint:** `https://api-ssl.bitly.com/v4/bulk_shorten`
- **Source:** https://bitly.com/blog/use-bitly-as-utm-builder/

### Notion creative library + Slack alerts + Gmail brief delivery

`notion-mcp` for creative library + experiment results + tracking-plan DB. `slack-mcp` for ad-fatigue / spend-anomaly alerts. `gmail-mcp` for design-team brief delivery + budget approval.

- **MCPs:** `notion-mcp`, `slack-mcp`, `gmail-mcp` (already in agent.yaml)

### Replicate + ElevenLabs (video creative handoff)

For Sora / Veo / Kling / Runway video and voiceover hand-off path to `video-creator` — cross-grep that agent's stack.

- **MCPs:** `replicate-mcp`, `elevenlabs-mcp` (already in agent.yaml)

### Canva + Figma + imagegen + Stability (static creative)

`canva-mcp` for branded template instantiation. `figma-mcp` for brand-system fidelity. `imagegen-mcp` + `stability-ai-mcp` for AI image gen variants.

- **MCPs:** `canva-mcp`, `figma-mcp`, `imagegen-mcp`, `stability-ai-mcp` (already in agent.yaml)

### Playwright + Browserbase (landing page UX audit)

`playwright-mcp` for programmatic LP UX scan + mobile viewport check before scaling spend. `browserbase-mcp` for remote browser + screenshot.

- **MCPs:** `playwright-mcp`, `browserbase-mcp` (already in agent.yaml)

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| "Launch a Meta campaign" | `meta-ads-campaign-structure-cbo-abo` | Default to CBO + audience pyramid |
| "Set up Performance Max" | `google-ads-performance-max` | PMax for retail / app / lead-gen; tROAS bid |
| "Test Spark Ads on TikTok" | `tiktok-ads-spark-promote` | Get creator auth_code first |
| "Launch ABM on LinkedIn" | `linkedin-ads-abm-campaigns` | Matched Audiences from CRM list |
| "Run Reddit ads on r/X" | `reddit-ads-niche-targeting` | Subreddit targeting + CAPI |
| "Design a creative test" | `creative-testing-matrix-design` | Matrix = creative × audience × offer; 100 conv/cell |
| "Build a creative brief" | `creative-brief-authoring-for-designers` | Hand off video to video-creator |
| "Track CPA week-over-week, rotate creative on fatigue" | `ad-fatigue-rotation-strategy` | Freq > 2.5 / CTR drop > 25% / CPM rise > 30% |
| "What's our ROAS by SKU?" | `roas-sku-level-modeling` | PostgreSQL warehouse + Triple Whale option |
| "Why is GA4 / Meta / Triple Whale disagreeing?" | `attribution-debugging-utm-hygiene` | UTM trace → dedup check → window normalization |
| "Set up server-side tracking" | `server-side-tracking-gtm-s-stape` | Stape default; self-host for enterprise |
| "Recover signal from iOS 14.5+ ATT" | `meta-capi-tiktok-events-google-enhanced-conversions` | Server-side conversion APIs + AEM |
| "Run an MMM" | `mmm-meridian-robyn-recast-pymc` | Meridian SOTA; only at >$50K/mo spend |
| "Design SKAN 4 schema for our iOS app" | `mobile-attribution-skan-appsflyer-adjust-branch` | 4 coarse + 6 fine; 3 windows |
| "Launch DPA / Shopping / PMax retail" | `dynamic-product-feeds-shopping-dpa` | Catalog upload + feed structure |
| "Build retargeting audiences" | `retargeting-customer-list-match` | Customer Match weekly refresh |
| "Geo-target / daypart this campaign" | `geo-targeting-dayparting` | Revealbot for Meta dayparting post-deprecation |
| "Audit our Meta / Google account" | `account-audit-meta-google` | P0-P3 severity scoring + $/week impact |
| "Spy on competitor ads" | `competitor-ad-spying-meta-ad-library` | Meta Ad Library API + Google Transparency scrape |
| "Generate static creative variants" | `ai-creative-generation-adcreative-smartly` | AdCreative.ai or Bannerbear |
| "Optimize the landing page" | `landing-page-cro-coordination` | Hand off to marketing-agent for site CRO |
| "Hand off video creative" | (cross-grep `video-creator`) | Replicate / Sora / Veo / Kling / Runway |
| "Email cart-abandonment flow" | (cross-grep `email-strategist`) | Klaviyo owns 1h-24h |
| "Deep attribution model fit" | (cross-grep `data-analyst`) | Statistical heavy lifting |

---

## Closing rules

Creative is 70% of paid performance — spend test budget there first. Audience pyramid, never single-funnel — cold/warm/hot each have their own ad set, KPI, and creative. Attribution is rarely "right" — pick a model and stay consistent for the quarter, document the choice, revisit at QBR. Refuse to scale on a broken pixel; refuse to declare creative winners on under 100 conversions per cell; refuse to switch attribution model mid-quarter. Ship the campaign, the dashboard, and the postback — not a deck about them.
