<!--
Source: https://docs.salesforcespiff.com/ + https://docs.quotapath.com/ + https://help.captivateiq.com/
Commission plan administration — Spiff + QuotaPath + CaptivateIQ (June 2026 SOTA).
-->
# Commission Plan Administration — Spiff + QuotaPath + CaptivateIQ — SKILL

ICM (Incentive Compensation Management) plan modeling: base rates, accelerators, SPIFs, clawbacks, draws. Spiff (Salesforce-acquired, enterprise tier), QuotaPath (mid-market), CaptivateIQ (enterprise alt). Source-of-truth chain: CRM deal record → plan eligibility → rate logic → SPIFs → clawbacks → net payable.

## When to use

- **Model a new commission plan** — define base + accelerators + SPIFs + clawbacks.
- **Publish a plan to the team** — push from modeled YAML/JSON to live system.
- **Pre/post comp delta** — show reps the dollar impact of a plan change.
- **Generate test statements** — preview earnings for top-5 reps + edge cases.
- **CRM-to-ICM sync** — verify deal data flows correctly into plan calculation.
- **Manual fallback** — when paid ICM isn't onboarded, build the calc in Sheets.
- **Trigger phrases**: "model a commission plan", "comp delta", "test statement", "Spiff plan", "QuotaPath setup", "accelerator tier".

Do NOT use this skill for: **dispute resolution** (use `commission-dispute-audit-trail`); **payroll handoff** (handed to `finance-controller`); **quota planning** (use `territory-planning-assignment`).

## Setup

```bash
# Spiff — Personal API token (Settings → API Tokens)
export SPIFF_TOKEN="<token>"

# QuotaPath — OAuth token
export QUOTAPATH_TOKEN="<token>"

# CaptivateIQ — API key (Admin → Integrations → API)
export CAPTIVATEIQ_TOKEN="<token>"

# CRM source-of-truth (deal data)
export MATON_API_KEY="<key>"

# Test connectivity
curl "https://api.spiff.com/v1/plans" -H "Authorization: Bearer $SPIFF_TOKEN" | jq '.[:1]'
```

Required:
- Admin role on the ICM tool
- Spiff: paid Salesforce add-on
- QuotaPath: SMB/Mid-market, simpler plan logic
- CaptivateIQ: enterprise, complex multi-currency / multi-entity

## Common recipes

### Recipe 1: Plan YAML template (canonical)

```yaml
plan_name: "AE_New_Business_2026Q3"
effective_date: 2026-07-01
end_date: 2026-09-30
target_audience:
  role: AE
  segment: enterprise
quota:
  amount: 250000              # USD per quarter
  measure: ACV_closed_won_in_period
base_commission:
  rate: 0.08                  # 8% of ACV
  applies_to: new_logo
accelerators:
  - threshold: 1.00           # 100% of quota
    multiplier: 1.5
  - threshold: 1.10
    multiplier: 2.0
  - threshold: 1.30
    multiplier: 2.5
spifs:
  - name: "New Logo > $100K"
    condition: "amount > 100000 AND deal_type == 'new_logo'"
    bonus: 5000
  - name: "Multi-year (3yr+)"
    condition: "term_months >= 36"
    bonus: 2000
clawbacks:
  - name: "Churn within 6mo"
    condition: "churned_within_days <= 180"
    percentage: 1.00          # 100% clawback
  - name: "Payment default 90d+"
    condition: "payment_overdue_days >= 90"
    percentage: 0.50
draws:
  monthly_minimum: 5000
  recoverable: true
```

### Recipe 2: Spiff — create plan via API

```bash
curl -X POST "https://api.spiff.com/v1/plans" \
  -H "Authorization: Bearer $SPIFF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AE_New_Business_2026Q3",
    "effective_date": "2026-07-01",
    "end_date": "2026-09-30",
    "target_role_id": 12,
    "rules": [
      {
        "name": "Base",
        "rate": 0.08,
        "measure_field": "ACV",
        "filter": "deal_type = '\''new_logo'\''"
      },
      {
        "name": "Accelerator 100%",
        "type": "tier",
        "threshold_pct": 100,
        "multiplier": 1.5
      },
      {
        "name": "SPIF: New Logo > $100K",
        "type": "bonus",
        "amount": 5000,
        "condition": "deal_amount > 100000 AND deal_type = '\''new_logo'\''"
      }
    ]
  }'
```

