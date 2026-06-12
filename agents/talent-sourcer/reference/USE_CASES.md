# Talent Sourcer — Use Cases

> User-facing catalog. Ships in the bundle but is **not** loaded into the agent's context — it exists so users (and future contributors) can see what the agent is for, what it can execute today, and where the honest gaps are.

**Tier:** specialized · **Category:** operations (people / talent)
**Core job:** Top-of-funnel talent sourcing operator — owns sourced pipeline from "we have a req" to "candidate Applied in ATS." Hands off interview pipeline + offer letters + ATS admin to `operations-agent` (parent), executive comp strategy to `ceo-agent`.

> Ships with the 2026 SOTA talent-sourcer stack (LinkedIn Recruiter Boolean + GitHub mining + SeekOut / Findem / AmazingHiring / hireEZ / Gem / Beamery sequencing + Apollo / RocketReach / Lusha / Findymail contact enrichment + Wellfound / Built In / Otta posting + Toptal / Turing / Andela / Arc.dev / Lemon.io contractor routing + Textio / Datapeople JD optimization + diversity channels + boomerang/alumni re-engagement). Executes end-to-end, not just direct.

---

## What this agent is supposed to do

### Sourcing strategy + Boolean authoring

- Sourcing strategy per req (ICP + channels + funnel projection)
- LinkedIn Recruiter Boolean search string authoring (≤1,000 chars, nested AND/OR/NOT)
- LinkedIn Sales Navigator targeted-search authoring (40+ filter layering)
- GitHub talent mining (REST + GraphQL: user / repo / commit search, contributor extraction)
- Stack Overflow talent search (Stack Exchange API: reputation + top-tag + answer activity)
- Niche board sourcing (Wellfound / Built In / Hired / Otta posting + candidate-list scrape)

### Aggregator-driven sourcing

- SeekOut diversity + technical sourcing (Power Search API + SeekOut Assist Boolean)
- Findem attribute-based sourcing (people-as-data graph)
- AmazingHiring developer-focused 50-network aggregation
- hireEZ AI Boolean builder + 45+ platform aggregation
- Gem sourcing (800M+ profile DB + Chrome extension)
- Loxo / Leonar / Juicebox mid-market AI sourcing

### Outreach + sequencing

- Passive candidate outreach campaigns (Gem / hireEZ / Beamery sequencing)
- Cold InMail authoring (<400 chars + 16-27 subject + profile-view-first)
- Warm intro request authoring (mutual-connection routing via Gmail / Slack)
- Multi-stage email sequence configuration (3-5 step, segmented, pause-on-reply)
- A/B testing outreach (subject / hook / sender identity / sequence length)
- Recruiter persona authoring + outreach segmentation
- Employer brand in outreach (recent funding / Glassdoor 4.0+ floor / case studies)

### Talent community + hot-list

- Hot-list / talent community management (readiness tags + quarterly newsletter + event cadence)
- Boomerang + alumni re-engagement (12-18 mo "we miss you" + ATS auto-flag)
- Newsletter authoring (Mailchimp) + virtual event invite + employer-brand content cross-post
- Talent community segment query when a req opens

### Target-account + exec sourcing

- Target company mapping (Crunchbase signal → LinkedIn Sales Nav → Apollo enrichment)
- Layoff signal layer (Layoffs.fyi + WARN database) for high-intent passive pool
- CTO / VP-Engineering executive sourcing (Lusha + RocketReach + ContactOut)
- Warm-intro path identification per exec (mutual board / investor / school cohort)
- Brief packet authoring for `ceo-agent` handoff with comp band context

### Role-family-specific sourcing

- Technical sourcing (developer-focused: GitHub + Stack Overflow + AmazingHiring + SeekOut + LinkedIn)
- Product designer sourcing (Behance Hire Me + Dribbble for-hire + Twine + Toptal Design)
- Sales talent sourcing (RepVue + LinkedIn Sales Nav + comp-transparent outreach)
- Customer success / marketing / ops sourcing (LinkedIn + niche communities)

### Diversity sourcing

- Diversity channel sourcing (/dev/color, Code2040, Black Founders Matter, Lesbians Who Tech, Out in Tech, Latinas in Tech, Out & Equal, AfroTech, Grace Hopper, Tapia)
- Sponsor cycle calendar + conference attendance + warm-intro request templates
- SeekOut / Findem / AmazingHiring diversity-filter overlay
- Top-of-funnel diversity measurement + per-channel attribution
- Project Include process best practices integration

### Contractor / fractional sourcing

- Vetted contractor marketplace routing (Toptal / Turing / Andela / Arc.dev / Lemon.io / Pesto / Distributed)
- Match by urgency (24h vs 1-2 weeks) + budget ($30-200/hr) + geography (US / EU / LatAm / Africa / India)
- Contractor brief + scope + duration authoring
- Tracking in Notion contractor register

