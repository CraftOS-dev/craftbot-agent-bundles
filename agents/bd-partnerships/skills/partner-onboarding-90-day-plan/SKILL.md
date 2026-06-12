<!--
Source: https://partnerstack.com/blog/partner-onboarding + https://www.allbound.com/blog/partner-onboarding-checklist + https://www.impartner.com/blog/partner-onboarding + https://canvas.instructure.com/doc/api/ + https://developers.hubspot.com/docs/api/crm/objects/custom-objects
Standardized 90-day partner onboarding: Day 0 / 7 / 30 / 60 / 90 milestones (June 2026 SOTA).
-->
# Partner Onboarding 90-Day Plan — SKILL

Standardized 90-day onboarding from Day-0 contract sign through Day-90 scorecard review + tier-eligibility check. Auto-creates: per-partner Slack channel, CRM tasks, LMS enrollment, Notion onboarding plan, Day-7 kickoff calendar invite, Day-30/60/90 review checkpoints. Drives consistent partner experience and measurable time-to-first-deal-reg / time-to-first-closed-won.

## When to use

- **New partner agreement signed** — fire the full 90-day plan.
- **Partner re-onboarding** — after long dormancy or tier change.
- **Multi-partner cohort onboarding** — quarterly cohort of 5-10 new partners.
- **Onboarding health check** — % of partners passing Day-30 / Day-60 / Day-90 gates.
- **Onboarding template iteration** — improve based on cohort retros.
- **Trigger phrases**: "onboard new partner X", "kick off Acme onboarding", "Day-30 review for Acme", "first deal-reg from new partners this quarter", "onboarding completion rate".

Do NOT use this skill for: **the partner agreement itself** (use `referral-affiliate-channel-oem-agreement-structuring`); **per-partner scorecard** (use `partner-scorecard-authoring`); **certification programs** (use `partner-enablement-certification-programs`); **Partnerstack/PRM CRUD ops** (use `partnerstack-tackle-channel-management`).

## Setup

```bash
export MATON_API_KEY="<key>"
export HUBSPOT_PRIVATE_APP_TOKEN="<token>"
export SALESFORCE_INSTANCE_URL="<url>"
export SALESFORCE_ACCESS_TOKEN="<token>"
export NOTION_API_KEY="<key>"
export SLACK_BOT_TOKEN="<token>"
export GMAIL_OAUTH_TOKEN="<token>"
export GOOGLE_CALENDAR_TOKEN="<token>"
export CANVAS_ACCESS_TOKEN="<token>"
export CANVAS_BASE_URL="https://your-org.instructure.com"
export PARTNERSTACK_API_KEY="<key>"
```

**One-time Notion DBs:**
- `Onboarding Plans` (partner_id, owner, start_date, status, current_milestone, day0/7/30/60/90 fields)
- `Onboarding Tasks` (task, owner, due, status, partner_id, milestone)
- `Onboarding Cohort Retros` (cohort, completion %, time-to-first-deal-reg, time-to-first-closed-won, top-3 friction)

## Common recipes

### Recipe 1: Day-0 — kick off all subsystems

```python
def kickoff_onboarding(partner_id, partner_name, primary_contact_email, primary_contact_first_name,
                       motion, tier, channel_manager_email, start_date):
    # 1. Welcome email
    gmail_send(to=primary_contact_email,
               subject=f"Welcome to {VENDOR_NAME} Partner Program",
               body=f"""Hi {primary_contact_first_name},

Welcome to {partner_name}'s onboarding. Schedule:
- Day 7: Kickoff call (calendar invite incoming)
- Day 7-30: Foundation cert (LMS link in next email)
- Day 30 / 60 / 90: Reviews

Channel manager: {channel_manager_email}. Slack: #partner-{partner_id}.

— Sarah, VP Partnerships""")

    # 2. Slack channel
    slack_create_channel(f"partner-{partner_id}", invite=[primary_contact_email, channel_manager_email, "sarah@vendor.com"])

    # 3. CRM partner record + onboarding tasks
    create_crm_onboarding_tasks(partner_id, start_date, channel_manager_email)

    # 4. LMS enrollment
    if motion in ("reseller","integration"):
        canvas_enroll_in_foundation_cert(primary_contact_email, partner_id)

    # 5. Notion onboarding plan from template
    notion_create_onboarding_plan(partner_id, partner_name, motion, tier, channel_manager_email, start_date)

    # 6. Day-7 kickoff call calendar invite
    schedule_kickoff(partner_id, primary_contact_email, channel_manager_email, start_date + timedelta(days=7))
```

