<!--
Source: https://docs.github.com/en/actions · https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services
Authored: June 2026 for the devops-engineer agent bundle.
-->

# GitHub Actions CI/CD + OIDC

Author and operate GitHub Actions workflows the 2026 way: **OIDC trust to
AWS/GCP/Azure** (no long-lived cloud creds in secrets), reusable workflows
(`workflow_call`), matrix strategies, composite actions, `permissions:`
blocks scoped per-job, immutable action pinning by full commit SHA,
`actionlint` static analysis, and `act` for local dry-run.

## When to use

- New repo — wire up CI from scratch.
- Existing CI has long-lived `AWS_ACCESS_KEY_ID` in secrets → migrate to OIDC.
- "Why is this workflow failing?" — diagnose via `gh run view --log-failed`.
- DRY refactor: 8 repos with the same release workflow → reusable workflow.
- Tighten security: `permissions: read-all` default + per-job scopes.

Skip when: repo lives on GitLab (different CI), or the workload is so tiny
that a Makefile + cron suffices.

## Setup

```bash
# GitHub CLI
brew install gh
gh auth login --hostname github.com --web

# Linters + local runners
brew install actionlint                        # static analysis
brew install act                                # local runner (Docker-based)
brew install dprint                             # YAML formatter

# Optional: nektos/act in lieu of GH-hosted runners for local PR testing
docker pull catthehacker/ubuntu:act-24.04
```

OIDC requires no per-repo secret — the GitHub-issued JWT is the auth. You
configure trust on the cloud side once.

## Common recipes

### Recipe 1 — Canonical OIDC-to-AWS deploy

```yaml
# .github/workflows/deploy.yml
name: deploy
on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment: { type: choice, options: [staging, prod] }

permissions: { id-token: write, contents: read }   # default-deny; scope up per job

concurrency:
  group: deploy-${{ github.ref }}-${{ inputs.environment }}
  cancel-in-progress: false                         # never cancel deploys

jobs:
  deploy:
    runs-on: ubuntu-24.04
    environment: ${{ inputs.environment || 'staging' }}
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683    # v5.0.0 — SHA-pinned
      - uses: aws-actions/configure-aws-credentials@e3dd6a429d7300a6a4c196c26e071d42e0343502    # v4.0.2
        with:
          role-to-assume: arn:aws:iam::123456789012:role/gh-deploy-${{ inputs.environment }}
          aws-region: us-east-1
      - run: |
          aws eks update-kubeconfig --name ${{ inputs.environment }}
          kubectl set image deployment/api api=ghcr.io/${{ github.repository }}:${{ github.sha }}
          kubectl rollout status deployment/api --timeout=5m
```

### Recipe 2 — AWS IAM role trust policy for GitHub OIDC

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com" },
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": {
        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
      },
      "StringLike": {
        "token.actions.githubusercontent.com:sub": "repo:myorg/myrepo:ref:refs/heads/main"
      }
    }
  }]
}
```

`StringLike` lets you match patterns: `repo:myorg/myrepo:environment:prod`,
`repo:myorg/myrepo:pull_request`, etc. Lock down by branch + environment.

### Recipe 3 — Reusable workflow

```yaml
# .github/workflows/build-image.yml  (the reusable one)
on:
  workflow_call:
    inputs:
      registry:  { type: string, required: true }
      image:     { type: string, required: true }
    outputs:
      digest:    { value: ${{ jobs.build.outputs.digest }} }

permissions: { id-token: write, contents: read, packages: write }

jobs:
  build:
    runs-on: ubuntu-24.04
    outputs: { digest: ${{ steps.build.outputs.digest }} }
    steps:
      - uses: actions/checkout@v5
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with: { registry: ${{ inputs.registry }}, username: ${{ github.actor }}, password: ${{ secrets.GITHUB_TOKEN }} }
      - id: build
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: ${{ inputs.registry }}/${{ inputs.image }}:${{ github.sha }}
          provenance: mode=max
          sbom: true
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

```yaml
# .github/workflows/release.yml  (caller)
jobs:
  build:
    uses: ./.github/workflows/build-image.yml
    with: { registry: ghcr.io, image: ${{ github.repository }} }
  deploy:
    needs: build
    runs-on: ubuntu-24.04
    steps:
      - run: echo "deploying ${{ needs.build.outputs.digest }}"
```

### Recipe 4 — Matrix builds

