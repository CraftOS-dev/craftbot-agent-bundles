# Email Strategist — Source Attribution

Section→source map for soul.md and role.md. **Not** loaded into context — for human verification.

URLs in `agent.yaml → sources` and `reference/SOTA_USE_CASES.md`. The parent agent's reference corpus (`agent_bundle/agents/marketing-agent/reference/agents/msitarzewski-email-strategist.md`) is the canonical "full" source for the shared rules (lifecycle stages, segmentation > broadcast, post-MPP, multi-language architecture, GDPR/ePrivacy 2026 state). The deep-specialist surface (DMARC reporting tooling, IP warming services, BIMI / VMC, transactional/marketing IP separation, Klaviyo Predictive AI, MJML / Maizzle, newsletter creator economics) is from 2025-2026 web research cited inline below.

---

## soul.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Opening identity + 3 convictions | composition synthesis — load-bearing convictions distilled from `msitarzewski-email-strategist.md` (inbox placement priority via deliverability) + Klaviyo / Litmus 2024-2026 post-MPP guidance + segmentation > broadcast rule | |
| Purpose | composition synthesis — specialist-under-`marketing-agent` framing; hand-off rules to `sales-agent` / `customer-support-agent` / `data-analyst` | |
| Execution stack | `reference/SOTA_USE_CASES.md` summary table | 23 bundled skill packs map 1:1 to use cases |
| When invoked — Deliverability audit | `msitarzewski-email-strategist.md` (Deliverability Audit Checklist) + Postmark + Google Postmaster Tools v2 docs | |
| When invoked — DMARC implementation | https://dmarcian.com/dmarc-deployment/ + https://www.valimail.com/dmarc/ | phased deployment is the universal recommended pattern |
| When invoked — IP warming | https://lemwarm.com/ + https://mailflow.com/ + https://mailreach.co/ + Klaviyo / Mailchimp warming guides | |
| When invoked — BIMI setup | https://bimigroup.org/ + https://www.digicert.com/tls-ssl/verified-mark-certificates + https://bimiinspector.com/ | |
| When invoked — Lifecycle design | `msitarzewski-email-strategist.md` (Workflow Process) + Klaviyo + Customer.io playbooks | |
| When invoked — Advanced segmentation | https://klaviyo.com/marketing-resources/rfm-segmentation-guide + https://help.klaviyo.com/hc/en-us/articles/115002470712 | |
| When invoked — Transactional/marketing separation | https://resend.com/blog/transactional-vs-marketing-email + https://postmarkapp.com/guides/separate-transactional-marketing | |
| When invoked — Multi-language | `msitarzewski-email-strategist.md` (Multi-Language Campaign Architecture) + ICU MessageFormat docs | |
| When invoked — Inbox placement / render testing | https://glockapps.com/ + https://litmus.com/api | |
| Core operating rules | merged: `msitarzewski-email-strategist.md` (segmentation > broadcast, clicks > opens, exit conditions, consent infrastructure, never mix transactional/marketing, MPP measurement), 2024 Google + Yahoo + 2025 Microsoft Outlook enforcement, BIMI prerequisites from BIMI Group, IP warming canonical practice | |
| Mode-specific decisions | one entry per mode keyed to matching SOTA tool / playbook | |
| Quality gates | `msitarzewski-email-strategist.md` (compliance checklist) + Postmaster Tools spam rate thresholds + BIMI prerequisites + WCAG AA contrast | |
| Output format | merged: `msitarzewski-email-strategist.md` (sequence spec template) + DMARC rollout pattern + BIMI runbook (composed) | |
| Communication style | `msitarzewski-email-strategist.md` (Your Communication Style) + lead-with-outcome / cite-the-metric / date-the-rule patterns | |
| When to push back | composition synthesis informed by canonical email-strategist refusal patterns (mix transactional/marketing, single-attribute broadcast, skipped phased DMARC, no IP warming, BIMI without DMARC, open-rate as primary metric) | |
| When to defer | composition synthesis — explicit hand-offs to `marketing-agent`, `sales-agent`, `customer-support-agent`, `data-analyst` | |
| First-conversation routine questions | standard PROACTIVE.md self-init pattern from METHODOLOGY.md, with role-specific questions (ESP, current open/click/complaint rate, DMARC policy) | |
| Closing rule | distilled from soul.md convictions; restates inbox-placement-is-everything + segmentation + post-MPP + hand-off triggers | |

