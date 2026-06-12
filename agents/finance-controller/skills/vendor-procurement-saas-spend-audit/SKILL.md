<!--
Source: https://www.tropicapp.io/reports/software-spending-trends-2025
Source: https://www.spendflo.com/pricing-benchmarks
Source: https://www.spendhound.com/blog/vendr-alternatives
Source: https://www.tropicapp.io/blog/saas-budgeting
-->

# Vendor procurement + SaaS spend audit

Identify duplicate / unused / overpriced vendors; benchmark contract pricing; consolidate stack; negotiate renewals. Tropic 2025 benchmark: top-10 vendors = 74% of SaaS spend.

## When to use

- Quarterly SaaS spend audit.
- Pre-renewal negotiation for any contract >$10K/yr.
- Cost cutting under runway pressure.
- New vendor evaluation (TCO + benchmark check).
- Single SOX of vendor records (master vendor list).
- Trigger phrases: "SaaS audit", "spend audit", "renewal", "vendor pricing", "consolidate", "Tropic", "Vendr".

NOT for: AP scheduling (use `ar-ap-aging-collections`); contract redlining (defer to `legal-counsel`).

## Setup

```bash
# Spend data sources — already in catalog/bundled:
# - xero-mcp (GL by vendor)
# - cli-anything + Ramp/Brex APIs (corp-card data) — see ramp-brex-expense-management
# - cli-anything + bank-feed via Plaid/Mercury — see mercury-modern-treasury-banking

# Benchmark sources:
# - Vendr Index: https://www.vendr.com/marketplace
# - Tropic benchmarks: https://www.tropicapp.io/pricing-benchmarks
# - Spendflo: https://www.spendflo.com/pricing-benchmarks
# - Spendhound: https://www.spendhound.com/
# - Cledara / Sastrify (EU): https://cledara.com/ · https://sastrify.com/

# Optional managed procurement APIs:
# Vendr API access on request — partners@vendr.com
# Tropic / Spendflo: dashboard + Slack integrations, limited public API
```

## The 2026 SaaS spend landscape

Per Tropic 2025 SaaS spending trends report:
- Top 10 vendors typically = **74% of total SaaS spend**
- Average company has 130+ SaaS subscriptions
- **35% of SaaS spend is wasted** (unused or duplicate)
- **22% of contracts renew without negotiation** at list price
- Negotiated savings on standard SaaS deals: 15-30% off list with leverage

## Common recipes

### Recipe 1 — Pull all SaaS spend from GL + cards

```python
import pandas as pd

# Pull from Xero (recurring subscription accounts)
xero_subs = xero.bank_transactions.list(
  where='Type=="SPEND" AND AccountCode IN ("6300","5000","5050") ' \
        'AND Date>=DateTime(2025,07,01) AND Date<=DateTime(2026,06,30)'
)

# Pull from Ramp / Brex (corp-card SaaS spend)
ramp_subs = requests.get(
  "https://api.ramp.com/developer/v1/transactions",
  headers={"Authorization": f"Bearer {RAMP_TOKEN}"},
  params={"category":"SOFTWARE_SUBSCRIPTIONS","from_date":"2025-07-01","to_date":"2026-06-30"}
).json()

# Aggregate by vendor name (normalize)
combined = pd.DataFrame(xero_subs + ramp_subs)
combined["vendor_normalized"] = combined.merchant.str.lower().str.replace(r"[^a-z0-9 ]","")
spend_by_vendor = combined.groupby("vendor_normalized").agg(
  annual_spend=("amount","sum"),
  transactions=("amount","count")
).sort_values("annual_spend", ascending=False)
```

### Recipe 2 — Identify duplicates

```python
# Common duplicate patterns
DUPLICATE_PATTERNS = [
  ["slack","msteams","discord"],          # team chat
  ["zoom","gmeet","webex","ms-teams-mtg"],# video conf
  ["dropbox","box","gdrive"],             # file storage
  ["mailchimp","sendgrid","postmark","mandrill"], # email
  ["jira","linear","asana","clickup","monday"],   # project mgmt
  ["zendesk","intercom","helpscout","freshdesk"], # support
  ["calendly","savvycal","cal.com"],     # scheduling
  ["figma","sketch","invision"],         # design
  ["github","gitlab","bitbucket"],       # source control
]

duplicates = []
for group in DUPLICATE_PATTERNS:
    matched = spend_by_vendor[spend_by_vendor.index.str.contains("|".join(group))]
    if len(matched) > 1:
        duplicates.append({
          "category": group[0],
          "vendors": list(matched.index),
          "total_spend": matched.annual_spend.sum()
        })
print(duplicates)
```

