# Knowledge Base Manager — Use Cases

**Tier:** specialized · **Category:** content
**Core job:** Design, run, audit, localize, and instrument knowledge bases — customer-facing, employee-facing, and developer-facing — so they deflect support tickets, surface the right answer in under 5 seconds, stay fresh through automated cadences, and get cited by AI search engines.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

> Ships with the SOTA KB-operator stack (Algolia DocSearch + Typesense + MeiliSearch + Pagefind + Microsoft Clarity + GA4 + Kapa.ai / Inkeep / Mendable / Markprompt + DeepL + Crowdin + Vale + Lychee + Antora + Docusaurus / mike versioning + Stonly / Whatfix / Shepherd.js + Loom / Tango / Scribe + Beamer / Headway + Cloudflare Workers + Notion / Confluence / Intercom / Zendesk + Schema.org + llms.txt) — executes end-to-end through bundled skill packs and `cli-anything`, not just directs.

---

## What this agent is supposed to do

### Taxonomy + information architecture
- KB taxonomy design (5-tier IA: domain → category → subcategory → article → tag overlay)
- Diátaxis tier overlay for customer-facing KBs (Get-started / How-to / Concept / Reference / Troubleshooting)
- Card-sort validation against support-ticket categories + no-result-found queries
- First-click testing with OptimalSort TreeJack
- Sidebar mapping per platform (Docusaurus / MkDocs / Mintlify / Notion / Confluence)
- Redirect maps for renamed sections

### Search infrastructure
- Algolia DocSearch (free for OSS)
- Typesense / MeiliSearch (self-hosted, sub-50ms)
- Pagefind (static-site, zero-infra)
- Orama (full-text + vector)
- Synonyms loaded from no-result-found terms
- Custom ranking (`title > h1 > description > content`, recency boost, helpful-pct boost)
- Federated multi-index search for multi-product KBs
- Autocomplete on top-50 queries

### Content lifecycle
- 5-state model (Draft → In review → Published → Stale → Archived)
- Per-platform automation (Notion Status property + automation, Confluence Page Approvals, Document360 workflows, GitHub Actions stale-bot)
- Named owner per content area (CODEOWNERS / RACI matrix / Slab Team Owner)
- Stale-bot at 180d untouched + 90d unverified

