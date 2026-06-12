<!--
Source: https://docs.leandata.com/ + https://docs.chilipiper.com/api/ + https://www.distribute.so/
Lead routing — LeanData + Chili Piper + Distribute (June 2026 SOTA).
-->
# Lead Routing — LeanData + Chili Piper + Distribute — SKILL

LeanData (Salesforce-native): match → route → book in one flow, ABM-aware. Chili Piper: inbound calendar router + form-to-meeting, round-robin. Distribute: HubSpot-focused routing + handoff. Routing logic: round-robin, geo, vertical, named-account, ABM tier, AE territory, SDR pod.

## When to use

- **Build a lead-routing flow** — segment + geo + ABM tier rules.
- **Inbound calendar router** — form submission → first-available AE meeting.
- **Round-robin pod** — distribute leads evenly across SDR/AE pod.
- **ABM tier override** — Tier 1 named accounts bypass round-robin.
- **Form-to-meeting booking** — high-intent demo request → auto-book.
- **Routing audit** — find leads that fell through (no owner, no follow-up).
- **Trigger phrases**: "lead routing", "round robin", "Chili Piper", "LeanData flow", "form to meeting", "ABM tier routing".

Do NOT use this skill for: **lead enrichment** (use `data-enrichment-zoominfo-apollo-clay`); **deduplication** (use `duplicate-mgmt-leandata-dedupe`); **lead-to-opp conversion** (use `salesforce-admin-custom-fields-flows`); **territory definition** (use `territory-planning-assignment`).

## Setup

```bash
# LeanData is Salesforce-native — uses standard SF auth
sf org login web --alias prod
# LeanData lives in custom-metadata + flows; no separate API key

# Chili Piper — API key (Settings → API → Generate)
export CHILIPIPER_API_KEY="<key>"
export CHILIPIPER_BASE="https://api.chilipiper.com/v1"

# Distribute — token (Settings → Developers)
export DISTRIBUTE_TOKEN="<token>"

# Or via api-gateway
export MATON_API_KEY="<key>"
```

Required:
- LeanData: paid Salesforce-native package (~$5K-25K/yr depending on volume)
- Chili Piper: per-seat or volume-based (~$25-45/seat/mo)
- Distribute: HubSpot-focused, comparable pricing

## Common recipes

### Recipe 1: LeanData routing graph (canonical flow)

```
Trigger: Lead Created OR Form Submission
Step 1 — Match to existing Account
  If match → route to existing Account Owner
  Else → continue
Step 2 — ICP fit score check (custom field on Lead)
  Score < 50 → route to Nurture queue (Marketing Cloud or HubSpot)
  Score ≥ 50 → continue
Step 3 — Segment routing
  Enterprise (employees > 1000) → Enterprise AE pod (round-robin)
  Mid-market (200-1000) → MM AE pod (round-robin)
  SMB (< 200) → SDR pod (round-robin)
Step 4 — Geo override
  EMEA → EMEA team
  APAC → APAC team
  Other → North America team
Step 5 — ABM tier override
  Tier 1 ABM account → named AE (bypass round-robin)
Step 6 — Calendar slot booking via Chili Piper
  Auto-book first available slot with assigned AE
```

LeanData routes are visual graphs (configured in-app), backed by:
- `LeanData__Match_Node__c` (matching logic)
- `LeanData__Routing_Node__c` (routing decisions)
- `LeanData__Round_Robin_Pool__c` (pod definitions)

### Recipe 2: LeanData round-robin pool definition

```bash
# Create a pool via Salesforce records (LeanData stores pools in custom objects)
sf data create record --target-org prod --sobject LeanData__Round_Robin_Pool__c \
  --values "Name='Enterprise AE Pod West' LeanData__Pool_Type__c='Round Robin' \
            LeanData__Skip_If_Out_Of_Office__c=true"

# Add members
sf data create record --target-org prod --sobject LeanData__Pool_Member__c \
  --values "LeanData__Pool__c=<pool_id> LeanData__User__c=<user_id_alice> LeanData__Weight__c=1"
sf data create record --target-org prod --sobject LeanData__Pool_Member__c \
  --values "LeanData__Pool__c=<pool_id> LeanData__User__c=<user_id_bob> LeanData__Weight__c=1"
```