### Recipe 3 — Identify low-utilization tools

```python
# Cross-check vendor list with SSO logs (if available via Okta / Google Workspace)
# Or with last_login fields from API where available

def utilization_check(vendor, last_30_day_logins):
    seats_paid = vendor.contracted_seats
    active_seats = last_30_day_logins.unique_users
    utilization = active_seats / seats_paid if seats_paid else 0

    if utilization < 0.30:
        return f"LOW UTILIZATION: {utilization:.0%} — consider downgrade or eliminate"
    elif utilization < 0.60:
        return f"PARTIAL UTILIZATION: {utilization:.0%} — right-size seats"
    return "OK"
```

### Recipe 4 — Benchmark against Vendr / Tropic / Spendflo

```python
# Manual benchmark check — most platforms don't have public APIs
BENCHMARKS_2026 = {
  "Slack":     {"list_per_seat": 12.50, "median_negotiated": 8.50, "leverage_threshold_seats": 50},
  "Zoom":      {"list_per_seat": 19.99, "median_negotiated": 14.00, "leverage_threshold_seats": 100},
  "Salesforce":{"list_per_seat": 165,   "median_negotiated": 105,   "leverage_threshold_seats": 25},
  "HubSpot":   {"list_per_seat": 50,    "median_negotiated": 35,    "leverage_threshold_seats": 20},
  "Notion":    {"list_per_seat": 10,    "median_negotiated": 7,     "leverage_threshold_seats": 50},
  "GitHub":    {"list_per_seat": 21,    "median_negotiated": 16,    "leverage_threshold_seats": 50},
  "Figma":     {"list_per_seat": 15,    "median_negotiated": 12,    "leverage_threshold_seats": 30},
  # ...
}

def benchmark(vendor_name, actual_per_seat, seats):
    b = BENCHMARKS_2026.get(vendor_name, {})
    if not b: return "No benchmark data"
    overpay_pct = (actual_per_seat - b["median_negotiated"]) / b["median_negotiated"]
    if overpay_pct > 0.20 and seats >= b["leverage_threshold_seats"]:
        return f"OVERPAYING by {overpay_pct:.0%} (negotiating leverage at {seats} seats); target ${b['median_negotiated']:.0f}"
    return "WITHIN BENCHMARK"
```

### Recipe 5 — Renewal calendar

```python
# Pull subscription renewal dates from GL + Ramp + vendor portal exports
from datetime import date, timedelta
import pandas as pd

renewals = pd.DataFrame([
  {"vendor":"Slack",      "amount":24_000, "renewal":date(2026,7,15)},
  {"vendor":"Zoom",       "amount":18_000, "renewal":date(2026,8,1)},
  {"vendor":"Salesforce", "amount":48_000, "renewal":date(2026,9,15)},
  # ...
]).sort_values("renewal")

# Surface next 90 days
upcoming = renewals[renewals.renewal <= date.today() + timedelta(days=90)]
upcoming["weeks_until"] = (upcoming.renewal - date.today()).dt.days // 7
print(upcoming)

# Rule of thumb: start renewal negotiation 60-90 days before contract end
# Many vendors auto-renew with 30-day cancellation; missing window = stuck
```

### Recipe 6 — Negotiation leverage table

```markdown
NEGOTIATION LEVERAGE INDICATORS

High leverage:
- 50%+ growth in seats since last contract
- Competitor offering similar product at 20%+ lower
- Multi-year commit possible (3-yr usually 20-30% off)
- Volume tier upgrade available
- End-of-quarter / end-of-year vendor pressure

Low leverage:
- Locked into platform (high switching cost)
- < 12 months tenure
- Already at lowest tier
- Vendor recently acquired (less pricing flexibility post-integration)

Tactics that work:
1. "I have budget for $X" (not "what's your best price")
2. Multi-year commit in exchange for X% discount
3. Cross-quarter timing (close last week of vendor's quarter)
4. Ask for "ramp clauses" (lower price year 1, higher year 2)
5. Cite specific competitor offer in writing
6. Bundle multiple products with same vendor
```

