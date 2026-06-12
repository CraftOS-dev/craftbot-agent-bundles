<!--
Source: https://docs.vitally.io/reference/projects + https://help.gainsight.com/docs/journey-orchestrator/ + https://help.catalyst.io/ + https://developers.pendo.io/ + https://docs.userpilot.com/
-->
# Customer Onboarding — Day 0/7/30/60/90 — SKILL

Run the structured Day 0 -> Day 90 onboarding playbook end-to-end: create a CSP project with milestones, wire PostHog event triggers, schedule kickoff + check-ins via Calendly, send milestone emails via Gmail, enroll the customer into in-product onboarding flows (Pendo/Userpilot/Appcues), and roll status back to CSM dashboards. Covers Vitally (modern SaaS), Catalyst/Totango (enterprise), Gainsight (enterprise heavy), and a Notion + Calendly + gmail-mcp + posthog-mcp fallback for no-CSP shops.

## When to use

- **New customer just signed** — Day 0 kickoff needs to fire within 24h.
- **Onboarding is slipping** — TTFV > 14d, missed Day 30 activation gate.
- **Switching to outcomes-led onboarding** — moving away from feature-tour checklists toward business-outcome milestones.
- **Rolling new tier into onboarding** — Enterprise customers get a different cadence than Starter.
- **Recovering a stalled onboarding** — customer signed but champion went dark in week 2.

This skill **complements** `success-plan-goals-milestones` (this skill schedules + tracks; that skill drafts the outcomes) and `ramp-to-value-tracking` (this skill triggers TTFV measurement).

Trigger phrases: "onboard this customer", "Day 0 kickoff", "Day 30 activation", "Day 90 health check", "onboarding plan", "kickoff call".

## Setup

```bash
# Vitally (modern CSP - SOTA for SaaS)
export VITALLY_SUBDOMAIN="acme"
export VITALLY_API_KEY="<key>"

# Catalyst / Totango (enterprise CSP)
export CATALYST_API_KEY="<key>"

# Gainsight (enterprise JO)
export GAINSIGHT_DOMAIN="acme.gainsightcloud.com"
export GAINSIGHT_TOKEN="<key>"

# Pendo / Userpilot / Appcues (in-product flows)
export PENDO_API_KEY="<key>"
export USERPILOT_API_KEY="<key>"
export APPCUES_API_KEY="<key>"

# Calendly + Zoom + Fathom (kickoff hosting)
export CALENDLY_TOKEN="<token>"
export ZOOM_OAUTH_TOKEN="<token>"
export FATHOM_API_KEY="<key>"

# Free fallback path
# notion-mcp + gmail-mcp + posthog-mcp already wired via agent.yaml
```

