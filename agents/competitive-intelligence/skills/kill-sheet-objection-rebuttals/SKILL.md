<!--
Sources: Apify Review Intelligence https://apify.com/ramsford/review-intelligence-agent
         Aikenhouse Review Platforms 2026 https://www.aikenhouse.com/post/the-best-software-review-platforms-in-2026
         PageCrawl velocity alerts https://pagecrawl.io/blog/trustpilot-g2-capterra-review-velocity-alerts
Companion playbook: role.md → "Kill-sheet playbook" + "Kill-sheet template"
-->

# Kill-sheet authoring (objection rebuttals)

Per-competitor 1-pager: "When prospect says X" → "Rep says Y." Review-mined objections (G2 / TrustRadius / Capterra / Trustpilot, top 5 negative themes), PMM-approved rebuttals, public-evidence per claim. Refreshed quarterly + on any new G2 review batch.

## When to use

- "Refresh the kill sheet for [competitor]"
- "What's our rebuttal to [verbatim objection]?"
- After 5+ new G2 reviews on a competitor
- Pre-deal: rep asks "how do I handle their X claim?"
- Quarterly PMM kill-sheet refresh

## When NOT to use

- Full battlecard (kill sheet is a subset) → use `battlecard-authoring-maintenance`
- Review monitoring (not authoring) → use `competitor-review-g2-trustradius-capterra`
- Pricing-only objections → use `competitor-pricing-tier-comparison`

## Setup

```bash
# Apify Review Intelligence (pay-per-event)
export APIFY_TOKEN="..."

# PageCrawl velocity alerts ($8+/mo)
export PAGECRAWL_API_KEY="..."

# Firecrawl direct
export FIRECRAWL_API_KEY="..."

# Anthropic for theme extraction
export ANTHROPIC_API_KEY="sk-ant-..."
```

MCPs in `agent.yaml`: `firecrawl-mcp`, `playwright-mcp`, `slack-mcp`, `notion-mcp`, `docx`, `pdf`, `gmail-mcp`.

## Common recipes

### Recipe 1: Apify Review Intelligence — scrape G2 reviews

```bash
curl -X POST "https://api.apify.com/v2/acts/ramsford~review-intelligence-agent/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms":["g2","trustradius","capterra","trustpilot"],
    "competitorUrls":[
      "https://www.g2.com/products/acme-corp/reviews",
      "https://www.trustradius.com/products/acme-corp/reviews"
    ],
    "sinceDays":90,
    "extract":["rating","title","pros","cons","date","reviewer_role","industry"]
  }'
# Returns Apify run ID; poll for completion + pull dataset
```

### Recipe 2: Firecrawl direct review extraction

```python
from firecrawl import FirecrawlApp
fc = FirecrawlApp(api_key=os.environ["FIRECRAWL_API_KEY"])
out = fc.scrape_url("https://www.g2.com/products/acme-corp/reviews",
                    params={"formats":["markdown"],"onlyMainContent":True})
# parse markdown → pull "cons" sections + ratings
```

### Recipe 3: LLM top-5 theme extraction

```python
import anthropic, json
client = anthropic.Anthropic()
prompt = f"""From these {len(reviews)} reviews, extract top 5 negative themes + top 5 positive themes.
Output JSON: {{
  "negative_themes":[{{"theme":"short label","support":int,"sample_quotes":["v1","v2"]}}],
  "positive_themes":[{{"theme":"short label","support":int,"sample_quotes":["v1","v2"]}}]
}}
Rules:
- Each theme needs ≥2 reviews supporting it.
- Use verbatim review fragments for quotes.
- Reject themes with only 1 supporting review.

Reviews:
{json.dumps(reviews)}
"""
resp = client.messages.create(model="claude-sonnet-4-5-20250929",
    max_tokens=3000, messages=[{"role":"user","content":prompt}])
themes = json.loads(resp.content[0].text)
```

### Recipe 4: Cross-reference to our differentiators

