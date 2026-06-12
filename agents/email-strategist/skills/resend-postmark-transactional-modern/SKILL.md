<!--
Source: https://resend.com/docs + https://postmarkapp.com/developer
Modern dev-focused transactional. Resend: React Email + fast adoption.
Postmark: deliverability-first, sub-second median, generous free DMARC tier.
-->
# Resend + Postmark Modern Transactional — SKILL

Modern dev-focused transactional email: **Resend** (React Email templates, fast 2024-2026 adoption, KV-style API) and **Postmark** (deliverability-first, sub-second median delivery, free DMARC monitoring). Both default to high-deliverability shared IPs and reject bulk-marketing patterns by policy.

## When to use

- "Send transactional emails (receipts, password reset, magic link, shipping notification) from a modern stack"
- "I want React Email components for templates" → Resend
- "I want deliverability-focused transactional with sub-second SLA" → Postmark
- "Set up message streams to separate password-reset from order-confirmation"
- "Get DMARC report parsing for free on one domain" → Postmark DMARC Monitoring
- "Embed Postmark Spam Check API to score outbound drafts"

Do **not** use for: marketing campaigns (Resend / Postmark explicitly disallow bulk marketing — use Klaviyo / Customer.io); high volume above 10M / month (use SES / Mailgun); newsletter sends (Beehiiv).

## Setup

```bash
# Resend
npm i resend                            # SDK
npm i @react-email/components           # React Email components

# Postmark
npm i postmark                          # SDK
```

Auth:

```bash
# Resend
export RESEND_API_KEY="re_<your_key>"      # https://resend.com/api-keys

# Postmark
export POSTMARK_SERVER_TOKEN="<server-token>"  # https://account.postmarkapp.com/servers
export POSTMARK_ACCOUNT_TOKEN="<account-token>" # for managing servers + domains
```

DNS setup (both):
```
# Verify domain — required for above ~100 sends/day
# Resend
resend._domainkey.<domain>    TXT   "v=DKIM1; k=rsa; p=<key>"
<domain>                       MX    10  feedback-smtp.us-east-1.amazonses.com
<domain>                       TXT   "v=spf1 include:amazonses.com ~all"

# Postmark
<selector>._domainkey.<domain>  TXT   "v=DKIM1; k=rsa; p=<key>"
<domain>                         TXT   "v=spf1 include:spf.mtasv.net ~all"
pm-bounces.<domain>              CNAME pm.mtasv.net
```

## Common recipes

### Recipe 1: Resend — send transactional via REST

```bash
curl -X POST "https://api.resend.com/emails" \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "Brand <hello@notify.brand.com>",
    "to": ["user@example.com"],
    "subject": "Your receipt",
    "html": "<h1>Thanks!</h1><p>Order #1234</p>",
    "headers": {
      "X-Entity-Ref-ID": "order_1234"
    },
    "tags": [{"name":"category","value":"transactional"},
             {"name":"type","value":"receipt"}]
  }'
```

### Recipe 2: Resend with React Email component

```tsx
// emails/Receipt.tsx
import { Html, Head, Body, Container, Text, Button } from '@react-email/components';

export default function Receipt({ name, orderId, total }: any) {
  return (
    <Html><Head /><Body>
      <Container>
        <Text>Hi {name}, thanks for your order.</Text>
        <Text>Order #{orderId} — ${total}</Text>
        <Button href={`https://brand.com/orders/${orderId}`}>View order</Button>
      </Container>
    </Body></Html>
  );
}

// send.ts
import { Resend } from 'resend';
import Receipt from './emails/Receipt';

const resend = new Resend(process.env.RESEND_API_KEY!);
await resend.emails.send({
  from: 'Brand <hello@notify.brand.com>',
  to: 'user@example.com',
  subject: 'Your receipt',
  react: <Receipt name="Sam" orderId="1234" total="49.00" />,
});
```

### Recipe 3: Resend batching (send up to 100 in one call)

```bash
curl -X POST "https://api.resend.com/emails/batch" \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -d '[
    {"from":"Brand <hi@notify.brand.com>","to":["a@x.com"],"subject":"...","html":"..."},
    {"from":"Brand <hi@notify.brand.com>","to":["b@x.com"],"subject":"...","html":"..."}
  ]'