### Recipe 2: Create Slack channel per partner

```bash
curl -X POST "https://slack.com/api/conversations.create" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" -H "Content-Type: application/json; charset=utf-8" \
  -d '{"name":"partner-acme-001","is_private":false}'

# Invite primary contact + channel manager
curl -X POST "https://slack.com/api/conversations.invite" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" -H "Content-Type: application/json; charset=utf-8" \
  -d '{"channel":"<channel_id>","users":"U01ABC,U02DEF"}'

# Pin onboarding plan
curl -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" -H "Content-Type: application/json; charset=utf-8" \
  -d '{"channel":"<channel_id>","text":"Welcome! Onboarding plan: <Notion URL>. Day-7 kickoff calendar incoming."}'
```

Reference: https://api.slack.com/methods/conversations.create.

### Recipe 3: Create CRM onboarding tasks

```bash
# HubSpot: per-partner task list via Tasks API
for task in "Day-7 kickoff call" "Day-30 review" "Day-60 review" "Day-90 scorecard review"; do
  curl -X POST "https://gateway.maton.ai/hubspot/crm/v3/objects/tasks" \
    -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
    -d "{\"properties\":{
        \"hs_task_subject\":\"$task — Acme\",
        \"hs_task_status\":\"NOT_STARTED\",
        \"hs_task_priority\":\"HIGH\",
        \"hubspot_owner_id\":\"<channel_manager_owner_id>\",
        \"hs_timestamp\":\"<due_iso>\"
      }}"
done
```

### Recipe 4: LMS enrollment in Foundation certification (Canvas)

```bash
curl -X POST "$CANVAS_BASE_URL/api/v1/courses/<foundation_course_id>/enrollments" \
  -H "Authorization: Bearer $CANVAS_ACCESS_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "enrollment":{
      "user_id":"sis_user_id:sarah@acme.com",
      "type":"StudentEnrollment",
      "enrollment_state":"active",
      "notify":true
    }
  }'
```

Reference: https://canvas.instructure.com/doc/api/enrollments.html.

### Recipe 5: Notion onboarding plan from template

```python
def notion_create_onboarding_plan(partner_id, partner_name, motion, tier, channel_manager_email, start_date):
    day7 = start_date + timedelta(days=7)
    day30 = start_date + timedelta(days=30)
    day60 = start_date + timedelta(days=60)
    day90 = start_date + timedelta(days=90)

    page = notion.pages.create(
        parent={"database_id": ONBOARDING_PLANS_DB},
        properties={
            "Partner":{"title":[{"text":{"content":partner_name}}]},
            "Partner ID":{"rich_text":[{"text":{"content":partner_id}}]},
            "Motion":{"select":{"name":motion}},
            "Tier":{"select":{"name":tier}},
            "Owner":{"rich_text":[{"text":{"content":channel_manager_email}}]},
            "Start":{"date":{"start":start_date.isoformat()}},
            "Day 7":{"date":{"start":day7.isoformat()}},
            "Day 30":{"date":{"start":day30.isoformat()}},
            "Day 60":{"date":{"start":day60.isoformat()}},
            "Day 90":{"date":{"start":day90.isoformat()}},
            "Status":{"select":{"name":"day_0"}},
            "Current milestone":{"select":{"name":"contract_signed"}},
        },
        children=onboarding_template_blocks(motion, tier),  # static page template with checklists
    )
    return page["id"]
```

### Recipe 6: Day-7 kickoff calendar invite

```bash
curl -X POST "https://www.googleapis.com/calendar/v3/calendars/primary/events?conferenceDataVersion=1" \
  -H "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "summary":"Acme × Vendor — Onboarding Kickoff (Day 7)",
    "description":"Onboarding plan: <Notion URL>. Agenda: program overview, certification path, deal-reg + MDF, joint roadmap (if integration).",
    "start":{"dateTime":"2026-06-18T15:00:00Z"},
    "end":{"dateTime":"2026-06-18T16:00:00Z"},
    "attendees":[
      {"email":"sarah@acme.com"},
      {"email":"channelmgr@vendor.com"},
      {"email":"product@vendor.com"}
    ],
    "conferenceData":{"createRequest":{"requestId":"acme-001-kickoff"}}
  }'
```

### Recipe 7: Day-30 review query

