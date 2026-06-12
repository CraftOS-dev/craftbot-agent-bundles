<!--
Sources: https://developers.greenhouse.io/harvest.html
         https://developers.ashbyhq.com/reference
         https://hire.lever.co/developer/documentation
         https://www.index.dev/blog/greenhouse-vs-lever-vs-ashby-ats-comparison
ATS landscape 2026: Greenhouse = G2 Winter 2026 leader (series B+, 7,500+ customers);
Ashby = fastest-growing API-first (series A-B, deepest analytics, includeCompensation=true);
Lever = ATS+CRM unified (series B+); Workable = SMB tier.
-->
# ATS Configuration — Greenhouse / Lever / Ashby / Workable — SKILL

Configure the ATS that runs the recruiter's day: pipeline stages, scorecards, interview kits, automation webhooks, rejection-reason taxonomy, demographic survey, and user permissions. Specialized to the Big-4 SMB-to-growth ATSes (Greenhouse, Ashby, Lever, Workable) plus the cross-cutting patterns that are identical across all four.

## When to use

- User opens a new requisition and needs the **pipeline stages, scorecards, and interview kit** wired up before the first candidate enters.
- Adding **automation webhooks** (stage-advance, scorecard-submit, offer-extended, offer-signed) — the heart of the recruiter's async workflow.
- Configuring **rejection-reason taxonomy**, **demographic survey**, **user permissions / On-Behalf-Of** for compliance + audit trail.
- Trigger phrases: "configure ATS", "new req setup", "open job stages", "build scorecard", "interview kit deploy", "ATS automation", "webhook fired wrong".
- Defer to `talent-sourcer` for top-of-funnel CRM sourcing; defer to `legal-counsel` for demographic-data retention questions.

## Setup

```bash
# Greenhouse Harvest API
export GREENHOUSE_API_KEY="harvest_xxx"      # https://app.greenhouse.io/configure/dev_center/credentials
export GREENHOUSE_BOARD_TOKEN="company"      # public job-board slug
export GH_USER_ID="123456"                   # responsible recruiter (for On-Behalf-Of)

# Ashby
export ASHBY_API_KEY="xxx"                   # https://app.ashbyhq.com/admin/api-keys

# Lever
export LEVER_API_KEY="xxx"                   # https://hire.lever.co/settings/integrations/api
export LEVER_SITE="company"

# Workable
export WORKABLE_API_KEY="xxx"                # https://<subdomain>.workable.com/backend/account/api_access
export WORKABLE_SUBDOMAIN="company"
```

Auth model:
- Greenhouse / Ashby / Lever / Workable all use **basic auth with empty password** (`-u "$KEY:"`). API itself is free; ATS seat is paid.
- Greenhouse writes require `On-Behalf-Of: <user_id>` header. Lever requires `?perform_as=<user_id>` query param. Ashby + Workable infer actor from key.

## Common recipes

### Recipe 1: List job stages on an existing job (Greenhouse)
```bash
curl -s -u "$GREENHOUSE_API_KEY:" \
  "https://harvest.greenhouse.io/v1/jobs/<job_id>/job_stages" | jq '.[] | {id, name, position}'
```
Returns ordered stages. Useful as input to scorecard binding (Recipe 4).

### Recipe 2: Add a custom job stage (Greenhouse)
```bash
curl -s -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -H "Content-Type: application/json" \
  -X POST "https://harvest.greenhouse.io/v1/jobs/<job_id>/job_stages" \
  -d '{"name":"Architecture Review","position":5}'
```

### Recipe 3: Create interview kit with weighted rubric (Greenhouse)
```bash
curl -s -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -H "Content-Type: application/json" \
  -X POST "https://harvest.greenhouse.io/v1/jobs/<job_id>/job_stages/<stage_id>/interviews" \
  -d '{
    "name":"Senior Backend — Live Pairing (90 min)",
    "estimated_minutes":90,
    "interview_kit":{
      "instructions":"Live-pair on the URL-shortener problem. Score system-design and code-quality competencies.",
      "questions":[
        {"question":"Walk me through your design before you code.","competencies":["system-design"]},
        {"question":"How would you handle 10× load?","competencies":["system-design"]}
      ]
    }
  }'
```

### Recipe 4: Submit scorecard (Greenhouse)
```bash
curl -s -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -H "Content-Type: application/json" \
  -X PATCH "https://harvest.greenhouse.io/v1/applications/<app_id>/scorecards/<scorecard_id>" \
  -d '{
    "overall_recommendation":"yes",
    "attributes":[
      {"name":"System design","rating":4},
      {"name":"Code quality","rating":4},
      {"name":"Collaboration","rating":5}
    ],
    "submitted_by_id": '"$GH_USER_ID"'
  }'
```

