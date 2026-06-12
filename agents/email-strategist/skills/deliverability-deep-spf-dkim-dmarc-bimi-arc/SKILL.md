<!--
Source: https://dmarcian.com/dmarc-deployment/ + trulyinbox.com
Full email auth: SPF + DKIM + DMARC + BIMI + ARC + MTA-STS + TLS-RPT.
Phased DMARC rollout. Google/Yahoo Feb 2024 + Microsoft May 2025 mandate.
-->
# Deliverability Deep — SPF / DKIM / DMARC / BIMI / ARC — SKILL

Full authentication audit + remediation. Phased DMARC rollout (`p=none` → `p=quarantine` → `p=reject`). ARC for forwarders. MTA-STS + TLS-RPT for transport. Mandatory for 5K+/day senders per Google + Yahoo Feb 2024 and Microsoft May 2025 enforcement.

## When to use

- "Audit our email authentication"
- "We're failing DMARC — diagnose"
- "Roll out DMARC for the first time"
- "Why are our emails going to spam at Gmail / Outlook / Yahoo"
- "We just got a 'less than 0.30% complaint rate' warning from Gmail"
- "Set up MTA-STS + TLS-RPT for transport security"
- "Add ARC for our forwarder so authentication isn't lost"

## Setup

```bash
# Core CLI deps — should be on any unix env
which dig openssl curl jq      # all required

# Optional helpers
brew install swaks             # SMTP test client
brew install dmarc-cat         # DMARC report viewer (formatted)
pipx install checkdmarc        # comprehensive auth audit
pipx install parsedmarc        # RUA/RUF report parser
```

Online tools (no install):
- mxtoolbox.com — blocklist + SPF/DKIM/DMARC check
- mail-tester.com — sender score (1-10)
- intodns.com — DNS sanity check
- dmarcian.com/dmarc-inspector — DMARC validation
- ondmarc.redsift.com — DMARC investigator
- mailhardener.com — full audit
- bimiinspector.com — BIMI check

## Common recipes

### Recipe 1: Full audit with `dig`

```bash
DOMAIN="brand.com"

# SPF
dig +short TXT "$DOMAIN" | grep -i 'v=spf1'

# DKIM — must know selectors (common: google, k1, selector1, ks1, default, mailo, em1, s1, s2, dkim, m1)
for sel in google k1 k2 selector1 selector2 default mailo em1 s1 s2 dkim m1 ks1 ks2 resend pm; do
  echo "=== $sel ==="
  dig +short TXT "${sel}._domainkey.${DOMAIN}" | head -1
done

# DMARC
dig +short TXT "_dmarc.${DOMAIN}"

# BIMI
dig +short TXT "default._bimi.${DOMAIN}"

# MTA-STS
dig +short TXT "_mta-sts.${DOMAIN}"
curl -s "https://mta-sts.${DOMAIN}/.well-known/mta-sts.txt"

# TLS-RPT
dig +short TXT "_smtp._tls.${DOMAIN}"

# MX
dig +short MX "$DOMAIN"
```

### Recipe 2: Validate SPF mechanism count + lookups

SPF spec limits to **10 DNS lookups**. Each `include:`, `a`, `mx`, `exists`, `ptr` counts. Exceed 10 → `permerror` → SPF fails.

```bash
# checkdmarc gives full SPF expansion + lookup count
checkdmarc "$DOMAIN"

# Or query the SPF flattener
curl -s "https://api.dmarcian.com/v1/spf/inspect?domain=${DOMAIN}" \
  -H "Authorization: Bearer $DMARCIAN_KEY" | jq '.lookup_count'
```

Fix when count > 10:
- Remove unused includes (legacy SendGrid? Old Mailchimp?)
- Flatten via SPF macro service (Valimail Monitor, Mimecast, ProofPoint)
- Subdomain delegation per ESP

### Recipe 3: DKIM key validation (size + alignment)

```bash
# Get DKIM record
dig +short TXT "k1._domainkey.${DOMAIN}" | tr -d '"' | tr -d ' '

# Inspect key
curl -s "https://dmarcian.com/api/dkim?selector=k1&domain=${DOMAIN}" \
  | jq '{key_size, key_type, valid}'

# Modern requirement: 2048-bit RSA (1024 acceptable but flagged)
openssl rsa -text -noout -pubin -in <(echo "-----BEGIN PUBLIC KEY-----"; \
  dig +short TXT k1._domainkey.${DOMAIN} | tr -d '"' | sed 's/v=DKIM1.*p=//' | tr -d '\n'; \
  echo "-----END PUBLIC KEY-----") 2>&1 | head -3
# RSA Public-Key: (2048 bit)
```

### Recipe 4: Test inbox placement at mail-tester

```bash
# Get a unique test address
TEST_ADDR=$(curl -s "https://www.mail-tester.com/" | grep -Eo 'test-[a-z0-9]+@srv1.mail-tester.com' | head -1)
echo "Send your draft to: $TEST_ADDR"

# After sending, fetch score:
TEST_ID=$(echo "$TEST_ADDR" | sed 's/@.*//')
curl -s "https://www.mail-tester.com/${TEST_ID}&format=json" | jq '.'
```

