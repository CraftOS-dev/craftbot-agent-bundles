<!--
Source: https://mooncamp.com/blog/best-okr-software
OKR cascade via Lattice / Mooncamp / WorkBoard (Quantive renamed)
-->
# OKR Cascade — Mooncamp / Lattice / WorkBoard

Christina Wodtke's "Radical Focus" method (ONE objective + 3 KRs per team per quarter, confidence dial, no rollover) executed on the 2026 OKR stack: Mooncamp (design-conscious teams <150, €8/user/mo, REST API), Lattice Goals (HR-integrated, $8/seat), WorkBoard (Quantive renamed Sep 2025 — 200+ employees with auto-tracked KRs). Auto-check-ins pull from analytics MCPs.

## When to use

- Quarterly OKR setting (company → team → individual cascade).
- Weekly OKR check-in cadence (confidence dial).
- Mid-quarter OKR refresh after material strategy shift.
- End-of-quarter OKR scoring + retrospective.

Trigger phrases: "set Q3 OKRs", "OKR cascade", "company OKRs", "OKR check-in", "OKR retro", "score OKRs".

**Note on WorkBoard (2026):** Quantive was renamed WorkBoard in September 2025 after WorkBoard acquired the Quantive product. Same product, new brand.

## Setup

```bash
# Mooncamp API
curl -fsSL "https://api.mooncamp.com/v1/me" \
  -H "Authorization: Bearer $MOONCAMP_API_KEY"

# Lattice Goals API
curl -fsSL "https://api.latticehq.com/v1/goals?period=Q3-2027" \
  -H "Authorization: Bearer $LATTICE_API_TOKEN"

# WorkBoard (formerly Quantive)
curl -fsSL "https://api.workboard.com/v2/me" \
  -H "Authorization: Bearer $WORKBOARD_API_KEY"
```

Auth / API key requirements:
- `MOONCAMP_API_KEY` — Mooncamp Settings → API (paid plan).
- `LATTICE_API_TOKEN` — Lattice integrations.
- `WORKBOARD_API_KEY` — WorkBoard admin tier.
- Analytics keys for auto-check-in: `POSTHOG_API_KEY`, `AMPLITUDE_API_KEY`, `STRIPE_API_KEY`.

## Common recipes

### Recipe 1: Company OKR (one per quarter)

```bash
# Mooncamp — create company-level objective
curl -X POST "https://api.mooncamp.com/v1/objectives" \
  -H "Authorization: Bearer $MOONCAMP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Solo founders ship in their first session",
    "description":"Q3 2027. Activation is the constraint on retention; if D7 retention holds, runway extends 6 months.",
    "owner_id":"<ceo-id>",
    "team_id":"company",
    "period":"Q3-2027",
    "visibility":"public"
  }'
```

### Recipe 2: 3 KRs per objective (Wodtke radical focus)

```bash
OBJECTIVE_ID="<from Recipe 1>"

# KR1 — primary outcome metric
curl -X POST "https://api.mooncamp.com/v1/key-results" \
  -H "Authorization: Bearer $MOONCAMP_API_KEY" \
  -d "{
    \"objective_id\":\"$OBJECTIVE_ID\",
    \"title\":\"D7 retention 11% → 25%\",
    \"start_value\":11,
    \"target_value\":25,
    \"unit\":\"%\",
    \"owner_id\":\"<pm-id>\"
  }"

# KR2 — supporting outcome
curl -X POST "https://api.mooncamp.com/v1/key-results" \
  -H "Authorization: Bearer $MOONCAMP_API_KEY" \
  -d "{
    \"objective_id\":\"$OBJECTIVE_ID\",
    \"title\":\"Time-to-first-value 14min → 5min\",
    \"start_value\":840,
    \"target_value\":300,
    \"unit\":\"seconds\"
  }"

# KR3 — leading indicator
curl -X POST "https://api.mooncamp.com/v1/key-results" \
  -H "Authorization: Bearer $MOONCAMP_API_KEY" \
  -d "{
    \"objective_id\":\"$OBJECTIVE_ID\",
    \"title\":\"Onboarding completion 45% → 70%\",
    \"start_value\":45,
    \"target_value\":70,
    \"unit\":\"%\"
  }"
```

### Recipe 3: Cascade — team OKR aligns to company OKR

```bash
# Product team objective rolls up to company objective
curl -X POST "https://api.mooncamp.com/v1/objectives" \
  -H "Authorization: Bearer $MOONCAMP_API_KEY" \
  -d "{
    \"title\":\"Ship the activation redesign\",
    \"team_id\":\"product\",
    \"parent_id\":\"$COMPANY_OBJECTIVE_ID\",
    \"alignment\":\"contributes_to\",
    \"period\":\"Q3-2027\"
  }"
```

