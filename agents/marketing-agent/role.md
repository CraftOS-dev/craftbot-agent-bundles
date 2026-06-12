# Marketing Agent — deep reference

This appends to `AGENT.md`. **Not** in the agent's default context. Grep when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "Content strategy framework", "SEO playbook", "Email lifecycle playbook", "Social media platform playbook", "Growth loop playbook", "Campaign management framework", "Success metrics", "AI-slop catch list", "Multi-language email architecture", "Deliverability landscape", "Sequence design spec template", "Cannibalization audit template", "Keyword strategy template", "On-page SEO checklist", "Technical SEO audit template", "Editorial calendar template".

For provenance, see `SOURCES.md`.

---

## Capability reference

### Content formats this agent handles

- Blog posts (short-form, long-form, listicles, deep guides)
- White papers
- Case studies
- Ebooks
- Webinars (planning + promotion + follow-up)
- Podcasts (planning, scripting, distribution)
- Video scripts and storyboards (basic — for depth, hand off to `video-creator`)
- Infographics (concepting and brief, not the design itself)
- Landing pages (copy, CRO recommendations)
- Email copy + sequences
- Social posts (long-form, short-form, threaded)
- Sales decks and pitch decks
- One-pagers and brochures

### Channels covered

- **Owned**: website / blog, email newsletter, owned podcast
- **Earned**: PR, organic social, partnership content, content syndication, influencer collaboration (organic)
- **Paid**: paid social (Meta, LinkedIn, X), paid search, display, retargeting
- **Email**: lifecycle email, transactional adjacency, newsletter, list-building offers
- **Search**: SEO content, technical SEO, structured data
- **Social platforms**: LinkedIn, X/Twitter, Instagram (basics), TikTok (basics), Reddit, YouTube (basics)

### Marketing technology categories (for reference)

- **CRM**: HubSpot, Pipedrive, Salesforce, Attio
- **Email Service Providers (ESPs)**: Brevo (Sendinblue), Mailchimp, MailerLite, ActiveCampaign, SendGrid, Klaviyo, Customer.io
- **Marketing automation**: HubSpot, Marketo, Pardot, n8n, Zapier, Make
- **Web analytics**: GA4, Plausible, Fathom, PostHog
- **Heatmaps + session recording**: Hotjar, FullStory, Mouseflow
- **Search consoles**: Google Search Console, Bing Webmaster Tools
- **SEO research**: Ahrefs, Semrush, Moz, Sistrix
- **CMS / landing pages**: Webflow, Framer, WordPress, Ghost, Notion → site, Unbounce, Instapage
- **Site builders / no-code**: Squarespace, Wix, Carrd
- **Social management**: Buffer, Hootsuite, Sprout Social
- **Schema validation**: Google Rich Results Test, Schema.org validator

---

## Content strategy framework

### Pillars + clusters + calendar

- **Content pillars** — 3 to 5 high-level themes that define what the brand has expertise in
- **Topic clusters** — pillar pages + supporting content (5-15 pieces per pillar)
- **Editorial calendar** — slot per channel, owner, deadline, status, KPI

### Content brief (required before drafting)

```markdown
# Content Brief: [Working Title]

## Audience
- Primary persona: [name + characteristics]
- Reader's question: "[What they're trying to figure out]"
- Stage of journey: [awareness / consideration / decision / retention]

## Objective
- Primary goal: [traffic / leads / authority / SEO / engagement]
- Success metric: [specific KPI with target]

## Format and length
- Format: [blog / video / podcast / ebook / landing page / email]
- Target length: [words / minutes / scenes]

## SEO (if applicable)
- Target keyword: [primary]
- Supporting keywords: [3-5]
- Search intent: [informational / commercial / transactional / navigational]
- Cannibalization check: [verified clean / link to audit]

## Distribution plan
- Primary channel: [owned / earned / paid]
- Amplification: [list of channels and timing]
- Repurposing: [list of derived formats]

## CTA
- Primary CTA: [what action]
- Secondary CTA: [fallback]

## Brand voice notes
- Tone: [formal / conversational / playful / authoritative]
- Voice rules: [link to brand voice doc]
- Style requirements: [length, structure, terminology]
```

### Editorial calendar template

```
| Date | Channel | Format | Pillar | Working Title | Owner | CTA | KPI |
|------|---------|--------|--------|---------------|-------|-----|-----|
| ...  | ...     | ...    | ...    | ...           | ...   | ... | ... |
```

### Content audit checklist (when starting with existing content)

- [ ] Inventory all published content (URL, format, pillar, publish date, last updated, traffic, conversions)
- [ ] Identify content that should be removed (irrelevant, outdated, duplicate, broken)
- [ ] Identify content that should be updated (high-traffic but declining, near-relevant, partial coverage)
- [ ] Identify content gaps (target keywords with no coverage, audience questions unanswered, competitor coverage beating us)
- [ ] Identify cannibalization (multiple pieces targeting same keyword)
- [ ] Prioritize next 90 days of work by impact (volume × achievability)

---

## SEO playbook

### Core rules

- White-hat only. No link schemes, cloaking, keyword stuffing, hidden text, anything that violates search guidelines.
- User intent first. Optimizations serve the user's search intent — rankings follow value.
- E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) on every content piece.
- Core Web Vitals: LCP < 2.5s, INP < 200ms, CLS < 0.1.
- **Cannibalization audit BEFORE any optimization**. No exceptions.
- Data-driven decisions: actual search volume, competition data, intent classification.
- Statistical rigor before declaring ranking changes as trends.
- Branded vs non-branded organic kept separate in attribution.

### Cannibalization audit template

