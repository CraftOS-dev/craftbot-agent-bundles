---
name: content-reuse-single-source-asciidoc-antora
description: Single-source publishing for multi-product / multi-channel KBs — AsciiDoc + Antora (DITA-style topic modules → multi-output), Docusaurus MDX partials, Mintlify Snippets, Astro Starlight content collections. Use when one canonical "write SSO setup once" must render in 3+ places (web docs, PDF, in-app help).
---

# Content reuse — single-source publishing (AsciiDoc/Antora, MDX partials, snippets)

## When to use

Reach for this skill when the user says: "we keep writing the same warning paragraph in 5 places", "our product manual and web docs drift", "single-source publishing", "reuse content across docs", "DITA-like reuse without DITA", "we maintain N copies of the install instructions". Use AsciiDoc + Antora for large enterprise KBs (3+ products, PDF + web + in-app output). Use MDX partials / Mintlify snippets / Astro content collections when staying markdown-native is the priority. Skip this skill for KBs with <5 reused fragments — the maintenance overhead beats the savings.

## Setup

```bash
# Antora (AsciiDoc topic-modules → static site)
npm i -g @antora/cli @antora/site-generator
antora --version

# AsciiDoctor (if rendering AsciiDoc outside Antora)
gem install asciidoctor asciidoctor-pdf

# Docusaurus / MDX (assumed already set up if going the MDX route)
# Mintlify snippets — no install; just /snippets folder in repo
# Astro Starlight content collections — already in @astrojs/starlight
```

Auth / env vars: none — all four approaches operate on the source repo.

## Common recipes

### Recipe 1: Antora playbook for a multi-product KB

```yaml
# antora-playbook.yml
site:
  title: Acme Docs
  url: https://docs.example.com
  start_page: acme::index.adoc

content:
  sources:
    - url: https://github.com/acme/product-a
      branches: [main, v2.0, v1.0]
      start_path: docs
    - url: https://github.com/acme/product-b
      branches: [main, v3.0]
      start_path: docs
    - url: https://github.com/acme/shared-topics
      branches: [main]
      start_path: docs

ui:
  bundle:
    url: https://gitlab.com/antora/antora-ui-default/-/jobs/artifacts/HEAD/raw/build/ui-bundle.zip
```

```bash
# Build the multi-product site
antora antora-playbook.yml --to-dir build/site
```

Each product is a "component"; shared content lives in a separate component. Antora composes one site from all of them with version-aware navigation.

### Recipe 2: AsciiDoc include directive (the core reuse primitive)

```asciidoc
= SSO Setup
:experimental:

== Okta integration

include::shared:partial$sso-prereqs.adoc[]

The Acme app exposes a SAML 2.0 endpoint at...

include::shared:partial$saml-signature-verification.adoc[tags=okta-snippet]
```

```bash
# Source: shared/modules/ROOT/partials/sso-prereqs.adoc
# tag::okta-snippet[]
== Verify the IdP signature
WARNING: The signing certificate must be uploaded to Acme...
# end::okta-snippet[]
```

Tags slice large partials. Edit the partial once → both product manuals update.

### Recipe 3: Antora component descriptor (per-product config)

```yaml
# product-a/docs/antora.yml
name: product-a
title: Product A
version: '2.0'
nav:
  - modules/ROOT/nav.adoc
asciidoc:
  attributes:
    product-name: 'Acme Product A'
    product-version: '2.0'
```

```asciidoc
# In any topic:
Welcome to {product-name} {product-version}.
```

Attributes replace `{tokens}` at build time. One topic, two products, two outputs.

### Recipe 4: Antora multi-output (HTML site + PDF)

```bash
# Default HTML site
antora antora-playbook.yml --to-dir build/site

# Convert AsciiDoc topics to PDF for offline / customer-distributable manuals
find product-a/docs -name '*.adoc' -exec \
  asciidoctor-pdf -o build/pdf/{}.pdf {} \;
```

