---
name: non-compete-non-solicit-state-enforceability
description: State-by-state non-compete enforceability map + FTC Non-Compete Rule status (April 2024 final; stayed by 5th Cir Aug 2024; uncertain in 2026 — always fetch current). Non-solicit (employees + customers) typically more durable than non-compete. Output is the enforceability memo with the consult-an-attorney disclaimer.
---

# Non-Compete + Non-Solicit — State Enforceability Map

This skill is volatile — the FTC rule status changes; states pass new laws annually. Always fetch current data before drafting.

## When to use

User says:

- "Is this non-compete enforceable in [state]?"
- "Add a non-compete to employment / contractor agreement"
- "Non-solicit drafting"
- "FTC Non-Compete Rule status"
- "Garden leave"
- "Blue-pencil vs red-pencil reformation"
- "Choice of law overriding for non-compete"

Companion skills:
- `contract-review-msa-nda-employment` — employment + contractor agreements.
- `founders-agreement-vesting-ip-assignment` — founder departure terms.

## Setup

```bash
# NCSL state map — primary source
# https://www.ncsl.org/labor-and-employment/non-compete-agreements

# FTC Non-Compete Rule
# https://www.ftc.gov/legal-library/browse/rules/noncompete-rule
# https://www.federalregister.gov/documents/2024/05/07/2024-09171/non-compete-clause-rule

# 5th Circuit decision (August 2024 — stayed rule)
# https://www.ca5.uscourts.gov/

# State statutes (key ones below)

# Python helpers
pip install requests beautifulsoup4 pandas

# firecrawl-mcp for fetching changing pages
# (Configured in app/config/mcp_config.json)
```

## Common recipes

### Recipe 1: ALWAYS fetch current status before drafting
```bash
# FTC Non-Compete Rule status (April 2024 final → stayed by ND Texas + 5th Cir Aug 2024)
curl -fsSL https://www.ftc.gov/legal-library/browse/rules/noncompete-rule -o ftc_current.html

# NCSL state map (updated frequently)
curl -fsSL https://www.ncsl.org/labor-and-employment/non-compete-agreements -o ncsl_current.html

# Check key states for recent legislation
# 2024-2026 active jurisdictions: CA, MN, NY (proposed), MA, WA, CO, IL, VA, OR, NV, DC
```

### Recipe 2: State enforceability map (snapshot June 2026 — verify current)
| State | Enforceability | Wage threshold | Notes |
|---|---|---|---|
| **California** | VOID (Cal. Bus. & Prof. Code §16600) | N/A | Strictest. Even out-of-state choice of law overridden for CA employees (Cal. Labor Code §925). AB 1076 effective Feb 2024 voids retroactively + requires employer notice. |
| **North Dakota** | VOID (N.D. Cent. Code §9-08-06) | N/A | — |
| **Oklahoma** | VOID (15 OS §219A) | N/A | Limited carve-outs for sale-of-business |
| **Minnesota** | VOID for post-July 1 2023 (Stat. §181.988) | N/A | No retroactive; existing pre-July 2023 still enforceable |
| **Washington** | Enforceable above thresholds | ~$120k employee / ~$300k contractor (2024 — annual CPI adjust) | RCW 49.62; strict notice + consideration |
| **Massachusetts** | Enforceable with strict reqs (G.L. c. 149 §24L, 2018) | — | Garden leave OR mutually agreed consideration; 12-month max |
| **Texas** | Enforceable if reasonable + ancillary to otherwise enforceable agreement | — | Strong blue-pencil tradition |
| **Florida** | Enforceable per Stat. §542.335 | — | Strong statutory framework; favors employers; 2-year typical |
| **New York** | Enforceable but case-law strict | — | NY AG scrutiny on overreach. NY proposed ban (2023, vetoed); revived attempts |
| **Illinois** | Enforceable above wage thresholds (Stat. §820 ILCS 90) | $75k employee / $45k non-solicit (2024) | Strict notice + 14-day review |
| **Colorado** | Highly restricted (C.R.S. §8-2-113, 2022) | $112,500+ (2024 CPI) | Limited to highly-compensated employees; trade secret protection only |
| **Virginia** | Limited (Code §40.1-28.7:8) | $76k+ (2024) | Low-wage employee carve-outs |
| **Oregon** | Restricted (ORS §653.295) | $108,000+ (2024) | Required: 2-week written notice OR provided at hire |
| **Nevada** | Restricted (NRS §613.195) | — | Cannot prevent service to former customers if employee didn't solicit |
| **Maine** | Restricted | — | Bans for $59k+ employees, low-wage workers + healthcare |
| **Maryland** | Limited | $46.21/hr (2024) | Wage threshold |
| **New Hampshire** | Limited | — | Required disclosure before offer |
| **Rhode Island** | Limited | $14.34/hr (2024) | Low-wage worker ban |
| **District of Columbia** | Most banned (D.C. Code §32-581) | — | Bans for most employees; narrow exceptions |
| **Federal (FTC Rule)** | **Status uncertain in 2026** | — | Rule final April 23, 2024; effective Sept 4, 2024; stayed by ND Texas (Ryan, LLC v. FTC, Aug 20, 2024) → on appeal to 5th Cir. ALWAYS FETCH CURRENT |
| Other US states | Generally enforceable | — | Reasonable + ancillary + consideration; varying degrees of judicial scrutiny |