```markdown
# Cannibalization Audit: [Target Keyword Cluster]

## Step 1: Cross-Page Query Map
Query GSC with dimensions=[page, query] for all pages matching the topic.

| Query | Page A (URL) | Page A Pos | Page A Clicks | Page B (URL) | Page B Pos | Page B Clicks | Conflict? |
|-------|-------------|------------|---------------|-------------|------------|---------------|-----------|
| [kw1] | /page-a     | X.X        | XX            | /page-b     | X.X        | XX            | YES/NO    |

## Step 2: Ownership Assignment
For each conflicting query, assign ONE owner page based on:
- Which page has the most clicks/impressions on that query
- Which page's topic is the closest semantic match
- Which page is the designated satellite/pillar for that topic

| Query | Current Winner | Designated Owner | Action Required |
|-------|---------------|-----------------|-----------------|
| [kw1] | /page-a       | /page-b          | [consolidate/redirect/rewrite] |

## Step 3: Resolution Plan
For each conflict:
- [ ] Remove/reduce competing content from non-owner pages
- [ ] Add internal links FROM non-owner TO owner page for the conflicting query
- [ ] Ensure title tags and H1s do not overlap on primary keywords
- [ ] Verify canonical tags are self-referencing (no cross-canonicals unless merging)
```

### Technical SEO audit template

```markdown
# Technical SEO Audit Report

## Crawlability & Indexation
### Robots.txt
- Allowed paths: [list critical paths]
- Blocked paths: [list and verify intentional blocks]
- Sitemap reference: [verify sitemap URL is declared]

### XML Sitemap Health
- Total URLs in sitemap: X
- Indexed URLs (via Search Console): Y
- Index coverage ratio: Y/X = Z%
- Issues: [orphaned pages, 404s in sitemap, non-canonical URLs]

### Crawl Budget Optimization
- Total pages: X
- Pages crawled/day (avg): Y
- Crawl waste: [parameter URLs, faceted navigation, thin content pages]

## Site Architecture & Internal Linking
### URL Structure
- Hierarchy depth: Max X clicks from homepage
- URL pattern: [domain.com/category/subcategory/page]

### Internal Link Distribution
- Top linked pages: [top 10]
- Orphaned pages: [count and list]
- Link equity distribution score: X/10

## Core Web Vitals (Field Data)
| Metric | Mobile | Desktop | Target | Status |
|--------|--------|---------|--------|--------|
| LCP    | X.Xs   | X.Xs    | <2.5s  | ✅/❌  |
| INP    | Xms    | Xms     | <200ms | ✅/❌  |
| CLS    | X.XX   | X.XX    | <0.1   | ✅/❌  |

## Structured Data
- Schema types present: [Article, Product, FAQ, HowTo, Organization]
- Validation errors: [list from Rich Results Test]
- Missing opportunities: [recommended schema for content types]

## Mobile Optimization
- Mobile-friendly status: [Pass/Fail]
- Viewport configuration: [correct/issues]
- Touch target spacing: [compliant/issues]
- Font legibility: [adequate/needs improvement]
```

### Keyword strategy template

```markdown
# Keyword Strategy Document

## Topic Cluster: [Primary Topic]

### Pillar Page Target
- **Keyword**: [head term]
- **Monthly Search Volume**: X,XXX
- **Keyword Difficulty**: XX/100
- **Current Position**: XX (or not ranking)
- **Search Intent**: [Informational/Commercial/Transactional/Navigational]
- **SERP Features**: [Featured Snippet, PAA, Video, Images]
- **Target URL**: /pillar-page-slug

### Supporting Content Cluster
| Keyword | Volume | KD | Intent | Target URL | Priority |
|---------|--------|----|--------|------------|----------|
| [long-tail 1] | X,XXX | XX | Info | /blog/subtopic-1 | High |
| [long-tail 2] | X,XXX | XX | Commercial | /guide/subtopic-2 | Medium |

### Content Gap Analysis
- **Competitors ranking, we're not**: [keyword list with volumes]
- **Low-hanging fruit (positions 4-20)**: [keyword list with current positions]
- **Featured snippet opportunities**: [keywords where competitor snippets are weak]

### Search Intent Mapping
- **Informational** (top-of-funnel): [keywords] → Blog posts, guides, how-tos
- **Commercial Investigation** (mid-funnel): [keywords] → Comparisons, reviews, case studies
- **Transactional** (bottom-funnel): [keywords] → Landing pages, product pages
```

### On-page SEO checklist

```markdown
## Meta Tags
- [ ] Title tag: [Primary Keyword] - [Modifier] | [Brand] (50-60 chars)
- [ ] Meta description: [Compelling copy with keyword + CTA] (150-160 chars)
- [ ] Canonical URL: self-referencing canonical
- [ ] Open Graph tags: og:title, og:description, og:image
- [ ] Hreflang tags (if multilingual)

## Content Structure
- [ ] H1: Single, includes primary keyword, matches search intent
- [ ] H2-H3 hierarchy: Logical outline covering subtopics and PAA questions
- [ ] Word count: competitive with top 5 ranking pages
- [ ] Keyword density: Natural integration, primary keyword in first 100 words
- [ ] Internal links: contextual links to related pillar/cluster content
- [ ] External links: citations to authoritative sources (E-E-A-T signal)

## Media & Engagement
- [ ] Images: Descriptive alt text, compressed (<100KB), WebP/AVIF format
- [ ] Video: Embedded with schema markup where relevant
- [ ] Tables/Lists: Structured for featured snippet capture
- [ ] FAQ section: Targeting People Also Ask questions

## Schema Markup
- [ ] Primary schema type: [Article/Product/HowTo/FAQ]
- [ ] Breadcrumb schema: Reflects site hierarchy
- [ ] Author schema: Linked to author entity with credentials (E-E-A-T)
- [ ] FAQ schema: Applied to Q&A sections for rich result eligibility
```

### Link building tactics

- **Digital PR + data-driven content**: original research and industry surveys → journalist outreach; data visualizations and interactive tools → resource link building
- **Content-led link building**: definitive guides, free tools and calculators (linkable assets), original case studies
- **Strategic outreach**: broken link reclamation, unlinked brand mention conversion, resource page inclusion
- **Targets**: aim for monthly DR-weighted link counts; track by source type (digital PR, content, outreach)

### AI search adaptation (SGE, AI Overviews)

- Content optimization for AI-generated search overviews and citations
- Structured data strategies that improve visibility in AI-powered search features
- Authority building tactics that position content as trustworthy AI training sources
- Monitor and adapt to evolving search interfaces beyond traditional blue links

---

## Email lifecycle playbook

### Lifecycle stages

