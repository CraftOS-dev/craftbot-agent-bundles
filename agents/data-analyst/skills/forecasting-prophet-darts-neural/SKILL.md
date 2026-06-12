<!--
Prophet: https://facebook.github.io/prophet/
Darts: https://unit8co.github.io/darts/
skforecast: https://skforecast.org/
statsmodels: https://www.statsmodels.org/stable/tsa.html
pmdarima: https://alkaline-ml.com/pmdarima/
Companion: role.md → "Forecasting playbook"
-->

# Forecasting — Prophet, Darts, skforecast, statsmodels

End-to-end time-series forecasting: Prophet for additive trend + seasonality + holidays (the easy default), statsmodels ARIMA / SARIMA for classical, Darts as unified API across exponential smoothing → NBEATS → TFT, skforecast for ML regressors as forecasters. Includes rolling-origin backtesting and prediction intervals.

## When to use

- "Forecast next quarter's MRR / users / orders / churn"
- "Daily / weekly data with strong seasonality + known holidays" → Prophet
- "Classical / interpretable forecast for finance team" → ARIMA / SARIMA
- "Multiple related series (per-region forecasts)" → Darts global models
- "Have ML features beyond the series itself" → skforecast
- "Need uncertainty quantification (PIs)" → all of the above support PIs

Defer A/B test math to `ab-test-significance-mde-sequential`. Defer anomaly detection to `anomaly-detection-statistical-ml`. Defer causal questions to `causal-inference-dag-iv-rdd`.

## Setup

```bash
pip install prophet                    # Meta's additive model
pip install darts                      # unified API
pip install skforecast                 # sklearn-style autoregression
pip install statsmodels pmdarima       # classical (incl. auto-ARIMA)
pip install pandas numpy matplotlib
```

Optional: GPU/torch for Darts neural models (`pip install darts[torch]`).

## Model selection decision tree

1. Daily/weekly data with seasonality + holidays + needs to be quick → **Prophet**
2. Classical reviewers, interpretability needed → **ARIMA / SARIMA** (statsmodels + pmdarima)
3. Multiple related series, neural for accuracy → **Darts** (NBEATS / NHiTS / TFT / TiDE)
4. Have exogenous ML features → **skforecast** (any sklearn regressor + autoregressive features)
5. Hierarchical reconciliation needed (totals must match) → **Darts hierarchical** or `hierarchicalforecast` package

## Common recipes

### Recipe 1 — Prophet quickstart

```python
from prophet import Prophet
import pandas as pd

# Prophet expects columns: ds (datetime), y (value)
df = data.rename(columns={"date": "ds", "revenue": "y"})

m = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    changepoint_prior_scale=0.05,      # higher = more flexible trend (default 0.05)
    seasonality_prior_scale=10,         # higher = more flexible seasonality
    interval_width=0.95,
)
m.add_country_holidays(country_name="US")
m.fit(df)

future = m.make_future_dataframe(periods=90)        # 90 days ahead
forecast = m.predict(future)

# Forecast columns: yhat, yhat_lower, yhat_upper, trend, weekly, yearly, holidays
m.plot(forecast)
m.plot_components(forecast)
```

### Recipe 2 — Prophet with additional regressors

```python
m = Prophet()
m.add_regressor("promo_active", standardize=True)
m.add_regressor("price_index", standardize=True)
m.add_regressor("competitor_promotions", standardize=True)
m.fit(df)

# Future must include the regressors
future["promo_active"] = ...
future["price_index"] = ...
future["competitor_promotions"] = ...
forecast = m.predict(future)
```

### Recipe 3 — Prophet backtesting (rolling-origin CV)

```python
from prophet.diagnostics import cross_validation, performance_metrics

df_cv = cross_validation(
    m,
    initial="730 days",       # initial training window
    period="30 days",          # how far apart to slide
    horizon="90 days",          # forecast horizon per fold
)

df_p = performance_metrics(df_cv)
print(df_p[["horizon", "mape", "smape", "mae", "rmse", "coverage"]])
# MAPE per horizon; coverage of 95% PI should be ≈ 0.95
```

### Recipe 4 — Auto-ARIMA (pmdarima)

```python
import pmdarima as pm

model = pm.auto_arima(
    train["y"],
    seasonal=True, m=7,                  # weekly seasonality
    stepwise=True, trace=False,
    suppress_warnings=True,
    error_action="ignore",
    information_criterion="aicc",
)
print(model.summary())

# Forecast with PI
n_periods = 30
forecast, conf_int = model.predict(n_periods=n_periods, return_conf_int=True, alpha=0.05)
```

