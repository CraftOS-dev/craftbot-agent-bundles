# Email Strategist — Use Cases

**Tier:** **specialized** (under `marketing-agent`) · **Category:** marketing
**Core job:** Deep email lifecycle + deliverability specialist beyond `marketing-agent` — advanced segmentation, DMARC implementation + report parsing, IP warming, BIMI + VMC, post-MPP measurement, transactional/marketing stream separation, multi-language email architecture, MJML / Maizzle modular design, complaint + bounce ops, newsletter creator economics.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes today via SOTA tools, and when to use it vs. its parent or siblings.

Ships with the SOTA email-strategist stack (Klaviyo MCP, Customer.io API, Resend + Postmark, Valimail / dmarcian, Google Postmaster v2 / SNDS, Lemwarm / MailReach, ZeroBounce, MJML / Maizzle, Litmus / Email on Acid, Glock Apps, Movable Ink, Beehiiv API) — executes end-to-end, not just direct.

---

## What this agent is supposed to do

### Lifecycle design

- Welcome series (zero-party data collection via progressive profiling)
- Onboarding sequence (educational + activation milestones)
- Nurture sequence (TOFU / MOFU / BOFU progression)
- Reactivation sequence (sunset + re-engagement)
- Win-back sequence (lapsed customer)
- Sunset list management (when to remove engagement-only subscribers)
- Birthday / anniversary triggers
- Browse abandonment trigger (e-com)
- Cart abandonment trigger (e-com)
- Post-purchase sequence (review + upsell + replenishment)
- Customer review request (timing + content)
- Referral program email triggers

### Advanced segmentation

- RFM (Recency / Frequency / Monetary) segmentation
- Predictive churn / LTV / next-purchase-date bands
- Klaviyo predictive AI segments (high-value, churn risk, predicted CLV)
- Engagement-tier suppression (engaged / sometimes-engaged / dormant / sunset)

### Deliverability foundation

- SPF + DKIM + DMARC + BIMI + ARC authentication audit
- Phased DMARC implementation (`p=none` → `p=quarantine` → `p=reject`)
- DMARC RUA + RUF report parsing (Valimail / dmarcian / Postmark DMARC / EasyDMARC)
- BIMI setup (logo verification, VMC procurement from DigiCert / Entrust)
- IP warming strategy (new domain or new dedicated IP, 4-6 week ramp)
- Google Postmaster Tools v2 + Microsoft SNDS + Yahoo Postmaster + Apple iCloud Postmaster monitoring
- Complaint rate management (< 0.10% target)
- Bounce rate management (hard vs soft, suppression rules)
- List cleaning + verification (ZeroBounce / Emailable / Kickbox)

### Stream architecture

- Transactional vs marketing separation (different subdomain, different ESP, different IP pool)
- Multi-ESP architecture (Klaviyo for e-com marketing + Resend / Postmark for transactional + Customer.io for B2B lifecycle)

### Multi-language email

- Multi-language email architecture (per-locale templates, NOT dynamic content blocks)
- ICU MessageFormat for plurals, gender, number formatting
- DeepL-driven translation pipeline
- Router node by Language profile property
- Recategorization flow for wrong-locale captures

### Post-MPP measurement

- Clicks over opens (post-Apple-MPP)
- MIE handling (Mailbox Identifier Extension)
- Revenue per email / revenue per recipient
- CTR + CTOR + conversion rate per send
- GA4 + Klaviyo / Customer.io cross-reference

### Creative + testing

- A/B testing email creative (subject, preview text, copy, CTA, send time)
- Send-time optimization (per recipient via Smart Send Time)
- Dynamic content (Movable Ink open-time + AMP for Email interactive forms)
- MJML / Maizzle modular email design (responsive, cross-client)
- Email accessibility (WCAG AA, ARIA landmarks, alt text, font sizes)
- Dark mode email design (`prefers-color-scheme: dark`)
- Reply-to + custom domains (vanity sender)

### Operations

- Email throttling / rate limiting
- Pre-send inbox placement testing (Glock Apps / Inboxable / mail-tester)
- Cross-client render testing (Litmus / Email on Acid — 90+ clients)
- Spam filter trigger word audit (Postmark Spam Check / SpamAssassin)

### Newsletter strategy

- Newsletter strategy (Beehiiv / Substack creator economics)
- Programmatic Beehiiv publishing + analytics
- Substack migration (RSS + CSV export)

### Transactional ESPs

- Resend (modern dev-focused + React Email)
- Postmark (deliverability-focused + free DMARC monitoring)
- Mailgun + SendGrid + Amazon SES + Mailchannels + SparkPost (volume transactional)

---

## Execution status (SOTA — June 2026)

The agent ships with SOTA MCPs and skill packs. Each use case maps to a concrete execution mechanism — no "I'll draft, you publish" disclaimers unless the user explicitly wants manual control.

### What this agent EXECUTES today

