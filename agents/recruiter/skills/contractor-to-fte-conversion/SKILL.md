<!--
Sources: https://www.deel.com/blog/contractor-to-employee
         https://www.workable.com/hr-terms/contractor-to-employee-conversion
         https://www.shrm.org/topics-tools/news/talent-acquisition/converting-contractors-to-employees
6-12 months of contractor work signals strong fit. Critical: classification audit (1099/W-2 in US,
IR35 in UK). Compressed loop OK; background check + I-9 still required. Defer classification +
IR35 + wording to legal-counsel.
-->
# Contractor-to-FTE Conversion — SKILL

Run the operational conversion: nomination → compressed interview loop → comp benchmarking → offer letter → background check + I-9 → start date. Critical: verify contractor was correctly classified during contract phase (1099 vs W-2 in US; IR35 vs PAYE in UK). Classification + binding wording defers to `legal-counsel`.

## When to use

- Manager nominates a contractor (6+ months on contract) for FTE conversion.
- Bulk conversion (post-acquisition, team-build via vendor unwind).
- IR35 / off-payroll-working reform in UK; mandatory worker-status review.
- Trigger phrases: "contractor to FTE", "1099 to W-2", "convert contractor", "contractor classification", "IR35", "co-employment", "FTE conversion offer".
- Defer to `legal-counsel`: classification audit, IR35 status determination, co-employment risk, non-compete on prior contract work.
- Defer to `operations-agent`: payroll setup, benefits enrollment, equity issuance.

## Setup

```bash
# ATS
export GREENHOUSE_API_KEY="harvest_xxx"
export GH_USER_ID="123456"

# Offer letter
export DOCUSIGN_ACCESS_TOKEN="<bearer>"

# Background check (still required for conversion in most cases)
export CHECKR_API_KEY="xxx"

# Comp benchmarking
export PAVE_API_KEY="xxx"
# or firecrawl Levels.fyi as free fallback

# Classification audit support (paid)
export DEEL_API_KEY="xxx"                  # Deel global classification flags
# https://developer.deel.com/

# Scheduling
export GOOGLE_CAL_OAUTH="<bearer>"
```

Auth model: standard ATS + offer-letter + background-check stack. Deel API specifically helpful for international classification.

## Conversion-eligible checklist

```text
Before manager nomination is accepted:
[ ] 6+ months contractor tenure (signals real fit + de-risks hire)
[ ] Performance trajectory: positive + improving (manager + skip-level confirm)
[ ] Manager confirms full-time equivalent need (not "use them more cheaply as contractor")
[ ] Budget approved for FTE conversion (HRBP / Finance handoff)
[ ] Classification audit: contractor was correctly classified during contract phase
[ ] No outstanding contract IP / confidentiality dispute
[ ] No non-compete blocker from contractor's prior arrangement
[ ] Work-authorization confirmed (visa requirements; H-1B sponsorship if applicable)
[ ] Geo + tax residence confirmed (multi-state / multi-country = added review)
[ ] Comp band per FTE role × level × geo
```

## Common recipes

### Recipe 1: Manager nomination intake (notion-mcp template)
```markdown
# Contractor Conversion Nomination — {contractor_name}

## Manager nomination
- Nominator: {manager}
- Contractor tenure: {months}
- Hours/week current: {N}
- Proposed FTE role: {title} / {level}
- Proposed start as FTE: {date}

## Why convert?
- Skill signal: {behavioral evidence}
- Culture signal: {behavioral evidence}
- Org need: {why FTE vs continued contract}

## Comp recommendation
- Manager target: ${base}-${base_high}
- Equity recommendation: {shares / %}
- Sign-on (if needed): ${amount}

## Risk flags
- [ ] Outstanding non-compete from prior arrangement
- [ ] Work auth concern (visa, sponsorship)
- [ ] Multi-state / multi-country tax residence
- [ ] Existing IP / NDA dispute

## Sign-off
- Manager: ___
- Skip-level: ___
- HRBP: ___
- Recruiter: ___
```

### Recipe 2: Compressed interview loop (NOT skip — abbreviated but real)
```text
Standard contractor-to-FTE loop:
- Recruiter screen (30 min): comp expectation + motivation + culture cross-check (skip role-fit; you have 6 mo of performance data)
- Hiring manager 1:1 (45 min): forward-looking outcomes + level + scope
- Skip-level 1:1 (30 min): leadership signal + growth trajectory
- Peer (45 min): collaboration + culture (someone they DIDN'T work with — find dispassionate signal)

Skip these compared to external candidate:
- Technical live-pair (you have 6 mo of code)
- Full panel (overkill — they're not net-new to the team)
- Take-home assessment (irrelevant)

Total: 2-3 hours over 1 week
```

