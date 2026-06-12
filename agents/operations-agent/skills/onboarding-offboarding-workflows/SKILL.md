<!--
Sources: https://www.hibob.com/blog/rippling-vs-gusto-vs-hibob/
         https://johngalt-finance.com/gusto-vs-justworks-vs-rippling-payroll-hr-2026/
         https://workos.com/blog/best-scim-providers-for-automated-user-provisioning-in-2026
         https://www.rippling.com/blog/rippling-mdm-review
HRIS-coupled onboarding/offboarding flows with SCIM provisioning + MDM device hooks.
-->
# Onboarding / Offboarding Workflows — SKILL

End-to-end Day-1 / Week-1 / 30-60-90 onboarding playbook and termination-day offboarding playbook coupled to the HRIS (Rippling / Gusto / HiBob) and downstream SCIM-connected apps + MDM. Drives account provisioning on hire, equipment shipping, manager onboarding plan, and on offboarding triggers automatic deprovisioning + device wipe + exit-interview survey.

## When to use

- A hire is signed and you need a **Day-1 / Week-1 / 30-60-90 plan** + account creation across Google Workspace / Slack / GitHub / Notion / Linear.
- An employee is terminating and you need **deprovisioning, equipment return, device wipe, exit interview, COBRA notice** orchestrated.
- Trigger phrases: "new hire", "day 1 checklist", "onboarding plan", "offboard", "exit", "termination", "knowledge transfer", "deprovision", "exit interview".

## Setup

```bash
export RIPPLING_API_KEY="xxx"      # https://developer.rippling.com — Rippling Public API
export GUSTO_API_KEY="xxx"         # https://docs.gusto.com — partner-only OAuth
export HIBOB_SERVICE_USER_ID="xxx" # https://apidocs.hibob.com/ — service users
export HIBOB_SERVICE_USER_TOKEN="xxx"
export OKTA_API_TOKEN="xxx"        # https://developer.okta.com — SCIM 2.0
export WORKOS_API_KEY="xxx"        # https://workos.com — Directory Sync (SCIM)
export KANDJI_API_TOKEN="xxx"      # Iru (formerly Kandji, rebranded Oct 2025)
```

Auth notes:
- Rippling Public API uses a key per integration; one key per app surface (HR, IT, Finance) on Rippling Enterprise tiers.
- HiBob requires a service-user pair (id + token).
- Iru/Kandji bearer token in `Authorization: Bearer`.

## Common recipes

### Recipe 1: Day-1 onboarding plan template (Notion DB row)
```bash
# Push checklist row to Notion onboarding DB
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Content-Type: application/json" -H "Notion-Version: 2022-06-28" \
  -d '{
    "parent":{"database_id":"<onboarding-db>"},
    "properties":{
      "Name":{"title":[{"text":{"content":"Avery Lee — Sr Ops Analyst — 2026-08-01"}}]},
      "Start Date":{"date":{"start":"2026-08-01"}},
      "Manager":{"people":[{"id":"<manager-user>"}]},
      "Status":{"select":{"name":"Pre-boarding"}}
    }
  }'
```

### Recipe 2: Pre-boarding — order laptop (Rippling IT)
```bash
# Rippling IT — provision Mac to ship to home address before start
curl -s -X POST "https://api.rippling.com/platform/api/devices/orders" \
  -H "Authorization: Bearer $RIPPLING_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "employee_id":"<rippling_emp_id>",
    "device_type":"MacBook Pro 14 M4 Pro",
    "ship_to":"home_on_file",
    "deliver_by":"2026-07-29"
  }'
```

### Recipe 3: Day-1 SCIM provisioning fanout (Okta)
```bash
# Create user → push to all assigned apps via SCIM
NEW_USER=$(curl -s -X POST "https://<org>.okta.com/api/v1/users?activate=true" \
  -H "Authorization: SSWS $OKTA_API_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "profile":{"firstName":"Avery","lastName":"Lee","email":"avery@co.com","login":"avery@co.com"},
    "groupIds":["<ops-group>","<all-staff-group>"]
  }' | jq -r .id)

# Group assignment automatically pushes to all SCIM-connected apps (Slack, GitHub, Notion, Linear, Figma, ...)
echo "$NEW_USER provisioned across $(curl -s -H "Authorization: SSWS $OKTA_API_TOKEN" \
  "https://<org>.okta.com/api/v1/users/$NEW_USER/appLinks" | jq length) apps"
```

