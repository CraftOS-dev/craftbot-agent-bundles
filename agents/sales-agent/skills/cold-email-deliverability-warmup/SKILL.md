<!--
Source: https://www.mail-tester.com/ + https://lemwarm.com/ + https://glockapps.com/
Cold email deliverability + sender warmup (June 2026 SOTA).
-->
# Cold Email Deliverability + Warmup — SKILL

Before a single cold email goes out, the sending domain has to pass authentication (SPF / DKIM / DMARC), warm up for 4-6 weeks, and stay below the complaint-rate cliff (<0.10%). This skill is the pre-launch + ongoing-hygiene workflow: validate DNS, warm the domain, test inbox placement, monitor blocklists, and tune daily volume so the inbox-placement-rate stays above 80%.

## When to use

- **Setting up a new cold-outbound domain** (`brand-go.com`, `try-brand.com` — never the primary transactional domain).
- **Diagnosing a deliverability drop** — open-rate or reply-rate collapsed; check authentication + reputation before blaming the copy.
- **Pre-launch checklist** for any campaign in `outreach-salesloft-sequences`.
- **Weekly hygiene** — monitor complaint rate, bounce rate, blocklist status, postmaster reputation.
- **Trigger phrases**: "set up SPF / DKIM / DMARC", "warmup my new domain", "why are emails going to spam", "check deliverability", "mail-tester score", "domain reputation check".

Do NOT use this skill for: **transactional email setup** (use Resend / Postmark / SES — different deliverability rules); **content-side fixes** (subject-line / spam-trigger words — those belong in the sequence design); **non-email channels** (LinkedIn / SMS / phone — see other skills).

## Setup

```bash
# Core tools — all CLI-native, no auth needed
which dig             # comes with bind-utils / dnsutils on macOS + Linux
which curl
which jq

# Optional paid tools (highly recommended for production)
# Lemwarm — $29/mo per mailbox, 4-6 week warmup
export LEMWARM_API_KEY="<key>"      # lemlist account, Lemwarm add-on
# Mailwarm — $69/mo, similar warmup
# Instantly's built-in warmup — included in $30/mo workspace add-on
# Smartlead warmup — built into platform
export MAILTESTER_API_KEY="<key>"   # mail-tester.com paid plan: $14-72/mo for API
export GLOCKAPPS_API_KEY="<key>"    # GlockApps: $59-199/mo for inbox-placement testing
```

DNS access requirement:
- You need write access to the DNS for your cold-outbound domain (registrar or DNS host like Cloudflare, Route 53, GoDaddy).
- Domain age: register the domain **30+ days** before any send; warmed-but-newborn domains still get filtered.

## Common recipes

### Recipe 1: Verify SPF / DKIM / DMARC for a domain

```bash
DOMAIN="brand-go.com"

# SPF — should end in ~all or -all
dig +short TXT "$DOMAIN" | grep -i "v=spf1"

# DKIM — selector varies by ESP (default, google, k1, s1, etc.); try common ones
for selector in default google k1 s1 selector1 selector2; do
  echo "=== $selector ==="
  dig +short TXT "${selector}._domainkey.${DOMAIN}"
done

# DMARC — must exist; p=quarantine minimum, p=reject ideal; rua= reporting
dig +short TXT "_dmarc.${DOMAIN}"
```

Expected output:
- SPF: `"v=spf1 include:_spf.google.com include:sendgrid.net ~all"`
- DKIM: `"v=DKIM1; k=rsa; p=MIIBIjANBgkq..."` (the p= key, 2048-bit minimum)
- DMARC: `"v=DMARC1; p=quarantine; rua=mailto:dmarc@brand.com; sp=quarantine; aspf=s; adkim=s"`

### Recipe 2: Add SPF / DKIM / DMARC (Cloudflare example)

