<!--
Sources: https://ramp.com/procurement/
         https://www.spendhound.com/blog/best-saas-spend-management-software
Procurement playbook: intake form → approval workflow → contract storage → renewal calendar.
Built-in to Ramp/Brex procurement modules; or DIY with Typeform + Linear + Notion + GCal.
-->
# Procurement Playbook — Intake → Approval → Renewal — SKILL

End-to-end procurement workflow: structured intake form, approval routing matrix, contract storage convention, renewal calendar with 90/60/30/7-day alerts. Works either with Ramp/Brex Procurement built-ins, or DIY via Typeform/Tally + Linear + Notion + Google Calendar.

## When to use

- Standing up procurement for the first time.
- Replacing chaotic "Slack DM to ops" intake with a process.
- Codifying who approves what dollar amounts.
- Building a renewal calendar that doesn't surprise the team.
- Trigger phrases: "procurement", "purchase request", "PR", "vendor approval", "renewal alert", "contract storage", "intake form".

## Setup

```bash
export RAMP_TOKEN="xxx"          # Ramp Procurement module
export BREX_TOKEN="xxx"          # Brex Procurement
export TYPEFORM_TOKEN="xxx"      # or TALLY_TOKEN
export LINEAR_API_KEY="xxx"      # approval workflow
export NOTION_TOKEN="xxx"        # contract storage + vendor registry
export GCAL_TOKEN="xxx"          # renewal calendar
export GDRIVE_TOKEN="xxx"        # signed PDFs
export SLACK_BOT_TOKEN="xxx"     # reminders
```

## Common recipes

### Recipe 1: Approval matrix policy
```yaml
approval_matrix:
  # Dollar thresholds (annual contract value)
  tier_1_lt_1k:
    approver: requester_manager
    sla_hours: 24
    contract_review_required: false
  tier_2_1k_to_10k:
    approver: department_head
    sla_hours: 48
    contract_review_required: false
  tier_3_10k_to_50k:
    approver: [department_head, finance_lead]
    sla_hours: 72
    contract_review_required: true   # ops + DPA review
  tier_4_50k_to_250k:
    approver: [department_head, finance_lead, cfo]
    sla_hours: 5_days
    contract_review_required: true   # ops + DPA + legal review
  tier_5_gt_250k:
    approver: [department_head, finance_lead, cfo, ceo]
    sla_hours: 10_days
    contract_review_required: true
    board_notification: true

# Special categories regardless of dollar
data_processor_vendor:
  contract_review_required: true   # DPA + security questionnaire mandatory
  approver_addons: [security_lead]
ai_genai_vendor:
  approver_addons: [security_lead, head_of_ai]
financial_vendor:
  approver_addons: [finance_lead, security_lead]
```

### Recipe 2: Intake form (Typeform)
```bash
curl -s -X POST "https://api.typeform.com/forms" \
  -H "Authorization: Bearer $TYPEFORM_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "title":"Procurement Intake",
    "fields":[
      {"title":"What problem are you solving?","type":"long_text","required":true},
      {"title":"What is the proposed vendor/tool?","type":"short_text","required":true},
      {"title":"Annual cost (USD)","type":"number","required":true},
      {"title":"Contract term","type":"multiple_choice","choices":[{"label":"Monthly"},{"label":"Annual"},{"label":"Multi-year"}]},
      {"title":"Alternatives considered","type":"long_text"},
      {"title":"Will this process customer data / PII?","type":"yes_no","required":true},
      {"title":"Will this use / contain AI / GenAI?","type":"yes_no","required":true},
      {"title":"Integrates with which systems?","type":"long_text"},
      {"title":"Requested start date","type":"date","required":true},
      {"title":"Budget category","type":"dropdown","choices":[{"label":"Engineering"},{"label":"Ops"},{"label":"Marketing"},{"label":"Sales"},{"label":"Finance"},{"label":"People"}]},
      {"title":"Manager email (approval)","type":"email","required":true}
    ]
  }'
```

