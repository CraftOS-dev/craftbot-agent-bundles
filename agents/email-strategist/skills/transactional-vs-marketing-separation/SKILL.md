<!--
Source: Resend + Postmark + Klaviyo guides on stream separation.
Subdomain + IP + ESP separation. Stricter DMARC on transactional.
-->
# Transactional vs Marketing Separation — SKILL

Separate transactional (receipts, password resets, magic links) from marketing (campaigns, newsletters, lifecycle). Different subdomains, different IP pools, ideally different ESPs, stricter DMARC on transactional. Co-mingling drags transactional deliverability down to marketing's level.

## When to use

- "Receipts are landing in spam — we send marketing on same domain"
- "Set up separate transactional + marketing email infrastructure"
- "Migrate from single-domain to subdomain split"
- "Architecture review: what should be transactional vs marketing"
- "Configure stricter DMARC on transactional subdomain"

## Setup

```bash
# No new tools — DNS + ESP architecture skill.
# Required tools (already in agent.yaml):
#   cli-anything dig
#   AWS Route53 / Cloudflare DNS API for DNS automation
```

## Common recipes

### Recipe 1: Classify each sender into transactional or marketing

```
| Sender                              | Stream         | Justification |
|-------------------------------------|----------------|---------------|
| Order receipt                       | Transactional  | Explicit user expectation |
| Shipping notification               | Transactional  | Required for order completion |
| Password reset                      | Transactional  | Security-critical, auth flow |
| Magic link / OTP                    | Transactional  | Auth flow |
| Account verification                | Transactional  | Account creation |
| Invoice                             | Transactional  | Billing requirement |
| Newsletter                          | Marketing      | Opt-in content |
| Promotional campaign                | Marketing      | Opt-in content |
| Browse abandonment                  | Marketing      | Opt-in lifecycle |
| Cart abandonment                    | Marketing-gray | Industry usually marketing; "your cart" content vs "your order" |
| Review request                      | Marketing      | Post-purchase but opt-in |
| Win-back                            | Marketing      | Opt-in lifecycle |
| Survey                              | Marketing      | Opt-in content |
| Birthday / anniversary              | Marketing      | Opt-in content |
| Notification (e.g., "X commented")  | Transactional  | User-action-triggered notification |
| Digest (e.g., "10 new comments")    | Marketing      | Aggregated, periodic |
```

When unsure: if user EXPECTS the email at that exact moment based on an action they just took → transactional. Else → marketing.

### Recipe 2: DNS architecture

```
brand.com                   ← corp / website only; no mail sends
├── notify.brand.com        ← transactional ESP (Resend / Postmark)
│   SPF:    "v=spf1 include:_spf.resend.com ~all"
│   DKIM:   resend._domainkey.notify.brand.com TXT "v=DKIM1; ..."
│   DMARC:  _dmarc.notify.brand.com TXT "v=DMARC1; p=reject; rua=mailto:rua@brand.com; adkim=s; aspf=s"
│
└── mail.brand.com          ← marketing ESP (Klaviyo / Customer.io)
    SPF:    "v=spf1 include:_spf.klaviyo.com ~all"
    DKIM:   <klaviyo-selector>._domainkey.mail.brand.com TXT "v=DKIM1; ..."
    DMARC:  _dmarc.mail.brand.com TXT "v=DMARC1; p=quarantine; pct=100; rua=mailto:rua@brand.com; adkim=r; aspf=r"
```

Why subdomains? SPF mechanism limit (10 lookups). One subdomain = one ESP = small SPF. Two subdomains = two small SPF records. Two ESPs on parent domain = SPF likely overflows.

Parent domain DMARC governs subdomains via `sp=` flag:

```
_dmarc.brand.com.   TXT   "v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s; rua=mailto:rua@brand.com"
```

But subdomain explicit DMARC records OVERRIDE parent.

### Recipe 3: ESP per stream

```
Transactional ESP (choose one):
  - Resend          — modern dev-focused, React Email
  - Postmark        — deliverability-focused, sub-second median
  - SendGrid        — high-volume + automation
  - Amazon SES      — cheapest at scale (own reputation)
  - Mailgun         — EU residency option

Marketing ESP (choose one):
  - Klaviyo         — e-commerce / DTC default
  - Customer.io     — B2B / lifecycle / product-led
  - HubSpot         — B2B / Workflows tied to deal stage
  - Iterable        — enterprise cross-channel
  - Braze           — enterprise lifecycle
```

Why different ESPs? Specialization. Transactional ESPs (Resend, Postmark) optimize for sub-second delivery + 100% expected reach. Marketing ESPs (Klaviyo, Customer.io) optimize for segmentation + flow logic.

