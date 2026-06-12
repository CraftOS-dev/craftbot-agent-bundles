<!--
Source: https://next-intl-docs.vercel.app/ · https://inlang.com/m/gerre34r/library-inlang-paraglideJs
Authored: June 2026 for the frontend-engineer agent bundle.
-->

# i18n — next-intl + Paraglide JS

Two leading i18n approaches in 2026: **next-intl** (locale routing + RSC-safe,
the default for Next 15) and **Paraglide JS** (Inlang, tree-shakeable + type-
safe, ~5kb runtime, smallest bundle). FormatJS / react-intl remain valid for
ICU compliance.

## When to use

- Next 15 app needs locale routing + RSC-safe translations → **next-intl**
- Bundle-critical app needs i18n → **Paraglide JS** (tree-shakeable)
- Astro / SvelteKit / Vue site → Paraglide or framework-native plugin
- ICU MessageFormat compliance required (plural, gender) → **next-intl** /
  **react-intl**
- Trigger phrases: "i18n", "translation", "locale", "next-intl", "Paraglide",
  "ICU", "react-intl", "FormatJS", "rtl"

## Setup — next-intl (Next 15)

```bash
pnpm add next-intl
```

```ts
// next.config.ts
import type { NextConfig } from "next";
import createNextIntlPlugin from "next-intl/plugin";

const withNextIntl = createNextIntlPlugin();

const config: NextConfig = {};
export default withNextIntl(config);
```

```ts
// src/i18n/routing.ts
import { defineRouting } from "next-intl/routing";

export const routing = defineRouting({
  locales: ["en", "ja", "fr", "de"],
  defaultLocale: "en",
  localePrefix: "as-needed",      // / for default, /ja for others
});
```

```ts
// src/i18n/request.ts
import { getRequestConfig } from "next-intl/server";
import { routing } from "./routing";

export default getRequestConfig(async ({ requestLocale }) => {
  let locale = await requestLocale;
  if (!locale || !routing.locales.includes(locale as any)) locale = routing.defaultLocale;
  return { locale, messages: (await import(`../../messages/${locale}.json`)).default };
});
```

```ts
// src/middleware.ts
import createMiddleware from "next-intl/middleware";
import { routing } from "./i18n/routing";

export default createMiddleware(routing);

export const config = { matcher: ["/((?!api|_next|.*\\..*).*)"] };
```

## Setup — Paraglide JS

```bash
pnpm dlx @inlang/paraglide-next@latest init
# Detects framework, sets up:
#   - inlang/project.inlang/
#   - messages/en.json, messages/ja.json
#   - paraglide.config.js
#   - .gitignore additions
```

Verify: `pnpm list @inlang/paraglide-next`.

No API keys.

## Common recipes — next-intl

### Recipe 1 — Translation file (ICU MessageFormat)

```jsonc
// messages/en.json
{
  "Home": {
    "title": "Welcome to {appName}",
    "subtitle": "The fastest way to ship.",
    "cta": "Get started"
  },
  "Cart": {
    "summary": "{count, plural, =0 {Cart is empty} one {1 item} other {# items}}",
    "checkout": "Checkout"
  }
}
```

```jsonc
// messages/ja.json
{
  "Home": {
    "title": "{appName} へようこそ",
    "subtitle": "最速で出荷する方法。",
    "cta": "始める"
  },
  "Cart": {
    "summary": "{count, plural, =0 {カートは空です} other {# 個のアイテム}}",
    "checkout": "チェックアウト"
  }
}
```

### Recipe 2 — Use in a Server Component

```tsx
// app/[locale]/page.tsx
import { getTranslations } from "next-intl/server";
import { Link } from "@/i18n/navigation";

export default async function HomePage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "Home" });

  return (
    <main>
      <h1>{t("title", { appName: "Acme" })}</h1>
      <p>{t("subtitle")}</p>
      <Link href="/start">{t("cta")}</Link>
    </main>
  );
}
```

