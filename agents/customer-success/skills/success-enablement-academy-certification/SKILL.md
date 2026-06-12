<!--
Source: https://help.skilljar.com/hc/en-us/categories/200182230 + https://www.northpass.com/ + https://www.workramp.com/ + https://www.intellum.com/
-->
# Success Enablement — Customer Academy / Certification — SKILL

Stand up + operate customer academy + certification: Skilljar (SOTA), Northpass, WorkRamp, Intellum. Enrollment on milestone trigger, completion webhook -> CSP trait writeback, certification gates feature adoption. Free fallback: Notion + Loom-recorded lessons + Calendly for live training.

## When to use

- **Stand up customer academy** — net-new program.
- **Milestone-triggered enrollment** — Day 7 -> Onboarding 101 course.
- **Feature-launch curriculum** — new product, new lesson set.
- **Certification gate** — admin features require admin cert.
- **Track completion** — per-customer course completion fed into health score.
- **Free fallback academy** — no LMS budget; Notion + Loom.

This skill **complements** `customer-onboarding-day-0-90` (which fires academy enrollment as Day 7 milestone) and `customer-health-scoring-vitally-catalyst-churnzero` (training-adoption trait feeds score).

Trigger phrases: "customer academy", "academy", "certification", "Skilljar", "Northpass", "course enrollment", "training", "LMS".

## Setup

```bash
# Skilljar (SOTA)
export SKILLJAR_API_KEY="<key>"
export SKILLJAR_DOMAIN="acme.skilljar.com"

# Northpass (alt)
export NORTHPASS_API_KEY="<key>"

# WorkRamp (sales + customer enablement)
export WORKRAMP_API_KEY="<key>"

# Intellum (enterprise)
export INTELLUM_API_KEY="<key>"

# Loom for free-fallback recorded lessons
export LOOM_API_KEY="<key>"
```

Workspace prerequisites:
- Skilljar courses configured: "Onboarding 101", "Admin Certification", "Advanced Workflow", per product.
- Notion fallback "Academy" database with: Course, Lesson, Loom URL, Duration, Audience Tier.
- CSP trait: `academy_courses_completed` (number), `is_certified_admin` (boolean).
- Calendly event type "Live Training - 60min" for fallback live sessions.

## Common recipes

### Recipe 1: Enroll customer in Skilljar course

```bash
curl -sS -X POST "https://api.skilljar.com/v1/published-courses/$COURSE_ID/registrations" \
  -H "Authorization: Token $SKILLJAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "'$USER_EMAIL'",
    "first_name": "'$FIRST_NAME'",
    "last_name": "'$LAST_NAME'",
    "send_welcome_email": true
  }'
```

Doc: https://help.skilljar.com/hc/en-us/categories/200182230

### Recipe 2: Pull completion data

```bash
# All completions in last 7 days
curl -sS "https://api.skilljar.com/v1/users?since=$(date -u -d '7 days ago' +%FT%T)" \
  -H "Authorization: Token $SKILLJAR_API_KEY" \
  | jq '.results[] | {email, courses_completed, certificates_earned}'
```

### Recipe 3: Webhook handler for course completion

Skilljar fires webhook on completion. Handler:

```python
@app.route("/webhook/skilljar", methods=["POST"])
def skilljar_webhook():
    event = request.json
    if event["event_type"] == "course.completed":
        email = event["data"]["email"]
        course_id = event["data"]["course_id"]
        customer_id = lookup_customer_by_email(email)

        # Update CSP trait
        push_vitally_trait(customer_id, {
            "academy_courses_completed": +1,
            "last_course_completed": course_id,
            "last_course_completed_at": event["data"]["completed_at"],
        })

        # Notion log
        notion.create_page(...)
```

### Recipe 4: Northpass enrollment alt

```bash
curl -sS -X POST "https://api.northpass.com/v2/students" \
  -H "Authorization: Bearer $NORTHPASS_API_KEY" \
  -d '{
    "email": "'$USER_EMAIL'",
    "name": "'$NAME'",
    "course_id": "'$COURSE_ID'"
  }'
```

Doc: https://www.northpass.com/

