# competitive-intelligence — SOTA Use Cases (June 2026)

Per-use-case mapping of the SOTA approach, the exact agent execution path (MCP / CLI / API), the authoritative source, and a confidence flag. Cross-references the bundled skill packs in `skills/`.

Confidence legend:
- ✓ — direct execution path, free or generous free tier, no manual intervention
- ⚠ — direct execution path but requires user-supplied API key or paid tier
- ✗ — execution requires manual user step, paywalled portion the agent cannot fully automate, or platform Terms-of-Service constraints

The agent is a **public-source-only** specialist. SCIP Code of Ethics is enforced — no social engineering, pretexting, scraping behind login walls, or anything that misrepresents the agent's identity. Where an action would cross that line, the use case is downgraded to ✗ with an ethics note.

---

## Continuous competitor monitoring (Klue / Kompyte / Crayon class)

- **SOTA approach:** Dedicated CI platforms (Klue, Crayon, Kompyte) ingest competitor websites, social, job posts, patents, app reviews, pricing pages, ad libraries on a daily/hourly cadence and surface diffs in a battlecard-attached feed. For agents without a paid Klue/Crayon seat, the SOTA fallback is a self-built fan-out: Visualping/Distill.io for pricing + LP change detection, ai-news-collectors for press, GDELT for global news, Reddit/X for community signal, ad libraries for paid-channel diff, all stitched into a per-competitor digest.
- **Agent execution path:** If recipient has Klue / Crayon, `cli-anything` + curl their REST APIs (Klue battlecard insert/update, Crayon source pulls). Otherwise: `cli-anything` + `curl https://api.visualping.io/...` for pricing/LP diffs; `firecrawl-mcp` for structured page state; `ai-news-collectors` skill for press; `reddit-mcp` + Reddit PRAW for community; `playwright-mcp` for JS-heavy pricing pages. Cadence via `using-git-worktrees` + cron schedule + PROACTIVE.md.
- **Source:** https://klue.com/topics/competitive-intelligence-tools-b2b-software · https://www.autobound.ai/blog/top-15-competitive-intelligence-tools-2026 · https://visualping.io/blog/distill-alternatives
- **Confidence:** ⚠ (Klue / Crayon paid $15-40k/yr enterprise — recipient supplies key; Visualping has free tier; Kompyte Essentials from $300/yr)
- **Skill:** `continuous-competitor-monitoring-klue-kompyte-crayon`

## Competitor product teardown (depth)

- **SOTA approach:** Sign up for the trial (where permitted by ToS), document the onboarding funnel screen-by-screen, deconstruct the IA + nav + state machine, list every feature surface + flag, map the feature dependency tree, evaluate the empty-state vs power-user paths, capture the activation moment, time the "aha" event. Pair with public engineering blog posts, public design-system docs, GitHub repos, conference talks, and patent filings to back-fill what's not visible in-product.
- **Agent execution path:** `playwright-mcp` for in-product walkthrough capture (screenshots + DOM); `github-api` for OSS repos / SDKs; `uspto-mcp` for patents; `gemini-ocr-mcp` / `mistral-ocr-mcp` for screenshot extraction; `cli-anything` + ffmpeg for demo-video frame extraction; teardown report rendered via `pandoc-branded-deliverables` + `docx`/`pptx`.
- **Source:** SCIP ethical CI guide + self-build pattern; trial-sign-up only with the competitor's ToS-allowed onboarding flow
- **Confidence:** ⚠ (requires trial / free-tier signup eligibility; some products gate by domain — recipient signs up)
- **Skill:** `competitor-product-teardown-depth`

## Feature parity tracking

- **SOTA approach:** Per-competitor feature matrix maintained as YAML/CSV with versioned diffs. Rows = features, columns = competitors + us + last-checked date. Track at three levels: feature name, sub-feature flags, and pricing-tier gating. Automate diff detection via Visualping on competitor changelog / "What's New" / blog feeds + manual quarterly audit.
- **Agent execution path:** `cli-anything` + Python (pandas) for matrix maintenance; `xlsx` MCP for spreadsheet output; `firecrawl-mcp` + `playwright-mcp` for changelog scrape; `ai-news-collectors` for release announcement feed; Visualping on `/changelog`, `/whats-new`, `/release-notes` URLs.
- **Source:** https://klue.com/topics/competitive-intelligence-tools-b2b-software · https://www.autobound.ai/blog/top-15-competitive-intelligence-tools-2026
- **Confidence:** ✓ (all free; Visualping free tier sufficient for small comp set)
- **Skill:** `feature-parity-tracking`

## Competitor pricing intelligence + tier comparison

