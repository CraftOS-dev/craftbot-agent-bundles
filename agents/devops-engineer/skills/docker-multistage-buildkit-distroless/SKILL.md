<!--
Source: https://docs.docker.com/build/buildkit/ · https://github.com/chainguard-images/images · https://github.com/GoogleContainerTools/distroless
Authored: June 2026 for the devops-engineer agent bundle.
-->

# Docker Multi-stage + BuildKit + Distroless

Build minimal, reproducible, signed container images using Docker BuildKit's
multi-stage syntax, cache mounts, and distroless or Chainguard base images.
The 2026 default for any production container: tiny attack surface, fast CI
builds via layer-cache and registry-cache, multi-arch (amd64/arm64) in one
shot, ready for Cosign signing.

## When to use

- Authoring a new `Dockerfile` for a service shipping to prod.
- Auditing an existing image — `docker history`, `dive`, size > 200 MB.
- CI pipeline build step ("we need multi-arch", "the build takes 8 min").
- "Why is our image flagged with 200 CVEs?" — answer is almost always
  the base image (switch to `cgr.dev/chainguard/*` or
  `gcr.io/distroless/*`).
- Locking down: non-root user, read-only rootfs, no shell, no package manager.

Skip when the workload is a one-off script (just use `python:3.12-slim`) or
the runtime constraint is a Lambda/CloudRun-managed base.

## Setup

```bash
# Docker Engine 23+ ships with BuildKit; enable buildx for multi-arch
docker buildx create --use --name multi --driver docker-container
docker buildx inspect --bootstrap

# Verify BuildKit is the default
DOCKER_BUILDKIT=1 docker build --help | grep -i buildkit

# Companion tools
brew install dive       # image-layer explorer
brew install trivy      # scan
brew install cosign     # sign
brew install syft       # SBOM
```

No auth required for local builds; pushing to a registry needs
`docker login <registry>` or `gh auth token | docker login ghcr.io -u $(gh
api user -q .login) --password-stdin`.

## Common recipes

### Recipe 1 — Canonical multi-stage Python service (distroless)

```dockerfile
# syntax=docker/dockerfile:1.7
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim AS builder
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip install --user --no-cache-dir -r requirements.txt
COPY . .

FROM gcr.io/distroless/python3-debian12:nonroot AS runtime
WORKDIR /app
COPY --from=builder /root/.local /home/nonroot/.local
COPY --from=builder /app /app
ENV PATH="/home/nonroot/.local/bin:$PATH"
EXPOSE 8080
USER nonroot
ENTRYPOINT ["python", "-m", "myapp"]
```

`--mount=type=cache` keeps the pip cache between builds; the runtime stage
has no shell, no apt, no pip — only Python and your code.

### Recipe 2 — Go binary on Chainguard static (zero-CVE base)

```dockerfile
# syntax=docker/dockerfile:1.7
FROM golang:1.23-alpine AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod go mod download
COPY . .
RUN --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=linux GOARCH=${TARGETARCH} \
    go build -ldflags="-s -w" -trimpath -o /out/app ./cmd/app

FROM cgr.dev/chainguard/static:latest
COPY --from=builder /out/app /app
USER 65532:65532
ENTRYPOINT ["/app"]
```

Chainguard `static` image is ~2 MB with zero CVEs. The Go binary is the
entire userspace.

### Recipe 3 — Node.js with pnpm + corepack

```dockerfile
# syntax=docker/dockerfile:1.7
FROM node:20-alpine AS deps
WORKDIR /app
RUN corepack enable
COPY package.json pnpm-lock.yaml ./
RUN --mount=type=cache,id=pnpm,target=/pnpm/store \
    pnpm config set store-dir /pnpm/store && pnpm install --frozen-lockfile

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN corepack enable && pnpm build

FROM gcr.io/distroless/nodejs20-debian12:nonroot
WORKDIR /app
COPY --from=builder /app/dist /app/dist
COPY --from=builder /app/node_modules /app/node_modules
COPY --from=builder /app/package.json /app/package.json
EXPOSE 3000
USER nonroot
CMD ["dist/server.js"]
```

### Recipe 4 — Multi-arch build + push

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --cache-from type=registry,ref=ghcr.io/myorg/api:cache \
  --cache-to type=registry,ref=ghcr.io/myorg/api:cache,mode=max \
  --tag ghcr.io/myorg/api:1.27.3 \
  --tag ghcr.io/myorg/api:$(git rev-parse --short HEAD) \
  --provenance=mode=max \
  --sbom=true \
  --push \
  .
```

`--provenance=mode=max` emits in-toto attestation; `--sbom=true` emits an
SPDX SBOM into the registry alongside the image.

### Recipe 5 — Secrets at build time (no leak in layers)

```dockerfile
# syntax=docker/dockerfile:1.7
RUN --mount=type=secret,id=github_token,env=GITHUB_TOKEN \
    pip install git+https://oauth2:${GITHUB_TOKEN}@github.com/myorg/private.git
