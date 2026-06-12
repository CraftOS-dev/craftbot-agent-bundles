<!--
Sources: https://www.metaview.ai/resources/blog/recruiting-trends
         https://unified.to/blog/15_ats_apis_to_integrate_with_in_2026_greenhouse_lever_workable
         https://support.greenhouse.io/hc/en-us/articles/202709324
         https://developers.ashbyhq.com/reference/
         https://hire.lever.co/developer/documentation
         https://www.gem.com/blog/candidate-sourcing-software
24-hour reply SLA; 7-day stage-advance SLA; auto-rejection within 5 business days.
Companies hitting 24h reply rate convert 2-3x higher than 72+ hour.
Pull stale candidates from ATS; auto-touch via Gem campaign; auto-reject template.
-->
# Candidate Experience Hygiene — Response Time — SKILL

Enforce 24h reply SLA on candidate replies + 7-day SLA on stage advancement + auto-rejection within 5 business days for declines. Pull stale candidates from Greenhouse / Ashby / Lever, fire Gem auto-touch sequences, and use ATS native auto-rejection templates. Companies that hit 24h reply convert 2-3x higher than companies at 72+ hours.

## When to use

- User wants to **audit current SLA performance** ("are we replying within 24h?").
- User wants to **set up stale-candidate alerts** in the ATS (no movement >7 days).
- User wants to **wire auto-rejection templates** for decline-without-recruiter-touch flows.
- User wants to **fire a "we're still reviewing" Gem auto-touch** to candidates parked >5 days.
- User asks: "candidate ghosting", "stale pipeline", "SLA report", "response time", "auto-rejection", "candidate experience score", "drop-off rate".

Do not use for: full source-of-hire reporting (`source-of-hire-reporting`); per-source funnel diagnosis (`source-to-contact-metrics`); writing the offer letter (defer to `operations-agent`).

## Setup

```bash
# ATS keys
export GREENHOUSE_API_KEY="harvest_xxx"   # https://app.greenhouse.io/configure/dev_center/credentials
export ASHBY_API_KEY="xxx"                # https://app.ashbyhq.com/admin/api-keys
export LEVER_API_KEY="xxx"                # https://hire.lever.co/settings/integrations

# CRM (auto-touch fallback when ATS is silent)
export GEM_API_KEY="xxx"

# Slack alerts to recruiter-coordinator on SLA breach
export SLACK_BOT_TOKEN="xoxb-xxx"
export SLACK_RECRUITER_CHANNEL="C0XXX"

# Output targets
export NOTION_API_KEY="secret_xxx"        # weekly SLA scorecard
export GOOGLE_SHEET_ID="xxx"
```

Required ATS scope (Greenhouse): `applications.read`, `applications.update`, `users.read`. Ashby: `candidate:read`, `application:read`, `application:update`. Lever: `applications:read`, `applications:write`.

## Common recipes

### Recipe 1: SLA definition table (the canonical thresholds)

| Trigger event | SLA | Action on breach |
|---|---|---|
| Candidate replies to InMail / email | 24h | Slack alert to assigned recruiter |
| Candidate applies via career site | 48h | Auto-acknowledgment + stage move within 5d |
| Recruiter screen scheduled | 48h | Calendly invite within 24h of schedule confirm |
| Stage transition (any) | 7d | Stale alert; auto-touch via Gem |
| Decline decision made | 5 business days | Auto-rejection template fired |
| Final-round → offer | 7d | Hiring manager nudge + offer-letter handoff |
| Offer-extended → accepted | 7d | Recruiter follow-up + comp clarification |

### Recipe 2: Greenhouse — pull candidates parked >7 days

```bash
# All active applications stalled in current stage >7 days
curl -u "$GREENHOUSE_API_KEY:" \
  "https://harvest.greenhouse.io/v1/applications?status=active&per_page=500" \
  | jq '[.[] | select(.last_activity_at < (now - 604800 | strftime("%Y-%m-%dT%H:%M:%SZ"))) | {id, candidate_id, last_activity_at, current_stage: .current_stage.name, days_stale: (((now | tonumber) - (.last_activity_at | fromdateiso8601)) / 86400 | floor)}]'
```

Output: list of `{application_id, days_stale, current_stage}`. Pipe to Slack alert (Recipe 9).

### Recipe 3: Ashby — pull stale applications

