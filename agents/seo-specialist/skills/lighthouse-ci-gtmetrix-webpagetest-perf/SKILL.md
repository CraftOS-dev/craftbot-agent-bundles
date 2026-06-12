<!--
Source: https://github.com/GoogleChrome/lighthouse-ci
Source: https://gtmetrix.com/api/docs/2.0/
Source: https://docs.webpagetest.org/api/
Depth: lab perf measurement + regression gating with Lighthouse CI / GTmetrix / WebPageTest
-->
# Lab Performance — Lighthouse CI / GTmetrix / WebPageTest

## When to use

Reach for this skill when the user asks for: "Lighthouse CI", "performance regression gate", "GTmetrix waterfall", "WebPageTest real device", "lab perf measurement", "pre-deploy perf check", "CI/CD performance gating", "perf budget". This is the depth specialist for LAB-side performance — Lighthouse CI for regression gating in CI/CD, GTmetrix for waterfall + perf scoring (alt), WebPageTest for real-device + connection profiles. Pairs with `core-web-vitals-deep-pagespeed-crux` (field data) — labs catch regressions before users.

## Setup

```bash
# Lighthouse CI — primary lab perf gating
npx @lhci/cli --version
# Or pin: npm install -g @lhci/cli@latest

# GTmetrix API — waterfall analysis
export GTMETRIX_API_KEY="<from gtmetrix.com/api/dashboard>"

# WebPageTest API — real devices + connections
export WPT_API_KEY="<from webpagetest.org/getkey.php>"
```

Auth/pricing:
- Lighthouse CI — free (open source)
- `GTMETRIX_API_KEY` — Pro $14.95+/mo for API (250 calls/mo)
- `WPT_API_KEY` — free 200 runs/day on public WPT; private instances paid

## Common recipes

### Recipe 1: Lighthouse CI one-off audit
```bash
npx @lhci/cli autorun \
  --collect.url=https://example.com/page \
  --collect.url=https://example.com/category/electronics \
  --collect.url=https://example.com/products/widget \
  --collect.numberOfRuns=3 \
  --collect.settings.preset=desktop \
  --upload.target=temporary-public-storage
```
`numberOfRuns=3` median-of-3 reduces noise. `temporary-public-storage` uploads to a temporary share URL for review.

### Recipe 2: Lighthouse CI config file (.lighthouserc.json)
```json
{
  "ci": {
    "collect": {
      "url": [
        "https://example.com/",
        "https://example.com/category/electronics",
        "https://example.com/products/widget"
      ],
      "numberOfRuns": 3,
      "settings": {
        "preset": "desktop",
        "throttling": {
          "rttMs": 40,
          "throughputKbps": 10240,
          "cpuSlowdownMultiplier": 1
        }
      }
    },
    "assert": {
      "assertions": {
        "categories:performance": ["error", {"minScore": 0.85}],
        "categories:accessibility": ["error", {"minScore": 0.9}],
        "categories:seo": ["error", {"minScore": 0.95}],
        "largest-contentful-paint": ["error", {"maxNumericValue": 2500}],
        "cumulative-layout-shift": ["error", {"maxNumericValue": 0.1}],
        "total-blocking-time": ["error", {"maxNumericValue": 300}],
        "interactive": ["warn", {"maxNumericValue": 3500}],
        "speed-index": ["warn", {"maxNumericValue": 3400}]
      }
    },
    "upload": {
      "target": "lhci",
      "serverBaseUrl": "https://lhci-server.example.com",
      "token": "<lhci-token>"
    }
  }
}
```
Stricter for mobile: use `preset: "mobile"` and lower CPU/throughput.

### Recipe 3: Lighthouse CI in GitHub Actions
```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI
on: [pull_request]
jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: {node-version: '20'}
      - run: npm ci
      - run: npm run build
      - run: npm run start &
      - run: |
          sleep 5
          npx @lhci/cli autorun --config=.lighthouserc.json
        env:
          LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}
```
Blocks PR merge if any `assertion` fails.

### Recipe 4: GTmetrix waterfall + perf scoring
```bash
# Trigger test
curl -X POST https://gtmetrix.com/api/2.0/tests \
  -u "$GTMETRIX_API_KEY:" \
  -H "Content-Type: application/vnd.api+json" \
  -d '{
    "data": {
      "type":"test",
      "attributes":{
        "url":"https://example.com/page",
        "browser":"5",
        "location":"1",
        "report":"lighthouse",
        "throttle":"4G"
      }
    }
  }'

# Returns: {"data":{"id":"<test-id>","links":{"self":"..."}}}

# Poll for completion
curl "https://gtmetrix.com/api/2.0/tests/<test-id>" -u "$GTMETRIX_API_KEY:"

# Pull waterfall report
curl "https://gtmetrix.com/api/2.0/reports/<report-id>" -u "$GTMETRIX_API_KEY:" \
  -H "Accept: application/vnd.api+json"
```
GTmetrix reports include Lighthouse data + waterfall + filmstrip.

