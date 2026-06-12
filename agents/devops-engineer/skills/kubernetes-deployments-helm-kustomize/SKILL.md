<!--
Source: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/ · https://helm.sh/docs/ · https://kustomize.io/
Authored: June 2026 for the devops-engineer agent bundle.
-->

# Kubernetes Deployments + Helm + Kustomize

Author production-grade K8s workloads (Deployment, Service, Ingress,
ConfigMap, Secret, HPA, PDB, NetworkPolicy), package them as Helm charts
with `values.schema.json` validation, and layer env-specific patches via
Kustomize overlays. Includes Velero backups, Kyverno admission policies,
and vCluster ephemeral preview envs.

## When to use

- New service shipping to K8s — need the full manifest set.
- "Why is my pod CrashLoopBackOff?" — diagnose by reading the manifest.
- Helm chart authoring or adoption of someone else's chart.
- Kustomize overlay refactor (dev/staging/prod from one base).
- DR drill — restore namespace from Velero backup.
- Need a per-PR preview cluster (vCluster).

Skip when: just running an off-the-shelf chart (use the upstream Helm CLI
docs); pure infrastructure (use Terraform/Pulumi/Crossplane); serverless
PaaS (use `cloudflare-vercel-railway-fly-render-paas`).

## Setup

```bash
brew install kubectl helm kustomize kubeconform k9s velero kyverno
brew install derailed/k9s/k9s
curl -sSL "https://github.com/loft-sh/vcluster/releases/latest/download/vcluster-darwin-arm64" -o vcluster && chmod +x vcluster

# Recommended kubectl plugins
brew install krew
kubectl krew install neat tree resource-capacity who-can ctx ns
```

Cluster access: `aws eks update-kubeconfig --name prod --region us-east-1`
or `gcloud container clusters get-credentials prod --region us-central1` or
`az aks get-credentials --name prod --resource-group rg-prod`.

## Common recipes

### Recipe 1 — Production-grade Deployment + Service + PDB + HPA

```yaml
# k8s/api/deployment.yaml
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
    rollingUpdate: { maxSurge: 1, maxUnavailable: 0 }
  selector: { matchLabels: { app.kubernetes.io/name: api } }
  template:
    metadata:
      labels: { app.kubernetes.io/name: api, app.kubernetes.io/version: "1.27.3" }
    spec:
      serviceAccountName: api-svc
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        fsGroup: 10001
        seccompProfile: { type: RuntimeDefault }
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: ScheduleAnyway
          labelSelector: { matchLabels: { app.kubernetes.io/name: api } }
      containers:
        - name: api
          image: ghcr.io/myorg/api@sha256:6ba7b810...
          ports: [{ name: http, containerPort: 8080 }]
          resources:
            requests: { cpu: 100m, memory: 256Mi }
            limits:   { cpu: 500m, memory: 512Mi }
          readinessProbe:
            httpGet: { path: /ready, port: http }
            periodSeconds: 5
          livenessProbe:
            httpGet: { path: /health, port: http }
            initialDelaySeconds: 15
            periodSeconds: 20
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities: { drop: ["ALL"] }
          volumeMounts:
            - { name: tmp, mountPath: /tmp }
      volumes:
        - name: tmp
          emptyDir: { sizeLimit: 100Mi }
---
apiVersion: v1
kind: Service
metadata: { name: api, namespace: prod }
spec:
  selector: { app.kubernetes.io/name: api }
  ports: [{ name: http, port: 80, targetPort: http }]
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata: { name: api, namespace: prod }
spec:
  minAvailable: 2
  selector: { matchLabels: { app.kubernetes.io/name: api } }
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: { name: api, namespace: prod }
spec:
  scaleTargetRef: { apiVersion: apps/v1, kind: Deployment, name: api }
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource: { name: cpu, target: { type: Utilization, averageUtilization: 70 } }
```

### Recipe 2 — Ingress with cert-manager + path routing

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api
  namespace: prod
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
spec:
  ingressClassName: nginx
  tls:
    - hosts: [api.myorg.com]
      secretName: api-tls
  rules:
    - host: api.myorg.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend: { service: { name: api, port: { name: http } } }
