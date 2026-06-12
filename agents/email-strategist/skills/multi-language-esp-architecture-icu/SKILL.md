<!--
Source: ICU MessageFormat (Unicode) + DeepL + Klaviyo / Customer.io per-locale.
Per-locale templates with Language router; not dynamic blocks in one template.
-->
# Multi-Language ESP Architecture + ICU MessageFormat — SKILL

Per-locale template architecture with Language attribute routing, DeepL-powered translation, ICU MessageFormat for plurals/gender/dates. Not "translate one template into 5 languages via dynamic blocks" — that fails for translation quality and RTL handling. Per-locale templates each get a translator's full review.

## When to use

- "Launch newsletter in 5 languages"
- "Set up Klaviyo / Customer.io to send per-locale templates"
- "Translate templates from English to French / German / Spanish / Japanese"
- "Handle Arabic / Hebrew right-to-left email"
- "Plural and gender handling for German / Russian / Polish"
- "Set up locale-aware send time per cohort"

## Setup

```bash
# ICU MessageFormat tools
npm i -g messageformat                   # ICU MF compiler
npm i intl-messageformat                 # runtime
pipx install babel                       # Python ICU + locale handling
brew install icu4c                       # native ICU library

# DeepL translation (via deepl-mcp or direct API)
export DEEPL_API_KEY="<your-key>"        # https://www.deepl.com/pro-api
```

Klaviyo / Customer.io / HubSpot all support per-locale templates by ID; the routing is done at flow-step level.

## Common recipes

### Recipe 1: Language profile property setup

Use ISO 639-1 codes (lowercase, 2-letter). Set on profile at signup based on browser `Accept-Language` or explicit dropdown.

```bash
# Klaviyo update_profile
curl -X PATCH "https://a.klaviyo.com/api/profiles/<id>" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"profile","attributes":{"properties":{"language":"de","locale":"de-DE","timezone":"Europe/Berlin"}}}}'
```

Common locales:
- `en-US` / `en-GB` — English US/UK (different spellings)
- `de-DE` / `de-AT` / `de-CH` — German variants
- `fr-FR` / `fr-CA` — French variants
- `es-ES` / `es-MX` — Spanish variants
- `pt-PT` / `pt-BR` — Portuguese
- `zh-CN` / `zh-TW` — Chinese
- `ja-JP` — Japanese
- `ko-KR` — Korean
- `ar-SA` — Arabic (RTL)
- `he-IL` — Hebrew (RTL)
- `ru-RU`, `pl-PL`, `nl-NL`, `it-IT`, `sv-SE`, `da-DK`, `no-NO`, `fi-FI`

### Recipe 2: ICU MessageFormat — plurals

```icu
{count, plural,
  =0 {You have no new messages}
  one {You have # new message}
  few {You have # new messages}
  many {You have # new messages}
  other {You have # new messages}
}
```

CLDR plural categories per language:
- English: `one` + `other` (2 categories)
- French: `one` + `other` (note: French treats 0 and 1 as singular)
- German: `one` + `other`
- Russian: `one` + `few` + `many` + `other` (4 categories)
- Polish: `one` + `few` + `many` + `other`
- Arabic: `zero` + `one` + `two` + `few` + `many` + `other` (6 categories!)
- Japanese, Chinese, Korean: `other` only (no plural)

Compile to JavaScript:

```bash
# message.json
echo '{
  "en-US": {"new_messages": "You have {count, plural, =0 {no new messages} one {# new message} other {# new messages}}"},
  "de-DE": {"new_messages": "Du hast {count, plural, =0 {keine neuen Nachrichten} one {# neue Nachricht} other {# neue Nachrichten}}"},
  "ru-RU": {"new_messages": "У вас {count, plural, one {# новое сообщение} few {# новых сообщения} many {# новых сообщений} other {# новых сообщения}}"}
}' > messages.json

npx messageformat compile -l en-US,de-DE,ru-RU messages.json > messages.compiled.js
```

### Recipe 3: ICU MessageFormat — gender + select

```icu
{gender, select,
  male {He purchased {item}.}
  female {She purchased {item}.}
  other {They purchased {item}.}
}

{role, select,
  admin {You have access to all settings.}
  member {You have access to your team.}
  viewer {You can view but not edit.}
  other {Please contact support.}
}
```

### Recipe 4: ICU MessageFormat — number, date, currency

```icu
You earned {amount, number, ::compact-short} dollars.
The sale ends {endDate, date, ::yyyyMMMd}.
Price: {price, number, ::currency/EUR}
```

In Python:

```python
from babel import Locale
from babel.numbers import format_currency, format_decimal
from babel.dates import format_datetime
from datetime import datetime

locale = Locale.parse('de_DE')
print(format_currency(1234.56, 'EUR', locale=locale))
# 1.234,56 €
print(format_datetime(datetime(2026, 6, 9), 'long', locale=locale))
# 9. Juni 2026
```

### Recipe 5: DeepL translation via API

