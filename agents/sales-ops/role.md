# Sales Operations — deep reference

This appends to `AGENT.md`. **Not** in the agent's default context. Grep when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "SalesOps technology categories", "Salesforce admin playbook", "HubSpot Operations Hub playbook", "Tooling API field-usage audit", "SFDX deploy workflow", "Validation rule patterns", "Lightning Flow patterns", "HubSpot Workflow patterns", "Commission plan modeling playbook", "Commission dispute audit-trail template", "ICM source-of-truth chain", "Salesforce CPQ rollout playbook", "Pricing rule patterns", "Approval Process playbook", "Lead routing playbook", "LeanData routing patterns", "Chili Piper routing patterns", "Duplicate management playbook", "Cloudingo dedup patterns", "Fuzzy match thresholds", "Enrichment waterfall playbook", "Apollo ZoomInfo Clay source order", "Pipeline metrics methodology", "Stage criteria template", "Salesforce Account Hierarchy playbook", "Forecasting methodology", "Three-bucket discipline", "Commit accuracy tracking", "Territory planning playbook", "Anaplan + Fullcast", "Salesforce TM2", "Rep performance dashboard playbook", "Salesforce CRMA dataset deploy", "Looker LookML patterns", "Stalled-deal alert spec", "Engagement signal sources", "Deal desk discount approval matrix", "Approval SLA tracking", "Win/loss reporting playbook", "Drift detection patterns", "Sales tech stack audit playbook", "Utilization scoring", "Ramp-to-quota analysis playbook", "Cohort table patterns", "Sales enablement infrastructure playbook", "Highspot tag taxonomy", "SalesOps onboarding runbook", "SOTA tool reference".

For provenance, see `SOURCES.md`.

---

## Capability reference

### SalesOps motions this agent handles

- CRM admin (Salesforce / HubSpot / Pipedrive / Dynamics / Attio / Zoho) — custom objects, fields, validation rules, flows, formulas, page layouts, record types, approval processes, page-layout governance
- Sales engagement tech-stack admin (Salesloft / Outreach / Gong / Apollo / Clay)
- Commission plan administration (Spiff / QuotaPath / CaptivateIQ / Performio / Xactly / Everstage)
- Commission dispute resolution + audit trail
- Salesforce CPQ + Conga CPQ + DealHub CPQ configuration (pricing rules, product bundles, approval rules, quote-to-cash)
- Lead routing (LeanData / Chili Piper / Distribute / native Salesforce assignment)
- Duplicate management (LeanData Dedup / Cloudingo / DupeBlocker / native dedup / custom fuzzy match)
- Data enrichment orchestration (ZoomInfo / Apollo / Clay / Demandbase / LeadIQ — waterfall + trigger-based)
- Pipeline metrics + reporting (velocity, conversion %, deal age, win rate, coverage ratio)
- Pipeline-stage definition + criteria-based progression (validation rule enforcement)
- Territory planning + assignment (Salesforce TM2 / Anaplan / Fullcast / k-means clustering)
- Forecasting (Clari / BoostUp / Aviso / manual three-bucket via CRM + Sheets)
- Forecast accuracy improvement + commit accuracy tracking per AE
- Sales enablement infrastructure (Highspot / Showpad / Seismic / Mindtickle)
- Deal desk operations (discount approval routing, exception management, SLA tracking)
- Rep performance dashboards (Salesforce CRMA / Looker / Sigma / Hex / google-sheets)
- Sales attainment dashboards (quota attainment per rep + per team)
- Stalled-deal alerts + engagement signal scoring
- Ramp-to-quota analysis (new-hire cohort tracking)
- Contact-account hierarchy maintenance (Salesforce Account Hierarchy + D&B Direct+ refresh)
- Win/loss reporting at scale (quarterly rollup + drift detection)
- Sales tech stack consolidation audit (utilization scoring + renegotiation)
- Lead-to-opportunity conversion hygiene
- Schema audit + custom field cleanup
- Salesforce CRMA / Einstein Analytics / Tableau CRM dashboard ops

### SalesOps technology categories (for reference)

- **CRM:** Salesforce (Sales Cloud, Revenue Cloud), HubSpot (Sales Hub + Operations Hub), Pipedrive, Attio, Microsoft Dynamics 365 Sales, Zoho CRM, Zoho Bigin, Folk, Copper
- **CRM admin tooling:** SFDX CLI, Salesforce Inspector, Workbench, DemandTools, Cloudingo, Validity, Conga Composer
- **Sales engagement (admin scope):** Salesloft, Outreach, lemlist, Reply.io, instantly.ai, Smartlead, La Growth Machine, HeyReach
- **Conversation intelligence (admin scope):** Gong, Chorus.ai, Fathom, tl;dv, Fireflies, Otter.ai, Avoma
- **Commission / ICM / SPM:** Spiff (Salesforce), QuotaPath, CaptivateIQ, Performio, Xactly, Everstage, Forma.ai, CompCloud, Beqom, Iconixx, Varicent, Anaplan Incentive Compensation
- **CPQ:** Salesforce CPQ (Steelbrick), Conga CPQ (Apttus), DealHub CPQ, Pricefx, Subskribe, Salesforce Revenue Cloud (Vlocity)
- **Forecasting / revenue intelligence:** Clari, Clari Align, BoostUp, Aviso, InsightSquared (Mediafly), Gong Forecast, Salesforce Sales Cloud forecasting
- **Lead routing:** LeanData (Salesforce-native), Chili Piper, Distribute, RouterDB, Default, OpenPrise routing, RingDNA routing
- **Duplicate management:** LeanData Dedup, Cloudingo, DupeBlocker (Validity), RingLead, DemandTools, native Salesforce Duplicate Rules
- **Data enrichment:** Apollo, ZoomInfo, Clay, Demandbase, LeadIQ, Lusha, Cognism, Crunchbase, D&B Hoovers
- **Territory + quota planning:** Anaplan, Varicent Territory, Salesforce Territory Management 2.0, Fullcast, RingLead Cleanse + Route
- **Sales enablement:** Highspot, Showpad, Seismic, Lessonly, Mindtickle, Brainshark, Allego, Bigtincan
- **Sales analytics:** Salesforce CRMA (Tableau CRM / Einstein Analytics), HubSpot Reports, Looker, Sigma, Mode, Hex, Tableau, Power BI, Domo
- **Warehouse + transformation:** Snowflake, BigQuery, Databricks, Redshift, dbt, Fivetran, Hightouch, Census, Segment
- **Deal desk + approvals:** Salesforce Approval Process, HubSpot Approvals, DealHub deal-desk module, native CPQ approval rules

---

## Salesforce admin playbook

### SFDX deploy workflow

```bash
# 1. Pull current org metadata into a project
sf project retrieve start --metadata CustomField:Opportunity.SBQQ__SubscriptionTerm__c

# 2. Edit force-app/main/default/objects/Opportunity/fields/
# (add validation rules, formulas, flows, etc.)

# 3. Validate to sandbox
sf project deploy start --target-org sandbox --test-level RunLocalTests --check-only

# 4. Deploy to sandbox
sf project deploy start --target-org sandbox --test-level RunLocalTests

# 5. Smoke test in sandbox UI
# (create record, trigger validation, verify flow fires, confirm dashboard updates)

# 6. Promote to production
sf project deploy start --target-org production --test-level RunLocalTests
```

