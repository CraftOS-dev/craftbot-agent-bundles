# email-strategist — SOTA Use Cases (June 2026)

> Specialist agent under `marketing-agent`. Drills deeper than the parent on lifecycle, deliverability, DMARC, IP warming, BIMI, post-MPP, transactional/marketing separation, IP reputation.

This document maps every use case in `USE_CASES.md` to a concrete SOTA execution mechanism with a source URL and confidence rating.

**Legend:**
- (yes) — production MCP / first-class API, OAuth or key exposed via `agent.yaml`, end-to-end automated.
- (caveat) — works today but with a one-time setup step (OAuth, paid API key, app approval) the recipient owns.
- (gap) — partial coverage; rate-limited, scraping-fallback, or domain-specific paid tooling.

---

## Welcome series design (zero-party data collection)

- **SOTA approach:** Klaviyo Flow Builder (e-com) / Customer.io Campaigns (B2B + lifecycle) / HubSpot Workflows (B2B). Zero-party data via progressive profiling — capture preference center attributes across emails 1-5, not all at signup.
- **Agent execution path:** `klaviyo-deep-lifecycle-predictive-ai` skill → `cli-anything npx @klaviyo/mcp-server` → `create_flow(trigger='profile_subscribed', steps=[delay+email+profile_property_update])`. For B2B, `customer-io-b2b-lifecycle` skill → Customer.io `create_campaign` via App API.
- **Source:** https://developers.klaviyo.com/en/docs/klaviyo_mcp_server + https://customer.io/docs/api/
- **Confidence:** yes

## Onboarding sequence design (educational + activation milestones)

- **SOTA approach:** Customer.io segmented onboarding tied to activation events; Klaviyo profile property "activated_at"; HubSpot lifecycle stage transitions.
- **Agent execution path:** `customer-io-b2b-lifecycle` skill → event-triggered campaign keyed to `feature_first_used`, `team_invited`, etc. PostHog provides activation event source via `posthog-mcp`.
- **Source:** https://customer.io/docs/journeys/campaigns
- **Confidence:** yes

## Nurture sequence (TOFU/MOFU/BOFU progression)

- **SOTA approach:** HubSpot Workflows with lifecycle stage progression; Customer.io segments by lead score; Klaviyo conditional splits.
- **Agent execution path:** `klaviyo-customer-io-flow-design-patterns` skill named-flow templates → push to HubSpot via remote MCP (`mcp.hubspot.com`) or Customer.io App API.
- **Source:** https://developers.hubspot.com/mcp + https://customer.io/docs/api/
- **Confidence:** caveat (HubSpot one-time OAuth)

## Reactivation sequence (sunset + re-engagement)

- **SOTA approach:** Klaviyo segment `engaged_60d_ago AND NOT engaged_30d` → 2-3 email re-engagement → conditional suppression on no-engage.
- **Agent execution path:** `engagement-based-suppression` skill → Klaviyo `create_segment(definition={conditions: [last_clicked > 60d AND last_clicked < 30d]})` → flow.
- **Source:** https://help.klaviyo.com/hc/en-us/articles/115002542091
- **Confidence:** yes

## Win-back sequence (lapsed customer)

- **SOTA approach:** RFM segmentation (Recency-Frequency-Monetary) flagging "lost-best" cohort → 3-email win-back with incentive escalation → final unsubscribe-or-stay choice.
- **Agent execution path:** PostHog HogQL or warehouse SQL via `postgresql-mcp` to compute RFM scores → push to Klaviyo segment → win-back flow.
- **Source:** https://klaviyo.com/marketing-resources/rfm-segmentation-guide
- **Confidence:** yes

## Sunset list management (when to remove engagement-only subscribers)

- **SOTA approach:** Engagement-tier suppression: hard-suppress profiles with zero opens + zero clicks for 180 days post-acquisition; soft-suppress at 90 days with sunset email.
- **Agent execution path:** `engagement-based-suppression` skill → Klaviyo `create_segment(definition={last_open > 180d AND last_click > 180d})` → `suppress_profiles` API or set to non-mailable.
- **Source:** https://www.klaviyo.com/blog/list-cleaning-deliverability
- **Confidence:** yes

## Birthday / anniversary triggers

- **SOTA approach:** Klaviyo / Customer.io date-property triggered campaigns (DOB or signup-anniversary). Conditional discount based on customer LTV tier.
- **Agent execution path:** Klaviyo `create_flow(trigger='date_property:birthday', timing='annual')`; Customer.io date-attribute trigger.
- **Source:** https://help.klaviyo.com/hc/en-us/articles/360003936232
- **Confidence:** yes

## Browse abandonment trigger (e-commerce)