```bash
# SPF record (one TXT at apex)
# Name: @  Value: v=spf1 include:_spf.google.com include:mailchannels.net include:amazonses.com ~all

# DKIM (selector + key from your ESP — Google Workspace, SendGrid, Postmark, etc.)
# Name: google._domainkey  Value: v=DKIM1; k=rsa; p=<base64-key-from-ESP>

# DMARC (one TXT at _dmarc subdomain)
# Name: _dmarc  Value: v=DMARC1; p=quarantine; rua=mailto:dmarc@brand.com; pct=100

# Wait 1-24h for DNS to propagate, then re-run Recipe 1
```

DMARC policy progression:
1. **Week 1**: `p=none; rua=mailto:dmarc@brand.com` (monitor-only).
2. **Week 2-4**: review `rua` aggregate reports; fix any unauthorized senders.
3. **Week 5+**: ramp to `p=quarantine; pct=25` → `pct=50` → `pct=100`.
4. **Long-term**: `p=reject` (best protection, do only after weeks of clean reports).

### Recipe 3: mail-tester.com score check

```bash
# Step 1: Get the unique tester address
RESPONSE=$(curl -s "https://api.mail-tester.com/v2/test?api_token=$MAILTESTER_API_KEY")
TEST_ID=$(echo "$RESPONSE" | jq -r '.id')
TEST_EMAIL=$(echo "$RESPONSE" | jq -r '.email')

# Step 2: send your test email FROM the warmup domain TO that address
# (Use your sequence platform's "send test" or a manual send from a connected mailbox.)

# Step 3: poll for the score (mail-tester needs ~30s to grade)
sleep 60
curl -s "https://api.mail-tester.com/v2/test/$TEST_ID?api_token=$MAILTESTER_API_KEY" | \
  jq '{score: .score, max: .max, breakdown: .checks}'
```

Score interpretation:
- **9-10/10**: ship it.
- **7-8.5/10**: fix the largest score-loss items first (usually SPF/DKIM/DMARC or text-to-html ratio).
- **< 7/10**: do not launch. Common fixes: add DMARC, remove `<img>` tracking pixel from Touch 1, drop link count to 1 max, plain-text only first email.

### Recipe 4: Blocklist check (MXToolbox)

```bash
# No API key needed for the basic check; use the web UI for full report
DOMAIN_IP=$(dig +short A mail.brand-go.com | head -1)
curl -s "https://api.mxtoolbox.com/api/v1/lookup/blacklist/${DOMAIN_IP}" \
  -H "Authorization: <mxtoolbox-key>" | jq '.Failed'
```

Major lists to check: SBL, CBL, Spamhaus DBL, Barracuda, SORBS, UCEPROTECT. If listed → do NOT send; submit delist request to the listing org and wait.

### Recipe 5: Lemwarm warmup setup (4-6 weeks)

```bash
# Step 1: Create a warmup-only mailbox profile in lemlist UI (or API).
curl -X POST "https://api.lemlist.com/api/warmup" \
  -u ":$LEMWARM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email":"sender1@brand-go.com",
    "smtp":{"host":"smtp.gmail.com","port":587,"user":"sender1@brand-go.com","pass":"<app-password>"},
    "imap":{"host":"imap.gmail.com","port":993,"user":"sender1@brand-go.com","pass":"<app-password>"},
    "rampupVolume":40,
    "maxDailyVolume":150,
    "rampupDays":28
  }'
```

Lemwarm exchanges emails with a network of ~10k other warming inboxes, replying + marking-as-not-spam to build sender reputation.

### Recipe 6: Daily volume ramp schedule (any tool)

```python
# Per role.md domain warmup table
SCHEDULE = [
    ("Week 1", 10, 20, "100% warmup peers"),
    ("Week 2", 30, 50, "90% warmup / 10% real engaged"),
    ("Week 3", 50, 80, "70% warmup / 30% real engaged"),
    ("Week 4", 80, 100, "50% warmup / 50% real cold"),
    ("Week 5+", 100, 150, "30% warmup / 70% real cold (cap and hold)"),
]
```

Hold at 100-150/day per mailbox. Do NOT scale above 200/day per mailbox — Gmail/Microsoft both flag aggressive senders at that range.

### Recipe 7: Google Postmaster Tools (reputation monitoring)

