<!--
Source: https://developer.statuspage.io/
-->
# Incident Customer Comms — Statuspage — SKILL

Statuspage.io (Atlassian) is the SOTA for public status pages + incident customer comms. This skill drives the full lifecycle: create incident → post Investigating → Identified → Monitoring → Resolved updates → Slack pin → affected-customer email batch. Includes templates aligned with `role.md`'s incident comms playbook.

## When to use

- **Active incident** detected (SEV-1 / SEV-2 / SEV-3) — publish to Statuspage + Slack.
- **Pre-scheduled maintenance** — create a scheduled incident in advance.
- **Per-component impact** — degraded API but Dashboard fine — update the right components.
- **Affected-customer batch email** — enterprise customers within 1h of incident start.
- **Resolved → post-mortem queue** — close incident, queue 5-business-day post-mortem.

Trigger phrases: "create incident", "Statuspage update", "post Identified", "post Resolved", "incident comms".

## Setup

```bash
# Statuspage Manage API
curl -sS "https://api.statuspage.io/v1/pages" \
  -H "Authorization: OAuth $STATUSPAGE_API_KEY" | jq '.[] | {id, name, url}'
```

Auth + env:
- `STATUSPAGE_API_KEY` — at `Statuspage > Manage API > API Keys > Create`. Note: header is `Authorization: OAuth <key>` (NOT `Bearer`).
- `STATUSPAGE_PAGE_ID` — your page UUID (from the call above).
- `STATUSPAGE_COMPONENT_IDS` — cache via `GET /pages/<id>/components` (one-time).

Workspace prerequisites:
- Statuspage page configured with components (API, Dashboard, Auth, Webhooks, etc.).
- Subscribers configured (email / SMS / Twitter).
- Slack `#incidents` channel for cross-posting.

## Common recipes

### Recipe 1: List components (one-time cache)

```bash
curl -sS "https://api.statuspage.io/v1/pages/$STATUSPAGE_PAGE_ID/components" \
  -H "Authorization: OAuth $STATUSPAGE_API_KEY" | jq '.[] | {id, name, status, description}'
```

Statuses: `operational` | `degraded_performance` | `partial_outage` | `major_outage` | `under_maintenance`.

### Recipe 2: Create an incident (Investigating phase)

```bash
curl -sS -X POST "https://api.statuspage.io/v1/pages/$STATUSPAGE_PAGE_ID/incidents" \
  -H "Authorization: OAuth $STATUSPAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "incident":{
      "name":"Elevated API error rates",
      "status":"investigating",
      "impact_override":"major",
      "body":"We are investigating reports of elevated error rates on the API. We will update again within 30 minutes.\n\n— Platform team",
      "component_ids":["'$API_COMPONENT_ID'"],
      "components":{"'$API_COMPONENT_ID'":"partial_outage"},
      "deliver_notifications":true
    }
  }' | jq '{id, name, status, shortlink}'
```

`deliver_notifications: true` triggers email + Twitter + Slack subscriber notifications. `impact_override` is `none|minor|major|critical`.

### Recipe 3: Post Identified update

```bash
curl -sS -X PATCH "https://api.statuspage.io/v1/pages/$STATUSPAGE_PAGE_ID/incidents/$INCIDENT_ID" \
  -H "Authorization: OAuth $STATUSPAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "incident":{
      "status":"identified",
      "body":"We have identified the cause as an issue with our database. A fix is being prepared. ETA 30 minutes.\n\n— Platform team",
      "deliver_notifications":true
    }
  }'
```

### Recipe 4: Post Monitoring update

```bash
curl -sS -X PATCH "https://api.statuspage.io/v1/pages/$STATUSPAGE_PAGE_ID/incidents/$INCIDENT_ID" \
  -H "Authorization: OAuth $STATUSPAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "incident":{
      "status":"monitoring",
      "body":"We have deployed a fix and the system is recovering. We are monitoring closely and will update when fully resolved.\n\n— Platform team",
      "deliver_notifications":true,
      "components":{"'$API_COMPONENT_ID'":"degraded_performance"}
    }
  }'
```

### Recipe 5: Post Resolved update + close

