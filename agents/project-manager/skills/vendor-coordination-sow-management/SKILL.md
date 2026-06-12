<!--
Source: https://monday.com/blog/project-management/vendor-management/
Source: https://ironcladapp.com/journal/contracts/what-is-an-sow
-->
# Vendor Coordination + SOW Management — SKILL

Vendor scorecards (delivery / quality / cost / comms / compliance) + SOW lifecycle (draft → reviewed → signed → in-progress → accepted → closed) + milestone-based payment tracking + vendor RAID. Notion + Ironclad/PandaDoc + Harvest stack for SMB; Fieldglass/Beeline/Vndly for enterprise VMS.

## When to use

- Onboarding a new vendor (legal + procurement + PM coordination).
- Authoring or reviewing a Statement of Work (SOW).
- Tracking vendor delivery against SOW milestones.
- Quarterly vendor scorecard reviews.
- Closing a vendor engagement at project end.

Trigger phrases: "vendor SOW", "vendor onboarding", "vendor scorecard", "contractor", "external resource", "milestone payment", "vendor performance", "SOW lifecycle".

## Setup

```bash
# Ironclad API
curl -fsSL "https://api.ironcladapp.com/v1/contracts" \
  -H "Authorization: Bearer $IRONCLAD_TOKEN"

# PandaDoc API
curl -fsSL "https://api.pandadoc.com/public/v1/documents" \
  -H "Authorization: API-Key $PANDADOC_KEY"

# Harvest for vendor invoice tracking (cross-link budget skill)
# Notion DB for vendor + SOW
```

Auth:
- `IRONCLAD_TOKEN` — paid contract platform
- `PANDADOC_KEY` — paid (free trial)
- DocuSign API as alternative
- SMB free fallback: Notion DB + email + PDF attachments

## Common recipes

### Recipe 1: Vendor DB schema (Notion)
```yaml
Database: "Vendors"
Properties:
  Vendor_name:           title
  Type:                  select        # SaaS / Contractor / Consultancy / Agency / Supplier
  Engagement_status:     select        # Onboarding / Active / Paused / Closed
  Primary_contact:       rich_text
  Account_owner:         person
  Onboarded_date:        date
  MSA_signed:            checkbox
  Open_SOWs:             relation      # → SOW DB
  Quality_score:         number        # 1-5 rolling avg
  Delivery_score:        number
  Cost_efficiency:       number
  Comms_score:           number
  Compliance_score:      number
  Overall_score:         formula       # avg of 5
  Strategic_value:       select        # Critical / Important / Tactical / Replaceable
  Total_spend_ytd:       number
  Last_scorecard:        date
  Risk_flags:            multi_select  # SLA-miss / Data-breach / Late-invoice / Compliance / Other
  Renewal_date:          date
```

### Recipe 2: SOW DB schema
```yaml
Database: "SOWs"
Properties:
  SOW_id:                title           # SOW-2026-001
  Vendor:                relation        # → Vendor DB
  Project:               relation        # → Project DB
  Title:                 rich_text
  Status:                select          # Draft / Under review / Out for signature / Signed / In progress / Accepted / Closed
  Total_value:           number
  Currency:              select          # USD / EUR / GBP ...
  Start_date:            date
  End_date:              date
  Milestones:            relation        # → Milestone DB
  Payment_terms:         select          # Net 15 / Net 30 / Net 45 / Milestone / Hourly
  PM_owner:              person
  Legal_reviewer:        person
  Procurement_approver:  person
  Sponsor_approver:      person
  Signed_date:           date
  Acceptance_criteria:   rich_text
  Linked_RAID:           relation
  Linked_invoices:       relation
  Notes:                 rich_text
```

