---
name: data-retention-deletion-policy
description: Retention schedule per data category × jurisdiction × purpose × legal hold. GDPR Art. 5(1)(e) storage limitation + CCPA + state law + sector retention (HIPAA 6yr; FINRA 17a-4 supervisory; SOX 5-7yr; PCI auth data 1yr). Automated deletion via OneTrust Retention / Securiti / DataGrail + Salesforce / HubSpot / Stripe purge APIs. Litigation hold workflow.
---

# Data Retention + Deletion Policy

Retention schedule + deletion runbook + litigation hold. Required by GDPR + CCPA + state laws + sector-specific (HIPAA, FINRA, SOX, PCI).

## When to use

User says:
- "Retention schedule" / "retention policy"
- "Data deletion" / "purge" / "RTBF"
- "Storage limitation" / "GDPR Art. 5(1)(e)"
- "Legal hold" / "litigation hold"
- "Records management"
- "HIPAA 6 year" / "FINRA 17a-4" / "SOX 7 year"
- "Deletion runbook"

Companion skills: `gdpr-article-30-ropa-dpia`, `ccpa-cpra-dsar-workflows`, `data-classification-dlp-purview-nightfall`.

## Setup

```bash
# Paid retention platforms
# https://www.onetrust.com/products/data-discovery-classification/
# https://securiti.ai/
# https://www.datagrail.io/
# https://www.mineos.ai/

export ONETRUST_API_KEY=<dashboard>
export SECURITI_API_KEY=<dashboard>
export DATAGRAIL_API_KEY=<dashboard>

# Free reference
# GDPR Art. 5
curl -fsSL https://gdpr-info.eu/art-5-gdpr/ > /tmp/gdpr_art5.html
# IRS records retention
curl -fsSL https://www.irs.gov/businesses/small-businesses-self-employed/how-long-should-i-keep-records > /tmp/irs.html
# FINRA 17a-4
curl -fsSL https://www.finra.org/rules-guidance/key-topics/books-records > /tmp/finra.html
```

## Common recipes

### Recipe 1: Retention principles

```text
GDPR Art. 5(1)(e): "kept in a form which permits identification of data
subjects for no longer than is necessary for the purposes for which the
personal data are processed".

CCPA / CPRA: business must disclose retention period or criteria for each
category collected.

Principles:
1. Define purpose for each data category.
2. Set retention based on purpose + legal obligation.
3. Document the schedule.
4. Automate deletion.
5. Handle legal hold exceptions.
6. Periodic audit (annual).
```

### Recipe 2: Retention schedule template (cross-jurisdiction)

```markdown
# Data Retention Schedule — <Co.>

**Effective:** <date>
**Owner:** <Privacy Lead>
**Annual review:** <date>

| Data category | Purpose | Lawful basis (GDPR) | Retention (active) | Retention (archive) | Trigger for deletion | Disposal method | Legal hold exception |
|---|---|---|---|---|---|---|---|
| Customer account profile | Service delivery | Contract (6(1)(b)) | Lifecycle of account | 7 years (financial reporting) | Account closure + 7yr | Soft delete + cryptoshred | Litigation hold per <SOP> |
| Customer support tickets | Support resolution | Contract / LIA | 3 years | — | Ticket close + 3yr | Hard delete | — |
| Marketing email subscribers | Marketing | Consent (6(1)(a)) | Until consent withdrawn | — | Withdrawal / inactive 24mo | Hard delete | — |
| Job applicants (unsuccessful) | Recruitment | LIA (6(1)(f)) | 6 months default; longer if applicant consents | — | 6mo from close | Hard delete | — |
| Employees (active) | Employment | Contract / legal obligation | Throughout employment | — | Per HR | — | — |
| Employees (post-termination) | Tax + employment law | Legal obligation (6(1)(c)) | 7 years (US tax); 6 years (HIPAA if applicable) | Permanent (pension) | 7 years from separation | Cryptoshred | Litigation hold |
| Financial transactions | Tax + AML | Legal obligation | 7 years US (5+2); 6 years UK | — | 7yr from transaction | Cryptoshred | AML investigation hold |
| PHI (HIPAA) | Care + legal | Legal obligation | 6 years from creation OR last effect | Per state (some 10+) | Per HIPAA | Cryptoshred + cert | Litigation hold |
| CHD authorization data (PCI) | Payment authorization | Contract | 1 year (Req 3.3.x) | — | After auth | Hard delete | Forensic exception |
| Audit logs | Compliance | Legal obligation / LIA | 1 year hot / 7 years cold | — | Per SOC 2 + PCI Req 10.5 | Cryptoshred | Litigation hold |
| Backups | Disaster recovery | LIA / contract | 90 days rolling | — | Rolling overwrite | Tape rotation / S3 lifecycle | — |
| Email archive | Compliance / discovery | Contract / legal | 7 years (US business) | — | Per email retention SOP | — | Litigation hold |
| Court / FOIA records (public) | Legal | Legal | Per legal counsel | — | — | — | — |
| AI training datasets | ML development | LIA + consent (varies) | Per consent + bias-audit window | — | Model retirement | Cryptoshred | EU AI Act post-market monitoring |

---
*This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.*
```

