<!--
Source: Litmus + Email on Acid dark-mode + WCAG AA accessibility.
prefers-color-scheme, color contrast, alt text, ARIA, font sizes.
-->
# Dark Mode Email Design + Accessibility — SKILL

`prefers-color-scheme: dark` media query, WCAG AA contrast (≥ 4.5:1 normal, ≥ 3:1 large), ARIA landmarks where supported, alt text on all images, body ≥ 14px / headlines ≥ 22px. Test in Litmus / EOA dark-mode previews. Apple Mail flips automatically; Gmail unreliable; Outlook varies.

## When to use

- "Add dark mode support to our templates"
- "Make our emails WCAG AA compliant"
- "Review email accessibility for screen readers"
- "Fix dark mode contrast issue in Apple Mail"
- "Audit our existing templates for accessibility"

## Setup

```bash
# Testing tools
brew install pa11y                 # accessibility CLI
npm i -g pa11y                     # alternative
npm i -g axe-core/cli              # axe accessibility audit
pipx install accessibility-checker

# Color contrast
brew install wcag-contrast-ratio
# Online: https://webaim.org/resources/contrastchecker/

# Dark mode preview
# Litmus + Email on Acid (paid) — primary
# Browser DevTools: emulate prefers-color-scheme
```

## Common recipes

### Recipe 1: Dark mode CSS pattern (MJML / inline)

```html
<style>
  /* Defaults — light mode */
  .bg-card { background-color: #ffffff; }
  .text-primary { color: #111111; }
  .text-muted { color: #6b7280; }
  .border-soft { border: 1px solid #e5e7eb; }
  .btn-primary { background-color: #0066ff; color: #ffffff; }

  /* Dark mode override */
  @media (prefers-color-scheme: dark) {
    .bg-card { background-color: #1a1a1a !important; }
    .text-primary { color: #f0f0f0 !important; }
    .text-muted { color: #9ca3af !important; }
    .border-soft { border: 1px solid #333333 !important; }
    .btn-primary { background-color: #3b82f6 !important; color: #ffffff !important; }
  }

  /* Apple Mail specific tag (when prefers-color-scheme not supported but Apple flips) */
  [data-ogsc] .bg-card { background-color: #1a1a1a !important; }
  [data-ogsc] .text-primary { color: #f0f0f0 !important; }
</style>
```

Outlook.com uses `[data-ogsb]` and `[data-ogsc]` selectors. Cover both:

```css
[data-ogsb] .bg-card { background-color: #1a1a1a !important; }
[data-ogsc] .text-primary { color: #f0f0f0 !important; }
```

### Recipe 2: Dark-mode logo swap

```html
<style>
  .logo-light { display: block; }
  .logo-dark  { display: none; }

  @media (prefers-color-scheme: dark) {
    .logo-light { display: none !important; }
    .logo-dark  { display: block !important; }
  }

  [data-ogsc] .logo-light { display: none !important; }
  [data-ogsc] .logo-dark  { display: block !important; }
</style>

<img class="logo-light" src="https://cdn.brand.com/logo-dark-on-light.png" alt="Brand" />
<img class="logo-dark"  src="https://cdn.brand.com/logo-light-on-dark.png" alt="Brand" />
```

Or single SVG with `mix-blend-mode` (works in some clients):

```html
<img src="logo.svg" alt="Brand" style="mix-blend-mode: difference;" />
```

### Recipe 3: WCAG AA contrast — checker

```bash
# CLI check
npx wcag-contrast-ratio "#0066ff" "#ffffff"
# Returns: 5.4 (AA pass for normal text, AAA for large text)

# AA thresholds:
#   ≥ 4.5:1 — normal text (body, captions)
#   ≥ 3:1   — large text (≥ 18.66px regular, ≥ 14px bold)
#   ≥ 3:1   — non-text UI elements (icons, buttons)

# Common pairings
npx wcag-contrast-ratio "#666" "#fff"     # 5.74 — pass
npx wcag-contrast-ratio "#999" "#fff"     # 2.85 — FAIL for normal
npx wcag-contrast-ratio "#777" "#fff"     # 4.48 — borderline, prefer #666 or darker
```

Python alternative:

```python
def luminance(rgb):
    r, g, b = [(c/255) for c in rgb]
    def adjust(c): return c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4
    return 0.2126*adjust(r) + 0.7152*adjust(g) + 0.0722*adjust(b)

def contrast(fg_rgb, bg_rgb):
    l1, l2 = luminance(fg_rgb), luminance(bg_rgb)
    return (max(l1,l2) + 0.05) / (min(l1,l2) + 0.05)

print(contrast((0,102,255), (255,255,255)))  # 5.41
```