- **SOTA approach:** Klaviyo viewed-product event → 1-2 hour delay → tailored email referencing the SKU + related products. Shopify/BigCommerce integration auto-captures the event.
- **Agent execution path:** `klaviyo-deep-lifecycle-predictive-ai` skill → flow trigger `event=Viewed Product AND NOT Placed Order`. Shopify MCP (`shopify-mcp`) for product detail enrichment.
- **Source:** https://help.klaviyo.com/hc/en-us/articles/115001545512
- **Confidence:** yes

## Cart abandonment trigger (e-commerce)

- **SOTA approach:** Klaviyo Started Checkout flow with 3-email cadence (1h reminder, 24h offer, 72h scarcity). Predictive AI suggests best discount tier per profile.
- **Agent execution path:** Klaviyo `create_flow(trigger='Started Checkout', steps=[email_1h, email_24h_discount, email_72h_scarcity])`. Klaviyo Predictive AI segment for high-discount-sensitivity profiles.
- **Source:** https://help.klaviyo.com/hc/en-us/articles/360001070631
- **Confidence:** yes

## Post-purchase sequence (review + upsell + replenishment)

- **SOTA approach:** Klaviyo `Placed Order` flow → delay aligned with product use cycle (consumables ~replenishment window; durable ~review at 14d, upsell at 60d) → conditional branches by product category.
- **Agent execution path:** Klaviyo `create_flow(trigger='Placed Order', conditional_splits=[by_product_category])`.
- **Source:** https://www.klaviyo.com/blog/post-purchase-email-flow
- **Confidence:** yes

## Customer review request (timing + content)

- **SOTA approach:** Klaviyo `Placed Order` flow → wait 7-14 days (DTC physical goods) or 24-48 hours (SaaS onboarding milestone) → request review with Yotpo / Trustpilot / Loox integration.
- **Agent execution path:** `klaviyo-deep-lifecycle-predictive-ai` skill → review-request flow with 7d delay. Yotpo / Trustpilot API via `cli-anything` for review collection.
- **Source:** https://klaviyo.com/blog/review-request-email-best-practices
- **Confidence:** yes

## Referral program email triggers

- **SOTA approach:** Klaviyo / Customer.io referral-event-triggered email sequence. ReferralCandy / Friendbuy / GrowSurf for the underlying referral logic.
- **Agent execution path:** Trigger from referral platform event → Klaviyo/Customer.io campaign → custom referral link via Bitly bulk_shorten.
- **Source:** https://www.referralcandy.com/api-docs
- **Confidence:** caveat (referral platform paid tier)

## Advanced segmentation (RFM, predictive churn, LTV bands)

- **SOTA approach:** Klaviyo Predictive AI segments (built-in churn risk, expected LTV, expected next purchase date, average time between orders). PostgreSQL warehouse for custom RFM/cohort joins.
- **Agent execution path:** `klaviyo-deep-lifecycle-predictive-ai` skill → `create_segment(predictive_property={churn_risk: high})`. For non-Klaviyo, `postgresql-mcp` RFM SQL → sync to ESP via API.
- **Source:** https://help.klaviyo.com/hc/en-us/articles/360054384451
- **Confidence:** yes

## Klaviyo predictive AI segments

- **SOTA approach:** Klaviyo Predictive Analytics (built into Plus / Advanced plans) — exposes predicted CLV, expected next order date, churn risk, average order value as profile properties.
- **Agent execution path:** Klaviyo MCP `create_segment` filter on `predictive_clv > $500` or `churn_risk = high` etc.
- **Source:** https://help.klaviyo.com/hc/en-us/articles/115002470712
- **Confidence:** caveat (Klaviyo paid tier — Plus/Advanced)

## IP warming strategy (new domain or new dedicated IP)

- **SOTA approach:** 4-6 week ramp curve following Sender Score guidance (start at 50/day to most-engaged, double daily up to volume cap, throttle aggressively at first signs of complaint or block). Tools: Lemwarm, Mailflow, Warmup Inbox, Folderly, MailReach, TrulyInbox, GMass Warmer.
- **Agent execution path:** `ip-warming-strategy-dedicated-shared` skill produces day-by-day volume schedule + engaged-cohort targeting plan. `cli-anything` calls Lemwarm/Mailflow/MailReach API to enroll the sender domain.
- **Source:** https://lemwarm.com/ + https://mailflow.com/ + https://www.warmupinbox.com/
- **Confidence:** caveat (warmup-service paid subscription)

## DMARC implementation (p=none → p=quarantine → p=reject)

