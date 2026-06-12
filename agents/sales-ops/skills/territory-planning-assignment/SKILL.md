<!--
Source: https://help.salesforce.com/s/articleView?id=sf.tm2_intro.htm + https://www.anaplan.com/products/sales-planning/
Territory planning + assignment — Salesforce TM2 + Anaplan + Fullcast + k-means (June 2026 SOTA).
-->
# Territory Planning + Assignment — TM2 + Anaplan + Fullcast + k-means — SKILL

Territory design tools: **Anaplan** (enterprise scenario modeling), **Varicent Territory**, **Salesforce Territory Management 2.0** (native, in-CRM enforcement), **Fullcast** (mid-market). Inputs: account ICP fit + TAM + rep capacity + geo + vertical. Output: balanced territory book per rep. Custom k-means clustering in Python when no paid tool.

## When to use

- **Annual territory redesign** — re-balance based on coverage gaps.
- **Mid-year quota carve-up** — new hire, new region.
- **Account-to-territory assignment** — bulk apply via Composite API.
- **Balance check** — same TAM + same # accounts per rep.
- **What-if scenario** — Anaplan modeling for alternate carve-ups.
- **Trigger phrases**: "territory plan", "TM2", "Anaplan territory", "k-means territory", "account assignment", "territory balance check".

Do NOT use this skill for: **quota calculation per AE** (use `commission-spiff-quotapath-captivateiq`); **lead routing** (use `lead-routing-leandata-chili-piper`); **rep performance** (use `rep-performance-dashboards`); **account hierarchy** (use `contact-account-hierarchy-maintenance`).

## Setup

```bash
# Salesforce TM2 — standard SF auth
sf org login web --alias prod
# TM2 must be enabled in org: Setup → Territory Settings → Enable

# Anaplan — OAuth or basic auth
export ANAPLAN_USER="<email>"
export ANAPLAN_PASSWORD="<password>"
export ANAPLAN_WORKSPACE_ID="<id>"
export ANAPLAN_MODEL_ID="<id>"

# Fullcast — API token
export FULLCAST_TOKEN="<token>"

# Python for k-means
pip install pandas scikit-learn numpy

# Or via api-gateway
export MATON_API_KEY="<key>"
```

Required:
- Salesforce Enterprise+ for TM2
- Anaplan: enterprise license (~$50K-200K/yr)
- Fullcast: mid-market territory planning (~$20K-60K/yr)

## Common recipes

### Recipe 1: Inputs for territory design (canonical)

```yaml
account_inputs:
  - account_id
  - account_name
  - billing_country
  - billing_state
  - billing_city
  - industry
  - employee_count
  - annual_revenue
  - tam_score                 # estimated total addressable spend
  - icp_fit_score            # 0-100 ICP match score
  - existing_relationship    # current customer / past customer / cold

rep_inputs:
  - rep_id
  - segment_capacity         # enterprise / MM / SMB
  - geo_constraint           # required geo coverage
  - vertical_specialty       # if any
  - tenure_months
  - target_quota

balance_constraints:
  - target_accounts_per_rep_range: 80-120
  - target_tam_per_rep_range: $40M-$60M
  - max_geo_dispersion        # for travel-heavy territories
  - vertical_concentration_pct  # > 50% same vertical OK
```

### Recipe 2: Pull all accounts via Bulk API

```bash
sf data query --target-org prod --bulk --wait 30 --query \
  "SELECT Id, Name, BillingCountry, BillingState, BillingCity, \
          Industry, NumberOfEmployees, AnnualRevenue, \
          TAM_Score__c, ICP_Fit_Score__c, Type \
   FROM Account \
   WHERE Type IN ('Prospect','Customer') \
     AND Active__c = TRUE" \
  --result-format csv > accounts.csv
```

### Recipe 3: K-means territory clustering (geo-based)