### Recipe 5: Register webhook (Greenhouse)
```bash
curl -s -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -H "Content-Type: application/json" \
  -X POST "https://harvest.greenhouse.io/v1/web_hooks" \
  -d '{
    "name":"Stage advance → recruiter Slack",
    "url":"https://hooks.example.com/greenhouse/stage-advance",
    "secret_key":"<hmac_secret>",
    "web_hook_type":"candidate_stage_change"
  }'
```
Events: `candidate_stage_change`, `application_updated`, `scorecard_submitted`, `offer_created`, `offer_accepted`, `candidate_hired`, `candidate_rejected`.

### Recipe 6: Create feedback form with weighted scoring (Ashby)
```bash
curl -s -X POST "https://api.ashbyhq.com/feedbackForm.create" \
  -u "$ASHBY_API_KEY:" -H "Content-Type: application/json" \
  -d '{
    "title":"Senior Backend — Onsite Loop",
    "questions":[
      {"id":"q1","title":"System design","type":"RatingFromOneToFour","competency":"system-design","weight":3},
      {"id":"q2","title":"Code quality","type":"RatingFromOneToFour","competency":"code-quality","weight":2},
      {"id":"q3","title":"Overall recommendation","type":"RatingFromOneToFour","weight":1}
    ]
  }'
```

### Recipe 7: Change candidate stage (Ashby)
```bash
curl -s -X POST "https://api.ashbyhq.com/application.changeStage" \
  -u "$ASHBY_API_KEY:" -H "Content-Type: application/json" \
  -d '{"applicationId":"<id>","interviewStageId":"<stage_id>"}'
```

### Recipe 8: Register Ashby webhook subscription
```bash
curl -s -X POST "https://api.ashbyhq.com/webhook.create" \
  -u "$ASHBY_API_KEY:" -H "Content-Type: application/json" \
  -d '{
    "webhookEventType":"applicationStageTransition",
    "requestUrl":"https://hooks.example.com/ashby/stage",
    "secretToken":"<hmac>"
  }'
```
Events: `applicationStageTransition`, `applicationSubmit`, `feedbackSubmit`, `offerCreate`, `interviewScheduleCreate`.

### Recipe 9: List stages + post feedback (Lever)
```bash
# List stages
curl -s -u "$LEVER_API_KEY:" "https://api.lever.co/v1/stages?limit=100" | jq '.data[] | {id, text}'

# Post feedback
curl -s -u "$LEVER_API_KEY:" \
  -H "Content-Type: application/json" \
  -X POST "https://api.lever.co/v1/opportunities/<opp_id>/feedback?perform_as=$LEVER_USER_ID" \
  -d '{
    "baseTemplateId":"<feedback_template_id>",
    "fields":[
      {"id":"system_design","value":"4"},
      {"id":"summary","value":"Strong system-design depth; concerns on team-lead experience."}
    ]
  }'
```

### Recipe 10: Lever Hooks (webhook registration)
```bash
# Lever Hooks are configured in UI under Settings → Integrations → Lever Hooks.
# Programmatic registration via signed integration; for ad-hoc, use the UI.
# Test webhook payload locally:
curl -X POST "https://hooks.example.com/lever/stage" \
  -H "X-Lever-Signature: <hmac>" \
  -d '{"event":"candidateStageChange","data":{...}}'
```

### Recipe 11: Workable — list + create job, push candidate
```bash
# List jobs
curl -s -H "Authorization: Bearer $WORKABLE_API_KEY" \
  "https://$WORKABLE_SUBDOMAIN.workable.com/spi/v3/jobs?state=published"

# Create candidate against a job
curl -s -X POST -H "Authorization: Bearer $WORKABLE_API_KEY" \
  -H "Content-Type: application/json" \
  "https://$WORKABLE_SUBDOMAIN.workable.com/spi/v3/jobs/<shortcode>/candidates" \
  -d '{"candidate":{"name":"Jane Doe","email":"jane@example.com","headline":"Senior Backend","summary":"..."}}'
```

### Recipe 12: Build rejection-reason taxonomy (Greenhouse)
```bash
# List reasons in current account
curl -s -u "$GREENHOUSE_API_KEY:" "https://harvest.greenhouse.io/v1/rejection_reasons" \
  | jq '.[] | {id, name, type: .type.name}'

# Output: We Rejected / They Withdrew categories with sub-reasons. Use the IDs
# in the rejection endpoint (see candidate-experience-sla-status-updates skill).
```

### Recipe 13: Configure demographic survey (Greenhouse)
```bash
# Demographic questions are managed at the org level — enable per job:
curl -s -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -X PATCH "https://harvest.greenhouse.io/v1/jobs/<job_id>" \
  -d '{"custom_fields":{"eeoc_survey_enabled":true}}'

# Demographic answers come through aggregated; never tied to candidate IDs in
# reports. See dei-hiring-diverse-slate-blind-resume skill.
```

