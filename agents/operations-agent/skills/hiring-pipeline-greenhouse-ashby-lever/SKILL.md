<!--
Sources: https://unified.to/blog/15_ats_apis_to_integrate_with_in_2026_greenhouse_lever_workable
         https://www.index.dev/blog/greenhouse-vs-lever-vs-ashby-ats-comparison
         https://cavuno.com/blog/ats-platforms-public-job-posting-apis
ATS landscape 2026: Greenhouse = #1 G2 Winter 2026, 7,500+ customers.
Ashby = founded 2019, deepest analytics + compensation field on public feed.
Lever = ATS+CRM in one.
-->
# Hiring Pipeline — Greenhouse / Ashby / Lever — SKILL

Structured-hiring ATS recipes covering candidate CRUD, pipeline reports, interview scorecards, offer letters, and pipeline reporting across the three SOTA SMB-to-growth-stage ATSes. Defaults to Greenhouse for structured-hiring teams, Ashby for data-obsessed growth-stage shops, Lever for ATS+CRM unified workflows.

## When to use

- User wants to **create a job, open a requisition, push candidates, move stages, schedule interviews, submit scorecards, or extend offers** on Greenhouse / Ashby / Lever.
- Building a **pipeline report** (time-to-hire, time-in-stage, source attribution, interviewer scorecard ratios).
- Public **job feed mirroring** for a careers page (Ashby `includeCompensation=true`, Lever JSON feed).
- Trigger phrases: "open req", "post a job", "move candidate to onsite", "send offer", "pipeline velocity", "careers page sync".

## Setup

```bash
# All three publish REST APIs. Use cli-anything for raw curl.
# Greenhouse (Harvest API for write, Job Board API for public feed)
export GREENHOUSE_API_KEY="harvest_xxx"    # https://app.greenhouse.io/configure/dev_center/credentials
export GREENHOUSE_BOARD_TOKEN="company"    # public job-board slug

# Ashby
export ASHBY_API_KEY="xxx"                 # https://app.ashbyhq.com/admin/api-keys

# Lever
export LEVER_API_KEY="xxx"                 # https://hire.lever.co/settings/integrations/api
export LEVER_SITE="company"                # public posting feed slug
```

Auth:
- `GREENHOUSE_API_KEY` — basic auth (`-u "$GREENHOUSE_API_KEY:"`). Free for the API; ATS seat is paid. Per-user permissions matter.
- `ASHBY_API_KEY` — basic auth. Same model.
- `LEVER_API_KEY` — basic auth. Paid platform.

## Common recipes

### Recipe 1: List open jobs (Greenhouse)
```bash
curl -s -u "$GREENHOUSE_API_KEY:" \
  "https://harvest.greenhouse.io/v1/jobs?status=open&per_page=100" | jq '.[] | {id, name, status, departments: [.departments[].name]}'
```

### Recipe 2: Create a job (Greenhouse)
```bash
curl -s -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: <user_id>" \
  -H "Content-Type: application/json" \
  -X POST "https://harvest.greenhouse.io/v1/jobs" \
  -d '{
    "template_job_id": <template>,
    "number_of_openings": 1,
    "job_post_name": "Senior Operations Analyst",
    "department_id": <dept>,
    "office_ids": [<office>],
    "requisition_id": "OPS-2026-04"
  }'
```

### Recipe 3: Public job feed (Ashby + Lever + Greenhouse)
```bash
# Ashby — compensation on the public feed
curl -s "https://api.ashbyhq.com/posting-api/job-board/$ASHBY_SITE?includeCompensation=true" \
  | jq '.jobs[] | {title, locationName, compensation: .compensation.summary, applyUrl}'

# Lever — JSON public feed
curl -s "https://api.lever.co/v0/postings/$LEVER_SITE?mode=json" \
  | jq '.[] | {text, categories, hostedUrl}'

# Greenhouse — public board
curl -s "https://boards-api.greenhouse.io/v1/boards/$GREENHOUSE_BOARD_TOKEN/jobs?content=true"
```

