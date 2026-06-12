<!--
Sources: https://www.toptal.com
         https://www.turing.com
         https://andela.com
         https://arc.dev
         https://lemon.io
         https://pesto.tech
         https://distributed.com
         https://www.twine.net/blog/best-dribbble-alternatives-to-hire-top-designers/
         https://lemon.io/blog/toptal-alternatives/
         https://www.secondtalent.com/alternatives/lemon-io/
         https://distantjob.com/blog/toptal-alternatives-hire-remote-developers/
Vetted contractor marketplaces routing by urgency + budget + geography.
Toptal premium (top 3%, $100-200/hr); Turing 24h match ($40-80/hr);
Andela Africa-focused; Arc.dev AI-match; Lemon.io startup EU/LatAm;
Pesto Indian senior eng; Distributed full-teams; Twine designer marketplace.
-->
# Contractor Sourcing — Toptal / Turing / Pesto / Andela / Lemon.io / Arc.dev — SKILL

Route contractor / fractional / nearshore hires to the right vetted marketplace by urgency + budget + geography. Classify the scope; produce JD + duration brief; submit intake (API where available, email otherwise); track in Notion contractor register; manage onboarding handoff to operations-agent. The marketplace decision tree replaces hours of vendor comparison.

## When to use

- User wants to **fill a contractor / fractional / specialist role** (not full-time hire).
- User wants to **route by urgency / budget / geo** to the right marketplace.
- User wants to **scope a JD for contractor brief** (different structure than FTE JD).
- User wants to **compare Toptal vs Turing vs alternatives** for a specific scope.
- Trigger phrases: "contractor", "freelancer", "fractional", "Toptal", "Turing", "Andela", "Arc.dev", "Lemon.io", "Pesto", "nearshore dev team", "specialist for 6 weeks", "augment with offshore".

Do not use for: FTE sourcing (`linkedin-recruiter-boolean-search-strings` + `github-talent-mining-language-stars-commits`); freelance design (`product-designer-sourcing-dribbble-behance` overlaps with Twine + Toptal Design — both work); contractor onboarding / contracts / payroll (defer to `operations-agent` or finance).

## Setup

```bash
# Marketplaces with API
export TURING_API_KEY="xxx"           # https://www.turing.com/contact (employer plan)
export ARC_API_KEY="xxx"              # https://arc.dev/employer
export LEMON_INTAKE_URL="https://lemon.io/api/v1/requests"
export LEMON_API_KEY="xxx"

# Email intake (no API)
export TOPTAL_INTAKE_EMAIL="enterprise@toptal.com"
export ANDELA_INTAKE_EMAIL="sales@andela.com"
export PESTO_INTAKE_EMAIL="enterprise@pesto.tech"
export DISTRIBUTED_INTAKE_EMAIL="hello@distributed.com"

# Tracking
export NOTION_API_KEY="secret_xxx"
export NOTION_CONTRACTORS_DB="<db_id>"

# Outreach
export GMAIL_TOKEN="xxx"

# Contracts / NDA (defer to ops-agent if available)
export DOCUSIGN_KEY="xxx"
```

## Common recipes

### Recipe 1: Marketplace routing matrix (the canonical decision tree)

| Marketplace | Speed | Cost band | Sweet spot | API | Geography | Notes |
|---|---|---|---|---|---|---|
| Toptal | 5-10 days | $100-200/hr | Premium top 3%; finance + dev + design + PM | Email intake only | Global | Highest filter; slowest |
| Turing | 24h match | $40-80/hr | Mid-senior dev; AI-matched | Yes (REST) | Global (India / LatAm / Eastern Europe heavy) | Fastest at scale; 40-60% below Toptal |
| Andela | 1-2 weeks | $40-80/hr mid | Africa-based teams; full teams > solo | Email intake | Africa primary; expanded to LatAm | Strong full-team builds; HQ Nigeria |
| Arc.dev | 72h | $50-90/hr | 1% accept rate; AI-matched | Yes (REST) | Global | Strong AI-matching depth |
| Lemon.io | 24-48h | $55-95/hr | Startup-focused; EU + LatAm | Yes (intake form API) | EU + LatAm primary | Most Toptal-equivalent at lower price; no subscription |
| Pesto | 3-7 days | $30-60/hr | Indian senior engineers | Email intake | India | Strong senior India focus |
| Distributed | 1-2 weeks | varies | Full distributed teams (not solo) | Email intake | Global | Team build, not individual contractor |
| Twine | varies | $30-150/hr | Designer + creative marketplace | Yes (browse-and-message) | Global | Design-specific alt to Toptal Design |

