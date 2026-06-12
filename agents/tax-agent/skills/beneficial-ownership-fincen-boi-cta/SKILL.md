<!--
Source: https://www.fincen.gov/boi
Source: https://www.fincen.gov/news/news-releases/fincen-issues-interim-final-rule-removes-beneficial-ownership-reporting
Source: https://boiefiling.fincen.gov/
Reference role.md: "FinCEN BOI / Corporate Transparency Act"
-->

# Beneficial Ownership reporting — Corporate Transparency Act + FinCEN BOI

Corporate Transparency Act (CTA) enforced January 1, 2024. **BOI (Beneficial Ownership Information) report** filed via **FinCEN BOSS** portal. **March 2025 interim final rule**: domestic entities EXEMPT from filing; foreign entities registered to do business in US STILL required. Software: FinCEN BOSS portal direct, FincenFetch, BOIfincen.com, Harbor Compliance, Wolters Kluwer CT Corp.

## When to use

- Foreign-formed company registered to do business in US — BOI report required within 30 days of registration.
- Foreign-formed reporting company change of beneficial ownership (BOI update within 30 days).
- Existing domestic reporting company under court injunctions / earlier interim rules — verify current obligation.
- Diligence on whether target / acquirer is BOI-compliant.
- Annual review of beneficial ownership structure (if exemptions changed).
- Trigger phrases: "BOI", "beneficial ownership", "FinCEN", "CTA", "Corporate Transparency Act", "BOSS portal", "FinCEN BOSS", "reporting company".

NOT for: SEC Schedule 13D/G beneficial ownership (out of scope; refer to `compliance-agent`); state-level beneficial ownership (some states adopted similar — e.g., NY LLC Transparency Act — refer to `legal-counsel`); FBAR foreign financial accounts (out of scope; refer to `compliance-agent`).

## Setup

### FinCEN BOSS Portal (no public API)

```bash
# https://boiefiling.fincen.gov/
# Web-only filing portal
# Free; no charge to file BOI report
# Login requires Login.gov account
# Filing tracked via "ID number" returned post-submission
```

### FincenFetch (third-party SaaS)

```bash
# https://www.fincenfetch.com/
# Automation for law firms / CPAs filing on behalf of clients
# Bulk filing + status tracking
# Pricing: $20-100 per report depending on volume
export FINCENFETCH_API_KEY="..."
curl -H "Authorization: Bearer $FINCENFETCH_API_KEY" \
  https://api.fincenfetch.com/v1/reports
```

### Harbor Compliance / Wolters Kluwer CT Corp (managed)

```bash
# Enterprise managed BOI service
# https://www.harborcompliance.com/services/corporate-transparency-act
```

### BOIfincen.com (DIY)

```bash
# https://www.boifincen.com/
# DIY self-file portal with form-builder
```

## Current state of CTA enforcement (June 2026)

After substantial 2024-2025 litigation (NSBA v. Yellen, Texas Top Cop Shop v. Garland, multiple injunctions):

- **March 2025 FinCEN interim final rule** removed BOI reporting requirement for DOMESTIC reporting companies.
- **Foreign-formed reporting companies** registered to do business in any US state STILL must file.
- **Domestic-formed companies** (Inc/LLC formed in any US state) currently NOT required to file BOI.
- Legal landscape may evolve — verify current status before relying on exemption.

## Common recipes

### Recipe 1 — Identify reporting company status

```python
# Reporting company = entity FORMED OR REGISTERED to do business in US
# by filing with secretary of state or similar office.

def is_reporting_company(entity):
    formed_in_us = entity["formation_jurisdiction"] in US_STATES
    formed_outside_us = not formed_in_us
    registered_in_us = entity.get("us_state_registration") is not None
    
    if formed_in_us:
        # March 2025 IFR: domestic exempt
        return False, "Domestic — exempt per March 2025 IFR"
    
    if formed_outside_us and registered_in_us:
        return True, "Foreign-registered — must file"
    
    return False, "Foreign-only, no US registration — exempt"
```

### Recipe 2 — 23 categories of exemption (pre-IFR — still relevant for domestic exemption verification)

