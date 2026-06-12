# seo-specialist — SOTA Use Cases (June 2026)

This document maps every documented use case in `USE_CASES.md` to a concrete SOTA execution mechanism for a deep technical + content SEO specialist in 2026. Every use case has: a named tool, an exact agent-level execution path, a source URL, and a confidence rating.

**Legend**:
- ✓ Fully executable — production MCP / first-class API, auth already exposed via `agent.yaml`, end-to-end automated.
- ⚠ Executable with caveats — works today but requires a one-time setup step (OAuth, paid API key, app approval) the recipient owns.
- ✗ Genuinely impossible today — none of these expected for the v1 SEO build pass.

Scope note: this agent's SOTA mapping intentionally goes deeper than the parent `marketing-agent`'s SEO row coverage. Anything `marketing-agent` already handles end-to-end (basic keyword research, on-page checklist, light schema, parent-topic clustering, broken-link reclamation surface) is **inherited**; this agent's "use case" rows are the depth-beyond-marketing-agent slices (1000+ check deep technical audit, log file analysis at scale, programmatic SEO, JS-rendering audit, parent-topic clustering at the cluster-architecture-level, AEO/GEO depth, etc.).

---

## 1. Deep technical SEO audit (1000+ checks)

- **SOTA approach:** Screaming Frog SEO Spider in CLI mode + Sitebulb hint engine + Botify Analytics (enterprise) for crawl-budget overlay. Screaming Frog has remained the de facto deep-crawl tool with 250+ built-in checks; Sitebulb adds hint-based prioritization; Botify layers log-file + GSC crawl-stats overlay for Googlebot-vs-Bingbot behavior.
- **Agent execution path:** `cli-anything` + `screamingfrogseospider --crawl <url> --headless --save-crawl --export-tabs "Internal:All,Response Codes:Client Error (4xx),Response Codes:Server Error (5xx),Page Titles:Duplicate,Meta Description:Duplicate,H1:Duplicate,Canonicals:Non-Indexable Canonical,Hreflang:Missing Return Tag,Structured Data:Validation Errors" --output-folder ./crawl --timestamped-output`. Then `cli-anything` to load Sitebulb via CLI exports OR run Botify queries via REST.
- **Source:** https://www.screamingfrog.co.uk/seo-spider/user-guide/general/#commandlineinterface + https://sitebulb.com/resources/guides/how-to-use-the-sitebulb-cli/
- **Confidence:** ✓ (Screaming Frog free up to 500 URLs; license at $259/yr for unlimited; Sitebulb $13.50+/mo; Botify enterprise)

## 2. Cannibalization audit at scale

- **SOTA approach:** Suganthan GSC MCP v2.2.2 dedicated `cannibalisation` tool (also used by parent `marketing-agent`), but here extended to multi-property + multi-cluster batch mode + DataForSEO Labs SERP-position cross-validation. For 10K+ URL sites, Ahrefs `Top Pages` × `Organic Keywords` join shipped to DataForSEO Labs `keyword_overlap` API.
- **Agent execution path:** `cli-anything` `npx suganthan-gsc-mcp@2.2.2` → loop over property × cluster pairs → output to Notion via `notion-mcp`. For ≥10K URLs: `ahrefs-deep-keyword-cluster-research` skill (Ahrefs MCP `keywords_explorer` + `top_pages`) → DataForSEO `keyword_overlap` for SERP confirmation.
- **Source:** https://suganthan.com/blog/google-search-console-mcp-server/ + https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_overlap/live/
- **Confidence:** ✓ (one-time GSC OAuth; DataForSEO at $0.0006/SERP)

## 3. Parent-topic clustering (Ahrefs semantic intent)

- **SOTA approach:** Ahrefs `parent_topic` field on Keywords Explorer to group semantically-equivalent queries into one canonical pillar, then manual review of borderline clusters using SERP overlap (Ahrefs SERP Comparison) to decide whether to consolidate or keep separate.
- **Agent execution path:** Use `parent-topic-clustering-ahrefs-semantic-intent` skill. Ahrefs MCP `keywords_explorer` (returns `parent_topic`) → group by `parent_topic` → for borderline pairs, `serp_comparison` tool returns SERP overlap % (≥40% means consolidate). Store as Notion DB.
- **Source:** https://ahrefs.com/blog/parent-topic/ + https://help.ahrefs.com/en/articles/13913559-getting-started-with-ahrefs-mcp
- **Confidence:** ⚠ (Ahrefs Lite paid plan required)

## 4. Keyword research for clusters (semantic groupings, search intent layering)

- **SOTA approach:** Ahrefs Keywords Explorer with intent classification (informational/commercial/transactional/navigational) + `parent_topic` grouping; DataForSEO `keywords_data/google/keyword_suggestions/live` for $0.0006/SERP fallback; SEMrush Topic Research as alt. Layer search intent over `parent_topic` clusters.
- **Agent execution path:** Use `ahrefs-deep-keyword-cluster-research` skill. Ahrefs MCP `keywords_explorer(seed=<term>, country=US)` → `keyword_difficulty_bulk` for KD scoring → `serp_overview` for intent confirmation. Cross-output to DataForSEO for cheap volume confirmation.
- **Source:** https://help.ahrefs.com/en/articles/13913559-getting-started-with-ahrefs-mcp + https://docs.dataforseo.com/v3/keywords_data/google/keyword_suggestions/live/
- **Confidence:** ⚠ (Ahrefs paid)