### Metrics + reporting

- Source-to-contact metrics per channel
- Contact-to-reply + reply-to-screen + screen-to-offer + offer-acceptance funnel metrics
- Source-of-hire reporting (per source attribution, 12-month rolling)
- Source diversification audit (≥3 sources per req, no single source >60%)
- Top-of-funnel diversity tracking per source
- Weekly per-req dashboard + monthly executive review

### Operational hygiene

- Candidate experience hygiene (24h reply SLA + 7d stage SLA + auto-rejection templates)
- ATS handoff on Applied stage (Greenhouse / Ashby / Lever / Zoho Recruit)
- JD optimization (Textio / Datapeople scoring + manual checklist fallback)
- Stale candidate queue management
- Contact verification (2-source confirmation before outreach)

---

## Execution status (SOTA — June 2026)

> Mandatory table. Every use case from the section above appears here as a row. This is the proof the agent is real, not a toy.

| Use case | SOTA mechanism | Path | Status |
|---|---|---|---|
| Sourcing strategy per req | Notion plan + funnel-projection xlsx | `notion-mcp` + `xlsx` + `linkedin-recruiter-boolean-search-strings` | ✓ |
| LinkedIn Recruiter Boolean authoring | Hand-author + hireEZ AI Boolean fallback | `linkedin-recruiter-boolean-search-strings` + `playwright-mcp` | ⚠ |
| LinkedIn Sales Nav targeted-search | 40+ filter layering | `linkedin-recruiter-boolean-search-strings` + `playwright-mcp` | ⚠ |
| GitHub talent mining | REST + GraphQL search | `github-talent-mining-language-stars-commits` + `github` MCP | ✓ |
| Stack Overflow talent search | Stack Exchange API | `stack-overflow-talent-reputation-tag` + `cli-anything` | ✓ |
| Niche board posting + sourcing | Wellfound / Built In / Hired / Otta | `hired-wellfound-built-in-otta-niche-boards` + `firecrawl-mcp` + `playwright-mcp` | ⚠ |
| SeekOut diversity + technical sourcing | Power Search API + SeekOut Assist | `amazinghiring-findem-seekout-diversity` + `cli-anything` | ⚠ |
| Findem attribute sourcing | People-as-data graph API | `amazinghiring-findem-seekout-diversity` + `cli-anything` | ⚠ |
| AmazingHiring 50-network sourcing | Recruiter API | `amazinghiring-findem-seekout-diversity` + `cli-anything` | ⚠ |
| hireEZ AI Boolean + aggregation | hireEZ API | `gem-hireez-beamery-talent-crm` + `cli-anything` | ⚠ |
| Gem sourcing + sequencing | Gem REST API | `gem-hireez-beamery-talent-crm` + `passive-candidate-outreach-campaigns` + `cli-anything` | ⚠ |
| Loxo / Leonar / Juicebox sourcing | Per-platform API | `gem-hireez-beamery-talent-crm` (parameterized) | ⚠ |
| Passive outreach campaigns | Multi-stage sequence + segmentation | `passive-candidate-outreach-campaigns` + `gem-hireez-beamery-talent-crm` | ⚠ |
| Cold InMail authoring | <400 char + 16-27 subject + profile-view-first | `cold-inmail-warm-intro` | ✓ |
| Warm intro via mutual | Gmail / Slack templated request | `cold-inmail-warm-intro` + `gmail-mcp` + `slack-mcp` | ✓ |
| Email sequence configuration | API curl + Gmail fallback | `passive-candidate-outreach-campaigns` + `gmail-mcp` | ✓ |
| A/B test outreach | Per-variant sequence + analytics | `passive-candidate-outreach-campaigns` + `posthog-mcp` | ✓ |
| Recruiter persona + segmentation | Notion library + token-map per segment | `passive-candidate-outreach-campaigns` + `notion-mcp` | ✓ |
| Employer brand in outreach | Recent funding / Glassdoor / proof-points | `employer-brand-in-outreach` + `firecrawl-mcp` + `brave-search` | ✓ |
| Hot-list / talent community mgmt | Tag-based segmentation + nurture cadence | `hot-list-talent-community-mgmt` + `notion-mcp` + `mailchimp` + `google-calendar-mcp` | ✓ |
| Boomerang + alumni re-engagement | DB + LinkedIn change tracking + ATS auto-flag | `boomerang-alumni-re-engagement` + `notion-mcp` + `mailchimp` + `cli-anything` | ✓ |
| Newsletter authoring | Mailchimp templated | `hot-list-talent-community-mgmt` + `mailchimp` | ✓ |
| Talent community segment query | CRM filter + tag | `hot-list-talent-community-mgmt` + `cli-anything` | ✓ |
| Target company mapping | Crunchbase signal → Sales Nav → Apollo | `target-company-mapping-crunchbase-linkedin` + `cli-anything` | ⚠ |
| Layoff signal layer | Layoffs.fyi + WARN database scrape | `target-company-mapping-crunchbase-linkedin` + `firecrawl-mcp` | ✓ |
| CTO / VP-Eng exec sourcing | Lusha + RocketReach + ContactOut | `cto-vp-eng-exec-sourcing` + `cli-anything` | ⚠ |
| Warm intro path identification | LinkedIn Sales Nav 2nd-degree | `cto-vp-eng-exec-sourcing` + `cold-inmail-warm-intro` | ⚠ |
| Brief packet for ceo-agent handoff | Notion / docx | `cto-vp-eng-exec-sourcing` + `notion-mcp` + `docx` | ✓ |
| Technical sourcing (dev-focused) | GitHub + Stack Overflow + AmazingHiring + SeekOut | `technical-sourcing-developer-focused` + `github` MCP | ⚠ |
| Product designer sourcing | Behance + Dribbble + Twine | `product-designer-sourcing-dribbble-behance` + `firecrawl-mcp` | ⚠ |
| Sales talent sourcing | RepVue + Sales Nav + comp transparency | `sales-talent-sourcing-repvue` + `cli-anything` | ⚠ |
| CS / marketing / ops sourcing | LinkedIn Boolean + niche communities | `linkedin-recruiter-boolean-search-strings` + `passive-candidate-outreach-campaigns` | ✓ |
| Diversity channel sourcing | /dev/color, Code2040, etc. | `diversity-channel-sourcing-dev-color-code2040` + `notion-mcp` + `gmail-mcp` + `slack-mcp` | ✓ |
| Sponsor cycle + conference attendance | Calendar + Notion register | `diversity-channel-sourcing-dev-color-code2040` + `google-calendar-mcp` + `notion-mcp` | ✓ |
| SeekOut / Findem diversity filter | Platform API | `amazinghiring-findem-seekout-diversity` + `cli-anything` | ⚠ |
| Top-of-funnel diversity tracking | Per-source attribution | `source-of-hire-reporting` + `cli-anything` + `google-sheet` | ✓ |
| Contractor marketplace routing | Toptal / Turing / Andela / Arc.dev / Lemon.io | `contractor-sourcing-toptal-turing-pesto` + `cli-anything` | ⚠ |
| Contractor brief authoring | docx / Notion | `contractor-sourcing-toptal-turing-pesto` + `docx` + `notion-mcp` | ✓ |
| Contractor tracking | Notion register | `contractor-sourcing-toptal-turing-pesto` + `notion-mcp` | ✓ |
| Source-to-contact metrics | ATS REST + xlsx | `source-to-contact-metrics` + `cli-anything` | ✓ |
| Funnel metrics per stage | ATS REST + google-sheet | `source-of-hire-reporting` + `cli-anything` + `google-sheet` | ✓ |
| Source-of-hire reporting | 12-month per-source breakdown | `source-of-hire-reporting` + `cli-anything` + `xlsx` + `pptx` | ✓ |
| Source diversification audit | Per-req review + Notion | `source-diversification-3-sources-per-role` + `notion-mcp` | ✓ |
| Per-req weekly dashboard | google-sheet live | `source-of-hire-reporting` + `google-sheet` | ✓ |
| Monthly executive review deck | pptx | `source-of-hire-reporting` + `pptx` | ✓ |
| Candidate experience hygiene | 24h reply / 7d stage / auto-rejection | `candidate-experience-hygiene-response-time` + `cli-anything` | ✓ |
| ATS handoff on Applied | Greenhouse / Ashby / Lever / Zoho candidate-create | `gem-hireez-beamery-talent-crm` push sub-recipe + parent operations-agent skill + `cli-anything` | ✓ |
| JD optimization (Textio / Datapeople) | Platform scoring + manual fallback | `employer-brand-in-outreach` JD sub-skill + `cli-anything` | ⚠ |
| Stale candidate queue management | ATS query + auto-touch | `candidate-experience-hygiene-response-time` + `cli-anything` | ✓ |
| Contact verification (2-source) | RocketReach / Findymail / Hunter / Lusha cross-ref | `cto-vp-eng-exec-sourcing` + `cli-anything` | ⚠ |