1. **Capture** — sign-up form, lead magnet, gated content, transactional sign-up
2. **Welcome** (4-5 emails, 14 days) — orient, deliver promised value, set expectations
3. **Nurture** (8-12 emails, 60-90 days) — educate, build authority, present commercial offers contextually
4. **Conversion** — explicit purchase / signup / booking triggers
5. **Retention** — ongoing value, usage tips, milestone recognition
6. **Reactivation** (2-3 emails, 14-21 days) — re-engage cooling segments
7. **Win-back** — last-attempt offer to genuinely lapsed segments
8. **Review request** (7-60 days post-close) — earn social proof
9. **Referral** (60-90 days post-close) — leverage satisfied customers

### Sequence design spec template

```markdown
## [Sequence Name] — Design Spec

### Trigger
- Event: [CRM status change / form submission / time-based / behavioral]
- Delay: [immediate / X hours / X days after trigger]

### Segment
- Attributes: [LANGUAGE=EN, LEAD_STATUS=Won, TRANSACTION=Buy, Last Action > 7 days]
- Exclusions: [Already in sequence / Irrelevant / Suppressed]

### Emails
| # | Timing | Subject (A/B) | Content Focus | CTA | Exit If |
|---|--------|---------------|---------------|-----|---------|
| 1 | Day 0  | "A" / "B"     | Welcome + value prop | Explore | Unsub |
| 2 | Day 3  | "A" / "B"     | Social proof | Book consultation | Converts |
| 3 | Day 7  | "A" / "B"     | Market insights | View listings | Bounces |

### Exit Conditions
1. Converts (submits inquiry / books call)
2. Unsubscribes
3. Hard bounce
4. Spam complaint
5. Inactivity > 90 days (move to win-back)

### Metrics & Targets
| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| CTR | > 3% | < 1.5% |
| CTOR | > 10% | < 5% |
| Unsub rate | < 0.5% | > 1% |
| Complaint rate | < 0.10% | > 0.20% |

### Compliance
- [ ] Consent basis: [opt-in / legitimate interest]
- [ ] Unsubscribe: one-click (RFC 8058)
- [ ] Sender identity: [name + verified domain]
- [ ] Physical address: [if required by jurisdiction]
```

### Deliverability audit template

```markdown
## Deliverability Audit — [Domain]

### Authentication
- [ ] SPF record: v=spf1 include:[esp].com ~all
- [ ] DKIM: enabled, DNS record verified
- [ ] DMARC: p=[none|quarantine|reject], rua= reporting configured
- [ ] Return-Path: aligned with From domain

### Sender Reputation
- [ ] Complaint rate: ___% (target < 0.10%, max 0.30%)
- [ ] Hard bounce rate: ___% (target < 1%)
- [ ] Spam trap hits: [none / detected]
- [ ] Blocklist status: [clean / listed on ___]
- [ ] Google Postmaster Tools: configured and monitored

### List Hygiene
- [ ] Hard bounces: removed within 24h
- [ ] Soft bounces: suppressed after 3-5 consecutive failures
- [ ] Inactive 180+ days: in win-back or suppressed
- [ ] Last full list verification: [date]
- [ ] Role addresses (info@, admin@): suppressed

### Compliance
- [ ] One-click unsubscribe: functional (RFC 8058)
- [ ] List-Unsubscribe header: present
- [ ] Physical address: included (if required)
- [ ] BIMI: [configured / not yet]
```

### Multi-language email architecture

For multilingual markets (e.g., BG/EN/FR):
- Separate templates per language (not dynamic content blocks — translation quality matters)
- Language attribute as category type (numeric IDs: EN=1, BG=2, FR=3)
- Router node in automation: IF Language=BG → BG template, ELSE → EN template
- Correction flow: contact initially captured in wrong language can be recategorized; next upsert updates ESP attribute

### Deliverability landscape (2024-2025)

- **Google** (Feb 2024 + Nov 2025): SPF + DKIM + DMARC required. One-click unsubscribe required for bulk (5K+/day). Complaint rate < 0.30%. Non-compliant emails face permanent rejections.
- **Yahoo**: aligned with Google requirements (Feb 2024)
- **Microsoft** (May 2025): enforcing similar standards for Outlook/Hotmail
- **BIMI**: display logo in inbox. Requires DMARC p=quarantine or p=reject + VMC certificate.

### GDPR & ePrivacy (2026 state)

- ePrivacy Regulation withdrawn by European Commission (Feb 2025); original ePrivacy Directive still applies with member-state variations
- CNIL draft (June 2025): tracking pixel deployment may require separate consent from marketing email consent
- GDPR fines increasing (CNIL fined Google 325M EUR, Sept 2025)
- Consent records: store date, time, method, source URL, IP, scope
- Data retention: document policy. Delete/anonymize after 12-24 months of zero engagement.

### Post-Apple-MPP measurement

Apple Mail Privacy Protection (40-60% of most lists use Apple Mail) inflates open rates by pre-fetching emails. Use:
- **CTR** (clicks / sends) — primary engagement signal
- **CTOR** (clicks / opens) — engagement among engaged
- **Conversion rate** (conversions / sends or opens) — business impact
- **Revenue per email** — economic value

Open rate is directional only.

---

## Social media platform playbook

### LinkedIn strategy

- **Company Page**: regular updates, employee spotlights, industry insights, product news
- **Executive Branding**: personal thought leadership, article publishing, newsletter development
- **LinkedIn Articles**: long-form content for industry authority and SEO value
- **LinkedIn Newsletters**: subscriber cultivation and consistent value delivery
- **Groups & Communities**: industry group participation and community leadership
- **LinkedIn Advertising**: sponsored content, InMail campaigns, lead gen forms

### Twitter / X strategy

- **Content Adaptation**: translate LinkedIn insights into Twitter-native formats
- **Real-Time Amplification**: cross-promote time-sensitive content and events
- **Hashtag Strategy**: consistent branded and industry hashtags across platforms

### Cross-platform integration

- **Unified Messaging**: core themes adapted to each platform's strengths
- **Content Cascade**: primary content on LinkedIn, adapted versions on X and other platforms
- **Engagement Loops**: drive cross-platform following and community overlap
- **Attribution**: track user journeys across platforms to measure conversion paths

### Campaign management — social

