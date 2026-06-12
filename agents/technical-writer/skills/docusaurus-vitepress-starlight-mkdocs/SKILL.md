---
name: docusaurus-vitepress-starlight-mkdocs
description: Decision tree and per-stack setup for the 2026 SOTA self-hosted doc generators — Docusaurus (React/MDX), VitePress (Vue), Astro Starlight (Islands), MkDocs Material (Python). Includes scaffold commands and deploy workflows (Cloudflare Pages / Vercel / GitHub Pages).
---

# Docusaurus / VitePress / Starlight / MkDocs Material

Choose by the team's existing stack and constraints. All four are SOTA in 2026; none is universally best.

## Decision tree

```
START
  │
  ├─ Team uses React already?              → Docusaurus
  ├─ Team uses Vue already?                → VitePress
  ├─ Python project, wants simple config?  → MkDocs Material
  ├─ Wants fastest cold builds + Islands?  → Astro Starlight
  ├─ Wants AI-first + hosted + branded?    → Mintlify (see mintlify-api-docs)
  └─ Heavy versioning needs?               → Docusaurus
```

| | Docusaurus | VitePress | Starlight | MkDocs Material |
|---|---|---|---|---|
| Framework | React | Vue | Astro | Python (Jinja) |
| Build speed | Medium | Fastest (Vite) | Fast (cold), fastest (warm) | Fast |
| MDX | ✓ | partial (`<script setup>`) | ✓ (Astro components) | extensions only |
| Versioning | best-in-class | yes (plugin) | manual | mike plugin |
| i18n | best-in-class | yes | yes | i18n plugin |
| Search | Algolia / pagefind | local + Algolia | pagefind | built-in lunr / Algolia |
| Weekly DLs (npm/PyPI, 2026) | ~3M | ~600k | ~700k | ~1.5M (PyPI) |
| Best for | React shops, big sites | Vue, small/medium | Speed-obsessed | Python ecosystem |

## When to use this skill

- The user is starting a new docs site.
- The user wants to migrate from an older generator (Gitbook, Read the Docs default, Jekyll).
- The user is comparing options for an RFC.

## Setup — Docusaurus

```bash
npx create-docusaurus@latest docs classic --typescript
cd docs
npm start                # http://localhost:3000
```

Key files:

- `docusaurus.config.js` — site config.
- `sidebars.js` — navigation.
- `docs/intro.md` — first page.

Versioning:

```bash
npm run docusaurus docs:version 1.0.0
# creates versioned_docs/version-1.0.0/ + sidebar
```

Deploy:

```yaml
# .github/workflows/deploy.yml — GitHub Pages
- uses: actions/checkout@v4
- uses: actions/setup-node@v4
  with: { node-version: 20 }
- run: cd docs && npm ci && npm run build
- uses: peaceiris/actions-gh-pages@v4
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: docs/build
```

Cloudflare Pages: connect repo, build command `npm run build`, output dir `build`.

## Setup — VitePress

```bash
npm create vitepress@latest docs
cd docs
npm run docs:dev
```

`docs/.vitepress/config.ts`:

```typescript
import { defineConfig } from 'vitepress';

export default defineConfig({
  title: 'Acme',
  description: 'Acme docs',
  themeConfig: {
    nav:     [{ text: 'Guide', link: '/guide/' }, { text: 'API', link: '/api/' }],
    sidebar: { '/guide/': [{ text: 'Intro', items: [{ text: 'Quickstart', link: '/guide/quickstart' }] }] },
    search:  { provider: 'local' },        // or 'algolia'
    editLink: { pattern: 'https://github.com/acme/docs/edit/main/:path' },
  },
});
```

Deploy: `npm run docs:build` → `docs/.vitepress/dist/`.

## Setup — Astro Starlight

```bash
npm create astro@latest -- --template starlight
cd <project>
npm run dev
```

`astro.config.mjs`:

```javascript
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  integrations: [starlight({
    title: 'Acme',
    social: { github: 'https://github.com/acme/docs' },
    sidebar: [
      { label: 'Guide', autogenerate: { directory: 'guide' } },
      { label: 'API',   autogenerate: { directory: 'reference' } },
    ],
    plugins: [
      // starlight-typedoc, starlight-openapi, etc.
    ],
  })],
});
```

Deploy: `npm run build` → `dist/`.

