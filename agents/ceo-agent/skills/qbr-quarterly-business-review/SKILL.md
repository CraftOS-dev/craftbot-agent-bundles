<!--
Source: https://www.stellafai.com/post/how-to-run-a-stellar-quarterly-business-review-meeting
QBR — 5-component, 60% decisions, 48h pre-read
-->
# Quarterly Business Review (QBR)

60-min QBR with 48h pre-read. 5-component structure: Strategic Scorecard Snapshot → Exception Report → Initiative Portfolio Review → Forward Look → Decision Log. 60% of meeting time on decisions, not status. Pre-read with clean design (5-8 pages, not 40 slides) sent with note: "Read before — we'll discuss decisions, not present."

## When to use

- Quarterly business review (end of each fiscal quarter).
- Mid-quarter check-in if strategy needs realignment.
- Year-end QBR (heavier, doubles as annual planning kickoff).

Trigger phrases: "QBR prep", "quarterly review", "Q2 review", "QBR deck", "scorecard pre-read", "initiative review".

## Setup

```bash
# pptx for deck
pip show python-pptx

# Linear for initiative portfolio
mcp tool linear.search --query "initiative"

# Notion for pre-read + decision log
mcp tool notion.search --query "QBR"
```

Auth / API key requirements:
- `LINEAR_API_KEY` — for initiative pull (scope `issues:read`).
- `NOTION_API_KEY` — for pre-read + decision log.
- `STRIPE_API_KEY`, `POSTHOG_API_KEY`, `POSTGRES_URL` — for scorecard auto-pull.

## Common recipes

### Recipe 1: Pre-read structure (5-8 pages)

```markdown
# Q2 2027 QBR Pre-read

## Top 3 decisions on the docket (read first)
1. **Should we open Series B in Q3?** — DACI link
2. **Pricing v2 launch — go / no-go** — DACI link
3. **Hiring slowdown? Net zero or +5 in Q3?** — DACI link

## Strategic Scorecard (1 page)
| KPI | Q1 actual | Q2 target | Q2 actual | Status |
|---|---|---|---|---|
| MRR | $48k | $60k | $58k | 🟡 |
| Customers | 142 | 175 | 168 | 🟡 |
| D7 retention | 18% | 25% | 22% | 🟡 |
| North star (Time-to-Ship) | 14min | 10min | 9min | 🟢 |
| Cash | $2.1M | $1.8M | $1.92M | 🟢 |
| Runway | 17mo | 15mo | 16mo | 🟢 |

## Exception Report (red items, 1 page)
- (none red this quarter — first time!)

## Initiative Portfolio (1 page)
| Initiative | DRI | KR | Confidence | Notes |
|---|---|---|---|---|
| Activation v2 | PM Sara | D7 25% (22% actual) | 0.7 | Shipped Q2; iterating |
| VP Eng hire | CEO | Hired by Apr | ✅ Done | Started Apr 5 |
| Enterprise pilot | Head of Sales | 3 close | 0.5 | 2 closed, 1 negotiating |

## Forward Look — Q3 (1 page)
- Carry forward: Activation iteration, Enterprise pilot expansion
- New: Series B prep, Pricing v2 launch, SDR team hire
- Decommission: Vanity-metric tracking (consolidate to North Star + 4)

## Decision Log (running, 1 page)
| Decision | Date | Approver | Outcome | Review |
|---|---|---|---|---|
| Q1: Open Series B Q3 | Apr 15 | CEO | (today's QBR confirms?) | — |
| Q1: Sunset Free plan | Jan 12 | CEO | MRR up 8% post-decision | Done |
```

### Recipe 2: Auto-pull scorecard from data sources

```bash
# MRR from Stripe
MRR=$(curl -s "https://api.stripe.com/v1/balance" -u "$STRIPE_API_KEY:" | jq '.subscriptions.amount / 100')

# D7 retention from PostHog
D7=$(curl -s "https://app.posthog.com/api/projects/$PH_PROJECT_ID/insights/<d7-insight>" -H "Authorization: Bearer $POSTHOG_API_KEY" | jq '.result[0].value')

# Cash from Xero
CASH=$(curl -s "https://api.xero.com/api.xro/2.0/Accounts/<bank>" -H "Authorization: Bearer $XERO_API_KEY" | jq '.Accounts[0].Balance')

# Populate scorecard
cat > qbr-scorecard.md <<EOF
| MRR | \$$MRR |
| D7 | $D7% |
| Cash | \$$CASH |
EOF
```

### Recipe 3: Pull initiative portfolio from Linear

