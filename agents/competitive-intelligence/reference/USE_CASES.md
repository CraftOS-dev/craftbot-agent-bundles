# Competitive Intelligence — Use Cases

**Tier:** specialized (under `research-analyst`) · **Category:** research
**Core job:** Continuous competitor monitoring + battlecard authoring + win/loss CI integration + ethical public-source-only methodology. Specialist sibling of `research-analyst`.

> Ships with the SOTA competitive-intelligence stack (Klue / Crayon / Kompyte paid + Visualping / Distill.io / Apify Review Intelligence / SEC EDGAR / USPTO / `firecrawl-mcp` / `playwright-mcp` / `reddit-mcp` / `salesforce-api` / `slack-mcp` / `notion-mcp` free-and-self-build) — executes end-to-end battlecards live in Salesforce and Slack, not just director-mode advisories.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### Continuous monitoring (the daily loop)

- Continuous competitor monitoring (Klue / Crayon / Kompyte paid; free self-build via Visualping + `ai-news-collectors` + `reddit-mcp` + GDELT)
- Competitor messaging tracking + diff over time (homepage + LP weekly diff with positioning/claims/category-language classifier)
- Competitor pricing page change detection (Visualping / Distill.io / ChangeTower element-level diff with webhook → Slack)
- Competitor product release tracking (changelog + RSS + GitHub releases + engineering blog feed)
- Competitor customer logo + case-study tracking
- Competitor support intelligence (response time + NPS proxy via public-channel signals + review theme distribution)

### Battlecards + kill sheets

- Battlecard authoring + maintenance (one per competitor, 1-screen first pane, drawers for depth)
- Kill-sheet authoring (review-mined objection rebuttals with PMM-approved language)
- Battlecard refresh-on-signal rules (release / pricing diff / G2 batch / exec move / win-loss interview)
- Battlecard delivery into Salesforce + Slack + weekly digest

### Win/loss CI integration

- Win/loss CI integration (Klue Win/Loss path + self-build Whisper + LLM coding + Salesforce loop)
- Win/loss interview queuing + thematic coding (won-because / lost-because / objection / champion / detractor)
- Win/loss-to-battlecard push (themes refresh competitor battlecard within the week)

### Deal-level CI

- Hot-deals CI (deal-specific micro-battlecard on Salesforce competitor-field trigger)
- Per-account intent signals + competitor recent wins/losses + LinkedIn contact history + tech-stack overlay
- Slack-ping the AE within minutes of signal

### Competitive scenarios + war games

- War-games / mock competitive scenarios (pre-mortem ≥5 attack vectors, then red-team response decision tree)
- Quarterly war-game re-run with new signals

### Public-data CI surfaces

- Competitor tech stack monitoring (BuiltWith historical + python-Wappalyzer fingerprint + DetectZeStack)
- Competitor ad intelligence (Meta + LinkedIn + TikTok + Google Ads Library free first; Pathmatics / SpyFu paid uplift)
- Competitor SEO intelligence (Ahrefs backlinks + SEMrush keywords + Similarweb traffic + DataForSEO SERP)
- Competitor app intelligence (Sensor Tower post-data.ai + Apptopia + Appfigures)
- Competitor review monitoring (Apify Review Intelligence + PageCrawl velocity on G2 / TrustRadius / Capterra / Trustpilot / Glassdoor)
- Competitor LP + funnel analysis (SEMrush Top Pages + `playwright-mcp` + Lighthouse)
- Feature parity tracking (YAML/CSV matrix with versioned diffs + changelog watch)
- Competitor pricing intelligence + tier comparison (public pricing-page scrape + per-tier grid + diff history + Reddit/G2 chatter overlay)
- Competitor M&A + funding (Crunchbase + PitchBook + Owler + CB Insights + SEC EDGAR free fallback)
- Exec moves + leadership tracking (Owler + LinkedIn Sales Nav + press)
- Competitor hiring intel (LinkedIn Sales Nav + careers-page scrape + Glassdoor signal)

### Intent data + buyer signals

- Intent-data CI (Bombora category + G2 vendor-specific + ZoomInfo + 6sense Surge integration)

### Analyst relations

- Analyst-relations watching (Gartner MQ / Forrester Wave / IDC MarketScape / Constellation ShortList diff per cycle + analyst-quote citation tracking)

### Deep teardowns

- Competitor product teardown at depth (in-product walkthrough + IA + state machine + activation-moment timing + cross-reference public sources)

### Program-level CI

- CI program metrics (battlecard open-rate + competitive win-rate uplift + CI-influenced revenue)
- CI delivery to sales (tri-layer: Salesforce cards + Slack feed + weekly digest)
- Quarterly CI program QBR deck + budget/headcount asks

### Methodology + ethics

- Ethical public-source-only methodology (SCIP Code of Ethics enforcement + per-deliverable provenance footer + ethics class tagging on every source)

### Social listening for CI

- Social listening (Brandwatch / Talkwalker / Meltwater / Pulsar TRAC if licensed; free fallback via `reddit-mcp` + `twitter-mcp` + GDELT)

