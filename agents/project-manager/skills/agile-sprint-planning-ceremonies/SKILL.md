<!--
Source: https://www.scrum.org/resources/scrum-guide
Source: https://www.scrum.org/resources/what-is-a-sprint-planning-meeting
Source: https://geekbot.com
-->
# Agile Sprint Planning + Ceremonies — SKILL

Sprint planning, daily standup (sync + async), backlog grooming, sprint review, retro. DoR + DoD enforcement. Sprint goal = singular outcome.

## When to use

- Planning the next sprint / cycle (Linear cycle, Jira sprint, Asana sprint).
- Running daily standup (sync or async via Geekbot / Range / Standuply).
- Backlog grooming (refinement) to keep items "ready."
- Sprint review (demo to stakeholders).
- Establishing Definition of Ready + Definition of Done for the team.

Trigger phrases: "sprint planning", "next sprint", "standup", "grooming", "refinement", "sprint review", "demo", "DoR", "DoD", "ceremony", "scrum".

## Setup

```bash
# Linear cycles (default for software shops)
mcp tool linear.create_cycle --help

# Jira sprints (Atlassian Rovo MCP GA Feb 2026)
curl -fsSL "https://api.atlassian.com/ex/jira/<cloud-id>/rest/agile/1.0/sprint" \
  -H "Authorization: Bearer $JIRA_TOKEN"

# Geekbot async standup
curl -fsSL "https://api.geekbot.com/v1/standups" \
  -H "Authorization: $GEEKBOT_TOKEN"

# Range (engineering manager-focused standup)
curl -fsSL "https://api.range.co/v1/checkins" \
  -H "Authorization: Bearer $RANGE_TOKEN"
```

Auth:
- `LINEAR_API_KEY`, Linear ships free
- `JIRA_TOKEN` — Atlassian API token
- `GEEKBOT_TOKEN` — paid $2.50/user/mo
- `RANGE_TOKEN` — paid

## Common recipes

### Recipe 1: Sprint planning procedure
```markdown
## Sprint planning (90-min default, 2-wk sprint)

### Before the meeting
- [ ] Backlog groomed (top 30 items meet DoR)
- [ ] Team capacity computed (FTE × hours × focus × (1 - PTO%))
- [ ] Velocity from last 3 sprints averaged
- [ ] Sprint goal proposal drafted by PM/PO

### In the meeting
00-10 min | Sprint goal alignment (singular outcome)
10-20 min | Recap top-priority items (PO walks through)
20-50 min | Team estimates + commits issues ≤ capacity
50-70 min | Acceptance criteria reviewed + dependencies flagged
70-80 min | Risks + assumptions called out (→ RAID)
80-90 min | Owners assigned; cycle created in PM tool

### After the meeting
- [ ] Cycle/sprint created in Linear/Jira/Asana
- [ ] Issues moved to cycle with owner
- [ ] Sprint goal posted in Slack + Notion
- [ ] DoR check passed on every committed issue
```

### Recipe 2: Sprint goal template
```
Sprint goal = singular outcome statement

GOOD: "Activated users grew by X this cycle"
GOOD: "Onboarding revamp shipped to 5 design partners"
GOOD: "SSO refactor merged + deployed staging"

BAD: "We worked on the activation funnel"  (no outcome)
BAD: "Ship X, Y, Z, and start W"  (multiple goals = no goal)
BAD: "Improve UX"                  (not measurable)

Rule: 1 sentence; outcome-focused; binary measurable (achieved Y/N at end).
```

### Recipe 3: Definition of Ready (DoR)
```
A story is READY for sprint commitment when:
- [ ] User story or work item written (As X, I want Y, so that Z)
- [ ] Acceptance criteria defined (≥3 Given/When/Then)
- [ ] Estimate exists (story points or hours)
- [ ] Dependencies identified + logged in RAID
- [ ] Design / spec / data linked (if applicable)
- [ ] Outcome metric tied to sprint goal (when applicable)
- [ ] Owner identified (assignee or "TBD on day 1")
- [ ] No open questions blocking start
```