```python
EXEMPT_CATEGORIES = [
    "1. SEC reporting issuer",
    "2. Governmental authority",
    "3. Bank",
    "4. Credit union",
    "5. Depository institution holding company",
    "6. Money transmitting business registered with FinCEN",
    "7. Broker-dealer registered with SEC",
    "8. Securities exchange / clearing agency",
    "9. Other Exchange Act registered entity",
    "10. Investment company / adviser",
    "11. Venture capital fund adviser",
    "12. Insurance company",
    "13. State-licensed insurance producer",
    "14. CEA registered entity",
    "15. Accounting firm (PCAOB)",
    "16. Public utility",
    "17. Financial market utility",
    "18. Pooled investment vehicle",
    "19. Tax-exempt entity (501(c) etc.)",
    "20. Entity assisting tax-exempt",
    "21. Large operating company (20+ employees + $5M+ US revenue + US office)",
    "22. Subsidiary of exempt entity (wholly owned by 1-21)",
    "23. Inactive entity (existed 1/1/2020+, no activity, no foreign ownership)",
]
```

### Recipe 3 — Beneficial owner identification

```python
# Beneficial owner = individual who EITHER:
#  (a) exercises substantial control (CEO, CFO, GC, similar officer; 
#       senior officer; person able to appoint/remove majority of board;
#       important decision-maker), OR
#  (b) owns or controls 25%+ of ownership interests

def identify_beneficial_owners(entity):
    owners = []
    
    # Substantial control
    for officer in entity["senior_officers"]:
        owners.append({
            "name": officer.name,
            "dob": officer.dob,
            "address": officer.address,
            "id_type": officer.id_type,  # passport, driver's license, etc.
            "id_number": officer.id_number,
            "id_issuing_jurisdiction": officer.id_jurisdiction,
            "id_image_url": officer.id_image_url,
            "type": "control",
        })
    
    # 25%+ ownership
    for owner in entity["cap_table"]:
        if owner.fully_diluted_pct >= 0.25:
            owners.append({**owner_info(owner), "type": "ownership"})
    
    return owners
```

### Recipe 4 — Company applicant (entities formed 2024+)

```python
# Company applicant = individual who DIRECTLY FILES or DIRECTS the filing
# of the document that creates / registers the entity
# Required for entities formed/registered 1/1/2024+
# Max 2 company applicants reportable

# Common scenarios:
#  - Founder filed formation docs themselves → founder is company applicant
#  - Stripe Atlas filed on behalf of founder → Atlas paralegal is company applicant
#  - Outside counsel filed → attorney + paralegal who directed filing
```

### Recipe 5 — Filing BOI via BOSS portal

```python
# Step-by-step (manual UI):
# 1. Navigate to https://boiefiling.fincen.gov/
# 2. Login with Login.gov
# 3. Click "File BOIR"
# 4. Choose: Initial / Update / Correct / Newly Exempt
# 5. Enter entity info: legal name, EIN, formation jurisdiction, US state, address
# 6. Enter beneficial owners (1+) with ID details
# 7. Enter company applicants (if entity formed 2024+)
# 8. Upload ID images
# 9. Certify under penalty of perjury
# 10. Submit; receive ID number; download PDF receipt

# Recipient prepares data with agent; recipient files at BOSS portal
# Agent CANNOT directly file (no public API)
```

### Recipe 6 — FinCEN ID (one-time individual identifier)

```python
# Beneficial owners can apply for FinCEN ID (free, one-time)
# Then for each reporting company, just reference FinCEN ID
# Avoids re-uploading ID images each time
# https://fincenid.fincen.gov/

# Once issued, reportable entity provides FinCEN ID instead of full info
```

### Recipe 7 — BOI update / change (foreign-registered cos)

```python
# 30-day window from triggering event:
#  - Change in beneficial owner identification info (name, address, ID#)
#  - Beneficial owner crosses 25% threshold or drops below
#  - New senior officer
#  - Change in legal entity name / address

update_events = [
    {"event": "CEO change", "date": "2026-05-15", "deadline": "2026-06-14"},
    {"event": "Beneficial owner address change", "date": "2026-05-20",
     "deadline": "2026-06-19"},
    {"event": "Founder ID renewal (new passport)", "date": "2026-06-01",
     "deadline": "2026-07-01"},
]
```

