<!--
Source: https://help.getharvest.com/api-v2
Source: https://developers.track.toggl.com
Source: https://clockify.me/developers-api
Source: https://www.pmi.org/learning/library/earned-value-project-management-method-measuring-5037
-->
# Budget Tracking (Planned vs Actual) — SKILL

Plan vs Actual cost variance reporting + CV/CPI/EAC computation + threshold flagging. Pulls AC from Harvest / Toggl / Clockify / Tempo (time tracking) plus expenses; cross-references against planned budget per WBS element.

## When to use

- Weekly/monthly budget vs actual variance reporting.
- Computing CV / CPI / EAC / variance % for status reports.
- Flagging budget overruns at threshold (>10% variance OR CPI < 0.9).
- Drill-down: which WBS elements drive overrun.
- Forecast EAC: at current burn rate, where will we land?

Trigger phrases: "budget variance", "planned vs actual", "CPI", "EAC", "where are we on budget", "burn rate", "cost overrun", "budget forecast".

## Setup

```bash
# Harvest (paid — small consultancies, REST v2)
curl -fsSL "https://api.harvestapp.com/v2/users/me" \
  -H "Authorization: Bearer $HARVEST_TOKEN" \
  -H "Harvest-Account-Id: $HARVEST_ACCOUNT_ID" \
  -H "User-Agent: PM-Agent (email@example.com)"

# Toggl Track (paid premium, free starter)
curl -fsSL "https://api.track.toggl.com/api/v9/me" \
  -u "$TOGGL_API_TOKEN:api_token"

# Clockify (free tier — 5-user cap as of April 2026)
curl -fsSL "https://api.clockify.me/api/v1/user" \
  -H "X-Api-Key: $CLOCKIFY_KEY"

# Tempo for Jira (Jira-stack default)
curl -fsSL "https://api.tempo.io/4/worklogs?from=2026-06-01&to=2026-06-30" \
  -H "Authorization: Bearer $TEMPO_TOKEN"
```

Auth:
- `HARVEST_TOKEN`, `HARVEST_ACCOUNT_ID` — from https://id.getharvest.com/developers
- `TOGGL_API_TOKEN` — from https://track.toggl.com/profile (free)
- `CLOCKIFY_KEY` — from https://clockify.me/user/settings (free 5-user)
- `TEMPO_TOKEN` — from Jira → Tempo → Settings → API integrations (paid)

## Common recipes

### Recipe 1: Variance metric formulas
```
Planned (PV)        = budget scheduled by date X        (BAC × planned % complete)
Earned (EV)         = budget earned by date X            (BAC × actual % complete)
Actual cost (AC)    = money spent by date X              (from time tracking + expenses)

Variance:
  Cost variance (CV)         = EV - AC                   (negative = over budget)
  Schedule variance (SV)     = EV - PV                   (negative = behind schedule)
  CV%                        = CV / EV × 100             (flag at ±10%)

Indices:
  Cost performance (CPI)     = EV / AC                   (flag at <0.9)
  Schedule performance (SPI) = EV / PV                   (flag at <0.9)

Forecast:
  Estimate at completion (EAC) = BAC / CPI               (assumes CPI persists)
  Estimate to complete (ETC)   = EAC - AC
  To-complete performance (TCPI) = (BAC - EV) / (BAC - AC)
  Variance at completion (VAC) = BAC - EAC
```

### Recipe 2: Harvest — pull actual hours + cost for a project
```bash
# Hours + cost for project in date range
curl -s "https://api.harvestapp.com/v2/reports/time/projects?from=2026-06-01&to=2026-06-30&project_id=12345" \
  -H "Authorization: Bearer $HARVEST_TOKEN" \
  -H "Harvest-Account-Id: $HARVEST_ACCOUNT_ID" \
  -H "User-Agent: PM-Agent (you@email.com)" \
| jq '.results[] | {project_name, billable_hours, total_hours, billable_amount, total_cost: (.total_hours * .avg_cost_rate)}'
```