### Recipe 4: ARIA landmarks (where supported)

```html
<table role="presentation">
  <tr>
    <td>
      <table role="article" aria-labelledby="email-title">
        <tr role="banner">
          <td>
            <img src="logo.png" alt="Brand" />
          </td>
        </tr>
        <tr role="main">
          <td>
            <h1 id="email-title">Welcome to Brand!</h1>
            <p>Here is what to expect.</p>
            <a href="..." role="button" aria-label="Get started with Brand">Get started</a>
          </td>
        </tr>
        <tr role="contentinfo">
          <td>
            <p><a href="{% unsubscribe %}">Unsubscribe</a></p>
            <p>Brand Inc, 123 Main St, City, State 12345</p>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
```

Layout tables get `role="presentation"` so screen readers don't announce row/column structure. Semantic tables (e.g., product comparison) leave native semantics.

### Recipe 5: Alt text patterns

```html
<!-- Informative image -->
<img src="product-hero.jpg" alt="Black leather backpack on wooden table, side view" />

<!-- Decorative image -->
<img src="divider.png" alt="" role="presentation" />

<!-- Image with text overlay -->
<img src="banner-with-text.jpg" alt="Summer Sale: 30% off all swimwear through July 31" />

<!-- Logo -->
<img src="logo.png" alt="Brand" />

<!-- CTA-image link -->
<a href="...">
  <img src="cta-shop.png" alt="Shop the new collection" />
</a>
```

Empty alt (`alt=""`) marks as decorative. NEVER omit `alt` — screen readers will read the URL.

### Recipe 6: Font sizes for accessibility

```css
/* Body */
font-size: 16px;       /* preferred; 14px minimum */
line-height: 1.5;      /* not 1.0 — too tight */

/* Headlines */
h1 { font-size: 28px; line-height: 1.3; }
h2 { font-size: 22px; line-height: 1.3; }
h3 { font-size: 18px; line-height: 1.4; }

/* Captions / small print */
.caption { font-size: 13px; }    /* don't go below 12px */
.legal { font-size: 12px; }

/* Buttons */
.btn { font-size: 16px; padding: 14px 28px; }
```

### Recipe 7: Link affordance (not color only)

```css
/* WCAG: don't rely on color alone */
a {
  color: #0066ff;
  text-decoration: underline;    /* explicit underline */
}

a.btn {
  text-decoration: none;          /* buttons OK without underline if button-shaped */
  background-color: #0066ff;
  color: #fff;
  padding: 14px 28px;
  border-radius: 6px;
  display: inline-block;
}
```

### Recipe 8: Keyboard / focus order

Email is mostly non-interactive, but where you have buttons:

```html
<!-- Logical tab order — DOM order should match visual order -->
<a href="..." tabindex="0">Read more</a>
<a href="..." tabindex="0">Shop now</a>
<a href="..." tabindex="0">Unsubscribe</a>

<!-- Don't use tabindex > 0 — disrupts natural flow -->
```

### Recipe 9: Pa11y audit on compiled HTML

```bash
# Serve compiled email locally
npx http-server build_production -p 8080 &

# Run pa11y
npx pa11y http://localhost:8080/welcome.html --standard WCAG2AA --reporter json > pa11y-report.json

cat pa11y-report.json | jq '.results[] | {code, message, context, selector}'
```

Common findings:
- `WCAG2AA.Principle1.Guideline1_1.1_1_1.H37` — image missing alt
- `WCAG2AA.Principle1.Guideline1_3.1_3_1.H42` — heading levels skipped
- `WCAG2AA.Principle1.Guideline1_4.1_4_3.G18` — contrast ratio insufficient

### Recipe 10: Email on Acid / Litmus dark mode preview

```bash
# Litmus API
curl -X POST "https://api.litmus.com/v1/emails" \
  -H "Authorization: Basic $LITMUS_AUTH" \
  -d "{
    \"subject\":\"Welcome\",
    \"body_html\":$(cat welcome.html | jq -Rs .),
    \"results_required\":[\"gmailnewdark\",\"outlook2019dark\",\"applemail17dark\",\"yahoodark\"]
  }"

# Poll for screenshots
curl "https://api.litmus.com/v1/emails/<id>" -H "Authorization: Basic $LITMUS_AUTH" \
  | jq '.test_set_versions[].results[] | {client: .client_name, screenshot_url: .screenshot_url}'
```

