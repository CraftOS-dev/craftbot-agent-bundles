<!--
Sources: G2 https://www.g2.com/
         TrustRadius https://www.trustradius.com/
         Capterra https://www.capterra.com/
         Trustpilot https://www.trustpilot.com/
         Glassdoor https://www.glassdoor.com/
         Apify Review Intelligence https://apify.com/ramsford/review-intelligence-agent
         PageCrawl https://pagecrawl.io/blog/trustpilot-g2-capterra-review-velocity-alerts
         Aikenhouse Review Platforms 2026 https://www.aikenhouse.com/post/the-best-software-review-platforms-in-2026
         G2 acquires Capterra Feb 2026 https://www.aikenhouse.com/post/the-best-software-review-platforms-in-2026
Companion playbook: role.md → "Signal layer cadence" → Reviews row + "SOTA tool reference"
-->

# Competitor review monitoring (G2 / TrustRadius / Capterra / Trustpilot / Glassdoor)

Public review monitoring across the consolidated landscape. **Post-Feb 2026 G2 acquired Capterra + Software Advice + GetApp from Gartner — combined ~55-58% of global software-review influence**; TrustRadius retains independence + 60% rejection rate (signal-per-review higher); Trustpilot covers consumer + SMB; Glassdoor for employee-sentiment proxy (ToS-grey — flag). Monitor: new review velocity, rating trend, theme-shift in 1-star + 5-star, NPS proxy, competitor responses.

## When to use

- "Monitor [competitor]'s G2/TR/Capterra reviews"
- "What are people complaining about with Acme?"
- Kill-sheet refresh (mine top 5 negative themes)
- Battlecard refresh (pair with PMM differentiator language)
- Pre-launch teardown (what reviews say about the category leader)
- Weekly cadence per signal layer table
- Sentiment shift alert (1-star spike → flash brief)

## When NOT to use

- App store reviews → use `competitor-app-intel-sensor-tower-data-ai`
- B2C / DTC review mining → Trustpilot only; G2/Capterra/TR are B2B
- Brand sentiment outside review platforms → social-listening component
- Employee sentiment only → Glassdoor, but flag ToS-grey in deliverable

## Setup

```bash
# Apify Review Intelligence — pay-per-event
export APIFY_TOKEN="..."

# PageCrawl ($8+/mo) for review-velocity alerts
export PAGECRAWL_API_KEY="..."

# Firecrawl for direct review-page scrape
export FIRECRAWL_API_KEY="..."

# Anthropic for theme extraction
export ANTHROPIC_API_KEY="sk-ant-..."

# Slack delivery
export SLACK_WEBHOOK_URL="..."
```

MCPs in `agent.yaml`: `firecrawl-mcp`, `playwright-mcp`, `slack-mcp`, `gmail-mcp`, `notion-mcp`, `docx`, `pdf`.

## Common recipes

### Recipe 1: Apify Review Intelligence — G2 scrape

```bash
curl -X POST "https://api.apify.com/v2/acts/ramsford~review-intelligence-agent/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["g2"],
    "productSlugs": ["acme-corp"],
    "maxReviewsPerProduct": 500,
    "since": "2026-04-01"
  }'
```

Pay-per-event. Returns: structured reviews with rating, title, body, reviewer-company-size, reviewer-role, pros, cons, support-quality, value-for-money.

### Recipe 2: Apify Review Intelligence — TrustRadius

```bash
curl -X POST "https://api.apify.com/v2/acts/ramsford~review-intelligence-agent/runs?token=$APIFY_TOKEN" \
  -d '{
    "platforms": ["trustradius"],
    "productSlugs": ["acme-corp"],
    "maxReviewsPerProduct": 200
  }'
```

TrustRadius 60% rejection rate — fewer reviews, but each carries higher signal density.

### Recipe 3: Firecrawl direct extraction

```bash
curl -X POST "https://api.firecrawl.dev/v1/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -d '{
    "url": "https://www.g2.com/products/acme-corp/reviews",
    "formats": ["markdown", "json"],
    "schema": {
      "type": "object",
      "properties": {
        "reviews": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "rating": {"type":"number"},
              "title": {"type":"string"},
              "pros": {"type":"string"},
              "cons": {"type":"string"},
              "reviewer_role": {"type":"string"},
              "reviewer_company_size": {"type":"string"},
              "review_date": {"type":"string"}
            }
          }
        }
      }
    }
  }'
```

### Recipe 4: PageCrawl velocity alerts

```bash
curl -X POST "https://api.pagecrawl.io/v1/monitors" \
  -H "Authorization: Bearer $PAGECRAWL_API_KEY" \
  -d '{
    "url": "https://www.g2.com/products/acme-corp/reviews",
    "alert_on": "new_review",
    "webhook_url": "'"$SLACK_WEBHOOK_URL"'",
    "frequency_hours": 6
  }'
```

