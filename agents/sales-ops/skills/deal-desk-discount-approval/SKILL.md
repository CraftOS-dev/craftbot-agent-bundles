<!--
Source: https://help.salesforce.com/s/articleView?id=sf.approvals_intro.htm + https://knowledge.hubspot.com/approvals
Deal desk operations — discount approval routing + SLA tracking (June 2026 SOTA).
-->
# Deal Desk Operations — Discount Approval + SLA Tracking — SKILL

Discount-tier approval routing: tier 1 (< 10% AE self), tier 2 (10-20% Manager), tier 3 (20-30% VP Sales), tier 4 (> 30% CRO + Finance). **Salesforce Approval Process** native; **HubSpot Approvals**; **DealHub deal-desk module**. Approval SLA tracking + auto-escalation. Exception management.

## When to use

- **Deploy a discount approval process** — tier-by-tier routing.
- **Approve a non-standard exception** — bespoke pricing > 30%.
- **SLA monitoring** — pending > tier SLA → escalate.
- **Auto-route discount escalation** — manager → VP → CRO chain.
- **Exception log** — capture reason codes for non-standard discounts.
- **Trigger phrases**: "discount approval", "deal desk", "Salesforce Approval Process", "approval SLA breach", "tier 4 escalation", "exception management".

Do NOT use this skill for: **CPQ pricing rules** (use `salesforce-cpq-conga-dealhub`); **commission disputes** (use `commission-dispute-audit-trail`); **non-discount approvals** (general use Salesforce/HubSpot Approval natively).

## Setup

```bash
# Salesforce — standard auth + sf CLI
sf org login web --alias prod

# HubSpot — Private App token with crm.objects.deals.write + automation
export HUBSPOT_PRIVATE_APP_TOKEN="<token>"

# DealHub — API key
export DEALHUB_API_KEY="<key>"

# Slack for escalations
export SLACK_TOKEN="<token>"

# Or via api-gateway
export MATON_API_KEY="<key>"
```

Required:
- Salesforce: Approval Process feature (Enterprise+)
- HubSpot: Sales Hub Enterprise for Approvals
- DealHub: deal-desk module included in plan

## Common recipes

### Recipe 1: Discount approval matrix (canonical)

| Tier | Discount | Auto-approver | SLA | Escalation |
|---|---|---|---|---|
| 1 | 0-10% | AE (self) | n/a | n/a |
| 2 | 10-20% | Manager | 24h | → VP Sales after 36h |
| 3 | 20-30% | VP Sales | 48h | → CRO after 72h |
| 4 | 30-40% | CRO + Finance | 72h | → CEO + Board after 96h |
| Exception | > 40% | Strategic deal review | Case-by-case | n/a |

### Recipe 2: Salesforce Approval Process — XML metadata

```xml
<!-- force-app/main/default/approvalProcesses/Opportunity.Discount_Tier_2.approvalProcess-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<ApprovalProcess xmlns="http://soap.sforce.com/2006/04/metadata">
    <active>true</active>
    <label>Discount Tier 2 (10-20%) — Manager Approval</label>
    <description>Routes 10-20% discount requests to direct manager</description>
    <entryCriteria>
      <booleanFilter>1 AND 2</booleanFilter>
      <criteriaItems>
        <field>Opportunity.Discount_Percent__c</field>
        <operation>greaterThan</operation>
        <value>10</value>
      </criteriaItems>
      <criteriaItems>
        <field>Opportunity.Discount_Percent__c</field>
        <operation>lessOrEqual</operation>
        <value>20</value>
      </criteriaItems>
    </entryCriteria>
    <initialSubmissionActions>
        <action>
            <name>Lock_Opportunity_During_Approval</name>
            <type>RecordLock</type>
        </action>
    </initialSubmissionActions>
    <approvalSteps>
        <name>Manager_Step</name>
        <label>Direct Manager Approval</label>
        <assignedApprover>
            <type>userHierarchyField</type>
            <field>Opportunity.Owner.Manager</field>
        </assignedApprover>
        <allowDelegate>true</allowDelegate>
        <ifCriteriaNotMet>NextApprover</ifCriteriaNotMet>
    </approvalSteps>
    <finalApprovalActions>
        <action>
            <name>Update_Approval_Status</name>
            <type>FieldUpdate</type>
        </action>
    </finalApprovalActions>
    <recordEditability>AdminOnly</recordEditability>
</ApprovalProcess>
```