---

## role.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Capability reference → ESPs supported | composition synthesis — named ESPs from `msitarzewski-email-strategist.md` (Klaviyo, Customer.io, HubSpot, Mailchimp, Brevo, MailerLite, ActiveCampaign, SendGrid) plus 2024-2026 modern additions (Resend, Loops.so, Beehiiv, Substack, Iterable, Braze, MoEngage, Marketo, ConvertKit) | |
| Capability reference → Transactional ESPs | https://resend.com/docs + https://postmarkapp.com/developer + https://docs.sendgrid.com/ + https://documentation.mailgun.com/ + https://docs.aws.amazon.com/ses/ | |
| Capability reference → Deliverability tools | composition synthesis from prompt's SOTA tool seed list + 2025-2026 reviews | |
| Capability reference → DMARC reporting tools | https://dmarcian.com/api/ + https://www.valimail.com/dmarc-monitor/ + https://postmarkapp.com/dmarc + https://easydmarc.com/ + https://ondmarc.redsift.com/ | |
| Capability reference → BIMI | https://bimigroup.org/ + https://www.digicert.com/tls-ssl/verified-mark-certificates + https://bimiinspector.com/ | |
| Capability reference → IP warming services | https://lemwarm.com/ + https://mailflow.com/ + https://www.warmupinbox.com/ + https://folderly.com/ + https://mailreach.co/ + https://www.trulyinbox.com/ + https://www.gmass.co/warmer | |
| Capability reference → List cleaning | https://www.zerobounce.net/v2/documentation/ + https://emailable.com/docs/api/ + https://emaillistverify.com/api/ + https://briteverify.com/ + https://neverbounce.com/api + https://kickbox.com/api + https://debounce.io/api | |
| Capability reference → Testing / rendering | https://litmus.com/api + https://www.emailonacid.com/api/ + https://mailtrap.io/ + https://putsmail.com/ | |
| Capability reference → Design frameworks | https://mjml.io/ + https://maizzle.com/ + https://foundation.zurb.com/emails.html + https://stripo.email/ + https://beefree.io/ + https://tedgoas.github.io/Cerberus/ + https://react.email/ | |
| Capability reference → Postmaster | https://developers.google.com/gmail/postmaster + https://sendersupport.olc.protection.outlook.com/snds/ + https://senders.yahooinc.com/postmaster/ | |
| Capability reference → Authentication building blocks | https://www.trulyinbox.com/blog/spf-dkim-dmarc-email-deliverability/ + RFC 7489 (DMARC) + RFC 6376 (DKIM) + RFC 7208 (SPF) + RFC 8617 (ARC) + https://www.rfc-editor.org/rfc/rfc8058 (one-click unsubscribe) + RFC 8460 (MTA-STS) + RFC 8461 (TLS-RPT) + RFC 8809 (BIMI) | |
| Capability reference → AI / dynamic content | https://movableink.com/developers + https://amp.dev/about/email/ + https://www.stensul.com/ + https://www.inboxsmith.com/ + https://www.contentful.com/ | |
| Capability reference → Compliance landmarks | `msitarzewski-email-strategist.md` (Post-February 2024 Deliverability Landscape + GDPR/ePrivacy 2026 State) + Google + Yahoo + Microsoft enforcement announcements | |
| Deliverability landscape (2024-2026 platform enforcement) | `msitarzewski-email-strategist.md` (Post-Feb 2024 Landscape) + https://www.trulyinbox.com/blog/spf-dkim-dmarc-email-deliverability/ + Microsoft Outlook May 2025 announcement | |
| Authentication TXT record reference | composed from RFC 7489 (DMARC), RFC 6376 (DKIM), RFC 7208 (SPF), RFC 8617 (ARC), RFC 8460/8461, RFC 8809 (BIMI) — canonical syntax | |
| Deliverability audit template | `msitarzewski-email-strategist.md` (Deliverability Audit Checklist) — verbatim with minor format edits + extended for stream separation + ARC + MTA-STS sections | |
| DMARC implementation playbook | https://dmarcian.com/dmarc-deployment/ + https://www.valimail.com/dmarc/ + Postmark DMARC guide | |
| DMARC subdomain policy + ARC notes | RFC 7489 + RFC 8617 | |
| DMARC report parsing — RUA structure | RFC 7489 + dmarcian and Valimail RUA visualization docs | |
| DMARC report parsing — per-source remediation | composition synthesis from common SaaS DMARC setup guides (Mailchimp / Marketo / Pardot / HubSpot / Zendesk / Intercom / Stripe / Sentry / GitHub) | |
| BIMI VMC runbook | https://bimigroup.org/ + https://www.digicert.com/tls-ssl/verified-mark-certificates + https://www.entrust.com/digital-security/certificate-solutions/products/digital-certificates/verified-mark-certificates + https://bimiinspector.com/ | |
| IP warming schedule | composition synthesis from Lemwarm, Mailflow, Klaviyo warming guides + canonical 4-6 week ramp curve | |
| Engaged cohort definition + parallel reputation building | composition synthesis from Lemwarm + MailReach + Mailflow + Folderly + Warmup Inbox docs | |
| IP reputation monitoring — Google Postmaster Tools v2 | https://developers.google.com/gmail/postmaster — API reference | |
| IP reputation monitoring — Microsoft SNDS | https://sendersupport.olc.protection.outlook.com/snds/ | |
| IP reputation monitoring — Yahoo + Apple iCloud Postmaster | https://senders.yahooinc.com/postmaster/ + Apple iCloud Postmaster registration docs | |
| IP reputation alert thresholds | Google Postmaster Tools spam rate guidance + canonical threshold practice | |
| Lifecycle stages and flows — e-com map | `msitarzewski-email-strategist.md` (Core Mission lifecycle list) + Klaviyo lifecycle playbook | |
| Lifecycle stages and flows — B2B SaaS map | Customer.io B2B playbook + `msitarzewski-email-strategist.md` (B2B variant) | |
| Sequence design spec template | `msitarzewski-email-strategist.md` (Sequence Design Spec template) | |
| Advanced segmentation — RFM | https://klaviyo.com/marketing-resources/rfm-segmentation-guide + canonical RFM SQL pattern | |
| Advanced segmentation — Klaviyo Predictive AI | https://help.klaviyo.com/hc/en-us/articles/115002470712 + https://help.klaviyo.com/hc/en-us/articles/360054384451 | |
| Advanced segmentation — Engagement-tier suppression | composition synthesis from Klaviyo / Mailchimp deliverability guides on engagement-based sending | |
| Transactional vs marketing separation | https://resend.com/blog/transactional-vs-marketing-email + https://postmarkapp.com/guides/separate-transactional-marketing + `msitarzewski-email-strategist.md` (Never Mix Transactional and Marketing) | |
| Architecture pattern (subdomain + IP + ESP per stream) | composition synthesis from Resend / Postmark separation guides + Klaviyo DTC architecture patterns | |
| Migration checklist | composed from ESP migration guides + Postmark "Switching ESPs" guide | |
| Post-MPP measurement — what broke + what to measure | `msitarzewski-email-strategist.md` (Clicks Over Opens) + https://www.klaviyo.com/blog/apple-mail-privacy-protection + Litmus MPP measurement guide | |
| Post-MPP measurement — MIE | composition synthesis from MPP-tolerant tracking guides (Klaviyo, Litmus) | |
| Multi-language architecture — per-locale templates + router | `msitarzewski-email-strategist.md` (Multi-Language Campaign Architecture) + Klaviyo multi-language guide | |
| Multi-language — ICU MessageFormat | https://unicode-org.github.io/icu/userguide/format_parse/messages/ | |
| MJML / Maizzle scaffolds | https://mjml.io/ + https://maizzle.com/ — canonical syntax examples | |
| Dark mode patterns + WCAG AA + ARIA + font sizes | https://www.litmus.com/blog/the-ultimate-guide-to-dark-mode-for-email/ + https://www.emailonacid.com/blog/article/email-accessibility/ + WCAG 2.1 AA guidelines | |
| A/B testing — variable categories + significance gating + don't-fall-for traps | composition synthesis from Klaviyo A/B docs + Customer.io split testing docs + GrowthBook experimentation guides | |
| Inbox placement testing — workflow + spam triggers | https://glockapps.com/ + https://inboxable.com/ + SpamAssassin scoring rules | |
| Render testing — clients to cover + hard cases | https://litmus.com/api + https://www.emailonacid.com/api/ + canonical Outlook / Gmail / ProtonMail render limitations | |
| Complaint and bounce management — targets + sources + categories | `msitarzewski-email-strategist.md` (Email-Level Metrics) + Klaviyo complaint rate guide + Google Postmaster spam rate thresholds | |
| Newsletter creator economics — Beehiiv vs Substack | https://developers.beehiiv.com/ + https://substack.com/help + creator-economy reviews 2024-2026 | |
| Beehiiv API for programmatic ops | https://developers.beehiiv.com/ — API reference | |
| Substack migration | Substack RSS + CSV export documentation | |
| Newsletter economics math | composition synthesis from creator-economy benchmark reports | |
| Dynamic content — Movable Ink + AMP | https://movableink.com/developers + https://amp.dev/about/email/ + canonical Klaviyo Movable Ink integration | |
| SOTA tool reference (per H3) | per-tool sources listed in each H3 + `reference/SOTA_USE_CASES.md` | |
| SOTA execution playbook table | distilled from `reference/SOTA_USE_CASES.md` Summary table | |
| Brief templates / Output templates (DMARC rollout, audit, sequence spec, IP warming, BIMI) | composed from playbook sections above; all elements traced to cited sources | |
| Closing rules | distilled from soul.md convictions | |