### Tooling API field-usage audit

```bash
# Query custom field nullity to find unused fields
sf data query --query "SELECT EntityDefinition.QualifiedApiName, DeveloperName, DataType FROM CustomField WHERE ManageableState = 'unmanaged'" --use-tooling-api

# For each field, run a nullity check:
sf data query --query "SELECT COUNT(Id) total, COUNT(<FieldName__c>) populated FROM <Object>"

# If populated / total < 20%, mark as deprecation candidate
# Then check report usage via Tooling API:
sf data query --query "SELECT Id, DeveloperName FROM Report WHERE FieldName__c IN <field list>" --use-tooling-api

# And workflow / flow usage:
sf data query --query "SELECT Id, MasterLabel FROM Flow WHERE DefinitionId IN (SELECT Id FROM FlowDefinition WHERE DeveloperName LIKE '%<field>%')" --use-tooling-api
```

### Validation rule patterns

```
// MEDDIC champion required to advance to "Evaluation" stage
AND(
  ISCHANGED(StageName),
  TEXT(StageName) = "Evaluation",
  OR(
    ISBLANK(Champion__c),
    ISBLANK(Champion_Advocacy_Note__c)
  )
)

// Discount > 20% requires approval reason
AND(
  Discount_Percent__c > 20,
  ISBLANK(Discount_Approval_Reason__c)
)

// Close date in past blocks save for open opps
AND(
  NOT(IsClosed),
  CloseDate < TODAY()
)
```

### Lightning Flow patterns

- **Record-triggered flow on Opportunity update** — fires on stage advance to enforce required fields (validation rules block save; record-triggered flow auto-fills or routes to approval)
- **Scheduled flow** — daily stalled-deal scan: find opps in stage > 1.5× median, no recent activity, send Slack alert via outbound action
- **Screen flow** — guided commission dispute filing: AE inputs deal + statement period + dispute reason → flow generates audit-trail request + creates dispute Case + auto-routes to SalesOps

### Concrete example — discount approval flow

```
Trigger: Opportunity update where Discount_Percent__c > 10 AND Approval_Status__c != 'Approved'
Decision:
  - Discount 10-20% → Submit for Approval → Manager queue
  - Discount 20-30% → Submit for Approval → VP Sales queue
  - Discount > 30% → Submit for Approval → CRO queue + Finance Slack notification
Approval Process: Salesforce native approval process per tier
SLA: 24h tier 2; 48h tier 3; 72h tier 4 → escalation if breached
```

---

## HubSpot Operations Hub playbook

### Workflow patterns

```
# Stage-criteria-based progression (HubSpot Workflow JSON via api-gateway)
POST https://gateway.maton.ai/hubspot/automation/v4/flows
{
  "name": "Discovery to Evaluation - Validation",
  "enabled": true,
  "type": "DRAFT",
  "actions": [
    {
      "type": "BRANCH",
      "filters": [
        {
          "filterType": "PROPERTY",
          "property": "champion_name",
          "operator": "IS_EMPTY"
        }
      ],
      "trueBranch": {
        "type": "SET_PROPERTY",
        "property": "deal_stage_blocked",
        "value": "true"
      },
      "falseBranch": {
        "type": "ALLOW_STAGE_ADVANCE"
      }
    }
  ]
}
```

### Custom-coded action pattern (Operations Hub Pro)

```javascript
// Operations Hub custom-coded action — daily enrichment trigger
exports.main = async (event, callback) => {
  const { domain, contactId } = event.inputFields;

  // Hit Apollo first via api-gateway
  const apollo = await fetch(`https://gateway.maton.ai/apollo/api/v1/organizations/enrich?domain=${domain}`, {
    headers: { 'Authorization': `Bearer ${process.env.MATON_KEY}` }
  });
  const data = await apollo.json();

  callback({
    outputFields: {
      industry: data.industry,
      employee_count: data.estimated_num_employees,
      tech_stack: data.technologies.join(',')
    }
  });
};
```

### Data sync mapping (PieSync successor)

- Source: Salesforce Account
- Target: HubSpot Company
- Field map: Name → name, BillingCountry → country, NumberOfEmployees → numberofemployees
- Conflict resolution: source-wins (Salesforce master), target-overwrites-empty (fill blanks only)

---

## Commission plan modeling playbook

### Plan logic chain (source-of-truth)

```
Source CRM Deal Record
  → Plan Eligibility (AE assignment, deal close date in period, product type)
  → Base Rate (e.g., 8% of ACV for new business; 4% of ACV for renewal; 6% of ACV for expansion)
  → Accelerators (over-quota uplift: 100-110% = 1.5×, 110-130% = 2×, > 130% = 2.5×)
  → SPIFs (one-time bonuses: new logo > $100K = $5K SPIF, multi-year deal = $2K SPIF)
  → Clawbacks (deal churns within 6 months = 100% commission clawback; payment default > 90 days = 50% clawback)
  → Draws (guaranteed minimum monthly $X; recoverable from future earnings)
  → Net Payable
```

### Commission plan modeling template (Spiff / QuotaPath / CaptivateIQ)

```yaml
plan_name: "AE_New_Business_2026Q3"
effective_date: 2026-07-01
end_date: 2026-09-30
target_audience:
  role: AE
  segment: enterprise
quota:
  amount: 250000  # USD per quarter
  measure: ACV closed-won in period
base_commission:
  rate: 0.08  # 8% of ACV
  applies_to: new_logo
accelerators:
  - threshold: 1.00  # 100% of quota
    multiplier: 1.5
  - threshold: 1.10
    multiplier: 2.0
  - threshold: 1.30
    multiplier: 2.5
spifs:
  - name: "New Logo > $100K"
    condition: "amount > 100000 AND deal_type = new_logo"
    bonus: 5000
  - name: "Multi-year (3yr+)"
    condition: "term_months >= 36"
    bonus: 2000
clawbacks:
  - name: "Churn within 6mo"
    condition: "churned_within_days <= 180"
    percentage: 1.00  # 100% clawback
  - name: "Payment default 90d+"
    condition: "payment_overdue_days >= 90"
    percentage: 0.50
draws:
  monthly_minimum: 5000
  recoverable: true
```

### Pre/post comp delta workflow

1. Snapshot current plan + last 6 months of closed-won deals
2. Run current plan logic → compute baseline comp per AE per period
3. Apply proposed plan logic → compute new comp per AE per period
4. Render delta table (AE / Baseline / Proposed / Delta % / Delta $)
5. Flag anyone with > 10% delta + leadership notification
6. Generate test statements for top 5 reps + 2 edge cases (lowest-paid, highest-paid, ramp-tier, terminated)

---

## Commission dispute audit-trail template

```markdown
# Commission Dispute Audit Trail — [Dispute ID]

## Filer
- AE: ___
- Period: 2026 Q3 (Jul-Sep)
- Statement ID: ___
- Filed: 2026-10-08
- Disputed amount: $___