### Recipe 4: Auto-check-in from Amplitude → Mooncamp

```bash
# Pull D7 retention from Amplitude
D7=$(curl -s "https://amplitude.com/api/3/funnels?e=%5B%22onboarding%22%2C%22d7%22%5D" \
  -u "$AMPLITUDE_API_KEY:$AMPLITUDE_SECRET" \
  | jq '.data.dataSeries[0][-1].value')

# Push to Mooncamp as check-in
curl -X POST "https://api.mooncamp.com/v1/check-ins" \
  -H "Authorization: Bearer $MOONCAMP_API_KEY" \
  -d "{
    \"key_result_id\":\"<d7-kr-id>\",
    \"current_value\":$D7,
    \"confidence\":0.65,
    \"note\":\"Auto from Amplitude $(date +%F)\"
  }"
```

### Recipe 5: Weekly check-in (manual)

```bash
curl -X POST "https://api.mooncamp.com/v1/check-ins" \
  -H "Authorization: Bearer $MOONCAMP_API_KEY" \
  -d '{
    "key_result_id":"<kr-id>",
    "current_value":18.5,
    "confidence":0.55,
    "status":"at_risk",
    "note":"D7 at 18.5% — onboarding redesign behind schedule; mitigation: pull 1 eng from infra to ship by Aug 1."
  }'
```

### Recipe 6: Lattice Goals fallback

```bash
curl -X POST "https://api.latticehq.com/v1/goals" \
  -H "Authorization: Bearer $LATTICE_API_TOKEN" \
  -d '{
    "name":"D7 retention 11% → 25%",
    "type":"key_result",
    "parent_id":"<lattice-objective-id>",
    "start_value":11,
    "target_value":25,
    "unit":"%",
    "owner_id":"<pm-id>",
    "period_id":"<q3-2027-period-id>"
  }'
```

### Recipe 7: WorkBoard (formerly Quantive) auto-tracking

```bash
# WorkBoard supports auto-tracking from connected data sources
curl -X POST "https://api.workboard.com/v2/objectives" \
  -H "Authorization: Bearer $WORKBOARD_API_KEY" \
  -d '{
    "title":"Solo founders ship in their first session",
    "team":"company",
    "quarter":"Q3-2027",
    "auto_tracking":{
      "data_source":"amplitude",
      "metric_id":"d7_retention_funnel"
    }
  }'
```

### Recipe 8: Notion fallback (free)

```bash
mcp tool notion.create_database \
  --parent '{"page_id":"<okr-page>"}' \
  --title '[{"text":{"content":"OKRs Q3 2027"}}]' \
  --properties '{
    "Name":{"title":{}},
    "Type":{"select":{"options":[{"name":"Objective"},{"name":"Key Result"}]}},
    "Owner":{"people":{}},
    "Team":{"select":{}},
    "Start":{"number":{}},
    "Target":{"number":{}},
    "Current":{"number":{}},
    "Confidence":{"number":{}},
    "Status":{"select":{"options":[{"name":"🟢 On track"},{"name":"🟡 At risk"},{"name":"🔴 Off track"}]}},
    "Parent":{"relation":{"database_id":"<self>"}}
  }'
```

### Recipe 9: Pull all OKR statuses for QBR

```python
import requests, os
H = {"Authorization": f"Bearer {os.environ['MOONCAMP_API_KEY']}"}

objectives = requests.get(
    f"https://api.mooncamp.com/v1/objectives?period=Q3-2027",
    headers=H
).json()["objectives"]

for o in objectives:
    print(f"\n### {o['title']} ({o['team_id']})")
    print(f"  Confidence: {o['confidence']*10:.0f}/10")
    for kr in o["key_results"]:
        pct = (kr["current_value"] - kr["start_value"]) / (kr["target_value"] - kr["start_value"]) * 100
        emoji = "🟢" if kr["status"] == "on_track" else "🟡" if kr["status"] == "at_risk" else "🔴"
        print(f"  {emoji} {kr['title']} — {kr['current_value']}{kr['unit']} ({pct:.0f}%)")
```

### Recipe 10: End-of-quarter scoring + close

```bash
curl -X PATCH "https://api.mooncamp.com/v1/objectives/$OBJECTIVE_ID" \
  -H "Authorization: Bearer $MOONCAMP_API_KEY" \
  -d '{
    "status":"closed",
    "final_score":0.7,
    "retrospective":"Hit D7 at 21% vs 25% target (84% — stretch met). Time-to-value redesign deferred to Q4; learned that onboarding flow is the deeper constraint."
  }'
```

Score scale: 0.6-0.7 = stretch met (healthy); 1.0 = sandbagged. Educate the team.

### Recipe 11: Quarterly OKR retro template

