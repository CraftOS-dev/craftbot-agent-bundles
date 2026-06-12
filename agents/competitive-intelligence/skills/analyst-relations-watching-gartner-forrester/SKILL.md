<!--
Sources: Gartner Magic Quadrant https://www.gartner.com/en/research/magic-quadrant
         Forrester Wave https://go.forrester.com/research/the-forrester-wave/
         IDC MarketScape https://www.idc.com/marketscape
         Constellation ShortList https://www.constellationr.com/research/shortlists
         451 Research / S&P https://www.spglobal.com/marketintelligence/en/mi/products/451-research.html
         AlphaSense https://www.alpha-sense.com/
         Mendix — Gartner Forrester guide https://www.mendix.com/evaluation-guide/gartner-forrester-mendix/
Companion playbook: role.md → "Analyst-relations playbook" + "SOTA tool reference" → AlphaSense / Gartner / Forrester
-->

# Analyst-relations watching (Gartner MQ / Forrester Wave / IDC MarketScape / Constellation ShortList)

Track competitor position in Gartner Magic Quadrant + Forrester Wave + IDC MarketScape + Constellation ShortList + 451 / Omdia per category. Per-report diff: axis movement (Vision ↔ Execution / Strategy ↔ Current Offering), quadrant change (Leader / Challenger / Visionary / Niche), new/retired dimensions. Capture quotable analyst lines per competitor. Pair with analyst-quote citation tracking — when competitor lands a Gartner/Forrester quote in PR, flag it. AlphaSense for AI-powered search across analyst content (paid).

## When to use

- "Track the new Gartner MQ release"
- "Did Acme become a Leader on the Forrester Wave?"
- New report drop (Gartner / Forrester / IDC / Constellation)
- Competitor PR cites analyst — flag
- Pre-RFP: which competitors are top-right-quadrant in this category?
- Quarterly analyst-relations roll-up to leadership

## When NOT to use

- M&A / funding driving analyst coverage → use `competitor-m-a-funding-crunchbase-pitchbook`
- General press coverage → use `continuous-competitor-monitoring-klue-kompyte-crayon` ai-news-collectors layer
- Internal positioning / messaging → out of scope (use `competitor-messaging-tracking-diff`)

## Setup

```bash
# Gartner subscription ($5-30k/seat/yr) — recipient supplies
export GARTNER_USERNAME="..."  # OAuth via Gartner portal

# Forrester subscription
export FORRESTER_USERNAME="..."

# IDC MarketScape (per-report purchase or subscription)
# Constellation ShortList (mid-tier subscription)
# 451 Research / S&P Market Intelligence (enterprise)

# AlphaSense (enterprise; $10k+/seat/yr)
export ALPHASENSE_API_KEY="..."

# Free fallback: press coverage
# ai-news-collectors + Firecrawl + Google Scholar (for citations)
export FIRECRAWL_API_KEY="..."

# Slack
export SLACK_WEBHOOK_URL="..."
```

MCPs in `agent.yaml`: `firecrawl-mcp`, `playwright-mcp`, `slack-mcp`, `gmail-mcp`, `notion-mcp`.

## Common recipes

### Recipe 1: Subscription portal scrape (recipient's legit access)

```python
# Use Playwright with recipient's session cookie
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(storage_state="gartner_session.json")
    page = ctx.new_page()
    page.goto("https://www.gartner.com/document/MQ-Sales-Engagement-2026")
    # Scrape DOM for figure + analyst commentary
    figure_url = page.query_selector("img.mq-figure").get_attribute("src")
    analyst_text = page.query_selector("div.analyst-commentary").text_content()
```

Recipient logs in via Playwright headed once to seed `storage_state`. Then headless re-use.

### Recipe 2: Per-report axis-position capture

