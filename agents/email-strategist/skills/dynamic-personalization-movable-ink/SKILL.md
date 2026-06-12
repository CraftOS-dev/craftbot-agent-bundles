<!--
Source: https://movableink.com/developers + AMP for Email
Open-time dynamic content (weather, countdown, inventory, geo, behavior).
AMP for Email in-inbox interactivity (Gmail, Yahoo, Mail.ru).
-->
# Dynamic Personalization (Movable Ink + AMP for Email) — SKILL

Open-time dynamic content via Movable Ink (weather / countdown / inventory / geo / behavior) and in-inbox interactivity via AMP for Email (forms, carousels, live data). Movable Ink generates personalized images at open-time; AMP for Email runs interactive components in supported inboxes (Gmail, Yahoo, Mail.ru, Verizon).

## When to use

- "Add weather-personalized hero to campaign"
- "Insert live countdown timer in email"
- "Show real-time inventory in product email"
- "Build in-inbox booking form" → AMP
- "Embed live carousel of products" → AMP
- "Open-time geo-targeted store map"

## Setup

### Movable Ink

```bash
# Enterprise contract; no self-serve signup.
# Movable Ink provides:
#   - Account API key
#   - Asset URL template (https://<your-instance>.movableink.com/v1/img/...)
export MI_API_KEY="<movable-ink-key>"
export MI_INSTANCE="<your-instance>"
```

### AMP for Email

```bash
# Domain must be authorized by each receiver:
#   Gmail: https://developers.google.com/gmail/ampemail/register-with-gmail
#   Yahoo: https://senders.yahooinc.com/amp
#   Mail.ru: https://postmaster.mail.ru/amp
#
# Production-only after approval (which requires test sends + DMARC at quarantine/reject)

npm i -g @ampproject/amp-toolbox      # validator
```

## Common recipes

### Recipe 1: Movable Ink — weather-personalized hero

```html
<!-- In Klaviyo template, insert MI tag -->
<img src="https://<your-instance>.movableink.com/v1/img/{{ profile_id }}/weather?lat={{ profile.latitude }}&lon={{ profile.longitude }}&campaign=summer-sale"
     width="600" alt="Today's forecast" />

<!-- MI fetches at open-time, returns an image showing current weather + custom CTA -->
```

Movable Ink setup (server-side via UI / API):
1. Create a "weather" content unit
2. Configure: data source (Weather API), template (image template), fallback (default image)
3. Tag returns the URL pattern above

### Recipe 2: Movable Ink — countdown timer

```html
<img src="https://<your-instance>.movableink.com/v1/img/countdown?end=2026-06-30T23:59:59Z&size=600x100&theme=dark"
     width="600" height="100" alt="Sale ends in" />
```

Renders real-time countdown at open. Apple Mail's pre-fetch is friend or foe: if image pre-fetched at receipt, countdown is from-receipt-time. Use cache-busting tokens if you need open-time accuracy.

### Recipe 3: Movable Ink — inventory status

```html
<img src="https://<your-instance>.movableink.com/v1/img/inventory?sku={{ event.sku }}&campaign={{ campaign }}"
     alt="Stock status" />
```

Movable Ink calls your inventory API at open-time. If stock < threshold, shows "Only X left!" with urgency styling; else shows generic CTA.

### Recipe 4: Movable Ink — geo-targeted nearest store

```html
<img src="https://<your-instance>.movableink.com/v1/img/nearest-store?lat={{ profile.latitude }}&lon={{ profile.longitude }}"
     alt="Your nearest store" />
```

Calls map provider (Mapbox, Google) at open-time, renders local map + store info.

### Recipe 5: AMP for Email — basic structure

AMP for Email requires three MIME parts: `text/html` (fallback), `text/x-amp-html` (AMP), `text/plain`.

```html
<!doctype html>
<html ⚡4email>
<head>
  <meta charset="utf-8" />
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp4email-boilerplate>body{visibility:hidden}</style>
</head>
<body>
  <h1>Hello!</h1>
  <p>Welcome to interactive email.</p>
</body>
</html>
```

### Recipe 6: AMP — in-inbox form

