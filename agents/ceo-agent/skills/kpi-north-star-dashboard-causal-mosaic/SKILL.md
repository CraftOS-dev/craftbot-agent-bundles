<!--
Source: https://valueaddvc.com/blog/best-financial-modeling-tools-for-startups-excel-vs-runway-vs-causal-vs-mosaic
KPI dashboard: Causal / Mosaic / Visible / Finmark + warehouse pull + cadence
-->
# KPI / North Star Dashboard — Causal / Mosaic / Visible / Finmark

One north star metric + 4-5 supporting KPIs. Stage-tiered tooling: Causal (spreadsheet-inspired FP&A, scenario modeling, Seed-Series B), Mosaic (AI-powered FP&A, Series C+), Visible.vc (investor-facing KPI sync), Finmark (startup-budgeting). Daily-cash + weekly-revenue rhythm is the SOTA CEO cadence (~62% fewer cash crises per cited research). Source-of-record principle: every metric has ONE owning system.

## When to use

- Designing a KPI dashboard from scratch.
- Identifying the right north star metric for the stage.
- Choosing FP&A tooling (Causal vs Mosaic vs Finmark).
- Setting up daily-cash / weekly-revenue / monthly-variance review cadence.
- Refresh of a stale dashboard.

Trigger phrases: "CEO dashboard", "north star metric", "KPIs", "Causal vs Mosaic", "daily cash review", "weekly metrics", "KPI hierarchy".

## Setup

```bash
# Causal API
curl -fsSL "https://api.causal.app/v1/me" \
  -H "Authorization: Bearer $CAUSAL_API_KEY"

# Mosaic API
curl -fsSL "https://api.mosaic.tech/v1/me" \
  -H "Authorization: Bearer $MOSAIC_API_KEY"

# Visible (cross-ref to investor-update skill)
curl -fsSL "https://api.visible.vc/v1/me" \
  -H "Authorization: Bearer $VISIBLE_API_KEY"

# PostgreSQL warehouse pull
psql $DATABASE_URL -c "SELECT version()"
```

Auth / API key requirements:
- `CAUSAL_API_KEY` — Causal Settings → API ($39/mo+).
- `MOSAIC_API_KEY` — Mosaic admin.
- `VISIBLE_API_KEY` — Visible (cross-ref to investor-update skill).
- `STRIPE_API_KEY` / `XERO_API_KEY` / `POSTHOG_API_KEY` — for source-of-record pulls.
- `DATABASE_URL` — warehouse for SQL queries.

## Common recipes

### Recipe 1: North star metric chooser

```markdown
## Pick ONE north star

| Business model | North star candidates |
|---|---|
| SaaS B2B | MRR or ARR-Net-of-Churn or NRR |
| Consumer subscription | Weekly Active Subscribers, MRR |
| Marketplace | GMV or Active Both-sided Users |
| PLG product | Activated Users (D7 or D30) |
| Free → paid funnel | Conversion-to-Paid Cohort |
| Hardware / IoT | Devices Activated or DAU/Devices |
| Open source / dev tool | Weekly Active Builds or Stars/repo activity |

Rule: north star ties to the customer value delivered AND business value (revenue). Pick ONE. Educate the team.
```

### Recipe 2: KPI hierarchy (5 max)

```markdown
## KPI hierarchy — example (B2B SaaS)

```
NORTH STAR: Time-to-Ship (median minutes from signup → first ship)
  ├── MRR
  │     ├── New MRR
  │     ├── Expansion MRR
  │     └── Churn MRR
  ├── Active customers (Paying)
  ├── D7 retention
  ├── Gross margin
  └── Cash + runway
```

5 KPIs max. More than that and you're tracking a dashboard, not running a company.
```

### Recipe 3: Daily / weekly / monthly review cadence

```markdown
## CEO review cadence

| Frequency | Metrics | Where | Time |
|---|---|---|---|
| Daily | Cash position, key sales / customer events | Slack #cfo-alerts | 5 min |
| Weekly | Revenue + product + pipeline + hiring | Monday metrics meeting | 60 min |
| Monthly | Full P&L variance, retention cohorts | Last Thu variance review | 90 min |
| Quarterly | Strategy KPIs, north star trend | QBR | (in QBR) |

Daily-cash + weekly-revenue rhythm: shown to correlate with ~62% fewer cash crises.
```

### Recipe 4: Source-of-record table

```markdown
## Every metric has ONE owning system

| Metric | Source of record | Why |
|---|---|---|
| MRR / churn | stripe-mcp | Stripe is the cash source |
| Cash balance | xero-mcp | Accounting is the bank source |
| Runway | (cash / monthly burn) | Derived; lock the formula |
| D7 retention | posthog-mcp | Product analytics owns user data |
| Pipeline | CRM (SFDC / HubSpot) | Sales CRM owns deal stages |
| Hiring | Ashby / Greenhouse | ATS owns reqs + offers |
| North Star (Time-to-Ship) | postgresql-mcp (warehouse) | Derived from product events |

Rule: if a metric is in two places, they MUST reconcile. Otherwise you don't have a metric, you have a debate.
```

