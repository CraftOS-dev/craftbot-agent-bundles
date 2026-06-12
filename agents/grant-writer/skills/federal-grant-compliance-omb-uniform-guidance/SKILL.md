---
name: federal-grant-compliance-omb-uniform-guidance
description: Navigate federal grant compliance — 2 CFR 200 Subparts A-F (OMB Uniform Guidance) + October 2024 update + May 29 2026 OMB proposed rewrite + NIH 45 CFR 75 reversion (NOT-OD-26-072). Use when the user says "are we compliant with 2 CFR 200" / "OMB Uniform Guidance question" / "what changed in 2024/2026".
---

# Federal grant compliance — 2 CFR 200 OMB Uniform Guidance

The governing federal framework for most discretionary grants. Subparts A-F cover definitions through audit. October 2024 update raised key thresholds; May 29 2026 OMB proposed rewrite under public comment (comment by July 13 2026; effective Oct 1, 2026). NIH reverts to 45 CFR 75 per NOT-OD-26-072 starting FY2026.

Disclaimer: For binding compliance interpretation, allowability rulings, audit risk assessment, or sub-recipient determinations, consult a qualified grants professional, nonprofit attorney, or CPA. This skill provides reference and starting points only.

## When to use

- New federal award — establish compliance baseline at award acceptance
- Audit prep or response to audit finding
- Cost allowability questions (can we charge X to this grant?)
- Sub-recipient vs contractor classification
- Indirect cost methodology selection
- Cross-walking pre-Oct 2024 vs post-Oct 2024 award rules
- Tracking the May 29 2026 OMB rewrite impact

Do NOT use this skill for:
- SF-424 form filling (→ `sf-424-sf-lll-subaward`)
- Indirect rate negotiation (→ `indirect-cost-nicra`)
- Single Audit prep (→ `single-audit-prep-federal-750k`)
- Budget construction (→ `budget-narrative-justification`)

## Setup

```bash
# Free
# eCFR live API for regulation queries
curl https://www.ecfr.gov/api/...

# firecrawl-mcp for OMB blog posts + agency interpretive guidance
```

Auth / API key requirements: None. eCFR + Federal Register + agency guidance are free.

## Common recipes

### Recipe 1: Pull current 2 CFR 200 text

```bash
# Full Part 200
curl "https://www.ecfr.gov/api/versioner/v1/full/2026-06-01/title-2.xml?part=200"

# Specific section
curl "https://www.ecfr.gov/api/versioner/v1/full/2026-06-01/title-2.xml?part=200&section=200.414"

# Or scrape via firecrawl
firecrawl_scrape url="https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200" formats=["markdown"]
```

### Recipe 2: 2 CFR 200 Subpart map

```markdown
| Subpart | Sections | Topic | Notes |
|---|---|---|---|
| A | 200.0-200.1 | Acronyms + Definitions | Term-of-art reference |
| B | 200.100-200.113 | General Provisions | Federal awarding agency requirements |
| C | 200.200-200.215 | Pre-Federal Award Reqs | Including 200.205 risk assessment |
| D | 200.300-200.346 | Post-Federal Award Reqs | 200.305 payment, 200.306 cost share, 200.308 budget revision, 200.331 subrecipient mgmt, 200.334 records retention |
| E | 200.400-200.476 | Cost Principles | Allowable / unallowable per object class — 200.414 indirect, 200.430 personnel, 200.431 fringe, 200.439 equipment |
| F | 200.500-200.521 | Audit Requirements | Single Audit ≥$1M (Oct 2024+) / $750K (pre-Oct 2024) |
```

### Recipe 3: October 2024 update — critical changes

```markdown
| Topic | Old | New (Oct 2024+) | Section |
|---|---|---|---|
| De Minimis Indirect Rate | 10% MTDC | 15% MTDC | 200.414(f) |
| Subaward MTDC base | First $25K (unchanged) | First $50K | 200.331(a)(8) |
| Equipment Threshold | $5,000 | $10,000 | 200.439 |
| Single Audit Threshold | $750K | $1M | 200.501 |
| Cost Share documentation | Stricter | Slightly relaxed for in-kind | 200.306 |
```

Applies to awards issued ON OR AFTER Oct 1, 2024. Pre-Oct 2024 awards continue under old thresholds = dual-compliance environment.

