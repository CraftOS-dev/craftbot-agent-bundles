---
name: ccpa-cpra-readiness-audit
description: Audit CCPA / CPRA readiness for California — applicability, consumer rights infrastructure, "Do Not Sell or Share" link, sensitive PI limit link, GPC signal, service-provider agreements, Cal AG + CPPA enforcement focus. Output is a gap-analysis report with the consult-an-attorney disclaimer. Pairs with `gdpr-readiness-audit` for cross-jurisdiction work.
---

# CCPA / CPRA Readiness Audit

## When to use

User says:

- "Audit our CCPA / CPRA compliance"
- "Are we California-compliant?"
- "Do we sell or share personal info under CCPA?"
- "Add a 'Do Not Sell or Share' link"
- "Implement GPC signal honoring"
- "Service provider agreement language for CPRA"
- "California Privacy Protection Agency (CPPA) audit prep"

Companion skills:
- `privacy-policy-gdpr-ccpa` — privacy policy text.
- `gdpr-readiness-audit` — sibling audit for EU.
- `cookie-consent-management-cookiebot-onetrust` — banner + GPC.

## Setup

```bash
# Fetch Cal AG + CPPA current guidance
curl -fsSL -o calag_ccpa.html https://oag.ca.gov/privacy/ccpa
curl -fsSL -o cppa_regs.html https://cppa.ca.gov/regulations/

# Full text — Cal. Civ. Code §1798.100 et seq.
# https://leginfo.legislature.ca.gov/faces/codes_displayexpandedbranch.xhtml?tocCode=CIV&division=3.&title=1.81.5.
curl -fsSL -o ccpa_text.html "https://leginfo.legislature.ca.gov/faces/codes_displayexpandedbranch.xhtml?tocCode=CIV&division=3.&title=1.81.5."

# CPPA Final Regulations (effective 2023+)
curl -fsSL -o cppa_final.pdf https://cppa.ca.gov/regulations/pdf/cppa_regs.pdf

# Python helpers
pip install pandas openpyxl
```

## Common recipes

### Recipe 1: Applicability check — are we subject to CCPA / CPRA?
```python
# applicability.py
# Apply if for-profit doing business in CA AND ANY of:
applies_ccpa = (
    annual_gross_revenue > 25_000_000 OR
    annually_buy_sell_share_personal_info_of >= 100_000_consumers_households_devices OR
    derive_50pct_or_more_revenue_from_selling_sharing_personal_info
)
print("CCPA / CPRA applies:", applies_ccpa)
```
"Doing business in CA" = significant CA presence — selling to CA consumers, employees in CA, etc.

### Recipe 2: Consumer rights infrastructure checklist
```markdown
- [ ] Right to know (specific pieces in 12 months; CPRA extends on request)
  - [ ] Disclosure of categories collected, sources, purposes, third parties
  - [ ] Disclosure of specific pieces (with verification)
- [ ] Right to delete (with statutory exceptions)
- [ ] Right to correct (CPRA-new, effective 2023)
- [ ] Right to opt out of sale
- [ ] Right to opt out of share (CPRA-new — cross-context behavioral advertising)
- [ ] Right to limit use of sensitive personal info (CPRA-new)
- [ ] Right to non-discrimination (no charging more / providing less service)
- [ ] Right to data portability
- [ ] Authorized agent submission
- [ ] Verification process (proportionate to risk)
- [ ] SLA: 45 days (extendable +45 days with notice)
- [ ] Fee policy: free for first 2 requests / 12 months; reasonable fee for manifestly unfounded
```

### Recipe 3: "Do Not Sell or Share My Personal Information" link
```html
<!-- Required on homepage + every page where PI is collected -->
<a href="/privacy/do-not-sell-or-share">Do Not Sell or Share My Personal Information</a>

<!-- Honor GPC signal (Recipe 9) — auto-treat as opt-out request -->
```
Location requirements (CCPA §1798.135):
- Homepage (clear and conspicuous link)
- Every page where PI is collected
- Privacy policy

Combined with sensitive PI link if applicable:
```html
<a href="/privacy/limit-sensitive">Limit Use of My Sensitive Personal Information</a>
```

