<!--
Source: https://external-secrets.io/ · https://github.com/external-secrets/external-secrets
Authored: June 2026 for the devops-engineer agent bundle.
-->

# External Secrets Operator (ESO) for Kubernetes

Sync secrets from external providers (Vault, AWS Secrets Manager, GCP Secret
Manager, Azure Key Vault, Doppler, 1Password, Infisical, GitHub, Pulumi ESC)
into Kubernetes `Secret` resources via `SecretStore` / `ClusterSecretStore`
and `ExternalSecret` CRDs. CNCF incubating; the 2026 standard pattern for
"secrets in Git without secrets in Git."

## When to use

- Migrating from `kubectl create secret` to GitOps-friendly secrets.
- One source-of-truth (Vault/SM/etc.) but many K8s clusters need the secrets.
- Per-namespace secret access without giving each tenant Vault creds.
- "Rotate the DB password" — change once in Vault, ESO refreshes K8s Secret
  on its interval, pods read on next restart (or sidecar reload).

Skip when: secrets live entirely inside K8s already (use Sealed Secrets);
truly transient creds (use Vault Agent Injector directly to skip the
K8s Secret resource).

## Setup

```bash
# Install via Helm
helm repo add external-secrets https://charts.external-secrets.io
helm upgrade --install external-secrets external-secrets/external-secrets \
  -n external-secrets --create-namespace \
  --version 0.10.x \
  --set installCRDs=true \
  --set webhook.port=9443

kubectl get crd | grep external-secrets    # confirm CRDs installed
# externalsecrets.external-secrets.io
# secretstores.external-secrets.io
# clustersecretstores.external-secrets.io
# clusterexternalsecrets.external-secrets.io
# pushsecrets.external-secrets.io
```

CRD versions: `external-secrets.io/v1beta1` (production stable, ≥0.9.x).
`v1` GA in 0.10.x.

## Common recipes

### Recipe 1 — ClusterSecretStore (Vault backend, K8s auth)

```yaml
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
          serviceAccountRef:
            name: external-secrets
            namespace: external-secrets
```

```bash
# Pre-req: configure Vault K8s auth role binding `external-secrets`
# (see vault-doppler-pulumi-esc-secrets skill, Recipe 4)
kubectl apply -f vault-secret-store.yaml
kubectl describe clustersecretstore vault-backend
# Status: Valid
```

### Recipe 2 — ExternalSecret pulling from Vault

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata: { name: api-db, namespace: prod }
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: api-db
    creationPolicy: Owner   # ESO creates the K8s Secret; deletes on ES delete
    deletionPolicy: Delete  # delete K8s Secret if ExternalSecret deleted
    template:
      type: Opaque
      metadata:
        labels: { app.kubernetes.io/name: api }
  data:
    - secretKey: DB_PASSWORD
      remoteRef:
        key: secret/data/prod/api/db
        property: password
    - secretKey: DB_HOST
      remoteRef:
        key: secret/data/prod/api/db
        property: host
```

```bash
kubectl apply -f api-db-external-secret.yaml
kubectl get externalsecret api-db -n prod
# STATUS: SecretSynced
kubectl get secret api-db -n prod -o yaml    # synced K8s Secret
```

### Recipe 3 — `dataFrom` (pull all keys from a path)

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata: { name: api-env, namespace: prod }
spec:
  refreshInterval: 30m
  secretStoreRef: { name: vault-backend, kind: ClusterSecretStore }
  target: { name: api-env }
  dataFrom:
    - extract:
        key: secret/data/prod/api/env       # all keys at path become Secret data
```

Now `secret/data/prod/api/env` keys `LOG_LEVEL`, `OTEL_SERVICE_NAME`, etc.
all materialize as Secret keys.

### Recipe 4 — AWS Secrets Manager via IRSA (IAM Role for ServiceAccount)

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata: { name: aws-sm }
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets
            namespace: external-secrets
