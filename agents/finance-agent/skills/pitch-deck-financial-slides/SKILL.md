<!--
Source: https://waveup.com/blog/financial-projections-slide/
Source: https://ltse.com/insights/the-metrics-that-should-be-in-your-pitch-deck
Source: https://www.spectup.com/resource-hub/pitch-deck-financials-slide
Reference role.md: "Pitch deck financials playbook"
-->

# Pitch deck financial slides — 6-metric max

Designs the financial slides that survive Series A/B/C diligence. 2026 standard: max 6 metrics; story arc = growth (top) → unit economics (middle) → path to profit (bottom). 3-5 year projections; label actuals vs projections explicitly. "Growth at all costs" is dead — show profitability path. Pre-seed: revenue + margins, 1 slide. Seed: full unit economics. Series A+: cohort retention + NRR + CAC payback prominent.

## When to use

- Pre-seed / seed / Series A/B/C pitch deck financials slide(s).
- Investor update appendix.
- Board deck financial slides.
- Internal "where we are" snapshot for leadership.
- Trigger phrases: "pitch deck financials", "financial slide", "metrics slide", "deck financials", "investor deck financials".

NOT for: full model (use `three-statement-financial-model-tied`); board CFO package (use `board-cfo-financial-package`).

## Setup

```bash
uvx --with python-pptx --with matplotlib --with pandas python -c "import pptx, matplotlib, pandas"
```

## The 6-metric framework (max!)

```
SaaS Series A+:
  1. ARR (current) + ARR growth trajectory (last 12mo + projection)
  2. NRR / Net Dollar Retention
  3. CAC Payback (months)
  4. LTV:CAC ratio
  5. Gross Margin %
  6. Rule of 40 OR Burn Multiple

E-commerce / DTC:
  1. Revenue (current) + growth trajectory
  2. Contribution margin (after COGS + variable S&M)
  3. Repeat purchase rate / cohort retention
  4. CAC + LTV by channel
  5. Inventory turn / cash conversion cycle
  6. EBITDA margin

Marketplace:
  1. GMV + growth trajectory
  2. Take rate (net revenue / GMV)
  3. Active buyers / sellers + retention
  4. CAC + LTV per side
  5. Liquidity ratio (matched orders / listings)
  6. EBITDA margin
```

## Slide structure (2-3 slides max)

```
SLIDE 1 — TRACTION (current state + trajectory)
  Top half: ARR / Revenue chart (last 12mo actual + 3-5yr projection)
  Bottom half: Logo / Customer count chart
  Annotations: Closed-won milestones, key inflection points

SLIDE 2 — UNIT ECONOMICS (efficiency)
  4-up tile: CAC Payback / LTV:CAC / NRR / Gross Margin
  Each tile: number + trend arrow + benchmark line
  Footer note: Methodology link (data room file ref)

SLIDE 3 — PATH TO PROFITABILITY (financial picture)
  Stacked area: Revenue (top), then Gross Profit, Opex, EBITDA
  Annotation: "Cash flow breakeven projected $XM ARR by [date]"
  Right column: Plan vs Actual variance last 4 quarters
```

## Common recipes

### Recipe 1 — Generate ARR / Revenue chart (matplotlib)

```python
import matplotlib.pyplot as plt
import pandas as pd

def arr_chart(historical_df, projection_df, save="arr_chart.png"):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(historical_df["month"], historical_df["arr"]/1e6, color="#1f77b4", linewidth=2.5, label="Actual")
    ax.plot(projection_df["month"], projection_df["arr"]/1e6, color="#1f77b4", linewidth=2.5, linestyle="--", label="Projection")
    ax.fill_between(projection_df["month"], projection_df["arr_lower"]/1e6, projection_df["arr_upper"]/1e6,
                    alpha=0.15, color="#1f77b4")
    ax.set_ylabel("ARR ($M)")
    ax.set_title("ARR Growth — Actual + 36mo Projection")
    ax.legend(); ax.grid(alpha=0.3)
    plt.tight_layout(); plt.savefig(save, dpi=200)
    return save
```

### Recipe 2 — 4-up unit-econ tile chart

