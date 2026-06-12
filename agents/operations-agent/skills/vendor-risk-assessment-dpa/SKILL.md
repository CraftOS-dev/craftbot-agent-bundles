<!--
Sources: https://secureframe.com/blog/soc-2-vs-security-questionnaires
         https://soc2auditors.org/insights/vendor-security-questionnaire-guide/
         https://copla.com/blog/third-party-risk-management/guide-to-vendor-security-and-risk-assessment-questionnaires/
2026 benchmark: 73% companies use SOC 2 reports; 70% use security questionnaires.
DPA checklist: purpose / confidentiality / sub-processors / breach notice / audit / retention.
-->
# Vendor Risk Assessment + DPA — SKILL

Assess third-party vendor risk: SOC 2 / ISO 27001 / penetration test review, security questionnaire (SIG / CAIQ / custom), Data Processing Agreement (DPA) drafting, sub-processor tracking, data-retention + deletion policies, breach-notification clauses. Aligns with SOC 2 CC3 + CC6 + CC7 third-party risk + GDPR Article 28.

## When to use

- Onboarding a new vendor that touches customer data / PII.
- Annual vendor re-assessment.
- Customer asks "how do you manage third-party risk?"
- SOC 2 audit prep.
- Trigger phrases: "DPA", "vendor risk", "security questionnaire", "SOC 2 review", "ISO 27001", "sub-processor", "data processing addendum", "GDPR Art. 28".

## Setup

```bash
# Trust centers
export VANTA_TOKEN="xxx"           # Vanta Trust Center
export DRATA_TOKEN="xxx"           # Drata Trust Center
export SECUREFRAME_TOKEN="xxx"     # Secureframe Trust Center
export WHISTIC_TOKEN="xxx"         # Whistic profile / share

# DPA + e-sign
export DOCUSIGN_TOKEN="xxx"
export GMAIL_TOKEN="xxx"           # gmail-mcp for security@ outreach
export NOTION_TOKEN="xxx"          # questionnaire DB + vendor registry
```

## Common recipes

### Recipe 1: Vendor tiering (data-classification driven)
```yaml
tier_definitions:
  T0_critical:
    criteria: "Processes regulated data (PHI, PCI, financial), or core infra (cloud, identity, CDN)"
    artifacts_required:
      - SOC 2 Type II annual
      - DPA + SCCs current
      - Cyber insurance ≥ $5M
      - Pen test annual summary
      - Sub-processor list
    review_cadence: annual
  T1_high:
    criteria: "Processes customer PII / employee PII"
    artifacts_required:
      - SOC 2 Type II OR ISO 27001
      - DPA + SCCs
      - Sub-processor list
    review_cadence: annual
  T2_medium:
    criteria: "Processes internal data, no PII"
    artifacts_required:
      - Security questionnaire (SIG Lite or 20-question custom)
    review_cadence: biannual
  T3_low:
    criteria: "No data processing (e.g., billing-only utility)"
    artifacts_required:
      - Vendor name + contact + invoice
    review_cadence: at renewal
```

### Recipe 2: Security questionnaire (custom 25-question short form)
```yaml
questionnaire:
  org_security:
    - "Do you have a written infosec policy reviewed annually?"
    - "Do you have an information security officer / CISO?"
  certifications:
    - "Do you have SOC 2 Type II? Attach latest report."
    - "Do you have ISO 27001? Attach cert + Statement of Applicability."
    - "Do you have other relevant attestations (HIPAA, PCI, FedRAMP)?"
  access_controls:
    - "Is MFA enforced on all employee accounts?"
    - "How do you provision/deprovision access for offboarded employees? Within what SLA?"
    - "Do you use SSO? Which IdP?"
  data:
    - "How is customer data encrypted at rest? Algorithm + key mgmt?"
    - "How is data encrypted in transit? TLS version?"
    - "Where is data stored (regions)?"
    - "Sub-processors involved in handling customer data — list with country + role."
  vulnerability_mgmt:
    - "Frequency of vulnerability scans?"
    - "Patching SLA for critical CVEs?"
    - "Pen test cadence?"
  incident_response:
    - "Do you have a documented IR plan? Tested?"
    - "Breach notification SLA to customers?"
    - "Last material incident in past 24 months? Describe."
  business_continuity:
    - "RTO + RPO for our service tier?"
    - "Cross-region backup?"
    - "BCP tested in past 12 months?"
  hr_controls:
    - "Background checks on employees with data access?"
    - "Annual security training?"
  subcontractor_controls:
    - "Sub-processor flow-down DPA?"
```

