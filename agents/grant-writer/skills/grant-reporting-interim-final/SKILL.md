---
name: grant-reporting-interim-final
description: Draft post-award grant reports — SF-425 Federal Financial Report + SF-PPR Performance Progress Report + foundation portal narratives. Reconcile to GL via xero-mcp. Anchor narrative to logic-model outcomes promised. Use when the user says "draft the quarterly report" / "the SF-425 is due" / "we need to file the final report".
---

# Grant reporting — interim, final, financial, programmatic

Reporting begins at award acceptance, not 11 months later. Federal reports: SF-425 (Federal Financial Report) + SF-PPR (Performance Progress Report). Foundations: portal-specific narrative + financials. Reconcile spend to GL; anchor narrative to logic-model outcomes promised.

Disclaimer: For binding interpretation of financial reporting or expenditure categorization, consult a qualified grants professional or CPA.

## When to use

- Quarterly / annual / final report due to federal funder
- Foundation annual progress / impact report due
- Closeout report 90 days post end-of-period
- Award acceptance: set up reporting cadence on day 1
- Funder requests off-cycle financial / programmatic update

Do NOT use this skill for:
- Single Audit prep (→ `single-audit-prep-federal-750k`)
- Budget creation for new proposals (→ `budget-narrative-justification`)
- Indirect cost reconciliation (→ `indirect-cost-nicra`)

## Setup

```bash
# Financial data pull
# - xero-mcp (Xero accounting)
# - cli-anything for QuickBooks Online API
# - postgresql-mcp for org data warehouse outcomes

# Report templates
ls agent_bundle/agents/grant-writer/templates/sf425_template.xlsx
ls agent_bundle/agents/grant-writer/templates/sf_ppr_template.docx
```

Auth / API key requirements:
- xero-mcp — OAuth (free for read; paid Xero subscription required)
- Grants.gov SF-425 / SF-PPR — submitted via Grants.gov portal
- Foundation portals — per-funder credentials

## Common recipes

### Recipe 1: At award acceptance — set up reporting schedule

```markdown
## Reporting schedule (calendar at award)
| Report | Frequency | Due | Form | Source |
|---|---|---|---|---|
| SF-425 Federal Financial | Quarterly | 30 days post-quarter | SF-425 | xero-mcp GL |
| SF-PPR Programmatic | Annual | 90 days post-year | SF-PPR | Outcomes data + narrative |
| Closeout final | One time | 90 days post-end | Final SF-425 + SF-PPR | All data + final narrative |
| Foundation interim | Per agreement | Per agreement | Funder template | GL + outcomes |
```

Calendar all of these in Google Calendar (skill: `grant-deadline-calendar-management`).

### Recipe 2: Set up outcome data collection on day 1

```markdown
## Day 1 program team conversation
- What outcomes did we promise in the proposal? (Pull from logic model)
- What indicator measures each outcome?
- Who collects what data?
- What's the data tool? (REDCap, Qualtrics, Salesforce, paper → Airtable)
- What's the collection schedule? (Pre, mid, post; monthly; quarterly)
- Who owns analysis? (Internal or external evaluator)
- Where does the data live? (Shared drive folder)
```

If outcome data collection isn't set up day 1, the 11th-month-of-the-grant scramble is inevitable.

### Recipe 3: Monthly GL pull + variance check

```bash
# Pull GL data filtered to grant project code
xero_get_general_ledger \
  organisation_id="$XERO_ORG_ID" \
  tracking_category="Project" \
  tracking_option="HRSA_MCH_2026" \
  from_date="2026-04-01" \
  to_date="2026-06-30"

# Variance check
# Compare actuals vs budget per object class
# Flag any line >10% variance to ED + Finance
```

### Recipe 4: SF-425 Federal Financial Report

```markdown
## SF-425 key fields
| Field | Source |
|---|---|
| Federal Agency / Awarding Organization | NoA |
| Federal Grant Number | NoA |
| Recipient Org | SAM entity |
| Reporting Period | Quarter / fiscal year |
| 10a. Cash Receipts | GL — cash drawdowns this period |
| 10b. Cash Disbursements | GL — federal expenditures this period |
| 10c. Cash on Hand (10a-10b) | Calc |
| 10d. Total Federal funds authorized | NoA total minus prior periods |
| 10e. Federal share of expenditures | GL federal-coded expenditures |
| 10f. Federal share of unliquidated obligations | Encumbrances |
| 10g. Total federal share (10e + 10f) | Calc |
| 10h. Unobligated balance (10d - 10g) | Calc |
| 10i. Recipient share required (match) | Per NoA |
| 10j. Recipient share of expenditures | GL match-coded expenditures |
| 10k. Remaining match (10i - 10j) | Calc |
| 10l. Total federal program income earned | GL revenue-coded |
| 11. Indirect Expense | Per NICRA or de minimis |
| 12. Remarks | Variances, explanations |
```