`asciidoctor-pdf` honors the same `include::` and attributes, so PDF and web stay in sync.

### Recipe 5: Docusaurus MDX partial component

```mdx
{/* docs/_partials/sso-prereqs.mdx */}
import Admonition from '@theme/Admonition';

<Admonition type="warning">
You must enable SCIM 2.0 in Okta before completing SSO setup.
</Admonition>

* Provision an Okta app with SAML 2.0
* Upload the Acme signing certificate
* Map `groups` claim to Acme roles
```

```mdx
{/* docs/how-to/authentication/sso-okta.mdx */}
import SsoPrereqs from '@site/docs/_partials/sso-prereqs.mdx';

# SSO with Okta

<SsoPrereqs />

## Configure the Acme side
...
```

One partial; every SSO page renders the same prereqs.

### Recipe 6: Mintlify Snippets

```mdx
{/* snippets/sso-prereqs.mdx */}
> **Warning:** You must enable SCIM 2.0 in Okta before completing SSO setup.

- Provision an Okta app with SAML 2.0
- Upload the Acme signing certificate
- Map `groups` claim to Acme roles
```

```mdx
{/* how-to/authentication/sso-okta.mdx */}
import SsoPrereqs from '/snippets/sso-prereqs.mdx';

# SSO with Okta

<SsoPrereqs />
```

Mintlify auto-resolves the `/snippets/` path. Snippets can accept props too: `<SsoPrereqs idp="okta" />`.

### Recipe 7: Astro Starlight content collections

```ts
// src/content/config.ts
import { defineCollection } from 'astro:content';
import { docsSchema } from '@astrojs/starlight/schema';

export const collections = {
  docs: defineCollection({ schema: docsSchema() }),
  partials: defineCollection({ type: 'content' }),
};
```

```mdx
{/* src/content/docs/how-to/sso-okta.mdx */}
import { getEntry } from 'astro:content';
const prereqs = await getEntry('partials', 'sso-prereqs');
const { Content } = await prereqs.render();

# SSO with Okta

<Content />
```

Astro composes the partial into the parent at build time; collection schemas validate frontmatter.

### Recipe 8: Conditional reuse (build-time attribute switch)

```asciidoc
# shared topic with product-specific paths
ifeval::["{product-name}" == "Product A"]
Run `acme-a login` to authenticate.
endif::[]
ifeval::["{product-name}" == "Product B"]
Run `acme-b auth login` to authenticate.
endif::[]
```

One topic; renders the right command for whichever product imports it.

### Recipe 9: Detect orphaned partials

```bash
# Find partials never included anywhere
find shared/modules -path '*/partials/*.adoc' | while read p; do
  name=$(basename "$p" .adoc)
  if ! grep -rq "include::shared:partial\$$name\.adoc" --include='*.adoc' .; then
    echo "ORPHAN: $p"
  fi
done
```

Run quarterly; archive orphans.

### Recipe 10: Validate include resolution before publish

```bash
# Antora --log-level=info surfaces every unresolved include::
antora antora-playbook.yml --log-level=info 2>&1 | grep -E 'unresolved|missing'

# For MDX partials, use a build-time link checker
npx lychee 'build/**/*.html' --format json | jq '.[] | select(.status >= 400)'
```

Catch broken includes in CI before they ship.

## Examples

### Example 1: Single-source SSO setup across Product A + Product B

**Goal:** One "SSO prereqs" topic; renders in both product manuals + the marketing site.

**Steps:**
1. Set up `shared-topics` repo with `modules/ROOT/partials/sso-prereqs.adoc` (Recipe 2).
2. Add `shared-topics` as an Antora content source (Recipe 1).
3. In each product's SSO page: `include::shared:partial$sso-prereqs.adoc[]`.
4. Build the site: `antora antora-playbook.yml` (Recipe 1).
5. Edit `sso-prereqs.adoc` → confirm both products show the change in the next build.

