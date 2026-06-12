<!--
Source: https://vwo.com/landing-page-optimization/
Source: https://developers.google.com/speed/docs/insights/v5/about
Landing page coordination: message match + PageSpeed + VWO/Hotjar/Maze handoff.
-->
# Landing Page CRO Coordination — SKILL

The ad-to-landing-page handoff makes or breaks ROAS. **Message match** between ad headline and LP H1 is the #1 LP conversion driver. **PageSpeed** below 2.5s LCP adds 30%+ bounce. CRO execution itself defers to `marketing-agent` (VWO / Hotjar / Maze) — this skill ships the message-match brief, the pre-launch PageSpeed audit, and the hand-off path.

## When to use this skill

- **Pre-scale audit** — verify LP ready for ad spend before scaling.
- **New campaign launch** — ensure dedicated LP exists per concept.
- **Message-match audit** — ad headline ↔ LP H1 ↔ first paragraph alignment.
- **Mobile LP check** — 70%+ paid traffic is mobile; viewport test.
- **PageSpeed regression** — LP got slower; bounce rate climbed.
- **CRO experiment proposal** — author hypothesis + send to marketing-agent.

**Do NOT use this skill when:**
- LP build (defer to `frontend-engineer`).
- A/B test execution on LP (defer to `marketing-agent` via VWO / GrowthBook).
- Copy iteration (defer to `marketing-agent` Vale + brand voice).

## Setup

### Tools

- **PageSpeed Insights API** — `https://www.googleapis.com/pagespeedonline/v5/runPagespeed`
- **playwright-mcp** — mobile viewport screenshot + interaction
- **browserbase-mcp** — remote browser for full session capture
- **VWO** — paid CRO platform (cross-grep marketing-agent)
- **Hotjar** — heatmap + session replay (cross-grep)
- **Maze** — UX testing (cross-grep)
- **GrowthBook** — feature flags + experiments (via marketing-agent)

### Core Web Vitals 2026 SOTA targets

| Metric | Good | Needs work | Poor |
|---|---|---|---|
| LCP (Largest Contentful Paint) | <2.5s | 2.5-4.0s | >4.0s |
| INP (Interaction to Next Paint) | <200ms | 200-500ms | >500ms |
| CLS (Cumulative Layout Shift) | <0.1 | 0.1-0.25 | >0.25 |

Below "Good" → quality score suffers + bounce rises 20-40%.

### Message match checklist

```yaml
ad_creative:
  headline: "20% off skincare this weekend"
  body: "Free shipping over $50. 30K customers love us."
  cta: "Shop now"

landing_page:
  h1: "20% off skincare — this weekend only"   # MUST mirror ad headline
  hero_subheader: "Free shipping over $50"     # echoes ad body
  social_proof_above_fold: "Loved by 30K customers — 4.9 stars"   # mirrors body proof
  cta_button_text: "Shop now"                   # mirrors ad CTA
  destination: matches utm_content for tracking
```

## Common recipes

### Recipe 1: PageSpeed Insights API — single URL

```bash
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?\
url=https://brand.com/lp/q3-promo&\
strategy=mobile&\
category=PERFORMANCE&\
category=ACCESSIBILITY&\
category=BEST_PRACTICES&\
key=$PAGESPEED_API_KEY" \
  | jq '{
    lcp: .lighthouseResult.audits["largest-contentful-paint"].displayValue,
    inp: .lighthouseResult.audits["interaction-to-next-paint"].displayValue,
    cls: .lighthouseResult.audits["cumulative-layout-shift"].displayValue,
    performance_score: .lighthouseResult.categories.performance.score
  }'
```

### Recipe 2: Bulk PageSpeed audit across all active LPs

```python
import requests, os
from concurrent.futures import ThreadPoolExecutor

# Pull all active LP URLs from Meta
ads = mcp_call("meta-ads.list_ads", {"status": "ACTIVE"})
urls = list(set(a["creative"]["object_story_spec"]["link_data"]["link"] for a in ads if a.get("creative")))

def check(url):
    r = requests.get("https://www.googleapis.com/pagespeedonline/v5/runPagespeed", params={
      "url": url, "strategy": "mobile", "category": "PERFORMANCE",
      "key": os.environ["PAGESPEED_API_KEY"]})
    a = r.json()["lighthouseResult"]["audits"]
    return {
      "url": url,
      "lcp_ms": a["largest-contentful-paint"]["numericValue"],
      "inp_ms": a.get("interaction-to-next-paint",{}).get("numericValue", 0),
      "cls": a["cumulative-layout-shift"]["numericValue"],
      "score": r.json()["lighthouseResult"]["categories"]["performance"]["score"]
    }

with ThreadPoolExecutor(max_workers=5) as ex:
    results = list(ex.map(check, urls))

# Flag slow LPs
slow = [r for r in results if r["lcp_ms"] > 2500]
for r in slow:
    print(f"P0 PageSpeed: {r['url']} LCP={r['lcp_ms']/1000:.1f}s")
```

