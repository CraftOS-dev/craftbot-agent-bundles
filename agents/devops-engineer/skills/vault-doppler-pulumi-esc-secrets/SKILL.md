<!--
Source: https://developer.hashicorp.com/vault/docs · https://openbao.org/ · https://www.doppler.com/docs · https://www.pulumi.com/docs/pulumi-cloud/esc/ · https://infisical.com/docs
Authored: June 2026 for the devops-engineer agent bundle.
-->

# Vault / OpenBao / Doppler / Pulumi ESC / Infisical (Secret Source-of-Truth)

Centralized secret storage with dynamic credentials, audit logs, fine-grained
ACLs, and short TTLs. The source-of-truth tier — paired with ESO (see
`external-secrets-operator-k8s`) for K8s secret injection. Choose by team:
**Vault 1.17+** (HashiCorp, BSL since 2023), **OpenBao 2.0** (LF fork, OSS),
**Doppler** (managed SaaS, great UX), **Pulumi ESC** (envs+secrets+config,
ties to Pulumi), **Infisical** (OSS managed). All speak ESO; all support
versioning + access policies.

## When to use

- Anywhere a credential, API key, cert private key, or DB password exists
  outside Git.
- Rotating creds on schedule (Vault DB engine dynamic creds — 1 hour TTL).
- Replacing `kubectl create secret generic` workflows.
- Cross-team secret sharing with audit (who read which secret when).

Skip when: secrets are short-lived OIDC tokens (let the issuer handle it);
true zero-secret architecture (SPIFFE/SPIRE — out of scope here).

## Setup

```bash
# Vault
brew install vault                # OSS binary
# OR self-host on K8s
helm repo add hashicorp https://helm.releases.hashicorp.com
helm upgrade --install vault hashicorp/vault -n vault --create-namespace \
  --set "server.ha.enabled=true" \
  --set "server.ha.replicas=3" \
  --set "server.ha.raft.enabled=true"

# OpenBao (LF fork — same API)
brew install openbao
# OR Helm: helm repo add openbao https://openbao.github.io/openbao-helm

# Doppler
brew install dopplerhq/cli/doppler
doppler login
doppler setup       # selects project + config

# Pulumi ESC
curl -fsSL https://get.pulumi.com | sh
pulumi env init myorg/prod

# Infisical
brew install infisical/get-cli/infisical
infisical login
infisical init     # selects project + env
```

Authenticate to Vault (one of):

```bash
# Root token (initial only; rotate immediately)
export VAULT_TOKEN=$(vault operator init -key-shares=5 -key-threshold=3 -format=json | jq -r .root_token)

# Kubernetes auth (in-cluster)
vault auth enable kubernetes
vault write auth/kubernetes/config kubernetes_host=https://kubernetes.default.svc

# AWS IAM auth (EC2/EKS)
vault auth enable aws
vault write auth/aws/role/api auth_type=iam ...

# GitHub Actions OIDC
vault auth enable jwt
vault write auth/jwt/config bound_issuer=https://token.actions.githubusercontent.com \
  oidc_discovery_url=https://token.actions.githubusercontent.com
```

## Common recipes

### Recipe 1 — Vault KV v2 (static secrets)

```bash
vault secrets enable -path=secret kv-v2
vault kv put secret/prod/api/db password=$(openssl rand -base64 32) host=db.prod.local
vault kv get secret/prod/api/db
vault kv get -field=password secret/prod/api/db
vault kv list secret/prod/api/
vault kv metadata get secret/prod/api/db    # version history, lease, etc.
vault kv destroy -versions=3 secret/prod/api/db    # destroy a specific version
```

### Recipe 2 — Vault dynamic DB credentials (1h TTL)

```bash
vault secrets enable database
vault write database/config/prod-postgres \
  plugin_name=postgresql-database-plugin \
  allowed_roles="api-readwrite,api-readonly" \
  connection_url="postgresql://{{username}}:{{password}}@db.prod:5432/app" \
  username="vault" password="$(cat vault-bootstrap-pw)"

vault write database/roles/api-readwrite \
  db_name=prod-postgres \
  creation_statements="CREATE USER \"{{name}}\" WITH PASSWORD '{{password}}' IN ROLE app_rw VALID UNTIL '{{expiration}}';" \
  default_ttl=1h max_ttl=24h

vault read database/creds/api-readwrite
# username = v-token-api-readwrite-2026-06-09-...
# password = AAA...  (random 20 chars)
# lease    = expires in 1h
```

The app fetches creds at startup; Vault revokes them at TTL expiry.

### Recipe 3 — Vault transit (encryption-as-a-service)