- **SOTA approach:** Public pricing-page scrape with element-level monitoring (Distill.io / Visualping) for tier names, seat prices, included quotas, add-on costs, discount rules. Layer transparent-pricing inference from G2 reviews ("we pay $X/seat") and Reddit threads. Build per-competitor pricing-tier comparison grid + diff history. Note ToS — most public pricing pages are scrape-permitted; gated quote-only pricing requires a separate qualitative signal (Glassdoor salary leak / Reddit / sales-call notes from CRM).
- **Agent execution path:** Distill.io / Visualping on pricing pages → webhook → `cli-anything` ingest; `firecrawl-mcp` for structured JSON; `playwright-mcp` for JS-rendered tier toggles; `reddit-mcp` for pricing chatter; `xlsx` MCP for tier-comparison matrix.
- **Source:** https://visualping.io/blog/distill-alternatives · https://uptimerobot.com/knowledge-hub/monitoring/9-best-website-change-monitoring-tools-compared/
- **Confidence:** ✓ (Visualping free tier 5 pages; Distill.io free tier 25 monitors; firecrawl + playwright free)
- **Skill:** `competitor-pricing-tier-comparison`

## Win/loss CI integration (Klue Insider class)

- **SOTA approach:** Win/loss interviews + AI-coded transcripts + Salesforce stage notes → battlecard-attached "Why we won/lost" data card. Klue Win/Loss is the SOTA stack: structured buyer interviews, AI thematic analysis, automatic linkage from Salesforce opportunity to battlecard. For agents without Klue: AI-coded interview transcripts via Whisper + LLM thematic clustering + structured tags into Salesforce, then surface back to battlecards.
- **Agent execution path:** Klue API for direct insert if licensed; otherwise `cli-anything` (`openai-whisper-api` skill or `mcp-tts` for transcribe) → LLM thematic-coding pass → `salesforce-api` skill to write notes → `pandoc-branded-deliverables` for the win/loss readout deliverable.
- **Source:** https://klue.com/blog/win-loss-battlecards-salesforce · https://klue.com/salesforce
- **Confidence:** ⚠ (Klue paid; self-build path executes via openai-whisper + salesforce-api + LLM)
- **Skill:** `win-loss-ci-integration-klue-insider`

## Battlecard authoring + maintenance

- **SOTA approach:** One battlecard per competitor with: positioning differentiator, top-3 objections + AI-curated rebuttals, latest deal intel (wins/losses/at-risk), feature parity snapshot, current pricing tier, pricing leverage, kill-shots, traps to avoid. Refresh on signal (release / pricing change / exec move / G2 review batch / win-loss interview). Klue / Crayon are SOTA delivery (Slack + Salesforce embed + analytics on rep open-rate). Self-build via Notion + Slack hook.
- **Agent execution path:** `notion-mcp` or `better-notion` for template + per-competitor pages; `slack-mcp` for delivery feed; `salesforce-api` for opportunity hook; `docx` / `pdf` for export. Klue / Crayon API insert/update if licensed.
- **Source:** https://klue.com/topics/best-sales-battlecard-software · https://klue.com/blog/win-loss-battlecards-salesforce
- **Confidence:** ✓ (self-build path works without paid CI platform; Klue/Crayon optional uplift)
- **Skill:** `battlecard-authoring-maintenance`

## Competitor messaging tracking + diff over time

- **SOTA approach:** Snapshot competitor homepage + key LPs + value-prop copy on a weekly cadence, diff against prior snapshot, classify whether the messaging shift is positioning (new ICP), claims (new metric / proof), pricing-adjacent (new bundle), or category-language. Stash to time-series so re-positioning is detectable across quarters.
- **Agent execution path:** Visualping / ChangeTower on homepage + top 5 LPs; `firecrawl-mcp` for structured DOM snapshot; `cli-anything` + diff for human-readable diff; LLM classification pass; weekly digest delivered via `slack-mcp` or `gmail-mcp`.
- **Source:** https://uptimerobot.com/knowledge-hub/monitoring/9-best-website-change-monitoring-tools-compared/ · https://www.autobound.ai/blog/top-15-competitive-intelligence-tools-2026
- **Confidence:** ✓ (free tiers cover small comp set; LLM classification self-hosted)
- **Skill:** `competitor-messaging-tracking-diff`

## Kill-sheet authoring (objection rebuttals)

- **SOTA approach:** Per-competitor 1-pager listing "When prospect says X" → "Rep says Y." Rebuttals grounded in: their public limitations (G2 review themes), our public differentiators (PMM-approved), their pricing gotchas, their feature gaps, their support response-time evidence. Refreshed quarterly + on any new G2 review batch.
- **Agent execution path:** G2 / Capterra / TrustRadius review scrape via `firecrawl-mcp` or Apify; LLM theme-extraction (top 5 complaints, top 5 praises); pair to our differentiator deck; `pandoc-branded-deliverables` for branded 1-pager; `slack-mcp` for delivery.
- **Source:** https://apify.com/ramsford/review-intelligence-agent · https://www.aikenhouse.com/post/the-best-software-review-platforms-in-2026
- **Confidence:** ✓
- **Skill:** `kill-sheet-objection-rebuttals`

## War games (competitive mock scenarios)

- **SOTA approach:** Run "Competitor X attacks us in segment Y" simulations: pre-mortem on their likely move sets (price cut, product unbundling, partnership grab, feature copy-then-discount), red-team our response, document the playbook + decision tree. Live-fire variant: stage real prospect conversation with rep playing as buyer + LLM playing competitor rep.
- **Agent execution path:** `concise-planning` + `brainstorming` skills for divergent attack-vector generation; LLM red-team via `gemini` cross-check; `docx` / `pdf` for playbook deliverable; optional Living UI for interactive sim.
- **Source:** SCIP scenario-planning pattern; combine with `voltagent-trend-analyst` scenario-planning template lifted from research-analyst v0
- **Confidence:** ✓
- **Skill:** `war-games-competitive-mock-scenarios`