### Recipe 5: Causal — scenario model

```bash
# Causal supports spreadsheet-like formulas + Monte Carlo scenarios
curl -X POST "https://api.causal.app/v1/models" \
  -H "Authorization: Bearer $CAUSAL_API_KEY" \
  -d '{
    "name":"FY27 forward",
    "variables":{
      "new_mrr_per_month":{"formula":"15000 * (1 + uniform(0.02, 0.08))","distribution":"uniform"},
      "churn_rate":{"formula":"normal(0.03, 0.01)","distribution":"normal"},
      "monthly_burn":{"formula":"150000"}
    },
    "outputs":[
      {"name":"ARR_eoq4","formula":"sum(new_mrr_per_month)*12 - churn"},
      {"name":"runway_months","formula":"cash / monthly_burn"}
    ]
  }'
```

### Recipe 6: Mosaic dashboard (Series C+)

```bash
# Mosaic auto-pulls from ERP / CRM / billing
curl -X POST "https://api.mosaic.tech/v1/metrics" \
  -H "Authorization: Bearer $MOSAIC_API_KEY" \
  -d '{
    "name":"NRR",
    "formula":"(beginning_arr + expansion - churn - downgrade) / beginning_arr",
    "owner_team":"finance",
    "refresh":"daily",
    "source":"stripe"
  }'
```

### Recipe 7: Warehouse pull (postgresql for derived metrics)

```bash
# Pull north star from warehouse
psql $DATABASE_URL <<'SQL'
SELECT 
  date_trunc('week', signup_at) as week,
  count(*) as signups,
  count(*) FILTER (WHERE first_ship_at IS NOT NULL) as activated,
  percentile_cont(0.5) WITHIN GROUP (ORDER BY extract(epoch from first_ship_at - signup_at)/60) as median_ttv_min
FROM users
WHERE signup_at >= now() - interval '13 weeks'
GROUP BY 1 ORDER BY 1;
SQL
```

### Recipe 8: Daily cash alert

```bash
# Run every morning 7am
CASH=$(curl -s "https://api.xero.com/api.xro/2.0/Accounts/<bank>" \
  -H "Authorization: Bearer $XERO_API_KEY" | jq '.Accounts[0].Balance')
BURN=150000
RUNWAY=$(echo "$CASH / $BURN" | bc -l | xargs printf "%.0f")

if [ "$RUNWAY" -lt 12 ]; then
  mcp tool slack.send --channel "#leadership" --message "🚨 Runway $RUNWAY months — surface at QBR"
fi

mcp tool slack.send --channel "#cfo-alerts" --message "Cash: \$$CASH | Burn: \$$BURN | Runway: $RUNWAY months"
```

### Recipe 9: Weekly metrics review template

```markdown
## Weekly Metrics Review — Monday 9am

### Last week's wins / lowlights
- [3 bullets]

### KPI walk (15 min)
| KPI | Last week | This week | % change | Target |
|---|---|---|---|---|
| MRR | $52k | $54k | +3.8% | $60k |
| Customers | 168 | 173 | +3% | 175 |
| D7 ret | 22% | 23% | +1pp | 25% |
| Pipeline coverage | 2.4x | 2.6x | +0.2x | 3x |
| Cash | $1.92M | $1.85M | -3.6% | $1.8M plan |

### Exceptions (15 min)
- D7 below target — Sara presenting recovery plan
- Pipeline coverage low — VP Sales SDR offer out

### Decisions (15 min)
- Pricing v2 launch — go/no-go decision

### Asks + unblock (10 min)
- Each leader: 1 ask
```

### Recipe 10: Dashboard storage (Notion + URL to FP&A tool)

```bash
mcp tool notion.create_page \
  --parent '{"page_id":"<exec-hub>"}' \
  --properties '{"title":[{"text":{"content":"CEO Dashboard"}}]}' \
  --children-markdown "## North Star: Time-to-Ship
Live: [Causal link]

## Supporting KPIs
| KPI | Source | Link |
|---|---|---|
| MRR | Stripe | [Causal] |
| D7 Retention | PostHog | [Amplitude] |
| Cash | Xero | [Causal] |
| Pipeline | HubSpot | [HubSpot dashboard] |
| Hiring | Ashby | [Ashby] |

## Cadence
- Daily 7am: cash alert (#cfo-alerts)
- Weekly Monday 9am: full metrics review
- Monthly variance: last Thursday
- Quarterly: QBR

Last refresh: $(date)"
```

