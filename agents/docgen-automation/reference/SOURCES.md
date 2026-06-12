# Document Automation — Source Attribution

This file maps every section of `soul.md` and `role.md` back to the research source(s) it was derived from. It is part of the bundle but is **not** loaded into the agent's context — it exists for human verification and future updates.

Upstream reference agents have not been downloaded in v1 (see `reference/INVENTORY.md`). Provenance is the SOTA web research summarized in `reference/SOTA_USE_CASES.md`. The "Notes on authored-from-synthesis" section below flags the small portions composed locally as operational glue.

---

## soul.md → source map

| Section in soul.md | Source(s) |
|---|---|
| Title + opening identity + load-bearing convictions | Authored from synthesis of the agent's per-agent prompt + `agent_bundle/METHODOLOGY.md` (load-bearing convictions pattern) |
| Purpose | Authored from synthesis informed by per-agent prompt's "one-line role" + the doc-automation operator survey in `reference/SOTA_USE_CASES.md` |
| Execution stack | `reference/SOTA_USE_CASES.md` (per-use-case skill-pack mapping) |
| When invoked — Template authoring mode | `reference/SOTA_USE_CASES.md` § "Contract template authoring" + Bonterms / Common Paper / Documate / HotDocs intro material |
| When invoked — Proposal automation mode | `reference/SOTA_USE_CASES.md` § "Proposal template authoring + automation" + PandaDoc / Proposify / Qwilr REST docs |
| When invoked — RFP response mode | `reference/SOTA_USE_CASES.md` § "RFP / RFI response automation" + Loopio / Responsive / Arphie material |
| When invoked — E-signature mode | `reference/SOTA_USE_CASES.md` § "E-signature workflow setup" + DocuSign / Adobe Sign / Dropbox Sign developer docs |
| When invoked — Smart form mode | `reference/SOTA_USE_CASES.md` § "Client onboarding form-to-doc workflows" + Jotform / Formstack / Typeform / Tally API docs |
| When invoked — Doc extraction (IDP) mode | `reference/SOTA_USE_CASES.md` § "AI doc extraction — IDP" + AWS Textract / Azure DI / Google Document AI / Hyperscience / Rossum docs |
| When invoked — Receipt / invoice extraction mode | `reference/SOTA_USE_CASES.md` § "Receipt / invoice extraction" + Veryfi / Mindee / Klippa / Nanonets docs |
| When invoked — CLM integration mode | `reference/SOTA_USE_CASES.md` § "CLM integration" + Ironclad / ContractWorks / LinkSquares / Evisort developer docs |
| When invoked — Bulk doc gen mode | `reference/SOTA_USE_CASES.md` § "Bulk document generation" + DocSpring / PDFmonkey / docxtemplater docs |
| When invoked — Redaction mode | `reference/SOTA_USE_CASES.md` § "Redaction automation" + Presidio / AWS Comprehend / Google DLP docs |
| When invoked — Accessibility mode | `reference/SOTA_USE_CASES.md` § "Document accessibility" + PDF/UA + WCAG 2.2 references |
| When invoked — Multilingual mode | `reference/SOTA_USE_CASES.md` § "Multilingual template generation" + DeepL / Lokalise / Crowdin docs |
| Core operating rules | Synthesis from the per-agent prompt's "CRITICAL HAND-OFF" lines + standard doc-automation operator hygiene (versioning, hashing, accessibility checks) |
| Mode-specific decisions | `reference/SOTA_USE_CASES.md` per-use-case rows + Templafy / DocuSign / PandaDoc enterprise vs SMB segmentation |
| Quality gates | Authored from synthesis of the per-agent prompt + accessibility / audit-trail / version-control best practices in the SOTA mapping |
| Output format | Authored from synthesis informed by docx / pdf / markdown-converter skill defaults |
| Communication style | Authored from synthesis aligned with the load-bearing conviction "ship doc-gen machinery, not opinions on binding effect" |
| When to push back | Synthesis from the agent's "defer binding-language to legal-counsel + pricing to finance-controller" hand-off rules |
| When to defer (sibling agents) | Per-agent prompt's defer rules + CraftBot agent catalog (`legal-counsel`, `finance-controller`, `sales-ops`, `l10n`, `compliance-agent`) |
| On first conversation (PROACTIVE init) | `METHODOLOGY.md` standard footer; the 3 routine questions tailored from the per-agent prompt (target platform, data source, e-sign requirement) |
| Closing rule | Authored from synthesis restating the three convictions |