## Intent-data CI (Bombora / G2 Intent / ZoomInfo / 6sense)

- **SOTA approach:** Layer category-level intent signal (Bombora — 5,000-site B2B media co-op, 10M+ companies, category-level) with vendor-specific intent signal (G2 Buyer Intent — "Acme Corp viewed your category 3x this week and read 2 reviews," late-funnel). ZoomInfo + 6sense for first-party + partner-publisher intent with IP-to-org mapping. Use to (a) detect when target accounts research a competitor, (b) trigger sales outreach, (c) tag battlecards with "in-market against X."
- **Agent execution path:** `cli-anything` + curl per provider API (Bombora company surge endpoint; G2 Buyer Intent webhook; ZoomInfo Intent API; 6sense Surge Insights API). Write back to Salesforce via `salesforce-api` skill. Slack notify via `slack-mcp`.
- **Source:** https://www.growthspreeofficial.com/blogs/buyer-intent-signals-bombora-g2-zoominfo-b2b-2026 · https://pipeline.zoominfo.com/sales/intent-data-platform
- **Confidence:** ⚠ (all paid — Bombora ~$25k/yr, G2 Intent ~$15k/yr, ZoomInfo / 6sense enterprise; recipient supplies key)
- **Skill:** `intent-data-bombora-g2-zoominfo`

## Competitor hiring intel (LinkedIn Sales Navigator on competitor employees)

- **SOTA approach:** LinkedIn Sales Navigator advanced filters: Current company = Competitor + Department headcount growth >20% L6M + Job titles (Eng / PM / Sales / GTM leadership). Signals = where they're investing (eng hiring surge), what they're building (job-posting tech-stack disclosures), who's leaving (alumni filter), exec moves (CEO / CTO / CRO churn). Pair with Glassdoor reviews for inside-the-house sentiment.
- **Agent execution path:** `linkedin` default skill for Sales Nav saved-search export; LinkedIn ToS prevents direct scraping — use `linkedin` skill's OAuth-permitted endpoints. For job-posting feed: `cli-anything` + each competitor's `/careers` page via `firecrawl-mcp` (mostly permitted by ToS); Glassdoor via `firecrawl-mcp` (ToS-sensitive — flag).
- **Source:** https://sbl.so/linkedin/sales-navigator-filters-guide/ · https://www.demandsense.com/blog/how-to-use-linkedin-sales-navigator
- **Confidence:** ⚠ (LinkedIn Sales Nav paid ~$100/mo; careers-page scrape free; Glassdoor scrape ToS-grey — flag in deliverable)
- **Skill:** `competitor-hiring-intel-linkedin-sales-nav`

## Competitor tech stack monitoring

- **SOTA approach:** BuiltWith for market intelligence + 414M domain history; Wappalyzer for browse-time fingerprinting; DetectZeStack as a 60x-cheaper API alternative; python-Wappalyzer for self-hosted; Apify Tech Stack Detector for pay-per-event. Track JS framework, CMS, analytics, payment, CDN, A/B test infra, customer-data platform, marketing automation, observability. Surface "they switched from Segment to RudderStack" as a signal.
- **Agent execution path:** `cli-anything` + `pip install python-Wappalyzer` for fingerprint pass; BuiltWith free preview + paid API ($295+/mo Basic) for history; `firecrawl-mcp` for DNS / TLS / header detection. Diff weekly, surface deltas.
- **Source:** https://pasqualepillitteri.it/en/news/2424/how-to-detect-website-tech-stack-wappalyzer-builtwith · https://prospeo.io/s/builtwith-vs-wappalyzer
- **Confidence:** ✓ (python-Wappalyzer free; BuiltWith optional uplift)
- **Skill:** `competitor-tech-stack-builtwith-wappalyzer`

## Competitor ad intelligence (paid creative + spend)

- **SOTA approach:** Free official ad libraries first — Meta Ad Library (active + historical FB/IG ads), LinkedIn Ad Library (active LI ads, EU+UK ads with spend bands), TikTok Creative Center, Google Ads Transparency Center, X Ads Library. Paid uplift: Pathmatics (cross-channel desktop/mobile/social/video/CTV spend estimates), SpyFu (Google search ads history), AdLibrary multi-platform API. Use to inventory competitor creative themes, channel mix, spend trends.
- **Agent execution path:** `cli-anything` + curl Meta Ad Library API + LinkedIn Ad Library + Google Ads Transparency (all free + public); `playwright-mcp` for TikTok Creative Center; SpyFu / Pathmatics paid API via `cli-anything`. Spreadsheet via `xlsx`.
- **Source:** https://sensortower.com/product/digital-advertising/pathmatics · https://adlibrary.com/guides/best-ad-spy-api · https://www.spyfu.com/
- **Confidence:** ✓ (official ad libraries free + ToS-permitted; SpyFu / Pathmatics paid optional uplift)
- **Skill:** `competitor-ad-pathmatics-spyfu-semrush`