```bash
curl -sS -X PATCH "https://api.statuspage.io/v1/pages/$STATUSPAGE_PAGE_ID/incidents/$INCIDENT_ID" \
  -H "Authorization: OAuth $STATUSPAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "incident":{
      "status":"resolved",
      "body":"This issue has been resolved. We will publish a full post-mortem within 5 business days.\n\n— Platform team",
      "deliver_notifications":true,
      "components":{"'$API_COMPONENT_ID'":"operational"}
    }
  }'
```

### Recipe 6: Scheduled maintenance

```bash
curl -sS -X POST "https://api.statuspage.io/v1/pages/$STATUSPAGE_PAGE_ID/incidents" \
  -H "Authorization: OAuth $STATUSPAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "incident":{
      "name":"Scheduled: Database maintenance (US-East)",
      "status":"scheduled",
      "scheduled_for":"2026-06-15T02:00:00Z",
      "scheduled_until":"2026-06-15T04:00:00Z",
      "scheduled_remind_prior":true,
      "scheduled_auto_in_progress":true,
      "scheduled_auto_completed":false,
      "body":"Routine database maintenance. Brief degraded performance possible.\n\n— Platform team",
      "component_ids":["'$API_COMPONENT_ID'"],
      "components":{"'$API_COMPONENT_ID'":"under_maintenance"}
    }
  }'
```

`scheduled_remind_prior` sends 60-min-before reminder.

### Recipe 7: Slack pin via slack-mcp

```bash
SLACK_MSG=$(mcp tool slack.chat_postMessage \
  --channel '#incidents' \
  --text "INCIDENT: Elevated API error rates — Investigating. https://status.brand.com/incidents/$SHORTLINK")

MSG_TS=$(echo "$SLACK_MSG" | jq -r '.ts')

mcp tool slack.pins_add \
  --channel '$INCIDENTS_CHANNEL' \
  --timestamp "$MSG_TS"
```

Pin survives until you `pins.remove` post-resolution.

### Recipe 8: Affected-customer batch email (enterprise tier)

```bash
# Get enterprise customer emails affected by component
psql -tA -c "SELECT email FROM crm.customers WHERE tier='enterprise' AND uses_component='api'" > affected.txt

# Personalized batch via gmail-mcp
while read email; do
  mcp tool gmail.send \
    --to "$email" \
    --subject "[Incident] Elevated API error rates affecting your account" \
    --body "$(cat <<EOF
Hi $(lookup_first_name $email),

We are currently investigating elevated error rates on the API, which may affect your integration. Current status: investigating, fix in progress.

You can monitor real-time updates at https://status.brand.com/incidents/$SHORTLINK or contact your CSM directly.

We expect to have more information within the next 30 minutes.

— $CSM_NAME
$CSM_EMAIL
EOF
)"
done < affected.txt
```

Personalized for enterprise; don't batch-blast smaller tiers.

### Recipe 9: List active incidents

```bash
curl -sS "https://api.statuspage.io/v1/pages/$STATUSPAGE_PAGE_ID/incidents/active" \
  -H "Authorization: OAuth $STATUSPAGE_API_KEY" | jq '.[] | {id, name, status, created_at, shortlink}'
```

Cron every 15min — if you've forgotten about an open incident, escalate.

### Recipe 10: Add a midstream update (without changing status)

```bash
curl -sS -X POST "https://api.statuspage.io/v1/pages/$STATUSPAGE_PAGE_ID/incidents/$INCIDENT_ID/incident_updates" \
  -H "Authorization: OAuth $STATUSPAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "incident_update":{
      "body":"Update: most users should now see normal performance. We are continuing to monitor.\n\n— Platform team",
      "deliver_notifications":true
    }
  }'
```

Use for "30-minute promise" updates without changing the incident state.

### Recipe 11: Component status update (no incident)

```bash
curl -sS -X PATCH "https://api.statuspage.io/v1/pages/$STATUSPAGE_PAGE_ID/components/$COMPONENT_ID" \
  -H "Authorization: OAuth $STATUSPAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"component":{"status":"degraded_performance"}}'
```

Used for brief incidents not warranting a full Statuspage incident page.

### Recipe 12: Post-mortem queueing

