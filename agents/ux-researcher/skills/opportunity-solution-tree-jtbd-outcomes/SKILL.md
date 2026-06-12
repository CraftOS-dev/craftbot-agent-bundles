<!--
Sources:
Teresa Torres — Opportunity Solution Tree — https://www.producttalk.org/opportunity-solution-tree
Tony Ulwick — Outcome Statements — https://jtbd.info/outcome-statements
Teresa Torres — Continuous Discovery Habits
-->
# Opportunity Solution Tree + JTBD Outcomes — SKILL

Teresa Torres opportunity solution tree: Outcome → Opportunities → Solutions → Experiments. Built from continuous interview cadence (weekly touchpoints). Pair with Ulwick outcome statements for measurable opportunity framing. Living artifact in Excalidraw / Miro / FigJam. Leaf-level handoff to Linear for tracking.

## When to use

- Building a continuous discovery practice.
- Mapping research themes to product backlog.
- Aligning team on outcome → opportunity → solution → experiment chain.
- Quarterly product strategy planning grounded in research.
- Per-feature opportunity scoping.

Trigger phrases: "opportunity solution tree", "OST", "Teresa Torres", "continuous discovery", "outcome to opportunities", "JTBD outcome statements", "map research to roadmap".

## Setup

```bash
# Excalidraw via excalidraw-diagram-generator skill (visual)

# Notion for narrative + evidence links
curl -fsSL "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer $NOTION_API_KEY" -H "Notion-Version: 2022-06-28"

# Linear for experiment leaf tracking
curl -fsSL "https://api.linear.app/graphql" \
  -H "Authorization: $LINEAR_API_TOKEN" \
  -d '{"query":"query { viewer { id name } }"}'

# Dovetail for per-node evidence
curl -fsSL "https://dovetail.com/api/v1/me" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN"
```

## Common recipes

### Recipe 1: The OST structure (Torres)

```markdown
# Opportunity Solution Tree — 4 layers

## Layer 1: Outcome (1)
- A business outcome with a measurable target
- Not "ship more features"; "reduce time-to-first-value by 30%"

## Layer 2: Opportunities (3-5 strong)
- User pains, needs, desires surfaced from research
- Customer voice — verbatim or paraphrased
- Each opportunity = one job's worth of pain
- Distinct (not overlapping)

## Layer 3: Solutions (per opportunity)
- 3-5 candidate solutions per opportunity
- Don't commit to one yet; multiple paths
- Include do-nothing / wait / partial fixes

## Layer 4: Experiments (per solution)
- Tests to validate the solution before commit
- Riskiest assumption first
- Specific test method (e.g., Maze prototype test, A/B, fake door)
```

### Recipe 2: Outcome statement (Ulwick format)

```markdown
# Outcome format
`<direction> the <unit> of <object> when <context>`

## Examples for OST root
- "Maximize the number of users who reach activation in their first session"
- "Minimize the time it takes to import existing data when migrating from competitor"
- "Reduce the rate of churn for free-tier users in week 2"

## Tied to:
- A measurable metric (current baseline)
- A target (post-intervention)
- A timeframe
```

### Recipe 3: Map research to opportunities

```python
def research_to_opportunities(research_findings):
    """
    Each Dovetail insight or JTBD outcome → candidate opportunity
    """
    opportunities = []
    for finding in research_findings:
        if finding["type"] == "insight" and finding["mention_count"] >= 3:
            opp = {
                "name": finding["title"],
                "pain_or_desire": finding["summary"],
                "evidence_count": finding["mention_count"],
                "verbatims": finding["sample_quotes"],
                "dovetail_url": finding["url"],
                "candidate_solutions": [],
                "priority": finding["mention_count"] * finding.get("severity", 1)
            }
            opportunities.append(opp)
    return sorted(opportunities, key=lambda x: x["priority"], reverse=True)[:5]
```

### Recipe 4: Solution discovery for each opportunity

```markdown
# Per-opportunity: list candidate solutions

## Opportunity: "Inbox-overload pain for solo founders"

### Candidate solutions
1. Priority inbox feature (Gmail-like)
2. Smart digest email (1x daily summary)
3. Slack bot that pulls top emails
4. Native integration with Superhuman
5. Do nothing (recommend existing tool)

## Each solution gets:
- Cost estimate (eng weeks)
- Riskiest assumption
- Test method
```

