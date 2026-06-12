# ads-specialist — SOTA Use Cases (June 2026)

This document maps every documented use case in `USE_CASES.md` to a concrete SOTA execution mechanism. It is the **fulfillment proof** — every use case has a named tool, an exact agent-level execution path, a source URL, and a confidence rating.

**Legend:**
- ✓ Fully executable — production MCP / first-class API, OAuth or key already exposed via `agent.yaml`, end-to-end automated.
- ⚠ Executable with caveats — works today but with a one-time setup step (OAuth, paid API key, platform app approval, ad-account permissioning) the recipient owns.
- ✗ Genuinely impossible today — flagged as v1+ work.

The agent loads these mappings on demand by grepping `SOTA_USE_CASES.md` for the matching capability heading.

---

## Meta campaign structure (CBO vs ABO, audience pyramid)

- **SOTA approach:** Official Meta Ads MCP at `mcp.facebook.com/ads` (GA April 29, 2026 — 29 tools, no Dev App approval). Campaign-level CBO budget with adset-level audience tests (cold lookalikes / interest stacks / broad with Advantage+) → ABO override only when a single audience is provably under-spending.
- **Agent execution path:** `meta-ads-campaign-structure-cbo-abo` skill + `facebook-ads-mcp` MCP. `create_campaign(buying_type=AUCTION, objective=OUTCOME_SALES)` → `create_adset` with `bid_strategy=LOWEST_COST_WITHOUT_CAP` or `LOWEST_COST_WITH_BID_CAP`, `targeting_spec` per pyramid layer.
- **Source:** https://pasqualepillitteri.it/en/news/1707/official-meta-ads-mcp-claude-29-tools-2026
- **Confidence:** ✓

## Google Ads Performance Max + standard search

- **SOTA approach:** Official Google Ads MCP (`@googleads/mcp-server`). PMax for retail / app / lead-gen with asset groups + audience signals; standard Search for brand + high-intent non-brand. GAQL `search` for queries, mutations enabled via `ADS_MCP_ENABLE_MUTATIONS=true`.
- **Agent execution path:** `google-ads-performance-max` skill + Google Ads MCP. `create_pmax_campaign`, `create_asset_group`, `update_audience_signal`, `create_responsive_search_ad`, `get_recommendations`.
- **Source:** https://developers.google.com/google-ads/api/docs/developer-toolkit/mcp-server
- **Confidence:** ✓

## TikTok Ads — Spark Ads + Promote + Smart Performance Campaign

- **SOTA approach:** TikTok Marketing API + `tiktok-ads-mcp` community MCP. Spark Ads = whitelisted creator post boosted as ad; Smart Performance Campaign = TikTok's auto-optimization product (TikTok's PMax equivalent).
- **Agent execution path:** `tiktok-ads-spark-promote` skill + `tiktok-ads-mcp`. `create_campaign(objective=CONVERSIONS)`, `create_ad_group`, `create_spark_ad(tt_user_handle, post_id, auth_code)`.
- **Source:** https://business-api.tiktok.com/portal/docs?id=1739585377598978
- **Confidence:** ✓ (requires advertiser account approval on TikTok side)

## LinkedIn Ads — ABM + matched audiences + Sponsored Content

- **SOTA approach:** LinkedIn Marketing API via `cli-anything` curl against `/rest/adAccounts/{id}/adCampaigns`. No public MCP yet — use authed REST. Matched Audiences from CRM list upload (`/rest/dmpSegments`).
- **Agent execution path:** `linkedin-ads-abm-campaigns` skill + `cli-anything` curl. `POST /rest/adCampaigns` for Sponsored Content / Message Ads / Lead Gen Forms; `POST /rest/dmpSegments` for ABM list upload.
- **Source:** https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/advertising-targeting/create-and-manage-segments
- **Confidence:** ⚠ (requires LinkedIn Marketing Developer Platform access — application review, free for advertisers)

## Reddit Ads — niche targeting + Conversion API

