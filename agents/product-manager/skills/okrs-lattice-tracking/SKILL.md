<!--
Source: https://lattice.com/api-docs
Lattice Goals API
-->
# OKRs via Lattice Tracking — SKILL

Lattice (lattice.com) is the 2026 OKR module of choice. The Goals API creates cascading org → team → individual objectives + key results with auto-tracked check-ins. This pack covers drafting OKRs, syncing KR values from analytics MCPs, and the weekly check-in cadence.

## When to use

- Drafting quarterly OKRs for the product team.
- Cascading an org-level objective into team-level KRs.
- Auto-checking KR values from Amplitude / Mixpanel / PostHog.
- Running the weekly OKR check-in (red / yellow / green) into a stakeholder update.
- Closing the quarter with an OKR retrospective.

Trigger phrases: "draft our Q3 OKRs", "OKR check-in", "are we on track for the retention objective", "set up a new key result", "OKR retro".

**Fallback when no Lattice contract:** 15Five Objectives (similar shape) OR a Notion DB OKR tracker (free) — see Recipe 10.

## Setup

```bash
# Lattice REST API — no native MCP yet; use cli-anything + curl
curl -fsSL "https://api.latticehq.com/v1/me" \
  -H "Authorization: Bearer $LATTICE_API_TOKEN"
```

Auth:
- `LATTICE_API_TOKEN` — admin token from Lattice Settings → Integrations. Paid HR-stack tool.
- For 15Five alt: `FIFTEENFIVE_API_KEY` from 15Five → My Account → API.

API surface (Lattice v1):
- `POST /goals` (objective or KR)
- `GET /goals/{id}` / `PATCH /goals/{id}`
- `POST /check-ins` (status update on a goal)
- `GET /goals?owner_id=X&period=Q3-2026`
- `POST /goals/{id}/relationships` (cascade / align)
- `GET /periods` (list quarter periods)

## Common recipes

### Recipe 1: Draft a quarterly objective

```bash
curl -X POST "https://api.latticehq.com/v1/goals" \
  -H "Authorization: Bearer $LATTICE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Help solo founders activate within their first session",
    "description": "Q3 2026 product objective. Activation is the constraint on retention; this objective owns the activation surface.",
    "type": "objective",
    "owner_id": "<pm-user-id>",
    "team_id": "<product-team-id>",
    "period_id": "<q3-2026-period-id>",
    "visibility": "company"
  }'
```

### Recipe 2: Attach key results to an objective

```bash
OBJECTIVE_ID="<from Recipe 1>"

# KR1 — primary outcome metric
curl -X POST "https://api.latticehq.com/v1/goals" \
  -H "Authorization: Bearer $LATTICE_API_TOKEN" \
  -d '{
    "name":"D7 retention from 35% → 42%",
    "type":"key_result",
    "parent_id":"'$OBJECTIVE_ID'",
    "start_value":35,
    "target_value":42,
    "unit":"%",
    "owner_id":"<pm-user-id>",
    "period_id":"<q3-2026-period-id>"
  }'

# KR2 — supporting outcome
curl -X POST "https://api.latticehq.com/v1/goals" \
  -H "Authorization: Bearer $LATTICE_API_TOKEN" \
  -d '{
    "name":"Time-to-first-value (median) from 14min → 5min",
    "type":"key_result",
    "parent_id":"'$OBJECTIVE_ID'",
    "start_value":840,
    "target_value":300,
    "unit":"seconds",
    "owner_id":"<pm-user-id>",
    "period_id":"<q3-2026-period-id>"
  }'

# KR3 — leading indicator
curl -X POST "https://api.latticehq.com/v1/goals" \
  -H "Authorization: Bearer $LATTICE_API_TOKEN" \
  -d '{
    "name":"% of new users completing onboarding from 45% → 70%",
    "type":"key_result",
    "parent_id":"'$OBJECTIVE_ID'",
    "start_value":45,
    "target_value":70,
    "unit":"%",
    "period_id":"<q3-2026-period-id>"
  }'
```

