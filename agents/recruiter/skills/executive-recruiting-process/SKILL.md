<!--
Sources: https://www.heidrick.com/
         https://www.spencerstuart.com/
         https://truesearch.com/
         https://www.daversapartners.com/
Exec recruiting (VP+, C-level) = different process: 90-180 day engagement, retained search vs
in-house decision, outcome scorecard, 360 references. Strategy + comp + closing lives with
ceo-agent; recruiter executes operational layer.
-->
# Executive Recruiting Process — SKILL

Run the executive recruiting operational layer: outcome scorecard authoring, retained-search-vs-in-house decision, longlist research, compressed-loop scheduling, 360 reference checks, and offer logistics for VP+ / C-level hires. Strategy + comp framing + closing defers to `ceo-agent`.

## When to use

- New VP+ or C-level req opened.
- Decide retained-search firm vs in-house execution.
- Coordinate retained-search engagement (weekly sync, longlist review, candidate scheduling).
- Trigger phrases: "exec hire", "VP recruiting", "C-level search", "retained search", "Heidrick", "Spencer Stuart", "True Search", "Daversa", "Riviera", "exec scorecard", "360 reference exec".
- Defer to `ceo-agent`: strategy, comp framing, equity grant, closing call.
- Defer to `legal-counsel`: exec equity grant, non-compete, severance terms, change-of-control.

## Setup

```bash
# Documents
# notion-mcp for outcome scorecard + intake doc
# google-drive-mcp for secure exec candidate dossiers

# Research
export FIRECRAWL_API_KEY="fc-xxx"           # firecrawl-mcp
export LUSHA_API_KEY="xxx"                  # contact enrichment
export ROCKETREACH_API_KEY="xxx"

# Scheduling
export GOODTIME_API_KEY="xxx"               # for multi-person compressed loops
export GOOGLE_CAL_OAUTH="<bearer>"          # 1:1 exec interviews

# References
export CROSSCHQ_API_KEY="xxx"
export TYPEFORM_TOKEN="tfp_xxx"             # fallback

# ATS
export GREENHOUSE_API_KEY="harvest_xxx"
export GH_USER_ID="123456"
```

Auth model: most components are recipient-paid seats. Retained-search firms are engagement-based (no API); coordinate via email + shared Drive.

## Common recipes

### Recipe 1: Retained-search vs in-house decision
```text
Use retained search ($75K-$300K fee, 90-180 days) when:
- C-level (CEO, CFO, CTO, CRO, COO, CHRO, GC)
- VP role with no existing internal candidate pool + no recruiter exec capacity
- Confidential search (existing exec being replaced)
- Sub-specialized (AI Research Lead, Bio CFO, Defense GC)

Use in-house when:
- VP role where recruiter has existing network + bandwidth
- Internal mobility candidate present
- Highly-recognizable employer brand reducing search effort
- Budget constrained (in-house cost ~$20-50K vs retained $75-300K)

Tier 1 firms (C-level, broad): Heidrick & Struggles, Spencer Stuart, Russell Reynolds, Egon Zehnder
Tier 2 firms (tech-focused VP): True Search, Riviera Partners, Daversa Partners, Caldwell Tech
Tier 3 / boutique: 2-3 specialists per function (AI, security, infrastructure, etc.)
```

### Recipe 2: Outcome scorecard authoring (notion-mcp template)
```markdown
# {Role} — Outcome Scorecard

## 12-month deliverables (3-5 outcomes, NOT JD tasks)
1. Hit $XM ARR by Q4 (CRO)
2. Ship platform GA by Q3 + scale to 10K users (CTO)
3. Close Series C by month 9 (CFO)
4. Build C-suite (CMO + CRO) within 6 months (CEO)
5. Reduce attrition to <12% by year-end (CHRO)

## 3-year vision
- {strategic narrative}

## Team
- Direct reports: {names + roles + tenure}
- Org size: {N people across X functions}

## Comp
- Base: {range}
- Bonus: {target %}
- Equity: {%} or {shares} (board-approved range)
- Severance: {months} (defer wording to legal-counsel)
- Change-of-control: {provisions} (defer to legal-counsel)

## Must-have / Nice-to-have / Disqualifier
{lists}

## Confidentiality
{public search vs confidential; comms plan}

## Sign-off
- CEO: ___
- Board chair (if C-level): ___
- Recruiter: ___
```

