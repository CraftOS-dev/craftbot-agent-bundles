---
name: aml-kyc-bsa-ofac-fincen-fatf
description: Design + maintain AML program per BSA + FinCEN + OFAC + FATF + 6AMLD + MiCA. Five BSA pillars (CIP / CDD / EDD / TM / SAR-CTR). Sanctions screening cadence per risk tier. SAR (30 days) + CTR (next business day) filing via FinCEN BSA E-Filing. Crypto Travel Rule (FATF R.16). MiCA CASP obligations (EU 2026 enforcement). Risk-based approach (RBA) inventory + independent audit.
---

# AML / KYC / BSA / OFAC / FinCEN / FATF Program

US Bank Secrecy Act + FinCEN guidance + OFAC sanctions + FATF Recommendations + EU 6AMLD + UK MLR 2017 + MiCA (EU crypto). Five BSA Pillars (FinCEN CDD Final Rule 2018): Customer Identification Program, Customer Due Diligence, Enhanced Due Diligence, Transaction Monitoring, SAR/CTR filing.

## When to use

User says:
- "AML program" / "BSA program" / "anti-money laundering"
- "KYC" / "Customer Identification Program" / "CIP"
- "CDD" / "EDD" / "Customer Due Diligence" / "Enhanced Due Diligence"
- "OFAC screening" / "SDN list" / "sanctions screening"
- "SAR" / "Suspicious Activity Report"
- "CTR" / "Currency Transaction Report"
- "FATF Travel Rule" / "R.16"
- "FinCEN BSA E-Filing"
- "MiCA" / "EU crypto regulation"
- "MSB" / "Money Services Business" / "money transmitter"

Companion skills: `customer-due-diligence-cdd-edd-sumsub-persona-jumio`, `sanctions-transaction-monitoring-comply-advantage`, `vendor-risk-bitsight-securityscorecard-upguard`.

## Setup

```bash
# FinCEN BSA Resources
curl -fsSL https://www.fincen.gov/resources/financial-institutions/bank-secrecy-act-resources > /tmp/fincen.html

# OFAC SDN List (download for offline screening)
curl -fsSL -o sdn.xml https://www.treasury.gov/ofac/downloads/sdn.xml
curl -fsSL -o sdn.csv https://www.treasury.gov/ofac/downloads/sdn.csv
curl -fsSL -o consolidated.xml https://www.treasury.gov/ofac/downloads/consolidated/consolidated.xml

# OFAC daily delta (for incremental updates)
curl -fsSL https://www.treasury.gov/ofac/downloads/sdnlist.txt > sdnlist.txt

# FATF Recommendations
curl -fsSL https://www.fatf-gafi.org/en/topics/Fatf-recommendations.html > /tmp/fatf.html

# FATF Mutual Evaluation Reports (jurisdictions in scope)
curl -fsSL https://www.fatf-gafi.org/en/countries.html > /tmp/fatf_countries.html

# FinCEN SAR forms
curl -fsSL https://www.fincen.gov/sites/default/files/shared/FinCEN_SAR_ElectronicFilingInstructions-%20Stand%20Alone%20doc.pdf -o fincen_sar.pdf

# MiCA (EU)
curl -fsSL https://eur-lex.europa.eu/eli/reg/2023/1114/oj > /tmp/mica.html

# Paid vendor APIs (recipient supplies)
export COMPLYADVANTAGE_API_KEY=<dashboard>
export REFINITIV_API_KEY=<refinitiv>
export DOWJONES_API_KEY=<dj-watchlist>
export CHAINALYSIS_API_KEY=<chainalysis>
```

Auth notes:
- OFAC SDN List is free + public, updated daily/intraday.
- ComplyAdvantage / Refinitiv / Dow Jones / Chainalysis are paid SaaS.
- FinCEN BSA E-Filing System requires registration (free) for designated BSA Officer.

## Common recipes

### Recipe 1: Determine BSA applicability

```text
US BSA obliged entities (31 CFR Chapter X):
- Banks + credit unions + foreign branches
- Broker-dealers (registered with SEC)
- Mutual funds
- Futures Commission Merchants (FCMs)
- MSB (Money Services Business — includes most crypto exchanges per
  FinCEN 2013 + 2019 guidance):
  - Money transmitter
  - Currency dealer / exchanger
  - Issuer / seller / redeemer of money orders / traveler's checks
  - Provider / seller of prepaid access
  - Crypto exchange / CVCs (Convertible Virtual Currencies)
- Insurance companies (life + annuity)
- Casinos with $1M+ gross annual revenue
- Dealers in precious metals / stones / jewels ($50K+ transactions)
- Mortgage lenders + originators (RMLOs)
- Loan + finance companies (LFCs)
- Lawyers/notaries in limited contexts (gatekeeper)

EU obliged entities (6AMLD + AMLR):
- Banks + credit institutions
- Investment firms
- Payment + e-money institutions
- Crypto Asset Service Providers (CASPs — MiCA)
- Real estate agents
- High-value goods dealers
- DNFBPs (Designated Non-Financial Businesses + Professions)
```