### Recipe 11: Tooling by stage

```markdown
| Stage | Tool stack |
|---|---|
| Pre-seed / Seed | Google Sheets + Causal + Stripe + Xero |
| Seed / Series A | Causal + Visible (investor view) + Finmark + Stripe |
| Series A / B | Causal or Runway + Visible + postgresql warehouse |
| Series B / C+ | Mosaic + Visible + warehouse + Looker / Tableau |
```

### Recipe 12: Monthly variance review (last Thursday)

```bash
# Pull actuals vs plan from Causal/Mosaic
ACTUAL=$(curl -fsSL "https://api.causal.app/v1/models/$MODEL_ID/actuals?period=2027-04" \
  -H "Authorization: Bearer $CAUSAL_API_KEY")
PLAN=$(curl -fsSL "https://api.causal.app/v1/models/$MODEL_ID/forecast?period=2027-04" \
  -H "Authorization: Bearer $CAUSAL_API_KEY")

# Generate variance table for review meeting
python3 -c "
import json
a = json.loads('$ACTUAL')
p = json.loads('$PLAN')
for k in a:
    var = (a[k] - p[k]) / p[k] * 100
    sign = '✅' if abs(var) < 5 else ('🟡' if abs(var) < 15 else '🔴')
    print(f'{sign} {k}: actual {a[k]:.0f} vs plan {p[k]:.0f} ({var:+.1f}%)')
"
```

## Examples

### Example 1: New CEO sets up dashboard

**Goal:** First dashboard end-to-end.

**Steps:**
1. Pick north star (Recipe 1).
2. Define KPI hierarchy (Recipe 2).
3. Source-of-record table (Recipe 4).
4. Pick FP&A tool (Recipe 11) — Causal for Seed-Series B.
5. Build dashboard (Recipe 5) + wire data sources.
6. Set cadence (Recipe 3).
7. Daily alerts (Recipe 8).
8. Weekly review template (Recipe 9).
9. Document in Notion (Recipe 10).

**Result:** Dashboard with explicit sources; cadence locked.

### Example 2: Migrate from Causal to Mosaic at Series C

**Goal:** Outgrown Causal; need Mosaic enterprise FP&A.

**Steps:**
1. Audit Causal models (3-5 in use).
2. Provision Mosaic + connect sources.
3. Rebuild north star + scenario models in Mosaic.
4. 2-week parallel run; reconcile numbers daily.
5. Sunset Causal.
6. Update Notion dashboard links (Recipe 10).

**Result:** No metric regression during migration; FP&A team scaled.

## Edge cases / gotchas

- **Two north stars = no north star.** Pick ONE. Educate the team.
- **Don't add KPIs because someone asked.** 5 max. Resist.
- **Source-of-record violations.** Two systems showing different MRR = trust killer. Reconcile immediately.
- **Daily cash review > daily revenue review.** Cash is binary; revenue is trailing.
- **Causal vs Mosaic stage rule.** Causal for Seed-Series B (spreadsheet-inspired). Mosaic for Series C+ (enterprise FP&A).
- **Finmark for startup budget.** Cheaper than Causal/Mosaic for budget-only use.
- **Warehouse-derived metrics need maintenance.** SQL changes break things. Version the queries.
- **Stripe MRR vs GAAP revenue.** Stripe MRR is a billing metric; GAAP revenue recognized over time. Educate investors on the difference.
- **NRR vs Net Revenue.** NRR includes expansion; Net Revenue is total minus discounts. Define which you mean.
- **Refresh frequency mismatch.** Daily metrics from a system that updates weekly = stale data. Match cadence to source freshness.
- **Dashboard nobody opens = no dashboard.** Make the URL the start of every meeting. Or it dies.
- **62% fewer cash crises stat.** Cited in industry literature; correlation not causation. The discipline of daily review is the value, not the stat.
- **Don't tie KR scores to bonuses directly.** Distorts the metric. Bonuses on company-wide outcomes; KRs as input to coaching.

## Sources

- [Causal vs Mosaic vs Runway FP&A](https://valueaddvc.com/blog/best-financial-modeling-tools-for-startups-excel-vs-runway-vs-causal-vs-mosaic)
- [Executive dashboard 2026 — Mandrill](https://www.mandrill.com.my/blog/executive-dashboard-software-ceos-cfos-2026/)
- [David Sacks CEO dashboard](https://www.capitaly.vc/blog/david-sacks-operating-cadence-weekly-metrics-okrs-ceo-dashboard)
- [Causal API docs](https://help.causal.app/api)
- [Mosaic API docs](https://help.mosaic.tech/)
- [Sean Ellis — North Star Framework](https://amplitude.com/blog/product-north-star-metric)
