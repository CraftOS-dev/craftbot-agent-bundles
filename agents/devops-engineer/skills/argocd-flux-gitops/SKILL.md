<!--
Source: https://argo-cd.readthedocs.io/en/stable/ · https://fluxcd.io/flux/ · https://opengitops.dev/
Authored: June 2026 for the devops-engineer agent bundle.
-->

# ArgoCD / Flux GitOps

Pull-based GitOps for Kubernetes — Git is the source of truth; an in-cluster
controller reconciles. Use **ArgoCD** (CNCF graduated, App-of-Apps,
ApplicationSets, image-updater, web UI) or **Flux v2** (CNCF graduated,
finer-grained controllers, no UI, minimal). Both implement the
OpenGitOps v1.0 principles: declarative, versioned, pulled, observed.

## When to use

- "How do we deploy?" → answer is "merge a PR; the cluster pulls".
- Multi-environment promotion (`dev → staging → prod` via PR).
- Multi-cluster fleet management.
- Drift detection between Git and cluster.
- Auto-promote new image digests when CI pushes (image-updater).

Skip when: there's no K8s (use Terraform + Atlantis); single-developer
hobby project (just `kubectl apply`); deployment frequency is < 1/month
(GitOps overhead doesn't pay off).

## Setup

```bash
brew install argocd
brew install fluxcd/tap/flux

# ArgoCD install (in-cluster)
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v2.13.0/manifests/install.yaml

# Flux install (bootstrap = installs + creates Git source pointing at this repo)
flux bootstrap github \
  --owner=myorg \
  --repository=infra \
  --branch=main \
  --path=clusters/prod \
  --personal=false

# Login (ArgoCD)
kubectl port-forward -n argocd svc/argocd-server 8080:443 &
argocd login localhost:8080 --username admin --password $(kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 -d)
```

Auth via GitHub OAuth / SSO is recommended for prod — disable the local
`admin` account after onboarding (`argocd account update-password`).

## Common recipes

### Recipe 1 — ArgoCD Application (single app)

```yaml
# clusters/prod/apps/api.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: api
  namespace: argocd
  finalizers: [resources-finalizer.argocd.argoproj.io]
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/manifests
    targetRevision: main
    path: apps/api/overlays/prod
  destination:
    server: https://kubernetes.default.svc
    namespace: prod
  syncPolicy:
    automated: { prune: true, selfHeal: true }
    syncOptions:
      - CreateNamespace=true
      - ServerSideApply=true
      - PruneLast=true
    retry:
      limit: 5
      backoff: { duration: 30s, factor: 2, maxDuration: 5m }
```

```bash
argocd app create -f api.yaml
argocd app sync api
argocd app get api
argocd app diff api
argocd app rollback api 12       # to revision 12
```

### Recipe 2 — App-of-Apps pattern

```yaml
# clusters/prod/root.yaml — one root references many child Applications
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata: { name: root, namespace: argocd }
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/manifests
    targetRevision: main
    path: clusters/prod/apps
  destination: { server: https://kubernetes.default.svc, namespace: argocd }
  syncPolicy: { automated: { prune: true, selfHeal: true } }
```

```
clusters/prod/apps/
├── api.yaml
├── worker.yaml
├── monitoring.yaml
└── ingress.yaml
```

Apply once: `kubectl apply -f clusters/prod/root.yaml -n argocd`. Root
syncs children; children sync their respective workloads. One-click cluster
bootstrap.

### Recipe 3 — ApplicationSet (fan-out)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata: { name: api-clusters, namespace: argocd }
spec:
  generators:
    - matrix:
        generators:
          - list:
              elements:
                - { cluster: prod-us-east-1, url: https://prod-us-east-1.example.com }
                - { cluster: prod-eu-west-1, url: https://prod-eu-west-1.example.com }
                - { cluster: prod-ap-south-1, url: https://prod-ap-south-1.example.com }
          - git:
              repoURL: https://github.com/myorg/manifests
              revision: main
              directories:
                - path: apps/*
  template:
    metadata: { name: '{{path.basename}}-{{cluster}}' }
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/manifests
        targetRevision: main
        path: '{{path}}/overlays/{{cluster}}'
      destination:
        server: '{{url}}'
        namespace: '{{path.basename}}'
      syncPolicy: { automated: { prune: true, selfHeal: true } }
```

Generates `<app>-<cluster>` Applications for every app × every cluster.

### Recipe 4 — Sync waves (ordering)

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: prod
  annotations: { argocd.argoproj.io/sync-wave: "-2" }
---
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: vault
  annotations: { argocd.argoproj.io/sync-wave: "-1" }
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  annotations: { argocd.argoproj.io/sync-wave: "0" }
```

Lower wave numbers sync first.

### Recipe 5 — argocd-image-updater

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: api
  annotations:
    argocd-image-updater.argoproj.io/image-list: api=ghcr.io/myorg/api
    argocd-image-updater.argoproj.io/api.update-strategy: digest
    argocd-image-updater.argoproj.io/api.allow-tags: regexp:^main-[a-f0-9]+$
    argocd-image-updater.argoproj.io/write-back-method: git
    argocd-image-updater.argoproj.io/git-branch: main
```

Image-updater watches the registry, opens a PR (or direct commit) to bump
the digest in Git, ArgoCD syncs.

### Recipe 6 — Flux GitRepository + Kustomization

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata: { name: api, namespace: flux-system }
spec:
  interval: 1m
  url: https://github.com/myorg/manifests
  ref: { branch: main }
---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata: { name: api-prod, namespace: flux-system }
spec:
  interval: 5m
  path: ./apps/api/overlays/prod
  prune: true
  sourceRef: { kind: GitRepository, name: api }
  targetNamespace: prod
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: api
      namespace: prod
  timeout: 5m
```

### Recipe 7 — Flux HelmRelease

```yaml
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
metadata: { name: cert-manager, namespace: cert-manager }
spec:
  interval: 10m
  chart:
    spec:
      chart: cert-manager
      version: "1.15.x"
      sourceRef: { kind: HelmRepository, name: jetstack, namespace: flux-system }
  values:
    installCRDs: true
  install: { createNamespace: true }
  upgrade: { remediation: { remediateLastFailure: true } }
```

### Recipe 8 — Flux image automation

```yaml
# Detect new tags
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImageRepository
metadata: { name: api, namespace: flux-system }
spec:
  image: ghcr.io/myorg/api
  interval: 1m
---
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImagePolicy
metadata: { name: api, namespace: flux-system }
spec:
  imageRepositoryRef: { name: api }
  policy: { semver: { range: '>=1.0.0' } }
---
# Write back to Git
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImageUpdateAutomation
metadata: { name: api, namespace: flux-system }
spec:
  interval: 5m
  sourceRef: { kind: GitRepository, name: api }
  git:
    checkout: { ref: { branch: main } }
    commit:
      author: { email: flux@myorg.com, name: Flux }
      messageTemplate: "chore: bump api to {{ .Updated.Images }}"
    push: { branch: flux-image-updates }
  update: { path: ./apps/api/overlays/prod }
```

### Recipe 9 — ArgoCD notifications (Slack)

```yaml
# argocd-notifications-cm.yaml
apiVersion: v1
kind: ConfigMap
metadata: { name: argocd-notifications-cm, namespace: argocd }
data:
  service.slack: |
    token: $slack-token
  template.app-sync-failed: |
    message: |
      Application {{.app.metadata.name}} sync failed.
      Sync status: {{.app.status.sync.status}}
      Reason: {{.app.status.operationState.message}}
  trigger.on-sync-failed: |
    - when: app.status.operationState.phase in ['Error', 'Failed']
      send: [app-sync-failed]
  subscriptions: |
    - recipients: [slack:platform-alerts]
      triggers: [on-sync-failed]
```

### Recipe 10 — ArgoCD CLI ops

```bash
argocd app list
argocd app get api --refresh
argocd app diff api
argocd app sync api --prune
argocd app sync api --resource apps:Deployment:api
argocd app history api
argocd app rollback api 42
argocd app set api --revision feature/canary --sync-policy none
argocd cluster add prod-eu-west-1     # add another K8s cluster
argocd repo add https://github.com/myorg/manifests --username git --password $TOKEN
```

### Recipe 11 — Flux CLI ops

```bash
flux get all -A
flux get sources git
flux get kustomizations
flux reconcile source git api
flux reconcile kustomization api-prod --with-source
flux suspend kustomization api-prod
flux resume kustomization api-prod
flux trace deployment/api -n prod      # which Flux objects manage this
flux events -A
```

### Recipe 12 — Disaster: stuck rollout, rollback in 60s

```bash
# ArgoCD
argocd app history api
argocd app rollback api 41        # back to revision 41

# Flux
flux suspend kustomization api-prod
git revert <bad-sha>; git push     # or `flux delete kustomization` then re-apply
flux resume kustomization api-prod
```

## Examples

### Example 1 — Bootstrap fresh cluster with App-of-Apps

**Goal:** From a fresh EKS cluster to fully running prod workloads.

1. Install ArgoCD: `kubectl apply -n argocd -f manifests/install.yaml`.
2. Apply root: `kubectl apply -f clusters/prod/root.yaml`.
3. Watch: `argocd app sync root --watch` — root syncs child apps in waves.
4. Verify: `kubectl get applications -n argocd` shows all `Synced + Healthy`.

**Result:** Cluster fully provisioned via 1 `kubectl apply`.

### Example 2 — Migrate from ArgoCD to Flux (CNCF-only mandate)

**Goal:** Stop using ArgoCD; standardize on Flux v2.

1. `flux bootstrap github --owner=myorg --repository=infra --path=clusters/prod`.
2. For each ArgoCD `Application`, write a `Flux Kustomization` (Recipe 6).
3. Run side-by-side: ArgoCD on namespace `argocd`, Flux on namespace `flux-system`.
4. Set ArgoCD apps to manual sync; verify Flux reconciles identical state.
5. `argocd app delete <app> --cascade=false` (keep workloads); `kubectl delete ns argocd`.

**Result:** Same workloads, now reconciled by Flux only.

## Edge cases / gotchas

- **`syncPolicy.automated.prune: true`** will delete resources removed
  from Git — including PVs/PVCs if you're not careful. Use
  `argocd.argoproj.io/sync-options: Prune=false` on stateful resources.
- **`selfHeal: true`** undoes any out-of-band `kubectl edit`. Some teams
  disable in dev to allow experimentation; always on in prod.
- **`ServerSideApply=true`** is recommended for CRDs and large manifests
  (avoids the 256 KB annotation size limit of client-side apply).
- **Sync waves are per-resource, not per-app.** For app-level ordering, use
  ApplicationSet with `syncPolicy.preserveResourcesOnDeletion` + explicit
  dependencies via `argocd.argoproj.io/sync-wave` on the Application CRDs.
- **ArgoCD image-updater + Flux image automation both rely on registry
  polling.** Pulls increase egress cost on large registries; tune
  `interval`.
- **Helm chart in Git vs Helm chart from OCI:** ArgoCD `source.chart` field
  pulls from OCI; `source.path` reads chart from Git. OCI is faster but
  needs registry credentials.
- **Flux Kustomization `prune: true`** deletes everything labeled with
  the inventory; if you change the path, old resources at the old path are
  deleted.
- **Multi-source Applications (ArgoCD 2.6+)** allow merging Helm values from
  a separate Git repo — useful for env-specific values without per-env charts.
- **`argocd app diff`** shows live state vs Git — sometimes false positives
  from defaulted fields (`creationTimestamp`, `status`). Ignore noise via
  `argocd.argoproj.io/compare-options: IgnoreExtraneous`.
- **ArgoCD's `cluster-admin` default:** the `argocd-application-controller`
  has cluster-admin in target clusters. Scope down via
  AppProject `clusterResourceWhitelist`.
- **Flux `--allow-cluster-mutation`** flag is required for `flux install`
  in air-gapped environments.

## Sources

- https://argo-cd.readthedocs.io/en/stable/ — ArgoCD docs
- https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/ — App-of-Apps
- https://argocd-image-updater.readthedocs.io/ — image-updater
- https://fluxcd.io/flux/ — Flux v2 docs
- https://fluxcd.io/flux/components/image/imageupdateautomations/ — Flux image automation
- https://opengitops.dev/ — OpenGitOps Principles v1.0
- https://www.cncf.io/blog/2022/12/02/argocd-vs-flux-which-one-should-i-use/ — ArgoCD vs Flux comparison
- https://github.com/argoproj-labs/argocd-autopilot — automated ArgoCD bootstrap
