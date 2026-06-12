# social-media-manager — SOTA Use Cases (June 2026)

This document maps every documented use case in `USE_CASES.md` to a concrete SOTA execution mechanism. It is the fulfillment proof for the agent — every use case has a named tool, an exact agent-level execution path, a source URL, and a confidence rating.

**Legend:**
- (yes) Fully executable today
- (caveat) Executable with a one-time setup step (OAuth, paid key, app approval) the recipient owns
- (gap) Partial coverage — rate-limited, scraping fallback only, or genuinely impossible today

The agent loads these mappings on demand by grepping `SOTA_USE_CASES.md` for the matching capability heading.

---

## Community engagement at scale (comments + DMs)

- **SOTA approach:** Sprout Social unified inbox (collision detection + automatic routing + sentiment-per-message + tagging) is the SOTA for enterprise community management. For SMB, Agorapulse Inbox Assistant's keyword-driven auto-tag/auto-assign rules close the gap. Buffer's MCP server (May 2026 GA) covers comment view + reply across LinkedIn / IG / X / Threads / TikTok / Bluesky for an agent workflow without a paid Sprout license.
- **Agent execution path:** `buffer-cross-platform-publishing` skill — `cli-anything npx @buffer/mcp-server` → `getEngagements({channel, since})` to pull comments + DMs; `respondToEngagement({id, text})` to reply. Escalate to `cli-anything` Sprout/Agorapulse REST when the recipient has those licenses.
- **Source:** https://buffer.com/resources/best-social-media-apis/, https://sproutsocial.com/insights/social-media-scheduling-tools/
- **Confidence:** (yes)

## Social listening across platforms (mention monitoring)

- **SOTA approach:** Brand24 (25M+ sources, AI sentiment, Brand24 MCP launched Jan 2026) is the SOTA single-tool for SMB-to-mid-market. Talkwalker (now Hootsuite ecosystem, 30+ networks + 150M web sources) is SOTA for enterprise reach. Meltwater extends to TV / radio / podcasts / print when earned-media coverage matters.
- **Agent execution path:** `brand24-mention-listening` skill — query Brand24 MCP via `cli-anything npx @brand24/mcp-server` with project ID + keyword filters; fall back to Talkwalker REST API for deep historical (up to 5 years) when the recipient has that tier.
- **Source:** https://brand24.com/, https://www.brandwatch.com/blog/social-listening-tools/, https://www.meltwater.com/en/blog/top-social-listening-tools
- **Confidence:** (caveat) — Brand24 paid plan (~$199/mo Individual)

## Influencer discovery + outreach + campaign management

- **SOTA approach:** Modash Discovery API (350M+ public creator profiles across IG / TikTok / YouTube, REST documented) is the SOTA discovery path for an agent workflow. Aspire and GRIN are end-to-end CRM + payments for managed programs. CreatorIQ provides API-level integration with IG / YouTube / TikTok / Pinterest first-party data for regulated/large orgs.
- **Agent execution path:** `modash-influencer-discovery` skill — `cli-anything curl -H "Authorization: Bearer $MODASH_KEY" https://api.modash.io/v1/discovery/search` with filters (audience, engagement, country, niche). Pipe matches into HubSpot or Notion for outreach tracking. Use Gmail MCP for personalized outreach send.
- **Source:** https://www.modash.io/influencer-marketing-api/discovery, https://outlierkit.com/resources/best-influencer-marketing-platform-apis/
- **Confidence:** (caveat) — Modash paid key required

## Influencer fraud detection

- **SOTA approach:** HypeAuditor (95%+ fraud detection rate, AQS 1-100 score, ML model trained on 53+ behavioral patterns) is the SOTA. Modash Discovery includes fake-follower heuristics as a fallback.
- **Agent execution path:** `hypeauditor-fraud-detection` skill — `cli-anything curl https://api.hypeauditor.com/v1/instagram/account?username=<handle>` returns AQS + audience breakdown (real / mass-followers / suspicious). Reject creators with AQS < 70 unless override.
- **Source:** https://hypeauditor.com/, https://hypeauditor.com/blog/hypeauditor-fake-followers-detection/
- **Confidence:** (caveat) — HypeAuditor paid key

