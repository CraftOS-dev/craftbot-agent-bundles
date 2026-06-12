<!--
Source: https://www.screamingfrog.co.uk/seo-spider/user-guide/configuration/#javascript-rendering
Source: https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect
Source: https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
Depth: CSR vs SSR vs SSG vs ISR indexing-impact decision tree + Search Console URL Inspection
-->
# JS Rendering — CSR / SSR / SSG / ISR Indexing Impact

## When to use

Reach for this skill when the user asks for: "JavaScript SEO audit", "is Google rendering my SPA", "CSR vs SSR", "Next.js SSR check", "React SEO", "Vue SEO", "Angular SEO", "URL Inspection API", "Googlebot rendered DOM", "JS rendering audit", "client-side rendering indexing", "rendering strategy". This is the depth specialist for verifying that JS-rendered content actually reaches Google's index. Decision tree: CSR (high risk) → SSR (low risk) → SSG (very low) → ISR (low). Test via SF JS-mode vs Text-Only diff, then verify via Search Console URL Inspection API.

## Setup

```bash
# Screaming Frog for JS-mode + Text-Only crawl modes
screamingfrogseospider --help

# Search Console URL Inspection API
# Requires GSC OAuth (same as Suganthan GSC MCP)
export GSC_TOKEN="<bearer token>"

# Lighthouse CI for render-blocking + TBT diagnostics
npx @lhci/cli --version

# Playwright MCP for direct headless Chrome render checks (alt to SF)
# Pre-configured via CraftBot defaults
```

Auth requirements:
- SF license
- `GSC_TOKEN` — webmasters scope; same OAuth as Suganthan GSC

## Common recipes

### Recipe 1: SF JavaScript-mode crawl
```bash
screamingfrogseospider \
  --crawl https://spa-site.com \
  --crawl-mode JavaScript \
  --headless \
  --max-threads 5 \
  --crawl-delay 500 \
  --export-tabs "Internal:All,JavaScript:All,JavaScript:Pages with Blocked Resources,JavaScript:Pages with JavaScript Content,JavaScript:Contains JavaScript Links" \
  --output-folder ./js-crawl
```

### Recipe 2: SF Text-Only-mode crawl (no JS execution)
```bash
screamingfrogseospider \
  --crawl https://spa-site.com \
  --crawl-mode TextOnly \
  --headless \
  --export-tabs "Internal:All" \
  --output-folder ./txt-crawl
```

### Recipe 3: Diff JS vs Text-Only — identify at-risk content
```python
import pandas as pd

js = pd.read_csv('./js-crawl/internal_all.csv')[['Address','Word Count','Title 1','H1','Outlinks']]
txt = pd.read_csv('./txt-crawl/internal_all.csv')[['Address','Word Count','Title 1','H1','Outlinks']]

# Merge on URL
diff = js.merge(txt, on='Address', suffixes=('_js','_txt'), how='outer')

# At-risk URLs: JS WC ≫ Text WC (content is JS-dependent)
diff['wc_diff'] = diff['Word Count_js'] - diff['Word Count_txt']
diff['wc_ratio'] = diff['Word Count_js'] / diff['Word Count_txt'].replace(0, 1)

at_risk = diff[diff['wc_ratio'] > 2]  # JS renders 2× more content than text-only
print(f"At-risk URLs: {len(at_risk)}")
print(at_risk[['Address','Word Count_js','Word Count_txt','wc_ratio']].head(20))

# URLs in JS but NOT in Text-Only = invisible to non-JS crawlers
js_only = diff[diff['Word Count_txt'].isna()]
print(f"JS-only URLs: {len(js_only)}")
```

### Recipe 4: Search Console URL Inspection API — confirm Googlebot rendered DOM
```bash
curl -X POST "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect" \
  -H "Authorization: Bearer $GSC_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "inspectionUrl":"https://spa-site.com/page",
    "siteUrl":"sc-domain:spa-site.com",
    "languageCode":"en-US"
  }'
```
Returns:
- `lastCrawlTime` — when Googlebot last fetched
- `pageFetchState` — SUCCESSFUL / NOT_FOUND / SOFT_404 / FORBIDDEN / BLOCKED_ROBOTS_TXT
- `indexingState` — INDEXING_ALLOWED / BLOCKED_BY_NOINDEX / etc.
- `googleCanonical` vs `userCanonical` — mismatch warning
- `crawledAs` — DESKTOP / MOBILE
- `mobileUsabilityResult` — issues detected on mobile