### Recipe 8 — Newly exempt or no-longer-exempt

```python
# File "Newly Exempt Entity" report if previously filed BOI and now qualifies 
# for exemption (e.g., crossed Large Operating Company threshold)
# File initial BOI report if previously exempt entity loses exemption

# Large Operating Company exemption threshold (Category 21):
#  - 20+ FT US employees, AND
#  - $5M+ US revenue in prior year, AND
#  - US-based office for business operations
```

### Recipe 9 — Penalty exposure

```python
# Civil penalty: up to $591/day (2025 inflation-adjusted)
# Criminal penalty: up to $10,000 fine + 2 years imprisonment
# Senior officer + reporting company both liable for willful violations
# Reporting individuals liable

# Safe harbor (CTA section 5336(h)(3)):
# Voluntary correction within 90 days of identifying error → no penalty
```

### Recipe 10 — Diligence on M&A target BOI status

```python
# In M&A diligence, request:
#  - Whether target is reporting company (was domestic-exempt? foreign-registered?)
#  - Most recent BOI report (if foreign-registered)
#  - Any FinCEN penalty actions
#  - Updates pending for changes in ownership

diligence_checklist = [
    "Target's formation state / jurisdiction",
    "Target's US state registrations (if foreign)",
    "Most recent BOI submission ID + date",
    "List of beneficial owners on file",
    "Any pending updates (e.g., new C-suite)",
    "Confirmation of exemption application (if exempt)",
    "Post-closing BOI update commitment (30 days from close)",
]
```

## Examples

### Example 1: Singapore parent registered subsidiary in Delaware

**Goal:** Singapore Pte Ltd registers as a foreign entity in Delaware to do business; BOI filing required.

**Steps:**