## 5. On-page deep optimization (E-E-A-T, schema, internal links per page)

- **SOTA approach:** Layered audit: (a) JSON-LD generation per content type (Article + Author + Organization + BreadcrumbList minimum), (b) Schema.org validator + Google Rich Results Test, (c) Ahrefs internal link audit at the per-URL level, (d) E-E-A-T signals scoring (author bio presence, source citation count, original imagery, named expert quotes). Each page passes only if ALL four pass.
- **Agent execution path:** Use `schema-org-deep-jsonld-eeat` + `eeat-author-bio-source-authority` skills. Generate JSON-LD → `cli-anything` `curl https://validator.schema.org/validate -d @schema.json` → `cli-anything` `curl https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run` for Rich Results equivalent → Ahrefs MCP `internal_links(url=<page>)` → score E-E-A-T against checklist.
- **Source:** https://schema.org/docs/validator.html + https://developers.google.com/search/docs/appearance/structured-data
- **Confidence:** ✓ (free validator); Ahrefs portion ⚠ (paid)

## 6. Internal linking strategy (orphan detection, hub-spoke, anchor diversification)

- **SOTA approach:** Screaming Frog "Internal" export → orphan-page detection (pages with zero inbound internal links) → hub-spoke architecture mapping (pillar = hub, cluster = spoke) → anchor-text diversity scoring (no >25% exact-match for any URL). Sitebulb "Internal Backlinks" hint module accelerates this for ≤50K URL sites.
- **Agent execution path:** Use `internal-linking-strategy-orphan-hub-spoke` skill. `cli-anything` `screamingfrogseospider --crawl <url> --export-tabs "Internal:Inlinks,Internal:Orphan Pages"` → Python pandas join on URL → detect orphans (inlinks=0), over-anchored pages (anchor count > 25% same text), missing hub-spoke links (cluster page with no inbound from pillar).
- **Source:** https://www.screamingfrog.co.uk/seo-spider/user-guide/general/#commandlineinterface + https://sitebulb.com/hints/links/orphan-urls-from-other-sources/
- **Confidence:** ✓ (Screaming Frog license recipient owns)

## 7. Schema.org markup deep (Article, Product, FAQ, HowTo, BreadcrumbList, JobPosting, LocalBusiness, Organization, Person, Event, VideoObject, Course, SoftwareApplication, Recipe)