### Recipe 3: FTC Non-Compete Rule status (volatile)
```text
Timeline:
- April 23, 2024: FTC final rule
  - Bans new non-competes for ALL workers (except senior executives — $151,164+ + policy-making position)
  - Existing senior-executive non-competes enforceable
  - All others voided
  - Notice required to current/former workers within 180 days
- May 7, 2024: Federal Register publication
- August 20, 2024: ND Texas (Ryan, LLC v. FTC) — stayed nationally
- August/September 2024: 5th Cir appeal filed
- ?2025: 5th Cir decision (uncertain timing)
- ?2026: Possible Supreme Court review

As of June 2026: ALWAYS FETCH CURRENT before relying on FTC rule.

Drafting strategy:
- If FTC rule stayed → state law controls (Recipe 2 map)
- If FTC rule active → only senior executives + sale-of-business exceptions allowed
- If status uncertain → don't draft a new non-compete; use non-solicit + IP + confidentiality
```

### Recipe 4: Non-compete drafting requirements (where allowed)
```text
General requirements across most states:
1. Reasonable in time (typically 6-24 months; 12 months common)
2. Reasonable in geographic scope
3. Reasonable in scope of restricted activity
4. Necessary to protect legitimate business interest (trade secrets, customer relationships, goodwill)
5. Supported by consideration (employment + ongoing OR separate payment OR new role)
6. NOT contrary to public policy
7. Compliant with state-specific procedural reqs (notice, review period)
```

### Recipe 5: Non-solicit (more durable than non-compete)
```text
Non-solicit of EMPLOYEES:
- Standard 12-24 month after termination
- Covers active recruitment of former employees
- Does NOT prevent former employees from voluntarily seeking new role with you
- Enforceable in nearly all states

Non-solicit of CUSTOMERS:
- Standard 12-24 month after termination
- Covers solicitation of clients/prospects employee worked with
- Some states require customer list pre-defined
- Stronger if tied to confidentiality (you can't solicit using confidential info)
- Enforceable in most states

Non-solicit drafting:
"For [12/24] months after termination, [Employee] shall not directly or indirectly:
(a) solicit, induce, or encourage any employee of Company to leave Company OR to violate any agreement with Company, OR
(b) solicit, divert, or accept business from any client/customer of Company that Employee had material contact with during the [12] months prior to termination."

The CA exception:
Even in CA, non-solicit of CUSTOMERS may be void under Edwards v. Arthur Andersen, 44 Cal.4th 937 (2008) — interpreted broadly. Use carefully.
Non-solicit of EMPLOYEES is more likely enforceable in CA but still scrutinized.
```

