---
name: clm-ironclad-contractworks-integration
description: Integrate with CLM platforms — Ironclad (enterprise workflow + AI clause discovery), ContractWorks (SMB repository + e-sign), Lexion (DocuSign-owned pre-execution workflow), LinkSquares (AI post-execution analysis), Evisort (clause search), Concord, Agiloft, SirionLabs. Push contracts, trigger workflows, pull repository data, sync clause libraries. Use when the user says "push to Ironclad", "ContractWorks repository", "LinkSquares export", "Evisort search", "CLM integration", "contract repository sync".
---

# CLM integration — Ironclad / ContractWorks / Lexion / LinkSquares / Evisort

This skill ships the read/write integrations to the major CLM platforms. The CLM itself is the contract repository + workflow + AI extraction engine; this skill is the pipe between it and the rest of the doc-gen stack.

## When to use

User says:

- "Push the executed contract into Ironclad"
- "Pull all our MSAs from ContractWorks"
- "Trigger an Ironclad workflow from a HubSpot deal"
- "Sync the LinkSquares clause library to our local catalog"
- "Evisort search for indemnity caps below $X"
- "Lexion review workflow before DocuSign send"
- "Concord / Agiloft / SirionLabs"

Companion skills:
- `contract-template-authoring-msa-nda` — source of templates pushed to CLM workflows.
- `e-signature-docusign-adobe-sign-pandadoc` — execution side.
- `audit-trail-e-sign-versioning` — Certificate of Completion archival.
- `ai-summarization-clause-extraction` — local mirror of CLM extraction.

## Setup

```bash
# Ironclad — Public API v1 (REST)
# Required env: IRONCLAD_API_KEY (per-workspace; admin → API Keys)
# Base: https://ironcladapp.com/public/api/v1
# Docs: https://developer.ironcladapp.com/reference/

# ContractWorks — REST API
# Required env: CONTRACTWORKS_API_KEY, CONTRACTWORKS_WORKSPACE_ID

# Lexion — REST API (now DocuSign IAM-secured post-acquisition)
# Required env: LEXION_API_KEY OR DocuSign OAuth token w/ Lexion scope

# LinkSquares — REST API
# Required env: LINKSQUARES_API_KEY

# Evisort — REST API
# Required env: EVISORT_API_KEY

# Concord — REST API
# Required env: CONCORD_API_TOKEN

# Agiloft — REST + EWS
# Required env: AGILOFT_API_TOKEN, AGILOFT_KB

# All curl-based — no SDK needed (helps with cli-anything)
pip install requests
```

## Common recipes

### Recipe 1: Pick the CLM

| CLM | Best for | Pricing tier (approx 2026) | Strength | Weakness |
|---|---|---|---|---|
| Ironclad | Enterprise + procurement-led | $20K+/yr | Mature workflow + AI Assist | Steep onboarding |
| ContractWorks | SMB repository + e-sign | $7K-15K/yr | Simple; cost-effective; e-sign included | Light on workflow |
| Lexion (DocuSign) | Pre-execution legal workflow | Bundled into DocuSign IAM | Tightly integrated with DocuSign | DocuSign-centric |
| LinkSquares | Post-execution AI + analytics | $20K+/yr | AI-first clause extraction | Pre-exec workflow lighter |
| Evisort | Pure AI clause search | $25K+/yr | Best-in-class clause AI | Repo-only, not workflow-first |
| Concord | Mid-market all-in-one | $8K-20K/yr | Negotiation collab + simple workflow | AI capabilities lighter |
| Agiloft | Complex configurable workflow | $50K+/yr | Low-code workflow engine | Older UX |
| SirionLabs | Sourcing + supplier-side | $50K+/yr | Strong on supplier mgmt | Buy-side focused |

Pick: Ironclad for enterprise legal-led; ContractWorks for SMB; LinkSquares for post-exec analytics; Evisort if AI search is the killer feature.

### Recipe 2: Ironclad — list workflows + create a draft

```bash
# List active workflow templates
curl https://ironcladapp.com/public/api/v1/workflows \
  -H "Authorization: Bearer $IRONCLAD_API_KEY"

# Launch a new draft from workflow template
curl -X POST https://ironcladapp.com/public/api/v1/workflows \
  -H "Authorization: Bearer $IRONCLAD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "template": "msa-customer-v3",
    "creator": "rep@widgetco.com",
    "attributes": {
      "counterparty": "Acme Corp",
      "deal_value": 240000,
      "term_length": 36,
      "renewal": "auto"
    }
  }'
```

### Recipe 3: Ironclad — upload + attach a doc to a workflow record

```bash
WORKFLOW_ID=...
curl -X POST https://ironcladapp.com/public/api/v1/workflows/$WORKFLOW_ID/documents \
  -H "Authorization: Bearer $IRONCLAD_API_KEY" \
  -F "file=@msa-acme-draft.docx" \
  -F "name=MSA - Acme - Draft v1"
```

