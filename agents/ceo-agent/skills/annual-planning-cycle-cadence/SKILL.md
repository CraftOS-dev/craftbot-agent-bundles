<!--
Source: https://www.capitaly.vc/blog/david-sacks-operating-cadence-weekly-metrics-okrs-ceo-dashboard
Annual planning: David Sacks rhythm + 2-day offsite + pre-mortem + Wardley + bottom-up
-->
# Annual Planning Cycle + Cadence

David Sacks operating cadence — annual: strategy + capital + hiring plan. Pre-work: pre-mortem on prior year + Wardley map refresh + bottom-up team plans. 2-day offsite. 8-section annual plan template (diagnosis / ambition / focus / OKRs / hiring / capital / risks / kill-criteria). OKR cascade follows via Mooncamp/Lattice/WorkBoard.

## When to use

- Annual planning cycle (Q4 prep for next fiscal year).
- Mid-year strategy refresh after material market shift.
- Pre-fundraise planning (annual plan IS the narrative).
- Onboarding board to next year's strategy.

Trigger phrases: "annual planning", "2027 plan", "FY27 offsite", "annual offsite", "yearly strategy", "planning cycle".

## Setup

```bash
# Notion for the planning canvas
mcp tool notion.search --query "Annual plan"

# Google Calendar for offsite blocks
mcp tool google-calendar.list_calendars
```

Auth / API key requirements:
- `NOTION_API_KEY` — for the 8-section plan + bottom-up doc collection.
- `GOOGLE_OAUTH_TOKEN` — for offsite scheduling.
- Analytics + finance keys — for diagnosis section.

## Common recipes

### Recipe 1: 2-week pre-work timeline

```markdown
## Pre-offsite prep (T-14 days to T-0)

| Day | Task | Owner |
|---|---|---|
| T-14 | Pre-mortem on prior year (30 min facilitation) | CEO |
| T-12 | Wardley map refresh (refresh from Q4 QBR) | CEO |
| T-10 | Bottom-up team plans assigned to leaders (1-pager each) | Leaders |
| T-7 | Capital plan refresh (runway, next round timing) | CFO |
| T-5 | Risk register update (top 10 risks + mitigations) | CEO + Leaders |
| T-3 | Bottom-up plans submitted; CEO reads | Leaders → CEO |
| T-1 | Offsite logistics + room + materials | Ops |
| T-0 | Day 1 of offsite | All |
```

### Recipe 2: Pre-mortem on prior year (30 min)

```markdown
## Pre-mortem — FY2026

Imagine: it is Jan 2028. FY2026 ambition (reach $5M ARR) failed. We are at $2M ARR.

### Silent brainstorm + round-robin (Gary Klein method)
### Top 5 reasons identified
1. ICP definition too broad — sales spread thin across segments
2. VP Eng hire late (May vs Jan target) — eng productivity gap
3. Pricing change underpriced; gross margin missed
4. Customer success understaffed; churn 12% vs 6% target
5. Brand awareness initiative pulled focus from PLG loop

### Q4 2026 → FY2027 implications
- Sharpen ICP to SaaS Series A-B (250 person + cap)
- Front-load VP-level hires (3 by Q1)
- Pricing v3 with margin floor at 78%
- CS investment up 40%
- Drop brand awareness as initiative; embed in PLG content loop instead
```

### Recipe 3: Wardley map refresh

```markdown
## Wardley map — FY27 refresh

What evolved since Q4 2026:
- Vector store: Product → Commodity (Pinecone IPO; price war)
- Agent orchestration: Custom → Product (3 frameworks competing)
- Voice / multimodal: Genesis → Custom (new entrant pressure)

Implications for FY27 strategy:
- Vector store: shift from BUILD to RENT (lower COGS)
- Agent orchestration: faster ship of patterns layer; productize
- Voice: experiment Genesis stage (low commit, high option value)
```

### Recipe 4: Bottom-up team plan template (each leader fills)

```markdown
## [Team] FY27 Plan (1 page)

### Mission for FY27
[One sentence — why team exists, what's the year about]

### Proposed objectives (1-3, qualitative)
1. ...
2. ...

### Proposed KRs (3 max per objective)
- KR1: ...
- KR2: ...
- KR3: ...

### Resources needed
- Headcount: [current X, asking +Y by month]
- Budget: $[current → ask]
- Cross-functional dependencies: [list]

### Top risks
1. ...
2. ...
3. ...

### What I would say NO to (constraints)
- ...
```

### Recipe 5: 8-section annual plan template