### Recipe 5: WorkRamp enrollment alt

```bash
curl -sS -X POST "https://api.workramp.com/v1/learners/enrollments" \
  -H "Authorization: Bearer $WORKRAMP_API_KEY" \
  -d '{
    "email": "'$USER_EMAIL'",
    "academy_id": "'$ACADEMY_ID'",
    "path_id": "'$PATH_ID'"
  }'
```

### Recipe 6: Intellum enterprise alt

```bash
curl -sS -X POST "https://api.intellum.com/v1/users/$USER_ID/enrollments" \
  -H "Authorization: Bearer $INTELLUM_API_KEY" \
  -d '{"course_id": "'$COURSE_ID'"}'
```

### Recipe 7: Notion fallback academy

If no LMS budget, Notion DB stands in:

```python
# Course catalog page (Notion)
notion.create_page(
    parent={"database_id": ACADEMY_DB_ID},
    properties={
        "Course": {"title": [{"text": {"content": "Onboarding 101"}}]},
        "Audience": {"multi_select": [{"name": "All tiers"}]},
        "Duration": {"number": 45},  # minutes
        "Loom URL": {"url": "https://www.loom.com/share/abc123"},
        "Description": {"rich_text": [{"text": {"content": "Get up and running in 45 min..."}}]},
    },
    children=[
        {"object": "block", "type": "embed", "embed": {"url": "https://www.loom.com/embed/abc123"}},
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "What you'll learn"}}]}},
        # ... lesson outline
    ],
)
```

Enrollment = Notion page sent via gmail-mcp. Completion = customer replies "done" (manual track).

### Recipe 8: Milestone-triggered enrollment

Tied to `customer-onboarding-day-0-90` Day 7 milestone:

```python
# Day 7 fires; enroll customer in Onboarding 101
def on_day7_milestone(customer):
    for user in customer.users:
        Recipe 1 enroll user in COURSE_ID_ONBOARDING_101
    gmail.send_email(
        to=customer.champion.email,
        subject=f"Day 7 - your team's training is unlocked",
        body=f"Your team is enrolled in Onboarding 101. Check inbox for the welcome from {LMS_VENDOR}."
    )
```

### Recipe 9: Certification gate enforcement

```sql
-- Customers whose admin user isn't certified
SELECT c.customer_id, c.name, u.email AS admin_email
FROM customers c
JOIN users u ON u.customer_id = c.customer_id AND u.role = 'admin'
LEFT JOIN academy_completions ac ON ac.user_id = u.user_id AND ac.course_id = ADMIN_CERT_COURSE_ID
WHERE c.tier = 'Enterprise'
  AND ac.user_id IS NULL;
```

For each: Recipe 1 enroll admin in admin cert; gate access to admin features at backend until cert complete (engineering implementation, not agent).

### Recipe 10: Certification badge / LinkedIn share

```bash
# After cert, email user with LinkedIn share link
gmail.send_email(
    to=[user.email],
    subject=f"You're certified! Share on LinkedIn?",
    body=f"""
Congrats on completing Admin Certification for {product}.

Want to share? Here's a one-click LinkedIn add: {linkedin_cert_share_url}

Or download badge: {badge_png_url}
"""
)
```

### Recipe 11: Quarterly academy performance report

```sql
SELECT
  course_id,
  course_name,
  count(*) AS enrolled,
  count(*) FILTER (WHERE completed_at IS NOT NULL) AS completed,
  100.0 * count(*) FILTER (WHERE completed_at IS NOT NULL) / count(*)::numeric AS completion_pct,
  percentile_cont(0.5) WITHIN GROUP (ORDER BY (completed_at - enrolled_at)) AS p50_time_to_complete
FROM academy_enrollments
WHERE enrolled_at >= now() - INTERVAL '90 days'
GROUP BY course_id, course_name
ORDER BY completion_pct DESC;
```

### Recipe 12: Cross-link academy completion to health score