### Recipe 5: Python loop for URL Inspection sample
```python
import requests, time

def inspect_url(url, site_url):
    r = requests.post(
        'https://searchconsole.googleapis.com/v1/urlInspection/index:inspect',
        headers={'Authorization': f'Bearer {GSC_TOKEN}','Content-Type':'application/json'},
        json={'inspectionUrl': url, 'siteUrl': site_url, 'languageCode':'en-US'}
    )
    return r.json().get('inspectionResult',{})

# Sample 30 representative URLs
sample_urls = [
    'https://spa-site.com/',
    'https://spa-site.com/products/widget',
    # ... 28 more covering main templates
]

results = []
for url in sample_urls:
    res = inspect_url(url, 'sc-domain:spa-site.com')
    results.append({
        'url': url,
        'verdict': res.get('indexStatusResult',{}).get('verdict'),
        'coverage': res.get('indexStatusResult',{}).get('coverageState'),
        'last_crawl': res.get('indexStatusResult',{}).get('lastCrawlTime'),
        'fetch_state': res.get('indexStatusResult',{}).get('pageFetchState'),
        'google_canonical': res.get('indexStatusResult',{}).get('googleCanonical'),
        'user_canonical': res.get('indexStatusResult',{}).get('userCanonical'),
    })
    time.sleep(1)  # rate limit

# Flag mismatches
import pandas as pd
df = pd.DataFrame(results)
canonical_conflicts = df[df['google_canonical'] != df['user_canonical']]
print(f"Canonical conflicts: {len(canonical_conflicts)}")
```

### Recipe 6: Playwright direct render check (alt to SF)
```python
# Pure Playwright headless Chrome render to verify what JS produces
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(user_agent='Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')
    page.goto('https://spa-site.com/page', wait_until='networkidle')

    # Get rendered HTML
    html = page.content()
    # Get rendered text
    text = page.evaluate('() => document.body.innerText')
    # Get all links
    links = page.evaluate('() => Array.from(document.querySelectorAll("a")).map(a => a.href)')

    print(f"Rendered text length: {len(text)} chars")
    print(f"Links found: {len(links)}")

    browser.close()
```

### Recipe 7: Decision matrix — rendering strategy → recommendation
```python
RECOMMENDATIONS = {
    'CSR': {
        'risk': 'High — Googlebot may not render full content on first crawl',
        'fix': 'Migrate to SSR or SSG; verify with Search Console URL Inspection',
        'examples': ['React SPA without SSR', 'Vue SPA without nuxt', 'Angular SPA'],
    },
    'SSR': {
        'risk': 'Low — Googlebot sees fully-rendered HTML on first crawl',
        'fix': 'Verify periodically via URL Inspection; consider ISR for performance',
        'examples': ['Next.js getServerSideProps', 'Nuxt SSR', 'Express + React render'],
    },
    'SSG': {
        'risk': 'Very low — static HTML on first crawl',
        'fix': 'Verify build outputs match expected URLs; verify sitemap completeness',
        'examples': ['Astro SSG', 'Next.js getStaticProps', 'Hugo', 'Jekyll', '11ty'],
    },
    'ISR': {
        'risk': 'Low — static at edge, regenerates on revalidate period',
        'fix': 'Verify revalidate balances freshness vs crawl-budget (24-72h sweet spot)',
        'examples': ['Next.js ISR', 'Vercel ISR', 'Cloudflare incremental'],
    },
}
```

### Recipe 8: Detect rendering strategy from HTML signals
```python
def detect_rendering(url):
    # Fetch raw HTML (no JS)
    raw = requests.get(url, headers={'User-Agent':'Mozilla/5.0 (compatible; Googlebot/2.1)'}).text

    # Fetch JS-rendered HTML
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')
        rendered = page.content()
        browser.close()

    raw_word_count = len(raw.split())
    rendered_word_count = len(rendered.split())

    # Heuristics
    if rendered_word_count > raw_word_count * 5:
        return 'CSR'  # JS produces vastly more content
    if 'data-reactroot' in raw or 'data-server-rendered="true"' in raw:
        return 'SSR'  # React/Vue SSR markers
    if rendered_word_count <= raw_word_count * 1.1:
        return 'SSG'  # No meaningful JS execution
    if 'x-vercel-cache' in raw.lower():
        return 'ISR'  # Vercel ISR marker
    return 'Unknown'
```

### Recipe 9: Infinite scroll + pagination SEO check
```python
# Infinite scroll requires paginated URL fallback (Google reaffirmed 2024)
# Test:
# 1. Recipe 1 (SF JS-mode) — confirms paginated URLs discovered via JS
# 2. Test paginated URL directly:
import requests

def test_pagination(base_url, page_num):
    # Try common pagination URL patterns
    patterns = [
        f"{base_url}?page={page_num}",
        f"{base_url}/page/{page_num}",
        f"{base_url}/p/{page_num}",
        f"{base_url}/{page_num}",
    ]
    for pattern in patterns:
        r = requests.get(pattern)
        if r.status_code == 200 and 'page 2' in r.text.lower():  # heuristic
            print(f"Works: {pattern}")
            return pattern
    print(f"No paginated URL found for {base_url}")
    return None
```

### Recipe 10: Lighthouse render-blocking + TBT diagnosis
```bash
npx @lhci/cli autorun --collect.url=https://spa-site.com/page --collect.settings.preset=desktop

# Key audits for JS rendering:
# - render-blocking-resources
# - bootup-time  (JS parsing/compile time)
# - mainthread-work-breakdown
# - third-party-summary
# - unused-javascript
```

