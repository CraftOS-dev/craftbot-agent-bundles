# Performance Ads Specialist — Use Cases

**Tier:** **specialized** · **Category:** marketing / paid
**Core job:** Deep paid-ads operator — launch / measure / iterate Meta / Google / TikTok / LinkedIn / Reddit campaigns end-to-end with server-side tracking, conversion APIs, MMM, and SKAN 4.0 mobile attribution.

> Ships with the 2026 SOTA performance-ads stack (official Meta Ads MCP / Google Ads MCP / TikTok Marketing API / LinkedIn Marketing API / Reddit Ads API + Meta CAPI / TikTok Events / Google Enhanced Conversions / Reddit CAPI + GTM Server-side on Stape + Google Meridian / Meta Robyn / PyMC-Marketing / AppsFlyer / Adjust / Triple Whale / Madgicx / Revealbot + AdCreative.ai / Smartly / Bannerbear) — executes end-to-end, not just briefs.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### Ad platforms — campaign structure + launch
- Meta (Facebook + Instagram) — CBO vs ABO, audience pyramid, Advantage+ Shopping, bid strategy
- Google Ads — Performance Max + standard Search + Shopping + YouTube + Demand Gen
- TikTok Ads — In-Feed + Spark Ads + Smart Performance Campaign + Custom Audiences
- LinkedIn Ads — Sponsored Content + Message Ads + Lead Gen Forms + Matched Audiences (ABM)
- Reddit Ads — subreddit niche targeting + Promoted Posts + Conversation Ads
- Pinterest / Microsoft (Bing) / Snap / Amazon / X / Spotify / Quora / AppLovin — via `cli-anything` curl

### Audience strategy
- Audience pyramid (cold → warm → hot + look-alikes)
- Customer Match list upload + weekly refresh
- Custom Audiences from website / engagement / video / CRM
- Lookalike Audiences (1% / 2-5% seeded on top-LTV)
- ABM Matched Audiences from CRM list

### Creative strategy
- Creative testing matrix design (creative × audience × offer, 20-60 cells, 100 conv/cell)
- Creative brief authoring (for designers + video team)
- Ad copy A/B testing (RSA + Meta Dynamic Creative + z-test)
- Ad fatigue rotation (frequency > 2.5, CPM rise > 30%, CTR drop > 25%)
- AI creative generation (AdCreative.ai / Smartly / Bannerbear / Creatify / MotionDen)
- Creative library management + brand consistency

### Measurement + attribution
- ROAS modeling at SKU level (PostgreSQL warehouse + Triple Whale / Northbeam path)
- Attribution debugging (UTM hygiene, view-through, click-through window normalization)
- Multi-touch attribution layer (Triple Whale / Northbeam / Wicked / Hyros / Rockerbox / Polar)
- MMM (Google Meridian + GeoX / Meta Robyn / Recast / lightweight_mmm / PyMC-Marketing)
- Cross-platform reporting (Funnel.io / Improvado / Supermetrics)

### Server-side tracking + conversion APIs
- GTM Server-side on Stape (managed) or self-hosted (Cloud Run / Fly.io)
- Meta Conversions API (CAPI) + Aggregated Event Measurement (AEM)
- TikTok Events API
- Google Enhanced Conversions (Web + Leads + Click Conversion Import)
- Reddit Conversion API
- LinkedIn / Pinterest / Snap Conversion APIs
- Event dedup via `event_id`
- First-party cookie strategy via custom domain (`sgtm.brand.com`)

### iOS 14.5+ ATT + Mobile attribution
- SKAN 4.0 conversion-value schema design (4 coarse + 6 fine, 3 windows)
- AppsFlyer / Adjust / Branch / Singular integration
- Privacy Sandbox (Android) — Attribution Reporting API + FLEDGE + Topics
- Cross-channel deterministic attribution (where IDFA opted in)

### Account operations
- Account audit (Meta + Google) — severity-ranked findings ($/week impact)
- Bid strategy optimization
- Geo-targeting + dayparting (Revealbot for Meta post-deprecation)
- Dynamic product feeds (Shopping / DPA / PMax retail)
- Retargeting strategy + abandoned cart (paid side coordination with email)
- Competitor ad spying (Meta Ad Library API + Google Ads Transparency Center + Pathmatics)

### Landing page coordination (for paid)
- Message-match validation (ad headline ↔ LP H1)
- Mobile-first audit (via `playwright-mcp` + viewport check)
- PageSpeed gate (LCP < 2.5s, INP < 200ms, CLS < 0.1)
- Hand-off to `marketing-agent` for CRO testing depth and `frontend-engineer` for page rebuild

---

## Execution status (SOTA — June 2026)