### Recipe 4: Set up notify.brand.com on Resend

```bash
# 1. Add domain in Resend dashboard
# 2. Resend gives DNS records to add:
notify.brand.com                TXT   "v=spf1 include:_spf.resend.com ~all"
notify.brand.com                MX    10  feedback-smtp.us-east-1.amazonses.com
resend._domainkey.notify.brand.com  TXT   "v=DKIM1; k=rsa; p=<key>"

# 3. Verify domain
curl -X GET "https://api.resend.com/domains/<domain-id>/verify" \
  -H "Authorization: Bearer $RESEND_API_KEY"

# 4. Configure strict DMARC on the subdomain
_dmarc.notify.brand.com.  TXT   "v=DMARC1; p=reject; rua=mailto:rua@brand.com; adkim=s; aspf=s"

# 5. Send from Resend with from=hello@notify.brand.com
curl -X POST "https://api.resend.com/emails" \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -d '{"from":"Brand <hello@notify.brand.com>","to":["u@x.com"],"subject":"...","html":"..."}'
```

### Recipe 5: Set up mail.brand.com on Klaviyo

```bash
# 1. Klaviyo Account → Settings → Domains → Add Sending Domain
# 2. Klaviyo issues DNS records — typically 3+ CNAMEs (DKIM, link tracking, etc.)
em1.mail.brand.com         CNAME   u<id>.<klaviyo-domain>
em2.mail.brand.com         CNAME   ...
k1._domainkey.mail.brand.com  CNAME   k1.k.<klaviyo-domain>
k2._domainkey.mail.brand.com  CNAME   k2.k.<klaviyo-domain>

# 3. SPF
mail.brand.com.            TXT     "v=spf1 include:_spf.klaviyo.com ~all"

# 4. DMARC (start at p=none; phase to p=quarantine then p=reject)
_dmarc.mail.brand.com.     TXT     "v=DMARC1; p=quarantine; pct=100; rua=mailto:rua@brand.com; adkim=r; aspf=r"

# 5. Klaviyo verifies and enables sending
```

### Recipe 6: Migration plan from single-domain to split

```markdown
# Migration: brand.com → notify.brand.com + mail.brand.com

## Phase 1 (Week 1-2): DNS prep
- [ ] Audit current senders. Classify each (Recipe 1).
- [ ] Choose transactional ESP and marketing ESP.
- [ ] Set up notify.brand.com DNS records (Recipe 4).
- [ ] Set up mail.brand.com DNS records (Recipe 5).
- [ ] Set DMARC at p=none for new subdomains (reporting only).
- [ ] Verify both ESPs see green DNS.

## Phase 2 (Week 3-4): Template + flow migration
- [ ] Migrate transactional templates to new ESP.
- [ ] QA each template in render testers (Litmus / EOA).
- [ ] Migrate marketing flows to new ESP.
- [ ] QA segmentation, flow logic, exit conditions.

## Phase 3 (Week 5-6): Cutover, low-volume first
- [ ] Switch low-volume transactional (e.g., admin notifications) to notify.brand.com.
- [ ] Monitor 48h — delivery rate, errors.
- [ ] Switch mid-volume (e.g., password resets) — monitor.
- [ ] Switch high-volume (order receipts) last.
- [ ] Concurrent: switch marketing campaigns to mail.brand.com.

## Phase 4 (Week 7-8): DMARC tightening
- [ ] Advance notify subdomain DMARC to p=reject (transactional should achieve 100% alignment easily).
- [ ] Advance mail subdomain DMARC to p=quarantine pct=100.
- [ ] Then mail to p=reject once 95%+ alignment confirmed.

## Phase 5 (Week 9+): Deprecate brand.com sends
- [ ] Audit: any remaining brand.com sends?
- [ ] Either migrate to subdomain or kill.
- [ ] Update brand.com DMARC to p=reject as final state.
```

### Recipe 7: Per-stream IP pool

For volume justifying dedicated IPs:

```bash
# Resend dedicated IP (Pro+ plan)
curl -X POST "https://api.resend.com/dedicated-ips" \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -d '{"region":"us-east-1"}'

# Klaviyo dedicated sending pool (Plus/Advanced)
# Contact Klaviyo support to provision dedicated IP for the marketing subdomain
```

### Recipe 8: Verify separation with dig + Klaviyo / Resend test

```bash
# Confirm distinct SPF
dig +short TXT notify.brand.com | grep spf1
# v=spf1 include:_spf.resend.com ~all

dig +short TXT mail.brand.com | grep spf1
# v=spf1 include:_spf.klaviyo.com ~all

# Confirm distinct DMARC
dig +short TXT _dmarc.notify.brand.com
dig +short TXT _dmarc.mail.brand.com

# Send test from each, inspect headers in receiver inbox
swaks --to test@gmail.com --from hello@notify.brand.com --server smtp.resend.com:587
swaks --to test@gmail.com --from hello@mail.brand.com --server smtp.klaviyo.com:587
```

