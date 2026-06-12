---
name: irs-501c3-compliance-docs
description: Maintain a ready-to-attach 501(c)(3) org credentials packet — IRS determination letter, current 990s, audited financials, board roster, governance policies. Verify status via IRS Tax Exempt Organization Search + ProPublica. Use when the user says "build our 501(c)(3) packet" / "verify our 501(c)(3) status" / "get IRS docs ready for the funder".
---

# IRS 501(c)(3) compliance documents + org credentials

Most funders require a standard packet of 501(c)(3) credentials attached to every proposal. Build it once, version it, and keep it current. Verify funder's status too — granting to an unverified "nonprofit" is the kind of detail that drops a proposal late.

Disclaimer: For binding tax-status interpretation, public-charity vs private-foundation classification, or 990 filing issues, consult a qualified nonprofit attorney or CPA.

## When to use

- Org is preparing first federal proposal and lacks a standard credentials packet
- Funder application requires "IRS determination letter" + supporting docs
- Verifying a peer org's or funder's 501(c)(3) status for prospect research
- Annual refresh of the credentials packet (every Form 990 filing)
- Responding to a funder audit / due diligence request

Do NOT use this skill for:
- 990 filing itself (handled by org's CPA / `finance-controller`)
- Audited financial statement preparation (→ `finance-controller`)
- Fiscal sponsorship setup if org is NOT 501(c)(3) (→ `fiscal-sponsorship-coordination`)

## Setup

```bash
# No specialized install
# Tools:
# - cli-anything → IRS EO Search + ProPublica
# - filesystem (org docs library)
# - docx (assemble packet cover memo)

# Standard credentials folder layout
mkdir -p org_credentials/{irs,financials,governance,operating,personnel}
ls org_credentials/
```

Auth / API key requirements: None. IRS EO Search + ProPublica are free.

## Common recipes

### Recipe 1: Verify org's 501(c)(3) status via IRS EO Search

```bash
# Direct query (no API; URL pattern)
echo "https://apps.irs.gov/app/eos/displayAll.do?dispatchMethod=displayAllInfo&Id=12345&ein=$EIN"

# Or via firecrawl-mcp
firecrawl_scrape url="https://apps.irs.gov/app/eos/" formats=["markdown"]
```

Look for: Status "Pub 78 Data" (deductibility) + "Auto-Revocation List" check + Subsection 03 (public charity) vs Subsection 04 (private foundation).

### Recipe 2: Verify via ProPublica

```bash
curl "https://projects.propublica.org/nonprofits/api/v2/organizations/941655673.json"
```

Returns: `subsection_code` (03 = public charity), `affiliation_code`, `classification_codes`, last 5 years of 990 PDFs.

### Recipe 3: Standard credentials packet checklist

```markdown
## 501(c)(3) Credentials Packet

### IRS
- [ ] IRS Determination Letter (the original; older orgs may have multiple if structure changed)
- [ ] IRS EO Search printout (current verification, dated within last 12 months)
- [ ] EIN verification letter
- [ ] State charitable registration certificate (per state where org solicits)

### Financials
- [ ] Form 990 (last 3 years, signed)
- [ ] Audited Financial Statements (last 3 years, signed by auditor)
- [ ] Most recent unaudited interim financials (if mid-year proposal)
- [ ] Single Audit report (if applicable — federal expenditures ≥ $1M/$750K)

### Governance
- [ ] Articles of Incorporation
- [ ] Bylaws (current version, with adoption date)
- [ ] Board of Directors roster (current, with terms + affiliations)
- [ ] Conflict of Interest Policy + annual signed disclosures
- [ ] Whistleblower Policy
- [ ] Document Retention + Destruction Policy
- [ ] Gift Acceptance Policy

### Operating
- [ ] W-9 (current, signed)
- [ ] State sales tax exemption (if applicable)
- [ ] DBA / fictitious-business-name filing (if applicable)
- [ ] Insurance certificates (general liability, D&O, professional)

### Personnel
- [ ] Key staff CVs / bios
- [ ] Executive director bio
- [ ] Org chart
```

### Recipe 4: Pull current 990 PDFs from ProPublica

```bash
# Pull last 3 years' 990s
EIN="941655673"
curl "https://projects.propublica.org/nonprofits/api/v2/organizations/${EIN}.json" \
  | jq -r '.filings_with_data[] | "\(.tax_prd_yr) \(.pdf_url)"' \
  | head -3
# Download each PDF
```

### Recipe 5: Generate the IRS EO Search verification PDF

```bash
# Via firecrawl-mcp or playwright-mcp — capture screenshot of current status page
playwright_screenshot url="https://apps.irs.gov/app/eos/" \
  selector="#searchResults" \
  output="org_credentials/irs/eo_verification_$(date +%Y%m%d).pdf"
```

Funders prefer dated verification (within 12 months).

### Recipe 6: Public charity vs Private foundation check

```bash
# ProPublica subsection codes
# 03 = 501(c)(3) — most public charities + some private foundations
# Check classification_codes for public-charity status:
# - 170(b)(1)(A)(i)-(vi) = various public charity classifications
# - 509(a)(1), (a)(2), (a)(3) = public charity tests
# - 509(a)(4) = supporting org
```

If org is private foundation (most foundation funders ARE — that's why they fund you), this affects what THEY can fund (some federal sub-recipient rules).

### Recipe 7: Form 1023 / 1023-EZ retention

```markdown
## If org's IRS determination letter is lost:
1. Request copy via IRS Form 4506-A (allow 60 days)
2. ProPublica may have the original determination letter scan
3. For 1023-EZ orgs (since 2014): EIN holders can re-print from IRS pub
```

### Recipe 8: Annual refresh cadence

```markdown
| Doc | Refresh trigger | Owner |
|---|---|---|
| 990 | Within 30 days of filing | Finance |
| Audited financials | Within 30 days of audit signoff | Finance |
| Board roster | After every board change | Board chair |
| COI disclosures | Annually + at board onboarding | Board secretary |
| EO verification | Every 12 months | Grant writer |
| Insurance certs | At renewal | Operations |
```

### Recipe 9: Cover memo for the credentials packet

```markdown
# <Org Name> — 501(c)(3) Credentials Packet
**EIN:** XX-XXXXXXX
**IRS Status:** 501(c)(3) public charity (Pub 78 verified <date>)
**State:** Incorporated in <state> <date>
**Fiscal Year End:** <month> <day>

## Contents
1. IRS Determination Letter (<date>)
2. IRS EO Search verification (<date>)
3. Most recent Form 990 (FY<year>)
4. Last 3 years audited financials
5. Articles + Bylaws
6. Board roster
7. Governance policies (COI, whistleblower, doc retention, gift acceptance)
8. W-9
9. Insurance certificates
10. Key staff bios

## Contact
<Grant writer name + email + phone>
```

### Recipe 10: Bundle to a single PDF for funder portals

```bash
# Combine all PDFs into one bundle (most funders allow one combined PDF)
pdfunite org_credentials/irs/*.pdf \
  org_credentials/financials/*.pdf \
  org_credentials/governance/*.pdf \
  org_credentials/operating/*.pdf \
  org_credentials/501c3_packet_$(date +%Y%m%d).pdf
```

## Examples

### Example 1: Build packet for first federal proposal

**Goal:** Org has never done a federal proposal. Build the standard credentials packet.

**Steps:**
1. Verify 501(c)(3) status via IRS EO Search + ProPublica → save dated verification screenshot.
2. Locate IRS determination letter in board secretary files; scan if needed.
3. Pull last 3 years' 990s from ProPublica → save PDFs.
4. Request last 3 years' audited financials from CPA.
5. Gather articles + bylaws from board secretary.
6. Refresh COI disclosures + confirm whistleblower + doc-retention policies adopted by board.
7. Pull current board roster + assemble key staff bios.
8. Sign current W-9.
9. Assemble cover memo + bundle into single PDF.
10. Save to org_credentials/ and version in proposal library.

**Result:** Standard packet ready to attach to any federal or foundation proposal.

### Example 2: Verify a peer org's 501(c)(3) status (prospect research)

**Goal:** Confirm a peer org is a public charity 501(c)(3) before referencing them in our proposal.

**Steps:**
1. `curl https://projects.propublica.org/nonprofits/api/v2/search.json?q=PeerOrgName` → get EIN.
2. `curl https://projects.propublica.org/nonprofits/api/v2/organizations/<EIN>.json` → check subsection_code 03 + classification_codes 509(a)(1) or (a)(2).
3. Cross-check IRS EO Search for current Pub 78 + no auto-revocation.

**Result:** Verified status, EIN noted in prospect file.

## Edge cases / gotchas

- **Auto-revocation list.** Orgs that fail to file 990s for 3 years get auto-revoked. Verify NOT on the list at https://apps.irs.gov/app/eos/.
- **1023-EZ orgs.** Smaller orgs filed Form 1023-EZ since 2014 → less rigorous review. Some funders weight 1023-EZ orgs as "lighter" credibility; have org-credibility narrative ready.
- **Subsection 04 vs 03.** Many private foundations are 501(c)(3) but subsection 04 (private foundation, not public charity). Public charities are 03. Funders care about the distinction (sub-recipient rules differ).
- **State charitable registration.** Each state has its own charitable solicitation rules (~40 states). Funders may require state cert per state where org solicits. National Association of State Charity Officials (NASCO) is the reference.
- **Group exemption letters.** Religious / advocacy orgs may be covered by a group exemption (parent org's determination). Use parent's letter + group exemption documentation.
- **Fiscal sponsorship arrangements.** Sponsored projects do NOT have their own 501(c)(3) — sponsor's documentation attaches. Confirm with sponsor.
- **Foreign nonprofits.** US 501(c)(3) status is US-IRS-specific. Foreign orgs use Friends-of org structures (501(c)(3) US-side org + foreign affiliate).
- **Form 990 vs 990-EZ vs 990-N.** 990-N postcard for <$50K revenue; 990-EZ for $50K-$200K; full 990 for ≥$200K. Most funders expect to see the highest version filed.
- **Public Inspection Rule.** 990s must be available for public inspection on request (IRS rule). Refusing to provide a 990 = compliance flag.
- **Auditor opinion type.** Unmodified = clean. Modified = qualified or adverse. Going-concern = audit raises survival doubt. Funders read the opinion — be ready to narrate any non-clean opinion.
- **Disclaimer:** Binding tax-status questions → qualified nonprofit attorney / CPA.

## Sources

- IRS Tax Exempt Organization Search: https://apps.irs.gov/app/eos/
- ProPublica Nonprofit Explorer: https://projects.propublica.org/nonprofits/
- IRS Form 1023 / 1023-EZ instructions: https://www.irs.gov/forms-pubs/about-form-1023
- IRS Publication 78 (deductibility): https://apps.irs.gov/app/eos/
- IRS Form 990 instructions: https://www.irs.gov/forms-pubs/about-form-990
- National Council of Nonprofits — Principles and Practices: https://www.councilofnonprofits.org/running-nonprofit/administration-and-financial-management/principles-and-practices
- NASCO (state charitable registration): https://www.nasconet.org/