```bash
sf project deploy start --target-org prod \
  --source-dir force-app/main/default/approvalProcesses/ \
  --test-level RunLocalTests
```

### Recipe 3: Submit for approval via REST

```bash
curl -X POST "https://gateway.maton.ai/salesforce/services/data/v60.0/process/approvals/" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "requests": [{
      "actionType": "Submit",
      "contextId": "006XX0000123ABC",
      "comments": "Discount 18% — competitive bid against CompetitorA",
      "nextApproverIds": ["005XX0000456DEF"]
    }]
  }'
```

### Recipe 4: Approve / Reject via REST

```bash
# Approver hits this from email link or Salesforce mobile
curl -X POST "https://gateway.maton.ai/salesforce/services/data/v60.0/process/approvals/" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "requests": [{
      "actionType": "Approve",
      "contextId": "a0XXX0000789",
      "comments": "Approved — competitive justification valid"
    }]
  }'
```

### Recipe 5: SLA breach query (Tier 2 > 24h pending)

```bash
sf data query --target-org prod --query \
  "SELECT Id, ProcessInstance.TargetObjectId, ProcessInstance.Status, \
   ProcessInstance.CreatedDate, ProcessInstance.SubmittedById, \
   StepStatus, ProcessNodeId \
   FROM ProcessInstanceStep \
   WHERE ProcessInstance.Status = 'Pending' \
     AND ProcessInstance.CreatedDate < N_HOURS_AGO:24"
```

### Recipe 6: Auto-escalate breached approval (Python cron)

```python
import requests, os
from datetime import datetime, timedelta

# Find tier 2 approvals > 24h pending
q = """
SELECT Id, TargetObjectId, ProcessDefinitionId, CreatedDate, SubmittedById
FROM ProcessInstance
WHERE Status = 'Pending'
  AND CreatedDate < N_HOURS_AGO:24
  AND ProcessDefinition.DeveloperName LIKE 'Discount_Tier_2%'
"""
r = requests.get(f"https://gateway.maton.ai/salesforce/services/data/v60.0/query",
                 params={"q": q},
                 headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"}).json()

VP_USER_ID = "005XX0000999XXX"
for breach in r['records']:
    # 1. Slack escalation
    requests.post("https://slack.com/api/chat.postMessage",
                  headers={"Authorization": f"Bearer {os.environ['SLACK_TOKEN']}"},
                  json={"channel": "#deal-desk-escalations",
                        "text": (f":warning: SLA breach — Opp {breach['TargetObjectId']} "
                                f"submitted {breach['CreatedDate']}, "
                                f"awaiting tier-2 approver. Escalating to VP.")})

    # 2. Reassign approval to VP
    requests.post(f"https://gateway.maton.ai/salesforce/services/data/v60.0/process/approvals/",
                  headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
                           "Content-Type": "application/json"},
                  json={"requests": [{"actionType": "Reassign",
                                       "contextId": breach['Id'],
                                       "nextApproverIds": [VP_USER_ID],
                                       "comments": "Auto-escalated: SLA breach > 24h"}]})
```

### Recipe 7: Discount validation rule (require reason)

```xml
<!-- force-app/main/default/objects/Opportunity/validationRules/Discount_Reason_Required.validationRule-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<ValidationRule xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Discount_Reason_Required</fullName>
    <active>true</active>
    <description>Discounts > 10% must include reason</description>
    <errorConditionFormula>AND(
  Discount_Percent__c > 10,
  ISBLANK(Discount_Approval_Reason__c)
)</errorConditionFormula>
    <errorMessage>Discounts > 10% require a Discount Approval Reason.</errorMessage>
    <errorDisplayField>Discount_Approval_Reason__c</errorDisplayField>
</ValidationRule>
```

### Recipe 8: HubSpot Approvals API (Enterprise)

```bash
# Create an approval request on a deal
curl -X POST "https://api.hubapi.com/crm/v3/objects/deals/<deal_id>/approvals" \
  -H "Authorization: Bearer $HUBSPOT_PRIVATE_APP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "approval_type": "discount_tier_2",
    "approver_ids": ["12345-manager-user"],
    "requested_by": "67890-ae-user",
    "comments": "18% discount — competitive bid",
    "due_date": "2026-06-12T17:00:00Z"
  }'
```

