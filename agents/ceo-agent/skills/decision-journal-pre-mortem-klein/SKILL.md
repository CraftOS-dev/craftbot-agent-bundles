<!--
Source: https://www.gary-klein.com/premortem + https://grahammann.net/book-notes/how-to-decide-annie-duke
Decision journal (Annie Duke) + Pre-mortem (Gary Klein)
-->
# Decision Journal + Pre-mortem (Annie Duke + Gary Klein)

Annie Duke's decision journal (record context / alternatives / chosen / confidence / kill-criteria / review-date / outcome) separates decision quality from outcome. Gary Klein's pre-mortem ("assume it failed in 12 months; list why") — Wharton study shows ~30% better risk identification vs. brainstorming alone. Both stored in Notion as a structured DB.

## When to use

- Any strategic decision >$50k or 1-year horizon (decision journal entry).
- Irreversible 1-way-door decisions (pre-mortem mandatory).
- Quarterly review — looking back at past decisions to learn.
- Pre-launch / pre-fundraise / pre-M&A (pre-mortem mandatory).

Trigger phrases: "decision journal", "pre-mortem", "what could go wrong", "decide on X", "1-way door", "kill criteria", "Annie Duke", "Gary Klein".

## Setup

```bash
# Notion is the decision DB source-of-record
mcp tool notion.search --query "Decision journal"
```

Auth / API key requirements:
- `NOTION_API_KEY` — for the DB.
- `GOOGLE_OAUTH_TOKEN` — for review-date calendar set.

## Common recipes

### Recipe 1: Decision journal entry (Annie Duke)

```bash
mcp tool notion.create_page \
  --parent '{"page_id":"<decision-journal-db>"}' \
  --properties '{
    "Decision":[{"text":{"content":"Open Series B fundraise in Q3 2027"}}],
    "Date":{"date":{"start":"2027-04-15"}},
    "Confidence":{"number":7},
    "Type":{"select":{"name":"1-way door"}},
    "Review date":{"date":{"start":"2027-10-15"}}
  }' \
  --children-markdown '## Date
2027-04-15

## Decision
Open Series B fundraise process in Q3 2027 at $20M target, $80M pre.

## Context
- Current: $5M ARR, 140% NRR, 15-month runway
- Market: Series B environment Q3 forecast tighter than Q1
- Team: VP Eng + VP Sales hired; ready for scale
- Burn: $400k/mo, 18-month runway at current trajectory

## Alternatives considered
- A: Wait until Q4 2027 — more revenue history; risk: market deterioration
- B: Bridge round from existing investors — faster; risk: less aggressive pricing
- C [chosen]: Q3 2027 Series B — balance of momentum + market window
- D: Skip Series B — bootstrap to profitability; risk: slower growth, competitive loss

## Why this option
- Q3 timing leverages NRR momentum + 2 enterprise pilot conversions
- Banker selection allows competitive process
- Conservative $20M target leaves headroom for outperformance
- Existing VCs supportive of A+ option

## Confidence
7/10

## Expected outcome (3, 6, 12 months out)
- 3mo: Banker selected, narrative locked, top-20 investor list
- 6mo: Term sheet from lead investor at $80M+ pre
- 12mo: Round closed, 24-month runway, hiring plan executing

## Kill criteria
- If MRR drops >10% MoM in Q2 → defer to Q4
- If lead banker fails to source 5+ engaged investors by Aug 15 → switch process
- If lead investor proposes <$60M pre → walk; bridge from current investors

## Review date
2027-10-15

## Outcome (filled at review)
[Will fill at review]
'
```

### Recipe 2: Pre-mortem facilitation script (30 min, Gary Klein)

```markdown
## Pre-mortem — [Decision]

### Setup (3 min)
"Assume the decision is made. It is 12 months from now. The project failed catastrophically. We are at the funeral."

Participants: 5-10 (mix of skeptics + executors).
Materials: silent brainstorm tool (Mural / Miro / sticky notes).

### Silent brainstorm (10 min)
Each participant writes — INDIVIDUALLY, NO TALKING — every reason the project failed.
Push past obvious ("we ran out of money"). Push for specific ("the lead enterprise deal pulled out in Q2 because their CIO was replaced and the new CIO had a vendor preference").

### Round-robin (10 min)
Each person shares ONE reason at a time. No debate. No "I agree." Just write it on the wall.
Continue until everyone passes.

### Cluster + prioritize (5 min)
Cluster similar reasons. Vote on top 5 risks (each person 3 dots).

### Mitigation assignment (2 min)
For each top-5 risk: assign owner + mitigation + due date. Add to Linear.
```

### Recipe 3: Pre-mortem capture template

