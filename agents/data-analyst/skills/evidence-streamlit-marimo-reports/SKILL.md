<!--
Evidence.dev: https://docs.evidence.dev/
Streamlit: https://docs.streamlit.io/
Marimo: https://docs.marimo.io/
Companion: role.md → "Capability reference → BI tools" + "Notebook → report → dashboard pipeline"
-->

# Evidence + Streamlit + Marimo — code-first reports & apps

Three OSS code-first alternatives to traditional BI: Evidence.dev (markdown + SQL → static HTML), Streamlit (Python-only data apps), Marimo (reactive notebooks with no hidden state). All version-controllable, all deployable as static or always-on.

## When to use

| Pick | When |
|---|---|
| **Evidence** | Polished, narrative-driven report; static HTML; version-controlled; non-technical readers |
| **Streamlit** | Quick interactive app; widget-driven; ML inference UI; data scientist demo |
| **Marimo** | Reactive notebook; replaces Jupyter; deployable as app; git-friendly Python |

Defer dashboard-style work to `metabase-self-serve-dashboards` / `looker-lookml-modeling`. Defer notebook-as-product to `hex-notebooks-apps`.

## Setup

```bash
# Evidence
npx degit evidence-dev/template my-report
cd my-report
npm install
npm run sources                # cache data
npm run dev                    # local dev server on :3000

# Streamlit
pip install streamlit pandas plotly altair
streamlit run app.py

# Marimo
pip install marimo
marimo new notebook.py         # scaffolds new reactive notebook
marimo edit notebook.py        # opens browser editor
marimo run notebook.py         # production app server
```

No auth required for local; deployments need warehouse credentials.

## Common recipes — Evidence

### Recipe 1 — Markdown report with SQL + chart

```markdown
---
title: Q2 Revenue Review
---

# Q2 Revenue Review

The quarter closed at **$<Value data={mrr_q2} value="total" fmt=usd0/>**,
up <Value data={mrr_q2} value="growth_yoy" fmt=pct1/> YoY.

```sql mrr_q2
SELECT
    sum(amount_usd) FILTER (WHERE order_date BETWEEN '2026-04-01' AND '2026-06-30') AS total,
    sum(amount_usd) FILTER (WHERE order_date BETWEEN '2026-04-01' AND '2026-06-30')
      / NULLIF(sum(amount_usd) FILTER (WHERE order_date BETWEEN '2025-04-01' AND '2025-06-30'), 0) - 1
      AS growth_yoy
FROM marts.fct_orders
WHERE status = 'paid'
```

## Daily Trend

```sql daily_revenue
SELECT order_date, sum(amount_usd) AS revenue
FROM marts.fct_orders
WHERE status = 'paid' AND order_date >= '2026-04-01' AND order_date <= '2026-06-30'
GROUP BY 1
ORDER BY 1
```

<LineChart data={daily_revenue} x=order_date y=revenue title="Daily revenue, Q2"/>

## Breakdown by Region

```sql region_breakdown
SELECT region, sum(amount_usd) AS revenue
FROM marts.fct_orders JOIN marts.dim_customers USING (customer_id)
WHERE status = 'paid' AND order_date BETWEEN '2026-04-01' AND '2026-06-30'
GROUP BY 1 ORDER BY revenue DESC
```

<BarChart data={region_breakdown} x=region y=revenue/>
```

### Recipe 2 — Evidence source connection

`sources/snowflake/connection.yaml`:

```yaml
name: snowflake
type: snowflake

options:
  account: ab12345.us-east-1
  username: evidence_user
  database: ANALYTICS
  warehouse: REPORTS_WH
  role: ANALYST_ROLE
  authenticator: snowflake_jwt
  privateKeyPath: ./.evidence/private_key.p8
```

`.env`:

```bash
SNOWFLAKE_PASSWORD=...
# Or for OAuth, configure via Evidence settings
```

Then `npm run sources` caches query results into Parquet for fast page loads.

### Recipe 3 — Evidence build + deploy

