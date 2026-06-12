<!--
Sources: https://www.greenhouse.io/blog/recruiting-funnel-metrics
         https://www.metaview.ai/resources/blog/recruiting-metrics
         https://www.lever.co/blog/recruiting-metrics-funnel
         https://www.paradox.ai/olivia
2026 funnel benchmarks: 30-50% sourced→applied, 50-70% applied→screen, 40-60%
screen→onsite, 30-50% onsite→offer, 70-90% offer-accept. Per-stage age limits
drive recruiter's daily hygiene loop.
-->
# Candidate Pipeline — Applied → Hired — SKILL

The recruiter's daily heartbeat: poll the ATS for stalled candidates, run hiring-manager intake, enforce per-stage age limits, fast-track boomerangs, and hand off to the next stage owner. Covers the **post-Applied** scope (handoff from `talent-sourcer` on application receipt) through **Hired** (handoff to `operations-agent` for onboarding).

## When to use

- User asks for **pipeline status**, **stalled candidates**, **per-req funnel report**, **stage age check**, **intake meeting**, **boomerang fast-track**, **weekly recruiting sync**.
- Daily hygiene: archive 30-day-no-response, advance ready candidates, escalate breaches.
- Trigger phrases: "who's stuck", "pipeline report", "stalled candidates", "intake with HM", "fast-track this alum", "bulk archive cold candidates", "pipeline velocity".
- Hand off top-of-funnel sourcing back to `talent-sourcer`; hand off Day-1 readiness to `operations-agent`.

## Setup

```bash
# Greenhouse Harvest API
export GREENHOUSE_API_KEY="harvest_xxx"
export GH_USER_ID="123456"

# Ashby
export ASHBY_API_KEY="xxx"

# Lever
export LEVER_API_KEY="xxx"

# Paradox Olivia (high-volume RPO)
export PARADOX_API_KEY="xxx"                 # https://www.paradox.ai/olivia
```

Per-stage age targets (2026 benchmarks):

| Stage | Target age | Hard limit | Action at hard limit |
|---|---|---|---|
| Applied | ≤3 days | 7 days | Auto-screen or archive |
| Recruiter screen | ≤7 days | 14 days | Escalate to HM or decline |
| HM screen | ≤7 days | 14 days | Escalate to recruiter or decline |
| Onsite | ≤14 days | 21 days | Escalate to hiring leader |
| Offer extended | ≤7 days | 10 days | Counter-offer scenario; escalate |

## Common recipes

### Recipe 1: Pull active candidates per req with stage age (Greenhouse)
```bash
JOB_ID=<id>
curl -s -u "$GREENHOUSE_API_KEY:" \
  "https://harvest.greenhouse.io/v1/jobs/$JOB_ID/applications?status=active&per_page=100" \
  | jq '.[] | {id, candidate_id, stage: .current_stage.name, last_activity_at}'
```

### Recipe 2: Compute stage age locally + flag stalled
```python
import requests, os, datetime as dt
GH = (os.environ['GREENHOUSE_API_KEY'], '')
JOB_ID = '<id>'
apps = requests.get(
    f'https://harvest.greenhouse.io/v1/jobs/{JOB_ID}/applications?status=active&per_page=100',
    auth=GH
).json()
now = dt.datetime.now(dt.timezone.utc)
LIMITS = {'Applied': 7, 'Recruiter Screen': 14, 'HM Screen': 14, 'Onsite': 21, 'Offer': 10}
stalled = []
for a in apps:
    stage = (a.get('current_stage') or {}).get('name')
    age = (now - dt.datetime.fromisoformat(a['last_activity_at'].replace('Z', '+00:00'))).days
    if stage in LIMITS and age > LIMITS[stage]:
        stalled.append({'id': a['id'], 'stage': stage, 'age_days': age})
print(stalled)
```

### Recipe 3: Move stage in Greenhouse
```bash
curl -s -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -X PATCH "https://harvest.greenhouse.io/v1/applications/<app_id>" \
  -H "Content-Type: application/json" \
  -d '{"job_stage_id": <next_stage_id>}'
```