### Recipe 6: CA choice-of-law override (Lab. Code §925)
```text
Cal. Labor Code §925 (2017):
- Applies to employees primarily working in CA
- Employer cannot require employee to:
  - Agree to non-CA choice of law for disputes arising in CA, OR
  - Agree to non-CA forum
- Exception: employee represented by counsel in negotiation

Practical: Out-of-state employer with CA employee CANNOT use Delaware/NY choice of law to enforce a non-compete that CA would void. CA law applies.
```

### Recipe 7: Garden leave alternative
```text
Garden leave = paid leave during which the employee is restricted from working elsewhere.

Used in:
- MA (G.L. c. 149 §24L — required consideration for non-compete is garden leave OR mutual)
- Sometimes UK / EU for senior executives
- Increasingly used as substitute for unenforceable non-compete

Mechanic:
- Employer pays full salary + benefits during restriction period
- Employee cannot work for competitor
- Mutual termination right after period
- Cost: 6-12 months salary

Pros: Avoids state-law enforceability issues
Cons: Expensive
```

### Recipe 8: Blue-pencil vs red-pencil reformation
```text
Blue-pencil: Court STRIKES unreasonable provisions but enforces the rest.
- TX, FL, IN, OH, WI, NJ (varies), TN
- Example: 5-year + nationwide non-compete → court enforces 1-year + 50-mile radius

Red-pencil: Court REWRITES unreasonable provisions to be reasonable.
- Some states permit, others reject (depends on state).
- More forgiving for employers.

NO-pencil (strict approach):
- Whole agreement void if any part unreasonable
- WA, MS, AR
- Drafting incentive: be conservative

CA: Most states void agreement entirely if unreasonable. CA is no-pencil for non-competes (void) but blue-pencil for non-solicit.

Drafting strategy: Conservative limits (6-12 months, narrow geographic + activity scope) regardless of state, to maximize enforceability.
```

### Recipe 9: Sale-of-business exception
```text
Most states exempt non-competes ancillary to a sale of business:
- Selling shareholder agrees not to compete with the acquirer
- Common 3-5 year + reasonable geographic scope
- Even CA permits: Cal. Bus. & Prof. Code §16601 (ownership sold), §16602 (LLC dissolution), §16602.5 (partnership dissolution)

Typical use: founder sells startup; agrees to non-compete to preserve goodwill being acquired.

Note: FTC 2024 rule had sale-of-business exception (>25% ownership sold).
```

### Recipe 10: Federal trade secret + non-compete substitute
```text
Even where non-competes are void, employer still has:
1. Federal Defend Trade Secrets Act (DTSA, 2016) — federal claim for trade secret misappropriation
2. State Uniform Trade Secrets Act (UTSA) — state claim
3. Non-disclosure / confidentiality clauses
4. IP assignment ("hereby assigns")
5. Non-solicit of employees + customers
6. Customer database protection
7. Notice provisions

In CA: rely heavily on (1)-(7). Don't try to enforce non-compete.

DTSA whistleblower immunity required notice:
Per 18 USC §1833(b), provide notice in NDA / IP agreement:
"An individual shall not be held criminally or civilly liable under any Federal or State trade secret law for the disclosure of a trade secret that—
(A) is made in confidence to a Federal, State, or local government official, either directly or indirectly, or to an attorney; and
(B) solely for the purpose of reporting or investigating a suspected violation of law; or
(C) is made in a complaint or other document filed in a lawsuit or other proceeding, if such filing is made under seal."

Without this notice, employer cannot recover exemplary damages + attorney fees under DTSA.
```

