---
name: privacy-policy-gdpr-ccpa
description: Draft privacy policies that cover GDPR Art. 13 + 14, CCPA / CPRA §1798.130, state privacy laws (VA, CO, CT, UT, OR, TX, FL etc.), and product-specific data flows. Pair with `iubenda-termly-privacy-policy-generators` for generator-based output and `gdpr-readiness-audit` / `ccpa-cpra-readiness-audit` for the underlying compliance work.
---

# Privacy Policy — GDPR + CCPA + Multi-State Drafting

The agent's manual / hand-rolled privacy policy skill. For generator-based output, see `iubenda-termly-privacy-policy-generators`.

## When to use

User says:

- "Write our privacy policy"
- "Update our privacy policy for GDPR / CCPA / [new state]"
- "What should our privacy policy say?"
- "Add [analytics tool / pixel / sub-processor] to our policy"
- "Is our privacy policy compliant with [regulation]?"

Companion skills:
- `iubenda-termly-privacy-policy-generators` — generator alternative.
- `gdpr-readiness-audit` — underlying GDPR compliance.
- `ccpa-cpra-readiness-audit` — underlying CCPA compliance.
- `cookie-consent-management-cookiebot-onetrust` — cookies are separate.
- `dpa-data-processing-agreement` — B2B DPA separate.

## Setup

```bash
# Pull current ICO + Cal AG + EDPB guidance (changes frequently)
curl -fsSL -o ico_privacy.html https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/
curl -fsSL -o calag_ccpa.html https://oag.ca.gov/privacy/ccpa
curl -fsSL -o edpb_guidelines.html https://edpb.europa.eu/our-work-tools/general-guidance/guidelines-recommendations-best-practices_en

# Document I/O
which pandoc || brew install pandoc

# Optional: Iubenda / Termly generator (see sister skill)
# Optional: data-flow inventory via Spreadsheet
pip install pandas openpyxl
```

Auth / API keys: none required for manual drafting.

## Common recipes

### Recipe 1: Inventory data flows BEFORE drafting
The policy describes what you actually do. Always map first:
```python
# data_inventory.py
import pandas as pd
flows = pd.DataFrame([
    {"data": "Email", "purpose": "Account + transactional", "basis": "Contract (Art. 6(1)(b))",
     "retention": "Until account deletion + 30 days", "third_party": "SendGrid (sub-processor)"},
    {"data": "IP address", "purpose": "Security + fraud", "basis": "Legitimate interest (Art. 6(1)(f))",
     "retention": "90 days", "third_party": "Cloudflare"},
    {"data": "Behavioral analytics", "purpose": "Product improvement", "basis": "Consent (Art. 6(1)(a))",
     "retention": "26 months", "third_party": "PostHog (self-hosted) / GA4"},
    {"data": "Marketing pixels", "purpose": "Advertising", "basis": "Consent (Art. 6(1)(a))",
     "retention": "13 months", "third_party": "Meta, Google Ads"},
    {"data": "Payment method (tokenized)", "purpose": "Payment processing", "basis": "Contract (Art. 6(1)(b))",
     "retention": "7 years (tax/SOX)", "third_party": "Stripe"},
])
flows.to_markdown("data_inventory.md", index=False)
```

### Recipe 2: GDPR Art. 13 + 14 mandatory elements checklist
```markdown
- [ ] Identity + contact details of controller
- [ ] Contact details of DPO (if appointed)
- [ ] Purposes of processing
- [ ] Lawful basis under Art. 6 (and Art. 9 if special-category data)
- [ ] Legitimate interests of controller (if Art. 6(1)(f))
- [ ] Recipients / categories of recipients (sub-processors)
- [ ] International transfer mechanism (SCC, BCR, adequacy decision)
- [ ] Retention period or criteria
- [ ] Data subject rights (access, rectification, erasure, restriction, portability, objection, no automated decision-making)
- [ ] Right to withdraw consent (where Art. 6(1)(a) basis)
- [ ] Right to lodge complaint with supervisory authority
- [ ] Whether providing data is statutory / contractual + consequences
- [ ] Existence of automated decision-making + logic + consequences
```