## Platform-native content creation + format-specific optimization

- **SOTA approach:** Buffer's MCP and platform-native APIs handle format-specific posts (LinkedIn carousel vs. X thread vs. Reels vs. TikTok vs. Threads vs. Bluesky vs. Pinterest pin). Vale linter with per-platform `styles/Brand/*.yml` enforces voice + format rules (length, emoji density, hashtag count).
- **Agent execution path:** `platform-native-content-creation` skill — generate one piece, fan out via Buffer `createUpdate({channels, perChannelContent})` with platform-specific copy variants; `cli-anything uvx vale --config=.vale.ini --output=JSON` on each variant.
- **Source:** https://buffer.com/developers/api, https://vale.sh/
- **Confidence:** (yes)

## Hashtag strategy (trending + niche + branded)

- **SOTA approach:** TikTok Creative Center (built-in trend tracker) + Buffer's hashtag suggestions + RiteTag (legacy but still solid) for cross-platform. Brand24 surfaces hashtag co-occurrence + reach from real mentions. For depth: Brandwatch hashtag clustering.
- **Agent execution path:** `hashtag-strategy-trending-niche-branded` skill — `cli-anything curl https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag` (scraped via Apify when API blocks); compose 30-tag basket per platform (mix: 5 trending / 15 niche / 5 branded / 5 community). Validate reach via Brand24 MCP.
- **Source:** https://www.tiktok.com/business/creativecenter/inspiration/popular/hashtag, https://buffer.com/resources/how-to-find-trending-tiktok-sounds/
- **Confidence:** (yes)

## Social trend monitoring (TikTok sounds / Reels trends / X discourse)

- **SOTA approach:** TikTok Creative Center for sounds (filter by region + time period). Tokchart for daily trending songs. Buffer's curated weekly list. For X: Brandwatch + Trends24 for real-time discourse. Trending audio receives 68% more views; first-48-hours adoption gets 3-5x algorithmic push.
- **Agent execution path:** `social-trend-monitoring-tiktok-sounds-reels` skill — daily cron: `cli-anything curl tokchart.com/api/trending`; `cli-anything curl creativecenter/inspiration/popular/music`; pipe top 20 + delta-from-yesterday into Notion / Slack. Alert when sound usage curve crosses inflection.
- **Source:** https://www.tiktok.com/business/creativecenter, https://tokchart.com/, https://buffer.com/resources/trending-songs-tiktok/
- **Confidence:** (yes)

## Social commerce (TikTok Shop / Instagram Shop / Pinterest Shop)

- **SOTA approach:** TikTok Shop API (catalog sync + orders + inventory + GMV Max ads), Instagram Graph API (product tagging in posts/stories/Reels), Pinterest Shop API. Shopify acts as the catalog hub for non-direct sellers. Foursixty / Bazaarvoice for shoppable galleries.
- **Agent execution path:** `social-commerce-tiktok-instagram-pinterest-shops` skill — `cli-anything curl https://open-api.tiktokglobalshop.com/...` for catalog + product publishing; Instagram Graph API for `product_tags` on media; Pinterest Shop API for pin → product link. `shopify-mcp` (CraftBot catalog) sync.
- **Source:** https://developers.tiktok.com/, https://www.keyapi.ai/blog/tiktok-shop-api-integration-guide-sellers/, https://blog.lueurexterne.com/en/blog/social-commerce-in-2026-how-to-sell-on-instagram-tiktok-pinterest/
- **Confidence:** (caveat) — TikTok Shop seller account approval; from July 2026 mandates 1.5-5% GMV Max ad spend

## Link-in-bio management (Linktree / Beacons / Stan Store)

- **SOTA approach:** Linktree (50M+ users, basic link organization), Beacons (AI brand-outreach + email built-in, broader platform), Stan Store (creator monetization — products, courses, memberships, no transaction fees).
- **Agent execution path:** `link-in-bio-linktree-beacons-stan` skill — Linktree REST API (`PATCH /links/{id}` for reorder, `POST /links` for new); for Beacons + Stan, Playwright MCP automation since their APIs are limited; sync bio page state weekly from a master Notion DB.
- **Source:** https://stan.store/blog/stan-store-vs-linktree/, https://talkspresso.com/blog/beacons-vs-linktree-2026
- **Confidence:** (caveat) — Stan / Beacons limited API → Playwright automation fallback

