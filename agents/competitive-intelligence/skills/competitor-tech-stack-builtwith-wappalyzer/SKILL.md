<!--
Sources: BuiltWith https://builtwith.com/
         Wappalyzer https://www.wappalyzer.com/
         python-Wappalyzer https://github.com/chorsley/python-Wappalyzer
         BuiltWith vs Wappalyzer comparison https://prospeo.io/s/builtwith-vs-wappalyzer
         DetectZeStack https://detectzestack.com/
         Apify Tech Stack Detector https://apify.com/store/categories/tech-stack
Companion playbook: role.md → SOTA tool reference → BuiltWith / Wappalyzer / DetectZeStack
-->

# Competitor tech stack monitoring (BuiltWith / Wappalyzer / DetectZeStack)

Detect competitor frontend + backend + integration stack and changes over time. BuiltWith for market-scale + historical depth (414M domain index); Wappalyzer for browse-time fingerprint accuracy; DetectZeStack for 60-90x cheaper API; python-Wappalyzer for self-hosted; Apify Tech Stack Detector for pay-per-event. Track: JS framework, CMS, analytics, payment, CDN, A/B test infra, CDP, marketing automation, observability. Surface "they switched from Segment to RudderStack" as a signal.

## When to use

- "What's [competitor]'s tech stack?"
- "Did they switch from Segment to RudderStack?"
- "Which competitors are running on Vercel / Cloudflare / AWS?"
- Diff competitor's analytics + observability stack over quarters
- Pre-deal: tech-stack overlap signal for migration story
- Filter prospect list by tech ("companies running Segment + Salesforce")
- Build feature-parity matrix's "infra" row

## When NOT to use

- Hiring-driven stack inference → use `competitor-hiring-intel-linkedin-sales-nav` (Recipe 5)
- In-product feature inventory → use `competitor-product-teardown-depth`
- API endpoint reverse-engineering → out of scope
- Mobile SDK stack → use `competitor-app-intel-sensor-tower-data-ai`

## Setup

```bash
# BuiltWith Basic API $295/mo; Team $995+/mo for full
export BUILTWITH_API_KEY="..."

# Wappalyzer paid API (from $450/mo)
export WAPPALYZER_API_KEY="..."

# DetectZeStack (60-90x cheaper; $15/mo for 25k requests)
export DETECTZESTACK_API_KEY="..."

# python-Wappalyzer (free, self-hosted)
# pip install python-Wappalyzer requests-html

# Apify Tech Stack Detector (pay-per-event)
export APIFY_TOKEN="..."

# Firecrawl for DOM / headers fallback (free tier)
export FIRECRAWL_API_KEY="..."
```

MCPs in `agent.yaml`: `firecrawl-mcp`, `playwright-mcp`, `cli-anything`, `slack-mcp`, `notion-mcp`.

## Common recipes

### Recipe 1: BuiltWith — full tech profile

```bash
# Single domain full profile (Basic + Team plans)
curl "https://api.builtwith.com/v21/api.json?KEY=$BUILTWITH_API_KEY&LOOKUP=acme.example.com" \
  | jq '.Results[].Result.Paths[].Technologies[]
        | {Name, Tag, FirstDetected, LastDetected}'
```

Returns: each tech with Tag (`analytics`, `cdn`, `framework`, `cms`, `marketing-automation`, ...), first detected timestamp, last detected timestamp.

### Recipe 2: BuiltWith — domain-history endpoint

```bash
# When did Acme switch from GA4 to Mixpanel?
curl "https://api.builtwith.com/free1/api.json?KEY=$BUILTWITH_API_KEY&LOOKUP=acme.example.com" \
  | jq '.Results[].Result.Paths[].Technologies[]
        | select(.Name == "Mixpanel" or .Name == "Google Analytics 4")
        | {Name, FirstDetected, LastDetected}'
```

### Recipe 3: BuiltWith — find sites using a tech (prospect-list builder)

```bash
# All companies in your TAM running Snowflake + dbt
curl -X POST "https://api.builtwith.com/lists7/api.json" \
  -H "Content-Type: application/json" \
  -d '{
    "KEY": "'"$BUILTWITH_API_KEY"'",
    "TECH": "Snowflake,dbt",
    "META": true,
    "GEO": "US"
  }'
```

Use to build the comp-set's customer-base inference (which companies use both their stack + ours).

### Recipe 4: python-Wappalyzer fingerprint (free, self-hosted)

