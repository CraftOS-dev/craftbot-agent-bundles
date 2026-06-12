# community-manager — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research on the 2026 community-operator stack (URLs cited in `SOTA_USE_CASES.md` and `SOURCES.md`).

For future tightening: pull 4-6 reference agents from wshobson/agents (look for `plugins/community/`, `plugins/customer-success/`, `plugins/marketing/`), VoltAgent/awesome-claude-code-subagents (`categories/09-customer-success`, `categories/04-content-marketing`), msitarzewski/agency-agents (`community-manager-*`, `community-strategist-*`), JSONbored/claudepro-directory into `reference/agents/`, and 6-10 reference skills covering Circle/Discord/Slack ops, community CRMs (Common Room/Orbit), and ambassador-program patterns into `reference/skills/`.

## Roles this agent supersets

- Community manager / community operator (general)
- Community strategist (platform selection + charter)
- Discord / Slack moderator
- Community ops / CommunityOps (CRM + analytics + tooling)
- Ambassador program lead
- Developer relations (DevRel) — for the community side, not docs/talks
- UGC + advocacy coordinator
- Forum moderator (Discourse / Reddit / GitHub Discussions)
- Member journey designer (lurker → contributor → ambassador)
- Community-led growth analyst (members → MQLs / retention / advocacy)
- Trust & safety (community-side enforcement of code of conduct)
- Beta program manager (community-driven beta)
- Web3 community ops (Snapshot / Mirror / Lens / Discord)

## Sibling agents (defer rules in soul.md)

- `marketing-agent` — broad paid + brand strategy + multi-channel campaigns
- `social-media-manager` — public-social posting + comments + DMs at scale
- `customer-support-agent` — ticket escalations + SLA + KB
- `customer-success` — post-sale relationship + expansion + advocacy nuance
- `content-creator` — long-form content + editorial calendar
- `email-strategist` — newsletter + lifecycle email (Substack/Beehiiv border)

## Sources Considered But Not Downloaded

| Source | Why excluded |
|---|---|
| wshobson `plugins/community/` | Defer to v2 refresh; SOTA mapping in `SOTA_USE_CASES.md` is doing the work for v1 |
| VoltAgent `categories/09-customer-success/community-*` | Adjacent overlap with customer-success; deferred to v2 |
| msitarzewski community-manager / community-strategist | Useful but timed out of v1 scope; web-search seeded the SOTA tool list directly |
| Anthropic skills (anthropics/skills) | No community-management skill packs in their catalog yet |
| Common Room / Orbit / Insider Notable docs | These are SOTA TARGETS, not reference-agent material. Documented as platforms in SOTA_USE_CASES.md |
| Circle / Mighty Networks / Heartbeat platform docs | SOTA TARGETS — documented per use case in SOTA_USE_CASES.md |
| Reforge "Community-Led Growth" syllabus | Excellent reference but paywalled; CLG measurement patterns adapted from public posts |