### Recipe 9: DealHub deal-desk module

```bash
# DealHub deal-desk: built-in workflows for discount approval
curl -X POST "https://api.dealhub.io/v1/approvals" \
  -H "Authorization: Bearer $DEALHUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "deal_id": "deal_xyz",
    "quote_id": "quote_abc",
    "approval_chain": ["manager@co.com","vp_sales@co.com","cro@co.com"],
    "auto_advance_on_sla_breach": true,
    "sla_hours_per_step": [24, 48, 72]
  }'
```

### Recipe 10: Exception log (Notion)

```python
# Capture every > 30% exception with reason code
import requests, os

exception = {
    "deal_id": "006XX0000123",
    "discount_pct": 35,
    "reason_code": "strategic_logo",  # standardized codes
    "narrative": "Anchor logo for FinTech vertical expansion",
    "approver": "cro@co.com",
    "approved_at": "2026-06-11T14:23:00Z",
    "deal_acv": 250000,
    "discount_dollars": 87500
}

requests.post("https://api.notion.com/v1/pages",
              headers={"Authorization": f"Bearer {os.environ['NOTION_TOKEN']}",
                       "Notion-Version": "2022-06-28"},
              json={"parent": {"database_id": os.environ['EXCEPTION_LOG_DB']},
                    "properties": {
                      "Deal": {"title": [{"text": {"content": exception["deal_id"]}}]},
                      "Discount %": {"number": exception["discount_pct"]},
                      "Reason Code": {"select": {"name": exception["reason_code"]}},
                      "Approver": {"rich_text": [{"text": {"content": exception["approver"]}}]},
                      "ACV": {"number": exception["deal_acv"]},
                      "Discount $": {"number": exception["discount_dollars"]}
                    }})
```

### Recipe 11: Quarterly discount audit

```sql
-- All discounts > 10% in Q3, by tier + outcome
SELECT
  CASE
    WHEN discount_pct <= 10 THEN 'Tier 1'
    WHEN discount_pct <= 20 THEN 'Tier 2'
    WHEN discount_pct <= 30 THEN 'Tier 3'
    WHEN discount_pct <= 40 THEN 'Tier 4'
    ELSE 'Exception'
  END AS tier,
  COUNT(*) AS deal_count,
  SUM(amount) AS deal_value,
  SUM(amount * discount_pct / 100.0) AS discount_dollars,
  ROUND(AVG(discount_pct), 1) AS avg_discount_pct,
  COUNT(*) FILTER (WHERE is_won) AS wins,
  ROUND(100.0 * COUNT(*) FILTER (WHERE is_won) / COUNT(*), 1) AS win_rate
FROM fct_opportunities
WHERE close_date >= '2026-07-01' AND close_date <= '2026-09-30'
  AND discount_pct > 0
GROUP BY 1
ORDER BY 1;
```

### Recipe 12: SLA dashboard (notion + slack digest)

```python
# Weekly Monday morning: SLA performance recap
import requests, os
from collections import Counter

# Pull all approvals last week
q = """
SELECT ProcessDefinition.DeveloperName AS tier, Status, CreatedDate, CompletedDate
FROM ProcessInstance
WHERE CreatedDate >= LAST_N_DAYS:7
"""
r = requests.get(f"https://gateway.maton.ai/salesforce/services/data/v60.0/query",
                 params={"q": q},
                 headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"}).json()

# Compute SLA hit rate per tier
by_tier = {}
for p in r['records']:
    tier = p['ProcessDefinition']['DeveloperName']
    if p['Status'] in ('Approved','Rejected') and p['CompletedDate']:
        from datetime import datetime
        c = datetime.fromisoformat(p['CreatedDate'].replace('Z','+00:00'))
        e = datetime.fromisoformat(p['CompletedDate'].replace('Z','+00:00'))
        hours = (e - c).total_seconds() / 3600
        by_tier.setdefault(tier, []).append(hours)

msg = "Approval SLA digest (last 7d):\n"
for tier, hrs in by_tier.items():
    avg = sum(hrs) / len(hrs)
    msg += f"- {tier}: {len(hrs)} closed, avg {avg:.1f}h\n"
requests.post("https://slack.com/api/chat.postMessage",
              headers={"Authorization": f"Bearer {os.environ['SLACK_TOKEN']}"},
              json={"channel": "#sales-ops", "text": msg})
```