### Recipe 2: Five BSA Pillars (FinCEN CDD Final Rule 2018)

```text
Pillar 1 — Customer Identification Program (CIP) — §1020.220
- At onboarding: verify name + DOB + address + ID number (SSN / EIN / passport)
- Documentary OR non-documentary verification
- Maintain records 5 years after account closure
- Sanctions check at onboarding + ongoing

Pillar 2 — Customer Due Diligence (CDD)
- Risk-based customer profile
- BENEFICIAL OWNERSHIP (FinCEN CDD Rule 2018): 
  - 25%+ ownership prong (each individual)
  - 1 control prong (CEO/CFO/COO/Pres/MP/General Counsel/Director or
    equivalent control)
  - Verify identity of each beneficial owner
- Ongoing monitoring + risk reassessment

Pillar 3 — Enhanced Due Diligence (EDD) — for high-risk customers
- Triggers: PEPs, high-risk jurisdictions, high-volume cash, correspondent
  banking, private banking, MSB customers, crypto exposure, adverse media
- Additional collection: source of funds, source of wealth, expected
  activity, ownership clarification

Pillar 4 — Transaction Monitoring
- Risk-based rules + thresholds
- ML-driven anomaly detection (2026 SOTA)
- Reasonable design for org's risk profile
- Investigated alerts → SAR decision

Pillar 5 — SAR / CTR Filing
- SAR: 30 days from detection (60 days if no subject identified)
- CTR: cash transactions >$10K same day or next business day (aggregated
  per day per customer)
- Confidentiality (no tip-off to customer)
- 5-year retention
```

### Recipe 3: OFAC sanctions screening cadence

```text
Required at onboarding + ongoing.

Lists to screen against:
- SDN (Specially Designated Nationals) — primary
- Consolidated Sanctions List
- Sectoral Sanctions Identifications (SSI)
- Non-SDN PLC (Palestinian Legislative Council)
- Non-SDN Iranian Sanctions Act List (NS-ISA)
- Foreign Sanctions Evaders (FSE)
- Non-SDN Communist Chinese Military Companies (NS-CMIC)
- 50% Rule — entities owned 50%+ by SDN are also blocked

Re-screening cadence by risk tier:
- High risk (PEPs, high-risk jurisdictions): daily
- Medium risk: weekly
- Low risk: monthly

Match handling:
- Potential match → on-hold + manual investigation
- True match → block + freeze + OFAC report (10 days for blocked property)
- False positive → document + clear + log

OFAC SDN download (refresh daily intraday):
```bash
curl -fsSL https://www.treasury.gov/ofac/downloads/sdn.xml > sdn_$(date +%Y%m%d).xml
```

### Recipe 4: Risk-Based Approach (RBA) inventory

```text
FATF + FinCEN both mandate RBA. Document risk categories:

Customer risk factors:
- PEP (Politically Exposed Person — domestic + foreign + international org)
- Higher-risk jurisdictions (FATF grey + black lists; OFAC sanctioned)
- Cash-intensive businesses
- Shell companies / opaque ownership
- Adverse media (criminal history, regulator action)
- High-net-worth without clear source

Product / service risk factors:
- Cross-border payments
- Private banking
- Correspondent banking
- Crypto / CVC
- Trade finance
- Prepaid access

Geographic risk factors:
- FATF grey list (Increased Monitoring Jurisdictions)
- FATF black list (High-Risk Jurisdictions Subject to a Call for Action — DPRK,
  Iran)
- OFAC comprehensive sanctioned (Cuba, Iran, NK, Syria, Crimea/Donetsk/Luhansk/
  Zaporizhzhia/Kherson regions)
- US-designated terrorism state sponsors

Delivery channel risk:
- Non-face-to-face onboarding
- Third-party introducer
- Mobile / digital only