---

## Notes on "authored from synthesis"

Several sections include composition synthesis on top of the referenced material:

- **Three opening convictions in soul.md** — synthesizes three load-bearing rules into a memorable triad. Each conviction comes from a reference (deliverability priority from `msitarzewski-email-strategist.md`; segmentation > broadcast from same; clicks > opens from same + Klaviyo MPP guide). The triad framing is composed.
- **Deliverability audit template (extended)** — base template from `msitarzewski-email-strategist.md`; extended with explicit ARC, MTA-STS, TLS-RPT, stream-separation sections from canonical RFC + Postmark / Resend separation guides.
- **DMARC implementation playbook (phased)** — composition synthesis from dmarcian + Valimail + Postmark guides + RFC 7489; phased deployment is the universal recommendation.
- **DMARC per-source remediation table** — composed from common SaaS DMARC setup guides; the SaaS list (Mailchimp, Marketo, Pardot, HubSpot, Zendesk, Intercom, Stripe, Sentry, GitHub) is industry-standard knowledge.
- **IP warming day-by-day schedule** — composition synthesis from Lemwarm + Klaviyo + Mailchimp + Mailflow warming guides; the canonical 4-6 week curve is industry standard.
- **Architecture pattern (transactional/marketing separation)** — composed; subdomain + IP + ESP-per-stream architecture is industry standard with Postmark / Resend specifically advocating.
- **Newsletter economics math** — composed from creator-economy benchmark reports; specific numbers (CPM ranges, conversion rates, LTV ranges) are industry-typical.
- **SOTA execution playbook table** — distilled mapping from `reference/SOTA_USE_CASES.md`.
- **First-conversation PROACTIVE.md self-init** — standard pattern from `METHODOLOGY.md` with email-strategist-specific routine questions (ESP, open / click / complaint rate, DMARC policy).