### Recipe 3: Chili Piper inbound router

```bash
curl -X POST "$CHILIPIPER_BASE/routers" \
  -H "X-API-Key: $CHILIPIPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Inbound Demo Request — Enterprise",
    "router_type": "round_robin",
    "queue_users": ["ae1@co.com", "ae2@co.com", "ae3@co.com"],
    "filter_rules": [
      {"field": "country", "operator": "IN", "values": ["US", "CA"]},
      {"field": "company_size", "operator": "GTE", "value": 200}
    ],
    "fallback_router_id": "rtr_smb_default",
    "calendar_integration": "google",
    "meeting_buffer_minutes": 15,
    "meeting_duration_minutes": 30
  }'
```

### Recipe 4: Chili Piper form-to-meeting booking

```javascript
// On a marketing form submission: trigger Chili Piper booking iframe
// Embed in form thank-you page
<script src="https://cdn.chilipiper.com/marketing/concierge.js"></script>
<script>
  ChiliPiper.submit('your-domain', 'inbound-router-name', {
    map: true,
    lead: {
      Email: 'visitor@co.com',
      FirstName: 'Visitor',
      LastName: 'Last',
      Company: 'Acme Co',
      Country: 'US',
      Employees: 500
    }
  });
</script>
```

### Recipe 5: ABM tier 1 named account override

```sql
-- LeanData routing logic: ABM tier 1 → named AE
-- Configured in LeanData Routing Node "ABM Override"
-- Condition (Apex-like syntax in LeanData):
Account.ABM_Tier__c == "1" AND Account.Named_AE__c != null

-- Action:
SET Lead.Owner = Account.Named_AE__c
SKIP downstream routing
```

This is a no-code config in LeanData visual builder; equivalent SOQL test:

```bash
sf data query --target-org prod --query \
  "SELECT Id, Name, ABM_Tier__c, Named_AE__r.Name FROM Account WHERE ABM_Tier__c = '1' LIMIT 20"
```

### Recipe 6: SLA audit — leads with no owner action in 4h

```python
import requests, os
from datetime import datetime, timedelta

q = """
SELECT Id, Name, Email, CreatedDate, Owner.Name, Owner.Email, Status, Last_Activity_Date__c
FROM Lead
WHERE CreatedDate >= TODAY
  AND CreatedDate < N_HOURS_AGO:4
  AND (Last_Activity_Date__c = null OR Last_Activity_Date__c < CreatedDate)
"""
r = requests.get(f"https://gateway.maton.ai/salesforce/services/data/v60.0/query",
                 params={"q": q},
                 headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"}).json()

for lead in r['records']:
    print(f"SLA breach: {lead['Name']} owned by {lead['Owner']['Name']}, no activity since {lead['CreatedDate']}")
    # Slack alert (via slack-mcp)
```

### Recipe 7: Routing manifest (notion-stored, single source of truth)

Store the canonical routing decision tree as a Notion page or markdown:

```yaml
# routing_manifest_2026Q3.yaml
trigger:
  - lead_created
  - form_submitted

decision_tree:
  - check: existing_account_match
    yes: route_to_account_owner
    no: continue
  - check: icp_fit_score >= 50
    no: route_to_nurture
    yes: continue
  - check: company_size
    cases:
      enterprise (> 1000): pool_enterprise_ae
      mid_market (200-1000): pool_mm_ae
      smb (< 200): pool_sdr
  - check: geo_region
    cases:
      EMEA: override_to_emea_team
      APAC: override_to_apac_team
      else: continue
  - check: abm_tier == 1
    yes: override_to_named_ae
  - action: book_chili_piper_calendar
```

LeanData configuration mirrors this. Quarterly: diff actual LeanData graph vs manifest, flag drift.

### Recipe 8: Chili Piper booking via API (bypass embedded widget)

```bash
curl -X POST "$CHILIPIPER_BASE/bookings" \
  -H "X-API-Key: $CHILIPIPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "router_id": "rtr_xyz789",
    "guest": {
      "email": "lead@co.com",
      "first_name": "Lead",
      "last_name": "Name",
      "company": "Acme",
      "country": "US"
    },
    "preferred_dates": ["2026-06-15T10:00:00Z", "2026-06-15T14:00:00Z"]
  }'
# Returns confirmed slot + Zoom link + calendar invite
```

