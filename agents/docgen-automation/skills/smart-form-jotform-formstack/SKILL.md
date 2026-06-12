---
name: smart-form-jotform-formstack
description: Deploy smart intake forms — Jotform (10K+ templates + native e-sign), Formstack (HIPAA-eligible), Typeform (conversational UX), Tally (free + Notion-style) — and wire submissions to doc generation + e-sign + CRM. Use when the user says "intake form", "smart form", "form to PDF", "Jotform / Formstack / Typeform / Tally", "client onboarding form", "form submission triggers doc gen".
---

# Smart form deployment — Jotform / Formstack / Typeform / Tally

This skill ships the form-intake layer that feeds the document pipeline. The form collects structured data; downstream skills render the doc, route for approval, and e-sign.

## When to use

User says:

- "Intake form for new clients"
- "Form → PDF → e-sign chain"
- "Jotform / Formstack / Typeform / Tally"
- "HIPAA-eligible form"
- "Conditional logic in the form"
- "Form submission to HubSpot / Salesforce / Notion / GSheets"
- "Pre-fill fields from URL parameters"

Companion skills:
- `conditional-logic-doc-assembly` — drive doc branches from form answers.
- `e-signature-docusign-adobe-sign-pandadoc` — sign post-render.
- `redaction-automation-pii` — strip PII from logs.
- `document-workflow-routing-approval` — approval before sign.

## Setup

```bash
# Jotform REST API
# Required env: JOTFORM_API_KEY
# Base: https://api.jotform.com

# Formstack REST API
# Required env: FORMSTACK_API_KEY
# Base: https://www.formstack.com/api/v2

# Typeform — use the default `typeform` skill in agent
# Required env: TYPEFORM_PERSONAL_TOKEN
# Base: https://api.typeform.com

# Tally (free)
# Required env: TALLY_API_KEY (paid feature) — for free tier use webhooks only

pip install requests
```

## Common recipes

### Recipe 1: Pick the platform

| Platform | Best for | Pricing (approx 2026) | Strengths | Watch out |
|---|---|---|---|---|
| Jotform | Broad form templates + e-sign + PDF auto-fill | Free → $99/mo | 10K+ templates; PDF designer included | UX feels older |
| Formstack | Enterprise + HIPAA | $50+/mo per user | HIPAA workspace; Salesforce-native | Pricier; complex setup |
| Typeform | Conversational UX | Free → $99/mo | Best response rate UX | One question at a time can be slow |
| Tally | Free / SMB | Free → $29/mo | Notion-style; unlimited fields free | Less integrations |
| Google Forms | Internal / quick | Free | Free + GSuite integrated | No conditional logic; clunky for clients |
| Microsoft Forms | Internal Microsoft shops | Free w/ M365 | Native to M365 | Same limits as Google Forms |

Default for client-facing intake: Jotform. For HIPAA: Formstack. For conversion-optimized: Typeform. For free + design-first: Tally.

### Recipe 2: Jotform — create a form via API

```bash
curl -X POST "https://api.jotform.com/form?apiKey=$JOTFORM_API_KEY" \
  -d "properties[title]=Client Onboarding" \
  -d "properties[height]=600" \
  -d "questions[1][type]=control_textbox" \
  -d "questions[1][text]=Company name" \
  -d "questions[1][required]=Yes" \
  -d "questions[1][order]=1" \
  -d "questions[2][type]=control_email" \
  -d "questions[2][text]=Email" \
  -d "questions[2][required]=Yes" \
  -d "questions[2][order]=2"
```

Most teams build the form in Jotform UI; use the API for read + conditional-logic mass updates.

### Recipe 3: Jotform — fetch submissions

```bash
# List all submissions of a form
curl "https://api.jotform.com/form/$FORM_ID/submissions?apiKey=$JOTFORM_API_KEY&limit=100" | jq '.content'

# Get a single submission
curl "https://api.jotform.com/submission/$SUBMISSION_ID?apiKey=$JOTFORM_API_KEY"
```

Each submission has `answers` keyed by question ID — flatten for downstream use.

### Recipe 4: Jotform — webhook on submission

```bash
# Add webhook to form
curl -X POST "https://api.jotform.com/form/$FORM_ID/webhooks?apiKey=$JOTFORM_API_KEY" \
  -d "webhookURL=https://your-app/webhooks/jotform"
```

Webhook payload includes `formID`, `submissionID`, `rawRequest` (JSON-encoded answers).

### Recipe 5: Jotform — auto-fill PDF on submission