### Recipe 2: Decision tree (the algorithm)

```python
def route_contractor_request(scope: dict) -> str:
    """
    scope keys: urgency_days, budget_hourly, geography, role_type, duration_weeks, team_size
    Returns: recommended marketplace
    """
    role = scope["role_type"]                  # dev | design | pm | finance | data
    urgency = scope["urgency_days"]
    budget = scope["budget_hourly"]
    geo = scope.get("geography", "global")
    team_size = scope.get("team_size", 1)
    duration_weeks = scope.get("duration_weeks", 12)

    # Premium budget + premium quality + slow ok
    if budget >= 120 and urgency >= 7:
        return "Toptal"

    # Speed required + global mid-budget
    if urgency <= 2 and 40 <= budget <= 80 and team_size == 1:
        return "Turing"

    # Full team (3+ contractors) + Africa nearshore
    if team_size >= 3 and geo in ("africa", "global"):
        return "Andela"

    # AI matching + 72h SLA + mid-budget
    if 50 <= budget <= 90 and urgency <= 3:
        return "Arc.dev"

    # Startup-stage + EU/LatAm + no subscription
    if 55 <= budget <= 95 and geo in ("eu", "latam", "global") and duration_weeks <= 12:
        return "Lemon.io"

    # India + senior
    if geo == "india" and budget <= 60:
        return "Pesto"

    # Full distributed team
    if team_size >= 5:
        return "Distributed"

    # Designer
    if role == "design":
        return "Twine" if budget <= 100 else "Toptal Design"

    return "Toptal"  # default for ambiguous premium scope
```

### Recipe 3: Submit request via Turing API

```bash
curl -X POST "https://api.turing.com/v1/employer/requests" \
  -H "Authorization: Bearer $TURING_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "role_type": "senior_backend_engineer",
    "tech_stack": ["python", "go", "kubernetes"],
    "duration_weeks": 12,
    "start_date": "2026-07-01",
    "hours_per_week": 40,
    "budget_hourly_usd": 65,
    "timezone_overlap_hours_pst": 4,
    "scope": "Build event-driven microservices for billing pipeline; lead 2 mid-level engineers.",
    "must_haves": ["5+ yrs Python", "shipped production K8s", "distributed systems"],
    "interview_rounds": 1
  }' | jq '{request_id: .id, matched_count: .matches_estimated, sla_hours: 24}'
```

### Recipe 4: Submit request via Arc.dev Employer API

```bash
curl -X POST "https://arc.dev/api/employer/v1/requests" \
  -H "Authorization: Bearer $ARC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior React Engineer (3-mo contract)",
    "stack": ["react", "typescript", "graphql"],
    "duration_weeks": 12,
    "rate_max_usd": 85,
    "timezone": "US-PT",
    "description": "Build design-system migration to React 19 + Server Components.",
    "matching_mode": "ai-shortlist"
  }' | jq '{request_id: .id, shortlist_eta_hours: 72}'
```

### Recipe 5: Submit request via Lemon.io intake API

```bash
curl -X POST "https://lemon.io/api/v1/requests" \
  -H "Authorization: Bearer $LEMON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "company": "Acme",
    "company_stage": "Series B",
    "role_title": "Senior Full-stack Engineer",
    "stack": ["nextjs", "typescript", "postgresql"],
    "duration_weeks": 12,
    "hours_per_week": 40,
    "budget_hourly_usd": 75,
    "start_date": "2026-07-01",
    "timezone_match": "us-east + eu",
    "description": "Ship MVP of new analytics product; work directly with co-founder CTO."
  }' | jq '{request_id, matches_eta_hours: 48}'
```

