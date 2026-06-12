<!--
Sources: Bombora https://bombora.com/
         G2 Buyer Intent https://www.g2.com/products/g2-buyer-intent
         ZoomInfo Intent https://pipeline.zoominfo.com/sales/intent-data-platform
         GrowthSpree 2026 https://www.growthspreeofficial.com/blogs/buyer-intent-signals-bombora-g2-zoominfo-b2b-2026
         6sense https://6sense.com/
Companion playbook: role.md → CI delivery + deal-level CI playbook
-->

# Intent-data CI (Bombora / G2 Intent / ZoomInfo / 6sense)

Layer category-level intent (Bombora 5,000-site B2B media co-op) + vendor-specific late-funnel intent (G2 Buyer Intent) + first-party + predictive (ZoomInfo / 6sense). Use to (a) detect when target accounts research a competitor, (b) trigger sales outreach, (c) tag battlecards with "in-market against X."

## When to use

- "Set up intent-data alerts"
- "Who's researching [competitor X] right now?"
- "Surge signal on competitor category"
- ABM list enrichment with CI angle
- Pre-deal: rep asks "is this account in-market against Acme?"

## When NOT to use

- Org-firmographics only → use ZoomInfo basic, not intent
- Page-content-engagement on our site → product analytics, not CI intent
- Long-tail keyword research → use `competitor-seo-ahrefs-semrush-organic`

## Setup

```bash
# Bombora (~$25k/yr) — Company Surge REST
export BOMBORA_API_KEY="..."
export BOMBORA_ORG_ID="..."

# G2 Buyer Intent (~$15k+/yr) — REST + webhook
export G2_BUYER_INTENT_API_KEY="..."

# ZoomInfo (enterprise) — REST + CRM-native
export ZOOMINFO_API_KEY="..."

# 6sense (enterprise) — REST + ABM platform
export SIXSENSE_API_KEY="..."

# Demandbase, TrustRadius Intent — similar pattern
```

MCPs in `agent.yaml`: `salesforce-api`, `slack-mcp`, `posthog-mcp`, `notion-mcp`.

## Common recipes

### Recipe 1: Bombora Company Surge pull

```bash
curl -H "Authorization: Bearer $BOMBORA_API_KEY" \
  "https://api.bombora.com/v1/orgs/$BOMBORA_ORG_ID/company-surge?topics=competitor-x&since=2026-06-04"
```

Returns: list of `{company_name, domain, surge_score, top_topics, week_of}`. Surge score ≥60 = research signal; 80+ = active eval.

### Recipe 2: Bombora topic taxonomy lookup

```bash
# Search for topic IDs matching your competitive category
curl -H "Authorization: Bearer $BOMBORA_API_KEY" \
  "https://api.bombora.com/v1/topics?search=competitor-x"
# Most competitors don't have a dedicated topic; use category topics like "Sales Engagement Platforms"
```

### Recipe 3: G2 Buyer Intent webhook handler

```python
from flask import Flask, request
app = Flask(__name__)

@app.post("/g2-intent-webhook")
def g2():
    payload = request.json
    # Payload: {company, domain, signal_kind, product_viewed, comparison_with, week_of}
    if payload["signal_kind"] == "comparison" and payload["comparison_with"] == "acme-corp":
        notify_ae(payload)
    return "ok"
```

G2 fires events: `product_view`, `comparison`, `pricing_view`, `category_view`. Comparison + competitor name = highest-fidelity CI signal.

### Recipe 4: G2 REST pull

```bash
curl -H "Authorization: Bearer $G2_BUYER_INTENT_API_KEY" \
  "https://api.g2.com/v1/buyer-intent/events?since=2026-06-04&products=acme-corp,beta-inc"
```

### Recipe 5: ZoomInfo Intent topic search

```bash
curl -X POST "https://api.zoominfo.com/v1/intent/search" \
  -H "Authorization: Bearer $ZOOMINFO_API_KEY" \
  -d '{
    "topics":["sales-engagement-platforms","crm-alternatives-to-acme"],
    "minSignalScore":60,
    "since":"2026-06-04"
  }'
```

ZoomInfo claims 210M+ IP-to-Org pairings; deduped against partner-publisher network.

### Recipe 6: 6sense Surge Insights

```bash
curl -H "Authorization: Bearer $SIXSENSE_API_KEY" \
  "https://api.6sense.com/v3/insights/surge?topics=competitor-x&account_ids=$account_id"
```

6sense layers ML prediction on top of partner-publisher signal — "in-decision" prediction is the headline value.

### Recipe 7: Multi-source intent fusion

```python
# Pull from all providers; dedupe by domain; fuse scores
sources = ["bombora","g2","zoominfo","6sense"]
events = {}
for s in sources:
    for e in fetch_from(s):
        d = e["domain"]
        events.setdefault(d, []).append({"source":s, "score":e["score"], "topic":e["topic"]})

# Fused score: weighted average prioritizing G2 (late-funnel) + 6sense (predictive)
weights = {"g2":1.5, "6sense":1.3, "bombora":1.0, "zoominfo":1.1}
def fused(events_for_domain):
    n = sum(weights[e["source"]] * e["score"] for e in events_for_domain)
    d = sum(weights[e["source"]] for e in events_for_domain)
    return n/d if d else 0
```

