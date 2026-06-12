<!--
Source: https://cutlefish.substack.com/p/tbm-332-the-last-strategy-framework
Rumelt kernel + OGSM + V2MOM strategy doc skill
-->
# Vision + Strategy Doc — Rumelt / OGSM / V2MOM

Rumelt's "Good Strategy / Bad Strategy" kernel (diagnosis → guiding policy → coherent actions) is the spine the CEO Agent uses to verify a strategy isn't bad. OGSM (Objectives / Goals / Strategies / Measures) and Salesforce V2MOM (Vision / Values / Methods / Obstacles / Measures) are operating formats. This pack carries the templates, the Rumelt 3-question test, and the bad-strategy checklist.

## When to use

- Drafting or refreshing an annual or multi-year company strategy.
- Pressure-testing a strategy doc against Rumelt's "bad strategy" signatures.
- Choosing an operating canvas (OGSM for SaaS / B2B, V2MOM for values-led culture co).
- Founder asks "is my strategy any good?" or "write our FY2027 strategy."

Trigger phrases: "write our strategy", "refresh strategy", "is this bad strategy", "OGSM", "V2MOM", "Rumelt kernel", "FY27 strategy doc".

**Fallback when Notion unavailable:** Markdown file in repo, `pdf`/`docx` skill for distribution.

## Setup

```bash
# notion-mcp is the source-of-record. Verify connectivity.
mcp tool notion.search --query "Strategy"

# gemini for second-opinion critique against the bad-strategy checklist
gemini --model gemini-2.5-pro --prompt-file ./bad-strategy-checklist.md
```

Auth / API key requirements:
- `NOTION_API_KEY` — Notion integration token (settings → integrations).
- `GEMINI_API_KEY` — for critique pass (free tier covers 50 req/day).

## Common recipes

### Recipe 1: Create the strategy doc page in Notion

```bash
mcp tool notion.create_page \
  --parent '{"page_id":"<company-strategy-hub-page-id>"}' \
  --properties '{"title":[{"text":{"content":"Strategy — FY2027"}}]}' \
  --children-template ./strategy-doc-spine.md
```

Loads the Rumelt + OGSM spine (diagnosis / guiding policy / coherent actions / OGSM table / risk register / bad-strategy checklist).

### Recipe 2: Diagnosis section — the unflinching what-is

```markdown
## 1. Diagnosis
What's the challenge? What changed? What's the data?

- Specific, evidence-cited, no fluff.
- Example: "We're losing 40% of trials at Day 2 because activation is broken; Amplitude funnel D7 = 11% vs 28% needed for LTV:CAC > 3."

NOT: "Competition is fierce" / "Macro is tough" / "We need to grow."
```

### Recipe 3: Guiding policy — the explicit YES/NO

```markdown
## 2. Guiding policy
The choice. What we say YES to. What we say NO to (load-bearing).

YES:
- Focus on PLG-led activation for solo founders.
- Ship 1 onboarding redesign per month.
- Hire a content-led-growth lead by Aug 1.

NO:
- No paid acquisition above $100k/mo through Q4.
- No enterprise sales motion until $10M ARR.
- No new vertical until D7 retention > 30%.
```

### Recipe 4: Coherent actions table

```markdown
## 3. Coherent actions
| Initiative | Owner (DRI) | KR | Resources | Sequence | Kill criteria |
|---|---|---|---|---|---|
| Activation redesign v2 | PM Sara | D7 11% → 25% | 2 eng + 1 design | Q1 | If D7 < 18% by end Q2, pause |
| Content-led-growth lead hire | CEO | Hired by Aug 1 | $260k base + 1% | Q1-Q2 | If no offer by Sep, retained search |
| In-product viral loop | PM Tom | K-factor 0.3 → 0.6 | 1 eng | Q3 | If K-factor < 0.4 by Q4, kill |
```

### Recipe 5: OGSM operating canvas

```markdown
## 4. OGSM
| Objective | Goal (measurable) | Strategy | Measure |
|---|---|---|---|
| Activate solo founders faster | D7 11% → 25% by EOQ4 | Onboarding-redesign + nudge sequence | Amplitude D7 retention |
| Grow ARR responsibly | $1.2M → $5M ARR by EOQ4 | PLG + content-loop only | Stripe MRR x 12 |
| Build content-led growth muscle | 50k → 500k MAU on site | Hire CLG lead + content sprint | Plausible MAU |
```

### Recipe 6: V2MOM alternative spine

```markdown
- **Vision** — every solo founder shipping by Day 7.
- **Values** — speed, candor, customer obsession.
- **Methods** — (1) activation redesign, (2) content-led growth, (3) viral loop, (4) hire CLG lead, (5) ship 1 customer story / week.
- **Obstacles** — eng bandwidth, content credibility, CAC unknown.
- **Measures** — D7 retention, MRR, content MAU, CLG hire date.
```

### Recipe 7: Run Rumelt 3-question test (critic pass)

```bash
gemini --prompt "Read attached strategy doc. Answer with YES/NO + 1-sentence reasoning for each:
1. Is the diagnosis named, specific, evidence-cited, unflinching?
2. Is the guiding policy a real choice (says NO to as much as YES)?
3. Are the actions mutually reinforcing, sequenced, resourced?

If any answer is NO, list the failing section and why." \
  --file ./fy27-strategy.md
```

If any answer is NO → that's bad strategy. Don't ship.

### Recipe 8: Bad-strategy signature scan

```bash
gemini --prompt "Scan attached strategy doc for Rumelt's four bad-strategy signatures:
1. Fluff (vague abstractions like 'synergize value across the ecosystem')
2. Failure to face the challenge (no diagnosis section)
3. Mistaking goals for strategy ('grow to \$100M ARR' as the strategy)
4. Bad strategic objectives (too many, disconnected, unresourced)

Quote offending text. Suggest rewrites." \
  --file ./fy27-strategy.md
```