### Recipe 3: CCPA / CPRA mandatory elements checklist
```markdown
- [ ] Categories of personal info collected (per CCPA categories)
- [ ] Categories of sources
- [ ] Business / commercial purposes
- [ ] Categories of third parties shared with
- [ ] Right to know
- [ ] Right to delete (with exceptions)
- [ ] Right to correct (CPRA-new)
- [ ] Right to opt out of sale / share
- [ ] Right to limit use of sensitive personal info (CPRA-new)
- [ ] Right to non-discrimination
- [ ] "Do Not Sell or Share My Personal Information" link (homepage + collection points)
- [ ] Methods to submit requests
- [ ] Verification process description
- [ ] Authorized agent submission process
```

### Recipe 4: State privacy laws checklist (15+ as of 2026)
| State | Statute | Effective | Notes |
|---|---|---|---|
| California | CCPA / CPRA | 2020 / 2023 | CPPA enforces |
| Virginia | VA CDPA | 2023 | AG enforces |
| Colorado | CO CPA | 2023 | AG + Universal Opt-Out |
| Connecticut | CT CTDPA | 2023 | AG enforces |
| Utah | UT UCPA | 2023 | Narrower; no AG fines first year |
| Iowa | IA ICDPA | 2025 | Narrower |
| Indiana | IN CDPA | 2026 | — |
| Tennessee | TN ICDPA | 2025 | Narrower |
| Montana | MT CDPA | 2024 | — |
| Texas | TX TDPSA | 2024 | Broad; AG enforces |
| Oregon | OR OCPA | 2024 | — |
| Delaware | DE PDPA | 2025 | — |
| Florida | FL FDBR | 2024 | Limited applicability ($1B+) |
| New Jersey | NJ DPA | 2025 | — |
| New Hampshire | NH PDPA | 2025 | — |
| Maryland | MD ODPPA | 2025 | Strictest data minimization |
| Minnesota | MN CDPA | 2025 | — |

For multi-state operations, draft to the strictest standard (typically CA + MD) and add state-specific addenda.

### Recipe 5: Privacy policy skeleton (GDPR + CCPA combined)
```markdown
# Privacy Policy

**Effective Date:** 2026-06-09
**Last Updated:** 2026-06-09

## 1. Controller information
<Co.>, <address>, <DPO email or contact>

## 2. Categories of personal information we collect
| Category (CCPA §1798.140) | Example | Collected? |
|---|---|---|
| Identifiers | Email, IP, account ID | Yes |
| Personal info under Cal. Civ. Code §1798.80(e) | Name, address | Yes |
| Protected class | (race, religion, etc.) | No |
| Commercial info | Purchase history | Yes |
| Internet activity | Browse / interaction logs | Yes |
| Geolocation | Approximate (from IP) | Yes |
| Sensory data | (audio / video) | No |
| Employment / education | — | No |
| Inferences | Behavior profiles | Yes (with consent) |
| Sensitive PI (CPRA) | Precise geo, biometric, etc. | No |

## 3. Sources
- Directly from you (account, forms, support)
- Automatic (cookies, pixels, server logs)
- Sub-processors (analytics, payment, support)

## 4. Purposes + lawful basis
| Purpose | GDPR Art. 6 basis | CCPA "business purpose" |
|---|---|---|
| Account + service delivery | Contract (b) | Yes |
| Security + fraud | Legitimate interest (f) | Yes |
| Marketing | Consent (a) | Yes (opt-out for sale/share) |
| Product analytics | Consent (a) | Yes |
| Legal compliance | Legal obligation (c) | Yes |

## 5. Recipients / sub-processors
- Stripe (payment, US)
- AWS (hosting, US/EU)
- SendGrid (email, US)
- PostHog (analytics, EU-hosted option available)
- See current sub-processor list: <url>

## 6. International transfers (GDPR Art. 44+)
- Transfers to US under EU-US Data Privacy Framework + EU SCCs (2021/914) where applicable
- Transfer Impact Assessment (TIA) on file per Schrems II

## 7. Retention
- Account data: until deletion + 30 days
- Payment data: 7 years (tax)
- Logs: 90 days (security)
- Marketing: until consent withdrawn

## 8. Your rights
### GDPR (EU / UK)
- Access, rectification, erasure, restriction, portability, objection, no automated decision-making
- Right to withdraw consent
- Right to complain to supervisory authority (ICO for UK; your local DPA for EU)

### CCPA / CPRA (CA)
- Right to know, delete, correct, opt out of sale/share, limit sensitive PI use, non-discrimination
- "Do Not Sell or Share My Personal Information" — <link>
- "Limit Use of My Sensitive Personal Information" — <link if applicable>

### Submit a request
- <portal URL> or <email>
- For CA: toll-free phone OR online form
- Verification process: <describe>
- Authorized agent: <describe>

## 9. Cookies
See Cookie Policy: <url>

## 10. Children
We do not knowingly collect from under-13 (COPPA) or under-16 (GDPR Art. 8).

## 11. Changes
We will notify of material changes via in-app + email + 30 days' lead time.

## 12. Contact
privacy@<co>.com
DPO (EU): dpo@<co>.com (if appointed)

---
**Disclaimer:** This is informational guidance from an AI agent. Always consult a licensed attorney in your jurisdiction before publishing or relying on a privacy policy.
```

