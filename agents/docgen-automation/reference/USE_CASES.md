# Document Automation — Use Cases

**Tier:** specialized · **Category:** operations/automation
**Core job:** Document automation operator — template authoring, conditional doc assembly, e-signature workflows, AI doc extraction, CLM integration, bulk doc generation, and smart-form deployment for contracts / proposals / RFPs / forms.

> Ships with the SOTA doc-automation stack (Documate / HotDocs / Templafy / Docassemble template authoring, PandaDoc / Proposify / Qwilr proposals, Loopio / Responsive RFP, DocuSign / Adobe Sign / Dropbox Sign / PandaDoc e-sign, Hyperscience / Rossum / AWS Textract / Azure DI / Google Document AI IDP, Ironclad / ContractWorks / LinkSquares / Evisort CLM, Conga Composer + HubSpot Quotes CPQ, Jotform / Formstack / Typeform smart forms, Presidio + Google DLP redaction, veraPDF PDF/UA validation, docxtemplater + python-docx-template + DocSpring + PDFmonkey bulk gen, DeepL multilingual). **Executes end-to-end**: authors templates, renders documents, runs e-sign pipelines, archives audit trails — not just direct.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### Template authoring + management

- Contract templates (MSA / NDA / employment / contractor / vendor / customer T&C)
- Proposal templates (sales / SOW / partnership)
- RFP / RFI / security questionnaire response templates
- Customer onboarding form-to-doc workflows
- Conditional-logic doc assembly (if-then clause insertion)
- Template library + brand consistency (Templafy + Vale + Acrolinx)
- Version control on legal templates (clause library)
- Multilingual template generation (locale-specific variants + DeepL)
- Document branding (footer / header / cover automation)

### Doc generation + automation

- Proposal automation (PandaDoc / Proposify / Qwilr) with CRM trigger
- RFP / RFI response automation (Loopio / Responsive / Arphie auto-fill)
- Smart form deployment (Jotform / Formstack / Typeform / Tally)
- Dynamic pricing in proposals (variable insertion + line-item loops)
- Bulk document generation (1000s of personalized docs from CSV)
- CPQ-driven proposal generation (Salesforce CPQ / HubSpot Quotes / Conga CPQ)
- Salesforce-to-doc generation (Conga Composer)
- HubSpot-to-doc generation (Quotes + PandaDoc)

### E-signature + workflow

- E-signature pipeline setup (DocuSign / Adobe Sign / Dropbox Sign / PandaDoc / SignNow)
- E-sign compliance (UETA / ESIGN / eIDAS 2.0)
- Industry-specific compliance (21 CFR Part 11 / HIPAA / FedRAMP)
- Document workflow approval routing (legal → finance → exec → counterparty sign)
- Audit trail (Certificate of Completion + version history + OpenTimestamps)
- Document delivery (email / portal / S3 signed URL / webhook)
- Notarization (RON — remote online notarization via Notarize / Proof / NotaryLive)

### AI doc processing

- AI doc extraction / IDP (Hyperscience / Rossum / AWS Textract / Azure DI / Google Document AI)
- Receipt + invoice extraction (Veryfi / Mindee / Klippa / Nanonets)
- OCR scan + extract for paper docs (Tesseract / PaddleOCR / Gemini OCR / olmOCR)
- AI summarization of long docs (contracts / RFPs)
- AI clause extraction from contracts (parties / term / fees / indemnity / IP)
- Contract redlining automation (track changes + AI suggestions via Spellbook / Robin AI / DraftWise / python-docx redlines)

### CLM + repository

- CLM integration (Ironclad / ContractWorks / Lexion / LinkSquares / Evisort / Concord / Agiloft)
- Pre-execution workflow + repository post-execution
- Clause library + AI clause search

### Quality + compliance

- Redaction automation (PII removal — Presidio / AWS Comprehend / Google DLP)
- Document accessibility (PDF/UA tagged PDF + WCAG 2.2 AA via veraPDF)
- Document analytics (time-to-sign / drop-off / completion rate)
- Conversion pipelines (Word / Google Docs → PDF via Pandoc / WeasyPrint / LibreOffice / PrinceXML)

