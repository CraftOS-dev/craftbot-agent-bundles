---
name: declined-grant-iteration
description: Respond to a declined grant — request feedback in 30 days, run internal debrief, log in portfolio decline tracker, surface pattern categories, drive portfolio-level pivots (not proposal-level fixes). Use when the user says "we got declined" / "why didn't we get funded?" / "analyze our declines" / "what's our pattern?".
---

# Declined grant iteration

A declined grant is data, not failure. Within 30 days, request feedback in writing. If not provided, run internal debrief. Log every decline in portfolio tracker. After 5+ declines, run pattern analysis — the top category becomes the portfolio-level pivot. Track patterns at portfolio level, not proposal level: chasing every individual decline is whack-a-mole.

## When to use

- A grant was just declined (within 30 days of notice)
- Reviewing 6+ months of declines to find pattern
- Building a declined-grant pattern memo for board
- Iterating on a proposal that was declined to resubmit to different funder
- Replacing a portfolio strategy where decline category is concentrated
- Using FundRobin smart-matching to improve decline-driven alignment

Do NOT use this skill for:
- Standard grant prospect research → `grant-prospect-research-grants-gov-instrumentl-candid`
- Proposal-level revision drafting → `full-grant-proposal-narrative-methods-evaluation`
- Foundation cultivation while declined → `foundation-cultivation-program-officer`
- Multi-grant pipeline tracking → `multi-grant-pipeline-mgmt`

## Setup

```bash
# Tools: gmail-mcp (feedback request), notion-mcp (declined-grant log), xlsx (pattern analysis), firecrawl-mcp (peer-org analysis)

# FundRobin AI smart-matching for declined-grant root cause
# Pricing: $29/mo
# https://www.fundrobin.com/

# Reference (free)
# Grant Writing Academy — patterns in rejections: https://grantwritingacademy.substack.com/p/tracking-patterns-in-rejections-the
# Funding for Good — rejection response: https://fundingforgood.org/rejected-what-to-do-if-your-grant-proposal-is-denied/
```

Auth / API key requirements: None. FundRobin optional ($29/mo).

## Common recipes

### Recipe 1: 30-day feedback request

```markdown
## Feedback request email (within 30 days of decline)

Subject: Thank you — and a quick request

Dear [PO Name],

Thank you for your team's review of our recent <project> proposal. We value <Funder>'s
commitment to <priority area> and we want to learn from our submission.

If your review process allows, would you be willing to share any feedback that could
strengthen a future submission? Even a brief note on what could have been stronger would
be tremendously helpful as we refine our approach.

We deeply appreciate the work <Funder> does for <community/cause>. Thank you for your
time and consideration.

Best,
[Name]
[Title]
[Org]
```

### Recipe 2: Internal debrief (if no feedback offered)

```markdown
## Debrief participants
- Grant writer
- Program lead
- Finance lead
- ED (optional)

## Debrief artifacts
- NOFO / RFP
- Submitted proposal
- Publicly known peer projects funded this cycle (use ProPublica + funder press releases)
- Funder's stated priorities (current)
- Any feedback received

## Debrief questions
1. Did we align with funder's stated priorities VERBATIM (their language, not ours)?
2. Did our budget match the funder's average grant size (within range)?
3. Did our geography match the funder's geographic priorities?
4. Did our evaluation plan have measurable, indicator-level metrics?
5. Was our org credibility evidence strong (years, prior grants, key staff)?
6. Did our need statement have primary-source data + specific population?
7. Did our timeline match the funder's typical project period?
8. Did we have a match / sustainability plan?
9. Did the funded peers have something we lacked?
10. Was the cycle particularly crowded? (Some cycles have 10x normal volume)

## Output
Pick the SINGLE most likely primary decline reason. Track in declined-grant log.
```

### Recipe 3: Decline reason categories

```markdown
## Standard categories (taxonomy)

| Category | Definition | Portfolio pivot |
|---|---|---|
| Funder priority mismatch | Project pitched outside funder's stated priorities | Tighten prospect-research alignment scoring |
| Geographic misalignment | Project area not in funder's geographic priorities | Filter prospects on geography first |
| Amount mismatch | Too high vs funder's avg grant, OR too low | Match request to funder's median |
| Weak evaluation plan | No logic model; no indicators; no data sources | Org-wide outcomes framework + eval partnership |
| Weak org credibility | Org's track record / staff / financials gap | Org credibility narrative + audited financials packet |
| Vague need statement | No primary-source data; no specific population | Standardize need-statement methodology |
| Budget misalignment | Too much indirect; missing match; unclear narrative | Standardize indirect strategy + match approach |
| Crowded field | Highly competitive cycle | Geography/topic mix-up in prospect diversification |
| Late submission / non-compliant | Missed deadline or technical errors | Deadline calendar + tech check + 5-day buffer |
| Methodology weak | Activities don't tie to outcomes | Strengthen logic model + methods sections |
| Sustainability unclear | No post-grant funding plan | Standardize sustainability section template |
| Org capacity concern | Funder doubts org can execute | Capacity-building investment + reference letters |
| Unknown | Cannot determine; insufficient info | Try peer-org outreach for funded grants context |
```

