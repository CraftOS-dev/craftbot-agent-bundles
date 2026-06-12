<!--
Source: https://litmus.com/api + https://www.emailonacid.com/api/
Cross-client render testing. 90+ clients. Dark / light + mobile / desktop.
-->
# Litmus + Email on Acid Rendering Testing — SKILL

Pixel-perfect render testing across 90+ email clients (Outlook 2007/2010/2013/2016/2019/365, Gmail web/iOS/Android, Apple Mail, Yahoo, ProtonMail, Mail.ru, Fastmail, etc.). Light/dark modes, mobile/desktop. Visual diff between versions. Spam-check scoring.

## When to use

- "Render-test our new template across major clients"
- "Confirm dark mode works in Apple Mail + Gmail iOS + Outlook"
- "Diagnose Outlook 2016 layout breakage"
- "Visual diff between template v1 and v2"
- "Spam check before high-stakes send"

## Setup

```bash
# Both are paid services
#   Litmus       — $99/mo+ (Essentials); $300/mo for API access
#   Email on Acid — $84/mo+; API on higher tiers

# Auth
export LITMUS_AUTH="Basic <base64(username:password)>"
# Or API token (newer auth)
export LITMUS_API_KEY="<key>"

export EOA_API_KEY="<key>"
export EOA_USERNAME="<user>"
```

Login: https://litmus.com/login | https://www.emailonacid.com/

## Common recipes

### Recipe 1: Litmus — submit HTML for render testing

```bash
# Submit
RESULT=$(curl -s -X POST "https://api.litmus.com/v1/emails" \
  -H "Authorization: $LITMUS_AUTH" \
  -H "Content-Type: application/json" \
  -d "{
    \"subject\":\"Test render\",
    \"body_html\":$(cat welcome.html | jq -Rs .),
    \"body_text\":$(cat welcome.txt | jq -Rs .),
    \"results_required\":[
      \"gmailnew\",\"gmailnewios\",\"gmailnewandroid\",
      \"outlook2019\",\"outlook365\",\"outlookiphone\",\"outlookandroid\",
      \"applemail17\",\"appleiphone17\",\"appleipad17\",
      \"yahoo\",\"protonmail\",\"fastmail\",
      \"gmailnewdark\",\"outlook2019dark\",\"applemail17dark\"
    ]
  }")

EMAIL_ID=$(echo "$RESULT" | jq -r '.id')
echo "Email ID: $EMAIL_ID"
```

### Recipe 2: Poll for screenshots

```bash
# Poll until status = completed (typically 2-10 min)
while true; do
  STATUS=$(curl -s "https://api.litmus.com/v1/emails/$EMAIL_ID" \
    -H "Authorization: $LITMUS_AUTH" | jq -r '.state')
  echo "Status: $STATUS"
  [ "$STATUS" = "completed" ] && break
  sleep 30
done

# Get screenshots
curl -s "https://api.litmus.com/v1/emails/$EMAIL_ID" \
  -H "Authorization: $LITMUS_AUTH" | \
  jq '.test_set_versions[].results[] | {client: .client_name, screenshot_url: .screenshot_url, status}'
```

### Recipe 3: Litmus — Spam Test (Litmus's spam-check scoring)

```bash
curl -X POST "https://api.litmus.com/v1/spam-tests" \
  -H "Authorization: $LITMUS_AUTH" \
  -d "{
    \"subject\":\"Test\",
    \"body_html\":$(cat welcome.html | jq -Rs .),
    \"from_email\":\"hello@mail.brand.com\",
    \"from_name\":\"Brand\"
  }"

# Poll for results
curl "https://api.litmus.com/v1/spam-tests/<test-id>" \
  -H "Authorization: $LITMUS_AUTH" | \
  jq '{filter_scores: .results[] | {filter, score, comment}}'
```

Returns SpamAssassin + Postini + Apache + ClamAV-style scoring per major filter.

### Recipe 4: Email on Acid — submit test

```bash
curl -X POST "https://api.emailonacid.com/v5/email/tests" \
  -u "${EOA_USERNAME}:${EOA_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{
    \"subject\":\"Test\",
    \"html\":$(cat welcome.html | jq -Rs .),
    \"clients\":[
      \"gmail_chrome_pixel6\",\"gmail_safari_iphone15\",
      \"outlook_2021\",\"outlook_2019_windows10\",
      \"apple_mail_18\",\"apple_iphone_18\",
      \"yahoo_chrome\",\"protonmail_chrome\"
    ]
  }"
```

### Recipe 5: EOA — poll results

```bash
curl "https://api.emailonacid.com/v5/email/tests/<test-id>" \
  -u "${EOA_USERNAME}:${EOA_API_KEY}" | \
  jq '.client_screenshots[] | {client, image_url, accessibility_score, dark_mode}'
```

