<!--
Sources: https://incident.io/ , https://www.pagerduty.com/products/process-automation/
Operational runbooks in Notion/Slab. Incident runbooks via PagerDuty Process Automation, Incident.io, Statuspage / Better Stack.
Post-mortem template per Google SRE (blameless).
-->
# Runbook Authoring — Operational + Incident — SKILL

Author and maintain two flavors of runbooks: **operational** (recurring task — "how to run the weekly KPI digest") and **incident** (scenario — "what to do when production database fails over"). Includes post-mortem framework (Google SRE blameless), status-page playbook, severity definitions, on-call rotation hygiene.

## When to use

- New service / new ops process needs a written runbook.
- Post-incident — produce post-mortem + update runbook.
- On-call rotation needs starter set of runbooks.
- SOC 2 / ISO 27001 audit on incident response.
- Trigger phrases: "runbook", "incident", "post-mortem", "blameless retro", "on-call", "SEV-1", "PagerDuty", "Incident.io", "status page".

## Setup

```bash
export PAGERDUTY_TOKEN="xxx"      # https://developer.pagerduty.com
export INCIDENT_IO_TOKEN="xxx"    # https://api.incident.io
export STATUSPAGE_TOKEN="xxx"
export NOTION_TOKEN="xxx"
export SLACK_BOT_TOKEN="xxx"
```

## Common recipes

### Recipe 1: Operational runbook template
```markdown
# Runbook: <Process>

## Metadata
- Owner: @<owner>
- Backup: @<backup>
- Frequency: Daily / Weekly / Monthly / Quarterly / Ad-hoc
- Last reviewed: 2026-07-01 (v2026.07)
- Estimated time: 30 min

## Purpose
1-2 sentences on the outcome.

## Prerequisites
- Account access: list
- Tools: list (with versions / config)
- Inputs needed: list
- Working day window: e.g., "Mon-Fri 09-17 ET only"

## Steps
1. Step 1 — `command/screenshot/exact action`
2. Step 2 — ...
3. Step 3 — ...

## Verification
- Expected output: [what to look for]
- Verify command: `<command>`
- Smoke-test: e.g., visit URL, confirm `200`

## Common failure modes
| Symptom | Cause | Fix |
|---------|-------|-----|
| API 429 | Rate-limited | Sleep 30s + retry |
| Slack 401 | Token rotated | Refresh from Vault |

## Escalation
- If stuck > 30 min, page secondary on-call.
- If > 1h, declare incident; see Recipe 4 (incident runbook).

## Change log
- v2026.07 — initial
- v2026.08 — added Step 4 for new vendor
```

### Recipe 2: Incident runbook template
```markdown
# Incident Runbook: <Scenario>

## Triggers
- Alert: <alert_name>
- Symptoms: <user-visible behavior>

## Severity
- SEV-1 if: complete outage, data loss, security breach
- SEV-2 if: partial outage, paying customer affected
- SEV-3 if: degraded but workable
- SEV-4 if: cosmetic

## Mitigation steps (try in order)
1. **Stop bleeding first.** Throttle / disable feature flag / revert deploy.
2. **Communicate.** Status page → "Investigating" within 15 min.
3. **Diagnose.** Run `<command>` for breadcrumbs. Check `<dashboard>`.
4. **Common causes (try first):**
   - Recent deploy: revert last (Recipe X)
   - Database failover: promote replica (Recipe X)
   - Vendor outage: switch fallback (Recipe X)
5. **Escalation tree:**
   - 30 min unresolved → page secondary
   - 60 min unresolved → CTO
   - 90 min unresolved → CEO + comms

## Comms cadence
- T+0: Declare in #incident-room; status page → Investigating
- T+15min: First update
- T+30min: Update
- T+1h: Severity confirmation; update plan
- T+resolved: Status page → resolved; schedule post-mortem within 5 days

## Post-mortem
- Use Recipe 6.
- Owner: IC
- Due: 5 business days
```

### Recipe 3: Notion DB structure for runbooks
```yaml
# Runbooks DB schema
properties:
  Name: title
  Type: select [Operational, Incident]
  Owner: people
  Frequency: select [Daily, Weekly, Monthly, Quarterly, Ad-hoc, Scenario]
  Last Reviewed: date
  Version: rich_text
  Severity: select [SEV-1, SEV-2, SEV-3, SEV-4, N/A]
  System: multi_select [API, DB, Auth, Search, Payments, ...]
  Status: select [Draft, Live, Archived]
  Estimated Time Min: number
```