```sql
-- Partners hitting Day 30 this week; surface their progress
SELECT op.partner_id, op.partner_name, op.start_date,
       (op.start_date + INTERVAL '30 days')::date AS day_30,
       op.foundation_cert_complete,
       COUNT(DISTINCT acct.id) AS joint_accounts_identified,
       (SELECT COUNT(*) FROM deal_registrations dr WHERE dr.partner_id=op.partner_id) AS first_deal_reg_submitted
FROM onboarding_plans op
LEFT JOIN joint_accounts acct ON acct.partner_id = op.partner_id
WHERE op.start_date BETWEEN NOW() - INTERVAL '32 days' AND NOW() - INTERVAL '28 days'
GROUP BY op.partner_id, op.partner_name, op.start_date, op.foundation_cert_complete;
```

Pipe to channel manager via Slack `#onboarding-reviews`.

### Recipe 8: Day-30 review checklist (in Slack canvas)

```python
def post_day30_checklist(partner_id):
    blocks = [
        {"type":"header","text":{"type":"plain_text","text":f"Day-30 Review — {partner_id}"}},
        {"type":"section","text":{"type":"mrkdwn","text":"Run with: channel manager + partner primary contact (30 min)"}},
        {"type":"divider"},
        {"type":"section","text":{"type":"mrkdwn","text":(
            "*Checklist:*\n"
            ":black_square: Foundation cert complete?\n"
            ":black_square: First joint-account list identified (≥ 10 accounts)?\n"
            ":black_square: First deal-reg submitted?\n"
            ":black_square: Weekly sync established?\n"
            ":black_square: Friction points captured?\n"
        )}},
    ]
    slack_chat_post(f"#partner-{partner_id}", blocks=blocks)
```

### Recipe 9: Day-60 + Day-90 review fires

```python
def schedule_review_fires(partner_id, start_date):
    schedule_at(start_date + timedelta(days=30),
                lambda: post_day30_checklist(partner_id) and trigger_review_call(partner_id, 30))
    schedule_at(start_date + timedelta(days=60),
                lambda: post_day60_checklist(partner_id) and trigger_review_call(partner_id, 60))
    schedule_at(start_date + timedelta(days=90),
                lambda: trigger_day90_scorecard(partner_id) and tier_eligibility_check(partner_id))
```

### Recipe 10: Day-90 scorecard generation + tier check

```python
def trigger_day90_scorecard(partner_id):
    # Hand off to partner-scorecard-authoring skill
    publish_event("partner-scorecard-authoring.generate", {
        "partner_id": partner_id, "context": "onboarding-day-90",
        "compare_to": "onboarding_targets",
    })

def tier_eligibility_check(partner_id):
    metrics = warehouse_query("""
      SELECT
        (SELECT COUNT(*) FROM partner_certifications WHERE partner_id=%s AND status='active') AS certs,
        (SELECT COUNT(*) FROM deal_registrations WHERE partner_id=%s AND status IN ('approved','closed_won')) AS deals,
        (SELECT COALESCE(SUM(amount),0) FROM opportunities WHERE partner_id=%s AND stage='Closed Won') AS revenue
    """, (partner_id, partner_id, partner_id))[0]
    new_tier = (
        "gold" if metrics["certs"]>=3 and metrics["revenue"]>=500_000 else
        "silver" if metrics["certs"]>=1 and metrics["revenue"]>=100_000 else
        "authorized"
    )
    update_partner_tier(partner_id, new_tier)
    return new_tier
```

### Recipe 11: Cohort retro

```sql
-- Quarterly cohort: partners onboarded same quarter
SELECT
  DATE_TRUNC('quarter', start_date) AS cohort,
  COUNT(*) AS partners_onboarded,
  COUNT(*) FILTER (WHERE foundation_cert_complete AND foundation_cert_at <= start_date + INTERVAL '30 days') AS day30_cert_pass,
  AVG(EXTRACT(EPOCH FROM (first_deal_reg_at - start_date))/86400) AS avg_days_to_first_dealreg,
  COUNT(*) FILTER (WHERE first_closed_won_at <= start_date + INTERVAL '90 days') AS day90_closed_won
FROM onboarding_plans
WHERE start_date >= NOW() - INTERVAL '12 months'
GROUP BY 1 ORDER BY 1 DESC;
```

Render to `xlsx`/`google-sheets` for partner-program leadership.

### Recipe 12: Onboarding template variants by motion

Templates differ by motion:
- **Referral**: Day 7 = portal walkthrough; Day 30 = first lead; Day 90 = first closed-won.
- **Affiliate**: Day 7 = tracking link setup + creatives; Day 30 = first conversion; Day 90 = volume target.
- **Reseller**: Day 7 = certifications path + pricing; Day 30 = first deal-reg; Day 60 = first co-marketing campaign; Day 90 = first closed-won + tier check.
- **Integration**: Day 7 = sandbox + API keys; Day 30 = joint roadmap signed; Day 60 = first beta customer; Day 90 = production launch + joint customer story.
- **OEM**: Day 7 = legal review + technical scoping; Day 30 = joint launch plan; Day 60 = co-build in flight; Day 90 = first joint customer commit.