### Recipe 5 — statsmodels SARIMA (manual order)

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX

# (p,d,q)(P,D,Q,m) — orders identified from ACF/PACF or via auto_arima
model = SARIMAX(
    endog=train["y"],
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 7),
    exog=train[["promo_active", "price_index"]],
)
fit = model.fit(disp=False)

# Forecast
forecast = fit.get_forecast(steps=30, exog=test[["promo_active", "price_index"]])
print(forecast.predicted_mean)
print(forecast.conf_int(alpha=0.05))      # 95% PI
```

### Recipe 6 — Darts unified API

```python
from darts import TimeSeries
from darts.models import ExponentialSmoothing, AutoARIMA, NBEATSModel, TFTModel, Prophet
from darts.metrics import mape, smape

# Build TimeSeries
series = TimeSeries.from_dataframe(df, time_col="date", value_cols="revenue")
train, val = series.split_after(0.85)

# Classical
model = ExponentialSmoothing()
model.fit(train)
forecast = model.predict(n=len(val), num_samples=500)         # probabilistic

# Deep learning (requires torch)
model = NBEATSModel(
    input_chunk_length=30,
    output_chunk_length=7,
    n_epochs=100,
    random_state=42,
)
model.fit(train, verbose=True)
forecast = model.predict(n=len(val), num_samples=500)         # probabilistic via dropout

# Quantile forecasts (uncertainty)
import matplotlib.pyplot as plt
series.plot()
forecast.plot(label="forecast", low_quantile=0.05, high_quantile=0.95)
plt.legend(); plt.show()

print(f"MAPE: {mape(val, forecast):.2f}%")
```

### Recipe 7 — Darts: global model across many series

```python
from darts import TimeSeries
from darts.models import TFTModel

# Multiple related series — one model trained jointly
series_per_region = [
    TimeSeries.from_dataframe(df[df.region == r], time_col="date", value_cols="revenue")
    for r in regions
]

# Cross-series covariates (static + future-known)
static_covs = [...]                # e.g., region characteristics
future_covs = [...]                # e.g., calendar features

model = TFTModel(
    input_chunk_length=30,
    output_chunk_length=14,
    hidden_size=64,
    lstm_layers=2,
    n_epochs=50,
    add_relative_index=True,
)
model.fit(series_per_region, future_covariates=future_covs, verbose=True)

forecast_per_region = model.predict(n=14, series=series_per_region, num_samples=500)
```

### Recipe 8 — skforecast (sklearn regressor as forecaster)

```python
from skforecast.recursive import ForecasterRecursive
from sklearn.ensemble import GradientBoostingRegressor

forecaster = ForecasterRecursive(
    regressor=GradientBoostingRegressor(n_estimators=200, max_depth=4, random_state=42),
    lags=[1, 2, 3, 7, 14, 28],                # autoregressive features
    window_features=None,                       # add rolling means/stds here
)

forecaster.fit(
    y=train["y"],
    exog=train[["promo_active", "price_index", "day_of_week"]],
)

# Forecast 30 steps with exogenous values
predictions = forecaster.predict(steps=30, exog=test[["promo_active", "price_index", "day_of_week"]])

# Backtest
from skforecast.model_selection import backtesting_forecaster, TimeSeriesFold

cv = TimeSeriesFold(steps=30, initial_train_size=len(train), refit=False)
metric, predictions = backtesting_forecaster(
    forecaster=forecaster,
    y=df["y"], exog=df[["promo_active","price_index","day_of_week"]],
    cv=cv, metric="mean_absolute_error",
)
print(f"Backtest MAE: {metric:.2f}")
```

### Recipe 9 — STL decomposition (interpretation)

```python
from statsmodels.tsa.seasonal import STL

stl = STL(series, period=7, robust=True)         # robust to outliers
result = stl.fit()

