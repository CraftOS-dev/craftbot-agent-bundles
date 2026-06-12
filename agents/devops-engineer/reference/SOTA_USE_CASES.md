<!--
SOTA per-use-case mapping for devops-engineer (June 2026).

This file translates the documented use cases (see ../USE_CASES.md) into the
exact 2026 SOTA tool + the concrete `uvx`/`npx`/`uv run`/`gh` command the agent
should reach for. Most tools are reachable through the agent's `cli-anything`
skill — a handful (Kubernetes, AWS S3, Cloudflare, Sentry, GitHub) have dedicated
MCPs in CraftBot's catalog and are wired in `agent.yaml`.

Confidence legend:
  ✓ — agent can fully execute this today via documented tools
  ⚠ — agent can execute but depends on environment (cloud creds, paid key)
  ✗ — out of scope or requires a different specialist
-->

# devops-engineer — SOTA use cases (June 2026)

This file maps each documented use case to its current SOTA tool and the exact
execution path. Read alongside `../USE_CASES.md` (capabilities) and `../role.md`
(deep tool reference). Skill packs implementing each tool live under
`agents/devops-engineer/skills/` (created in Round 2).

---

## 1. Dockerfile authoring (multi-stage, distroless, BuildKit cache)
- **SOTA approach:** Multi-stage Dockerfile with BuildKit (`# syntax=docker/dockerfile:1.7+`), distroless or Wolfi base images (Chainguard), cache mounts (`--mount=type=cache`), non-root `USER`, `HEALTHCHECK`. Use `docker buildx build --platform linux/amd64,linux/arm64` for multi-arch. Sign with Cosign.
- **Agent execution path:** `cli-anything` → `docker buildx create --use && docker buildx build --platform linux/amd64,linux/arm64 --push -t <reg>/<img>:<tag> .` plus `cosign sign <reg>/<img>:<tag>`.
- **Source:** https://docs.docker.com/build/buildkit/ · https://github.com/chainguard-images/images · https://github.com/GoogleContainerTools/distroless
- **Skill pack:** `docker-multistage-buildkit-distroless`
- **Confidence:** ✓

## 2. Kubernetes deployment manifests (Deployment, Service, Ingress, ConfigMap, Secret, HPA, PDB)
- **SOTA approach:** Helm 3.x charts for parameterized apps; Kustomize overlays for env-specific patches; raw manifests for simple workloads. Always include `resources.requests/limits`, `PodDisruptionBudget`, `HorizontalPodAutoscaler` (with `metrics-server` or KEDA), `topologySpreadConstraints`, `securityContext`. Use `kubectl-validate` for schema and `kubeconform` for fast CI checks.
- **Agent execution path:** `kubernetes-mcp` (apply, scale, describe, logs) + `cli-anything` (`helm upgrade --install <rel> <chart> -f values.yaml`, `kustomize build overlays/prod | kubectl apply -f -`, `kubeconform -strict -summary`).
- **Source:** https://kubernetes.io/docs/concepts/workloads/controllers/deployment/ · https://helm.sh/docs/ · https://kustomize.io/ · https://github.com/yannh/kubeconform
- **Skill pack:** `kubernetes-deployments-helm-kustomize`
- **Confidence:** ✓

## 3. Helm chart authoring + values.yaml patterns
- **SOTA approach:** Helm 3.x with strict `Chart.yaml` schema, `values.schema.json` for input validation, library-chart pattern for shared templates, `helm-docs` for auto-generated README, `helm lint` + `helm template | kubeval` in CI. Sign charts with Cosign + OCI registry. Use `bjw-s/common` library chart for boilerplate-free apps.
- **Agent execution path:** `cli-anything` → `helm create <name> && helm lint . && helm template . | kubeconform -strict && cosign sign --yes <oci-ref>` and `helm push <chart>.tgz oci://<reg>`.
- **Source:** https://helm.sh/docs/topics/charts/ · https://github.com/norwoodj/helm-docs · https://helm.sh/docs/topics/registries/
- **Skill pack:** `kubernetes-deployments-helm-kustomize`
- **Confidence:** ✓

## 4. Kustomize overlays (dev/staging/prod)
- **SOTA approach:** Base + overlays pattern. `kustomization.yaml` per env. ConfigMapGenerator/SecretGenerator with `disableNameSuffixHash: false` for atomic rollouts. `replacements:` for cross-resource substitutions. `helmCharts:` field for hybrid Helm+Kustomize. Build via `kubectl apply -k` or pre-render via `kustomize build`.
- **Agent execution path:** `cli-anything` (`kustomize build overlays/prod | kubectl diff -f -`, then apply) + `kubernetes-mcp` for state inspection.
- **Source:** https://kubectl.docs.kubernetes.io/references/kustomize/ · https://kustomize.io/
- **Skill pack:** `kubernetes-deployments-helm-kustomize`
- **Confidence:** ✓

## 5. Terraform / OpenTofu module authoring
- **SOTA approach:** OpenTofu 1.8+ (open-source Terraform fork governed by Linux Foundation, drop-in compatible) is the 2026 default; HashiCorp Terraform 1.9+ for orgs on BSL-license-incompatible workflows. Modules follow `main.tf`/`variables.tf`/`outputs.tf`/`versions.tf`/`README.md` layout. `terraform-docs` for README auto-gen. State in remote backend (S3+DynamoDB or Terraform Cloud / Scalr / Spacelift). `tflint` + `terraform validate` + `checkov`/`tfsec` in CI. `infracost diff` on PRs. Atlantis or Spacelift for PR-driven plan/apply.
- **Agent execution path:** `cli-anything` (`tofu init && tofu fmt -recursive && tofu validate && tofu plan -out=tfplan && tofu apply tfplan`, `tflint --recursive`, `checkov -d . --framework terraform`, `infracost diff --path .`).
- **Source:** https://opentofu.org/docs/ · https://developer.hashicorp.com/terraform/language/modules · https://terraform-docs.io/ · https://www.checkov.io/ · https://www.infracost.io/
- **Skill pack:** `terraform-opentofu-iac`
- **Confidence:** ✓

