<!--
Source: https://www.screamingfrog.co.uk/seo-spider/user-guide/general/#commandlineinterface
Source: https://sitebulb.com/resources/guides/how-to-use-the-sitebulb-cli/
Source: https://www.botify.com/blog/log-analyzer
Depth: 1000+ check deep technical SEO audit beyond marketing-agent's surface coverage
-->
# Technical SEO Deep Audit — Screaming Frog + Sitebulb + Botify

## When to use

Reach for this skill when the user asks for: "full technical SEO audit", "deep crawl", "1000+ check audit", "Screaming Frog crawl", "Sitebulb hint audit", "comprehensive site audit", "find every technical issue", or hands you a domain and says "audit it". This is the deep-technical sibling of marketing-agent's surface SEO scan — go to ≥250 SF checks plus Sitebulb hint prioritization plus optional Botify enterprise overlay. **NEVER** run this skill before completing the cannibalization audit (`suganthan-gsc-cannibalization-decay-indexing`) — that audit blocks all other recommendations.

## Setup

```bash
# Screaming Frog SEO Spider — primary deep-crawl engine
# Download from screamingfrog.co.uk; free up to 500 URLs; $259/yr unlimited
# Windows install path: "C:\Program Files (x86)\Screaming Frog SEO Spider\ScreamingFrogSEOSpiderCli.exe"
# macOS: /Applications/Screaming\ Frog\ SEO\ Spider.app/Contents/MacOS/ScreamingFrogSEOSpiderLauncher
screamingfrogseospider --help

# Sitebulb — hint engine for prioritization (CLI requires Sitebulb Server license)
# $13.50+/mo Desktop; CLI requires Server plan ($35+/mo). Download from sitebulb.com
sitebulb --help

# Botify (enterprise) — REST API, no CLI; auth via API key
# Apply for trial at botify.com/contact; production tier is 5-figure annual
export BOTIFY_API_KEY="<paste-key>"
```

Auth / license requirements:
- `SF_LICENSE_KEY` — Screaming Frog license string in `~/.ScreamingFrogSEOSpider/spider.config` (free tier capped at 500 URLs)
- `SITEBULB_LICENSE` — Server-tier license file in `~/.sitebulb/`
- `BOTIFY_API_KEY` — required for enterprise log + crawl-stats overlay

## Common recipes

### Recipe 1: Comprehensive SF headless crawl with all key tabs exported
```bash
screamingfrogseospider \
  --crawl https://example.com \
  --headless \
  --save-crawl \
  --export-tabs "Internal:All,Internal:HTML,Response Codes:Client Error (4xx),Response Codes:Server Error (5xx),Response Codes:Redirection (3xx),Page Titles:Duplicate,Page Titles:Missing,Page Titles:Over 60 Characters,Meta Description:Duplicate,Meta Description:Missing,H1:Duplicate,H1:Missing,H1:Multiple,Canonicals:Self Referencing,Canonicals:Non-Indexable Canonical,Canonicals:Missing,Directives:Noindex,Directives:Nofollow,Hreflang:All,Hreflang:Missing Return Tag,Hreflang:Inconsistent Language Confirmation Links,Hreflang:Incorrect Language and Region,Structured Data:All,Structured Data:Validation Errors,Structured Data:Validation Warnings,Images:Missing Alt Text,Images:Over 100KB,Pagination:All,AMP:All" \
  --output-folder ./crawl-out \
  --timestamped-output
```
The `--export-tabs` list above covers the SF 2026 default 250+ check surface. `--headless` runs without GUI; `--save-crawl` writes the `.seospider` binary for later inspection in GUI.

### Recipe 2: JavaScript-render crawl (for SPA / CSR sites)
```bash
screamingfrogseospider \
  --crawl https://spa-site.com \
  --crawl-mode JavaScript \
  --headless \
  --max-threads 5 \
  --user-agent "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36" \
  --export-tabs "Internal:All,JavaScript:All,JavaScript:Pages with Blocked Resources,JavaScript:Contains JavaScript Content" \
  --output-folder ./js-crawl \
  --timestamped-output
```
JS-mode uses headless Chrome — slower (1-3s/URL vs 0.05s text-only) but renders client-side content. Limit threads (5-10) to avoid OOM on large crawls.

