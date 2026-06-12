<!--
Source: https://developer.float.com/api_reference.html
Source: https://app.runn.io/api/v0/docs
Source: https://help.resourceguruapp.com/article/19-resource-guru-api-documentation
-->
# Resource Allocation: Float / Runn / Resource Guru / Smartsheet RM — SKILL

The four leading resource-management platforms in 2026 + Smartsheet Resource Management for Smartsheet shops. Each exposes REST API for people / projects / allocations / leave / utilization.

## When to use

- Allocating people across projects + tracking utilization (target 70-85% billable).
- Surfacing >100% (over-allocated) weeks per person.
- Capacity forecasting: demand (project pipeline × person-weeks) vs supply (FTE - PTO - committed).
- Profitability tracking on consulting projects (Runn specialty).
- Leave management + PTO sync to schedule.

Trigger phrases: "allocate resources", "who's over-allocated", "capacity plan", "Float schedule", "Runn forecast", "resource heatmap", "utilization report".

## Setup

```bash
# Float (paid — $7.50/user/mo)
curl -fsSL "https://api.float.com/v3/accounts" \
  -H "Authorization: Bearer $FLOAT_API_KEY" \
  -H "User-Agent: PM-Agent (email@example.com)"

# Runn (paid — $10/user/mo)
curl -fsSL "https://api.runn.io/v0/accounts" \
  -H "Authorization: Bearer $RUNN_API_KEY"

# Resource Guru (paid — $2.50/user/mo, cheapest)
curl -fsSL "https://api.resourceguruapp.com/v1/<account-slug>/users/me" \
  -H "Authorization: Bearer $RG_TOKEN"

# Smartsheet Resource Management (bundled with Smartsheet Pro+)
curl -fsSL "https://api.smartsheet.com/2.0/server/resourcemanagement/<workspace>/people" \
  -H "Authorization: Bearer $SMARTSHEET_TOKEN"
```

Auth:
- `FLOAT_API_KEY` — Float app → Account → Integrations → API. Required `User-Agent` header per Float docs
- `RUNN_API_KEY` — Runn → Settings → API tokens (Business plan and above)
- `RG_TOKEN` — Resource Guru → Account Settings → API
- `SMARTSHEET_TOKEN` — same as Smartsheet (resource-management is bundled feature)

## Common recipes

### Recipe 1: Float — list all people + capacity
```bash
curl -s "https://api.float.com/v3/people?per_page=100" \
  -H "Authorization: Bearer $FLOAT_API_KEY" \
  -H "User-Agent: PM-Agent (you@email.com)" \
| jq '.[] | {id, name, role: .job_title, capacity_hours_per_day: .people_type_id, department: .department.name}'
```

### Recipe 2: Float — create an allocation
```bash
curl -X POST "https://api.float.com/v3/allocations" \
  -H "Authorization: Bearer $FLOAT_API_KEY" \
  -H "User-Agent: PM-Agent (you@email.com)" \
  -H "Content-Type: application/json" \
  -d '{
    "people_id": 12345,
    "project_id": 67890,
    "phase_id": null,
    "start_date": "2026-06-15",
    "end_date": "2026-06-19",
    "hours": 40,
    "notes": "Onboarding revamp sprint 27 — frontend"
  }'
```

### Recipe 3: Float — list allocations + compute weekly utilization
```bash
# Pull all allocations for a date range
curl -s "https://api.float.com/v3/allocations?start_date=2026-06-15&end_date=2026-06-19&per_page=200" \
  -H "Authorization: Bearer $FLOAT_API_KEY" \
  -H "User-Agent: PM-Agent (you@email.com)" \
| jq 'group_by(.people_id) | map({people_id: .[0].people_id, total_hours: ([.[].hours] | add)})'
```

### Recipe 4: Float — surface over-allocated people week-of
```bash
# Assume 40 hrs/week standard capacity; flag total > 40
curl -s "https://api.float.com/v3/allocations?start_date=2026-06-15&end_date=2026-06-19" \
  -H "Authorization: Bearer $FLOAT_API_KEY" \
  -H "User-Agent: PM-Agent (you@email.com)" \
| jq 'group_by(.people_id) |
  map({people_id: .[0].people_id, total: ([.[].hours] | add)}) |
  map(select(.total > 40))'
```