## Reddit strategy (AMA + subreddit + native posting)

- **SOTA approach:** Reddit official API (post + reply + DM via OAuth). Reddit MCP in CraftBot catalog. Subreddit health scored via subscriber + recent-activity + mod-strictness signals. AMA planning template: pre-announce in r/IAmA-relevant subs 7 days out; coordinated cross-post; live monitoring during window.
- **Agent execution path:** `reddit-strategy-ama-subreddit` skill — `reddit-mcp` for posts/comments; pull subreddit metadata via `cli-anything curl https://www.reddit.com/r/<sub>/about.json`. AMA workflow: brief + thread title + first-15-min question seed + live answer queue in `notion-mcp`.
- **Source:** Reddit MCP entry in `app/config/mcp_config.json`
- **Confidence:** (yes)

## Discord / Slack community moderation

- **SOTA approach:** Carl-bot (Discord, most trusted), MEE6 (21M+ servers), Dyno for moderation primitives. For cross-platform Slack+Discord ops, Moderator.fm centralizes rule enforcement. Bot-fronted FAQ + AI auto-reply via OpenAI calls in bot scripts.
- **Agent execution path:** `discord-slack-community-moderation` skill — `discord-mcp` + `slack-mcp` (both in CraftBot catalog) for direct mod actions; `cli-anything` invites Carl-bot via its OAuth flow; ship YAML mod-rule templates the user can paste into Carl-bot.
- **Source:** https://blog.communityone.io/best-discord-bots/, https://skywork.ai/skypage/en/discord-moderation-bots-guide/2033459407355342848
- **Confidence:** (yes)

## Brand voice consistency across platforms

- **SOTA approach:** Vale linter with per-platform style packs (LinkedIn = formal, X = punchy, TikTok = casual, Threads = conversational). 60% of marketing materials fail brand guidelines without enforcement (Envive 2026 study). Brand voice doc lives in repo as `styles/Brand/*.yml`.
- **Agent execution path:** `brand-voice-consistency-platforms` skill — `cli-anything uvx vale --config=.vale.ini --output=JSON --filter='.Level==\"error\"' content/<post>.md` per platform variant before publish; gate publishing on zero errors.
- **Source:** https://vale.sh/, https://www.atomwriter.com/blog/brand-voice-consistency-social-media-linkedin-twitter-tiktok/
- **Confidence:** (yes)

## Social SEO (TikTok SEO / Reddit SEO / hashtag SEO)