## Dispute claim
[AE narrative — what they claim should have been paid vs. what was paid]

## Source-of-truth chain
| Step | Source | Value | Notes |
|---|---|---|---|
| Deal record | Salesforce Opp 006XX0000... | ACV $85,000 | Closed-won 2026-09-15 |
| Owner at close | Salesforce User 005XX0000... | AE = filer | Confirmed |
| Plan logic at payment | Spiff Plan v2.3 effective 2026-07-01 | Base 8% + accelerator | |
| Quota attainment at close | 105% of $250K | 1.5× accelerator applies | |
| Base commission | 8% × $85K | $6,800 | |
| Accelerator multiplier | 1.5× | $10,200 | |
| SPIF — new logo > $100K | Condition: ACV > $100K? | NO ($85K) | Not eligible |
| Clawback check | Churn within 180d? | NO (account active) | Not applied |
| Draw recovery | Draw outstanding? | NO | Not applied |
| **Net paid** | | **$10,200** | |

## Discrepancy investigation
- Claim: AE expected $13,200 ($10,200 + $3,000 SPIF)
- Investigation: SPIF condition is `ACV > $100,000`. Deal ACV is $85,000. SPIF not eligible per plan.
- Plan reference: Spiff Plan v2.3 effective 2026-07-01, section 3.b
- Conclusion: payment is correct per plan logic at time of close

## Resolution
- Recommendation: deny dispute with audit-trail explanation
- Alternative: if SPIF threshold is intended to be $75K (per leadership Slack 2026-08-22), update plan + retro-pay $3,000
- Decision: ___
- Effective date: ___

## Plan changes triggered (if any)
- Plan: Spiff Plan v2.3 → v2.4
- Change: SPIF threshold $100K → $75K
- Affected AEs (retro): 7 reps
- Retro-pay total: $21,000
- Effective retro from: 2026-07-01
```

---

## Salesforce CPQ rollout playbook

### Pricing rule patterns

```
# Tiered pricing (volume discount)
Product: Seat License
  - 1-50 seats: $200/seat/year
  - 51-200 seats: $175/seat/year (12.5% discount)
  - 201-500 seats: $150/seat/year (25% discount)
  - 501+ seats: $125/seat/year (37.5% discount)

# Multi-year discount (ramp deal)
Term: 3-year contract
  - Year 1: 100% of list
  - Year 2: 95% of list
  - Year 3: 90% of list
  - Pre-bill discount: 5% if Y1 + Y2 + Y3 paid upfront

# Bundle discount
Bundle: Platform + Analytics + AI
  - Sum of components: $50K
  - Bundle price: $35K (30% discount)
  - Requires: all 3 components selected

# Channel partner override
Partner tier: Gold
  - Auto-apply 15% partner discount on all products
  - Approval required: NO (auto-eligible)
```

### Bundle dependency rules

```
# Required dependency
Product A (Platform) → IF selected → REQUIRE Product B (Support Package)

# Mutually exclusive
Product C (Annual Plan) → IF selected → EXCLUDE Product D (Monthly Plan)

# Recommended add-on
Product A (Platform) → IF selected → RECOMMEND Product E (Onboarding Services)
```

### Approval Process playbook

| Discount tier | Threshold | Approver | SLA | Escalation |
|---|---|---|---|---|
| Tier 1 | < 10% | AE self-approve | n/a | n/a |
| Tier 2 | 10-20% | Manager | 24 hours | → VP Sales after 36h |
| Tier 3 | 20-30% | VP Sales | 48 hours | → CRO after 72h |
| Tier 4 | > 30% | CRO + Finance | 72 hours | → CEO after 96h |
| Strategic exception | Any | Deal desk + CRO | Case-by-case | n/a |

---

## Lead routing playbook

### LeanData routing patterns

```
Trigger: Lead Created OR Form Submission
Step 1: Match to existing Account
  - If match → route to existing Account Owner
  - If no match → continue
Step 2: ICP fit score check
  - Score < 50 → route to Nurture queue
  - Score >= 50 → continue
Step 3: Segment routing
  - Enterprise (> 1000 employees) → Enterprise AE pod (round-robin)
  - Mid-market (200-1000) → MM AE pod (round-robin)
  - SMB (< 200) → SDR pod (round-robin)
Step 4: Geo override
  - EMEA → EMEA team
  - APAC → APAC team
  - Other → North America team
Step 5: ABM tier override
  - Tier 1 ABM account → named AE (bypass round-robin)
Step 6: Calendar slot booking via Chili Piper
  - Auto-book first available slot with assigned AE
```

### Chili Piper routing patterns

```javascript
// Chili Piper router config via api-gateway
POST https://gateway.maton.ai/chilipiper/api/v1/routers
{
  "name": "Inbound Demo Request",
  "router_type": "round_robin",
  "queue_users": ["ae1@co.com", "ae2@co.com", "ae3@co.com"],
  "filter_rules": [
    { "field": "country", "operator": "IN", "values": ["US", "CA"] },
    { "field": "company_size", "operator": "GTE", "value": 200 }
  ],
  "fallback_router": "smb_router_id",
  "calendar_integration": "google",
  "meeting_buffer_minutes": 15
}
```

---

## Duplicate management playbook

### Fuzzy match thresholds

```
Email exact match → 100% confidence → auto-merge
Email + phone exact match → 100% → auto-merge
Normalized name (Levenshtein < 2) + domain exact → 95% → auto-merge
Normalized name + phone exact (no email) → 90% → auto-merge
Normalized name (Levenshtein < 3) + same city + same employer → 75% → human-review queue
Normalized name only → < 50% → suppress (likely twin / father-son / common name)
```

### Cloudingo / LeanData Dedup workflow

1. Schedule daily scan via `api-gateway` (Cloudingo) or in-Salesforce (LeanData Dedup)
2. Categorize matches by confidence threshold above
3. Auto-merge above 90% → log to dedup audit table
4. Human-review queue 75-90% → render in `notion` for SalesOps reviewer
5. Suppress < 75% → log reason for future tuning
6. Weekly accuracy review: any twin-as-one false positives? Any missed obvious dupes?

### Custom Python fuzzy dedup (when Cloudingo unavailable)

```python
# Run via cli-anything
import pandas as pd
from rapidfuzz import fuzz, process

leads = pd.read_csv('salesforce_leads.csv')
leads['email_normalized'] = leads['email'].str.lower().str.strip()
leads['name_normalized'] = leads['first_name'].str.lower() + ' ' + leads['last_name'].str.lower()

# Find duplicates by normalized email
dupes_by_email = leads[leads.duplicated('email_normalized', keep=False)]

# Fuzzy match by name + domain for missing-email cases
for idx, row in leads[leads['email_normalized'].isna()].iterrows():
    matches = process.extract(
        row['name_normalized'],
        leads['name_normalized'].tolist(),
        scorer=fuzz.token_sort_ratio,
        limit=5
    )
    high_confidence = [m for m in matches if m[1] >= 90 and m[0] != row['name_normalized']]
    # ... merge logic