### Recipe 3 — Use in a Client Component

```tsx
"use client";
import { useTranslations } from "next-intl";

export function Cart({ count }: { count: number }) {
  const t = useTranslations("Cart");
  return (
    <div>
      <p>{t("summary", { count })}</p>
      <button>{t("checkout")}</button>
    </div>
  );
}
```

### Recipe 4 — Locale-aware navigation

```ts
// src/i18n/navigation.ts
import { createNavigation } from "next-intl/navigation";
import { routing } from "./routing";

export const { Link, redirect, usePathname, useRouter } = createNavigation(routing);
```

```tsx
import { Link } from "@/i18n/navigation";

<Link href="/about">About</Link>            // resolves to /ja/about for Japanese
<Link href="/about" locale="fr">À propos</Link>
```

### Recipe 5 — Date / number / currency formatters

```tsx
import { useFormatter } from "next-intl";

function PriceTag({ price, date }: { price: number; date: Date }) {
  const f = useFormatter();
  return (
    <>
      <p>{f.number(price, { style: "currency", currency: "JPY" })}</p>
      <p>{f.dateTime(date, { dateStyle: "long" })}</p>
      <p>{f.relativeTime(date)}</p>
    </>
  );
}
```

### Recipe 6 — Language switcher

```tsx
"use client";
import { useLocale } from "next-intl";
import { useRouter, usePathname } from "@/i18n/navigation";

export function LanguageSwitcher() {
  const locale = useLocale();
  const router = useRouter();
  const pathname = usePathname();

  return (
    <select
      value={locale}
      onChange={(e) => router.replace(pathname, { locale: e.target.value })}
      aria-label="Choose language"
    >
      <option value="en">English</option>
      <option value="ja">日本語</option>
      <option value="fr">Français</option>
    </select>
  );
}
```

### Recipe 7 — `app/[locale]/layout.tsx`

```tsx
import { NextIntlClientProvider } from "next-intl";
import { getMessages } from "next-intl/server";
import { notFound } from "next/navigation";
import { routing } from "@/i18n/routing";

export function generateStaticParams() {
  return routing.locales.map((locale) => ({ locale }));
}

export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!routing.locales.includes(locale as any)) notFound();

  const messages = await getMessages();

  return (
    <html lang={locale} dir={locale === "ar" ? "rtl" : "ltr"}>
      <body>
        <NextIntlClientProvider messages={messages}>{children}</NextIntlClientProvider>
      </body>
    </html>
  );
}
```

## Common recipes — Paraglide JS

### Recipe 8 — Translation file (Paraglide JSON)

```jsonc
// messages/en.json
{
  "$schema": "https://inlang.com/schema/inlang-message-format",
  "hello_world": "Hello, world!",
  "greeting": "Hello, {name}!"
}
```

```jsonc
// messages/ja.json
{
  "$schema": "https://inlang.com/schema/inlang-message-format",
  "hello_world": "こんにちは、世界！",
  "greeting": "こんにちは、{name}さん！"
}
```

After editing, run `pnpm exec paraglide-next compile` (or wait for the watcher).

### Recipe 9 — Use Paraglide messages

```tsx
import * as m from "@/paraglide/messages";

export default function Page() {
  return <h1>{m.hello_world()}</h1>;
}
```

Each message is its own tree-shakeable function. Unused messages drop out of
the bundle.

```tsx
<p>{m.greeting({ name: "Ada" })}</p>
```

### Recipe 10 — Paraglide language switch

```tsx
"use client";
import { setLanguageTag, languageTag } from "@/paraglide/runtime";

export function Switcher() {
  return (
    <button onClick={() => setLanguageTag(languageTag() === "en" ? "ja" : "en")}>
      Switch
    </button>
  );
}
```

## Common recipes — translation workflow

### Recipe 11 — Auto-translate with DeepL (via deepl-mcp)