```bash
# Translate plain text
curl "https://api-free.deepl.com/v2/translate" \
  -H "Authorization: DeepL-Auth-Key $DEEPL_API_KEY" \
  -d "text=Welcome to our newsletter!" \
  -d "source_lang=EN" \
  -d "target_lang=DE" \
  -d "formality=more"
# {"translations":[{"detected_source_language":"EN","text":"Willkommen zu unserem Newsletter!"}]}

# Translate HTML email body (DeepL preserves tags)
curl "https://api.deepl.com/v2/translate" \
  -H "Authorization: DeepL-Auth-Key $DEEPL_API_KEY" \
  -d "text=$(cat email.html)" \
  -d "tag_handling=html" \
  -d "source_lang=EN" \
  -d "target_lang=DE"
```

### Recipe 6: Per-locale template in Klaviyo

```bash
# Create one template per language; same skeleton, translated body
for LANG in en de fr es ja; do
  HTML=$(cat templates/welcome.$LANG.html)
  curl -X POST "https://a.klaviyo.com/api/templates" \
    -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
    -d "{\"data\":{\"type\":\"template\",\"attributes\":{
      \"name\":\"Welcome 1 — $LANG\",
      \"editor_type\":\"CODE\",
      \"html\":$(echo "$HTML" | jq -Rs .)
    }}}"
done
```

Capture template IDs for the router.

### Recipe 7: Klaviyo router flow (language → template)

```bash
curl -X POST "https://a.klaviyo.com/api/flows" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"flow","attributes":{
    "name":"Welcome (multi-language router)",
    "trigger":{"type":"list_subscribed","list_id":"<welcome-list>"},
    "steps":[
      {"type":"conditional_split",
       "condition":{"type":"profile-property","property":"language","op":"equals","value":"de"},
       "yes_branch":"de_welcome",
       "no_branch":"check_fr"},
      {"id":"check_fr","type":"conditional_split",
       "condition":{"type":"profile-property","property":"language","op":"equals","value":"fr"},
       "yes_branch":"fr_welcome",
       "no_branch":"check_es"},
      {"id":"check_es","type":"conditional_split",
       "condition":{"type":"profile-property","property":"language","op":"equals","value":"es"},
       "yes_branch":"es_welcome",
       "no_branch":"default_en"},
      {"id":"de_welcome","type":"email","delay_seconds":0,"template_id":"<welcome-de>"},
      {"id":"fr_welcome","type":"email","delay_seconds":0,"template_id":"<welcome-fr>"},
      {"id":"es_welcome","type":"email","delay_seconds":0,"template_id":"<welcome-es>"},
      {"id":"default_en","type":"email","delay_seconds":0,"template_id":"<welcome-en>"}
    ]
  }}}'
```

### Recipe 8: RTL (Arabic / Hebrew) MJML scaffold

```xml
<mjml dir="rtl" lang="ar">
  <mj-head>
    <mj-attributes>
      <mj-all font-family="Cairo, Tahoma, sans-serif" />
    </mj-attributes>
    <mj-style inline="inline">
      body { direction: rtl; text-align: right; }
    </mj-style>
  </mj-head>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text align="right">مرحباً بك في علامتنا التجارية!</mj-text>
        <mj-button background-color="#0066ff" align="right">ابدأ الآن</mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
```

### Recipe 9: Locale-aware send time

```bash
# Klaviyo smart send time per locale
for LANG in en de fr es; do
  curl -X PATCH "https://a.klaviyo.com/api/segments/<segment-id-$LANG>" \
    -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
    -d '{"data":{"type":"segment","attributes":{"send_time_settings":{"smart_send_time":true,"fallback_timezone":"<region-default>"}}}}'
done
```

Cohort-level send time (when not using Smart Send Time):
- EN-US: Tuesday 10am ET
- EN-GB / DE / FR / NL: Tuesday 10am local
- ES-ES: Wednesday 8pm (late evening peak)
- JA: Sunday evening 8pm JST
- AR-SA / HE-IL: Sunday 10am (work week starts Sunday)

### Recipe 10: Recategorize flow (language correction)

For when user receives wrong-language welcome (signup form defaulted to browser lang but they prefer English):

```bash
# Welcome email includes recategorize link:
# https://brand.com/i18n/set?lang=en&p=<profile_id>

# Server-side handler updates Klaviyo profile property
curl -X PATCH "https://a.klaviyo.com/api/profiles/<id>" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"profile","attributes":{"properties":{"language":"en","locale":"en-US"}}}}'
```

### Recipe 11: Translation memory (consistency across templates)

```python
# Maintain a glossary so "Account" always translates as "Konto" (de) not "Account"
glossary_id = create_deepl_glossary({
    'source_lang': 'EN',
    'target_lang': 'DE',
    'entries': {
        'Account': 'Konto',
        'Dashboard': 'Dashboard',  # keep English (brand term)
        'Sign in': 'Anmelden',
        'Sign up': 'Registrieren',
        'Reset password': 'Passwort zurücksetzen',
    }
})

# Use glossary in translation
curl "https://api.deepl.com/v2/translate" \
  -H "Authorization: DeepL-Auth-Key $DEEPL_API_KEY" \
  -d "text=Click here to access your Account" \
  -d "target_lang=DE" \
  -d "glossary_id=$glossary_id"
```