```

---

## Enrichment waterfall playbook

### Apollo → ZoomInfo → Clay → Demandbase source order

```
Trigger: Lead Created (HubSpot) OR Lead converted from Form (Salesforce)

Step 1: Apollo (cost-efficient B2B baseline)
  - Hit api-gateway: POST /apollo/api/v1/people/match
  - Fields written: title, seniority, function, company size, industry
  - Cost: ~$0.10 per match
  - Fallback: ZoomInfo if Apollo returns "not found"

Step 2: ZoomInfo (gaps + Scoops intent)
  - Hit api-gateway: POST /zoominfo/persons/enrich
  - Fields written: mobile phone, scoops_intent_topics
  - Cost: ~$0.50 per match
  - Conditional: only if Apollo missing phone OR account has > $500K TAM

Step 3: Clay (multi-source for stubborn gaps)
  - Hit Clay workflow trigger via api-gateway
  - Tries: Hunter, RocketReach, Dropcontact, AeroLeads
  - Cost: ~$0.30 per match
  - Conditional: only if Apollo + ZoomInfo both missed

Step 4: Demandbase (ABM intent overlay)
  - Hit api-gateway: POST /demandbase/account-intent
  - Fields written: intent_topics, surge_score
  - Cost: subscription-based (no per-record)
  - Conditional: only for ABM tier-1 accounts

Spend cap: $5 per enriched contact (alert + suppress beyond)
Field-write rule: ZoomInfo phone wins over Apollo; Demandbase intent wins all
```

---

## Pipeline metrics methodology

### Velocity (Sales Velocity formula)

```
Sales Velocity = (Win Rate × Average Deal Size × Open Opps) / Sales Cycle Days

Example:
  Win Rate = 28%
  Average Deal Size = $45,000
  Open Opps = 120
  Sales Cycle = 60 days

  Velocity = (0.28 × 45000 × 120) / 60 = $25,200 / day
```

### Stage conversion %

```
Per stage, last 4 quarters:
  Conversion % = (deals that advanced to next stage) / (deals that entered this stage)

  Stage 1 (Prospect → Discovery): 40%
  Stage 2 (Discovery → Evaluation): 55%
  Stage 3 (Evaluation → Proposal): 60%
  Stage 4 (Proposal → Negotiation): 70%
  Stage 5 (Negotiation → Closed): 75%

  Overall conversion (Prospect → Closed-Won): 40% × 55% × 60% × 70% × 75% = 6.9%
```

### Deal age in stage

```
Per stage, median time-in-stage (last 4 quarters):
  Prospect: 14 days
  Discovery: 21 days
  Evaluation: 35 days
  Proposal: 21 days
  Negotiation: 14 days

  Stale-deal threshold: 1.5× median
  Flag for review: in-stage longer than threshold
  Auto-alert via slack-mcp + recommended NBA from sales-agent
```

### Stage criteria template

```markdown
## Stage 3 — Evaluation

### Entry criteria
- [ ] Champion identified (Salesforce field: Champion__c populated + Champion_Advocacy_Note__c populated)
- [ ] Pain articulated by prospect (Salesforce field: Identified_Pain__c populated, > 50 chars)
- [ ] Technical evaluator named (Salesforce field: Technical_Evaluator__c populated)

### Exit criteria (to advance to Proposal)
- [ ] Decision criteria documented (Salesforce field: Decision_Criteria__c populated, > 100 chars)
- [ ] Economic buyer named (Salesforce field: Economic_Buyer__c populated)
- [ ] Demo completed (Salesforce activity: Demo type, after stage entry date)
- [ ] Verbal interest confirmed (Champion or EB)

### Validation rule
- Save blocked if advancing to Proposal without all 4 exit criteria met
```

---

## Forecasting methodology

### Three-bucket discipline

- **Commit (> 80% confidence):** MEDDIC ≥ 2.5/3 on all fields, EB confirmed close date, MAP signed (deals > 60 days), competition known and our position confirmed. AE is accountable to deliver. Sit-down with manager weekly if pattern of missed commits.
- **Best Case (50-80%):** MEDDIC mostly validated, champion engaged, EB awareness confirmed, close date in period. AE works active risks; reports weekly delta.
- **Pipeline (< 50%):** Discovery complete, qualification in progress. Counts toward coverage, not commit. No expected impact on this period.

### Commit accuracy tracking

```
Per AE per quarter:
  Commit Accuracy % = (commit deals that actually closed in period) / (total commit deals)

  Target: > 80%
  Action thresholds:
    > 80%: Confirmed forecaster — promote to commit-bucket review
    70-80%: Acceptable — coach on tightening commit criteria
    60-70%: Retraining — sit-in on next forecast call
    < 60%: Ride-along — manager joins every forecast meeting

Slippage tracking:
  Slipped deals = commit deals that missed close date but eventually closed
  Pull-ins = best-case deals that closed ahead of forecast date

  Both are normal; chronic patterns are coaching signals
```

### Forecast snapshot diff (weekly)

```python
# Run via cli-anything
import pandas as pd

this_week = pd.read_csv('forecast_2026_10_08.csv')
last_week = pd.read_csv('forecast_2026_10_01.csv')

merged = this_week.merge(last_week, on='opp_id', suffixes=('_now', '_prev'))

# Detect bucket movement
merged['bucket_change'] = merged['bucket_now'] != merged['bucket_prev']
slipped = merged[(merged['bucket_prev'] == 'Commit') & (merged['bucket_now'] != 'Commit')]
pulled_in = merged[(merged['bucket_prev'] != 'Commit') & (merged['bucket_now'] == 'Commit')]

# Render diff doc to Notion + Slack digest to manager
```

---

## Territory planning playbook

### Salesforce TM2 (native)

```bash
# Bulk territory assignment via SOQL + Composite API
sf data query --query "SELECT Id, Name, BillingCountry, AnnualRevenue FROM Account WHERE Type = 'Customer'" > accounts.csv

# Apply territory assignment logic (Python via cli-anything)
python territory_assign.py accounts.csv > assignments.csv

# Bulk update via Composite API
sf data upsert bulk --sobject Account --external-id Id --file assignments.csv --wait 10
```

### K-means territory clustering (Python)

```python
# Run via cli-anything
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np

accounts = pd.read_csv('accounts.csv')
# Features: lat/lng (geo) OR (acv_band, vertical, employee_band) (segment-based)
X = accounts[['lat', 'lng', 'employee_count_log', 'tam_score']].values

# K = number of territories
kmeans = KMeans(n_clusters=15, random_state=42, n_init=10)
accounts['territory_id'] = kmeans.fit_predict(X)

# Balance check — each territory has similar # of accounts + similar total TAM
balance = accounts.groupby('territory_id').agg({'tam_score': 'sum', 'id': 'count'})
# Iterate: swap accounts between adjacent territories to balance
```

---

## Rep performance dashboard playbook

### Salesforce CRMA dataset deploy

```bash
# 1. Define dataset from SOQL
sf wave dataset create --name "Pipeline_Velocity_2026Q3" --label "Pipeline Velocity Q3 2026"

# 2. Upload data via SAQL or external source
sf wave dataset upload --name "Pipeline_Velocity_2026Q3" --file q3_velocity.csv

