<!--
Sources: Visualping https://visualping.io/
         ChangeTower https://changetower.com/
         Autobound CI tools 2026 https://www.autobound.ai/blog/top-15-competitive-intelligence-tools-2026
Companion playbook: role.md → "Continuous monitoring playbook"
-->

# Competitor messaging tracking + diff over time

Weekly snapshot of competitor homepage + top 5 LPs + value-prop copy. Diff against prior snapshot. Classify shift as: positioning (new ICP), claims (new metric/proof), pricing-adjacent (new bundle), category-language. Stash time-series so re-positioning detectable across quarters.

## When to use

- "Has Acme repositioned this quarter?"
- "Did Beta shift to enterprise messaging?"
- "Track Acme's hero claim weekly"
- Pre-launch positioning calibration (where's the air?)
- After a competitor exec change (often coincides with messaging reset)

## When NOT to use

- Pricing-only change → use `competitor-pricing-page-visualping-distill`
- Ad-creative tracking → use `competitor-ad-pathmatics-spyfu-semrush`
- Single LP teardown depth → use `competitor-product-teardown-depth`

## Setup

```bash
# Visualping (free 5 monitors; $13/mo+)
export VISUALPING_API_KEY="..."

# ChangeTower (audit-friendly $79+/mo)
export CHANGETOWER_API_KEY="..."

# Python for diff + classify
uv pip install requests beautifulsoup4 difflib2 anthropic

# Anthropic for classification
export ANTHROPIC_API_KEY="sk-ant-..."
```

MCPs in `agent.yaml`: `firecrawl-mcp`, `playwright-mcp`, `markdown-converter`, `slack-mcp`, `gmail-mcp`.

## Common recipes

### Recipe 1: Visualping monitor on homepage

```bash
curl -X POST https://api.visualping.io/v1/jobs \
  -H "Authorization: Bearer $VISUALPING_API_KEY" \
  -d '{
    "url": "https://acme.example.com",
    "frequency_minutes": 10080,
    "selector": "main",
    "ignore_selector": ".footer, .cookie-banner",
    "webhook_url": "https://hooks.slack.com/services/..."
  }'
```

Weekly cadence (10080 min = 7 days); `ignore_selector` cuts noise.

### Recipe 2: Per-competitor LP list

```yaml
# messaging.yaml
competitors:
  acme:
    pages:
      - url: https://acme.example.com
        kind: homepage
      - url: https://acme.example.com/product
        kind: product-overview
      - url: https://acme.example.com/use-cases/sales
        kind: use-case-LP
      - url: https://acme.example.com/use-cases/marketing
        kind: use-case-LP
      - url: https://acme.example.com/customers/enterprise
        kind: segment-LP
```

### Recipe 3: Snapshot via firecrawl-mcp

```python
from firecrawl import FirecrawlApp
fc = FirecrawlApp(api_key=os.environ["FIRECRAWL_API_KEY"])
out = fc.scrape_url("https://acme.example.com",
                    params={"formats":["markdown"], "onlyMainContent":True})
md = out["data"]["markdown"]
# Save to snapshots/acme/homepage-2026-06-11.md
```

### Recipe 4: Extract messaging elements

```python
from bs4 import BeautifulSoup
import requests
html = requests.get("https://acme.example.com").text
soup = BeautifulSoup(html, "html.parser")
hero_h1 = soup.select_one("h1").get_text(strip=True)
hero_sub = soup.select_one("h1 + p, h1 + h2").get_text(strip=True) if soup.select_one("h1 + p, h1 + h2") else ""
ctas = [a.get_text(strip=True) for a in soup.select("a.cta, button.cta")]
social_proof = [el.get_text(strip=True) for el in soup.select(".testimonial, .logo-wall img")]
```

### Recipe 5: Diff snapshots

```python
import difflib, pathlib
prev = pathlib.Path("snapshots/acme/homepage-2026-w22.md").read_text()
curr = pathlib.Path("snapshots/acme/homepage-2026-w23.md").read_text()
diff = "\n".join(difflib.unified_diff(prev.splitlines(), curr.splitlines(),
                                       fromfile="w22", tofile="w23", lineterm=""))
```

### Recipe 6: LLM classification pass

```python
import anthropic
client = anthropic.Anthropic()
prompt = f"""Classify this diff into messaging shift categories. Output JSON:
{{
  "shift_kind": "positioning|claims|pricing-adjacent|category-language|none",
  "summary": "<1 sentence>",
  "evidence": ["<verbatim line>", "..."],
  "impact": "low|medium|high"
}}

POSITIONING = changed ICP / segment / job-to-be-done framing
CLAIMS = new metric / proof / case-study / customer-count change
PRICING-ADJACENT = new bundle name / "starts at $X" / free-tier shift
CATEGORY-LANGUAGE = new category positioning (e.g., from "BI tool" → "AI analytics platform")

Diff:
{diff}
"""
resp = client.messages.create(model="claude-sonnet-4-5-20250929",
    max_tokens=1000, messages=[{"role":"user","content":prompt}])
classification = json.loads(resp.content[0].text)
```

### Recipe 7: Time-series messaging log

```yaml
# messaging-history.yaml — append-only
- competitor: acme
  page: homepage
  ts: 2026-06-11
  shift_kind: positioning
  summary: "Re-positioned from 'analytics for product teams' to 'AI insights for revenue teams'"
  evidence: ["AI insights for revenue teams"]
  impact: high
  snapshot_url: snapshots/acme/homepage-2026-w23.md
- competitor: acme
  page: homepage
  ts: 2026-05-15
  shift_kind: claims
  summary: "Added 'Trusted by 10,000+ teams'"
  evidence: ["Trusted by 10,000+ teams"]
  impact: low
```

### Recipe 8: Weekly digest synthesis

```python
import yaml
hist = yaml.safe_load(open("messaging-history.yaml"))
week = [h for h in hist if h["ts"] >= "2026-06-04"]
# Group by competitor; rank by impact
```

### Recipe 9: Hero-element archival

Capture hero copy weekly:

```python
import json, pathlib
archive = pathlib.Path("archive/acme/hero.jsonl")
archive.parent.mkdir(parents=True, exist_ok=True)
with archive.open("a") as f:
    f.write(json.dumps({"ts":"2026-06-11","h1":hero_h1,"sub":hero_sub,"ctas":ctas}) + "\n")
```

Quarterly: read the JSONL, see when claims first appeared / disappeared.

### Recipe 10: Category-language tracker

Pre-define category terms; count their frequency across pages weekly:

```python
terms = ["AI","BI","analytics","insights","data platform","data fabric","data mesh"]
counts = {t: html.lower().count(t.lower()) for t in terms}
# Track shift over time — when "data mesh" drops out and "AI insights" peaks, category-language shift
```

### Recipe 11: playwright-mcp for JS-rendered LP

```python
# Some hero copy is JS-rendered; use Playwright instead of plain HTML
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    page = p.chromium.launch().new_page()
    page.goto("https://acme.example.com")
    page.wait_for_load_state("networkidle")
    text = page.locator("main").inner_text()
```

## Examples

### Example 1: Weekly messaging-diff for 3 competitors

**Goal:** Surface positioning shifts within 24 hours.

**Steps:**
1. Author `messaging.yaml` with 5 pages per competitor (Recipe 2).
2. Visualping monitors on each (Recipe 1).
3. On webhook fire: Recipe 3 scrape → Recipe 5 diff → Recipe 6 classify.
4. Append to `messaging-history.yaml` (Recipe 7).
5. Friday digest (Recipe 8) → Slack + email.

**Result:** Material positioning shifts caught within 1 week; trend visible quarterly.

### Example 2: Pre-launch positioning calibration

**Goal:** Before our launch, find empty messaging space.

**Steps:**
1. Pull last 8 weeks of messaging-history.yaml across 5 competitors.
2. LLM cluster: where are they crowding? What category-language terms are saturated?
3. Identify empty positioning space (categories none of them claim).
4. Recommend positioning + hero-copy directions to PMM.

**Result:** Positioning brief grounded in actual competitor messaging.

## Edge cases / gotchas

- **A/B-tested hero copy** — competitor shows different headlines to different traffic. Scrape from 3 IPs (use `brightdata-mcp` proxy) over 3 days before declaring a shift.
- **Cookie banners** — `ignore_selector` is critical or you get diff noise weekly.
- **CMS rebuild noise** — competitor restructures DOM; diff shows everything changed but content didn't. Use `markdown-converter` for prose-only diff that's structure-resilient.
- **Time-zone drift** — Visualping captures in UTC; weekly cadence may drift over months. Use cron rather than relative schedules for canonical Friday-9am snapshots.
- **Press release ≠ messaging** — competitor presses an "AI Analytics" badge for a one-off campaign; their homepage doesn't update. Capture only homepage + key LPs as canonical.
- **LP retired** — competitor removes an LP; Visualping starts 404-ing. Add page-health check.
- **Personalization** — geo-personalized hero (US sees one, EU another). Force `Accept-Language` + IP region; or capture both.
- **Internal LP for paid traffic only** — sometimes `/lp/campaign-xyz` is only reachable via ad click. Discover via SEMrush Top Pages (paid) or skip.
- **Don't conflate refresh with reposition** — a homepage redesign with same positioning ≠ messaging shift. Classify as "design refresh" + skip.
- **Quarterly canonical** — week-by-week noise; quarterly grain is what PMM acts on. Surface both grains in the digest.

## Sources

- Visualping — https://visualping.io/
- ChangeTower — https://changetower.com/
- UptimeRobot — 9 Best Website Change Monitoring 2026 — https://uptimerobot.com/knowledge-hub/monitoring/9-best-website-change-monitoring-tools-compared/
- Autobound — CI Tools Compared 2026 — https://www.autobound.ai/blog/top-15-competitive-intelligence-tools-2026
- role.md → "Continuous monitoring playbook" (this bundle)

## Related skills

- `competitor-pricing-page-visualping-distill` — pricing-page focused diff
- `continuous-competitor-monitoring-klue-kompyte-crayon` — broader signal fan-out
- `battlecard-authoring-maintenance` — positioning shift → pane 1 refresh trigger
- `feature-parity-tracking` — new claim often pairs with new feature
- `competitor-ad-pathmatics-spyfu-semrush` — paid messaging often leads website
