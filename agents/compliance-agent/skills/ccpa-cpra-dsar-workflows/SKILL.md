---
name: ccpa-cpra-dsar-workflows
description: Handle Data Subject Access Requests (GDPR Art. 15-22) + Data Subject Rights requests (CCPA / CPRA / state privacy laws). Cover identity verification, lawful denial grounds, response packet assembly, GPC (Global Privacy Control) signal handling, "Do Not Sell or Share" + "Limit Use of Sensitive PI" links. SOTA platforms: Transcend / Securiti / DataGrail / OneTrust DSR / Ketch. Free fallback: ICO + Cal AG templates.
---

# DSAR / DSR Workflows — GDPR + CCPA + CPRA + US State Privacy

GDPR Art. 15 access, Art. 16 rectify, Art. 17 erasure (RTBF), Art. 18 restriction, Art. 20 portability, Art. 21 objection, Art. 22 no automated decision. CCPA right to know + delete + correct + opt-out of sale/share + limit sensitive PI use + non-discrimination. US state laws (19+ as of 2026 — VA, CO, CT, UT, OR, TX, FL, MT, IA, DE, NJ, NH, MD, IN, KY, MN, NE, RI, TN) layer their own variants.

## When to use

User says:
- "DSAR" / "Data Subject Access Request" / "GDPR access request"
- "DSR" / "Data Subject Rights request"
- "Right to know" / "Right to delete" / "Right to correct" / "Right to opt out"
- "CCPA / CPRA workflow" / "Cal AG"
- "GPC" / "Global Privacy Control" / "browser opt-out signal"
- "RTBF" / "Right To Be Forgotten" / "Article 17"
- "Identity verification for DSAR"
- "Data portability" / "Article 20"
- "Limit use of sensitive PI"

Companion skills: `gdpr-article-30-ropa-dpia`, `data-classification-dlp-purview-nightfall`, `data-retention-deletion-policy`.

## Setup

```bash
# Free templates
# ICO subject access request template
curl -fsSL https://ico.org.uk/for-the-public/your-right-of-access/ > /tmp/ico_sar.html

# Cal AG CCPA right-to-know template + denials
curl -fsSL https://oag.ca.gov/privacy/ccpa > /tmp/cal_ag_ccpa.html

# CPPA regulations
curl -fsSL https://cppa.ca.gov/regulations/ > /tmp/cppa_regs.html

# GPC technical spec
curl -fsSL https://globalprivacycontrol.org/ > /tmp/gpc.html

# IAPP US State Privacy Tracker (live)
curl -fsSL https://iapp.org/resources/article/us-state-privacy-legislation-tracker/ > /tmp/iapp_state.html

# Paid SOTA platforms (recipient supplies API token)
export TRANSCEND_API_KEY=<transcend-dashboard>
export SECURITI_API_KEY=<securiti-dashboard>
export DATAGRAIL_API_KEY=<datagrail-dashboard>
export ONETRUST_API_KEY=<onetrust-dashboard>
export KETCH_API_KEY=<ketch-dashboard>
```

Auth notes:
- All five paid platforms require tenant-issued API tokens.
- Transcend is unique: end-to-end encryption — Transcend never accesses user data; processing happens in your own infra via Transcend's orchestration layer.

## Common recipes

### Recipe 1: Rights matrix (GDPR vs CCPA/CPRA vs US states)

| Right | GDPR | CCPA | CPRA (added) | Common state (CO/CT/VA/UT) |
|---|---|---|---|---|
| Access / Know | Art. 15 | §1798.110 (12mo) | Extended on request | Yes |
| Rectify / Correct | Art. 16 | (CPRA-new §1798.106) | Yes | Yes |
| Erasure / Delete | Art. 17 | §1798.105 | Same | Yes |
| Restriction | Art. 18 | N/A | N/A | N/A |
| Portability | Art. 20 | §1798.130 | Same | Limited |
| Objection | Art. 21 | §1798.120 (opt-out sale/share) | §1798.120 + share | Yes |
| Limit sensitive PI | N/A (Art. 9 + 22) | N/A | §1798.121 | UT/CO/CT yes |
| Automated decision | Art. 22 | (limited) | Cap on profiling | Some states |
| Non-discrimination | (implicit Art. 12-22) | §1798.125 | Same | Yes |

### Recipe 2: Response timeline

