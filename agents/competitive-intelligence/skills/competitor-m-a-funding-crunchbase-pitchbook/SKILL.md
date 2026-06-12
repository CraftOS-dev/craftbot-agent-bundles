<!--
Sources: Crunchbase https://data.crunchbase.com/docs/using-the-api
         PitchBook https://pitchbook.com/
         Owler https://www.owler.com/
         CB Insights https://www.cbinsights.com/
         SEC EDGAR https://www.sec.gov/edgar/sec-api-documentation
         Harmonic — Crunchbase alternatives 2026 https://harmonic.ai/blog/top-crunchbase-competitors-and-alternatives-in-2026
         Otio — Crunchbase vs PitchBook https://otio.ai/blog/crunchbase-vs-pitchbook
Companion playbook: role.md → "Signal layer cadence" → M&A row + "SOTA tool reference"
-->

# Competitor M&A + funding (Crunchbase / PitchBook / Owler / CB Insights / SEC EDGAR)

Funding rounds, investor relationships, key personnel changes, acquisitions, M&A pipeline. Crunchbase Pro for startup funding depth ($588/yr). PitchBook for VC/PE deal-term depth + LP intel ($12-15k/seat/yr). Owler for org-level competitive news alerts + exec changes (15M companies). CB Insights for emerging-tech + market maps. SEC EDGAR for public-company filings (free). Free fallback: SEC + press feed (`ai-news-collectors`) + GDELT + Crunchbase Basic ($49/mo).

## When to use

- "Track [competitor]'s M&A and funding"
- "Did Acme raise / get acquired?"
- "Who are Acme's investors?"
- Exec moves + leadership tracking (Owler exec-change feed)
- New competitor entrant detection (CB Insights / Crunchbase)
- Pre-war-games scenario "competitor acquires X"
- Quarterly funding-round digest

## When NOT to use

- Public-company quarterly earnings deep dive → SEC EDGAR via `sec-edgar-mcp` directly
- Patent / R&D direction → USPTO via `uspto-mcp`
- Hiring as growth signal → use `competitor-hiring-intel-linkedin-sales-nav`
- Analyst-report-driven coverage → use `analyst-relations-watching-gartner-forrester`

## Setup

```bash
# Crunchbase ($49/mo Basic; $99/mo Pro; $588/yr Starter; enterprise)
export CRUNCHBASE_API_KEY="..."
export CRUNCHBASE_API_BASE="https://api.crunchbase.com/api/v4"

# PitchBook (enterprise, $12-15k/seat/yr)
export PITCHBOOK_API_KEY="..."

# Owler (exec change + news alerts)
export OWLER_API_KEY="..."

# CB Insights (enterprise)
export CBINSIGHTS_API_KEY="..."

# SEC EDGAR — free; user agent required
export EDGAR_USER_AGENT="CraftBot CI ci@example.com"

# ai-news-collectors via free skill

# Slack
export SLACK_WEBHOOK_URL="..."
```

MCPs in `agent.yaml`: `sec-edgar-mcp`, `firecrawl-mcp`, `slack-mcp`, `gmail-mcp`, `notion-mcp`, `cli-anything`.

## Common recipes

### Recipe 1: Crunchbase — funding-rounds endpoint

```bash
curl "$CRUNCHBASE_API_BASE/searches/funding_rounds" \
  -H "X-cb-user-key: $CRUNCHBASE_API_KEY" \
  -d '{
    "query": [
      {"type":"predicate","field_id":"funded_organization_identifier","operator_id":"includes","values":["acme-corp"]},
      {"type":"predicate","field_id":"announced_on","operator_id":"gte","values":["2026-04-01"]}
    ],
    "field_ids":["announced_on","money_raised","investment_type","investor_identifiers"],
    "order":[{"field_id":"announced_on","sort":"desc"}],
    "limit":50
  }'
```

### Recipe 2: Crunchbase — key-personnel diff

```bash
curl "$CRUNCHBASE_API_BASE/entities/organizations/acme-corp?\
field_ids=name,founders,executives" \
  -H "X-cb-user-key: $CRUNCHBASE_API_KEY"
```

Snapshot weekly; diff exec roster to detect C-suite changes.

### Recipe 3: Crunchbase — acquisitions

```bash
curl "$CRUNCHBASE_API_BASE/searches/acquisitions" \
  -H "X-cb-user-key: $CRUNCHBASE_API_KEY" \
  -d '{
    "query": [
      {"type":"predicate","field_id":"acquirer_identifier","operator_id":"includes","values":["acme-corp"]}
    ],
    "field_ids":["announced_on","price","acquiree_identifier"]
  }'
```

### Recipe 4: PitchBook — deal terms

```bash
curl -H "Authorization: Bearer $PITCHBOOK_API_KEY" \
  "https://api.pitchbook.com/v1/companies/acme-corp/deals?\
since=2026-01-01&\
include=valuation,investors,deal_type,round_size,participation_rights"
```