### Recipe 6: Common clients to cover (priority order)

Tier 1 (must-have):
- gmailnew (web)
- gmailnewios
- gmailnewandroid
- outlook2019 (Word renderer)
- outlook365 (web)
- applemail17 (latest)
- appleiphone17 (latest iOS)
- yahoo (web)

Tier 2 (broad coverage):
- outlookiphone
- outlookandroid
- protonmail
- fastmail
- gmailnewipad

Tier 3 (legacy / regional):
- outlook2007, outlook2010, outlook2013, outlook2016
- mail.ru
- yandex
- gmx, web.de

Dark mode variants:
- gmailnewdark
- outlook2019dark
- applemail17dark
- yahoodark

### Recipe 7: Visual diff between two versions

```bash
# Submit v1
V1_ID=$(curl -s -X POST "https://api.litmus.com/v1/emails" \
  -H "Authorization: $LITMUS_AUTH" \
  -d "{\"subject\":\"v1\",\"body_html\":$(cat v1.html | jq -Rs .),\"results_required\":[\"applemail17\",\"outlook2019\"]}" \
  | jq -r '.id')

# Submit v2
V2_ID=$(curl -s -X POST "https://api.litmus.com/v1/emails" \
  -H "Authorization: $LITMUS_AUTH" \
  -d "{\"subject\":\"v2\",\"body_html\":$(cat v2.html | jq -Rs .),\"results_required\":[\"applemail17\",\"outlook2019\"]}" \
  | jq -r '.id')

# Once both completed, diff via Litmus UI (Compare button) or download both screenshots:
curl -O "$(curl -s "https://api.litmus.com/v1/emails/$V1_ID" -H "Authorization: $LITMUS_AUTH" | jq -r '.test_set_versions[].results[]|select(.client_name=="applemail17").screenshot_url')"
mv applemail17.png v1-applemail17.png

curl -O "$(curl -s "https://api.litmus.com/v1/emails/$V2_ID" -H "Authorization: $LITMUS_AUTH" | jq -r '.test_set_versions[].results[]|select(.client_name=="applemail17").screenshot_url')"
mv applemail17.png v2-applemail17.png

# Use ImageMagick for diff
compare -metric AE v1-applemail17.png v2-applemail17.png diff.png
```

### Recipe 8: CI render test on PR

```yaml
# .github/workflows/email-render.yml
name: Email render check
on: pull_request

jobs:
  render:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx maizzle build production
      - name: Litmus render test
        env: { LITMUS_AUTH: ${{ secrets.LITMUS_AUTH }} }
        run: |
          for f in build_production/*.html; do
            NAME=$(basename "$f" .html)
            ID=$(curl -s -X POST "https://api.litmus.com/v1/emails" \
              -H "Authorization: $LITMUS_AUTH" \
              -d "{\"subject\":\"$NAME render check\",\"body_html\":$(cat "$f" | jq -Rs .),\"results_required\":[\"outlook2019\",\"gmailnew\",\"applemail17\",\"applemail17dark\"]}" \
              | jq -r '.id')
            echo "$NAME → $ID"
            # Wait + diff vs main branch baseline (image hash compare via dHash)
          done
```

### Recipe 9: Outlook 2007-2019 quirks check

Outlook uses Microsoft Word as its rendering engine on desktop. Common failures:

```python
# Lint email HTML for Outlook gotchas
import re

with open('welcome.html') as f:
    html = f.read()

issues = []
if re.search(r'display:\s*flex', html):
    issues.append("'display: flex' — Outlook won't render")
if re.search(r'display:\s*grid', html):
    issues.append("'display: grid' — Outlook won't render")
if re.search(r'border-radius', html) and not re.search(r'mso-', html):
    issues.append("border-radius without VML fallback — Outlook renders square corners")
if re.search(r'<button', html, re.I):
    issues.append("<button> not <a> — Outlook may not style as expected")
if re.search(r'background-image:\s*url', html) and not re.search(r'<v:rect', html):
    issues.append("CSS background-image without VML fallback — Outlook blank background")
if re.search(r'rgba\(', html):
    issues.append("rgba() — Outlook needs solid hex")
if re.search(r'<svg', html, re.I):
    issues.append("inline SVG — Outlook may not render")

for i in issues: print(f"WARN: {i}")
```

VML fallback for buttons / backgrounds (Outlook-specific):

```html
<!--[if mso]>
  <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" href="https://brand.com/start"
    style="height:50px;width:200px;v-text-anchor:middle;" arcsize="12%" fillcolor="#0066ff">
    <w:anchorlock/>
    <center style="color:#fff;font-family:sans-serif;font-size:16px;">Get started</center>
  </v:roundrect>
<![endif]-->

<!--[if !mso]><!-->
  <a href="https://brand.com/start" style="background-color:#0066ff;color:#fff;padding:14px 28px;border-radius:6px;text-decoration:none;display:inline-block;">Get started</a>
<!--<![endif]-->
```

