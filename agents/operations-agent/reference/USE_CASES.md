# Operations Agent — Use Cases

**Tier:** general · **Category:** operations
**Core job:** End-to-end business operations operator — hiring pipeline, onboarding + offboarding flows, performance reviews + 1:1s, comp bands, employee handbook + policies, vendor evaluation + SaaS spend audit, procurement playbook, internal tool building, workflow automation, process documentation, SSO + device management, payroll setup, PEO/EOR global hiring, travel + expense, business insurance audit, office management, business continuity / DR, vendor risk + DPA, internal KB, and runbook authoring.

> Ships with the SOTA 2026 ops stack — Greenhouse / Ashby / Lever for ATS; Rippling / Gusto / HiBob / Deel for HRIS + payroll + EOR; Lattice / 15Five / Culture Amp / Leapsome for performance; Pave / Carta Total Comp for compensation; Vendr / Tropic / Spendflo for procurement; ToolJet / Retool / Budibase / Appsmith for internal tools; n8n / Zapier / Make / Pipedream for workflow automation; Scribe / Tango / Whale / Trainual for process docs; Okta / JumpCloud / WorkOS / Stytch / Auth0 for SSO; Iru (Kandji) / Jamf / Intune / Rippling IT for MDM; Pebl / Oyster / Remote / G-P / Deel for global hiring; Brex / Ramp / Navan / Expensify for T&E; Vouch / Embroker / Newfront / Coalition for insurance; Robin / Envoy for office; Notion / Confluence / Slab / Tettra for KB; PagerDuty / Incident.io for incident runbooks. Executes end-to-end against ATS / HRIS / MDM / SSO / vendor data / KB / workflow automation. **Always defers binding employment-law / vendor-contract / insurance-binder review to `legal-counsel`** — agent computes, models, and surfaces; humans approve binding actions; a licensed counsel signs anything legally binding.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### Hiring pipeline (ATS)
- Open req in Greenhouse / Ashby / Lever / Workable with structured scorecards
- JD authoring with bias review + comp band disclosure
- Pipeline stage design + pass-through targets
- Interviewer training + calibration cadence
- Offer letter draft (binding signature deferred to `legal-counsel`)

### Onboarding lifecycle (Day 0 → 30/60/90)
- T-7 hardware order + zero-touch enrollment (Apple ABM / Microsoft AutoPilot)
- T-3 HRIS profile + SCIM provisioning across Google Workspace / Slack / GitHub / Notion / Linear / role apps
- T-0 welcome message + Day-1 checklist (handbook ACK, I-9, W-4/W-9, benefits enrollment)
- 30/60/90 milestone tracking in Lattice Grow / Notion + calendar holds
- Buddy pairing + manager 1:1 cadence

### Offboarding lifecycle (resignation / termination)
- Same-day SCIM deprovisioning across all SSO-connected apps
- Device wipe via MDM + relocation to standby pool
- GitHub / repo / Linear access revoke + transfer
- Final paycheck per-state PTO payout rules (CA / IL / MA mandatory)
- Exit interview + knowledge transfer doc

### Performance review cycle
- Annual / semi-annual / continuous cadence
- Cycle config (rating scale + rubric + sources: self / peer / upward / downward)
- Calibration session structure + distribution targets
- Manager training on rating bias
- Comp-decision matrix (rating × base raise × equity refresh × bonus % × promo)

### 1:1 cadence + manager training
- 1:1 templates (weekly / biweekly)
- Manager onboarding (first-time manager training: Lattice Grow / LifeLabs)
- 1:1 cadence drift detection

### Compensation philosophy + bands
- Pave / Carta Total Comp band data pulls
- Band structure (low / mid / high) per role × level × geography
- Geo-tier rules (Tier 1 / 2 / 3 US; international per local market)
- Band placement rules (new hire / Meets / High performer / promotion)

