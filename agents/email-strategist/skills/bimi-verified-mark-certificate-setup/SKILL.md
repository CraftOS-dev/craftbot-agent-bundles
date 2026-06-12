<!--
Source: https://bimigroup.org/ + DigiCert / Entrust VMC
BIMI displays brand logo in Gmail / Yahoo / Apple Mail / Fastmail.
Requires DMARC at quarantine/reject pct=100 + SVG Tiny PS + VMC.
-->
# BIMI + Verified Mark Certificate (VMC) Setup — SKILL

BIMI (Brand Indicators for Message Identification) displays your brand logo in supporting receivers' inbox. Hard requirements: DMARC at `p=quarantine` or `p=reject` with `pct=100`, an SVG Tiny PS profile logo, and a Verified Mark Certificate (VMC) from DigiCert ($1,500/yr) or Entrust ($1,800/yr).

## When to use

- "Set up BIMI for Gmail logo display"
- "Procure a VMC for our domain"
- "Why isn't our BIMI logo showing in Gmail / Apple / Yahoo?"
- "Validate our BIMI implementation"
- "Move from CMC to VMC (Apple's stricter requirement)"

Prerequisite: DMARC at `p=quarantine; pct=100` (minimum) or `p=reject`. If you're not there, use `deliverability-deep-spf-dkim-dmarc-bimi-arc` skill first.

## Setup

```bash
# CLI tools
brew install librsvg          # rsvg-convert for SVG inspection
npm i -g svg-validator        # SVG syntax check
pipx install svgcheck         # PSEUDO SVG checker — use BIMI Group's validator (web)
```

Online validators (no install):
- https://bimigroup.org/bimi-generator/ — generates the BIMI DNS record
- https://bimiinspector.com/?domain=brand.com — full audit
- https://www.brandindicators.org/ — overview
- https://easydmarc.com/tools/bimi-record-checker

VMC providers:
- DigiCert — https://www.digicert.com/tls-ssl/verified-mark-certificates ($1,499/yr)
- Entrust — https://www.entrust.com/products/certificate-solutions/verified-mark-certificates ($1,795/yr)

## Common recipes

### Recipe 1: Verify prerequisites with dig

```bash
DOMAIN="brand.com"

# DMARC must be quarantine or reject at pct=100
DMARC=$(dig +short TXT "_dmarc.${DOMAIN}" | tr -d '"')
echo "DMARC: $DMARC"
# Required: contains 'p=quarantine' OR 'p=reject', AND 'pct=100' (or no pct, which defaults to 100)

# SPF must exist
dig +short TXT "$DOMAIN" | grep -i 'v=spf1'

# DKIM (any selector signing your mail)
dig +short TXT "k1._domainkey.${DOMAIN}"
```

If `p=none` or `pct<100`, BIMI Inspector will fail. Fix DMARC first.

### Recipe 2: Prepare SVG Tiny PS logo

Requirements:
- **Profile:** SVG Tiny 1.2 with Portable/Secure (PS) restrictions
- **Aspect:** square (1:1), viewBox="0 0 X X"
- **Size:** ≤ 32 KB
- **No external references:** no `<script>`, no `<a>`, no external font URLs, no embedded raster (no `<image>` with href)
- **No animation:** no `<animate>`, no `<animateTransform>`, no `<set>`
- **Solid background OR transparent** (transparent is fine)
- **Centered** with safe padding

Validate locally:

```bash
# Inspect SVG structure
svg-validator logo.svg

# Check no disallowed elements
grep -E '<(script|a |animate|foreignObject|image )' logo.svg && echo "FAIL — disallowed element" || echo "OK"

# Check file size
wc -c logo.svg
# Should be < 32768
```

Use the BIMI Group validator for definitive check (web-only):
https://bimigroup.org/bimi-generator/

### Recipe 3: Host the SVG

```bash
# Host at HTTPS (HTTP not allowed)
# Must be reachable, CORS not required, MIME image/svg+xml

# Test
curl -I "https://brand.com/logo.svg"
# Expect: HTTP 200, content-type: image/svg+xml, content-length < 32768

# CDN tip — set far-future caching, immutable
```

### Recipe 4: Procure VMC from DigiCert

