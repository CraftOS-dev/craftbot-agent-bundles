<!--
Sources: https://developers.greenhouse.io/harvest.html#reports
         https://developers.ashbyhq.com/reference
         https://www.greenhouse.io/blog/recruiting-funnel-metrics
         https://www.lever.co/blog/recruiting-metrics-funnel
Canonical formulas + 2026 benchmarks live in role.md "Recruiting metrics formulas".
-->
# Recruiting Metrics — Time-to-Fill / Offer-Accept — SKILL

Pull, compute, and report the canonical recruiting metrics: time-to-fill, time-to-offer, offer-accept rate, candidate NPS, source-of-hire, cost-per-hire, quality-of-hire, and DEI funnel metrics. Outputs land in `google-sheet` weekly + `pptx` quarterly. Adverse-impact interpretation defers to `legal-counsel`.

## When to use

- Weekly: refresh recruiting dashboard for HM + CEO standup.
- Quarterly: build leadership review deck with trended metrics + benchmarks.
- Mid-quarter: deep-dive any breached SLA (time-to-fill exceeded benchmark, offer-accept dropping).
- Trigger phrases: "recruiting metrics", "time-to-fill", "offer accept rate", "candidate NPS", "source of hire", "funnel report", "DEI funnel", "cost per hire", "weekly sync".

Canonical formulas + 2026 benchmarks live in `role.md` "Recruiting metrics formulas". Adverse impact / 4/5 rule interpretation → `legal-counsel`.

## Setup

```bash
# Greenhouse Reports
export GREENHOUSE_API_KEY="harvest_xxx"
export GH_USER_ID="123456"

# Ashby Analytics
export ASHBY_API_KEY="xxx"

# Lever Reports
export LEVER_API_KEY="xxx"; export LEVER_USER_ID="xxx"

# Output
export GOOGLE_SHEETS_OAUTH="<bearer>"  # google-workspace-mcp
# pptx generated via python-pptx
```

Auth model: same basic-auth-with-empty-password as ATS configuration skill. Reports API + Analytics endpoints are read-only.

## Common recipes

### Recipe 1: List custom reports (Greenhouse)
```bash
curl -s -u "$GREENHOUSE_API_KEY:" \
  "https://harvest.greenhouse.io/v1/custom_fields?field_type=offer" | jq
# OR Reports API
curl -s -u "$GREENHOUSE_API_KEY:" \
  "https://harvest.greenhouse.io/v1/reports/job_funnel_report?start_date=2026-01-01&end_date=2026-06-09"
```

### Recipe 2: Time-to-fill per req (Greenhouse, computed from candidate data)
```python
import requests, os, pandas as pd
# Pull hires in window
hires = requests.get(
  "https://harvest.greenhouse.io/v1/candidates?status=hired&hired_after=2026-01-01",
  auth=(os.environ["GREENHOUSE_API_KEY"], "")
).json()
rows = []
for c in hires:
  for a in c["applications"]:
    if a.get("status") == "hired" and a.get("offers"):
      offer = a["offers"][0]
      req = requests.get(f"https://harvest.greenhouse.io/v1/jobs/{a['job_id']}",
                        auth=(os.environ["GREENHOUSE_API_KEY"], "")).json()
      ttf = (pd.to_datetime(offer["resolved_at"]) - pd.to_datetime(req["opened_at"])).days
      rows.append({"job": req["name"], "candidate": c["first_name"], "days_to_fill": ttf, "role_family": req.get("departments", [{}])[0].get("name")})
df = pd.DataFrame(rows)
print(df.groupby("role_family")["days_to_fill"].describe())
```
Compare to role.md benchmarks: 30-45 IC, 60-90 senior, 90-150 exec.

### Recipe 3: Offer-acceptance rate (Greenhouse)
```python
# offers extended in window vs offers accepted
import requests, os
extended = requests.get(
  "https://harvest.greenhouse.io/v1/offers?created_after=2026-01-01",
  auth=(os.environ["GREENHOUSE_API_KEY"], "")
).json()
accepted = [o for o in extended if o["status"] == "accepted"]
declined = [o for o in extended if o["status"] == "rejected"]
rate = len(accepted) / max(1, len(accepted) + len(declined))
print(f"Offer-accept rate: {rate:.1%}  (target >85% strong, >90% elite)")
```