```yaml
# data/analyst-reports/gartner-mq-sales-engagement-2026.yaml
report:
  vendor: Gartner
  type: Magic Quadrant
  category: Sales Engagement Platforms
  published: 2026-05-28
  url: https://www.gartner.com/document/MQ-Sales-Engagement-2026
positions:
  - vendor: Salesforce
    quadrant: Leader
    ability_to_execute: 8.4
    completeness_of_vision: 8.1
  - vendor: Outreach
    quadrant: Leader
    ability_to_execute: 7.8
    completeness_of_vision: 7.5
  - vendor: Acme Corp
    quadrant: Challenger
    ability_to_execute: 6.9
    completeness_of_vision: 5.4
  - vendor: Beta Inc
    quadrant: Visionary
    ability_to_execute: 4.8
    completeness_of_vision: 7.1
analyst_quotes:
  - vendor: Acme Corp
    quote: "Acme demonstrates strong execution but lacks roadmap clarity for the AI-driven outbound segment."
    source: Magic Quadrant 2026 Strengths/Cautions section
```

### Recipe 3: Per-report diff vs prior cycle

```python
import yaml
prior = yaml.safe_load(open("data/analyst-reports/gartner-mq-sales-engagement-2025.yaml"))
curr  = yaml.safe_load(open("data/analyst-reports/gartner-mq-sales-engagement-2026.yaml"))

def diff_positions(prior, curr):
    p = {v["vendor"]: v for v in prior["positions"]}
    c = {v["vendor"]: v for v in curr["positions"]}
    delta = {}
    for v in set(p) | set(c):
        if v in p and v in c:
            delta[v] = {
                "quadrant_change": (p[v]["quadrant"], c[v]["quadrant"]) if p[v]["quadrant"] != c[v]["quadrant"] else None,
                "execution_delta": c[v]["ability_to_execute"] - p[v]["ability_to_execute"],
                "vision_delta":    c[v]["completeness_of_vision"] - p[v]["completeness_of_vision"],
            }
        elif v in c:
            delta[v] = {"status": "NEW"}
        else:
            delta[v] = {"status": "DROPPED"}
    return delta
```

### Recipe 4: Forrester Wave structure

```yaml
report:
  vendor: Forrester
  type: Wave
  category: Sales Engagement
  published: 2026-04-15
positions:
  - vendor: Acme Corp
    segment: Strong Performer       # vs Leader / Strong Performer / Contender / Challenger
    strategy: 3.8
    current_offering: 4.1
    market_presence: 5
```

### Recipe 5: IDC MarketScape capture

```yaml
report:
  vendor: IDC
  type: MarketScape
  category: Worldwide Sales Engagement
positions:
  - vendor: Acme Corp
    segment: Major Players   # vs Leader / Major Player / Contender / Participant
    capabilities: 3.5         # IDC uses Capabilities + Strategies axis
    strategies: 3.7
```

### Recipe 6: Constellation ShortList

```yaml
# Constellation publishes quarterly; "ShortList" naming
report:
  vendor: Constellation Research
  type: ShortList
  category: Sales Engagement
  published_quarter: Q2-2026
positions:
  - vendor: Acme Corp
    included: true
    rank: 4   # ordered list, not quadrant
```

### Recipe 7: Free fallback — press coverage of report drop

```python
# When subscription unavailable, capture press summaries
from ai_news_collectors import collect
items = collect(
    queries=["Gartner Magic Quadrant Sales Engagement 2026",
             "Forrester Wave Sales Engagement 2026"],
    sources=["techcrunch","theinformation","prnewswire","businesswire"],
    since="2026-04-01",
)
# LLM extract: vendor positions mentioned, quadrant terminology
```

### Recipe 8: AlphaSense AI-powered search

```bash
curl -H "Authorization: Bearer $ALPHASENSE_API_KEY" \
  "https://api.alpha-sense.com/v1/search?\
query=Gartner+Magic+Quadrant+Sales+Engagement+2026+Acme&\
asset_classes=analyst_report,earnings_transcript,industry_report"
```

