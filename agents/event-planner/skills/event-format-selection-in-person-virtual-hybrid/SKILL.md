<!--
Sources:
- PCMA 2026 Business Events Industry Outlook: https://www.pcma.org/research-insights/2026-business-events-industry-outlook/
- Bizzabo Event ROI Calculation: https://www.bizzabo.com/blog/event-roi-calculation
- MPI Industry Benchmarks: https://www.mpi.org/research
-->
# Event Format Selection (In-Person / Virtual / Hybrid) — SKILL

The first irreversible decision in every event project. Format dictates budget envelope, venue strategy, AV tier, sponsor revenue model, and timeline. Apply this decision tree before any other planning happens. Wrong format = wasted budget OR missed audience.

## When to use this skill

- Discovery call with stakeholder ("we want to host an event")
- RFP / brief lacks explicit format (read between the lines: audience + outcome + budget)
- Budget request from finance asks "should we do this in-person?"
- Pivot decision (e.g., COVID-era pivot, weather pivot, low reg pivot)
- Annual event-program planning (which 4-6 events run this year, in what mix)

**Do NOT use this skill when:**
- Format is locked by contract (venue signed, sponsor committed) — proceed to execution
- Single recurring program where format is established (e.g., monthly webinar)
- User asks about *promotion* or *registration* — use `event-marketing-paid-social-email` or `attendee-registration-cvent-eventbrite-splash`

## Setup

No external tools required — this is a native decision-tree skill. Inputs needed from the requestor:

1. **Audience target** — total attendee count, persona (executive / IC / consumer / mixed), geographic spread (single city / single region / multi-region / global)
2. **Business outcome** — MQLs, retention, brand, revenue, recruiting, training, partner relations
3. **Content density** — keynote-only, multi-track, workshop hands-on, panel-heavy
4. **Networking importance** — primary driver / secondary / nice-to-have / irrelevant
5. **Budget envelope** — total or per-attendee floor
6. **Sponsor revenue dependency** — % of total event revenue (matters for booth viability)
7. **Timeline** — date locked, season, lead time

Capture these in `notion-mcp` event-brief DB row before running the tree.

## Common recipes

### Recipe 1: Audience + geography filter (Step 1)

```
Attendee count + spread → format candidates
─────────────────────────────────────────────
<50, single region          → in-person workshop / small summit
50-300, single region       → in-person summit / small conference
300-3000, multi-region      → in-person conference (+ travel grants) OR hybrid
3000-10000, multi-region    → in-person mega-conf (+ virtual stream) OR hybrid
Global (multi-region req'd) → hybrid OR virtual
>10000 viewers              → virtual conf OR multi-region hybrid hubs
```

### Recipe 2: Business outcome overlay (Step 2)

```python
OUTCOME_BIAS = {
    'mql_leadgen':        ['hybrid', 'virtual_webinar'],
    'customer_retention': ['in_person_summit'],   # defer to customer-success
    'brand_category':     ['in_person_conf', 'hybrid'],
    'paid_revenue':       ['in_person_conf'],     # higher ticket
    'partner_investor':   ['in_person_summit', 'hybrid'],  # defer to bd-partnerships
    'recruiting_talent':  ['in_person_career_fair', 'virtual_job_fair'],
    'education_training': ['workshop'],
}
```

### Recipe 3: Content density + interactivity check (Step 3)

- **Dense technical, multi-track** → in-person OR hybrid (virtual loses focus)
- **Networking-critical** → in-person OR hybrid + Brella / Swapcard matchmaking
- **Light keynote + Q&A only** → virtual webinar (Demio / Livestorm / Zoom Events)
- **Hands-on workshop** → in-person OR virtual with breakout rooms

### Recipe 4: Budget envelope vs cost floor (Step 4)

Per PCMA 2026 + Bizzabo benchmarks:

| Format | Cost / attendee | Min viable budget (200 attendees) |
|---|---|---|
| In-person conference | $800-$2,500 (avg $1,400) | $160K-$500K |
| Hybrid | $500-$1,200 (avg $900) | $100K-$240K |
| Virtual conference | $50-$300 (avg $135) | $10K-$60K |
| Virtual webinar | $20-$80 (avg $40) | $4K-$16K |

If budget / attendee < floor → downgrade format OR cut features (AV tier, catering, swag).

### Recipe 5: Sponsor revenue dependency (Step 5)

```
% of revenue from sponsors → format recommendation
─────────────────────────────────────────────────
>40%   → in-person OR hybrid (booth + lead capture justify cost)
10-40% → hybrid (virtual booth + in-person booth)
<10%   → format-agnostic (use outcome + budget)
```

### Recipe 6: Decision matrix → Notion DB

Store every decision with explicit reasoning:

```bash
mcp tool notion.create_page \
  --database "event-briefs-db" \
  --properties '{
    "Event Name": "Q3 Customer Summit",
    "Format": "Hybrid",
    "Audience": 350,
    "Geography": "Multi-region (NA + EU)",
    "Outcome": "Retention + expansion",
    "Cost/Attendee": "$1100",
    "Sponsor Dependency": "<10%",
    "Decision Rationale": "Audience demands single shared moment but EU travel cost prohibitive. Hybrid lets EU attend virtually; NA in-person."
  }'
```