Workspace prerequisites:
- Stable `customer_id` from CRM mirrored as `external_id` in CSP.
- PostHog event taxonomy includes `signup`, `first_aha_event`, `workspace_setup_complete`, `key_feature_used`.
- Calendly event types: "Day 0 Kickoff", "Day 30 Check-in", "Day 60 Expansion Review", "Day 90 QBR".
- Onboarding plan template in Notion (or CSP if you've got one).

## Common recipes

### Recipe 1: Create Vitally Project (success plan) on signup

```bash
curl -sS -X POST "https://$VITALLY_SUBDOMAIN.rest.vitally.io/resources/accounts/external/$CUSTOMER_ID/projects" \
  -H "Authorization: Basic $(echo -n $VITALLY_API_KEY: | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Onboarding - 90 day plan",
    "description": "Day 0/7/30/60/90 milestones",
    "milestones": [
      {"name": "Day 0 - Kickoff held", "dueDate": "2026-06-11", "owner": "csm"},
      {"name": "Day 7 - First aha event", "dueDate": "2026-06-18", "owner": "customer"},
      {"name": "Day 30 - Activation (adoption score >= 0.4)", "dueDate": "2026-07-11", "owner": "customer"},
      {"name": "Day 60 - Expansion readiness", "dueDate": "2026-08-10", "owner": "csm"},
      {"name": "Day 90 - Health check + QBR scheduled", "dueDate": "2026-09-09", "owner": "csm"}
    ]
  }'
```

Doc: https://docs.vitally.io/reference/projects

### Recipe 2: Notion fallback onboarding plan (no CSP)

Use `notion-mcp create_page` against an "Onboarding Plans" database. Schema: Customer, Plan Tier, Exec Sponsor, Champion, CSM, Signup Date, Day 0 (status), Day 7 (status), Day 30 (status), Day 60 (status), Day 90 (status), Use Case, Outcomes.

```python
# via notion-mcp
notion.create_page(
    parent={"database_id": ONBOARDING_DB_ID},
    properties={
        "Customer": {"title": [{"text": {"content": customer_name}}]},
        "Plan Tier": {"select": {"name": tier}},
        "CSM": {"people": [{"id": csm_user_id}]},
        "Signup Date": {"date": {"start": signup_iso}},
        "Day 0": {"status": {"name": "Not started"}},
        "Day 7": {"status": {"name": "Not started"}},
        # ... etc
    },
)
```

### Recipe 3: Book Day 0 kickoff via Calendly single-use link

```bash
curl -sS -X POST "https://api.calendly.com/scheduling_links" \
  -H "Authorization: Bearer $CALENDLY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "max_event_count": 1,
    "owner": "https://api.calendly.com/event_types/'$KICKOFF_EVENT_TYPE_UUID'",
    "owner_type": "EventType"
  }' | jq -r '.resource.booking_url'
```

Pipe the booking URL into the Day 0 welcome email (Recipe 5). Doc: https://developer.calendly.com/api-docs/

### Recipe 4: Create Zoom meeting for kickoff (when date confirmed)

```bash
curl -sS -X POST "https://api.zoom.us/v2/users/me/meetings" \
  -H "Authorization: Bearer $ZOOM_OAUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Kickoff - '$CUSTOMER_NAME'",
    "type": 2,
    "start_time": "2026-06-13T15:00:00Z",
    "duration": 60,
    "settings": {"join_before_host": false, "auto_recording": "cloud"}
  }' | jq '{join_url, password}'
```

Auto-recording on so Fathom can transcribe (Recipe 11).

### Recipe 5: Schedule the Day 0/7/30/60/90 email cadence (Gmail)

Via `gmail-mcp send_email_scheduled` (or queue 5 jobs in cron). Subject lines that work:

- Day 0: "Welcome to [Product] - let's get you set up"
- Day 7: "[Customer], how's your first week going?"
- Day 30: "30 days in - quick check-in on your outcomes"
- Day 60: "Where you are at Day 60 + what's next"
- Day 90: "Booking your first QBR - quick 15"

Don't generic-greet. Reference the specific outcome from the success plan in every email body.

### Recipe 6: Wire PostHog event trigger for Day 7 first-aha

```sql
-- HogQL cohort: customers who hit first_aha_event within 7 days
SELECT
  properties.customer_id AS customer_id,
  min(timestamp) AS first_aha_at,
  dateDiff('day', properties.signup_at, min(timestamp)) AS ttfv_days
FROM events
WHERE event = 'first_aha_event'
  AND timestamp >= now() - INTERVAL 30 DAY
GROUP BY properties.customer_id
HAVING ttfv_days <= 7
```

Via `posthog-mcp query`. Output -> mark Day 7 milestone complete in Vitally (Recipe 7) for each customer_id.

### Recipe 7: Mark milestone complete in Vitally

```bash
# Find the milestone ID first (one-time)
curl -sS "https://$VITALLY_SUBDOMAIN.rest.vitally.io/resources/projects/$PROJECT_ID" \
  -H "Authorization: Basic $(echo -n $VITALLY_API_KEY: | base64)" | jq '.milestones[]'

# Mark complete
curl -sS -X PUT "https://$VITALLY_SUBDOMAIN.rest.vitally.io/resources/projects/$PROJECT_ID/milestones/$MILESTONE_ID" \
  -H "Authorization: Basic $(echo -n $VITALLY_API_KEY: | base64)" \
  -H "Content-Type: application/json" \
  -d '{"completedAt": "2026-06-18T14:00:00Z"}'
```

### Recipe 8: Enroll customer into Pendo onboarding guide

```bash
curl -sS -X POST "https://app.engage.pendo.io/api/v1/segment/$ONBOARDING_SEGMENT_ID/members" \
  -H "X-Pendo-Integration-Key: $PENDO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"visitorIds": ["'$VISITOR_ID'"], "accountIds": ["'$CUSTOMER_ID'"]}'
```

Doc: https://developers.pendo.io/

Userpilot equivalent:
```bash
curl -sS -X POST "https://api.userpilot.io/v1/users/$USER_ID/groups" \
  -H "X-API-KEY: $USERPILOT_API_KEY" \
  -d '{"company_id": "'$CUSTOMER_ID'", "metadata": {"onboarding_cohort": "day_0_90"}}'
```

Appcues equivalent: `POST https://api.appcues.com/v1/audiences/<id>/members` with `user_id`.

### Recipe 9: Catalyst playbook assignment

```bash
curl -sS -X POST "https://api.catalyst.io/v1/playbooks/$PLAYBOOK_ID/assignments" \
  -H "Authorization: Bearer $CATALYST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"company_id": "'$CUSTOMER_ID'", "start_date": "'$SIGNUP_DATE'"}'
```

Doc: https://help.catalyst.io/

### Recipe 10: Gainsight Journey Orchestrator program enrollment

```bash
curl -sS -X POST "https://$GAINSIGHT_DOMAIN/v1/api/journey/program/$PROGRAM_ID/participants" \
  -H "accesskey: $GAINSIGHT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"company_id": "'$CUSTOMER_ID'", "person_id": "'$SPONSOR_ID'"}'
```

Doc: https://help.gainsight.com/docs/journey-orchestrator/

### Recipe 11: Extract Day 0 kickoff action items via Fathom

```bash
# After kickoff, pull transcript
curl -sS "https://api.fathom.video/external/v1/meetings/$MEETING_ID/transcript" \
  -H "X-Api-Key: $FATHOM_API_KEY" | jq -r '.transcript'
```

Pipe transcript to Claude -> extract action items + use case statement -> write back to Vitally project notes via Recipe 1 pattern.

### Recipe 12: Adoption-score Day 30 gate via HogQL

```sql
-- Per-customer adoption score (used to fire Day 30 milestone)
SELECT
  properties.customer_id AS customer_id,
  uniq(case when event = 'user_action' then properties.user_id end) AS active_users,
  uniq(case when event = 'user_action'
            and timestamp >= now() - INTERVAL 7 DAY
            then properties.user_id end) AS wau,
  uniq(case when event = 'user_action'
            and timestamp >= now() - INTERVAL 30 DAY
            then properties.user_id end) AS mau,
  uniq(properties.feature_name) FILTER (WHERE event = 'key_feature_used') AS feature_breadth,
  (uniq(case when event = 'user_action' and timestamp >= now() - INTERVAL 1 DAY then properties.user_id end) * 1.0
   / nullif(uniq(case when event = 'user_action' and timestamp >= now() - INTERVAL 30 DAY then properties.user_id end), 0)) AS dau_mau
FROM events
WHERE timestamp >= now() - INTERVAL 30 DAY
GROUP BY properties.customer_id
```

`dau_mau >= 0.4` AND `feature_breadth >= 3` -> Day 30 milestone complete.

### Recipe 13: Stalled-onboarding watcher (nightly)

```sql
-- Find onboardings where milestone overdue and no recent customer activity
SELECT c.customer_id, c.name, c.csm, m.milestone_name, m.due_date,
       max(e.timestamp) AS last_activity
FROM onboarding_milestones m
JOIN customers c USING (customer_id)
LEFT JOIN events e ON e.properties_customer_id = c.customer_id
WHERE m.completed_at IS NULL
  AND m.due_date < CURRENT_DATE - INTERVAL '3 days'
GROUP BY c.customer_id, c.name, c.csm, m.milestone_name, m.due_date
HAVING max(e.timestamp) < CURRENT_DATE - INTERVAL '7 days';
```

For each row, `slack-mcp chat_postMessage` to `#cs-onboarding-watch` with CSM tagged.

## Examples

### Example 1: End-to-end Day 0 fire on signup webhook

**Goal:** Customer signs up at 10:00 UTC; by 11:00 UTC plan exists in Vitally, kickoff link sent, Pendo enrolled, Slack notified.

**Steps:**
1. Stripe webhook `customer.created` -> agent receives.
2. Recipe 1 (Vitally project) + Recipe 5 (Day 0 welcome email scheduled) + Recipe 8 (Pendo enrollment) -> parallel.
3. Recipe 3 (Calendly single-use kickoff link) -> embed in welcome email body.
4. `slack-mcp` -> #cs-new-customers: "[Customer] signed up; plan created; kickoff link sent."

**Result:** First-touch is consistent, fast, instrumented.

### Example 2: Day 30 activation gate didn't trigger - debug

**Goal:** Customer is on Day 35, milestone still open. Find out why.

**Steps:**
1. Recipe 12 HogQL -> dau_mau = 0.18, feature_breadth = 2. They're not activating.
2. Recipe 11 - re-listen to kickoff transcript: "champion mentioned blockers around SSO." Never resolved.
3. Auto-create Linear issue + Slack escalation to AE for SSO unblock.
4. Send personalized re-onboard email (referencing the SSO blocker, not generic) via `gmail-mcp`.

**Result:** Recovers stalled onboarding before churn risk hardens.

## Edge cases / gotchas

- **External ID drift** — if CRM `customer_id` doesn't match Vitally `external_id`, the project never finds the account. Sync on customer create, audit weekly.
- **Time zones** — milestone due dates in UTC; customer in PT. Day 30 in their world may be Day 31 in yours. Use customer timezone in CSP project metadata.
- **Multi-account customers** — parent + child accounts (HQ + subsidiaries). Decide whether onboarding is per-child or rolled up to parent; mirror in CSP hierarchy.
- **Webhook race condition** — Stripe `customer.created` fires before Vitally has synced the new account. Wait 5 min or retry with exponential backoff.
- **Email cadence storms** — if customer also gets product-marketing nurture emails, Day 0/7 from CSM can collide. Coordinate with marketing-agent before going live.
- **Calendly link expiry** — single-use links expire after 90 days. If kickoff slips, generate fresh link; don't ask customer to use the original.
- **Champion turnover during onboarding** — Day 14, champion leaves the customer org. Flag, multi-thread (executive-sponsor-relationships), re-onboard the replacement.
- **Self-serve customers don't want kickoff calls** — for Starter tier, Day 0 might be in-product Pendo flow + email only. Don't force Calendly.
- **CSP Project name collision** — re-onboarding (year 2 expansion) creates duplicate project; archive old one first.
- **Fathom transcript privacy** — some customers don't allow external recording. Use Granola for local-capture fallback or document plain-text notes.

## Sources

- [Vitally Projects API](https://docs.vitally.io/reference/projects)
- [Vitally REST API overview](https://docs.vitally.io/reference)
- [Catalyst (Totango) playbook docs](https://help.catalyst.io/)
- [Gainsight Journey Orchestrator](https://help.gainsight.com/docs/journey-orchestrator/)
- [Pendo Engage API](https://developers.pendo.io/)
- [Userpilot API](https://docs.userpilot.com/)
- [Appcues REST API](https://help.appcues.com/en/articles/123-appcues-rest-api)
- [Calendly API v2 scheduling links](https://developer.calendly.com/api-docs/)
- [Zoom Meetings API](https://developers.zoom.us/docs/api/meetings/)
- [Fathom API](https://help.fathom.video/en/articles/8430832-fathom-api)
- [PostHog HogQL Query API](https://posthog.com/docs/api/queries)
- [Notion API create page](https://developers.notion.com/reference/post-page)
