---
name: locale-routing-subdomain-subdirectory
description: Locale URL routing — subdirectory (preferred), subdomain, ccTLD trade-offs. hreflang correctness checklist. Framework-native i18n routing for Next.js / Astro / Docusaurus / VitePress / MkDocs Material. Use when the user asks "set up locale routes", "add hreflang", "subdomain vs subdirectory", or "multi-locale URL structure".
---

# Locale Routing — Subdomain / Subdirectory / ccTLD + hreflang

The SEO-preferred 2026 default is **subdirectory** (`example.com/de/`) — consolidates link equity, simpler to maintain, single domain. Subdomains lose authority. ccTLDs maximize geo-signal at the cost of operational complexity. All Next.js / Astro / Docusaurus / VitePress / MkDocs Material ship native subdirectory locale routing.

Defer deep hreflang strategy to `seo-specialist`. This skill emits correct routing + hreflang block.

## When to use

- New project — pick a routing pattern.
- Existing project needs locale URLs added.
- hreflang misconfiguration warnings in Google Search Console.
- Framework-specific setup (Next.js / Astro / Docusaurus).
- Migrating from subdomain → subdirectory.

Trigger phrases: "locale URL", "hreflang", "subdirectory", "subdomain", "ccTLD", "i18n routing", "multi-locale URLs", "locale prefix".

## Setup

Pick first:

| Pattern | When | Pros | Cons |
|---|---|---|---|
| `example.com/de/` | **Default** — SaaS, marketing, docs | Single domain SEO, simple ops | Server-side routing required |
| `de.example.com` | Independent infra per locale | Per-locale infra isolation | Link equity split, weaker geo-signal |
| `example.de` | Strong geo-signal needed | Best ccTLD ranking | Multiple registrations, complex ops |
| `?lang=de` | Never (anti-pattern) | Simplest | Google does not recognize as separate URL; bad SEO |

## Common recipes

### Recipe 1: Next.js App Router (next-intl) — subdirectory

```bash
npm i next-intl
```

```ts
// i18n/routing.ts
import { defineRouting } from 'next-intl/routing';
import { createNavigation } from 'next-intl/navigation';

export const routing = defineRouting({
  locales: ['en', 'de', 'fr', 'ja', 'ar', 'zh-Hans-CN'],
  defaultLocale: 'en',
  localePrefix: 'as-needed',           // /de/, /fr/ but / (root) for en
});

export const { Link, redirect, usePathname, useRouter } = createNavigation(routing);
```

```ts
// middleware.ts
import createMiddleware from 'next-intl/middleware';
import { routing } from './i18n/routing';

export default createMiddleware(routing);

export const config = {
  matcher: ['/((?!api|_next|.*\\..*).*)'],
};
```

```tsx
// app/[locale]/layout.tsx
import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';

export default async function LocaleLayout({ children, params: { locale } }) {
  const messages = await getMessages();
  const dir = ['ar', 'he', 'ur', 'fa'].includes(locale) ? 'rtl' : 'ltr';
  return (
    <html lang={locale} dir={dir}>
      <body>
        <NextIntlClientProvider messages={messages}>
          {children}
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
```

### Recipe 2: Astro Starlight (docs) — subdirectory

```bash
npm create astro@latest -- --template starlight
```

```js
// astro.config.mjs
import starlight from '@astrojs/starlight';

export default defineConfig({
  integrations: [
    starlight({
      title: 'Docs',
      defaultLocale: 'en',
      locales: {
        en: { label: 'English' },
        de: { label: 'Deutsch' },
        fr: { label: 'Français' },
        ja: { label: '日本語', lang: 'ja' },
        ar: { label: 'العربية', dir: 'rtl' },
      },
    }),
  ],
});
```

Files at `src/content/docs/<locale>/getting-started.md`.

### Recipe 3: Docusaurus — subdirectory

```js
// docusaurus.config.js
module.exports = {
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'de', 'fr', 'ja', 'ar'],
    localeConfigs: {
      ar: { direction: 'rtl', label: 'العربية' },
      ja: { label: '日本語' },
    },
  },
};
```

Files at `i18n/<locale>/docusaurus-plugin-content-docs/current/`.

```bash
npm run write-translations -- --locale de    # generate empty stub files
```

### Recipe 4: VitePress — subdirectory

```ts
// .vitepress/config.ts
export default defineConfig({
  locales: {
    root: { label: 'English', lang: 'en' },
    de: { label: 'Deutsch', lang: 'de', link: '/de/' },
    fr: { label: 'Français', lang: 'fr', link: '/fr/' },
  },
});
```

Files at `de/index.md`, `fr/index.md`.

### Recipe 5: MkDocs Material — subdirectory