1. Confirm filing required: foreign-formed + US-registered → yes (March 2025 IFR doesn't exempt).
2. Identify beneficial owners:
   - CEO (Singapore resident, 35% ownership)
   - CTO (US resident, 28% ownership)
   - Senior officers without 25% ownership (CFO, COO)
3. Identify company applicants (registered 2024+):
   - Delaware registered agent service paralegal
   - Outside counsel attorney
4. Collect ID details for each (passport for foreign; driver's license for US).
5. Apply for FinCEN ID for each beneficial owner (optional, simplifies future updates).
6. File initial BOI report via BOSS portal within 30 days of Delaware registration.
7. Calendar 30-day update deadline for any future changes.

**Result:** BOI compliant; FinCEN IDs issued; update process documented.

### Example 2: Domestic LLC unsure of current obligation

**Goal:** Texas LLC formed 2023; founder confused about CTA after various rulings.

**Steps:**

1. Confirm entity is domestic (formed in TX).
2. March 2025 IFR exempts domestic entities → NO filing currently required.
3. Document IFR reliance memo in entity records (in case rules change again).
4. Monitor FinCEN updates quarterly via firecrawl-mcp scrape of https://www.fincen.gov/boi.
5. Set up `remindme` quarterly check (Q1, Q2, Q3, Q4 of each year).

**Result:** Domestic exemption documented; ongoing monitoring.

### Example 3: Large Operating Company exemption (Category 21)

**Goal:** Mature private company 25 US employees, $8M revenue, US HQ. Want exemption.

**Steps:**

1. Verify Large Operating Company criteria:
   - 20+ FT US employees: 25 ✓
   - $5M+ US revenue: $8M ✓
   - US-based office: yes ✓
2. If foreign-formed: file "Newly Exempt Entity" report (BOSS portal) → no further filings.
3. If domestic-formed: already exempt under March 2025 IFR; double-protected.
4. Annual monitoring: ensure employee count + revenue remain above threshold; otherwise lose exemption.

**Result:** Large Operating Company exemption claimed; no ongoing BOI filings.

## Edge cases / gotchas

- **March 2025 IFR ongoing litigation:** legal landscape unstable — confirm current status before relying on exemption.
- **State-level BOI laws:** NY LLC Transparency Act (effective 2026) requires LLCs registered in NY to file BOI with state. Other states proposing similar.
- **Foreign-formed even with US sub:** if foreign parent is the reporting entity (registered in US), file BOI. If only US subsidiary is reporting entity, parent's data not direct.
- **30-day update window:** very tight. Senior officer change = 30-day clock. Calendar each foreseeable change.
- **Beneficial owner address must be RESIDENTIAL, not business.** Many founders try to use business address; rejected.
- **ID image upload:** passport bio page OR driver's license front. Some founders try state ID with different name → mismatch rejection.
- **FinCEN ID lifecycle:** if beneficial owner gets new passport (post-renewal), must update FinCEN ID; old ID auto-references stale doc.
- **Company applicant only for entities formed 2024+:** pre-2024 entities don't report company applicants.
- **Disregarded LLCs vs. corporations:** entity classification doesn't matter — reporting company determined by formation/registration, not tax classification.
- **Trusts as beneficial owners:** if a trust owns 25%+ of reporting company, look-through to trustees + beneficiaries with substantial control.
- **Pooled investment vehicles exemption (Cat 18):** must be regulated by SEC/CFTC OR identified as a "pooled investment vehicle" per investment adviser registered with SEC.
- **Subsidiary exemption (Cat 22):** ONLY if wholly owned by 1+ of the OTHER 22 exempt categories. 99%-owned doesn't qualify.
- **Inactive entity (Cat 23):** strict — existed before 1/1/2020, no activity in last 12 mo, no change in ownership in 12 mo, no foreign owners, no funds, no assets >$1K.
- **Sole proprietorship NOT reporting company** — sole prop is not a separate legal entity.
- **General partnership only reporting if registered:** Most states don't require GP filing; UCC-style GPs not reporting companies. Limited partnerships (LP) ARE reporting companies.
- **Trust NOT reporting company unless registered with state filing office.** Most common law trusts don't register; statutory trusts (e.g., Delaware Statutory Trusts) do.
- **Safe harbor for voluntary correction:** within 90 days of discovering error, file correction → no penalty. Document the discovery date.
- **Beneficial owner privacy:** BOI data is NOT public. Accessible by FinCEN + law enforcement + (under conditions) financial institutions for AML compliance.

> WARNING **This is informational guidance from an AI agent. Always consult a licensed CPA or tax attorney in your jurisdiction before filing returns, claiming credits, or implementing binding tax positions.**

## Sources

- FinCEN BOI landing: https://www.fincen.gov/boi
- FinCEN BOSS portal: https://boiefiling.fincen.gov/
- FinCEN BOI Small Entity Compliance Guide: https://www.fincen.gov/sites/default/files/shared/BOI_Small_Compliance_Guide.v1.1-FINAL.pdf
- FinCEN March 2025 IFR: https://www.fincen.gov/news/news-releases/fincen-issues-interim-final-rule-removes-beneficial-ownership-reporting
- Corporate Transparency Act (31 USC 5336): https://www.law.cornell.edu/uscode/text/31/5336
- 31 CFR 1010.380 (BOI reporting regulations): https://www.ecfr.gov/current/title-31/subtitle-B/chapter-X/part-1010/subpart-D/section-1010.380
- FincenFetch: https://www.fincenfetch.com/
- BOIfincen.com: https://www.boifincen.com/
- FinCEN ID portal: https://fincenid.fincen.gov/
- NY LLC Transparency Act: https://www.dos.ny.gov/corps/cta_llc.html
- NSBA v. Yellen ruling: https://www.govinfo.gov/app/details/USCOURTS-alnd-5_22-cv-01448
- Texas Top Cop Shop v. Garland: https://storage.courtlistener.com/recap/gov.uscourts.txed.227731/
- AICPA BOI guidance: https://www.aicpa.org/topic/business-tax/corporate-transparency-act

## Related skills

- `entity-structure-c-vs-s-vs-llc` — entity formation triggers CTA analysis
- `irs-state-dor-notice-response` — FinCEN penalty notice response
- `tax-audit-prep-response-federal-state` — BOI substantiation file for diligence