## Setup — MkDocs Material

```bash
uv add mkdocs-material mkdocs-glightbox mkdocs-git-revision-date-localized-plugin
mkdocs new .
```

`mkdocs.yml`:

```yaml
site_name: Acme
site_url: https://docs.example.com

theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.path
    - navigation.indexes
    - navigation.top
    - search.suggest
    - search.highlight
    - content.code.copy
    - content.code.annotate
  palette:
    - scheme: default
      toggle: { icon: material/brightness-7, name: Switch to dark mode }
    - scheme: slate
      toggle: { icon: material/brightness-4, name: Switch to light mode }

plugins:
  - search
  - glightbox
  - git-revision-date-localized
  - mkdocstrings:
      handlers:
        python:
          options:
            show_source: true
            show_root_heading: true

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed: { alternate_style: true }
  - pymdownx.snippets
  - pymdownx.highlight: { anchor_linenums: true }
  - tables
  - footnotes
```

Build: `mkdocs build`. Serve: `mkdocs serve`.

Versioning via **mike**:

```bash
uv add mike
mike deploy --push --update-aliases 1.0 latest
mike set-default --push latest
```

## Deploy targets — comparison

| Target | Docusaurus | VitePress | Starlight | MkDocs |
|---|---|---|---|---|
| GitHub Pages | ✓ official action | ✓ | ✓ | ✓ |
| Cloudflare Pages | ✓ native | ✓ | ✓ | ✓ (Python buildpack) |
| Vercel | ✓ | ✓ | ✓ | ✓ |
| Netlify | ✓ | ✓ | ✓ | ✓ |
| Self-host (nginx/S3) | ✓ static | ✓ static | ✓ static | ✓ static |

Recommended default: **Cloudflare Pages** (free, fastest CDN, Workers integration).

## i18n setup quickref

| Generator | i18n config |
|---|---|
| Docusaurus | `i18n: { defaultLocale: 'en', locales: ['en', 'fr'] }` in config |
| VitePress | `locales` map in config |
| Starlight | `locales` map in starlight config |
| MkDocs Material | `i18n` plugin with per-language file suffix or directory |

See `deepl-translation-i18n` for the translation workflow.

## Search setup quickref

| Generator | Default | Drop-in upgrade |
|---|---|---|
| Docusaurus | none | Algolia DocSearch (free for OSS) |
| VitePress | local minisearch | Algolia DocSearch |
| Starlight | pagefind (local) | Algolia DocSearch |
| MkDocs Material | local lunr | Algolia, Pagefind, MeiliSearch |

See `algolia-doc-search` for setup.

## Common recipes

### Recipe 1: OpenAPI reference in any of these sites

- **Docusaurus:** `docusaurus-plugin-openapi-docs` (community).
- **VitePress:** `vitepress-openapi`.
- **Starlight:** `starlight-openapi`.
- **MkDocs Material:** `neoteroi-mkdocs` with `neoteroi.spantable` and OpenAPI plugin.

For polished output, prefer routing the API reference through Mintlify/Scalar/ReDoc (see `mintlify-api-docs`, `redocly-openapi-pipeline`) and embedding via iframe or subdomain.

### Recipe 2: Migrate from Gitbook → Docusaurus

```bash
npx @docusaurus/migrate import-gitbook /path/to/gitbook-export /path/to/new-docs
```

### Recipe 3: Bulk redirect old paths

Docusaurus: `@docusaurus/plugin-client-redirects`.
VitePress: `vite.config.ts` rewrite rules.
Starlight: `astro:redirects` config.
MkDocs Material: `redirects` plugin.

## Edge cases

- **MDX in MkDocs:** not natively supported. Use Material's `pymdownx` extensions for ~80% of MDX power.
- **React components in Starlight:** wrap in `client:load`, otherwise they don't hydrate.
- **Docusaurus + heavy MDX:** build slowdown — code-split with `<BrowserOnly>` and dynamic imports.
- **VitePress + many locales:** path-based routing only; subdomain routing requires custom server.
- **MkDocs without Python:** there are non-Python rewrites but Material is still the leader.

## Sources

- Docusaurus: https://docusaurus.io/
- VitePress: https://vitepress.dev/
- Astro Starlight: https://starlight.astro.build/
- MkDocs Material: https://squidfunk.github.io/mkdocs-material/