### Recipe 5: Runn — get utilization report
```bash
# Runn ships native utilization endpoint
curl -s "https://api.runn.io/v0/utilization?start_date=2026-06-15&end_date=2026-06-19&group_by=person" \
  -H "Authorization: Bearer $RUNN_API_KEY" \
| jq '.[] | {name, capacity, allocated, utilization_pct: ((.allocated / .capacity) * 100)}'
```

### Recipe 6: Runn — profitability forecast on a project
```bash
curl -s "https://api.runn.io/v0/projects/<project-id>/profitability" \
  -H "Authorization: Bearer $RUNN_API_KEY" \
| jq '{budget, billable, cost, profit, margin: (.profit / .budget)}'
```

### Recipe 7: Resource Guru — create a booking
```bash
curl -X POST "https://api.resourceguruapp.com/v1/<account-slug>/bookings" \
  -H "Authorization: Bearer $RG_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "resource_id": 12345,
    "project_id": 67890,
    "client_id": 11111,
    "start_date": "2026-06-15",
    "end_date": "2026-06-19",
    "start_time": "09:00",
    "end_time": "17:00",
    "duration": 2400,
    "details": "Onboarding revamp"
  }'
```

### Recipe 8: Resource Guru — leave management (PTO entry)
```bash
curl -X POST "https://api.resourceguruapp.com/v1/<account-slug>/bookings" \
  -H "Authorization: Bearer $RG_TOKEN" \
  -d '{
    "resource_id": 12345,
    "leave_type_id": 99,
    "start_date": "2026-07-15",
    "end_date": "2026-07-19"
  }'
```

### Recipe 9: Resource plan template (Notion DB schema)
```yaml
# Use when no paid RM platform available — Notion fallback
Database: "Resource Plan — Q3"
Properties:
  Person:                title
  Role:                  select (Eng/Design/Data/PM/QA)
  W1_2026-06-15:         number  # hours
  W2_2026-06-22:         number
  W3_2026-06-29:         number
  # ... one column per week ...
  Capacity_per_week:     number (default 40)
  Focus_factor:          number (default 0.7)
  Effective_capacity:    formula (Capacity * Focus)
  Utilization_W1:        formula (W1 / Effective_capacity)
  Over_allocated:        formula (Utilization_W1 > 1)
```

### Recipe 10: Capacity = FTE × hours × focus factor (defaults)
```
Engineering deep work: 0.6-0.7
Design:                0.6-0.7
PM / coordination:     0.5-0.6
QA:                    0.7-0.8
DevOps / SRE on-call:  0.4-0.5 (interrupts)

Per-week capacity (hrs) = headcount × 40 × focus_factor

Example: 3 eng × 40 × 0.65 = 78 hrs/week effective
PTO subtraction: subtract 8 hrs per PTO-day from that week
```

### Recipe 11: Over-allocation handling playbook
```
When utilization > 100% for week W:
1. Surface in status report — RAG amber on resource dimension
2. Replan options (in order):
   a. Move task to next week (if float allows — check CPM)
   b. Reassign to another person with capacity
   c. Hire / contract (10-30 day lead)
   d. Defer scope via CR (last resort)
3. If material (>20% over): CR required
4. If repeated 2+ weeks: capacity planning fail — escalate to sponsor
```

### Recipe 12: Resource utilization heatmap (CSV → Excalidraw or matplotlib)
```python
# heatmap.py
import json, sys
import matplotlib.pyplot as plt
import numpy as np

data = json.load(open(sys.argv[1]))  # [{person, week, hours, capacity}]
people = sorted(set(d["person"] for d in data))
weeks  = sorted(set(d["week"] for d in data))

matrix = np.zeros((len(people), len(weeks)))
for d in data:
    i = people.index(d["person"])
    j = weeks.index(d["week"])
    matrix[i][j] = d["hours"] / d["capacity"]  # utilization ratio

fig, ax = plt.subplots(figsize=(12, len(people) * 0.4))
im = ax.imshow(matrix, cmap="RdYlGn_r", vmin=0, vmax=1.5, aspect="auto")
ax.set_xticks(range(len(weeks))); ax.set_xticklabels(weeks, rotation=45)
ax.set_yticks(range(len(people))); ax.set_yticklabels(people)
plt.colorbar(im, label="Utilization (1.0 = 100%)")
plt.tight_layout(); plt.savefig("util.png")
```

