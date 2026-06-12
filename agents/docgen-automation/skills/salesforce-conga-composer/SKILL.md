---
name: salesforce-conga-composer
description: Generate documents from Salesforce data using Conga Composer (the Salesforce AppExchange leader for doc gen) — merge Salesforce records into Word / Excel / PPT / PDF templates with conditional logic, loop over child records (opportunity → line items), and chain to Conga Sign or DocuSign. Fallback to PandaDoc + Salesforce native integration when Conga is not licensed. Use when the user says "Conga Composer", "Salesforce doc gen", "merge Salesforce into Word", "Composer URL button", "Salesforce CPQ proposal".
---

# Salesforce-to-doc generation — Conga Composer + PandaDoc fallback

This skill ships the Salesforce-native doc generation pipeline. The dominant 2026 tool is Conga Composer (formerly Appextremes); the agent has the wiring for both Composer URL-based and Composer Direct REST.

## When to use

User says:

- "Generate a quote / proposal from this Salesforce opportunity"
- "Conga Composer / Conga Sign"
- "Merge Salesforce data into a Word / Excel / PPT template"
- "Salesforce CPQ → proposal PDF"
- "Composer URL button on an opportunity"
- "Lightning Flow action that creates a proposal"
- "Without Conga, what's the Salesforce alternative?" → PandaDoc / DocuSign Gen / S-Docs / Nintex DocGen

Companion skills:
- `proposal-automation-pandadoc-proposify-qwilr` — PandaDoc fallback path.
- `e-signature-docusign-adobe-sign-pandadoc` — Conga Sign vs DocuSign hand-off.
- `dynamic-pricing-variable-insertion` — CPQ-driven line-item math.
- `clm-ironclad-contractworks-integration` — push executed proposal into CLM.

## Setup

```bash
# Salesforce — REST API for record fetching + CPQ
# Required env: SF_INSTANCE_URL, SF_ACCESS_TOKEN (or use OAuth refresh token)
# Default skill: salesforce-api
pip install simple-salesforce

# Conga Composer — accessed via Composer URL pattern OR Composer Direct REST
# Required env (URL mode): SF session ID (Salesforce-issued) — auto in Lightning context
# Required env (REST mode): CONGA_API_KEY, CONGA_DC_BASE_URL (https://composer.congamerge.com or regional)

# Conga Sign (if e-sign via Conga)
# Required env: CONGA_SIGN_API_KEY

# Fallback: PandaDoc REST
# Required env: PANDADOC_API_KEY
```

## Common recipes

### Recipe 1: Pick the doc-gen path

| Option | Best when | Notes |
|---|---|---|
| Conga Composer (URL button on record) | Click-to-generate UX in SF | Renders in browser; supports Word/Excel/PPT/PDF |
| Conga Composer Direct (REST) | Server-side batch | No browser; raw REST |
| Conga CPQ Generate | Salesforce CPQ orgs | Native CPQ workflow |
| S-Docs | Free-tier alternative | Limited features |
| Nintex DocGen (formerly Drawloop) | Nintex shops | Workflow-heavy |
| PandaDoc + SF native | No Conga license | Less native, broader features |
| DocuSign Gen for Salesforce | DocuSign-only shop | Tightly bound to DocuSign |
| Mail merge (manual) | Edge / one-off | Not recommended |

Default: Conga Composer if licensed; PandaDoc otherwise.

### Recipe 2: Build a Composer URL button

Composer URL pattern:

```
https://composer.congamerge.com/Composer8/index.html
  ?sessionId={!$Api.Session_ID}
  &serverUrl={!$Api.Partner_Server_URL_290}
  &id={!Opportunity.Id}
  &templateId=a0X1U000000XXXXUAJ
  &DefaultPDF=1
  &EmailToId={!Opportunity.Primary_Contact_Email__c}
  &OFN=Proposal-{!Opportunity.Name}
```

Create a Salesforce custom button on Opportunity → Behavior: Execute JavaScript (Classic) or Lightning Web Component action.

### Recipe 3: Conga Composer template authoring (Word merge fields)

Inside the Word template, use Composer's merge syntax:

```text
Customer: «Opportunity_Account_Name»
Deal value: «Opportunity_Amount»
Term length: «Opportunity_Term_Months__c»

«TableStart:LineItems»
 - «Product__r_Name» × «Quantity__c» @ «UnitPrice__c»  = «TotalPrice__c»
«TableEnd:LineItems»

«IF Opportunity_Tier__c="Enterprise"»
   This MSA is governed by Section 8 SLA.
«ENDIF»
```