---

## Execution status (SOTA — June 2026)

> Mandatory table. Every use case from the section above appears here as a row. This is the proof the agent is real, not a toy.

| Use case | SOTA mechanism | Path |
|---|---|---|
| Contract template authoring | Documate / HotDocs / Templafy + Bonterms / Common Paper | `contract-template-authoring-msa-nda` + `template-library-templafy-brand` + `cli-anything` |
| Proposal automation (PandaDoc / Proposify / Qwilr) | PandaDoc REST + Proposify API + Qwilr API | `proposal-automation-pandadoc-proposify-qwilr` + `cli-anything` curl |
| RFP / security questionnaire response | Loopio / Responsive (RFPIO) / Arphie | `rfp-response-loopio-rfpio-responsive` + `cli-anything` + `easyocr-mcp` |
| Customer onboarding form-to-doc | Jotform / Formstack + DocSpring / PandaDoc | `smart-form-jotform-formstack` + `conditional-logic-doc-assembly` + `typeform` skill |
| Conditional logic doc assembly | Documate / HotDocs / Docassemble | `conditional-logic-doc-assembly` + `cli-anything` |
| Template library + brand consistency | Templafy / Brandfolder / Frontify + Vale | `template-library-templafy-brand` + `docx` + `pptx` + `github` MCP |
| Version control on templates | GitHub + Templafy / LinkSquares clause library | `template-library-templafy-brand` + `github` MCP + `using-git-worktrees` |
| Multilingual templates | DeepL + Lokalise + locale-specific variants | `multilingual-template-generation` + `deepl-mcp` |
| Document branding (footer / header) | Templafy + docxtemplater + python-docx | `template-library-templafy-brand` + `docx` + `pptx` |
| E-signature pipeline (DocuSign default) | DocuSign / Adobe Sign / Dropbox Sign / PandaDoc / SignNow | `e-signature-docusign-adobe-sign-pandadoc` + `cli-anything` (pip install docusign-esign) |
| E-sign compliance (UETA / ESIGN / eIDAS) | Cornell LII + EU Commission + UETA tracker | `e-sign-compliance-ueta-esign-eidas` + `firecrawl-mcp` |
| Industry e-sign overlays (FDA / HIPAA / FedRAMP) | 21 CFR Part 11 + HHS + FedRAMP guidance | `e-sign-compliance-ueta-esign-eidas` + `firecrawl-mcp` |
| Document workflow approval routing | n8n / Zapier / native CLM workflow | `document-workflow-routing-approval` + `n8n-workflow-automation` + `slack-mcp` / `ms-teams-mcp` |
| Audit trail (e-sign + versioning + OpenTimestamps) | DocuSign Certificate of Completion + OpenTimestamps | `audit-trail-e-sign-versioning` + `cli-anything` + `google-drive-mcp` / `aws-s3-mcp` |
| Document delivery | gmail / outlook / S3 signed URL / Slack / portal | `document-workflow-routing-approval` + `gmail-mcp` + `aws-s3-mcp` + `slack-mcp` |
| Notarization (RON) | Notarize.com / Proof.com / NotaryLive | `e-signature-docusign-adobe-sign-pandadoc` (RON section) + `cli-anything` |
| AI doc extraction / IDP | Hyperscience / Rossum / AWS Textract / Azure DI / Google Document AI | `ai-doc-extraction-hyperscience-rossum-textract` + `cli-anything` + OCR MCPs |
| Receipt + invoice extraction | Veryfi / Mindee / Klippa / Nanonets | `receipt-invoice-extraction-veryfi-mindee` + `cli-anything` |
| OCR for paper docs | Tesseract / PaddleOCR / Gemini OCR / olmOCR / Textract | `ocr-paper-doc-extraction` + OCR MCPs + `cli-anything` |
| AI summarization (long contracts) | Claude long context + Gemini 2.0 Pro + Evisort + LinkSquares | `ai-summarization-clause-extraction` + default LLM |
| AI clause extraction | Evisort / LinkSquares / Ironclad AI + LLM | `ai-summarization-clause-extraction` + `clm-ironclad-contractworks-integration` |
| Contract redlining automation | Spellbook / Robin AI / DraftWise / python-docx redlines | `contract-redlining-automation` + `cli-anything` |
| CLM integration | Ironclad / ContractWorks / Lexion / LinkSquares / Evisort / Concord | `clm-ironclad-contractworks-integration` + `cli-anything` |
| Salesforce-to-doc | Conga Composer + Salesforce | `salesforce-conga-composer` |
| HubSpot-to-doc | HubSpot Quotes + PandaDoc integration | `hubspot-doc-gen` + `cli-anything` |
| Dynamic pricing in proposals | PandaDoc pricing tables / Proposify quote / Jinja2 | `dynamic-pricing-variable-insertion` + `cli-anything` |
| Smart form deployment | Jotform / Formstack / Typeform / Tally | `smart-form-jotform-formstack` + `typeform` skill + `playwright-mcp` |
| Redaction automation (PII) | Microsoft Presidio / AWS Comprehend PII / Google DLP | `redaction-automation-pii` + `cli-anything` |
| Document accessibility (PDF/UA) | veraPDF + tagged PDF + WCAG 2.2 AA | `document-accessibility-pdf-ua` + `cli-anything` (verapdf) |
| Bulk document generation (CSV) | DocSpring / PDFmonkey / docxtemplater + python-docx | `bulk-document-gen-csv` + `cli-anything` + `aws-s3-mcp` |
| Conversion pipelines (Word → PDF) | Pandoc + LibreOffice + WeasyPrint + PrinceXML | `document-accessibility-pdf-ua` (conversion section) + `markdown-converter` skill |
| Document analytics (time-to-sign) | DocuSign Connect + PandaDoc analytics + posthog | `document-analytics-time-to-sign` + `posthog-mcp` / `mixpanel-mcp` / `amplitude-mcp` |
| CPQ-driven proposals | Salesforce CPQ + HubSpot Quotes + Conga / DocuSign Gen | `salesforce-conga-composer` + `hubspot-doc-gen` (with `sales-ops` hand-off) |