### Recipe 5: WebPageTest real-device + connection profiles
```bash
# Trigger test on iPhone Galaxy S20 with 4G throttling
curl "https://www.webpagetest.org/runtest.php?url=https://example.com&runs=3&fvonly=1&location=Dulles_iPhone12:4G&f=json&k=$WPT_API_KEY"

# Poll: returns testId
# https://www.webpagetest.org/testStatus.php?test=<testId>&f=json

# Pull result
curl "https://www.webpagetest.org/jsonResult.php?test=<testId>"
```
`location=Dulles_iPhone12:4G` — Dulles location, iPhone 12 device, 4G profile. WPT has 30+ device + 10+ connection options.

### Recipe 6: Perf budget definition (Lighthouse CI assertions)
```json
{
  "ci": {
    "assert": {
      "assertions": {
        "resource-summary:script:size": ["error", {"maxNumericValue": 350000}],
        "resource-summary:image:size": ["error", {"maxNumericValue": 500000}],
        "resource-summary:stylesheet:size": ["error", {"maxNumericValue": 60000}],
        "resource-summary:document:size": ["error", {"maxNumericValue": 30000}],
        "resource-summary:font:size": ["error", {"maxNumericValue": 100000}],
        "resource-summary:third-party:count": ["warn", {"maxNumericValue": 10}],
        "uses-text-compression": ["error", {"minScore": 1}],
        "uses-responsive-images": ["error", {"minScore": 1}],
        "uses-rel-preconnect": ["warn", {"minScore": 1}],
        "uses-rel-preload": ["warn", {"minScore": 1}]
      }
    }
  }
}
```

### Recipe 7: Multi-URL diff (which URL is the worst offender)
```python
import json

# Lighthouse CI reports land in .lighthouseci/
import glob
reports = [json.load(open(f)) for f in glob.glob('.lighthouseci/lhr-*.json')]

import pandas as pd
df = pd.DataFrame([{
    'url': r['finalDisplayedUrl'],
    'performance_score': r['categories']['performance']['score'] * 100,
    'lcp': r['audits']['largest-contentful-paint']['numericValue'],
    'tbt': r['audits']['total-blocking-time']['numericValue'],
    'cls': r['audits']['cumulative-layout-shift']['numericValue'],
    'fcp': r['audits']['first-contentful-paint']['numericValue'],
    'si': r['audits']['speed-index']['numericValue']
} for r in reports])

# Worst-performing URLs
print(df.sort_values('performance_score').head(10))
```

### Recipe 8: Diagnose specific issue (render-blocking, etc.)
```python
def diagnose_url(report):
    issues = []
    for audit_id, audit in report['audits'].items():
        if audit.get('score') is not None and audit['score'] < 0.9 and audit.get('numericValue', 0) > 0:
            issues.append({
                'audit': audit_id,
                'title': audit.get('title'),
                'score': audit['score'],
                'value': audit.get('numericValue'),
                'description': audit.get('description'),
                'items': audit.get('details', {}).get('items', [])[:5]
            })
    return sorted(issues, key=lambda x: x['score'])[:10]
```
Common offenders: `render-blocking-resources`, `unused-javascript`, `unused-css-rules`, `total-blocking-time`, `uses-text-compression`, `efficient-animated-content`, `uses-responsive-images`, `offscreen-images`.

### Recipe 9: Lighthouse CI Server for trend tracking
```bash
# Self-host LHCI Server for historical trend tracking
docker run -d --name lhci-server -p 9001:9001 patrickhulce/lhci-server:0.13.0

# Configure .lighthouserc.json
{
  "ci": {
    "upload": {
      "target": "lhci",
      "serverBaseUrl": "http://lhci-server:9001",
      "token": "<wizard-generated-token>"
    }
  }
}

# Run: `lhci autorun` → uploads runs to server with project context
# Dashboard at http://localhost:9001 shows trend per metric per URL
```