```yaml
# our-differentiators.yaml — PMM-owned
differentiators:
  - id: snowflake-pushdown
    name: Snowflake pushdown SQL
    addresses_objections: ["acme-snowflake-integration"]
    pmm_language: "Our pushdown SQL runs 3x faster on Snowflake vs theirs."
    public_evidence:
      - https://us.example.com/case-studies/listco
      - https://us.example.com/benchmarks/snowflake
```

### Recipe 5: Kill-sheet JSON schema

```json
{
  "competitor":"acme-corp",
  "last_refresh":"2026-06-11",
  "pmm_approved":"2026-06-01",
  "pmm_owner":"@pmm-lead",
  "rebuttals":[
    {
      "objection":"Acme has better Snowflake integration",
      "rebut":"Our Snowflake pushdown SQL runs 3x faster than theirs — see ListCo case study.",
      "differentiator":"snowflake-pushdown",
      "sources":[
        "https://www.g2.com/products/acme/reviews/45678",
        "https://us.example.com/case-studies/listco"
      ]
    },
    {
      "objection":"Their pricing is lower at SMB",
      "rebut":"True at $19 entry; our $29 includes SSO that Acme charges $5/seat for. Net cost equal at 6 seats.",
      "sources":["https://acme.example.com/pricing","https://us.example.com/pricing"]
    }
  ],
  "proof_points":[
    {"kind":"case-study","title":"ListCo migrated from Acme","url":"https://us.example.com/case-studies/listco"},
    {"kind":"g2-quote","verbatim":"After 6 months on us, NPS up 22","g2_url":"https://www.g2.com/.../12345"}
  ]
}
```

### Recipe 6: PMM approval workflow

```python
# Same shape as battlecard-authoring-maintenance Recipe 8
# Slack PMM owner with diff + 1-line preview; set pmm_approved date on :white_check_mark: reaction
```

### Recipe 7: Render branded 1-pager (docx + pdf)

```python
from docx import Document
doc = Document()
doc.add_heading(f"Kill sheet — vs {ks['competitor']}", 0)
doc.add_paragraph(f"Last refresh: {ks['last_refresh']} · PMM approved: {ks['pmm_approved']}").italic = True
for r in ks["rebuttals"]:
    doc.add_heading(f"When prospect says: \"{r['objection']}\"", level=2)
    p = doc.add_paragraph("Rep says: ")
    p.add_run(r["rebut"]).bold = True
    doc.add_paragraph("Sources: " + ", ".join(r["sources"]))
doc.save(f"killsheets/{ks['competitor']}.docx")
# Convert to PDF via docx → pdf MCP
```

### Recipe 8: PageCrawl review-velocity alert

```bash
curl -X POST "https://api.pagecrawl.io/v1/monitors" \
  -H "Authorization: Bearer $PAGECRAWL_API_KEY" \
  -d '{
    "url":"https://www.g2.com/products/acme-corp/reviews",
    "kind":"review-velocity",
    "threshold":{"new_reviews_per_day":3},
    "webhook":"https://hooks.slack.com/services/..."
  }'
```

Fires when ≥3 new reviews land in a day → trigger kill-sheet refresh.

### Recipe 9: Two-source triangulation enforcement

```python
def validate(rebuttal):
    if len(rebuttal["sources"]) < 2:
        raise ValueError(f"Need ≥2 sources for: {rebuttal['objection']}")
    return True
# Run before push; refuse single-source claims (antipattern #6 in role.md)
```

### Recipe 10: Quarterly accumulated theme roll-up

```python
import yaml, glob, collections
all_themes = []
for f in glob.glob("themes/*.json"):
    all_themes.extend(json.load(open(f))["negative_themes"])
c = collections.Counter()
for t in all_themes:
    c[t["theme"]] += t["support"]
print("Top 10 cumulative objection themes:", c.most_common(10))
```

### Recipe 11: TrustRadius signal-per-review weighting