### Recipe 3: Mobile viewport screenshot via playwright-mcp

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    for url in lp_urls:
        # iPhone 14 mobile viewport
        ctx = browser.new_context(
          viewport={"width": 390, "height": 844},
          user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
          device_scale_factor=3
        )
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle")
        page.screenshot(path=f"lp-mobile-{url.replace('/','_')}.png", full_page=True)
        ctx.close()
```

### Recipe 4: Message-match audit — ad vs LP

```python
# Pull ad copy + LP destination
import requests
from bs4 import BeautifulSoup

ads = mcp_call("meta-ads.list_ads", {"status": "ACTIVE", "fields": ["id","name","creative"]})

mismatches = []
for a in ads:
    if not a.get("creative"): continue
    ad_headline = a["creative"]["object_story_spec"]["link_data"]["name"]
    ad_body = a["creative"]["object_story_spec"]["link_data"]["message"]
    lp_url = a["creative"]["object_story_spec"]["link_data"]["link"]
    
    lp_html = requests.get(lp_url).text
    soup = BeautifulSoup(lp_html, "html.parser")
    lp_h1 = soup.find("h1").get_text(strip=True) if soup.find("h1") else ""
    
    # Naive overlap check (improve with semantic similarity if needed)
    ad_words = set(ad_headline.lower().split())
    lp_words = set(lp_h1.lower().split())
    overlap = len(ad_words & lp_words) / max(len(ad_words), 1)
    
    if overlap < 0.3:
        mismatches.append({"ad_id": a["id"], "ad": ad_headline, "lp_h1": lp_h1, "overlap_pct": overlap*100, "lp_url": lp_url})

import json
print(json.dumps(mismatches, indent=2))
```

### Recipe 5: CRO experiment proposal to marketing-agent

```yaml
# Brief sent to marketing-agent for VWO / GrowthBook execution
experiment_proposal:
  page: https://brand.com/lp/q3-promo
  current_conversion_rate: 2.3%
  hypothesis: |
    Adding social proof element above-fold ("30K customers, 4.9★") 
    will lift CR by 0.5-1.0 absolute percentage points by reducing 
    new-visitor distrust.
  test_design:
    variants:
      - control: current page (no social proof above fold)
      - variant_A: trust badge + customer count
      - variant_B: trust badge + customer count + 1-line testimonial
    sample_size_per_variant: 5000 (power analysis at p<0.05, 80% power)
    duration: 14 days
    primary_metric: conversion_rate (form submit OR purchase)
  hand_off_to: marketing-agent
  execution_tool: VWO (or GrowthBook if available)
  reporting_back: weekly until significance
```

### Recipe 6: Pre-launch checklist

```python
# Run before allowing spend > $100/day on an LP
def pre_launch_check(lp_url):
    issues = []
    
    # 1. PageSpeed
    ps = pagespeed_check(lp_url)
    if ps["lcp_ms"] > 2500: issues.append(f"LCP {ps['lcp_ms']}ms > 2500 target")
    if ps["inp_ms"] > 200: issues.append(f"INP {ps['inp_ms']}ms > 200 target")
    if ps["cls"] > 0.1: issues.append(f"CLS {ps['cls']} > 0.1 target")
    
    # 2. Mobile viewport
    mobile_screenshot = capture_mobile(lp_url)
    if has_horizontal_scroll(mobile_screenshot): issues.append("Mobile horizontal scroll detected")
    
    # 3. Conversion goal fires
    test_event = simulate_purchase(lp_url)
    if not test_event["pixel_fired"]: issues.append("Meta pixel not firing on conversion")
    if not test_event["capi_received"]: issues.append("CAPI event not received")
    if not test_event["ga4_event"]: issues.append("GA4 event not logged")
    
    # 4. Trust signals above fold
    soup = parse_html(lp_url)
    if not has_trust_signal(soup): issues.append("No trust signal above fold (testimonial / badge / star rating)")
    
    # 5. Single CTA
    cta_count = count_cta(soup)
    if cta_count > 2: issues.append(f"{cta_count} CTAs above fold — should be 1 primary")
    
    return issues
```

### Recipe 7: Heatmap delegate to marketing-agent (Hotjar)

```bash
# Trigger Hotjar recording start (deferred via marketing-agent)
# This skill just authors the brief:
cat > hotjar-recording-brief.yaml <<EOF
page: https://brand.com/lp/q3-promo
recording_duration: 14d (or 1000 sessions)
heatmap_types: [click, move, scroll]
funnel_to_track: 
  - landing
  - cta_click  
  - checkout_complete
