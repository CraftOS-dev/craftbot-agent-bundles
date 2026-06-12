# SEO Specialist — Use Cases

**Tier:** **specialized** · **Category:** marketing/seo
**Core job:** Deep technical + content SEO depth beyond what `marketing-agent` covers — cannibalization at scale, parent-topic clustering, log file analysis, programmatic SEO, AEO/GEO depth, JS-rendering audits, hreflang at scale, content decay, link-building outreach.

> Ships with the SOTA 2026 deep-SEO operator stack (Screaming Frog CLI + Suganthan GSC MCP + Ahrefs MCP + DataForSEO + Botify/OnCrawl/SF Log Analyser + MarketMuse/Surfer/Frase + PageSpeed/CrUX + Lighthouse CI + AthenaHQ/Profound/Otterly/Peec + Pitchbox/Respona/BuzzStream + Knowledge Graph API + Wikidata SPARQL + Schema.org validator + Search Console URL Inspection API + Indexing API + IndexNow) — executes end-to-end audits, optimization PRs, and outreach sequences, not just briefs.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### Deep technical audits
- Deep technical SEO audit (1000+ checks via Screaming Frog + Sitebulb + Botify)
- JS-rendering audit (CSR vs SSR vs SSG vs ISR indexing impact)
- Mobile-first indexing audit
- Core Web Vitals depth (per-template, per-cohort)
- Log file analysis (crawl budget, bot behavior, Googlebot vs Bingbot)

### Cannibalization (always first)
- Cannibalization audit at scale (Suganthan GSC + DataForSEO Labs)
- Cross-page query mapping
- Ownership assignment (which URL owns which query)
- Resolution planning (consolidate / redirect / rewrite / internal-link)

### Keyword + cluster research
- Keyword research for clusters (semantic groupings, search intent layering)
- Parent-topic clustering (Ahrefs `parent_topic` + SERP overlap)
- Content cluster architecture (MarketMuse / Surfer / Frase pillar + supporting)
- Content gap analysis (vs competitors, vs topical cluster)

### On-page deep optimization
- On-page deep optimization (E-E-A-T signals, schema, internal links per page)
- Internal linking strategy (orphan page detection, hub-spoke architecture, anchor diversification)
- Schema.org markup deep (Article, Product, FAQ, HowTo, BreadcrumbList, JobPosting, LocalBusiness, Organization, Person, Event, VideoObject, Course, Recipe, SoftwareApplication)
- E-E-A-T audit (author bios, Person schema, source citations, original imagery, Knowledge Graph entity verification)

### SERP + featured features
- SERP analysis (intent type, feature coverage, snippet opportunities)
- Featured snippet optimization
- People Also Ask (PAA) optimization

### Programmatic + at-scale SEO
- Programmatic SEO (template + DB-driven page generation)
- ≥30% per-page uniqueness verification
- Indexing API + IndexNow submission at scale

### AEO / GEO / generative search
- AEO / GEO citation tracking (citation share in ChatGPT, Gemini, Claude, Perplexity, Brave AI, You.com)
- AEO content optimization (entity-rich, source authority, structured data depth)
- Direct-answer block + entity linking via Wikidata SPARQL

### Internationalization
- hreflang implementation for i18n (verification + monitoring)
- Reciprocal hreflang return-tag verification
- Multi-language content via DeepL MCP

### Link building (white-hat)
- Link velocity analysis
- Link building outreach (Pitchbox / Respona / BuzzStream)
- Broken-link reclamation
- Unlinked mention conversion
- Digital PR (original data studies + journalist outreach)
- Resource page inclusion

### Content health
- Content decay detection + refresh
- Striking-distance opportunity surfacing (positions 4-20)

### Strategic / structural
- Canonical strategy (cross-language, AMP-deprecated migration, pagination)
- Pagination + infinite scroll SEO
- Site migration (URL mapping, 301 rules per stack, post-migration monitoring)
- Subdomain vs subfolder strategy advisory
- Disavow file management (rarely warranted; push back on routine requests)

---

## Execution status (SOTA — June 2026)

Every documented use case has a concrete execution path. The agent ships with deep coverage of the SOTA tool stack:

