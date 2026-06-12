<!--
Source: https://easyretro.io
Source: https://www.parabol.co
Source: https://miro.com/api/
-->
# Retrospective Facilitation: EasyRetro / Parabol / Miro / FigJam — SKILL

SaaS retro tools + format selection by team mood + project phase + time-box patterns. Async option via Miro / FigJam. AI summary via Parabol.

## When to use

- Facilitating an end-of-sprint or end-of-phase retrospective.
- Picking the right retro format for team state (Start/Stop/Continue, 4Ls, Mad/Sad/Glad, Sailboat).
- Running async retros for distributed teams.
- Generating retro summary + action items + linking back to Linear/Asana.
- Tracking retro action items across sprints (action repeat = unresolved root cause).

Trigger phrases: "run a retro", "sprint retro", "retrospective", "EasyRetro", "Parabol", "Miro retro", "4Ls", "Mad Sad Glad", "Start Stop Continue", "retro summary".

## Setup

```bash
# EasyRetro (paid — $25/user/mo for full features; free tier limited)
curl -fsSL "https://easyretro.io/api/v1/boards" \
  -H "Authorization: Bearer $EASYRETRO_TOKEN"

# Parabol (paid — $6/user/mo; AI summary on Pro)
curl -fsSL "https://api.parabol.co/graphql" \
  -H "Authorization: Bearer $PARABOL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ viewer { id email } }"}'

# Miro (free tier with limits; paid for unlimited boards)
curl -fsSL "https://api.miro.com/v2/boards" \
  -H "Authorization: Bearer $MIRO_TOKEN"

# FigJam (via figma-mcp; included with Figma seat)
mcp tool figma.create_board --help
```

Auth:
- `EASYRETRO_TOKEN` — EasyRetro Settings → API (paid)
- `PARABOL_TOKEN` — Parabol Settings → API (paid)
- `MIRO_TOKEN` — Miro Apps → Create app → OAuth or token (free tier OK)
- Figma seat for FigJam

## Common recipes

### Recipe 1: Retro format selection guide
```
TEAM STATE              | FORMAT
First retro / new team  | Start / Stop / Continue
                        | (simple; non-confrontational)

Team friction / morale  | Mad / Sad / Glad
                        | (emotional surface; relationship-heavy)

Mid-project balanced    | 4Ls (Liked / Learned / Lacked / Longed-for)
                        | (broader signal; learning-focused)

Strategic / big-picture | Sailboat (wind / anchors / rocks / island)
                        | (problem-solving; team alignment)

Tight time / minimal    | What went well / What didn't / What changes
                        | (cuts to action)

End-of-phase / G3-G5    | KALM (Keep / Add / Less / More)
                        | (informs phase-out decisions)

Post-incident           | Blameless post-mortem (5 Whys + actions)
                        | (NOT a retro — see incident-response skill)
```

### Recipe 2: Standard 60-min retro time-box
```
00-05 min | Set context — sprint goal recap, metrics, ground rules
05-15 min | Gather data — silent stickies (anonymous if needed)
15-20 min | Group themes — facilitator clusters similar
20-25 min | Dot vote — top items (3 dots per person)
25-45 min | Discuss top 2-3 items — 5 Whys / root cause
45-55 min | Action items — owner + due date + Linear issue
55-60 min | Close — appreciate + pulse check
```

### Recipe 3: 30-min lightweight retro (for high-frequency teams)
```
00-05 min | Pulse + recap
05-10 min | Silent stickies
10-15 min | Group + vote
15-25 min | Discuss top 1-2 items
25-30 min | Actions + close
```

### Recipe 4: Create EasyRetro board (4Ls)
```bash
curl -X POST "https://easyretro.io/api/v1/boards" \
  -H "Authorization: Bearer $EASYRETRO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Sprint 27 — Onboarding Revamp",
    "template":"4ls",
    "columns":[
      {"title":"Liked","color":"green"},
      {"title":"Learned","color":"blue"},
      {"title":"Lacked","color":"amber"},
      {"title":"Longed for","color":"purple"}
    ],
    "anonymous":true,
    "voting_enabled":true,
    "votes_per_user":3
  }'
```

### Recipe 5: Create Parabol retro with AI summary
```bash
# Parabol GraphQL
curl -X POST "https://api.parabol.co/graphql" \
  -H "Authorization: Bearer $PARABOL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query":"mutation { startRetrospective(teamId:\"<team-id>\", templateId:\"start-stop-continue\") { meeting { id } } }"
  }'

# After meeting ends, fetch AI summary
curl -X POST "https://api.parabol.co/graphql" \
  -H "Authorization: Bearer $PARABOL_TOKEN" \
  -d '{"query":"{ meeting(meetingId:\"<id>\") { summary { content actionItems { content assignee } } } }"}'
```