```yaml
# mkdocs.yml
plugins:
  - i18n:
      languages:
        - locale: en
          default: true
          name: English
        - locale: de
          name: Deutsch
          link: /de/
        - locale: ja
          name: 日本語
          link: /ja/
        - locale: ar
          name: العربية
          link: /ar/
          # MkDocs auto-applies dir=rtl for ar
```

```bash
uv add mkdocs-material mkdocs-static-i18n
mkdocs serve
```

### Recipe 6: Mintlify — subdirectory

```json
// docs.json
{
  "locales": ["en", "de", "fr", "ja", "ar"],
  "defaultLocale": "en"
}
```

Files at `en/`, `de/`, etc.

### Recipe 7: hreflang block (canonical correctness)

```html
<head>
  <!-- Self-reference + every other locale in cluster + x-default -->
  <link rel="alternate" hreflang="en" href="https://example.com/" />
  <link rel="alternate" hreflang="de" href="https://example.com/de/" />
  <link rel="alternate" hreflang="fr" href="https://example.com/fr/" />
  <link rel="alternate" hreflang="ja" href="https://example.com/ja/" />
  <link rel="alternate" hreflang="ar" href="https://example.com/ar/" />
  <link rel="alternate" hreflang="x-default" href="https://example.com/" />
</head>
```

Rules:
1. **Self-reference** — every page in the cluster includes its own hreflang.
2. **Symmetric** — every page lists every other page in the cluster (Page A links B, Page B links A).
3. **Valid BCP 47 tags** — ISO 639-1 language + optional ISO 3166-1 region.
4. **x-default mandatory** — fallback for unmatched users.
5. **No mixing language-only with language-region** in same cluster.
6. **Absolute URLs** — fully-qualified, not relative.
7. **One delivery method** — `<head>` OR HTTP Link header OR XML sitemap (not multiple — duplicates confuse Google).
8. **All cluster pages return 200** — no redirects.

### Recipe 8: hreflang in Next.js (automated)

```tsx
// app/[locale]/page.tsx
export async function generateMetadata({ params }) {
  const path = `/`;   // route path
  return {
    alternates: {
      canonical: `https://example.com/${params.locale === 'en' ? '' : params.locale + '/'}${path}`,
      languages: {
        en: `https://example.com${path}`,
        de: `https://example.com/de${path}`,
        fr: `https://example.com/fr${path}`,
        ja: `https://example.com/ja${path}`,
        ar: `https://example.com/ar${path}`,
        'x-default': `https://example.com${path}`,
      },
    },
  };
}
```

### Recipe 9: hreflang in XML sitemap

```xml
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://example.com/</loc>
    <xhtml:link rel="alternate" hreflang="en" href="https://example.com/" />
    <xhtml:link rel="alternate" hreflang="de" href="https://example.com/de/" />
    <xhtml:link rel="alternate" hreflang="x-default" href="https://example.com/" />
  </url>
  <url>
    <loc>https://example.com/de/</loc>
    <xhtml:link rel="alternate" hreflang="en" href="https://example.com/" />
    <xhtml:link rel="alternate" hreflang="de" href="https://example.com/de/" />
    <xhtml:link rel="alternate" hreflang="x-default" href="https://example.com/" />
  </url>
</urlset>
```

### Recipe 10: hreflang via HTTP Link header (for non-HTML resources)

```
HTTP/1.1 200 OK
Content-Type: application/pdf
Link: <https://example.com/whitepaper-en.pdf>; rel="alternate"; hreflang="en",
      <https://example.com/whitepaper-de.pdf>; rel="alternate"; hreflang="de",
      <https://example.com/whitepaper.pdf>; rel="alternate"; hreflang="x-default"
```

### Recipe 11: hreflang validator

```bash
# hreflang-validator (CLI)
npm i -g hreflang-validator
hreflang-validator https://example.com/

# Or use online validators:
# - https://www.aleydasolis.com/english/international-seo-tools/hreflang-tags-generator/
# - https://technicalseo.com/tools/hreflang/

# Or via Google Search Console — Reports → International Targeting → hreflang issues
```

### Recipe 12: Subdomain pattern (when chosen)

```
Cloudflare / DNS:
  de.example.com → CNAME → example-de.cdn.com
  fr.example.com → CNAME → example-fr.cdn.com
```

```nginx
# nginx
server {
  server_name de.example.com;
  root /var/www/de;
}
server {
  server_name fr.example.com;
  root /var/www/fr;
}
```

### Recipe 13: Migration from subdomain → subdirectory

```nginx
# 301 redirect old subdomain to new subdirectory
server {
  server_name de.example.com;
  return 301 https://example.com/de$request_uri;
}
```

Track in Search Console — expect 4-8 weeks for re-indexing.

### Recipe 14: Locale detection + redirect (first-visit)

```ts
// middleware.ts (Next.js)
import { NextResponse } from 'next/server';
import { match } from '@formatjs/intl-localematcher';
import Negotiator from 'negotiator';