### Recipe 4: Declined-grant log schema (Notion / Airtable)

```markdown
## Declined-grant DB columns

| Column | Type | Notes |
|---|---|---|
| Grant name | Text | "<Funder> <Project> <FY>" |
| Funder | Relation → Funders DB | |
| Funder type | Select | Federal / State / Foundation / Corporate |
| Project | Text | Internal project name |
| Amount requested | Currency | |
| Match required | Currency | |
| Submitted | Date | |
| Declined | Date | |
| Time-to-decline | Formula | Declined - Submitted |
| Reason (funder-offered) | Text | If feedback received |
| Reason (hypothesized) | Select | One of Recipe 3 categories |
| Confidence in reason | Select | High / Medium / Low |
| Funded peer projects | Multi-select | Linked to ProPublica grantees if known |
| Iteration notes | Text | What we'd change |
| Next action | Select | Resubmit / Pivot funder / Pivot project / Archive |
| Linked pattern | Relation → Pattern DB | If contributing to a pattern |
```

### Recipe 5: Pattern analysis (after 5+ declines)

```markdown
## Aggregate decline categories

| Category | Declines | % of total | Award $ left on table |
|---|---|---|---|
| Weak evaluation plan | 4 | 36% | $450K |
| Funder priority mismatch | 3 | 27% | $200K |
| Crowded field | 2 | 18% | $150K |
| Vague need statement | 1 | 9% | $80K |
| Geographic misalignment | 1 | 9% | $50K |

## Top category drives portfolio pivot
- Top = "Weak evaluation plan"
- 36% of declines
- $450K cumulative $ at risk
- Pivot: invest in evaluation infrastructure (consultant + data system + framework)
- Cost of pivot: $75K + staff time
- Expected impact: reduce "weak evaluation" declines from 36% to ≤10% within 12 mo
- ROI: $450K @ improved win = $300K+ new awards / yr
```

### Recipe 6: Portfolio-level pivots (vs proposal-level)

```markdown
## Pivot examples by top category

### "Weak evaluation" → portfolio-level investment
- Hire evaluation consultant or partner with university
- Adopt outcomes framework org-wide
- Standardize logic model template
- Build org-wide outcomes data system (Sopact, Salesforce custom, internal)
- Train all program staff on indicator collection

### "Funder priority mismatch" → prospect-research filter
- Re-build prospect rubric with weighted alignment scoring
- Require 80%+ alignment threshold before submission
- Disqualify mismatches at LOI stage

### "Vague need statement" → methodology standardization
- Need-statement template enforced org-wide
- Primary-source data library maintained
- Specific population + quantified gap + citation required

### "Crowded field" → diversification
- Diversify geography (move some submissions to less-competitive geos)
- Diversify funder type (add corp + state + DAF mix)
- Time submissions to less-competitive cycles

### "Budget misalignment" → financial standards
- Standardize indirect strategy (de minimis vs NICRA)
- Standardize match approach (target 25%+)
- Budget narrative review by finance pre-submission
```

### Recipe 7: Resubmission decision tree

```markdown
## Decline → next move

Decline category?
├── Priority mismatch → Don't resubmit to same funder; pivot to better-aligned funder
├── Crowded field → Resubmit next cycle (after addressing any minor weakness)
├── Geographic misalignment → Find funder with matching geo
├── Weak evaluation → Strengthen evaluation; resubmit OR submit elsewhere
├── Org capacity concern → Pause + build capacity; revisit next cycle
├── Methodology weak → Revise + resubmit (to same funder) OR pivot
└── Unknown → Pivot to different funder (don't waste cycle on guessing)

## Resubmission timing
- Same cycle next year (most common)
- Different cycle if funder has multiple cycles per year
- Different funder if reason was alignment/geo (don't wait)
```

### Recipe 8: FundRobin smart-matching for root cause

```markdown
## FundRobin workflow
1. Sign up at https://www.fundrobin.com/ ($29/mo)
2. Upload declined proposals + funder context
3. AI analyzes alignment gaps between proposal + funder priorities
4. Generates root-cause hypothesis + improvement recommendations
5. Smart-matches your project to better-fit funders for resubmission

## When to use FundRobin vs manual debrief
- Use FundRobin: limited internal capacity, many declines, want quick directional analysis
- Use manual debrief: nuanced sector context AI may miss, board reporting, training newer staff
```

### Recipe 9: Decline pattern memo (for ED / board)

