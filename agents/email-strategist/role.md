# Email Strategist — deep reference

This appends to `AGENT.md`. **Not** in the agent's default context. Grep when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "Deliverability landscape", "DMARC implementation playbook", "DMARC report parsing", "BIMI VMC runbook", "IP warming schedule", "IP reputation monitoring", "Lifecycle stages and flows", "Advanced segmentation (RFM, predictive, engagement tiers)", "Transactional vs marketing separation", "Post-MPP measurement", "Multi-language email architecture", "MJML / Maizzle scaffolds", "Dark mode + accessibility", "A/B testing email", "Inbox placement testing", "Render testing", "Complaint and bounce management", "Newsletter creator economics", "Dynamic content (Movable Ink, AMP)", "Sequence design spec template", "Deliverability audit template", "SOTA tool reference".

For provenance, see `SOURCES.md`. Per-use-case SOTA confidence map at `reference/SOTA_USE_CASES.md`.

---

## Capability reference

### ESPs supported (deep)

- **E-commerce / DTC lifecycle:** Klaviyo (default — best e-com depth, predictive AI on Plus/Advanced)
- **B2B lifecycle:** Customer.io (event-driven, segments, broadcasts), HubSpot Marketing Hub (Workflows + lifecycle stages)
- **Newsletter / creator:** Beehiiv (creator-economy, ad-network, referral, recommendations), Substack (paid-tier mechanics), ConvertKit (creator default)
- **Enterprise:** Iterable (cross-channel), Braze (enterprise lifecycle), MoEngage (mobile-first), Marketo (legacy enterprise), Salesforce Marketing Cloud
- **Modern SaaS-friendly:** Loops.so, Resend (also transactional), Customer.io
- **SMB / legacy:** Mailchimp, ActiveCampaign, Mailerlite, Brevo (formerly Sendinblue)

### Transactional ESPs

- **Modern dev-focused:** Resend (React Email templates), Postmark (deliverability-focused, sub-second median)
- **High-volume:** SendGrid (Twilio), Mailgun, Amazon SES, Mailchannels, SparkPost (DigitalOcean)

### Deliverability monitoring tools

- Glock Apps (inbox placement testing)
- Mailflow (warming + monitoring)
- GMass (placement + warming)
- 250ok / Validity (enterprise)
- Inboxable (placement testing)
- Email on Acid (rendering + sender score)
- Litmus Spam Testing
- Yardstick (formerly Sendforensics)
- Postmaster Tools v2 (Google, free)
- SNDS (Microsoft, free)
- Yahoo Postmaster (free, registered programs)
- Apple iCloud Mail Postmaster

### DMARC reporting tools

- Valimail (enterprise, deep enforcement automation)
- dmarcian (popular, generous free tier)
- DMARCLY
- EasyDMARC
- URI Ports (RUA viewer)
- Postmark DMARC Monitoring (free up to a domain)
- ondmarc by Red Sift

### BIMI authentication

- BIMI Group (specification + tools)
- DigiCert VMC (Verified Mark Certificate)
- Entrust VMC
- BIMI Inspector (validation tool)
- BIMI Radar (validation tool)
- mark.bimigroup.org (list of recognized trademarks)

### IP warming services

- Lemwarm (Lemlist)
- Mailflow
- Warmup Inbox
- Folderly
- GMass Warmer
- TrulyInbox
- MailReach

### List cleaning / verification

- ZeroBounce
- Emailable
- EmailListVerify
- BriteVerify (Validity)
- NeverBounce
- Kickbox
- DeBounce

### Email testing / rendering

- Litmus (90+ clients, dark mode, spam check)
- Email on Acid (95+ clients, dark mode, accessibility)
- Mailtrap (staging + inbox view)
- Putsmail (Litmus tool — quick send test)
- HTML Email Check (free linting)

### Design / dev frameworks

- MJML (responsive HTML abstraction → cross-client HTML)
- Maizzle (Tailwind utility-first → cross-client HTML)
- Foundation for Emails 2 / Inky
- Stripo (drag-and-drop)
- BEE Plugin / BEE Free
- Cerberus (legacy template patterns)
- Tutum Email Editor
- React Email (Resend-native)

### Analytics / measurement

- Klaviyo metrics (CTR / CTOR / revenue per recipient / placed-order rate)
- Customer.io metrics
- GA4 Data API
- PostHog (email events as PostHog events)
- Amplitude
- Mixpanel

### Postmaster + reputation

- Google Postmaster Tools v2 (free API)
- Microsoft SNDS (CSV)
- Yahoo Postmaster (registered programs)
- Apple iCloud Mail (Postmaster registration)

### Authentication building blocks

- SPF (Sender Policy Framework)
- DKIM (DomainKeys Identified Mail) — 2048-bit modern; 1024 acceptable for legacy
- DMARC (Domain-based Message Authentication, Reporting, Conformance)
- BIMI (Brand Indicators for Message Identification)
- ARC (Authenticated Received Chain) — for forwarders preserving auth
- MTA-STS (Mail Transfer Agent Strict Transport Security)
- TLS-RPT (TLS Reporting)

### AI / dynamic content

- Movable Ink (open-time dynamic content)
- Stensul (creative operations)
- AMP for Email (Gmail / Yahoo / Mail.ru / Verizon)
- Inboxsmith
- Contentful (headless content blocks)

### Compliance landmarks

- GDPR (EU)
- ePrivacy Directive (EU, member-state variations)
- CAN-SPAM (US)
- CASL (Canada)
- LGPD (Brazil)
- POPIA (South Africa)
- PIPEDA (Canada — older)
- Google + Yahoo Feb 2024 enforcement mandate
- Microsoft Outlook May 2025 enforcement mandate

---

## Deliverability landscape

### 2024-2026 platform enforcement

- **Google + Yahoo (Feb 2024):** Bulk senders (5K+/day) must: SPF + DKIM + DMARC (`p=none` minimum, alignment required); one-click unsubscribe (RFC 8058 List-Unsubscribe + List-Unsubscribe-Post headers); complaint rate < 0.30% (investigate at 0.10%, suppress at 0.30%); From-header valid + matching authenticated domain. Non-compliant: permanent rejections, not just spam folder.
- **Microsoft Outlook (May 2025):** Aligned with Google + Yahoo mandate. Outlook.com / Hotmail / Live enforcement.
- **Apple iCloud Mail:** Aligned with broader industry, enforces auth, suppresses senders with high complaint.
- **Apple MPP (Mail Privacy Protection — iOS 15+, Sep 2021):** Pre-fetches images on receipt → open rates 40-60% inflated for Apple Mail users. Treat opens as directional only.

### Authentication TXT record reference

```
# SPF
example.com.    TXT    "v=spf1 include:_spf.klaviyo.com include:_spf.google.com ~all"

# DKIM (selector ks1 example)
ks1._domainkey.example.com.    TXT    "v=DKIM1; k=rsa; p=<base64-public-key>"

# DMARC — phased deployment
_dmarc.example.com.    TXT    "v=DMARC1; p=none; rua=mailto:rua@example.com; ruf=mailto:ruf@example.com; fo=1"
# Then ramp:
_dmarc.example.com.    TXT    "v=DMARC1; p=quarantine; pct=10; rua=mailto:rua@example.com; sp=quarantine; adkim=r; aspf=r"
# Final:
_dmarc.example.com.    TXT    "v=DMARC1; p=reject; rua=mailto:rua@example.com; sp=reject; adkim=s; aspf=s"

# BIMI (requires DMARC at quarantine or reject, pct=100)
default._bimi.example.com.    TXT    "v=BIMI1; l=https://example.com/logo.svg; a=https://example.com/vmc.pem"

# MTA-STS
_mta-sts.example.com.    TXT    "v=STSv1; id=2026060901"

# TLS-RPT
_smtp._tls.example.com.    TXT    "v=TLSRPTv1; rua=mailto:tls-rpt@example.com"
```

