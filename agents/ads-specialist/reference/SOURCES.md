# Performance Ads Specialist — Source Attribution

Section-to-source map for `soul.md` and `role.md`. **Not** loaded into context — for human verification.

Raw URLs are in `agent.yaml → sources`, `reference/INVENTORY.md`, and the per-use-case mapping in `reference/SOTA_USE_CASES.md`. Bundled skill packs (Round 2) will each carry a `## Sources` section in their `SKILL.md` extending the URLs below.

---

## soul.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Title + persona intro (action-verb first) | composition synthesis from `reference/SOTA_USE_CASES.md` + per-agent prompt seed | Verbs paired with specific tools / MCPs |
| Three convictions | per-agent prompt seed: creative-is-70%, audience-pyramid-beats-single-funnel, attribution-pick-and-stay | Industry-standard performance ads convictions (Madgicx blog + Smartly framework + 2024-2026 operator consensus) |
| Purpose | `reference/SOTA_USE_CASES.md` + per-agent prompt seed (sibling defer rules to marketing-agent / growth-agent / seo-specialist / data-analyst / video-creator) | |
| Execution stack | `reference/SOTA_USE_CASES.md` — 22 bundled skill packs distilled from per-use-case SOTA research | Verbatim names match `agent.yaml → enabled_skills` Bundled section |
| When invoked — Account audit mode | Meta Business Help (`check_signal_health`) + Google Ads recommendations API docs + Industry standard P0-P3 severity scoring | |
| When invoked — Campaign launch mode | Meta Ads campaign structure best practices (CBO/ABO decision, audience pyramid) + Google PMax campaign setup docs | |
| When invoked — Creative testing mode | Smartly creative testing framework + general statistical significance practice | https://www.smartly.io/blog/creative-testing-framework |
| When invoked — Attribution debugging mode | UTM hygiene + Bitly bulk_shorten + Funnel.io normalization patterns | https://funnel.io/blog/utm-builder |
| When invoked — Server-side tracking mode | GTM Server-side + Stape setup guides | https://stape.io/blog/google-tag-manager-server-side-setup + https://developers.google.com/tag-platform/tag-manager/server-side |
| When invoked — MMM mode | Google Meridian docs + Meta Robyn docs + PyMC-Marketing docs | https://developers.google.com/meridian + https://facebookexperimental.github.io/Robyn/ + https://www.pymc-marketing.io/ |
| When invoked — Mobile attribution mode | AppsFlyer SKAN 4.0 guide + Apple App Store Connect docs | https://www.appsflyer.com/resources/guides/skadnetwork-4/ |
| When invoked — Competitor intel mode | Meta Ad Library API docs + Google Ads Transparency Center | https://www.facebook.com/ads/library/api + https://adstransparency.google.com/ |
| Core operating rules | merged: creative-is-70% (Madgicx + Smartly + 2025-2026 operator consensus), audience-pyramid (Meta best practices), pick-attribution-and-stay (data-driven attribution literature), pixel+CAPI as floor (Meta CAPI docs), one-offer-per-adset (statistical significance practice), 100-conv-per-cell (power calculation industry norm), first-week-burn-in (Meta learning phase docs), frequency cap = health (Madgicx + Revealbot fatigue thresholds), Customer Match weekly refresh (Meta + Google docs), iOS 14.5+ permanence (Apple ATT framework + Meta AEM), Klaviyo 1h-24h owns cart (Klaviyo best practices), GTM-S event_id required (GTM-S dedup mechanism), UTM kebab-case required (Funnel.io / Bitly convention), MMM only at scale (industry norm), no tool you can't drive (operator-builder principle) | |
| Mode-specific decisions | one entry per mode, each keyed to the matching upstream doc | |
| Quality gates | merged: pixel + CAPI health (Meta), UTM trace (Funnel.io), event dedup (GTM-S), creative cell sizing (Smartly), attribution model documented (data-driven literature), account structure compliance (Meta + Google audit guides), GTM-S deployment QA (Stape docs), MMM input data quality (Meridian + Robyn requirements) | |
| Output format | Industry-standard performance ads deliverables (campaign brief, weekly performance report, account audit, attribution memo, server-side tracking spec, MMM result deck, creative testing matrix) | |
| Communication style | distilled from operator-tone consensus: lead with action, concrete numbers, name the metric, specific about failure, honest about attribution uncertainty, don't sell the platform, strip AI-slop | |
| When to push back | informed by: refuse-scale-on-broken-pixel (Meta CAPI docs), 100-conv-cell-significance (z-test power calc), single-attribution-model (data-driven attribution literature), one-offer-per-adset (statistical confounding), dayparting deprecation (Meta product update 2024), MMM noise floor (industry norm), GTM-S iOS recovery (Meta AEM) | |
| When to defer | per-agent prompt seed: marketing-agent (broad), growth-agent (loops + activation + retention), seo-specialist (organic + AEO), data-analyst (attribution math), video-creator (video production), email-strategist (owned cart flow), frontend-engineer (page rebuild) | |
| First-conversation routine questions | standard PROACTIVE.md self-init pattern (PROGRESS.md decision #3 / METHODOLOGY.md footer); questions adapted to paid-ads workflows: primary ad platforms, monthly ad spend, attribution stack | |
| Closing rule | distilled from the three convictions + the operator-builder principle | |

---

## role.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Capability reference → Ad platforms supported | per-agent prompt seed + each platform's official Marketing API docs | |
| Capability reference → Bid strategies supported | Meta Business Help, Google Ads Help, TikTok Marketing API docs, LinkedIn Marketing API docs, Reddit Ads docs | |
| Capability reference → Conversion APIs / server-side endpoints | per-platform CAPI / Events API / Enhanced Conversions docs | |
| Capability reference → Attribution windows | each platform's official attribution-window documentation, 2026-current defaults | |
| Capability reference → Mobile MMP options | AppsFlyer / Adjust / Branch / Singular / Kochava / Tenjin official sites + 2026 review posts | |
| Capability reference → MMM tooling | Google Meridian + Meta Robyn + Recast + lightweight_mmm + PyMC-Marketing official docs | |
| Capability reference → MTA SaaS | Triple Whale / Northbeam / Wicked / Hyros / Rockerbox / Polar official sites | |
| Capability reference → Cross-platform reporting | Funnel.io / Improvado / Supermetrics / Whatagraph / Glew / Bullets official sites | |
| Capability reference → Creative tooling | Smartly / AdCreative.ai / Bannerbear / Creatify / Vidico / MotionDen / Magic Hour official sites | |
| Capability reference → Server-side tagging tools | GTM-S docs + Stape + Snowplow | |
| Capability reference → Competitor intel tools | Meta Ad Library API + Google Ads Transparency + Pathmatics / WhatRunsWhere / SpyFu / SimilarWeb | |
| Meta campaign structure playbook | Meta Business Help campaign structure docs + Madgicx CBO/ABO decision framework | https://www.facebook.com/business/help/ |
| Google Ads PMax playbook | Google Ads PMax product docs + Google Ads Help asset group best practices | https://support.google.com/google-ads/answer/10724817 |
| TikTok Ads playbook | TikTok Marketing API + Spark Ads documentation | https://business-api.tiktok.com/portal/docs |
| LinkedIn Ads ABM playbook | LinkedIn Marketing API + DMP Segments docs | https://learn.microsoft.com/en-us/linkedin/marketing/ |
| Reddit Ads playbook | Reddit Ads API + Reddit CAPI docs | https://ads-api.reddit.com/docs/v3/ |
| Audience pyramid playbook | composition synthesis from per-platform audience docs + industry-standard pyramid framework | |
| Creative testing matrix playbook | Smartly creative testing framework + statistical significance z-test formulas | https://www.smartly.io/blog/creative-testing-framework |
| Ad fatigue rotation playbook | Madgicx fatigue thresholds + Revealbot rule patterns | https://www.madgicx.com/blog/facebook-ad-fatigue + https://revealbot.com/ |
| ROAS at SKU playbook | Triple Whale SKU attribution post + general DTC warehouse pattern | https://www.triplewhale.com/blog/sku-level-attribution |
| Attribution debugging playbook | UTM convention practice + Funnel.io / Improvado normalization patterns + Meta dedup docs | https://funnel.io/blog/utm-builder |
| Server-side tracking playbook | Stape docs + GTM-S docs + CAPI gateway template | https://stape.io/blog/google-tag-manager-server-side-setup + https://developers.google.com/tag-platform/tag-manager/server-side |
| Conversion APIs playbook | Meta CAPI + TikTok Events API + Google Enhanced Conversions + Reddit CAPI docs | |
| MMM playbook | Google Meridian + Meta Robyn + PyMC-Marketing + Recast docs | https://developers.google.com/meridian + https://facebookexperimental.github.io/Robyn/ |
| Mobile attribution SKAN playbook | AppsFlyer SKAN 4.0 guide + Apple Privacy + Singular SKAN encoder docs | https://www.appsflyer.com/resources/guides/skadnetwork-4/ |
| Dynamic product feeds playbook | Meta Catalog API + Google Merchant Center Content API + DPA / PMax retail docs | https://www.facebook.com/business/help/1670743469549027 + https://developers.google.com/shopping-content |
| Retargeting playbook | Customer Match (Google) + Custom Audiences (Meta) + Matched Audiences (LinkedIn) docs | https://www.facebook.com/business/help/170456843145568 + https://support.google.com/google-ads/answer/6379332 |
| Geo + dayparting playbook | Google Ads ad_schedule + Meta dayparting deprecation note + Revealbot dayparting guide | https://support.google.com/google-ads/answer/2404244 + https://revealbot.com/blog/facebook-dayparting |
| Account audit playbook | composition synthesis from Meta `check_signal_health` + Google `get_recommendations` + industry-standard severity scoring | |
| Competitor ad spying playbook | Meta Ad Library API docs + Google Ads Transparency Center | https://www.facebook.com/ads/library/api + https://adstransparency.google.com/ |
| AI creative generation playbook | AdCreative.ai API + Smartly API + Bannerbear API docs | https://www.adcreative.ai/api + https://www.smartly.io/products + https://www.bannerbear.com/api |
| Landing page CRO playbook | composition synthesis from VWO / Hotjar / Maze docs + PageSpeed Insights API + Core Web Vitals thresholds | https://vwo.com/landing-page-optimization/ + https://developers.google.com/speed/docs/insights/v5/about |
| Antipattern catalog | composition synthesis distilling top-5 operator anti-patterns from 2024-2026 paid-ads operator consensus (mixing offers, scaling broken pixel, mid-quarter attribution switch, declaring winner on n=30, Customer Match list stale) | |
| Reference patterns (campaign brief, weekly report) | composition synthesis from operator-standard deliverable templates | |
| SOTA tool reference | `reference/SOTA_USE_CASES.md` + per-tool docs from agent.yaml `sources` block + below SOTA sources table | |
| SOTA execution playbook (skill pack mapping table) | `reference/SOTA_USE_CASES.md` summary table + agent.yaml `enabled_skills` cross-walk | |
| Closing rules | mirrors soul.md closing | |

---

## SOTA tool sources (June 2026)

These sources back the `role.md → SOTA tool reference (June 2026)` section, the `reference/SOTA_USE_CASES.md` per-use-case mapping, and the 22 bundled skill packs in `skills/` (Round 2 will populate `SKILL.md` content). Each skill pack's `SKILL.md` will have a `## Sources` section duplicating + extending these.

| Tool | Source URL | Used for |
|---|---|---|
| Official Meta Ads MCP | https://pasqualepillitteri.it/en/news/1707/official-meta-ads-mcp-claude-29-tools-2026 | `skills/meta-ads-campaign-structure-cbo-abo/SKILL.md` — 29 tools, no Dev App approval, campaign + adset + ad creative + catalog + Advantage+ Shopping + signal health + AEM |
| Official Google Ads MCP | https://developers.google.com/google-ads/api/docs/developer-toolkit/mcp-server | `skills/google-ads-performance-max/SKILL.md` — GAQL search + mutations, PMax / Search / Display / YouTube / App / Demand Gen + Customer Match + recommendations |
| TikTok Marketing API | https://business-api.tiktok.com/portal/docs?id=1739585377598978 | `skills/tiktok-ads-spark-promote/SKILL.md` — campaigns / ad groups / Spark Ads / Smart Performance / Custom Audiences |
| LinkedIn Marketing API | https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/advertising-targeting/create-and-manage-segments | `skills/linkedin-ads-abm-campaigns/SKILL.md` — Matched Audiences upload, Sponsored Content / Message Ads / Lead Gen Forms / Conversation Ads |
| Reddit Ads API + Conversion API | https://ads-api.reddit.com/docs/v3/ | `skills/reddit-ads-niche-targeting/SKILL.md` — subreddit targeting + Promoted Posts / Conversation Ads + Reddit CAPI |
| Meta Conversions API (CAPI) | https://developers.facebook.com/docs/marketing-api/conversions-api | `skills/meta-capi-tiktok-events-google-enhanced-conversions/SKILL.md` — server-side conversion + AEM 8-event priority |
| TikTok Events API | https://business-api.tiktok.com/portal/docs?id=1739585696931842 | Same skill — TikTok server-side conversion |
| Google Enhanced Conversions | https://developers.google.com/google-ads/api/docs/conversions/upload-clicks | Same skill — Web + Leads + Click Conversion Import |
| Google Tag Manager Server-side | https://developers.google.com/tag-platform/tag-manager/server-side | `skills/server-side-tracking-gtm-s-stape/SKILL.md` — server container, event_id dedup, custom domain |
| Stape.io | https://stape.io/blog/google-tag-manager-server-side-setup | Same skill — managed GTM-S hosting + CAPI gateway templates |
| Google Meridian | https://developers.google.com/meridian | `skills/mmm-meridian-robyn-recast-pymc/SKILL.md` — SOTA Bayesian MMM + GeoX geo-incrementality |
| Meta Robyn | https://facebookexperimental.github.io/Robyn/ | Same skill — R-based Bayesian MMM + Prophet seasonality + budget allocator |
| PyMC-Marketing | https://www.pymc-marketing.io/ | Same skill — Python Bayesian MMM + customer LTV modeling |
| AppsFlyer SKAN 4.0 guide | https://www.appsflyer.com/resources/guides/skadnetwork-4/ | `skills/mobile-attribution-skan-appsflyer-adjust-branch/SKILL.md` — conversion-value schema design + postback decoding |
| Triple Whale | https://www.triplewhale.com | `skills/roas-sku-level-modeling/SKILL.md` + `skills/attribution-debugging-utm-hygiene/SKILL.md` — Shopify-native SKU attribution + blended-ROAS |
| Northbeam | https://www.northbeam.io/ | Same skills — DTC multi-touch + channel incrementality |
| Funnel.io | https://funnel.io/api-docs | `skills/attribution-debugging-utm-hygiene/SKILL.md` + `skills/roas-sku-level-modeling/SKILL.md` — cross-platform warehouse pipe + UTM normalization |
| Madgicx | https://www.madgicx.com/blog/facebook-ad-fatigue | `skills/ad-fatigue-rotation-strategy/SKILL.md` — Meta fatigue thresholds + Advantage+ rules |
| Revealbot | https://revealbot.com/blog/facebook-dayparting | `skills/ad-fatigue-rotation-strategy/SKILL.md` + `skills/geo-targeting-dayparting/SKILL.md` — rules + Meta dayparting (post-native-deprecation) |
| AdCreative.ai API | https://www.adcreative.ai/api | `skills/ai-creative-generation-adcreative-smartly/SKILL.md` — AI banner / carousel generation |
| Smartly.io | https://www.smartly.io/products | Same skill — cross-platform programmatic creative + auto-optimization |
| Smartly creative testing framework | https://www.smartly.io/blog/creative-testing-framework | `skills/creative-testing-matrix-design/SKILL.md` — matrix design + cell sizing + significance |
| Bannerbear API | https://www.bannerbear.com/api | `skills/ai-creative-generation-adcreative-smartly/SKILL.md` — templated programmatic static |
| Meta Ad Library API | https://www.facebook.com/ads/library/api | `skills/competitor-ad-spying-meta-ad-library/SKILL.md` — free public commercial-open competitor ad intel |
| Google Ads Transparency Center | https://adstransparency.google.com/ | Same skill — Google Ads competitor intel via `firecrawl-mcp` scrape |
| Vidico creative brief | https://www.vidico.com/news/video-creative-brief/ | `skills/creative-brief-authoring-for-designers/SKILL.md` — structured video / static brief template |
| Bitly bulk_shorten | https://bitly.com/blog/use-bitly-as-utm-builder/ | `skills/attribution-debugging-utm-hygiene/SKILL.md` — UTM convention + bulk shorten (up to 100K links) |
| Klaviyo abandoned-cart best practices | https://www.klaviyo.com/blog/abandoned-cart-best-practices | `skills/retargeting-customer-list-match/SKILL.md` — paid-side retargeting overlap with Klaviyo flow ownership |
| VWO landing page optimization | https://vwo.com/landing-page-optimization/ | `skills/landing-page-cro-coordination/SKILL.md` — CRO testing framework + message match |
| Google PageSpeed Insights API v5 | https://developers.google.com/speed/docs/insights/v5/about | `skills/landing-page-cro-coordination/SKILL.md` — CWV gate for ad LP (cross-grep marketing-agent `pagespeed-cwv-audit`) |
| Native CraftBot MCPs (facebook-ads-mcp / tiktok-ads-mcp / facebook-mcp-server / tiktok-mcp / reddit-mcp / twitter-mcp / posthog-mcp / mixpanel-mcp / amplitude-mcp / notion-mcp / gmail-mcp / slack-mcp / postgresql-mcp / firecrawl-mcp / brightdata-mcp / deepl-mcp / canva-mcp / figma-mcp / imagegen-mcp / stability-ai-mcp / replicate-mcp / elevenlabs-mcp / playwright-mcp / browserbase-mcp) | agent.yaml | per-platform paid ads, organic context, analytics, knowledge base, comms, warehouse, scraping, translation, design, AI gen, LP audit |

Total: 22 bundled skill packs (Round 2 build) + 25 native MCPs + multiple `cli-anything` REST API paths covering ≥96% of `USE_CASES.md` documented use cases. See `reference/SOTA_USE_CASES.md` for the per-use-case confidence map.

---

## Notes on "authored from synthesis"

Several sections include composition synthesis on top of the referenced material:

- **Title + persona intro (action-verb-first)** — synthesizes 12+ verbs from the methodology's approved verb list, each paired with the SOTA tool from the per-use-case research. Verbs and tool names are not invented; the pairing-into-one-paragraph is the synthesis move.
- **Three load-bearing convictions** — sourced from the per-agent prompt's curated convictions (industry-consensus performance-ads operator wisdom 2024-2026). Triad framing is composed.
- **Core operating rules** — most rules trace to a specific industry doc (Meta CAPI docs, Madgicx fatigue thresholds, Smartly creative framework, etc.). Their selection-into-a-15-rule-list is composed.
- **Mode-specific decisions** — each mode's quality bar is composed from the upstream platform doc plus statistical-significance norms (100 conv/cell, 1-year MMM data minimum, etc.).
- **Antipattern catalog (5 entries)** — distilled from operator-consensus 2024-2026 (mixing offers, scaling broken pixel, mid-quarter attribution switch, n=30 winner declaration, stale Customer Match). The BAD/GOOD code framing is composed; the patterns themselves are operator-canon.
- **Campaign brief / weekly performance report templates** — composed from operator-standard deliverable shapes; no single canonical source.
- **First-conversation PROACTIVE.md self-init** — standard pattern from METHODOLOGY.md footer with paid-ads-specific routine questions (primary platforms, monthly spend, attribution stack).

No domain claims, performance benchmarks, conversion-window numbers, or platform API endpoints were invented. All API endpoint formats, bid strategy names, audience-window defaults, and SKAN schema specifications come from the referenced official docs.

---

## How to update this agent

1. Re-fetch source docs (Meta CAPI, Google Ads MCP, TikTok Marketing API, LinkedIn Marketing API, etc.) and update `reference/SOTA_USE_CASES.md` confidence ratings if endpoints changed
2. Diff against previous versions to see what changed (e.g., new platform MCP launched, attribution window default shifted, MMM tool added)
3. Update corresponding sections of `soul.md` (sparingly — token discipline) and `role.md` (where deep playbook detail lives)
4. Update this `SOURCES.md` if section names or source URLs changed
5. Re-run `verify.py ads-specialist` to confirm structure intact
6. Re-build: `python build.py ads-specialist` produces a fresh `.craftbot`

---

## Refreshing from upstream

When SOTA tools change (e.g., new platform MCP launched, attribution window default shifted, MMM tool added):
1. Update the relevant skill pack(s) in `agents/ads-specialist/skills/<name>/SKILL.md` (Round 2 deliverable)
2. Update the SOTA sources table above
3. Update `reference/SOTA_USE_CASES.md` confidence ratings if applicable
4. Re-run `python verify.py ads-specialist` to confirm structure intact
5. Re-build: `python build.py ads-specialist` produces a fresh `.craftbot`

For the canonical reference repos (Step 2 of methodology) — to be tightened in v2+ when the v1 pass pulls full upstream `agents/` and `skills/` mirrors:
- `wshobson/agents` plugins (paid-ads / performance-marketing) — repull every quarter
- `VoltAgent/awesome-claude-code-subagents` — same cadence
- `msitarzewski/agency-agents` paid/* — same cadence