### Recipe 3: Retained-search firm vetting + engagement
```text
Before engagement:
1. Get 3-firm intro decks; compare placement track record in your space + comp tier.
2. Verify off-limits list (firms can't poach from current clients; conflict check).
3. Negotiate fee structure:
   - Engaged fee (1/3 upfront, 1/3 at shortlist, 1/3 at hire) standard
   - Cap as % of cash comp (33% IC, 25-30% sliding for VP+)
   - Guarantee period (90-180 days replace-or-refund)
4. Define cadence: weekly sync (Mondays), longlist review at week 2, shortlist at week 4-6.
5. Define communication boundaries: firm fronts; candidates don't know company until week 4+.

Engagement letter must include:
- Scope of work + role
- Fee structure + payment schedule
- Off-limits list
- Confidentiality + IP + non-solicit terms
- Replacement guarantee
- Termination provisions
```

### Recipe 4: Longlist research (in-house path)
```bash
# Firecrawl LinkedIn profiles via Sales Navigator-style queries (compliance: check ToS)
curl -s -X POST -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -d '{
    "url": "https://www.linkedin.com/sales/search/people?keywords=VP%20Engineering%20fintech&companies=stripe%2Cbrex",
    "formats": ["extract"]
  }'
# Lusha / RocketReach for verified emails + phones
curl -s -H "Authorization: Bearer $LUSHA_API_KEY" \
  "https://api.lusha.com/v2/person?linkedinUrl=<profile_url>"
```
Coordinate with `talent-sourcer`'s `cto-vp-eng-exec-sourcing` for execution; recruiter owns longlist curation + outreach quality.

### Recipe 5: Compressed-loop scheduling (Goodtime for 5+ panel)
```bash
# Exec loop: typically 4-7 interviews over 1-2 days
curl -s -X POST -H "X-API-Key: $GOODTIME_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.goodtime.io/v1/interviews/schedule" \
  -d '{
    "candidate_id": "<id>",
    "interview_template_id": "<exec_loop_template>",
    "candidate_availability_window": ["2026-06-22", "2026-06-26"],
    "constraints": {
      "compress_to_days": 2,
      "min_buffer_minutes": 30,
      "require_diversity": true,
      "interviewer_seniority_floor": "vp"
    }
  }'
```

### Recipe 6: 360 reference checks for exec
```text
Exec references = different than IC:
- 8-12 references (not 3-4): 3-4 managers + 3-4 peers + 2-3 reports + 1-2 board / customer
- Phone calls (no surveys) for senior IC+; surveys OK for skip-level board
- 45-60 min per call vs 20-30 for IC
- Structured 10-12 questions per reference (vs 6-8 for IC)
- Cross-reference for consistency (manager says "great execution" + peer says "stalled at decision point" → probe)

Crosschq for survey distribution + aggregation:
```
```bash
curl -s -X POST -H "Authorization: Bearer $CROSSCHQ_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.crosschq.com/v2/checks" \
  -d '{
    "candidate_email": "exec@example.com",
    "package": "exec_360",
    "min_references": 8,
    "categories": ["manager", "peer", "report", "board_customer"]
  }'
```

### Recipe 7: Confidential search comms (private candidate workflow)
```text
Confidential search:
- Candidate dossier in Drive folder with view-only restriction to {CEO, recruiter, board chair}
- No ATS until signed NDA + onsite (some firms never put exec in main ATS — separate confidential tracker)
- All recruiter-firm comms via firm portal (not corporate email — leak risk)
- Internal comms: code-name the role ("Project Atlas") until offer accepted
- Press / candidate disclosure plan: pre-announce internal vs market (varies)
```