### Recipe 3: SOW lifecycle stages
```
1. DRAFT
   - PM + vendor draft scope, milestones, deliverables, AC, $ value
   - PM internal review

2. UNDER REVIEW
   - Legal review (terms, IP, indemnity, data privacy)
   - Procurement review ($ approval, vendor compliance)
   - Sponsor review (budget approval)

3. OUT FOR SIGNATURE
   - Ironclad/PandaDoc/DocuSign workflow
   - Vendor signs first → org signs

4. SIGNED
   - SOW archived (PDF in vendor folder + Notion link)
   - Vendor onboarded to PM tools (Linear/Asana access if needed)
   - Kickoff scheduled

5. IN PROGRESS
   - Milestone tracking
   - Weekly check-ins
   - Invoice processing per terms
   - SLA monitoring

6. ACCEPTED
   - All milestones validated
   - Final acceptance signed
   - All invoices paid

7. CLOSED
   - Vendor scorecard completed
   - Lessons learned captured
   - Vendor archived (or renewal triggered)
```

### Recipe 4: SOW template (condensed)
```markdown
# SOW-[ID] — [Vendor] — [Project]

## 1. Parties + dates
Client / Vendor / Effective / Expires

## 2. Scope (reference MSA, specific work)

## 3. Deliverables + AC
| # | Deliverable | Format | AC | Due | Owner |

## 4. Milestones + payment schedule
| Milestone | $ | Trigger |
| M1 signed | 25% | on execution |
| M2 storyboard approved | 25% | PM written approval |
| M3 v2 accepted | 25% | UAT pass + PM signoff |
| M4 final | 25% | all deliverables accepted |

## 5. Timeline (start, milestone dates, end)

## 6. Acceptance procedure (5-day SLA, 2 revisions, extra hrly)

## 7. Resources + access (tools, password mgr, MFA, NDA)

## 8. IP (work-for-hire, NDA date, data class)

## 9. Termination (14d notice, prorated fee)

## 10. Signatures (Client PM, Sponsor, Legal, Vendor)
```

### Recipe 5: Vendor scorecard (per quarter, 5 dims × 1-5)
```markdown
# Vendor Scorecard — [Vendor] — Q[N] [YYYY]

Overall: X/5 (rolling avg of dims)

Delivery       (on-time + AC quality)         | 4 | 3/4 milestones; 1 needed 3rd rev
Cost efficiency (vs budget + scope changes)   | 5 | 100% on budget; 0 unauthorized adds
Quality        (defects + AC pass rate)        | 4 | 75% first-review pass; 0 critical defects
Communication  (responsiveness, clarity)       | 5 | 4hr avg response; weekly check-ins held
Compliance     (security, privacy, contract)   | 5 | 0 incidents; 100% MFA/NDA

Risks this quarter: [list or "none"]
Recommendation: [ ] Renew  [ ] Continue  [ ] Improvement plan  [ ] Replace next renewal
→ feeds Vendor DB (Recipe 1)
```

### Recipe 6: Milestone payment tracking
```bash
# Notion DB query — milestones due for payment
mcp tool notion.query_database \
  --database_id "<sow-milestones-db>" \
  --filter '{"and":[
    {"property":"Status","select":{"equals":"Achieved"}},
    {"property":"Payment_status","select":{"equals":"Pending"}}
  ]}' \
| jq '.results[] | {
    milestone: .properties.Name.title[0].plain_text,
    amount: .properties.Amount.number,
    vendor: .properties.Vendor.relation[0].id,
    achieved_date: .properties.Achieved_date.date.start
  }'

# Generate Harvest invoice
curl -X POST "https://api.harvestapp.com/v2/invoices" \
  -H "Authorization: Bearer $HARVEST_TOKEN" \
  -H "Harvest-Account-Id: $HARVEST_ACCOUNT_ID" \
  -H "User-Agent: PM-Agent (you@email.com)" \
  -d '{
    "client_id":12345,
    "subject":"Milestone M2 — Storyboard approved",
    "due_date":"2026-07-22",
    "line_items":[{"kind":"Service","description":"M2 milestone payment","quantity":1,"unit_price":5000}]
  }'
```

