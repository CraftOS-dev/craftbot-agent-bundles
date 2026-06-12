---
name: founders-agreement-vesting-ip-assignment
description: Draft founders agreements + co-founder vesting + IP assignment from founders/contractors. 4-year / 1-year cliff vesting (market), single / double trigger acceleration, company repurchase right at cost on departure, explicit "hereby assigns" IP language + CA Labor Code §2870 carve-out. Output is a complete founders agreement with the consult-an-attorney disclaimer.
---

# Founders Agreement + Vesting + IP Assignment

## When to use

User says:

- "Draft a founders agreement"
- "Co-founder vesting"
- "IP assignment from founders / contractors"
- "Equity split between founders"
- "What happens if a co-founder leaves?"
- "4-year vest / 1-year cliff"
- "Acceleration on CoC"
- "Reverse vesting"
- "Work-for-hire vs hereby assigns"

Companion skills:
- `equity-grants-isos-rsus-83b-election` — 83(b) election for restricted stock.
- `safe-convertible-note-yc-template` — early-stage fundraising.
- `term-sheet-review-series-a-typical-terms` — Series A founder vesting refresh.
- `contract-review-msa-nda-employment` — contractor agreements.

## Setup

```bash
# Cooley GO Founders Stock + Agreement
# https://www.cooleygo.com/documents/founders-stock/
# https://www.cooleygo.com/documents/founders-agreement/

# Stripe Atlas Founder Templates
# https://stripe.com/atlas

# Clerky Incorporation + Founders
# https://www.clerky.com/

# IP assignment templates
# https://www.cooleygo.com/documents/proprietary-information-and-inventions-agreement/

# CA Labor Code §2870 — carve-out for personal-time / no-company-resources inventions
# https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=LAB&sectionNum=2870

# 17 USC §101 — Work for hire definition
# https://www.law.cornell.edu/uscode/text/17/101

# Python helpers
pip install python-docx pandas
```

## Common recipes

### Recipe 1: Founders agreement skeleton
```markdown
# Founders Agreement — <Company Name>

**Effective Date:** 2026-06-09

## Parties
- Founder A: <Name>, role, address
- Founder B: <Name>, role, address
- (Optional Founder C, D)

## Equity split
- Founder A: <X>% (<Y> shares of Common Stock)
- Founder B: <X>% (<Y> shares of Common Stock)
- Initial common stock issued at par ($0.0001/share) → Founder pays total $<Z>
- 83(b) election filed within 30 days of grant (see attached)

## Vesting
- 4-year vest with 1-year cliff
- Vesting start: <date>
- Monthly vest thereafter (after cliff)
- Pre-vested founder shares vest 0% pre-cliff, 25% at cliff, then 1/48 monthly

## Reverse vesting / company repurchase right
- Company has the right to repurchase UNVESTED shares at original purchase price ($<Z> per share) on:
  - Voluntary termination by founder
  - Termination for cause
  - Death / disability (vested only, optionally)
- ROFR by company on transfers to third parties (vested shares)

## Acceleration
- Single trigger (CoC alone): <0% | 25% | 50%>
- Double trigger (CoC + involuntary termination within 12 months): 100% of unvested vests

## IP assignment
- Each Founder hereby (present-tense) assigns to the Company all IP related to the business made by Founder before or during the engagement
- Pre-existing IP listed in Schedule A is excluded
- Includes inventions, software, designs, trademarks, copyrights, trade secrets, know-how
- Includes work product whether made on personal time/equipment EXCEPT as carved out by Cal. Lab. Code §2870 (CA founders) or equivalent state law

## Confidentiality
- Each Founder agrees to maintain confidentiality of company proprietary info
- Survives termination indefinitely for trade secrets; 5 years for general confidential info

## Roles + responsibilities (advisory)
- Founder A (CEO): <responsibilities>
- Founder B (CTO): <responsibilities>
- Material decisions require mutual consent

## Decision-making
- Day-to-day: each Founder within their domain
- Material: mutual written consent
- Tie-breaking: <board chairperson / mutually-agreed advisor>

## Resignation / departure
- 30-day notice required
- Unvested shares forfeit (subject to company repurchase right)
- Vested shares retained
- Non-compete: <state-dependent — 12mo subject to enforceability>
- Non-solicit: 24-month for employees + customers

## Non-disparagement
- Mutual; survives termination

## Dispute resolution
- Good-faith negotiation (30 days) → mediation → AAA Commercial Arbitration

## Governing law
- <State>, USA

## Severability + entire agreement + amendment in writing

## Signatures

---
**Disclaimer:** This is informational guidance from an AI agent. Always consult a licensed attorney before signing or executing a Founders Agreement, particularly regarding equity split, vesting, and IP assignment terms.
```

