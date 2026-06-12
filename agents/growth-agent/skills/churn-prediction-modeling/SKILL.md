<!--
Source: CamDavidsonPilon lifelines SaaS churn notebook + saaslatestnews 2026 AI-powered churn + Andrew Chen retention
-->
# Churn Prediction Modeling — lifelines Cox PH + LLM Signals SKILL

> Predict per-user time-to-churn using lifelines survival analysis (Cox Proportional Hazards, Kaplan-Meier, AFT). 2026 SOTA: augment structured features with LLM-extracted signals from tickets, NPS comments, and call transcripts. Output at-risk cohorts piped to win-back skills.

## When to use

Trigger phrases:
- "Predict churn"
- "Who's about to churn?"
- "Survival analysis for SaaS"
- "Cox PH model"
- "Score users by churn risk"
- "Pipe at-risk users to win-back"

Pair: `retention-curve-churn-diagnosis-j-smile` (diagnose shape FIRST; predict only on J/flat shapes — decay = activation problem), `win-back-campaigns` (downstream action), `pql-product-qualified-leads-framework` (positive analog of same scoring approach).

## Setup

```bash
export POSTHOG_PERSONAL_API_KEY="phx_..."
export POSTGRES_URL="postgresql://..."

# Install via cli-anything uvx (ephemeral)
# uvx --from lifelines python -c "from lifelines import CoxPHFitter; print('OK')"
pip install lifelines pandas numpy scikit-learn matplotlib

# For LLM signals
pip install anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Survival analysis canonical models

| Model | When to use | Strength | Limitation |
|---|---|---|---|
| **Kaplan-Meier** | Group-level survival curve | Non-parametric, no assumptions | No covariates |
| **Cox Proportional Hazards** | Per-feature hazard ratios | Interpretable per feature | Assumes proportional hazards |
| **Accelerated Failure Time (AFT)** | When PH assumption violated | Direct time-to-event predict | Distributional assumption |
| **Random Survival Forests** | Non-linear, many features | High predictive | Less interpretable |
| **DeepSurv / Pycox** | Big data, deep features | Best predictive | Black box, infra |

Default: Cox PH for interpretability + Kaplan-Meier for group curves.

## Common recipes

### Recipe 1: Data preparation (cohort + features + churn event)

```python
import pandas as pd
import psycopg2

# Pull cohort with tenure + event + features
conn = psycopg2.connect(POSTGRES_URL)
df = pd.read_sql("""
  SELECT
    user_id,
    DATEDIFF('day', signup_date, COALESCE(churn_date, CURRENT_DATE)) AS tenure_days,
    CASE WHEN churn_date IS NOT NULL THEN 1 ELSE 0 END AS churned,
    -- Structured features
    feature_adoption_count,
    team_size,
    weekly_active_days_avg,
    nps_score,
    support_tickets_count,
    plan_tier,
    monthly_revenue,
    -- Time-since-last-action
    days_since_last_session,
    days_since_last_core_action,
    -- Lifecycle
    onboarding_completed,
    activation_event_hit
  FROM analytics.users
  WHERE signup_date >= now() - INTERVAL '24 months'
""", conn)

# Encode categorical
df = pd.get_dummies(df, columns=['plan_tier'], drop_first=True)
df = df.dropna()  # or fillna with median; depends on missing-data semantics
```

### Recipe 2: Cox PH model

```python
from lifelines import CoxPHFitter

cph = CoxPHFitter()
cph.fit(df, duration_col='tenure_days', event_col='churned')
cph.print_summary()

# Hazard ratios:
# exp(coef) > 1.0 → feature increases churn risk
# exp(coef) < 1.0 → feature decreases churn risk
# p < 0.05 → statistically significant
```

Interpretation example:
- `team_size` HR = 0.42, p < 0.001 → each +1 team member halves churn risk
- `days_since_last_session` HR = 1.08, p < 0.001 → each +1 day idle → 8% more churn risk

### Recipe 3: Kaplan-Meier survival curves per segment

```python
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt

kmf = KaplanMeierFitter()

for tier in df['plan_tier'].unique():
    sub = df[df['plan_tier'] == tier]
    kmf.fit(sub['tenure_days'], event_observed=sub['churned'], label=tier)
    kmf.plot_survival_function()