### Recipe 6: Sub-processor list maintenance
```python
# sub_processors.py — keep this as your single source of truth
import pandas as pd
sp = pd.DataFrame([
    {"name": "Stripe", "purpose": "Payment processing", "data": "Payment method (tokenized), email, name",
     "location": "US, IE", "dpa_url": "https://stripe.com/privacy-center/legal"},
    {"name": "AWS", "purpose": "Hosting", "data": "All service data",
     "location": "US, EU, UK", "dpa_url": "https://aws.amazon.com/service-terms/"},
    {"name": "SendGrid", "purpose": "Transactional email", "data": "Email, name, content",
     "location": "US", "dpa_url": "https://www.twilio.com/legal/data-protection-addendum"},
    {"name": "PostHog", "purpose": "Product analytics", "data": "Pseudonymized user ID, events",
     "location": "EU", "dpa_url": "https://posthog.com/dpa"},
])
sp.to_markdown("sub_processors.md", index=False)
# Update privacy policy link with timestamp; surface in DPA appendices
```

### Recipe 7: Verify all required disclosures
```bash
# checklist.sh
required=(
  "Controller" "Lawful basis" "Recipients" "International transfer"
  "Retention" "Right to access" "Right to erasure" "Right to portability"
  "Right to lodge complaint" "Categories of personal information" "Do Not Sell"
  "Verification" "consult a licensed attorney"
)
for term in "${required[@]}"; do
  grep -qi "$term" privacy_policy.md || echo "MISSING: $term"
done
```

### Recipe 8: Layer for COPPA (under-13)
If service is "directed to children" or you have actual knowledge of under-13 users:
- Verifiable parental consent (16 CFR §312.5)
- Limited data collection
- Right to review + delete
- No marketing without separate consent
- See: https://www.ftc.gov/business-guidance/privacy-security/childrens-privacy

## Examples

### Example 1: SaaS startup launching in US + EU
**Goal:** Draft a privacy policy for a B2B SaaS with EU + US customers.
**Steps:**
1. Run Recipe 1 data inventory.
2. Walk Recipes 2 + 3 mandatory-elements checklists.
3. Customize Recipe 5 skeleton.
4. Build sub-processor list (Recipe 6); publish at a stable URL.
5. Cross-link to Cookie Policy (`cookie-consent-management-cookiebot-onetrust`) and DPA (`dpa-data-processing-agreement`).
6. Verify all disclosures (Recipe 7).
7. Send to licensed counsel for sign-off.

