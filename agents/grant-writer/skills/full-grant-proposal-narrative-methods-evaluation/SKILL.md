---
name: full-grant-proposal-narrative-methods-evaluation
description: Author full federal / foundation / corporate grant proposals — 8 standard sections (executive summary, statement of need, project description, methods, evaluation, org capability, budget narrative, sustainability) with AI-assist via Grantable / GrantBoost / Instrumentl. Use when the user says "draft a proposal for <NOFO/funder>".
---

# Full grant proposal authoring

The 8-section standard structure scored by federal reviewers + most foundations. Reviewers score against the NOFO rubric; deviating from the NOFO outline costs points. AI-assist tools (Grantable, GrantBoost, FundRobin, Instrumentl) accelerate drafting but require human ground-truthing on outcomes, evidence base, and budget reconciliation.

## When to use

- User has a federal NOFO and needs a full proposal
- Foundation invited a full proposal after LOI acceptance
- User wants to convert an existing concept paper into a full proposal
- Multi-funder proposal where the same project is being pitched to several funders with section tweaks

Do NOT use this skill for:
- LOI / concept paper drafting (→ `loi-letter-of-inquiry-drafting`)
- Budget construction in isolation (→ `budget-narrative-justification`)
- Logic model construction in isolation (→ `logic-model-inputs-activities-outputs-outcomes`)
- Capital campaigns (→ `capital-campaign-capacity-equipment-grants`)

## Setup

```bash
# Optional AI-assist tools (recipient subscriptions)
# Grantable: https://grantable.co/ — $24/mo
# GrantBoost: https://grantboost.io/ — $19.99/mo Pro
# FundRobin: https://fundrobin.com/ — $29/mo
# Instrumentl writing assistant: bundled with $299/mo plan
export GRANTABLE_API_KEY="..."
```

Auth / API key requirements:
- Grantable / GrantBoost / Instrumentl — paid recipient subscriptions
- `firecrawl-mcp` API key — optional, scrape NOFO HTML when only PDF is published
- No keys for the writing itself

## Common recipes

### Recipe 1: Read the NOFO end-to-end + extract rubric

```bash
# Pull the NOFO PDF from Grants.gov
curl -X POST https://api.grants.gov/v1/api/fetchOpportunity \
  -d '{"opportunityId":"352421"}' | jq '.data.synopsisAttachments'

# Download attached PDF, extract text
pdftotext -layout nofo.pdf nofo.txt

# Find scoring rubric
grep -n -A 20 "scoring\|review criteria\|evaluation criteria" nofo.txt
```

The rubric drives section weight. If "Project Design" is 40 points, that section gets 40% of the page budget.

### Recipe 2: Map NOFO outline to your sections

```bash
# Build a section-by-section map
cat > section_map.md <<EOF
| NOFO section | Rubric weight | Pages allowed | Your file |
|---|---|---|---|
| Need | 15 pts | 3 | sections/01_need.md |
| Approach | 35 pts | 8 | sections/02_approach.md |
| Eval | 20 pts | 4 | sections/03_eval.md |
| Capability | 15 pts | 3 | sections/04_capability.md |
| Sustainability | 10 pts | 2 | sections/05_sustain.md |
| Budget narrative | 5 pts | 5 | sections/06_budget.md |
EOF
```

Mirror the NOFO outline EXACTLY. Reviewers grade against the rubric; deviation costs points.

### Recipe 3: Draft order (NOT executive-summary first)

```
1. Logic model FIRST (skill: logic-model-inputs-activities-outputs-outcomes)
2. Statement of Need (data + citation)
3. Project Description (goals → objectives → activities → timeline)
4. Methods (evidence base + how)
5. Evaluation Plan (linked to logic model)
6. Org Capability
7. Sustainability
8. Budget Narrative (skill: budget-narrative-justification)
9. Executive Summary (LAST — it's a summary, not an intro)
```

### Recipe 4: Statement of Need section

```markdown
## Statement of Need

### The problem
<Quantified problem with primary-source citation. Specific population. Geographic scope.>
"In Alameda County, 28.3% of children under 5 live in households below 200% FPL,
compared to 21.4% statewide (U.S. Census ACS 5-year 2019-2023)."

### Why current approaches fall short
<Gaps in existing services. Cite peer-reviewed evidence + sector reports.>

### Why now
<Time-sensitive urgency. New data, expiring funding, policy window.>

### Population most affected
<Demographic + geographic + access-barrier specifics.>
```

### Recipe 5: Project Description section

