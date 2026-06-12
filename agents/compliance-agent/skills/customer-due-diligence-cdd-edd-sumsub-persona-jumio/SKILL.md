---
name: customer-due-diligence-cdd-edd-sumsub-persona-jumio
description: Integrate KYC vendors — Sumsub (14k+ doc types; crypto-native; MiCA + FinCEN aligned), Persona (customizable workflows), Jumio (enterprise ID-doc + facial liveness; 5k doc types / 200 countries), Onfido (Entrust subsidiary), Trulioo (global ID + KYB), Veriff, Alloy (orchestration layer chaining multiple vendors). Document + biometric + database verification in one flow. EDD for high-risk customers; ongoing rescreening.
---

# KYC Vendor Integration — CDD + EDD

KYC is execution layer for the BSA CIP + CDD obligations (see `aml-kyc-bsa-ofac-fincen-fatf`). 2026 SOTA stack: Sumsub for breadth, Persona for customization, Jumio for enterprise scale, Onfido as enterprise alternative, Trulioo for global KYB, Veriff for fast onboarding, Alloy for orchestrating multiple vendors per risk tier.

## When to use

User says:
- "KYC vendor selection" / "Sumsub vs Persona vs Jumio"
- "Identity verification" / "ID-doc verification"
- "Facial liveness" / "selfie check"
- "KYB" / "Know Your Business"
- "Onfido" / "Trulioo" / "Veriff" / "Alloy"
- "MiCA KYC" / "crypto onboarding"
- "Document fraud detection"
- "PEP screening" / "watchlist screening at onboarding"

Companion skills: `aml-kyc-bsa-ofac-fincen-fatf`, `sanctions-transaction-monitoring-comply-advantage`, `gdpr-article-30-ropa-dpia`.

## Setup

```bash
# Vendor docs + sandbox
# Sumsub: https://developers.sumsub.com/
# Persona: https://docs.withpersona.com/
# Jumio: https://docs.jumio.com/production/Content/Integration/Welcome.htm
# Onfido: https://documentation.onfido.com/api/latest
# Trulioo: https://developer.trulioo.com/
# Veriff: https://developers.veriff.com/
# Alloy: https://docs.alloy.com/

export SUMSUB_APP_TOKEN=<dashboard>
export SUMSUB_SECRET_KEY=<dashboard>
export PERSONA_API_KEY=<dashboard>
export JUMIO_API_TOKEN=<dashboard>
export JUMIO_API_SECRET=<dashboard>
export ONFIDO_API_TOKEN=<dashboard>
export TRULIOO_API_USERNAME=<dashboard>
export TRULIOO_API_PASSWORD=<dashboard>
export VERIFF_API_KEY=<dashboard>
export ALLOY_WORKFLOW_TOKEN=<dashboard>

# DocV (document verification) standards
# ISO/IEC 18013-5 (mDL — mobile driver's license)
# eIDAS (EU) — qualified digital identity
# NIST SP 800-63-3 (IAL2 / IAL3 levels)
```

Auth notes:
- All vendors offer sandbox tokens with synthetic data sets.
- Sumsub + Jumio have AWS / Azure region selection (EU vs US) for GDPR.
- Pricing: tier-based; typically $1-$5 per verification at low volume; sub-$1 at scale.

## Common recipes

### Recipe 1: Vendor selection guide (2026)

```text
Sumsub — pick when:
- Crypto / Web3 (MiCA + FinCEN aligned out of box)
- Breadth of document support critical (14k+ types, 220+ countries)
- All-in-one (KYC + KYB + sanctions + AML + Travel Rule + DocV)
- Cost-sensitive at scale

Persona — pick when:
- Customizable workflows for branded/embedded experience
- Engineering team prefers flexibility
- Growth-stage stablecoin / fintech / marketplace

Jumio — pick when:
- Enterprise scale (millions of verifications/yr)
- Need 5k+ document types from 200 countries
- AI ID-doc + facial liveness + AML+KYC bundle
- Procurement requires Tier 1 Forrester Wave vendor

Onfido (Entrust subsidiary) — pick when:
- Existing Entrust IAM / PKI relationship
- UK / EU strong
- IAL2-compliant flows

Trulioo — pick when:
- Global KYB (business verification) primary need
- 195+ country corporate registry coverage

Veriff — pick when:
- Speed-first onboarding (sub-2-min)
- Strong EU privacy posture
- Volume-based pricing favorable

Alloy — pick when:
- Multi-vendor orchestration (route to different vendors per risk tier)
- Hybrid US bank/MSB needing CDD + KYB + adverse media via single API
```

### Recipe 2: Sumsub applicant flow

