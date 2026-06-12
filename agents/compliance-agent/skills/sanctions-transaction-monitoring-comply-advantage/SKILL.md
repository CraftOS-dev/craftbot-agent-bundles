---
name: sanctions-transaction-monitoring-comply-advantage
description: Real-time sanctions + PEP + adverse media screening via ComplyAdvantage (AI real-time, proprietary DB), Refinitiv World-Check, Dow Jones Watchlist, LexisNexis Bridger XG. Transaction monitoring rule engine + ML anomaly detection. Crypto-specific Chainalysis KYT / Address Screening / Sentinel / VASP Risk Scoring, Elliptic, TRM Labs. SAR filing within 30 days via FinCEN BSA E-Filing.
---

# Sanctions + Transaction Monitoring + SAR (TradFi + Crypto)

Continuous sanctions / PEP / adverse media screening + TM rule engine + ML anomaly detection + investigation workflow + SAR filing. 2026 SOTA: ComplyAdvantage for AI-driven real-time screening; Chainalysis / Elliptic / TRM Labs for crypto; Refinitiv / Dow Jones / LexisNexis for established TradFi.

## When to use

User says:
- "Sanctions screening" / "OFAC SDN" / "PEP" / "adverse media"
- "Transaction monitoring" / "TM rules" / "TM engine"
- "ML AML detection" / "anomaly detection AML"
- "Chainalysis KYT" / "Elliptic Lens" / "TRM Labs"
- "SAR filing" / "Suspicious Activity Report" / "30 days"
- "ComplyAdvantage" / "World-Check" / "Watchlist"
- "Crypto wallet screening" / "VASP risk"
- "Sentinel risk categories"

Companion skills: `aml-kyc-bsa-ofac-fincen-fatf`, `customer-due-diligence-cdd-edd-sumsub-persona-jumio`.

## Setup

```bash
# OFAC daily download (free)
curl -fsSL -o sdn_$(date +%Y%m%d).xml https://www.treasury.gov/ofac/downloads/sdn.xml
curl -fsSL -o consolidated_$(date +%Y%m%d).xml https://www.treasury.gov/ofac/downloads/consolidated/consolidated.xml

# OFAC Recent Actions (RSS for breaking sanctions)
curl -fsSL https://ofac.treasury.gov/recent-actions/rss > /tmp/ofac_rss.xml

# EU consolidated list
curl -fsSL https://webgate.ec.europa.eu/fsd/fsf/public/files/xmlFullSanctionsList_1_1/content > eu_sanctions.xml

# UK HMT sanctions list
curl -fsSL https://www.gov.uk/government/publications/the-uk-sanctions-list > /tmp/uk_hmt.html

# UN consolidated sanctions
curl -fsSL https://scsanctions.un.org/resources/xml/en/consolidated.xml > un_sanctions.xml

# Paid vendor APIs (recipient supplies)
export COMPLYADVANTAGE_API_KEY=<dashboard>
export REFINITIV_USERNAME=<refinitiv>
export REFINITIV_PASSWORD=<refinitiv>
export DOWJONES_API_KEY=<dj>
export CHAINALYSIS_API_KEY=<chainalysis>
export ELLIPTIC_API_KEY=<elliptic>
export TRMLABS_API_KEY=<trm>
```

Auth notes:
- All government sanctions lists are free + public.
- ComplyAdvantage: API + Mesh case-management platform.
- Chainalysis KYT requires production licensing; sandbox available.
- TRM Labs + Elliptic: API access via paid tier.

## Common recipes

### Recipe 1: Sanctions lists in scope

