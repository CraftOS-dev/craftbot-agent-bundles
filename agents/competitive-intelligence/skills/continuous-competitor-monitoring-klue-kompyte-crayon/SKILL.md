<!--
Sources: Klue https://klue.com/
         Crayon https://www.crayon.co/
         Kompyte https://www.kompyte.com/
         Autobound CI 2026 https://www.autobound.ai/blog/top-15-competitive-intelligence-tools-2026
         Visualping https://visualping.io/
Companion playbook: role.md → "Continuous monitoring playbook"
-->

# Continuous competitor monitoring (Klue / Kompyte / Crayon class)

Daily-to-weekly automated diff across pricing, changelogs, social, jobs, patents, app reviews, ad libraries for a 3-5 competitor comp set. Paid path uses Klue / Crayon / Kompyte; free self-build path uses Visualping + ai-news-collectors + Reddit + GDELT + ad libraries. Both surface signals into Slack `#ci-hotline` and a weekly digest.

## When to use

- "Set up monitoring on these 5 competitors"
- "Track [competitor] daily for [signal type]"
- "I need a weekly competitor digest"
- "What changed at [competitor] this week?"
- New CI program kickoff; comp-set re-scoping
- After a competitor surprise (released a feature you missed, won a deal you should have)

## When NOT to use

- One-off "research this competitor" → use `competitor-product-teardown-depth`
- Single competitor deep dive → use `battlecard-authoring-maintenance`
- Win/loss-driven battlecard refresh → use `win-loss-ci-integration-klue-insider`

## Setup

### Paid path (Klue / Crayon / Kompyte)

```bash
# Klue REST API (battlecard insert/update, source attachment)
export KLUE_API_KEY="..."
export KLUE_API_BASE="https://api.klue.com/v1"

# Crayon (battlecard + monitoring source)
export CRAYON_API_KEY="..."
export CRAYON_API_BASE="https://api.crayon.co/v1"

# Kompyte (now Semrush; mid-market)
export KOMPYTE_API_KEY="..."
```

Pricing: Klue $15-40k/yr enterprise; Crayon similar; Kompyte Essentials from $300/yr. Free trials usually 14 days. Recipient supplies keys.

### Free self-build path (Visualping + ai-news + Reddit + GDELT)

```bash
# Visualping (free tier 5 monitors; $13/mo from)
export VISUALPING_API_KEY="..."

# GDELT (free, global news, no key)
# Reddit PRAW (free with app registration)
export REDDIT_CLIENT_ID="..."
export REDDIT_CLIENT_SECRET="..."
export REDDIT_USER_AGENT="CraftBot CI/0.1 by <handle>"

# Slack webhook for delivery
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
```

MCPs already in `agent.yaml`: `firecrawl-mcp`, `playwright-mcp`, `reddit-mcp`, `twitter-mcp`, `slack-mcp`, `gmail-mcp`, `notion-mcp`.

## Common recipes

### Recipe 1: Klue create battlecard via REST API

```bash
curl -X POST "$KLUE_API_BASE/battlecards" \
  -H "Authorization: Bearer $KLUE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "competitor_id": "acme-corp",
    "title": "Acme Corp battlecard",
    "panes": [
      {"name": "positioning", "content_md": "..."},
      {"name": "objections", "content_md": "..."}
    ],
    "refresh_triggers": ["changelog_diff","pricing_diff","g2_review_batch_gt_3"]
  }'
```

### Recipe 2: Klue attach a source for auto-monitoring

```bash
curl -X POST "$KLUE_API_BASE/sources" \
  -H "Authorization: Bearer $KLUE_API_KEY" \
  -d '{
    "competitor_id": "acme-corp",
    "url": "https://acme.example.com/changelog",
    "source_type": "changelog",
    "frequency": "daily"
  }'
```

### Recipe 3: Crayon source pull

```bash
curl -H "Authorization: Bearer $CRAYON_API_KEY" \
  "$CRAYON_API_BASE/competitors/acme/insights?since=2026-06-04" \
  | jq '.insights[] | {type, source, summary, captured_at}'
```

