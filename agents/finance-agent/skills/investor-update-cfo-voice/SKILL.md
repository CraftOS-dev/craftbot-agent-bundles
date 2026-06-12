<!--
Source: https://visible.vc/templates/the-visible-standard-investor-update-template/
Source: https://visible.vc/product/updates/
Source: https://visible.vc/blog/docsend-vs-visible-comparison/
Reference role.md: "Investor update CFO voice playbook"
-->

# Investor update — CFO voice (distinct from CEO voice)

CFO-authoritative version of monthly / quarterly investor update. Visible.vc Standard template (most-used 2026); YC variant for YC-backed. CFO voice = financials-led; conservative on revenue, aggressive on COGS surfacing; lead with cash + runway. Distinct from CEO update (vision + narrative + asks). Cadence: monthly during active raise / pre-A; quarterly for steady-state / Series B+.

## When to use

- Monthly / quarterly recurring investor update.
- LP communication for fund-stage updates.
- Active fundraise — keep all investors warm via consistent cadence.
- Bridge round prep — established pattern of transparent updates.
- Trigger phrases: "investor update", "monthly update", "Visible.vc update", "CFO update", "LP update".

NOT for: pitch deck (use `pitch-deck-financial-slides`); board package (use `board-cfo-financial-package`).

## Setup

```bash
# Visible.vc (free Starter tier — up to 100 investor recipients)
export VISIBLE_API_KEY="<from Visible Settings>"

# Gmail / Outlook for direct send fallback
export GMAIL_API_KEY="<from Google Cloud Console>"
```

## The Visible Standard structure

```
SECTION 1 — Highlights (3-4 bullets)
  Headline financial + product + commercial milestones
  Lead with metrics (CFO voice)

SECTION 2 — Lowlights (2-3 bullets)
  Be honest. What didn't go well? Why? What are you doing about it?
  Critical for trust; investors penalize hiding negatives more than the negatives themselves.

SECTION 3 — Financial Update (CFO core)
  Cash, runway, ARR/Revenue, NRR, key efficiency metrics
  Plan vs Actual variance > 10% explained
  Forward guidance if comfortable (conservatism prevails)

SECTION 4 — Product / GTM Update
  Key shipments
  Customer milestones (logos, expansion)
  Hiring updates

SECTION 5 — Asks
  Specific, time-bound, named.
  "Need intros to [X type of buyer]."
  "Looking for advisor in [Y domain]."
  "Reviewing options for [Z service category]."
  Empty asks = closed loop. Always have 1-2.

SECTION 6 — KPI Table
  Optional but recommended.
  6-9 metrics × current + MoM + YoY + benchmark.

SECTION 7 — Closing
  Thanks + next-update date + reply CTA
```

## CFO vs CEO voice (split labor)

```
CEO VOICE                    CFO VOICE
─────────────────────────────────────────────────────────────────
Vision-led                   Metrics-led
Narrative arc                Numbers + variance
Aspirational                 Conservative
Product / Market focus       Cash / Runway / Unit econ focus
External wins (PR)           Internal efficiency
Hiring senior leaders        Comp / equity / headcount efficiency
"What we believe"            "What we measured"
Asks: customers, talent      Asks: introductions to debt/RBF, treasury providers, M&A advisors
```

Many investor updates fail because the CEO writes it alone — too vision-heavy, light on numbers. The CFO voice version (this skill) leads with finance and grounds the narrative.

## Common recipes

### Recipe 1 — Visible.vc CFO update template

