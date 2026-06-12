# DevOps Engineer — Source Attribution

This file maps every section of `soul.md` and `role.md` back to the primary source it was derived from. It is part of the bundle but is **not** loaded into the agent's context — it exists for human verification and future updates.

This is a **v1 build** (web-research-driven). Upstream reference agents and skills were not downloaded into `reference/agents/` and `reference/skills/`; the v1 mapping pulls from the primary sources listed below. The v1 tightening pass will re-pull `wshobson/agents`, `VoltAgent/awesome-claude-code-subagents`, `msitarzewski/agency-agents`, and `vijaythecoder/awesome-claude-agents` into `reference/agents/` and `reference/skills/`. Full source URLs for every claim are in `agent.yaml → sources` and `reference/SOTA_USE_CASES.md`.

---

## soul.md → source map

| Section in soul.md | Source(s) |
|---|---|
| Opening identity paragraph + three convictions | Synthesis of Google SRE Workbook (immutability + observability), OpenGitOps Principles v1.0 (declarative state), and Google SRE Book "Eliminating Toil" chapter |
| Purpose | Synthesis from CNCF Cloud Native Definition + Google SRE chapter "What is Site Reliability Engineering?" |
| Execution stack | `reference/SOTA_USE_CASES.md` (per-use-case SOTA mapping) — every bullet maps to a row in that file with primary source URL |
| When invoked (build mode) | OpenGitOps Principles + ArgoCD operator manual |
| When invoked (incident mode) | Google SRE Book "Managing Incidents" + Incident.io operations guide |
| When invoked (review mode) | OpenGitOps Principles + GitHub Actions security hardening doc |
| When invoked (SLO mode) | Google SRE Workbook "Implementing SLOs" |
| When invoked (cost mode) | FinOps Foundation Framework + Infracost docs |
| Core operating rule: immutability | CNCF Cloud Native Definition v1.1 + Twelve-Factor App principle V (Build/Release/Run) |
| Core operating rule: GitOps default | OpenGitOps Principles v1.0 (declarative, versioned, pulled, continuously reconciled) |
| Core operating rule: pin by digest | Sigstore docs + Kubernetes pod spec reference |
| Core operating rule: runbook URL on every alert | Google SRE Workbook ch. "Alerting on SLOs" + Prometheus alerting best practices |
| Core operating rule: observability mandatory | OpenTelemetry semantic conventions + CNCF Observability Whitepaper |
| Core operating rule: secrets never in git | OWASP Cheat Sheet "Secrets Management" + HashiCorp Vault best practices |
| Core operating rule: OIDC over long-lived creds | GitHub Actions OIDC docs + AWS IAM OIDC best practices |
| Core operating rule: sign + attest | SLSA Framework v1.0 + Sigstore docs |
| Core operating rule: pre-merge cost diff | Infracost docs + FinOps Foundation policy guidance |
| Core operating rule: mitigate before diagnose | Google SRE Book "Managing Incidents" |
| Core operating rule: blameless PIR | Google SRE Book "Postmortem Culture" |
| Core operating rule: toil is a bug | Google SRE Book "Eliminating Toil" |
| Core operating rule: multi-AZ / multi-region | AWS Well-Architected Reliability Pillar + Google SRE Workbook "Setting SLOs" |
| Core operating rule: resource limits | Kubernetes docs "Resource Management for Pods and Containers" |
| Mode-specific decisions (deploy strategy) | Argo Rollouts docs (canary / blueGreen) + Martin Fowler "BlueGreenDeployment" |
| Review flag priority | OWASP DevSecOps Guideline + CIS Kubernetes Benchmark + Kyverno best practices |
| Antipatterns to flag on sight | OWASP K8s Top Ten + Kyverno policy library + CIS Docker Benchmark |
| Cost optimization order of wins | FinOps Foundation Framework + Karpenter docs + AWS cost optimization pillar |
| Quality gates | Synthesis from CIS benchmarks + SLSA Level 3 requirements + Trivy/Cosign verification recipes |
| Output format | Synthesis from incident.io PIR template + Google SRE book postmortem template |
| Communication style | Synthesis from Google SRE Book "Effective Incident Response" + Atlassian Incident Management handbook |
| When to push back (kubectl exec / cluster-admin / hardcoded secrets / state-on-disk) | Synthesis from CIS Kubernetes Benchmark + HashiCorp Vault docs + Terraform best practices |
| When to defer (sibling-agent hand-offs) | Author-synthesis based on CraftBot agent catalog + per-agent prompt seeds |
| PROACTIVE self-init footer | `METHODOLOGY.md` standard footer (verbatim across all CraftBot agents) |
| Closing rule | Restatement of the three convictions from the identity paragraph |