```bash
npm run build                  # → build/ static HTML site
npx evidence deploy            # → Evidence Cloud (free tier)
# Or upload build/ to S3 / Netlify / Vercel
```

### Recipe 4 — Evidence components reference

```markdown
<Value data={daily} column=revenue fmt=usd0/>
<BigValue data={mrr} value=total comparison=growth_yoy comparisonFmt=pct1/>
<LineChart data={daily} x=date y=revenue/>
<BarChart data={by_region} x=region y=revenue/>
<DataTable data={top_customers} link=https://crm.example.com/customers/{customer_id}/>
<AreaChart data={mrr_breakdown} x=month y=revenue series=plan_tier/>
<Heatmap data={cohort_table} x=months_since y=cohort_month value=retention/>
```

## Common recipes — Streamlit

### Recipe 5 — Streamlit app with inputs + charts

```python
# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cohort Explorer", layout="wide")

st.title("Cohort Retention Explorer")

# Inputs
col1, col2, col3 = st.columns(3)
with col1:
    start = st.date_input("Cohort start", value=pd.Timestamp("2025-01-01"))
with col2:
    end = st.date_input("Cohort end", value=pd.Timestamp("2025-12-31"))
with col3:
    region = st.selectbox("Region", ["All", "US", "EU", "APAC"])

# Cached query
@st.cache_data(ttl=3600)
def load_data(start, end, region):
    import snowflake.connector
    conn = snowflake.connector.connect(**st.secrets["snowflake"])
    region_filter = "1=1" if region == "All" else f"region = '{region}'"
    df = pd.read_sql(f"""
        SELECT cohort_month, months_since, active_users, retention
        FROM marts.cohort_retention
        WHERE cohort_month BETWEEN '{start}' AND '{end}' AND {region_filter}
    """, conn)
    conn.close()
    return df

df = load_data(start, end, region)

# Layout
col_a, col_b = st.columns([2, 1])
with col_a:
    pivot = df.pivot(index="cohort_month", columns="months_since", values="retention")
    fig = px.imshow(pivot, color_continuous_scale="Blues", aspect="auto")
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    st.metric("Avg 30-day retention",
              f"{df[df.months_since==1].retention.mean():.1%}")
    st.metric("Avg 90-day retention",
              f"{df[df.months_since==3].retention.mean():.1%}")
    st.dataframe(df.head(20))
```

Run: `streamlit run app.py`.

### Recipe 6 — Streamlit secrets

`.streamlit/secrets.toml`:

```toml
[snowflake]
account = "ab12345.us-east-1"
user = "..."
password = "..."
warehouse = "COMPUTE_WH"
database = "ANALYTICS"
```

Use as `st.secrets["snowflake"]["account"]`.

### Recipe 7 — Streamlit deploy

```bash
# Streamlit Community Cloud (free)
# Push repo to GitHub → share.streamlit.io → connect repo

# Self-host via Docker
cat > Dockerfile <<'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
EOF
docker build -t my-app . && docker run -p 8501:8501 my-app
```

## Common recipes — Marimo

### Recipe 8 — Marimo reactive notebook

```python
# notebook.py — marimo generates this format
import marimo

__generated_with = "0.10.0"
app = marimo.App()

@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import plotly.express as px
    return mo, pd, px

@app.cell
def __(mo):
    # Reactive UI element — changes trigger downstream cells
    start = mo.ui.date(value="2025-01-01", label="Start date")
    end = mo.ui.date(value="2025-12-31", label="End date")
    region = mo.ui.dropdown(options=["All", "US", "EU", "APAC"], value="All")
    mo.hstack([start, end, region])
    return start, end, region

@app.cell
def __(pd, start, end, region):
    # Auto-reruns when start, end, or region changes
    import snowflake.connector
    conn = snowflake.connector.connect(...)
    region_filter = "1=1" if region.value == "All" else f"region = '{region.value}'"
    df = pd.read_sql(f"""
        SELECT cohort_month, months_since, active_users
        FROM marts.cohort_retention
        WHERE cohort_month BETWEEN '{start.value}' AND '{end.value}' AND {region_filter}
    """, conn)
    conn.close()
    return df,

@app.cell
def __(df, px):
    pivot = df.pivot(index="cohort_month", columns="months_since", values="active_users")
    fig = px.imshow(pivot, color_continuous_scale="Blues")
    fig
    return fig, pivot

if __name__ == "__main__":
    app.run()
```