```markdown
## Q3 2027 OKR Retrospective

### What we set
- Company O: Solo founders ship in their first session
  - KR1: D7 11% → 25% (final: 21% = 0.71)
  - KR2: TTFV 840s → 300s (final: 420s = 0.78)
  - KR3: Onboarding completion 45% → 70% (final: 64% = 0.76)

### What worked
- Daily metric review caught issues fast
- Cross-functional swarming on Q2 onboarding redesign

### What didn't
- TTFV depended on infra refactor; we underestimated scope
- KR3 overlapped too much with KR1 (double-counting risk)

### Q4 implication
- Continue D7 push (deeper than expected constraint)
- Drop KR3 (subsumed by KR1)
- New KR: 2nd-session re-engagement
```

### Recipe 12: Confidence trend alert

```bash
# Alert if any KR drops below 0.5 confidence
for KR in $(curl -fsSL "https://api.mooncamp.com/v1/key-results?period=Q3-2027" -H "Authorization: Bearer $MOONCAMP_API_KEY" | jq -r '.key_results[] | select(.confidence < 0.5) | .id'); do
  TITLE=$(curl -fsSL "https://api.mooncamp.com/v1/key-results/$KR" -H "Authorization: Bearer $MOONCAMP_API_KEY" | jq -r '.title')
  mcp tool slack.send --channel "#leadership" --message "🔴 KR confidence below 0.5: $TITLE — surface at QBR"
done
```

## Examples

### Example 1: Quarterly OKR setting

**Goal:** Set Q3 OKRs in 2 days during planning offsite.

**Steps:**
1. Day 1 morning: review prior quarter scores + retro (Recipe 11).
2. Day 1 afternoon: draft company objective + 3 KRs (Recipe 1-2). Force trade-offs.
3. Day 2 morning: team objectives cascade (Recipe 3).
4. Day 2 afternoon: confidence dial set to 0.6-0.7 (healthy stretch).
5. Day 2 EOD: publish in Mooncamp + announce in all-hands.
6. Set weekly auto-check-in cron (Recipe 4).

**Result:** Org aligned on ≤5 company OKRs + cascaded team OKRs; weekly cadence ready.

### Example 2: Mid-quarter OKR refresh after pivot

**Goal:** Major customer churn event forces strategy adjustment; need to re-do OKRs mid-Q3.

**Steps:**
1. Pull current OKR status (Recipe 9).
2. Decide what to keep (still relevant), revise (target changed), kill (no longer relevant).
3. Update objectives in Mooncamp via PATCH.
4. Communicate in next all-hands. Update Notion canvas.

**Result:** OKRs reflect new reality; team not chasing dead objectives.

## Edge cases / gotchas

- **More than 1 O per team = no focus.** Wodtke method: one O per team per quarter. Resist exec urge to add more.
- **More than 3 KRs = activity list, not outcomes.** 3 KRs forces choosing what matters. 5+ is hedge.
- **Confidence 1.0 = sandbagged.** Educate the team: 0.6-0.7 is stretch met. 1.0 = you set easy KRs.
- **Output KRs are not outcome KRs.** "Ship feature X" is an output. "D7 retention 25%" is an outcome. Force outcomes.
- **Don't cascade by paste-and-replicate.** Each team's OKRs justify how they roll up; don't just copy the company OKR to each team.
- **Cross-functional OKRs need a DRI.** Single owner per OKR. Multi-owner = no owner.
- **Carry-over rule.** Don't roll incomplete OKRs forward by default; re-justify each quarter.
- **Auto-check-in beats manual.** Map every KR to a metric source (Amplitude / Stripe / etc.). Manual check-ins drift.
- **Confidence trend is the early warning.** Weekly confidence dial dropping below 0.5 = surface in QBR before it goes red.
- **Lattice Goals vs Mooncamp choice.** Lattice if you already pay for Lattice HR. Mooncamp if standalone OKR design-first tool. WorkBoard if 200+ employees with enterprise integration.
- **WorkBoard ≠ Quantive deprecation.** Quantive was renamed to WorkBoard in Sep 2025; product continues. Existing Quantive customers automatically migrated.
- **End-of-quarter score conversation is performance-adjacent.** Don't tie comp to OKR scores directly (Wodtke); use as input to coaching.

## Sources

- [Mooncamp — 27 Best OKR Software 2026](https://mooncamp.com/blog/best-okr-software)
- [Mooncamp REST API docs](https://docs.mooncamp.com/api)
- [Lattice Goals API](https://lattice.com/api-docs)
- [WorkBoard (formerly Quantive) docs](https://www.workboard.com/)
- [Christina Wodtke — Radical Focus](https://www.amazon.com/Radical-Focus-Achieving-Important-Objectives/dp/0996006028)
- [John Doerr — Measure What Matters](https://www.whatmatters.com/)