AlphaSense returns highlighted analyst commentary across the corpus. Gartner CMI MQ Leader 2026 themselves. Incorporated Sentieo features.

### Recipe 9: Analyst-quote capture for battlecard

```python
# When report drops, extract any quotable analyst line per competitor
def extract_quotes(report_text, vendors):
    quotes = {}
    for v in vendors:
        # Find paragraphs mentioning the vendor; extract sentences that are evaluative
        for para in report_text.split("\n\n"):
            if v in para:
                quotes.setdefault(v, []).append(para)
    return quotes
```

### Recipe 10: Update battlecard with analyst position

```python
def update_battlecard(competitor, report, position):
    bc_pane_7 = f"""ANALYST POSITION (latest):
- {report['vendor']} {report['type']} {report['category']}, {report['published']}
- Position: {position['segment'] or position['quadrant']}
- Execution / Current Offering: {position.get('ability_to_execute') or position.get('current_offering')}
- Vision / Strategy: {position.get('completeness_of_vision') or position.get('strategy')}
"""
    klue_update_pane(competitor, pane="analyst", content=bc_pane_7)
```

### Recipe 11: Slack hot-signal on report drop

```python
def alert_report_drop(report, delta):
    blocks = [
        {"type":"header","text":{"type":"plain_text",
         "text":f":books: {report['vendor']} {report['type']} {report['category']} dropped"}},
        {"type":"section","text":{"type":"mrkdwn",
         "text":format_delta_summary(delta)}}
    ]
    requests.post(SLACK_WEBHOOK_URL, json={"channel":"#ci-hotline","blocks":blocks})
```

### Recipe 12: Quarterly analyst-relations roll-up

```python
# Aggregate all reports last quarter; render leadership deck
reports = load_reports(quarter="Q2-2026")
summary = {
    "new_leader_badges": [r for r in reports if any(p["quadrant"] == "Leader" and p["status"] == "promoted" for p in r["positions"])],
    "our_position":      our_position_trend(reports),
    "competitor_movement": competitor_movement_summary(reports),
}
```

### Recipe 13: Analyst-quote citation tracking

```python
# When competitor cites analyst in PR/LP, flag it
def detect_analyst_citation_in_press(competitor_press, known_analysts):
    flags = []
    for press in competitor_press:
        for a in known_analysts:
            if a in press["body"]:
                flags.append({"competitor": press["competitor"], "analyst": a, "url": press["url"]})
    return flags
```

### Recipe 14: Pair analyst grading with feature parity matrix

```python
# Update parity matrix with analyst-graded capability dimensions
def append_analyst_capabilities_to_parity_matrix(report, parity_yaml):
    for vendor_pos in report["positions"]:
        if "capability_dimensions" in vendor_pos:
            for cap, grade in vendor_pos["capability_dimensions"].items():
                parity_yaml.setdefault(cap, {})[vendor_pos["vendor"]] = grade
```

## Examples

### Example 1: Gartner MQ drops — full diff pipeline

**Goal:** New Gartner MQ for Sales Engagement drops; diff vs prior; brief leadership.