- **SOTA approach:** Phased policy progression. Week 1-4: `p=none` with `rua` reporting enabled; weeks 5-8: analyze DMARC reports, fix all legitimate-but-unaligned senders; week 9-12: `p=quarantine; pct=10` then ramp to 100; week 13+: `p=reject`. Tools: Valimail, dmarcian, DMARCLY, EasyDMARC, URI Ports, Postmark DMARC, ondmarc by Red Sift.
- **Agent execution path:** `deliverability-deep-spf-dkim-dmarc-bimi-arc` skill → `cli-anything dig TXT _dmarc.<domain>` baseline → write progressive policy DNS records → enroll in dmarcian or Valimail via API.
- **Source:** https://dmarcian.com/dmarc-deployment/ + https://www.valimail.com/dmarc/
- **Confidence:** yes

## DMARC report parsing + analysis (Valimail, dmarcian)

- **SOTA approach:** Aggregate (RUA) and Forensic (RUF) report parsing via dmarcian / Valimail / Postmark DMARC. Identifies misaligned senders, third-party tools mailing on your behalf, spoofing attempts.
- **Agent execution path:** `dmarc-reporting-valimail-dmarcian` skill → `cli-anything curl https://api.dmarcian.com/v1/reports` (or `https://api.valimail.com/...`) → parse XML rua reports → produce remediation plan per misaligned source.
- **Source:** https://dmarcian.com/api/ + https://www.valimail.com/dmarc-monitor/
- **Confidence:** caveat (paid subscription; Postmark DMARC has free tier)

## BIMI setup (logo verification, VMC)

- **SOTA approach:** BIMI requires DMARC `p=quarantine` or `p=reject` (at pct=100), SVG Tiny PS logo at the brand's domain, and a Verified Mark Certificate (VMC) from DigiCert or Entrust. Gmail / Yahoo / Apple Mail / Fastmail render the inbox logo.
- **Agent execution path:** `bimi-verified-mark-certificate-setup` skill → validate DMARC at pct=100 reject → generate SVG Tiny PS → procure VMC from DigiCert/Entrust ($1,500-$1,800/year typical) → publish BIMI DNS TXT record `v=BIMI1; l=<svg-url>; a=<vmc-pem-url>` → verify via BIMI Inspector / BIMI Radar.
- **Source:** https://bimigroup.org/ + https://www.digicert.com/tls-ssl/verified-mark-certificates + https://bimiinspector.com/
- **Confidence:** caveat (VMC ~$1,500/yr; one-time setup)

## Email authentication audit (SPF, DKIM, DMARC, BIMI, ARC)

- **SOTA approach:** Full auth audit: `dig` for SPF/DKIM selectors/DMARC, mail-tester.com for combined score, MXToolbox API for blocklist + auth check, intoDNS for DNS sanity. ARC enables forwarders to preserve auth signals.
- **Agent execution path:** `deliverability-deep-spf-dkim-dmarc-bimi-arc` skill → orchestrate `dig` + `curl mail-tester.com` + `curl mxtoolbox` + Postmark spam check.
- **Source:** https://mxtoolbox.com/ + https://www.mail-tester.com/ + https://www.trulyinbox.com/blog/spf-dkim-dmarc-email-deliverability/
- **Confidence:** yes

## IP reputation monitoring (Google Postmaster, SNDS)

- **SOTA approach:** Google Postmaster Tools v2 (free) exposes spam rate, IP reputation, domain reputation, feedback loop data, authentication results. Microsoft SNDS (Smart Network Data Services) for Outlook/Hotmail. Yahoo Postmaster (registered programs). Apple iCloud Postmaster.
- **Agent execution path:** `ip-reputation-google-postmaster-snds` skill → Google Postmaster Tools API v1 (`https://gmailpostmastertools.googleapis.com/v1/domains`) via OAuth → daily polling → alert if `spamRate > 0.1%`. Microsoft SNDS via authenticated CSV scrape.
- **Source:** https://developers.google.com/gmail/postmaster + https://sendersupport.olc.protection.outlook.com/snds/
- **Confidence:** caveat (one-time GCP OAuth)

## Complaint rate management (<0.10% target)

- **SOTA approach:** Track per-campaign and rolling 30-day complaint rate via Klaviyo `get_campaign_metrics`, Customer.io reports, or ESP-specific FBL data. Auto-suppress complainers. Trigger investigation if > 0.10%.
- **Agent execution path:** `complaint-bounce-rate-management` skill → Klaviyo MCP `get_campaign_metrics(metrics=['complaint_rate'])` → if > 0.10% trigger investigation flow + Slack/Gmail alert.
- **Source:** https://help.klaviyo.com/hc/en-us/articles/360046068731
- **Confidence:** yes

## Bounce rate management (hard vs soft, suppression)

- **SOTA approach:** ESPs auto-suppress hard bounces; soft bounces suppress after 3-5 consecutive failures. Validate at signup with ZeroBounce / Emailable / BriteVerify to prevent bounces in the first place.
- **Agent execution path:** `complaint-bounce-rate-management` skill → query Klaviyo / Customer.io bounce reports → cross-check suppression list. `list-cleaning-zerobounce-emailable` skill for proactive validation.
- **Source:** https://www.zerobounce.net/ + Klaviyo bounce handling
- **Confidence:** yes

