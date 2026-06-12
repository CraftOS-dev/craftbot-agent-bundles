<!--
Source: https://www.trulyinbox.com/blog/spf-dkim-dmarc-email-deliverability/
Microsoft Outlook May 2025 mandate
Google/Yahoo Feb 2024 + Nov 2025 enforcement
-->
# Email Deliverability — SPF / DKIM / DMARC — SKILL

The 2024-2025 deliverability landscape — Google + Yahoo (Feb 2024), Microsoft Outlook (May 2025) — mandates SPF + DKIM + DMARC, one-click unsubscribe (RFC 8058), and complaint rate < 0.10% for 5K+/day senders. This skill runs the full audit via `dig` lookups + mail-tester.com + Postmark spam check + DMARC aggregate report parsing.

## When to use this skill

- **Pre-launch deliverability audit** before sending bulk email from a new domain.
- **Compliance check** for Google/Yahoo/Microsoft May 2025 mandate.
- **Ongoing monitor** — weekly DMARC aggregate report parsing.
- **Diagnosing inbox-placement issues** — emails going to spam/promotions.
- **DKIM rotation** — quarterly key rotation per best practice.
- **BIMI setup** — display brand logo in inbox.

**Do NOT use this skill when:**
- **Klaviyo / HubSpot built-in deliverability** dashboards — use those for ESP-side metrics.
- **Email content spam scoring** — Postmark spam check via this skill covers it.

## Setup

### Tools used

- `dig` (built into all Unix; available on Windows via PowerShell `Resolve-DnsName`)
- `curl` for mail-tester.com + Postmark spam check
- Optionally `dmarcian` or `dmarc-report-parser` for XML report parsing

### Mail-tester.com (sender reputation + content score)

```bash
# Free 3 tests/day, paid for more
# Method: send an email to the unique address mail-tester gives you, then poll the API
```

### Postmark spam check (content-only score)

```bash
# Free, unauth API
curl -X POST https://spamcheck.postmarkapp.com/filter \
  -H "Content-Type: application/json" \
  -d '{
    "email":"From: brand@yourbrand.com\nSubject: Test\n\nBody here",
    "options":"long"
  }'
```

## Common recipes

### Recipe 1: SPF check

```bash
dig TXT yourbrand.com +short | grep -i spf

# Expected output:
# "v=spf1 include:_spf.google.com include:mail.zendesk.com include:_spf.klaviyo.com ~all"
```

Audit:
- Must start with `v=spf1`
- All sending services included (ESP, transactional, support tool)
- Ends with `~all` (soft fail) or `-all` (hard fail) — `-all` is safer once stable
- Max 10 DNS lookups (count `include:` directives; each is 1 lookup; nested SPF chains)

Use https://www.kitterman.com/spf/validate.html for chain validation.

### Recipe 2: DKIM check

```bash
# Selector typically = "default", "google", "k1", "k2", or ESP-specific
# Klaviyo: klaviyo._domainkey
# Mailchimp: k1._domainkey
# Google Workspace: google._domainkey

dig TXT default._domainkey.yourbrand.com +short
# "v=DKIM1; k=rsa; p=MIIBIjANBgkqhki..."

# Per-ESP selectors
dig TXT klaviyo._domainkey.yourbrand.com +short
dig TXT google._domainkey.yourbrand.com +short
```

Audit:
- Key starts with `v=DKIM1`
- `p=` (public key) is non-empty (revoked keys = empty)
- 2048-bit RSA recommended (older 1024-bit still works but weaker)
- Key rotation every 6-12 months

### Recipe 3: DMARC check

```bash
dig TXT _dmarc.yourbrand.com +short
# "v=DMARC1; p=quarantine; pct=100; rua=mailto:dmarc@yourbrand.com; ruf=mailto:dmarc-forensic@yourbrand.com; adkim=s; aspf=s"
```

Audit:
- `v=DMARC1` first
- `p=` policy: `none` (monitor) → `quarantine` → `reject` (strict)
- `pct=100` — applies to all mail (start at 10 → 50 → 100 over weeks)
- `rua=mailto:...` for aggregate reports (REQUIRED for monitoring)
- `adkim=s` strict DKIM alignment (vs relaxed `r`)
- `aspf=s` strict SPF alignment

Recommended progression:
1. Week 1-2: `p=none; pct=100; rua=...` — monitor only
2. Week 3-4: `p=quarantine; pct=10; rua=...` — quarantine 10%
3. Week 5-6: `p=quarantine; pct=50`
4. Week 7+: `p=quarantine; pct=100` or `p=reject`

### Recipe 4: Full single-domain audit (script)