### Recipe 11: Memo skeleton — non-compete enforceability analysis
```markdown
# Non-Compete / Non-Solicit Enforceability Analysis — <Employee + State>

**Reviewed by:** Legal Counsel (AI agent)
**Date:** 2026-06-09
**State:** <state>
**Employee role:** <title>
**Compensation:** $<amount>

## State enforceability snapshot
- Non-compete: <Void / Restricted / Enforceable>
- Statute: <citation>
- Wage threshold (if applicable):
- Notice requirements:
- Court tradition: blue-pencil / red-pencil / strict

## Current FTC Non-Compete Rule status
- <Active / Stayed / Other> as of <date>
- If active: senior executive exception applies? <Y/N>
- Last checked: <date> — fetch from https://www.ftc.gov/legal-library/browse/rules/noncompete-rule

## Recommendation
### If non-compete sought:
- (a) Likely enforceable: <conditions> — proceed with strict drafting (Recipe 4)
- (b) Unlikely enforceable: replace with non-solicit (Recipe 5) + DTSA notice (Recipe 10)
- (c) Status uncertain: defer to non-solicit + confidentiality + IP

### If non-solicit:
- Employees: <12/24> months
- Customers: <12/24> months
- DTSA notice required
- §2870 carve-out (if CA)

## Alternative durability measures
- DTSA + state UTSA
- Confidentiality + IP assignment
- Customer non-solicit
- Employee non-solicit
- (For senior execs) Garden leave

---
**Disclaimer:** This is informational guidance from an AI agent. Always consult a licensed attorney in your jurisdiction before signing or relying on a non-compete, non-solicit, or related employment agreement. State law on non-compete enforceability changes frequently; FTC rule status is volatile. Verify current state of the law before relying on this analysis.
```

### Recipe 12: Common drafting pitfalls
```text
1. Worldwide / nationwide scope — usually unreasonable for individual employee.
   Better: limit to specific geographic area where employee worked OR specific industry.

2. Multi-year duration — beyond 24 months rarely enforceable for employees.
   Better: 6-12 months default; up to 24 for senior execs.

3. No consideration documented — many states require explicit consideration for non-compete.
   Better: hire offer + non-compete signed simultaneously OR sign-on bonus tied to non-compete.

4. Choice-of-law clause to friendly state — California (and increasingly others) override.
   Better: file in state where employee works.

5. Restraining "all related activities" — too broad.
   Better: enumerate specific competitors or specific job functions.

6. No carve-outs — employee can't work in unrelated industry.
   Better: carve out unrelated industries; carve out passive investments.

7. Forgetting state-specific notice rules.
   Examples: CA AB 1076 (notice of voided non-compete to current/former employees), IL (14-day review), OR (notice at hire OR 2 weeks before).

8. Trade secrets only — relying solely on trade secret protection without proper documentation.
   Better: classify + label confidential info + restrict access + audit logs.
```

## Examples

### Example 1: Drafting employment agreement for a CA software engineer
**Goal:** Maximize enforceability given CA law.
**Steps:**
1. Recipe 2 confirm CA voids non-competes.
2. Recipe 6 confirm §925 overrides any non-CA choice of law.
3. Drop non-compete entirely.
4. Include:
   - Confidentiality (Recipe 10 + DTSA notice)
   - IP assignment "hereby assigns" + §2870 carve-out
   - Non-solicit of employees (12-24 months)
   - Non-solicit of customers (12 months) — carefully drafted given Edwards v. Andersen
   - At-will employment
5. Recipe 11 memo for user; add disclaimer; send to licensed attorney.

**Result:** CA-compliant employment agreement.

### Example 2: VP-level executive joining a Massachusetts startup
**Goal:** 12-month non-compete with garden leave structure.
**Steps:**
1. Recipe 2 confirm MA permits with G.L. c. 149 §24L.
2. Required: garden leave OR mutually-agreed consideration.
3. Recipe 7 structure 12-month garden leave at 50% salary (mutually-agreed alternative).
4. 12-month max duration.
5. Recipe 11 memo; engage MA-licensed counsel.

**Result:** MA-compliant exec non-compete.

### Example 3: Founder sale of business
**Goal:** 3-year non-compete on founder selling startup to acquirer.
**Steps:**
1. Recipe 9 sale-of-business exception applies in nearly all states (including CA per §16601).
2. Reasonable scope: industry + geographic.
3. Reasonable duration: 3-5 years (longer than employment context).
4. Tied to ownership stake sold + consideration received.
5. Add disclaimer.

**Result:** Enforceable non-compete tied to sale.

## Edge cases / gotchas

