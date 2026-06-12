# Talent Sourcer — Sources

> Section→source map for `soul.md` and `role.md`. Ships in the bundle but is **not** loaded into the agent's context. For humans verifying provenance and for future updates.

## soul.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Title + persona intro | Synthesized from all sources below + the build-prompt seed list | Action-verb-first per build_new_agent_instructions.md operator framing rule |
| Purpose | Synthesis: 2026 sourcing-craft canon + ICP framing + hand-off rules to operations-agent / ceo-agent | Operational glue |
| Execution stack | `reference/SOTA_USE_CASES.md` + all SOTA sources below | Built during runtime build (Step 10); skill packs named, not yet authored |
| When invoked (per-mode procedures) | LinkedIn Recruiter Boolean guides + Gem/hireEZ/Beamery + SeekOut/Findem/AmazingHiring + GitHub mining + Crunchbase/Apollo + RepVue + Toptal/Turing/Andela + diversity-channel community sites + cold-InMail benchmark articles | Cross-source synthesis per mode |
| Core operating rules | Boolean-vs-search-filter benchmark (Talentprise + AmazingHiring), passive vs active recruiting canon, ≥3 sources / no single source >60% (Lupahire + Metaview), 24h reply SLA (Metaview), InMail <400 char rule (ConnectSafely + Salesflow), source-attribution rule (Unified.to + Greenhouse/Ashby/Lever docs), diversity intentional vs aspirational (Project Include + MindHunt AI), warm-intro vs cold benchmark (Salesflow + LinkedIn's 78% acceptance lift) | Each rule traces to a benchmark or playbook |
| Mode-specific decisions | Same per-mode sources as When-invoked, with quality bars sourced from 2026 published benchmarks | |
| Quality gates | Cross-source synthesis of 2026 sourcing-craft completion definitions | |
| Output format | Notion / Mailchimp / Google Sheet / Greenhouse Harvest doc patterns + 2026 dashboard convention | |
| Communication style | Synthesized from ConnectSafely + Salesflow + Expandi InMail templates + 2026 reply-rate data | |
| When to push back / defer | Hand-off rules per agent catalog adjacency (operations-agent parent + ceo-agent + marketing-agent + legal-counsel + senior-python-engineer + sales-agent) | Operational glue per CraftBot agent catalog |
| PROACTIVE self-init footer | `METHODOLOGY.md` standard footer | Same wording across all agents; role-specific questions only |

## role.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Capability reference (channels by role family) | 2026 sourcing tool comparison articles (SelectSoftware Reviews, Leonar, Metaview, Lupahire, Recruitingtoolsreview, Glozo, Proficiently) | Comprehensive 2026 landscape |
| Sourcing aggregator capabilities (SeekOut / Findem / AmazingHiring / hireEZ / Gem / Beamery / Phenom / Eightfold / Loxo / Leonar / Juicebox) | Vendor sites + 2026 review articles | Per-tool capability summary |
| Contact finder API matrix | Findymail comparison + Knowlee 2026 article + per-vendor docs | Includes API-supported tools only |
| Cold InMail benchmarks 2026 | ConnectSafely + Salesflow + Careery + Expandi | 2026 reply-rate by function + InMail levers |
| ATS handoff matrix | Greenhouse Harvest docs + Ashby docs + Lever API + Workable + Zoho Recruit + SmartRecruiters + Unified.to comparison | Per-ATS candidate-create + source-attribution endpoints |
| LinkedIn 40-filter reference | LinkedIn Recruiter + Sales Nav 2026 product docs + Talentprise guide | |
| LinkedIn Recruiter Boolean library | Talentprise 2026 guide + hireEZ + Built In + per-role-family pattern synthesis | Battle-tested patterns |
| GitHub search operator reference | docs.github.com + hireEZ + Kula + Built In recruiting articles | API + UI patterns |
| Stack Exchange API recipes | api.stackexchange.com docs + HeroHunt sourcing article | |
| Cold InMail template library | Per-segment templates synthesized from ConnectSafely + Salesflow + Careery + Expandi + 2026 reply-rate benchmarks | Tested patterns; char-counted |
| Sequence pattern by role | Gem / hireEZ documented patterns + 2026 multi-stage benchmarks | 4-5 touch per role family |
| Hot-list segmentation patterns | Beamery + Gem + Phenom tagging conventions + 2026 talent-community articles | |
| Target-company mapping playbook | Crunchbase + Apollo + Layoffs.fyi pattern from 2026 account-based sourcing articles | |
| Exec sourcing playbook | Lusha + RocketReach + ContactOut docs + 2026 exec-search articles | Warm-intro emphasis |
| Diversity channel relationship playbook | /dev/color + Code2040 + Lesbians Who Tech + Out in Tech + Latinas in Tech + Out & Equal + AfroTech + Grace Hopper + Tapia + Project Include community sites + 2026 diversity-sourcing articles | |
| Boomerang re-engagement playbook | KS Agents + PeoplePath + Beamery alumni articles + 35% 2025 hire benchmark + Bain $4,200/hire savings stat | |
| Source-of-hire dashboard schema | ATS REST documentation + 2026 source-of-hire reporting articles + Metaview / Lupahire benchmarks | |
| ATS handoff API recipes | Greenhouse Harvest + Ashby + Lever + Zoho Recruit per-vendor docs | curl recipes |
| Contractor marketplace routing matrix | Lemon.io + Second Talent + DistantJob 2026 comparison articles | Per-vendor speed + cost + sweet spot |
| JD optimization checklist | Textio + Datapeople 2026 articles + Ongig competitor article + manual-checklist fallback synthesis | Free fallback for paid platforms |
| Antipattern catalog | Synthesized from sourcing-craft canon + 2026 reply-rate failure-mode articles | BAD/GOOD pairs per common mistake |
| SOTA tool reference (June 2026) | Per-tool docs + 2026 review articles (one H3 per tool) | Generated from SOTA_USE_CASES.md |
| SOTA execution playbook table | Built from skill-pack-to-use-case mapping | Decision routing |
| Brief / Output templates | Synthesized from 2026 best-practice sourcing docs | Sourcing strategy brief + candidate brief + dashboard |

## SOTA tool sources (June 2026)

> One row per SOTA tool referenced in the agent.

| Tool | Source URL | Used for |
|---|---|---|
| LinkedIn Recruiter / Sales Navigator | https://business.linkedin.com/talent-solutions/recruiter + https://developer.linkedin.com/product-catalog/talent | Primary sourcing channel, Boolean authoring, 40-filter layering, InMail outreach |
| LinkedIn Boolean Guide 2026 | https://www.talentprise.com/linkedin-boolean-search-guide/ | Boolean string patterns ≤1,000 chars, nested operators |
| Unipile (LinkedIn API proxy) | https://www.unipile.com/linkedin-recruiter-search-api-guide-for-developers-and-editors/ | Recruiter Search API access path for non-Partner recipients |
| RecruitAI Suite | https://recruitaisuite.com/products/linkedin-automation-api/ | Alt LinkedIn Recruiter API automation surface |
| GitHub REST + GraphQL | https://docs.github.com/en/rest/search/search | User/repo/commit search; 180M+ active developers |
| hireEZ GitHub Sourcing Guide | https://explore.hireez.com/blog/how-to-source-candidates-on-github/ | Developer mining 2026 + AI Boolean builder + 45+ platform aggregation |
| Built In GitHub Advanced Search | https://builtin.com/recruiting/github-advanced-search | Recruiter-facing GitHub operator syntax |
| Kula GitHub Sourcing | https://www.kula.ai/blog/github-beginners-guide-source-candidates | 2026 GitHub sourcing patterns |
| Stack Exchange API | https://api.stackexchange.com/docs | Stack Overflow reputation + top-tag search |
| Stack Overflow Talent Discontinuation | https://totalent.eu/stack-overflow-exits-the-talent-acquisition-sphere-announces-plans-to-discontinue-jobs/ | Jobs discontinued 2022 context |
| HeroHunt Stack Overflow Sourcing | https://www.herohunt.ai/blog/how-to-source-tech-talent-on-stack-overflow/ | Reputation + tag sourcing pattern |
| SeekOut | https://juicebox.ai/blog/seekout-reviews + https://skima.ai/blog/product-deep-dives/seekout-review | 800M+ DB, 330M underrepresented, diversity filters, SeekOut Assist |
| Findem | https://www.findem.ai/ | Attribute-based filters, people-as-data graph |
| AmazingHiring | https://amazinghiring.com | 50+ developer network aggregation |
| hireEZ | https://explore.hireez.com/ + https://www.metaview.ai/resources/blog/hireez-alternatives | AI Boolean builder + 45-platform aggregation + sequencing |
| Gem | https://www.selectsoftwarereviews.com/reviews/gem + https://www.gem.com/blog/candidate-sourcing-software | 800M+ DB + AI-first + sequencing + Chrome extension |
| Beamery | https://beamery.com/platform/talent-acquisition/talent-crm/ + https://beamery.com/resources/blogs/why-enterprise-organizations-need-an-alumni-hiring-strategy | Enterprise CRM + alumni strategy |
| Phenom | https://www.phenom.com/ + https://www.industrylabs.ai/articles/phenom-review | Talent Experience Platform (career site + chatbot + CRM + CMS + AI scheduling) |
| Eightfold AI | https://www.goperfect.com/blog/10-best-eightfold-ai-alternatives-for-talent-intelligence-in-2026 | Talent intelligence + silver-medalist + alumni re-engagement |
| Symphony Talent (SmashFly) | https://www.metaview.ai/resources/blog/candidate-sourcing-tools | CRM + career sites + programmatic job advertising |
| Loxo / Leonar / Juicebox | https://www.leonar.app/blog/best-talent-sourcing-platforms/ + https://juicebox.ai/blog/2026-guide-to-the-top-candidate-sourcing-tools-for-recruiters | Mid-market AI sourcing alternatives |
| Apollo.io | https://www.apollo.io/product/api + https://pipeline.zoominfo.com/sales/crunchbase-vs-apollo | 275M+ contacts + company graph |
| Crunchbase Enterprise | https://www.crunchbase.com/api | 4M+ private companies + predictive signals |
| RocketReach | https://rocketreach.co/ + https://www.findymail.com/blog/best-email-finder-tools/ | 700M+ professional contacts + confidence scoring |
| Lusha | https://www.lusha.com/api | Verified executive direct phones + emails |
| Hunter.io | https://hunter.io/api | Real free tier + email verification |
| Snov.io | https://snov.io/api | Public API + verification + multi-touch outreach |
| Findymail | https://www.findymail.com/ | <5% bounce rate + Sales Nav Chrome extension |
| AnyMail Finder | https://anymailfinder.com/api | Public API + bulk lookup |
| ContactOut | https://derrick-app.com/tools/contactout-review | Alt email + cell phone lookup |
| FullEnrich | https://fullenrich.com/ | Data pipeline (Snowflake / dbt) integration |
| Derrick | https://derrick-app.com/en/linkedin-email-finder-comparison-2026/ | Newer high-accuracy LinkedIn-tied lookup |
| Wellfound (formerly AngelList Talent) | https://wellfound.com/recruit/pricing + https://www.remotejobassistant.com/blog/wellfound-review | 35K+ companies + 10M+ candidate profiles + free for startups |
| Built In | https://www.glozo.com/blog/niche-it-job-boards-recruiters-2025 + https://proficiently.com/blog/best-tech-job-boards/ | US tech metros (Chicago, Austin, NYC, LA, Boston) |
| Hired | https://www.glozo.com/blog/niche-it-job-boards-recruiters-2025 | Curated two-sided matching |
| Otta | https://www.glozo.com/blog/niche-it-job-boards-recruiters-2025 | Curated startup roles + candidate-ranked |
| Y Combinator Work at a Startup | https://www.workatastartup.com/ | YC-only, highest signal |
| RepVue | https://www.repvue.com/employers + https://www.repvue.com/blog/sales-salary-guide + https://www.repvue.com/blog/how-hubspot-uses-repvue-to-source-top-tier-sales-talent | Sales talent sourcing + 2026 comp benchmarks |
| Behance | https://www.behance.net/dev + https://amazinghiring.com/blog/searching-for-designers-on-dribbble-and-behance | Long-form designer case studies; Hire Me filter |
| Dribbble | https://dribbble.com/api + https://www.twine.net/blog/best-dribbble-alternatives-to-hire-top-designers/ | Designer shots + for-hire filter |
| Twine | https://www.twine.net/ | Designer marketplace alt to Dribbble |
| Toptal | https://www.toptal.com/ + https://lemon.io/blog/toptal-alternatives/ | Top 3% vetted freelancer marketplace |
| Turing | https://www.turing.com/ + https://distantjob.com/blog/toptal-alternatives-hire-remote-developers/ | 24h match + 40-60% below Toptal |
| Andela | https://andela.com/ + https://www.1840andco.com/blog/andela-alternatives | Africa-focused full-team builder |
| Arc.dev | https://arc.dev/ + https://arc.dev/employer-blog/toptal-alternatives/ | 1% accept + AI matching |
| Lemon.io | https://lemon.io/ + https://www.secondtalent.com/alternatives/lemon-io/ | Startup-focused EU/LatAm 24-48h |
| Pesto | https://pesto.tech/ | Indian senior eng |
| Distributed | https://distributed.team/ | Full distributed team-build |
| Textio | https://textio.com/products/recruiting + https://www.index.dev/blog/textio-review | Outcome-based JD language guidance |
| Datapeople | https://datapeople.io/ + https://datapeople.io/comparison/datapeople-vs-textio/ | JD readability + template enforcement |
| Joonko / Atomic AI | https://blog.ongig.com/job-descriptions/textio-competitors/ | Free JD bias scorers (alternatives to Textio/Datapeople) |
| Greenhouse Harvest API | https://developers.greenhouse.io/harvest.html | ATS candidate-create + source-attribution |
| Ashby API | https://developers.ashbyhq.com/ | ATS candidate-create + analytics-first |
| Lever API | https://hire.lever.co/developer/documentation | ATS candidate-create + CRM module |
| Workable API | https://workable.readme.io/ | ATS alt for SMB recipients |
| Zoho Recruit API | https://www.zoho.com/recruit/developer-guide/ | ATS for Zoho-shop recipients |
| SmartRecruiters API | https://developers.smartrecruiters.com/ | ATS enterprise alt |
| ConnectSafely InMail Templates 2026 | https://connectsafely.ai/articles/linkedin-inmail-templates-response-rates-2026 | 2026 InMail reply rate benchmarks (18-25%); <400 char + 16-27 subject |
| Salesflow InMail Best Practices 2026 | https://salesflow.io/blog/linkedin-inmail-best-practices-improve-response-rates | 78% lift from profile-view-first; AI assist 69% lift since April 2026; per-function reply rates |
| Careery Recruiter Outreach Templates | https://careery.pro/blog/recruiter-outreach-templates | Per-segment 2026 InMail + email templates |
| Expandi Recruiter Message Templates 2026 | https://expandi.io/blog/linkedin-recruiter-message-templates/ | Per-segment templates + warm-intro patterns |
| /dev/color | https://devcolor.org | Black engineers community channel |
| Code2040 | https://www.code2040.org | Early-career Black + Latine technical talent |
| Lesbians Who Tech | https://lesbianswhotech.org | LGBTQ+ technical community + annual summit |
| Out in Tech | https://outintech.com | LGBTQ+ tech community + biannual events |
| Latinas in Tech | https://latinasintech.org | Latine technical community + annual summit |
| Out & Equal | https://outandequal.org | LGBTQ+ workplace community + annual summit |
| AfroTech | https://experience.afrotech.com | Black tech professional community + annual conference |
| Grace Hopper Celebration | https://anitab.org/event/2026-grace-hopper-celebration-india/ | Women-in-tech largest annual conference (AnitaB.org) |
| Tapia Conference | https://tapiaconference.cmd-it.org/ | URM-in-computing annual conference |
| Project Include | https://projectinclude.org | Diversity-of-thought best practices over recruiting process |
| KS Agents Boomerang Strategy | https://ks-agents.com/blog/boomerang-employees-alumni-network-strategy/ | 35% of 2025 hires boomerangs; alumni network ROI |
| PeoplePath Alumni Network | https://peoplepath.com/blog/attract-and-rehire-boomerang-employees-through-your-corporate-alumni-network/ | Alumni outreach cadence + DB schema |
| Enterprise Alumni | https://enterprisealumni.com/news/new-skills | Boomerang skill upgrade tracking |
| HR Morning Boomerang Trend | https://www.hrmorning.com/articles/boomerang-employees/ | 2026 boomerang retention strategy |
| Layoffs.fyi | https://layoffs.fyi/ | Layoff signal for target-account sourcing |
| Pave / Carta Total Comp / Levels.fyi | https://www.pave.com/ + https://carta.com/blog/total-comp/ + https://www.levels.fyi/ | Comp benchmarks for executive offer framing (hand off to ceo-agent) |
| Unified.to ATS APIs 2026 | https://unified.to/blog/15_ats_apis_to_integrate_with_in_2026_greenhouse_lever_workable | ATS landscape + REST surfaces + source-of-hire patterns |
| Index Greenhouse vs Lever vs Ashby | https://www.index.dev/blog/greenhouse-vs-lever-vs-ashby-ats-comparison | ATS handoff target selection |
| Outsail Greenhouse vs Lever vs Ashby | https://www.outsail.co/post/greenhouse-vs-lever-vs-ashby | ATS positioning |
| SelectSoftware Reviews Sourcing Tools 2026 | https://www.selectsoftwarereviews.com/buyer-guide/best-candidate-sourcing-tools | Sourcing tool buyer guide |
| Leonar Sourcing Platforms 2026 | https://www.leonar.app/blog/best-talent-sourcing-platforms/ | Per-team-size sourcing tool comparison |
| Juicebox Sourcing Tools 2026 | https://juicebox.ai/blog/2026-guide-to-the-top-candidate-sourcing-tools-for-recruiters | Natural-language search adoption + 2026 landscape |
| Metaview Sourcing Tools 2026 | https://www.metaview.ai/resources/blog/sourcing-tools-for-recruiters + https://www.metaview.ai/resources/blog/recruiting-trends | 10 top sourcing tools + 2026 recruiting trends |
| Lupahire Sourcing Tools 2026 | https://www.lupahire.com/blog/candidate-sourcing-tools-for-recruiters | 20 best sourcing tools + multi-channel diversification |
| Recruitingtoolsreview Sourcing 2026 | https://recruitingtoolsreview.com/blog/comparison-guide-candidate-sourcing-tools-for-recruiters-2026 | Per-platform 2026 comparison |
| MindHunt AI Diversity Sourcing | https://mindhuntai.com/blog/diversity-sourcing-strategies | Diversity-sourcing 2026 strategies + best tools |
| WebHR Diversity Sourcing | https://web.hr/contents/diversity-sourcing-strategy | 12 diversity sourcing strategies 2026 |

## Notes on authored-from-synthesis

Sections that aren't directly lifted from a single source (rare — should always be operational glue, not domain claims):

- The 25 use case mappings in `reference/SOTA_USE_CASES.md` — each maps to ≥1 of the SOTA sources above. The agent's execution path is the synthesis layer (which `cli-anything` call + which MCP), not the domain claim itself.
- The Boolean strings in `role.md` "LinkedIn Recruiter Boolean library" — patterns synthesized from Talentprise + hireEZ + Built In sources, role-family-specific variations authored from per-role ICP knowledge.
- The InMail templates in `role.md` "Cold InMail template library" — char-counted, synthesized from ConnectSafely + Salesflow + Careery + Expandi 2026 templates.
- The sequence patterns in `role.md` — synthesized from Gem + hireEZ documented patterns + 2026 multi-stage benchmarks.

## Refreshing from upstream

When SOTA tools change (e.g., LinkedIn API tier change, SeekOut acquisition, new sourcing platform launch):
1. Update the relevant skill pack(s) in `agents/talent-sourcer/skills/<name>/SKILL.md`.
2. Update the SOTA sources table above.
3. Update `reference/SOTA_USE_CASES.md` confidence ratings if applicable.
4. Re-run `python verify.py talent-sourcer` to confirm structure intact.
5. Re-build: `python build.py talent-sourcer` produces a fresh `.craftbot`.

For the canonical reference repos (Step 2):
- `wshobson/agents` — repull every quarter for SOTA agent definitions.
- `VoltAgent/awesome-claude-code-subagents` — same cadence.
- `msitarzewski/agency-agents` — same cadence.
- Per-quarter check on SeekOut / Findem / AmazingHiring / hireEZ / Gem / Beamery pricing, API changes, and new feature releases (these tools move fast).
- Monthly check on LinkedIn Recruiter pricing tier changes and Talent Solutions API access tiers.