### Recipe 9: Test routing with synthetic leads

```python
# Before deploying new routing rules: spawn 10 test leads covering edge cases
test_leads = [
    {"name": "Test Enterprise EMEA", "company_size": 5000, "country": "GB", "expect_owner": "EMEA AE pod"},
    {"name": "Test SMB US", "company_size": 50, "country": "US", "expect_owner": "SDR pod"},
    {"name": "Test ABM Tier 1", "company_size": 2000, "country": "US", "expect_account_match": True, "expect_owner": "named AE"},
    {"name": "Test ICP fail", "icp_fit_score": 30, "expect_owner": "Nurture queue"},
    # ... etc
]

import requests, os
for tl in test_leads:
    r = requests.post(f"https://gateway.maton.ai/salesforce/services/data/v60.0/sobjects/Lead",
                      headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
                               "Content-Type": "application/json"},
                      json={"FirstName": "Test", "LastName": tl["name"],
                            "Company": tl["name"], "Email": f"{tl['name'].lower().replace(' ','')}@test.co",
                            "NumberOfEmployees": tl.get("company_size",100),
                            "Country": tl.get("country","US"),
                            "ICP_Fit_Score__c": tl.get("icp_fit_score",75)})
    lead_id = r.json()["id"]
    # Wait 30s for LeanData to route, then query owner
    import time; time.sleep(30)
    owner = requests.get(f"https://gateway.maton.ai/salesforce/services/data/v60.0/sobjects/Lead/{lead_id}",
                         headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"}).json()["Owner"]["Name"]
    expected = tl["expect_owner"]
    ok = "✓" if expected in owner else "✗"
    print(f"{ok} {tl['name']}: routed to {owner} (expected {expected})")
```

### Recipe 10: Distribute (HubSpot) routing flow

```bash
# Distribute uses HubSpot workflows under the hood
curl -X POST "https://api.distribute.so/v1/routes" \
  -H "Authorization: Bearer $DISTRIBUTE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "HubSpot Inbound Router",
    "source": "hubspot_form",
    "form_id": "frm_xyz",
    "rules": [
      {"condition": "country IN [US,CA]", "assign_pool": "americas_ae"},
      {"condition": "country IN [GB,DE,FR]", "assign_pool": "emea_ae"}
    ],
    "default_pool": "global_sdr"
  }'
```

### Recipe 11: LeanData routing performance audit

```bash
# Query LeanData routing audit log (custom object)
sf data query --target-org prod --query \
  "SELECT Id, LeanData__Lead__r.Name, LeanData__Final_Owner__r.Name, LeanData__Routing_Time_Ms__c, \
   LeanData__Decision_Path__c, CreatedDate \
   FROM LeanData__Routing_Audit__c \
   WHERE CreatedDate = LAST_N_DAYS:7 \
   ORDER BY CreatedDate DESC"
# Look for: anomalous routing times, unexpected fallbacks, owner=null cases
```

### Recipe 12: Slack escalation for stale unrouted leads

```python
# Daily 9am scan: any leads stuck in "Routing" status > 1 hour
import requests, os
q = """
SELECT Id, Name, Email, Status, CreatedDate
FROM Lead
WHERE Status = 'Routing'
  AND CreatedDate < N_HOURS_AGO:1
"""
r = requests.get(f"https://gateway.maton.ai/salesforce/services/data/v60.0/query",
                 params={"q": q},
                 headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"}).json()

if r['totalSize'] > 0:
    msg = f":warning: {r['totalSize']} leads stuck in routing > 1h\n"
    for lead in r['records'][:5]:
        msg += f"- {lead['Name']} ({lead['Email']}), created {lead['CreatedDate']}\n"
    # Post to #sales-ops via slack-mcp
```

## Examples

### Example 1: Deploy new ABM tier 1 override

**Goal:** Tier 1 ABM accounts (top 50 strategic) bypass round-robin; go to named AE.

**Steps:**
1. In Salesforce: add `Account.ABM_Tier__c` picklist (1/2/3) + `Account.Named_AE__c` lookup to User.
2. Tag accounts: 50 Tier 1 + 200 Tier 2 (via `salesforce-admin-custom-fields-flows`).
3. Add LeanData routing node "ABM Tier 1 Override" (Recipe 5) before standard pod routing.
4. Recipe 9 — test with 5 synthetic Tier 1 leads + 5 non-tier leads.
5. Verify Tier 1 routes to named AE; others go through normal flow.
6. Activate in production.