### Recipe 5: Experiment design per solution

```markdown
# Per-solution: design experiment

## Solution: Priority inbox feature

### Riskiest assumption
"Users will adopt and actively use a separate priority inbox view."

### Experiment type
- **Fake door:** add a "Priority Inbox" link in main nav for 1 week; measure click rate; show 'coming soon' page
- **Unmoderated prototype test:** Figma mock in Maze with 30 users — task: "Find your priority email"
- **Behavioral cohort A/B:** push to 10% of users; measure 7-day retention

### Decision criteria
- Adopt if >25% click rate in fake door
- Adopt if Maze SUS >68 + task success ≥75%
- Adopt if 7-day retention lift ≥10%
```

### Recipe 6: Build the tree in Excalidraw

```python
# Pseudo: build Excalidraw scene
def ost_excalidraw(outcome, opportunities, solutions, experiments):
    scene = {"elements": []}

    # Root: outcome
    scene["elements"].append({
        "type": "rectangle", "x": 500, "y": 50, "width": 400, "height": 60,
        "fillColor": "#1e88e5"
    })
    scene["elements"].append({
        "type": "text", "text": outcome["statement"],
        "x": 510, "y": 65, "fontSize": 14, "color": "white"
    })

    # Opportunities (row 2)
    for i, opp in enumerate(opportunities):
        x = 100 + i * 200
        scene["elements"].append({
            "type": "rectangle", "x": x, "y": 200, "width": 180, "height": 80
        })
        scene["elements"].append({
            "type": "text", "text": opp["name"], "x": x + 10, "y": 215, "fontSize": 12
        })
        # Line from outcome to opportunity
        scene["elements"].append({
            "type": "line", "x1": 700, "y1": 110, "x2": x + 90, "y2": 200
        })

        # Solutions (row 3, under each opportunity)
        for j, sol in enumerate(opp["solutions"]):
            sy = 400 + j * 90
            scene["elements"].append({
                "type": "rectangle", "x": x, "y": sy, "width": 180, "height": 70
            })
            scene["elements"].append({
                "type": "text", "text": sol["name"], "x": x + 10, "y": sy + 15, "fontSize": 10
            })

    return scene
```

### Recipe 7: Notion narrative companion to Excalidraw

```markdown
# Opportunity Solution Tree: [Outcome Name]

**Date:** [YYYY-MM-DD] · **Researcher + PM:** [Names]
**Excalidraw:** [link]

## Outcome
> [Ulwick-format outcome statement]
- **Current baseline:** [metric: value]
- **Target:** [metric: value by date]
- **Owner:** [PM name]

## Opportunities (sorted by evidence + impact)

### Opp 1: [Name]
- **Pain / desire (verbatim):**
  > "[quote]" — P3 (Dovetail link)
  > "[quote]" — P7
- **Evidence count:** 9 of 12 JTBD interviews
- **Linked research:** [Dovetail insight link]

#### Candidate solutions
1. **[Solution name]**
   - Riskiest assumption: [statement]
   - Experiment: [type + design] → see [Linear issue]
   - Decision criteria: [thresholds]
2. ...

### Opp 2: ...

## Decision log
- 2026-06-10: Opportunity 1 confirmed by Q3 JTBD; experiment Linear PROD-1234 launched
- 2026-06-25: Experiment failed (only 8% fake-door clicks); deprioritize this solution
- 2026-07-05: Solution 2 (smart digest) experiment scheduled
```

### Recipe 8: Linear leaf tracking

```bash
# Per-experiment Linear issue
curl -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $LINEAR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { issueCreate(input: {title: \"OST experiment: Priority inbox fake door\", description: \"From OST [Excalidraw link]. Opportunity: Inbox overload (9 of 12 interviews). Solution: Priority inbox feature. Riskiest assumption: users will adopt a separate priority view. Experiment: fake door for 1 week; decision threshold 25% click rate. Linear PROD-1234.\", teamId: \"<team-id>\", labelIds: [\"<discovery-experiment>\"]}) { success issue { id title url } } }"
  }'
```