### Recipe 4: CCPA categories of personal info — disclosure table
```python
import pandas as pd
categories = pd.DataFrame([
    {"category": "Identifiers", "examples": "Name, email, IP, SSN, account ID",
     "collected": "Yes", "sold_or_shared": "No"},
    {"category": "Customer records (Cal Civ §1798.80(e))", "examples": "Name, address, phone",
     "collected": "Yes", "sold_or_shared": "No"},
    {"category": "Protected class", "examples": "Race, religion, sexual orientation",
     "collected": "No", "sold_or_shared": "—"},
    {"category": "Commercial info", "examples": "Purchase records, preferences",
     "collected": "Yes", "sold_or_shared": "No"},
    {"category": "Biometric info", "examples": "Fingerprint, voiceprint",
     "collected": "No", "sold_or_shared": "—"},
    {"category": "Internet / network activity", "examples": "Browse history, interactions, ads",
     "collected": "Yes", "sold_or_shared": "Yes (analytics → CPRA 'share')"},
    {"category": "Geolocation", "examples": "Approx from IP; precise from app",
     "collected": "Yes (approx)", "sold_or_shared": "No"},
    {"category": "Sensory data", "examples": "Audio, video, electronic info",
     "collected": "No", "sold_or_shared": "—"},
    {"category": "Professional / employment", "examples": "Job title, employer",
     "collected": "Yes (B2B)", "sold_or_shared": "No"},
    {"category": "Education info (FERPA)", "examples": "School, transcript",
     "collected": "No", "sold_or_shared": "—"},
    {"category": "Inferences", "examples": "Behavioral profile, preferences",
     "collected": "Yes (with consent)", "sold_or_shared": "No"},
    {"category": "Sensitive PI (CPRA)", "examples": "Geo (precise), race, religion, mail/text content, biometric, health, sexual orientation, SSN, DL #, financial #",
     "collected": "No", "sold_or_shared": "—"},
])
categories.to_markdown("ccpa_categories.md", index=False)
```

### Recipe 5: "Sale" vs "Share" definitions (CPRA broadened both)
```text
SALE (CCPA §1798.140(ad)): "Selling, renting, releasing, disclosing, disseminating, making available, transferring, or otherwise communicating orally, in writing, or by electronic or other means, a consumer's personal information by the business to another business or a third party for monetary OR OTHER VALUABLE CONSIDERATION."

SHARE (CPRA §1798.140(ah)): "Sharing, renting, releasing, disclosing, disseminating, making available, transferring, or otherwise communicating orally, in writing, or by electronic or other means, a consumer's personal information by the business to a third party for cross-context behavioral advertising, whether or not for monetary or other valuable consideration."

Practical: most ad-tech pixel firing = "share." Many analytics integrations = "share" or "sale" depending on data flows. Audit each tag.
```

### Recipe 6: Service provider vs contractor vs third party
```text
SERVICE PROVIDER (CCPA §1798.140(ag), CPRA expanded):
- Processes PI on behalf of business per written contract
- Can't sell or share PI
- Can't use PI for own purposes or "cross-context behavioral advertising"
- Contract MUST include CPRA-specific terms

CONTRACTOR (CPRA-new):
- Like service provider but not under service-provider definition

THIRD PARTY:
- Anyone who isn't business, service provider, or contractor
- Sharing with third parties may = "sale" or "share"

Service provider contract MUST include (§1798.140(ag)(2)):
1. Process only for business purposes
2. No selling / sharing
3. No combining with other PI from other sources unless allowed
4. Notification of compliance
5. Right to take reasonable + appropriate steps to remediate
```

### Recipe 7: Privacy notice at collection (just-in-time)
```text
Required: at or before collection, disclose:
1. Categories of PI collected
2. Purposes for which used
3. Categories of sensitive PI collected (if applicable) + purposes
4. Whether sold or shared
5. Retention period (or criteria)
6. Link to full privacy policy

Format: clear, plain language; in collection context (form, signup, app onboarding).
```

### Recipe 8: Sensitive PI processing (CPRA new)
```text
Sensitive PI categories (CPRA §1798.140(ae)):
- Precise geolocation
- Racial / ethnic origin
- Religious / philosophical beliefs
- Union membership
- Mail / email / text message content
- Genetic data
- Biometric for unique identification
- Health
- Sex life / sexual orientation
- SSN, driver's license #, state ID, passport #
- Financial account / debit / credit card #
- Account credentials

If used for purposes other than:
- Performing services
- Detecting security incidents
- Resisting malicious / deceptive / fraudulent / illegal actions
- Short-term, transient use
- Performing services on behalf of business
- Verifying / maintaining quality

THEN must offer "Limit Use" right.
```

