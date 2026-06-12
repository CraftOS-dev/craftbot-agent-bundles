---
name: in-app-message-i18next-react-intl
description: In-app i18n libraries — i18next (largest ecosystem), react-intl (strict ICU), next-intl (Next.js native), paraglide-js (compiler-based, type-safe). Setup, message format, integration with TMS. Use when the user asks "set up i18n in React/Next.js/Astro/Svelte", "pick i18n library", or "type-safe translations".
---

# In-App Message Localization — i18next / react-intl / next-intl / paraglide-js

Pick by stack:
- **react-i18next** — largest React ecosystem (3.5M+ weekly DLs); plugin-rich.
- **react-intl (FormatJS)** — strict ICU compliance; smallest bundle.
- **next-intl** — Next.js App Router native; server rendering.
- **paraglide-js (inlang)** — compiler-based, type-safe, 70% smaller bundle (47KB vs 205KB i18next).

## When to use

- Adding i18n to React / Next.js / Vue / Svelte / Astro / RN.
- Picking between libraries for new project.
- Migrating from one library to another.
- Reducing i18n bundle size.
- Need type-safe message calls.

Trigger phrases: "set up i18n", "react-i18next", "react-intl", "next-intl", "paraglide", "i18n library", "type-safe translations", "i18n bundle size".

## Setup

```bash
# i18next
npm i i18next react-i18next i18next-icu i18next-browser-languagedetector
npm i i18next-http-backend                # for HTTP backend

# react-intl (FormatJS)
npm i react-intl @formatjs/cli

# next-intl
npm i next-intl

# paraglide-js (Svelte / Astro / React)
npx @inlang/paraglide-js@latest init

# LinguiJS (alternative — macro-based)
npm i @lingui/core @lingui/macro
```

Auth/env: none required.

## Library selection matrix

| Stack | Recommend | Why |
|---|---|---|
| Next.js App Router | next-intl | Server-side rendering + route-based locales native |
| React (Vite / CRA / generic) | react-intl OR react-i18next | ICU strictness vs ecosystem |
| React + bundle critical | paraglide-js | 47KB vs 205KB i18next |
| Vue 3 | vue-i18n v9 | Framework standard; ICU |
| Svelte / SvelteKit | paraglide-js | Type-safe, compiler-based |
| Astro | paraglide-js + Astro i18n | Islands-friendly |
| Angular | $localize | Framework standard |
| React Native | i18next + react-native-localize | Crowdin RN OTA SDK |

## Common recipes

### Recipe 1: react-i18next bootstrap

```ts
// src/i18n/config.ts
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import HttpBackend from 'i18next-http-backend';
import ICU from 'i18next-icu';

i18n
  .use(ICU)
  .use(HttpBackend)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    fallbackLng: 'en',
    supportedLngs: ['en', 'de', 'fr', 'ja', 'ar'],
    backend: { loadPath: '/locales/{{lng}}.json' },
    detection: {
      order: ['querystring', 'cookie', 'localStorage', 'navigator'],
      caches: ['cookie'],
    },
    interpolation: { escapeValue: false },
  });

export default i18n;
```

```tsx
// usage
import { useTranslation, Trans } from 'react-i18next';

const { t, i18n } = useTranslation();
t('cart.items', { count: 3 });

// Rich text
<Trans i18nKey="welcome">Hello <strong>{{name}}</strong>!</Trans>
```

### Recipe 2: react-intl bootstrap

```tsx
// src/i18n/Provider.tsx
import { IntlProvider } from 'react-intl';

const messages = {
  en: { 'cart.items': '{count, plural, =0 {No items} one {# item} other {# items}}' },
  de: { 'cart.items': '{count, plural, =0 {Keine Artikel} one {# Artikel} other {# Artikel}}' },
};

export function I18nProvider({ children, locale }) {
  return (
    <IntlProvider locale={locale} messages={messages[locale]} defaultLocale="en">
      {children}
    </IntlProvider>
  );
}
```

```tsx
// usage
import { FormattedMessage, useIntl } from 'react-intl';

<FormattedMessage
  id="cart.items"
  defaultMessage="{count, plural, =0 {No items} one {# item} other {# items}}"
  values={{ count }}
/>

const intl = useIntl();
intl.formatNumber(amount, { style: 'currency', currency: 'EUR' });
```

### Recipe 3: react-intl extraction + compile (FormatJS CLI)

```bash
# Extract messages from source
formatjs extract 'src/**/*.{ts,tsx}' --out-file lang/en.json \
  --id-interpolation-pattern '[sha512:contenthash:base64:6]'

# Lint for ICU correctness
formatjs lint 'lang/**/*.json'

# Compile to AST (faster runtime)
formatjs compile lang/de.json --ast --out-file lang/compiled/de.json
```

### Recipe 4: next-intl App Router setup

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
  localePrefix: 'as-needed',
});

