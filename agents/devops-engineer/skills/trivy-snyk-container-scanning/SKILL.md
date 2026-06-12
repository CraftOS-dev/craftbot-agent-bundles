<!--
Source: https://aquasecurity.github.io/trivy/ · https://docs.snyk.io/scan-using-snyk/snyk-container · https://github.com/anchore/grype
Authored: June 2026 for the devops-engineer agent bundle.
-->

# Trivy / Snyk / Grype — Container Scanning

Vulnerability + misconfig + secret scanning for container images, IaC, and
filesystems. **Trivy** (Aqua, fast, free, all-in-one — 2026 default),
**Snyk** (commercial; policy + license + IaC + dashboards), **Grype**
(Anchore — Trivy alternative). Pair with admission policies (Kyverno) to
block unsigned/vulnerable images at deploy time.

## When to use

- CI step: scan image before pushing to registry.
- "How many CVEs in our prod images right now?" — `trivy k8s cluster`.
- IaC misconfig scanning (Terraform, Helm, K8s manifests).
- Secrets accidentally in code (`AWS_SECRET_ACCESS_KEY=AKIA...`).
- SBOM-based scanning (faster, audit-friendly).

Skip when: image is from a vendor with own security guarantees (e.g.,
`cgr.dev/chainguard/static` is zero-CVE by construction); team has Wiz/Aqua
running already.

## Setup

```bash
# Trivy (Apache 2.0, free)
brew install trivy
# OR: docker pull aquasec/trivy:latest

# Snyk (commercial; free tier)
brew install snyk/tap/snyk
snyk auth                          # opens browser

# Grype (Apache 2.0)
brew install grype
brew install syft                  # SBOM generator (often paired with grype)

# Database update (do this in CI before scan)
trivy image --download-db-only
grype db update
```

API keys:
- Snyk: `SNYK_TOKEN` from https://app.snyk.io/account
- Trivy: no auth needed for vuln DB; private registry creds via
  `~/.docker/config.json` or env.

## Common recipes

### Recipe 1 — Trivy image scan (canonical CI step)

```bash
trivy image \
  --severity HIGH,CRITICAL \
  --exit-code 1 \
  --ignore-unfixed \
  --scanners vuln,misconfig,secret \
  --format sarif \
  --output trivy-results.sarif \
  ghcr.io/myorg/api:1.27.3
```

`--ignore-unfixed` skips CVEs with no fix available (signal-to-noise++).
`--scanners` enables vuln + misconfig + secret in one pass.

### Recipe 2 — GitHub Actions integration

```yaml
- name: Trivy scan
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ghcr.io/${{ github.repository }}:${{ github.sha }}
    severity: HIGH,CRITICAL
    exit-code: '1'
    ignore-unfixed: 'true'
    format: 'sarif'
    output: 'trivy-results.sarif'

- name: Upload SARIF
  uses: github/codeql-action/upload-sarif@v3
  with: { sarif_file: trivy-results.sarif }
```

Results render in repo Security tab → Code scanning.

### Recipe 3 — Trivy filesystem scan (source code)

```bash
# Scan project root for vulns + misconfig + secrets
trivy fs --scanners vuln,misconfig,secret .

# Just secrets
trivy fs --scanners secret --skip-dirs .git .

# Just dependency vulns
trivy fs --scanners vuln --severity HIGH,CRITICAL .
```

### Recipe 4 — Trivy K8s cluster scan

```bash
trivy k8s --report summary cluster
# Shows worst pods + CVE counts

trivy k8s --severity HIGH,CRITICAL --report all cluster
trivy k8s --namespace prod cluster      # scoped

# JSON output for further processing
trivy k8s --format json --output cluster-report.json cluster
```

### Recipe 5 — Trivy IaC scan

```bash
# Terraform / OpenTofu
trivy config --severity HIGH,CRITICAL terraform/

# K8s manifests
trivy config --severity HIGH,CRITICAL manifests/

# Dockerfile
trivy config Dockerfile

# Helm chart (rendered)
helm template my-app charts/my-app | trivy config --severity HIGH,CRITICAL -
```

### Recipe 6 — `.trivyignore` (accepted risk)