### Recipe 9: BIMI per subdomain

If you want logo display in both transactional and marketing:

```
default._bimi.notify.brand.com.    TXT    "v=BIMI1; l=https://brand.com/logos/transactional.svg; a=https://brand.com/vmc.pem"
default._bimi.mail.brand.com.      TXT    "v=BIMI1; l=https://brand.com/logos/marketing.svg; a=https://brand.com/vmc.pem"
```

(Same VMC works if its Subject Alternative Names include both subdomains.)

### Recipe 10: One-click unsubscribe (RFC 8058)

For marketing stream only — transactional MUST NOT include unsubscribe:

```http
List-Unsubscribe: <mailto:unsubscribe@mail.brand.com>, <https://brand.com/u/abc123>
List-Unsubscribe-Post: List-Unsubscribe=One-Click
```

Klaviyo / Customer.io / HubSpot auto-add these on marketing streams.

## Examples

### Example 1: Full migration for $5M+ SaaS

**Goal:** receipts and password resets going to spam at Gmail; identified root cause is mixed sender.

**Steps:**

1. Audit. brand.com is sending: receipts (Stripe), magic links (Auth0), product newsletter (Mailchimp), promotional campaigns (Mailchimp). Mixed.
2. Plan:
   - notify.brand.com → Postmark (transactional: receipts + magic links + alerts)
   - mail.brand.com → Customer.io (marketing: newsletter + campaigns + lifecycle)
3. Provision DNS + ESPs per Recipes 4-5.
4. 8-week migration plan (Recipe 6).
5. Post-cutover: transactional median delivery time falls from 6s to 0.4s (Postmark median). Spam rate at Gmail drops below 0.05%.

### Example 2: Adding marketing to existing transactional-only stack

**Goal:** company is currently transactional-only on SES. Adding marketing campaigns.

**Steps:**

1. Continue SES on notify.brand.com for transactional.
2. Provision NEW subdomain mail.brand.com with new marketing ESP (Klaviyo).
3. Warm new IPs over 4-6 weeks (`ip-warming-strategy-dedicated-shared` skill).
4. Do NOT add Klaviyo SPF to notify.brand.com — keep streams isolated.
5. Tighten notify DMARC to p=reject since transactional should achieve 100% alignment.

## Edge cases

- **Classification gray zones** — "cart abandonment" can be argued either way. Industry default: marketing (opt-in lifecycle). Track via marketing stream.
- **Single ESP, two streams** — Postmark + SendGrid + Customer.io support stream separation within one account. Lower architectural overhead but reputation co-mingles. Better than nothing; worse than separate ESPs.
- **Apex domain sends** — emails from `@brand.com` (no subdomain) are problematic post-split. Consolidate to subdomains; reserve brand.com for corporate / website only.
- **DNS propagation time** — DKIM and SPF changes take 5min-48h to propagate globally. Test from multiple geographies.
- **Existing reputation on brand.com** — apex reputation doesn't transfer to subdomains. New subdomains start cold; warm them.
- **Forwarders** — if brand.com has email forwarding, those forwards may break SPF on the subdomain too. Audit forwarder behavior.
- **Brand consistency** — From-name should remain "Brand" across both streams; only domain differs. Don't confuse users with different sender names.
- **Privacy / GDPR** — physical address footer required on marketing; not on transactional. Make sure footer logic checks stream.
- **AMP for Email** — marketing only. Transactional support is limited and risky.
- **CASL (Canada)** — implied consent applies to transactional only when it's strictly transactional. Bake into Canadian-recipient targeting.

## Sources

- [Postmark: transactional vs marketing](https://postmarkapp.com/guides/separate-transactional-marketing)
- [Resend: marketing vs transactional](https://resend.com/blog/transactional-vs-marketing-email)
- [Klaviyo: transactional vs marketing](https://www.klaviyo.com/blog/transactional-vs-marketing-email)
- [Google sender guidelines](https://support.google.com/mail/answer/81126)
- [RFC 7489 (DMARC)](https://datatracker.ietf.org/doc/html/rfc7489)
- [RFC 8058 (one-click unsubscribe)](https://datatracker.ietf.org/doc/html/rfc8058)
- [Customer.io message-type docs](https://customer.io/docs/journeys/message-types/)
- [BIMI subdomain considerations](https://bimigroup.org/guidance-for-multiple-bimi-records/)
