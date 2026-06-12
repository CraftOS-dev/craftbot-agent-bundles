# Competitive Intelligence — deep reference

This appends to `AGENT.md`. **Not** in the agent's default context. Grep when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "Continuous monitoring playbook", "Battlecard authoring playbook", "Kill-sheet playbook", "Win-loss CI playbook", "War games playbook", "Pricing intelligence playbook", "Product teardown playbook", "Hot-deals CI playbook", "Analyst-relations playbook", "Ethical CI playbook (SCIP code)", "Antipattern catalog", "SOTA tool reference", "SOTA execution playbook", "Battlecard template", "Kill-sheet template", "Pricing-tier grid template", "Feature parity matrix template", "Weekly digest template", "QBR deck template", "Provenance footer template".

For provenance, see `SOURCES.md`. For per-use-case SOTA mapping with confidence flags, see `reference/SOTA_USE_CASES.md`.

---

## Capability reference

### CI program tiers

- **Program-of-one** — solo PMM or strategy ops; default to self-build (Visualping + `ai-news-collectors` + `reddit-mcp` + Notion + Slack). Klue / Crayon may not be ROI-positive until the comp set hits 5+.
- **Team-of-2-to-5** — dedicated CI / PMM team; default to Klue Essentials or Crayon Standard ($15-25k/yr); self-build still covers the long tail.
- **Enterprise** — multi-PMM + dedicated CI roles; Klue Enterprise / Crayon Premium ($40k+/yr); AlphaSense seat for financial CI; Brandwatch / Talkwalker for narrative intelligence; Bombora + G2 Intent + 6sense for intent-data CI.

### Competitor scope categories

- **Direct competitors** — same product, same segment. Battlecard mandatory.
- **Indirect competitors** — different product, same job-to-be-done. Light battlecard.
- **Adjacent / substitute competitors** — different category, same customer dollar. Watch list only.
- **Potential entrants** — capability + motive (e.g., big-tech adjacent move). Watch list + escalate-on-signal.
- **Channel competitors** — same channel partner ecosystem; matters for partnership negotiations.

### Signal layer cadence (default)

| Layer | Cadence | Tool |
|---|---|---|
| Pricing pages | Daily | Visualping / Distill.io / `firecrawl-mcp` |
| Changelog / release notes | Daily | Visualping / RSS / `github-api` (OSS) |
| Homepage + key LPs | Weekly | Visualping / ChangeTower |
| Ad library (Meta / LI / TikTok / Google) | Weekly | `cli-anything` + curl per library API + `playwright-mcp` |
| Social listening (Reddit / X / GDELT) | Weekly | `reddit-mcp` + `twitter-mcp` + `cli-anything` + `gdeltdoc` |
| Reviews (G2 / TR / Capterra / Trustpilot) | Weekly | Apify Review Intelligence + `firecrawl-mcp` |
| Hiring (LinkedIn + careers page + Glassdoor) | Bi-weekly | `linkedin` skill + `firecrawl-mcp` |
| Tech stack (BuiltWith / Wappalyzer) | Monthly | `cli-anything` + python-Wappalyzer |
| M&A + funding (Crunchbase + press) | Weekly | `cli-anything` + Crunchbase API + `ai-news-collectors` |
| Patents (USPTO) | Quarterly | `uspto-mcp` |
| SEC filings | Quarterly + on filing | `sec-edgar-mcp` |
| Analyst reports (Gartner MQ / Forrester Wave) | On report drop | analyst subscription + `ai-news-collectors` |
| App store / Play Store reviews | Weekly | Sensor Tower + Apptopia + Apify |
| Exec moves | Bi-weekly | LinkedIn Sales Nav + Owler + press |

### CI delivery channels

- **Salesforce opportunity record** — battlecard surface + win-loss data card (Klue/Crayon native or Lightning component)
- **Slack channel** — hot-signal feed (`#ci-hotline` style) + weekly digest summary post
- **Weekly digest email** — exec-targeted summary; Slack channel for ICs
- **Notion / Confluence** — battlecard staging; never the primary surface for reps
- **Klue Insider / Crayon Sales App** — native deal-level surface if licensed
- **Steve / northr / Insiteful** — alternative AI-CI delivery tools

### Battlecard sections (canonical)

1. **Positioning differentiator** (1 sentence — how we win vs them)
2. **Top 3 objections + rebuttals** (rep-facing — load-bearing surface)
3. **Latest deal intel** (wins / losses / at-risk in last 90 days)
4. **Feature parity snapshot** (where we lead / where they lead / contested)
5. **Pricing leverage** (their tier / our tier / typical discount needed)
6. **Kill-shots** (their proven weakness — review-mined)
7. **Traps to avoid** (claims that get fact-checked by a savvy buyer)
8. **Refresh-on-signal rule** (what triggers a re-author pass)
9. **Provenance footer** (source URLs + retrieval dates + ethics class)

### Kill-sheet sections (canonical)

1. **Header** — competitor + last refresh date + PMM approval status
2. **3-5 "When prospect says X" → "Rep says Y"** rebuttals with:
   - Public-source citation per claim
   - PMM-approved language for our differentiator
   - Public-evidence for their gap
3. **Proof-points** — case studies / G2 quotes / public benchmarks
4. **Provenance footer**

---

## Continuous monitoring playbook

### Step 1: Scope the comp set
- 3-5 direct competitors maximum for a starter program (each adds ongoing cost)
- 2-3 indirect competitors on watch list
- 1-2 potential entrants flagged
- Adjust quarterly; comp sets drift

### Step 2: Decide signal layers
- For each competitor, choose the layers that drive deals in your category (pricing for cost-sensitive, changelog for fast-moving feature parity, ad library for marketing-led categories, hiring for engineering-talent signals)
- Map each layer to a tool (table in Capability reference above)

### Step 3: Configure tools
- Visualping / Distill.io: 1 monitor per pricing URL + 1 per changelog URL + 1 per homepage
- `firecrawl-mcp`: structured JSON pulls for reviews + case studies + pricing
- `ai-news-collectors`: per-competitor press feed
- `reddit-mcp` / `twitter-mcp`: per-competitor search queries
- `slack-mcp`: webhook destination for hot signals