### Recipe 4: Definition of Done (DoD)
```
A story is DONE when:
- [ ] Code complete + merged to main (or release branch)
- [ ] Tests passing — unit + integration + E2E for critical paths
- [ ] Peer review approved (≥2 approvals for core changes)
- [ ] Acceptance criteria validated by reviewer (Given/When/Then ✓)
- [ ] Documentation updated (READMEs, ADRs, user-facing if applicable)
- [ ] Analytics instrumentation live (events firing in non-prod)
- [ ] Deployed (or staged for release)
- [ ] Linked GitHub PR closed
- [ ] Customer-visible behavior verified (UAT or PM review)
```

### Recipe 5: Compute team capacity
```python
# capacity.py
team = [
    {"name":"Alice","fte":1.0,"role":"eng","pto_hrs":0},
    {"name":"Bob","fte":1.0,"role":"eng","pto_hrs":8},   # 1 day PTO
    {"name":"Carol","fte":0.5,"role":"eng","pto_hrs":0},
    {"name":"Dan","fte":1.0,"role":"qa","pto_hrs":16},   # 2 days PTO
]
FOCUS = {"eng":0.65, "qa":0.75, "design":0.65, "pm":0.55}
HRS_PER_WEEK = 40
SPRINT_WEEKS = 2

total_hrs = 0
for p in team:
    raw = p["fte"] * HRS_PER_WEEK * SPRINT_WEEKS - p["pto_hrs"]
    effective = raw * FOCUS[p["role"]]
    total_hrs += effective
    print(f"  {p['name']}: raw={raw}h effective={effective:.0f}h")

# Convert to story points if team uses points
# Velocity_last_3_avg = 32 pts; hrs_per_point = 32 / total_hrs_last_sprint
print(f"\nTotal effective hours this sprint: {total_hrs:.0f}h")
```

### Recipe 6: Create Linear cycle for the sprint
```bash
mcp tool linear.create_cycle \
  --teamKey "PROD" \
  --name "Cycle 28 — Activation push wave 2" \
  --startsAt "2026-06-29" \
  --endsAt "2026-07-13"
```

### Recipe 7: Commit issues to cycle ≤ capacity
```bash
# Filter ready issues; pull top-N up to capacity
mcp tool linear.list_issues \
  --filter '{"state":{"type":{"eq":"backlog"}},"labels":{"name":{"in":["dor-ok","sprint-28-candidate"]}}}' \
  --orderBy '{"field":"priority","direction":"asc"}' \
  --first 30 \
| jq -r '.nodes[] | .id' \
| head -10 \
| xargs -I{} mcp tool linear.update_issue --id {} --cycleId "<cycle-28-id>"
```

### Recipe 8: Daily standup format (sync, 15-min)
```
Each team member, 2 min each:
1. What I shipped yesterday (link issue)
2. What I'll ship today
3. Blockers — including dep waits

Facilitator notes:
- No tangential discussion — "park" for after
- Blockers → RAID issue → owner + ETA
- Cross-team blockers → cross-team-dep escalation
- ≤ 15 min hard stop
```

### Recipe 9: Async standup via Geekbot
```bash
# Configure Geekbot Slack standup
curl -X POST "https://api.geekbot.com/v1/standups" \
  -H "Authorization: $GEEKBOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Onboarding Revamp Daily",
    "channel":"#proj-onboarding-revamp",
    "schedule":"0 10 * * 1-5",
    "questions":[
      {"id":1,"text":"What did you ship yesterday?","color":"#4caf50"},
      {"id":2,"text":"What are you shipping today?","color":"#2196f3"},
      {"id":3,"text":"Any blockers?","color":"#f44336"}
    ],
    "participants":[12345,12346,12347],
    "timezones":"local"
  }'

# Fetch summary
curl -s "https://api.geekbot.com/v1/reports?after=$(date -d yesterday +%s)" \
  -H "Authorization: $GEEKBOT_TOKEN" \
| jq '.[] | {member, answers: .questions}'
```