### Recipe 7 — Consolidate vendor count

```python
# Goal: reduce tail vendors (last 30 vendors by spend)
tail_vendors = spend_by_vendor.tail(30)
tail_total = tail_vendors.annual_spend.sum()
total_spend = spend_by_vendor.annual_spend.sum()
tail_pct = tail_total / total_spend

print(f"Tail (30 vendors): ${tail_total:,.0f} ({tail_pct:.0%} of total spend)")
# Action: eliminate or replace with consolidated tool
```

### Recipe 8 — Negotiation outreach template (Gmail)

```python
def negotiation_email(vendor_contact, vendor_name, current_spend, target_discount,
                     renewal_date, leverage_points):
    body = f"""
Hi {vendor_contact_first_name},

We're reviewing renewals for our {renewal_date.strftime('%B')} cycle and {vendor_name}
is up for renewal {renewal_date}. Current spend with you is ${current_spend:,}/year.

A few notes that may help us land at a renewal price that works for both of us:

{chr(10).join(f"- {pt}" for pt in leverage_points)}

We'd like to commit to {vendor_name} long-term and would propose:
- {target_discount:.0%} discount on current pricing
- 2-year term in exchange

Could we schedule 30 minutes to discuss? Earlier the better given our internal
budget timing.

Thanks,
{sender_name}
"""
    gmail.send(to=vendor_contact, subject=f"{vendor_name} renewal — {renewal_date}",
               body=body)
```

### Recipe 9 — TCO comparison (Make-vs-buy / vendor switch)

```python
def total_cost_of_ownership(vendor_option):
    return {
      "annual_license": vendor_option.annual_license,
      "implementation": vendor_option.implementation_one_time,
      "training": vendor_option.training_one_time,
      "migration_from_current": vendor_option.migration_cost,
      "ongoing_admin_FTE_hours_yr": vendor_option.admin_hours * blended_hourly_rate,
      "integration_cost": vendor_option.integration_one_time,
      "annual_total_year_1": vendor_option.annual_license + sum_one_times,
      "annual_total_year_2_plus": vendor_option.annual_license + vendor_option.admin_hours * blended_hourly_rate,
    }

# Compare two options over 3 years
option_a_total = sum([tco_a[k] for k in tco_a if k.startswith("annual_total")]) * [1,1,1]
option_b_total = sum([tco_b[k] for k in tco_b if k.startswith("annual_total")]) * [1,1,1]
print(f"3-year TCO: A=${sum(option_a_total):,.0f} | B=${sum(option_b_total):,.0f}")
```

### Recipe 10 — Quarterly SaaS audit report template

```markdown
SAAS SPEND AUDIT — Q2 2026

EXECUTIVE SUMMARY
- Total SaaS spend: $640K (T12M); $42K MoM run-rate
- Vendor count: 87 (vs 94 last quarter)
- Top 10 vendors: 74% of spend ($473K)
- Identified savings this quarter: $58K annualized

DUPLICATES IDENTIFIED
- [Tool A] + [Tool B] (project mgmt): consolidating to Tool A — $12K/yr savings
- [Tool C] + [Tool D] (storage): keeping D, sunsetting C — $4K/yr savings

LOW UTILIZATION
- [Tool E]: 8 of 25 seats active; downgrading — $6K/yr savings
- [Tool F]: 30 of 50 seats active; right-sizing — $9K/yr savings

OVERPAYING vs BENCHMARK
- [Tool G]: $X/seat vs benchmark $Y; negotiating at renewal — target $18K savings
- [Tool H]: 35% above median; negotiating — target $9K savings

UPCOMING RENEWALS (next 90 days)
- [Tool I] — 7/15 — start negotiation now
- [Tool J] — 8/1 — start negotiation by 7/1
- [Tool K] — 8/15 — multi-year commit option

ACTIONS THIS QUARTER
1. Consolidate project mgmt — done by 7/15
2. Negotiate Tool G renewal — by 7/15
3. Quarterly utilization review — Recurring
4. Vendor count target: < 80 by Q4
```

