<!--
Source: https://docs.salesforcespiff.com/disputes + https://docs.quotapath.com/ + https://help.captivateiq.com/disputes
Commission dispute resolution + audit trail — Spiff + QuotaPath + CaptivateIQ (June 2026 SOTA).
-->
# Commission Dispute Audit Trail — SKILL

5-day SLA, audit-trail-backed commission dispute resolution. **Spiff** (Salesforce-acquired) + **QuotaPath** (mid-market) + **CaptivateIQ** (enterprise alt) all support a structured dispute workflow. The agent's job: build the source-of-truth chain — CRM deal record → plan logic at time of payment → rate applied → SPIFs → clawbacks → net payable — and render an audit-trail PDF the AE + manager + finance can sign off on. 15-20% of comp time goes to disputes; this skill compresses it.

## When to use

- **AE files a dispute** — "I should have been paid $X, was paid $Y."
- **Reconstruct the calculation chain** — what plan version applied, what fields fired, what didn't.
- **Generate audit-trail PDF** — formal documentation for AE + finance.
- **Resolve + log** — recommend deny / approve / partial; update statement; close dispute in ICM tool.
- **Detect plan-logic ambiguity** — multiple disputes on the same SPIF? plan text is unclear → flag for revision.
- **Quarterly dispute analytics** — which AEs file most? which plan provisions trigger most disputes?
- **Trigger phrases**: "commission dispute", "audit trail", "Spiff dispute", "CaptivateIQ statement", "comp recalc", "SPIF dispute", "clawback dispute", "missed accelerator".

Do NOT use this skill for: **plan modeling / publish a new plan** (use `commission-spiff-quotapath-captivateiq`); **payroll handoff** (handed to `finance-controller`); **forecast attainment dispute** (use `forecasting-clari-boostup-aviso`).

## Setup

```bash
# Spiff — Personal API token (Settings → API Tokens)
export SPIFF_TOKEN="<token>"
export SPIFF_BASE="https://api.spiff.com/v1"

# QuotaPath — OAuth token
export QUOTAPATH_TOKEN="<token>"
export QUOTAPATH_BASE="https://api.quotapath.com/v1"

# CaptivateIQ — API key (Admin → Integrations → API)
export CAPTIVATEIQ_TOKEN="<token>"
export CAPTIVATEIQ_BASE="https://api.captivateiq.com/v1"

# Salesforce (source-of-truth deal record)
export MATON_API_KEY="<key>"

# PDF / docs
pip install reportlab jinja2 pandas requests

# Test connectivity
curl "$SPIFF_BASE/disputes?status=open" -H "Authorization: Bearer $SPIFF_TOKEN" | jq '.[:2]'
curl "$CAPTIVATEIQ_BASE/statements" -H "Authorization: Bearer $CAPTIVATEIQ_TOKEN" | jq '.[:1]'
```

Required:
- Admin role on the ICM tool (dispute log read + write)
- Salesforce admin or read-with-audit-fields scope (CreatedDate, LastModifiedDate, OwnerId changes)
- Notion for dispute SLA log

## Common recipes

### Recipe 1: Audit-trail template (canonical markdown)

```markdown
# Commission Dispute Audit Trail — Dispute ID: {{dispute_id}}

## Filer
- AE: {{ae_name}}
- Period: {{period}}
- Statement ID: {{statement_id}}
- Filed: {{filed_date}}
- Disputed amount: ${{disputed_amount}}

## Dispute claim
{{ae_narrative}}

## Source-of-truth chain
| Step | Source | Value | Notes |
|------|--------|-------|-------|
| Deal record | Salesforce Opp {{opp_id}} | ACV ${{acv}} | Closed-won {{close_date}} |
| Owner at close | Salesforce User {{owner_id}} | AE = filer? {{owner_match}} | |
| Plan logic at payment | {{tool}} Plan v{{plan_version}} effective {{plan_effective}} | | |
| Quota attainment at close | {{attainment_pct}}% of ${{quota}} | accelerator? {{accel}} | |
| Base commission | {{base_rate}}% × ${{acv}} | ${{base_comm}} | |
| Accelerator multiplier | {{accel_multiplier}}× | ${{accel_comm}} | |
| SPIF — {{spif_name}} | {{spif_condition}} | {{spif_eligible}} | |
| Clawback check | {{clawback_condition}} | {{clawback_applied}} | |
| Draw recovery | Draw outstanding? | {{draw_applied}} | |
| **Net paid** | | **${{net_paid}}** | |

## Discrepancy investigation
- Claim: AE expected ${{expected}} 
- Investigation: {{investigation_notes}}
- Plan reference: {{tool}} Plan v{{plan_version}}, section {{section}}
- Conclusion: {{conclusion}}

## Resolution
- Recommendation: {{recommendation}}
- Alternative: {{alternative}}
- Decision: {{decision}}
- Effective date: {{effective_date}}

## Plan changes triggered (if any)
- Plan: {{old_plan_version}} → {{new_plan_version}}
- Change: {{change_description}}
- Affected AEs (retro): {{affected_ae_count}} reps
- Retro-pay total: ${{retro_total}}
- Effective retro from: {{retro_effective}}

---
Audit log: filed {{filed_date}}; reviewed {{reviewed_date}}; resolved {{resolved_date}}; SLA {{sla_status}}
```

