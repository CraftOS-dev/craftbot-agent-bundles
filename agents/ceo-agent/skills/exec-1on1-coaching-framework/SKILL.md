<!--
Source: https://www.tability.io/compare/platform/lattice + Lattice 1:1s API
Exec 1:1 prep + coaching question library + KR check-in
-->
# Exec 1:1 — Coaching Framework + KR Check-in

CEO ↔ direct-report 1:1s anchored in Lattice 1:1s API (Feb 2026 public) + a CEO coaching question library + integrated KR check-in. 15Five / Leapsome as alternatives. Cadence: weekly 45-min per direct report. Structure: their topics first, your topics second, coaching question, KR check-in, actions.

## When to use

- Running weekly 1:1s with each direct report.
- Onboarding a new exec hire's 1:1 cadence.
- Coaching a struggling leader (separate from performance review).
- Skip-level 1:1 (1-2x per quarter with reports' reports).

Trigger phrases: "1:1 with VP Eng", "coaching question for CFO", "skip-level", "my 1:1 with [name]", "talking points", "weekly 1:1".

**Fallback when no Lattice contract:** Notion DB with the same structure (free) — see Recipe 10.

## Setup

```bash
# Lattice 1:1s API (Feb 2026 public release)
curl -fsSL "https://api.latticehq.com/v1/me" \
  -H "Authorization: Bearer $LATTICE_API_TOKEN"
```

Auth / API key requirements:
- `LATTICE_API_TOKEN` — Lattice Settings → Integrations.
- `NOTION_API_KEY` — for fallback + decision-log integration.
- `GOOGLE_OAUTH_TOKEN` — for calendar.

## Common recipes

### Recipe 1: Schedule recurring 1:1 (45 min weekly)

```bash
mcp tool google-calendar.create_event \
  --calendar-id primary \
  --summary "1:1 — CEO + VP Eng" \
  --start "2027-04-08T14:00:00" \
  --end "2027-04-08T14:45:00" \
  --recurrence "RRULE:FREQ=WEEKLY;BYDAY=TH;COUNT=52" \
  --attendees "vp-eng@company.com" \
  --description "Talking points: [Lattice link]
Their topics first (20 min)
My topics (10 min)
Coaching question (5 min)
KR check-in (5 min)
Actions + next time (5 min)"
```

### Recipe 2: Create talking-points doc in Lattice (per 1:1)

```bash
curl -X POST "https://api.latticehq.com/v1/one-on-ones" \
  -H "Authorization: Bearer $LATTICE_API_TOKEN" \
  -d '{
    "participants":[{"user_id":"<ceo-id>"},{"user_id":"<vp-eng-id>"}],
    "scheduled_at":"2027-04-08T14:00:00Z",
    "agenda":[
      {"text":"Their topics","owner":"<vp-eng-id>"},
      {"text":"My topics","owner":"<ceo-id>"},
      {"text":"Coaching question","owner":"<ceo-id>"},
      {"text":"KR check-in","owner":"both"},
      {"text":"Actions","owner":"both"}
    ]
  }'
```

### Recipe 3: Coaching question library

```markdown
## Strategic
- What is the one decision you've been avoiding?
- What would you change if you owned the whole company?
- If you had to cut your team's scope in half, what would you keep?
- What is the highest-leverage thing you are not doing?

## Team
- Who on your team is underperforming and what is your plan?
- Who is your highest-potential person and what are you investing in them?
- Where is the team's morale this week, honestly?
- If you lost your top performer tomorrow, what would break?

## Personal / leadership
- What is keeping you up at night?
- What feedback have you been avoiding asking for?
- Where do you feel like an impostor right now?
- What would your most ambitious version of yourself do?

## Unblock
- How can I unblock you in the next 24 hours?
- What is one thing I am doing that is making your job harder?
- What is one decision you need from me by Friday?
```

### Recipe 4: Pull last 1:1's action items

```bash
curl -fsSL "https://api.latticehq.com/v1/one-on-ones?participant_ids=<vp-eng-id>&limit=1" \
  -H "Authorization: Bearer $LATTICE_API_TOKEN" \
| jq '.one_on_ones[0].action_items[] | {text, owner, status, due_date}'
```

Open the 1:1 by reviewing whether they did what they said.

### Recipe 5: Push action items to Linear

```bash
ACTION=$(curl -X POST "https://api.latticehq.com/v1/one-on-ones/$ONE_ON_ONE_ID/action-items" \
  -H "Authorization: Bearer $LATTICE_API_TOKEN" \
  -d '{"text":"Ship VP Eng onboarding plan","owner":"<vp-eng-id>","due_date":"2027-04-15"}')

# Mirror to Linear
mcp tool linear.create_issue \
  --team "EXEC" \
  --title "1:1 action: ship VP Eng onboarding plan" \
  --assignee "vp-eng@company.com" \
  --due "2027-04-15" \
  --labels "1on1-action"
```

### Recipe 6: KR check-in within 1:1

```bash
# Pull current KRs for this report
curl -fsSL "https://api.latticehq.com/v1/goals?owner_id=<vp-eng-id>&period=Q2-2027&type=key_result" \
  -H "Authorization: Bearer $LATTICE_API_TOKEN" \
| jq '.goals[] | {name, latest_check_in: .latest_check_in.status, confidence: .latest_check_in.confidence}'

# During 1:1, push confidence + blockers
curl -X POST "https://api.latticehq.com/v1/check-ins" \
  -H "Authorization: Bearer $LATTICE_API_TOKEN" \
  -d '{
    "goal_id":"<kr-id>",
    "current_value":85,
    "status":"on_track",
    "confidence":0.7,
    "note":"On-track. Slight risk on hiring DRI by EOQ; will mitigate via retained search."
  }'
```

### Recipe 7: Skip-level 1:1 cadence (quarterly per skip)

```bash
mcp tool google-calendar.create_event \
  --calendar-id primary \
  --summary "Skip-level — CEO + [skip-name]" \
  --start "2027-05-01T15:00:00" \
  --end "2027-05-01T15:30:00" \
  --recurrence "RRULE:FREQ=QUARTERLY;COUNT=4" \
  --description "Skip-level (their manager NOT invited).
Questions:
- What is working on your team?
- What is not working?
- Anything you can't tell your manager?
- If you had a magic wand, what would change?"
```

### Recipe 8: Post-1:1 summary for memory-processor

```bash
mcp tool notion.create_page \
  --parent '{"page_id":"<1on1-history-db>"}' \
  --properties '{
    "Title":[{"text":{"content":"VP Eng — 2027-04-08"}}],
    "Date":{"date":{"start":"2027-04-08"}},
    "Person":{"select":{"name":"VP Eng"}}
  }' \
  --children-markdown "## Summary
- Top concern this week: hiring DRI by EOQ at risk
- Action: kick off retained search by Wed
- Coaching topic: delegation muscle on architecture decisions
- KR confidence: 7/10 on D7 retention KR
- Blockers I owe: decision on Eng team org structure"
```

### Recipe 9: Performance review separation

```markdown
1:1s are coaching — NOT performance reviews. Educate the team:
- 1:1s: tactical + coaching + KR check-in. Weekly.
- Quarterly check-ins: KR scoring + skill development. In Lattice Reviews.
- Annual review: comp + level decisions. Separate process.

If you find yourself doing performance feedback in 1:1s, you're using the wrong tool.
```

### Recipe 10: Notion fallback (no Lattice)

```bash
mcp tool notion.create_database \
  --parent '{"page_id":"<exec-1on1-hub>"}' \
  --title '[{"text":{"content":"1:1 Talking Points"}}]' \
  --properties '{
    "Date":{"date":{}},
    "Person":{"people":{}},
    "Their topics":{"rich_text":{}},
    "My topics":{"rich_text":{}},
    "Coaching question":{"rich_text":{}},
    "KR check-in":{"rich_text":{}},
    "Actions":{"rich_text":{}},
    "Open from last":{"rich_text":{}}
  }'
```

### Recipe 11: Coaching plan for struggling leader

```markdown
## Coaching Plan — [Name]

### Diagnosis
What's the specific gap? (specific behavior, not "needs to grow")
- Example: "Avoids cross-functional conflict; gives up on decisions when pushback comes"

### Targeted coaching topics (4 weeks each)
Week 1-4: Direct feedback delivery
Week 5-8: Holding decisions under pushback
Week 9-12: Building cross-functional alliances

### Check-in cadence
- Weekly 1:1 includes 10 min on coaching topic
- Monthly 360 micro-survey (3 questions)
- Quarterly: continue / change / exit decision

### Exit criteria
If no measurable progress after 12 weeks → performance conversation with operations-agent + legal-counsel.
```

### Recipe 12: 1:1 prep checklist (5 min pre-meeting)

```markdown
- [ ] Pull last 1:1's action items (Recipe 4)
- [ ] Pull their current KR status (Recipe 6)
- [ ] Pick 1 coaching question (Recipe 3)
- [ ] Decide on 1-2 of MY topics
- [ ] Review their Linear assignments from board / QBR
- [ ] Note any cross-functional issues to surface
```

## Examples

### Example 1: VP Eng weekly 1:1

**Goal:** Run a 45-min 1:1 that drives decisions, not status.

**Steps:**
1. T-5 min: prep checklist (Recipe 12).
2. Open with last week's actions (5 min) — what did they ship.
3. Their topics (20 min) — they drive the agenda.
4. My topics (10 min) — surface cross-functional issues, ask about team.
5. Coaching question (5 min) — pull from library (Recipe 3).
6. KR check-in (5 min) — update confidence in Lattice (Recipe 6).
7. Actions + next time (5 min) — push to Linear (Recipe 5).

**Result:** Tight cadence; both leave with clarity.

### Example 2: Skip-level with senior IC

**Goal:** Get unfiltered signal from a senior IC two levels down.

**Steps:**
1. Schedule (Recipe 7). Their manager NOT invited.
2. Open with: "This is your time. I'll keep what you share confidential unless you say otherwise."
3. Listen 80% — ask "tell me more" when they surface something.
4. Note 1-2 themes for follow-up with their manager (without naming source).
5. Send thank-you note within 24h.

**Result:** Signal from the front lines; trust built; you spot issues before they escalate.

## Edge cases / gotchas

- **1:1 ≠ status update.** If status is the topic, you're doing it wrong. Use written updates for status.
- **Their topics first non-negotiable.** Manager taking the floor first is the #1 1:1 failure mode.
- **Skip 1:1 = signal.** If you skip a 1:1 with a direct report, you're saying "you're not a priority." Reschedule, don't cancel.
- **Cadence is sacred.** Same day, same time, every week. Reschedule, don't cancel.
- **Don't bring HR issues to 1:1.** Coach in 1:1; performance/HR in separate forum with operations-agent in loop.
- **Lattice 1:1s API requires admin scope.** Default tokens may not have `one-on-ones:write`.
- **Confidentiality in skip-levels.** Educate the org that skip-levels are confidential unless explicitly shared.
- **Coaching questions are one per 1:1.** Don't fire all 12 at them; pick one that fits the moment.
- **KR check-in stays light.** Quarterly Lattice review is for deep scoring. In 1:1 just confidence + blockers.
- **Don't let actions pile up.** If they have >3 open 1:1 actions from prior weeks, slow down adding new ones; clear backlog first.
- **Coaching plan for struggling leader = 90-day clock.** Document everything. Exit criteria written upfront.
- **Lattice API rate limit.** ~100 req/min. Batch action item creates if you have a big team.

## Sources

- [Lattice pricing + comparison (Tability)](https://www.tability.io/compare/platform/lattice)
- [Lattice 1:1s product page](https://lattice.com/product/1-on-1s)
- [Lattice API docs](https://lattice.com/api-docs)
- [Michael Lopp — Managing Humans (1:1 origin)](https://www.amazon.com/Managing-Humans-Humorous-Software-Engineering/dp/1484221575)
- [Camille Fournier — The Manager's Path](https://www.amazon.com/Managers-Path-Leaders-Navigating-Growth/dp/1491973897)
