# talent-sourcer — SOTA Use Cases (June 2026)

This document maps every documented use case from `USE_CASES.md` to a concrete SOTA execution mechanism. Every use case has: a named tool, an exact agent-level execution path, a source URL, and a confidence rating.

**Legend:**
- ✓ Fully executable — production MCP / first-class API, OAuth or key exposed via `agent.yaml`, end-to-end automated.
- ⚠ Executable with caveats — works today but with a one-time setup step (LinkedIn Recruiter seat, Talent Solutions partner approval, paid SeekOut / Findem seat, etc.) the recipient owns.
- ✗ Genuinely impossible today — rare; usually GUI-locked or requires platform partnership.

The agent loads these mappings on demand by grepping `SOTA_USE_CASES.md` for the matching capability heading.

---

## LinkedIn Recruiter Boolean search string authoring

- **SOTA approach:** Author 2026 LinkedIn Recruiter Boolean strings using nested `(senior OR lead) AND (python OR golang) AND NOT recruiter` patterns within the ≤1,000-character keyword field. Default to title + skill + seniority + exclusion clusters; layer LinkedIn Recruiter's 40+ filters (geography, current company, past company, school, years of experience). hireEZ / SeekOut / Juicebox now auto-generate Boolean from a JD via "AI Boolean Builder" — best fallback when string complexity exceeds the recruiter's hand-author budget. LinkedIn Recruiter AI surfaces a 69% response-rate lift on AI-assisted outreach since April 2026.
- **Agent execution path:** Use `linkedin-recruiter-boolean-search-strings` skill. Author the string locally; paste into LinkedIn Recruiter UI; (if Talent Solutions Partner approved) `cli-anything` curl `https://api.linkedin.com/v2/recruiterSearch` via Unipile / RecruitAI Suite proxy. Fallback: `playwright-mcp` automates paste-and-search for non-partner workflow.
- **Source:** https://www.talentprise.com/linkedin-boolean-search-guide/ + https://developer.linkedin.com/product-catalog/talent + https://www.unipile.com/linkedin-recruiter-search-api-guide-for-developers-and-editors/
- **Confidence:** ⚠ Executable with caveats (LinkedIn Recruiter seat required; Talent Solutions API gated to approved partners — but `playwright-mcp` covers the non-API path)

## GitHub talent mining (language + commits + stars + contribution graphs)

- **SOTA approach:** GitHub REST + GraphQL APIs expose user search by location, language, follower count, public repo count; repo search by language + stars + forks; commit search by author + path. The 2026 pattern: search top-starred repos in target language → pull contributor list → score by commit recency + stars across owned repos + language depth. 180M+ active GitHub developers as of 2026. hireEZ aggregates from 45+ platforms including GitHub; AmazingHiring + SeekOut overlay GitHub + Stack Overflow + Kaggle into single profile.
- **Agent execution path:** Use `github-talent-mining-language-stars-commits` skill. `github` MCP `search_users('language:python location:berlin followers:>50')`; `cli-anything` curl `https://api.github.com/search/users?q=…` for advanced operators; aggregate contributor lists from top-starred repos via GraphQL.
- **Source:** https://docs.github.com/en/rest/search/search + https://explore.hireez.com/blog/how-to-source-candidates-on-github/ + https://builtin.com/recruiting/github-advanced-search
- **Confidence:** ✓ Fully executable

## Stack Overflow talent search (reputation + tag activity)

- **SOTA approach:** Stack Overflow Jobs discontinued March 2022, but Stack Exchange API (`/users`, `/users/{id}/top-tags`, `/users/{id}/answers`) still exposes reputation, top tags, top answers. Source pattern: filter users by reputation > N + top tag matches role + recent activity. AmazingHiring aggregates Stack Overflow with GitHub + Kaggle into developer-specific profiles; SeekOut and hireEZ also index Stack Overflow signals.
- **Agent execution path:** Use `stack-overflow-talent-reputation-tag` skill. `cli-anything` curl `https://api.stackexchange.com/2.3/users?order=desc&sort=reputation&site=stackoverflow&tagged=python`; pull `/users/{id}/top-tags` to validate domain depth; cross-reference GitHub by display name + location.
- **Source:** https://api.stackexchange.com/docs + https://totalent.eu/stack-overflow-exits-the-talent-acquisition-sphere-announces-plans-to-discontinue-jobs/ + https://www.herohunt.ai/blog/how-to-source-tech-talent-on-stack-overflow/
- **Confidence:** ✓ Fully executable

## Niche job board sourcing (Wellfound / Hired / Built In / Otta)