```yaml
jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-24.04, macos-14, windows-latest]
        python: ["3.11", "3.12", "3.13"]
        exclude:
          - { os: windows-latest, python: "3.13" }
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-python@v5
        with: { python-version: ${{ matrix.python }}, cache: pip }
      - run: pip install -e . && pytest
```

### Recipe 5 — Composite action

```yaml
# .github/actions/setup-uv/action.yml
name: setup-uv
description: Install uv and sync deps
inputs:
  python-version: { required: true }
runs:
  using: composite
  steps:
    - uses: actions/setup-python@v5
      with: { python-version: ${{ inputs.python-version }} }
    - shell: bash
      run: |
        curl -LsSf https://astral.sh/uv/install.sh | sh
        uv sync --frozen
```

```yaml
# caller
- uses: ./.github/actions/setup-uv
  with: { python-version: "3.12" }
```

### Recipe 6 — Cache mounts (npm + uv + Gradle)

```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.cache/uv
      ~/.npm
      ~/.gradle/caches
    key: ${{ runner.os }}-${{ hashFiles('**/uv.lock', '**/package-lock.json', '**/build.gradle.kts') }}
    restore-keys: ${{ runner.os }}-
```

`setup-node`, `setup-python`, `setup-java` ship built-in cache flags — prefer those over manual.

### Recipe 7 — Build → Scan → Sign → Deploy (canonical pipeline)

```yaml
permissions: { id-token: write, contents: read, packages: write, attestations: write }

jobs:
  build:
    runs-on: ubuntu-24.04
    outputs:
      digest: ${{ steps.push.outputs.digest }}
    steps:
      - uses: actions/checkout@v5
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with: { registry: ghcr.io, username: ${{ github.actor }}, password: ${{ secrets.GITHUB_TOKEN }} }
      - id: push
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
          provenance: mode=max
          sbom: true
      - uses: aquasecurity/trivy-action@master
        with:
          image-ref: ghcr.io/${{ github.repository }}@${{ steps.push.outputs.digest }}
          severity: HIGH,CRITICAL
          exit-code: 1
          ignore-unfixed: true
      - uses: sigstore/cosign-installer@v3
      - run: cosign sign --yes ghcr.io/${{ github.repository }}@${{ steps.push.outputs.digest }}
      - uses: actions/attest-build-provenance@v2
        with: { subject-name: ghcr.io/${{ github.repository }}, subject-digest: ${{ steps.push.outputs.digest }}, push-to-registry: true }
```

### Recipe 8 — Environment protection rules + manual approval

```yaml
jobs:
  deploy-prod:
    environment:
      name: prod
      url: https://api.myorg.com
    runs-on: ubuntu-24.04
    needs: [build, test]
    steps:
      - run: ./deploy.sh
```

Configure the `prod` environment in repo Settings → Environments:
- Required reviewers: @platform-lead
- Wait timer: 0 min
- Deployment branches: `main` only
- Environment secrets (scoped to this env only)

### Recipe 9 — Concurrency control

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}
```

Cancel old PR runs on push; never cancel deploys to prod.

### Recipe 10 — `gh` CLI ops

```bash
gh workflow list
gh workflow run deploy.yml -f environment=prod -r main
gh run list --workflow=deploy.yml --limit 5
gh run watch                           # live log of latest run
gh run view 12345 --log-failed        # just failed steps
gh run download 12345 -n test-results # artifacts
gh run rerun 12345 --failed           # retry failed jobs only
gh pr checks --watch                   # follow CI on current PR
```

### Recipe 11 — `actionlint` in pre-commit

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/rhysd/actionlint
    rev: v1.7.7
    hooks: [{ id: actionlint }]
```

Catches: shell injection (`${{ github.event.issue.title }}`), invalid
runner labels, type mismatches, deprecated `set-output`.

### Recipe 12 — Local dry-run with `act`

```bash
act -W .github/workflows/test.yml -j test --container-architecture linux/amd64
act push -e events/push.json           # simulate push event
act pull_request                        # default PR event
act -l                                  # list jobs
```

`act` uses Docker — runner image is `catthehacker/ubuntu:act-24.04`
(closest to `ubuntu-24.04`). Some actions need `-P ubuntu-24.04=...`.

### Recipe 13 — Self-hosted runner (Actions Runner Controller)