```bash
# Create applicant
curl -X POST 'https://api.sumsub.com/resources/applicants' \
  -H "X-App-Token: $SUMSUB_APP_TOKEN" \
  -H "X-App-Access-Sig: <HMAC>" \
  -H "X-App-Access-Ts: $(date +%s)" \
  -H "Content-Type: application/json" \
  -d '{
    "externalUserId": "user_001",
    "info": {
      "firstName": "John",
      "lastName": "Doe",
      "country": "USA"
    },
    "type": "individual"
  }'

# Generate access token for client SDK
curl -X POST 'https://api.sumsub.com/resources/accessTokens?userId=user_001&levelName=basic-kyc-level' \
  -H "X-App-Token: $SUMSUB_APP_TOKEN"

# Check applicant status
curl -X GET 'https://api.sumsub.com/resources/applicants/<applicantId>/status' \
  -H "X-App-Token: $SUMSUB_APP_TOKEN"
```

### Recipe 3: Persona inquiry creation

```bash
# https://docs.withpersona.com/reference/create-an-inquiry
curl -X POST 'https://withpersona.com/api/v1/inquiries' \
  -H "Authorization: Bearer $PERSONA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "attributes": {
        "inquiry-template-id": "itmpl_xxx",
        "reference-id": "user_001"
      }
    }
  }'

# Webhook handler: subscribe to inquiry.completed / inquiry.failed events
```

### Recipe 4: Jumio Netverify

```bash
# https://docs.jumio.com/production/IDV/Documents/
curl -X POST 'https://netverify.com/api/v4/accounts' \
  -u "$JUMIO_API_TOKEN:$JUMIO_API_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"customerInternalReference": "user_001"}'

# Retrieve verification result
curl -X GET 'https://netverify.com/api/netverify/v2/scans/<scanReference>' \
  -u "$JUMIO_API_TOKEN:$JUMIO_API_SECRET"
```

### Recipe 5: Onfido check

```bash
# https://documentation.onfido.com/api/latest
# Create applicant
curl -X POST 'https://api.onfido.com/v3.6/applicants' \
  -H "Authorization: Token token=$ONFIDO_API_TOKEN" \
  -d '{"first_name": "John", "last_name": "Doe"}'

# Create check (document + facial similarity)
curl -X POST 'https://api.onfido.com/v3.6/checks' \
  -H "Authorization: Token token=$ONFIDO_API_TOKEN" \
  -d '{"applicant_id": "<id>", "report_names": ["document", "facial_similarity_photo"]}'
```

### Recipe 6: Trulioo Identity Verification + Business Verification

```bash
# https://developer.trulioo.com/docs
# Identity verify (multi-country)
curl -X POST 'https://api.globaldatacompany.com/verifications/v1/verify' \
  -u "$TRULIOO_API_USERNAME:$TRULIOO_API_PASSWORD" \
  -H "Content-Type: application/json" \
  -d '{
    "AcceptTruliooTermsAndConditions": true,
    "Demo": false,
    "CountryCode": "US",
    "DataFields": {
      "PersonInfo": {"FirstGivenName": "John", "FirstSurName": "Doe", "DayOfBirth": 1, "MonthOfBirth": 1, "YearOfBirth": 1980},
      "Location": {"BuildingNumber": "123", "StreetName": "Main", "City": "Anytown", "StateProvinceCode": "CA", "Country": "US", "PostalCode": "94000"}
    }
  }'

# KYB business search
curl -X POST 'https://api.globaldatacompany.com/business/v1/search' \
  -u "$TRULIOO_API_USERNAME:$TRULIOO_API_PASSWORD" \
  -d '{"CountryCode": "US", "BusinessName": "Acme Corp"}'
```

### Recipe 7: Veriff session

```bash
# https://developers.veriff.com/
curl -X POST 'https://stationapi.veriff.com/v1/sessions' \
  -H "X-AUTH-CLIENT: $VERIFF_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "verification": {
      "person": {"firstName": "John", "lastName": "Doe"},
      "vendorData": "user_001"
    }
  }'
```

### Recipe 8: Alloy orchestration (multi-vendor routing)

```bash
# https://docs.alloy.com/
# Alloy routes the request based on workflow logic (e.g., low risk →
# document only; high risk → document + selfie + sanctions + adverse media).

curl -X POST 'https://sandbox.alloy.co/v1/evaluations' \
  -H "Authorization: Basic <base64(workflow_token:workflow_secret)>" \
  -H "Content-Type: application/json" \
  -d '{
    "name_first": "John",
    "name_last": "Doe",
    "document_ssn": "123-45-6789",
    "address_line_1": "123 Main",
    "address_city": "Anytown",
    "address_state": "CA",
    "address_postal_code": "94000",
    "address_country_code": "US",
    "birth_date": "1980-01-01"
  }'
```