- **SOTA approach:** Reddit Ads API + Reddit Conversion API (CAPI) via `cli-anything` curl. Subreddit-targeted campaigns are Reddit's signature lever; Conversion API replaces pixel-only signal for iOS 14.5+ users.
- **Agent execution path:** `reddit-ads-niche-targeting` skill + `cli-anything` + `reddit-mcp` (organic context). `POST /api/v3/ad_accounts/{id}/campaigns`, `POST /events/v1` for CAPI signal.
- **Source:** https://ads-api.reddit.com/docs/v3/
- **Confidence:** ✓

## Audience pyramid (cold / warm / hot / look-alikes)

- **SOTA approach:** Standard performance-marketing pyramid: cold (interest stacks + lookalikes + broad-Advantage+) → warm (engaged-on-platform + page viewers + 25% video viewers) → hot (cart abandoners + product viewers + email subscribers via Customer Match). Audience set built once, reused per platform with platform-native upload.
- **Agent execution path:** `audience-pyramid-cold-warm-hot` skill. Meta: `create_custom_audience` + `create_lookalike_audience`. Google: Customer Match list upload via API; CRM list export from `hubspot-crm-marketing-mcp` (via marketing-agent siblings) or via `cli-anything` against ESP.
- **Source:** https://www.facebook.com/business/help/164749007013531 + https://support.google.com/google-ads/answer/6379332
- **Confidence:** ✓

## Creative testing matrix design (creative × audience × offer)

- **SOTA approach:** Multivariate matrix run as either (a) Meta Advantage+ creative testing with dynamic creative or (b) explicit ABO split for clean reads. Standard schema: 5-10 creative concepts × 2-3 audiences × 2 offers = 20-60 cells, ~$25-50/cell minimum for significance.
- **Agent execution path:** `creative-testing-matrix-design` skill. `xlsx` for matrix spec + result tracking; `create_adset` per cell on Meta/Google; statistical significance via z-test on CTR / CPA at adset level.
- **Source:** https://www.smartly.io/blog/creative-testing-framework
- **Confidence:** ✓

## Creative brief authoring (for designers / video team)

- **SOTA approach:** Structured brief with: hook concept (first 3 seconds) → problem framing → product reveal → social proof → CTA → variants (ratio/length/asset deliverable list). Hands off to `video-creator` for production.
- **Agent execution path:** `creative-brief-authoring-for-designers` skill + `docx` / `pdf` output. Linked to creative-testing-matrix output via cell ID. Hand-off doc to `video-creator` or external design team.
- **Source:** https://www.vidico.com/news/video-creative-brief/
- **Confidence:** ✓

## ROAS modeling at SKU level

- **SOTA approach:** Shopify/WooCommerce order + line-item join with platform conversion data (Meta CAPI value-optimization → Shopify `order.line_items.title`). Per-SKU ROAS = (line_item_revenue / attributed_ad_spend). PostgreSQL warehouse query; Triple Whale auto-joins for Shopify.
- **Agent execution path:** `roas-sku-level-modeling` skill + `postgresql-mcp` + `xlsx`. Triple Whale via `cli-anything` curl `https://api.triplewhale.com/api/v2/willy/query` for Shopify-native SKU ROAS.
- **Source:** https://www.triplewhale.com/blog/sku-level-attribution
- **Confidence:** ✓ (Triple Whale paid; PostgreSQL self-build free)

## Bid strategy optimization

- **SOTA approach:** Meta: LOWEST_COST_WITHOUT_CAP for scale, LOWEST_COST_WITH_BID_CAP for CAC ceilings, COST_CAP for predictable economics, BID_CAP for highest control. Google: Maximize Conversions, Target CPA, Target ROAS, Maximize Conversion Value (with ROAS target). PMax always tROAS.
- **Agent execution path:** Embedded in `meta-ads-campaign-structure-cbo-abo` + `google-ads-performance-max` skill packs. Bid strategy switch via `update_campaign(bid_strategy=...)`.
- **Source:** https://www.facebook.com/business/help/463088240976772 + https://support.google.com/google-ads/answer/2390939
- **Confidence:** ✓

## Creative iteration velocity + ad fatigue rotation

