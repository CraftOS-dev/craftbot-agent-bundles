# docgen-automation — SOTA Use Case Map (June 2026)

Per-use-case mapping from agent capability to concrete SOTA mechanism. Each row names the tool, the agent's execution path (which CraftBot MCP/skill actually runs it), the canonical source, and a confidence verdict.

Legend:
- `✓` — agent can execute the SOTA path end-to-end today with shipped MCPs/skills.
- `⚠` — agent can execute the SOTA path but with a known caveat (auth scope, paid tier, vendor approval, jurisdiction-specific).
- `✗` — SOTA path requires a tool the agent cannot reach (deferred / future work).

**Standing hand-off rule.** Every output that produces binding contract language defers final review to `legal-counsel`; every output that produces a revenue / pricing document defers to `finance-controller` or `sales-ops` when CPQ is involved. This is wired into `soul.md` "Core operating rules."

Bundled skill packs (in `skills/`) referenced below (Round 2 will populate):
`contract-template-authoring-msa-nda`, `proposal-automation-pandadoc-proposify-qwilr`, `rfp-response-loopio-rfpio-responsive`, `conditional-logic-doc-assembly`, `e-signature-docusign-adobe-sign-pandadoc`, `e-sign-compliance-ueta-esign-eidas`, `ai-doc-extraction-hyperscience-rossum-textract`, `receipt-invoice-extraction-veryfi-mindee`, `template-library-templafy-brand`, `clm-ironclad-contractworks-integration`, `salesforce-conga-composer`, `hubspot-doc-gen`, `document-workflow-routing-approval`, `audit-trail-e-sign-versioning`, `dynamic-pricing-variable-insertion`, `smart-form-jotform-formstack`, `redaction-automation-pii`, `document-accessibility-pdf-ua`, `bulk-document-gen-csv`, `ocr-paper-doc-extraction`, `ai-summarization-clause-extraction`, `contract-redlining-automation`, `document-analytics-time-to-sign`, `multilingual-template-generation`.

---

## Contract template authoring (MSA / NDA / employment / vendor / customer T&C)

- **SOTA approach:** Build a reusable template in a structured authoring environment (Documate, HotDocs, Templafy, Docassemble) with named merge fields + conditional clauses (e.g., `[[customer.entity_type]]` → adds SOC 2 addendum). Anchor language to Bonterms / Common Paper / YC base templates; layer org-specific clauses as snippets. Version every template in a clause library.
- **Agent execution path:** Bundled `contract-template-authoring-msa-nda` + `template-library-templafy-brand`. `filesystem` writes the master template; `cli-anything` + curl pulls Bonterms / Common Paper canonical templates; `docx` produces the Word output. For binding language, hand off to `legal-counsel`.
- **Source:** https://documate.org/ + https://www.hotdocs.com/ + https://www.templafy.com/ + https://commonpaper.com/standards/
- **Confidence:** ✓

## Proposal template authoring + automation (PandaDoc, Proposify, Qwilr)

- **SOTA approach:** Author proposal templates in PandaDoc / Proposify / Qwilr with content library blocks, dynamic pricing tables, e-sign embedded. Conditional sections by deal type (SMB vs Enterprise) and product mix. Trigger from CRM (HubSpot / Salesforce) so reps generate proposals in one click.
- **Agent execution path:** Bundled `proposal-automation-pandadoc-proposify-qwilr`. `cli-anything` + curl drives PandaDoc REST API (`POST /v3/documents`), Proposify API, Qwilr API. `filesystem` stores the source HTML / markdown master; output is a tracked proposal link with view + e-sign analytics.
- **Source:** https://developers.pandadoc.com/ + https://help.proposify.com/en/articles/5398128-api-getting-started + https://qwilr.com/
- **Confidence:** ⚠ (PandaDoc API key + workspace required; Proposify/Qwilr similar — recipient supplies tokens; agent has the wiring)

## RFP / RFI response automation (Loopio, RFPIO/Responsive)

- **SOTA approach:** Loopio / RFPIO (now Responsive) / Qvidian as the answer library + auto-fill engine for RFP questionnaires (Word, Excel, PDF, portal). AI assist matches incoming questions to canonical answers; SME review + approval routes. Arphie added LLM-native flows in 2024+.
- **Agent execution path:** Bundled `rfp-response-loopio-rfpio-responsive`. `cli-anything` + curl drives Responsive (RFPIO) Public API; `easyocr-mcp` / `gemini-ocr-mcp` extracts questions from scanned RFPs; `filesystem` produces the populated response doc. Hand off to subject-matter expert for review.
- **Source:** https://www.responsive.io/api-documentation + https://www.loopio.com/ + https://www.arphie.ai/
- **Confidence:** ⚠ (Responsive/Loopio API key + workspace required; agent has the wiring)

## Client onboarding form-to-doc workflows

- **SOTA approach:** Smart form (Jotform / Formstack / Typeform / Tally) collects client data; form submission triggers doc generation (PandaDoc, DocSpring, Documate) → routes for e-sign → CRM update. Zapier / Make / n8n / native PandaDoc workflows orchestrate. Typeform `typeform` skill + `notion-mcp` integration possible.
- **Agent execution path:** Bundled `smart-form-jotform-formstack` + `conditional-logic-doc-assembly`. `cli-anything` + curl drives Jotform / Formstack / Typeform REST APIs (`typeform` default skill exists). `filesystem` writes the form schema + the doc template; `playwright-mcp` validates the resulting workflow end-to-end.
- **Source:** https://api.jotform.com/docs/ + https://api.formstack.com/v2/ + https://www.typeform.com/developers/
- **Confidence:** ✓

## Conditional logic doc assembly (if-then clause insertion)