PitchBook reveals deal terms (preferred-stock structure, liquidation prefs, board seats) that Crunchbase doesn't.

### Recipe 5: Owler — exec change alerts

```bash
curl -H "Authorization: Bearer $OWLER_API_KEY" \
  "https://api.owler.com/v1/orgs/acme-corp/news?\
category=executive_changes&\
since=2026-04-01"
```

Owler tracks 15M companies; specializes in org-level competitive news + exec changes.

### Recipe 6: Owler — competitive-news feed

```bash
curl -H "Authorization: Bearer $OWLER_API_KEY" \
  "https://api.owler.com/v1/orgs/acme-corp/competitive-news?\
since=2026-04-01"
```

### Recipe 7: SEC EDGAR — recent 8-K filings (free)

```bash
# 8-K = material event filing (M&A, exec change, big customer loss)
curl -A "$EDGAR_USER_AGENT" \
  "https://data.sec.gov/submissions/CIK0001234567.json" | \
  jq '.filings.recent | select(.form[] == "8-K")'
```

### Recipe 8: SEC EDGAR — 10-K risk factors

```bash
# 10-K Item 1A.Risk Factors mentions competitors + market dynamics
curl -A "$EDGAR_USER_AGENT" \
  "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001234567&type=10-K&dateb=&owner=include&count=10"
```

### Recipe 9: CB Insights — market map + competitors

```bash
curl -H "Authorization: Bearer $CBINSIGHTS_API_KEY" \
  "https://api.cbinsights.com/v1/market-maps/saas-sales-engagement"
```

Useful for: detect new competitor entrants you didn't have in your comp set.

### Recipe 10: ai-news-collectors press feed (free)

```python
from ai_news_collectors import collect
items = collect(
    queries=["Acme Corp funding", "Acme acquires", "Acme Series", "Acme CEO"],
    sources=["techcrunch","theinformation","businesswire","prnewswire","reuters"],
    since="2026-05-01",
)
```

### Recipe 11: GDELT global news (free)

```python
from gdeltdoc import GdeltDoc, Filters
f = Filters(keyword="Acme Corp acquires", start_date="2026-04-01", end_date="2026-06-11")
articles = GdeltDoc().article_search(f)
```

### Recipe 12: Material-event flash brief

```python
def flash_brief_funding(competitor, round_size, investors, announced):
    return f"""**FLASH CI BRIEF — {competitor} funding**
Round: ${round_size:,} ({round_type})
Investors: {', '.join(investors)}
Announced: {announced}
Implications:
  - Likely 18-24 month runway extension
  - Watch for hiring surge in next 90 days
  - Possible pricing aggressiveness (subsidy by capital)
Battlecard pane 4 (parity) + pane 5 (pricing leverage) flagged for refresh.
"""
```

### Recipe 13: Slack hot signal on M&A

```python
def alert_ma(acquirer, acquiree, price=None, announced=None):
    requests.post(SLACK_WEBHOOK_URL, json={
        "blocks":[
            {"type":"header","text":{"type":"plain_text",
             "text":f":briefcase: {acquirer} acquires {acquiree}"}},
            {"type":"section","text":{"type":"mrkdwn",
             "text":f"*Price:* {price or 'undisclosed'}\n*Announced:* {announced}"}}
        ],
        "channel":"#ci-hotline",
    })
```

### Recipe 14: Multi-source dedup

```python
# Crunchbase + Owler + press may report same event with different timestamps
events = {}
for e in fetch_from_all_sources():
    key = (e["competitor"], e["event_type"], e["date"][:10])
    if key not in events:
        events[key] = e
    else:
        events[key]["sources"].append(e["source"])
# Output: deduped event list with multi-source confirmation
```

### Recipe 15: Quarterly funding-round digest

```python
# Per competitor, sum funding L4 quarters; build trend
import pandas as pd
df = pd.DataFrame(funding_events)
df["quarter"] = df["announced_on"].dt.to_period("Q")
trend = df.groupby(["competitor","quarter"])["money_raised"].sum().unstack()
```

## Examples

### Example 1: Acme raises Series D — full pipeline

**Goal:** Detect + brief + flag-battlecard within 1 hour.

**Steps:**
1. Recipe 10 → ai-news-collectors flags TechCrunch article.
2. Recipe 1 → Crunchbase confirms: $120M Series D, lead investor a16z, 2026-06-09.
3. Recipe 14 → dedup against Owler news (Recipe 6).
4. Recipe 12 → flash brief generated.
5. Recipe 13 → `#ci-hotline` post.
6. Auto-flag battlecard pane 4 + pane 5.
7. War-games scenario triggers: "Acme uses Series D to undercut pricing." Update playbook.

