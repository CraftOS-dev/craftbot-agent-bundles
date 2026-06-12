---
name: logic-model-inputs-activities-outputs-outcomes
description: Build 5-column logic models (Inputs → Activities → Outputs → Outcomes → Impact) + Theory of Change causal narratives using Sopact's ToC wizard, W.K. Kellogg methodology, and drawio diagrams. Use when the user says "build a logic model" or "draft a theory of change".
---

# Logic model + Theory of Change construction

Logic models force clarity. If you can't draw the arrow from Activity X to Outcome Z, you can't write the section. The W.K. Kellogg 5-column model is still the 2026 industry standard; Sopact's ToC wizard accelerates first drafts; foundation reviewers expect a Theory of Change overlay with causal arrows + assumptions.

## When to use

- Drafting the evaluation section of a federal / foundation proposal
- Funder explicitly requires a logic model (most foundations + many federal NOFOs)
- Foundation requires Theory of Change (Gates, MacArthur, Hewlett, Packard, Robert Wood Johnson)
- Org strategy planning — clarifying program logic at the operations level
- Re-evaluating a declined proposal whose evaluation section was weak

Do NOT use this skill for:
- The evaluation plan with indicators + data collection methods (→ `full-grant-proposal-narrative-methods-evaluation` evaluation section)
- Budget allocation by logic-model row (→ `budget-narrative-justification`)
- Outcome measurement frameworks alone (covered here at the logic-model level, but detailed measurement plans live in the eval section)

## Setup

```bash
# Visual diagram tools (pick one)
# drawio-mcp tool (in agent context — preferred for grant-writer)
# OR
brew install drawio   # desktop fallback

# Sopact Theory of Change wizard (free signup)
# Visit https://www.sopact.com/use-case/logic-model

# Templates
ls agent_bundle/agents/grant-writer/templates/logic_model_5col.docx
```

Auth / API key requirements:
- Sopact — free signup; paid for advanced features
- W.K. Kellogg guide — free PDF download

## Common recipes

### Recipe 1: 5-column logic model in Markdown table

```markdown
| Inputs | Activities | Outputs | Short-term Outcomes (3-12 mo) | Medium-term Outcomes (1-3 yr) | Long-term Impact (3-5+ yr) |
|---|---|---|---|---|---|
| 2.5 FTE staff | Weekly home visits to 60 families | 1,560 visits delivered | 80% of parents demonstrate ≥3 new positive parenting skills | 60% of children meet kindergarten-readiness milestones | Reduced 3rd-grade reading gap from 22% to 12% |
| $250K | Quarterly group workshops (12/yr) | 720 workshop attendees | 70% increase in parents' confidence (validated scale) | 50% reduction in family stress (validated scale) | Improved community-level family wellbeing |
| 1 evaluator | Pre/post + 6-mo follow-up surveys | 60 baseline + 60 follow-up datasets | (measurement, not outcome) | (measurement, not outcome) | |
| Evidence-based curriculum | | | | | |
| 4 partner orgs | | | | | |
```

### Recipe 2: Step-by-step column logic

```
Inputs: WHAT we commit — staff FTE, $, partners, facilities, curriculum, evaluation tools.

Activities: WHAT we DO — training delivered, services provided, advocacy meetings, research, dissemination.

Outputs: IMMEDIATE countable products — # people trained, # services delivered, # materials distributed. Outputs are NOT outcomes — they are units of activity.

Short-term Outcomes (3-12 mo): Changes in KNOWLEDGE / SKILLS / ATTITUDES / AWARENESS. Measurable with pre/post.

Medium-term Outcomes (1-3 yr): Changes in BEHAVIOR / PRACTICE / DECISION / POLICY.

Long-term Impact (3-5+ yr): Changes in CONDITION / STATUS / QUALITY OF LIFE / SYSTEMS.
```

### Recipe 3: Theory of Change causal arrows