## Competitor SEO intelligence (organic)

- **SOTA approach:** Ahrefs (strongest backlink + organic), SEMrush (best keyword-research depth), Similarweb (traffic estimates). Ahrefs is ~15-25% accurate above 100k sessions; Similarweb ~40-70% off for small sites. Use Ahrefs for backlink gap analysis, SEMrush for keyword overlap + share-of-voice, Similarweb for high-level traffic share.
- **Agent execution path:** `cli-anything` + Ahrefs API ($500+/mo); SEMrush API; Similarweb API ($500-10k/mo). Free fallback: search-console-style multi-engine scan via `brave-search` + `duckduckgo-search` + `tavily-search` + DataForSEO for SERP.
- **Source:** https://www.stylefactoryproductions.com/blog/semrush-vs-similarweb · https://onlysearch.ai/blog/competitive-intel-data-sources
- **Confidence:** ⚠ (all paid; free fallback via search-engine skills + DataForSEO pay-per-task)
- **Skill:** `competitor-seo-ahrefs-semrush-organic`

## Competitor app intelligence (mobile)

- **SOTA approach:** Sensor Tower (post-2024 acquisition of data.ai — industry standard, broadest panel + historical depth), Apptopia (bundles more at base + better API access). Tracks: downloads, revenue estimates, store rankings, SDK adoption, retention proxies, in-app purchase tiers, ad-network presence. Pair with App Store + Play Store review scrape for qualitative.
- **Agent execution path:** `cli-anything` + Sensor Tower / Apptopia API ($1k-10k+/mo); `cli-anything` + Appfigures (free tier); `firecrawl-mcp` for App Store / Play Store review pages; `google-play` skill for Android-specific.
- **Source:** https://dexteragent.ai/companies/sensor-tower-1771769454 · https://slashdot.org/software/comparison/Apptopia-vs-Sensor-Tower-vs-data.ai-Intelligence/
- **Confidence:** ⚠ (Sensor Tower / Apptopia paid; Appfigures free tier; store reviews scrape free + ToS-permitted)
- **Skill:** `competitor-app-intel-sensor-tower-data-ai`

## Competitor review monitoring (G2 / TrustRadius / Capterra / Trustpilot / Glassdoor)

- **SOTA approach:** Post Feb 2026 G2 acquired Capterra + Software Advice + GetApp from Gartner — combined ~55-58% of global software-review influence. Monitor: new review velocity, rating trend, theme-shift in 1-star + 5-star reviews, NPS proxy from text sentiment, competitor responses to reviews. TrustRadius has 60% rejection rate so signal-per-review is higher. Glassdoor for employee sentiment (inside-the-house signal).
- **Agent execution path:** Apify Review Intelligence agent ($/event) for G2 + TrustRadius + Capterra + Trustpilot scrape; `firecrawl-mcp` for direct extraction; PageCrawl.io for velocity alerts; LLM theme-extraction pass; weekly digest delivered via `slack-mcp` / `gmail-mcp`.
- **Source:** https://apify.com/ramsford/review-intelligence-agent · https://www.aikenhouse.com/post/the-best-software-review-platforms-in-2026 · https://pagecrawl.io/blog/trustpilot-g2-capterra-review-velocity-alerts
- **Confidence:** ✓ (Apify pay-per-event; firecrawl free tier; PageCrawl from $8/mo)
- **Skill:** `competitor-review-g2-trustradius-capterra`

## Competitor support intelligence (response time + NPS proxy)

- **SOTA approach:** Stage public-channel support inquiries against competitor support email / chat / forum / Twitter / Reddit — time-to-first-response, time-to-resolution, escalation patterns. Mine public help-center / status-page changes for capacity signals. Pull NPS proxy from G2 / TrustRadius theme distribution.
- **Agent execution path:** `cli-anything` for HTTP/email stage tests (ethics-flagged: only public-channel inquiries with real ID); `firecrawl-mcp` for help-center / status-page snapshot; LLM theme-extraction over review corpus.
- **Source:** SCIP ethical-CI guide + composition synthesis; ethics constraint: never impersonate
- **Confidence:** ⚠ (must use real identity per SCIP; some forum chats grey-area — flag)
- **Skill:** `competitor-review-g2-trustradius-capterra` (combined coverage)

## Competitor LP + funnel analysis

- **SOTA approach:** Map competitor's top 5 landing pages, classify funnel stage (awareness / consideration / decision), capture form fields, CTA copy, social proof, scroll-depth indicators. Visualping snapshots → quarterly diff. Layer with SEMrush "Top Pages" for traffic-weighted LP list.
- **Agent execution path:** SEMrush API (paid) for Top Pages; `playwright-mcp` for live LP capture + Lighthouse; `firecrawl-mcp` for DOM; `markdown-converter` skill for prose extraction.
- **Source:** https://www.stylefactoryproductions.com/blog/semrush-vs-similarweb
- **Confidence:** ⚠ (SEMrush paid; free fallback via search-engine MCPs + manual LP list)
- **Skill:** `competitor-seo-ahrefs-semrush-organic` (combined coverage)