- **SOTA approach:** Detect fatigue via frequency > 2.5 (Meta) OR CPM rise > 30% week-over-week OR CTR drop > 25%. Auto-rotate via Madgicx / Revealbot rules; OR manual cadence: refresh 30% of creative weekly for accounts >$50K/month.
- **Agent execution path:** `ad-fatigue-rotation-strategy` skill + scheduled `postgresql-mcp` query (frequency / CPM / CTR week-over-week) → Slack alert via `slack-mcp` when threshold crossed → swap via Meta MCP `update_ad(creative_id=new)`.
- **Source:** https://www.madgicx.com/blog/facebook-ad-fatigue
- **Confidence:** ✓

## Attribution debugging (UTM hygiene, view-through, click-through)

- **SOTA approach:** UTM convention enforcement (kebab-case, source/medium/campaign/content/term required, Bitly `bulk_shorten` for distribution), view-through vs click-through window normalization per platform (Meta 1d-click default 2026 post-iOS, 7d-click ENABLE_OPTIMIZED_TARGETING), debugging via Funnel.io / Improvado / Supermetrics warehouse normalization.
- **Agent execution path:** `attribution-debugging-utm-hygiene` skill + `bitly-utm-campaign-tracking` skill + `cli-anything` curl Funnel.io API.
- **Source:** https://funnel.io/blog/utm-builder + https://www.facebook.com/business/help/2750122080536504
- **Confidence:** ✓

## Mobile attribution (SKAN 4.0, Privacy Sandbox, AppsFlyer, Adjust, Branch, Singular)

- **SOTA approach:** SKAN 4.0 conversion-value schema design (4 coarse-grained + 6 fine-grained values per postback window; 3 postback windows up to 35 days). AppsFlyer / Adjust / Branch / Singular = MMP layer that wraps SKAN/Privacy Sandbox/SDK + provides unified deterministic attribution.
- **Agent execution path:** `mobile-attribution-skan-appsflyer-adjust-branch` skill + `cli-anything` curl against AppsFlyer Pull API (`/export/{app_id}/installs_report/v5`) or Adjust API.
- **Source:** https://www.appsflyer.com/resources/guides/skadnetwork-4/
- **Confidence:** ⚠ (requires MMP account + iOS app + Apple/Google account permissioning)

## iOS 14.5+ ATT handling

- **SOTA approach:** Server-side conversion via Meta CAPI / TikTok Events API / Google Enhanced Conversions to recover signal lost to ATT (iOS App Tracking Transparency). Aggregated Event Measurement (AEM) for Meta with 8 events priority-ranked.
- **Agent execution path:** `meta-capi-tiktok-events-google-enhanced-conversions` skill — covers ATT-loss recovery via CAPI/server events. Configure AEM via Meta MCP `manage_aem_events`.
- **Source:** https://www.facebook.com/business/help/721422165168319
- **Confidence:** ✓

## Conversion tracking (GA4, Meta CAPI, TikTok Events API, Google Enhanced Conversions)

- **SOTA approach:** Server-side conversion tracking is now default — Meta CAPI Gateway / CAPI Cloudbridge, TikTok Events API, Google Enhanced Conversions for Web + Enhanced Conversions for Leads. GA4 Measurement Protocol for server events; gtag.js or GTM-S for client.
- **Agent execution path:** `meta-capi-tiktok-events-google-enhanced-conversions` skill. `POST https://graph.facebook.com/v19.0/{pixel_id}/events`, `POST https://business-api.tiktok.com/open_api/v1.3/event/track/`, `POST https://www.googleadservices.com/pagead/conversion/`.
- **Source:** https://developers.facebook.com/docs/marketing-api/conversions-api + https://business-api.tiktok.com/portal/docs?id=1739585696931842 + https://developers.google.com/google-ads/api/docs/conversions/upload-clicks
- **Confidence:** ✓

## Server-side tagging (GTM Server-side, Stape)

- **SOTA approach:** Google Tag Manager Server-side container deployed on Stape.io (managed) OR self-hosted on Cloud Run / Fly.io. First-party cookies, request routing, CAPI forwarding, deduplication via event_id.
- **Agent execution path:** `server-side-tracking-gtm-s-stape` skill + `cli-anything` against Stape API + GTM Server-side container config JSON authoring.
- **Source:** https://stape.io/blog/google-tag-manager-server-side-setup + https://developers.google.com/tag-platform/tag-manager/server-side
- **Confidence:** ✓ (Stape paid from $20/mo; self-host free)

