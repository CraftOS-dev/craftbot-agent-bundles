<!--
Source: https://www.pmi.org/learning/library/earned-value-project-management-method-measuring-5037
Source: https://www.casinelli.net/en/congruenza-tra-metriche-earned-value-e-critical-path/
-->
# Earned Value Management (EV / PV / AC / CV / SV / CPI / SPI / EAC / ETC) — SKILL

PMI-standard EVM computation. Inputs: BAC, PV, EV, AC. Outputs: CV, SV, CPI, SPI, EAC, ETC, VAC, TCPI. Flag CPI/SPI < 0.9.

## When to use

- Computing EVM metrics for weekly/monthly status reports.
- Forecasting EAC at month-end or stage-gate.
- Diagnosing whether project is over budget AND/OR behind schedule.
- Computing TCPI to assess realism of remaining work.
- Cross-referencing EVM vs critical-path analysis (CPM).

Trigger phrases: "EVM", "earned value", "CPI", "SPI", "EAC", "ETC", "VAC", "TCPI", "cost variance", "schedule variance", "where will we land".

## Setup

```bash
# Python compute via uvx (no install)
uvx python -c "print('OK')"

# Data sources: Harvest (AC), Linear/Asana (% complete → EV), Notion DB (BAC + PV curve)
```

## Common recipes

### Recipe 1: EVM glossary
```
BAC  | Budget at Completion           | total planned $ for full project
PV   | Planned Value at date X        | BAC × (planned % complete at date X)
EV   | Earned Value at date X         | BAC × (actual % complete at date X)
AC   | Actual Cost at date X          | $ actually spent by date X

CV   | Cost Variance     | EV - AC   (negative = over budget)
SV   | Schedule Variance | EV - PV   (negative = behind schedule)
CPI  | Cost Performance  | EV / AC   (<1 = over budget)
SPI  | Schedule Performance | EV / PV (<1 = behind)
EAC  | Estimate at Completion | BAC / CPI (assumes CPI persists)
ETC  | Estimate to Complete  | EAC - AC
VAC  | Variance at Completion | BAC - EAC
TCPI | To-Complete Performance | (BAC - EV) / (BAC - AC)

Flag thresholds:
- CPI < 0.9 → flag
- SPI < 0.9 → flag
- TCPI > 1.1 → unrealistic recovery needed
- |CV%| > 10% → flag
- |SV%| > 10% → flag
```

### Recipe 2: EVM compute (Python)
```python
# evm.py — usage: uvx python evm.py inputs.json
import json, sys, math

# inputs.json = {
#   "BAC": 180000,
#   "PV":  117000,          # planned cumulative by today
#   "EV":   99000,          # earned cumulative by today (% complete × BAC)
#   "AC":  108000           # actual cumulative cost by today
# }
i = json.load(open(sys.argv[1]))
BAC, PV, EV, AC = i["BAC"], i["PV"], i["EV"], i["AC"]

CV  = EV - AC
SV  = EV - PV
CPI = EV / AC if AC else float("inf")
SPI = EV / PV if PV else float("inf")

# EAC formulas — pick based on assumption:
EAC_cpi = BAC / CPI if CPI else float("inf")          # most common (CPI persists)
EAC_remain_at_plan = AC + (BAC - EV)                  # remaining work at planned rate
EAC_combined = AC + (BAC - EV) / (CPI * SPI) if (CPI * SPI) else float("inf")  # CPI×SPI factor

ETC = EAC_cpi - AC
VAC = BAC - EAC_cpi
TCPI = (BAC - EV) / (BAC - AC) if (BAC - AC) else float("inf")

CV_pct = (CV / EV * 100) if EV else 0
SV_pct = (SV / PV * 100) if PV else 0

print(f"BAC:  ${BAC:>10,.0f}")
print(f"PV:   ${PV:>10,.0f}")
print(f"EV:   ${EV:>10,.0f}")
print(f"AC:   ${AC:>10,.0f}")
print()
print(f"CV:   ${CV:>+10,.0f} ({CV_pct:+.1f}%)  {'over' if CV<0 else 'under'} budget")
print(f"SV:   ${SV:>+10,.0f} ({SV_pct:+.1f}%)  {'behind' if SV<0 else 'ahead'}")
print(f"CPI:  {CPI:>10.2f}                {'FLAG' if CPI < 0.9 else 'ok'}")
print(f"SPI:  {SPI:>10.2f}                {'FLAG' if SPI < 0.9 else 'ok'}")
print()
print(f"EAC (CPI persists):       ${EAC_cpi:>10,.0f}")
print(f"EAC (remaining at plan):  ${EAC_remain_at_plan:>10,.0f}")
print(f"EAC (CPI × SPI):          ${EAC_combined:>10,.0f}")
print(f"ETC:                      ${ETC:>10,.0f}")
print(f"VAC:                      ${VAC:>+10,.0f}  {'over' if VAC<0 else 'under'} BAC")
print(f"TCPI:                     {TCPI:>10.2f}  ({'achievable' if TCPI <= 1.1 else 'UNREALISTIC — replan'})")
```

