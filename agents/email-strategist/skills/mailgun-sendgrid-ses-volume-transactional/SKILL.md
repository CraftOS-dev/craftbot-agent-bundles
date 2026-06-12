<!--
Source: SendGrid v3 + Mailgun + Amazon SES + Mailchannels + SparkPost
High-volume transactional. SES is cheapest at scale (own reputation).
Mailgun: EU residency. SendGrid: Subuser caps + automation features.
-->
# High-Volume Transactional (Mailgun / SendGrid / SES) — SKILL

For transactional volumes ≥ 1M emails/month. SES is cheapest at scale ($0.10 per 1k) but lower default deliverability — you manage reputation. Mailgun offers EU residency. SendGrid offers Subuser caps + automation. Choose by volume + region + complexity needs.

## When to use

- "Send 10M emails/month transactionally — minimize cost"
- "Need EU data residency for transactional"
- "Multi-tenant SaaS — per-customer sending caps with separate reputation"
- "Build own reputation on dedicated IPs at scale"
- "SES dedicated IP pools for warm/separate flows"

Do **not** use for: low volume (< 100K/mo — Resend/Postmark are easier); marketing campaigns (use Klaviyo/Customer.io); newsletter platforms (Beehiiv).

## Setup

### Amazon SES

```bash
# AWS CLI
aws ses verify-domain-identity --domain notify.brand.com
aws ses verify-domain-dkim --domain notify.brand.com    # returns 3 selector tokens
aws ses get-account-sending-enabled                     # confirm prod (not sandbox)

# Move out of sandbox: open support ticket — typical 24h approval
```

DNS:
```
# 3 DKIM selector CNAMEs (SES gives you these)
<token1>._domainkey.notify.brand.com  CNAME  <token1>.dkim.amazonses.com
<token2>._domainkey.notify.brand.com  CNAME  <token2>.dkim.amazonses.com
<token3>._domainkey.notify.brand.com  CNAME  <token3>.dkim.amazonses.com

# SPF
notify.brand.com  TXT  "v=spf1 include:amazonses.com ~all"

# Custom MAIL FROM (for SPF alignment)
mail.notify.brand.com  MX  10  feedback-smtp.us-east-1.amazonses.com
mail.notify.brand.com  TXT "v=spf1 include:amazonses.com ~all"
```

### Mailgun

```bash
# Sign up at mailgun.com, add domain
export MAILGUN_API_KEY="key-<your-key>"   # https://app.mailgun.com/app/account/security/api_keys
export MAILGUN_DOMAIN="notify.brand.com"
export MAILGUN_REGION="us"                # or "eu"
```

DNS — Mailgun shows in dashboard:
```
mailo._domainkey.<domain>  TXT  "v=DKIM1; k=rsa; p=<key>"
<domain>                   TXT  "v=spf1 include:mailgun.org ~all"
email.<domain>             MX   10  mxa.mailgun.org
email.<domain>             MX   10  mxb.mailgun.org
```

### SendGrid

```bash
export SENDGRID_API_KEY="SG.<your-key>"   # https://app.sendgrid.com/settings/api_keys
```

DNS — domain auth in dashboard generates:
```
em<n>.<domain>   CNAME u<id>.wl.sendgrid.net
s1._domainkey.<domain>  CNAME s1.domainkey.u<id>.wl.sendgrid.net
s2._domainkey.<domain>  CNAME s2.domainkey.u<id>.wl.sendgrid.net
```

## Common recipes

### Recipe 1: SES — send via API (cheapest at scale)

```bash
# Via aws CLI (uses your credential chain)
aws sesv2 send-email \
  --from-email-address "Brand <hello@notify.brand.com>" \
  --destination "ToAddresses=user@example.com" \
  --content '{
    "Simple": {
      "Subject": {"Data":"Your receipt","Charset":"UTF-8"},
      "Body": {"Html":{"Data":"<h1>Thanks!</h1>","Charset":"UTF-8"}}
    }
  }'
```

### Recipe 2: SES — dedicated IP pool (for high-volume reputation isolation)

```bash
# Create pool
aws sesv2 create-dedicated-ip-pool --pool-name marketing-pool --scaling-mode MANAGED

# Allocate dedicated IPs
aws sesv2 put-dedicated-ip-in-pool --ip <ip> --destination-pool-name marketing-pool

# Set up configuration set bound to pool
aws sesv2 create-configuration-set \
  --configuration-set-name marketing-config \
  --delivery-options "SendingPoolName=marketing-pool,TlsPolicy=REQUIRE"

# Send via config set
aws sesv2 send-email \
  --configuration-set-name marketing-config \
  --from-email-address "..." \
  --destination "ToAddresses=user@example.com" \
  --content '{...}'
```

