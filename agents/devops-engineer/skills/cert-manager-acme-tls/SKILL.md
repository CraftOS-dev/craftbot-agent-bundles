<!--
Source: https://cert-manager.io/docs/ · https://letsencrypt.org/docs/ · https://smallstep.com/docs/step-ca/
Authored: June 2026 for the devops-engineer agent bundle.
-->

# cert-manager + ACME + step-ca + trust-manager

Automate TLS certificate issuance, renewal, and distribution in Kubernetes.
**cert-manager** (CNCF graduated) integrates with **Let's Encrypt** (free
public certs), **ZeroSSL**, **DigiCert**, **AWS PCA**, or internal **step-ca**
(open-source internal PKI). **trust-manager** distributes CA bundles to
namespaces. ACME-01 HTTP / DNS challenges. Wildcard certs require DNS-01.

## When to use

- New cluster — need HTTPS for every service.
- "Our cert expired and prod went down" — auto-renewal needed.
- Internal mTLS — issue per-service certs from an internal CA.
- "We have 50 microservices, each needs a cert" — cert-manager scales.
- ZTA / mTLS via Istio/Linkerd — they use cert-manager underneath.

Skip when: PaaS handles TLS (Vercel, Cloudflare, Fly do this); cluster has
zero ingress (no need).

## Setup

```bash
helm repo add jetstack https://charts.jetstack.io
helm upgrade --install cert-manager jetstack/cert-manager \
  -n cert-manager --create-namespace \
  --version 1.15.x \
  --set installCRDs=true \
  --set crds.enabled=true \
  --set prometheus.enabled=true

# Verify
kubectl get pods -n cert-manager
# cert-manager / cert-manager-cainjector / cert-manager-webhook

# trust-manager (CA bundle distribution)
helm upgrade --install trust-manager jetstack/trust-manager \
  -n cert-manager --version 0.12.x

# step-ca for internal PKI (alternative to ACME)
brew install step
step ca init --name "MyOrg Internal CA" --dns "ca.internal" --address ":443"
```

## Common recipes

### Recipe 1 — ClusterIssuer (Let's Encrypt + HTTP-01)

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
      - http01:
          ingress: { class: nginx }
---
# Staging issuer (don't hit LE rate limits during testing)
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata: { name: letsencrypt-staging }
spec:
  acme:
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    email: ops@myorg.com
    privateKeySecretRef: { name: letsencrypt-staging-key }
    solvers:
      - http01: { ingress: { class: nginx } }
```

Always test on staging issuer first; LE has strict rate limits (5
duplicate certs/week).

### Recipe 2 — Ingress with auto-cert annotation

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api
  namespace: prod
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
    - hosts: [api.myorg.com]
      secretName: api-tls         # cert-manager creates + manages this
  rules:
    - host: api.myorg.com
      http:
        paths:
          - { path: /, pathType: Prefix, backend: { service: { name: api, port: { name: http } } } }
```

cert-manager watches Ingress; creates `Certificate` → solves ACME →
writes `Secret/api-tls`.

### Recipe 3 — DNS-01 challenge (for wildcards)

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata: { name: letsencrypt-dns-cf }
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: ops@myorg.com
    privateKeySecretRef: { name: letsencrypt-dns-cf-key }
    solvers:
      - dns01:
          cloudflare:
            apiTokenSecretRef:
              name: cloudflare-api-token
              key: api-token
```

```bash
kubectl create secret generic cloudflare-api-token \
  -n cert-manager \
  --from-literal=api-token=$CLOUDFLARE_API_TOKEN
```

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata: { name: wildcard-myorg, namespace: prod }
spec:
  secretName: wildcard-myorg-tls
  issuerRef: { name: letsencrypt-dns-cf, kind: ClusterIssuer }
  dnsNames:
    - "*.myorg.com"
    - myorg.com
```

DNS-01 works for wildcards; HTTP-01 doesn't (LE restriction).

### Recipe 4 — Route53 DNS-01 (AWS)

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata: { name: letsencrypt-route53 }
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: ops@myorg.com
    privateKeySecretRef: { name: letsencrypt-route53-key }
    solvers:
      - dns01:
          route53:
            region: us-east-1
            hostedZoneID: Z123456ABCDEFG
            # IRSA: cert-manager SA assumes role with DNS-write permission