### Recipe 10: Backlog grooming session (60 min, weekly)
```markdown
## Backlog grooming — [date] 60min

### Pre-meeting
- [ ] PO/PM has ranked top-30 items
- [ ] New customer asks triaged

### Agenda
00-10 min | Recap sprint goal + Q3 trajectory
10-30 min | Top-10 candidate items — clarify; estimate; flag missing AC
30-50 min | Top 11-20 — quick scan; flag deeper work needed
50-60 min | Next steps; flag items needing design / data spike

### Outputs
- 10 items DoR-ready for next sprint planning
- 5 items needing design spike before commit
- 5 items refined but not yet ready
```

### Recipe 11: Sprint review (demo) format
```markdown
## Sprint review — [date] 60min

### Attendees
- Team
- PO / PM
- Stakeholders (sponsor, dependent teams, beta partners)

### Agenda
00-05 min | Sprint goal recap
05-15 min | Velocity + completion (story points done / committed)
15-50 min | Demos — each completed story shown live (NOT slides)
50-55 min | Feedback gathering (Slack thread or live)
55-60 min | Next sprint preview (one-liner)

### Outputs
- Demo video archived
- Stakeholder feedback → backlog grooming
- Customer-facing updates → release notes
```

### Recipe 12: Sprint plan output (Notion / markdown)
```markdown
# Sprint 28 — [Project] — [start → end]

## Sprint goal
Onboarding revamp shipped to 5 design partners by Fri sprint-end.

## Capacity
- 3 eng × 80h × 0.65 = 156h
- 1 QA × 80h × 0.75 = 60h
- 0.5 design × 80h × 0.65 = 26h
- Total = 242h
- PTO subtracted = -24h
- Net = 218h

## Committed
| Issue | Estimate | Owner | DoR? |
|---|---|---|---|
| LIN-301 Activation event Android fix | 16h | Bob | ✓ |
| LIN-302 SSO refactor 3.1.3 | 40h | Alice | ✓ |
| LIN-303 Step 1 modal | 24h | Alice | ✓ |
| LIN-304 Step 2 prompt | 24h | Carol | ✓ |
| LIN-305 Checklist component | 24h | Carol | ✓ |
| LIN-306 E2E test scenarios | 32h | Dan | ✓ |
| LIN-307 Beta deployment scripts | 16h | Bob | ✓ |
| LIN-308 Beta partner onboarding emails | 8h | PM | ✓ |
| Total | 184h | | |

## Dependencies
- D-002 Auth team SSO ETA Mon (impacts LIN-302)

## Risks
- R-007 SSO cert renewal in flight (impacts LIN-302)

## Stretch (only if commit done)
- LIN-309 Step 3 prompt (12h)
- LIN-310 Tracking validation script (8h)
```

### Recipe 13: Cross-team scrum-of-scrums (weekly)
```markdown
## Scrum-of-Scrums — [date] 15min

Each team rep, 2 min:
1. What we're shipping this week
2. What's blocking us (cross-team)
3. What other teams need from us

Facilitator: program manager / chief-of-staff PM

Output: cross-team-dep log updates (cross-link dependency-mapping-cross-team)
```

## Examples

### Example 1: Plan Sprint 28 from groomed backlog
**Goal:** Sprint 27 ends Fri; planning Mon 10am.

**Steps:**
1. Wed grooming session (Recipe 10) — 12 items DoR-ready.
2. PM drafts sprint goal proposal (Recipe 2).
3. Compute capacity (Recipe 5) — 218h.
4. Planning Mon: walk top-priority items; team commits 184h.
5. Create cycle (Recipe 6); commit issues (Recipe 7).
6. Post sprint plan in Notion (Recipe 12); pin Slack.
7. Geekbot daily standup configured (Recipe 9).

