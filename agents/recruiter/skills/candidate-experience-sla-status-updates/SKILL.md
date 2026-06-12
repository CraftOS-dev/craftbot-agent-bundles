<!--
Sources: https://www.thetalentboard.org/cande-research-reports/
         https://www.greenhouse.io/blog/candidate-experience
         https://developers.greenhouse.io/harvest.html
         https://developers.ashbyhq.com/reference
SLA matrix (canonical):
  Apply ack <24h, Initial screen <72h post-apply, Post-screen decision <5 biz days,
  Post-onsite decision <5 biz days, Bulk archive at 30 days no-response.
Decline template library lives in role.md "Decline template library".
-->
# Candidate Experience — SLA + Status Updates + Decline Templates — SKILL

Run the recruiter's candidate-experience layer: detect stage-age SLA breaches, fire structured status updates, send stage-appropriate decline emails, and bulk-archive non-responders. Includes the 30-day non-response cleanup and the post-decision NPS survey.

## When to use

- Daily: detect candidates whose stage age has crossed the SLA threshold (apply >24h without ack; screen >72h without scheduling; onsite >5 biz days without decision).
- Per-stage: send the appropriate structured rejection email (apply / post-screen / post-onsite / post-offer counter-offer).
- 30 days no-response: bulk-archive + re-engage tag.
- Post-decision: trigger Talent Board CandE-style NPS survey.
- Trigger phrases: "candidate hasn't heard back", "stalled candidate", "decline this person", "rejection template", "candidate experience survey", "bulk archive".

## Setup

```bash
# ATS
export GREENHOUSE_API_KEY="harvest_xxx"
export GH_USER_ID="123456"
export ASHBY_API_KEY="xxx"
export LEVER_API_KEY="xxx"; export LEVER_USER_ID="xxx"

# Email / sequence sender (when ATS native templates not in use)
export GMAIL_OAUTH_TOKEN="<bearer>"   # gmail-mcp also exposes this
export GEM_API_KEY="xxx"              # optional, for sequence campaigns

# Survey
export TYPEFORM_TOKEN="tfp_xxx"       # for CandE-style post-decision survey
```

Reference: full decline template library lives in `role.md` under "Decline template library". Pull from there; don't inline copies.

## Common recipes

### Recipe 1: List candidates whose stage age has exceeded SLA (Greenhouse)
```bash
# Open candidates with current stage entered >5 biz days ago
NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
CUTOFF=$(date -u -d "5 days ago" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u -v -5d +"%Y-%m-%dT%H:%M:%SZ")

curl -s -u "$GREENHOUSE_API_KEY:" \
  "https://harvest.greenhouse.io/v1/candidates?status=active&updated_before=$CUTOFF" \
  | jq '.[] | {id, name: (.first_name + " " + .last_name), last_stage_change: .last_activity, job_ids: [.applications[].job_id]}'
```
For per-stage age, fetch `/v1/applications/<id>/activity_feed` and find the most recent `Moved` event; compute delta locally.

### Recipe 2: List stalled applications (Ashby)
```bash
curl -s -X POST -u "$ASHBY_API_KEY:" \
  -H "Content-Type: application/json" \
  "https://api.ashbyhq.com/application.list" \
  -d '{"status": "ACTIVE", "stageUpdatedAfter": "2026-06-01T00:00:00Z"}' \
  | jq '.results[] | select(.currentInterviewStage.daysInStage > 5) | {id: .id, stage: .currentInterviewStage.title, days: .currentInterviewStage.daysInStage}'
```

### Recipe 3: Send rejection with template (Greenhouse)
```bash
curl -s -X POST -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -H "Content-Type: application/json" \
  "https://harvest.greenhouse.io/v1/applications/<app_id>/reject" \
  -d '{
    "rejection_reason": {"id": <reason_id>},
    "rejection_email": {
      "email_template_id": <template_id>,
      "send_email_at": "now"
    }
  }'
```
Templates managed in Greenhouse UI under Configure → Email Templates. Use per-stage variants — see `role.md` "Decline template library".

### Recipe 4: Archive with reason + email (Ashby)
```bash
curl -s -X POST -u "$ASHBY_API_KEY:" \
  -H "Content-Type: application/json" \
  "https://api.ashbyhq.com/application.archive" \
  -d '{
    "applicationId": "<app_id>",
    "archiveReasonId": "<reason_id>",
    "sendNotificationToCandidate": true,
    "emailTemplateId": "<template_id>"
  }'
```