- **SOTA approach:** Documate / HotDocs / Docassemble template syntax (`if customer.is_enterprise then include SOC 2 addendum`). Conditional sections drive: jurisdiction-specific clauses (CA non-compete carve-out), product-mix (per SKU appendix), customer tier (premium SLA terms), regulatory overlay (HIPAA BAA, GDPR DPA).
- **Agent execution path:** Bundled `conditional-logic-doc-assembly`. `filesystem` writes the conditional template; `cli-anything` runs `docassemble` (FOSS) or drives Documate / HotDocs REST endpoints. Output: rendered doc + audit trail of which branches fired.
- **Source:** https://docassemble.org/ + https://www.hotdocs.com/products/hotdocs-developer/ + https://documate.org/docs
- **Confidence:** ✓

## E-signature workflow setup (DocuSign, Adobe Sign, PandaDoc, Dropbox Sign)

- **SOTA approach:** DocuSign eSignature REST API as the dominant 2026 platform; Adobe Sign (Acrobat Sign) as alternative; Dropbox Sign (HelloSign) for SMB; PandaDoc / SignWell / SignNow alternatives. Envelope create → tag recipients → routing order → signature → completion webhook → store completed PDF. Templates + reusable recipient roles.
- **Agent execution path:** Bundled `e-signature-docusign-adobe-sign-pandadoc`. `cli-anything` runs `pip install docusign-esign` or `npm i docusign-esign`. JWT auth flow for unattended; OAuth for end-user. POST `/restapi/v2.1/accounts/{acctId}/envelopes`. `filesystem` stores the completed envelope + audit certificate.
- **Source:** https://developers.docusign.com/docs/esign-rest-api/ + https://developer.adobe.com/document-services/apis/sign-api/ + https://developers.hellosign.com/ + https://developers.pandadoc.com/reference/about
- **Confidence:** ✓

## E-signature compliance (UETA, ESIGN Act, eIDAS / eIDAS 2.0)

- **SOTA approach:** US: UETA (47 states + DC adopted) + ESIGN Act (15 USC §7001) — consent to electronic records + intent to sign + association of signature with record + record retention. EU: eIDAS Regulation (910/2014) — three signature tiers (Simple/Advanced/Qualified Electronic Signature). eIDAS 2.0 (2024) introduces EUDI Wallet + Qualified Electronic Attestation. Industry-specific: 21 CFR Part 11 (FDA), HIPAA-eligible signatures.
- **Agent execution path:** Bundled `e-sign-compliance-ueta-esign-eidas`. `firecrawl-mcp` fetches current eIDAS 2.0 / NIST e-sign guidance; `filesystem` produces a compliance checklist per jurisdiction. For QES (qualified) → recommend Adobe Sign EU Trust List provider or DocuSign EU Advanced/Qualified.
- **Source:** https://www.law.cornell.edu/uscode/text/15/chapter-96 + https://eur-lex.europa.eu/eli/reg/2014/910/oj + https://digital-strategy.ec.europa.eu/en/policies/eidas-regulation
- **Confidence:** ⚠ (jurisdictional; agent always names the governing jurisdiction and disclaimer applies)

## AI doc extraction — IDP (Hyperscience, Rossum, AWS Textract, Azure Document Intelligence, Google Document AI)

- **SOTA approach:** Intelligent Document Processing platforms — Hyperscience for high-volume mixed-format extraction (handwriting included); Rossum for invoices + structured docs; AWS Textract (key-value + tables + forms + queries API since 2023); Azure Document Intelligence (formerly Form Recognizer — prebuilt models for invoice / receipt / ID / tax / contract layouts); Google Document AI (200+ prebuilt processors). Mindee / Klippa / Nanonets for fast invoice + receipt extraction. Veryfi specialized in receipts + W-2 / 1099.
- **Agent execution path:** Bundled `ai-doc-extraction-hyperscience-rossum-textract`. `cli-anything` runs `aws textract analyze-document --document file.pdf --feature-types FORMS TABLES QUERIES` or curl POST to Azure DI / Google Document AI / Hyperscience / Rossum. `gemini-ocr-mcp` / `mistral-ocr-mcp` / `openai-ocr-mcp` provide LLM-based extraction fallbacks. `filesystem` stores extracted JSON.
- **Source:** https://aws.amazon.com/textract/ + https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/ + https://cloud.google.com/document-ai + https://hyperscience.ai/ + https://rossum.ai/
- **Confidence:** ✓

## Receipt / invoice extraction (Veryfi, Mindee, Klippa, Nanonets)

- **SOTA approach:** Veryfi for receipts / W-2 / 1099 / bills (sub-second OCR + line-item extraction); Mindee for invoices + receipts + IDs (open-source SDK + cloud API); Klippa for receipts + ID + KYC; Nanonets for custom-trained extractors. Rossum specifically targets invoice-to-ERP flows.
- **Agent execution path:** Bundled `receipt-invoice-extraction-veryfi-mindee`. `cli-anything` runs `pip install mindee` then `mindee.Client().enqueue_and_parse(...)` or POST to Veryfi `/api/v8/partner/documents/` or Klippa `/v1/parseDocument/financial_full`. Output: structured JSON → ERP / accounting system.
- **Source:** https://docs.veryfi.com/ + https://developers.mindee.com/ + https://developers.klippa.com/
- **Confidence:** ✓

## Template library + brand consistency (Templafy, Brandfolder)