### Recipe 3: EVM interpretation matrix
```
| CPI | SPI | Meaning | Action |
|---|---|---|---|
| > 1.0 | > 1.0 | Ahead + under budget | Continue; consider pulling forward scope |
| > 1.0 | < 1.0 | Under budget but behind | Catch up via fast-track (no extra $) |
| < 1.0 | > 1.0 | Over budget but ahead | Slow burn; identify cost driver |
| < 1.0 | < 1.0 | Over budget AND behind — RED | Immediate replan; CR-level intervention |
| < 0.9 | < 0.9 | Critical — sponsor escalation | Re-baseline or kill |
```

### Recipe 4: EAC formulas (3 variants — pick by assumption)
```
Variant 1: EAC = BAC / CPI
  Use when: CPI is expected to persist
  Most common; pessimistic when CPI < 1.0

Variant 2: EAC = AC + (BAC - EV)
  Use when: remaining work will be at planned rate (CPI improves)
  Optimistic; assumes problem is past

Variant 3: EAC = AC + (BAC - EV) / (CPI × SPI)
  Use when: both schedule and cost performance issues persist
  Most pessimistic; reflects compounded inefficiency

Report all 3 in monthly steering; sponsor decides which to commit to.
```

### Recipe 5: Status report EVM snapshot block
```markdown
## EVM snapshot — Week of [YYYY-MM-DD]

| Metric | Value | Flag |
|---|---|---|
| BAC | $180,000 | — |
| PV (planned by today) | $117,000 (65%) | — |
| EV (earned by today) | $99,000 (55%) | — |
| AC (actual to date) | $108,000 | — |
| CV | -$9,000 (-9.1%) | 🟠 |
| SV | -$18,000 (-15.4%) | 🔴 |
| CPI | 0.92 | 🟠 |
| SPI | 0.85 | 🔴 |
| EAC (CPI persists) | $195,652 | — |
| ETC | $87,652 | — |
| VAC | -$15,652 | 🟠 |
| TCPI | 1.13 | 🟠 |

**Read:** Over budget AND behind schedule. SV worse than CV — the slip is primarily schedule.
**Driver:** SSO refactor (3.1.3) overrunning hours due to vendor cert dep (R-007).
**Action:** Crash 3.1.3 + 2.2.2 ($7k) recovers ~5 days; restores SPI > 0.95.
**Decision needed:** Approve $7k crash by Fri.
```

### Recipe 6: PV curve construction (S-curve)
```python
# pv-curve.py — generate planned cumulative spend curve from WBS
import json, datetime as dt
import matplotlib.pyplot as plt

wbs = json.load(open("wbs.json"))
# [{"wbs":"1.1.1","start":"2026-06-15","end":"2026-06-19","cost":1920}, ...]

# Spread each leaf's cost linearly over its days
daily = {}
for w in wbs:
    s = dt.date.fromisoformat(w["start"])
    e = dt.date.fromisoformat(w["end"])
    days = (e - s).days + 1
    per_day = w["cost"] / days
    cur = s
    while cur <= e:
        daily[cur] = daily.get(cur, 0) + per_day
        cur += dt.timedelta(days=1)

# Cumulative PV by date
dates = sorted(daily)
cum = []
total = 0
for d in dates:
    total += daily[d]
    cum.append(total)

plt.plot(dates, cum, label="PV (planned cumulative)")
plt.xlabel("Date"); plt.ylabel("$")
plt.title("Planned Value S-curve")
plt.savefig("pv-curve.png")
```