Process:

1. Visit https://www.digicert.com/tls-ssl/verified-mark-certificates
2. Provide:
   - Registered trademark (USPTO / UKIPO / EUIPO / JPO / IPO India / CIPA / IP Australia)
   - Domain ownership proof (DNS challenge or HTTP file)
   - Organization verification (D&B, articles of incorporation, etc.)
3. SVG logo upload — DigiCert validates against your trademark image (must visually match)
4. Wait 1-2 weeks for trademark vetting
5. Receive `vmc.pem` file (X.509 certificate chain)

Cost: $1,499/yr (DigiCert), $1,795/yr (Entrust). No volume discount.

### Recipe 5: Host the VMC PEM file

```bash
# Same HTTPS hosting as SVG
curl -I "https://brand.com/vmc.pem"
# Expect: HTTP 200, content-type: application/x-pem-file (or application/octet-stream)
```

### Recipe 6: Publish BIMI DNS TXT record

```
default._bimi.brand.com.    TXT    "v=BIMI1; l=https://brand.com/logo.svg; a=https://brand.com/vmc.pem"
```

Fields:
- `v=BIMI1` — version (currently only BIMI1)
- `l=` — logo URL (must be HTTPS SVG)
- `a=` — VMC certificate URL (must be HTTPS PEM)

Subdomain BIMI: separate record for `marketing.brand.com`, e.g.:

```
default._bimi.marketing.brand.com.    TXT    "v=BIMI1; l=https://brand.com/logos/marketing.svg; a=https://brand.com/vmc.pem"
```

(Same VMC works for parent + subdomains if domain SAN includes them.)

### Recipe 7: Apple's BIMI variant — Common Mark Certificate (CMC) vs VMC

Apple Mail (iOS 16+, macOS 13+) accepts:
- **VMC** — trademark-backed, full BIMI logo display
- **CMC** (Common Mark Certificate) — no trademark required, but Apple Mail shows logo with "?" indicator

Most senders go VMC for the unmarked logo display. CMC is for very-early-stage brands without registered trademarks.

### Recipe 8: Validate with BIMI Inspector

```bash
curl "https://api.bimigroup.org/v1/bimi-inspector?domain=brand.com&selector=default" \
  -H "Accept: application/json" | jq '.'
```

Or web UI: https://bimiinspector.com/?domain=brand.com

Expected:
```json
{
  "domain": "brand.com",
  "selector": "default",
  "dmarc": {"valid": true, "policy": "reject", "pct": 100},
  "svg": {"valid": true, "url": "https://brand.com/logo.svg", "size": 12345},
  "vmc": {"valid": true, "url": "https://brand.com/vmc.pem", "expires": "2027-06-09", "trademark": "REGISTERED"},
  "result": "PASS"
}
```

### Recipe 9: Live test in inbox

Send a test email from the BIMI-configured domain to:
- A Gmail inbox (gmail.com or Google Workspace) — logo shows in inbox list
- A Yahoo inbox (yahoo.com) — logo shows
- An Apple iCloud Mail inbox (icloud.com) — logo shows on iOS 16+ / macOS 13+
- A Fastmail inbox (fastmail.com) — logo shows

**Critical:** logos only show when the message passes DMARC at the active sender's domain. If you're sending from `mail.brand.com` but BIMI is published only at `brand.com` (with `sp=none`), Gmail won't display the subdomain logo without a subdomain BIMI record.

### Recipe 10: VMC renewal

VMC is annual. Calendar reminder 60 days before expiry. Renewal process: re-submit trademark proof + domain proof, re-issue PEM, update hosting. The DNS BIMI record doesn't change (URL stays same), only the PEM contents.

```bash
# Check VMC expiry
openssl x509 -in vmc.pem -noout -enddate
# notAfter=Jun  9 23:59:59 2027 GMT
```

## Examples

### Example 1: End-to-end BIMI setup for $5M+ brand

**Goal:** display brand logo in Gmail / Yahoo / Apple Mail for trust + recall.

**Steps:**