Aggregate score → CDD vs EDD pathway + monitoring cadence.
```

### Recipe 5: SAR filing — when to file + how

```text
SAR triggers (any transaction $5K+ for banks; $2K+ for MSBs):
- Reasonable suspicion of money laundering, structuring, terrorism financing,
  computer intrusion, fraud, account takeover, identity theft.

Timeline:
- 30 days from detection (60 days if subject not yet identified).
- File via FinCEN BSA E-Filing System (bsaefiling.fincen.treas.gov).
- Confidentiality — NO tip-off to customer (Title 31 USC §5318(g)(2)).

SAR template structure:
1. Subject identification (account #, identity, address — if known)
2. Suspicious activity description (5W: who, what, when, where, why) —
   chronological narrative
3. Activity total ($) + duration
4. Detection mechanism (TM alert, employee tip, regulator inquiry, customer
   reported, law enforcement)
5. Other parties involved
6. Status of activity (continuing / ceased / unknown)
7. Filer + contact info

Continuing activity SARs: every 90 days while activity continues.

Retention: 5 years from filing date.

False / no SAR — document the decision rationale; auditable.
```

### Recipe 6: CTR filing

```text
Cash transaction(s) >$10,000 by/through/to financial institution by/on
behalf of any one person on any one business day.

Aggregation:
- Multiple transactions same business day same customer → aggregate.
- Structuring (intentionally breaking into smaller amounts) → CTR EXEMPT
  the customer + SAR.

Timeline: 15 days from transaction.

Filing: FinCEN BSA E-Filing.

Exemptions (FinCEN-designated):
- Listed companies + subsidiaries (Phase I exemption)
- Non-listed businesses meeting criteria (Phase II exemption — qualifying
  for 2+ years of frequent reportable transactions)

Retention: 5 years.
```

### Recipe 7: Crypto-specific — FATF Travel Rule (R.16)

```text
FATF Recommendation 16 — applies to wire transfers + crypto VASPs.

Crypto Travel Rule (FATF Updated Guidance 2021 + 2023):
- VASP-to-VASP crypto transfers above threshold (varies: US $1K; EU MiCA;
  most jurisdictions $1K USD equivalent).
- Originator VASP must transmit:
  - Originator name + account/wallet address + physical address OR ID + DOB
    OR customer ID #
  - Beneficiary name + account/wallet address
- Beneficiary VASP must screen + verify + receive.

Compliance protocols (2026):
- TRP (Travel Rule Protocol)
- Sumsub Travel Rule
- Notabene
- Shyft
- Chainalysis Travel Rule
- Coinbase + Kraken + Gemini built-in

Unhosted wallet handling — varies by jurisdiction:
- US FinCEN: proposed 2020 (still in rule-making); current practice =
  beneficial owner attestation.
- EU MiCA: stricter — unhosted wallet origin/dest > €1K requires beneficial
  owner ID.
```

### Recipe 8: MiCA (Markets in Crypto-Assets Regulation — EU)

```text
EU 2023/1114; phased in force June 30, 2024 + Dec 30, 2024;
2026 enforcement intensifying.

CASP (Crypto-Asset Service Provider) authorization required for:
- Custody + administration of crypto on behalf of clients
- Operation of a crypto trading platform
- Exchange of crypto for fiat / other crypto
- Execution of orders
- Placement / advice / portfolio management of crypto

Obligations:
- Prudential safeguards (own funds requirements)
- Governance + organizational requirements
- Conduct of business + conflicts of interest
- ICT (DORA-aligned operational resilience)
- White paper requirements for crypto-asset issuance
- Market abuse provisions (parallel to MAR)
- AML — full AMLR/6AMLD coverage

Stablecoins:
- ART (Asset-Referenced Tokens) + EMT (E-Money Tokens) authorization.
- Reserve requirements + redemption rights.

Transition: existing operators have until July 1, 2026 (Member State option
to extend to Dec 2026) to obtain MiCA authorization.
```

### Recipe 9: Independent audit (annual minimum for MSB)

```text
31 CFR §1022.210(d)(3) — MSBs must designate an individual responsible for
ensuring program compliance + an independent review.

Independent audit scope:
- AML program design adequacy
- Implementation effectiveness
- Sample testing of CIP / CDD / EDD / TM / SAR-CTR
- OFAC screening effectiveness
- BSA Officer adequacy of authority + resources
- Recordkeeping
- Training adequacy

Frequency: annual minimum; risk-based for larger orgs (some require
semi-annual).

Auditor independence: NOT in BSA Officer role; can be internal audit OR
external firm; documented independence.

Output: report to senior management + Board (or equivalent governance).
Corrective action tracked.
```

### Recipe 10: AML program memo template

```markdown
# AML Compliance Program — <Co.>

**Effective:** <date>
**BSA Officer:** <name + title + reporting line>
**Senior management approval:** <name + date>
**Board oversight:** <if applicable>
**Frameworks:** BSA (31 USC §§5311 et seq.) + 31 CFR Chapter X + FinCEN
guidance + OFAC sanctions + FATF Recommendations + 
<additional jurisdictions>

## 1. Scope + applicability
- Org type: <bank / MSB / broker-dealer / CASP / etc.>
- Products + services: <list>
- Geographic footprint: <list>

## 2. Risk-Based Approach (RBA) — Risk Assessment
- Customer risk: <high-risk customer profile>
- Product risk: <crypto, cross-border, etc.>
- Geographic risk: <FATF high-risk jurisdictions>
- Delivery channel risk: <non-FTF, etc.>
- Inherent + residual risk per category

## 3. Five BSA Pillars

### CIP
- Onboarding verification: <Sumsub / Persona / Jumio config>
- Documentary + non-documentary methods
- Record retention 5 years

### CDD
- Risk-based customer profile
- Beneficial Ownership Rule — 25% + control prong
- Ongoing monitoring

### EDD
- Triggers (PEP, high-risk jurisdiction, etc.)
- Additional collection: source of funds, source of wealth, expected
  activity

### Transaction Monitoring
- Rule library: <e.g., structuring, rapid in/out, high-velocity, sanctions
  proximity, cash-equivalent volume>
- ML/anomaly detection: <ComplyAdvantage / Actimize / SAS / in-house>
- Alert investigation SLA: <e.g., 14 days from generation>

### SAR / CTR Filing
- SAR within 30 days; FinCEN BSA E-Filing
- CTR within 15 days; cash $10K+ aggregated daily

## 4. OFAC Sanctions Compliance
- Screening at onboarding + ongoing
- Re-screening cadence: high daily / med weekly / low monthly
- SDN + Consolidated + SSI + sector lists
- Match handling SOP + 10-day blocked property report

## 5. Training
- BSA Officer: annual + role-specific
- Customer-facing staff: annual
- Senior management + Board: annual brief

## 6. Independent Audit
- Annual minimum (MSB; or per risk profile)
- Internal or external; independent of BSA Officer

## 7. Recordkeeping
- 5 years from account closure / transaction date

---
*This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.*
```

### Recipe 11: Sanctions screening — local matching

```bash
# Simple Python lookup against SDN XML
python3 - <<'EOF'
import xml.etree.ElementTree as ET
tree = ET.parse('sdn.xml')
ns = {'s': 'http://tempuri.org/sdnList.xsd'}
target = 'JOHN DOE'.upper()
for entry in tree.findall('.//s:sdnEntry', ns):
    name = (entry.findtext('s:lastName', namespaces=ns) or '') + ', ' + \
           (entry.findtext('s:firstName', namespaces=ns) or '')
    if target in name.upper():
        print(entry.findtext('s:uid', namespaces=ns), name)
EOF
```

### Recipe 12: ComplyAdvantage screening via API

```bash
# https://docs.complyadvantage.com/
curl -X POST 'https://api.complyadvantage.com/searches' \
  -H "Authorization: Bearer $COMPLYADVANTAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "search_term": "John Doe",
    "fuzziness": 0.6,
    "filters": {"types": ["sanction","pep","warning","adverse-media"]}
  }'