### Recipe 4: May 29 2026 OMB proposed rewrite — what to watch

```markdown
## OMB Notice of Proposed Rulemaking (May 29, 2026)
- Public comment period: through July 13, 2026
- Effective date (if adopted): October 1, 2026
- Key proposed changes:
  - Political pre-issuance review layer for discretionary grants
  - Streamlined language across subparts
  - Tightened sub-recipient monitoring requirements
  - Updated cost principles for technology + AI tools
  - Potential changes to indirect cost framework (uncertainty)
- Recipient action: monitor; comment if relevant; do NOT rewrite existing
  compliance procedures pre-adoption.
```

### Recipe 5: NIH 45 CFR 75 reversion (FY2026)

```markdown
## NIH NOT-OD-26-072
NIH awards in FY2026 revert to 45 CFR Part 75 indirect cost provisions
(vs 2 CFR 200). Practical impact:
- NIH may publish a separate ceiling indirect rate
- De minimis still available at NIH's discretion
- All other 2 CFR 200 cost principles continue to apply for non-indirect items
- Read NoA carefully; reference the specific cost principle framework cited
```

### Recipe 6: Allowability decision tree

```markdown
For any proposed cost, ask in order:

1. Is the cost necessary for the project? (Reasonableness)
   ↓
2. Is the cost permitted by the NOFO + award terms? (Federal NOFO trumps)
   ↓
3. Is the cost permitted by 2 CFR 200 Subpart E (or agency cost principles)?
   ↓
4. Is the cost allocable to this project? (Charged in proportion to benefit)
   ↓
5. Is the cost consistent with the recipient's accounting policies?
   ↓
6. Is the cost net of applicable credits? (Refunds, discounts)
   ↓
7. Is the cost adequately documented? (Receipts, time sheets, calculations)

If YES to all 7 → allowable.
If NO to any → unallowable; charge elsewhere or absorb in indirect.
```

### Recipe 7: Sub-recipient vs Contractor classification

```markdown
## 2 CFR 200.331(b) classification
**Sub-recipient (sub-award):**
- Substantive program work, not just procurement
- Performance measured against program objectives
- Has its own award-like responsibilities
- Eligible to make programmatic decisions
- Federal compliance obligations flow through

**Contractor (vendor):**
- Procurement-of-goods-or-services relationship
- Performance measured against marketplace
- Not eligible to make programmatic decisions
- Federal compliance does NOT flow through

Misclassification = audit finding.
```

### Recipe 8: Time-and-effort certification

```markdown
## 2 CFR 200.430(i) — Personnel records
Records that account for after-the-fact effort:
- Reflect actual activity charged + supported in workload
- Approved by responsible official with knowledge
- Comparable to a "personnel activity report" or other equivalent records
- Reasonable estimate vs actual depends on cost-allocation system

Frequency: typically quarterly or semi-annual; some agencies require monthly.
```

### Recipe 9: 2 CFR 200.305 payment rules

```markdown
## Cash management
- Advance payment: justified only when recipient has demonstrated
  capacity to manage cash + minimize time between draw and disbursement
- Reimbursement: default for first-time grantees + small awards
- Drawdowns: minimize advance balances; spend within "as soon as
  administratively feasible" window
- Interest earned on advances >$500 must be remitted (per agency rules)
```

### Recipe 10: Budget revision thresholds

```markdown
## 2 CFR 200.308 budget revisions
Prior written approval needed for:
- Cumulative transfers among direct cost categories >10% of award
- Change in scope or objectives
- Change in key personnel named in award
- Disengagement from project >3 months by approved PI
- Inclusion of costs requiring prior approval (e.g., foreign travel, equipment)
- Transfer of funds budgeted for participant support
- Sub-award not in approved budget
- No-cost extension (one-time, up to 12 months)

For lesser changes: notify but no prior approval needed.
```

### Recipe 11: Records retention (200.334)

```markdown
## 2 CFR 200.334 retention
- 3 years from date of submission of final expenditure report
- Longer if litigation, claim, or audit started before 3 years
- Real property + equipment: 3 years after final disposition
- Indirect cost rate proposals: 3 years from submission

Org records-retention policy should reflect these.
```

### Recipe 12: Audit findings response

