---
name: indirect-cost-nicra
description: Choose between De Minimis 15% MTDC and a federally negotiated indirect cost rate (NICRA), compute MTDC base, and prepare a NICRA proposal. Use when the user says "what's our indirect rate?" / "do we have a NICRA?" / "calculate indirect" / "first federal grant — what indirect should I use?".
---

# Indirect cost rate + NICRA

Three options post-Oct 2024: (1) De Minimis 15% MTDC — no federal approval, indefinite use; (2) federally Negotiated Indirect Cost Rate Agreement (NICRA) — annual negotiation with cognizant agency; (3) cost allocation plan (less common). First-time grantees should almost always use De Minimis; switching to NICRA makes sense at scale (typically $1M+ federal expenditures or multi-agency awards).

Disclaimer: For binding determinations on indirect rate selection, NICRA cognizant agency assignment, or audit treatment of indirect costs, consult a qualified grants professional / CPA.

## When to use

- First-time federal grant — deciding rate strategy
- Org has NICRA but wondering if it's worth keeping
- NOFO has indirect cap that contradicts your NICRA
- Computing MTDC base correctly for a federal budget
- Drafting a NICRA proposal narrative
- Negotiating rate increase with cognizant agency
- Auditor questioning indirect classification

Do NOT use this skill for:
- Full budget narrative drafting → `budget-narrative-justification`
- Match strategy that uses unrecovered indirect → `matching-funds-in-kind-strategy`
- Single Audit indirect cost finding response → `single-audit-prep-federal-750k`
- General federal cost principles → `federal-grant-compliance-omb-uniform-guidance`

## Setup

```bash
# Reference (free, public)
# 2 CFR 200.414 (Indirect cost rates): https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-E
# 2 CFR 200 Appendix IV (Indirect cost rates for Nonprofits)
# 45 CFR 75 (NIH-specific reversion per NOT-OD-26-072)

# Cognizant agency contacts
# - HHS Program Support Center (PSC): https://psc.gov/Home/CostAllocationServices.html
# - DOI Interior Business Center (IBC): https://www.doi.gov/ibc/services/finance/indirect-cost-services
# - ED Office of Indirect Cost: https://www2.ed.gov/about/offices/list/ocfo/intind.html

# Tools: xlsx (rate calc + MTDC computation), docx (NICRA proposal narrative)
```

Auth / API key requirements: None for De Minimis. NICRA negotiation requires audited financials, organizational chart, and direct/indirect cost allocation methodology.

## Common recipes

### Recipe 1: Decision tree — De Minimis vs NICRA

```markdown
## Pick your indirect approach

Has your org ever had a federally negotiated rate?
├── YES → You must use the negotiated rate (cannot revert to De Minimis without surrender)
│         → Apply NICRA rate × MTDC
│
└── NO → Two options:
        ├── De Minimis 15% MTDC
        │   - Available to any non-federal entity that has never had a NICRA
        │   - No federal approval required
        │   - Can use indefinitely
        │   - Per 2 CFR 200.414(f) (raised from 10% to 15% Oct 2024)
        │
        └── Negotiate a NICRA
            - Worth the effort if federal portfolio ≥ $1M and/or your true indirect rate > 15%
            - Requires audited financials + cost allocation plan + proposal narrative
            - Annual renewal (provisional → predetermined → fixed → final)
            - Typically 6-12 months to negotiate initial rate
```

### Recipe 2: MTDC base computation (critical — auditors check this)

```markdown
## MTDC = Modified Total Direct Costs

MTDC = Total Direct Costs MINUS:
✗ Capital expenditures (equipment ≥ $10K per 2024 update; was $5K)
✗ Subaward portions over the first $25K (2024 update; was first $25K of EACH subaward)
✗ Participant support costs (e.g., scholarships, stipends, conference fees for participants)
✗ Pass-through funds to sub-recipients beyond first $25K
✗ Rental costs (rent / lease payments for facilities)
✗ Certain federal scholarships
✗ Tuition remission (if related to research training awards)
✗ Hospitalization charges

## Example MTDC calc
Total Direct Costs: $500K
- Equipment ($30K): -$30K
- Subaward $80K (first $25K stays in base): -$55K (the portion over $25K)
- Participant support stipends: -$15K
= MTDC: $400K

Indirect at 15% De Minimis: $400K × 15% = $60K
TOTAL Federal request: $500K direct + $60K indirect = $560K
```

### Recipe 3: De Minimis 15% — when to use

```markdown
## Use De Minimis IF:
✓ First-time federal grantee
✓ Federal portfolio < $1M
✓ True indirect costs roughly equal 15% or less
✓ Avoid administrative burden of annual NICRA negotiation
✓ Cognizant agency negotiation timeline (6-12 mo) exceeds urgency

## Don't use De Minimis IF:
✗ True indirect runs 25%+ (university orgs, research institutes) — leaving money on table
✗ Multi-state operations with complex cost pools — NICRA more accurate
✗ Already have NICRA (cannot revert)
```