```

Service account annotation for IRSA:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: external-secrets
  namespace: external-secrets
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/eso-aws-sm-reader
```

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata: { name: api-db, namespace: prod }
spec:
  refreshInterval: 1h
  secretStoreRef: { name: aws-sm, kind: ClusterSecretStore }
  target: { name: api-db }
  data:
    - secretKey: DB_PASSWORD
      remoteRef: { key: prod/api/db, property: password }
```

### Recipe 5 — GCP Secret Manager via Workload Identity

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata: { name: gcp-sm }
spec:
  provider:
    gcpsm:
      projectID: myorg-prod
      auth:
        workloadIdentity:
          clusterLocation: us-central1
          clusterName: prod
          serviceAccountRef:
            name: external-secrets
            namespace: external-secrets
```

### Recipe 6 — Azure Key Vault via Workload Identity

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata: { name: azkv }
spec:
  provider:
    azurekv:
      authType: WorkloadIdentity
      vaultUrl: "https://myorg-prod-kv.vault.azure.net"
      serviceAccountRef:
        name: external-secrets
        namespace: external-secrets
```

### Recipe 7 — Doppler provider

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata: { name: doppler }
spec:
  provider:
    doppler:
      project: my-app
      config: prod
      auth:
        secretRef:
          dopplerToken: { name: doppler-token, key: token, namespace: external-secrets }
```

### Recipe 8 — Template the Secret content

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata: { name: api-cfg, namespace: prod }
spec:
  refreshInterval: 1h
  secretStoreRef: { name: vault-backend, kind: ClusterSecretStore }
  target:
    name: api-cfg
    template:
      type: Opaque
      data:
        # Render a connection string from multiple Vault fields
        DATABASE_URL: "postgresql://{{ .username }}:{{ .password }}@{{ .host }}:5432/{{ .dbname }}"
        config.yaml: |
          log_level: info
          db:
            host: {{ .host }}
            password: {{ .password }}
  data:
    - secretKey: username
      remoteRef: { key: secret/data/prod/api/db, property: username }
    - secretKey: password
      remoteRef: { key: secret/data/prod/api/db, property: password }
    - secretKey: host
      remoteRef: { key: secret/data/prod/api/db, property: host }
    - secretKey: dbname
      remoteRef: { key: secret/data/prod/api/db, property: dbname }
```

### Recipe 9 — ClusterExternalSecret (fan-out across namespaces)

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ClusterExternalSecret
metadata: { name: org-ca }
spec:
  externalSecretName: org-ca
  namespaceSelector:
    matchLabels: { secret-target: yes }
  externalSecretSpec:
    refreshInterval: 24h
    secretStoreRef: { name: vault-backend, kind: ClusterSecretStore }
    target: { name: org-ca }
    data:
      - secretKey: ca.crt
        remoteRef: { key: secret/data/internal-ca, property: cert }
```

Every namespace labeled `secret-target=yes` gets a `Secret/org-ca`.

### Recipe 10 — PushSecret (Secret → Vault, reverse direction)

```yaml
apiVersion: external-secrets.io/v1alpha1
kind: PushSecret
metadata: { name: api-tls, namespace: prod }
spec:
  refreshInterval: 1h
  secretStoreRefs:
    - name: vault-backend
      kind: ClusterSecretStore
  selector:
    secret:
      name: api-tls       # K8s Secret created by cert-manager
  data:
    - match:
        secretKey: tls.crt
        remoteRef: { remoteKey: secret/prod/api/tls, property: crt }
    - match:
        secretKey: tls.key
        remoteRef: { remoteKey: secret/prod/api/tls, property: key }
```

Useful when cert-manager generates a cert and you want to back it up to Vault.

### Recipe 11 — Force resync

```bash
kubectl annotate externalsecret api-db \
  force-sync="$(date +%s)" -n prod --overwrite
# OR: kubectl delete externalsecret api-db && kubectl apply -f api-db.yaml
```

### Recipe 12 — Reloader for auto-restart on Secret change

```bash
helm upgrade --install reloader stakater/reloader -n reloader --create-namespace
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  namespace: prod
  annotations:
    reloader.stakater.com/auto: "true"
    # OR specific:
    secret.reloader.stakater.com/reload: "api-db,api-cfg"
spec: {...}
```