In Jotform → Form Builder → PDF Editor: attach a PDF template, drag form fields onto positions. On submission, Jotform renders the PDF + emails / stores.

This is the simplest form-to-doc path; for richer logic use `conditional-logic-doc-assembly`.

### Recipe 6: Formstack — create form via API

```bash
curl -X POST https://www.formstack.com/api/v2/form.json \
  -H "Authorization: Bearer $FORMSTACK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Client Onboarding",
    "language": "en",
    "should_display_one_question_at_a_time": false,
    "fields": [
      {"field_type":"text","label":"Company name","required":true,"sort":1},
      {"field_type":"email","label":"Email","required":true,"sort":2}
    ]
  }'
```

### Recipe 7: Formstack — submissions + webhook

```bash
# Submissions
curl https://www.formstack.com/api/v2/form/$FORM_ID/submission.json \
  -H "Authorization: Bearer $FORMSTACK_API_KEY"

# Webhook
curl -X POST https://www.formstack.com/api/v2/webhook.json \
  -H "Authorization: Bearer $FORMSTACK_API_KEY" \
  -d 'form_id=$FORM_ID&url=https://your-app/webhooks/formstack'
```

### Recipe 8: Formstack HIPAA workspace

For HIPAA forms, set workspace to "HIPAA Workspace" in Formstack Admin → Workspace Settings; submissions encrypt at rest + transit; BAA executed by Formstack. Required for any form with PHI.

### Recipe 9: Typeform — create form via API

```bash
curl -X POST https://api.typeform.com/forms \
  -H "Authorization: Bearer $TYPEFORM_PERSONAL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Client Onboarding",
    "fields": [
      {"title":"What is your company name?","type":"short_text","ref":"company_name"},
      {"title":"What is your email?","type":"email","ref":"email"},
      {"title":"What entity type?","type":"multiple_choice","ref":"entity_type",
       "properties":{"choices":[{"label":"LLC"},{"label":"C-Corp"},{"label":"Other"}]}}
    ]
  }'
```

### Recipe 10: Typeform — webhook on submission

```bash
curl -X PUT https://api.typeform.com/forms/$FORM_ID/webhooks/main \
  -H "Authorization: Bearer $TYPEFORM_PERSONAL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url":"https://your-app/webhooks/typeform",
    "enabled":true,
    "secret":"shared-secret-here"
  }'
```

Validate `Typeform-Signature` HMAC header on inbound.

### Recipe 11: Tally — webhook

In Tally UI → Form → Settings → Integrations → Webhooks → add URL.
Tally payload includes `data.fields[]` array with `label`, `value`, `type`. Free tier supports up to 100 submissions/mo with webhooks.

### Recipe 12: Conditional logic — show/hide fields in Jotform

In Jotform Form Builder → Settings → Conditions → Add Condition:
- IF entity_type == "C-Corp" THEN show DUNS_number field
- IF deal_value > 50000 THEN show CFO_email field

Conditions live in Jotform; reading via API returns evaluated visible answers only.

### Recipe 13: Form → PandaDoc proposal chain

```python
@app.post("/webhooks/jotform")
async def jotform_to_pandadoc(req: Request):
    submission = await req.json()
    answers = parse_jotform_answers(submission["rawRequest"])
    # Recipe from hubspot-doc-gen / proposal-automation-pandadoc-proposify-qwilr
    pdoc = create_pandadoc(
        template_uuid=TEMPLATE_FOR[answers["service_type"]],
        recipient_email=answers["email"],
        tokens=[
            {"name":"customer.name","value":answers["company"]},
            {"name":"customer.state","value":answers["state"]},
        ]
    )
    return {"ok": True, "doc_id": pdoc["id"]}
```

### Recipe 14: Form → DocSpring custom PDF chain

```python
# When form data needs a custom-rendered PDF (non-PandaDoc)
@app.post("/webhooks/typeform")
async def typeform_to_docspring(req: Request):
    body = await req.json()
    answers = {f["field"]["ref"]: f["answer"]["text"] for f in body["form_response"]["answers"]}
    requests.post(
        f"https://api.docspring.com/api/v1/templates/{TEMPLATE_ID}/submissions",
        auth=(DOCSPRING_TOKEN, ""),
        json={"data": answers}
    )
```

### Recipe 15: Pre-fill via URL parameter

```text
https://form.jotform.com/F0RM1D?company={{Account.Name}}&email={{Contact.Email}}
```

