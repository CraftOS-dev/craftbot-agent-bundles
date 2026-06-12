<!--
Storytelling with Data: https://www.storytellingwithdata.com/
Pyramid Principle (Minto)
Plotly: https://plotly.com/python/
Altair: https://altair-viz.github.io/
Companion: role.md → "Capability reference → Visualization" + "Report templates"
-->

# Data storytelling — narrative structure + charts + reports

Turn analytics findings into executive-ready deliverables. Apply Setup → Conflict → Resolution structure, lead with "so what", use the Pyramid Principle for memos, and ship via Plotly / Altair / matplotlib + Pandoc into branded DOCX / PDF / PPTX.

## When to use

- "Write the exec summary of this analysis"
- "Turn this notebook into a slide deck"
- "Build a chart that tells a story (not just shows data)"
- "Pyramid-Principle memo for leadership"
- "Generate a DOCX from markdown via Pandoc"

Defer notebook / report platforms to `evidence-streamlit-marimo-reports` / `hex-notebooks-apps`. Defer dashboard design to `metabase-self-serve-dashboards`. Defer the analytics itself to the relevant skill (`cohort-retention-deep-survival`, etc.).

## Setup

```bash
pip install plotly altair matplotlib seaborn kaleido       # kaleido for static PNG export from Plotly
pip install pandas numpy
# Pandoc for markdown → DOCX/PDF/HTML/PPTX
brew install pandoc          # macOS
# Or: choco install pandoc, or download from pandoc.org
```

No auth required.

## Principles cheat sheet (from storytellingwithdata.com)

1. **Understand the context** — Who's the audience? What action do they need to take?
2. **Choose appropriate visual** — Data shape → chart type (table for precision, bar for comparison, line for change-over-time, scatter for relationship).
3. **Eliminate clutter** — Every pixel earns its place. Remove gridlines, borders, redundant labels, chart-junk.
4. **Focus attention** — Pre-attentive attributes (color, size, bold) direct the eye.
5. **Think like a designer** — Affordances, accessibility, alignment.
6. **Tell a story** — Setup → Conflict → Resolution; lead with the "so what".

## Common recipes

### Recipe 1 — Pyramid Principle (Minto) executive memo

```
[Title — single sentence with the headline insight]

Recommendation:
We should <X> in order to <achieve Y> by <date Z>.

This recommendation rests on three findings:

1. <Finding 1 — single sentence>
   - <Supporting data point with magnitude + reference>
   - <Supporting data point>

2. <Finding 2 — single sentence>
   - <Supporting data>
   - <Supporting data>

3. <Finding 3 — single sentence>
   - <Supporting data>
   - <Supporting data>

Risks & caveats:
- <Top risk>
- <Top caveat>

Next steps:
1. <Action by whom by when>
2. <Action by whom by when>
```

### Recipe 2 — Setup → Conflict → Resolution analytics narrative

```markdown
# Q2 Revenue Review — North America Slowdown

## Setup (what was normal)
For the past 6 quarters, North America revenue grew 8% QoQ on the strength
of mid-market expansion. Coming into Q2 we expected the same: +$2.1M projected.

## Conflict (what changed)
Actual Q2 came in at +$420K, **20% of forecast**. Three drivers:

1. **Mid-market expansion stalled** — Annualized expansion revenue from existing
   customers dropped 64% vs Q1. Root cause: 3 large accounts paused upgrades
   pending procurement reviews.
2. **New logo acquisition flat** — Marketing-qualified leads grew 12% but win
   rate fell from 28% → 19%. Loss reasons cluster around feature parity gaps
   vs Competitor X.
3. **Churn ticked up** — Quarterly logo churn rose from 2.1% to 3.4%, driven
   by SMB segment. Cohort analysis shows the Q4-2025 cohort retains 14pp
   worse than Q4-2024 — onboarding regression.

## Resolution (what to do)
Three concrete actions, owners, dates:

1. **Unblock paused upgrades.** Sales VP + Customer Success VP, by Jul 15.
   Expected lift: $800K.
2. **Close the top 3 feature gaps vs Competitor X.** Product VP, prioritize
   for Q3 sprint. Expected lift: 5pp win rate.
3. **Onboarding regression hotfix.** Product + CS, complete by Jun 30. Expected
   lift: 8pp on Q3-2026 SMB cohort retention.

Total expected Q3 impact: +$1.8M closing the gap to forecast.
```

### Recipe 3 — Chart: BAR — most common comparison

