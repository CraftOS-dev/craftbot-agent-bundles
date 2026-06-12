<!--
Source: https://www.cubesoftware.com/blog/cfo-guide-board-deck
Source: https://www.venasolutions.com/blog/cfo-board-reports
Source: https://winningpresentations.com/how-to-present-to-cfo/
Reference role.md: "Board CFO package playbook"
-->

# Board CFO financial package — 10-slide structure

The CFO's board deliverable. Cube/Vena 2026 structure: 10-slide package with TL;DR + KPI dashboard + Plan vs Actual + Cash + Strategic initiatives + Risks + Forecast revision + Decisions sought + backup. Start prep T-28 days; pre-wire individual board members T-7 days.

## When to use

- Quarterly board meeting prep (the main use).
- Annual board strategic offsite.
- Mid-quarter board update on material event (e.g. large deal, regulatory).
- Special-purpose committees (audit, comp).
- Trigger phrases: "board deck", "CFO board package", "board prep", "board meeting financials", "quarterly board".

NOT for: ad-hoc investor update (use `investor-update-cfo-voice`); pitch deck (use `pitch-deck-financial-slides`).

## Setup

```bash
uvx --with python-pptx --with pandas --with matplotlib python -c "import pptx, pandas, matplotlib"

# Data sources:
# - finance-controller's monthly close output → P&L, BS, Cash
# - Stripe / Xero / HRIS
# - PostHog / Mixpanel for product KPIs
```

## The 10-slide structure (Cube/Vena pattern)

```
SLIDE 1 — TL;DR + Decisions Sought
  TOP: 3-bullet headline (financial, operational, strategic)
  BOTTOM: 3 decisions sought from board, with options

SLIDE 2 — KPI Dashboard
  6-9 metrics; current + trend + benchmark
  ARR / NRR / Cash / Runway / Gross Margin / Rule of 40 / Headcount / etc.

SLIDE 3 — Plan vs Actual (Last Quarter)
  P&L lines: variance > 10% explained
  Revenue, COGS, GM, S&M, R&D, G&A, EBITDA, Cash

SLIDE 4 — Cash + Runway Forward
  Cash trajectory next 18 months (3 scenarios)
  Treasury allocation summary (operating / reserve / strategic)
  Funding need + timing

SLIDE 5 — Strategic Initiative Status
  3-5 named initiatives; current status (green/yellow/red); KPIs

SLIDE 6 — Risk + Mitigation Register
  Top 5 risks; likelihood × impact heat map; mitigation plan + owner

SLIDE 7 — Forecast Revision
  Walk from prior plan to new forecast; reasons; sensitivity

SLIDE 8 — Decisions Sought (Detail)
  Each decision: context, options A/B/C, CFO recommendation, board vote

SLIDE 9 — Backup: Detailed Financials
  Three-statement IS / BS / CF detail

SLIDE 10 — Backup: Unit Economics + Cohort Detail
  Per-segment / per-channel LTV / CAC / NRR
```

## The T-28 timeline

```
T-28 days: Monthly close locked; start board prep
T-21 days: Draft KPI dashboard; circulate to founders + GTM lead
T-14 days: Draft slides 1-7; review with CEO
T-10 days: Pre-wire individual board members on contentious items
T-7 days:  Send pre-read deck
T-3 days:  Lock final deck
T-0:      Board meeting
T+3 days: Send minutes + decisions register
```

## Common recipes

### Recipe 1 — Build PPTX skeleton

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

def board_deck_skeleton(quarter="Q2 2026", save="board_deck.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)

    slides = [
        ("Board Meeting — " + quarter, "TL;DR + Decisions Sought"),
        ("KPI Dashboard", "9 metrics × current / trend / benchmark"),
        ("Plan vs Actual — " + quarter, "Variance > 10% explained"),
        ("Cash + Runway Forward", "18-month projection × 3 scenarios"),
        ("Strategic Initiatives", "3-5 named; status; KPIs"),
        ("Risk + Mitigation Register", "Top 5; heat map; owners"),
        ("Forecast Revision", "Walk from prior to new; sensitivity"),
        ("Decisions Sought (Detail)", "Options A/B/C per decision"),
        ("Backup: Financials Detail", "IS / BS / CF"),
        ("Backup: Unit Economics", "Per-segment cohort detail"),
    ]
    for title, sub in slides:
        s = prs.slides.add_slide(prs.slide_layouts[5])
        s.shapes.title.text = title
        tb = s.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(12), Inches(0.5))
        tb.text_frame.text = sub

    prs.save(save)
    return save
```

### Recipe 2 — KPI dashboard tile generator

```python
import matplotlib.pyplot as plt