Conga supports: simple fields, `«TableStart» / «TableEnd»` for child loops, `«IF» / «ELSEIF» / «ENDIF»` for conditionals.

### Recipe 4: Composer Direct REST (server-side)

```bash
curl -X POST $CONGA_DC_BASE_URL/composer/api/v1/composer \
  -H "Authorization: Bearer $CONGA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "'"$SF_ACCESS_TOKEN"'",
    "serverUrl": "'"$SF_INSTANCE_URL"'/services/Soap/u/56.0",
    "templateId": "a0X1U000000XXXXUAJ",
    "recordId": "0061U000000abcdAAA",
    "outputFormat": "PDF",
    "queries": ["Conga_LineItems_Query"]
  }'
```

Returns the generated doc as base64 or as a URL pointer.

### Recipe 5: Conga query — define a parent-child record pull

Create a Conga Query custom record:

```sql
SELECT Id, Product2.Name, Quantity, UnitPrice, TotalPrice
FROM OpportunityLineItem
WHERE OpportunityId = '{pv0}'
ORDER BY ListPrice DESC
```

Reference in Composer URL via `&queryId=a0Q...` or in REST via `"queries":["Conga_LineItems_Query"]`.

### Recipe 6: Conga Sign — send for signature

```bash
curl -X POST $CONGA_SIGN_API/v1/transactions \
  -H "Authorization: Bearer $CONGA_SIGN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MSA - Acme - 2026-Q2",
    "documents": [{"file_base64": "...", "name": "msa.pdf"}],
    "recipients": [{
      "email": "buyer@acme.com",
      "name": "Jane Smith",
      "role": "SIGNER",
      "routing_order": 1
    }],
    "salesforceRecordId": "0061U000000abcdAAA"
  }'
```

### Recipe 7: Lightning Flow action — generate proposal on stage change

In Setup → Flows, create a record-triggered flow:

1. Trigger: Opportunity StageName changes to "Proposal".
2. Action: Apex callout (or external service) → Recipe 4 (Composer Direct).
3. Action: Attach returned PDF to Opportunity as `ContentDocument`.
4. Action: Update Opportunity field `Proposal_Generated_At__c = NOW()`.

### Recipe 8: PandaDoc fallback — Salesforce data → PandaDoc template

```bash
# 1) Fetch the opp + line items
curl "$SF_INSTANCE_URL/services/data/v56.0/sobjects/Opportunity/0061U.../$SF_LINE_ITEMS_QUERY" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"

# 2) Create PandaDoc from template
curl -X POST https://api.pandadoc.com/public/v1/documents \
  -H "Authorization: API-Key $PANDADOC_API_KEY" \
  -H "Content-Type: application/json" \
  -d @<(cat <<EOF
{
  "name": "Proposal - Acme",
  "template_uuid": "abc...",
  "recipients": [
    {"email":"buyer@acme.com","first_name":"Jane","last_name":"Smith","role":"client"}
  ],
  "tokens": [
    {"name":"opp.amount","value":"240000"},
    {"name":"opp.term","value":"36"}
  ],
  "pricing_tables":[{
    "name":"Pricing",
    "data_merge": false,
    "sections":[{"title":"Subscription","rows":[
      {"options":{"qty_editable":false},"data":{"name":"Pro Plan","price":2000,"qty":120}}
    ]}]
  }]
}
EOF
)
```

### Recipe 9: Salesforce CPQ → Conga Composer chain

Salesforce CPQ produces a Quote record + QuoteLineItem records; Conga Composer merges those into the proposal Word template. The Conga button can be placed on the Quote object — Composer pulls `Quote` + child `QuoteLineItem` automatically.

### Recipe 10: DocuSign Gen for Salesforce (DocuSign-only shops)

Setup → DocuSign for Salesforce → Document Generation feature; tag Word templates with field merge tokens, attach to a Process Builder / Flow trigger. Generated PDFs flow into DocuSign Envelopes for signature.

### Recipe 11: Auto-archive output to Files + sync to Drive

```bash
# After Composer returns PDF, attach as ContentVersion
curl -X POST "$SF_INSTANCE_URL/services/data/v56.0/sobjects/ContentVersion" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "Title": "Proposal - Acme",
    "PathOnClient": "proposal-acme.pdf",
    "VersionData": "'"$(base64 -i proposal.pdf)"'",
    "FirstPublishLocationId": "0061U000000abcdAAA"
  }'
# Then mirror to Drive
gdrive upload --parent $DRIVE_FOLDER proposal.pdf
```

### Recipe 12: Test in sandbox first

Conga URL parameters differ between Salesforce sandbox and prod base URLs:
- Production: `https://composer.congamerge.com`
- Sandbox: `https://composer.congamerge.com` (same domain; sessionId comes from sandbox)