### Recipe 5: Archive opportunity (Lever)
```bash
curl -s -X POST -u "$LEVER_API_KEY:" \
  -H "Content-Type: application/json" \
  "https://api.lever.co/v1/opportunities/<opp_id>/archived?perform_as=$LEVER_USER_ID" \
  -d '{
    "reason": "<archive_reason_id>",
    "cleanInterviews": true
  }'
```

### Recipe 6: Bulk archive 30-day no-response (Greenhouse)
```bash
# 1) List candidates last active >30 days ago in any open stage
CUT=$(date -u -d "30 days ago" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u -v -30d +"%Y-%m-%dT%H:%M:%SZ")
curl -s -u "$GREENHOUSE_API_KEY:" \
  "https://harvest.greenhouse.io/v1/candidates?status=active&updated_before=$CUT&per_page=100" \
  | jq -r '.[] | "\(.id):\(.applications[0].id)"' > stale.txt

# 2) Reject each with the silver-medalist template + reason
while IFS=: read -r CAND_ID APP_ID; do
  curl -s -X POST -u "$GREENHOUSE_API_KEY:" \
    -H "On-Behalf-Of: $GH_USER_ID" \
    -H "Content-Type: application/json" \
    "https://harvest.greenhouse.io/v1/applications/$APP_ID/reject" \
    -d '{"rejection_reason":{"id":<no_response_reason_id>},"rejection_email":{"email_template_id":<silver_template_id>,"send_email_at":"now"}}'
  sleep 0.25  # rate-limit: 50 req / 10s
done < stale.txt
```

### Recipe 7: Apply auto-acknowledgment within 24h (Greenhouse)
```bash
# Greenhouse fires auto-ack on the job's confirmation_email setting:
curl -s -X PATCH -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -H "Content-Type: application/json" \
  "https://harvest.greenhouse.io/v1/jobs/<job_id>" \
  -d '{"confirmation_email_template_id": <ack_template_id>}'
```
Now every new application triggers the ack template. No-op for already-applied candidates.

### Recipe 8: Send status update via Gmail (when ATS template doesn't fit)
```python
# gmail-mcp send (PythonSDK style; use MCP tool inside the agent)
import os, base64, email.mime.text
msg = email.mime.text.MIMEText(open("status_update_post_screen.md").read())
msg["Subject"] = "Update on your Acme application"
msg["To"] = "jane@example.com"
msg["From"] = "recruiter@acme.com"
# gmail-mcp.send(raw=base64.urlsafe_b64encode(msg.as_bytes()).decode())
```
Pull template from `role.md` "Decline template library" → fill `{first_name}` / `{role}` placeholders → send.

### Recipe 9: Trigger Talent Board CandE-style NPS via Typeform
```bash
# Pre-built Typeform with `application_id` hidden field
LINK="https://acme.typeform.com/to/<form_id>?application_id=<app_id>&stage=post_onsite"
# Embed LINK in the stage-decision email or in a follow-up nudge T+1 after decision.
```

### Recipe 10: Pull CandE survey responses for weekly review
```bash
curl -s -H "Authorization: Bearer $TYPEFORM_TOKEN" \
  "https://api.typeform.com/forms/<form_id>/responses?since=2026-05-01T00:00:00Z" \
  | jq '.items[] | {submitted_at, nps: .answers[0].number, stage: .hidden.stage}'
```

### Recipe 11: Stage-age dashboard snapshot (any ATS, pandas)
```python
import pandas as pd, requests, os
# Pull active candidates → enrich with last stage-change timestamp
data = requests.get(
  "https://harvest.greenhouse.io/v1/candidates?status=active",
  auth=(os.environ["GREENHOUSE_API_KEY"], "")
).json()
df = pd.DataFrame(data)
df["days_in_stage"] = (pd.Timestamp.utcnow() - pd.to_datetime(df["last_activity"])).dt.days
df.groupby("days_in_stage").size().sort_index().to_csv("stage_age.csv")
```

### Recipe 12: Post-offer counter-offer reconciliation (T+2 nudge)
```bash
# Find offers sent but not accepted after 2 biz days
curl -s -u "$GREENHOUSE_API_KEY:" \
  "https://harvest.greenhouse.io/v1/offers?status=sent" \
  | jq '.[] | select((now - (.created_at | fromdateiso8601)) > (2*86400)) | {candidate_id, sent_at: .created_at}'
# For each: send the role.md "Post-offer counter-offer/decline" template OR recruiter call.
```