- **FTC Non-Compete Rule status is volatile.** ALWAYS fetch https://www.ftc.gov/legal-library/browse/rules/noncompete-rule before drafting. Senior-executive exception, sale-of-business exception, notice obligations all depend on current status.
- **State laws change annually.** MN voided 2023; CO restricted 2022; CA enhanced 2024. Always check NCSL.
- **CA §925 overrides choice of law.** Don't think a Delaware choice-of-law clause saves you for CA employees.
- **CA AB 1076 retroactive notice (Feb 2024).** Employers must notify current + former employees in CA that their non-compete is void by Feb 14, 2024. Failure may trigger UCL claim.
- **"Blue-pencil" doesn't mean "court will save you."** Some states refuse to rewrite; whole agreement may fail.
- **Wage thresholds adjust annually.** WA, IL, OR, CO, VA, MD have CPI-adjusted thresholds. Verify current $.
- **Non-solicit broader than non-compete?** In CA, non-solicit of customers may be void post-Edwards if it functions as a de facto non-compete. Carefully draft tied to confidential info.
- **DTSA notice requirement.** Without DTSA whistleblower notice, can't recover exemplary damages + attorney fees. Easy add to NDAs/IPAs.
- **Garden leave is expensive.** 12-month salary + benefits — often $200k+. Reserve for senior execs.
- **International transfers.** EU non-competes (especially DE, FR, IT) often require explicit consideration during restriction period (paid). UK enforces "blue-pencil" but requires reasonableness. China + India have specific frameworks.
- **Customer lists as trade secret.** Some states recognize customer lists as protected trade secrets; others require additional protection. Audit your treatment.
- **No-poach + no-hire agreements between employers** (e.g., between competitors) violate antitrust (Sherman Act). Don't conflate with employee non-solicits.
- **Industry-specific bans.** Healthcare (many states ban physician non-competes), broadcasting (some state-specific rules), legal (state bar may prohibit), etc.
- **Mandatory arbitration + non-compete.** Many employers include both; CA AB 51 (struck down by 9th Cir) is volatile. Confirm arbitration enforceability separately.

> Warning: **This is informational guidance from an AI agent. State law on non-compete and non-solicit enforceability changes frequently; the FTC Non-Compete Rule status is volatile and unclear in 2026. Always consult a licensed attorney in your jurisdiction before signing, filing, or executing a non-compete, non-solicit, or related employment agreement, and verify current law before relying on this analysis.**

## Sources

- [NCSL Non-Compete State Map](https://www.ncsl.org/labor-and-employment/non-compete-agreements) — state-by-state.
- [FTC Non-Compete Rule](https://www.ftc.gov/legal-library/browse/rules/noncompete-rule) — federal rule + status.
- [FTC Non-Compete Rule Federal Register](https://www.federalregister.gov/documents/2024/05/07/2024-09171/non-compete-clause-rule) — final rule text.
- [Cal. Bus. & Prof. Code §16600](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=16600) — CA non-compete ban.
- [Cal. Labor Code §925](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=LAB&sectionNum=925) — CA choice-of-law override.
- [Cal. AB 1076 (2023)](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240AB1076) — CA retroactive notice.
- [MA G.L. c. 149 §24L](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXXI/Chapter149/Section24L) — MA non-compete framework.
- [WA RCW 49.62](https://app.leg.wa.gov/RCW/default.aspx?cite=49.62) — WA non-compete.
- [CO C.R.S. §8-2-113](https://leg.colorado.gov/sites/default/files/2021a_1024_signed.pdf) — CO restrictions.
- [IL 820 ILCS 90 (Freedom to Work Act)](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=4054) — IL framework.
- [OR ORS §653.295](https://www.oregonlegislature.gov/bills_laws/ors/ors653.html) — OR restrictions.
- [Edwards v. Arthur Andersen LLP, 44 Cal.4th 937 (2008)](https://casetext.com/case/edwards-v-arthur-andersen-llp-2) — CA non-solicit case.
- [Ryan, LLC v. FTC (ND Tex Aug 2024)](https://www.txnd.uscourts.gov/) — FTC rule stay.
- [18 USC §1833 — DTSA Whistleblower Notice](https://www.law.cornell.edu/uscode/text/18/1833) — DTSA notice requirement.
- Sister skills: `contract-review-msa-nda-employment`, `founders-agreement-vesting-ip-assignment`.
