<!--
scikit-learn clustering: https://scikit-learn.org/stable/modules/clustering.html
HDBSCAN: https://hdbscan.readthedocs.io/
Companion: role.md → "Customer segmentation playbook"
-->

# Customer segmentation — RFM, behavioral, ML clustering

Three-tier segmentation: RFM quintiles via SQL `NTILE(5)`, behavioral clusters via k-means on engagement features, ML-based via HDBSCAN / GMM for arbitrary shapes. Includes silhouette + business-validity checks and segment-action mapping.

## When to use

- "Segment our customers into actionable groups"
- "RFM quintiles for email campaign targeting"
- "Behavioral clusters from product-usage telemetry"
- "Find power users vs casual users vs at-risk"
- "Personalized pricing tier mapping"

Defer cohort retention to `cohort-retention-deep-survival`. Defer A/B test math to `ab-test-significance-mde-sequential`. Defer attribution to `attribution-multi-touch-mmm`.

## Setup

```bash
pip install scikit-learn pandas numpy
pip install hdbscan                       # density-based clustering
pip install umap-learn                    # nonlinear dim reduction for viz
pip install plotly matplotlib seaborn
```

No external auth; warehouse credentials for source data.

## Segmentation method-selection

| Method | When to use | Pros | Cons |
|---|---|---|---|
| **RFM quintiles** | Quick reporting; CRM email targeting | Explainable, SQL-native | Only 3 dimensions; ignores other behavior |
| **k-means** | Continuous features, ~spherical clusters | Scalable, well-known | Needs k; assumes spherical |
| **GMM** | Continuous + soft assignments | Probabilistic cluster membership | Slower; needs k |
| **HDBSCAN** | Arbitrary shapes, unknown k | No k needed; finds noise | Sensitive to scale, less intuitive |
| **Hierarchical** | Need a dendrogram for interpretation | Visualization | Slow at scale (O(n²)) |

## Common recipes

### Recipe 1 — RFM quintiles in SQL

```sql
WITH rfm_base AS (
    SELECT
        customer_id,
        DATEDIFF('day', MAX(order_at), CURRENT_DATE) AS recency_days,
        COUNT(*) AS frequency,
        SUM(order_value) AS monetary
    FROM fct_orders
    WHERE order_at > CURRENT_DATE - INTERVAL '365 days'
    GROUP BY 1
),
quintiles AS (
    SELECT
        customer_id,
        recency_days,
        frequency,
        monetary,
        NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,    -- low recency_days = 5
        NTILE(5) OVER (ORDER BY frequency)         AS f_score,
        NTILE(5) OVER (ORDER BY monetary)          AS m_score
    FROM rfm_base
)
SELECT
    customer_id, recency_days, frequency, monetary,
    r_score, f_score, m_score,
    r_score * 100 + f_score * 10 + m_score AS rfm_code,
    CASE
        WHEN r_score = 5 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
        WHEN r_score >= 4 AND f_score >= 3                  THEN 'Loyal'
        WHEN r_score = 5 AND f_score <= 2                  THEN 'New'
        WHEN r_score <= 2 AND f_score >= 4                  THEN 'At Risk'
        WHEN r_score <= 2 AND f_score <= 2 AND m_score >= 4 THEN 'Hibernating Big Spender'
        WHEN r_score = 1 AND f_score = 1                    THEN 'Lost'
        ELSE 'Standard'
    END AS segment
FROM quintiles;
```

### Recipe 2 — k-means on behavioral features

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Features per customer
features = df[[
    "sessions_per_week",
    "avg_session_minutes",
    "unique_features_used",
    "support_tickets_per_month",
    "feature_X_usage_rate",
    "weekend_activity_share",
    "mobile_share",
]]

# Scale (essential for distance-based methods)
scaler = StandardScaler()
X = scaler.fit_transform(features)

# Pick k via silhouette + elbow
results = []
for k in range(2, 10):
    km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X)
    sil = silhouette_score(X, km.labels_)
    inertia = km.inertia_
    results.append({"k": k, "silhouette": sil, "inertia": inertia})

import pandas as pd
metrics_df = pd.DataFrame(results)
print(metrics_df)

# Pick k=5 (typical sweet spot)
km = KMeans(n_clusters=5, random_state=42, n_init=10).fit(X)
df["segment"] = km.labels_
```

### Recipe 3 — Cluster profiling

```python
# Mean of each feature per cluster — interpret what each segment "is"
profile = features.assign(segment=km.labels_).groupby("segment").mean().round(2)
print(profile)