### Deliverability audit template

```markdown
# Deliverability Audit — <domain>

## 1. Authentication
- [ ] SPF record present: `v=spf1 include:<esp>.com ~all`
- [ ] SPF mechanism count ≤ 10
- [ ] DKIM: 2048-bit key (preferred), DNS record present, signing enabled on ESP
- [ ] DMARC: `p=<none|quarantine|reject>`; pct=<n>; rua=<email>; ruf=<email>
- [ ] Return-Path aligned with From domain
- [ ] BIMI: configured / not yet
- [ ] ARC: configured for forwarder scenarios
- [ ] MTA-STS + TLS-RPT: configured for transport security

## 2. Sender reputation
- [ ] Google Postmaster Tools enrolled and monitored
- [ ] spamRate (rolling 7d): __% (target < 0.10%)
- [ ] domainReputation: HIGH / MEDIUM / LOW / BAD
- [ ] ipReputation: HIGH / MEDIUM / LOW / BAD
- [ ] FeedbackLoop subscribed and complaints suppressed
- [ ] Microsoft SNDS enrolled
- [ ] Blocklist status: clean / listed on <list>

## 3. List hygiene
- [ ] Last full validation: <date> (ZeroBounce / Emailable / NeverBounce)
- [ ] Hard bounces: removed within 24h
- [ ] Soft bounces: suppressed after 3-5 consecutive failures
- [ ] Inactive 180+ days: suppressed (sunset cohort)
- [ ] Role addresses (info@, admin@, etc.): suppressed
- [ ] Spam traps / catch-alls: suppressed

## 4. Compliance
- [ ] One-click unsubscribe (RFC 8058) functional
- [ ] List-Unsubscribe + List-Unsubscribe-Post headers present
- [ ] Physical address present (CAN-SPAM / GDPR jurisdiction)
- [ ] Consent records: date / method / source URL / IP / scope captured
- [ ] GDPR DPA in place where required
- [ ] BIMI displaying logo: yes / no / N/A

## 5. Stream separation
- [ ] Transactional subdomain separate from marketing
- [ ] Transactional ESP separate from marketing ESP
- [ ] IP pools separate (dedicated transactional / dedicated marketing)
- [ ] DMARC per subdomain (optional differing strictness)

## Remediation backlog (prioritized)
1. <P0 — production-critical issue>
2. <P1 — reputation risk>
3. <P2 — optimization opportunity>
```

---

## DMARC implementation playbook

### Phased deployment (mandatory)

**Phase 0 — Baseline.** `cli-anything dig TXT _dmarc.<domain>`. Confirm current state (unconfigured / `p=none` / `p=quarantine` / `p=reject`).

**Phase 1 — `p=none` with reporting (2-4 weeks).**
- Publish: `v=DMARC1; p=none; rua=mailto:rua@<domain>; ruf=mailto:ruf@<domain>; fo=1; adkim=r; aspf=r`
- Enroll the `rua@` mailbox in a DMARC report parser (dmarcian, Valimail, Postmark DMARC, EasyDMARC, ondmarc by Red Sift).
- Receive aggregate (RUA) reports daily from all major receivers (Google, Yahoo, Microsoft, Apple, etc.).

**Phase 2 — Analyze RUA reports + remediate alignment.**
- For each "source IP" appearing in reports:
  - Identify the sender (ESP, transactional service, third-party tool).
  - Verify SPF passes for that source (include the SPF mechanism).
  - Verify DKIM passes for that source (publish the right selector → key chain).
  - Identify any spoofing / forged sources (these are the goal of DMARC).
- Common offenders to align: Mailchimp (legacy), Marketo, Pardot, HubSpot, Salesforce, support helpdesks (Zendesk, Intercom, Freshdesk), invoicing tools (Stripe, Chargebee), HR tools (BambooHR, Gusto), CI / monitoring alerts.

**Phase 3 — `p=quarantine; pct=10` (1-2 weeks).** Monitor reports. Confirm aligned legitimate mail still passes.

**Phase 4 — `p=quarantine; pct=25` → 50 → 100 (each 1-2 weeks).** Advance only when previous step is clean. Roll back to previous pct if alignment drops.

**Phase 5 — `p=reject` (final).** Hold `p=quarantine; pct=100` for 2+ weeks clean before flipping to `p=reject`.

### DMARC subdomain policy

- `sp=` flag controls subdomain policy independent of main domain. Useful when transactional is on `notify.brand.com` and you want stricter there.
- ARC (`Authenticated Received Chain`) headers preserve auth state across forwarders — enable on ESPs that support it (Gmail, Outlook, Apple Mail).

### Common DMARC failures to fix

- ESP not configured to sign DKIM with your domain → fix in ESP setup
- SPF too long (> 10 mechanisms) → flatten via SPF macros / flattening services
- Third-party sending without DKIM → either ask vendor to add DKIM, or set up subdomain delegation with vendor's keys
- Forwarders breaking SPF → ARC helps; otherwise accept some failures and monitor
- Strict alignment (`adkim=s; aspf=s`) breaks subdomain sending → use relaxed (`r`) unless strict is necessary

---

## DMARC report parsing

### RUA (aggregate) report structure

XML over the wire (typically gzipped, attached to daily emails from each receiver). Key fields:

```xml
<feedback>
  <report_metadata>
    <org_name>google.com</org_name>
    <date_range>...</date_range>
  </report_metadata>
  <policy_published>
    <domain>example.com</domain>
    <p>none</p>
    <sp>none</sp>
    <pct>100</pct>
  </policy_published>
  <record>
    <row>
      <source_ip>198.51.100.10</source_ip>
      <count>120</count>
      <policy_evaluated>
        <disposition>none</disposition>
        <dkim>pass</dkim>
        <spf>pass</spf>
      </policy_evaluated>
    </row>
    <identifiers>
      <header_from>example.com</header_from>
    </identifiers>
    <auth_results>
      <dkim>...</dkim>
      <spf>...</spf>
    </auth_results>
  </record>
</feedback>
```

### Parsing via SOTA tools (preferred)

- **dmarcian** — `cli-anything curl https://api.dmarcian.com/v1/reports?domain=<domain>&from=<date>&to=<date>` → returns JSON with source IP groupings + auth results.
- **Valimail** — `cli-anything curl https://api.valimail.com/v1/...` → enterprise enforcement-focused.
- **Postmark DMARC** — free tier for one domain; UI + email digests.
- **EasyDMARC** — `cli-anything curl https://api.easydmarc.com/v3/...`
- **ondmarc by Red Sift** — `cli-anything curl https://api.redsift.com/v1/...`

### Per-source remediation actions

| Source IP cluster | Likely identity | Action |
|---|---|---|
| ESP-owned IP range | Klaviyo / Customer.io / HubSpot / Mailchimp | Verify DKIM selector + SPF include — ESP-side fix |
| Helpdesk IP | Zendesk / Intercom / Freshdesk / HelpScout | Add CNAME / SPF include / DKIM via vendor docs |
| Invoicing / billing | Stripe / Chargebee / Recurly | Add DKIM selector, SPF include |
| HR / payroll | BambooHR / Gusto / Workday | Add DKIM selector, SPF include |
| CI / monitoring | GitHub / GitLab / PagerDuty / Sentry | Add DKIM selector, SPF include or delegated subdomain |
| Unknown IP | Forwarder OR spoofing | If forwarder, accept and rely on `pct` ramp; if spoofing, validate then advance DMARC enforcement |