```bash
curl -X POST "https://api.ashbyhq.com/application.list" \
  -u "$ASHBY_API_KEY:" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "Active",
    "limit": 500
  }' \
  | jq '[.results[] | select((now - (.updatedAt | fromdateiso8601)) > 604800) | {id, candidateId, currentInterviewStage, daysStale: (((now) - (.updatedAt | fromdateiso8601)) / 86400 | floor)}]'
```

### Recipe 4: Lever — pull stale opportunities

```bash
curl -u "$LEVER_API_KEY:" \
  "https://api.lever.co/v1/opportunities?stage_id=lead-new&updated_at_end=$(date -d '7 days ago' -u +%Y-%m-%dT%H:%M:%SZ)&limit=200" \
  | jq '[.data[] | {id, candidateId: .id, lastInteractionAt, daysStale: (((now) - (.lastInteractionAt | tonumber / 1000)) / 86400 | floor)}]'
```

Note: Lever timestamps are millisecond Unix epochs. Divide by 1000 before comparing.

### Recipe 5: Auto-rejection template (Greenhouse)

```bash
# Reject candidate with template; no recruiter touch needed
curl -X POST "https://harvest.greenhouse.io/v1/applications/{application_id}/reject" \
  -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: <user_id>" \
  -H "Content-Type: application/json" \
  -d '{
    "rejection_reason_id": 12345,
    "rejection_email": {
      "send_email_at": "now",
      "email_template_id": 67890
    },
    "notes": "Auto-rejected via SLA hygiene job"
  }'
```

`email_template_id` references a saved rejection template in Greenhouse (Configure → Email Templates). Required for compliant tone + brand consistency.

### Recipe 6: Auto-rejection (Ashby)

```bash
curl -X POST "https://api.ashbyhq.com/application.changeStage" \
  -u "$ASHBY_API_KEY:" \
  -d '{
    "applicationId": "{id}",
    "interviewStageId": "<archived-stage-id>",
    "archiveReasonId": "<reason-id>"
  }'

# Then send rejection email via template
curl -X POST "https://api.ashbyhq.com/applicationCorrespondence.sendEmail" \
  -u "$ASHBY_API_KEY:" \
  -d '{
    "applicationId": "{id}",
    "templateId": "<rejection-template-id>"
  }'
```

### Recipe 7: Auto-rejection (Lever)

```bash
curl -X POST "https://api.lever.co/v1/opportunities/{id}/archived" \
  -u "$LEVER_API_KEY:" \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "<archive-reason-id>",
    "requisitionId": "<req-id>"
  }'

# Send templated rejection note
curl -X POST "https://api.lever.co/v1/opportunities/{id}/notes" \
  -u "$LEVER_API_KEY:" \
  -d '{"value": "Auto-rejection sent via SLA hygiene job; reason: silver medalist — added to hot-list."}'
```

### Recipe 8: Gem "still reviewing" auto-touch (when ATS silent >5 days)

```bash
# Pull prospects with last_touch >5d AND no auto-touch fired in last 14d
curl "https://api.gem.com/v1/prospects?last_touch_lt=$(date -u -d '5 days ago' +%Y-%m-%dT%H:%M:%SZ)&tags=in-pipeline&-tags=auto-touch-fired-14d" \
  -H "Authorization: Bearer $GEM_API_KEY" \
  | jq '.results[] | .id' \
  | xargs -I {} curl -X POST "https://api.gem.com/v1/sequences/<still-reviewing-seq>/enroll" \
      -H "Authorization: Bearer $GEM_API_KEY" \
      -d '{"prospect_id":"{}","start_step":1}'
```

Template body (Gem sequence step 1):
```
Subject: Quick update on your application, {first}

Hi {first} — wanted to follow up on your application to {role}. We're still working through the early-stage review; should have a substantive update by {date_plus_7d}. Appreciate your patience. Best, {recruiter}
```

### Recipe 9: Slack SLA-breach alert (recruiter-coordinator channel)

```bash
# After Recipe 2/3/4 produces stale-list, post to Slack
STALE=$(curl -u "$GREENHOUSE_API_KEY:" "https://harvest.greenhouse.io/v1/applications?status=active&per_page=500" | jq '[.[] | select(.last_activity_at < (now - 604800 | strftime("%Y-%m-%dT%H:%M:%SZ")))] | length')

curl -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -d "channel=$SLACK_RECRUITER_CHANNEL&text=:warning: SLA breach — $STALE candidates stalled >7d. Run /sla-report for details."
```

### Recipe 10: Weekly SLA scorecard (Notion / Google Sheet)