### Recipe 3: Vendor security review — pull trust center artifacts
```bash
# Vanta Trust Center share — vendor's public/private trust profile
curl -s "https://api.vanta.com/v1/external/trust-center/<vendor-slug>" \
  -H "Authorization: Bearer $VANTA_TOKEN"

# Drata Trust Center
curl -s "https://api.drata.com/v1/trust-center/<vendor>" \
  -H "Authorization: Bearer $DRATA_TOKEN"
```

### Recipe 4: SOC 2 Type II review template
```markdown
# SOC 2 Type II Review — <Vendor>

## Audit basics
- Auditor: [firm + qualified opinion?]
- Type: II (operating effectiveness over time)
- Period: [start - end] — must cover ≥ 6 months
- Report date: [must be recent — within last 12 months]
- Trust Services Criteria: Security + [Availability / Confidentiality / Processing Integrity / Privacy]

## Bridge letter
- [ ] Bridge letter from last report-period-end through today (if > 90 days old)

## Exceptions (Section 4)
- List + my-assessment for each:
  - Exception: [...]
  - Vendor remediation: [...]
  - My assessment: [Material / Acceptable] + reasoning

## CUEC (Complementary User Entity Controls)
- Controls WE must operate for vendor's controls to be effective. List + map to our control set.

## Decisions
- [ ] Accept
- [ ] Accept with mitigation: [...]
- [ ] Reject — require remediation
```

### Recipe 5: DPA checklist (binding draft)
```yaml
dpa_required_clauses:
  scope_and_purpose:
    - "Vendor processes data ONLY for documented purposes in MSA + SOW"
    - "Vendor will not use data for own purposes (training AI models, marketing, etc.)"
  confidentiality:
    - "Vendor employees/contractors subject to binding confidentiality"
  technical_organizational:
    - "Reference: Schedule A — Annex II SCCs"
    - "Specific list: encryption, access control, IR, vulnerability mgmt, backup"
  sub_processors:
    - "Authorized list — Schedule B"
    - "30-day prior notice of change"
    - "Customer right to object; if unresolved → termination"
  data_subjects_rights:
    - "Vendor assists customer with DSAR within 5 business days"
  breach_notification:
    - "Vendor notifies customer within 24/48/72 hours of confirmed breach"
    - "Notice includes: scope, data affected, root cause, mitigation"
  audit:
    - "Customer right to audit annually (or rely on SOC 2/ISO 27001)"
  data_return_or_deletion:
    - "Within 30 days of termination, vendor returns or deletes per customer instruction"
    - "Certification of deletion provided in writing"
  international_transfers:
    - "EU SCCs (2021 modules) for EU→non-EU transfers"
    - "UK IDTA addendum for UK transfers"
    - "Adequacy decisions referenced where applicable (Japan, UK, EU-US DPF)"
  retention_after_termination:
    - "Vendor MAY retain only what's legally required, in encrypted backup, for max [X] days"
```

### Recipe 6: Sub-processor tracking (Notion DB)
```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_TOKEN" -H "Notion-Version: 2022-06-28" -H "Content-Type: application/json" \
  -d '{
    "parent":{"database_id":"<subprocessor-db>"},
    "properties":{
      "Name":{"title":[{"text":{"content":"AWS"}}]},
      "Used By Vendor":{"select":{"name":"<vendor>"}},
      "Purpose":{"rich_text":[{"text":{"content":"Hosting"}}]},
      "Country":{"select":{"name":"US"}},
      "Data Types":{"multi_select":[{"name":"PII"},{"name":"Telemetry"}]},
      "DPA URL":{"url":"..."},
      "SOC 2 URL":{"url":"..."}
    }
  }'
```