---

## BIMI VMC runbook

### Prerequisites

- DMARC at `p=quarantine; pct=100` or `p=reject`. Hard requirement. BIMI Inspector will fail if not.
- Brand owns a registered trademark (USPTO, UKIPO, EUIPO, JPO, IPO India, ICANN-recognized authority).
- Brand has an SVG Tiny PS logo (square aspect ratio, transparent background ideal, ≤ 32KB).

### Step-by-step

1. **DMARC check.** `cli-anything dig TXT _dmarc.<domain>`. Confirm `p=quarantine` (or `reject`) and `pct=100`.
2. **SVG Tiny PS.** Produce square SVG, validate via `cli-anything svgcheck` or BIMI Inspector. Host at `https://<domain>/logo.svg`.
3. **VMC procurement.** Apply via DigiCert or Entrust. Expect 1-2 week turnaround for trademark verification. Cost: ~$1,500-$1,800/yr.
4. **Publish BIMI DNS record:**
   ```
   default._bimi.<domain>.    TXT    "v=BIMI1; l=https://<domain>/logo.svg; a=https://<domain>/vmc.pem"
   ```
5. **Verification.** Visit https://bimiinspector.com/?domain=<domain> + https://bimigroup.org/bimi-generator/. Confirm all-green status.
6. **Live test.** Send to Gmail (gmail.com), Yahoo (yahoo.com), Apple Mail (icloud.com), Fastmail (fastmail.com) test inboxes. Verify logo renders in inbox list.

### Common BIMI failures

- SVG not Tiny PS profile → re-export with profile constraint
- DMARC at pct < 100 → ramp first
- VMC expired or chain invalid → renew and republish PEM
- Mark domain mismatch with VMC subject → coordinate with cert issuer

---

## IP warming schedule

### When you need to warm

- New dedicated IP from ESP (Klaviyo / Customer.io / HubSpot / Sendgrid / Mailgun / SES dedicated)
- New sending domain (cold reputation)
- Reactivating a previously-paused sending domain
- Switching ESPs and bringing your existing volume to a new IP pool

### 4-6 week ramp curve

| Week | Day | Volume to most-engaged | Volume to engaged | Volume to all |
|---|---|---|---|---|
| 1 | 1 | 50 | 0 | 0 |
| 1 | 2 | 100 | 0 | 0 |
| 1 | 3 | 200 | 0 | 0 |
| 1 | 4 | 400 | 0 | 0 |
| 1 | 5 | 800 | 0 | 0 |
| 1 | 6-7 | 1,600 | 0 | 0 |
| 2 | 8-14 | 3,000-10,000/day | 0 | 0 |
| 3 | 15-21 | full | 5,000-10,000/day | 0 |
| 4 | 22-28 | full | 25,000/day | 0 |
| 5 | 29-35 | full | full | 25,000/day |
| 6 | 36+ | full | full | full |

Adjust based on:
- Provisioned daily cap of the IP pool
- Engagement health (Postmaster Tools spamRate, ipReputation)
- Complaint rate spikes — pause or throttle on complaint > 0.10%

### Engaged cohort definition

- **Most engaged:** Opened OR clicked in last 30 days. Hand-picked for first 1-2 weeks of warming.
- **Engaged:** Opened OR clicked in last 90 days. Add weeks 3-4.
- **Sometimes engaged:** Opened OR clicked in last 180 days. Add weeks 5-6.
- **All:** Full active list (excluding sunset cohort 180+ days). Final phase.

### Parallel reputation building

- Enroll the warming domain / IP in Lemwarm, Mailflow, MailReach, Folderly, Warmup Inbox, or TrulyInbox.
- These services create reply-and-star loops with friendly inboxes to build positive engagement signals.
- Cost: ~$50-$150/month per service.

---

## IP reputation monitoring

### Google Postmaster Tools v2 (free, mandatory)

API: `https://gmailpostmastertools.googleapis.com/v1/domains`

Daily polling fields:
- `spamRate` — target < 0.10%, investigate at 0.10%, action at 0.30%
- `domainReputation` — HIGH / MEDIUM / LOW / BAD
- `ipReputation` — HIGH / MEDIUM / LOW / BAD (per IP)
- `feedbackLoop` — subscriber-initiated spam complaints (auto-suppress)
- `authenticationResults` — SPF / DKIM / DMARC pass percentages

```bash
# OAuth flow once, then:
cli-anything curl -H "Authorization: Bearer $GPMT_TOKEN" \
  "https://gmailpostmastertools.googleapis.com/v1/domains/<domain>/trafficStats?endDate.year=2026&endDate.month=6"
```

### Microsoft SNDS (free, mandatory)

CSV via authenticated session. Fields:
- complaintRate
- trapHits
- ratioOfDataStarPercent
- filterResult (green / yellow / red)

### Yahoo Postmaster + Apple iCloud Postmaster

Lower API depth than Google; register your domain in their programs for feedback loops + sender support.

### Alert thresholds

- Postmaster spamRate > 0.10% → investigate (Slack alert via `slack-mcp`)
- Postmaster domainReputation drops a tier → pause sunset / dormant sends
- Postmaster ipReputation drops a tier → check warming schedule, throttle hot sends
- SNDS filterResult = yellow → audit recent campaigns
- SNDS filterResult = red → pause and audit before next send

---

## Lifecycle stages and flows

### Stage map (e-commerce / DTC)

1. **Capture** — signup form, lead magnet, gated content
2. **Welcome** (4-5 emails, 14 days) — orient, deliver value, set expectations
3. **Browse abandonment** (1-2 emails, 1-72h) — viewed product, didn't add to cart
4. **Cart abandonment** (2-3 emails, 1-72h) — added to cart, didn't checkout
5. **First purchase** — celebration + shipping + community
6. **Post-purchase** (3-5 emails, 14-60d) — usage tips, review request, replenishment, upsell
7. **Win-back / replenishment** — consumables when window approaches
8. **Reactivation** (2-3 emails, 14-21d) — 60-90d no engagement
9. **Sunset** — 180+d, last-attempt or suppression
10. **Birthday / anniversary** — date-property triggers
11. **Referral** — post-purchase, customer-tier triggers
12. **Review request** — 7-14d post-fulfillment

### Stage map (B2B SaaS)

1. **Capture** — content download, demo request, trial signup
2. **Welcome** (3-5 emails, 7-14 days) — orient, key features, support resources
3. **Onboarding** (activation event triggered) — based on activation milestones (first project, first team invite, first integration)
4. **Nurture** (TOFU → MOFU → BOFU, by lead score) — educational → comparison → conversion
5. **Trial-to-paid** — feature highlight + ROI + booking nudge
6. **Customer expansion** — usage milestones, additional seats, premium features
7. **Renewal** (60 / 30 / 14 / 7 days pre-renewal)
8. **Win-back** — lapsed customer / cancelled trial
9. **Sunset** — long-term-dormant trial

### Sequence design spec template