### Recipe 3: Harvest — drill by person × project
```bash
curl -s "https://api.harvestapp.com/v2/reports/time/team?from=2026-06-01&to=2026-06-30&project_id=12345" \
  -H "Authorization: Bearer $HARVEST_TOKEN" \
  -H "Harvest-Account-Id: $HARVEST_ACCOUNT_ID" \
  -H "User-Agent: PM-Agent (you@email.com)" \
| jq '.results[] | {user_name, hours: .total_hours, cost: (.total_hours * .billable_rate)}'
```

### Recipe 4: Toggl — fetch detailed worklogs
```bash
# Toggl uses workspace_id; reports v3 API
curl -s "https://api.track.toggl.com/reports/api/v3/workspace/<workspace-id>/search/time_entries" \
  -u "$TOGGL_API_TOKEN:api_token" \
  -H "Content-Type: application/json" \
  -d '{"start_date":"2026-06-01","end_date":"2026-06-30","project_ids":[12345]}' \
| jq 'map({user: .user_id, duration: .time_entries[0].seconds, project: .project_id})'
```

### Recipe 5: Clockify — pull time entries for project
```bash
curl -s "https://api.clockify.me/api/v1/workspaces/<ws-id>/projects/<proj-id>/users/<user-id>/time-entries?start=2026-06-01T00:00:00Z&end=2026-06-30T23:59:59Z" \
  -H "X-Api-Key: $CLOCKIFY_KEY" \
| jq '.[] | {start: .timeInterval.start, duration: .timeInterval.duration}'
```

### Recipe 6: Tempo — worklogs for a Jira project
```bash
curl -s "https://api.tempo.io/4/worklogs?from=2026-06-01&to=2026-06-30&projectId=10042" \
  -H "Authorization: Bearer $TEMPO_TOKEN" \
| jq '.results[] | {author: .author.accountId, timeSpentSeconds, billableSeconds, issueKey: .issue.key}'
```

### Recipe 7: Compute AC + CV + CPI per project
```python
# budget.py — usage: uvx python budget.py budget.json
import json, sys

# budget.json = {
#   "BAC": 180000,
#   "planned_pct_complete": 0.65,     # PV by date X
#   "actual_pct_complete": 0.55,      # EV by date X (from PM tool)
#   "actual_cost_to_date": 110000     # AC from Harvest+expenses
# }
b = json.load(open(sys.argv[1]))
BAC, AC = b["BAC"], b["actual_cost_to_date"]
PV = BAC * b["planned_pct_complete"]
EV = BAC * b["actual_pct_complete"]

CV  = EV - AC
SV  = EV - PV
CPI = EV / AC if AC else float("inf")
SPI = EV / PV if PV else float("inf")
EAC = BAC / CPI if CPI else float("inf")
ETC = EAC - AC
VAC = BAC - EAC
TCPI = (BAC - EV) / (BAC - AC) if (BAC - AC) else float("inf")

print(f"BAC: ${BAC:,.0f}")
print(f"PV:  ${PV:,.0f}  EV: ${EV:,.0f}  AC: ${AC:,.0f}")
print(f"CV:  ${CV:,.0f} ({'over' if CV < 0 else 'under'})")
print(f"SV:  ${SV:,.0f} ({'behind' if SV < 0 else 'ahead'})")
print(f"CPI: {CPI:.2f}  {'FLAG' if CPI < 0.9 else 'ok'}")
print(f"SPI: {SPI:.2f}  {'FLAG' if SPI < 0.9 else 'ok'}")
print(f"EAC: ${EAC:,.0f}  ETC: ${ETC:,.0f}  VAC: ${VAC:,.0f}")
print(f"TCPI: {TCPI:.2f}  ({'achievable' if TCPI <= 1.1 else 'unrealistic — recover plan needed'})")
```

### Recipe 8: Variance threshold flag rules
```
GREEN  |  |CV%| ≤ 5%  AND CPI ≥ 0.95
AMBER  |  5% < |CV%| ≤ 10%  OR  0.9 ≤ CPI < 0.95
RED    |  |CV%| > 10%  OR  CPI < 0.9

Action by zone:
GREEN  | report only
AMBER  | top-line callout in status; root-cause memo
RED    | CR triggered + sponsor brief 24h; corrective plan in 5 days
```