```markdown
# Acme Inc. — June 2026 Investor Update

> CFO Update — written by [CFO name], finance-led perspective
> *(CEO update follows separately; see attached or earlier email)*

## Highlights

- **ARR $4.2M (+5.2% MoM, +83% YoY)** — tracking to $5.0M EoQ3.
- **NRR 118%** — driven by mid-market expansion + one Enterprise tier upgrade.
- **Gross Margin 78.5%** — improved 30bps on hosting renegotiation.
- **Cash $8.5M, runway 20 months** at current $420K monthly burn.

## Lowlights

- **Burn ticked up $40K/mo** (engineering hiring); planned but worth noting.
- **One mid-market customer (3% of ARR) churned** to in-house build.
- **Customer concentration:** top-3 = 28% of ARR; one renewal Q3 watching.

## Financial Update — Q2 2026 Plan vs Actual

| Metric          | Q2 Plan  | Q2 Actual | Variance | Status |
|-----------------|----------|-----------|----------|--------|
| Revenue         | $3.15M   | $3.29M    | +4.4%    | ahead  |
| Gross Margin    | 78%      | 78.5%     | +0.5pp   | ahead  |
| S&M Spend       | $1.32M   | $1.24M    | -6.1%    | under  |
| R&D Spend       | $870K    | $915K     | +5.2%    | over   |
| EBITDA          | -$75K    | +$57K     | beat     | ahead  |

**Variance commentary:** Revenue beat from earlier-than-expected enterprise renewal expansion.
S&M under-spend = paused on under-performing channel mid-Q (decision made April).
R&D over = 2 senior engineers hired ahead of plan; productivity ramp on track.

## Product / GTM

- Shipped: AI assistant feature (used by 24% of customers in first 3 weeks).
- Customers added: Acme Bank ($120K ACV), Beta Corp ($85K).
- Hires: 2 Senior Engineers, 1 Director of Customer Success.

## Asks

1. **Introductions to Series B leads** — meeting 5 funds in Sep; appreciate warm intros to Tier-1 VCs focused on AI-finance.
2. **Venture debt advisor** — exploring $3M venture debt to extend runway; intros to Founderpath / Lighter Capital welcome.
3. **CRO candidates** — sourcing for CRO hire end of Q3.

## KPI Snapshot

| KPI            | Current | MoM    | YoY    | Benchmark      |
|----------------|---------|--------|--------|----------------|
| ARR            | $4.2M   | +5.2%  | +83%   | —              |
| NRR            | 118%    | -1pp   | +8pp   | ≥100% healthy  |
| CAC Payback    | 14mo    | -1mo   | -3mo   | <18mo healthy  |
| LTV:CAC        | 4.2:1   | +0.3   | +0.8   | ≥3:1 healthy   |
| Gross Margin   | 78.5%   | +0.3pp | +2.1pp | ≥75% healthy   |
| Rule of 40     | 58      | +3     | +12    | ≥40 healthy    |
| Burn Multiple  | 1.35x   | -0.10  | -0.40  | <1.5 healthy   |
| Runway (mo)    | 20      | -1     | -7     | ≥24 target     |

---

Next update: July 31, 2026. Reply to this email or message [name] directly. Thanks for being part of the journey.

— [CFO Name]
```

### Recipe 2 — Visible.vc API send

```bash
# Create update
curl -X POST "https://api.visible.vc/v1/updates" \
  -H "Authorization: Bearer $VISIBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Acme Inc. — June 2026 Update",
    "content": "<markdown content here>",
    "template_id": "standard_investor_update"
  }'

# Add metrics to update
curl -X POST "https://api.visible.vc/v1/updates/$UPDATE_ID/metrics" \
  -H "Authorization: Bearer $VISIBLE_API_KEY" \
  -d '{"metric": "ARR", "value": 4200000, "period": "2026-06"}'

# Send to investor list
curl -X POST "https://api.visible.vc/v1/updates/$UPDATE_ID/send" \
  -H "Authorization: Bearer $VISIBLE_API_KEY" \
  -d '{"investor_list_id": "INVESTOR_LIST_ID"}'
```

### Recipe 3 — Engagement tracking + follow-up

```python
import requests

def engagement_summary(api_key, update_id):
    r = requests.get(f"https://api.visible.vc/v1/updates/{update_id}/engagement",
                     headers={"Authorization": f"Bearer {api_key}"})
    data = r.json()
    return {
        "opens": data.get("opens", 0),
        "click_throughs": data.get("clicks", 0),
        "by_investor": data.get("investor_breakdown", []),
    }
```

### Recipe 4 — Monthly metric pack auto-populate

```python
def populate_metrics(visible_update_id, metric_dict):
    """Auto-populate metrics from internal source."""
    import requests
    for metric, value in metric_dict.items():
        requests.post(
            f"https://api.visible.vc/v1/updates/{visible_update_id}/metrics",
            headers={"Authorization": f"Bearer {VISIBLE_API_KEY}"},
            json={"metric": metric, "value": value, "period": "2026-06"}
        )
```

### Recipe 5 — Variance commentary auto-generator

```python
def variance_commentary(plan, actual, threshold_pct=0.10):
    out = []
    for metric, p in plan.items():
        a = actual.get(metric, 0)
        var_pct = (a - p) / p if p else 0
        if abs(var_pct) > threshold_pct:
            direction = "beat" if var_pct > 0 else "missed"
            sign = "+" if var_pct > 0 else ""
            out.append(f"- **{metric}:** {direction} plan by {sign}{var_pct:.1%}; reason: [explain]")
    return "\n".join(out) if out else "No material variances (>10% threshold)."

plan = {"Revenue": 1_050_000, "GM_pct": 0.78, "EBITDA": -25_000}
actual = {"Revenue": 1_220_000, "GM_pct": 0.785, "EBITDA": 19_000}
print(variance_commentary(plan, actual))
```

### Recipe 6 — Asks generator

```python
ASKS_LIBRARY = {
    "fundraise": "Introductions to [stage] funds focused on [sector]",
    "venture_debt": "Venture debt advisor intros (Founderpath / Lighter / Hercules)",
    "rbf": "RBF advisor intros (Capchase / Pipe / Wayflyer for e-com)",
    "treasury": "Treasury provider advisors (Rho / Public.com / Mercury Treasury)",
    "hire_cro": "CRO candidates for [type of motion]",
    "hire_cfo": "CFO candidates for [stage]",
    "hire_engineering": "Senior Engineering hires (mention specific role)",
    "customers": "Customer intros to [type of buyer at type of company]",
    "advisors": "Advisor for [specific domain expertise]",
    "comp_data": "Comp benchmarking source recommendations",
    "tax_planning": "Tax planning attorney for QSBS strategy",
    "ma_targets": "Strategic M&A targets in [adjacent space]",
}

def generate_asks(focus_areas):
    return [{"ask": ASKS_LIBRARY[area]} for area in focus_areas if area in ASKS_LIBRARY]

print(generate_asks(["fundraise", "venture_debt", "hire_cro"]))
```

