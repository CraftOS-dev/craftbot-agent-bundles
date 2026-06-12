<!--
Source: https://otio.ai/blog/cb-insights-vs-pitchbook
M&A build vs buy vs partner: Wardley overlay + DCF + scorecard + walk-away + sourcing
-->
# M&A — Build vs Buy vs Partner Framework

Wardley overlay (genesis/custom = build, product = partner, commodity = buy/rent) + strategic fit scorecard + DCF + comparable multiples + walk-away price + kill criteria. Target sourcing via PitchBook ($20k+/yr) / CB Insights ($30k+/yr) / Crunchbase ($29-49/mo) / Tracxn / SEC EDGAR (public co). At seed-Series B, Crunchbase + Tracxn + Firecrawl covers ~80%.

## When to use

- Build vs buy vs partner decision for any capability.
- Target sourcing for acquisition or strategic partnership.
- M&A decision memo for board.
- Strategic partnership evaluation (overlap with this framework).

Trigger phrases: "should we acquire X", "build vs buy", "partnership eval", "M&A memo", "target sourcing", "DCF for target", "walk-away price".

## Setup

```bash
# Crunchbase API
curl -fsSL "https://api.crunchbase.com/api/v4/data/searches/organizations" \
  -H "X-Cb-User-Key: $CRUNCHBASE_API_KEY" \
  -d '{"query":[]}'

# PitchBook (enterprise key)
curl -fsSL "https://api.pitchbook.com/v1/companies" \
  -H "Authorization: Bearer $PITCHBOOK_API_KEY"

# Tracxn API
curl -fsSL "https://platform.tracxn.com/api/2.2/auth/login" \
  -d "email=$TRACXN_EMAIL&password=$TRACXN_PASSWORD"

# SEC EDGAR for public co
curl -fsSL "https://data.sec.gov/submissions/CIK<10-digit-cik>.json" \
  -H "User-Agent: <company> <email>"
```

Auth / API key requirements:
- `CRUNCHBASE_API_KEY` — Crunchbase Settings (Starter $29/mo + Pro $49/mo).
- `PITCHBOOK_API_KEY` — Enterprise contract.
- `TRACXN_EMAIL` + `TRACXN_PASSWORD` — Tracxn account.
- `SEC_EDGAR_USER_AGENT` — SEC requires User-Agent identifying you.
- `NOTION_API_KEY` — for memo + scorecard.

## Common recipes

### Recipe 1: Wardley overlay — Build / Buy / Partner

```markdown
| Wardley position | Decision | Why |
|---|---|---|
| Genesis | BUILD | No one else has it; this is differentiation |
| Custom Built | BUILD | Still differentiating; capability not productized yet |
| Product | PARTNER | Off-the-shelf exists; differentiation isn't here |
| Commodity | BUY / RENT | Utility — AWS, Stripe, Twilio. Don't build. |

Test: where is THIS capability on the Wardley map of OUR landscape?
```

### Recipe 2: Strategic fit scorecard (weighted)

```markdown
| Dimension | Weight | Score 1-5 | Weighted |
|---|---|---|---|
| Revenue impact | 25% | 4 | 1.00 |
| Cost / margin impact | 15% | 3 | 0.45 |
| Capability acquisition | 25% | 5 | 1.25 |
| Competitive moat | 20% | 4 | 0.80 |
| Cultural fit | 15% | 3 | 0.45 |
| **TOTAL** | 100% | | **3.95** |

Rule:
- < 3.5 weighted = decline
- 3.5-4.0 = pilot first
- > 4.0 = proceed
```

### Recipe 3: DCF for acquisition target

```python
import numpy as np

# Target financials (5-year projection)
revenue_y1 = 5_000_000   # $5M ARR
growth_rate = 0.40        # 40% YoY
gross_margin = 0.75
ebitda_margin = -0.20     # negative early
years_to_positive = 3

# Discount rate
wacc = 0.18

# Project free cash flow
cf = []
rev = revenue_y1
for y in range(1, 6):
    rev = rev * (1 + growth_rate)
    margin = ebitda_margin + (y - 1) * 0.10  # margin improvement
    fcf = rev * margin
    cf.append(fcf)

# Terminal value (gordon growth)
terminal_growth = 0.03
tv = (cf[-1] * (1 + terminal_growth)) / (wacc - terminal_growth)

# DCF
pv = sum(c / (1 + wacc)**(i+1) for i, c in enumerate(cf))
pv_tv = tv / (1 + wacc)**5
dcf_value = pv + pv_tv

print(f"DCF value: ${dcf_value/1e6:.1f}M")
```

### Recipe 4: Comparable multiples (Crunchbase pull)

```bash
# Find comparable companies in the same vertical + revenue range
curl -X POST "https://api.crunchbase.com/api/v4/data/searches/organizations" \
  -H "X-Cb-User-Key: $CRUNCHBASE_API_KEY" \
  -d '{
    "field_ids":["identifier","name","funding_total","last_funding_at","revenue_range"],
    "query":[
      {"type":"predicate","field_id":"categories","operator_id":"includes","values":["saas","ai"]},
      {"type":"predicate","field_id":"revenue_range","operator_id":"includes","values":["r_00001000000_00010000000"]}
    ],
    "limit":50
  }' | jq '.entities[] | {name: .properties.name.value, funding: .properties.funding_total.value_usd, last_round: .properties.last_funding_at.value}'
```