def kpi_dashboard(metrics, save="kpi_dash.png"):
    """metrics: list of dicts {name, value, mom, yoy, benchmark, flag}"""
    n = len(metrics); cols = 3; rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(14, 3 * rows))
    axes = axes.flatten() if rows > 1 else [axes] if cols == 1 else axes
    for ax, m in zip(axes, metrics):
        color = {"green": "#2e7d32", "yellow": "#f9a825", "red": "#c62828"}.get(m["flag"], "#333")
        ax.text(0.5, 0.7, m["value"], ha="center", fontsize=28, fontweight="bold", color=color, transform=ax.transAxes)
        ax.text(0.5, 0.5, m["name"], ha="center", fontsize=12, transform=ax.transAxes)
        ax.text(0.5, 0.35, f"MoM {m['mom']} | YoY {m['yoy']}", ha="center", fontsize=9, transform=ax.transAxes)
        ax.text(0.5, 0.2, f"Benchmark: {m['benchmark']}", ha="center", fontsize=9, color="gray", transform=ax.transAxes)
        ax.axis("off")
    plt.tight_layout(); plt.savefig(save, dpi=200)
    return save

kpi_dashboard([
    {"name": "ARR", "value": "$4.2M", "mom": "+5.2%", "yoy": "+83%", "benchmark": "—", "flag": "green"},
    {"name": "NRR", "value": "118%", "mom": "-1pp", "yoy": "+8pp", "benchmark": "≥100%", "flag": "green"},
    {"name": "Gross Margin", "value": "78.5%", "mom": "+0.3pp", "yoy": "+2.1pp", "benchmark": "≥75%", "flag": "green"},
    {"name": "Cash", "value": "$8.5M", "mom": "-$420K", "yoy": "-$2.1M", "benchmark": "—", "flag": "yellow"},
    {"name": "Runway", "value": "20mo", "mom": "-1mo", "yoy": "-7mo", "benchmark": "≥24mo", "flag": "yellow"},
    {"name": "Headcount", "value": "85", "mom": "+3", "yoy": "+22", "benchmark": "—", "flag": "green"},
])
```

### Recipe 3 — Plan vs Actual variance table

```python
import pandas as pd

def plan_vs_actual_table(plan, actual):
    df = pd.DataFrame({"Plan": plan, "Actual": actual})
    df["Variance"] = df["Actual"] - df["Plan"]
    df["Var%"] = df["Variance"] / df["Plan"].replace(0, 1) * 100
    df["Flag"] = df["Var%"].apply(lambda v: "RED" if abs(v) > 10 else "YELLOW" if abs(v) > 5 else "GREEN")
    return df

print(plan_vs_actual_table(
    plan={"Revenue": 1_050_000, "COGS": 220_000, "S&M": 440_000, "R&D": 290_000, "G&A": 125_000, "EBITDA": -25_000},
    actual={"Revenue": 1_098_000, "COGS": 234_000, "S&M": 412_000, "R&D": 305_000, "G&A": 128_000, "EBITDA": 19_000}
))
```

### Recipe 4 — Cash + runway scenario chart

```python
def runway_chart(scenarios, save="runway.png"):
    """scenarios: dict label → list of monthly cash"""
    fig, ax = plt.subplots(figsize=(10, 5))
    for label, cash_series in scenarios.items():
        ax.plot(range(len(cash_series)), [c/1e6 for c in cash_series], label=label, linewidth=2.5)
    ax.axhline(0, color="red", linestyle="--", alpha=0.5)
    ax.set_xlabel("Months from today"); ax.set_ylabel("Cash ($M)")
    ax.set_title("Cash trajectory — 18mo × 3 scenarios")
    ax.legend(); ax.grid(alpha=0.3)
    plt.tight_layout(); plt.savefig(save, dpi=200)
    return save
```

### Recipe 5 — Risk heat map

```python
def risk_heat_map(risks, save="risk_heat.png"):
    """risks: list of {name, likelihood (1-5), impact (1-5), owner}"""
    fig, ax = plt.subplots(figsize=(8, 6))
    for r in risks:
        ax.scatter(r["likelihood"], r["impact"], s=400, alpha=0.6)
        ax.annotate(r["name"], (r["likelihood"], r["impact"]), fontsize=9)
    ax.set_xlabel("Likelihood (1-5)"); ax.set_ylabel("Impact (1-5)")
    ax.set_xlim(0, 6); ax.set_ylim(0, 6)
    ax.set_title("Risk Heat Map")
    ax.grid(alpha=0.3)
    # Color regions
    ax.axhspan(4, 6, xmin=0.66, xmax=1.0, alpha=0.1, color="red")
    ax.axhspan(0, 2, xmin=0, xmax=0.33, alpha=0.1, color="green")
    plt.tight_layout(); plt.savefig(save, dpi=200)
    return save
```

### Recipe 6 — Forecast walk

```python
def forecast_walk(walk_items, save="forecast_walk.png"):
    """walk_items: list of {label, delta}"""
    labels = ["Prior plan"] + [w["label"] for w in walk_items] + ["New forecast"]
    cumulative = [walk_items[0].get("starting", 0)]
    for w in walk_items:
        cumulative.append(cumulative[-1] + w["delta"])
    cumulative.append(cumulative[-1])

    fig, ax = plt.subplots(figsize=(10, 5))
    for i, val in enumerate(cumulative):
        color = "blue" if i in (0, len(cumulative)-1) else ("green" if walk_items[i-1]["delta"] >= 0 else "red")
        ax.bar(i, val if i in (0, len(cumulative)-1) else walk_items[i-1]["delta"],
               bottom=0 if i in (0, len(cumulative)-1) else cumulative[i-1],
               color=color, alpha=0.7)
    ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels, rotation=30, ha="right")
    ax.set_title("Forecast walk: Prior plan → New plan")
    plt.tight_layout(); plt.savefig(save, dpi=200)
    return save