### Recipe 7: EV measurement methods (pick per WBS family)
```
0/100 (binary)
  - 0% until complete, then 100%
  - Best for: 1-day-or-less leaves, milestones
  - Easy to game; precise after completion

0/50/100
  - 0% at start, 50% when in progress, 100% complete
  - Best for: mid-size leaves (3-10 days)
  - Less gameable than 0/100; reasonable approximation

Percent-complete (subjective)
  - PM/team estimates % complete
  - Best for: ongoing work, level-of-effort
  - Most gameable; needs weekly cross-check via PR/UAT status

Milestone-weighted
  - Predefined milestones with weights (e.g., M1=25%, M2=25%, M3=50%)
  - Best for: vendor SOWs with milestone payments
  - Clean; aligns with payment schedule

Level-of-effort (LOE)
  - EV = PV (mirrors plan)
  - Best for: support / overhead tasks
  - Not useful for performance signal; budget tracking only

Apportioned effort
  - Tied to performance of related discrete work
  - Best for: QA tied to dev throughput
  - Niche

Pick ONE per WBS family + document in charter.
```

### Recipe 8: Auto-aggregate EVM data
```bash
#!/usr/bin/env bash
# evm-aggregate.sh — weekly Friday cron

WEEK_END=$(date +%Y-%m-%d)
PROJECT_ID=12345
BAC=180000

# AC from Harvest
AC=$(curl -s "https://api.harvestapp.com/v2/reports/time/projects?from=2026-06-15&to=$WEEK_END&project_id=$PROJECT_ID" \
  -H "Authorization: Bearer $HARVEST_TOKEN" -H "Harvest-Account-Id: $HARVEST_ACCOUNT_ID" -H "User-Agent: PM-Agent (you@email.com)" \
  | jq '.results[0].total_cost')

# EV from Linear (% complete × BAC)
PCT_COMPLETE=$(curl -s "https://api.linear.app/graphql" -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query":"{ project(id:\"<id>\") { progress } }"}' \
  | jq '.data.project.progress')
EV=$(echo "$BAC * $PCT_COMPLETE" | bc -l)

# PV from Notion DB (PV S-curve indexed by date)
PV=$(mcp tool notion.query_database --database_id "<pv-curve-db>" --filter "{\"property\":\"Date\",\"date\":{\"on_or_before\":\"$WEEK_END\"}}" \
  | jq '[.results[] | .properties.PV_cum.number] | last')

# Compute via Recipe 2
echo "{\"BAC\":$BAC,\"PV\":$PV,\"EV\":$EV,\"AC\":$AC}" > evm-input.json
uvx python evm.py evm-input.json > evm-output.txt
cat evm-output.txt

# Archive to Notion
mcp tool notion.create_page --parent "{\"database_id\":\"<evm-archive>\"}" \
  --properties "{\"Name\":{\"title\":[{\"text\":{\"content\":\"EVM $WEEK_END\"}}]}}" \
  --children "$(cat evm-output.txt)"
```

### Recipe 9: EVM trend chart
```python
# evm-trend.py
import json, matplotlib.pyplot as plt
hist = json.load(open("evm-weekly.json"))
# [{"week":"W22","PV":85000,"EV":80000,"AC":83000}, ...]

weeks = [d["week"] for d in hist]
plt.plot(weeks, [d["PV"] for d in hist], label="PV (planned)", linestyle="--")
plt.plot(weeks, [d["EV"] for d in hist], label="EV (earned)")
plt.plot(weeks, [d["AC"] for d in hist], label="AC (actual)")
plt.axhline(y=180000, color="red", linestyle=":", label="BAC")
plt.legend(); plt.ylabel("$"); plt.xticks(rotation=45); plt.tight_layout()
plt.savefig("evm-trend.png")
```

### Recipe 10: EVM + CPM cross-check
```
EVM SPI ≠ critical-path SPI necessarily:
- EVM SPI is dollar-weighted across all work
- CPM-derived SPI looks only at critical-path tasks

Reconcile:
1. Compute weighted SPI of critical-path tasks only
2. If CPM-SPI worse than overall SPI → schedule slip is on critical path → urgent
3. If CPM-SPI better than overall SPI → slack tasks slipping → less urgent (until float consumed)

Action: report both in monthly steering.
```

### Recipe 11: TCPI interpretation
```
TCPI = (BAC - EV) / (BAC - AC)

If TCPI = 1.0  → continue at current efficiency → hit BAC
If TCPI < 1.0  → BAC achievable with less efficiency than current → ahead
If TCPI > 1.1  → would need significant productivity gain → UNREALISTIC
If TCPI ∞      → AC > BAC → blown the budget; replan required

Threshold: TCPI > 1.1 is sponsor-escalate signal.
```

