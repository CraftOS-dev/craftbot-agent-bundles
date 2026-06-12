<!--
Source: https://visible.vc/product/data-rooms/
Source: https://www.ycombinator.com/documents
Source: https://carta.com/learn/startups/fundraising/data-room/
Source: https://www.docsend.com/blog/startup-fundraising/
-->

# Fundraising data room — section-by-section setup

Build a complete, organized, defensible data room for due diligence. Standard sections + YC SAFE post-money template + term sheet review framework.

## When to use

- Pre-fundraise: build data room 4-6 weeks before outreach.
- Active raise: maintain + provide access per stage of diligence.
- M&A discussions: extended data room with additional sections.
- Annual investor refresh: keep updated even when not raising.
- Trigger phrases: "data room", "diligence", "DD", "SAFE", "term sheet", "investor docs".

NOT for: legal opinions on term sheet (defer to `legal-counsel`); product / technical diligence (separate flow with engineering).

## Data room structure (industry standard)

```
00_PINNED                       # docs every investor wants first
  /00_Pitch_Deck.pdf
  /00_Executive_Summary.pdf
  /00_Quick_Stats.pdf            # 1-page metric snapshot

01_COMPANY                      # entity + governance
  /01_Cert_Incorporation.pdf
  /02_Bylaws.pdf
  /03_Board_Resolutions/         # historical, in order
  /04_Stockholder_Resolutions/
  /05_409A_Valuations/           # all historical 409A reports
  /06_Board_Meeting_Minutes/     # last 24 months
  /07_Org_Chart.pdf

02_CAP_TABLE
  /01_Cap_Table_Current.pdf      # latest snapshot from Carta/Pulley
  /02_Cap_Table_Historical/      # per-round snapshots
  /03_Stock_Option_Plan.pdf      # ESOP doc
  /04_Outstanding_Grants.xlsx    # all option grants, vesting, exercise
  /05_SAFEs_and_Notes/           # all convertible instruments
  /06_Warrant_Agreements/

03_FINANCIAL
  /01_Audited_Financials/        # if applicable (Series B+ usually)
  /02_Unaudited_Financials/      # monthly P&L / BS / CF for trailing 24 months
  /03_Financial_Model.xlsx       # forward 3-5 year projection
  /04_Budget_vs_Actual_Tracker.xlsx
  /05_Cash_Flow_Forecast_13W.xlsx
  /06_Bank_Statements/           # last 12 months
  /07_Capitalization_History.xlsx
  /08_Revenue_Recognition_Schedule.xlsx  # ASC 606 waterfall

04_REVENUE_METRICS              # the metrics investors review
  /01_ARR_MRR_Trend.xlsx
  /02_Cohort_Retention.xlsx
  /03_NRR_GRR_Computation.xlsx
  /04_CAC_LTV_Computation.xlsx
  /05_Customer_List/             # anonymized for early diligence; full at LOI
  /06_Top_Customer_Detail.xlsx   # 10-20 largest customer ARR/usage
  /07_Pipeline_Detail.xlsx       # at LOI stage
  /08_Churn_Analysis.xlsx

05_CONTRACTS                    # material agreements
  /01_Customer_Master_Agreements/  # template + any negotiated MSAs
  /02_Top_Customer_Contracts/     # 10-20 largest (material)
  /03_Vendor_Contracts_Material/  # hosting, payment processor, etc.
  /04_Office_Lease/
  /05_Equipment_Leases/
  /06_Loan_Agreements/

06_LEGAL_AND_IP
  /01_Trademark_Registrations/
  /02_Patent_Applications/
  /03_Patent_Grants/
  /04_Copyright_Registrations/
  /05_Open_Source_License_Audit.xlsx
  /06_IP_Assignment_Agreements/   # ALL employees + contractors
  /07_NDA_Templates/
  /08_Domain_Names_Registry/
  /09_Litigation_Summary/        # current + historical; "none" if applicable

07_PEOPLE
  /01_Founders_Bios.pdf
  /02_Key_Hires_Resumes/
  /03_Employee_Census.xlsx       # anonymized at early diligence
  /04_Compensation_Bands.xlsx
  /05_Hiring_Plan_FY27.xlsx
  /06_Org_Structure_Current.pdf
  /07_HR_Policies/                # handbook, harassment, etc.

08_PRODUCT_AND_TECH
  /01_Product_Roadmap.pdf
  /02_Architecture_Overview.pdf
  /03_Security_Documentation/
  /04_SOC2_Report/                # if applicable
  /05_Privacy_Policy.pdf
  /06_Terms_of_Service.pdf
  /07_Vulnerability_Scans/

09_MARKETING_AND_GTM
  /01_Marketing_Plan_FY27.pdf
  /02_Customer_Acquisition_Channels.xlsx
  /03_Sales_Methodology.pdf
  /04_Brand_Assets/
  /05_Press_Coverage/

10_TAX_AND_INSURANCE
  /01_Tax_Returns/                # 3 years federal + state
  /02_Sales_Tax_Filings/
  /03_R&D_Credit_Documentation/
  /04_Nexus_Map.xlsx
  /05_Insurance_Policies/         # D&O, E&O, cyber, general liability

99_DEAL_SPECIFIC                # populated at LOI
  /01_Term_Sheet_Drafts/
  /02_SAFE_or_Note_Agreements/
  /03_Investor_Rights_Agreement_Draft/
  /04_Voting_Agreement_Draft/
  /05_Right_of_First_Refusal_Draft/
  /06_Stock_Purchase_Agreement_Draft/
```