### Recipe 3: Mailgun — send via REST

```bash
curl -X POST "https://api.mailgun.net/v3/$MAILGUN_DOMAIN/messages" \
  --user "api:$MAILGUN_API_KEY" \
  -F from="Brand <hello@notify.brand.com>" \
  -F to="user@example.com" \
  -F subject="Your receipt" \
  -F html="<h1>Thanks!</h1>" \
  -F "o:tag=receipt" \
  -F "o:tracking=yes" \
  -F "o:tracking-clicks=htmlonly"

# EU region: change to https://api.eu.mailgun.net/v3/...
```

### Recipe 4: Mailgun — validate email at signup

```bash
curl "https://api.mailgun.net/v4/address/validate?address=user@example.com" \
  --user "api:$MAILGUN_API_KEY"
```

Returns: deliverability score, role-address flag, disposable-domain flag. Use inline at signup to reject typos.

### Recipe 5: SendGrid — send with categories + custom args

```bash
curl -X POST "https://api.sendgrid.com/v3/mail/send" \
  -H "Authorization: Bearer $SENDGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "personalizations": [{
      "to":[{"email":"user@example.com"}],
      "custom_args":{"order_id":"1234"}
    }],
    "from": {"email":"hello@notify.brand.com","name":"Brand"},
    "subject": "Your receipt",
    "content": [{"type":"text/html","value":"<h1>Thanks!</h1>"}],
    "categories": ["receipt","transactional"],
    "tracking_settings": {
      "click_tracking": {"enable": true,"enable_text":false},
      "open_tracking": {"enable": true}
    }
  }'
```

### Recipe 6: SendGrid Subuser — multi-tenant SaaS pattern

For SaaS that sends on behalf of customers, create one Subuser per tenant for separate reputation + caps:

```bash
# Create subuser
curl -X POST "https://api.sendgrid.com/v3/subusers" \
  -H "Authorization: Bearer $SENDGRID_API_KEY" \
  -d '{
    "username":"tenant-acme",
    "email":"billing+acme@brand.com",
    "password":"<random-secure-pw>",
    "ips":["<dedicated-ip>"]
  }'

# Per-subuser send: use subuser API key, or impersonate
curl -X POST "https://api.sendgrid.com/v3/mail/send" \
  -H "Authorization: Bearer $SUBUSER_API_KEY" \
  -d '{...}'

# Throttle: subuser monthly cap
curl -X PUT "https://api.sendgrid.com/v3/subusers/tenant-acme/monitor" \
  -H "Authorization: Bearer $SENDGRID_API_KEY" \
  -d '{"email":"ops@brand.com","frequency":10000}'
```

### Recipe 7: SES Receipt-Rule + S3 for inbound

```bash
# Create receipt rule that drops inbound to S3 + Lambda
aws ses create-receipt-rule \
  --rule-set-name default-rule-set \
  --rule '{
    "Name":"inbound-replies",
    "Enabled":true,
    "TlsPolicy":"Require",
    "Recipients":["replies@notify.brand.com"],
    "Actions":[
      {"S3Action":{"BucketName":"brand-inbound-mail","ObjectKeyPrefix":"replies/"}},
      {"LambdaAction":{"FunctionArn":"arn:aws:lambda:...:fn:process-reply"}}
    ]
  }'
```

### Recipe 8: SES bounce + complaint feedback via SNS

```bash
# Set up SNS topic; configure config set to publish events
aws sns create-topic --name ses-events
aws sesv2 put-configuration-set-event-destination \
  --configuration-set-name marketing-config \
  --event-destination-name sns-events \
  --event-destination '{
    "Enabled":true,
    "MatchingEventTypes":["BOUNCE","COMPLAINT","DELIVERY","SEND","REJECT","RENDERING_FAILURE"],
    "SnsDestination":{"TopicArn":"arn:aws:sns:us-east-1:<acct>:ses-events"}
  }'

# Subscribe Lambda or SQS to topic for processing
```

### Recipe 9: Mailgun routes (inbound + forwarding)