### Recipe 4: Ironclad — fetch records by query

```bash
# Records with deal_value > $100K and stage = "Counterparty Review"
curl -X POST https://ironcladapp.com/public/api/v1/records/search \
  -H "Authorization: Bearer $IRONCLAD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "type": "AND",
      "filters": [
        { "property": "deal_value", "operator": "GREATER_THAN", "value": 100000 },
        { "property": "stage", "operator": "EQUALS", "value": "Counterparty Review" }
      ]
    },
    "page": 1, "pageSize": 100
  }'
```

### Recipe 5: Ironclad — webhook on workflow stage transition

```bash
curl -X POST https://ironcladapp.com/public/api/v1/webhooks \
  -H "Authorization: Bearer $IRONCLAD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "events": ["workflow.activated", "workflow.completed", "workflow.archived"],
    "targetURL": "https://your-app/webhooks/ironclad"
  }'
```

Validate `X-Ironclad-Signature` header (HMAC-SHA256) on inbound.

### Recipe 6: ContractWorks — upload contract + tag

```bash
curl -X POST https://app.contractworks.com/api/v2/contracts \
  -H "Authorization: Bearer $CONTRACTWORKS_API_KEY" \
  -F "file=@msa-acme-executed.pdf" \
  -F 'metadata={"counterparty":"Acme Corp","type":"MSA","start_date":"2026-06-15","end_date":"2029-06-14","renewal":"auto","tags":["enterprise","americas"]}'
```

ContractWorks auto-OCRs PDF + applies AI tags; tags also drive its reminder workflow.

### Recipe 7: ContractWorks — list expiring contracts (renewal mgmt)

```bash
curl "https://app.contractworks.com/api/v2/contracts?expires_within_days=90" \
  -H "Authorization: Bearer $CONTRACTWORKS_API_KEY"
```

Push the response into Linear/Jira via `linear-mcp` / `jira-mcp` as renewal tasks.

### Recipe 8: LinkSquares — upload + trigger AI extraction

```bash
curl -X POST https://api.linksquares.com/v1/contracts \
  -H "Authorization: Bearer $LINKSQUARES_API_KEY" \
  -F "file=@msa-acme-executed.pdf" \
  -F "agreement_type=MSA"
```

Poll for AI completion:

```bash
curl https://api.linksquares.com/v1/contracts/$ID/clauses \
  -H "Authorization: Bearer $LINKSQUARES_API_KEY"
```

Returns indemnity, LoL, term, auto-renewal, governing law, etc., as structured JSON.

### Recipe 9: Evisort — semantic clause search across repo

```bash
curl -X POST https://api.evisort.com/v1/search \
  -H "Authorization: Bearer $EVISORT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "indemnity cap less than 2x fees paid",
    "filters": { "agreement_type": ["MSA","Cloud Service"] }
  }'
```

Returns matching contract IDs + clause snippets. Good for "which contracts have weak indemnity caps?" risk audits.

### Recipe 10: Lexion — list workflow tasks + complete

```bash
# Tasks assigned to me
curl https://api.lexion.ai/v1/tasks?assignee=$USER_ID \
  -H "Authorization: Bearer $LEXION_TOKEN"

# Mark approved
curl -X POST https://api.lexion.ai/v1/tasks/$TASK_ID/complete \
  -H "Authorization: Bearer $LEXION_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"decision":"approved","note":"Standard terms; cleared by legal."}'
```

### Recipe 11: Concord — push contract via REST

```bash
curl -X POST https://api.concordnow.com/api/rest/3/organizations/$ORG_ID/folders/$FOLDER_ID/agreements \
  -H "Authorization: Bearer $CONCORD_API_TOKEN" \
  -F "file=@msa-acme.pdf" \
  -F "title=MSA - Acme Corp"
```

### Recipe 12: Agiloft — fire a record-create via EWS

```python
import requests
xml = """<?xml version="1.0"?>
<EWCreateRecord login="user" password="pass" kb="Contracts">
  <table>Contract</table>
  <fields>
    <field name="contract_name">MSA - Acme</field>
    <field name="counterparty">Acme Corp</field>
    <field name="deal_value">240000</field>
  </fields>
</EWCreateRecord>"""
r = requests.post(f"https://{AGILOFT_HOST}/gui2/ewservices",
                  data=xml,
                  headers={"Content-Type": "text/xml"})
```

### Recipe 13: Cross-CLM contract migration

