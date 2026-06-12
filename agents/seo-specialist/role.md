# SEO Specialist — deep reference

This appends to `AGENT.md`. **Not** in the agent's default context. Grep when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "Deep technical audit playbook", "Cannibalization at scale playbook", "Parent-topic clustering methodology", "Log file analysis methodology", "Programmatic SEO playbook", "JS-rendering audit decision tree", "Schema deep templates", "Hreflang at scale playbook", "AEO/GEO content optimization", "Site migration playbook", "E-E-A-T scoring rubric", "Link building outreach playbook", "Antipattern catalog", "Audit report template", "Cannibalization audit template (deep)", "Migration URL map template", "JSON-LD templates per type", "SOTA tool reference".

For provenance, see `SOURCES.md`.

---

## Capability reference

### Crawlers + audit tools handled
- Screaming Frog SEO Spider (CLI headless mode, JavaScript-render mode, custom extraction, scheduling)
- Sitebulb (CLI mode, hint engine prioritization)
- OnCrawl (REST API)
- Botify Analytics (enterprise REST API)
- JetOctopus
- Lumar (formerly Deepcrawl)
- Audisto
- Ryte
- Screaming Frog Log File Analyser (SMB)
- Botify Log Analyzer (enterprise)
- OnCrawl Log Analyzer (mid-market)
- ELK stack for custom log pipelines
- Splunk for enterprise log pipelines

### SEO research + keyword platforms handled
- Ahrefs (remote MCP at `mcp.ahrefs.com` + Keywords Explorer, Site Explorer, Content Explorer, Broken Backlinks, Referring Domains, Content Gap, parent_topic)
- SEMrush API (alt — Topic Research, Keyword Gap, Domain Overview)
- Moz Pro API (alt — Domain Authority, Page Authority, Spam Score)
- DataForSEO MCP / API ($0.0006/SERP — cheap volume + SERP positions)
- seoClarity (enterprise)
- BrightEdge (enterprise)
- Conductor (formerly ContentKing — change monitoring)
- Sistrix (European market focus)

### GSC + indexing platforms
- Google Search Console (Suganthan GSC MCP v2.2.2 — 20 tools)
- Bing Webmaster Tools API (URL submission, crawl errors)
- Google Indexing API (200/day quota per property, application for higher)
- IndexNow protocol (Bing + Yandex + Naver — free, instant, ping submission)
- Yandex Webmaster
- Naver Search Advisor

### Content / topic intelligence
- MarketMuse Topical Map API (Standard plan minimum — pillar + supporting cluster generation, content briefs)
- Surfer SEO Content Planner + GEO (per-page on-page scoring, content scoring, GEO recent feature)
- Clearscope API (content optimization scoring)
- Frase API (Topic Model, AEO scoring, content briefs)
- NeuronWriter (alt content optimization)
- Page Optimizer Pro (POP — content scoring)

### Schema + structured data
- Schema.org Markup Validator (free, validator.schema.org)
- Google Rich Results Test (free, via Search Console API)
- Schema.dev
- WordLift (semantic SEO + knowledge graph)
- Bonsai schema generator
- JSON-LD per type: Article, NewsArticle, BlogPosting, Product, FAQPage, HowTo, BreadcrumbList, JobPosting, LocalBusiness, Organization, Person, Event, VideoObject, Course, SoftwareApplication, Recipe, Review, AggregateRating

### AEO / GEO / generative search
- AthenaHQ ($249+/mo — UI-leading citation tracking across ChatGPT, Gemini, Claude, Perplexity, Brave AI, You.com)
- Profound (public API — citation tracking + share of voice vs competitors)
- Otterly (EU, $49+/mo — Cologne-based)
- Peec.ai (EU, $79+/mo — European market focus)
- Goodie (AI-search-only brand monitoring)
- Glasp (community-driven citation surface)
- Surfer GEO (recent feature — content scoring for AI surfaces)

### Core Web Vitals + perf
- Google PageSpeed Insights API v5 (CrUX field data + Lighthouse lab data in one call)
- Lighthouse CI (regression gating + CI integration)
- GTmetrix API (waterfall + perf scoring)
- WebPageTest API (real-device + connection profiles)
- Chrome UX Report (CrUX) API (real-user p75 by URL/origin, device + connection cohorts)

### Link building + outreach
- Pitchbox API ($499+/mo — outreach automation at scale)
- Respona API ($399+/mo — link builder in a box)
- BuzzStream API ($24+/mo — SMB relationship management)
- LinkResearchTools (link risk auditing)
- Linkody (link monitoring)

### International / hreflang
- Aleyda Solis Hreflang Tags Tester
- The Hreflang Checker
- Screaming Frog hreflang exports (Missing Return Tag, Inconsistent Language Confirmation Links, Incorrect Language and Region)
- DeepL (multi-language content translation — via `deepl-mcp`)

### Programmatic SEO stacks
- Next.js ISR / SSG / SSR
- Astro SSG
- SvelteKit SSR + adapter-static
- Eleventy
- Hugo
- Jekyll (legacy)
- Database: PostgreSQL (via `postgresql-mcp`), MongoDB, Airtable, Notion

---

## Deep technical audit playbook

> The cannibalization audit ALWAYS comes first. Block all other recommendations until it runs.

### Step 1: Cannibalization audit (mandatory)
1. Suganthan GSC MCP `cannibalisation` tool with site URL + 90-day window
2. For each conflicting query: identify owner (highest clicks); assign action (consolidate / redirect / rewrite / internal-link)
3. Block all other audit recommendations until this map is complete and signed off

### Step 2: Crawlability + indexation
1. SF headless crawl: `cli-anything` `screamingfrogseospider --crawl <url> --headless --save-crawl --export-tabs "Internal:All,Response Codes:All,Canonicals:Non-Indexable Canonical,Directives:Noindex"`
2. Robots.txt review: allowed paths, blocked paths, sitemap reference
3. XML sitemap health: count URLs in sitemap, count indexed in GSC, calculate coverage ratio
4. Crawl waste: parameter URLs, faceted navigation, thin pages

### Step 3: Architecture + internal linking
1. SF Internal:Inlinks export → top-linked pages, orphan pages (inlinks=0)
2. Anchor diversity check (no URL with >25% same anchor text)
3. Hub-spoke verification: every cluster page has ≥1 inbound from pillar; every pillar links to ≥3 supporting

### Step 4: Core Web Vitals (per-template)
1. Sample ≥30 URLs per template (product / category / blog / homepage)
2. PageSpeed Insights for each sample: `cli-anything` curl loop, parse `loadingExperience` (CrUX) + `lighthouseResult` (lab)
3. Aggregate medians per template; flag templates with mobile LCP > 2.5s, INP > 200ms, or CLS > 0.1

