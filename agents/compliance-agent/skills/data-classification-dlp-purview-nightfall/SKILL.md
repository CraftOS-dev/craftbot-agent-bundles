---
name: data-classification-dlp-purview-nightfall
description: Data classification scheme + DLP (Data Loss Prevention) deployment. Sensitivity labels (Public / Internal / Confidential / Restricted). 2026 SOTA tools — Microsoft Purview (M365-native + consolidated DLP + DSPM + insider risk + AI), Nightfall AI (API-first SaaS — Slack/Salesforce/GitHub/GenAI), Cyberhaven (Data Lineage / DDR — 2026 unified AI & data security platform), Varonis (file-system + AD), Forcepoint, Symantec DLP. GenAI is biggest 2026 DLP challenge (avg 66 GenAI apps/org).
---

# Data Classification + DLP

Classification scheme + DLP rule deployment. 2026 SOTA: Microsoft Purview (M365-native), Nightfall (API-first SaaS), Cyberhaven (data lineage / DDR), Varonis (file + AD).

## When to use

User says:
- "Data classification" / "sensitivity labels"
- "DLP" / "Data Loss Prevention"
- "Microsoft Purview" / "Nightfall" / "Cyberhaven" / "Varonis"
- "GenAI data leakage" / "ChatGPT DLP"
- "DSPM" / "Data Security Posture Management"
- "Insider risk"
- "Data lineage" / "DDR" / "Data Detection and Response"
- "Sensitive PII detection"

Companion skills: `data-retention-deletion-policy`, `ai-governance-eu-ai-act-eticas-credo`, `gdpr-article-30-ropa-dpia`.

## Setup

```bash
# Microsoft Purview (E5 or P2)
# https://learn.microsoft.com/en-us/purview/
# Tenant + Compliance Center access

# Nightfall AI
# https://www.nightfall.ai/
export NIGHTFALL_API_KEY=<dashboard>

# Cyberhaven
# https://www.cyberhaven.com/

# Varonis
# https://www.varonis.com/

# Open-source / OSS
# https://github.com/microsoft/presidio    — Microsoft Presidio (PII detection)
# https://github.com/uber/cadence-data-loss-prevention
```

Auth notes:
- Purview included in M365 E5 + Compliance F5 + standalone P2.
- Nightfall has free starter; paid tier scales.
- Cyberhaven 2026 unified platform (post-2024 launch).

## Common recipes

### Recipe 1: Classification scheme

```text
4-tier (default — most orgs):

PUBLIC:
- Marketing materials, public web content
- Press releases (after embargo)
- No-restriction publish

INTERNAL:
- Employee directory, internal comms
- Roadmap docs (non-customer)
- Default for all non-public content
- Standard handling

CONFIDENTIAL:
- Customer data (general)
- Business strategy
- Contract terms
- Financial data (pre-public)
- Encryption + access control required

RESTRICTED:
- PII / PHI / PCI cardholder data
- Source code (proprietary algorithms)
- IP / patents pre-filing
- Employee personnel files
- Regulated data (banking secrets, IRBs)
- Encryption at rest + in transit MANDATORY
- Tight access + audit logging
- DLP enforcement

Mapped to ISO 27001 A.5.13 + GDPR data minimization + HIPAA + PCI.
```

### Recipe 2: Classification labeling — apply to assets

```text
Manual + auto:

Microsoft Purview sensitivity labels:
- Word / Excel / PowerPoint: sidebar label
- Outlook email: prefix [CONFIDENTIAL] in subject + footer
- SharePoint / OneDrive: visual marker + RMS protection
- Auto-labeling: regex + ML-based detection (e.g., 9-digit pattern → SSN
  → Restricted)

Google Workspace Drive labels:
- DLP rules; Drive sensitivity labels (in Workspace Enterprise Plus +
  Education Plus).

File-system DLP (Cyberhaven, Varonis):
- File metadata + content scanning.
- Apply label as extended attribute or metadata.

Code repos:
- README + repo-level classification tag (custom; GH topic, GitLab label).
- File-level "DO NOT DISTRIBUTE" header.

Database tables:
- Column-level classification (SHOW POLICIES).
- Snowflake: classification + tags.
- BigQuery: Data Catalog + DLP scan.
- AWS Macie for S3.
```

### Recipe 3: PII detection patterns (Presidio / Nightfall)