```markdown
## Quarterly decline pattern memo template

# Declined-Grant Pattern Memo — <Quarter>

**Period:** <date range>
**Total submissions:** <S>
**Total awarded:** <A>
**Total declined:** <D>
**Win rate:** <A/(A+D)>%
**Win rate previous period:** <previous>%

## Pattern analysis
[Recipe 5 table]

## Top pattern: <Category>
- Examples: <funder> + <funder> + <funder>
- Root cause hypothesis: <hypothesis>
- Evidence: <feedback received + internal debriefs + peer-org analysis>

## Recommended portfolio-level pivot
- Action 1: <specific>
- Action 2: <specific>
- Investment required: $<amount> or <FTE>
- Expected impact: <reduce category X declines from Y% to Z% within N months>
- Cost-benefit: <$ at risk vs $ to implement vs expected uplift>

## Lower-tier patterns
[Categories 2-4 with brief notes]

## Recommendation
Board approve $<X> for <pivot investment>; expect win rate improvement from <Y>% to <Z>% by <date>.
```

### Recipe 10: Iteration cadence

```markdown
## Quarterly cadence
- Run Recipe 5 pattern analysis
- Update declined-grant log
- Identify top category
- Brief ED / board

## Annual cadence
- Compare year-over-year win rate
- Track pattern shifts (last year's top vs this year's top)
- Reassess prospect-research rubric weights
- Refresh evaluation framework if needed
- Budget for next year's portfolio pivot
```

## Examples

### Example 1: Single decline — request feedback + log

**Goal:** Got declined by Ford Foundation; respond + log within 30 days.

**Steps:**
1. Day 5 of decline: Recipe 1 feedback request emailed to PO.
2. Day 10: PO replies — "Your project aligned with our priority but evaluation was thin; we funded peers with stronger evidence base."
3. Recipe 4: log in Notion declined-grant DB.
   - Reason (funder-offered): "Weak evaluation"
   - Reason (hypothesized): "Weak evaluation plan"
   - Confidence: High
   - Funded peers: <peer A>, <peer B>
4. Internal debrief 1 hr; agree this is the reason.
5. Next action: stronger evaluation plan; resubmit next cycle.

**Result:** Specific feedback obtained; log updated; future submission to Ford will lead with stronger evaluation evidence.

### Example 2: Portfolio pattern analysis after 12 months (15 declines)

**Goal:** Identify the top pattern + recommend portfolio pivot.

**Steps:**
1. Recipe 5: aggregate 15 declines into 6 categories.
2. Top category: "Weak evaluation plan" (5/15 = 33%).
3. $ at risk: $500K cumulative.
4. Recipe 6 portfolio pivot: hire $75K evaluation consultant Year 1; build org outcomes framework; train all programs.
5. Expected impact: reduce "weak evaluation" declines from 33% to ≤10% within 12 mo → +$300K/yr awards.
6. Recipe 9: pattern memo drafted; ED + board review.
7. Investment approved; consultant engaged.
8. Re-baseline declines in 6 months.

**Result:** Single investment addresses top decline category at portfolio level (vs whack-a-mole proposal fixes); win rate improvement targeted.

## Edge cases / gotchas

- **Don't take it personal.** Decline ≠ org failure. Most funders fund 5-20% of applications.
- **30-day window matters.** Feedback requests after 60+ days get ignored. Window of warmth is short.
- **PO won't always provide feedback.** Many funders policy = no feedback (Ford, MacArthur, Gates often decline). Don't be offended.
- **Funded peers tell you a lot.** Funder's press releases + 990 PF Schedule I list grantees. Pattern of who they funded vs your proposal = signal.
- **Crowded field is real.** Some cycles have 10x normal volume (e.g., post-disaster, end of year). Adjust expectations.
- **Pattern analysis needs sample.** 5+ declines minimum; 10+ for confidence. Don't pivot on 1-2 declines.
- **Distinguish funder feedback from your hypothesis.** Funder-offered (gold standard) vs hypothesized (informed guess). Confidence matters.
- **Don't chase every decline.** Some declines are correctly hypothesized as "wrong funder" — pivot to better-fit; don't iterate on the wrong funder.
- **Portfolio-level pivots are expensive but high-ROI.** $75K eval investment paying off $300K/yr is worth it; $50K to chase one declined funder is rarely worth it.
- **Track win-rate trend.** Not single declines; rolling 12-mo win rate is the real signal.
- **Don't blame staff.** Pattern often = system gap, not writer skill. Address system.
- **Resubmission stigma is rare.** Funders generally welcome revised resubmission next cycle if you've addressed feedback.
## Sources

- Grant Writing Academy — patterns in rejections: https://grantwritingacademy.substack.com/p/tracking-patterns-in-rejections-the
- Funding for Good — rejected response: https://fundingforgood.org/rejected-what-to-do-if-your-grant-proposal-is-denied/
- FundRobin AI smart-matching: https://www.fundrobin.com/
- FundRobin thought leadership: https://www.fundrobin.com/articles/thought-leadership/nonprofit-grant-rejection-smart-matching-solution/
- Granted AI — NSF rejection rates context: https://grantedai.com/blog/national-science-foundation-rejection-rates-what-to-know
- Instrumentl — handling grant rejection: https://www.instrumentl.com/blog/grant-rejection
- ProPublica Nonprofit Explorer (peer-grantee research): https://projects.propublica.org/nonprofits/
- Northwestern Foundation Relations — handling declines: https://www.northwestern.edu/foundationrelations/
