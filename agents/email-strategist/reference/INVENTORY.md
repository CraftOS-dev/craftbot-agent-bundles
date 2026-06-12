# email-strategist — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in `SOTA_USE_CASES.md` and `SOURCES.md`) plus the parent agent's reference corpus at `agent_bundle/agents/marketing-agent/reference/agents/msitarzewski-email-strategist.md` (richest single source on lifecycle, deliverability, post-MPP measurement, multi-language architecture, 2024-2025 compliance).

This is a **specialist** under `marketing-agent` — drilling much deeper than the parent on email lifecycle, deliverability, DMARC reporting, IP warming, BIMI, post-MPP measurement, transactional/marketing separation, and IP reputation.

For future tightening: pull 4-6 reference agents (e.g., wshobson/agents `email-marketing-specialist`, VoltAgent `lifecycle-email-strategist`, msitarzewski `email-strategist`, plus dedicated deliverability + IP-warming playbooks) into `reference/agents/`, and 6-10 reference skill packs (e.g., wshobson `dmarc-rua-parser`, `bimi-vmc-setup`) into `reference/skills/`.

## Source posture for v1 build

The parent `marketing-agent` already carries `msitarzewski-email-strategist.md` (lifecycle stages, deliverability landscape, MPP measurement, multi-language architecture, GDPR + ePrivacy 2026 state, sequence + audit templates) as a "full" reference. This agent re-uses that source for shared rules and extends with 2025-2026 web research for the deep-specialist surface (DMARC reporting tooling, IP warming services, BIMI / VMC, transactional vs marketing IP/domain separation, advanced RFM / predictive segmentation, dynamic personalization, Beehiiv / Substack newsletter economics).

## Sources Considered But Not Downloaded

| Source | Why deferred to v1 follow-up |
|---|---|
| wshobson `plugins/email-marketing/agents/` | Not yet enumerated; planned for next refresh |
| Anthropic skills catalog | No email-strategist skill at June 2026 catalog |
| Customer.io / Klaviyo blog playbooks (deep flow design, predictive AI) | Cited inline in `SOTA_USE_CASES.md`; not snapshotted to `reference/` yet |
| dmarcian + Valimail blog posts on DMARC enforcement | Cited inline in `SOTA_USE_CASES.md`; not snapshotted to `reference/` yet |
| BIMI Group + DigiCert / Entrust VMC docs | Cited inline; full snapshot deferred |