Build sandbox test buttons + templates before flipping prod.

## Examples

### Example 1: Click-to-generate Enterprise MSA from Opportunity

**Goal:** AE clicks one button on an Opp → branded MSA pre-filled.
**Steps:**
1. Recipe 3 — author MSA Word template with merge fields.
2. Recipe 5 — Conga Query for `OpportunityLineItem`.
3. Recipe 2 — build the URL button; place on Opportunity layout.
4. AE clicks → PDF previewed → DocuSign send (via Conga Sign or DocuSign hand-off).
5. Recipe 11 — attach to opp record.

**Result:** 30-second proposal create instead of 30-minute Word merge.

### Example 2: Auto-generate proposal on stage change

**Goal:** When Opp moves to "Proposal", generate + email the doc automatically.
**Steps:**
1. Recipe 7 — Lightning Flow on stage change.
2. Recipe 4 — Composer Direct call from Apex.
3. Recipe 11 — attach to record + email to primary contact.
4. Slack notify the AE: "Proposal sent to <contact>".

**Result:** Hands-free proposal creation tied to pipeline progression.

### Example 3: Non-Conga shop — Salesforce + PandaDoc fallback

**Goal:** Org doesn't have Conga; still needs proposal automation.
**Steps:**
1. Recipe 8 — PandaDoc template authored in PandaDoc UI.
2. AE creates PandaDoc directly inside Salesforce via the PandaDoc add-in.
3. PandaDoc analytics + e-sign embedded.

**Result:** PandaDoc covers it; cheaper for sub-50-rep teams.

## Edge cases / gotchas

- **Salesforce session ID expiration.** `$Api.Session_ID` is short-lived; for batch Composer Direct, use OAuth refresh token instead.
- **Lightning Locker.** Composer 8 URL buttons work in Lightning + Classic; Composer 7 is Classic-only.
- **Merge field naming.** Conga uses `«Object_Field»` (underscore-joined); some special chars need escaping.
- **TableStart/TableEnd inside paragraphs.** They must be in plain paragraphs, not inside tables — Word merging breaks otherwise.
- **CPQ Quote rendered vs Composer rendered.** CPQ has its own PDF rendering; Conga overrides it. Decide which is canonical.
- **Email send via Composer.** `&EmailToId=...` parameter sends via Salesforce email; respects org-wide email config.
- **Conga query governor limits.** Per Salesforce SOQL limits — 50K rows per query.
- **Image inclusion.** Need `&CETID=` for chart inclusion + image merge field syntax with `«IMG__c»`.
- **Locale / currency formatting.** Use `&FP0=MultiCurrency=1` in URL to enforce per-record currency formatting.
- **Profile permissions.** Users need "API Enabled" + Conga managed package perms.
- **Conga Composer License.** Per-user; check available licenses before mass rollout.
- **Sandbox templateId differs from prod.** Templates must be deployed (Conga Solutions managed package or change sets) — don't hardcode IDs.
- **HTML email body.** When using `&EmailHTMLBodyId=`, body must be a stored Conga Email Template, not an arbitrary Salesforce email template.
- **DocuSign vs Conga Sign on the same doc.** If both add-ons installed, choose explicitly per template — running both causes duplicate envelopes.
- **PandaDoc as fallback.** PandaDoc + Salesforce sync is one-way (Salesforce → PandaDoc); analytics flow back via PandaDoc webhook → SF Custom Object.

## Sources

- [Conga Composer documentation](https://documentation.conga.com/composer) — URL parameters + templates.
- [Conga Composer Direct REST](https://documentation.conga.com/composer/composer-direct/) — server-side rendering.
- [Conga Sign API](https://documentation.conga.com/sign) — Conga's e-sign.
- [Salesforce REST API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/) — record fetch + ContentVersion attach.
- [Salesforce CPQ Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.cpq_dev_api.meta/cpq_dev_api/) — Quote + QuoteLineItem.
- [DocuSign Gen for Salesforce](https://www.docusign.com/products/gen-salesforce) — DocuSign-only alternative.
- [S-Docs](https://www.sdocs.com/) — free-tier alternative.
- [Nintex DocGen](https://www.nintex.com/process-platform/document-generation/) — Nintex workflow alternative.
- [PandaDoc Salesforce integration](https://www.pandadoc.com/integrations/salesforce/) — fallback path.
- Sister skills: `proposal-automation-pandadoc-proposify-qwilr`, `dynamic-pricing-variable-insertion`, `e-signature-docusign-adobe-sign-pandadoc`, `clm-ironclad-contractworks-integration`.