```python
# Daily Postgres -> CSP trait update
trained_users_pct = postgres.query(f"""
  SELECT customer_id,
         count(DISTINCT u.user_id) FILTER (WHERE ac.user_id IS NOT NULL) * 1.0
         / count(DISTINCT u.user_id) AS pct_trained
  FROM customers c
  JOIN users u USING (customer_id)
  LEFT JOIN academy_completions ac ON ac.user_id = u.user_id
  GROUP BY customer_id
""")

for row in trained_users_pct:
    push_vitally_trait(row.customer_id, {"academy_adoption_pct": row.pct_trained})
```

### Recipe 13: Live training fallback (Calendly + Loom)

Recipe 7 Notion academy + Calendly for live cohort sessions:

```bash
curl -sS -X POST "https://api.calendly.com/scheduling_links" \
  -d '{"max_event_count": 1, "owner": "https://api.calendly.com/event_types/'$LIVE_TRAINING_EVENT'"}'
```

After session, Loom-record + add to Notion academy DB as new lesson.

## Examples

### Example 1: Stand up Skilljar academy from scratch

**Goal:** Customer academy live in 30 days.

**Steps:**
1. Week 1: Course inventory (Onboarding 101, Admin Cert, Advanced).
2. Week 2: Record lessons via Loom; upload to Skilljar.
3. Week 2: Configure Skilljar courses + cert workflow.
4. Week 3: Configure webhook (Recipe 3); Postgres `academy_enrollments` table.
5. Week 4: Wire `customer-onboarding-day-0-90` Day 7 -> Recipe 1.
6. Week 4: Recipe 12 trait writeback live.

**Result:** Academy live, integrated with health score.

### Example 2: Notion fallback for low-volume

**Goal:** No LMS budget; serve 50 customers with Notion + Loom.

**Steps:**
1. Recipe 7 create courses in Notion DB.
2. Loom-record each lesson.
3. Milestone trigger (Day 7): gmail-mcp sends Notion course link.
4. Manual completion track in Notion: customer marks "Done" via shared form.
5. Recipe 12 writeback monthly (not daily; low volume).

**Result:** Academy delivered without LMS cost.

## Edge cases / gotchas

- **SSO friction** — Skilljar SSO with customer's IdP often requires setup; without it, customer manages separate login. Some customers won't accept that.
- **Cert-gate enforcement requires engineering** — backend must check cert before showing admin features. Agent flags; eng implements.
- **Completion tracking via webhook reliability** — webhook drops -> CSP trait stale. Daily reconciliation via Recipe 2 polling.
- **Multiple LMSs per customer base** — some customers self-host content (their own LMS). Don't force yours; offer SCORM export.
- **Lesson freshness** — product UI changes, Loom-recorded lessons go stale. Quarterly audit.
- **Free-tier Skilljar limits** — Skilljar has paid-only enterprise features (SSO, SAML); plan accordingly.
- **Cert expiry** — Admin Cert good for 2 years? Or perpetual? Document; renew via email reminder.
- **Cert credentials** — customer wants resume-worthy credential. LinkedIn add-to-profile is value add; ensure cert badge meta is correct.
- **Notion fallback at scale** — > 200 customers in Notion academy = ugly. Migrate to LMS.
- **Webhook signature verification** — Skilljar webhooks signed; verify before processing to avoid spoofed completion events.
- **Per-user vs per-customer enrollment** — academy is per-user; cert is per-user. Customer health rolls up; align which metric drives.
- **Language / locale** — single-language academy excludes non-English customers. Use DeepL for course transcripts; cap effort by tier.

## Sources

- [Skilljar API docs](https://help.skilljar.com/hc/en-us/categories/200182230)
- [Skilljar enrollment API](https://help.skilljar.com/hc/en-us/articles/360001268807-Skilljar-API)
- [Northpass API docs](https://www.northpass.com/)
- [WorkRamp API](https://www.workramp.com/)
- [Intellum API](https://www.intellum.com/)
- [Loom API docs](https://dev.loom.com/)
- [Calendly scheduling API](https://developer.calendly.com/api-docs/)
- [SCORM compliance overview](https://scorm.com/scorm-explained/)
- [Customer education ROI (Forrester)](https://www.forrester.com/blogs/?contextual_tags=customer+education)
- [Notion API](https://developers.notion.com/)