```bash
mcp tool notion.create_page \
  --parent '{"page_id":"<planning-hub>"}' \
  --properties '{"title":[{"text":{"content":"FY27 Annual Plan"}}]}' \
  --children-markdown '## 1. Diagnosis
[What is the challenge for FY27? Data-cited.]

## 2. Ambition
[Where are we going? The big bet.]

## 3. Focus (YES / NO)
YES:
- ...
NO:
- ...

## 4. OKRs (company → team cascade)
[Company OKRs first. Team OKRs in linked Mooncamp.]

## 5. Hiring plan (roles + timing + budget)
| Role | Q1 | Q2 | Q3 | Q4 | Notes |
|---|---|---|---|---|---|
| VP Eng | ✅ | | | | hired |
| VP Sales | | open | | | retained search |
| Head of CS | | | open | | |
| SDRs | | 2 | | 1 | |
| Eng IC | 1 | 2 | 2 | | |

Total FY27 net adds: +12 (current 40 → 52)

## 6. Capital plan
- Current cash: $2.1M
- FY27 monthly burn: $150k → $250k (ramp)
- FY27 EOP cash without raise: $0 (raise required)
- Series B target: Q3 2027, $20M, $80M pre
- Bridge option from current investors: confirmed up to $2M

## 7. Risk register (top 10)
| Risk | L | I | Mitigation | Owner |
|---|---|---|---|---|
| Series B market window closes Q3 | M | C | Open Q3 with broad list | CEO+CFO |
| ...

## 8. Kill criteria (what forces a strategy pivot)
- If MRR drops >15% in any 2 consecutive months
- If Series B target raises >50% in dilution
- If churn hits >15% in core segment
- If 2+ co-founders / VPs leave in same quarter
'
```

### Recipe 6: 2-day offsite agenda

```markdown
## Day 1 — Diagnosis + Ambition

| Time | Topic |
|---|---|
| 09:00-10:30 | Pre-mortem learnings review |
| 10:30-12:00 | Wardley map walk-through + climate discussion |
| 12:00-13:00 | Lunch (mix tables) |
| 13:00-15:00 | Diagnosis exercise — what is the FY27 challenge? |
| 15:00-17:00 | Ambition exercise — what is the big bet? |
| 17:00-17:30 | Day 1 synthesis |
| 19:00 | Team dinner (no work talk) |

## Day 2 — Focus + OKRs

| Time | Topic |
|---|---|
| 09:00-11:00 | Strategic policy (YES / NO choices) |
| 11:00-13:00 | OKR drafting (company → team) |
| 13:00-14:00 | Lunch |
| 14:00-15:00 | Hiring plan + capital plan |
| 15:00-16:00 | Risk register + kill criteria |
| 16:00-17:00 | Operating rhythm calendar lock |
| 17:00-17:30 | Commitment + share-out plan |
```

### Recipe 7: Schedule the offsite

```bash
mcp tool google-calendar.create_event \
  --calendar-id leadership@company.com \
  --summary "FY27 Annual Planning Offsite" \
  --start "2026-12-15T09:00:00" \
  --end "2026-12-16T18:00:00" \
  --attendees "leadership-team@company.com" \
  --location "Offsite — to be confirmed" \
  --description "2-day FY27 planning. Read pre-work in Notion before arrival."
```

### Recipe 8: Diagnosis exercise (90 min)

```markdown
## Diagnosis exercise — facilitation script

### Part 1: Silent (10 min)
Each person writes 3 candidates for "the FY27 challenge."
Specific, evidence-cited, unflinching.

### Part 2: Round-robin (20 min)
Each shares 1 at a time. Capture on wall.

### Part 3: Cluster (15 min)
Group similar items. Look for the ONE underlying challenge.

### Part 4: Cross-examination (30 min)
- Is it specific? (Not "competition is fierce")
- Is it evidence-cited?
- Is it unflinching?
- Does fixing it unlock everything else?

### Part 5: Lock (15 min)
Write the FY27 diagnosis in 1 paragraph. Get unanimous sign-off.
```

### Recipe 9: OKR cascade — same day

```bash
# After offsite Day 2 OKR drafting, push to Mooncamp same day
for OBJECTIVE in "Activation" "Enterprise GTM" "Profitability"; do
  curl -X POST "https://api.mooncamp.com/v1/objectives" \
    -H "Authorization: Bearer $MOONCAMP_API_KEY" \
    -d "{\"title\":\"$OBJECTIVE\",\"team_id\":\"company\",\"period\":\"FY27\"}"
done
```

### Recipe 10: Annual cadence calendar lock

```markdown
## FY27 Cadence Calendar (lock on Day 2 of offsite)

| Cadence | Date | Who | Pre-read SLA |
|---|---|---|---|
| Weekly metrics | Mondays 9-10am | CEO + Leaders | Sunday EOD |
| Monthly all-hands | 1st Thu | Full company | T-24h |
| Monthly variance review | Last Thu | CEO + CFO + Leaders | T-48h |
| Quarterly QBR | Q1/Q2/Q3/Q4 first weeks | Leaders | T-48h |
| Quarterly OKR set | Q1/Q2/Q3/Q4 first days | Leaders | T-3 days |
| Board meeting | Every 8 weeks | Board + CEO + CFO | T-72h |
| Annual planning offsite | Dec 15-16 2027 | Leaders | T-14 days |
```