| Use case | SOTA mechanism | Path |
|---|---|---|
| Welcome series (zero-party data) | Klaviyo Flow + progressive profiling | `klaviyo-deep-lifecycle-predictive-ai` skill |
| Onboarding sequence (activation events) | Customer.io event-driven + PostHog event source | `customer-io-b2b-lifecycle` + `posthog-mcp` |
| Nurture TOFU/MOFU/BOFU | HubSpot Workflows + Customer.io | `klaviyo-customer-io-flow-design-patterns` |
| Reactivation sequence | Klaviyo segment + flow | `engagement-based-suppression` + Klaviyo MCP |
| Win-back (RFM) | Klaviyo + Postgres RFM SQL | `klaviyo-deep-lifecycle-predictive-ai` + `postgresql-mcp` |
| Sunset list mgmt | Klaviyo segment | `engagement-based-suppression` |
| Birthday / anniversary triggers | Klaviyo / Customer.io date-prop | date-trigger flow |
| Browse abandonment (e-com) | Klaviyo Viewed Product flow | `klaviyo-deep-lifecycle-predictive-ai` |
| Cart abandonment (e-com) | Klaviyo Started Checkout flow | `klaviyo-deep-lifecycle-predictive-ai` |
| Post-purchase sequence | Klaviyo Placed Order flow | `klaviyo-deep-lifecycle-predictive-ai` |
| Review request | Klaviyo + Yotpo / Trustpilot integration | `klaviyo-deep-lifecycle-predictive-ai` |
| Referral triggers | Klaviyo / Customer.io + ReferralCandy | `cli-anything` |
| RFM segmentation | Postgres SQL + Klaviyo segment push | `klaviyo-deep-lifecycle-predictive-ai` + `postgresql-mcp` |
| Klaviyo Predictive AI segments | Klaviyo Plus/Advanced predictive properties | `klaviyo-deep-lifecycle-predictive-ai` |
| Engagement-tier suppression | Klaviyo segments + send rules | `engagement-based-suppression` |
| SPF + DKIM + DMARC + BIMI + ARC audit | `dig` + mail-tester + MXToolbox + Postmark spam check | `deliverability-deep-spf-dkim-dmarc-bimi-arc` |
| Phased DMARC implementation | Progressive DNS records + RUA analysis | `deliverability-deep-spf-dkim-dmarc-bimi-arc` |
| DMARC RUA / RUF report parsing | dmarcian / Valimail / Postmark DMARC | `dmarc-reporting-valimail-dmarcian` |
| BIMI + VMC setup | DigiCert / Entrust VMC + DNS + BIMI Inspector | `bimi-verified-mark-certificate-setup` |
| IP warming (4-6 week ramp) | Lemwarm / Mailflow / MailReach + day-by-day schedule | `ip-warming-strategy-dedicated-shared` |
| IP / domain reputation monitoring | Google Postmaster Tools v2 API + SNDS CSV | `ip-reputation-google-postmaster-snds` |
| List cleaning | ZeroBounce / Emailable bulk validation | `list-cleaning-zerobounce-emailable` |
| Complaint rate management | Klaviyo `get_campaign_metrics` + Postgres cron alert | `complaint-bounce-rate-management` + `postgresql-mcp` + `slack-mcp` |
| Bounce rate management | Klaviyo / Customer.io bounce reports + suppression | `complaint-bounce-rate-management` |
| Transactional/marketing separation | DNS + ESP migration plan | `transactional-vs-marketing-separation` |
| Multi-ESP architecture | Per-stream ESP + IP + DNS | `transactional-vs-marketing-separation` |
| Multi-language email architecture | Per-locale templates + DeepL + ICU + Klaviyo router | `multi-language-esp-architecture-icu` + `deepl-mcp` |
| Post-MPP measurement | Klaviyo `get_campaign_metrics` + GA4 `run_report` | `post-mpp-measurement-clicks-conversions-revenue` |
| A/B testing email (subject/preview/copy/CTA/time) | Klaviyo native A/B + GrowthBook for multi-variant | `ab-testing-subject-preview-copy-send-time` |
| Send-time optimization (per recipient) | Klaviyo Smart Send Time + Customer.io Send-time Optimization | `klaviyo-deep-lifecycle-predictive-ai` |
| Dynamic content (Movable Ink, AMP) | Movable Ink API + AMP for Email | `dynamic-personalization-movable-ink` |
| MJML / Maizzle responsive design | MJML / Maizzle compile + push to ESP | `mjml-maizzle-responsive-modular-email` |
| Dark mode + accessibility | `prefers-color-scheme: dark` + WCAG AA + ARIA | `dark-mode-email-design-accessibility` |
| Inbox placement testing | Glock Apps / Inboxable seed-list test | `glock-apps-inboxable-inbox-placement-testing` |
| Render testing (90+ clients) | Litmus / Email on Acid API | `litmus-email-on-acid-rendering-testing` |
| Email throttling / rate limiting | Postmark MessageStream + Klaviyo throttle | `klaviyo-customer-io-flow-design-patterns` |
| Reply-to + vanity sender | DNS architecture + ESP from-address config | `transactional-vs-marketing-separation` |
| Spam trigger word audit | Postmark Spam Check + SpamAssassin via `cli-anything` | `cli-anything` curl |
| Newsletter strategy (Beehiiv) | Beehiiv API for publishing + analytics + referrals | `beehiiv-substack-newsletter-creator-strategy` |
| Substack migration | RSS + CSV export + DNS cutover | `beehiiv-substack-newsletter-creator-strategy` |
| Resend transactional + React Email | Resend API + React Email templates | `resend-postmark-transactional-modern` |
| Postmark transactional + DMARC monitoring | Postmark API + free DMARC tier | `resend-postmark-transactional-modern` |
| Volume transactional (Mailgun / SendGrid / SES) | Direct REST API via `cli-anything` | `mailgun-sendgrid-ses-volume-transactional` |