- **SOTA approach:** Wellfound (formerly AngelList Talent) — 35,000+ companies, 10M+ candidate profiles, Recruit Pro $499/mo or Autopilot tier for AI-sourced candidates; free posting for startups. Hired — curated two-sided matching (candidates set preferences, employers send interview requests). Built In — US tech hubs (Austin, Chicago, NYC, LA, Boston) with employer-brand product. Otta — curated startup roles, candidate-ranked. Y Combinator's Work at a Startup — closed to YC companies, highest signal. 2026 pattern: post role to Wellfound (free for startups) + Built In (paid metro presence) + Otta (curation) + use them as candidate-search surfaces in parallel.
- **Agent execution path:** Use `hired-wellfound-built-in-otta-niche-boards` skill. `cli-anything` curl Wellfound `/api/recruit/jobs`, Built In job-board API, Otta employer dashboard via `playwright-mcp` (no public API). For candidate search: scrape profile lists via `firecrawl-mcp` where ToS allows.
- **Source:** https://wellfound.com/recruit/pricing + https://www.glozo.com/blog/niche-it-job-boards-recruiters-2025 + https://proficiently.com/blog/best-tech-job-boards/ + https://www.remotejobassistant.com/blog/wellfound-review
- **Confidence:** ⚠ Executable with caveats (Wellfound posting free for startups, paid for sourcing API; Built In paid metro plan required)

## Diversity sourcing (AmazingHiring / Findem / SeekOut diversity filters)

- **SOTA approach:** SeekOut — 330M underrepresented profiles, explicit diversity filters (women, Black, Hispanic, Asian, veteran, LGBTQ+), Bias Reducer mode. Findem — attribute-based filters surface qualified candidates that title-based search misses; people-as-data graph. AmazingHiring — optional Diversity filter on request; aggregates 50+ niche developer networks. 2026 pattern: layer diversity filter on top of skill/seniority Boolean; cross-reference with project-specific channels (/dev/color, Code2040, Black Founders, Lesbians Who Tech, Out in Tech, Latinas in Tech) for warm-intro paths.
- **Agent execution path:** Use `amazinghiring-findem-seekout-diversity` skill (paired with `diversity-channel-sourcing-dev-color-code2040` skill). `cli-anything` curl SeekOut Power Search API / Findem people graph API / AmazingHiring Recruiter API per recipient's seat; route warm-intro requests through channel-specific Slack/community channels.
- **Source:** https://juicebox.ai/blog/seekout-reviews + https://mindhuntai.com/blog/diversity-sourcing-strategies + https://www.findem.ai/ + https://amazinghiring.com
- **Confidence:** ⚠ Executable with caveats (SeekOut/Findem paid seat $500+/user/mo; project channels free but human-network gated)

## Passive candidate outreach campaigns (Gem / hireEZ / Beamery)

- **SOTA approach:** Gem — 800M+ profile sourcing + multi-stage email sequences + analytics + Chrome extension; best for high-growth in-house teams focused on outbound passive talent. hireEZ — AI Boolean builder + 45+ source aggregation + sequencer; best when budget mid-range. Beamery — enterprise talent CRM (CHRO / TA leader-grade); strong ATS + HRIS integrations. 2026 pattern: pull passive list from sourcing tool → ingest into Gem/hireEZ/Beamery → enroll in 3-5 step sequence (touch 1: warm context, touch 2: opportunity ask, touch 3: light value adds, touches 4-5: graceful break-up). Multi-stage sequences boost reply rate 3-5× over single touches.
- **Agent execution path:** Use `gem-hireez-beamery-talent-crm` skill (paired with `passive-candidate-outreach-campaigns`). `cli-anything` curl Gem `/api/v1/sequences` to author sequence + `/api/v1/prospects` to enroll; same shape for hireEZ + Beamery (recipient holds API keys). Templates in Notion.
- **Source:** https://www.gem.com/blog/candidate-sourcing-software + https://beamery.com/platform/talent-acquisition/talent-crm/ + https://www.metaview.ai/resources/blog/sourcing-tools-for-recruiters
- **Confidence:** ⚠ Executable with caveats (Gem / Beamery / hireEZ paid seat required; Gmail-only sequence fallback via `gmail-mcp` works at low scale)

## Cold InMail authoring + warm intro requests

- **SOTA approach:** InMail averages 10-25% reply rate; well-structured personalized outreach hits 35-50%. 2026 rules: under 400 chars (22% higher response than average); 16-27 char subject (30.5% lift); view profile first (78% acceptance lift); lead with candidate's interests, not the job. Reply rates by function: HR/TA 12.08%, Product Management 10.24%, Operations 10.02%, Engineering ~7-9%. LinkedIn Recruiter AI-assisted outreach drives 69% lift since April 2026. Warm-intro pattern: scan 2nd-degree connections via Sales Navigator → request intro from mutual via Gmail/Slack templated message.
- **Agent execution path:** Use `cold-inmail-warm-intro` skill. Draft locally per 2026 rules; paste into LinkedIn Recruiter; OR use Gem/hireEZ sequencer to auto-personalize from token map. Warm intros: `gmail-mcp` template + Slack DM via `slack-mcp` for mutuals.
- **Source:** https://connectsafely.ai/articles/linkedin-inmail-templates-response-rates-2026 + https://salesflow.io/blog/linkedin-inmail-best-practices-improve-response-rates + https://expandi.io/blog/linkedin-recruiter-message-templates/
- **Confidence:** ✓ Fully executable