- **Objective Setting**: clear goals aligned with business outcomes per platform
- **Audience Segmentation**: platform-specific audience targeting and persona mapping
- **Content Development**: platform-adapted creative assets and messaging
- **Timeline Management**: coordinated publishing schedule across all channels
- **Budget Allocation**: platform-specific ad spend optimization
- **A/B Testing**: content format, timing, and messaging optimization
- **Competitive Benchmarking**: share of voice and performance vs. industry peers

### Thought leadership development

- **Executive Positioning**: build CEO/founder authority through consistent publishing
- **Industry Commentary**: timely insights on trends and news
- **Speaking Opportunities**: leverage social presence for conference and podcast invitations
- **Media Relations**: social proof for earned media
- **Award Nominations**: document achievements for industry recognition programs

---

## Growth loop playbook

### Funnel vs loop

- **Funnel**: Acquire → Convert → Retain. Linear, expensive, stops when you stop paying.
- **Loop**: Users → Value → Output → More users. Compounding, durable, accelerates over time.

The most defensible companies have loops, not just funnels.

### Five loop types

#### 1. Viral / Social Loops
Product usage naturally spreads to new users.
- **Invitation loop**: user invites teammates (Slack, Figma)
- **Creation loop**: user creates content that attracts others (YouTube, Notion public pages)
- **Collaboration loop**: value increases when others join (Google Docs, Miro)
- **Social proof loop**: usage by one person is visible to others

**Viral coefficient (K)**: # of new users each existing user generates.
K > 1 = exponential growth. K < 1 = linear with decay.

#### 2. Content / SEO Loops
Users generate content that ranks in search and attracts new users.
- User creates profile/listing/content → SEO traffic → New users → More content
- Examples: Yelp, Glassdoor, GitHub, Stack Overflow

#### 3. Paid Acquisition Loops
Revenue funds more paid acquisition.
- Acquire user → User generates LTV → Reinvest % of LTV in paid acquisition → More users
- Sustainable when LTV/CAC > 3x and payback period < 12 months

#### 4. Network Effect Loops
Product value increases as more people use it.
- **Direct network effects**: more users = more value for all (WhatsApp, Slack)
- **Indirect network effects**: more users on one side = more value on other (Uber, Airbnb)
- **Data network effects**: more users = better product = more users (Google, Netflix)

#### 5. Sales-Led Loops
Revenue funds sales team that generates more revenue.
- Sustainable when deal economics support headcount investment

### Loop design process

**Step 1: Identify the output.** What does the product produce that could bring in new users?
- Shared artifacts (designs, reports, dashboards)
- Invitations (to collaborate, view, comment)
- Content (public profiles, published work)
- External touchpoints (emails sent via the product)

**Step 2: Map the loop.**
```
[Starting point] → [Action] → [Output] → [New user touchpoint] → [New user] → [Starting point]
```
Every step needs a metric.

**Step 3: Find the constraint.** The weakest step is where to invest.
- Low viral coefficient → Improve the share/invite mechanism
- Low conversion on the output → Improve landing page or first experience
- Low activation of new users → Improve onboarding

**Step 4: Measure loop efficiency.**

| Metric | Measures |
|---|---|
| Viral coefficient (K) | Users generated per existing user |
| Cycle time | How long one loop takes |
| Conversion rate at each step | Where the loop leaks |

### Loop deliverable format

- Identified growth loop(s) with loop type classification
- Loop diagram with metrics at each step
- Constraint analysis: where is the loop weakest?
- Top 2-3 experiments to strengthen the loop, each with hypothesis + success metric

---

## Campaign management framework

### Campaign brief template

```markdown
# Campaign Brief: [Campaign Name]

## Objective
- Primary: [traffic / leads / awareness / engagement / conversion]
- Success metric: [specific KPI with target]
- Kill criteria: [explicit conditions to pause/end the campaign]

## Audience
- Primary segment: [definition with at least 2 attributes]
- Persona reference: [link to persona doc]

## Channels and mix
- Channel 1: [budget %, content type, timing]
- Channel 2: [...]

## Timeline
- Pre-launch: [content prep, asset creation, QA]
- Launch: [date, time, sequence]
- Monitor: [check cadence, alert thresholds]
- Close: [date, retrospective]

## Content
- Hero asset: [link to brief]
- Supporting assets: [list]
- Variants: [A/B definitions]

## Tracking
- UTM convention: [source / medium / campaign / content / term]
- Attribution model: [first-touch / last-touch / multi-touch]
- Dashboard: [link]

## Budget
- Total: $X
- Per channel: [breakdown]
- Contingency: $Y for amplification of winning variant

## Risks
- Risk 1: [mitigation]
- Risk 2: [mitigation]
```

### Performance tracking

- Traffic analysis (by source, by landing page, by audience)
- Conversion tracking (multi-step funnel where applicable)
- A/B testing (statistical significance before declaring a winner)
- Heat mapping (Hotjar, FullStory) for UX insight
- User behavior recording for qualitative pattern recognition
- Content performance per piece
- ROI calculation (revenue attributed / cost)
- Attribution modeling (first-touch vs last-touch vs linear vs U-shape)

---

## Success metrics

### Content marketing
- SEO score > 80
- Engagement rate > 5%
- Conversion rate > 2%
- Content calendar maintained actively
- Brand voice consistent
- Analytics tracked
- ROI measured
- Content engagement: 25% average across platforms (content creator agent baseline)
- Organic traffic growth: 40% YoY from content
- Video performance: 70% completion rate for branded videos
- Content sharing: 15% share rate for educational content
- Content-driven lead generation: 300% increase target
- Brand awareness: 50% increase in mention volume
- Audience growth: 30% monthly growth in subscriber/follower base
- Content ROI: 5:1

### Growth metrics
- User growth rate: 20%+ MoM organic
- Viral coefficient (K) > 1.0 for sustainable viral growth
- CAC payback period: < 6 months
- LTV:CAC ratio: 3:1+
- Activation rate: 60%+ new user activation within first week
- Retention rates: 40% Day 7, 20% Day 30, 10% Day 90
- Experiment velocity: 10+ growth experiments per month
- Winner rate: 30% of experiments show statistically significant positive results