```bash
# After Recipe 5 (resolved):
DURATION_MIN=$(( ($(date -u +%s) - $(date -u -d "$INCIDENT_STARTED_AT" +%s)) / 60 ))

curl -sS -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -d '{
    "parent":{"database_id":"'$POSTMORTEM_DB_ID'"},
    "properties":{
      "Title":{"title":[{"text":{"content":"[SEV-2] Elevated API error rates"}}]},
      "Status":{"status":{"name":"Draft Required"}},
      "Severity":{"select":{"name":"SEV-2"}},
      "Duration (min)":{"number":'$DURATION_MIN'},
      "Statuspage URL":{"url":"https://status.brand.com/incidents/'$SHORTLINK'"},
      "Due":{"date":{"start":"'$(date -u -d "+5 days" +%Y-%m-%d)'"}}
    }
  }'
```

Schedules the 5-business-day post-mortem.

## Examples

### Example 1: SEV-2 incident — full lifecycle

**Goal:** API errors detected; communicate transparently through resolution.

**Steps (timeline):**
1. T+0min: Sentry alert fires. On-call confirms incident.
2. T+15min: Recipe 2 — create incident `Investigating` + Recipe 7 Slack pin.
3. T+15min: Recipe 8 — email enterprise affected customers.
4. T+45min: Root cause found. Recipe 3 — post `Identified`.
5. T+90min: Fix deployed. Recipe 4 — post `Monitoring`.
6. T+120min: Stable. Recipe 5 — post `Resolved` + `pins_remove`.
7. T+120min: Recipe 12 — queue post-mortem in Notion.
8. T+5business-days: post-mortem published (separate workflow).

**Result:** Transparent comms; enterprise customers feel attended-to; engineering has post-mortem on the calendar.

### Example 2: Scheduled maintenance

**Goal:** Pre-announce planned 2h DB maintenance.

**Steps:**
1. T-48h: Recipe 6 creates scheduled incident.
2. T-1h: Statuspage auto-reminds subscribers.
3. T+0min: Recipe 11 marks component `under_maintenance`; auto-update fires from `scheduled_auto_in_progress`.
4. T+2h: Recipe 11 marks component `operational`; close incident.
5. T+2h: Slack post-maintenance summary.

**Result:** Predictable customer expectations; no surprise downtime.

## Edge cases / gotchas

- **Authorization header uses `OAuth`, not `Bearer`** — common 401. `Authorization: OAuth $STATUSPAGE_API_KEY`.
- **Rate limit: 60 req/min** — burst protection on mass-update operations. Pace incident-list polls.
- **`impact_override` is sticky** — once set, you must explicitly change it; otherwise it persists across updates.
- **Component status drift** — if components show `partial_outage` but no active incident references them, customers see a confusing page. Always tie component status to an incident or revert.
- **Subscribers only notified on `deliver_notifications: true`** — easy to forget; subscribers may miss a critical update.
- **`scheduled_auto_in_progress` and `scheduled_auto_completed`** — convenient but the auto-update body is a default. Override with custom `body` if branding matters.
- **Twitter integration deprecated 2024** — Statuspage's Twitter posting was disabled when X changed API pricing. Use Slack / Discord instead.
- **Statuspage page subdomain** — `status.brand.com` requires DNS CNAME + verification. URL shortlinks (`https://stspg.io/abc`) work without setup.
- **Don't use scheduled incidents for unscheduled ones** — converting status `scheduled` → `investigating` doesn't trigger the right notification cascade.
- **Component impacts cascade** — marking a parent component `major_outage` may not auto-set children. Update children explicitly.
- **Affected-customer email at scale** — for 100+ enterprise customers, batch with rate limits (Gmail: 250 msgs/sec for paid Workspace).
- **Post-mortem template** — see `role.md` post-mortem playbook for the structured template.

## Sources

- [Statuspage Manage API docs](https://developer.statuspage.io/)
- [Statuspage incidents endpoint](https://doers.statuspage.io/api/v1/incidents/)
- [Different APIs under Statuspage (Atlassian support)](https://support.atlassian.com/statuspage/docs/what-are-the-different-apis-under-statuspage/)
- [Statuspage Postman collection](https://www.postman.com/api-evangelist/statuspage/documentation/a3hnv5a/statuspage-io)
- [incident.io status pages comparison](https://incident.io/status-pages)