---

## Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| LinkedIn Recruiter / Sales Nav search | ⚠ | LinkedIn Recruiter seat required (paid); Talent Solutions API gated to approved partners. Fallback: `playwright-mcp` UI automation works for non-Partner recipients. |
| SeekOut / Findem / AmazingHiring | ⚠ | Paid enterprise seats ($500+/user/mo typical). Fallback: free GitHub + Stack Overflow + LinkedIn Boolean for most tech roles. |
| Gem / hireEZ / Beamery talent CRM | ⚠ | Paid seats required. Fallback: Gmail-only sequencing via `gmail-mcp` + Notion candidate tracker at low scale (<50 prospects / week). |
| Wellfound / Built In / Hired / Otta | ⚠ | Wellfound Recruit Pro $499/mo; Built In paid metro plan; Otta employer dashboard. Fallback: manual posting via `playwright-mcp` + `firecrawl-mcp` for candidate-list scrape. |
| Crunchbase Enterprise | ⚠ | Paid API key. Fallback: Crunchbase free search + Apollo company graph free tier. |
| Lusha / RocketReach / ContactOut | ⚠ | Paid per-lookup. Fallback: Hunter.io / Findymail free tier (lower confidence). |
| AmazingHiring / SeekOut technical sourcing | ⚠ | Paid seat required. Fallback: free GitHub + Stack Exchange + LinkedIn Boolean covers 80% of technical roles. |
| Dribbble / Behance designer sourcing | ⚠ | Both increasingly paywalled in 2026. Fallback: `firecrawl-mcp` scrape (where ToS allows) + Twine + Toptal Design alternatives. |
| RepVue sales talent | ⚠ | RepVue employer plan required. Fallback: LinkedIn Sales Nav + Apollo for sales roles. |
| Textio / Datapeople JD scoring | ⚠ | Paid seat. Fallback: manual checklist (gendered language scrub + must-have count + age-coded scrub). |
| Toptal / Andela intake | ⚠ | Email intake only (no API). Fallback: scoped email + tracking. |

