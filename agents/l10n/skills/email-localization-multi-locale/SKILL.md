---
name: email-localization-multi-locale
description: Multi-locale email templates — MJML + react-email + ICU. Per-locale subject + preheader + body + CTA. Locale-aware date/currency. RTL HTML support. Use when the user asks "localize email templates", "translate email", "RTL email", or "transactional email i18n".
---

# Email Localization — Multi-Locale Templates

Email localization differs from in-app i18n: subject + preheader matter as much as body; engagement differs per region (JA/KO prefer short subjects, DE/RU tolerate longer); CTAs must be transcreated; RTL HTML support varies by mail client.

Stack: **MJML** (responsive email DSL) or **react-email** + ICU MessageFormat + per-locale subject/preheader/CTA pairs.

## When to use

- Transactional emails (welcome, password reset, receipt) for multiple locales.
- Lifecycle / marketing emails (drip, re-engagement) per region.
- Adding new locale to existing email template system.
- Need RTL-aware emails for Arabic / Hebrew markets.

Trigger phrases: "localize email", "translate email", "MJML i18n", "react-email locale", "RTL email", "email subject lines per locale".

## Setup

```bash
# MJML
npm i -g mjml

# react-email
npm i react-email
npx create-email                          # scaffold project

# ICU MessageFormat
npm i intl-messageformat

# i18next for templating
npm i i18next

# ESP SDKs (pick one)
npm i @sendgrid/mail                     # SendGrid
npm i @aws-sdk/client-ses                # AWS SES
npm i resend                             # Resend
npm i @customerio/track-node             # Customer.io
npm i @klaviyo/api                        # Klaviyo
```

Auth/env:
- `SENDGRID_API_KEY` / `RESEND_API_KEY` / etc.

## Per-locale considerations

| Locale | Subject length | Preheader | CTA copy | Notes |
|---|---|---|---|---|
| en-US | 40-50 chars | 80-100 chars | Verb-led ("Get started") | Wide tolerance |
| de-DE | 40-60 chars | Up to 130 chars | Imperative ("Jetzt starten") | Tolerates compound nouns |
| ja-JP | 15-20 chars | 25-30 chars | Polite ("始める") | Mobile-first; shorter |
| ko-KR | 15-25 chars | 30 chars | Polite | Mobile-first |
| ar | 30-40 chars | 60-80 chars | Direct | RTL display |
| fr-FR | 40-50 chars | 80-100 chars | Elegant | Avoid exclamations |
| pt-BR | 40-60 chars | 100-130 chars | Emoji OK | Warm tone |
| es-MX/ES | 40-50 chars | 80-100 chars | Friendly | Latam vs Europe |

Subject lines should be **transcreated** (see `transcreation-cultural-adaptation`), not translated.

## Common recipes

### Recipe 1: MJML template with locale-aware vars

```mjml
<mjml dir="{{dir}}" lang="{{lang}}">
  <mj-head>
    <mj-title>{{subject}}</mj-title>
    <mj-preview>{{preheader}}</mj-preview>
    <mj-attributes>
      <mj-all font-family="'Noto Sans', sans-serif" />
    </mj-attributes>
    <mj-style>
      [dir="rtl"] { text-align: right; direction: rtl; }
      [dir="rtl"] .cta-btn { text-align: center; }
    </mj-style>
  </mj-head>
  <mj-body background-color="#f4f4f4">
    <mj-section background-color="#ffffff">
      <mj-column>
        <mj-text font-size="20px">{{greeting}}, {{name}}!</mj-text>
        <mj-text>{{body}}</mj-text>
        <mj-button href="{{cta_url}}" background-color="#0066cc">
          {{cta_text}}
        </mj-button>
        <mj-text font-size="12px" color="#888">{{footer}}</mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
```

### Recipe 2: Per-locale render script