### Recipe 5: Public co comparable (SEC EDGAR)

```bash
# Pull 10-K filings for public comparables
CIK="0001234567"  # 10-digit CIK
curl -fsSL "https://data.sec.gov/submissions/CIK$CIK.json" \
  -H "User-Agent: $SEC_EDGAR_USER_AGENT" \
| jq '.filings.recent | {form, filingDate, accessionNumber}'

# Extract revenue + multiples from 10-K via parsing
```

### Recipe 6: Integration cost estimate

```markdown
## Integration cost framework

Rough rule: 30-100% of acquisition price for software M&A.

Components:
- Engineering integration (months × FTE × loaded cost): $___
- Sales integration (territory rework, comp redesign): $___
- Customer migration (CS, support, comms): $___
- Brand / website / product UI consolidation: $___
- Legal + IP + contract assignment: $___
- Cultural / retention / severance: $___
- Real estate / HR systems consolidation: $___

Typical: 50% of price for similar-stage tuck-in; 75-100% for transformative.
```

### Recipe 7: Walk-away price

```markdown
## Walk-away price determination

Pre-negotiation:
- Below walk-away = strong yes
- At walk-away = take the deal if every other condition holds
- Above walk-away = walk

Components:
- DCF base case: $___
- Add integration cost: -$___
- Risk-adjust (synergy probability × value): -$___
- Strategic premium (only if defendable): +$___
- WALK-AWAY: $___

Lock walk-away with board before any LOI negotiation. Pre-commitment beats heat-of-moment.
```

### Recipe 8: Kill criteria

```markdown
## Kill criteria — diligence findings that force a no

| Finding | Why kill |
|---|---|
| Key talent flight risk (founder, CTO, top eng) | Acquisition value evaporates |
| Customer concentration >40% in 1 logo | Single-point churn risk |
| Tech debt requires rewrite | Integration cost balloons |
| Pending IP litigation | Liability unknowable |
| Material misrepresentation in financials | Trust gone |
| Cultural mismatch (interview their team) | Post-deal attrition |
| Regulatory action pending | Tail risk |
| Customer NPS <0 | Buying a churn problem |
```

### Recipe 9: M&A decision memo (Notion template)

```bash
mcp tool notion.create_page \
  --parent '{"page_id":"<ma-hub>"}' \
  --properties '{"title":[{"text":{"content":"M&A Memo: Target X"}}]}' \
  --children-markdown '## TL;DR
Recommendation: [Proceed at $X-Y / Pilot first / Decline]
Walk-away: $X
DACI Approver: CEO + Board (vote)

## Strategic rationale
[Why this, why now — tied to Wardley + strategy doc]

## Strategic fit scorecard
[Table — Recipe 2]

## Financial framework
- DCF at offer: $X
- Comparables: $X (range)
- Walk-away price: $X
- Integration cost: $X (Y% of price)

## Wardley overlay
[Where is target capability in our value chain]

## Integration plan
- Timeline: [...]
- Cost estimate: [...]
- Retention plan for key talent: [...]
- Brand strategy: [merge / sunset / keep distinct]

## Risks
[Top 5 with mitigations]

## Kill criteria
[Diligence findings that force a no — Recipe 8]

## Pre-mortem
[Top 5 reasons this could fail — `decision-journal-pre-mortem-klein` skill]

## DACI
- Driver: Head of Corp Dev / CFO
- Approver: CEO + Board
- Contributors: CFO, legal-counsel, target-DRI
- Informed: exec team, board

## Decision journal
[Annie Duke decision journal entry — `decision-journal-pre-mortem-klein`]
'
```

### Recipe 10: Partnership evaluation (4-quadrant)

```markdown
## Partnership eval — strategic fit × execution risk

|  | Low execution risk | High execution risk |
|---|---|---|
| **High strategic fit** | Pursue | Pilot first (limited commit) |
| **Low strategic fit** | Decline politely | Refuse |

For each candidate:
1. Score strategic fit (Recipe 2 scorecard)
2. Score execution risk (team size, regulatory, integration depth, payment terms)
3. Place on quadrant
4. Decide per quadrant rule

Term sheet → pilot → MSA scaffold for top-right.
```

### Recipe 11: Sourcing playbook

```markdown
## Target sourcing

1. **Define filters** (revenue range, vertical, geography, stage, employee count)
2. **Pull from databases**:
   - Crunchbase (Recipe 4) — $29-49/mo accessible
   - Tracxn (sector mapping + emerging tech)
   - PitchBook (if enterprise contract)
   - SEC EDGAR for public targets (Recipe 5)
3. **Enrich with Firecrawl** — pull public-facing data on each
4. **Filter by strategic fit scorecard** (Recipe 2)
5. **Initial outreach** via warm intros (VC network, advisors)

Avoid: cold outreach to founders; signals desperation.
```