```bash
DOMAIN="yourbrand.com"

echo "=== SPF ==="
dig TXT "$DOMAIN" +short | grep -i spf || echo "MISSING"

echo "=== DKIM (common selectors) ==="
for sel in default google klaviyo k1 k2 selector1 selector2; do
  result=$(dig TXT "${sel}._domainkey.${DOMAIN}" +short)
  [ -n "$result" ] && echo "$sel: present" || echo "$sel: none"
done

echo "=== DMARC ==="
dig TXT "_dmarc.${DOMAIN}" +short || echo "MISSING (CRITICAL)"

echo "=== MX ==="
dig MX "$DOMAIN" +short

echo "=== BIMI (optional) ==="
dig TXT "default._bimi.${DOMAIN}" +short
```

### Recipe 5: Mail-tester.com API audit

```bash
# Step 1: Get test ID
TEST_ID=$(curl -s "https://www.mail-tester.com/get-test-id" | jq -r .test_id)
TEST_EMAIL="test-${TEST_ID}@srv1.mail-tester.com"
echo "Send test email to: $TEST_EMAIL"

# Step 2: Send a real test email from the ESP/domain you want to test
# (via Klaviyo single-send, HubSpot test send, or Postmark API)

# Step 3: Wait 30s, then fetch report
sleep 30
curl -s "https://www.mail-tester.com/${TEST_ID}&format=json" | jq '{
  score: .score,
  spf: .spf,
  dkim: .dkim,
  dmarc: .dmarc,
  blacklists: .blacklists,
  spamassassin_score: .spamassassin_score,
  content_issues: .content_issues
}'
```

Target: score >= 9/10.

### Recipe 6: Postmark spam check (content-only)

```bash
curl -X POST https://spamcheck.postmarkapp.com/filter \
  -H "Content-Type: application/json" \
  -d @- <<EOF
{
  "email": "From: brand@yourbrand.com\nTo: user@example.com\nSubject: Welcome!\n\nHi there,\n\n<body>",
  "options": "long"
}
EOF
```

Returns SpamAssassin-style score. Below 5 = good, 5-7 = borderline, > 7 = likely spam.

Common content red flags:
- ALL CAPS subject
- "FREE!" / "Limited time" / "Act now" / "Click here"
- Excessive exclamation marks
- "Re:" without actual thread
- Missing physical address
- Missing unsubscribe link
- Image-only emails

### Recipe 7: DMARC aggregate report parsing

DMARC reports arrive as XML attachments. Parse to find unauthorized senders:

```bash
# Install dmarc-report-parser (pip)
pip install dmarc-report-parser

# Parse a single report
dmarc-report-parser report.xml | jq '.[] | {
  source_ip: .source_ip,
  count: .count,
  spf_result: .spf.result,
  dkim_result: .dkim.result,
  disposition: .policy_evaluated.disposition
}'
```

Or use cloud service: https://dmarcian.com / https://dmarc.postmarkapp.com (free for low volume).

Investigate any IPs sending `spf_result=fail AND dkim_result=fail` — could be a forgotten service (shadow IT) or an attacker.

### Recipe 8: BIMI setup (logo in inbox)

```bash
# 1. Get VMC (Verified Mark Certificate) from CA — Entrust or DigiCert
# 2. Host SVG (Tiny Profile) at https://yourbrand.com/bimi/logo.svg
# 3. Add DNS record

# DNS:
default._bimi.yourbrand.com TXT "v=BIMI1; l=https://yourbrand.com/bimi/logo.svg; a=https://yourbrand.com/bimi/vmc.pem"
```

Requirements:
- DMARC at `p=quarantine` or `p=reject` AND `pct=100`
- VMC certificate ($1500+/year)
- SVG Tiny Profile format

Without VMC, "self-asserted" BIMI works in Yahoo / Apple Mail but not Gmail.

### Recipe 9: Compliance scorecard

```yaml
# yourbrand-deliverability-scorecard.yaml
date: 2026-06-09
domain: yourbrand.com

spf:
  present: true
  starts_with_v_spf1: true
  ends_with: "-all"
  dns_lookups_count: 6        # max 10
  includes:
    - _spf.google.com
    - _spf.klaviyo.com
    - mailgun.org
  status: PASS

dkim:
  selectors_present:
    - google: 2048-bit
    - klaviyo: 2048-bit
  status: PASS

dmarc:
  present: true
  policy: quarantine
  pct: 100
  rua_email: dmarc-aggregate@yourbrand.com
  ruf_email: dmarc-forensic@yourbrand.com
  alignment: strict
  status: PASS

google_postmaster_tools:
  configured: true
  spam_rate_last_7d: 0.04%   # < 0.10% target
  ip_reputation: HIGH
  domain_reputation: HIGH
  status: PASS

postmark_spam_check:
  score: 0.4
  status: PASS

mail_tester_score: 9.4/10

microsoft_smart_network_data_services:
  configured: true
  ip_reputation: GREEN
  status: PASS

one_click_unsub_rfc8058:
  list_unsubscribe_header: true
  list_unsubscribe_post_header: true
  status: PASS

physical_address_in_footer: true (CAN-SPAM)

bimi:
  configured: false           # optional
```