```text
Standard PII types (common across DLP tools):

US:
- SSN (123-45-6789 + dashless variants)
- EIN (12-3456789)
- Driver's license (state-specific)
- US passport (9-digit + letter prefix)
- US bank account / routing
- US credit card (LUHN-validated)

EU:
- IBAN (per country regex)
- VAT ID (per country)
- National ID (varies — Italian Codice Fiscale, Spanish DNI, French INSEE, etc.)
- EU passport / DL formats

Healthcare:
- US Medical Record Number (org-specific; pattern-train)
- NHS Number (UK; 10-digit with check)
- ICD-10 code (diagnostic)
- NDC (drug code)

Financial:
- Credit card (Visa/MC/Amex/Discover/JCB by IIN)
- IBAN / BIC / SWIFT
- Bitcoin / ETH wallet (address format)
- Routing + account combo

Identity:
- Email address (regex)
- Phone (E.164 + US/intl)
- IPv4 / IPv6
- MAC address

Custom (org-specific):
- Employee ID
- Customer account ID
- Internal project codenames
- Trade secrets (specific phrases)
```

### Recipe 4: Microsoft Purview DLP rule example

```text
Purview > Solutions > Data loss prevention > Policies > Create policy

Template: "Custom" → "Custom policy"

Locations:
- Exchange email
- SharePoint sites
- OneDrive accounts
- Teams chat + channels
- M365 Copilot (NEW 2026 — DLP scope for Copilot prompts/outputs)
- Endpoint devices (Windows 10/11 + macOS)
- On-premises repositories (Purview agent)

Conditions:
- Content contains: sensitive info type (e.g., US SSN — high confidence)
- Volume: > 1 instance (or > N for higher-confidence aggregation)

Actions:
- Restrict access (apply Encryption / IRM)
- Block sharing externally
- Show policy tip to user
- Notify admin
- Generate incident report
- (Endpoint) Block clipboard copy / removable storage / cloud sync

Test → enforce gradually (audit mode → policy tips → enforcement).
```

### Recipe 5: Nightfall API — scan content

```bash
# https://docs.nightfall.ai/
curl -X POST 'https://api.nightfall.ai/v3/scan' \
  -H "Authorization: Bearer $NIGHTFALL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "payload": ["John SSN is 123-45-6789 and his card is 4111 1111 1111 1111."],
    "policy": {
      "detectionRules": [{
        "detectors": [
          {"detectorType": "NIGHTFALL_DETECTOR", "nightfallDetector": "US_SOCIAL_SECURITY_NUMBER", "minConfidence": "POSSIBLE"},
          {"detectorType": "NIGHTFALL_DETECTOR", "nightfallDetector": "CREDIT_CARD_NUMBER", "minConfidence": "LIKELY"}
        ],
        "logicalOp": "ANY"
      }]
    }
  }'
```

### Recipe 6: Nightfall Slack + GitHub integration

```text
Nightfall Slack:
- OAuth install to workspace.
- Real-time DM + channel scanning.
- Actions: delete + DM user + notify admin.
- Common findings: SSN / cred + secret / customer PII.

Nightfall GitHub:
- App install to org.
- PR-time scan + commit scan + secret scanning.
- Block merge if findings; or warn-only.

Nightfall Salesforce / Confluence / Drive / Jira similar pattern.
```

### Recipe 7: GenAI DLP (2026 critical use case)

```text
Avg 66 GenAI apps in use per org (2026 surveys). Top GenAI DLP risks:

1. Employees pasting customer PII into ChatGPT / Claude / Gemini / Copilot
   public tier.
2. Employees uploading customer docs to AI tools.
3. Employees granting OAuth to unsanctioned GenAI plugins.
4. Code copy-paste into AI (IP leakage).

Controls:
- Network: block public AI tools (DNS filter — Cloudflare Gateway,
  Cisco Umbrella, Zscaler).
- Browser: extension (Nightfall Browser, Cyberhaven Browser) inspects
  content before paste; blocks sensitive content.
- API: API gateway between users + AI (Cyberhaven, Promptly, LayerX);
  redacts before transmission.
- M365 Copilot DLP: Purview integration enforces sensitivity labels.
- Approved tools: enterprise tier ChatGPT Team / Claude for Work /
  Workspace Gemini / M365 Copilot with DPA.

Policy + training:
- AI Use policy (`policy-authoring-cybersecurity-aup-byod`)
- Approved tools list
- Sensitivity-restricted classes (no Restricted in GenAI ever)
- Audit logs review
```