```bash
vault secrets enable transit
vault write -f transit/keys/orders
vault write transit/encrypt/orders plaintext=$(echo -n "sensitive" | base64)
# Returns ciphertext: vault:v1:abc...
vault write transit/decrypt/orders ciphertext="vault:v1:abc..."
# Returns plaintext base64
```

App never stores the key — Vault holds it; app sends plaintext, gets
ciphertext.

### Recipe 4 — Vault policy (least-privilege ACL)

```hcl
# api-read.hcl
path "secret/data/prod/api/*" {
  capabilities = ["read"]
}
path "database/creds/api-readonly" {
  capabilities = ["read"]
}
```

```bash
vault policy write api-read api-read.hcl
vault write auth/kubernetes/role/api \
  bound_service_account_names=api \
  bound_service_account_namespaces=prod \
  policies=api-read ttl=24h
```

### Recipe 5 — Vault Agent Injector (K8s sidecar)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: api, namespace: prod }
spec:
  template:
    metadata:
      annotations:
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/role: api
        vault.hashicorp.com/agent-inject-secret-db: "secret/data/prod/api/db"
        vault.hashicorp.com/agent-inject-template-db: |
          {{- with secret "secret/data/prod/api/db" -}}
          DB_PASSWORD={{ .Data.data.password }}
          DB_HOST={{ .Data.data.host }}
          {{- end }}
    spec:
      serviceAccountName: api
      containers:
        - name: app
          image: ghcr.io/myorg/api:1.27.3
          envFrom:
            - { configMapRef: { name: api-config } }
          # Reads /vault/secrets/db on startup
```

Sidecar fetches the secret on pod startup; template rendered to
`/vault/secrets/db`.

### Recipe 6 — Doppler basics

```bash
doppler projects create my-app
doppler configs create prod --project my-app
doppler secrets set --project my-app --config prod DB_PASSWORD="$(openssl rand -base64 32)"
doppler secrets --project my-app --config prod    # list
doppler run --project my-app --config prod -- python app.py    # injects as env vars
doppler secrets download --project my-app --config prod --no-file --format env > .env.prod
```

Integrations: GitHub Actions (`doppler/secrets-fetch-action`), K8s (Doppler
K8s operator), Vercel/Railway native.

### Recipe 7 — Pulumi ESC environment

```bash
pulumi env init myorg/prod
pulumi env edit myorg/prod
```

```yaml
# myorg/prod.yaml
values:
  aws:
    login:
      fn::open::aws-login:
        oidc:
          duration: 1h
          roleArn: arn:aws:iam::123456789012:role/pulumi-prod
          sessionName: pulumi
  secrets:
    db-password:
      fn::secret: !!sec_AESGCM:dGhpcyBpcyBlbmNyeXB0ZWQ=
  files:
    KUBECONFIG:
      fn::open::aws-secrets-manager:
        region: us-east-1
        secretId: prod/kubeconfig
  environmentVariables:
    AWS_ACCESS_KEY_ID: ${aws.login.accessKeyId}
    AWS_SECRET_ACCESS_KEY: ${aws.login.secretAccessKey}
    AWS_SESSION_TOKEN: ${aws.login.sessionToken}
    DB_PASSWORD: ${secrets.db-password}
```

```bash
pulumi env open myorg/prod        # JSON of resolved values
pulumi env run myorg/prod -- aws s3 ls    # injects env vars + runs cmd
pulumi env set myorg/prod --secret secrets.db-password "$(openssl rand -base64 32)"
```

### Recipe 8 — Infisical basics

```bash
infisical init                                      # link project
infisical secrets set DB_PASSWORD="$(openssl rand -base64 32)" --env=prod
infisical secrets --env=prod
infisical run --env=prod -- python app.py            # injects env vars
infisical export --env=prod --format=dotenv > .env   # for local dev
infisical secrets folders create --path=/api --name=db --env=prod
```

K8s integration via Infisical Operator (CRDs analogous to ESO).

### Recipe 9 — Vault audit log

```bash
vault audit enable file file_path=/vault/logs/audit.log
tail -f /vault/logs/audit.log | jq .
# Every read/write logged with hmac'd request + response
```

Required for SOC 2 / ISO 27001 evidence.

### Recipe 10 — Vault seal / unseal (Shamir's secret sharing)

```bash
# Init creates 5 unseal keys; 3 needed to unseal
vault operator init -key-shares=5 -key-threshold=3
vault operator unseal $KEY1
vault operator unseal $KEY2
vault operator unseal $KEY3
# Vault now unsealed; can serve requests