```

ServiceAccount annotated for IRSA:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: cert-manager
  namespace: cert-manager
  annotations: { eks.amazonaws.com/role-arn: arn:aws:iam::...:role/cert-manager-route53 }
```

### Recipe 5 — Internal PKI with step-ca

```bash
# Bootstrap
step ca init --name "MyOrg" --dns "ca.internal" --address ":443" --provisioner admin@myorg.com

# Run as K8s deployment (Helm chart available)
helm repo add smallstep https://smallstep.github.io/helm-charts
helm upgrade --install step-ca smallstep/step-certificates -n step-ca --create-namespace
```

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata: { name: step-ca-internal }
spec:
  vault:
    server: https://step-ca.step-ca:443
    path: pki_int/sign/internal
    auth:
      tokenSecretRef: { name: step-ca-token, key: token }
```

OR cert-manager has native step-ca integration via the
`smallstep/cert-manager-issuer` controller.

### Recipe 6 — Verify certificate status

```bash
kubectl get certificate -n prod
# NAME    READY   SECRET    AGE
# api     True    api-tls   10m

kubectl describe certificate api -n prod
# Events: ... Issuing certificate ... Order created ... Challenge solved ... Issued certificate

kubectl get certificaterequest -n prod
kubectl get challenge -n prod      # only during issuance

# Inspect issued cert
kubectl get secret api-tls -n prod -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -text -noout | head -20
```

### Recipe 7 — Force renewal

```bash
# Renew by recreating the Certificate
kubectl annotate certificate api -n prod cert-manager.io/issue-temporary-certificate="true" --overwrite

# OR via cmctl
brew install cmctl
cmctl renew api -n prod
```

cert-manager auto-renews 2/3 through the cert's lifetime (e.g., LE 90d
→ renews at 60d).

### Recipe 8 — trust-manager for CA bundle distribution

```yaml
apiVersion: trust.cert-manager.io/v1alpha1
kind: Bundle
metadata: { name: myorg-ca-bundle }
spec:
  sources:
    - useDefaultCAs: true     # public CAs
    - secret:
        name: step-ca-cert
        namespace: cert-manager
        key: ca.crt
  target:
    configMap: { key: ca-bundle.crt }
    namespaceSelector: { matchLabels: { trust: myorg } }
```

ConfigMap `myorg-ca-bundle` materializes in every namespace labeled
`trust: myorg`, containing public + internal CA certs. Apps mount it for
TLS verification.

### Recipe 9 — Monitoring (Prometheus + Alertmanager)

```yaml
# PrometheusRule
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata: { name: cert-expiry, namespace: monitoring, labels: { release: kps } }
spec:
  groups:
    - name: certificates
      rules:
        - alert: CertificateExpiringSoon
          expr: |
            certmanager_certificate_expiration_timestamp_seconds - time() < 7 * 24 * 60 * 60
          for: 1h
          labels: { severity: warning }
          annotations:
            summary: "Cert {{ $labels.name }} in {{ $labels.namespace }} expires in <7d"
            runbook_url: "https://github.com/myorg/runbooks/cert-expiry.md"
```

### Recipe 10 — Cert-manager + Istio integration

Istio uses cert-manager for the mesh CA:

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata: { name: istio-ca, namespace: istio-system }
spec:
  isCA: true
  duration: 2160h        # 90 days
  renewBefore: 720h
  secretName: cacerts    # Istio looks for this name
  commonName: istio-ca
  issuerRef: { name: step-ca-internal, kind: ClusterIssuer }
```

Same pattern for Linkerd: it expects `linkerd-trust-anchor`.

### Recipe 11 — Self-signed for local/dev

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata: { name: selfsigned }
spec:
  selfSigned: {}
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata: { name: dev-cert, namespace: dev }
spec:
  secretName: dev-cert
  duration: 24h
  issuerRef: { name: selfsigned, kind: ClusterIssuer }
  commonName: dev.local
  dnsNames: [dev.local]