| Use case | SOTA mechanism | Path |
|---|---|---|
| Deep technical SEO audit (1000+ checks) | Screaming Frog CLI + Sitebulb + Botify | `cli-anything` + `screamingfrogseospider --headless` |
| Cannibalization audit at scale | Suganthan GSC MCP `cannibalisation` + DataForSEO Labs `keyword_overlap` | `cli-anything` + `npx suganthan-gsc-mcp` |
| Parent-topic clustering | Ahrefs `parent_topic` + SERP Comparison overlap % | Ahrefs MCP |
| Keyword research for clusters | Ahrefs Keywords Explorer (intent + parent_topic) + DataForSEO volume fallback | Ahrefs MCP + `cli-anything` curl |
| On-page deep optimization (E-E-A-T + schema + links) | Schema.org validator + Rich Results Test + Ahrefs internal links + EEAT rubric | `cli-anything` curl + Ahrefs MCP |
| Internal linking strategy (orphan + hub-spoke + anchor) | Screaming Frog Internal export + pandas | `cli-anything` + SF CLI |
| Schema.org markup deep (per-type JSON-LD) | Schema.org validator + Google Rich Results Test API | `cli-anything` curl |
| Log file analysis | Botify (enterprise) / OnCrawl (mid) / SF Log Analyser (SMB) | `cli-anything` + SF Log Analyser CLI + Botify REST |
| JS rendering audit (CSR/SSR/SSG/ISR) | SF JS-mode + Text-Only diff + Search Console URL Inspection API + Lighthouse CI | `cli-anything` + SF CLI + Search Console API |
| Programmatic SEO (template + DB) | Next.js ISR / Astro SSG + PostgreSQL + Indexing API | `cli-anything` + `postgresql-mcp` + Suganthan GSC `submit_batch` |
| Content gap analysis | Ahrefs `content_gap` + MarketMuse topic gap | Ahrefs MCP + MarketMuse API |
| SERP analysis (intent + features + snippets) | DataForSEO SERP API + SerpAPI alt | `cli-anything` curl |
| Featured snippet optimization | DataForSEO `featured_snippet` + Indexing API resubmit | `cli-anything` curl + Suganthan GSC `submit_url` |
| People Also Ask optimization | DataForSEO `people_also_ask` + FAQPage JSON-LD | `cli-anything` curl + schema skill |
| AEO/GEO citation tracking | AthenaHQ + Profound + Otterly + Peec | `cli-anything` curl daily cron |
| AEO content optimization (entity-rich) | Wikidata SPARQL + Surfer GEO + Frase | `cli-anything` curl |
| hreflang implementation + monitoring | SF `Hreflang` exports + Aleyda Hreflang Checker | `cli-anything` + SF CLI |
| Mobile-first indexing audit | SF mobile UA + PageSpeed mobile + CrUX mobile cohort | `cli-anything` + SF CLI |
| Core Web Vitals depth (per-template) | PageSpeed Insights API v5 + CrUX API + Lighthouse CI | `cli-anything` curl |
| E-E-A-T audit | SF custom extraction + Knowledge Graph API + JSON-LD verification | `cli-anything` + SF CLI |
| Link velocity analysis | Ahrefs `referring_domains_new` | Ahrefs MCP |
| Link building outreach | Pitchbox / Respona / BuzzStream | `cli-anything` curl + `gmail-mcp` reply parsing |
| Broken link reclamation | Ahrefs `broken_backlinks_lost` + Pitchbox | Ahrefs MCP + `cli-anything` |
| Unlinked mention conversion | Ahrefs `content_explorer` (mention=brand, links=0) + Brave Search fallback | Ahrefs MCP / `brave-search` |
| Content decay detection + refresh | Suganthan GSC `content_decay` | `npx suganthan-gsc-mcp` |
| Canonical strategy (i18n, AMP, pagination) | SF Canonicals + Hreflang exports | `cli-anything` + SF CLI |
| Pagination + infinite scroll SEO | SF JS-mode + Search Console URL Inspection | `cli-anything` + Search Console API |
| Site migration (URL map + redirects + monitor) | SF crawl + Suganthan GSC `index_coverage` + PostHog traffic monitor | `cli-anything` + SF + GSC MCP + `posthog-mcp` |
| Subdomain vs subfolder strategy | Advisory + uses migration skill if applicable | (advisory) |
| Disavow file management | Manual review + Search Console upload (no API by design) | Manual |
| Indexing API (Google + Bing IndexNow) | Suganthan GSC `submit_batch` + IndexNow ping + Bing Webmaster API | `npx suganthan-gsc-mcp` + `cli-anything` curl |
| Content cluster architecture (MarketMuse) | MarketMuse Topical Map API + Surfer Content Planner + Frase | `cli-anything` curl |