```

### Recipe 13: Chainalysis KYT (Know Your Transaction) crypto

```bash
# https://docs.chainalysis.com/
curl -X POST 'https://api.chainalysis.com/api/kyt/v2/users/<userId>/transfers/received' \
  -H "Token: $CHAINALYSIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"network":"ETH","asset":"USDT","transferReference":"0xabc"}'
```

## Examples

### Example 1: Stand up MSB AML program (crypto exchange)

**Goal:** Launch FinCEN-registered MSB; ship AML program + KYC stack.

**Steps:**
1. Register as MSB with FinCEN (Form 107).
2. Designate BSA Officer + senior mgmt approval.
3. Draft AML program memo per Recipe 10.
4. Wire Sumsub KYC + ComplyAdvantage sanctions + Chainalysis KYT.
5. Implement Travel Rule (Notabene or Sumsub Travel Rule).
6. Train staff; document curriculum + attendance.
7. Schedule independent audit Q4.
8. Register for FinCEN BSA E-Filing System.

**Result:** FinCEN-compliant MSB ready for state Money Transmitter Licensing (separate).

### Example 2: SAR filing for structuring

**Goal:** Customer made 9 cash deposits of $9,500 in 8 days. File SAR.

**Steps:**
1. TM alert flags repetitive cash deposits just under $10K.
2. Investigate: customer profile, source of funds, expected activity.
3. Conclude: reasonable suspicion of structuring (31 USC §5324).
4. SAR narrative per Recipe 5; submit via FinCEN BSA E-Filing within 30 days.
5. Internal flag — continuing activity; re-SAR every 90 days if ongoing.
6. Retain 5 years; no tip-off to customer.

**Result:** Compliant SAR filing; documented investigation.

### Example 3: OFAC potential match handling

**Goal:** Onboarding screen returns potential match against SDN.

**Steps:**
1. Auto-screen via ComplyAdvantage at onboarding; "potential match" flagged.
2. Hold account; manual investigation.
3. Compare match details: DOB, address, photo, country.
4. False positive: document clearance + continue onboarding.
5. True match: block + freeze; file OFAC report within 10 days; do not tip-off.

**Result:** Compliant screening; clean false-positive documentation.

## Edge cases / gotchas

- **50% rule** — entities owned 50%+ by SDN are themselves blocked even if not on list. Build ownership graph for screening.
- **Beneficial Ownership confusion** — FinCEN CDD Rule (banks/MSBs) ≠ FinCEN Corporate Transparency Act BOIR (filed at FinCEN by reporting companies). Both apply.
- **Structuring is itself a federal crime** under 31 USC §5324. Even if no underlying ML, breaking transactions to avoid CTR triggers SAR + criminal liability.
- **Tip-off prohibition** (31 USC §5318(g)(2)). Cannot tell customer about SAR; affects how to close suspicious accounts.
- **MSB state licensing** is separate from federal FinCEN registration. Most US states require Money Transmitter License (MTL) — 50+ separate licenses.
- **NMLS Conference of State Bank Supervisors** offers MTL processing.
- **Crypto = MSB per FinCEN 2013 + 2019 guidance.** Exchanges, administrators (centralized stablecoins), and (per 2019) certain custodians.
- **MiCA timeline 2026 critical.** Operators without MiCA authorization by deadline cannot serve EU clients.
- **OFAC violations are STRICT LIABILITY.** Lack of intent is not a defense. Penalties up to $1.5M per violation (civil).
- **SAR confidentiality across organization.** Even other parts of org cannot know about SAR (need-to-know basis).
- **Adverse media** — FATF + ComplyAdvantage flag negative news; auditors expect adverse media coverage as part of CDD.
- **PEP definitions vary by jurisdiction** — FATF + EU 6AMLD broad (domestic + foreign + international org); US BSA narrower (foreign mainly).
- **Sanctions evasion via crypto** — increased OFAC + DOJ focus 2024-2026. Robust crypto-address screening (Chainalysis, Elliptic, TRM Labs) is industry standard.

> ⚠ **This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.**

## Sources

- [FinCEN BSA Resources](https://www.fincen.gov/resources/financial-institutions/bank-secrecy-act-resources)
- [FinCEN CDD Final Rule (2018)](https://www.fincen.gov/news/news-releases/fincen-issues-final-rule-customer-due-diligence)
- [FinCEN BSA E-Filing System](https://bsaefiling.fincen.treas.gov/)
- [OFAC Sanctions Programs](https://ofac.treasury.gov/sanctions-programs-and-country-information)
- [OFAC SDN List](https://ofac.treasury.gov/specially-designated-nationals-and-blocked-persons-list-sdn-human-readable-lists)
- [FATF Recommendations](https://www.fatf-gafi.org/en/topics/Fatf-recommendations.html)
- [FATF Country Assessment](https://www.fatf-gafi.org/en/countries.html)
- [FATF Crypto Travel Rule Guidance](https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Updated-Guidance-RBA-VASP.html)
- [EU MiCA (2023/1114)](https://eur-lex.europa.eu/eli/reg/2023/1114/oj)
- [EU 6AMLD](https://eur-lex.europa.eu/eli/dir/2018/1673/oj)
- [UK MLR 2017](https://www.legislation.gov.uk/uksi/2017/692)
- [ComplyAdvantage](https://complyadvantage.com/)
- [Chainalysis](https://www.chainalysis.com/)
- [Sumsub](https://sumsub.com/)
- [Notabene Travel Rule](https://notabene.id/)
- [CSBS NMLS](https://mortgage.nationwidelicensingsystem.org/)