**Result:** Sales leadership briefed in 1h; battlecards refreshed within the day.

### Example 2: Detect Acme acquires BetaInc

**Goal:** Trigger competitive cascade when competitor acquires a partner-adjacent company.

**Steps:**
1. Recipe 3 → Crunchbase acquisitions endpoint flags BetaInc as acquired.
2. Recipe 7 → SEC EDGAR 8-K filed (if public).
3. Recipe 11 → GDELT confirms global news pickup.
4. Cross-reference: is BetaInc one of our channel partners?
5. War-games: scenario "competitor acquires our channel partner."
6. Battlecard, kill-sheet, channel-strategy all flagged for review.

### Example 3: Exec move flash brief (Owler trigger)

**Goal:** Acme CTO departs → flash brief.

**Steps:**
1. Recipe 5 → Owler exec-change webhook fires.
2. Recipe 2 → Crunchbase confirms exec field updated.
3. Recipe 10 → ai-news-collectors picks up press confirmation.
4. Triangulated (3 sources) → flash brief sent.
5. Battlecard pane 3 (latest deal intel) refreshed.

### Example 4: Free path — no paid Crunchbase / PitchBook

**Goal:** Track competitor funding without paid CI tooling.

**Steps:**
1. Recipe 10 → ai-news-collectors daily for press.
2. Recipe 11 → GDELT for global pickup.
3. Recipe 7 → SEC EDGAR for public-company filings (free).
4. Recipe 5 → Owler trial / free tier for exec changes (limited).
5. Mark confidence as `inferred (press-only, no Crunchbase confirmation)` until confirmed.

**Result:** ~80% coverage on a $0 budget; misses non-public early-stage details.

## Edge cases / gotchas

- **Crunchbase Basic vs Pro vs Enterprise** — Basic ($49/mo) limited API; Pro ($99/mo) higher limits; Enterprise has full API. Match plan to comp-set size.
- **Crunchbase data freshness** — public-funding announcements usually within 24h; some private rounds lag weeks.
- **PitchBook seat cost** — $12-15k/seat/yr; usually a finance/strategy seat; coordinate with that team.
- **Owler false positives on exec change** — sometimes flags promotions as departures. Verify via LinkedIn (`competitor-hiring-intel-linkedin-sales-nav` Recipe 2 alumni filter).
- **SEC EDGAR rate limit** — 10 rps with proper User-Agent header. Stay under or get throttled.
- **8-K interpretation** — Item 1.01 (material agreement), 2.01 (acquisition), 5.02 (exec change). Map Items to event types.
- **Press release pump-and-dump** — undisclosed amounts ("strategic investment") often inflate by acquirer; cite "undisclosed" without inferring.
- **Bridge rounds + extensions** — common; don't double-count Series B + Series B extension as 2 rounds.
- **Investor signal noise** — same investor leads many rounds; presence of a16z doesn't mean Acme is special. Use investor-quality only as one input.
- **Stealth-mode competitors** — pre-launch; only visible via Crunchbase founder profile / LinkedIn / patents.
- **CB Insights market maps** — refreshed quarterly; add new entrants you missed.
- **Multi-jurisdiction filings** — EU competitor may file with Companies House (UK) or local equivalent. SEC EDGAR doesn't cover.
- **Don't infer ARR from funding** — "raised $50M Series C" doesn't equal $X ARR. Common misuse.
- **PROACTIVE.md cadence** — weekly default per signal layer; quarterly for SEC filings; on-trigger for 8-K + funding press.
- **Provenance footer** — every claim cites Crunchbase / PitchBook / SEC / press URL + retrieval date.

## Sources

- Crunchbase API docs — https://data.crunchbase.com/docs/using-the-api
- Crunchbase Basic ($49/mo) — https://www.crunchbase.com/products
- PitchBook — https://pitchbook.com/
- Owler — https://www.owler.com/
- CB Insights — https://www.cbinsights.com/
- SEC EDGAR API — https://www.sec.gov/edgar/sec-api-documentation
- Harmonic — Top Crunchbase alternatives 2026 — https://harmonic.ai/blog/top-crunchbase-competitors-and-alternatives-in-2026
- Otio — Crunchbase vs PitchBook — https://otio.ai/blog/crunchbase-vs-pitchbook
- GDELT — https://www.gdeltproject.org/
- role.md → "Capability reference" → M&A row + "SOTA tool reference"

## Related skills

- `competitor-hiring-intel-linkedin-sales-nav` — exec-move triangulation
- `continuous-competitor-monitoring-klue-kompyte-crayon` — M&A is one fan-out layer
- `war-games-competitive-mock-scenarios` — funding/acquisition triggers a scenario re-run
- `battlecard-authoring-maintenance` — pane 3 + pane 5 refresh on funding event
- `analyst-relations-watching-gartner-forrester` — analyst reports often follow material events