Crayon classifies into: website-change, social-post, job-post, patent, app-review, pricing-page, ad-creative.

### Recipe 4: Visualping create monitor (free path equivalent)

```bash
curl -X POST "https://api.visualping.io/v1/jobs" \
  -H "Authorization: Bearer $VISUALPING_API_KEY" \
  -d '{
    "url": "https://acme.example.com/pricing",
    "frequency_minutes": 1440,
    "selector": "#pricing-table",
    "webhook_url": "'"$SLACK_WEBHOOK_URL"'"
  }'
```

`selector` is the CSS selector for element-level monitoring — pricing table only, not noise from blog banners.

### Recipe 5: Per-competitor source fan-out (free self-build)

```yaml
# config/competitors/acme.yaml
competitor: acme-corp
homepage: https://acme.example.com
sources:
  - kind: pricing_page
    url: https://acme.example.com/pricing
    cadence: daily
    tool: visualping
  - kind: changelog
    url: https://acme.example.com/changelog
    cadence: daily
    tool: visualping
  - kind: homepage
    url: https://acme.example.com
    cadence: weekly
    tool: visualping
  - kind: reddit
    query: "acme corp"
    cadence: weekly
    tool: reddit-mcp
  - kind: github_releases
    org: acme-org
    cadence: daily
    tool: github-api
  - kind: press
    query: "Acme Corp"
    cadence: daily
    tool: ai-news-collectors
  - kind: gdelt
    query: "Acme Corp"
    cadence: daily
    tool: gdeltdoc
```

### Recipe 6: GDELT competitor news fan-out (free)

```python
from gdeltdoc import GdeltDoc, Filters

f = Filters(
    keyword="Acme Corp",
    start_date="2026-06-04",
    end_date="2026-06-11",
    country=["US","GB","DE"],
)
articles = GdeltDoc().article_search(f)
# Returns title, url, domain, language, seendate
```

### Recipe 7: Reddit signal pull via PRAW

```python
import praw
r = praw.Reddit(client_id=os.environ["REDDIT_CLIENT_ID"],
                client_secret=os.environ["REDDIT_CLIENT_SECRET"],
                user_agent=os.environ["REDDIT_USER_AGENT"])
posts = list(r.subreddit("saas+sales+sysadmin").search(
    "Acme Corp", sort="new", time_filter="week", limit=50))
for p in posts:
    print(p.created_utc, p.score, p.title, p.url)
```

### Recipe 8: GitHub release feed (OSS competitor)

```bash
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.github.com/repos/acme-org/acme/releases?per_page=5" \
  | jq '.[] | {tag: .tag_name, date: .published_at, body: .body[0:300]}'
```

### Recipe 9: ai-news-collectors press feed wiring

```python
from ai_news_collectors import collect
items = collect(
    queries=["Acme Corp", "Acme acquires", "Acme funding"],
    sources=["techcrunch","theinformation","businesswire","prnewswire"],
    since="2026-06-04",
)
```

### Recipe 10: Slack hot-signal delivery

```python
import requests
def post_signal(competitor, signal_type, summary, source_url):
    block = {
        "blocks": [
            {"type":"header","text":{"type":"plain_text","text":f"{competitor} • {signal_type}"}},
            {"type":"section","text":{"type":"mrkdwn","text":summary}},
            {"type":"context","elements":[{"type":"mrkdwn","text":f"<{source_url}|source>"}]},
        ]
    }
    requests.post(os.environ["SLACK_WEBHOOK_URL"], json=block)
```

### Recipe 11: Weekly digest synthesis

```python
# Pull last 7 days of signals across competitors,
# group by competitor + signal_type,
# rank by impact (pricing > release > exec move > social),
# render top 5 as weekly digest via gmail-mcp / markdown
```

### Recipe 12: Refresh-on-signal trigger wiring

See role.md → "Refresh-on-signal trigger config" YAML pattern. Wire signal events to either Klue auto-refresh API or local battlecard staleness flag.

## Examples

### Example 1: New CI program for a 5-competitor comp set (free self-build)

**Goal:** Stand up monitoring + weekly digest for Acme, Beta, Gamma, Delta, Epsilon in 1 day.

