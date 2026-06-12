<!--
Sources: https://www.tropicapp.io/reports/software-spending-trends-2025
         https://www.spendhound.com/blog/best-saas-spend-management-software
         https://najar.ai/blog/spendflo-alternatives
Tropic benchmark: top-10 SaaS vendors = 74% of spend.
SSO log cross-ref = unused-seat killer.
-->
# SaaS Spend Audit — Vendr / Tropic / Spendflo — SKILL

Audit SaaS spend by joining four data sources: corporate card (Ramp / Brex), AP system (Xero / QuickBooks), SSO login logs (Okta / WorkOS / JumpCloud), and HRIS active-user roster. Surface duplicate tools, unused seats, dormant licenses, auto-renewals, and price drift. Produce a rationalization plan.

## When to use

- Annual or quarterly SaaS audit.
- Pre-board-meeting spend deep-dive.
- Investigating a budget overrun.
- New CFO / Ops lead wants a SaaS map.
- Trigger phrases: "SaaS audit", "spend audit", "unused seats", "shadow IT", "tool sprawl", "rationalize tools", "consolidation".

## Setup

```bash
export RAMP_TOKEN="xxx"         # Ramp Developer API
export BREX_TOKEN="xxx"         # Brex API (Capital One owned post-Apr 2026; product surface evolving)
export XERO_TOKEN="xxx"
export QBO_TOKEN="xxx"
export OKTA_TOKEN="xxx"
export WORKOS_KEY="xxx"
export RIPPLING_KEY="xxx"
export VENDR_KEY="xxx"          # optional managed-buying platform
export TROPIC_KEY="xxx"         # optional
export SPENDHOUND_KEY="xxx"     # has free tier
```

## Common recipes

### Recipe 1: Pull all card transactions (Ramp)
```bash
curl -s "https://api.ramp.com/developer/v1/transactions?state=CLEARED&from_date=2026-01-01" \
  -H "Authorization: Bearer $RAMP_TOKEN" \
  | jq '[.data[] | {date, merchant_name, amount_usd: (.amount_cents / 100), category: .sk_category_name}]'
```

### Recipe 2: Vendor consolidation by merchant fuzzy-match (Python)
```python
import pandas as pd
from rapidfuzz import fuzz

tx = pd.read_csv('ramp_export.csv')  # date, merchant, amount, category
# Normalize merchant
tx['merchant_clean'] = tx['merchant'].str.lower().str.replace(r'[^a-z]', '', regex=True)
# Cluster similar
clusters = {}
for m in tx['merchant_clean'].unique():
    matched = None
    for canonical in clusters:
        if fuzz.token_sort_ratio(m, canonical) > 85:
            matched = canonical
            break
    if matched:
        clusters[matched].append(m)
    else:
        clusters[m] = [m]
# Roll up spend per cluster
tx['canonical'] = tx['merchant_clean'].map({m: c for c, mlist in clusters.items() for m in mlist})
by_vendor = tx.groupby('canonical')['amount'].sum().sort_values(ascending=False)
print(by_vendor.head(20))  # Tropic benchmark: top-10 ≈ 74% of total
```

### Recipe 3: SSO log cross-reference for unused seats (Okta)
```bash
# Pull last 90 days of app logins per user
curl -s "https://<org>.okta.com/api/v1/logs?filter=eventType+eq+%22user.authentication.sso%22&since=2026-03-01" \
  -H "Authorization: SSWS $OKTA_TOKEN" \
  | jq '.[] | {user: .actor.alternateId, app: .target[0].displayName, ts: .published}' \
  > sso_logins.json

# Cross-reference with seat license count per app
# Users licensed but no login in 90 days → unused seat
```

### Recipe 4: Unused seat detection (Python)
```python
import pandas as pd, json
sso = pd.read_json('sso_logins.json')
sso['last_login'] = pd.to_datetime(sso['ts'])
last_per_user_app = sso.groupby(['user','app'])['last_login'].max().reset_index()

# Pull licensed users per app from each vendor (e.g., Slack admin.users.list, Notion users list)
licensed = pd.read_csv('vendor_seat_export.csv')  # user, app, license_tier
joined = licensed.merge(last_per_user_app, on=['user','app'], how='left')
dormant = joined[joined['last_login'].isna() | (joined['last_login'] < pd.Timestamp('2026-03-15'))]
dormant_cost = dormant.merge(pd.read_csv('cost_per_seat.csv'), on=['app','license_tier'])
print(dormant_cost.groupby('app')['cost_per_seat_USD'].sum().sort_values(ascending=False))
```

