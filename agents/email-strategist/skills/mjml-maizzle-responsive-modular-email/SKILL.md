<!--
Source: https://mjml.io/ + https://maizzle.com/
MJML — responsive abstraction. Maizzle — Tailwind utility-first.
Compile to cross-client HTML. Push to Klaviyo / Customer.io via API.
-->
# MJML / Maizzle Responsive Modular Email — SKILL

MJML (responsive abstraction) and Maizzle (Tailwind utility-first) compile email source to cross-client HTML. Solves Outlook Word-renderer quirks, Gmail clipping, ProtonMail strict CSP, and dark mode handling. Pipe compiled HTML to Klaviyo / Customer.io / Resend / Postmark via their template APIs.

## When to use

- "Build responsive cross-client email templates"
- "Migrate hand-coded HTML emails to a modern framework"
- "Set up MJML compile pipeline + push to ESP"
- "Tailwind workflow for email" → Maizzle
- "Mobile-first email design"
- "Component-reused email library"

## Setup

```bash
# MJML
npm i -g mjml                  # CLI
# OR per-project
npm i mjml --save-dev

# Maizzle
npm i -g @maizzle/cli           # CLI
maizzle new welcome-emails      # scaffold a project
cd welcome-emails && npm i
```

Inline tools:

```bash
# CSS inliner (sometimes needed before final ESP push)
npm i -g juice

# HTML minifier
npm i -g html-minifier-terser
```

## Common recipes

### Recipe 1: MJML hello-world

```xml
<!-- welcome.mjml -->
<mjml>
  <mj-head>
    <mj-title>Welcome to Brand</mj-title>
    <mj-preview>We are glad you are here.</mj-preview>
    <mj-attributes>
      <mj-all font-family="Helvetica, Arial, sans-serif" />
      <mj-text font-size="16px" color="#333333" line-height="1.5" />
      <mj-button background-color="#0066ff" color="white" border-radius="6px" />
    </mj-attributes>
    <mj-style>
      @media (prefers-color-scheme: dark) {
        .bg { background-color: #111 !important; }
        .text { color: #fff !important; }
      }
    </mj-style>
  </mj-head>
  <mj-body width="600px" background-color="#f4f4f4">
    <mj-section background-color="#ffffff" css-class="bg">
      <mj-column>
        <mj-image src="https://cdn.brand.com/logo.png" alt="Brand" width="120px" align="center" />
        <mj-text align="center" font-size="24px" css-class="text">
          Welcome to Brand!
        </mj-text>
        <mj-text css-class="text">
          Here is what to expect over the next 14 days:
        </mj-text>
        <mj-text css-class="text">
          - Day 1: Your starter guide<br/>
          - Day 3: Three quick wins<br/>
          - Day 7: Power-user tips<br/>
          - Day 14: A special invitation
        </mj-text>
        <mj-button href="https://brand.com/start" align="center">
          Get started
        </mj-button>
      </mj-column>
    </mj-section>
    <mj-section background-color="#f4f4f4">
      <mj-column>
        <mj-text align="center" font-size="12px" color="#888">
          Brand Inc, 123 Main St, City, State 12345<br/>
          <a href="{% unsubscribe %}">Unsubscribe</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
```

Compile:

```bash
npx mjml welcome.mjml -o welcome.html

# With minification + skip comments
npx mjml welcome.mjml -o welcome.html --config.minify true --config.beautify false
```

### Recipe 2: MJML — modular components

```xml
<!-- components/header.mjml -->
<mj-section background-color="#fff">
  <mj-column>
    <mj-image src="https://cdn.brand.com/logo.png" alt="Brand" width="120px" />
  </mj-column>
</mj-section>

<!-- components/footer.mjml -->
<mj-section background-color="#f4f4f4">
  <mj-column>
    <mj-text align="center" font-size="12px" color="#888">
      Brand Inc, 123 Main St<br/>
      <a href="{% unsubscribe %}">Unsubscribe</a>
    </mj-text>
  </mj-column>
</mj-section>

<!-- welcome.mjml uses includes -->
<mjml>
  <mj-body>
    <mj-include path="./components/header.mjml" />
    <!-- body content -->
    <mj-include path="./components/footer.mjml" />
  </mj-body>
</mjml>
```

### Recipe 3: Maizzle Tailwind-style template

```html
<!-- src/templates/welcome.html -->
---
title: Welcome to Brand
preheader: We are glad you are here.
---

<x-main>
  <table class="font-sans w-full" cellpadding="0" cellspacing="0">
    <tr>
      <td align="center" class="p-6 bg-white dark:bg-gray-900">
        <table class="w-full sm:w-[600px]" cellpadding="0" cellspacing="0">
          <tr>
            <td class="text-center p-6">
              <img src="https://cdn.brand.com/logo.png" alt="Brand" class="w-24 mx-auto" />
              <h1 class="text-2xl font-bold mt-4 text-gray-900 dark:text-white">
                Welcome to Brand!
              </h1>
              <p class="mt-4 text-gray-600 dark:text-gray-300">
                Here is what to expect over the next 14 days.
              </p>
              <a href="https://brand.com/start" class="inline-block mt-6 px-6 py-3 bg-blue-600 text-white rounded font-semibold no-underline">
                Get started
              </a>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</x-main>
```