### Recipe 12: Re-baseline trigger (when EVM signals can't be ignored)
```
Re-baseline (per sponsor decision) when:
- CPI < 0.85 sustained 4+ weeks
- TCPI > 1.2 sustained
- VAC > 20% of BAC
- Approved CRs cumulatively > 20% scope change

Re-baseline procedure:
1. Recompute PV curve from current state (new EAC becomes new "BAC")
2. CCB approval for new baseline
3. Re-run all EVM going forward against new baseline
4. Archive old baseline (audit trail)
```

## Examples

### Example 1: Weekly EVM for status report
**Goal:** Friday EVM snapshot.

**Steps:**
1. Recipe 8 auto-aggregate.
2. Recipe 2 compute.
3. Recipe 5 status block.
4. Embed in weekly status (cross-link status-reporting skill).

**Result:** "CPI 0.92 / SPI 0.85; SV the main concern; mitigation in flight."

### Example 2: Sponsor decision on EAC
**Goal:** Month-end: which EAC variant to commit to?

**Steps:**
1. Recipe 4 — compute all 3 variants.
2. Variant 1 (CPI persists): $195k. Variant 2 (improves): $189k. Variant 3 (compounded): $211k.
3. Sponsor brief: present range; recommend commit to Variant 1.
4. Track delta from commit weekly.

**Result:** $195k commit; sponsor + finance aligned.

### Example 3: Replan trigger
**Goal:** TCPI 1.18 sustained 4 weeks.

**Steps:**
1. Recipe 11 flags unrealistic.
2. Sponsor brief: options — scope cut ($10k savings) + crash ($5k cost) → restore TCPI to 1.04.
3. Recipe 12 re-baseline if accepted.
4. CR triggered (cross-link change-request-management).

**Result:** Project re-baselined; clean EVM forward.

## Edge cases / gotchas

- **EVM useless without good % complete data.** Garbage in, garbage out.
- **0/100 measurement gameable late.** Devs report "done" mid-PR review. Cross-check via DoD.
- **Early-project EVM noisy.** First 20% of project, CPI swings wildly. Useful from ~30% onward.
- **AC must include all loaded cost.** Salary × overhead (1.4-1.6x typical) + tooling + vendor. Hour × billable rate ≠ AC for internal team.
- **Capital vs expense.** Capitalized portion flows to balance sheet; PM tracks both for full picture.
- **Multi-currency.** Lock FX rate at baseline; revalue at month-end.
- **EVM at WBS level + roll up.** Compute per WBS leaf; aggregate up. Avoids one-number averaging issues.
- **PV curve is S-shaped.** Not linear. Use Recipe 6 daily-distribution method, not constant burn rate.
- **EVM ≠ CPM.** EVM is $$-time integration; CPM is task network. Use both.
- **EAC variants differ widely.** Don't pick the most optimistic without sponsor agreement.
- **TCPI > 1.1 = replan, not pep talk.** Don't expect 10%+ productivity gain mid-project.
- **Re-baselining is governance event.** CCB approval; old baseline archived; audit trail.
- **EVM hides bottlenecks.** Aggregate CPI healthy can mask one disastrous WBS branch. Drill weekly.
- **LOE makes EVM less useful.** Level-of-effort tasks where EV = PV by definition; track separately.
- **Tempo for Jira → AC for Jira shops.** Tempo Cost Tracking add-on gives loaded AC.
- **CPI vs SPI divergence diagnoses.** Schedule problem? Cost problem? Both? Drives different mitigations.
- **EVM is a leading indicator at 30-60% complete.** Late-project EVM is mostly accounting.
- **Sponsor may not understand EVM jargon.** Translate to plain English: "We're 9% over budget and 15% behind schedule; here's why and our plan."

## Sources

- [PMI Earned Value canon](https://www.pmi.org/learning/library/earned-value-project-management-method-measuring-5037)
- [PMBOK 7th Edition: EVM](https://www.pmi.org/standards/pmbok)
- [EV + critical-path congruence](https://www.casinelli.net/en/congruenza-tra-metriche-earned-value-e-critical-path/)
- [Smartsheet EVM templates](https://www.smartsheet.com/free-earned-value-management-templates)
- [Atlassian project cost variance](https://www.atlassian.com/agile/project-management/budget-variance)
- [Primavera P6 EVM](https://www.oracle.com/industries/construction-engineering/primavera-p6/)
- [Tempo Cost Tracking](https://www.tempo.io/products/jira-time-tracking/cost-tracker)
- [EVM Wikipedia (formulas reference)](https://en.wikipedia.org/wiki/Earned_value_management)
- [DoD EVM standard](https://www.acq.osd.mil/asda/dpc/cp/policy/evm.html)