### Recipe 7: SOW via Ironclad
```bash
# Create contract record + send for review
curl -X POST "https://api.ironcladapp.com/v1/workflows" \
  -H "Authorization: Bearer $IRONCLAD_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "template":"sow_template_v3",
    "data":{
      "vendor_name":"Acme Video LLC",
      "client_name":"OurCompany Inc",
      "total_value":20000,
      "effective_date":"2026-06-25"
    },
    "reviewers":["legal@ourco.com","procurement@ourco.com","sponsor@ourco.com"]
  }'
```

### Recipe 8: SOW via PandaDoc
```bash
# Send SOW PDF for vendor + sponsor signature
curl -X POST "https://api.pandadoc.com/public/v1/documents" \
  -H "Authorization: API-Key $PANDADOC_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"SOW-2026-005 Acme Video",
    "template_uuid":"<template-uuid>",
    "recipients":[
      {"email":"vendor-signer@acme.com","first_name":"Jane","last_name":"V","role":"Vendor"},
      {"email":"sponsor@ourco.com","first_name":"Alice","last_name":"S","role":"Client"}
    ],
    "tokens":[
      {"name":"sow.value","value":"$20,000"},
      {"name":"sow.start","value":"2026-06-25"}
    ]
  }'
```

### Recipe 9: Vendor RAID
```
Vendor-specific risks tracked in main RAID with prefix V-:

V-001 | Vendor SOW delivery slip risk | P=3, I=4 → 12 (AMBER) | Mitigation: weekly milestone check-in
V-002 | Vendor IP compliance unclear | P=2, I=5 → 10 (AMBER) | Mitigation: legal review pre-signature
V-003 | Single point of failure (1 designer) | P=3, I=3 → 9 (AMBER) | Mitigation: SOW requires backup designer named
```

### Recipe 10: Vendor onboarding checklist (5 categories)
```
LEGAL       | MSA | NDA | DPA (if PII) | insurance cert
SECURITY    | sec questionnaire | MFA | password mgr | SSO | data class
PROCUREMENT | approved vendor | W-9/W-8BEN | tax withholding | payment terms
TOOL ACCESS | Notion guest | Slack guest | Figma | Linear/Asana | Drive folder
PM          | kickoff scheduled | weekly check-in | escalation path | scorecard initiated
```

### Recipe 11: Vendor closure checklist (4 categories)
```
DELIVERABLES   | all accepted (PM signoff) | final UAT | docs handoff
FINANCE        | all payments processed | final invoice | $0 outstanding | 1099 if US contractor
ACCESS REMOVAL | tools revoked | pwd mgr freed | data export | Slack guest removed
SCORECARD+ARCH | Q-end scorecard | lessons learned | SOW+invoices archived | RAID V-XXX closed | DB → Closed
```

### Recipe 12: Enterprise VMS comparison (Fieldglass / Beeline / Vndly)
```
SAP Fieldglass    — most-deployed; SAP-integrated; strong workforce management
Beeline           — strong analytics + spend visibility; cross-vendor
Vndly             — cloud-native; lightweight; SMB-friendly
Workday VNDLY     — Workday-integrated
Coupa Contingent  — procurement + contingent workforce combined

When to consider VMS:
- 50+ active contractors / vendors
- Multi-region spend management needed
- Procurement controls + invoice automation required
- Vendor diversity / DEI tracking
```

## Examples

### Example 1: Onboard new video production vendor
**Goal:** SOW signed by Friday; first milestone Mon.

**Steps:**
1. Recipe 4 SOW template populated.
2. Recipe 10 onboarding checklist initiated.
3. Recipe 7 or 8 send for signature.
4. Vendor + sponsor signed Thu.
5. Notion DB updated (Recipes 1, 2).
6. Kickoff scheduled Fri.
7. Recipe 6 milestone tracking started.