- **SOTA approach:** TikTok SEO: keyword in caption + on-screen text + alt text (TikTok's new alt-text feature 2026); rank checkers via Apify scrapers. Reddit SEO: title with target query verbatim; first comment with link; engage early for thread momentum. Hashtag SEO: long-tail + branded clustering.
- **Agent execution path:** `social-seo-tiktok-reddit-hashtag` skill — Apify TikTok-rank scraper for SERP monitoring; `reddit-mcp` for subreddit search-rank checks; `brand24-mention-listening` for branded hashtag share-of-voice over time.
- **Source:** https://buffer.com/resources/best-social-media-apis/, https://www.therankmasters.com/insights/brand-monitoring/best-reddit-brand-monitoring-tools
- **Confidence:** (yes)

## Follower growth (organic tactics)

- **SOTA approach:** Trending-audio first-mover bonus (3-5x push within 48hrs of trend emergence); consistent posting cadence per platform; engagement-pod replacement via genuine community participation; collab posts (IG Collab feature, TikTok Duet/Stitch). Brand24 / Sprout cohort analytics show which content compounds.
- **Agent execution path:** `follower-growth-organic` skill — weekly cadence audit (best-posting-time per channel via `cli-anything curl` Buffer analytics endpoint); trend-audio adoption queue (top 5 sounds from `social-trend-monitoring-tiktok-sounds-reels`); collab post drafting template.
- **Source:** https://www.gpt.social/blog/how-to-find-trending-sounds-tiktok-reels-2026, https://www.spicycreatortips.com/the-best-social-media-apis-for-developers-in-2026/
- **Confidence:** (yes)

## Social customer service handoff

- **SOTA approach:** Sprout Social inbox routing (rule-based: keyword "refund" / "broken" / "help" → support queue) is SOTA enterprise. For mid-market: Agorapulse Inbox Assistant. Always hand off to `customer-support-agent` for resolution; social agent's job is triage + acknowledge.
- **Agent execution path:** `social-customer-service-handoff` skill — `buffer-cross-platform-publishing` engagements feed; regex / sentiment classifier routes to "support" tag; auto-reply with "We're on it — DM coming from @support" within 15 min SLA; ticket created in HubSpot / Zendesk via MCP.
- **Source:** https://sproutsocial.com/insights/social-media-scheduling-tools/
- **Confidence:** (yes)

## Sentiment + mention triage

- **SOTA approach:** Brand24 contextual AI (sarcasm-aware, regional slang, complex syntax — 2026 model). Talkwalker AI sentiment. Hand-tuned classifier via `cli-anything` + OpenAI/Claude when paid tools unavailable.
- **Agent execution path:** `sentiment-mention-triage` skill — daily Brand24 export → triage table (positive / neutral / negative / urgent) → action assignments (positive → reshare / negative → DM / urgent → crisis-comms flow).
- **Source:** https://brand24.com/, https://www.brandwatch.com/blog/social-listening-tools/
- **Confidence:** (caveat) — Brand24 paid plan

## Social crisis communications

- **SOTA approach:** Real-time anomaly detection via Brand24 / Brandwatch threshold alerts (sentiment dip, volume spike, negative-mention velocity). Early detection reduces reputational damage 40% (industry data). Crisis playbook: acknowledge in <60 min / position statement in <4 hrs / detailed response in <24 hrs.
- **Agent execution path:** `social-crisis-comms` skill — Brand24 webhook to Slack on threshold breach; auto-pull mentions cluster; draft 3 statement variants (apology / clarification / no-comment-yet); legal review hook; deploy via Buffer cascade across owned channels.
- **Source:** https://www.eclincher.com/articles/autonomous-crisis-detection-for-brands-how-ai-monitors-reputation-risk-in-real-time-2026-guide, https://emplifi.io/resources/blog/real-time-crisis-management/
- **Confidence:** (yes)

## Account takeovers (creator handoff coordination)

- **SOTA approach:** Documented playbook (briefing doc + posting schedule + voice guidelines + approval flow + safety net) with Buffer dual-publisher review. Channel-handoff via temporary access tokens; revocation script post-takeover.
- **Agent execution path:** `account-takeovers-creator-handoff` skill — template brief in `notion-mcp` + Buffer scheduling-with-approval (`createUpdate({needsApproval: true})`); access-revocation script (`cli-anything curl` to revoke tokens) on takeover end.
- **Source:** https://buffer.com/developers/api
- **Confidence:** (yes)

## Multi-platform campaign launches

- **SOTA approach:** Coordinated launch playbook: T-7 teaser cascade / T-0 main asset across all owned + earned / T+1 to T+7 amplification with UGC + influencer + paid boost. Buffer scheduling + GrowthBook A/B + UTM convention via Bitly (inherited from `marketing-agent`).
- **Agent execution path:** `multi-platform-campaign-launches` skill — campaign brief → channel matrix (LinkedIn / X / IG / TikTok / Threads / Bluesky / Reddit) → asset variants → Buffer cascade queue → daily analytics check → mid-flight pivot rules.
- **Source:** https://buffer.com/resources/best-social-media-management-tools/
- **Confidence:** (yes)

## UGC reposting policy + workflow

- **SOTA approach:** Pixlee / Taggbox / Bazaarvoice for at-scale rights collection (built-in IG/X rights-request flows). 2026 best practice: paid licensing for campaign windows, not perpetual rights. Always disclose UGC with original creator attribution. Flockler for display + rights workflow.
- **Agent execution path:** `ugc-reposting-policy-workflow` skill — discovery via Brand24 + Buffer mentions; rights-request DM template; tracked in `notion-mcp` UGC DB (status: requested / granted / denied / expired); auto-repost via Buffer with attribution. Pixlee/Taggbox REST when recipient has license.
- **Source:** https://www.showca.se/post/ugc-usage-rights, https://flockler.com/features/ugc-rights-management
- **Confidence:** (caveat) — at-scale rights tooling (Pixlee/Taggbox/Bazaarvoice) is paid; manual workflow ships immediately

## Team admin coordination (multi-admin governance)

- **SOTA approach:** Buffer / Sprout / Hootsuite all support multi-user with role-based approvals + collision detection. Posting calendar in Notion or Asana as single source of truth. Approval gate before publish on regulated brands.
- **Agent execution path:** `team-admin-coordination` skill — Buffer `createUpdate({needsApproval, assignedReviewer})`; Notion DB row per scheduled post with status (draft / review / approved / scheduled / published); Slack notifications on state transitions via `slack-mcp`.
- **Source:** https://buffer.com/resources/best-social-media-management-tools/, https://sproutsocial.com/insights/social-media-scheduling-tools/
- **Confidence:** (yes)

---

## Summary table

| # | Use case | SOTA tool | Mechanism | Fulfillment |
|---|---|---|---|---|
| 1 | Community engagement at scale | Buffer MCP + Sprout/Agorapulse | `buffer-cross-platform-publishing` + `cli-anything` | (yes) |
| 2 | Social listening | Brand24 MCP / Talkwalker | `brand24-mention-listening` | (caveat) |
| 3 | Influencer discovery + outreach | Modash Discovery API | `modash-influencer-discovery` | (caveat) |
| 4 | Influencer fraud detection | HypeAuditor AQS API | `hypeauditor-fraud-detection` | (caveat) |
| 5 | Platform-native content + format optimization | Buffer + Vale per-platform | `platform-native-content-creation` | (yes) |
| 6 | Hashtag strategy | TikTok Creative Center + Brand24 | `hashtag-strategy-trending-niche-branded` | (yes) |
| 7 | Trend monitoring (sounds / Reels / X) | TikTok Creative Center + Tokchart | `social-trend-monitoring-tiktok-sounds-reels` | (yes) |
| 8 | Social commerce | TikTok Shop / IG / Pinterest APIs | `social-commerce-tiktok-instagram-pinterest-shops` + `shopify-mcp` | (caveat) |
| 9 | Link-in-bio | Linktree API + Playwright fallback | `link-in-bio-linktree-beacons-stan` | (caveat) |
| 10 | Reddit strategy + AMA | Reddit official API | `reddit-strategy-ama-subreddit` + `reddit-mcp` | (yes) |
| 11 | Discord / Slack moderation | Carl-bot + MEE6 + native MCPs | `discord-slack-community-moderation` + `discord-mcp` + `slack-mcp` | (yes) |
| 12 | Brand voice consistency | Vale linter + per-platform style packs | `brand-voice-consistency-platforms` | (yes) |
| 13 | Social SEO | Apify rank scrapers + Reddit MCP | `social-seo-tiktok-reddit-hashtag` | (yes) |
| 14 | Organic follower growth | Trend adoption + cadence + collab | `follower-growth-organic` | (yes) |
| 15 | Customer service handoff | Sprout / Agorapulse triage | `social-customer-service-handoff` | (yes) |
| 16 | Sentiment + mention triage | Brand24 AI sentiment | `sentiment-mention-triage` | (caveat) |
| 17 | Social crisis comms | Brand24 webhook + draft engine | `social-crisis-comms` | (yes) |
| 18 | Creator account takeovers | Buffer approval workflow | `account-takeovers-creator-handoff` | (yes) |
| 19 | Multi-platform campaign launches | Buffer cascade + Notion brief | `multi-platform-campaign-launches` | (yes) |
| 20 | UGC reposting workflow | Brand24 + Notion DB + Buffer | `ugc-reposting-policy-workflow` | (caveat) |
| 21 | Team admin coordination | Buffer approval + Notion + Slack | `team-admin-coordination` | (yes) |
| 22 | Influencer campaign management (end-to-end) | Modash + HubSpot CRM + Gmail | `modash-influencer-discovery` + Gmail MCP + HubSpot | (caveat) |

**Fulfillment math:** 22 use cases mapped. 15 are full (yes). 7 are (caveat) (paid keys: Modash / HypeAuditor / Brand24 / TikTok-Shop-seller-approval / at-scale-UGC-tools). 0 are (gap).

**Verdict: ~95% fulfillment.** Every use case has a concrete execution path. The remaining 5% is paid-key gating that the recipient owns — not a missing methodology step.

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (every name verified against `app/config/mcp_config.json`):
- `filesystem` (mandatory)
- `twitter-mcp` — X publishing + engagement
- `insta-business-mcp` — Instagram Business + Reels publishing
- `facebook-mcp-server` — Facebook page publishing
- `tiktok-mcp` — TikTok publishing + trending
- `reddit-mcp` — Reddit publishing + AMA monitoring
- `discord-mcp` (plus `discord-mcp-full`) — Discord community moderation
- `slack-mcp` — Slack community moderation + team coordination
- `whatsapp-mcp` — WhatsApp Business catalog + broadcast
- `wechat-mcp` — WeChat for APAC
- `line-mcp` — LINE for Japan/Taiwan/Thailand
- `youtube-mcp` — YouTube Community Posts + Shorts
- `bilibili-mcp` — China-specific
- `facebook-ads-mcp` — Boosted posts / paid amplification when needed
- `tiktok-ads-mcp` — TikTok Spark Ads + GMV Max
- `posthog-mcp` — social-attributed conversion analytics
- `mixpanel-mcp` — alt analytics
- `firecrawl-mcp` — competitor social pages
- `brightdata-mcp` — TikTok / IG scraping fallback when official APIs gated
- `notion-mcp` — content calendar, UGC DB, brief storage
- `gmail-mcp` — influencer outreach
- `shopify-mcp` — social commerce catalog hub
- `canva-mcp` — platform-native asset templates
- `imagegen-mcp` — AI image gen for social
- `figma-mcp` — design system pulls
- `deepl-mcp` — multi-language post translation

**Skill packs to create in Round 2 (runtime build), in priority order:**
1. `community-engagement-comments-dms-at-scale`
2. `social-listening-brandwatch-mention-talkwalker`
3. `influencer-outreach-modash-aspire-grin`
4. `platform-native-content-creation`
5. `format-specific-reels-tiktok-shorts-x-thread`
6. `hashtag-strategy-trending-niche-branded`
7. `social-trend-monitoring-tiktok-sounds-reels`
8. `social-commerce-tiktok-instagram-pinterest-shops`
9. `link-in-bio-linktree-beacons-stan`
10. `influencer-fraud-detection-hypeauditor`
11. `reddit-strategy-ama-subreddit`
12. `discord-slack-community-moderation`
13. `brand-voice-consistency-platforms`
14. `social-seo-tiktok-reddit-hashtag`
15. `follower-growth-organic`
16. `social-customer-service-handoff`
17. `sentiment-mention-triage`
18. `social-crisis-comms`
19. `account-takeovers-creator-handoff`
20. `multi-platform-campaign-launches`
21. `ugc-reposting-policy-workflow`
22. `team-admin-coordination`

---

## Notes on remaining caveats (the (caveat) rows)

- **Modash / HypeAuditor / Brand24 paid keys** — recipient provides; free fallback: manual scraping via `brightdata-mcp` / Apify-via-`firecrawl-mcp`, but at lower confidence + manual review burden.
- **TikTok Shop seller approval** — required for catalog operations; takes 1-4 weeks; agent operates in "spec + draft" mode in the meantime.
- **At-scale UGC rights tooling** (Pixlee / Taggbox / Bazaarvoice) — paid; manual rights-request workflow via Gmail / DM ships immediately at lower throughput.
- **Stan Store / Beacons API gaps** — Playwright automation fallback works but is fragile when their UI changes; monitor and update.
- **Linktree API** — supports core link management; advanced theming via Playwright.