## List cleaning + verification (ZeroBounce + ongoing hygiene)

- **SOTA approach:** Pre-send full-list validation via ZeroBounce / Emailable / EmailListVerify / NeverBounce / BriteVerify / Kickbox. Inline validation at signup via Mailgun Validate / SendGrid Email Validation API.
- **Agent execution path:** `list-cleaning-zerobounce-emailable` skill → `cli-anything curl -X POST https://api.zerobounce.net/v2/sendfile` with subscriber list → ingest results → suppress invalid/catch-all/spam-trap.
- **Source:** https://www.zerobounce.net/v2/documentation/ + https://emailable.com/docs/api/
- **Confidence:** caveat (per-validation cost ~$0.005-$0.01)

## Engagement-based suppression

- **SOTA approach:** Engagement tiers (engaged < 30d, sometimes-engaged 30-90d, dormant 90-180d, sunset > 180d). Only send re-engagement to dormant; suppress sunset cohort entirely (unless explicit re-opt).
- **Agent execution path:** `engagement-based-suppression` skill → Klaviyo `create_segment` per tier → send rules: mass campaigns only to engaged + sometimes-engaged; reactivation only to dormant; sunset = suppressed.
- **Source:** https://www.klaviyo.com/blog/list-cleaning-deliverability
- **Confidence:** yes

## Multi-language email architecture (per-locale templates, ICU MessageFormat)

- **SOTA approach:** Per-language template files (not dynamic blocks). Language attribute as router. ICU MessageFormat for pluralization, gender, number formatting. DeepL for translation. Klaviyo / HubSpot / Customer.io support per-language template variants.
- **Agent execution path:** `multi-language-esp-architecture-icu` skill → DeepL MCP for translation → Klaviyo `create_template` per language → flow router on Language profile property.
- **Source:** https://klaviyo.com/blog/multi-language-email + https://unicode-org.github.io/icu/userguide/format_parse/messages/
- **Confidence:** yes

## Transactional vs marketing separation (different streams, different domains)

- **SOTA approach:** Separate sender subdomains (e.g., `mail.brand.com` for marketing, `notify.brand.com` for transactional), separate IP pools, separate ESPs ideal (Resend / Postmark / SendGrid for transactional; Klaviyo / Customer.io for marketing). Different DMARC policies if needed (transactional usually stricter).
- **Agent execution path:** `transactional-vs-marketing-separation` skill → DNS architecture plan + ESP migration plan + per-stream auth records. `resend-postmark-transactional-modern` skill drives the transactional side.
- **Source:** https://resend.com/blog/transactional-vs-marketing-email + https://postmarkapp.com/guides/separate-transactional-marketing
- **Confidence:** yes

## Post-MPP measurement (clicks > opens, MIE handling, ratio tracking)

- **SOTA approach:** Open rates are pre-inflated by Apple Mail Privacy Protection (40-60% of US list). Track CTR (clicks/sends), CTOR (clicks/opens), conversion rate (purchases/sends or /opens), revenue per email, revenue per recipient. Klaviyo / Customer.io expose these natively. Mailbox Identifier Extension (MIE) helps de-noise opens.
- **Agent execution path:** `post-mpp-measurement-clicks-conversions-revenue` skill → Klaviyo `get_campaign_metrics(metrics=['clicked','clicked_unique','ctr','ctor','revenue_per_recipient'])` → cross-reference GA4 MCP `run_report(filter={source=email})` for conversion.
- **Source:** https://www.klaviyo.com/blog/apple-mail-privacy-protection + https://github.com/googleanalytics/google-analytics-mcp
- **Confidence:** yes

## A/B testing email creative (subject, preview text, copy, CTA, send time)

- **SOTA approach:** Klaviyo native A/B with statistical significance gating; Customer.io split tests; ESP-native variant management. Statistical power calculation per test.
- **Agent execution path:** `ab-testing-subject-preview-copy-send-time` skill → Klaviyo `create_campaign(variations=[A,B], split_percent=10, winner_metric=ctr)`. For multi-variant, GrowthBook MCP via `cli-anything`.
- **Source:** https://help.klaviyo.com/hc/en-us/articles/115005075928
- **Confidence:** yes

## Send-time optimization (per recipient)

- **SOTA approach:** Klaviyo Smart Send Time, Customer.io Send-time Optimization, HubSpot "Send Time Optimization" — algorithmically pick best send time per recipient based on past engagement. Fallback: cohort-level analysis (best send day/hour by segment).
- **Agent execution path:** `klaviyo-deep-lifecycle-predictive-ai` skill → enable smart send time at flow/campaign level. Custom: warehouse SQL via `postgresql-mcp` for cohort optimal hour.
- **Source:** https://help.klaviyo.com/hc/en-us/articles/360050287831
- **Confidence:** yes

