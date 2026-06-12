<!--
Source: https://www.alpha-sense.com/blog/guidance-best-practices/
Source: https://corporate.factset.com/insights/consensus-estimates
Source: https://www.sentieo.com/blog/guidance-philosophy/
Source: https://www.refinitiv.com/en/financial-data/company-data/i-b-e-s-estimates
Reference role.md: "Guidance setting playbook"
Round 2 enrichment: full consensus-pull-and-compare + range vs point decision tree + beat-and-raise cadence + pre-guidance straw poll + counsel Safe Harbor checklist.
-->

# Guidance setting (range vs point; consensus-grounded)

Sets quarterly + annual guidance for public companies. Pulls sell-side consensus via FactSet / Refinitiv / AlphaSense; cross-references `finance-agent` internal forecast; decides range vs point; runs pre-guidance straw poll of top 3-5 analysts (Reg FD-bounded); coordinates Safe Harbor language with counsel. 2026 philosophy: under-promise + over-deliver; beat-and-raise > miss-and-cut.

## When to use

- Setting next-quarter + full-year guidance pre-earnings.
- Annual full-year guidance issuance on Q4 call.
- Mid-quarter guidance revision (rare; requires 8-K Item 7.01 Reg FD).
- Long-range guidance (3-year framework) at investor day.
- Trigger phrases: "set guidance", "guide", "guidance recommendation", "consensus comparison", "range vs point guide", "beat-and-raise design".

NOT for: earnings press release wire (use `quarterly-earnings-press-release`); financial modeling (use `finance-agent`); 8-K mid-quarter guidance revision (use `8k-event-reporting`); investor day long-range plan presentation (use `investor-day-capital-markets-day`).

## Setup

```bash
# Consensus research (paywalled; recipient supplies one)
export FACTSET_API_KEY="<from FactSet Workstation>"      # $24K+/yr/seat
export REFINITIV_API_KEY="<from Refinitiv Workspace>"    # $22K+/yr
export ALPHASENSE_API_KEY="<from AlphaSense Admin>"      # $20K+/yr
export BLOOMBERG_BEST_API_KEY="<from BBG Terminal>"      # via BPIPE

# Free fallback: Yahoo Finance + sec-edgar-mcp for analyst PT history
# (lower fidelity; usable for small cap)

# Tools: xlsx for consensus comparison; cli-anything for REST pulls
```

Auth / API key requirements:
- One consensus vendor (recipient picks).
- Free fallback: Yahoo Finance + Bloomberg ANR (slower; coarser).