```markdown
## <Sequence Name> — Design Spec

### Trigger
- Event: <profile_subscribed / event=<name> / time-based / metric-threshold>
- Delay: <immediate / X hours / X days after trigger>

### Segment
- Conditions: [<attribute_1>, <attribute_2>, ...]
  Example: [LANGUAGE=EN, LIFECYCLE=Lead, LAST_ENGAGED < 30d]
- Exclusions: [Already in sequence / Suppressed / Won customer]

### Emails
| # | Timing | Subject (A/B) | Content focus | CTA | Exit if |
|---|--------|---------------|---------------|-----|---------|
| 1 | Day 0 | <A>/<B> | <focus> | <CTA> | <condition> |
| 2 | Day 3 | <A>/<B> | <focus> | <CTA> | <condition> |
| 3 | Day 7 | <A>/<B> | <focus> | <CTA> | <condition> |

### Exit conditions
1. Converts (<event>)
2. Unsubscribes
3. Hard bounces
4. Spam complaint
5. Inactivity > <threshold> (move to <next sequence>)

### Metrics & targets
| Metric | Target | Alert threshold |
|--------|--------|-----------------|
| CTR | > 2% | < 1% |
| CTOR | > 10% | < 5% |
| Conversion rate | > 0.5% | < 0.2% |
| Unsubscribe rate | < 0.5% | > 1% |
| Complaint rate | < 0.10% | > 0.30% |

### Compliance
- [ ] Consent basis: <opt-in / legitimate interest>
- [ ] Unsubscribe: one-click (RFC 8058) functional
- [ ] List-Unsubscribe headers present
- [ ] Sender identity: <name + verified domain>
- [ ] Physical address present (jurisdiction-dependent)
```

---

## Advanced segmentation (RFM, predictive, engagement tiers)

### RFM segmentation

Compute Recency / Frequency / Monetary scores per customer (1-5 each, 5 = best).

```sql
-- Postgres warehouse via postgresql-mcp
WITH rfm AS (
  SELECT
    customer_id,
    NTILE(5) OVER (ORDER BY MAX(order_date) DESC) AS R,
    NTILE(5) OVER (ORDER BY COUNT(*) ASC) AS F,
    NTILE(5) OVER (ORDER BY SUM(total_value) ASC) AS M
  FROM orders
  WHERE order_date > NOW() - INTERVAL '24 months'
  GROUP BY customer_id
)
SELECT
  customer_id,
  CASE
    WHEN R >= 4 AND F >= 4 AND M >= 4 THEN 'Champions'
    WHEN R >= 3 AND F >= 3 THEN 'Loyal'
    WHEN R >= 4 AND F <= 2 THEN 'Recent'
    WHEN R <= 2 AND F >= 4 AND M >= 4 THEN 'At Risk'
    WHEN R <= 1 AND F >= 3 THEN 'Hibernating'
    WHEN R <= 2 AND F >= 4 AND M >= 5 THEN 'Cant Lose Best'
    ELSE 'Other'
  END AS rfm_segment
FROM rfm;
```

Push segment to ESP via Klaviyo `update_profile` or Customer.io attribute upsert.

### Klaviyo Predictive AI segments

Klaviyo Plus / Advanced tier exposes per-profile:
- `predicted_clv` (Customer Lifetime Value)
- `expected_date_of_next_order`
- `expected_number_of_orders`
- `predicted_average_order_value`
- `churn_risk` (low / medium / high)

```python
# Create segment via Klaviyo MCP
klaviyo.create_segment(
  name="High-CLV Champions",
  definition={
    "and": [
      {"profile_property": {"property": "predicted_clv", "op": "gt", "value": 500}},
      {"profile_property": {"property": "churn_risk", "op": "eq", "value": "low"}}
    ]
  }
)
```

### Engagement-tier suppression

| Tier | Definition | Send rule |
|---|---|---|
| Engaged | Opened OR clicked < 30 days | All campaigns + flows |
| Sometimes engaged | Opened OR clicked 30-90 days | Campaigns + non-aggressive flows |
| Dormant | Opened OR clicked 90-180 days | Reactivation sequence only |
| Sunset | No open AND no click > 180 days | Suppressed (no sends unless explicit re-opt) |

### Don't segment broadcast → segment-of-1 fallacy

Even with Klaviyo Predictive + RFM + engagement tiers, the practical floor is "segment defined by ≥ 2 attributes." Going to segment-of-1 means losing statistical signal in the send and breaking A/B testing.

---

## Transactional vs marketing separation

### Why separate

- Transactional emails (receipts, password resets, magic links, shipping notifications) have ~100% expected delivery and near-zero complaint rate.
- Marketing emails have variable complaint rates and require active reputation management.
- Co-mingling drags transactional deliverability down to marketing's level.

### Architecture pattern

```
brand.com (corp / non-mailing)
├── notify.brand.com  → transactional ESP (Resend / Postmark)
│   ├── SPF: include:_spf.resend.com ~all
│   ├── DKIM: rsa1024-2048
│   ├── DMARC: p=reject (stricter for transactional)
│   └── Dedicated IP pool (or transactional shared pool)
│
└── mail.brand.com  → marketing ESP (Klaviyo / Customer.io)
    ├── SPF: include:_spf.klaviyo.com ~all
    ├── DKIM: rsa2048
    ├── DMARC: p=quarantine; pct=100 (or reject after settled)
    └── Marketing IP pool (warmed)
```

### Migration checklist

- [ ] Inventory all current senders (helpdesks, ESPs, transactional services, billing, monitoring)
- [ ] Classify each as transactional / marketing
- [ ] Plan subdomain assignment per stream
- [ ] Set up new ESP accounts per stream
- [ ] Configure DNS for new subdomains (SPF / DKIM / DMARC)
- [ ] Migrate templates with QA + render testing
- [ ] Cutover ordering: lowest-volume transactional first, then marketing in cohorts
- [ ] Post-cutover monitoring (Postmaster Tools, complaint rate, deliverability)

---

## Post-MPP measurement

### What broke in Sep 2021 (iOS 15 launch)

Apple Mail Privacy Protection pre-fetches images when an email arrives at an Apple Mail user's account — regardless of whether the user opens the email. Result: Apple Mail users register as "opened" almost universally. Apple Mail is ~40-60% of US lists.

### What to measure instead

- **CTR** (clicks / sends) — primary engagement signal. Not faked by MPP.
- **CTOR** (clicks / opens) — engagement among engaged. Inflated by MPP-only-opened, so falls naturally but still informative for relative comparison.
- **Conversion rate** (purchases / sends OR purchases / opens) — business impact.
- **Revenue per email** (total revenue attributed / emails sent) — economic value.
- **Revenue per recipient** (total revenue attributed / unique recipients).
- **Placed-order rate** (Klaviyo native) — orders within 5-day attribution window.
- **Average order value from email**

### What MPP-tolerant tracking looks like

- Klaviyo `get_campaign_metrics` returns all of the above natively.
- Customer.io `metrics` endpoint similarly.
- GA4 `run_report` with `source=email + campaign=<utm>` for cross-channel conversion.
- Don't compare absolute open rates across years (the post-iOS-15 baseline is permanently higher).

### Mailbox Identifier Extension (MIE)

Apple Mail sends opens through a privacy relay → assigns a synthetic open. ESPs that distinguish "real open" vs "synthetic open" via timing heuristics (open within 1 second of send → MPP-fake; open spread out → real) help de-noise. Klaviyo handles this internally; for raw ESPs, track raw `opens` + `unique opens by time-since-send` to surface MPP shadow.

---

## Multi-language email architecture

### Pattern: per-locale templates with router

For supported languages (e.g., EN / BG / FR / DE / ES):