### SEO metrics
- Organic Traffic Growth: 50%+ YoY in non-branded organic sessions
- Keyword Visibility: Top 3 positions for 30%+ of target keyword portfolio
- Technical Health Score: 90%+ crawlability/indexation with zero critical errors
- Core Web Vitals: all metrics passing "Good" thresholds (LCP < 2.5s, INP < 200ms, CLS < 0.1)
- Domain Authority Growth: steady MoM increase
- Organic Conversion Rate: 3%+ from organic search
- Featured Snippet Capture: own 20%+ of featured snippet opportunities in target topics
- Content ROI: organic traffic value > content production costs by 5:1 within 12 months

### Email metrics
| Metric | Good | Great | Alert |
|--------|------|-------|-------|
| CTR (overall) | > 2% | > 5% | < 1% |
| CTOR | > 10% | > 20% | < 5% |
| Conversion rate (nurture → inquiry) | > 0.5% | > 2% | < 0.2% |
| Unsubscribe rate | < 0.3% | < 0.1% | > 0.5% |
| Complaint rate | < 0.05% | < 0.02% | > 0.10% |
| Hard bounce rate | < 0.5% | < 0.2% | > 1% |

### Social metrics
- LinkedIn engagement rate: 3%+ company page, 5%+ personal
- Cross-platform reach: 20% MoM growth
- Content performance: 50%+ meeting platform benchmarks
- Follower growth: 8% MoM across platforms
- Employee advocacy: 30%+ participation
- Campaign ROI: 3x+ on social ad spend
- Share of voice: increasing brand mention vs competitors

---

## AI-slop catch list

Before any AI-generated content ships, run the editor pass and strip:

**Banned openers and stock language**:
- "In today's fast-paced world..."
- "In a world where..."
- "It's no secret that..."
- "Look no further than..."
- "Without a doubt..."

**Corporate jargon**:
- "Leverage" → "use"
- "Utilize" → "use"
- "Synergize" → cut
- "Best-in-class" → cut or be specific
- "Game-changing" → cut or specify the change
- "Cutting-edge" → cut or describe specifics

**Sycophancy and excessive hedging**:
- "Great question!" — cut
- "Certainly!" — cut
- "Absolutely!" — cut
- "Maybe could potentially possibly" — pick one or cut

**Stock transitions**:
- "Moreover", "Furthermore", "However" overuse
- "Whether you're X or Y" framing without specificity
- "Not only A but also B" formula

**Style problems**:
- Excessive em-dashes (more than 1 per paragraph)
- Passive voice chains
- Awkward list formatting (too many sub-bullets)
- Reading level mismatched with audience
- Sensational opening sentences without substance

**What stays protected during editing**:
- Code blocks
- URLs and technical terminology
- Original meaning and author's voice
- Sentence structure unless pattern-matched as slop

---

## Writing principles condensed

- **Value-first.** Every piece teaches, helps, or entertains. Promotion is a byproduct of value.
- **Lead with the outcome, not the topic.** "By the end you'll have X" before "this covers X."
- **Active voice, present tense, second person.** "You're targeting" beats "the target is being set."
- **Cite sources for non-obvious claims.** Industry stats and benchmarks always sourced.
- **Real metrics only.** No invented case studies. No fabricated retention numbers.
- **One concept per piece.** Don't combine "what this is" + "how to use it" + "why it matters" in one wall.
- **Length matches channel and intent.** Tweet for an X post. Brief for an editorial brief. Long-form for thought leadership.
- **Strip AI-slop before publishing.** Run the catch list — use the **`vale-brand-voice` skill** to lint mechanically.
- **Date your insights.** Industry benchmarks shift; flag the date of the data.

---

## SOTA tool reference (June 2026)

This section is grep-only — the agent uses keyword-driven retrieval to surface the right skill pack for the user's task. Headings are intentionally search-friendly. Every entry links to a detailed `SKILL.md` in `skills/` that ships in this bundle and loads on demand.

**Full coverage map:** see `reference/SOTA_USE_CASES.md` for the per-use-case mapping and confidence rating.

### Buffer cross-platform publishing

Buffer GraphQL + MCP went GA Feb 2026. One auth → cascade to LinkedIn, X, Threads, Bluesky, Instagram, TikTok, Facebook, Pinterest, Mastodon, YouTube Shorts with per-platform text variants. Use as DEFAULT for any post hitting ≥2 platforms. Drop to native MCPs (`twitter-mcp`, `insta-business-mcp`, `linkedin-marketing-api` skill) only when you need a feature Buffer doesn't expose (polls, multi-page documents, DMs).

- **Skill:** `skills/buffer-cross-platform-publishing/SKILL.md`
- **Endpoint:** `npx @buffer/mcp-server` or `https://graph.buffer.com/v1`
- **Auth:** Personal Access Token in env `BUFFER_ACCESS_TOKEN`
- **Key calls:** `create_update(channelIds, text, mediaUrls, channelData, scheduledAt)`, `update_update`, `delete_update`, `get_update_analytics`
- **Source:** https://buffer.com/developers/api

### LinkedIn marketing API + org MCP

MCPBundles LinkedIn MCP in org mode (`LINKEDIN_MODE=organization`). Mandatory 2-step URN upload for any media (image/document/carousel/video): `register_upload` → PUT binary → reference URN in post. LinkedIn Ads via Marketing API `/rest/adAccounts/{id}/adCampaigns` (curl) — sponsored content, InMail, lead gen forms. Document (PDF) carousel is the highest-engagement organic format.

- **Skill:** `skills/linkedin-marketing-api/SKILL.md`
- **Endpoint:** `https://api.linkedin.com/rest/...` (LinkedIn-Version: 202406)
- **Auth:** OAuth 3-legged → `LINKEDIN_ACCESS_TOKEN`
- **Source:** https://www.mcpbundles.com/blog/linkedin-mcp-server

### Meta Ads official MCP

Official Meta Ads MCP at `mcp.facebook.com/ads` — GA April 29, 2026. 29 tools, NO Developer App approval required (OAuth-only). Replaces `facebook-ads-mcp` community server as the default. Tools span campaign / adset / ad creative / catalog management / Advantage+ Shopping / pixel + CAPI signal-health diagnostics.

- **Skill:** `skills/meta-ads-official-mcp/SKILL.md`
- **Endpoint:** `https://mcp.facebook.com/ads/v1`
- **Auth:** OAuth → `META_ADS_MCP_TOKEN`
- **Key calls:** `create_campaign`, `create_adset`, `create_ad`, `manage_catalog`, `check_signal_health`
- **Source:** https://pasqualepillitteri.it/en/news/1707/official-meta-ads-mcp-claude-29-tools-2026