```text
Primary US:
- OFAC SDN (Specially Designated Nationals)
- OFAC Consolidated Sanctions List (Non-SDN PLC, NS-ISA, FSE, etc.)
- OFAC SSI (Sectoral Sanctions Identifications)
- OFAC NS-CMIC (Non-SDN Chinese Military-Industrial Complex Companies)
- BIS Entity List (export controls)
- BIS Denied Persons List (DPL)

Other major:
- UN Consolidated Sanctions
- EU Consolidated List
- UK HMT (Office of Financial Sanctions Implementation — OFSI)
- Australia DFAT
- Switzerland SECO
- Canada OSFI
- Japan METI

Country-specific OFAC programs (comprehensive):
- Iran (ITSR, IFSR, IRGC)
- North Korea (NKSR)
- Cuba (CACR)
- Syria (SySR)
- Russia (RuHSR + Executive Orders 14024 + 14066 + 14068 + 14071)
- Belarus
- Ukraine-Russia-related regions (Crimea, Donetsk, Luhansk, Zaporizhzhia, Kherson)
- Venezuela
- Burma/Myanmar
- Zimbabwe (sunset 2024 mostly)

Sectoral:
- Chinese Military Companies (CMC)
- Russian financial / oil / shipbuilding sectors
```

### Recipe 2: ComplyAdvantage real-time screening

```bash
# https://docs.complyadvantage.com/
# Single search
curl -X POST 'https://api.complyadvantage.com/searches' \
  -H "Authorization: Token $COMPLYADVANTAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "search_term": "John Smith",
    "fuzziness": 0.6,
    "filters": {
      "types": ["sanction", "pep", "warning", "adverse-media"],
      "birth_year": 1975,
      "country_codes": ["US","GB"]
    },
    "share_url": 1
  }'

# Monitored search (ongoing alerts on match changes)
curl -X PATCH 'https://api.complyadvantage.com/searches/<id>/monitors' \
  -H "Authorization: Token $COMPLYADVANTAGE_API_KEY" \
  -d '{"is_monitored": true}'
```

### Recipe 3: Refinitiv World-Check One

```bash
# https://developers.refinitiv.com/
# OAuth 2.0 flow first
TOKEN=$(curl -X POST 'https://api.refinitiv.com/auth/oauth2/v1/token' \
  -d "grant_type=password" -d "username=$REFINITIV_USERNAME" \
  -d "password=$REFINITIV_PASSWORD" | jq -r '.access_token')

# Screen a name
curl -X POST 'https://api-worldcheck.refinitiv.com/v2/cases/screeningRequest' \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"groupId":"<id>","entityType":"INDIVIDUAL","name":"John Smith"}'
```

### Recipe 4: Match handling SOP

```text
For each alert:
1. Capture alert details (vendor + match score + match attributes).
2. Compare against customer profile (DOB, address, photo, ID #, country).
3. Decision matrix:
   - True match (high confidence) → escalate to senior compliance + block +
     OFAC 10-day blocked property report (if US OFAC) + SAR consideration.
   - Likely false positive (low confidence, mismatched DOB/address/photo) →
     document + clear.
   - Inconclusive → request additional info from customer; reassess.
4. Document decision rationale in case management.
5. Senior compliance approval for clear or block.

Retention: 5 years per BSA; 10 years for serious enforcement matter.
```

### Recipe 5: OFAC blocked property report

```text
Required: 10 business days from blocking action.

Filing:
- Online: OFAC's Reporting and License Application Forms (OFAC RLAF)
  https://home.treasury.gov/policy-issues/financial-sanctions/recent-actions

Annual report (TD-F 90-22.50):
- Filed by Sept 30 for property blocked as of June 30.
- Lists all blocked property + transactions.

Penalties for non-reporting: $250-$50K/violation civil (depending on
program); strict liability.
```

### Recipe 6: Transaction Monitoring rule library