### Recipe 3: QuotaPath — create plan

```bash
curl -X POST "https://api.quotapath.com/v1/plans" \
  -H "Authorization: Bearer $QUOTAPATH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AE_New_Business_2026Q3",
    "quota_period": "QUARTERLY",
    "quota_amount": 250000,
    "currency": "USD",
    "start_date": "2026-07-01",
    "end_date": "2026-09-30",
    "structure": {
      "type": "TIERED",
      "tiers": [
        {"to": 100, "rate": 0.08},
        {"from": 100, "to": 110, "rate": 0.12},
        {"from": 110, "to": 130, "rate": 0.16},
        {"from": 130, "rate": 0.20}
      ]
    }
  }'
```

### Recipe 4: CaptivateIQ — assign plan to rep

```bash
curl -X POST "https://api.captivateiq.com/v1/assignments" \
  -H "Authorization: Bearer $CAPTIVATEIQ_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_email": "alice@co.com",
    "plan_id": "plan_abc123",
    "period_start": "2026-07-01",
    "period_end": "2026-09-30",
    "quota_override": 250000
  }'
```

### Recipe 5: Pre/post comp delta (Python — manual)

```python
import pandas as pd

# Pull last 6 months of closed-won deals from CRM
deals = pd.read_csv("closed_won_2026H1.csv")
# Columns: deal_id, owner_id, owner_name, amount, deal_type, term_months, close_date, churned

def calc_baseline(d):
    # OLD plan: flat 8%, no SPIF, accelerator at 1.5x past 110%
    base = d['amount'] * 0.08
    return base

def calc_proposed(d):
    # NEW plan: 8% base, SPIF at >$100K, accelerator tiers
    base = d['amount'] * 0.08
    spif = 5000 if d['amount'] > 100000 and d['deal_type'] == 'new_logo' else 0
    return base + spif

deals['baseline'] = deals.apply(calc_baseline, axis=1)
deals['proposed'] = deals.apply(calc_proposed, axis=1)

delta = deals.groupby('owner_name').agg(
    baseline_total=('baseline','sum'),
    proposed_total=('proposed','sum'),
    delta=('proposed', lambda s: s.sum() - deals.loc[s.index, 'baseline'].sum())
).reset_index()
delta['delta_pct'] = 100 * delta['delta'] / delta['baseline_total']
delta = delta.sort_values('delta_pct', ascending=False)
print(delta.to_string(index=False))

# Flag anyone with > 10% swing for leadership review
flagged = delta[abs(delta['delta_pct']) > 10]
print("\nFlagged for review:")
print(flagged.to_string(index=False))
```

### Recipe 6: Generate test statement (Spiff)

```bash
# Trigger statement generation for a specific rep + period
curl -X POST "https://api.spiff.com/v1/statements/preview" \
  -H "Authorization: Bearer $SPIFF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 5012345,
    "plan_id": 78,
    "period_start": "2026-07-01",
    "period_end": "2026-09-30",
    "include_deals": true
  }'
```

### Recipe 7: CaptivateIQ — pull current statement

```bash
curl "https://api.captivateiq.com/v1/statements?user_email=alice@co.com&period=2026-Q3" \
  -H "Authorization: Bearer $CAPTIVATEIQ_TOKEN" \
  | jq '.statements[] | {user, period, gross_commission, net_payable, line_items}'
```

### Recipe 8: CRM-to-ICM sync verification

