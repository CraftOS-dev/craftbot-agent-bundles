# DevOps Engineer — deep reference

This section appends to `AGENT.md`. It is **not** in the agent's default context. Grep it when the SOUL.md summary isn't enough.

Headings are kept search-friendly: "Antipattern catalog", "Incident response playbook", "SLO design playbook", "Kubernetes manifest reference", "Helm chart reference", "Terraform / OpenTofu reference", "Pulumi reference", "GitHub Actions reference", "ArgoCD reference", "Flux reference", "Vault reference", "ESO reference", "OpenTelemetry reference", "Cosign reference", "Trivy reference", "k6 reference", "Backstage reference", "SOTA tool reference".

For provenance of any section, see `SOURCES.md` in this bundle.

---

## Capability reference

Pure factual reference — what tools, services, and patterns exist in the 2026 cloud-native ecosystem. SOUL.md does not carry these (they don't drive decisions); grep here when the user asks "what should I use for X?" or you need to name a specific tool.

### Container engines + builders

- Docker / docker-compose (default)
- BuildKit (mandatory for cache mounts, secrets mounts, multi-arch)
- Podman (rootless alt to Docker; supports Docker CLI compat)
- Buildah (image build without daemon)
- Wolfi OS (distroless from Chainguard — minimal CVE surface)
- Chainguard Images (zero-CVE base images)
- Google distroless (`gcr.io/distroless/*`)
- Alpine (legacy minimal; musl can break Python wheels)

### Kubernetes distributions + tools

- kubectl / kubeadm
- Helm 3.x (chart packaging, OCI registry support)
- Kustomize (overlay/patch templating, built into `kubectl`)
- k9s (TUI cluster navigator)
- kubectx / kubens (context + namespace switcher)
- Kind / minikube / k3s / Docker Desktop (local clusters)
- Talos Linux (immutable, API-managed K8s nodes)
- EKS / GKE / AKS / DigitalOcean Kubernetes / Civo / Linode
- OpenShift / Rancher RKE2 / kubespray (self-managed)
- vCluster (virtual K8s for PR preview envs)
- Crossplane (K8s-native multi-cloud IaC)

### GitOps + progressive delivery

- ArgoCD (CNCF graduated — App-of-Apps + ApplicationSets + image-updater)
- Flux v2 (CNCF graduated — source-controller + kustomize-controller + helm-controller + notification-controller + image-controllers)
- Argo Rollouts (canary + blue/green CRDs with analysis hooks)
- Flagger (Flux-ecosystem progressive delivery)
- Spinnaker (legacy multi-cloud CD; declining for new deployments)
- LaunchDarkly / Statsig / Unleash / Flagsmith (feature flags)
- OpenFeature (CNCF vendor-neutral SDK)

### IaC

- Terraform 1.9 (HashiCorp; BSL-licensed post-2023)
- OpenTofu 1.8 (Linux Foundation fork; drop-in compatible)
- Pulumi 3.130+ (Python/TS/Go/C#/Java)
- AWS CDK 2.x (TS/Python — synthesizes CloudFormation)
- SST v3 (built on Pulumi runtime; modern AWS serverless)
- AWS SAM (Lambda-centric CloudFormation extension)
- Serverless Framework (multi-cloud serverless)
- Crossplane (K8s CRDs control AWS/GCP/Azure)
- Atlantis (Terraform PR automation)
- Spacelift / Scalr / env0 (managed IaC orchestration)
- Terragrunt (Terraform DRY wrapper — declining vs. native modules)

### Secrets

- HashiCorp Vault 1.17+ (source-of-truth; BSL-licensed)
- OpenBao 2.0 (Linux Foundation Vault fork; OSS)
- External Secrets Operator (K8s sync; CNCF incubating)
- Sealed Secrets (Bitnami; encrypted secrets in git)
- SOPS (Mozilla; YAML/JSON encryption with KMS/age/PGP)
- Doppler (managed)
- Pulumi ESC (environments, secrets, config)
- 1Password Secrets Automation
- Infisical (OSS managed)
- Bitwarden Secrets Manager
- AWS Secrets Manager / AWS KMS
- GCP Secret Manager
- Azure Key Vault

### CI/CD platforms

- GitHub Actions (default for GitHub repos)
- GitLab CI (default for GitLab repos)
- CircleCI (legacy; still strong on macOS runners)
- Buildkite (self-hosted runners; popular at scale)
- Jenkins (legacy)
- Drone CI / Woodpecker CI (OSS Drone fork)
- Earthly (build automation in Earthfile syntax)
- Dagger (programmable CI in Go/Python/TS)
- Tekton (CNCF K8s-native CI/CD)
- Argo Workflows (CNCF; K8s-native workflow engine)

### Observability stack

- OpenTelemetry (CNCF graduated — SDKs + Collector)
- Sentry (errors + tracing + profiling)
- Honeycomb (wide-events + traces)
- Datadog (full APM/RUM/logs)
- New Relic (APM + browser + mobile)
- Grafana Cloud (managed Tempo+Mimir+Loki+Pyroscope)
- Lightstep (now part of ServiceNow Cloud Observability)
- AppDynamics (Cisco)
- Splunk (logs + SIEM)
- Prometheus + Alertmanager (CNCF graduated)
- Grafana (dashboards)
- Loki (logs, push-based)
- Tempo (traces)
- Mimir (HA Prometheus-compatible long-term metrics)
- Pyroscope (continuous profiling)
- Vector (Rust log/metric router)
- Fluent Bit / Fluentd (legacy log routers)
- Better Stack (Uptime + Logtail + Telemetry — combined)
- Highlight (OSS Sentry alt)

### Incident response platforms

- PagerDuty (legacy default)
- Opsgenie (Atlassian)
- Incident.io (modern combined IRM + on-call)
- Rootly (modern IRM)
- FireHydrant (modern IRM)
- Statuspage (Atlassian)
- Better Stack Uptime
- Grafana OnCall (OSS, free)
- Howie.ai (LLM-assisted PIR drafter)

### Cloud providers / PaaS

- AWS (catalog: `aws-s3-mcp`; plus IAM/VPC/EC2/EKS/RDS/Lambda)
- GCP (GKE, Cloud Run, Cloud Functions, BigQuery)
- Azure (AKS, Container Apps, Functions, Cosmos DB)
- Cloudflare (catalog: `cloudflare-mcp`; DNS+CDN+Workers+Pages+R2+D1+Zero-Trust)
- Vercel (Next.js, frontend, edge)
- Railway (monorepo-friendly app PaaS)
- Render (low-config containerized PaaS)
- Fly.io (global edge + Fly Machines)
- DigitalOcean App Platform + Kubernetes
- Heroku (legacy; still in use)
- Akamai Connected Cloud (Linode + Akamai)
- Hetzner / OVHCloud / Scaleway (EU low-cost)

### Security / supply chain

- Trivy (Aqua — fast, free, all-in-one)
- Snyk (commercial; policy + license + IaC)
- Grype (Anchore — Trivy alt)
- Wiz (cloud security posture mgmt, paid)
- Aqua Security (commercial supply chain)
- Chainguard Images (distroless minimal CVE)
- Sigstore (CNCF incubating — Cosign + Fulcio + Rekor)
- SLSA framework (Levels 1-4 build provenance)
- in-toto attestations (CNCF graduated)
- Syft (Anchore — SBOM generator)
- OPA / Conftest (CNCF graduated — policy)
- Kyverno (CNCF incubating — K8s-native policy)
- Falco (CNCF graduated — runtime security)
- Gatekeeper (OPA for K8s admission; declining vs Kyverno)
- Tetragon (Cilium — eBPF-based runtime visibility)
- Cilium (CNCF graduated — eBPF networking + security)
- gitleaks / trufflehog (secrets detection)

### Cost / FinOps

- Infracost (Terraform/OpenTofu/Pulumi cost in PR — free OSS + paid SaaS)
- OpenCost (CNCF — K8s workload cost; was Kubecost OSS)
- Vantage (multi-cloud cost SaaS)
- CloudHealth (VMware multi-cloud)
- Apptio Cloudability
- Cast.ai (K8s autoscaling + cost optimization)
- Karpenter (AWS — open-source K8s spot+rightsize autoscaler)
- Goldilocks (Fairwinds — K8s right-sizing recommendations)
- FinOps Foundation FOCUS spec (normalized cloud bills)

### Developer portals

- Spotify Backstage (CNCF incubating — dominant 2026 IDP)
- Port (modern hosted developer portal)
- Cortex (engineering excellence platform)
- OpsLevel (service catalog + maturity)
- Roadie (managed Backstage)

### Network mesh + ingress

- NGINX Ingress Controller (CNCF — most popular)
- Traefik (CNCF incubating)
- HAProxy Ingress
- Contour (CNCF — Envoy-based)
- Istio (CNCF graduated — full mesh)
- Linkerd (CNCF graduated — lightweight mesh, Rust)
- Cilium Service Mesh (eBPF, sidecarless)
- Gateway API (K8s next-gen Ingress)
- Envoy Proxy (CNCF graduated — building block)

---

## Antipattern catalog

Full BAD/GOOD pairs for every antipattern in the SOUL.md checklist. Use these when reviewing infra code or when the user asks "what's wrong with this pattern?"

### Mutable image tag in production

**BAD:**
```yaml
# k8s/deployment.yaml
containers:
  - name: api
    image: myorg/api:latest
```

**Why it's bad:** `latest` is mutable. Same manifest at two points in time may pull different image content. Breaks reproducibility and rollback.

**GOOD:**
```yaml
containers:
  - name: api
    image: myorg/api@sha256:6ba7b8...0bc9
```

**Why it's better:** Digest is immutable. Same manifest = same image, forever. CI builds and prints the digest; ArgoCD image-updater pins it.

---

### `kubectl apply` from a laptop against prod

**BAD:**
```bash
$ kubectl apply -f deployment.yaml --context=prod
```

**Why it's bad:** No audit trail, no diff review, no rollback. The deployed state diverges from git. "What's actually in prod?" becomes unanswerable.

**GOOD:**
```bash
# 1. Edit manifests in git
$ git checkout -b feature/api-v1.27
$ vim manifests/prod/api-deployment.yaml
$ git commit -sm "feat(api): bump to v1.27.3"
$ gh pr create --base main

# 2. After PR merge, ArgoCD pulls and applies
$ argocd app get api-prod          # confirm sync
$ argocd app diff api-prod         # diff if anything off
```

**Why it's better:** Git is the source of truth. Audit, diff, review, rollback all work.

---

### Secret committed to git

**BAD:**
```yaml
# k8s/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-creds
type: Opaque
data:
  password: cHJvZF9wYXNzd29yZA==   # base64-encoded; trivially decoded
```

**Why it's bad:** Base64 is encoding, not encryption. Committing this leaks the password. `gitleaks` catches it; reviewers may miss it.

**GOOD:**
```yaml
# k8s/external-secret.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-creds
spec:
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: db-creds
  data:
    - secretKey: password
      remoteRef:
        key: secret/prod/api/db
        property: password
```

**Why it's better:** Vault holds the secret. ESO syncs it into the cluster. Rotation in Vault auto-propagates. No secret in git.

---

### `cluster-admin` for service account

**BAD:**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: api-cluster-admin
subjects:
  - kind: ServiceAccount
    name: api-svc
    namespace: prod
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
```

**Why it's bad:** Application service account can delete any resource cluster-wide. Compromise of the API pod = compromise of the cluster.

**GOOD:**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role             # namespace-scoped
metadata:
  name: api-svc-role
  namespace: prod
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "list", "watch"]   # least-privilege: only what's needed
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: api-svc-binding
  namespace: prod
subjects:
  - kind: ServiceAccount
    name: api-svc
    namespace: prod
roleRef:
  kind: Role
  name: api-svc-role
  apiGroup: rbac.authorization.k8s.io
```

---

### Missing resource limits

**BAD:**
```yaml
containers:
  - name: api
    image: myorg/api@sha256:6ba7b8...
    # no resources block — pod can OOM the node
```

**Why it's bad:** Unbounded memory growth crashes the node, taking down everything scheduled there. K8s evicts pods on memory pressure with cryptic reasons.

**GOOD:**
```yaml
containers:
  - name: api
    image: myorg/api@sha256:6ba7b8...
    resources:
      requests:
        cpu: 100m
        memory: 256Mi
      limits:
        cpu: 500m
        memory: 512Mi
```

**Why it's better:** OOM-kill is explicit, attributable, and contained to the offending pod. Scheduler can plan properly.

---

### Terraform state on local disk

**BAD:**
```hcl
# no backend block → state file in working directory
resource "aws_s3_bucket" "data" {
  bucket = "myorg-data"
}
```

**Why it's bad:** Local state means one engineer can run terraform safely. CI/CD can't. State is unencrypted, easily lost, not locked.

**GOOD:**
```hcl
terraform {
  backend "s3" {
    bucket         = "myorg-tfstate"
    key            = "prod/data.tfstate"
    region         = "us-east-1"
    dynamodb_table = "myorg-tfstate-lock"
    encrypt        = true
  }
}
```

**Why it's better:** State is remote, encrypted, locked, accessible to CI. Engineers can collaborate; rollback works.

---

### Long-lived AWS credentials in GitHub Actions

**BAD:**
```yaml
- uses: aws-actions/configure-aws-credentials@v1
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

**Why it's bad:** Long-lived creds. If the secret leaks, blast radius is the lifetime of the key. Rotation is manual.

**GOOD:**
```yaml
permissions:
  id-token: write       # required for OIDC
  contents: read

steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789012:role/gh-actions-deploy
      aws-region: us-east-1
```

**Why it's better:** GitHub OIDC mints a short-lived (15min) token. No long-lived secret in the repo. Trust policy on the IAM role pins to specific repo+branch.

---

### Alert without runbook

**BAD:**
```yaml
- alert: HighErrorRate
  expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
  labels:
    severity: critical
  annotations:
    summary: "High error rate"
```

**Why it's bad:** Page wakes someone at 3am. They see "High error rate" and have to figure out what to do from scratch. MTTR climbs.

**GOOD:**
```yaml
- alert: HighErrorRate
  expr: |
    sum(rate(http_requests_total{status=~"5..",service="api"}[5m])) by (service)
    /
    sum(rate(http_requests_total{service="api"}[5m])) by (service)
    > 0.05
  for: 2m
  labels:
    severity: critical
    service: api
  annotations:
    summary: "5xx error rate >5% on {{ $labels.service }} (current: {{ $value | humanizePercentage }})"
    description: "Burn rate exceeds 14.4x — 1h budget consumed in 2.5h at current rate."
    runbook_url: "https://github.com/myorg/runbooks/blob/main/api/high-error-rate.md"
    dashboard: "https://grafana.myorg.com/d/api-overview"
```

---

### Common fixes summary

| Antipattern | Fix |
|---|---|
| Mutable image tag | Pin by `@sha256:` digest |
| `kubectl apply` from laptop | GitOps — git PR → ArgoCD/Flux pull |
| Secret in git | Vault + ESO; or SOPS for encrypted git |
| `cluster-admin` for app SA | Namespace `Role` + `RoleBinding` — least-privilege |
| No resource limits | `resources.requests/limits` on every container |
| Local Terraform state | Remote backend + lock + encryption |
| Long-lived cloud creds | OIDC federation |
| Alert without runbook | `annotations.runbook_url` |
| Per-service LoadBalancer | One Ingress + path/host routing |
| No canary/rollback | Argo Rollouts canary + AnalysisTemplate |
| `latest` Docker tag | Digest pinning |
| Manual cert renewal | cert-manager + ACME |
| Hand-rolled log pipeline | Vector + Loki/Datadog/Honeycomb via OTLP |

---

## Incident response playbook

### Severity matrix

| Level | Definition | Response | Comms |
|---|---|---|---|
| SEV1 | User-facing outage; revenue/SLA impact | Page now. Mitigate first. War-room. | Status page + customer email |
| SEV2 | Degraded service for >10 min | Page during biz hours. Diagnose+mitigate. | Internal Slack + status page if customer-visible |
| SEV3 | Internal-only issue; no user impact | File ticket. Schedule fix. | Internal Slack |

### SEV1 incident flow

1. **Acknowledge the page** within 5 min. Reply in the incident Slack channel: "Ack — investigating."
2. **Open the war-room.** `incident-io create` or `rootly declare` creates the channel + timeline. Add the SRE on-call, the service owner, the recent-deployer.
3. **Mitigate first.** Default ladder:
   - `argocd app rollback <app>` to last known good (60 sec)
   - `kubectl rollout undo deployment <name>` (30 sec)
   - Feature flag off the new code path
   - `kubectl scale deployment <name> --replicas=0` for runaway pods
   - `kubectl patch svc <name>` to route traffic away from bad cluster
4. **Confirm mitigation.** Watch the SLI graph. Error rate drops, latency recovers? Good. Re-page channel; downgrade severity.
5. **Diagnose** — only after mitigation. Pull:
   - Last 5 PRs / deployments before incident start
   - Sentry errors filtered to the affected service
   - `kubectl logs --tail=200 -l app=<svc>`
   - Trace samples from Honeycomb / Datadog
   - Continuous profiling diff (Pyroscope / Sentry Profiling)
6. **Status page** update for SEV1 — `statuspage` CLI or incident.io auto-syncs. Customer wording is short, factual, dated.
7. **Resolve** — incident closes when SLI is back in budget AND root cause is at least hypothesized (full RCA can be later).

### Diagnosis order — what to suspect first

1. Recent deploy (last 30 min): `kubectl rollout history` / `argocd app history`
2. Recent config change: `kubectl diff -k`, ArgoCD app diff
3. Upstream dependency: cloud provider status pages, DNS resolution, third-party API status
4. Resource exhaustion: CPU / memory / disk / file descriptor / connection pool
5. Network: NetworkPolicy change, DNS, Ingress controller config
6. Cert expiry: `kubectl describe certificate -A | grep -A 3 Status`
7. Data corruption: DB replication lag, cache poisoning

### Post-incident review (blameless PIR)

Template:

```markdown
# Incident: <one-line summary> — YYYY-MM-DD

**Severity:** SEV<n>
**Started:** YYYY-MM-DD HH:MM UTC
**Detected:** YYYY-MM-DD HH:MM UTC (Time-to-Detect: X min)
**Mitigated:** YYYY-MM-DD HH:MM UTC (Time-to-Mitigate: X min)
**Resolved:** YYYY-MM-DD HH:MM UTC (Time-to-Resolve: X min)
**Author:** <on-call> — <author>
**Customer impact:** <% requests failed × duration × user count>

## Summary
<2-3 sentences. What broke, what we did, what fixed it.>

## Timeline (UTC)
- HH:MM — <event>
- HH:MM — <event>

## Root cause
<Technical detail. Code path / config change / dep failure. Cite the PR or commit SHA.>

## Contributing factors
<What made this worse than it had to be? Missing alert, wrong runbook, slow rollback, on-call confused, etc.>

## What went well
<Don't skip this. Fast detection, clean rollback, clear comms — name them.>

## What went poorly
<Specific. "MTTD was 18 min because the SLI alert was on the wrong metric.">

## Lessons learned
<Honest. Not a fix list — observations about the system + process.>

## Action items
| Owner | Action | Due | GitHub issue |
|---|---|---|---|
| @<user> | Add SLI for upstream-dep latency | 2026-MM-DD | #1234 (label: incident-followup) |
| @<user> | Update runbook with rollback command | 2026-MM-DD | #1235 |

## Appendix
- Grafana dashboard URL
- Sentry issue URL
- ArgoCD app history snapshot
- Slack war-room export
```

---

## SLO design playbook

### Step 1 — define the SLI

The SLI is the **measurable signal** that maps to user happiness. Pick one of:

- **Availability** — successful_requests / total_requests
- **Latency** — requests under threshold / total_requests (e.g., requests < 200ms)
- **Quality** — requests returning correct/fresh data / total
- **Throughput** — requests/sec sustained
- **Freshness** — events with age <threshold / total events (for streaming/batch)

Per Google SRE Workbook: SLI must be measurable from the user's perspective, not from internal-cluster metrics.

### Step 2 — set the SLO

Format: `<percent> over <window>`. Common windows: 28 days (rolling), 7 days, 30 days.

Examples:
- 99.9% availability over 30d (~43 min budget/month)
- 99% requests <200ms p99 over 7d
- 99.5% events processed within 60s over 28d

### Step 3 — express as Sloth YAML

```yaml
version: prometheus/v1
service: api
labels:
  team: platform
slos:
  - name: requests-availability
    objective: 99.9
    description: "99.9% of requests succeed (non-5xx)"
    sli:
      events:
        error_query: sum(rate(http_requests_total{service="api",status=~"5.."}[{{.window}}]))
        total_query: sum(rate(http_requests_total{service="api"}[{{.window}}]))
    alerting:
      name: ApiHighErrorRate
      page_alert:
        labels: { severity: critical }
      ticket_alert:
        labels: { severity: warning }
      annotations:
        runbook: "https://github.com/myorg/runbooks/blob/main/api/availability.md"
```

`sloth generate -i slos.yaml -o prometheus-rules.yaml` produces the alerting + recording rules. Apply via `kubectl apply -f prometheus-rules.yaml` to `kube-prometheus-stack`.

### Step 4 — multi-window multi-burn-rate alerts

| Burn rate | Window | Alert window | Time to consume 30d budget |
|---|---|---|---|
| 14.4× | 1h | 5m | 2.1h |
| 6× | 6h | 30m | 5d |
| 3× | 24h | 2h | 10d |
| 1× | 72h | 6h | 30d |

The 14.4×/5m and 6×/30m combos page; the slower combos ticket.

### Step 5 — error budget policy

Document in `docs/slo/error-budget-policy.md`:
- If budget is exhausted: freeze feature releases; only reliability work.
- If budget is healthy (>50%): proceed normally.
- Quarterly review: SLOs that nobody alerts on are too generous; SLOs that page constantly are too aggressive.

---

## Kubernetes manifest reference

### Minimal production-grade Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  namespace: prod
  labels:
    app.kubernetes.io/name: api
    app.kubernetes.io/version: "1.27.3"
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0     # zero-downtime
  selector:
    matchLabels:
      app.kubernetes.io/name: api
  template:
    metadata:
      labels:
        app.kubernetes.io/name: api
        app.kubernetes.io/version: "1.27.3"
    spec:
      serviceAccountName: api-svc
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        fsGroup: 10001
        seccompProfile:
          type: RuntimeDefault
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: ScheduleAnyway
          labelSelector:
            matchLabels:
              app.kubernetes.io/name: api
      containers:
        - name: api
          image: myreg.io/api@sha256:6ba7b8...
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 8080
          env:
            - name: OTEL_SERVICE_NAME
              value: api
            - name: OTEL_EXPORTER_OTLP_ENDPOINT
              value: http://otel-collector:4318
          resources:
            requests:
              cpu: 100m
              memory: 256Mi
            limits:
              cpu: 500m
              memory: 512Mi
          readinessProbe:
            httpGet: { path: /ready, port: http }
            initialDelaySeconds: 5
            periodSeconds: 5
          livenessProbe:
            httpGet: { path: /health, port: http }
            initialDelaySeconds: 15
            periodSeconds: 20
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: ["ALL"]
---
apiVersion: v1
kind: Service
metadata:
  name: api
  namespace: prod
spec:
  selector:
    app.kubernetes.io/name: api
  ports:
    - name: http
      port: 80
      targetPort: http
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: api
  namespace: prod
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app.kubernetes.io/name: api
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api
  namespace: prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target: { type: Utilization, averageUtilization: 70 }
```

### NetworkPolicy default-deny + explicit allow

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: prod
spec:
  podSelector: {}        # all pods
  policyTypes: [Ingress]
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-allow-ingress
  namespace: prod
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: api
  policyTypes: [Ingress]
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
      ports:
        - protocol: TCP
          port: 8080
```

---

## SOTA tool reference (June 2026)

Grep-friendly per-tool reference. Each tool gets ~10-30 lines naming the verb, source, canonical command(s), and the bundled skill pack that deep-dives. Run any CLI through the `cli-anything` skill.

### docker buildx (BuildKit)

**Use for:** Multi-stage, multi-arch, cache-mounted container builds.
**Skill pack:** [`docker-multistage-buildkit-distroless`](skills/docker-multistage-buildkit-distroless/SKILL.md)
**Install:** comes with Docker Engine 23+
**Quick recipe:**
```bash
docker buildx create --use --name multi
docker buildx build --platform linux/amd64,linux/arm64 \
  --cache-from type=registry,ref=myreg.io/api:cache \
  --cache-to type=registry,ref=myreg.io/api:cache,mode=max \
  --push -t myreg.io/api:1.27.3 .
```
**Source:** https://docs.docker.com/build/buildkit/

### helm (3.x)

**Use for:** Parameterized K8s app packaging + OCI registry distribution.
**Skill pack:** [`kubernetes-deployments-helm-kustomize`](skills/kubernetes-deployments-helm-kustomize/SKILL.md)
**Install:** `curl https://baltocdn.com/helm/signing.asc | ... apt install helm`
**Quick recipe:**
```bash
helm create my-app && cd my-app
helm lint . && helm template . | kubeconform -strict
helm package . && helm push my-app-0.1.0.tgz oci://myreg.io/charts
helm upgrade --install my-app oci://myreg.io/charts/my-app --version 0.1.0 -f values.prod.yaml
```
**Source:** https://helm.sh/docs/

### kustomize

**Use for:** Overlay-based env-specific manifest patching.
**Skill pack:** [`kubernetes-deployments-helm-kustomize`](skills/kubernetes-deployments-helm-kustomize/SKILL.md)
**Install:** built into `kubectl` (`kubectl kustomize`); standalone `kustomize` CLI for advanced use.
**Quick recipe:**
```bash
# base/kustomization.yaml + overlays/{dev,staging,prod}/kustomization.yaml
kubectl diff -k overlays/prod
kubectl apply -k overlays/prod
```
**Source:** https://kustomize.io/

### tofu / terraform

**Use for:** Declarative cloud infra in HCL.
**Skill pack:** [`terraform-opentofu-iac`](skills/terraform-opentofu-iac/SKILL.md)
**Install:** `brew install opentofu` or download from https://opentofu.org/docs/intro/install/
**Quick recipe:**
```bash
tofu init -backend-config=backend.tfvars
tofu fmt -recursive && tofu validate
tflint --recursive
checkov -d . --framework terraform
infracost diff --path .
tofu plan -out=tfplan && tofu apply tfplan
```
**Source:** https://opentofu.org/docs/

### pulumi

**Use for:** Real-language IaC (Python/TS/Go/C#/Java).
**Skill pack:** [`pulumi-iac-python-typescript`](skills/pulumi-iac-python-typescript/SKILL.md)
**Install:** `curl -fsSL https://get.pulumi.com | sh`
**Quick recipe:**
```bash
pulumi new aws-typescript
pulumi config set --secret db-password "$(openssl rand -base64 32)"
pulumi preview --diff
pulumi up --yes
pulumi stack export --file backup.json
```
**Source:** https://www.pulumi.com/docs/

### cdk / sst / sam

**Use for:** AWS-native IaC (CloudFormation under the hood) — CDK for general; SST for serverless fullstack; SAM for Lambda-centric.
**Skill pack:** [`aws-cdk-sst-serverless`](skills/aws-cdk-sst-serverless/SKILL.md)
**Quick recipe:**
```bash
# CDK
cdk init app --language=typescript
cdk synth && cdk diff && cdk deploy --require-approval=never
# SST v3
npx create-sst@latest
sst deploy --stage=prod
# SAM
sam init && sam build && sam deploy --guided
```
**Source:** https://docs.aws.amazon.com/cdk/ · https://sst.dev/docs/ · https://docs.aws.amazon.com/serverless-application-model/

### gh (GitHub CLI) + Actions

**Use for:** Workflow trigger, log inspection, PR review, releases.
**Skill pack:** [`github-actions-cicd-oidc`](skills/github-actions-cicd-oidc/SKILL.md) (also `github` default skill)
**Install:** `brew install gh` or https://cli.github.com/
**Quick recipe:**
```bash
gh workflow run deploy.yml -f environment=prod
gh run watch
gh run view --log-failed
actionlint .github/workflows/*.yml
act -j build --container-architecture linux/amd64
gh pr create --fill --base main
gh pr checks --watch
```
**Source:** https://cli.github.com/manual/

### argocd

**Use for:** GitOps pull-based deployment to K8s.
**Skill pack:** [`argocd-flux-gitops`](skills/argocd-flux-gitops/SKILL.md)
**Install:** `brew install argocd` or `curl -sSL -o argocd ... github.com/argoproj/argo-cd/releases`
**Quick recipe:**
```bash
argocd login argocd.myorg.com
argocd app create api-prod --repo https://github.com/myorg/manifests \
  --path apps/api/overlays/prod --dest-server kubernetes.default.svc --dest-namespace prod \
  --sync-policy automated --auto-prune --self-heal
argocd app diff api-prod
argocd app sync api-prod
argocd app rollback api-prod <revision>
```
**Source:** https://argo-cd.readthedocs.io/

### flux

**Use for:** Alt GitOps controller (CNCF graduated; finer-grained controllers).
**Skill pack:** [`argocd-flux-gitops`](skills/argocd-flux-gitops/SKILL.md)
**Install:** `brew install fluxcd/tap/flux`
**Quick recipe:**
```bash
flux bootstrap github --owner=myorg --repository=infra --path=clusters/prod \
  --branch=main --personal=false
flux create source git api --url=https://github.com/myorg/api --branch=main
flux create kustomization api --source=GitRepository/api --path=./deploy --prune=true
flux reconcile kustomization api
flux get all -A
```
**Source:** https://fluxcd.io/flux/

### argo-rollouts

**Use for:** Canary + blue/green with metric analysis on K8s.
**Skill pack:** [`blue-green-canary-argo-rollouts`](skills/blue-green-canary-argo-rollouts/SKILL.md)
**Install:** `kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml` + `brew install argoproj/tap/kubectl-argo-rollouts`
**Quick recipe:**
```bash
kubectl argo rollouts get rollout api --watch
kubectl argo rollouts set image api api=myreg.io/api:1.27.3
kubectl argo rollouts promote api
kubectl argo rollouts abort api
```
**Source:** https://argo-rollouts.readthedocs.io/

### vault / openbao

**Use for:** Secret source-of-truth + dynamic credentials.
**Skill pack:** [`vault-doppler-pulumi-esc-secrets`](skills/vault-doppler-pulumi-esc-secrets/SKILL.md)
**Install:** `brew install vault` or OpenBao binary.
**Quick recipe:**
```bash
vault kv put secret/prod/api/db password=$(openssl rand -base64 32) host=db.prod
vault kv get secret/prod/api/db
vault read database/creds/api-role   # dynamic Postgres creds, short TTL
vault token create -policy=api-read -ttl=24h
```
**Source:** https://developer.hashicorp.com/vault/docs · https://openbao.org/

### external-secrets (ESO)

**Use for:** Sync external secrets into K8s Secret resources.
**Skill pack:** [`external-secrets-operator-k8s`](skills/external-secrets-operator-k8s/SKILL.md)
**Install:** `helm upgrade --install external-secrets external-secrets/external-secrets -n external-secrets --create-namespace`
**Quick recipe:**
```yaml
# ClusterSecretStore (Vault backend)
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata: { name: vault-backend }
spec:
  provider:
    vault:
      server: "https://vault.myorg.com"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "external-secrets"
---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata: { name: api-db, namespace: prod }
spec:
  refreshInterval: 1h
  secretStoreRef: { name: vault-backend, kind: ClusterSecretStore }
  target: { name: api-db }
  data:
    - secretKey: password
      remoteRef: { key: secret/prod/api/db, property: password }
```
**Source:** https://external-secrets.io/

### cosign (Sigstore)

**Use for:** Keyless image + SBOM signing via OIDC.
**Skill pack:** [`sigstore-slsa-supply-chain-attestation`](skills/sigstore-slsa-supply-chain-attestation/SKILL.md)
**Install:** `brew install cosign`
**Quick recipe:**
```bash
# Keyless sign (in CI, uses OIDC token; locally, opens browser flow)
cosign sign --yes myreg.io/api@sha256:6ba7b8...
# Attest SBOM
syft myreg.io/api -o cyclonedx-json > sbom.json
cosign attest --predicate sbom.json --type cyclonedx myreg.io/api@sha256:...
# Verify (admission)
cosign verify --certificate-identity-regexp='^https://github\.com/myorg/' \
  --certificate-oidc-issuer=https://token.actions.githubusercontent.com \
  myreg.io/api@sha256:...
```
**Source:** https://docs.sigstore.dev/cosign/

### trivy

**Use for:** Container/IaC/fs/secret/misconfig scanning.
**Skill pack:** [`trivy-snyk-container-scanning`](skills/trivy-snyk-container-scanning/SKILL.md)
**Install:** `brew install trivy`
**Quick recipe:**
```bash
trivy image --severity HIGH,CRITICAL --exit-code 1 --ignore-unfixed myreg.io/api:latest
trivy fs --scanners vuln,misconfig,secret .
trivy k8s --report summary cluster
trivy sbom sbom.json    # scan SBOM instead of image
```
**Source:** https://aquasecurity.github.io/trivy/

### syft

**Use for:** SBOM generation (SPDX / CycloneDX).
**Skill pack:** [`sigstore-slsa-supply-chain-attestation`](skills/sigstore-slsa-supply-chain-attestation/SKILL.md)
**Install:** `brew install syft`
**Quick recipe:**
```bash
syft myreg.io/api:1.27.3 -o cyclonedx-json > sbom.cyclonedx.json
syft myreg.io/api:1.27.3 -o spdx-json > sbom.spdx.json
syft dir:. -o cyclonedx-json    # scan project source
```
**Source:** https://github.com/anchore/syft

### opentelemetry-collector

**Use for:** Universal telemetry sink — receive OTLP/Prometheus/Jaeger, fan out to backends.
**Skill pack:** [`opentelemetry-instrumentation`](skills/opentelemetry-instrumentation/SKILL.md)
**Install:** `helm upgrade --install otel-collector open-telemetry/opentelemetry-collector -f values.yaml`
**Quick recipe (config snippet):**
```yaml
receivers:
  otlp: { protocols: { grpc: { endpoint: 0.0.0.0:4317 }, http: { endpoint: 0.0.0.0:4318 } } }
processors:
  batch: {}
  memory_limiter: { check_interval: 5s, limit_percentage: 80 }
  resource: { attributes: [{ key: deployment.environment, value: prod, action: upsert }] }
exporters:
  honeycomb: { endpoint: api.honeycomb.io:443, headers: { x-honeycomb-team: ${HC_KEY} } }
  prometheus: { endpoint: 0.0.0.0:8889 }
service:
  pipelines:
    traces: { receivers: [otlp], processors: [memory_limiter, resource, batch], exporters: [honeycomb] }
    metrics: { receivers: [otlp], processors: [memory_limiter, batch], exporters: [prometheus] }
```
**Source:** https://opentelemetry.io/docs/collector/

### prometheus + kube-prometheus-stack

**Use for:** Metric collection + alerting.
**Skill pack:** [`prometheus-grafana-loki-tempo-self-hosted`](skills/prometheus-grafana-loki-tempo-self-hosted/SKILL.md)
**Install:** `helm upgrade --install kps prometheus-community/kube-prometheus-stack -n monitoring --create-namespace`
**Source:** https://github.com/prometheus-operator/kube-prometheus

### loki / tempo / mimir / pyroscope (Grafana stack)

**Use for:** Logs / traces / long-term metrics / continuous profiling.
**Skill pack:** [`prometheus-grafana-loki-tempo-self-hosted`](skills/prometheus-grafana-loki-tempo-self-hosted/SKILL.md)
**Install (each):** Helm charts from `grafana/` repo.
**Source:** https://grafana.com/oss/

### vector

**Use for:** Modern log/metric router (Rust, replaces Fluentd/Bit).
**Skill pack:** [`prometheus-grafana-loki-tempo-self-hosted`](skills/prometheus-grafana-loki-tempo-self-hosted/SKILL.md)
**Install:** `brew install vectordotdev/brew/vector`
**Quick recipe:**
```bash
vector validate config.yaml
vector --config config.yaml
```
**Source:** https://vector.dev/

### sloth / pyrra

**Use for:** SLO → Prometheus rules generation.
**Skill pack:** [`slos-error-budgets-google-sre`](skills/slos-error-budgets-google-sre/SKILL.md)
**Install:** `brew install slok/repo/sloth` or `kubectl apply -f pyrra-operator.yaml`
**Quick recipe:**
```bash
sloth generate -i slos.yaml -o prometheus-rules.yaml
sloth validate -i slos.yaml
```
**Source:** https://sloth.dev/ · https://github.com/pyrra-dev/pyrra

### cert-manager

**Use for:** ACME-issued certs in K8s.
**Skill pack:** [`cert-manager-acme-tls`](skills/cert-manager-acme-tls/SKILL.md)
**Install:** `helm upgrade --install cert-manager jetstack/cert-manager --set installCRDs=true -n cert-manager --create-namespace`
**Quick recipe:**
```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata: { name: letsencrypt-prod }
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: ops@myorg.com
    privateKeySecretRef: { name: letsencrypt-prod-key }
    solvers:
      - dns01:
          cloudflare:
            apiTokenSecretRef: { name: cloudflare-api-token, key: api-token }
```
**Source:** https://cert-manager.io/docs/

### kyverno

**Use for:** K8s-native YAML policy admission control.
**Quick recipe:**
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata: { name: require-resource-limits }
spec:
  validationFailureAction: Enforce
  rules:
    - name: validate-resources
      match: { any: [{ resources: { kinds: [Pod] } }] }
      validate:
        message: "CPU and memory limits are required."
        pattern:
          spec:
            containers:
              - resources:
                  limits:
                    memory: "?*"
                    cpu: "?*"
```
**Source:** https://kyverno.io/docs/

### k6 (Grafana)

**Use for:** Load testing (JS scripts).
**Install:** `brew install k6`
**Quick recipe:**
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';
export const options = { vus: 100, duration: '5m', thresholds: { http_req_duration: ['p(95)<200'] } };
export default function () {
  const r = http.get('https://api.myorg.com/health');
  check(r, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
```
```bash
k6 run script.js
k6 cloud script.js
```
**Source:** https://k6.io/docs/

### infracost

**Use for:** Cost diff in IaC PRs.
**Skill pack:** [`cost-optimization-finops-infracost`](skills/cost-optimization-finops-infracost/SKILL.md)
**Install:** `brew install infracost`
**Quick recipe:**
```bash
infracost breakdown --path . --format json --out-file baseline.json
infracost diff --path . --compare-to baseline.json --format github-comment
```
**Source:** https://www.infracost.io/docs/

### opencost / karpenter / goldilocks

**Use for:** K8s cost / autoscale / right-sizing.
**Skill pack:** [`cost-optimization-finops-infracost`](skills/cost-optimization-finops-infracost/SKILL.md)
**Source:** https://www.opencost.io/ · https://karpenter.sh/ · https://goldilocks.fairwinds.com/

### velero

**Use for:** K8s cluster + PV backup/restore.
**Install:** `brew install velero`
**Quick recipe:**
```bash
velero install --provider aws --bucket myorg-velero --backup-location-config region=us-east-1 ...
velero backup create prod-2026-06-09 --include-namespaces=prod
velero schedule create nightly --schedule="@every 24h" --include-namespaces=prod --ttl 720h
velero restore create --from-backup prod-2026-06-09
```
**Source:** https://velero.io/

### backstage (Spotify)

**Use for:** Internal developer portal.
**Skill pack:** [`backstage-developer-portal`](skills/backstage-developer-portal/SKILL.md)
**Install:** `npx @backstage/create-app`
**Source:** https://backstage.io/docs

### k9s

**Use for:** TUI K8s navigator — fastest way to triage during incident.
**Install:** `brew install derailed/k9s/k9s`
**Quick recipe:**
```bash
k9s -n prod
# :pod → enter → l (logs) → / (filter)
# :deploy → enter → s (scale)
# :rollouts → enter → p (promote)
```
**Source:** https://k9scli.io/

### Other tools (no dedicated skill pack; documented in role.md)

- **flagger** — Flux-ecosystem progressive delivery — https://docs.flagger.app/
- **kubeconform** — fast K8s schema validator — https://github.com/yannh/kubeconform
- **actionlint** — GitHub Actions linter — https://github.com/rhysd/actionlint
- **act** — local GitHub Actions runner — https://github.com/nektos/act
- **tflint** — Terraform linter — https://github.com/terraform-linters/tflint
- **checkov** — IaC misconfig scanner — https://www.checkov.io/
- **gitleaks / trufflehog** — secrets detection
- **atlas** — declarative SQL migrations — https://atlasgo.io/
- **wrangler** — Cloudflare Workers CLI — https://developers.cloudflare.com/workers/wrangler/
- **opa / conftest** — policy-as-code — https://www.openpolicyagent.org/
- **falco** — runtime security — https://falco.org/
- **cilium** — eBPF networking + security — https://cilium.io/

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| Dockerfile / image build | `docker-multistage-buildkit-distroless` | Add cosign sign step + SBOM via syft for prod |
| K8s manifest / deployment | `kubernetes-deployments-helm-kustomize` | Helm if templating exists; else raw + Kustomize overlays |
| Terraform / OpenTofu module | `terraform-opentofu-iac` | OpenTofu default; tflint + checkov + infracost in CI |
| Pulumi program | `pulumi-iac-python-typescript` | TS for type-safety; Python for ML/data shops |
| AWS-specific IaC | `aws-cdk-sst-serverless` | CDK for general; SST for serverless fullstack; SAM for Lambda |
| CI/CD workflow | `github-actions-cicd-oidc` | OIDC trust mandatory; reusable workflows |
| GitOps deployment | `argocd-flux-gitops` | ArgoCD default; Flux if CNCF-only stack |
| Canary / blue-green rollout | `blue-green-canary-argo-rollouts` | Argo Rollouts + AnalysisTemplate against SLI |
| Feature flag wiring | `feature-flags-launchdarkly-statsig` | OpenFeature SDK + LD/Statsig/Unleash backend |
| Secret management | `vault-doppler-pulumi-esc-secrets` + `external-secrets-operator-k8s` | Vault SoT + ESO sync to K8s |
| Observability instrumentation | `opentelemetry-instrumentation` | OTel SDK + Collector + backend (separate pack for backend recipe) |
| Backend recipe (Honeycomb/Datadog) | `honeycomb-datadog-observability` | Backend-specific OTel exporter config |
| Self-hosted observability | `prometheus-grafana-loki-tempo-self-hosted` | kube-prometheus-stack + Grafana stack |
| SLO definition | `slos-error-budgets-google-sre` | Sloth or Pyrra → Prometheus rules |
| Paging / on-call / PIR | `pagerduty-incident-io-incident-response` | + sentry-mcp for error correlation |
| Container security scan | `trivy-snyk-container-scanning` | Trivy free default; Snyk for org policy |
| Supply chain attestation | `sigstore-slsa-supply-chain-attestation` | Cosign + Syft + SLSA |
| DNS / CDN / PaaS | `cloudflare-vercel-railway-fly-render-paas` | Cloudflare default; Vercel for frontend |
| Cost optimization | `cost-optimization-finops-infracost` | Infracost in PR + OpenCost in cluster |
| TLS / cert | `cert-manager-acme-tls` | cert-manager + Let's Encrypt + step-ca internal |
| Developer portal | `backstage-developer-portal` | Backstage IDP |

---

## Brief templates / Output templates

### Production-grade Dockerfile

```dockerfile
# syntax=docker/dockerfile:1.7
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim AS builder
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user uv && \
    /root/.local/bin/uv pip install --system --no-cache-dir -r requirements.txt
COPY . .

FROM gcr.io/distroless/python3-debian12:nonroot AS runtime
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app /app
EXPOSE 8080
USER nonroot
ENTRYPOINT ["python", "-m", "myapp"]
```

### Production-grade GitHub Actions workflow (OIDC + Cosign)

```yaml
name: build-sign-deploy
on:
  push:
    branches: [main]
permissions:
  id-token: write    # OIDC for AWS + Cosign
  contents: read
  packages: write
  attestations: write
jobs:
  build:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v5
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with: { registry: ghcr.io, username: ${{ github.actor }}, password: ${{ secrets.GITHUB_TOKEN }} }
      - id: build
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
          provenance: mode=max
          sbom: true
          cache-from: type=gha
          cache-to: type=gha,mode=max
      - uses: aquasecurity/trivy-action@master
        with:
          image-ref: ghcr.io/${{ github.repository }}:${{ github.sha }}
          severity: HIGH,CRITICAL
          exit-code: 1
      - uses: sigstore/cosign-installer@v3
      - run: cosign sign --yes ghcr.io/${{ github.repository }}@${{ steps.build.outputs.digest }}
  deploy:
    needs: build
    runs-on: ubuntu-24.04
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/gh-actions-deploy
          aws-region: us-east-1
      - run: |
          aws eks update-kubeconfig --name prod
          kubectl set image deployment/api api=ghcr.io/${{ github.repository }}@${{ needs.build.outputs.digest }}
```

### Runbook template

```markdown
# Runbook: <service> — <scenario>

## Severity
SEV1 / SEV2 / SEV3

## Impact
What users see; what SLI burns; revenue/SLA at risk.

## Symptoms
- Symptom 1 (specific log line, alert name, metric value)
- Symptom 2

## Diagnose
1. `kubectl logs --tail=200 -l app=<svc> -n prod`
2. `argocd app history <app>` — recent deploys
3. Sentry: filter by service + last 1h
4. Grafana dashboard: <URL>

## Mitigate
Choose first that applies:
- `kubectl rollout undo deployment <name> -n prod`  (30 sec)
- `argocd app rollback <app> <revision>`             (60 sec)
- Feature flag off: `curl -X PATCH https://app.launchdarkly.com/...`
- Scale down: `kubectl scale deployment <name> --replicas=0 -n prod`

## Recover
After mitigation, verify SLI returns to budget:
- `curl https://api.myorg.com/health`
- Grafana SLI panel green for 10 min

## Escalate
- Primary: @<slack-handle>
- Backup: @<slack-handle>
- Service owner: <team Slack channel>
- SEV1 only: VP Eng @<handle>
```

---

## Closing rules

Always: rebuild before patching, instrument before guessing, automate before repeating, defer to language/UI/data specialists for app-internal concerns. The contract between the app and the world is yours.