### Recipe 11: Color-blind / Daltonism check

```bash
# Use Coblis simulator: https://www.color-blindness.com/coblis-color-blindness-simulator/
# Or CLI:
pipx install daltonize
daltonize welcome.png deuteranopia welcome-deut.png
daltonize welcome.png protanopia welcome-prot.png

# Check: still readable + actionable for color-blind viewers?
```

### Recipe 12: VoiceOver / TalkBack live test

```
# iOS: Settings → Accessibility → VoiceOver → ON
# macOS: Cmd+F5
# Android: Settings → Accessibility → TalkBack → ON

# Send compiled email to test device → open in Mail app → swipe-listen
# Confirm:
#   - Logo announced as "Brand image" (alt text)
#   - Headings announced as "Heading level 1, Welcome..."
#   - Links announced as "Link, Get started"
#   - No "graphic, graphic, graphic" (would indicate alt-less images)
```

## Examples

### Example 1: Add dark mode to existing welcome template

**Goal:** existing welcome looks broken in Apple Mail dark mode (auto-inverted text invisible on auto-inverted bg).

**Steps:**

1. Identify problem: hex `#ffffff` text on `#0066ff` bg — Apple inverts bg to dark blue, text stays white, but the white text on dark blue is now OK; the problem is body content (#111 on #fff bg inverts to white on white).
2. Wrap content in dark-mode-aware classes (Recipe 1).
3. Add `[data-ogsc]` selectors for Outlook (Recipe 1).
4. Test in Litmus dark previews (Recipe 10).
5. Send live test to iCloud + Gmail + Outlook accounts in their dark modes.
6. Iterate until clean across all targets.

### Example 2: WCAG AA audit + remediation

**Goal:** legal team flagged accessibility risk; bring templates to AA.

**Steps:**

1. Pull current templates from Klaviyo (export HTML).
2. Run pa11y on each (Recipe 9).
3. Common findings batch:
   - Missing alt → add per Recipe 5
   - Low contrast `#999 on #fff` → change to `#666 or darker`
   - Font sizes 12px body → bump to 14-16px
   - Headings skip levels (h1 → h3) → restructure
4. Re-compile + re-test in pa11y. Aim for zero AA-level errors.
5. VoiceOver live test top 3 templates (Recipe 12).
6. Document accessibility statement on brand's site referencing email standards.

## Edge cases

- **Apple Mail flips colors aggressively** — `#fff` becomes `#000`, but `#ffffff` may flip differently than `#FFF`. Always use 6-digit hex.
- **Gmail mobile (Android/iOS) dark mode varies** — Gmail Android honors `prefers-color-scheme`; Gmail iOS sometimes does, sometimes auto-inverts. Test both.
- **Outlook.com web client `[data-ogsc]`** — undocumented selectors; behavior changes over time. Always test in current Outlook.com.
- **Yahoo Mail dark mode** — newer support but quirky. Test live.
- **Image text in dark mode** — text rendered as image (banner) doesn't auto-invert. Provide light/dark image swap.
- **Buttons in dark mode** — solid-color buttons usually fine. Outline buttons (1px border on white bg) become invisible on dark inverted bg.
- **Outlook desktop ignores most CSS** — dark mode in desktop Outlook = system setting impacts client chrome only; email body uses your literal colors.
- **Auto-color from clients** — Gmail and Yahoo iOS sometimes auto-invert based on background luminance. Use explicit hex.
- **Color blindness** — never rely on red/green alone. Add icons + text labels.
- **Screen reader email support** — limited; treat email as "linear narrative." Avoid complex columns.
- **WCAG AA vs AAA** — AA is industry standard; AAA is aspirational. Focus on AA.

## Sources

- [Litmus: dark mode for email guide](https://www.litmus.com/blog/the-ultimate-guide-to-dark-mode-for-email/)
- [Email on Acid: dark mode](https://www.emailonacid.com/blog/article/email-development/dark-mode-for-email/)
- [Email on Acid: accessibility](https://www.emailonacid.com/blog/article/email-development/email-accessibility-tips/)
- [WCAG 2.1 quick reference](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [pa11y](https://pa11y.org/)
- [axe accessibility](https://www.deque.com/axe/)
- [Apple Mail dark mode](https://www.litmus.com/blog/coding-for-apple-mail-dark-mode/)
- [Outlook.com dark mode (`data-ogsc`)](https://www.howtogeek.com/734983/how-to-enable-dark-mode-in-outlook/)
