<!--
Source: https://developers.google.com/search/docs/appearance/core-web-vitals
PageSpeed Insights API v5
-->
# PageSpeed Insights + Core Web Vitals — SKILL

Google PageSpeed Insights API combines CrUX field data (real users) + Lighthouse lab data into one API call. SOTA for the LCP < 2.5s / INP < 200ms / CLS < 0.1 audit that gates SEO ranking.

## When to use this skill

- **Core Web Vitals audit** — LCP, INP (replaced FID in March 2024), CLS.
- **Mobile vs desktop performance comparison** — separate runs required.
- **Pre/post-deploy performance regression check**.
- **Competitive benchmarking** — same audit on competitor URLs.
- **Lighthouse SEO + Accessibility + Best Practices score** beyond just CWV.

**Do NOT use this skill when:**
- **GSC's Search Performance** report — use `suganthan-gsc-audit` skill.
- **Real-user RUM** with custom dimensions — use a dedicated RUM tool (SpeedCurve, RUMVision).
- **Synthetic transaction tests across user flows** — Lighthouse single-page only.

## Setup

### Auth — API key (free)

```bash
# Get free key at https://developers.google.com/speed/docs/insights/v5/get-started
export PSI_KEY="<key>"
```

Free tier: 25,000 queries/day. No OAuth needed.

### Endpoint

```bash
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?\
url=https://yourbrand.com/&\
category=performance&\
category=accessibility&\
category=best-practices&\
category=seo&\
strategy=mobile&\
key=$PSI_KEY"
```

## Common recipes

### Recipe 1: Mobile + desktop CWV audit (single URL)

```bash
URL="https://yourbrand.com/important-page"

for strategy in mobile desktop; do
  curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?\
url=$URL&\
category=performance&\
strategy=$strategy&\
key=$PSI_KEY" > psi-$strategy.json
done

# Extract CrUX field data
jq '{
  strategy: .lighthouseResult.configSettings.formFactor,
  cwv: {
    lcp: .loadingExperience.metrics.LARGEST_CONTENTFUL_PAINT_MS,
    inp: .loadingExperience.metrics.INTERACTION_TO_NEXT_PAINT,
    cls: .loadingExperience.metrics.CUMULATIVE_LAYOUT_SHIFT_SCORE
  },
  lab: {
    lcp: .lighthouseResult.audits["largest-contentful-paint"].numericValue,
    inp_proxy: .lighthouseResult.audits["interactive"].numericValue,
    cls: .lighthouseResult.audits["cumulative-layout-shift"].numericValue,
    fcp: .lighthouseResult.audits["first-contentful-paint"].numericValue,
    tbt: .lighthouseResult.audits["total-blocking-time"].numericValue,
    si: .lighthouseResult.audits["speed-index"].numericValue
  },
  performance_score: .lighthouseResult.categories.performance.score
}' psi-mobile.json
```

### Recipe 2: Pass/fail against Google thresholds

```python
def cwv_status(field):
    """field is loadingExperience.metrics from PSI response"""
    lcp = field.get('LARGEST_CONTENTFUL_PAINT_MS', {})
    inp = field.get('INTERACTION_TO_NEXT_PAINT', {})
    cls = field.get('CUMULATIVE_LAYOUT_SHIFT_SCORE', {})

    return {
        'LCP': {
            'p75_ms': lcp.get('percentile'),
            'status': 'GOOD' if lcp.get('percentile', 99999) < 2500 else ('NEEDS_IMPROVEMENT' if lcp.get('percentile') < 4000 else 'POOR'),
        },
        'INP': {
            'p75_ms': inp.get('percentile'),
            'status': 'GOOD' if inp.get('percentile', 99999) < 200 else ('NEEDS_IMPROVEMENT' if inp.get('percentile') < 500 else 'POOR'),
        },
        'CLS': {
            'p75': cls.get('percentile', 0) / 100,  # CrUX returns ×100
            'status': 'GOOD' if cls.get('percentile', 99999) < 10 else ('NEEDS_IMPROVEMENT' if cls.get('percentile') < 25 else 'POOR'),
        },
    }
```

Pass = all three GOOD on mobile + desktop.

### Recipe 3: Top opportunities (Lighthouse audit recommendations)

```bash
jq '.lighthouseResult.audits | to_entries[] | select(.value.details.type=="opportunity") | {audit: .key, savings_ms: .value.numericValue, description: .value.title}' psi-mobile.json | head -10
```

Common opportunities:
- `unused-css-rules` — remove unused CSS
- `unused-javascript` — code-split / tree-shake
- `render-blocking-resources` — defer non-critical CSS/JS
- `uses-optimized-images` — WebP/AVIF
- `uses-text-compression` — Brotli/gzip
- `uses-rel-preconnect` — preconnect to CDN
- `largest-contentful-paint-element` — optimize the LCP image specifically

### Recipe 4: Multi-URL batch audit

```bash
# urls.txt — one per line
while read url; do
  echo "Auditing $url..."
  curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=$url&strategy=mobile&key=$PSI_KEY" \
    | jq "{url: \"$url\", performance: .lighthouseResult.categories.performance.score, lcp: .lighthouseResult.audits[\"largest-contentful-paint\"].numericValue, cls: .lighthouseResult.audits[\"cumulative-layout-shift\"].numericValue}" \
    >> audit-results.jsonl
done < urls.txt
```

Rate limit: 1 req/sec safe; PSI auto-throttles beyond.

### Recipe 5: LCP element identification (most actionable)

```bash
jq '.lighthouseResult.audits["largest-contentful-paint-element"].details' psi-mobile.json
```