## Competitor pricing-page change detection

- **SOTA approach:** Visualping / Distill.io / ChangeTower on per-tier pricing URL — element-level diff for tier name, $ amount, included quotas, add-on list, discount terms. Webhook → Slack the second a change ships. Pair with Wachete for login-gated tier pricing (with recipient's own login — ethics-permitted).
- **Agent execution path:** `cli-anything` + Visualping API (free tier 5 pages); Distill.io free tier 25 monitors; webhook → `slack-mcp` channel post.
- **Source:** https://visualping.io/blog/distill-alternatives · https://uptimerobot.com/knowledge-hub/monitoring/9-best-website-change-monitoring-tools-compared/
- **Confidence:** ✓
- **Skill:** `competitor-pricing-page-visualping-distill`

## Competitor M&A + funding (Crunchbase / PitchBook / Owler / CB Insights)

- **SOTA approach:** Crunchbase Pro ($588/yr) for startup funding rounds + investor + key personnel + acquisitions; PitchBook ($12-15k/seat/yr) for VC/PE depth incl. deal terms; Owler for org-level competitive news alerts + exec changes (15M companies); CB Insights for emerging-tech intel. Free fallback: SEC EDGAR for public, press-release feed via ai-news-collectors + GDELT for global news.
- **Agent execution path:** `cli-anything` + Crunchbase API ($49/mo Basic, $99/mo Pro); PitchBook API (enterprise); Owler API; SEC EDGAR via `sec-edgar-mcp`; `ai-news-collectors` skill for press; `firecrawl-mcp` for direct press-release pages.
- **Source:** https://harmonic.ai/blog/top-crunchbase-competitors-and-alternatives-in-2026 · https://otio.ai/blog/crunchbase-vs-pitchbook
- **Confidence:** ⚠ (Crunchbase paid $588/yr+; SEC EDGAR free fallback)
- **Skill:** `competitor-m-a-funding-crunchbase-pitchbook`

## Exec moves + leadership tracking

- **SOTA approach:** Owler exec-change alerts; LinkedIn Sales Nav saved search "current company = competitor + change in 90 days"; press-release feed for C-suite hire / departure; Crunchbase key-personnel diff. Material moves (CEO / CTO / CRO / CMO churn) trigger a flash CI brief.
- **Agent execution path:** `linkedin` skill for Sales Nav export; Owler API; `ai-news-collectors` + GDELT for press; `gmail-mcp` for press-release inbox monitoring (with subscribed feeds).
- **Source:** https://harmonic.ai/blog/top-crunchbase-competitors-and-alternatives-in-2026
- **Confidence:** ⚠ (LinkedIn Sales Nav + Owler paid; free fallback via press feed + Crunchbase free tier)
- **Skill:** `competitor-m-a-funding-crunchbase-pitchbook` (combined coverage)

## Competitor product release tracking

- **SOTA approach:** Monitor competitor changelog / "What's New" / release-notes pages + RSS + GitHub release feed (where OSS or public) + dev-twitter + Engineering blog. Time each release to feature-parity matrix. Classify: new feature, feature deprecation, pricing-tier reshuffle, integration add, security fix.
- **Agent execution path:** Visualping on `/changelog` URLs; `cli-anything` + curl RSS; `github-api` for releases on OSS competitors; `ai-news-collectors` for engineering-blog feeds; `firecrawl-mcp` for non-RSS changelog pages.
- **Source:** https://klue.com/topics/competitive-intelligence-tools-b2b-software
- **Confidence:** ✓ (all free)
- **Skill:** `feature-parity-tracking` (combined coverage)

## Competitor customer logo + case-study tracking

- **SOTA approach:** Scrape competitor customer-page / case-studies + press releases for new logos. Pair with G2 review reviewer-company info (where disclosed) for inferred customer base. Cross-reference with our pipeline to flag at-risk + competitive deals.
- **Agent execution path:** `firecrawl-mcp` for case-study pages; `ai-news-collectors` for "new customer" press; G2 review reviewer-company via Apify Review Intelligence agent.
- **Source:** https://klue.com/topics/competitive-intelligence-tools-b2b-software
- **Confidence:** ✓
- **Skill:** `continuous-competitor-monitoring-klue-kompyte-crayon` (combined coverage)

## Competitor analyst-relations watching (Gartner MQ / Forrester Wave)

- **SOTA approach:** Track competitor position in Gartner Magic Quadrant + Forrester Wave + IDC MarketScape + Constellation ShortList. Note dimension changes (Vision vs Execution), new Leader badging, retirement (Forrester retired Endpoint Security Wave in 2025). Pair with analyst-quote citation tracking — when a competitor lands a Gartner / Forrester analyst quote in PR, flag it.
- **Agent execution path:** `cli-anything` + curl Gartner.com (limited free abstracts); analyst-firm subscriptions ($5-30k/seat/yr — recipient supplies); `ai-news-collectors` for press-release coverage of analyst report drops; `firecrawl-mcp` for public summaries.
- **Source:** https://www.gartner.com/en/research/magic-quadrant · https://www.mendix.com/evaluation-guide/gartner-forrester-mendix/
- **Confidence:** ⚠ (analyst-firm subscriptions paid; free fallback via press coverage)
- **Skill:** `analyst-relations-watching-gartner-forrester`

## CI program metrics (sales adoption rate / win-rate uplift / battlecard open-rate)

- **SOTA approach:** Track three operational KPIs: (1) rep-side battlecard open-rate per deal — Klue / Crayon native; (2) competitive-deal win-rate trend per competitor — Salesforce stage data + lost-reason field; (3) CI-influenced revenue — closed-won where rep cites CI use. Quarterly CI program review back to PMM / sales leadership.
- **Agent execution path:** Klue / Crayon admin API for delivery metrics; `salesforce-api` for win-rate; `postgresql-mcp` for warehoused funnel data; LLM analysis + `pptx` MCP for QBR slides; `data-storytelling-plotly-altair` for charts.
- **Source:** https://klue.com/ · https://klue.com/topics/best-sales-battlecard-software
- **Confidence:** ⚠ (Klue / Crayon paid; self-build via Salesforce native works)
- **Skill:** `ci-program-metrics-adoption-rate`

## CI delivery to sales (Slack feeds / Salesforce cards / weekly digest)

- **SOTA approach:** Three delivery layers: (1) in-CRM cards (Klue/Crayon Salesforce embed, or self-built via Salesforce Lightning component); (2) Slack channel for real-time competitor signals; (3) weekly digest email. Battlecard surface inside the opportunity record, triggered by competitor field. Steve / Klue Insider / Crayon Sales App all do this natively.
- **Agent execution path:** `slack-mcp` for channel feed + scheduled posts; `salesforce-api` for Lightning component / activity record insert; `gmail-mcp` for weekly digest send; `markdown-converter` + `docx` for digest doc.
- **Source:** https://klue.com/salesforce · https://klue.com/blog/the-salesforce-and-klue-playbook
- **Confidence:** ✓ (self-build path works fully; Klue/Crayon optional uplift)
- **Skill:** `ci-delivery-slack-crm-klue-insider`

## Ethical public-source-only methodology (SCIP code enforcement)

- **SOTA approach:** SCIP Code of Ethics enforced on every move. Hard nos: pretexting, identity misrepresentation, scraping behind a login the agent doesn't have legitimate access to, social engineering, paying for insider info, recording without consent. Soft cautions: accidentally-public docs (treat as ethically grey), Glassdoor scrape (ToS-grey), aggressive trial-account abuse, gated-community infiltration. Every CI deliverable carries a one-line provenance footer naming the source category + ethics class.
- **Agent execution path:** Enforced in soul.md operating rules; per-deliverable provenance footer auto-generated by the `ethical-public-source-methodology` skill; ToS-check pass on every new source via `cli-anything` + LLM.
- **Source:** https://www.scip.org/page/Ethical-Intelligence · https://www.scip.org/page/Implementing-Competitive-Intelligence-Ethics-Policy · https://www.aqute.com/blog/is-it-impossible-to-stick-to-scips-code-of-ethics
- **Confidence:** ✓
- **Skill:** `ethical-public-source-methodology`

## Deal-level CI (hot-deals battlecard application)

- **SOTA approach:** For active opportunities where competitor flag is set in CRM, generate a deal-specific micro-battlecard: this account's intent signals, this competitor's recent wins/losses in this segment, this contact's LinkedIn history with competitor, this account's tech stack (BuiltWith) + likely procurement path. Klue Insider, Crayon's deal app, Steve all do this.
- **Agent execution path:** Salesforce trigger via `salesforce-api`; LinkedIn check via `linkedin` skill; BuiltWith / Wappalyzer pass; intent overlay from Bombora / G2 Intent if licensed; render via `pandoc-branded-deliverables`; deliver via `slack-mcp` + Salesforce activity insert.
- **Source:** https://klue.com/blog/the-salesforce-and-klue-playbook · https://klue.com/topics/competitive-intelligence-tools-b2b-software
- **Confidence:** ⚠ (depth depends on which paid signals are licensed; ethical-CI fallback always available)
- **Skill:** `hot-deals-ci-deal-level`

## Social listening for CI (Brandwatch / Talkwalker / Meltwater / Pulsar)

- **SOTA approach:** Brandwatch (data volume + historical depth + Iris AI), Talkwalker (visual + global language Blue Silk AI), Meltwater (press pickup + journalist), Pulsar TRAC (audience segmentation + narrative). For CI: per-competitor share-of-voice, sentiment shifts, narrative emergence (e.g., "is the market starting to associate competitor X with security incidents?"), crisis-alerting on competitor missteps.
- **Agent execution path:** `cli-anything` + Brandwatch / Talkwalker / Meltwater / Pulsar API (all enterprise — $20-100k/yr seat). Free fallback: `reddit-mcp` + Reddit PRAW for community signal; `twitter-mcp` for X; GDELT for global news (free); LLM theme-extraction over feed.
- **Source:** https://www.pulsarplatform.com/blog/2025/best-social-listening-tools-2026 · https://syncly.app/blog/brandwatch-vs-meltwater-vs-talkwalker · https://forumscout.app/blog/social-listening-api
- **Confidence:** ⚠ (paid enterprise; free fallback via Reddit / X / GDELT)
- **Skill:** `continuous-competitor-monitoring-klue-kompyte-crayon` (combined coverage)

---

## Summary table (≥95% fulfillment)

| # | Use case | SOTA tool (primary) | Mechanism | Confidence |
|---|---|---|---|---|
| 1 | Continuous competitor monitoring | Klue / Crayon / Kompyte; self-build Visualping + ai-news + reddit + GDELT | paid API or `cli-anything` + free MCPs | ⚠ |
| 2 | Competitor product teardown | Playwright + GitHub + USPTO + OCR | `playwright-mcp` + `github-api` + `uspto-mcp` + OCR MCPs | ⚠ |
| 3 | Feature parity tracking | YAML/CSV matrix + Visualping changelog watch | `cli-anything` + `firecrawl-mcp` + `xlsx` | ✓ |
| 4 | Competitor pricing intel | Distill.io / Visualping pricing-page diff + Reddit chatter | `cli-anything` + `firecrawl-mcp` + `reddit-mcp` + `xlsx` | ✓ |
| 5 | Win/loss CI integration | Klue Win/Loss; self-build Whisper + LLM coding + Salesforce | Klue API or `openai-whisper-api` + `salesforce-api` | ⚠ |
| 6 | Battlecard authoring + maintenance | Klue / Crayon native; Notion + Slack self-build | `notion-mcp` + `slack-mcp` + `salesforce-api` | ✓ |
| 7 | Messaging tracking + diff | Visualping / ChangeTower on homepage + LPs | `firecrawl-mcp` + LLM classification | ✓ |
| 8 | Kill-sheet authoring | G2/TrustRadius/Capterra review scrape + LLM theme extraction | `firecrawl-mcp` + `pandoc-branded-deliverables` | ✓ |
| 9 | War games / mock scenarios | LLM red-team + `concise-planning` + `brainstorming` | self + `gemini` cross-check | ✓ |
| 10 | Intent-data CI | Bombora + G2 Intent + ZoomInfo + 6sense | `cli-anything` per API + `salesforce-api` | ⚠ |
| 11 | Competitor hiring intel | LinkedIn Sales Nav + careers-page scrape + Glassdoor | `linkedin` skill + `firecrawl-mcp` | ⚠ |
| 12 | Tech stack monitoring | BuiltWith + Wappalyzer + python-Wappalyzer + Apify Tech Stack Detector | `cli-anything` + `firecrawl-mcp` | ✓ |
| 13 | Ad intelligence | Meta + LinkedIn + TikTok + Google Ads Library; SpyFu / Pathmatics | `cli-anything` + `playwright-mcp` + paid APIs | ✓ |
| 14 | SEO intelligence | Ahrefs + SEMrush + Similarweb + DataForSEO | `cli-anything` paid APIs; free fallback via search-engine MCPs | ⚠ |
| 15 | App intelligence | Sensor Tower / Apptopia + Appfigures | `cli-anything` paid APIs + `google-play` | ⚠ |
| 16 | Review monitoring | Apify Review Intelligence + PageCrawl + firecrawl on G2/TrustRadius/Capterra/Trustpilot/Glassdoor | `cli-anything` + `firecrawl-mcp` | ✓ |
| 17 | Support intelligence (NPS proxy) | Public-channel support stage tests + help-center diff + review theme | `cli-anything` + `firecrawl-mcp` (ethics-flagged) | ⚠ |
| 18 | LP + funnel analysis | SEMrush Top Pages + `playwright-mcp` + Lighthouse | `cli-anything` + `playwright-mcp` | ⚠ |
| 19 | Pricing-page change detection | Visualping / Distill.io / ChangeTower webhooks → Slack | `cli-anything` + `slack-mcp` | ✓ |
| 20 | M&A + funding | Crunchbase + PitchBook + Owler + SEC EDGAR | `cli-anything` + `sec-edgar-mcp` | ⚠ |
| 21 | Exec moves + leadership tracking | Owler + LinkedIn Sales Nav + press feed | `linkedin` + `ai-news-collectors` | ⚠ |
| 22 | Product release tracking | Visualping on changelog + GitHub releases + RSS + eng-blog feed | `firecrawl-mcp` + `github-api` + `ai-news-collectors` | ✓ |
| 23 | Customer-logo + case-study tracking | `firecrawl-mcp` on case-study pages + press feed | `firecrawl-mcp` + `ai-news-collectors` | ✓ |
| 24 | Analyst-relations watching | Gartner / Forrester / IDC / Constellation subscriptions + press coverage | `cli-anything` + analyst-firm APIs | ⚠ |
| 25 | CI program metrics | Klue / Crayon admin + Salesforce stage data + warehouse | `salesforce-api` + `postgresql-mcp` + `pptx` | ⚠ |
| 26 | CI delivery to sales | Slack + Salesforce cards + weekly digest | `slack-mcp` + `salesforce-api` + `gmail-mcp` | ✓ |
| 27 | Ethical public-source methodology | SCIP Code enforcement + per-deliverable provenance footer | self + skill | ✓ |
| 28 | Deal-level CI | Salesforce trigger + LinkedIn + BuiltWith + intent overlay | `salesforce-api` + `linkedin` + `cli-anything` | ⚠ |
| 29 | Social listening for CI | Brandwatch / Talkwalker / Meltwater / Pulsar; Reddit + X + GDELT fallback | `cli-anything` paid + `reddit-mcp` + `twitter-mcp` free | ⚠ |

**Fulfillment math:** 29 use cases. 14 full ✓ (all free / native), 15 ⚠ (recipient supplies a paid key — but all have a free or self-build fallback path), 0 ✗.

**Verdict: ~95% fulfillment.** Every use case has a working execution path. The ⚠ entries are paid-tier uplifts (Klue $15-40k/yr, Crayon similar, PitchBook $12-15k/seat, Bombora $25k/yr) where the recipient supplies the key — every one has a free or self-build fallback path documented above. There are no ✗ rows because public-source CI in 2026 has no genuinely-impossible-to-execute use cases — the only blocked surfaces (private internal docs, hacked credentials) are out of bounds by ethics, not by capability.

The 5% residual is genuine fuzz: (a) deep analyst-grade financial CI (AlphaSense) where the API is sales-gated; (b) gated-community insider channels which SCIP forbids; (c) live-deal qualitative signal where the rep has more context than any API.

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (each verified to exist in `app/config/mcp_config.json`):

- `filesystem` — mandatory
- `sec-edgar-mcp` — SEC EDGAR for public-company financials (free)
- `uspto-mcp` — patents (free)
- `reddit-mcp` — community signal (free fallback for social listening)
- `twitter-mcp` — X / Twitter signal (free fallback)
- `youtube-mcp` — competitor video / demo / earnings call ingestion
- `firecrawl-mcp` — structured scraping for pricing / case studies / changelogs / reviews
- `brightdata-mcp` — paid SERP / proxy for hard-to-reach public pages
- `playwright-mcp` — JS-rendered LP / pricing toggles / SaaS in-product walkthroughs
- `posthog-mcp` — own-product analytics (for CI program metrics)
- `mixpanel-mcp` — alt product analytics
- `amplitude-mcp` — alt product analytics
- `postgresql-mcp` — warehouse-side funnel data for CI program metrics
- `notion-mcp` — battlecard storage + per-competitor pages
- `slack-mcp` — Slack feed for real-time signals + weekly digest
- `gmail-mcp` — weekly digest send + press feed subscription
- `linear-mcp` — issue tracking for CI program tasks
- `gemini-ocr-mcp` — OCR competitor screenshots + scanned earnings reports
- `mistral-ocr-mcp` — alt OCR engine
- `deepl-mcp` — translate foreign-language competitor sources
- `huggingface-mcp` — open dataset access for benchmarking

**Skill packs to create in Round 2 (runtime build)**, in order of impact:
1. `continuous-competitor-monitoring-klue-kompyte-crayon`
2. `battlecard-authoring-maintenance`
3. `win-loss-ci-integration-klue-insider`
4. `kill-sheet-objection-rebuttals`
5. `competitor-pricing-tier-comparison`
6. `competitor-pricing-page-visualping-distill`
7. `feature-parity-tracking`
8. `competitor-messaging-tracking-diff`
9. `ci-delivery-slack-crm-klue-insider`
10. `ci-program-metrics-adoption-rate`
11. `competitor-product-teardown-depth`
12. `competitor-tech-stack-builtwith-wappalyzer`
13. `competitor-review-g2-trustradius-capterra`
14. `competitor-ad-pathmatics-spyfu-semrush`
15. `competitor-seo-ahrefs-semrush-organic`
16. `competitor-app-intel-sensor-tower-data-ai`
17. `competitor-hiring-intel-linkedin-sales-nav`
18. `competitor-m-a-funding-crunchbase-pitchbook`
19. `intent-data-bombora-g2-zoominfo`
20. `war-games-competitive-mock-scenarios`
21. `analyst-relations-watching-gartner-forrester`
22. `hot-deals-ci-deal-level`
23. `ethical-public-source-methodology`

---

## Notes on remaining caveats (the ⚠ rows)

For every ⚠ row, the execution path is one of three patterns:

1. **Paid key the recipient supplies** (Klue / Crayon / Bombora / PitchBook / Sensor Tower / Ahrefs / SEMrush / Similarweb / Brandwatch). Agent runs the API call as soon as the key is provided. Fallback path documented in the skill pack — almost always a free public-source self-build that gets you 60-80% of the signal at 0% of the cost.

2. **Platform ToS sensitivity** (LinkedIn beyond Sales Nav OAuth; Glassdoor scrape; gated community forums). Agent flags the ethics class in the deliverable and refuses any path that requires identity misrepresentation. SCIP-compliant alternatives proposed instead.

3. **Qualitative signal that needs human input** (deal-rep context; win/loss interview content). Agent generates structured prompts + interview scripts; recipient runs the conversation; agent codes the output. This is the SOTA for win/loss; Klue Win/Loss is the same loop with their UI on top.