plt.xlabel('Tenure (days)')
plt.ylabel('Survival probability')
plt.title('Survival curves by plan tier')
plt.savefig('survival_by_tier.png')
```

Shows: probability of being alive at day N per group.

### Recipe 4: Predict at-risk cohort (30-day survival)

```python
# For each current user, predict 30-day survival probability
df['surv_30'] = cph.predict_survival_function(df, times=[30]).T.iloc[:, 0]

# At-risk = < 70% chance of surviving 30 days
at_risk = df[df['surv_30'] < 0.70].sort_values('surv_30')

# Pipe to Customer.io / Klaviyo for win-back
at_risk[['user_id', 'surv_30', 'tenure_days']].to_csv('at_risk_users.csv', index=False)
```

### Recipe 5: Accelerated Failure Time (when PH violated)

```python
from lifelines import WeibullAFTFitter

aft = WeibullAFTFitter()
aft.fit(df, duration_col='tenure_days', event_col='churned')
aft.print_summary()

# Direct predicted time-to-churn
df['predicted_churn_day'] = aft.predict_median(df)
```

Test PH assumption:
```python
from lifelines.statistics import proportional_hazard_test
results = proportional_hazard_test(cph, df, time_transform='rank')
results.print_summary()
# If p < 0.05 → PH violated → use AFT or stratified Cox
```

### Recipe 6: LLM-augmented signals (2026 SOTA)

```python
from anthropic import Anthropic
client = Anthropic()