### Recipe 4: PagerDuty service + escalation policy
```bash
# Create service tied to incident-room channel
curl -s -X POST "https://api.pagerduty.com/services" \
  -H "Authorization: Token token=$PAGERDUTY_TOKEN" \
  -H "Accept: application/vnd.pagerduty+json;version=2" \
  -H "Content-Type: application/json" \
  -d '{
    "service":{
      "name":"production-api",
      "escalation_policy":{"id":"<policy>","type":"escalation_policy_reference"},
      "alert_creation":"create_incidents",
      "auto_resolve_timeout":1800,
      "acknowledgement_timeout":600
    }
  }'

# Escalation policy
curl -s -X POST "https://api.pagerduty.com/escalation_policies" \
  -H "Authorization: Token token=$PAGERDUTY_TOKEN" \
  -d '{
    "escalation_policy":{
      "name":"production-on-call",
      "escalation_rules":[
        {"escalation_delay_in_minutes":10,"targets":[{"id":"<primary>","type":"user_reference"}]},
        {"escalation_delay_in_minutes":15,"targets":[{"id":"<secondary>","type":"user_reference"}]},
        {"escalation_delay_in_minutes":30,"targets":[{"id":"<cto>","type":"user_reference"}]}
      ]
    }
  }'
```

### Recipe 5: Incident.io — declare incident
```bash
curl -s -X POST "https://api.incident.io/v2/incidents" \
  -H "Authorization: Bearer $INCIDENT_IO_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "name":"Production API elevated 5xx",
    "summary":"5xx error rate > 5% on /api/v1/*",
    "severity_id":"<sev1>",
    "incident_type_id":"<production-impact>",
    "status_category":"investigating",
    "mode":"standard"
  }'
```

### Recipe 6: Post-mortem template (Google SRE blameless)
```markdown
# Post-Mortem: <Incident name>

## Metadata
- Incident ID: INC-2026-0042
- Date: 2026-07-08
- IC: @alex
- Severity: SEV-1
- Duration: 2h 14m (09:30 - 11:44 UTC)
- Customers affected: ~12,000
- Revenue impact (est.): $X
- Author: @<author>

## Summary (1 paragraph)
What happened, in plain language.

## Impact
- Customers affected: [%, count, key accounts]
- Revenue impact: [$ + methodology]
- Data loss: [bytes / rows / none]
- Customer-trust impact: [tickets opened, social mentions]
- Internal hours: [people × hours]

## Timeline (UTC)
- 09:00 — Deploy v2.45.1 to production
- 09:25 — Datadog alert: 5xx rate climbing
- 09:30 — IC declared; #inc-2026-0042 created
- 09:34 — Status page → Investigating
- 09:48 — Root cause identified: DB index missing on new schema
- 10:05 — Revert deploy
- 10:12 — Error rate falling
- 11:44 — All clear; status page → Resolved

## Root cause
[Single sentence, then 1-2 paragraphs of detail. Multiple causes if true.]

## What went well
- Detection was fast (Datadog alert fired in 25 min)
- IC declaration + comms cadence held
- Status page updates were timely

## What went poorly
- Deploy went out without pre-prod migration test
- First customer email took 2h (template missing)
- On-call secondary not paged correctly (PagerDuty policy gap)

## What we got lucky with
- It was 09:30 (low traffic); had it been 14:00, impact 4x

## Action items
| ID | Owner | Action | Due | Type |
|----|-------|--------|-----|------|
| AI-01 | @bob | Add pre-prod migration test gate to CI | 2026-07-22 | Prevent |
| AI-02 | @maria | Author customer-incident-email template | 2026-07-15 | Improve |
| AI-03 | @alex | Fix PagerDuty escalation rule for sec on-call | 2026-07-12 | Fix |
| AI-04 | @sam | Add DB-index lint to schema CI | 2026-07-29 | Prevent |

## Lessons learned
[Reflective; what's the systemic takeaway, not just the surface bug.]

## Appendix
- Datadog dashboards: [links]
- Slack incident-room export: [link]
- Customer comms drafts: [link]
```

### Recipe 7: Status page incident lifecycle
```bash
# Investigating
curl -s -X POST "https://api.statuspage.io/v1/pages/<page>/incidents" \
  -H "Authorization: OAuth $STATUSPAGE_TOKEN" \
  -d "incident[name]=Elevated API errors" \
  -d "incident[status]=investigating" \
  -d "incident[impact_override]=major"

# Identified
curl -s -X PATCH "https://api.statuspage.io/v1/pages/<page>/incidents/<inc>" \
  -H "Authorization: OAuth $STATUSPAGE_TOKEN" \
  -d "incident[status]=identified" \
  -d "incident[body]=Root cause identified — DB index missing. Reverting deploy."

# Monitoring → Resolved
curl -s -X PATCH "https://api.statuspage.io/v1/pages/<page>/incidents/<inc>" \
  -d "incident[status]=resolved"
```

### Recipe 8: On-call rotation hygiene
```yaml
rotation_principles:
  - Primary + secondary always; never single-person
  - Max shift length: 1 week
  - Handoff window: 30 min overlap
  - PTO blackout: on-call cannot be on PTO; swap or move
  - Compensation: $250 weekly stipend + 0.5 day comp time per page
  - Post-on-call: 1 day light schedule
  - Page volume cap: > 5 pages / shift → quarterly review
  - Runbook coverage: every page-able alert must have a runbook (Recipe 2)
```