### Recipe 9: KYB (Know Your Business) workflow

```text
Layered KYB requires:
1. Entity verification — registered name, registration #, incorporation
   date, status (active/dissolved/struck-off).
2. Address verification — registered office.
3. Beneficial ownership — 25%+ owners + control prong (CEO/CFO/etc.).
4. UBO identity verification — full KYC on each UBO.
5. Sanctions + PEP + adverse media on entity + UBOs.
6. Industry / SIC code review for high-risk industries (gambling, MSB,
   crypto, cannabis, adult).

Vendors with strong KYB:
- Trulioo (195+ country registries)
- Sumsub (KYB module)
- Persona (KYB via Marketplace integrations)
- Middesk (US LLCs / corps deep)
- LexisNexis Risk Solutions

US-specific: FinCEN Corporate Transparency Act BOIR (Beneficial Ownership
Information Reporting; effective Jan 1, 2024) — reporting companies file
beneficial ownership directly with FinCEN. KYB vendors may incorporate
FinCEN BOIR data.
```

### Recipe 10: Liveness detection (facial)

```text
Active liveness — user performs action (blink, turn head, smile).
- Pro: harder to spoof.
- Con: user friction; abandonment.

Passive liveness — analysis of selfie/video without user action.
- Pro: smoother UX.
- Con: research-grade attacks possible.

Hybrid — passive default; active fallback for ambiguous cases.

Standards:
- ISO/IEC 30107-3 — PAD (Presentation Attack Detection) testing standard.
  Level 1 (printed photo), Level 2 (digital screen), Level 3 (mask/3D),
  Level 4 (deepfake).
- iBeta / FIDO Alliance PAD-certified.

2026 standout: Sumsub + Jumio + Veriff all iBeta Level 2 certified;
Sumsub + Jumio offer Level 3 / 4.
```

### Recipe 11: EDD additional collection (high-risk customer)

```markdown
# Enhanced Due Diligence — <Customer ID>

**Risk tier:** High
**Trigger(s):** <PEP / high-risk jurisdiction / industry / volume>
**EDD Decision Date:** <date>
**EDD Approver:** <senior compliance>

## Additional collection

### Source of Funds (SoF)
- Origin of funds being deposited: <employment / business / investment
  return / inheritance / sale of asset>
- Supporting docs: <pay stubs, business bank statements, tax returns, sale
  contract>

### Source of Wealth (SoW)
- How the customer accumulated overall wealth: <career trajectory, 
  inheritance, investment, business sale>
- Supporting docs: <CV/résumé, business ownership records, asset records,
  press coverage>

### Expected Activity
- Account type: <e.g., trading, custody, transfer>
- Expected volume: <monthly $ + transaction count>
- Expected counterparties: <list / categories>
- Expected geographies: <list>

### Ownership / Control Clarification
- Beneficial owners >10% (lower threshold than 25% for EDD)
- Trust + beneficiary disclosure (if applicable)
- Family / associate links (PEP-adjacent screening)

### Sanctions + PEP + Adverse Media
- Re-screen with deeper coverage (Refinitiv WorldCheck / Dow Jones)
- Adverse media search beyond 5 years

### Ongoing monitoring
- Re-screen daily (vs weekly for medium / monthly for low)
- TM alerts at lower thresholds
- Quarterly senior compliance review

---
*Disclaimer per template.*
```

### Recipe 12: KYC denial template

```markdown
# Application Decline Notification

**Date:** <YYYY-MM-DD>
**Reference:** <Application ID>

Dear <name>,

We are unable to approve your account application at this time.

Should you have questions, please contact <compliance email>.

Please note: under <jurisdiction> law, we are not permitted to disclose
specific reasons for this decision.

Regards,
<Co.> Compliance Team

---
Internal note (NOT shared with applicant):
- Reason: <sanctions match / failed document verification / failed liveness
  / suspected fraud / negative adverse media / PEP w/o approval>
- Retention: 5 years per BSA
- SAR consideration: <Y/N — if Y, file separately>
```

### Recipe 13: Periodic refresh (ongoing CDD)

```text
Risk-tier-driven refresh cadence:
- Low: every 3 years
- Medium: every 2 years
- High: annually

Refresh triggers (any tier):
- Material change in customer profile (address, employment, ownership)
- Material change in transaction patterns (volume jump 3x, new geography)
- Adverse media or sanctions list match
- Regulator inquiry
- Account dormant >12 months reactivation
```

## Examples