```
Activity X → Output Y → Outcome Z

Causal claim: Activity X (weekly home visits using <curriculum>)
  produces Output Y (60 families served, 1,560 visits)
  which produces Outcome Z (80% of parents demonstrate new skills)

Assumption A: Parents engage in skill practice between visits
Evidence: Sandler et al. 2024 meta-analysis (k=42) — home-visit programs
  show 0.65 SD effect on skill acquisition when families complete ≥80% of visits.

Assumption B: New parenting skills translate to kindergarten readiness
Evidence: NSCH 2023 — positive parenting practices associated with
  41% higher kindergarten readiness (controlling for SES).
```

### Recipe 4: Draw the model in drawio

```bash
# Via drawio-mcp (in agent context)
drawio_create_diagram \
  template="logic_model_5col" \
  inputs=["2.5 FTE", "$250K", "1 evaluator", "curriculum"] \
  activities=["Home visits", "Workshops", "Surveys"] \
  outputs=["1,560 visits", "720 attendees", "60+60 datasets"] \
  short_outcomes=["80% skill demo", "70% confidence ↑"] \
  long_outcomes=["KR met", "Reading gap closed"]
```

Export PNG for the proposal + editable .drawio for revisions.

### Recipe 5: Use Sopact ToC wizard for first draft

```bash
# Sopact: paste plain-language program description, get ToC scaffold
# https://www.sopact.com/use-case/logic-model
# Output: editable 5-column model + causal narrative + assumption list
```