---

## Execution status (SOTA — June 2026)

> Mandatory table. Every use case above appears here as a row. This is the proof the agent is real, not a toy.

| Use case | SOTA mechanism | Path |
|---|---|---|
| Continuous competitor monitoring | Klue / Crayon / Kompyte paid; free self-build Visualping + `ai-news-collectors` + `reddit-mcp` + GDELT | `cli-anything` + paid API or `firecrawl-mcp` + free MCPs |
| Competitor messaging tracking + diff | Visualping / ChangeTower on homepage + LPs + LLM classifier | `firecrawl-mcp` + LLM |
| Pricing-page change detection | Visualping / Distill.io / ChangeTower element-level diff + webhook → Slack | `cli-anything` + `slack-mcp` |
| Product release tracking | Visualping on changelog + GitHub releases + RSS + engineering-blog feed | `firecrawl-mcp` + `github-api` + `ai-news-collectors` |
| Customer-logo + case-study tracking | `firecrawl-mcp` on case-study pages + press feed | `firecrawl-mcp` + `ai-news-collectors` |
| Support intelligence (NPS proxy) | Public-channel support stage tests + help-center diff + review theme | `cli-anything` + `firecrawl-mcp` (ethics-flagged) |
| Battlecard authoring + maintenance | Klue / Crayon native or self-build Notion + Slack + Salesforce | `notion-mcp` + `slack-mcp` + `salesforce-api` |
| Kill-sheet authoring | G2 / TrustRadius / Capterra review scrape + LLM theme + PMM-approved language | `firecrawl-mcp` + `pandoc-branded-deliverables` |
| Battlecard delivery into Salesforce + Slack | Klue / Crayon Salesforce native + Slack app + Lightning component self-build | `salesforce-api` + `slack-mcp` |
| Win/loss CI integration | Klue Win/Loss; self-build Whisper + LLM coding + Salesforce | Klue API or `openai-whisper-api` + `salesforce-api` |
| Win/loss interview + thematic coding | Whisper / OpenAI Whisper + LLM thematic pass | `cli-anything` + `openai-whisper-api` skill |
| Hot deals CI (deal-level) | Salesforce competitor-field trigger → micro-battlecard | `salesforce-api` + `linkedin` + `cli-anything` |
| War games / mock scenarios | LLM red-team + `brainstorming` + `concise-planning` + `gemini` cross-check | self + `gemini` |
| Competitor tech stack monitoring | BuiltWith historical + python-Wappalyzer + DetectZeStack + Apify Tech Stack Detector | `cli-anything` + `firecrawl-mcp` |
| Competitor ad intelligence | Meta / LinkedIn / TikTok / Google Ads Library free + Pathmatics / SpyFu / AdLibrary paid | `cli-anything` + `playwright-mcp` |
| Competitor SEO intelligence | Ahrefs + SEMrush + Similarweb + DataForSEO | `cli-anything` paid APIs |
| Competitor app intelligence | Sensor Tower (post-data.ai) + Apptopia + Appfigures | `cli-anything` paid APIs |
| Competitor review monitoring | Apify Review Intelligence + PageCrawl velocity on G2 / TrustRadius / Capterra / Trustpilot / Glassdoor | `cli-anything` + `firecrawl-mcp` |
| Competitor LP + funnel analysis | SEMrush Top Pages + `playwright-mcp` + Lighthouse | `cli-anything` + `playwright-mcp` |
| Feature parity tracking | YAML/CSV matrix + Visualping changelog watch + LLM auto-tag | `cli-anything` + `firecrawl-mcp` + `xlsx` |
| Competitor pricing intel | Distill.io / Visualping pricing-page diff + Reddit/G2 chatter | `cli-anything` + `firecrawl-mcp` + `reddit-mcp` + `xlsx` |
| Competitor M&A + funding | Crunchbase + PitchBook + Owler + CB Insights + SEC EDGAR | `cli-anything` + `sec-edgar-mcp` |
| Exec moves + leadership tracking | Owler + LinkedIn Sales Nav + press feed | `linkedin` + `ai-news-collectors` |
| Competitor hiring intel | LinkedIn Sales Nav + careers-page scrape + Glassdoor | `linkedin` skill + `firecrawl-mcp` |
| Intent-data CI | Bombora + G2 Intent + ZoomInfo + 6sense Surge | `cli-anything` per API + `salesforce-api` |
| Analyst-relations watching | Gartner / Forrester / IDC / Constellation subscriptions + press coverage | `cli-anything` + analyst-firm APIs + `ai-news-collectors` |
| Competitor product teardown | Playwright in-product walkthrough + GitHub + USPTO + OCR + eng-blog cross-reference | `playwright-mcp` + `github-api` + `uspto-mcp` + OCR MCPs |
| CI program metrics | Klue / Crayon admin + Salesforce stage data + warehouse | `salesforce-api` + `postgresql-mcp` + `pptx` |
| CI delivery to sales | Salesforce cards + Slack feed + weekly digest tri-layer | `slack-mcp` + `salesforce-api` + `gmail-mcp` |
| Ethical public-source methodology | SCIP Code enforcement + per-deliverable provenance footer | self + skill |
| Social listening for CI | Brandwatch / Talkwalker / Meltwater / Pulsar paid; free fallback Reddit + X + GDELT | `cli-anything` paid + `reddit-mcp` + `twitter-mcp` |