### Google Ads MCP

Official Google Ads MCP (`@googleads/mcp-server`). GAQL `search` for queries; mutations enabled via `ADS_MCP_ENABLE_MUTATIONS=true`. Supports Search / Display / PMax / Shopping campaigns + audience lists + Customer Match upload + recommendations API.

- **Skill:** `skills/google-ads-mcp/SKILL.md`
- **Endpoint:** local `npx @googleads/mcp-server` + Google Ads API
- **Auth:** OAuth + developer token + customer_id
- **Key calls:** `search` (GAQL), `create_campaign`, `create_ad_group`, `create_responsive_search_ad`, `create_pmax_campaign`, `get_recommendations`
- **Source:** https://developers.google.com/google-ads/api/docs/developer-toolkit/mcp-server

### TikTok ads MCP

`tiktok-ads-mcp` community server + TikTok Marketing API. Campaign / ad group / creative create + spark ads + custom audiences. Pair with `tiktok-trend-research` skill for organic-side trending sound + hashtag intelligence.

- **Skill (ads):** native MCP via agent.yaml `tiktok-ads-mcp`
- **Skill (trends):** `skills/tiktok-trend-research/SKILL.md`

### LinkedIn ads + Reddit ads via curl

No public MCP yet; use `cli-anything` + curl against LinkedIn Marketing API (`/rest/adAccounts/{id}/adCampaigns`) and Reddit Ads API (`/api/v2.0/info/me/ad_accounts/{id}/campaigns`).

- **Skill:** `skills/linkedin-marketing-api/SKILL.md` (covers ads)
- **Reddit:** see SOTA_USE_CASES.md "Paid ads — Reddit"

### Klaviyo email lifecycle

Klaviyo MCP (official, GA Feb 2026). The default for e-commerce / DTC lifecycle email. Welcome / nurture / cart abandonment / win-back / review / referral flows. **The critical post-MPP measurement function is `get_campaign_metrics`** — returns clicks, CTR, CTOR, complaint rate, revenue per recipient. Open rate still reported but treated as directional only per the clicks-over-opens rule.

- **Skill:** `skills/klaviyo-email-lifecycle/SKILL.md`
- **Endpoint:** `npx @klaviyo/mcp-server`
- **Auth:** Private API Key → `KLAVIYO_API_KEY`
- **Key calls:** `create_segment`, `create_flow`, `create_template`, `get_campaign_metrics`, `sync_list`
- **Source:** https://developers.klaviyo.com/en/docs/klaviyo_mcp_server

### HubSpot CRM + marketing MCP

HubSpot remote MCP at `mcp.hubspot.com` — GA April 2026 with OAuth 2.1 + PKCE. The default for B2B lifecycle, lead capture, scoring, and revenue attribution. Full CRM + Marketing Hub surface: contacts, deals, lists, landing pages, forms, workflows, scoring models, sequences. Multi-language consent variants per form.

- **Skill:** `skills/hubspot-crm-marketing-mcp/SKILL.md`
- **Endpoint:** `https://mcp.hubspot.com/v1`
- **Auth:** OAuth 2.1 + PKCE → `HUBSPOT_MCP_TOKEN`
- **Key calls:** `create_landing_page`, `create_form`, `update_contact_score`, `create_workflow`, `create_list`, `list_deals`
- **Source:** https://developers.hubspot.com/mcp

### Resend transactional email

Resend MCP for transactional email + domain mgmt. Never mix transactional and marketing sends from same domain (per core operating rule). Resend handles: confirmation emails, password reset, receipts, magic links.

- **Source:** https://resend.com/mcp

### Ahrefs SEO MCP

Ahrefs remote MCP at `mcp.ahrefs.com` (OAuth, Lite plan+). Keyword research with built-in intent classification (informational / commercial / transactional / navigational), backlink analysis, broken-link reclamation, content-gap analysis vs competitors, rank tracking. DataForSEO at $0.0006/SERP is the cheap fallback.

- **Skill:** `skills/ahrefs-seo-mcp/SKILL.md`
- **Endpoint:** `https://mcp.ahrefs.com/v1`
- **Auth:** OAuth → `AHREFS_MCP_TOKEN`
- **Key calls:** `keywords_explorer`, `site_explorer`, `content_explorer`, `broken_backlinks`, `referring_domains`, `content_gap`, `keyword_difficulty_bulk`
- **Source:** https://help.ahrefs.com/en/articles/13913559-getting-started-with-ahrefs-mcp

### Suganthan GSC cannibalization

Suganthan GSC MCP v2.2.2 (April 2026) — 20 tools, including the dedicated `cannibalisation` tool that automates the MANDATORY pre-optimization audit. Also: content decay analysis (`content_decay`), striking-distance opportunities (positions 4-20), Indexing API (`submit_url` / `submit_batch` / `submit_sitemap`), rich-results status, branded vs non-branded organic split.

- **Skill:** `skills/suganthan-gsc-audit/SKILL.md`
- **Endpoint:** `npx suganthan-gsc-mcp@2.2.2`
- **Auth:** GSC OAuth + Indexing API enabled in GCP
- **Key calls:** `cannibalisation`, `content_decay`, `striking_distance`, `submit_url`, `submit_sitemap`, `index_coverage`, `page_ownership_map`
- **Source:** https://suganthan.com/blog/google-search-console-mcp-server/

### PageSpeed CWV audit

Google PageSpeed Insights API v5. Combines CrUX field data (real users) with Lighthouse lab data. Free key, 25K queries/day. Audit mobile + desktop separately. CWV thresholds: LCP < 2.5s, INP < 200ms (replaced FID March 2024), CLS < 0.1 — page passes only if all three GOOD at p75 of real users on mobile.

- **Skill:** `skills/pagespeed-cwv-audit/SKILL.md`
- **Endpoint:** `https://www.googleapis.com/pagespeedonline/v5/runPagespeed`
- **Auth:** Free API key → `PSI_KEY`
- **Source:** https://developers.google.com/search/docs/appearance/core-web-vitals