**Result:** A GDPR + CCPA compliant privacy policy with US + EU coverage.

### Example 2: Adding a new analytics sub-processor
**Goal:** Add PostHog to existing privacy policy.
**Steps:**
1. Update Recipe 1 data inventory.
2. Update Recipe 6 sub-processor list.
3. Update §5 Recipients in privacy policy.
4. If processing changes substantively, notify users (Recipe 5 §11 modification clause).
5. Update DPA appendix.
6. Update Cookie Policy if PostHog drops cookies.

**Result:** A policy reflecting the new sub-processor with version control.

## Edge cases / gotchas

- **Copying from a competitor.** Verbatim copy = (a) copyright infringement on the text, (b) misalignment with actual data practices = FTC §5 deception + state AG enforcement. Always draft from your own data inventory.
- **Generators don't know your sub-processors.** Iubenda / Termly produce a base policy; YOU must add your specific sub-processor list. The generator-based policy without customization is incomplete.
- **Lawful basis mapping mismatches.** You can't claim "consent" if you require the data for service delivery (consent must be freely given — EDPB Guidelines 05/2020). Use "contract" for service-essential data.
- **Cookies need a SEPARATE policy + banner.** Privacy policy mentions cookies; doesn't replace the banner consent or cookie-specific policy. See `cookie-consent-management-cookiebot-onetrust`.
- **CCPA "sale" + "share" definitions are broader than you'd think.** Sharing analytics data with Google Analytics can count as "share" for cross-context behavioral advertising. Audit your tag stack.
- **Maryland Online Data Privacy Act (MODPA) effective 2025.** Strictest data minimization in US. If MD-targeting, plan for purpose-limited processing without "broad" consent.
- **Children's data + COPPA verification.** Reasonable methods are listed in 16 CFR §312.5 — credit card verification, gov ID, signed consent form via email, etc. Just-clicking-a-box does NOT meet the standard.
- **EU-US Data Privacy Framework status.** Validated July 2023; challenge expected (Schrems III). Track current status via EDPB.
- **DPO designation triggers.** Public authority, OR core activities = regular & systematic large-scale monitoring, OR large-scale special-category. If borderline, document the decision in a memo.
- **Privacy notice "at collection" + full policy.** CCPA requires a short notice at point of collection AND a full policy. Don't conflate.
- **Sensitive PI (CPRA) opt-out.** Precise geo, biometric, race/ethnicity, religion, mail/email/text content, genetic, health, sexual orientation, SSN, driver's license — must have a separate opt-out mechanism IF you use sensitive PI beyond required service.

> Warning: **This is informational guidance from an AI agent. Always consult a licensed attorney in your jurisdiction before publishing or relying on a privacy policy.**

## Sources

- [GDPR — Eur-Lex Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj) — full text.
- [ICO UK GDPR Guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/) — practical interpretations.
- [EDPB Guidelines](https://edpb.europa.eu/our-work-tools/general-guidance/guidelines-recommendations-best-practices_en) — official GDPR enforcement guidance.
- [California AG CCPA page](https://oag.ca.gov/privacy/ccpa) — CCPA + CPRA enforcement.
- [California Privacy Protection Agency (CPPA)](https://cppa.ca.gov/) — current enforcement.
- [IAPP State Privacy Tracker](https://iapp.org/resources/article/us-state-privacy-legislation-tracker/) — state law map.
- [FTC Children's Privacy](https://www.ftc.gov/business-guidance/privacy-security/childrens-privacy) — COPPA guidance.
- [EU-US Data Privacy Framework](https://www.dataprivacyframework.gov/) — current DPF status.
- [EU Standard Contractual Clauses 2021/914](https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/standard-contractual-clauses-scc_en) — international transfer mechanism.
- Sister skill: `iubenda-termly-privacy-policy-generators`.