```bash
#!/bin/bash
for locale in en de fr ja ar zh-Hans-CN; do
  # Substitute locale data from JSON catalog
  jq -r --arg loc "$locale" \
    '.[$loc] | "subject=\(.subject)\npreheader=\(.preheader)\ngreeting=\(.greeting)\nbody=\(.body)\ncta_text=\(.cta_text)\nfooter=\(.footer)"' \
    catalog.json > vars.env

  # Use envsubst or template engine to substitute
  source vars.env
  export lang="$locale"
  export dir=$([[ "$locale" == ar* || "$locale" == he* ]] && echo "rtl" || echo "ltr")

  envsubst < templates/welcome.mjml > rendered/welcome-$locale.mjml
  npx mjml rendered/welcome-$locale.mjml -o dist/welcome-$locale.html
done
```

### Recipe 3: react-email per-locale build

```tsx
// emails/Welcome.tsx
import { Html, Head, Body, Container, Text, Button } from '@react-email/components';
import { useTranslations } from 'next-intl';

export default function Welcome({ locale, name }) {
  const t = useTranslations({ locale });
  const dir = ['ar', 'he', 'ur'].includes(locale) ? 'rtl' : 'ltr';
  return (
    <Html dir={dir} lang={locale}>
      <Head>
        <title>{t('email.welcome.subject', { name })}</title>
      </Head>
      <Body style={{ fontFamily: 'Noto Sans, sans-serif' }}>
        <Container>
          <Text>{t('email.welcome.greeting', { name })}</Text>
          <Text>{t('email.welcome.body')}</Text>
          <Button href={`https://app.com/${locale}/onboarding`}>
            {t('email.welcome.cta')}
          </Button>
        </Container>
      </Body>
    </Html>
  );
}
```

```bash
npx react-email export --locale=de --output=dist/welcome-de.html
```

### Recipe 4: Per-locale catalog (JSON)

```json
{
  "en": {
    "subject": "Welcome to CraftBot, {name}!",
    "preheader": "Get started in 60 seconds — your dashboard is ready.",
    "greeting": "Hi {name}",
    "body": "Thanks for joining. Your account is ready. Let's get you started.",
    "cta_text": "Open dashboard",
    "footer": "© 2026 CraftBot Inc."
  },
  "de": {
    "subject": "Willkommen bei CraftBot, {name}!",
    "preheader": "In 60 Sekunden startbereit — Ihre Übersicht ist da.",
    "greeting": "Hallo {name}",
    "body": "Vielen Dank, dass Sie dabei sind. Ihr Konto ist bereit.",
    "cta_text": "Übersicht öffnen",
    "footer": "© 2026 CraftBot Inc."
  },
  "ja": {
    "subject": "{name}様、CraftBotへようこそ",
    "preheader": "60秒で始められます。",
    "greeting": "{name}様",
    "body": "ご登録ありがとうございます。",
    "cta_text": "始める",
    "footer": "© 2026 CraftBot Inc."
  },
  "ar": {
    "subject": "مرحباً {name} في CraftBot!",
    "preheader": "ابدأ في 60 ثانية.",
    "greeting": "مرحباً {name}",
    "body": "شكراً لانضمامك. حسابك جاهز.",
    "cta_text": "افتح لوحة التحكم",
    "footer": "© 2026 CraftBot Inc."
  }
}
```

### Recipe 5: Locale-aware date / currency in email

```tsx
// Receipt email with locale formatting
const formatted = {
  amount: new Intl.NumberFormat(locale, { style: 'currency', currency }).format(amount),
  date: new Intl.DateTimeFormat(locale, { dateStyle: 'long' }).format(date),
};

<Text>
  {t('receipt.body', {
    amount: formatted.amount,
    date: formatted.date,
  })}
</Text>
```

### Recipe 6: ESP send with per-locale subject + body

```ts
// SendGrid
import sgMail from '@sendgrid/mail';
sgMail.setApiKey(process.env.SENDGRID_API_KEY);

const html = await renderEmail({ locale, name });   // react-email or MJML
const subject = t({ locale }, 'email.welcome.subject', { name });