```python
# TrustRadius rejects 60% of submissions; signal-per-review higher.
# Weight TrustRadius reviews 2x vs G2/Capterra in theme support tally.
weight = {"trustradius":2.0, "g2":1.0, "capterra":1.0, "trustpilot":1.0, "glassdoor":1.0}
support = sum(weight[r["source"]] for r in reviews if t["theme"] in r["text"])
```

## Examples

### Example 1: Quarterly Acme kill-sheet refresh

**Goal:** Refresh top-3-objection kill sheet using Q2 G2 + TrustRadius reviews.

**Steps:**
1. Recipe 1 (Apify) → scrape G2 + TrustRadius last-90-day reviews.
2. Recipe 3 → top 5 negative themes; weight TrustRadius 2x (Recipe 11).
3. For top 3 themes, cross-reference our differentiators (Recipe 4).
4. Draft rebuttals; Recipe 6 → PMM-approve.
5. Recipe 9 → validate ≥2 sources per rebuttal.
6. Recipe 7 → render docx + pdf; commit JSON; surface in Notion + Slack.

**Result:** Acme kill-sheet refreshed with PMM-approved language + public evidence.

### Example 2: Refresh-on-review-batch trigger

**Goal:** PageCrawl fires "5 new G2 reviews on Acme" — re-evaluate without full quarterly cycle.

**Steps:**
1. Recipe 8 alert fires.
2. Re-scrape last 14 days reviews (Recipe 1 with `sinceDays:14`).
3. Run Recipe 3 — flag any new theme not already on kill sheet.
4. PMM-approve new rebuttal if needed.
5. Push update; Slack-announce.

**Result:** Kill sheet refreshed within 24 hours of meaningful new review batch.

## Edge cases / gotchas

- **Single-source rebuttals** — antipattern #6 in role.md. Enforce ≥2 source via Recipe 9.
- **G2 review incentive bias** — G2 incentivizes reviews; positive skew. Weight TrustRadius (60% rejection) higher per Recipe 11.
- **Verbatim quote safety** — copy verbatim reviewer fragments only; never paraphrase to sharpen the objection.
- **PMM language change** — if our differentiator language shifts (rebrand), trigger kill-sheet re-validation across all competitors.
- **Stale review batch** — reviews older than 12 months may reflect resolved issues; weight recent reviews higher in theme tally.
- **Rebuttal sharpness vs accuracy** — "their support is terrible" is sharper than "support response time exceeds 48hrs in 4 of 10 recent G2 reviews." Sharpness loses if buyer fact-checks. Stay grounded.
- **Apify cost creep** — pay-per-event; running daily across 10 competitors gets expensive. Run weekly + use PageCrawl velocity alert as trigger.
- **5 rebuttals max** — kill sheet is load-bearing; not encyclopedic. Top-3 is best; 5 is hard cap.
- **Source rot** — G2 review URLs change on platform redesign; cite review ID + URL.
- **Apify rate limit** — actor runs queue; expect 1-3 min latency per platform; batch by day.
- **TrustRadius access pattern** — sometimes requires user-agent; firecrawl handles this; bare requests can 403.

## Sources

- Apify Review Intelligence — https://apify.com/ramsford/review-intelligence-agent
- Aikenhouse — Best Software Review Platforms 2026 — https://www.aikenhouse.com/post/the-best-software-review-platforms-in-2026
- PageCrawl — review velocity alerts — https://pagecrawl.io/blog/trustpilot-g2-capterra-review-velocity-alerts
- G2 — https://www.g2.com/
- TrustRadius — https://www.trustradius.com/
- role.md → "Kill-sheet playbook" + "Kill-sheet template" (this bundle)

## Related skills

- `competitor-review-g2-trustradius-capterra` — review monitoring source
- `battlecard-authoring-maintenance` — kill-sheet rebuttals feed battlecard pane 2 + 6
- `win-loss-ci-integration-klue-insider` — quarterly themes from interviews
- `ethical-public-source-methodology` — provenance footer
- `ci-delivery-slack-crm-klue-insider` — Salesforce surface mechanics