PageCrawl from $8/mo; pings Slack when new review detected.

### Recipe 5: Capterra (now G2-owned) scrape

```bash
# Capterra URL pattern: https://www.capterra.com/p/<id>/<slug>/
curl -X POST "https://api.firecrawl.dev/v1/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -d '{
    "url": "https://www.capterra.com/p/12345/acme-corp/",
    "formats": ["markdown"]
  }'
```

### Recipe 6: Trustpilot

```bash
curl -X POST "https://api.firecrawl.dev/v1/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -d '{
    "url": "https://www.trustpilot.com/review/acme.example.com",
    "formats": ["markdown"]
  }'
```

### Recipe 7: Glassdoor (ToS-grey — flag)

```bash
# Glassdoor scrape is a SCIP soft-caution; flag in provenance footer
# Approval required from recipient before include
curl -X POST "https://api.firecrawl.dev/v1/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -d '{
    "url": "https://www.glassdoor.com/Reviews/Acme-Corp-Reviews-E123456.htm",
    "formats": ["markdown"]
  }'
```

**Always tag in deliverable provenance footer: `glassdoor — ToS-grey-flagged`.**

### Recipe 8: Top 5 negative / positive theme extraction

```python
import anthropic
client = anthropic.Anthropic()

reviews_text = open("acme_g2_reviews_last_90d.md").read()
prompt = f"""You are a CI analyst. Extract from these G2 reviews of Acme Corp:

1. Top 5 NEGATIVE themes (with example verbatim cons + reviewer role).
2. Top 5 POSITIVE themes (with example verbatim pros + reviewer role).
3. Any emerging theme (mentioned only in L30D, not in prior 60D).
4. Rating distribution by reviewer-company-size and reviewer-role.
5. Average sentiment score 0-10 for support quality, value for money, ease of use.

Reviews:
{reviews_text}

Output JSON.
"""
msg = client.messages.create(
    model="claude-opus-4-7-1m",
    max_tokens=4000,
    messages=[{"role":"user","content":prompt}],
)
```

### Recipe 9: Per-platform rating trend timeseries

```python
import pandas as pd
df = pd.read_csv("acme_reviews_all_platforms.csv")
trend = df.groupby([df["review_date"].dt.to_period("W"), "platform"])["rating"].mean()
trend.unstack().plot(title="Acme — avg rating per week per platform")
```

### Recipe 10: Triangulation for kill-sheet claim

```python
# Two-source minimum per role.md
def triangulate_claim(claim, reviews):
    sources = []
    for r in reviews:
        if claim.lower() in r["cons"].lower() or claim.lower() in r["body"].lower():
            sources.append(f"{r['platform']} review {r['review_id']} (rating {r['rating']}*)")
    return {
        "claim": claim,
        "n_sources": len(sources),
        "passes_triangulation": len(sources) >= 2,
        "sources": sources[:5],
    }

t = triangulate_claim("slow support response", all_reviews)
```

### Recipe 11: NPS proxy from text sentiment

```python
# Score 1-5 ratings to NPS-like proxy
def nps_proxy(reviews):
    promoters = sum(1 for r in reviews if r["rating"] >= 5)
    detractors = sum(1 for r in reviews if r["rating"] <= 2)
    n = len(reviews)
    return (promoters - detractors) / n * 100 if n else 0
```

### Recipe 12: Competitor-response analysis

```python
# Does the competitor reply to negative reviews? How fast?
for r in negative_reviews:
    if r.get("vendor_response"):
        delta = r["vendor_response_date"] - r["review_date"]
        print(f"Response time: {delta.days} days; response tone: {classify(r['vendor_response'])}")
```

### Recipe 13: Slack hot signal on rating shift

```python
def alert_rating_shift(competitor, platform, prior_avg, curr_avg):
    if curr_avg - prior_avg <= -0.2:
        requests.post(SLACK_WEBHOOK_URL, json={
            "text": f":small_red_triangle: {competitor} {platform} rating drop: "
                    f"{prior_avg:.2f} -> {curr_avg:.2f} (L7D)",
            "channel": "#ci-hotline",
        })
```

### Recipe 14: Weekly review digest

```python
sections = {
    "TOP THIS WEEK": "5 new G2 reviews; avg rating 3.8 (vs 4.6 baseline)",
    "EMERGING THEMES": "'crashes after v3.4 update' (3 reviews L7D)",
    "NEW PRAISE": "'fast Slack integration' (top positive L7D)",
    "COMPETITOR RESPONSE": "vendor response time: 2.4 days (vs 1.1 L30D)",
}
```

## Examples

### Example 1: Quarterly kill-sheet refresh