### Recipe 3: Sector-specific retention requirements

```text
HIPAA (45 CFR §164.316(b)(2)(i)):
- Policies + documentation: 6 years from creation OR last effective date
- Medical records: state law (typically 5-10 years adult; 21+ minor age)
- Accounting of disclosures: 6 years (Privacy Rule)

FINRA Rule 4511 + SEC 17a-4:
- Books + records: 6 years (first 2 in accessible)
- Communications: 3-7 years per rule (17a-4(b)(4))
- Customer agreements: 6 years post account close
- Order tickets: 3 years
- Email + IM: 3 years
- Marketing communications: 3 years
- 17a-4(f) electronic storage requirements (WORM / write-once + indexing
  + audit trail)

SOX (15 USC §7245):
- Audit work papers: 7 years
- Financial records: 5-7 years
- Internal controls evidence: 7 years
- Material communications: 7 years
- Sec. 802 — 5-year retention for accountants

PCI DSS v4.0:
- Authentication data (full track / CVV / PIN): MUST NOT be stored
  post-authorization
- Account data (PAN, expiry): defined retention + secure deletion
- Logs: 1 year minimum; 3 months immediately available
- Inventory: current

GLBA:
- 6 years post-relationship (Reg DD overlap)

CCPA:
- Service provider may not retain longer than necessary; must delete at
  business request

ERISA:
- Plan records: 6 years
- Participant records: indefinitely (some plans)

Tax (US):
- 3 years general (IRC §6501)
- 6 years for under-reported income >25%
- 7 years for losses claimed
- INDEFINITE for fraud

Tax (EU):
- 10 years typical (varies by Member State — DE 10yr; FR 10yr; ES 6+4yr)

OSHA:
- 5 years for occupational injury records
```

### Recipe 4: Automated deletion via SaaS APIs

```bash
# Stripe — delete customer (subject to retention rules)
curl -X DELETE 'https://api.stripe.com/v1/customers/<cus_xxx>' \
  -u "$STRIPE_API_KEY:"

# Salesforce — bulk delete via API
sf data delete record --sobject Contact --record-id <id>
# Or SOQL + bulk DELETE for criteria-based

# HubSpot — delete contact
curl -X DELETE 'https://api.hubapi.com/contacts/v1/contact/vid/<id>' \
  -H "Authorization: Bearer $HUBSPOT_TOKEN"

# Segment — request deletion
curl -X POST 'https://platform.segmentapis.com/v1beta/workspaces/<workspace>/regulations' \
  -H "Authorization: Bearer $SEGMENT_TOKEN" \
  -d '{"regulationType":"DELETE_ONLY","subjects":[{"type":"USER_ID","value":"<id>"}]}'

# Mailchimp — permanent delete
curl -X POST "https://<dc>.api.mailchimp.com/3.0/lists/<list_id>/members/<subscriber_hash>/actions/delete-permanent" \
  -u "anystring:$MAILCHIMP_API_KEY"

# Intercom — delete contact (RTBF)
curl -X POST 'https://api.intercom.io/contacts/<id>/erase' \
  -H "Authorization: Bearer $INTERCOM_TOKEN"

# AWS S3 — lifecycle expiration rule
aws s3api put-bucket-lifecycle-configuration --bucket <bucket> \
  --lifecycle-configuration '{"Rules":[{"ID":"expire-90d","Status":"Enabled","Filter":{"Prefix":"temp/"},"Expiration":{"Days":90}}]}'

# Snowflake — time travel + drop
ALTER TABLE customer_pii SET DATA_RETENTION_TIME_IN_DAYS = 0;
DELETE FROM customer_pii WHERE deleted_at < DATEADD(YEAR, -7, CURRENT_DATE());

# Postgres — cron job (pg_cron)
SELECT cron.schedule('purge-old-tickets', '0 2 * * *',
  $$ DELETE FROM tickets WHERE closed_at < NOW() - INTERVAL '3 years'; $$);
```

### Recipe 5: Cryptoshredding (key destruction)