### Recipe 7: Data retention + deletion policy template
```markdown
# Data Retention + Deletion Policy — [Co]

## Purpose
Define retention periods for each data class; ensure deletion on retention end; honor DSAR + erasure rights.

## Data classes + retention
| Data class             | Examples                       | Retention | Justification |
|------------------------|--------------------------------|-----------|---------------|
| Customer account data  | name, email, billing           | Until termination + 30 days | Active service |
| Customer content       | uploads, projects              | Until termination + 30 days | Active service |
| Audit logs             | system + API access logs       | 7 years   | SOX, SOC 2 |
| Financial records      | invoices, payments             | 7 years   | IRS / state |
| Support tickets        | conversations                  | 2 years   | Quality, training |
| Marketing leads        | inbound forms                  | 2 years   | Lawful basis (consent) |
| Employee PII           | HR, payroll                    | 7 years post-termination | EEOC / IRS |
| Background checks      | Checkr reports                 | per Fair Credit Reporting Act |
| Cookies — analytics    | GA, Mixpanel                   | 14 months | GDPR cookie consent |

## Deletion workflows
- Manual DSAR: Linear ticket → assigned to engineer; SLA 30 days; verify deletion across systems.
- Automated retention end: cron job per data class.
- Vendor sub-processor deletion: Recipe 5 DPA clause forces.

## Erasure rights
- GDPR Art. 17 / CCPA delete request → end-to-end deletion within 30 days.
- Exceptions: legal hold, regulatory retention, fraud detection.

## Compliance
- DSAR tracking: Notion DB.
- Annual audit: sample 10 deletions for validation.

> Defer to `legal-counsel` for binding retention-period determinations and legal-hold management.
```

### Recipe 8: Annual vendor re-assessment cycle
```python
# Annual cycle: pull vendor registry; for each Tier 0/1, request fresh SOC 2 + sub-processor list
import requests, datetime, os
vendors = requests.post('https://api.notion.com/v1/databases/<vendor-registry>/query',
    headers={'Authorization': f"Bearer {os.environ['NOTION_TOKEN']}",'Notion-Version':'2022-06-28','Content-Type':'application/json'},
    json={'filter':{'and':[
        {'property':'Tier','select':{'does_not_equal':'T3_low'}},
        {'property':'Last Reviewed','date':{'before': (datetime.date.today() - datetime.timedelta(days=365)).isoformat()}}
    ]}}).json()
for v in vendors['results']:
    name = v['properties']['Name']['title'][0]['plain_text']
    # email security@vendor for fresh SOC 2 + sub-processor list
    # via gmail-mcp
```

### Recipe 9: Customer-facing DPA portal
```markdown
# Customer DPA self-serve
- Public link: https://<co>.com/legal/dpa
- Auto-fill: company name + signer fields
- DocuSign template — Recipe 5 clauses pre-loaded
- Storage: Google Drive `Legal/DPA/Signed/<year>/<customer>.pdf`
```

### Recipe 10: GDPR-related vendor outreach email
```markdown
Subject: 2026 DPA + Sub-processor refresh — [Co]

Hi <vendor security/legal>,

For our annual vendor risk assessment, please share:
1. Current SOC 2 Type II report (cover period must include past 6 months) or ISO 27001 cert + SoA.
2. Current sub-processor list with country + purpose.
3. Updated DPA signed by an authorized signer of <vendor>. Our template attached; we are flexible on yours if substantively equivalent.
4. Cyber insurance certificate showing ≥ $5M coverage.
5. Last completed pen test (executive summary acceptable).

Our SLA for collection: 30 days.

Thanks,
[Name], Security / Compliance @ [Co]
```