Score breakdown:
- 10/10 = clean
- 8-9 = minor issues
- < 7 = serious deliverability risk

### Recipe 5: Postmark Spam Check API (pre-send draft scoring)

```bash
EMAIL_RAW=$(cat <<EOF
From: Brand <hello@brand.com>
To: user@example.com
Subject: Your receipt for order #1234

Thank you for your purchase. View your order at https://brand.com/orders/1234.
EOF
)

curl -X POST "https://spamcheck.postmarkapp.com/filter" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d "{\"email\":$(echo "$EMAIL_RAW" | jq -Rs .),\"options\":\"long\"}"
```

Score < 5.0 ≈ inbox; ≥ 5.0 ≈ spam folder risk.

### Recipe 6: MXToolbox audit

```bash
curl -s "https://api.mxtoolbox.com/api/v1/lookup/blacklist/${DOMAIN}" \
  -H "Authorization: $MXTOOLBOX_KEY" | jq '.Failed[] | .Name'

curl -s "https://api.mxtoolbox.com/api/v1/lookup/dmarc/${DOMAIN}" \
  -H "Authorization: $MXTOOLBOX_KEY" | jq '.'
```

### Recipe 7: ARC validation (for forwarders)

ARC (RFC 8617) lets forwarders preserve original auth state. Critical when mailing-list software, custom forwarders, or relays sit between sender and final ISP.

```bash
# Send test mail through forwarder, inspect headers in receiving inbox
# Look for ARC-Authentication-Results + ARC-Message-Signature + ARC-Seal triplets

# Headers should chain (i=1, i=2, ...) for each hop
# Tools — Gmail does NOT show ARC headers in UI; download .eml and inspect
swaks --to user@gmail.com --from sender@${DOMAIN} \
  --server smtp.${DOMAIN} --header 'Subject: ARC test' \
  --body 'ARC chain test'
```

### Recipe 8: Phased DMARC rollout — DNS records

**Phase 1 — `p=none` with reporting (2-4 weeks):**

```
_dmarc.brand.com.   TXT   "v=DMARC1; p=none; rua=mailto:rua@brand.com; ruf=mailto:ruf@brand.com; fo=1; adkim=r; aspf=r; pct=100"
```

**Phase 2 — `p=quarantine; pct=10` (1-2 weeks):**

```
_dmarc.brand.com.   TXT   "v=DMARC1; p=quarantine; pct=10; rua=mailto:rua@brand.com; ruf=mailto:ruf@brand.com; fo=1; adkim=r; aspf=r"
```

**Phase 3 — ramp `pct=25 → 50 → 100`, each ~1-2 weeks if clean.**

**Phase 4 — final `p=reject`:**

```
_dmarc.brand.com.   TXT   "v=DMARC1; p=reject; rua=mailto:rua@brand.com; sp=reject; adkim=s; aspf=s; pct=100; fo=1"
```

Critical tags:
- `p=` — policy on failure (none / quarantine / reject)
- `pct=` — % of failing mail subject to policy
- `sp=` — subdomain policy
- `adkim=` / `aspf=` — alignment (s=strict, r=relaxed)
- `fo=` — failure-report options (1=any failure, d=DKIM, s=SPF, 0=both)

### Recipe 9: MTA-STS (Mail Transfer Agent Strict Transport Security)

Tell senders to require TLS to your MX. Defends against downgrade attacks.

```bash
# DNS record
_mta-sts.brand.com.    TXT    "v=STSv1; id=20260609T010000Z"

# Policy file at https://mta-sts.brand.com/.well-known/mta-sts.txt
cat <<EOF > /var/www/mta-sts/.well-known/mta-sts.txt
version: STSv1
mode: enforce
mx: mxa.brand.com
mx: mxb.brand.com
max_age: 604800
EOF
```

### Recipe 10: TLS-RPT (reports of TLS failures)

```
_smtp._tls.brand.com.    TXT    "v=TLSRPTv1; rua=mailto:tls-rpt@brand.com"
```

Receives daily JSON reports on TLS handshake failures from receivers that support TLS-RPT.

### Recipe 11: BIMI (requires DMARC quarantine/reject pct=100)

```
default._bimi.brand.com.    TXT    "v=BIMI1; l=https://brand.com/logo.svg; a=https://brand.com/vmc.pem"
```

See `bimi-verified-mark-certificate-setup` skill for VMC procurement.

## Examples

### Example 1: Email auth audit + remediation plan

**Goal:** establish current auth state and remediation backlog.

**Steps:**

1. Run full dig recipe (Recipe 1). Capture each record.
2. Run checkdmarc for full programmatic audit:
   ```bash
   checkdmarc brand.com -o audit.json
   jq '.spf, .dkim, .dmarc' audit.json
   ```