```python
from Wappalyzer import Wappalyzer, WebPage
w = Wappalyzer.latest()
page = WebPage.new_from_url("https://acme.example.com")
detected = w.analyze_with_versions_and_categories(page)
# Returns: {'React': {'versions': ['18.2.0'], 'categories': ['JavaScript Frameworks']}, ...}
print(detected)
```

Free, accurate for client-side detection (frontend frameworks, analytics tags, fonts).

### Recipe 5: DetectZeStack — 60-90x cheaper API alternative

```bash
curl -H "Authorization: Bearer $DETECTZESTACK_API_KEY" \
  "https://api.detectzestack.com/v1/lookup?domain=acme.example.com"
```

Layers: Wappalyzer-style fingerprint + DNS CNAME (Cloudflare? AWS CloudFront?) + TLS issuer + custom headers (e.g., `X-Powered-By`).

### Recipe 6: Apify Tech Stack Detector (pay-per-event)

```bash
curl -X POST "https://api.apify.com/v2/acts/apify~tech-stack-detector/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "startUrls": [{"url":"https://acme.example.com"}],
    "maxResults": 1
  }'
```

### Recipe 7: DNS + TLS detection (free, manual)

```bash
# CDN / hosting inference
dig CNAME www.acme.example.com +short  # cloudflare-dnssec.com → Cloudflare
host acme.example.com                  # IP → reverse → AWS / GCP / Fastly
# TLS issuer
echo | openssl s_client -connect acme.example.com:443 -servername acme.example.com 2>/dev/null \
  | openssl x509 -noout -issuer
# Custom headers (server-side)
curl -sI https://acme.example.com | grep -iE 'server|x-powered|via|x-cdn'
```

### Recipe 8: Per-competitor stack snapshot (YAML)

```yaml
# data/tech-stack/acme.yaml
competitor: acme-corp
snapshot_date: 2026-06-11
sources:
  - tool: builtwith
    asof: 2026-06-10
  - tool: python-wappalyzer
    asof: 2026-06-11
detected:
  frontend:
    framework: Next.js 14
    css: Tailwind v3
    bundler: turbo
  hosting:
    cdn: Cloudflare
    edge: Vercel
  analytics:
    product: Mixpanel
    marketing: GA4 + Segment
  cdp: Segment
  ab_test: Statsig
  observability: Datadog
  payments: Stripe
  ci_cd: GitHub Actions (inferred from job posts)
  ml_infra: AWS SageMaker (inferred from job posts)
```

### Recipe 9: Diff stack snapshot week-over-week

```python
import yaml, deepdiff
prior = yaml.safe_load(open("data/tech-stack/acme-2026-06-04.yaml"))
curr  = yaml.safe_load(open("data/tech-stack/acme-2026-06-11.yaml"))
delta = deepdiff.DeepDiff(prior["detected"], curr["detected"])
# Returns: {'values_changed': {"root['cdp']": {"old_value":"Segment","new_value":"RudderStack"}}}
```

### Recipe 10: Slack signal on stack switch

```python
import requests
def notify_stack_switch(competitor, category, prior, curr):
    requests.post(SLACK_WEBHOOK_URL, json={
        "text": f":wrench: {competitor} switched {category}: *{prior}* -> *{curr}*",
        "channel": "#ci-hotline",
    })
```

### Recipe 11: Build per-category competitor matrix

```python
import pandas as pd
competitors = ["acme","beta","gamma","delta","epsilon"]
categories  = ["frontend","cdp","observability","ab_test","payments","cdn"]
matrix = pd.DataFrame(index=competitors, columns=categories)
for c in competitors:
    snap = yaml.safe_load(open(f"data/tech-stack/{c}.yaml"))
    for cat in categories:
        matrix.at[c, cat] = snap["detected"].get(cat) or snap["detected"].get(cat.replace("_", "/"))
matrix.to_csv("competitor_stack_matrix.csv")
```

### Recipe 12: Cross-reference with hiring signal

If `competitor-hiring-intel-linkedin-sales-nav` Recipe 5 found "Acme hiring 6 Rust + 5 ClickHouse roles," cross-check Recipe 1 BuiltWith for already-deployed Rust/CH. If absent in BuiltWith but rising in hiring → forward-leaning signal of new stack rollout in 6-12 months.

## Examples

### Example 1: "Did Acme switch off Segment?" — answer in 5 min

**Goal:** Confirm rumor that Acme replaced Segment with RudderStack.

**Steps:**
1. Recipe 4 → python-Wappalyzer scan of acme.example.com. Detected: RudderStack analytics tag.
2. Recipe 2 → BuiltWith history shows Segment "LastDetected: 2026-04-15"; RudderStack "FirstDetected: 2026-04-22."
3. Recipe 7 → confirm via response headers: `X-Powered-By` includes RudderStack CDN.