### Recipe 4: Sync-token-driven pipeline poll (Ashby)
```bash
# First pull
curl -s -X POST "https://api.ashbyhq.com/candidate.list" \
  -u "$ASHBY_API_KEY:" -H "Content-Type: application/json" \
  -d '{"limit":100}'

# Subsequent pulls — pass syncToken to get only changes since last call
curl -s -X POST "https://api.ashbyhq.com/candidate.list" \
  -u "$ASHBY_API_KEY:" -H "Content-Type: application/json" \
  -d '{"limit":100,"syncToken":"<token_from_previous_response>"}'
```

### Recipe 5: Lever opportunity filter by stage
```bash
curl -s -u "$LEVER_API_KEY:" \
  "https://api.lever.co/v1/opportunities?stage_id=<stage_id>&limit=100" \
  | jq '.data[] | {id, name, stage, lastInteractionAt}'
```

### Recipe 6: Boomerang fast-track detection (Greenhouse)
```bash
EMAIL="alum@example.com"
# Pull historical applications for this email
curl -s -u "$GREENHOUSE_API_KEY:" \
  "https://harvest.greenhouse.io/v1/candidates?email=$EMAIL" \
  | jq '.[] | {id, prior_jobs: [.applications[].job_id], status, last_activity_at}'

# If any prior application status was "hired" → boomerang fast-track tag
curl -s -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -X PUT "https://harvest.greenhouse.io/v1/candidates/<candidate_id>/tags/BOOMERANG-FAST-TRACK"
```

### Recipe 7: Hiring-manager intake template (Notion)
```bash
# Push intake template to Notion as a page under the req database
notion-cli pages create \
  --parent-database-id "$RECRUITING_DB_ID" \
  --title "Senior Backend Engineer — Intake" \
  --template "intake-template-v3"
# Template body: outcome scorecard, ICP, comp band, panel composition, timeline,
# DEI goals, market context, sign-off (HM + recruiter + hiring leader)
```
Then PATCH the Greenhouse job to add the Notion URL as an attachment / custom field for interviewer access.

### Recipe 8: Bulk archive 30-day-no-response
```python
import requests, os, datetime as dt
GH = (os.environ['GREENHOUSE_API_KEY'], '')
USER = os.environ['GH_USER_ID']
cutoff = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=30)).isoformat()
apps = requests.get(
    f'https://harvest.greenhouse.io/v1/applications?status=active&updated_before={cutoff}',
    auth=GH
).json()
for a in apps:
    if (a.get('current_stage') or {}).get('name') == 'Applied':
        requests.post(
            f"https://harvest.greenhouse.io/v1/applications/{a['id']}/reject",
            auth=GH,
            headers={'On-Behalf-Of': USER, 'Content-Type': 'application/json'},
            json={
                'rejection_reason_id': <COLD_NO_RESPONSE_REASON_ID>,
                'rejection_email': {'send_email_at': 'now', 'email_template_id': <STALE_TEMPLATE_ID>}
            }
        )
```

### Recipe 9: Paradox Olivia AI top-of-funnel screen (high volume)
```bash
# Trigger Olivia chat screen for a candidate (high-volume retail / call-center / scaling engineering)
curl -s -X POST "https://api.paradox.ai/v1/candidates/<id>/screens" \
  -H "Authorization: Bearer $PARADOX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "screen_template_id":"<template_id>",
    "channel":"sms",
    "questions":[
      {"id":"q1","text":"Are you authorized to work in the US?","type":"yesno"},
      {"id":"q2","text":"What is your earliest available start date?","type":"date"}
    ]
  }'
```

### Recipe 10: Per-channel funnel attribution
```python
# Join Greenhouse source attribution to outcome
import requests, os
from collections import defaultdict
GH = (os.environ['GREENHOUSE_API_KEY'], '')
apps = requests.get('https://harvest.greenhouse.io/v1/applications?per_page=500', auth=GH).json()
funnel = defaultdict(lambda: {'applied': 0, 'hired': 0})
for a in apps:
    src = (a.get('source') or {}).get('public_name', 'unknown')
    funnel[src]['applied'] += 1
    if a.get('status') == 'hired':
        funnel[src]['hired'] += 1
for src, v in funnel.items():
    rate = v['hired'] / v['applied'] if v['applied'] else 0
    print(f"{src}: {v['applied']} applied → {v['hired']} hired ({rate:.1%})")
```