## Examples

### Example 1: Deploy 4-tier discount approval

**Goal:** Salesforce-native approvals for tiers 2-4; SLA-tracked with auto-escalation.

**Steps:**
1. Add custom field `Discount_Percent__c` + `Discount_Approval_Reason__c` to Opportunity.
2. Recipe 7 — deploy validation rule (reason required > 10%).
3. Recipe 2 — deploy 3 ApprovalProcess metadata files (Tier 2/3/4).
4. Recipe 6 — schedule cron for SLA escalation.
5. Recipe 10 — Notion exception log database.
6. Train AEs: when to submit, where to find SLA status.
7. Recipe 12 — weekly digest deployed.

**Result:** Discount governance is automated; no more "we lost track of approval" excuses.

### Example 2: SLA breach auto-escalation in action

**Goal:** Tier 2 approval pending 28h → escalate to VP without manual intervention.

**Steps:**
1. AE submits 18% discount Monday 9am.
2. Manager doesn't respond by Tuesday 9am (24h SLA breached).
3. Recipe 6 cron runs Tuesday 10am.
4. Detects breach; reassigns to VP via REST; posts Slack #deal-desk-escalations.
5. VP responds within 12h; deal closes Wednesday.

**Result:** No deal-stalled-on-approval losses; reps trust the process.

### Example 3: Quarterly discount audit

**Goal:** Q3 review — discount discipline degrading?

**Steps:**
1. Recipe 11 — query Q3 vs Q2 trends.
2. Q3 has more Tier 3-4 approvals: 18% of deals vs Q2 9%.
3. Drill: which competitors? Which AEs?
4. Recipe 10 audit — reason codes; "strategic_logo" overused?
5. Discuss with sales leadership: tighten Tier 4 criteria; coach AEs.
6. Update reason-code dropdown; track Q4.

**Result:** Discount creep caught early; margin protected.

## Edge cases / gotchas

- **Approval process locks records** — while pending, AE can't edit. Use page layout to show "pending" status clearly.
- **Salesforce Approval recall** — AE can recall before action; tracked in ProcessInstanceHistory.
- **Approver delegation** — out-of-office: delegate set in user profile; Approval respects delegation.
- **Salesforce Approval emails go to inbox** — VPs ignore. Pair with Slack notification.
- **Manager hierarchy field** — `Owner.Manager` requires User Manager field populated; common missing config.
- **Approval steps for multiple approvers** — sequential vs parallel. Default sequential; parallel via `ParallelApproval` action.
- **HubSpot Approvals requires Enterprise tier** — Pro can't.
- **DealHub deal-desk module is separate purchase** — confirm in plan.
- **SLA calculation skips weekends?** — define business hours config; default is calendar hours.
- **Reason code freedom** — free-text reasons = unauditable. Force picklist with curated codes.
- **Multi-step approval ordering** — Tier 4 requires CRO + Finance both; parallel approval avoids serial delay.
- **Locked record gotcha** — record-triggered Flows can't update locked records. Workflow tries fail silently.
- **Mobile approval UX** — Salesforce mobile app + email-from-mobile work; rich approvals (large opportunities) clunky.
- **Approval-to-CPQ sync** — approved discount writes back to CPQ; if not, CPQ quote stays at list price.
- **Audit trail for approvals** — ProcessInstanceStep retains everything. Don't delete.
- **Exception escalation to CEO needs human touch** — auto-escalation past CRO not advisable; queue for SalesOps.

## Sources

- [Salesforce Approval Processes Help](https://help.salesforce.com/s/articleView?id=sf.approvals_intro.htm)
- [Salesforce ApprovalProcess Metadata](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_approvalprocesses.htm)
- [Salesforce Process Approvals REST](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_process_approvals.htm)
- [HubSpot Approvals (Enterprise)](https://knowledge.hubspot.com/approvals)
- [DealHub deal-desk module](https://dealhub.io/products/deal-desk/)
- [Discount governance benchmarks (Pavilion 2026)](https://www.joinpavilion.com/insights/sales-discounting)
- [Sales Approval SLA best practices](https://www.openview.com/saas-sales-approval/)
- [Conga Approvals (alternative)](https://docs.conga.com/approvals)