**Result:** Top accounts get senior attention immediately; no SDR-handoff lag.

### Example 2: Inbound demo request → Chili Piper booking

**Goal:** Marketing form "Request Demo" → instant calendar slot with AE.

**Steps:**
1. Recipe 3 — create Chili Piper router for inbound demos (Enterprise pool, geo US/CA, size > 200).
2. Build SMB fallback router for sub-200 leads.
3. Recipe 4 — embed booking widget on form thank-you page.
4. Test 5 form submissions; verify slots auto-booked, AE notifications fire.
5. Track conversion: form submission → meeting held % (target > 60%).

**Result:** Inbound demo speed-to-meeting drops from 24h to < 1h; show rate +20%.

### Example 3: Quarterly routing manifest audit

**Goal:** Confirm LeanData graph matches the canonical manifest.

**Steps:**
1. Recipe 7 — pull latest manifest from notion.
2. In LeanData: export current graph (PDF or screenshot).
3. Recipe 11 — query routing audit log for last 30 days; group by decision path.
4. Cross-check decision paths against manifest steps.
5. Recipe 6 — find any SLA breach pattern (lead created but no owner action in 4h).
6. Document any drift in notion routing-changes-log.
7. Fix via LeanData UI; re-test via Recipe 9.

**Result:** Routing is trustworthy; no "lead fell through" tickets next quarter.

## Edge cases / gotchas

- **LeanData is Salesforce-native, not SaaS** — config lives in your org as records + flows. Sandbox-prod drift is real.
- **Round-robin "fairness" caveats** — out-of-office handling, vacation, ramp tier weighting. Default skips OOO but config matters.
- **Chili Piper booking buffer** — `meeting_buffer_minutes` prevents back-to-backs; 0 = AE pain.
- **Form-to-meeting on mobile** — Chili Piper iframe doesn't always render right on mobile; test before deploy.
- **Time zone handling** — Chili Piper uses user-local TZ; AE TZ; account TZ. Mismatches confuse AEs.
- **LeanData routing audit log retention** — 90 days default. Long-term audits: replicate to warehouse.
- **ABM tier source-of-truth** — usually Demandbase or Account Engagement. Sync nightly to Salesforce; stale tags route wrong.
- **Round-robin pools shouldn't have OOO members** — leads to skip/loop; pre-onboarding flag often missed.
- **Fallback routers** — must always have a fallback. Otherwise leads silently fail routing.
- **Account match logic** — fuzzy or exact? Email domain or name? Wrong choice fragments accounts.
- **LeanData "no owner found" branch** — defaults to queue; queue must be staffed.
- **Chili Piper webhook reliability** — webhook can lag; primary state in their UI.
- **Cross-tool latency** — form → LeanData (5s) → Chili Piper booking (3s) → calendar (instant) → SF lead update (10s). Total user-perceived delay matters.
- **Lead-to-Contact conversion timing** — LeanData routes Leads; once converted, Contact routing is different (often a separate flow).
- **Holiday / weekend rules** — round-robin may book Monday slot Friday night; AE surprised. Configure routing hours.
- **GDPR consent** — EMEA leads must have consent before auto-booking; LeanData has consent-check nodes.

## Sources

- [LeanData documentation](https://docs.leandata.com/)
- [LeanData Routing Node Reference](https://docs.leandata.com/v1/reference/routing-nodes)
- [Chili Piper API docs](https://docs.chilipiper.com/api/)
- [Chili Piper Routers + Bookings](https://help.chilipiper.com/hc/en-us/articles/360038773192)
- [Distribute (HubSpot routing)](https://www.distribute.so/)
- [Round-robin best practices (LeanData)](https://www.leandata.com/blog/round-robin/)
- [Salesforce Lead Assignment Rules (native fallback)](https://help.salesforce.com/s/articleView?id=sf.creating_assignment_rules.htm)
- [Inbound lead response benchmarks (HBR / Lead Response Mgmt)](https://hbr.org/2011/03/the-short-life-of-online-sales-leads)