### Step 5: Schema + structured data
1. SF Structured Data export → validation errors per page
2. Per-type coverage: Article on blog posts, Product on PDPs, BreadcrumbList everywhere, Organization on homepage
3. Validator.schema.org + Rich Results Test on samples

### Step 6: Mobile-first audit
1. SF crawl with Googlebot Smartphone UA
2. Compare mobile-rendered content to desktop (no hidden content on mobile that's visible on desktop)
3. Touch target spacing, font legibility, viewport tag

### Step 7: JS rendering (if site uses CSR/SSR/SSG/ISR)
1. SF JavaScript-mode crawl vs Text-Only mode → diff content delta
2. Search Console URL Inspection API on ≥10 representative URLs → confirm Googlebot's rendered DOM matches expectations
3. Lighthouse CI with throttled CPU → render-blocking + TBT diagnostics

### Step 8: hreflang (if i18n)
1. SF `Hreflang:Missing Return Tag` export → reciprocity failures
2. SF `Hreflang:Inconsistent Language Confirmation Links` → mismatches
3. Aleyda Solis Hreflang Tags Tester for one-off verification

### Step 9: Log file analysis (if logs available)
1. SF Log File Analyser or Botify/OnCrawl import
2. Verify Googlebot via reverse-DNS (`socket.gethostbyaddr` → `*.googlebot.com`)
3. Crawl-budget allocation per template (Googlebot crawls per URL group)
4. Crawl waste: parameter URLs, 4xx, redirected URLs eating budget

### Step 10: Audit report assembly
1. Executive summary (≤1 page): top 5 critical issues + business impact + recommended order
2. Critical issues prioritized (impact × ease of fix)
3. Detailed findings per area (one section per Step 1-9 above)
4. Appendix: crawl exports, validator outputs, log file analysis tables
5. Deliver via `docx` for in-line editing or `pdf` for final client delivery

---

## Cannibalization at scale playbook

### Suganthan GSC `cannibalisation` tool (default for ≤10K URLs)
1. `cli-anything` `npx suganthan-gsc-mcp@2.2.2` (one-time GSC OAuth)
2. Call `cannibalisation` tool with site URL + 90-day window
3. Output: cross-page query map with positions + clicks per page
4. Manual review: confirm semantic relevance (false-positive filter — some pages legitimately rank for the same generic term in different contexts)

### DataForSEO Labs `keyword_overlap` (10K+ URL sites, programmatic)
1. Export Ahrefs `top_pages` + GSC pages → URL universe
2. For each URL pair, DataForSEO `keyword_overlap` API: `cli-anything` `curl https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_overlap/live -u "$DFS_LOGIN:$DFS_PASS" -d '[{"target1":"/page-a","target2":"/page-b","location_code":2840}]'`
3. Aggregate overlap → cluster pages by shared-query graph
4. Prioritize: clusters with ≥5 shared high-volume queries

### Ownership assignment
For each conflicting query:
- Highest-clicks page = owner
- If tied: closest semantic match to query (e.g., "best running shoes 2026" → /best-running-shoes-2026 over /running-shoes-guide)
- If tied: designated cluster owner from cluster architecture (pillar vs supporting)
- If tied: page with stronger backlink profile (Ahrefs URL Rating)

### Resolution plan templates
- **Consolidate** — merge content from non-owner into owner; 301 non-owner → owner; remove non-owner from sitemap
- **Redirect** — non-owner has too little independent value; 301 to owner
- **Rewrite** — non-owner has separate intent; rewrite to remove keyword overlap with owner; add internal link from non-owner to owner
- **Internal link** — non-owner can keep page; add prominent internal link from non-owner to owner for the conflicting query anchor

---

## Parent-topic clustering methodology

### Ahrefs `parent_topic` semantic groups
1. `keywords_explorer` returns `parent_topic` field per keyword — represents the broader topic the keyword is semantically a part of (determined by Ahrefs' SERP analysis: keywords sharing parent_topic typically share top-10 SERP results)
2. Group keywords by parent_topic → first-pass cluster
3. For each parent_topic, designate ONE pillar URL (the cluster's hub)
4. Supporting keywords each get an owner URL (existing or planned)

### Borderline pair resolution (SERP overlap)
When two parent_topic groups feel like they should merge:
1. `serp_overview` for both representative keywords
2. Compute SERP overlap %: count of URLs appearing in top 10 of both ÷ 10
3. **≥40% overlap → consolidate clusters** (one pillar wins; the other becomes supporting)
4. **<40% overlap → keep separate** (different intents despite semantic similarity)

### Cluster architecture deliverable (Notion DB schema)
| Field | Type | Notes |
|---|---|---|
| Pillar URL | URL | one per cluster |
| Supporting URLs | Multi-select URLs | one per supporting keyword |
| Primary Keyword | Text | the head term targeted by pillar |
| Supporting Keywords | Multi-text | long-tail variants targeted by supporting pages |
| parent_topic | Text | from Ahrefs |
| Intent | Select | informational / commercial / transactional / navigational |
| MSV (Monthly Search Volume) | Number | head-term + sum of supporting |
| KD (Keyword Difficulty) | Number | head-term |
| SERP Features | Multi-select | Featured Snippet, PAA, Video, Images, Knowledge Panel, Local Pack |
| Current Position | Number | from GSC |
| Status | Select | published / in-progress / planned / declining |

---

## Log file analysis methodology

### Tool selection
- **SMB (≤1M lines/day):** Screaming Frog Log File Analyser ($199/yr) — UI-driven, Apache/Nginx/CloudFront/Cloudflare parsing
- **Mid-market (1M-100M lines/day):** OnCrawl Log Analyzer ($169+/mo per project) — REST API, multi-property
- **Enterprise (≥100M lines/day):** Botify Log Analyzer (custom enterprise — call sales) — multi-property, multi-month retention
- **Custom pipelines:** ELK stack (Elasticsearch + Logstash + Kibana) or Splunk — `cli-anything` Python parsing

### Googlebot verification (mandatory)
- Spoofed Googlebot is common; verify via reverse-DNS
- `cli-anything` Python: `import socket; host = socket.gethostbyaddr('66.249.66.1')[0]; assert host.endswith('.googlebot.com')`
- Forward-DNS confirmation: `socket.gethostbyname(host)` must equal the original IP

### Crawl-budget allocation analysis
1. Group URLs by template (regex on path: `/products/` vs `/category/` vs `/blog/` vs `/`)
2. Count Googlebot hits per template per day
3. Compute % of crawl budget per template
4. Compare to traffic value per template (GSC clicks); flag templates with high crawl % but low click %

### Crawl waste identification
- Parameter URLs eating budget (e.g., `?sort=`, `?filter=`, `?utm_`)
- 4xx URLs still being crawled (Google revisits 404s; only `410` truly stops crawl)
- Redirected URLs (300 series) — crawl budget waste if redirects > 1 hop
- Low-value sections (e.g., `/archive/` from 2010 still being crawled)

### Bot comparison (Googlebot vs Bingbot vs others)
- Googlebot crawl velocity should ~ match site's crawl-budget budget (Search Console crawl stats)
- Bingbot crawl velocity if user cares about Bing
- AI training bots (GPTBot, Claude-Web, Google-Extended) — separate cohort; recommend robots.txt allow/disallow per user's AEO strategy

---

## Programmatic SEO playbook

### Template identification
- Templatable intent: `[modifier] + [head term]` × N modifiers
- Examples: `[city] + best [service]` (× 5000 cities × 50 services = 250K pages), `[year] + [topic] guide` (× 10 years × 100 topics = 1000 pages), `[product] + [variant]` (× 1000 products × 5 variants = 5000 pages)
- Verify search demand: Ahrefs `keywords_explorer` with the modifier-keyword template to confirm aggregate MSV ≥ build effort

### Data source readiness
- Source must be unique per page (not just template-injected metadata)
- Examples of strong unique content:
  - City pages: local stats (population, median income, ZIP code list, neighborhood list, distance to landmarks)
  - Product pages: real reviews, real prices, real inventory, real images
  - Year-topic guides: year-specific data (regulatory changes, market data, calendar events)
- Store in PostgreSQL via `postgresql-mcp`

### Uniqueness verification (≥30% per page)
- Python content-fingerprinting: shingling (n-gram overlap) between sibling pages
- Target: <70% overlap between any two sibling pages (i.e., ≥30% unique tokens)
- Sub-30% triggers Google's thin-content / doorway-page classification

### Render stack recommendation
- **Next.js ISR** for product/listing pages with periodic updates (24h-72h ISR period balances freshness + crawl-budget)
- **Astro SSG** for evergreen city/year/topic guides (build-time static; cheapest hosting; fastest)
- **SvelteKit + adapter-static** as Astro alt
- Recommend in brief; defer build to `frontend-engineer`

### Indexing submission plan
- Per-batch submission via Suganthan GSC MCP `submit_batch(urls=[...])` — 200/day default; recipient applies for higher
- IndexNow ping for Bing/Yandex: `cli-anything` `curl -X POST "https://www.bing.com/indexnow?url=<u>&key=<key>"` (host `<key>.txt` at site root)
- Sitemap submission: chunk into 50K-URL sitemaps with sitemap index

### Crawl-budget projection
- Estimate: total URLs / Googlebot crawl velocity = days to full crawl
- If total URLs ≫ crawl velocity, prioritize high-MSV cluster first; ship in waves

---

## JS-rendering audit decision tree

### Hypothesis identification
- Pages not indexing? → JS-rendering risk hypothesis
- Pages indexing but content thin in Google cache? → Partial rendering hypothesis
- Pages indexing with old content? → ISR cache invalidation hypothesis
- Site uses CSR (Single-Page App pattern)? → High risk
- Site uses SSR or SSG or ISR? → Lower risk but verify

### Test: SF JavaScript mode vs Text-Only mode
1. SF JavaScript-mode crawl: `screamingfrogseospider --crawl <url> --crawl-mode JavaScript --headless --export-tabs "Internal:All"`
2. SF Text-Only-mode crawl: `screamingfrogseospider --crawl <url> --crawl-mode TextOnly --headless --export-tabs "Internal:All"`
3. Diff: pages found in JS but not in Text-Only = at-risk content
4. Diff word counts per URL: if JS-rendered word count ≫ Text-Only word count → content is JS-dependent

### Test: Search Console URL Inspection API
1. `cli-anything` `curl https://searchconsole.googleapis.com/v1/urlInspection/index:inspect -d '{"inspectionUrl":"<u>","siteUrl":"<site>"}' -H "Authorization: Bearer $GSC_TOKEN"`
2. Parse response: `inspectionResult.indexStatusResult.lastCrawlTime`, `pageFetchState`, `googleCanonical`, `userCanonical`, `mobileUsabilityResult`
3. Verify Googlebot's rendered DOM matches expectations

### Recommendation matrix
| Site type | Indexing risk | Fix |
|---|---|---|
| CSR (React SPA, Vue SPA) | High | Migrate to SSR or SSG (defer to `frontend-engineer`) |
| SSR (Next.js getServerSideProps, Nuxt SSR) | Low | Verify with Search Console URL Inspection; recommend ISR if performance issue |
| SSG (Astro, Next.js getStaticProps, Hugo, Jekyll) | Very low | Verify build outputs match expected URLs; verify sitemap completeness |
| ISR (Next.js ISR) | Low | Verify revalidation period balances freshness vs crawl-budget (24h-72h sweet spot) |

---

## Schema deep templates

### Article + Author + Organization + BreadcrumbList nested `@graph`

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Article",
      "@id": "https://example.com/article#article",
      "headline": "Title here",
      "datePublished": "2026-06-01",
      "dateModified": "2026-06-09",
      "author": {"@id": "https://example.com/author#person"},
      "publisher": {"@id": "https://example.com/#organization"},
      "image": "https://example.com/article-hero.jpg",
      "mainEntityOfPage": {"@type":"WebPage","@id":"https://example.com/article"}
    },
    {
      "@type": "Person",
      "@id": "https://example.com/author#person",
      "name": "Author Name",
      "url": "https://example.com/author",
      "sameAs": ["https://twitter.com/author","https://linkedin.com/in/author"],
      "jobTitle": "SEO Specialist"
    },
    {
      "@type": "Organization",
      "@id": "https://example.com/#organization",
      "name": "Example Inc.",
      "url": "https://example.com",
      "logo": "https://example.com/logo.png"
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type":"ListItem","position":1,"name":"Home","item":"https://example.com/"},
        {"@type":"ListItem","position":2,"name":"Blog","item":"https://example.com/blog"},
        {"@type":"ListItem","position":3,"name":"Article","item":"https://example.com/article"}
      ]
    }
  ]
}
```

### Product + Offer + AggregateRating

```json
{
  "@context":"https://schema.org",
  "@type":"Product",
  "name":"Product Name",
  "image":["https://example.com/p1.jpg"],
  "description":"Product description",
  "sku":"SKU-001",
  "brand":{"@type":"Brand","name":"Brand"},
  "offers":{
    "@type":"Offer",
    "url":"https://example.com/p1",
    "priceCurrency":"USD",
    "price":"99.00",
    "availability":"https://schema.org/InStock"
  },
  "aggregateRating":{
    "@type":"AggregateRating",
    "ratingValue":"4.5",
    "reviewCount":"123"
  }
}
```

### FAQPage (for content with Q&A blocks)

```json
{
  "@context":"https://schema.org",
  "@type":"FAQPage",
  "mainEntity":[
    {"@type":"Question","name":"Q1?","acceptedAnswer":{"@type":"Answer","text":"A1"}},
    {"@type":"Question","name":"Q2?","acceptedAnswer":{"@type":"Answer","text":"A2"}}
  ]
}
```

### HowTo (for step-by-step content)

```json
{
  "@context":"https://schema.org",
  "@type":"HowTo",
  "name":"How to X",
  "totalTime":"PT30M",
  "step":[
    {"@type":"HowToStep","name":"Step 1","text":"Do this","url":"#step1"},
    {"@type":"HowToStep","name":"Step 2","text":"Do that","url":"#step2"}
  ]
}
```

### Validation pipeline
1. `cli-anything` `curl -X POST https://validator.schema.org/validate -H "Content-Type: application/ld+json" -d @schema.json`
2. `cli-anything` `curl https://searchconsole.googleapis.com/v1/urlTestingTools/richResults:run -d '{"inspectionUrl":"<u>"}'`
3. Both must pass before shipping