```python
def unit_econ_tiles(metrics, save="unit_econ.png"):
    """metrics: dict of {name: {value, benchmark, trend}}"""
    fig, axes = plt.subplots(1, 4, figsize=(14, 4))
    for i, (name, m) in enumerate(metrics.items()):
        ax = axes[i]
        ax.text(0.5, 0.65, f"{m['value']}", ha="center", fontsize=36, fontweight="bold", transform=ax.transAxes)
        ax.text(0.5, 0.45, name, ha="center", fontsize=14, transform=ax.transAxes)
        ax.text(0.5, 0.25, f"Benchmark: {m['benchmark']}", ha="center", fontsize=10, color="gray", transform=ax.transAxes)
        ax.text(0.5, 0.10, m["trend"], ha="center", fontsize=12,
                color="green" if "↑" in m["trend"] else "red", transform=ax.transAxes)
        ax.axis("off")
    plt.tight_layout(); plt.savefig(save, dpi=200)
    return save

unit_econ_tiles({
    "CAC Payback": {"value": "14mo", "benchmark": "<18mo", "trend": "↓3mo YoY ✓"},
    "LTV:CAC":     {"value": "4.2:1", "benchmark": "≥3:1", "trend": "↑0.8 YoY ✓"},
    "NRR":         {"value": "118%", "benchmark": "≥100%", "trend": "↑8pp YoY ✓"},
    "Gross Margin":{"value": "78%",  "benchmark": "≥75%", "trend": "↑2pp YoY ✓"},
})
```

### Recipe 3 — Path to profitability chart (stacked area)

```python
def path_to_profit_chart(df, save="path_to_profit.png"):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.fill_between(df["month"], 0, df["revenue"]/1e6, label="Revenue", alpha=0.7)
    ax.fill_between(df["month"], 0, df["gross_profit"]/1e6, label="Gross Profit", alpha=0.5, color="green")
    ax.plot(df["month"], df["opex"]/1e6, label="OpEx", color="red", linestyle="--", linewidth=2)
    ax.plot(df["month"], df["ebitda"]/1e6, label="EBITDA", color="black", linewidth=2.5)
    ax.axhline(0, color="gray", linewidth=0.5)
    ax.set_ylabel("$M")
    breakeven = df[df["ebitda"] >= 0].head(1)
    if not breakeven.empty:
        bm = breakeven.iloc[0]["month"]
        ax.axvline(bm, color="green", linestyle=":", alpha=0.5)
        ax.text(bm, df["ebitda"].max()/1e6*0.8, f"Breakeven {bm}", ha="left")
    ax.legend(); ax.grid(alpha=0.3)
    plt.tight_layout(); plt.savefig(save, dpi=200)
    return save
```

### Recipe 4 — Generate PPTX slides

```python
from pptx import Presentation
from pptx.util import Inches, Pt

def build_pitch_financials_pptx(save="financials.pptx", arr_img="arr_chart.png",
                                  unit_img="unit_econ.png", profit_img="path_to_profit.png"):
    prs = Presentation()
    prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)

    # Slide 1 — ARR
    s = prs.slides.add_slide(prs.slide_layouts[5])
    s.shapes.title.text = "Traction — ARR + 36mo projection"
    s.shapes.add_picture(arr_img, Inches(1), Inches(1.4), width=Inches(11.3))

    # Slide 2 — Unit econ
    s = prs.slides.add_slide(prs.slide_layouts[5])
    s.shapes.title.text = "Unit Economics — 4 metrics that matter"
    s.shapes.add_picture(unit_img, Inches(0.5), Inches(2), width=Inches(12.3))

    # Slide 3 — Path to profit
    s = prs.slides.add_slide(prs.slide_layouts[5])
    s.shapes.title.text = "Path to Profitability"
    s.shapes.add_picture(profit_img, Inches(1), Inches(1.4), width=Inches(11.3))

    prs.save(save)
    return save
```

### Recipe 5 — Stage-graded benchmark overlay

```python
STAGE_BENCHMARKS = {
    "Seed":      {"NRR": "90-100%", "GM": "65-75%",  "Rule of 40": "growth-only", "Burn Mult": "2.0-3.0"},
    "Series A":  {"NRR": "100-110%", "GM": "70-78%", "Rule of 40": "25-40",       "Burn Mult": "1.5-2.0"},
    "Series B":  {"NRR": "110-120%", "GM": "75-80%", "Rule of 40": "40-50",       "Burn Mult": "1.0-1.5"},
    "Series C+": {"NRR": "115-125%+","GM": "78-82%", "Rule of 40": "50-60",       "Burn Mult": "<1.0"},
}

def benchmark_for(stage, metric):
    return STAGE_BENCHMARKS.get(stage, {}).get(metric, "—")
```

### Recipe 6 — Actuals vs projections divider

```python
def split_actual_projection(df, transition_month):
    actual = df[df["month"] < transition_month].copy()
    actual["type"] = "Actual"
    proj = df[df["month"] >= transition_month].copy()
    proj["type"] = "Projection"
    return actual, proj
```

### Recipe 7 — Variance vs plan (4 quarters)