### Recipe 9: Global Privacy Control (GPC) signal
```javascript
// Detect GPC + treat as opt-out request
if (navigator.globalPrivacyControl) {
  // 1. Set opt-out cookie / state
  document.cookie = "ccpa_optout=1; max-age=31536000; SameSite=Lax; Secure";
  
  // 2. Update CMP state (Cookiebot / OneTrust / etc.)
  if (window.Cookiebot) Cookiebot.renew();
  
  // 3. Update Google Consent Mode v2
  gtag('consent', 'update', {
    'ad_storage': 'denied',
    'ad_user_data': 'denied',
    'ad_personalization': 'denied'
  });
  
  // 4. Backend acknowledgment via API
  fetch('/api/privacy/optout', { method: 'POST', body: JSON.stringify({source: 'GPC'}) });
}
```
CA AG enforcement focus 2024-2026: GPC honor is mandatory. Sephora $1.2M settlement (2022) hinged on GPC non-honor.

### Recipe 10: Authorized agent submission
```text
CCPA §1798.135(c) allows consumers to designate an authorized agent (e.g., privacy NGO, family member, attorney).

Required process:
1. Consumer signs written permission OR power of attorney
2. Agent submits request with proof
3. Business verifies BOTH:
   - Consumer's identity (per Recipe 2 verification)
   - Agent's authorization

Permission Slip / DataGrail / Transcend handle agent flows.
```

### Recipe 11: Verification methodology (CCPA Regs §7060-7064)
```text
Verification proportionate to:
- Type of request (delete > know specific pieces > know categories)
- Sensitivity of data
- Risk of harm

Methods:
- 2+ data points matching account records (low risk)
- 3+ data points + signed declaration (medium risk)
- Gov ID + signed declaration (high risk — delete sensitive PI)

Don't request MORE PI than necessary for verification.
```

### Recipe 12: CPPA enforcement focus areas (2024-2026)
```text
California Privacy Protection Agency (created by CPRA) enforcement focus:
1. Children's data (under 13 consent; opt-in for under 16 sale/share)
2. Dark patterns in consent flows
3. GPC signal honor
4. "Sensitive PI" handling (precise geo, biometric)
5. Service provider contractual compliance
6. Data broker registration + Delete Act compliance
```

### Recipe 13: CCPA audit gap-analysis report skeleton
```markdown
# CCPA / CPRA Readiness Audit — <Co.>

**Date:** 2026-06-09
**Auditor:** Legal Counsel (AI agent)
**Scope:** All processing of California consumer PI

## Executive summary
- HIGH gaps: <N>
- MED gaps: <N>
- LOW gaps: <N>

## Applicability
- Revenue: $X — meets §1798.140(d)(1)(A)? Y/N
- Consumer count: X — meets (B)? Y/N
- Revenue from PI sale: X% — meets (C)? Y/N
- **Subject to CCPA / CPRA:** Yes / No

## Findings
### 1. Privacy policy
- §1798.130 disclosures: ✓ / Gaps
- Annual update: ✓ / Gaps

### 2. Notice at collection
- Just-in-time notices: ✓ / Gaps

### 3. Consumer rights infrastructure
- Right to know: ✓ / Gaps
- Right to delete: ✓ / Gaps
- Right to correct: ✓ / Gaps
- Right to opt-out (sale + share): ✓ / Gaps
- Right to limit sensitive PI: ✓ / Gaps
- Right to non-discrimination: ✓ / Gaps

### 4. "Do Not Sell or Share" link
- Homepage: ✓ / Gaps
- Each PI collection page: ✓ / Gaps
- Method to submit (online + toll-free for online-only biz): ✓ / Gaps

### 5. GPC signal
- Honor GPC: ✓ / Gaps
- Document GPC implementation: ✓ / Gaps

### 6. Service provider contracts
- All vendors signed CPRA-compliant service provider agreement: ✓ / Gaps

### 7. Sensitive PI
- Map sensitive PI flows: ✓ / Gaps
- Limit Use link (if applicable): ✓ / Gaps

### 8. Verification + agent submission
- Documented verification process: ✓ / Gaps
- Authorized agent flow: ✓ / Gaps

### 9. Record retention + SLA tracking
- 45-day SLA tracker: ✓ / Gaps
- Records of requests (2 years): ✓ / Gaps

## Remediation plan
| Gap | Priority | Owner | Deadline |
|---|---|---|---|

---
**Disclaimer:** This is informational guidance from an AI agent. Always consult a licensed attorney in your jurisdiction before relying on this audit for compliance posture or regulatory filings.
```