```

Useful for `tilt`/`skaffold` local dev environments.

### Recipe 12 — AWS Private CA (PCA)

```yaml
# Install AWS PCA Issuer
helm repo add awspca https://cert-manager.github.io/aws-privateca-issuer
helm upgrade --install aws-pca-issuer awspca/aws-privateca-issuer -n aws-pca-issuer --create-namespace
```

```yaml
apiVersion: awspca.cert-manager.io/v1beta1
kind: AWSPCAClusterIssuer
metadata: { name: aws-pca-internal }
spec:
  arn: arn:aws:acm-pca:us-east-1:123456789012:certificate-authority/abc
  region: us-east-1
```

Use for compliance-mandated internal PKI on AWS.

## Examples

### Example 1 — Add TLS to all prod services in <1h

**Goal:** Every service gets HTTPS via Let's Encrypt; no manual cert ops.

1. `helm install cert-manager jetstack/cert-manager --set installCRDs=true`.
2. Apply `ClusterIssuer/letsencrypt-prod` (Recipe 1).
3. For each service Ingress, add `cert-manager.io/cluster-issuer:
   letsencrypt-prod` annotation + `tls:` block (Recipe 2).
4. cert-manager solves HTTP-01 for each; certs issue within ~30s each.
5. Verify: `curl -v https://service.myorg.com 2>&1 | grep -i 'verify ok'`.

**Result:** All services HTTPS; auto-renewal forever.

### Example 2 — Wildcard cert for `*.dev.myorg.com` via Cloudflare DNS-01

**Goal:** One cert covers all `*.dev.myorg.com` preview environments.

1. Create Cloudflare API token: Zone:DNS:Edit on `myorg.com`.
2. Store as Secret (Recipe 3).
3. Apply `ClusterIssuer/letsencrypt-dns-cf` (Recipe 3).
4. Apply `Certificate` requesting `*.dev.myorg.com`.
5. Cert issues in ~60s (DNS propagation).
6. Use Secret `wildcard-dev-tls` in all dev Ingresses.

**Result:** One cert for all PR preview URLs.

## Edge cases / gotchas

- **Let's Encrypt rate limits**: 50 certs/week per registered domain; 5
  duplicate cert orders/week. Use staging issuer for testing.
- **HTTP-01 won't work behind cert-manager**: requires public reachability
  on port 80. Use DNS-01 for internal-only services.
- **DNS-01 propagation delay**: typically 30-60s; cert-manager polls. If
  cert is stuck "pending", check the `Challenge` resource for the TXT
  record cert-manager wrote.
- **`installCRDs=true`** must be on first install; bypasses Helm CRD
  ownership issues. Use `crds.enabled=true` in newer chart versions.
- **Webhook timeouts** on creation of Certificate: `cert-manager-webhook`
  must be healthy. `kubectl logs -n cert-manager -l app=webhook`.
- **Cert renewal silently fails**: monitor via Prometheus alerts (Recipe 9).
  Don't trust "it just works".
- **`renewBefore` default = 2/3 of duration**. Custom value can clash with
  cert lifetime; set explicitly.
- **Wildcard certs and SANs**: a cert for `*.myorg.com` does NOT cover
  `myorg.com` itself; need both `dnsNames`.
- **Old `kubernetes.io/tls-acme: "true"` annotation** is legacy and ignored
  by modern cert-manager — always use `cert-manager.io/cluster-issuer`.
- **step-ca client-cert auth**: clients need `step ca certificate` calls;
  for K8s pods, use step-ca's K8s integration with cert-manager.
- **Multi-cluster trust**: trust-manager Bundle is cluster-scoped; for
  multi-cluster, sync via a shared Vault or ESO ClusterExternalSecret.

## Sources

- https://cert-manager.io/docs/ — cert-manager docs
- https://cert-manager.io/docs/configuration/acme/ — ACME configuration
- https://cert-manager.io/docs/configuration/acme/dns01/ — DNS-01 providers
- https://cert-manager.io/docs/trust/trust-manager/ — trust-manager
- https://letsencrypt.org/docs/rate-limits/ — Let's Encrypt rate limits
- https://smallstep.com/docs/step-ca/ — step-ca
- https://github.com/cert-manager/cmctl — cmctl CLI
- https://aws.amazon.com/private-ca/ — AWS PCA
- https://docs.cilium.io/en/stable/network/servicemesh/ingress/#tls-passthrough — Cilium + cert-manager
- https://blog.jetstack.io/ — cert-manager blog
