<!--
Source: https://www.lennysnewsletter.com/p/how-to-write-a-great-weekly-update
-->
# Stakeholder Update Format — SKILL

Lenny Rachitsky's weekly update format: Wins / Lowlights / Asks / Plans / Metrics. This pack auto-aggregates from Linear (cycle status), Amplitude/Mixpanel/PostHog (KPI deltas), and Dovetail (themes), then distributes via Notion + Gmail + Slack.

## When to use

- Writing the weekly product update for exec / org.
- Monthly product review (extends weekly with OKR check-in).
- Quarterly board update (extends monthly with strategy + "what we learned").
- One-off launch retro updates.

Trigger phrases: "write the weekly update", "stakeholder update", "monthly review", "board update", "what happened this week".

## Setup

```bash
# Aggregator skill — no native API; chains Linear + Analytics + Notion + Gmail + Slack
mcp tool linear.viewer
mcp tool notion.viewer
mcp tool gmail.viewer
mcp tool slack.viewer
```

## Common recipes

### Recipe 1: Weekly update template (Lenny format)

```markdown
# Product Weekly — Week of [YYYY-MM-DD]

## Wins
- **[Outcome statement]** — [what shipped + measured impact + source]
- e.g., "D7 retention 35% → 38% — onboarding revamp shipped Mon (Amplitude funnel, 7-day rolling)"

## Lowlights
- **[What slipped + why + new ETA]** — be honest
- e.g., "Notification center bumped 1 week — API rate-limit issue; new ship date 2026-06-22"

## Asks
- **[Decision needed by date X from person Y]** — explicit
- e.g., "Need exec call on enterprise pricing by Friday — PSM data ready in Notion"

## Plans (next week)
- [3-5 outcome-led commitments — NOT activities]

## Metrics
| Metric | This week | Last week | Δ |
|---|---|---|---|
| Activated users | 1,234 | 1,150 | +7.3% |
| D7 retention | 37.2% | 35.0% | +2.2pp |
| MAU | 18,450 | 18,200 | +1.4% |
| NPS | 42 | 38 | +4 |

## Calendar
- [Major events: launch dates, customer interviews, exec reviews]
```

### Recipe 2: Auto-pull Wins from Linear (completed-this-week)

```bash
# Issues completed in last 7 days, filtered to release-worthy
mcp tool linear.list_issues \
  --filter "{
    \"completedAt\":{\"gte\":\"$(date -d '7 days ago' +%Y-%m-%d)\"},
    \"labels\":{\"name\":{\"eq\":\"release-worthy\"}}
  }" \
  --first 50 \
| jq -r '.nodes[] | "- **\(.title)** — \(.description | split("\n")[0])"' \
> wins.md
```

### Recipe 3: Auto-pull Lowlights from Linear (slipped issues)

```bash
# Issues with cycle past end but not completed
mcp tool linear.list_issues \
  --filter '{
    "cycle":{"endsAt":{"lt":"now"}},
    "state":{"type":{"in":["started","unstarted"]}}
  }' \
  --first 20 \
| jq -r '.nodes[] | "- **\(.title)** — slipped from cycle \(.cycle.name); new ETA TBD"' \
> lowlights.md
```

### Recipe 4: Auto-pull KPI deltas

```python
# Pull this week + last week values from PostHog
import subprocess, json

def query(hogql):
    return json.loads(subprocess.check_output(["mcp","tool","posthog.query","--query",hogql]))

def week_value(metric_sql, week_start_offset):
    sql = f"{metric_sql} WHERE timestamp BETWEEN now() - INTERVAL {week_start_offset+7} DAY AND now() - INTERVAL {week_start_offset} DAY"
    return query(sql)["results"][0][0]

metrics = {
    "Activated users": "SELECT count(DISTINCT person_id) FROM events WHERE event='activation_completed'",
    "D7 retention":   "SELECT avg(d7_retained) FROM cohort_table",
    "MAU":            "SELECT count(DISTINCT person_id) FROM events WHERE event='active_session'",
}

table = "| Metric | This week | Last week | Δ |\n|---|---|---|---|\n"
for name, sql in metrics.items():
    this_wk = week_value(sql, 0)
    last_wk = week_value(sql, 7)
    delta = (this_wk - last_wk) / last_wk * 100 if last_wk else 0
    table += f"| {name} | {this_wk:,.0f} | {last_wk:,.0f} | {'+' if delta>=0 else ''}{delta:.1f}% |\n"

print(table)
```

### Recipe 5: Compose the full update

```bash
DATE=$(date +%Y-%m-%d)
cat > weekly-$DATE.md <<EOF
# Product Weekly — Week of $DATE

## Wins
$(cat wins.md)

## Lowlights
$(cat lowlights.md)

## Asks
- [Manual: enumerate decisions needed]

## Plans (next week)
- [Manual: 3-5 outcomes for next week]

## Metrics
$(cat metrics-table.md)

## Calendar
- [Manual: major upcoming events]
EOF
```

### Recipe 6: Publish to Notion archive

```bash
mcp tool notion.append_block_children \
  --block_id "<weekly-updates-archive-page>" \
  --children "$(jq -Rs '. as $md | [
    {type:"heading_2",heading_2:{rich_text:[{text:{content:"Week of '"$DATE"'"}}]}},
    {type:"paragraph",paragraph:{rich_text:[{text:{content:$md}}]}}
  ]' < weekly-$DATE.md)"
```