```text
Rule categories (every TM engine should cover):

Structuring detection:
- Cash deposits / withdrawals just under reportable threshold
  (e.g., $9,500 multiple times within rolling 7 days)
- Wire transfers structured to avoid $10K aggregation

Velocity rules:
- Multiple low-dollar transfers same day → out
- Same originator multiple beneficiaries
- Same beneficiary multiple originators
- New account high-velocity (within 30 days of opening)

Geographic rules:
- Transfer to/from high-risk jurisdiction (FATF grey/black, OFAC sanctioned)
- Transfer pattern inconsistent with KYC stated geography
- IP/device geo mismatch with customer stated

Counterparty rules:
- Counterparty on watchlist
- Counterparty in adverse media within 12 months
- Counterparty newly added (low history)

Pattern rules:
- Round-tripping (out + back in)
- Layering (multiple intermediaries)
- Smurfing (multiple small transactions split across accounts)
- Rapid in-and-out
- Cash-intensive business with low expected cash

Behavioral anomaly:
- Volume exceeds 3x rolling 90-day average
- Transaction outside customer's normal hours
- New beneficiary + immediate large transfer

ML-driven (2026 default):
- Unsupervised anomaly detection on customer / cohort behavior
- Network analysis on transaction graphs
- Supervised models trained on confirmed SAR cases
```

### Recipe 7: Investigation workflow

```text
1. Alert generation (TM rule / ML / customer report / law enforcement
   inquiry / news).
2. Initial review (60 minutes) — close obvious false positives.
3. Open case in case mgmt (ComplyAdvantage Mesh / Actimize / SAS / Hummingbird):
   - Customer profile snapshot
   - Transaction history (90-180 days)
   - Counterparty profile + screening
   - Sanctions + PEP + adverse media re-screen
4. Investigation summary (3-5 paragraphs):
   - What happened
   - Why suspicious
   - What corroborates / what disconfirms
   - Recommendation: clear / monitor / file SAR
5. Reviewer / senior compliance sign-off (2 levels for SAR).
6. Decision documented; if SAR — file within 30 days (60 if unknown subj).
7. Continuing activity SAR every 90 days while ongoing.
```

### Recipe 8: Chainalysis KYT (crypto transaction screening)

```bash
# https://docs.chainalysis.com/api/kyt
# Register user (account)
curl -X POST 'https://api.chainalysis.com/api/kyt/v2/users' \
  -H "Token: $CHAINALYSIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"externalUserId": "user_001"}'

# Submit received transfer for screening
curl -X POST 'https://api.chainalysis.com/api/kyt/v2/users/user_001/transfers/received' \
  -H "Token: $CHAINALYSIS_API_KEY" \
  -d '{
    "network": "BTC",
    "asset": "BTC",
    "transferReference": "<txHash>:<vout>",
    "direction": "received"
  }'

# Alert retrieval
curl -X GET 'https://api.chainalysis.com/api/kyt/v2/users/user_001/alerts' \
  -H "Token: $CHAINALYSIS_API_KEY"
```

### Recipe 9: Chainalysis address screening (pre-transaction)

```bash
# Screen an address before allowing deposit/withdrawal
curl -X POST 'https://public.chainalysis.com/api/v1/address/<address>' \
  -H "X-API-Key: $CHAINALYSIS_API_KEY"

# Sentinel risk categories (35+ as of 2026): ransomware, sanctions, child abuse 
# material, terrorism financing, mixer, darknet market, theft, scam, 
# illicit actor org, fraud shop, etc.
```

### Recipe 10: Elliptic / TRM Labs APIs

```bash
# Elliptic Lens
curl -X POST 'https://aiapi.elliptic.co/v2/analyses/synchronous/wallet' \
  -H "x-token: $ELLIPTIC_API_KEY" \
  -d '{"subject": {"asset":"BTC","blockchain":"bitcoin","hash":"<address>"}, "type": "exposure"}'

# TRM Labs
curl -X POST 'https://api.trmlabs.com/public/v2/screening/addresses' \
  -H "Authorization: Basic <base64(user:key)>" \
  -d '[{"address":"<addr>","chain":"ethereum"}]'
```

### Recipe 11: SAR template (FinCEN SAR Form 111)