Edit interactively: `marimo edit notebook.py`. Run as app: `marimo run notebook.py`.

### Recipe 9 — Marimo deploy

```bash
# Deploy as an HTTP app
marimo run notebook.py --host 0.0.0.0 --port 2718

# Export to static HTML (no Python server — uses WASM)
marimo export html-wasm notebook.py -o report.html
```

The WASM export runs Python entirely in the browser via Pyodide — no backend needed.

### Recipe 10 — Pandoc post-processing (any markdown → DOCX/PDF)

```bash
# Render Evidence build to markdown, then pandoc to DOCX
pandoc report.md \
  -o quarterly-review.docx \
  --reference-doc=company-template.docx \
  --toc --toc-depth=2

# Markdown → PDF (via wkhtmltopdf or weasyprint)
pandoc report.md -o report.pdf --pdf-engine=weasyprint
```

## Example end-to-end

**Goal:** Quarterly revenue review delivered as a polished HTML report and a DOCX for execs.

1. New Evidence project: `npx degit evidence-dev/template q2-review`.
2. Configure Snowflake source in `sources/snowflake/connection.yaml`.
3. Author `pages/index.md`: SQL blocks for MRR / cohort / channel breakdown; charts via `<LineChart>` etc.
4. `npm run sources && npm run build` → static HTML in `build/`.
5. Deploy: `npx evidence deploy` → shareable URL.
6. Convert to DOCX: render markdown via Pandoc with branded template for execs who prefer Word.
7. Schedule rebuild via GitHub Actions on cron; commit `data/` cache for reproducibility.

## Edge cases / gotchas

- **Evidence build vs sources** — `npm run sources` caches queries into `.evidence/.tmp/`; `npm run build` reads from cache. Forgetting `sources` first ships stale data.
- **Evidence component data shape** — `<LineChart data={query_name}>` expects the data variable name to match the SQL block alias. Typos silently render empty.
- **Streamlit reruns** — every widget interaction re-executes the script top-to-bottom. Use `@st.cache_data` to avoid redundant warehouse calls.
- **Streamlit state** — use `st.session_state` for cross-rerun state; otherwise variables reset.
- **Marimo reactive graph** — cells re-run when their dependencies change. If you forget to `return` a variable, downstream cells get None.
- **Marimo no global mutation** — by design, can't `global df`; this is the safety feature (no hidden state). Pass values via cell returns.
- **Streamlit on prod** — Community Cloud spins down idle apps (cold start ~30s). Use Snowflake/Streamlit native runtime or self-host for SLA workloads.
- **Evidence dynamic params** — Evidence supports URL params for inputs but doesn't replace a real BI tool's interactivity. Use Streamlit/Marimo for heavy interactivity.
- **Authentication** — Evidence Cloud + Streamlit Cloud have basic SSO; for enterprise, self-host with OAuth2-proxy.
- **WASM export limitations** — Marimo WASM can't open warehouse connections directly (no sockets). Pre-bake data as Parquet served with the HTML.
- **Versioned reports** — Evidence + Marimo are git-versionable (text-based). Streamlit is too, but secrets must live outside the repo.

## Sources

- [Evidence documentation](https://docs.evidence.dev/)
- [Evidence component reference](https://docs.evidence.dev/components/all-components/)
- [Streamlit documentation](https://docs.streamlit.io/)
- [Streamlit API reference](https://docs.streamlit.io/develop/api-reference)
- [Marimo documentation](https://docs.marimo.io/)
- [Marimo WASM deployment](https://docs.marimo.io/guides/wasm.html)
- [Pandoc manual](https://pandoc.org/MANUAL.html)
- [Evidence vs Streamlit vs Marimo comparison (2025)](https://docs.evidence.dev/why-evidence)
- role.md → "Notebook → report → dashboard pipeline"