## Examples

### Example 1: Open a new Series-A Senior Backend req end-to-end (Ashby)
**Goal:** Job created with compensation field, stages laid out, feedback forms bound, webhook firing into Linear and Slack.
**Steps:**
1. Create job with `POST /job.create` and include `compensation: {min, max, currency, type: "Salary"}`.
2. List default stages with `GET /interviewStage.list?interviewPlanId=<plan>`; add `Architecture Review` between `Onsite` and `Debrief` via `POST /interviewStage.create`.
3. Create feedback forms for each stage (Recipe 6) with weighted rubric.
4. Register `applicationStageTransition` + `feedbackSubmit` webhooks (Recipe 8).
5. Verify the public job board: `curl "https://api.ashbyhq.com/posting-api/job-board/$ASHBY_SITE?includeCompensation=true"` shows the comp range.

**Result:** Req live with structured scorecards + comp-transparent posting + automation hooks into Linear ticket creation per stage advance.

### Example 2: Migrate scorecard rubric across Greenhouse + Ashby for same role
**Goal:** Maintain a single source-of-truth competency model (Notion) and push the same weighted rubric to both ATSes.
**Steps:**
1. Author competency model in Notion (`structured-interview-star-bar` skill).
2. Greenhouse: PATCH each interview's `interview_kit.questions[]` with competency tags (Recipe 3).
3. Ashby: POST `feedbackForm.create` with matching `competency` + `weight` (Recipe 6).
4. Diff check: pull both back and compare `(competency, weight)` tuples to confirm parity.

**Result:** One competency model, two ATS-native rubrics, defensible audit trail.

## Edge cases / gotchas

- **Greenhouse `On-Behalf-Of` is mandatory for writes.** Drop the header → 403. Always pass the responsible recruiter's `user_id`. Audit trail depends on it.
- **Lever `perform_as` is mandatory for mutations.** Same pattern; omit → 403.
- **Rate limits.** Greenhouse Harvest = 50 req / 10s. Ashby = 60 req / min default (raise via support). Lever = 10 req / s. Workable = 60 req / min. For backfills: chunk + sleep with `time.sleep(0.25)`; on 429, exponential backoff to 30s.
- **Ashby `includeCompensation=true` is empty unless the job has compensation set in-app.** Required for CA SB 1162 + NY pay transparency + CO Equal Pay for Equal Work.
- **Greenhouse job-board cache.** `boards-api.greenhouse.io` lags Harvest mutations by 2-5 min. Don't gate on instant consistency.
- **Scorecard schema is per-job-template.** Fetch `/scorecards/<id>` first to learn the attribute list before submitting.
- **Webhook secret verification.** All four sign with HMAC-SHA256; verify or get spoofed. Greenhouse: `X-Greenhouse-Signature`. Ashby: `Ashby-Signature`. Lever: `X-Lever-Signature`. Workable: `X-Workable-Signature`.
- **Webhook delivery retries.** Greenhouse retries up to 6 times with backoff. Ashby retries for 24h. Idempotent handler required.
- **Candidate dedupe.** Greenhouse + Lever dedupe by email globally; re-creating returns the existing record. Idempotent by design but be aware that `POST /candidates` may return 200 with the existing ID, not 201.
- **Permissions vs API key scope.** A "Site Admin" key sees everything; a "Job Admin" key sees only assigned jobs. Permission mismatch → 403 or empty list. Verify with `GET /users/me`.
- **DEI demographic data.** Aggregated only — never join to individual candidate IDs in reports. See `dei-hiring-diverse-slate-blind-resume`.
- **Workable's API is lighter.** No interview-kit endpoint; manage in UI. API supports candidate CRUD + stage moves + basic feedback.
- **Defer to `legal-counsel`** for: demographic-data retention windows (varies by state + country), GDPR right-to-erasure on ATS records, EEO-1 reporting format.

## Sources

- [Greenhouse Harvest API](https://developers.greenhouse.io/harvest.html)
- [Greenhouse Job Board API](https://developers.greenhouse.io/job-board.html)
- [Ashby Developer Docs](https://developers.ashbyhq.com/reference)
- [Lever Developer Documentation](https://hire.lever.co/developer/documentation)
- [Lever Hooks (webhooks)](https://hire.lever.co/developer/webhooks)
- [Workable API reference](https://workable.readme.io/reference)
- [Index — Greenhouse vs Lever vs Ashby 2026](https://www.index.dev/blog/greenhouse-vs-lever-vs-ashby-ats-comparison)
- [Unified.to — 15 ATS APIs 2026](https://unified.to/blog/15_ats_apis_to_integrate_with_in_2026_greenhouse_lever_workable)
