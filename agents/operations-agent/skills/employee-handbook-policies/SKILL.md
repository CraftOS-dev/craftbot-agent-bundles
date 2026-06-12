<!--
Sources: https://www.trainual.com/ , https://gusto.com/
Multi-state handbook + PTO + remote/hybrid + AI usage policy templates.
HRIS-templated state-specific policies; non-binding; defer to legal-counsel for binding review.
-->
# Employee Handbook + Policies — SKILL

Author and version-control the employee handbook and adjacent policies: PTO, leave, remote/hybrid, code of conduct, anti-harassment, AI usage, BYOD, IP assignment, expense, equipment, social media. Pulls Gusto / Rippling / Justworks templated state-specific clauses; assembles in `docx` + Notion + Trainual; tracks signed acknowledgments.

## When to use

- New company → first handbook.
- Multi-state expansion → add state-specific addenda (CA, NY, MA, IL, WA, CO are the heavy ones).
- New policy roll-out: AI usage, remote/hybrid, equipment, expense, BYOD.
- Annual review (the federal/state law refresh).
- Trigger phrases: "handbook", "PTO policy", "leave policy", "remote work policy", "AI policy", "BYOD", "code of conduct", "acknowledge", "ACK".

## Setup

```bash
# Authoring local
# Notion + docx + markdown-converter + Google Drive — no API key needed

# HRIS templated policies
export GUSTO_API_KEY="xxx"
export RIPPLING_API_KEY="xxx"
export TRAINUAL_API_TOKEN="xxx"   # https://trainual.com — paid

# Signature / ACK tracking
export DOCUSIGN_TOKEN="xxx"       # or hellosign / dropbox-sign
export NOTION_TOKEN="xxx"
```

## Common recipes

### Recipe 1: Handbook section index (skeleton)
```markdown
# Employee Handbook — [Co]
## 1. Welcome
   1.1 About us
   1.2 Our values
   1.3 How to use this handbook
## 2. Employment basics
   2.1 At-will employment (US states except MT)
   2.2 Equal employment opportunity (EEO)
   2.3 Non-discrimination + anti-harassment
   2.4 Drug-free workplace
## 3. Workplace policies
   3.1 Code of conduct
   3.2 Conflicts of interest
   3.3 Confidentiality + IP assignment
   3.4 Acceptable use of technology
   3.5 AI / GenAI usage (Recipe 7)
   3.6 Social media
   3.7 Workplace safety
## 4. Compensation + benefits
   4.1 Pay schedule + deductions
   4.2 Overtime + classification (FLSA exempt vs non-exempt)
   4.3 Benefits overview (med/dental/vision/401k/HSA)
   4.4 Equity (reference comp philosophy)
## 5. Time off
   5.1 PTO (Recipe 2)
   5.2 Sick leave (state-specific: CA, NY, WA, MA — Recipe 3)
   5.3 Holidays
   5.4 Bereavement
   5.5 Jury duty + voting leave
   5.6 Parental leave (Recipe 4)
   5.7 FMLA + state FMLA equivalents
## 6. Remote + hybrid
   6.1 Work-from-anywhere policy (Recipe 5)
   6.2 Equipment + expense (Recipe 6)
   6.3 In-office days + booking
## 7. Performance + development
   7.1 Review cycle
   7.2 1:1 expectations
   7.3 Learning + development budget
## 8. Separation
   8.1 Resignation
   8.2 Termination
   8.3 Final-pay timing (state-specific)
   8.4 Equipment return
## 9. State-specific addenda
   9.A California
   9.B New York
   9.C Massachusetts
   9.D Illinois
   9.E Washington
   9.F Colorado
   9.G Other
## 10. Acknowledgment
   I have read and understood the Employee Handbook.
```

### Recipe 2: Open PTO policy template
```markdown
## 5.1 Paid Time Off (PTO)
**Eligibility:** Full-time US employees, effective Day 1.

**Accrual + use:** This is an open / flexible PTO policy.
You are expected to take **at least 15 working days off per year**, including a 5-day continuous block.
There is no fixed cap; we trust you and your manager to plan around team coverage.

**Request process:** Submit PTO ≥ 2 weeks ahead for trips >3 days. Use [HRIS calendar tool].
For coverage-critical roles (on-call, finance close), align with rotation calendar.

**Sick days:** Unlimited. Notify your manager same morning. Doctor's note only required after 3 consecutive days (or per state law).

**Holidays:** 11 US federal/cultural holidays (see calendar). One floating cultural holiday.

**State-specific minimum sick leave** (overrides above where stricter):
- CA: 5 days / 40 hours/yr accrued (1 hour per 30 worked). HSL Law.
- NY (NYC): up to 56 hours/yr depending on employer size.
- WA: 1 hour per 40 hours worked.
- MA: 1 hour per 30 hours, up to 40 hours.
- See state addenda.

> **Defer to `legal-counsel` for binding state-by-state minimum-leave reconciliation, especially in CA, NY, NJ, MA, RI, OR, WA, CO, IL, MD.**
```