### Recipe 6: Email intake template (Toptal / Andela / Pesto / Distributed)

```
Subject: {Role} contractor request — {Company} ({duration_weeks}w)

Hi {marketplace} team,

We're looking for {N} {role} contractor(s) for {company} (Series {round}, {sector}).

Scope:
- Duration: {N} weeks ({start_date} to {end_date})
- Hours: {hours/week}
- Tech stack: {stack}
- Must-haves: {3-5 bullets}
- Geography / timezone: {pref}
- Budget: ${hourly}/hr ({budget_band})
- Interview rounds: {N}

Brief attached. Available to chat this week.

Best,
{recruiter}
```

Send via Gmail; track in Notion (Recipe 9). Expect 24-72h initial response from Toptal / Andela enterprise teams.

### Recipe 7: Contractor JD brief structure (different from FTE)

```markdown
# {Role} Contractor Brief — {Date}

## Scope (1 paragraph)
{What outcome the contractor delivers; not "tasks" but "deliverable + decision authority"}

## Timeline
- Start: {date}
- End: {date}
- Hours: {N}/week
- Total budget: ${total}

## Tech stack (specific)
- Languages: {list}
- Frameworks: {list}
- Infra: {list}
- Production deps to know: {list}

## Must-haves (3-5, not 8+)
- Has shipped X in production
- Has debugged Y at scale
- Has experience with Z stack

## Working agreement
- Timezone overlap: {hours/day with internal team}
- Communication: {Slack channel + standup time}
- Tooling access: {repo + Linear + GH + AWS readonly}
- Documentation standard: {ADR + README + tests}
- IP ownership: {standard CLA — pre-existing IP carved out}

## Success criteria (measurable)
- Week 2: {milestone}
- Week 6: {milestone}
- Week 12: {deliverable + handoff}

## Onboarding owner
{Internal engineer name + email — single point of contact}
```

### Recipe 8: Notion contractor register schema

```yaml
# One row per contractor request
schema:
  request_id: "ACME-CONTRACTOR-2026-06-01"
  marketplace: "Turing"   # or Toptal, Lemon.io, etc.
  role: "Senior Backend Engineer"
  scope_summary: "Build billing event pipeline"
  budget_hourly_usd: 65
  duration_weeks: 12
  start_date: "2026-07-01"
  end_date: "2026-09-23"
  status: "in_matching"    # draft | submitted | in_matching | shortlisted | interviewing | hired | rejected | completed
  matched_count: 4
  shortlist:
    - name: "Alex K."
      profile_url: "https://turing.com/profile/alex-k"
      rate_usd: 62
      tz: "EET"
      shortlist_status: "interviewed"
  hired_contractor:
    name: "Alex K."
    contract_signed: "2026-06-28"
    start_date: "2026-07-01"
  ongoing_check_in: "Weekly Fri 09:00"
  end_disposition: "{tbd | extended | offboarded_clean | offboarded_issue}"
```

### Recipe 9: Marketplace comparison (when scope is ambiguous)

```python
# Send the SAME scope to 2-3 marketplaces; compare shortlists
candidates = {}

# Turing
candidates["turing"] = post_turing(scope)   # 24h SLA, 3-5 matches

# Lemon.io
candidates["lemon"] = post_lemon(scope)     # 24-48h SLA, 3-7 matches

# Toptal (if budget supports premium)
candidates["toptal"] = email_toptal(scope)  # 5-10d, 1-3 high-tier matches

# After 72h: compare on rate + experience + tz + first-impression
for marketplace, matches in candidates.items():
    print(f"{marketplace}: {len(matches)} matches, median rate ${median([m.rate for m in matches])}/hr")
```

Use shortlist comparison to inform marketplace contract negotiation (e.g., Toptal counter-offer with Turing rate as leverage).

### Recipe 10: 48-hour interview workflow (contractor speed-pace)

Contractors are accustomed to fast interviews. Standard structure:

| Round | Format | Length | Purpose |
|---|---|---|---|
| 1 | Recruiter call | 30 min | Scope match + rate confirm + timeline |
| 2 | Hiring eng (paired coding or take-home review) | 60-90 min | Technical depth (avoid junior-style algo whiteboard for senior contractors) |
| 3 | Stakeholder + culture (optional) | 30 min | Working agreement + Slack/standup pace |

End-to-end target: 5 business days from shortlist to offer. Anything longer signals you're not serious; top contractors disengage.

### Recipe 11: Rate negotiation cheat sheet

| Marketplace | Negotiable? | Typical range | Notes |
|---|---|---|---|
| Toptal | Limited | Stated rate ± 10% | Highly vetted; doesn't discount aggressively |
| Turing | Yes (via Turing AM) | ± 15-20% | Volume discounts at 3+ contractors |
| Andela | Yes | ± 15% | Full-team builds get bigger discounts (-25%) |
| Arc.dev | Limited | ± 10% | AI-matched rate is close to fair-market |
| Lemon.io | Yes | ± 15% | Direct rep negotiation; flexible for repeat clients |
| Pesto | Yes | ± 20% | India market dynamics; rates negotiable |
| Distributed | Yes | varies | Full-team pricing is contract-by-contract |

### Recipe 12: Post-engagement retro (per contractor)

```markdown
# Contractor Retro — {Name} — {End Date}

## Engagement
- Marketplace: {Turing}
- Rate: ${rate}/hr × {hours} = ${total}
- Duration: {weeks} weeks

## Quality
- Deliverable completeness: {1-5}
- Code quality: {1-5}
- Communication: {1-5}
- Timezone fit: {1-5}
- Would re-engage: {yes | no | with caveats}

## Marketplace performance
- Match quality vs alternatives: {1-5}
- Speed of shortlist: {1-5}
- AM responsiveness: {1-5}

## Lessons
- {what worked}
- {what didn't}
- {scope adjustments for next request}
```

Aggregate quarterly to inform Recipe 1 routing matrix updates per your team's experience.

## Examples

### Example 1: 24h urgent — senior Python contractor for billing migration
**Goal:** Need 1 senior Python contractor by Monday (today is Thursday). Budget $80/hr. 8-week scope.
**Steps:**
1. Run Recipe 2 decision tree → Turing (24h SLA, mid-budget, solo).
2. Author scope per Recipe 7; budget = $80/hr × 40h × 8w = $25,600.
3. Submit via Recipe 3 (Turing API); request_id returned within 30s.
4. By Friday 09:00, receive 3 matches from Turing AM (24h SLA).
5. Recipe 10 interview workflow: 60-min paired session Friday afternoon; pick Alex K. (Eastern Europe, 4h overlap).
6. Contract signed via DocuSign Friday end-of-day; starts Monday.
7. Log in Notion register (Recipe 8); set Friday 09:00 weekly check-ins.

**Result:** Contractor on board within 4 business days; billing migration unblocked.

### Example 2: Build a 4-person nearshore team (Andela)
**Goal:** Need 4 contractors (2 backend, 1 frontend, 1 DevOps) for 6-month duration; budget $70/hr each. Team-build vs solo.
**Steps:**
1. Recipe 2 → Andela (team build > solo, Africa nearshore, mid-budget).
2. Author scope per Recipe 7 with explicit team composition; emphasize team coherence.
3. Email intake (Recipe 6); attach Notion doc with 4 sub-scopes + team-cohesion criteria.
4. Andela AM proposes 2 team options (8 contractor profiles, 4 per option) within 10 business days.
5. Pick option A; 4 interview rounds in single week (Recipe 10).
6. Sign master contract + 4 individual SOWs; start date in 3 weeks.
7. Onboard via single internal eng PoC for team coordination.

**Result:** 4-contractor team starts in 4 weeks total; team cohesion bonus (vs random matching).