```markdown
# Pre-mortem — Series B Fundraise

## Setup
Imagine: it is October 2027. The Series B failed. We didn't close the round.

## Top 5 risks identified
| Risk | Owner | Mitigation | Due |
|---|---|---|---|
| Lead investor pulled due to growth deceleration | CEO | Lock Q2 growth narrative + secondary metrics | 2027-06-01 |
| Banker chose us 2nd-tier list of investors | CFO | Define narrative + tier-1 list ourselves | 2027-05-15 |
| Sales pipeline coverage <3x at fundraise open | VP Sales | Pre-pipeline blitz, 2 SDR hires | 2027-05-30 |
| Founder burnout from 4-month process | CEO | Block 1 week pre-process for prep; cadence calls | 2027-07-15 |
| Cash dropped to <12mo during round | CFO | Lock bridge option from current investors | 2027-06-30 |
```

### Recipe 4: 1-way vs 2-way door classifier (Bezos)

```markdown
## Reversibility test

| Question | 1-way door | 2-way door |
|---|---|---|
| Can we cheaply reverse it in 90 days? | No | Yes |
| Does it commit headcount > 6 months? | Yes | No |
| Does it change company position publicly? | Yes | No |
| Does it cost > $100k to reverse? | Yes | No |
| Does it affect customer trust? | Yes | No |

If 1-way → mandatory pre-mortem + decision journal + DACI.
If 2-way → DACI only; move fast; pre-mortem optional.
```

### Recipe 5: Decision journal DB schema

```bash
mcp tool notion.create_database \
  --parent '{"page_id":"<exec-hub>"}' \
  --title '[{"text":{"content":"Decision Journal"}}]' \
  --properties '{
    "Decision":{"title":{}},
    "Date":{"date":{}},
    "Confidence":{"number":{}},
    "Type":{"select":{"options":[{"name":"1-way door"},{"name":"2-way door"}]}},
    "Review date":{"date":{}},
    "Status":{"select":{"options":[{"name":"Open"},{"name":"Reviewed"},{"name":"Reversed"}]}},
    "Outcome rating":{"select":{"options":[{"name":"Better than expected"},{"name":"As expected"},{"name":"Worse than expected"}]}},
    "Process rating":{"select":{"options":[{"name":"Good process"},{"name":"OK process"},{"name":"Bad process"}]}}
  }'
```