# Cluster size + share
sizes = pd.Series(km.labels_).value_counts().sort_index()
print(sizes / len(km.labels_))

# Quick name suggestions
def name_cluster(row):
    if row["sessions_per_week"] > 5 and row["unique_features_used"] > 10: return "Power Users"
    if row["sessions_per_week"] < 1: return "Dormant"
    if row["support_tickets_per_month"] > 2: return "High-Touch / Struggling"
    if row["mobile_share"] > 0.8: return "Mobile-First"
    return "Standard"

profile["suggested_name"] = profile.apply(name_cluster, axis=1)
print(profile)
```

### Recipe 4 — HDBSCAN (arbitrary shapes, no k)

```python
import hdbscan
from sklearn.preprocessing import StandardScaler

X = StandardScaler().fit_transform(features)

clusterer = hdbscan.HDBSCAN(
    min_cluster_size=200,        # min points per cluster
    min_samples=20,
    cluster_selection_method="eom",   # "eom" or "leaf"
    metric="euclidean",
)
labels = clusterer.fit_predict(X)
df["segment"] = labels
# -1 = noise (point doesn't belong to any cluster)
print(pd.Series(labels).value_counts())
print(f"Noise share: {(labels == -1).mean():.1%}")
```

### Recipe 5 — UMAP for visualization

```python
import umap.umap_ as umap
import matplotlib.pyplot as plt

reducer = umap.UMAP(n_neighbors=30, min_dist=0.1, n_components=2, random_state=42)
embedding = reducer.fit_transform(X)

fig, ax = plt.subplots(figsize=(10, 8))
scatter = ax.scatter(embedding[:, 0], embedding[:, 1], c=df["segment"], cmap="tab10", s=8, alpha=0.6)
ax.set_title("Customer segments — UMAP projection")
plt.colorbar(scatter, label="Segment")
plt.savefig("segments_umap.png", dpi=150)
```

### Recipe 6 — Gaussian Mixture Model (soft assignment)

```python
from sklearn.mixture import GaussianMixture

gmm = GaussianMixture(n_components=5, covariance_type="full", random_state=42, n_init=10)
gmm.fit(X)
df["segment_hard"] = gmm.predict(X)
df["segment_proba"] = list(gmm.predict_proba(X))     # array of probabilities

# Customers with uncertain membership (no segment >70% confidence)
uncertain = df[df["segment_proba"].apply(max) < 0.7]
print(f"Uncertain assignment: {len(uncertain)} / {len(df)}")

# Model selection: lowest BIC over k
for k in range(2, 10):
    gmm_k = GaussianMixture(n_components=k, random_state=42).fit(X)
    print(k, gmm_k.bic(X), gmm_k.aic(X))
```

### Recipe 7 — Segment validation: retention curves

```python
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))
for segment in sorted(df["segment"].unique()):
    seg_df = df[df["segment"] == segment]
    kmf = KaplanMeierFitter()
    kmf.fit(seg_df["tenure_days"], seg_df["churned"], label=f"Segment {segment} (n={len(seg_df)})")
    kmf.plot_survival_function(ax=ax, ci_show=True)
plt.title("Retention by segment — sanity check")
plt.xlabel("Days since signup")
plt.ylabel("P(active)")
plt.savefig("segment_retention.png", dpi=150)

# Statistical comparison (log-rank multivariate)
from lifelines.statistics import multivariate_logrank_test
result = multivariate_logrank_test(df["tenure_days"], df["segment"], df["churned"])
print(f"Log-rank: p = {result.p_value:.4f}")
```

If segments don't differ on retention (or LTV, or any outcome you care about), the segmentation isn't useful — re-cluster with different features.

### Recipe 8 — Segment-action mapping template

```
SEGMENT REPORT
==============

Method: <RFM / k-means / HDBSCAN / GMM>
Features: <list>
Cluster count: <k>
Silhouette: <X> (target >0.3)
Noise share (HDBSCAN): <X%>

PER-SEGMENT PROFILE:
| Segment           | Size  | LTV (median) | 90d retention | Avg sessions/wk | Action                                |
|-------------------|-------|--------------|---------------|-----------------|---------------------------------------|
| Champions         | 8.4%  | $4,800       | 92%           | 18              | VIP program + retention rewards       |
| Loyal             | 22.1% | $2,100       | 78%           | 8               | Cross-sell adjacent product           |
| New & Promising   | 11.5% | $850         | 55%           | 4               | Onboarding nudge + Aha-moment trigger |
| At Risk           | 14.0% | $1,200       | 31%           | 1.5             | Re-engagement campaign + offer        |
| Hibernating Spend | 5.2%  | $3,400       | 12%           | 0.3             | Win-back personal outreach            |
| Lost              | 28.5% | $400         | 4%            | 0.1             | Skip — opportunity cost too high      |
| Standard          | 10.3% | $700         | 48%           | 3               | Standard lifecycle                    |
```

### Recipe 9 — Feature engineering best practices

```python
# Time-decayed features (recency-weighted)
import numpy as np