### Recipe 7 — Cadence schedule

```
Stage / Situation             Cadence       Format            Channel
─────────────────────────────────────────────────────────────────────────
Pre-seed / Seed (raising)     Monthly       Visible.vc        Email + portal
Series A (steady)             Quarterly     Visible.vc        Email + portal
Series A (raising B)          Monthly       Visible.vc        Email + portal
Series B+ (steady)            Quarterly     Visible.vc        Email + portal
Series B+ (raising C)         Monthly       Visible.vc        Email + portal
Pre-IPO                       Quarterly     Carta IR / private Quiet period
Public                        Quarterly     SEC + earnings    Public filing
─────────────────────────────────────────────────────────────────────────
```

### Recipe 8 — Pre-write template seeding

```python
def seed_update_from_close(close_output):
    """Pre-populate Section 1 (Highlights) from monthly close output."""
    arr = close_output["arr"]
    arr_mom = close_output["arr_mom_pct"]
    arr_yoy = close_output["arr_yoy_pct"]
    nrr = close_output["nrr"]
    gm = close_output["gross_margin"]
    runway = close_output["runway_months"]
    cash = close_output["cash"]

    return f"""
- **ARR ${arr/1e6:.1f}M ({arr_mom:+.1%} MoM, {arr_yoy:+.1%} YoY)**
- **NRR {nrr:.0%}**
- **Gross Margin {gm:.1%}**
- **Cash ${cash/1e6:.1f}M, runway {runway} months**
"""
```

## Examples

### Example 1: Monthly update (active fundraise)

**Goal:** Visible.vc Standard CFO-voice update.

**Steps:**
1. Recipe 8 → seed Highlights from monthly close.
2. Manually populate Lowlights + Asks.
3. Recipe 5 → auto-generate variance commentary.
4. Recipe 6 → asks list.
5. Recipe 1 → assemble markdown.
6. Recipe 2 → post to Visible.vc; send to investor list.
7. Recipe 3 → engagement tracking; follow up with high-engagers within 48h.

**Result:** Investor-pack-ready in 30-45 minutes.

### Example 2: Steady-state quarterly

**Goal:** Quarterly update; less detail than monthly during raise.

**Steps:**
1. Use Recipe 1 template; expand financial section (quarterly P&L + variance).
2. Skip month-level granularity.
3. Heavier asks (since less frequent).
4. Add forward 3-month guidance.

**Result:** Quarterly cadence; high signal-to-noise.

## Edge cases / gotchas

- **Don't only lead with wins.** Hiding lowlights = trust killer. Visible Standard explicitly requires lowlights section.
- **Forward guidance is risky if you miss it.** Conservative > aspirational. Be CFO-careful.
- **Empty asks = closed loop.** Always have at least 1-2; investors want to be useful.
- **CEO + CFO voices should align.** If CEO says "we're killing it" and CFO says "burn rate concern" → mixed signals. Reconcile pre-send.
- **Don't update on bad news only.** Even if quarter is hard, maintain cadence. Skipping = signal of distress.
- **Investor segmentation.** Lead investors get more detail; angels can have lighter version. Visible.vc segments.
- **NDA on financials.** Most investor updates assume NDA; if not, sanitize customer names + ARR specifics.
- **Quiet period for pre-IPO.** Stop public-facing updates 30+ days before S-1 effectiveness.
- **Lockup period for public.** Earnings + SEC filings only; private CFO-voice updates discontinue.
- **Visible.vc engagement spying.** Investors know they're tracked. Some prefer DocSend-style stealth.
- **One-pager alt.** Some investors prefer 1-page summary + linked details. Recipe 1 is verbose; condense for these.
- **Foreign investors.** Translate currency context; explain US-centric metrics.

> ⚠ **This is informational guidance from an AI agent. Always consult a licensed CFO, CPA, or qualified investment advisor before making binding strategic-finance decisions.**

## Sources

- Visible.vc Standard template: https://visible.vc/templates/the-visible-standard-investor-update-template/
- Visible.vc Updates product: https://visible.vc/product/updates/
- Visible vs DocSend: https://visible.vc/blog/docsend-vs-visible-comparison/
- Visible.vc API: https://visible.vc/developers
- YC investor update template: https://www.ycombinator.com/library/4F-monthly-investor-updates
- Foundersuite investor CRM: https://foundersuite.com/

## Related skills

- `pitch-deck-financial-slides` — content for first pitch; recurring updates use this skill.
- `investor-data-room-curation` — hosts updates archive.
- `board-cfo-financial-package` — internal version of CFO voice.
- `three-statement-financial-model-tied` — financial section source.
- `driver-based-revenue-modeling` — KPI metric source.