### Recipe 9: Budget report template (markdown)
```markdown
# Budget Report — [Project] — Week of [YYYY-MM-DD]

## Headline
| Metric | Value | RAG |
|---|---|---|
| BAC | $180,000 | — |
| PV (planned by today) | $117,000 | — |
| EV (earned by today) | $99,000 | — |
| AC (actual to date) | $108,000 | — |
| CV | -$9,000 (over) | 🟠 |
| SV | -$18,000 (behind) | 🟠 |
| CPI | 0.92 | 🟠 |
| SPI | 0.85 | 🔴 |
| EAC | $195,650 | — |
| ETC | $87,650 | — |
| TCPI | 1.13 | 🟠 |

## Variance drivers (top-3)
1. **3.1.3 SSO unified session** — actual 60h vs planned 40h (+$2.4k). Root cause: SSO vendor cert renewal added rework. Action: vendor escalation; renegotiate cert delivery; +1d slip.
2. **2.2.3 Mobile parity** — actual 22h vs planned 16h (+$0.7k). Root cause: undocumented iOS edge case. Action: scope to P2 in next sprint.
3. **3.2.2 Step components** — actual 44h vs planned 36h (+$1.0k). Root cause: design system component not reusable as-built. Action: design-eng sync to refactor.

## Forecast
At current CPI 0.92, EAC = $195,650 (BAC $180k + $15.6k overrun). VAC = -$15,650.
Recovery scenario: lift CPI to 1.0 by close → ETC = $72k (vs current $87.6k); save $15.6k.

## Actions
- [ ] Vendor escalation memo (Eng Lead, by Fri)
- [ ] CR-009 — scope 2.2.3 mobile to P2 (PM, by Mon)
- [ ] Design-eng sync (Design Lead + Eng Lead, by Tue)
```

### Recipe 10: Auto-aggregate from Harvest + PM tool for status report
```bash
#!/usr/bin/env bash
# weekly-budget.sh
PROJECT_ID=12345
WEEK_START=2026-06-15
WEEK_END=2026-06-19

# AC from Harvest
ac=$(curl -s "https://api.harvestapp.com/v2/reports/time/projects?from=$WEEK_START&to=$WEEK_END&project_id=$PROJECT_ID" \
  -H "Authorization: Bearer $HARVEST_TOKEN" -H "Harvest-Account-Id: $HARVEST_ACCOUNT_ID" -H "User-Agent: PM-Agent (you@email.com)" \
  | jq '.results[0].total_cost')

# Planned + EV from Linear (% complete × BAC)
project=$(curl -s "https://api.linear.app/graphql" -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query":"{ project(id:\"<linear-id>\") { progress } }"}')
pct_complete=$(echo $project | jq '.data.project.progress')

BAC=180000
EV=$(echo "$BAC * $pct_complete" | bc -l)
echo "AC=$ac EV=$EV CPI=$(echo "$EV / $ac" | bc -l)"
```

### Recipe 11: Budget breakdown CSV schema
```csv
wbs_code,description,planned_hours,planned_rate,planned_cost,actual_hours,actual_cost,cv,cv_pct,status
1.1.1,5 user interviews,16,120,1920,18,2160,-240,-12.5%,AMBER
1.1.2,Funnel data pull,8,140,1120,8,1120,0,0%,GREEN
2.1.1,Onboarding flow map,16,150,2400,16,2400,0,0%,GREEN
3.1.3,SSO unified refactor,40,180,7200,60,10800,-3600,-50%,RED
4.1.1,E2E tests,24,130,3120,20,2600,520,16.7%,GREEN (under)
```

### Recipe 12: Burn rate forecast chart
```python
# burn.py
import json, matplotlib.pyplot as plt
data = json.load(open("weekly-burn.json"))  # [{week, planned_cum, actual_cum, ev_cum}]
weeks = [d["week"] for d in data]
plt.plot(weeks, [d["planned_cum"] for d in data], label="Planned (PV)", linestyle="--")
plt.plot(weeks, [d["actual_cum"] for d in data], label="Actual (AC)")
plt.plot(weeks, [d["ev_cum"] for d in data],     label="Earned (EV)")
plt.axhline(y=180000, color="red", linestyle=":", label="BAC")
plt.legend(); plt.xticks(rotation=45); plt.ylabel("$"); plt.tight_layout()
plt.savefig("burn-rate.png")
```

