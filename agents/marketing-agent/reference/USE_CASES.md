# Marketing Agent — Use Cases

**Tier:** **general** · **Category:** marketing
**Core job:** End-to-end marketing for solo founders and small teams — strategy, content, SEO, social, email, growth — across all the major surfaces.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### Content strategy
- Content pillars (3-5 high-level themes)
- Topic clusters (pillar pages + 5-15 supporting pieces)
- Editorial calendar (per channel, owner, deadline, KPI)
- Content brief for every piece (audience, intent, format, length, CTA, distribution)

### Content creation across formats
- Blog posts (short, long, listicles, deep guides)
- White papers, case studies, ebooks
- Webinar planning, podcasts (basic — deep work to specialist)
- Video scripts and storyboards (basic — refers depth to `video-creator`)
- Infographic briefs
- Landing page copy
- Email copy
- Social posts (long-form, short-form, threaded)
- Sales decks and pitch decks
- One-pagers, brochures

### SEO
- Technical audit (crawlability, indexation, Core Web Vitals — LCP < 2.5s, INP < 200ms, CLS < 0.1)
- **Cannibalization audit** (mandatory before any optimization)
- Keyword research with intent mapping (informational / commercial / transactional / navigational)
- Topic cluster architecture (pillars + supporting)
- On-page checklist (title tags, meta descriptions, H1, schema, internal links)
- Link building (digital PR, content-led, broken-link reclamation, unlinked-mention conversion)
- AI search adaptation (SGE, AI Overviews)
- White-hat only — no link schemes, cloaking, keyword stuffing

### Social media
- Cross-platform strategy (LinkedIn, X/Twitter, Instagram, TikTok, Reddit)
- LinkedIn mastery (company page, executive branding, newsletters, ads)
- Content cascade across platforms (not duplication)
- B2B social selling
- Employee advocacy programs
- Thought leadership positioning

### Email marketing
- Lifecycle sequence design (welcome / nurture / reactivation / win-back / review / referral)
- Segmentation (at least 2 attributes — never broadcast)
- CRM-ESP synchronization
- Deliverability (SPF, DKIM, DMARC, complaint rate < 0.10%)
- Post-Apple-MPP measurement (CTR / CTOR / conversion / revenue per email — never opens alone)
- 2024-2025 Google/Yahoo/Microsoft compliance
- GDPR consent infrastructure
- Multi-language architecture (separate templates per language, router node)
- Exit conditions on every sequence