### Recipe 11: Weekly recruiting sync digest
```bash
# Cron — every Monday 8am post per-req status to Slack
python pipeline_digest.py | curl -s -X POST -H "Content-Type: application/json" \
  --data @- "$SLACK_WEBHOOK_URL"
# Body lists: open reqs, stage breakdown, stalled candidates, weekly conversion, blockers.
```

## Examples

### Example 1: Monday morning pipeline hygiene loop
**Goal:** Surface every stalled candidate, fast-track boomerangs, archive cold no-response, post status to `#hiring-sync`.
**Steps:**
1. Run Recipe 2 across all open reqs → list of (app_id, stage, age_days).
2. For each stalled: draft personalized touch via `gmail-mcp` (recruiter screen pending) or escalate to HM Slack DM (HM screen pending).
3. Run Recipe 6 for any new application with prior `hired` status → tag `BOOMERANG-FAST-TRACK` + skip to skip-level interview.
4. Run Recipe 8 to bulk-archive 30-day-no-response (use the post-application decline template from `candidate-experience-sla-status-updates`).
5. Post weekly digest to Slack (Recipe 11).

**Result:** Pipeline freshness restored; candidate-experience SLA preserved; HM visibility on bottlenecks before the standup.

### Example 2: Hiring-manager intake for a new req
**Goal:** Capture outcomes scorecard + ICP + comp band + panel + DEI goals in 30 min.
**Steps:**
1. Push Notion intake template to req database (Recipe 7).
2. 30-min Zoom with HM; recruiter fills template live.
3. Sign-off in Notion → PDF export.
4. Attach PDF to Greenhouse job via `POST /v1/jobs/<id>/attachments`.
5. Notify panel interviewers in Slack with link to intake doc.

**Result:** Calibrated kickoff; interviewers see exactly what we're hiring for; no ambiguity on level / scope / comp band.

## Edge cases / gotchas

- **`last_activity_at` is the wrong field for stage age** when stage was changed but activity didn't update. Use `current_stage_changed_at` (Ashby) or compute age from the `activity_feed` stage-change event in Greenhouse.
- **Greenhouse `On-Behalf-Of`** is mandatory for any state mutation (move stage, reject, attach). 403 if missing.
- **Ashby `syncToken` rotation.** Tokens expire after 24h of non-use; if 410 Gone, do full pull again.
- **Lever pagination.** Use `?next=<cursor>` not page numbers; `has_next` indicates more pages.
- **Paradox Olivia rate limits.** 100 conversations/hour on the standard tier; queue with backpressure if higher volume.
- **Boomerang detection by email only is brittle.** Personal email often differs from company email at prior role. Cross-check by first+last name + prior employer in LinkedIn data (via `talent-sourcer`).
- **Bulk archive of "Applied" stage with no recent activity** must use the right rejection reason (`Cold — no response` not `Not qualified`) to avoid skewing rejection-reason analytics.
- **Stage-name drift.** Different ATSes name stages differently; normalize via a stage-equivalence map in code, never hard-code strings.
- **Defer to `legal-counsel`** for: rejection-reason wording that suggests protected-class basis, EEO impact of bulk archive policy, time-to-decision SLA compliance with NY Local Law 4 / similar.

## Sources

- [Greenhouse — Recruiting Funnel Metrics](https://www.greenhouse.io/blog/recruiting-funnel-metrics)
- [Metaview — Recruiting Metrics That Matter](https://www.metaview.ai/resources/blog/recruiting-metrics)
- [Lever — Recruiting Metrics Funnel](https://www.lever.co/blog/recruiting-metrics-funnel)
- [Greenhouse Harvest API](https://developers.greenhouse.io/harvest.html)
- [Ashby Developer Docs](https://developers.ashbyhq.com/reference)
- [Paradox Olivia](https://www.paradox.ai/olivia)
- [Greenhouse — Hiring Manager Intake Meeting](https://www.greenhouse.io/blog/hiring-manager-intake-meeting)