```yaml
# arc-runner.yaml
apiVersion: actions.github.com/v1alpha1
kind: AutoscalingRunnerSet
metadata: { name: myorg-runners, namespace: arc-systems }
spec:
  githubConfigUrl: https://github.com/myorg
  githubConfigSecret: github-app-secret
  minRunners: 1
  maxRunners: 20
  template:
    spec:
      containers:
        - name: runner
          image: ghcr.io/actions/actions-runner:latest
          resources: { requests: { cpu: 1, memory: 2Gi } }
```

Uses ARC (Actions Runner Controller, Kubernetes-based).

### Recipe 14 — Pin actions by SHA (OpenSSF + Dependabot)

```yaml
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683    # v5.0.0
```

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule: { interval: "weekly" }
```

Dependabot auto-PRs SHA bumps; `actionlint` confirms each is a valid action ref.

## Examples

### Example 1 — Migrate from `AWS_ACCESS_KEY_ID` secret to OIDC

**Goal:** Remove long-lived AWS creds from `myorg/myrepo`.

1. AWS console → IAM → create OIDC provider for `token.actions.githubusercontent.com`.
2. Create role `gh-deploy-prod` with trust policy (Recipe 2), scoped to `repo:myorg/myrepo:environment:prod`.
3. Attach inline policy with least-privilege actions (`eks:*`, `s3:Get*`, etc.).
4. In workflow, replace `aws-access-key-id` / `aws-secret-access-key` inputs with `role-to-assume`.
5. Add `permissions: { id-token: write }` at job level.
6. Delete `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` from repo secrets.
7. `gh workflow run deploy.yml` → confirm green.

**Result:** No long-lived AWS creds in GH; STS issues 15-min tokens per run.

### Example 2 — Refactor 8 repo workflows to one reusable

**Goal:** All services use the same build-scan-sign-deploy flow.

1. Move workflow body to `myorg/.github/.github/workflows/release.yml` (org-level).
2. Add `on: workflow_call` + parameterize inputs (image name, deploy target).
3. In each service repo: `uses: myorg/.github/.github/workflows/release.yml@v1`.
4. Tag the workflow repo `v1`; bump on changes.

**Result:** 8 workflows × ~120 lines collapsed to 8 × ~10-line callers.

## Edge cases / gotchas

- **`${{ github.event.pull_request.head.ref }}`** in `pull_request` events
  comes from the PR's fork — never `checkout` it without `pull_request_target`
  + careful permissions, or you get RCE via untrusted code. See:
  https://securitylab.github.com/research/github-actions-preventing-pwn-requests/
- **Default `GITHUB_TOKEN` permissions** were tightened in 2024; many old
  workflows fail with `Resource not accessible by integration`. Set
  `permissions:` at workflow or job level explicitly.
- **`permissions: write-all`** is the implicit default for some old repos;
  set `default-permissions: read` org-wide in Settings.
- **`gh run watch`** times out at 2 hours.
- **GitHub-hosted runners get a fresh VM each job** — no state between
  jobs unless cached or uploaded as artifact.
- **Matrix `include` adds; `exclude` removes** — both can fight; verify with
  `gh workflow view --yaml`.
- **`${{ secrets.* }}` is empty in PRs from forks** by default — security
  feature; can't share secrets with untrusted code.
- **OIDC token audience defaults to `sts.amazonaws.com`** for AWS; for GCP
  set `audience: //iam.googleapis.com/projects/.../workloadIdentityPools/...`.
- **Composite actions can't have `if:` on individual steps via inputs** —
  use shell conditionals inside steps.
- **`act` doesn't support reusable workflows perfectly** as of v0.2.65 —
  test reusable callers on real GH runners.
- **Workflow file caching:** GitHub caches per `<key>` — if you have non-
  deterministic data in the key, you never get a hit. Use `hashFiles(...)`.
- **`actions/cache` 10GB repo limit; LRU eviction** — heavy caches evict
  the small ones.

## Sources

- https://docs.github.com/en/actions — Actions docs root
- https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services — OIDC for AWS
- https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-google-cloud-platform — OIDC for GCP
- https://docs.github.com/en/actions/sharing-automations/reusing-workflows — reusable workflows
- https://github.com/rhysd/actionlint — actionlint
- https://github.com/nektos/act — act (local runner)
- https://github.com/actions/actions-runner-controller — ARC (self-hosted on K8s)
- https://securitylab.github.com/research/github-actions-preventing-pwn-requests/ — security guide
- https://github.com/sigstore/cosign-installer — Cosign action
- https://github.com/actions/attest-build-provenance — SLSA provenance attestation
- https://github.blog/changelog/2024-04-09-github-actions-permissions-tightening/ — 2024 permissions change