```bash
# Compile
maizzle build production

# Output: build_production/welcome.html
```

### Recipe 4: Maizzle config (tailwind.config.js + config.production.js)

```js
// config.production.js
module.exports = {
  build: {
    templates: { source: 'src/templates', destination: 'build_production' },
    tailwind: { css: 'src/css/main.css', config: 'tailwind.config.js' },
  },
  inlineCSS: true,
  removeUnusedCSS: true,
  prettify: false,
}
```

```js
// tailwind.config.js (email-specific)
module.exports = {
  content: ['./src/**/*.{html,njk}'],
  theme: {
    screens: { sm: { max: '600px' } },
    extend: {
      colors: { brand: '#0066ff' },
      fontFamily: { sans: ['Helvetica', 'Arial', 'sans-serif'] },
    },
  },
}
```

### Recipe 5: Push compiled HTML to Klaviyo

```bash
HTML=$(cat build_production/welcome.html)
curl -X POST "https://a.klaviyo.com/api/templates" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" \
  -H "revision: 2024-10-15" \
  -H "Content-Type: application/json" \
  -d "{\"data\":{\"type\":\"template\",\"attributes\":{
    \"name\":\"Welcome 1\",
    \"editor_type\":\"CODE\",
    \"html\":$(echo "$HTML" | jq -Rs .)
  }}}"
```

### Recipe 6: Push to Customer.io

```bash
HTML=$(cat build_production/welcome.html)
curl -X POST "https://api.customer.io/v1/transactional/templates" \
  -H "Authorization: $CIO_APP_API_KEY" \
  -d "{
    \"name\":\"Welcome 1\",
    \"body_html\":$(echo "$HTML" | jq -Rs .),
    \"subject\":\"Welcome to Brand\",
    \"preheader\":\"We are glad you are here.\"
  }"
```

### Recipe 7: Push to Resend (via React Email is more native)

```bash
# Resend prefers React Email components, but raw HTML works
curl -X POST "https://api.resend.com/emails" \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -d "{
    \"from\":\"hello@notify.brand.com\",
    \"to\":\"user@example.com\",
    \"subject\":\"Welcome to Brand\",
    \"html\":$(cat build_production/welcome.html | jq -Rs .)
  }"
```

### Recipe 8: CI pipeline — compile + push to Klaviyo on merge

```yaml
# .github/workflows/email-deploy.yml
name: Email deploy
on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm ci
      - run: npx maizzle build production
      - name: Push to Klaviyo
        env:
          KLAVIYO_API_KEY: ${{ secrets.KLAVIYO_API_KEY }}
        run: |
          for f in build_production/*.html; do
            NAME=$(basename "$f" .html)
            HTML=$(cat "$f")
            curl -X POST "https://a.klaviyo.com/api/templates" \
              -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" \
              -H "revision: 2024-10-15" \
              -d "{\"data\":{\"type\":\"template\",\"attributes\":{
                \"name\":\"$NAME\",
                \"editor_type\":\"CODE\",
                \"html\":$(echo "$HTML" | jq -Rs .)
              }}}"
          done
```

### Recipe 9: MJML dark mode pattern

```xml
<mj-style>
  /* Light defaults */
  .bg-card { background-color: #ffffff !important; }
  .text-primary { color: #111111 !important; }
  .border-soft { border: 1px solid #e5e5e5 !important; }

  /* Dark mode override */
  @media (prefers-color-scheme: dark) {
    .bg-card { background-color: #1a1a1a !important; }
    .text-primary { color: #f0f0f0 !important; }
    .border-soft { border: 1px solid #333 !important; }

    /* Dark-mode-only logo swap */
    .logo-light { display: none !important; }
    .logo-dark  { display: block !important; }
  }

  /* Default: hide dark logo */
  .logo-dark { display: none; }
</mj-style>

<mj-section>
  <mj-column>
    <mj-image css-class="logo-light" src="logo-light.png" />
    <mj-image css-class="logo-dark"  src="logo-dark.png" />
    <mj-text css-class="text-primary">Welcome!</mj-text>
  </mj-column>
</mj-section>
```

### Recipe 10: Render-test compiled HTML (Litmus / EOA via CLI)

```bash
# Compile, upload to Litmus for cross-client render
npx mjml welcome.mjml -o welcome.html
HTML_B64=$(base64 < welcome.html)
curl -X POST "https://api.litmus.com/v1/emails" \
  -H "Authorization: Basic $LITMUS_AUTH" \
  -d "{
    \"subject\":\"Welcome\",
    \"body_html\":\"$(cat welcome.html | jq -Rs .)\",
    \"results_required\":[\"gmailnew\",\"outlook2019\",\"applemail17\",\"yahoo\",\"protonmail\"]
  }"
```