### Recipe 3: Cascade — align team OKR to org OKR

```bash
curl -X POST "https://api.latticehq.com/v1/goals/$TEAM_OBJECTIVE_ID/relationships" \
  -H "Authorization: Bearer $LATTICE_API_TOKEN" \
  -d '{
    "type":"aligns_to",
    "parent_id":"<org-objective-id>"
  }'
```

### Recipe 4: Weekly KR check-in (manual)

```bash
curl -X POST "https://api.latticehq.com/v1/check-ins" \
  -H "Authorization: Bearer $LATTICE_API_TOKEN" \
  -d '{
    "goal_id":"<kr-id>",
    "current_value":37.2,
    "status":"on_track",   // on_track / at_risk / off_track / missed
    "confidence":0.65,
    "note":"D7 at 37.2% after onboarding revamp shipped Mon (Amplitude funnel; 7-day rolling)"
  }'
```

### Recipe 5: Auto check-in from Amplitude

```bash
# 1. Query the funnel from Amplitude MCP
D7_RETENTION=$(mcp tool amplitude.query --chart-id "<retention-chart>" \
  | jq '.series[0].values[-1]')

# 2. Push to Lattice as a check-in
curl -X POST "https://api.latticehq.com/v1/check-ins" \
  -H "Authorization: Bearer $LATTICE_API_TOKEN" \
  -d "{
    \"goal_id\":\"<d7-kr-id>\",
    \"current_value\":$D7_RETENTION,
    \"status\":\"$([ $(echo "$D7_RETENTION > 40" | bc) = "1" ] && echo on_track || echo at_risk)\",
    \"note\":\"Auto check-in from Amplitude $(date +%F)\"
  }"
```

### Recipe 6: List all PM team OKRs for the quarter

```bash
curl -fsSL "https://api.latticehq.com/v1/goals?team_id=$PRODUCT_TEAM_ID&period_id=$Q3_PERIOD_ID&type=objective" \
  -H "Authorization: Bearer $LATTICE_API_TOKEN" \
| jq '.goals[] | {name, status: .latest_check_in.status, confidence: .latest_check_in.confidence, krs: .children | length}'
```

### Recipe 7: Pull KR status for the stakeholder update

```python
import requests, os
H = {"Authorization": f"Bearer {os.environ['LATTICE_API_TOKEN']}"}

goals = requests.get(
    f"https://api.latticehq.com/v1/goals?period_id={Q3_PERIOD}&type=objective&team_id={PRODUCT}",
    headers=H
).json()["goals"]

def emoji(s): return {"on_track":"🟢","at_risk":"🟡","off_track":"🔴","missed":"⚫"}.get(s,"⚪")

for o in goals:
    print(f"\n### {o['name']}")
    print(f"Confidence: {o['latest_check_in']['confidence']*10:.0f}/10")
    for kr in o["children"]:
        ci = kr["latest_check_in"]
        progress = (ci["current_value"] - kr["start_value"]) / (kr["target_value"] - kr["start_value"]) * 100
        print(f"- {emoji(ci['status'])} **{kr['name']}** — {ci['current_value']}{kr['unit']} ({progress:.0f}% to target)")
```

### Recipe 8: End-of-quarter close

```bash
curl -X PATCH "https://api.latticehq.com/v1/goals/$OBJECTIVE_ID" \
  -H "Authorization: Bearer $LATTICE_API_TOKEN" \
  -d '{
    "status":"closed",
    "final_score":0.7,   // 0.6-0.7 = "stretch met"; 1.0 = sandbagged
    "closing_note":"D7 retention 35% → 39% — short of 42% target. Learned that the 2nd-session re-engagement loop is the deeper constraint; Q4 hypothesis updated."
  }'
```

### Recipe 9: 15Five fallback (when no Lattice)

```bash
# 15Five "Objectives" — same shape, different endpoints
curl -X POST "https://api.15five.com/v1/objectives" \
  -H "Authorization: Bearer $FIFTEENFIVE_API_KEY" \
  -d '{"name":"...", "owner":"...", "period":"Q3-2026", "key_results":[{"name":"D7 retention","start":35,"target":42}]}'
```

