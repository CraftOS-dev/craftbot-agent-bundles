<!--
Sources: https://goodtime.io/product/scheduling
         https://help.goodtime.io/en/articles/api-documentation
         https://www.ashbyhq.com/scheduling
         https://developer.calendly.com/api-docs
         https://cal.com/docs/api-reference
Goodtime = 2026 SOTA for ≥4-person panels + multi-day windows + DEI composition.
Ashby Scheduling = native, zero-config for Ashby ATS. Calendly / Cal.com = ≤2 person.
-->
# Interview Panel Scheduling — Goodtime / Ashby / Calendly / Cal.com — SKILL

The multi-person, multi-day interview-panel coordination layer. Pick the right tool for the panel size + complexity; load-balance interviewers; enforce DEI composition; survive cancellations.

## When to use

- User needs **a 4+ person onsite scheduled** in a multi-day window.
- 1:1 **recruiter screen** or **HM screen** scheduling.
- **Reschedule cascade** after interviewer cancels.
- **Panel composition rule** (≥1 non-direct-report; ≥1 underrepresented interviewer).
- Trigger phrases: "schedule the onsite", "panel for next week", "interviewer can't make it", "Goodtime for this loop", "Calendly screen", "balance interviewer load".

## Setup

```bash
# Goodtime
export GOODTIME_API_KEY="xxx"                # https://help.goodtime.io/en/articles/api-documentation

# Ashby Scheduling (native — uses Ashby API key)
export ASHBY_API_KEY="xxx"

# Calendly
export CALENDLY_TOKEN="xxx"                  # https://developer.calendly.com/

# Cal.com (OSS Calendly alt)
export CAL_API_KEY="xxx"                     # https://cal.com/docs/api-reference
export CAL_USERNAME="company"
```

Decision rule:

| Panel size + complexity | Tool | Why |
|---|---|---|
| 1-2 interviewer, 1 day | Calendly / Cal.com | Free tier covers it |
| 3 interviewer, 1-2 days | Calendly Round Robin / Ashby native | Mid |
| 4+ interviewer, multi-day | **Goodtime** | Load balance + DEI rules + auto-reschedule |
| Ashby ATS shop, any size | **Ashby Scheduling** | Zero-config, ATS-native |

## Common recipes

### Recipe 1: Goodtime — schedule a panel
```bash
curl -s -X POST "https://api.goodtime.io/v1/interviews/schedule" \
  -H "X-API-Key: $GOODTIME_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id":"<candidate_id>",
    "interview_template_id":"<template_id>",
    "candidate_availability_window":["2026-06-17","2026-06-24"],
    "constraints":{
      "max_interviews_per_interviewer_per_week":5,
      "min_buffer_minutes":15,
      "require_diversity":true,
      "no_back_to_back_for_interviewer":true,
      "preferred_time_zone":"America/Los_Angeles"
    }
  }'
```

### Recipe 2: Goodtime — pull interviewer availability
```bash
curl -s -H "X-API-Key: $GOODTIME_API_KEY" \
  "https://api.goodtime.io/v1/interviewers/availability?start=2026-06-17&end=2026-06-24"
```

### Recipe 3: Ashby native scheduling
```bash
# Create interview event with auto-scheduling
curl -s -X POST "https://api.ashbyhq.com/interview.schedule" \
  -u "$ASHBY_API_KEY:" \
  -H "Content-Type: application/json" \
  -d '{
    "applicationId":"<app_id>",
    "interviewPlanId":"<plan_id>",
    "stageId":"<stage_id>",
    "candidateAvailability":[
      {"start":"2026-06-17T16:00:00Z","end":"2026-06-17T20:00:00Z"},
      {"start":"2026-06-18T16:00:00Z","end":"2026-06-18T22:00:00Z"}
    ],
    "useScheduler":true
  }'
```

### Recipe 4: Calendly — generate single-use scheduling link
```bash
curl -s -X POST "https://api.calendly.com/scheduling_links" \
  -H "Authorization: Bearer $CALENDLY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "max_event_count":1,
    "owner":"https://api.calendly.com/event_types/<event_type_uuid>",
    "owner_type":"EventType"
  }'
```

### Recipe 5: Cal.com — generate booking link
```bash
curl -s "https://api.cal.com/v2/bookings?apiKey=$CAL_API_KEY" \
  -X POST -H "Content-Type: application/json" \
  -d '{
    "eventTypeId":<id>,
    "start":"2026-06-17T16:00:00Z",
    "responses":{"name":"<candidate>","email":"<email>"},
    "timeZone":"America/Los_Angeles"
  }'
```

### Recipe 6: Reschedule cascade (interviewer drops out)
```python
# When interviewer cancels: Goodtime auto-suggests replacement matching constraints
import requests, os
GT = os.environ['GOODTIME_API_KEY']
r = requests.post(
    'https://api.goodtime.io/v1/interviews/reschedule',
    headers={'X-API-Key': GT, 'Content-Type': 'application/json'},
    json={
        'interview_id': '<interview_id>',
        'cancelled_interviewer_id': '<user_id>',
        'find_replacement': True,
        'replacement_constraints': {
            'same_competency': True,
            'require_diversity': True,
            'within_org_team': True
        }
    }
)
print(r.json())
```

### Recipe 7: Goodtime — interviewer load balancing report
```bash
# Pull per-interviewer load over rolling 4 weeks
curl -s -H "X-API-Key: $GOODTIME_API_KEY" \
  "https://api.goodtime.io/v1/interviewers/load?period=4w" \
  | jq '.interviewers[] | select(.weekly_average > 4)'
# Flag anyone >4/week → likely interviewer fatigue → rotate
```