### Employee handbook + policies
- Multi-state US handbook (CA / NY / IL / MA / WA + national)
- PTO + sick leave per state (CA paid sick leave + IL Wage Payment Act + MA Earned Sick Time)
- Remote / hybrid / in-office policy
- AI usage policy (NIST AI RMF + ISO 42001 + Anthropic responsible-use)
- Information security + acceptable use
- Anti-harassment + EEO + ADA accommodations
- Code of conduct + conflict of interest
- Annual handbook ACK distribution

### Vendor evaluation + negotiation
- Build-vs-buy framework (Spolsky Strategy Letter V — core vs context)
- TCO matrix (license + integration + training + opportunity + switching + lock-in)
- Security review (SOC 2 + DPA + ISO + pen-test)
- Reference call protocol
- 1-page recommendation memo

### SaaS spend audit + rationalization
- 12-month spend pull from Xero / QBO + Ramp / Brex
- SSO log cross-ref for MAU-per-tool (Okta / WorkOS / JumpCloud)
- Duplicate detection (Notion + Confluence + Slab; Loom + Berrycast + Scribe; etc.)
- Tropic 2025 benchmark application (top-10 = 74% of spend)
- Renewal calendar (90/60/30/7-day alerts)

### Procurement playbook (intake → approval → contract → renewal)
- Intake form (Typeform / Tally / Notion forms)
- Approval routing by spend tier (<$500 / $500-$5K / $5K-$25K / >$25K)
- Security review SLA per tier
- Contract storage (Google Drive + Notion DB)
- Renewal calendar entry on signature

### Internal tool building
- Retool / ToolJet / Budibase / Appsmith / Internal.io / Stacker / Softr pick
- Data connection + query design + UI assembly
- Permission model + SSO gating
- Audit log + Notion KB entry
- 30-day usage review + PostHog analytics

### Workflow automation
- n8n self-host (>5K runs/mo or LangChain agent) / Make (visual mid-volume) / Zapier (app catalog low-tech)
- Common automations: hire-provisioning, term-deprovisioning, renewal reminders, expense flagging, milestone tracking, exit survey, handbook ACK, status-page incident
- Idempotency + error handling + dry-run + owner-with-last-tested

### Process documentation (SOP / runbook)
- Auto-capture (Scribe / Tango / Whale) vs manual authoring
- Divio / Diátaxis taxonomy (tutorial / how-to / reference / explanation)
- Distribution (Notion / Slab / Tettra / Confluence / Trainual) per team size + Slack heaviness
- 30-day freshness recheck + stale-content flag

### SSO / IAM setup
- Stage-based platform pick (Stytch / Auth0 / WorkOS / Okta / JumpCloud)
- SCIM directory sync for top-10 apps
- SAML config + per-role group mapping
- JIT provisioning + audit log
- Conditional access policies (geo / MFA) — defer binding compliance to `devops-engineer` / `legal-counsel`

### Device management (MDM)
- Platform pick (Iru/Kandji / Jamf / Intune / Rippling IT / Hexnode)
- Blueprint authoring (app bundle + OS update + encryption + EDR + VPN)
- Zero-touch enrollment (Apple ABM / Microsoft AutoPilot)
- Lifecycle hooks (HRIS hire/term → MDM enroll/wipe)
- Quarterly compliance review