```

### Recipe 4: Postmark — send via SDK with template

```bash
# REST
curl -X POST "https://api.postmarkapp.com/email/withTemplate" \
  -H "X-Postmark-Server-Token: $POSTMARK_SERVER_TOKEN" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "From": "Brand <support@notify.brand.com>",
    "To": "user@example.com",
    "TemplateAlias": "password-reset",
    "TemplateModel": {
      "name": "Sam",
      "reset_url": "https://brand.com/reset?t=abc123",
      "expires_in_minutes": 30
    },
    "MessageStream": "outbound"
  }'
```

### Recipe 5: Postmark message streams (separate transactional categories)

Streams let you separate password-reset from order-confirmation from receipt. Each stream has independent reputation:

```bash
# Create a stream
curl -X POST "https://api.postmarkapp.com/message-streams" \
  -H "X-Postmark-Server-Token: $POSTMARK_SERVER_TOKEN" \
  -d '{
    "ID":"password-reset",
    "Name":"Password Reset",
    "MessageStreamType":"Transactional",
    "Description":"Auth-flow emails only"
  }'

# Send via stream
curl -X POST "https://api.postmarkapp.com/email" \
  -H "X-Postmark-Server-Token: $POSTMARK_SERVER_TOKEN" \
  -d '{
    "From": "auth@notify.brand.com",
    "To": "user@example.com",
    "Subject": "Reset your password",
    "HtmlBody": "<p>Click <a href=\"...\">here</a>.</p>",
    "MessageStream": "password-reset"
  }'
```

### Recipe 6: Postmark Spam Check API — pre-send scoring

```bash
curl -X POST "https://spamcheck.postmarkapp.com/filter" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "email":"From: Brand <hello@brand.com>\nTo: user@example.com\nSubject: Save 50% now\n\nLimited offer! Click here!",
    "options":"long"
  }'
```

Returns SpamAssassin-style report with score + rules triggered. Score < 5.0 is safe; ≥ 5.0 risks spam folder.

### Recipe 7: Postmark DMARC Monitoring (free for 1 domain)

```bash
# Sign up at https://dmarc.postmarkapp.com (free)
# Add DMARC record:
_dmarc.<domain>.    TXT   "v=DMARC1; p=none; rua=mailto:<your-id>@inbound.dmarc.postmarkapp.com"

# Weekly digest emailed to you. Web UI shows source IPs, alignment, failures.
```

### Recipe 8: Resend webhook for delivery / bounce / complaint events

```bash
# Create webhook endpoint via Resend dashboard, or:
curl -X POST "https://api.resend.com/webhooks" \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -d '{
    "endpoint_url":"https://brand.com/webhooks/resend",
    "events":["email.sent","email.delivered","email.bounced","email.complained","email.opened","email.clicked"]
  }'
```

Resend POSTs JSON to your endpoint. Verify with `svix-signature` header.

### Recipe 9: Postmark inbound — turn replies into events

```bash
# Set up inbound stream
curl -X POST "https://api.postmarkapp.com/message-streams" \
  -H "X-Postmark-Server-Token: $POSTMARK_SERVER_TOKEN" \
  -d '{
    "ID":"replies","MessageStreamType":"Inbound","Name":"Inbound replies",
    "InboundHookUrl":"https://brand.com/webhooks/postmark-reply"
  }'

# DNS: MX record for inbound subdomain
# replies.<domain>   MX   10  inbound.postmarkapp.com
```

### Recipe 10: Postmark Bounce + Suppression handling

```bash
# Get bounce list
curl "https://api.postmarkapp.com/bounces?count=50&offset=0" \
  -H "X-Postmark-Server-Token: $POSTMARK_SERVER_TOKEN" | jq '.Bounces[] | {Email, Type, MessageStream}'

# Reactivate a hard bounce after manual verification (rare; usually don't)
curl -X PUT "https://api.postmarkapp.com/bounces/<bounce-id>/activate" \
  -H "X-Postmark-Server-Token: $POSTMARK_SERVER_TOKEN"
