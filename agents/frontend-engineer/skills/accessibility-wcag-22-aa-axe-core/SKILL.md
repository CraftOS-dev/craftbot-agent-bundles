<!--
Source: https://www.deque.com/axe/ · https://www.w3.org/TR/WCAG22/
Authored: June 2026 for the frontend-engineer agent bundle.
-->

# Accessibility — WCAG 2.2 AA + axe-core toolchain

WCAG 2.2 AA is the legal-and-ethical floor for production web. The toolchain:
**axe-core** (engine) + **@axe-core/playwright** (E2E integration) + **pa11y-ci**
(static page sweep) + **Lighthouse** (full-page audit) + **eslint-plugin-jsx-a11y**
(lint-time). Manual checks remain mandatory.

## When to use

- A11y audit / report / compliance check
- Pre-launch / pre-merge gate
- Building accessible components from scratch (forms, dialogs, menus)
- A user reported keyboard nav or screen-reader issues
- Trigger phrases: "accessibility", "a11y", "WCAG", "screen reader", "keyboard
  nav", "axe", "Lighthouse", "ARIA", "focus management", "color contrast"

## Setup

```bash
# Lint-time
pnpm add -D eslint-plugin-jsx-a11y

# E2E in Playwright
pnpm add -D @axe-core/playwright

# Static sweep
pnpm add -D pa11y pa11y-ci

# Lighthouse CI
pnpm add -D @lhci/cli

# react-aria primitives (for compliant components)
pnpm add react-aria-components
```

No API keys.

## Common recipes

### Recipe 1 — ESLint flat config with jsx-a11y

```ts
// eslint.config.ts
import jsxA11y from "eslint-plugin-jsx-a11y";

export default [
  {
    files: ["**/*.{jsx,tsx}"],
    plugins: { "jsx-a11y": jsxA11y },
    rules: jsxA11y.configs.recommended.rules,
  },
];
```

```bash
pnpm exec eslint . --fix
```

Catches: `alt` missing on `<img>`, `onClick` on `<div>` without keyboard
handler, missing `htmlFor` on labels, etc.

### Recipe 2 — Playwright + axe-core E2E

```ts
// tests/a11y.spec.ts
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

const urls = ["/", "/about", "/pricing", "/blog"];

for (const url of urls) {
  test(`${url} is WCAG 2.2 AA accessible`, async ({ page }) => {
    await page.goto(url);
    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"])
      .analyze();

    if (results.violations.length) {
      console.log(JSON.stringify(results.violations, null, 2));
    }
    expect(results.violations).toEqual([]);
  });
}
```

### Recipe 3 — pa11y-ci config + sitemap sweep

```json
// .pa11yci.json
{
  "defaults": {
    "standard": "WCAG2AA",
    "timeout": 30000,
    "wait": 500
  },
  "urls": [
    "http://localhost:3000/",
    "http://localhost:3000/about",
    "http://localhost:3000/contact"
  ]
}
```

```bash
pnpm exec pa11y-ci
# or from sitemap
pnpm exec pa11y-ci --sitemap https://example.com/sitemap.xml
```

### Recipe 4 — Lighthouse CI accessibility budget

```js
// lighthouserc.cjs
module.exports = {
  ci: {
    collect: {
      url: ["http://localhost:3000/", "http://localhost:3000/blog"],
      numberOfRuns: 3,
      startServerCommand: "pnpm start",
    },
    assert: {
      assertions: {
        "categories:accessibility": ["error", { minScore: 0.95 }],
        "categories:best-practices": ["warn", { minScore: 0.9 }],
      },
    },
    upload: { target: "temporary-public-storage" },
  },
};
```

```bash
pnpm exec lhci autorun
```

### Recipe 5 — Accessible button (don't use `<div>` for clickable!)

```tsx
// BAD — invisible to screen readers, no keyboard activation
<div onClick={close}>×</div>

// GOOD
<button type="button" onClick={close} aria-label="Close dialog">
  <span aria-hidden="true">×</span>
</button>
```

### Recipe 6 — Accessible dialog (focus trap + Esc)

```tsx
import { Dialog, DialogContent, DialogTitle, DialogDescription } from "@/components/ui/dialog";

<Dialog open={open} onOpenChange={setOpen}>
  <DialogContent>
    <DialogTitle>Confirm deletion</DialogTitle>
    <DialogDescription>This action cannot be undone.</DialogDescription>
    <button onClick={confirm}>Delete</button>
    <button onClick={() => setOpen(false)}>Cancel</button>
  </DialogContent>
</Dialog>
```

Radix/shadcn handle: focus trap inside dialog, Esc to close, scroll lock,
focus restore on close, `aria-labelledby` + `aria-describedby` wiring.

### Recipe 7 — Accessible form label + error

```tsx
<label htmlFor="email">Email</label>
<input
  id="email"
  type="email"
  autoComplete="email"
  required
  aria-required="true"
  aria-invalid={!!error}
  aria-describedby={error ? "email-err" : "email-help"}
/>
<p id="email-help">We'll never share your email.</p>
{error && <p id="email-err" role="alert">{error}</p>}
```

### Recipe 8 — Visually hidden text (for screen readers only)

```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

Tailwind has `sr-only` built in. Use for icon-only buttons or skip links:

```tsx
<a href="#main" className="sr-only focus:not-sr-only">Skip to main content</a>
<button>
  <SettingsIcon aria-hidden="true" />
  <span className="sr-only">Settings</span>