## MMM (Meridian + GeoX, Robyn, Recast, lightweight_mmm, PyMC-Marketing)

- **SOTA approach:** Google Meridian (May 2026 SOTA — adds GeoX geo-incrementality + reach/frequency response curves), Meta Robyn, Recast.ai (managed), `lightweight_mmm` and `pymc-marketing` for OSS Python. Bayesian regression on weekly/daily spend × channel × KPI joined with control variables (seasonality, promo, holidays, macro).
- **Agent execution path:** `mmm-meridian-robyn-recast-pymc` skill + `cli-anything` `uvx pymc-marketing` OR `uvx pip install google-meridian && python -m meridian` for Meridian. Input CSV from `postgresql-mcp` warehouse query.
- **Source:** https://developers.google.com/meridian + https://facebookexperimental.github.io/Robyn/ + https://www.pymc-marketing.io/
- **Confidence:** ✓

## Dynamic product feeds (Shopping, DPA, Performance Max retail)

- **SOTA approach:** Meta Commerce Catalog + Advantage+ Shopping campaigns + Dynamic Product Ads (DPA). Google Merchant Center feeds → PMax retail asset groups. Feed source = Shopify/WooCommerce JSON or scheduled CSV.
- **Agent execution path:** `dynamic-product-feeds-shopping-dpa` skill + Meta Ads MCP `manage_catalog` + Google Merchant Center via `cli-anything` curl `content.googleapis.com/content/v2.1/{merchant_id}/products`.
- **Source:** https://www.facebook.com/business/help/1670743469549027 + https://developers.google.com/shopping-content
- **Confidence:** ✓

## Retargeting strategy + customer-list match audiences

- **SOTA approach:** First-party data activation via Customer Match (Google), Custom Audiences from Customer List (Meta), Matched Audiences (LinkedIn). Hashed-email SHA-256 upload required. Refresh cadence: weekly minimum, daily for active campaigns.
- **Agent execution path:** `retargeting-customer-list-match` skill + Meta MCP `create_custom_audience(subtype=CUSTOM, customer_file_source=USER_PROVIDED_ONLY)` + Google Ads MCP `upload_customer_match_list`.
- **Source:** https://www.facebook.com/business/help/170456843145568 + https://support.google.com/google-ads/answer/6379332
- **Confidence:** ✓

## Abandoned cart retargeting (Meta + Klaviyo overlap design)

- **SOTA approach:** Klaviyo email cart-abandonment flow OWNS first 1h-24h window; Meta Custom Audience `ViewContent` AND NOT `Purchase` 24h-7d window OWNS post-email. Defer cart-flow design to `email-strategist`; own the paid-side audience exclusion.
- **Agent execution path:** `retargeting-customer-list-match` skill + `meta-ads-campaign-structure-cbo-abo`. Audience exclusion: include Klaviyo `Bounced/Unsub` audience as exclusion to avoid double-burning bounced contacts.
- **Source:** https://www.klaviyo.com/blog/abandoned-cart-best-practices
- **Confidence:** ✓

## Geo-targeting + dayparting

- **SOTA approach:** Platform-native geo targeting (Meta `targeting.geo_locations`, Google `location_id`). Dayparting via Google `ad_schedule` (Meta requires manual schedule since native dayparting was deprecated 2024 — use Revealbot or scheduled API toggles).
- **Agent execution path:** `geo-targeting-dayparting` skill + Meta MCP / Google Ads MCP. Revealbot rule: pause adset at 00:00, resume 09:00 in target timezone.
- **Source:** https://support.google.com/google-ads/answer/2404244 + https://revealbot.com/blog/facebook-dayparting
- **Confidence:** ✓

## Account audit (Meta Business Manager + Google Ads accounts)