```text
GDPR (Art. 12):
- 1 month from receipt
- Extendable to 3 months for complex / numerous requests (notify within 1mo)
- FREE for first request in 12 months; "reasonable fee" for repeated /
  unfounded / excessive

CCPA / CPRA:
- 45 days from receipt
- Extendable to 90 days (one 45-day extension; notify within first 45)
- 2x free per 12 months; reasonable fee thereafter

US state laws (typical):
- 45 days (VA, CO, CT, UT, OR, TX, FL, MT, IA, DE, NJ, NH, MD, IN, KY, MN, NE, RI, TN)
- Some allow 60-day extension

HIPAA (45 CFR §164.524):
- 30 days from receipt
- Extendable to 60 days (one 30-day extension)
```

### Recipe 3: Identity verification before disclosure

```text
GDPR (Recital 64): "Use all reasonable measures to verify identity."
CCPA: "Reasonable methods" — based on type of PI requested + harm of
disclosure to wrong person.

Verification methods (tier by data sensitivity):

Low sensitivity (e.g., account opt-out):
- Confirmed email link click (existing on-file address)
- Logged-in session

Medium sensitivity (e.g., access to PI):
- 2-3 personal info matches (name + email + DoB OR transaction ID)
- Account password + MFA

High sensitivity (e.g., sensitive PI, financial, health):
- Multi-factor: government ID + selfie OR notarized affidavit
- Authorized agent: separate verification per Cal AG regs

Refusal: if identity cannot be verified after reasonable attempts, deny with
written explanation. Do NOT disclose to unverified party.
```

### Recipe 4: GDPR Art. 15 access response packet

```markdown
# Subject Access Response — Request <ID>

**Date received:** <YYYY-MM-DD>
**Date responded:** <YYYY-MM-DD>
**Data subject:** <verified identity>

## 1. Purposes of processing
<List per ROPA — by activity>

## 2. Categories of personal data
<List per ROPA>

## 3. Recipients / categories of recipients
<Internal teams + external processors>

## 4. Retention period or criteria
<Per retention schedule>

## 5. Rights summary
<Rectify, erase, restrict, port, object, withdraw consent, complain to SA>

## 6. Source of data (if not from subject)
<Public records / referrer / third party>

## 7. Automated decision-making (Art. 22) involved?
<Y/N + logic + significance + consequences if Y>

## 8. International transfers + safeguards
<List per ROPA>

## 9. Personal data (copy)
<Structured export from systems — JSON / CSV / PDF>

---
*This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.*
```

### Recipe 5: CCPA right-to-know response packet

```markdown
# CCPA Right-to-Know Response — Request <ID>

**Date received:** <YYYY-MM-DD>
**Date responded:** <YYYY-MM-DD>
**Consumer:** <verified identity>

## Categories of PI collected in past 12 months
- Identifiers (name, email, account ID, IP address)
- Customer records (transactional, contact)
- Internet activity (page views, browser metadata)
- Geolocation (city-level)
- Inferences (segmentation labels)

## Categories of sources
- Directly from consumer (forms, account)
- Service providers (analytics, payment)
- Third parties (referrer)

## Categories of business purposes
- Service delivery
- Security + fraud prevention
- Customer support
- Service improvement
- Compliance

## Categories of third parties shared with
- Payment processor (Stripe)
- Hosting (AWS)
- Customer support (Zendesk)
- Analytics (Segment, Amplitude)
- (CPRA: "share" for cross-context behavioral ads — separate disclosure)

## Specific pieces of PI (if requested)
<JSON / CSV export>

---
*Disclaimer per template.*
```

### Recipe 6: Erasure (Art. 17 / §1798.105) decision matrix

```text
GRANT erasure UNLESS one of:

GDPR Art. 17(3) exceptions:
- Exercise of right to freedom of expression + information
- Compliance with legal obligation (e.g., AML retention, tax records)
- Public interest in public health
- Archiving in public interest, scientific / historical research, statistics
- Establishment, exercise, defense of legal claims

CCPA §1798.105(d) exceptions:
- Complete transaction in progress
- Detect security incidents / protect against fraud
- Repair errors that impair functionality
- Exercise free speech / ensure right of others
- Compliance with CalECPA
- Engage in research subject to specific ethical standards
- Solely internal uses reasonably aligned with consumer expectations
- Compliance with legal obligation
- Otherwise use the personal info internally, in a lawful manner compatible
  with the context

Document the denial reason in the response. Partial erasure (only data not
covered by exception) is required where feasible.
```

### Recipe 7: Erasure cascade — what systems get touched