---

## role.md → source map

| Section in role.md | Source(s) |
|---|---|
| Capability reference → Document types in scope | Aggregated from Common Paper + Bonterms + NVCA + Cooley GO + Stripe Atlas + Clerky template catalogs + HR / proposal / RFP / compliance doc surveys |
| Capability reference → Doc-automation platforms in scope | Aggregated from Documate / HotDocs / Docassemble / Templafy / Conga / PandaDoc / DocuSign / Loopio / Responsive / Ironclad / ContractWorks / LinkSquares product pages + G2 / Capterra category leaders 2026 |
| Capability reference → Template libraries to start from | Common Paper + Bonterms + YC + Cooley GO + Stripe Atlas + Clerky + NVCA + AICPA + EU Commission SCC + HHS BAA + AAA / JAMS |
| Capability reference → Compliance regimes for e-signature | ESIGN Act (15 USC §7001-7031) + UETA (uniformlaws.org) + eIDAS Regulation 910/2014 + eIDAS 2.0 (digital-strategy.ec.europa.eu) + 21 CFR Part 11 + HIPAA + state RON statutes |
| Capability reference → Pricing model in scope | Synthesis from PandaDoc / Proposify / Qwilr / CPQ literature on dynamic pricing |
| Contract template authoring playbook | Synthesis from Documate + HotDocs + Docassemble + Templafy + docxtemplater / python-docx-template documentation |
| Proposal automation playbook | PandaDoc developer docs + Proposify API guide + Qwilr API; CRM trigger patterns from PandaDoc + Salesforce + HubSpot integrations |
| RFP response playbook | Responsive (RFPIO) Public API + Loopio + Arphie product docs + RFP parsing patterns (`python-docx`, `openpyxl`, OCR fallbacks) |
| E-signature pipeline playbook | DocuSign eSignature REST + JWT + Connect docs + Adobe Sign Developer + Dropbox Sign (HelloSign) + SignNow + PandaDoc + Proof.com docs |
| E-sign compliance checklist | ESIGN Act + UETA + eIDAS + eIDAS 2.0 + 21 CFR Part 11 + HIPAA framing + state RON statute survey |
| IDP / doc extraction playbook | AWS Textract + Azure Document Intelligence + Google Document AI + Hyperscience + Rossum + Nanonets developer docs |
| Bulk doc gen playbook | DocSpring + PDFmonkey + docxtemplater + python-docx-template + WeasyPrint + Celery / BullMQ docs + AWS S3 best practices |
| Smart form deployment playbook | Jotform API + Formstack API + Typeform Developer + Tally help docs + HIPAA workspace notes for Formstack/Jotform |
| Redaction playbook | Microsoft Presidio + AWS Comprehend Detect-PII + AWS Comprehend Medical + Google DLP + HHS HIPAA Safe Harbor + Apryse / qpdf / mutool / exiftool |
| PDF/UA accessibility checklist | PDF/UA (ISO 14289) + WCAG 2.2 + Section 508 + EAA 2025 + EN 301 549 + Matterhorn Protocol + veraPDF + pa11y + axe-core |
| Multilingual templating playbook | DeepL Developer + Lokalise + Crowdin + Smartling + Babel locale-aware formatting + Toubon Law / EU Consumer Rights Directive context |
| CLM integration playbook | Ironclad Public API + ContractWorks + LinkSquares + Evisort + Lexion + Concord + Agiloft + SirionLabs developer docs |
| Salesforce Conga Composer | Conga Composer documentation + Conga Composer Direct REST + Conga Sign + Salesforce REST + CPQ Developer Guide |
| HubSpot doc gen | HubSpot CRM API v3 + HubSpot Quotes API + HubSpot Files API + PandaDoc HubSpot integration + DocSpring REST + DocuSign Gen for HubSpot |
| Audit trail recipe | DocuSign Certificate of Completion + Audit Events API + Adobe Sign / PandaDoc audit log + OpenTimestamps + AWS S3 Object Lock + eIDAS qualified time-stamping |
| Antipattern catalog | Composition synthesis informed by doc-automation operator forums + PandaDoc / DocuSign customer-failure case studies + the per-use-case caveats in `reference/SOTA_USE_CASES.md` |
| Reference templates | Composition from Bonterms / Common Paper / YC / NVCA / Cooley GO clause libraries adapted as authoring briefs |
| SOTA tool reference (June 2026) | `reference/SOTA_USE_CASES.md` + per-tool source URLs (cited in the SOTA sources table below) |
| SOTA execution playbook (which skill pack to reach for) | `reference/SOTA_USE_CASES.md` summary table |
| Brief templates / Output templates | Composition synthesis from PandaDoc / DocuSign / Conga production templates + audit-trail-e-sign-versioning manifest spec |
| Closing rules | Authored from synthesis restating soul.md convictions |