## Examples

### Example 1: Daily stalled-candidate sweep (Greenhouse)
**Goal:** No candidate sits >5 biz days in stage without a touch.
**Steps:**
1. Recipe 1 to list candidates by age bucket.
2. For each bucket: pull the per-stage template from `role.md` "Decline template library" or "Status update".
3. Decision: advance / decline / nudge with status — Recipe 3 (decline) or Recipe 8 (nudge).
4. Log results: total touched / declined / advanced; surface in weekly sync (`recruiting-metrics-time-to-fill-offer-accept`).

**Result:** Zero candidates >5 biz days untouched. CandE NPS lifts 10-20 points over 6 weeks.

### Example 2: 30-day cleanup with silver-medalist preservation
**Goal:** Archive no-response candidates without burning future-reconnect opportunity.
**Steps:**
1. Recipe 6 to bulk-archive 30-day no-response with the silver-medalist template (not the cold-reject template).
2. Tag each archived candidate `silver_medalist=true` via `POST /v1/candidates/<id>/tags`.
3. Hand the list to `talent-sourcer`'s `hot-list-talent-community-mgmt` for quarterly nurture.

**Result:** Clean active pipeline + preserved 15-25% next-quarter rehire pool.

### Example 3: SLA breach Slack alert
**Goal:** Recruiter gets pinged when any candidate crosses 5-biz-day onsite SLA.
**Steps:**
1. Register Greenhouse webhook `candidate_stage_change` (see `ats-greenhouse-lever-ashby-configuration` Recipe 5).
2. Cron job nightly via Recipe 1; if any candidate's onsite stage age >5 biz days, fire to `#recruiting-alerts` via slack-mcp.

**Result:** SLA breach detection without polling burden on recruiter.

## Edge cases / gotchas

- **"Decline" vs "withdraw" reason categories.** Greenhouse splits "We Rejected" vs "They Withdrew" — pick the right one or your funnel reports lie. Withdraw = candidate-initiated; reject = company-initiated.
- **Email template variables.** Greenhouse merges `{{CANDIDATE_FIRST_NAME}}`, `{{JOB_NAME}}`, `{{COMPANY_NAME}}`. Test in sandbox once per template update — a typo silently leaves the variable visible to the candidate.
- **Silent rejection still happens.** Even with templates configured, candidates fall through if you reject without `rejection_email.send_email_at`. Always include it.
- **Counter-offer recapture.** ~30% of senior candidates renege after counter-offer. Use Recipe 12 + the role.md "Post-offer counter-offer/decline" template; sometimes a 24h delay + recruiter call beats an immediate "OK noted" email.
- **Post-onsite decline tone.** Use specific behavioral feedback ("the panel wanted more X") not generic ("we went a different direction"). Candidates remember; brand depends on it.
- **Bulk archive sensitivity.** Don't bulk-archive applicants who applied within last 7 days — looks robotic + reduces re-apply rates. Set `applied_before` cutoff at 14+ days minimum.
- **Demographic survey + rejection coupling.** Voluntary demographic survey responses are aggregated; never join to individual rejection decisions in reporting (defer to `dei-hiring-diverse-slate-blind-resume` + `legal-counsel`).
- **CandE NPS sample size.** Typeform NPS needs ≥30 responses for stable reading; pool quarterly if low volume.
- **Time-zone math.** "5 business days" is recipient-tz; many ATSes return UTC timestamps. Convert before applying SLA cutoff.
- **Defer to `legal-counsel`** for: rejection-email retention windows (state-specific), demographic-data join restrictions, GDPR right-to-erasure on rejected applicants.

## Sources

- [Talent Board CandE Research](https://www.thetalentboard.org/cande-research-reports/)
- [Greenhouse candidate experience playbook](https://www.greenhouse.io/blog/candidate-experience)
- [Greenhouse `/applications/{id}/reject`](https://developers.greenhouse.io/harvest.html#post-reject-application)
- [Greenhouse Rejection Reasons](https://developers.greenhouse.io/harvest.html#rejection-reasons)
- [Ashby `application.archive`](https://developers.ashbyhq.com/reference/applicationarchive)
- [Lever `archived`](https://hire.lever.co/developer/documentation#archive-an-opportunity)
- [Greenhouse candidate-rejection-emails guide](https://www.greenhouse.io/blog/candidate-rejection-emails)
- [Metaview — candidate experience 2026](https://www.metaview.ai/resources/blog/candidate-experience)