def time_decay(events, decay=0.05):
    """Sum events weighted by exp(-decay * days_ago)."""
    return np.sum(np.exp(-decay * events["days_ago"]) * events["value"])

# Standardization vs log-transform
import numpy as np

# Heavy-tailed features (revenue, page views) — log-transform first
features["log_monetary"] = np.log1p(features["monetary"])

# Skewness check
from scipy.stats import skew
print({c: skew(features[c]) for c in features.columns})
# > |2| = highly skewed → log-transform
```

### Recipe 10 — Production scoring pipeline

```python
import joblib

# Train + save
joblib.dump(scaler, "scaler.pkl")
joblib.dump(km, "kmeans.pkl")

# Score new customers daily
def score_customer(customer_features_df):
    scaler = joblib.load("scaler.pkl")
    km = joblib.load("kmeans.pkl")
    X = scaler.transform(customer_features_df[FEATURE_COLS])
    return km.predict(X)

# Daily refresh
df_today = pd.read_sql("SELECT * FROM marts.customer_features WHERE feature_date = current_date", con)
df_today["segment"] = score_customer(df_today)

# Push back to warehouse (reverse ETL)
df_today[["customer_id", "segment"]].to_sql("dim_customer_segments", con, if_exists="replace")
```

## Example end-to-end

**Goal:** Segment 200k customers for personalized retention campaigns.

1. Pull features: RFM + engagement metrics + product-usage (Recipe 9 standardization).
2. Try RFM quintiles (Recipe 1) for quick win — 7 named segments.
3. Build behavioral k-means with k=5 (Recipe 2-3) — discovers 2 segments not visible in RFM.
4. Validate: log-rank on retention by segment (Recipe 7) — p<0.001, segments differ meaningfully.
5. Cross-tab RFM × behavioral: power-users include both high-RFM and low-RFM "new but engaged" customers.
6. Map segments → actions (Recipe 8 template).
7. Reverse-ETL segment labels to CRM (Census/Hightouch — see that skill).
8. A/B test re-engagement campaign on "At Risk" segment vs holdout.
9. Re-run segmentation quarterly; track membership drift.

## Edge cases / gotchas

- **Scaling matters** — distance-based methods (k-means, HDBSCAN) require StandardScaler or MinMaxScaler. Otherwise, large-range features dominate.
- **Skewed features** — log-transform `monetary`, `frequency` before clustering; otherwise extreme outliers form their own cluster.
- **Silhouette > 0.3 is the rough threshold** — below that, clusters are weak. Above 0.5 is strong.
- **High k can overfit** — many small clusters that won't generalize. Cap k at business-sensible 4-7.
- **HDBSCAN noise points** — flag as "Unclustered" segment; for actionable use, force them into the nearest cluster via `approximate_predict`.
- **Categorical features** — k-means doesn't natively support. Use one-hot + Gower distance + `gower` package, or KModes.
- **Segment drift** — customer behavior shifts; segment membership decays. Re-fit quarterly.
- **Sensitivity to random_state** — k-means initialization matters; use `n_init=10` and fix `random_state`.
- **Curse of dimensionality** — with 20+ features, distances become uniform. Use UMAP/PCA for dimension reduction first.
- **Business validity over statistical validity** — silhouette 0.6 but segments are uninterpretable = useless. Segments must map to actions.
- **Causation again** — being in a high-LTV segment correlates with future LTV; it doesn't *cause* it. Use A/B testing to validate that targeting segment X with action Y improves outcome.
- **Privacy** — segments are PII when revealing sensitive groupings. Apply data minimization and consent.

## Sources

- [scikit-learn — clustering](https://scikit-learn.org/stable/modules/clustering.html)
- [scikit-learn — k-means](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)
- [HDBSCAN documentation](https://hdbscan.readthedocs.io/)
- [UMAP documentation](https://umap-learn.readthedocs.io/)
- [Silhouette score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html)
- [RFM segmentation — original paper (Hughes 1996)](https://www.researchgate.net/publication/235955488)
- [Customer segmentation best practices (Optimove 2025)](https://www.optimove.com/blog/customer-segmentation)
- role.md → "Customer segmentation playbook"