### Recipe 3: Linear auto-create approval ticket on form submit
```bash
# Typeform webhook → endpoint that calls Linear
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $LINEAR_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "query":"mutation { issueCreate(input: { teamId: \"<ops-team>\", title: \"PR: <vendor> — $<cost>/yr — <category>\", description: \"<intake-payload>\", labelIds: [\"<procurement-label>\", \"<tier-2-label>\"], assigneeId: \"<approver-by-tier>\" }) { issue { id url } } }"
  }'
```

### Recipe 4: Notion vendor registry (one row per vendor)
```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_TOKEN" -H "Notion-Version: 2022-06-28" -H "Content-Type: application/json" \
  -d '{
    "parent":{"database_id":"<vendor-registry>"},
    "properties":{
      "Name":{"title":[{"text":{"content":"<Vendor>"}}]},
      "Owner":{"people":[{"id":"<owner>"}]},
      "Category":{"select":{"name":"<Category>"}},
      "Annual Spend USD":{"number":12000},
      "Term":{"select":{"name":"Annual"}},
      "Renewal Date":{"date":{"start":"2027-06-15"}},
      "Auto-Renew":{"checkbox":false},
      "Contract URL":{"url":"https://drive.google.com/..."},
      "DPA URL":{"url":"https://drive.google.com/..."},
      "SOC 2 URL":{"url":"https://drive.google.com/..."},
      "MSA URL":{"url":"https://drive.google.com/..."},
      "Status":{"select":{"name":"Active"}},
      "Data Processor":{"checkbox":true}
    }
  }'
```

### Recipe 5: Contract storage convention (Google Drive)
```
Vendors/
├── Active/
│   ├── <Vendor>/
│   │   ├── MSA/
│   │   │   └── 2024-MSA-v1.pdf
│   │   ├── DPA/
│   │   │   └── 2024-DPA-v1.pdf
│   │   ├── Orders/
│   │   │   └── 2026-renewal-order.pdf
│   │   ├── Trust/
│   │   │   ├── 2025-SOC2-Type2.pdf
│   │   │   └── ISO27001-2025.pdf
│   │   └── Security-Questionnaire/
│   │       └── 2025-questionnaire-completed.xlsx
├── Sunset/
└── Pending/
```

### Recipe 6: Renewal calendar with 90/60/30/7-day alerts (Python)
```python
import datetime
from dateutil.relativedelta import relativedelta
import requests, os

renewals = requests.post('https://api.notion.com/v1/databases/<vendor-db>/query',
    headers={'Authorization':f"Bearer {os.environ['NOTION_TOKEN']}",
             'Notion-Version':'2022-06-28','Content-Type':'application/json'},
    json={'filter':{'property':'Renewal Date','date':{'next_six_months':{}}}}).json()

for r in renewals['results']:
    rd = datetime.date.fromisoformat(r['properties']['Renewal Date']['date']['start'])
    vendor = r['properties']['Name']['title'][0]['plain_text']
    for days_out in [90, 60, 30, 7]:
        trigger = rd - datetime.timedelta(days=days_out)
        # Create GCal event
        requests.post(f"https://www.googleapis.com/calendar/v3/calendars/<cal>/events",
            headers={'Authorization':f"Bearer {os.environ['GCAL_TOKEN']}"},
            json={
                'summary': f"[{days_out}D] Renewal: {vendor}",
                'description': f"Action by tier: pull benchmark, draft counter, notify champion.",
                'start': {'date': trigger.isoformat()},
                'end': {'date': trigger.isoformat()},
            })
```

### Recipe 7: Slack #ops renewal digest (weekly)
```bash
curl -s -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "channel":"#ops-renewals",
    "text":"Renewals — next 90 days:\n• <Vendor A> | $24k | 2026-09-01 (in 60d) — start counter\n• <Vendor B> | $80k | 2026-08-15 (in 45d) — owner: @alex\n• <Vendor C> | $6k | 2026-07-30 (in 30d) — auto-renew, decide today\n"
  }'
```

### Recipe 8: Ramp Procurement intake (built-in)
```bash
curl -s -X POST "https://api.ramp.com/developer/v1/procurement/requests" \
  -H "Authorization: Bearer $RAMP_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "requester_id":"<user>",
    "vendor":"Acme SaaS",
    "annual_amount_cents": 1200000,
    "category":"software_subscription",
    "description":"...",
    "approval_chain":["dept_head","finance_lead"]
  }'
```