```python
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

accounts = pd.read_csv('accounts.csv')
# Geocode if needed (use a geocoding API; see Recipe 6)

# Features: lat + lng + TAM (log-scaled) + ICP fit
features = accounts[['lat','lng','tam_score','icp_fit_score']].copy()
features['tam_log'] = np.log1p(features['tam_score'])
features = features.drop(columns=['tam_score'])

# Standardize
scaler = StandardScaler()
X = scaler.fit_transform(features)

# K-means — K = # territories (= # AEs)
NUM_TERRITORIES = 15
km = KMeans(n_clusters=NUM_TERRITORIES, random_state=42, n_init=10)
accounts['territory_id'] = km.fit_predict(X)

# Per-territory summary
summary = accounts.groupby('territory_id').agg(
    accounts=('Id','count'),
    total_tam=('tam_score','sum'),
    mean_icp=('icp_fit_score','mean'),
    states=('BillingState', lambda s: list(s.unique())[:10])
).reset_index()
print(summary)
```

### Recipe 4: Balance check + iterative rebalancing

```python
# Per-territory metrics
print(summary.describe())

# Identify imbalance: > 30% deviation from target
target_accounts = 100
target_tam = 50_000_000

imbalanced = summary[
    (summary['accounts'] < target_accounts * 0.7) |
    (summary['accounts'] > target_accounts * 1.3) |
    (summary['total_tam'] < target_tam * 0.7) |
    (summary['total_tam'] > target_tam * 1.3)
]
print(f"Imbalanced territories: {len(imbalanced)}")

# Iterative swap: move accounts from over-allocated to under-allocated adjacent territories
def swap_accounts(accounts, n_iters=5):
    for _ in range(n_iters):
        # Compute pairwise territory distances
        territories = accounts.groupby('territory_id')[['lat','lng']].mean()
        # For each over-allocated territory, find nearest under-allocated
        # Move N borderline accounts (lowest tam) to neighbor
        # ... (impl)
    return accounts

accounts = swap_accounts(accounts)
```

### Recipe 5: Salesforce TM2 — create territory

```bash
# TM2 Territory2 object (must enable TM2 in setup)
sf data create record --target-org prod --sobject Territory2 \
  --values "DeveloperName=EMEA_DACH_Enterprise Name='EMEA DACH Enterprise' \
            Territory2ModelId=<model_id> Territory2TypeId=<type_id> \
            ParentTerritory2Id=<parent_id>"

# Assign accounts to territory (bulk)
sf data upsert bulk --target-org prod --sobject ObjectTerritory2Association \
  --external-id ObjectId --file territory_assignments.csv --wait 30
```

CSV format:
```csv
ObjectId,Territory2Id,AssociationCause
001XX0000123ABC,0M2XX0000456DEF,Territory2Manual
001XX0000123BCD,0M2XX0000456DEF,Territory2Manual
```

### Recipe 6: Geocoding accounts (Mapbox / Google)

```python
import requests, os

def geocode(address):
    r = requests.get("https://api.mapbox.com/geocoding/v5/mapbox.places/" + address + ".json",
                     params={"access_token": os.environ["MAPBOX_TOKEN"], "limit": 1}).json()
    if r.get("features"):
        coords = r["features"][0]["center"]
        return coords[1], coords[0]  # lat, lng
    return None, None

accounts = pd.read_csv('accounts.csv')
accounts['address_str'] = accounts.apply(lambda r: f"{r['BillingCity']}, {r['BillingState']}, {r['BillingCountry']}", axis=1)
accounts[['lat','lng']] = accounts['address_str'].apply(lambda a: pd.Series(geocode(a)))
accounts.to_csv('accounts_geocoded.csv', index=False)
```

### Recipe 7: Anaplan REST — push territory assignment

```bash
# Anaplan uses a session token + workspace/model context
# Step 1: Auth
TOKEN=$(curl -s -X POST "https://auth.anaplan.com/token/authenticate" \
  -u "$ANAPLAN_USER:$ANAPLAN_PASSWORD" | jq -r .tokenInfo.tokenValue)

# Step 2: Upload assignment file to Anaplan workspace
curl -X POST \
  "https://api.anaplan.com/2/0/workspaces/$ANAPLAN_WORKSPACE_ID/models/$ANAPLAN_MODEL_ID/files/<file_id>/chunks/0" \
  -H "Authorization: AnaplanAuthToken $TOKEN" \
  -H "Content-Type: application/octet-stream" \
  --data-binary @territory_assignments.csv

# Step 3: Trigger import action
curl -X POST \
  "https://api.anaplan.com/2/0/workspaces/$ANAPLAN_WORKSPACE_ID/models/$ANAPLAN_MODEL_ID/imports/<import_id>/tasks" \
  -H "Authorization: AnaplanAuthToken $TOKEN" \
  -d '{"localeName":"en_US"}'
```