```text
Erasure must propagate to:

Primary stores:
- Production DB (Postgres / MySQL / DynamoDB)
- Application backends
- Customer support tools (Zendesk, Intercom)
- CRM (Salesforce, HubSpot)
- Marketing (Mailchimp, Klaviyo, Iterable)

Analytics + product:
- Segment, Amplitude, Mixpanel
- Product analytics
- Heap, FullStory

Backups + DR:
- Backups (NOTE: deletion from backups within reasonable timeframe per
  retention schedule; usually next backup cycle expiry)
- DR replicas

Logs + audit:
- Application logs (Datadog, Splunk, Sumo Logic) — selective
- Audit logs (preserve hashed reference if needed for legal)

Sub-processors:
- Hosting (AWS S3, GCS — overwrites)
- Email (SES, SendGrid, Postmark)

Document destruction certificate per sub-processor; retain proof of erasure.
```

### Recipe 8: GPC (Global Privacy Control) handling

```text
Cal AG enforcement priority + CPRA-codified.

Treat GPC signal (HTTP header `Sec-GPC: 1` or DOM `navigator.globalPrivacyControl`) as:
- Opt-out of sale (CCPA §1798.120)
- Opt-out of share for cross-context behavioral ads (CPRA §1798.120)
- Opt-out of targeted advertising (state law equivalents)

Implementation:
1. Detect signal server-side (request header) AND client-side (DOM check).
2. Persist as user preference linked to identifier (cookie ID, account ID,
   IP address — coarse).
3. Honor across sessions + devices to the extent feasible.
4. Disclose recognition in privacy policy.
5. Do NOT require additional verification for GPC opt-out (CPPA reg).

Test: visit your site with Brave / Firefox GPC-enabled or DuckDuckGo browser
extension; verify opt-out applied.
```

### Recipe 9: "Do Not Sell or Share My Personal Information" link

```text
Required (CPRA §1798.135):
- Homepage + every page collecting PI
- Title: "Do Not Sell or Share My Personal Information" (exact)
- Clear + conspicuous (per Cal AG dark-pattern enforcement)
- Click → opt-out workflow (no account login required)

Additional CPRA-required link (if you process sensitive PI):
- "Limit the Use of My Sensitive Personal Information" (exact title)
- Same conspicuousness requirements

Many orgs combine into one "Your Privacy Choices" page (CCPA recognizes
"Your Privacy Choices" + opt-out icon as alternative — Cal AG icon at
oag.ca.gov).
```

### Recipe 10: Transcend DSR fulfillment via API

```bash
# https://docs.transcend.io/
# Submit DSR
curl -X POST 'https://api.transcend.io/v1/data-subject-request' \
  -H "Authorization: Bearer $TRANSCEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "ERASURE",
    "subject": {"email": "user@example.com"},
    "regime": "GDPR"
  }'

# Check status
curl -X GET 'https://api.transcend.io/v1/data-subject-request/<id>' \
  -H "Authorization: Bearer $TRANSCEND_API_KEY"
```

### Recipe 11: DataGrail DSR via API

```bash
# https://docs.datagrail.io/
curl -X POST 'https://api.datagrail.io/v1/requests' \
  -H "Authorization: Bearer $DATAGRAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "delete", "email": "user@example.com"}'
```

### Recipe 12: OneTrust DSR via API

```bash
# https://developer.onetrust.com/
curl -X POST 'https://app.onetrust.com/api/datasubject/v3/datasubject/requestqueue' \
  -H "Authorization: Bearer $ONETRUST_API_KEY" \
  -d '{"requestType": "DELETE", "datasubject": {"email": "user@example.com"}}'
```

### Recipe 13: Authorized agent handling

```text
CCPA + CPRA allow consumers to use an authorized agent (e.g., Mine, Permission
Slip).

Verification:
- Written authorization from consumer (signed)
- OR power of attorney
- AND verify identity of consumer themselves (CPPA reg)

Process flow:
1. Agent submits on behalf of consumer.
2. Request consumer's written permission (within 10 days; pause clock).
3. Verify consumer identity per Recipe 3.
4. Process per consumer's right.
5. Respond to agent unless consumer specifies direct response.
```

### Recipe 14: Lawful denial template

```markdown
# Denial of Data Subject Rights Request — <ID>

**Date received:** <YYYY-MM-DD>
**Date responded:** <YYYY-MM-DD>
**Request type:** <Access / Erasure / etc.>

## Reason for denial / partial denial

<Cite specific exception:
- Identity could not be verified
- Legal retention obligation (cite law, e.g., 26 U.S.C. § 6001 for tax)
- Conflict with other person's rights (Art. 17(3)(a))
- Frivolous / excessive (cite history)
- Other lawful basis>

## Right to complain
You have the right to lodge a complaint with the supervisory authority:
- EU/EEA: <list relevant SA> (Art. 77 GDPR)
- UK: ICO (ico.org.uk)
- California: California Privacy Protection Agency (cppa.ca.gov)
- <Other state>: <relevant AG / agency>

You may also seek judicial remedy (Art. 79 GDPR).

---
*This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.*
```