### Recipe 4: NICRA cognizant agency assignment

```markdown
## Who negotiates your NICRA?

| Entity type | Cognizant agency |
|---|---|
| Most nonprofits ≥ $10M federal | HHS Program Support Center (PSC) |
| Most universities | ED Office of Indirect Cost Negotiation |
| Native American tribes | DOI Interior Business Center (IBC) Indirect Cost Services |
| States / local govts | DHHS Cost Allocation Services |
| Smaller nonprofits (≤$10M) | Whichever federal agency provides the largest share of funding |

## Default rule (2 CFR 200 Appendix IV)
"Cognizant agency for indirect costs" = the federal agency providing the LARGEST dollar value
of direct federal funding to the entity, unless otherwise assigned by OMB.
```

### Recipe 5: NICRA proposal contents

```markdown
## NICRA proposal package

| Component | What's included |
|---|---|
| Cover letter | Signed by org leader; rate type requested (provisional / predetermined / fixed) |
| Audited financial statements | Last 3 years |
| Indirect cost pool detail | G&A salaries, occupancy, IT, accounting, HR, executive — by line |
| Direct cost base detail | Salaries, fringe, travel, materials by program |
| Allocation methodology | How shared costs are split (sq ft, headcount, salary $) |
| Org chart | Showing direct-cost vs indirect-cost staff |
| Federal awards list | Current + recent awards with $ amounts |
| Rate calc worksheet | (Indirect pool ÷ direct base) × 100 = rate |
| Certification | Signed cost policy statement |
```

### Recipe 6: NICRA rate types

```markdown
## Rate types — which to request?

| Type | When used | Pros | Cons |
|---|---|---|---|
| Provisional | Initial year, awaiting final cost data | Get a working rate quickly | Subject to retroactive adjustment |
| Predetermined | Stable orgs, established cost history | Locked for 2-4 years | Bears the risk if costs change |
| Fixed with carry-forward | Mid-stability orgs | Year-to-year true-up | More accounting work |
| Final | After fiscal year close | True actuals | Cannot use prospectively |

Most first NICRAs are PROVISIONAL → converted to PREDETERMINED after 1-2 years.
```

### Recipe 7: NICRA submission timeline

```markdown
## Timeline (HHS PSC example)
- Month 1: Compile proposal package (Recipe 5)
- Month 2: Pre-submission consultation with PSC negotiator (free)
- Month 3: Submit complete proposal
- Months 3-6: PSC review + clarifying questions + on-site or virtual visit
- Months 6-9: Draft NICRA letter
- Months 9-12: Final NICRA letter signed by both parties
- Annually thereafter: Renewal proposal due 6 months before NICRA expiration
```

### Recipe 8: NICRA vs De Minimis math

```markdown
## When NICRA pays off — example

Org with $2M annual federal awards
True indirect costs ≈ 22% of direct

Scenario A: De Minimis 15% MTDC
- Direct $1.74M; MTDC ≈ $1.6M (after exclusions)
- Indirect recovered: 15% × $1.6M = $240K
- Underrecovery: ($1.6M × 22%) - $240K = $112K shortfall absorbed by org

Scenario B: NICRA at 22%
- Same direct $1.74M; MTDC $1.6M
- Indirect recovered: 22% × $1.6M = $352K
- Full recovery (no shortfall)
- Marginal value of NICRA: $112K/yr

Break-even on NICRA admin cost (~$30K/yr) at portfolio of ~$1.5M+
```

### Recipe 9: NIH 45 CFR 75 reversion

```markdown
## NIH FY2026 reversion (NOT-OD-26-072)
- NIH awards in FY2026 revert to 45 CFR Part 75 indirect cost provisions (vs 2 CFR 200)
- Practical impact:
  - NIH may publish a separate ceiling rate (historically ~10% on training awards)
  - De Minimis still available at NIH's discretion
  - Same MTDC base rules apply
  - NICRA holders apply their negotiated rate up to NIH ceiling (if any)
- Read 45 CFR 75.414 + NIH NoA before applying NICRA to NIH awards
```

### Recipe 10: NOFO indirect caps

```markdown
## When the NOFO restricts indirect

Common patterns:
- "Indirect capped at 10% of total direct" → use that, not your NICRA
- "Indirect must use de minimis OR NICRA, whichever is less" → compare both
- "Indirect not allowable for program funds" → 0% indirect; bake costs into direct
- "Training grant — indirect at 8% of direct (45 CFR 75)" → NIH-specific

## Action
- Read NOFO Indirect Cost section verbatim
- If NOFO < NICRA, use the cap (the difference can sometimes be claimed as match per `matching-funds-in-kind-strategy`)
- If NOFO requires "use de minimis", you must use 15% even if you have a NICRA
```