**Result:** Sprint 28 launched Mon noon with clear goal + DoR-met scope.

### Example 2: Daily standup catches a blocker
**Goal:** Day 3 standup; Alice mentions SSO cert renewal stuck.

**Steps:**
1. PM logs blocker → RAID R-007 status: Open → At-risk.
2. Cross-team escalation (Auth team PM via Slack).
3. Auth team responds: SLA confirmed Fri.
4. Update Alice; adjust Sprint 28 sequencing (work 3.2.2 in parallel).
5. Status email to sponsor as heads-up.

**Result:** Blocker surfaced Day 3, mitigated Day 4; no Day 5 surprise.

### Example 3: Sprint review with design partners
**Goal:** Show Sprint 27 outcomes to 5 beta partners.

**Steps:**
1. Recipe 11 review format — 60 min Friday.
2. Demo each shipped story live.
3. Collect feedback via Notion form during review.
4. Triage feedback Mon — 3 items → backlog with `customer-feedback` label.
5. Post-meeting: Loom video archive; share with absent partners.

**Result:** Stakeholder demo done; 3 items into next grooming.

## Edge cases / gotchas

- **Sprint goal singular.** "Ship A, B, C" = no goal. Pick one outcome that A/B/C all serve.
- **DoR is gate, not aspiration.** No DoR = no commit. Forces clarity upstream.
- **Capacity is a ceiling, not a floor.** Commit ≤ capacity; overcommit = predictable miss.
- **Focus factor honest.** 0.7 default; verify per-team. New team or context-switch-heavy = 0.5.
- **PTO subtraction explicit.** Don't average "team capacity"; subtract specific PTO hours per person.
- **Story-point velocity early-team unreliable.** First 5 sprints, focus on commitment-vs-completion %; switch to velocity when stable.
- **Standup = sync up, not status update.** "What did I do yesterday" → 1 line. Anything longer = parking lot.
- **Async standup ≠ standup deleted.** Geekbot answers still need someone reading; otherwise blockers sit.
- **Backlog grooming weekly minimum.** Skipping = sprint planning chaos.
- **Sprint review ≠ demo to PM.** Stakeholders + customers; live demo, not slides.
- **Retro every sprint** (cross-link retrospective-facilitation-easyretro-parabol).
- **Mid-sprint estimate changes.** Smell — DoR likely insufficient. Track + improve DoR.
- **Sprint length consistency.** 2 weeks is default; 1-week = high-tempo; 3+ week = slow. Don't vary mid-project.
- **Definition of Done expands silently.** Lock DoD at kickoff; CR for changes.
- **Async standups for distributed.** Geekbot/Range/Standuply with local-time prompts beat 6am-EU-3am-US sync calls.
- **Carrying over work hides under-estimation.** Track carryover; 3+ sprints of >20% carryover = capacity/estimation issue.
- **Sprint goal achievement %.** Track over time; trending down = upstream problem (capacity, charter, deps).
- **Demo prep doesn't expand the sprint.** Cap prep at 1 hr/story; if more needed, story wasn't done.

## Sources

- [Scrum Guide 2020 (scrum.org)](https://www.scrum.org/resources/scrum-guide)
- [Sprint planning meeting (scrum.org)](https://www.scrum.org/resources/what-is-a-sprint-planning-meeting)
- [Linear cycles docs](https://linear.app/docs/cycles)
- [Atlassian Jira sprint best practices](https://www.atlassian.com/agile/scrum/sprint-planning)
- [Geekbot async standup API](https://geekbot.com/api)
- [Range standup](https://www.range.co)
- [Standuply](https://standuply.com)
- [DoR + DoD examples (Atlassian)](https://www.atlassian.com/agile/project-management/definition-of-done)
- [PMI agile practice guide](https://www.pmi.org/learning/library/disciplined-agile-pmbok-7th-foundation-9924)
