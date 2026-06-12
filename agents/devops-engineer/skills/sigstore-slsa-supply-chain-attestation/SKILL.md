<!--
Source: https://docs.sigstore.dev/ · https://slsa.dev/spec/v1.0/levels · https://in-toto.io/
Authored: June 2026 for the devops-engineer agent bundle.
-->

# Sigstore (Cosign + Fulcio + Rekor) + SLSA + in-toto

Supply-chain attestation for container images and artifacts. **Sigstore**
ecosystem: **Cosign** (sign + verify), **Fulcio** (cert authority from OIDC
identity), **Rekor** (transparency log). **Syft** generates SBOM (SPDX or
CycloneDX). **SLSA framework** defines build provenance levels 1-4. **in-toto**
attestations are the format. Pair with **Kyverno** admission for verification
on deploy.

## When to use

- Production image signing (mandatory for compliance: NIST SSDF, SLSA L3+).
- "How do I know this image came from our CI?" — verify signature + cert
  identity matches GH org.
- SBOM-as-attestation for SOC 2 / FedRAMP.
- Image policy enforcement in K8s (Kyverno verifyImages).

Skip when: hobby project; you can't enforce in admission (signing without
verification is theater).

## Setup

```bash
# Cosign (Sigstore CLI)
brew install cosign
cosign version

# Syft (SBOM)
brew install syft

# Crane (image inspection)
brew install crane

# SLSA generators (used inside GH Actions; no local install)
# https://github.com/slsa-framework/slsa-github-generator

# in-toto attestation tooling
brew install in-toto-attest          # OR: pip install in-toto-attestation
```

Sigstore public infrastructure (free) at https://fulcio.sigstore.dev +
https://rekor.sigstore.dev — no API keys for the public service. For private,
deploy your own Sigstore stack.

## Common recipes

### Recipe 1 — Keyless sign in GitHub Actions

```yaml
permissions: { id-token: write, contents: read, packages: write }

steps:
  - uses: docker/build-push-action@v6
    id: build
    with:
      push: true
      tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
  - uses: sigstore/cosign-installer@v3
  - name: Cosign sign (keyless)
    run: |
      cosign sign --yes \
        ghcr.io/${{ github.repository }}@${{ steps.build.outputs.digest }}
```

Workflow's OIDC token is the identity; Fulcio issues a short-lived cert
bound to `repo:myorg/myrepo:ref:refs/heads/main`. Signature + cert end up in
Rekor.

### Recipe 2 — Verify image (admission-grade)

```bash
cosign verify \
  --certificate-identity-regexp='^https://github\.com/myorg/[^/]+/\.github/workflows/' \
  --certificate-oidc-issuer=https://token.actions.githubusercontent.com \
  ghcr.io/myorg/api@sha256:6ba7b810...
```

Returns the verified payload if signature + cert + Rekor inclusion proof
all check out.

### Recipe 3 — Sign with a long-term key (legacy, less recommended)

```bash
cosign generate-key-pair                # creates cosign.key + cosign.pub
cosign sign --key cosign.key ghcr.io/myorg/api@sha256:...
cosign verify --key cosign.pub ghcr.io/myorg/api@sha256:...
```

Prefer keyless except when air-gapped or required by policy.

### Recipe 4 — Attest SBOM (in-toto + CycloneDX)

```bash
syft ghcr.io/myorg/api:1.27.3 -o cyclonedx-json > sbom.cdx.json

cosign attest --yes \
  --predicate sbom.cdx.json \
  --type cyclonedx \
  ghcr.io/myorg/api@sha256:6ba7b810...

cosign verify-attestation \
  --certificate-identity-regexp='^https://github\.com/myorg/' \
  --certificate-oidc-issuer=https://token.actions.githubusercontent.com \
  --type cyclonedx \
  ghcr.io/myorg/api@sha256:6ba7b810... | jq '.payload | @base64d | fromjson'
```

`predicate` is any JSON; `type` is the schema URI.

### Recipe 5 — SLSA Build Level 3 provenance (GH Actions Generator)