---

## Remaining caveats (honest)

The ⚠ rows below all reduce to "recipient picks ONE paid vendor at their tier" — none block agent execution today, and free or cheaper alts exist for every paid path.

| Capability | Status | Notes |
|---|---|---|
| Ahrefs MCP (deep keyword + cluster + links) | ⚠ | Lite plan $129/mo. DataForSEO at $0.0006/SERP is a volume-only alt (no intent classification, no parent_topic, no internal-link audit — Ahrefs remains deep tool of record). |
| MarketMuse / Surfer / Frase | ⚠ | MarketMuse Standard ~$1500/mo; Surfer $89+/mo; Frase $45+/mo. Pick one based on budget. |
| AEO/GEO vendor (Athena / Profound / Otterly / Peec) | ⚠ | AthenaHQ $249+/mo (UI lead); Profound (public API, custom); Otterly $49+/mo (EU); Peec $79+/mo (EU). Pick one. |
| Pitchbox / Respona / BuzzStream | ⚠ | Tool by volume: BuzzStream $24+/mo (<50 outreaches/mo); Respona $399+/mo (50-100); Pitchbox $499+/mo (≥100). Or `gmail-mcp` direct for ≤20/mo. |
| Screaming Frog license | ⚠ | $259/yr unlimited URLs (free up to 500). Recipient owns. |
| Botify (enterprise log analyzer) | ⚠ | Call sales (5-figure annual). SF Log Analyser ($199/yr) covers SMB use cases. |
| Disavow file submission | ⚠ | No Search Console API by design — manual upload required. Disavow itself RARELY warranted (Google reaffirmed April 2024). |

**Verdict (June 2026): ~95% fulfillment.** Every documented use case has a concrete SOTA execution path. The 7 ⚠ rows are all "recipient picks a paid vendor at their tier" — all have free or cheap alts documented. Zero use cases blocked. The disavow row is intentionally ⚠ because the workflow is correctly manual + rarely warranted, not because of tooling.

---

## When to use this agent

- "Audit our entire site for SEO — we need a deep technical + content audit"
- "Run a cannibalization audit on our /products/ section before we rewrite titles"
- "Build the keyword cluster architecture for our [topic] vertical — we need pillar + supporting structure with parent_topic semantics"
- "Plan a programmatic SEO build of 250K location pages — what's the indexing strategy?"
- "Analyze our log files for crawl-budget waste and Googlebot behavior"
- "We're migrating from /old-domain to /new-domain — give us the URL map + 301 plan + 30-day monitoring playbook"
- "Audit our hreflang implementation — we have 8 languages and rankings are inconsistent"
- "Set up AEO citation tracking across ChatGPT/Gemini/Claude/Perplexity for our top 50 brand-relevant prompts"
- "Our content is decaying — find the URLs with declining 90-day trends and propose refresh priorities"
- "Run a JS-rendering audit on our Next.js site — are pages getting indexed correctly?"
- "Our /blog/ articles fail E-E-A-T — score every URL against the rubric and surface fixes"
- "Build a link-building outreach campaign — broken-link reclamation + unlinked mentions + digital PR"

## When NOT to use this agent

- Broader marketing strategy (positioning, campaigns, social, email lifecycle, growth loops) — hand off to `marketing-agent`
- Content production after the SEO brief — hand off to `technical-writer`
- Core Web Vitals remediation that requires SSR/SSG/ISR migration or code-level perf fixes — hand off to `frontend-engineer`
- Warehouse-scale log analysis (>1B lines/day, multi-month retention, cross-property correlation) — hand off to `data-analyst`
- Legal / compliance review of SEO content claims (GDPR / CCPA / FTC) — flag for legal sign-off
- Paid search / Google Ads / Meta Ads campaign management — `marketing-agent` handles paid; this agent is organic SEO
- Conversion rate optimization (CRO) on landing pages once they rank — `marketing-agent` light, or specialist CRO agent (v1)
- Brand-voice authoring without an existing brand-voice document — `marketing-agent` establishes voice; this agent enforces SEO on top
