---
name: kb-versioning-per-product-docusaurus-mike
description: Per-product-version KB snapshots via Docusaurus versions, mike (MkDocs), Mintlify versions.json, sphinx-multiversion. Version dropdown UI, canonical-to-latest, redirects from old versions. Use when documenting a product whose API/UX changes per release and v1 users must still find their docs.
---

# KB versioning — per-product-version snapshots (Docusaurus / mike / Mintlify / Sphinx)

## When to use

Reach for this skill when the user says: "version our docs per release", "we just shipped v2 and v1 customers still need their docs", "add a version dropdown", "snapshot the docs at release time", "freeze the v1 reference", or "the docs only show the latest version". Skip this skill for evergreen single-version KBs (don't version a marketing-tour KB); skip for documentation of self-updating SaaS where every customer is always on latest — versioning is a tax. Pair with `content-migration-between-platforms` if migrating from unversioned → versioned.

## Setup

```bash
# Docusaurus (versions baked into the CLI; no install needed beyond Docusaurus itself)
npx create-docusaurus@latest my-docs classic
cd my-docs && npm install

# mike (MkDocs versioning)
pip install mike
mkdocs --version  # confirm >= 1.5

# sphinx-multiversion (Sphinx per-branch docs)
pip install sphinx-multiversion

# Mintlify (versions baked into versions.json — no install beyond Mintlify CLI)
npm i -g mintlify
mintlify --version
```

Auth / env vars:
- No API keys required for any of these — they all operate on the source repo + build output.
- `GH_TOKEN` if using GitHub Actions to push the versioned site to `gh-pages` branch.

## Common recipes

### Recipe 1: Snapshot a new Docusaurus version

```bash
# Run BEFORE shipping v2.0 — freezes current docs/ tree into versioned_docs/version-2.0/
npm run docusaurus docs:version 2.0

# Files created:
#   versioned_docs/version-2.0/        # frozen markdown
#   versioned_sidebars/version-2.0-sidebars.json
#   versions.json                       # ["2.0","1.0"]
git add versioned_docs versioned_sidebars versions.json
git commit -m "docs: snapshot v2.0"
```

After `docs:version`, the `docs/` folder continues to be the "next" (unreleased) version. Old versions live in `versioned_docs/`.

### Recipe 2: Configure Docusaurus version dropdown + label

```js
// docusaurus.config.js
module.exports = {
  presets: [['classic', {
    docs: {
      lastVersion: 'current',          // 'current' = docs/ (next); or '2.0'
      versions: {
        current: { label: '2.1 (next)', path: 'next', banner: 'unreleased' },
        '2.0': { label: '2.0', path: '/' },               // default route
        '1.0': { label: '1.0', path: '1.0', banner: 'unmaintained' },
      },
    },
  }]],
  themeConfig: {
    navbar: { items: [{ type: 'docsVersionDropdown', position: 'right' }] },
  },
};
```

Banner values: `none` | `unreleased` | `unmaintained`. Apply `unmaintained` to versions you no longer patch.

### Recipe 3: mike deploy a new MkDocs version

```bash
# Deploys the current site as v2.0 AND aliases it as 'latest'
mike deploy --push --update-aliases 2.0 latest

# Set 2.0 as the default landing
mike set-default --push latest

# Inspect what's deployed
mike list
# 2.0 [latest]
# 1.0
# 1.1
```

`mike` writes to the `gh-pages` branch by default. Each `mike deploy` adds a folder; `mike alias` creates symlinks. The dropdown is rendered by `mkdocs-material`'s `version` extra.

### Recipe 4: Configure mkdocs-material version selector

```yaml
# mkdocs.yml
extra:
  version:
    provider: mike
    default: latest
    alias: true

theme:
  name: material
```

The selector appears in the header. Combined with `mike alias`, `https://docs.example.com/latest/...` always redirects to the newest alias.

### Recipe 5: Mintlify versions.json

```json
{
  "$schema": "https://mintlify.com/docs.json",
  "versions": [
    { "name": "v2", "default": true },
    { "name": "v1" }
  ],
  "navigation": {
    "versions": [
      {
        "version": "v2",
        "groups": [{ "group": "Get started", "pages": ["v2/quickstart"] }]
      },
      {
        "version": "v1",
        "groups": [{ "group": "Get started", "pages": ["v1/quickstart"] }]
      }
    ]
  }
}
```

Mintlify renders a version dropdown in the navbar. Folder layout: `v2/` and `v1/` at repo root; canonical URL goes to `default: true`.

### Recipe 6: sphinx-multiversion build per-branch

```python
# conf.py additions
templates_path = ['_templates']
html_sidebars = {
    '**': ['versions.html', 'localtoc.html', 'searchbox.html'],
}

# Whitelist branches/tags to build
smv_branch_whitelist = r'^(main|release/.*)$'
smv_tag_whitelist = r'^v\d+\.\d+$'
smv_released_pattern = r'^tags/v\d+\.\d+$'
```

```bash
# Build all matching branches and tags into _build/
sphinx-multiversion docs _build
```

`versions.html` template renders the dropdown. Each branch/tag gets a subfolder under `_build/`.

### Recipe 7: Per-version redirects (Docusaurus → /v1 → /v2)

```js
// docusaurus.config.js — using @docusaurus/plugin-client-redirects
plugins: [
  ['@docusaurus/plugin-client-redirects', {
    redirects: [
      { from: '/docs/1.0/authentication/sso', to: '/docs/2.0/authentication/sso' },
      { from: '/docs/1.0/webhooks', to: '/docs/2.0/webhooks/configure' },
    ],
    createRedirects(existingPath) {
      // Pattern-based: send any /1.0 path missing in 2.0 to the 2.0 root
      if (existingPath.startsWith('/docs/2.0/')) {
        return [existingPath.replace('/docs/2.0/', '/docs/1.0/')];
      }
      return undefined;
    },
  }],
],
```

For server-level redirects, use `_redirects` (Netlify), `vercel.json`, or Cloudflare Pages — same syntax as `kb-taxonomy-design` recipe 8.

### Recipe 8: Mid-version patch badge ("Updated in 2.0.3")

```markdown
---
title: Webhook retry strategy
updated_in: 2.0.3
---

import UpdatedBadge from '@site/src/components/UpdatedBadge';

<UpdatedBadge version="2.0.3" /> The retry budget changed in 2.0.3 — see [changelog](/changelog#2-0-3).
```

```jsx
// src/components/UpdatedBadge.jsx
export default function UpdatedBadge({ version }) {
  return <span className="badge badge--info">Updated in {version}</span>;
}
```

Surfaces inline so readers know a section changed without diffing the whole page.

### Recipe 9: Deprecate an old version (banner + redirect)

```js
// docusaurus.config.js
versions: {
  '1.0': {
    label: '1.0 (unmaintained — upgrade to 2.0)',
    banner: 'unmaintained',
    path: '1.0',
  },
},
```

Then add a 410 Gone or 301 redirect for high-value 1.0 pages → 2.0 equivalents (Recipe 7). Keep 1.0 indexable for 90d after deprecation; then remove from sitemap.

### Recipe 10: CI gate — block release if version snapshot missing

```yaml
# .github/workflows/version-gate.yml
name: Version snapshot gate
on:
  push:
    tags: ['v*.*.*']
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Ensure docs snapshotted for tag
        run: |
          TAG=${GITHUB_REF##*/v}
          if ! jq -e --arg t "$TAG" 'index($t)' versions.json >/dev/null; then
            echo "::error::No docs snapshot for $TAG — run 'npm run docusaurus docs:version $TAG'"
            exit 1
          fi
```

Forces engineers to snapshot docs before tagging a release.

## Examples

### Example 1: Snapshot v2.0 for Docusaurus + ship version dropdown

**Goal:** Customers on v1 keep their docs; new visitors see v2 by default.

**Steps:**
1. Verify current `docs/` reflects v2.0 (last v2 PR merged).
2. Run `npm run docusaurus docs:version 2.0` (Recipe 1).
3. Edit `docusaurus.config.js` to add `versions: { '2.0': { label: '2.0', path: '/' }, '1.0': { label: '1.0', banner: 'unmaintained' } }` (Recipe 2).
4. Add `docsVersionDropdown` navbar item (Recipe 2).
5. Test locally: `npm run start` — confirm dropdown works.
6. Write redirect map for renamed 1.0 → 2.0 URLs (Recipe 7).
7. Commit + ship.

**Result:** `https://docs.example.com/` defaults to 2.0. `/1.0/...` still works with the "unmaintained" banner.

### Example 2: Migrate MkDocs site to mike + first versioned deploy

**Goal:** Existing MkDocs site has no versioning — add it before v3 ships.

**Steps:**
1. `pip install mike` (Setup).
2. Configure `mkdocs.yml` with `extra.version.provider: mike` (Recipe 4).
3. From current `main` branch (= v2.x): `mike deploy --push --update-aliases 2.0 latest`.
4. `mike set-default --push latest`.
5. When v3.0 ships: `mike deploy --push --update-aliases 3.0 latest` (re-aliases `latest` to 3.0).
6. v2.0 stays accessible at `/2.0/...`.

**Result:** Version dropdown lives in navbar; deep links to old versions stable.

### Example 3: Sphinx project with per-branch docs

**Goal:** Build docs for `main` + every `v*.*` tag into one site.

**Steps:**
1. `pip install sphinx-multiversion`.
2. Add `smv_branch_whitelist`, `smv_tag_whitelist` to `conf.py` (Recipe 6).
3. Add `versions.html` template under `_templates/`.
4. Build: `sphinx-multiversion docs _build`.
5. Inspect `_build/` — one folder per branch/tag.
6. Deploy `_build/` to GitHub Pages or S3.

**Result:** Single site with branch + tag selectors; all docs builds reproducible from git history.

## Edge cases / gotchas

- **Docusaurus snapshot is destructive-ish** — after `docs:version`, edits to `docs/` only affect the "next" version. To patch an older version, edit `versioned_docs/version-2.0/` directly.
- **mike writes to `gh-pages` branch** — don't push generated files to `main`. Set `gh-pages` as the GitHub Pages source.
- **Version proliferation** — keep ≤3 active versions in dropdown. Archive older versions to subdomain or redirect to migration guide.
- **`lastVersion`** in Docusaurus controls which version `/docs/...` URL maps to. Default is `current` (next/unreleased). Switch to a released version (e.g., `'2.0'`) to make production routes stable.
- **mkdocs-material version selector requires `mike`** — it won't read `versions.json`-style alternatives. The provider must be `mike`.
- **Mintlify default version controls canonical URL** — set `default: true` on exactly one version. Multiple defaults = build error.
- **sphinx-multiversion needs absolute imports** in `conf.py` — relative imports break across branches if dirs renamed.
- **Sidebar drift** — each Docusaurus version has its own `versioned_sidebars/version-X.Y-sidebars.json`. Restructuring the sidebar in `docs/` doesn't backport.
- **CI build time grows linearly** with versions — `sphinx-multiversion` rebuilds every whitelisted branch on each commit. Cache or shard if >5 versions.
- **Cross-version search** — Docusaurus + Algolia DocSearch by default indexes only the default version; configure `facetFilters: ['version:2.0']` to filter, or run separate indices.
- **Redirects per-version vs global** — declare per-version redirects in `versions.json` (Mintlify) or via `@docusaurus/plugin-client-redirects` with version-aware paths.
- **Branch naming for sphinx-multiversion** — match `smv_branch_whitelist` regex exactly. `release/v2.0` ≠ `v2.0`; pick a convention and stick with it.
- **Don't snapshot too early** — `docs:version` BEFORE final QA bakes in mistakes. Snapshot on release-day, not release-week.

## Sources

- [Docusaurus versioning docs](https://docusaurus.io/docs/versioning)
- [Docusaurus plugin-client-redirects](https://docusaurus.io/docs/api/plugins/@docusaurus/plugin-client-redirects)
- [mike (MkDocs versioning) — GitHub](https://github.com/jimporter/mike)
- [mkdocs-material version selector](https://squidfunk.github.io/mkdocs-material/setup/setting-up-versioning/)
- [sphinx-multiversion docs](https://holzhaus.github.io/sphinx-multiversion/master/index.html)
- [Mintlify versions reference](https://mintlify.com/docs/settings/versions)
- [Diataxis on versioning vs deprecation](https://diataxis.fr/needs/)
- [Write the Docs — versioning patterns](https://www.writethedocs.org/guide/tools/version-control/)