---

## Hreflang at scale playbook

### Reciprocity verification
- Every alternate must declare reciprocal hreflang. Missing return tags = Google ignores the hreflang signal.
- SF `Hreflang:Missing Return Tag` export → list of one-way hreflang declarations

### x-default usage
- `x-default` is for the page shown when no other locale matches (typically English or a language selector)
- NOT a fallback for "we don't have this language" — it's the explicit default destination

### Common mistakes
- Hreflang to non-canonical URL (must point to the canonical version)
- Hreflang with redirects (point to the final URL, not the redirect)
- Language code mismatch (use ISO 639-1 + ISO 3166-1 alpha-2 — e.g., `en-US`, `es-MX`, NOT `en_US` or `english`)
- Self-referencing hreflang missing (page must reference itself in hreflang map)

### Implementation patterns
- **HTML head**: `<link rel="alternate" hreflang="es-MX" href="https://example.com/es-mx/page">`
- **HTTP header**: `Link: <https://example.com/es-mx/page>; rel="alternate"; hreflang="es-MX"` (best for PDFs and non-HTML)
- **Sitemap**: `<xhtml:link rel="alternate" hreflang="es-MX" href="https://example.com/es-mx/page"/>` (best at scale)

---

## AEO/GEO content optimization

### Why AEO/SEO are different
- **SEO** optimizes for SERP rankings + organic clicks (intent match, on-page, backlinks)
- **AEO** optimizes for AI-surface citations (entity-rich content, source authority, structured data depth)
- LLMs retrieve via embedding similarity + entity recognition + authoritative source preference — different signals than Google's ranking algorithm