await sgMail.send({
  from: 'hello@craftbot.com',
  to: user.email,
  subject,
  html,
  headers: { 'Content-Language': locale },
});
```

### Recipe 7: AWS SES with template per locale

```bash
# Create SES template per locale
aws ses create-template --template '{
  "TemplateName": "welcome-de",
  "SubjectPart": "Willkommen bei CraftBot, {{name}}!",
  "HtmlPart": "<html>...</html>"
}'

# Send
aws ses send-templated-email \
  --from-email-address hello@craftbot.com \
  --destination ToAddresses=user@example.com \
  --template welcome-de \
  --template-data '{"name":"Max"}'
```

### Recipe 8: Klaviyo / Customer.io multi-locale templates

```ts
// Customer.io — template language picked per profile attribute
import { TrackClient } from 'customerio-node';
const cio = new TrackClient(SITE_ID, API_KEY);

await cio.identify(userId, { language: 'de' });        // tag user
await cio.track(userId, {
  name: 'welcome_email',                                // template chooses language by user.language
  data: { name: 'Max' },
});
```

### Recipe 9: MJML inline styles for Outlook RTL

```mjml
<mj-style>
  /* Outlook ignores external CSS for RTL — inline! */
  [dir="rtl"] .table-cell {
    text-align: right !important;
  }
  [dir="rtl"] td[data-mj-button] {
    text-align: center !important;
  }
</mj-style>
```

Outlook 2007-2019 strip many RTL styles; fall back to explicit `align="right"`.

### Recipe 10: A/B subject line testing per locale

```ts
// Per-locale variant pool
const subjects = {
  de: ['Willkommen bei CraftBot', 'Ihr Konto ist da', 'Endlich produktiv'],
  ja: ['CraftBotへようこそ', '始めましょう', 'はじめての一歩'],
};

const variant = pickVariant(userId, locale, subjects[locale]);
await sendEmail({ subject: variant, ... });
```

Measure open rate per variant per locale; promote winner.

### Recipe 11: Preheader truncation per client

```html
<!-- Hidden preheader — visible in Gmail inbox preview -->
<div style="display:none; overflow:hidden; height:0;">
  {{preheader}}
  &zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;
</div>
```

Length budget:
- Gmail mobile: ~50 chars
- Gmail desktop: ~100 chars
- Outlook: ~30 chars
- iOS Mail: ~90 chars

Localize preheader to fit shortest target client.

### Recipe 12: From-name localization

```ts
// Per-locale "from" name
const FROM = {
  en: 'CraftBot Team <hello@craftbot.com>',
  de: 'CraftBot-Team <hello@craftbot.com>',
  ja: 'CraftBotチーム <hello@craftbot.com>',
  ar: 'فريق CraftBot <hello@craftbot.com>',
};
```

Some ESP support per-locale from name natively (Customer.io); others require parameter.

### Recipe 13: Plain text fallback per locale

```ts
const html = await renderHtml(template, locale, vars);
const text = await renderText(template, locale, vars);   // strip HTML or use separate template

await sgMail.send({ to, subject, html, text });
```

Plain text doesn't need RTL handling but does need locale-aware encoding (UTF-8).

### Recipe 14: Email locale switch trigger

```ts
// User changes locale in product → re-send welcome in new locale OR just update profile
await db.users.update({ id: userId, locale: 'de' });
await emailService.sendWelcome({ userId, locale: 'de' });  // resend in DE
```

### Recipe 15: Litmus / Email on Acid preview per locale

```bash
# Litmus API — preview rendering across 90+ email clients per locale
curl -X POST 'https://api.litmus.com/v1/emails' \
  -H "Authorization: Basic $LITMUS_API_KEY" \
  -d '{"name":"welcome-de","subject":"Willkommen","html":"<html>...</html>"}'