```yaml
jobs:
  build:
    outputs:
      image: ghcr.io/${{ github.repository }}
      digest: ${{ steps.build.outputs.digest }}
    runs-on: ubuntu-24.04
    permissions: { id-token: write, contents: read, packages: write }
    steps: # ... build + push ...

  provenance:
    needs: build
    permissions: { actions: read, id-token: write, packages: write }
    uses: slsa-framework/slsa-github-generator/.github/workflows/generator_container_slsa3.yml@v2.0.0
    with:
      image: ${{ needs.build.outputs.image }}
      digest: ${{ needs.build.outputs.digest }}
      registry-username: ${{ github.actor }}
    secrets:
      registry-password: ${{ secrets.GITHUB_TOKEN }}
```

Result: a SLSA L3 provenance attestation attached to the image.

### Recipe 6 — Verify SLSA provenance

```bash
slsa-verifier verify-image \
  --source-uri github.com/myorg/myrepo \
  --source-tag v1.27.3 \
  ghcr.io/myorg/api@sha256:6ba7b810...
```

Confirms: the image was built from `github.com/myorg/myrepo` at tag
`v1.27.3` by GH Actions, signed via Sigstore.

### Recipe 7 — Kyverno admission policy (verify on deploy)

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata: { name: verify-image-signatures }
spec:
  validationFailureAction: Enforce
  webhookTimeoutSeconds: 30
  rules:
    - name: verify-image
      match: { any: [{ resources: { kinds: [Pod] } }] }
      verifyImages:
        - imageReferences:
            - "ghcr.io/myorg/*"
          mutateDigest: true              # auto-rewrite tag to digest
          attestors:
            - entries:
                - keyless:
                    subject: "https://github.com/myorg/*/.github/workflows/*"
                    issuer: "https://token.actions.githubusercontent.com"
                    rekor: { url: "https://rekor.sigstore.dev" }