### Recipe 2: Equity split — common patterns
```text
2-founder splits:
- 50/50 — easy, but creates deadlock risk; consider tie-breaking
- 60/40 — recognizes asymmetric contribution
- 55/45 — split for asymmetric contribution
- Initial idea contributor often gets 5-10% premium

3-founder splits:
- 33/33/33 — easy but deadlock risk
- 40/30/30 — leader + two others
- 50/25/25 — CEO + two domain leads
- 60/20/20 — strong leader + two supporters

Dynamic equity:
- Slicing Pie (Mike Moyer) — equity vests proportional to actual contributions
- Less common in 2026; most founders use fixed split + vesting

Key principle: AVOID 50/50 deadlock without tie-breaking mechanism.
```

### Recipe 3: Vesting structure — 4-year / 1-year cliff explained
```text
"4-year vest with 1-year cliff, monthly thereafter":

Day 1 (grant): 0 shares vested
Months 1-11: 0 shares vested
Month 12 (cliff): 25% of total vests in one batch
Months 13-48: 1/48 per month vests
Month 48: 100% vested

If founder leaves between month 0 and month 12 (pre-cliff): forfeits ALL shares (subject to company repurchase right at cost).

Why this structure:
- Aligns long-term commitment
- Cliff protects against short-tenured founders
- Monthly cadence keeps founders engaged ongoing

Alternatives (less common):
- 3-year vest (sometimes used for advisors, not founders)
- No cliff (riskier — founder leaves at month 2 with 6 weeks of vest)
- Annual vest (less granular)
```

### Recipe 4: Pre-vested founder shares + reverse vesting
```text
Founders typically receive ALL shares at incorporation (or shortly after).
Vesting = company's right to REPURCHASE if founder leaves before vesting completes.

Mechanics:
- Founder pays par × total shares upfront (e.g., $0.0001 × 1M = $100)
- Stock Purchase Agreement signed
- Reverse-vesting schedule attached
- 83(b) election filed within 30 days (CRITICAL — see equity-grants-isos-rsus-83b-election)

If founder leaves at month X:
- Vested shares (X/48 of total) — founder keeps
- Unvested shares (1 - X/48 of total) — company repurchases at original price ($100 × proportion)
```

### Recipe 5: Acceleration triggers
```text
Single trigger acceleration:
- On Change of Control (CoC) alone (M&A, IPO)
- 25-50% of unvested vests
- Why: rewards founder for the deal
- Investor pushback: makes acquisition harder + more expensive

Double trigger acceleration:
- On Change of Control AND involuntary termination within X months (typically 12-24)
- 100% of unvested vests
- Why: protects founder against post-acquisition firing
- Market standard 2026

Definitions:
- "Change of Control" = sale of substantially all assets, merger where company doesn't survive, sale of >50% voting power
- "Involuntary termination" = without cause OR resignation for good reason (compensation cut, role change, location move)

Single trigger is rare and founder-favorable. Push for double trigger as floor.
```

### Recipe 6: IP assignment — "hereby assigns" not "agrees to assign"
```text
CRITICAL DIFFERENCE:
- "Founder hereby assigns to Company all IP..."
  → Present-tense vesting — IP transfers automatically as created
  → Strong, enforceable

- "Founder agrees to assign to Company all IP..."
  → Future promise — requires separate assignment act
  → Weaker; Founder could refuse to execute the separate assignment

Case law:
- DDB Technologies v. MLB Advanced Media, 517 F.3d 1284 (Fed. Cir. 2008)
  Held that "agrees to assign" creates contract right, not automatic assignment
  Required ongoing executions

Always use "hereby assigns" in founders / contractor / employment agreements.
```

### Recipe 7: Work-for-hire ≠ enough for software
```text
17 USC §101 "Work made for hire" categories:
1. Work prepared by employee within scope of employment
2. Work specially ordered or commissioned for use as:
   - Contribution to collective work
   - Part of motion picture / audiovisual work
   - Translation
   - Supplementary work
   - Compilation
   - Instructional text
   - Test
   - Answer material for test
   - Atlas

SOFTWARE CODE IS NOT IN THE LIST.

For contractor-developed software:
- "Work for hire" language alone DOES NOT transfer ownership
- Must add explicit "hereby assigns" backup

Standard contractor IP language:
"To the maximum extent permitted by law, all Work Product shall be deemed 'work made for hire' (17 USC §101). To the extent any Work Product is not deemed work for hire, Contractor hereby irrevocably assigns to Company all right, title, and interest in and to such Work Product, including all intellectual property rights therein."
```

