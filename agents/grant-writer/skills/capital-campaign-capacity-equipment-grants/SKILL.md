---
name: capital-campaign-capacity-equipment-grants
description: Write proposals for capital campaigns (building / endowment), capacity-building grants (org infrastructure), and equipment grants — distinct from program grants in case-for-support, timeline, and feasibility study expectations. Use when the user says "capital campaign" / "capacity-building" / "endowment" / "equipment grant" / "case for support".
---

# Capital campaign + capacity-building + equipment grants

These grants fund the org's foundation, not its programs. Capital = building, renovation, endowment, equipment > $50K. Capacity-building = technology, leadership development, evaluation systems, fundraising infrastructure. Equipment = single-purpose major purchase. Each has a different proposal structure than the standard program grant: case-for-support over need statement; feasibility study over evaluation plan; sustainability through quiet/public phasing.

## When to use

- Capital campaign for a new building, renovation, or endowment
- Capacity-building proposal (technology, leadership, evaluation, fundraising systems)
- Single equipment grant > $10K (vehicle, server, lab equipment, kitchen build-out)
- Feasibility study for a capital campaign
- Naming-rights / major-gift component of a capital campaign
- Capacity grants from Kresge / Hewlett / Packard / Ford / RWJF
- Multi-year endowment-building proposal

Do NOT use this skill for:
- Standard program grant proposal → `full-grant-proposal-narrative-methods-evaluation`
- Operating support proposal → `full-grant-proposal-narrative-methods-evaluation`
- Logic model for a program → `logic-model-inputs-activities-outputs-outcomes`
- Foundation cultivation cycle → `foundation-cultivation-program-officer`

## Setup

```bash
# Tools: docx (case for support), xlsx (capital budget + pledge tracker), firecrawl-mcp (feasibility study research), notion-mcp (campaign tracker)

# Free reference
# Council of Nonprofits — Capital Campaigns: https://www.councilofnonprofits.org/running-nonprofit/fundraising-and-resource-development/capital-campaigns
# Kresge capacity-building grants: https://kresge.org/our-work/capacity-building/
# Hewlett Strategy: https://hewlett.org/strategy/

# Software (for campaign tracking)
# - DonorPerfect / Bloomerang / Salesforce NPSP for pledge tracking
# - Bonterra for integrated CSR + capital
# - Network for Good (now Bonterra) for small-org campaigns
```

Auth / API key requirements: None for proposal drafting. CRM API key (Salesforce, Bloomerang, DonorPerfect) for pledge tracking.

## Common recipes

### Recipe 1: Identify the grant type

```markdown
## Capital vs capacity vs equipment

| Type | What it funds | Typical size | Funders | Timeline |
|---|---|---|---|---|
| Capital (building) | New construction, renovation | $500K - $50M+ | Capital-grant foundations + major individual donors + bonds | 2-5 yr quiet phase + 1-2 yr public |
| Capital (endowment) | Permanent corpus generating yield for ops | $500K - $50M+ | Endowment-only foundations + major donors | 3-7 yr quiet phase |
| Capacity-building | Org infrastructure (tech, leadership, eval, fundraising) | $25K - $500K | Kresge, Hewlett, Packard, Ford, RWJF, Bloomberg, Knight | 1-3 yr |
| Equipment | Single major purchase (vehicle, server, kitchen) | $10K - $250K | Local foundations, civic clubs (Rotary, Kiwanis), corp giving | 6-18 mo |
| Program-related | Program execution costs | Varies | Most funders | Standard cycle |

## Combined proposals
A new building can include capacity-building (e.g., FF&E + tech infrastructure + staff training).
Frame each component clearly.
```

### Recipe 2: Capital campaign structure (4 phases)

