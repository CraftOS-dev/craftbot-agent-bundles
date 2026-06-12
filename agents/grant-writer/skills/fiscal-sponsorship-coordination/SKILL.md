---
name: fiscal-sponsorship-coordination
description: Pick a fiscal sponsor (Model A vs C vs F), negotiate the agreement, manage the pre-approved grant relationship, and plan an eventual spin-off. Use when the user says "we need a fiscal sponsor" / "find us a sponsor" / "review our sponsorship agreement" / "we want to become our own 501(c)(3)".
---

# Fiscal sponsorship coordination

A fiscal sponsorship lets a project receive tax-deductible donations + federal grants without forming its own 501(c)(3). Model A = sponsored project IS the sponsor's program (full liability + control). Model C = pre-approved grant relationship (most common; sponsor passes funds; project has separate governance). Model F = single-member LLC. Top US sponsors: NEO Philanthropy, Fractured Atlas (artists), Players Philanthropy Fund, Community Initiatives, Third Sector New England. Open Collective Foundation dissolved Dec 31, 2024.

Disclaimer: For binding decisions on model selection, agreement clauses, indemnification, or spin-off to independent 501(c)(3), consult a qualified nonprofit attorney.

## When to use

- Starting a new project that needs to raise tax-deductible $ but doesn't want to form a 501(c)(3) yet
- Existing project deciding between staying sponsored OR forming independent 501(c)(3)
- Negotiating fiscal sponsorship agreement (admin fee, termination, IP rights)
- Comparing sponsors (NEO vs Fractured Atlas vs Community Initiatives vs Players)
- Auditing current sponsorship to confirm Model C compliance
- Planning a spin-off from sponsor to independent 501(c)(3)
- Sponsor reviewing prospective new sponsored project

Do NOT use this skill for:
- Forming a 501(c)(3) from scratch → `legal-counsel` + IRS Form 1023 / 1023-EZ
- 501(c)(3) compliance docs (already independent) → `irs-501c3-compliance-docs`
- Foundation cultivation while under sponsorship → `foundation-cultivation-program-officer`
- Grant pipeline management for sponsored project → `multi-grant-pipeline-mgmt`

## Setup

```bash
# Tools: firecrawl-mcp (sponsor research), docx (agreement review), notion-mcp (sponsor comparison matrix)

# Free directories for sponsor research
# National Network of Fiscal Sponsors: https://www.fiscalsponsors.org/

# Reference
# IRS Pub 78 (verify sponsor's exempt status)
# https://apps.irs.gov/app/eos/
```

Auth / API key requirements: None for research. Agreement signing = legally binding; counsel-reviewed.

## Common recipes

### Recipe 1: Model decision tree

```markdown
## Which fiscal sponsorship model?

Goal of sponsored project:
├── Build long-term capacity; might eventually become 501(c)(3) → Model A or C
│   ├── Want sponsor to handle all legal + financial liability → Model A
│   └── Want project to have its own governance + spin off later → Model C
│
├── Short-term project (event, time-bounded campaign) → Model C
├── Single-member LLC structure preferred → Model F (uncommon)
└── Project that crosses int'l borders → Specialty sponsor (NEO Philanthropy, etc.)

## Most common in 2026: Model C (~80%+ of sponsorships)
```

### Recipe 2: Model A vs C vs F comparison

```markdown
## Side-by-side

| Dimension | Model A (Comprehensive) | Model C (Pre-Approved Grant) | Model F (Single-Member LLC) |
|---|---|---|---|
| Project status | IS the sponsor's program | Separate identity; sponsor regrants | Sponsor's LLC |
| Project governance | Sponsor's board (sometimes advisory committee) | Project has its own steering committee | Sponsor controls LLC |
| Employee status | Sponsor's employees | Sponsor's employees (most common) or project's contractors | Sponsor's employees |
| Donations flow | Donor → Sponsor → Project program | Donor → Sponsor → Regrant to project | Donor → Sponsor → LLC |
| Legal liability | 100% sponsor | Shared; sponsor for funds; project for activity | Sponsor (LLC veil) |
| Spin-off pathway | Hard (sponsor "owns" the program) | Easier (sponsor regrants assets at exit) | Moderate |
| Admin fee | 7-12% | 5-10% | 7-9% |
| Best for | Programs sponsor wants to operate long-term | Short-to-medium term projects with own identity | Single-purpose LLC |
| Examples | Tides historic sponsorships | Fractured Atlas, Players Phil Fund | Less common |
```