## Examples

### Example 1: First federal grant — choose De Minimis

**Goal:** Small nonprofit (~$500K total revenue) wins first federal grant ($150K, 1 year).

**Steps:**
1. Confirm: no prior NICRA → De Minimis available.
2. Compute MTDC: $150K total - $0 equipment - $0 subaward = $150K direct, MTDC = $150K (no exclusions apply).
3. Wait — that's wrong. If $150K is TOTAL request, work backwards:
   - Total = Direct + (15% × MTDC)
   - $150K = Direct + (0.15 × Direct) [if no MTDC exclusions]
   - Direct = $150K / 1.15 = $130,435
   - Indirect = $19,565
4. Document in budget narrative: "Indirect calculated at De Minimis 15% MTDC per 2 CFR 200.414(f) updated October 2024. Org has never held a NICRA."
5. Add to org policy: De Minimis is our standard until federal portfolio exceeds $1M.

**Result:** Compliant, simple, no NICRA admin burden.

### Example 2: Negotiate first NICRA at HHS PSC

**Goal:** Org grows to $2M federal portfolio; current De Minimis leaves $100K+/yr on the table.

**Steps:**
1. Pre-submission call with HHS PSC negotiator (free, schedule via psc.gov).
2. Compile 3 years audited financials + cost policy statement.
3. Categorize every cost: direct (project-specific) vs indirect (G&A, occupancy, exec, HR, IT).
4. Build allocation methodology (e.g., occupancy by sq ft; HR by FTE).
5. Compute proposed rate: indirect pool ÷ MTDC direct base = 22%.
6. Submit package per Recipe 5.
7. Provisional rate negotiated within 6-9 months.
8. After 2 years, request predetermined rate (multi-year stability).

**Result:** $100K+/yr additional indirect recovery; cost of NICRA admin ~$30K/yr; net +$70K/yr.

## Edge cases / gotchas

- **You cannot revert from NICRA to De Minimis.** Once you have a NICRA, you must apply it. Surrendering NICRA requires formal cognizant agency approval.
- **Subaward $25K rule changed Oct 2024.** Pre-Oct 2024: first $25K of EACH subaward in MTDC base. Post-Oct 2024: first $25K TOTAL across all subawards. Re-verify on every NOFO.
- **Equipment threshold raised to $10K Oct 2024.** Items $5K-$10K now go in MTDC base (were excluded).
- **Indirect on subawards.** Generally, sub-recipients get their own indirect (their NICRA or de minimis). Recipient's NICRA does NOT pass through to sub.
- **Training grants often have lower cap.** NIH F & T awards often cap indirect at 8%. Read NoA.
- **NIH cap rumor (Trump admin 2025).** Watch for executive action capping NIH indirect at 15% on new awards. As of 2026, status varies by court.
- **Foundation indirect.** Foundations vary: Gates allows 10-15%; Hewlett up to 20%; Ford up to 25%. Few foundations honor a NICRA.
- **State pass-through indirect.** States must honor your NICRA on federal pass-through funds per 2 CFR 200.414(c)(3).
- **Cost allocation plan vs NICRA.** Some orgs (especially states/locals) use a cost allocation plan instead. Outside scope here; route to specialist.
- **Cognizant agency change.** If your federal funding mix shifts (e.g., majority becomes ED instead of HHS), cognizant agency can be reassigned. Don't initiate without strategy call.
- **Disclaimer.** Indirect rate selection is a binding compliance decision affecting all federal awards. For first NICRA submission, switching agencies, or audit response, consult a qualified grants professional or CPA.

## Sources

- 2 CFR 200.414 (Indirect costs): https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-E
- 2 CFR 200 Appendix IV (Indirect Cost Identification + Assignment): https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/appendix-Appendix%20IV%20to%20Part%20200
- 45 CFR 75 (HHS indirect provisions, NIH reversion): https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-75
- NIH NOT-OD-26-072 (FY2026 indirect provisions): https://grants.nih.gov/grants/guide/notice-files/
- HHS Program Support Center (PSC): https://psc.gov/Home/CostAllocationServices.html
- DOI Interior Business Center: https://www.doi.gov/ibc/services/finance/indirect-cost-services
- ED Office of Indirect Cost Negotiation: https://www2.ed.gov/about/offices/list/ocfo/intind.html
- Clark Nuber De Minimis update explainer: https://clarknuber.com/articles/uniform-guidance-the-de-minimis-indirect-cost-rate-updated/
- Granted AI first-time NICRA guide: https://grantedai.com/blog/indirect-cost-rate-negotiation-first-time-grantees