Data inputs:
- `finance-agent` internal forecast (range, drivers, sensitivity).
- Consensus snapshot (mean, median, high, low, stdev; # of analysts).
- Each individual analyst's published model (FactSet "by-analyst" view).
- Prior 4 quarters' own guidance vs actual (history of beat/miss/raise/cut).
- Peer guidance philosophies (point vs range; cadence; tone).
- Macro indicators (Fed funds, sector indexes, FX) for sensitivity.

## Decision tree (range vs point)

```
Volatility on metric (next-Q) >±3% revenue / ±5% EPS?
  Yes -> RANGE
  No  -> POINT or NARROW RANGE

Visibility on backlog / pipeline >65% of Q?
  Yes -> tighter (POINT or NARROW)
  No  -> wider (RANGE)

Macro / FX exposure material (>15% of revenue)?
  Yes -> wider (RANGE)
  No  -> POINT acceptable

First-year-of-guidance precedent?
  Yes -> wider (RANGE; build trust before narrowing)

Stage (early growth -> mature):
  Early growth: RANGE wide
  Steady-state: NARROW or POINT
  Mature with backlog visibility: POINT
```

## Beat-and-raise cadence

| Scenario | Action |
|----------|--------|
| Q-1 set conservatively (60-70% confidence at low end) | Set range; communicate "based on visibility..." |
| Q-0 beat 2-5% on revenue | Raise FY by half the beat |
| Q-0 beat 5%+ on revenue | Consider raising whole-year by full beat |
| Q-0 in-line | Reaffirm FY |
| Q-0 miss | Lower guidance immediately + name reasons (NEVER claim "one-time" without rigor) |
| Mid-quarter material shift | 8-K Item 7.01 Reg FD revision + counsel-supervised |

## Pre-guidance straw poll (Reg FD-bounded)

- Top 3-5 analysts (highest influence) — brief 1:1 ~10 days pre-earnings.
- "If we land at $X / $Y / $Z, what's the model reaction?" — DIRECTIONAL only.
- **NEVER** confirm or hint actual landing.
- **NEVER** preview an internal number.
- Counsel sign-off on line of questioning each cycle.
- Document each call in `notion-mcp` for Reg FD audit trail.

## Common recipes

### Recipe 1 — Pull FactSet consensus
```bash
curl -H "Authorization: Bearer $FACTSET_API_KEY" \
  "https://api.factset.com/v1/consensus?ticker=$TICKER&period=Q+1&fields=revenue,eps_adj,op_inc"
# Returns: mean / median / high / low / stdev / # analysts
```

### Recipe 2 — Pull Refinitiv I/B/E/S consensus
```bash
curl -H "Authorization: Bearer $REFINITIV_API_KEY" \
  "https://api.refinitiv.com/data/v1/financial/estimates/$TICKER?period=Q1"
```

### Recipe 3 — Pull individual-analyst breakouts
```bash
curl -H "Authorization: Bearer $FACTSET_API_KEY" \
  "https://api.factset.com/v1/consensus/by_analyst?ticker=$TICKER&period=Q+1"
# Identifies outliers (high + low); analyst names visible
```

### Recipe 4 — Build consensus comparison sheet (xlsx)
```python
import pandas as pd

df = pd.DataFrame({
    "Metric": ["Revenue", "Op Inc", "EPS (adj)"],
    "Consensus Mean": [1050, 252, 1.78],
    "Consensus Median": [1048, 250, 1.79],
    "High": [1080, 268, 1.85],
    "Low": [1020, 240, 1.72],
    "StDev": [15, 7, 0.03],
    "# Analysts": [12, 12, 12],
    "Internal Mean": [1062, 260, 1.81],
    "Internal Low": [1045, 250, 1.76],
    "Internal High": [1078, 270, 1.86],
})
df.to_excel("consensus_comparison_Q3_2026.xlsx")
```

### Recipe 5 — Peer guidance philosophy mining
```bash
curl -H "Authorization: Bearer $ALPHASENSE_API_KEY" \
  "https://api.alpha-sense.com/v1/search?q=\"guidance\"+OR+\"outlook\"+$PEER_TICKERS&doc_type=transcript&limit=10"
```

### Recipe 6 — Pre-guidance straw-poll script (Reg FD safe)
```
SCRIPT (counsel-reviewed):
"I'm not previewing our number — we'll share it on the call. But I want to
test your framework. If we landed at <consensus mid> with <stable margin>,
how would your model react? At <consensus high>? At <consensus low>?
What's your confidence interval on the Q-1 mid?"

NEVER: confirm a specific number is the landing
NEVER: hint at direction (beat/miss)
DOCUMENT: timestamp + name + script-followed flag in notion-mcp
```

### Recipe 7 — Sensitivity table for guidance range
```python
# Sensitivity: revenue x margin x FX -> guidance bracket
SENSITIVITIES = {
    "FX": {"-3%": -8, "0%": 0, "+3%": +7},
    "Macro PMI": {"<50": -15, "50-52": 0, ">52": +12},
    "Backlog conversion": {"60%": -20, "70%": 0, "80%": +18},
}
# Roll up to range; should match published guidance high/low
```

### Recipe 8 — Long-range (3-year) framework (investor day)
```
Standard 3-year framework structure:
- Revenue CAGR (15-25% growth co; 5-10% mature)
- Gross margin trajectory (steady or improving 100-300 bps)
- Operating margin expansion (200-400 bps)
- Free cash flow conversion (75-90%)
- Capital allocation framework (M&A / buyback / dividend split)
- ROIC target

Long-range framework != quarterly guidance; framed as ambition + framework
```

### Recipe 9 — Counsel Safe Harbor coverage check
```python
SAFE_HARBOR_CHECKLIST = [
    "Each forward-looking statement identified",
    "Safe Harbor reference in press release",
    "Risk Factors cross-ref to most recent 10-K",
    "Specific forward statements 'reasonable basis' documented",
    "No omitted material assumption",
    "No specific named external event (e.g., 'when rates cut') unless backed",
]
# Counsel signs each quarter; document in notion-mcp
```

### Recipe 10 — Mid-quarter guidance revision (8-K Item 7.01)
```python
# Triggers: material adverse condition; material favorable surprise
# Mechanics: counsel review materiality determination; if material:
# - 8-K Item 7.01 same-day or next-day
# - Press release simultaneously
# - Conference call optional (depends on magnitude)
# Coordinates with `8k-event-reporting` skill
```

## Examples

### Example 1: Beat-and-raise Q3 prep (steady-state SaaS)

**Goal:** Q2 closed; expected Q3 revenue $1.06B, $80M above consensus mid ($980M).

**Steps:**
1. Pull consensus (Recipe 1) — Q3 revenue mean $980M, range $960-$1.0B.
2. Pull by-analyst (Recipe 3) — high outlier $1.02B (one analyst); rest cluster $975-$985M.
3. Build comparison sheet (Recipe 4).
4. `finance-agent` internal: $1.05-1.07B with 75% confidence at $1.06B.
5. Decision: RANGE $1.04-1.07B (40 bps above high analyst); reflects beat-and-raise cadence.
6. Pre-guidance straw poll (Recipe 6) with top 4 analysts; confirm $1.04-1.07B above all models.
7. Counsel Safe Harbor review (Recipe 9).
8. Set in `quarterly-earnings-press-release` guidance table.

**Result:** Beat-and-raise signal sent cleanly; stock +4% post-release; PT raises within 5 days.

### Example 2: Miss + lower guidance (macro headwind)

**Goal:** Q2 actual revenue $980M vs guidance $1.00-1.03B; macro weakness identified.

**Steps:**
1. Identify miss factors (Recipe 7) — FX -2%, PMI <50, deal slip $20M.
2. `finance-agent` revises Q3 forecast and FY.
3. Lower Q3 guidance to $940-970M (was $1.00B mid).
4. Lower FY to $3.95-4.05B (was $4.10-4.20B).
5. Counsel review of "reason" narrative — NO "one-time" claim without rigor.
6. Press release leads with the miss + lowered guidance + framework for recovery.
7. CFO call script emphasizes capital discipline + visibility into Q4.

**Result:** Stock -8% on day but no "credibility broken" analyst commentary; trust preserved.

### Example 3: First-year guidance (recent IPO)

**Goal:** First post-IPO earnings; need to set initial Q1 + FY guidance.

**Steps:**
1. No own consensus history; pull peer guidance ranges (Recipe 5).
2. `finance-agent` internal: 70% confidence at FY range mid.
3. Decision: WIDE RANGE (build trust; never miss in year 1).
4. Pre-guidance straw poll w/ post-IPO analyst initiations (Recipe 6).
5. Counsel Safe Harbor — extra-careful first cycle.
6. Issue WIDE range; commit to narrowing over time as visibility builds.

**Result:** Conservative bar; beat Q1 cleanly; narrowed FY range Q2.

## Edge cases / gotchas

- **Reg FD straw poll trap.** "If you land at X..." sounds neutral but if combined with prior context could be selective MNPI. Counsel review each cycle.
- **Beat-and-raise inflation.** Continual raises without backing erode credibility; only raise when visibility supports.
- **One-time miss narrative.** "One-time" only valid when truly non-recurring (M&A, restructuring, regulatory); never use for macro softness.
- **Long-range vs quarterly conflation.** Investor day long-range framework is ambition; quarterly guide is commitment. Mixing erodes both.
- **FactSet vs Refinitiv vs Bloomberg consensus difference.** Different vendors aggregate differently; pick one + state clearly.
- **Stale consensus.** Consensus updates 24-48h post-event; pull within 5 days of earnings.
- **Analyst outlier weighting.** One analyst $50M above all others = ignore or named (don't average them in equally).
- **Currency translation.** Multinational guidance needs FX assumption disclosed.
- **Backlog visibility seasonality.** Q4 closes-bias means Q4 guidance can be tighter than Q1; communicate cadence.
- **Mid-quarter revision threshold.** Materiality is counsel-driven; not all macro changes trigger.
- **Investor day framework slippage.** If 3-year framework set and missed in year 1, next investor day must address.
- **Pre-guidance pull timing.** Pulls T-10 to T-5 to capture stable view; pulling T-1 captures pre-print volatility.
- **Yahoo Finance consensus quality.** Acceptable for small cap (<$1B) but coarse; institutional bar = FactSet/Refinitiv.

> Mandatory disclaimer: Guidance is a forward-looking statement subject to the Private Securities Litigation Reform Act Safe Harbor + Reg G + Reg FD. **Consult licensed securities counsel** for binding Safe Harbor language, forward-looking statement coverage, mid-quarter revision materiality determinations, and Reg FD interpretation around pre-guidance analyst engagement. This skill drafts guidance recommendations; counsel + CFO + audit committee approve binding issuance.

## Sources

- AlphaSense Guidance Best Practices: https://www.alpha-sense.com/blog/guidance-best-practices/
- FactSet Consensus Estimates: https://corporate.factset.com/insights/consensus-estimates
- Refinitiv I/B/E/S Estimates: https://www.refinitiv.com/en/financial-data/company-data/i-b-e-s-estimates
- Sentieo Guidance Philosophy: https://www.sentieo.com/blog/guidance-philosophy/
- SEC Regulation FD: https://www.sec.gov/divisions/corpfin/guidance/regfd-interp.htm
- Private Securities Litigation Reform Act (Safe Harbor): https://www.congress.gov/bill/104th-congress/house-bill/1058
- See `role.md` -> "Guidance setting playbook"

## Related skills

- `quarterly-earnings-press-release` — guidance table publication.
- `earnings-call-script-qa` — guidance narrative on call.
- `equity-analyst-relations-briefings` — straw poll context.
- `8k-event-reporting` — mid-quarter revision Item 7.01.
- `investor-day-capital-markets-day` — long-range framework venue.