---

## Notes on authored-from-synthesis

Sections composed as operational glue rather than lifted verbatim:

- **Core operating rules (soul.md)** — composed locally from the per-agent prompt's hand-off rules + practical doc-automation operator hygiene (versioning, hashing, accessibility, audit trail). None of these are domain claims that lack underlying support.
- **When to push back / When to defer (soul.md)** — operational glue. Domain claims (binding language → legal-counsel; pricing → finance-controller; CPQ rules → sales-ops) come from the per-agent prompt's hand-off rules.
- **Antipattern catalog (role.md)** — composition synthesis from doc-automation operator forums, PandaDoc / DocuSign customer feedback patterns, and the caveats called out in `reference/SOTA_USE_CASES.md`. Each antipattern's underlying recipe / template is cited inline in the corresponding skill pack.
- **Reference templates (role.md)** — composed as deployable briefs aligned with the open template libraries (Common Paper / Bonterms / YC).
- **First-conversation routine questions (soul.md)** — adapted from the standard PROACTIVE.md self-init pattern in `METHODOLOGY.md`. The 3 role-specific questions are tailored to doc-automation workflows (target platform, data source, e-sign requirement).

These are operational glue, not domain claims. They do not introduce knowledge claims that lack a source.

---

## How to update this agent

If you want to refresh content from upstream:

1. Re-fetch the SOTA sources listed in the table below — many of these (DocuSign / PandaDoc / AWS Textract / Azure DI / Google Document AI / Ironclad release notes; ISO / W3C / EU regulator pages) update quarterly or on major regulatory event.
2. Diff against the previous versions to see what changed.
3. Update the corresponding sections of `soul.md`, `role.md`, and `reference/SOTA_USE_CASES.md`.
4. Update this `SOURCES.md` if section names or source URLs changed.
5. Re-run `python verify.py docgen-automation` to confirm structure intact.
6. Re-run `python build.py docgen-automation` to regenerate `dist/docgen-automation.craftbot`.

The bundled skill packs (in `skills/`) cite tool-specific sources independently inside each `SKILL.md`.

---

## SOTA tool sources (June 2026)