```python
def variance_vs_plan_chart(actual_quarters, plan_quarters, save="variance.png"):
    fig, ax = plt.subplots(figsize=(8, 4))
    x = range(len(actual_quarters))
    ax.bar([i-0.2 for i in x], plan_quarters, width=0.4, label="Plan", color="lightgray")
    ax.bar([i+0.2 for i in x], actual_quarters, width=0.4, label="Actual", color="#1f77b4")
    for i, (a, p) in enumerate(zip(actual_quarters, plan_quarters)):
        delta_pct = (a - p) / p if p else 0
        color = "green" if delta_pct >= 0 else "red"
        ax.text(i, max(a, p) * 1.05, f"{delta_pct:+.0%}", ha="center", color=color, fontweight="bold")
    ax.legend(); ax.grid(alpha=0.3)
    plt.tight_layout(); plt.savefig(save, dpi=200)
    return save
```

### Recipe 8 — Visible.vc data-room hosting + DocSend tracking

```bash
# Upload deck to Visible.vc (data room)
curl -X POST "https://api.visible.vc/v1/dataroom/files" \
  -H "Authorization: Bearer $VISIBLE_API_KEY" \
  -F "file=@pitch_deck.pdf" \
  -F "title=Series_A_Deck_v3"

# DocSend slide-by-slide tracking
curl -X POST "https://docsend.com/api/v1/documents" \
  -H "Authorization: Bearer $DOCSEND_API_KEY" \
  -F "file=@pitch_deck.pdf"
```

## Examples

### Example 1: Series A pitch deck financials (3 slides)

**Goal:** 3 financial slides for Series A deck.

**Steps:**
1. Recipe 1 → ARR chart (24mo history + 36mo projection).
2. Recipe 2 → 4-up unit econ tiles (CAC Payback / LTV:CAC / NRR / GM).
3. Recipe 3 → path-to-profit stacked area.
4. Recipe 4 → assemble PPTX.
5. Recipe 8 → host on Visible.vc + DocSend for engagement tracking.

**Result:** Deck financial section investors can scan in 30 seconds.

### Example 2: Seed deck (1 slide)

**Goal:** Single slide — early-stage; no NRR yet.

**Steps:**
1. Recipe 1 → revenue chart (12mo + 24mo projection).
2. Add 2 stat callouts: customer count, average MRR/customer.
3. Add 1 narrative line: "Path to $1M ARR in 14 months at current MoM growth."

**Result:** Clean seed financials slide.

## Edge cases / gotchas

- **Don't overcrowd.** Investors won't read 12 metrics; pick the 6 that tell your story.
- **Mark actuals vs projections.** Solid line + dashed line + shaded confidence band. Lying-by-omission = trust-killer.
- **Don't show MRR for enterprise.** Lumpy contracts; ARR or contract-weighted run-rate is better.
- **Don't show "burn rate" alone.** Pair with runway (months) and burn multiple (efficiency).
- **CAC Payback assumption must be defined.** Months to recover CAC from gross profit; specify GM used.
- **NRR cohort consistency.** TTM NRR on same cohort definition across periods.
- **3-year projections are credible; 5-year is signaling.** Series A: 3yr ok; Series B+ → 5yr acceptable if defensible.
- **Don't extrapolate hockey-stick from 2 data points.** Investors discount; show 12-24mo of monthly data.
- **Plan vs Actual matters more than just Actual.** Investors test execution by accuracy of past forecasts. Show variance.
- **Stage-graded benchmarks** (Recipe 5) — investors compare to peer cohort. Surface explicitly: "118% NRR vs SaaS Series B benchmark 110-120%."

> ⚠ **This is informational guidance from an AI agent. Always consult a licensed CFO, CPA, or qualified investment advisor before making binding strategic-finance decisions.**

## Sources

- WaveUp financial projections slide 2026: https://waveup.com/blog/financial-projections-slide/
- LTSE pitch deck metrics: https://ltse.com/insights/the-metrics-that-should-be-in-your-pitch-deck
- Spectup pitch deck financials: https://www.spectup.com/resource-hub/pitch-deck-financials-slide
- Eagle Rock CFO benchmarks: https://www.eaglerockcfo.com/blog/research/saas-finance-metrics-benchmarks
- Bessemer SaaS metrics: https://www.bvp.com/atlas
- python-pptx docs: https://python-pptx.readthedocs.io/
- Visible.vc pitch deck hosting: https://visible.vc/product/data-rooms/

## Related skills

- `three-statement-financial-model-tied` — model that feeds the slides.
- `driver-based-revenue-modeling` — revenue trajectory chart source.
- `ltv-cohort-strategic` — unit economics tile data.
- `investor-data-room-curation` — hosts the deck + back-up data.
- `investor-update-cfo-voice` — recurring updates after pitch.
