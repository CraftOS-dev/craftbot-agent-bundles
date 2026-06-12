<!--
PyOD: https://pyod.readthedocs.io/
ADTK: https://adtk.readthedocs.io/
Prophet residuals: https://facebook.github.io/prophet/
Companion: role.md → "Anomaly detection playbook"
-->

# Anomaly detection — statistical + ML, time-series + multivariate

Detect anomalies via statistical methods (rolling z-score, MAD, ESD, STL residuals, Prophet PI breach) and ML methods (Isolation Forest, One-Class SVM, autoencoder reconstruction). Wire into production monitoring with dynamic thresholds and business-context overlays.

## When to use

- "Alert me when MAU drops X%" → rolling threshold + Prophet residuals
- "Flag outliers in this multivariate feature set" → Isolation Forest / PyOD
- "Detect anomalies in a time series with trend + seasonality" → ADTK + STL
- "Production metric monitoring" → dynamic thresholds, not static cutoffs
- "Find unusual customers / orders / sessions" → PyOD multivariate

Defer forecasting itself to `forecasting-prophet-darts-neural`. Defer data-quality contracts to `great-expectations-soda-data-quality`. Defer A/B / experimentation to `ab-test-significance-mde-sequential`.

## Setup

```bash
pip install pyod                          # 40+ algorithms
pip install adtk                          # time-series toolkit
pip install scikit-learn                  # IsolationForest, OneClassSVM
pip install statsmodels                   # ESD, STL
pip install prophet                       # Prophet + outlier removal
pip install pandas numpy matplotlib
```

## Method-selection matrix

| Data type | Recommended | Why |
|---|---|---|
| Univariate time series with trend + seasonality | STL residuals + threshold | Removes structure first |
| Univariate, no seasonality | Rolling z-score / MAD | Simple, fast |
| Multiple time series | Prophet PI breach | Per-series confidence band |
| Multivariate i.i.d. (transactions / sessions) | IsolationForest / LOF / ABOD | Distribution-free |
| High-dim + abundant data | Autoencoder reconstruction | Learns latent manifold |
| Streaming / online | River library | Incremental learning |

## Common recipes

### Recipe 1 — Rolling z-score (univariate)

```python
import pandas as pd
import numpy as np

window = 28
df["rolling_mean"] = df["metric"].rolling(window, min_periods=14).mean()
df["rolling_std"]  = df["metric"].rolling(window, min_periods=14).std()
df["z_score"] = (df["metric"] - df["rolling_mean"]) / df["rolling_std"]
df["anomaly_z"] = df["z_score"].abs() > 3.0

anomalies = df[df["anomaly_z"]][["date", "metric", "z_score"]]
print(anomalies)
```

### Recipe 2 — MAD (robust to outliers in window)

```python
from scipy.stats import median_abs_deviation

window = 28
df["rolling_median"] = df["metric"].rolling(window, min_periods=14).median()
df["rolling_mad"] = df["metric"].rolling(window, min_periods=14).apply(
    lambda x: median_abs_deviation(x, scale="normal")
)
df["mad_score"] = (df["metric"] - df["rolling_median"]) / df["rolling_mad"]
df["anomaly_mad"] = df["mad_score"].abs() > 3.5
```

MAD is preferred when the window itself may contain outliers (rolling std becomes inflated).

### Recipe 3 — Generalized ESD test (statsmodels)

```python
from statsmodels.stats.diagnostic import generalized_esd_test

# Returns (test_statistics, critical_values, n_outliers)
n_outliers, indices = generalized_esd_test(df["metric"].dropna(), alpha=0.05, max_outliers=10)
print(f"Detected {n_outliers} outliers at indices {indices}")
df.loc[indices, "anomaly_esd"] = True
```

### Recipe 4 — STL residuals (decomposition-based)

```python
from statsmodels.tsa.seasonal import STL

stl = STL(df["metric"], period=7, robust=True).fit()
residuals = stl.resid

threshold = 3 * residuals.std()
df["anomaly_stl"] = residuals.abs() > threshold

# Visual
import matplotlib.pyplot as plt
fig, axes = plt.subplots(4, 1, figsize=(12, 8), sharex=True)
stl.observed.plot(ax=axes[0], title="Observed")
stl.trend.plot(ax=axes[1], title="Trend")
stl.seasonal.plot(ax=axes[2], title="Seasonal")
residuals.plot(ax=axes[3], title="Residuals")
axes[3].axhline(threshold, color="red", linestyle="--")
axes[3].axhline(-threshold, color="red", linestyle="--")
plt.savefig("stl_decomposition.png", dpi=150)
```