### Recipe 10: Notion OKR DB (free fallback)

```bash
mcp tool notion.create_database \
  --parent '{"page_id":"<okr-page>"}' \
  --title '[{"text":{"content":"OKRs"}}]' \
  --properties '{
    "Name":{"title":{}},
    "Type":{"select":{"options":[{"name":"Objective"},{"name":"Key Result"}]}},
    "Owner":{"people":{}},
    "Period":{"select":{"options":[{"name":"Q3-2026"},{"name":"Q4-2026"}]}},
    "Start":{"number":{}},
    "Target":{"number":{}},
    "Current":{"number":{}},
    "Status":{"select":{"options":[{"name":"🟢 On track"},{"name":"🟡 At risk"},{"name":"🔴 Off track"}]}},
    "Parent":{"relation":{"database_id":"<same-db>"}}
  }'
```

## Examples

### Example 1: Q3 OKR draft → publish
**Goal:** Draft, publish, and start tracking the Q3 product OKRs.

**Steps:**
1. Confirm period IDs via `GET /periods`.
2. Create objective(s) (Recipe 1) — 3-5 objectives, no more.
3. Attach 2-4 KRs per objective (Recipe 2). KRs are outcome-led metrics, not activities.
4. Cascade team OKR up to org OKR if applicable (Recipe 3).
5. First check-in at 60-70% confidence (Recipe 4). Hitting 100% later means you sandbagged.

**Result:** Live OKR set in Lattice, visible to org, weekly cadence ready.

### Example 2: Auto-tracked KR pipeline
**Goal:** KR values update from analytics without manual entry.

**Steps:**
1. Define each KR with a unit (e.g., %, seconds, $).
2. Map each KR to an Amplitude / Mixpanel / PostHog query (Recipe 5).
3. Schedule a weekly cron via CraftBot `loop` skill to run Recipe 5 each Monday.
4. Slack-broadcast the check-in summary to #product-leads.

**Result:** Hands-off KR tracking; PM intervenes only when a KR goes yellow/red.

## Edge cases / gotchas

- **Paid plan only (Lattice).** Goals module is included in Lattice's HR plan ($11/user/mo+). Demand finance approval.
- **Period setup once per quarter.** Periods are created by admins; the API can read but typically not create them. Coordinate with HR ops.
- **Owner must be a Lattice user.** Cannot assign goals to email-only addresses; the user must be onboarded.
- **Confidence is a Lattice convention.** 60-70% start = healthy stretch. Score ≥1.0 close = sandbagged. Educate the team.
- **KR units are free-text.** API doesn't enforce them; agree on a convention (% / # / $ / ms).
- **No nesting beyond 2 levels** for objectives. Org → team is supported; team → individual works via assignment but not as a separate hierarchy.
- **Rate limits.** ~100 req/min on the v1 API; bulk operations should chunk.
- **OAuth scope.** Custom integrations need `goals:write` + `check-ins:write` scopes; default tokens may be read-only.
- **Auto check-ins overwrite manual notes.** If a human writes a check-in note, automatic write next day overwrites; agent should append rather than replace via `PATCH /check-ins/{id}`.
- **Quarter close happens at Lattice's period boundary.** If your fiscal calendar differs from Lattice's "period_id," create a custom period in admin first.

## Sources

- [Lattice API docs](https://lattice.com/api-docs)
- [Lattice Goals product overview](https://lattice.com/product/goals)
- [OKR Movement — Christina Wodtke](https://www.amazon.com/Radical-Focus-Achieving-Important-Objectives/dp/0996006028)
- [Andy Grove — High Output Management (origin of OKRs)](https://www.amazon.com/High-Output-Management-Andrew-Grove/dp/0679762884)
- [WhatMatters.com — John Doerr's OKR primer](https://www.whatmatters.com/faqs/ok-r-meaning-objectives-and-key-results)
- [15Five Objectives API](https://15five.com/api)
