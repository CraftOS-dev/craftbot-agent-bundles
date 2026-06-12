<!--
Sources: https://pave.com/product/total-comp
         https://www.levels.fyi/
         https://carta.com/learn/equity/
         https://www.compa.ai/
Pave / Carta / Compa / Levels.fyi 2026 comp intel stack. Anchor offer at
appropriate percentile for stage + competitiveness. Defend with data, leave
room for one counter (~±5-10% base or +0.25 equity points).
-->
# Offer Negotiation — Comp Band + Equity + Perks — SKILL

Defend the offer with data, model equity scenarios, and close. Pave / Carta / Compa / Levels.fyi / Radford comp intel; equity dilution + vesting + cliff modeling; counter-offer playbook; perks negotiation; never anchor on past salary.

## When to use

- User asks to **build offer comp band**, **defend offer to candidate**, **counter-offer scenario**, **equity model dilution / strike / vesting**, **negotiation talking points**, **percentile anchor by stage**.
- Trigger phrases: "what's the band for X", "candidate is countering", "equity ask", "Pave benchmark", "Levels.fyi check", "Carta total comp", "Compa talking points".

## Setup

```bash
# Pave
export PAVE_API_KEY="xxx"                    # https://www.pave.com/developers
# Carta Total Comp
export CARTA_API_KEY="xxx"                   # https://docs.carta.com/
# Compa AI
export COMPA_API_KEY="xxx"                   # https://www.compa.ai/
# Levels.fyi (free public — via firecrawl)
# Radford (enterprise login + report download — no public API)
```

Comp-band percentile by stage:

| Stage | Base anchor | Equity anchor |
|---|---|---|
| Seed / pre-Series A | 25-50th | Larger grant (1-3% pre-seed founders bias toward equity) |
| Series A-B | 40-65th | Meaningful (0.1-0.5% IC, 0.5-1.5% senior+) |
| Series C+ | 50-75th | Smaller (0.05-0.2% IC, 0.25-0.75% senior+) |
| Late / public | 60-90th | Smallest (RSUs at FMV) |
| Counter / competitive | +10 percentile pts | Or +signing bonus |

## Common recipes

### Recipe 1: Pull Pave benchmark per role × level × geo × stage
```bash
curl -s -G "https://api.pave.com/v1/comp/benchmark" \
  -H "Authorization: Bearer $PAVE_API_KEY" \
  --data-urlencode "role=engineer" \
  --data-urlencode "level=staff" \
  --data-urlencode "geo=san_francisco" \
  --data-urlencode "company_size=200-500" \
  --data-urlencode "data_type=total_comp" \
  | jq '{base: .base_salary, bonus, equity, total_comp}'
# Returns 25/50/75 percentiles for each
```

### Recipe 2: Carta Total Comp benchmark (cap-table-aware)
```bash
curl -s -X POST "https://api.carta.com/v1/companies/<company_id>/comp_benchmarks" \
  -H "Authorization: Bearer $CARTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "role_family":"engineering",
    "level":"staff",
    "geo":"us_remote",
    "include_equity_dilution":true
  }'
```

### Recipe 3: Compa AI — offer talking points + counter prep
```bash
curl -s -X POST "https://api.compa.ai/v1/offer_letters" \
  -H "Authorization: Bearer $COMPA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_name":"Jane Doe",
    "role":"Senior Backend Engineer",
    "base":195000,
    "bonus_pct":10,
    "equity_shares":15000,
    "geo":"sf",
    "company_stage":"series_b",
    "generate":["talking_points","counter_responses","equity_explainer"]
  }'
```

### Recipe 4: Levels.fyi public scrape (firecrawl free fallback)
```bash
firecrawl crawl "https://www.levels.fyi/?compare=Stripe,Brex,Ramp&track=Software%20Engineer" \
  --extract-schema "title,level,base,equity,bonus,location,total_comp"
```