### Recipe 10: Gmail clipping prevention

```bash
# Check final HTML size
wc -c welcome.html
# Gmail clips at 102 KB; aim for < 80 KB

# Minify
npx html-minifier-terser welcome.html --collapse-whitespace --remove-comments --minify-css -o welcome.min.html
wc -c welcome.min.html
```

### Recipe 11: ProtonMail strict CSP test

ProtonMail blocks external resources by default (proxied through ProtonMail CDN). Test:

- Images load (proxied)
- No external CSS fetches
- No `<script>` tags (always strip in email)
- No `<iframe>`
- Web fonts fall back to system

### Recipe 12: Email on Acid Accessibility Audit

EOA includes built-in accessibility scoring:

```bash
curl "https://api.emailonacid.com/v5/email/tests/<test-id>/accessibility" \
  -u "${EOA_USERNAME}:${EOA_API_KEY}" | \
  jq '.audit | {score, issues: [.issues[] | {severity, message, selector}]}'
```

## Examples

### Example 1: Pre-launch render testing

**Goal:** new template — confirm renders across all major clients before going live.

**Steps:**

1. Compile email source → HTML (MJML / Maizzle / hand).
2. Submit to Litmus with Tier 1 + Tier 2 clients (Recipe 1).
3. Wait 5-10 min.
4. Review each screenshot. Look for:
   - Outlook desktop: layout intact? Rounded corners? Buttons render?
   - Gmail web: links work? Tabs (Promotions vs Primary)?
   - Apple Mail dark: contrast acceptable? Logo visible?
   - Mobile (iOS/Android): width responsive? Tap targets ≥ 44px?
5. Fix anything broken. Re-submit until clean.
6. Sign off; push to ESP.

### Example 2: Diagnose Outlook 2019 layout breakage

**Goal:** user-reported screenshot from Outlook 2019 desktop shows broken layout.

**Steps:**

1. Submit to Litmus (Recipe 1) targeting only outlook2019.
2. Inspect screenshot — confirm visible issue.
3. Lint HTML for Outlook gotchas (Recipe 9).
4. Common fixes:
   - Replace flexbox with table layout
   - Add VML fallback for rounded buttons (Recipe 9)
   - Replace CSS background with `<v:rect>` background fill
   - Replace `<button>` with `<a>` styled as button
5. Re-submit; confirm fix.

## Edge cases

- **Email on Acid has more clients (95+); Litmus has cleaner API** — pick based on tradeoff. Some teams use both.
- **Outlook 365 web ≠ Outlook desktop** — they use different rendering engines. Test both separately.
- **Dark mode rendering varies wildly** — Apple Mail flips automatically; Gmail respects prefers-color-scheme; Outlook desktop varies. Test all dark variants.
- **Apple Mail 17 vs 18** — newer versions have different default behaviors. Pin to latest version in tests.
- **Outlook 2007/2010 deprecated** — still possible to test in Litmus; usually unnecessary unless serving B2B SMB market with old IT.
- **Real-device vs simulator** — Litmus uses real machines; EOA uses partially simulated. Real always wins for tricky cases.
- **API rate limits** — Litmus: 100 tests/day on Essentials. EOA: 50 tests/day on basic. Plan CI carefully.
- **Cost of unused tests** — both services charge per test. Pre-PR rendering on every commit can rack up bill. Trigger on merge to main, not push.
- **AMP for Email render** — Litmus / EOA show only HTML fallback rendering. AMP requires real Gmail / Yahoo / Mail.ru test.
- **Web fonts** — clients show fallback during testing if font not pre-loaded. Real customers may see same.
- **Spam testing** — Litmus's SpamAssassin scoring is directional only; real ISPs (Gmail, Outlook) have proprietary filters not modeled.

## Sources

- [Litmus API](https://www.litmus.com/api/)
- [Litmus client list](https://help.litmus.com/article/86-tested-email-clients)
- [Email on Acid API](https://www.emailonacid.com/api/)
- [Email on Acid client list](https://www.emailonacid.com/email-clients-list/)
- [Outlook Word-renderer guide](https://www.litmus.com/blog/the-ultimate-guide-to-css-support-in-email/)
- [VML for Outlook backgrounds](https://www.campaignmonitor.com/blog/email-marketing/2017/01/cross-platform-email-and-vml/)
- [ProtonMail CSS support](https://proton.me/support/email-design-guidelines)
- [Gmail render guide](https://developers.google.com/gmail/design/reference)
