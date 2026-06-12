# Social Media Manager — Sources

Section→source map for `soul.md` and `role.md`. Ships in the bundle but is **not** loaded into the agent's context. For humans verifying provenance and for future updates.

## soul.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Title + persona intro | `reference/SOTA_USE_CASES.md` (every named tool) + parent `marketing-agent/soul.md` shape | Action-verb-first; 12 verbs from the allowed list (publish / respond / monitor / score / search / render / launch / post / moderate / track / trigger / deploy) |
| Purpose | Synthesis of marketing-agent parent + 2026 social-platform-landscape research | |
| Execution stack | `reference/SOTA_USE_CASES.md` summary table | Built from per-use-case SOTA mapping |
| When invoked | Synthesis of mode-specific best practices from web research + Buffer / Brand24 / Modash docs | |
| Core operating rules | Web research: Buffer / Sprout / Brand24 / FTC disclosure guidance / TikTok Shop GMV Max 2026 mandate / hashtag-basket discipline studies | |
| Mode-specific decisions | Platform format spec (role.md) + SOTA mapping (reference) | |
| Quality gates | Synthesis of best-practice SLAs across listening / engagement / influencer / crisis playbooks | |
| Communication style | Mirror of marketing-agent communication-style discipline (Vale-clean, action verbs, numbered claims) | |
| When to push back | FTC disclosure 16 CFR 255.5; platform terms (no follower buying); HypeAuditor AQS threshold; cross-post penalty | |
| When to defer | Sibling agent catalog (`marketing-agent`, `video-creator`, `customer-support-agent`, `email-strategist`, `content-creator`, `seo-specialist`) | |
| PROACTIVE self-init footer | `METHODOLOGY.md` standard footer | Same wording across all agents |

## role.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Capability reference (platforms / formats / tool categories) | 2026 web research aggregated in `reference/SOTA_USE_CASES.md` | |
| Platform format spec | Per-platform official developer docs + Buffer / Hootsuite resource guides (2026) | LinkedIn / X / IG / TikTok / Threads / Bluesky / Reddit / Pinterest / YouTube / WhatsApp |
| Hashtag basket spec | TikTok Creative Center + IG Creator Studio 2026 best-practice docs + Buffer hashtag-strategy guide | |
| Community engagement playbook | Sprout Social inbox routing docs + Agorapulse Inbox Assistant + Buffer engagements API | |
| Influencer outreach playbook | Modash Discovery API docs + HypeAuditor AQS methodology + Aspire / GRIN campaign-CRM patterns | |
| Social listening playbook | Brand24 + Talkwalker + Meltwater 2026 product docs + tool-comparison roundups | |
| Trend monitoring playbook | TikTok Creative Center + Tokchart + Buffer trending-songs weekly roundups | |
| Reddit AMA playbook | Reddit official API docs + r/IAmA mod guidelines + AMA-prep resources | |
| Crisis comms playbook | Eclincher autonomous crisis detection 2026 guide + Emplifi real-time crisis management | |
| Brand voice per platform | Vale linter docs + per-platform voice-style research (LinkedIn formal / X punchy / TikTok casual / Threads conversational) | |
| UGC reposting workflow | ShowCa UGC rights guide 2026 + FTC disclosure 16 CFR 255 + per-platform rights-request conventions | |
| Multi-platform campaign playbook | Buffer best-management-tools 2026 + cross-platform launch patterns | |
| Discord rule pack template | CommunityOne best-Discord-bots guide 2026 + Carl-bot dashboard docs | |
| Slack rule pack template | Slack workspace governance best practices + community-management patterns | |
| Social commerce setup | TikTok Shop API docs + Meta Commerce Manager + Pinterest Shop docs + Shopify integration | |
| SOTA tool reference | `reference/SOTA_USE_CASES.md` + per-tool official docs | One H3 per tool; grep-friendly |

## SOTA tool sources (June 2026)