# 3. Create dashboard with predefined widgets
sf wave dashboard create --file pipeline_velocity_dashboard.json
```

### Looker LookML patterns

```lookml
# explore: opportunities
explore: opportunity {
  join: account {
    sql_on: ${opportunity.account_id} = ${account.id} ;;
  }
  join: user {
    sql_on: ${opportunity.owner_id} = ${user.id} ;;
  }
}

measure: win_rate {
  type: number
  sql: SAFE_DIVIDE(
    COUNTIF(${stage_name} = 'Closed Won'),
    COUNTIF(${is_closed})
  ) ;;
  value_format: "0.0%"
}

measure: avg_cycle_days {
  type: average
  sql: DATE_DIFF(${closed_date}, ${created_date}, DAY) ;;
}

# dashboard.lkml: AE-level scorecard
dashboard: ae_scorecard {
  title: "AE Performance Scorecard"
  filters:
    - name: ae
      title: "Account Executive"
      field: user.name

  element: pipeline_created {
    type: single_value
    measure: opportunity.pipeline_amount_qtd
  }
  # ... etc
}
```

---

## Stalled-deal alert spec

```python
# Run as scheduled flow or cron
# Pulls Salesforce + queries stale deals + Slack alert

import requests
from datetime import datetime, timedelta

# 1. Query stale deals via api-gateway
query = """
SELECT Id, Name, Amount, StageName, Owner.Name,
       LastModifiedDate, Last_Activity_Date__c
FROM Opportunity
WHERE IsClosed = FALSE
  AND Last_Activity_Date__c < N_DAYS_AGO:14
  AND CALENDAR_DAYS_IN_CURRENT_STAGE__C > 1.5 * CURRENT_STAGE_MEDIAN_DAYS__C
"""
deals = requests.get('https://gateway.maton.ai/salesforce/services/data/v60.0/query',
                     params={'q': query}, headers={'Authorization': f'Bearer {MATON_KEY}'}).json()

# 2. For each, recommend NBA (hand off to sales-agent for the literal copy)
for deal in deals['records']:
    nba = "Multi-thread to economic buyer this week" if deal['Stage'] in ['Evaluation', 'Proposal'] else "Diagnose stall — call champion"

    # 3. Slack alert
    requests.post('https://slack.com/api/chat.postMessage', json={
        'channel': '#sales-alerts',
        'text': f":warning: STALE: {deal['Name']} ${deal['Amount']:,.0f} | {deal['StageName']} | last activity {deal['Last_Activity_Date__c']} | NBA: {nba} | <{deal_url}|view>"
    }, headers={'Authorization': f'Bearer {SLACK_TOKEN}'})
```

### Engagement signal sources

| Source | Signal | Weight |
|---|---|---|
| Salesforce activity | Last activity date | High (recency) |
| Gong call | Call attended in last 7 days | High |
| Gong sentiment | Sentiment shift (positive → neutral → negative) | Critical |
| Email engagement | Open in last 7 days | Medium |
| Email engagement | Reply in last 7 days | High |
| Calendar | Meeting scheduled in next 14 days | High |
| Champion engagement | Champion responded in last 7 days | Critical |
| Multi-thread depth | Stakeholders engaged | Medium (deal size > $50K) |
| Days in stage | > 1.5× median | High (stall risk) |

---

## Deal desk discount approval matrix

| Discount | Auto-approver | SLA | Escalation if breached |
|---|---|---|---|
| 0-10% | AE (self) | n/a | n/a |
| 10-20% | Manager | 24 hours | → VP Sales |
| 20-30% | VP Sales | 48 hours | → CRO |
| 30-40% | CRO + Finance | 72 hours | → CEO + Board |
| > 40% | Special exception only | Case-by-case | Strategic deal review |

### Approval SLA tracking

```python
# Daily SLA breach check
slas_breached = query("""
SELECT Id, OpportunityId, SubmittedById, CreatedDate
FROM ProcessInstance
WHERE Status = 'Pending'
  AND CreatedDate < N_HOURS_AGO:24  # Tier 2 SLA
""")

for breach in slas_breached:
    # Slack escalation
    slack_post(channel='#deal-desk-escalations',
               text=f"SLA breach: Opp {breach.OpportunityId}, submitted {breach.CreatedDate}, awaiting tier-2 approver. Auto-escalating to VP.")
    # Reassign approval
    reassign_approval(breach.Id, 'vp_sales_user_id')
```

---

## Win/loss reporting playbook

### Quarterly rollup query

```sql
-- Run against dbt-modeled fct_opportunities in warehouse via postgresql-mcp
SELECT
  industry,
  CASE
    WHEN amount < 50000 THEN 'SMB'
    WHEN amount < 250000 THEN 'Mid-Market'
    ELSE 'Enterprise'
  END AS deal_size_tier,
  CASE
    WHEN cycle_days < 30 THEN '< 30d'
    WHEN cycle_days < 90 THEN '30-90d'
    WHEN cycle_days < 180 THEN '90-180d'
    ELSE '> 180d'
  END AS cycle_band,
  primary_competitor,
  win_loss_status,
  loss_reason,
  COUNT(*) AS deal_count,
  SUM(amount) AS total_value
FROM fct_opportunities
WHERE close_date >= DATE '2026-07-01' AND close_date < DATE '2026-10-01'
  AND is_closed = TRUE
GROUP BY 1, 2, 3, 4, 5, 6
ORDER BY total_value DESC;
```

### Drift detection patterns

```python
# Compare current quarter rollup to prior 4 quarters
import pandas as pd

current_q = pd.read_csv('q3_2026_winloss.csv')
prior_4q = pd.read_csv('prior_4q_winloss.csv')

# Detect competitor mention rate drift
current_competitor_mentions = current_q.groupby('primary_competitor')['deal_count'].sum() / current_q['deal_count'].sum()
prior_competitor_mentions = prior_4q.groupby('primary_competitor')['deal_count'].sum() / prior_4q['deal_count'].sum()

drift = (current_competitor_mentions - prior_competitor_mentions).sort_values(ascending=False)
# Flag any competitor with > 10% mention-rate increase
emerging_threats = drift[drift > 0.10]
```

---

## Sales tech stack audit playbook

### Utilization scoring per tool

```python
# Run quarterly via cli-anything
tools = [
    {'name': 'Outreach', 'endpoint': '/outreach/api/v2/users', 'license_count': 50, 'annual_cost': 60000},
    {'name': 'Salesloft', 'endpoint': '/salesloft/v2/users', 'license_count': 30, 'annual_cost': 36000},
    {'name': 'Apollo', 'endpoint': '/apollo/api/v1/users', 'license_count': 50, 'annual_cost': 25000},
    {'name': 'ZoomInfo', 'endpoint': '/zoominfo/users', 'license_count': 25, 'annual_cost': 65000},
    {'name': 'Gong', 'endpoint': '/gong/v2/users', 'license_count': 75, 'annual_cost': 90000},
    # ... etc
]

