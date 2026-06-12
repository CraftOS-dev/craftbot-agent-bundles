# Social Media Manager — Use Cases

**Tier:** **specialized** · **Category:** marketing (social)
**Core job:** Social-platform-native operator — cross-platform publishing, two-way community engagement, social listening, influencer outreach, real-time community management, social commerce, social crisis comms.

> Ships with the SOTA social-operator stack (Buffer MCP cascade, Brand24 listening, Modash + HypeAuditor influencer, Vale per-platform brand voice, Carl-bot/MEE6/Dyno moderation, Reddit / TikTok / IG / LinkedIn / X / Threads / Bluesky / YouTube / WhatsApp / WeChat / LINE / Bilibili native MCPs) — executes end-to-end, not just direct.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it (vs. its parent `marketing-agent` or siblings `video-creator`, `customer-support-agent`).

---

## What this agent is supposed to do

### Community engagement
- Comment + DM triage at scale (across LinkedIn / X / IG / TikTok / Threads / Bluesky / Reddit / YouTube / Discord / Slack)
- SLA-driven reply queue (15 min urgent / 4 hrs question / 24 hrs praise)
- Recurring-pattern detection (complaint → product team; question → FAQ; praise → testimonial DB)
- Comment quality moderation (pin, hide, escalate)

### Cross-platform publishing
- Platform-native content creation (Reels / TikTok / Shorts / X thread / LinkedIn carousel / Pinterest pin / Bluesky / Threads / Stories)
- Buffer cascade with per-channel variants (caption length, emoji density, hashtag count, hook style)
- Scheduling with approval flow for regulated brands
- Multi-language publishing (DeepL + per-language Vale style packs)

### Social listening
- Brand mention monitoring (Brand24 MCP / Talkwalker / Meltwater)
- Sentiment triage (positive / neutral / negative / urgent)
- Threshold-based crisis alerts
- Share-of-voice tracking
- Competitor monitoring

### Influencer marketing
- Discovery (Modash Discovery API — 350M+ profiles, audience match + engagement filters)
- Fraud detection (HypeAuditor AQS gate, ≥ 70 threshold)
- Personalized outreach (Gmail + per-creator brief)
- Campaign tracking (Notion or HubSpot pipeline)
- Performance attribution + ROI reporting

### Hashtag + trend strategy
- Hashtag basket discipline (30-tag basket: 5 trending + 15 niche + 5 branded + 5 community)
- Trending audio adoption within 48-hour window (3-5x algorithmic push)
- Daily 9am trend brief (TikTok Creative Center + Tokchart)
- Reddit / TikTok / hashtag SEO

### Social commerce
- TikTok Shop setup + GMV Max ad budget (mandatory from July 2026)
- Instagram Shop product tagging
- Pinterest Shop catalog sync
- Shopify-hub-first architecture
- Conversion attribution

### Link-in-bio
- Linktree API (REST-managed link reorder + analytics)
- Beacons / Stan Store automation (Playwright fallback when no API)
- Weekly sync from master Notion DB

### Reddit + AMA
- Subreddit health audit before posting
- AMA playbook (pre-game / day-of / post-AMA digest)
- Cross-post coordination
- Native posting with 80/20 community/brand rule

### Discord / Slack moderation
- Bot stack deployment (Carl-bot, MEE6, Dyno + native MCPs)
- YAML rule pack (spam / link policy / toxicity threshold / new-member onboarding)
- Mod-log routing

### Brand voice consistency
- Per-platform Vale style packs (`styles/Brand/LinkedIn.yml`, `styles/Brand/X.yml`, etc.)
- Common-banned list (corporate jargon, AI-slop, sycophancy, em-dash storms)
- Multi-language voice enforcement

### Crisis comms
- Real-time threshold detection via Brand24 webhook
- 3-variant draft engine (apology / clarification / holding statement)
- SLA matrix (acknowledge < 60 min / statement < 4 hrs / detailed < 24 hrs)
- Cascade to owned channels via Buffer
- Legal review hook

### Multi-platform campaign launches
- T-7 teaser cascade
- T-0 coordinated launch (6+ platforms simultaneous)
- T+1 to T+7 amplification (UGC + influencer + paid boost)
- Mid-flight pivots
- Performance + ROI reporting

### UGC reposting
- Discovery via Brand24 + Buffer mention feeds
- Rights-request DM workflow (per-platform templates)
- License-window tracking in Notion DB
- Attribution-baked repost copy

### Account takeovers
- Brief template (voice / safety net / posting schedule)
- Buffer scheduling-with-approval
- Token-revocation script post-takeover