### Recipe 3: Mobile-first audit with Googlebot Smartphone UA
```bash
screamingfrogseospider \
  --crawl https://example.com \
  --headless \
  --user-agent "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" \
  --device "Mobile" \
  --export-tabs "Internal:All,Mobile:All,Mobile:Viewport Issues,Mobile:Touch Element Issues" \
  --output-folder ./mobile-crawl
```
Mobile-first indexing has been default since 2023 — desktop is deprecated for new sites since July 2024.

### Recipe 4: Custom XPath extraction (e.g., grab author meta on blog posts)
```bash
# Write extraction config to ~/.ScreamingFrogSEOSpider/custom_extraction.txt
cat > /tmp/sf-extract.txt <<EOF
Author Name|//meta[@name='author']/@content|XPath
Published Date|//time[@itemprop='datePublished']/@datetime|XPath
JSON-LD|//script[@type='application/ld+json']/text()|XPath
EOF

screamingfrogseospider \
  --crawl https://example.com/blog \
  --headless \
  --use-custom-extraction /tmp/sf-extract.txt \
  --export-tabs "Internal:All,Custom Extraction:All" \
  --output-folder ./custom-extract
```
XPath / CSS / regex extractors handle any markup pattern SF doesn't audit by default.

### Recipe 5: Sitebulb hint-prioritized audit (≤50K URL sites)
```bash
sitebulb crawl \
  --url https://example.com \
  --project "client-q3-audit" \
  --crawl-speed 5 \
  --max-urls 50000 \
  --enable-javascript true \
  --hints "all" \
  --export-format csv \
  --output ./sitebulb-out
```
Sitebulb's "hint engine" ranks ~300 hints by impact × ease automatically (saves manual triage time). Best when you need an executive priority list, not a raw dump.

### Recipe 6: Botify enterprise log + crawl overlay
```bash
# Trigger a Botify analysis
curl -X POST https://api.botify.com/v1/projects/<project-slug>/analyses/launch \
  -H "Authorization: Token $BOTIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"area":"current","name":"q3-audit","comment":"deep audit + log overlay"}'

# Poll analysis status
curl https://api.botify.com/v1/projects/<project-slug>/analyses/<analysis-slug> \
  -H "Authorization: Token $BOTIFY_API_KEY"

# Pull URL-level data once status=DONE
curl "https://api.botify.com/v1/projects/<project-slug>/analyses/<analysis-slug>/urls?size=10000&fields=url,http_code,canonical.is_self,inlinks_internal.nb.total,outlinks_internal.nb.total,segments.pagetype.value,strategic.is_strategic,visits.organic.google.nb,crawls.google.has_been_crawled" \
  -H "Authorization: Token $BOTIFY_API_KEY"
```
Botify joins Googlebot log entries with crawl + GSC + analytics — only Botify (and OnCrawl mid-market) does this single-pane.

### Recipe 7: Scheduled SF crawl for change monitoring
```bash
# Save crawl config + schedule via SF GUI first (File > Scheduling), then CLI variant:
screamingfrogseospider \
  --crawl-config ~/saved-configs/monitor.seospiderconfig \
  --crawl https://example.com \
  --headless \
  --save-crawl \
  --schedule "0 2 * * *" \
  --output-folder ./monitor-out
```
Detects new noindex tags, new 404s, new schema errors day-over-day.

### Recipe 8: Robots.txt + sitemap audit
```bash
# Robots.txt fetch + parse
curl https://example.com/robots.txt -o /tmp/robots.txt
python3 -c "import urllib.robotparser; rp=urllib.robotparser.RobotFileParser(); rp.set_url('https://example.com/robots.txt'); rp.read(); print('Disallowed:', [r for r in rp.entries])"

# Sitemap fetch + URL count + indexed-coverage gap
curl https://example.com/sitemap.xml -o /tmp/sitemap.xml
xmllint --xpath "count(//*[local-name()='url'])" /tmp/sitemap.xml
# Compare against GSC `index_coverage` via Suganthan GSC MCP for coverage ratio
```

### Recipe 9: Load SF CSV into pandas for cross-tab analysis
```python
import pandas as pd

internal = pd.read_csv('./crawl-out/internal_all.csv')
canonicals = pd.read_csv('./crawl-out/canonicals_non_indexable_canonical.csv')
hreflang = pd.read_csv('./crawl-out/hreflang_missing_return_tag.csv')

# Cross-issue join — find URLs with multiple problems
problem_urls = internal.merge(canonicals, on='Address', how='inner').merge(
    hreflang, on='Address', how='inner'
)
print(f"URLs with canonical+hreflang issues: {len(problem_urls)}")
```