### Recipe 4: GitHub provisioning (org invite)
```bash
curl -s -X POST "https://api.github.com/orgs/<org>/invitations" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d '{
    "email":"avery@co.com",
    "role":"direct_member",
    "team_ids":[<ops-team-id>]
  }'
```

### Recipe 5: Day-1 welcome Slack DM + #intros post
```bash
# slack-mcp call equivalent
curl -s -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" -H "Content-Type: application/json" \
  -d '{"channel":"#intros","text":"Welcome Avery Lee, Sr Ops Analyst, joining the Ops team today. Manager: @maria. Buddy: @sam."}'
```

### Recipe 6: 30-60-90 milestone tracking (Linear)
```bash
# Create three tracked milestones from a template
for DAY in 30 60 90; do
  curl -s -X POST https://api.linear.app/graphql \
    -H "Authorization: $LINEAR_API_KEY" -H "Content-Type: application/json" \
    -d "{\"query\":\"mutation { issueCreate(input: { title: \\\"Avery Lee — $DAY-day milestone\\\", teamId: \\\"<team>\\\", dueDate: \\\"2026-$( [ $DAY = 30 ] && echo 08-31 || [ $DAY = 60 ] && echo 09-30 || echo 10-31 )\\\", assigneeId: \\\"<manager>\\\" }) { success } }\"}"
done
```

### Recipe 7: Termination → deprovision fanout (Okta)
```bash
# Disable user → SCIM deprovisions across all assigned apps
curl -s -X POST "https://<org>.okta.com/api/v1/users/<id>/lifecycle/suspend" \
  -H "Authorization: SSWS $OKTA_API_TOKEN"

# After 24h, deactivate (audit window)
curl -s -X POST "https://<org>.okta.com/api/v1/users/<id>/lifecycle/deactivate" \
  -H "Authorization: SSWS $OKTA_API_TOKEN"
```

### Recipe 8: Remote device wipe (Iru / Kandji)
```bash
# Iru — Self Service + Compliance wipe
curl -s -X POST "https://<tenant>.api.iru.com/api/v1/devices/<device_id>/actions/erase" \
  -H "Authorization: Bearer $KANDJI_API_TOKEN" -H "Content-Type: application/json" \
  -d '{"PIN":"123456"}'

# Jamf Pro equivalent
curl -s -X POST "https://<jss>.jamfcloud.com/api/v1/computer-inventory/<id>/erase" \
  -H "Authorization: Bearer $JAMF_TOKEN" \
  -d '{"pin":"123456","obliterationBehavior":"Default"}'

# Microsoft Intune via Graph
curl -s -X POST "https://graph.microsoft.com/v1.0/deviceManagement/managedDevices/<id>/wipe" \
  -H "Authorization: Bearer $GRAPH_TOKEN"
```

### Recipe 9: Exit interview survey (Tally)
```bash
# Tally form invite
curl -s -X POST "https://api.tally.so/v1/forms" \
  -H "Authorization: Bearer $TALLY_TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"Exit Interview — Standard","blocks":[...]}'

# gmail-mcp → send survey link
```

### Recipe 10: COBRA + final-paycheck timing (Gusto)
```bash
curl -s -X POST "https://api.gusto.com/v1/companies/<co>/employees/<emp>/terminations" \
  -H "Authorization: Bearer $GUSTO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "effective_date":"2026-06-30",
    "run_termination_payroll":true,
    "wages_payable_method":"check"
  }'
```

### Recipe 11: HiBob lifecycle webhook listener
```bash
# Configure a webhook to fire termination events to your offboarding workflow runner
curl -s -X POST "https://api.hibob.com/v1/webhooks" \
  -u "$HIBOB_SERVICE_USER_ID:$HIBOB_SERVICE_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Termination → Offboard runner",
    "events":["employee.terminated"],
    "url":"https://hooks.example.com/hibob-termination"
  }'
```

## Examples