```bash
# UI only — no public API. Set up at https://postmaster.google.com/
# Add your domain, verify ownership via DNS TXT record, then daily check:
# - Domain reputation: High / Medium / Low / Bad
# - IP reputation
# - Authentication pass rate (SPF/DKIM/DMARC)
# - Spam complaint rate (must be < 0.30%, target < 0.10%)
# - Encryption pass rate
```

Bad / Low reputation → pause cold sends immediately; investigate complaint sources, unsubscribe handling, list hygiene.

### Recipe 8: GlockApps inbox placement test

```bash
# Step 1: Create a test
RESP=$(curl -X POST "https://api.glockapps.com/api/v1/tests" \
  -H "Authorization: Bearer $GLOCKAPPS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"Q3 Cold Test","seedlist":"full"}')

# Step 2: send your test email to the seedlist addresses returned
# Step 3: poll results
curl "https://api.glockapps.com/api/v1/tests/<test-id>/results" \
  -H "Authorization: Bearer $GLOCKAPPS_API_KEY" | \
  jq '{
    gmail_inbox: .results.Gmail.inbox_pct,
    outlook_inbox: .results.Outlook.inbox_pct,
    yahoo_inbox: .results.Yahoo.inbox_pct
  }'
```

Targets: Gmail inbox > 80%, Outlook inbox > 70%, Yahoo inbox > 75%. Below those → diagnose with Postmaster Tools + mail-tester.

### Recipe 9: Suppression list hygiene (prevent complaints)

```bash
# Pre-launch suppression must include:
# 1. Hard-bounced addresses (auto-suppressed by sender platform — verify it's on)
# 2. Unsubscribed (auto-suppressed)
# 3. Customers / Closed-Won contacts (pull from CRM, manually add)
# 4. Competitors + competitor employees (manual)
# 5. Do-Not-Contact list (manual)
# 6. Spam-trap lookalike domains (use Hunter or NeverBounce verify before send)

# Example: pull customer emails from HubSpot, add to Instantly blocklist
curl -X POST "https://gateway.maton.ai/instantly/api/v2/blocklist" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{"emails":["customer1@x.com","customer2@y.com"],"reason":"closed-won customer"}'
```

### Recipe 10: Complaint-rate monitoring (daily cron)

```python
# Pull yesterday's campaign stats from Instantly + check thresholds
import requests, os
r = requests.get("https://gateway.maton.ai/instantly/api/v2/campaigns/<id>/analytics?date_from=yesterday&date_to=yesterday",
                 headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"})
d = r.json()
complaint_rate = d["complaints"] / max(d["sent"], 1)
bounce_rate = d["bounces"] / max(d["sent"], 1)
reply_rate = d["replies"] / max(d["sent"], 1)

if complaint_rate > 0.001:   # 0.10%
    print("ALERT: complaint rate exceeded 0.10% — pause campaign")
if bounce_rate > 0.02:       # 2.0%
    print("ALERT: bounce rate exceeded 2.0% — re-verify list with Hunter/NeverBounce")
if reply_rate < 0.02 and d["sent"] > 200:
    print("WARN: reply rate below 2.0% — copy/targeting likely off")
```

Wire this to `slack-mcp` for daily ops alerts.

## Examples

### Example 1: Cold-domain launch from zero

**Goal:** New domain `brand-go.com` ready for 100/day per mailbox sends in 5 weeks.

**Steps:**
1. **Day -30**: Register the domain. Set up DNS (Recipe 2) with SPF, DKIM, DMARC `p=none`. Set up 2 mailboxes (`alex@`, `morgan@`) in Google Workspace.
2. **Day -28**: Connect mailboxes to Lemwarm (Recipe 5). Start at 10/day, ramp +5/day until day 7.
3. **Day -21**: Mail-tester (Recipe 3) — must be 9+/10. Fix if not.
4. **Day -14**: Postmaster Tools check (Recipe 7) — reputation should be "Medium" or higher.
5. **Day -7**: GlockApps placement test (Recipe 8) — Gmail inbox > 70%.
6. **Day 0**: Launch first cold campaign at 50/day per mailbox, daily volume monitored (Recipe 10).
7. **Day +14**: If complaint < 0.10%, bounce < 2%, reply > 2% → scale to 100/day per mailbox.