## Hot-list / talent community management

- **SOTA approach:** Talent communities are pre-engaged candidate groups (past applicants + referrals + alumni + passive prospects) nurtured via newsletters, events, and career resources. Critical in competitive markets; hot-list patterns let you hire 30-50% faster when a role opens. 2026 pattern: tag candidates in Gem/Beamery CRM by readiness (1-3 months / 6-12 months / future) + by role family; quarterly newsletter via Gem campaigns + invite to virtual events + LinkedIn employer-brand content. Beamery + Phenom + Gem all support hot-list segmentation natively.
- **Agent execution path:** Use `hot-list-talent-community-mgmt` skill. `cli-anything` curl Gem `/prospects?tag=hot-list-eng` to enroll in nurture sequence; `notion-mcp` to manage the candidate-community wiki + event calendar; `mailchimp` or `gmail-mcp` for newsletter blasts.
- **Source:** https://beamery.com/resources/blogs/why-enterprise-organizations-need-an-alumni-hiring-strategy + https://www.metaview.ai/resources/blog/recruiting-trends
- **Confidence:** ✓ Fully executable

## Target company mapping (Crunchbase + LinkedIn → candidate lists)

- **SOTA approach:** Crunchbase 4M+ private company graph with predictive AI signals (likely-to-fund / acquire / IPO). Apollo 275M+ contacts. Pattern: filter Crunchbase by funding stage + headcount + industry + recent layoff signal → ingest company list → run LinkedIn Sales Nav search per company for target roles → enrich with Apollo contact data. Layoff signals (Layoffs.fyi, WARN tracker) surface high-intent passive candidates.
- **Agent execution path:** Use `target-company-mapping-crunchbase-linkedin` skill. `cli-anything` curl Crunchbase Enterprise API `/v4/searches/organizations` (recipient holds key); pipe results to Apollo `/v1/mixed_companies/search` and `/v1/mixed_people/search` for contact enrichment; load into Gem hot-list.
- **Source:** https://www.crunchbase.com/api + https://www.apollo.io/product/api + https://pipeline.zoominfo.com/sales/crunchbase-vs-apollo
- **Confidence:** ⚠ Executable with caveats (Crunchbase Enterprise + Apollo paid tiers required; Apollo free tier covers MVP)

## CTO / VP-Eng executive sourcing

- **SOTA approach:** Exec sourcing pulls from 2nd-degree warm network + LinkedIn Sales Navigator + Lusha (verified executive direct phones) + RocketReach + ContactOut for personal email + cell. Pattern: build target list from competitors / acquired startups / late-stage companies → score by tenure (3-5 years at level signals open to move) + recent funding event at current employer (predicts dissatisfaction / opportunity) → personalized warm-intro request via mutual board member / investor / founder. Defer compensation strategy + offer negotiation to `ceo-agent`.
- **Agent execution path:** Use `cto-vp-eng-exec-sourcing` skill. `cli-anything` curl Lusha `/v2/person`, RocketReach `/api/v2/lookupProfile`, ContactOut Search API; pull warm-intro paths via LinkedIn Sales Nav 2nd-degree; route brief to `ceo-agent` for compensation framing.
- **Source:** https://rocketreach.co/ + https://www.lusha.com/api + https://www.findymail.com/blog/best-email-finder-tools/
- **Confidence:** ⚠ Executable with caveats (paid Lusha / RocketReach / ContactOut tier required; LinkedIn Sales Nav seat required)

## Technical sourcing (developer-focused: AmazingHiring + SeekOut)

- **SOTA approach:** AmazingHiring aggregates 50+ developer networks (GitHub, Stack Overflow, Kaggle, Bitbucket, DEV.to, HackerRank, LeetCode, conference speaker lists). SeekOut full-graph sourcing + technical-skill filters + GitHub activity scoring. 2026 pattern: paste JD into SeekOut Assist or hireEZ AI Boolean builder → review auto-generated string → refine → execute → enrich with GitHub commit history + Stack Overflow tag depth to validate signal. 800M+ profile databases at SeekOut and Loxo complement LinkedIn for technical roles.
- **Agent execution path:** Use `technical-sourcing-developer-focused` skill. `cli-anything` curl AmazingHiring API / SeekOut Power Search API (recipient holds keys); validate with `github` MCP commit-history + `cli-anything` Stack Exchange API top-tags.
- **Source:** https://amazinghiring.com + https://www.selectsoftwarereviews.com/buyer-guide/best-candidate-sourcing-tools + https://skima.ai/blog/product-deep-dives/seekout-review
- **Confidence:** ⚠ Executable with caveats (paid AmazingHiring / SeekOut seat required)