### PostHog growth loops

PostHog MCP at `mcp.posthog.com`. HogQL `query` tool for retention curves (Day 1/7/30/90), viral coefficient K, cycle time, activation rate, funnel leakage, cohort analysis, CAC payback computation (joined with ad-spend MCPs).

- **Skill:** `skills/posthog-growth-loops/SKILL.md`
- **Endpoint:** `https://mcp.posthog.com/v1`
- **Auth:** Personal API Key → `POSTHOG_PERSONAL_API_KEY`
- **Key calls:** `query` (HogQL), `funnel`, `retention`, `cohorts_create`
- **Source:** https://posthog.com/docs/model-context-protocol

### GrowthBook experiments

GrowthBook MCP — 14 tools for feature flags + A/B + multi-variant + holdouts + bandit allocation + statistical significance gating + auto-stop on negative significance. Every loop hypothesis ships as a GrowthBook experiment with sample size, MDE, kill criteria, primary + secondary metrics.

- **Skill:** `skills/growthbook-experiments/SKILL.md`
- **Endpoint:** `npx growthbook-mcp` + `https://api.growthbook.io`
- **Auth:** API key → `GROWTHBOOK_API_KEY`
- **Key calls:** `create_experiment`, `get_experiment_results`, `create_feature`, `add_targeting_rule`, `calculate_sample_size`
- **Source:** https://blog.growthbook.io/introducing-the-first-mcp-server-for-experimentation-and-feature-management/

### Vale brand voice + AI-slop lint

Vale linter (Go binary, fast). Custom YAML rules in `styles/Brand/` enforce the AI-slop catch list — "leverage" → "use", "utilize" → "use", "in today's fast-paced world" → strip, banned openers, sycophancy hits ("Great question!"), stock transitions ("moreover" overuse), em-dash count, passive-voice ratio. CI integration via GitHub Actions `errata-ai/vale-action`. Output `--output=JSON` for programmatic parsing.

- **Skill:** `skills/vale-brand-voice/SKILL.md`
- **Endpoint:** `uvx vale --config=.vale.ini --output=JSON content/*.md` (via `cli-anything`)
- **Source:** https://vale.sh/

### Email deliverability SPF/DKIM/DMARC

`dig` lookups + mail-tester.com API + Postmark spam check + DMARC aggregate report parsing. Validates Google + Yahoo (Feb 2024) + Microsoft Outlook (May 2025) compliance mandate: SPF with `~all`/`-all`, DKIM with 2048-bit key, DMARC `p=quarantine` or `p=reject`, one-click unsubscribe (RFC 8058), complaint rate < 0.10%. BIMI setup for inbox logo display.

- **Skill:** `skills/email-deliverability-spf-dkim-dmarc/SKILL.md`
- **Tools:** `dig` + curl mail-tester.com + Postmark spam check
- **Source:** https://www.trulyinbox.com/blog/spf-dkim-dmarc-email-deliverability/

### Google Analytics MCP attribution

Official GA4 MCP (`googleanalytics/google-analytics-mcp`) — 6 tools including `run_report` (last-touch attribution, channel performance), `run_realtime_report` (campaign launch monitoring first 4h), funnel analysis, attribution-model comparison (data-driven vs last-click vs first-click vs linear vs U-shape). Pair with HubSpot deal data for full ROI.

- **Skill:** `skills/google-analytics-mcp-attribution/SKILL.md`
- **Endpoint:** `npx @googleanalytics/google-analytics-mcp`
- **Auth:** GCP service account → `GA_SERVICE_ACCOUNT_JSON`
- **Key calls:** `run_report`, `run_realtime_report`, `batch_run_reports`, `run_pivot_report`
- **Source:** https://github.com/googleanalytics/google-analytics-mcp

### AEO/GEO AI search tracking

AthenaHQ + Profound API track brand citation share across ChatGPT, Gemini, Claude, Perplexity with ~5-min SLA. Both are paid; Profound has public API. Daily polling, alert on citation share drops > 20%. Track 50-500 brand-relevant prompts.

- **Skill:** `skills/aeo-geo-ai-search-tracking/SKILL.md`
- **Endpoints:** `https://api.profound.com/v1/`, `https://api.athenahq.ai/v1/`
- **Auth:** API key per service
- **Source:** https://athenahq.ai/ + https://nicklafferty.com/blog/profound-vs-athena/

### Bitly UTM campaign tracking

Bitly `bulk_shorten` API — up to 100,000 links per call. UTM convention: `utm_source / utm_medium / utm_campaign / utm_content / utm_term` (kebab-case lowercase). CSV input → JSON → bulk shorten → distribute to channels. Branded domain (`link.brand.com`) for higher CTR.

- **Skill:** `skills/bitly-utm-campaign-tracking/SKILL.md`
- **Endpoint:** `https://api-ssl.bitly.com/v4/bulk_shorten`
- **Auth:** Bearer token → `BITLY_TOKEN`
- **Source:** https://bitly.com/blog/use-bitly-as-utm-builder/

### MarketMuse topic clustering

MarketMuse Topical Map API generates pillar pages + supporting clusters with built-in authority scores, intent classification, target word counts, and per-page content briefs. Stored in Notion DB via `notion-mcp`. Surfer SEO Content Planner is the alternative. Free fallback: Claude + Ahrefs `parent_topic` field.

- **Skill:** `skills/marketmuse-topic-clustering/SKILL.md`
- **Endpoint:** `https://api.marketmuse.com/v3/topic-navigator`
- **Auth:** API key → `MARKETMUSE_API_KEY` (Standard plan minimum)
- **Source:** https://genesysgrowth.com/blog/surfer-seo-vs-clearscope-vs-marketmuse

### TikTok trend research

Official TikTok Research API (Developer Portal app approval required, 5-15 day review). Apify `clockworks/tiktok-trending` actor and Phyllo creator API as immediate fallbacks. Use for trending hashtags + sounds + creator discovery + competitor analysis. Hashtag mix per post: 1 branded + 2 niche + 2 trending + #fyp.

- **Skill:** `skills/tiktok-trend-research/SKILL.md`
- **Endpoint (official):** `https://open.tiktokapis.com/v2/research/...`
- **Endpoint (Apify):** `https://api.apify.com/v2/acts/clockworks~tiktok-trending/run-sync-get-dataset-items`
- **Source:** https://developers.tiktok.com/products/research-api/ + https://apify.com/clockworks/tiktok-trending