Jotform / Typeform / Formstack all support URL parameters; useful for chained flows (CRM record → form pre-filled).

## Examples

### Example 1: Onboarding intake → MSA + DocuSign

**Goal:** New customer fills onboarding form; MSA auto-generated + sent for signature.
**Steps:**
1. Recipe 2 — Jotform onboarding form with conditional logic (Recipe 12).
2. Recipe 4 — webhook to your handler.
3. Recipe 13 — chain to PandaDoc OR `contract-template-authoring-msa-nda` + DocuSign.
4. `audit-trail-e-sign-versioning` archives the executed envelope.

**Result:** End-to-end zero-touch onboarding in <5 min from form submit.

### Example 2: HIPAA-compliant patient intake

**Goal:** Healthcare provider intakes patient PHI safely.
**Steps:**
1. Recipe 8 — Formstack HIPAA workspace.
2. Recipe 6 — fields for demographics + insurance.
3. Recipe 7 — webhook to HIPAA-eligible backend.
4. Auto-fill HHS BAA template + DocuSign for patient consent signature.

**Result:** HIPAA-compliant intake without sticky paper PHI.

### Example 3: Conversational lead intake → Notion DB + Slack notify

**Goal:** SaaS lead form; conversational UX; new leads land in Notion + ping AE on Slack.
**Steps:**
1. Recipe 9 — Typeform with 5-7 short questions.
2. Recipe 10 — webhook.
3. `notion-mcp` writes new row to Leads DB.
4. `slack-mcp` posts in #leads channel: "New lead: <company> via Typeform".

**Result:** Higher conversion (Typeform conversational UX) + zero manual lead entry.

## Edge cases / gotchas

- **Jotform `rawRequest` is a JSON string.** Always `json.loads(payload["rawRequest"])` before reading.
- **Jotform question IDs are sequential per form.** When you duplicate a form, IDs change; don't hardcode in handlers.
- **Webhook secret/signature support.** Jotform: HMAC of payload with shared secret; Typeform: `Typeform-Signature` header; Formstack: signature param. ALWAYS validate.
- **PHI in forms requires BAA.** Only Formstack HIPAA workspace + Jotform HIPAA tier (paid) are BAA-eligible. Don't send PHI through free tiers.
- **Conditional logic at form vs handler.** Form-level (Jotform Conditions) is easier; complex logic better in handler.
- **Pre-fill leak.** URL-prefilled email + name in screenshots can leak PII; use short tokens that resolve server-side.
- **Submission limit per plan.** Jotform Starter: 100/mo; Tally Free: 100/mo. Plan upgrades silently or surprise.
- **File uploads.** Jotform: 100MB; Formstack: 50MB; Typeform: 25MB. Larger files need S3 signed-URL upload from form widget.
- **Multi-language forms.** Typeform + Jotform support translations; Tally limited.
- **GDPR consent checkbox.** Required if collecting EU resident data; bake in checkbox + consent receipt.
- **Spam / bot submissions.** Enable reCAPTCHA / hCaptcha; high-traffic public forms get hammered.
- **Idempotency.** Webhooks may fire twice on network retry; dedupe by submissionID.
- **Data retention.** Jotform stores submissions on their cloud until you delete; for GDPR, periodic purge.
- **Locale-specific date format.** Form widget date picker may be MM/DD vs DD/MM by user locale; standardize ISO-8601 in handler.
- **CAPTCHA on embedded forms.** Embedded Typeforms can be CAPTCHA-bypassed if the embed is misconfigured; verify.

## Sources

- [Jotform API docs](https://api.jotform.com/docs/) — REST + webhooks + form structure.
- [Jotform PDF Editor](https://www.jotform.com/help/527-how-to-create-a-pdf-from-a-form-submission/) — auto-fill PDFs.
- [Formstack API v2](https://developers.formstack.com/reference/api-overview) — forms + submissions + HIPAA.
- [Typeform Developer](https://www.typeform.com/developers/) — Create API + Responses API + webhooks.
- [Tally API + webhooks](https://tally.so/help/api) — webhook payload + paid API.
- [Jotform HIPAA tier](https://www.jotform.com/hipaa-compliant-forms/) — BAA-eligible.
- [Formstack HIPAA](https://www.formstack.com/products/formstack-hipaa-forms) — HIPAA workspace.
- Sister skills: `conditional-logic-doc-assembly`, `e-signature-docusign-adobe-sign-pandadoc`, `redaction-automation-pii`, `document-workflow-routing-approval`.
