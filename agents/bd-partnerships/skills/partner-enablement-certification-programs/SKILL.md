<!--
Source: https://canvas.instructure.com/doc/api/ + https://academy.hubspot.com/partner-program + https://www.allbound.com/
Tiered partner certification programs via LMS (June 2026 SOTA).
-->
# Partner Enablement + Certification Programs — SKILL

Build, deliver, and track tiered partner certification programs. Standard tier model: **Foundation → Specialist → Expert**, each gated by training module + assessment + practical exercise. Delivered via LMS (Canvas / HubSpot Academy / Salesforce Trailhead / Allbound LMS / Mindtickle / Highspot). Track per-partner certification status in CRM custom object; sandbox + technical accreditation for integration partners.

## When to use

- **Launching a new partner certification program** — from scratch.
- **Adding a tier or specialization** to existing program.
- **Authoring new training module** + assessment + practical exercise.
- **Tracking partner cert status** — feeds into tier eligibility, deal-reg uplift, scorecards.
- **Renewing certifications** — annual recertification + recall-test cadence.
- **Trigger phrases**: "build partner certification", "Foundation Specialist Expert tiers", "LMS for partners", "partner sandbox", "certification renewal".

Do NOT use this skill for: **internal employee training** (out of scope); **the actual content authoring expertise** (subject-matter experts); **commercial reseller tier gating** (use `channel-pricing-discount-tiers`).

## Setup

```bash
# Canvas LMS (open source, self-hosted, most flexible)
# Canvas-mcp configured in MCP settings; or direct API:
export CANVAS_BASE_URL="https://your-canvas-instance.example.com"
export CANVAS_API_TOKEN="<token>"          # User profile → Settings → New Access Token

# HubSpot Academy (if HubSpot ecosystem partner)
# No public API for course creation — use the academy portal directly + Recipe 11 for tracking

# Salesforce Trailhead (for Salesforce partners)
# Trailmix authoring via Trailmaker (portal); badging via Trailhead

# Allbound (if PRM = Allbound) — has built-in LMS
export ALLBOUND_API_KEY="<key>"

# CRM custom-object for certification status
export MATON_API_KEY="<key>"               # used for HubSpot/Salesforce certification updates
```

## Common recipes

### Recipe 1: Canvas — create a course (Foundation tier)

```bash
curl -X POST "$CANVAS_BASE_URL/api/v1/accounts/<account-id>/courses" \
  -H "Authorization: Bearer $CANVAS_API_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "course": {
      "name": "Brand Partner Foundation",
      "course_code": "BPF-101",
      "start_at": "2026-07-01T00:00:00Z",
      "end_at": "2027-06-30T23:59:59Z",
      "is_public_to_auth_users": true,
      "default_view": "modules"
    }
  }'
```

Reference: https://canvas.instructure.com/doc/api/courses.html#method.courses.create.

### Recipe 2: Canvas — create modules (sequenced learning path)

```bash
COURSE_ID="<from-recipe-1>"
curl -X POST "$CANVAS_BASE_URL/api/v1/courses/$COURSE_ID/modules" \
  -H "Authorization: Bearer $CANVAS_API_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "module": {
      "name": "Module 1 — Brand 101",
      "position": 1,
      "require_sequential_progress": true,
      "publish_final_grade": false
    }
  }'

# Add page to module
curl -X POST "$CANVAS_BASE_URL/api/v1/courses/$COURSE_ID/pages" \
  -H "Authorization: Bearer $CANVAS_API_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "wiki_page": {
      "title": "What is Brand and who is it for",
      "body": "<markdown-converted-html>",
      "published": true
    }
  }'

# Link page to module
curl -X POST "$CANVAS_BASE_URL/api/v1/courses/$COURSE_ID/modules/<module-id>/items" \
  -H "Authorization: Bearer $CANVAS_API_TOKEN" -H "Content-Type: application/json" \
  -d '{"module_item": {"type":"Page","page_url":"what-is-brand","position":1}}'
```

### Recipe 3: Canvas — create assessment (quiz)