Key Annie Duke insight: process and outcome are independent. Good process + bad outcome = bad luck. Bad process + good outcome = lucky (don't congratulate).

### Recipe 6: Calendar-set the review

```bash
mcp tool google-calendar.create_event \
  --calendar-id primary \
  --summary "Decision review: Series B timing" \
  --start "2027-10-15T10:00:00" \
  --end "2027-10-15T10:30:00" \
  --description "Review decision journal entry [Notion link]. What actually happened? What did we learn?"
```

### Recipe 7: Outcome review template

```markdown
## Decision Review — Series B Timing (Q3 2027)

### What we decided (Apr 15, 2027)
Open Series B in Q3 2027, $20M target, $80M pre.

### What we predicted
- 3mo: banker + narrative + top-20 list
- 6mo: term sheet at $80M+
- 12mo: closed round, 24-month runway

### What actually happened
- Banker selected May; narrative locked Jun (on time)
- Term sheet at $90M pre Aug 2027 (better than expected)
- Closed Sep 2027, 28-month runway

### Process rating
GOOD. Pre-mortem caught growth-deceleration risk → we doubled down on Q2 growth narrative.

### Outcome rating
BETTER THAN EXPECTED.

### Lessons
- Pre-mortem risk #1 (lead investor pull due to growth) became the central narrative we proactively addressed
- Risk #4 (founder burnout) hit mid-process; pre-locked 1-week prep was insufficient
- Adjust: next round, block 2 weeks prep + delegate weekly metrics during process

### Forward decisions
- For Series C: open ~ 18-24 months ahead (versus 12 months this time)
- Add: founder support fund $X for therapist + EA during process
```

### Recipe 8: Quarterly journal review

```bash
# Pull all decisions due for review this quarter
mcp tool notion.query_database \
  --database-id "<decision-journal-db>" \
  --filter '{
    "and":[
      {"property":"Status","select":{"equals":"Open"}},
      {"property":"Review date","date":{"on_or_before":"2027-06-30"}}
    ]
  }'

# Each gets reviewed in QBR or dedicated 1h review block
```

### Recipe 9: Pre-mortem for product launch

```markdown
## Pre-mortem — Activation v2 launch (Q3)

Imagine: it is October 2027. Activation v2 failed. D7 retention is 14% (target was 25%).

### Top 5 risks
1. Engineering team underestimated migration complexity → 6-week slip
2. Customer comms missed; users confused by new flow
3. A/B test rollout too aggressive — bad cohort sample
4. Support team not trained; surge of tickets
5. Mobile experience broken at launch
```

### Recipe 10: Pre-mortem for M&A

```markdown
## Pre-mortem — Acquire CompetitorX

Imagine: it is 18 months post-close. Acquisition failed. We wrote down 80% of value.

### Top 5 risks
1. Key founders + technical lead left in first 6 months
2. Customer churn on acquired side accelerated due to feature integration delays
3. Cultural clash — eng team rejected our practices
4. Integration cost 2x estimate
5. Strategic rationale eroded (LLM landscape shifted, capability commoditized)
```

### Recipe 11: Confidence calibration (Annie Duke)

```markdown
## Confidence calibration retrospective

Pull last 20 decision journal entries. Plot predicted confidence vs outcome rating.

- If you said 9/10 confidence on 10 decisions and only 7 went well → over-confident, recalibrate.
- If you said 5/10 on 10 decisions and 9 went well → under-confident, take more risk.

Quarterly check; CEO + leadership team.
```

### Recipe 12: Decision journal weekly habit

```bash
# Friday afternoon cron — surface decisions made this week without journal entry
mcp tool linear.list_issues --updated-after "2027-04-08" --filter "decision-grade:1-way" \
| jq '.issues[] | select(.fields.decision_journal_link == null)' \
| tee missing-journal-entries.json

mcp tool slack.send --channel "#ceo" --message "Missing decision journal entries this week: $(cat missing-journal-entries.json | jq length). Set 30 min Friday."
```

## Examples

### Example 1: Pre-mortem for fundraise

**Goal:** Pressure-test the Series B fundraise decision before commit.

**Steps:**
1. Decide reversibility (Recipe 4) — 1-way door (announcing the round publicly).
2. Schedule 30-min pre-mortem with 5-7 participants.
3. Run facilitation (Recipe 2). Capture top 5 risks (Recipe 3).
4. Assign owners + mitigations + due dates (Linear).
5. Write decision journal (Recipe 1) with kill criteria.
6. Set 6-month review (Recipe 6).
7. At review: outcome retrospective (Recipe 7) → feeds confidence calibration (Recipe 11).

**Result:** Risks identified upfront; mitigations in flight; learning captured.

### Example 2: Weekly decision review habit

**Goal:** CEO commits to journaling every strategic decision.

**Steps:**
1. Set Friday 4-5pm "Decision journal" block.
2. Each week: list 2-5 strategic decisions made.
3. Write journal entry for each (Recipe 1).
4. Set review dates (3-month default for most; 6-12 for fundraise / hire).
5. Quarterly: calibration review (Recipe 11).

**Result:** Within 1 year, calibration improves measurably; institutional learning compounds.

## Edge cases / gotchas

- **Pre-mortem feels redundant when you're confident.** That's exactly when you need it most. Wharton study: ~30% better risk identification.
- **Don't skip silent brainstorm.** Going straight to discussion lets the loudest voice dominate. Silent = honest.
- **Frame as "the funeral," not "the post-mortem."** Subtle but important: forces concreteness ("how did it fail" vs "could it fail").
- **Pre-mortem participants should include skeptics.** Inviting only believers = motivated reasoning.
- **Journal kill criteria are non-negotiable.** Without them, sunk cost wins. Every entry needs explicit kill criteria.
- **Confidence ≠ probability.** Calibrate quarterly (Recipe 11). Most CEOs are over-confident on go decisions, under-confident on no decisions.
- **Process and outcome are separate.** Bad outcome with good process is bad luck. Good outcome with bad process is luck (don't repeat the process).
- **Journal entries are private until review.** Publishing entries up-front creates motivated reasoning. Review them in QBR.
- **Don't journal every decision.** Only strategic / 1-way / >$50k. Daily ops decisions don't need journals.
- **Review dates calendar-locked.** Without calendar reminders, reviews drop. Set at journal creation time.
- **Pre-mortem != risk register.** Risk register lists ongoing risks. Pre-mortem is point-in-time pressure-test before a specific decision.
- **Pre-mortem outputs feed Linear.** Risks without assigned owners + due dates evaporate.

## Sources

- [Gary Klein pre-mortem method](https://www.gary-klein.com/premortem)
- [HBR — Performing a Project Pre-Mortem (Gary Klein)](https://hbr.org/2007/09/performing-a-project-premortem)
- [Annie Duke — How to Decide (book notes)](https://grahammann.net/book-notes/how-to-decide-annie-duke)
- [Annie Duke — Thinking in Bets](https://www.amazon.com/Thinking-Bets-Making-Smarter-Decisions/dp/0735216355)
- [Bezos 1-way vs 2-way doors](https://www.allthingsdistributed.com/2022/04/one-way-and-two-way-doors.html)