```markdown
## Capital campaign phases

| Phase | Goal | Activities |
|---|---|---|
| Phase 1: Planning + Feasibility | Confirm campaign viability | Feasibility study, case for support v1, board commitment |
| Phase 2: Quiet phase | Raise 40-60% of goal before public announcement | Major donor cultivation, naming-rights asks, lead gifts |
| Phase 3: Public phase | Broad community fundraising | Public launch, donor events, broad outreach |
| Phase 4: Stewardship + recognition | Donor recognition + sustain pledges | Recognition events, plaque dedication, pledge collection |

## Rule of thirds (classic)
- 1/3 of goal from top 10 donors
- 1/3 from next 100 donors
- 1/3 from remaining community

## Quiet phase rule
Public launch only after 50-60% raised. Public launch with <40% raised = high failure risk.
```

### Recipe 3: Feasibility study (before campaign launch)

```markdown
## Feasibility study scope (typically external consultant)

| Component | Method |
|---|---|
| Donor capacity assessment | Survey + interview 30-50 prospective major donors |
| Case for support test | Draft case → focus group → refine |
| Goal range recommendation | Triangulated from donor capacity + community baseline |
| Leadership readiness | Board interviews; executive readiness |
| Org readiness | Financial health, staff capacity, infrastructure |
| Competitive landscape | Other capital campaigns in market |
| Recommendation | Go / Wait / Modify scope |

## Cost
$25K-$100K typical for nonprofit feasibility study from external consultant.

## Self-conducted feasibility (smaller orgs)
- Limit to confidential interviews with 15-20 top prospects
- Case for support draft v1 tested with board + 3 peers
- Honest "would you give" question
- Output: goal range + readiness assessment
```

### Recipe 4: Case for support (the central document)

```markdown
## Case for support — 8-15 pages

| Section | Length | Purpose |
|---|---|---|
| Cover + executive summary | 1 pg | Hook donors |
| Vision + mission tie-in | 1 pg | Why this campaign matters |
| Why now (urgency) | 1 pg | Market timing |
| What we'll build | 2-4 pg | Project specifics + visuals (renderings, floor plans) |
| Impact projection | 1-2 pg | Beneficiaries + outcomes + community impact |
| Org credibility | 1 pg | Track record, leadership, financial health |
| Budget | 1 pg | Campaign budget + naming opportunities + recognition tiers |
| Naming opportunities | 1 pg | $100K → conference room; $1M → wing; $10M → building |
| Timeline | 1 pg | Phasing, milestones, completion |
| How to give | 1 pg | Cash, pledge, stock, planned gift, IRA QCD, real estate |
| Thank you + next steps | 0.5 pg | Donor recognition + lead gifts |

## Tone
Aspirational + concrete. Numbers + photos + testimonials.
```

### Recipe 5: Naming opportunities + recognition tiers

```markdown
## Naming-rights structure

| Gift level | Naming opportunity | Example |
|---|---|---|
| $5K | Donor wall plaque | Permanent recognition |
| $25K | Office / classroom name | "John Smith Office" |
| $100K | Conference room / lab | "Smith Family Conference Room" |
| $250K | Wing / floor | "Smith Wing" |
| $500K | Major program area | "Smith Center for Excellence" |
| $1M+ | Major building element | "Smith Atrium" |
| $5M+ | Wing / building | "Smith Pavilion" |
| $10M+ | Whole building / campus | "Smith Hall" |

## Pricing principle
Naming-rights pricing = 25-40% of construction cost of named element.
Premium for visibility + permanence.

## Term
- Lifetime / permanent (most desirable, highest price)
- 10-year term (lower price, allows future opportunity)
- Until renovation (medium)

## Reversion rights
- What happens at building demolition / sale
- Donor recognition transfers to replacement structure
- Documented in gift agreement (route through `legal-counsel`)
```

### Recipe 6: Capacity-building proposal (vs program proposal)

```markdown
## Capacity-building proposal structure

| Section | Capacity-building focus |
|---|---|
| Statement of need | Org's capacity gap (not community problem) |
| Goal | Org's capacity outcome (e.g., "increase fundraising capacity by 40%") |
| Activities | Infrastructure investments (tech, training, systems) |
| Methods | How capacity gets built (consulting, training, software) |
| Evaluation | Org capacity metrics + program impact downstream |
| Sustainability | How capacity persists post-grant (org budget absorbs operating) |

## Capacity-building funders' theory of change
"If we invest in org infrastructure, programs become more effective."

## Common capacity-building grant priorities (2026)
- Technology + data systems (CRM, evaluation, fundraising platforms)
- Leadership development (executive coaching, succession planning)
- Evaluation + outcomes measurement infrastructure
- Strategic planning
- DEI infrastructure
- Diversification of revenue streams
- Board governance training
```