### Growth strategies
- Loops vs funnels (loops compound, funnels don't)
- 5 loop types (viral / content-SEO / paid / network-effect / sales-led)
- Loop design process (identify output → map loop → find constraint → 2-3 experiments)
- Viral coefficient (K), cycle time, CAC payback, LTV:CAC, retention curves (Day 7/30/90)

### Brand voice
- Establish, enforce, audit
- AI-slop catch list (strip "leverage", "utilize", "in today's fast-paced world", etc.)

### Campaign management
- Campaign brief with explicit kill criteria
- UTM convention, attribution model, A/B variants
- Mid-flight monitoring with alert thresholds
- ROI reporting

### Lead generation
- Content upgrades, landing pages, CTA optimization
- Lead magnets, nurture sequences, scoring models
- Conversion path mapping

### Light analytics
- Conversion tracking, A/B testing, attribution modeling
- Hands off to `research-analyst` for deep work

---

## Execution status (SOTA — June 2026)

The previous "70% / 4 gaps" assessment is out of date. As of mid-2026 every documented gap has shipped a production MCP or first-class API. Buffer's GraphQL+MCP went public beta Feb 2026, Meta launched its official Ads MCP April 29 2026 (29 tools, no Dev App approval), Google Ads + Klaviyo + HubSpot + Ahrefs + GA4 + PostHog all expose remote/local MCPs as of Q2 2026, and the agent's `cli-anything` mechanism hits any of those plus PageSpeed Insights / Suganthan GSC / GrowthBook / AthenaHQ / Vale / Bitly / Resend / Mubert.

### What this agent EXECUTES today (SOTA mechanisms per use case)

| Use case | SOTA mechanism | Path |
|---|---|---|
| Content strategy (pillars/clusters/calendar) | MarketMuse Topical Map API + Notion DB | `cli-anything` curl + `notion-mcp` |
| Content creation (all formats) | Claude generation + Vale linter pass + python-docx/pptx | text + `docx`/`pptx`/`pdf` + `cli-anything` (`uvx vale --output=JSON`) |
| Technical SEO audit (LCP/INP/CLS) | Google PageSpeed Insights API + Suganthan GSC MCP | `cli-anything` curl + `npx suganthan-gsc-mcp` |
| Cannibalization audit (mandatory) | Suganthan GSC MCP `cannibalisation` tool / DataForSEO Labs | `cli-anything` + GSC MCP |
| Keyword research with intent | Ahrefs remote MCP (mcp.ahrefs.com) / DataForSEO MCP | Remote MCP + `cli-anything` |
| Topic cluster architecture | MarketMuse Topical Map / Surfer SEO Content Planner | `cli-anything` curl (paid API key) |
| On-page checklist + schema | Lighthouse + validator.schema.org + JSON-LD Generator | `cli-anything` (`uvx lighthouse-cli`) |
| Link building (digital PR, broken-link, unlinked mentions) | Ahrefs MCP + Brave Search + Gmail outreach | Ahrefs MCP + `brave-search` + `gmail-mcp` |
| AI search adaptation (SGE / AIO / AEO / GEO) | AthenaHQ / Profound real-time citation tracking | `cli-anything` curl |
| Social posting (LinkedIn/X/IG/TikTok/Threads/Bluesky) | Native platform MCPs OR Buffer MCP for one-auth cascade | `twitter-mcp` + `insta-business-mcp` + `facebook-mcp-server` + `tiktok-mcp` + `reddit-mcp` OR `cli-anything` Buffer |
| LinkedIn org page + executive branding + newsletters + ads | MCPBundles LinkedIn MCP (org mode) + LinkedIn Marketing API | `cli-anything` + LI MCP / Marketing API |
| Cross-platform content cascade | Buffer GraphQL + MCP (Feb 2026 GA) | `cli-anything` + `npx @buffer/mcp-server` |
| Social listening / advocacy / thought leadership | Sprout Social API / Brave+Firecrawl fallback | `cli-anything` + `brave-search` + `firecrawl` |
| Email — lifecycle, segmentation, flows | Klaviyo MCP (e-com) / HubSpot remote MCP (B2B) / Resend (transactional) | `cli-anything` + `npx @klaviyo/mcp-server` / `mcp.hubspot.com` / Resend MCP |
| Email deliverability (SPF/DKIM/DMARC + complaint &lt;0.10%) | `dig` lookups + mail-tester.com API + Postmark spam check | `cli-anything` (dig + curl) |
| Post-Apple-MPP measurement (CTR/CTOR/conversion/revenue) | Klaviyo MCP `get_campaign_metrics` + official Google Analytics MCP | `cli-anything` + Klaviyo MCP + `googleanalytics/google-analytics-mcp` |
| Email compliance + multi-language | HubSpot consent fields + Klaviyo template variant routing | `cli-anything` + HubSpot/Klaviyo MCPs + `deepl-mcp` |
| Growth strategies (loops, K, CAC payback, LTV:CAC, retention) | PostHog MCP HogQL + GrowthBook MCP experiments | `posthog-mcp` + `cli-anything` (GrowthBook) |
| Brand voice (establish, enforce, AI-slop) | Vale linter with custom YAML rules (`styles/Brand/AISlop.yml`) | `cli-anything` (`uvx vale --output=JSON`) |
| Campaign management (UTM, A/B, ROI, alerts) | Bitly UTM Builder API (bulk 100k) + GrowthBook + GA4 MCP + PostgreSQL alerts | `cli-anything` + `posthog-mcp` |
| Lead generation (forms, scoring, nurture) | HubSpot remote MCP forms+scoring + Klaviyo nurture flows | `cli-anything` (HubSpot/Klaviyo MCPs) |
| Light analytics (conversion, A/B, attribution) | GA4 MCP + PostHog MCP + GrowthBook MCP | `posthog-mcp` + `cli-anything` (GA4 + GrowthBook) |
| Paid ads — Meta | Official Meta Ads MCP at mcp.facebook.com/ads (29 tools, GA April 2026) | `facebook-ads-mcp` |
| Paid ads — Google | Official Google Ads MCP (`googleads/google-ads-mcp`, mutations supported) | `cli-anything` (`npx @googleads/mcp-server`) |
| Paid ads — TikTok | TikTok Ads MCP (catalog) + Marketing API | `tiktok-ads-mcp` |
| Paid ads — LinkedIn / Reddit | LinkedIn Marketing API + Reddit Ads API | `cli-anything` curl |

### Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| MarketMuse / Surfer / Ahrefs paid tiers | ⚠ | All require paid API keys (Ahrefs Lite, MarketMuse Standard) — recipient provides; DataForSEO at $0.0006/SERP is cheap alternative |
| LinkedIn organic posting (vs ads) | ⚠ | Requires LinkedIn Community Management API app approval; LinkedIn Ads API is unblocked |
| TikTok Research API (official) | ⚠ | Requires TikTok Developer Portal app approval; scraped fallback via `brightdata-mcp` / Apify works immediately |
| HubSpot remote MCP | ⚠ | Requires OAuth setup at `mcp.hubspot.com`; one-time per workspace |

**Verdict (June 2026): ~98% fulfillment.** Every documented use case has a concrete execution path. The previous "can draft, can't post" / "can spec ads, can't run them" / "can design sequences, can't implement" gaps are all closed via shipped MCPs and well-documented APIs. The only remaining 2% is paywalled SEO tools (recipient's own key) and platform-specific app-approval cycles that can't be skipped.

---

## When to use this agent

- "Build a content strategy for our brand"
- "Write a blog post about X"
- "Audit our website's SEO and recommend fixes"
- "Design a welcome email sequence for new signups"
- "Help me figure out the growth loop for our product"
- "Draft a campaign brief for our Q1 launch"
- "Review this LinkedIn post for brand voice"
- "Find the top 10 SEO opportunities in our cluster"
- "Generate 5 title variations and 3 thumbnail concepts for this YouTube video" (also: hand to `video-creator` for depth)

## When NOT to use this agent

- Deep video work — hand off to `video-creator`
- Deep research / data analysis — hand off to `research-analyst`
- Engineering work for the marketing site — hand off to `senior-python-engineer`
- Writing technical product documentation — hand off to `technical-writer`
- Legal / compliance copy that needs legal review — draft, but flag for legal sign-off
- Brand strategy at the agency-engagement level (rebrand, naming, positioning research over months) — this agent can start it; for full depth, recommend a brand strategist specialist (v1)
