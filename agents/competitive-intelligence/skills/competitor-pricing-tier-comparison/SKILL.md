<!--
Sources: Visualping https://visualping.io/blog/distill-alternatives
         Distill.io https://distill.io/
         UptimeRobot change monitoring 2026 https://uptimerobot.com/knowledge-hub/monitoring/9-best-website-change-monitoring-tools-compared/
Companion playbook: role.md → "Pricing intelligence playbook" + "Pricing-tier grid template"
-->

# Competitor pricing tier comparison

Per-competitor per-tier grid with diff history + Reddit/G2 chatter overlay for gated quote-only tiers. Public pricing-page scrape via Visualping / Distill.io / firecrawl + element-level monitoring; per-cell confidence flag (confirmed/inferred/unknown). Output: `xlsx` pricing-tier grid + weekly diff digest.

## When to use

- "Compare pricing across [3-5 competitors]"
- "Did Acme just change their pricing?"
- "What's Beta's Enterprise tier really cost?"
- Build pricing leverage for battlecard pane 5
- Pre-deal: rep asks "what's their starting tier?"

## When NOT to use

- Single-page change detection → use `competitor-pricing-page-visualping-distill`
- Feature gating only → use `feature-parity-tracking`
- Discount strategy / negotiation → that's PMM/sales ops, not CI

## Setup

```bash
# Distill.io free tier — 25 monitors, granular element-level
export DISTILL_API_KEY="..."
# Visualping free tier — 5 monitors visual diff
export VISUALPING_API_KEY="..."

# Python for grid maintenance
uv pip install pandas openpyxl pyyaml requests beautifulsoup4
```

MCPs in `agent.yaml`: `firecrawl-mcp`, `playwright-mcp`, `reddit-mcp`, `xlsx`, `slack-mcp`.

## Common recipes

### Recipe 1: pricing.yaml schema

```yaml
# pricing.yaml — versioned source of truth
competitors:
  acme:
    name: Acme Corp
    pricing_url: https://acme.example.com/pricing
    last_scraped: 2026-06-10
    tiers:
      - name: Free
        price_per_seat_month_usd: 0
        seats_included: 1
        quotas: {storage_gb: 1, api_calls: 1000}
        addons: []
        confidence: confirmed
        source: https://acme.example.com/pricing
      - name: Starter
        price_per_seat_month_usd: 19
        seats_included: 5
        quotas: {storage_gb: 50, api_calls: 50000}
        addons: ["SSO +$5/seat","SOC2 audit log +$200/mo"]
        confidence: confirmed
        source: https://acme.example.com/pricing
      - name: Pro
        price_per_seat_month_usd: 49
        seats_included: 25
        quotas: {storage_gb: 500, api_calls: 250000}
        confidence: confirmed
      - name: Enterprise
        price_per_seat_month_usd: ~85   # inferred
        seats_included: "custom"
        quotas: {storage_gb: "custom"}
        confidence: inferred
        sources:
          - https://www.reddit.com/r/saas/comments/xyz/acme_enterprise_pricing
          - "G2 review #45678 quote: 'we pay $85/seat'"
```

### Recipe 2: Scrape pricing page (firecrawl)

```python
from firecrawl import FirecrawlApp
fc = FirecrawlApp(api_key=os.environ["FIRECRAWL_API_KEY"])
result = fc.scrape_url("https://acme.example.com/pricing",
                       params={"formats":["markdown","structured"]})
# 'structured' returns JSON schema if site uses Schema.org Product/Offer markup
```

### Recipe 3: Playwright pricing-toggle handling

```python
# Many SaaS pricing pages toggle monthly/annual; capture both
page.goto("https://acme.example.com/pricing")
page.click("text=Monthly")
m_prices = page.eval_on_selector_all(".tier .price", "els => els.map(e => e.innerText)")
page.click("text=Annual")
a_prices = page.eval_on_selector_all(".tier .price", "els => els.map(e => e.innerText)")
```