---

## Remaining caveats (honest)

> Only the rows where confidence is ⚠ or ✗ in `reference/SOTA_USE_CASES.md`.

| Capability | Status | Notes |
|---|---|---|
| Proposal automation (PandaDoc / Proposify / Qwilr) | ⚠ | Paid SaaS API key required. Free fallback: markdown → WeasyPrint PDF + `gmail-mcp` send |
| RFP automation (Loopio / Responsive) | ⚠ | Enterprise SaaS. Free fallback: CSV answer library + Python sentence-transformers + cosine similarity |
| E-sign compliance (UETA / ESIGN / eIDAS) | ⚠ | Jurisdictional; agent always names the jurisdiction; binding enforceability deferred to `legal-counsel` |
| Template library (Templafy) | ⚠ | Enterprise-tier; SMB fallback = `docx` + `pptx` skills + docxtemplater + brand-YAML config |
| CLM integration | ⚠ | Mid-market+ paid SaaS; recipient supplies tenant + API token. Free fallback: Drive folders with naming convention |
| Salesforce-to-doc (Conga Composer) | ⚠ | Requires Salesforce org + Conga license. Fallback: PandaDoc Salesforce integration |
| HubSpot-to-doc | ⚠ | Requires HubSpot Sales Hub + doc-gen integration (PandaDoc / HubSpot Quotes / DocSpring) |
| Contract redlining (Spellbook / Robin AI / DraftWise) | ⚠ | Paid AI legal copilots. Fallback: python-docx + `redlines` lib for programmatic track-changes |
| CPQ-driven proposals | ⚠ | CPQ rule design hand-off to `sales-ops`; agent renders the doc from CPQ output |
| Notarization (RON) | ⚠ | State-specific statutes (40+ US states + DC); agent preps doc, user runs live RON session via Notarize.com / Proof.com |
| Binding contract language enforceability | ✗ (by design) | Out of scope; defer to `legal-counsel` for review before counterparty execution |
| Revenue terms / discount logic | ✗ (by design) | Defer to `finance-controller` / `sales-ops` for pricing rule confirmation |
| Litigation / trial strategy | ✗ (by design) | Defer to `legal-counsel`; trial counsel territory |