### Recipe 5: Equity grant modeling (Python)
```python
# Model expected value at common outcomes
shares = 15000
strike = 0.50           # for ISO; RSU has no strike
fmv_at_grant = 2.50     # 409A
preferred_per_share = 8.00   # last round price

scenarios = {
  '2x_exit_5yr':       {'exit_per_share': 16, 'dilution': 0.30},
  '5x_exit_5yr':       {'exit_per_share': 40, 'dilution': 0.30},
  '10x_exit_5yr_IPO':  {'exit_per_share': 80, 'dilution': 0.30},
  'no_exit_writedown': {'exit_per_share': 0.50, 'dilution': 0.50},
}

for name, s in scenarios.items():
    shares_after_dilution = shares * (1 - s['dilution'])
    gross = shares_after_dilution * s['exit_per_share']
    strike_cost = shares_after_dilution * strike
    net = gross - strike_cost
    print(f"{name}: ${net:,.0f}")
```

### Recipe 6: Vesting + cliff explainer (Notion template)
```markdown
# Equity Grant Explainer — {candidate}
- **Grant size:** {N} {ISO | NSO | RSU}
- **Strike:** ${strike} (ISO/NSO only; FMV at grant per 409A)
- **Vesting schedule:** 4 years, 1-year cliff
  - Year 1: 25% vests on month 12 anniversary
  - Year 2-4: monthly vest of remaining 75%
- **Total at full vest:** {N} shares
- **Current preferred-per-share (last round):** ${preferred_per_share}
- **Hypothetical valuations:** see scenario modeling
- **Common stock vs preferred:** common (your grant) is subordinate to preferred (investor) — only converts in liquidity event
- **Acceleration:** single-trigger (none); double-trigger (acquisition + termination = vest balance) — standard for most companies
- **Exercise window:** 90 days post-termination standard; some companies extend (e.g., Stripe 10-year)
- **83(b) election:** required within 30 days of grant if early-exercising NSOs / ISOs — defer to legal-counsel + tax advisor
```

### Recipe 7: Counter-offer response playbook
```
Candidate says: "I have a competing offer at $X higher."

Response steps:
1. Acknowledge: "Thanks for being transparent — let me understand the other offer fully."
2. Probe: "Same role + level + comp structure?" Often the comparison is asymmetric.
3. Pull Pave / Levels.fyi (Recipe 1, 4) for that company's stage + level.
4. Validate: ask for written offer letter (decline politely if not provided — many "competing offers" are aspirational).
5. Frame total comp: base + equity + signing + benefits. They may be comparing only base.
6. Decide internal: can we match? close gap? hold firm with non-comp lever?
7. Counter response: one move only ("+5% base or +signing bonus or +equity") — never iterative back-and-forth.

If we can't match: "I understand. Here's our best offer; here's what's behind it. Take your time and let me know."
If we won't match: "We won't go above [band ceiling]; you should take the other if comp is the deciding factor."
```

### Recipe 8: Signing bonus levers
```
Use signing bonus when:
- Counter-offer at a higher base (avoid permanent band creep)
- Candidate forfeits unvested equity at current employer (make whole + 20%)
- Candidate has competing offer with cash-heavy structure

Standard amounts:
- IC: $5K-$25K
- Senior IC: $15K-$50K
- Manager: $25K-$75K
- Director+: $50K-$200K

Repayment clause: 12-24 month proration (defer wording to legal-counsel).
```

### Recipe 9: Perks negotiation — non-comp levers
```
Levers when comp is at ceiling:
- Remote / hybrid flexibility (huge for senior)
- Title escalation (Sr → Staff = ~$10K perceived value)
- Start date flexibility (candidate may want 1-month gap before start)
- Additional vacation (4 weeks vs standard 3)
- Learning budget ($3-5K/yr conference + cert)
- Home office stipend ($2-5K one-time)
- WFH equipment (laptop choice, monitor, chair)
- Sabbatical eligibility (3-month after 4 years)
- Promotion timeline commitment (review in 6 months)
- Reporting line / team / project commitment
```

### Recipe 10: Negotiation transparency principle
```
Always disclose:
- Comp band ceiling for the role + level
- Why we offered at the specific percentile (stage / role / market)
- What's negotiable (always: signing bonus, sometimes: equity, rarely: base above band)
- Decision timeline + path forward
- If decline: future reconnection ask
```

## Examples