### Customer service triage
- Comment/DM classification (question / complaint / urgent)
- 15-min acknowledgment SLA
- Route to `customer-support-agent` for resolution

### Sentiment + mention triage
- Daily Brand24 export → triage table
- Action assignments (positive → reshare / negative → DM / urgent → crisis flow)

### Team admin coordination
- Buffer approval workflow (collision detection, multi-reviewer)
- Notion DB single source of truth
- Slack notifications on state transitions

### Follower growth (organic)
- Trend first-mover bonus (3-5x within 48 hrs)
- Posting cadence per platform best window
- Collab posts (IG Collab, TikTok Duet/Stitch, X thread reply collabs)
- Cohort analytics (Brand24, native platform analytics)

### Social SEO
- TikTok SEO (caption + on-screen text + alt text keyword front-loading)
- Reddit SEO (title verbatim + first-comment link + early engagement)
- Hashtag SEO (long-tail + branded clustering)

### Format-specific optimization
- Reels 15-90s vertical 9:16
- TikTok 15-180s with trending audio + on-screen text
- Shorts ≤60s
- X thread 5-25 posts with hook in first 7 words
- LinkedIn carousel up to 100 pages
- IG carousel 10 cards
- Pinterest 1000×1500 vertical
- WhatsApp broadcast 256 contacts max per list

### Translation
- Multi-language post variants via DeepL MCP
- Per-language brand voice via separate Vale style pack

---

## Execution status (SOTA — June 2026)

| Use case | SOTA mechanism | Path |
|---|---|---|
| Community engagement at scale (comments + DMs) | Buffer MCP `getEngagements` + Sprout/Agorapulse inbox routing | `community-engagement-comments-dms-at-scale` + `cli-anything` Buffer |
| Cross-platform publishing | Buffer GraphQL + MCP cascade | `platform-native-content-creation` + `cli-anything npx @buffer/mcp-server` |
| Platform-specific publishing | Native platform MCPs | `twitter-mcp` / `insta-business-mcp` / `tiktok-mcp` / `reddit-mcp` / `youtube-mcp` / `bilibili-mcp` / etc. |
| Format-specific (Reels/TikTok/Shorts/X thread/carousel) | Per-platform format specs in role.md + Vale linter | `format-specific-reels-tiktok-shorts-x-thread` |
| Social listening | Brand24 MCP + Talkwalker (enterprise) | `social-listening-brandwatch-mention-talkwalker` |
| Sentiment + mention triage | Brand24 AI sentiment 2026 model | `sentiment-mention-triage` |
| Influencer discovery + outreach | Modash Discovery API (350M+ profiles) | `influencer-outreach-modash-aspire-grin` + `gmail-mcp` |
| Influencer fraud detection | HypeAuditor AQS 70+ gate | `influencer-fraud-detection-hypeauditor` |
| Hashtag strategy | TikTok Creative Center + Brand24 co-occurrence | `hashtag-strategy-trending-niche-branded` |
| Trend monitoring (TikTok sounds + Reels + X) | Tokchart + Creative Center daily cron | `social-trend-monitoring-tiktok-sounds-reels` |
| Social commerce setup | TikTok Shop / IG Graph / Pinterest Shop APIs + Shopify hub | `social-commerce-tiktok-instagram-pinterest-shops` + `shopify-mcp` |
| Link-in-bio management | Linktree REST + Playwright for Beacons / Stan | `link-in-bio-linktree-beacons-stan` + `playwright-mcp` |
| Reddit strategy + AMA | Reddit MCP + subreddit health scoring + AMA playbook | `reddit-strategy-ama-subreddit` + `reddit-mcp` |
| Discord / Slack community moderation | Carl-bot / MEE6 / Dyno YAML rule packs + native MCPs | `discord-slack-community-moderation` + `discord-mcp` + `slack-mcp` |
| Brand voice consistency across platforms | Vale per-platform `styles/Brand/*.yml` rule packs | `brand-voice-consistency-platforms` + `cli-anything` |
| Social SEO (TikTok / Reddit / hashtag) | Caption + on-screen text + alt text keyword strategies | `social-seo-tiktok-reddit-hashtag` |
| Organic follower growth | Trend first-mover + cadence + collab posts | `follower-growth-organic` |
| Social customer service handoff | Triage + 15-min SLA + route to support agent | `social-customer-service-handoff` |
| Social crisis comms | Brand24 webhook + 3-variant draft + cascade | `social-crisis-comms` + Buffer cascade |
| Account takeovers (creator handoff) | Brief + Buffer approval + token revoke | `account-takeovers-creator-handoff` |
| Multi-platform campaign launches | T-7 / T-0 / T+7 cascade + analytics | `multi-platform-campaign-launches` |
| UGC reposting workflow | Brand24 discovery + Notion DB + attribution | `ugc-reposting-policy-workflow` |
| Team admin coordination | Buffer approval + Notion DB + Slack notifications | `team-admin-coordination` + `slack-mcp` + `notion-mcp` |
| Multi-language publishing | DeepL MCP + per-language Vale pack | `deepl-mcp` + `brand-voice-consistency-platforms` |
| Analytics + attribution | PostHog MCP + native platform dashboards | `posthog-mcp` + native MCPs |
| Asset generation | Canva templates + Figma pulls + AI image gen | `canva-mcp` + `figma-mcp` + `imagegen-mcp` |
| WhatsApp Business broadcast | Native MCP + catalog | `whatsapp-mcp` |
| WeChat / Bilibili / LINE (APAC) | Native MCPs | `wechat-mcp` + `bilibili-mcp` + `line-mcp` |
| Competitor scraping fallback | Firecrawl / Brightdata when APIs gated | `firecrawl-mcp` + `brightdata-mcp` |
| Paid amplification when organic ceilings | Meta + TikTok ads MCPs | `facebook-ads-mcp` + `tiktok-ads-mcp` |

### Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Brand24 / Modash / HypeAuditor paid keys | (caveat) | Recipient provides paid API keys; free fallback via Apify scrapers / brightdata-mcp at lower confidence |
| TikTok Shop seller approval | (caveat) | 1-4 week approval cycle; agent operates in "spec + draft" mode in the meantime; GMV Max mandatory from July 2026 |
| At-scale UGC rights tooling (Pixlee / Taggbox / Bazaarvoice) | (caveat) | Paid platforms; manual rights-request workflow via Gmail / DM ships immediately at lower throughput |
| Stan Store / Beacons API gaps | (caveat) | Playwright automation fallback works but is fragile when UI changes; monitor + update periodically |
| LinkedIn organic posting (Community Management API) | (caveat) | Requires LinkedIn Community Management API app approval; LinkedIn Ads API is unblocked |
| TikTok Research API official | (caveat) | Requires TikTok Developer Portal app approval; scraped fallback via Brightdata / Apify works immediately |
| Buffer MCP partner-permission for each connected channel | (caveat) | One-time OAuth per channel; in-app authorization flow |

**Verdict (June 2026): ~95% fulfillment.** Every documented use case has a concrete execution path. The remaining 5% is paid-key gating that the recipient owns + one-time platform app-approval cycles (LinkedIn Community Management, TikTok Shop, TikTok Research) that cannot be skipped. Where official APIs are gated, scraping fallback via `brightdata-mcp` / `firecrawl-mcp` keeps the agent operational at lower confidence + manual review burden.

---

## When to use this agent

- "Publish this announcement across LinkedIn, X, IG, TikTok, Threads, and Bluesky"
- "Reply to all comments and DMs across our channels from the last 24 hours"
- "Find 50 micro-influencers in our niche and screen for fraud"
- "Set up our TikTok Shop and sync the Shopify catalog"
- "Plan a Reddit AMA in r/[subreddit] for next month"
- "Moderate our Discord — set up the rule pack and bots"
- "Build the hashtag baskets for our July campaign"
- "We've got a brand mention spike — is this a crisis?"
- "Coordinate our multi-platform product launch (T-7 to T+7)"
- "Run our UGC reposting workflow with rights tracking"
- "What trending TikTok sounds should we use this week?"
- "Audit our brand voice consistency across last month's posts"

## When NOT to use this agent

- **Long-form video production** (30-min+ videos, color grading, motion graphics) — hand off to `video-creator`.
- **Support escalations** beyond triage (refund, broken product, technical resolution) — hand off to `customer-support-agent` after acknowledging.
- **Broader marketing strategy** (positioning, content pillars, SEO program, email lifecycle) — hand off to `marketing-agent` (parent — general).
- **Email-only campaigns** (lifecycle, deliverability, segmentation) — hand off to `email-strategist` or `marketing-agent`.
- **Deep SEO program** (technical audit, content cluster build, multi-month link-building) — hand off to `seo-specialist` or `marketing-agent`.
- **Long-form written content** (blog posts, white papers, e-books) — hand off to `content-creator` or `marketing-agent`.
- **Earned media / journalist relations / PR** — v1 → hand off to `pr-comms-agent` when built.
- **Paid ads beyond social** (Google Ads search, display, programmatic) — hand off to `marketing-agent`.
- **Brand strategy at the agency-engagement level** (rebrand, naming, positioning research over months) — flag the depth need; this agent can start it, but recommend a brand-strategy specialist for full depth.