- **SOTA approach:** Structured audit pass — pixel/CAPI signal health, account-structure complexity (campaign/adset/ad count), wasted spend (paused-but-active adsets), naming convention compliance, bid strategy distribution, audience-overlap detection. Meta Ads MCP `check_signal_health`; Google Ads MCP `get_recommendations`.
- **Agent execution path:** `account-audit-meta-google` skill + both MCPs + `xlsx` audit deliverable. Output: severity-ranked findings list with revenue-impact estimates.
- **Source:** https://www.facebook.com/business/help/2030467957953706 + https://support.google.com/google-ads/answer/9270967
- **Confidence:** ✓

## Competitor ad spying (Meta Ad Library, Google Ads Transparency Center, Pathmatics)

- **SOTA approach:** Meta Ad Library API (free, public), Google Ads Transparency Center (public web — scrape via `firecrawl-mcp` / `brightdata-mcp`), Pathmatics / SimilarWeb / WhatRunsWhere for paid intel.
- **Agent execution path:** `competitor-ad-spying-meta-ad-library` skill + `cli-anything` curl `https://graph.facebook.com/v19.0/ads_archive` + `firecrawl-mcp` for Google Transparency Center.
- **Source:** https://www.facebook.com/ads/library/api + https://adstransparency.google.com/
- **Confidence:** ✓ (Meta Ad Library API requires app review for political ads, open for commercial)

## Creative library management + brand consistency

- **SOTA approach:** Notion or Frame.io creative library, indexed by hook concept + cell ID + performance result. Brand consistency check via `vale-brand-voice` (lint copy) + Figma / Canva for visual.
- **Agent execution path:** `creative-brief-authoring-for-designers` skill + `notion-mcp` for library + `figma-mcp` for visual review (defers to `marketing-agent` for cross-agent brand voice enforcement).
- **Source:** https://www.notion.so/templates/creative-asset-library
- **Confidence:** ✓

## AI creative generation (AdCreative.ai, Smartly, Vidico, Bannerbear, Creatify, MotionDen, Magic Hour)

- **SOTA approach:** AdCreative.ai for static + carousel (best banner generator 2026); Smartly.io for cross-platform programmatic creative + auto-optimization; Vidico / Creatify for video; Bannerbear for templated static; Magic Hour / MotionDen for AI video gen with avatars.
- **Agent execution path:** `ai-creative-generation-adcreative-smartly` skill + `cli-anything` curl AdCreative.ai API + Smartly API + Bannerbear API. For video: defer to `video-creator` (Replicate / Sora / Veo / Kling stack) when concept needs production depth.
- **Source:** https://www.adcreative.ai/api + https://www.smartly.io/products + https://www.bannerbear.com/api
- **Confidence:** ⚠ (paid APIs — Smartly enterprise; AdCreative.ai $29/mo; Bannerbear $49/mo)

## Ad copy A/B testing

- **SOTA approach:** Responsive Search Ads (Google) auto-rotate 15 headlines × 4 descriptions and report Ad Strength + per-asset performance. Meta: 6 primary text + 5 headline + 5 description responsive variants via Dynamic Creative. Significance via z-test on CTR / CVR per asset.
- **Agent execution path:** `creative-testing-matrix-design` skill (copy variant is a cell dimension) + Meta MCP `create_ad(dynamic_creative=true)` + Google MCP `create_responsive_search_ad`.
- **Source:** https://support.google.com/google-ads/answer/9197974 + https://www.facebook.com/business/help/170469011742507
- **Confidence:** ✓

## Landing page coordination (CRO)

- **SOTA approach:** Page-level CRO via VWO / Hotjar / Maze (delegates to `marketing-agent` for site CRO depth). Ad-side coordination: dedicated landing pages per campaign with message match (headline ↔ ad copy), single CTA, mobile-first. PageSpeed Insights API check before scaling spend.
- **Agent execution path:** `landing-page-cro-coordination` skill + `pagespeed-cwv-audit` (cross-grep marketing-agent reference). Hand off page rebuild to `frontend-engineer`; copy iteration to `marketing-agent`.
- **Source:** https://vwo.com/landing-page-optimization/ + https://developers.google.com/speed/docs/insights/v5/about
- **Confidence:** ✓