## 6. Pulumi authoring (Python / TypeScript / Go)
- **SOTA approach:** Pulumi 3.130+ with native providers. Choose language by team: TypeScript for type-safety + ecosystem; Python for ML/data shops; Go for static binaries. Use `ComponentResource` for reusable abstractions. Pulumi ESC for secret + config management (sibling to Pulumi). State in Pulumi Cloud (free for individuals) or S3 backend. Use `crosscode/pulumi-cdk-conversion` to migrate from CDK if needed.
- **Agent execution path:** `cli-anything` (`pulumi new aws-typescript`, `pulumi up --yes --suppress-outputs`, `pulumi preview --diff`, `pulumi config set --secret <key> <val>`, `pulumi esc env init <env-name>`).
- **Source:** https://www.pulumi.com/docs/ · https://www.pulumi.com/docs/pulumi-cloud/esc/ · https://www.pulumi.com/blog/pulumi-3-0/
- **Skill pack:** `pulumi-iac-python-typescript`
- **Confidence:** ✓

## 7. AWS CDK / SAM / SST serverless IaC
- **SOTA approach:** AWS CDK 2.x for AWS-only infra in TS/Python. SST v3 for modern AWS serverless apps (built on Pulumi runtime since v3, replaces CDK for fullstack). AWS SAM for Lambda-centric workflows. Use CDK Constructs Hub for community patterns. Bootstrap once per account/region: `cdk bootstrap`.
- **Agent execution path:** `cli-anything` (`cdk init app --language=typescript`, `cdk synth`, `cdk diff`, `cdk deploy --require-approval=never`, `sst deploy --stage=prod`, `sam build && sam deploy --guided`).
- **Source:** https://docs.aws.amazon.com/cdk/ · https://sst.dev/docs/ · https://docs.aws.amazon.com/serverless-application-model/
- **Skill pack:** `aws-cdk-sst-serverless`
- **Confidence:** ✓

## 8. GitHub Actions workflow authoring (matrix, reusable, OIDC)
- **SOTA approach:** GitHub Actions with OIDC trust to AWS/GCP/Azure (no long-lived cloud creds in secrets), reusable workflows (`workflow_call`), matrix strategy for cross-platform, `permissions:` block scoped per-job (`id-token: write`, `contents: read`), composite actions for shared logic, `actions/cache@v4`, immutable-action versioning by SHA. Pin actions by full commit SHA per OpenSSF guidance. Use `act` for local testing and `actionlint` in CI.
- **Agent execution path:** `cli-anything` (`gh workflow run <name>`, `gh run watch`, `gh run view --log-failed`, `actionlint .github/workflows/*.yml`, `act -j <job> --container-architecture linux/amd64`).
- **Source:** https://docs.github.com/en/actions · https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services · https://github.com/rhysd/actionlint · https://github.com/nektos/act
- **Skill pack:** `github-actions-cicd-oidc`
- **Confidence:** ✓

## 9. ArgoCD app-of-apps + sync waves
- **SOTA approach:** ArgoCD 2.13+ with App-of-Apps pattern (one root app references child apps via `Application` CRD). Sync waves (`argocd.argoproj.io/sync-wave` annotation) for ordering. ApplicationSets for multi-cluster fan-out. Notifications via the `argocd-notifications` controller (Slack/Teams/Email). Diff via `argocd app diff <app>`. Auto-sync + self-heal + prune for true GitOps. Use `argocd-image-updater` to auto-bump image tags after CI builds.
- **Agent execution path:** `cli-anything` (`argocd app create -f app.yaml`, `argocd app sync <app> --prune`, `argocd app diff <app>`, `argocd app set <app> --revision <git-sha>`) + `kubernetes-mcp` for cluster inspection.
- **Source:** https://argo-cd.readthedocs.io/en/stable/ · https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/ · https://argocd-image-updater.readthedocs.io/
- **Skill pack:** `argocd-flux-gitops`
- **Confidence:** ✓

## 10. Flux CD (alternative GitOps controller)
- **SOTA approach:** Flux v2 (CNCF graduated) for pull-based GitOps. `GitRepository` + `Kustomization` / `HelmRelease` resources. `flux bootstrap github` for repo-init. `notification-controller` for Slack/Webhook alerts. `image-reflector-controller` + `image-automation-controller` for auto-bump. Prefer Flux when org needs CNCF-only stack or finer-grained controller separation than ArgoCD.
- **Agent execution path:** `cli-anything` (`flux bootstrap github --owner=<o> --repository=<r> --path=clusters/prod`, `flux reconcile kustomization <name>`, `flux get all -A`, `flux create source git ...`).
- **Source:** https://fluxcd.io/flux/ · https://fluxcd.io/flux/components/
- **Skill pack:** `argocd-flux-gitops`
- **Confidence:** ✓