**Result:** One canonical source; two product manuals stay in sync; PDF + web outputs both updated from one edit.

### Example 2: Reusable callout box across all Docusaurus docs

**Goal:** Same "API rate limit warning" admonition in 12 places; no copy-paste.

**Steps:**
1. Create `docs/_partials/rate-limit-warning.mdx` (Recipe 5).
2. Each consumer page imports + renders it.
3. Edit the partial; verify all 12 pages now show the new wording with `npm run start`.

**Result:** 12 pages updated with one commit; reviewer only checks one diff.

### Example 3: Migrate from N copies of install instructions → Mintlify snippets

**Goal:** "Install the CLI" appears 8 times in slightly different wording.

**Steps:**
1. Identify divergence: `diff` the 8 sections.
2. Pick canonical wording; create `/snippets/install-cli.mdx` (Recipe 6).
3. Replace each of the 8 occurrences with `<InstallCli />`.
4. Run Vale + spell-check on the canonical snippet only.
5. Audit no other "Install the CLI" copies via `grep -r 'npm install -g @acme/cli'`.

**Result:** 8 → 1 source-of-truth; future edits land in one place.

## Edge cases / gotchas

- **Antora needs explicit component versions** — `version: '2.0'` in `antora.yml` is required. Use `version: 'main'` only for true evergreen content.
- **AsciiDoc `include::` is not transitive across components** — `shared:partial$x.adoc` works; `product-b:partial$x.adoc` does not by default unless `product-b` is in the same playbook.
- **MDX partial props are JSX-only** — markdown doesn't support `{props.x}` interpolation. Wrap dynamic content in a JSX expression.
- **Mintlify snippets cap at 100KB** — large reusable blocks split into multiple files.
- **Astro content collections need TypeScript** — `src/content/config.ts` only. JS not supported.
- **Don't reuse below the paragraph level** — single-source per topic / section / admonition; reusing single sentences becomes maintenance hell.
- **Search indexing of partials** — by default, partials aren't indexed standalone; only the composed page is. If a partial has unique content needed for search, also ship as a standalone page.
- **Conditional includes are powerful but easy to misuse** — keep `ifeval::` blocks to ≤3 per topic; beyond that, split topics.
- **Antora build times scale with component × version × branch** — cache the build server; multi-product playbooks routinely hit 5-15min builds.
- **Translation handoff** — Crowdin / Lokalise can ingest AsciiDoc and MDX; tag-handle partials to keep token boundaries.
- **MDX partials with React state break SSR** — partials should be pure-render only; no `useState` / `useEffect`.
- **AsciiDoc tags + sections drift** — if you tag a snippet and later restructure the partial, the tag may now wrap the wrong region. Run `asciidoctor --trace` to surface tag-resolution warnings.
- **Mixing AsciiDoc and MDX** — possible (Antora can host MDX-backed UI components), but the migration cost is real. Pick one per KB.

## Sources

- [Antora docs](https://docs.antora.org/antora/latest/)
- [Antora component versions](https://docs.antora.org/antora/latest/component-with-no-version/)
- [AsciiDoc include directive](https://docs.asciidoctor.org/asciidoc/latest/directives/include/)
- [AsciiDoc tagged regions](https://docs.asciidoctor.org/asciidoc/latest/directives/include-tagged-regions/)
- [Docusaurus MDX](https://docusaurus.io/docs/markdown-features/react)
- [Docusaurus reusable content (partials)](https://docusaurus.io/docs/markdown-features/react#mdx-component-scope)
- [Mintlify reusable snippets](https://mintlify.com/docs/reusable-snippets)
- [Astro content collections](https://docs.astro.build/en/guides/content-collections/)
- [Astro Starlight](https://starlight.astro.build/)
- [DITA-like reuse without DITA — Write the Docs](https://www.writethedocs.org/guide/writing/single-sourcing/)
