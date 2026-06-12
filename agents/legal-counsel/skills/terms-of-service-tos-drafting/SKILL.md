---
name: terms-of-service-tos-drafting
description: Draft customer Terms of Service / Terms & Conditions, marketplace ToS (multi-sided), and Acceptable Use Policy (AUP). Anchored on Bonterms Cloud Terms + Common Paper standardized terms + Section 230 (US) + EU Digital Services Act compliance overlays. Output is a complete .docx + memo with the consult-an-attorney disclaimer.
---

# Terms of Service Drafting — Customer T&C, Marketplace ToS, AUP

Use this skill to draft the **outbound** terms users / customers accept. For **inbound** contracts (your customer's MSA, vendor T&C), use `contract-review-msa-nda-employment`.

## When to use

User says:

- "Write our terms of service / T&C / ToS"
- "Draft a marketplace ToS"
- "Draft an Acceptable Use Policy"
- "What should our website ToS say?"
- "Update our SaaS T&C for [new feature]"

Companion skills:
- `privacy-policy-gdpr-ccpa` — privacy policy lives separately from ToS.
- `iubenda-termly-privacy-policy-generators` — if user wants generator-based ToS.
- `cookie-consent-management-cookiebot-onetrust` — cookie banner separately.
- `dpa-data-processing-agreement` — B2B DPA separately.

## Setup

```bash
# Fetch open templates
curl -fsSL -o bonterms-cloud-terms.docx https://bonterms.com/forms/cloud-terms
curl -fsSL -o bonterms-aup.docx https://bonterms.com/forms/acceptable-use-policy
curl -fsSL -o cp-cloud-service.html https://commonpaper.com/standards/cloud-service-agreement/

# Generators (alternative — see iubenda-termly skill)
# Iubenda: https://www.iubenda.com/en/terms-and-conditions-generator
# Termly: https://termly.io/products/terms-and-conditions-generator/

# Document I/O
which pandoc || brew install pandoc
which pdftotext || brew install poppler

# Optional Python helpers
pip install python-docx jinja2
```

Auth / API keys:
- `IUBENDA_API_KEY` — if generating via Iubenda (paid).
- `TERMLY_API_KEY` — if generating via Termly.
- No keys for Bonterms / Common Paper.

## Common recipes

### Recipe 1: Standard B2B SaaS ToS skeleton (Bonterms)
```bash
curl -fsSL https://bonterms.com/forms/cloud-terms -o cloud-terms.docx
pandoc cloud-terms.docx -o cloud-terms.md
```
Bonterms Cloud Terms is the leading 2026 open-source SaaS ToS template. Modular: pick the modules (DPA, AUP, SLA, BAA) you need. Use as base; customize the Order Form to match your product.

### Recipe 2: Standard B2C consumer ToS skeleton
```markdown
# Terms of Service

**Effective Date:** 2026-06-09
**Last Updated:** 2026-06-09

## 1. Acceptance of Terms
By accessing or using <Service>, you agree to be bound by these Terms.

## 2. Eligibility
You must be 13+ (or local age of digital consent) to use this Service.

## 3. Account
- You are responsible for the security of your account credentials.
- One account per person.
- Notify us of unauthorized use.

## 4. Acceptable use
- No illegal activity.
- No infringement.
- No automated scraping.
- No interference with other users / the service.
- See AUP at <url>.

## 5. User content
- You retain ownership of your content.
- You grant us a worldwide, royalty-free license to host, display, perform, and modify your content for the purpose of providing the Service.
- This license terminates when you delete your content (subject to backup retention).

## 6. Intellectual property
- The Service, including all software, designs, trademarks, is our property.
- These Terms do not grant any license to our IP except as expressly stated.

## 7. Termination
- You may terminate at any time by deleting your account.
- We may terminate or suspend immediately for material breach.
- Upon termination, sections 5 (license), 9 (warranties), 10 (liability), 12 (dispute resolution) survive.

## 8. Modifications
- We may modify these Terms; we will provide 30 days' notice for material changes.
- Continued use after the effective date is acceptance.

## 9. Disclaimers
- Service is provided "AS IS" without warranties of any kind.
- (Capitalized disclaimer block per state consumer-protection requirements.)

## 10. Limitation of liability
- We are not liable for indirect, incidental, consequential, special, or punitive damages.
- Aggregate liability capped at fees paid in the prior 12 months (or $100 if no fees).
- Some jurisdictions do not permit such limits — your statutory rights are not waived.

## 11. Indemnification
- You indemnify us for claims arising from your breach of these Terms or your use.

## 12. Dispute resolution
- Governing law: <state>, USA.
- Venue: <county>, <state>.
- Class action waiver + mandatory arbitration (AAA Commercial Rules) unless prohibited.
- 30-day pre-suit notice + good-faith negotiation.

## 13. Contact
<email + address>

---
**Disclaimer:** This is informational guidance from an AI agent. Always consult a licensed attorney in your jurisdiction before publishing or relying on these terms.
```

### Recipe 3: Marketplace ToS (three-party structure)
Marketplaces serving sellers + buyers + platform need:
```markdown
## Roles
- **Platform** = <Co.> — operates the marketplace, doesn't own listings.
- **Seller** = user who lists goods / services.
- **Buyer** = user who purchases.

## Section 230 (US) reliance
- Platform is an "interactive computer service" under 47 USC §230.
- Platform does not endorse seller content; not responsible for seller-listed accuracy.

## EU Digital Services Act (DSA) compliance (if EU-targeting)
- Trader identifiability: Seller must provide name, address, registration, contact.
- Internal complaint handling system.
- Statement of reasons for content removal.
- Notice-and-action mechanism.
- Out-of-court dispute settlement option.

## Seller terms
- Listing accuracy + lawfulness.
- Indemnify Platform for claims arising from Seller's listings.
- Payment + fee schedule.

## Buyer terms
- Purchase is between Buyer and Seller (not Platform).
- Platform processes payment as agent for Seller.
- Refund / dispute via Platform-mediated process first, then arbitration.

## Prohibited items / activities
- Comprehensive list (illegal, restricted, regulated).

## Escrow + chargebacks
- Payment held in escrow until delivery confirmation OR <N> days.
- Chargeback policy: Platform debits Seller for chargebacks; Seller can appeal.

## Termination
- Platform may delist or suspend sellers for violations.
- Buyer-protection program separately.

---
Disclaimer.
```

### Recipe 4: Acceptable Use Policy (AUP)
```markdown
# Acceptable Use Policy

You may not use the Service to:

## Illegal activity
- Violate any law, regulation, or third-party rights.
- Engage in fraud, money laundering, or tax evasion.

## Harmful content
- Threaten, harass, or stalk other users.
- Distribute child sexual abuse material (CSAM).
- Promote violence, terrorism, or discrimination.

## Infringement
- Infringe IP rights (copyright, trademark, patent, trade secret).
- Distribute pirated content.

## Security violations
- Probe, scan, or test vulnerability without authorization.
- Distribute malware, viruses, or harmful code.
- Bypass access controls or rate limits.

## Automated abuse
- Run automated scrapers, crawlers, or scripts at non-trivial volume without permission.
- Use the API in ways not documented or beyond rate limits.

## Spam + abuse
- Send unsolicited bulk messages (CAN-SPAM, CASL, TCPA compliance required).
- Manipulate engagement metrics.

## Enforcement
- Warning → suspension → termination, depending on severity.
- We may immediately suspend without notice for serious violations.

---
Disclaimer.
```

### Recipe 5: Order Form (Bonterms style)
```markdown
# Order Form

**Customer:** <legal entity>
**Effective Date:** <date>
**Order Term:** 12 months from Effective Date
**Auto-renewal:** Yes (annual) unless 30-day non-renewal notice
**Fees:** $<amount> per <month/year>, payable Net 30
**Payment method:** ACH / wire / credit card
**Plan:** <Plan Name>
**Service Levels:** 99.9% monthly uptime per SLA Module
**Permitted Use Cap:** <users / seats / API calls>
**Order-specific terms:**
- [ ] DPA Module attached (required if EU PII)
- [ ] BAA Module attached (required if PHI)
- [ ] Custom indemnity carve-out (see Schedule 1)

Bonterms Cloud Terms apply to this Order. Signed:
<Customer signature>
<Provider signature>
```

### Recipe 6: Click-through vs sign-here vs browse-wrap enforceability
| Pattern | US enforceability | EU / UK enforceability | Recommendation |
|---|---|---|---|
| Click-through ("I agree" button) | Strong | Strong | Default for SaaS / web |
| Sign-here (DocuSign / wet sig) | Strongest | Strongest | Use for B2B Order Forms |
| Scroll-wrap (must scroll then click) | Strong | Strong | UX-acceptable |
| Browse-wrap (link in footer) | Weak (Nguyen v. Barnes & Noble) | Weak | AVOID for paid services |
| Email-confirm | Moderate | Moderate | Add to click-through |

Always use click-through or sign-here for material terms; browse-wrap fails enforceability tests.

### Recipe 7: California consumer-protection overlays
- **Automatic Renewal Law (Cal. Bus. & Prof. Code §17602):** disclose auto-renewal terms before purchase + send reminder 3-21 days before renewal for terms over 6 months.
- **Right to Cancel (Cal. Civ. Code §1789.37):** specific cancellation methods for consumer subscriptions.
- **Shine the Light (Cal. Civ. Code §1798.83):** specific personal-info disclosure rights.
- **CCPA / CPRA cross-references:** privacy policy section reference + DNSMPI link.

### Recipe 8: EU DSA + Consumer Rights Directive overlays
- **DSA Art. 31 (large platforms):** notice-and-action, trader info, recommender transparency.
- **Consumer Rights Directive 2011/83/EU:** 14-day withdrawal right; specific info before contract.
- **Unfair Contract Terms Directive 93/13/EEC:** required plain-language; one-sided clauses voidable.

### Recipe 9: Verify the consult-an-attorney disclaimer is present
```bash
grep -i "consult a licensed attorney" output_tos.md || echo "MISSING DISCLAIMER — ABORT"
```

## Examples

### Example 1: B2B SaaS ToS for a US-based startup
**Goal:** Draft a Cloud Terms + Order Form bundle.
**Steps:**
1. Download Bonterms Cloud Terms (Recipe 1).
2. Customize Order Form (Recipe 5) — fees, term, plan, use cap.
3. Attach DPA Module if customer is in EU (`dpa-data-processing-agreement` skill).
4. Attach BAA Module if customer handles PHI.
5. Add AUP (Recipe 4) by reference.
6. Verify CA + EU overlays (Recipes 7-8) if shipping cross-border.
7. Add disclaimer + send to licensed counsel for sign-off.

**Result:** A complete ToS + Order Form package ready for click-through implementation.

### Example 2: Marketplace ToS for a peer-to-peer rental platform
**Goal:** Draft three-party ToS — platform, host, guest.
**Steps:**
1. Use Recipe 3 marketplace skeleton.
2. Add §230 statement (US).
3. If EU-targeting, add DSA-trader-identifiability + complaint-handling sections.
4. Add escrow + chargeback policy.
5. Add prohibited items list.
6. Add disclaimer + send to licensed counsel for sign-off.

**Result:** A marketplace ToS with three-party structure + DSA compliance.

## Edge cases / gotchas

- **Browse-wrap traps.** Burying ToS in a footer link with no affirmative acceptance fails Nguyen v. Barnes & Noble, 763 F.3d 1171 (9th Cir. 2014). Always click-through or scroll-wrap for material terms.
- **Class action waiver enforceability volatile by state.** Enforceable post-AT&T v. Concepcion in most states, but CA, NY, IL have specific carve-outs (PAGA in CA; consumer-fraud in NJ). Always pair with a severability clause.
- **EU consumer overrides US choice of law.** EU consumers retain mandatory protections regardless of US choice-of-law clauses (Rome I Regulation Art. 6). Don't assume Delaware law applies to EU consumers.
- **Marketplace ≠ publisher.** Section 230 protects intermediaries who don't materially contribute to content. Recommendation algorithms + paid promotion narrow §230 protection; defamation suits increasingly survive.
- **Auto-renewal disclosure rules in 18+ US states.** CA SB-1659 (2024) is the strictest — Reminder 3-21 days before renewal for terms over 6 months. Non-compliance makes the auto-renewal voidable.
- **GDPR DPA cannot live inside ToS.** Art. 28 DPA is a separate document with specific required terms. Don't try to fold it into the ToS body.
- **DMCA designated agent must be registered.** ToS should reference your designated agent + copyright.gov registration. See `dmca-takedown-process`.
- **AI-generated terms can include hallucinated citations.** Always verify any statute / regulation reference manually against Cornell LII before publication.

> Warning: **This is informational guidance from an AI agent. Always consult a licensed attorney in your jurisdiction before publishing or relying on Terms of Service or Acceptable Use Policy documents.**

## Sources

- [Bonterms Cloud Terms](https://bonterms.com/forms/cloud-terms) — leading open SaaS T&C template.
- [Bonterms AUP](https://bonterms.com/forms/acceptable-use-policy) — open AUP.
- [Common Paper Cloud Service Agreement](https://commonpaper.com/standards/cloud-service-agreement/) — alt open SaaS template.
- [EU Digital Services Act overview](https://commission.europa.eu/strategy-and-policy/priorities-2019-2024/europe-fit-digital-age/digital-services-act_en) — marketplace + large-platform obligations.
- [Cornell LII 47 USC §230](https://www.law.cornell.edu/uscode/text/47/230) — Section 230 text.
- [Cal. Bus. & Prof. Code §17602 (Auto-Renewal)](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=17602) — auto-renewal disclosure rules.
- [Nguyen v. Barnes & Noble, 763 F.3d 1171 (9th Cir. 2014)](https://www.courtlistener.com/opinion/2698127/nguyen-v-barnes-noble-inc/) — browse-wrap enforceability case.
- [AT&T Mobility v. Concepcion, 563 U.S. 333 (2011)](https://www.law.cornell.edu/supct/html/09-893.ZS.html) — arbitration + class-waiver case.
- [Iubenda ToS Generator](https://www.iubenda.com/en/terms-and-conditions-generator) — alternative generator.
- [Termly ToS Generator](https://termly.io/products/terms-and-conditions-generator/) — alternative generator.