for tool in tools:
    users = api_gateway_get(tool['endpoint'])
    active_30d = [u for u in users if u['last_login'] > now - timedelta(days=30)]
    tool['utilization'] = len(active_30d) / tool['license_count']
    tool['cost_per_active'] = tool['annual_cost'] / max(len(active_30d), 1)

# Flag low utilization
low_util = [t for t in tools if t['utilization'] < 0.30]
# Flag overlap
enrichment_overlap = [t for t in tools if t['name'] in ['Apollo', 'ZoomInfo', 'Cognism', 'Clay'] and t['utilization'] < 0.50]
```

### Kill / keep / renegotiate recommendation

| Utilization | Action |
|---|---|
| > 70% | Keep, renew at current seats |
| 50-70% | Keep, renegotiate seat count down 20-30% |
| 30-50% | Critical look — kill or consolidate with overlapping tool |
| < 30% | Kill at renewal unless strategic exception |

---

## Ramp-to-quota analysis playbook

### Cohort table

```python
# Run via cli-anything
import pandas as pd

reps = pd.read_csv('reps_with_start_date.csv')
deals = pd.read_csv('closed_won_deals.csv')

# Compute days from start date to first closed-won
reps['first_close_date'] = deals.groupby('owner_id')['close_date'].min()
reps['days_to_first_close'] = (reps['first_close_date'] - reps['start_date']).dt.days

# Cohort by hire month
reps['hire_cohort'] = reps['start_date'].dt.to_period('M')
cohort_summary = reps.groupby('hire_cohort').agg({
    'days_to_first_close': ['median', 'mean'],
    'rep_id': 'count'
})

# Per-rep monthly attainment from start
attainment = []
for _, rep in reps.iterrows():
    for month_offset in range(1, 13):
        month_start = rep['start_date'] + pd.DateOffset(months=month_offset - 1)
        month_end = rep['start_date'] + pd.DateOffset(months=month_offset)
        month_deals = deals[(deals['owner_id'] == rep['id']) & (deals['close_date'] >= month_start) & (deals['close_date'] < month_end)]
        attainment.append({
            'rep_id': rep['id'],
            'month_offset': month_offset,
            'attainment_pct': month_deals['amount'].sum() / rep['monthly_quota']
        })

attainment_df = pd.DataFrame(attainment)
ramp_curve = attainment_df.groupby('month_offset')['attainment_pct'].median()
# Render curve as matplotlib chart → exported via Pillow → pasted to notion
```

---

## Sales enablement infrastructure playbook

### Highspot tag taxonomy

```
Stage:
  - Prospecting
  - Discovery
  - Evaluation
  - Proposal
  - Negotiation
  - Closed-Won
  - Renewal

Persona:
  - CEO
  - CFO
  - VP Sales
  - VP Marketing
  - VP Engineering
  - VP Customer Success
  - Director Ops
  - Manager
  - Individual Contributor

Industry:
  - SaaS
  - FinTech
  - HealthTech
  - Retail
  - Manufacturing
  - Government

Competitor:
  - CompetitorA
  - CompetitorB
  - DIY/In-house build

Format:
  - Battlecard
  - Case study
  - Demo recording
  - Email template
  - Slide deck
  - One-pager
  - ROI calculator
  - Whitepaper
```

### Orphan content quarantine

Content with 0 views in last 90 days + no tags → quarantine queue → review monthly → archive if still 0 views.

---

## SalesOps onboarding runbook (for new SalesOps hire)

```markdown
# Week 1 — Baseline
- [ ] Salesforce / HubSpot admin access (read-only first, write after week 2)
- [ ] Spiff / QuotaPath / CaptivateIQ admin
- [ ] Gong admin (call review access)
- [ ] Salesloft / Outreach admin
- [ ] Highspot / Showpad admin
- [ ] Clari / BoostUp admin (forecasting)
- [ ] LeanData / Chili Piper admin
- [ ] Notion `SalesOps Runbook` + Metric Glossary
- [ ] Slack channels: #sales-ops, #deal-desk, #commission-disputes, #sales-alerts

# Week 2 — Read-only audits
- [ ] Schema audit: which custom fields are unused?
- [ ] Stage criteria audit: which stages have validation rules? Which don't?
- [ ] Commission plan review: current plan logic + last 4Q dispute log
- [ ] Forecast accuracy review: last 4Q commit vs. actual per AE
- [ ] Tech stack utilization: last 30 days per tool
- [ ] Win/loss tag completeness: any closed deals missing tags?

# Week 3 — Small change deploys (sandbox first)
- [ ] One validation rule (stage criteria enforcement)
- [ ] One workflow (auto-fill required field on save)
- [ ] One Slack alert (stalled deal)

# Week 4 — Stakeholder rounds
- [ ] Sales leadership: forecast + attainment dashboard walkthrough
- [ ] AE pod: which CRM friction is biggest?
- [ ] SDR pod: which routing rule mis-fires most?
- [ ] Finance: commission accrual + GL handoff
```

---

## SOTA tool reference (June 2026)

This section is grep-only — the agent uses keyword-driven retrieval to surface the right skill pack for the user's task. Headings are intentionally search-friendly. Every entry links to a detailed `SKILL.md` in `skills/` that ships in this bundle and loads on demand.

**Full coverage map:** see `reference/SOTA_USE_CASES.md` for the per-use-case mapping and confidence rating.

### Salesforce (Sales Cloud + Revenue Cloud)

Primary CRM admin surface. Custom fields, validation rules, flows, formulas, page layouts, approval processes, Apex (light), CPQ. Use SFDX CLI for sandbox-to-production deploys.

- **Skill:** `skills/salesforce-admin-custom-fields-flows/SKILL.md`
- **Endpoint:** `https://gateway.maton.ai/salesforce/services/data/v60.0/...` via `api-gateway` + native `salesforce-api` skill
- **Tools:** SFDX CLI (`sf project deploy`, `sf data query`), Salesforce Inspector, Workbench
- **Key calls:** `SELECT Id, DeveloperName FROM CustomField` (Tooling API), `POST /sobjects/Opportunity`, `PATCH /sobjects/Opportunity/{id}`, `POST /tooling/sobjects/ValidationRule`
- **Source:** https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/

### HubSpot Operations Hub

HubSpot Pro/Enterprise add-on for data quality automations + custom-coded workflow actions + data sync. Operations Hub workflows have richer logic than Marketing Hub workflows.

- **Skill:** `skills/hubspot-ops-hub-workflows/SKILL.md`
- **Endpoint:** `https://gateway.maton.ai/hubspot/automation/v4/...` + `/crm/v3/data-sync/...`
- **Key calls:** `POST /automation/v4/flows`, `POST /crm/v3/objects/custom_objects/...`
- **Source:** https://developers.hubspot.com/docs/api/automation/workflows

### Salesloft + Outreach + Gong (admin)

Tech-stack admin: Salesloft cadence governance, Outreach sequence governance, Gong scorecard creation + smart trackers.

- **Skill:** `skills/salesloft-outreach-tech-stack-admin/SKILL.md`
- **Endpoints:** `https://gateway.maton.ai/{salesloft|outreach|gong}/...` via `api-gateway`
- **Key calls:** Salesloft `POST /v2/cadences`, `POST /v2/team_templates`, Outreach `POST /api/v2/sequences`, Gong `POST /v2/users`, `POST /v2/calls/scorecards`
- **Source:** https://developers.salesloft.com/api.html + https://developers.outreach.io/api/ + https://app.gong.io/settings/api/documentation