### Recipe 3: Top US fiscal sponsors (2026 landscape)

```markdown
## Sponsor directory (sample)

| Sponsor | Specialty | Admin fee | Model | Project size |
|---|---|---|---|---|
| NEO Philanthropy | Social justice, advocacy, gender, racial equity | 6-8% | Model A/C | Mid-large; $250K-$10M projects |
| Fractured Atlas | Artists + creators | 7% (waived for first $5K/yr) | Model C | Any size |
| Players Philanthropy Fund | Athletes + sports orgs | 5% | Model C | Any size |
| Community Initiatives | Multi-purpose (Bay Area strong) | 7-9% | Model A/C | Mid-large |
| Third Sector New England | New England multi-purpose | 7% | Model A/C | Any size |
| NCRP | Multi-purpose national | Varies | Model C | Advocacy-leaning |
| Common Counsel Foundation | Progressive multi-purpose coastal | 6-9% | Model A/C | Any size |
| Tides Foundation | Established programs (selective) | 8-10% | Model A historically | Large |
| Equity Trust Inc. | Land + housing justice | 6-8% | Model C | Specialty |
| Allied Media Projects | Media + tech justice | 9% | Model C | Detroit-anchored |

## Open Collective Foundation
DISSOLVED Dec 31, 2024 — no longer an option. Existing sponsored projects had to migrate.

## Verify sponsor 501(c)(3)
Always run sponsor through IRS EO Search before signing.
```

### Recipe 4: Admin fee + cost benchmark

```markdown
## What admin fee covers (Model C typical)

Included in fee:
- 501(c)(3) status use for solicitation
- Donor acknowledgment letters (IRS-compliant)
- Bookkeeping + monthly financial reports to project
- Audit (if sponsor's Single Audit covers project)
- Form 990 filing (project as program of sponsor)
- 1099 issuance to project contractors
- Limited HR support (Model A more; Model C less)

NOT included (often charged separately):
- HR + payroll for project employees (Model A: yes; Model C: project hires own)
- Grant management software access
- Legal review of project contracts (route through `legal-counsel`)
- D&O insurance for project advisory committee
- Specialty insurance (event, professional liability)

## Benchmark
5-8% Model C is reasonable for established projects
8-12% Model A reflects higher sponsor liability + service load
< 5% suspicious — sponsor likely under-pricing services
> 15% high — negotiate or shop alternative
```

### Recipe 5: Fiscal sponsorship agreement key terms

```markdown
## Sponsorship agreement clauses (Model C)

1. **Term + termination** — typical 1-3 yr renewable; termination with 60-90 day notice
2. **Admin fee structure** — % of gross receipts vs % of net expenses; floor / cap
3. **Decision-making authority** — sponsor approves: budget, hires above threshold, contracts above threshold; project advisory cmte recommends
4. **Use of sponsor's tax-exempt status** — only for project; not personal/unrelated activities
5. **Bank accounts** — sponsor holds all funds; project authorized signers on debit card or expense reimbursement
6. **Grant agreements** — sponsor is grantee of record; project is sub-recipient OR program
7. **Reporting** — sponsor provides monthly financials to project; project provides programmatic + impact data to sponsor
8. **Indemnification + insurance** — typically mutual; project carries GL + PL insurance for activities
9. **Intellectual property** — clarify ownership at term + at exit
10. **Name + brand rights** — project's brand stays with project at exit; logo / domain transfer at exit
11. **Exit clause** — project becomes independent 501(c)(3): assets transfer; staff offered transition; brand transfers; cash balance transfers per agreement
12. **Audit + records** — sponsor right of access; project right of inspection
13. **Dispute resolution** — typically mediation → arbitration; governing law of sponsor's state
14. **Restricted vs unrestricted gifts** — donor intent honored; project influence over allocation
15. **Sponsor's liability cap** — sometimes capped at admin fees collected
16. **Project's compliance obligations** — flow down 2 CFR 200 if federal funds; per-funder requirements

Route binding agreement review through `legal-counsel`.
```

### Recipe 6: Sponsor due diligence checklist (before signing)