### Recipe 8: California Labor Code §2870 — required carve-out
```text
CA Lab. Code §2870 invalidates any IP assignment to the extent it requires assignment of an invention that:
- Was developed entirely on the employee's own time
- Without using employer equipment, supplies, facilities, or trade secrets
- UNLESS the invention either:
  (a) relates to the employer's business or research/development; OR
  (b) results from work performed by the employee for the employer

Required notice (CA Lab. Code §2872):
- Notice must be given to the employee at the time the assignment is signed
- Notice describes the §2870 carve-out

Without §2870 carve-out: assignment may be unenforceable for personal-time inventions.

Other states with similar laws:
- DE, IL, KS, MN, NC, UT, WA, NJ, NV, RI

Always include §2870 carve-out for CA-based founders/employees/contractors:

"Notwithstanding the foregoing, this Agreement does not require assignment of any invention that Founder developed entirely on Founder's own time without using Company equipment, supplies, facilities, or trade secrets, and that does not relate to the Company's business or actual or demonstrably anticipated research or development, and does not result from work performed by Founder for the Company (Cal. Labor Code §2870)."
```

### Recipe 9: PIIA (Proprietary Information and Inventions Agreement)
```text
PIIA is the IP + confidentiality contract for employees (separate from employment agreement).

Components:
1. Confidentiality (perpetual for trade secrets; 3-5 years for confidential)
2. IP assignment ("hereby assigns") + §2870 carve-out
3. Pre-existing IP exclusion (Schedule A listing)
4. Return / destruction on termination
5. Non-solicit (12-24 months, state-dependent)
6. Notice of conflicting third-party obligations (must inform on hire)

Every employee + contractor signs a PIIA on day 1. Critical for due diligence at fundraising.
```

### Recipe 10: Pre-existing IP — Schedule A
```markdown
# Schedule A — Pre-existing IP (excluded from assignment)

Founder identifies any IP created BEFORE company formation that Founder wants to retain:

- Github repos: github.com/foundera/personal-project (MIT-licensed; not used in company product)
- Side-project app: <name> (separate company; no overlap with current business)
- Pending patents: US Provisional 63/<number> (assigned to other entity)
- Trademarks: <Mark> registered to Founder personally
- Other:

If Schedule A is empty, founder represents that all IP created before is unrelated to the business or that founder is not aware of any.

Importance: Without Schedule A, the agreement may inadvertently assign pre-existing IP to the company — including non-business projects.
```

### Recipe 11: Buy-sell / drag-along among founders
```text
Among founders, common provisions:
- ROFR: Company first, then other founders, then outside transfer
- Drag-along: If founders representing X% (typically 75%) approve a sale, remaining founders must sell
- Tag-along: If a founder sells to outside party, other founders can join pro-rata
- Right of First Negotiation (ROFN): Mutual obligation to offer to other founders first

These overlap with Series A documents but are useful pre-financing.
```

### Recipe 12: What happens when a co-founder departs
```text
Scenarios:

1. Pre-cliff voluntary departure (month 0-11):
   - Founder forfeits ALL shares
   - Company repurchases at cost ($100 × ratio)
   - 30-day notice
   - Vested shares: 0
   - Non-compete + non-solicit applies

2. Post-cliff voluntary departure (month 12+):
   - Founder keeps vested shares (X/48 of total)
   - Unvested shares: company repurchases at cost
   - 30-day notice
   - Non-solicit applies; non-compete state-dependent

3. Termination for cause (theft, fraud, criminal, breach):
   - Vested shares: typically forfeit OR company repurchase at cost (cause definition matters)
   - Unvested: company repurchase at cost
   - No severance, no acceleration

4. Termination without cause:
   - Vested shares: retained
   - Unvested: company repurchase at cost
   - May trigger severance if employment agreement
   - May trigger acceleration if double trigger + CoC nearby

5. Death / disability:
   - Vested shares: pass to estate (subject to ROFR)
   - Unvested: company can repurchase OR vest immediately depending on plan terms
```

## Examples

### Example 1: Two co-founders forming a Delaware C-corp
**Goal:** Standard founders agreement with 60/40 split.
**Steps:**
1. Incorporate (Clerky / Stripe Atlas / Atlas / direct).
2. Issue 6M shares to Founder A, 4M to Founder B at par.
3. Each Founder pays $600 / $400 respectively (par × shares).
4. Sign Stock Purchase Agreement with vesting schedule (Recipe 3-4).
5. File 83(b) within 30 days (see `equity-grants-isos-rsus-83b-election`).
6. Sign Founders Agreement (Recipe 1) covering IP, decision-making, departure.
7. Sign PIIA (Recipe 9) — separate IP + confidentiality.
8. Schedule A listing pre-existing IP.
9. Add §2870 carve-out (Recipe 8).
10. Add disclaimer; send to user's licensed attorney.

**Result:** Complete founder documentation, audit-ready for Series A.