```python
# Schema
scorecard = {
    "week_of": "2026-06-08",
    "applications_received": 142,
    "responded_within_24h": 128,    # pct = 90.1%
    "responded_within_48h": 138,    # pct = 97.2%
    "responded_3d_plus": 4,          # pct = 2.8%  -> SLA BREACH count
    "auto_rejections_within_5bd": 18,
    "auto_rejections_late": 2,       # SLA breach
    "stage_advances_within_7d": 95,
    "stage_stale_breaches": 7,       # 7-day SLA breaches
    "avg_time_to_first_reply_h": 16.4,
    "avg_time_in_stage_d": 4.8,
    "candidate_nps_proxy": 4.2  # from post-reject survey if running one
}
# Push to Google Sheet via gspread / sheets API
# Or Notion via /v1/pages
```

### Recipe 11: Candidate NPS pulse (optional, after rejection)

```bash
# 7 days after rejection, fire a 1-question survey via Gem or Typeform
curl -X POST "https://api.typeform.com/forms/<nps-form-id>/responses" \
  -H "Authorization: Bearer $TYPEFORM_KEY" \
  -d '{
    "fields": [{"id":"rating","value":"{score}"}],
    "respondent_email": "{candidate_email}",
    "metadata": {"source":"reject-7d-pulse","req_id":"{req_id}"}
  }'
```

Track score >= 7 as "promoter"; <= 6 as "detractor". Detractor responses route to recruiter-coordinator for personal touch (lifts brand sentiment + boomerang potential).

### Recipe 12: Daily cron — SLA hygiene job (the end-to-end)

```bash
#!/bin/bash
# Run daily 08:00 local time

# 1. Pull stale list (Recipe 2)
STALE=$(./pull_stale_greenhouse.sh)

# 2. For each stale: auto-touch via Gem (Recipe 8) if not in interview stage
#    OR auto-reject (Recipe 5) if in "Decision Pending — Decline" sub-stage
echo "$STALE" | jq -r '.[] | "\(.id)\t\(.current_stage)"' | while IFS=$'\t' read id stage; do
  case "$stage" in
    "Application Review"|"Recruiter Screen"|"Hiring Manager Review")
      ./gem_auto_touch.sh "$id"
      ;;
    "Decline Pending"|"Silver Medalist")
      ./greenhouse_auto_reject.sh "$id"
      ;;
    *)
      ./slack_alert.sh "$id" "$stage"
      ;;
  esac
done

# 3. Post weekly scorecard on Mondays
[ "$(date +%u)" = "1" ] && ./post_scorecard.sh
```

## Examples

### Example 1: Audit a struggling team — 30% reply rate, 8d avg time-to-first-touch
**Goal:** Recruiter team has 8d average time-to-first-reply (benchmark: 24h). Diagnose + fix.
**Steps:**
1. Run Recipe 2 on Greenhouse — count applications stale >24h with no recruiter activity → 47 candidates.
2. Bucket by req_id; identify 3 reqs with >10 stale candidates each → these are the bottleneck reqs.
3. For those 3 reqs, check stage breakdown — likely 90% stuck in "Application Review" with no assignment.
4. Run Recipe 8 to fire "still reviewing" Gem auto-touch on all 47 — stops candidate-side ghosting.
5. Slack the 3 bottleneck recruiters (Recipe 9) — assign + commit to clear backlog in 48h.
6. Set up cron (Recipe 12) so it never gets there again.

**Result:** 47-candidate backlog cleared in 72h; avg time-to-first-reply drops to <36h within 2 weeks; reply→screen conversion lifts ~25% from preserved goodwill.

### Example 2: Wire auto-rejection for declines (zero recruiter touch)
**Goal:** Hiring manager declines 80 candidates/month after review; recruiters don't have bandwidth to manually reject + email each one.
**Steps:**
1. Create rejection template in Greenhouse: Configure → Email Templates → "Standard decline, with-thank-you, with-future-opt-in".
2. Create rejection reason: "Did not advance past application review".
3. Create Greenhouse webhook on `application.rejected` → POST to Slack so recruiter sees what was auto-fired.
4. Wire daily job that pulls applications in "Decline Pending" stage and runs Recipe 5 with the template ID.
5. Add candidates to `silver-medalist` hot-list if `nice-to-revisit` checkbox set.

**Result:** 80/month auto-rejected within 5 business days; recruiters reclaim ~5h/week; candidate experience score (post-reject NPS) stays >7 from professional tone + future-opt-in.