### Step 4: Wire delivery
- Slack channel `#ci-hotline` for hot signals (pricing change, exec move, M&A, analyst report)
- Slack channel `#ci-digest` for weekly summary
- Salesforce battlecard surface (Klue / Crayon component or Lightning component)
- Weekly digest email scheduled via `gmail-mcp`

### Step 5: Define refresh-on-signal rules
- Battlecard auto-flag for re-author when: changelog ships / pricing page diffs / G2 review batch (>3 new) / exec move / earnings call / new analyst report
- Kill-sheet auto-flag for refresh when: G2 review batch / win-loss interview / PMM approval expires

### Step 6: Audit signal-to-noise quarterly
- Cull noisy monitors (font-color changes etc.)
- Add new signal types as the category evolves
- Drop competitors that haven't been in a deal in 2 quarters

---

## Battlecard authoring playbook

### Step 1: Gather inputs
- Their positioning (homepage hero + 2-3 LPs)
- Their feature set (changelog + product pages + GitHub if OSS)
- Their pricing-tier shape (pricing page + Reddit / G2 chatter for gated tiers)
- Their top complaints (G2 / TrustRadius / Capterra reviews — top 5 negative themes)
- Their top praises (top 5 positive themes — what they actually do well)
- Win/loss themes from your CRM (last 4 quarters competitive deals)
- PMM-approved differentiator language

### Step 2: Author the 1-screen first pane
- 1-sentence positioning differentiator
- Top 3 objections + 1-2-sentence rebuttals each
- Latest deal intel (wins / losses / at-risk count, last 90 days)
- Pricing snapshot (their entry tier $ vs our equivalent)

### Step 3: Author the drawer content
- SWOT (strengths from positive reviews, weaknesses from negative, opportunities from gaps, threats from their trajectory)
- Feature parity matrix snapshot
- Message archive (their last 5 LP / blog / ad messages with date)
- Win/loss theme summary (top 3 won-because, top 3 lost-because)

### Step 4: Define refresh trigger
- Always: "Refresh when [release / pricing diff / new G2 batch / exec move / win-loss interview]"
- Document in the battlecard footer

### Step 5: Surface in Salesforce + Slack
- Klue / Crayon API insert if licensed
- Lightning component or custom Visualforce panel if self-built
- Notion as staging only

### Step 6: Measure adoption
- Battlecard open-rate per deal (Klue / Crayon native or Salesforce activity log)
- Competitive win-rate trend by competitor
- CI-influenced revenue (closed-won where rep cites CI use)

---

## Kill-sheet playbook

### Step 1: Mine reviews
- Scrape last 90 days of G2 + TrustRadius + Capterra + Trustpilot reviews (via Apify Review Intelligence or `firecrawl-mcp`)
- LLM theme-extract: top 5 negative + top 5 positive themes
- Note rejection rate context (TrustRadius 60% rejection — signal-per-review higher; G2 broader volume — statistical reliability)

### Step 2: Cross-reference with our differentiators
- For each negative theme, identify whether our product addresses it
- Match to PMM-approved differentiator language
- Triangulate evidence: public benchmark / case study / G2 review of ours

### Step 3: Author rebuttals
- "When prospect says: [verbatim or near-verbatim from their G2 review theme]"
- "Rep says: [PMM-approved differentiator framing + public evidence + soft close]"
- 3-5 rebuttals per kill sheet (not 20 — load-bearing only)

### Step 4: Provenance + PMM approval
- Source URL + retrieval date per claim
- PMM sign-off date in header
- Refresh trigger: new G2 batch (>5 reviews) / win-loss theme shift / PMM language update

---

## Win-loss CI playbook

### Step 1: Queue interviews
- Filter Salesforce: closed-won + closed-lost in last quarter where competitor field is set
- Aim for 3-5 won + 3-5 lost per primary competitor per quarter
- Reach out via buyer-research vendor (Klue Win/Loss, ClozeLoop, Primary Intelligence) or self-run