### Recipe 6: Async retro via Miro (distributed team)
```bash
# Create Miro board with retro template
curl -X POST "https://api.miro.com/v2/boards" \
  -H "Authorization: Bearer $MIRO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Sprint 27 Retro — async (open Wed-Fri)",
    "description":"Add stickies through Fri 5pm. Live discussion Mon 10am.",
    "policy":{
      "permissionsPolicy":{"collaborationToolsStartAccess":"all_editors","copyAccess":"team_editors","sharingAccess":"team_members_with_editing_rights"},
      "sharingPolicy":{"access":"edit","inviteToAccountAndBoardLinkAccess":"editor","organizationAccess":"edit","teamAccess":"edit"}
    }
  }'

# Add starter frames (4Ls columns)
for col in "Liked" "Learned" "Lacked" "Longed for"; do
  curl -X POST "https://api.miro.com/v2/boards/<board-id>/frames" \
    -H "Authorization: Bearer $MIRO_TOKEN" \
    -d "{\"data\":{\"title\":\"$col\"},\"position\":{\"x\":0,\"y\":0}}"
done
```

### Recipe 7: FigJam retro via figma-mcp
```bash
mcp tool figma.create_file \
  --name "Sprint 27 Retro — async" \
  --template "figjam-retro-4ls" \
  --share_with "team-onboarding@company.com"
```

### Recipe 8: Retro ground rules (read aloud at start)
```
1. Vegas rule — what's said here stays here, unless action items
2. Focus on systems, not individuals — "the process" not "Alice"
3. Be specific — "step 3 acceptance criteria were unclear" not "the spec was bad"
4. Action items have owner + due date — otherwise they don't exist
5. No litigating personal behavior — escalate 1:1 with manager
6. Hard stop at [end-time] — discipline drives clarity
```

### Recipe 9: 5 Whys for root cause
```
Issue: "We missed the sprint goal by 30%."

Why? Because 3 issues spilled to next sprint.
Why? Because they were re-estimated mid-sprint.
Why? Because acceptance criteria were ambiguous.
Why? Because PM rushed sprint planning under time pressure.
Why? Because charter sign-off slipped 5 days into the sprint planning week.

Root cause: charter timing.
Action: tighten charter sign-off SLA to T-1 sprint vs T-0.
```

### Recipe 10: Retro summary template
```markdown
# Retro — Sprint [N] — [Project] — [YYYY-MM-DD]

## Format
[Start/Stop/Continue / 4Ls / Mad-Sad-Glad / Sailboat / KALM]

## Attendees
[List]

## Themes

### What went well
- [Theme 1: e.g., "Tight design-eng sync prevented rework"]
- [Theme 2]

### What didn't
- [Theme 1: e.g., "Mid-sprint estimate changes (3 issues)"]
- [Theme 2]

### Insights
- [Insight 1: e.g., "Charter sign-off timing is upstream root cause"]
- [Insight 2]

## Action items
| # | Action | Owner | Due | Issue |
|---|---|---|---|---|
| 1 | Tighten charter sign-off SLA to T-1 sprint | PM | 2026-07-05 | LIN-301 |
| 2 | Add "estimates frozen at start of sprint" to DoR | Eng Lead | 2026-07-01 | LIN-302 |
| 3 | Pre-grooming 1 sprint ahead | PM + Eng Lead | 2026-07-15 | LIN-303 |

## Repeat actions (open from prior retros — ROOT CAUSE)
- LIN-280 (from Sprint 26): "Add design-eng pair on critical-path tasks" — still partial
  → escalate: not enough capacity → CR or backlog deprioritize?

## Pulse check (1-5)
- Team energy: 3.8 / 5
- Confidence in next sprint: 4.1 / 5
- Sustainability (do we feel rushed?): 3.0 / 5 ← attention

## Notes
- Mad/Sad/Glad considered for next sprint if pulse drops below 3 — relationship signal
```

### Recipe 11: Repeat-action detection (root cause flag)
```python
# repeats.py — find action items appearing across multiple retros
import json, statistics
retros = json.load(open("retros-history.json"))
# [{"date":"2026-06-15","actions":[{"text":"..","status":"open"},...]}]

all_actions = {}
for r in retros:
    for a in r["actions"]:
        key = a["text"].lower()[:50]
        all_actions.setdefault(key, []).append((r["date"], a["status"]))

print("Repeat actions (3+ retros):")
for txt, occurrences in all_actions.items():
    if len(occurrences) >= 3:
        print(f"  '{txt}' — {len(occurrences)} retros — root cause?")
        for d, s in occurrences: print(f"    {d}: {s}")
```

### Recipe 12: Sailboat retro template
```
                          ☀ ISLAND (vision)
                       Where we want to go
                              │
                              ↑
                   ╱╲      ╔═══════════╗
                  ╱  ╲     ║   SHIP    ║
   〰️ WIND     ╱    ╲   ║  (team)   ║      🪨 ROCKS
   What's   →  ╱  ⛵  ╲  ╚═══════════╝  ← Risks
   pushing      ╱      ╲       │            ahead
   us           ╱──────╲       │
   forward                     ↓
                          ⚓ ANCHORS
                       What's holding
                          us back

Run flow:
1. Show diagram; explain quadrants (5 min)
2. Silent stickies in each (10 min)
3. Cluster + vote (10 min)
4. Discuss anchors + rocks (root cause; 20 min)
5. Actions to lift anchors / dodge rocks (10 min)
6. Close (5 min)
```