```bash
# .trivyignore
# Format: <CVE-ID> [<EXPIRES>] [<REASON>]
CVE-2023-12345 2026-12-31 # not exploitable in our config; fix in 1.28
CVE-2024-67890 # third-party lib; vendor refuses fix
```

```bash
trivy image --severity HIGH,CRITICAL ghcr.io/myorg/api:1.27.3 --ignorefile .trivyignore
```

Always include EXPIRES + REASON for audit trail.

### Recipe 7 — Snyk container test

```bash
snyk container test ghcr.io/myorg/api:1.27.3 \
  --file=Dockerfile \
  --severity-threshold=high \
  --fail-on=upgradable

snyk container monitor ghcr.io/myorg/api:1.27.3 \
  --file=Dockerfile \
  --project-name=api-prod
```

`monitor` uploads to Snyk dashboard for ongoing tracking.

### Recipe 8 — Snyk IaC + code

```bash
snyk iac test terraform/ --severity-threshold=high
snyk test --severity-threshold=high           # source deps (npm/pip/maven/etc.)
snyk code test --severity-threshold=high      # SAST
snyk monitor --all-projects                   # batch monitor everything in repo
```

### Recipe 9 — Grype scan (Trivy alternative)

```bash
grype ghcr.io/myorg/api:1.27.3 \
  --scope all-layers \
  --fail-on high \
  --only-fixed \
  --output sarif \
  --file grype-results.sarif

# Pair with Syft for SBOM-first scanning
syft ghcr.io/myorg/api:1.27.3 -o cyclonedx-json > sbom.json
grype sbom:sbom.json                          # scan SBOM, not image
```

### Recipe 10 — Scan SBOM (faster + reproducible)

```bash
# Generate SBOM once
syft ghcr.io/myorg/api:1.27.3 -o cyclonedx-json > sbom.cdx.json

# Scan SBOM (no need to re-pull image)
trivy sbom sbom.cdx.json --severity HIGH,CRITICAL
grype sbom:sbom.cdx.json --fail-on high

# Snyk
snyk test --sbom sbom.cdx.json
```

### Recipe 11 — Kyverno admission policy (block CVE-heavy images)

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata: { name: block-high-cve-images }
spec:
  validationFailureAction: Enforce
  rules:
    - name: scan-image
      match: { any: [{ resources: { kinds: [Pod] } }] }
      verifyImages:
        - imageReferences: ["ghcr.io/myorg/*"]
          mutateDigest: false
          attestations:
            - predicateType: https://aquasecurity.github.io/trivy/0.50.0/scanner
              attestors:
                - entries:
                    - keyless:
                        subject: "https://github.com/myorg/*/.github/workflows/*"
                        issuer: "https://token.actions.githubusercontent.com"
              conditions:
                - all:
                    - key: "{{ scanner.severity_summary.critical }}"
                      operator: Equals
                      value: 0
```

Requires Trivy attestation (Recipe 12) on each image.

### Recipe 12 — Trivy as attestation (signed scan result)

```bash
# Generate scan attestation
trivy image --format cyclonedx --output sbom.json ghcr.io/myorg/api:1.27.3
cosign attest --predicate sbom.json --type cyclonedx \
  ghcr.io/myorg/api@$(crane digest ghcr.io/myorg/api:1.27.3)

# Verify
cosign verify-attestation \
  --certificate-identity-regexp='^https://github\.com/myorg/' \
  --certificate-oidc-issuer=https://token.actions.githubusercontent.com \
  --type cyclonedx \
  ghcr.io/myorg/api@sha256:...
```

### Recipe 13 — Operator: Trivy Operator in K8s

```bash
helm repo add aqua https://aquasecurity.github.io/helm-charts
helm upgrade --install trivy-operator aqua/trivy-operator \
  -n trivy-system --create-namespace --version 0.22.x