```python
import plotly.express as px
import plotly.io as pio

df_summary = (df.groupby("region")["revenue"].sum() / 1e6).reset_index()
df_summary = df_summary.sort_values("revenue", ascending=True)        # ascending for horizontal bar
df_summary["highlight"] = df_summary["region"] == "North America"      # flag the focus

fig = px.bar(
    df_summary, x="revenue", y="region", orientation="h",
    color="highlight",
    color_discrete_map={True: "#E74C3C", False: "#BDC3C7"},       # red for focus, gray for context
    text=df_summary["revenue"].round(1).astype(str) + "M",
)
fig.update_layout(
    title="Q2 revenue ($M) — North America underperformed",
    showlegend=False,
    plot_bgcolor="white",
    xaxis=dict(showgrid=False, showticklabels=False),    # remove clutter
    yaxis=dict(showgrid=False, title=""),
    margin=dict(t=80, b=40, l=20, r=20),
)
fig.update_traces(textposition="outside", cliponaxis=False)
fig.write_image("revenue_by_region.png", scale=2, width=900, height=500)
```

### Recipe 4 — Chart: LINE with annotated focus point

```python
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df["date"], y=df["revenue"],
    mode="lines", line=dict(color="#34495E", width=2),
    name="Revenue",
))

# Forecast vs actual divergence — highlight Q2 gap
fig.add_trace(go.Scatter(
    x=df["date"], y=df["forecast"],
    mode="lines", line=dict(color="#BDC3C7", width=1.5, dash="dash"),
    name="Forecast",
))

# Annotate the gap
fig.add_annotation(
    x="2026-06-30", y=df["revenue"].iloc[-1],
    text=f"Q2 actual: ${df['revenue'].iloc[-1]/1e6:.1f}M<br>vs forecast: ${df['forecast'].iloc[-1]/1e6:.1f}M",
    showarrow=True, arrowhead=2, ax=-60, ay=-40,
    bgcolor="white", bordercolor="#E74C3C",
)
fig.update_layout(
    title="NA monthly revenue — Q2 broke the trend",
    plot_bgcolor="white",
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor="#ECF0F1", tickformat="$.1s"),
)
fig.write_image("revenue_trend.png", scale=2, width=1000, height=500)
```

### Recipe 5 — Chart: cohort HEATMAP

```python
import altair as alt
import pandas as pd

# cohort_df: cohort_month × months_since_signup → retention
chart = alt.Chart(cohort_df).mark_rect().encode(
    x=alt.X("months_since_signup:O", title="Months since signup"),
    y=alt.Y("cohort_month:O", title="Cohort month"),
    color=alt.Color("retention:Q", scale=alt.Scale(scheme="blues"), title="Retention %"),
    tooltip=["cohort_month", "months_since_signup", "retention"],
).properties(
    title="Cohort retention — 30/60/90 day milestones",
    width=600, height=400,
)
chart.save("cohort_heatmap.png")
```

### Recipe 6 — Chart-junk removal cheat sheet

| Remove | Why |
|---|---|
| Y-axis at zero when comparing tiny deltas | False precision; doesn't show the story |
| 3D bars / pie slices | Distort visual perception |
| Gridlines | Compete with the data |
| Drop-shadows / borders | Visual noise |
| All-caps everything | Hard to read |
| Tons of decimals | "84.752912%" → "85%" |
| Rainbow color schemes | Not perceptually uniform; bad for color-blind |
| Pie charts with >5 slices | Replace with horizontal bar |
| Dual y-axes (when not unit-equivalent) | Misleading |
| Legend when chart can self-label | Use direct labels on lines |

### Recipe 7 — Color palette (perceptually uniform + colorblind-safe)

```python
# Categorical — Okabe-Ito (8 colorblind-safe)
OKABE_ITO = ["#E69F00", "#56B4E9", "#009E73", "#F0E442",
             "#0072B2", "#D55E00", "#CC79A7", "#000000"]

# Sequential — Viridis / Cividis
import plotly.express as px
fig = px.imshow(matrix, color_continuous_scale="Viridis")

# Diverging — RdBu
fig = px.imshow(matrix, color_continuous_scale="RdBu_r", color_continuous_midpoint=0)

# Brand single-hue:
# Focus: #E74C3C (red)
# Context: #BDC3C7 (gray)
# Positive: #27AE60 (green)
```

### Recipe 8 — Pandoc markdown → DOCX

`template.docx` (Word reference document) defines styles + branding; create once and reuse.

```bash
pandoc report.md \
  -o quarterly-review.docx \
  --reference-doc=template.docx \
  --toc --toc-depth=2 \
  --number-sections \
  --metadata title="Q2 2026 Review"

# Markdown → PDF (LaTeX or weasyprint)
pandoc report.md -o report.pdf --pdf-engine=weasyprint

# Markdown → PPTX (Pandoc 2.0+, slides via second-level headers)
pandoc slides.md -o deck.pptx --reference-doc=template.pptx
```

### Recipe 9 — Slide-deck source in markdown