### Recipe 2: Spiff — list open disputes + fetch dispute details

```bash
# Open disputes
curl -s "$SPIFF_BASE/disputes?status=open" \
  -H "Authorization: Bearer $SPIFF_TOKEN" | jq '.[] | {id, user_id, period, amount_disputed, filed_at, reason}'

# Single dispute
curl -s "$SPIFF_BASE/disputes/DISPUTE_ID" \
  -H "Authorization: Bearer $SPIFF_TOKEN" | jq .

# Statement linked to the dispute
curl -s "$SPIFF_BASE/statements/STATEMENT_ID" \
  -H "Authorization: Bearer $SPIFF_TOKEN" | jq '{period, total, line_items: .line_items[:5]}'
```

### Recipe 3: Spiff — file resolution + close dispute

```bash
# Resolution payload
curl -X POST "$SPIFF_BASE/disputes/DISPUTE_ID/resolve" \
  -H "Authorization: Bearer $SPIFF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "decision": "denied",          # denied | approved | partial
    "resolution_amount": 0,        # USD adjustment if approved/partial
    "resolution_note": "Plan v2.3 section 3.b SPIF threshold is $100K; deal was $85K. See audit trail.",
    "audit_trail_url": "https://notion.so/team/dispute-12345"
  }'
```

### Recipe 4: CaptivateIQ — pull statement audit log

```bash
# Statement audit log includes every field-level change + calc trace
curl -s "$CAPTIVATEIQ_BASE/statements/STATEMENT_ID/audit_log" \
  -H "Authorization: Bearer $CAPTIVATEIQ_TOKEN" | jq '.events[] | {timestamp, event_type, field, before, after, actor}'

# Statement with line items
curl -s "$CAPTIVATEIQ_BASE/statements/STATEMENT_ID?include=line_items,calculation_trace" \
  -H "Authorization: Bearer $CAPTIVATEIQ_TOKEN" | jq '.calculation_trace'
```

CaptivateIQ's `calculation_trace` is the canonical artifact — every input + formula + output for each commission line item.

### Recipe 5: QuotaPath — fetch dispute + commission detail

```bash
# QuotaPath uses "exceptions" rather than "disputes"
curl -s "$QUOTAPATH_BASE/exceptions?status=open" \
  -H "Authorization: Bearer $QUOTAPATH_TOKEN" | jq '.[]'

# Commission detail per user per period
curl -s "$QUOTAPATH_BASE/users/USER_ID/commissions?period=2026-Q3" \
  -H "Authorization: Bearer $QUOTAPATH_TOKEN" | jq '.deals[]'
```

### Recipe 6: Salesforce — pull deal as it was at close (history audit)

```bash
# Current state
sf data query --target-org prod \
  --query "SELECT Id, Name, Amount, CloseDate, OwnerId, Owner.Name, StageName, Type, SBQQ__SubscriptionTerm__c FROM Opportunity WHERE Id = '006XX0000ABCDEF'" \
  --result-format json > opp_current.json

# Field history (AccountHistory / OpportunityFieldHistory for date-of-close snapshot)
sf data query --target-org prod \
  --query "SELECT Field, OldValue, NewValue, CreatedDate FROM OpportunityFieldHistory WHERE OpportunityId = '006XX0000ABCDEF' ORDER BY CreatedDate" \
  --result-format json > opp_history.json
```

Note: Opportunity field history must be enabled on the org. Salesforce retains 24 months by default.