When ESO refreshes the Secret, Reloader detects + rolls the Deployment.

## Examples

### Example 1 — Replace 12 `kubectl create secret` calls with one ESO chart

**Goal:** Move all team-A secrets from cluster-local to Vault SoT.

1. `vault kv put secret/prod/team-a/<each-secret> ...` (one-time migration).
2. Author 1 `ClusterSecretStore` (Recipe 1) + 12 `ExternalSecret` manifests.
3. `kubectl apply -k overlays/prod/secrets/`.
4. Verify: `kubectl get externalsecret -n prod` all `SecretSynced`.
5. Roll deployments: `kubectl rollout restart -n prod deploy`.
6. Delete old K8s Secrets: `kubectl delete secret -n prod team-a-*`.

**Result:** Vault is SoT; rotation = single `vault kv put`.

### Example 2 — TLS cert rotation chain (cert-manager → Secret → ESO PushSecret → Vault)

**Goal:** cert-manager renews; copy renewed cert to Vault for disaster recovery.

1. cert-manager `Certificate` produces `Secret/api-tls` with renewed cert.
2. `PushSecret/api-tls` (Recipe 10) pushes to `secret/prod/api/tls` in Vault.
3. Vault audit log records rotation event.
4. If cluster is destroyed, restore by re-issuing the cert OR pulling from Vault into a new cluster's Secret via ExternalSecret.

**Result:** TLS material backed up automatically; DR ready.

## Edge cases / gotchas

- **`refreshInterval: 0`** disables refresh — secret syncs once. Useful for
  static, immutable secrets.
- **ESO doesn't auto-restart pods on secret update.** Pods continue with
  old secret in memory. Pair with Stakater Reloader (Recipe 12) or a
  sidecar that watches `/etc/secrets`.
- **Vault `kv-v2` paths require `data/` prefix** in `key`: use
  `secret/data/prod/api/db`, not `secret/prod/api/db`. ESO converts in
  some provider versions; verify with `kubectl describe externalsecret`.
- **`ExternalSecret` is namespace-scoped**; reads from `ClusterSecretStore`
  (cluster-scoped) or `SecretStore` (namespace-scoped). Naming clash =
  confusing errors. Prefer cluster-scoped stores with per-namespace
  `ExternalSecret`.
- **AWS IRSA + Pod Identity:** EKS Pod Identity is the 2024+ replacement
  for IRSA; ESO supports it via `auth.jwt` or new `auth.podIdentity`.
- **Rate limits**: ESO refreshes on `refreshInterval` × number of
  `ExternalSecret` × number of secrets. AWS Secrets Manager throttles at
  ~5000 req/sec; tune `refreshInterval` upward for large fleets.
- **`creationPolicy: Owner`** means deleting the `ExternalSecret` deletes
  the K8s Secret. `Merge` lets you co-manage (ESO + something else write
  different keys). `None` requires the Secret to pre-exist.
- **`dataFrom.extract`** pulls all keys; `dataFrom.find` lets you regex
  match.
- **Webhook failures** during ESO upgrade can block CRD updates. Use
  `--no-hooks` carefully; back up CRs first.
- **Audit:** ESO does not log every read to the secret backend by default.
  Backend audit logging (Vault audit, AWS CloudTrail) is your record.

## Sources

- https://external-secrets.io/ — ESO docs
- https://external-secrets.io/latest/provider/hashicorp-vault/ — Vault provider
- https://external-secrets.io/latest/provider/aws-secrets-manager/ — AWS SM provider
- https://external-secrets.io/latest/provider/google-secrets-manager/ — GCP SM provider
- https://external-secrets.io/latest/provider/azure-key-vault/ — Azure KV provider
- https://external-secrets.io/latest/api/externalsecret/ — ExternalSecret API
- https://external-secrets.io/latest/api/pushsecret/ — PushSecret API
- https://github.com/external-secrets/external-secrets — source
- https://github.com/stakater/Reloader — Reloader companion
- https://aws.amazon.com/blogs/containers/migrate-from-irsa-to-eks-pod-identity/ — IRSA → Pod Identity