```ts
// scripts/translate.ts
import { readFileSync, writeFileSync } from "node:fs";

const SOURCE = "messages/en.json";
const TARGETS = ["ja", "fr", "de"];
const en = JSON.parse(readFileSync(SOURCE, "utf8"));

for (const lang of TARGETS) {
  const out: Record<string, string> = {};
  for (const [key, text] of Object.entries(en)) {
    if (typeof text !== "string") continue;
    const res = await fetch("https://api-free.deepl.com/v2/translate", {
      method: "POST",
      headers: {
        "Authorization": `DeepL-Auth-Key ${process.env.DEEPL_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: [text], target_lang: lang.toUpperCase() }),
    }).then((r) => r.json());
    out[key] = res.translations[0].text;
  }
  writeFileSync(`messages/${lang}.json`, JSON.stringify(out, null, 2));
}
```

Or use the CraftBot `deepl-mcp` for the same flow without writing the script.

### Recipe 12 — Test i18n with Playwright

```ts
test("Japanese homepage", async ({ page }) => {
  await page.goto("/ja");
  await expect(page).toHaveTitle(/へようこそ/);
  await expect(page.getByRole("button", { name: "始める" })).toBeVisible();
});
```

## Examples

### Example 1: Add i18n to an existing Next 15 app

```bash
pnpm add next-intl
mkdir -p src/i18n messages
# Create routing.ts + request.ts + middleware.ts (Recipes above)
# Move app/* to app/[locale]/*
# Add messages/en.json (Recipe 1)
pnpm dev
# Visit /ja/about for Japanese routing
```

### Example 2: Bundle-critical SPA → Paraglide

```bash
pnpm dlx @inlang/paraglide-next@latest init   # works for SPA via vite plugin too
# Use m.message_name() in components (Recipe 9)
pnpm build
# Inspect bundle — only used messages are included
```

## Edge cases / gotchas

- **Server Components can't access `useTranslations`** — use `getTranslations`
  from `next-intl/server`.
- **`useTranslations` requires `NextIntlClientProvider`** in a parent client
  layout — wrap once at the root.
- **Locale prefix `"as-needed"` vs `"always"`** — `"always"` puts every locale
  in the URL (`/en/about`); `"as-needed"` keeps the default at the root.
- **ICU plural categories** vary by language (e.g., Arabic has 6). Test with
  real locales, not just `=0` / `=1` / `other`.
- **RTL languages** need `dir="rtl"` on `<html>` (or scoped). Tailwind 4 has
  built-in RTL utilities (`rtl:` modifier).
- **Date formats** are locale-dependent — `Intl.DateTimeFormat` handles it.
- **Paraglide compile-step** must run before `next dev` / `next build` —
  add `paraglide-next compile` to the build script.
- **Paraglide messages are typed** — typos at call sites cause TS errors.
- **Don't store untranslated strings in code** — even one missed string ruins
  the UX for non-default users. Use Knip-style audit (`pnpm exec inlang
  machine translate`) to find gaps.
- **Translation memory / glossary** — for serious projects, use Crowdin /
  Lokalise (paid) instead of raw JSON files; they keep context per key.
- **SEO** — `<link rel="alternate" hreflang="ja" href="/ja" />` for every
  locale + `<link rel="canonical">`. next-intl emits these automatically when
  `routing.localePrefix === "always"`.

## Sources

- [next-intl docs](https://next-intl-docs.vercel.app/)
- [Paraglide JS docs](https://inlang.com/m/gerre34r/library-inlang-paraglideJs)
- [ICU MessageFormat](https://unicode-org.github.io/icu/userguide/format_parse/messages/)
- [FormatJS](https://formatjs.io/) — react-intl docs
- [DeepL API](https://www.deepl.com/docs-api)
- [Crowdin](https://crowdin.com/) — translation management
- [Lokalise](https://lokalise.com/) — translation management alt
- [Next.js i18n routing](https://nextjs.org/docs/app/building-your-application/routing/internationalization)
- [Inlang ecosystem](https://inlang.com/) — Paraglide author's other tools