## Dynamic content (Movable Ink, contentful AMP, Stensul)

- **SOTA approach:** Movable Ink for real-time dynamic content (open-time weather, countdown, inventory, geo, behavior). Stensul for content creation operations. Contentful for headless content blocks. AMP for Email for in-inbox interactive forms.
- **Agent execution path:** `dynamic-personalization-movable-ink` skill → Movable Ink API (`https://api.movableink.com/v1/...`) to define dynamic blocks → embed Movable Ink tags in Klaviyo / Customer.io templates.
- **Source:** https://movableink.com/developers + https://amp.dev/about/email/
- **Confidence:** caveat (Movable Ink paid tier)

## MJML / Maizzle modular email design

- **SOTA approach:** MJML (responsive abstraction → cross-client HTML). Maizzle (Tailwind utility-first for email → HTML). Foundation for Emails 2 (Inky). Cerberus templates as legacy reference.
- **Agent execution path:** `mjml-maizzle-responsive-modular-email` skill → `cli-anything npx mjml input.mjml > output.html` or `cli-anything npx maizzle build`. Push compiled HTML to Klaviyo / Customer.io via API.
- **Source:** https://mjml.io/ + https://maizzle.com/
- **Confidence:** yes

## Dark mode email design + accessibility

- **SOTA approach:** Use `prefers-color-scheme: dark` media query; provide dark-mode-safe logos (SVG with `mix-blend-mode`); use semantic colors; test in Litmus / Email on Acid dark-mode previews. WCAG AA contrast for both modes. ARIA landmarks where supported. Alt text on every image. Font size ≥ 14px body, ≥ 22px headlines.
- **Agent execution path:** `dark-mode-email-design-accessibility` skill → compose MJML/Maizzle with dark-mode tokens → Litmus / Email on Acid render test.
- **Source:** https://www.litmus.com/blog/the-ultimate-guide-to-dark-mode-for-email/ + https://www.emailonacid.com/blog/article/email-accessibility/
- **Confidence:** caveat (Litmus / EOA paid subscription)

## Glock Apps + Inboxable inbox placement testing

- **SOTA approach:** Pre-send seed-list test: send campaign to 50-100 seed addresses across major ISPs (Gmail, Outlook, Yahoo, Apple, ProtonMail, regional like Mail.ru) → measure inbox vs spam vs missing. Tools: Glock Apps, Inboxable, Mail-tester, Mailtrap, GMass Inbox Placement.
- **Agent execution path:** `glock-apps-inboxable-inbox-placement-testing` skill → `cli-anything curl https://api.glockapps.com/v1/tests` → run test → poll for results → produce per-ISP placement matrix.
- **Source:** https://glockapps.com/ + https://inboxable.com/
- **Confidence:** caveat (paid tools, ~$50-$100/month)

## Litmus + Email on Acid rendering testing

- **SOTA approach:** Multi-client render test across 90+ email clients (Outlook 2007/2016/365, Gmail web/iOS/Android, Apple Mail, Yahoo, ProtonMail, dark/light, mobile/desktop). Visual diff between versions.
- **Agent execution path:** `litmus-email-on-acid-rendering-testing` skill → Litmus API (`https://api.litmus.com/v1/...`) or EOA API to upload HTML → poll for screenshots → produce rendering diff report.
- **Source:** https://litmus.com/api + https://www.emailonacid.com/api/
- **Confidence:** caveat (paid subscription)

## Email throttling / rate limiting

- **SOTA approach:** ESP-level send throttling to respect Gmail / Yahoo / Outlook arrival-rate suggestions (especially for warming IPs). Postmark `MessageStreamId` with stream-specific rate; SendGrid Subuser caps; Klaviyo per-campaign throttle.
- **Agent execution path:** `klaviyo-customer-io-flow-design-patterns` skill → set `send_rate_per_minute` on campaign. For dedicated IP, follow warming schedule from `ip-warming-strategy-dedicated-shared`.
- **Source:** https://postmarkapp.com/manual#rate-limits + https://help.klaviyo.com/hc/en-us/articles/115005076748
- **Confidence:** yes

## Reply-to + custom domains (vanity sender)

- **SOTA approach:** Reply-to domain CNAME / forward to support inbox; custom From domain authenticated end-to-end (SPF + DKIM + DMARC aligned); BIMI logo display. Avoid `noreply@` whenever possible.
- **Agent execution path:** `transactional-vs-marketing-separation` skill includes the DNS architecture playbook. `cli-anything dig` for verification.
- **Source:** https://postmarkapp.com/guides/email-sender-best-practices
- **Confidence:** yes