## role.md → source map

| Section in role.md | Source(s) |
|---|---|
| Capability reference — container engines | Docker docs + Chainguard images docs + Wolfi OS docs + GoogleContainerTools/distroless README |
| Capability reference — Kubernetes distributions + tools | CNCF Landscape (filtered: containers / scheduling) + Talos Linux docs |
| Capability reference — GitOps + progressive delivery | ArgoCD docs + Flux docs + Argo Rollouts docs + OpenFeature docs |
| Capability reference — IaC | OpenTofu docs + Pulumi docs + AWS CDK docs + SST docs + Crossplane docs |
| Capability reference — Secrets | Vault docs + ESO docs + OpenBao docs + Pulumi ESC docs |
| Capability reference — CI/CD platforms | GitHub Actions docs + Tekton docs + Argo Workflows docs + Earthly docs + Dagger docs |
| Capability reference — Observability stack | OpenTelemetry docs + Honeycomb docs + Datadog docs + Grafana docs + Vector docs |
| Capability reference — Incident response platforms | PagerDuty + Opsgenie + Incident.io + Rootly + FireHydrant + Grafana OnCall docs |
| Capability reference — Cloud providers / PaaS | AWS/GCP/Azure/Cloudflare/Vercel/Railway/Fly.io/Render official docs |
| Capability reference — Security / supply chain | Trivy docs + Sigstore docs + SLSA framework + in-toto spec + Falco docs + Kyverno docs + Cilium docs |
| Capability reference — Cost / FinOps | FinOps Foundation Framework + Infracost docs + OpenCost docs + Karpenter docs |
| Capability reference — Developer portals | Backstage docs + Port docs + Cortex docs + OpsLevel docs |
| Capability reference — Network mesh + ingress | CNCF Landscape (filtered: networking) + Istio/Linkerd/Cilium docs |
| Antipattern catalog — mutable image tag | Kubernetes docs "Container Images" + Sigstore docs |
| Antipattern catalog — kubectl apply from laptop | OpenGitOps Principles + ArgoCD docs |
| Antipattern catalog — secret in git | HashiCorp Vault docs + ESO docs + OWASP Cheat Sheet "Secrets Management" |
| Antipattern catalog — cluster-admin for SA | Kubernetes RBAC docs + CIS Kubernetes Benchmark v1.9 |
| Antipattern catalog — missing resource limits | Kubernetes docs "Resource Management for Pods and Containers" |
| Antipattern catalog — local Terraform state | OpenTofu docs "Backend Configuration" + Terraform best practices |
| Antipattern catalog — long-lived AWS creds | GitHub Actions OIDC docs + AWS IAM OIDC federation guide |
| Antipattern catalog — alert without runbook | Prometheus alerting best practices + Google SRE Workbook ch. "Alerting on SLOs" |
| Common fixes summary table | Synthesis from the antipattern entries above |
| Incident response playbook — severity matrix | Google SRE Book "Managing Incidents" + PagerDuty severity guide |
| Incident response playbook — SEV1 flow | Google SRE Book "Managing Incidents" + Atlassian Incident Management handbook |
| Incident response playbook — diagnosis order | Google SRE Book "Effective Troubleshooting" |
| Incident response playbook — PIR template | Google SRE Book "Postmortem Culture" + Incident.io postmortem template |
| SLO design playbook — define SLI / set SLO | Google SRE Workbook "Implementing SLOs" |
| SLO design playbook — Sloth YAML | Sloth docs (https://sloth.dev/) + Pyrra docs |
| SLO design playbook — multi-window multi-burn-rate alerts | Google SRE Workbook "Alerting on SLOs" |
| SLO design playbook — error budget policy | Google SRE Workbook "Implementing SLOs" + Google SRE Book "Embracing Risk" |
| Kubernetes manifest reference — production-grade Deployment | Kubernetes docs + CIS Kubernetes Benchmark + bjw-s/common library chart patterns |
| Kubernetes manifest reference — NetworkPolicy | Kubernetes docs "Network Policies" + Calico docs |
| SOTA tool reference — every H3 (docker buildx through k9s) | Per-tool official docs (URLs in agent.yaml sources + reference/SOTA_USE_CASES.md per-row source field) |
| SOTA execution playbook table | Synthesis from `reference/SOTA_USE_CASES.md` "Recommended agent.yaml additions" |
| Brief templates — Dockerfile | Docker BuildKit docs + Chainguard images + GoogleContainerTools/distroless examples |
| Brief templates — GitHub Actions workflow | GitHub Actions OIDC docs + Sigstore cosign-installer action + Trivy aquasecurity/trivy-action |
| Brief templates — Runbook template | Google SRE Book "Service Best Practices" + Atlassian Incident Management runbook examples |
| Closing rules | Restatement of soul.md three convictions |

---

## Notes on authored-from-synthesis

The following sections in soul.md and role.md are operational glue (not domain claims). They are short and connect lifted sections from primary sources:

- **soul.md "When to push back / When to defer"** — sibling-agent hand-offs are author-synthesized from the CraftBot agent catalog (the seven sibling agents currently in `agents/` + the per-agent prompt seeds for v1 catalog adds). Not lifted from any single source.
- **soul.md Purpose** — distillation of the per-agent prompt one-line role, not lifted verbatim.
- **role.md "Antipattern catalog" Why-it's-bad / Why-it's-better commentary** — short prose framing around the BAD/GOOD code pairs. The code patterns themselves are lifted from primary docs (Kubernetes, Sigstore, OpenTofu).
- **role.md "Common fixes summary" table** — author-distillation of the antipattern catalog above. No new claims.
- **role.md "SOTA execution playbook" table** — author-distillation of `reference/SOTA_USE_CASES.md` "Recommended skill packs" section.

Each above is operational glue, not a domain claim. They are not adding new SOTA assertions; they're packaging the lifted material for the agent's grep workflow.

---

## How to update this agent

If you want to refresh content from upstream:

1. Re-fetch SOTA tool docs listed in `reference/SOTA_USE_CASES.md` per-row Source field; update confidence ratings if the tool changes (e.g., new CNCF graduation, new SaaS pricing tier, deprecation).
2. Re-pull `wshobson/agents` + `VoltAgent/awesome-claude-code-subagents` + `msitarzewski/agency-agents` + `vijaythecoder/awesome-claude-agents` into `reference/agents/` and `reference/skills/` for v1 tightening pass.
3. Diff against the previous versions to see what changed.
4. Update the corresponding sections of `soul.md` and `role.md` to match.
5. Update this `SOURCES.md` if section names or source URLs changed.
6. Re-run `python verify.py devops-engineer` (verifies structure) then `python build.py devops-engineer` (produces `dist/devops-engineer.craftbot`).

Because the SOTA tool sources are listed by URL, this update path is mechanical and traceable.

---

## SOTA tool sources (June 2026)

Per-tool source table for the 2026 SOTA stack. Every tool listed here will ship
with a dedicated SKILL.md under `skills/` (created in Round 2) and is referenced from role.md
under `## SOTA tool reference (June 2026)`.

### Containers

| Tool | Source | Skill pack |
|---|---|---|
| Docker BuildKit | https://docs.docker.com/build/buildkit/ | `docker-multistage-buildkit-distroless` |
| Chainguard Images | https://github.com/chainguard-images/images | `docker-multistage-buildkit-distroless` |
| Wolfi OS | https://wolfi.dev/ | `docker-multistage-buildkit-distroless` |
| GoogleContainerTools/distroless | https://github.com/GoogleContainerTools/distroless | `docker-multistage-buildkit-distroless` |
| Podman | https://podman.io/docs | role.md SOTA section |
| Buildah | https://buildah.io/ | role.md SOTA section |

### Kubernetes

| Tool | Source | Skill pack |
|---|---|---|
| kubectl | https://kubernetes.io/docs/reference/kubectl/ | `kubernetes-deployments-helm-kustomize` |
| Helm 3 | https://helm.sh/docs/ | `kubernetes-deployments-helm-kustomize` |
| Kustomize | https://kustomize.io/ · https://kubectl.docs.kubernetes.io/references/kustomize/ | `kubernetes-deployments-helm-kustomize` |
| kubeconform | https://github.com/yannh/kubeconform | `kubernetes-deployments-helm-kustomize` |
| k9s | https://k9scli.io/ | role.md SOTA section |
| Talos Linux | https://www.talos.dev/ | role.md SOTA section |
| Velero | https://velero.io/ | `kubernetes-deployments-helm-kustomize` (DR subsection) |
| Kyverno | https://kyverno.io/docs/ | `kubernetes-deployments-helm-kustomize` (policy subsection) |
| vCluster | https://www.vcluster.com/ | `kubernetes-deployments-helm-kustomize` |

### IaC

| Tool | Source | Skill pack |
|---|---|---|
| OpenTofu | https://opentofu.org/docs/ | `terraform-opentofu-iac` |
| Terraform | https://developer.hashicorp.com/terraform/docs | `terraform-opentofu-iac` |
| tflint | https://github.com/terraform-linters/tflint | `terraform-opentofu-iac` |
| terraform-docs | https://terraform-docs.io/ | `terraform-opentofu-iac` |
| checkov | https://www.checkov.io/ | `terraform-opentofu-iac` |
| tfsec | https://github.com/aquasecurity/tfsec | `terraform-opentofu-iac` |
| Infracost | https://www.infracost.io/docs/ | `terraform-opentofu-iac`, `cost-optimization-finops-infracost` |
| Atlantis | https://www.runatlantis.io/ | `terraform-opentofu-iac` |
| Pulumi | https://www.pulumi.com/docs/ | `pulumi-iac-python-typescript` |
| Pulumi ESC | https://www.pulumi.com/docs/pulumi-cloud/esc/ | `pulumi-iac-python-typescript`, `vault-doppler-pulumi-esc-secrets` |
| AWS CDK | https://docs.aws.amazon.com/cdk/ | `aws-cdk-sst-serverless` |
| SST | https://sst.dev/docs/ | `aws-cdk-sst-serverless` |
| AWS SAM | https://docs.aws.amazon.com/serverless-application-model/ | `aws-cdk-sst-serverless` |
| Crossplane | https://www.crossplane.io/ | role.md SOTA section |

### GitOps + progressive delivery

| Tool | Source | Skill pack |
|---|---|---|
| ArgoCD | https://argo-cd.readthedocs.io/ | `argocd-flux-gitops` |
| Flux v2 | https://fluxcd.io/flux/ | `argocd-flux-gitops` |
| argocd-image-updater | https://argocd-image-updater.readthedocs.io/ | `argocd-flux-gitops` |
| Argo Rollouts | https://argo-rollouts.readthedocs.io/ | `blue-green-canary-argo-rollouts` |
| Flagger | https://docs.flagger.app/ | `blue-green-canary-argo-rollouts` |
| OpenFeature | https://openfeature.dev/ | `feature-flags-launchdarkly-statsig` |
| LaunchDarkly | https://docs.launchdarkly.com/ | `feature-flags-launchdarkly-statsig` |
| Statsig | https://docs.statsig.com/ | `feature-flags-launchdarkly-statsig` |
| Unleash | https://docs.getunleash.io/ | `feature-flags-launchdarkly-statsig` |
| Flagsmith | https://docs.flagsmith.com/ | `feature-flags-launchdarkly-statsig` |
| OpenGitOps Principles | https://opengitops.dev/ | `argocd-flux-gitops`, soul.md core rule |

### CI/CD

| Tool | Source | Skill pack |
|---|---|---|
| GitHub Actions | https://docs.github.com/en/actions | `github-actions-cicd-oidc` |
| GitHub Actions OIDC | https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services | `github-actions-cicd-oidc` |
| actionlint | https://github.com/rhysd/actionlint | `github-actions-cicd-oidc` |
| act | https://github.com/nektos/act | `github-actions-cicd-oidc` |
| Earthly | https://earthly.dev/ | role.md SOTA section |
| Dagger | https://dagger.io/ | role.md SOTA section |
| Tekton | https://tekton.dev/ | role.md SOTA section |
| Argo Workflows | https://argoproj.github.io/workflows/ | role.md SOTA section |

### Secrets

| Tool | Source | Skill pack |
|---|---|---|
| HashiCorp Vault | https://www.vaultproject.io/docs · https://developer.hashicorp.com/vault/docs | `vault-doppler-pulumi-esc-secrets` |
| OpenBao | https://openbao.org/ | `vault-doppler-pulumi-esc-secrets` |
| External Secrets Operator | https://external-secrets.io/ | `external-secrets-operator-k8s` |
| Doppler | https://docs.doppler.com/ | `vault-doppler-pulumi-esc-secrets` |
| Infisical | https://infisical.com/docs/ | `vault-doppler-pulumi-esc-secrets` |
| Sealed Secrets | https://github.com/bitnami-labs/sealed-secrets | `external-secrets-operator-k8s` |
| SOPS | https://github.com/getsops/sops | `external-secrets-operator-k8s` |
| gitleaks | https://github.com/gitleaks/gitleaks | `vault-doppler-pulumi-esc-secrets` (pre-commit subsection) |
| trufflehog | https://github.com/trufflesecurity/trufflehog | `vault-doppler-pulumi-esc-secrets` |

### Container security + supply chain

| Tool | Source | Skill pack |
|---|---|---|
| Trivy | https://aquasecurity.github.io/trivy/ | `trivy-snyk-container-scanning` |
| Snyk | https://docs.snyk.io/scan-using-snyk/snyk-container | `trivy-snyk-container-scanning` |
| Grype | https://github.com/anchore/grype | `trivy-snyk-container-scanning` |
| Syft | https://github.com/anchore/syft | `sigstore-slsa-supply-chain-attestation` |
| Cosign (Sigstore) | https://docs.sigstore.dev/cosign/ | `sigstore-slsa-supply-chain-attestation` |
| Fulcio (Sigstore CA) | https://docs.sigstore.dev/fulcio/overview/ | `sigstore-slsa-supply-chain-attestation` |
| Rekor (Sigstore transparency log) | https://docs.sigstore.dev/rekor/overview/ | `sigstore-slsa-supply-chain-attestation` |
| SLSA framework | https://slsa.dev/spec/v1.0/levels | `sigstore-slsa-supply-chain-attestation` |
| slsa-github-generator | https://github.com/slsa-framework/slsa-github-generator | `sigstore-slsa-supply-chain-attestation` |
| in-toto | https://in-toto.io/ | `sigstore-slsa-supply-chain-attestation` |
| OPA / Conftest | https://www.openpolicyagent.org/docs | role.md SOTA section |
| Falco | https://falco.org/docs/ | role.md SOTA section |
| Cilium / Tetragon | https://cilium.io/ · https://tetragon.io/ | role.md SOTA section |

### Observability

| Tool | Source | Skill pack |
|---|---|---|
| OpenTelemetry | https://opentelemetry.io/docs/ | `opentelemetry-instrumentation` |
| OTel Collector | https://opentelemetry.io/docs/collector/ | `opentelemetry-instrumentation` |
| OTel Operator (K8s auto-injection) | https://github.com/open-telemetry/opentelemetry-operator | `opentelemetry-instrumentation` |
| Honeycomb | https://docs.honeycomb.io/getting-data-in/opentelemetry/ | `honeycomb-datadog-observability` |
| Datadog | https://docs.datadoghq.com/opentelemetry/ | `honeycomb-datadog-observability` |
| Grafana Cloud | https://grafana.com/oss/opentelemetry/ | `honeycomb-datadog-observability` |
| Sentry | https://docs.sentry.io/ | `pagerduty-incident-io-incident-response` (error correlation subsection) |
| kube-prometheus-stack | https://github.com/prometheus-operator/kube-prometheus | `prometheus-grafana-loki-tempo-self-hosted` |
| Prometheus | https://prometheus.io/docs/ | `prometheus-grafana-loki-tempo-self-hosted` |
| Loki | https://grafana.com/oss/loki/ | `prometheus-grafana-loki-tempo-self-hosted` |
| Tempo | https://grafana.com/oss/tempo/ | `prometheus-grafana-loki-tempo-self-hosted` |
| Mimir | https://grafana.com/oss/mimir/ | `prometheus-grafana-loki-tempo-self-hosted` |
| Pyroscope | https://pyroscope.io/ | `prometheus-grafana-loki-tempo-self-hosted` |
| Vector | https://vector.dev/ | `prometheus-grafana-loki-tempo-self-hosted` |

### SLOs

| Tool | Source | Skill pack |
|---|---|---|
| Google SRE Workbook | https://sre.google/workbook/implementing-slos/ | `slos-error-budgets-google-sre` |
| Sloth | https://sloth.dev/ | `slos-error-budgets-google-sre` |
| Pyrra | https://github.com/pyrra-dev/pyrra | `slos-error-budgets-google-sre` |
| Nobl9 | https://www.nobl9.com/ | `slos-error-budgets-google-sre` |

### Incident response

| Tool | Source | Skill pack |
|---|---|---|
| Google SRE — Managing Incidents | https://sre.google/sre-book/managing-incidents/ | `pagerduty-incident-io-incident-response` |
| Google SRE — Postmortem Culture | https://sre.google/sre-book/postmortem-culture/ | `pagerduty-incident-io-incident-response` |
| PagerDuty | https://developer.pagerduty.com/api-reference/ | `pagerduty-incident-io-incident-response` |
| Opsgenie | https://docs.opsgenie.com/ | `pagerduty-incident-io-incident-response` |
| Incident.io | https://incident.io/ | `pagerduty-incident-io-incident-response` |
| Rootly | https://rootly.com/ | `pagerduty-incident-io-incident-response` |
| FireHydrant | https://firehydrant.com/ | `pagerduty-incident-io-incident-response` |
| Better Stack | https://betterstack.com/ | `pagerduty-incident-io-incident-response` |
| Grafana OnCall | https://grafana.com/products/oncall/ | `pagerduty-incident-io-incident-response` |
| Howie.ai | https://howie.ai/ | `pagerduty-incident-io-incident-response` |
| Atlassian Statuspage | https://www.atlassian.com/software/statuspage | `pagerduty-incident-io-incident-response` |

### DNS / CDN / PaaS

| Tool | Source | Skill pack |
|---|---|---|
| Cloudflare | https://developers.cloudflare.com/ | `cloudflare-vercel-railway-fly-render-paas` |
| Fastly | https://docs.fastly.com/ | `cloudflare-vercel-railway-fly-render-paas` |
| Vercel | https://vercel.com/docs | `cloudflare-vercel-railway-fly-render-paas` |
| Railway | https://docs.railway.com/ | `cloudflare-vercel-railway-fly-render-paas` |
| Fly.io | https://fly.io/docs/ | `cloudflare-vercel-railway-fly-render-paas` |
| Render | https://render.com/docs | `cloudflare-vercel-railway-fly-render-paas` |
| cert-manager | https://cert-manager.io/docs/ | `cert-manager-acme-tls` |
| step-ca | https://smallstep.com/docs/step-ca/ | `cert-manager-acme-tls` |
| trust-manager | https://cert-manager.io/docs/trust/trust-manager/ | `cert-manager-acme-tls` |
| Let's Encrypt | https://letsencrypt.org/docs/ | `cert-manager-acme-tls` |
| Wrangler (Cloudflare) | https://developers.cloudflare.com/workers/wrangler/ | `cloudflare-vercel-railway-fly-render-paas` |

### Cost / FinOps

| Tool | Source | Skill pack |
|---|---|---|
| FinOps Foundation Framework | https://www.finops.org/framework/ | `cost-optimization-finops-infracost` |
| Infracost | https://www.infracost.io/docs/ | `cost-optimization-finops-infracost` |
| OpenCost | https://www.opencost.io/ | `cost-optimization-finops-infracost` |
| Karpenter | https://karpenter.sh/ | `cost-optimization-finops-infracost` |
| Goldilocks (Fairwinds) | https://goldilocks.fairwinds.com/ | `cost-optimization-finops-infracost` |
| FOCUS spec | https://focus.finops.org/ | `cost-optimization-finops-infracost` |
| Vantage | https://www.vantage.sh/ | role.md SOTA section |
| CloudHealth | https://www.vmware.com/products/cloudhealth.html | role.md SOTA section |

### Developer portal

| Tool | Source | Skill pack |
|---|---|---|
| Backstage (Spotify) | https://backstage.io/docs | `backstage-developer-portal` |
| Port | https://www.getport.io/ | `backstage-developer-portal` |
| Cortex | https://www.cortex.io/ | `backstage-developer-portal` |
| OpsLevel | https://www.opslevel.com/ | `backstage-developer-portal` |
| Roadie | https://roadie.io/ | `backstage-developer-portal` |

### Load testing

| Tool | Source | Skill pack |
|---|---|---|
| k6 (Grafana) | https://k6.io/docs/ | role.md SOTA section |
| Locust | https://docs.locust.io/ | role.md SOTA section |
| Vegeta | https://github.com/tsenart/vegeta | role.md SOTA section |
| xk6-disruptor | https://k6.io/docs/javascript-api/xk6-disruptor/ | role.md SOTA section |

### DB migration

| Tool | Source | Skill pack |
|---|---|---|
| Atlas | https://atlasgo.io/ | role.md SOTA section + handoff to senior-python-engineer |
| Liquibase | https://docs.liquibase.com/ | role.md SOTA section |
| WAL-G | https://github.com/wal-g/wal-g | role.md SOTA section |
| Velero | https://velero.io/ | `kubernetes-deployments-helm-kustomize` DR subsection |

### Compliance + policy

| Tool | Source | Skill pack |
|---|---|---|
| OPA / Conftest | https://www.openpolicyagent.org/docs · https://www.conftest.dev/ | role.md SOTA section |
| Kyverno | https://kyverno.io/docs/ | `kubernetes-deployments-helm-kustomize` policy subsection |
| Falco | https://falco.org/docs/ | role.md SOTA section |
| Vanta | https://www.vanta.com/ | USE_CASES.md caveat |
| Drata | https://drata.com/ | USE_CASES.md caveat |
| Secureframe | https://secureframe.com/ | USE_CASES.md caveat |
| CIS Kubernetes Benchmark | https://www.cisecurity.org/benchmark/kubernetes | role.md SOTA section |
| OWASP DevSecOps Guideline | https://owasp.org/www-project-devsecops-guideline/ | soul.md core rule |
| OWASP Cheat Sheets | https://cheatsheetseries.owasp.org/ | role.md SOTA section |

### Skill pack inventory (bundled — 22 total)

| Skill pack | Tools covered |
|---|---|
| `docker-multistage-buildkit-distroless` | Docker BuildKit, Chainguard, Wolfi, distroless |
| `kubernetes-deployments-helm-kustomize` | kubectl, Helm 3, Kustomize, kubeconform, Kyverno, Velero, vCluster |
| `terraform-opentofu-iac` | OpenTofu 1.8, Terraform 1.9, tflint, checkov, infracost, terraform-docs, Atlantis |
| `pulumi-iac-python-typescript` | Pulumi 3.x, Pulumi ESC |
| `aws-cdk-sst-serverless` | AWS CDK 2.x, SST v3, AWS SAM |
| `github-actions-cicd-oidc` | GitHub Actions, OIDC, reusable workflows, actionlint, act |
| `argocd-flux-gitops` | ArgoCD, Flux v2, ApplicationSets, image-updater |
| `vault-doppler-pulumi-esc-secrets` | Vault, OpenBao, Doppler, Pulumi ESC, Infisical, gitleaks, trufflehog |
| `external-secrets-operator-k8s` | ESO, Sealed Secrets, SOPS |
| `opentelemetry-instrumentation` | OTel SDK, Collector, OTel Operator, semantic conventions |
| `honeycomb-datadog-observability` | Honeycomb, Datadog, Grafana Cloud — backend-specific OTel recipes |
| `prometheus-grafana-loki-tempo-self-hosted` | kube-prometheus-stack, Prometheus, Grafana, Loki, Tempo, Mimir, Pyroscope, Vector |
| `slos-error-budgets-google-sre` | Sloth, Pyrra, Nobl9, Google SRE Workbook |
| `pagerduty-incident-io-incident-response` | PagerDuty, Opsgenie, Incident.io, Rootly, FireHydrant, Grafana OnCall, Howie.ai, Statuspage, Better Stack |
| `blue-green-canary-argo-rollouts` | Argo Rollouts, Flagger |
| `feature-flags-launchdarkly-statsig` | OpenFeature, LaunchDarkly, Statsig, Unleash, Flagsmith |
| `trivy-snyk-container-scanning` | Trivy, Snyk, Grype |
| `sigstore-slsa-supply-chain-attestation` | Cosign, Fulcio, Rekor, Syft, SLSA framework, in-toto, slsa-github-generator |
| `cloudflare-vercel-railway-fly-render-paas` | Cloudflare, Fastly, Vercel, Railway, Fly.io, Render, Wrangler |
| `cost-optimization-finops-infracost` | Infracost, OpenCost, Karpenter, Goldilocks, FOCUS spec, Vantage |
| `cert-manager-acme-tls` | cert-manager, Let's Encrypt, step-ca, trust-manager |
| `backstage-developer-portal` | Spotify Backstage, Port, Cortex, OpsLevel, Roadie |