### Example 3: Compare Toptal vs Lemon.io for fractional CTO advisor
**Goal:** Need 10h/week fractional CTO advisor for 6 months. Budget $150/hr. Strategic, not delivery.
**Steps:**
1. Recipe 2 → Toptal (premium, low-urgency, strategic).
2. ALSO try Lemon.io (Recipe 5 API submit) for comparison; flag as "explore" not "decide".
3. Recipe 6 email Toptal Enterprise with scope (10h/wk, $150/hr ceiling, advisor-tier).
4. Toptal sends 2 profiles in 7 business days; Lemon.io sends 1 in 48h.
5. Interview all 3 (Recipe 10); 2 from Toptal at higher senior tier; Lemon.io candidate strong but more delivery-leaning.
6. Pick Toptal candidate B (ex-Stripe principal, advisor-style); contract $150/hr fixed.
7. Log in Notion register; bi-weekly check-ins.

**Result:** Strategic advisor on board within 2.5 weeks; comparison validated Toptal as right call for advisor tier.

## Edge cases / gotchas

- **Misclassification cost.** Contractor vs employee distinction varies by US state + country. Confirm with finance / legal before signing. ABC test (California), IRS 20-factor (federal), EU varies. Don't be casual about this.
- **IP assignment in contractor agreement.** Standard MSAs cover work-for-hire; bespoke clauses may carve out pre-existing IP. Confirm with legal before signing.
- **NDA before exposing internal scope.** Send 1-paragraph public scope to marketplace; gate full scope behind NDA at shortlist stage.
- **Toptal exclusivity.** Toptal candidates can't be poached for FTE without paying Toptal a buyout fee (typically $25-50K for first year). Discuss before extending FTE offer.
- **Andela full-team is faster than 4 solo Andelas.** Use the team-build pathway for 3+ contractors; faster matching + lower coordination cost.
- **Turing AI-matching can over-fit on stack keywords.** If your scope needs judgement + system-design depth, weight `must_haves` heavily and interview hard.
- **Lemon.io has no subscription** = excellent for irregular contractor needs; bad if you want a recurring AM. They re-engage on request.
- **Pesto + India timezone offset.** US Pacific → IST is 12.5h offset. Plan for async-first or hire team that overlaps PT-mornings.
- **Arc.dev's 1% accept rate is marketing.** Quality is solid but no better than Turing in practice for $50-90/hr band. Differentiation is matching speed.
- **Distributed is team-build only.** Don't use for solo contractor; they'll politely decline.
- **Twine is designer-heavy; weaker for pure dev.** Use Toptal Design or Lemon.io for design contractors.
- **Contractor onboarding is YOUR job, not the marketplace's.** Tooling access, Slack channels, repo permissions, 1:1 cadence all internal. Recipe 7 working-agreement section is non-negotiable.
- **Rate negotiation has a ceiling.** Below 80% of marketplace's stated rate = quality drop. Below 70% = rejection. Be respectful.
- **Multi-marketplace shortlists violate exclusivity** at premium tiers. Toptal expects exclusive engagement at search stage. Compare BEFORE signing intake, not after.
- **48h interview pace surprises FTE recruiters.** Brief hiring managers in advance — contractor interview ≠ FTE interview cadence.
- **Geographic restrictions on contractors.** Some countries (Iran, Cuba, NK) blocked under OFAC; some company policies block all non-OECD. Confirm geography filter at intake.
- **Currency + payment terms.** USD invoicing standard; some marketplaces (Pesto) bill in INR — confirm with finance.
- **Contractor → FTE conversion path** (the Toptal buyout, the Turing direct-hire). Plan for it upfront if there's any chance.
- **Hand off contract execution + payroll + tooling provisioning** to `operations-agent` once shortlist is approved. Marketplaces don't do that for you.

## Sources

- Toptal: https://www.toptal.com
- Turing: https://www.turing.com
- Andela: https://andela.com
- Arc.dev: https://arc.dev
- Lemon.io: https://lemon.io
- Lemon.io blog — Toptal alternatives 2026: https://lemon.io/blog/toptal-alternatives/
- Pesto: https://pesto.tech
- Distributed: https://distributed.com
- Twine — Dribbble alternatives 2026: https://www.twine.net/blog/best-dribbble-alternatives-to-hire-top-designers/
- Second Talent — Lemon.io alternatives: https://www.secondtalent.com/alternatives/lemon-io/
- DistantJob — Toptal alternatives: https://distantjob.com/blog/toptal-alternatives-hire-remote-developers/