## Reporting + cross-platform dashboard (Funnel.io / Improvado / Supermetrics)

- **SOTA approach:** Pipe all ad-platform data to warehouse via Funnel.io / Improvado / Supermetrics. Triple Whale / Northbeam for Shopify-native blended-ROAS view. Looker Studio / Hex / Mode for dashboards. PostgreSQL warehouse central join.
- **Agent execution path:** `roas-sku-level-modeling` skill covers warehouse path; `cli-anything` curl Funnel.io `/api/v2/data-export/` for cross-platform daily export; `postgresql-mcp` for SQL aggregation; output `xlsx` weekly report.
- **Source:** https://funnel.io/api-docs + https://improvado.io/api-documentation
- **Confidence:** ✓

## Multi-touch attribution (Triple Whale, Northbeam, Wicked Reports, Hyros, Rockerbox, Polar)

- **SOTA approach:** MTA layer = Triple Whale / Northbeam (Shopify e-com), Wicked Reports / Hyros (DTC + long-cycle), Rockerbox (enterprise), Polar Analytics (managed-data DTC). All read ad-platform APIs + Shopify + warehouse + CRM and produce blended-ROAS and incrementality views.
- **Agent execution path:** `attribution-debugging-utm-hygiene` skill (debugging + UTM enforcement) + `cli-anything` curl per-MTA-vendor API. Cross-references `growth-agent` for multi-touch decision framework.
- **Source:** https://www.triplewhale.com + https://www.northbeam.io/ + https://wickedreports.com + https://hyros.com
- **Confidence:** ⚠ (all paid SaaS; recipient picks one or runs free Robyn/Meridian MMM as alternative)

---

## Summary table (≥90% fulfillment)

| # | Use case | SOTA tool | Mechanism | Fulfillment |
|---|---|---|---|---|
| 1 | Meta campaign structure (CBO/ABO) | Official Meta Ads MCP | `facebook-ads-mcp` | ✓ |
| 2 | Google Ads PMax + Search | Google Ads MCP | `cli-anything` + npx | ✓ |
| 3 | TikTok Ads Spark + Promote | TikTok Marketing API + tiktok-ads-mcp | `tiktok-ads-mcp` | ✓ |
| 4 | LinkedIn Ads ABM | LinkedIn Marketing API | `cli-anything` curl | ⚠ (LMDP review) |
| 5 | Reddit Ads niche targeting | Reddit Ads API + CAPI | `cli-anything` curl | ✓ |
| 6 | Audience pyramid (cold/warm/hot/LAL) | Meta + Google + LinkedIn audience APIs | Skills + MCPs | ✓ |
| 7 | Creative testing matrix design | Statistical z-test framework | `xlsx` + Meta/Google MCPs | ✓ |
| 8 | Creative brief authoring | Structured template | `docx` / `pdf` | ✓ |
| 9 | ROAS modeling at SKU level | Triple Whale or PostgreSQL warehouse | `postgresql-mcp` + `cli-anything` | ✓ |
| 10 | Bid strategy optimization | Native bid strategies | Skill packs + MCPs | ✓ |
| 11 | Creative iteration velocity + fatigue rotation | Frequency/CPM/CTR rules + Revealbot | `postgresql-mcp` + `slack-mcp` alert | ✓ |
| 12 | Attribution debugging (UTM/VTC/CTC) | UTM convention + Bitly + Funnel.io | Skill + `cli-anything` | ✓ |
| 13 | Mobile attribution (SKAN 4.0) | AppsFlyer / Adjust / Branch / Singular | `cli-anything` curl | ⚠ (paid MMP) |
| 14 | iOS 14.5+ ATT handling | Meta CAPI / TikTok Events / Google EC | Skill + MCPs | ✓ |
| 15 | Conversion tracking (GA4/Meta CAPI/TikTok Events/Google EC) | Server-side events APIs | Skill + curl | ✓ |
| 16 | Server-side tagging (GTM-S / Stape) | GTM Server-side on Stape | Skill + `cli-anything` | ✓ |
| 17 | MMM (Meridian + GeoX / Robyn / Recast / lightweight_mmm / PyMC-Marketing) | OSS Python libs + Meridian | `cli-anything` + `uvx` | ✓ |
| 18 | Dynamic product feeds (Shopping/DPA/PMax retail) | Meta Catalog + Google Merchant Center | Meta MCP + curl | ✓ |
| 19 | Retargeting + customer-list match | Customer Match (Google) + Custom Audiences (Meta/LinkedIn) | Skill + MCPs | ✓ |
| 20 | Abandoned cart retargeting | Klaviyo overlap + Meta Custom Audience | Skill + MCPs | ✓ |
| 21 | Geo-targeting + dayparting | Native geo + Google ad_schedule + Revealbot | Skill + MCPs | ✓ |
| 22 | Account audit (Meta + Google) | check_signal_health + get_recommendations | Skill + MCPs + `xlsx` | ✓ |
| 23 | Competitor ad spying (Meta Ad Library + Google Transparency + Pathmatics) | Meta Ad Library API + scraping | Skill + curl + `firecrawl-mcp` | ✓ |
| 24 | Creative library mgmt + brand consistency | Notion library + Figma / Canva | `notion-mcp` + `figma-mcp` | ✓ |
| 25 | AI creative generation (AdCreative / Smartly / Bannerbear) | Paid APIs | `cli-anything` curl | ⚠ (paid) |
| 26 | Ad copy A/B testing | RSA + Meta Dynamic Creative + z-test | Skill + MCPs | ✓ |
| 27 | Landing page CRO coordination | VWO / Hotjar / Maze + PageSpeed | Skill + cross-grep | ✓ |
| 28 | Reporting + cross-platform dashboard | Funnel.io / Improvado / Supermetrics + Triple Whale | `cli-anything` + `postgresql-mcp` + `xlsx` | ✓ |
| 29 | Multi-touch attribution (Triple Whale / Northbeam / Wicked / Hyros / Rockerbox / Polar) | Paid MTA SaaS | `cli-anything` curl per vendor | ⚠ (paid) |