### Recipe 8: Salesforce account-tag write-back

```python
from simple_salesforce import Salesforce
sf = Salesforce(...)
# Tag accounts "in-market against Acme"
sf.Account.update(account_id, {"In_Market_Against__c":"acme-corp", "Surge_Score__c":fused_score})
```

### Recipe 9: Slack notify the AE

```python
import requests
def alert_ae(account_name, ae_slack_id, surge_score, competitor):
    requests.post(SLACK_WEBHOOK_URL, json={
        "channel": f"@{ae_slack_id}",
        "text": f":bar_chart: {account_name} surging on *{competitor}* — score {surge_score}.\n"
                f"Battlecard: <{sf_battlecard_url}>"
    })
```

### Recipe 10: Battlecard "in-market against X" tag

```python
# On the battlecard, add a panel showing accounts currently in-market against this competitor
in_market = [a for a in accounts if a["In_Market_Against__c"] == competitor and a["Surge_Score__c"] >= 70]
# Render into battlecard pane: "Accounts surging on Acme (last 7 days)"
```

### Recipe 11: Bombora topic surge to ABM cohort

```python
# Pull surging companies on category topic; intersect with our ICP filter
surging = bombora_surge("Sales Engagement Platforms")
icp = [c for c in surging if c["employees"] >= 500 and c["industry"] in ["Software","FinServ"]]
# Push as ABM list to ZoomInfo / Demandbase / 6sense play
```

### Recipe 12: TrustRadius Intent

TrustRadius launched intent in 2024-2025; account-research signal at the product-comparison level. Similar API pattern to G2.

```bash
curl -H "Authorization: Bearer $TR_INTENT_API_KEY" \
  "https://api.trustradius.com/v1/intent/events?since=2026-06-04&products=acme,beta"
```

## Examples

### Example 1: G2 Buyer Intent → AE notification

**Goal:** When a target account compares us vs Acme on G2, ping the AE.

**Steps:**
1. Recipe 3 → host G2 webhook.
2. Recipe 8 → write `In_Market_Against__c = acme-corp` on the SF account.
3. Recipe 9 → DM the account's AE with the surge fact + battlecard link.

**Result:** AE knows within minutes; conversation starts pre-emptively.

### Example 2: Fused multi-source intent for ABM

**Goal:** Build weekly "in-market against top 3 competitors" cohort across all 4 providers.

**Steps:**
1. Recipe 1 + 4 + 5 + 6 → pull all 4 sources for last 7 days.
2. Recipe 7 → fuse scores; rank by fused score.
3. Top 100 → push to ABM play; tag accounts in SF (Recipe 8).
4. Battlecard pane (Recipe 10) surfaces the list to reps.

**Result:** ABM cohort + battlecard tag refreshed weekly with multi-source signal.

## Edge cases / gotchas

- **Bombora topic coverage** — pre-defined taxonomy; competitor-name topics rare. Use category topic + filter by competitor mention in G2/6sense.
- **G2 comparison signal volume** — small; high-fidelity. Don't expect daily fires per AE.
- **ZoomInfo IP-to-Org accuracy** — overstated; office IPs map to org, but home/coffee IPs misattribute. Treat as directional.
- **6sense prediction confidence** — black box; treat ML score as one input, not gospel.
- **Cost** — Bombora $25k+, G2 Intent $15k+, ZoomInfo enterprise, 6sense enterprise. Stack of 3+ runs $50-100k+/yr. Recipient supplies all keys.
- **Webhook reliability** — G2 webhook retry not always guaranteed. Add idempotent ingestion + dead-letter queue.
- **Privacy / GDPR** — EU accounts may opt out of intent tracking; respect provider's GDPR filter flag.
- **Cookie deprecation** — third-party cookies' decline reduces partner-publisher signal quality; providers compensate with first-party data.
- **Score normalization** — each provider scales 0-100 differently; fused score per Recipe 7 needs per-provider calibration.
- **Don't spam reps** — surge alerts that fire 5x/day per AE → ignored. Threshold + dedupe + 1 alert per account per 7 days.
- **Salesforce field collisions** — `Intent_Score__c` may already exist; namespace your fields (`CI_Intent_Score__c`).
- **Bombora topic refresh** — they add 50+ topics/quarter; review quarterly to add new relevant ones.

## Sources

- Bombora — https://bombora.com/
- G2 Buyer Intent — https://www.g2.com/products/g2-buyer-intent
- ZoomInfo Intent — https://pipeline.zoominfo.com/sales/intent-data-platform
- 6sense — https://6sense.com/
- GrowthSpree 2026 — https://www.growthspreeofficial.com/blogs/buyer-intent-signals-bombora-g2-zoominfo-b2b-2026
- AutoBound — Best Buyer Intent Platforms — https://www.autobound.ai/blog/best-intent-data-platforms
- role.md → "Hot-deals CI playbook" (this bundle)

## Related skills

- `hot-deals-ci-deal-level` — intent signal feeds micro-battlecard at deal level
- `ci-delivery-slack-crm-klue-insider` — Salesforce + Slack surface
- `battlecard-authoring-maintenance` — "in-market" pane
- `continuous-competitor-monitoring-klue-kompyte-crayon` — intent paired with monitoring
- `ci-program-metrics-adoption-rate` — intent-driven deal win-rate measurement