## Setup

```bash
# Storage — choose ONE primary platform
# Recommended:
# - Visible.vc Data Rooms — built-in tracking + investor access
# - DocSend — engagement analytics
# - Google Drive / Dropbox / Notion — simpler, less tracking

# Cap-table snapshot tool
# - Carta API (via carta-pulley-cap-table skill)

# File organization (already shipped):
# - file-organizer
# - google-sheet / google-drive
```

## Common recipes

### Recipe 1 — Initialize data room from template

```bash
mkdir -p data_room/{00_PINNED,01_COMPANY,02_CAP_TABLE,03_FINANCIAL,04_REVENUE_METRICS,05_CONTRACTS,06_LEGAL_AND_IP,07_PEOPLE,08_PRODUCT_AND_TECH,09_MARKETING_AND_GTM,10_TAX_AND_INSURANCE,99_DEAL_SPECIFIC}
mkdir -p data_room/01_COMPANY/{03_Board_Resolutions,04_Stockholder_Resolutions,05_409A_Valuations,06_Board_Meeting_Minutes}
mkdir -p data_room/02_CAP_TABLE/{02_Cap_Table_Historical,05_SAFEs_and_Notes,06_Warrant_Agreements}
# ... build full directory tree from template
```

### Recipe 2 — Generate current cap-table snapshot (PDF)

```python
# Pull from Carta
import requests, os
cap_table = requests.get(
  f"https://api.carta.com/v1alpha/companies/{COMPANY_ID}/cap-table",
  headers={"Authorization": f"Bearer {os.environ['CARTA_TOKEN']}"}
).json()

# Render to PDF via docx → pdf
from docx import Document
doc = Document()
doc.add_heading(f"Cap Table — {company_name} — {date.today()}", 0)
table = doc.add_table(rows=1, cols=5)
hdr = table.rows[0].cells
hdr[0].text, hdr[1].text, hdr[2].text, hdr[3].text, hdr[4].text = \
  "Stakeholder", "Instrument", "Shares", "% of FD", "Status"

for stake in cap_table.stakeholders:
    row = table.add_row().cells
    row[0].text = stake.name
    row[1].text = stake.instrument
    row[2].text = f"{stake.shares:,.0f}"
    row[3].text = f"{stake.percent_fd:.2%}"
    row[4].text = stake.status

doc.save("data_room/02_CAP_TABLE/01_Cap_Table_Current.docx")
# Convert to PDF via pandoc-branded-deliverables skill
```

### Recipe 3 — Generate financial summary pack