**Result:** Vendor producing Mon; payment terms automated.

### Example 2: Quarterly vendor scorecard
**Goal:** Review 8 vendors; identify renewal candidates.

**Steps:**
1. Per vendor, run Recipe 5 scorecard.
2. Update Vendor DB (Recipe 1).
3. Rank by Overall_score.
4. Bottom-2 (<3.5) → improvement plan or replace recommendation.
5. Top-2 + strategic-value=Critical → renew discussion.

**Result:** Renewal pipeline + improvement plans documented.

### Example 3: Close vendor engagement at project end
**Goal:** Project closure; vendor delivered all deliverables.

**Steps:**
1. Recipe 11 closure checklist.
2. Final scorecard (Recipe 5).
3. Vendor DB → engagement_status=Closed.
4. Lessons learned added to vendor profile (renewal context).

**Result:** Clean closure; renewal-ready profile for next project need.

## Edge cases / gotchas

- **MSA first, SOW second.** Don't sign SOW without underlying MSA; legal risk + IP confusion.
- **Acceptance criteria specific.** Vague AC → endless revisions → scope creep. "Reviewed by PM" is vague; "AC: <60s video, captions, 4K, audience comprehension ≥90% in pilot test" is specific.
- **Milestone payments tied to deliverables, not dates.** Date-based payments incentivize speed over quality.
- **Don't pay 100% upfront.** 25% on signature is fine; 100% upfront kills leverage.
- **Termination clause must exist.** No-termination contracts are unwise.
- **Single-vendor lock-in.** Critical-path vendor without backup = single point of failure (V-003).
- **Cross-border + tax.** US contractor → W-9 + 1099. Foreign → W-8BEN + treaty rates. Get help from finance.
- **Vendor RAID separate from vendor DB.** Don't conflate engagement risk (V-XXX) with vendor scorecard (per-quarter).
- **NDA before kickoff.** Don't share confidential before NDA signed.
- **Data processing agreement (DPA).** Required if vendor processes PII (GDPR, CCPA).
- **Vendor scorecard drift.** Without quarterly cadence, scorecards stale → no signal at renewal.
- **Hidden vendor spend.** Team-bought tools (Figma seats, GitHub) often not in vendor management; surface for portfolio visibility.
- **SOW vs PO.** PO = order; SOW = scope + terms. Don't conflate. SOW first, PO references SOW.
- **Sponsor approval required ≥ org threshold.** Often $25k+. Forgetting = compliance miss.
- **Ironclad vs PandaDoc vs DocuSign.** Ironclad for full lifecycle (review + storage + redlines); PandaDoc for SMB sales-style flow; DocuSign for signature-only.
- **Vendor scope creep.** Vendors propose "small adds"; treat as CR (cross-link change-request-management).
- **Out-of-pocket expenses.** SOW must specify whether T&E is included or pass-through; common dispute source.
- **Anti-SOW: "best efforts" language.** "Vendor will use best efforts" = no commitment. Force "Vendor will deliver X by Y."
- **Vendor's subcontractors.** Approval rights? Liability? Include clause.

## Sources

- [Monday.com vendor management guide](https://monday.com/blog/project-management/vendor-management/)
- [Ironclad SOW guide](https://ironcladapp.com/journal/contracts/what-is-an-sow)
- [PandaDoc API](https://developers.pandadoc.com)
- [DocuSign API](https://developers.docusign.com)
- [SAP Fieldglass](https://www.fieldglass.com)
- [Beeline VMS](https://www.beeline.com)
- [Workday VNDLY](https://www.workday.com/en-us/products/vndly.html)
- [Atlassian vendor management templates](https://www.atlassian.com/templates/vendor-management)
- [PMI vendor management](https://www.pmi.org/learning/library/project-procurement-vendor-management-8086)
- [PMBOK 7th Edition: procurement performance domain](https://www.pmi.org/standards/pmbok)