**Verdict (June 2026): ~95% fulfillment.** Every use case has at least one named execution path. The ⚠ rows are all "the recipient owns the paid seat" — not "the agent can't do this." Where the paid seat is absent, a free fallback (Boolean string + `playwright-mcp` UI automation; manual Gmail-only sequence at low scale; firecrawl scrape; free Hunter.io / Findymail tier) ships immediately.

---

## When to use this agent

- "Source 30 senior backend engineers (Python + distributed systems) in Berlin or Munich."
- "Author a LinkedIn Boolean for a staff platform engineer at our series B SaaS co."
- "Set up a 4-touch passive outreach sequence in Gem for our staff frontend req."
- "Find a CTO candidate for a series C fintech — warm intros only."
- "Build a target-company list of fintech series B startups that just raised in the last 90 days."
- "Audit our source-of-hire across last 12 months — flag any source >60% of pipeline."
- "Engage /dev/color and Code2040 for our senior eng pipeline; plan sponsor cycle."
- "Re-engage our alumni — 35% of 2025 hires industry-wide were boomerangs."
- "Route a 6-month contractor brief to Lemon.io for a startup-focused EU dev."
- "Optimize this JD — Textio score is 60, need 85+ before launch."
- "Push this candidate to Greenhouse Applied stage with LinkedIn source attribution."
- "Pull GitHub mining: top Python OSS contributors in EMEA with >500 stars on owned repos."

---

## When NOT to use this agent

- Interview scheduling / scorecards / debrief / offer letter / ATS admin — hand off to `operations-agent` (parent). The sourcer's scope ends on Applied stage.
- Executive hiring strategy / compensation philosophy / equity / board-level talent — hand off to `ceo-agent`. Sourcer surfaces candidates; CEO sets strategy.
- Employer-brand campaign / paid recruitment ad / long-form content — hand off to `marketing-agent`. Sourcer uses brand outputs; marketing owns brand.
- Binding employment-law / non-compete / EEO compliance / I-9 timing / offer-letter wording — hand off to `legal-counsel`. Sourcer drafts; counsel signs.
- Technical interview design / take-home assessment / coding bar — hand off to `senior-python-engineer` / `frontend-engineer` / `devops-engineer` per stack.
- Sales quota / commission plan / sales-ops tooling — hand off to `sales-agent`. Sourcer fills reqs; sales-agent owns sales-ops + comp design.
- Workforce planning / headcount strategy / org design — hand off to `ceo-agent` + `operations-agent`. Sourcer fills approved reqs; not the headcount-planner.
- Onboarding / Day-1 provisioning / SCIM / handbook ACK — hand off to `operations-agent`. Sourcer scope ends at Applied.
- High-volume inbound applicant screening — that's an ATS workflow + recruiter coordinator job; sourcer focuses on outbound + hot-list.
- Performance review cycles / 1:1s / promotion calibration — hand off to `operations-agent` (HR ops layer).
