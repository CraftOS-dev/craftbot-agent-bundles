<!--
Sources: Plotly https://plotly.com/python/
         Altair https://altair-viz.github.io/
         Vega-Lite https://vega.github.io/vega-lite/
         matplotlib https://matplotlib.org/
         seaborn https://seaborn.pydata.org/
         kaleido https://github.com/plotly/Kaleido (Plotly static-export)
         Datawrapper https://developer.datawrapper.de/
         Mermaid CLI https://github.com/mermaid-js/mermaid-cli
Companion: skills/data-storytelling/ (existing — Setup→Conflict→Resolution principle)
-->

# Data storytelling — Plotly, Altair, matplotlib, Mermaid

Toolkit for the visualization layer of the role.md data-storytelling playbook. Five complementary visualization libraries plus Mermaid for diagrams and Datawrapper for publishing-grade. Pick the right tool per audience and embed format.

## When to use this skill

- Producing charts for executive briefings, full reports, slide decks
- Building cohort-retention curves, KPI trend charts, comparison matrices
- Survival curves with confidence intervals (Kaplan-Meier from `cohort-retention-lifelines`)
- Interactive HTML reports with hover, zoom, brush
- Static PNG / SVG / PDF for branded DOCX / PDF deliverables
- Diagrams (architecture, process, decision trees)
- Publishing-grade interactive embeds (web-facing reports)

## When NOT to use

- For ad-hoc data exploration → use pandas + matplotlib directly without ceremony
- For real-time dashboards → hand off to engineering with the spec; analyst designs, eng builds
- For non-data visuals (illustrations, photography) → out of scope

## Tool selection matrix

| Need | Tool | Why |
|---|---|---|
| Interactive HTML report (hover, zoom, export) | **Plotly** | Best interactive layer in Python; HTML self-contained |
| Concise declarative grammar (5-line chart) | **Altair / Vega-Lite** | Grammar of graphics; readable code |
| Publication-grade static (research papers, journals) | **matplotlib + seaborn** | Fine control over every element |
| Static PNG export of Plotly chart | **kaleido** | Reliable headless Plotly→PNG |
| Embed-grade web-facing (newsroom-style) | **Datawrapper API** | Best-in-class responsive embeds; $799+/mo |
| Diagrams (flow, sequence, ERD, gantt, mindmap) | **Mermaid CLI** | Text-to-diagram in markdown; CI-friendly |
| Slide chart | **matplotlib (PNG) → pptx** | Best for static slide chart |
| DOCX chart | **matplotlib / Plotly+kaleido (PNG) → docx** | Embed PNG in DOCX |

## Setup

```bash
pip install plotly altair vega_datasets matplotlib seaborn kaleido pandas
# Mermaid CLI (requires Node)
npm i -g @mermaid-js/mermaid-cli
# Datawrapper (paid)
export DATAWRAPPER_API_TOKEN="..."
```

## Recipes by library

### Recipe 1 — Plotly: interactive cohort retention curves

```python
import plotly.graph_objects as go
fig = go.Figure()
for cohort, row in retention_pct.iterrows():
    fig.add_trace(go.Scatter(x=row.index, y=row.values, mode="lines+markers", name=str(cohort)))
fig.update_layout(
    title="Cohort retention (% active vs days since signup)",
    xaxis_title="Days since signup",
    yaxis_title="% retained",
    yaxis=dict(ticksuffix="%"),
    hovermode="x unified",
)
fig.write_html("cohort_retention.html")
fig.write_image("cohort_retention.png", width=1200, height=700)  # via kaleido
```

### Recipe 2 — Plotly: Kaplan-Meier with confidence band

```python
import plotly.graph_objects as go
# kmf is a fitted lifelines KaplanMeierFitter
sf = kmf.survival_function_
ci = kmf.confidence_interval_

fig = go.Figure([
    go.Scatter(x=sf.index, y=sf.iloc[:,0], mode="lines", name="Survival", line=dict(width=2)),
    go.Scatter(x=ci.index, y=ci.iloc[:,1], mode="lines", name="Upper CI", line=dict(width=0), showlegend=False),
    go.Scatter(x=ci.index, y=ci.iloc[:,0], mode="lines", name="95% CI", fill="tonexty",
               fillcolor="rgba(0,100,200,0.2)", line=dict(width=0)),
])
fig.update_layout(title="Kaplan-Meier Survival Curve", xaxis_title="Days", yaxis_title="P(active)")
fig.write_html("survival.html")
```

### Recipe 3 — Altair: declarative comparison chart

```python
import altair as alt
import pandas as pd

# Sales by region by year — grouped bar
chart = alt.Chart(df).mark_bar().encode(
    x=alt.X("year:O", title="Fiscal Year"),
    y=alt.Y("revenue:Q", title="Revenue (USD)", axis=alt.Axis(format="$,.0f")),
    color="region:N",
    column="region:N",
).properties(title="Revenue by region", width=120)
chart.save("revenue.html")
chart.save("revenue.png", scale_factor=2.0)
```

### Recipe 4 — matplotlib + seaborn: publication-grade