### Recipe 5: Pull data for SF-425 from Xero

```bash
# Via xero-mcp
xero_get_report_profit_and_loss \
  organisation_id="$XERO_ORG_ID" \
  tracking_category="Project" \
  tracking_option="HRSA_MCH_2026" \
  from_date="2026-04-01" \
  to_date="2026-06-30" \
  output="sf425_data_q1.csv"

# Cross-tab by object class for SF-424A-aligned breakdown
```

### Recipe 6: SF-PPR Performance Progress Report

```markdown
## SF-PPR structure
- Cover page: NoA info + reporting period + PI signature
- Section A: Status of activities + accomplishments
  - For each goal/objective from proposal:
    - Target promised
    - Actual achieved this period
    - Cumulative to date
    - Variance + explanation
    - Activities completed
    - Outcome evidence (data summary)
- Section B: Challenges + corrective actions
- Section C: Other significant items (publications, presentations, partnerships formed)
- Section D: Next period plan
- Attachments: evaluation data tables, evidence of outcomes
```

### Recipe 7: SF-PPR narrative anchored to logic model

```markdown
## Goal 1: <goal text from proposal>

### Objective 1.1
**Target:** By end of Year 1, 60 families enrolled in home-visiting program.
**Actual this quarter:** 18 families enrolled.
**Cumulative through Q3:** 47 families enrolled.
**Variance:** -22% behind target.
**Explanation:** Recruitment delayed by Q1 staff transition; new outreach specialist
hired in Feb 2026 has accelerated enrollment 35% MoM.
**Activities:** Community outreach events (4), partner clinic referrals
(12 referrals → 6 enrollments), social media campaign launched.
**Outcome evidence:** Pre-survey administered to all 47 enrolled families.
Mean baseline score on Parenting Self-Agency Measure: 3.2/5.

### Objective 1.2
...
```

### Recipe 8: Reconcile SF-425 to SF-PPR

```markdown
## Cross-check before submission
- Federal share of expenditures (SF-425 10e) should fund the activities reported
  in SF-PPR Section A
- If you spent $X on home visits but report 0 home visits delivered, the numbers
  contradict → reviewers flag
- Match column should align with match commitment in NoA
- Variance >25% requires written justification per 2 CFR 200
```

### Recipe 9: Foundation portal report

```markdown
## Foundation reports vary by funder; common elements:
- Narrative (1-3 pages): activities + outcomes + variances + next steps
- Financial: actuals vs budget by category
- Outcomes summary: indicator-by-indicator
- Stories: 1-2 beneficiary stories (with consent)
- Photos: with permission + caption
- Lessons learned + adaptations

## Pull from portal
# Fluxx / Foundant / Submittable have report templates
firecrawl_scrape url="https://<funder>.fluxx.io/apply/grantee/reports" formats=["markdown"]
```

### Recipe 10: Closeout report (90 days post-end-of-period)

```markdown
## Closeout content
- Final SF-425 (or foundation final financial)
- Final SF-PPR (or foundation final narrative)
- Final inventory of equipment purchased (if equipment >$10K)
- Final budget reconciliation (return unspent funds)
- Final outcomes data
- Sustainability update: which post-grant funders confirmed?
- Lessons learned memo for org learning + funder
- Property close: equipment disposition, intellectual property assignment
- Grant award files archived per record retention policy (typically 3 years post-closeout per 2 CFR 200.334)
```

### Recipe 11: Variance flagging + explanation

```markdown
## When to write a variance explanation
- Spend >10% under: explain why; clarify if unspent will be carried forward (federal NoA term)
- Spend >10% over a category: requires prior approval per 2 CFR 200.308
- Outcome variance >25%: explain root cause + corrective action
- Programmatic delay: explain + revised timeline + check no-cost extension needed
```