1. Verify DMARC at `p=quarantine; pct=100` or `p=reject`. If not, run phased rollout via `deliverability-deep-spf-dkim-dmarc-bimi-arc` first (4-8 weeks).
2. Procure registered trademark for the logo (if not already). USPTO process: 6-12 months, ~$300 filing fee. **Hard prerequisite.**
3. Produce SVG Tiny PS logo (Recipe 2). If your design team gives you a regular SVG, strip animations + external refs + scripts; export at 512x512 max.
4. Apply for VMC at DigiCert (Recipe 4). 1-2 weeks of trademark vetting.
5. While waiting: host SVG (Recipe 3). Validate dimensions + size.
6. Receive VMC PEM. Host (Recipe 5).
7. Publish DNS record (Recipe 6).
8. Validate with BIMI Inspector (Recipe 8). All-green.
9. Send live tests to Gmail / Yahoo / Apple / Fastmail (Recipe 9). Confirm logo renders.
10. Calendar 60-day-before-expiry reminder for renewal.

**Result:** brand logo visible in supported inboxes; estimated 10-30% open-rate lift (per BIMI Group case studies).

### Example 2: Troubleshoot "logo doesn't show in Gmail" complaint

**Goal:** diagnose missing BIMI display.

**Steps:**

1. Run BIMI Inspector (Recipe 8). Capture each field's status.
2. Common findings:
   - **DMARC pct < 100** → ramp pct to 100, wait 1 week, re-test.
   - **DMARC at sending subdomain is p=none** even if parent is p=reject → publish BIMI record at the sending subdomain.
   - **SVG fails Tiny PS profile** → re-export, strip animations/scripts/external refs.
   - **VMC expired** → renew + re-host PEM.
   - **VMC trademark mismatch** (DigiCert verifies logo matches trademark image) → coordinate with cert issuer.
   - **Logo file unreachable (404, HTTPS mismatch)** → fix hosting; verify with `curl -I`.
3. After fix, re-test in Gmail. Note: Gmail caches BIMI status for 24-48h; may need to wait.

## Edge cases

- **VMC trademark must be registered, not "in application"** — pending trademark applications don't qualify. Wait until issued.
- **VMC trademark vetting can fail** — if your logo materially differs from the trademark image (color, layout, text), DigiCert rejects. Re-apply with matching logo.
- **No VMC = no logo in Gmail/Apple** — Gmail and Apple require VMC. Yahoo accepted SVG-only briefly but tightened in 2023. CMC works only for Apple Mail with "?" indicator.
- **Domains with multiple sending subdomains** — each subdomain needs its own BIMI record OR explicit `sp=` policy + parent BIMI inheritance (varies by receiver, not universal).
- **SVG color profile** — sRGB required. Pantone / CMYK won't pass. Bake colors as hex.
- **Logo aspect 1:1** — non-square will be rejected. Pad with transparent if needed.
- **Apple Mail iOS 16+ shows the logo** — older iOS / macOS don't, even with valid BIMI. Affects ~5-10% of Apple Mail users until they upgrade.
- **Gmail in dark mode** — your SVG must look acceptable on dark background. Test! Use dark-friendly color or include subtle outline.
- **Multiple `default._bimi` records** — only one TXT record per selector. Publishing two breaks BIMI.
- **VMC takeover risk** — VMC is bound to your domain + trademark. If you transfer the domain mid-cycle, the VMC is invalidated; the new owner must procure their own.

## Sources

- [BIMI Group](https://bimigroup.org/)
- [BIMI specification (IETF draft)](https://datatracker.ietf.org/doc/draft-brand-indicators-for-message-identification/)
- [BIMI Inspector](https://bimiinspector.com/)
- [BIMI Generator](https://bimigroup.org/bimi-generator/)
- [DigiCert VMC](https://www.digicert.com/tls-ssl/verified-mark-certificates)
- [Entrust VMC](https://www.entrust.com/products/certificate-solutions/verified-mark-certificates)
- [Apple Common Mark Certificate](https://support.apple.com/en-us/HT213511)
- [Gmail BIMI guide](https://support.google.com/a/answer/10911321)
- [SVG Tiny 1.2 spec](https://www.w3.org/TR/SVGTiny12/)
- [Logo creation guide (BIMI Group)](https://bimigroup.org/creating-bimi-svg-logo-files/)