### Recipe 7: Equipment grant proposal

```markdown
## Equipment grant structure (1-2 pages + appendix)

1. Equipment description + purpose (3 sentences)
2. Program need it addresses + scale ("serves 500 clients/yr")
3. Equipment specifications + total cost (include 15% contingency)
4. Vendor quotes (3 if possible — required for federal)
5. Alternatives considered + why this is best (cost-benefit)
6. Maintenance plan + sustainability (who maintains; what's the lifetime cost)
7. Cost + match
8. Recognition / acknowledgment

## Total cost example
| Item | $ |
|---|---|
| Equipment purchase | $20,000 |
| Installation | $2,000 |
| Training (first staff) | $1,500 |
| Contingency (15%) | $3,525 |
| Total | $27,025 |

## Maintenance + sustainability is often the deciding factor
Funders worry about $50K equipment becoming $0 after 3 years for lack of maintenance plan.
Document the plan: who, how often, funded from where.
```

### Recipe 8: Capital budget detail

```markdown
## Capital budget structure (detailed)

| Category | Detail | $ |
|---|---|---|
| Acquisition (land / building) | If applicable | $X |
| Hard construction costs | GC contract, subs, materials | $X |
| Soft costs | Architecture, permits, legal, engineering | $X (typically 15-25% of hard) |
| FF&E (furniture, fixtures, equipment) | Tech, furniture, AV, kitchen, etc. | $X |
| Contingency | 10-15% hard + soft | $X |
| Campaign costs | Feasibility, consultant, materials, events | $X (typically 3-5% of goal) |
| Total project | Sum | $X |

## Campaign goal includes campaign costs
A $5M campaign nets $4.75M for project; $250K covers feasibility + consulting + materials.
```

### Recipe 9: Pledge tracking + collection

```markdown
## Pledge management (CRM-backed)

| Field | Detail |
|---|---|
| Donor name + EIN if org | |
| Pledge amount | |
| Pledge date | |
| Payment schedule | Lump sum / annual / multi-year |
| Payment received to date | |
| Balance outstanding | |
| Naming-rights designation | |
| Recognition level | |
| Soft credit (e.g., DAF advisor) | |
| Pledge agreement | Signed PDF link |
| Status | Active / Paid in full / Defaulted |
| Last steward touch | Date + activity |

## Stewardship rule
Multi-year pledge donors require quarterly touches minimum to keep pledge cycle active.
Pledge default risk rises after 6+ months of silence.
```

### Recipe 10: Major capacity-building funders (2026)

```markdown
## Top capacity-building funders

| Funder | Focus | Typical size |
|---|---|---|
| Kresge Foundation | Capacity-building for justice, equity | $50K-$500K |
| Hewlett Foundation | Org effectiveness, philanthropy field-building | $100K-$1M |
| David & Lucile Packard Foundation | Org effectiveness + Population, Conservation | $50K-$500K |
| Ford Foundation | BUILD Initiative for racial justice orgs | $1M-$10M (multi-year) |
| Robert Wood Johnson Foundation | Health equity capacity | $50K-$500K |
| Bloomberg Philanthropies | Government innovation + capacity | $50K-$1M |
| Knight Foundation | Local journalism, civic engagement capacity | $50K-$500K |
| Walton Family Foundation | Education capacity | $50K-$500K |
| MacArthur Foundation | Building Power program | $250K-$2M |
| Surdna Foundation | Org strengthening for racial justice | $50K-$200K |
```

## Examples

### Example 1: $3M capital campaign for a new community center

**Goal:** Raise $3M for new building over 24 months.