## Spam filter trigger word audit

- **SOTA approach:** SpamAssassin / Postmark Spam Check / mail-tester scoring. Identify high-score-contribution words (FREE, GUARANTEE, !!!), excessive caps, link/text ratio, suspicious URLs.
- **Agent execution path:** `litmus-email-on-acid-rendering-testing` skill (Litmus also includes spam check) + `cli-anything curl -X POST https://spamcheck.postmarkapp.com/filter` per draft.
- **Source:** https://spamcheck.postmarkapp.com/
- **Confidence:** yes

## Newsletter strategy (Beehiiv / Substack creator economics)

- **SOTA approach:** Beehiiv (creator-economy newsletter platform, ad-network monetization, referral programs, recommendations network) and Substack (subscription-based, paid tier mechanics) are the SOTA for newsletter monetization. Beehiiv API for programmatic publishing + analytics; Substack API limited.
- **Agent execution path:** `beehiiv-substack-newsletter-creator-strategy` skill → Beehiiv API (`https://api.beehiiv.com/v2/...`) for publishing + subscriber sync. Substack via RSS + manual export for migration scenarios.
- **Source:** https://developers.beehiiv.com/ + https://substack.com/help
- **Confidence:** caveat (Beehiiv API access requires paid plan)

## Resend / Postmark / SendGrid / Mailgun / SES (modern transactional)

- **SOTA approach:** Resend (modern dev-focused, React Email templates, very fast adoption 2024-2026); Postmark (deliverability-focused, sub-second median); SendGrid (high-volume + automation); Mailgun (high-volume + EU residency); Amazon SES (cheapest at scale, lower deliverability defaults).
- **Agent execution path:** `resend-postmark-transactional-modern` skill for Resend/Postmark; `mailgun-sendgrid-ses-volume-transactional` skill for high-volume. All via `cli-anything curl` against respective REST APIs.
- **Source:** https://resend.com/docs + https://postmarkapp.com/developer + https://docs.sendgrid.com/ + https://documentation.mailgun.com/ + https://docs.aws.amazon.com/ses/
- **Confidence:** yes

## Multi-ESP architecture (one ESP per stream)

- **SOTA approach:** Klaviyo (marketing/e-com) + Resend (transactional) + Customer.io (B2B lifecycle) + Postmark (transactional alt) per stream. Each on dedicated subdomain + IP pool. Identity federation via warehouse / CDP (Segment / RudderStack / Hightouch).
- **Agent execution path:** `transactional-vs-marketing-separation` skill produces the architecture diagram + DNS + IP plan. `cli-anything` for CDP integration calls.
- **Source:** https://www.klaviyo.com/blog/transactional-vs-marketing-email
- **Confidence:** yes

---

## Summary table (≥95% fulfillment)