### Recipe 9: Weekly continuous discovery cadence (Torres)

```markdown
# Weekly continuous discovery cadence

## Mondays — Story-tell research (30 min team)
- Researcher shares 1-2 customer stories from week
- Team asks questions
- Surface emerging themes

## Tuesdays — Update OST (60 min)
- PM + researcher update tree
- Add new opportunities from week's research
- Mark solutions tested / experiments closed

## Wednesdays — Recruit + interview (4-6 hr)
- 2-3 customer interviews
- Pre-build interview guide

## Thursdays — Synthesize (3-4 hr)
- Tag transcripts in Dovetail
- Update insights
- Promote insights to OST opportunities

## Fridays — Plan next experiments (90 min)
- Review experiment results
- Identify next riskiest assumption
- Build experiment for following week
```

### Recipe 10: OST review cadence + governance

```markdown
# OST as living artifact

## Per-week
- Update with new evidence
- Mark experiments outcome
- Re-prioritize opportunities

## Per-month
- Cross-functional review (design + PM + eng + research)
- Are opportunities still right? (research drift)
- Are solutions still viable? (tech / scope shifts)

## Per-quarter
- Outcome review — still the right outcome?
- Archive completed branches
- Refresh persona links

## Anti-pattern
- OST as one-shot whiteboard exercise
- "We built it last quarter; we never updated it"
- Tree gets stale → team ignores
```

## Examples

### Example 1: Build OST for activation outcome
**Goal:** Map activation research to product backlog.

**Steps:**
1. Define outcome (Recipe 2): "Maximize % of users who reach activation in first session"
2. Pull research findings (Recipe 3) — 5 opportunities surface.
3. Brainstorm 3-5 solutions per opportunity (Recipe 4).
4. Design experiment per solution (Recipe 5).
5. Build Excalidraw tree (Recipe 6).
6. Notion narrative (Recipe 7).
7. File experiment leaves in Linear (Recipe 8).
8. Weekly cadence (Recipe 9).

**Result:** Living discovery map; team aligned on what to learn next.

### Example 2: Maintain OST quarterly
**Goal:** Keep OST living, not stale.

**Steps:**
1. Quarterly cross-functional review (Recipe 10).
2. Archive shipped solutions.
3. Add new opportunities from quarter's research.
4. Refresh outcome statement (still aligned with company priority?).

**Result:** OST stays relevant; not graveyard.

## Edge cases / gotchas

- **Outcome too vague.** "Improve UX" = not an outcome. Use Ulwick format.
- **Opportunities without evidence.** "Users probably want X" = guess. Tie every opp to research.
- **One solution per opportunity.** Locks in too early. Generate 3-5; test riskiest first.
- **Solutions without experiments.** Solution = hypothesis; experiment = test.
- **Experiment without decision criteria.** "Let's see what happens" → no real test. Define thresholds.
- **OST as one-shot whiteboard.** Living artifact requires weekly cadence.
- **No outcome owner.** Without PM owning the outcome, tree drifts.
- **Skipping continuous interview cadence.** Tree dies without fresh evidence.
- **All experiments are A/B tests.** Use mix: fake door, prototype test, wizard-of-oz, A/B.
- **Single-quarter OST.** OST lives across quarters; outcomes evolve.
- **Tree explosion.** >7 opportunities = nothing prioritized. Cap at 5.
- **Linking only finished experiments.** Always link in-flight + planned to Linear.

## Sources

- [Teresa Torres — Opportunity Solution Tree](https://www.producttalk.org/opportunity-solution-tree)
- [Teresa Torres — Continuous Discovery Habits](https://www.amazon.com/Continuous-Discovery-Habits-Discover-Products/dp/1736633309)
- [Tony Ulwick — Outcome Statements](https://jtbd.info/outcome-statements)
- [Product Talk Blog](https://www.producttalk.org/blog)
- [Linear API](https://developers.linear.app)
- [Dovetail v3 API](https://dovetail.com/help/api)
- [Excalidraw](https://excalidraw.com/)