```python
# 3-statement summary for trailing 24 months
def financial_pack_for_data_room():
    months = pd.date_range("2024-07-01", periods=24, freq="MS")
    pnl_rows = []
    bs_rows = []
    cf_rows = []
    for m in months:
        pnl = xero.reports.profit_and_loss(
          fromDate=m.strftime("%Y-%m-01"),
          toDate=(m + pd.offsets.MonthEnd(0)).strftime("%Y-%m-%d")
        )
        bs = xero.reports.balance_sheet(date=(m + pd.offsets.MonthEnd(0)).strftime("%Y-%m-%d"))
        cf = xero.reports.cash_summary(
          fromDate=m.strftime("%Y-%m-01"),
          toDate=(m + pd.offsets.MonthEnd(0)).strftime("%Y-%m-%d")
        )
        pnl_rows.append({"month": m, **pnl.summary})
        bs_rows.append({"month": m, **bs.summary})
        cf_rows.append({"month": m, **cf.summary})

    # Save 3 sheets in one xlsx
    with pd.ExcelWriter("data_room/03_FINANCIAL/02_Unaudited_Financials.xlsx") as writer:
        pd.DataFrame(pnl_rows).to_excel(writer, sheet_name="P&L", index=False)
        pd.DataFrame(bs_rows).to_excel(writer, sheet_name="Balance Sheet", index=False)
        pd.DataFrame(cf_rows).to_excel(writer, sheet_name="Cash Flow", index=False)
```

### Recipe 4 — YC standard SAFE document

YC post-money SAFE: https://www.ycombinator.com/documents

Standard fields to fill (cap-only or discount-only or both):

```yaml
investor_name: "Acme Ventures, LP"
investor_address: "..."
purchase_amount: "$1,000,000"
post_money_valuation_cap: "$10,000,000"
discount_rate: "20%"     # or "N/A" for cap-only
mfn_clause: false        # most favored nation
pro_rata_rights: true    # standard add-on
date_signed: "2026-06-15"
```

YC also has SAFE letter agreement variants. Use as-is; only modify if your counsel insists.

### Recipe 5 — Term sheet review checklist

Standard Series A term sheet redlines (consult `legal-counsel` for binding interpretation):

```markdown
TERM SHEET REVIEW (non-binding checklist; defer to counsel)

ECONOMICS
- [ ] Pre-money valuation: $X
- [ ] Investment amount: $Y
- [ ] Post-money: X + Y
- [ ] Price per share: $Z
- [ ] Pool top-up to N% (pre-money pool top-up dilutes existing more)
- [ ] Liquidation preference: 1x non-participating (industry standard); 1x participating = WORSE; 2x+ = AVOID
- [ ] Dividends: 8% non-cumulative non-compounding (standard); cumulative = aggressive
- [ ] Anti-dilution: weighted-average broad-based (standard); full ratchet = AVOID

GOVERNANCE
- [ ] Board: 3 seats — 1 investor / 2 founders (standard at Series A)
- [ ] Investor consent rights / protective provisions — check scope (asset sale, IPO, debt, etc.)
- [ ] Drag-along: standard
- [ ] Tag-along: standard
- [ ] Voting: 1 share = 1 vote

INFORMATION RIGHTS
- [ ] Annual audited financials
- [ ] Quarterly financials + KPIs
- [ ] Annual budget
- [ ] Right to inspect books

EMPLOYEE TERMS
- [ ] Founder vesting reset/refresh — common but negotiate
- [ ] Acceleration: double-trigger (Change of Control + termination without cause)

CLOSING
- [ ] Pro-rata rights for investor in subsequent rounds
- [ ] Right of first refusal (ROFR) — investor right to participate before stranger
- [ ] Exclusivity / no-shop: 30-45 days standard, longer = aggressive
- [ ] Closing conditions: legal due diligence, definitive docs
- [ ] Expense reimbursement: $50-75K standard for Series A; cap it
```

### Recipe 6 — Investor access management