export const { Link, redirect, usePathname, useRouter } = createNavigation(routing);
```

```ts
// middleware.ts
import createMiddleware from 'next-intl/middleware';
import { routing } from './i18n/routing';
export default createMiddleware(routing);
export const config = { matcher: ['/((?!api|_next|.*\\..*).*)'] };
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
        <NextIntlClientProvider messages={messages}>{children}</NextIntlClientProvider>
      </body>
    </html>
  );
}
```

```tsx
// page.tsx (client)
import { useTranslations } from 'next-intl';
const t = useTranslations('Cart');
t('items', { count: 3 });

// server component
import { getTranslations } from 'next-intl/server';
const t = await getTranslations('Cart');
t('items', { count: 3 });
```

### Recipe 5: paraglide-js setup

```bash
npx @inlang/paraglide-js@latest init --languageTags en,de,fr,ja,ar
```

```
project.inlang/settings.json      # language list + plugin config
messages/en.json                  # source
messages/de.json                  # target
src/paraglide/                    # auto-generated compiled output
```

```bash
# Compile (rerun on message changes)
npx @inlang/paraglide-js@latest compile
```

```ts
// usage — type-checked function calls!
import * as m from '$lib/paraglide/messages';
import { setLanguageTag } from '$lib/paraglide/runtime';

setLanguageTag('de');
m.hello_world({ name: 'Welt' });       // type-checked!
m.cart_items({ count: 3 });
```

### Recipe 6: paraglide-js + ICU MessageFormat plugin

```bash
npm i @inlang/paraglide-js-adapter-message-format
```

```json
// messages/en.json
{
  "cart_items": "{count, plural, =0 {No items} one {# item} other {# items}}"
}
```

```ts
m.cart_items({ count: 0 });    // "No items" — ICU resolved at compile time
```

### Recipe 7: paraglide-js + Vite plugin

```ts
// vite.config.ts
import { paraglide } from '@inlang/paraglide-js-adapter-vite';

export default defineConfig({
  plugins: [
    paraglide({ project: './project.inlang', outdir: './src/paraglide' }),
  ],
});
```

Auto-recompile on save; no manual `npx paraglide-js compile`.

### Recipe 8: LinguiJS (macro-based, type-safe)

```tsx
import { Trans, t } from '@lingui/macro';

<Trans>Hello world</Trans>
<Trans>You have {count} items</Trans>      // macro adds id + plural

t`Submit`                                   // inline string
```

Compile:
```bash
lingui extract                              # extract messages
lingui compile                              # compile catalogs
```

### Recipe 9: vue-i18n v9 (Vue 3)

```ts
import { createI18n } from 'vue-i18n';

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  messages: {
    en: { 'cart.items': '{count, plural, =0 {No items} one {# item} other {# items}}' },
  },
});

app.use(i18n);
```

```vue
<template>
  <p>{{ t('cart.items', { count: 3 }) }}</p>
</template>

<script setup>
const { t, locale } = useI18n();
</script>
```

### Recipe 10: Angular $localize

```bash
ng add @angular/localize
```

```html
<!-- in template -->
<p i18n="@@cart.items">You have {count, plural, =0 {no items} one {1 item} other {{{count}} items}}</p>
```

```bash
ng extract-i18n --output-path src/locale/
# Translate src/locale/messages.de.xlf
ng build --localize
```

### Recipe 11: React Native with Crowdin OTA

```bash
npm i i18next react-i18next i18next-react-native-language-detector
npm i @crowdin/ota-client
```

```ts
import OtaClient from '@crowdin/ota-client';
import i18n from 'i18next';

const ota = new OtaClient('your-distribution-hash');
const translations = await ota.getStringsByLocale('de');
i18n.addResourceBundle('de', 'translation', translations, true, true);
```

Strings update without app-store resubmit.

### Recipe 12: Lazy-load locales (any library)

```ts
// i18next
i18n.use(HttpBackend).init({
  backend: { loadPath: '/locales/{{lng}}.json' },
});
// Loads /locales/de.json only when user switches to de

// react-intl
const messages = await fetch(`/locales/${locale}.json`).then(r => r.json());
```

### Recipe 13: Bundle size optimization

```bash
# react-intl + AST compilation = smallest
formatjs compile lang/de.json --ast --out-file lang/compiled/de.json
# Then bundle compiled instead of raw

# paraglide-js = ~47KB total (vs 205KB i18next)
# Compiler tree-shakes unused messages

# Lingui = small (~20KB runtime)
```

### Recipe 14: Locale-specific code splitting

```tsx
// Next.js — per-locale message bundle
import { unstable_setRequestLocale } from 'next-intl/server';

export function generateStaticParams() {
  return [{ locale: 'en' }, { locale: 'de' }, { locale: 'fr' }];
}

export default async function Layout({ params: { locale } }) {
  unstable_setRequestLocale(locale);
  // ...
}
```

### Recipe 15: TMS integration (Crowdin / Lokalise / Phrase)

```yaml
# crowdin.yml
files:
  - source: locales/en.json                    # source
    translation: locales/%two_letters_code%.json  # target

# i18next reads /locales/{{lng}}.json — drop-in compatible
```

```bash
crowdin upload sources && crowdin download
# After download, run paraglide-js compile / formatjs compile / etc.
```

### Recipe 16: Locale switcher component

```tsx
import { useRouter, useLocale } from 'next-intl';

