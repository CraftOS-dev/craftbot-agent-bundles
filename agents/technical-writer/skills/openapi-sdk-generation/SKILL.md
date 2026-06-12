---
name: openapi-sdk-generation
description: Generate language-specific SDKs from a single OpenAPI spec — `@hey-api/openapi-ts` (TS-first, modern), `@openapitools/openapi-generator-cli` (multi-language: TS/Python/Go/Java/C#/PHP/Ruby), Speakeasy / Fern (paid, polished output). Use when shipping SDKs alongside docs.
---

# OpenAPI → SDK Generation

One OpenAPI spec, many SDKs. The 2026 SOTA stack:

- **`@hey-api/openapi-ts`** — fastest, cleanest TypeScript output, modern client architecture (fetch / axios / next / Hono).
- **`@openapitools/openapi-generator-cli`** — multi-language coverage (TS / Python / Go / Java / C# / PHP / Ruby / Rust / Kotlin / Swift / Dart). Java-based generator; clunkier output but unmatched breadth.
- **Speakeasy** — paid, ergonomic, ships SDKs with idiomatic per-language patterns (pagination, retries, telemetry). Best for production SDKs at scale.
- **Fern** — paid alternative to Speakeasy; ships SDK + docs + CLI.

## When to use this skill

- The user has a stable OpenAPI 3.x spec and wants TS / Python / Go / etc client libraries.
- The user wants to publish SDK packages to npm / PyPI / Go Modules / etc.
- The user wants SDK references generated alongside API docs (Mintlify, Redocly).

## Setup

### Install (TypeScript only)

```bash
# @hey-api/openapi-ts — recommended for new TS projects
npm i -D @hey-api/openapi-ts

# OR @openapitools/openapi-generator-cli — multi-language
npm i -D @openapitools/openapi-generator-cli
```

The openapi-generator-cli wraps a Java JAR; first run downloads it. Requires JDK 11+.

## Common recipes

### Recipe 1: TypeScript SDK with `@hey-api/openapi-ts`

```bash
npx @hey-api/openapi-ts \
  --input ./api/openapi.yaml \
  --output ./packages/sdk-ts/src \
  --client @hey-api/client-fetch
```

Project config `openapi-ts.config.ts`:

```typescript
import { defineConfig } from '@hey-api/openapi-ts';

export default defineConfig({
  input: './api/openapi.yaml',
  output: {
    path: './packages/sdk-ts/src',
    format: 'prettier',
    lint:   'eslint',
  },
  plugins: [
    '@hey-api/client-fetch',
    '@hey-api/typescript',
    '@hey-api/sdk',
    '@hey-api/schemas',
    { name: '@tanstack/react-query' },        // optional: gen react-query hooks
  ],
});
```

Then `npx openapi-ts`.

Output structure:

```
packages/sdk-ts/src/
├── client.gen.ts        # fetch client
├── sdk.gen.ts           # one function per operationId
├── types.gen.ts         # request/response types
└── schemas.gen.ts       # JSON Schema runtime objects
```

### Recipe 2: Multi-language SDKs with openapi-generator-cli

```bash
# TypeScript (axios)
npx @openapitools/openapi-generator-cli generate \
  -i ./api/openapi.yaml \
  -g typescript-axios \
  -o ./packages/sdk-ts \
  --additional-properties=npmName=@acme/sdk,supportsES6=true

# Python
npx @openapitools/openapi-generator-cli generate \
  -i ./api/openapi.yaml \
  -g python \
  -o ./packages/sdk-py \
  --additional-properties=packageName=acme_sdk,packageVersion=2.0.0

# Go
npx @openapitools/openapi-generator-cli generate \
  -i ./api/openapi.yaml \
  -g go \
  -o ./packages/sdk-go \
  --additional-properties=packageName=acme

# Java
npx @openapitools/openapi-generator-cli generate \
  -i ./api/openapi.yaml \
  -g java \
  -o ./packages/sdk-java \
  --additional-properties=groupId=com.acme,artifactId=acme-sdk

# C#
npx @openapitools/openapi-generator-cli generate \
  -i ./api/openapi.yaml \
  -g csharp \
  -o ./packages/sdk-csharp \
  --additional-properties=packageName=Acme.Sdk

# Ruby
npx @openapitools/openapi-generator-cli generate \
  -i ./api/openapi.yaml \
  -g ruby \
  -o ./packages/sdk-rb \
  --additional-properties=gemName=acme-sdk
```

### Recipe 3: openapi-generator-cli config file

`openapitools.json`:

```json
{
  "$schema": "node_modules/@openapitools/openapi-generator-cli/config.schema.json",
  "spaces": 2,
  "generator-cli": {
    "version": "7.x.x",
    "generators": {
      "ts": {
        "generatorName": "typescript-axios",
        "output": "packages/sdk-ts",
        "inputSpec": "api/openapi.yaml",
        "additionalProperties": { "supportsES6": true }
      },
      "py": {
        "generatorName": "python",
        "output": "packages/sdk-py",
        "inputSpec": "api/openapi.yaml",
        "additionalProperties": { "packageName": "acme_sdk" }
      }
    }
  }
}
```

Then `npx openapi-generator-cli generate` regenerates everything.

### Recipe 4: CI gate — regen and verify-no-diff

```yaml
# .github/workflows/sdks.yml
name: SDKs
on: [pull_request]
jobs:
  regen:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npx @openapitools/openapi-generator-cli generate
      - run: git diff --exit-code packages/   # fail if SDKs drifted from spec
```

### Recipe 5: Speakeasy (paid; SOTA polish)

```bash
brew install speakeasy
speakeasy quickstart
# wizard creates `.speakeasy/workflow.yaml`
speakeasy run     # generates all configured SDKs + publishes
```

Speakeasy auto-publishes to npm/PyPI/Go Modules/Maven via Speakeasy-managed releases. Use when SDK quality and per-language idioms matter more than zero-cost.

### Recipe 6: Fern (paid; alt to Speakeasy)

```bash
npm i -g fern-api
fern init
# edit fern/api/definition/api.yml (Fern's spec format) OR import openapi.yaml
fern generate     # SDKs to packages/<lang>
```

Fern's selling point is bundling SDKs + docs + a Postman-style client in one workflow.

### Recipe 7: Publish workflow per language

| Language | Publish command | Registry |
|---|---|---|
| TypeScript | `npm publish --access public` | npm |
| Python | `uv build && uv publish` | PyPI |
| Go | tag commit (`git tag v1.0.0 && git push --tags`) | Go modules (auto-discovered) |
| Java | `mvn deploy` | Maven Central |
| C# | `dotnet pack && dotnet nuget push` | NuGet |
| Ruby | `gem build *.gemspec && gem push *.gem` | RubyGems |

## Tool selection cheat sheet

| Use case | Tool |
|---|---|
| TS-only, modern fetch/axios client, no Java dep | `@hey-api/openapi-ts` |
| Multi-language, free, OSS-friendly | `@openapitools/openapi-generator-cli` |
| Paid budget, want polished idiomatic SDKs | Speakeasy |
| Paid budget, want SDK + docs unified | Fern |
| Java/Kotlin-heavy shop | openapi-generator-cli (best Java output) |
| Rust SDK | openapi-generator-cli (`-g rust`) |

## Edge cases

- **OpenAPI 3.1 support:** `@hey-api/openapi-ts` is fully 3.1-compatible; openapi-generator's 3.1 support shipped in v7.x and is generator-dependent (TS/Python/Go are solid; Java/C# lag).
- **Discriminator unions:** spec must use OpenAPI 3.1's `discriminator` + `oneOf` correctly; otherwise generated unions are `any`.
- **Pagination:** none of the OSS generators auto-handle cursor pagination — wrap manually or use Speakeasy/Fern.
- **Auth:** generators emit a configuration object; document how to set `apiKey` / `bearerToken` in the SDK README.
- **Generated code in git:** prefer committing for review traceability; add `.gen.ts` suffix and exclude from linters with `.eslintignore`.

## Sources

- @hey-api/openapi-ts: https://github.com/hey-api/openapi-ts
- @openapitools/openapi-generator-cli: https://github.com/OpenAPITools/openapi-generator-cli
- OpenAPI Generator: https://openapi-generator.tech/
- Speakeasy: https://www.speakeasy.com/
- Fern: https://www.buildwithfern.com/