const LOCALES = ['en', 'de', 'fr', 'ja', 'ar'];
const DEFAULT = 'en';

function getLocale(request) {
  const headers = { 'accept-language': request.headers.get('accept-language') };
  const negotiator = new Negotiator({ headers });
  const accepted = negotiator.languages();
  return match(accepted, LOCALES, DEFAULT);
}

export function middleware(request) {
  const pathname = request.nextUrl.pathname;
  const hasLocale = LOCALES.some(l => pathname.startsWith(`/${l}/`) || pathname === `/${l}`);
  if (hasLocale) return NextResponse.next();
  const locale = getLocale(request);
  request.nextUrl.pathname = `/${locale}${pathname}`;
  return NextResponse.redirect(request.nextUrl);
}
```

Use **302 (temporary)** for locale detection so Google doesn't index the redirect as canonical.

## Examples

### Example 1: Add 5 locales to existing Next.js App Router

**Goal:** Single-locale Next.js site → 6-locale site with hreflang.

**Steps:**
1. `npm i next-intl`.
2. Move all routes from `app/` to `app/[locale]/` (Recipe 1).
3. Add `i18n/routing.ts` + `middleware.ts`.
4. Add `app/[locale]/layout.tsx` with `<html lang={locale} dir={dir}>`.
5. Add `generateMetadata` for hreflang (Recipe 8).
6. Add `next-sitemap` for XML sitemap with hreflang (Recipe 9).
7. Deploy; verify in Search Console → International Targeting.

**Result:** 6 locale URLs, valid hreflang, no SEO penalty.

### Example 2: Fix hreflang errors in Search Console

**Goal:** Search Console reports "hreflang tags missing return tags" on 1.2k URLs.

**Steps:**
1. Pull list of affected URLs from Search Console.
2. Spot-check first 10 — confirm Page A links B but Page B doesn't link A (asymmetric).
3. Audit the source of hreflang generation — likely a template missing the `en` self-reference.
4. Fix template (Recipe 7) — add all locales + x-default + self-reference.
5. Deploy; resubmit sitemap; wait 1-2 weeks for re-crawl.
6. Search Console clears the error.

**Result:** hreflang cluster intact; international rankings stabilize.

## Edge cases / gotchas

- **hreflang ≠ canonical** — hreflang signals locale alternates; canonical signals duplicate-content preference. Don't conflate.
- **Self-canonical to locale URL** — each locale page's `<link rel="canonical">` should self-reference (not point to `en` version).
- **Subdirectory vs locale-prefix `as-needed`** — `next-intl` `as-needed` keeps `en` at root (`/`) and prefixes others (`/de/`). Cleaner UX but breaks pure URL symmetry; document choice.
- **Region without language** — `en-US` and `en-GB` are valid; `US` alone is not (need lang).
- **Country code != language code** — `ja-JP` is fine; `jp` alone is not a language. Don't use `ar-AE` if same content as `ar`.
- **Search Console hreflang errors auto-clear in 14-28 days** after fix; don't panic.
- **Multiple delivery methods conflict** — `<head>` hreflang + sitemap hreflang of same URL = Google takes most recently crawled. Pick one.
- **Subdomain + ccTLD mixing** — `de.example.com` + `example.de` both pointing to DE content = duplicate content, hreflang can't fix; pick one.
- **Geo-targeting (Search Console) overrides hreflang** — if `example.com/de/` is geo-targeted to Germany in Search Console + hreflang says `de` (language-only), Search Console wins for Germany rankings.
- **Lazy-loaded hreflang via JS** — Google may not see JS-injected hreflang reliably; emit server-side.
- **Pseudo-locale in routing** — `ach` should not be indexed; add `Disallow: /ach/` to robots.txt + remove from hreflang block.
- **Region variants in TMS but not URL** — e.g., `es-MX` translation but URL is `/es/`; verify Search Console geo-targeting reflects intent.
- **301 vs 302 for locale detection** — initial accept-language redirect = 302 (temporary). Permanent route changes = 301.

## Sources

- Google managing multi-regional sites: https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites
- i18n SEO hreflang guide: https://better-i18n.com/en/blog/i18n-seo-hreflang-locale-urls-guide/
- next-intl docs: https://next-intl.dev/
- Astro Starlight i18n: https://starlight.astro.build/guides/i18n/
- Docusaurus i18n: https://docusaurus.io/docs/i18n/introduction
- VitePress i18n: https://vitepress.dev/guide/i18n
- MkDocs static-i18n: https://github.com/ultrabug/mkdocs-static-i18n
- hreflang validator: https://technicalseo.com/tools/hreflang/
- Mintlify i18n: https://mintlify.com/docs/settings/localization
- @formatjs/intl-localematcher: https://formatjs.io/docs/polyfills/intl-localematcher/