const LOCALES = [
  { code: 'en', label: 'English', flag: '🇺🇸' },
  { code: 'de', label: 'Deutsch', flag: '🇩🇪' },
  { code: 'ja', label: '日本語', flag: '🇯🇵' },
  { code: 'ar', label: 'العربية', flag: '🇸🇦' },
];

export function LocaleSwitcher() {
  const router = useRouter();
  const locale = useLocale();
  return (
    <select value={locale} onChange={e => router.push(window.location.pathname, { locale: e.target.value })}>
      {LOCALES.map(l => <option key={l.code} value={l.code}>{l.flag} {l.label}</option>)}
    </select>
  );
}
```

## Examples

### Example 1: New Next.js App Router project with next-intl + ICU

**Goal:** Greenfield Next.js 14 app with 6 locales, type-safe messages, server rendering.

**Steps:**
1. `npm i next-intl`
2. Add `i18n/routing.ts`, `middleware.ts`, `app/[locale]/layout.tsx` (Recipe 4).
3. Create `messages/en.json` with ICU plurals.
4. Add Crowdin sync (Recipe 15) — translators populate `de.json`, `fr.json`, etc.
5. Add hreflang metadata (see `locale-routing-subdomain-subdirectory` skill).
6. Deploy. Routes: `/en/`, `/de/`, `/fr/`, etc.

**Result:** Server-rendered, SEO-optimized multi-locale app; type-safe via `useTranslations`.

### Example 2: Migrate React app from i18next to paraglide-js for 70% bundle reduction

**Goal:** React + Vite app currently 205KB+ on i18next; reduce to <60KB i18n footprint.

**Steps:**
1. Audit current bundle: i18next + plugins = 205KB gzipped.
2. Init paraglide: `npx @inlang/paraglide-js@latest init --languageTags en,de,fr,ja,ar`.
3. Move messages from i18next JSON shape (nested) → paraglide flat shape.
4. Replace `t('cart.items', { count })` → `m.cart_items({ count })`.
5. Codemod with regex or hand-edit per call site.
6. Remove i18next + react-i18next from deps.
7. Verify bundle: 47KB total for i18n surface.
8. Type-check fails reveal stale message calls — fix.

**Result:** Bundle down 160KB; type-safe calls; build time faster.

## Edge cases / gotchas

- **i18next + ICU plugin order matters** — `.use(ICU)` before `.use(initReactI18next)`.
- **next-intl client/server separation** — `useTranslations` (client) vs `getTranslations` (server). Don't mix.
- **react-intl `defaultMessage`** — required for extraction; without it, extraction produces empty source.
- **paraglide message keys** — snake_case enforced; reformat existing camelCase keys.
- **Trans component children** — `<Trans>` in react-i18next requires placeholders, not interpolation. `<Trans i18nKey="welcome" values={{name}}>Hello {{name}}</Trans>`.
- **ICU in nested JSON** — i18next supports both flat and nested; ICU plural keys must be flat (`cart.items.{count, ...}` not nested object).
- **vue-i18n composition API** — `useI18n` requires `legacy: false` in createI18n.
- **Angular $localize requires build step** — `ng build --localize` produces N builds (one per locale); affects deployment.
- **React Native locale detection** — `react-native-localize` returns `de-DE` even when user has just `de`; map to your locale list.
- **paraglide message IDs are functions** — no string lookup; can't dynamically construct key name. For dynamic, use string-key fallback.
- **Code splitting + locale switch** — switching locale must re-import the new messages chunk; some libraries (paraglide) compile per locale.
- **Locale detection cookie + SSR mismatch** — Next.js requires Accept-Language header read on server; client cookie post-hydrate; sync.
- **Pluralization fallback** — if locale has 4 forms (RU) but only `one`/`other` defined, RU users see English. Lint catches.
- **Missing translation behavior** — i18next: returns key. react-intl: returns defaultMessage. next-intl: throws in dev / returns key in prod.
- **Production bundling** — never ship raw catalogs; compile (FormatJS AST, paraglide TS) for runtime.
- **HOT module replace** — paraglide-js needs Vite plugin reload; without, stale messages persist.

## Sources

- i18next: https://www.i18next.com/
- react-i18next: https://react.i18next.com/
- react-intl (FormatJS): https://formatjs.io/docs/react-intl/
- FormatJS CLI: https://formatjs.io/docs/tooling/cli
- next-intl: https://next-intl.dev/
- paraglide-js: https://github.com/opral/paraglide-js
- LinguiJS: https://lingui.dev/
- vue-i18n: https://vue-i18n.intlify.dev/
- Angular $localize: https://angular.io/guide/i18n-overview
- React Native localization: https://github.com/zoontek/react-native-localize
- i18n libraries 2026 comparison: https://gundogmuseray.medium.com/the-definitive-guide-to-i18n-libraries-for-next-js-react-in-2026-8102c7f68a77
- react-i18n 2026 selector: https://www.auto18n.com/en/blog/react-i18n-2026
- Crowdin React Native OTA: https://github.com/crowdin/ota-client-js
