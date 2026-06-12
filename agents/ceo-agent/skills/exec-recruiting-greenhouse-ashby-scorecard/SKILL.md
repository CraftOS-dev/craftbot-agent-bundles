<!--
Source: https://www.index.dev/blog/greenhouse-vs-lever-vs-ashby-ats-comparison
Exec recruiting: Geoff Smart topgrading scorecard + Ashby/Greenhouse APIs
-->
# Executive Recruiting — Greenhouse / Ashby / Outcomes Scorecard

Ashby (analytics-depth, fast-rising challenger) and Greenhouse (#1 G2 satisfaction at 98% for structured hiring) with Geoff Smart's topgrading method: outcomes-first scorecards (not JDs), structured interview kits, 360 reference checks. Lever as candidate-experience-focused alt. For C-level: retained search via True Search / SPMB / Heidrick & Struggles.

## When to use

- Hiring VP / Head of / C-level role.
- Drafting an outcomes scorecard before opening a req.
- Structuring an interview process (stage gate + scorecard).
- Running topgrading 360 reference checks.
- Onboarding plan post-offer.

Trigger phrases: "hire VP Eng", "VP Marketing scorecard", "CFO search", "exec hire", "topgrading", "reference checks", "interview kit".

## Setup

```bash
# Ashby API
curl -fsSL "https://api.ashbyhq.com/info" \
  -H "Authorization: Basic $(echo -n "$ASHBY_API_KEY:" | base64)"

# Greenhouse Harvest API
curl -fsSL "https://harvest.greenhouse.io/v1/users" \
  -u "$GREENHOUSE_API_KEY:"
```

Auth / API key requirements:
- `ASHBY_API_KEY` — Ashby Settings → API Keys (admin tier).
- `GREENHOUSE_API_KEY` — Greenhouse Configure → Dev Center → API Credential Management → Harvest API.
- `LEVER_API_KEY` — Lever Settings → Integrations → API.
- `NOTION_API_KEY` — for scorecard doc.

## Common recipes

### Recipe 1: Outcomes-first scorecard (NOT a JD)

```markdown
# VP Marketing Scorecard

## Mission
One sentence: drive top-of-funnel growth from $1M ARR → $5M ARR in 12 months via PLG-content loops.

## Outcomes (5-7 in 12 months — measurable, time-bound)
1. Hit $5M ARR with $200k/mo blended CAC by EOQ4.
2. Hire 4 marketers (Growth, Content, Demand, Brand) at quality bar by Q2.
3. Lift unaided brand awareness in ICP from 18% → 35% per Q4 survey.
4. Ship pricing v2 in collaboration with product by Q2.
5. Drive content MAU from 50k → 500k by Q4.

## Competencies (5-7 they must be world-class at)
- PLG-content loop design
- Marketing analytics (Amplitude / posthog / Google Analytics)
- B2B SaaS positioning
- Team building (hired ≥3 marketers prior)
- Founder collaboration (worked with founder-CEOs before)

## Cultural fit
- Bias to action (ships > debates)
- Customer obsession (sat in 20+ user calls last role)
- Data-driven (writes SQL or hires people who do)

## Compensation
- Base: $200-260k
- Equity: 0.5-1.0%
- Variable: 10-20% based on ARR

## Reporting
- Reports to: CEO
- Direct reports: 4 (after hires)
- Cross-functional: product, sales, customer-success
```

### Recipe 2: Create the role in Ashby

```bash
curl -X POST "https://api.ashbyhq.com/job.create" \
  -H "Authorization: Basic $(echo -n "$ASHBY_API_KEY:" | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"VP Marketing",
    "departmentId":"<marketing-dept-id>",
    "locationId":"<sf-or-remote-id>",
    "employmentType":"FullTime",
    "publishToJobBoard":true,
    "description":"<markdown of scorecard mission + outcomes>",
    "compensation":{
      "type":"Range",
      "minimum":200000,
      "maximum":260000,
      "currency":"USD"
    }
  }'
```

### Recipe 3: Create the role in Greenhouse

```bash
curl -X POST "https://harvest.greenhouse.io/v1/jobs" \
  -u "$GREENHOUSE_API_KEY:" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"VP Marketing",
    "departments":[{"id":<dept-id>}],
    "offices":[{"id":<office-id>}],
    "requisition_id":"VPM-2027",
    "users":[{"user_id":<hiring-manager-id>,"first":true,"second":false,"third":false}]
  }'
```

### Recipe 4: Structured interview kit (5-stage)

```markdown
## Stage 1 — Phone screen (30 min, recruiter)
Outcomes-fit + comp + motivation. Scorecard: yes/no on each.

## Stage 2 — Outcomes interview (60 min, CEO)
Walk through each outcome from the scorecard. For each: "Tell me about a time you did this. What was the situation, your specific actions, the measurable result?"

## Stage 3 — Working session (90 min, CEO + 1 leader)
Present a real problem: "Here's our current funnel. You have $200k/mo to grow MQLs 3x in 6 months. Walk us through your plan."

## Stage 4 — Team interviews (60 min × 3)
Each peer: outcomes + competencies. Use structured scorecard.

## Stage 5 — References (3-5 by 360)
3 peers + 2 reports + 1 manager. Topgrading template (Recipe 6).
```

### Recipe 5: Push interview kit to Ashby

```bash
curl -X POST "https://api.ashbyhq.com/interviewPlan.create" \
  -H "Authorization: Basic $(echo -n "$ASHBY_API_KEY:" | base64)" \
  -d '{
    "jobId":"<job-id>",
    "stages":[
      {"name":"Phone screen","durationMinutes":30,"interviewers":1},
      {"name":"Outcomes interview","durationMinutes":60,"interviewers":1},
      {"name":"Working session","durationMinutes":90,"interviewers":2},
      {"name":"Team interviews","durationMinutes":60,"interviewers":3,"parallelize":true},
      {"name":"References","durationMinutes":30,"interviewers":1}
    ]
  }'
```

### Recipe 6: Topgrading 360 reference call template

```markdown
1. How do you know [candidate]? When did you work together, in what capacity?
2. What were [candidate]'s 3 biggest strengths in that role? Be specific — give examples.
3. What were [candidate]'s 3 biggest weaknesses? How did they handle feedback on them?
4. How would you rate [candidate] as a [role] on a 1-10? Why that number?
5. Would you hire [candidate] again — yes or no? Why?
6. Who else should I talk to who worked closely with [candidate]?
7. [Anything specific to scorecard outcomes — "Have you seen them hit a $5M ARR goal?"]
```

### Recipe 7: Score the candidate (Ashby scorecard)

```bash
curl -X POST "https://api.ashbyhq.com/applicationFeedback.create" \
  -H "Authorization: Basic $(echo -n "$ASHBY_API_KEY:" | base64)" \
  -d '{
    "applicationId":"<app-id>",
    "interviewId":"<interview-id>",
    "scorecard":{
      "Outcome-1-hit-5M-ARR":4,
      "Outcome-2-hire-team":5,
      "Competency-PLG":5,
      "Cultural-fit":4
    },
    "overallScore":4,
    "recommendation":"Strong yes",
    "notes":"Hit similar ARR goal at PrevCo. Hired 6 in 12 months. Strong PLG instincts."
  }'
```

### Recipe 8: C-level retained search outreach

```bash
mcp tool gmail.send \
  --to "rick@truesearch.com" \
  --subject "Retained search — CFO for Series-B SaaS" \
  --body "Hi Rick,
We're opening a CFO search. Outcomes scorecard attached. Target: 12-week close.

Comp: \$250-320k base + 0.5-1.5% + 15-25% bonus.
Series B SaaS, \$5M ARR, 40 people, runway 18 months.

Process:
- 4-week sourcing + screen
- 2-week founder interviews
- 4-week refs + offer + close

Retainer: \$50k retainer + 25% of first-year cash comp on placement.

Available to kick off next week?
" \
  --attachment "./cfo-scorecard.pdf"
```

### Recipe 9: Comp benchmarking pull

```bash
# Pave / Carta Total Comp / Option Impact — manual lookups for benchmark ranges
# Cache benchmarks in Notion DB for re-use across roles
mcp tool notion.query_database \
  --database-id "<comp-benchmarks-db>" \
  --filter '{"property":"Role","select":{"equals":"VP Marketing"},"and":[{"property":"Stage","select":{"equals":"Series B"}}]}'
```

### Recipe 10: Offer letter generation

```bash
# Use Cooley GO offer letter template
mcp tool notion.create_page \
  --parent '{"page_id":"<offers-db>"}' \
  --properties '{"title":[{"text":{"content":"Offer — Jane Doe — VP Marketing"}}]}' \
  --children-markdown './offer-letter-template.md'

# Fill in: name, title, base, equity grant, vesting, start date
# Pass to legal-counsel for review before sending
```

### Recipe 11: Onboarding plan (first 90 days)

```markdown
## Days 1-30: Listen + Learn
- Read: strategy doc, last 6 board packs, last 6 investor updates
- Meet: every direct report (45 min), every leader (30 min), 10 customers (30 min)
- No major decisions

## Days 31-60: Diagnose + Plan
- Present diagnosis of current state to CEO
- Draft 12-month outcomes plan (mirror the scorecard)
- Identify first 3 hires

## Days 61-90: Execute + Decide
- First strategic decision shipped
- First hire made
- First metric moved
```

### Recipe 12: Open req tracker

```bash
mcp tool notion.create_database \
  --parent '{"page_id":"<recruiting-hub>"}' \
  --title '[{"text":{"content":"Exec Req Tracker"}}]' \
  --properties '{
    "Role":{"title":{}},
    "Stage":{"select":{"options":[{"name":"Scorecard draft"},{"name":"Sourcing"},{"name":"Interviewing"},{"name":"References"},{"name":"Offer"},{"name":"Closed"}]}},
    "Days open":{"formula":{"expression":"prop(\"Today\") - prop(\"Opened\")"}},
    "Candidates":{"number":{}},
    "Owner":{"people":{}},
    "Target close":{"date":{}}
  }'
```

## Examples

### Example 1: VP Eng search from scratch

**Goal:** Hire VP Eng in 12 weeks.

**Steps:**
1. Draft outcomes scorecard (Recipe 1) — must include 5-7 measurable outcomes.
2. Create role in Ashby (Recipe 2).
3. Push interview kit (Recipe 5). All scorecards loaded.
4. Comp benchmark check (Recipe 9). Confirm $260-330k + 0.5-1.5% is competitive.
5. Source 30 candidates via personal network + LinkedIn Recruiter + Bolster.
6. 4-week sourcing → screen → 5-stage process.
7. 360 references (Recipe 6) before any offer.
8. Generate offer (Recipe 10).
9. Pass to operations-agent for onboarding execution.

**Result:** VP Eng hired with measurable outcomes; bad-hire risk minimized via references.

### Example 2: C-level retained search

**Goal:** CFO search; founder doesn't have direct network.

**Steps:**
1. Draft scorecard (Recipe 1) — engage CEO + board on outcomes.
2. Engage retained search (Recipe 8) — True Search / SPMB / Heidrick & Struggles.
3. Search firm sources + screens.
4. Founder runs Stages 2-5 (outcomes / working session / team / references).
5. 360 references via search firm + 2 founder-direct calls.
6. Offer + close (Recipe 10).

**Result:** Senior hire in 16-20 weeks with strong references.

## Edge cases / gotchas

- **Skipping references = 80% of bad hires.** Topgrading 360s catch what interviews miss. Mandatory for VP+.
- **Two Approvers on offer = no Approver.** DACI: CEO is Approver. Board chair Informed (for C-level).
- **Scorecard outcomes must be measurable.** "Build a great marketing team" is fluff. "Hire 4 marketers at quality bar by Q2" is measurable.
- **Don't skip working session.** Interviews are theater; working sessions reveal how they think under pressure.
- **Candidate-provided references = curated.** Topgrading method: ask the candidate "who else did you work with?" then call those people.
- **Comp benchmarks shift quarterly.** Pave / Carta Total Comp data is real-time; check at offer time, not requisition time.
- **Equity refresh non-obvious.** VP equity grants include refresh: 0.5-1.5% upfront + annual refresh at 0.1-0.25%. Educate the candidate.
- **Diversity in sourcing.** Bolster + Board List + Diversity Hires Network for diverse exec candidates. Start sourcing from day 1.
- **Ashby vs Greenhouse choice.** Ashby for analytics-driven teams; Greenhouse for structured hiring playbooks at scale. Lever for candidate experience.
- **Retained search costs ~25% of first-year cash.** Budget $60-120k for C-level retained search.
- **Onboarding is the second hire process.** A bad first 90 days kills the hire even if the hire was right. Build the onboarding plan before they accept.
- **Founder bias on culture-fit interviews.** Use structured scorecards to override gut. "Culture fit" without rubric is bias.

## Sources

- [Greenhouse vs Lever vs Ashby — Index.dev](https://www.index.dev/blog/greenhouse-vs-lever-vs-ashby-ats-comparison)
- [Ashby (all-in-one recruiting)](https://www.ashbyhq.com/)
- [Greenhouse Harvest API](https://developers.greenhouse.io/harvest.html)
- [Geoff Smart — Who: The A Method for Hiring](https://www.amazon.com/Who-Method-Hiring-Geoff-Smart/dp/0345504194)
- [Pave compensation benchmarks](https://www.pave.com)
- [Carta Total Comp](https://carta.com/total-comp/)