### Recipe 5: Duplicate-tool detection
```python
# Group by category — flag where >1 vendor in same category
CATEGORIES = {
  'Project Management': ['Linear','Jira','Asana','Trello','ClickUp','monday.com','Notion'],
  'Note Taking / KB': ['Notion','Confluence','Slab','Tettra','Slite','Obsidian'],
  'Design': ['Figma','Sketch','Adobe XD','Framer'],
  'Video Conferencing': ['Zoom','Google Meet','Teams','Webex'],
  'CRM': ['HubSpot','Salesforce','Pipedrive','Close','Attio','Folk'],
  'Marketing Email': ['HubSpot','Klaviyo','Mailchimp','Customer.io','Iterable','Braze'],
  'ATS': ['Greenhouse','Ashby','Lever','Workable'],
  'HRIS / Payroll': ['Rippling','Gusto','HiBob','Justworks','Deel','BambooHR'],
  'MDM': ['Iru','Kandji','Jamf','Intune','Rippling IT'],
  'Spend Mgmt': ['Vendr','Tropic','Spendflo','SpendHound','Cledara'],
}

def find_dupes(vendor_spend):
    by_cat = {}
    for v, spend in vendor_spend.items():
        for cat, vendors in CATEGORIES.items():
            if v in vendors:
                by_cat.setdefault(cat, []).append((v, spend))
    return {c: vs for c, vs in by_cat.items() if len(vs) > 1}
```

### Recipe 6: HRIS-active vs licensed reconciliation
```python
# Active employees from Rippling vs total licensed seats
rip = requests.get('https://api.rippling.com/platform/api/employees?status=active',
                   headers={'Authorization': f"Bearer {os.environ['RIPPLING_KEY']}"}).json()
active_emails = {e['workEmail'] for e in rip['data']}
licensed_emails = set(licensed['user'])
ex_employee_seats = licensed_emails - active_emails  # orphan seats — highest priority cleanup
print(f"Found {len(ex_employee_seats)} ex-employee orphan seats")
```

### Recipe 7: Top-10 vendor concentration (Tropic benchmark)
```python
# Tropic 2025 benchmark: top-10 SaaS vendors typically = 74% of total spend
total = by_vendor.sum()
top10_pct = by_vendor.head(10).sum() / total * 100
print(f"Top-10 concentration: {top10_pct:.1f}% (benchmark: 74%)")
# > 80% means risky concentration; < 60% means probable sprawl
```

### Recipe 8: Auto-renewal detection
```bash
# Pull invoices from Xero, flag recurring with >5% YoY uplift
curl -s "https://api.xero.com/api.xro/2.0/Invoices" \
  -H "Authorization: Bearer $XERO_TOKEN" -H "Xero-tenant-id: <tenant>" -H "Accept: application/json" \
  | jq '[.Invoices[] | select(.Type=="ACCPAY" and .Status=="PAID") | {date: .Date, contact: .Contact.Name, total: .Total}]'

# Then in Python: detect repeating contact+amount sequences with YoY > 5% delta = uplift renewal
```

### Recipe 9: Spend rationalization plan (template)
```markdown
# SaaS Audit — Q3 2026

## Headline
- Total annual SaaS run-rate: $<X>
- Top-10 concentration: <N>% (benchmark: 74%)
- Estimated annualized waste: $<X> from dormant seats + duplicates

## Quick wins (this month)
| Action | Vendor | Annual savings |
|--------|--------|----------------|
| Reclaim orphan seats from ex-employees | Slack, Notion, GitHub | $X |
| Downgrade dormant Tier-Pro to Tier-Standard | Vendor B | $X |
| Cancel duplicate (KB has both Notion + Confluence) | Confluence | $X |
| Move from 1-yr to 3-yr lock for top-3 vendors | A, B, C | $X (15%) |

## Renewal calendar — next 6 months
| Vendor | Renewal date | Annual $ | Negotiation lever |
|--------|-------------|----------|-------------------|
| | | | |

## Tools to evaluate replacing
- Vendor X (replaceable with built-in Y feature)

## Recommended consolidations
- KB: standardize on Notion; sunset Confluence Q4
- VC: standardize on Zoom; sunset Meet ent license
```