### Recipe 4: Add candidate to pipeline (Greenhouse Harvest)
```bash
curl -s -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: <user_id>" \
  -H "Content-Type: application/json" \
  -X POST "https://harvest.greenhouse.io/v1/candidates" \
  -d '{
    "first_name":"Avery", "last_name":"Lee",
    "applications":[{"job_id":<job_id>}],
    "email_addresses":[{"value":"avery@example.com","type":"personal"}],
    "phone_numbers":[{"value":"+1-555-0143","type":"mobile"}]
  }'
```

### Recipe 5: Move candidate stage (Ashby)
```bash
curl -s -X POST "https://api.ashbyhq.com/application.changeStage" \
  -u "$ASHBY_API_KEY:" \
  -H "Content-Type: application/json" \
  -d '{"applicationId":"<id>","interviewStageId":"<stage>"}'
```

### Recipe 6: Submit interview scorecard (Greenhouse)
```bash
curl -s -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: <interviewer_id>" \
  -H "Content-Type: application/json" \
  -X PATCH "https://harvest.greenhouse.io/v1/applications/<app_id>/scorecards/<scorecard_id>" \
  -d '{
    "overall_recommendation":"yes",
    "attributes":[
      {"name":"Communication","rating":4},
      {"name":"Operational rigor","rating":5}
    ],
    "submitted_by_id":<interviewer_id>
  }'
```

### Recipe 7: Source attribution + time-in-stage (Ashby)
```bash
# Ashby has the deepest analytics — pull candidate source + days in stage
curl -s -X POST "https://api.ashbyhq.com/candidate.list" \
  -u "$ASHBY_API_KEY:" -H "Content-Type: application/json" \
  -d '{"limit":100}' \
  | jq '.results[] | {name, source: .sourceTitle, daysInStage: .currentStageDuration}'
```

### Recipe 8: Extend offer (Greenhouse)
```bash
curl -s -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: <user_id>" \
  -H "Content-Type: application/json" \
  -X POST "https://harvest.greenhouse.io/v1/applications/<app_id>/offers" \
  -d '{
    "starts_at":"2026-08-01",
    "sent_at":"2026-06-15",
    "custom_fields":{
      "base_salary":{"value":"185000","currency":"USD"},
      "equity_grant":"15000 ISOs",
      "signing_bonus":"$10000"
    }
  }'
```

### Recipe 9: Cross-ATS normalized via Unified.to
```bash
# When recipient runs more than one ATS (acquisitions / multi-region)
curl -s "https://api.unified.to/ats/<connection_id>/candidate?limit=100" \
  -H "Authorization: Bearer $UNIFIED_TOKEN" \
  | jq '.[] | {id, name, ats_id, raw_source}'
```

### Recipe 10: Lever — note + tag a candidate
```bash
curl -s -u "$LEVER_API_KEY:" \
  -X POST "https://api.lever.co/v1/opportunities/<opp_id>/notes?perform_as=<user_id>" \
  -H "Content-Type: application/json" \
  -d '{"value":"Strong ops generalist; resilient under ambiguity. Recommend onsite."}'

curl -s -u "$LEVER_API_KEY:" \
  -X POST "https://api.lever.co/v1/opportunities/<opp_id>/addTags?perform_as=<user_id>" \
  -H "Content-Type: application/json" \
  -d '{"tags":["fast-track","ops-2026-h2"]}'
```