```bash
# Quizzes API — multi-question assessment
curl -X POST "$CANVAS_BASE_URL/api/v1/courses/$COURSE_ID/quizzes" \
  -H "Authorization: Bearer $CANVAS_API_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "quiz": {
      "title": "Foundation Assessment",
      "quiz_type": "graded_quiz",
      "scoring_policy": "keep_highest",
      "time_limit": 30,
      "allowed_attempts": 3,
      "show_correct_answers": false,
      "shuffle_answers": true,
      "points_possible": 50,
      "published": false
    }
  }'

# Add a question
curl -X POST "$CANVAS_BASE_URL/api/v1/courses/$COURSE_ID/quizzes/<quiz-id>/questions" \
  -H "Authorization: Bearer $CANVAS_API_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "question": {
      "question_name": "Q1 — ICP definition",
      "question_text": "What is the primary use case for Brand?",
      "question_type": "multiple_choice_question",
      "points_possible": 5,
      "answers": [
        {"answer_text":"Pipeline analytics for revenue teams","weight":100,"answer_comments":"Correct"},
        {"answer_text":"Email marketing","weight":0},
        {"answer_text":"Calendar scheduling","weight":0}
      ]
    }
  }'
```

Reference: https://canvas.instructure.com/doc/api/quizzes.html.

### Recipe 4: Canvas — enroll partner contact

```bash
curl -X POST "$CANVAS_BASE_URL/api/v1/courses/$COURSE_ID/enrollments" \
  -H "Authorization: Bearer $CANVAS_API_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "enrollment": {
      "user_id": "<canvas-user-id>",
      "type": "StudentEnrollment",
      "enrollment_state": "active",
      "notify": true
    }
  }'

# Bulk enroll via SIS or CSV; for ≤ 25 enrollments, the API is fine
```

### Recipe 5: Canvas — pull completion status (drives CRM update)

```bash
curl "$CANVAS_BASE_URL/api/v1/courses/$COURSE_ID/students?include[]=enrollments" \
  -H "Authorization: Bearer $CANVAS_API_TOKEN" | jq '.[] | {
    user_id: .id,
    name,
    grade: .enrollments[0].grades.current_score,
    completed_at: .enrollments[0].completed_at
  }'
```

### Recipe 6: Tiered program design (canonical)

```yaml
program:
  name: "Brand Partner Certification Program"
  tiers:
    foundation:
      audience: "Anyone at partner — sales, marketing, CS"
      hours: 4
      modules: ["Brand 101","ICP + value props","Demo walkthrough","Common objections"]
      assessment: "Quiz, 70% pass, 3 attempts allowed"
      validity: "12 months"
      perks: "Authorized Partner tier eligibility"
    specialist:
      audience: "Sales reps actively selling Brand"
      prereq: "Foundation pass"
      hours: 8
      modules: ["Discovery framework","MEDDIC w/ Brand","Pricing + packaging","Competitive positioning","Customer references"]
      assessment: "Quiz (80% pass) + roleplay submission (recorded; reviewed by us)"
      validity: "12 months"
      perks: "Silver tier eligibility; 5% deal-reg uplift"
    expert:
      audience: "Solution architects, technical pre-sales"
      prereq: "Specialist pass + 1+ closed-won deal"
      hours: 16
      modules: ["Architecture deep dive","Integration patterns","Sandbox certification","Advanced demo authoring","Customer success patterns"]
      assessment: "Quiz (85% pass) + live technical demo session with our team + case study submission"
      validity: "12 months"
      perks: "Gold tier eligibility; 10% deal-reg uplift; co-sell motion access"
```

### Recipe 7: Sandbox provisioning (integration partner certs)

```bash
# For integration partners — provision sandbox account
curl -X POST "https://gateway.maton.ai/yourapp/v1/admin/sandbox" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "partner_id": "acme-int-001",
    "partner_contact_email": "dev@acme.com",
    "sandbox_tier": "partner_sandbox",
    "data_seed": "demo_dataset_v2",
    "expiration": "2027-06-30"
  }'
```

Sandbox onboarding is a 60-min orientation + 2-week build-along. Track sandbox use as a leading certification metric.

### Recipe 8: CRM certification-status field update

```bash
# HubSpot company-level certifications
curl -X PATCH "https://gateway.maton.ai/hubspot/crm/v3/objects/companies/<company-id>" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "partner_cert_foundation_count": "5",
      "partner_cert_specialist_count": "2",
      "partner_cert_expert_count": "0",
      "partner_tier_eligible": "silver",
      "partner_tier_last_updated": "2026-06-10"
    }
  }'

# Salesforce partner contact custom field
sf data update record --target-org packaging \
  --sobject Contact --record-id <contact-id> \
  --values "Partner_Cert_Level__c='Specialist' Partner_Cert_Expires__c=2027-06-10"
```