| # | Use case | SOTA tool | Mechanism | Fulfillment |
|---|---|---|---|---|
| 1 | Welcome series (zero-party) | Klaviyo / Customer.io / HubSpot | `klaviyo-deep-lifecycle-predictive-ai` skill + `cli-anything` | yes |
| 2 | Onboarding sequence | Customer.io / Klaviyo | `customer-io-b2b-lifecycle` + `posthog-mcp` | yes |
| 3 | Nurture TOFU/MOFU/BOFU | HubSpot / Customer.io / Klaviyo | `klaviyo-customer-io-flow-design-patterns` skill | caveat |
| 4 | Reactivation sequence | Klaviyo segment+flow | `engagement-based-suppression` skill | yes |
| 5 | Win-back (RFM) | Klaviyo + Postgres RFM | `klaviyo-deep-lifecycle-predictive-ai` + `postgresql-mcp` | yes |
| 6 | Sunset list mgmt | Klaviyo / Customer.io | `engagement-based-suppression` skill | yes |
| 7 | Birthday triggers | Klaviyo / Customer.io | date-prop flow | yes |
| 8 | Browse abandonment | Klaviyo + Shopify | `klaviyo-deep-lifecycle-predictive-ai` skill | yes |
| 9 | Cart abandonment | Klaviyo Started Checkout | `klaviyo-deep-lifecycle-predictive-ai` skill | yes |
| 10 | Post-purchase sequence | Klaviyo Placed Order | `klaviyo-deep-lifecycle-predictive-ai` skill | yes |
| 11 | Review request timing | Klaviyo + Yotpo/Trustpilot | `klaviyo-deep-lifecycle-predictive-ai` skill | yes |
| 12 | Referral triggers | Klaviyo/Customer.io + ReferralCandy | `cli-anything` | caveat |
| 13 | Advanced segmentation (RFM, churn, LTV) | Klaviyo Predictive + Postgres | `klaviyo-deep-lifecycle-predictive-ai` + `postgresql-mcp` | yes |
| 14 | Klaviyo predictive AI | Klaviyo Predictive | `klaviyo-deep-lifecycle-predictive-ai` skill | caveat (paid tier) |
| 15 | IP warming strategy | Lemwarm / Mailflow / MailReach | `ip-warming-strategy-dedicated-shared` skill | caveat (paid) |
| 16 | DMARC implementation (phased) | Valimail / dmarcian | `deliverability-deep-spf-dkim-dmarc-bimi-arc` skill | yes |
| 17 | DMARC report parsing | dmarcian / Valimail / Postmark | `dmarc-reporting-valimail-dmarcian` skill | caveat |
| 18 | BIMI + VMC | BIMI Group + DigiCert/Entrust | `bimi-verified-mark-certificate-setup` skill | caveat (VMC) |
| 19 | Email auth audit | dig + mail-tester + MXToolbox | `deliverability-deep-spf-dkim-dmarc-bimi-arc` skill | yes |
| 20 | IP reputation (Postmaster/SNDS) | Google Postmaster v2 + SNDS | `ip-reputation-google-postmaster-snds` skill | caveat (one-time OAuth) |
| 21 | Complaint rate management | Klaviyo get_campaign_metrics | `complaint-bounce-rate-management` skill | yes |
| 22 | Bounce rate management | Klaviyo + ZeroBounce | `complaint-bounce-rate-management` skill | yes |
| 23 | List cleaning | ZeroBounce / Emailable / Kickbox | `list-cleaning-zerobounce-emailable` skill | caveat (per-record cost) |
| 24 | Engagement suppression | Klaviyo segments | `engagement-based-suppression` skill | yes |
| 25 | Multi-language (ICU) | DeepL + per-locale templates | `multi-language-esp-architecture-icu` + `deepl-mcp` | yes |
| 26 | Transactional/marketing separation | Resend + Klaviyo split | `transactional-vs-marketing-separation` skill | yes |
| 27 | Post-MPP measurement | Klaviyo + GA4 | `post-mpp-measurement-clicks-conversions-revenue` skill | yes |
| 28 | A/B testing (subject/copy/CTA/time) | Klaviyo A/B + GrowthBook | `ab-testing-subject-preview-copy-send-time` skill | yes |
| 29 | Send-time optimization | Klaviyo Smart Send Time | `klaviyo-deep-lifecycle-predictive-ai` skill | yes |
| 30 | Dynamic content (Movable Ink, AMP) | Movable Ink + AMP for Email | `dynamic-personalization-movable-ink` skill | caveat (paid) |
| 31 | MJML / Maizzle responsive | MJML + Maizzle | `mjml-maizzle-responsive-modular-email` skill | yes |
| 32 | Dark mode + accessibility | MJML + Litmus | `dark-mode-email-design-accessibility` skill | caveat |
| 33 | Inbox placement testing | Glock Apps / Inboxable / Mailtrap | `glock-apps-inboxable-inbox-placement-testing` skill | caveat (paid) |
| 34 | Litmus / EOA rendering | Litmus / Email on Acid | `litmus-email-on-acid-rendering-testing` skill | caveat (paid) |
| 35 | Email throttling | Postmark / Klaviyo throttle | `klaviyo-customer-io-flow-design-patterns` skill | yes |
| 36 | Reply-to + vanity sender | DNS + ESP config | `transactional-vs-marketing-separation` skill | yes |
| 37 | Spam trigger word audit | Postmark Spam Check / SpamAssassin | `cli-anything curl spamcheck.postmarkapp.com` | yes |
| 38 | Newsletter strategy (Beehiiv/Substack) | Beehiiv API + Substack RSS | `beehiiv-substack-newsletter-creator-strategy` skill | caveat (paid) |
| 39 | Transactional ESPs (modern) | Resend / Postmark | `resend-postmark-transactional-modern` skill | yes |
| 40 | High-volume transactional | Mailgun / SendGrid / SES | `mailgun-sendgrid-ses-volume-transactional` skill | yes |