**Goal:** Refresh Acme kill-sheet using last 90 days of review data.

**Steps:**
1. Recipes 1-3, 5-6 → scrape G2 + TrustRadius + Capterra + Trustpilot for Acme L90D.
2. Recipe 8 → LLM theme extraction; top 5 negative.
3. Recipe 10 → triangulate each candidate claim across platforms.
4. PMM approves rebuttal language; render kill sheet via `pandoc-branded-deliverables`.
5. Hand off to `kill-sheet-objection-rebuttals` skill for final authoring.

**Result:** Triangulated, public-source-only kill sheet with 3-5 PMM-approved rebuttals.

### Example 2: Detect Acme support quality decline

**Goal:** Surface support-quality signal as a sales play.

**Steps:**
1. Recipe 8 weekly → "support response" theme in 4 of 8 new G2 reviews L30D.
2. Recipe 12 → Acme vendor-response time 3.8d L30D vs 1.5d prior.
3. Recipe 11 → NPS proxy dropped -8 L30D.
4. Recipe 13 → Slack hot alert.

**Verdict:** Battlecard pane 6 (kill-shots) and kill sheet updated. Sales play: "support quality" comparison.

### Example 3: Velocity alert + battlecard auto-flag

**Goal:** Auto-flag battlecard for refresh when 5+ new reviews drop in 7 days.

**Steps:**
1. Recipe 4 → PageCrawl monitor.
2. On 5+ new reviews L7D → webhook → flag battlecard.
3. PMM review queue notifies via Slack/Linear ticket.

**Result:** Battlecards never stale on review-mined data.

## Edge cases / gotchas

- **G2 review consolidation post-Feb-2026** — Capterra/Software Advice/GetApp now under G2. Don't double-count; treat as one consolidated platform. Combined ~55-58% global share.
- **TrustRadius 60% rejection rate** — higher signal-per-review; but volume small. Don't dismiss small N — verify-and-cite.
- **Glassdoor ToS-grey** — flag in every deliverable; some recipients refuse Glassdoor data entirely.
- **Trustpilot SMB+B2C bias** — strong for self-serve SaaS / B2C; weak for enterprise B2B.
- **Reviewer-role disclosure varies** — G2 captures role + company size; TrustRadius more depth; Capterra less; normalize.
- **Vendor-incentivized reviews** — some competitors offer gift cards; G2 flags but doesn't filter. Note in deliverable.
- **Theme extraction prompt drift** — LLM output drifts; pin prompt + sample 20 reviews/quarter for QA.
- **One-source-anecdote** — single complaint != theme. Two-source minimum per role.md kill-sheet pattern.
- **Country-specific reviews** — G2/TR mostly US; Capterra global; Trustpilot strong EU. Filter by geo for region-specific battlecards.
- **Apify pay-per-event cost** — 1000 reviews ~$2-5; quarterly bulk pulls manageable.
- **PageCrawl 6h frequency floor** — for sub-hour, build a custom monitor; for most CI, 6h is fine.
- **Firecrawl rate limit** — free tier limited; paid tier needed for sustained scrape.
- **Competitor responses count as data** — they reveal CS posture; track vendor_response_date.
- **PII handling** — reviewer-name often partially redacted; never expose in deliverable.
- **PROACTIVE.md cadence** — weekly default; daily for active war-game scenarios.
- **Provenance footer** — every claim cites review ID + URL + retrieval date; Glassdoor entries flagged ToS-grey.

## Sources

- Apify Review Intelligence — https://apify.com/ramsford/review-intelligence-agent
- PageCrawl velocity alerts — https://pagecrawl.io/blog/trustpilot-g2-capterra-review-velocity-alerts
- Aikenhouse Review Platforms 2026 — https://www.aikenhouse.com/post/the-best-software-review-platforms-in-2026
- G2 — https://www.g2.com/
- TrustRadius — https://www.trustradius.com/
- Capterra — https://www.capterra.com/
- Trustpilot — https://www.trustpilot.com/
- Glassdoor — https://www.glassdoor.com/ (ToS-grey, flag in deliverable)
- SCIP Code of Ethics — https://www.scip.org/page/Ethical-Intelligence
- role.md → "Kill-sheet playbook" + "SOTA tool reference" → G2/Capterra/TR/Trustpilot/Glassdoor

## Related skills

- `kill-sheet-objection-rebuttals` — the authoring step after review mining
- `battlecard-authoring-maintenance` — review-mined SWOT into the battlecard
- `competitor-app-intel-sensor-tower-data-ai` — app-store reviews for mobile signal
- `continuous-competitor-monitoring-klue-kompyte-crayon` — review monitoring layer in the fan-out
- `ethical-public-source-methodology` — SCIP code compliance + Glassdoor flagging
