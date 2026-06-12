# Competitive Intelligence — Source Attribution

Section-to-source map for soul.md and role.md. This file is part of the bundle but is **not** loaded into context — it exists for human verification and future refreshes.

Per-use-case mapping with confidence flags lives at `reference/SOTA_USE_CASES.md`. Per-tool source URLs in `agent.yaml → sources` and `reference/INVENTORY.md`.

The v1 build pass derived methodology from web research (URLs cited below); the adjacent v0 mirror at `agent_bundle/agents/research-analyst/` provided the baseline patterns for battlecard / SWOT / monitoring frameworks (lifted from `voltagent-competitive-analyst.md` via research-analyst's transitive citation).

---

## soul.md → source map

| Section | Source(s) |
|---|---|
| Opening identity / action-verb persona intro | composition synthesis from CraftBot operator-framing rule + 2026 SOTA tool catalog (Klue / Crayon / Visualping / `firecrawl-mcp` / etc.) |
| 3 load-bearing convictions | composition: (1) continuous-vs-episodic synthesized from `https://klue.com/topics/competitive-intelligence-tools-b2b-software` + `https://www.autobound.ai/blog/top-15-competitive-intelligence-tools-2026`; (2) sales-adoption-as-metric from `https://klue.com/topics/best-sales-battlecard-software`; (3) ethics-as-non-binding from `https://www.scip.org/page/Ethical-Intelligence` + `https://www.aqute.com/blog/is-it-impossible-to-stick-to-scips-code-of-ethics` |
| Purpose | composition synthesis from `research-analyst/soul.md` competitive-intelligence mode + Klue / Crayon platform language |
| Execution stack | `reference/SOTA_USE_CASES.md` (this agent) |
| When invoked — Continuous monitoring | Klue + Crayon + Kompyte feature coverage (Autobound 2026 CI tools comparison + Klue blog) |
| When invoked — Battlecard authoring | `https://klue.com/topics/best-sales-battlecard-software` + Klue Salesforce playbook |
| When invoked — Win/loss CI | `https://klue.com/blog/win-loss-battlecards-salesforce` + Klue Win/Loss product page |
| When invoked — Kill-sheet authoring | composition synthesis from G2/TR/Capterra review-mining patterns + PMM-approval rule |
| When invoked — War games | composition synthesis from `voltagent-trend-analyst.md` scenario-planning template (lifted via research-analyst v0) |
| When invoked — Deal-level CI | `https://klue.com/salesforce` + `https://klue.com/blog/the-salesforce-and-klue-playbook` |
| When invoked — Product teardown | composition synthesis + SCIP trial-account ethics rule |
| When invoked — Pricing intelligence | `https://visualping.io/blog/distill-alternatives` + Distill.io / Visualping product docs |
| When invoked — Analyst-relations | `https://www.gartner.com/en/research/magic-quadrant` + `https://www.mendix.com/evaluation-guide/gartner-forrester-mendix/` |
| When invoked — CI program metrics | `https://klue.com/` + Klue sales-enablement metrics framing |
| Core operating rules | merged from SCIP Code of Ethics + Klue/Crayon adoption-rate rhetoric + research-analyst v0 source-triangulation rules |
| Mode-specific decisions | one entry per mode matched to its referenced source platform |
| Quality gates | composition synthesis from SCIP ethics policy + battlecard best practices (Klue 7 Best Battlecard Software) |
| Output format | composition synthesis from battlecard / kill-sheet / digest patterns in Klue + Crayon + Kompyte blogs |
| Communication style | composition synthesis from research-analyst v0 "lead with so-what" + CI-specific deal-impact framing |
| When to push back | SCIP Code of Ethics (refuse) + Klue/Crayon adoption-rule (push back on Notion-only) |
| When to defer | composition synthesis — sibling-agent hand-offs to `research-analyst`, `sales-agent`, `product-manager`, `marketing-agent` |
| First-conversation routine questions | standard PROACTIVE.md self-init pattern (METHODOLOGY.md decision); questions tailored to CI program setup |
| Closing rule | composition synthesis restating 3 convictions |

---

## role.md → source map

| Section | Source(s) |
|---|---|
| Capability reference — CI program tiers | composition: Klue / Kompyte / Crayon pricing-vs-team-size analysis (Klue blog + Parano.ai 2026 pricing) |
| Capability reference — Competitor scope categories | `voltagent-competitive-analyst.md` competitor identification (via research-analyst v0) |
| Capability reference — Signal layer cadence | composition: per-layer cadence derived from Crayon depth (Autobound 2026) + Klue continuous-monitoring framing |
| Capability reference — CI delivery channels | `https://klue.com/salesforce` + Klue Insider product page |
| Capability reference — Battlecard sections | `https://klue.com/topics/best-sales-battlecard-software` |
| Capability reference — Kill-sheet sections | composition synthesis from PMM-approval pattern |
| Continuous monitoring playbook | Klue + Crayon + Kompyte feature coverage + Visualping config docs |
| Battlecard authoring playbook | Klue 7 Best Battlecard Software + Klue Salesforce playbook |
| Kill-sheet playbook | composition: Apify Review Intelligence + LLM theme-extraction pattern + PMM-approval rule |
| Win-loss CI playbook | `https://klue.com/blog/win-loss-battlecards-salesforce` + Klue Win/Loss product feature list |
| War games playbook | composition: pre-mortem + red-team pattern from `voltagent-trend-analyst.md` scenario-planning (via research-analyst v0) + `gemini` adversarial cross-check pattern |
| Pricing intelligence playbook | `https://visualping.io/blog/distill-alternatives` + Distill.io element-level monitoring docs |
| Product teardown playbook | composition: SCIP trial-account rule + `playwright-mcp` patterns |
| Hot-deals CI playbook | `https://klue.com/blog/the-salesforce-and-klue-playbook` Klue Insider patterns |
| Analyst-relations playbook | `https://www.gartner.com/en/research/magic-quadrant` + Mendix MQ-vs-Wave guide |
| Ethical CI playbook (SCIP code) | `https://www.scip.org/page/Ethical-Intelligence` + `https://www.scip.org/page/Implementing-Competitive-Intelligence-Ethics-Policy` + Aqute "is SCIP code practical" |
| Antipattern catalog | composition synthesis from observed CI program failure modes (Klue + Crayon blogs) |
| Reference patterns — refresh-on-signal trigger config | composition synthesis from Klue refresh-trigger pattern |
| Reference patterns — Provenance footer | composition synthesis from SCIP per-deliverable provenance requirement |
| Reference patterns — Two-source triangulation | research-analyst v0 multi-source triangulation procedure |
| SOTA tool reference | `reference/SOTA_USE_CASES.md` (this agent) + per-tool docs (URLs in agent.yaml sources) |
| SOTA execution playbook | `reference/SOTA_USE_CASES.md` (this agent) |
| Battlecard template | composition synthesis from Klue 7 Best Battlecard Software + Klue Sales Enablement Playbook |
| Kill-sheet template | composition synthesis |
| Pricing-tier grid template | composition synthesis |
| Feature parity matrix template | composition synthesis |
| Weekly digest template | composition synthesis from Klue / Crayon weekly-digest patterns |
| QBR deck template (CI program metrics) | composition synthesis from Klue program-metrics framing + research-analyst v0 KPI-dashboard pattern |

---

## Notes on "authored from synthesis"

Several role.md sections include composition synthesis on top of referenced material:

- **Refresh-on-signal trigger config (YAML pattern)** — Klue refresh rules are described prose-wise in their docs; the YAML schema is synthesized to make it agent-actionable.
- **Provenance footer pattern** — SCIP requires per-deliverable source provenance; the specific ASCII-box-format footer is synthesized.
- **Two-source triangulation pattern** — lifted from research-analyst v0 (`voltagent-research-analyst.md`'s source-triangulation procedure); applied to CI claims.
- **Antipattern catalog** — composition from observed failure modes in published CI program audits + Klue / Crayon blog posts.
- **Battlecard / kill-sheet / digest / QBR templates** — section structure synthesized from Klue / Crayon platform UI screenshots and product blog posts; specific ASCII layouts authored fresh for CraftBot.
- **Signal-layer cadence table** — synthesized from Crayon "all 8+ signal types" coverage (Autobound 2026) + Klue continuous-monitoring framing + research-analyst v0 trend-analysis cadence rules.

The first-conversation PROACTIVE.md self-init footer is the standard pattern (METHODOLOGY.md decision); only the three routine questions are CI-specific (primary CI platform / top competitors / delivery channels).

The action-verb persona intro is mandatory per the operator-framing rule in `build_new_agent_instructions.md` (and verified by `verify.py`); verbs (monitor / scrape / fetch / query / render / ship / trigger / deploy / track / enforce) chosen from the approved action-verb set.

---

## How to update this agent

1. Re-fetch SOTA tool pricing + feature URLs listed in `reference/INVENTORY.md`, overwrite the cited URLs in agent.yaml sources
2. Diff to see what changed (pricing tier moves, feature additions, vendor consolidation events like the Feb 2026 G2-Capterra deal)
3. Update corresponding sections of soul.md (only if a decision rule changes — e.g., if a major free tier disappears) and role.md (every URL change)
4. Update `reference/SOTA_USE_CASES.md` confidence ratings if a free tier disappears or a paid tier becomes free
5. Re-run `python verify.py competitive-intelligence` to confirm structure intact
6. Re-build: `python build.py competitive-intelligence` produces a fresh `.craftbot`

---

## SOTA tool sources (June 2026)

Source map for the SOTA-tool reference section in role.md and the bundled skill packs in `skills/` (created in Round 2). Per-use-case mapping with confidence flags lives in `reference/SOTA_USE_CASES.md`.

| Tool / API | Source URL | Skill pack(s) |
|---|---|---|
| Klue (CI platform + Win/Loss + Salesforce) | https://klue.com/ · https://klue.com/salesforce · https://klue.com/blog/win-loss-battlecards-salesforce · https://klue.com/topics/best-sales-battlecard-software | `continuous-competitor-monitoring-klue-kompyte-crayon`, `win-loss-ci-integration-klue-insider`, `battlecard-authoring-maintenance`, `ci-delivery-slack-crm-klue-insider` |
| Klue 2026 CI tools landscape | https://klue.com/topics/competitive-intelligence-tools-b2b-software | `continuous-competitor-monitoring-klue-kompyte-crayon` |
| Klue × Crayon 2026 pricing | https://parano.ai/blog/klue-vs-crayon | `continuous-competitor-monitoring-klue-kompyte-crayon` |
| Klue × Salesforce playbook | https://klue.com/blog/the-salesforce-and-klue-playbook | `ci-delivery-slack-crm-klue-insider`, `hot-deals-ci-deal-level` |
| Crayon CI depth coverage | https://www.autobound.ai/blog/top-15-competitive-intelligence-tools-2026 | `continuous-competitor-monitoring-klue-kompyte-crayon` |
| Kompyte (Semrush) | https://www.kompyte.com/blog/top-competitive-intelligence-tools | `continuous-competitor-monitoring-klue-kompyte-crayon` |
| Visualping | https://visualping.io/ · https://visualping.io/blog/distill-alternatives | `competitor-pricing-page-visualping-distill`, `competitor-messaging-tracking-diff` |
| Distill.io | https://distill.io/ | `competitor-pricing-page-visualping-distill` |
| ChangeTower | https://changetower.com/ · https://uptimerobot.com/knowledge-hub/monitoring/9-best-website-change-monitoring-tools-compared/ | `competitor-pricing-page-visualping-distill` |
| Wachete | https://www.wachete.com/ | `competitor-pricing-page-visualping-distill` |
| PageCrawl | https://pagecrawl.io/blog/trustpilot-g2-capterra-review-velocity-alerts | `competitor-review-g2-trustradius-capterra` |
| Apify Review Intelligence | https://apify.com/ramsford/review-intelligence-agent | `competitor-review-g2-trustradius-capterra`, `kill-sheet-objection-rebuttals` |
| G2 / Capterra / Software Advice / GetApp Feb 2026 consolidation | https://www.aikenhouse.com/post/the-best-software-review-platforms-in-2026 | `competitor-review-g2-trustradius-capterra` |
| TrustRadius (60% rejection rate) | https://www.g2.com/products/trustradius/reviews | `competitor-review-g2-trustradius-capterra` |
| BuiltWith | https://builtwith.com/ · https://prospeo.io/s/builtwith-vs-wappalyzer | `competitor-tech-stack-builtwith-wappalyzer` |
| Wappalyzer | https://www.wappalyzer.com/ · https://pasqualepillitteri.it/en/news/2424/how-to-detect-website-tech-stack-wappalyzer-builtwith | `competitor-tech-stack-builtwith-wappalyzer` |
| python-Wappalyzer | https://github.com/chorsley/python-Wappalyzer | `competitor-tech-stack-builtwith-wappalyzer` |
| DetectZeStack | (per source comparison) | `competitor-tech-stack-builtwith-wappalyzer` |
| Apify Tech Stack Detector | https://apify.com/automation-lab/tech-stack-detector | `competitor-tech-stack-builtwith-wappalyzer` |
| Bombora | https://bombora.com/ · https://www.growthspreeofficial.com/blogs/buyer-intent-signals-bombora-g2-zoominfo-b2b-2026 | `intent-data-bombora-g2-zoominfo` |
| G2 Buyer Intent | https://www.g2.com/products/g2-buyer-intent | `intent-data-bombora-g2-zoominfo` |
| ZoomInfo Intent | https://pipeline.zoominfo.com/sales/intent-data-platform | `intent-data-bombora-g2-zoominfo` |
| 6sense Surge | https://6sense.com/ | `intent-data-bombora-g2-zoominfo` |
| Demandbase | https://www.demandbase.com/ · https://www.autobound.ai/blog/best-intent-data-platforms | `intent-data-bombora-g2-zoominfo` |
| TrustRadius Buyer Intent | https://www.trustradius.com/for-vendors/intent | `intent-data-bombora-g2-zoominfo` |
| LinkedIn Sales Navigator filters 2026 | https://sbl.so/linkedin/sales-navigator-filters-guide/ · https://www.demandsense.com/blog/how-to-use-linkedin-sales-navigator | `competitor-hiring-intel-linkedin-sales-nav` |
| Sensor Tower + data.ai | https://sensortower.com/ · https://dexteragent.ai/companies/sensor-tower-1771769454 · https://sensortower.com/blog/data-ai-joins-sensor-tower | `competitor-app-intel-sensor-tower-data-ai` |
| Apptopia | https://apptopia.com/ · https://slashdot.org/software/comparison/Apptopia-vs-Sensor-Tower-vs-data.ai-Intelligence/ | `competitor-app-intel-sensor-tower-data-ai` |
| Pathmatics (Sensor Tower digital ad) | https://sensortower.com/product/digital-advertising/pathmatics | `competitor-ad-pathmatics-spyfu-semrush` |
| SpyFu | https://www.spyfu.com/ | `competitor-ad-pathmatics-spyfu-semrush` |
| AdLibrary multi-platform API | https://adlibrary.com/guides/best-ad-spy-api | `competitor-ad-pathmatics-spyfu-semrush` |
| Meta Ad Library | https://www.facebook.com/ads/library | `competitor-ad-pathmatics-spyfu-semrush` |
| LinkedIn Ad Library | https://www.linkedin.com/ad-library/ | `competitor-ad-pathmatics-spyfu-semrush` |
| TikTok Creative Center | https://library.tiktok.com/ads | `competitor-ad-pathmatics-spyfu-semrush` |
| Google Ads Transparency Center | https://adstransparency.google.com/ | `competitor-ad-pathmatics-spyfu-semrush` |
| Ahrefs | https://ahrefs.com/ | `competitor-seo-ahrefs-semrush-organic` |
| SEMrush + SEMrush .Trends | https://www.semrush.com/ · https://www.stylefactoryproductions.com/blog/semrush-vs-similarweb | `competitor-seo-ahrefs-semrush-organic` |
| Similarweb | https://www.similarweb.com/ · https://onlysearch.ai/blog/competitive-intel-data-sources | `competitor-seo-ahrefs-semrush-organic` |
| DataForSEO | https://dataforseo.com/ | `competitor-seo-ahrefs-semrush-organic` |
| Crunchbase API | https://data.crunchbase.com/docs/using-the-api · https://harmonic.ai/blog/top-crunchbase-competitors-and-alternatives-in-2026 | `competitor-m-a-funding-crunchbase-pitchbook` |
| PitchBook | https://pitchbook.com/ · https://otio.ai/blog/crunchbase-vs-pitchbook | `competitor-m-a-funding-crunchbase-pitchbook` |
| Owler | https://www.owler.com/ | `competitor-m-a-funding-crunchbase-pitchbook` |
| CB Insights | https://www.cbinsights.com/ | `competitor-m-a-funding-crunchbase-pitchbook` |
| AlphaSense (+ Sentieo merger) | https://www.alpha-sense.com/ · https://www.alpha-sense.com/tr-alphasense-and-sentieo/ | `analyst-relations-watching-gartner-forrester`, `competitor-m-a-funding-crunchbase-pitchbook` |
| Brandwatch | https://www.brandwatch.com/ · https://syncly.app/blog/brandwatch-vs-meltwater-vs-talkwalker · https://www.pulsarplatform.com/blog/2025/best-social-listening-tools-2026 | `continuous-competitor-monitoring-klue-kompyte-crayon` |
| Talkwalker | https://www.talkwalker.com/ · https://www.talkwalker.com/brandwatch-alternative | `continuous-competitor-monitoring-klue-kompyte-crayon` |
| Meltwater | https://www.meltwater.com/ · https://www.meltwater.com/en/blog/top-social-listening-tools | `continuous-competitor-monitoring-klue-kompyte-crayon` |
| Pulsar TRAC | https://www.pulsarplatform.com/ · https://www.pulsarplatform.com/guides/social-listening-competitive-analysis-narratives | `continuous-competitor-monitoring-klue-kompyte-crayon` |
| Gartner Magic Quadrant | https://www.gartner.com/en/research/magic-quadrant · https://www.mendix.com/evaluation-guide/gartner-forrester-mendix/ | `analyst-relations-watching-gartner-forrester` |
| Forrester Wave | https://www.ataccama.com/blog/the-forrester-wave-data-quality-solutions-2026-how-to-read-it-and-why-it-matters-now | `analyst-relations-watching-gartner-forrester` |
| IDC MarketScape | https://www.idc.com/marketscape | `analyst-relations-watching-gartner-forrester` |
| Constellation ShortList | https://www.constellationr.com/research/constellation-shortlist | `analyst-relations-watching-gartner-forrester` |
| SCIP Code of Ethics | https://www.scip.org/page/Ethical-Intelligence | `ethical-public-source-methodology` |
| SCIP Implementing a CI Ethics Policy | https://www.scip.org/page/Implementing-Competitive-Intelligence-Ethics-Policy | `ethical-public-source-methodology` |
| SCIP code practical guide | https://www.aqute.com/blog/is-it-impossible-to-stick-to-scips-code-of-ethics | `ethical-public-source-methodology` |
| SEC EDGAR | https://www.sec.gov/edgar/sec-api-documentation | `competitor-m-a-funding-crunchbase-pitchbook` (via `sec-edgar-mcp`) |
| USPTO PatentsView | https://data.uspto.gov/apis/getting-started | (via `uspto-mcp`) |

### Bundled skill packs (`skills/`) — file map

| Skill folder | Companion playbook in role.md |
|---|---|
| `continuous-competitor-monitoring-klue-kompyte-crayon/` | Continuous monitoring playbook |
| `competitor-product-teardown-depth/` | Product teardown playbook |
| `feature-parity-tracking/` | Capability reference → Signal layer cadence; Battlecard template (drawer) |
| `competitor-pricing-tier-comparison/` | Pricing intelligence playbook; Pricing-tier grid template |
| `win-loss-ci-integration-klue-insider/` | Win-loss CI playbook |
| `battlecard-authoring-maintenance/` | Battlecard authoring playbook; Battlecard template |
| `competitor-messaging-tracking-diff/` | Continuous monitoring playbook → Messaging diff layer |
| `kill-sheet-objection-rebuttals/` | Kill-sheet playbook; Kill-sheet template |
| `war-games-competitive-mock-scenarios/` | War games playbook |
| `intent-data-bombora-g2-zoominfo/` | Hot-deals CI playbook → Intent overlay |
| `competitor-hiring-intel-linkedin-sales-nav/` | Capability reference → Hiring layer |
| `competitor-tech-stack-builtwith-wappalyzer/` | Hot-deals CI playbook → Tech-stack overlay |
| `competitor-ad-pathmatics-spyfu-semrush/` | Capability reference → Ad-library layer |
| `competitor-seo-ahrefs-semrush-organic/` | Capability reference → SEO layer |
| `competitor-app-intel-sensor-tower-data-ai/` | Capability reference → Mobile-app layer |
| `competitor-review-g2-trustradius-capterra/` | Kill-sheet playbook → Review mining |
| `competitor-pricing-page-visualping-distill/` | Pricing intelligence playbook |
| `competitor-m-a-funding-crunchbase-pitchbook/` | Capability reference → M&A + funding layer |
| `ci-program-metrics-adoption-rate/` | QBR deck template |
| `ci-delivery-slack-crm-klue-insider/` | Battlecard authoring playbook → Delivery |
| `ethical-public-source-methodology/` | Ethical CI playbook (SCIP code) |
| `hot-deals-ci-deal-level/` | Hot-deals CI playbook |
| `analyst-relations-watching-gartner-forrester/` | Analyst-relations playbook |

### Per-use-case mapping

See `reference/SOTA_USE_CASES.md` for the per-use-case SOTA approach, agent execution path, source URL, and confidence flag (✓ / ⚠ / ✗) — required reading for understanding what the agent can and cannot fully automate.
