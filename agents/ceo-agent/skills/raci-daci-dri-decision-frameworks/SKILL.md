<!--
Source: https://www.atlassian.com/team-playbook/plays/daci + https://dectrack.com/en/blog/decision-models-raci-daci-rapid
Decision frameworks: DACI / RACI / DRI chooser + templates
-->
# Decision Frameworks — DACI / RACI / DRI

DACI (Atlassian — Driver / Approver / Contributors / Informed; single Approver) for strategic decisions. RACI (Responsible / Accountable / Consulted / Informed) for execution tasks. DRI (Apple — Directly Responsible Individual) for cross-functional initiatives. RAPID (Bain — Recommend / Agree / Perform / Input / Decide) as legacy alternative to DACI. This pack carries the chooser, templates, and Linear/Notion implementations.

## When to use

- A strategic decision is stuck because "everyone has input."
- An initiative has unclear ownership ("who's actually responsible?").
- Cross-functional work where multiple teams need to coordinate without losing accountability.
- Onboarding a new exec — explaining the decision system.

Trigger phrases: "who decides this", "DACI for X", "RACI matrix", "DRI for the initiative", "decision is stuck", "no one's owning this".

## Setup

```bash
# Notion as the decision-log source-of-record
mcp tool notion.search --query "Decision log"

# Linear for DRI assignment on initiatives
mcp tool linear.search --query "DRI"
```

Auth / API key requirements:
- `NOTION_API_KEY` — for DACI / RACI templates + decision DB.
- `LINEAR_API_KEY` — for DRI as issue assignee with label.

## Common recipes

### Recipe 1: Which framework — the chooser

```markdown
## Decision type → Framework

| Question | Use |
|---|---|
| Strategic decision (board / OKR / capital) | DACI |
| Execution task / project handoff | RACI |
| Cross-functional initiative ownership | DRI |
| Multi-stakeholder where roles unclear | RAPID (legacy) |
| Recurring operational decision | DRI + decision criteria doc |

Rule of thumb:
- One decision = DACI
- Many tasks = RACI
- One owner = DRI
```

### Recipe 2: DACI template (Notion page)

```bash
mcp tool notion.create_page \
  --parent '{"page_id":"<decision-log-db>"}' \
  --properties '{
    "Decision":[{"text":{"content":"Should we move to enterprise GTM in 2027?"}}],
    "Status":{"select":{"name":"Open"}},
    "Approver":{"people":[{"id":"<ceo-id>"}]},
    "Due":{"date":{"start":"2027-04-15"}}
  }' \
  --children-markdown '## Driver
[Name — corrals stakeholders, brings recommendation, owns the deadline]
Sarah Chen, Head of Sales

## Approver
[ONE name — makes the decision]
CEO Alice Park

## Contributors
- VP Product — capability assessment
- VP Eng — feasibility + cost
- CFO — financial model
- Head of Marketing — positioning impact

## Informed
- Board (post-decision)
- Full eng team
- Customer success

## Recommendation
Driver recommends: Move to enterprise pilot in Q3 with 3 design partners.
Reasoning: 4 inbound enterprise leads in 60 days; current SMB CAC creeping; enterprise gross margin 78% vs 62%.

## Alternatives considered
- A: Stay pure SMB. Pro: focus. Con: TAM ceiling at $20M ARR.
- B: Hybrid SMB + enterprise. Pro: hedge. Con: split focus, longer sales cycle drag.
- C [chosen]: Pilot 3 enterprise design partners Q3. Pro: low-commit learning. Con: split eng for 1 quarter.

## Decision due
2027-04-15

## Decision made
[Date / Outcome / Approver signature]

## Kill criteria
- If <2 of 3 pilots close by EOQ3 → revert to pure SMB
- If enterprise sales cycle > 9 months → revert
- If SMB churn rises >2pp during pilot → pause and reassess'
```

### Recipe 3: RACI template (execution matrix)