### Recipe 9: New-vendor security questionnaire trigger
```bash
# When intake flag "Data Processor" = true, kick off vendor-risk-assessment-dpa flow
# Send vendor security@ email via gmail-mcp
curl -s -X POST "https://gmail.googleapis.com/gmail/v1/users/me/messages/send" \
  -H "Authorization: Bearer $GMAIL_TOKEN" -H "Content-Type: application/json" \
  -d '{"raw":"<base64-encoded MIME with our questionnaire attached>"}'
```

### Recipe 10: Sunset workflow (vendor decommission)
```python
def sunset_vendor(vendor_id):
    # 1. Cancel auto-renew if not already
    # 2. Confirm written cancellation per MSA notice clause
    # 3. Export all data per DPA Article 28 right-to-deletion
    # 4. SCIM revoke per SSO (Okta/WorkOS)
    # 5. Update Notion registry Status = Sunset, archive folder move
    # 6. Final invoice reconciliation
    # 7. Notify all users (Slack #internal-comms)
    pass
```

## Examples

### Example 1: New SaaS request comes in
**Goal:** $30k/yr CDP request from Marketing.
**Steps:**
1. User submits Recipe 2 Typeform.
2. Recipe 3 fires → Linear ticket with Tier 3 routing.
3. Recipe 9 triggers vendor risk assessment (DPA, SOC 2 request).
4. Department head + finance approve.
5. Vendor evaluation per `vendor-evaluation-negotiation` skill.
6. Contract signed → Recipe 4 vendor registry row + Recipe 5 Drive folder.
7. Recipe 6 calendar fires for renewals.

**Result:** Documented decision, signed contract stored properly, future renewal alarmed.

### Example 2: Annual procurement hygiene
**Goal:** Refresh vendor registry, flag missing artifacts.
**Steps:**
1. Notion DB report: vendors with missing MSA / DPA / SOC 2 URL.
2. Recipe 9 to request missing artifacts.
3. Recipe 6 re-run to refresh renewal calendar.
4. Sunset orphans (no owner = candidate for sunset).

**Result:** Clean registry, no unknowns, ready for SOC 2 / due-diligence audit.

## Edge cases / gotchas

- **Tier creep.** People submit at $9,999 to dodge Tier-3 approval. Audit quarterly + spot-check intake values vs invoice.
- **"Just a trial" exemption.** Trials with auto-conversion to paid are NOT trial-exempt. Recipe 2 should force a question: "Trial converts to paid in ≤ 30 days?" If yes, route as full procurement.
- **Renewal owner ≠ original requester.** People leave. Recipe 4 must enforce `Owner` is non-null; on owner departure, reassign before deprovision.
- **Auto-renew default true.** Recipe 4 enforces `Auto-Renew: false` as policy; vendors often re-flip in renewal amendment. Re-check at every renewal.
- **DPA out-of-date.** SCCs were updated in 2021; some old DPAs reference 2010 SCCs. Refresh on renewal.
- **Approval-matrix bypass via founder.** Even founders should use intake; otherwise the registry has holes. Build a "founder fast-track" tier-0 path.
- **Multi-currency.** USD-centric matrix breaks for EU/UK teams. Normalize at intake time at month-of-submission FX rate.
- **Splitting POs.** $48k order + $8k "support add-on" both tiered separately is fraud-pattern; check 12-month vendor totals at approval time.
- **MSA red-line latency.** Tier-3+ contracts need 2-3 wk legal cycle; bake into Recipe 1 SLA. Don't approve effective date < negotiation cycle.
- **Defer to `legal-counsel` for MSA / DPA / SOW red-line and for binding interpretation of cancellation / notice clauses.**

## Sources

- Ramp Procurement: https://ramp.com/procurement/
- SpendHound — Spend Mgmt 2026: https://www.spendhound.com/blog/best-saas-spend-management-software
- Brex Procurement: https://www.brex.com/product/procurement
- Coupa procurement: https://www.coupa.com/products/procurement
- Notion API: https://developers.notion.com/
- Linear API: https://developers.linear.app/
- Typeform API: https://www.typeform.com/developers/
- DPA SCCs (2021): https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/standard-contractual-clauses-scc_en