1. **Language attribute** as a numeric ID on each profile (EN=1, BG=2, FR=3, …)
2. **Per-locale templates** in the ESP — NOT dynamic content blocks in one template. Translation quality matters; a per-locale template lets a translator review the full email rendering, not a snippet.
3. **Translation via `deepl-mcp`** for the first pass; human review for the final.
4. **ICU MessageFormat** for plurals, gender, number formatting:
   ```
   {count, plural,
     one {You have # new item}
     other {You have # new items}
   }
   ```
5. **Router node** in the flow:
   ```
   IF Language == "BG" → BG template
   ELSE IF Language == "FR" → FR template
   ELSE → EN template (default)
   ```
6. **Recategorization flow** — if a contact is captured in the wrong language (e.g., browser was BG but user prefers EN), provide a one-click recategorize link in the welcome email that updates the Language attribute.

### Per-locale considerations

- **Send-time:** BG and EN audiences may have different peak engagement hours; Smart Send Time should be per-locale.
- **Frequency:** Different cultures have different tolerance for email frequency; FR / DE typically lower than US-EN.
- **Subject line length:** German subject lines compress poorly; budget more characters.
- **Right-to-left:** Arabic / Hebrew templates need full RTL CSS handling (MJML supports it via `dir="rtl"`).
- **Currency / date format:** ICU's number / date format handlers.

---

## MJML / Maizzle scaffolds

### MJML quick start

```xml
<!-- welcome.mjml -->
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="Helvetica, Arial, sans-serif" />
    </mj-attributes>
    <mj-style>
      @media (prefers-color-scheme: dark) {
        .bg { background-color: #111 !important; }
        .text { color: #fff !important; }
      }
    </mj-style>
  </mj-head>
  <mj-body>
    <mj-section background-color="#fff" css-class="bg">
      <mj-column>
        <mj-image src="https://cdn.brand.com/logo.png" alt="Brand" width="120px" />
        <mj-text font-size="20px" css-class="text">Welcome to <Brand>!</mj-text>
        <mj-text font-size="14px" css-class="text">
          Here's what to expect …
        </mj-text>
        <mj-button background-color="#0066ff" href="https://brand.com/start">Get started</mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
```

Compile: `cli-anything npx mjml welcome.mjml -o welcome.html`

### Maizzle quick start

```html
<!-- src/templates/welcome.html -->
---
title: Welcome to Brand
preheader: We're glad you're here.
---

<x-main>
  <table class="font-sans w-full sm:w-[600px] mx-auto">
    <tr>
      <td class="p-6 text-center">
        <img src="https://cdn.brand.com/logo.png" alt="Brand" class="w-24" />
        <h1 class="text-2xl font-bold mt-4 text-gray-900 dark:text-white">Welcome to Brand!</h1>
        <p class="mt-2 text-gray-600 dark:text-gray-300">Here's what to expect …</p>
        <a href="https://brand.com/start" class="inline-block mt-6 px-6 py-3 bg-blue-600 text-white rounded">
          Get started
        </a>
      </td>
    </tr>
  </table>
</x-main>
```

Compile: `cli-anything npx maizzle build production`

### Why MJML / Maizzle over hand-coded HTML

- Cross-client compatibility (Outlook 2007+ via VML fallbacks, Gmail clipping handling, ProtonMail strict CSP)
- Responsive defaults
- Dark mode handling
- Component reuse
- Modern syntax → "looks like HTML" rather than "looks like 2003"

---

## Dark mode + accessibility

### Dark mode patterns

- Use `prefers-color-scheme: dark` media query (supported in Apple Mail, Gmail iOS/Android partial, Outlook desktop varies)
- Provide dark-mode-safe logos (SVG with `mix-blend-mode` OR light/dark variant URL)
- Use semantic CSS colors (`color: #000` flips automatically in some clients but unreliably; explicit dark variants are safer)
- Test in Litmus / Email on Acid dark-mode previews

### WCAG AA compliance

- Color contrast: ≥ 4.5:1 for normal text, ≥ 3:1 for large text (body 14px+ counts as normal)
- Alt text on every image (informative for visual, decorative for visual flourish)
- Logical heading hierarchy (`<h1>` for title, `<h2>` for section)
- Focus order: tab-navigable order matches visual order
- Color is not the only signal (link underlines, button shapes)

### ARIA landmarks (where supported)

- `role="article"` on the email body
- `role="banner"` on header
- `role="contentinfo"` on footer
- Outlook strips many ARIA attributes — graceful degradation
- VoiceOver / TalkBack on iOS / Android handle ARIA in webview-rendered email clients

### Font sizes for accessibility

- Body: ≥ 14px (16px preferred)
- Headlines: ≥ 22px
- Avoid pixel-perfect font weights — use 400 / 600 / 700 for predictability across clients

---

## A/B testing email

### Variable categories

- **Subject line** — most-tested, highest variance impact. Length, emoji, personalization, urgency, curiosity.
- **Preview text** — second-most-impactful. Avoid duplicating subject.
- **From name** — "Brand" vs "<Person> at Brand" vs "<Person>" alone.
- **Send time** — per-recipient (Smart Send Time) is SOTA; cohort-level still useful for non-Klaviyo.
- **Copy** — first line hook, length, CTA placement.
- **CTA** — copy ("Shop now" vs "See the new collection"), color, button vs text link.
- **Hero image** — product close-up vs lifestyle vs no image.
- **Discount tier** — 10% vs 15% vs free shipping (revenue × conversion lift trade-off).

### Statistical significance gating

- Minimum sample size: 1,000 per variant for subject (high-variance), 5,000+ for copy / CTA (lower lift).
- Confidence level: 95% (p < 0.05) minimum; 99% (p < 0.01) for high-stakes.
- Klaviyo / Customer.io / HubSpot natively report statistical significance.
- For multi-variant: GrowthBook MCP via `cli-anything`.

### Don't fall for these

- "We tested subject A vs subject B, A won." → How many sends? What confidence? What was the metric? (CTR not opens.)
- "Send-time test was inconclusive." → Likely the test ran < 1 week and didn't capture day-of-week variance.
- "Discount tier test: 20% won." → Yes, but at what revenue cost? Convert lift × AOV - 20% of every order. Often net-negative.

---

## Inbox placement testing

### When to test

- Before any major campaign launch
- After DMARC enforcement change
- After IP warming completion (sanity check)
- After ESP migration
- Quarterly baseline

### Tools

- **Glock Apps** — seed list across 60+ ISPs, ISP-specific inbox / spam / missing matrix, deliverability rating
- **Inboxable** — similar, faster results
- **Mailtrap** — primarily for dev/staging inbox previews (not real ISPs)
- **mail-tester.com** — single-test sender score (1-10)
- **GMass Inbox Placement** — within their tool

### Pre-send placement test workflow

```bash
# 1. Send draft to GlockApps seed addresses
cli-anything curl -X POST https://api.glockapps.com/v1/tests \
  -H "Authorization: Bearer $GLOCK_TOKEN" \
  -d @test-config.json

# 2. Wait 30-60 min for ISPs to deliver

# 3. Poll results
cli-anything curl "https://api.glockapps.com/v1/tests/<test-id>/results" \
  -H "Authorization: Bearer $GLOCK_TOKEN"

# 4. Produce per-ISP matrix:
# | ISP | Inbox | Spam | Tabs (Promotions) | Missing |
# | Gmail | 8 | 0 | 2 | 0 |
# | Yahoo | 9 | 1 | 0 | 0 |
# ...
```

### Common spam-folder triggers

- Subject line spam-trigger words (FREE, GUARANTEE, !!!)
- Link-to-text ratio > 30% links
- Single tracking link without secondary content
- Embedded `<img>` only (no text) — looks like image-only spam
- URL shortener as primary link in unauthenticated send
- All-caps subject
- Phishing-pattern phrasing ("verify your account")