### Recipe 11: Distribution + commitment

```bash
mcp tool gmail.send \
  --to "everyone@company.com" \
  --subject "FY27 Plan — published" \
  --body "Our FY27 plan: [Notion link]
TL;DR: [3-bullet summary from Section 2 Ambition]

What's next:
- Week of Jan 5: company all-hands FY27 kickoff
- Week of Jan 12: team-level OKR launches in Mooncamp
- Q1 review: April 8 QBR

Please read by Jan 3. Q&A doc: [link]"
```

### Recipe 12: Quarterly plan review against annual

```bash
# Each QBR — check plan vs reality
mcp tool notion.create_page \
  --parent '{"page_id":"<qbr-db>"}' \
  --properties '{"title":[{"text":{"content":"FY27 Plan Review — Q1"}}]}' \
  --children-markdown "## FY27 vs Q1 reality
- Diagnosis still valid? Yes / sharpen / pivot
- Ambition still ambitious? Yes / lower / raise
- YES/NO list still right? [list changes]
- OKRs on track? [pull from Mooncamp]
- Hiring plan on schedule? [vs hiring plan table]
- Capital plan on track? [vs runway forecast]
- New risks? [vs risk register]"
```

## Examples

### Example 1: FY27 planning offsite — full cycle

**Goal:** End-to-end annual planning in 4 weeks of prep + 2-day offsite.

**Steps:**
1. **T-14:** Pre-mortem on FY26 (Recipe 2).
2. **T-12:** Wardley refresh (Recipe 3).
3. **T-10:** Assign bottom-up team plans (Recipe 4).
4. **T-7:** Capital plan refresh (CFO).
5. **T-5:** Risk register update.
6. **T-3:** Team plans submitted; CEO reads.
7. **T-0 (Day 1):** Diagnosis + Ambition.
8. **Day 2:** Focus + OKRs + Hiring + Capital + Risk + Kill criteria.
9. **Day 2 EOD:** Cascade OKRs in Mooncamp (Recipe 9).
10. **T+1 week:** Distribute company-wide (Recipe 11).
11. **Q1 QBR:** First plan review (Recipe 12).

**Result:** Aligned annual plan; cadence calendar locked; OKR cascade live in 2 weeks post-offsite.

### Example 2: Mid-year strategy refresh

**Goal:** Material market shift forces mid-year replan.

**Steps:**
1. 1-day offsite (compressed from 2).
2. Re-run diagnosis (Recipe 8) on new reality.
3. Sharpen guiding policy YES / NO.
4. Adjust OKRs (drop / revise / add).
5. Update risk register.
6. Distribute v1.1 with red-line.

**Result:** Strategy matches market in 1 week; team aligned.

## Edge cases / gotchas

- **Skip pre-mortem = miss 30% of risks.** Wharton study; non-negotiable.
- **Top-down without bottom-up = team disengagement.** Bottom-up team plans force buy-in.
- **2-day offsite is the minimum.** 1-day = no diagnosis depth. 3-day = diminishing returns.
- **Diagnosis is the work.** Most teams rush to ambition + OKRs. Spend half of Day 1 on diagnosis.
- **Don't OKR before diagnosis.** OKRs without diagnosis = decorative numbers.
- **Kill criteria are non-negotiable.** Without them, sunk-cost runs the year.
- **Capital plan honesty.** If you need to raise, plan for it explicitly. Don't paper over.
- **Hiring plan has timing AND budget.** "We will hire VP Sales" without timing/budget is wishful.
- **Bottom-up plan template strict 1 page.** Forces leaders to prioritize.
- **Offsite no laptops.** Phones in basket. Deep work or it doesn't work.
- **Day 2 ends with calendar lock.** Operating rhythm calendar in (Recipe 10) BEFORE people leave.
- **Distribute fast.** Day 2 EOD → company-wide within 1 week. Memory decays.
- **Annual plan vs strategy doc.** Annual plan is the operating canvas; strategy doc is the spine. Both. Refresh both annually.
- **Mid-year refresh ≠ failure.** If reality changes, refresh. Sticking to a wrong plan is the failure.

## Sources

- [David Sacks operating cadence](https://www.capitaly.vc/blog/david-sacks-operating-cadence-weekly-metrics-okrs-ceo-dashboard)
- [Lenny Rachitsky — annual planning](https://www.lennysnewsletter.com/p/lessons-learned-from-our-yearly-planning)
- [Rumelt — Good Strategy / Bad Strategy](https://cutlefish.substack.com/p/tbm-332-the-last-strategy-framework)
- [Christina Wodtke — Radical Focus](https://www.amazon.com/Radical-Focus-Achieving-Important-Objectives/dp/0996006028)
- [Gary Klein pre-mortem](https://www.gary-klein.com/premortem)