```markdown
## RACI Matrix — Product launch — Activation v2

| Task | PM | Eng Lead | Designer | Marketing | Support |
|---|---|---|---|---|---|
| Spec | A | C | C | I | I |
| Implementation | I | A | C | I | I |
| Design | C | C | A | I | I |
| Launch comms | I | I | I | A | C |
| Customer enablement | C | I | I | I | A |
| QA | C | A | I | I | C |

R = Responsible (does the work)
A = Accountable (signs off — one per row)
C = Consulted (input)
I = Informed (knows when done)
```

### Recipe 4: DRI for cross-functional initiative

```bash
# Linear issue with DRI label + single assignee
mcp tool linear.create_issue \
  --team "EXEC" \
  --title "Initiative: Activation v2 launch" \
  --assignee "pm-sara@company.com" \
  --labels "DRI,initiative,Q3-OKR" \
  --description "DRI: Sara Chen
Contributing teams: Product, Eng, Design, Marketing, Support
Decision authority: DACI link [Notion page]
KR linked: D7 11% → 25%
Cadence: weekly status in #activation-v2; biweekly DRI sync with CEO."
```

### Recipe 5: RAPID template (legacy alt)

```markdown
## RAPID — [Decision]

- **R**ecommend: [name — owns the recommendation]
- **A**gree: [name(s) — must sign off; if disagree, escalate]
- **P**erform: [name(s) — will execute after decision]
- **I**nput: [name(s) — consulted]
- **D**ecide: [ONE name — final call]
```

Use RAPID instead of DACI only when the org already uses it; otherwise DACI is simpler.

### Recipe 6: Decision DB schema (Notion)

```bash
mcp tool notion.create_database \
  --parent '{"page_id":"<exec-hub>"}' \
  --title '[{"text":{"content":"Decision Log"}}]' \
  --properties '{
    "Decision":{"title":{}},
    "Type":{"select":{"options":[{"name":"DACI"},{"name":"RACI"},{"name":"DRI"},{"name":"RAPID"}]}},
    "Approver":{"people":{}},
    "Driver":{"people":{}},
    "Status":{"select":{"options":[{"name":"Open"},{"name":"Decided"},{"name":"Deferred"},{"name":"Reversed"}]}},
    "Due":{"date":{}},
    "Decided":{"date":{}},
    "Outcome":{"rich_text":{}},
    "Review date":{"date":{}},
    "Tied to OKR":{"relation":{"database_id":"<okr-db>"}}
  }'
```

### Recipe 7: Stuck decision diagnostic

```markdown
## Why is this decision stuck?

- [ ] No named Approver → DACI fix: assign ONE Approver
- [ ] Two Approvers → DACI fix: collapse to one (CEO breaks ties)
- [ ] Driver not corralling → DACI fix: change Driver or set deadline
- [ ] Missing data → Driver action: pull data with explicit deadline
- [ ] Approver avoiding → Coach Approver (separate conversation)
- [ ] Not actually a decision (it's a goal / wish) → Reframe
- [ ] Stakeholder feels Informed → Confirm RACI / DACI; resentment is usually here
```

### Recipe 8: DACI for board-level decision

```markdown
## DACI — Board-level

- Driver: CEO (typically)
- Approver: Board (collective via vote OR board chair as DACI Approver)
- Contributors: CFO, legal-counsel, relevant VP
- Informed: full leadership team

Board-level decisions usually require unanimous-or-majority vote per articles of incorporation. Treat board as collective Approver in DACI; individual board members as Contributors.
```

### Recipe 9: Recurring decision criteria doc

```markdown
## Decision criteria — Hiring approval

For VP+ hires, this is the standing criteria. CEO is the standing Approver.

A hire is approved if all of:
- [ ] Scorecard outcomes signed off by CEO + relevant board member
- [ ] 3+ topgrading references completed
- [ ] Comp within band per benchmarking pull
- [ ] Equity per Series-stage table
- [ ] Working session pass + 2/3 panel pass

A hire requires DACI escalation if any of:
- Comp >10% above band
- Equity >upper bound
- Mixed reference signal (require explicit Driver reasoning)
```

### Recipe 10: Decision review cadence