### Recipe 11: Minify + inline before final push

```bash
# After Maizzle/MJML compile, juice for inline CSS (sometimes needed for Outlook)
npx juice build_production/welcome.html welcome.inlined.html

# Minify HTML
npx html-minifier-terser welcome.inlined.html \
  --collapse-whitespace --remove-comments --minify-css \
  -o welcome.final.html

# Check size (Gmail clips > 102 KB)
wc -c welcome.final.html
# Aim for < 80 KB to avoid clipping
```

### Recipe 12: MJML attributes for re-use

```xml
<mj-head>
  <mj-attributes>
    <mj-text font-family="Helvetica, Arial, sans-serif" font-size="16px" line-height="1.5" color="#111" />
    <mj-button background-color="#0066ff" border-radius="6px" color="#fff" padding="14px 28px" />
    <mj-section background-color="#ffffff" padding="0" />
    <mj-class name="muted" color="#888" font-size="14px" />
    <mj-class name="cta" background-color="#0066ff" color="#fff" />
  </mj-attributes>
</mj-head>

<mj-body>
  <mj-text mj-class="muted">Small print here.</mj-text>
  <mj-button mj-class="cta" href="...">Click</mj-button>
</mj-body>
```

## Examples

### Example 1: Build modular welcome series in Maizzle

**Goal:** 4-email welcome series with shared header/footer; deploy to Klaviyo.

**Steps:**

1. `maizzle new welcome-series && cd welcome-series && npm i`
2. Create `src/components/header.html`, `src/components/footer.html`.
3. Author 4 templates in `src/templates/`: welcome-1.html through welcome-4.html, each `<x-include src="components/header.html" />` and footer.
4. Configure dark-mode utilities in `tailwind.config.js`.
5. Test locally: `maizzle serve` — opens render preview at http://localhost:3000.
6. Build: `maizzle build production`.
7. Render-test each compiled template in Litmus (Recipe 10).
8. Push all 4 to Klaviyo via CI pipeline (Recipe 8).
9. Build Klaviyo flow with the 4 template IDs.

### Example 2: Migrate hand-coded HTML to MJML

**Goal:** legacy 800-line table HTML email migrating to MJML maintainability.

**Steps:**

1. Identify structural sections: header, hero, content, CTA, footer.
2. Translate each table block to `<mj-section><mj-column>...`.
3. Replace inline styles with `<mj-attributes>` defaults.
4. Replace media queries with MJML's auto-responsive defaults + `@media` rules in `<mj-style>`.
5. Compile MJML → compare rendered HTML in browser + Litmus to legacy.
6. Once parity confirmed, swap source-of-truth from HTML to MJML in repo.

## Edge cases

- **Outlook (Word engine) renders MJML's auto-tables** — MJML handles it; you usually don't need to think about it. But Outlook breaks on flexbox / CSS grid; never use those in mj-body raw HTML.
- **Gmail clipping at 102 KB** — minify (Recipe 11). Move large CSS to `<mj-style>` (it gets inlined / pruned at compile).
- **Dark mode in Apple Mail flips backgrounds** automatically (annoyingly) — explicit dark-mode classes (Recipe 9) prevent surprises.
- **Gmail does NOT honor `prefers-color-scheme`** consistently — always test in Gmail dark mode.
- **Maizzle requires `<x-main>` outer** — without it, layout templates won't compile.
- **MJML version drift** — newer mj-* elements (mj-spacer, mj-divider, etc.) require recent versions. Pin version in package.json.
- **External CSS in production builds** — both MJML and Maizzle inline CSS by default (correct for email). Don't disable.
- **Custom fonts** — web fonts work in Apple Mail + iOS; Gmail and Outlook fall back to system fonts. Provide good fallback stack.
- **MJML `<mj-raw>` for ESP merge tags** — `{{ first_name }}` or `{% if ... %}` need to be wrapped in `<mj-raw>` so MJML doesn't try to parse them.
- **Maizzle interpolation conflicts with Liquid / Mustache** — wrap ESP-side merge tags in `@{{ raw }}` blocks if Maizzle compilation fights with them.

## Sources

- [MJML docs](https://documentation.mjml.io/)
- [MJML components reference](https://documentation.mjml.io/#components)
- [Maizzle docs](https://maizzle.com/docs)
- [Maizzle Tailwind config](https://maizzle.com/docs/tailwindcss)
- [Cerberus templates](https://tedgoas.github.io/Cerberus/)
- [Foundation for Emails 2 (Inky)](https://get.foundation/emails/docs/inky.html)
- [Litmus best practices](https://www.litmus.com/blog/css-support-in-email-2/)
- [Gmail clipping](https://email.uplers.com/blog/gmail-clipping/)
- [React Email (Resend's framework)](https://react.email/docs/introduction)