```html
<!doctype html>
<html ⚡4email>
<head>
  <meta charset="utf-8" />
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <script async custom-element="amp-form" src="https://cdn.ampproject.org/v0/amp-form-0.1.js"></script>
  <style amp4email-boilerplate>body{visibility:hidden}</style>
  <style amp-custom>
    form { padding: 24px; }
    input[type=text] { width: 100%; padding: 12px; border: 1px solid #ccc; }
    input[type=submit] { background: #0066ff; color: #fff; padding: 12px 24px; border: 0; }
  </style>
</head>
<body>
  <form method="POST"
        action-xhr="https://api.brand.com/feedback"
        target="_top">
    <h2>How was your experience?</h2>
    <textarea name="feedback" required></textarea>
    <input type="submit" value="Send feedback" />
    <div submit-success>
      <template type="amp-mustache">
        Thanks for the feedback, {{first_name}}!
      </template>
    </div>
    <div submit-error>
      <template type="amp-mustache">
        Something went wrong. Please try again.
      </template>
    </div>
  </form>
</body>
</html>
```

Server endpoint must:
- Accept `application/x-www-form-urlencoded` POST
- Return `application/json`
- Include CORS headers: `Access-Control-Allow-Credentials: true`, `Access-Control-Allow-Origin: <sender-domain>`, `AMP-Access-Control-Allow-Source-Origin: <sender-domain>`, `Access-Control-Expose-Headers: AMP-Access-Control-Allow-Source-Origin`

### Recipe 7: AMP — live product carousel

```html
<script async custom-element="amp-carousel" src="https://cdn.ampproject.org/v0/amp-carousel-0.1.js"></script>
<script async custom-element="amp-list" src="https://cdn.ampproject.org/v0/amp-list-0.1.js"></script>

<amp-list
  src="https://api.brand.com/featured-products"
  layout="responsive"
  width="600"
  height="400"
  binding="no">
  <template type="amp-mustache">
    <amp-carousel width="600" height="400" type="slides" layout="responsive">
      {{#products}}
      <div>
        <amp-img src="{{image}}" width="600" height="400" layout="responsive"></amp-img>
        <h3>{{name}}</h3>
        <p>${{price}}</p>
        <a href="{{url}}" target="_blank">Shop now</a>
      </div>
      {{/products}}
    </amp-carousel>
  </template>
</amp-list>
```

### Recipe 8: AMP validation

```bash
# Validate AMP HTML
amp validator amp-email.html
# Or web tool: https://amp.dev/documentation/tools/?format=email

# Programmatic
node -e "
const validator = require('@ampproject/amp-toolbox-cli');
validator.validate('amp-email.html');
"
```

### Recipe 9: Send AMP via Resend / Postmark / SES

```bash
# Resend (does NOT yet support text/x-amp-html in primary API — workaround required)

# SES via MIME parts
aws sesv2 send-email \
  --from-email-address "Brand <hello@notify.brand.com>" \
  --destination "ToAddresses=user@gmail.com" \
  --content '{
    "Raw":{
      "Data":"Subject: Interactive email\nMIME-Version: 1.0\nContent-Type: multipart/alternative; boundary=\"BOUND\"\n\n--BOUND\nContent-Type: text/plain\n\nFallback text...\n\n--BOUND\nContent-Type: text/x-amp-html; charset=utf-8\n\n<!doctype html><html ⚡4email>...</html>\n\n--BOUND\nContent-Type: text/html; charset=utf-8\n\n<html>HTML fallback</html>\n\n--BOUND--"
    }
  }'
```

Klaviyo supports AMP via their template editor; specify the AMP version alongside HTML.

### Recipe 10: AMP — domain authorization (Gmail)

```
# 1. Send AMP-enabled email from your authorized sending domain
# 2. From a known-good test inbox, manually approve via "Trusted senders" → Add YOUR-DOMAIN.com
# 3. Submit production application at https://developers.google.com/gmail/ampemail/register-with-gmail
#    Requires:
#      - DMARC at p=quarantine or reject
#      - Volume history
#      - Sample AMP messages
# 4. Approval typically 5-10 days
# 5. Once approved, all subscribers see AMP version
```

### Recipe 11: Combine Movable Ink + AMP

For maximum personalization, AMP body shows interactive content powered by your backend (live data), Movable Ink generates the static fallback HTML hero image:

```html
<!-- HTML fallback (most clients) -->
<img src="https://<mi-instance>.movableink.com/v1/img/{{ profile_id }}/weather" alt="Today's weather" />

<!-- AMP version (Gmail / Yahoo) -->
<!doctype html>
<html ⚡4email>
<head>...</head>
<body>
  <amp-list src="https://api.brand.com/weather?id={{profile_id}}" ...>
    <template type="amp-mustache">
      <div>Today: {{conditions}}, {{temp_f}}°F</div>
    </template>
  </amp-list>
</body>
</html>
```

### Recipe 12: Movable Ink reporting

```bash
# Pull per-campaign performance via MI API
curl "https://api.movableink.com/v1/reports/campaigns?from=2026-05-01&to=2026-06-09" \
  -H "Authorization: Bearer $MI_API_KEY" | jq '.data[] | {campaign_name, impressions, clicks, ctr, revenue}'
```

## Examples

### Example 1: Weather-personalized seasonal sale

**Goal:** "Summer Sale" email shows local weather + recommended product (winter coat for snow areas, sunglasses for sunny).

**Steps:**

1. Movable Ink content unit: input lat/lon, output image with weather + product recommendation.
2. In Klaviyo template, embed MI tag (Recipe 1).
3. Klaviyo passes `{{ profile.latitude }}` from profile property (captured at signup via geolocation).
4. At open-time, MI fetches weather, picks product, renders image.
5. Campaign sees CTR lift 30-50% over generic hero (case study average).

### Example 2: In-inbox event RSVP via AMP

**Goal:** for VIP event invite, let users RSVP in inbox without clicking through.

**Steps:**

1. Author AMP email (Recipe 6).
2. Build CORS-compliant endpoint at `api.brand.com/rsvp`.
3. Get Gmail AMP authorization (Recipe 10) — 5-10 day approval.
4. Send via SES MIME-parts (Recipe 9).
5. Track RSVPs server-side; non-AMP users click through to standard form.
6. RSVP conversion rate typically 2-3x higher than landing-page click-through.

## Edge cases

- **Movable Ink is enterprise-priced** ($25K+/yr typical). Not accessible to small senders. Free alternatives are limited (Stripo, BEE templates have some dynamic blocks; nothing matches MI breadth).
- **Apple Mail Privacy Protection pre-fetches images** at receipt time, not open time. Countdown timers fire at receipt; weather is at-receipt accuracy. For true open-time, use AMP if recipient is on Gmail / Yahoo.
- **AMP for Email needs domain authorization** per receiver. Gmail approval is the major one; Yahoo and Mail.ru also.
- **AMP fallback critical** — Apple Mail, Outlook, ProtonMail show only the HTML fallback. Design HTML to look complete; AMP is enhancement.
- **AMP forms require HTTPS + CORS** correctly. AMP validator catches missing headers; production sends fail silently if CORS broken.
- **AMP cache invalidation** — Gmail caches AMP for 24h; if you need fresher data, set `cache-control: no-cache` headers on amp-list sources.
- **Movable Ink renders as image** — image-blocking clients (some Outlook configurations) show alt text only. Provide meaningful alt.
- **AMP version not available in many clients** — coverage is ~30-40% of US lists (Gmail + Yahoo + Verizon).
- **Privacy concerns** — Movable Ink loads image with profile_id; this discloses an open event to MI's servers. GDPR requires processor agreement.
- **AMP tracking** — opens still tracked via traditional pixel; AMP additionally tracks engagement (clicks within AMP). Klaviyo + MI provide combined reports.
- **AMP content is NOT searchable** in Gmail inbox-search. Important content should also be in HTML fallback.

## Sources

- [Movable Ink](https://movableink.com/)
- [Movable Ink developer docs](https://movableink.com/developers)
- [AMP for Email](https://amp.dev/about/email/)
- [AMP for Email components](https://amp.dev/documentation/components/?format=email)
- [Gmail AMP authorization](https://developers.google.com/gmail/ampemail/register-with-gmail)
- [Yahoo AMP](https://senders.yahooinc.com/amp)
- [Mail.ru AMP](https://postmaster.mail.ru/amp)
- [Klaviyo AMP support](https://help.klaviyo.com/hc/en-us/articles/9333207193243)
- [SES sending AMP](https://docs.aws.amazon.com/ses/latest/dg/send-email-amp.html)
- [AMP validator](https://amp.dev/documentation/tools/)