### Recipe 4: Source-of-hire breakdown (Greenhouse)
```python
import requests, os
from collections import Counter
hires = requests.get(
  "https://harvest.greenhouse.io/v1/candidates?status=hired&hired_after=2026-01-01",
  auth=(os.environ["GREENHOUSE_API_KEY"], "")
).json()
src = Counter(c.get("application_source", {}).get("source_name", "unknown") for c in hires)
total = sum(src.values())
for k, v in src.most_common():
  print(f"{k:30s} {v:4d}  {v/total:.1%}")
```

### Recipe 5: Pull Ashby analytics directly (job_funnel_report equivalent)
```bash
curl -s -X POST -u "$ASHBY_API_KEY:" \
  -H "Content-Type: application/json" \
  "https://api.ashbyhq.com/report.create" \
  -d '{
    "reportType": "JobFunnel",
    "filters": {"jobIds": ["<job_id>"], "createdAfter": "2026-01-01"}
  }'
# Returns report URL after async generation; poll report.list for status
```

### Recipe 6: Compute time-to-offer (Ashby)
```bash
curl -s -X POST -u "$ASHBY_API_KEY:" \
  -H "Content-Type: application/json" \
  "https://api.ashbyhq.com/application.list" \
  -d '{"status": "ACTIVE,OFFER", "createdAfter": "2026-01-01"}' \
  | jq '.results[] | {id, firstInterview: (.interviews | map(.scheduledStart) | min), offerExtendedAt: .offer.extendedAt}'
```

### Recipe 7: DEI funnel by EEO-1 category (Greenhouse, aggregated only)
```bash
# Demographic data ONLY surfaces aggregated; never tied to candidate IDs.
# Pull EEO Reports endpoint:
curl -s -u "$GREENHOUSE_API_KEY:" \
  "https://harvest.greenhouse.io/v1/eeoc?start_date=2026-01-01&end_date=2026-06-09" \
  | jq '.[] | {category, stage, count}'
```
Analyze with `dei-hiring-diverse-slate-blind-resume` skill; flag 4/5 violations to `legal-counsel`.

### Recipe 8: Candidate NPS (post-decision survey)
```bash
# Pulled from Typeform / SurveyMonkey; weighted by stage (post-screen / post-onsite / post-decision)
curl -s -H "Authorization: Bearer $TYPEFORM_TOKEN" \
  "https://api.typeform.com/forms/<form_id>/responses?since=2026-04-01" \
  | jq '[.items[] | {nps: .answers[0].number, stage: .hidden.stage}] | group_by(.stage)
        | map({stage: .[0].stage, count: length,
               promoters: ([.[]|select(.nps>=9)]|length),
               detractors: ([.[]|select(.nps<=6)]|length)})
        | map(. + {nps_score: ((.promoters - .detractors)/.count * 100)})'
```

### Recipe 9: Cost-per-hire computation (rolling 90-day)
```python
import os
recruiting_spend = 245_000   # salaries fully loaded + tools + ads + agency  (sum manually quarterly)
hires_count = 18             # hires in window from Recipe 4
cph = recruiting_spend / max(1, hires_count)
print(f"Cost per hire: ${cph:,.0f}  (industry benchmark $4-5K IC, $10-30K senior, $30K+ exec)")
```

### Recipe 10: Quality-of-hire composite (90-day stay + manager-sat)
```python
# Pull 90-day stay rate from operations-agent's onboarding data; manager sat from quarterly survey.
# Composite: 0.4 * (90d_stay_rate) + 0.4 * (manager_sat_avg / 5) + 0.2 * (post-hire performance rating / 5)
# Output per source-of-hire bucket → identifies which channels deliver high-QoH.
```

### Recipe 11: Push weekly snapshot to Google Sheet
```python
# google-workspace-mcp / gspread
import gspread
gc = gspread.service_account()
sh = gc.open("Recruiting Weekly Dashboard")
ws = sh.worksheet("Snapshot")
ws.update("A1", [["Week", "Open reqs", "Hires", "Time-to-fill avg", "Offer-accept %", "NPS"]])
ws.append_row([str(pd.Timestamp.today().date()), 24, 18, 38, 0.89, 54])
```

### Recipe 12: Quarterly PPTX deck (python-pptx)
```python
from pptx import Presentation
from pptx.util import Inches
prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[5])
slide.shapes.title.text = "Q2 2026 Recruiting Review"
slide.placeholders[1].text = "Time-to-fill IC: 38 days (target 30-45)\nOffer-accept: 89% (elite >90%)\nNPS: 54 (strong >50)"
prs.save("Q2_recruiting_review.pptx")
```

## Examples