### Recipe 3: Per-state sick leave matrix (Python)
```python
STATE_SICK_LEAVE = {
    'CA': {'rate':'1h/30h worked','annual_cap':'40h','carryover':'48h','use_after':'90 days'},
    'NY-NYC':{'rate':'1h/30h','annual_cap':'40h or 56h (employer size)','carryover':'40h'},
    'WA':{'rate':'1h/40h','annual_cap':'no cap','carryover':'40h'},
    'MA':{'rate':'1h/30h','annual_cap':'40h','carryover':'40h'},
    'OR':{'rate':'1h/30h','annual_cap':'40h','carryover':'40h'},
    'NJ':{'rate':'1h/30h','annual_cap':'40h','carryover':'40h'},
    'RI':{'rate':'1h/35h','annual_cap':'40h','carryover':'40h'},
    'CO':{'rate':'1h/30h','annual_cap':'48h','carryover':'48h'},
    'CT':{'rate':'1h/40h','annual_cap':'40h','carryover':'40h'},
    'IL':{'rate':'1h/40h','annual_cap':'40h','carryover':'80h'},
    'MD':{'rate':'1h/30h','annual_cap':'40h','carryover':'40h'},
    'VT':{'rate':'1h/52h','annual_cap':'40h','carryover':'40h'},
    'ME':{'rate':'1h/40h','annual_cap':'40h','carryover':'40h'},
    'NM':{'rate':'1h/30h','annual_cap':'64h','carryover':'unused'},
}
```

### Recipe 4: Parental leave template
```markdown
## 5.6 Parental Leave
**Birthing parent:** 16 weeks fully paid (including FMLA period).
**Non-birthing / adoptive parent:** 10 weeks fully paid.
**Eligibility:** All FT employees, no waiting period.

**Stacking + state PFL:**
- CA PFL, NY PFL, NJ PFL, WA PFL, MA PFML, CT PFML, CO FAMLI, OR PFML coordinate with company leave.
- Net pay protected to 100% (state benefits + company top-up).

**Job protection:** Same role or substantially similar on return.
**Phase-back:** 80% schedule for first 4 weeks back, full pay.

> **Defer to `legal-counsel` for binding FMLA / state PFL coordination; mis-coordination triggers significant penalty risk.**
```

### Recipe 5: Remote + hybrid policy template
```markdown
## 6.1 Work-from-Anywhere
**Categories:**
- **Remote:** primary residence is the working location, no expectation of in-office days.
- **Hybrid (2 days/wk):** 2 anchored days per week per team calendar.
- **Hybrid (3 days/wk):** 3 anchored days.
- **In-office:** 5 days a week.

**Residence-of-record:** Employee's tax-residence state/country on HRIS = tax + benefits + comp tier basis. Notify People Ops 30 days before any move > 1 county.
**Temporary travel:** ≤ 30 days / yr in a different state may not trigger nexus; ≥ 30 days requires People Ops + tax review.
**International:** WFA from another country only via EOR or pre-approved entity; **defer to `legal-counsel` for tax-residency + work-permit confirmation**.

**In-office expectations** (for hybrid + in-office):
- Anchor days per team posted in [calendar].
- Room/desk booking via Robin / Envoy.

**Equipment:** see Recipe 6.
```

### Recipe 6: Equipment + expense policy
```markdown
## 6.2 Equipment + Expense
**Provided at hire:** Laptop (per spec sheet) + accessories budget ($500 first 90 days).
**Refresh:** Every 4 years or sooner on failure.
**Internet stipend:** $75/mo for fully-remote employees.
**Home office one-time:** $1,000 (chair, desk, monitor) reimbursable on receipt within first 90 days.
**Co-working stipend:** $200/mo reimbursable on receipt for employees without home office.
**Cell phone:** Personal device; reimbursable up to $50/mo for business use.
**Software:** request via internal-tools intake; do NOT expense.
**Receipts:** required for ≥ $25; submit via [expense tool] within 30 days.
**Per diem:** $75 daily travel meals; ≥ $100 in any single meal requires receipt + business reason.
```

### Recipe 7: AI / GenAI usage policy (2026)
```markdown
## 3.5 Acceptable AI Usage
**Approved tools (Tier-A — any data):**
- ChatGPT Enterprise / Claude for Work / Gemini Workspace under our SSO and DPA.
- GitHub Copilot Enterprise (no training on private code).

**Approved tools (Tier-B — public/internal data only, no PII/customer/IP):**
- Claude.ai personal, ChatGPT free/Plus, Perplexity, Gemini consumer.

**Prohibited (data classification):**
- Customer PII, PHI, payment data → only Tier-A.
- Source code in IP-sensitive areas → only Tier-A.
- Employee PII → only Tier-A.

**Rules:**
- All AI-generated code merged into production requires human review.
- Disclose AI assistance in deliverables when the output is the primary work product (per role).
- No prompt injection of credentials, secrets, customer keys.
- Vendor AI features (e.g., Notion AI, Linear AI) require People Ops approval before enabling org-wide.

**Frameworks referenced:** NIST AI RMF, ISO 42001, EU AI Act Articles 5/10/26 obligations.

> **Defer to `legal-counsel` for binding EU AI Act exposure assessment (Risk tier mapping for HR / hiring uses).**
```