### Recipe 7: Build audit-trail chain (Python)

```python
import json, requests, pandas as pd
from datetime import datetime

def build_audit_chain(dispute_id, tool="spiff"):
    # 1. Fetch dispute
    base = {"spiff": SPIFF_BASE, "captivateiq": CAPTIVATEIQ_BASE, "quotapath": QUOTAPATH_BASE}[tool]
    token = {"spiff": SPIFF_TOKEN, "captivateiq": CAPTIVATEIQ_TOKEN, "quotapath": QUOTAPATH_TOKEN}[tool]
    
    dispute = requests.get(f"{base}/disputes/{dispute_id}",
        headers={"Authorization": f"Bearer {token}"}).json()
    
    opp_id = dispute["deal_id"]  # Spiff stores the linked Salesforce Opp Id
    
    # 2. Fetch Salesforce Opp at current state + at close
    opp = requests.get(
        f"https://gateway.maton.ai/salesforce/services/data/v60.0/sobjects/Opportunity/{opp_id}",
        headers={"Authorization": f"Bearer {MATON_KEY}"}).json()
    
    # 3. Fetch plan version effective at payment date
    plan = requests.get(f"{base}/plans/{dispute['plan_id']}",
        headers={"Authorization": f"Bearer {token}"}).json()
    
    # 4. Reconstruct chain
    chain = {
        "opp_id": opp_id,
        "opp_amount": opp["Amount"],
        "owner": opp["OwnerId"],
        "close_date": opp["CloseDate"],
        "plan_version": plan["version"],
        "plan_effective": plan["effective_date"],
        "base_rate": plan["base_rate"],
        "accelerators": plan["accelerators"],
        "spifs_evaluated": [
            {
                "name": s["name"],
                "condition": s["condition"],
                "eligible": evaluate(s["condition"], opp)
            } for s in plan["spifs"]
        ],
        "clawbacks_evaluated": [
            {
                "name": c["name"],
                "condition": c["condition"],
                "applied": evaluate(c["condition"], opp)
            } for c in plan["clawbacks"]
        ],
        "net_paid": dispute["amount_paid"],
        "amount_disputed": dispute["amount_disputed"],
    }
    return chain

def evaluate(condition, context):
    """Stub — translates plan condition DSL to Python eval. Real impl uses safe AST."""
    # Example: condition "amount > 100000" + context.amount = 85000 → False
    # Use restricted-eval lib (asteval / simpleeval) in prod
    from simpleeval import simple_eval
    return simple_eval(condition, names={"amount": context["Amount"]})
```

### Recipe 8: Generate audit-trail PDF (jinja2 + reportlab)

```python
from jinja2 import Template
import subprocess

with open("dispute_template.md") as f:
    tmpl = Template(f.read())

chain = build_audit_chain("DISPUTE_ID")
md = tmpl.render(**chain)

with open(f"dispute_{chain['opp_id']}.md", "w") as f:
    f.write(md)

# Render md → pdf via pandoc (one-liner)
subprocess.run([
    "pandoc",
    f"dispute_{chain['opp_id']}.md",
    "-o", f"dispute_{chain['opp_id']}.pdf",
    "--pdf-engine=xelatex",
    "-V", "geometry:margin=1in"
], check=True)
```

### Recipe 9: SLA tracking — open dispute aging

```python
import pandas as pd
from datetime import datetime, timezone

disputes = requests.get(f"{SPIFF_BASE}/disputes?status=open",
    headers={"Authorization": f"Bearer {SPIFF_TOKEN}"}).json()

now = datetime.now(timezone.utc)
aged = []
for d in disputes:
    filed = datetime.fromisoformat(d["filed_at"].replace("Z", "+00:00"))
    business_days = pd.bdate_range(filed.date(), now.date()).size
    sla_status = "ok" if business_days <= 5 else ("at_risk" if business_days <= 7 else "breached")
    aged.append({
        "id": d["id"],
        "ae": d["user_email"],
        "filed": filed.date(),
        "business_days_open": business_days,
        "sla_status": sla_status,
        "amount": d["amount_disputed"]
    })

df = pd.DataFrame(aged).sort_values("business_days_open", ascending=False)
breached = df[df["sla_status"] == "breached"]

# Slack alert on breach
for _, r in breached.iterrows():
    requests.post("https://slack.com/api/chat.postMessage", json={
        "channel": "#commission-disputes",
        "text": f":alert: SLA breach — dispute {r['id']} ({r['ae']}), filed {r['filed']}, {r['business_days_open']} business days open. ${r['amount']:,.0f} disputed."
    }, headers={"Authorization": f"Bearer {SLACK_TOKEN}"})
```