**Steps:**
1. Recipe 3: feasibility study via consultant ($50K); confirms goal achievable.
2. Recipe 4: case for support drafted + tested with top 10 prospects.
3. Recipe 5: naming rights priced: $1M = building wing; $500K = main hall; $100K = classrooms.
4. Recipe 8: capital budget = $2.5M hard + $375K soft + $250K FF&E + $125K contingency + $125K campaign costs = $3.375M (campaign goal $3M with bridge financing for remainder).
5. Phase 2 quiet phase: board commits $750K; cultivate top 10 donors → $1.5M secured ($2.25M total = 75% of goal).
6. Public launch with $2.25M / $3M (75%) committed.
7. Phase 3 public phase: events, broad community → $750K additional.
8. Recipe 9: pledge tracker in DonorPerfect; monthly review.
9. Phase 4: recognition event, plaque dedication.

**Result:** $3M+ raised; building opens; permanent naming recognition installed.

### Example 2: $150K capacity-building grant from Kresge for evaluation infrastructure

**Goal:** Build org-wide outcomes evaluation system.

**Steps:**
1. Recipe 6: proposal frames CAPACITY gap (no consistent outcomes data) not program need.
2. Logic model: input = grant + staff time → activity = build eval system → output = data tool + trained staff → outcome = 100% programs reporting consistent outcomes.
3. Budget: $80K consulting for eval system design; $40K data platform (Sopact); $20K staff training; $10K eval librarian (PT, 1 yr).
4. Sustainability: Year 2 = absorbed into org operating budget at $30K/yr.
5. Application via Kresge online portal.
6. Decision Q3.

**Result:** Capacity-building proposal funded; evaluation system live in 12 months; downstream programs more competitive for future grants.

## Edge cases / gotchas

- **Capital vs capacity confusion.** A new building IS capital, but the IT system inside might be capacity. Frame each line accurately.
- **Endowment grants are rare.** Most foundations don't fund endowments. Cultivate over years; endowment-friendly foundations: Mott, Lilly, Templeton.
- **Naming-rights term must be agreed.** Lifetime vs term-limited matters at building renovation / sale. Document with `legal-counsel`.
- **Pledge default risk.** 10-20% of pledge dollars typically default. Plan accordingly; don't spend pledged $ that isn't received.
- **Federal capital grants are rare.** Most federal capital is HUD CDBG, EDA, USDA Rural Development. Different rules + Davis-Bacon wages apply.
- **Capacity-building proposals can't double as program proposals.** Funders specifically fund capacity; program proposals get rejected at portfolio level.
- **Feasibility study is the gate to a campaign.** Don't skip; campaigns that skip feasibility have higher failure rates.
- **Quiet phase below 40% = high failure risk.** Wait until you've secured 50-60% quietly before public launch.
- **Equipment grants need maintenance plan.** Without it, funders frame the grant as "buying equipment that becomes scrap" — declined.
- **Match for federal capital.** Often required at 20-50%; bonds + state matches common. Plan months ahead.
- **State charitable solicitation.** Multi-state capital campaign may trigger registration in multiple states; route through `legal-counsel`.
- **Donor recognition placement permanence.** Bronze plaques outlive buildings; document plans for re-installation at renovation / move.

## Sources

- Council of Nonprofits — Capital Campaigns: https://www.councilofnonprofits.org/running-nonprofit/fundraising-and-resource-development/capital-campaigns
- Kresge — Capacity-building: https://kresge.org/our-work/capacity-building/
- Hewlett Foundation — Strategy: https://hewlett.org/strategy/
- Packard Foundation — Organizational Effectiveness: https://www.packard.org/what-we-fund/organizational-effectiveness/
- Ford Foundation BUILD Initiative: https://www.fordfoundation.org/work/our-grants/build/
- AFP Bookstore — Capital Campaigns: https://afpglobal.org/AFP%20Bookstore/CapitalCampaign
- Strategic Resource Group capital campaign guide: https://strategicresourcegroup.com/capital-campaign-feasibility-study/
- Forbes Nonprofit Council on capacity-building: https://www.forbes.com/sites/forbesnonprofitcouncil/
- BoardSource capital campaigns: https://boardsource.org/resources/capital-campaigns/