### Recipe 4: Distill.io element-level monitor

```bash
curl -X POST https://distill.io/api/v3/watchlists \
  -H "Authorization: Token $DISTILL_API_KEY" \
  -d '{
    "watchlist":{
      "name":"Acme pricing — Pro tier",
      "url":"https://acme.example.com/pricing",
      "selector":"#pricing-pro .price",
      "config":{"schedule":"@daily","webhook_url":"https://hooks.slack.com/..."}
    }
  }'
```

### Recipe 5: Reddit / G2 chatter for gated tiers

```python
import praw
r = praw.Reddit(client_id=..., client_secret=..., user_agent="CraftBot CI/0.1")
posts = list(r.subreddit("saas+sales").search(
    "Acme enterprise pricing", sort="relevance", limit=30))
# Filter to posts with dollar mentions
import re
relevant = [p for p in posts if re.search(r"\$\d{2,}", p.title + (p.selftext or ""))]
```

For G2: scrape reviews where reviewer discloses pricing (`firecrawl-mcp` on `acme/reviews`).

### Recipe 6: Glassdoor salary-leak grey-area (ethics flag)

```python
# Flagged ToS-grey — only if recipient OK with the ethics class.
# Glassdoor salaries sometimes leak per-seat cost via enterprise account-exec OTE.
# Recipient supplies + signs off; provenance footer = "glassdoor ToS-grey-flagged"
```

### Recipe 7: Convert pricing.yaml → xlsx grid

```python
import yaml, pandas as pd
data = yaml.safe_load(open("pricing.yaml"))
rows = []
for cid, comp in data["competitors"].items():
    for t in comp["tiers"]:
        rows.append({
            "Competitor": comp["name"],
            "Tier": t["name"],
            "$/seat/mo": t.get("price_per_seat_month_usd"),
            "Seats": t.get("seats_included"),
            "Storage GB": t.get("quotas",{}).get("storage_gb"),
            "Addons": "; ".join(t.get("addons",[])),
            "Confidence": t.get("confidence"),
            "Last verified": comp.get("last_scraped"),
        })
df = pd.DataFrame(rows)
with pd.ExcelWriter("pricing.xlsx", engine="openpyxl") as w:
    df.to_excel(w, sheet_name="Tiers", index=False)
```

### Recipe 8: Diff vs prior snapshot

```python
import yaml
prev = yaml.safe_load(open("pricing-2026-w22.yaml"))
curr = yaml.safe_load(open("pricing.yaml"))
deltas = []
for cid, comp in curr["competitors"].items():
    if cid in prev["competitors"]:
        for ct, pt in zip(comp["tiers"], prev["competitors"][cid]["tiers"]):
            if ct["price_per_seat_month_usd"] != pt["price_per_seat_month_usd"]:
                deltas.append((cid, ct["name"], pt["price_per_seat_month_usd"], ct["price_per_seat_month_usd"]))
```

### Recipe 9: Slack hot-alert on material change

```python
import requests
def alert(cid, tier, old, new):
    pct = (new - old) / old * 100 if old else 100
    if abs(pct) >= 10:
        requests.post(os.environ["SLACK_WEBHOOK_URL"],
                      json={"text": f":rotating_light: {cid} {tier} tier: ${old} → ${new} ({pct:+.0f}%)"})
```

### Recipe 10: Per-tier color-code legend

In xlsx, use conditional formatting:

```python
from openpyxl.styles import PatternFill
from openpyxl import load_workbook
wb = load_workbook("pricing.xlsx")
ws = wb["Tiers"]
fills = {"confirmed": PatternFill("solid", fgColor="C6EFCE"),
         "inferred":  PatternFill("solid", fgColor="FFEB9C"),
         "unknown":   PatternFill("solid", fgColor="FFC7CE")}
for row in ws.iter_rows(min_row=2):
    conf = row[6].value
    if conf in fills:
        for c in row:
            c.fill = fills[conf]
wb.save("pricing.xlsx")
```