### Recipe 11: Acceptance criteria scoring
```python
SCORE_WEIGHTS = {
    'soc2_or_iso_current': 30,
    'mfa_enforced_all_emps': 10,
    'breach_notice_le_72h': 15,
    'cyber_insurance_ge_5m': 10,
    'sub_processor_30d_notice': 10,
    'data_residency_clear': 10,
    'deletion_certification': 5,
    'pen_test_le_12mo': 5,
    'last_breach_disclosure': 5,
}
def score(vendor):
    return sum(w for k, w in SCORE_WEIGHTS.items() if vendor.get(k))
# > 70 = accept; 50-70 = accept with conditions; < 50 = reject
```

## Examples

### Example 1: Onboard a new analytics vendor (Tier 1)
**Goal:** PII-touching vendor green-lit in 2 weeks.
**Steps:**
1. Recipe 1 tier: PII → Tier 1.
2. Recipe 10 email → vendor security@.
3. Recipe 4 SOC 2 review.
4. Recipe 5 DPA red-line (defer binding to legal-counsel).
5. Recipe 6 add sub-processors to DB.
6. Recipe 11 score → accept.

**Result:** Documented decision; SOC 2 + DPA on file; audit-ready.

### Example 2: Customer security questionnaire — answer ours
**Goal:** Customer asks us to fill SIG Lite.
**Steps:**
1. Pull pre-built canonical answer library (Notion DB).
2. Compose SIG Lite + attach SOC 2 Type II + DPA + sub-processor list.
3. DocuSign for any binding sections.
4. Customer-facing portal: Vanta / Drata trust center link.

**Result:** Same-day turn; consistent answers across customers.

## Edge cases / gotchas

- **Bridge letter required.** SOC 2 reports older than 90 days from the report date require a bridge letter from the vendor's auditor attesting controls are still operating. Without it, audit value drops.
- **CUECs (Complementary User Entity Controls).** Vendor's controls only work if YOU operate counterpart controls. Read Section 4 and map.
- **AI-vendor "we don't train on your data" — verify.** Vendor's marketing ≠ contract. Recipe 5 `scope_and_purpose` must explicitly carve out training/secondary use.
- **Sub-processor change without notice.** If discovered, immediate written notice + reserve termination right per Recipe 5.
- **Schrems II + EU-US DPF.** Post-Schrems II + the 2023 EU-US Data Privacy Framework. SCCs still required for non-DPF-certified vendors. **Defer to `legal-counsel`.**
- **Breach-notice SLAs differ.** GDPR Art. 33 = 72 hours to supervisory authority; vendor → you should be ≤ 24-48h. SEC public cos 4 business days.
- **Retention vs deletion.** Backups containing personal data must be deletable on DSAR (or destroyed at backup expiry). Most vendors retain in tape/cold storage 30-90d.
- **DPA "out of scope" loopholes.** Some vendor DPAs exclude metadata, logs, support transcripts. Confirm scope = ALL personal data they process.
- **Customer auditing right.** Most vendors won't let customers physically audit; will accept SOC 2 instead. Recipe 5 audit clause should permit either.
- **Defer to `legal-counsel` for binding DPA red-line, SCC module selection (Module 1-4), cross-border transfer assessment, and breach-notification customer-facing draft.**

## Sources

- Secureframe — SOC 2 vs Security Questionnaires: https://secureframe.com/blog/soc-2-vs-security-questionnaires
- SOC 2 Auditors — Vendor Questionnaire Guide: https://soc2auditors.org/insights/vendor-security-questionnaire-guide/
- Copla — Vendor Risk Assessment Guide: https://copla.com/blog/third-party-risk-management/guide-to-vendor-security-and-risk-assessment-questionnaires/
- GDPR Art. 28 (Processor): https://gdpr-info.eu/art-28-gdpr/
- GDPR Art. 33 (Breach Notification): https://gdpr-info.eu/art-33-gdpr/
- EU SCCs (2021): https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/standard-contractual-clauses-scc_en
- EU-US DPF: https://www.dataprivacyframework.gov/
- SOC 2 (AICPA): https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2