3. mxtoolbox.com — blocklist + SuperTool report.
4. mail-tester.com — actual send to test address from each ESP (Klaviyo, Resend, SendGrid).
5. Document in audit template (from role.md "Deliverability audit template").
6. Build remediation backlog: P0 (current failures), P1 (reputation risk), P2 (optimizations).

**Result:** prioritized backlog of DNS / ESP / template changes.

### Example 2: Phased DMARC rollout for 5K+/day sender

**Goal:** comply with Google + Yahoo Feb 2024 mandate; reach `p=reject` safely.

**Steps:**

1. Baseline: `dig TXT _dmarc.brand.com`. Likely `unconfigured`.
2. Publish `p=none` (Phase 1). Enroll in dmarcian or Postmark DMARC for free single-domain reporting.
3. Wait 2 weeks. Daily review of RUA reports:
   - Categorize each source IP cluster (legitimate ESP / third-party tool / forwarder / spoofing).
   - For each unaligned legitimate source, document fix (DKIM selector, SPF include, subdomain delegation).
4. Implement all alignment fixes. Re-check RUA reports for 1 week. Confirm 95%+ alignment for legitimate mail.
5. Ramp pct: 10 → 25 → 50 → 100 over ~6 weeks. Monitor delivery to your own seed inboxes at each step.
6. At `p=quarantine; pct=100` clean for 2 weeks → flip to `p=reject`.
7. Concurrent: set `sp=quarantine` (then `sp=reject`) on subdomains.

**Result:** full DMARC enforcement; spoof-resistant; compliant with major-provider mandates.

### Example 3: ARC for mailing-list forwarder

**Goal:** mailing-list software (Mailman / Discourse mail integration) breaks SPF when forwarding. Without ARC, DMARC fails at downstream receivers.

**Steps:**

1. Verify forwarder supports ARC signing. (Mailman 3+ does, Discourse depends on version.)
2. Configure forwarder to sign ARC headers as it relays.
3. Verify chain in delivered mail: ARC-Authentication-Results / ARC-Message-Signature / ARC-Seal with incrementing `i=` values.
4. Confirm Gmail / Outlook receivers honor the ARC chain (they do as of 2023+).

## Edge cases

- **SPF mechanism overflow** — > 10 lookups = `permerror`. Common culprit: stacked `include:` for multiple ESPs. Solution: per-subdomain ESPs (mail.brand.com → Klaviyo, notify.brand.com → Postmark) so each subdomain SPF is small.
- **DMARC `p=reject` cliff** — flipping straight to reject (skipping ramp) without remediation will reject legitimate mail. **Always ramp.**
- **DKIM 1024-bit deprecation** — Google flags 1024-bit DKIM as "weak"; some receivers reject. Upgrade to 2048.
- **DKIM key rotation breaks DMARC alignment** — when rotating, publish new selector first, sign with new selector for 7 days, then retire old. Don't delete old key until 7+ days after last signed mail.
- **`pct=` does NOT apply to `p=none`** — pct is meaningless for none. Pct gates how much failing mail is subject to the policy.
- **DMARC alignment `s` strict vs `r` relaxed** — `r` allows subdomain auth to satisfy parent-domain DMARC. `s` requires exact match. Most rollouts start with `r`; tighten to `s` only when sure.
- **`rua` mailbox capacity** — receiving DMARC reports from Google, Yahoo, Microsoft, Apple, AOL, etc. averages 5-50 emails/day per active domain. Use a dedicated mailbox; auto-archive after parse.
- **BIMI fail at `p=quarantine; pct=10`** — BIMI requires pct=100 + quarantine or reject. Inspector tools flag the pct violation clearly.
- **MTA-STS HTTP redirect breaks policy** — the policy file MUST be served over HTTPS at the exact URL `https://mta-sts.<domain>/.well-known/mta-sts.txt`. No redirects.
- **ARC alone won't save you** — ARC only preserves prior auth state; if original SPF / DKIM failed, ARC simply records the failure. Fix root auth first.

## Sources

- [DMARC.org spec](https://dmarc.org/overview/)
- [dmarcian deployment guide](https://dmarcian.com/dmarc-deployment/)
- [RFC 7489 (DMARC)](https://datatracker.ietf.org/doc/html/rfc7489)
- [RFC 8617 (ARC)](https://datatracker.ietf.org/doc/html/rfc8617)
- [RFC 8460 (TLS-RPT)](https://datatracker.ietf.org/doc/html/rfc8460)
- [RFC 8461 (MTA-STS)](https://datatracker.ietf.org/doc/html/rfc8461)
- [Google sender guidelines](https://support.google.com/mail/answer/81126)
- [Yahoo sender best practices](https://senders.yahooinc.com/best-practices/)
- [Microsoft sender enforcement](https://learn.microsoft.com/en-us/exchange/mail-flow-best-practices/email-authentication)
- [TrulyInbox SPF/DKIM/DMARC](https://www.trulyinbox.com/blog/spf-dkim-dmarc-email-deliverability/)
- [checkdmarc](https://github.com/domainaware/checkdmarc)
- [parsedmarc](https://github.com/domainaware/parsedmarc)