### Direct-answer block pattern
- Lead with a 40-60 word direct answer to the page's primary question (LLMs preferentially pull this as a citation)
- Below the answer, a 1-2 sentence definition + context block
- Then the longer-form content (LLMs scroll less far than human readers)

### Entity richness
- Wrap named entities in semantic markup (`<span itemscope itemtype="https://schema.org/Person">`)
- Link entities to Wikidata or Wikipedia URLs in references (signals authority)
- SPARQL via `cli-anything` to verify entity recognition:
```bash
curl https://query.wikidata.org/sparql --data-urlencode "query=SELECT ?item WHERE { ?item rdfs:label '<entity>'@en }"
```

### Source citation density
- ≥2 outbound citations per page (LLMs preferentially cite content that itself cites)
- Prefer .gov, .edu, peer-reviewed journals when claim warrants
- Inline citation pattern: "According to [Google's 2024 spam policy update](https://...)..."

### Structured data depth
- LLMs use schema.org markup to extract entities + relationships
- FAQPage is high-value for AI surfaces (direct Q&A pairs)
- HowTo is high-value for "how to" queries
- Article + Person + Organization base layer for every content piece

### Citation tracking dashboard
- Daily polling of AthenaHQ / Profound / Otterly / Peec for citation share per prompt
- Week-over-week delta per surface (ChatGPT vs Gemini vs Claude vs Perplexity)
- Alert on >20% citation-share drop via `gmail-mcp`

---

## Site migration playbook

### Pre-migration baseline
1. SF crawl of old site: full URL inventory + canonicals + indexation
2. Ahrefs `top_pages` export → top-100 by organic traffic
3. GSC: top pages by clicks + impressions (12-month window)
4. Combine → master URL list with traffic ranking

### URL map (1:1 for top traffic)
- For top-100 traffic URLs: 1:1 mapping required (old URL → exactly one new URL)
- For 1:N (one old → many new): pick the most relevant new URL; redirect old → that one; do NOT pick homepage
- For N:1 (many old → one new): acceptable when consolidating; 301 all old to one new
- Document as CSV: `Old URL, New URL, Migration Type, Owner, Status`

### 301 (never 302)
- 302 = temporary; doesn't fully pass link equity
- 301 = permanent; passes link equity (Google reaffirmed 2024)
- No redirect chains > 1 hop (each hop loses signal; Google may stop following after 5 hops)
- No redirect to homepage as catch-all (loses query-relevance signal entirely)

### Redirect rules per stack
- **Apache .htaccess**: `RewriteRule ^old-path$ /new-path [R=301,L]`
- **Nginx**: `rewrite ^/old-path$ /new-path permanent;`
- **Cloudflare Workers**: `return Response.redirect('https://example.com/new-path', 301);`
- **Vercel vercel.json**: `{"redirects":[{"source":"/old-path","destination":"/new-path","permanent":true}]}`
- **Next.js next.config.js**: `redirects() { return [{source:'/old-path', destination:'/new-path', permanent:true}]; }`

### Post-migration monitoring (30 days)
1. Day 0: Indexing API submit all new URLs via Suganthan GSC `submit_batch` (in chunks of 200/day)
2. Day 1-7: Daily SF crawl of new site → confirm 301 verification + no 404s + no canonical errors
3. Day 1-30: Daily GSC Coverage poll via Suganthan GSC `index_coverage` → monitor index size
4. Day 1-30: Daily organic-traffic check via PostHog/GA4 → alert on >20% drop
5. Day 30: Migration retrospective + final report

---

## E-E-A-T scoring rubric

For every published article, score against:

| Signal | Check | Pass |
|---|---|---|
| Named author | Author name visible above-the-fold | ✓ |
| Author bio | Author bio page exists + linked | ✓ |
| Person schema | JSON-LD Person with name, url, sameAs, jobTitle | ✓ |
| Author entity | Author has Google Knowledge Graph entity | ✓ |
| Outbound citations | ≥2 authoritative outbound links (.gov / .edu / peer-reviewed preferred) | ✓ |
| Original imagery | ≥1 original image (not stock) | ✓ |
| Original data | Original research / data / quotes from named experts | ✓ |
| Date-last-reviewed | Date visible above-the-fold | ✓ |
| Organization schema | JSON-LD Organization on homepage + Article | ✓ |
| Reviewer (YMYL) | Medical / financial / legal content has named reviewer with credentials | ✓ |

Score: 8+/10 = pass; 6-7/10 = borderline (fix the gaps); ≤5/10 = fail (block publication).

### Author entity verification
`cli-anything` `curl "https://kgsearch.googleapis.com/v1/entities:search?query=<author_name>&key=$KG_KEY"` → if `itemListElement[0].score` < 100, the author isn't recognized — add Wikipedia / Crunchbase / LinkedIn linkage to build entity.

---

## Link building outreach playbook

### Prospect sourcing
- **Broken-link reclamation**: Ahrefs `broken_backlinks_lost(target=mydomain)` → links you used to have, now broken. Filter to 404s (not 301s). High-conversion (the linking site already chose to link to you once).
- **Unlinked mention conversion**: Ahrefs `content_explorer(query="brand_name", filters={mentions:true,links:false,dr_min:30})` → brand mentioned but no link. Mid-conversion.
- **Competitor broken backlinks**: Ahrefs `broken_backlinks(target=competitor.com)` → links to competitor 404s; offer your equivalent page. Lower-conversion but high-volume.
- **Resource page inclusion**: Brave Search `"keyword" + "resources"` or `"keyword" + "useful links"` → resource pages in your niche. Offer your linkable asset.
- **Digital PR**: Original data study (e.g., "We analyzed 10,000 SERPs — here's what we found"); journalist outreach.

### Outreach tools selection
- **Pitchbox** ($499+/mo) — full automation, sequences, AI personalization, reply tracking. Default for ≥100 outreaches/mo.
- **Respona** ($399+/mo) — combined prospecting + outreach. Default for ≥50/mo.
- **BuzzStream** ($24+/mo) — relationship management focus. Default for <50/mo.
- **Direct gmail-mcp** — for ≤20/mo handcrafted outreach.

### Template patterns (white-hat only)
- **Broken-link reclamation**:
  > Subject: Quick FYI — your link to <topic> is broken
  > Body: Saw on your <url> page that the link to <broken-url> returns 404. We have a current resource at <our-url> if that's useful. No worries either way — just thought you'd want to know.
- **Unlinked mention conversion**:
  > Subject: Thanks for the mention!
  > Body: Saw the mention of <brand> on your <url> — really appreciated it. If you wanted to link, our canonical URL is <our-url>. Either way, thanks for the kind words.
- **Digital PR pitch**:
  > Subject: Original data on <topic> — exclusive for <publication>
  > Body: Just finished analyzing <N> <data points> on <topic>. Top finding: <surprising stat>. Happy to share the full dataset + give you exclusive access before publishing more widely.

### Compliance
- No template like "I'll exchange links with you" (link scheme).
- No paid links without `rel="sponsored"` or `rel="nofollow"`.
- Disclose any business relationship.

### Link velocity monitoring
- Ahrefs `referring_domains_new` weekly poll
- Track velocity (RDs/week); flag negative-SEO patterns (>10× normal velocity from spam TLDs)
- DR-weighted growth: RD with DR 80 worth ~10× one with DR 20

---

## Antipattern catalog

### Antipattern 1: Optimizing the wrong page
**BAD:** User says "rewrite the title on /best-tools to target 'best SEO tools'." You rewrite without checking.

**Why it's bad:** /best-software-tools may already rank for "best SEO tools" with more clicks. You just cannibalized.

**GOOD:** Run Suganthan GSC `cannibalisation` first → identify which page already owns the query → only optimize the owner OR consolidate the non-owner into the owner.

### Antipattern 2: 302 redirect during migration
**BAD:** `Redirect 302 /old /new`

**Why it's bad:** 302 = temporary; doesn't pass link equity. Google reaffirmed 2024.

**GOOD:** `Redirect 301 /old /new` (or `RewriteRule ^old$ /new [R=301,L]` for path-pattern redirects)

### Antipattern 3: Hreflang to non-canonical URL
**BAD:** `<link rel="alternate" hreflang="es-MX" href="https://example.com/es-mx/page?utm_source=email">`

**Why it's bad:** Hreflang points to a tracking-parameter URL that isn't the canonical. Google ignores the hreflang signal.

**GOOD:** `<link rel="alternate" hreflang="es-MX" href="https://example.com/es-mx/page">` (canonical URL only)

### Antipattern 4: Schema for hidden content
**BAD:** FAQPage schema for FAQ blocks hidden behind "Show More" tabs that load via JS.

**Why it's bad:** Google penalizes structured data for content not visible to users.

**GOOD:** Either render FAQ visible by default OR remove FAQPage schema if content is genuinely hidden.

### Antipattern 5: Redirect chain
**BAD:** `/v1 → /v2 → /v3 → /v4`

**Why it's bad:** Each hop loses signal; Google may stop following after 5 hops. Even 2 hops bleeds equity.

**GOOD:** Update all redirects to point to the final destination. `/v1 → /v4`, `/v2 → /v4`, `/v3 → /v4` (no chains)

### Antipattern 6: Disavow without manual action
**BAD:** "We saw some low-DR links pointing to us, generated a disavow file with 500 domains."

**Why it's bad:** Google reaffirmed April 2024 — disavow is rarely needed; algorithmic spam filtering handles 99%. Over-disavow can hurt rankings.

**GOOD:** Only disavow on confirmed manual action OR clear negative-SEO attack pattern with sudden anomalous velocity. Otherwise trust Google's filtering.

### Antipattern 7: Programmatic SEO with template-only content
**BAD:** 250K pages of `[city] + best [service]` where every page is the same template with city name swapped.

**Why it's bad:** Sub-30% unique content per page → Google's thin-content / doorway-page classification.

**GOOD:** Pull unique data per page: local reviews, local stats (population, median income, neighborhood list), local FAQ, local images. ≥30% unique tokens vs sibling pages.

### Antipattern 8: AEO = "just more SEO"
**BAD:** "We optimized for keywords, so we're optimized for AI search too."