```markdown
---
title: Q2 2026 Revenue Review
author: Data Analytics Team
date: June 9, 2026
---

# Q2 2026 — Revenue underperformed; here is why and what we'll do

::: notes
Speaker notes (not visible to audience)
:::

## Setup: Q2 forecast was $2.1M; actual was $420K

![Revenue trend chart](revenue_trend.png){ width=80% }

## Conflict: Three drivers explain 80% of the gap

| Driver                        | Impact ($M) | Owner       |
|-------------------------------|-------------|-------------|
| Mid-market expansion paused   | -0.8        | CSM / Sales |
| Lower new-logo win rate       | -0.6        | Sales / Mkt |
| Higher SMB churn              | -0.3        | Product/CS  |

## Resolution: 3 actions, owners, dates

1. Unblock paused upgrades — Jul 15 — VP Sales + VP CS
2. Close top 3 feature gaps — Q3 sprint — VP Product
3. Onboarding hotfix — Jun 30 — VP Product + VP CS

## Q&A
```

Build: `pandoc slides.md -o q2-review.pptx --reference-doc=brand-template.pptx`.

### Recipe 10 — Deliverable checklist

```
DELIVERABLE QA
==============

CONTEXT:
[ ] Audience identified (exec / manager / IC)?
[ ] "So what" leads the document?
[ ] Recommended action is concrete (who / what / by when)?

NARRATIVE:
[ ] Setup → Conflict → Resolution structure?
[ ] Pyramid Principle: top-line + 3 supporting points + supporting data?
[ ] Caveats / limitations stated explicitly?

CHARTS:
[ ] Each chart has a one-line takeaway title (not just "Revenue over time")?
[ ] Focus element highlighted (color / size)?
[ ] Context grayed out?
[ ] Numbers rounded sensibly (no false precision)?
[ ] Color palette is colorblind-safe?
[ ] Chart-junk removed (gridlines, borders, 3D effects)?

DATA INTEGRITY:
[ ] Source dataset + as-of date in footnote?
[ ] Sample size shown?
[ ] CI / p-value where applicable?
[ ] Comparison context (vs prior period / vs target)?

DELIVERY:
[ ] Format matches audience (DOCX / PDF / PPTX / HTML)?
[ ] Branded template applied?
[ ] Embedded in committable markdown source?
[ ] Link to underlying queries / notebook?
```

## Example end-to-end

**Goal:** Q2 revenue review deck for CEO + board, derived from a Hex notebook.

1. Frame: audience = CEO/board; action = approve $1M Q3 spend on recovery.
2. Outline via Pyramid Principle (Recipe 1) → top-line + 3 findings.
3. Draft narrative with Setup → Conflict → Resolution (Recipe 2).
4. Build 4 charts: revenue trend with forecast overlay (Recipe 4), regional bar (Recipe 3), cohort heatmap (Recipe 5), funnel waterfall.
5. Apply Okabe-Ito palette (Recipe 7); remove chart-junk (Recipe 6).
6. Write narrative as `slides.md` (Recipe 9).
7. Render: `pandoc slides.md -o q2-review.pptx --reference-doc=brand-template.pptx` (Recipe 8).
8. QA via Recipe 10 checklist.
9. Commit `slides.md` + chart-generation Python to git; export PPTX as artifact.

## Edge cases / gotchas

- **Lead with the conclusion** — never bury the recommendation on slide 12. Exec readers scan, not read.
- **Charts should be self-titling** — title = the takeaway, not the data subject. "NA revenue dropped 20% vs forecast" not "Quarterly revenue".
- **One chart, one point** — if you can't say the takeaway in one breath, split into two charts.
- **Y-axis truncation tradeoff** — truncating at zero hides nothing but the size of the change; starting above zero exaggerates. Decide based on whether magnitude or change is the story.
- **Color overload** — limit to 4-5 colors in one view; use shade variations for sub-categories.
- **Accessible chart text** — minimum 14pt for body, 18pt for slide titles; embed alt text in HTML/Markdown.
- **Audience proxy** — execs care about $; engineers about p99 latency; investors about CAC payback. Same data, different framing.
- **Pandoc DOCX tables** — Pandoc renders markdown tables; for complex tables use a `.docx` template with style names referenced.
- **PPTX rendering quirks** — Pandoc PPTX doesn't preserve all PowerPoint features; for animated/transition-heavy decks, build in PowerPoint directly.
- **Plotly to static PNG** — needs `kaleido` (`pip install kaleido`); without it, `write_image` fails silently.
- **Don't show your work** — analysts often want to demonstrate effort; execs want the answer. Move methodology to appendix.
- **"So what?" test** — before shipping, ask "what should change as a result of reading this?" If you can't answer, the deliverable is incomplete.

## Sources

- [Storytelling with Data (Knaflic 2015 + companion site)](https://www.storytellingwithdata.com/)
- [Pyramid Principle (Minto 1996)](https://en.wikipedia.org/wiki/Pyramid_principle)
- [Plotly Python](https://plotly.com/python/)
- [Altair (Vega-Lite for Python)](https://altair-viz.github.io/)
- [Pandoc manual](https://pandoc.org/MANUAL.html)
- [Okabe-Ito color palette](https://jfly.uni-koeln.de/color/)
- [ColorBrewer 2.0](https://colorbrewer2.org/)
- [Edward Tufte — The Visual Display of Quantitative Information](https://www.edwardtufte.com/tufte/)
- role.md → "Report templates"