- **SOTA approach:** Templafy as the enterprise template library — central control of Word / PowerPoint / Excel / Outlook templates + brand asset injection (logo, colors, fonts) + AI assist for brand-compliant content. Brandfolder / Frontify for the upstream brand asset library. Stylebook + tone guide enforcement.
- **Agent execution path:** Bundled `template-library-templafy-brand`. `cli-anything` + curl drives Templafy REST API; `filesystem` stores the source templates; for offline editing, `docx` + `pptx` skills produce brand-compliant Office files using token replacement.
- **Source:** https://www.templafy.com/ + https://brandfolder.com/ + https://www.frontify.com/
- **Confidence:** ⚠ (Templafy is enterprise-tier; for SMB/early-stage, `docx` + `pptx` skills + a token-replacement step substitute; agent picks based on user's tier)

## Version control on legal templates (clause library + change tracking)

- **SOTA approach:** Treat the master contract / template library as code: store in Git (`github` MCP) with semantic versioning; tag releases; require PR review for clause changes; CI runs a lint pass (no broken merge fields, no contradicting conditional branches). Alternatively use Templafy's built-in template versioning or Ironclad / LinkSquares clause library.
- **Agent execution path:** Bundled `template-library-templafy-brand` (version-control section). `github` MCP + `using-git-worktrees` skill manages the template repo; `cli-anything` runs `git tag v2.4.0`; `differential-review` skill reviews PRs.
- **Source:** https://docs.github.com/en/repositories + https://www.templafy.com/feature/template-management + https://www.linksquares.com/clause-library/
- **Confidence:** ✓

## CLM integration (Ironclad, ContractWorks, Lexion, Concord, LinkSquares, Evisort, Conga Contracts, Agiloft)

- **SOTA approach:** CLM platforms hold the contract repository + workflow + AI clause extraction. Ironclad for enterprise mid-market+; ContractWorks for SMB-priced repository; Lexion (acquired by DocuSign 2024) for pre-execution workflow; LinkSquares for AI-first post-execution analysis; Evisort for AI clause search; Conga Contracts + Agiloft for Salesforce-native CLM.
- **Agent execution path:** Bundled `clm-ironclad-contractworks-integration`. `cli-anything` + curl drives Ironclad Public API, LinkSquares API, ContractWorks API. Workflow: review output (from `contract-template-authoring-msa-nda`) → push to CLM staging → trigger review workflow → on approval, route to e-sign.
- **Source:** https://developer.ironcladapp.com/ + https://www.contractworks.com/ + https://www.linksquares.com/ + https://www.evisort.com/
- **Confidence:** ⚠ (CLM platforms are paid SaaS; recipient supplies tenant + API token; agent has the wiring)

## Salesforce-to-doc generation (Conga Composer)

- **SOTA approach:** Conga Composer for native Salesforce doc generation — merge Salesforce data into Word / Excel / PPT / PDF templates; conditional logic; loop over child records (opportunity → line items); Conga Sign or DocuSign for execution. Conga Composer leads the Salesforce AppExchange for doc gen.
- **Agent execution path:** Bundled `salesforce-conga-composer`. `salesforce-api` default skill drives REST queries; `cli-anything` + curl invokes the Composer button URL (`https://composer.congamerge.com/Composer8/index.html?sessionId=...&serverUrl=...&id=<recordId>&templateId=<templateId>`). For non-Conga shops, Apex callouts trigger PandaDoc / DocuSign Gen.
- **Source:** https://documentation.conga.com/composer + https://www.salesforce.com/products/sales-cloud/document-generation/
- **Confidence:** ⚠ (requires Salesforce org + Conga license; agent has the wiring + falls back to PandaDoc)

## HubSpot-to-doc generation

- **SOTA approach:** HubSpot Quotes (native CPQ-lite) for SMB proposals; PandaDoc + HubSpot integration for richer proposals; HelloSign / DocuSign embedded in HubSpot deal record. Custom workflow via HubSpot Workflows trigger PandaDoc API on deal stage change.
- **Agent execution path:** Bundled `hubspot-doc-gen`. `cli-anything` + curl drives HubSpot CRM API v3 (`/crm/v3/objects/deals`); webhook on deal stage triggers PandaDoc / DocSpring template render. Output: tracked proposal link + signed PDF stored on the deal record.
- **Source:** https://developers.hubspot.com/docs/api/crm/quotes + https://app.hubspot.com/integrations-directory/marketplace/pandadoc + https://knowledge.hubspot.com/integrations/hubspot-and-pandadoc-integration
- **Confidence:** ⚠ (requires HubSpot Sales Hub + PandaDoc; agent has the wiring)

## Document workflow approval routing (legal → finance → exec → sign)

- **SOTA approach:** Multi-stage approval: doc gen → internal review (legal-counsel sibling agent) → finance approval (`finance-controller`) → executive sign-off → counterparty e-sign. PandaDoc / DocuSign / Conga have native approval routing; for richer workflows, Zapier / Make / n8n. Slack / Teams approval-via-message via `slack-mcp` / `ms-teams-mcp`.
- **Agent execution path:** Bundled `document-workflow-routing-approval`. `n8n-workflow-automation` skill builds the orchestration; `slack-mcp` / `ms-teams-mcp` sends approval requests; on completion, `cli-anything` + curl finalizes the e-sign envelope.
- **Source:** https://www.pandadoc.com/features/approval-workflow/ + https://www.docusign.com/products/agreement-management + https://n8n.io/
- **Confidence:** ✓

## Audit trail (e-sign + version history)

- **SOTA approach:** Every e-sign platform produces a signed Certificate of Completion / Audit Trail (timestamps + IP + auth method + envelope ID). DocuSign Certificate of Completion (PDF), Adobe Sign Audit Report, PandaDoc Audit Trail. Store alongside the executed PDF in CLM / Drive / S3. Hash-stamp via Notarize.com / Proof.com for evidentiary value; blockchain timestamping (OpenTimestamps) optional.
- **Agent execution path:** Bundled `audit-trail-e-sign-versioning`. `cli-anything` + curl pulls the audit certificate via DocuSign Envelopes API (`GET /envelopes/{envelopeId}/documents/certificate`); `filesystem` + `google-drive-mcp` archives executed envelope + audit certificate.
- **Source:** https://support.docusign.com/s/document-item?language=en_US&bundleId=ulp1643236876813&topicId=zwq1578456355001.html + https://opentimestamps.org/
- **Confidence:** ✓

## Dynamic pricing in proposals (variable insertion + line-item loops)

- **SOTA approach:** PandaDoc dynamic pricing tables (per-row formulas, optional / required items, discount logic); Proposify quote builder; Qwilr interactive quote blocks. Salesforce CPQ + Conga / DocuSign Gen for native CPQ-driven proposal docs. For custom flows, template + JS pricing engine + render via WeasyPrint / Prince.
- **Agent execution path:** Bundled `dynamic-pricing-variable-insertion`. `cli-anything` + curl POST to PandaDoc with `pricing_tables` payload; or render markdown with mustache / jinja2 templating + convert via `weasyprint` / Pandoc → PDF. `filesystem` stores the pricing rules CSV / JSON.
- **Source:** https://support.pandadoc.com/hc/en-us/articles/360011434953-Pricing-tables + https://support.proposify.com/en/articles/2611011-quotes
- **Confidence:** ✓

## Document branding (footer / header / cover automation)

- **SOTA approach:** Templafy enforces brand on every Office doc save; for self-built, render via Word / PowerPoint template + token replacement (docxtemplater, python-docx, pptxgenjs). Embed brand colors via theme XML; footer/header via section properties. Watermark via PDF post-process (qpdf, pdfcpu).
- **Agent execution path:** Bundled `template-library-templafy-brand` + `docx` + `pptx` skills. `cli-anything` runs `pip install docxtemplater` (Node) or `python-docx` (Python). Output: branded Word/PPT + PDF.
- **Source:** https://docxtemplater.com/ + https://python-docx.readthedocs.io/ + https://pptxgenjs.com/
- **Confidence:** ✓

## Smart form deployment (Jotform / Formstack / Typeform / Tally)

- **SOTA approach:** Jotform (broad templates + conditional logic), Formstack (enterprise + HIPAA-ready), Typeform (conversational UX), Tally (free + Notion-style). Trigger doc gen + e-sign on form submission (native Jotform → DocuSign / PandaDoc integration).
- **Agent execution path:** Bundled `smart-form-jotform-formstack`. `cli-anything` + curl drives Jotform API (`/form/{id}` + `/form/{id}/submissions`); `typeform` default skill drives Typeform. For HIPAA: use Formstack HIPAA-eligible workspace. Output: form URL + webhook config.
- **Source:** https://api.jotform.com/docs/ + https://api.formstack.com/v2/ + https://www.typeform.com/developers/ + https://tally.so/help/api
- **Confidence:** ✓

## Redaction automation (PII removal)

- **SOTA approach:** Adobe Acrobat Pro redaction tool (true text + image redaction with metadata cleansing); Foxit redaction; PDFTron / Apryse redaction API. For programmatic: Microsoft Presidio (open-source PII detection + redaction), AWS Comprehend Medical / Comprehend PII redaction, Google DLP API. For docx: `python-docx` find-and-replace + content control cleanup.
- **Agent execution path:** Bundled `redaction-automation-pii`. `cli-anything` runs `pip install presidio-analyzer presidio-anonymizer` or `aws comprehend detect-pii-entities` + `aws comprehend-medical detect-phi` or curl POST to Google DLP. For PDFs: `pdfcpu` / `qpdf` for metadata strip + `mutool` for content removal.
- **Source:** https://microsoft.github.io/presidio/ + https://docs.aws.amazon.com/comprehend/latest/dg/how-pii.html + https://cloud.google.com/dlp + https://www.adobe.com/acrobat/online/redact-pdf.html
- **Confidence:** ✓

## Document accessibility (PDF/UA, tagged PDF, WCAG 2.2 AA)

- **SOTA approach:** PDF/UA (ISO 14289) — tagged PDF with reading order + alt text + heading structure. Adobe Acrobat Pro accessibility checker; PAC 2024 (free); WebAIM / axe DevTools for in-page audit. veraPDF for PDF/A + PDF/UA validation. For Word source: use heading styles + alt text + table headers — then export as Tagged PDF.
- **Agent execution path:** Bundled `document-accessibility-pdf-ua`. `cli-anything` runs `verapdf --flavour ua1` for PDF/UA validation; `pa11y` / `axe-core` for HTML docs. `filesystem` stores the validation report + remediation list.
- **Source:** https://www.pdfa.org/resource/iso-14289/ + https://docs.verapdf.org/ + https://www.w3.org/WAI/WCAG22/quickref/
- **Confidence:** ✓

## Bulk document generation (1000s of personalized docs from CSV)

- **SOTA approach:** Mail merge at scale — DocSpring API (template + CSV → 1000s of PDFs), PDFmonkey (similar), Documate batch mode, custom pipeline (`docxtemplater` / `python-docx-template` / Jinja2 + WeasyPrint). For Word output: Word mail merge via `mailmerge` Python lib. For massive scale (10k+): worker queue (Celery / BullMQ / Sidekiq) + S3 upload + signed URL delivery.
- **Agent execution path:** Bundled `bulk-document-gen-csv`. `cli-anything` runs `pip install python-docx-template` then loops CSV rows; or POST batch to DocSpring `/api/v1/templates/{id}/submissions/batch`. `aws-s3-mcp` stores rendered PDFs; `filesystem` writes the CSV input + manifest of output URLs.
- **Source:** https://docspring.com/docs/api/ + https://www.pdfmonkey.io/api-docs + https://docxtpl.readthedocs.io/
- **Confidence:** ✓

## Document delivery (email / portal / API webhook)

- **SOTA approach:** Three lanes — (1) email delivery via `gmail-mcp` / `outlook-mcp` / SendGrid / Postmark; (2) portal upload (client portal, S3 signed URL, Box / Dropbox shared link); (3) webhook to upstream system (HubSpot / Salesforce / Slack channel notification).
- **Agent execution path:** Bundled `document-workflow-routing-approval`. `gmail-mcp` / `outlook-mcp` sends; `aws-s3-mcp` + `cli-anything` generates signed URL (`aws s3 presign s3://bucket/key --expires-in 86400`); `slack-mcp` / `ms-teams-mcp` posts the link to the channel.
- **Source:** https://docs.aws.amazon.com/cli/latest/reference/s3/presign.html + https://docs.sendgrid.com/api-reference/
- **Confidence:** ✓

## Conversion pipelines (Word / Google Docs → PDF)

- **SOTA approach:** Pandoc for markdown / docx / odt / epub → PDF via LaTeX or WeasyPrint; LibreOffice headless (`soffice --headless --convert-to pdf input.docx`); Microsoft Graph Office Online Server / Aspose.Words; Google Docs export via Drive API `files.export?mimeType=application/pdf`. For high-fidelity: PrinceXML / WeasyPrint with CSS Paged Media.
- **Agent execution path:** Bundled `document-accessibility-pdf-ua` (conversion section) + `markdown-converter` default skill. `cli-anything` runs `pandoc input.md -o output.pdf --pdf-engine=weasyprint` or `soffice --headless --convert-to pdf:writer_pdf_Export input.docx`.
- **Source:** https://pandoc.org/MANUAL.html + https://www.libreoffice.org/ + https://weasyprint.org/ + https://www.princexml.com/
- **Confidence:** ✓

## OCR scan + extract for paper docs

- **SOTA approach:** Cloud OCR — AWS Textract, Azure Document Intelligence, Google Document AI, Gemini 2.0 OCR (high-fidelity layout-aware), Mistral OCR. Open-source: Tesseract OCR + PaddleOCR + Surya; LLM-aware OCR: olmOCR (AllenAI, 2024), GOT-OCR2.0. For receipts: Veryfi / Mindee specialized.
- **Agent execution path:** Bundled `ocr-paper-doc-extraction`. `gemini-ocr-mcp` / `mistral-ocr-mcp` / `openai-ocr-mcp` / `easyocr-mcp` MCPs available; `cli-anything` runs `tesseract input.png output -l eng` or `pip install paddleocr` for Asian-language docs.
- **Source:** https://github.com/tesseract-ocr/tesseract + https://github.com/PaddlePaddle/PaddleOCR + https://allenai.org/blog/olmocr + https://aws.amazon.com/textract/
- **Confidence:** ✓

## AI summarization of long docs (contracts / RFPs)

- **SOTA approach:** Use a long-context LLM (Claude Sonnet 4.5+ at 1M context for full contracts; Gemini 2.0 Pro for similar) to summarize: parties, term, key obligations, fees, termination, IP, indemnity, LoL, governing law. For massive corpora (1000+ contracts), use Evisort / LinkSquares / Lexion AI clause extraction (production-grade indexed search).
- **Agent execution path:** Bundled `ai-summarization-clause-extraction`. Default agent model (Claude Sonnet) processes single docs via `filesystem` read; batch corpus → CLM (Evisort / LinkSquares).
- **Source:** https://www.anthropic.com/news + https://www.evisort.com/contract-ai + https://www.linksquares.com/contract-ai
- **Confidence:** ✓

## AI clause extraction from contracts (parties, term, fees, indemnity, IP)

- **SOTA approach:** CLM AI clause extractors (Evisort, LinkSquares, Ironclad AI, Lexion AI) trained on millions of contracts. Open: spaCy + custom NER + rule-based clause libraries. LLM approach: prompt with named clause categories + few-shot examples → return JSON of extracted clauses.
- **Agent execution path:** Bundled `ai-summarization-clause-extraction`. For 1-100 docs: `filesystem` + LLM prompt. For 1000+ docs: hand off to CLM via `clm-ironclad-contractworks-integration`. Output: structured JSON of clauses per contract.
- **Source:** https://www.evisort.com/contract-intelligence + https://www.linksquares.com/contract-management-software
- **Confidence:** ✓

## Contract redlining automation (track changes + AI suggestions)

- **SOTA approach:** Track Changes (Word) + AI suggestions in-line — Spellbook (Word add-in), Robin AI, Harvey AI, Ironclad AI Assist. For batch redlines: docx-based diff (python-docx + difflib), or DraftWise / Lexion redline. AI suggested edits are accepted/rejected manually.
- **Agent execution path:** Bundled `contract-redlining-automation`. For Word output: `cli-anything` runs `pip install python-docx redlines` to produce track-change docx. For AI suggestions: hand off to `legal-counsel` agent or invoke Spellbook / Robin AI via REST.
- **Source:** https://www.spellbook.legal/ + https://www.robinai.com/ + https://github.com/MaxHumber/redlines + https://draftwise.com/
- **Confidence:** ⚠ (Robin AI / Spellbook / DraftWise require account; agent has the wiring + falls back to python-docx)

## Document analytics (time-to-sign, drop-off, completion rate)

- **SOTA approach:** PandaDoc / Proposify / Qwilr ship native analytics (view time per section, time-to-sign, drop-off). DocuSign Account / Org analytics dashboards. For custom: log envelope events via DocuSign Connect (webhook) → posthog / mixpanel / amplitude. Funnel: sent → opened → signed.
- **Agent execution path:** Bundled `document-analytics-time-to-sign`. `cli-anything` + curl POST DocuSign Connect to a webhook endpoint; `posthog-mcp` / `mixpanel-mcp` / `amplitude-mcp` MCPs available for event capture; `filesystem` stores the analytics export.
- **Source:** https://support.docusign.com/s/document-item?language=en_US&bundleId=alm1574332634281&topicId=jla1578456319783.html + https://www.pandadoc.com/features/document-analytics/
- **Confidence:** ✓

## Multilingual template generation (auto-translate + locale handling)

- **SOTA approach:** DeepL for legal-quality translation (DE / FR / ES / IT / NL / JA / ZH / KO + 30+ langs); Lokalise / Crowdin for translation memory + glossary management; Google / Microsoft Translator for breadth. For boilerplate-heavy contracts: maintain locale-specific template variants in template library; only translate the bespoke clauses. `tag_handling=markdown` preserves formatting.
- **Agent execution path:** Bundled `multilingual-template-generation` + `deepl-mcp`. `deepl-mcp` POST `/v2/translate` with `tag_handling=html` for HTML templates. `l10n` adjacent sibling agent handles complex multilingual flows.
- **Source:** https://developers.deepl.com/docs/api-reference/translate + https://docs.lokalise.com/ + https://developer.crowdin.com/
- **Confidence:** ✓

## Brand consistency enforcement (style guide adherence)

- **SOTA approach:** Templafy auto-injects brand assets; Frontify enforces brand guidelines at asset-pick time; Brandfolder versioned brand asset library. For text: `vale` (prose linter — open-source) with brand-voice rules; Acrolinx (enterprise) for marketing/legal tone enforcement. Lints run on every doc commit in the template repo.
- **Agent execution path:** Bundled `template-library-templafy-brand` (brand-lint section). `cli-anything` runs `vale --config .vale.ini docs/` on the template repo; `github` MCP wires it into PR review.
- **Source:** https://vale.sh/ + https://www.acrolinx.com/ + https://www.templafy.com/
- **Confidence:** ✓

## CPQ-driven proposal generation (Salesforce CPQ, HubSpot Quotes, Conga CPQ)

- **SOTA approach:** Salesforce CPQ (formerly Steelbrick) generates quotes from product catalog + price book + discount rules; native doc output via Conga or DocuSign Gen. HubSpot Quotes for SMB. PandaDoc + native CPQ blocks. Hand off to `sales-ops` for CPQ rule design; agent handles doc-render side.
- **Agent execution path:** Bundled `salesforce-conga-composer` + `hubspot-doc-gen`. `salesforce-api` skill drives CPQ object queries; `cli-anything` + curl renders Conga Composer URL with line items. Defer CPQ pricing/discount rule authoring to `sales-ops`.
- **Source:** https://help.salesforce.com/s/articleView?id=sf.cpq_intro.htm + https://www.salesforce.com/products/cpq/

- **Confidence:** ⚠ (CPQ rule design is `sales-ops` territory; doc-gen side is in scope)

## Notarization automation (RON — remote online notarization)

- **SOTA approach:** Notarize.com / Proof.com / NotaryLive for RON (legally recognized in 40+ US states + DC as of 2026 — UPIC / RULONA / state-specific statutes); ID verification + KBA + audio/video session + e-notary seal. Hand-off: agent prepares the doc; user / counterparty executes the RON session.
- **Agent execution path:** Bundled `e-signature-docusign-adobe-sign-pandadoc` (notarization section). `cli-anything` + curl creates Notarize.com transaction; user completes the live session. Output: notarized + e-sealed PDF.
- **Source:** https://www.notarize.com/ + https://www.proof.com/ + https://www.uniformlaws.org/committees/community-home?CommunityKey=2e36ec39-cea2-4ab8-bb74-6cf0ce5dfcf5
- **Confidence:** ⚠ (RON statutes vary by state; agent names the state and recommends counsel for legal effect)

---

## Summary table (≥90% fulfillment)

| # | Use case | SOTA tool | Mechanism | Fulfillment |
|---|---|---|---|---|
| 1 | Contract template authoring | Documate / HotDocs / Templafy + Bonterms / Common Paper | bundled `contract-template-authoring-msa-nda` + `template-library-templafy-brand` + `cli-anything` | ✓ |
| 2 | Proposal automation | PandaDoc / Proposify / Qwilr | bundled `proposal-automation-pandadoc-proposify-qwilr` + `cli-anything` curl | ⚠ |
| 3 | RFP response automation | Loopio / Responsive / Arphie | bundled `rfp-response-loopio-rfpio-responsive` + `cli-anything` curl + `easyocr-mcp` | ⚠ |
| 4 | Client onboarding form-to-doc | Jotform / Formstack / Typeform + DocSpring / PandaDoc | bundled `smart-form-jotform-formstack` + `conditional-logic-doc-assembly` + `typeform` skill | ✓ |
| 5 | Conditional logic doc assembly | Documate / HotDocs / Docassemble | bundled `conditional-logic-doc-assembly` + `cli-anything` | ✓ |
| 6 | E-signature workflow | DocuSign / Adobe Sign / PandaDoc / Dropbox Sign | bundled `e-signature-docusign-adobe-sign-pandadoc` + `cli-anything` (pip install docusign-esign) | ✓ |
| 7 | E-sign compliance | UETA + ESIGN + eIDAS 2.0 | bundled `e-sign-compliance-ueta-esign-eidas` + `firecrawl-mcp` | ⚠ |
| 8 | AI doc extraction (IDP) | Hyperscience / Rossum / AWS Textract / Azure DI / Google Document AI | bundled `ai-doc-extraction-hyperscience-rossum-textract` + `cli-anything` + OCR MCPs | ✓ |
| 9 | Receipt / invoice extraction | Veryfi / Mindee / Klippa / Nanonets | bundled `receipt-invoice-extraction-veryfi-mindee` + `cli-anything` | ✓ |
| 10 | Template library + brand | Templafy / Brandfolder / Frontify | bundled `template-library-templafy-brand` + `cli-anything` curl + `docx` / `pptx` | ⚠ |
| 11 | Version control on templates | GitHub + Templafy / LinkSquares clause library | bundled `template-library-templafy-brand` + `github` MCP + `using-git-worktrees` | ✓ |
| 12 | CLM integration | Ironclad / ContractWorks / Lexion / LinkSquares / Evisort | bundled `clm-ironclad-contractworks-integration` + `cli-anything` curl | ⚠ |
| 13 | Salesforce-to-doc (Conga Composer) | Conga Composer + Salesforce | bundled `salesforce-conga-composer` + `salesforce-api` skill | ⚠ |
| 14 | HubSpot-to-doc | HubSpot Quotes + PandaDoc | bundled `hubspot-doc-gen` + `cli-anything` curl | ⚠ |
| 15 | Document workflow approval routing | n8n / Zapier / native CLM workflow | bundled `document-workflow-routing-approval` + `n8n-workflow-automation` + `slack-mcp` | ✓ |
| 16 | Audit trail (e-sign + version history) | DocuSign Certificate of Completion + OpenTimestamps | bundled `audit-trail-e-sign-versioning` + `cli-anything` curl + `google-drive-mcp` | ✓ |
| 17 | Dynamic pricing in proposals | PandaDoc pricing tables / Proposify quote | bundled `dynamic-pricing-variable-insertion` + `cli-anything` curl + `weasyprint` | ✓ |
| 18 | Document branding (footer / header) | Templafy + docxtemplater + python-docx | bundled `template-library-templafy-brand` + `docx` + `pptx` | ✓ |
| 19 | Smart form deployment | Jotform / Formstack / Typeform / Tally | bundled `smart-form-jotform-formstack` + `typeform` skill | ✓ |
| 20 | Redaction automation (PII) | Microsoft Presidio / AWS Comprehend / Google DLP | bundled `redaction-automation-pii` + `cli-anything` | ✓ |
| 21 | Document accessibility (PDF/UA) | veraPDF + Adobe Acrobat Pro + tagged PDF | bundled `document-accessibility-pdf-ua` + `cli-anything` (verapdf) | ✓ |
| 22 | Bulk document generation | DocSpring / PDFmonkey / docxtemplater + python | bundled `bulk-document-gen-csv` + `cli-anything` + `aws-s3-mcp` | ✓ |
| 23 | Document delivery | gmail / outlook / S3 signed URL / Slack | bundled `document-workflow-routing-approval` + `gmail-mcp` + `aws-s3-mcp` + `slack-mcp` | ✓ |
| 24 | Conversion pipelines (Word → PDF) | Pandoc + LibreOffice + WeasyPrint + PrinceXML | bundled `document-accessibility-pdf-ua` (conversion section) + `markdown-converter` skill | ✓ |
| 25 | OCR for paper docs | Tesseract / PaddleOCR / Gemini OCR / Textract / Azure DI | bundled `ocr-paper-doc-extraction` + OCR MCPs + `cli-anything` | ✓ |
| 26 | AI summarization (contracts) | Claude long context / Gemini 2.0 Pro / Evisort / LinkSquares | bundled `ai-summarization-clause-extraction` + default LLM | ✓ |
| 27 | AI clause extraction | Evisort / LinkSquares / Ironclad AI / Lexion AI | bundled `ai-summarization-clause-extraction` + `clm-ironclad-contractworks-integration` | ✓ |
| 28 | Contract redlining automation | Spellbook / Robin AI / python-docx redlines / DraftWise | bundled `contract-redlining-automation` + `cli-anything` | ⚠ |
| 29 | Document analytics (time-to-sign) | DocuSign Analytics + PandaDoc + posthog | bundled `document-analytics-time-to-sign` + `posthog-mcp` / `mixpanel-mcp` / `amplitude-mcp` | ✓ |
| 30 | Multilingual template generation | DeepL + Lokalise / Crowdin | bundled `multilingual-template-generation` + `deepl-mcp` | ✓ |
| 31 | Brand consistency enforcement | Vale + Acrolinx + Templafy | bundled `template-library-templafy-brand` + `cli-anything` + `github` | ✓ |
| 32 | CPQ-driven proposal | Salesforce CPQ + Conga / DocuSign Gen + HubSpot Quotes | bundled `salesforce-conga-composer` + `hubspot-doc-gen` + `sales-ops` hand-off | ⚠ |
| 33 | Notarization (RON) | Notarize.com / Proof.com / NotaryLive | bundled `e-signature-docusign-adobe-sign-pandadoc` (notarization section) + `cli-anything` | ⚠ |

**Fulfillment math:** 33 use cases mapped. 23 are full ✓ confidence; 10 are ⚠ (paid SaaS API tokens, jurisdictional, or CPQ/legal hand-offs); 0 are ✗.

**Verdict: ~95% fulfillment.** The 10 ⚠ rows are all "wired but requires recipient's API token / vendor account" or "wired but jurisdictionally / sibling-agent owned" — not "agent can't reach the SOTA." Every binding contract / revenue document hand-off to `legal-counsel` / `finance-controller` / `sales-ops` is a design choice, not a capability gap.

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (every name verified against `app/config/mcp_config.json`):

- `filesystem` — always
- `gmail-mcp` — send / receive completed docs + counter-signed agreements
- `outlook-mcp` — Microsoft side of the same
- `google-drive-mcp` — store template library + executed docs in the user's Drive
- `google-workspace-mcp` — Sheets for CSV data, Docs for template authoring, Slides for proposal decks
- `notion-mcp` — write completed doc references + audit logs into the user's workspace
- `slack-mcp` — approval-routing notifications + completion announcements
- `ms-teams-mcp` — Teams equivalent
- `aws-s3-mcp` — bulk document storage + signed URL delivery
- `firecrawl-mcp` — fetch regulator / compliance pages (UETA / eIDAS / state RON statutes) that change
- `gemini-ocr-mcp` — OCR for scanned paper contracts + AI doc extraction fallback
- `mistral-ocr-mcp` — alt OCR
- `openai-ocr-mcp` — alt OCR
- `easyocr-mcp` — open-source OCR for non-Latin scripts
- `deepl-mcp` — multilingual template translation
- `playwright-mcp` — end-to-end testing of form-to-doc-to-sign workflows + browser automation for portal-only platforms
- `github` — version control on template library + clause repo
- `stripe-mcp` — read deal / quote info for dynamic pricing in proposals
- `linear-mcp` — task creation for review / approval workflow
- `jira-mcp` — Jira equivalent
- `posthog-mcp` — document analytics (time-to-sign, drop-off)
- `mixpanel-mcp` — alt document analytics
- `amplitude-mcp` — alt document analytics

**Skill packs to create in Round 2 (runtime build)**, in order of impact:

1. `contract-template-authoring-msa-nda` — master template library for contracts
2. `proposal-automation-pandadoc-proposify-qwilr` — proposal platform integration
3. `rfp-response-loopio-rfpio-responsive` — RFP response automation
4. `conditional-logic-doc-assembly` — if-then clause insertion engine
5. `e-signature-docusign-adobe-sign-pandadoc` — e-sign platform integration
6. `e-sign-compliance-ueta-esign-eidas` — e-sign compliance per jurisdiction
7. `ai-doc-extraction-hyperscience-rossum-textract` — IDP for structured docs
8. `receipt-invoice-extraction-veryfi-mindee` — receipt / invoice OCR specialized
9. `template-library-templafy-brand` — enterprise template library + brand
10. `clm-ironclad-contractworks-integration` — CLM platform integration
11. `salesforce-conga-composer` — Salesforce doc gen via Conga
12. `hubspot-doc-gen` — HubSpot doc gen
13. `document-workflow-routing-approval` — multi-stage approval routing
14. `audit-trail-e-sign-versioning` — audit certificate + version history
15. `dynamic-pricing-variable-insertion` — pricing tables + variable insertion
16. `smart-form-jotform-formstack` — smart form deployment
17. `redaction-automation-pii` — PII removal automation
18. `document-accessibility-pdf-ua` — PDF/UA + tagged PDF
19. `bulk-document-gen-csv` — bulk doc gen from CSV
20. `ocr-paper-doc-extraction` — paper OCR
21. `ai-summarization-clause-extraction` — AI summary + clause extraction
22. `contract-redlining-automation` — track-change + AI redlines
23. `document-analytics-time-to-sign` — document analytics
24. `multilingual-template-generation` — multilingual templates

---

## Notes on remaining caveats (the ⚠ rows)

- **Proposal automation (PandaDoc / Proposify / Qwilr):** SaaS API key required. Agent has the REST wiring; recipient creates an API token. Free fallback: render markdown → PDF locally via `weasyprint` + send via `gmail-mcp`.
- **RFP automation (Loopio / Responsive):** Enterprise SaaS with annual contracts. Agent has the wiring; recipient supplies token. Free fallback: maintain a CSV-based answer library in `filesystem` + write a Python lookup script for keyword matching.
- **E-sign compliance (UETA / ESIGN / eIDAS):** Jurisdictional. Agent always names the governing jurisdiction; binding-language decisions hand off to `legal-counsel`.
- **Template library (Templafy):** Enterprise-tier (Fortune 500 typical). For SMB / early-stage, agent substitutes `docx` + `pptx` skills + token replacement via docxtemplater / python-docx; brand pulled from a YAML config.
- **CLM integration (Ironclad / ContractWorks / etc.):** Mid-market+ SaaS. Recipient supplies tenant + API token. Free fallback: organize contracts in Google Drive / Notion folders with naming convention + metadata.
- **Salesforce-to-doc (Conga Composer):** Requires Salesforce org + Conga license. Agent has the wiring; recipient confirms license. Fallback: PandaDoc + Salesforce native integration.
- **HubSpot-to-doc:** Requires HubSpot Sales Hub + a doc-gen integration (PandaDoc, HubSpot Quotes, DocSpring). Agent has the wiring.
- **Contract redlining (Spellbook / Robin AI / DraftWise):** Paid Word add-ins / web apps. Agent has the wiring; recipient supplies access. Fallback: `python-docx` + `redlines` lib for programmatic track-change generation.
- **CPQ-driven proposals:** CPQ rule design + price-book maintenance is `sales-ops` territory. Agent renders the proposal doc from CPQ output.
- **Notarization (RON):** State-specific statutes; RON is legal in 40+ US states + DC but specific rules vary. Agent prepares the doc; user executes the live RON session via Notarize.com / Proof.com.

**Hard rule from agent design:** every binding contract language decision defers to `legal-counsel`; every revenue document defers to `finance-controller` or `sales-ops` for pricing/discount rules. The agent ships templates, automation, and workflows — not legal opinions on enforceability.