### Recipe 12: Pseudo-localization for QA

Before real translations exist, "pseudo-localize" to expose layout bugs:

```python
# Replace EN text with accented + 30% longer pseudo-translation
def pseudoloc(s):
    pseudo_map = {'a':'á','e':'é','i':'í','o':'ó','u':'ú','y':'ý','A':'Á','E':'É','I':'Í','O':'Ó','U':'Ú'}
    result = ''.join(pseudo_map.get(c, c) for c in s)
    return f"[!! {result} !!][!! padding to test layout !!]"
```

Renders templates with extreme text expansion → catches truncation, overflow, broken responsiveness BEFORE you commit to real translation costs.

## Examples

### Example 1: Launch newsletter in 5 languages

**Goal:** EN newsletter in market 6 months; now expanding to DE / FR / ES / JA.

**Steps:**

1. Add `language` profile property to all profiles (Recipe 1). Default = `en` for existing; capture from form for new.
2. Build language signup-form selector OR detect from `Accept-Language` header.
3. Author EN master template in MJML / Maizzle.
4. Translate body via DeepL for each target language (Recipe 5). Use glossary (Recipe 11) for brand terms.
5. Human review each translation for cultural fit (CTA wording, formality, idioms). German marketing copy is more reserved than English; French is more formal.
6. Upload per-locale templates to Klaviyo (Recipe 6). Capture template IDs.
7. Build router flow (Recipe 7).
8. Cohort-specific send time per locale (Recipe 9).
9. Per-locale subject A/B tests (subject lines compress differently per language; budget more chars for DE).
10. Per-locale tracking: tag campaigns with `lang=de` etc., compare CTR per language.

**Result:** 5-language newsletter with consistent brand voice + locale-aware UX.

### Example 2: Add Arabic (RTL) without breaking existing flows

**Goal:** support Saudi Arabia market.

**Steps:**

1. Add `ar` to language whitelist. Set `locale=ar-SA`.
2. Author Arabic templates with `dir="rtl"` MJML (Recipe 8).
3. Test in Litmus / Email on Acid Outlook + Gmail Arabic preview. Watch for:
   - Punctuation mirroring (some clients flip parens)
   - Number rendering (Arabic numerals vs Hindi-Arabic)
   - Logo + CTA alignment
4. Update router flow to add AR branch.
5. Sunday send-time (Saudi work week).
6. Monitor CTR for first month; iterate copy per cultural fit.

## Edge cases

- **DeepL HTML mode preserves tags** — use `tag_handling=html` for HTML emails. Without it, DeepL may break inline styles.
- **DeepL formality** — `formality=more` / `less` for languages that support it (DE, FR, IT, ES, NL, PL, PT-BR, JA, RU). Use `more` for B2B.
- **Plural categories differ per language** — never assume English's "one + other" works elsewhere. Russian has 4 categories; Arabic 6.
- **German text expansion** — German is typically 30-40% longer than English. Layout breaks if you fixed width. Test pseudo-localized first (Recipe 12).
- **Japanese / Chinese / Korean line breaks** — no spaces between words. Don't word-wrap; use CSS `word-break: break-all` or `keep-all` depending on context.
- **RTL languages flip layout** — not just text. Buttons, images, CTAs flip too. Test in real RTL clients (Gmail RTL view).
- **MJML `dir="rtl"`** — not all MJML versions support; check current MJML release. Maizzle handles via Tailwind's `dir-rtl` modifier.
- **Locale-specific dates** — never hardcode "MM/DD/YYYY". Use ICU date format ("date, ::yyyyMMMd") or Babel.
- **Currency** — render in profile's currency, not sender's. Use ICU currency format with profile.currency code.
- **Per-locale unsubscribe text** — "Unsubscribe" needs translation too. Klaviyo / Customer.io footer text is per-account, not per-template. Set locale-aware footer via segment-specific account if your ESP supports.
- **Apple Mail privacy adjusts per locale** — opens inflated similarly across locales, but engagement signals (click rate) vary by locale; cross-locale comparison needs adjustment.
- **Spam filters in non-English** — some filters trained on English; Russian / Arabic copy may trigger less, OR more (Cyrillic in subject is a known spam pattern in EN markets).

## Sources

- [ICU MessageFormat](https://unicode-org.github.io/icu/userguide/format_parse/messages/)
- [CLDR plural rules](https://cldr.unicode.org/index/cldr-spec/plural-rules)
- [DeepL API](https://www.deepl.com/pro-api)
- [DeepL glossaries](https://www.deepl.com/docs-api/glossaries/)
- [Babel for Python](https://babel.pocoo.org/)
- [messageformat.js](https://messageformat.github.io/messageformat/)
- [Klaviyo multi-language guide](https://help.klaviyo.com/hc/en-us/articles/360038522832)
- [MJML RTL](https://documentation.mjml.io/)
- [Maizzle i18n](https://maizzle.com/docs/templates#components)