---

## Render testing

### Clients to cover

- **Desktop:** Outlook 2007, 2010, 2013, 2016, 2019, 365, Apple Mail macOS, Thunderbird
- **Web:** Gmail web, Yahoo web, Outlook.com, ProtonMail, Fastmail
- **iOS:** Mail iOS 15+, Gmail iOS, Outlook iOS
- **Android:** Gmail Android, Outlook Android, Samsung Mail
- **Modes:** Light, Dark, Mobile, Desktop

### Litmus workflow

```bash
# Upload HTML, get screenshots
cli-anything curl -X POST https://api.litmus.com/v1/emails \
  -H "Authorization: Basic $LITMUS_AUTH" \
  -d @email-config.json
# Poll for screenshots, return matrix
```

### Hard cases

- **Outlook desktop** (Word rendering engine) — break on flexbox, CSS grid, complex padding. Use MJML/Maizzle abstractions, fall back to tables.
- **Gmail clipping** — Gmail clips messages > 102KB. Trim HTML, especially inline CSS.
- **Dark mode** — Apple Mail flips backgrounds automatically; Gmail doesn't. Use `@media (prefers-color-scheme: dark)` + explicit dark variants.
- **ProtonMail** — strict CSP, no external resources without proxy. Inline everything.

---

## Complaint and bounce management

### Complaint rate targets

- **Best:** < 0.02% (0.2 per 1,000)
- **Good:** < 0.05% (0.5 per 1,000)
- **Investigate:** 0.10% (1 per 1,000)
- **Action:** 0.30% (3 per 1,000) — Google's permanent-rejection threshold
- **Block:** 0.50%+ — major ISPs start outright blocking

### Sources of complaints (in order of frequency)

1. **Send-to-wrong-segment.** Marketing to dormant. Reactivation to engaged. Mismatched intent.
2. **Frequency overload.** Multiple sends/day, or every-day cadence on a list that opted in for "weekly."
3. **Subject line bait-and-switch.** Subject says "Order shipped" but body is promotional.
4. **Unsubscribe is hard.** Hidden, broken, or multi-step unsubscribe → users complain instead.
5. **Unfamiliar sender.** Months-old signup; user forgot they opted in.

### Bounce categories

- **Hard bounce:** Permanent failure (mailbox doesn't exist, domain doesn't exist, account closed). Suppress immediately.
- **Soft bounce:** Temporary failure (mailbox full, server down, transient block). Suppress after 3-5 consecutive failures.
- **Spam bounce / Block:** ISP blocked due to reputation. Investigate sender reputation before resuming.
- **Auto-reply / OOO:** Not really a bounce; ignore.

### Complaint rate alert thresholds

```sql
-- Postgres cron via postgresql-mcp
SELECT
  campaign_id,
  total_sent,
  total_complaints,
  total_complaints::float / total_sent AS complaint_rate
FROM campaign_metrics
WHERE sent_date >= NOW() - INTERVAL '7 days'
  AND total_complaints::float / total_sent > 0.001 -- 0.10%
ORDER BY complaint_rate DESC;
```

If > 0.10%, trigger Slack alert via `slack-mcp` to ops channel.

---

## Newsletter creator economics

### Beehiiv vs Substack

| Feature | Beehiiv | Substack |
|---|---|---|
| Monetization | Ad network (built-in) + paid subscriptions + boost (paid recommendations) | Paid subscriptions only (10% cut) |
| Free plan | Generous, ad-supported | Free for free newsletters, 10% on paid |
| API | Comprehensive (v2 REST) | Limited; RSS + export |
| Recommendations network | Yes (boost = paid placement) | Yes (organic only) |
| Referral program | Built-in | Plug-in only |
| Email deliverability | Strong (shared infra) | Decent (shared infra) |
| Audience portability | Full export | Full export |
| Custom domain | Paid plan | Paid plan |
| Best for | Creator-economy scale, ads + paid mix | Writers focused on paid subs |

### Beehiiv API for programmatic ops

```bash
# Get newsletter stats
cli-anything curl "https://api.beehiiv.com/v2/publications/<pub-id>/posts" \
  -H "Authorization: Bearer $BEEHIIV_KEY"

# Create a post
cli-anything curl -X POST "https://api.beehiiv.com/v2/publications/<pub-id>/posts" \
  -H "Authorization: Bearer $BEEHIIV_KEY" \
  -d @post.json

# Subscriber sync
cli-anything curl "https://api.beehiiv.com/v2/publications/<pub-id>/subscriptions" \
  -H "Authorization: Bearer $BEEHIIV_KEY"
```

### Substack migration

- Substack RSS feed → ingest historical content
- Substack CSV export → migrate subscribers
- DNS migration → custom domain points to new platform
- Cancellation handling for paid subs → coordinate with Substack support

### Newsletter economics math

- **Free-to-paid conversion rate:** Industry baseline ~5-10%. Writer-niche specific.
- **Paid sub LTV:** monthly_price × avg_months_subscribed. For $5/mo with 18-month avg LTV, $90/sub.
- **Ad CPM (Beehiiv):** $10-$30 CPM typical for niche newsletters; up to $50+ for high-engagement B2B.
- **Boost rate (Beehiiv recommendations):** $1-$5 per qualified subscriber acquired.

---

## Dynamic content (Movable Ink, AMP)

### Movable Ink — open-time dynamic content

Use cases:
- **Weather-personalized hero image** (current weather at recipient location)
- **Countdown timer** (real-time countdown for sale, restock, event)
- **Inventory status** (live count of stock remaining)
- **Geo-targeted store map** (nearest brick-and-mortar location)
- **Behavior-based recommendations** (latest browse / cart contents on open)

```html
<!-- Movable Ink tag in Klaviyo template -->
<img src="https://<your-mi-instance>.movableink.com/v1/img/{{ recipient_id }}/weather?lat={{lat}}&lon={{lon}}" />
```

### AMP for Email — in-inbox interactivity

Use cases:
- **In-inbox booking** (calendar slot picker for service businesses)
- **Live carousel** (browse products without leaving inbox)
- **Survey / poll** (multiple-choice response without click-through)
- **Real-time data** (latest stock price, sports score)

```html
<!doctype html>
<html ⚡4email>
<head>
  <meta charset="utf-8" />
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <script async custom-element="amp-form" src="https://cdn.ampproject.org/v0/amp-form-0.1.js"></script>
  <style amp4email-boilerplate>body{visibility:hidden}</style>
</head>
<body>
  <form method="POST" action-xhr="https://brand.com/submit-feedback">
    <input type="text" name="feedback" />
    <input type="submit" value="Send" />
  </form>
</body>
</html>
```

Supported in: Gmail, Yahoo, Mail.ru, Verizon. Apple Mail / Outlook fall back to HTML version.

---

## SOTA tool reference (June 2026)

This section is grep-only — the agent uses keyword-driven retrieval to surface the right skill pack. Headings are intentionally search-friendly. Every entry links to a `SKILL.md` in `skills/` that ships in this bundle (Round 2 populates the contents).

**Full coverage map:** see `reference/SOTA_USE_CASES.md` for the per-use-case mapping and confidence rating.

### Klaviyo MCP — e-com lifecycle deep

Klaviyo MCP (official, GA Feb 2026) is the default for e-commerce / DTC lifecycle: flows, segments (including Predictive AI on Plus / Advanced), templates, campaigns, smart send time. The critical post-MPP measurement function is `get_campaign_metrics` — returns clicks, CTR, CTOR, complaint rate, revenue per recipient.