### Example 1: Weekly recruiting sync standup (15 min)
**Goal:** 15-min standup: what shipped / what's at risk / what I need.
**Steps:**
1. Recipe 2 + Recipe 3 + Recipe 4 produce: TTF avg, offer-accept %, source mix.
2. Recipe 7 produces DEI funnel snapshot.
3. Recipe 11 lands all in Google Sheet "Recruiting Weekly Dashboard".
4. Recruiter pulls 3 callouts: top win, top risk, top ask.

**Result:** No 30-min status meeting; CEO + HM aligned in 15 min.

### Example 2: Quarterly review deck
**Goal:** Q-over-Q trend visibility for leadership.
**Steps:**
1. Pull last 4 quarters of data via Recipes 2 + 3 + 4 + 8 + 9 + 10.
2. Build comparison table (this Q vs last Q vs same-Q-LY).
3. Surface 2-3 strategic shifts driven by data (e.g., "doubled referral source — closed 6 hires from referrals this Q; recommend increasing bonus from $3K to $5K").
4. Recipe 12 outputs deck.

**Result:** Leadership sees trends + strategy proposals; data-driven Q+1 plan.

### Example 3: Source-of-hire ROI deep-dive
**Goal:** Should we keep the LinkedIn Recruiter seat?
**Steps:**
1. Recipe 4: source mix.
2. Recipe 9: cost per source (split LinkedIn seat cost across LinkedIn-sourced hires).
3. Recipe 10: quality per source (90-day stay + manager sat).
4. Output: ROI table per source.

**Result:** "LinkedIn delivers 22% of hires but 35% of QoH composite — keep seat" OR "LinkedIn at $X per hire, referral at $Y per hire with 1.5× QoH — shift budget."

## Edge cases / gotchas

- **Time-to-fill "starts when?"** Req-opened ≠ candidate-found ≠ first-interview. Pick one definition, document it, stick with it. `role.md` canonical: req-opened → accepted-offer.
- **Hiring vs Hired status.** Greenhouse `status=hired` may include candidates not started yet. Filter on `hired_at` date.
- **Time-zone in `resolved_at`.** Greenhouse returns UTC; report in recipient TZ.
- **Adverse impact (4/5 rule).** Selection rate of minority group ≥ 80% of majority group. If violated, statistical significance test required — **defer interpretation to `legal-counsel`**. Don't change hiring decisions on raw stats.
- **Demographic data aggregation only.** Never join individual demographic responses to candidate decisions in reports. Greenhouse `/eeoc` endpoint returns aggregated buckets — use those.
- **Source attribution drift.** "LinkedIn" sometimes records via apply, sometimes via recruiter-tagged sourcing; dedupe by candidate ID + first-source-touch.
- **Cost-per-hire denominator.** Don't divide by hires in window — fully-loaded recruiter salary covers the whole quarter even if hires concentrate in one month. Use 90-day rolling.
- **Quality-of-hire data lag.** 90-day stay needs 90 days post-hire data. Lag the QoH report one quarter.
- **Greenhouse Reports API rate limits.** Same 50/10s; long reports return async — poll `/v1/reports/<id>` for status.
- **Ashby analytics async.** `report.create` returns immediately; poll `report.list?reportId=` until `status=COMPLETE` then fetch CSV/JSON.
- **Pulling raw funnel from Lever.** Lever doesn't expose `job_funnel_report` — compute from `/v1/opportunities?stage_id=` per stage with snapshot timestamps; more work than Greenhouse/Ashby.
- **Defer to `legal-counsel`** for: EEO-1 reporting format, OFCCP audit prep, 4/5 rule statistical interpretation, demographic-data retention windows.

## Sources

- [Greenhouse Harvest Reports](https://developers.greenhouse.io/harvest.html#reports)
- [Greenhouse Job Funnel Report](https://developers.greenhouse.io/harvest.html#get-retrieve-job-funnel-report)
- [Ashby Reports API](https://developers.ashbyhq.com/reference/reportcreate)
- [Greenhouse recruiting-funnel-metrics blog](https://www.greenhouse.io/blog/recruiting-funnel-metrics)
- [Lever recruiting metrics funnel](https://www.lever.co/blog/recruiting-metrics-funnel)
- [Talent Board CandE Research (NPS benchmarks)](https://www.thetalentboard.org/cande-research-reports/)
- [Metaview recruiting metrics 2026](https://www.metaview.ai/resources/blog/recruiting-metrics)
- [SHRM cost-per-hire methodology](https://www.shrm.org/topics-tools/news/talent-acquisition/calculate-cost-per-hire)