## Examples

### Example 1: Quarterly SaaS audit at Series A SaaS startup

**Goal:** Reduce SaaS spend 10-15% without disrupting operations.

**Steps:**

1. Pull spend data (Recipe 1).
2. Identify duplicates (Recipe 2) → 4 categories of redundancy found.
3. Cross-check utilization with SSO logs (Recipe 3) → 6 tools below 30%.
4. Benchmark top 10 vendors (Recipe 4) → 3 are overpaying significantly.
5. Build renewal calendar (Recipe 5).
6. Start negotiations 60 days pre-renewal (Recipe 8) on overpaying contracts.
7. Issue audit report (Recipe 10) to founder + leadership.
8. Track savings YTD: $58K annualized identified; ~$42K realized.

**Result:** ~9% spend reduction with no productivity impact.

### Example 2: Pre-renewal negotiation on Salesforce contract

**Goal:** $48K/yr Salesforce contract up for renewal in 60 days.

**Steps:**

1. Pull current spend + seat count (Recipe 1).
2. Benchmark: $200/seat vs benchmark $105/seat (Recipe 4) → 90% overpay.
3. Build leverage points (Recipe 6):
   - Headcount grew from 25 → 60 (3x seats potential, more leverage)
   - HubSpot Enterprise offered $80/seat for parallel evaluation
   - Multi-year commit option
4. Draft negotiation email (Recipe 8) targeting 30% off.
5. Initial response: 12% off. Counter: cite HubSpot, request 25%.
6. Result: 22% off + 3-year commit + extra training.

**Result:** $10.5K/yr savings ($31.5K over 3 years); same product, same outcomes.

## Edge cases / gotchas

- **Auto-renewal traps:** most SaaS auto-renews with 30-60 day cancellation window. Missing the window = locked in another year. Track in calendar.
- **Multi-year commit risk:** if your business changes, multi-year locks hurt. Negotiate "early termination for material breach" or "right to renegotiate at year 2".
- **Pricing changes mid-contract:** vendor pricing changes mid-term — verify your contract locks the per-seat rate, not just the total.
- **Vendor consolidation in industry:** when vendors get acquired, pricing often changes. Monitor M&A in your stack.
- **Hidden fees:** implementation, training, premium support, API overage. Get TCO not just license.
- **Negotiation leverage decays:** after you've adopted a tool, leverage decreases. Negotiate hard at initial purchase.
- **Free trials extending forever:** some vendors keep "free trial" features locked until paid. Audit free trials > 90 days.
- **Procurement vs finance roles:** if you have a procurement team, partner with them; if not, finance owns it. Don't let department heads sole-source major contracts.
- **Vendor-side time pressure:** end-of-vendor's-quarter / end-of-year = better deals. Identify their fiscal calendar.
- **Shadow IT:** marketing / sales / eng each may sign vendors without finance review. Run quarterly all-card audit (Recipe 1 includes all corp-card spend).
- **Negotiation patience pays:** standard SaaS negotiations take 2-4 weeks; complex enterprise 6-12 weeks. Don't rush.
- **Cancellation logistics:** some vendors require certified mail or in-app form. Don't just email; follow their cancellation procedure precisely.

## Sources

- Tropic 2025 SaaS spending trends: https://www.tropicapp.io/reports/software-spending-trends-2025
- Tropic SaaS budgeting: https://www.tropicapp.io/blog/saas-budgeting
- Spendflo pricing benchmarks: https://www.spendflo.com/pricing-benchmarks
- Vendr Marketplace: https://www.vendr.com/marketplace
- Spendhound alternatives: https://www.spendhound.com/blog/vendr-alternatives
- Cledara (EU focus): https://cledara.com/
- Sastrify (EU): https://sastrify.com/
- Zluri: https://www.zluri.com/

## Related skills

- `xero-quickbooks-bookkeeping` — GL data feeds Recipe 1
- `ramp-brex-expense-management` — corp-card data feeds Recipe 1
- `ar-ap-aging-collections` — vendor payments + early-pay discounts
- `cogs-margin-improvement-analysis` — vendor cost optimization in COGS bucket