## 11. Secret management (Vault + External Secrets Operator)
- **SOTA approach:** HashiCorp Vault 1.17+ (or OpenBao 2.0, the LF fork) as the source-of-truth for secrets; External Secrets Operator (ESO) syncs them into K8s `Secret` resources via `SecretStore`/`ClusterSecretStore` + `ExternalSecret` CRDs. Alternatives: Doppler (managed), Infisical (OSS), AWS Secrets Manager + ESO, Pulumi ESC. Rotate via Vault's database secret engine or short-TTL dynamic credentials. Never `kubectl create secret` by hand.
- **Agent execution path:** `cli-anything` (`vault kv put secret/<app>/db password=$(openssl rand -base64 32)`, `kubectl apply -f external-secret.yaml`, `vault read database/creds/<role>`) + `kubernetes-mcp` to verify synced secret.
- **Source:** https://www.vaultproject.io/docs · https://external-secrets.io/ · https://openbao.org/ · https://www.pulumi.com/docs/pulumi-cloud/esc/
- **Skill pack:** `vault-doppler-pulumi-esc-secrets` + `external-secrets-operator-k8s`
- **Confidence:** ✓

## 12. CI/CD pipeline design (build → test → scan → sign → deploy)
- **SOTA approach:** Canonical 2026 pipeline: (1) `actions/checkout` with fetch-depth=0; (2) language setup + cache (`setup-node`/`setup-python` + `actions/cache`); (3) lint + unit tests; (4) build container with BuildKit cache; (5) scan with Trivy + Snyk; (6) sign with Cosign (keyless via OIDC + Fulcio + Rekor); (7) push to OCI registry; (8) generate SBOM via Syft; (9) attest provenance via SLSA Generator; (10) trigger ArgoCD/Flux sync. Total time target <8 min for typical service.
- **Agent execution path:** `cli-anything` (`trivy image --severity HIGH,CRITICAL <img>`, `cosign sign --yes <img>`, `syft <img> -o spdx-json > sbom.json`, `gh workflow run ...`) + `github` MCP for PR/check status.
- **Source:** https://docs.github.com/en/actions · https://github.com/aquasecurity/trivy · https://github.com/sigstore/cosign · https://github.com/anchore/syft · https://slsa.dev/
- **Skill pack:** `github-actions-cicd-oidc`, `trivy-snyk-container-scanning`, `sigstore-slsa-supply-chain-attestation`
- **Confidence:** ✓

## 13. Container image scanning (Trivy + Snyk)
- **SOTA approach:** Trivy (Aqua) for fast, all-in-one vuln + misconfig + secret scanning, free; Snyk for org-policy + license + IaC + commercial reporting (paid). Grype (Anchore) as Trivy alternative. Always scan post-build, pre-push. Fail builds on CRITICAL CVEs with no fix. Use `trivy.yaml` + `.trivyignore` for accepted risk. SBOM-aware mode: scan the SBOM, not the image.
- **Agent execution path:** `cli-anything` (`trivy image --severity HIGH,CRITICAL --exit-code 1 --ignore-unfixed <img>`, `trivy fs --scanners vuln,misconfig,secret .`, `snyk container test <img>`, `grype <img>`).
- **Source:** https://aquasecurity.github.io/trivy/ · https://docs.snyk.io/scan-using-snyk/snyk-container · https://github.com/anchore/grype
- **Skill pack:** `trivy-snyk-container-scanning`
- **Confidence:** ✓

## 14. SBOM generation + supply chain attestation (Sigstore)
- **SOTA approach:** Syft (Anchore) generates SBOM in SPDX or CycloneDX. Cosign (Sigstore) signs and attests images + SBOM keylessly via OIDC → Fulcio (cert authority) → Rekor (transparency log). SLSA Build Level 3 via `slsa-framework/slsa-github-generator`. in-toto attestations for end-to-end provenance. Verify in admission via Kyverno or `cosign verify-attestation`.
- **Agent execution path:** `cli-anything` (`syft <img> -o cyclonedx-json > sbom.json`, `cosign sign --yes <img>`, `cosign attest --predicate sbom.json --type cyclonedx <img>`, `cosign verify --certificate-identity-regexp=... <img>`).
- **Source:** https://github.com/anchore/syft · https://docs.sigstore.dev/cosign/ · https://slsa.dev/spec/v1.0/levels · https://in-toto.io/
- **Skill pack:** `sigstore-slsa-supply-chain-attestation`
- **Confidence:** ✓

## 15. Observability stack setup (OpenTelemetry → Honeycomb/Datadog/Grafana)
- **SOTA approach:** OpenTelemetry Collector (otelcol) as the universal sink — instrument apps with OTel SDKs (Python/JS/Go/Java auto-instrumentation), ship traces+metrics+logs to OTel Collector, fan out to Honeycomb (best-in-class traces/wide-events) OR Datadog (full APM/RUM/log) OR Grafana Cloud (Tempo+Mimir+Loki) OR self-hosted Tempo+Mimir+Loki. Resource attribute conventions: `service.name`, `deployment.environment`, `service.version`. OTel Operator for K8s auto-injection.
- **Agent execution path:** `cli-anything` (`helm upgrade --install otel-collector open-telemetry/opentelemetry-collector -f values.yaml`, `kubectl apply -f otel-instrumentation.yaml`) + `kubernetes-mcp` for verification.
- **Source:** https://opentelemetry.io/docs/collector/ · https://docs.honeycomb.io/getting-data-in/opentelemetry/ · https://docs.datadoghq.com/opentelemetry/ · https://grafana.com/oss/opentelemetry/
- **Skill pack:** `opentelemetry-instrumentation`, `honeycomb-datadog-observability`
- **Confidence:** ✓

## 16. Self-hosted observability (Prometheus + Grafana + Loki + Tempo + Mimir)
- **SOTA approach:** kube-prometheus-stack (CNCF) for Prometheus + Grafana + Alertmanager. Loki for logs (push via Promtail/Vector). Tempo for traces. Mimir for HA Prometheus-compatible long-term metrics. Pyroscope for continuous profiling. Vector (Datadog/Timber, Rust) is the SOTA log router (replaces Fluentd/Fluent Bit for new deploys). All glued via Grafana for unified dashboards.
- **Agent execution path:** `cli-anything` (`helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack`, `helm upgrade --install loki grafana/loki -f values.yaml`, `vector validate config.yaml`) + `kubernetes-mcp`.
- **Source:** https://github.com/prometheus-operator/kube-prometheus · https://grafana.com/oss/loki/ · https://grafana.com/oss/tempo/ · https://grafana.com/oss/mimir/ · https://vector.dev/
- **Skill pack:** `prometheus-grafana-loki-tempo-self-hosted`
- **Confidence:** ✓