### Recipe 10: WebPageTest connection profile testing
```bash
# Test same URL across multiple connections (3G slow / 4G / Cable)
for CONN in 'Cable' '4G' '3G' '3GSlow' '3GFast'; do
  curl "https://www.webpagetest.org/runtest.php?url=https://example.com&runs=3&fvonly=1&location=Dulles_iPhone12:$CONN&f=json&k=$WPT_API_KEY"
done

# Especially important for mobile-first audit + global audiences (3G common in India / SEA / Latin America)
```

### Recipe 11: WebPageTest filmstrip + visual progress
```bash
# Returns visual progress images at each timeline point
curl "https://www.webpagetest.org/video/createVideo.php?tests=<test-id>&f=json&end=visual"
# Returns videoUrl
```
Useful for showing engineering team WHERE perf gets slow visually.

## Examples

### Example 1: Set up Lighthouse CI gate for new feature deploys
**Goal:** Block PR merge if perf regresses.

**Steps:**
1. Recipe 2: write `.lighthouserc.json` with assertions per ranking-relevant URL.
2. Recipe 3: add GitHub Action.
3. Recipe 6: define perf budget assertions.
4. Test on existing PR — verify gate fires correctly.
5. Iterate thresholds based on stable baseline.

**Result:** Perf regression caught at PR time, not post-deploy.

### Example 2: Diagnose specific perf regression (LCP up 800ms post-deploy)
**Goal:** Identify what changed.

**Steps:**
1. Recipe 4 (GTmetrix) or Recipe 5 (WPT) on the affected URL.
2. Recipe 8: diagnose top 10 audits.
3. Common findings: new render-blocking JS, new font preload, unoptimized hero image.
4. Hand off to `frontend-engineer` with specific recommendations.

**Result:** Root cause + remediation hand-off.

### Example 3: 3G-emulated audit for emerging markets
**Goal:** Site fast in US but slow in India — verify.

**Steps:**
1. Recipe 5: WPT from India location (Mumbai), 3GSlow.
2. Compare to US baseline (Cable + Dulles).
3. Identify mobile + slow-connection specific issues.
4. Recipe 11: filmstrip → confirm visual completion time.

**Result:** Emerging-market perf snapshot; targeted fixes for global audience.

## Edge cases / gotchas

- **Lab data != real-user data** — Lighthouse simulates Slow 4G + 4× CPU slowdown. Real users vary. Combine with CrUX (`core-web-vitals-deep-pagespeed-crux`).
- **Median-of-3 still noisy** — for stable trend, use median-of-5 or roll over 24h with multiple test runs.
- **Lighthouse CI assertions error vs warn** — `error` blocks PR; `warn` logs but allows. Reserve `error` for critical CWV (LCP, INP, CLS) + perf score.
- **Single-URL Lighthouse misses template variance** — sample multiple URLs per template (Recipe 1 multi-url).
- **GTmetrix browser only Chrome by default** — Firefox + Safari testing requires separate setup.
- **WebPageTest public instance rate limit** — 200 runs/day across all keys. Private WPT for higher.
- **Lighthouse CI Server token leak risk** — store in env or secret manager; never commit.
- **3rd-party scripts dominate INP/TBT** — chat widgets, ads, analytics. Defer / async where possible.
- **Page-load events vary by metric definition** — LCP is largest contentful paint; TTI/TBT measure interactivity. Don't conflate.
- **Service workers can mask perf** — pre-cached pages look fast in lab; first-visit users see real perf.
- **Vercel preview deployments** — Lighthouse CI on preview URLs needs auth; pass `LHCI_HEADERS` env var.
- **HTTP/3 + early hints** — newer optimizations not all measured by older Lighthouse versions. Update to latest @lhci/cli regularly.
- **`@lhci/cli` autorun upload step** — without `--upload.target=temporary-public-storage`, no share URL; useful in CI logs.

## Sources

- [Lighthouse CI GitHub](https://github.com/GoogleChrome/lighthouse-ci)
- [Lighthouse CI getting started](https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/getting-started.md)
- [Lighthouse CI assertions](https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/configuration.md#assertions)
- [GTmetrix API documentation](https://gtmetrix.com/api/docs/2.0/)
- [WebPageTest API documentation](https://docs.webpagetest.org/api/)
- [WebPageTest locations + connections](https://docs.webpagetest.org/api/locations/)
- [web.dev — Lighthouse performance scoring](https://web.dev/articles/performance-scoring)
- [web.dev — performance budgets](https://web.dev/articles/use-lighthouse-for-performance-budgets)
- [Vercel — Lighthouse CI preview deployments](https://vercel.com/docs/integrations/lighthouse-ci)