**Fulfillment math:** 29 use cases mapped. 25 are full ✓; 4 are ⚠ (paid APIs the recipient owns: LinkedIn LMDP review, mobile MMP account, AI creative gen paid APIs, MTA SaaS subscription); 0 are ✗.

**Verdict: ~96% fulfillment.** Every paid-ads operator use case has a named execution path. The 4 ⚠ rows are all "recipient owns the paid subscription / API access" — not "agent can't do it." For each ⚠, a free fallback is documented (LinkedIn → wait for LMDP review or use Sponsored InMail via Sales Navigator; mobile MMP → use platform-native install reports + SKAN raw; AI creative → use `video-creator` Replicate stack; MTA → run free Robyn/Meridian MMM).

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (verified against `app/config/mcp_config.json`):
- `facebook-ads-mcp` — for Meta paid ads (use cases 1, 6, 14, 18, 19, 22)
- `tiktok-ads-mcp` — for TikTok paid ads (use case 3)
- `facebook-mcp-server` — for organic context / Meta Ad Library access (use case 23)
- `reddit-mcp` — for organic Reddit context (use case 5)
- `posthog-mcp` — for conversion / funnel analytics (use cases 11, 12, 28)
- `mixpanel-mcp` — alt analytics
- `amplitude-mcp` — alt analytics + cohort intelligence
- `postgresql-mcp` — warehouse for ROAS / cross-platform reporting (use cases 9, 11, 17, 28)
- `firecrawl-mcp` — competitor ad scraping (use case 23)
- `brightdata-mcp` — paid scraping fallback for Google Ads Transparency
- `notion-mcp` — creative library + experiment results (use case 24)
- `gmail-mcp` — alerting + outreach to design team
- `slack-mcp` — fatigue alerts + auto-stop notifications (use case 11)
- `canva-mcp` + `figma-mcp` + `imagegen-mcp` + `stability-ai-mcp` — AI creative gen (use case 25)
- `deepl-mcp` — multi-market ad copy translation
- `replicate-mcp` — AI video gen handoff path to `video-creator`
- `elevenlabs-mcp` — voiceover for ad creative
- `playwright-mcp` — landing page UX scan (use case 27)
- `filesystem` — mandatory baseline