**Steps:**
1. Write `config/competitors/<name>.yaml` for each (Recipe 5).
2. Visualping monitors: 1 pricing + 1 changelog + 1 homepage per competitor = 15 monitors. Free tier 5; need $13/mo Starter for 15.
3. Reddit + GDELT + ai-news scheduled daily via cron / PROACTIVE.md.
4. Slack `#ci-hotline` channel + webhook for hot signals; `#ci-digest` channel for weekly summary.
5. Friday 9am: synthesize weekly digest via Recipe 11; post + email via `gmail-mcp`.

**Result:** Daily hot signals in Slack; weekly digest in inbox; cost <$30/mo plus Reddit/GDELT/GitHub free.

### Example 2: Paid Klue program — wire 8-competitor monitoring

**Goal:** Use Klue Standard ($25k/yr) to handle source ingestion + battlecard delivery.

**Steps:**
1. In Klue UI: create 8 competitor profiles; attach 5-7 sources each (Recipe 2).
2. Use Klue Insider Salesforce app to surface battlecards on opportunity record.
3. Wire Klue alerts → Slack channel `#ci-hotline` via Klue's native Slack app.
4. Set refresh-on-signal in Klue: changelog diff, pricing diff, exec move.

**Result:** Klue handles fan-out + delivery; CraftBot agent layers self-build sources on top (GDELT, Reddit, USPTO) that Klue doesn't cover.

## Edge cases / gotchas

- **Visualping noise** — font-color and minor CSS changes trigger noise. Use CSS selector to scope to the meaningful element (price element, feature list, changelog `<article>`).
- **Klue source-attachment limit per battlecard** — typically 20 in Standard tier. Prioritize daily-changing sources (changelog, pricing) over rarely-changing (about page).
- **Crayon insight overlap** — Crayon flags some sources Klue also covers. Don't double-monitor; choose one.
- **Reddit PRAW rate limit** — 60 req/min OAuth, 30/min anonymous. Stagger competitor queries.
- **GDELT lag** — usually 15-min lag from publish; sometimes a few hours. Real-time press alerts want ai-news-collectors RSS or NewsAPI directly.
- **GitHub release feed** — only catches *tagged* releases. Some teams ship via deploy-from-main with no GitHub release; use changelog page as canonical.
- **Klue free trial 14 days** — schedule comp-set scoping + URL prep so you actually configure during the trial.
- **Don't monitor too much** — 5 competitors × 7 source types × daily = 35 signals/day. Most are noise. Set strict signal-to-noise rules in Slack-channel filter step.
- **Time zones** — Visualping timestamps are UTC; Klue/Crayon often local. Normalize to UTC in your digest.
- **PROACTIVE.md scheduling** — runs from the harness; document the cron in PROACTIVE.md and the YAML config file references so future maintainers can find both halves.

## Sources

- Klue — Competitive Intelligence Tools for B2B Tech Teams 2026 — https://klue.com/topics/competitive-intelligence-tools-b2b-software
- Klue × Salesforce integration playbook — https://klue.com/salesforce
- Klue vs Crayon (2026) — https://parano.ai/blog/klue-vs-crayon
- Autobound — 15 CI Tools Compared 2026 — https://www.autobound.ai/blog/top-15-competitive-intelligence-tools-2026
- Visualping — 8 Best Distill Alternatives — https://visualping.io/blog/distill-alternatives
- UptimeRobot — 9 Best Website Change Monitoring 2026 — https://uptimerobot.com/knowledge-hub/monitoring/9-best-website-change-monitoring-tools-compared/
- Kompyte (Semrush) — https://www.kompyte.com/
- role.md → "Continuous monitoring playbook" (this bundle)

## Related skills

- `battlecard-authoring-maintenance` — what the monitoring signals refresh
- `competitor-pricing-page-visualping-distill` — pricing-page specific element-level monitor
- `competitor-messaging-tracking-diff` — weekly LP / homepage diff classifier
- `ci-delivery-slack-crm-klue-insider` — how the hot signals surface to reps
- `ethical-public-source-methodology` — SCIP code compliance on every source added
