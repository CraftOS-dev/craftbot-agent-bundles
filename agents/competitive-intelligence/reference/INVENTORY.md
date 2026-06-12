# competitive-intelligence — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in SOTA_USE_CASES.md and SOURCES.md). The adjacent v0 mirror is `agent_bundle/agents/research-analyst/`, whose competitive-intelligence section was lifted as the v0 baseline and then expanded into a full specialist with 2026-SOTA tool-by-tool coverage.

For future tightening: pull 4-6 reference agents related to competitive intelligence and product marketing (e.g., `wshobson/agents` PMM packs, VoltAgent `competitive-analyst.md`, `msitarzewski` agency CI agents) into `reference/agents/`, and 6-10 reference skills for battlecard authoring, ad intel, intent data, and review monitoring into `reference/skills/`.

## Web research sources actually used in v1 build pass

| # | Topic | URL | Used for |
|---|---|---|---|
| 1 | CI platforms 2026 (Klue / Crayon / Kompyte) | https://klue.com/topics/competitive-intelligence-tools-b2b-software | Continuous monitoring, battlecard delivery, win-loss CI |
| 2 | Klue vs Crayon 2026 pricing | https://parano.ai/blog/klue-vs-crayon | Tier comparison, CRM integration depth |
| 3 | Klue Salesforce integration & win-loss | https://klue.com/blog/win-loss-battlecards-salesforce | Win/loss-to-battlecard pipeline |
| 4 | Crayon depth (websites, social, jobs, patents, app reviews) | https://www.autobound.ai/blog/top-15-competitive-intelligence-tools-2026 | Continuous-monitoring source coverage |
| 5 | Visualping / Distill.io / ChangeTower / Wachete | https://visualping.io/blog/distill-alternatives · https://uptimerobot.com/knowledge-hub/monitoring/9-best-website-change-monitoring-tools-compared/ | Pricing-page change monitoring; element-level diff |
| 6 | SimilarWeb / SEMrush / Ahrefs comparison | https://www.stylefactoryproductions.com/blog/semrush-vs-similarweb · https://onlysearch.ai/blog/competitive-intel-data-sources | Competitor SEO / traffic intel methodology |
| 7 | Bombora / G2 Intent / ZoomInfo / 6sense | https://www.growthspreeofficial.com/blogs/buyer-intent-signals-bombora-g2-zoominfo-b2b-2026 | Intent-data CI sourcing |
| 8 | Sensor Tower + data.ai (post-2024 merge) + Apptopia | https://dexteragent.ai/companies/sensor-tower-1771769454 · https://slashdot.org/software/comparison/Apptopia-vs-Sensor-Tower-vs-data.ai-Intelligence/ | Competitor app/mobile intel |
| 9 | BuiltWith vs Wappalyzer (with TechPeeker / Bloomberry / DetectZeStack) | https://pasqualepillitteri.it/en/news/2424/how-to-detect-website-tech-stack-wappalyzer-builtwith · https://prospeo.io/s/builtwith-vs-wappalyzer | Competitor tech-stack monitoring |
| 10 | Review platforms (G2 + Capterra consolidation Feb 2026; TrustRadius; Trustpilot; Glassdoor) | https://apify.com/ramsford/review-intelligence-agent · https://www.aikenhouse.com/post/the-best-software-review-platforms-in-2026 | Competitor review intel |
| 11 | Pathmatics / SpyFu / AdLibrary / Adbeat | https://sensortower.com/product/digital-advertising/pathmatics · https://adlibrary.com/guides/best-ad-spy-api · https://www.spyfu.com/ | Competitor ad intel |
| 12 | Crunchbase / PitchBook / Owler / CB Insights | https://harmonic.ai/blog/top-crunchbase-competitors-and-alternatives-in-2026 · https://otio.ai/blog/crunchbase-vs-pitchbook | Funding + M&A + exec moves |
| 13 | LinkedIn Sales Navigator advanced filters 2026 | https://sbl.so/linkedin/sales-navigator-filters-guide/ · https://www.demandsense.com/blog/how-to-use-linkedin-sales-navigator | Competitor hiring intel |
| 14 | AlphaSense (+ Sentieo merger) | https://www.alpha-sense.com/ · https://www.alpha-sense.com/tr-alphasense-and-sentieo/ | Analyst-grade financial CI |
| 15 | Brandwatch / Talkwalker / Meltwater / Pulsar TRAC | https://www.pulsarplatform.com/blog/2025/best-social-listening-tools-2026 · https://syncly.app/blog/brandwatch-vs-meltwater-vs-talkwalker | Social listening for CI |
| 16 | SCIP Code of Ethics | https://www.scip.org/page/Ethical-Intelligence · https://www.scip.org/page/Implementing-Competitive-Intelligence-Ethics-Policy | Public-source-only methodology enforcement |
| 17 | Gartner Magic Quadrant / Forrester Wave watching | https://www.gartner.com/en/research/magic-quadrant | Analyst-relations CI |
| 18 | Meta Ad Library + LinkedIn Ad Library + TikTok Creative Center + Google Ads Transparency | https://www.facebook.com/ads/library · https://www.linkedin.com/ad-library/ · https://adstransparency.google.com/ · https://library.tiktok.com/ads | Free, official ad intel APIs |

## Sources considered but not downloaded

- **wshobson/agents** PMM packs — left for v2; not yet known to ship a CI-specialist agent definition
- **VoltAgent competitive-analyst.md** — already lifted into research-analyst v0 baseline; would be duplicate in v1
- **Anthropic skills repo** — has no CI-specific skill at time of build
- **Klue / Crayon / Kompyte product docs deep-dive** — bookmarked for v2 when bundled skill packs are authored in Round 2

For each tool listed in the SOTA table, the cited URL is the canonical product or pricing reference. Round 2 (skill-pack authoring) will pull the per-tool how-to docs.
