---
name: mintlify-api-docs
description: Author and ship API documentation with Mintlify — auto-generated playgrounds, llms.txt for AI agent ingestion, MCP integration, and `mint dev`/`mint deploy` workflow. Use when the user wants AI-first, hosted, branded API docs from an OpenAPI spec.
---

# Mintlify API Docs

Mintlify is the 2026 SOTA hosted-documentation platform for API references. It ships auto-generated try-it-out playgrounds, an llms.txt feed that lets AI agents (Claude / ChatGPT / Cursor) index the docs, an MCP server for agent-driven doc lookup, and a CLI that bundles local preview + deploy.

## When to use this skill

- The user has an OpenAPI 3.x spec and wants hosted docs with a try-it-out playground out of the box.
- The user wants AI-friendly docs (llms.txt + MCP) so agents can answer "how do I call your API" without scraping HTML.
- The user wants a branded developer portal without owning a Docusaurus/Starlight build.
- The user is comfortable with a hosted platform (free OSS plan, paid teams plan).

**Do NOT use this skill when:**
- The user explicitly wants self-hosted docs with no third-party dependency → use `redocly-openapi-pipeline` or `docusaurus-vitepress-starlight-mkdocs` instead.
- The user is on the wshobson Sphinx/MkDocs Python stack → use `sphinx-typedoc-reference-docs`.

## Setup

### Install the CLI (one-time)

```bash
npm i -g mintlify
mintlify --version    # confirm install
```

The CLI requires Node 18+. The agent should probe via `node --version` before running install.

### Initialize a new docs site

```bash
mintlify init docs/
cd docs
mintlify dev          # local preview at http://localhost:3000
```

`mintlify init` writes:

- `docs.json` — site config, navigation, theme, API source paths.
- `index.mdx` — landing page.
- `api-reference/` — auto-generated reference pages from an OpenAPI source.

### Wire an OpenAPI spec

In `docs.json`:

```json
{
  "name": "Acme API",
  "navigation": {
    "tabs": [
      { "tab": "Guides", "groups": [{ "group": "Get started", "pages": ["index", "quickstart"] }] },
      { "tab": "API reference", "openapi": "api/openapi.yaml" }
    ]
  },
  "api": {
    "playground": { "display": "interactive" },
    "examples": { "languages": ["curl", "python", "javascript", "go"] }
  }
}
```

`openapi` may be a local path or an https URL. Mintlify regenerates the reference on every `mint dev` / `mint deploy` run; do not hand-edit the reference pages.

### Enable llms.txt and MCP

```json
{
  "integrations": {
    "llmstxt": { "enabled": true },
    "mcp":      { "enabled": true, "auth": "none" }
  }
}
```

After `mint deploy`, the docs site exposes:

- `https://<site>/llms.txt` — markdown index for AI agents.
- `https://<site>/llms-full.txt` — full content dump for AI agents.
- `https://<site>/mcp` — Mintlify-hosted MCP endpoint that any MCP client can connect to.

## Common recipes

### Recipe 1: Author + preview cycle

```bash
mintlify dev              # hot-reload preview
# edit *.mdx, save, see updates in <1s
mintlify broken-links     # link checker (built-in)
mintlify deploy           # ship to hosted site
```

### Recipe 2: API reference from existing OpenAPI

1. Drop `openapi.yaml` into `api/`.
2. Add to `docs.json`: `"tabs": [{ "tab": "API", "openapi": "api/openapi.yaml" }]`.
3. Run `mintlify dev` — playground is live.
4. Override individual endpoint pages by creating `api-reference/<operationId>.mdx` with custom prose; the playground stays auto-generated.

### Recipe 3: MDX components for code switchers

```mdx
<CodeGroup>

```bash cURL
curl https://api.example.com/orders \
  -H "Authorization: Bearer $TOKEN"
```

```python Python
client.orders.list()
```

```javascript JavaScript
await acme.orders.list();
```

</CodeGroup>
```

Mintlify auto-builds language switchers, copy-to-clipboard, and syntax highlighting.

### Recipe 4: Snippet reuse with Card/CardGroup

```mdx
<CardGroup cols={2}>
  <Card title="Quickstart" icon="rocket" href="/quickstart">
    Ship your first request in 3 minutes.
  </Card>
  <Card title="API reference" icon="square-terminal" href="/api-reference">
    Every endpoint, every parameter.
  </Card>
</CardGroup>
```

### Recipe 5: Versioning

```json
{
  "versions": ["v2", "v1"],
  "navigation": {
    "versions": {
      "v2": [{ "group": "Get started", "pages": ["v2/intro"] }],
      "v1": [{ "group": "Get started", "pages": ["v1/intro"] }]
    }
  }
}
```

Mintlify renders a version switcher in the navbar.

## Edge cases

- **Custom domain:** `mintlify deploy` ships to `<slug>.mintlify.app` by default; CNAME a subdomain (`docs.example.com`) in the Mintlify dashboard for branded URLs.
- **Authenticated docs:** Mintlify supports JWT/SAML; configure in dashboard, then the playground sends the user's token on try-it-out calls.
- **OpenAPI 3.1 + JSON Schema 2020-12:** fully supported as of 2025. For older 3.0 specs, run through `redocly bundle` first.
- **Broken-link check is fast but not transitive:** still run `lychee` against the deployed site (see `lychee-link-checking`).
- **CI deploy:** `mint deploy` in CI requires `MINTLIFY_API_TOKEN`. Add via `gh secret set MINTLIFY_API_TOKEN`.

## Sources

- Mintlify CLI docs: https://mintlify.com/docs/installation
- Mintlify llms.txt support: https://mintlify.com/blog/llmstxt
- Mintlify MCP server: https://mintlify.com/docs/integrations/mcp
- Source: https://www.mintlify.com/library/best-api-docs-and-sdk-generation-tools