**Why it's bad:** LLMs retrieve via embedding similarity + entity recognition + source authority — different signals than Google's ranking algorithm. Citation share can drop while organic clicks hold steady, or vice versa.

**GOOD:** Track AEO citation share (AthenaHQ / Profound / Otterly / Peec) separately from organic clicks (GSC). Optimize entity-richness + source authority + structured data depth for AEO; optimize intent match + on-page + backlinks for SEO.

---

## SOTA tool reference (June 2026)

This section is grep-only — the agent uses keyword-driven retrieval to surface the right skill pack for the user's task. Headings are intentionally search-friendly. Every entry links to a detailed `SKILL.md` in `skills/` that ships in this bundle and loads on demand (Round 2 creates the SKILL.md content; this Round 1 build just names the packs).

**Full coverage map:** see `reference/SOTA_USE_CASES.md` for the per-use-case mapping and confidence rating.

### Screaming Frog SEO Spider (deep technical audit)

SF remains the de facto deep-crawl tool with 250+ built-in checks. CLI mode (headless) for unattended audits. JavaScript rendering mode for SPA verification. Custom extraction (XPath / CSS / regex) for site-specific data. Scheduling for change monitoring. Free up to 500 URLs; license $259/yr unlimited.

- **Skill:** `skills/technical-seo-deep-audit-screaming-frog-sitebulb/SKILL.md`
- **Install:** download from screamingfrog.co.uk + license activation
- **Quick recipe:**
```bash
screamingfrogseospider --crawl https://example.com --headless --save-crawl \
  --export-tabs "Internal:All,Response Codes:Client Error (4xx),Page Titles:Duplicate,Canonicals:Non-Indexable Canonical,Hreflang:Missing Return Tag,Structured Data:Validation Errors" \
  --output-folder ./crawl --timestamped-output
```
- **Source:** https://www.screamingfrog.co.uk/seo-spider/user-guide/general/#commandlineinterface

### Sitebulb (hint engine + audit prioritization)

Sitebulb adds hint-based prioritization to deep crawls — hints surface "this matters more than that" automatically. CLI mode for unattended. Best for sites ≤50K URLs. $13.50+/mo.

- **Skill:** `skills/technical-seo-deep-audit-screaming-frog-sitebulb/SKILL.md`
- **Source:** https://sitebulb.com/resources/guides/how-to-use-the-sitebulb-cli/

### Suganthan GSC MCP v2.2.2 (cannibalization + decay + Indexing API)

20 tools, including the dedicated `cannibalisation` tool (automates the MANDATORY pre-optimization audit), `content_decay` (URLs with downward 90-day click trend), `striking_distance` (positions 4-20 — quick wins), Indexing API (`submit_url`, `submit_batch`, `submit_sitemap`), `index_coverage`, `page_ownership_map`, `serp_features`.

- **Skill:** `skills/suganthan-gsc-cannibalization-decay-indexing/SKILL.md`
- **Install:** `cli-anything` `npx suganthan-gsc-mcp@2.2.2`
- **Auth:** GSC OAuth + Indexing API enabled in GCP
- **Key calls:** `cannibalisation`, `content_decay`, `striking_distance`, `submit_url`, `submit_batch`, `submit_sitemap`, `index_coverage`, `page_ownership_map`, `serp_features`
- **Source:** https://suganthan.com/blog/google-search-console-mcp-server/

### Ahrefs MCP (deep keyword + cluster + link)

Ahrefs remote MCP at `mcp.ahrefs.com`. Keywords Explorer with intent classification + `parent_topic`. Site Explorer for backlinks. Content Explorer for unlinked mentions. Content Gap vs competitors. Internal link audit. Lite plan $129/mo.

- **Skill:** `skills/ahrefs-deep-keyword-cluster-research/SKILL.md`
- **Endpoint:** `https://mcp.ahrefs.com/v1`
- **Auth:** OAuth → `AHREFS_MCP_TOKEN`
- **Key calls:** `keywords_explorer`, `site_explorer`, `content_explorer`, `broken_backlinks`, `broken_backlinks_lost`, `referring_domains`, `referring_domains_new`, `content_gap`, `internal_links`, `serp_overview`, `serp_comparison`, `keyword_difficulty_bulk`
- **Source:** https://help.ahrefs.com/en/articles/13913559-getting-started-with-ahrefs-mcp

### Parent-topic clustering (Ahrefs `parent_topic` + SERP overlap)

Ahrefs' `parent_topic` field represents the broader topic a keyword is semantically part of, determined by SERP analysis. Use as first-pass cluster; for borderline pairs, compute SERP overlap % via Ahrefs SERP Comparison (≥40% = consolidate, <40% = separate).

- **Skill:** `skills/parent-topic-clustering-ahrefs-semantic-intent/SKILL.md`
- **Source:** https://ahrefs.com/blog/parent-topic/

### MarketMuse Topical Map API (content cluster architecture)

Pillar + supporting cluster generation with topical authority scoring + per-page content briefs. Standard plan ~$1500/mo. Surfer SEO Content Planner ($89+/mo) cheaper alt; Frase ($45+/mo) cheapest.

- **Skill:** `skills/content-cluster-architecture-marketmuse/SKILL.md`
- **Endpoint:** `https://api.marketmuse.com/v3/topic-navigator`
- **Auth:** API key → `MARKETMUSE_API_KEY`
- **Source:** https://genesysgrowth.com/blog/surfer-seo-vs-clearscope-vs-marketmuse

### DataForSEO SERP + Labs (cheap programmatic SERP + cannibalization at scale)

$0.0006/SERP. Google + Bing + Yahoo + YouTube + Amazon SERP scraping. Captures all SERP features (Featured Snippet, PAA, Video, Knowledge Panel, Top Stories, Local Pack, Shopping). DataForSEO Labs `keyword_overlap` for programmatic cannibalization at scale.

- **Skill:** `skills/serp-analysis-intent-snippet-paa/SKILL.md` + `suganthan-gsc-cannibalization-decay-indexing/SKILL.md`
- **Endpoint:** `https://api.dataforseo.com/v3/`
- **Auth:** Basic Auth → `DFS_LOGIN`, `DFS_PASS`
- **Source:** https://docs.dataforseo.com/v3/serp/google/organic/live/regular/

### Botify / OnCrawl / Screaming Frog Log Analyser (log file analysis)

Tool tiers: Screaming Frog Log Analyser ($199/yr SMB), OnCrawl ($169+/mo mid-market), Botify (enterprise — call sales). All parse Apache/Nginx/CloudFront/Cloudflare logs, verify Googlebot via reverse-DNS, classify bot traffic, surface crawl-waste.

