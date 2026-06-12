# sales-agent — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in SOTA_USE_CASES.md and SOURCES.md) plus the seed list in the per-agent build prompt.

For future tightening: pull 4-6 reference agents from wshobson/agents, VoltAgent/awesome-claude-code-subagents, msitarzewski/agency-agents, vijaythecoder/awesome-claude-agents into `reference/agents/`, and 6-10 reference skills into `reference/skills/`.

## Seed list (from build prompt, June 2026)

**CRM + revenue platforms:** HubSpot remote MCP (mcp.hubspot.com), Salesforce MCP (Apex/SOQL), Pipedrive API, Attio, Folk CRM, Copper CRM, Zoho CRM, Zoho Bigin.

**Lead enrichment + data:** Apollo.io, Clay.com, Lusha, ZoomInfo, Cognism, Common Room, Default API, RB2B (deanonymization), Pocus (PLG), Koala (PLG).

**Engagement / sequences:** Outreach.io, Salesloft, lemlist, Reply.io, instantly.ai, Smartlead, HeyReach (LinkedIn), Lemwarm (warmup), La Growth Machine, Heyflow.

**Conversation intelligence:** Gong, Chorus.ai, Fathom, tl;dv, Fireflies, Otter.ai.

**LinkedIn / social selling:** LinkedIn Sales Navigator (Phantombuster/TexAu scraping), Phantombuster, TexAu.

**Proposals / quotes / signing:** DocuSign, PandaDoc, Qwilr, Proposify, DealHub (CPQ).

**Forecasting / analytics:** Clari, Gong Forecast, BoostUp, InsightSquared.

**Cold email deliverability:** mail-tester.com, Postmark spam check, Glock Apps, MXToolbox.

## Resolution against CraftBot catalog (June 2026)

- HubSpot, Apollo, Salesforce, Outreach, Salesloft, Lemlist, Instantly, Gong, Fathom, Fireflies, Calendly, DocuSign, PandaDoc, Clay, LinkedIn, Microsoft Excel, Google Sheets — **already proxied** via the `api-gateway` default skill (`gateway.maton.ai/<app>/`).
- `pipedrive-api`, `salesforce-api`, `attio-api`, `zoho-crm`, `zoho-bigin`, `calendly-api`, `fathom-api`, `linkedin`, `mailchimp`, `gmail`, `outlook`, `slack`, `microsoft-teams`, `notion`, `google-sheets` — **dedicated default skills** (in `skills/` root).
- Sibling agents already in catalog: `marketing-agent`, `research-analyst`, `senior-python-engineer`, `technical-writer`, `video-creator`. Hand-offs to `customer-support-agent`, `product-manager`, `finance-controller`, `legal-counsel` are aspirational (catalog v1).

SOTA mapping is verified per use case in `SOTA_USE_CASES.md` with confidence ratings and source URLs.