### Example 3: 7-day stage-advance breach — silent pipeline cleanup
**Goal:** 23 candidates stuck >14 days in "Recruiter Screen Scheduled" stage with no follow-through.
**Steps:**
1. Run Recipe 2 with filter `current_stage = "Recruiter Screen Scheduled" AND last_activity_at < 14d ago`.
2. Output 23 candidates → bucket by recruiter via `recruiter_id`.
3. For each recruiter: post Slack DM with assigned-stale list + 48h deadline.
4. If no movement in 48h: escalate to hiring manager DM (Recipe 9 with different channel).
5. Track recurrence weekly; if a recruiter has >5 stale per week, surface in 1:1 with TA leader.

**Result:** Stale stage breaches drop from 23 to <5 within 3 weeks; candidate drop-off rate (closed_lost from candidate side) drops ~30%.

## Edge cases / gotchas

- **24h SLA on weekends?** Soft yes for replies; hard no for outbound stage moves. Pause cron Sat-Sun; resume Monday 08:00 local. Don't burn weekend goodwill.
- **Auto-rejection without recruiter eyes is risky.** Always wire a "Decline Pending" stage that requires recruiter or HM to set. Direct rejection without review = lawsuit risk + brand damage. Recipe 5 only fires once HM has approved.
- **Rejection template language must be reviewed by legal.** "Not a fit" + "We'll keep your résumé on file" boilerplate has EEOC implications. Cite the role's must-have not met where defensible.
- **Greenhouse webhook payloads omit candidate email by default.** Pull candidate object separately if you need to mirror the rejection event to CRM.
- **Ashby rate limit: 100 req/min.** Recipe 6 hitting 200 candidates in a batch will throttle. Use `application.list` once + iterate locally.
- **Lever's `archived` field is permanent.** No un-archive endpoint. Confirm decision before firing Recipe 7.
- **Gem auto-touch can race the recruiter.** If recruiter sends manual touch within 24h of Gem auto-touch, candidate gets two emails 5 minutes apart. Add a `last_touch_lt=24h` exclusion to Gem query.
- **Slack alert noise.** If you Slack every breach, recruiters mute the channel. Batch into daily 09:00 summary or set threshold (>5 breaches triggers alert; 1-5 = silent track).
- **Some candidates self-withdraw mid-pipeline.** Distinguish `closed_lost: withdrawn` from `closed_lost: rejected`. Withdrawn candidates are warm hot-list material; rejected are silver-medalist track at most.
- **Auto-rejection of internal applicants is HR landmine.** Filter Recipe 5 to `application.source != "Internal Transfer"`. Internal declines always need a manager + HRBP human conversation.
- **EEO data deletion lag.** Greenhouse retains rejected-candidate EEO data per US-EEOC; Ashby and Lever have configurable retention. Confirm retention before mass-rejecting.
- **Candidate NPS surveys may bias positive** because detractors don't respond. Treat <20% response rate as "no signal" and don't make decisions on it.
- **A "we're still reviewing" auto-touch can frustrate candidates if it repeats.** Cap at 2 sends per candidate. After the second, the candidate either gets a stage move or a rejection — no third "still reviewing" allowed.
- **24h SLA on a Friday afternoon application** = Monday morning reply, which is technically >24h. Track business-hour SLA, not wall-clock SLA, to avoid false breaches.
- **Hand off to `boomerang-alumni-re-engagement`** for the silver-medalist → 12-mo-later re-engage cadence. Auto-rejection adds the tag; that skill drives the follow-up.

## Sources

- Metaview — Recruiting Trends 2026 (24h SLA + 2-3x conversion lift): https://www.metaview.ai/resources/blog/recruiting-trends
- Unified.to — 15 ATS APIs for 2026 (Greenhouse / Ashby / Lever): https://unified.to/blog/15_ats_apis_to_integrate_with_in_2026_greenhouse_lever_workable
- Greenhouse Harvest API — Applications endpoint: https://developers.greenhouse.io/harvest.html#applications
- Greenhouse — Reject Application: https://developers.greenhouse.io/harvest.html#reject-application
- Ashby API reference (application.list, changeStage, sendEmail): https://developers.ashbyhq.com/reference/
- Lever API — Opportunities + Archived: https://hire.lever.co/developer/documentation
- Gem — Best Candidate Sourcing Software 2026: https://www.gem.com/blog/candidate-sourcing-software
- Outsail — Greenhouse vs Lever vs Ashby (auto-rejection feature parity): https://www.outsail.co/post/greenhouse-vs-lever-vs-ashby