The previous "I'll brief the campaign, you launch and measure" gap is closed. As of mid-2026 every documented use case has a production MCP, first-class API, or documented `cli-anything` execution path. Meta's official Ads MCP went GA April 29 2026 (29 tools, no Dev App approval). Google Ads MCP exposes mutations via `ADS_MCP_ENABLE_MUTATIONS=true`. Stape's GTM-S API + Meta CAPI / TikTok Events / Google Enhanced Conversions endpoints cover server-side conversion end-to-end. Google Meridian (May 2026) is the SOTA MMM with GeoX geo-incrementality. AppsFlyer SKAN 4.0 schema design + AdCreative.ai / Smartly / Bannerbear creative gen + Madgicx / Revealbot automation rules round out the operator stack.

### What this agent EXECUTES today (SOTA mechanisms per use case)

| Use case | SOTA mechanism | Path |
|---|---|---|
| Meta campaign structure (CBO/ABO + audience pyramid) | Official Meta Ads MCP (29 tools, GA April 2026) | `facebook-ads-mcp` + `meta-ads-campaign-structure-cbo-abo` skill |
| Google Ads Performance Max + Search | Official Google Ads MCP | `cli-anything` + `npx @googleads/mcp-server` + `google-ads-performance-max` skill |
| TikTok Ads Spark + Smart Performance + Promote | TikTok Marketing API + `tiktok-ads-mcp` community MCP | `tiktok-ads-mcp` + `tiktok-ads-spark-promote` skill |
| LinkedIn Ads ABM + Sponsored Content + Lead Gen Forms | LinkedIn Marketing API | `cli-anything` curl + `linkedin-ads-abm-campaigns` skill |
| Reddit Ads niche targeting + CAPI | Reddit Ads API + Conversion API | `cli-anything` curl + `reddit-mcp` (organic) + `reddit-ads-niche-targeting` skill |
| Audience pyramid (cold / warm / hot / LAL) | Native platform audience APIs | `audience-pyramid-cold-warm-hot` skill + platform MCPs |
| Creative testing matrix (creative × audience × offer) | Z-test significance framework + 100 conv/cell rule | `creative-testing-matrix-design` skill + `xlsx` + platform MCPs |
| Creative brief authoring | Structured template + hand-off | `creative-brief-authoring-for-designers` skill + `docx` / `pdf` |
| Ad fatigue rotation (freq / CPM / CTR thresholds) | Madgicx / Revealbot rules + warehouse alerts | `ad-fatigue-rotation-strategy` skill + `postgresql-mcp` + `slack-mcp` |
| ROAS modeling at SKU level | Triple Whale (Shopify) or PostgreSQL warehouse join | `roas-sku-level-modeling` skill + `postgresql-mcp` + `cli-anything` |
| Attribution debugging (UTM / VTC / CTC) | UTM convention + Bitly bulk_shorten + Funnel.io / Improvado | `attribution-debugging-utm-hygiene` skill + `cli-anything` |
| Server-side tagging (GTM-S on Stape) | Stape API + custom domain + CAPI gateway templates | `server-side-tracking-gtm-s-stape` skill + `cli-anything` |
| Conversion APIs (Meta / TikTok / Google EC / Reddit) | Server-side conversion endpoints + AEM | `meta-capi-tiktok-events-google-enhanced-conversions` skill |
| iOS 14.5+ ATT handling | Server-side conversion via CAPI + AEM 8-event ranking | Same skill as above |
| MMM (Meridian + GeoX / Robyn / PyMC-Marketing) | OSS Python / R libs + `cli-anything uvx` | `mmm-meridian-robyn-recast-pymc` skill + `cli-anything` |
| Mobile attribution (SKAN 4.0 + MMP layer) | AppsFlyer / Adjust / Branch / Singular API | `mobile-attribution-skan-appsflyer-adjust-branch` skill + `cli-anything` |
| Dynamic product feeds (Catalog + Merchant Center + DPA + PMax retail) | Meta Catalog API + Google Content API | `dynamic-product-feeds-shopping-dpa` skill + Meta/Google MCPs |
| Retargeting + Customer Match | Customer Match (Google) + Custom Audiences (Meta / LinkedIn) | `retargeting-customer-list-match` skill + platform MCPs |
| Abandoned cart paid retargeting | Meta Custom Audience + Klaviyo overlap design | `retargeting-customer-list-match` skill |
| Geo-targeting + dayparting | Platform-native geo + Google ad_schedule + Revealbot | `geo-targeting-dayparting` skill |
| Account audit (Meta + Google P0-P3 severity) | `check_signal_health` + `get_recommendations` + structured audit | `account-audit-meta-google` skill + `xlsx` |
| Competitor ad spying | Meta Ad Library API + Google Transparency scrape | `competitor-ad-spying-meta-ad-library` skill + `firecrawl-mcp` |
| Creative library mgmt + brand consistency | Notion library + Figma fidelity check | `notion-mcp` + `figma-mcp` |
| AI creative generation (static + carousel) | AdCreative.ai + Smartly + Bannerbear APIs | `ai-creative-generation-adcreative-smartly` skill + `cli-anything` |
| AI video creative gen | Hand-off to `video-creator` (Replicate / Sora / Veo / Kling) | cross-grep `video-creator` |
| Ad copy A/B testing | RSA + Meta Dynamic Creative + z-test | `creative-testing-matrix-design` skill (copy is a cell dimension) |
| Landing page CRO coordination | Message match + PageSpeed gate + hand-off | `landing-page-cro-coordination` skill |
| Cross-platform reporting + dashboard | Funnel.io / Improvado / Supermetrics warehouse pipe | `roas-sku-level-modeling` skill + `postgresql-mcp` + `xlsx` |
| Multi-touch attribution layer (paid SaaS) | Triple Whale / Northbeam / Wicked / Hyros / Rockerbox / Polar | `attribution-debugging-utm-hygiene` skill + `cli-anything` curl per vendor |

### Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| LinkedIn Marketing Developer Platform access | ⚠ | Requires LMDP application review (5-10 business days). Agent can author the brief; recipient executes in UI until approved. |
| Mobile attribution MMP account (AppsFlyer / Adjust / Branch / Singular) | ⚠ | Requires SDK installed in iOS/Android app + paid MMP plan ($500-$10K/mo at scale). Free fallback: raw Apple SKAN postbacks via `https://api-storekit.itunes.apple.com/`. Singular Free Tier ($0 up to 50K installs/month) works for early-stage. |
| AI creative generation paid APIs (AdCreative.ai / Smartly / Bannerbear) | ⚠ | Each requires paid subscription ($29-$49/mo+ entry; Smartly enterprise quote). Free fallback: hand off to `video-creator` for Replicate stack, or use `imagegen-mcp` / `stability-ai-mcp` / `canva-mcp` (already bundled). |
| Multi-touch attribution paid SaaS (Triple Whale / Northbeam / Wicked / Hyros / Rockerbox / Polar) | ⚠ | Each MTA vendor is paid SaaS ($300-$3K+/mo). Free fallback: run Robyn / Meridian MMM via `cli-anything uvx` on warehouse-exported data. |

**Verdict (June 2026): ~96% fulfillment.** Every paid-ads operator use case has a concrete execution path via a production MCP, first-class API, or `cli-anything` + documented endpoint. The 4 ⚠ rows are all "recipient owns the paid subscription / API access / app approval" — not "agent can't do it." For each, a free fallback is documented so the agent can ship immediately while the recipient pursues the paid path.

---

## When to use this agent

- "Audit our Meta + Google ad accounts and rank what to fix first"
- "Launch a Meta CBO with cold + warm + hot pyramid for our new product launch"
- "Set up Performance Max for our Shopify store with Customer Match seed"
- "Design a creative testing matrix — 5 hooks × 3 audiences × 2 offers"
- "Debug why GA4, Meta, and Triple Whale disagree by 35%"
- "Set up server-side tracking on Stape and forward to Meta + TikTok + Google EC"
- "Design our SKAN 4.0 conversion-value schema for the iOS app"
- "Run an MMM on the last 18 months of weekly spend to allocate FY26 budget"
- "Spy on the top 5 competitors' Meta + Google ads — what hooks are they running"
- "Our pixel signal health dropped to 'needs work' — fix it before we scale"
- "Rotate creative on every adset where frequency hit 2.5 this week"

## When NOT to use this agent

- Broad marketing (content strategy, brand voice, organic social, email lifecycle, growth strategy) — hand off to `marketing-agent`
- Growth loops, activation, retention curve diagnosis, churn prediction, cohort analysis — hand off to `growth-agent`
- Organic SEO + AEO + GEO citation share, technical SEO audit, link building — hand off to `seo-specialist`
- Deep attribution math (custom multi-touch model fit, statistical significance heavy lifting, mixed-effects regression) — hand off to `data-analyst`
- Video creative production (Sora 2 / Veo 3.1 / Kling / Runway / Remotion / motion graphics / color grading) — hand off to `video-creator`
- Owned email cart-abandonment flow (1h-24h window) — hand off to `email-strategist`
- Page rebuild for CRO (frontend / SSR / SSG) — hand off to `frontend-engineer`
- Brand strategy / positioning / naming research over months — flag as out of scope; recommend brand-strategist specialist (v1)