Then human-revise: the AI fills logic-model boxes accurately ~70% of time; outcomes column is where it most often hallucinates ambition (claims long-term impact your activities won't drive).

### Recipe 6: Anchor in W.K. Kellogg methodology

```bash
curl -O https://wkkf.issuelab.org/resource/logic-model-development-guide.html
# 70-page guide — canonical reference. Cite "W.K. Kellogg Foundation Logic Model Development Guide"
# in evaluation section for methodological credibility.
```

### Recipe 7: Indicator framework per outcome row

```markdown
| Outcome | Indicator | Data source | Collection schedule | Analysis | Target |
|---|---|---|---|---|---|
| Increased parenting skills | % parents demonstrating ≥3 skills on validated rubric | Direct observation during home visit | Pre, 6mo, 12mo | Paired t-test + effect size | 80% at 12mo |
| Increased parent confidence | Mean score on Parenting Self-Agency Measure | Self-report survey | Pre, 12mo | Paired t-test | +0.5 SD at 12mo |
| Kindergarten readiness | % children meeting all 5 readiness domains | Teacher-administered KRA | At kindergarten entry | Comparison to district baseline | 60% at K entry |
```

Indicators MUST be measurable. "Increased awareness" is not an indicator — "% participants who can correctly identify 4 of 5 program services" is.

### Recipe 8: Assumption layer (ToC requirement)

For every arrow between two boxes, name the assumption + evidence:

```markdown
## Causal arrow: Activities → Short-term Outcomes
**Assumption:** Participants will attend ≥75% of activities.
**Evidence:** Prior cohort attendance averaged 82% (FY24 internal data).
**Risk if false:** If attendance <60%, dosage-effect threshold not met (per Sandler 2024); revise recruitment + retention plan.

## Causal arrow: Short-term → Medium-term Outcomes
**Assumption:** Skills practiced in workshop transfer to home behavior.
**Evidence:** Independent evaluation of FY23 cohort showed 0.4 SD home-behavior effect.
**Risk if false:** Add booster sessions + family coaching.
```

### Recipe 9: Match logic model to evaluation budget

```bash
# Every outcome row needs a data-collection cost in the budget
# Rule of thumb: 5-15% of grant budget on evaluation
# Federal NIH-style research grants: 20-30% on evaluation
```

If logic model has 6 outcome rows but budget has $0 for evaluation, reviewers catch the mismatch.

### Recipe 10: 1-page logic model summary for funder appendix

```bash
# Final deliverable: PNG + Markdown table + assumption narrative
# Export from drawio: File → Export → PNG (high-res, 300 DPI for print)
# Render Markdown via pandoc to PDF
pandoc logic_model_5col.md -o logic_model_appendix.pdf
```

## Examples

### Example 1: Logic model for HRSA Maternal & Child Health proposal

**Goal:** Logic model for $750K, 3-year HRSA MCH proposal serving 200 families.

**Steps:**
1. Draft column-by-column in Markdown table (Recipe 1).
2. Sopact ToC wizard for first-draft ToC narrative (Recipe 5).
3. Add assumption + evidence per arrow (Recipe 8).
4. Draw in drawio with HRSA color palette (Recipe 4).
5. Add indicator framework per outcome (Recipe 7).
6. Cite W.K. Kellogg methodology in eval narrative.
7. Cross-check: every output → outcome arrow has evidence; every outcome has a budgeted indicator data source.
8. Render to PDF appendix + paste table into eval section main body.

**Result:** Logic model PNG + indicator framework table + ToC causal narrative — all ready to drop into HRSA proposal appendix.

### Example 2: ToC for Hewlett Foundation strategy proposal

**Goal:** Theory of Change for $500K Hewlett climate-policy capacity-building grant.

**Steps:**
1. Sopact ToC wizard with policy-change use case.
2. Map activities (policymaker briefings + research) to short-term outcomes (policymaker awareness shift).
3. Map short-term to medium-term (policy adoption in 2 target states).
4. Map medium-term to long-term impact (emissions reduction at state level).
5. Make assumptions explicit + cite IPCC / academic evidence base.
6. Draw clean 5-column drawio diagram.
7. Bundle as 1-page appendix.

**Result:** ToC PDF + assumption narrative + evidence citations ready for Hewlett's full-proposal appendix.

## Edge cases / gotchas

- **Output ≠ Outcome.** "1,560 visits delivered" is an output. "80% of parents demonstrate new skills" is an outcome. Reviewers downscore conflated columns.
- **Long-term impact reach.** Don't claim long-term outcomes your activities won't drive in your project period. "Reduced reading gap from 22% to 12% by Year 3 of a 1-year project" is overreach.
- **Theory of Change vs Logic Model:** ToC adds causal narrative + assumptions + evidence to the logic model. Foundations increasingly require ToC; federal usually accepts logic model alone.
- **Indicator measurability:** "Increased awareness" is not measurable; "% correctly answer 4 of 5 quiz items" is. Federal reviewers will downscore non-measurable indicators.
- **Effect size + power for research grants.** NIH / NSF / IES require power calc + alpha + effect size assumption. Add a sample-size justification.
- **Evaluation budget mismatch.** Logic model with 8 outcomes + $0 eval line = decline. Budget 5-15% (or 20-30% for NIH-tier research) for data collection + analysis.
- **W.K. Kellogg guide is canonical.** Cite it. Reviewers familiar with it weight your methodology higher.
- **Sopact AI ground-truth required.** AI wizard fills boxes ~70% accurately; long-term impact claims most often wrong. Human-review every arrow.
- **Mixed-methods evaluation gets bonus credit.** Quant outcomes + qualitative narratives + case studies score higher than quant-only.

## Sources

- W.K. Kellogg Foundation Logic Model Development Guide: https://wkkf.issuelab.org/resource/logic-model-development-guide.html
- Sopact Logic Model: https://www.sopact.com/use-case/logic-model
- Sopact Theory of Change vs Logic Model: https://www.sopact.com/use-case/theory-of-change-vs-logic-model
- ActKnowledge ToC (legacy canonical reference): https://www.theoryofchange.org/
- What Works Clearinghouse evidence tiers (ESSA): https://ies.ed.gov/ncee/wwc/
- Center for Theory of Change: https://www.theoryofchange.org/