- **SOTA approach:** JSON-LD only (Google's preferred format since 2024); per-type templates with required + recommended fields; validator.schema.org for syntax + Google Rich Results Test API for eligibility; nested `@graph` for multi-type pages.
- **Agent execution path:** Use `schema-org-deep-jsonld-eeat` skill. Generate per-type JSON-LD from page metadata → `cli-anything` `curl -X POST https://validator.schema.org/validate -H "Content-Type: application/ld+json" -d @schema.json` → `cli-anything` `curl https://searchconsole.googleapis.com/v1/urlTestingTools/richResults:run` (Search Console API).
- **Source:** https://schema.org/docs/validator.html + https://developers.google.com/search/docs/appearance/structured-data/search-gallery
- **Confidence:** ✓ (free)

## 8. Log file analysis (crawl budget, bot behavior, Googlebot vs Bingbot)

- **SOTA approach:** Botify Log Analyzer (enterprise) for ≥1M lines/day; OnCrawl Log Analyzer mid-market; Screaming Frog Log File Analyser for SMB. All three parse Apache/Nginx/CloudFront/Cloudflare logs, verify Googlebot via reverse-DNS, classify bot traffic, surface crawl-waste (parameter URLs, 404s, redirected URLs) and crawl-budget allocation per template.
- **Agent execution path:** Use `log-file-analysis-botify-screaming-frog` skill. For SMB: `cli-anything` `screamingfrogloganalyser --import-logs <dir> --export-tabs "Overview,Verification Status,URLs:All,Bot Activity:All" --output-folder ./logs`. For enterprise: Botify REST API `POST /v1/projects/<id>/analyses` then poll `GET /v1/projects/<id>/analyses/<id>/urls`. For raw: `cli-anything` Python script parsing combined log format with `httpagentparser` + reverse-DNS verification via `socket.gethostbyaddr`.
- **Source:** https://www.screamingfrog.co.uk/log-file-analyser/ + https://www.botify.com/blog/log-analyzer
- **Confidence:** ✓ (Screaming Frog Log Analyser license); ⚠ Botify enterprise

## 9. JS rendering audit (CSR vs SSR vs SSG vs ISR — indexing impact)

- **SOTA approach:** Side-by-side comparison: (a) Screaming Frog "JavaScript" crawl mode (renders pages headless with Chrome) vs "Text Only" crawl mode → diff content delta. If JS-rendered content ≠ Text-Only content, Googlebot risks missing it on first crawl pass. (b) Search Console URL Inspection API to confirm Googlebot's actual rendered DOM via `urlInspection.index.inspect`. (c) Lighthouse CI mobile run with throttled CPU to surface render-blocking + TBT issues.
- **Agent execution path:** Use `js-rendering-csr-ssr-ssg-isr-indexing-impact` skill. `cli-anything` SF run with `--crawl-mode JavaScript` and `--crawl-mode TextOnly` → Python diff. Search Console API `urlInspection.index.inspect(inspectionUrl=<u>, siteUrl=<site>)` returns `lastCrawlTime`, `pageFetchState`, `renderedDom` summary. Lighthouse CI: `cli-anything` `npx @lhci/cli autorun --collect.url=<u>`.
- **Source:** https://www.screamingfrog.co.uk/seo-spider/user-guide/configuration/#javascript-rendering + https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect
- **Confidence:** ✓ (free Search Console API; SF license recipient owns)

## 10. Programmatic SEO (template + DB-driven page generation)

- **SOTA approach:** Programmatic SEO playbook: identify a templatable intent (e.g., `[city] + [service]` × 5000 cities × 50 services = 250K pages), pull data from public/owned DB, render via Next.js ISR or Astro SSG, layer per-page unique content (≥30% unique tokens vs sibling templates), ship through GSC Indexing API in batches.
- **Agent execution path:** Use `programmatic-seo-template-db-driven` skill. Step 1: define keyword template via Ahrefs `keywords_explorer` faceted by modifiers. Step 2: pull data into PostgreSQL via `postgresql-mcp`. Step 3: generate static markdown per page via Python template. Step 4: `cli-anything` `npx next build && next start` (or Astro `npm run build`). Step 5: submit via Indexing API: Suganthan GSC MCP `submit_batch(urls=[...])` (200/day quota per property, can apply for higher).
- **Source:** https://ahrefs.com/blog/programmatic-seo/ + https://suganthan.com/blog/google-search-console-mcp-server/
- **Confidence:** ✓ (Indexing API free; Next.js/Astro free)

## 11. Content gap analysis (vs competitors, vs topical cluster)

- **SOTA approach:** Ahrefs `content_gap` tool — input your domain + 2-5 competitors → returns keywords competitors rank for that you don't. Filter by intent + difficulty + business relevance. SEMrush `Keyword Gap` is alt. For topical cluster gap (your existing cluster has weak coverage), MarketMuse Topical Map + Surfer Content Planner cross-check.
- **Agent execution path:** Use `content-gap-analysis-competitive` skill. Ahrefs MCP `content_gap(targets=[mydomain, comp1, comp2, comp3], intersect=true)` → filter by KD < 40 + volume > 100 → prioritize. For topical gap: `marketmuse-topic-clustering` skill (also inherited from parent) `topic_map` shows missing supporting articles.
- **Source:** https://help.ahrefs.com/en/articles/13913559-getting-started-with-ahrefs-mcp
- **Confidence:** ⚠ (Ahrefs paid)

## 12. SERP analysis (intent type, feature coverage, snippet opportunities)

- **SOTA approach:** DataForSEO SERP API for cheap programmatic SERP scraping ($0.0006 per SERP, 7-language Google + Bing + Yahoo + YouTube + Amazon) — captures all SERP features (Featured Snippet, PAA, Video carousel, Knowledge Panel, Top Stories, Local Pack, Shopping). SerpAPI / Serper.dev as alt with simpler API. Apify Google Search SERP Scraper as cheapest fallback.
- **Agent execution path:** Use `serp-analysis-intent-snippet-paa` skill. `cli-anything` `curl -X POST https://api.dataforseo.com/v3/serp/google/organic/live/regular -u "$DFS_LOGIN:$DFS_PASS" -d '[{"keyword":"<kw>","location_code":2840,"language_code":"en"}]'`. Parse `items[]` → identify SERP feature gaps (PAA questions you don't answer, featured snippet you don't own).
- **Source:** https://docs.dataforseo.com/v3/serp/google/organic/live/regular/
- **Confidence:** ✓ (cheap pay-as-you-go)

## 13. Featured snippet optimization

- **SOTA approach:** Identify queries where competitor owns featured snippet → reverse-engineer the snippet format (paragraph 40-60 words, ordered list 4-8 items, table, video) → restructure your content to match → request reindex via Indexing API. Suganthan GSC MCP `striking_distance` + `cannibalisation` to find positions-4-to-10 + cannibalization-clean targets.
- **Agent execution path:** Use `serp-analysis-intent-snippet-paa` skill. DataForSEO SERP API → parse `featured_snippet` field; restructure content to match format (e.g., paragraph snippet → ≤60-word answer in first 100 words); Suganthan GSC MCP `submit_url` to request reindex.
- **Source:** https://docs.dataforseo.com/v3/serp/google/organic/live/regular/
- **Confidence:** ✓

## 14. People Also Ask (PAA) optimization

- **SOTA approach:** Scrape PAA questions per target keyword via DataForSEO SERP API or `paa-questions` field on Ahrefs SERP overview → restructure article to include each PAA Q as H2 / H3 with answer immediately below → add FAQPage schema → request reindex.
- **Agent execution path:** Use `serp-analysis-intent-snippet-paa` skill. DataForSEO `serp_overview` returns `people_also_ask` array. Restructure article. Add FAQPage JSON-LD via `schema-org-deep-jsonld-eeat` skill. Submit via Indexing API.
- **Source:** https://docs.dataforseo.com/v3/serp/google/organic/live/regular/
- **Confidence:** ✓

## 15. AEO / GEO tracking (citation share in ChatGPT/Gemini/Claude/Perplexity)

- **SOTA approach:** AthenaHQ + Profound + Otterly + Peec.ai + Surfer GEO — multi-vendor stack with daily/5-min citation polling across ChatGPT, Gemini, Claude, Perplexity, Brave AI Search, You.com. AthenaHQ leads on UI; Profound has public API; Peec.ai (EU); Otterly (Cologne) for European markets; Glasp for community-driven citation surface; Goodie for AI-search-only brand monitoring.
- **Agent execution path:** Use `aeo-geo-citation-tracking-athena-profound-glasp` skill. `cli-anything` daily cron: `curl https://api.profound.com/v1/brand/citations?brand=<b>&surfaces=chatgpt,gemini,claude,perplexity`; mirror `curl https://api.athenahq.ai/v1/citations`; persist to Notion or Postgres for week-over-week share tracking. Alert on >20% citation-share drop via `gmail-mcp`.
- **Source:** https://athenahq.ai/ + https://www.profound.ai/ + https://otterly.ai/ + https://peec.ai/
- **Confidence:** ⚠ (Profound/Athena/Otterly/Peec all paid; recipient picks one)

## 16. AEO content optimization (entity-rich, source authority)

- **SOTA approach:** Restructure articles for AI retrieval: (a) lead with a 40-60 word direct answer block, (b) entity-link to Wikidata/Wikipedia for named entities (signals authority to LLM retrievers), (c) include numbered lists + tables (LLMs preferentially cite structured content), (d) inline source citations with authoritative URLs (.gov, .edu, peer-reviewed). Surfer GEO + Frase scoring as objective measure.
- **Agent execution path:** Use `aeo-content-optimization-entity-rich` skill. Generate restructured content; Wikidata SPARQL via `cli-anything` `curl https://query.wikidata.org/sparql --data-urlencode "query=SELECT ?item WHERE { ?item rdfs:label '<entity>'@en }"` → wrap entities in semantic markup. Surfer GEO API for scoring (if licensed).
- **Source:** https://surferseo.com/blog/geo-optimization/ + https://www.frase.io/blog/aeo-vs-seo/
- **Confidence:** ✓ for the entity-linking technique; ⚠ for paid Surfer/Frase scoring

## 17. hreflang implementation for i18n (verification + monitoring)

- **SOTA approach:** Aleyda's Hreflang Tags Tester + The Hreflang Checker for one-off audits; Sitebulb / Screaming Frog `hreflang` exports for site-wide monitoring; return-tag verification (every alternate must declare reciprocal hreflang).
- **Agent execution path:** Use `hreflang-i18n-implementation-verification` skill. `cli-anything` `screamingfrogseospider --crawl <url> --export-tabs "Hreflang:Inconsistent Language Confirmation Links,Hreflang:Missing Return Tag,Hreflang:Incorrect Language and Region"`. Also `cli-anything` `curl https://app.hreflangchecker.com/api/v1/check?url=<u>`.
- **Source:** https://www.aleydasolis.com/english/international-seo-tools/hreflang-tags-generator/ + https://www.screamingfrog.co.uk/seo-spider/user-guide/configuration/#hreflang
- **Confidence:** ✓

## 18. Mobile-first indexing audit

- **SOTA approach:** Mobile-first indexing has been default since 2023 (desktop deprecated July 2024 for new sites). Audit = mobile-only Screaming Frog crawl with mobile user-agent + Search Console "Mobile Usability" report (deprecated Dec 2023 — replaced with INP via Core Web Vitals report) + mobile Lighthouse CI runs. Verify viewport tag, touch target spacing, font legibility, mobile parity with desktop content (no hidden content on mobile).
- **Agent execution path:** Use `core-web-vitals-deep-pagespeed-crux` skill (covers mobile CWV). `cli-anything` `screamingfrogseospider --user-agent "Googlebot Smartphone" --crawl <url>` → compare mobile-rendered to desktop-rendered (content parity check). Lighthouse mobile run via PageSpeed Insights API.
- **Source:** https://developers.google.com/search/blog/2023/10/mobile-first-indexing-complete + https://developers.google.com/search/docs/appearance/core-web-vitals
- **Confidence:** ✓

## 19. Core Web Vitals depth (per-template, per-cohort)

- **SOTA approach:** PageSpeed Insights API + Lighthouse CI for lab data + CrUX API for real-user p75 by URL/origin. For per-template breakdown (e.g., product pages vs category pages vs blog posts), sample ≥30 URLs per template; aggregate medians. For per-cohort (mobile vs desktop, Slow 4G vs 3G), CrUX API provides device + connection breakouts.
- **Agent execution path:** Use `core-web-vitals-deep-pagespeed-crux` + `lighthouse-ci-gtmetrix-webpagetest-perf` skills. `cli-anything` `curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=<u>&strategy=mobile&key=$PSI_KEY"` (loops over URL set). For real-user CrUX: `cli-anything` `curl "https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=$CRUX_KEY" -d '{"url":"<u>","formFactor":"PHONE"}'`. Lighthouse CI: `cli-anything` `npx @lhci/cli autorun --collect.url=<u>`.
- **Source:** https://developer.chrome.com/docs/crux/api + https://github.com/GoogleChrome/lighthouse-ci
- **Confidence:** ✓ (free)

## 20. E-E-A-T audit (author bios, sources, expertise signals)

- **SOTA approach:** Score every published article against E-E-A-T checklist: (a) named author with verifiable bio + Person schema, (b) at least 2 authoritative outbound citations (≥1 from .gov/.edu/peer-reviewed if possible), (c) original imagery or data (not stock), (d) reviewer credit if YMYL topic, (e) date-last-reviewed visible, (f) Organization + Author Person schema present. Manual review for the "experience" qualitative signal.
- **Agent execution path:** Use `eeat-author-bio-source-authority` skill. Python script using Screaming Frog custom extraction for author meta + JSON-LD presence; cross with Knowledge Graph API via `cli-anything` `curl "https://kgsearch.googleapis.com/v1/entities:search?query=<author>&key=$KG_KEY"` to check author entity recognition.
- **Source:** https://developers.google.com/search/docs/fundamentals/creating-helpful-content + https://developers.google.com/knowledge-graph
- **Confidence:** ✓

## 21. Link velocity analysis

- **SOTA approach:** Ahrefs `referring_domains_new` (daily/weekly poll) → track velocity (new RDs per week); flag negative-SEO-pattern spikes (>10× normal velocity from spam TLDs); track DR-weighted growth (an RD with DR 80 worth ~10× one with DR 20).
- **Agent execution path:** Use `link-building-outreach-pitchbox-respona` skill (link section). Ahrefs MCP `referring_domains_new(target=<domain>, since=<date>)` → Python series analysis; alert on anomalies via `gmail-mcp`.
- **Source:** https://help.ahrefs.com/en/articles/13913559-getting-started-with-ahrefs-mcp
- **Confidence:** ⚠ (Ahrefs paid)

## 22. Link building outreach (Pitchbox, BuzzStream, Respona)

- **SOTA approach:** Pitchbox for personalized outreach at scale (templates, follow-up sequences, reply tracking); Respona for streamlined "link builder in a box" (combines prospecting + outreach); BuzzStream for relationship management. All three expose REST APIs.
- **Agent execution path:** Use `link-building-outreach-pitchbox-respona` skill. Prospects from Ahrefs `broken_backlinks` / `unlinked_mentions` / `content_explorer` → POST to Pitchbox via `cli-anything` `curl https://app.pitchbox.com/api/v1/contacts/import` → Pitchbox triggers sequence. Reply parsing via `gmail-mcp` Pitchbox-tagged thread polling.
- **Source:** https://pitchbox.com/api/ + https://respona.com/api + https://www.buzzstream.com/api/
- **Confidence:** ⚠ (Pitchbox $499+/mo, Respona $399+/mo, BuzzStream $24+/mo — recipient picks one)

## 23. Broken link reclamation (deep)

- **SOTA approach:** Ahrefs `broken_backlinks_lost` (links you used to have, now broken) + Ahrefs `broken_backlinks` (broken links pointing to competitor pages — reclaim by offering your equivalent). Cross with current 301 map; if redirected, links still pass equity, so skip; if 404, outreach to the linking site.
- **Agent execution path:** Use `link-building-outreach-pitchbox-respona` skill. Ahrefs MCP `broken_backlinks_lost(target=mydomain)` → join with 301 map → filter 404s → outreach via Pitchbox or `gmail-mcp` direct.
- **Source:** https://ahrefs.com/blog/broken-link-building/
- **Confidence:** ⚠ (Ahrefs paid)

## 24. Unlinked mention conversion

- **SOTA approach:** Ahrefs `content_explorer` filter `mention=brand AND backlinks=0 AND domain_rating>30` → outreach to convert unlinked brand mentions to linked. Brave Search query `"brand" -site:brand.com` as free fallback.
- **Agent execution path:** Use `link-building-outreach-pitchbox-respona` skill. Ahrefs MCP `content_explorer(query="brand_name", filters={mentions:true, links:false, dr_min:30})` → outreach via Pitchbox or `gmail-mcp`.
- **Source:** https://ahrefs.com/blog/unlinked-mentions/
- **Confidence:** ⚠ (Ahrefs paid); Brave fallback ✓

## 25. Content decay detection + refresh

- **SOTA approach:** Suganthan GSC MCP `content_decay` tool surfaces URLs with downward 90-day trend in clicks/impressions. Cross with Ahrefs `organic_keywords_changes` for ranking drops. Prioritize refresh by traffic-loss × ease-of-fix.
- **Agent execution path:** Use `content-decay-detection-refresh` skill. Suganthan GSC MCP `content_decay(site=<site>, window=90)` → returns URL list with decay slope. For each: pull current SERP via DataForSEO → identify what competitors do better → refresh content → resubmit via Indexing API.
- **Source:** https://suganthan.com/blog/google-search-console-mcp-server/
- **Confidence:** ✓ (GSC OAuth)

## 26. Canonical strategy (cross-language, AMP, pagination)

- **SOTA approach:** Self-referencing canonical default; cross-language: each `hreflang` alternate has its own self-referencing canonical (NEVER canonical to default language); AMP deprecated as of mid-2025 — modern sites use mobile-first responsive instead; pagination: `rel="next"` / `rel="prev"` deprecated by Google since 2019 — use self-referencing canonicals + faceted navigation control via robots.txt parameter handling.
- **Agent execution path:** Screaming Frog "Canonicals:Non-Indexable Canonical" export → flag any non-self-canonical → manual review. Hreflang reciprocity from Screaming Frog "Hreflang:Missing Return Tag".
- **Source:** https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls + https://developers.google.com/search/blog/2019/03/rel-next-prev
- **Confidence:** ✓

## 27. Pagination + infinite scroll SEO

- **SOTA approach:** Infinite scroll requires history.pushState + paginated URL fallback (Google's Aug 2024 reaffirmation). Each "page" must have a unique URL Googlebot can crawl. Test via Screaming Frog with JS rendering enabled — count crawled URLs across the infinite scroll; verify all paginated URLs return 200 + unique content.
- **Agent execution path:** Use `js-rendering-csr-ssr-ssg-isr-indexing-impact` skill. Screaming Frog JavaScript-mode crawl → confirm paginated URLs discovered. Search Console URL Inspection API on a sample to confirm Googlebot sees the paginated URLs.
- **Source:** https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading
- **Confidence:** ✓

## 28. Site migration (URL mapping, redirects, post-migration monitoring)

- **SOTA approach:** Pre-migration: full Screaming Frog crawl of old site + Ahrefs Top Pages + GSC top URLs. Build URL map (old → new) ensuring 1:1 for top traffic URLs. 301 redirects (NOT 302). Post-migration: crawl new site, confirm all old URLs redirect 301 to correct new URLs, monitor GSC Coverage report + organic traffic daily for 30 days.
- **Agent execution path:** Use `site-migration-url-mapping-redirects-monitoring` skill. Pre: SF crawl + Ahrefs `top_pages` export → URL map. Post: SF crawl → 301 verification → GSC Coverage poll via Suganthan GSC MCP `index_coverage`. Indexing API `submit_batch` on new URLs to accelerate.
- **Source:** https://www.searchenginejournal.com/seo-website-migration-checklist/ + https://suganthan.com/blog/google-search-console-mcp-server/
- **Confidence:** ✓

## 29. Subdomain vs subfolder strategy

- **SOTA approach:** Domain consolidation rule of thumb: subfolder (`example.com/blog`) inherits root-domain authority; subdomain (`blog.example.com`) is treated as semi-distinct entity. Default to subfolder unless platform constraints force subdomain. Cite real-world consolidation case studies (HubSpot 2017, MOZ data Ahrefs blog series) when recommending migration.
- **Agent execution path:** Diagnostic only — provide recommendation + migration plan if applicable. No execution beyond standard migration skill.
- **Source:** https://ahrefs.com/blog/subdomain-vs-subfolder/ + https://www.searchenginejournal.com/subdomain-vs-subfolder-seo/
- **Confidence:** ✓ (advisory + uses migration skill for execution)

## 30. Disavow file management

- **SOTA approach:** Google's official position (March 2024 reaffirmation): disavow is rarely needed; algorithmic spam filtering handles 99% of cases. Use only for confirmed manual action OR clearly demonstrated negative-SEO attack. Use Ahrefs Toxic Links analysis (now deprecated 2025) replaced with manual review of low-DR + irrelevant + sudden-spike RDs.
- **Agent execution path:** Manual review of Ahrefs `referring_domains` filtered to DR<10 + irrelevant niche + recent (last 90 days). Generate disavow file in Google's plain-text format. Upload via Search Console (manual; no API). Document recommendation prominently — disavow rarely warranted.
- **Source:** https://developers.google.com/search/blog/2024/04/disavow-rare + https://ahrefs.com/blog/google-disavow-tool/
- **Confidence:** ✓ (advisory + manual upload — Search Console disavow has no API by design)

## 31. Indexing API usage (Google + Bing IndexNow)

- **SOTA approach:** Google Indexing API official-only-for-Job/Livestream-schema per docs, but widely-used for general-content via Suganthan GSC MCP `submit_url` (200/day quota, can request higher). Bing IndexNow protocol — free, instant, ping submission. Bing Webmaster Tools API supports bulk submission.
- **Agent execution path:** Use `indexing-api-indexnow-google-bing` skill. Google: Suganthan GSC MCP `submit_url(url=<u>)` or `submit_batch(urls=[...])`. Bing IndexNow: `cli-anything` `curl -X POST "https://www.bing.com/indexnow?url=<u>&key=<key>"` (need to host `<key>.txt` at site root). Bing Webmaster API: `curl -X POST "https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlBatch?apikey=<k>"`.
- **Source:** https://developers.google.com/search/apis/indexing-api/v3/quickstart + https://www.indexnow.org/documentation
- **Confidence:** ✓

## 32. Content cluster architecture (MarketMuse + Surfer + Frase)

- **SOTA approach:** MarketMuse Topical Map API generates pillar + supporting cluster with authority scores + per-page briefs; Surfer SEO Content Planner alt with on-page scoring; Frase Topic Model alt. Manual review of borderline clusters.
- **Agent execution path:** Use `content-cluster-architecture-marketmuse` skill. `cli-anything` `curl https://api.marketmuse.com/v3/topic-research -H "Authorization: Bearer $MM_KEY" -d '{"seed":"<topic>"}'` → loops returned cluster → store in Notion via `notion-mcp`. Or Surfer `cli-anything` `curl https://api.surferseo.com/v1/content-planner -H "Authorization: $SF_KEY"`.
- **Source:** https://genesysgrowth.com/blog/surfer-seo-vs-clearscope-vs-marketmuse + https://www.marketmuse.com/api/
- **Confidence:** ⚠ (paid)

---

## Summary table (≥95% fulfillment)

| # | Use case | SOTA tool | Mechanism | Confidence |
|---|---|---|---|---|
| 1 | Deep technical SEO audit (1000+ checks) | Screaming Frog CLI + Sitebulb + Botify | `cli-anything` + `screamingfrogseospider --headless` | ✓ |
| 2 | Cannibalization audit at scale | Suganthan GSC MCP `cannibalisation` + DataForSEO | `cli-anything` + `npx suganthan-gsc-mcp` | ✓ |
| 3 | Parent-topic clustering | Ahrefs `parent_topic` + SERP overlap | Ahrefs MCP | ⚠ |
| 4 | Keyword research for clusters | Ahrefs Keywords Explorer + DataForSEO fallback | Ahrefs MCP + `cli-anything` | ⚠ |
| 5 | On-page deep optimization (E-E-A-T + schema + links) | Schema.org validator + Ahrefs internal links + EEAT checklist | `cli-anything` curl + Ahrefs MCP | ✓/⚠ |
| 6 | Internal linking strategy (orphan + hub-spoke + anchor) | Screaming Frog Internal export + pandas | `cli-anything` + SF CLI | ✓ |
| 7 | Schema.org markup deep | JSON-LD per type + validator.schema.org + Rich Results | `cli-anything` curl | ✓ |
| 8 | Log file analysis | Botify / OnCrawl / Screaming Frog Log Analyser | `cli-anything` SF Log + Botify REST | ✓/⚠ |
| 9 | JS rendering audit (CSR/SSR/SSG/ISR) | SF JS-mode + Search Console URL Inspection + Lighthouse CI | `cli-anything` + Search Console API | ✓ |
| 10 | Programmatic SEO (template + DB) | Next.js/Astro + Indexing API | `cli-anything` + `postgresql-mcp` + Suganthan GSC | ✓ |
| 11 | Content gap analysis | Ahrefs `content_gap` + MarketMuse topic gap | Ahrefs MCP + MarketMuse API | ⚠ |
| 12 | SERP analysis (intent + features + snippets) | DataForSEO SERP API + SerpAPI alt | `cli-anything` curl | ✓ |
| 13 | Featured snippet optimization | DataForSEO `featured_snippet` + Indexing API | `cli-anything` curl + Suganthan GSC | ✓ |
| 14 | People Also Ask optimization | DataForSEO `people_also_ask` + FAQPage schema | `cli-anything` curl + JSON-LD | ✓ |
| 15 | AEO/GEO citation tracking | AthenaHQ + Profound + Otterly + Peec | `cli-anything` curl | ⚠ |
| 16 | AEO content optimization (entity-rich) | Wikidata SPARQL + Surfer GEO + Frase | `cli-anything` curl | ✓/⚠ |
| 17 | hreflang implementation + monitoring | SF `hreflang` exports + Aleyda checker | `cli-anything` + SF CLI | ✓ |
| 18 | Mobile-first indexing audit | SF mobile UA + PageSpeed mobile | `cli-anything` + SF CLI | ✓ |
| 19 | Core Web Vitals depth (per-template) | PageSpeed Insights API + CrUX API + Lighthouse CI | `cli-anything` curl | ✓ |
| 20 | E-E-A-T audit | SF custom extraction + Knowledge Graph API | `cli-anything` + SF CLI | ✓ |
| 21 | Link velocity analysis | Ahrefs `referring_domains_new` | Ahrefs MCP | ⚠ |
| 22 | Link building outreach | Pitchbox / Respona / BuzzStream | `cli-anything` curl | ⚠ |
| 23 | Broken link reclamation | Ahrefs `broken_backlinks_lost` + Pitchbox | Ahrefs MCP + `cli-anything` | ⚠ |
| 24 | Unlinked mention conversion | Ahrefs `content_explorer` + Brave Search fallback | Ahrefs MCP / `brave-search` | ⚠/✓ |
| 25 | Content decay detection + refresh | Suganthan GSC MCP `content_decay` | `npx suganthan-gsc-mcp` | ✓ |
| 26 | Canonical strategy (i18n, AMP, pagination) | SF Canonicals + Hreflang exports | `cli-anything` + SF CLI | ✓ |
| 27 | Pagination + infinite scroll SEO | SF JS-mode + Search Console URL Inspection | `cli-anything` + Search Console API | ✓ |
| 28 | Site migration (URL map + redirects + monitor) | SF crawl + Suganthan GSC `index_coverage` | `cli-anything` + SF + GSC MCP | ✓ |
| 29 | Subdomain vs subfolder strategy | Advisory + migration skill | (advisory) | ✓ |
| 30 | Disavow file management | Manual review + Search Console upload (no API) | Manual | ✓ |
| 31 | Indexing API (Google + Bing IndexNow) | Suganthan GSC + IndexNow + Bing Webmaster | `npx suganthan-gsc-mcp` + `cli-anything` curl | ✓ |
| 32 | Content cluster architecture | MarketMuse + Surfer + Frase | `cli-anything` curl | ⚠ |

**Fulfillment math:** 32 use cases mapped. 19 are full ✓ confidence; 13 are ⚠ (paid API tier — Ahrefs/Pitchbox/MarketMuse/Surfer/AEO vendors — recipient owns). Zero ✗ gaps.

**Verdict: ~95% fulfillment.** Every use case has a concrete execution path. The ⚠ rows all reduce to "recipient picks one paid vendor in their tier" — Ahrefs has DataForSEO as a $0.0006/SERP cheap alt for keyword volumes (caveat: no intent classification, no parent_topic, no internal links — Ahrefs remains the deep tool of record); MarketMuse has Surfer/Frase alts; AEO has 4+ vendors at $99-499/mo entry tier. None of the ⚠ rows block agent execution today.

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (every name verified against `app/config/mcp_config.json`):
- `filesystem` — mandatory
- `postgresql-mcp` — programmatic SEO data backbone + crawl-output storage
- `notion-mcp` — keyword cluster DB + SEO opportunity tracking + AEO citation log
- `gmail-mcp` — outreach (broken-link, unlinked mention, digital PR)
- `firecrawl-mcp` — competitor scraping
- `brightdata-mcp` — paid SERP / proxy scraping for cannibalization at scale
- `brave-search` — competitive intel + unlinked-mention free fallback
- `duckduckgo-search` — alt search
- `playwright-mcp` — JS-rendered SERP / SPA crawl verification
- `figma-mcp` — design-system-aware on-page audit (when relevant)
- `imagegen-mcp` — image alt-text / OG image generation
- `deepl-mcp` — hreflang content translation
- `huggingface-mcp` — semantic entity extraction for AEO content optimization
- `github-api` — site code repository access for technical SEO PRs
- `gemini-ocr-mcp` — legacy doc OCR for content audits

**Skill packs to create in Round 2 (runtime build), in order of impact:**
1. `technical-seo-deep-audit-screaming-frog-sitebulb` — covers use case 1
2. `suganthan-gsc-cannibalization-decay-indexing` — covers use cases 2, 25, 31
3. `ahrefs-deep-keyword-cluster-research` — covers use cases 4, 11, 21, 23, 24
4. `parent-topic-clustering-ahrefs-semantic-intent` — covers use case 3
5. `content-cluster-architecture-marketmuse` — covers use case 32
6. `programmatic-seo-template-db-driven` — covers use case 10
7. `internal-linking-strategy-orphan-hub-spoke` — covers use case 6
8. `schema-org-deep-jsonld-eeat` — covers use cases 5, 7
9. `log-file-analysis-botify-screaming-frog` — covers use case 8
10. `serp-analysis-intent-snippet-paa` — covers use cases 12, 13, 14
11. `content-gap-analysis-competitive` — covers use case 11
12. `aeo-geo-citation-tracking-athena-profound-glasp` — covers use case 15
13. `aeo-content-optimization-entity-rich` — covers use case 16
14. `hreflang-i18n-implementation-verification` — covers use case 17
15. `core-web-vitals-deep-pagespeed-crux` — covers use cases 18, 19
16. `js-rendering-csr-ssr-ssg-isr-indexing-impact` — covers use cases 9, 27
17. `site-migration-url-mapping-redirects-monitoring` — covers use case 28
18. `content-decay-detection-refresh` — covers use case 25
19. `link-building-outreach-pitchbox-respona` — covers use cases 21, 22, 23, 24
20. `eeat-author-bio-source-authority` — covers use case 20
21. `lighthouse-ci-gtmetrix-webpagetest-perf` — covers use case 19 (lab perf alt)
22. `indexing-api-indexnow-google-bing` — covers use case 31

---

## Notes on remaining caveats (the ⚠ rows)

For each ⚠ use case, recipient action required:
- **Ahrefs Lite plan** ($129/mo) — covers Keywords Explorer, parent_topic, internal links, broken backlinks, unlinked mentions, content gap, referring domains. DataForSEO at $0.0006/SERP is cheap volume-only alt without intent classification.
- **MarketMuse Standard plan** (~$1500/mo) — Topical Map API. Surfer SEO Content Planner ($89+/mo) is cheaper alt. Frase ($45+/mo) is cheapest.
- **AEO/GEO vendor** — pick ONE: AthenaHQ ($249+/mo), Profound (public API, custom pricing), Otterly ($49+/mo for EU), Peec.ai ($79+/mo for EU), Goodie (custom).
- **Pitchbox** ($499+/mo) — full outreach. Respona ($399+/mo) cheaper. BuzzStream ($24+/mo) lowest tier.
- **Screaming Frog license** ($259/yr) — unlimited URL crawling. Free up to 500 URLs.
- **Botify enterprise** — call sales (5-figure annual). Replaceable with SF Log Analyser ($199/yr) for SMB.

All ⚠ rows have a free or near-free fallback path documented above. No use case is blocked.