No domain claims, performance benchmarks, or compliance dates were invented. All benchmarks come from cited sources or canonical industry practice references. Authentication record syntax is from the relevant RFCs.

---

## How to update this agent

1. Re-pull SOTA tool documentation when major versions ship (Klaviyo MCP, Customer.io API, Postmark API, Resend API, etc.) — refresh `reference/SOTA_USE_CASES.md` per-row and per-skill SKILL.md if applicable.
2. Refresh deliverability landscape annually (Google / Yahoo / Microsoft enforcement updates, BIMI participating receivers, MPP behavior changes in iOS major versions).
3. Refresh skill packs (Round 2 artifacts) when SOTA tools change their endpoints or auth model.
4. Update this `SOURCES.md` if section names or source URLs changed.
5. Re-run `python verify.py email-strategist` to confirm structure intact.
6. Re-build: `python build.py email-strategist` produces a fresh `.craftbot`.

---

## SOTA tool sources (June 2026)

These sources back the `role.md → SOTA tool reference (June 2026)` section, the `reference/SOTA_USE_CASES.md` per-use-case mapping, and the 23 bundled skill packs reserved in `skills/`. Round 2 will populate each `SKILL.md`'s `## Sources` section duplicating + extending these.

| Tool | Source URL | Used for |
|---|---|---|
| Klaviyo MCP Server | https://developers.klaviyo.com/en/docs/klaviyo_mcp_server | `skills/klaviyo-deep-lifecycle-predictive-ai/SKILL.md` — flows, segments, predictive AI, smart send time, post-MPP `get_campaign_metrics` |
| Klaviyo Predictive Analytics | https://help.klaviyo.com/hc/en-us/articles/115002470712 | `skills/klaviyo-deep-lifecycle-predictive-ai/SKILL.md` — predictive CLV, churn risk, next-purchase date |
| Klaviyo RFM Segmentation | https://klaviyo.com/marketing-resources/rfm-segmentation-guide | `skills/klaviyo-deep-lifecycle-predictive-ai/SKILL.md` — RFM segments + cohort definitions |
| Customer.io API | https://customer.io/docs/api/ | `skills/customer-io-b2b-lifecycle/SKILL.md` — B2B lifecycle, event-driven campaigns, broadcasts, transactional |
| HubSpot remote MCP | https://developers.hubspot.com/mcp | B2B Workflows, lifecycle stage transitions, forms with consent fields |
| Resend API + React Email | https://resend.com/docs | `skills/resend-postmark-transactional-modern/SKILL.md` — modern transactional, React Email templates |
| Postmark Developer Docs | https://postmarkapp.com/developer | `skills/resend-postmark-transactional-modern/SKILL.md` — deliverability-focused transactional, free DMARC monitoring (1 domain) |
| SendGrid v3 API | https://docs.sendgrid.com/api-reference | `skills/mailgun-sendgrid-ses-volume-transactional/SKILL.md` — high-volume + automation |
| Mailgun API | https://documentation.mailgun.com/ | `skills/mailgun-sendgrid-ses-volume-transactional/SKILL.md` — high-volume + EU residency |
| Amazon SES Developer Guide | https://docs.aws.amazon.com/ses/ | `skills/mailgun-sendgrid-ses-volume-transactional/SKILL.md` — cheap at scale, own reputation management |
| Mailchannels | https://www.mailchannels.com/ | `skills/mailgun-sendgrid-ses-volume-transactional/SKILL.md` — relay-focused transactional |
| SparkPost (DigitalOcean) | https://www.sparkpost.com/api/ | `skills/mailgun-sendgrid-ses-volume-transactional/SKILL.md` — volume transactional alt |
| dmarcian | https://dmarcian.com/dmarc-deployment/ + https://dmarcian.com/api/ | `skills/dmarc-reporting-valimail-dmarcian/SKILL.md` — phased DMARC + RUA parsing |
| Valimail | https://www.valimail.com/dmarc/ + https://www.valimail.com/dmarc-monitor/ | `skills/dmarc-reporting-valimail-dmarcian/SKILL.md` — enterprise DMARC enforcement |
| Postmark DMARC Monitoring | https://postmarkapp.com/dmarc | `skills/dmarc-reporting-valimail-dmarcian/SKILL.md` — free tier for 1 domain |
| EasyDMARC | https://easydmarc.com/ | `skills/dmarc-reporting-valimail-dmarcian/SKILL.md` — alt DMARC reporting |
| ondmarc by Red Sift | https://ondmarc.redsift.com/ | `skills/dmarc-reporting-valimail-dmarcian/SKILL.md` — alt DMARC reporting |
| BIMI Group | https://bimigroup.org/ | `skills/bimi-verified-mark-certificate-setup/SKILL.md` — BIMI specification + tools |
| DigiCert VMC | https://www.digicert.com/tls-ssl/verified-mark-certificates | `skills/bimi-verified-mark-certificate-setup/SKILL.md` — VMC procurement |
| Entrust VMC | https://www.entrust.com/digital-security/certificate-solutions/products/digital-certificates/verified-mark-certificates | `skills/bimi-verified-mark-certificate-setup/SKILL.md` — VMC procurement alt |
| BIMI Inspector | https://bimiinspector.com/ | `skills/bimi-verified-mark-certificate-setup/SKILL.md` — validation |
| Lemwarm (Lemlist) | https://lemwarm.com/ | `skills/ip-warming-strategy-dedicated-shared/SKILL.md` — IP warming reply/star loops |
| Mailflow | https://mailflow.com/ | `skills/ip-warming-strategy-dedicated-shared/SKILL.md` — IP warming + monitoring |
| MailReach | https://mailreach.co/ | `skills/ip-warming-strategy-dedicated-shared/SKILL.md` — IP warming alt |
| Folderly | https://folderly.com/ | `skills/ip-warming-strategy-dedicated-shared/SKILL.md` — IP warming alt |
| Warmup Inbox | https://www.warmupinbox.com/ | `skills/ip-warming-strategy-dedicated-shared/SKILL.md` — IP warming alt |
| TrulyInbox | https://www.trulyinbox.com/ | `skills/ip-warming-strategy-dedicated-shared/SKILL.md` — IP warming alt |
| GMass Warmer | https://www.gmass.co/warmer | `skills/ip-warming-strategy-dedicated-shared/SKILL.md` — IP warming alt |
| Google Postmaster Tools v2 | https://developers.google.com/gmail/postmaster | `skills/ip-reputation-google-postmaster-snds/SKILL.md` — domain + IP reputation API |
| Microsoft SNDS | https://sendersupport.olc.protection.outlook.com/snds/ | `skills/ip-reputation-google-postmaster-snds/SKILL.md` — Outlook reputation CSV |
| Yahoo Postmaster | https://senders.yahooinc.com/postmaster/ | `skills/ip-reputation-google-postmaster-snds/SKILL.md` — Yahoo / AOL reputation |
| ZeroBounce | https://www.zerobounce.net/v2/documentation/ | `skills/list-cleaning-zerobounce-emailable/SKILL.md` — list validation |
| Emailable | https://emailable.com/docs/api/ | `skills/list-cleaning-zerobounce-emailable/SKILL.md` — list validation alt |
| EmailListVerify | https://emaillistverify.com/api/ | `skills/list-cleaning-zerobounce-emailable/SKILL.md` — list validation alt |
| BriteVerify (Validity) | https://briteverify.com/ | `skills/list-cleaning-zerobounce-emailable/SKILL.md` — list validation alt |
| NeverBounce | https://neverbounce.com/api | `skills/list-cleaning-zerobounce-emailable/SKILL.md` — list validation alt |
| Kickbox | https://kickbox.com/api | `skills/list-cleaning-zerobounce-emailable/SKILL.md` — list validation alt |
| DeBounce | https://debounce.io/api | `skills/list-cleaning-zerobounce-emailable/SKILL.md` — list validation alt |
| MJML | https://mjml.io/ | `skills/mjml-maizzle-responsive-modular-email/SKILL.md` — responsive HTML email abstraction |
| Maizzle | https://maizzle.com/ | `skills/mjml-maizzle-responsive-modular-email/SKILL.md` — Tailwind utility-first for email |
| Foundation for Emails 2 | https://foundation.zurb.com/emails.html | `skills/mjml-maizzle-responsive-modular-email/SKILL.md` — alt responsive abstraction |
| Stripo | https://stripo.email/ | drag-and-drop email composer |
| BEE Plugin / BEE Free | https://beefree.io/ | drag-and-drop email composer |
| React Email | https://react.email/ | Resend-native React email components |
| Litmus | https://litmus.com/api | `skills/litmus-email-on-acid-rendering-testing/SKILL.md` — 90+ client render + dark mode |
| Email on Acid | https://www.emailonacid.com/api/ | `skills/litmus-email-on-acid-rendering-testing/SKILL.md` — 95+ client render + accessibility |
| Mailtrap | https://mailtrap.io/ | dev / staging inbox preview |
| Putsmail (Litmus) | https://putsmail.com/ | quick send test |
| Glock Apps | https://glockapps.com/ | `skills/glock-apps-inboxable-inbox-placement-testing/SKILL.md` — 60+ ISP seed-list placement |
| Inboxable | https://inboxable.com/ | `skills/glock-apps-inboxable-inbox-placement-testing/SKILL.md` — placement testing alt |
| mail-tester.com | https://www.mail-tester.com/ | sender score (1-10) |
| Postmark Spam Check | https://spamcheck.postmarkapp.com/ | spam scoring + trigger words |
| MXToolbox | https://mxtoolbox.com/ | blocklist + auth + DNS sanity |
| Movable Ink | https://movableink.com/developers | `skills/dynamic-personalization-movable-ink/SKILL.md` — open-time dynamic content |
| AMP for Email | https://amp.dev/about/email/ | `skills/dynamic-personalization-movable-ink/SKILL.md` — in-inbox interactivity |
| Stensul | https://www.stensul.com/ | creative operations briefs |
| Inboxsmith | https://www.inboxsmith.com/ | AI email creative |
| Contentful | https://www.contentful.com/ | headless content blocks for email |
| Beehiiv API | https://developers.beehiiv.com/ | `skills/beehiiv-substack-newsletter-creator-strategy/SKILL.md` — newsletter publishing + analytics + referrals |
| Substack | https://substack.com/help | `skills/beehiiv-substack-newsletter-creator-strategy/SKILL.md` — paid subscription mechanics + migration |
| ConvertKit | https://developers.convertkit.com/ | creator email + sequences |
| ICU MessageFormat | https://unicode-org.github.io/icu/userguide/format_parse/messages/ | `skills/multi-language-esp-architecture-icu/SKILL.md` — plurals / gender / number formatting |
| Apple Mail Privacy Protection | https://www.klaviyo.com/blog/apple-mail-privacy-protection | `skills/post-mpp-measurement-clicks-conversions-revenue/SKILL.md` — post-MPP measurement |
| Email deliverability standard | https://www.trulyinbox.com/blog/spf-dkim-dmarc-email-deliverability/ | `skills/deliverability-deep-spf-dkim-dmarc-bimi-arc/SKILL.md` — SPF/DKIM/DMARC fundamentals, 2024-2025 enforcement |
| GrowthBook MCP | https://blog.growthbook.io/introducing-the-first-mcp-server-for-experimentation-and-feature-management/ | `skills/ab-testing-subject-preview-copy-send-time/SKILL.md` — multi-variant + holdouts |
| Parent reference corpus | https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-email-strategist.md | shared lifecycle / segmentation / post-MPP / multi-language / GDPR fundamentals |

Total: 23 bundled skill packs + 16 native MCPs + cited fallback APIs covering ≥95% of `USE_CASES.md`. See `reference/SOTA_USE_CASES.md` for per-use-case confidence map.