### Recipe 7: Email distribution

```bash
mcp tool gmail.send \
  --to "exec-list@your.com" \
  --cc "extended-leads@your.com" \
  --subject "Product Weekly — $(date +%B\ %-d)" \
  --bodyType "markdown" \
  --body "$(cat weekly-$DATE.md)"
```

### Recipe 8: Slack distribution (short form)

```bash
# Slack version: just the headline + Wins + link
WINS=$(head -10 wins.md)
mcp tool slack.post \
  --channel "#product-updates" \
  --text "*Product Weekly — $(date +%b\ %-d)*

$WINS

Full update: https://www.notion.so/weekly-update-$(date +%Y-%m-%d)" \
  --markdown true
```

### Recipe 9: Monthly variant (adds OKR check-in)

```markdown
# Product Monthly — [Month YYYY]

## Wins (this month)
[Roll up 4 weekly wins; top 3-5]

## Lowlights
[Misses + structural issues]

## OKR check-in
### O1: D7 retention 35% → 42%
- KR1: D7 retention currently 38.5% (54% to target) — 🟢 On track
- KR2: Time-to-first-value 8min (was 14min) — 🟢 On track

## Asks
[Decision-makers needed for cross-team]

## Plans (next month)
[2-4 outcomes; team-level commitments]

## Metrics (full)
[Expanded KPI table including LTV/CAC/ARPU if applicable]

## What we learned
[1-2 paragraphs of insights — discovery, customer themes, market signal]
```

### Recipe 10: Quarterly board update

```markdown
# Product Q3 2026 — Board Update

## Headline
[1 paragraph: the story of the quarter]

## What we set out to do
[Q3 OKR objectives — verbatim from Lattice]

## Outcomes (vs targets)
[Each KR: actual / target / status — citing source]

## What worked
[2-3 wins with cause-effect explanation]

## What didn't
[2-3 misses with diagnosis]

## What we learned
[Customer insights, market shifts, strategy refinements]

## Q4 intent
[3-5 themes — NOT roadmap commitments]

## Asks of the board
[Decisions, hiring approvals, budget shifts]
```

## Examples

### Example 1: Friday afternoon weekly update
**Goal:** Generate and send by 4pm Friday.

**Steps:**
1. Run Recipe 2 (Wins from Linear).
2. Run Recipe 3 (Lowlights — slipped issues).
3. Run Recipe 4 (KPI deltas).
4. Manually fill Asks + Plans (the human-judgment parts).
5. Recipe 5 composes; Recipe 6 archives; Recipes 7-8 distribute.

**Result:** A consistent, cited, actionable update — without 90 minutes of compilation.

### Example 2: End-of-quarter board prep
**Goal:** Pull together the Q3 board update.

**Steps:**
1. Pull final OKR statuses from Lattice (see `okrs-lattice-tracking`).
2. Aggregate 12 weeks of weeklies into headline themes.
3. Pull KPI quarter-over-quarter from PostHog/Amplitude.
4. Synthesize Dovetail learnings (top 3 themes from the quarter's research).
5. Compose using Recipe 10.
6. Draft → review by exec → publish to board Notion page.

**Result:** Cited, defensible Q3 board update with clear "what worked / what didn't / what we learned."

## Edge cases / gotchas

- **Vague Wins.** "Made progress on X" is not a win. Wins have measured impact, citation, and an outcome statement.
- **Hiding Lowlights.** Don't. Exec read every update; missing Lowlights destroy trust. If it slipped, say so + ETA.
- **Asks without owners + dates.** "We need a decision on pricing" is not an ask. "Need exec call on enterprise pricing by Fri 6/13 — Maria please" is.
- **Activity-led Plans.** "Work on onboarding" is activity; "Ship onboarding step 2 + measure D7 lift" is outcome. Plans should be outcomes.
- **KPI cherry-picking.** Show the same metrics every week — don't drop ones that look bad. Trust = consistency.
- **Cadence drift.** If you skip weeks, the update loses signal. Either commit weekly OR move to monthly. No semi-weekly.
- **Audience tier.** Weekly is for exec + product/eng leads. Don't blast org-wide weekly; that's monthly.
- **Slack channel pollution.** Long Slack updates get skimmed. Keep Slack to headline + link; full update in Notion + email.
- **Async over meeting.** A good weekly update REPLACES the standing exec meeting. If everyone's still meeting after the update, the update isn't doing its job.
- **Templates vs honesty.** Templates speed writing; honesty makes it valuable. Don't fill Wins to pad if it was a slow week — write 2 wins instead of forcing 5.

## Sources

- [Lenny — How to write a great weekly update](https://www.lennysnewsletter.com/p/how-to-write-a-great-weekly-update)
- [Marty Cagan — The product leader's week](https://www.svpg.com/the-product-leaders-week)
- [First Round — How to write a great status update](https://review.firstround.com/the-status-update-that-replaced-the-meeting-and-saved-the-day)
- [Andy Grove — Operating reports (High Output Management)](https://www.amazon.com/High-Output-Management-Andrew-Grove/dp/0679762884)
- [Stripe Capital style guide for board updates](https://stripe.com/jobs/principles)
- [Linear cycle status API](https://developers.linear.app)