Returns the actual DOM element + selector that's the LCP. Optimization plan:
- If `<img>`: preload, optimize size, WebP, lazy-load offscreen
- If `<h1>` text: ensure font is preloaded with `font-display: swap`
- If video poster: same as image

### Recipe 6: CLS root cause

```bash
jq '.lighthouseResult.audits["layout-shift-elements"].details.items' psi-mobile.json
```

Each item: the DOM element + the shift score it contributed. Top contributors usually:
- Images without `width`/`height` attributes
- Ads / iframes without reserved space
- Late-loading webfonts (FOIT/FOUT)
- Cookie banners that push content down

### Recipe 7: INP audit (interaction responsiveness)

```bash
# CrUX field INP
jq '.loadingExperience.metrics.INTERACTION_TO_NEXT_PAINT' psi-mobile.json

# Lab proxy via Lighthouse Total Blocking Time
jq '.lighthouseResult.audits["total-blocking-time"]' psi-mobile.json
```

INP fixes:
- Break long tasks (> 50ms) into smaller chunks
- Defer non-essential JS
- Use `requestIdleCallback`
- Optimize event handlers (debounce/throttle)
- Reduce React/Vue re-renders on interaction

### Recipe 8: Schedule weekly audits (Notion alert)

```bash
# Cron weekly via cli-anything
KEY_PAGES="https://brand.com/ https://brand.com/pricing https://brand.com/blog/key-post"

for url in $KEY_PAGES; do
  result=$(curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=$url&strategy=mobile&key=$PSI_KEY")
  score=$(echo "$result" | jq '.lighthouseResult.categories.performance.score * 100')
  lcp_status=$(echo "$result" | jq '.loadingExperience.metrics.LARGEST_CONTENTFUL_PAINT_MS.category')

  if (( $(echo "$score < 70" | bc -l) )); then
    # Alert via gmail-mcp or Notion
    notion_create_alert "PSI score for $url dropped to $score (LCP: $lcp_status)"
  fi
done
```

## Examples — full performance audit report

```markdown
# Performance Audit — yourbrand.com

## Summary (mobile)
| Page | Score | LCP | INP | CLS | Status |
|---|---|---|---|---|---|
| / | 78 | 2.1s ✅ | 180ms ✅ | 0.08 ✅ | GOOD |
| /pricing | 62 | 3.2s ⚠ | 240ms ⚠ | 0.04 ✅ | NEEDS_IMPROVEMENT |
| /blog/post | 71 | 2.8s ⚠ | 150ms ✅ | 0.12 ⚠ | NEEDS_IMPROVEMENT |

## Top opportunities (sorted by impact)
1. Unused JS — savings 1.4s — pages: /pricing, /blog/post
2. Render-blocking CSS — savings 0.9s — all pages
3. Image format (WebP/AVIF) — savings 0.6s — /blog/post hero
4. Preconnect to CDN — savings 0.3s — all pages

## LCP elements
- /pricing — `<img class="hero">` (1.8MB JPG) — needs WebP + width/height
- /blog/post — `<img class="featured">` (2.1MB PNG) — needs WebP + lazy

## CLS contributors
- /blog/post — `<iframe>` ad slot — needs reserved height
- All pages — webfont loading FOUT — needs `font-display:optional` or preload

## Recommended fixes (priority order)
1. Convert hero images to WebP/AVIF + add explicit dimensions (CTO: 1 day)
2. Defer non-critical JS bundles via dynamic import (engineering: 2 days)
3. Inline critical CSS, defer rest (engineering: 1 day)
4. Preconnect to CDN + preload critical assets (engineering: 0.5 day)
```

## Edge cases

### CrUX coverage
- Some URLs have no CrUX data (low traffic). Then `loadingExperience` is absent — fall back to `lighthouseResult` lab metrics.
- CrUX is rolling 28 days. Recent changes take time to reflect.
- CrUX is page-level for high-traffic pages, origin-level fallback otherwise.

### Mobile-first
Google ranking uses mobile CWV primarily. Always audit mobile first; desktop is secondary.

### INP rollout
- INP replaced FID March 2024 as the responsiveness metric
- Lab tools (Lighthouse) don't have a perfect INP simulator — `total-blocking-time` is the closest proxy
- Real INP only available via CrUX field data

### Variability
Lab Lighthouse scores fluctuate ±10 across runs due to network simulation. For production decisions, average 3 runs or rely on CrUX field data.

### Mobile network throttling
Default Lighthouse mobile = "Slow 4G" + 4x CPU slowdown. Realistic but pessimistic. For exec reporting, also include "no throttling" desktop score.

### CWV "good" thresholds (June 2026)
- LCP: < 2.5s (good), 2.5-4.0s (needs improvement), > 4.0s (poor)
- INP: < 200ms (good), 200-500ms (needs improvement), > 500ms (poor)
- CLS: < 0.1 (good), 0.1-0.25 (needs improvement), > 0.25 (poor)

Page passes only if ALL three are "good" at p75 of real users.

### Rate limits
- 25,000 requests/day free
- 1 request/sec recommended
- For 100s of URLs, batch over multiple days or use Lighthouse CLI locally

### Lighthouse CLI alternative
For deeper customization (custom user agents, internal pages, headers):

```bash
npx lighthouse https://yourbrand.com/ --output=json --output-path=./report.json --chrome-flags="--headless"
```

## Sources

- **Core Web Vitals**: https://developers.google.com/search/docs/appearance/core-web-vitals
- **PageSpeed Insights API**: https://developers.google.com/speed/docs/insights/v5/get-started
- **CrUX docs**: https://developer.chrome.com/docs/crux
- **INP guidance**: https://web.dev/articles/inp
- **Lighthouse CLI**: https://github.com/GoogleChrome/lighthouse