```text
For data encrypted with a per-customer or per-record key:
- "Delete" by destroying the key → ciphertext becomes unrecoverable.
- Faster than overwriting all encrypted bytes.
- Use case: large data sets where physical deletion is slow.

Implementation:
- AWS KMS: schedule key deletion (7-30 day waiting period)
- GCP KMS: destroy key version
- Azure Key Vault: delete key (soft-delete + purge)
- HashiCorp Vault: delete key

Document the cryptoshred event as the deletion event (timestamp + key ID
+ scope).
```

### Recipe 6: Hard delete vs soft delete

```text
Soft delete:
- Mark as deleted (deleted_at timestamp); preserved in DB.
- Allows undo + audit.
- DOES NOT satisfy GDPR Art. 17 erasure (data still present).

Hard delete:
- Remove row entirely; vacuum / TRUNCATE.
- Satisfies erasure.
- May still exist in backups (next backup cycle expiry typical).

Strategy:
- Soft delete first (audit window 30-90 days).
- Hard delete at end of audit window.
- Backups deleted via natural rotation OR forced for high-risk.
```

### Recipe 7: Backup deletion handling

```text
Backups present a tension:
- Need backups for resilience.
- Need to honor deletion requests.

Industry standard (most regulators accept):
- Document backup retention cycle (e.g., 90 days rolling).
- Deleted data remains in backups until natural rotation expiry.
- DO NOT restore the deleted data even from backup.

Documentation:
- Backup retention SOP
- Deletion → suppression list (re-blocks recreation if restore attempts re-add)
```

### Recipe 8: Legal hold workflow

```markdown
# Legal Hold Procedure

## Trigger
- Pending or anticipated litigation
- Regulatory investigation
- Subpoena / discovery request

## Issuance
1. Legal Counsel issues hold memo identifying:
   - Custodians (named employees)
   - Data sources (email, drives, chat, dbs)
   - Date ranges
   - Subject matter
2. Notify custodians + IT.

## Implementation
1. Suspend automatic deletion for in-scope data.
2. Apply system-side legal hold (M365 Compliance, Workspace Vault,
   Salesforce, Slack).
3. Document the hold scope + retention extension.

## Maintenance
1. Periodic reminder to custodians (quarterly).
2. New employee onboarding: confirm relevance to ongoing holds.

## Release
1. Counsel issues release memo.
2. Resume normal retention.
3. Schedule deletion of held data not otherwise retained.

---
*This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.*
```

### Recipe 9: Microsoft Purview retention labels

```text
Purview > Solutions > Records management > Retention labels

Create retention label:
- Label name: "Confidential — 7yr"
- Retention period: 7 years
- Retention trigger: when content was created OR labeled OR last modified
- At end of retention: Delete / Trigger disposition review

Apply to:
- Specific SharePoint sites
- OneDrive
- M365 Groups + Teams
- Exchange
- Auto-apply via auto-labeling rule (sensitive info type or KQL)

Compliance Center > Information governance > Retention policies for orgs
without records management.
```

### Recipe 10: Workspace Vault retention

```text
Google Workspace Vault > Retention > Rules

Default rule:
- Service: Drive / Gmail / Chat / Groups / Meet / Sites / Voice
- Hold all OR delete after N days

Custom rule:
- Apply to specific OU
- Conditions: search query
- Action: Indefinite hold OR delete after N days

Storage region: required for GDPR Art. 28 compliance.
```

### Recipe 11: Annual retention audit

```text
1. Inventory: data categories in scope.
2. Verify schedule current (annual review).
3. Spot-check 10-20 records:
   - Was it deleted at expected time?
   - Was legal hold honored?
   - Documentation matches actual?
4. Identify gaps + corrective actions.
5. Update schedule.
6. Report to senior management.
```

### Recipe 12: Deletion certification

```markdown
# Data Deletion Certification

**Reference:** <Deletion request ID / DSR / Project>
**Date:** <YYYY-MM-DD>
**Approver:** <Privacy Lead + Sec Lead>

## Scope
- Data category: <PII / PHI / customer data>
- Volume: <records / GB>
- Source systems: <list>
- Vendors involved: <sub-processors>

## Method
- Hard delete via <script / API>
- Cryptoshred (key ID: <KMS key ARN>)
- Backup expiry (rotation cycle: <date>)

## Verification
- Record count post-deletion: <0>
- Sample query verification: <results>
- Vendor confirmation (per DPA): <attached>

## Retention exceptions (if any)
- Legal hold active: <Y/N + matter>
- Regulatory retention: <citation>
- Aggregated / anonymized statistical: <Y/N + method>

## Sign-off
- Privacy Lead: <name + date>
- Sec Lead: <name + date>
- Retention period of THIS certificate: <e.g. 7 years>

---
*Disclaimer per template.*
```