def extract_ticket_signals(ticket_text):
    msg = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": f"""Extract churn-risk signals from this support ticket.
            Return JSON only:
            {{
              "frustration": 0-10,
              "competitor_mention": true/false,
              "cancellation_intent": true/false,
              "pricing_complaint": true/false,
              "feature_request_missing": true/false
            }}
            
            Ticket: {ticket_text}"""
        }]
    )
    return json.loads(msg.content[0].text)

# Apply to all recent tickets per user
df['llm_frustration'] = df['recent_ticket_text'].apply(
    lambda x: extract_ticket_signals(x)['frustration'] if x else 0
)
df['competitor_mention'] = df['recent_ticket_text'].apply(
    lambda x: int(extract_ticket_signals(x)['competitor_mention']) if x else 0
)

# Re-fit Cox PH with LLM features
cph.fit(df, duration_col='tenure_days', event_col='churned')
# LLM features typically rank top 5 in hazard contribution
```

### Recipe 7: NPS comment signal

```python
def extract_nps_signal(comment, score):
    if not comment:
        return {"churn_intent": 0}
    msg = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=100,
        messages=[{
            "role": "user",
            "content": f"""NPS score: {score}/10. Comment: "{comment}"
            Rate churn intent 0-10. JSON: {{"churn_intent": int}}"""
        }]
    )
    return json.loads(msg.content[0].text)

# Detractor (NPS 0-6) + cancellation language = high risk
```

### Recipe 8: Call-transcript red flags (Otter / Gong / Fathom)

```python
# For sales-led / CSM-led motion
def extract_call_red_flags(transcript):
    msg = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=400,
        messages=[{
            "role": "user",
            "content": f"""From this CSM call transcript, extract red flags.
            JSON:
            {{
              "champion_left_company": bool,
              "budget_cut_mentioned": bool,
              "alternative_evaluation": bool,
              "executive_buy_in_lost": bool,
              "renewal_doubt": 0-10
            }}
            Transcript: {transcript[:8000]}"""
        }]
    )
    return json.loads(msg.content[0].text)
```

Each flag = binary covariate in Cox PH.

### Recipe 9: Handoff to win-back

```python
# Tier at-risk users by risk level → different intervention
def tier_at_risk(surv_30):
    if surv_30 < 0.40: return 'critical'      # CSM call / phone outreach
    if surv_30 < 0.55: return 'high'           # Custom email + discount
    if surv_30 < 0.70: return 'moderate'       # Automated win-back sequence
    return 'low'                                # Monitor only

at_risk['intervention_tier'] = at_risk['surv_30'].apply(tier_at_risk)

# Pipe via Customer.io API to win-back sequences
for _, row in at_risk.iterrows():
    if row['intervention_tier'] == 'critical':
        hubspot.create_task(owner=row['csm_id'], note='Churn risk: schedule call this week')
        slack.send('#csm-alerts', f"At-risk: {row['user_email']}")
    elif row['intervention_tier'] in ('high', 'moderate'):
        customerio.add_to_segment(row['user_id'], 'win_back_high' if row['intervention_tier'] == 'high' else 'win_back_moderate')
```

### Recipe 10: Model validation + monitoring

```python
from lifelines.utils import concordance_index

# C-index = ranking quality (0.5 = random; 0.7+ = good; 0.8+ = excellent)
c_index = concordance_index(
    df['tenure_days'],
    -cph.predict_partial_hazard(df),  # negate because higher hazard = shorter survival
    df['churned']
)
print(f"C-index: {c_index:.3f}")

# Refit monthly; track c_index drift
# If c_index drops > 0.05 → features stale; retrain
```

### Recipe 11: Subgroup model (when one model doesn't fit all)

```python
# Often: SMB churn dynamics ≠ Enterprise. Fit per-segment.
models = {}
for tier in ['solo', 'team', 'enterprise']:
    sub = df[df['plan_tier'] == tier]
    cph = CoxPHFitter()
    cph.fit(sub, duration_col='tenure_days', event_col='churned')
    models[tier] = cph
```

## Examples

### Example 1: B2B SaaS, 18% annual logo churn

Sample: 1,400 users with 24-month history.

Cox PH top features (HR + p-value):
- `days_since_last_session` HR=1.18, p<0.001 — biggest predictor
- `team_size` HR=0.41, p<0.001 — multi-user accounts retain
- `llm_competitor_mention` HR=2.7, p=0.003 — strong negative signal
- `feature_adoption_count` HR=0.78, p<0.001 — wide adoption protects
- `nps_score` HR=0.84, p=0.012 — NPS predicts but weaker than behavior

c-index = 0.79 (excellent).

Plan: monthly scoring; pipe critical (<40% 30d-surv) to CSM; high (40-55%) to Customer.io reactivation.

### Example 2: Consumer subscription, 28% monthly churn

Decay-shape retention. STOP — don't predict; fix activation per `activation-funnel-aha-moment` skill first.

### Example 3: Mid-market SaaS, hybrid PLG + sales

Subgroup models per tier (Recipe 11).
- Solo tier: behavior + product signals
- Team tier: + invitations + team-activity signals
- Enterprise tier: + call-transcript LLM signals from CSM calls

Pipe results to per-tier interventions.

## Edge cases / gotchas

- **Don't predict on decay curves** — if retention shape is decay, churn is universal; predicting "who churns" is noise. Fix activation first.
- **Right-censoring** — users still alive at end of observation are censored, not churned. lifelines handles this correctly (`event_col` = 0); don't drop them.
- **Sparse churn events** — model fails with < 100 churn events. Use Bayesian priors or aggregate features.
- **Feature leakage** — `customer_success_engaged` may be downstream of churn risk (CSM reaches out because user is churning). Verify temporal direction.
- **Reverse-causation features** — `payment_failed` predicts churn but is often AFTER user decided to churn; not actionable.
- **PH assumption violation** — Cox assumes proportional hazards over time. Check via `proportional_hazard_test`; use AFT if violated.
- **Multicollinearity** — `team_size` + `seats_paid` redundant; VIF check.
- **Class imbalance** — 5% churn rate is normal; lifelines handles correctly via partial likelihood. Don't apply binary-classification techniques like SMOTE.
- **LLM feature drift** — Claude versions change; rerun ticket extraction quarterly + revalidate.
- **GDPR — predicting churn on PII** — keep prediction internal; never expose at-risk-list to user-facing dashboards without consent.
- **Champion-leaves blind spot** — when CSM contact leaves their company, you lose insight; track champion-tenure as feature.

## Sources

- lifelines (CamDavidsonPilon): https://github.com/CamDavidsonPilon/lifelines
- lifelines SaaS churn + piecewise regression notebook: https://github.com/CamDavidsonPilon/lifelines/blob/master/examples/SaaS%20churn%20and%20piecewise%20regression%20models.ipynb
- lifelines Cox PH docs: https://lifelines.readthedocs.io/en/latest/Survival%20Regression.html
- AI-powered SaaS churn prediction 2026: https://saaslatestnews.com/ai-powered-saas-churn-prediction/
- Pycox (deep survival): https://github.com/havakv/pycox
- scikit-survival: https://scikit-survival.readthedocs.io/
- Anthropic API: https://docs.anthropic.com/
- ProductLed PLG metrics (churn): https://www.productled.org/foundations/product-led-growth-metrics