```markdown
## Pre-signing checklist

| Check | How |
|---|---|
| Sponsor's 501(c)(3) active | IRS EO Search at apps.irs.gov/app/eos/ |
| Last 3 years Form 990 clean | ProPublica Nonprofit Explorer |
| Single Audit clean | Federal Audit Clearinghouse (fac.gov) |
| Sponsor's reputation | Council of Nonprofits + sector peer references |
| Financial health | Months of operating reserves (target ≥6 mo) |
| Sponsor's other sponsored projects | Count + types + retention (high turnover = red flag) |
| Sponsor staff capacity | Bookkeeping turnaround time; grant compliance experience |
| Sponsor's grant compliance track record | Federal grant experience if you'll have federal funds |
| Exit clause clear | Spin-off pathway documented |
| Admin fee market-competitive | Compare 3+ sponsors |

## Red flags
- Vague exit clause
- High project turnover (projects leaving)
- Recent IRS issues / Form 990 late
- Sponsor's own funder concentration > 50% (single-funder risk)
- Mismatched mission (e.g., arts sponsor for environmental project)
- Slow financial reporting (>30 days for month-end)
- Inflexible on agreement clauses
```

### Recipe 7: Sponsor comparison matrix

```markdown
## Build in Notion (Funders DB-style)

| Sponsor | Model offered | Admin fee | Min commitment | Federal grant exp | Specialty fit | Retention | Reference 1 | Reference 2 | Notes |
|---|---|---|---|---|---|---|---|---|---|
| NEO Phil | C | 6-8% | 1 yr | Strong | Advocacy | 90% | <peer> | <peer> | Great PO relationships |
| Fractured Atlas | C | 7% | None | Limited | Arts/creators | 85% | <peer> | <peer> | Best for artists |
| Community Initiatives | C | 8% | 1 yr | Strong | Bay Area | 88% | <peer> | <peer> | Operations-heavy |

Score 1-10 per row; weighted total drives selection.
```

### Recipe 8: Spin-off to independent 501(c)(3)

```markdown
## Spin-off timeline (12-18 months)

| Month | Milestone |
|---|---|
| 1 | Decision: confirm spin-off with steering committee + sponsor |
| 2-3 | Incorporate as 501(c)(3) (state Articles + bylaws) — route through `legal-counsel` |
| 4-6 | IRS Form 1023 or 1023-EZ submission |
| 6-12 | IRS determination letter (typically 6-12 months) |
| 12 | Establish own bank accounts + 990-N or 990 fiscal year |
| 12-14 | Transfer assets per sponsorship agreement |
| 14-16 | Migrate staff (offer letters from new entity) |
| 14-16 | Transition donors + funders (re-papered grant agreements) |
| 16-18 | Sponsor wind-down + final accounting |
```

### Recipe 9: Federal grants while under sponsorship

```markdown
## Federal grant flow (Model C)

1. Sponsor is the legal grant recipient (their EIN, UEI, SAM.gov registration)
2. Sponsor signs SF-424 as AOR
3. Sponsor sub-awards to project per 2 CFR 200.331 (→ `sf-424-sf-lll-subaward`)
4. Sponsor provides monthly financials, files SF-425, SF-PPR
5. Project executes programmatic work
6. Sponsor's Single Audit covers project's federal expenditures
7. At exit, federal grants typically novated to project's new 501(c)(3) (federal agency approval required)

## Risk
Federal agency may decline novation; project may need to wait until new grant cycle.
```

### Recipe 10: Annual sponsorship review

```markdown
## Annual check (project's side)

| Question | Why ask |
|---|---|
| Are admin fees still market-competitive? | Sponsor switching analysis |
| Is the relationship serving project's mission? | Strategic fit |
| Is sponsor's financial reporting timely? | Operational health |
| Is exit pathway still viable? | Long-term planning |
| Are restricted funds tracked correctly? | Audit readiness |
| Is project's brand identity protected? | IP / marketing |
| Are grant compliance requirements met? | Audit readiness |

If 3+ "no" answers → start sponsor comparison (Recipe 7).
```

## Examples

### Example 1: New climate-justice project picks Model C with NEO Philanthropy

**Goal:** Project wants to launch in 90 days, raise tax-deductible funds, eventually become own 501(c)(3) in 3-5 years.