**Result:** Production-ready cold-outbound domain with 200/day capacity across 2 mailboxes.

### Example 2: Diagnose deliverability collapse

**Goal:** Reply rate dropped 70% week-over-week. Find root cause.

**Steps:**
1. Recipe 1 — re-verify SPF/DKIM/DMARC still resolving. Common: a Cloudflare proxy got turned on, DNS started returning 404 to mail providers.
2. Recipe 4 — check blocklists. If listed → identify cause (volume spike, bad list, sudden subject change).
3. Recipe 7 — Postmaster Tools. If reputation dropped to "Low" → check spam complaints in the same period.
4. Recipe 3 — re-run mail-tester. If now <8/10 vs previously 9+, a template change introduced spam triggers.
5. Recipe 8 — GlockApps. If Gmail inbox dropped from 85% to 35% but Outlook is fine → Gmail-specific reputation issue.
6. Pause sends until score recovers.

**Result:** Root cause identified within 30 min; targeted fix instead of guessing.

## Edge cases / gotchas

- **Never cold-send from your primary domain.** Use `brand-go.com` / `try-brand.com` / `hello-brand.com` — secondary domains absorb reputation hits without affecting `brand.com` transactional email.
- **DKIM key rotation breaks things.** When your ESP rotates keys, the old selector goes 404; mail starts failing DKIM. Monitor DMARC `rua` reports for SPF/DKIM failures.
- **SPF `~all` (softfail) vs `-all` (hardfail)** — start with `~all` during setup, move to `-all` after 30 days of clean DMARC reports. `-all` is stricter but rejects spoofers outright.
- **Domain age trumps warmup.** Brand-new domains (< 30 days) get filtered even with perfect warmup. Buy or register 30+ days before first send.
- **Gmail's MPP (Mail Privacy Protection)** inflates open-rate as Apple Mail clients pre-fetch images. Treat open-rate as directional only; reply-rate is the only real-truth metric post-2021.
- **Microsoft / Outlook is the hardest provider.** Office 365 / Outlook.com block aggressively; if your TAM is Microsoft-shop, double the warmup duration and accept ~10pp lower placement.
- **Yahoo + AOL** require DMARC `p=quarantine` or `p=reject` since Feb 2024 — emails from `p=none` domains land in spam by default.
- **Suppression must cascade**: customers, opt-outs, hard-bounced, competitor employees, do-not-contact. Missing any of these → first complaint kills the domain.
- **The complaint-rate cliff is 0.30%.** Above that, Gmail / Microsoft auto-route to spam folder, not even quarantine. Target 0.10%; 0.20% is yellow; 0.30% is red.
- **Tracking pixels lower deliverability.** Disable tracking on Touch 1 (the highest-volume cold send); enable for Touch 3+ where engagement matters more than first impression.
- **Link count matters.** One link on Touch 1; max two on subsequent. Each link = +0.5 spam score on mail-tester.
- **Plain-text vs HTML on first email.** Plain-text scores higher with spam filters; HTML acceptable from Touch 3 onwards.
- **DNS propagation is not instant.** TXT changes can take 1-24h; some resolvers cache for 48h+. Plan for it.

## Sources

- mail-tester.com (deliverability scoring): https://www.mail-tester.com/
- Lemwarm (email warmup): https://lemwarm.com/
- GlockApps inbox placement testing: https://glockapps.com/
- MXToolbox blocklist + DNS checks: https://mxtoolbox.com/
- Google Postmaster Tools docs: https://support.google.com/mail/answer/9981691
- Yahoo/Gmail Feb 2024 sender requirements (DMARC `p=quarantine` minimum): https://blog.google/products/gmail/gmail-security-authentication-spam-protection/
- Instantly deliverability guide 2026: https://www.instantly.ai/blog/email-deliverability
- Smartlead cold-email warmup playbook: https://www.smartlead.ai/blog/cold-email-warmup
