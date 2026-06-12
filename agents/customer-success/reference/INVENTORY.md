# customer-success — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research on the 2026 customer-success operator stack (URLs cited in `SOTA_USE_CASES.md`, `SOURCES.md`, and `agent.yaml → sources`).

Adjacent CraftBot agent for shape and voice cross-reference: `agent_bundle/agents/customer-support-agent/` (reactive ticket-driven support — distinct motion from this agent's proactive renewal / expansion / health-score / onboarding ownership).

---

## Sources considered

| Source | Status | Notes |
|---|---|---|
| wshobson/agents — `plugins/customer-success/` | Not downloaded v1 | Round 2 backfill target |
| VoltAgent/awesome-claude-code-subagents — `categories/09-customer-success/` | Not downloaded v1 | Round 2 backfill target |
| msitarzewski/agency-agents | Not downloaded v1 | Round 2 backfill target |
| 2026 SOTA CSP platform docs (Vitally / Catalyst / Gainsight / ChurnZero / Totango / Custify / Velaris / Planhat) | Used directly | URLs cited in SOTA_USE_CASES.md |
| In-product onboarding tooling docs (Pendo / Userpilot / Appcues / Chameleon / Whatfix / ProductFruits) | Used directly | URLs cited in SOTA_USE_CASES.md |
| Product analytics docs (Amplitude / Mixpanel / PostHog / Heap / FullStory) | Used directly | CraftBot MCPs available |
| Survey / VoC docs (Delighted / Survicate / Sprig / Wootric / Iterate) | Used directly | URLs cited in SOTA_USE_CASES.md |
| Customer comms (Mixmax / Outreach / Salesloft / Klaviyo / Customer.io / Iterable) | Used directly | renewal outreach + lifecycle |
| Customer interview / call (Calendly / Zoom / Granola / Fathom / tl;dv / Otter.ai) | Used directly | Calendly, Fathom CraftBot skills exist |
| Renewal + commercial (Salesforce CPQ / Zuora / Stripe Subscriptions) | Used directly | Stripe MCP available |
| Advocacy + reference (Influitive / Slapfive / UserEvidence / Champion) | Used directly | URLs cited in SOTA_USE_CASES.md |
| Adjacent CraftBot agent (`customer-support-agent`) | Read for voice + structure mirror | NOT a content lift — this agent is a different motion |

---

## For Round 2 tightening

Pull 4-6 reference agents from upstream catalogs into `reference/agents/`:

1. `wshobson/agents` — `plugins/customer-success/agents/customer-success-manager.md` or similar
2. `VoltAgent/awesome-claude-code-subagents` — `categories/09-customer-success/` entries
3. `msitarzewski/agency-agents` — search for customer success / account management agents
4. `vijaythecoder/awesome-claude-agents` — any CS specialists

Pull 6-10 reference skills from those repos into `reference/skills/`:
- onboarding-day-30-60-90 patterns
- QBR facilitation templates
- health-score formula examples (composite weights)
- NRR / GRR calculation patterns
- renewal-prep 90-day procedure
- expansion-opportunity scoring rubric
- customer-advocacy outreach templates

Diff against current composition synthesis; tighten role.md voice where reference language is stronger.