```python
# Pull from ContractWorks → push to Ironclad with mapping
import requests

# Source pull
cw = requests.get("https://app.contractworks.com/api/v2/contracts",
                  headers={"Authorization": f"Bearer {CW_KEY}"}).json()

for c in cw["data"]:
    # Map ContractWorks fields to Ironclad workflow attributes
    payload = {
        "template": template_for(c["type"]),
        "attributes": {
            "counterparty": c["counterparty"],
            "deal_value": c.get("value", 0),
            "term_start": c["start_date"],
            "term_end": c["end_date"],
        }
    }
    # Push to Ironclad
    requests.post("https://ironcladapp.com/public/api/v1/workflows",
                  headers={"Authorization": f"Bearer {IRONCLAD_KEY}"},
                  json=payload)
```

## Examples

### Example 1: Render MSA → push to Ironclad workflow → e-sign on approval

**Goal:** End-to-end from contract template to executed in CLM.
**Steps:**
1. `contract-template-authoring-msa-nda` renders MSA docx.
2. Recipe 2 — launch Ironclad workflow with deal attributes.
3. Recipe 3 — attach the draft docx.
4. Ironclad routes through legal-counsel review (in-platform).
5. Recipe 5 — webhook on `workflow.completed` → triggers `e-signature-docusign-adobe-sign-pandadoc` send.
6. `audit-trail-e-sign-versioning` archives executed PDF + cert back into Ironclad workflow.

**Result:** Round-trip MSA execution in one orchestration.

### Example 2: Quarterly indemnity-risk audit via Evisort

**Goal:** Find every contract with sub-standard indemnity caps before Q3 board meeting.
**Steps:**
1. Recipe 9 — Evisort semantic search for weak caps across MSA + Cloud Service agreements.
2. Pull each contract metadata via Recipe 8 on LinkSquares (parallel coverage).
3. Build CSV: contract_id, counterparty, current cap, recommended cap, action.
4. Hand off to `legal-counsel` for redline strategy.

**Result:** Risk-prioritized list ready for the legal-ops standup.

### Example 3: SMB ContractWorks renewal workflow

**Goal:** 90-day-out renewal alerts auto-create CSM tasks.
**Steps:**
1. Recipe 7 — daily cron pulls expiring contracts.
2. Each result → `linear-mcp` creates a "Renewal: <counterparty>" issue.
3. `customer-success` sibling agent owns the issue + drafts renewal proposal via `proposal-automation-pandadoc-proposify-qwilr`.

**Result:** No renewal slips through cracks.

## Edge cases / gotchas

- **Ironclad workflow vs records API.** Workflows are pre-execution; records are post-execution. Don't confuse the endpoints.
- **Ironclad attribute schema drifts.** Each workflow template has its own attribute schema; pull `/workflows/$template/schema` before sending.
- **Webhook signature validation.** Every CLM signs webhooks; always validate HMAC before processing.
- **Rate limits.** Ironclad: 100 req/min; ContractWorks: 60/min; LinkSquares: 120/min. Use exponential backoff.
- **Pagination styles differ.** Ironclad cursor; ContractWorks offset; LinkSquares offset; Evisort cursor — don't assume.
- **API key scope.** Ironclad has read-only vs admin keys; many ops require admin scope.
- **PDF vs docx upload.** Most CLMs OCR PDFs but prefer docx for clause AI; send docx when available.
- **Counterparty deduplication.** CLMs use fuzzy match on counterparty name; create a master list to avoid "Acme Corp" vs "Acme Corp." duplicate records.
- **Custom metadata vs standard fields.** Use standard fields where possible — custom fields don't surface in default reports.
- **Lexion + DocuSign IAM.** Post-2024 acquisition, Lexion auth moved under DocuSign IAM; refresh tokens differ from legacy Lexion auth.
- **Concord on-prem region.** EU vs US instances at different base URLs; check user's region.
- **Migration data loss.** When moving CLMs, attachments + comments often don't migrate cleanly; map only the fields that exist on both sides.
- **AI extraction confidence.** LinkSquares + Evisort + Ironclad AI return clause confidence; always flag <0.85 for human review.
- **Pricing tier gates.** Some APIs (Ironclad bulk export, LinkSquares analytics) are paywalled — verify the user's tier before promising features.

## Sources

- [Ironclad Public API](https://developer.ironcladapp.com/reference/) — workflows + records + webhooks.
- [ContractWorks API](https://www.contractworks.com/contractworks-integrations) — REST upload + metadata.
- [Lexion docs](https://www.lexion.ai/) — workflow + tasks API.
- [LinkSquares API](https://help.linksquares.com/hc/en-us) — clause extraction + analytics.
- [Evisort API](https://docs.evisort.com/) — semantic search + extraction.
- [Concord API](https://api.concordnow.com/api-docs) — agreement create + manage.
- [Agiloft Hawkeye REST](https://www.agiloft.com/documentation/rest-api.html) — record CRUD.
- [SirionLabs developer](https://www.sirion.ai/) — sourcing CLM.
- Sister skills: `contract-template-authoring-msa-nda`, `e-signature-docusign-adobe-sign-pandadoc`, `audit-trail-e-sign-versioning`, `ai-summarization-clause-extraction`.