## Examples

### Example 1: First GDPR erasure request — small SaaS

**Goal:** Process Art. 17 RTBF in 30 days.

**Steps:**
1. Receive request via privacy@<co>.
2. Acknowledge within 7 days.
3. Verify identity via existing account login + email confirmation (Recipe 3 — medium tier).
4. Decision per Recipe 6: no exceptions apply. Grant.
5. Erasure cascade per Recipe 7: production DB + Stripe + Zendesk + Mailchimp + Segment + backups (next cycle).
6. Document destruction confirmations.
7. Respond per Recipe 4 (modified for erasure scope).
8. ROPA reflects completed deletion.

**Result:** Compliant erasure; documented chain-of-custody.

### Example 2: Bulk CCPA right-to-know

**Goal:** Handle 500 requests/month at scale.

**Steps:**
1. Deploy DataGrail (Recipe 11) — broadest US integrations.
2. Auto-verify via account login + email link.
3. Trigger system-side fetches (DB + Segment + CRM + Mailchimp).
4. Auto-assemble PDF response per Recipe 5.
5. Email signed encrypted PDF to verified address.
6. Track 45-day SLA per request.

**Result:** Sub-1% SLA breach rate; auditable trail.

### Example 3: GPC implementation

**Goal:** Honor GPC signal site-wide.

**Steps:**
1. Server middleware: detect `Sec-GPC: 1` header.
2. Set persistent opt-out cookie (encrypted; 13-month expiry per CCPA).
3. Disable third-party ad pixels (Meta Pixel, Google Ads tag) for opt-out users.
4. Honor at account level if user logged in.
5. Update privacy policy to disclose GPC handling.
6. Test with Brave + DuckDuckGo browser extension.

**Result:** GPC compliance; Cal AG enforcement risk reduced.

## Edge cases / gotchas

- **Identity verification cannot be more burdensome than the request would have been to honor.** Asking for ID for an opt-out request is over-verification per CPPA.
- **Erasure from backups** — most regulators accept "next backup cycle expiry" as reasonable. Document the schedule.
- **Sub-processor cascade**. Erasure must propagate to ALL processors. Maintain DPA-required deletion proof.
- **Partial denials** — disclose what you CAN'T delete (legal retention) and what you DID delete; never silently retain.
- **45-day vs 1-month** — CCPA 45 days is calendar days; GDPR 1 month is "one month" (calendar — ICO interpretation).
- **Authorized agent abuse** — verify consumer separately; agents (Mine, Permission Slip) sometimes submit bulk requests without consumer confirmation.
- **GPC is REQUIRED to be honored under CPRA;** Cal AG has actively enforced (Sephora 2022 $1.2M, DoorDash 2023 settlement).
- **"Sale" includes data brokerage** — any transfer to a third party for monetary OR other valuable consideration. Free analytics like GA4 with ad personalization counts in some interpretations.
- **State variation.** Some states (UT) require opt-in for sensitive PI; others (CO) require opt-out + universal opt-out signal recognition. Build a per-state policy engine.
- **Children's data** — COPPA verifiable parental consent required for under 13; CPRA opt-in for under 16 sale/share.
- **Penalties.** CCPA: $2,500 per violation; $7,500 if intentional or involving children's data. GDPR: up to €20M or 4% global revenue.
- **Logged-out users.** GPC + opt-out cookie covers anonymous browsing; tie to account on next login.

> ⚠ **This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.**

## Sources

- [GDPR Art. 12-23 (Data Subject Rights)](https://gdpr-info.eu/chapter-3/)
- [CCPA full text](https://oag.ca.gov/privacy/ccpa)
- [CPRA + CPPA regulations](https://cppa.ca.gov/regulations/)
- [Global Privacy Control spec](https://globalprivacycontrol.org/)
- [Cal AG GPC enforcement (Sephora 2022)](https://oag.ca.gov/news/press-releases/attorney-general-bonta-announces-settlement-sephora-part-ongoing-enforcement)
- [ICO Right of access guidance](https://ico.org.uk/your-data-matters/your-right-of-access/)
- [IAPP US State Privacy Tracker](https://iapp.org/resources/article/us-state-privacy-legislation-tracker/)
- [Transcend](https://www.transcend.io/)
- [Securiti.ai](https://securiti.ai/)
- [DataGrail](https://www.datagrail.io/)
- [OneTrust DSR](https://www.onetrust.com/products/data-subject-rights/)
- [Ketch](https://www.ketch.com/)
- [Mine — consumer agent](https://www.saymine.com/)