```

### Recipe 3 — NetworkPolicy default-deny + explicit allow

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: default-deny-ingress, namespace: prod }
spec:
  podSelector: {}
  policyTypes: [Ingress]
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: api-allow-ingress, namespace: prod }
spec:
  podSelector: { matchLabels: { app.kubernetes.io/name: api } }
  policyTypes: [Ingress]
  ingress:
    - from:
        - namespaceSelector: { matchLabels: { name: ingress-nginx } }
      ports: [{ protocol: TCP, port: 8080 }]
```

### Recipe 4 — Helm chart scaffolding + lint + package + push (OCI)

```bash
helm create my-app && cd my-app
# edit values.yaml, templates/
helm lint .
helm template . -f values.yaml | kubeconform -strict -summary
helm package . --version 0.1.0 --app-version 1.27.3
helm push my-app-0.1.0.tgz oci://ghcr.io/myorg/charts
helm upgrade --install my-app oci://ghcr.io/myorg/charts/my-app \
  --version 0.1.0 -f values.prod.yaml -n prod --create-namespace
```

### Recipe 5 — `values.schema.json` for chart input validation

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "my-app values",
  "type": "object",
  "required": ["image", "replicaCount"],
  "properties": {
    "replicaCount": { "type": "integer", "minimum": 1 },
    "image": {
      "type": "object",
      "required": ["repository", "digest"],
      "properties": {
        "repository": { "type": "string" },
        "digest": { "type": "string", "pattern": "^sha256:[a-f0-9]{64}$" }
      }
    }
  }
}
```

`helm install` fails if values don't match — kill the "I forgot to set replicas
in prod" class of bugs.

### Recipe 6 — Kustomize base + overlay structure

```
manifests/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── hpa.yaml
└── overlays/
    ├── dev/    { kustomization.yaml, patches/replicas.yaml }
    ├── staging/{ kustomization.yaml, patches/replicas.yaml }
    └── prod/   { kustomization.yaml, patches/replicas.yaml }
```

```yaml
# overlays/prod/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: prod
resources: [../../base]
patches:
  - path: patches/replicas.yaml
images:
  - name: ghcr.io/myorg/api
    digest: sha256:6ba7b810f0ec...
configMapGenerator:
  - name: api-config
    literals:
      - LOG_LEVEL=info
      - OTEL_SERVICE_NAME=api
```

```bash
kustomize build overlays/prod | kubectl diff -f -
kustomize build overlays/prod | kubectl apply -f -
# OR shorter:
kubectl apply -k overlays/prod
```

### Recipe 7 — `kubeconform` schema check in CI

```bash
kustomize build overlays/prod | kubeconform -strict -summary \
  -schema-location default \
  -schema-location 'https://raw.githubusercontent.com/datreeio/CRDs-catalog/main/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json'
```

Fast schema validation including CRDs.

### Recipe 8 — Velero backup + scheduled DR

```bash
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.10.0 \
  --bucket myorg-velero \
  --backup-location-config region=us-east-1 \
  --snapshot-location-config region=us-east-1 \
  --secret-file ./credentials-velero

velero backup create prod-$(date +%Y-%m-%d) --include-namespaces=prod
velero schedule create nightly --schedule="0 2 * * *" \
  --include-namespaces=prod --ttl 720h
velero restore create --from-backup prod-2026-06-09 --namespace-mappings prod:prod-restored
```

### Recipe 9 — Kyverno admission policy: require resource limits

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata: { name: require-resource-limits }
spec:
  validationFailureAction: Enforce
  background: true
  rules:
    - name: validate-resources
      match: { any: [{ resources: { kinds: [Pod] } }] }
      validate:
        message: "CPU and memory limits are required."
        pattern:
          spec:
            containers:
              - resources:
                  limits: { memory: "?*", cpu: "?*" }
```

```bash
kubectl apply -f cluster-policy.yaml
kubectl get policyreport -A
```

### Recipe 10 — vCluster ephemeral preview per PR

```bash
vcluster create pr-1234 --namespace pr-1234 --connect=false
vcluster connect pr-1234 -- kubectl apply -k overlays/dev
# user opens preview URL routed by ingress + wildcard DNS
vcluster delete pr-1234   # at PR close
```

### Recipe 11 — Quick triage with k9s

```bash
k9s -n prod
# :pod → enter → l (logs) → /api (filter)
# :events → /Warning
# :deploy → enter → s (scale) → 5 → enter
# :rollouts → enter → p (promote)
```

### Recipe 12 — kubectl one-liners (incident triage)