**Steps:**
1. Recipe 1 → scrape new MQ via Playwright + recipient session.
2. Recipe 2 → capture positions YAML.
3. Recipe 3 → diff vs 2025 cycle.
4. Recipe 9 → extract quotable lines per competitor.
5. Recipe 10 → update battlecards (each competitor's pane 7).
6. Recipe 11 → Slack hot signal.
7. Recipe 12 → leadership deck slide.

**Result:** Acme moved from Visionary to Challenger; we held Leader; Beta entered Niche. Battlecards refreshed within 24h.

### Example 2: Free path — Forrester Wave drop without subscription

**Goal:** Track Forrester Wave Sales Engagement without paid Forrester access.

**Steps:**
1. Recipe 7 → press coverage via ai-news-collectors.
2. Manual reading of vendor press releases (Acme touts "Strong Performer"; Salesforce announces "Leader").
3. Cross-reference G2 review trend with analyst grading.
4. Note in deliverable: "inferred from press; not verified against Wave document directly."

**Result:** Workable signal on a $0 budget; lower-fidelity than Recipe 1.

### Example 3: AlphaSense for financial-CI analyst depth

**Goal:** Beyond MQ/Wave — find analyst commentary on Acme in earnings transcripts.

**Steps:**
1. Recipe 8 → AlphaSense semantic search "Acme Corp" + recent earnings.
2. Filter to last 4 quarters.
3. Extract analyst Q&A directed at Acme management.
4. Build "what analysts ask Acme" intelligence brief.

**Result:** Deep financial-CI context for war-game scenarios.

### Example 4: Competitor cites analyst — flag and verify

**Goal:** Acme's homepage hero claims "named Leader by Forrester." Verify.

**Steps:**
1. Recipe 13 → detected the citation.
2. Recipe 4 → check Forrester Wave YAML — Acme is `Strong Performer`, not `Leader`.
3. Flag misleading citation; battlecard pane 7 (analyst position) updated with correction.
4. Sales play: factually-correct rebuttal when prospect cites Acme's "Leader" claim.

## Edge cases / gotchas

- **Subscription cost** — Gartner $5-30k/seat/yr; Forrester similar; IDC + Constellation tier-based. Recipient supplies.
- **Per-report ownership** — analyst-firm ToS limits sharing internally; respect distribution clauses.
- **Press summaries are biased** — vendors who placed well issue PR; lagging vendors don't. Press-only signal under-represents losers.
- **Methodology change cycle-to-cycle** — Gartner sometimes adds/retires dimensions; can't always do clean diff. Note methodology change in delta.
- **Analyst-quote misuse** — vendor may quote out of context; verify the full sentence; cite report page/section.
- **Quadrant promotion ≠ market truth** — analyst grading lags market by 6-12 months; treat as one input.
- **Forrester retired Wave for some categories** — e.g., Endpoint Security Wave retired 2025. Track retirement events.
- **Constellation cycle** — quarterly; lower bar than Gartner/Forrester but useful for emerging categories.
- **451 / Omdia / Aragon** — sub-tier coverage; useful for niche categories.
- **Don't pretexting Gartner inquiry** — Gartner inquiry calls require seat; SCIP hard no on pretexting another firm's seat.
- **Conference-talk citation** — analyst public webinars are public; cite + use.
- **AlphaSense gated demos** — sales-gated; recipient handles procurement.
- **Translation** — non-English regional analyst reports common; use `deepl-mcp`.
- **PROACTIVE.md cadence** — on-trigger per report drop; quarterly roll-up.
- **Provenance footer** — cite analyst firm + report title + section + retrieval date.

## Sources

- Gartner Magic Quadrant — https://www.gartner.com/en/research/magic-quadrant
- Forrester Wave — https://go.forrester.com/research/the-forrester-wave/
- IDC MarketScape — https://www.idc.com/marketscape
- Constellation ShortList — https://www.constellationr.com/research/shortlists
- 451 Research / S&P — https://www.spglobal.com/marketintelligence/en/mi/products/451-research.html
- AlphaSense — https://www.alpha-sense.com/
- Mendix — Gartner Forrester evaluation — https://www.mendix.com/evaluation-guide/gartner-forrester-mendix/
- role.md → "Analyst-relations playbook" + "SOTA tool reference" → AlphaSense / Gartner / Forrester

## Related skills

- `battlecard-authoring-maintenance` — pane 7 (analyst position)
- `feature-parity-tracking` — analyst-graded capability dimensions
- `continuous-competitor-monitoring-klue-kompyte-crayon` — analyst drop is one signal source
- `competitor-messaging-tracking-diff` — competitor homepage analyst-citation tracking
- `ethical-public-source-methodology` — Gartner subscription ToS compliance