```bash
# Set review for kill criteria check
mcp tool google-calendar.create_event \
  --calendar-id primary \
  --summary "Decision review: Enterprise GTM pilot" \
  --start "2027-09-15T10:00:00" \
  --description "Review against kill criteria. Continue / sharpen / reverse."
```

### Recipe 11: Linear DRI label setup

```bash
mcp tool linear.create_label --team "EXEC" --name "DRI" --color "#ff4d4f"
mcp tool linear.create_label --team "EXEC" --name "initiative" --color "#4d6dff"

# Convention: every cross-functional initiative is a Linear issue with both labels + single assignee = DRI
```

### Recipe 12: Slack template for surfacing DACI to team

```bash
mcp tool slack.send \
  --channel "#exec" \
  --message ":pushpin: *New DACI: Should we move to enterprise GTM in 2027?*
Driver: Sarah Chen | Approver: Alice (CEO)
Contributors: see Notion link
Decision due: Apr 15

[Notion link to full DACI]

Contributors: please add input by Apr 12 EOD."
```

## Examples

### Example 1: Untangling a stuck multi-team decision

**Goal:** "Should we sunset feature X?" has been debated for 3 weeks.

**Steps:**
1. Diagnose with Recipe 7 — what's stuck?
2. Diagnosis: 2 VPs both think they're Approver.
3. Frame as DACI with Recipe 2 — CEO as Approver, both VPs as Contributors.
4. Driver: PM owning feature X.
5. Set deadline + alternatives + recommendation.
6. CEO decides within 5 business days.
7. Log in DB (Recipe 6) with kill criteria for future review.

**Result:** Decision made; both VPs feel heard via Contributor role.

### Example 2: Cross-functional initiative DRI

**Goal:** Q3 activation initiative needs single owner across product / eng / marketing.

**Steps:**
1. Create Linear issue (Recipe 4) with DRI + initiative labels.
2. Single assignee = PM Sara as DRI.
3. RACI matrix for sub-tasks (Recipe 3).
4. Weekly status in #activation-v2; biweekly DRI sync with CEO.
5. Tied to Q3 OKR (Recipe 6 schema).
6. Kill criteria at the DACI level for "should we continue this initiative."

**Result:** Single throat to choke; sub-task ownership clear via RACI.

## Edge cases / gotchas

- **Two Approvers = no Approver.** Most common DACI failure mode. CEO breaks ties; otherwise reframe.
- **Driver ≠ Approver.** Driver corrals + recommends. Approver decides. Conflating them = veto-by-Driver.
- **Contributors who feel like Approvers.** When a contributor doesn't get their way and stalls, the system breaks. Set expectation: Contributors give input, don't decide.
- **Informed ≠ consensus.** "We need to inform the team" doesn't mean they vote. Educate.
- **Don't DACI everything.** Daily ops decisions use DRI / RACI. DACI for strategic + irreversible decisions.
- **Kill criteria are non-negotiable.** Every DACI needs "we reverse this if X." Otherwise sunk cost wins.
- **Decision DB neglected.** Maintain monthly. Reviewable history = institutional learning.
- **Review dates calendar-locked.** Without calendar reminders, reviews drop.
- **RAPID is heavier than DACI.** Use only if org already runs it. DACI is the modern default.
- **Linear DRI is single assignee.** If you assign 2 people, you've lost the DRI principle. Use multi-assignee only on sub-tasks.
- **DACI for hiring offers.** Often missed. VP+ offers should have explicit DACI with CEO as Approver, board chair Informed.
- **DACI's invisible cousin: "no decision needed."** Sometimes the right move is "we're not deciding this yet — re-up in 4 weeks." Document that, too.

## Sources

- [Atlassian DACI play](https://www.atlassian.com/team-playbook/plays/daci)
- [RACI vs DACI vs RAPID — DecTrack](https://dectrack.com/en/blog/decision-models-raci-daci-rapid)
- [Apple DRI model — Steve Jobs / Tim Cook](https://www.executive-impact.com/blog/the-dri-model)
- [Bain RAPID framework](https://www.bain.com/insights/rapid-tool-to-clarify-decision-accountability/)
- [Notion decision log template](https://www.notion.so/templates/decision-log)