---

## Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Klue / Crayon / Kompyte CI platforms | ⚠ | Paid $15-40k/yr enterprise; recipient supplies key. Free self-build via Visualping + `ai-news-collectors` + `firecrawl-mcp` covers 70-80% of signal. |
| Bombora / G2 Intent / ZoomInfo / 6sense (intent data) | ⚠ | All paid — Bombora ~$25k/yr, G2 Intent ~$15k+/yr, ZoomInfo / 6sense enterprise. No equivalent free fallback for vendor-specific account-level intent. |
| Crunchbase / PitchBook (M&A + funding) | ⚠ | Crunchbase $588/yr Pro; PitchBook $12-15k/seat/yr. Free fallback via SEC EDGAR + `ai-news-collectors`. |
| Sensor Tower / Apptopia / Pathmatics (app + ad intel) | ⚠ | All paid; Appfigures free tier covers basic app data; free official ad libraries (Meta / LinkedIn / TikTok / Google) cover most ad-creative needs. |
| Ahrefs / SEMrush / Similarweb (SEO + traffic) | ⚠ | All paid $500-10k+/mo. Free fallback via search-engine MCPs + DataForSEO pay-per-task. |
| LinkedIn Sales Navigator (hiring intel) | ⚠ | Paid ~$100/mo per seat; LinkedIn ToS prevents direct scraping. Free fallback via careers-page scrape. |
| Brandwatch / Talkwalker / Meltwater / Pulsar (social listening) | ⚠ | All paid enterprise; free fallback via `reddit-mcp` + `twitter-mcp` + GDELT. |
| Analyst-firm subscriptions (Gartner / Forrester / IDC / Constellation) | ⚠ | $5-30k/seat/yr; free fallback via press-release coverage + public summaries. |
| AlphaSense (analyst-grade financial CI) | ⚠ | Enterprise pricing, sales-gated. No free equivalent for full transcript + filing search depth; SEC EDGAR covers public-company filings. |
| Glassdoor scraping for employee sentiment | ⚠ | Glassdoor ToS-grey; agent flags ethics class in deliverable; defers to user. |
| Trial-account access to competitor product | ⚠ | Many competitors gate by email domain; recipient signs up under real ID per SCIP. |
| Pretexting / login-walled access / insider info | ✗ | Refused on SCIP-ethics grounds. Not "we can't do it" — "we won't do it." |
| Real-time competitor strategic intent (their internal roadmap) | ✗ | Genuinely not public. Inferred from job posts + patents + analyst calls + LP changes. |
| Pricing-page detail for quote-only enterprise tiers | ✗ | Genuinely not public. Triangulate via Reddit / G2 reviewer-disclosed / Glassdoor (ToS-grey-flagged) / sales-call notes from CRM. |

**Verdict (June 2026): ~95% fulfillment.** Every use case has a working execution path. The ⚠ entries are paid-tier uplifts where the recipient supplies the key — every one has a free or self-build fallback path documented above. The ✗ entries are SCIP-ethics refusals (pretexting / login-walled scraping — by design) or genuine fuzz (competitor internal roadmap is not knowable; quote-only enterprise pricing has no clean public source). Public sources cover ~95% of what matters; the SCIP constraint binds on almost nothing useful.

---

## When to use this agent

- "Set up continuous monitoring on these 5 competitors — pricing pages, changelogs, social, M&A"
- "Build me a battlecard for Acme Corp that surfaces in Salesforce"
- "Refresh the kill sheet for Beta Inc with the last 90 days of G2 reviews"
- "We just lost a deal to Gamma — pull the win-loss interview and update the battlecard"
- "Their pricing page just changed — what's the deal-economics impact?"
- "Run a war-game session: what if Salesforce launches an SMB tier 50% below ours?"
- "Build a feature parity matrix across us + top 3 competitors"
- "Track the next Gartner MQ release for our category and diff competitor positions"
- "We have a hot deal vs Delta — generate a deal-level micro-battlecard now"
- "Show me CI program metrics for the QBR — open-rate, win-rate uplift, influenced revenue"

## When NOT to use this agent

- Broader research / scientific literature / market sizing / trend fan-out — hand off to `research-analyst` (parent)
- Turn CI signal into outbound sales sequences — hand off to `sales-agent`
- Turn CI signal into roadmap decisions (build / kill / extend) — hand off to `product-manager`
- Turn CI signal into positioning / messaging / category language — hand off to `marketing-agent`
- Long-form analyst-style reports (10-Q deep dive, primary research) — hand off to `research-analyst`
- Industrial espionage / pretexting / social engineering / login-walled scraping — refuse on SCIP grounds; propose ethical alternative