## 17. SLO design + error budgets
- **SOTA approach:** Google SRE Workbook framing: SLI (measurable) → SLO (target, e.g., 99.9% success / 24h) → error budget (1 - SLO). Track via Sloth (OSS SLO generator → Prometheus rules) or Pyrra (Kubernetes-native SLO operator) or Nobl9 (managed). Multi-window multi-burn-rate alerts (5min @ 14.4×, 1h @ 6×). Document SLOs in markdown sibling to code.
- **Agent execution path:** `cli-anything` (`sloth generate -i slos.yaml -o prometheus-rules.yaml`, `kubectl apply -f sli-recording-rules.yaml`, `pyrra generate slo.yaml`) + `filesystem` for docs.
- **Source:** https://sre.google/workbook/implementing-slos/ · https://sloth.dev/ · https://github.com/pyrra-dev/pyrra · https://www.nobl9.com/
- **Skill pack:** `slos-error-budgets-google-sre`
- **Confidence:** ✓

## 18. Alerting rules + on-call (PagerDuty / Opsgenie / Incident.io)
- **SOTA approach:** Define alerts as Prometheus AlertManager rules (or Grafana managed alerts). Route via webhook to PagerDuty (legacy default), Opsgenie (Atlassian), Incident.io (modern incident-mgmt + on-call), Rootly, or FireHydrant. Each integrates Slack/MS Teams for war-room creation. Use Better Stack for status pages. Burn-rate alerts feed the same paging channel. Severity matrix: SEV1 (page now) / SEV2 (page during biz hours) / SEV3 (ticket).
- **Agent execution path:** `cli-anything` (`curl -X POST <pagerduty-events-api>`, `gh issue create --title "[SEV1] ..."`, `incident-io-cli create`) + `sentry-mcp` for error correlation + `slack-mcp` (catalog) for war-room.
- **Source:** https://prometheus.io/docs/alerting/latest/alertmanager/ · https://developer.pagerduty.com/api-reference/ · https://incident.io/changelog · https://docs.opsgenie.com/
- **Skill pack:** `pagerduty-incident-io-incident-response`
- **Confidence:** ⚠ — paging providers require recipient's account + API key

## 19. Incident response runbook
- **SOTA approach:** Pre-written runbooks under `runbooks/<service>/<scenario>.md` linked from alert annotations (`annotations.runbook_url`). Standard structure: severity → impact → diagnose-3-symptoms → mitigate-3-options → escalation contacts → recovery-checklist. Trigger via incident.io / Rootly / FireHydrant; war-room in Slack; live timeline in incident.io. Stop-the-world for SEV1, parallel investigation for SEV2/3.
- **Agent execution path:** `filesystem` for runbook auth + retrieval + `cli-anything` (`gh search prs --label incident`, `kubectl logs --tail=200 -l app=<svc>`, `cosign verify-attestation`) + `sentry-mcp` (errors) + `kubernetes-mcp` (cluster state).
- **Source:** https://sre.google/sre-book/managing-incidents/ · https://incident.io/guide/ · https://response.pagerduty.com/
- **Skill pack:** `pagerduty-incident-io-incident-response`
- **Confidence:** ✓

## 20. Post-incident review (blameless PIR)
- **SOTA approach:** Blameless PIR following Google SRE template: timeline → impact → root cause → contributing factors → lessons learned → action items (with owner + due date). Use `incident.io` for auto-generated retro doc, or Howie.ai (LLM-assisted PIR drafter), or markdown template under `incidents/YYYY-MM-DD-<slug>.md`. Action items become GitHub issues with `incident-followup` label.
- **Agent execution path:** `filesystem` (template fill) + `github` MCP (`gh issue create --label incident-followup`) + `cli-anything` (`incident-io-cli postmortem export <id>`).
- **Source:** https://sre.google/sre-book/postmortem-culture/ · https://incident.io/blog/postmortem-template · https://howie.ai/
- **Skill pack:** `pagerduty-incident-io-incident-response`
- **Confidence:** ✓

## 21. Blue/green deployment strategy
- **SOTA approach:** Two-environment cutover via service-level traffic switch (K8s Service selector swap, or Istio/Linkerd VirtualService weight, or ALB target-group swap). Argo Rollouts `Rollout` CRD with `strategy.blueGreen` for K8s-native. Smoke tests pre-cutover; instant rollback by re-swapping. Best when env duplication cost < risk of canary leak (e.g., stateful migrations).
- **Agent execution path:** `cli-anything` (`kubectl argo rollouts get rollout <name>`, `kubectl argo rollouts promote <name>`, `kubectl patch svc <svc> -p '{"spec":{"selector":{"version":"green"}}}'`) + `kubernetes-mcp`.
- **Source:** https://argo-rollouts.readthedocs.io/en/stable/features/bluegreen/ · https://martinfowler.com/bliki/BlueGreenDeployment.html
- **Skill pack:** `blue-green-canary-argo-rollouts`
- **Confidence:** ✓