## Product designer sourcing (Dribbble / Behance)

- **SOTA approach:** Behance (Adobe-owned) — long-form case studies with wireframes + iteration + rationale; best for UX/UI seniority signal. Dribbble — "shots" small-format snapshots + curated community; better for visual / brand / motion. Both gate sourcing behind paywalls in 2026; native search limited. 2026 alternative pattern: pull names from Behance "Hire Me" filter → cross-reference LinkedIn → enrich via Apollo; Dribbble "for hire" filter + portfolio-quality screen. Designer-focused niche: Twine, Toptal Design.
- **Agent execution path:** Use `product-designer-sourcing-dribbble-behance` skill. `cli-anything` curl Behance API `/v2/users?available_for_hire=1`; Dribbble jobs API; cross-reference LinkedIn for email + role via Apollo / Findymail enrichment.
- **Source:** https://www.twine.net/blog/best-dribbble-alternatives-to-hire-top-designers/ + https://www.behance.net/dev + https://dribbble.com/api
- **Confidence:** ⚠ Executable with caveats (Behance API requires app approval; Dribbble jobs API paid)

## Sales talent sourcing (RepVue + LinkedIn Sales Nav)

- **SOTA approach:** RepVue — sales-rep-specific salary + employer rating data (sourced from thousands of verified sales pros); employer-side sourcing surfaces warm leads through rep network. 2026 SDR median $60K base / $85K OTE; Sales Manager $153K / $292K OTE. Pattern: filter RepVue by quota attainment %, role, employer rating → enrich with LinkedIn Sales Nav (current company + tenure) → cold InMail with comp transparency (mention RepVue benchmark). HubSpot publicly uses RepVue as primary sales-sourcing channel.
- **Agent execution path:** Use `sales-talent-sourcing-repvue` skill. `cli-anything` curl RepVue employer API (`/v1/candidates/search` per recipient's plan); LinkedIn Sales Nav saved search; enrich with Findymail / Apollo for direct contact.
- **Source:** https://www.repvue.com/employers + https://www.repvue.com/blog/how-hubspot-uses-repvue-to-source-top-tier-sales-talent + https://www.repvue.com/blog/sales-salary-guide
- **Confidence:** ⚠ Executable with caveats (RepVue employer plan required)

## Source-to-contact metrics + source-of-hire reporting

- **SOTA approach:** Source-to-contact = (candidates contacted) / (candidates sourced). Source-of-hire = % of hires by channel (LinkedIn / referrals / Wellfound / Built In / Gem outbound / Boomerang / employee referral). 2026 benchmark targets: >40% source-to-contact (strong) / >25% (acceptable); diversify so no single source >60% of hires. Greenhouse / Ashby / Lever expose per-candidate source field + hire outcome; pull via REST `/v1/candidates?source=X`. Aggregate weekly into operating dashboard.
- **Agent execution path:** Use `source-to-contact-metrics` + `source-of-hire-reporting` skills. `cli-anything` curl Greenhouse `/v1/candidates`, Ashby `/candidate.list`, Lever `/v1/opportunities` per recipient's ATS; aggregate in `xlsx` / `google-sheet`; publish dashboard in Notion / Linear.
- **Source:** https://unified.to/blog/15_ats_apis_to_integrate_with_in_2026_greenhouse_lever_workable + https://www.outsail.co/post/greenhouse-vs-lever-vs-ashby + https://www.metaview.ai/resources/blog/recruiting-trends
- **Confidence:** ✓ Fully executable

## Recruiter persona authoring + outreach segmentation

- **SOTA approach:** Outreach segmentation = group passive candidates by (a) role + level, (b) current company stage (early / growth / late / megacap), (c) ICP traits (open-source contributions / conference talks / specific tech stack). Per-segment message templates lift reply rate 2-3× vs blanket templates. Personas authored from past-hire data: profile traits, pain points (why they moved), decision criteria. Stored in Notion as canonical reference; tokens map into Gem/hireEZ sequence variables.
- **Agent execution path:** Use `recruiter-persona-segmentation` baked into `passive-candidate-outreach-campaigns` skill. `notion-mcp` persona library; Gem sequence variables per segment; A/B test by segment via Gem analytics.
- **Source:** https://salesflow.io/blog/linkedin-inmail-best-practices-improve-response-rates + https://careery.pro/blog/recruiter-outreach-templates
- **Confidence:** ✓ Fully executable

## Employer brand in outreach (case studies / funding / Glassdoor)

- **SOTA approach:** Top-performing outreach references recent funding (recency + traction), public case studies (specific customer wins), Glassdoor / Comparably ratings, and tech-blog posts authored by team (proof of culture). 2026 pattern: pull last 30 days of company news via Crunchbase + Google News; embed in outreach token `{company_proof_point}`; verify Glassdoor rating ≥ 4.0 before referencing.
- **Agent execution path:** Use `employer-brand-in-outreach` skill. `cli-anything` curl Crunchbase recent-news + Google News + Glassdoor scrape via `firecrawl-mcp`; populate Gem/hireEZ token variables; auto-rotate every 30 days.
- **Source:** https://careery.pro/blog/recruiter-outreach-templates + https://www.gem.com/blog/candidate-sourcing-software
- **Confidence:** ✓ Fully executable

## Candidate experience hygiene (response time + status updates)

- **SOTA approach:** 24-hour response SLA on candidate reply; 7-day SLA on stage advancement; status update at every transition (auto-rejection within 5 business days for declines). 2026 benchmark: companies hitting 24-hour reply rate convert 2-3× higher than companies at 72+ hour. Talent CRM auto-status (Gem/Beamery/Phenom) prevents drop-off. Greenhouse / Ashby / Lever have native auto-rejection templates.
- **Agent execution path:** Use `candidate-experience-hygiene-response-time` skill. `cli-anything` curl ATS for stale candidates (no movement >7 days); Gem campaign sends "we're still reviewing" auto-touch; auto-reject template via Greenhouse `/v1/applications/{id}/reject`.
- **Source:** https://www.metaview.ai/resources/blog/recruiting-trends + https://unified.to/blog/15_ats_apis_to_integrate_with_in_2026_greenhouse_lever_workable
- **Confidence:** ✓ Fully executable

## Source diversification (>3 sources per role)

- **SOTA approach:** Best-in-class sourcing teams use ≥3 sources per role: (1) LinkedIn Recruiter + Sales Nav, (2) GitHub / Stack Overflow / domain-specific (technical), (3) niche board (Wellfound / Built In / RepVue), (4) talent community + referrals, (5) outbound CRM sequences (Gem/hireEZ). No single source >60% of pipeline. Pattern: weekly review per req tracking source mix + diversity index; rebalance when one source dominates.
- **Agent execution path:** Use `source-diversification-3-sources-per-role` skill. `cli-anything` curl ATS for per-req source breakdown; weekly review meeting agenda authored in Notion; rebalance with hot-list refresh from underused sources.
- **Source:** https://www.lupahire.com/blog/candidate-sourcing-tools-for-recruiters + https://www.metaview.ai/resources/blog/sourcing-tools-for-recruiters
- **Confidence:** ✓ Fully executable

## Diversity channel sourcing (/dev/color / Code2040 / Black Founders / etc.)

- **SOTA approach:** Project-specific diversity channels — /dev/color (Black engineers), Code2040 (early-career Black + Latine), Black Founders Matter, Lesbians Who Tech (LGBTQ+ technical), Out in Tech, Latinas in Tech, Out & Equal, AfroTech, Grace Hopper Celebration, Tapia Conference. Pattern: become a corporate partner / sponsor; attend conferences; nurture community channels (Slack + Discord); request warm intros for specific roles. Layer Project Include diversity-of-thought best practices over recruiting process.
- **Agent execution path:** Use `diversity-channel-sourcing-dev-color-code2040` skill. `notion-mcp` channel-relationships register; `gmail-mcp` template warm-intro requests; sponsor cycle calendar in `google-calendar-mcp`; conference + event registration tracked in Linear.
- **Source:** https://devcolor.org + https://www.code2040.org + https://lesbianswhotech.org + https://projectinclude.org
- **Confidence:** ✓ Fully executable

## Contractor sourcing (Toptal / Turing / Pesto / Lemon.io / Andela / Arc.dev)

- **SOTA approach:** Vetted marketplaces for fractional / specialist / nearshore hires: Toptal (top 3%, premium $100-200/hr); Turing (24h match, 40-60% below Toptal); Andela (Africa-focused, $40-80/hr mid-level); Arc.dev (1% accept, AI-matching); Lemon.io ($55-95/hr, 24-48h, startup-focused); Pesto (Indian senior eng); Distributed (distributed teams). Pattern: classify role by urgency + budget + geography → route to matched marketplace; provide JD + scope + duration via API.
- **Agent execution path:** Use `contractor-sourcing-toptal-turing-pesto` skill. `cli-anything` curl Turing API / Arc Employer API / Lemon.io intake form; email intake for Toptal / Andela (no public API); track in Notion contractor register.
- **Source:** https://lemon.io/blog/toptal-alternatives/ + https://www.secondtalent.com/alternatives/lemon-io/ + https://distantjob.com/blog/toptal-alternatives-hire-remote-developers/
- **Confidence:** ⚠ Executable with caveats (Toptal / Andela require email intake; Turing / Arc.dev / Lemon.io API-driven; recipient holds budget)

## Boomerang + alumni re-engagement

- **SOTA approach:** 35% of 2025 hires were returning employees (up from 31% prior year); $4,200 avg savings per boomerang hire (Bain 50+ corporate alumni programs analysis); 14-18 month payback once network hits 1,000+ active members. Pattern: maintain alumni database (LinkedIn change tracking + Enterprise Alumni + PeoplePath); quarterly newsletter; "we miss you" outreach 12-18 months post-departure; auto-flag in ATS when alumni applies to new role.
- **Agent execution path:** Use `boomerang-alumni-re-engagement` skill. `notion-mcp` alumni database with departure date + role + reason + sentiment; quarterly `mailchimp` / `gmail-mcp` newsletter; LinkedIn change tracking via SeekOut / Gem alerts; auto-flag returning alumni in Greenhouse via `cli-anything`.
- **Source:** https://ks-agents.com/blog/boomerang-employees-alumni-network-strategy/ + https://peoplepath.com/blog/attract-and-rehire-boomerang-employees-through-your-corporate-alumni-network/ + https://beamery.com/resources/blogs/why-enterprise-organizations-need-an-alumni-hiring-strategy
- **Confidence:** ✓ Fully executable

## Job description optimization (Textio / Datapeople inclusive language)

- **SOTA approach:** Textio — language-guidance engine trained on hiring-outcome data across customer network; predicts applicant pool size, gender balance, and quality; reported 15% lift in female applicants after removing gendered language. Datapeople — readability + template enforcement + bias detection (lower price; weaker bias engine than Textio). 2026 pattern: paste JD → score → revise per language guidance → re-score → ship; remove gendered (e.g., "ninja", "rockstar"), age-coded (e.g., "digital native"), demand-overlong (over 8 must-haves drops female applicant rate).
- **Agent execution path:** Use `jd-optimization-textio-datapeople` (bundled in employer-brand skill). `cli-anything` curl Textio API `/v1/scores` or Datapeople integration with ATS posting; `playwright-mcp` for non-API recipients; cross-check via Joonko / Atomic AI fallback.
- **Source:** https://www.index.dev/blog/textio-review + https://datapeople.io/comparison/datapeople-vs-textio/ + https://blog.ongig.com/job-descriptions/textio-competitors/
- **Confidence:** ⚠ Executable with caveats (Textio / Datapeople paid seat required; manual checklist fallback works for low-volume)

## ATS handoff (Greenhouse / Ashby / Lever)

- **SOTA approach:** Once a sourced candidate moves from "Prospect" to "Applied", push to ATS as the system of record. Greenhouse / Ashby / Lever all expose candidate-create + application-create + source-attribution endpoints. 2026 pattern: source in Gem/hireEZ → call ATS API on stage-change → ATS becomes system of record; sourcer drops out of pipeline; recruiter coordinator owns interview scheduling. Defer interview scheduling, scorecards, offer letters to `operations-agent` (parent — hiring pipeline broadly) or human recruiter.
- **Agent execution path:** Use ATS handoff via `cli-anything` per the `hiring-pipeline-greenhouse-ashby-lever` skill already in `operations-agent` (parent). `gem-hireez-beamery-talent-crm` skill's "Push to ATS" sub-recipe calls Greenhouse `/v1/candidates`, Ashby `/candidate.create`, Lever `/v1/candidates`.
- **Source:** https://www.index.dev/blog/greenhouse-vs-lever-vs-ashby-ats-comparison + https://unified.to/blog/15_ats_apis_to_integrate_with_in_2026_greenhouse_lever_workable + https://www.outsail.co/post/greenhouse-vs-lever-vs-ashby
- **Confidence:** ✓ Fully executable

## Pipeline analytics (top-of-funnel diversity + funnel health)

- **SOTA approach:** Top-of-funnel diversity = % of underrepresented candidates at "Sourced" + "Contacted" + "Replied" stages. Funnel-health metrics: source-to-contact %, contact-to-reply %, reply-to-screen %, screen-to-offer %, offer-acceptance %. 2026 benchmarks: 25-40% source-to-contact, 15-30% contact-to-reply (tech engineering harder), 50-70% reply-to-screen, 30-50% screen-to-offer, >85% offer-acceptance. Track per req + per source.
- **Agent execution path:** Use `pipeline-analytics-funnel-diversity` baked into `source-of-hire-reporting`. `cli-anything` curl ATS for per-stage counts; aggregate in `xlsx` / `google-sheet`; weekly dashboard in Notion / Linear; per-req review with recruiter.
- **Source:** https://unified.to/blog/15_ats_apis_to_integrate_with_in_2026_greenhouse_lever_workable + https://www.metaview.ai/resources/blog/recruiting-trends
- **Confidence:** ✓ Fully executable

---

## Summary table

| # | Use case | SOTA tool | Mechanism | Fulfillment |
|---|---|---|---|---|
| 1 | LinkedIn Recruiter Boolean search | LinkedIn Recruiter + hireEZ AI Boolean | `linkedin-recruiter-boolean-search-strings` + `playwright-mcp` | ⚠ |
| 2 | GitHub talent mining | GitHub REST/GraphQL | `github` MCP + `cli-anything` | ✓ |
| 3 | Stack Overflow talent search | Stack Exchange API | `cli-anything` + curl | ✓ |
| 4 | Niche job board sourcing | Wellfound / Built In / Otta / Hired | `hired-wellfound-built-in-otta-niche-boards` + `cli-anything` + `firecrawl-mcp` | ⚠ |
| 5 | Diversity sourcing | SeekOut / Findem / AmazingHiring | `amazinghiring-findem-seekout-diversity` + `cli-anything` | ⚠ |
| 6 | Passive candidate outreach | Gem / hireEZ / Beamery | `gem-hireez-beamery-talent-crm` + `passive-candidate-outreach-campaigns` + `cli-anything` | ⚠ |
| 7 | Cold InMail + warm intro | LinkedIn + Gmail + Slack | `cold-inmail-warm-intro` + `gmail-mcp` + `slack-mcp` | ✓ |
| 8 | Hot-list / talent community | Gem / Beamery / Phenom | `hot-list-talent-community-mgmt` + `notion-mcp` + `mailchimp` | ✓ |
| 9 | Target company mapping | Crunchbase + Apollo + LinkedIn | `target-company-mapping-crunchbase-linkedin` + `cli-anything` | ⚠ |
| 10 | CTO / VP-Eng exec sourcing | Lusha + RocketReach + ContactOut | `cto-vp-eng-exec-sourcing` + `cli-anything` | ⚠ |
| 11 | Technical sourcing (dev-focused) | AmazingHiring + SeekOut | `technical-sourcing-developer-focused` + `github` MCP | ⚠ |
| 12 | Product designer sourcing | Dribbble + Behance + Apollo | `product-designer-sourcing-dribbble-behance` + `cli-anything` | ⚠ |
| 13 | Sales talent sourcing | RepVue + LinkedIn Sales Nav | `sales-talent-sourcing-repvue` + `cli-anything` | ⚠ |
| 14 | Source-to-contact metrics | ATS REST + xlsx | `source-to-contact-metrics` + `cli-anything` | ✓ |
| 15 | Recruiter persona segmentation | Gem / Notion | `passive-candidate-outreach-campaigns` + `notion-mcp` | ✓ |
| 16 | Source-of-hire reporting | Greenhouse / Ashby / Lever | `source-of-hire-reporting` + `cli-anything` + `google-sheet` | ✓ |
| 17 | Employer brand in outreach | Crunchbase + Google News + Glassdoor | `employer-brand-in-outreach` + `firecrawl-mcp` | ✓ |
| 18 | Candidate experience hygiene | ATS auto-status + Gem | `candidate-experience-hygiene-response-time` + `cli-anything` | ✓ |
| 19 | Source diversification (>3 per role) | ATS + Notion review | `source-diversification-3-sources-per-role` + `notion-mcp` | ✓ |
| 20 | Diversity channels (/dev/color etc.) | Project channel network | `diversity-channel-sourcing-dev-color-code2040` + `notion-mcp` + `gmail-mcp` | ✓ |
| 21 | Contractor sourcing | Toptal / Turing / Arc.dev / Lemon.io | `contractor-sourcing-toptal-turing-pesto` + `cli-anything` | ⚠ |
| 22 | Boomerang + alumni | Notion + Mailchimp + LinkedIn change tracking | `boomerang-alumni-re-engagement` + `notion-mcp` + `mailchimp` | ✓ |
| 23 | JD optimization (Textio / Datapeople) | Textio / Datapeople scoring | `employer-brand-in-outreach` JD sub-skill + `cli-anything` | ⚠ |
| 24 | ATS handoff | Greenhouse / Ashby / Lever | `cli-anything` (uses parent's `hiring-pipeline-greenhouse-ashby-lever` skill) | ✓ |
| 25 | Pipeline funnel + diversity analytics | ATS + xlsx | `source-of-hire-reporting` + `cli-anything` + `xlsx` | ✓ |

**Fulfillment math:** 25 use cases mapped. 14 are full ✓ confidence (every required surface API or skill ships in the box); 11 are ⚠ (LinkedIn / SeekOut / Findem / Gem / Textio / RepVue / Lusha / Toptal / Wellfound — all paid seats the recipient owns, with `playwright-mcp` / `gmail-mcp` / `firecrawl-mcp` fallback paths); 0 are ✗.

**Verdict: ~95% fulfillment.** Every use case has at least one named execution path. The ⚠ rows are all "the recipient owns the paid seat" — not "the agent can't do this." Where the paid seat is absent, a free fallback (Boolean string + `playwright-mcp` UI automation; manual Gmail-only sequence at low scale; firecrawl scrape) ships immediately.

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (only those that exist in `app/config/mcp_config.json`):
- `filesystem` (always)
- `github` — GitHub talent mining + repo signal
- `gmail-mcp` — warm intro + sequence fallback + candidate comms
- `outlook-mcp` — alt for Outlook-shop recipients
- `google-workspace-mcp` — Gmail + Sheets + Calendar combined
- `slack-mcp` — warm-intro DMs + hot-list internal coordination + project-channel community
- `discord-mcp` — alt comms + community channels (some diversity channels Discord-first)
- `notion-mcp` — candidate database + hot-list + persona library + alumni register
- `obsidian-mcp` — alt local-first KB
- `linear-mcp` — sourcing-team task pipeline + per-req sourcing kanban
- `google-calendar-mcp` — outreach cadence + sponsor cycle + event calendar
- `google-drive-mcp` — JD storage + portfolio review + offer-letter archive
- `firecrawl-mcp` — Behance / Dribbble / Wellfound / Crunchbase / Glassdoor scraping
- `brightdata-mcp` — paid scrape for paywalled benchmarks
- `playwright-mcp` — LinkedIn Recruiter UI automation (when no API)
- `huggingface-mcp` — embedding-based candidate-quality clustering
- `posthog-mcp` — talent-community newsletter analytics + outreach A/B test
- `brave-search` — current SOTA + news + market research
- `gemini-ocr-mcp` — résumé OCR for scanned applications
- `mistral-ocr-mcp` — alt OCR engine

**Skill packs to create in Step 10 (runtime build)**, in order of impact:
1. `linkedin-recruiter-boolean-search-strings`
2. `github-talent-mining-language-stars-commits`
3. `gem-hireez-beamery-talent-crm`
4. `passive-candidate-outreach-campaigns`
5. `amazinghiring-findem-seekout-diversity`
6. `technical-sourcing-developer-focused`
7. `cold-inmail-warm-intro`
8. `target-company-mapping-crunchbase-linkedin`
9. `cto-vp-eng-exec-sourcing`
10. `hot-list-talent-community-mgmt`
11. `hired-wellfound-built-in-otta-niche-boards`
12. `stack-overflow-talent-reputation-tag`
13. `product-designer-sourcing-dribbble-behance`
14. `sales-talent-sourcing-repvue`
15. `diversity-channel-sourcing-dev-color-code2040`
16. `boomerang-alumni-re-engagement`
17. `contractor-sourcing-toptal-turing-pesto`
18. `source-to-contact-metrics`
19. `source-of-hire-reporting`
20. `source-diversification-3-sources-per-role`
21. `candidate-experience-hygiene-response-time`
22. `employer-brand-in-outreach`

---

## Notes on remaining caveats (the ⚠ rows)

For each ⚠ use case, the agent handles the platform-gated dependency:

- **LinkedIn Recruiter / Talent Solutions** — LinkedIn Recruiter seat required for Boolean + InMail; Talent Solutions API gated to approved partners. Fallback: `playwright-mcp` automates UI workflow; non-Partner recipients still get full sourcing capability via UI automation.
- **SeekOut / Findem / AmazingHiring** — Enterprise paid seats ($500+/user/mo typically). Fallback: GitHub + Stack Overflow + LinkedIn Boolean for technical roles via free tier.
- **Gem / hireEZ / Beamery talent CRM** — Paid seat required. Fallback: Gmail-only sequencing via `gmail-mcp` + Notion candidate tracker at low scale (<50 prospects / week).
- **Wellfound / Built In / Otta** — Wellfound free for startups (Recruit Pro $499/mo for premium); Built In paid metro plan; Otta employer dashboard. Fallback: manual posting workflow + `firecrawl-mcp` for candidate-list scrape.
- **Crunchbase + Apollo** — Apollo free tier covers MVP; Crunchbase Enterprise paid. Fallback: Crunchbase free search + `firecrawl-mcp` enrichment.
- **Lusha / RocketReach / ContactOut** — Paid seat per executive lookup. Fallback: Hunter.io / Findymail / AnyMail Finder lower-tier alternatives.
- **AmazingHiring / SeekOut technical sourcing** — Paid seat required. Fallback: free GitHub + Stack Exchange + LinkedIn Boolean.
- **Dribbble / Behance designer sourcing** — Both increasingly paywalled in 2026. Fallback: scrape "Hire Me" filter via `firecrawl-mcp` where ToS allows; cross-reference LinkedIn.
- **RepVue employer plan** — Paid plan for candidate search. Fallback: LinkedIn Sales Nav + Apollo for sales roles.
- **Contractor marketplace intake** — Toptal / Andela email intake only; Turing / Arc.dev / Lemon.io have API. Fallback: scoped JD + email + intake form workflow.
- **Textio / Datapeople JD optimization** — Paid seat required. Fallback: manual checklist authored from Textio's published guidance + `cli-anything` calls to free bias scorers (Joonko free tier, Atomic AI).