### Recipe 8: Push handbook ACK to all employees (Gusto)
```bash
curl -s -X POST "https://api.gusto.com/v1/companies/<co>/document_signatures" \
  -H "Authorization: Bearer $GUSTO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "title":"2026 Employee Handbook — ACK",
    "document_file_url":"https://drive.google.com/...handbook.pdf",
    "signers":"all_active_employees",
    "due_date":"2026-07-15"
  }'
```

### Recipe 9: Versioned Notion handbook with audit history
```bash
# Notion page with a `Version` property + `Effective Date` + `Owner`
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_TOKEN" -H "Content-Type: application/json" -H "Notion-Version: 2022-06-28" \
  -d '{
    "parent":{"database_id":"<handbook-db>"},
    "properties":{
      "Section":{"title":[{"text":{"content":"5.1 PTO"}}]},
      "Version":{"rich_text":[{"text":{"content":"v2026.07"}}]},
      "Effective Date":{"date":{"start":"2026-07-01"}},
      "Owner":{"people":[{"id":"<people-ops-lead>"}]}
    }
  }'
```

### Recipe 10: Trainual policy training rollout
```bash
curl -s -X POST "https://api.trainual.com/v1/topics" \
  -H "Authorization: Bearer $TRAINUAL_API_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "title":"Q3 2026 Handbook Refresh",
    "content_html":"<h1>...</h1>",
    "assigned_to":["all_employees"],
    "due_within_days":14,
    "quiz":{"required_passing":80,"questions":[...]}
  }'
```

## Examples

### Example 1: First handbook for a 25-person 3-state startup
**Goal:** Compliance-clean v1 in 2 weeks.
**Steps:**
1. Recipe 1: section skeleton in `docx`.
2. Recipe 2-7: populate per templates.
3. State addenda for CA + NY + MA from Recipe 3 + Gusto template pull.
4. Legal review (sibling `legal-counsel`).
5. Recipe 9: import to Notion handbook DB with version v2026.07.
6. Recipe 8: push ACK signature collection via Gusto.

**Result:** Versioned handbook + signed ACKs in HRIS audit trail.

### Example 2: Add AI policy mid-cycle
**Goal:** Roll out AI usage policy to existing handbook.
**Steps:**
1. Recipe 7 → drop into Section 3.5.
2. Recipe 9: new version v2026.10 published in Notion.
3. Recipe 10: Trainual topic + quiz; 14-day due window.
4. Recipe 8: re-ACK only the policy diff (Gusto supports policy-only signing).

**Result:** Employees acknowledge AI policy without re-signing the whole handbook.

## Edge cases / gotchas

- **At-will employment exclusions.** MT (just-cause), public-sector employees, union employees. Don't generalize at-will language.
- **EEO + protected classes vary by state.** CA + NY + IL include more (sexual orientation, gender identity, ancestry, marital status, source of income). **Defer to `legal-counsel`.**
- **Final-pay timing.** CA = same day on involuntary termination; MA = same day; MI/MO = next regular payday. Sect 8.3 must reference state-specific.
- **Stacking PFL with company leave.** Tax treatment matters; structure as 100% net-pay protection rather than additive to avoid windfalls.
- **Trainual ACK ≠ DocuSign signature.** For binding ACK, route through Gusto (Recipe 8) or DocuSign; Trainual is training compliance, not signature.
- **Version drift.** Without Recipe 9 versioning + Effective Date, you can't prove what policy was in force on a given date. Audit risk.
- **Open PTO + unused-PTO payout.** Open PTO sidesteps the wage-equivalent payout obligation that accrued PTO creates in CA, MT, NE. Document carefully. **Defer to `legal-counsel`.**
- **Cell phone reimbursement (CA Labor Code §2802).** California requires reasonable reimbursement of business cell use; flat $50/mo is widely accepted but contestable.
- **Remote work + nexus.** A single employee in NY can create NY corporate-tax nexus. Coordinate Recipe 5 with finance.
- **EU AI Act (Aug 2026 enforcement on high-risk AI).** HR uses (hiring, performance, attendance) may be high-risk. Recipe 7 needs an addendum once enforcement starts. **Defer to `legal-counsel`.**
- **Sexual harassment training mandates** (CA, NY, CT, DE, IL, ME, WA): biennial. Wire training schedule into Trainual.

## Sources

- Trainual: https://www.trainual.com/
- Gusto handbook builder: https://gusto.com/products/hr/handbook
- Rippling Handbook: https://www.rippling.com/products/handbook
- NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework
- EU AI Act: https://artificialintelligenceact.eu/
- DocuSign API: https://developers.docusign.com/
- Notion API: https://developers.notion.com/
- CA HSL: https://www.dir.ca.gov/dlse/Paid_Sick_Leave.htm
- NYC ESSTA: https://www.nyc.gov/site/dca/about/paid-sick-leave-FAQs.page