### Recipe 10: Plan-logic ambiguity detection

```python
# Run quarterly — which plan provisions trigger > 1 dispute?
disputes = requests.get(f"{SPIFF_BASE}/disputes?status=resolved&since=2026-04-01",
    headers={"Authorization": f"Bearer {SPIFF_TOKEN}"}).json()

# Tag each dispute by the provision it touched (SPIF name, accelerator tier, clawback rule)
provision_disputes = pd.DataFrame([{
    "dispute_id": d["id"],
    "provision_type": d["disputed_provision"]["type"],  # spif | accelerator | clawback | base
    "provision_name": d["disputed_provision"]["name"],
    "resolution": d["resolution"]["decision"],
} for d in disputes])

# Count by provision
ambiguity = provision_disputes.groupby(["provision_type", "provision_name"]).agg(
    dispute_count=("dispute_id", "count"),
    approval_rate=("resolution", lambda s: (s == "approved").mean())
).sort_values("dispute_count", ascending=False)

# Flag provisions with > 3 disputes OR > 50% approval rate (i.e., plan was probably wrong)
flagged = ambiguity[(ambiguity["dispute_count"] > 3) | (ambiguity["approval_rate"] > 0.5)]
print("Plan provisions needing revision:")
print(flagged)
```

### Recipe 11: Bulk retroactive recalc (when plan amended)

```bash
# Spiff — recalculate statements for affected period
curl -X POST "$SPIFF_BASE/statements/recalculate" \
  -H "Authorization: Bearer $SPIFF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "plan_id": "PLAN_ID",
    "period_start": "2026-07-01",
    "period_end": "2026-09-30",
    "force": true,
    "audit_note": "Retroactive recalc after dispute 12345 — SPIF threshold lowered to $75K per leadership decision"
  }'
```

### Recipe 12: Dispute analytics — quarterly summary

```python
disputes_q = [d for d in disputes if "2026-Q3" in d["period"]]
summary = {
    "filed_count": len(disputes_q),
    "approved_count": sum(1 for d in disputes_q if d["resolution"]["decision"] == "approved"),
    "denied_count": sum(1 for d in disputes_q if d["resolution"]["decision"] == "denied"),
    "partial_count": sum(1 for d in disputes_q if d["resolution"]["decision"] == "partial"),
    "total_disputed": sum(d["amount_disputed"] for d in disputes_q),
    "total_adjusted": sum(d["resolution"]["amount"] for d in disputes_q),
    "median_resolution_business_days": pd.Series([
        pd.bdate_range(d["filed_at"][:10], d["resolved_at"][:10]).size for d in disputes_q
    ]).median(),
    "top_filers": pd.Series([d["user_email"] for d in disputes_q]).value_counts().head(5).to_dict(),
}
print(summary)
```

### Recipe 13: api-gateway fallback

```bash
curl "https://gateway.maton.ai/spiff/v1/disputes?status=open" \
  -H "Authorization: Bearer $MATON_API_KEY"

curl "https://gateway.maton.ai/captivateiq/v1/statements/STATEMENT_ID/audit_log" \
  -H "Authorization: Bearer $MATON_API_KEY"
```

## Examples

### Example 1: AE disputes missing SPIF

**Goal:** AE Jane claims $3K SPIF on $85K deal; comp shows no SPIF.

**Steps:**
1. Recipe 2 — pull dispute from Spiff.
2. Recipe 6 — pull Salesforce Opp current + history at close date.
3. Recipe 7 — build audit chain. SPIF condition evaluates to False (`amount > 100000` and amount is $85K).
4. Recipe 8 — render audit PDF.
5. Recipe 3 — file resolution: `denied` with audit_trail_url to notion page.
6. Slack Jane + her manager with PDF link.

**Result:** Dispute closed in 2 business days; AE has documented reason.

### Example 2: Pattern-find plan ambiguity

**Goal:** Spot the SPIF that keeps generating disputes; recommend a plan revision.