result.plot()       # 4 panels: observed / trend / seasonal / residual
print("Trend slope:", (result.trend.iloc[-1] - result.trend.iloc[0]) / len(result.trend))
print("Seasonal amplitude:", result.seasonal.max() - result.seasonal.min())
print("Residual std:", result.resid.std())       # benchmark for anomaly detection
```

### Recipe 10 — Forecast report template

```python
def forecast_report(actual, predicted, pi_lower, pi_upper, model_name):
    import numpy as np
    mape = np.mean(np.abs((actual - predicted) / actual)) * 100
    smape = np.mean(2 * np.abs(actual - predicted) / (np.abs(actual) + np.abs(predicted))) * 100
    mae = np.mean(np.abs(actual - predicted))
    rmse = np.sqrt(np.mean((actual - predicted) ** 2))
    coverage = ((actual >= pi_lower) & (actual <= pi_upper)).mean()

    return f"""
FORECAST REPORT
===============
Model:      {model_name}
Horizon:    {len(actual)} periods

Point accuracy:
- MAPE:  {mape:.2f}%
- sMAPE: {smape:.2f}%
- MAE:   {mae:.2f}
- RMSE:  {rmse:.2f}

Uncertainty:
- 95% PI coverage: {coverage:.1%}  (target: 95%)

Caveats:
- Stationarity:  <assessed via ADF test>
- Structural breaks: <none / list of breakpoints>
- Out-of-distribution risk: <flag if forecast extrapolates beyond observed range>
"""
```

## Example end-to-end

**Goal:** Forecast next 90 days of daily revenue with 95% PI; backtested.

1. Load 2+ years of daily revenue from warehouse.
2. EDA: STL decomposition (Recipe 9) — confirms weekly + yearly seasonality.
3. Add regressors: `promo_active`, `holiday`, `day_of_week_dummies`.
4. Fit Prophet with US holidays (Recipe 2).
5. Rolling-origin CV (Recipe 3) — `mape=4.8%`, 95% PI coverage = 92% (slightly underconfident).
6. Compare to Darts NBEATS (Recipe 6) — NBEATS MAPE=4.2%; pick NBEATS for production.
7. Generate 90-day forecast with quantile bands.
8. Deliverable per Recipe 10 template.
9. Schedule daily refit via Airflow; alert when point forecast deviates >2σ from incoming actuals.

## Edge cases / gotchas

- **Stationarity** — ARIMA assumes stationarity; check via ADF / KPSS tests. Differencing (`d=1` or higher) handles trend; seasonal differencing for seasonal series.
- **Holidays beyond US** — Prophet's built-in holidays cover 40+ countries; for company-specific events (sale dates, product launches), supply custom DataFrame.
- **Outliers** — Prophet is somewhat robust; for severe outliers, winsorize or use a robust loss (Darts allows loss customization).
- **Structural breaks** — sudden regime change (COVID, pricing model change). Prophet's `changepoint_prior_scale` increases responsiveness; consider segmenting training data.
- **Train/test split must be temporal** — random splits leak future into past. Use TimeSeriesSplit / rolling-origin.
- **PI coverage check** — if 95% PI coverage is far from 95% in backtest, the model is mis-calibrated; reduce or recalibrate.
- **Hierarchy reconciliation** — if you forecast per-region and totals don't match the all-region forecast, reconcile via `hierarchicalforecast`.
- **Sparse data / zeros** — for intermittent demand (most days zero), use Croston's method or specialized intermittent-demand models.
- **Forecast horizon vs. training-window ratio** — keep horizon < 20% of training history. Forecasting 1 year from 1 year of data is unreliable.
- **Out-of-distribution exogenous values** — if future regressors include unseen values (e.g., promo discount you've never run), the model extrapolates blindly.
- **Auto-ARIMA computational cost** — `stepwise=True` is fast; `stepwise=False` exhaustive but slow. Limit search via `max_p`, `max_q`.
- **Darts deep models need GPU for large series** — TFT/NHiTS on CPU works but is slow; benchmark before committing.

## Sources

- [Prophet documentation](https://facebook.github.io/prophet/)
- [Prophet cross-validation](https://facebook.github.io/prophet/docs/diagnostics.html)
- [Darts documentation](https://unit8co.github.io/darts/)
- [Darts model selector](https://unit8co.github.io/darts/userguide/models.html)
- [skforecast user guide](https://skforecast.org/latest/user_guides/user-guides)
- [statsmodels SARIMAX](https://www.statsmodels.org/stable/generated/statsmodels.tsa.statespace.sarimax.SARIMAX.html)
- [pmdarima auto-ARIMA](https://alkaline-ml.com/pmdarima/auto_examples/example_simple_fit.html)
- [Forecasting: Principles and Practice (Hyndman, 3rd ed.)](https://otexts.com/fpp3/)
- role.md → "Forecasting playbook"
