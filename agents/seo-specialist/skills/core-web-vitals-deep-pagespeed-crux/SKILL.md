<!--
Source: https://developers.google.com/search/docs/appearance/core-web-vitals
Source: https://developer.chrome.com/docs/crux/api
Source: https://developers.google.com/speed/docs/insights/v5/get-started
Depth: per-template + per-cohort CWV depth (PageSpeed + CrUX + Lighthouse CI)
-->
# Core Web Vitals — Deep PageSpeed + CrUX Analysis

## When to use

Reach for this skill when the user asks for: "Core Web Vitals audit", "LCP optimization", "INP / FID issues", "CLS layout shift", "mobile vs desktop CWV", "per-template CWV breakdown", "real-user CrUX data", "PageSpeed Insights at scale", "field data vs lab data", "p75 metrics". This is the depth specialist — per-template sampling (≥30 URLs per template), per-cohort breakdown (mobile vs desktop, fast vs slow connection), CrUX real-user p75. Beyond marketing-agent's single-URL PageSpeed: this is the at-scale playbook. Recommend remediation to `frontend-engineer` agent.

## Setup

```bash
# Google PageSpeed Insights API v5 — free, 25K queries/day
export PSI_KEY="<from console.cloud.google.com/apis/credentials>"
# Enable PageSpeed Insights API at console.cloud.google.com/apis/library/pagespeedonline.googleapis.com

# Chrome UX Report (CrUX) API — free, no quota documented
export CRUX_KEY="<same console.cloud.google.com project, enable CrUX API>"
# Enable CrUX API at console.cloud.google.com/apis/library/chromeuxreport.googleapis.com

# CrUX BigQuery — free public dataset
# bq query --use_legacy_sql=false 'SELECT * FROM `chrome-ux-report.all.202606` LIMIT 10'
```

Auth requirements:
- `PSI_KEY` — free; enable PageSpeed Insights API
- `CRUX_KEY` — free; enable CrUX API (same GCP project)
- Optional: BigQuery for CrUX historical data

## Common recipes

### Recipe 1: PageSpeed Insights for single URL (mobile + desktop)
```bash
# Mobile (default)
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com/page&strategy=mobile&key=$PSI_KEY&category=performance&category=accessibility&category=best-practices&category=seo"

# Desktop
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com/page&strategy=desktop&key=$PSI_KEY"
```

### Recipe 2: Parse PSI response — CrUX + Lighthouse in one call
```python
import requests

def psi_analyze(url, strategy='mobile'):
    r = requests.get(
        'https://www.googleapis.com/pagespeedonline/v5/runPagespeed',
        params={'url': url, 'strategy': strategy, 'key': PSI_KEY}
    )
    data = r.json()

    return {
        'url': url,
        'strategy': strategy,
        # CrUX field data (real-user p75 from last 28 days)
        'crux': {
            'lcp_ms': data.get('loadingExperience',{}).get('metrics',{}).get('LARGEST_CONTENTFUL_PAINT_MS',{}).get('percentile'),
            'inp_ms': data.get('loadingExperience',{}).get('metrics',{}).get('INTERACTION_TO_NEXT_PAINT',{}).get('percentile'),
            'cls': data.get('loadingExperience',{}).get('metrics',{}).get('CUMULATIVE_LAYOUT_SHIFT_SCORE',{}).get('percentile'),
            'overall': data.get('loadingExperience',{}).get('overall_category'),  # FAST/AVERAGE/SLOW
        },
        # Lab data (simulated, deterministic)
        'lab': {
            'lcp_ms': data['lighthouseResult']['audits']['largest-contentful-paint']['numericValue'],
            'tbt_ms': data['lighthouseResult']['audits']['total-blocking-time']['numericValue'],
            'cls': data['lighthouseResult']['audits']['cumulative-layout-shift']['numericValue'],
            'fcp_ms': data['lighthouseResult']['audits']['first-contentful-paint']['numericValue'],
            'si_ms': data['lighthouseResult']['audits']['speed-index']['numericValue'],
        },
        'performance_score': data['lighthouseResult']['categories']['performance']['score'] * 100,
    }
```