```python
# Compare deal counts between Salesforce + Spiff
import requests, os

# Salesforce: closed-won in Q3
sf_query = "SELECT COUNT(Id) c, SUM(Amount) total FROM Opportunity WHERE IsClosed = TRUE AND IsWon = TRUE AND CloseDate >= 2026-07-01 AND CloseDate <= 2026-09-30"
sf = requests.get(f"https://gateway.maton.ai/salesforce/services/data/v60.0/query",
                  params={"q": sf_query},
                  headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"}).json()
sf_count = sf['records'][0]['c']
sf_total = sf['records'][0]['total']

# Spiff: same period
spiff = requests.get(f"https://api.spiff.com/v1/deals",
                     params={"period_start": "2026-07-01", "period_end": "2026-09-30"},
                     headers={"Authorization": f"Bearer {os.environ['SPIFF_TOKEN']}"}).json()
spiff_count = len(spiff)
spiff_total = sum(d.get('amount', 0) for d in spiff)

print(f"Salesforce: {sf_count} deals, ${sf_total:,.0f}")
print(f"Spiff:      {spiff_count} deals, ${spiff_total:,.0f}")
if abs(sf_count - spiff_count) > 2 or abs(sf_total - spiff_total) > 1000:
    print("⚠ SYNC GAP — investigate missing deals before paying")
```

### Recipe 9: Manual fallback — Google Sheets commission model

```python
# When no ICM tool: pandas + gspread to write per-AE comp to a Sheet
import pandas as pd, gspread

deals = pd.read_csv("closed_won_2026Q3.csv")
deals['base_comm'] = deals['amount'] * 0.08
deals['spif'] = deals.apply(lambda d: 5000 if d['amount'] > 100000 else 0, axis=1)

# Per-AE attainment
attainment = deals.groupby('owner_name').agg(
    deals_count=('deal_id','count'),
    acv_total=('amount','sum'),
    base_comm_total=('base_comm','sum'),
    spif_total=('spif','sum')
).reset_index()
attainment['attainment_pct'] = 100 * attainment['acv_total'] / 250000  # quota
attainment['accelerator_mult'] = attainment['attainment_pct'].apply(
    lambda a: 2.5 if a > 130 else (2.0 if a > 110 else (1.5 if a > 100 else 1.0))
)
attainment['accelerated_comm'] = attainment['base_comm_total'] * attainment['accelerator_mult']
attainment['total_comm'] = attainment['accelerated_comm'] + attainment['spif_total']

# Write to sheet
gc = gspread.service_account()
sh = gc.open("Commission Model 2026Q3").worksheet("Per AE")
sh.update([attainment.columns.values.tolist()] + attainment.values.tolist())
```

### Recipe 10: Clawback evaluation (post-payment churn)

```python
# Quarterly job: re-evaluate paid commissions for clawback triggers
import pandas as pd
from datetime import datetime, timedelta

paid = pd.read_csv("commissions_paid_2026Q2.csv")  # paid Q2, evaluating in Q3
deals = pd.read_csv("deal_status_current.csv")     # latest churned flag

merged = paid.merge(deals[['deal_id','close_date','churn_date','churned']], on='deal_id')
merged['days_to_churn'] = (pd.to_datetime(merged['churn_date']) - pd.to_datetime(merged['close_date'])).dt.days

clawbacks = merged[(merged['churned']==True) & (merged['days_to_churn'] <= 180)]
clawbacks['clawback_amount'] = clawbacks['commission_paid']  # 100% clawback

print(f"Clawback events: {len(clawbacks)}")
print(f"Total clawback: ${clawbacks['clawback_amount'].sum():,.0f}")
print(clawbacks[['deal_id','owner_name','commission_paid','clawback_amount']].to_string(index=False))
```

### Recipe 11: Spiff dispute API

```bash
# AE files a dispute
curl -X POST "https://api.spiff.com/v1/disputes" \
  -H "Authorization: Bearer $SPIFF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "statement_id": "stmt_xyz789",
    "user_id": 5012345,
    "claim": "Expected $13,200 — actual $10,200. SPIF for new logo > $100K not applied.",
    "expected_amount": 13200,
    "actual_amount": 10200,
    "deal_ids": ["006XX0000123ABC"]
  }'
```

### Recipe 12: Plan publish + AE notification

```bash
# Publish (activate) plan in Spiff
curl -X PATCH "https://api.spiff.com/v1/plans/<plan_id>" \
  -H "Authorization: Bearer $SPIFF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "active", "publish_to_users": true}'

# Email notification template (via gmail-mcp or slack-mcp)
# "Your 2026 Q3 plan is now live. Quota: $250K. Base: 8% on new logo. SPIF: $5K on > $100K deals.
#  Statement preview: <link>. Plan doc: <notion>."
```

## Examples

### Example 1: Q3 plan rollout (5-rep team)