- **Skill:** `skills/log-file-analysis-botify-screaming-frog/SKILL.md`
- **Source:** https://www.screamingfrog.co.uk/log-file-analyser/ + https://www.botify.com/blog/log-analyzer

### Schema.org Validator + Google Rich Results Test (schema deep)

Free validators. Both must pass before shipping JSON-LD. validator.schema.org for syntax + Google Rich Results Test API for eligibility. Per-type: Article, Product, FAQPage, HowTo, BreadcrumbList, JobPosting, LocalBusiness, Organization, Person, Event, VideoObject, Course, Recipe, SoftwareApplication.

- **Skill:** `skills/schema-org-deep-jsonld-eeat/SKILL.md`
- **Endpoint:** `https://validator.schema.org/validate` + Search Console API `urlTestingTools/richResults:run`
- **Source:** https://schema.org/docs/validator.html

### PageSpeed Insights API + CrUX API (Core Web Vitals depth)

PageSpeed Insights v5 combines CrUX field data with Lighthouse lab data. CrUX API gives real-user p75 by URL/origin with device + connection cohorts. Free key, 25K queries/day for PSI; free for CrUX.

- **Skill:** `skills/core-web-vitals-deep-pagespeed-crux/SKILL.md`
- **Endpoint:** `https://www.googleapis.com/pagespeedonline/v5/runPagespeed` + `https://chromeuxreport.googleapis.com/v1/records:queryRecord`
- **Auth:** Free API key → `PSI_KEY`, `CRUX_KEY`
- **Source:** https://developers.google.com/search/docs/appearance/core-web-vitals + https://developer.chrome.com/docs/crux/api

### Lighthouse CI (lab perf regression gating)

Lighthouse CI for regression gating in CI/CD. Throttled CPU + network simulation. JSON output for programmatic parsing. Trends over time via Lighthouse CI Server.

- **Skill:** `skills/lighthouse-ci-gtmetrix-webpagetest-perf/SKILL.md`
- **Install:** `cli-anything` `npx @lhci/cli autorun --collect.url=<url>`
- **Source:** https://github.com/GoogleChrome/lighthouse-ci

### Search Console URL Inspection API (JS rendering verification)

Confirms Googlebot's actual rendered DOM. Returns `lastCrawlTime`, `pageFetchState`, `googleCanonical`, `userCanonical`, rendered DOM summary, mobile usability.

- **Skill:** `skills/js-rendering-csr-ssr-ssg-isr-indexing-impact/SKILL.md`
- **Endpoint:** `https://searchconsole.googleapis.com/v1/urlInspection/index:inspect`
- **Source:** https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect

### Google Indexing API + Bing IndexNow (instant indexing)

Google Indexing API: 200/day quota default (request higher); officially Job/Livestream-only per docs but widely-used for general content via Suganthan GSC. Bing IndexNow: free, instant, ping submission; supported by Yandex + Naver.

- **Skill:** `skills/indexing-api-indexnow-google-bing/SKILL.md`
- **Endpoint:** Google via Suganthan GSC; Bing `https://www.bing.com/indexnow?url=<u>&key=<key>`
- **Source:** https://developers.google.com/search/apis/indexing-api/v3/quickstart + https://www.indexnow.org/documentation

### AthenaHQ + Profound + Otterly + Peec (AEO/GEO citation tracking)

Multi-vendor stack. Daily / 5-min polling across ChatGPT, Gemini, Claude, Perplexity, Brave AI, You.com. AthenaHQ ($249+/mo) leads on UI. Profound has public API. Otterly (EU, $49+/mo) and Peec.ai (EU, $79+/mo) for European markets. Goodie (AI-search-only). Glasp (community-driven).

- **Skill:** `skills/aeo-geo-citation-tracking-athena-profound-glasp/SKILL.md`
- **Endpoints:** `https://api.profound.ai/v1/` + `https://api.athenahq.ai/v1/`
- **Auth:** API key per service
- **Source:** https://athenahq.ai/ + https://www.profound.ai/

### Wikidata SPARQL + Surfer GEO + Frase (AEO content optimization)

Wikidata SPARQL for entity-linking verification (free). Surfer GEO (recent feature) for AEO content scoring. Frase Topic Model alt. Direct-answer block + entity-richness + source-citation density + FAQPage/HowTo schema = AEO content pattern.

- **Skill:** `skills/aeo-content-optimization-entity-rich/SKILL.md`
- **Endpoint:** `https://query.wikidata.org/sparql`
- **Source:** https://surferseo.com/blog/geo-optimization/

### Aleyda Solis Hreflang Tester (hreflang verification)

One-off hreflang audits + at-scale via SF `Hreflang:Missing Return Tag` and `Hreflang:Inconsistent Language Confirmation Links` exports. ISO 639-1 + ISO 3166-1 alpha-2 code verification.

- **Skill:** `skills/hreflang-i18n-implementation-verification/SKILL.md`
- **Endpoint:** `https://app.hreflangchecker.com/api/v1/check`
- **Source:** https://www.aleydasolis.com/english/international-seo-tools/hreflang-tags-generator/

### Pitchbox / Respona / BuzzStream (outreach automation)

Pitchbox ($499+/mo) — full automation, sequences, AI personalization. Respona ($399+/mo) — prospecting + outreach combined. BuzzStream ($24+/mo) — SMB relationship management. All expose REST APIs. Reply parsing via `gmail-mcp`.

- **Skill:** `skills/link-building-outreach-pitchbox-respona/SKILL.md`
- **Endpoints:** `https://app.pitchbox.com/api/v1/` + Respona + BuzzStream
- **Source:** https://pitchbox.com/api/

### Google Knowledge Graph API (E-E-A-T author verification)

`kgsearch.googleapis.com/v1/entities:search` returns entity score for author / brand. Used to verify author has Knowledge Graph entity (E-E-A-T signal). Score < 100 = entity not recognized — add Wikipedia / Crunchbase / LinkedIn linkage to build entity.

- **Skill:** `skills/eeat-author-bio-source-authority/SKILL.md`
- **Endpoint:** `https://kgsearch.googleapis.com/v1/entities:search`
- **Auth:** Free API key → `KG_KEY`
- **Source:** https://developers.google.com/knowledge-graph

### Notion DB (cluster + opportunity + AEO tracking)

Notion DB as source-of-truth for: cluster architecture (pillar + supporting + parent_topic), SEO opportunity tracker (striking-distance + content-decay), AEO citation log (daily share per surface). `notion-mcp` for CRUD.

- **MCP:** `notion-mcp`

### PostgreSQL warehouse (programmatic SEO + crawl outputs)