### Recipe 3: Schedule compressed loop
```python
# google-calendar-mcp insert 4 events over 1 week
events = [
  {"title": "Recruiter screen — {contractor_name}", "duration_min": 30, "attendees": ["recruiter@acme.com"]},
  {"title": "HM 1:1 — {contractor_name}", "duration_min": 45, "attendees": ["hm@acme.com"]},
  {"title": "Skip-level — {contractor_name}", "duration_min": 30, "attendees": ["skip@acme.com"]},
  {"title": "Peer cross-check — {contractor_name}", "duration_min": 45, "attendees": ["peer@acme.com"]}
]
# google_calendar.events.insert for each
```

### Recipe 4: Comp benchmark for contractor's new FTE role
```bash
# Use offer-negotiation-comp-band-equity-perks skill's Pave/Levels.fyi recipe
curl -s -H "Authorization: Bearer $PAVE_API_KEY" \
  "https://api.pave.com/v1/comp/benchmark?role=engineer&level=senior&geo=us_remote&company_size=200-500"
# Anchor at appropriate percentile for stage + role.
# Note: contractor's prior rate often exceeds FTE base (no benefits/taxes); use FTE total comp not contractor day rate as the comparison.
```

### Recipe 5: Classification audit (US 1099/W-2 — IRS 20-factor test)
```text
20-factor test (high-level):
- Behavioral control (who decides how work is done?)
- Financial control (who provides tools? Reimbursement?)
- Relationship type (permanency, integration into business)

If contractor:
- Worked exclusively for you 6+ months
- Used company laptop / tools / Slack / email
- Followed your processes / standups
- Was integrated into team comms
- Did the same work as FTEs in their function
→ likely should have been W-2 the whole time = classification risk = back-tax + penalty exposure

Action: legal-counsel reviews; if misclassified, payroll back-correction may be required.
Don't proceed with FTE conversion until classification audit is complete.
```

### Recipe 6: Classification audit (UK IR35 — off-payroll working)
```text
IR35 Status Determination Statement (SDS) required:
- "Inside IR35" = should be PAYE / employment-like
- "Outside IR35" = genuine self-employed contractor

Factors:
- Substitution clause (can contractor send someone else?)
- Mutuality of obligation (must you give work? Must they take it?)
- Control (who directs the day-to-day?)
- Equipment + risk + integration

Action: HR + legal-counsel issue SDS before conversion; if "inside IR35" for prior 12 months, payroll back-correction may apply.
```

### Recipe 7: Generate FTE offer letter (DocuSign)
```bash
# Use offer-letter-docusign-pandadoc skill's Recipe 2
# Key fields specific to conversion:
# - "Effective start date as FTE" (not first-day-with-company)
# - PTO accrual reset (or pre-credit per local policy + manager discretion)
# - Equity grant — new FTE-level grant; prior contract work didn't accrue equity
# - Benefits effective date (often start date or T+30 days)
# - No "contractor → FTE = same role" assumption — confirm title, level, scope
```

### Recipe 8: Background check (still required)
```bash
# Even with 6+ months on contract, BG check often required by policy:
curl -s -X POST -H "Authorization: Bearer $CHECKR_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.checkr.com/v1/invitations" \
  -d '{"candidate":{"email":"contractor@example.com"},"package":"standard"}'
# Defer FCRA flow to background-check-checkr-sterling skill.
```

### Recipe 9: I-9 verification (US)
```text
US: I-9 within 3 business days of FTE start date.
Contractor period doesn't count; I-9 must be completed for FTE relationship.
Operations-agent owns the I-9 execution; recruiter coordinates timing.
```

### Recipe 10: Multi-state tax residence flag
```text
If contractor worked remote from multiple states / countries:
- Tax residence at start date matters for state withholding + benefits eligibility
- Some states have nexus implications for employer (CA, NY, MA aggressive)
- Defer to operations-agent / payroll for setup
- Cross-border: separate entity, EOR (Employer of Record) like Deel/Remote, or terminate + re-engage via local entity
```

### Recipe 11: Equity grant for converted FTE
```text
Standard pattern:
- New FTE-level grant at conversion start
- Standard vesting (4yr / 1yr cliff)
- Contractor period does NOT count for vesting cliff
- Some companies offer "credit" for tenure (cliff reduced from 12mo to 6mo)
- Board approval required for grant; Carta issuance after
- Defer 83(b) timing to legal-counsel
```

### Recipe 12: Post-conversion sentiment check at day 30
```text
Hidden risk: contractor "lost autonomy" feel after conversion (no longer day-rate flexibility).
Day-30 1:1 with manager + recruiter: explicit conversation about what changed + what's working.
Renege risk for converted contractors is LOWER than external hires but emotional friction higher.
```

## Examples