```

## Examples

### Example 1: Localize welcome email into 6 locales

**Goal:** Single welcome email template; per-locale subject/body/CTA in en/de/fr/ja/ar/pt-BR.

**Steps:**
1. Write MJML template with vars (Recipe 1).
2. Build per-locale `catalog.json` (Recipe 4) — source EN + Crowdin-translated targets.
3. Render per locale (Recipe 2 — `for locale in en de fr ja ar pt-BR`).
4. Inline CSS via `juice` (MJML auto-inlines).
5. Send via SES / SendGrid with per-locale subject (Recipe 6).
6. Track open rate / click rate per locale.

**Result:** Single template, 6 localized emails; A/B test subjects (Recipe 10).

### Example 2: Add Arabic RTL email support

**Goal:** Existing en/de email template → add ar with RTL layout.

**Steps:**
1. Add `dir="rtl"` to MJML root for ar (Recipe 1).
2. Inline `[dir="rtl"] { text-align: right; }` style (Recipe 1, 9).
3. Translate catalog: include ar subject (Arabic-Indic digits OK).
4. Render: `npx mjml ... -o welcome-ar.html`.
5. Litmus preview (Recipe 15) — check Outlook 2016, iOS Mail, Gmail mobile.
6. Fix any Outlook clipping with inline `align="right"` attributes.
7. Test send to AR-locale mailbox; verify rendering.

**Result:** Arabic emails render correctly RTL across Gmail, Apple Mail, Outlook (mostly), Yahoo.

## Edge cases / gotchas

- **Outlook + RTL** — Outlook 2007-2019 strip many CSS direction rules; use HTML attributes (`align="right"`, `dir="rtl"` on cells).
- **Subject line emoji** — works in most clients but breaks Outlook 2010/2013. Test per region.
- **Subject line truncation** — Gmail mobile truncates at ~30 chars on phones. JP/KO already short; DE/EN need front-loaded keywords.
- **From-name length** — Outlook truncates from-name at 30 chars; JP from-name in kana ~10 visible chars.
- **MIME encoding** — non-Latin subject lines need MIME-encoded headers (RFC 2047). Most ESP handle, but verify.
- **CSS `font-family` fallback for CJK** — many fonts missing; fall back to `'Noto Sans JP', 'Hiragino Sans', sans-serif`.
- **Image-based CJK characters** — clients may not render web fonts; consider inline images for hero headlines.
- **DPI scaling on retina** — provide 2x images per locale.
- **Plain text wrap** — per-locale word wrap at 72 chars; CJK has no spaces, harder to wrap.
- **Unsubscribe link mandatory** — CAN-SPAM (US), CASL (Canada), GDPR (EU); list-unsubscribe header required for Gmail bulk.
- **ESP catalog format diff** — SendGrid uses dynamic templates (Handlebars-ish); SES uses Mustache; Klaviyo uses Jinja2. Pick one + cross-render.
- **Locale fallback** — user lacks locale → default. Don't email en to ja user when ja template exists.
- **Email rendering tests cost** — Litmus/EoA charge per render; budget; or use Mailtrap free tier.
- **Subject A/B sample size** — need 1k+ sends per variant per locale for stat-sig open-rate diff.
- **Holiday-aware send timing** — Lunar New Year (CN/KR/VN), Ramadan (MENA), Golden Week (JP); skip campaigns.
- **GDPR right to be forgotten** — recipient asks deletion → remove from ESP suppression list + product DB.
- **Localized footer (CASL/GDPR)** — physical address required; localize labels but not data.

## Sources

- MJML: https://mjml.io/
- MJML i18n: https://documentation.mjml.io/
- react-email: https://react.email/
- react-email components: https://react.email/docs/components
- SendGrid dynamic templates: https://docs.sendgrid.com/ui/sending-email/how-to-send-an-email-with-dynamic-templates
- AWS SES templates: https://docs.aws.amazon.com/ses/latest/dg/send-email-formatted-using-ses-api.html
- Customer.io languages: https://customer.io/docs/journeys/multi-language-content/
- Klaviyo multi-language: https://help.klaviyo.com/hc/en-us/articles/115005082427
- Resend: https://resend.com/docs
- RFC 2047 (MIME headers): https://www.rfc-editor.org/rfc/rfc2047
- Litmus: https://www.litmus.com/
- Email on Acid: https://www.emailonacid.com/
- Email RTL guide: https://www.email-on-acid.com/blog/article/email-development/right-to-left-email-design/
