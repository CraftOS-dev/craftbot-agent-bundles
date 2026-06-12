---
name: in-context-editor-setup
description: Stand up in-context translation editors — Crowdin In-Context, Lokalise LiveEdit, Phrase In-Context Editor. Translators edit strings overlaid on the running web app. Use when the user asks "set up in-context editing" or wants translators to see the UI surface they're editing.
---

# In-Context Editor Setup (Crowdin / Lokalise / Phrase)

In-context editors overlay a translation UI directly on the running web app — translators see exactly what they're editing in situ. Setup pattern: deploy a pseudo-translation locale as a build target → inject the editor JS only on that locale → restrict access by role.

## When to use

- Translators are losing context (translating "Save" without knowing it's a button vs a verb).
- QA pass needs visual review (alignment, length, surrounding text).
- Marketing wants real-time copy edits without redeploys.
- You're already on Crowdin / Lokalise / Phrase and have a staging environment.

Trigger phrases: "in-context", "WYSIWYG translation", "translator preview", "Crowdin In-Context", "Lokalise LiveEdit", "live edit".

## Setup

### Prerequisites

- TMS account (Crowdin / Lokalise / Phrase) with project provisioned via `tms-setup-crowdin-lokalise-phrase`.
- Staging or preview environment (in-context editor must NOT run in production).
- Translator role provisioned in TMS (with In-Context permission).

### Per-TMS install

```bash
# Crowdin In-Context — Chrome extension OR JS proxy
# Extension: https://chrome.google.com/webstore/detail/crowdin-in-context/
# OR: enable Crowdin's pseudo-locale "ach" + inject JS snippet

# Lokalise LiveEdit — JS snippet
# Add: <script src="https://app.lokalise.com/live-js/script.min.js"></script>

# Phrase In-Context Editor — JS snippet
# Add: <script src="https://phrase.com/assets/in-context-editor/2.0/app.js"></script>
```

## Common recipes

### Recipe 1: Crowdin In-Context — pseudo-locale + JS

```bash
# 1. Create pseudo-locale distribution
crowdin distribution add --name in-context --target-language ach

# 2. Get distribution hash
crowdin distribution list

# 3. Inject editor on `ach` locale (e.g., staging.app.com/ach/...)
```

```html
<!-- index.html -->
<script>
  window._jipt = [];
  window._jipt.push(['project', 'your-project-name']);
  window._jipt.push(['preload_texts', true]);
</script>
<script src="https://cdn.crowdin.com/jipt/jipt.js"></script>
```

```ts
// React app — only inject for 'ach' locale
if (locale === 'ach') {
  const script = document.createElement('script');
  script.src = 'https://cdn.crowdin.com/jipt/jipt.js';
  document.head.appendChild(script);
}
```

Translator visits `staging.app.com/ach/checkout`, clicks any string, edits in floating panel, saves → string lands in Crowdin TM for review.

### Recipe 2: Lokalise LiveEdit — preview server pairing

```html
<!-- Inject conditionally for staging only -->
<script>
  if (window.location.host.includes('staging')) {
    window.LOKALISE_CONFIG = {
      projectId: 'YOUR_PROJECT_ID',
      locale: 'en'
    };
    const s = document.createElement('script');
    s.src = 'https://app.lokalise.com/live-js/script.min.js';
    document.head.appendChild(s);
  }
</script>
```

Configure in Lokalise project settings:
```
Project → Settings → LiveEdit → ON
Allowed origins: https://staging.app.com
```

Translator logs in to Lokalise, opens staging URL with `?lokalise=1` query param, clicks any string → live edit.

### Recipe 3: Phrase In-Context Editor

```html
<script>
  window.PHRASEAPP_CONFIG = {
    projectId: 'PHRASE_PROJECT_ID',
    accountId: 'PHRASE_ACCOUNT_ID',
    autoLowercase: false,
  };
  if (location.search.includes('phrase')) {
    const s = document.createElement('script');
    s.async = true;
    s.src = 'https://phrase.com/assets/in-context-editor/2.0/app.js';
    document.head.appendChild(s);
  }
</script>
```

Translator visits `https://staging.app.com/?phrase` → editor activates.

### Recipe 4: Wrap i18next strings for in-context

```ts
// i18next with Phrase or Crowdin requires "wrapped keys" so the editor finds them
// i18next: switch to `phraseAppEditor: true` mode

import i18next from 'i18next';
import { phraseAppPostProcessor } from '@phrase/in-context-editor-post-processor';

i18next
  .use(phraseAppPostProcessor)
  .init({
    postProcess: 'phraseapp',
    phraseapp: {
      projectId: 'PHRASE_PROJECT_ID',
      prefix: '{{__',
      suffix: '__}}',
    },
  });
```

Or for Crowdin In-Context with i18next:
```ts
// crowdin requires the string to be in the DOM verbatim for the JS to find it
// — works automatically with React + i18next if no string concatenation
```

### Recipe 5: SPA route awareness (Next.js, React Router)

```tsx
// Re-init editor on route change so newly-rendered strings get clickable
import { useRouter } from 'next/router';
import { useEffect } from 'react';

const router = useRouter();
useEffect(() => {
  if (locale === 'ach' && window._jipt) {
    // Crowdin: trigger rescan
    window._jipt.push(['rescan']);
  }
}, [router.asPath]);
```

### Recipe 6: Restrict editor to translator role

```ts
// Only inject if user is in 'translator' or 'reviewer' role
import { getSession } from 'next-auth/react';
const session = await getSession();
if (session?.user?.role === 'translator' || session?.user?.role === 'reviewer') {
  injectInContextEditor();
}
```

### Recipe 7: Chrome extension fallback (Crowdin Translate)

For sites that can't change source code:
```
1. Install "Crowdin Translate" Chrome extension
2. Configure with project ID + token
3. Translator browses site normally — extension overlays editor on clickable strings
```

Best for SaaS sites where the customer cannot deploy code changes.

### Recipe 8: Screenshot-aware context

```bash
# Crowdin: upload screenshots tagged to specific keys
curl -X POST "https://api.crowdin.com/api/v2/projects/<PID>/screenshots" \
  -H "Authorization: Bearer $CROWDIN_PERSONAL_TOKEN" \
  -F 'storageId=<storage_id>' \
  -F 'name=checkout-button.png'

# Lokalise: upload via UI or API; auto-tag keys visible in screenshot
lokalise2 screenshot upload --token "$LOKALISE_API_TOKEN" --project-id $PID \
  --file=checkout.png --title="Checkout page"
```

### Recipe 9: Locale switcher with `ach` (pseudo) option

```tsx
// app/[locale]/layout.tsx
const LOCALES = ['en', 'de', 'fr', 'ja', 'ar', 'ach'];   // ach for in-context QA
const LOCALE_LABELS = {
  en: 'English', de: 'Deutsch', fr: 'Français',
  ja: '日本語', ar: 'العربية', ach: '⟦Pseudo (In-Context)⟧',
};
```

Don't ship `ach` in production; hide via feature flag.

### Recipe 10: In-context QA workflow

```
1. Translator translates batch in TMS web UI (Crowdin / Lokalise / Phrase)
2. CI builds staging app with new translations
3. Reviewer visits staging.app.com/de/ in browser
4. Reviewer clicks misplaced/awkward strings → leaves comment via in-context editor
5. Translator updates → CI rebuilds → reviewer re-checks
```

## Examples

### Example 1: Wire Crowdin In-Context for a Next.js app

**Goal:** Translators visit `staging.app.com/ach/checkout` and click-edit any string.

**Steps:**
1. Create Crowdin distribution: `crowdin distribution add --name in-context --target-language ach`.
2. Capture distribution hash from `crowdin distribution list`.
3. In `app/[locale]/layout.tsx`, conditionally inject `jipt.js` when `locale === 'ach'` (Recipe 1).
4. Add `ach` to `next-intl` `locales` array (treat as 7th locale).
5. Deploy staging build — translator visits `/ach/checkout`, clicks "Save" button → editor opens with key + screenshot context.
6. Translator edits → string updated in Crowdin TM → next build pulls the change.

**Result:** Translators have screenshot-grounded context; QA cycle drops from days to hours.

### Example 2: Lokalise LiveEdit for a mobile-web staging app

**Goal:** Mobile-first SaaS team uses Lokalise; want translators previewing mobile web with LiveEdit.

**Steps:**
1. In Lokalise project settings → LiveEdit → ON. Add `https://staging-mobile.app.com` to allowed origins.
2. Inject conditional snippet (Recipe 2) — gated on `?lokalise=1` query string.
3. Translator logs in to Lokalise account, opens `staging-mobile.app.com/de?lokalise=1` in mobile-emulator browser.
4. Live edits land directly in Lokalise project; auto-translate suggestions surface inline.
5. CI auto-pulls and rebuilds preview within 60s.

**Result:** Mobile context preserved; translators see actual viewport.

## Edge cases / gotchas

- **String concatenation breaks in-context** — `"Hello " + name` renders as `"Hello __PHRASE_0__"`; editor can't bind. Fix source code first.
- **Dynamic strings** — strings generated from arrays / loops with dynamic IDs may not be discoverable; pre-register keys via TMS API.
- **HTTPS required** — Crowdin/Lokalise/Phrase editor scripts won't load on insecure origin (mixed-content blocked).
- **CSP (Content-Security-Policy)** — TMS scripts need explicit `script-src https://cdn.crowdin.com https://app.lokalise.com https://phrase.com`; add to staging CSP.
- **Production injection = data leak** — editor exposes string structure + TMS project ID. Always gate by environment.
- **`ach` locale in URL** — search engines may index pseudo URLs if not robots.txt'd; add `Disallow: /ach/` to staging robots.txt.
- **Translator login session** — Crowdin/Lokalise editor requires translator to be logged in to TMS in same browser. Provide login URL.
- **Polluted DOM** — editor injects overlays that interfere with click handlers; test critical flows (form submit) work alongside editor.
- **React 18 hydration mismatch** — Crowdin JIPT may modify text node BEFORE React hydrates, causing mismatch warnings. Use `suppressHydrationWarning` on translated nodes.
- **Per-route key registration** — large SPAs may need `_jipt.push(['rescan'])` after each route change (Recipe 5).
- **SSR + in-context** — SSR'd HTML must contain the source string verbatim (no placeholder replacement); else editor can't find it.

## Sources

- Crowdin In-Context: https://support.crowdin.com/in-context-localization/
- Crowdin JIPT (Just-in-Place Translation): https://support.crowdin.com/jipt-installation/
- Lokalise LiveEdit: https://docs.lokalise.com/en/articles/1400520-lokalise-live-edit
- Phrase In-Context Editor: https://support.phrase.com/hc/en-us/articles/5808623543708-In-Context-Editor-Strings-
- i18next + Phrase in-context: https://github.com/i18next/i18next-locize-backend
- Crowdin Translate Chrome ext: https://chrome.google.com/webstore/category/extensions
- React + Crowdin: https://github.com/crowdin/example-react