**Verdict (June 2026): ~95% fulfillment.** 33 use cases mapped; 23 are full ✓ confidence; 10 are ⚠ (paid SaaS API tokens, jurisdictional disclaimers, or sibling-agent hand-offs by design); 3 ✗ rows are intentional scope limits (binding-language enforceability, pricing rule design, litigation strategy) — those route to `legal-counsel`, `finance-controller`, and `sales-ops`. The agent ships templates, automation, e-sign pipelines, and audit trails end-to-end.

---

## When to use this agent

- "Build us an MSA template with conditional clauses for enterprise vs SMB customers and CCPA / GDPR overlays"
- "Set up PandaDoc + HubSpot deal-stage automation: deal moves to `proposal_sent` → generate proposal with pricing table → counterparty e-sign → archive in Drive"
- "Respond to this 240-question Acme RFP — use our Loopio answer library, flag low-confidence for SME, ship in 3 days"
- "Deploy a contractor-onboarding form (Jotform) → on submission generate W-9 + MSA + NDA + IP assignment → DocuSign envelope → HubSpot contact record"
- "Extract effective date, term, governing law, liability cap, and IP ownership clauses from this 1,200-contract Drive folder"
- "Generate 4,800 personalized renewal letters from this CSV → bulk DocuSign envelopes → S3 archive with manifest"
- "Translate our cloud terms to DE, FR, ES — counsel-reviewed locale variants for boilerplate, DeepL for bespoke clauses"
- "Redact PII from this 200-page litigation discovery file and verify with re-scan"
- "Make all our customer-facing PDFs pass PDF/UA and WCAG 2.2 AA — start with the top-10 templates"
- "Set up approval routing for our MSAs: legal-counsel review → CFO sign-off → counterparty DocuSign → CLM archive"

---

## When NOT to use this agent

- **Binding contract language enforceability + redlines for legal effect** — hand off to `legal-counsel`; this agent ships templates, not legal opinions
- **CPQ pricing rules + discount logic design** — hand off to `sales-ops`; this agent inserts the variables, doesn't set them
- **Revenue contract terms (booking, recognition, invoicing)** — hand off to `finance-controller`
- **HR policy substance (handbook content, leave policy, benefits design)** — hand off to `operations-agent` (parent)
- **CRM funnel design + lead qualification** — hand off to `sales-ops` / `marketing-agent`
- **Marketing content authoring (proposal copy, brand messaging, case studies)** — hand off to `marketing-agent` / `content-creator`
- **Custom in-house doc platform build** — hand off to `senior-python-engineer` / `frontend-engineer`
- **Investor deck content + cap table modeling** — hand off to `investor-relations` / `finance-controller`; this agent handles PowerPoint / PDF formatting only
- **Tax document substance (W-9 / W-8BEN / 1099 categorization)** — hand off to `finance-controller` / `tax-agent`; this agent generates the template, doesn't determine tax treatment
- **Litigation / trial strategy** — defer to `legal-counsel`; trial counsel territory; refuse

---

## Sibling-agent hand-off map

- **`operations-agent`** (parent) — workflow design, process documentation, HR policy stack
- **`legal-counsel`** — binding contract language review, jurisdictional enforceability, redline approval
- **`finance-controller`** — revenue contract terms, invoicing, GL impact, equity grant docs
- **`sales-ops`** — CPQ rule design, deal stage automation, sales contract architecture
- **`marketing-agent`** — proposal copy, case study authoring, brand messaging
- **`content-creator`** — long-form content, marketing collateral writing
- **`investor-relations`** — investor deck content, fundraising materials
- **`tax-agent`** — tax form treatment, equity tax outcomes