```markdown
## Project Description

**Goal:** <1 sentence — long-term aim>

**Objectives** (SMART — Specific, Measurable, Achievable, Relevant, Time-bound):
- Objective 1: By <date>, <X% of population> will <specific outcome>.
- Objective 2: <same shape>
- Objective 3: <same shape>

**Activities per objective:**
- For Objective 1:
  - Activity 1.1: <activity> — <quantity> — <by when>
  - Activity 1.2: ...

**Timeline (Gantt):**
| Activity | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| 1.1 | X | X | | |
| 1.2 | | X | X | X |

**Target population + outreach plan:**
<Who, how many, recruitment strategy.>

**Partnerships:**
<Subgrantees, evaluation partner, service-delivery partners — with MOUs attached.>
```

### Recipe 6: Methods section

```markdown
## Methods

### Evidence base for the approach
<Cite peer-reviewed studies + government evidence repositories.>
"Our approach builds on the CDC Community Preventive Services Task Force
recommendation for <intervention> (Strong Evidence, 2024)."

### Why this approach not alternatives
<Compare to alternative approaches and explain choice — federal reviewers expect this.>

### Implementation steps
<Specific milestones + decision points.>

### Roles
| Role | FTE | Responsibilities | Indirect supervisor |
|---|---|---|---|
| PI | 0.20 | Overall accountability + funder relations | ED |
| Project Manager | 1.0 | Day-to-day implementation | PI |
| Evaluator | 0.30 | Data collection + analysis | PI |
```

### Recipe 7: Evaluation Plan section

```markdown
## Evaluation Plan

### Linked to logic model
<Attach or reference logic model; outcomes here mirror logic-model outcomes column.>

### Indicators per outcome
| Outcome | Indicator | Data source | Schedule | Analysis | Target |
|---|---|---|---|---|---|
| Increased knowledge of X | % participants demonstrating skill X | Pre/post survey | T0, T+3mo, T+12mo | Paired t-test | 70% by EOY1 |

### Evaluation partner
<Name + institution + prior similar evaluations.>

### Sample size + power
<For research-oriented projects: power calc, alpha, effect size assumption.>

### Reporting cadence to funder
<Quarterly SF-425 + annual SF-PPR for federal; per funder schedule for foundation.>
```

### Recipe 8: Org Capability section

```markdown
## Organizational Capability

- **Years operating:** <X years since 501(c)(3) determination, <year>.>
- **Mission:** <one sentence>
- **501(c)(3) status:** verified per IRS EO Search, EIN <XX-XXXXXXX>
- **Prior grant history with similar funders:** <list 3-5 prior awards with $ + outcomes>
- **Key staff:**
  - <Name>, <Role>: <bio + relevant credential>
  - <Name>, <Role>: ...
- **Evaluation track record:** <prior evaluations, publications if applicable>
- **Financial health:**
  - Most recent audit: FY<year>, clean opinion, no material weaknesses
  - Operating reserves: <months of expenses>
  - Single Audit status (if applicable): <up to date / N/A>
```

### Recipe 9: Sustainability section

```markdown
## Sustainability

### Post-grant funding plan
| Year post-grant | Funder/source | Status | $ |
|---|---|---|---|
| Y1 | Foundation X | LOI submitted Q3 2026 | $50K |
| Y1 | Earned revenue (fee-for-service) | Pilot underway | $30K |
| Y2 | Foundation Y | Cultivation in progress | $75K |

### Capacity built that persists
<Staff training, infrastructure, partnerships, data systems that outlast the grant.>

### Partnerships that continue
<Which partnerships persist post-grant.>
```

### Recipe 10: Executive Summary (drafted LAST)

```markdown
## Executive Summary
(1 page — 250-400 words)

<Org name> requests $<amount> over <period> from <funder> to implement
<project name>, addressing <quantified problem> in <geography>.

The project will <2-sentence summary of approach>. Expected outcomes:
- <Outcome 1 with metric>
- <Outcome 2 with metric>
- <Outcome 3 with metric>

<Org> has <credibility line>. The project leverages <partnerships> and
<match/leverage>. Sustainability secured via <funding plan>.

We welcome your partnership.
```

### Recipe 11: AI-assist via Grantable

```bash
# Grantable supports persistent funder memory — paste the NOFO once, drafts persist
curl -H "Authorization: Bearer $GRANTABLE_API_KEY" \
  -X POST https://api.grantable.co/v1/projects \
  -d '{"name":"<Project>","funder":"<Funder>","nofo_text":"..."}'

# Then iterate per section
curl -H "Authorization: Bearer $GRANTABLE_API_KEY" \
  -X POST https://api.grantable.co/v1/projects/<id>/sections \
  -d '{"section":"need","prompt":"draft 800 words on..."}'
```

