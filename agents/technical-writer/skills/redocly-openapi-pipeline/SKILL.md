---
name: redocly-openapi-pipeline
description: Self-hosted API reference pipeline with Redocly CLI — lint, bundle, build static docs from OpenAPI 3.1. Pair with Scalar or ReDoc as the renderer. Use when the user wants free, self-hosted, version-controlled API docs without a SaaS dependency.
---

# Redocly OpenAPI Pipeline

Redocly CLI is the open-source SOTA for OpenAPI lint + bundle + build-docs. Combined with Scalar (modern API reference renderer) or ReDoc (Redocly's own renderer), it produces a static HTML reference that can ship anywhere — GitHub Pages, Cloudflare Pages, Netlify, S3.

## When to use this skill

- The user wants self-hosted API docs (no Mintlify SaaS dependency).
- The repo already has an OpenAPI spec or AsyncAPI spec.
- The user wants enforce style/lint rules on the spec in CI.
- The user wants to bundle a multi-file spec (`$ref` across files) into a single deployable artifact.

**Choose this skill over `mintlify-api-docs` when:** the user can't or won't use SaaS, or when the org already has a static-site CI pipeline.

## Setup

### Install

```bash
npm i -g @redocly/cli
npm i -g @scalar/cli       # optional, for Scalar rendering
redocly --version
```

The agent should probe `node --version` (Node 18+ required) before install.

### Initialize project config

```bash
redocly init
# answers:
#   spec entrypoint: ./openapi.yaml
#   linting preset:  recommended
```

This writes `redocly.yaml`:

```yaml
apis:
  main:
    root: ./openapi.yaml

extends:
  - recommended       # or recommended-strict / minimal

rules:
  no-empty-servers: error
  operation-operationId: error
  operation-summary: error
  no-ambiguous-paths: error
```

## Common recipes

### Recipe 1: Lint a spec

```bash
redocly lint openapi.yaml --extends=recommended
# JSON output for CI:
redocly lint openapi.yaml --format=json > lint.json
```

CI gate pattern:

```yaml
# .github/workflows/openapi-lint.yml
- run: npx @redocly/cli@latest lint openapi.yaml --extends=recommended
```

### Recipe 2: Bundle a multi-file spec

```bash
redocly bundle openapi.yaml --output dist/openapi.bundle.yaml
# JSON variant:
redocly bundle openapi.yaml --output dist/openapi.bundle.json --ext json
# Deref everything (no $ref left):
redocly bundle openapi.yaml --dereferenced --output dist/openapi.deref.yaml
```

Use a bundled spec as the upload target for SDK generators (see `openapi-sdk-generation`) and for Mintlify when the source is multi-file.

### Recipe 3: Build static reference docs with ReDoc

```bash
redocly build-docs openapi.yaml --output dist/api.html
# host: copy dist/api.html anywhere
```

Single-file output, no runtime dependency. Deploy with:

```yaml
# .github/workflows/api-docs-deploy.yml
- run: npx @redocly/cli@latest build-docs openapi.yaml --output public/api/index.html
- uses: peaceiris/actions-gh-pages@v4
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: public
```

### Recipe 4: Build with Scalar (alternative renderer)

```bash
# install
npm i -g @scalar/cli
# generate
scalar reference openapi.yaml --output dist/scalar.html
# or live-server preview
scalar reference openapi.yaml --watch
```

Scalar's rendering is faster and more modern (2026 leader for "feels native"); use it when the user wants a Stripe-style reference.

### Recipe 5: Split a giant spec

```bash
redocly split openapi.yaml --outDir spec/
```

Produces `spec/openapi.yaml` (root) + `spec/paths/*.yaml` + `spec/components/schemas/*.yaml`. Re-bundle for deploy with `redocly bundle`.

### Recipe 6: Decorators for tenant-specific docs

`redocly.yaml`:

```yaml
apis:
  public@v2:
    root: ./openapi.yaml
    decorators:
      remove-x-internal: on    # strip x-internal endpoints from the public bundle
  internal@v2:
    root: ./openapi.yaml
```

Then `redocly bundle public@v2 -o dist/public.yaml`.

## OpenAPI 3.1 best practices the agent enforces

- Use `openapi: 3.1.0` (JSON Schema 2020-12 alignment).
- Every operation needs `operationId`, `summary`, `description`, and at least one example response.
- Use `$ref` for reusable schemas; never inline a schema used in 2+ places.
- Define `securitySchemes` once in `components.securitySchemes`; reference per-operation with `security`.
- For multi-tenant or versioned APIs, prefer `servers[].variables` over per-operation server overrides.
- Use `application/problem+json` for error responses (RFC 7807) — Redocly's recommended preset checks for this.
- Pair every 4xx/5xx with at least one `examples` entry.

## Edge cases

- **AsyncAPI:** Redocly CLI supports AsyncAPI 2.x and 3.x with the same `lint`/`bundle` commands.
- **OpenAPI 3.0 → 3.1 migration:** `redocly bundle --upgrade-from-3-0-to-3-1` (experimental as of June 2026); validate manually.
- **Spectral users:** Redocly can consume Spectral rulesets via `extends: spectral:oas`.
- **`build-docs` with Scalar theming:** pass `--theme=alternate` (saturn/solarized/etc); for full customization, prefer Scalar CLI direct.

## Sources

- Redocly CLI: https://github.com/Redocly/redocly-cli
- Redocly CLI docs: https://redocly.com/docs/cli/
- Scalar API reference: https://github.com/scalar/scalar
- OpenAPI 3.1 spec: https://spec.openapis.org/oas/v3.1.0