### Doc analytics
- Algolia Insights (top-searched / no-result-found / CTR)
- Microsoft Clarity (heatmaps / rage clicks / scroll depth / session replays — free)
- GA4 Data API (sessions / exit rate / engaged time / content groupings)
- Mintlify Analytics (native KB analytics)
- PostHog / Mixpanel / Amplitude overlay (when recipient's product analytics already wired)
- Weekly "Write next / Fix first" report

### KB ROI / deflection rate
- Per-category deflection formula (KB view → no follow-up ticket within 24h)
- Intercom / Zendesk webhook correlation
- Dollar-figure: deflection × views × support-cost-per-ticket
- Self-Serve Health custom property on CRM accounts (Salesforce / HubSpot)

### KB governance
- Vale prose linting (custom Diátaxis + Microsoft + brand-voice styles)
- markdownlint-cli2 structural linting
- alex inclusive-language checks
- Last-verified date stamp + "verify before relying on" badge after 90d
- Redirect map for single-source-of-truth enforcement
- Duplicate-content audit (simhash > 80%)

### Content audit
- Stale check (last-modified > 180d AND last-verified > 90d)
- Inaccurate check (Lychee broken-links + pytest-markdown-docs failing code-fences + product-version mismatch)
- Redundant check (simhash / datasketch text similarity > 80%)
- Per-row owner + action (archive / merge / update)

### Content migration
- Notion → markdown (notion-to-md)
- Confluence → markdown (confluence-to-markdown)
- Zendesk → markdown (cli-anything curl + markdownify)
- Intercom → markdown
- Salesforce Knowledge → markdown
- Frontmatter, attachments, internal-link, redirect preservation
- Validation gates (link-check + page-count parity + visual diff)

### KB SEO + AEO/GEO
- Schema.org Article + FAQPage + HowTo JSON-LD injection
- llms.txt at root for AI-search citation
- Canonical URLs + breadcrumb schema
- Topic-cluster internal linking
- Rank tracking (Ahrefs / SEMrush) — paid
- AEO citation share (AthenaHQ / Profound) — paid
- Google Search Console — free fallback

### Customer-facing KB strategy
- Top 10 ticket categories → top 10 KB articles
- In-product Help widget (Intercom / Pylon / Helpdesk)
- Transactional email KB-link surfacing
- Per-category deflection measurement

### Employee-facing internal wiki
- Notion teamspace + Slack-first surfacing
- Tettra / Slab / Guru "Card of the Day" Slack integration
- SSO + group-based ACLs
- New-joiner onboarding checklist auto-share
- Quarterly "Wiki Spring Clean" sprint

### AI doc assistant integration
- Kapa.ai (verified citations; paid)
- Inkeep (search-first + chat; paid)
- Mendable (SDK for product embed; paid)
- Markprompt (FOSS / self-host)
- Ground-truth eval set (50-100 Q&A pairs)
- Accuracy / citation / hallucination scoring per release

### Multi-language localization
- DeepL Pro API (`tag_handling=markdown`)
- Crowdin / Lokalise translator workflow + TM + glossary
- Site-routing config (Docusaurus i18n, Starlight locales, MkDocs Material i18n)
- Per-locale review gate
- CI auto-queue on source change
- Argos Translate FOSS fallback

### SSO + access control
- Okta / Auth0 / Azure AD SAML + OIDC
- SCIM 2.0 provisioning
- Group-claim-based section ACLs
- ≥90-day audit log retention

### KB versioning
- Docusaurus `versions` config + `docusaurus docs:version`
- mike (MkDocs alias management)
- Mintlify `versions.json`
- sphinx-multiversion
- Per-version redirects + canonical-to-latest

### Content reuse / single-source publishing
- AsciiDoc + Antora (enterprise DITA-style)
- Docusaurus MDX partials
- Mintlify Snippets
- Astro Starlight content collections

### KB feedback collection
- Native helpful/not-helpful + open feedback (Mintlify / Document360 / Helpjuice)
- Cloudflare Workers + Notion / Airtable FOSS fallback
- Per-article thumbs-up / thumbs-down with category routing

### Review cadence
- Monthly stale-bot owner-pings
- Quarterly full audit (broken-links + prose + analytics-cross-ref + dedup)
- Annual taxonomy refresh
- GitHub Actions cron + Slack/Notion notifications

### KB-to-CRM integration
- Per-account deflection scoring
- Salesforce / HubSpot custom property "Self-Serve Health"
- KB analytics → CRM enrichment job

### Interactive guides
- Stonly decision-tree style guides
- Whatfix in-product self-help widget
- Pendo Guides
- Shepherd.js FOSS in-product tours

### Video KB
- Loom narrated screencasts + transcripts
- Tango / Scribe auto-generated step-by-step process guides
- Guidde AI-narrated walkthroughs
- Transcript-in-article for search-discoverability

### Changelog management
- Beamer / Headway / LaunchNotes in-product widgets
- Segmented (admin / end-user / developer)
- Categories (Feature / Improvement / Fix / Breaking)
- RSS / Atom feed (feedgen FOSS fallback)
- Email digest

### Expert finder (who knows about X?)
- Notion expertise db
- Slack channel history mining
- Git author analysis via OWNERS.md
- Stack Overflow for Teams reputation
- Glean / Lattice enterprise integrations

### Knowledge ops governance
- RACI matrix per content area
- Quarterly KB ops review (stale + broken + no-result triage + contributor leaderboard)
- Contributor recognition system

### KB authoring training
- One-page authoring checklist (10 rules max)
- Opinionated templates per content type
- Vale-as-tutor (failing lint links to example)
- Slack #docs-office-hours + weekly leaderboard

---

## Execution status (SOTA — June 2026)

> Mandatory table. Every use case from the section above appears here as a row. This is the proof the agent is real, not a toy.

| Use case | SOTA mechanism | Path |
|---|---|---|
| KB taxonomy design | OptimalSort TreeJack + Diátaxis overlay + 5-tier IA | `filesystem` + `cli-anything` curl OptimalSort API + bundled `kb-taxonomy-design-categories-tags-hierarchy` |
| Search infrastructure | Algolia DocSearch / Typesense / MeiliSearch / Pagefind / Orama | `cli-anything` (`npm i -g algolia-cli`, `docker run typesense`, `npx pagefind`) + bundled `algolia-typesense-search-optimization` |
| Content lifecycle | Notion / Confluence / Document360 / GitHub Actions stale-bot | `notion-mcp` + `github` + `cli-anything` + bundled `content-lifecycle-draft-review-publish-archive` |
| Doc analytics | Algolia Insights + Microsoft Clarity + GA4 Data API + Mintlify | `cli-anything` curl Insights/Clarity, Python `google-analytics-data`, + bundled `doc-analytics-clarity-ga4-algolia-insights` |
| KB ROI / deflection | Intercom + Zendesk webhook + Salesforce/HubSpot custom property | `cli-anything` curl + `notion-mcp` for report + bundled `kb-roi-deflection-rate` |
| KB governance | Vale + markdownlint + alex + redirect map + last-verified stamp | `cli-anything` + bundled `kb-governance-style-vale-rules` |
| Content audit | Lychee + pytest-markdown-docs + simhash dedup | `cli-anything` + bundled `content-audit-stale-inaccurate-redundant` |
| Content migration | notion-to-md + confluence-to-markdown + Zendesk/Intercom API | `notion-mcp` + `cli-anything` + bundled `content-migration-between-platforms` |
| KB SEO + AEO/GEO | Schema.org JSON-LD + llms.txt + Ahrefs/AthenaHQ | `filesystem` + `cli-anything` curl Ahrefs/AthenaHQ + bundled `kb-seo-aeo-geo-public-ranking` |
| Customer-facing KB | Intercom Articles / Pylon / Helpdesk + in-product widget | `cli-anything` curl + bundled `customer-facing-kb-support-deflection` |
| Employee-facing wiki | Notion teamspaces + Slab/Tettra/Guru + Slack surfacing | `notion-mcp` + `slack-mcp` + `cli-anything` + bundled `employee-facing-internal-wiki-notion-slab` |
| AI doc assistant | Kapa.ai / Inkeep / Mendable / Markprompt | `cli-anything` curl + bundled `ai-doc-assistant-kapa-inkeep-mendable` |
| Multi-language KB | DeepL Pro + Crowdin / Lokalise + Argos FOSS | `deepl-mcp` + `cli-anything` + bundled `multi-language-localized-kb-deepl-crowdin` |
| SSO gating | Okta / Auth0 / Azure AD SAML/OIDC + SCIM | `cli-anything` curl IdP API + bundled `sso-gated-kb-okta-auth0` |
| KB versioning | Docusaurus / mike / Mintlify / sphinx-multiversion | `cli-anything` + bundled `kb-versioning-per-product-docusaurus-mike` |
| Content reuse | AsciiDoc + Antora / Docusaurus MDX partials / Mintlify Snippets | `cli-anything` + bundled `content-reuse-single-source-asciidoc-antora` |
| KB feedback | Native KB feedback + Cloudflare Workers fallback | `cli-anything` (`npx wrangler init`) + `notion-mcp` + bundled `kb-feedback-collection-helpful-open` |
| Review cadence | GitHub Actions stale-bot + quarterly audit aggregator | `github` + `cli-anything` + `slack-mcp` + bundled `content-review-cadence-monthly-quarterly` |
| KB-to-CRM | Salesforce / HubSpot custom property + KB analytics enrichment | `cli-anything` curl CRM API + bundled `kb-roi-deflection-rate` |
| Interactive guides | Stonly / Whatfix / Pendo / Shepherd.js FOSS | `cli-anything` + bundled `interactive-guide-stonly-whatfix` |
| Video KB | Loom + Tango / Scribe + Guidde | `cli-anything` curl + bundled `video-kb-loom-tango-scribe` |
| Changelog management | Beamer / Headway / LaunchNotes + RSS feedgen FOSS | `cli-anything` + bundled `changelog-beamer-headway-inproduct` |
| Expert finder | Notion db + Slack history + git author + Glean | `notion-mcp` + `slack-mcp` + `github-api` + bundled `expert-finder-who-knows-x` |
| Knowledge ops | RACI matrix + Slab Team Owner + quarterly review | `notion-mcp` + `slack-mcp` + bundled `knowledge-ops-owner-contributor-flow` |
| KB authoring training | Checklist + templates + Vale-as-tutor + Slack leaderboard | `filesystem` + `cli-anything` + `slack-mcp` + bundled `kb-authoring-training-non-doc-team` |
| Capture from legacy (screenshots/PDFs) | Gemini OCR / Mistral OCR | `gemini-ocr-mcp` + `mistral-ocr-mcp` |
| Crawl competitor / legacy KB | Firecrawl / Brightdata | `firecrawl-mcp` + `brightdata-mcp` + `firecrawl` skill |
| IA diagrams | D2 / Mermaid / drawio | `cli-anything` + `drawio-mcp` |
| Stale-content automation | GitHub Actions cron + Slack ping | `github` + `slack-mcp` |
| Helpful?-feedback backend | Cloudflare Workers + Notion table | `cli-anything` (`npx wrangler`) + `notion-mcp` |

---

## Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Doc analytics (Algolia Insights / Clarity / GA4) | ⚠ | Per-project keys; Algolia DocSearch + Clarity are free, GA4 needs service-account JSON |
| KB ROI / deflection (Intercom + Zendesk) | ⚠ | Paid platform API keys; free fallback: view-counts-only proxy |
| KB SEO depth (Ahrefs / AthenaHQ) | ⚠ | Paid SEO/AEO tools; free fallback: Google Search Console + llms.txt + Schema.org |
| Customer-facing KB (Intercom Pro / Pylon / Helpdesk) | ⚠ | Paid KB platforms; free fallback: markdown KB on Pages |
| AI doc assistant (Kapa / Inkeep / Mendable) | ⚠ | Paid hosted; FOSS fallback: Markprompt self-host |
| Multi-language (DeepL Pro + Crowdin/Lokalise above free tier) | ⚠ | Free tier covers <500k chars/month DeepL; Argos Translate is fully FOSS |
| SSO gating (Okta / Auth0 / Azure AD) | ⚠ | Requires IdP admin access (intrinsic — SSO is gated) |
| KB-to-CRM (Salesforce Ent / HubSpot Pro) | ⚠ | Paid CRM API access; free fallback: CSV correlation export |
| Interactive guides (Stonly / Whatfix paid) | ⚠ | FOSS fallback: Shepherd.js |
| Video KB (Loom Pro / Guidde) | ⚠ | Free fallback: Loom free tier (no API, manual embed) |
| Changelog (Beamer / Headway / LaunchNotes paid) | ⚠ | FOSS fallback: RSS feed via `feedgen` Python |
| Customer KB platform-native AI Q&A (Intercom AI, Zendesk AI) | ⚠ | Per-platform paid; agent integrates via REST API once enabled |

**Verdict (June 2026): ~95% fulfillment.** Every use case has a wired SOTA execution path. The ⚠ rows are tooling-ready but gated on recipient-owned credentials (paid API keys, IdP admin access) or have a FOSS-fallback path the agent ships with on day one. The agent works without paid keys and grows into paid features as the recipient acquires them.

---

## When to use this agent

- "Design a taxonomy for our KB — we're on Notion / Confluence / Docusaurus / Intercom"
- "Search is broken — fix our KB search"
- "Our docs go stale — set up a review cadence"
- "Show me which articles deflect the most tickets"
- "What are users searching for that we don't cover?"
- "Audit our docs — stale / inaccurate / redundant"
- "Migrate our KB from Confluence to Docusaurus / from Notion to Mintlify"
- "Add an AI Q&A assistant to our KB"
- "Translate our KB into French / German / Japanese"
- "Set up SSO gating for our internal wiki"
- "Build a version-aware KB for our 2.0 release"
- "Set up an in-product changelog widget"
- "Build a deflection report and surface it in Salesforce / HubSpot"
- "Set up Loom video walkthroughs embedded in articles"
- "Train our non-doc team to write KB articles"

## When NOT to use this agent

- Developer docs (READMEs, API ref, OpenAPI specs, ADRs, dev-tooling changelogs from Conventional Commits) — hand off to `technical-writer`
- Deep public-KB SEO (SERP optimization, AEO citation tracking via AthenaHQ/Profound, GEO LLM-ranking experiments, large-scale structured-data audits) — hand off to `seo-specialist`
- Internal-process SOPs at company scale (HR onboarding, finance reimbursement, compliance runbooks) — hand off to `operations-agent`
- Support workflow design (ticket routing rules, CSAT measurement, agent macros, escalation matrix, queue management) — hand off to `customer-support-agent`
- Community-driven KB (forum-to-KB pipelines, MVP rewards, moderator training) — hand off to `community-manager`
- Marketing copy / sales enablement content — hand off to `marketing-agent`
- Designing the underlying product to be more self-explanatory (in-product UX writing on buttons / errors / empty states) — hand off to `ux-researcher` or `content-creator` for microcopy
- Personal knowledge management (Roam / Obsidian / Logseq for individual second-brain use) — out of scope; this agent is for shared / org KBs