### Step 2: Interview structure (15-20 min)
- Why they bought (or didn't)
- Top 3 evaluation criteria
- Top 3 strengths / weaknesses of our product
- Top 3 strengths / weaknesses of competitor
- What would change their decision
- Champion / detractor identification

### Step 3: Transcribe + thematic-code
- Whisper / OpenAI Whisper API for transcription
- LLM thematic-coding pass: 2-3 themes per interview, not 10
- Tag: won-because / lost-because / objection / champion-quote / detractor-quote

### Step 4: Push to Salesforce + Klue Win/Loss
- Klue Win/Loss API insert if licensed (auto-attaches to opportunity)
- Otherwise: Salesforce custom object + Notion mirror for searchability

### Step 5: Surface back to battlecard
- Within 1 week of interview, update competitor battlecard's "latest deal intel" + objection-rebuttal language
- Update kill-sheet on quarterly cycle from accumulated themes
- Flag PMM-approval-needed for any new differentiator claims

---

## War games playbook

### Step 1: Scenario definition
- "Competitor X attacks us in segment Y" (e.g., "Salesforce announces SMB pricing tier 50% below ours")
- "Major economic shift" (e.g., "AI inference cost drops 10x — does that re-shape competitive positioning?")
- "Competitor partnership / acquisition" (e.g., "Competitor acquires our largest channel partner")

### Step 2: Pre-mortem (divergent generation)
- `brainstorming` skill: ≥5 attack vectors per scenario
- For each vector, list: trigger signals, lead time, segment impact, deal economics impact

### Step 3: Red-team responses
- For each attack vector, design our response (price match / unbundle / partner / launch counter-feature / message-shift)
- `gemini` adversarial cross-check: "what's wrong with this response?"
- Document decision tree (if signal X → trigger response Y)

### Step 4: Playbook deliverable
- `pptx` deck: scenario, attack vectors, response decision tree, signal triggers, owners
- Leadership review session; post-review adjustments
- Slack alert config: which signal triggers which playbook auto-activation

### Step 5: Quarterly re-run
- Re-run top 2-3 war games per quarter with new signals from monitoring
- Update playbook on any executed response (post-mortem learning)

---

## Pricing intelligence playbook

### Step 1: Configure pricing-page monitoring
- Visualping / Distill.io / ChangeTower element-level monitor on:
  - Per-tier $ amount
  - Per-tier feature inclusion list
  - Per-tier seat/user/usage quota
  - Add-on / upsell items
  - Discount / promo banner
- 1-day cadence default; hourly during pricing-change rumor periods

### Step 2: Triangulate gated quote-only tiers
- Reddit search (`reddit-mcp`) for pricing chatter
- G2 review reviewer-disclosed pricing
- Glassdoor salary leak (ToS-grey — flag in deliverable)
- Sales call notes from CRM (legitimate internal source)
- LinkedIn enterprise-buyer testimonials (sometimes price-disclosing)

### Step 3: Build per-competitor per-tier grid
- `xlsx`: rows = competitors, columns = tier name / $ / quota / add-on / discount / last-verified
- Each cell dated with retrieval timestamp
- Color-code: confirmed (>2 sources) / inferred (1 source + reasoning) / unknown (gated)

### Step 4: Weekly diff digest
- Compare current grid to prior week
- Slack hot alert on material change (>10% price move, new tier added, key feature gated)
- Quarterly comprehensive grid refresh

---

## Product teardown playbook

### Step 1: Pre-teardown
- Confirm trial-signup ToS permits the use; document if blocked
- Set up isolated test account with rep's real ID (per SCIP)
- `playwright-mcp` recording session prep

### Step 2: Walkthrough capture
- Onboarding: every screen captured + DOM + timing
- Primary jobs: walk through each top-level job-to-be-done
- Empty state: what does a brand-new account see?
- Power user state: what does an active account see after 30 days?
- Edge cases: error states, gated features, upgrade prompts

### Step 3: Reverse-engineer the IA
- Map the navigation tree
- Map the state machine for primary workflows
- Identify feature dependencies (Feature A requires Feature B to be enabled)
- Note progressive-disclosure patterns

### Step 4: Activation-moment timing
- For each primary job, time how long to first value
- Compare to our equivalent timing
- Flag activation-flow design moves (auto-import, sample data, guided tour, etc.)

### Step 5: Back-fill non-visible features
- Engineering blog: architecture choices
- GitHub OSS repos: SDK / library details
- Patents (`uspto-mcp`): R&D direction
- Conference talks: roadmap signals
- Job posts: hiring direction = capability investment direction

### Step 6: Deliverable
- `pptx` teardown deck: IA map, state machine, activation timing, feature inventory, non-visible inferences
- Pair with feature parity matrix update
- Surface key findings to competitor battlecard

---

## Hot-deals CI playbook

### Step 1: Trigger
- Salesforce opportunity field "Competitor" set or changed
- `salesforce-api` webhook → CI agent

### Step 2: Pull deal-specific signals
- This account's intent signals (Bombora / G2 / 6sense — if licensed; LinkedIn engagement otherwise)
- This competitor's recent wins/losses in this segment (last 90 days)
- This contact's LinkedIn history with competitor (current/former employee? deal history?)
- This account's tech stack (BuiltWith / Wappalyzer)
- This account's recent press / hiring signals

### Step 3: Render micro-battlecard (<1 screen)
- 6-8 bullets max
- Lead: deal-specific intel ("This account just acquired Company Y who uses [competitor]")
- Top 1-2 objections likely + rebuttal
- Pricing leverage specific to deal size

### Step 4: Deliver
- Salesforce activity record insert
- Slack-ping the AE in their DM
- Track open + deal outcome → CI-program-metrics

---

## Analyst-relations playbook

### Step 1: Track release calendar
- Gartner: per-category MQ usually annual; Critical Capabilities sometimes off-cycle
- Forrester: Wave per-category usually annual or every 18 months
- IDC: MarketScape per-category
- Constellation: ShortList quarterly
- 451 Research, Omdia, others per category

### Step 2: On report drop
- Diff competitor position against prior cycle:
  - Axis movement (Vision ↔ Execution / Strategy ↔ Current Offering)
  - Quadrant change (Leader / Challenger / Visionary / Niche)
  - New dimensions added or retired
- Capture quotable analyst lines per competitor
- Flag: did competitor newly become a Leader? Did we?

### Step 3: Pair to feature parity matrix
- Update parity matrix with analyst-graded capability dimensions
- Flag where analyst grading diverges from our internal grading

### Step 4: Deliverable
- Standalone analyst-relations brief per report drop
- Update competitor battlecards with quotable analyst lines
- Quarterly analyst-relations roll-up to leadership

---

## Ethical CI playbook (SCIP code)

### Hard nos (refuse and flag)

- **Pretexting** — pretending to be a prospect, journalist, analyst, or investor when you're not
- **Identity misrepresentation** — using a fake name, fake company, fake role in any outreach
- **Login-walled scraping** — pulling data from behind authentication the agent doesn't have legitimate access to
- **Recording without consent** — call recordings, meeting recordings, etc. without explicit consent
- **Insider info** — paying employees, accepting leaked docs, dumpster-diving (literal or metaphorical)
- **Social engineering** — manipulating people to reveal info they wouldn't normally share

### Soft cautions (flag, don't auto-decline — defer to user)

- **Accidentally-public docs** — Google Drive links shared publicly by mistake; technically public, ethically grey
- **Glassdoor scrape** — ToS may prohibit; flag in deliverable's ethics-class footer
- **Aggressive trial-account use** — multiple trial signups under different emails (ToS-violation in many)
- **Gated community infiltration** — joining a private Slack / Discord / forum for CI; flag if relevant ToS prohibits

### SCIP-approved methods (default)

- Public website content (homepage, LPs, pricing, blog, docs, changelog, careers)
- Public review platforms (G2, TrustRadius, Capterra, Trustpilot, Glassdoor for employee sentiment)
- Public regulatory filings (SEC, USPTO, EU filings, patents)
- Public press releases + analyst reports
- Trial signups with rep's real ID (where ToS permits)
- Buyer-interview vendors (Klue Win/Loss, ClozeLoop, Primary Intelligence)
- Public social posts (LinkedIn, X, Reddit, dev-twitter)
- Public conference talks + recordings
- Public job posts on competitor's careers page

### Per-deliverable provenance footer (mandatory)

```
SOURCES:
- [source category] [URL] [retrieval date] [ethics class]
- public-page  https://competitor.com/pricing  2026-06-09  public
- G2 review     https://www.g2.com/products/x/reviews/12345  2026-06-08  public
- LI public     https://linkedin.com/in/exec  2026-06-07  public
- glassdoor     https://www.glassdoor.com/...  2026-06-07  ToS-grey-flagged
- SEC filing    https://www.sec.gov/...  2026-04-30  public
```

---

## Antipattern catalog

### Antipattern 1: One-time CI deep-dive instead of monitoring
**BAD:** "Q3 Competitor Landscape Report" — 80-page PDF, takes 6 weeks to author, stale before it ships.

**Why it's bad:** Material competitor moves happen weekly. A quarterly report misses the deals it was supposed to inform. Reps don't open 80-page PDFs.

**GOOD:** Continuous monitoring + battlecards refreshed on signal. Quarterly QBR for the CI program metrics, not for the CI content.

### Antipattern 2: Battlecard with 30 bullets per pane
**BAD:** A "comprehensive" battlecard that includes everything anyone might ever ask about the competitor.

**Why it's bad:** Reps under deal pressure scan, not read. 30 bullets = 0 bullets in actual deal use.

**GOOD:** 1-screen first pane with 6-8 load-bearing bullets (positioning, top-3 objections + rebuttals, latest deal intel, pricing snapshot). Depth in drawers.

### Antipattern 3: "We heard" claims without public-source citation
**BAD:** "Their support is terrible / they're about to lose their CTO / they're getting acquired"

**Why it's bad:** Unverifiable. Embarrasses the rep when a buyer fact-checks. Erodes battlecard credibility long-term.

**GOOD:** Every claim has a public-source URL + retrieval date. If the claim is unverifiable, hold it.

### Antipattern 4: CI delivered only in Notion
**BAD:** Beautiful Notion workspace with per-competitor pages reps never open because they don't live in Notion.

**Why it's bad:** Adoption is the only metric that matters. Reps work in Salesforce + Slack + Gmail.

**GOOD:** Battlecard surfaces in Salesforce opportunity record + Slack `#ci-hotline` for hot signals + weekly digest email. Notion is staging.

### Antipattern 5: Pretexting to access competitor sales calls
**BAD:** Faking a prospect identity, scheduling a competitor demo to get pricing + product walkthrough.

**Why it's bad:** SCIP violation, identity misrepresentation, legal exposure, ethically indefensible.

**GOOD:** Trial signup with rep's real ID (where ToS permits) + buyer-interview vendor + win/loss interviews + public review mining. Covers >95% of the same signal ethically.

### Antipattern 6: Single-source kill-sheet rebuttals
**BAD:** "Their support is slow" sourced from one G2 review.

**Why it's bad:** A single complaint is anecdote. Buyer fact-checks → rep loses credibility.

**GOOD:** Two-source minimum — multiple G2 reviews + Trustpilot + public NPS proxy. Cite all sources. Flag if you can only find one source.

### Antipattern 7: Battlecard without a refresh trigger
**BAD:** Battlecard authored Q1, never refreshed; competitor shipped 3 releases, did a pricing change, won a Gartner MQ Leader badge.

**Why it's bad:** Stale battlecards lose deals. Reps stop trusting CI when they're caught with outdated info.

**GOOD:** Every battlecard has an explicit "Refresh when X" rule. Refresh-on-signal beats refresh-on-schedule.

### Antipattern 8: Ignoring CI program metrics
**BAD:** CI program runs for a year; nobody can quantify what it returned.

**Why it's bad:** First budget cycle, the program gets cut. CI without ROI is shelfware.

**GOOD:** Quarterly QBR: battlecard open-rate per rep × competitive win-rate trend × CI-influenced revenue. Tell the ROI story.

---

## Reference patterns

### Pattern: Refresh-on-signal trigger config

```yaml
competitor: acme-corp
refresh_triggers:
  - signal: changelog_diff
    source: visualping_monitor_id_12345
    cadence: daily
    action: notify_pmm + flag_battlecard_pane_4
  - signal: pricing_page_diff
    source: distill_monitor_id_67890
    cadence: hourly
    action: slack_alert_#ci-hotline + flag_battlecard_pane_5
  - signal: g2_review_batch_gt_3
    source: apify_review_intel_pipe
    cadence: weekly
    action: flag_kill_sheet_refresh
  - signal: exec_change
    source: owler_api + linkedin_sales_nav
    cadence: bi_weekly
    action: flash_brief + flag_battlecard_pane_3
  - signal: earnings_call
    source: sec_edgar_8k_filing
    cadence: quarterly
    action: flash_brief
```

### Pattern: Provenance footer (auto-generated)

```
─────────────────────────────────────────
SOURCES (last refresh: 2026-06-09)
─────────────────────────────────────────
• competitor.com/pricing (public-page, 2026-06-08)
• G2 review #45678 (public, 2026-06-07)
• G2 review #45712 (public, 2026-06-07)
• competitor.com/changelog (public-page, 2026-06-09)
• USPTO patent #11,234,567 (public, 2026-05-30)
• SEC EDGAR 10-Q FY2026Q1 (public, 2026-05-15)
• LinkedIn public post @ExecName (public, 2026-06-05)
• reddit.com/r/sales thread (public-anonymous-OK, 2026-06-03)
─────────────────────────────────────────
ETHICS CLASS: public-source-only · SCIP-compliant
PMM APPROVED: yes (signoff: 2026-06-01, @pmm-lead)
```

### Pattern: Two-source triangulation

For any kill-sheet rebuttal claim, two-source minimum:

```
CLAIM: Acme's customer support response time exceeds 48 hours
SOURCES:
- 4 of last 10 G2 reviews mention >48hr response (G2 review #45678, 45712, 45734, 45756)
- Trustpilot 3-star reviews: "support takes days" (Trustpilot review #88991)
- Reddit thread r/saas: 12 comments on slow Acme support (reddit post abc123)
TRIANGULATION: ≥3 independent sources ✓
PMM APPROVED: yes
```

---

## SOTA tool reference (June 2026)

Per-tool quick reference. Each entry: when to use, primary endpoint / install, source. Detailed recipes live in the bundled skill packs at `skills/<name>/SKILL.md` — heading text below maps 1:1 to the skill folder name.

### Klue (skill: `continuous-competitor-monitoring-klue-kompyte-crayon`)

- **When:** dedicated CI platform, best-in-class battlecard + Salesforce integration + win/loss. Highest G2 rating (4.8/5).
- **Endpoint:** REST API + Salesforce native app + Slack app. $15-40k/yr enterprise. Klue Win/Loss bundled in higher tiers.
- **Source:** https://klue.com/ · https://klue.com/salesforce
- **Skill:** `skills/continuous-competitor-monitoring-klue-kompyte-crayon/SKILL.md` — paid Klue path + free self-build alternative.

### Crayon (skill: `continuous-competitor-monitoring-klue-kompyte-crayon`)

- **When:** broadest monitoring depth — websites + social + jobs + patents + app reviews + pricing pages.
- **Endpoint:** REST API + Salesforce app + Slack app. $15-40k/yr enterprise.
- **Source:** https://www.autobound.ai/blog/top-15-competitive-intelligence-tools-2026

### Kompyte (skill: `continuous-competitor-monitoring-klue-kompyte-crayon`)

- **When:** website + digital monitoring + battlecards; now part of Semrush. Mid-market focus.
- **Endpoint:** REST API. Kompyte Essentials from $300/yr.
- **Source:** https://www.kompyte.com/

### Visualping (skill: `competitor-pricing-page-visualping-distill`)

- **When:** visual + element-level monitoring on pricing pages, changelogs, LPs. Free tier 5 monitors.
- **Endpoint:** `curl https://api.visualping.io/...` (REST + webhook). Pricing from $13/mo.
- **Source:** https://visualping.io/
- **Skill:** `skills/competitor-pricing-page-visualping-distill/SKILL.md`

### Distill.io (skill: `competitor-pricing-page-visualping-distill`)

- **When:** granular element-level monitoring (specific price element, specific feature row). Free tier 25 monitors.
- **Endpoint:** REST + webhook. Pricing from $9/mo.
- **Source:** https://distill.io/

### ChangeTower (skill: `competitor-pricing-page-visualping-distill`)

- **When:** audit-friendly text + HTML + visual change tracking. Compliance / SEO / legal teams.
- **Endpoint:** REST + webhook. From $79/mo, Enterprise $299+/mo.
- **Source:** https://changetower.com/

### Wachete (skill: `competitor-pricing-page-visualping-distill`)

- **When:** monitoring behind logins / client portals / PDF / DOCX (with recipient's legit credentials).
- **Endpoint:** REST + email digest. From $5/mo.
- **Source:** https://www.wachete.com/

### BuiltWith (skill: `competitor-tech-stack-builtwith-wappalyzer`)

- **When:** historical + market-scale tech-stack research. 414M indexed domains, deep history. Best for prospect-list filtering by tech.
- **Endpoint:** REST API. Basic from $295/mo; full API access requires Team $995+/mo.
- **Source:** https://builtwith.com/

### Wappalyzer (skill: `competitor-tech-stack-builtwith-wappalyzer`)

- **When:** browse-time fingerprint on single sites; faster + more accurate frontend detection.
- **Install:** `pip install python-Wappalyzer` for self-hosted; Wappalyzer paid plans from $450/mo for API.
- **Source:** https://www.wappalyzer.com/

### DetectZeStack (skill: `competitor-tech-stack-builtwith-wappalyzer`)

- **When:** 60-90x cheaper Wappalyzer alternative; Wappalyzer fingerprinting + DNS CNAME + TLS + custom headers. $15/mo for 25k requests.
- **Endpoint:** REST.
- **Source:** detectzestack.com (per source comparison)

### Apify Review Intelligence (skill: `competitor-review-g2-trustradius-capterra`)

- **When:** scrape G2 + TrustRadius + Capterra + Trustpilot reviews structured for analysis. Pay-per-event.
- **Endpoint:** Apify API. Pricing: pay-per-run.
- **Source:** https://apify.com/ramsford/review-intelligence-agent

### PageCrawl (skill: `competitor-review-g2-trustradius-capterra`)

- **When:** review-velocity alerts on G2 / Trustpilot / Capterra. From $8/mo.
- **Endpoint:** webhook + email alerts.
- **Source:** https://pagecrawl.io/blog/trustpilot-g2-capterra-review-velocity-alerts

### G2 / Capterra / TrustRadius / Trustpilot / Glassdoor

- **When:** public review monitoring. **Post-Feb-2026 consolidation:** G2 acquired Capterra + Software Advice + GetApp from Gartner; combined ~55-58% of global software-review influence. TrustRadius retains independence + 60% rejection rate (signal-per-review higher).
- **Endpoint:** Apify / `firecrawl-mcp` for direct scraping; PageCrawl for velocity; LLM theme extraction for analysis.
- **Source:** https://www.aikenhouse.com/post/the-best-software-review-platforms-in-2026

### Bombora (skill: `intent-data-bombora-g2-zoominfo`)

- **When:** category-level intent signal — 5,000-site B2B media co-op, 10M+ companies covered. Top-of-funnel account discovery.
- **Endpoint:** Company Surge REST API. Pricing from ~$25k/yr.
- **Source:** https://bombora.com/ · https://www.growthspreeofficial.com/blogs/buyer-intent-signals-bombora-g2-zoominfo-b2b-2026

### G2 Buyer Intent (skill: `intent-data-bombora-g2-zoominfo`)

- **When:** vendor-specific account-level signal ("Acme viewed your category 3x this week"). Late-funnel.
- **Endpoint:** REST + webhook. Pricing ~$15k+/yr.
- **Source:** https://www.g2.com/products/g2-buyer-intent

### ZoomInfo Intent (skill: `intent-data-bombora-g2-zoominfo`)

- **When:** CRM-native topic tracking + 210M+ IP-to-Org pairings.
- **Endpoint:** REST API. Enterprise pricing.
- **Source:** https://pipeline.zoominfo.com/sales/intent-data-platform

### 6sense (skill: `intent-data-bombora-g2-zoominfo`)

- **When:** predictive ML overlay on partner-publisher + first-party signal; Surge Insights endpoint.
- **Endpoint:** REST API. Enterprise pricing.
- **Source:** https://6sense.com/

### LinkedIn Sales Navigator (skill: `competitor-hiring-intel-linkedin-sales-nav`)

- **When:** competitor hiring intel — advanced filters (Current company / Department headcount growth / Technologies Used / Geo radius). Detect: where they're investing (eng surge), who's leaving (alumni filter), exec moves.
- **Endpoint:** LinkedIn OAuth via `linkedin` skill. Sales Nav Core ~$100/mo per seat.
- **Source:** https://sbl.so/linkedin/sales-navigator-filters-guide/

### Sensor Tower + data.ai (skill: `competitor-app-intel-sensor-tower-data-ai`)

- **When:** mobile app intelligence — downloads, revenue estimates, store rankings, SDK adoption, retention proxies. Post-2024 data.ai merger = industry standard.
- **Endpoint:** REST API. Enterprise pricing $1k-10k+/mo.
- **Source:** https://sensortower.com/

### Apptopia (skill: `competitor-app-intel-sensor-tower-data-ai`)

- **When:** alternative mobile intel; bundles more at base tier + better API access at higher tiers.
- **Endpoint:** REST API.
- **Source:** https://apptopia.com/

### Pathmatics (skill: `competitor-ad-pathmatics-spyfu-semrush`)

- **When:** cross-channel ad spend + creative — desktop, mobile, social, video, CTV in one interface. Acquired by Sensor Tower (now part of Adyntel).
- **Endpoint:** REST API. Enterprise pricing.
- **Source:** https://sensortower.com/product/digital-advertising/pathmatics

### SpyFu (skill: `competitor-ad-pathmatics-spyfu-semrush`)

- **When:** Google search ads history + keyword research. 18+ years history, live data refresh 15s, 38 countries.
- **Endpoint:** REST API. Pricing from $39/mo.
- **Source:** https://www.spyfu.com/

### Meta Ad Library (skill: `competitor-ad-pathmatics-spyfu-semrush`)

- **When:** free official Facebook + Instagram active and historical ads. Mandatory under EU DSA + US laws for political/issue ads; commercial visible too.
- **Endpoint:** Public Graph API. Free.
- **Source:** https://www.facebook.com/ads/library

### LinkedIn Ad Library (skill: `competitor-ad-pathmatics-spyfu-semrush`)

- **When:** free official LinkedIn ads. EU + UK ads include spend bands.
- **Endpoint:** Public page + scrape via `playwright-mcp`. Free.
- **Source:** https://www.linkedin.com/ad-library/

### Google Ads Transparency Center (skill: `competitor-ad-pathmatics-spyfu-semrush`)

- **When:** free official Google ads (search, display, YouTube).
- **Endpoint:** Public page + scrape. Free.
- **Source:** https://adstransparency.google.com/

### TikTok Creative Center (skill: `competitor-ad-pathmatics-spyfu-semrush`)

- **When:** free TikTok ad creative library.
- **Endpoint:** Public page + scrape via `playwright-mcp`. Free.
- **Source:** https://library.tiktok.com/ads

### Ahrefs (skill: `competitor-seo-ahrefs-semrush-organic`)

- **When:** strongest backlink analysis + organic search competitor intel. ~15-25% accuracy on organic-search-traffic estimates above 100k sessions.
- **Endpoint:** REST API. Pricing from $500/mo.
- **Source:** https://ahrefs.com/

### SEMrush (skill: `competitor-seo-ahrefs-semrush-organic`)

- **When:** best keyword research depth + competitor keyword overlap + share-of-voice + Top Pages for LP analysis.
- **Endpoint:** REST API. Pricing from $130/mo; .Trends from $289/mo.
- **Source:** https://www.semrush.com/

### Similarweb (skill: `competitor-seo-ahrefs-semrush-organic`)

- **When:** high-level traffic share + market intelligence. ~40-70% off for small sites; better for enterprise-scale comparisons.
- **Endpoint:** REST API. Pricing from $500/mo minimum, $2-10k+/mo typical.
- **Source:** https://www.similarweb.com/

### DataForSEO (skill: `competitor-seo-ahrefs-semrush-organic`)

- **When:** most flexible pay-per-task pricing for SERP / keyword data.
- **Endpoint:** REST API. Pay-per-task.
- **Source:** https://dataforseo.com/

### Crunchbase (skill: `competitor-m-a-funding-crunchbase-pitchbook`)

- **When:** startup funding rounds + investor relationships + key personnel + acquisition activity.
- **Endpoint:** REST API. Pro from $588/yr; Basic $49/mo, Pro $99/mo for higher API limits.
- **Source:** https://data.crunchbase.com/docs/using-the-api

### PitchBook (skill: `competitor-m-a-funding-crunchbase-pitchbook`)

- **When:** VC / PE depth — 10M+ companies, deal terms, LP intelligence, M&A pipeline.
- **Endpoint:** REST API + Chrome + Excel + PowerPoint plugins. Pricing ~$12-15k/seat/yr.
- **Source:** https://pitchbook.com/

### Owler (skill: `competitor-m-a-funding-crunchbase-pitchbook`)

- **When:** org-level competitive news alerts + exec changes; 15M companies tracked.
- **Endpoint:** REST API + email alerts.
- **Source:** https://www.owler.com/

### CB Insights (skill: `competitor-m-a-funding-crunchbase-pitchbook`)

- **When:** emerging-tech intel + market maps + venture data.
- **Endpoint:** REST API. Enterprise pricing.
- **Source:** https://www.cbinsights.com/

### AlphaSense (skill: `analyst-relations-watching-gartner-forrester`)

- **When:** analyst-grade financial CI. AI-powered market intelligence search across public + private content. Gartner CMI MQ Leader 2026. Incorporated Sentieo features.
- **Endpoint:** REST API + Sharepoint/OneNote/Box/Drive integrations. Enterprise pricing.
- **Source:** https://www.alpha-sense.com/

### Brandwatch (skill component within `continuous-competitor-monitoring-klue-kompyte-crayon`)

- **When:** social listening — data volume + historical depth + Iris AI + enterprise integrations.
- **Endpoint:** REST API + streaming. Enterprise pricing $20-100k/yr.
- **Source:** https://www.brandwatch.com/

### Talkwalker (skill component within `continuous-competitor-monitoring-klue-kompyte-crayon`)

- **When:** visual brand tracking + crisis alerting + Blue Silk AI for global-language coverage.
- **Endpoint:** REST API. Enterprise pricing.
- **Source:** https://www.talkwalker.com/

### Meltwater (skill component within `continuous-competitor-monitoring-klue-kompyte-crayon`)

- **When:** press pickup + journalist + newswire coverage. Most cost-effective for media-pickup focus.
- **Endpoint:** Developer portal for enterprise data integration (listening / export / streaming).
- **Source:** https://www.meltwater.com/

### Pulsar TRAC (skill component within `continuous-competitor-monitoring-klue-kompyte-crayon`)

- **When:** audience segmentation + narrative prediction; cultural intelligence.
- **Endpoint:** REST API. Enterprise pricing.
- **Source:** https://www.pulsarplatform.com/

### Gartner Magic Quadrant + Forrester Wave (skill: `analyst-relations-watching-gartner-forrester`)

- **When:** analyst-relations watching — per-category MQ / Wave / IDC MarketScape / Constellation ShortList.
- **Endpoint:** Subscription per analyst firm ($5-30k/seat/yr); public press summary via `ai-news-collectors` + `firecrawl-mcp`.
- **Source:** https://www.gartner.com/en/research/magic-quadrant · https://go.forrester.com/research/the-forrester-wave/

### SEC EDGAR (skill: via `sec-edgar-mcp` MCP)

- **When:** public-company filings — 10-K / 10-Q / 8-K for M&A, earnings, exec compensation, risk factors. Free, 10 rps.
- **Endpoint:** `sec-edgar-mcp` MCP. Direct: `curl -A "$EDGAR_USER_AGENT" https://data.sec.gov/...`.
- **Source:** https://www.sec.gov/edgar/sec-api-documentation

### USPTO PatentsView (skill: via `uspto-mcp` MCP)

- **When:** competitor patents — R&D direction signal. Free.
- **Endpoint:** `uspto-mcp` MCP. Direct: `https://api.patentsview.org/patents/query`.
- **Source:** https://data.uspto.gov/apis/getting-started

### Visualping vs Distill.io vs ChangeTower vs Wachete vs PageCrawl

| Tool | Best for | Free tier | Pricing |
|---|---|---|---|
| Visualping | Visual change tracking on pricing / LP | 5 monitors | $13+/mo |
| Distill.io | Granular element-level | 25 monitors | $9+/mo |
| ChangeTower | Audit-friendly compliance | trial | $79+/mo |
| Wachete | Behind-login + PDF/DOCX | trial | $5+/mo |
| PageCrawl | Review velocity alerts | trial | $8+/mo |

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| "Set up monitoring on these 5 competitors" | `continuous-competitor-monitoring-klue-kompyte-crayon` | Klue/Crayon path if licensed; else free self-build |
| "Build me a battlecard for Acme Corp" | `battlecard-authoring-maintenance` | Author + surface in Salesforce + Slack |
| "Refresh the kill sheet for X" | `kill-sheet-objection-rebuttals` | Mine G2/TR/Capterra reviews first |
| "Track win/loss data for competitive deals" | `win-loss-ci-integration-klue-insider` | Klue Win/Loss if licensed; else Whisper + LLM coding + Salesforce |
| "Diff their pricing page weekly" | `competitor-pricing-page-visualping-distill` | Visualping/Distill.io element-level |
| "Build feature parity matrix" | `feature-parity-tracking` | YAML/CSV + changelog watch |
| "What's their tech stack?" | `competitor-tech-stack-builtwith-wappalyzer` | BuiltWith + python-Wappalyzer |
| "What are their ads running?" | `competitor-ad-pathmatics-spyfu-semrush` | Meta + LinkedIn + Google + TikTok libraries first (free) |
| "Compare our SEO position to theirs" | `competitor-seo-ahrefs-semrush-organic` | Ahrefs + SEMrush if licensed |
| "Track their mobile app rankings" | `competitor-app-intel-sensor-tower-data-ai` | Sensor Tower + Apptopia |
| "Monitor their G2/TR/Capterra reviews" | `competitor-review-g2-trustradius-capterra` | Apify Review Intelligence + theme extraction |
| "Track their M&A and funding" | `competitor-m-a-funding-crunchbase-pitchbook` | Crunchbase + SEC EDGAR fallback |
| "Who's hiring at competitor X?" | `competitor-hiring-intel-linkedin-sales-nav` | Sales Nav saved-search + careers-page scrape |
| "Set up intent-data alerts" | `intent-data-bombora-g2-zoominfo` | Requires paid Bombora/G2/ZoomInfo/6sense key |
| "Run a war-game session on scenario X" | `war-games-competitive-mock-scenarios` | Pre-mortem ≥5 attack vectors, then red-team |
| "Generate deal-level CI for opportunity X" | `hot-deals-ci-deal-level` | Salesforce trigger → micro-battlecard |
| "Track the new Gartner MQ release" | `analyst-relations-watching-gartner-forrester` | Per-report diff + competitor position change |
| "Show me CI program metrics" | `ci-program-metrics-adoption-rate` | Open-rate × win-rate × influenced revenue |
| "Where do the battlecards live?" | `ci-delivery-slack-crm-klue-insider` | Salesforce + Slack + weekly digest |
| "Do a full product teardown of competitor X" | `competitor-product-teardown-depth` | Trial signup + Playwright + cross-reference public sources |
| "Is this method SCIP-compliant?" | `ethical-public-source-methodology` | Public-source only + provenance footer |

---

## Battlecard template

```
═══════════════════════════════════════════════════════════
COMPETITOR: [Name]
Last refresh: [date] · PMM approved: [date] · Open rate: [N% L30D]
Refresh-on-signal: [list of triggers]
═══════════════════════════════════════════════════════════

▸ POSITIONING DIFFERENTIATOR (1 sentence)
   [How we win against them in 1 line]

▸ TOP 3 OBJECTIONS + REBUTTALS
   1. "[Verbatim or near-verbatim from their pitch / G2 reviews]"
      → [PMM-approved rebuttal, 1-2 sentences, source-cited]
   2. "[...]"
      → [...]
   3. "[...]"
      → [...]

▸ LATEST DEAL INTEL (last 90 days)
   Wins: [N]   Losses: [N]   At-risk: [N]
   Top win reason: [theme]
   Top loss reason: [theme]
   Recent quote: "[champion or detractor verbatim]"

▸ PRICING SNAPSHOT
   Their entry tier: $[X]/seat (last verified [date])
   Our equivalent tier: $[Y]/seat
   Typical discount needed to win: [N]%

═══════════════════════════════════════════════════════════
▾ DRAWER: SWOT
[Strengths / Weaknesses / Opportunities / Threats — review-mined]

▾ DRAWER: Feature parity matrix
[xlsx link to per-feature comparison]

▾ DRAWER: Message archive
[Last 5 LP / blog / ad messages with date]

▾ DRAWER: Win/loss themes
[Top 3 won-because / Top 3 lost-because]

═══════════════════════════════════════════════════════════
SOURCES (provenance footer auto-generated — see Pattern above)
═══════════════════════════════════════════════════════════
```

## Kill-sheet template

```
═══════════════════════════════════════════════════════════
KILL SHEET — vs [Competitor]
Last refresh: [date] · PMM approved: [date]
═══════════════════════════════════════════════════════════

▸ When prospect says: "[Objection 1]"
   Rep says: "[PMM-approved rebuttal with public evidence]"
   Sources: [G2 #/Trustpilot #/SEC filing]

▸ When prospect says: "[Objection 2]"
   Rep says: "[Rebuttal]"
   Sources: [URLs]

▸ When prospect says: "[Objection 3]"
   Rep says: "[Rebuttal]"
   Sources: [URLs]

▸ Proof-points
   - [Case study link]
   - [G2 quote vs our differentiator]
   - [Public benchmark]

═══════════════════════════════════════════════════════════
SOURCES (provenance footer)
═══════════════════════════════════════════════════════════
```

## Pricing-tier grid template

```
xlsx structure (per competitor):
| Tier | $/seat | $/mo | Quota | Add-ons | Discount | Last verified |
|---|---|---|---|---|---|---|
| Free | $0 | $0 | [limits] | [list] | n/a | [date] |
| Starter | $X | $Y | [limits] | [list] | up to N% | [date] |
| Pro | $X | $Y | [limits] | [list] | up to N% | [date] |
| Enterprise | quote | quote | unlimited | [list] | varies | [date — confidence flag] |

Each cell:
  · color-coded: confirmed (>2 sources) / inferred (1 + reasoning) / unknown (gated)
  · source URL on hover
  · retrieval date
```

## Feature parity matrix template

```
xlsx structure:
| Feature | Us | Competitor A | Competitor B | Competitor C | Confidence | Source | Date |
|---|---|---|---|---|---|---|---|
| Feature 1 | ✓ | ✓ | ✗ | ⚠ partial | high | [URL] | [date] |
| Feature 2 | ✓ | ✗ | ✓ | ✓ | high | [URL] | [date] |
| Feature 3 | ⚠ roadmap | ✓ | ✗ | ✗ | medium | [URL] | [date] |

Confidence flags:
  · high — verified in product or official docs
  · medium — inferred from changelog / case study / G2 review
  · low — single-source claim
```

## Weekly digest template

```
═══════════════════════════════════════════════════════════
CI WEEKLY DIGEST — Week of [date]
═══════════════════════════════════════════════════════════

▸ TOP 5 COMPETITOR MOVES THIS WEEK
   1. [Competitor A] [classified: release | pricing | messaging | hiring | M&A]
      Impact: [1-line deal economics impact]
      Battlecard delta: [updated pane N]
      Source: [URL] (retrieved [date])
   2. [...]
   ...

▸ BATTLECARD UPDATES
   - [Competitor A] battlecard pane 4 refreshed (changelog)
   - [Competitor B] battlecard pane 5 refreshed (pricing diff)

▸ KILL SHEET UPDATES
   - [Competitor C] kill sheet refreshed (G2 review batch — 5 new reviews)

▸ DEAL INTEL
   Wins this week vs competitors: [count]
   Losses this week vs competitors: [count]
   New at-risk deals: [count]

═══════════════════════════════════════════════════════════
SOURCES (provenance footer)
═══════════════════════════════════════════════════════════
```

## QBR deck template (CI program metrics)

```
pptx structure (10-15 slides):
1. Title — "CI Program QBR — Q[N] FY[YYYY]"
2. Executive summary — open-rate / win-rate / influenced revenue headline numbers
3. Battlecard open-rate per rep (top + bottom quartile callouts)
4. Battlecard open-rate per competitor
5. Competitive win-rate trend (last 4 quarters)
6. Lost-reason histogram per competitor
7. CI-influenced revenue (closed-won where rep cites CI)
8. Case study: 1-2 deals won where CI was the inflection
9. Case study: 1 deal lost where CI gap is identified
10. Quarter-over-quarter delta vs commits
11. Next quarter focus: which competitors get more depth, which lose coverage
12. CI program asks (budget, headcount, tooling)
13. Sources + methodology footer
```

---

## Closing rules

Continuous beats episodic. Sales adoption beats page count. Ethics is a constraint that turns out to bind on almost nothing useful — public sources cover ~95% of what matters in 2026. The battlecard is the product; the open-rate is the metric. SCIP code-compliant always.