| Tool | Source URL | Used for |
|---|---|---|
| Buffer Developer API + MCP | https://buffer.com/developers/api | Cross-platform publish, comment/DM engagement, scheduling-with-approval |
| Buffer — best social media APIs 2026 | https://buffer.com/resources/best-social-media-apis/ | Tool landscape; partner API status |
| Buffer — best social media management tools 2026 | https://buffer.com/resources/best-social-media-management-tools/ | Tool comparison: Buffer / Later / Hootsuite / Sprout / Sprinklr / Agorapulse / Publer / SocialPilot |
| Buffer — trending TikTok songs (weekly) | https://buffer.com/resources/trending-songs-tiktok/ | Daily trend brief seed |
| Sprout Social — scheduling tools 2026 | https://sproutsocial.com/insights/social-media-scheduling-tools/ | Inbox routing + customer service handoff workflows |
| Brand24 | https://brand24.com/ | Social listening, sentiment, MCP (Jan 2026 GA) |
| Brandwatch — top social listening tools 2026 | https://www.brandwatch.com/blog/social-listening-tools/ | Listening tier comparison + hashtag clustering |
| Meltwater — top 13 listening tools 2026 | https://www.meltwater.com/en/blog/top-social-listening-tools | Earned-media coverage (TV / radio / podcast) |
| Modash — best influencer platforms 2026 | https://www.modash.io/blog/influencer-marketing-platforms | Influencer platform tier comparison |
| Modash — Discovery API | https://www.modash.io/influencer-marketing-api/discovery | Creator discovery REST API |
| HypeAuditor | https://hypeauditor.com/ | AQS fraud detection + audience-authenticity scoring |
| HypeAuditor — fake-followers detection methodology | https://hypeauditor.com/blog/hypeauditor-fake-followers-detection/ | AQS 70 threshold justification |
| ContentGrip — influencer fraud detection 2026 | https://www.contentgrip.com/influencer-marketing-fraud-detection/ | 81% of marketers encountered fraud last 12 months |
| TikTok Creative Center | https://www.tiktok.com/business/creativecenter | Trending sounds / hashtags / creators |
| TikTok Creative Center — popular hashtags | https://www.tiktok.com/business/creativecenter/inspiration/popular/hashtag | Hashtag trend source |
| TikTok Developer — Shop API | https://developers.tiktok.com/doc/research-api-specs-query-tiktok-shop-info?enter_method=left_navigation | Catalog sync, orders, inventory, GMV Max requirement |
| KeyAPI — TikTok Shop integration guide 2026 | https://www.keyapi.ai/blog/tiktok-shop-api-integration-guide-sellers/ | Setup mechanics + GMV Max budget |
| Lueurexterne — social commerce 2026 | https://blog.lueurexterne.com/en/blog/social-commerce-in-2026-how-to-sell-on-instagram-tiktok-pinterest/ | IG / TikTok / Pinterest commerce setup |
| GPTSocial — trending sounds 2026 | https://www.gpt.social/blog/how-to-find-trending-sounds-tiktok-reels-2026 | 48-hour adoption window justification |
| Vale prose linter | https://vale.sh/ | Brand voice enforcement |
| AtomWriter — brand-voice consistency 2026 | https://www.atomwriter.com/blog/brand-voice-consistency-social-media-linkedin-twitter-tiktok/ | Per-platform voice variance |
| Stan Store vs Linktree (2026) | https://stan.store/blog/stan-store-vs-linktree/ | Link-in-bio platform comparison |
| Talkspresso — Beacons vs Linktree 2026 | https://talkspresso.com/blog/beacons-vs-linktree-2026 | Link-in-bio feature comparison |
| Eclincher — autonomous crisis detection 2026 | https://www.eclincher.com/articles/autonomous-crisis-detection-for-brands-how-ai-monitors-reputation-risk-in-real-time-2026-guide | Crisis SLAs (60 min / 4 hrs / 24 hrs) |
| Emplifi — real-time crisis management | https://emplifi.io/resources/blog/real-time-crisis-management/ | Crisis playbook structure |
| ShowCa — UGC usage rights | https://www.showca.se/post/ugc-usage-rights | Rights-request workflow |
| Flockler — UGC rights management | https://flockler.com/features/ugc-rights-management | At-scale UGC rights tooling |
| CommunityOne — best Discord bots 2026 | https://blog.communityone.io/best-discord-bots/ | Carl-bot / MEE6 / Dyno comparison |
| Skywork — Discord moderation guide | https://skywork.ai/skypage/en/discord-moderation-bots-guide/2033459407355342848 | Discord rule pack template structure |
| SpicyCreator — social media APIs 2026 | https://www.spicycreatortips.com/the-best-social-media-apis-for-developers-in-2026/ | Per-platform API landscape |
| Tokchart | https://tokchart.com/ | Daily TikTok chart + trend deltas |
| OutlierKit — best influencer marketing APIs | https://outlierkit.com/resources/best-influencer-marketing-platform-apis/ | API-tier influencer-platform comparison |
| TheRankMasters — Reddit brand monitoring tools | https://www.therankmasters.com/insights/brand-monitoring/best-reddit-brand-monitoring-tools | Reddit SEO + brand monitoring |
| Parent marketing-agent SOURCES | `agent_bundle/agents/marketing-agent/SOURCES.md` | Inherits Vale brand-voice catch list + Bitly UTM + content quality editor framing |

## Notes on authored-from-synthesis

Sections that aren't directly lifted from a single source — always operational glue, not domain claims:

- **soul.md "When invoked" mode procedures** — synthesis from per-tool docs + per-use-case best practices. Each step traces to a tool's documented capability, but the order-of-operations is the agent's contribution.
- **role.md "SOTA execution playbook" table** — synthesis from `reference/SOTA_USE_CASES.md`; mapping is the agent's contribution.
- **role.md Discord + Slack rule pack YAML templates** — synthesis of Carl-bot docs + Slack admin best practices; no single canonical YAML format for this.
- **role.md Influencer outreach + brief templates** — synthesis from Modash / Aspire / GRIN documented field structures + standard influencer-campaign brief patterns.

## Refreshing from upstream

When SOTA tools change (new platform API GA, hashtag-policy update, crisis-response algorithm change):

1. Update the relevant skill pack(s) in `agents/social-media-manager/skills/<name>/SKILL.md` (Round 2 creates these initially).
2. Update the SOTA sources table above.
3. Update `reference/SOTA_USE_CASES.md` confidence ratings if applicable.
4. Re-run `python verify.py social-media-manager` to confirm structure intact.
5. Re-build: `python build.py social-media-manager` produces a fresh `.craftbot`.

For the canonical reference repos:
- **Buffer Developer API** — re-check every quarter for new platforms / new MCP tools.
- **Brand24 / Talkwalker / Meltwater** — re-check annually for AI-sentiment model updates + new source coverage.
- **TikTok Creative Center + TikTok Shop API** — re-check every two months — TikTok policy + API changes faster than other platforms.
- **HypeAuditor + Modash** — re-check annually for AQS methodology + new platform coverage.
- **Vale linter** — re-check annually; brand-voice catch list is the most-frequently-iterated piece.