```markdown
# Suspicious Activity Report — Internal Draft

**Filing institution:** <Co.>
**Filing date:** <within 30 days of detection>
**Detection date:** <date>
**Activity dates:** <range>

## Subject Information
- Name: <full legal>
- DOB: <YYYY-MM-DD>
- Address: <full>
- ID: <SSN / EIN / passport / etc.>
- Account #: <internal>
- Relationship: <customer / counterparty / both>

## Suspicious Activity Information
- Activity type: <structuring / fraud / ML / terrorist financing / 
  computer intrusion / identity theft / etc.>
- Aggregate amount: $<total>
- Currency: <USD / BTC / etc.>
- Detection mechanism: <TM rule X / employee tip / external referral>

## Narrative (5W chronological)

WHO: <subject + counterparties>
WHAT: <activity type + dollar amount + frequency>
WHEN: <timeline of transactions>
WHERE: <accounts, jurisdictions, IP addresses>
WHY: <basis for suspicion — what makes this anomalous vs subject's
  expected profile>

Supporting evidence:
- Customer profile mismatch: <e.g., stated salary $80k; deposits $850k/mo>
- Counterparty risk: <e.g., wallet linked to known darknet market>
- Pattern: <e.g., 14 deposits $9,500 each within 9 calendar days>
- Other red flags: <list>

## Status
- Continuing? <Y/N>
- Activity ceased? <date + how>
- Account action: <closed / restricted / monitored>

## Filer
- BSA Officer: <name + title>
- Contact: <email + phone>

---
*This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.*

*CONFIDENTIAL — Title 31 USC §5318(g)(2): SAR existence and content may not
be disclosed to subject or third parties.*
```

### Recipe 12: Continuing activity SARs

```text
Required: 90-day intervals if suspicious activity continues.

Process:
- Original SAR + 1st continuing (90 days from original) + 2nd (90 days
  later) + ...
- Each continuing SAR references original SAR # (item 75 of form).
- Account closure can stop the cycle (note in final SAR).

Best practice: close clearly suspicious accounts after investigation.
Avoid indefinite tipping-off-banned customer relationship.
```

### Recipe 13: Adverse media screening sources

```text
Vendor-aggregated (typical 30K+ source feeds):
- ComplyAdvantage adverse media
- Refinitiv adverse media
- Dow Jones adverse media

Free sources for manual top-up:
- OFAC press releases
- SEC enforcement actions (EDGAR + press releases)
- DOJ press releases
- FATF Mutual Evaluation Reports
- Major news outlets (Reuters, FT, WSJ, Bloomberg)
- ProPublica investigative
- Country-specific (e.g., Independent for UK, Le Monde for FR)

Categories of adverse media:
- Financial crime conviction / charge / settlement
- Money laundering / terrorism financing
- Bribery / corruption (FCPA, UKBA, Sapin II)
- Fraud / Ponzi / pyramid scheme
- Sanctions violation
- Tax evasion
- Cybercrime
- Drug / human trafficking
- Organized crime
- Adverse regulatory action
```

## Examples

### Example 1: Onboarding screening with ComplyAdvantage

**Goal:** Screen new account applicant at onboarding.

**Steps:**
1. POST to ComplyAdvantage `/searches` with name + DOB + country (Recipe 2).
2. Response: matches array; risk score.
3. No matches → continue onboarding.
4. Matches: route to compliance for manual review (Recipe 4).
5. Enable monitored search → daily re-screening alerts.

**Result:** Sub-second onboarding decision for clean records; auditable trail for matches.

### Example 2: SAR for structuring pattern

**Goal:** TM detected structuring; investigate + file SAR.

**Steps:**
1. TM alert: 14 cash deposits $9,500 each in 9 days at multiple branches.
2. Open case; pull customer profile.
3. Stated employment: server at restaurant (~$45k/yr).
4. Investigation summary (Recipe 7): inconsistent volume; structuring pattern.
5. Senior comp approval; SAR drafted (Recipe 11).
6. File via FinCEN BSA E-Filing within 30 days.
7. Account decision: close account (de-risk); continuing-activity SAR not required.
8. Retain 5 years.