### Example 1: Crypto exchange MVP — Sumsub all-in

**Goal:** Stand up KYC + KYB + sanctions + Travel Rule for crypto exchange MVP.

**Steps:**
1. Sumsub sandbox; pick "crypto" level template.
2. Configure: ID-doc + selfie liveness + PoA (proof of address) + PEP/sanctions.
3. Embed Sumsub WebSDK in onboarding flow.
4. Webhook handler: applicant.reviewed → activate account; applicant.rejected → decline.
5. Enable Sumsub Travel Rule for crypto withdrawals.
6. Production cutover with EU + US AWS regions configured.

**Result:** Single-vendor stack covering KYC + KYB + Travel Rule + sanctions.

### Example 2: Marketplace requires KYB + KYC of UBOs

**Goal:** Marketplace onboards sellers; verify business + each UBO 25%+.

**Steps:**
1. Trulioo Business Verification — entity check (Recipe 6).
2. Capture UBOs from entity record OR direct seller input.
3. Persona inquiry per UBO (Recipe 3); KYC each.
4. Decision logic: all UBOs pass + entity clean → activate seller.
5. Annual refresh cadence (Recipe 13).

**Result:** Layered KYB + UBO KYC; CDD-compliant marketplace.

### Example 3: High-risk customer EDD

**Goal:** PEP family member applies; trigger EDD.

**Steps:**
1. Sanctions screen flags PEP-adjacent (RCA — Related Close Associate).
2. EDD per Recipe 11; collect SoF + SoW + expected activity.
3. Senior Compliance Officer approval before activation.
4. Daily re-screening; TM thresholds halved.
5. Annual EDD refresh; document.

**Result:** PEP-compliant onboarding; auditable trail.

## Edge cases / gotchas

- **Multi-vendor orchestration (Alloy)** routes by risk; ensure data sharing is GDPR-compliant per Art. 28 DPAs between vendors.
- **Liveness vs document only** — document-only KYC is cheaper but riskier for fraud. AML rule sets often require liveness for high-value accounts.
- **mDL (mobile driver's license) acceptance** is growing (ISO 18013-5). Sumsub + Jumio + Persona support; not all customers have mDL yet.
- **Indian Aadhaar / EU eID** — country-specific schemes; check vendor coverage per launching jurisdiction.
- **Customer-supplied selfie attacks** — deepfake-generated selfies are 2026 critical attack vector. iBeta Level 3+ PAD or active liveness required.
- **Failed verification = SAR consideration** — repeated verification failure with same identifier can indicate fraud. Document + SAR if pattern.
- **Data residency** — Sumsub, Jumio, Persona offer region selection (EU vs US data centers). Critical for GDPR Art. 28 + Schrems II.
- **PII retention** — KYC docs retained 5 years post-account closure per BSA; but GDPR storage limitation principle requires defensible retention schedule.
- **KYC vendor as processor** — DPA mandatory per Art. 28 GDPR. Audit SOC 2 / ISO of KYC vendor annually.
- **Synthetic identity fraud** — combination of real + fake info; KYC alone misses; pair with fraud-graph (Socure, SentiLink, Forter).
- **KYB beneficial ownership accuracy** — registry data may be stale; CTA BOIR helps US but other jurisdictions vary.
- **PEP classification varies** — FATF + EU broad (domestic + foreign + intl org); US BSA narrower (foreign mainly). Apply broader FATF definition for safety.
- **Pricing per verification** — ranges $1-$10 typical; jumps for biometric / adverse media / KYB. Model unit economics carefully.

> ⚠ **This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.**

## Sources

- [Sumsub](https://sumsub.com/)
- [Sumsub Developer Docs](https://developers.sumsub.com/)
- [Persona](https://withpersona.com/)
- [Persona API](https://docs.withpersona.com/)
- [Jumio](https://www.jumio.com/)
- [Jumio Developer](https://docs.jumio.com/)
- [Onfido](https://onfido.com/)
- [Onfido API](https://documentation.onfido.com/)
- [Trulioo](https://www.trulioo.com/)
- [Trulioo Developer](https://developer.trulioo.com/)
- [Veriff](https://www.veriff.com/)
- [Veriff Developer](https://developers.veriff.com/)
- [Alloy](https://alloy.com/)
- [Alloy Docs](https://docs.alloy.com/)
- [iBeta PAD certification](https://www.ibeta.com/)
- [ISO/IEC 30107-3 PAD](https://www.iso.org/standard/79520.html)
- [NIST SP 800-63-3 Digital Identity](https://pages.nist.gov/800-63-3/)
- [FinCEN Beneficial Ownership Information Reporting](https://www.fincen.gov/boi)