### Recipe 8: Cyberhaven Data Detection + Response (DDR)

```text
Cyberhaven 2026 Unified AI + Data Security Platform:
- Tracks data origin + every action since creation.
- "Data lineage" — file's full history (created → edited → emailed → uploaded).
- Detects unusual access pattern (insider).
- Differentiated from content-only DLP — knows where data CAME FROM.

Use case: 
- Marketing dept doc emailed to personal Gmail — flagged.
- Customer DB export uploaded to ChatGPT — blocked.
- Engineer copies source code to USB — alerted.

Deployed via endpoint agent + cloud APIs.
```

### Recipe 9: Cloud DLP — AWS Macie + GCP DLP + Azure Purview

```bash
# AWS Macie — automatic discovery + DLP for S3
aws macie2 create-classification-job \
  --job-type SCHEDULED \
  --schedule-frequency '{"dailySchedule":{}}' \
  --s3-job-definition '{"bucketDefinitions":[{"accountId":"<>","buckets":["<bucket>"]}]}' \
  --name "weekly-pii-scan"

# GCP DLP — content scan
gcloud dlp inspect-content \
  --info-types "US_SOCIAL_SECURITY_NUMBER,CREDIT_CARD_NUMBER" \
  --content "John SSN 123-45-6789"

# Azure Purview — register data source + scan
az purview account create --resource-group <rg> --name <purview-name>
```

### Recipe 10: Classification + handling matrix

```markdown
# Data Classification + Handling Matrix

| Class | Examples | Encryption (rest) | Encryption (transit) | External share | Storage location | Retention | DLP |
|---|---|---|---|---|---|---|---|
| PUBLIC | Marketing, press | Optional | TLS 1.2+ | Allowed | Anywhere | Per business need | None |
| INTERNAL | Roadmap, comms, internal docs | AES-256 | TLS 1.2+ | Limited (NDA) | M365 / Workspace | 5 years default | Monitor mode |
| CONFIDENTIAL | Customer data, financials, contracts | AES-256 mandatory | TLS 1.3 | Strict (DPA) | M365 / Workspace + DLP-tagged | Per contract | Tip + log |
| RESTRICTED | PII, PHI, PCI, source code | AES-256 + KMS-managed | TLS 1.3 + mTLS where applicable | Forbidden (or signed exception) | Encrypted storage; isolated | Per regulation | Block + alert |

---
*This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.*
```

### Recipe 11: Discovery + inventory (find sensitive data before DLP)

```bash
# Scan SharePoint / OneDrive
# Purview Content Search → search for SSN / CC pattern → output to PST or CSV

# Discover via Microsoft Presidio (open source)
pip install presidio-analyzer presidio-anonymizer
python -c "
from presidio_analyzer import AnalyzerEngine
analyzer = AnalyzerEngine()
results = analyzer.analyze(text='SSN 123-45-6789', entities=['US_SSN'], language='en')
print(results)
"

# AWS Macie discovery jobs (Recipe 9)
# Snowflake classification tags
# BigQuery Data Catalog auto-classification
```

### Recipe 12: DLP rollout phases

```text
Phase 1 — Discovery (1-2 months):
- Scan all repositories (M365, Workspace, S3, file shares).
- Map sensitive data locations.
- Quantify scope.

Phase 2 — Classification (1-2 months):
- Apply sensitivity labels (auto + manual sampling).
- Communicate labels + handling matrix to users.

Phase 3 — Monitor (1-2 months):
- DLP rules in audit-only mode.
- Tune false positives.
- User notifications without enforcement.

Phase 4 — Soft enforce (2 months):
- Policy tips + blocked actions for clear violations.
- Allow override with justification (logged).

Phase 5 — Full enforce:
- Block + alert.
- Selective override (signed exception only).
- Quarterly review of overrides.
```

### Recipe 13: Incident response — DLP alert