### Recipe 7: Format pivot mid-cycle

When pivoting (e.g., COVID, weather, low reg), re-run tree with new constraint:

```
Original: in-person conference, 500 attendees, Chicago, March
Constraint: travel restriction declared 4 weeks out
─────────────────────────────────────────────────────────────
Pivot 1: keep date, virtual conference (refund travel fees, reduce sponsor packages)
Pivot 2: postpone 90 days (force majeure clause; partial venue deposit credit)
Pivot 3: hybrid with reduced in-person cap (100 in-person + 400 virtual; renegotiate venue F&B minimum)
```

Document pivot rationale in event brief for post-mortem.

## Examples

### Example A: Mid-market SaaS — annual user conference

Inputs:
- Audience: 800 attendees, NA-heavy, mixed (CXO + IC)
- Outcome: Customer retention + expansion + advocacy
- Content density: 4-track, keynote, deep technical breakouts
- Networking: Primary driver (peer learning, product feedback)
- Budget: $1.2M ($1500 / attendee target)
- Sponsor dependency: 15%

Decision:
- Step 1 (size + geo): 800 / single region → in-person conference candidate
- Step 2 (outcome): retention → in-person summit OR conference
- Step 3 (density): multi-track technical → in-person ✓
- Step 4 (budget): $1500 / attendee within in-person range ✓
- Step 5 (sponsors): 15% → hybrid would expand booth value, but in-person sufficient

**Verdict: In-person conference. Add virtual streaming for keynote only (record + on-demand for absent customers).**

### Example B: Developer evangelism — webinar series

Inputs:
- Audience: 500-2000 viewers per session, global
- Outcome: MQL + community education
- Content density: 45-min talk + 15-min Q&A
- Networking: Nice-to-have
- Budget: $5K / session
- Sponsor dependency: 0%

Decision:
- Step 1 (geo): global → virtual
- Step 2 (outcome): MQL → virtual webinar ✓
- Step 3 (density): light + Q&A → virtual webinar ✓
- Step 4 (budget): $5K is virtual-only range
- Step 5: no sponsors, no dependency

**Verdict: Virtual webinar. Platform: Demio (no-download, simple) or Livestorm (evergreen on-demand).**

### Example C: Industry trade show booth presence (sponsor side)

Inputs:
- Audience: Attending someone else's 5000-attendee trade show
- Outcome: Lead generation + brand visibility
- Budget: $80K (booth + travel + lead capture)

This is not a "host an event" question — this is sponsor strategy. Hand off to `bd-partnerships` for sponsor placement; pull `sponsor-tier-deliverable-tracking` skill from the OTHER event's organizer side.

## Edge cases

### When audience is split (some demand in-person, some demand virtual)
Default to hybrid IF budget supports it. If hybrid is over budget, split into two events: in-person summit (smaller, exec-focused) + virtual webinar (broader, MQL-focused). Hand off the marketing brief to `marketing-agent` separately for each.

### When sponsor revenue depends on in-person but attendance is uncertain
Pre-sell sponsorships with a written contingency clause: "If event pivots to virtual format due to <named force majeure>, sponsor receives X virtual benefits OR pro-rata refund." Defer contract language to `venue-contract-negotiation` skill's force majeure section.

### When the event is recurring (monthly webinar, quarterly summit)
Lock format for the program, not each instance. Pivot only when audience or outcome changes materially. Re-run tree annually.

### When user says "let's do hybrid" before answering questions
Resist the default — hybrid is the most expensive AND complex format (in-person production cost + virtual platform cost + bridge tech for low-latency Q&A). Use `ask-questions-if-underspecified` to confirm hybrid is actually justified.

### When budget is below all viable floors
Reduce attendee count (smaller, higher-quality) OR cut features (no catering / DIY AV / no swag) OR shift to virtual webinar OR defer to next budget cycle.

### When networking is mandatory but budget is virtual-tier
Virtual networking requires Brella / Swapcard ($2K-$8K platform fee on top of $50-$300 / attendee). Add platform cost to budget envelope before locking decision.

### When format affects sibling-agent handoffs
- In-person → `marketing-agent` does paid social + email; `pr-comms` does earned media; `operations-agent` does insurance + procurement
- Virtual → `marketing-agent` owns the full promo; `pr-comms` only if newsworthy keynote
- Hybrid → both, with coordination on bridge tech (Brella / Swapcard / RingCentral Events)

## Sources

- **PCMA 2026 Business Events Outlook**: https://www.pcma.org/research-insights/2026-business-events-industry-outlook/
- **Bizzabo Event ROI Benchmark Data**: https://www.bizzabo.com/blog/event-roi-calculation
- **MPI Industry Research**: https://www.mpi.org/research
- **Eventmanagerblog Format Comparison**: https://www.eventmanagerblog.com/event-format-comparison