### Example 1: Hire a Senior Ops Analyst — 14 days out
**Goal:** All Day-1 systems ready by 2026-08-01.
**Steps:**
1. Recipe 1: create Notion onboarding row.
2. Recipe 2: Rippling IT laptop order, deliver by 2026-07-29.
3. T-3 days: Recipe 3 (Okta create) → fanout provisions Slack, GitHub, Notion, Linear, Figma, Loom.
4. T-1 day: send welcome email via `gmail-mcp` (calendar invite for Day-1 schedule, buddy intro, links).
5. Day 0 09:00: Recipe 5 Slack `#intros` post; manager runs Day-1 checklist (Notion); ML&D auto-enrolls in handbook ACK signing.
6. T+30/+60/+90: Recipe 6 Linear milestones; manager-template 1:1 cadence (see `performance-review-cycle-lattice-15five`).

**Result:** Hire arrives to a working laptop with all accounts live, calendar packed, and 30-60-90 in writing.

### Example 2: Offboard a leaver — termination day
**Goal:** Clean exit by end of last day.
**Steps:**
1. HR enters termination in HRIS → webhook fires (Recipe 11).
2. T-15min before last meeting: Recipe 7 suspend in Okta (SCIM deprovisions Slack workspace, GitHub seat, Notion guest, Linear, Figma editor).
3. Recipe 8: device wipe scheduled for shipping-label arrival.
4. `linear-mcp` issue: laptop return tracking (FedEx prepaid label via Rippling IT).
5. `gmail-mcp` → exit-interview link (Recipe 9).
6. Recipe 10: Gusto runs final paycheck and COBRA notice.
7. T+24h: full Okta deactivate (audit window for inbox migration).
8. Knowledge transfer doc archived in Notion `Offboarding/` per leaver.

**Result:** No orphan accounts, no surprise paychecks, audit-clean trail. **Defer to `legal-counsel` for state-specific final-pay deadlines (CA = same day, NY = next regular payday) and severance/release templates.**

## Edge cases / gotchas

- **SCIM lag.** Slack SCIM provisioning takes 2-15 minutes. For day-of-hire, schedule Recipe 3 the day before.
- **Okta `suspend` vs `deactivate`.** Suspend retains data + license; deactivate revokes both. Always suspend first to preserve audit trail and inbox transfer.
- **GitHub seat vs role.** Recipe 4 invites; user must accept. For SSO-only orgs, configure SCIM via Okta GitHub Enterprise app to auto-add.
- **Rippling laptop ship-to-home requires home address.** Will 422 if `address_home` missing on employee record.
- **Iru/Kandji erase PIN** must be 6 digits and stored — needed to unlock the device if user requests recovery. Don't lose it.
- **Final paycheck state law.** Gusto Recipe 10 routes correctly per state, but **MA, CA, MI, MO, IL, CO, RI** have same-day-or-next-day requirements. **Defer to `legal-counsel`.**
- **PII in onboarding rows.** Notion onboarding DB should restrict visibility to People Ops + manager; do not put SSN, DOB in Notion. Source-of-truth = HRIS.
- **30-60-90 cadence drift.** Without Recipe 6 reminders, milestones get skipped. Always wire Linear due-dates.
- **Equipment-return non-compliance.** Build a 14-day SLA in offboarding policy; after 14 days deduct from final paycheck (only where state law allows; **defer to `legal-counsel`**).
- **COBRA timing.** 14 days from termination to send notice (federal); some states stricter (CA Cal-COBRA 30 days). Gusto handles automatically when termination registered.
- **Background check on rehire.** Re-trigger via Checkr / GoodHire; HRIS may pull stale record.

## Sources

- HiBob — Rippling vs Gusto vs HiBob: https://www.hibob.com/blog/rippling-vs-gusto-vs-hibob/
- John Galt Finance — Gusto vs Justworks vs Rippling 2026: https://johngalt-finance.com/gusto-vs-justworks-vs-rippling-payroll-hr-2026/
- WorkOS — Best SCIM Providers 2026: https://workos.com/blog/best-scim-providers-for-automated-user-provisioning-in-2026
- Rippling — MDM Review: https://www.rippling.com/blog/rippling-mdm-review
- Iru — Kandji Alternatives (rebrand Oct 2025): https://www.iru.com/compare/kandji-alternatives
- Okta SCIM 2.0 spec: https://developer.okta.com/docs/concepts/scim/
- Rippling Public API: https://developer.rippling.com/
- HiBob API: https://apidocs.hibob.com/
- Gusto Embedded API: https://docs.gusto.com/embedded-payroll