```

Generates `VulnerabilityReport`, `ConfigAuditReport`, `ExposedSecretReport`
CRDs per workload. Integrate with Grafana via Trivy Prometheus exporter.

```bash
kubectl get vulnerabilityreports -A
kubectl get exposedsecretreports -A
```

### Recipe 14 — Compare tools

| Tool | Speed | OSS? | Coverage | Best for |
|---|---|---|---|---|
| Trivy | Fast | Apache 2.0 | Vulns + Misconfig + Secrets + IaC + K8s + SBOM | Default 2026; CI + cluster |
| Snyk | Med | Closed (CLI MIT) | Vulns + License + IaC + Code (SAST) | Org policy + dashboards |
| Grype | Fast | Apache 2.0 | Vulns + SBOM | Anchore stack; SBOM-first |
| Wiz | Slow | Closed (paid) | Full CSPM + CIEM + DSPM + container | Enterprise multi-cloud security |
| Aqua | Med | Closed (paid) | Container + runtime + cloud workload | Enterprise + runtime focus |

## Examples

### Example 1 — Add Trivy to existing GitHub Actions CI

**Goal:** Fail builds on new HIGH/CRITICAL CVEs.

1. After image push step, add Trivy action (Recipe 2).
2. Set `exit-code: '1'` to fail builds.
3. Set `ignore-unfixed: true` to avoid noise from unfixable CVEs.
4. Create `.trivyignore` with current accepted CVEs (Recipe 6).
5. Open Security tab → see SARIF findings.

**Result:** No new HIGH/CRITICAL CVE merges to main.

### Example 2 — Cluster-wide vulnerability inventory

**Goal:** Know which prod pods have CVEs right now.

1. Install Trivy Operator (Recipe 13).
2. Wait for it to scan all pods (~30 min for a 100-pod cluster).
3. `kubectl get vulnerabilityreport -A -o json | jq '... critical/high counts'`.
4. Dashboard: import Grafana dashboard 17813.
5. Per-image action plan: top 10 worst → file tickets to rebuild.

**Result:** Visible inventory; tracked over time.

## Edge cases / gotchas

- **Trivy DB is community-maintained** — sometimes lags Snyk's commercial
  feeds by 24-72h. Use both for defense in depth in regulated industries.
- **`--ignore-unfixed`** skips CVEs without a fix — pragmatic but hides
  truly unfixable critical risks. Re-scan monthly without this flag.
- **`--scanners secret`** finds high-entropy strings — false positives on
  test data. Tune via `--secret-config`.
- **Snyk free tier**: 200 container tests/mo. Enterprise needed for large
  fleets.
- **`trivy image` of a 5 GB image** = 5-10 min scan. Use SBOM-based
  scanning (Recipe 10) to cache work.
- **Private registry auth**: `docker login` first; Trivy reads
  `~/.docker/config.json`. For ECR: `aws ecr get-login-password | docker
  login`.
- **CVE noise**: Debian/Ubuntu base images carry hundreds of CVEs by
  default — switch to Chainguard/distroless to eliminate ~95%.
- **`--severity` flags** filter REPORT; scan still runs full. Use
  `--vuln-type` to skip OS-package scans.
- **Trivy in air-gapped envs**: pre-download DB via `trivy image
  --download-db-only`, ship to internal mirror, set `TRIVY_DB_REPOSITORY`.
- **Grype + Syft pipeline**: SBOM-first reproducibility. SBOM is the audit
  artifact; scan is dynamic.
- **CIS Benchmarks**: Trivy supports CIS K8s + Docker via
  `trivy --compliance docker-cis-1.6.0 image ...` or
  `trivy --compliance k8s-cis-1.23 cluster`.

## Sources

- https://aquasecurity.github.io/trivy/ — Trivy docs
- https://github.com/aquasecurity/trivy-action — Trivy GH Action
- https://github.com/aquasecurity/trivy-operator — Trivy K8s Operator
- https://docs.snyk.io/scan-using-snyk/snyk-container — Snyk container
- https://docs.snyk.io/scan-using-snyk/scan-infrastructure — Snyk IaC
- https://github.com/anchore/grype — Grype
- https://github.com/anchore/syft — Syft (SBOM)
- https://kyverno.io/docs/writing-policies/verify-images/ — Kyverno image verify
- https://www.cisecurity.org/benchmark/docker — Docker CIS
- https://chainguard.dev/news/why-distroless-images-matter — Chainguard CVE post (2025)