### Recipe 9: Incident comms template (customer email)
```markdown
Subject: Service incident — [resolved] — [date]

Hi <customer>,

Between <time> and <time> UTC on <date>, you may have experienced [X behavior].
We declared an incident, identified the root cause within <Y> minutes, and resolved by <time>.

What happened: <plain language, no jargon>
What we're doing to prevent this: <action items, in plain language>
What you can do: <usually nothing; or "review billing for double-charges" if applicable>

We're sorry. If your team was materially affected, please reach out and we'll work on it together.

Status page: https://status.<co>.com

— <on-call manager> + <CEO if SEV-1>
```

### Recipe 10: Runbook discoverability — alert → runbook link
```yaml
# In Datadog / Grafana / Sentry — every alert annotates with runbook URL
alert:
  name: "API 5xx > 5%"
  runbook_url: "https://notion.so/<co>/runbooks/api-5xx-spike"
  severity: SEV-2
  page_target: production-api  # PagerDuty service
```

### Recipe 11: Runbook freshness sweep
```python
# Same as KB stale sweep but tagged for runbooks
import datetime, requests, os
HEADER = {'Authorization': f"Bearer {os.environ['NOTION_TOKEN']}", 'Notion-Version':'2022-06-28'}
stale = requests.post(f"https://api.notion.com/v1/databases/<runbooks-db>/query",
    headers=HEADER, json={
        'filter':{'and':[
            {'property':'Status','select':{'equals':'Live'}},
            {'property':'Last Reviewed','date':{'before': (datetime.date.today() - datetime.timedelta(days=180)).isoformat()}}
        ]}
    }).json()
# Slack DM owners
```

## Examples

### Example 1: Stand up on-call + first 10 runbooks
**Goal:** Launch PagerDuty rotation for 5-engineer team.
**Steps:**
1. Recipe 4 service + policy.
2. Recipe 8 rotation policy doc.
3. Inventory page-able alerts; Recipe 2 runbook per alert.
4. Recipe 10 annotate alerts with runbook URLs.
5. Recipe 11 weekly freshness sweep.
6. Tabletop drill (per `business-continuity-disaster-recovery`).

**Result:** Coverage; documented escalation; on-call doesn't get woken without playbook.

### Example 2: Post-mortem for SEV-1
**Goal:** Quality blameless post-mortem within 5 days.
**Steps:**
1. Within 2h of resolution: schedule retro (60 min).
2. Recipe 6 template; IC drafts.
3. Retro meeting → fill timeline + action items.
4. Publish to KB; Slack #engineering.
5. Track AI completion (per `internal-knowledge-base-notion-slab-tettra`).

**Result:** Learnings codified; actions tracked; trust grows.

## Edge cases / gotchas

- **Blameless ≠ accountabilityless.** Action items have owners + dates. "We" is the wrong word; name owners.
- **Lessons learned ≠ apologies.** Recipe 9 customer email is one apology; the post-mortem is for engineering learning.
- **Runbook rot.** Recipe 11 sweep critical; outdated runbook is worse than no runbook (false confidence).
- **Severity inflation.** Define SEV-1 narrowly. Calling everything SEV-1 = nothing's SEV-1.
- **On-call burnout.** Cap pages per shift; rotation overlap prevents single-point-of-failure.
- **Status page over-promising.** Don't say "fixed by 11:00" unless verified. "Identified, reverting deploy now" is honest.
- **Customer comms timing.** Recipe 9 — SEV-1 customer email within 4h; SEV-2 within 24h. Faster than legal-mandated breach windows.
- **Insurance carrier coordination.** SEV-1 + security breach → cyber-insurance hotline FIRST (within 24h often). **Defer to `legal-counsel`.**
- **Privacy in post-mortem.** Don't publish customer-identifiable data in shared KB. Reference INC-2026-0042 only; full impact data in private channel.
- **Single-person knowledge.** If only one person can fix a system, that's a runbook gap. Pair-write the runbook before the incident.
- **Defer to `legal-counsel` for breach-notification timing (GDPR 72h, SEC 4 business days for public cos, state breach laws), and for customer-facing incident comms drafting where data-loss involved.**

## Sources

- Google SRE Book — Blameless Postmortems: https://sre.google/sre-book/postmortem-culture/
- Incident.io: https://incident.io/
- PagerDuty Process Automation: https://www.pagerduty.com/products/process-automation/
- PagerDuty API: https://developer.pagerduty.com/
- Incident.io API: https://api-docs.incident.io/
- Statuspage API: https://developer.statuspage.io/
- Better Stack: https://betterstack.com/uptime/docs/api/incidents
- Notion API: https://developers.notion.com/
- SEC cyber disclosure (4 business days): https://www.sec.gov/news/press-release/2023-139