- **Skill:** `skills/klaviyo-deep-lifecycle-predictive-ai/SKILL.md`
- **Endpoint:** `npx @klaviyo/mcp-server`
- **Auth:** Private API Key → `KLAVIYO_API_KEY`
- **Key calls:** `create_segment`, `create_flow`, `create_template`, `create_campaign`, `get_campaign_metrics`, `update_profile`, `sync_list`
- **Source:** https://developers.klaviyo.com/en/docs/klaviyo_mcp_server

### Customer.io — B2B + lifecycle

Customer.io is the SOTA for event-driven B2B and product-led lifecycle. Native event triggers from product warehouse → segmented campaigns + transactional. Smart Send Time + Broadcasts + Journeys.

- **Skill:** `skills/customer-io-b2b-lifecycle/SKILL.md`
- **Endpoint:** Customer.io App API + Track API
- **Auth:** Track API key + App API key
- **Key calls:** `create_campaign`, `track_event`, `update_attributes`, `broadcast`, `segment_create`
- **Source:** https://customer.io/docs/api/

### Resend + Postmark — modern transactional

Resend is the modern dev-focused choice (React Email templates, fast adoption 2024-2026). Postmark is the deliverability-focused choice (sub-second median, generous free DMARC monitoring).

- **Skill:** `skills/resend-postmark-transactional-modern/SKILL.md`
- **Resend endpoint:** `https://api.resend.com/emails` — `RESEND_API_KEY`
- **Postmark endpoint:** `https://api.postmarkapp.com/email` — `POSTMARK_SERVER_TOKEN`
- **Source:** https://resend.com/docs + https://postmarkapp.com/developer

### Mailgun / SendGrid / SES — volume transactional

For high-volume transactional (1M+ emails/month), use Mailgun (EU residency option), SendGrid (Twilio integration, Subuser caps), or Amazon SES (cheapest at scale, lower deliverability defaults — manage your own reputation).

- **Skill:** `skills/mailgun-sendgrid-ses-volume-transactional/SKILL.md`
- **Sources:** https://documentation.mailgun.com/ + https://docs.sendgrid.com/ + https://docs.aws.amazon.com/ses/

### DMARC implementation + ARC + BIMI

Phased DMARC deployment (`p=none` → `p=quarantine` → `p=reject`) is mandatory. ARC for forwarders preserving auth. BIMI requires DMARC at `pct=100` quarantine or reject minimum, plus VMC from DigiCert / Entrust.

- **Skill:** `skills/deliverability-deep-spf-dkim-dmarc-bimi-arc/SKILL.md`
- **Tools:** `cli-anything dig` + Postmark spam check + mail-tester + MXToolbox
- **Source:** https://dmarcian.com/dmarc-deployment/ + https://www.trulyinbox.com/blog/spf-dkim-dmarc-email-deliverability/

### DMARC report parsing (Valimail / dmarcian / Postmark DMARC)

RUA (aggregate) report parsing identifies misaligned senders, third-party tools mailing on your behalf, and spoofing attempts. dmarcian + Valimail are the enterprise leaders; Postmark DMARC has a generous free tier for single-domain monitoring.

- **Skill:** `skills/dmarc-reporting-valimail-dmarcian/SKILL.md`
- **Endpoints:** `https://api.dmarcian.com/v1/...` + `https://api.valimail.com/v1/...`
- **Source:** https://dmarcian.com/api/ + https://www.valimail.com/dmarc-monitor/

### BIMI + VMC procurement

BIMI displays brand logo in Gmail / Yahoo / Apple Mail / Fastmail inbox. Requires DMARC enforcement + SVG Tiny PS logo + VMC ($1,500-$1,800/yr from DigiCert or Entrust).

- **Skill:** `skills/bimi-verified-mark-certificate-setup/SKILL.md`
- **Sources:** https://bimigroup.org/ + https://www.digicert.com/tls-ssl/verified-mark-certificates + https://bimiinspector.com/

### IP warming (Lemwarm / Mailflow / MailReach)

Dedicated IP requires 4-6 week warmup with engaged-cohort targeting. Lemwarm / Mailflow / MailReach / Folderly / Warmup Inbox / TrulyInbox provide parallel reputation building via reply-and-star loops.

- **Skill:** `skills/ip-warming-strategy-dedicated-shared/SKILL.md`
- **Sources:** https://lemwarm.com/ + https://mailflow.com/ + https://mailreach.co/

### IP reputation (Google Postmaster v2 / SNDS)

Google Postmaster Tools v2 (free API) for spam rate + domain reputation + IP reputation. Microsoft SNDS for Outlook. Yahoo Postmaster + Apple iCloud Postmaster for those ecosystems.

- **Skill:** `skills/ip-reputation-google-postmaster-snds/SKILL.md`
- **Endpoint:** `https://gmailpostmastertools.googleapis.com/v1/domains`
- **Source:** https://developers.google.com/gmail/postmaster + https://sendersupport.olc.protection.outlook.com/snds/

### List cleaning (ZeroBounce / Emailable / Kickbox)

Pre-send validation removes invalids, catch-alls, spam traps, role addresses. Inline at signup prevents 90% of bounce events.

- **Skill:** `skills/list-cleaning-zerobounce-emailable/SKILL.md`
- **Sources:** https://www.zerobounce.net/v2/documentation/ + https://emailable.com/docs/api/

### Engagement-based suppression

Suppression by engagement tier (engaged / sometimes engaged / dormant / sunset) is non-negotiable for protecting sender reputation.

- **Skill:** `skills/engagement-based-suppression/SKILL.md`

### Multi-language ESP architecture + ICU

Per-locale templates (not dynamic blocks). DeepL for translation. ICU MessageFormat for plurals / gender / dates. Router by Language profile property.

- **Skill:** `skills/multi-language-esp-architecture-icu/SKILL.md`
- **MCP:** `deepl-mcp` (already in agent.yaml)
- **Source:** https://unicode-org.github.io/icu/userguide/format_parse/messages/

### Transactional / marketing separation

Separate subdomain + IP pool + ESP per stream. Stricter DMARC on transactional. Architecture diagram + migration plan.

- **Skill:** `skills/transactional-vs-marketing-separation/SKILL.md`
- **Source:** https://postmarkapp.com/guides/separate-transactional-marketing

### Post-MPP measurement

Track CTR / CTOR / conversion / revenue per recipient — never opens as primary. Klaviyo + GA4 cross-reference.

- **Skill:** `skills/post-mpp-measurement-clicks-conversions-revenue/SKILL.md`
- **Source:** https://www.klaviyo.com/blog/apple-mail-privacy-protection

### A/B testing (subject / preview / copy / CTA / send time)

Klaviyo native A/B + Customer.io split tests. GrowthBook MCP via `cli-anything` for multi-variant + holdouts + bandit.

- **Skill:** `skills/ab-testing-subject-preview-copy-send-time/SKILL.md`
- **Source:** https://help.klaviyo.com/hc/en-us/articles/115005075928

### MJML / Maizzle responsive modular email

MJML (responsive HTML abstraction) and Maizzle (Tailwind utility-first) compile to cross-client HTML. Component reuse + dark mode + Outlook compatibility built in.

- **Skill:** `skills/mjml-maizzle-responsive-modular-email/SKILL.md`
- **Sources:** https://mjml.io/ + https://maizzle.com/

### Dark mode + accessibility