</button>
```

### Recipe 9 — Focus management (return focus on dialog close)

```tsx
import { useRef, useEffect } from "react";

function Dialog({ open, onClose }: { open: boolean; onClose: () => void }) {
  const triggerRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (open) {
      triggerRef.current = document.activeElement as HTMLElement;
    } else {
      triggerRef.current?.focus();
    }
  }, [open]);
  // ...
}
```

Radix Dialog does this automatically.

### Recipe 10 — Color contrast check (CSS variable + Tailwind)

```css
@theme {
  /* OKLCH — lightness 0.4 against white (1.0) ≈ 4.6:1 ratio ✓ */
  --color-primary: oklch(0.4 0.18 250);
  --color-primary-foreground: oklch(0.98 0 0);
}
```

Test pairs with https://webaim.org/resources/contrastchecker/ or `axe` rule
`color-contrast`. Target: 4.5:1 normal text, 3:1 large text + UI elements.

### Recipe 11 — Keyboard-accessible custom menu

Prefer Radix DropdownMenu / shadcn — already keyboard-accessible. If rolling
your own:

```tsx
import { useState, useRef, useEffect } from "react";

function Menu({ items }: { items: { label: string; onSelect: () => void }[] }) {
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(0);
  const listRef = useRef<HTMLUListElement>(null);

  function onKeyDown(e: React.KeyboardEvent<HTMLButtonElement>) {
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      e.preventDefault();
      setOpen(true);
      setActive((a) => (e.key === "ArrowDown" ? (a + 1) % items.length : (a - 1 + items.length) % items.length));
    }
    if (e.key === "Escape") setOpen(false);
    if (e.key === "Enter") items[active].onSelect();
  }

  return (
    <>
      <button
        aria-haspopup="menu"
        aria-expanded={open}
        onKeyDown={onKeyDown}
        onClick={() => setOpen(o => !o)}
      >
        Open
      </button>
      {open && (
        <ul ref={listRef} role="menu">
          {items.map((it, i) => (
            <li key={it.label} role="menuitem" aria-current={i === active}>
              <button onClick={() => it.onSelect()}>{it.label}</button>
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
```

(Seriously, use Radix.)

## Examples

### Example 1: Audit playbook for a single page

1. Run axe via Playwright: `pnpm test:a11y`
2. Run Lighthouse: `pnpm exec lhci collect --url=http://localhost:3000/`
3. Run pa11y: `pnpm exec pa11y http://localhost:3000/`
4. Tab through manually — every interactive reachable?
5. VoiceOver / NVDA pass on primary flow
6. Zoom 200% — layout intact?
7. Disable CSS — content order makes sense?

### Example 2: Fix common violations from axe output

| axe rule | Fix |
|---|---|
| `image-alt` | Add `alt="..."` (or `alt=""` for decorative) |
| `button-name` | Add visible text or `aria-label` |
| `color-contrast` | Adjust foreground/background to meet 4.5:1 |
| `label` | Wrap input in `<label>` or use `htmlFor` + `id` |
| `link-name` | Add visible text or `aria-label` to `<a>` |
| `landmark-one-main` | Wrap main content in `<main>` |
| `region` | Wrap secondary content in `<aside>` / `<section aria-label>` |
| `aria-allowed-attr` | Remove invalid ARIA combos (e.g., `aria-required` on a `<div>`) |
| `frame-title` | Add `title` to `<iframe>` |
| `html-has-lang` | `<html lang="en">` |

## Edge cases / gotchas

- **Automated tools catch ~30%** — manual keyboard + screen reader testing
  catches the rest. Never rely on axe alone.
- **`role="button"` is a smell** — use `<button>`. If you must use `role`,
  also handle Space + Enter keys and tabindex.
- **`tabindex > 0`** breaks tab order. Only use `tabindex="0"` (in flow) or
  `tabindex="-1"` (focusable but not in tab flow).
- **Skip links** at the top of every page: `<a href="#main" className="sr-only
  focus:not-sr-only">Skip to main</a>`.
- **`aria-hidden="true"` on focusable content** is a critical bug — content
  becomes invisible to AT but still focusable, causing dead Tab stops.
- **Color alone for state** (red error / green success) fails colorblind users.
  Always pair with icon + text.
- **Live regions overuse** — `aria-live="assertive"` interrupts the user. Use
  sparingly; `polite` is the default.
- **Auto-rotating carousels** must have pause controls (WCAG 2.2.2).
- **Focus indicators must persist** — `outline: none` without an `outline:
  ...` on `:focus-visible` is the most common a11y bug.
- **WCAG 2.2 added requirements** — focus appearance (2.4.11), target size
  minimum 24×24 CSS px (2.5.8), dragging movements (2.5.7) must have a non-drag
  alternative.
- **`react-aria-components`** is the gold standard for compliant primitives;
  Radix is close. Both win against rolling your own.
- **`@axe-core/playwright`** can be scoped via `.include('main')` to skip
  third-party content you can't control.

## Sources

- [axe-core rules](https://dequeuniversity.com/rules/axe/4.10) — every rule explained
- [WCAG 2.2 spec](https://www.w3.org/TR/WCAG22/)
- [Inclusive Components — Heydon Pickering](https://inclusive-components.design/)
- [WebAIM contrast checker](https://webaim.org/resources/contrastchecker/)
- [react-aria patterns](https://react-spectrum.adobe.com/react-aria/components.html)
- [WCAG 2.2 what's new](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)
- [GOV.UK accessibility blog](https://accessibility.blog.gov.uk/) — practical writeups
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/) — patterns for every widget