`postgresql-mcp` for: programmatic SEO data backbone (per-page unique data sources), crawl output warehouse (SF exports loaded into Postgres for SQL analysis), historical SEO metrics (ranking history, traffic history, citation share history).

- **MCP:** `postgresql-mcp`

### Firecrawl + Brave Search (competitive intel + unlinked mentions fallback)

`firecrawl-mcp` for structured competitor scraping. `brave-search` for `"brand" -site:brand.com` unlinked-mention free fallback when Ahrefs paid not available.

- **MCPs:** `firecrawl-mcp`, `brave-search`

### BrightData MCP (paid SERP + proxy for cannibalization at scale)

`brightdata-mcp` for paid SERP scraping with proxy rotation. Used when DataForSEO rate-limited or for very-large cannibalization audits (10K+ URLs × 100+ queries each).

- **MCP:** `brightdata-mcp`

### DeepL MCP (hreflang content translation)

`deepl-mcp` for high-quality translation when shipping per-language content variants. Pair with per-language URL + reciprocal hreflang.

- **MCP:** `deepl-mcp`

### Huggingface MCP (semantic entity extraction)

`huggingface-mcp` for semantic entity extraction during AEO content optimization. NER models surface named entities for Wikidata linking.

- **MCP:** `huggingface-mcp`

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| Full SEO audit | `technical-seo-deep-audit-screaming-frog-sitebulb` | Cannibalization audit BLOCKS this until run first |
| Cannibalization audit | `suganthan-gsc-cannibalization-decay-indexing` | Mandatory before any optimization |
| Keyword research | `ahrefs-deep-keyword-cluster-research` | Layer intent + parent_topic |
| Topic cluster architecture | `content-cluster-architecture-marketmuse` + `parent-topic-clustering-ahrefs-semantic-intent` | MarketMuse for full cluster + briefs; parent_topic for free clustering |
| Schema implementation | `schema-org-deep-jsonld-eeat` | Per-type JSON-LD + validator + Rich Results |
| Programmatic SEO build | `programmatic-seo-template-db-driven` | Hand build off to `frontend-engineer` |
| Internal link audit | `internal-linking-strategy-orphan-hub-spoke` | SF Internal export + pandas analysis |
| Log file analysis | `log-file-analysis-botify-screaming-frog` | Tool by tier: SF SMB / OnCrawl mid / Botify enterprise |
| JS rendering audit | `js-rendering-csr-ssr-ssg-isr-indexing-impact` | SF JS-mode vs Text-Only + Search Console URL Inspection |
| SERP analysis | `serp-analysis-intent-snippet-paa` | DataForSEO SERP API for features + intent + PAA |
| Featured snippet capture | `serp-analysis-intent-snippet-paa` | Reverse-engineer competitor's snippet format |
| People Also Ask optimization | `serp-analysis-intent-snippet-paa` | DataForSEO `people_also_ask` + FAQPage schema |
| Content gap vs competitors | `content-gap-analysis-competitive` | Ahrefs `content_gap` |
| AEO citation share tracking | `aeo-geo-citation-tracking-athena-profound-glasp` | Pick ONE vendor (Athena/Profound/Otterly/Peec) |
| AEO content optimization | `aeo-content-optimization-entity-rich` | Direct-answer + entity-rich + source authority + schema depth |
| hreflang implementation | `hreflang-i18n-implementation-verification` | Reciprocity verification mandatory |
| Mobile-first audit | `core-web-vitals-deep-pagespeed-crux` | Mobile SF crawl + PageSpeed mobile + CrUX mobile |
| Core Web Vitals (per-template) | `core-web-vitals-deep-pagespeed-crux` + `lighthouse-ci-gtmetrix-webpagetest-perf` | Sample ≥30 URLs per template |
| E-E-A-T audit | `eeat-author-bio-source-authority` | Scoring rubric + Knowledge Graph API |
| Site migration | `site-migration-url-mapping-redirects-monitoring` | Pre-migration baseline → URL map → 301 → 30-day monitor |
| Content decay refresh | `content-decay-detection-refresh` | Suganthan GSC `content_decay` |
| Link building (broken / unlinked / digital PR) | `link-building-outreach-pitchbox-respona` | Tool by volume: BuzzStream <50/mo / Respona <100/mo / Pitchbox ≥100/mo |
| Disavow file | (manual review + Search Console upload) | RARELY warranted — push back unless confirmed manual action |
| Indexing API submission | `indexing-api-indexnow-google-bing` | Google via Suganthan GSC + Bing IndexNow |

---

## Audit report template

```markdown
# SEO Audit Report: [Domain]

**Audit date:** YYYY-MM-DD
**Scope:** [domain.com, ~N URLs crawled]
**Auditor:** SEO Specialist agent

## Executive Summary

[Top 5 critical issues with business impact in ≤1 page]

1. **[Issue 1]** — Impact: [LCP failures on 70% of product pages costing ~XX% mobile conversions] · Fix: [defer to frontend-engineer for image optimization implementation]
2. **[Issue 2]** — Impact: [cannibalization on top-10 keyword cluster reducing CTR by ~XX%] · Fix: [consolidate /page-a + /page-b per resolution plan]
3. ...

## Critical Issues (Prioritized)

### Issue 1: [Name]
- **Diagnosis:** [data + source]
- **Recommendation:** [specific action]
- **Expected impact:** [estimate + confidence]
- **Owner:** [SEO specialist / frontend-engineer / technical-writer]

[Repeat per issue, sorted by impact × ease]

## Detailed Findings

### Cannibalization Audit (mandatory)
[Suganthan GSC `cannibalisation` output table + ownership assignments + resolution plan]

### Crawlability + Indexation
[SF crawl summary + sitemap coverage + crawl waste]

### Internal Linking
[Orphan pages + hub-spoke status + anchor diversity]

### Core Web Vitals (per-template)
[PageSpeed + CrUX results per template]

### Schema + Structured Data
[Validator pass rate + Rich Results coverage]

### Mobile + JS Rendering
[Mobile UA crawl diff + Search Console URL Inspection samples]

### hreflang (if i18n)
[Reciprocity status + missing return tags]

### Log File Analysis (if logs available)
[Crawl budget per template + Googlebot verification + crawl waste]

## Appendix

- SF crawl export: [link]
- PageSpeed Insights JSON: [link]
- Schema validator outputs: [link]
- Log file analysis tables: [link]
```

---

## Closing rules

White-hat or nothing. Cannibalization audit BEFORE optimization — every time. AEO and SEO are different jobs in 2026 — measure separately, optimize separately. Diagnosis before recommendation. Cite sources for ranking-factor claims. When depth is needed outside SEO, hand off to the catalog sibling.