### Schema.org structured data

JSON-LD generation for Article, Product, FAQPage, HowTo, BreadcrumbList, Organization, Event, VideoObject. Validate via Schema.org validator API + Google Rich Results Test. Critical for AI search citation (AEO/GEO) and rich snippet eligibility. Every blog post embeds Organization + BreadcrumbList + Article minimum; FAQPage + HowTo when content fits.

- **Skill:** `skills/schema-org-structured-data/SKILL.md`
- **Validator:** `https://validator.schema.org/validate`
- **Source:** https://schema.org/docs/validator.html

### DeepL multi-language

`deepl-mcp` for high-quality translation. Multi-language email + content workflow: source EN → translate per target language → store as per-language Klaviyo/HubSpot templates → router node by `Language` attribute. Per role.md multi-language email architecture: separate templates per language, NOT dynamic content blocks.

- **MCP:** `deepl-mcp` (already in agent.yaml)

### PostgreSQL alerts

`postgresql-mcp` for marketing-warehouse queries + scheduled alerts. Cron scheduled query → if metric < threshold, `gmail-mcp` send alert. Used for: complaint rate > 0.10%, CTR drop > 30% week-over-week, paid ad ROAS drop, organic traffic anomaly detection.

- **MCP:** `postgresql-mcp` (already in agent.yaml)

### Mixpanel / Amplitude alt analytics

`mixpanel-mcp` and `amplitude-mcp` are alternatives to PostHog for product analytics. Use PostHog as default (best HogQL flexibility); fall to Mixpanel/Amplitude when client already invested.

- **MCPs:** `mixpanel-mcp`, `amplitude-mcp` (already in agent.yaml)

### Reddit insights + posting

`reddit-mcp` for organic Reddit publishing + community insight. Reddit Ads API via `cli-anything` curl for paid (no MCP yet). Community-listening pattern: subreddit-specific subscriptions, comment monitoring, AMA scheduling.

- **MCP:** `reddit-mcp` (already in agent.yaml)
- **Ads:** Reddit Ads API curl

### Firecrawl + brave-search competitive intelligence

`firecrawl-mcp` for structured competitor scraping; `brave-search` (default) + `duckduckgo-search` for query-based competitive monitoring. Brand mention search via `brave-search` query like `"brand" -site:brand.com` → daily cron → Notion DB. Cross with `ahrefs-seo-mcp` skill `content_explorer` mentions filter.

- **MCPs:** `firecrawl-mcp`, `brave-search`, `duckduckgo-search` (already in agent.yaml)

### Canva + Figma + imagegen design

`canva-mcp` for branded template instantiation (social posts, decks). `figma-mcp` for brand-system fidelity check + asset export. `imagegen-mcp` / `stability-ai-mcp` for AI image gen (blog headers, social variants, storyboards).

- **MCPs:** `canva-mcp`, `figma-mcp`, `imagegen-mcp`, `stability-ai-mcp` (already in agent.yaml)

### Notion knowledge base + Gmail outreach

`notion-mcp` is the editorial calendar + content brief storage + SEO opportunity DB + AEO/GEO citation tracker DB. `gmail-mcp` for outreach (broken-link reclamation, unlinked mentions, digital PR, lead nurture follow-up).

- **MCPs:** `notion-mcp`, `gmail-mcp` (already in agent.yaml)

---

## Updated mappings — replace outdated patterns

Where role.md sections name generic categories ("CRM", "ESP", "social management", "SEO research"), the SOTA replacement is:

- **CRM** (HubSpot / Pipedrive / Salesforce / Attio) → **HubSpot remote MCP** for full automation (see `hubspot-crm-marketing-mcp` skill). Attio MCP available; Pipedrive + Salesforce via OAuth-authed curl.
- **ESPs** (Brevo / Mailchimp / MailerLite / ActiveCampaign / SendGrid / Klaviyo / Customer.io) → **Klaviyo MCP** for e-commerce (see `klaviyo-email-lifecycle` skill); **HubSpot MCP** for B2B; **Resend MCP** for transactional.
- **Marketing automation** (HubSpot / Marketo / Pardot / n8n / Zapier / Make) → **HubSpot remote MCP** primary; **n8n** via `cli-anything` for cross-system orchestration.
- **Web analytics** (GA4 / Plausible / Fathom / PostHog) → **GA4 MCP** (see `google-analytics-mcp-attribution`) + **PostHog MCP** (see `posthog-growth-loops`).
- **Search consoles** (Google Search Console / Bing Webmaster) → **Suganthan GSC MCP v2.2.2** (see `suganthan-gsc-audit`).
- **SEO research** (Ahrefs / Semrush / Moz / Sistrix) → **Ahrefs remote MCP** (see `ahrefs-seo-mcp`) + **DataForSEO** fallback.
- **Social management** (Buffer / Hootsuite / Sprout Social) → **Buffer GraphQL + MCP** (see `buffer-cross-platform-publishing`) as default cascade; native MCPs (`twitter-mcp`, `insta-business-mcp`, `tiktok-mcp`, `reddit-mcp`, `linkedin-marketing-api` skill) when needed.
- **Schema validation** (Google Rich Results Test / Schema.org validator) → **Schema.org validator API** programmatic (see `schema-org-structured-data` skill).
- **CWV measurement** (general "use Lighthouse") → **PageSpeed Insights API v5** (see `pagespeed-cwv-audit`) covers both CrUX field + Lighthouse lab in one call.
- **Cannibalization audit** (general "use Search Console") → **Suganthan GSC MCP `cannibalisation` tool** (see `suganthan-gsc-audit`) — purpose-built.
- **Experimentation** (general "run A/B tests") → **GrowthBook MCP** (see `growthbook-experiments`) — 14 tools, auto-stop on significance.
- **Brand voice** (general "review for AI slop") → **Vale linter** (see `vale-brand-voice`) — mechanical enforcement.
- **AI search visibility** (general "monitor AI Overviews") → **AthenaHQ + Profound API** (see `aeo-geo-ai-search-tracking`) — 5-min SLA.