### Recipe 8: Panel diversity composition check
```python
# Before confirming: verify panel includes ≥1 underrepresented + ≥1 non-direct-report
import os, requests
GT = os.environ['GOODTIME_API_KEY']
panel = requests.get(
    f'https://api.goodtime.io/v1/interviews/<interview_id>/panel',
    headers={'X-API-Key': GT}
).json()
underrep = sum(1 for p in panel['interviewers'] if p.get('demographic_self_id_underrep'))
non_direct = sum(1 for p in panel['interviewers'] if not p.get('is_direct_report_of_hm'))
if underrep < 1:
    print("⚠ Panel lacks underrepresented interviewer; flag for staffing review")
if non_direct < 1:
    print("⚠ Panel lacks non-direct-report perspective")
```

### Recipe 9: Calendar holds via google-calendar-mcp
```bash
# Hold interviewer slots before sending candidate Calendly link to avoid double-book
gcalcli add \
  --calendar "interviewer@company.com" \
  --title "INTERVIEW HOLD — Senior Backend candidate" \
  --when "2026-06-17 10:00" \
  --duration 90 \
  --description "Tentative — release if no booking by EOD 2026-06-16"
```

### Recipe 10: Confirmation comms (Slack + email)
```bash
# After schedule confirmed, notify all interviewers in Slack
curl -s -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer $SLACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel":"#hiring-backend",
    "text":"📅 Onsite scheduled: <candidate>, 2026-06-18 10am-3pm PT. Kit: <notion_url>. Zoom: <link>."
  }'
```

## Examples

### Example 1: 5-person onsite for Senior Backend with diversity rule
**Goal:** Multi-day window (Tue-Fri), 5 interviewers including ≥1 underrep + ≥1 skip-level, 15-min buffers, candidate timezone PT.
**Steps:**
1. Goodtime POST `/v1/interviews/schedule` with panel pool of 8 interviewers + constraints (Recipe 1).
2. Goodtime returns proposed schedule; validate diversity (Recipe 8).
3. Calendar holds for interviewer slots (Recipe 9).
4. Candidate gets single confirmation email with full agenda + interviewer bios + Zoom links.
5. Slack notification to `#hiring-backend` (Recipe 10).

**Result:** Onsite confirmed in 24h vs typical 3-day back-and-forth; load-balanced; diverse panel.

### Example 2: Interviewer cancels day-of; cascade reschedule
**Goal:** Interviewer 3 of 5 cancels at 9am; onsite at 1pm; need replacement.
**Steps:**
1. Goodtime POST `/v1/interviews/reschedule` with `find_replacement: true` + `same_competency: true` (Recipe 6).
2. Goodtime suggests replacement matching competency + diversity rule.
3. Confirm replacement via Slack DM ("can you cover system design at 1:30?").
4. Update candidate via personal message ("Quick swap: Maya will be your system design interviewer instead of Alex").
5. Slack `#hiring-backend` post + Greenhouse activity log entry.

**Result:** Onsite stays on rails; candidate sees professionalism; interviewer-load impact tracked.

## Edge cases / gotchas

- **Goodtime constraint conflicts** (e.g., require diversity + small team) return empty schedule. Goodtime UI shows the conflict; relax one constraint or staff-up the panel pool.
- **Calendly Round Robin doesn't guarantee panel uniqueness.** Two candidates booking the same Tuesday slot get different interviewers — but the same interviewer can hit cap of 5/week silently. Goodtime explicitly tracks; Calendly doesn't.
- **Time-zone arithmetic.** Always store interviews in UTC, render in candidate's local tz in their email; render in interviewer's local tz in their calendar. Mixing breaks no-show analysis.
- **Zoom personal room vs scheduled meeting.** Personal rooms get hijacked; always use **scheduled meeting** with waiting room enabled.
- **15-min buffers are non-negotiable.** Back-to-back interviews = poor interviewer prep + scorecard quality dip.
- **5/week max per interviewer.** Beyond 5/week, scorecard quality drops + interviewer turnover risk rises. Goodtime enforces.
- **Ashby Scheduling lock-in.** Native scheduling only works for Ashby-hosted interviews; can't easily migrate to Goodtime mid-quarter.
- **Calendly + Cal.com don't enforce diversity.** Goodtime is the only major scheduler with the rule built-in. For non-Goodtime shops, manual check pre-confirm.
- **Holiday + PTO awareness.** Goodtime + Ashby integrate with Google / Outlook + can read PTO from BambooHR / Workday. Calendly doesn't — manual exclusion required.
- **Webhook reliability.** Goodtime fires `interview.scheduled` + `interview.rescheduled` + `interview.cancelled`; idempotent handler required (delivery retries up to 24h).
- **Defer to `legal-counsel`** for: candidate-data retention in scheduling tools (GDPR, CPRA), diversity-tracking data classification + consent.

## Sources

- [Goodtime — Interview Scheduling](https://goodtime.io/product/scheduling)
- [Goodtime API Documentation](https://help.goodtime.io/en/articles/api-documentation)
- [Ashby Scheduling](https://www.ashbyhq.com/scheduling)
- [Calendly API Documentation](https://developer.calendly.com/api-docs)
- [Cal.com API Reference](https://cal.com/docs/api-reference)
- [Zoom API](https://developers.zoom.us/docs/api/)
- [Google Calendar API](https://developers.google.com/calendar/api/v3/reference)