`prefers-color-scheme: dark` media query, WCAG AA contrast, ARIA landmarks (where supported), alt text, font sizes ≥ 14px body / ≥ 22px headlines.

- **Skill:** `skills/dark-mode-email-design-accessibility/SKILL.md`
- **Sources:** https://www.litmus.com/blog/the-ultimate-guide-to-dark-mode-for-email/ + https://www.emailonacid.com/blog/article/email-accessibility/

### Inbox placement testing (Glock Apps / Inboxable)

Pre-send seed-list inbox placement across 60+ ISPs. ISP-specific inbox / spam / missing matrix.

- **Skill:** `skills/glock-apps-inboxable-inbox-placement-testing/SKILL.md`
- **Sources:** https://glockapps.com/ + https://inboxable.com/

### Render testing (Litmus / Email on Acid)

90+ client render preview, dark / light mode, mobile / desktop. Visual diff across versions.

- **Skill:** `skills/litmus-email-on-acid-rendering-testing/SKILL.md`
- **Sources:** https://litmus.com/api + https://www.emailonacid.com/api/

### Complaint and bounce management

Complaint rate < 0.10% target; investigate at 0.10%; action at 0.30%. Bounce categories (hard / soft / spam-block) with suppression rules.

- **Skill:** `skills/complaint-bounce-rate-management/SKILL.md`

### Klaviyo / Customer.io flow design patterns

Named-flow templates: welcome-5-email, browse-abandonment-2-email, cart-abandonment-3-email, post-purchase-5-email, win-back-3-email, sunset-suppression-1-email. With throttling + exit conditions baked in.

- **Skill:** `skills/klaviyo-customer-io-flow-design-patterns/SKILL.md`

### Beehiiv / Substack newsletter

Beehiiv API for programmatic publishing + analytics + referral + ads. Substack migration via RSS + CSV export. Newsletter economics math.

- **Skill:** `skills/beehiiv-substack-newsletter-creator-strategy/SKILL.md`
- **Source:** https://developers.beehiiv.com/

### Dynamic personalization (Movable Ink / AMP for Email)

Open-time dynamic content (weather, countdown, inventory, geo, behavior). AMP for Email in-inbox interactivity (Gmail / Yahoo / Mail.ru / Verizon).

- **Skill:** `skills/dynamic-personalization-movable-ink/SKILL.md`
- **Sources:** https://movableink.com/developers + https://amp.dev/about/email/

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| "Build a Klaviyo welcome flow" | `klaviyo-deep-lifecycle-predictive-ai` | Combine with `klaviyo-customer-io-flow-design-patterns` for template |
| "Build a Customer.io onboarding sequence" | `customer-io-b2b-lifecycle` | Use PostHog MCP for activation events |
| "Set up Resend transactional emails" | `resend-postmark-transactional-modern` | Keep separate subdomain from marketing |
| "Send 10M emails/month transactionally" | `mailgun-sendgrid-ses-volume-transactional` | Cost ranking: SES < Mailgun < SendGrid |
| "Roll out DMARC for our domain" | `deliverability-deep-spf-dkim-dmarc-bimi-arc` | Always phased: none → quarantine → reject |
| "Analyze our DMARC reports" | `dmarc-reporting-valimail-dmarcian` | Postmark DMARC is free for 1 domain |
| "Set up BIMI for Gmail logo display" | `bimi-verified-mark-certificate-setup` | Requires VMC ~$1,500/yr |
| "Warm up a new dedicated IP" | `ip-warming-strategy-dedicated-shared` | 4-6 week schedule, engaged cohort first |
| "Monitor our domain reputation" | `ip-reputation-google-postmaster-snds` | Daily Postmaster API polling |
| "Clean our email list" | `list-cleaning-zerobounce-emailable` | ZeroBounce default; per-record cost |
| "Suppress inactive subscribers" | `engagement-based-suppression` | Engaged / dormant / sunset tiers |
| "Launch in 5 languages" | `multi-language-esp-architecture-icu` | Per-locale templates + DeepL + ICU |
| "Separate transactional from marketing" | `transactional-vs-marketing-separation` | New subdomain + ESP + IP pool |
| "Measure email performance post-MPP" | `post-mpp-measurement-clicks-conversions-revenue` | CTR / CTOR / revenue per recipient |
| "A/B test our subject lines" | `ab-testing-subject-preview-copy-send-time` | Klaviyo native; GrowthBook for multi-variant |
| "Build responsive cross-client templates" | `mjml-maizzle-responsive-modular-email` | MJML default; Maizzle for Tailwind teams |
| "Make our emails accessible" | `dark-mode-email-design-accessibility` | WCAG AA + ARIA + dark mode |
| "Pre-send inbox placement check" | `glock-apps-inboxable-inbox-placement-testing` | 60+ ISP seed list |
| "Render-test across email clients" | `litmus-email-on-acid-rendering-testing` | 90+ clients + dark mode |
| "Our complaint rate is high" | `complaint-bounce-rate-management` | Investigate at 0.10%; suppress at 0.30% |
| "Design our nurture flow" | `klaviyo-customer-io-flow-design-patterns` | Named-flow templates |
| "Launch a paid newsletter" | `beehiiv-substack-newsletter-creator-strategy` | Beehiiv default for monetization |
| "Add personalized real-time content" | `dynamic-personalization-movable-ink` | Movable Ink + AMP for Email |

---

## Brief templates / Output templates

### DMARC phased rollout plan

```markdown
# DMARC Rollout Plan — <domain>

## Current state
- DMARC: <unconfigured / p=none / p=quarantine / p=reject>
- SPF: <record>
- DKIM: <selector(s) and key sizes>
- BIMI: <none / configured>

## Phase 1: p=none with reporting (Weeks 1-4)
- Publish: `v=DMARC1; p=none; rua=mailto:rua@<domain>; fo=1`
- Enroll in: <dmarcian / Valimail / Postmark DMARC>
- Daily/weekly: review RUA reports, classify each source IP

## Phase 2: Sender alignment (Weeks 2-6, overlapping Phase 1)
- For each unaligned source IP, document remediation:
  - [ ] <source 1>: <action — e.g., "Add Mailchimp SPF include + DKIM selector">
  - [ ] <source 2>: <action>
- Re-check RUA reports weekly

## Phase 3: p=quarantine; pct=10 (Week 5)
- Publish: `v=DMARC1; p=quarantine; pct=10; rua=mailto:rua@<domain>`
- Monitor for delivery drops to legitimate senders

## Phase 4: Ramp pct (Weeks 6-9)
- pct=25 → 50 → 100 (each ~1-2 weeks if clean)

## Phase 5: p=reject (Week 10+)
- Publish: `v=DMARC1; p=reject; rua=mailto:rua@<domain>; sp=reject; adkim=s; aspf=s`
- Final state: full enforcement

## Rollback triggers
- > 0.10% legitimate-mail failure → roll back one phase
- < 95% authentication pass rate → investigate before advancing
```

### Deliverability audit report

(see Deliverability audit template above in this file)

### Sequence design spec

(see Sequence design spec template above in this file)

### IP warming day-by-day schedule

(see IP warming schedule above in this file)

### BIMI runbook

(see BIMI VMC runbook above in this file)

---

## Closing rules

Inbox placement is everything. Segmentation beats broadcast. Open rates are dead — measure clicks, conversions, revenue per email. Phased DMARC always. Never mix transactional and marketing. Engagement-tier suppression non-negotiable. Date the deliverability landscape. When broader marketing depth is needed, hand to `marketing-agent`. When cold outbound is the ask, hand to `sales-agent`.