```text
1. Alert from Purview / Nightfall / Cyberhaven.
2. Triage:
   - Confirm sensitive content + recipient + context.
   - User intent: error vs malicious?
3. Containment:
   - Recall email (if M365 / Workspace).
   - Revoke share (SharePoint / Drive).
   - Delete external upload (where possible).
4. Investigation:
   - Forensic of user activity.
   - Other sensitive data exposed?
5. Decision:
   - Minor error: coaching + training.
   - Pattern: HR + Legal involvement.
   - Malicious insider: IR plan
     (`incident-response-nist-sp-800-61` Recipe 7).
6. Document; close ticket.
```

## Examples

### Example 1: M365 org DLP rollout

**Goal:** Stand up Purview DLP across Exchange + SharePoint + OneDrive + Teams + Copilot.

**Steps:**
1. Classification scheme (Recipe 1).
2. Auto-labeling rules for PII / PHI / PCI patterns (Recipe 4).
3. Discovery scan (Recipe 11).
4. Apply labels.
5. DLP rule: block external share of Restricted; alert on Confidential.
6. Roll out phased (Recipe 12).

**Result:** SOC 2 CC6.7 + GDPR Art. 32 controls; ISO A.5.13 evidence.

### Example 2: GenAI DLP for ChatGPT

**Goal:** Block customer PII from leaving via ChatGPT.

**Steps:**
1. Block consumer ChatGPT at firewall.
2. Provision approved Claude for Work (DPA + no-training).
3. Browser extension (Cyberhaven Browser) inspects paste → redacts PII.
4. M365 Copilot DLP rules enforce sensitivity labels.
5. AI Use policy + training (`policy-authoring-cybersecurity-aup-byod`).

**Result:** Sanctioned GenAI with safe-handling enforced.

### Example 3: GitHub secret scanning + Nightfall

**Goal:** Detect + block secrets in code commits.

**Steps:**
1. Enable GitHub secret scanning + push protection.
2. Install Nightfall GitHub app for broader DLP (customer data, PII).
3. PR-time scan; block merge on findings.
4. Auto-rotate confirmed secrets.

**Result:** Prevents committed secrets + customer PII leaks.

## Edge cases / gotchas

- **False positive fatigue kills DLP.** Tune; start with audit mode + review weekly.
- **Encryption ≠ DLP.** DLP detects + acts on content; encryption protects at rest.
- **Endpoint vs cloud DLP.** Both needed for comprehensive coverage.
- **DLP can't see encrypted attachments** in email unless TLS termination + scan.
- **OCR cost for image scans.** PNG / PDF screenshots of PII bypass text-only DLP; OCR-enabled scanning required.
- **Auto-labeling accuracy.** Test against known sets; tune confidence thresholds.
- **GenAI is biggest 2026 gap.** Avg 66 unsanctioned AI apps/org → massive shadow IT for data leakage.
- **User override management.** Allow override with justification + audit; abusive override patterns trigger HR.
- **Mobile / BYOD coverage.** DLP harder on personal devices; isolate work data via MAM.
- **Compliance evidence.** Auditors expect classification scheme + DLP rule + exception log + tuning history.
- **Performance impact.** Endpoint DLP can slow systems if rule sets are huge; tune for org.
- **Pricing.** Purview included in E5; standalone P2 ~$10/user/mo. Nightfall ~$5-$15/user/mo. Cyberhaven enterprise $15-$30/user/mo.
- **Insider threat overlap.** DLP-driven insider detection is foundational but not sufficient — pair with UEBA + privileged access monitoring.

> ⚠ **This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.**

## Sources

- [Microsoft Purview](https://learn.microsoft.com/en-us/purview/)
- [Microsoft Purview DLP](https://learn.microsoft.com/en-us/purview/dlp-learn-about-dlp)
- [Microsoft Presidio (OSS)](https://github.com/microsoft/presidio)
- [Nightfall AI](https://www.nightfall.ai/)
- [Nightfall API Docs](https://docs.nightfall.ai/)
- [Cyberhaven](https://www.cyberhaven.com/)
- [Varonis](https://www.varonis.com/)
- [Forcepoint DLP](https://www.forcepoint.com/product/dlp-data-loss-prevention)
- [Symantec DLP (Broadcom)](https://www.broadcom.com/products/cybersecurity/information-protection/data-loss-prevention)
- [Digital Guardian](https://www.digitalguardian.com/)
- [AWS Macie](https://aws.amazon.com/macie/)
- [GCP DLP](https://cloud.google.com/security/products/dlp)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