```bash
curl -X POST "https://api.mailgun.net/v3/routes" \
  --user "api:$MAILGUN_API_KEY" \
  -F expression="match_recipient('support@notify.brand.com')" \
  -F action='forward("https://brand.com/inbound/mailgun")' \
  -F action="stop()" \
  -F priority=10
```

### Recipe 10: Cost compare (per 1K emails)

```
| ESP      | $/1K | EU residency | Dedicated IP cost |
|----------|------|--------------|-------------------|
| SES      | 0.10 | yes (region) | $24.95/mo        |
| Mailgun  | 0.80 | yes          | $59/mo            |
| SendGrid | 1.20 | no           | $80/mo            |
| Mailchannels | 0.40 | partial  | included on paid  |
| SparkPost | 0.90 | yes        | $99/mo            |
```

At 10M/mo: SES $1K, Mailchannels $4K, Mailgun $8K, SparkPost $9K, SendGrid $12K.

## Examples

### Example 1: Migrate 10M/mo transactional from SendGrid to SES

**Goal:** save ~$11K/mo vs SendGrid.

**Steps:**

1. Verify domain + DKIM in SES (Setup above).
2. Request production access (move out of sandbox) — AWS support ticket, 24h.
3. Request initial sending quota increase (default is 50K/24h after sandbox).
4. Allocate 2 dedicated IPs to start (warm second pool concurrently).
5. Set up config set with dedicated pool + SNS event destination (Recipe 2 + 8).
6. Migrate templates from SendGrid Handlebars to SES Mustache-equivalent.
7. Dual-send 7d (90% SendGrid, 10% SES) to confirm parity.
8. Ramp SES to 50% → 90% → 100% over 2-3 weeks.
9. Monitor `ipReputation` + complaint via Google Postmaster (separate skill).
10. Cancel SendGrid plan.

**Result:** $11K+/mo savings; own reputation on dedicated IPs.

### Example 2: Multi-tenant SaaS sends on behalf of 500 customer brands

**Goal:** isolated reputation per customer; per-customer caps.

**Steps:**

1. Choose SendGrid (Subuser model is best for this pattern).
2. Per onboarding customer, create Subuser (Recipe 6) + dedicated IP if usage > 100K/mo.
3. Set monthly Subuser caps for billing limits.
4. Per-customer DNS: customer adds CNAME records for DKIM (SendGrid generates per-domain auth).
5. Per-customer webhook for events.
6. Centralized observability: collect all subuser stats via SendGrid Stats API daily.

## Edge cases

- **SES sandbox** — out of the box, accounts are in sandbox: can only send to verified addresses, max 200/day. Production access takes 24-48h. Plan migrations with this lead time.
- **SES requires you manage reputation** — unlike SendGrid / Postmark / Resend, SES does NOT auto-suspend on bounce/complaint spikes. You must build the monitoring + suppression yourself.
- **SES suppression list** — global account-wide suppression for bounces/complaints. Inspect via `aws sesv2 list-suppressed-destinations`.
- **Mailgun EU vs US** — URL path differs (`api.mailgun.net` vs `api.eu.mailgun.net`). Mixing returns 404 with confusing error.
- **SendGrid 1000-recipient limit per `personalizations` array** — for batching above that, multiple API calls.
- **SendGrid IP warmup automation** — they offer automated warmup; let it run, don't manually override (you'll trash the schedule).
- **Mailgun rate limits per domain** — default 600/min on free tier, 100K/min on paid. Burst spikes hit 429.
- **SES rate limits** — start at 1 req/s + 200/day; production grants typically 14 req/s + 50K/day. Request higher caps as needed.
- **Mailchannels** — gaining mindshare for Cloudflare Workers (free tier for some Workers customers). Not ideal for transactional reliability if you need SLA.
- **All three (SES/Mailgun/SendGrid)** — explicit anti-spam policy. Marketing content with high complaint rates suspends accounts. Use proper marketing ESPs.

## Sources

- [SendGrid v3 API](https://docs.sendgrid.com/api-reference)
- [Mailgun API](https://documentation.mailgun.com/)
- [Amazon SES Developer Guide](https://docs.aws.amazon.com/ses/)
- [SES dedicated IP pools](https://docs.aws.amazon.com/ses/latest/dg/dedicated-ip.html)
- [Mailchannels API](https://docs.mailchannels.net/)
- [SparkPost API](https://developers.sparkpost.com/api/)
- [SendGrid Subuser API](https://docs.sendgrid.com/api-reference/subusers-api)