```python
import requests, os
H = {"Authorization": os.environ["LINEAR_API_KEY"]}
query = """
query {
  issues(filter: {labels: {name: {in: ["initiative"]}}, state: {type: {in: ["started","completed"]}}}) {
    nodes { id title state {name} assignee {name} dueDate priority project {name} }
  }
}
"""
issues = requests.post("https://api.linear.app/graphql", headers=H, json={"query":query}).json()["data"]["issues"]["nodes"]
for i in issues:
    print(f"| {i['title']} | {i['assignee']['name']} | {i['state']['name']} | {i['dueDate']} |")
```

### Recipe 4: Build the QBR deck (5-8 slides, clean design)

```python
from pptx import Presentation
prs = Presentation()
sections = [
    "Q2 2027 QBR — top decisions",
    "Strategic Scorecard — KPIs vs target",
    "Exception Report — what's red, why",
    "Initiative Portfolio — top 5 status",
    "Forward Look — Q3 priorities",
    "Decision Log — what we decided today",
]
for title in sections:
    s = prs.slides.add_slide(prs.slide_layouts[1])
    s.shapes.title.text = title
prs.save("qbr-q2-2027.pptx")
```

### Recipe 5: Send pre-read 48h ahead

```bash
mcp tool gmail.send \
  --to "leadership@company.com" \
  --subject "Q2 2027 QBR — 48h pre-read (read before Thu)" \
  --body "QBR Thursday 9am PT.

Pre-read: [Notion link]
Deck: [Drive link]

Top 3 decisions on the docket:
1. Series B Q3 timing
2. Pricing v2 launch
3. Hiring slowdown

Please add comments + questions in pre-read by Wed 5pm. We will use live time for decisions, not status presentations."
```

### Recipe 6: Live agenda — 60% decisions

```markdown
## QBR — 60 min agenda

| Time | Topic | % |
|---|---|---|
| 0-15 | Strategic scorecard snapshot (skim, not read) | 25% |
| 15-30 | Exception report — what's red, what we do | 25% |
| 30-45 | Decisions 1-2-3 from docket — DACI in real-time | 25% |
| 45-55 | Forward Look + Initiative Portfolio (5 min each) | 17% |
| 55-60 | Decision Log writeup + commitments | 8% |

Total: 60% on decisions (rows 3-5). Status compressed to 25%.
```

### Recipe 7: Decisions captured in real-time

```bash
# During the QBR — use Notion live capture
mcp tool notion.create_page \
  --parent '{"page_id":"<decision-log-db>"}' \
  --properties '{
    "Decision":[{"text":{"content":"Series B opens Aug 15, 2027"}}],
    "Date":{"date":{"start":"2027-04-08"}},
    "Approver":{"people":[{"id":"<ceo-id>"}]}
  }' \
  --children-markdown "DACI:
- Driver: CFO
- Approver: CEO
- Contributors: Board, Lead investor
- Informed: Leadership team

Decision: Open Series B process Aug 15, 2027. Target $20M at $80M pre.
Kill criteria: If MRR drops >10% Q2-Q3 → defer to Q4."
```

### Recipe 8: Post-QBR action items → Linear

```bash
# Each decision = 1+ Linear issue with DRI
mcp tool linear.create_issue \
  --team "EXEC" \
  --title "Series B prep — banker selection (per Q2 QBR)" \
  --assignee "cfo@company.com" \
  --due "2027-05-15" \
  --labels "qbr-action,initiative,DRI"
```

### Recipe 9: Forward look — Q3 priority sheet

```markdown
## Q3 2027 Forward Look

### Top 3 priorities (resourced + DRI'd)
1. Series B fundraise — CFO DRI — $250k legal + banker budget
2. Pricing v2 launch — PM Sara DRI — 4 eng + 2 design weeks
3. SDR team hire (3 SDRs) — VP Sales DRI — $180k OTE total + $5k Greenhouse

### What we say NO to
- Mobile app v2 (deferred to Q4)
- Compliance certification (Q4)
- New vertical (decided 6 months out)

### Carry-forward (still in flight)
- Activation v2 iteration (PM Sara)
- Enterprise pilot expansion (Head of Sales)
```

### Recipe 10: QBR decision review (next quarter)

```markdown
## Q1 → Q2 decision review

| Decision | What happened | Process rating | Outcome rating |
|---|---|---|---|
| Sunset Free plan | MRR +8% next month | GOOD | BETTER |
| Series B Q3 timing | (decision in Q2 confirms) | GOOD | TBD |
| Hire VP Eng | Hired Apr 5 | GOOD | TBD (6mo) |

Lessons:
- Sunset Free decision: data-driven, fast — repeat the pattern
- VP Eng search: 12 weeks (target was 10) — investigate retained search alternatives
```

