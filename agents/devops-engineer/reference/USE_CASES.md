# DevOps Engineer — Use Cases

**Tier:** specialized · **Category:** infra
**Core job:** Ship and operate production infrastructure end-to-end — containers, Kubernetes, IaC (Terraform/OpenTofu/Pulumi/CDK), GitOps (ArgoCD/Flux), CI/CD (GitHub Actions OIDC), observability (OpenTelemetry + Honeycomb/Datadog or self-hosted Grafana stack), incident response, SLOs, secrets management, supply-chain attestation, and FinOps.

> Ships with the SOTA 2026 cloud-native stack — executes end-to-end via Helm/Kustomize/OpenTofu/Pulumi/ArgoCD/Flux/Trivy/Cosign/Syft/Argo Rollouts/Vault/ESO/OTel/Sloth/Infracost. The five ⚠ rows in the execution table are all paid-SaaS / OAuth gates owned by the recipient (paging providers, feature-flag backends, SOC 2 evidence collectors); free OSS fallbacks (Grafana OnCall, Unleash, OPA/Kyverno) ship immediately.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### Containers
- Dockerfile authoring — multi-stage, distroless/Wolfi base, BuildKit cache, multi-arch, `HEALTHCHECK`, non-root `USER`
- Image signing + verification via Cosign keyless (OIDC + Fulcio + Rekor)
- SBOM generation (Syft → SPDX / CycloneDX)
- Container vuln scanning (Trivy + Snyk + Grype)

### Kubernetes
- Deployment / Service / Ingress / ConfigMap / Secret / HPA / PDB / NetworkPolicy manifests
- Helm chart authoring + `values.schema.json` + OCI registry distribution
- Kustomize overlays (dev / staging / prod)
- K8s admission policies (Kyverno / OPA Gatekeeper)
- Multi-env strategy (vCluster preview envs, ApplicationSets)
- Cluster + PV backup/restore (Velero)

### Infrastructure-as-Code
- Terraform / OpenTofu module authoring + remote state + lock + encryption
- Pulumi authoring (Python / TypeScript / Go) + Pulumi ESC
- AWS CDK 2.x / SST v3 / SAM
- Cost diff in PR (Infracost) + plan/preview attached
- Policy-as-code (Conftest / Checkov / tfsec / Kyverno)

### CI/CD
- GitHub Actions workflows — OIDC to AWS/GCP/Azure, reusable workflows, matrix strategy, composite actions
- Build → test → scan → sign → push → SBOM → SLSA attest → deploy pipeline
- Action pinning by SHA + `actionlint` + `act` local testing

### GitOps + progressive delivery
- ArgoCD App-of-Apps + ApplicationSets + sync waves + image-updater
- Flux v2 (CNCF graduated) — for orgs requiring CNCF-only stack
- Argo Rollouts canary + blue/green with AnalysisTemplate
- Feature flags via OpenFeature + LaunchDarkly / Statsig / Unleash backends

### Secrets
- HashiCorp Vault / OpenBao as source-of-truth + dynamic credentials
- External Secrets Operator (ESO) sync to K8s `Secret` resources
- Pulumi ESC, Doppler, AWS Secrets Manager, Infisical as alternatives
- Pre-commit + CI secret detection (gitleaks, trufflehog)

### Observability
- OpenTelemetry instrumentation (Python/JS/Go/Java auto-instrumentation) + Collector
- Managed backends (Honeycomb, Datadog, Grafana Cloud, New Relic)
- Self-hosted stack (kube-prometheus-stack + Loki + Tempo + Mimir + Pyroscope + Vector)
- Resource attribute conventions (`service.name`, `deployment.environment`, `service.version`)

### SLOs + alerting
- SLI / SLO / error budget design (Google SRE Workbook framing)
- SLO YAML → Prometheus rules (Sloth / Pyrra / Nobl9)
- Multi-window multi-burn-rate alerting (5min @ 14.4×, 1h @ 6×)
- Alert routing (Alertmanager + PagerDuty / Opsgenie / Incident.io / Grafana OnCall)

