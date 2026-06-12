<!--
Source: https://github.com/wshobson/agents/blob/main/plugins/documentation-generation/skills/openapi-spec-generation/SKILL.md
Repo: wshobson/agents
-->
---
name: openapi-spec-generation
description: Generate and maintain OpenAPI 3.1 specifications from code, design-first specs, and validation patterns. Use when creating API documentation, generating SDKs, or ensuring API contract compliance.
---

# OpenAPI Spec Generation

Comprehensive patterns for creating, maintaining, and validating OpenAPI 3.1 specifications for RESTful APIs.

## When to Use This Skill

- Creating API documentation from scratch
- Generating OpenAPI specs from existing code
- Designing API contracts (design-first approach)
- Validating API implementations against specs
- Generating client SDKs from specs
- Setting up API documentation portals

## Core Concepts

### OpenAPI 3.1 Structure

```yaml
openapi: 3.1.0
info:
  title: API Title
  version: 1.0.0
servers:
  - url: https://api.example.com/v1
paths:
  /resources:
    get: ...
components:
  schemas: ...
  securitySchemes: ...
```

### Design Approaches

| Approach | Description | Best For |
|---|---|---|
| **Design-First** | Write spec before code | New APIs, contracts |
| **Code-First** | Generate spec from code | Existing APIs |
| **Hybrid** | Annotate code, generate spec | Evolving APIs |

## Best Practices

### Do's
- **Use $ref** — Reuse schemas, parameters, responses
- **Add examples** — Real-world values help consumers
- **Document errors** — All possible error codes
- **Version your API** — In URL or header
- **Use semantic versioning** — For spec changes

### Don'ts
- Don't use generic descriptions — be specific
- Don't skip security — define all schemes
- Don't forget nullable — be explicit about null
- Don't mix styles — consistent naming throughout
- Don't hardcode URLs — use server variables