### Recipe 12: Diligence checklist

```markdown
## Diligence checklist (12-week typical)

### Week 1-2: Strategic
- [ ] Wardley overlay confirmed
- [ ] Strategic fit scorecard locked
- [ ] Walk-away set
- [ ] Pre-mortem complete

### Week 3-6: Financial + Customer
- [ ] 3-yr historical financials reviewed
- [ ] FP&A forecast pressure-tested
- [ ] Top-10 customer interviews (5-10 calls)
- [ ] Cohort retention analyzed
- [ ] Unit economics validated

### Week 7-9: Legal + IP
- [ ] Articles + bylaws reviewed
- [ ] All material contracts
- [ ] IP assignments (every employee)
- [ ] Pending litigation
- [ ] Tax review

### Week 10-12: People + Tech
- [ ] Key talent interviews (CTO, top 5 eng, key sales)
- [ ] Tech stack + architecture review
- [ ] Security + compliance audit
- [ ] Cultural assessment (their team's 1:1s)

### Week 12+: Close
- [ ] Final offer + walk-away check
- [ ] Definitive agreement
- [ ] Integration plan signed off
- [ ] Communications plan ready
```

## Examples

### Example 1: Build vs buy vs partner — agent orchestration

**Goal:** Decide whether to build, buy, or partner for agent orchestration.

**Steps:**
1. Map on Wardley (`wardley-mapping-competitive-landscape` skill).
2. Agent orchestration position: Custom → Product (transitioning).
3. Implication: lean BUY/PARTNER for framework, BUILD for differentiated patterns layer.
4. Score scorecard (Recipe 2) for top 3 candidates: LangChain (partner), LlamaIndex (partner), Anthropic Agent SDK (partner).
5. Pick LangChain as partner. Build patterns layer in-house.

**Result:** 4-week build avoided; differentiated patterns clear roadmap.

### Example 2: Acquisition of competitor

**Goal:** Acquire competitor X at fair price.

**Steps:**
1. Sourcing (Recipe 11) → identified target.
2. Wardley overlay (Recipe 1) — capability is Custom-Built; supports acquisition rationale.
3. Strategic fit scorecard (Recipe 2): 4.2 weighted → proceed.
4. DCF (Recipe 3): $18M base case.
5. Comparable pull (Recipe 4): range $15-25M.
6. Walk-away (Recipe 7): $22M with board lock.
7. Pre-mortem (cross-ref skill): top 5 risks logged.
8. Diligence (Recipe 12): 12 weeks.
9. Memo + DACI (Recipe 9): board vote.
10. Close at $19M; 6-month integration plan begins.

**Result:** Acquisition with explicit walk-away; pre-locked board approval.

## Edge cases / gotchas

- **Walk-away set BEFORE negotiation.** Otherwise heat-of-moment wins.
- **Strategic fit < 3.5 = decline.** Don't pilot a bad-fit deal.
- **Integration cost is 30-100% of price.** Most acquirers underestimate.
- **Key talent retention is the deal.** Lose the founder + CTO + top 5 eng = lose 70% of value.
- **Customer concentration risk.** >40% in one logo = single-point churn = potential write-down.
- **Tech debt diligence often skipped.** Schedule technical-deep-dive in week 7-9.
- **Cultural fit interview their team.** Not the founders; the senior ICs.
- **PitchBook / CB Insights enterprise-priced.** $20-30k/yr. At early-stage, Crunchbase + Tracxn covers ~80%.
- **SEC EDGAR free + powerful for public targets.** 10-K + DEF 14A give most of what you need.
- **Pre-mortem mandatory for M&A.** ~30% better risk identification.
- **Partnership ≠ acquisition.** Different process. Term sheet → pilot → MSA.
- **Cultural mismatch kills deals post-close.** Test before LOI; it's the #1 attrition driver.
- **Don't acquire to "buy talent" without product fit.** Acqui-hires fail when product is sunset.
- **Wardley overlay catches "buying a commodity" mistake.** Don't acquire something you can rent for $1k/mo.

## Sources

- [PitchBook vs CB Insights vs Crunchbase vs Tracxn](https://otio.ai/blog/cb-insights-vs-pitchbook)
- [Crunchbase vs PitchBook (Otio)](https://otio.ai/blog/crunchbase-vs-pitchbook)
- [Build vs Buy 2026 — Wardley + agentic AI](https://medium.com/@haberlah/build-vs-buy-in-2026-using-wardley-mapping-to-navigate-the-agentic-ai-shift-be24d534b054)
- [Tracxn vs Crunchbase vs PitchBook (ReviewAdda)](https://www.reviewadda.com/institute/article/518/tracxn-vs-crunchbase-vs-dealroom-vs-pitchbook-vs-cb-insights)
- [Crunchbase API docs](https://data.crunchbase.com/docs)
- [SEC EDGAR API](https://www.sec.gov/edgar/sec-api-documentation)