### Recipe 11: Weekly digest delivery

Bundle Recipe 8 deltas into a weekly Slack/email digest. Surface only material moves (≥10% price change, new tier, key feature gated/ungated).

## Examples

### Example 1: First-pass pricing grid for 5 competitors

**Goal:** Build pricing.yaml + pricing.xlsx in 1 day for Acme, Beta, Gamma, Delta, Epsilon.

**Steps:**
1. For each, scrape pricing page (Recipe 2 or 3) + capture tier names, $, quotas, addons.
2. For Enterprise tiers (gated), search Reddit + G2 (Recipe 5) — mark `inferred` if ≥2 sources, `unknown` if 0.
3. Render xlsx (Recipe 7) with color codes (Recipe 10).
4. Set up Distill.io element monitors (Recipe 4) for each pricing page.
5. Commit pricing.yaml; share xlsx via Notion + Slack.

**Result:** First grid + monitoring wired; <2 hours of agent work plus competitor verification.

### Example 2: Weekly diff digest

**Goal:** Every Monday, surface what changed in competitor pricing.

**Steps:**
1. Re-scrape (Recipe 2/3) → new pricing.yaml.
2. Run Recipe 8 diff vs prior week.
3. Surface deltas via Slack hot-alert (Recipe 9) + weekly digest summary.
4. Material changes → flag battlecard pane 5 refresh (`battlecard-authoring-maintenance`).

**Result:** Auto-detected pricing changes within 24 hours of competitor shipping them.

## Edge cases / gotchas

- **A/B-tested pricing** — competitor shows different prices to different traffic. Scrape from 2-3 IPs (use `brightdata-mcp` proxy) before declaring a price change.
- **Promotional pricing** — discounts displayed as crossed-out original + new. Capture both.
- **Currency localization** — `acme.example.com/pricing` may localize to user's geo. Force `Accept-Language: en-US` + use US-IP proxy for canonical USD.
- **Quote-only tiers** — Enterprise is often "Contact sales." Don't fabricate; use Reddit + G2 + LinkedIn enterprise-buyer testimonials with `inferred` confidence + ≥2 source minimum.
- **Glassdoor salary-leak** — ToS-grey; flag in deliverable's provenance footer per `ethical-public-source-methodology`.
- **Sales-call notes from CRM** — internal CRM notes on prior competitor deals = legitimate internal source; cite as "internal CRM, opportunity #12345."
- **Toggle missing** — some pricing pages show only annual or only monthly. Note in YAML; don't infer monthly from annual without divisor.
- **Pricing page redirects** — competitor moves URL; Visualping breaks silently. Add a 200-status health check.
- **Add-on creep** — tier price stable but add-ons multiplied. Capture addons; battlecard surfaces "effective price" not "headline price."
- **Free-tier limit changes** — Acme drops free tier from 5 → 3 seats. Capture quotas, not just price.
- **Per-seat vs flat-rate mix** — Beta charges flat $99/mo for Starter (not per-seat). Schema supports both via separate fields.

## Sources

- Visualping — Distill Alternatives — https://visualping.io/blog/distill-alternatives
- UptimeRobot — Change Monitoring 2026 — https://uptimerobot.com/knowledge-hub/monitoring/9-best-website-change-monitoring-tools-compared/
- Distill.io — https://distill.io/
- role.md → "Pricing intelligence playbook" + "Pricing-tier grid template" (this bundle)

## Related skills

- `competitor-pricing-page-visualping-distill` — element-level monitor + webhook (single-page focus)
- `feature-parity-tracking` — pricing tier gating maps into parity tiers
- `battlecard-authoring-maintenance` — pricing leverage = battlecard pane 5
- `continuous-competitor-monitoring-klue-kompyte-crayon` — daily fan-out
- `ethical-public-source-methodology` — Glassdoor / Reddit ethics classes