### Recipe 9: Add risk register

```markdown
## 5. Risks + mitigations
| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| CLG hire delays | M | H | Engage 2 retained searches in parallel | CEO |
| D7 redesign misses | M | H | Ship 3 A/B tests before locking | PM |
| Cash crunch if delay | L | C | 18mo runway buffer + bridge option | CFO |
```

### Recipe 10: Quarterly review block (set in calendar)

```bash
mcp tool google-calendar.create_event \
  --calendar-id primary \
  --summary "Strategy doc — quarterly refresh" \
  --start "2027-04-01T09:00:00" \
  --recurrence "RRULE:FREQ=QUARTERLY;COUNT=4" \
  --description "Re-run Rumelt 3-question test. Decide: stay, pivot, or sharpen?"
```

### Recipe 11: Version + publish

```bash
mcp tool notion.update_page --page-id "<strategy-page>" \
  --properties '{"Status":{"select":{"name":"Published"}},"Version":{"rich_text":[{"text":{"content":"FY2027 v1.0"}}]}}'

# Distribute via email to leadership team
mcp tool gmail.send \
  --to "leadership@co.com" \
  --subject "FY2027 Strategy — published (v1.0)" \
  --body "FY27 strategy doc is live: [link]. Please read before Monday's strategy review."
```

### Recipe 12: Notion DB for strategy version history

```bash
mcp tool notion.create_database \
  --parent '{"page_id":"<strategy-hub>"}' \
  --title '[{"text":{"content":"Strategy Versions"}}]' \
  --properties '{
    "Version":{"title":{}},
    "Period":{"select":{"options":[{"name":"FY2026"},{"name":"FY2027"}]}},
    "Status":{"select":{"options":[{"name":"Draft"},{"name":"Published"},{"name":"Superseded"}]}},
    "Rumelt-OK":{"checkbox":{}},
    "Published":{"date":{}}
  }'
```

## Examples

### Example 1: FY27 strategy from scratch

**Goal:** Solo founder draft → critic pass → publish.

**Steps:**
1. Run Recipe 1 to scaffold the spine in Notion.
2. CEO drafts diagnosis (Recipe 2) — must cite ≥3 evidence points (revenue, retention, NPS, cohort data).
3. Force YES/NO choices in guiding policy (Recipe 3). Each NO is a commitment.
4. Build coherent actions table (Recipe 4) — every initiative needs DRI + KR + kill criteria.
5. Fill OGSM table (Recipe 5).
6. Run Rumelt 3-question test (Recipe 7). If any NO → back to step 2.
7. Run bad-strategy signature scan (Recipe 8). Rewrite flagged sections.
8. Add risk register (Recipe 9).
9. Set quarterly refresh in calendar (Recipe 10).
10. Publish and distribute (Recipe 11).

**Result:** Lawyer-vetted-quality strategy doc with explicit kill criteria; quarterly cadence locked.

### Example 2: Mid-year strategy refresh after market shift

**Goal:** Strategy in market doesn't match June reality. Refresh in 1 week.

**Steps:**
1. Pull current strategy doc + last 2 QBR decision logs.
2. Diagnosis section — what changed since publish? Cite specifics.
3. Re-do guiding policy — what's the new YES/NO?
4. Update actions table — re-resource, re-sequence.
5. Run critic pass on the delta (Recipe 7).
6. Distribute v1.1 with red-line diff.

**Result:** Strategy doc reflects market; leadership team aligned in 5 working days.

## Edge cases / gotchas

- **No diagnosis = fluff strategy.** The most common failure mode. Force the founder to name the actual challenge with data before any "Action" gets written.
- **YES without NO is wishful thinking.** Guiding policy must include explicit declines. "We will not pursue enterprise until X" is more load-bearing than "We will focus on SMB."
- **Goals vs strategy confusion.** "Reach $100M ARR" is a goal. "Win SMB by collapsing time-to-value to 5 minutes" is a strategy. Educate the team relentlessly.
- **Too many objectives = no objectives.** Cap at 3-5 company objectives. More than that and they're decorative.
- **Kill criteria are non-negotiable.** Every initiative needs a "we reverse this if X" condition. Otherwise sunk-cost takes over.
- **Rumelt test is binary, not aspirational.** If diagnosis fails, send back. Don't ship "draft" strategies — they become permanent.
- **OGSM vs V2MOM choice.** OGSM is more standard for SaaS / B2B. V2MOM (Salesforce) is values-forward — pick if the company runs on values rituals (Marc Benioff style).
- **Quarterly refresh is not redoing.** It's: re-run Rumelt 3-question test. Decide stay / sharpen / pivot. Don't waste cycles rewriting unless something material changed.
- **Bad-strategy signatures repeat.** Same teams write the same fluff every cycle. Maintain a "rewrite catalog" in Notion to speed up future critic passes.
- **Founder ego attaches to wording.** Critic pass via `gemini` depersonalizes feedback. Frame as "the doc has these signatures" not "you wrote bad strategy."

## Sources

- [Rumelt — Good Strategy / Bad Strategy (TBM)](https://cutlefish.substack.com/p/tbm-332-the-last-strategy-framework)
- [OGSM framework (MasterClass)](https://www.masterclass.com/articles/ogsm)
- [Salesforce V2MOM origin](https://www.salesforce.com/blog/how-to-create-alignment-within-your-company/)
- [Rumelt — Good Strategy / Bad Strategy book](https://www.amazon.com/Good-Strategy-Bad-Difference-Matters/dp/0307886239)
- [Roger Martin — Playing to Win](https://rogermartin.medium.com/playing-to-win-strategy-d3df3fdab4dc)