### Recipe 5 — Prophet residuals (PI breach)

```python
from prophet import Prophet
import pandas as pd

df = data.rename(columns={"date": "ds", "metric": "y"})
m = Prophet(interval_width=0.99)        # 99% PI for tight anomaly threshold
m.fit(df)

forecast = m.predict(df[["ds"]])
joined = df.merge(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]], on="ds")
joined["anomaly_prophet"] = (joined["y"] < joined["yhat_lower"]) | (joined["y"] > joined["yhat_upper"])

print(joined[joined["anomaly_prophet"]][["ds", "y", "yhat", "yhat_lower", "yhat_upper"]])
```

### Recipe 6 — ADTK (curated time-series detectors)

```python
import pandas as pd
from adtk.data import validate_series
from adtk.detector import (
    ThresholdAD, QuantileAD, InterQuartileRangeAD,
    LevelShiftAD, VolatilityShiftAD, PersistAD, AutoregressionAD
)

s = validate_series(df.set_index("date")["metric"])

# Static threshold
det1 = ThresholdAD(low=100, high=10_000)
anomalies1 = det1.detect(s)

# Dynamic quantile threshold
det2 = QuantileAD(low=0.01, high=0.99).fit_detect(s)

# IQR-based
det3 = InterQuartileRangeAD(c=3.0).fit_detect(s)

# Level shift (regime change)
det4 = LevelShiftAD(window=28, c=6.0).fit_detect(s)

# Volatility shift
det5 = VolatilityShiftAD(window=28).fit_detect(s)

# Autoregressive deviation
det6 = AutoregressionAD(n_steps=7, c=3.0).fit_detect(s)
```

### Recipe 7 — Isolation Forest (multivariate i.i.d.)

```python
from sklearn.ensemble import IsolationForest

# Features per row — could be per-customer, per-order, per-session
X = df[["amount", "n_items", "time_on_site", "device_score", "ip_risk"]]

iso = IsolationForest(
    n_estimators=200,
    contamination=0.01,      # expected anomaly fraction; "auto" lets sklearn pick
    random_state=42,
)
iso.fit(X)
df["anomaly_iforest"] = (iso.predict(X) == -1)
df["iforest_score"] = -iso.score_samples(X)        # higher = more anomalous

# Inspect highest-score rows
top_anomalies = df.nlargest(20, "iforest_score")
```

### Recipe 8 — PyOD multi-model ensemble

```python
from pyod.models.iforest import IForest
from pyod.models.lof import LOF
from pyod.models.knn import KNN
from pyod.models.ecod import ECOD
from pyod.models.combination import maximization, average

# Fit multiple detectors
detectors = {
    "iforest": IForest(contamination=0.01).fit(X),
    "lof": LOF(contamination=0.01, n_neighbors=20).fit(X),
    "knn": KNN(contamination=0.01).fit(X),
    "ecod": ECOD(contamination=0.01).fit(X),       # 2022 SOTA, parameter-free
}

scores = np.column_stack([d.decision_function(X) for d in detectors.values()])
# Combine (max ensemble = "outlier per any detector")
ensemble_score = maximization(scores)
threshold = np.quantile(ensemble_score, 0.99)
df["anomaly_ensemble"] = ensemble_score > threshold
```

### Recipe 9 — Production monitoring template

```python
import pandas as pd

class MetricMonitor:
    def __init__(self, metric_name, prophet_model=None, k_sigma=3.0):
        self.metric_name = metric_name
        self.prophet = prophet_model
        self.k = k_sigma

    def fit(self, history):
        if self.prophet is None:
            from prophet import Prophet
            self.prophet = Prophet(interval_width=0.99)
        df = history.rename(columns={"date": "ds", self.metric_name: "y"})
        self.prophet.fit(df)
        residuals = (df["y"] - self.prophet.predict(df[["ds"]])["yhat"])
        self.resid_std = residuals.std()
        return self

    def check(self, new_row):
        forecast = self.prophet.predict(pd.DataFrame({"ds": [new_row["date"]]}))
        yhat, lo, hi = forecast.iloc[0][["yhat", "yhat_lower", "yhat_upper"]]
        residual = new_row[self.metric_name] - yhat

        severity = abs(residual) / self.resid_std
        if severity > 4:    level = "PAGE"
        elif severity > 3:  level = "ALERT"
        elif severity > 2:  level = "WARN"
        else:               level = "OK"

        return {
            "level": level, "severity_sigma": severity,
            "value": new_row[self.metric_name], "predicted": yhat,
            "pi_99": (lo, hi),
        }

monitor = MetricMonitor("dau").fit(history_df)
result = monitor.check({"date": "2026-06-09", "dau": 4_200})
print(result)
```