## Examples

### Example 1: Verify Next.js ISR site is rendering correctly to Googlebot
**Goal:** Confirm ISR pages reach Google's index with full content.

**Steps:**
1. Recipe 1: SF JS-mode crawl 100 URLs.
2. Recipe 2: SF Text-Only crawl same 100.
3. Recipe 3: diff → expect near-equal WC (ISR pre-renders, so Text-Only sees mostly-complete HTML).
4. Recipe 5: URL Inspection on 10 samples → confirm `pageFetchState=SUCCESSFUL` + `coverageState=Submitted and indexed`.
5. Recipe 10: confirm no render-blocking + TBT < 200ms.

**Result:** Confidence that ISR works as intended; no JS-rendering gap.

### Example 2: React SPA migration to SSR — pre-migration audit
**Goal:** Quantify current JS-rendering gap before migrating to SSR.

**Steps:**
1. Recipe 7: classify current = CSR.
2. Recipe 1+2+3: full JS vs Text-Only diff → typically 80-95% of pages show JS-WC > Text-WC × 5.
3. Recipe 5: URL Inspection sample → expect `coverageState="Crawled - currently not indexed"` or partial-content indexed.
4. Recipe 8: confirm rendering strategy CSR signals (data-reactroot absent in raw HTML).
5. Recommend SSR migration (defer to `frontend-engineer`); brief includes:
   - Migration target: Next.js getServerSideProps OR ISR (24h)
   - Expected impact: +30-60% indexing coverage, +20-40% organic traffic in 60-90 days

**Result:** Pre-migration audit; quantified gap; migration brief.

### Example 3: Infinite-scroll PLP indexing verification
**Goal:** E-comm PLP with infinite scroll — are paginated URLs indexing?

**Steps:**
1. Recipe 9: confirm `?page=2` etc. work directly.
2. Recipe 1: SF JS-mode crawl → should discover pagination URLs after scroll.
3. Recipe 5: URL Inspection on `?page=2`, `?page=5`, `?page=10` → confirm indexing.
4. If not indexing: ensure `<link rel="next">` (deprecated by Google 2019 but still useful) OR explicit anchor links in HTML.

**Result:** Pagination indexing confirmed (or recommendation to fix).

## Edge cases / gotchas

- **CSR sites slowly losing indexing share since 2020** — Google has improved JS rendering, but first-pass crawl still missing JS-only content frequently.
- **Two-pass indexing latency** — Google's JS-rendering queue lags 0-7 days behind first crawl. Critical content should be SSR.
- **`networkidle` Playwright wait** — may hang on sites with constant polling. Use `domcontentloaded` + manual wait if so.
- **URL Inspection API rate limit** — 2000/day per property. Sample, don't sweep.
- **`renderedDom` summary not in API response** — only available in Search Console UI. API gives metadata only; for actual DOM use Playwright.
- **`coverageState="Crawled - currently not indexed"`** — common JS-rendering symptom. Cross-verify with content quality / cannibalization first before blaming JS.
- **SSR + lazy-load JS components** — server renders the shell, client lazy-loads. Some content STILL needs CSR behavior. Audit critical above-fold content separately.
- **ISR revalidate too short = crawl-budget waste** — sub-24h ISR causes Googlebot to re-fetch unchanged pages.
- **Service worker caching** — can serve stale content to Googlebot. Disable SW for Googlebot UA OR use `s-maxage` headers.
- **Hash-based routing (#/page)** — Google does NOT crawl fragment URLs as separate pages. Use `pushState`-based routing only.
- **AJAX-rendered content with no fallback** — Googlebot may execute JS, but if your `<noscript>` is empty, low-end crawlers / preview cards see nothing. Add semantic HTML fallback.
- **`<noscript>` content not weighted as ranking signal** — useful for fallback display, not ranking boost.
- **Cookie banners blocking content** — render blockers that hide content until acceptance. Audit if banners trigger before Googlebot's intersection events.

## Sources

- [Google — JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics)
- [Google — fix JavaScript rendering issues](https://developers.google.com/search/docs/crawling-indexing/javascript/fix-search-javascript)
- [Google Search Console URL Inspection API](https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect)
- [Screaming Frog JavaScript rendering config](https://www.screamingfrog.co.uk/seo-spider/user-guide/configuration/#javascript-rendering)
- [Google — infinite scroll + pagination guide](https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading)
- [Google — rel=next prev deprecation](https://developers.google.com/search/blog/2019/03/rel-next-prev)
- [Playwright Python documentation](https://playwright.dev/python/docs/intro)
- [Vercel — Next.js ISR](https://vercel.com/docs/incremental-static-regeneration)
- [Search Engine Journal — JavaScript SEO guide](https://www.searchenginejournal.com/javascript-seo/)