### Recipe 9: Certification renewal workflow

```python
# Run weekly cron
import requests, os
from datetime import datetime, timedelta

# Find all certs expiring in 30/60/90 days
expiring = run_sql("""
  SELECT contact_id, contact_email, cert_level, cert_expires
  FROM partner_certifications
  WHERE cert_expires BETWEEN now() AND now() + interval '90 days'
""")

for row in expiring:
    days_left = (row["cert_expires"] - datetime.now()).days
    if days_left <= 30:
        template = "renewal-urgent"
    elif days_left <= 60:
        template = "renewal-soon"
    else:
        template = "renewal-window"
    send_email(row["contact_email"], template, days_left=days_left)
```

Send via `gmail-mcp` with templated content. Renewal often = condensed recall test (30 min) rather than full re-cert.

### Recipe 10: Practical exercise — roleplay submission flow

```yaml
# For Specialist tier, learner submits recorded mock-pitch
practical_exercise:
  prompt: "Record a 5-min discovery pitch covering pain probe, solution overview, pricing"
  submission: "Loom / Drift video upload + transcript"
  rubric:
    discovery_quality: "1-5; checks if rep probes pain"
    framing_accuracy: "1-5; product positioned correctly"
    competitive_handling: "1-5; objections handled gracefully"
    pricing_confidence: "1-5; presents pricing without apology"
  reviewer: "Our partner-success-team"
  feedback_sla: "5 business days"
  result: "Pass / Pass with comments / Re-submit"
```

Track submissions in `notion-mcp`; reviewer assignment via `slack-mcp` notifications.

### Recipe 11: Pull all certifications (no-API LMS fallback)

```python
# HubSpot Academy / Trailhead have no public cert-export API
# Use playwright-mcp:
# 1. Login to partner academy portal
# 2. Navigate to "My Certifications" or admin export view
# 3. CSV download → load to postgresql-mcp warehouse

# For Trailhead, expose your own Trailblazer profile via:
# https://trailblazer.me/id/<user-id>
# Scrape badge list weekly; update Salesforce contact field via Recipe 8
```

### Recipe 12: Certification dashboard query

```sql
-- postgresql-mcp warehouse query for QBR scorecard
SELECT
  c.partner_company,
  COUNT(*) FILTER (WHERE level='foundation') AS foundation_count,
  COUNT(*) FILTER (WHERE level='specialist') AS specialist_count,
  COUNT(*) FILTER (WHERE level='expert') AS expert_count,
  MAX(cert_date) AS most_recent_cert,
  COUNT(*) FILTER (WHERE cert_expires < now()) AS expired_count,
  CASE
    WHEN COUNT(*) FILTER (WHERE level='expert') >= 1 THEN 'gold'
    WHEN COUNT(*) FILTER (WHERE level='specialist') >= 3 THEN 'silver'
    WHEN COUNT(*) FILTER (WHERE level='foundation') >= 1 THEN 'authorized'
    ELSE 'none'
  END AS tier_eligible
FROM partner_certifications c
GROUP BY c.partner_company
ORDER BY specialist_count DESC;
```

## Examples

### Example 1: Launch Foundation tier from zero

**Goal:** First certification program; need Foundation-tier course live in 2 weeks.

**Steps:**
1. Week 1 Day 1-2 — Recipe 6 — Program design in Notion.
2. Day 3-5 — Content authoring (subject-matter experts).
3. Day 5 — `pptx` slides + `docx` learner workbook + Loom video recordings.
4. Day 6 — Recipe 1 + 2 — Canvas course skeleton with 4 modules.
5. Day 7 — Recipe 3 — Quiz with 20 questions.
6. Day 8 — Pilot with 5 internal team members; refine.
7. Day 10 — Recipe 4 — Enroll first 25 partner contacts; announcement via `gmail-mcp`.
8. Day 14 — First Foundation graduates; Recipe 8 → CRM updates.

**Result:** Foundation tier shipping; 25 enrolled; first 8 passes by Day 14.

### Example 2: Specialist tier with roleplay assessment

**Goal:** Specialist-tier program; mid-tier cert for active sellers.