### Example 2: Adding a 3rd co-founder mid-stage
**Goal:** Add late co-founder with 10% post-existing.
**Steps:**
1. Founders A + B issue new common shares to Founder C.
2. Founder C pays par × shares.
3. Founder C signs Stock Purchase Agreement with 4-year vest, 1-year cliff from C's start date.
4. Founder C files 83(b) within 30 days of C's grant.
5. Founders Agreement updated to include C (or new amendment).
6. C signs PIIA.

**Result:** Founder C added with proper documentation.

### Example 3: Co-founder departs at month 8 (pre-cliff)
**Goal:** Document departing founder's forfeiture.
**Steps:**
1. Founder gives 30-day notice.
2. Company exercises repurchase right on all unvested shares (= all shares, since pre-cliff).
3. Company pays founder back original purchase price.
4. Cap table updated.
5. Confirm non-solicit + non-compete (state-dependent) apply.
6. Confirm IP assignment survives (founder cannot take company IP).

**Result:** Clean exit without dead-equity drag on cap table.

## Edge cases / gotchas

- **No vesting = dead equity.** A founder who leaves at month 9 keeping 33% locks up the cap table → uninvestable. ALWAYS vest founder stock.
- **50/50 split without tie-breaker.** Deadlock kills companies. Build in tie-breaking mechanism (advisor, board, mutually-agreed third party).
- **"Agrees to assign" instead of "hereby assigns."** Weakens IP transfer; courts may require separate executions. Always use "hereby assigns."
- **Work-for-hire alone for software.** Software is NOT in 17 USC §101 list. Always include explicit "hereby assigns" backup.
- **Missing §2870 carve-out for CA founders.** Required by CA Lab. Code §2872; failure makes assignment voidable for personal-time work.
- **83(b) not filed within 30 days.** Catastrophic for founders. See `equity-grants-isos-rsus-83b-election`.
- **No Schedule A pre-existing IP.** Founder may inadvertently assign personal projects. Always list.
- **Acceleration single trigger.** Investor pushback; market is double trigger. Negotiate for double; single is bonus.
- **Repurchase right at "fair market value" instead of cost.** Cost is market for unvested; FMV is only for vested under specific circumstances. Avoid FMV repurchase on unvested.
- **Acceleration definitions.** "Change of Control" + "Involuntary Termination" definitions matter. Cover asset sale + merger; cover "termination without cause" + "resignation for good reason."
- **Non-compete enforceability.** Void in CA, ND, OK, MN. See `non-compete-non-solicit-state-enforceability`. Use non-solicit + IP assignment + confidentiality as substitutes.
- **Spousal consent in community-property states.** CA, AZ, ID, LA, NV, NM, TX, WA, WI. Founder spouse must consent to restrictions on community-property shares.
- **Pre-incorporation IP.** IP created BEFORE company exists belongs to the founders personally; an explicit assignment to the company AT incorporation is required.
- **Bringing co-founders into existing startup.** Late additions need careful equity math. Common: add at current FMV (with 83(b)) — gets tax-free founder treatment if FMV is low.
- **Vesting credit at Series A refresh.** Investors may push for full re-vest; negotiate credit for time served.

> Warning: **This is informational guidance from an AI agent. Always consult a licensed attorney before signing or executing a Founders Agreement, IP assignment, or related binding equity or IP documents.**

## Sources

- [Cooley GO Founders Stock](https://www.cooleygo.com/documents/founders-stock/) — founders stock + vesting templates.
- [Cooley GO Founders Agreement](https://www.cooleygo.com/documents/founders-agreement/) — founders agreement template.
- [Cooley GO PIIA](https://www.cooleygo.com/documents/proprietary-information-and-inventions-agreement/) — PIIA template.
- [Stripe Atlas](https://stripe.com/atlas) — incorporation + founder bundle.
- [Clerky](https://www.clerky.com/) — cap table + incorporation.
- [Cal. Labor Code §2870-2872](https://leginfo.legislature.ca.gov/faces/codes_displayexpandedbranch.xhtml?tocCode=LAB&division=3.&title=&part=&chapter=2.&article=3.5.) — CA invention assignment + notice.
- [17 USC §101](https://www.law.cornell.edu/uscode/text/17/101) — work made for hire definition.
- [DDB Technologies v. MLB Advanced Media, 517 F.3d 1284 (Fed. Cir. 2008)](https://casetext.com/case/ddb-tech-v-mlb-advanced-media) — "hereby assigns" vs "agrees to assign."
- Sister skills: `equity-grants-isos-rsus-83b-election`, `safe-convertible-note-yc-template`, `term-sheet-review-series-a-typical-terms`, `non-compete-non-solicit-state-enforceability`, `contract-review-msa-nda-employment`.