### Recipe 13: KALM retro for phase-out / G4-G5
```
KEEP   | What worked; preserve in BAU
ADD    | What's missing; needs creation in BAU handoff
LESS   | What we did too much of (over-engineering, theater)
MORE   | What we underinvested in (testing, docs)

Use at phase-out / closure to inform BAU + future projects.
```

## Examples

### Example 1: Run standard sprint retro
**Goal:** End of Sprint 27; 60-min retro Wed 4pm.

**Steps:**
1. Pick format (Recipe 1) — Sprint 27 had friction → Mad/Sad/Glad.
2. Create EasyRetro board (Recipe 4 with template=msg).
3. Email team Mon: "Sprint 27 retro Wed 4pm; format Mad/Sad/Glad; add stickies anytime before."
4. Open meeting; ground rules (Recipe 8); pulse check.
5. Group + vote.
6. Discuss top 3 with 5 Whys (Recipe 9).
7. Action items (Recipe 10 template) with owner + Linear issue.
8. Close + final pulse.
9. Post-meeting: Parabol AI summary to Notion archive; share with absent team members.

**Result:** Retro completed; 3 actions tracked; root cause surfaced; team felt heard.

### Example 2: Async retro for distributed team
**Goal:** Team split US/EU/APAC; sync retro impossible.

**Steps:**
1. Miro board (Recipe 6) opens Wed AM; closes Fri 5pm.
2. Email reminder Thu morning.
3. Fri 6pm PM clusters + posts AI summary in Slack.
4. Mon 10am 30-min sync discuss top 2 + actions.
5. Archive in Notion.

**Result:** Async input + sync decision; works across 3 time zones.

### Example 3: Detect root-cause repeat
**Goal:** 5 sprints in; sense that some actions keep re-appearing.

**Steps:**
1. Run Recipe 11 — find 1 action present 4 of 5 retros: "improve sprint planning estimation."
2. Root cause analysis (5 Whys, Recipe 9) — discover charter timing is upstream issue.
3. New action: tighten charter SLA (Sprint 26 carried-forward unresolved → escalate to sponsor).
4. Resolution: sponsor agrees charter T-1 sprint; root cause closed.

**Result:** Process root cause fixed; recurring action retired.

## Edge cases / gotchas

- **Retro every sprint — non-negotiable.** Cutting retros = same mistakes repeat = team doesn't improve.
- **Ground rules read aloud, every time.** Even tenured teams drift; ritual matters.
- **Action items without owner + due = wishes.** Always assign + link to Linear/Asana issue.
- **Repeat actions ≥3 retros = upstream root cause.** Stop treating symptoms; investigate.
- **Skipping the pulse check.** 1-5 pulse on team energy + confidence + sustainability — leading indicator of burnout.
- **Mad/Sad/Glad too soon = blameful.** Use only when team trust is strong; otherwise pick Start/Stop/Continue.
- **Anonymity matters.** Distributed / mixed-seniority teams need anonymous stickies (EasyRetro, Parabol toggle).
- **Async retros need closing sync.** Stickies alone don't generate actions; 30-min live discussion needed.
- **Parabol AI summary.** Good for first draft; PM should edit + add context before archiving.
- **Miro free tier 3-board cap.** Active org needs paid; or use FigJam if Figma seats already paid.
- **EasyRetro free tier limits voting + history.** $25/u/mo for full features.
- **FigJam included with Figma.** If org has Figma seats, FigJam is "free" — use over EasyRetro.
- **Hot topics derail.** Time-box discussion; if root cause is deep, schedule follow-up "fishbone session."
- **Retro for cross-team retros differ.** Inter-team retros (e.g., Onboarding + Auth) need facilitator from outside; otherwise blame-shifting.
- **Sponsor at retro = team won't be candid.** Keep sponsor out; share summary post-meeting.
- **Action items > meeting minutes.** Archive minutes; track actions to closure in Linear.
- **5 Whys can plateau.** Sometimes 3 whys is enough; sometimes 7. Stop when you hit a system root.
- **KALM for closure works well.** Use at G5 retro to inform BAU.
- **Recovery retros after RED status.** Don't blame; focus on systems.

## Sources

- [EasyRetro](https://easyretro.io)
- [Parabol — AI retros](https://www.parabol.co)
- [Miro API](https://miro.com/api/)
- [Scrum.org retrospective guide](https://www.scrum.org/resources/what-is-a-sprint-retrospective)
- [Atlassian retro templates](https://www.atlassian.com/team-playbook/plays/retrospective)
- [Retromat (format library)](https://retromat.org)
- [PMI lessons-learned retros](https://www.pmi.org/learning/library/lessons-learned-next-level-communicating-7991)
- [5 Whys technique (Lean)](https://leanmanufacturingtools.org/5-whys-root-cause-analysis/)
- [Sailboat retro template](https://miro.com/templates/sailboat-retro/)