```

```bash
docker buildx build --secret id=github_token,env=GITHUB_TOKEN -t api:dev .
```

Secret never lands in any image layer; it's only mounted for that RUN.

### Recipe 6 — Cache mounts for apt/yum/apk

```dockerfile
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
```

Cache survives across builds; image layer doesn't contain the cache.

### Recipe 7 — Pin base image by digest (reproducible)

```dockerfile
FROM gcr.io/distroless/python3-debian12@sha256:6ba7b810f0ec4c8...
```

`docker buildx imagetools inspect gcr.io/distroless/python3-debian12:nonroot`
shows the digest. Pinning by digest = builds are bit-for-bit reproducible.

### Recipe 8 — HEALTHCHECK + non-root user

```dockerfile
FROM cgr.dev/chainguard/python:latest-dev AS runtime
USER nonroot
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"]
```

Note: distroless has no shell, so HEALTHCHECK CMD must be exec form (no
`CMD curl ...`).

### Recipe 9 — Local dev convenience: docker buildx bake

```hcl
# docker-bake.hcl
group "default" { targets = ["api", "worker"] }
target "api" {
  context = "."
  dockerfile = "Dockerfile.api"
  platforms = ["linux/amd64", "linux/arm64"]
  tags = ["ghcr.io/myorg/api:dev"]
  cache-from = ["type=registry,ref=ghcr.io/myorg/api:cache"]
  cache-to = ["type=registry,ref=ghcr.io/myorg/api:cache,mode=max"]
}
target "worker" {
  context = "."
  dockerfile = "Dockerfile.worker"
  inherits = ["api"]
  tags = ["ghcr.io/myorg/worker:dev"]
}
```

```bash
docker buildx bake --push                # build all
docker buildx bake api --print           # show resolved plan
```

### Recipe 10 — Scan + sign in one shot (post-build)

```bash
IMAGE=ghcr.io/myorg/api@$(docker buildx imagetools inspect ghcr.io/myorg/api:1.27.3 --format '{{json .Manifest.Digest}}' | tr -d '"')

trivy image --severity HIGH,CRITICAL --exit-code 1 --ignore-unfixed $IMAGE
syft $IMAGE -o cyclonedx-json > sbom.json
cosign sign --yes $IMAGE
cosign attest --predicate sbom.json --type cyclonedx $IMAGE
```

Always sign by digest, never by mutable tag.

### Recipe 11 — Audit an existing image

```bash
dive ghcr.io/myorg/api:1.27.3                                # interactive size breakdown
docker history --no-trunc ghcr.io/myorg/api:1.27.3 | head    # layer-by-layer commands
docker buildx imagetools inspect ghcr.io/myorg/api:1.27.3    # OCI manifest + platforms
```

## Examples

### Example 1 — Migrate a 600 MB image to <50 MB

**Goal:** Slim down `myorg/api:latest` (built `FROM python:3.12`).

1. Read `Dockerfile`; confirm it uses `python:3.12` (~1 GB base) + `pip install` in final stage.
2. Rewrite using Recipe 1 (multi-stage + distroless).
3. Build: `docker buildx build -t api:slim .`
4. Verify size: `docker images api:slim` should show <80 MB compressed.
5. Smoke test: `docker run --rm -p 8080:8080 api:slim` and `curl localhost:8080/health`.
6. Scan: `trivy image api:slim` — expect 90%+ CVE reduction vs the full image.

**Result:** Image drops from 600 MB to ~45 MB; CVE count drops by ~95%.

### Example 2 — Add multi-arch + signing to existing CI

**Goal:** Build images for amd64 + arm64 and sign them keylessly from GitHub Actions.

1. In `.github/workflows/build.yml`, add `permissions: id-token: write`.
2. Use `docker/setup-buildx-action@v3` and `docker/build-push-action@v6` with `platforms: linux/amd64,linux/arm64`.
3. Add `provenance: mode=max` and `sbom: true`.
4. Add `sigstore/cosign-installer@v3` + `cosign sign --yes ${{ steps.build.outputs.imageid }}`.

**Result:** Both architectures pushed in one digest; Rekor entry visible at
`https://search.sigstore.dev/?logIndex=...`.

## Edge cases / gotchas

- **`docker buildx` requires QEMU for cross-arch.** On Linux runners, install
  `qemu-user-static`; GitHub Actions `setup-qemu-action@v3` handles it.
- **Cache to GHA (`type=gha,mode=max`)** is faster than registry cache but
  limited to ~10 GB per repo. Use registry cache for shared multi-repo caches.
- **`--mount=type=cache` is not pushed to the registry.** First build on a
  cold cache will be slow; budget for it on cold CI.
- **Distroless has no shell.** Cannot `docker exec -it api sh`. Use a
  `*-debug` variant locally if you need to poke around:
  `gcr.io/distroless/python3-debian12:debug` includes busybox.
- **`USER nonroot` + read-only rootfs** breaks apps that write to `/tmp`.
  Mount an `emptyDir` at `/tmp` in the K8s PodSpec.
- **`FROM scratch` for Go binaries** is even smaller than distroless
  `static`, but lacks `/etc/ssl/certs`. Use `cgr.dev/chainguard/static`
  (it ships CA bundle + tzdata) unless your binary statically links.
- **Multi-arch base images:** `cgr.dev/chainguard/static` and
  `gcr.io/distroless/*` ship `linux/amd64` and `linux/arm64`. Niche bases
  may not — `docker buildx imagetools inspect <base>` to verify.
- **Layer order matters for cache.** Copy `requirements.txt` / `package.json`
  BEFORE source so dep layers cache when source changes.
- **`docker buildx prune`** can free 10s of GB if cache grows unbounded on
  builders. Add a weekly cron.
- **`hadolint` lints Dockerfiles** — `docker run --rm -i hadolint/hadolint <
  Dockerfile`.

## Sources

- https://docs.docker.com/build/buildkit/ — BuildKit reference
- https://docs.docker.com/reference/dockerfile/ — Dockerfile syntax
- https://github.com/chainguard-images/images — Chainguard zero-CVE images
- https://github.com/GoogleContainerTools/distroless — Google distroless
- https://docs.docker.com/build/cache/ — cache backends + mount types
- https://docs.docker.com/build/attestations/ — provenance + SBOM
- https://github.com/wagoodman/dive — image layer inspector
- https://hadolint.github.io/hadolint/ — Dockerfile linter
- https://snyk.io/blog/choosing-the-best-node-js-docker-image/ — base-image comparison (2025)