```

### Recipe 11: One-click unsubscribe (RFC 8058) — Google/Yahoo Feb 2024 mandate

Required for 5K+/day senders. Both Resend and Postmark inject automatically for marketing-stream messages, but **for transactional you must NOT include unsubscribe** (defeats the point). For mixed senders:

```http
# Resend marketing stream auto-adds
List-Unsubscribe: <mailto:unsubscribe@brand.com>, <https://brand.com/u/abc123>
List-Unsubscribe-Post: List-Unsubscribe=One-Click
```

## Examples

### Example 1: Build a magic-link auth email with Resend + React Email

**Goal:** dev-stack-native magic link email, deliverable to Gmail and Outlook.

**Steps:**

1. Set up DNS (DKIM + SPF) per Resend setup above.
2. Create `emails/MagicLink.tsx` with React Email components.
3. In your auth handler, call `resend.emails.send({ react: <MagicLink ... /> })` (Recipe 2).
4. Tag with `{name: 'category', value: 'auth'}` for analytics segregation.
5. Set up webhook to receive bounce events and de-activate accounts that bounce (Recipe 8).

**Result:** sub-second magic link delivery with auto-handled bounce flow.

### Example 2: Migrate from SendGrid to Postmark for transactional

**Goal:** improve transactional deliverability (SendGrid mixed reputation hurting auth flows).

**Steps:**

1. Verify domain + DKIM in Postmark.
2. Create separate streams: `auth`, `receipts`, `notifications` (Recipe 5).
3. Migrate templates — Postmark uses Mustache syntax; convert SendGrid Handlebars.
4. Dual-send for 7 days (50% SendGrid, 50% Postmark) for comparison.
5. Compare delivery times: SendGrid median ~3-5s, Postmark median <1s.
6. Enable Postmark DMARC Monitoring on the transactional subdomain (Recipe 7).
7. Cutover to 100% Postmark; suppress SendGrid sub-user.

## Edge cases

- **Resend and Postmark reject bulk marketing.** Both will suspend accounts that send marketing volumes (1000+ to a list with marketing content patterns). Use Klaviyo / Customer.io for marketing. Postmark explicitly bans bulk marketing in TOS.
- **Postmark MessageStream type immutable** — you cannot change `Transactional` to `Broadcasts` after creation. Plan stream taxonomy up front.
- **Resend EU residency** — Resend defaults to US infra. For GDPR-strict customers, set `region: "eu-west-1"` at send time and verify EU domain regions.
- **DKIM key rotation** — Resend rotates automatically on 90d cadence; Postmark requires manual rotation. Set calendar reminder.
- **Postmark "outbound" stream is the default** — sending without `MessageStream` parameter routes to `outbound`. Set it explicitly to avoid mis-routing.
- **Sub-millisecond rate limits** — both APIs accept ~100 req/s steady, 1000 burst. Batching (Recipe 3) is the way for higher volume.
- **Resend `react: <Component />` vs `html`** — React Email pre-renders to HTML at send time. If render fails, send fails. Test in CI.
- **Postmark SpamCheck API ≠ inbox placement** — score < 5 doesn't mean Gmail accepts. Use Glock Apps for actual placement testing.
- **One-click unsubscribe in transactional is wrong.** Auth / receipt emails must NOT include unsubscribe links. Don't enable on transactional streams.

## Sources

- [Resend docs](https://resend.com/docs)
- [Resend API reference](https://resend.com/docs/api-reference)
- [React Email components](https://react.email/docs/introduction)
- [Postmark developer docs](https://postmarkapp.com/developer)
- [Postmark message streams](https://postmarkapp.com/blog/announcing-message-streams)
- [Postmark Spam Check](https://spamcheck.postmarkapp.com/doc)
- [Postmark DMARC](https://dmarc.postmarkapp.com/)
- [RFC 8058 one-click unsubscribe](https://datatracker.ietf.org/doc/html/rfc8058)
- [Google sender guidelines](https://support.google.com/mail/answer/81126)
- [Yahoo sender best practices](https://senders.yahooinc.com/best-practices/)