### Recipe 8: Exec interview kit (different from IC)
```markdown
# Exec Interview Kit — Senior Backend (CTO example)

## Competencies (4-6 typical)
1. Strategic vision + technical bet selection
2. Org design + scaling teams
3. Executive presence + board communication
4. Talent magnetism (recruit + retain senior engineers)
5. P&L / commercial fluency
6. Crisis leadership

## STAR-T questions per competency (exec-grade)
- "Walk me through a 3-year technical bet you placed that paid off. What was the alternative? What was the cost of being wrong?"
- "Tell me about a time you had to take a 200-person org through a major reorg. How did you frame it? What did you ship?"
- "Describe a board meeting where you delivered bad news. How did you frame it? What was the reaction?"
- "Tell me about a time you lost a senior IC to a competitor. What did you learn? What did you change?"
- "Walk me through a time you killed a project that the team loved. How did you make the call? Process?"
- "Describe a leadership crisis you walked into. What were the first 30/60/90 days?"

## Loop composition
- 1:1 with CEO (60-90 min)
- 1:1 with each peer C-level (45-60 min each)
- 1:1 with skip-level (60 min)
- Board chair (45-60 min, often last)
- Working session with team (3-5 senior ICs / managers)
- "Dinner" with founders / CEO (informal but evaluated)
```

### Recipe 9: Off-list candidate research (when retained firm misses)
```bash
# Use firecrawl-mcp + Lusha to surface 5-10 "the firm didn't find them" candidates
# Often: alumni of past portfolio companies, internal promo candidates, sabbatical-returners
# Present to CEO before week-6 shortlist review.
```

### Recipe 10: Compressed timeline pressure-test
```text
Standard exec timeline:
- Week 0: intake + scorecard
- Week 2: longlist review (15-25 candidates)
- Week 4: shortlist review (5-8 candidates)
- Week 6: first-round (3-5 finalists)
- Week 8: onsite loops (2-3 finalists)
- Week 10: references (8-12 per finalist)
- Week 12: offer + close

Compress to 8-10 weeks if:
- Urgent (departure / crisis)
- Strong internal candidate as backstop
- Firm has pre-built pool from adjacent search

Stretch to 16-20 weeks if:
- Confidential search
- Niche specialization (e.g., AI-Research-Lead post-LLM era)
- Board involvement at multiple stages
```

### Recipe 11: Hand off offer + close to ceo-agent
```text
Recruiter prep:
1. Reference packet finalized (Recipe 6).
2. Comp benchmark from offer-negotiation skill (Pave / Carta / Compa exec tier; Radford for serious enterprise).
3. Equity model in Carta (vesting + acceleration scenarios).
4. Legal sign-off on equity grant terms + non-compete + severance.
5. Compressed-timeline pressure-test (Recipe 10) re-confirmed with CEO.

Hand to ceo-agent: comp framing, closing call, compensation philosophy narrative.
Recruiter retains: offer letter logistics (offer-letter-docusign-pandadoc), background check (background-check-checkr-sterling), post-offer pre-start (post-offer-pre-start-check-ins).
```

### Recipe 12: Exec onboarding handoff to operations-agent
```text
Day-1 ready for exec:
- Compensation finalized + payroll set up
- Equity grant Board-approved + Carta issued
- 30-60-90 plan reviewed with CEO + board chair
- All-hands intro communication drafted
- Direct-report 1:1 calendar built T-1 week
- C-level peer onboarding cadence (weekly with each for first 90 days)
```

## Examples

### Example 1: CFO retained search (Series-C, IPO-ready)
**Goal:** Replace departing CFO with IPO-experienced operator.
**Steps:**
1. Recipe 1: retained search YES (C-level + IPO sub-specialty).
2. Recipe 3: vet 3 firms (Spencer Stuart + Heidrick + Daversa boutique tech-CFO arm); engage Spencer Stuart.
3. Recipe 2: outcome scorecard with CEO + board chair sign-off.
4. Recipe 7: confidential search comms.
5. Recipe 5 + Recipe 8: 2-day onsite + board chair add-on.
6. Recipe 6: Crosschq 360 with 10 references.
7. Recipe 11: hand to ceo-agent for offer + close.