**Goal:** Replace flat 8% plan with tiered + SPIF for Q3.

**Steps:**
1. Draft plan YAML (Recipe 1) — 8% base + 1.5×/2.0×/2.5× accelerators + $5K new-logo SPIF.
2. Pull last 6 months closed-won via Recipe 5 — compute baseline + proposed comp per AE.
3. Flag anyone with > 10% delta; review with leadership.
4. Run Recipe 6 to generate test statements for top-3 reps + 2 ramp reps.
5. Publish via Recipe 12; notify AEs via Slack + email with statement preview link.

**Result:** Reps see the math before Q3 starts; no surprises in first statement.

### Example 2: Mid-quarter sync gap detection

**Goal:** Monthly verify that all closed-won deals in Salesforce flow into Spiff.

**Steps:**
1. Recipe 8 — count + sum deals in both Salesforce + Spiff for current quarter-to-date.
2. If gap > 2 deals or $1K: pull deal IDs from Salesforce not in Spiff.
3. Investigate: missing user mapping? Excluded deal type? Sync lag?
4. Patch + re-trigger Spiff sync via `POST /v1/deals/sync`.

**Result:** AEs aren't surprised by missing deals at quarter end.

### Example 3: Clawback enforcement on churn

**Goal:** Account churned at month 4 of contract; rep was paid full commission.

**Steps:**
1. Recipe 10 — identify deal in clawback window (≤ 180 days).
2. Compute clawback per plan (100% on churn ≤ 180d).
3. File adjustment via Spiff `POST /v1/adjustments` (or CaptivateIQ equivalent).
4. Email rep with audit chain: deal ID, original commission, clawback %, net adjustment.
5. Log to `notion` clawback ledger.

**Result:** Plan integrity preserved; rep sees the calculation transparently.

## Edge cases / gotchas

- **Plan effective_date is fixed — retroactive changes break audit trail** — always create v2 with new effective_date; never modify v1 after publish.
- **Spiff is Salesforce-only** — for HubSpot shops, use QuotaPath or CaptivateIQ.
- **Currency conversion** — multi-currency teams: pin to deal close date FX. Spiff supports; QuotaPath has limited handling.
- **Quota mid-period changes destroy attainment %** — if quota changes Q2 to Q3, snapshot Q2 quota separately.
- **SPIF conditions are string formulas** — string vs numeric type mismatches silently fail. Test before publish.
- **Accelerator multiplier applies to base only, not SPIF** — common confusion. Confirm in plan doc.
- **Draws are recoverable across periods** — outstanding draw at period end carries forward; reps confused. Document.
- **CRM sync lag** — Salesforce → Spiff: 5-15 min. Last-day-of-quarter deals: race condition. Manual sync trigger before statement gen.
- **Splits + multi-rep deals** — Spiff supports; QuotaPath weak. Defined as % of deal credit per rep. Statement shows each rep's slice.
- **Negative commission** (clawback > earned) — clawback caps at earned; deficit is "owed" but uncollected (legal nuance).
- **Ramp tier overrides** — new hires usually have ramped quota (50% month 1, 75% month 2). Define separately, not as exception.
- **Statement period vs payment period** — Q3 statement might pay in Q4 (lag for accounting). Document both dates.
- **CaptivateIQ uses flexible field model** — extensible but complex. Field naming conventions matter; document the schema.
- **API tokens expire** — Spiff every 90d, QuotaPath every 365d. Rotate calendar reminder in notion runbook.
- **Plan publish is irreversible without manual revert** — pre-publish: backup current plan JSON to git.

## Sources

- [Salesforce Spiff documentation](https://docs.salesforcespiff.com/)
- [Spiff API reference](https://docs.salesforcespiff.com/api/)
- [QuotaPath documentation](https://docs.quotapath.com/)
- [QuotaPath API reference](https://docs.quotapath.com/reference/)
- [CaptivateIQ Help Center](https://help.captivateiq.com/)
- [CaptivateIQ API guide](https://help.captivateiq.com/article/integration-api)
- [Clari + Xactly + Performio overview (G2)](https://www.g2.com/categories/sales-compensation)
- [SaaStr ICM best practices 2026](https://www.saastr.com/sales-commissions/)
