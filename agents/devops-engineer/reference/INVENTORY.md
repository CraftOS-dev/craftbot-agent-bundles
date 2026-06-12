# devops-engineer — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in `SOTA_USE_CASES.md` and `SOURCES.md`).

For future tightening: pull 4-6 reference agents from `wshobson/agents` (devops-engineer, kubernetes-architect, terraform-engineer, sre-engineer, cloud-architect), `VoltAgent/awesome-claude-code-subagents` (07-devops-engineering/* category), `msitarzewski/agency-agents`, `vijaythecoder/awesome-claude-agents` into `reference/agents/`, and 6-10 reference skills (kubernetes-deployments, helm-patterns, terraform-modules, github-actions, argocd-flux, prometheus-grafana, opentelemetry-instrumentation, sigstore-supply-chain, slo-design, incident-response-runbook) into `reference/skills/`.

The agent's load-bearing convictions — (1) **immutability over mutation** (rebuild, don't patch), (2) **observability is non-negotiable** (if you can't see it, you can't operate it), (3) **toil is a bug** (automate every repeat-task) — were synthesized from the published Google SRE handbook, the GitOps Working Group principles, the CNCF cloud-native definition, and the methodology guidance in the per-agent prompt seeds. Each is traceable to a primary source in `SOURCES.md`.

---

## Composition rule

When updating `agent.yaml`, `soul.md`, or `role.md`, every section must be traceable back to either:
- A use-case row in `SOTA_USE_CASES.md` (which cites a primary source URL), OR
- A SOTA tool source in `SOURCES.md`, OR
- Short authored operational glue (must be flagged in `SOURCES.md` under "Notes on authored-from-synthesis").

If you cannot cite the source, you cannot write the sentence. The "generic SRE philosophy" failure mode (pleasant-sounding bullets with no source) is forbidden.

---

## Sources considered but not downloaded (for v1 reference pull)

- `github.com/wshobson/agents/tree/main/plugins/devops-engineering/agents/` — devops-engineer, deployment-engineer, kubernetes-architect, terraform-engineer, sre-engineer, cloud-architect
- `github.com/wshobson/agents/tree/main/plugins/devops-engineering/skills/` — multiple SOTA skills for Docker, K8s, IaC, CI/CD, secrets, observability
- `github.com/VoltAgent/awesome-claude-code-subagents/tree/main/categories/07-devops-engineering` — devops-engineer, deployment-engineer, cloud-architect, kubernetes-specialist, terraform-engineer, sre-engineer, incident-responder
- Google SRE handbook (https://sre.google/books/) — SLO design, error budgets, postmortems
- CNCF Landscape (https://landscape.cncf.io/) — cloud-native tool taxonomy
- The Twelve-Factor App (https://12factor.net/) — app/infra contract
- OpenTelemetry spec (https://opentelemetry.io/docs/specs/otel/) — observability standard
- SLSA framework (https://slsa.dev/) — supply chain attestation
- GitOps Principles (https://opengitops.dev/) — declarative, versioned, pulled, observed

These will be downloaded into `reference/agents/` and `reference/skills/` in the v1 tightening pass; the v1 SOTA mapping is already independently sourced via the URLs in `SOTA_USE_CASES.md`.