### Example 1: Senior engineer 8-month contract → FTE
**Goal:** Convert Sara (8 months contract on payments team) to Senior Backend FTE.
**Steps:**
1. Recipe 1: manager nomination + skip-level + HRBP sign-off.
2. Recipe 5: classification audit; legal confirms 1099 was at risk → process correction in next payroll.
3. Recipe 2 + 3: compressed loop over 1 week.
4. Recipe 4: comp benchmark; offer at 65th percentile (strong contractor performance).
5. Recipe 7 + 8 + 9: offer letter + background check + I-9 plan.
6. Recipe 11: standard equity grant; cliff at month 6 (credit for contract tenure not given per company policy).
7. Day-1: ops-agent owns onboarding execution; recruiter coordinates Day-1 readiness.

**Result:** Smooth conversion; Sara joins FTE without org reset.

### Example 2: Post-acquisition vendor unwind (10 contractors)
**Goal:** Acquired company terminates vendor relationship; convert 10 contractors to FTE.
**Steps:**
1. Recipe 1 ×10: manager nominations.
2. Recipe 5: bulk classification audit (likely needs corrections per past co-employment).
3. Recipe 2: batch compressed loops over 3 weeks.
4. Recipe 4: comp benchmarks; range-set bulk offer band.
5. Recipe 7: letters via DocuSign batch.
6. Operations-agent: payroll + benefits + equity bulk setup.

**Result:** Vendor terminated cleanly; 10 FTEs onboarded; co-employment risk closed.

### Example 3: UK IR35 status review + conversion
**Goal:** UK contractor's IR35 SDS = "inside" — convert to PAYE FTE.
**Steps:**
1. Recipe 6: legal issues IR35 SDS retroactively + going-forward.
2. HR + payroll back-correct PAYE for in-IR35 period.
3. Recipe 2 + 7: standard conversion process.
4. Convert to UK FTE entity OR engage via Deel EOR if no UK entity.

**Result:** IR35 compliant; tax exposure closed.

## Edge cases / gotchas

- **Classification audit is the #1 risk.** Misclassification penalties: US ~25-50% back-tax + interest + state penalties (CA AB5 strict); UK IR35 ~back-tax + NICs + interest. Don't skip the audit.
- **Co-employment risk.** Using staffing-agency contractors → employee-like treatment can create joint employer liability. Defer to `legal-counsel`.
- **Non-compete enforceability.** Contractor's prior arrangement may have IP/non-compete clauses that affect FTE conversion. Audit before offer.
- **Equity vesting cliff.** Some companies credit contract tenure (rare); most don't. Set expectation explicitly in offer; surprise = renege risk.
- **PTO reset.** Most companies reset PTO at FTE start; contractor period doesn't accrue. Communicate clearly.
- **Benefits enrollment window.** Often must enroll within 30 days of FTE start. Operations-agent owns the deadlines; recruiter ensures contractor knows.
- **Comp friction.** Contractor day-rate often translates to higher than FTE base when annualized (no benefits/taxes loaded). Frame total comp not day rate.
- **Title / level drift.** "Senior contractor" doesn't mean "Senior FTE level" — they're different ladders. Confirm level explicitly with manager + HRBP.
- **Visa / work-auth.** Contractor on visa (B1/B2 / J1) may not be FTE-eligible. H-1B sponsorship adds 6-12 month timeline. Recruiter flags early.
- **State tax nexus.** US contractor working remote from a non-employer state may create nexus for employer. Defer to `legal-counsel` + `operations-agent` payroll.
- **GDPR / data residency.** If contractor was outside EU but accessing EU data, conversion may trigger residency review. Defer to legal.
- **Skipping the loop entirely.** Tempting since you have 6mo of work product. Don't — short loop establishes the FTE expectation + level + comp clearly. Skipping invites confusion later.
- **Defer to `legal-counsel`** for: classification audit, IR35 SDS, co-employment risk, IP / non-compete review, equity grant doc.
- **Defer to `operations-agent`** for: payroll + benefits + equity issuance + I-9 execution, multi-state tax setup, EOR coordination if cross-border.

## Sources

- [Deel — Contractor to Employee Conversion](https://www.deel.com/blog/contractor-to-employee)
- [Deel API](https://developer.deel.com/)
- [Workable — Contractor-to-Employee guide](https://www.workable.com/hr-terms/contractor-to-employee-conversion)
- [SHRM — Converting Contractors to Employees](https://www.shrm.org/topics-tools/news/talent-acquisition/converting-contractors-to-employees)
- [IRS 20-factor test](https://www.irs.gov/businesses/small-businesses-self-employed/independent-contractor-defined)
- [California AB5 (independent contractor test)](https://www.dir.ca.gov/dlse/faq_independentcontractor.htm)
- [UK IR35 / off-payroll working](https://www.gov.uk/guidance/check-employment-status-for-tax)
- [HMRC IR35 status determination](https://www.tax.service.gov.uk/check-employment-status-for-tax)
- [Form I-9 timing (USCIS)](https://www.uscis.gov/i-9-central)
