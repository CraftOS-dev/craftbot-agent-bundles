# docgen-automation — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in `SOTA_USE_CASES.md` and `SOURCES.md`).

For future tightening: pull 4-6 reference agents from `wshobson/agents`, `VoltAgent/awesome-claude-code-subagents`, `msitarzewski/agency-agents`, `vijaythecoder/awesome-claude-agents` into `reference/agents/`, and 6-10 reference skills into `reference/skills/`. Candidate agents to mirror once available:

- Document automation / templating specialist (Documate, HotDocs, Templafy operator)
- Proposal automation specialist (Proposify / PandaDoc / Qwilr operator)
- RFP response automation specialist (Loopio / RFPIO / Responsive)
- E-signature integration specialist (DocuSign / Adobe Sign / Dropbox Sign)
- AI document extraction (Hyperscience / Rossum / AWS Textract / Azure DI)
- CLM integration specialist (Ironclad / ContractWorks / Conga / Evisort)

## Sources considered but not downloaded

- **Anthropic skills repo** — no published `doc-automation` / `e-signature` skills as of June 2026.
- **wshobson plugins** — no dedicated `doc-gen` plugin yet; closest is `operations` (not yet downloaded).
- **VoltAgent categories** — `13-business-operations` houses a `business-process` agent and `09-productivity-and-knowledge` houses doc-related agents; queued for v1 refresh.

## SOTA tooling sources

Primary research lanes for the agent's day-to-day stack (each cited per use case in `SOTA_USE_CASES.md`):

1. **Document automation / templating** — Documate, HotDocs, NetDocuments, Conga Document Generation, Salesforce Conga, DocuSign Gen, PandaDoc, Templafy, Docassemble (FOSS), Formstack Documents (formerly WebMerge), Jotform, Anvil, DocSpring, PDFmonkey.
2. **RFP automation** — Loopio, RFPIO/Responsive, Qvidian, Ombud, Arphie.
3. **Proposal automation** — Proposify, Better Proposals, GetAccept, Qwilr, Bonsai, HelloBonsai.
4. **CLM (contract lifecycle management)** — Ironclad, ContractWorks, Lexion, Concord, LinkSquares, Evisort, Conga Contracts, Agiloft.
5. **E-signature** — DocuSign, Adobe Sign (Acrobat Sign), HelloSign / Dropbox Sign, SignNow, eversign, SignWell, RightSignature, Conga Sign, OneSpan.
6. **AI document extraction (IDP)** — Hyperscience, Rossum, Klippa, AWS Textract, Azure Document Intelligence (formerly Form Recognizer), Google Document AI, Veryfi (receipts), Mindee, Nanonets.
7. **PDF tools** — Adobe Acrobat Pro DC, Foxit PDF Editor, PDFTron / Apryse, PDF.co API, pdf-lib, jsPDF, ReportLab, WeasyPrint, Prince, PrinceXML, Puppeteer / Playwright print-to-PDF.
8. **Compliance** — UETA (Uniform Electronic Transactions Act, US), ESIGN Act (15 USC §7001 et seq.), eIDAS Regulation (EU 910/2014 + eIDAS 2.0 with EUDI Wallet).

Each tool used as a SOTA mechanism in this agent has a canonical URL recorded in `SOURCES.md` "SOTA tool sources (June 2026)" and in the per-use-case rows of `SOTA_USE_CASES.md`.