### Recipe 10: SpendHound free spend visibility
```bash
# SpendHound free tier — automatic detection from card data
curl -s "https://api.spendhound.com/v1/subscriptions" \
  -H "Authorization: Bearer $SPENDHOUND_KEY" \
  | jq '.[] | {name, annual_cost_USD, renewal_date, users_count}'
```

### Recipe 11: Productiv / Torii usage-based optimization
```bash
# Productiv pulls SSO + app activity logs; surfaces unused even when SSO not enforced
curl -s "https://api.productiv.com/v1/applications" \
  -H "Authorization: Bearer $PRODUCTIV_TOKEN" \
  | jq '.[] | {app, license_cost_USD, active_users, license_count, utilization: (.active_users/.license_count*100)}'
```

## Examples

### Example 1: Pre-board quarterly audit
**Goal:** Cut 15% from SaaS run-rate before next board meeting.
**Steps:**
1. Recipe 1: Ramp YTD transaction pull.
2. Recipe 2: cluster + roll up by vendor.
3. Recipe 7: top-10 concentration math.
4. Recipe 3 + 4: Okta logs → unused seats.
5. Recipe 5: dup-tool detection.
6. Recipe 6: orphan seats from ex-employees.
7. Recipe 8: auto-renewal upcoming + uplift detection.
8. Recipe 9: write the rationalization plan.
9. Notion `Finance/SaaS-Audit/Q3-2026` + Slack #ops summary.

**Result:** Documented audit; ~12-18% typical savings; renewal calendar live.

### Example 2: New employee asks "what tools do we have?"
**Goal:** Inventory + permissions clarity.
**Steps:**
1. Recipe 1 + 2: produce vendor list.
2. Cross-reference Okta app catalog for SSO-managed vs shadow.
3. Publish inventory to Notion `IT/Tools-Catalog` with onboarding-tier flags (default-on / on-request / role-specific).

**Result:** Authoritative tool catalog; onboarding accelerates.

## Edge cases / gotchas

- **Shadow IT.** Stuff paid on personal card + expensed will not show in Ramp/Brex. Backstop: monthly Expensify/Ramp expense reports — flag "Software" category. Also: scrape Google login Audit log for unmanaged SaaS sign-ins via Gmail OAuth.
- **Annual vs monthly billing.** Annual invoices = quarterly 3x spike in spend pattern; don't mistake for waste.
- **Multi-entity finance.** Parent + sub vendors invoice differently (e.g., HubSpot vs HubSpot Inc EU). Recipe 2 fuzzy match handles most.
- **SSO bypass.** Users with non-SSO emails (alex@personal.com) won't show in Okta logs. Force SSO via vendor admin; or rely on vendor admin's user-list export.
- **Seat-true-up timing.** Some vendors true up annually (no mid-year savings). Negotiate quarterly true-down at renewal.
- **Tropic / Vendr managed deals.** These platforms often save 10-30% but take a cut. Compare net savings carefully on deals < $20k where the cut eats savings.
- **Brex post-acquisition (April 2026 Capital One).** API surface and product positioning evolving; verify Recipe data shape before automating.
- **Free-tier graduation traps.** Notion, Slack, Figma free tiers convert to paid silently when seat thresholds hit. Monitor seat counts monthly.
- **Auto-renewal already triggered.** If you're inside 30-day notice window, cancellation is forfeit for the next term. Recipe 4 calendar is non-negotiable.
- **Defer to `legal-counsel` for binding contract review on cancellation rights, MSA term-end notice provisions, and renewal-language interpretation.**

## Sources

- Tropic 2025 SaaS Buying Trends: https://www.tropicapp.io/reports/software-spending-trends-2025
- SpendHound — Best SaaS Spend Mgmt 2026: https://www.spendhound.com/blog/best-saas-spend-management-software
- Najar — Spendflo Alternatives 2026: https://najar.ai/blog/spendflo-alternatives
- Receiptor — Brex Alternatives Post-Capital One 2026: https://receiptor.ai/blog/brex-alternatives-after-the-capital-one-acquisition-2026
- Ramp Developer API: https://docs.ramp.com/
- Okta System Log API: https://developer.okta.com/docs/reference/api/system-log/
- Productiv: https://productiv.com/
- Vendr buyer guides: https://www.vendr.com/buyer-guides