```python
# Visible.vc — grant access per stage
def grant_data_room_access(investor_email, stage):
    if stage == "screening":
        allowed = ["00_PINNED", "04_REVENUE_METRICS/01_ARR_MRR_Trend.xlsx"]
    elif stage == "diligence":
        allowed = ["00_PINNED", "01_COMPANY", "02_CAP_TABLE",
                   "03_FINANCIAL", "04_REVENUE_METRICS", "07_PEOPLE"]
    elif stage == "loi":
        allowed = ["*"]  # everything except 99_DEAL_SPECIFIC
    elif stage == "term_sheet":
        allowed = ["*"]  # including deal docs
    visible.set_permissions(investor_email, allowed)
```

Track who has access, what was viewed, who downloaded.

### Recipe 7 — Diligence questionnaire response template

Investors typically send a 50-100 question questionnaire mid-diligence. Pre-populate a master response doc:

```markdown
DILIGENCE QUESTIONNAIRE RESPONSES

(General)
Q: Company history? A: Founded [date]; key milestones [list].
Q: Mission statement? A: [...]

(Customers + revenue)
Q: Top 5 customers % of revenue? A: Top 5 = 38% of ARR; top 10 = 58%.
Q: Customer concentration risk? A: No single customer >12% of ARR.
Q: Churn rate (logo + revenue)? A: Logo churn 1.2%/mo; revenue churn 0.9%/mo (offset by expansion).
Q: NRR trajectory? A: [Trailing 12 months trend].

(Financials)
Q: Burn rate trend? A: T3M $185K/mo net burn (Recipe from runway-burn-analysis).
Q: Path to profitability? A: Default-Alive at current growth + burn discipline.
Q: Major non-recurring items in financials? A: [Itemize].

(Team)
Q: Key person risk? A: [Identify + mitigation: documentation, key person insurance, etc.]
Q: Recent departures (>3 months tenure)? A: [List with reasons + replacement status].

(Tech / IP)
Q: Open source dependencies? A: Audit attached (06_LEGAL_AND_IP/05).
Q: Customer data protection? A: SOC2 in progress; current security posture summary.

(Legal)
Q: Active litigation? A: None / [list].
Q: Regulatory exposure? A: [Per jurisdiction; sales-tax via Anrok; data per GDPR/CCPA].

(Cap table)
Q: Outstanding SAFEs / notes? A: 4 SAFEs totaling $2.1M; cap-table impact attached.
```

### Recipe 8 — Track investor engagement via DocSend

```bash
# DocSend per-investor view + time-on-page
curl -H "Authorization: Bearer $DOCSEND_API_KEY" \
  https://api.docsend.com/v1/documents/$DOC_ID/views
# Returns: per-viewer page time + last access
```

Surface to founder: "Investor X spent 14 min on Cap Table page — strong interest signal."

### Recipe 9 — Pre-diligence walkthrough checklist

Before opening the data room:

```markdown
[ ] All 409A reports current + uploaded
[ ] Cap table reconciles to Carta as of yesterday
[ ] Last close completed; current financials uploaded
[ ] Top customer contracts uploaded (signed PDFs)
[ ] IP assignment agreements verified for ALL employees + contractors (no gaps)
[ ] Open source license audit completed
[ ] Outstanding SAFEs / notes listed with cap + discount
[ ] Board meeting minutes for last 24 months in chronological order
[ ] Tax returns 3 years federal + relevant state
[ ] Pitch deck current (within last 30 days)
[ ] Each top-level folder has a README.md explaining structure
```

### Recipe 10 — Post-close cleanup

After round closes:

```markdown
[ ] Cap table updated to post-close state
[ ] Signed definitive docs filed in 99_DEAL_SPECIFIC
[ ] Investor access permissions cleaned up
[ ] Routine investor reporting cadence established (Visible.vc / monthly update)
[ ] Next 409A scheduled (annual or post-round trigger)
[ ] Equity grant pool re-set per new ESOP plan
[ ] Onboarding new board observer (if applicable)
[ ] Update SOC2 if security commitments part of close
```

## Examples

### Example 1: Series A data room build (6-week preparation)

**Goal:** Series A raise targeting $10M; build complete data room.

**Steps:**