```

Pods using `ghcr.io/myorg/*` must have a Cosign signature from a
`myorg/*` GH Actions workflow. Otherwise creation is rejected.

### Recipe 8 — Attest SBOM AND provenance in one workflow

```yaml
- uses: actions/attest-build-provenance@v2
  with:
    subject-name: ghcr.io/${{ github.repository }}
    subject-digest: ${{ steps.build.outputs.digest }}
    push-to-registry: true

- name: Generate SBOM
  uses: anchore/sbom-action@v0
  with:
    image: ghcr.io/${{ github.repository }}@${{ steps.build.outputs.digest }}
    artifact-name: sbom.spdx.json
    format: spdx-json

- name: Attest SBOM
  uses: actions/attest-sbom@v2
  with:
    subject-name: ghcr.io/${{ github.repository }}
    subject-digest: ${{ steps.build.outputs.digest }}
    sbom-path: sbom.spdx.json
    push-to-registry: true
```

GitHub-native attestation actions are simpler than Cosign directly for
attestation workflows.

### Recipe 9 — Verify with `gh attestation`

```bash
gh attestation verify oci://ghcr.io/myorg/api@sha256:6ba7b810... \
  --owner myorg
# Verifies via GitHub's transparency log (which signs to Sigstore Rekor)
```

### Recipe 10 — Local sign-verify loop (no CI)

```bash
# Local dev sign (OAuth opens browser)
cosign sign --yes ghcr.io/myorg/api@sha256:...

# Inspect Rekor entry
curl https://rekor.sigstore.dev/api/v1/log/entries?logIndex=<INDEX>

# Verify
cosign verify \
  --certificate-identity=foong.lns2u@gmail.com \
  --certificate-oidc-issuer=https://accounts.google.com \
  ghcr.io/myorg/api@sha256:...
```

### Recipe 11 — Rekor search

```bash
# Find all Rekor entries for an image digest
rekor-cli search --rekor_server https://rekor.sigstore.dev \
  --sha sha256:6ba7b810f0ec4c8a0a...

rekor-cli get --uuid <uuid> --rekor_server https://rekor.sigstore.dev | jq .
```

### Recipe 12 — Private Sigstore stack (air-gapped)

```bash
# Use sigstore-private (chart bundle)
helm repo add sigstore https://sigstore.github.io/helm-charts
helm upgrade --install sigstore sigstore/scaffold -n sigstore --create-namespace

# Configure Cosign to use private
export COSIGN_FULCIO_URL=https://fulcio.internal
export COSIGN_REKOR_URL=https://rekor.internal
export COSIGN_OIDC_ISSUER=https://idp.internal/oidc
cosign sign --yes ghcr.io/myorg/api@sha256:...
```

### Recipe 13 — Signing non-container artifacts

```bash
# Sign a generic blob
cosign sign-blob --yes file.tar.gz > file.tar.gz.sig
cosign verify-blob --signature file.tar.gz.sig \
  --certificate-identity-regexp='^https://github\.com/myorg/' \
  --certificate-oidc-issuer=https://token.actions.githubusercontent.com \
  file.tar.gz

# Helm chart (signing via Cosign + OCI)
helm package my-chart
cosign sign --yes oci://ghcr.io/myorg/charts/my-chart:0.1.0
```

## Examples

### Example 1 — Full pipeline: build → sign → attest → verify

**Goal:** Every prod deploy carries SBOM + SLSA L3 provenance + signature.

1. GH Actions workflow (Recipes 1, 5, 8):
   - Build via BuildKit, push to GHCR.
   - Cosign sign (keyless).
   - SLSA Generator emits provenance attestation.
   - Syft generates SBOM; `attest-sbom` attaches to image.
2. Verify in CI: `cosign verify` + `slsa-verifier verify-image`.
3. K8s admission (Recipe 7): Kyverno blocks unsigned images.
4. Audit: Rekor log search yields all signatures by org.

**Result:** Cryptographic chain from source → image → cluster.

### Example 2 — Validate "this prod image came from main"

**Goal:** Prove that `ghcr.io/myorg/api@sha256:abc` was built from
`main` branch.

1. `cosign verify --certificate-github-workflow-sha=main ...` — fails if signed from a feature branch.
2. `slsa-verifier verify-image --source-branch=main ghcr.io/myorg/api@sha256:abc` — confirms.
3. Cross-check with `gh attestation verify oci://...`.

**Result:** Provenance verified end-to-end.

## Edge cases / gotchas

- **Signatures sign by digest, not tag.** `cosign sign image:tag` resolves
  the tag to a digest first. Always use `@sha256:...` in admission policies.
- **Rekor is APPEND-ONLY**: signatures can't be revoked. Re-sign with new
  cert and add the old one to a deny list.
- **Cert identity must match exactly** in admission. Wildcard with care:
  `https://github.com/myorg/*` allows any repo in your org; `https://github.com/myorg/specific-repo`
  is stricter.
- **OIDC issuer URL changes break verification.** GitHub's issuer is stable
  (`https://token.actions.githubusercontent.com`) but Google's varies.
- **`cosign sign` without `--yes`** prompts to confirm — fails in CI.
  Always use `--yes`.
- **Fulcio rate limits**: 60 signs/min per IP for public. Heavy CI loads
  need to batch or stagger.
- **In-toto predicate types matter**: SBOM with `--type cyclonedx` won't
  verify with `--type spdx`. Match types end-to-end.
- **SLSA Level 3 requires** ephemeral, isolated, parameterized build —
  GH Actions hosted runners meet this; self-hosted may not.
- **Kyverno `mutateDigest: true`** rewrites tags to digests during admission.
  This means redeploying the same tag pulls the same digest — immutable.
- **Long-term key vs keyless**: keyless = no key rotation; certs are 10-min;
  signature still valid because Rekor proves "this was signed by this
  identity at this time". Long-term keys need rotation infrastructure.

## Sources

- https://docs.sigstore.dev/ — Sigstore docs
- https://docs.sigstore.dev/cosign/overview/ — Cosign
- https://docs.sigstore.dev/fulcio/overview/ — Fulcio (CA)
- https://docs.sigstore.dev/rekor/overview/ — Rekor (transparency log)
- https://slsa.dev/spec/v1.0/levels — SLSA levels
- https://github.com/slsa-framework/slsa-github-generator — SLSA generators
- https://in-toto.io/ — in-toto attestations
- https://github.com/anchore/syft — Syft (SBOM)
- https://kyverno.io/docs/writing-policies/verify-images/ — Kyverno verify
- https://docs.github.com/en/actions/security-guides/using-artifact-attestations-to-establish-provenance-for-builds — GH attestations
- https://www.cisa.gov/sites/default/files/2023-04/secure-software-self-attestation_common-form_508.pdf — CISA SSDF attestation