### Incident response
- Runbook authoring (Markdown sibling to code, linked from alert `runbook_url`)
- War-room coordination (incident.io / Rootly / FireHydrant / Slack)
- Mitigation playbook (rollout undo, ArgoCD rollback, feature-flag-off, scale)
- Blameless PIR (Google SRE template, action items as GitHub issues)
- On-call rotation design (PagerDuty / Opsgenie / Grafana OnCall OSS)

### Supply chain security
- Cosign keyless image + SBOM signing
- SLSA Build Level 3 provenance (`slsa-framework/slsa-github-generator`)
- in-toto attestations
- Admission verification (Kyverno + `cosign verify-attestation`)

### Cost / FinOps
- Infracost diff on every IaC PR (cost regression gate)
- OpenCost (CNCF) for K8s workload-level cost
- Karpenter (AWS) for spot+rightsize autoscaling
- Goldilocks K8s right-sizing recommendations
- Cloud bill aggregation (Vantage / CloudHealth) — managed view

### DNS / CDN / PaaS
- Cloudflare (DNS + CDN + WAF + Workers + Pages + R2 + Zero-Trust)
- Vercel (Next.js, frontend)
- Railway / Fly.io / Render / DigitalOcean (containerized PaaS)
- TLS automation (cert-manager + Let's Encrypt + step-ca for internal PKI)

### DR + backup
- Velero (K8s cluster + PV backup → S3/GCS/Azure Blob)
- Restic / WAL-G for filesystem + Postgres point-in-time-recovery
- Cross-region replication for blob storage
- RTO/RPO documentation per service
- Quarterly DR drills

### DB migration coordination
- Atlas (declarative SQL migrations) or Liquibase 4.x for legacy
- Parallel-change (expand-contract) pattern for zero-downtime
- `pg-online-schema-change` / `pt-online-schema-change` for MySQL hot DDL

### Capacity planning + load testing
- k6 (Grafana, JS scripts) — modern default
- Locust (Python) for teams in Python ecosystem
- Vegeta for simple HTTP load
- xk6-disruptor for chaos injection

### Compliance + policy-as-code
- OPA / Conftest for IaC policy enforcement
- Kyverno for K8s admission control
- Falco for runtime security signals
- SOC 2 evidence generation (handoff to compliance-engineer for full packet)

### Developer experience
- Backstage IDP (Spotify, CNCF incubating) — Software Catalog, Tech Docs, Templates
- Port / Cortex / OpsLevel as managed alternatives
- Golden-path templates via Backstage Scaffolder

---

## Execution status (SOTA — June 2026)

> Mandatory table. Every use case from the section above appears here as a row. This is the proof the agent is real, not a toy. 1:1 with `reference/SOTA_USE_CASES.md`.

| Use case | SOTA mechanism | Path |
|---|---|---|
| Dockerfile authoring | Docker BuildKit + Chainguard/distroless + Cosign | `cli-anything` (`docker buildx`, `cosign sign`) |
| K8s deployment manifests | Helm 3 + Kustomize + kubeconform + Kyverno | `kubernetes-mcp` + `cli-anything` (`helm`, `kustomize`, `kubeconform`) |
| Helm chart authoring | Helm 3 + helm-docs + Cosign + OCI registry | `cli-anything` (`helm package`, `helm push oci://...`) |
| Kustomize overlays | kubectl + kustomize | `cli-anything` (`kubectl diff -k`, `kubectl apply -k`) + `kubernetes-mcp` |
| Terraform / OpenTofu | OpenTofu 1.8 (default) / Terraform 1.9 + tflint + checkov + infracost | `cli-anything` (`tofu init/plan/apply`, `tflint`, `checkov`, `infracost`) |
| Pulumi | Pulumi 3.x + Pulumi ESC | `cli-anything` (`pulumi up`, `pulumi config set --secret`, `pulumi esc env`) |
| AWS CDK / SST / SAM | CDK 2.x + SST v3 + SAM | `cli-anything` (`cdk deploy`, `sst deploy`, `sam build/deploy`) |
| GitHub Actions | OIDC + reusable workflows + actionlint + act | `github` MCP + `cli-anything` (`gh workflow run`, `actionlint`, `act`) |
| ArgoCD GitOps | ArgoCD 2.13 + App-of-Apps + image-updater | `cli-anything` (`argocd app sync/diff/rollback`) + `kubernetes-mcp` |
| Flux GitOps | Flux v2 (CNCF graduated) | `cli-anything` (`flux bootstrap/reconcile/get`) + `kubernetes-mcp` |
| Secret management | Vault/OpenBao + ESO + Pulumi ESC | `cli-anything` (`vault kv`, `kubectl apply -f external-secret.yaml`) + `kubernetes-mcp` |
| CI/CD pipeline | GH Actions + BuildKit + Trivy + Cosign + Syft + SLSA | `cli-anything` (`trivy`, `cosign`, `syft`) + `github` MCP |
| Container scanning | Trivy + Snyk + Grype | `cli-anything` (`trivy image/fs/k8s/sbom`) |
| SBOM + attestation | Syft + Cosign + SLSA + in-toto | `cli-anything` (`syft`, `cosign attest`, `slsa-generator`) |
| OTel observability | OTel SDK + Collector + Honeycomb/Datadog/Grafana Cloud | `cli-anything` (`helm install otel-collector`) + `kubernetes-mcp` |
| Self-hosted observability | kube-prometheus-stack + Loki + Tempo + Mimir + Vector | `cli-anything` (`helm install kps loki tempo mimir`) + `kubernetes-mcp` |
| SLO design | Sloth / Pyrra / Nobl9 | `cli-anything` (`sloth generate`, `pyrra generate`) |
| Alerting + paging | Alertmanager + PagerDuty/Opsgenie/Incident.io/Grafana OnCall (OSS) | `cli-anything` (paging API curl) + `sentry-mcp` |
| Incident response | Runbooks (`runbooks/<svc>/<scenario>.md`) + incident.io/Rootly + Slack | `filesystem` + `cli-anything` + `sentry-mcp` + `kubernetes-mcp` |
| Post-incident review | Blameless PIR template + incident.io + Howie.ai | `filesystem` + `github` MCP (issue creation with `incident-followup` label) |
| Blue/green deployment | Argo Rollouts blueGreen + service selector swap | `cli-anything` (`kubectl argo rollouts promote/abort`) + `kubernetes-mcp` |
| Canary deployment | Argo Rollouts canary + AnalysisTemplate / Flagger | `cli-anything` (`kubectl argo rollouts set image/status`) + `kubernetes-mcp` |
| Feature flags | OpenFeature SDK + LaunchDarkly/Statsig/Unleash | `cli-anything` (paged provider API curl) |
| Cost optimization | Infracost + OpenCost + Karpenter + Goldilocks | `cli-anything` (`infracost`, `kubectl-cost`, `goldilocks summary`) |
| Multi-environment | GitOps overlay pattern + vCluster + ApplicationSet | `cli-anything` (`vcluster create`, ArgoCD ApplicationSet YAML) + `kubernetes-mcp` |
| DR + backup | Velero + Restic + WAL-G + cross-region replication | `cli-anything` (`velero backup/schedule/restore`) + `aws-s3-mcp` + `kubernetes-mcp` |
| DB migration | Atlas / Liquibase + parallel-change | `cli-anything` (`atlas migrate apply`) + `postgresql-mcp` |
| DNS + CDN | Cloudflare + Wrangler / Fastly / CloudFront | `cloudflare-mcp` + `cli-anything` (`wrangler deploy`) |
| TLS / cert-manager | cert-manager + Let's Encrypt + step-ca + trust-manager | `cli-anything` (`helm install cert-manager`, `kubectl describe certificate`) + `kubernetes-mcp` |
| On-call rotation | PagerDuty / Opsgenie / Incident.io / Grafana OnCall (OSS) | `cli-anything` (provider scheduling API) + `filesystem` |
| Developer portal | Backstage (CNCF) | `cli-anything` (`npx @backstage/create-app`) + `filesystem` |
| Cost estimation in PR | Infracost GH Action | `cli-anything` (`infracost diff --format github-comment`) + `github` MCP |
| Compliance audits | OPA + Kyverno + Falco + Vanta/Drata (paid) | `cli-anything` (`conftest`, `kyverno apply`, `falco`) + `filesystem` |
| Load testing | k6 + Locust + Vegeta + xk6-disruptor | `cli-anything` (`k6 run/cloud`, `locust --headless`, `vegeta attack`) |
| K8s admission control | Kyverno (CNCF) | `cli-anything` (`kyverno apply`) + `kubernetes-mcp` |
| PaaS deployment | Vercel / Railway / Fly.io / Render / Cloudflare Pages | `cli-anything` (`vercel deploy`, `railway up`, `fly deploy`, `render deploy`) + `cloudflare-mcp` |

---

## Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Paging + on-call (PagerDuty / Opsgenie / Incident.io) | ⚠ | Paid SaaS — recipient owns account + API key. Free fallback: Grafana OnCall OSS (self-hosted) covers paging + rotation + ack/resolve. |
| Feature flags (LaunchDarkly / Statsig) | ⚠ | LaunchDarkly is paid; Statsig has free tier. Free OSS fallback: Unleash or Flagsmith (self-hosted). OpenFeature SDK abstracts the provider. |
| On-call rotation scheduling | ⚠ | PagerDuty / Opsgenie schedules need paid account. Free fallback: Grafana OnCall OSS. |
| SOC 2 evidence automation | ⚠ | Vanta / Drata / Secureframe are paid. Free OSS path: agent authors OPA + Kyverno + Falco policies; full SOC 2 packet preparation defers to a future `compliance-engineer` (v1). |
| Multi-cloud cost aggregation (Vantage / CloudHealth) | ⚠ | Paid SaaS. Free fallback: cloud-native cost APIs (AWS Cost Explorer, GCP Billing) + Infracost + OpenCost. |

**Verdict (June 2026): ~95% fulfillment.** 31 of 36 use cases are fully executable today via the bundled stack. The 5 ⚠ rows are all paid-SaaS / OAuth gates owned by the recipient. Each has a free OSS fallback that ships immediately. No genuinely impossible use cases.

---

## When to use this agent

- "Write me a multi-stage Dockerfile for a Python FastAPI service with distroless base, BuildKit cache, and Cosign signing"
- "Set up a GitHub Actions workflow that builds, scans with Trivy, signs with Cosign, generates an SBOM, and deploys to EKS via OIDC"
- "Design SLOs for our API service — 99.9% availability and 99% p99 < 200ms — and generate the Prometheus alert rules"
- "We had a SEV1 yesterday. Help me write the blameless PIR and action items"
- "Bootstrap ArgoCD App-of-Apps for our prod + staging clusters with image-updater for auto-bumps"
- "Audit our Terraform state setup — are we using a remote backend with lock and encryption?"
- "Migrate from long-lived AWS keys in GitHub secrets to OIDC federation"
- "Our cluster costs $40k/month. Help me find the top three cost-cuts (rightsize, spot, reserved)"
- "Set up cert-manager + Let's Encrypt for the prod ingress with DNS-01 challenge via Cloudflare"
- "Build a canary rollout for our checkout service with Argo Rollouts and Prometheus-based analysis"

---

## When NOT to use this agent

- **App-code language work** (Python type errors, Rust borrow checker, JS bundle errors) — hand to `senior-python-engineer` (Python) or the language-appropriate specialist.
- **Frontend build / deploy specifics** (Webpack/Vite config, Next.js ISR, browser bundle perf, web vitals) — hand to `frontend-engineer` (v1 catalog).
- **Warehouse / data pipeline tuning** (BigQuery slot allocation, Snowflake warehouse sizing, dbt models, Spark configs) — hand to `data-analyst`.
- **Customer-facing incident comms** (status page wording, customer email, support reply, post-incident customer credit calc) — hand to `customer-support-agent`. This agent writes the technical PIR; customer-support writes the customer-facing update.
- **Sales / pricing / contract / vendor negotiation** — out of scope; hand to `sales-agent` or `finance-controller`.
- **Legal / compliance certification packets** (SOC 2 audit Q&A, ISO 27001 attestation, GDPR/CCPA documentation) — this agent generates the technical evidence (OPA policies, Kyverno reports, Falco signals) and hands the packet authoring to a future `compliance-engineer` (v1).
- **Native mobile build pipelines** (Xcode iOS builds, Gradle Android signing, App Store deployment) — this agent can author CI workflows; mobile-specific certificate / provisioning-profile expertise belongs to a future `mobile-engineer` (v1).
- **Game-server / real-time multiplayer infra** (Agones, dedicated game-server scaling) — adjacent but specialized; recommend a `game-infra-engineer` (v1).