**Week 1:**
1. Recipe 1: Initialize directory structure.
2. Generate quick-stats 1-pager + pitch deck refresh.
3. Recipe 3: Build financial pack (trailing 24 months).

**Week 2:**
4. Recipe 2: Cap-table snapshot from Carta.
5. Schedule 409A refresh if stale (Carta-Pulley `carta-pulley-cap-table` Recipe 4).
6. IP assignment audit — verify every contractor + employee signed.

**Week 3:**
7. Top-10 customer contracts upload.
8. Open source license audit.
9. Insurance docs.

**Week 4:**
10. Tax returns + R&D credit documentation.
11. Diligence questionnaire pre-populated (Recipe 7).
12. Cohort retention + unit economics (`unit-economics-saas-metrics`).

**Week 5:**
13. Walkthrough checklist (Recipe 9).
14. Mock diligence with friendly investor for feedback.
15. Polish.

**Week 6:**
16. Final cap-table snapshot.
17. Pre-flight review with counsel.
18. Set up DocSend / Visible.vc tracking.
19. Generate pitch deck final.
20. Begin outreach.

**Result:** Data room ready when first investor requests access; diligence questions answered before asked.

### Example 2: Friendly seed round on YC SAFE

**Goal:** $500K from 5 angels on YC post-money SAFE; minimal diligence.

**Steps:**

1. Use YC SAFE post-money template (Recipe 4) — $5M cap, no discount.
2. Light data room: 1-pager + financials summary + cap table.
3. SAFE letter sent via gmail (no full data room needed).
4. Each investor signs SAFE + sends wire.
5. Record SAFE in Carta (`carta-pulley-cap-table` Recipe).
6. 30 days post-close: monthly investor updates begin (see `investor-update-monthly-quarterly`).

**Result:** Round closes in 2-3 weeks; minimal admin burden.

## Edge cases / gotchas

- **IP assignment gaps:** the single most common diligence break. Every employee + contractor MUST have a signed IP assignment. Audit comprehensively pre-raise.
- **409A stale:** if 409A is >12 months or material event since, refresh before opening data room. Stale = 409A penalty exposure surfaces in diligence.
- **Cap-table truth in dispute:** if Carta and signed agreements disagree, signed agreements govern. Reconcile in advance.
- **Customer concentration:** if one customer >20% of ARR, prepare narrative explaining diversification path.
- **Non-disclosure on SAFE holders:** SAFE holders typically have less rights than priced-round investors — they may not need full data room access; share what's required by the SAFE.
- **MFN clause activation:** if you've granted MFN in past SAFEs, any new SAFE with better terms (lower cap, higher discount) re-prices the old SAFEs. Track + disclose.
- **State filings:** Delaware annual franchise tax + state foreign qualifications often forgotten. Investors check at later stages.
- **Convertible note maturity:** notes have maturity dates; if you didn't convert by maturity, you're technically in default. Refinance / convert via amendment.
- **Open-source compliance:** AGPL / GPL / copyleft licenses may infect proprietary code. Audit thoroughly; some investors require GPL-free.
- **Confidentiality breach risk:** data room is competitive intelligence if it leaks. Use NDAs + watermarking (DocSend) at minimum.
- **Side letters:** different investors negotiate different terms. Maintain a side-letter log. Disclose to all major holders.
- **Data room hygiene:** delete superseded versions; clear file naming; folder README.md explaining structure. Sloppy data room = sloppy company.

## Sources

- Visible.vc Data Rooms: https://visible.vc/product/data-rooms/
- YC standard documents: https://www.ycombinator.com/documents
- Carta data room guide: https://carta.com/learn/startups/fundraising/data-room/
- DocSend startup fundraising: https://www.docsend.com/blog/startup-fundraising/
- Cooley GO (legal docs): https://www.cooleygo.com/
- NVCA model docs (Series A): https://nvca.org/model-legal-documents/

## Related skills

- `carta-pulley-cap-table` — cap-table snapshot for data room
- `equity-grant-83b-isos-rsus` — SAFE conversion + grant docs
- `investor-update-monthly-quarterly` — ongoing investor comms
- `monthly-close-procedure` — financials section is built here
