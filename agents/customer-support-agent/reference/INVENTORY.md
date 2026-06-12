# customer-support-agent — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in SOTA_USE_CASES.md and SOURCES.md).

For future tightening: pull 4-6 reference agents from wshobson/agents (look for `plugins/customer-support/` and `plugins/operations/`), VoltAgent/awesome-claude-code-subagents (categories/09-customer-success), msitarzewski/agency-agents (operations/customer-support-*), vijaythecoder/awesome-claude-agents into `reference/agents/`, and 6-10 reference skills into `reference/skills/`.

## Roles this agent supersets

- Senior support engineer / Tier-2 support
- Support operations / RevOps adjacent (ticket-to-Linear handoff, SLA mgmt)
- Customer experience (CSAT/CES/NPS measurement)
- Customer success early-warning (churn signals from support)
- Trust & safety triage
- Community manager (Discord / Reddit / forum monitoring)
- Post-incident communications (Statuspage)

## Sources Considered But Not Downloaded

| Source | Why excluded |
|---|---|
| wshobson `plugins/customer-support/skills/` | Not browseable at expected path in v1 pass — defer to v2 refresh |
| VoltAgent `categories/09-customer-success` | Deferred to v2 refresh; SOTA mapping in `SOTA_USE_CASES.md` does the work |
| msitarzewski customer-experience-manager / support-operations-lead | Adjacent; would add depth on CSP/CSM split but not on triage execution |
| Anthropic skills | No customer-support skills in their catalog yet |
| Intercom / Zendesk in-product AI (Fin, Resolution Bot) | These are the SOTA TARGET, not reference agent material. Documented as platforms in SOTA_USE_CASES.md |