```markdown
## When auditor issues a finding
1. Read finding + recommendations
2. Draft Management Response within 60 days
3. Corrective Action Plan with:
   - Steps to address
   - Owner + timeline
   - Documentation of completion
4. Track corrective actions through to closure
5. Subsequent audits will test for repeat findings (worse than new finding)
```

## Examples

### Example 1: Determine indirect cost methodology for first federal grant

**Goal:** Org has first federal grant; needs to choose indirect method.

**Steps:**
1. No NICRA → eligible for de minimis 15% MTDC per 200.414(f).
2. Document choice in proposal budget narrative + retain throughout life of award.
3. Compute MTDC base correctly (exclude equipment >$10K, subaward portions >$25K, etc.) per Recipe 6 in `budget-narrative-justification`.
4. Apply 15% to MTDC each reporting period.
5. Document in cost allocation policy.

**Result:** De minimis 15% MTDC selected + documented + auditable.

### Example 2: Determine sub-recipient vs contractor for $50K partnership

**Goal:** $50K to a partner org to deliver services; sub-recipient or contractor?

**Steps:**
1. Review 200.331(b) factors (Recipe 7).
2. Partner makes programmatic decisions + reports on outcomes → sub-recipient.
3. Document classification in writing.
4. Issue sub-award agreement with:
   - 2 CFR 200 flow-down requirements
   - Risk assessment (financial stability, prior audit findings, programmatic capacity)
   - Monitoring plan (quarterly reports + annual site visit)
   - FFATA reporting if >$30K
5. Calendar monitoring activities.
6. Document sub-recipient determination memo in award file.

**Result:** Sub-recipient classified + agreement signed + monitoring underway.

## Edge cases / gotchas

- **Dual compliance:** Orgs with multi-year grants straddling Oct 1, 2024 follow the threshold rule of the SOURCE AWARD. Track per award.
- **NIH 45 CFR 75 vs 2 CFR 200:** Read NoA to know which framework applies. NIH NOT-OD-26-072 reverts NIH but not other HHS agencies.
- **Foreign travel:** Prior approval required (200.474). Coach-class flight rule.
- **Prior approval is granular:** Some changes need agency prior approval; some need GS-level approval. Read NoA + agency-specific terms.
- **2 CFR 200.318-326 procurement standards:** Federal procurement rules flow to recipients. Competition required above micro-purchase threshold ($10K post-2024).
- **Subaward monitoring depth:** 200.331(b) factors guide depth — high-risk sub-recipient = quarterly reports + site visit; low-risk = annual reports.
- **Audit threshold trigger:** Single Audit if cumulative federal expenditures ≥$1M (post-Oct 2024) or $750K (pre-Oct 2024) in fiscal year. See `single-audit-prep-federal-750k`.
- **Cost principles by entity type:** State/local govt (200.E), Indian tribe (200.E), nonprofit (200.E), IHE/university (200.E) — same Subpart E but different supplements.
- **2026 OMB rewrite uncertainty:** Until effective Oct 1, 2026 (if adopted), existing rules apply. Don't pre-comply.
- **Audit timing:** Single Audit due 9 months after fiscal year end. Late = funding withhold + corrective action.
- **Disclaimer:** Binding compliance interpretation → qualified grants professional / nonprofit attorney / CPA.

## Sources

- eCFR 2 CFR 200: https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200
- 2 CFR 200.414 (Indirect / F&A): https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-E/subject-group-ECFRd93f2a98b1f6455/section-200.414
- 2 CFR 200.331 (Subrecipient mgmt): https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-D/section-200.331
- 2 CFR 200.306 (Cost sharing): https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-D/subject-group-ECFR2afe8a0b08d1cdc/section-200.306
- 2 CFR 200.308 (Budget revision): https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-D/section-200.308
- 2 CFR 200.334 (Records retention): https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-D/section-200.334
- May 29 2026 OMB proposed rule: https://grantedai.com/blog/omb-uniform-guidance-overhaul-2-cfr-200-may-29-2026-pre-issuance-political-review-october-1-effective-strategy
- NIH NOT-OD-26-072: https://grantedai.com/blog/federal-grants-regulatory-overhaul-2026
- Clark Nuber — De Minimis 15% update: https://clarknuber.com/articles/uniform-guidance-the-de-minimis-indirect-cost-rate-updated/
- Grant Sights — 2 CFR 200 Uniform Guidance Guide: https://grantsights.com/blog/2-cfr-200-uniform-guidance-guide