## Examples

### Example 1: Weekly budget variance report
**Goal:** Week-of status: budget RAG + variance drivers.

**Steps:**
1. Pull Harvest AC for week (Recipe 2).
2. Pull Linear `project.progress` for % complete → EV.
3. Compute CV / CPI / EAC via Recipe 7.
4. Apply Recipe 8 thresholds → RAG.
5. Drill top-3 over-running WBS leaves (Recipe 11 CSV grep > -10%).
6. Format Recipe 9 markdown; embed in status report.

**Result:** "Budget RAG amber. CPI 0.92. Top driver: SSO refactor +50% on plan."

### Example 2: Forecast EAC at month-end
**Goal:** Sponsor asks "will we go over budget?"

**Steps:**
1. Compute current CPI from Recipe 7.
2. EAC = BAC / CPI → $195,650 vs BAC $180k.
3. Identify levers: scope cut (CR-009 saves $4k) + crash decision ($7k save).
4. Project EAC after levers → $184,650 (just 2.6% over).
5. Sponsor decision: approve scope cut, monitor weekly.

**Result:** Quantified overrun + 2 levers + sponsor decision documented.

## Edge cases / gotchas

- **% complete from PM tool can lie.** Devs report optimistic complete; reconcile with code review status + QA pass + UAT for honesty.
- **AC must include all loaded cost.** Salary × overhead (1.4-1.6x typical) + tooling + vendor + contractor. Hour × billable rate ≠ AC if internal team.
- **Harvest billable rate vs cost rate.** `cost_rate` = your cost; `billable_rate` = client-facing. EVM uses cost, not billable.
- **Toggl Reports v3 vs v2.** v3 is current (2026); v2 deprecated. Auth header differs.
- **Clockify free tier 5-user cap (April 2026 change).** Was unlimited; for 6+ users, must upgrade to paid.
- **Tempo Cost Tracking add-on.** Tempo Timesheets alone gives time; Tempo Cost Tracking (separate add-on) gives $ figures.
- **TCPI > 1.1 = unrealistic.** Means you'd need to be 10%+ more efficient than planned for the rest of the project to hit BAC. Either scope cut or accept overrun.
- **CPI volatility early-project.** First 20% of project has noisy CPI; meaningful threshold flagging starts at 30%+ complete.
- **EV measurement methods.** Fixed formula (0/50/100, 0/100), weighted milestones, % complete, level-of-effort. Pick one per WBS family; document in charter.
- **Exchange rates for multi-currency.** Lock FX rate at baseline; revalue at month-end with a one-line note in variance.
- **Capitalize vs expense.** Capitalized cost flows to balance sheet; expense to P&L. PM tracks both but reports project budget on cash basis unless specified.
- **Contingency draws are CR-gated.** PM doesn't burn contingency unilaterally; per charter, sponsor approves draws above threshold (usually $5-10k).
- **Variance flag inversion for "under."** Negative CV usually = over budget; but if PV > EV due to schedule overrun (work not done), CV can look fine when project is actually in trouble. Always read CV + SV together.
- **Harvest rate limit 100 req/15s.** Bulk reports — batch.
- **Toggl rate limit 100/min/workspace.** Reports are heavier — backoff on 429.

## Sources

- [Harvest API v2](https://help.getharvest.com/api-v2)
- [Toggl Track API v9 + Reports v3](https://developers.track.toggl.com)
- [Clockify API](https://clockify.me/developers-api)
- [Tempo for Jira API](https://apidocs.tempo.io)
- [PMI Earned Value canon](https://www.pmi.org/learning/library/earned-value-project-management-method-measuring-5037)
- [Smartsheet budget tracking templates](https://www.smartsheet.com/free-project-budget-templates)
- [Atlassian budget variance guide](https://www.atlassian.com/agile/project-management/budget-variance)
- [Clockify free-tier cap change April 2026](https://clockify.me/pricing)
