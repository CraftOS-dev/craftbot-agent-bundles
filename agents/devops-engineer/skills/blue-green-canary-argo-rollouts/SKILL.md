<!--
Source: https://argo-rollouts.readthedocs.io/en/stable/ · https://docs.flagger.app/
Authored: June 2026 for the devops-engineer agent bundle.
-->

# Blue/Green + Canary with Argo Rollouts (+ Flagger)

Progressive delivery on Kubernetes. **Argo Rollouts** (`Rollout` CRD with
`blueGreen` or `canary` strategy + `AnalysisTemplate` querying Prometheus/
Datadog/NewRelic for SLI). **Flagger** (Flux ecosystem alt). Replaces
`Deployment` for prod workloads where mid-rollout abort matters.

## When to use

- "How do we ship new versions without page-the-on-call risk?"
- Stateful or risky deploys where instant rollback matters.
- A/B testing infra layer (route 50/50 by version).
- SLO-aware rollouts: pause if error rate climbs during 25% canary stage.

Skip when: dev clusters (just use Deployments); single-replica services
(canary math doesn't work); fully stateless and you can re-deploy in < 30
sec.

## Setup

```bash
# Argo Rollouts controller (in-cluster)
kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml

# kubectl plugin
brew install argoproj/tap/kubectl-argo-rollouts

# Argo Rollouts dashboard (optional UI)
kubectl argo rollouts dashboard      # http://localhost:3100/rollouts

# Flagger (alternative)
helm repo add flagger https://flagger.app
helm upgrade --install flagger flagger/flagger -n flagger-system --create-namespace \
  --set meshProvider=nginx
```

Requires:
- An ingress / service mesh that splits traffic by weight (NGINX Ingress,
  Istio, Linkerd, AWS ALB, Traefik, App Mesh).
- Prometheus/Datadog/NewRelic for SLI metrics during analysis.

## Common recipes

### Recipe 1 — Canary Rollout (progressive %)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata: { name: api, namespace: prod }
spec:
  replicas: 10
  selector: { matchLabels: { app: api } }
  template:
    metadata: { labels: { app: api } }
    spec:
      containers:
        - name: api
          image: ghcr.io/myorg/api:v1.27.3
          resources:
            requests: { cpu: 100m, memory: 256Mi }
            limits:   { cpu: 500m, memory: 512Mi }
          readinessProbe:
            httpGet: { path: /ready, port: 8080 }
  strategy:
    canary:
      canaryService: api-canary          # routes 5%/25%/50%/100% to canary
      stableService: api-stable
      trafficRouting:
        nginx:
          stableIngress: api-ingress
      steps:
        - setWeight: 5
        - pause: { duration: 5m }
        - analysis:
            templates: [{ templateName: success-rate }]
            args: [{ name: service-name, value: api-canary }]
        - setWeight: 25
        - pause: { duration: 10m }
        - analysis:
            templates: [{ templateName: success-rate }]
            args: [{ name: service-name, value: api-canary }]
        - setWeight: 50
        - pause: { duration: 10m }
        - setWeight: 100
```

### Recipe 2 — Blue/Green Rollout

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata: { name: api, namespace: prod }
spec:
  replicas: 5
  selector: { matchLabels: { app: api } }
  template: # ...same as above
  strategy:
    blueGreen:
      activeService: api-active
      previewService: api-preview
      autoPromotionEnabled: false       # require manual promote
      scaleDownDelaySeconds: 300         # keep old "blue" pods for 5min
      prePromotionAnalysis:
        templates: [{ templateName: smoke-tests }]
        args: [{ name: service-name, value: api-preview }]
      postPromotionAnalysis:
        templates: [{ templateName: success-rate }]
        args: [{ name: service-name, value: api-active }]
```

### Recipe 3 — AnalysisTemplate (Prometheus SLI)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata: { name: success-rate, namespace: prod }
spec:
  args:
    - name: service-name
  metrics:
    - name: success-rate
      interval: 30s
      count: 5
      successCondition: result[0] >= 0.99      # 99% success
      failureLimit: 1                          # one failed sample = abort
      provider:
        prometheus:
          address: http://prometheus.monitoring:9090
          query: |
            sum(rate(http_requests_total{service="{{args.service-name}}",status!~"5.."}[1m]))
            /
            sum(rate(http_requests_total{service="{{args.service-name}}"}[1m]))
```

If success-rate samples drop below 99% during canary stages, Rollouts
auto-aborts and reverts to stable.

### Recipe 4 — Header-based traffic (experiment)

```yaml
strategy:
  canary:
    trafficRouting:
      istio:
        virtualService:
          name: api-vs
          routes: [primary]
    steps:
      - setHeaderRoute:
          name: "canary-header"
          match:
            - headerName: X-Canary
              headerValue: { exact: "true" }
      - pause: {}                       # indefinite — manual promote
```

Now `curl -H "X-Canary: true" https://api.myorg.com` routes to new version;
default traffic untouched. Useful for internal QA.

### Recipe 5 — Manual promote + abort

```bash
kubectl argo rollouts get rollout api --watch
kubectl argo rollouts promote api          # promote to next step
kubectl argo rollouts promote api --full   # skip remaining steps; go to 100%
kubectl argo rollouts abort api            # rollback
kubectl argo rollouts retry rollout api    # re-attempt after abort
kubectl argo rollouts set image api api=ghcr.io/myorg/api:v1.27.4
kubectl argo rollouts undo api             # rollback to prev revision
kubectl argo rollouts list rollouts -A
kubectl argo rollouts history api          # see all revisions
```

### Recipe 6 — Convert Deployment to Rollout

```yaml
# Before
apiVersion: apps/v1
kind: Deployment
metadata: { name: api }

# After — identical spec, just change kind + apiVersion
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata: { name: api }
spec:                                   # same as Deployment.spec
  workloadRef:                          # OR reference an external Deployment
    apiVersion: apps/v1
    kind: Deployment
    name: api
```

`workloadRef` lets you keep the Deployment + add a Rollout on top — useful
for partial migration.

### Recipe 7 — Flagger Canary (alternative)

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata: { name: api, namespace: prod }
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  service:
    port: 80
    targetPort: 8080
  analysis:
    interval: 1m
    threshold: 5                         # max failures before rollback
    maxWeight: 50
    stepWeight: 10
    metrics:
      - name: request-success-rate
        thresholdRange: { min: 99 }
        interval: 1m
      - name: request-duration
        thresholdRange: { max: 500 }     # 500ms p99
        interval: 30s
    webhooks:
      - name: smoke-test
        type: pre-rollout
        url: http://flagger-loadtester.test/
        timeout: 30s
        metadata:
          cmd: "hey -z 2m -q 10 -c 2 http://api-canary.prod/health"
```

### Recipe 8 — Argo Rollouts dashboard

```bash
kubectl argo rollouts dashboard
# http://localhost:3100/rollouts
# See: live progression, analysis results, traffic weights, promote/abort buttons
```

### Recipe 9 — Notifications (Slack on rollout abort)

```yaml
# rollouts-notifications-cm.yaml
apiVersion: v1
kind: ConfigMap
metadata: { name: argo-rollouts-notification-configmap, namespace: argo-rollouts }
data:
  service.slack: |
    token: $slack-token
  trigger.on-rollout-aborted: |
    - when: rollout.status.abort
      send: [rollout-aborted]
  template.rollout-aborted: |
    message: |
      Rollout {{.rollout.metadata.name}} ABORTED.
      Reason: {{.rollout.status.message}}
      Image: {{(index .rollout.spec.template.spec.containers 0).image}}
  subscriptions: |
    - recipients: [slack:platform-alerts]
      triggers: [on-rollout-aborted]
```

### Recipe 10 — k6 smoke-test prePromotion analysis

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata: { name: smoke-tests, namespace: prod }
spec:
  args: [{ name: service-name }]
  metrics:
    - name: k6-smoke
      provider:
        job:
          spec:
            template:
              spec:
                restartPolicy: Never
                containers:
                  - name: k6
                    image: grafana/k6:latest
                    command: [k6, run, /scripts/smoke.js]
                    env:
                      - { name: TARGET, value: 'http://{{args.service-name}}' }
                    volumeMounts: [{ name: scripts, mountPath: /scripts }]
                volumes:
                  - { name: scripts, configMap: { name: k6-scripts } }
```

Rollouts spawns a Job per analysis interval; pass/fail per Job exit code.

### Recipe 11 — ArgoCD + Rollouts (GitOps + progressive)

```yaml
# ArgoCD Application targets a Rollout instead of a Deployment
# argocd-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata: { name: api, namespace: argocd }
spec:
  source:
    repoURL: https://github.com/myorg/manifests
    path: apps/api/overlays/prod
    targetRevision: main
  destination: { namespace: prod, server: https://kubernetes.default.svc }
  syncPolicy:
    automated: { prune: true, selfHeal: true }
```

ArgoCD applies the new Rollout spec; the Rollout controller orchestrates
the canary. ArgoCD's "Synced" doesn't mean "fully rolled out" — check
`kubectl argo rollouts status`.

## Examples

### Example 1 — Convert flaky Deployment to canary Rollout

**Goal:** Stop bad deploys — 25% canary with success-rate guard.

1. Save current Deployment YAML; copy spec into new `Rollout` (Recipe 6).
2. Create `api-stable` + `api-canary` Services (selector matches `app=api`).
3. Add NGINX Ingress with canary annotation.
4. Apply AnalysisTemplate (Recipe 3) querying Prometheus.
5. Switch CI: instead of `kubectl set image deployment/api`, use
   `kubectl argo rollouts set image api api=...`.
6. Test: ship a known-bad image; verify auto-abort at 25% stage.

**Result:** Bad deploys auto-roll-back without paging.

### Example 2 — Blue/Green for stateful migration

**Goal:** DB schema migration; need atomic cutover.

1. Apply Recipe 2 — `blueGreen` with `autoPromotionEnabled: false`.
2. Push v1.27.3 (with new schema reader): `kubectl argo rollouts set image api ...`.
3. Preview service `api-preview` routes to v1.27.3; active still v1.27.2.
4. Run migrations against the DB (schema is backwards-compatible).
5. Smoke-test preview: `curl -H "Host: api-preview.myorg.com" ...`.
6. `kubectl argo rollouts promote api` — active service flips to v1.27.3.
7. After 5 min (`scaleDownDelaySeconds`), old "blue" pods scale to 0.

**Result:** Instant traffic flip; old pods kept warm for instant revert.

## Edge cases / gotchas

- **Canary requires traffic splitting** at the ingress/mesh layer.
  Without it, Rollouts can only scale replicas proportionally — coarser.
- **`pause: {}` (no duration)** waits indefinitely; require manual
  `promote`. Useful for QA-driven canaries.
- **`failureLimit: 0`** in AnalysisTemplate = abort on the FIRST bad sample.
  Default `failureLimit: 0` for safety; raise if Prometheus is flaky.
- **`AnalysisTemplate` inconsistent metrics window**: short `interval` +
  short metric query window = high variance. Use ≥ 1min queries.
- **Rollout `status.message: "found 1 down out of N"`** during canary —
  expected; canary pods start up while stable pods serve.
- **`workloadRef` Deployment** must not be GitOps-managed if Rollout will
  scale it — conflict between ArgoCD scaling Deployment back and Rollout
  scaling it forward.
- **`scaleDownDelaySeconds`** for blue/green keeps old pods running —
  costs $$$. Tune to "minimum time to detect rollback need".
- **NGINX Ingress canary annotations** require the `nginx.ingress.kubernetes.io/canary-*`
  set. Argo Rollouts manages these via `stableIngress` config — don't
  hand-set.
- **Istio VirtualService weight changes** propagate via Pilot; brief flakes
  during weight change. Use Linkerd if you need crisper cuts.
- **`kubectl rollout` (Deployment cmd)** does NOT work on Rollouts. Use
  `kubectl argo rollouts`.
- **Flagger vs Argo Rollouts**: Flagger ties to Flux; Argo Rollouts ties
  to Argo ecosystem. Pick by your CD controller. Capabilities parity.

## Sources

- https://argo-rollouts.readthedocs.io/ — Argo Rollouts docs
- https://argo-rollouts.readthedocs.io/en/stable/features/canary/ — canary docs
- https://argo-rollouts.readthedocs.io/en/stable/features/bluegreen/ — blue/green docs
- https://argo-rollouts.readthedocs.io/en/stable/features/analysis/ — AnalysisTemplate
- https://docs.flagger.app/ — Flagger docs
- https://martinfowler.com/bliki/BlueGreenDeployment.html — Martin Fowler blue/green
- https://www.split.io/blog/canary-deployments/ — canary patterns
- https://argo-rollouts.readthedocs.io/en/stable/best-practices/ — best practices