### Recipe 12: Submit per funder portal

```markdown
## Federal — Grants.gov
- Submit SF-425 + SF-PPR via Workspace
- Receipt confirmation within 1 hour

## NIH — eRA Commons RPPR
- Research Performance Progress Report through eRA
- Different system from Grants.gov

## Foundation
- Portal-specific (Fluxx, Foundant, Submittable, Bonterra)
- Some foundations accept email PDFs

## State / Local
- State systems vary widely; check each
```

## Examples

### Example 1: Q1 SF-425 for HRSA MCH grant

**Goal:** File quarterly SF-425 30 days post-quarter for ongoing HRSA grant.

**Steps:**
1. Pull GL for Q1 via xero-mcp (Recipe 5).
2. Cross-tab by SF-424A object class.
3. Compute Federal Share / Match Share / Program Income / Unobligated.
4. Fill SF-425 (Recipe 4).
5. Variance check vs budget (Recipe 3).
6. Submit via Grants.gov Workspace.
7. Log in Notion pipeline as filed; calendar next quarter.

**Result:** Q1 SF-425 filed; receipt confirmation archived.

### Example 2: Annual SF-PPR + reconciliation

**Goal:** Year 1 SF-PPR with outcome narrative for HRSA MCH grant.

**Steps:**
1. Pull outcomes data from Salesforce/REDCap via team's data lead.
2. Aggregate by indicator per logic-model outcome.
3. Draft SF-PPR Section A goal-by-goal, objective-by-objective (Recipe 7).
4. Compute variance per objective; explain each.
5. Draft Section B challenges + corrective actions (be honest; reviewers prefer transparency).
6. Draft Section D next period plan.
7. Attach evidence: data tables + 2 case studies (with consent).
8. Cross-check vs SF-425 cumulative (Recipe 8).
9. Submit via Grants.gov + email PO confirmation.

**Result:** Annual SF-PPR submitted; outcomes documented; next year plan clear.

## Edge cases / gotchas

- **Reporting cadence in NoA, not standard.** Read the Notice of Award (NoA) carefully — some federal awards require monthly, some annual; foundations vary widely.
- **Closeout 90 days post end-of-period.** Often missed because the project feels "done." Calendar at award start.
- **Carry-forward of unspent funds.** Some federal awards allow; some don't. Check NoA terms; request prior approval per 2 CFR 200.308.
- **No-cost extension request.** If timeline slips, request NCE 90+ days before end-of-period; federal allows up to 12 months one-time without supplemental approval.
- **Budget revision threshold.** Reallocation >10% between object class categories requires prior approval (2 CFR 200.308). Document.
- **Match underspend.** If you don't meet match requirement, federal can reduce federal share proportionally. Track match monthly.
- **Program income.** Federal awards may have specific program-income rules (added to federal share, deducted from federal share, or matched). Read NoA.
- **Outcome data quality.** Reviewers can tell when outcome data is "estimated." If you don't have data, say so + describe collection plan.
- **PII in attachments.** Beneficiary stories require consent + de-identification. NEVER attach PII without explicit release.
- **NIH RPPR vs SF-PPR.** NIH uses Research Performance Progress Report (different sections + indicators). Read NIH-specific guidance.
- **Foundation report formats vary.** Don't assume federal SF-PPR structure works for foundations. Adopt foundation's structure.
- **Records retention.** 2 CFR 200.334: 3 years post-closeout for most grants; longer if litigation pending or audit findings open.
- **Disclaimer:** For binding interpretation of variance explanations or expenditure categorization, consult a qualified grants professional or CPA.

## Sources

- Grants.gov Post-Award Reporting Forms: https://www.grants.gov/forms/post-award-reporting-forms.html
- SF-425 (PDF): https://www.grants.gov/web/grants/forms/post-award-reporting-forms.html
- SF-PPR (PDF): https://www.grants.gov/web/grants/forms/post-award-reporting-forms.html
- 2 CFR 200.308 — Revision of budget and program plans: https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-D/section-200.308
- 2 CFR 200.334 — Retention requirements for records: https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-D/section-200.334
- NIH RPPR Instructions: https://grants.nih.gov/grants/rppr/rppr_instruction_guide.pdf
- Xero API: https://developer.xero.com/
- Submittable: https://submit.com/
- Fluxx Grantseeker: https://www.fluxx.io/products/grantseeker