## Examples

### Example 1: B2C SaaS first-time CCPA audit
**Goal:** Pre-CA-launch readiness.
**Steps:**
1. Recipe 1 applicability check.
2. Recipe 4 inventory categories of PI.
3. Recipe 5 audit "sale" + "share" — pay special attention to ad pixels + analytics.
4. Recipe 6 verify service-provider contracts (especially with analytics vendors).
5. Recipe 7-8 implement notice + sensitive PI handling.
6. Recipe 9 implement GPC.
7. Recipe 13 report with remediation plan.
8. Add disclaimer; send to licensed counsel.

**Result:** Audit + remediation plan ready to execute.

### Example 2: Adding a new analytics vendor — CCPA check
**Goal:** Add Mixpanel without triggering "sale" / "share."
**Steps:**
1. Review Mixpanel's CCPA service-provider contract addendum.
2. Confirm Mixpanel commits to no own-purpose use, no cross-context advertising.
3. Sign service-provider agreement.
4. Update privacy policy + Recipe 4 categories table.
5. Update sub-processor list.
6. Test GPC propagation through Mixpanel SDK.

**Result:** Compliant addition without "share" classification.

## Edge cases / gotchas

- **B2B exemption sunset.** Pre-CPRA, B2B contact info had carve-out; CPRA-effective 2023 closed it. B2B contact info now subject to CCPA/CPRA.
- **HR data subject to CCPA since 2023.** Employee + applicant data is now full CCPA — your HRIS, payroll, performance data fall under access / delete / correct rights.
- **"Cross-context behavioral advertising" is broad.** ANY use of data collected from one site/app to target ads on another = "share" — sweeps in most ad-tech integrations.
- **"Necessary and proportionate" purpose limitation.** Even with consent / disclosure, can't use PI for purposes incompatible with disclosed purposes.
- **Children + CCPA.** Sale / share of under-16 requires opt-in (not opt-out); under-13 requires parent opt-in.
- **De-identified data exemption is narrow.** Must meet specific technical + organizational standards (CCPA §1798.140(p)) to escape PI definition.
- **45-day SLA, not 1 month.** Different from GDPR (30 days). Extension allowed +45 days with notice.
- **CCPA fines: $2,500-$7,500/violation; CA AG fines via Unfair Competition Law.**
- **CPPA enforcement live since 2023.** First enforcement actions 2024+; expect ramp-up through 2026.
- **GPC = opt-out signal regardless of cookie banner state.** Even if user "Accepted All" cookies, GPC signal overrides to opt-out of sale/share. Don't double-prompt.
- **Right to delete exceptions.** Complete transaction, security incident, free speech, scientific research, legal obligation, internal use compatible with consumer expectations. Document refusal grounds.
- **Data broker registration (CA AB 1202 / Delete Act).** If you sell PI of CA consumers to third parties as a data broker, register annually + comply with CA Delete Act (effective 2026).
- **Multi-state coordination.** CO + CT + VA + others have similar but distinct laws. CA is strictest; comply with CA + add state-specific deltas.

> Warning: **This is informational guidance from an AI agent. Always consult a licensed attorney in your jurisdiction before relying on this audit for compliance posture, regulatory filings, or binding decisions.**

## Sources

- [California Attorney General — CCPA](https://oag.ca.gov/privacy/ccpa) — Cal AG enforcement.
- [California Privacy Protection Agency (CPPA)](https://cppa.ca.gov/) — current regs + enforcement.
- [Cal. Civ. Code §1798.100 et seq.](https://leginfo.legislature.ca.gov/faces/codes_displayexpandedbranch.xhtml?tocCode=CIV&division=3.&title=1.81.5.) — CCPA full text.
- [CPPA Final Regulations](https://cppa.ca.gov/regulations/) — implementing regulations.
- [Cal Delete Act AB 1202](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240SB362) — data broker registration.
- [Sephora $1.2M Settlement (2022)](https://oag.ca.gov/news/press-releases/attorney-general-bonta-announces-settlement-sephora-part-ongoing-enforcement) — first major CCPA enforcement; GPC non-honor.
- [Global Privacy Control](https://globalprivacycontrol.org/) — GPC spec.
- [IAPP US State Privacy Tracker](https://iapp.org/resources/article/us-state-privacy-legislation-tracker/) — multi-state coverage.
- Sister skills: `privacy-policy-gdpr-ccpa`, `gdpr-readiness-audit`, `cookie-consent-management-cookiebot-onetrust`.