**Steps:**
1. Recipe 10 — run provision-level dispute analytics.
2. Identify "New Logo > $100K" SPIF — 7 disputes, 3 approved (43% approval).
3. Pattern: AEs interpret "New Logo" as "first deal with the account" but plan defines it as "account never had any contract."
4. Draft plan v2.4 with explicit definition; route to CRO for approval.
5. Recipe 11 — retro-recalc Q3 statements under new plan version (if leadership approves retro).
6. Memo to all AEs explaining clarification.

**Result:** SPIF dispute volume drops from 7 to 0-1 next quarter.

### Example 3: SLA breach escalation

**Goal:** Dispute open 6 business days; auto-escalate to VP Finance + CRO.

**Steps:**
1. Recipe 9 — daily SLA aging job.
2. Auto-Slack `#commission-disputes` on breach.
3. Auto-Slack DM filer's manager.
4. Email VP Finance via gmail-mcp with dispute summary + audit chain (Recipe 7).
5. Log breach in notion SLA dashboard.

**Result:** No dispute sits past 7 business days without exec visibility.

## Edge cases / gotchas

- **Plan version at time of close, not at time of payment** — comp is calculated at payment cycle but should reference the plan in effect when the deal closed. Always pull plan version by close_date, not by current effective plan.
- **Quota attainment at close vs at end of period** — accelerators kick in at attainment thresholds. If deal closed mid-quarter and AE was at 60% then, the accelerator applies as if 60%, not as if 110% by quarter-end. Some tools handle this; some don't.
- **Multi-currency disputes** — deal in EUR, paid in USD. FX rate at close, at payment, or at dispute date? Plan must specify; doc in audit chain.
- **Owner change mid-deal** — if deal changed owners after creation, split-credit rules apply. Don't compute as if current owner = original closer.
- **Retroactive plan amendments** — generally avoid retro changes; they erode trust. If unavoidable, retro only with explicit CRO sign-off + retro-pay (never retro-claw).
- **CaptivateIQ audit_log endpoint requires premium tier** — basic plans don't expose it. Fall back to UI export.
- **Spiff "amount_paid" can be net or gross** — depends on org config. Confirm in plan settings before assuming.
- **Disputes filed after payment processed** — once payroll has run, adjustments come as separate "true-up" line items on next statement, not as recalc. Document this in resolution.
- **Salesforce field history limited to 24 months** — older deal disputes lose history. Use `RecordSnapshot__c` custom field that captures close-date state for any disputed-deal-eligible record.
- **Free-text plan provisions** — disputes spike when plan documentation uses ambiguous wording ("substantial", "significant", "approximately"). Quarterly plan-text audit to remove these.
- **AE turnover during dispute window** — AE leaves before dispute resolves. Don't auto-deny; resolve on merit and route final payment per termination agreement.
- **Clawback timing** — clawback applied at churn date, but commission was paid X months earlier. Some orgs hold a reserve; others pull back from next pay. Plan must say.
- **Cross-team commission splits** — SDR + AE + CSM split. Disputes can come from any role; audit chain must show full split logic.
- **PDF should not be the source of truth** — the source of truth is the source-of-truth chain in the ICM tool + Salesforce. The PDF is documentation. Don't paper over data corrections by editing the PDF.
- **Privacy** — audit trails contain comp data. Restrict notion / drive access to filer + manager + finance + SalesOps only.

## Sources

- [Spiff (Salesforce) — Disputes Documentation](https://docs.salesforcespiff.com/disputes)
- [Spiff API Reference](https://docs.salesforcespiff.com/api/)
- [QuotaPath API + Exceptions Workflow](https://docs.quotapath.com/)
- [CaptivateIQ — Disputes Workflow](https://help.captivateiq.com/hc/en-us/categories/360003486553-Disputes)
- [CaptivateIQ — Statement Audit Log](https://help.captivateiq.com/hc/en-us/articles/360051041713)
- [Salesforce Field History Tracking](https://help.salesforce.com/s/articleView?id=sf.tracking_field_history.htm)
- [WorldatWork — Sales Comp Dispute Best Practices](https://worldatwork.org/resources/publications/sales-compensation-dispute-resolution)
- [Pavilion — Commission Dispute Patterns](https://www.joinpavilion.com/resources/commission-disputes)
- [Salesforce Spiff Onboarding Guide](https://docs.salesforcespiff.com/admin-quickstart)
- [Pandoc — Markdown to PDF](https://pandoc.org/MANUAL.html)