### Spiff + QuotaPath + CaptivateIQ (commission)

ICM platforms. Spiff (Salesforce-acquired, Salesforce-tier) for enterprise; QuotaPath for mid-market; CaptivateIQ for enterprise alternative.

- **Skill:** `skills/commission-spiff-quotapath-captivateiq/SKILL.md` + `skills/commission-dispute-audit-trail/SKILL.md`
- **Endpoints:** `https://gateway.maton.ai/{spiff|quotapath|captivateiq}/...`
- **Key calls:** Spiff `POST /v1/plans`, `POST /v1/commissions`, `POST /v1/disputes`. QuotaPath `POST /api/v1/plans`. CaptivateIQ `GET /v1/statements/{id}/audit_log`.
- **Source:** https://docs.salesforcespiff.com/ + https://docs.quotapath.com/ + https://help.captivateiq.com/

### Salesforce CPQ + Conga CPQ + DealHub CPQ

Quote-to-cash configuration. Salesforce CPQ (Steelbrick) — native Salesforce add-on. Conga (Apttus). DealHub native UI + deal-desk module.

- **Skill:** `skills/salesforce-cpq-conga-dealhub/SKILL.md`
- **Endpoints:** Salesforce CPQ via `salesforce-api` SOQL on `SBQQ__*` objects. Conga + DealHub via `api-gateway`.
- **Key calls:** `POST /sobjects/SBQQ__Quote__c`, `POST /sobjects/SBQQ__PriceRule__c`, Conga `POST /quotes`, DealHub `POST /quotes`
- **Source:** https://developer.salesforce.com/docs/atlas.en-us.cpq_dev_api.meta/cpq_dev_api/ + https://docs.conga.com/ + https://docs.dealhub.io/

### LeanData + Chili Piper + Distribute (lead routing)

LeanData is Salesforce-native (match + route + book). Chili Piper is the inbound calendar router. Distribute is HubSpot-focused.

- **Skill:** `skills/lead-routing-leandata-chili-piper/SKILL.md`
- **Endpoints:** LeanData via `salesforce-api` (Salesforce-native config). Chili Piper via `api-gateway` `https://gateway.maton.ai/chilipiper/api/v1/...`. Distribute via `api-gateway`.
- **Source:** https://docs.leandata.com/ + https://docs.chilipiper.com/api/ + https://www.distribute.so/

### LeanData Dedup + Cloudingo + DupeBlocker

Duplicate management. LeanData Dedup (Salesforce-native). Cloudingo (Salesforce-native, mature fuzzy match). DupeBlocker (Validity). HubSpot has built-in deduper.

- **Skill:** `skills/duplicate-mgmt-leandata-dedupe/SKILL.md`
- **Mechanism:** Cloudingo via `api-gateway` proxy. LeanData Dedup runs in-platform; agent monitors + tunes rules. Custom Python fuzzy match via `cli-anything` (rapidfuzz) as fallback. Reports to `notion` weekly.
- **Source:** https://docs.leandata.com/dedup + https://cloudingo.com/ + https://www.validity.com/products/dupeblocker/

### ZoomInfo + Apollo + Clay + Demandbase (enrichment)

Waterfall enrichment. Apollo (cost-efficient B2B baseline), ZoomInfo (gaps + Scoops intent), Clay (workflow orchestration across 100+ sources), Demandbase (ABM intent overlay).

- **Skill:** `skills/data-enrichment-zoominfo-apollo-clay/SKILL.md`
- **Endpoints:** `https://gateway.maton.ai/{apollo|zoominfo|clay|demandbase}/...`
- **Key calls:** Apollo `POST /api/v1/people/match`, ZoomInfo `POST /persons/enrich`, Clay workflow trigger
- **Source:** https://docs.apollo.io/reference/people-search + https://api-docs.zoominfo.com/ + https://clay.com/docs/api

### Clari + BoostUp + Aviso (forecasting)

AI-driven forecasting platforms. Clari Align is enterprise standard; BoostUp is mid-market; Aviso is AI-driven alt. Manual fallback via CRM + Sheets always available.

- **Skill:** `skills/forecasting-clari-boostup-aviso/SKILL.md`
- **Endpoints:** `https://gateway.maton.ai/{clari|boostup|aviso}/...` (limited public APIs)
- **Mechanism:** CRM-side three-bucket forecast via `salesforce-api` + Python; Clari/BoostUp/Aviso integration when onboarded
- **Source:** https://www.clari.com/blog/sales-forecasting-methods/ + https://boostup.ai/ + https://aviso.com/

### Salesforce CRMA / Tableau CRM / Einstein Analytics

Native Salesforce dashboards. Build datasets from Salesforce + external sources (Snowflake, BigQuery, dbt). Embed in Lightning home pages. Predictive Einstein Discovery for AI-driven insights.

- **Skill:** `skills/rep-performance-dashboards/SKILL.md`
- **Endpoints:** `https://gateway.maton.ai/salesforce/services/data/v60.0/wave/...`
- **Tools:** `sf wave dataset deploy`, `sf wave dashboard create` via SFDX CLI
- **Source:** https://developer.salesforce.com/docs/atlas.en-us.bi_dev_guide_rest.meta/bi_dev_guide_rest/

### Looker + Sigma + Hex (warehouse dashboards)

Modern data-stack dashboards on warehouse data. Looker for enterprise, Sigma for spreadsheet-native, Hex for notebook + dashboard hybrid.

- **Skill:** `skills/rep-performance-dashboards/SKILL.md` (shared)
- **Endpoints:** Looker SDK via `api-gateway`. Sigma + Hex via `api-gateway`.
- **Source:** https://docs.looker.com/reference/api-and-integration + https://help.sigmacomputing.com/ + https://learn.hex.tech/

### Highspot + Showpad + Seismic (enablement)

Centralized content library + tracking + sales-play playbooks. Highspot leads market share; Showpad + Seismic close behind. Tag-driven content surfacing per deal stage.

- **Skill:** `skills/sales-enablement-infrastructure-highspot-showpad/SKILL.md`
- **Endpoints:** `https://gateway.maton.ai/{highspot|showpad|seismic}/...`
- **Source:** https://developers.highspot.com/ + https://developer.showpad.com/ + https://developer.seismic.com/

### Anaplan + Fullcast + Salesforce TM2 (territory)

Territory + quota planning. Anaplan for enterprise scenario modeling; Fullcast for mid-market; Salesforce TM2 for native enforcement.

- **Skill:** `skills/territory-planning-assignment/SKILL.md`
- **Endpoints:** Anaplan REST via `api-gateway`. Salesforce TM2 via `salesforce-api` on `Territory2` object.
- **Source:** https://help.salesforce.com/s/articleView?id=sf.tm2_intro.htm + https://www.anaplan.com/products/sales-planning/

### D&B Direct+ (account hierarchy)