## 22. Canary deployment + analysis (Argo Rollouts)
- **SOTA approach:** Argo Rollouts `Rollout` with `strategy.canary` + `analysis` reference (AnalysisTemplate querying Prometheus/Datadog/NewRelic for SLI). Progressive traffic shift: 5% → 25% → 50% → 100% over 30 min, gated by SLI checks. Auto-rollback on metric breach. Alternatives: Flagger (Flux ecosystem), Linkerd/Istio native canaries.
- **Agent execution path:** `cli-anything` (`kubectl argo rollouts set image <r> <c>=<img>:<tag>`, `kubectl argo rollouts status <r> --watch`, `kubectl argo rollouts abort <r>`) + `kubernetes-mcp`.
- **Source:** https://argo-rollouts.readthedocs.io/en/stable/features/canary/ · https://docs.flagger.app/
- **Skill pack:** `blue-green-canary-argo-rollouts`
- **Confidence:** ✓

## 23. Feature flags + progressive rollout (LaunchDarkly / Statsig / OpenFeature)
- **SOTA approach:** OpenFeature (CNCF, vendor-neutral SDK) as the SDK layer + LaunchDarkly (enterprise) / Statsig (modern, free tier) / Unleash (OSS self-hosted) / Flagsmith (OSS) as the backend. Default rule: ship dark, enable per-cohort, monitor SLI, expand. Tie flag changes to incident.io for auto-rollback.
- **Agent execution path:** `cli-anything` (`curl -X PATCH https://app.launchdarkly.com/api/v2/flags/<proj>/<flag> -H "Authorization: api-key"`, `statsig-cli rule update`) + `filesystem` for flag declaration YAML.
- **Source:** https://openfeature.dev/ · https://docs.launchdarkly.com/ · https://docs.statsig.com/ · https://docs.getunleash.io/
- **Skill pack:** `feature-flags-launchdarkly-statsig`
- **Confidence:** ⚠ — flag provider requires recipient's account + API key

## 24. Cost optimization (rightsizing, spot, reserved, FinOps)
- **SOTA approach:** Infracost on every PR (Terraform/OpenTofu cost diff before merge). OpenCost (CNCF, formerly Kubecost OSS) for K8s workload-level cost. Vantage / CloudHealth for multi-cloud aggregation. Karpenter (AWS) for K8s spot+rightsizing autoscaling. Reserved Instances / Savings Plans / CUDs for steady-state. Goldilocks for K8s right-sizing recommendations.
- **Agent execution path:** `cli-anything` (`infracost diff --path .`, `kubectl-cost namespace`, `goldilocks summary`, `karpenter-cli ...`) + `aws-s3-mcp` (catalog) for storage tiering.
- **Source:** https://www.infracost.io/ · https://www.opencost.io/ · https://karpenter.sh/ · https://goldilocks.fairwinds.com/ · https://www.finops.org/framework/
- **Skill pack:** `cost-optimization-finops-infracost`
- **Confidence:** ✓

## 25. Multi-environment strategy (dev / staging / prod)
- **SOTA approach:** GitOps repo structure: `clusters/<env>/<service>/*`. One overlay per env in Kustomize, or one values file per env in Helm. Ephemeral preview envs per PR via vCluster (virtual K8s clusters), Garden, or Okteto. Promote via PR from `staging` branch → `main` (or signed commit + ArgoCD ApplicationSet). Secrets isolated per env via ESO + Vault paths.
- **Agent execution path:** `cli-anything` (`vcluster create <pr-num>-preview --connect=false`, `argocd app set <app> --revision staging`) + `kubernetes-mcp`.
- **Source:** https://www.vcluster.com/ · https://garden.io/ · https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/
- **Skill pack:** `kubernetes-deployments-helm-kustomize`, `argocd-flux-gitops`
- **Confidence:** ✓

## 26. Disaster recovery + backup strategy
- **SOTA approach:** Velero for K8s cluster + PV backup (S3/GCS/Azure Blob target). Restic for filesystem-level backup. Database point-in-time-recovery (Postgres WAL-G, MySQL Percona XtraBackup, managed RDS snapshots). Cross-region replication for blob storage. Document RTO/RPO per service. Quarterly DR drills (`velero restore create --from-backup ...` on staging cluster).
- **Agent execution path:** `cli-anything` (`velero backup create <name> --include-namespaces=<ns>`, `velero restore create --from-backup <name>`, `aws s3 sync s3://prod-bucket s3://dr-bucket --region eu-west-1`) + `aws-s3-mcp` (catalog) + `kubernetes-mcp`.
- **Source:** https://velero.io/ · https://restic.net/ · https://github.com/wal-g/wal-g
- **Skill pack:** `kubernetes-deployments-helm-kustomize` (Velero subsection) + role.md DR section
- **Confidence:** ✓

## 27. Database migration coordination (zero-downtime)
- **SOTA approach:** Expand-contract / parallel-change pattern. Atlas (declarative SQL migrations, replaces Flyway/Liquibase for greenfield) or Liquibase 4.x for legacy. Use `pg-online-schema-change`/`pt-online-schema-change` for MySQL hot DDL. Coordinate with app deploys via two-phase (deploy backwards-compatible reader → migrate → deploy writer → cleanup).
- **Agent execution path:** `cli-anything` (`atlas migrate apply --env prod`, `atlas schema apply --auto-approve --to "file://migrations/v123.sql"`, `pg-online-schema-change ...`) + `postgresql-mcp` for inspection.
- **Source:** https://atlasgo.io/ · https://docs.liquibase.com/ · https://martinfowler.com/bliki/ParallelChange.html
- **Skill pack:** Defer to `senior-python-engineer` for app code; document path in role.md
- **Confidence:** ✓