Always human-review AI output for: hallucinated citations, generic language, evidence-base accuracy, math errors.

### Recipe 12: Differential review before submission

```bash
# Reviewers: ED + Program Lead + Finance + outside reader
# Check against NOFO rubric, page limits, attachment list, signed forms
# Run differential-review skill or manual checklist
```

## Examples

### Example 1: Federal HRSA proposal — 12-section community health proposal

**Goal:** Draft a $750K, 3-year HRSA Maternal & Child Health proposal.

**Steps:**
1. Pull NOFO via `fetchOpportunity` API + extract scoring rubric (40 pts Approach, 25 pts Eval, 20 pts Need, 15 pts Capability).
2. Build section_map.md with page budget per section.
3. Draft logic model in `drawio-mcp` first (skill: `logic-model-inputs-activities-outputs-outcomes`).
4. Draft Need (3 pages) with CDC + MMWR + state health dept citations.
5. Draft Approach (8 pages) with HRSA evidence-base alignment.
6. Draft Evaluation (4 pages) linked to logic model; collaborate with university evaluation partner.
7. Draft Capability (3 pages) — prior HRSA awards, 501(c)(3) docs, audit status.
8. Draft Sustainability (2 pages) — diversified post-grant plan.
9. Build budget + budget narrative (skill: `budget-narrative-justification`).
10. Executive Summary (1 page) LAST.
11. Differential review with ED + PM + Finance.
12. Submit via Grants.gov Workspace (skill: `grants-gov-sam-gov-submission`).

**Result:** Complete proposal package + SF-424 family + signed attachments ready for AOR submission.

### Example 2: Foundation full proposal — Hewlett $200K

**Goal:** After LOI acceptance, draft 12-page full proposal to Hewlett Foundation.

**Steps:**
1. Pull Hewlett's "How to apply" page for full-proposal structure (varies by program area).
2. Mirror their priority phrasing throughout.
3. Draft sections in order: Need → Project → Methods → Eval → Capability → Sustainability → Budget Narrative → Exec Summary.
4. Use Grantable for first draft, human-revise for foundation-fit voice.
5. Attach: IRS determination letter, board roster, audited financials, key staff bios, letters of support, logic model.
6. Submit via Hewlett's Fluxx portal.

**Result:** Foundation proposal in Fluxx with all attachments + tracking confirmation.

## Edge cases / gotchas

- **NOFO outline trumps your preferred structure.** If the NOFO calls Section 4 "Evaluation Approach," don't title yours "Evaluation Plan."
- **Page limits are strictly enforced.** Federal reviewers will discard the over-limit pages. Count BEFORE drafting.
- **Citations must be primary-source.** Wikipedia, secondary news = decline. Use peer-reviewed journals, government data (Census, BLS, CDC), evidence clearinghouses (What Works Clearinghouse, CrimeSolutions.gov).
- **AI hallucination risk.** Grantable / GrantBoost / Instrumentl AI assists are helpful but can invent citations or stats. Ground-truth every quantified claim against a primary source.
- **Evidence base for federal:** Federal reviewers expect either Strong Evidence (RCT replicated), Moderate (quasi-experimental), or Promising (correlational) per ESSA tiers. State your tier and cite.
- **Match commitment:** If the NOFO requires match, the budget narrative must show it and matching letters must be attached. Missing match = ineligible.
- **Letters of support vs letters of commitment:** LOSupport is mission alignment; LOCommitment specifies $ or hours promised. Federal often requires commitment letters with specific dollar amounts.
- **Submission day buffer:** Submit 24-48 hours before deadline. Grants.gov has been known to slow under deadline-day load.
- **Disclaimer:** For binding interpretation of cost allowability or compliance questions, consult a qualified grants professional, nonprofit attorney, or CPA before submission.

## Sources

- CMS Budget Request + Narrative Guidance: https://www.cms.gov/about-cms/work-us/cms-grants/cooperative-agreements/how-apply-cms-grants/cms-guidance-preparing-budget-request-and-narrative
- Granted AI — best AI grant writing tools 2026: https://grantedai.com/blog/best-ai-grant-writing-tools-2026
- Grantable: https://grantable.co/
- GrantBoost: https://grantboost.io/
- Instrumentl writing assistant: https://www.instrumentl.com/
- Giddings Consulting — Grant Proposal Template: https://giddingsconsulting.com/blog/grant-proposal-template-nonprofit/
- Grants.gov forms repository: https://www.grants.gov/forms/forms-repository
- What Works Clearinghouse (federal evidence tiers): https://ies.ed.gov/ncee/wwc/