### Recipe 11: QBR cadence calendar (4 per year)

```bash
mcp tool google-calendar.create_event \
  --calendar-id leadership@company.com \
  --summary "QBR — Q2 2027" \
  --start "2027-04-08T09:00:00" \
  --end "2027-04-08T10:00:00" \
  --recurrence "RRULE:FREQ=QUARTERLY;COUNT=4" \
  --description "Pre-read 48h ahead. 60% time on decisions. Decision log captured live."
```

### Recipe 12: QBR template DB

```bash
mcp tool notion.create_database \
  --parent '{"page_id":"<exec-hub>"}' \
  --title '[{"text":{"content":"QBRs"}}]' \
  --properties '{
    "Quarter":{"title":{}},
    "Date":{"date":{}},
    "Pre-read":{"url":{}},
    "Deck":{"url":{}},
    "Decisions made":{"number":{}},
    "Top decision":{"rich_text":{}},
    "Outcomes vs plan":{"rich_text":{}}
  }'
```

## Examples

### Example 1: Full Q2 QBR prep cycle

**Goal:** Land a tight QBR with decisions, not status.

**Steps:**
1. **T-2 weeks:** Auto-pull scorecard (Recipe 2). Auto-pull initiatives (Recipe 3).
2. **T-10 days:** Draft pre-read (Recipe 1). CEO review.
3. **T-7 days:** Build deck (Recipe 4). Iterate with leaders on lowlights.
4. **T-48h:** Send pre-read (Recipe 5). Add 3 top decisions.
5. **T-24h:** Leaders comment in pre-read.
6. **T-0:** Run meeting (Recipe 6). 60% on decisions.
7. **T+0:** Decision log captured live (Recipe 7).
8. **T+4h:** Action items → Linear (Recipe 8).
9. **T+24h:** Forward Look published (Recipe 9).
10. **T+1 quarter:** Review prior QBR decisions (Recipe 10).

**Result:** Tight cycle, decisions made, accountability locked.

### Example 2: Mid-quarter strategy realignment

**Goal:** Major customer churn forces mid-Q3 strategy review.

**Steps:**
1. Call ad-hoc QBR within 1 week.
2. Skip standard scorecard pre-read; focus on the exception.
3. 60-min on: what changed, top 3 decisions, Forward Look revision.
4. Capture decisions same day (Recipe 7).
5. Re-run regular QBR cadence next quarter.

**Result:** Strategy realigned without waiting for next regular QBR.

## Edge cases / gotchas

- **Pre-read late = meeting is status.** Without 48h pre-read, you spend the meeting catching everyone up. Defer if you can't pre-read.
- **No decisions on the docket = no QBR.** If there are no decisions, you don't need a QBR — you need a metrics walk.
- **60% on decisions is non-negotiable.** Without enforcement, the meeting drifts to status. Time-box ruthlessly.
- **Deck > 8 slides = pre-read failure.** Long decks signal you're presenting status. Cap at 8.
- **Decision log captured live = better than 24h-later.** Memory drifts; capture in the meeting.
- **DACI per decision.** Every decision in the QBR has a DACI. Approver named. Single.
- **Exception report skipping greens.** Don't waste time on greens; only red/amber.
- **Forward Look is resourced or it's fluff.** Each Q3 priority has DRI + budget + KR.
- **Carry-forward vs new.** Make this distinction explicit; otherwise team feels nothing finishes.
- **Decision review compounds learning.** Skipping the look-back at next QBR = no institutional memory.
- **Initiative count creep.** Cap at 5 top initiatives. More = unclear focus.
- **CEO + CFO co-leadership of QBR.** CFO owns scorecard pull + financial framing; CEO owns decisions. Split roles.
- **Don't skip the celebration.** 2-3 min on the green/wins. Energy matters.

## Sources

- [Stellafai — How to run a stellar QBR](https://www.stellafai.com/post/how-to-run-a-stellar-quarterly-business-review-meeting)
- [Sybill — QBR templates and best practices](https://www.sybill.ai/blogs/qbr-templates-agendas-and-best-practices)
- [David Sacks operating cadence](https://www.capitaly.vc/blog/david-sacks-operating-cadence-weekly-metrics-okrs-ceo-dashboard)
- [Linear initiatives docs](https://linear.app/docs/projects)