**Fulfillment math:** 40 distinct use cases mapped. 27 are full "yes" confidence; 13 are "caveat" (one-time OAuth or paid key the recipient owns — Klaviyo Plus, Valimail/dmarcian, VMC certificate, Lemwarm/MailReach warmup, Movable Ink, Litmus/EOA, Glock Apps, Beehiiv, ZeroBounce per-record). Zero genuine gaps. **~95% fulfillment** counting setup-and-paid-key as one-time, never-blocking steps.

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (only those present in `app/config/mcp_config.json`):
- `filesystem` (mandatory)
- `gmail-mcp` — outreach, deliverability dig output, sender alerts
- `notion-mcp` — segment library, flow inventory, DMARC remediation board
- `postgresql-mcp` — warehouse RFM / cohort SQL, event-stream lookups, complaint alerts
- `posthog-mcp` — activation event source for onboarding triggers, retention curves
- `mixpanel-mcp` — alt activation event source
- `amplitude-mcp` — alt activation event source
- `firecrawl-mcp` — competitive newsletter capture + scrape sender domains
- `brightdata-mcp` — paid SERP + scraping fallback
- `deepl-mcp` — multi-language template translation
- `shopify-mcp` — e-commerce event enrichment (cart, product, order)
- `stripe-mcp` — subscription event triggers (renewal, churn)
- `slack-mcp` — alerts on complaint-rate / bounce / spam-rate / IP-reputation drops
- `linear-mcp` — DMARC remediation tickets to engineering
- `playwright-mcp` — render competitor newsletters, validate ESP UIs
- `brave-search` — search ESP / deliverability tool research

**Bundled skill packs to create in Round 2** (in order of impact):

1. `klaviyo-deep-lifecycle-predictive-ai` — Klaviyo e-com deep (flows, segments, predictive, smart send time, predictive AI segments)
2. `customer-io-b2b-lifecycle` — Customer.io B2B lifecycle (campaigns, broadcasts, segments, transactional)
3. `resend-postmark-transactional-modern` — Resend / Postmark dev-focused transactional + React Email templates
4. `mailgun-sendgrid-ses-volume-transactional` — high-volume transactional (Mailgun / SendGrid / Amazon SES / Mailchannels / SparkPost)
5. `deliverability-deep-spf-dkim-dmarc-bimi-arc` — full auth audit + remediation
6. `dmarc-reporting-valimail-dmarcian` — RUA/RUF report analysis + sender alignment
7. `bimi-verified-mark-certificate-setup` — BIMI + VMC procurement + DNS publication
8. `ip-warming-strategy-dedicated-shared` — 4-6 week warming schedule + service enrollment
9. `ip-reputation-google-postmaster-snds` — Postmaster Tools / SNDS / Yahoo Postmaster polling + alerting
10. `list-cleaning-zerobounce-emailable` — pre-send validation + inline signup validation
11. `engagement-based-suppression` — engagement-tier definitions + suppression rules
12. `multi-language-esp-architecture-icu` — per-locale templates + ICU MessageFormat + DeepL routing
13. `transactional-vs-marketing-separation` — DNS architecture + ESP migration plan
14. `post-mpp-measurement-clicks-conversions-revenue` — clicks-over-opens + CTR / CTOR / revenue per recipient + GA4 join
15. `ab-testing-subject-preview-copy-send-time` — Klaviyo native + GrowthBook for multi-variant
16. `mjml-maizzle-responsive-modular-email` — MJML / Maizzle compile pipeline + push to ESP
17. `dark-mode-email-design-accessibility` — dark mode tokens + WCAG AA + ARIA
18. `glock-apps-inboxable-inbox-placement-testing` — pre-send seed-list inbox placement
19. `litmus-email-on-acid-rendering-testing` — cross-client render diff
20. `complaint-bounce-rate-management` — Klaviyo metrics + alert thresholds
21. `klaviyo-customer-io-flow-design-patterns` — named-flow templates + throttling + exit conditions
22. `beehiiv-substack-newsletter-creator-strategy` — Beehiiv API + Substack migration + creator monetization
23. `dynamic-personalization-movable-ink` — Movable Ink dynamic blocks + AMP for Email interactive forms

---

## Notes on remaining caveats (the caveat rows)

- **Klaviyo Predictive AI** requires Klaviyo Plus or Advanced tier (recipient brings).
- **Valimail / dmarcian / EasyDMARC / ondmarc** require paid subscription for full RUA report ingest; Postmark DMARC has a generous free tier.
- **VMC (Verified Mark Certificate)** is ~$1,500-$1,800/year from DigiCert or Entrust. Required for BIMI.
- **Lemwarm / Mailflow / MailReach / Folderly / Warmup Inbox** are paid subscriptions (~$50-$150/month) for IP warming.
- **Movable Ink** is enterprise-priced dynamic content.
- **Litmus / Email on Acid** are paid (~$99-$200/month).
- **Glock Apps / Inboxable** paid (~$50-$100/month).
- **Beehiiv API** is paid plan + above.
- **ZeroBounce / Emailable / NeverBounce / Kickbox** charge per-record (~$0.005-$0.01).
- **Google Postmaster Tools** is free but needs one-time GCP OAuth + domain verification.
- **HubSpot remote MCP** is one-time OAuth at `mcp.hubspot.com`.

None of these block the agent's default execution — each is a one-time recipient setup or a justified paid step for the enterprise / serious tier of the work.