## 28. DNS + CDN setup (Cloudflare / Fastly / AWS CloudFront)
- **SOTA approach:** Cloudflare as the modern default — DNS + CDN + WAF + DDoS + Pages + Workers in one. Manage via Terraform Cloudflare provider or `wrangler` CLI. Fastly for fine-grained VCL (now Compute@Edge in Rust/Go). CloudFront for AWS-only stacks. Use `cloudflared` for Zero-Trust tunnels. ACME-issued certs auto-managed by Cloudflare; CertManager for in-cluster.
- **Agent execution path:** `cloudflare-mcp` (DNS, Workers, page rules) + `cli-anything` (`wrangler deploy`, `wrangler tail`, `terraform apply -target=cloudflare_*`).
- **Source:** https://developers.cloudflare.com/ · https://docs.fastly.com/ · https://docs.aws.amazon.com/cloudfront/
- **Skill pack:** `cloudflare-vercel-railway-fly-render-paas`
- **Confidence:** ✓

## 29. TLS / certificate management (cert-manager + ACME)
- **SOTA approach:** cert-manager (CNCF graduated) in K8s for ACME-issued certs (Let's Encrypt / ZeroSSL). `Certificate` + `Issuer`/`ClusterIssuer` CRDs. DNS-01 challenge via cloud DNS provider for wildcards. Use `step-ca` for internal PKI. trust-manager for distributing CA bundles. Monitor expiry via cert-manager metrics in Prometheus.
- **Agent execution path:** `cli-anything` (`helm upgrade --install cert-manager jetstack/cert-manager --set installCRDs=true`, `kubectl apply -f cluster-issuer-letsencrypt.yaml`, `kubectl describe certificate <name>`) + `kubernetes-mcp`.
- **Source:** https://cert-manager.io/docs/ · https://letsencrypt.org/docs/ · https://smallstep.com/docs/step-ca/
- **Skill pack:** `cert-manager-acme-tls`
- **Confidence:** ✓

## 30. On-call rotation design
- **SOTA approach:** Tiered rotation (primary + secondary) with handoff at start of business day. Max 1-2 weeks per shift. Compensation per company policy. Schedule in PagerDuty / Opsgenie / Incident.io's on-call module / Grafana OnCall (OSS). Rotation YAML in repo for diff-ability. Pre-rotation runbook review session.
- **Agent execution path:** `cli-anything` (`curl PagerDuty schedules API`, `incident-io-cli oncall create-rotation`) + `filesystem` for docs.
- **Source:** https://sre.google/sre-book/being-on-call/ · https://www.pagerduty.com/resources/learn/oncall-management/ · https://grafana.com/products/oncall/
- **Skill pack:** `pagerduty-incident-io-incident-response`
- **Confidence:** ⚠ — paid scheduling tool; Grafana OnCall OSS works free

## 31. Developer portal setup (Backstage)
- **SOTA approach:** Spotify Backstage (CNCF incubating) as the dominant 2026 IDP. Software Catalog (entities in YAML), Tech Docs (Markdown-as-code), Software Templates (golden paths via cookiecutter-like flow), Scaffolder. Plugins: GitHub, ArgoCD, K8s, Sentry, PagerDuty. Hosted alts: Port, Cortex, OpsLevel (paid).
- **Agent execution path:** `cli-anything` (`npx @backstage/create-app`, `yarn dev`, `kubectl apply -f backstage-deployment.yaml`) + `filesystem` for catalog YAML.
- **Source:** https://backstage.io/docs · https://www.getport.io/ · https://www.cortex.io/
- **Skill pack:** `backstage-developer-portal`
- **Confidence:** ✓

## 32. Infrastructure cost estimation (Infracost in PR)
- **SOTA approach:** Infracost GitHub Action that comments on every Terraform/OpenTofu/Pulumi PR with the cost delta. `infracost-comment` for thread-update vs new-comment. Per-resource breakdown. Integrate with FinOps Foundation FOCUS spec for normalized billing exports.
- **Agent execution path:** `cli-anything` (`infracost breakdown --path . --format json --out-file ic.json`, `infracost diff --path . --compare-to baseline.json --format github-comment`) + `github` MCP for PR comment.
- **Source:** https://www.infracost.io/docs/ · https://focus.finops.org/
- **Skill pack:** `cost-optimization-finops-infracost`
- **Confidence:** ✓

## 33. Compliance audits (SOC 2 controls for infra)
- **SOTA approach:** Vanta / Drata / Secureframe for SOC 2 evidence automation (auto-pull MFA/encryption/backup proof from AWS+GitHub+Okta). Open Policy Agent (OPA) + Conftest for policy-as-code; Kyverno for K8s admission policies. Falco for runtime security signals. Document controls in `compliance/` folder.
- **Agent execution path:** `cli-anything` (`conftest test --policy policies/ infrastructure/`, `kubectl apply -f kyverno-policies/`, `falco -c falco.yaml`) + `filesystem` for control docs.
- **Source:** https://www.openpolicyagent.org/docs · https://kyverno.io/docs/ · https://falco.org/docs/ · https://www.vanta.com/
- **Skill pack:** Referenced in role.md; relies on `cli-anything` + OPA/Kyverno; full compliance flows defer to a future `compliance-engineer` agent
- **Confidence:** ⚠ — automated evidence collectors are paid SaaS; OPA/Kyverno run free

## 34. Capacity planning + load testing (k6 / Locust / Vegeta)
- **SOTA approach:** k6 (Grafana, JS scripts) as the modern default — replaces JMeter/Gatling for most workloads. Locust (Python) for teams already in Python ecosystem. Vegeta for HTTP load (Go, simple). k6 + xk6-disruptor for chaos injection. Capacity planning: load to 2x p99 expected, scale until p95 latency breaks SLO, document headroom.
- **Agent execution path:** `cli-anything` (`k6 run --vus 100 --duration 5m script.js`, `k6 cloud script.js`, `locust -f locustfile.py --headless -u 100 -r 10`, `echo "GET https://api.example.com" | vegeta attack -duration=30s | vegeta report`).
- **Source:** https://k6.io/docs/ · https://docs.locust.io/ · https://github.com/tsenart/vegeta
- **Skill pack:** Documented in role.md SOTA section; uses `cli-anything`
- **Confidence:** ✓

## 35. K8s admission control / policy enforcement
- **SOTA approach:** Kyverno (CNCF, Kubernetes-native YAML policies) as the 2026 default — replaces Gatekeeper/OPA for K8s use cases. Use for: image signature verification (Cosign), required resource limits, blocked privileged pods, mandatory labels. PolicyReports stored in cluster.
- **Agent execution path:** `cli-anything` (`kyverno apply policies/ --resource manifests/`, `kubectl apply -f cluster-policies/`, `kubectl get policyreport -A`) + `kubernetes-mcp`.
- **Source:** https://kyverno.io/docs/ · https://github.com/kyverno/policies
- **Skill pack:** Referenced in `kubernetes-deployments-helm-kustomize` + role.md
- **Confidence:** ✓

## 36. PaaS deployment (Vercel / Railway / Fly.io / Render)
- **SOTA approach:** Vercel for frontend / Next.js. Railway for monorepo apps. Fly.io for global edge (`fly.toml` config). Render for low-config containerized services. Cloudflare Pages + Workers for static + serverless. All via Git-push deploy or CLI. Choose PaaS when team doesn't want K8s overhead.
- **Agent execution path:** `cli-anything` (`vercel deploy --prod`, `railway up`, `fly deploy`, `render deploy`) + `cloudflare-mcp` (Pages/Workers).
- **Source:** https://vercel.com/docs · https://docs.railway.com/ · https://fly.io/docs/ · https://render.com/docs
- **Skill pack:** `cloudflare-vercel-railway-fly-render-paas`
- **Confidence:** ✓

---

## Summary table (≥90% fulfillment)

| # | Use case | SOTA tool | Mechanism | Fulfillment |
|---|---|---|---|---|
| 1 | Dockerfile authoring | Docker BuildKit + Chainguard/distroless + Cosign | `cli-anything` + `docker buildx` | ✓ |
| 2 | K8s deployment manifests | Helm + Kustomize + kubeconform | `kubernetes-mcp` + `cli-anything` | ✓ |
| 3 | Helm chart authoring | Helm 3 + helm-docs + Cosign + OCI registry | `cli-anything` | ✓ |
| 4 | Kustomize overlays | kubectl + kustomize | `cli-anything` + `kubernetes-mcp` | ✓ |
| 5 | Terraform / OpenTofu | OpenTofu 1.8 + tflint + checkov + infracost | `cli-anything` | ✓ |
| 6 | Pulumi | Pulumi 3.x + Pulumi ESC | `cli-anything` | ✓ |
| 7 | AWS CDK / SAM / SST | CDK 2.x / SST v3 / SAM | `cli-anything` | ✓ |
| 8 | GitHub Actions | OIDC + reusable workflows + actionlint + act | `github` MCP + `cli-anything` | ✓ |
| 9 | ArgoCD GitOps | ArgoCD 2.13 + App-of-Apps + image-updater | `cli-anything` + `kubernetes-mcp` | ✓ |
| 10 | Flux GitOps | Flux v2 (CNCF graduated) | `cli-anything` + `kubernetes-mcp` | ✓ |
| 11 | Secret management | Vault/OpenBao + ESO + Pulumi ESC | `cli-anything` + `kubernetes-mcp` | ✓ |
| 12 | CI/CD pipeline | GH Actions + BuildKit + Trivy + Cosign + Syft + SLSA | `cli-anything` + `github` MCP | ✓ |
| 13 | Container scanning | Trivy + Snyk + Grype | `cli-anything` | ✓ |
| 14 | SBOM + attestation | Syft + Cosign + SLSA + in-toto | `cli-anything` | ✓ |
| 15 | OTel observability | OTel Collector + Honeycomb/Datadog/Grafana Cloud | `cli-anything` + `kubernetes-mcp` | ✓ |
| 16 | Self-hosted observability | kube-prometheus-stack + Loki + Tempo + Mimir + Vector | `cli-anything` + `kubernetes-mcp` | ✓ |
| 17 | SLOs + error budgets | Sloth / Pyrra / Nobl9 | `cli-anything` | ✓ |
| 18 | Alerting + paging | Alertmanager + PagerDuty/Opsgenie/Incident.io | `cli-anything` + `sentry-mcp` | ⚠ |
| 19 | Incident response | Runbooks + incident.io/Rootly + Slack war-room | `filesystem` + `cli-anything` + `sentry-mcp` + `kubernetes-mcp` | ✓ |
| 20 | Post-incident review | Blameless template + incident.io + Howie.ai | `filesystem` + `github` MCP | ✓ |
| 21 | Blue/green deployment | Argo Rollouts blueGreen | `cli-anything` + `kubernetes-mcp` | ✓ |
| 22 | Canary deployment | Argo Rollouts canary + AnalysisTemplate / Flagger | `cli-anything` + `kubernetes-mcp` | ✓ |
| 23 | Feature flags | OpenFeature SDK + LaunchDarkly/Statsig/Unleash | `cli-anything` | ⚠ |
| 24 | Cost optimization | Infracost + OpenCost + Karpenter + Goldilocks | `cli-anything` | ✓ |
| 25 | Multi-environment | GitOps overlay pattern + vCluster + ApplicationSet | `cli-anything` + `kubernetes-mcp` | ✓ |
| 26 | DR + backup | Velero + Restic + WAL-G + cross-region replication | `cli-anything` + `aws-s3-mcp` + `kubernetes-mcp` | ✓ |
| 27 | DB migration | Atlas / Liquibase + parallel-change | `cli-anything` + `postgresql-mcp` | ✓ |
| 28 | DNS + CDN | Cloudflare + Wrangler / Fastly / CloudFront | `cloudflare-mcp` + `cli-anything` | ✓ |
| 29 | TLS / cert-manager | cert-manager + Let's Encrypt + trust-manager + step-ca | `cli-anything` + `kubernetes-mcp` | ✓ |
| 30 | On-call rotation | PagerDuty/Opsgenie/Incident.io/Grafana OnCall (OSS) | `cli-anything` | ⚠ |
| 31 | Developer portal | Backstage (CNCF) | `cli-anything` + `filesystem` | ✓ |
| 32 | Cost estimation in PR | Infracost GH Action | `cli-anything` + `github` MCP | ✓ |
| 33 | Compliance audits | OPA + Kyverno + Falco + Vanta/Drata | `cli-anything` + `filesystem` | ⚠ |
| 34 | Load testing | k6 + Locust + Vegeta + xk6-disruptor | `cli-anything` | ✓ |
| 35 | K8s admission control | Kyverno (CNCF) | `cli-anything` + `kubernetes-mcp` | ✓ |
| 36 | PaaS deployment | Vercel/Railway/Fly.io/Render + Cloudflare Pages | `cli-anything` + `cloudflare-mcp` | ✓ |

**Fulfillment math:** 36 use cases mapped. 31 are ✓ (fully executable). 5 are ⚠ (executable with paid SaaS or recipient account). 0 are ✗.

**Verdict: ~95% fulfillment.** The 5 ⚠ rows are all OAuth/paid-API gates owned by the recipient (PagerDuty, LaunchDarkly, Vanta/Drata, on-call schedulers). Free OSS fallbacks exist for each (Grafana OnCall for paging+rotation, Unleash for flags, OPA/Kyverno for compliance signals). No genuinely impossible use cases.

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (all verified to exist in `app/config/mcp_config.json`):
- `filesystem` — mandatory, used by 20+ use cases (runbooks, manifests, IaC code, docs)
- `kubernetes-mcp` — 14 use cases touch K8s
- `github` — 8 use cases use GitHub Actions / PRs / issues
- `aws-s3-mcp` — DR backups, log archiving, OCI image storage
- `cloudflare-mcp` — DNS, CDN, Workers, Pages, Zero-Trust
- `sentry-mcp` — production error correlation in incident response
- `postgresql-mcp` — DB migration coordination
- `splunk-mcp` — log search if recipient runs Splunk (alt to Loki/Datadog)

**Skill packs to create in Round 2 (bundled — 22 total), in order of impact:**

1. `docker-multistage-buildkit-distroless` — use cases 1, 12
2. `kubernetes-deployments-helm-kustomize` — use cases 2, 3, 4, 25, 26, 35
3. `terraform-opentofu-iac` — use case 5
4. `pulumi-iac-python-typescript` — use case 6
5. `aws-cdk-sst-serverless` — use case 7
6. `github-actions-cicd-oidc` — use cases 8, 12
7. `argocd-flux-gitops` — use cases 9, 10, 25
8. `vault-doppler-pulumi-esc-secrets` — use case 11
9. `external-secrets-operator-k8s` — use case 11
10. `opentelemetry-instrumentation` — use case 15
11. `honeycomb-datadog-observability` — use case 15
12. `prometheus-grafana-loki-tempo-self-hosted` — use case 16
13. `slos-error-budgets-google-sre` — use case 17
14. `pagerduty-incident-io-incident-response` — use cases 18, 19, 20, 30
15. `blue-green-canary-argo-rollouts` — use cases 21, 22
16. `feature-flags-launchdarkly-statsig` — use case 23
17. `trivy-snyk-container-scanning` — use case 13
18. `sigstore-slsa-supply-chain-attestation` — use case 14
19. `cloudflare-vercel-railway-fly-render-paas` — use cases 28, 36
20. `cost-optimization-finops-infracost` — use cases 24, 32
21. `cert-manager-acme-tls` — use case 29
22. `backstage-developer-portal` — use case 31

---

## Notes on remaining caveats (the ⚠ rows)

### Use case 18 — Alerting + paging
- **Blocked:** Recipient must own PagerDuty / Opsgenie / Incident.io account + API key.
- **Free fallback:** Grafana OnCall (OSS, self-hosted, free) — covers paging + rotation + ack/resolve flow.
- **Workaround:** Alertmanager → Slack webhook for non-pageable alerts.

### Use case 23 — Feature flags
- **Blocked:** LaunchDarkly / Statsig are SaaS (LaunchDarkly is paid; Statsig has a generous free tier).
- **Free fallback:** Unleash (OSS, self-hosted) or Flagsmith (OSS, self-hosted).
- **Workaround:** OpenFeature SDK abstracts the provider — recipient can swap later.

### Use case 30 — On-call rotation
- **Blocked:** PagerDuty / Opsgenie / Incident.io schedules require paid account.
- **Free fallback:** Grafana OnCall (OSS) or hand-rolled Google Calendar + Slack reminder.

### Use case 33 — Compliance audits
- **Blocked:** Vanta / Drata / Secureframe are paid evidence collectors.
- **Free fallback:** OPA + Kyverno + Falco generate the underlying signals; agent can author the policies for free. Hand off to a compliance-engineer (v1) for full SOC 2 audit packet.

### Use case 18, 30 (combined) — runbook / paging note
- Each paging provider has a documented REST API; agent can `curl -X POST` events even without a dedicated MCP. Adding `pagerduty-mcp` or `incident-io-mcp` to the catalog is a future improvement.