### Recipe 8: Fullcast — bulk territory upload

```bash
curl -X POST "https://api.fullcast.com/v1/territories/bulk" \
  -H "Authorization: Bearer $FULLCAST_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "model_abc",
    "territories": [
      {"name": "EMEA-DACH-Ent", "owner_email": "alice@co.com",
       "filter": {"country": ["DE","AT","CH"], "industry": ["SaaS","FinTech"], "employees_min": 1000}},
      {"name": "EMEA-UK-Ent", "owner_email": "bob@co.com",
       "filter": {"country": ["GB"], "employees_min": 1000}}
    ]
  }'
```

### Recipe 9: Account-segment-vertical clustering (not just geo)

```python
# Sometimes geo isn't the right dimension — vertical or product fit is
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np

accounts = pd.read_csv('accounts.csv')

# Encode categoricals
accounts = pd.get_dummies(accounts, columns=['Industry'])

# Features: ICP fit + TAM (log) + employee_log + industry one-hots
features = accounts[['ICP_Fit_Score__c','TAM_Score__c','NumberOfEmployees']].copy()
features['tam_log']      = np.log1p(features['TAM_Score__c'])
features['emp_log']      = np.log1p(features['NumberOfEmployees'])
features = features.drop(columns=['TAM_Score__c','NumberOfEmployees'])
features = pd.concat([features, accounts.filter(regex='^Industry_')], axis=1)

km = KMeans(n_clusters=12, random_state=42, n_init=10)
accounts['vertical_territory'] = km.fit_predict(features)
```

### Recipe 10: Pre/post coverage delta

```python
# Show: before redesign, each rep had X accounts; after, Y accounts
old = pd.read_csv('current_assignments.csv')  # account_id, owner_id
new = pd.read_csv('proposed_assignments.csv')  # account_id, owner_id

merged = old.merge(new, on='account_id', suffixes=('_old','_new'))
merged['changed'] = merged['owner_id_old'] != merged['owner_id_new']

# Per-rep delta
delta = merged.groupby('owner_id_new').agg(
    new_accounts=('account_id','count'),
    moved_in=('changed', lambda s: s.sum())
).reset_index()
old_count = merged.groupby('owner_id_old').agg(old_accounts=('account_id','count')).reset_index()
delta = delta.merge(old_count.rename(columns={'owner_id_old':'owner_id_new'}), on='owner_id_new', how='outer').fillna(0)
delta['net_change'] = delta['new_accounts'] - delta['old_accounts']
print(delta.sort_values('net_change', ascending=False))
```

### Recipe 11: Conflict-check (account overlap)

```bash
# Ensure no account assigned to two territories (Salesforce TM2)
sf data query --target-org prod --query \
  "SELECT ObjectId, COUNT(Id) territory_count \
   FROM ObjectTerritory2Association \
   GROUP BY ObjectId \
   HAVING COUNT(Id) > 1"
```

### Recipe 12: Communication template (rep notification)

```python
# After redesign: email each rep their new account list
for rep_id, group in accounts.groupby('owner_id_new'):
    rep = users[users['id'] == rep_id].iloc[0]
    new_accounts = group['Name'].tolist()
    lost_accounts = old[(old['owner_id_old']==rep_id) & (~old['account_id'].isin(group['account_id']))]['Name'].tolist()

    email_body = f"""
Subject: 2026 Territory — your new book

Hi {rep['first_name']},

Effective {effective_date}, your new territory:
- {len(new_accounts)} accounts
- ${group['TAM_Score__c'].sum() / 1e6:.1f}M TAM
- Geo: {group['BillingCountry'].value_counts().head(5).to_dict()}

New to you: {len(new_accounts) - len(set(new_accounts) & set(rep['previous_accounts']))} accounts
Moved away: {len(lost_accounts)}

Full list + map: <notion link>

— SalesOps
"""
    send_email(rep['email'], email_body)
```

## Examples

### Example 1: Annual redesign — 15 AEs, ~1,500 accounts

**Goal:** Balance accounts + TAM across 15 enterprise AEs for FY2026 carve-up.