### Recipe 3: Per-template sampling (≥30 URLs per template)
```python
TEMPLATES = {
    'product': ['https://example.com/products/widget-1', 'https://example.com/products/widget-2', ...],  # 30+ URLs
    'category': ['https://example.com/category/electronics', ...],
    'blog': ['https://example.com/blog/post-1', ...],
    'homepage': ['https://example.com/'],
    'pdp': ['https://example.com/products/<various>', ...],
}

import pandas as pd
results = []

for template, urls in TEMPLATES.items():
    for url in urls:
        for strategy in ['mobile','desktop']:
            try:
                r = psi_analyze(url, strategy)
                r['template'] = template
                results.append(r)
            except Exception as e:
                print(f"Failed {url} {strategy}: {e}")
            # Rate limit handling
            time.sleep(0.5)

df = pd.DataFrame(results)
df.to_csv('cwv-per-template.csv', index=False)
```

### Recipe 4: Per-template median aggregation
```python
# Flatten CrUX + lab into top-level columns
df_flat = pd.json_normalize(df.to_dict('records'))

# Per-template medians
agg = df_flat.groupby(['template','strategy']).agg({
    'crux.lcp_ms':'median',
    'crux.inp_ms':'median',
    'crux.cls':'median',
    'lab.lcp_ms':'median',
    'lab.tbt_ms':'median',
    'performance_score':'median'
}).round(2)

print(agg)

# Flag failing templates (Google's CWV thresholds for "Good" rating)
THRESHOLDS = {
    'lcp_ms': 2500,  # > 2500 = "Needs Improvement"; > 4000 = "Poor"
    'inp_ms': 200,
    'cls': 0.1
}

failing = agg[(agg['crux.lcp_ms'] > THRESHOLDS['lcp_ms']) |
              (agg['crux.inp_ms'] > THRESHOLDS['inp_ms']) |
              (agg['crux.cls'] > THRESHOLDS['cls'])]
print(f"Failing templates: {failing.index.tolist()}")
```

### Recipe 5: CrUX API — real-user p75 by URL or origin
```bash
# URL-level CrUX
curl -X POST "https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=$CRUX_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url":"https://example.com/page",
    "formFactor":"PHONE",
    "metrics":["largest_contentful_paint","interaction_to_next_paint","cumulative_layout_shift","first_contentful_paint","experimental_time_to_first_byte"]
  }'

# Origin-level (aggregated across all URLs)
curl -X POST "https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=$CRUX_KEY" \
  -H "Content-Type: application/json" \
  -d '{"origin":"https://example.com","formFactor":"DESKTOP"}'
```

### Recipe 6: CrUX historical via BigQuery (trend analysis)
```sql
-- BigQuery public dataset chrome-ux-report
SELECT
  yyyymm,
  origin,
  effective_connection_type.name AS connection,
  form_factor.name AS device,
  largest_contentful_paint.histogram[OFFSET(0)].density AS lcp_good_density,
  experimental.interaction_to_next_paint.histogram[OFFSET(0)].density AS inp_good_density,
  cumulative_layout_shift.histogram[OFFSET(0)].density AS cls_good_density
FROM
  `chrome-ux-report.materialized.metrics_summary`
WHERE
  yyyymm BETWEEN 202503 AND 202606
  AND origin = 'https://example.com'
ORDER BY yyyymm DESC, device, connection;
```
Returns 15-month trend. Free; queries within BigQuery free tier (1TB/mo).

### Recipe 7: Per-cohort breakdown (device × connection)
```bash
for FORM_FACTOR in PHONE DESKTOP TABLET; do
  for CONN in '"4G"' '"3G"' '"OFFLINE"'; do  # CrUX uses effective_connection_type
    curl -X POST "https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=$CRUX_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"origin\":\"https://example.com\",\"formFactor\":\"$FORM_FACTOR\",\"effectiveConnectionType\":$CONN}" \
      > "crux-$FORM_FACTOR-$CONN.json"
  done
done
```