**Result:** Filed SAR; investigation audit-ready.

### Example 3: Crypto deposit screening

**Goal:** Customer initiates ETH deposit; screen sending address.

**Steps:**
1. Chainalysis address screening (Recipe 9) on sending wallet.
2. Risk: severe (Sentinel category: Ransomware).
3. Reject deposit; freeze account.
4. SAR consideration (cryptocurrency ML).
5. File SAR; OFAC report if address matches sanctioned wallet (e.g., Tornado Cash post-2022, Garantex post-2025).

**Result:** Compliant rejection; sanctioned-address exposure avoided.

## Edge cases / gotchas

- **OFAC strict liability** — no intent required for civil violations. Even good-faith errors result in penalties.
- **Tornado Cash + sanctioned smart contracts** — OFAC sanctioned smart contract code 2022; court partially overturned for some users 2024. Re-check current OFAC status before reactive freeze.
- **False positive fatigue** — high FP rates erode analyst attention. Tune fuzziness + filters; baseline 20-50 FP per true positive.
- **Adverse media is messy** — "John Smith" hits noise; use disambiguation (DOB, country, role).
- **SAR confidentiality** — no tip-off; even cross-functional comms within institution gated. Penalties for disclosure ($250K+ civil; criminal for institutions).
- **PEP definitions vary by jurisdiction** — apply broadest (FATF + EU) for safety.
- **Continuing-activity SAR fatigue** — close suspicious account rather than file indefinitely.
- **Crypto address re-use** — same address may transact with both legitimate and sanctioned counterparties. Screen at transaction level (KYT), not just address.
- **Travel Rule + sanctions intersection** — counterparty VASP failing sanctions check requires transaction halt.
- **Iran / NK / Cuba exposure via stablecoin** — Tether USDT freezes via Treasury order (e.g., 2023+); maintain freeze coordination.
- **Volume + cost** — large institutions ingest millions of transactions; pricing per screened transaction. Negotiate enterprise tiers.
- **Vendor data freshness** — verify update cadence. OFAC SDN: intraday; ComplyAdvantage: real-time. Stale lists = OFAC penalty.

> ⚠ **This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.**

## Sources

- [OFAC](https://ofac.treasury.gov/)
- [OFAC Recent Actions](https://ofac.treasury.gov/recent-actions)
- [OFAC RLAF reporting](https://home.treasury.gov/policy-issues/financial-sanctions/financial-sanctions/license-application-and-reporting-forms)
- [FinCEN BSA E-Filing](https://bsaefiling.fincen.treas.gov/)
- [FinCEN SAR Filing Instructions](https://www.fincen.gov/sites/default/files/shared/FinCEN_SAR_ElectronicFilingInstructions-%20Stand%20Alone%20doc.pdf)
- [EU Sanctions Map](https://www.sanctionsmap.eu/)
- [UK OFSI Sanctions](https://www.gov.uk/government/organisations/office-of-financial-sanctions-implementation)
- [UN Sanctions Lists](https://main.un.org/securitycouncil/en/content/un-sc-consolidated-list)
- [ComplyAdvantage](https://complyadvantage.com/)
- [Refinitiv World-Check](https://www.refinitiv.com/en/products/world-check-kyc-screening)
- [Dow Jones Risk + Compliance](https://www.dowjones.com/professional/risk/)
- [LexisNexis Bridger XG](https://risk.lexisnexis.com/products/bridger-xg)
- [Chainalysis](https://www.chainalysis.com/)
- [Elliptic](https://www.elliptic.co/)
- [TRM Labs](https://www.trmlabs.com/)
- [Solidus Labs](https://www.soliduslabs.com/)