### Recipe 11: Pipeline velocity report (cross-ATS)
```python
# Python — pull all open jobs, count time-in-stage, surface stuck reqs
import requests, os, statistics
from collections import defaultdict

GH = (os.environ['GREENHOUSE_API_KEY'], '')
jobs = requests.get('https://harvest.greenhouse.io/v1/jobs?status=open', auth=GH).json()
stalled = []
for j in jobs:
    apps = requests.get(f"https://harvest.greenhouse.io/v1/jobs/{j['id']}/applications", auth=GH).json()
    by_stage = defaultdict(list)
    for a in apps:
        if a.get('current_stage'):
            by_stage[a['current_stage']['name']].append(a)
    for stage, items in by_stage.items():
        if len(items) > 5 and stage in ('Phone Screen','Onsite'):
            stalled.append({'job': j['name'], 'stage': stage, 'count': len(items)})
print(stalled)
```

## Examples

### Example 1: Open a new Senior Ops req end-to-end
**Goal:** Post req, mirror to public board, alert hiring manager Slack channel.
**Steps:**
1. Greenhouse: `POST /v1/jobs` with template, dept, office, requisition id (Recipe 2).
2. Greenhouse Job Board API: poll `/boards/$SLUG/jobs` until job appears.
3. `slack-mcp` post to `#hiring-ops`: "OPS-2026-04 open. Scorecard ready. Hiring manager: @maria."

**Result:** Public board updated, hiring manager + recruiter notified, candidate pipeline initialized.

### Example 2: Daily pipeline-velocity Slack digest
**Goal:** Each morning post stalled reqs + interviewers behind on scorecards.
**Steps:**
1. Cron via `cli-anything` or n8n.
2. Run Recipe 11 stalled-req scan + Greenhouse `/v1/scorecards` filter `pending=true age_days>3`.
3. `slack-mcp` post to `#hiring-ops` with table.

**Result:** Visibility on bottlenecks; recruiter chases interviewers same-day.

## Edge cases / gotchas

- **Greenhouse `On-Behalf-Of` is mandatory for writes.** Drop the header → 403. Always pass the `user_id` of the responsible recruiter/manager. Audit trail depends on it.
- **Rate limits.** Greenhouse Harvest = 50 req/10s; Ashby = 60 req/min by default; Lever = 10 req/s. For backfills, chunk + sleep; otherwise 429 → 30s backoff.
- **Ashby `includeCompensation=true`** only works if the job has compensation set in-app. Empty otherwise. Useful for SEO + diversity-pay compliance (CA SB1162, NY pay-transparency).
- **Greenhouse job-board content lag.** `boards-api` cache can be 2–5 min behind Harvest mutations. Don't gate flows on instant consistency.
- **Lever "perform_as" required for mutations.** Same model as Greenhouse `On-Behalf-Of`.
- **Scorecard schema is per-job-template.** Fetch `/scorecards/<id>` first to learn the attribute list before submitting (Recipe 6).
- **Candidate dedupe.** Greenhouse and Lever both dedupe by email; if you re-create same email you'll get the existing record back. Idempotent by design.
- **Background check trigger.** Not done in-ATS; trigger Checkr / GoodHire after offer accept (see `onboarding-offboarding-workflows`).
- **Offer letter ESign.** Greenhouse + DocuSign / Adobe Sign integrations exist but require Greenhouse Recruiting Pro tier; otherwise PDF via `pdf` skill.
- **Defer to `legal-counsel` for binding offer terms, equity grant language, non-competes, and state-specific clauses (e.g., MA non-compete law, CA Labor Code §2870 IP carve-outs).**

## Sources

- Unified.to — 15 ATS APIs 2026: https://unified.to/blog/15_ats_apis_to_integrate_with_in_2026_greenhouse_lever_workable
- Index — Greenhouse vs Lever vs Ashby 2026: https://www.index.dev/blog/greenhouse-vs-lever-vs-ashby-ats-comparison
- Cavuno — 6 ATS Public Job Posting APIs 2026: https://cavuno.com/blog/ats-platforms-public-job-posting-apis
- Greenhouse Harvest API: https://developers.greenhouse.io/harvest.html
- Greenhouse Job Board API: https://developers.greenhouse.io/job-board.html
- Ashby API: https://developers.ashbyhq.com/
- Lever API: https://hire.lever.co/developer/documentation