**Result:** Hire in week 14; smooth IPO-prep transition.

### Example 2: VP Engineering in-house (Series-A)
**Goal:** First VPE for 25-person eng org.
**Steps:**
1. Recipe 1: in-house (Series-A budget + recruiter has bandwidth).
2. Recipe 4: longlist with sourcer (cto-vp-eng-exec-sourcing).
3. Recipe 8: kit + Recipe 5 schedule.
4. Recipe 6: phone references (6 per finalist).
5. Recipe 11: hand to ceo-agent for offer.

**Result:** Hire in week 8; saved $150K retained fee; CEO + new VPE collaboration starting strong.

### Example 3: Confidential CEO succession
**Goal:** Board replacing CEO confidentially.
**Steps:**
1. Recipe 1: retained search (Heidrick).
2. Recipe 7: confidential workflow; no internal ATS.
3. Recipe 8: extended loop (3 weeks of executive interviews) including off-site dinner.
4. Recipe 6: extensive 360 via Crosschq + 3 board-chair-conducted reference calls.
5. Recipe 11: ceo-agent (here: board chair) owns closing call.

**Result:** Smooth public announcement; no leak.

## Edge cases / gotchas

- **Off-limits list violations.** If retained firm sources from a current client, they can be sued + lose engagement. Verify off-limits list in writing.
- **Confidentiality leak.** Press / glassdoor learn 1-2 weeks earlier than planned. Have comms ready; don't lie if asked (decline to comment).
- **Reference checking on senior execs is gameable.** Execs curate references — cross-check via boomerang sourcer (former reports who'd talk candidly).
- **Compressed-timeline pressure.** CEO wants offer by week 6 but board needs 8-10 references. Don't compress reference quality.
- **Equity grant size confusion.** "0.5% post-money" sounds different than "30K shares at $0.10 strike". Always express in dollar terms with multiple exit scenarios. Defer to `legal-counsel` for grant doc.
- **Non-compete vs garden leave.** UK / EU often require garden leave (paid post-termination); US states vary. Defer to `legal-counsel`.
- **Change-of-control acceleration.** Single-trigger vs double-trigger; board-sensitive. Defer to legal.
- **Retained firm "showing the same candidate to multiple clients."** Anti-pattern; verify search is dedicated to your role.
- **Background check for exec.** Extended package (criminal + civil + credit + media search + reference deep-dive). $200-$500/candidate. Defer FCRA flow to `background-check-checkr-sterling` skill.
- **Board involvement at offer stage.** Board often wants final sign-off on exec offers; budget 1-2 weeks for board cycle.
- **Severance pre-negotiation.** Sophisticated execs negotiate severance + non-compete upfront in offer. Defer wording to legal.
- **Defer to `ceo-agent`** for: strategy framing, comp philosophy, closing call. Recruiter executes ops; CEO closes.
- **Defer to `legal-counsel`** for: equity grant doc, non-compete enforceability, severance terms, change-of-control, IP assignment.
- **Defer to `operations-agent`** for: Day-1 exec onboarding execution, payroll set up at exec tier, board reporting cadence.

## Sources

- [Heidrick & Struggles](https://www.heidrick.com/)
- [Spencer Stuart](https://www.spencerstuart.com/)
- [Russell Reynolds](https://www.russellreynolds.com/)
- [Egon Zehnder](https://www.egonzehnder.com/)
- [True Search](https://truesearch.com/)
- [Daversa Partners](https://www.daversapartners.com/)
- [Riviera Partners](https://rivierapartners.com/)
- [HBR — Hiring an Executive](https://hbr.org/2017/01/the-incalculable-value-of-finding-a-ceo-who-can-coalesce-a-company)
- [Carta — Exec Equity Modeling](https://carta.com/learn/equity/exec-equity/)
- [SHRM — Executive Search Best Practices](https://www.shrm.org/topics-tools/news/talent-acquisition/executive-search-best-practices)
