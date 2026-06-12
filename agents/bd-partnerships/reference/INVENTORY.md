# bd-partnerships — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from per-vendor docs, methodology references, and web research (URLs cited in SOTA_USE_CASES.md and SOURCES.md).

For future tightening: pull 4-6 reference agents from `wshobson/agents`, `VoltAgent/awesome-claude-code-subagents`, `msitarzewski/agency-agents`, `vijaythecoder/awesome-claude-agents` into `reference/agents/`, and 6-10 reference skills into `reference/skills/`.

---

## Files in this folder

| File | Status | Source notes |
|---|---|---|
| `INVENTORY.md` | full | this file |
| `SOTA_USE_CASES.md` | full | Per-use-case SOTA mapping, June 2026 |

## Sources considered but not downloaded

- **wshobson/agents** — no bd-partnerships agent exists upstream; sales / marketing analogs scanned for shape. v2 should pull `business-development-architect` if/when it ships.
- **VoltAgent/awesome-claude-code-subagents** — no partnership-specific agent; closest is the `sales-architect` (sourced for hand-off patterns).
- **msitarzewski/agency-agents** — has a `partnerships-manager` agent reportedly; not downloaded in v1 — flag for v2.
- **Anthropic skills repo** — no partnership-specific skills; bundled skills authored from vendor docs + methodology references.

## Methodology sources used (web research, June 2026)

- Partnerstack API docs — referral / affiliate / reseller channel management
- Tackle.io product docs — cloud marketplace co-selling (AWS, Azure, GCP)
- Crossbeam + Reveal product docs — account mapping for co-sell ecosystems
- Impartner + Allbound + Channeltivity — PRM and partner portal patterns
- AWS Marketplace Seller Operations docs — listing creation, SaaS Contracts, private offers
- Azure Marketplace publisher docs — SaaS offers, Partner Center
- GCP Marketplace + Salesforce AppExchange listing requirements + security review
- HubSpot App Marketplace + Shopify App Store + Slack App Directory listing reqs
- PandaDoc + DocuSign for contract structuring + e-sign workflow
- Crunchbase + Pitchbook + LinkedIn Sales Navigator + Apollo for partner sourcing
- Forrester / Canalys / IDC partner ecosystem research (2025-2026)
- Channel Mechanics + Mindmatrix PRM frameworks
- "The Partnership Economy" (Crossbeam) + "Partner-Led Growth" (Tackle) playbooks
