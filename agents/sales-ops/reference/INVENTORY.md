# sales-ops — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in SOTA_USE_CASES.md and SOURCES.md) plus the seed list in the per-agent build prompt.

For future tightening: pull 4-6 reference agents from wshobson/agents (look in `plugins/sales/` and `plugins/operations/`), VoltAgent/awesome-claude-code-subagents (categories `06-business`, `04-data`), msitarzewski/agency-agents, vijaythecoder/awesome-claude-agents into `reference/agents/`, and 6-10 reference skill packs for SalesOps-adjacent tools (Salesforce Admin, HubSpot Operations Hub, CaptivateIQ, Spiff, QuotaPath, Clari, LeanData, Chili Piper, Salesforce CPQ, Highspot, Showpad) into `reference/skills/`.

## Seed list (from build prompt, June 2026)

**CRM admin:** Salesforce Admin (custom objects, validation rules, flows, formulas, Apex triggers, process builder, validation rules), HubSpot Operations Hub (data quality automations, programmable automation, custom-coded actions), Pipedrive Admin, Microsoft Dynamics 365 Admin.

**Sales engagement tech-stack admin:** Salesloft Admin, Outreach Admin, Gong Admin (call deployment, scorecards, smart trackers), Chorus Admin, Apollo Admin, Clay Workflows admin (enrichment pipelines).

**Forecasting:** Clari, BoostUp, InsightSquared (Mediafly), Aviso, Gong Forecast, Clari Align, Salesforce Sales Cloud forecasting.

**Commission automation (ICM/SPM):** Spiff (Salesforce), QuotaPath, Everstage, Performio, Xactly, CaptivateIQ, Forma.ai, CompCloud, Beqom, Iconixx, Salesforce Spiff (newly acquired), Varicent.

**CPQ + revenue:** Salesforce CPQ (Steelbrick), Pricefx, Conga CPQ, DealHub CPQ, Salesforce Revenue Cloud (acquired Vlocity), FastSpring, Stripe Subscriptions, Zuora CPQ, Subskribe.

**Lead routing + book-of-business:** LeanData (Salesforce-native), Chili Piper, Distribute, RouterDB, Default, OpenPrise routing, RingDNA routing.

**Data hygiene + dedup:** LeadIQ, ZoomInfo Engage, Apollo enrichment, Clay enrichment, Demandbase, Cloudingo (Salesforce dedup), DupeBlocker, RingLead.

**Sales enablement:** Highspot, Showpad, Seismic, Lessonly, Mindtickle, Brainshark, Allego.

**Reporting + sales analytics:** Salesforce CRMA (Tableau CRM / Einstein Analytics), HubSpot Reports, Looker, Sigma, Mode, Hex, dbt (transformation), Snowflake/BigQuery (warehouse).

**Territory + quota:** Anaplan (territory + quota planning), Varicent (territory), Salesforce Territory Management 2.0, Fullcast, RingLead Cleanse + Route.

**Sales process methodology:** Pipeline-stage definitions (entry/exit criteria), opportunity hygiene, opportunity stale-deal alerts, deal desk operations (discount approval, exception workflow), MAP/MEDDIC enforcement at the system level (custom fields + validation rules).

## Resolution against CraftBot catalog (June 2026)

- **Salesforce admin, HubSpot Operations Hub, Spiff, QuotaPath, CaptivateIQ, Salesforce CPQ, Conga, DealHub, Salesforce CRMA, LeanData, Chili Piper, Highspot, Showpad, Seismic, Clari, BoostUp, Gong Admin, Salesloft Admin, Outreach Admin, Apollo Admin, Clay Workflows, Looker, Sigma, Mode, Hex** — **proxied** via `api-gateway` managed OAuth (Maton has 100+ apps; SalesOps-tier tools are first-class).
- **`salesforce-api`, `attio-api`, `pipedrive-api`, `zoho-crm`, `zoho-bigin`** — **dedicated CraftBot default skills** for CRM read/write.
- **`postgres`, `mysql`, `xlsx`, `microsoft-excel`, `google-sheets`, `docx`, `pdf`, `pptx`, `notion`, `slack`, `microsoft-teams`** — **dedicated CraftBot default skills**.
- **`api-gateway`** — universal managed-OAuth proxy for SalesOps tools above.
- **`cli-anything`** — `dig` / `curl` / `jq` / `pandas` / `dbt` / scripted ETL — covers any SalesOps tool with a REST API.
- Sibling agents already in catalog: `sales-agent` (parent — direct seller motion), `data-analyst` (deep analytics), `finance-controller` (commission accounting, revenue recognition), `marketing-agent` (lead handoff at top of funnel), `operations-agent` (cross-functional ops), `customer-support-agent` (post-sale handoff stand-in for the future customer-success agent).

SOTA mapping is verified per use case in `SOTA_USE_CASES.md` with confidence ratings and source URLs.