### Recipe 13: AI training data retention

```text
EU AI Act + ISO 42001 considerations:

- Training data retention tied to model lifecycle.
- Post-market monitoring may require retaining training samples for
  bias / drift analysis.
- Data subject rights still apply to training data containing PII.
- "Right to be forgotten" → if data subject asks for deletion:
  - Remove from training set + future retraining
  - Document inability to remove already-trained model (or retrain)
- Document retention rationale per data category.

Documentation:
- AI inventory (`ai-governance-eu-ai-act-eticas-credo`)
- Training data lineage
- Refresh / retrain cadence
```

## Examples

### Example 1: Stand up retention policy

**Goal:** Build retention schedule + policy for 100-person SaaS.

**Steps:**
1. Inventory data categories (Recipe 2 template).
2. Cross-reference legal obligations (Recipe 3).
3. Document schedule.
4. Implement automated deletion (Recipe 4) for key systems.
5. Purview retention labels (Recipe 9).
6. Annual audit calendar (Recipe 11).

**Result:** GDPR Art. 5(1)(e) + SOC 2 + CCPA compliant.

### Example 2: Process erasure with backups

**Goal:** User requests RTBF; cascade through systems + backups.

**Steps:**
1. Verify identity (`ccpa-cpra-dsar-workflows` Recipe 3).
2. Hard delete from production (Recipe 4).
3. Backup retention: document; next rotation cycle.
4. Suppression list: re-create blocking.
5. Sub-processor cascade.
6. Deletion certificate (Recipe 12).

**Result:** Compliant erasure.

### Example 3: Legal hold

**Goal:** Pending litigation; preserve email + Slack + Drive for 5 custodians.

**Steps:**
1. Counsel issues hold memo.
2. Purview eDiscovery (Premium) hold OR M365 retention policy.
3. Slack: enable retention with hold.
4. Drive / Vault hold.
5. Notify custodians.
6. Quarterly reminder.
7. Release at case resolution; resume normal deletion.

**Result:** Discovery preserved; release clean.

## Edge cases / gotchas

- **Backups + erasure = tension.** Industry standard: natural rotation. Document.
- **Cross-jurisdiction conflict.** EU storage limitation vs US tax retention can conflict; longest applicable wins.
- **Auto-deletion failures.** Calendar quarterly verification of deletion jobs.
- **Sub-processor cascade.** DPAs must include deletion obligations; verify.
- **Legal hold scope creep.** Counsel may over-scope; right-size.
- **Soft delete that's never hard-deleted** is non-compliance for GDPR.
- **Audit log retention** can conflict with deletion — most regulators accept hashing identifiers.
- **AI model "memory."** Trained model may retain personal data; document inability to selectively forget.
- **Replicas + read-replicas + analytics warehouse.** Deletion cascades to all stores; map upfront.
- **State law variation.** Some states require notice before deletion (e.g., HR records); check.
- **PCI auth data MUST NOT be stored** post-authorization — common error in custom payment flows.
- **HIPAA 6yr is FROM CREATION OR LAST EFFECTIVE** date — whichever is LATER. Newer than expected.
- **Retention vs minimum necessary.** Minimum necessary (HIPAA) is collection limit; retention is keep-until.

> ⚠ **This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.**

## Sources

- [GDPR Art. 5(1)(e) Storage limitation](https://gdpr-info.eu/art-5-gdpr/)
- [HHS HIPAA §164.316(b)(2)](https://www.ecfr.gov/current/title-45/section-164.316)
- [FINRA Rule 4511 + 17a-4](https://www.finra.org/rules-guidance/key-topics/books-records)
- [SEC 17a-4](https://www.ecfr.gov/current/title-17/chapter-II/part-240/section-240.17a-4)
- [IRS Records Retention](https://www.irs.gov/businesses/small-businesses-self-employed/how-long-should-i-keep-records)
- [SOX §802](https://www.govinfo.gov/content/pkg/PLAW-107publ204/html/PLAW-107publ204.htm)
- [Microsoft Purview Records Management](https://learn.microsoft.com/en-us/purview/records-management)
- [Google Workspace Vault](https://support.google.com/vault/answer/2462365)
- [OneTrust Retention](https://www.onetrust.com/products/data-discovery-classification/)
- [Securiti.ai Retention](https://securiti.ai/)
- [DataGrail](https://www.datagrail.io/)
- [NIST SP 800-88 Rev. 1 Media Sanitization](https://csrc.nist.gov/pubs/sp/800/88/r1/final)