**Steps:**
1. Recipe 6 — Specialist tier spec; reviewer team in place.
2. Modules authored; Canvas course built (Recipe 1-3).
3. Recipe 10 — Roleplay rubric authored; reviewer assignment via Slack.
4. First cohort enrolled.
5. Roleplay submissions reviewed; pass/fail/re-submit feedback.
6. CRM updated; tier eligibility recalculated weekly via Recipe 12.

**Result:** Specialist tier delivers quality bar via roleplay; passes earn deal-reg uplift.

### Example 3: Annual recertification cycle

**Goal:** Q3 recertification campaign; 120 certs expiring within 90 days.

**Steps:**
1. Recipe 9 — Cron query identifies expiring certs.
2. Email campaign via `gmail-mcp` mailmerge — 30-day, 60-day, 90-day notices.
3. Renewal flow: 30-min recall test (Canvas Recipe 3 reused with subset of questions).
4. Pass → cert extended 12 months via Recipe 8.
5. Fail → 14-day grace period for full re-cert.

**Result:** 105/120 renewed (88% retention); tier-eligibility maintained.

## Edge cases / gotchas

- **Canvas LMS hosting** — self-hosting Canvas is non-trivial (Postgres + Redis + S3). For solo founders, use Instructure Cloud ($) or pivot to HubSpot Academy / Trailhead.
- **HubSpot Academy is closed** — you can't build courses there as a partner; HubSpot publishes its own. Use it as benchmark / target for your partners to learn HubSpot.
- **Salesforce Trailhead** is HubSpot-Academy-equivalent — partner-specific badges via Trailmix; build via Trailmaker (Salesforce CRM Analytics).
- **Allbound LMS** is fine for SMB-to-mid; UI is dated; reporting limited.
- **Roleplay assessments are reviewer-bottlenecked** — budget 30 min per submission; pre-train reviewers on rubric; use video-AI tools (Gong / Chorus equivalents) for automated scoring.
- **Cert validity period** — 12 months is standard; 24 months for stable categories. Shorter = more friction; longer = stale certifications.
- **Prerequisite enforcement** — Canvas can enforce by module-completion gates; LMS without can be bypassed.
- **Multi-language content** — translate via `deepl-mcp`; pre-localize before partner expansion (esp Japan, Germany, France).
- **Time-zone handling** — quizzes with time limits + global partners → use UTC; show local time on enrollment.
- **Cert renewal lapses are the #1 churn signal** — partners that don't renew often disengage from the program. Treat as early-warning.
- **Practical exercise plagiarism** — second time a partner submits the same video, you'll notice. Track video hashes.
- **CRM custom-object schema** — define partner-cert as separate object (1 partner : N certs) not company field (1 company : 1 string). Allows reporting + history.
- **PRM vs CRM source of truth** — PRM (Allbound, Impartner) often has its own cert tracking; reconcile with CRM via nightly sync.
- **Co-branding restrictions** — partner using "Brand Certified Expert" in their own marketing should have brand-usage guidelines; provide a 1-pager.
- **Certification ≠ enablement** — certified partner is technically competent but may not be motivated to sell. Pair with co-marketing + MDF + scorecard.
- **Tier eligibility floors vs ceilings** — Recipe 12 calculates eligibility from cert count; actual tier assignment also factors in revenue + sat. Eligibility is necessary, not sufficient.
- **Recertification cost** — annual content refresh is real engineering work. Budget 20% of program-team time on maintenance.
- **GDPR / data residency** — Canvas + LMS data may include EU partner-contact PII. Confirm data-residency for EU partners.

## Sources

- Canvas LMS API: https://canvas.instructure.com/doc/api/
- Canvas Quizzes API: https://canvas.instructure.com/doc/api/quizzes.html
- Canvas Modules API: https://canvas.instructure.com/doc/api/modules.html
- HubSpot Academy: https://academy.hubspot.com/partner-program
- Salesforce Trailhead Partner program: https://trailhead.salesforce.com/users/partners
- Allbound LMS: https://www.allbound.com/
- Mindtickle: https://www.mindtickle.com/
- Highspot: https://www.highspot.com/
- Partner certification benchmarks — Forrester: https://www.forrester.com/research/partner-ecosystems/
- Tiered partner program patterns: https://www.crossbeam.com/blog/partner-tiers/