**Verdict:** Confirmed switch in mid-April 2026. Battlecard pane 4 (parity) updated. Sales play: "We integrate natively with RudderStack via X feature."

### Example 2: Build TAM-filter prospect list using BuiltWith

**Goal:** Get list of "companies running Snowflake + dbt + Segment" in our TAM.

**Steps:**
1. Recipe 3 → BuiltWith lists7 API with tech filter.
2. Intersect with our ICP (employees 500+ in US Software vertical).
3. Push CSV to Salesforce as new ABM list; tag accounts `Stack_Match__c = True`.

**Result:** 184-account prospect list with high stack-match score; AEs notified.

### Example 3: Weekly tech-stack diff digest

**Goal:** Surface any meaningful stack switches across 5 competitors weekly.

**Steps:**
1. Recipe 8 → snapshot all 5 competitors.
2. Recipe 9 → diff vs last week.
3. Filter to material changes (analytics, CDP, observability, payment).
4. Recipe 10 → post to Slack `#ci-hotline`; roll into weekly digest.

**Result:** Caught 2 material switches in Q2; flagged Acme's move to Vercel as a hiring + product investment signal.

## Edge cases / gotchas

- **BuiltWith free preview** — limited (5 lookups/day); paid tier needed for sustained CI use.
- **Wappalyzer paid vs free** — free Chrome extension fingerprints in-browser; paid API for headless. python-Wappalyzer is OSS — fingerprint rules sometimes lag.
- **DNS CNAME masking** — when a domain uses Cloudflare in front of AWS, you see only Cloudflare. Use `dig` on `origin.acme.example.com` or check `Server` header from non-cached endpoints.
- **JS-rendered SPA** — Wappalyzer needs the *post-render* DOM; use `playwright-mcp` to load first, then fingerprint.
- **Header obfuscation** — security-conscious competitors strip `Server`, `X-Powered-By`. Fall back to JS/CSS asset path patterns (e.g., `/_next/static/` => Next.js).
- **Stale BuiltWith** — last-detected timestamps can lag weeks; cross-check with live Wappalyzer scan for current state.
- **Subdomain explosion** — Acme has 50 subdomains; tech stack varies by surface. Snapshot at minimum: marketing (root), app (`app.acme`), docs (`docs.acme`), API (`api.acme`).
- **False positive analytics** — Google Tag Manager hosts many tags; presence of GTM doesn't equal active use of each. Verify with network-tab inspection via Playwright.
- **DetectZeStack vs Wappalyzer accuracy** — DetectZeStack is fingerprinting + adjacencies; less granular than Wappalyzer on framework versions. Use for budget-constrained programs.
- **Apify pay-per-event spike** — 1000 domains × 1 run = ~$5; manageable. Quarterly bulk scans are fine.
- **Glassdoor's robots.txt** — disallows some scraping endpoints; don't pull Glassdoor through BuiltWith.
- **Don't fingerprint internal subdomains** — VPN-walled / staging subdomains are SCIP soft-caution; stick to public marketing + production app.
- **PROACTIVE.md scheduling** — monthly cadence default for stack monitoring (it's slow-changing); weekly for active war-game scenarios.
- **Provenance footer** — every claim cites BuiltWith / Wappalyzer / DNS resolver with retrieval date. Multi-source for any battlecard-grade claim.

## Sources

- BuiltWith API — https://api.builtwith.com/
- Wappalyzer — https://www.wappalyzer.com/
- python-Wappalyzer — https://github.com/chorsley/python-Wappalyzer
- BuiltWith vs Wappalyzer — https://prospeo.io/s/builtwith-vs-wappalyzer
- BuiltWith pricing — https://builtwith.com/pricing
- DetectZeStack — https://detectzestack.com/
- Pasquale Pillitteri — Detect tech stack — https://pasqualepillitteri.it/en/news/2424/how-to-detect-website-tech-stack-wappalyzer-builtwith
- Apify Tech Stack Detector — https://apify.com/store/categories/tech-stack
- role.md → "SOTA tool reference" → BuiltWith / Wappalyzer / DetectZeStack

## Related skills

- `competitor-hiring-intel-linkedin-sales-nav` — hiring signal for forward-looking stack moves
- `continuous-competitor-monitoring-klue-kompyte-crayon` — monthly stack snapshot fan-out
- `feature-parity-tracking` — infra row in the parity matrix
- `competitor-product-teardown-depth` — pair stack with in-product walkthrough
- `competitor-app-intel-sensor-tower-data-ai` — mobile SDK tech stack