### Recipe 8: Identify LCP element (lab data)
```python
# Lighthouse "largest-contentful-paint-element" audit reveals which element is the LCP
def get_lcp_element(url, strategy='mobile'):
    r = requests.get('https://www.googleapis.com/pagespeedonline/v5/runPagespeed',
                     params={'url':url,'strategy':strategy,'key':PSI_KEY})
    audits = r.json()['lighthouseResult']['audits']
    lcp_element = audits.get('largest-contentful-paint-element',{}).get('details',{}).get('items',[{}])[0]
    return {
        'node': lcp_element.get('node',{}).get('snippet'),
        'selector': lcp_element.get('node',{}).get('selector'),
        'phase_breakdown': audits.get('lcp-lazy-loaded',{}),
    }
```

### Recipe 9: INP element discovery (interaction-prone elements)
```python
# Lighthouse "interactive" + "max-potential-fid" audits surface INP-risk elements
def get_inp_issues(url, strategy='mobile'):
    r = requests.get('https://www.googleapis.com/pagespeedonline/v5/runPagespeed',
                     params={'url':url,'strategy':strategy,'key':PSI_KEY})
    audits = r.json()['lighthouseResult']['audits']
    return {
        'tbt_ms': audits['total-blocking-time']['numericValue'],
        'long_tasks': audits.get('long-tasks',{}).get('details',{}).get('items',[]),
        'main_thread_work': audits.get('mainthread-work-breakdown',{}).get('details',{}).get('items',[]),
        'unused_js': audits.get('unused-javascript',{}).get('details',{}).get('items',[])[:5],
    }
```

### Recipe 10: CLS element identification
```python
# "cumulative-layout-shift" audit details show the actual shifting elements
def get_cls_culprits(url, strategy='mobile'):
    r = requests.get('https://www.googleapis.com/pagespeedonline/v5/runPagespeed',
                     params={'url':url,'strategy':strategy,'key':PSI_KEY})
    audits = r.json()['lighthouseResult']['audits']
    cls = audits.get('cumulative-layout-shift',{}).get('details',{}).get('items',[])
    return [{'selector': item.get('node',{}).get('selector'),
             'snippet': item.get('node',{}).get('snippet'),
             'score': item.get('score')} for item in cls]
```

### Recipe 11: Output remediation brief for frontend-engineer
```python
# Aggregate findings into actionable brief
brief = {
    'site': 'example.com',
    'audit_date': '2026-06-09',
    'failing_templates': failing.index.tolist(),
    'critical_issues': []
}

# Per template, identify the worst metric + culprit
for template in failing.index:
    template_urls = TEMPLATES[template[0]]
    sample_url = template_urls[0]

    lcp_elem = get_lcp_element(sample_url)
    inp_issues = get_inp_issues(sample_url)
    cls_culprits = get_cls_culprits(sample_url)

    brief['critical_issues'].append({
        'template': template,
        'sample_url': sample_url,
        'lcp_element': lcp_elem,
        'inp_long_tasks': inp_issues['long_tasks'][:5],
        'cls_elements': cls_culprits[:5],
        'recommendation': '<auto-generated based on common patterns>',
    })

# Output to Notion via notion-mcp for handoff
```

### Recipe 12: Mobile-first audit (Googlebot Smartphone perspective)
```bash
# Mobile CWV is what Google ranks on (mobile-first indexing since 2023)
# Always strategy=mobile for ranking-relevant analysis
# Desktop only for desktop-specific UX issues
```

## Examples

### Example 1: Full CWV audit for e-comm site (4 templates, 30 URLs each)
**Goal:** Quantify CWV per template; identify worst-performing template; output remediation brief.