filter:
  - device: mobile
  - source: paid (utm_medium=paid)
hand_off_to: marketing-agent
EOF
```

### Recipe 8: LP per concept — dedicated URL convention

```
https://brand.com/lp/{campaign_concept}/?utm_source=meta&utm_medium=paid&utm_campaign={campaign_slug}&utm_content={cell_id}
```

Examples:
- `/lp/founder-story/` — founder-UGC concept
- `/lp/before-after/` — result-driven concept
- `/lp/price-anchor/` — discount-led concept

Each LP has its own message match optimized to its concept.

## Examples — pre-launch audit report

```markdown
# Landing Page Pre-Launch Audit — Q3 Promo LP

URL: https://brand.com/lp/q3-promo

## PageSpeed (mobile)
- LCP: 3.2s (FAIL — target <2.5s)
- INP: 145ms (PASS)
- CLS: 0.08 (PASS)
- Performance score: 67/100 (FAIL — target 90+)

## Action: 
- Compress hero image (currently 2.3MB → target 200KB)
- Defer non-critical JS (Klaviyo, Mouseflow)
- Preload hero font

## Message match
- Ad headline: "20% off skincare this weekend"
- LP H1: "Save big on skincare this week"  (PARTIAL match)
- Overlap: 50% (target 70%+)

## Action: 
- Update LP H1 to "20% off skincare — this weekend only"

## Mobile viewport
- iPhone 14: horizontal scroll detected on review section (FAIL)

## Action: 
- Fix review carousel CSS for max-width: 100vw

## Conversion tracking
- Meta pixel: firing OK
- CAPI: NOT receiving event_id (dedup broken)
- GA4: firing OK

## Action: 
- Fix GTM-S template to forward event_id

## Trust signals above fold
- Star rating: present ✓
- Customer count: present ("30K customers") ✓
- Testimonial: NOT present ✗

## Action (P2): 
- Add 1-line testimonial near hero CTA

## Single CTA
- 3 CTAs above fold ("Shop now", "Newsletter", "Free guide")

## Action: 
- Remove "Newsletter" and "Free guide" CTAs from above fold

## Verdict
- BLOCKED for scale until P0 fixes (PageSpeed + Message match + CAPI)
- Once P0 fixed: $200/day cap until tested 7d, then re-evaluate
```

## Edge cases

### LCP element is hero image
Largest element on most LPs is the hero. Optimize: WebP/AVIF format, srcset for responsive sizes, preload critical version, lazy-load below-fold.

### Single-page-app (SPA) routes
SPA LCP measured per route. Make sure first-paint route is the LP, not loading skeleton.

### Above-fold = first 100vh on mobile
Mobile viewport varies. Use 100vh as proxy. Test on real iPhone 14 / Pixel 8 via playwright.

### Dynamic CTA text
A/B testing CTA text: keep variants in scope. Avoid 5 different CTAs being tested simultaneously without significance.

### Localized LPs
Multi-market: per-language LP at `/lp/{lang}/{concept}/`. Same audit applies per language.

### Single CTA exception — shopping carousel
Product carousel LP has many "buy" CTAs by definition. Different rule: one CATEGORY of action (purchase), not literally one button.

### Form vs e-com LP
Form LP: single CTA = "Submit". E-com LP: "Add to cart" + "Buy now" both acceptable but call out the primary.

### CRO defer to marketing-agent
Don't run experiments directly. Author brief → marketing-agent executes via VWO / GrowthBook / Hotjar / Maze.

### Tracking pixel placement
Conversion events must fire on actual conversion page (thank-you page), not the LP itself. Verify the pixel/CAPI fire on the post-conversion redirect.

### Above-fold trust signal hierarchy
Best: customer count + star rating + 1-line testimonial. OK: customer count + star rating. Min: customer count.

### Mobile-first design check
Open in Chrome DevTools mobile view + actual phone. Don't trust desktop emulation alone.

### LP testing window
A/B test for 14 days minimum to wash daily seasonality. Below 1000 visitors per variant → not enough data.

## Sources

- VWO landing page optimization: https://vwo.com/landing-page-optimization/
- Google PageSpeed Insights API: https://developers.google.com/speed/docs/insights/v5/about
- Web Vitals targets: https://web.dev/articles/vitals
- Lighthouse audits: https://developer.chrome.com/docs/lighthouse/overview
- Hotjar heatmaps: https://www.hotjar.com/
- Maze UX testing: https://maze.co/
- GrowthBook feature flags: https://docs.growthbook.io/
- Message match research: https://unbounce.com/landing-page-optimization/message-match/
- Above-the-fold best practices: https://cxl.com/blog/above-the-fold/
- Google Core Web Vitals: https://web.dev/articles/vitals