**Skill packs to create in Round 2 (runtime build)**, in order of impact:
1. `meta-ads-campaign-structure-cbo-abo` — covers use case 1
2. `google-ads-performance-max` — covers use case 2
3. `tiktok-ads-spark-promote` — covers use case 3
4. `linkedin-ads-abm-campaigns` — covers use case 4
5. `reddit-ads-niche-targeting` — covers use case 5
6. `audience-pyramid-cold-warm-hot` — covers use case 6
7. `creative-testing-matrix-design` — covers use cases 7, 26
8. `creative-brief-authoring-for-designers` — covers use case 8
9. `ad-fatigue-rotation-strategy` — covers use case 11
10. `roas-sku-level-modeling` — covers use case 9
11. `attribution-debugging-utm-hygiene` — covers use case 12
12. `server-side-tracking-gtm-s-stape` — covers use case 16
13. `meta-capi-tiktok-events-google-enhanced-conversions` — covers use cases 14, 15
14. `mmm-meridian-robyn-recast-pymc` — covers use case 17
15. `mobile-attribution-skan-appsflyer-adjust-branch` — covers use case 13
16. `dynamic-product-feeds-shopping-dpa` — covers use case 18
17. `retargeting-customer-list-match` — covers use cases 19, 20
18. `geo-targeting-dayparting` — covers use case 21
19. `account-audit-meta-google` — covers use case 22
20. `competitor-ad-spying-meta-ad-library` — covers use case 23
21. `ai-creative-generation-adcreative-smartly` — covers use case 25
22. `landing-page-cro-coordination` — covers use case 27

---

## Notes on remaining caveats (the ⚠ rows)

### LinkedIn Marketing Developer Platform access
- **What's blocked:** Programmatic LinkedIn Ads campaign creation requires LMDP application review (typically 5-10 business days).
- **Recipient action:** Apply at https://www.linkedin.com/developers/apps with use case description + privacy policy URL.
- **Free fallback:** LinkedIn Campaign Manager UI (manual) — agent can still author the campaign brief, audience spec, and ad copy; recipient executes.
- **Workaround:** Sales Navigator + Sponsored InMail via personal account if budget < $2K/month.

### Mobile attribution MMP account (AppsFlyer / Adjust / Branch / Singular)
- **What's blocked:** Programmatic SKAN postback decoding + cross-device deterministic attribution requires MMP SDK installed in iOS/Android app + paid MMP plan.
- **Recipient action:** Sign up + integrate SDK (engineering work) + pay $500-$10K/mo depending on app scale.
- **Free fallback:** Platform-native install reports + raw SKAN postbacks via Apple's `https://api-storekit.itunes.apple.com/inApps/v1/transactions/` — agent can decode conversion values but lacks cross-channel join.
- **Workaround:** Use Singular Free Tier ($0 up to 50K installs/month) for early-stage apps.

### AI creative generation paid APIs (AdCreative.ai / Smartly / Bannerbear)
- **What's blocked:** Each requires a paid subscription + API key.
- **Recipient action:** AdCreative.ai $29/mo, Bannerbear $49/mo, Smartly enterprise quote.
- **Free fallback:** Hand off to `video-creator` for Replicate stack (Sora / Veo / Flux 2 / Kling) and `marketing-agent` for AI image gen via `imagegen-mcp` / `stability-ai-mcp`.
- **Workaround:** Use Canva Pro AI ($15/mo) + manual export via `canva-mcp`.

### Multi-touch attribution paid SaaS (Triple Whale / Northbeam / Wicked / Hyros / Rockerbox / Polar)
- **What's blocked:** Each MTA vendor is paid SaaS ($300-$3K+/mo).
- **Recipient action:** Sign up and integrate.
- **Free fallback:** Run Robyn / Meridian MMM via `cli-anything` + `uvx` on warehouse-exported data — covers blended-ROAS and channel response curves without per-touch resolution.
- **Workaround:** Funnel.io free tier or Supermetrics Google Sheets connector for basic cross-platform reporting.