## Examples — full new-domain warmup

```yaml
new_domain_warmup:
  week_1:
    - sends_per_day: 50
    - target_audience: most_engaged (last 7d)
    - DMARC p=none, monitor
  week_2:
    - sends_per_day: 200
    - DMARC p=quarantine pct=10
  week_3:
    - sends_per_day: 1000
    - DMARC p=quarantine pct=50
  week_4:
    - sends_per_day: 5000
    - DMARC p=quarantine pct=100
  week_5+:
    - DMARC p=reject (optional but stronger)
    - Apply for BIMI VMC
    - Configure Google Postmaster + Microsoft SNDS
```

## Edge cases

### Multiple SPF records
DNS allows only ONE SPF record (`v=spf1`). If you have two, merge them. Common error after adding a new ESP — they tell you to add a TXT record, you do, but you already had one.

```bash
# WRONG (two records):
yourbrand.com TXT "v=spf1 include:_spf.google.com ~all"
yourbrand.com TXT "v=spf1 include:_spf.klaviyo.com ~all"

# CORRECT (merged):
yourbrand.com TXT "v=spf1 include:_spf.google.com include:_spf.klaviyo.com ~all"
```

### DNS lookup limit
SPF max 10 DNS lookups. Each `include:` is 1. Nested SPF chains add up. If hitting limit, use SPF macros or flatten via `spf-record-checker` services.

### DKIM key rotation
Rotate keys every 6-12 months. Process:
1. Generate new key in ESP (e.g., Klaviyo Settings → Email → DKIM)
2. Add new DNS record at `klaviyo2._domainkey.yourbrand.com`
3. Wait 24h for DNS propagation
4. Switch ESP to use new selector
5. After 7 days (in case of in-flight retries), remove old DNS record

### DMARC `p=reject` risks
Strict reject can drop legitimate mail from forwarders / mailing lists that strip DKIM signatures. Monitor `rua` reports for legit-but-failing mail; whitelist via DKIM-only.

### Subdomain policy
DMARC `sp=` for subdomain policy. If unset, defaults to `p`. For strict apex but lenient subdomain (e.g., `dev.yourbrand.com` test sends), set `sp=none`.

### Forwarding pitfalls
Mail forwarders (e.g., catchall@yourbrand.com → realuser@gmail.com) strip the original DKIM signature. Use ARC (Authenticated Received Chain) to preserve. Most managed ESPs handle this.

### Apple iCloud's hidden behavior
Apple iCloud Mail filters slightly differently than Gmail/Outlook — its filter is opaque. Test sends to a personal iCloud account quarterly.

### Compliance for 5K+/day senders
Per Google Feb 2024 + Nov 2025:
- SPF + DKIM aligned
- DMARC p=none minimum
- One-click unsubscribe (RFC 8058): `List-Unsubscribe-Post: List-Unsubscribe=One-Click`
- Spam complaint rate < 0.30% (strict at 0.10%)

Per Microsoft May 2025:
- Same as Google
- Outlook bounce reports more aggressive

### Microsoft SNDS / SNDS-Online
- Sign up: https://sendersupport.olc.protection.outlook.com/snds/
- Per-IP reputation (GREEN / YELLOW / RED)
- Spam complaint feedback loop

### One-click unsubscribe (RFC 8058)
Add BOTH headers:

```
List-Unsubscribe: <https://yourbrand.com/unsub?token=xxx>, <mailto:unsub@yourbrand.com?subject=unsub-xxx>
List-Unsubscribe-Post: List-Unsubscribe=One-Click
```

The POST endpoint must:
- Process unsub WITHOUT user interaction (no captcha, no confirmation page)
- Return 2xx within 5s

Klaviyo / HubSpot / Resend handle this natively.

## Sources

- **Deliverability overview**: https://www.trulyinbox.com/blog/spf-dkim-dmarc-email-deliverability/
- **Google sender requirements**: https://support.google.com/mail/answer/81126
- **Microsoft sender requirements**: https://learn.microsoft.com/en-us/exchange/mail-flow-best-practices/how-to-set-up-a-multifunction-device-or-application-to-send-email-using-microsoft-365-or-office-365
- **Yahoo sender requirements**: https://senders.yahooinc.com/best-practices/
- **RFC 8058 (one-click unsub)**: https://www.rfc-editor.org/rfc/rfc8058
- **DMARC.org**: https://dmarc.org/
- **BIMI**: https://bimigroup.org/
- **Mail-tester**: https://www.mail-tester.com/
- **Postmark spam check**: https://spamcheck.postmarkapp.com/
- **Google Postmaster Tools**: https://postmaster.google.com/