## Examples

### Example 1: Full deep audit for a 25K-URL e-commerce site
**Goal:** Deliver a prioritized audit report covering crawlability, on-page, schema, hreflang, mobile.

**Steps:**
1. Run cannibalization audit FIRST — `suganthan-gsc-cannibalization-decay-indexing` skill blocks until done.
2. SF deep crawl (Recipe 1) — overnight headless. Export tabs land in `./crawl-out/`.
3. SF JS-mode crawl (Recipe 2) on `/products/*` subset (sample 500 URLs via `--include /products/.*`).
4. SF mobile-UA crawl (Recipe 3) — content parity check against desktop crawl.
5. Sitebulb hint-prioritized audit (Recipe 5) — get the impact-ranked hint list.
6. Pandas cross-join (Recipe 9) — URLs failing ≥3 SF checks rise to "critical".
7. Generate audit report via `docx` skill using template in `role.md` "Audit report template" section.

**Result:** A `.docx` audit report with executive summary, prioritized issues, per-category findings, and CSV appendix exports.

### Example 2: JS-rendering verification for a Next.js SPA migrating to SSG
**Goal:** Confirm content delta between JS-render and text-only — flag SPA content invisible to Googlebot.

**Steps:**
1. `screamingfrogseospider --crawl https://app.example.com --crawl-mode JavaScript --headless --export-tabs "Internal:All" --output-folder ./js`
2. `screamingfrogseospider --crawl https://app.example.com --crawl-mode TextOnly --headless --export-tabs "Internal:All" --output-folder ./txt`
3. Diff word counts per URL via pandas: `js_df.merge(txt_df, on='Address')[['Word Count_x','Word Count_y']]` — URLs where JS WC ≫ Text WC are at-risk.
4. Cross-verify with Search Console URL Inspection (`js-rendering-csr-ssr-ssg-isr-indexing-impact` skill).

**Result:** URL-level table of at-risk content; hand off to `frontend-engineer` for SSR/SSG remediation.

## Edge cases / gotchas

- **OOM on large crawls** — SF default heap is 2GB. Edit `~/.ScreamingFrogSEOSpider/spider.config` `-Xmx16g` before crawling 500K+ URL sites. JS-mode at 100K URLs needs ≥32GB RAM.
- **JS-mode rate limiting** — sites with WAF (Cloudflare, Akamai) will 429-block aggressive JS crawls. Drop `--max-threads` to 2 and add `--crawl-delay 1000` (ms).
- **License-bound URL caps** — free tier hard-stops at 500 URLs. Paid license file lives in spider config; CLI silently truncates if not present.
- **Sitebulb CLI requires Server plan** — Desktop license alone can't run CLI. If recipient only has Desktop, fall back to SF.
- **Custom extraction silently fails** — bad XPath returns empty cells, not errors. Always test config in SF GUI before scheduling.
- **Botify "current" area** — `--area current` analyzes live; `--area archived` re-analyzes a past crawl. Pass `current` for fresh audits.
- **Headless mode requires display in some Linux** — Ubuntu 22.04+ needs `xvfb-run screamingfrogseospider --headless ...` for some configs. macOS / Windows headless works natively.
- **Hreflang exports use SF's own validation** — for hreflang-checker.com / Aleyda parity, also use `hreflang-i18n-implementation-verification` skill.
- **`--save-crawl` writes 100MB+ binary per 10K URLs** — disk fills fast on scheduled crawls. Add `--max-saved-crawls 5` or rotate manually.
- **Mobile UA strings change yearly** — Google's official UA is at https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers. Update annually.

## Sources

- [Screaming Frog CLI guide](https://www.screamingfrog.co.uk/seo-spider/user-guide/general/#commandlineinterface)
- [Screaming Frog JavaScript rendering config](https://www.screamingfrog.co.uk/seo-spider/user-guide/configuration/#javascript-rendering)
- [Sitebulb CLI guide](https://sitebulb.com/resources/guides/how-to-use-the-sitebulb-cli/)
- [Botify Analytics REST API](https://developers.botify.com/reference/get-started)
- [Botify log analyzer overview](https://www.botify.com/blog/log-analyzer)
- [Google Search Central — mobile-first indexing complete (2023)](https://developers.google.com/search/blog/2023/10/mobile-first-indexing-complete)
- [Google Search Central — crawler user agents](https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers)