---

## Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Klaviyo Predictive AI segments | caveat | Requires Klaviyo Plus or Advanced tier — recipient brings paid subscription |
| Valimail / dmarcian / EasyDMARC | caveat | Paid subscription for full RUA report ingest; Postmark DMARC has free tier for 1 domain |
| VMC (Verified Mark Certificate) | caveat | ~$1,500-$1,800/yr from DigiCert / Entrust; required for BIMI |
| IP warming services (Lemwarm / MailReach / Mailflow / Folderly) | caveat | Paid subscription ~$50-$150/month |
| Movable Ink | caveat | Enterprise-priced dynamic content |
| Litmus / Email on Acid | caveat | Paid ~$99-$200/month |
| Glock Apps / Inboxable | caveat | Paid ~$50-$100/month |
| Beehiiv API | caveat | Paid plan required for API access |
| ZeroBounce / Emailable / NeverBounce | caveat | Per-record cost ~$0.005-$0.01 |
| Google Postmaster Tools | caveat | Free but needs one-time GCP OAuth + domain verification |
| HubSpot remote MCP | caveat | One-time OAuth at `mcp.hubspot.com` |
| LinkedIn Community Mgmt org posting | n/a | Out of scope — defer to `marketing-agent` |
| Cold outbound deliverability | n/a | Different game — defer to `sales-agent` |

**Verdict (June 2026): ~95% fulfillment.** Every documented use case has a concrete SOTA execution path. The ~5% residual is paywalled tier (Klaviyo Plus, VMC, warmup services, Movable Ink, Litmus / EOA, Glock Apps, Beehiiv) where the recipient brings the subscription — never blocking the agent's default execution.

---

## When to use this agent

- "Build a Klaviyo welcome flow with progressive profiling"
- "Roll out DMARC for our domain from `p=none` to `p=reject` over the next 12 weeks"
- "Set up BIMI so our logo shows in Gmail"
- "Warm up a new dedicated IP — produce the 6-week schedule"
- "Our complaint rate hit 0.18% last campaign — investigate and prescribe"
- "Audit our deliverability — auth, reputation, list hygiene, compliance"
- "Separate our transactional and marketing email streams"
- "Build a multi-language welcome flow for EN / FR / DE"
- "We're moving from open-rate reporting to clicks/conversions/revenue post-MPP — design the new dashboard"
- "Design an RFM-based win-back sequence for Champions / At Risk / Hibernating cohorts"
- "Render-test our Black Friday campaign across Outlook 2016 + Gmail iOS + Apple Mail dark mode"
- "Launch a paid newsletter on Beehiiv — strategy + API integration + monetization mix"
- "Add Movable Ink countdown timers to the cart-abandonment email"

---

## When NOT to use this agent

- **Broader marketing surface** (positioning, brand voice, blog content, social media, top-of-funnel acquisition, light analytics across non-email channels) — hand off to `marketing-agent`
- **Cold outbound for sales sequences** (list-building / enrichment, outbound deliverability with warmup, sequence cadence, reply detection, CRM-driven enrollment, MEDDIC / BANT on responses) — hand off to `sales-agent`
- **Transactional support content** (auto-replies, FAQ-driven helpdesk, incident comms, Statuspage emails) — hand off to `customer-support-agent`
- **Deep cohort analysis on email performance** (multi-touch attribution, cohort survival curves, predictive churn modeling beyond Klaviyo's built-in, custom RFM tied to LTV models with regression) — hand off to `data-analyst`
- **Engineering work on a transactional sending service** (SDK design, queue architecture, retry semantics, webhook ingestion pipelines) — hand off to `senior-python-engineer` or `devops-engineer`
- **Legal review of consent / GDPR / CCPA / LGPD** — draft, but flag for legal sign-off (or hand off to `legal-counsel`)
- **Brand strategy at the agency-engagement level** (rebrand, naming, positioning research over months) — `marketing-agent` can start it; for full depth, a brand strategist specialist (v1)