| Tool / framework | Source URL | Used in |
|---|---|---|
| Documate | https://documate.org/ | `skills/contract-template-authoring-msa-nda` + `skills/conditional-logic-doc-assembly` |
| HotDocs | https://www.hotdocs.com/ | `skills/contract-template-authoring-msa-nda` + `skills/conditional-logic-doc-assembly` |
| Docassemble | https://docassemble.org/ | `skills/conditional-logic-doc-assembly` |
| Templafy | https://www.templafy.com/ | `skills/template-library-templafy-brand` |
| Brandfolder | https://brandfolder.com/ | `skills/template-library-templafy-brand` |
| Frontify | https://www.frontify.com/ | `skills/template-library-templafy-brand` |
| Common Paper | https://commonpaper.com/standards/ | `skills/contract-template-authoring-msa-nda` |
| Bonterms | https://bonterms.com/ | `skills/contract-template-authoring-msa-nda` |
| Y Combinator SAFE templates | https://www.ycombinator.com/documents | `skills/contract-template-authoring-msa-nda` |
| Cooley GO Documents | https://www.cooleygo.com/documents/ | `skills/contract-template-authoring-msa-nda` |
| NVCA Model Legal Documents | https://nvca.org/model-legal-documents/ | `skills/contract-template-authoring-msa-nda` |
| Stripe Atlas | https://stripe.com/atlas | `skills/contract-template-authoring-msa-nda` |
| Clerky | https://www.clerky.com/ | `skills/contract-template-authoring-msa-nda` |
| PandaDoc Developer Docs | https://developers.pandadoc.com/ | `skills/proposal-automation-pandadoc-proposify-qwilr` + `skills/e-signature-docusign-adobe-sign-pandadoc` + `skills/hubspot-doc-gen` + `skills/dynamic-pricing-variable-insertion` |
| Proposify API | https://help.proposify.com/en/articles/5398128-api-getting-started | `skills/proposal-automation-pandadoc-proposify-qwilr` + `skills/dynamic-pricing-variable-insertion` |
| Qwilr API | https://qwilr.com/ | `skills/proposal-automation-pandadoc-proposify-qwilr` + `skills/dynamic-pricing-variable-insertion` |
| Loopio | https://www.loopio.com/ | `skills/rfp-response-loopio-rfpio-responsive` |
| Responsive (formerly RFPIO) | https://www.responsive.io/api-documentation | `skills/rfp-response-loopio-rfpio-responsive` |
| Arphie | https://www.arphie.ai/ | `skills/rfp-response-loopio-rfpio-responsive` |
| DocuSign eSignature REST API | https://developers.docusign.com/docs/esign-rest-api/ | `skills/e-signature-docusign-adobe-sign-pandadoc` + `skills/audit-trail-e-sign-versioning` + `skills/document-workflow-routing-approval` + `skills/document-analytics-time-to-sign` |
| DocuSign Connect (webhooks) | https://developers.docusign.com/platform/webhooks/connect/ | `skills/e-signature-docusign-adobe-sign-pandadoc` + `skills/document-analytics-time-to-sign` + `skills/audit-trail-e-sign-versioning` |
| DocuSign JWT Grant | https://developers.docusign.com/platform/auth/jwt/ | `skills/e-signature-docusign-adobe-sign-pandadoc` |
| Adobe Sign (Acrobat Sign) Developer | https://developer.adobe.com/document-services/apis/sign-api/ | `skills/e-signature-docusign-adobe-sign-pandadoc` + `skills/audit-trail-e-sign-versioning` |
| Dropbox Sign (HelloSign) Developer | https://developers.hellosign.com/ | `skills/e-signature-docusign-adobe-sign-pandadoc` |
| SignNow API | https://docs.signnow.com/docs/signnow/welcome | `skills/e-signature-docusign-adobe-sign-pandadoc` |
| Proof.com (formerly Notarize.com) | https://www.proof.com/ | `skills/e-signature-docusign-adobe-sign-pandadoc` (RON section) |
| ESIGN Act (15 USC §7001-7031) | https://www.law.cornell.edu/uscode/text/15/chapter-96 | `skills/e-sign-compliance-ueta-esign-eidas` |
| UETA (Uniform Electronic Transactions Act) | https://www.uniformlaws.org/ | `skills/e-sign-compliance-ueta-esign-eidas` |
| eIDAS Regulation 910/2014 + eIDAS 2.0 | https://digital-strategy.ec.europa.eu/en/policies/eidas-regulation | `skills/e-sign-compliance-ueta-esign-eidas` |
| 21 CFR Part 11 | https://www.fda.gov/regulatory-information/search-fda-guidance-documents/part-11-electronic-records-electronic-signatures-scope-and-application | `skills/e-sign-compliance-ueta-esign-eidas` + `skills/audit-trail-e-sign-versioning` |
| Hyperscience | https://hyperscience.ai/ | `skills/ai-doc-extraction-hyperscience-rossum-textract` |
| Rossum | https://rossum.ai/ | `skills/ai-doc-extraction-hyperscience-rossum-textract` |
| AWS Textract | https://aws.amazon.com/textract/ | `skills/ai-doc-extraction-hyperscience-rossum-textract` + `skills/ocr-paper-doc-extraction` |
| Azure Document Intelligence (Form Recognizer) | https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/ | `skills/ai-doc-extraction-hyperscience-rossum-textract` + `skills/ocr-paper-doc-extraction` |
| Google Document AI | https://cloud.google.com/document-ai | `skills/ai-doc-extraction-hyperscience-rossum-textract` + `skills/ocr-paper-doc-extraction` |
| Veryfi | https://docs.veryfi.com/ | `skills/receipt-invoice-extraction-veryfi-mindee` |
| Mindee | https://developers.mindee.com/ | `skills/receipt-invoice-extraction-veryfi-mindee` |
| Klippa | https://www.klippa.com/en/api/dochorizon/ | `skills/receipt-invoice-extraction-veryfi-mindee` |
| Nanonets | https://nanonets.com/api-docs/ | `skills/receipt-invoice-extraction-veryfi-mindee` |
| Ironclad Public API | https://developer.ironcladapp.com/ | `skills/clm-ironclad-contractworks-integration` |
| ContractWorks | https://www.contractworks.com/ | `skills/clm-ironclad-contractworks-integration` |
| Lexion (DocuSign) | https://www.lexion.ai/ | `skills/clm-ironclad-contractworks-integration` |
| LinkSquares | https://www.linksquares.com/ | `skills/clm-ironclad-contractworks-integration` + `skills/ai-summarization-clause-extraction` |
| Evisort | https://www.evisort.com/ | `skills/clm-ironclad-contractworks-integration` + `skills/ai-summarization-clause-extraction` |
| Concord | https://www.concord.app/ | `skills/clm-ironclad-contractworks-integration` |
| Agiloft | https://www.agiloft.com/ | `skills/clm-ironclad-contractworks-integration` |
| SirionLabs | https://www.sirion.ai/ | `skills/clm-ironclad-contractworks-integration` |
| Conga Composer | https://documentation.conga.com/composer | `skills/salesforce-conga-composer` |
| Conga Sign | https://documentation.conga.com/sign | `skills/salesforce-conga-composer` |
| Salesforce REST API | https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/ | `skills/salesforce-conga-composer` |
| Salesforce CPQ Developer Guide | https://developer.salesforce.com/docs/atlas.en-us.cpq_dev_api.meta/cpq_dev_api/ | `skills/salesforce-conga-composer` + `skills/dynamic-pricing-variable-insertion` |
| S-Docs | https://www.sdocs.com/ | `skills/salesforce-conga-composer` |
| Nintex DocGen | https://www.nintex.com/process-platform/document-generation/ | `skills/salesforce-conga-composer` |
| DocuSign Gen for Salesforce | https://www.docusign.com/products/gen-salesforce | `skills/salesforce-conga-composer` |
| HubSpot CRM API v3 | https://developers.hubspot.com/docs/api/crm/understanding-the-crm | `skills/hubspot-doc-gen` |
| HubSpot Quotes API | https://developers.hubspot.com/docs/api/crm/quotes | `skills/hubspot-doc-gen` |
| HubSpot Files API | https://developers.hubspot.com/docs/api/files/files | `skills/hubspot-doc-gen` |
| HubSpot Workflows | https://knowledge.hubspot.com/workflows/ | `skills/hubspot-doc-gen` |
| PandaDoc + HubSpot integration | https://www.pandadoc.com/integrations/hubspot/ | `skills/hubspot-doc-gen` |
| DocSpring API | https://docspring.com/docs/api/ | `skills/bulk-document-gen-csv` + `skills/hubspot-doc-gen` |
| PDFmonkey API | https://www.pdfmonkey.io/api-docs | `skills/bulk-document-gen-csv` |
| Anvil PDF | https://www.useanvil.com/docs/api/ | `skills/bulk-document-gen-csv` |
| Carbone.io | https://carbone.io/api-reference.html | `skills/bulk-document-gen-csv` |
| docxtemplater (Node) | https://docxtemplater.com/ | `skills/contract-template-authoring-msa-nda` + `skills/bulk-document-gen-csv` + `skills/template-library-templafy-brand` |
| docxtpl (Python) | https://docxtpl.readthedocs.io/ | `skills/contract-template-authoring-msa-nda` + `skills/bulk-document-gen-csv` + `skills/dynamic-pricing-variable-insertion` |
| python-docx | https://python-docx.readthedocs.io/ | `skills/template-library-templafy-brand` + `skills/contract-redlining-automation` + `skills/redaction-automation-pii` |
| python-pptx | https://python-pptx.readthedocs.io/ | `skills/template-library-templafy-brand` |
| WeasyPrint | https://doc.courtbouillon.org/weasyprint/ | `skills/bulk-document-gen-csv` + `skills/dynamic-pricing-variable-insertion` + `skills/document-accessibility-pdf-ua` |
| Pandoc | https://pandoc.org/MANUAL.html | `skills/document-accessibility-pdf-ua` + `skills/contract-template-authoring-msa-nda` |
| PrinceXML | https://www.princexml.com/ | `skills/contract-template-authoring-msa-nda` + `skills/bulk-document-gen-csv` |
| LibreOffice headless | https://www.libreoffice.org/ | `skills/bulk-document-gen-csv` + `skills/document-accessibility-pdf-ua` |
| Celery + Redis | https://docs.celeryq.dev/ | `skills/bulk-document-gen-csv` |
| BullMQ + Redis | https://docs.bullmq.io/ | `skills/bulk-document-gen-csv` |
| SendGrid v3 API | https://docs.sendgrid.com/api-reference/mail-send/mail-send | `skills/bulk-document-gen-csv` + `skills/document-workflow-routing-approval` |
| Postmark API | https://postmarkapp.com/developer | `skills/bulk-document-gen-csv` |
| AWS S3 presign + Object Lock | https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-overview.html | `skills/bulk-document-gen-csv` + `skills/audit-trail-e-sign-versioning` |
| DocuSign Bulk Send | https://developers.docusign.com/docs/esign-rest-api/how-to/send-bulk-envelopes/ | `skills/bulk-document-gen-csv` |
| Jotform API | https://api.jotform.com/docs/ | `skills/smart-form-jotform-formstack` |
| Formstack API v2 | https://developers.formstack.com/reference/api-overview | `skills/smart-form-jotform-formstack` |
| Typeform Developer | https://www.typeform.com/developers/ | `skills/smart-form-jotform-formstack` |
| Tally API + webhooks | https://tally.so/help/api | `skills/smart-form-jotform-formstack` |
| Microsoft Presidio | https://microsoft.github.io/presidio/ | `skills/redaction-automation-pii` |
| AWS Comprehend Detect-PII | https://docs.aws.amazon.com/comprehend/latest/dg/how-pii.html | `skills/redaction-automation-pii` |
| AWS Comprehend Medical Detect-PHI | https://docs.aws.amazon.com/comprehend-medical/latest/dev/textanalysis-phi.html | `skills/redaction-automation-pii` |
| Google Cloud DLP | https://cloud.google.com/dlp/docs | `skills/redaction-automation-pii` |
| Azure AI Language PII | https://learn.microsoft.com/en-us/azure/ai-services/language-service/personally-identifiable-information/overview | `skills/redaction-automation-pii` |
| HHS HIPAA Safe Harbor (18 identifiers) | https://www.hhs.gov/hipaa/for-professionals/special-topics/de-identification/index.html | `skills/redaction-automation-pii` |
| Apryse / PDFTron Redaction SDK | https://apryse.com/products/sdk/redaction | `skills/redaction-automation-pii` |
| qpdf | https://qpdf.readthedocs.io/ | `skills/redaction-automation-pii` |
| mutool (MuPDF) | https://mupdf.com/docs/manual-mutool-clean.html | `skills/redaction-automation-pii` |
| exiftool | https://exiftool.org/ | `skills/redaction-automation-pii` |
| PDF/UA — ISO 14289 | https://www.pdfa.org/resource/iso-14289/ | `skills/document-accessibility-pdf-ua` |
| veraPDF | https://docs.verapdf.org/ | `skills/document-accessibility-pdf-ua` |
| PAC 2024 (PDF Accessibility Checker) | https://pac.pdf-accessibility.org/ | `skills/document-accessibility-pdf-ua` |
| Matterhorn Protocol | https://www.pdfa.org/resource/the-matterhorn-protocol-2-0/ | `skills/document-accessibility-pdf-ua` |
| WCAG 2.2 quickref | https://www.w3.org/WAI/WCAG22/quickref/ | `skills/document-accessibility-pdf-ua` |
| Section 508 standards | https://www.section508.gov/ | `skills/document-accessibility-pdf-ua` |
| EAA 2025 | https://ec.europa.eu/social/main.jsp?catId=1202 | `skills/document-accessibility-pdf-ua` |
| EN 301 549 | https://www.etsi.org/standards#page=1&search=EN%20301%20549 | `skills/document-accessibility-pdf-ua` |
| Adobe Acrobat Accessibility | https://www.adobe.com/accessibility/pdf/pdf-accessibility-overview.html | `skills/document-accessibility-pdf-ua` |
| pa11y | https://pa11y.org/ | `skills/document-accessibility-pdf-ua` |
| axe-core | https://github.com/dequelabs/axe-core | `skills/document-accessibility-pdf-ua` |
| pikepdf | https://pikepdf.readthedocs.io/ | `skills/document-accessibility-pdf-ua` + `skills/multilingual-template-generation` |
| Tesseract OCR | https://github.com/tesseract-ocr/tesseract | `skills/ocr-paper-doc-extraction` |
| PaddleOCR | https://github.com/PaddlePaddle/PaddleOCR | `skills/ocr-paper-doc-extraction` |
| EasyOCR | https://github.com/JaidedAI/EasyOCR | `skills/ocr-paper-doc-extraction` |
| Surya OCR | https://github.com/VikParuchuri/surya | `skills/ocr-paper-doc-extraction` |
| olmOCR (AllenAI) | https://allenai.org/blog/olmocr | `skills/ocr-paper-doc-extraction` |
| GOT-OCR2.0 | https://github.com/Ucas-HaoranWei/GOT-OCR2.0 | `skills/ocr-paper-doc-extraction` |
| ocrmypdf | https://ocrmypdf.readthedocs.io/ | `skills/ocr-paper-doc-extraction` |
| pdf2image | https://github.com/Belval/pdf2image | `skills/ocr-paper-doc-extraction` |
| Anthropic Claude docs | https://docs.anthropic.com/ | `skills/ai-summarization-clause-extraction` |
| Google Gemini docs | https://ai.google.dev/docs | `skills/ai-summarization-clause-extraction` |
| OpenAI structured outputs | https://platform.openai.com/docs/guides/structured-outputs | `skills/ai-summarization-clause-extraction` |
| spaCy NER | https://spacy.io/usage/linguistic-features | `skills/ai-summarization-clause-extraction` + `skills/redaction-automation-pii` |
| tiktoken | https://github.com/openai/tiktoken | `skills/ai-summarization-clause-extraction` |
| Spellbook | https://www.spellbook.legal/ | `skills/contract-redlining-automation` |
| Robin AI | https://www.robinai.com/ | `skills/contract-redlining-automation` + `skills/ai-summarization-clause-extraction` |
| Harvey AI | https://www.harvey.ai/ | `skills/contract-redlining-automation` |
| DraftWise | https://draftwise.com/ | `skills/contract-redlining-automation` |
| Ironclad AI Assist | https://ironcladapp.com/products/ai/ | `skills/contract-redlining-automation` + `skills/ai-summarization-clause-extraction` |
| LegalOn | https://www.legalontech.com/ | `skills/contract-redlining-automation` |
| redlines (Python lib) | https://github.com/MaxHumber/redlines | `skills/contract-redlining-automation` |
| diff-match-patch (Google) | https://github.com/google/diff-match-patch | `skills/contract-redlining-automation` |
| OOXML / docx schema | https://learn.microsoft.com/en-us/openspecs/office_standards/ms-docx/ | `skills/contract-redlining-automation` + `skills/template-library-templafy-brand` |
| Vale (prose linter) | https://vale.sh/ | `skills/template-library-templafy-brand` |
| Vale Action for GitHub | https://github.com/errata-ai/vale-action | `skills/template-library-templafy-brand` |
| Acrolinx | https://www.acrolinx.com/ | `skills/template-library-templafy-brand` |
| n8n | https://docs.n8n.io/ | `skills/document-workflow-routing-approval` |
| Zapier Platform | https://platform.zapier.com/docs/welcome | `skills/document-workflow-routing-approval` |
| Make.com | https://www.make.com/en/help | `skills/document-workflow-routing-approval` |
| Slack Block Kit | https://api.slack.com/block-kit | `skills/document-workflow-routing-approval` |
| Slack Interactivity | https://api.slack.com/interactivity/handling | `skills/document-workflow-routing-approval` |
| Microsoft Teams Adaptive Cards | https://learn.microsoft.com/en-us/microsoftteams/platform/task-modules-and-cards/cards/cards-reference | `skills/document-workflow-routing-approval` |
| Linear API | https://developers.linear.app/docs | `skills/document-workflow-routing-approval` |
| PandaDoc Approval workflow | https://support.pandadoc.com/hc/en-us/articles/360011425933-Approval-Workflow | `skills/document-workflow-routing-approval` |
| OpenTimestamps | https://opentimestamps.org/ | `skills/audit-trail-e-sign-versioning` |
| Sectigo Qualified Time-Stamping | https://sectigo.com/resource-library/what-is-a-qualified-timestamp | `skills/audit-trail-e-sign-versioning` |
| DeepL Translate API | https://developers.deepl.com/docs/api-reference/translate | `skills/multilingual-template-generation` |
| DeepL Python SDK | https://github.com/DeepLcom/deepl-python | `skills/multilingual-template-generation` |
| Google Cloud Translate | https://cloud.google.com/translate/docs | `skills/multilingual-template-generation` |
| Microsoft Azure AI Translator | https://learn.microsoft.com/en-us/azure/ai-services/translator/ | `skills/multilingual-template-generation` |
| Amazon Translate | https://docs.aws.amazon.com/translate/ | `skills/multilingual-template-generation` |
| Lokalise API | https://developers.lokalise.com/reference/lokalise-rest-api | `skills/multilingual-template-generation` |
| Crowdin API | https://developer.crowdin.com/api/v2/ | `skills/multilingual-template-generation` |
| Smartling docs | https://help.smartling.com/ | `skills/multilingual-template-generation` |
| Phrase docs | https://developers.phrase.com/ | `skills/multilingual-template-generation` |
| Babel — Currency / date formatting | https://babel.pocoo.org/en/latest/ | `skills/multilingual-template-generation` + `skills/dynamic-pricing-variable-insertion` |
| QuickBooks Online API — Bill | https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/bill | `skills/receipt-invoice-extraction-veryfi-mindee` |
| NetSuite Expense Reports REST | https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_158156965962.html | `skills/receipt-invoice-extraction-veryfi-mindee` |
| Stripe Prices API | https://stripe.com/docs/api/prices | `skills/dynamic-pricing-variable-insertion` |
| PostHog Python SDK | https://posthog.com/docs/libraries/python | `skills/document-analytics-time-to-sign` |
| Mixpanel Python | https://developer.mixpanel.com/docs/python | `skills/document-analytics-time-to-sign` |
| Amplitude Python SDK | https://www.docs.developers.amplitude.com/data/sdks/python/ | `skills/document-analytics-time-to-sign` |
| Streamlit | https://docs.streamlit.io/ | `skills/document-analytics-time-to-sign` |
| Plotly funnel charts | https://plotly.com/python/funnel-charts/ | `skills/document-analytics-time-to-sign` |

---

These sources informed the `SOTA tool reference (June 2026)` section in `role.md`, the per-use-case mapping in `reference/SOTA_USE_CASES.md`, and the bundled SOTA skill packs (Round 2 created the SKILL.md content; see each skill's "Sources" section for the per-recipe URLs).