### Payroll setup
- Stage-based pick (Gusto SMB / Rippling 50+ / HiBob mid-market / Deel global / Justworks PEO)
- State tax registration (defer binding nexus to `finance-controller`)
- Benefits enrollment (health + 401(k) + commuter + EAP + workers' comp)
- Pay schedule + first-payroll dry run (defer GL tie-out to `finance-controller`)

### PEO / EOR global hiring
- Country selection matrix (own-entity vs partner; Deel best API; Pebl 48-hr)
- Statutory minimums per country (notice + leave + bonus)
- Local payroll + benefits + tax withholding
- Manager training on country norms
- **Defer binding country-specific employment law to `legal-counsel`**

### Travel + expense + corp card
- Brex (Capital One) + Navan + Ramp + Expensify + SAP Concur stage match
- Policy authoring (cabin class, hotel cap, per-diem, approval thresholds)
- Card setup (limits, MCC restrictions, receipt threshold)
- Auto-reconciliation routing (Brex/Ramp/Navan → Xero/QBO)

### Business insurance audit
- Coverage stack by stage (GL → D&O → E&O → Cyber → EPLI → Crime → Fiduciary → K&R)
- Carrier comparison (Vouch / Embroker / Newfront / Coalition / At-Bay / Hartford)
- Embroker Startup Package (instant D&O + E&O + Cyber + EPLI bundle)
- Renewal review (90 days pre-renewal; re-quote with 2-3 brokers)
- **Defer binding binder to `legal-counsel` + licensed insurance broker**

### Office management
- Desk + room + parking booking (Robin 2026 Gartner MQ Leader)
- Visitor management (Envoy delivery + compliance)
- Hybrid policy (in-office days, anchor day, hot-desking)

### Business continuity / disaster recovery
- BIA (criticality + downtime cost + RTO + RPO + dependencies)
- Recovery plan per tier (Tier 1 <4h / Tier 2 <24h / Tier 3 <1wk / Tier 4 <1mo)
- Comms playbook (status page + Slack incident + customer email + regulator notice)
- Tabletop exercise quarterly

### Vendor risk assessment + DPA
- SOC 2 Type 2 review (73% of 2026 buyers start here)
- Security questionnaire (CAIQ / SIG Lite / custom)
- DPA drafting (purpose + sub-processors + breach notice + audit + retention/deletion)
- Risk tier (Critical / Important / Standard)
- Vendor register + annual review

### Data retention + deletion policy
- GDPR Art. 17 (right to erasure) + CCPA delete-request workflows
- DSAR workflow (Linear / Notion + per-system deletion)
- Vanta / Drata / OneTrust / Transcend / Osano platform integration

### Internal knowledge base architecture
- Team-size pick (Slab <20 / Tettra Slack-native / Notion 20-50 / Confluence enterprise)
- Notion Agents trained per teamspace (HR Agent, IT Agent)
- Cross-tool unified search (Slab / Glean / Coveo)
- Permission mapping to SCIM groups
- Stale-content flag at 90 days

### Runbook authoring (operational + incident)
- Per-scenario structure (severity + symptoms + diagnostic + mitigation + comms + recovery + post-mortem)
- Blameless post-mortem (Google SRE template)
- Operational runbooks (recurring tasks documented)
- Incident runbooks (PagerDuty / Incident.io integrated)

### AI policy / responsible use
- Approved-tool inventory
- Data classification tier rules
- Vendor AI DPA addendum
- Output review tier for high-stakes outputs
- Frameworks: NIST AI RMF + ISO 42001 + EU AI Act + Anthropic guidance

### Compensation review cycle
- Annual / semi-annual band refresh from Pave / Carta
- Performance-tied comp decisions (calibration matrix)
- Pay-equity audit
- Promotion bar consistency

### Employee survey design
- eNPS + engagement (Culture Amp / Lattice / 15Five / Leapsome)
- Pulse surveys (Officevibe / Bonusly)
- Exit interview (Typeform / Lattice exit)
- Survey design (segmentation + free-text + benchmark)

### Vendor renewal calendar + alerts
- Notion DB with date triggers
- 90/60/30/7-day Slack + email reminders
- Auto-renewal removal policy

### Org chart + headcount visualization
- HRIS API pull (Rippling / Gusto / HiBob / BambooHR)
- ChartHop / Pingboard / Lattice Org Chart for managed
- Mermaid / D2 / drawio for ad-hoc

### Background check + I-9 / E-Verify
- Checkr / GoodHire / Certn / HireRight trigger
- I-9 via HRIS (Rippling / Gusto / HiBob / WorkBright)
- E-Verify via Gusto / Rippling

---

## Execution status (SOTA — June 2026)

> Mandatory table. Every use case above appears here as a row. Source: `reference/SOTA_USE_CASES.md`.

| Use case | SOTA mechanism | Path |
|---|---|---|
| Hiring pipeline (ATS) | Greenhouse + Ashby + Lever + Workable | `cli-anything` + ATS REST |
| Employee onboarding | Rippling + Gusto + HiBob + SCIM | `cli-anything` + `google-workspace-mcp` + `slack-mcp` + `github` + `notion-mcp` |
| Employee offboarding | HRIS + Okta/WorkOS + MDM | `cli-anything` + SCIM + MDM API |
| Performance review cycle | Lattice + 15Five + Culture Amp + Leapsome | `cli-anything` + platform REST |
| 1:1 cadence + manager training | Lattice + 15Five + Officevibe + LifeLabs | `notion-mcp` + `google-calendar-mcp` + platform REST |
| Compensation philosophy + bands | Pave + Carta Total Comp + Levels.fyi | `cli-anything` + `xlsx` + `notion-mcp` |
| Employee handbook + policies | Notion + Trainual + HRIS templates | `notion-mcp` + `docx` |
| PTO / vacation policy | HRIS (Gusto/Rippling/HiBob) + state-specific | `cli-anything` + `notion-mcp` |
| Remote / hybrid policy | Notion + Robin + Envoy | `notion-mcp` + `cli-anything` REST |
| Vendor evaluation framework | TCO matrix + Vendr/Tropic benchmarks | `xlsx` + `notion-mcp` |
| SaaS spend audit | Tropic + Vendr + Productiv + Torii + SSO logs | `cli-anything` + `xero-mcp` |
| Software contract negotiation | Vendr + Tropic + Spendflo + DIY | `cli-anything` + `docx` |
| Procurement playbook | Ramp Procurement + Brex + Coupa + intake forms | `cli-anything` + Typeform + `linear-mcp` + `notion-mcp` |
| Internal tool building | Retool + ToolJet + Budibase + Appsmith + Internal.io | `cli-anything` + docker/npm |
| Workflow automation | n8n + Zapier + Make + Pipedream | `cli-anything` + docker / REST |
| Process documentation | Scribe + Tango + Whale + Trainual + Notion | `cli-anything` + `notion-mcp` |
| SSO / IAM setup | WorkOS + Okta + JumpCloud + Stytch + Auth0 | `cli-anything` + SCIM + SAML |
| Device management | Iru (Kandji) + Jamf + Intune + Rippling IT | `cli-anything` + MDM REST |
| IT support tier-1 + runbook | Linear / Jira + Notion / Slab / Tettra | `linear-mcp` + `jira-mcp` + `notion-mcp` |
| Payroll setup | Gusto + Rippling + Deel + Justworks + HiBob | `cli-anything` + REST |
| PEO / EOR global hiring | Deel + Remote + Oyster + Pebl + G-P | `cli-anything` + REST (Deel best surface) |
| Travel + expense | Brex + Navan + Ramp + Expensify + SAP Concur | `cli-anything` + REST |
| Corporate card policy | Brex + Ramp + Navan Connect | `cli-anything` + REST |
| Business insurance audit | Vouch + Embroker + Newfront + Coalition + At-Bay | `cli-anything` + broker REST + `docx` |
| Office space management | Robin + Envoy + Tactic + Skedda | `cli-anything` + REST |
| Business continuity / DR | BIA + RTO/RPO + cloud backup + status page | `cli-anything` + `aws-s3-mcp` + `slack-mcp` + `twilio-mcp` |
| Vendor risk assessment | SOC 2 + DPA + security questionnaires | `cli-anything` + `gmail-mcp` + `docx` |
| Data retention + deletion | GDPR/CCPA + Vanta/Drata trust centers | `cli-anything` + `notion-mcp` + `linear-mcp` |
| Internal knowledge base | Notion + Slab + Tettra + Confluence + Slite | `notion-mcp` + `obsidian-mcp` + `cli-anything` |
| Runbook authoring | Notion + PagerDuty / Incident.io | `notion-mcp` + `cli-anything` |
| AI policy / responsible use | NIST AI RMF + ISO 42001 + Anthropic guidance | `docx` + `notion-mcp` |
| Compensation review cycle | Pave + Carta Total Comp + Lattice | `xlsx` + `cli-anything` REST |
| Employee survey design | Culture Amp + Lattice + 15Five + Typeform + Tally | `cli-anything` + REST |
| Vendor renewal calendar | Notion DB + Cledara / Vendr / Tropic / SpendHound | `notion-mcp` + `google-calendar-mcp` + `slack-mcp` |
| Org chart + headcount viz | ChartHop + Pingboard + Mermaid / D2 | HRIS REST + `drawio-mcp` + `excalidraw-diagram-generator` |
| Background check + I-9 | Checkr + GoodHire + Certn + HRIS I-9 | `cli-anything` + REST |

---

## Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| ATS (Greenhouse / Ashby / Lever / Workable) | ⚠ | Recipient provides paid API key. All have sandbox. |
| HRIS-led use cases (onboarding / offboarding / PTO / payroll / comp) | ⚠ | Recipient provides Gusto / Rippling / HiBob / Deel / Justworks key. Deel = best dev surface. |
| Performance / 1:1 platforms | ⚠ | Recipient provides Lattice / 15Five / Culture Amp / Leapsome key. |
| Compensation market data (Pave / Carta Total Comp) | ⚠ | Recipient pays for live market data; Levels.fyi / Glassdoor public fallback. |
| SSO / IAM | ⚠ | Recipient provides Okta / JumpCloud / WorkOS / Stytch / Auth0 key. Setup CLI-friendly. |
| Device management (MDM) | ⚠ | Recipient provides Iru/Kandji / Jamf / Intune / Rippling IT key. |
| EOR / PEO (Deel / Remote / Oyster / Pebl / G-P) | ⚠ | Recipient provides paid key. Deel has best dev surface (only EOR with public docs + sandbox + webhooks pre-contract). |
| Travel + expense + corp card (Brex / Ramp / Navan) | ⚠ | Recipient provides paid API key. Brex API surface evolving post-Capital One acquisition (April 2026). |
| Office management (Robin / Envoy) | ⚠ | Recipient provides paid key. |
| Vendor spend platforms (Vendr / Tropic / Spendflo / SpendHound) | ⚠ | Recipient pays for managed procurement; manual playbook works without. |
| Background check + I-9 (Checkr / GoodHire) | ⚠ | Recipient provides paid key. |
| Binding employment-law / vendor-contract / insurance-binder review | ⚠ | **Always disclose "defer to `legal-counsel` for binding review."** Agent drafts the structure, models trade-offs, surfaces decisions — humans + licensed counsel approve binding actions. Not a capability gap — operational discipline. |
| Multi-state employment-law compliance | ⚠ | Agent surfaces state-by-state variance; binding interpretation deferred to `legal-counsel`. |
| Country-specific employment-law (EOR work) | ⚠ | Agent surfaces statutory minimums + termination protection norms; binding interpretation deferred to `legal-counsel`. |
| Regulatory compliance audits (SOC 2 fieldwork / ISO 27001 audit / GDPR DPIAs) | ⚠ | Agent prepares + tracks; binding sign-off deferred to `compliance-agent` (when in catalog) + `legal-counsel`. |

**Verdict (June 2026): ~95% fulfillment.** Every documented use case has a named SOTA tool with an exact agent execution path. All ⚠ entries resolve once the recipient provides their existing platform's API key — these are operationally normal in ops / HR / IT / procurement work where every platform charges per seat. There are no ✗ rows (genuinely impossible work). Authoring (policies, runbooks, handbook sections, BCP plans, AI policy, evaluation frameworks) is fully free-tier across `notion-mcp` / `docx` / `xlsx` / `markdown-converter`. The "defer to `legal-counsel`" disclosure is operational discipline, not a capability gap.

---

## When to use this agent

- "Open a senior engineer req in Greenhouse — set up scorecards, pipeline stages, and JD."
- "Onboard [new hire] starting next Monday — laptop, accounts, handbook, Day-1 schedule, 30/60/90 plan."
- "Offboard [employee] effective Friday — same-day deprovisioning, exit interview, knowledge transfer."
- "Run our Q2 performance cycle in Lattice — config the cycle, calibration session prep, comp matrix."
- "Build comp bands for engineering L3-L6 + sales AE I-III — pull Pave + apply geo tiers."
- "Update the employee handbook for CA + NY + IL state changes + add AI usage policy."
- "Evaluate Lattice vs 15Five vs Leapsome — TCO matrix, reference calls, recommendation memo."
- "Audit our SaaS spend — find duplicates, low-utilization tools, top-10 review, build renewal calendar."
- "Set up a procurement intake form + approval routing — auto-renew prevention."
- "Build an internal tool in ToolJet for the sales team to track territory assignments."
- "Automate new-hire provisioning — Rippling hire event → SCIM + Slack welcome + calendar holds."
- "Roll out SSO via WorkOS for our top-10 SaaS apps — SCIM mapping per role."
- "Set up MDM in Iru/Kandji for our Mac fleet — zero-touch + lifecycle hooks."
- "Hire someone in Germany via Deel EOR — onboarding plan + benefits config."
- "Draft a BCP plan with BIA + tabletop schedule."
- "Review this vendor's SOC 2 + draft a DPA addendum."
- "Set up Notion as our internal KB — architecture, AI agents, SCIM permissions."
- "Write the incident runbook for AWS region failure."
- "Draft our AI usage policy — approved tools, data classification, vendor AI DPA."

---

## When NOT to use this agent

- **Binding employment-law review / vendor-contract review / IP assignment / insurance-binder signing** — hand off to `legal-counsel`. Agent drafts + surfaces clause-by-clause vs market norms; counsel signs binding language.
- **Financial reporting / AP execution / payroll-to-GL tie-out / cap-table maintenance** — hand off to `finance-controller`. Operations runs payroll setup; finance reconciles + reports + maintains cap table.
- **Deep IT infrastructure (network, Kubernetes, cloud architecture, observability stack design, security pen-testing)** — hand off to `devops-engineer`. Operations runs MDM + SSO + SaaS layer; devops runs infra layer.
- **Strategic org design / executive hiring / board comp / equity philosophy** — hand off to `ceo-agent` (when in catalog). Operations executes the org; CEO sets strategy.
- **Product-side analytics (feature usage, activation funnel, retention)** — hand off to `product-manager` (when in catalog). Operations runs internal-tool analytics; PM runs product analytics.
- **Marketing campaigns / paid ad ops / event ops / brand merch / customer marketing** — hand off to `marketing-agent`. They run go-to-market; you run go-to-team.
- **Sales pipeline / quota / commission plan / sales-ops Salesforce admin** — hand off to `sales-agent`. They own pipeline + quota; you own comp framework + sales-ops tooling design.
- **Customer support tier-1 escalations / customer support ticket process** — hand off to `customer-support-agent`. They own customer support; you own internal IT runbook + KB shape.
- **Security audits / SOC 2 fieldwork / regulatory compliance audits** — hand off to `compliance-agent` (when in catalog) + `legal-counsel`. Operations prepares + tracks; compliance audits + binding sign-off.
- **Code review for internal-tool components built in Retool / ToolJet beyond v1 prototyping** — hand off to `senior-python-engineer` or `frontend-engineer`. Operations builds v1; engineers review for prod-grade hardening.
- **Personal finance / individual taxes / personal HR** — out of scope. This is a business / startup ops agent.
- **Binding financial / tax decisions** — defer to a licensed CPA / CFO via `finance-controller`. **Always disclosed.** Operations agent computes + surfaces; humans + licensed counsel/CPA approve binding actions.