**Steps:**
1. Recipe 2 — pull all qualifying accounts to CSV.
2. Recipe 6 — geocode billing cities.
3. Recipe 3 — k-means cluster into 15 geo-balanced groups.
4. Recipe 4 — balance check; iterate swap until each territory has 80-120 accounts + $40M-$60M TAM.
5. Recipe 10 — pre/post delta to validate disruption is bounded.
6. Recipe 5 — push assignments to Salesforce TM2 via Composite API.
7. Recipe 12 — email each rep their book; Slack #sales-leadership summary.

**Result:** Balanced territories deployed; minimal account churn for sustained relationships.

### Example 2: Mid-year new-hire carve-out

**Goal:** New AE joining EMEA; carve 60 accounts from existing reps.

**Steps:**
1. Identify over-allocated EMEA AEs (Recipe 4 balance check).
2. Manually rank accounts on existing reps by "transferability": cold/dormant first.
3. Pull 60 accounts (4 per impacted AE on average).
4. Recipe 5 — reassign in Salesforce TM2.
5. Recipe 12 — notify both sending + receiving reps.
6. Track stakeholder transitions in notion (champion handoffs).

**Result:** New AE has working book Day 1; existing reps lose mostly inactive accounts.

### Example 3: What-if scenario in Anaplan

**Goal:** Evaluate 3 different carve-up strategies for FY2026 — geo, vertical, hybrid.

**Steps:**
1. Recipe 3 (geo-only) → Strategy A.
2. Recipe 9 (vertical-only) → Strategy B.
3. Combined geo + vertical features → Strategy C.
4. Recipe 7 — push each as a separate Anaplan scenario.
5. Anaplan modeling: predicted coverage, predicted attainment, predicted travel cost.
6. Leadership review: pick strategy → Recipe 5 deploy.

**Result:** Data-driven choice between geo vs vertical org structure.

## Edge cases / gotchas

- **TM2 model activation overhead** — only one active model at a time; switching models mid-quarter destroys current territory data.
- **TM2 rule-based vs manual assignment** — rule-based is auto (per filter); manual is one-by-one. Mix carefully.
- **Account swap mid-deal** — reassigning a Salesforce account mid-open-opp resets ownership cascade. Pause active deals.
- **Geo lookup cost** — Mapbox / Google ~$5/1K records. Cache results.
- **K-means non-determinism** — random seed varies; set `random_state` for reproducibility.
- **Empty territories** — k-means can produce tiny clusters; merge < 30-account territories.
- **TAM_Score__c definition drift** — TAM source: account budget? Industry × employees? Pick one canonical formula.
- **Annual revenue from D&B** — stale if not refreshed; influences TAM estimate.
- **Cross-segment overlaps** — enterprise AE vs MM AE on borderline account (700 employees). Pre-define handoff rules.
- **Geo boundary edge cases** — northern California vs Northwest US. Document territory borders explicitly.
- **OOO transitions** — when AE leaves, accounts become orphans. Trigger reassignment in `contact-account-hierarchy-maintenance`.
- **Anaplan model takes weeks to build** — first time; subsequent updates fast.
- **Fullcast vs Anaplan vs TM2** — Fullcast simpler/fast; Anaplan flexible/complex; TM2 native enforcement. Pick by complexity.
- **Vertical clustering risks** — one industry crash hits one AE hard. Mix verticals where possible.
- **Account count vs TAM weighting** — 100 small + 5 huge accounts ≠ 50 medium + 5 huge. Use both metrics.
- **Communication is the failure point** — reps freak about "lost" accounts. Over-communicate with rationale.

## Sources

- [Salesforce Territory Management 2.0 Help](https://help.salesforce.com/s/articleView?id=sf.tm2_intro.htm)
- [Salesforce TM2 — Territory2 Object](https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/sforce_api_objects_territory2.htm)
- [Anaplan Sales Planning](https://www.anaplan.com/products/sales-planning/)
- [Anaplan REST API docs](https://help.anaplan.com/anapedia/Content/APIs/Anaplan-APIs.htm)
- [Fullcast territory planning](https://www.fullcast.com/)
- [scikit-learn KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)
- [Territory design best practices (Alexander Group)](https://www.alexandergroup.com/insights/sales-territory-design/)
- [TAM-driven sales planning (Bain)](https://www.bain.com/insights/sales-planning/)