```bash
kubectl get events -n prod --sort-by='.lastTimestamp' | tail -20
kubectl describe pod -n prod -l app.kubernetes.io/name=api
kubectl logs -n prod -l app.kubernetes.io/name=api --tail=200 --since=10m
kubectl top pods -n prod --sort-by=memory
kubectl rollout history deployment/api -n prod
kubectl rollout undo deployment/api -n prod        # rollback to N-1
kubectl rollout status deployment/api -n prod --watch
kubectl debug -n prod pod/api-abc-xyz -it --image=nicolaka/netshoot --target=api
```

## Examples

### Example 1 — Take a service from "1 replica, no limits" to prod-grade

**Goal:** Add HPA, PDB, NetworkPolicy, securityContext to `api` deployment.

1. Pull current manifest: `kubectl get deploy api -n prod -o yaml | kubectl-neat > current.yaml`.
2. Apply Recipe 1 fields (`securityContext`, `resources`, `topologySpread`).
3. Add Recipe 3 NetworkPolicy.
4. Add HPA from Recipe 1.
5. `kubectl apply -k overlays/prod` and watch: `kubectl rollout status deploy/api -n prod`.
6. Validate PDB: `kubectl get pdb api -n prod` shows `minAvailable: 2`.

**Result:** Pods spread across zones, auto-scale 3–20, zero downtime during drain.

### Example 2 — Adopt an upstream Helm chart safely

**Goal:** Install `bitnami/redis` in prod with custom values.

1. `helm repo add bitnami https://charts.bitnami.com/bitnami && helm repo update`.
2. `helm show values bitnami/redis > values.upstream.yaml` — diff what's available.
3. Write `values.prod.yaml` with overrides (auth.password from ESO, persistence.size=10Gi).
4. Dry-run: `helm template redis bitnami/redis -f values.prod.yaml -n prod | kubeconform -strict`.
5. `helm upgrade --install redis bitnami/redis -f values.prod.yaml -n prod --version 19.6.4 --atomic --wait`.

**Result:** Redis up; `--atomic` rolls back on failure; pinned chart version.

## Edge cases / gotchas

- **`maxUnavailable: 0` requires `replicas >= 2` or rollout hangs.** Set
  `minAvailable` on PDB to `replicas - 1` not a hard number.
- **`readOnlyRootFilesystem: true` breaks Python tempfile, pip cache, /tmp
  writes.** Mount `emptyDir` at every write path.
- **`HPA` with CPU metric needs `metrics-server`.** Install via
  `helm upgrade --install metrics-server metrics-server/metrics-server -n kube-system`.
- **`kubectl apply -f` does 3-way merge.** Removing a field from YAML doesn't
  remove it from the cluster unless it's a managed field. Use
  `kubectl apply --prune` or GitOps controllers.
- **Helm `--atomic` rolls back on failure**, but only if `--wait` is set;
  without `--wait`, rollout continues async.
- **Kustomize `images.digest` works only since v4.4+**; older versions use
  `images.newTag`.
- **`kubectl rollout undo` only goes back to N-1.** Older revisions need
  `--to-revision=<n>`. Keep `revisionHistoryLimit: 10` on the Deployment.
- **Velero cluster-level resources** (CRDs, ClusterRoles) need
  `--include-cluster-resources=true` explicitly.
- **Kyverno `Enforce`** mode rejects non-conforming manifests at admission;
  always start in `Audit` mode in prod to gauge impact.
- **vCluster CNI doesn't ship NetworkPolicy by default**; use a host-cluster
  NetworkPolicy targeting the vCluster namespace, or install Cilium inside.
- **`topologySpreadConstraints` with `whenUnsatisfiable: DoNotSchedule`**
  can starve scheduling if your AZ has no capacity. Default to
  `ScheduleAnyway`.

## Sources

- https://kubernetes.io/docs/concepts/workloads/controllers/deployment/ — Deployment docs
- https://kubernetes.io/docs/concepts/security/pod-security-standards/ — Pod Security Standards
- https://helm.sh/docs/ — Helm 3 reference
- https://helm.sh/docs/topics/registries/ — Helm OCI registries
- https://kustomize.io/ — Kustomize official site
- https://kubectl.docs.kubernetes.io/references/kustomize/ — Kustomize reference
- https://github.com/yannh/kubeconform — kubeconform schema validator
- https://velero.io/docs/ — Velero backup/restore
- https://kyverno.io/docs/ — Kyverno policy engine
- https://www.vcluster.com/docs — vCluster docs
- https://k9scli.io/ — k9s