### Recipe 13: Demand vs Supply quarterly forecast
```bash
# Demand: sum of allocated hours from pipeline projects
demand=$(curl -s "https://api.runn.io/v0/projects?status=tentative,active&start_date=2026-07-01&end_date=2026-09-30" \
  -H "Authorization: Bearer $RUNN_API_KEY" \
  | jq '[.[] | .planned_hours] | add')

# Supply: FTE × 40 × 0.7 × 13 weeks - PTO hours
supply=$(curl -s "https://api.runn.io/v0/people?active=true" \
  -H "Authorization: Bearer $RUNN_API_KEY" \
  | jq '[.[] | .working_hours_per_week * 13 * 0.7] | add')

echo "Q3 demand: $demand hrs"
echo "Q3 supply: $supply hrs"
echo "Gap: $((supply - demand)) hrs"
```

## Examples

### Example 1: Plan resources for Onboarding Revamp Q3
**Goal:** Lock who works what week for 13-week project.

**Steps:**
1. Pull Float `/v3/people` — list 12 available (3 eng, 2 design, 1 data, 1 PM, +6 shared).
2. Allocate per WBS work package: Recipe 2 for each (person × week × hours).
3. Run Recipe 4 weekly to surface >100% weeks.
4. Adjust: shift 2.2.3 (Mobile parity) from W3 to W5 — relieves over-allocation.
5. Generate Recipe 12 heatmap → embed in kickoff deck.

**Result:** 13-week allocation plan, no over-allocated weeks, sponsor sign-off Friday.

### Example 2: Forecast Q3 capacity vs demand
**Goal:** Sponsor wants to know if Q3 has bandwidth for 2 more initiatives.

**Steps:**
1. Recipe 13 → demand 8400 hrs, supply 9100 hrs (13-week, 12 FTE × 0.7 focus).
2. Headroom 700 hrs ≈ 9% of supply.
3. 2 proposed initiatives = 1200 hrs. Gap: 500 hrs short.
4. Options surfaced: defer 1 initiative; contract 2 FTEs; sacrifice 0.1 focus factor.
5. Sponsor decides at portfolio review.

**Result:** Quantified Q3 capacity decision; no over-commit.

## Edge cases / gotchas

- **Float API requires `User-Agent` header.** Without it, 400 error. Include email per Float docs.
- **Float allocation hours field is total over date range.** 40 hrs over 5 days = 8 hrs/day. For half-day, set 20 over 5 days.
- **Float uses `people_type_id` for capacity.** Not a direct `capacity_per_day` field — map type-id → hours in your client.
- **Runn rate limit 60 req/min/token.** Bulk operations batch; backoff on 429.
- **Runn paid plan only.** No free tier; trial 14 days.
- **Resource Guru subdomain.** All URLs include `<account-slug>` — check URL of your Guru workspace.
- **Resource Guru duration in minutes.** `duration: 2400` = 40 hrs × 60 min — easy to off-by-60.
- **Smartsheet Resource Management is Pro+ bundled.** Not separate API key; same `$SMARTSHEET_TOKEN`.
- **Focus factor varies by team.** 0.7 default is engineering ballpark; verify per team via 2-week timesheet sample before locking.
- **PTO sync.** Float / Runn / RG all have leave types; sync from HR system (BambooHR / Rippling) to avoid manual PTO entry.
- **Capacity vs availability.** Capacity = max hours theoretically. Availability = capacity - PTO - meetings - already-allocated. Surface availability per week, not capacity.
- **Over-allocation triggers material change.** > 20% over 2 weeks → CR. Don't paper over with "team will work harder."
- **Free fallback: Notion DB.** Recipe 9. For solo PMs / sub-5-person teams, Notion + matplotlib heatmap covers 80% of paid RM features.
- **Smartsheet Resource Management API has different base.** `/server/resourcemanagement/`, not `/2.0/`. Auth same.
- **Hires/contractors not in supply until start date.** Forecast counts only confirmed FTE × % allocation × time-in-quarter.

## Sources

- [Float API reference](https://developer.float.com/api_reference.html)
- [Runn API docs](https://app.runn.io/api/v0/docs)
- [Resource Guru API documentation](https://help.resourceguruapp.com/article/19-resource-guru-api-documentation)
- [Smartsheet Resource Management](https://www.smartsheet.com/content/resource-management)
- [PMI resource management practice](https://www.pmi.org/learning/library/effective-resource-management-best-practices-9981)
- [Capacity planning guide (Atlassian)](https://www.atlassian.com/agile/agile-at-scale/capacity-planning)
- [Float pricing 2026](https://www.float.com/pricing)
- [Resource Guru pricing 2026](https://resourceguruapp.com/pricing)