### Recipe 10 — Root-cause drilldown when an anomaly fires

```python
import pandas as pd

def drilldown_anomaly(metric_df, anomaly_date, group_cols, value_col, baseline_window=28):
    """When an anomaly fires, identify the segment(s) contributing most to the deviation."""
    pre = metric_df[
        (metric_df["date"] >= anomaly_date - pd.Timedelta(days=baseline_window))
        & (metric_df["date"] < anomaly_date)
    ]
    anomaly = metric_df[metric_df["date"] == anomaly_date]

    pre_avg = pre.groupby(group_cols)[value_col].mean().rename("baseline")
    anomaly_val = anomaly.groupby(group_cols)[value_col].sum().rename("observed")

    joined = pd.concat([pre_avg, anomaly_val], axis=1).fillna(0)
    joined["delta"] = joined["observed"] - joined["baseline"]
    joined["delta_pct"] = joined["delta"] / joined["baseline"].replace(0, np.nan)
    return joined.sort_values("delta", key=abs, ascending=False).head(20)

drilldown_anomaly(events_df, anomaly_date="2026-06-09", group_cols=["region", "device"],
                  value_col="active_users")
```

## Example end-to-end

**Goal:** Production monitor for daily MRR with Slack alerts on anomalies.

1. Load 2 years of daily MRR.
2. Fit Prophet model with country holidays + business-known event dummies.
3. Compute residuals; std=$45k.
4. Wire monitor via Airflow DAG: every morning, fetch yesterday's MRR.
5. Predict with Prophet; compute severity = residual / std.
6. If severity > 3, fire Slack alert with drill-down (Recipe 10) showing top-deviating segments.
7. If severity > 4, page on-call.
8. Weekly: re-train Prophet with last week's data; suppress alerts for known event windows (launch, holiday spike).

## Edge cases / gotchas

- **Static thresholds are wrong** — a value of "DAU = 4,200" is anomalous in March but normal in August. Always use rolling/dynamic thresholds.
- **Contamination parameter sensitivity** — IsolationForest's `contamination` strongly affects the boundary; estimate from historical or use `"auto"`.
- **Seasonality leakage** — running z-score on a series with weekly seasonality flags every Tuesday as anomalous. Decompose first (STL) or use Prophet residuals.
- **Concept drift** — a model trained on Q1 data won't recognize Q4 patterns; re-train weekly or monthly.
- **Multiple-test correction** — when monitoring 200 metrics, ~10 will fire daily by chance at 5%. Apply Bonferroni or set per-metric severity thresholds higher.
- **Alert fatigue** — tier alerts (WARN/ALERT/PAGE) so non-critical anomalies don't page humans.
- **Known event windows** — exclude product launches, marketing campaigns, holidays before computing residuals; or supply them as Prophet regressors.
- **Anomaly ≠ root cause** — detection tells you something changed; drill-down (Recipe 10) tells you where.
- **Survivorship bias in training** — if your historical "normal" data already excludes prior anomalies, the model thinks current outliers are extreme. Keep modest anomalies in training to calibrate.
- **PyOD `decision_function` direction** — for some detectors higher = outlier (IsolationForest after sign flip), for others lower; check `__init__` docstrings.
- **ADTK series validation** — requires monotonic datetime index; gaps trigger errors. Resample to regular frequency first.
- **Real-time inference latency** — Prophet predict per-point is ~5-50ms; not suitable for sub-second streams. Use lighter models (rolling z-score) for high-frequency monitoring.

## Sources

- [PyOD documentation](https://pyod.readthedocs.io/)
- [PyOD algorithm comparison](https://pyod.readthedocs.io/en/latest/pyod.html)
- [ADTK documentation](https://adtk.readthedocs.io/)
- [statsmodels — STL decomposition](https://www.statsmodels.org/stable/examples/notebooks/generated/stl_decomposition.html)
- [statsmodels — Generalized ESD test](https://www.statsmodels.org/stable/generated/statsmodels.stats.diagnostic.generalized_esd_test.html)
- [Prophet — anomaly detection via outlier residuals](https://facebook.github.io/prophet/docs/outliers.html)
- [scikit-learn IsolationForest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)
- [ECOD (2022) — parameter-free anomaly detection](https://arxiv.org/abs/2201.00382)
- role.md → "Anomaly detection playbook"