```

### Recipe 7 — Decisions sought slide content

```markdown
## Decision 1: Raise timing — accelerate or delay Series B

**Context:** 20mo runway; Series B comp set valuing at 8-12× ARR
**Options:**
  A. Start raise now (Aug 2026) at $4.2M ARR → valuation $34-50M; 35-45% dilution
  B. Delay 6mo to $7M ARR → valuation $56-84M; 25-35% dilution; 14mo runway at raise time
  C. Bridge $2M now + raise Q1 2027 at $5.5M ARR → valuation $44-66M; bridge cost ~3% dilution

**CFO recommendation:** Option B. Q1 2027 timing; pre-wire investors now.
**Board vote:** —
```

### Recipe 8 — Pre-read summary memo

```markdown
# Pre-read Summary — Q2 2026 Board Meeting

**Headline:**
1. ARR $4.2M (+83% YoY), tracking to $5M EoQ3.
2. NRR 118%; Burn Multiple 1.35x (healthy).
3. Cash $8.5M; runway 20mo. Series B timing decision sought.

**Decisions sought:**
- Series B timing (Option A / B / C; recommendation B)
- 409A refresh authorization (Aug)
- Two senior hires (VP Sales, VP Engineering) — approve final offers

**Risks worth flagging:**
- Customer concentration: top-3 = 28% of ARR (one mid-market in renewal Q3)
- Hosting cost inflation (8% YoY; renegotiation in progress)
```

## Examples

### Example 1: Q2 2026 standard quarterly prep

**Goal:** Board-ready deck.

**Steps:**
1. T-28: pull finance-controller monthly close output.
2. T-21: Recipe 1 → skeleton; Recipe 2 → KPI dashboard; circulate.
3. T-14: Recipe 3 + 4 → Plan vs Actual + cash chart; CEO review.
4. T-10: pre-wire individual board members on Decision 1 (raise timing) + Decision 2 (409A).
5. T-7: send pre-read (Recipe 8).
6. T-3: lock deck.
7. T-0: meeting.
8. T+3: minutes + decisions log to Notion.

**Result:** No surprises; board votes informed.

### Example 2: Mid-quarter update on large deal close

**Goal:** Update board on $1.5M ACV enterprise deal.

**Steps:**
1. 1-slide impact: ARR + cash + headcount implications.
2. 1-slide ask: do we want to over-allocate engineering for delivery?
3. Send email + offer to schedule 30-min call.

**Result:** Real-time board alignment.

## Edge cases / gotchas

- **Don't bury the lede.** TL;DR slide first; details follow. Board members read 3 slides max.
- **Variance > 10% must be explained.** Otherwise board loses trust. Plan vs Actual is the single most-scrutinized slide.
- **Decisions sought must be specific.** "Approve Series B raise" is too vague. "Approve $15M raise at $40M pre-money, lead from FundX" = decisional.
- **Pre-wire is mandatory.** Surprises at the meeting = bad governance. T-10 days, individual calls.
- **Don't show 50 metrics.** 6-9 KPIs; rest in backup.
- **Be careful with comp benchmarks.** Carta/Pave are mostly accurate but reductive. Use as context, not gospel.
- **Risks must have owners.** "Customer concentration risk: owner = CRO; next review Q3."
- **Don't game variances.** If revenue beat plan, show it; if plan was lowballed, fix the planning process.
- **Stock-based comp confuses boards.** Always split EBITDA into "adjusted" (excl. SBC) and reported.
- **Treasury allocation = real CFO topic.** Surface yields, tier allocation, multi-bank posture explicitly.
- **Headcount slide drives big questions.** Plan for it — show hires, attrition, plan vs actual headcount.

> ⚠ **This is informational guidance from an AI agent. Always consult a licensed CFO, CPA, or qualified investment advisor before making binding strategic-finance decisions.**

## Sources

- Cube CFO board deck guide: https://www.cubesoftware.com/blog/cfo-guide-board-deck
- Vena CFO board reports: https://www.venasolutions.com/blog/cfo-board-reports
- Winning Presentations CFO: https://winningpresentations.com/how-to-present-to-cfo/
- Carta board playbook: https://carta.com/learn/private-companies/governance/board-meetings/
- Bessemer board ops: https://www.bvp.com/atlas
- python-pptx: https://python-pptx.readthedocs.io/

## Related skills

- `three-statement-financial-model-tied` — financials data source.
- `driver-based-revenue-modeling` — KPI dashboard inputs.
- `treasury-yield-ladder-risk-tier` — cash slide treasury context.
- `scenario-planning-monte-carlo` — runway scenarios chart.
- `investor-update-cfo-voice` — external version after board.
