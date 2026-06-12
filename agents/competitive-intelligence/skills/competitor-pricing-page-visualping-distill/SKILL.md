<!--
Sources: Visualping https://visualping.io/
         Distill.io https://distill.io/
         ChangeTower https://changetower.com/
         Wachete https://www.wachete.com/
         Distill alternatives https://visualping.io/blog/distill-alternatives
         UptimeRobot site-monitoring guide 2026 https://uptimerobot.com/knowledge-hub/monitoring/9-best-website-change-monitoring-tools-compared/
Companion playbook: role.md → "Pricing intelligence playbook" + "SOTA tool reference"
-->

# Competitor pricing-page change detection (Visualping / Distill.io / ChangeTower / Wachete)

Element-level pricing-page monitoring. Visualping (visual + element diffs, 5 free monitors). Distill.io (granular, 25 free monitors). ChangeTower (audit-friendly, compliance). Wachete (behind-login + PDF/DOCX with recipient's credentials). Webhook → Slack the second a change ships. Element selectors limit noise to the meaningful price element only.

## When to use

- "Diff their pricing page weekly"
- "Alert me when [competitor] changes price"
- Pricing-intelligence playbook (role.md)
- Pre-pricing-strategy review: history of competitor moves
- Cross-reference pricing diff with messaging-tracking-diff
- Quarterly pricing-tier grid refresh signal source

## When NOT to use

- Pricing-tier comparison authoring → use `competitor-pricing-tier-comparison`
- Quote-only / gated tier pricing → Recipe 12 falls back to qualitative source mining (Reddit / G2 / sales notes)
- LP / homepage messaging diff → use `competitor-messaging-tracking-diff`
- Changelog or release-note diff → use `continuous-competitor-monitoring-klue-kompyte-crayon` / `feature-parity-tracking`

## Setup

```bash
# Visualping (free 5 monitors; $13+/mo Starter)
export VISUALPING_API_KEY="..."

# Distill.io (free 25 monitors; $9+/mo)
export DISTILL_API_TOKEN="..."

# ChangeTower (audit-friendly; from $79/mo)
export CHANGETOWER_API_KEY="..."

# Wachete (behind-login + PDF; from $5/mo)
export WACHETE_API_KEY="..."

# Slack webhook
export SLACK_WEBHOOK_URL="..."

# Firecrawl for structured JSON extraction
export FIRECRAWL_API_KEY="..."
```

MCPs in `agent.yaml`: `firecrawl-mcp`, `playwright-mcp`, `slack-mcp`, `notion-mcp`, `cli-anything`.

## Common recipes

### Recipe 1: Visualping create element-level pricing monitor

```bash
curl -X POST "https://api.visualping.io/v1/jobs" \
  -H "Authorization: Bearer $VISUALPING_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://acme.example.com/pricing",
    "frequency_minutes": 1440,
    "selector": "#pricing-table",
    "webhook_url": "'"$SLACK_WEBHOOK_URL"'",
    "name": "Acme Pricing Daily"
  }'
```

`selector` scopes to pricing table only. Frequency: daily (1440 min); hourly during pricing-rumor periods.

### Recipe 2: Visualping multi-region monitor

```bash
# Capture both US + EU pricing pages
for region in us eu uk au; do
  curl -X POST "https://api.visualping.io/v1/jobs" \
    -H "Authorization: Bearer $VISUALPING_API_KEY" \
    -d '{
      "url": "https://acme.example.com/'"$region"'/pricing",
      "frequency_minutes": 1440,
      "selector": ".pricing-grid",
      "webhook_url": "'"$SLACK_WEBHOOK_URL"'"
    }'
done
```

Currency / tier variants per region matter — many SaaS competitors price differently per geo.

### Recipe 3: Distill.io create monitor via REST

```bash
curl -X POST "https://distill.io/api/v1/dashboard/watchlist" \
  -H "X-Auth-Token: $DISTILL_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Acme Pricing Granular",
    "uri": "https://acme.example.com/pricing",
    "config": {
      "selections": [
        {"type":"css","frames":[0],"path":"div.pricing-tier:nth-child(1) .price"},
        {"type":"css","frames":[0],"path":"div.pricing-tier:nth-child(2) .price"},
        {"type":"css","frames":[0],"path":"div.pricing-tier:nth-child(3) .price"},
        {"type":"css","frames":[0],"path":"div.pricing-tier:nth-child(4) .features"}
      ],
      "include_styles": false,
      "actions": [{"type":"alert","target":"'"$SLACK_WEBHOOK_URL"'"}]
    },
    "schedule": {"type":"interval","minutes":60}
  }'
```

Distill is the most granular — per-tier per-element monitoring with low noise.

### Recipe 4: ChangeTower create monitor (audit-friendly)

```bash
curl -X POST "https://api.changetower.com/v1/monitors" \
  -H "Authorization: Bearer $CHANGETOWER_API_KEY" \
  -d '{
    "url": "https://acme.example.com/pricing",
    "monitor_type": "text",
    "frequency": "daily",
    "alert_email": "ci@example.com",
    "audit_trail": true
  }'
```

`audit_trail: true` keeps timestamped + signed snapshots for compliance / legal.

### Recipe 5: Wachete monitor a login-gated PDF (recipient's own login)

```bash
# Wachete supports authenticated browsing; recipient's own credentials
curl -X POST "https://api.wachete.com/v1/checks" \
  -H "Authorization: Bearer $WACHETE_API_KEY" \
  -d '{
    "url": "https://acme.example.com/customers/pricing.pdf",
    "auth": {"username":"recipient@example.com","password":"...","cookie_storage":true},
    "frequency": "daily",
    "format": "pdf"
  }'
```

Only with the recipient's legitimate credentials — never the competitor's.

### Recipe 6: Webhook ingestion handler

```python
from flask import Flask, request
app = Flask(__name__)

@app.post("/visualping-webhook")
def vp():
    payload = request.json
    # {url, job_id, change_detected, before, after, screenshot_url, ts}
    diff = payload["after"]
    parsed = parse_pricing(diff)
    notify_slack(parsed)
    persist_snapshot(payload)
    return "ok"
```

### Recipe 7: Parse pricing from diff

```python
import re
def parse_pricing(html_or_text):
    # Capture tier name + $ amount
    pat = re.compile(r"(?P<tier>Starter|Pro|Team|Business|Enterprise)\s*\$(?P<price>\d+(?:\.\d+)?)\s*(?:/\s*(?P<unit>seat|user|mo|yr))?", re.I)
    return [m.groupdict() for m in pat.finditer(html_or_text)]
```

### Recipe 8: Hourly during pricing-rumor period

```bash
# Bump frequency on Reddit / press signal
curl -X PATCH "https://api.visualping.io/v1/jobs/$JOB_ID" \
  -H "Authorization: Bearer $VISUALPING_API_KEY" \
  -d '{"frequency_minutes": 60}'
```

### Recipe 9: Diff-classify (material vs cosmetic)

```python
import anthropic
client = anthropic.Anthropic()
prompt = f"""Classify this pricing-page diff as one of:
- material (price change, new tier, feature gated, discount banner)
- cosmetic (typo, font, image swap)
- ambiguous

Before:
{before}

After:
{after}

Output: {{classification, confidence, explanation}}
"""
msg = client.messages.create(model="claude-opus-4-7-1m", max_tokens=1000,
                              messages=[{"role":"user","content":prompt}])
```

### Recipe 10: Multi-tool coverage table

```yaml
# Use the right tool per surface
surfaces:
  pricing_public_page:    visualping (element selector)
  pricing_per_region:     visualping (one job per region)
  feature_table_granular: distill.io (per-row selectors)
  pricing_pdf_login:      wachete (recipient credentials)
  audit_compliance:       changetower (signed snapshot)
```

### Recipe 11: Snapshot history persistence

```python
# Visualping stores 30-90 days; persist to local for long-term diff
import boto3, json
def archive(payload):
    s3 = boto3.client("s3")
    key = f"pricing/{payload['job_id']}/{payload['ts']}.json"
    s3.put_object(Bucket="ci-archive", Key=key, Body=json.dumps(payload))
```

### Recipe 12: Gated quote-only pricing — qualitative sources

```python
# Reddit chatter (legitimate inference, no pretexting)
# r/saas, r/sales, r/sysadmin, r/devops
posts = reddit_search("acme corp pricing", time_filter="month")
# G2 review reviewer-disclosed pricing — Apify Review Intel
# Glassdoor salary leak (ToS-grey — flag)
# Sales call notes from CRM (legitimate internal source)
```

Cite as `inferred (1 source + reasoning)` per role.md confidence flags.

### Recipe 13: Slack hot alert formatting

```python
def post_pricing_change(competitor, tier, old, new, source_url):
    requests.post(SLACK_WEBHOOK_URL, json={
        "blocks": [
            {"type":"header","text":{"type":"plain_text",
             "text":f":dollar: {competitor} pricing change detected"}},
            {"type":"section","text":{"type":"mrkdwn",
             "text":f"*Tier:* {tier}\n*Was:* ${old}\n*Now:* ${new}\n*Change:* {(new-old)/old*100:+.1f}%"}},
            {"type":"context","elements":[{"type":"mrkdwn",
             "text":f"<{source_url}|source>"}]}
        ],
        "channel":"#ci-hotline",
    })
```

## Examples

### Example 1: 5-competitor pricing watch on free tier

**Goal:** Daily monitor on 5 pricing pages, $0 cost.

**Steps:**
1. Recipe 3 → Distill.io free tier handles 5 pricing pages (well under 25-monitor cap).
2. Recipe 13 → Slack `#ci-hotline` on change.
3. Recipe 9 → LLM classifier in webhook handler filters cosmetic from material.

**Result:** Free pricing monitoring; ~3 material changes/month surfaced.

### Example 2: Audit-grade pricing snapshots for legal review

**Goal:** Legal team needs signed snapshots of competitor pricing for trademark/comparative-advertising review.

**Steps:**
1. Recipe 4 → ChangeTower with `audit_trail: true`.
2. Recipe 11 → archive snapshots to S3 with retention policy.
3. Generate quarterly PDF report of all snapshots for legal.

**Result:** Defensible chain-of-custody pricing evidence.

### Example 3: Detect Acme price cut + cascade alerts

**Goal:** Acme cuts Pro tier from $99 to $79; alert CRO + flag battlecards.

**Steps:**
1. Recipe 1 → Visualping detects diff.
2. Recipe 7 → parse new $79 from after-snapshot.
3. Recipe 9 → classifier: material (price decrease 20%).
4. Recipe 13 → `#ci-hotline` post.
5. Webhook cascades:
   - Update `competitor-pricing-tier-comparison` grid.
   - Auto-flag battlecard pane 5 (pricing leverage) for re-author.
   - Notify CRO via gmail-mcp.

**Result:** End-to-end alert + battlecard refresh within 1 hour.

## Edge cases / gotchas

- **Font / color changes triggering noise** — use CSS selector to scope to the actual price element, not the whole tier card.
- **A/B-tested pricing pages** — competitor may show different prices to different cohorts. Use a stable session cookie / VPN to keep the variant consistent.
- **JS-rendered pricing toggles (monthly/yearly)** — Visualping captures default state; for both, set up 2 monitors with selectors for each toggle state. Distill supports actions to click before capture.
- **Geo-IP rerouting** — competitor may serve different prices by IP. Capture from at least US + EU + APAC datacenter egress.
- **Currency variance** — `$99/mo` in USD vs `€99/mo` in EUR triggers diff but is just currency. Normalize before classifying.
- **Quote-only Enterprise tier** — most are gated. Use Recipe 12 qualitative inference; flag confidence as `inferred (1 source + reasoning)`.
- **Visualping free tier limit** — 5 monitors; you'll hit it fast. Distill.io is the better free choice for CI.
- **Distill cloud vs extension** — paid REST monitors only on cloud; the free Chrome extension does not webhook.
- **Wachete login-monitoring** — recipient's credentials only; never the competitor's. SCIP hard no.
- **Snapshot retention** — Visualping 30-90d; persist to your own bucket for long-term history (Recipe 11).
- **Webhook reliability** — Visualping retries 3x then drops; add idempotency + dead-letter on your side.
- **Material classification miss** — LLM occasionally calls a font-color change "material." QA with weekly sample.
- **Don't monitor too many element selectors** — 4-5 per page is the sweet spot; more = brittle to DOM changes.
- **PROACTIVE.md scheduling** — daily default per role.md cadence; hourly during rumor periods.
- **Provenance footer** — include retrieval timestamp + snapshot URL per change; classification confidence shown.

## Sources

- Visualping API — https://visualping.io/docs/api
- Distill.io API — https://distill.io/docs/api/
- ChangeTower — https://changetower.com/
- Wachete — https://www.wachete.com/
- Visualping vs Distill alternatives — https://visualping.io/blog/distill-alternatives
- UptimeRobot — 9 Best Website Change Monitoring 2026 — https://uptimerobot.com/knowledge-hub/monitoring/9-best-website-change-monitoring-tools-compared/
- role.md → "Pricing intelligence playbook" + "SOTA tool reference"

## Related skills

- `competitor-pricing-tier-comparison` — authoring of the comparison grid after a change ships
- `competitor-messaging-tracking-diff` — homepage / LP diff paired with pricing diff
- `continuous-competitor-monitoring-klue-kompyte-crayon` — pricing diff is one fan-out layer
- `battlecard-authoring-maintenance` — pane 5 (pricing leverage) auto-flag
- `ethical-public-source-methodology` — public-page only; never pretexting