Dun & Bradstreet Direct+ for account hierarchy refresh (M&A, divestitures, subsidiary mapping). Provides DUNS ID + parent-child structure.

- **Skill:** `skills/contact-account-hierarchy-maintenance/SKILL.md`
- **Endpoints:** `https://gateway.maton.ai/dnb/...` or direct curl via `cli-anything`
- **Source:** https://www.dnb.com/business-credit/dun-and-bradstreet-direct.html

### Salesforce Approval Process + HubSpot Approvals + DealHub deal desk

Discount tier approval routing. Salesforce native approval process is most flexible; HubSpot Approvals for HubSpot-shop; DealHub for CPQ-integrated.

- **Skill:** `skills/deal-desk-discount-approval/SKILL.md`
- **Endpoints:** Salesforce `POST /process/approvals` + custom approval rules via metadata. HubSpot Approvals via `api-gateway`. DealHub deal-desk module via `api-gateway`.
- **Source:** https://help.salesforce.com/s/articleView?id=sf.approvals_intro.htm + https://knowledge.hubspot.com/approvals

### Mindtickle + Lessonly (training)

Sales training + LMS-style ramp tracking. Mindtickle is enterprise standard. Used for ramp-to-quota analysis (training completion → ramp curve correlation).

- **Skill:** `skills/ramp-to-quota-analysis/SKILL.md`
- **Endpoints:** `https://gateway.maton.ai/{mindtickle|lessonly}/...`
- **Source:** https://www.mindtickle.com/

### dbt + Snowflake + BigQuery (warehouse + transformation)

Modern warehouse stack for pipeline metrics modeling. dbt for transformations; Snowflake / BigQuery for storage; Fivetran / Hightouch for sync. Used as the source of truth for rep performance dashboards in Salesforce CRMA / Looker / Sigma.

- **Skill:** `skills/pipeline-metrics-velocity-conversion/SKILL.md`
- **Tools:** `cli-anything` runs `dbt run`, `dbt test`. `postgresql-mcp` queries against the warehouse for ad-hoc analysis.
- **Models:** `fct_opportunities`, `fct_deal_activities`, `dim_users`, `dim_accounts`
- **Source:** https://docs.getdbt.com/

### Salesforce SFDX CLI

Universal Salesforce admin tool. Metadata deploys, data queries, wave dataset/dashboard deploys, Apex test runs.

- **Skill:** `skills/salesforce-admin-custom-fields-flows/SKILL.md`
- **Tools:** `cli-anything` runs `sf` (npm install -g @salesforce/cli or `npx sf-cli`)
- **Key commands:** `sf project deploy start`, `sf data query`, `sf data upsert bulk`, `sf wave dataset deploy`
- **Source:** https://developer.salesforce.com/tools/salesforcecli

### Cloudingo (Salesforce dedup)

Salesforce-native fuzzy dedup. Mature, configurable thresholds, audit trail. Paid.

- **Skill:** `skills/duplicate-mgmt-leandata-dedupe/SKILL.md` (shared)
- **Endpoints:** `https://gateway.maton.ai/cloudingo/api/v3/...`
- **Source:** https://cloudingo.com/

### Slack-mcp (alerts)

Slack notifications for stalled deals, dispute SLAs, approval escalations, attainment digests. Channel posts + threaded follow-ups.

- **Mechanism:** `slack-mcp` `chat.postMessage` + `chat.update` for threaded SLA escalations
- **Source:** https://api.slack.com/methods/chat.postMessage

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| Deploy a Salesforce custom field | `salesforce-admin-custom-fields-flows` | Sandbox first; SFDX `sf project deploy start` |
| Build a Salesforce validation rule | `salesforce-admin-custom-fields-flows` | Stage criteria enforcement pattern |
| Build a Salesforce Lightning Flow | `salesforce-admin-custom-fields-flows` | Record-triggered / Scheduled / Screen flow |
| Build a HubSpot workflow | `hubspot-ops-hub-workflows` | Workflow API + custom-coded actions |
| HubSpot data sync mapping | `hubspot-ops-hub-workflows` | Data sync API + conflict resolution |
| Configure Salesloft / Outreach / Gong admin | `salesloft-outreach-tech-stack-admin` | Admin REST APIs via `api-gateway` |
| Model a commission plan | `commission-spiff-quotapath-captivateiq` | Plan YAML template + pre/post comp delta |
| Resolve a commission dispute | `commission-dispute-audit-trail` | 5-day SLA; PDF audit-trail chain |
| Deploy CPQ pricing rule | `salesforce-cpq-conga-dealhub` | Sandbox + edge-case test quote |
| Set up lead routing | `lead-routing-leandata-chili-piper` | 10 synthetic leads test before deploy |
| Dedup audit | `duplicate-mgmt-leandata-dedupe` | High-confidence auto-merge; human-review queue |
| Set up enrichment waterfall | `data-enrichment-zoominfo-apollo-clay` | Apollo → ZoomInfo → Clay → Demandbase source order |
| Build pipeline velocity dashboard | `pipeline-metrics-velocity-conversion` | Sales Velocity formula + stage conversion |
| Define pipeline stage criteria | `pipeline-metrics-velocity-conversion` | Entry + exit criteria + validation rule |
| Run territory planning | `territory-planning-assignment` | TM2 + k-means + balance check |
| Build a forecast | `forecasting-clari-boostup-aviso` | Three-bucket + commit accuracy per AE |
| Investigate forecast accuracy | `forecasting-clari-boostup-aviso` | Slip / pull-in pattern detection |
| Build a rep performance dashboard | `rep-performance-dashboards` | CRMA / Looker / Sigma / Hex |
| Set up stalled-deal alerts | `stalled-deal-alerts-engagement-signals` | 1.5× median + 14d inactivity threshold |
| Set up deal desk approvals | `deal-desk-discount-approval` | Tier 1-4 matrix + SLA tracking |
| Analyze ramp-to-quota | `ramp-to-quota-analysis` | Cohort by hire month + ramp curve |
| Refresh account hierarchy | `contact-account-hierarchy-maintenance` | D&B Direct+ + Salesforce Account Hierarchy |
| Win/loss rollup | `win-loss-reporting-at-scale` | Quarterly + drift detection |
| Tech stack audit | `sales-tech-stack-consolidation-audit` | Utilization scoring + renegotiation |
| Set up Highspot / Showpad | `sales-enablement-infrastructure-highspot-showpad` | Tag taxonomy + orphan quarantine |
| Schema audit (unused fields) | `salesforce-admin-custom-fields-flows` | Tooling API + report-usage scan |
| Convert lead to opp validation | `salesforce-admin-custom-fields-flows` + `hubspot-ops-hub-workflows` | Required-field enforcement |
| Salesforce CRMA dashboard deploy | `rep-performance-dashboards` | `sf wave dataset deploy` |

---

## Closing rules

Pipeline-stage definitions are the foundation; everything downstream breaks without them. Commission disputes are SLA-bound and audit-trail-backed. The CRM is the source of truth. Sandbox before production. Three-bucket forecast or none. When depth is required (direct selling, predictive analytics, commission accounting, lead-source quality), call in a specialist.