### Example 1: Series-B Senior Backend offer — Pave-anchored
**Goal:** Defend $200K base + 0.15% equity + 10% bonus offer; candidate at $215K target.
**Steps:**
1. Pull Pave benchmark (Recipe 1) — Series B + SF + Senior + Engineer: base p50=$195K, p75=$215K.
2. We're offering at p55 base + meaningful equity for stage.
3. Generate Compa talking points (Recipe 3): "Our offer is at the 55th percentile of comp companies; the equity gives material upside at our trajectory (model scenarios)."
4. Carta equity modeling (Recipe 5) — show 5x exit scenario = $X net of strike.
5. Negotiation framing: "We can flex on signing bonus (+$15K) or equity grant (+5K shares); base is at band."

**Result:** Candidate accepts with +$15K signing; relationship clean; no permanent band creep.

### Example 2: Counter-offer scenario
**Goal:** Candidate received $230K offer at competitor; ours is at $200K.
**Steps:**
1. Probe (Recipe 7): same level? same equity? Asymmetric — competitor offered Staff (we offered Senior) at series C company (we're series B).
2. Pull Pave for competitor stage + level (Recipe 1): $215K p50.
3. Validate the competitor offer letter (request it).
4. Decision: can't match at base (band ceiling = $215K for Senior) but can offer Staff title path.
5. Counter: $215K base (band ceiling) + Staff path commitment (6-month review) + +$10K signing.

**Result:** Candidate evaluates trade-off (lower base, higher-stage upside); accepts with logged commitments.

## Edge cases / gotchas

- **Never anchor on candidate's previous salary.** Banned in 20+ states / cities. Pay-equity disaster. Always lead with your band.
- **One counter only.** Iterative negotiation erodes trust + signals we don't know our band.
- **Equity is the most-misunderstood comp axis.** Always model scenarios (Recipe 5). Default to dilution-aware Carta Total Comp.
- **"Competing offer" without paperwork is aspirational.** Politely request the offer letter; most candidates can produce it; those who can't often haven't received one.
- **Signing bonus vs base increase:** signing bonus protects future hires (no band creep); base increase locks in long-term cost. Default to signing for one-time gap closes.
- **Pave / Carta / Compa data quality varies by role × geo.** Senior IC roles in SF / NYC are well-covered; obscure specialties or non-coastal geos may have <20 data points → use Levels.fyi cross-check.
- **Radford data is gold but expensive** ($10K-50K annual). Use when you have comp consultants on staff; overkill for SMB.
- **Levels.fyi is crowdsourced and biased toward Big Tech.** Use as floor not ceiling for non-Big-Tech offers.
- **Equity grant final terms require Board approval.** Offer letter says "we will recommend to Board"; don't promise final terms.
- **83(b) election timing.** 30 days from grant; tax election that defers ordinary income recognition. Defer to candidate's tax advisor; recruiter informs but doesn't advise.
- **ISO vs NSO vs RSU treatment differs.** ISO = preferential tax if held; NSO = ordinary income at exercise; RSU = ordinary income at vest. Don't conflate.
- **Pay-transparency disclosure.** CA SB 1162, CO Equal Pay, NY S9427, WA SB 5761 require comp band in JD + at offer. Comp band cannot be hidden then negotiated.
- **Defer to `legal-counsel`** for: binding equity grant document language, non-compete enforceability, repayment clause wording, 409A valuation timing, tax election advisory.
- **Defer to `ceo-agent`** for: comp philosophy + band-setting + above-band exceptions for strategic hires.

## Sources

- [Pave — Total Comp Benchmarks](https://pave.com/product/total-comp)
- [Pave Developer Docs](https://www.pave.com/developers)
- [Carta — Equity + Total Compensation](https://carta.com/learn/equity/)
- [Compa AI — Compensation Communication](https://www.compa.ai/)
- [Levels.fyi](https://www.levels.fyi/)
- [Radford McLagan (Aon)](https://radford.aon.com/)
- [Secfi — Equity Modeling](https://www.secfi.com/)
- [SHRM — Pay Transparency Laws by State](https://www.shrm.org/topics-tools/employment-law-compliance/pay-transparency-laws-state)