```python
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", context="paper", font_scale=1.1)
fig, ax = plt.subplots(figsize=(8, 5))
sns.lineplot(data=df, x="year", y="gdp_growth", hue="country", marker="o", ax=ax)
ax.set_title("Real GDP growth, 2015-2025")
ax.set_xlabel("Year")
ax.set_ylabel("Growth (%)")
ax.legend(title="", loc="upper right", frameon=False)
fig.tight_layout()
fig.savefig("gdp.pdf", dpi=300, bbox_inches="tight")
fig.savefig("gdp.png", dpi=200, bbox_inches="tight")
```

### Recipe 5 — Mermaid: process diagram

```bash
cat > flow.mmd <<'EOF'
flowchart TD
    A[User signs up] --> B{Completes onboarding?}
    B -->|Yes| C[Activated]
    B -->|No| D[Inactive]
    C --> E{Active at Day 30?}
    E -->|Yes| F[Retained user]
    E -->|No| G[Churned]
EOF
mmdc -i flow.mmd -o flow.png -w 1200 -H 800
```

Other Mermaid diagram types: `sequenceDiagram`, `classDiagram`, `erDiagram`, `gantt`, `mindmap`, `journey`. Full list: https://mermaid.js.org/

### Recipe 6 — Datawrapper (publishing-grade embeds)

```python
import requests
headers = {"Authorization": f"Bearer {os.environ['DATAWRAPPER_API_TOKEN']}"}

# Create chart
chart = requests.post("https://api.datawrapper.de/v3/charts",
    headers=headers,
    json={"title": "GDP growth", "type": "d3-lines"}).json()
# Upload data
requests.put(f"https://api.datawrapper.de/v3/charts/{chart['id']}/data",
    headers=headers, data=df.to_csv(index=False))
# Publish
requests.post(f"https://api.datawrapper.de/v3/charts/{chart['id']}/publish", headers=headers)
# → returns embed URL / iframe HTML
```

Use only for the final, polished, publication-facing deliverable. Don't burn Datawrapper credit on iterations.

## The role.md data-storytelling principles applied

The existing `data-storytelling` skill says: Setup → Conflict → Resolution; start with "so what"; three elements (data + narrative + visual).

How to apply in chart design:

- **Setup:** the chart's caption / annotation sets context (timeframe, scope)
- **Conflict:** the chart's *visual emphasis* should highlight the surprise / problem (color, callout, annotation arrow)
- **Resolution:** the chart's caption ends with the implication ("→ X is on track to overtake Y by Q4")

Never publish a chart without a one-sentence caption that answers "so what?". A naked chart with no narrative is a data dump.

## Color and accessibility

- Use **colorblind-safe palettes** (`viridis`, `cividis`, `Okabe-Ito`)
- Encode the same dimension in **shape + color** for redundancy
- Provide text alternatives (alt text in HTML, table fallback)
- Use **direct labels** instead of legends where space allows (reduces eye-jumps)
- Limit to ≤5 series per chart (≤7 max); split into small multiples otherwise

## Chart-type selection rules

| Comparison | Default chart |
|---|---|
| Trend over time | Line |
| Composition of a whole | Stacked bar (avoid pies unless ≤3 slices) |
| Distribution | Histogram + density |
| Two-variable relationship | Scatter (+ regression line if linear) |
| Categorical comparison | Bar (horizontal if labels long) |
| Hierarchical | Treemap or sunburst |
| Geographic | Choropleth |
| Network | Force-directed or matrix |
| Funnel / cohort | Cohort heatmap |
| Survival | KM curve with CI band |

## Edge cases

- **Plotly + kaleido on headless server:** `kaleido` runs Chromium headless; if installation fails, try `pip install -U kaleido==0.2.1` (older versions are more stable) or use `nbconvert` + selenium.
- **Mermaid render in dark mode:** add `%%{init: {'theme':'dark'}}%%` at the top of the diagram.
- **Altair size limits:** Altair embeds data in the spec by default; for > 5k rows use `alt.data_transformers.disable_max_rows()` or external CSV reference.
- **matplotlib backend on headless:** `import matplotlib; matplotlib.use("Agg")` before `pyplot` to avoid display errors.
- **High-DPI for print:** dpi ≥ 300 for print PDF; 150-200 for screen PNG.
- **Truncation in slide charts:** when exporting for PPTX, set figure size to slide aspect ratio (16:9, 1280×720 pixels) to avoid scaling artifacts.
- **Brand alignment:** if the deliverable is for a known brand, ask the user for a color palette + typography spec at the start; bake into a matplotlib style file.

## Sources

- Plotly Python: https://plotly.com/python/
- Altair: https://altair-viz.github.io/
- Vega-Lite: https://vega.github.io/vega-lite/
- matplotlib: https://matplotlib.org/
- seaborn: https://seaborn.pydata.org/
- kaleido: https://github.com/plotly/Kaleido
- Datawrapper API: https://developer.datawrapper.de/
- Mermaid CLI: https://github.com/mermaid-js/mermaid-cli
- Colorblind-safe palettes: https://jfly.uni-koeln.de/color/ (Okabe-Ito); `viridis` package
- role.md → "Data storytelling principles" (this bundle)

## Related skills

- `data-storytelling` (existing) — Setup → Conflict → Resolution principles
- `pandoc-branded-deliverables` — wrap visuals into branded DOCX / PDF
- `cohort-retention-lifelines` — visualize the cohort analysis output