# Auto-unseal with AWS KMS (prod)
vault server -config=config.hcl
# config.hcl includes:
# seal "awskms" { region = "us-east-1"  kms_key_id = "abcd-1234" }
```

### Recipe 11 — Compare and choose

| Tool | Best for | Pricing | OSS? |
|---|---|---|---|
| Vault 1.17 | Enterprise; dynamic creds; mature ecosystem | Enterprise paid; OSS BSL | Source-available (BSL) |
| OpenBao 2.0 | Same as Vault but truly OSS | Free | MPL-2.0 |
| Doppler | Mid-size team; great UX; SaaS | Free tier + paid | Closed source |
| Pulumi ESC | Pulumi shops; integrates with IaC | Free w/ Pulumi Cloud | Open SDK |
| Infisical | OSS-first; self-host | Free + cloud paid | MIT |
| AWS Secrets Mgr | AWS-only; native integration | Pay per secret | Closed |

## Examples

### Example 1 — Migrate `kubectl create secret` workflow to Vault + Agent Injector

**Goal:** Stop committing base64 secrets; rotate quarterly.

1. `vault kv put secret/prod/api/db password=$(openssl rand -base64 32)`.
2. Write Vault policy `api-read.hcl` (Recipe 4).
3. Enable K8s auth, bind to `api` ServiceAccount + namespace.
4. Add Vault Agent Injector annotations to Deployment (Recipe 5).
5. Pod restart → secret materializes at `/vault/secrets/db`.
6. Delete the old K8s Secret: `kubectl delete secret api-db -n prod`.
7. Audit confirms read on rotation: `tail /vault/logs/audit.log`.

**Result:** Zero base64 in Git; quarterly rotation via `vault kv put`.

### Example 2 — Wire GitHub Actions to Vault via OIDC

**Goal:** Deploy job fetches DB password from Vault without long-lived creds.

1. Enable JWT auth: `vault auth enable jwt`.
2. Configure: `vault write auth/jwt/config bound_issuer=... oidc_discovery_url=...`.
3. Create role tied to repo+branch: `vault write auth/jwt/role/gh-deploy ...`.
4. In workflow:

```yaml
- uses: hashicorp/vault-action@v3
  with:
    url: https://vault.myorg.com
    method: jwt
    role: gh-deploy
    secrets: |
      secret/data/prod/api/db password | DB_PASSWORD
```

5. `DB_PASSWORD` now exported as env var.

**Result:** No long-lived Vault token in CI.

## Edge cases / gotchas

- **Vault seal/unseal lockout:** lose >2 unseal keys = data unrecoverable.
  Distribute keys across 5 different people/storage locations.
- **`vault kv put` overwrites all keys at that path.** Use `vault kv patch`
  to update a single field; available in KV v2 only.
- **Vault TTL must respect database `max_ttl`.** If you request a
  `default_ttl` higher than `max_ttl`, the lease is silently capped.
- **Doppler free tier limits**: 3 users, 1 workplace. Paid for prod orgs.
- **Pulumi ESC requires Pulumi Cloud** (free for individuals, paid for
  teams). The ESC SDK is open but the resolution service is hosted.
- **OpenBao maintains API compatibility with Vault 1.14**; newer Vault-only
  features (e.g., HCP-specific) won't exist.
- **Vault Agent Injector and ESO can coexist** — Injector for synchronous
  per-pod fetch; ESO for `Secret` resource sync.
- **Audit logs grow fast** — rotate via logrotate + ship to Loki/Splunk for
  retention.
- **Secret renewal:** dynamic creds (DB engine) require the app to fetch a
  fresh lease before TTL expiry. Use the Vault SDK or sidecar; bare env vars
  don't auto-renew.
- **Encryption at rest:** Vault uses internal AES-GCM by default; backed by
  the seal (KMS auto-unseal in prod). Without auto-unseal, every restart
  needs manual unseal — never use in prod.
- **Doppler `service tokens` are long-lived** — rotate every 90 days.
  Doppler `oidc` integration is the better default.

## Sources

- https://developer.hashicorp.com/vault/docs — Vault docs
- https://developer.hashicorp.com/vault/docs/secrets/databases — dynamic DB creds
- https://developer.hashicorp.com/vault/docs/auth/jwt — OIDC/JWT auth
- https://developer.hashicorp.com/vault/docs/platform/k8s/injector — Agent Injector
- https://openbao.org/ — OpenBao (LF Vault fork)
- https://docs.doppler.com/ — Doppler docs
- https://www.pulumi.com/docs/pulumi-cloud/esc/ — Pulumi ESC
- https://infisical.com/docs — Infisical
- https://www.hashicorp.com/blog/announcing-vault-1-17 — Vault 1.17 release
- https://opensource.org/blog/openbao-vault-fork-mpl — OpenBao announcement