Store templates in Notion DB; `onboarding_template_blocks(motion, tier)` returns appropriate block tree.

## Examples

### Example 1: Acme reseller-tier silver — full 90-day plan auto-fires

**Goal:** Acme just signed silver-tier reseller agreement; kickoff all subsystems.

**Steps:**
1. PandaDoc envelope signed → webhook fires onto agent.
2. Recipe 1 — Day-0 kickoff runs: welcome email, Slack channel `#partner-acme-001`, CRM tasks for Day 7/30/60/90, Foundation cert enrollment, Notion plan, calendar invite for kickoff.
3. Day 7 — Kickoff call held; Notion plan updated `Current milestone = kickoff_complete`.
4. Day 14 — Foundation cert completed (via Canvas LMS); Notion auto-updates.
5. Day 28 — First joint-account list of 12 accounts; Day-30 review checklist (Recipe 8) posts to Slack channel.
6. Day 30 — Review call held; partner's first deal-reg submitted Day 32 (within target).
7. Day 60 — First co-marketing webinar scheduled (hand-off to `partner-led-webinars-events`).
8. Day 90 — Scorecard auto-generated (Recipe 10); tier-eligibility check confirms silver; QBR scheduled.

**Result:** Acme reaches Day-90 with foundation cert + first deal-reg + first webinar — strongest cohort cohort outcome.

### Example 2: Integration partner Globex — joint roadmap signed Day 30

**Goal:** Globex (integration partner) onboarding focuses on roadmap + sandbox.

**Steps:**
1. Recipe 1 — Day 0 fires with `motion=integration`; template includes sandbox provisioning + joint roadmap kickoff.
2. Day 7 — Sandbox access provisioned; Globex eng team given API keys.
3. Day 14 — First joint design review (cross-agent: `product-manager`).
4. Day 30 — Joint integration roadmap signed (`integration-roadmap-planning` skill); Notion DB updated.
5. Day 60 — First beta customer onboarded.
6. Day 90 — Production launch; first joint customer story drafted.

**Result:** Integration shipped within 90 days; joint customer story in flight for Q+1 marketing.

### Example 3: Cohort retro reveals Day-30 bottleneck

**Goal:** Q2 onboarding cohort retro identifies onboarding friction.

**Steps:**
1. Recipe 11 — Cohort SQL surfaces avg-days-to-first-deal-reg = 47 (target = 35).
2. Surface to onboarding-cohort retro Notion DB.
3. Survey 12 cohort partners on friction.
4. Top complaint: "Day-7 kickoff call too generic; didn't address our motion-specific questions."
5. Recipe 12 — Motion-specific templates rolled out for Q3 cohort.
6. Q3 cohort hits target avg-days-to-first-deal-reg = 31.

**Result:** Cohort retro → template iteration → measurable improvement.

## Edge cases / gotchas

- **Generic kickoff fails** — bores integration partners; confuses referral partners. Use motion-specific templates (Recipe 12).
- **Day-30 milestone vague** — quantitative gates only: cert + N joint accounts + first deal-reg.
- **Channel manager bandwidth** — one CM per 15-20 partners; > 25 = quality drops.
- **LMS enrollment / sandbox delays** — Canvas SSO + eng backlog may block Day-7; pre-provision.
- **Partner-side reciprocity** — send "your-team checklist" Day 0; partner onboards their team.
- **Day-30 review fatigue** — offer async checklist + 15-min sync if partner busy.
- **Slack channel decay** — transition onboarding mode → steady-state at Day-60.
- **Tier-eligibility surprise** — surface tier-trajectory at Day-60 for course-correction.
- **Onboarding KPI gaming** — forcing low-quality first deal-reg by Day 30. Filter: % converting to opp.
- **First-customer-story rushed** — Day-90 push without customer ready hurts relationship; defer to Day-180.

## Sources

- Partnerstack onboarding: https://partnerstack.com/blog/partner-onboarding
- Allbound onboarding checklist: https://www.allbound.com/blog/partner-onboarding-checklist
- Impartner onboarding: https://www.impartner.com/blog/partner-onboarding
- Canvas LMS API: https://canvas.instructure.com/doc/api/
- HubSpot Tasks API: https://developers.hubspot.com/docs/api/crm/objects/tasks