**Steps:**
1. Recipe 1 decision tree: Model C (own governance, eventual spin-off, short-medium term).
2. Recipe 3: shortlist NEO Phil, Common Counsel, Allied Media (mission fit).
3. Recipe 7: comparison matrix — NEO scores highest on advocacy expertise.
4. Recipe 6: due diligence — NEO's IRS status active, 990 clean, audit clean.
5. Recipe 5: agreement negotiation — admin fee 7% (negotiated down from 8%); exit clause clear.
6. `legal-counsel` reviews agreement; project signs.
7. Launch project under NEO's 501(c)(3); fundraise.

**Result:** Launched in 90 days; tax-deductible donations flowing; spin-off pathway documented for 2029.

### Example 2: Arts project spins off from Fractured Atlas to own 501(c)(3) after 4 years

**Goal:** Mature arts project ($800K annual budget) ready to be independent.

**Steps:**
1. Steering committee + Fractured Atlas confirm spin-off intent.
2. Recipe 8 timeline started: incorporate Delaware non-stock; bylaws drafted.
3. IRS Form 1023 submitted (Month 4); determination letter received Month 10.
4. Bank accounts opened in new entity name.
5. Asset transfer per agreement: cash ($120K reserve), donor pledges, contracts.
6. Staff offered new entity letters (no break in employment).
7. Donors + funders re-papered grant agreements.
8. Fractured Atlas final accounting + wind-down Month 16-18.

**Result:** Independent 501(c)(3) operating with continuity; no donor loss.

## Edge cases / gotchas

- **Open Collective Foundation dissolved Dec 31, 2024.** If a user references OCF, they need to migrate; not a current option.
- **501(c)(3) sponsor vs (c)(4) sponsor.** Model C with a (c)(4) sponsor doesn't yield tax-deductible donations. Always confirm sponsor is (c)(3).
- **International project + US donations.** Sponsor must have US 501(c)(3) status; activities can be international but require equivalency determination per IRS Rev. Proc. 92-94.
- **Sponsor's Single Audit.** Project's federal expenditures roll up to sponsor's Single Audit. Sponsor must do Single Audit if cumulative ≥ $1M.
- **Restricted donations to project.** Donors give to sponsor restricted to project. Sponsor honor donor intent per state charitable solicitation law.
- **Sponsor's variance power.** Most sponsors retain "variance power" — right to redirect funds if project mission drift; rarely invoked but in agreement.
- **Sponsor's name on grant.** Funder grant is to sponsor; project name in narrative. Some funders restrict; check before submitting.
- **State charitable solicitation registration.** Sponsor's registration covers most states; project may need additional registration for direct mail / online fundraising.
- **Insurance.** Project should carry own GL + PL + cyber + D&O even under sponsorship. Sponsor's insurance is for sponsor, not project.
- **Brand at exit.** Negotiate brand transfer up front in agreement. Some sponsors retain brand rights; deal-breaker for project.
- **Cash on hand at exit.** Most agreements: project's restricted funds + unspent unrestricted transfer to project's new entity (less admin fees per agreement).
- **Disclaimer.** Binding decisions on model selection, agreement clauses, IP, indemnification, or spin-off mechanics must be reviewed by a qualified nonprofit attorney.

## Sources

- National Network of Fiscal Sponsors: https://www.fiscalsponsors.org/
- Council of Nonprofits — Fiscal Sponsorship: https://www.councilofnonprofits.org/running-nonprofit/administration-and-financial-management/fiscal-sponsorship-nonprofits
- 501c3.org — Fiscal Sponsorship: https://www.501c3.org/what-is-a-fiscal-sponsor/
- JoinIt — Fiscal Sponsorship Organizations: https://joinit.com/blog/fiscal-sponsorship-organizations
- NEO Philanthropy: https://neophilanthropy.org/
- Fractured Atlas: https://fracturedatlas.org/
- Players Philanthropy Fund: https://playersphilanthropy.com/
- Community Initiatives: https://www.communityinitiatives.org/
- Third Sector New England: https://www.tsne.org/
- Tides Foundation: https://www.tides.org/
- IRS Form 1023 / 1023-EZ guide: https://www.irs.gov/charities-non-profits/charitable-organizations/application-for-recognition-of-exemption
- IRS Rev. Proc. 92-94 (international equivalency): https://www.irs.gov/charities-non-profits/private-foundations/private-foundation-grants-to-foreign-organizations