**Steps:**
1. Recipe 3: PSI calls for 4 templates × 30 URLs × 2 strategies = 240 calls (~2 hours respecting rate limit).
2. Recipe 4: per-template median aggregation.
3. Identify failing templates (LCP > 2500ms mobile, INP > 200ms, CLS > 0.1).
4. Recipe 5 + 6: CrUX per-template trend → confirm long-term pattern.
5. Recipe 8-10: per-URL culprit identification.
6. Recipe 11: brief for `frontend-engineer`.

**Result:** Prioritized remediation plan; expected CWV pass-rate uplift.

### Example 2: CrUX BigQuery trend analysis
**Goal:** Has CWV degraded over last 6 months?

**Steps:**
1. Recipe 6: BigQuery query for last 6 months.
2. Compare current vs 6-month-ago p75.
3. If degradation: cross with deploy log → which release introduced it.

**Result:** Time-series chart + root-cause hypothesis.

### Example 3: Pre-launch CWV gate for new feature
**Goal:** Block deploy if CWV regresses on PDP template.

**Steps:**
1. Run Recipe 3 baseline before deploy → save medians.
2. Deploy to staging.
3. Re-run on staging URLs → compare to baseline.
4. If median LCP > baseline × 1.1: block deploy; otherwise pass.
5. Codify as CI gate via Lighthouse CI (see `lighthouse-ci-gtmetrix-webpagetest-perf` skill).

**Result:** No regressions ship.

## Edge cases / gotchas

- **CrUX field data lags 28 days** — today's CrUX p75 reflects last 28 days. Recent changes invisible until window rolls.
- **Lab data deterministic but ≠ real-user** — Lighthouse simulates Slow 4G. Real users on Wi-Fi see better LCP. Use CrUX for ranking-relevant.
- **CrUX availability requires traffic** — origins/URLs with insufficient Chrome user traffic (< ~1000/mo) get empty CrUX response.
- **PSI rate limit 25K/day** — usually plenty, but at 5K-URL scan = consider rate limiting at 0.5-1s/request to avoid 429.
- **`strategy=mobile` default** — desktop CWV no longer used for ranking (mobile-first since 2023). Default to mobile.
- **INP replaced FID March 2024** — old FID data deprecated; track INP only going forward.
- **CLS aggressive threshold** — 0.1 is "Good", 0.25 is "Needs Improvement". Be strict.
- **LCP for SPAs (route changes)** — for SPA route changes, LCP measures the initial page load; subsequent navigations not part of CWV.
- **Cookie banners cause CLS** — almost universal CLS cause. Solution: reserve banner space with min-height OR delay other content render.
- **Image dimensions missing = CLS** — always set explicit width/height on `<img>` and `<video>`.
- **Web fonts cause FCP/LCP delay** — preload critical fonts + `font-display:swap`.
- **3rd-party scripts dominant INP cause** — chat widgets, analytics, ad scripts. Defer or async where possible.
- **CrUX BigQuery refresh monthly** — data lands 2nd Tuesday of each month for prior month.
- **Origin-level vs URL-level CrUX** — origin aggregates all URLs; URL-level requires sufficient per-URL traffic. Most pages won't have URL-level data.

## Sources

- [Google Search Central — Core Web Vitals](https://developers.google.com/search/docs/appearance/core-web-vitals)
- [PageSpeed Insights API v5 docs](https://developers.google.com/speed/docs/insights/v5/get-started)
- [CrUX API documentation](https://developer.chrome.com/docs/crux/api)
- [CrUX BigQuery dataset](https://developer.chrome.com/docs/crux/bigquery)
- [web.dev — LCP optimization](https://web.dev/articles/optimize-lcp)
- [web.dev — INP optimization](https://web.dev/articles/optimize-inp)
- [web.dev — CLS optimization](https://web.dev/articles/optimize-cls)
- [web.dev — INP replacing FID announcement](https://web.dev/blog/inp-cwv-march-12)
- [Google — mobile-first indexing complete](https://developers.google.com/search/blog/2023/10/mobile-first-indexing-complete)
