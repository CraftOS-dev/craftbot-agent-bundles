<!--
Source: https://zylo.com/ + https://productiv.com/ + https://vendr.com/ + https://www.openview.com/saas-sales-tech-stack/
Sales tech stack consolidation + utilization audit — Zylo / Productiv / Vendr + per-tool admin APIs (June 2026 SOTA).
-->
# Sales Tech Stack Consolidation Audit — SKILL

Audit current sales tech stack — name, cost, license count, active users (30/60/90-day login), overlap with peer tools. Decide **kill / keep / renegotiate / consolidate**. **Zylo** + **Productiv** for SaaS Management Platforms (SMPs) — automated discovery + utilization across the org. **Vendr** for vendor negotiation + benchmark pricing. Per-tool admin APIs (Outreach, Salesloft, Gong, Apollo, ZoomInfo) for direct utilization pull. Annual rationalization saves typical SalesOps org 20-40% of stack spend.

## When to use

- **Annual stack review** — pre-renewal cycle, find tools to kill / consolidate.
- **Renewal coming up in 90 days** — pull utilization + cost-per-active-user.
- **Overlap audit** — Apollo + ZoomInfo + Cognism all active; pick one.
- **License right-sizing** — 100 Outreach seats, 60 active; renew at 70 with buffer.
- **Vendor negotiation** — benchmark per-seat cost vs Vendr peer data.
- **Shadow IT discovery** — Zylo / Productiv surface tools paid-with-credit-card outside procurement.
- **Trigger phrases**: "tech stack audit", "tool utilization", "SaaS rationalization", "renewal review", "Zylo", "Productiv", "Vendr benchmark", "kill or keep", "license count", "stack consolidation".

Do NOT use this skill for: **tool selection for net-new category** (use brave-search / firecrawl for vendor comparison); **tool onboarding / admin** (use the tool's own skill, e.g., `salesloft-outreach-tech-stack-admin`); **commission tool admin** (use `commission-spiff-quotapath-captivateiq`).

## Setup

```bash
# Zylo — API key (Settings → Integrations → API)
export ZYLO_TOKEN="<token>"
export ZYLO_BASE="https://api.zylo.com/v2"

# Productiv — OAuth token
export PRODUCTIV_TOKEN="<token>"
export PRODUCTIV_BASE="https://api.productiv.com/v1"

# Vendr — API access (paid tier)
export VENDR_TOKEN="<token>"
export VENDR_BASE="https://api.vendr.com/v1"

# Per-tool admin tokens
export OUTREACH_TOKEN="<token>"
export SALESLOFT_TOKEN="<token>"
export GONG_TOKEN="<token>"
export APOLLO_TOKEN="<token>"
export ZOOMINFO_TOKEN="<token>"
export HIGHSPOT_TOKEN="<token>"
export SPIFF_TOKEN="<token>"
# ... etc

# api-gateway fallback (Maton-onboarded)
export MATON_API_KEY="<key>"

pip install pandas matplotlib requests jinja2
```

Required:
- Admin role on each tool to be audited
- SMP subscription if going beyond manual (Zylo: ~$50-100/employee/yr; Productiv: similar)
- Vendr subscription if leveraging benchmark data (or use public Vendr deal data + LinkedIn comp lookups)
- Finance partnership — contract dates + costs in NetSuite / Quickbooks / Spendesk

## Common recipes

### Recipe 1: Tool inventory (canonical YAML)

```yaml
sales_tech_stack:
  - name: "Salesforce Sales Cloud"
    category: CRM
    annual_cost_usd: 180000
    license_count: 100
    contract_renewal: 2027-03-01
    vendor: Salesforce
    owner_team: SalesOps
    util_endpoint: "salesforce-api"

  - name: "Outreach"
    category: sales_engagement
    annual_cost_usd: 60000
    license_count: 50
    contract_renewal: 2026-09-30
    vendor: Outreach
    owner_team: SalesOps
    util_endpoint: "/outreach/api/v2/users"

  - name: "Salesloft"
    category: sales_engagement
    annual_cost_usd: 36000
    license_count: 30
    contract_renewal: 2026-11-15
    vendor: Salesloft
    owner_team: SalesOps
    util_endpoint: "/salesloft/v2/users"
    overlap_with: "Outreach"

  - name: "Apollo"
    category: enrichment
    annual_cost_usd: 25000
    license_count: 50
    contract_renewal: 2026-08-01
    vendor: Apollo.io
    util_endpoint: "/apollo/api/v1/users"
    overlap_with: "ZoomInfo, Cognism"

  - name: "ZoomInfo"
    category: enrichment
    annual_cost_usd: 65000
    license_count: 25
    contract_renewal: 2026-12-31
    vendor: ZoomInfo
    util_endpoint: "/zoominfo/users"

  - name: "Cognism"
    category: enrichment
    annual_cost_usd: 30000
    license_count: 15
    contract_renewal: 2026-10-15
    util_endpoint: "/cognism/users"

  - name: "Gong"
    category: conversation_intelligence
    annual_cost_usd: 90000
    license_count: 75
    contract_renewal: 2026-07-31
    util_endpoint: "/gong/v2/users"

  - name: "Highspot"
    category: enablement
    annual_cost_usd: 85000
    license_count: 100
    contract_renewal: 2027-01-15
    util_endpoint: "/highspot/v0.5/users"

  - name: "Spiff"
    category: icm
    annual_cost_usd: 48000
    license_count: 80
    contract_renewal: 2026-09-01
    util_endpoint: "/spiff/v1/users"

# Total annual: ~$619K across 9 tools
```

Stored in `notion` as the canonical inventory; agent reads + writes.

### Recipe 2: Zylo — discovery + utilization pull

```bash
# All SaaS apps discovered in the org
curl -s "$ZYLO_BASE/applications" \
  -H "Authorization: Bearer $ZYLO_TOKEN" | jq '.[] | {name, vendor, monthly_cost, license_count, active_users_30d, active_users_90d, last_login}'

# Drill into a specific app
curl -s "$ZYLO_BASE/applications/APP_ID/users" \
  -H "Authorization: Bearer $ZYLO_TOKEN" | jq '.[] | {email, last_login, license_assigned}'

# Spend by category
curl -s "$ZYLO_BASE/spend?group_by=category&period=last_12m" \
  -H "Authorization: Bearer $ZYLO_TOKEN" | jq '.results[]'
```

Zylo discovers shadow IT via SSO logs + expense report scan — surfaces apps that procurement didn't know existed.

### Recipe 3: Productiv — engagement scoring

```bash
# Engagement scoring per app (Productiv's signature metric)
curl -s "$PRODUCTIV_BASE/applications" \
  -H "Authorization: Bearer $PRODUCTIV_TOKEN" | jq '.[] | {name, engagement_score, active_users, total_licenses, monthly_cost}'

# Drill: feature-level usage (what features inside the tool people actually use)
curl -s "$PRODUCTIV_BASE/applications/APP_ID/features" \
  -H "Authorization: Bearer $PRODUCTIV_TOKEN" | jq '.[] | {feature, usage_rate, daily_active_users}'
```

Productiv's engagement score combines login frequency + depth of feature use + days-since-last-login. Score < 30 = kill candidate.

### Recipe 4: Per-tool admin API utilization pull (Python)

```python
import requests
from datetime import datetime, timedelta, timezone
import pandas as pd

now = datetime.now(timezone.utc)
cutoff_30d = now - timedelta(days=30)
cutoff_90d = now - timedelta(days=90)

def pull_users(endpoint, token, last_login_field="last_login_at"):
    """Generic pull — most tools follow this pattern."""
    r = requests.get(f"https://gateway.maton.ai{endpoint}",
                     headers={"Authorization": f"Bearer {token}"})
    users = r.json().get("data", r.json())
    return [{
        "email": u.get("email"),
        "last_login": datetime.fromisoformat(u[last_login_field].replace("Z","+00:00")) if u.get(last_login_field) else None,
    } for u in users]

tools = [
    {"name": "Outreach",   "endpoint": "/outreach/api/v2/users",   "token": OUTREACH_TOKEN,   "license_count": 50, "annual_cost": 60000, "field": "last_active_at"},
    {"name": "Salesloft",  "endpoint": "/salesloft/v2/users",      "token": SALESLOFT_TOKEN,  "license_count": 30, "annual_cost": 36000, "field": "last_seen_at"},
    {"name": "Gong",       "endpoint": "/gong/v2/users",           "token": GONG_TOKEN,       "license_count": 75, "annual_cost": 90000, "field": "lastLogin"},
    {"name": "Apollo",     "endpoint": "/apollo/api/v1/users",     "token": APOLLO_TOKEN,     "license_count": 50, "annual_cost": 25000, "field": "last_active_at"},
    {"name": "ZoomInfo",   "endpoint": "/zoominfo/users",          "token": ZOOMINFO_TOKEN,   "license_count": 25, "annual_cost": 65000, "field": "lastLoginDate"},
    {"name": "Highspot",   "endpoint": "/highspot/v0.5/users",     "token": HIGHSPOT_TOKEN,   "license_count": 100, "annual_cost": 85000, "field": "last_login"},
    {"name": "Spiff",      "endpoint": "/spiff/v1/users",          "token": SPIFF_TOKEN,      "license_count": 80, "annual_cost": 48000, "field": "last_sign_in_at"},
]

results = []
for t in tools:
    users = pull_users(t["endpoint"], t["token"], t["field"])
    active_30d = sum(1 for u in users if u["last_login"] and u["last_login"] > cutoff_30d)
    active_90d = sum(1 for u in users if u["last_login"] and u["last_login"] > cutoff_90d)
    util_30 = active_30d / t["license_count"]
    cost_per_active = t["annual_cost"] / max(active_30d, 1)
    results.append({
        "tool": t["name"],
        "license_count": t["license_count"],
        "active_30d": active_30d,
        "active_90d": active_90d,
        "util_30": util_30,
        "annual_cost": t["annual_cost"],
        "cost_per_active": cost_per_active,
    })

df = pd.DataFrame(results).sort_values("util_30")
df.to_csv("stack_utilization.csv", index=False)
print(df)
```

### Recipe 5: Kill / keep / renegotiate scoring matrix

```python
def recommendation(util_30):
    if util_30 >= 0.70: return "KEEP — renew at current seats"
    if util_30 >= 0.50: return "RENEGOTIATE — cut seats 20-30%"
    if util_30 >= 0.30: return "CRITICAL LOOK — kill or consolidate with overlap"
    return "KILL — at renewal unless strategic"

df["recommendation"] = df["util_30"].apply(recommendation)

# Total potential savings (KILL + 25% seat cut on RENEGOTIATE)
df["potential_savings"] = df.apply(lambda r: (
    r["annual_cost"] if "KILL" in r["recommendation"] else
    r["annual_cost"] * 0.25 if "RENEGOTIATE" in r["recommendation"] else
    0
), axis=1)

print(f"Total potential annual savings: ${df['potential_savings'].sum():,.0f}")
```

### Recipe 6: Overlap detection (category collision)

```python
# Detect overlapping tools per category
stack = pd.read_csv("stack.csv")  # category column required
overlaps = stack.groupby("category").agg(
    tool_count=("tool", "count"),
    tools=("tool", lambda s: list(s)),
    combined_cost=("annual_cost", "sum")
).query("tool_count > 1")

print("Overlap candidates:")
for cat, row in overlaps.iterrows():
    print(f"  {cat}: {row['tools']} — ${row['combined_cost']:,.0f}/yr")
```

Typical overlaps to surface:
- **Enrichment**: Apollo + ZoomInfo + Cognism + LeadIQ
- **Sales engagement**: Outreach + Salesloft (almost never both fully needed)
- **CI**: Gong + Chorus + Fathom
- **Dedup**: LeanData Dedup + Cloudingo + DupeBlocker
- **CPQ**: Salesforce CPQ + Conga (legacy migration)
- **Enablement**: Highspot + Showpad + Seismic

### Recipe 7: Vendr — benchmark cost per seat

```bash
# Get benchmark pricing for a vendor
curl -s "$VENDR_BASE/benchmarks/outreach?segment=mid-market" \
  -H "Authorization: Bearer $VENDR_TOKEN" | jq '{
    median_per_seat_annual: .pricing.median_per_seat_annual,
    p25_per_seat: .pricing.p25_per_seat,
    p75_per_seat: .pricing.p75_per_seat,
    sample_size: .pricing.sample_size,
    typical_discount_pct: .pricing.typical_discount_pct
  }'
```

### Recipe 8: Renegotiation prep doc (per tool)

```python
from jinja2 import Template

tmpl = Template("""
# Renewal Brief — {{tool}}

**Contract**: ${{annual_cost:,.0f}}/yr, {{license_count}} seats, renews {{renewal_date}}
**Utilization (30d)**: {{active_30d}}/{{license_count}} = {{util_pct:.0%}}
**Cost per active user**: ${{cost_per_active:,.0f}}

## Benchmark (Vendr)
- Peer median per-seat (annual): ${{benchmark_median:,.0f}}
- Our per-seat (annual): ${{our_per_seat:,.0f}}
- Delta: {{seat_premium:+.0%}} vs benchmark
- Typical negotiation discount: {{typical_discount:.0%}}

## Negotiation strategy
- Target reduction: {{target_seats}} seats (from {{license_count}}, -{{seat_cut:.0%}})
- Target price ceiling: ${{target_cost:,.0f}}/yr ({{target_per_seat:,.0f}}/seat)
- Walk-away: ${{walk_cost:,.0f}}/yr; alternative is {{alternative_tool}}
- Multi-year? {{multiyear_offer}}

## Risk
{{risk_note}}

## Action items
- [ ] {{owner}} kicks off renewal conversation by {{kickoff_date}}
- [ ] CRO sign-off on walk-away if seat ask rejected
- [ ] Document final terms in notion vendor log
""")

# Render per tool with KILL/RENEGOTIATE recommendation
for _, r in df.query("util_30 < 0.70").iterrows():
    bench = requests.get(f"{VENDR_BASE}/benchmarks/{r['tool'].lower()}",
        headers={"Authorization": f"Bearer {VENDR_TOKEN}"}).json()
    doc = tmpl.render(
        tool=r["tool"], annual_cost=r["annual_cost"],
        license_count=r["license_count"], active_30d=r["active_30d"],
        util_pct=r["util_30"], cost_per_active=r["cost_per_active"],
        benchmark_median=bench["pricing"]["median_per_seat_annual"],
        our_per_seat=r["annual_cost"]/r["license_count"],
        seat_premium=(r["annual_cost"]/r["license_count"])/bench["pricing"]["median_per_seat_annual"] - 1,
        typical_discount=bench["pricing"]["typical_discount_pct"],
        target_seats=int(r["active_30d"] * 1.15),  # active + 15% headroom
        seat_cut=1 - (r["active_30d"] * 1.15 / r["license_count"]),
        target_cost=r["active_30d"] * 1.15 * bench["pricing"]["p25_per_seat"],
        target_per_seat=bench["pricing"]["p25_per_seat"],
        walk_cost=0, alternative_tool="<TBD>",
        multiyear_offer="Yes — 2yr commit for additional 8-12% off",
        owner="SalesOps lead", kickoff_date="60 days before renewal",
        renewal_date="<from contract>", risk_note="Low — usage data supports cut"
    )
    with open(f"renewal_brief_{r['tool']}.md", "w") as f: f.write(doc)
```

### Recipe 9: Stack rationalization scenario (Apollo vs ZoomInfo example)

```python
# Both used for enrichment. Compare per-call cost and value.
apollo = {
    "annual_cost": 25000, "license_count": 50, "active_30d": 35,
    "enrichments_30d": 8500,
    "match_rate": 0.72,
}
zoominfo = {
    "annual_cost": 65000, "license_count": 25, "active_30d": 12,
    "enrichments_30d": 1200,
    "match_rate": 0.86,
}

for tool, name in [(apollo, "Apollo"), (zoominfo, "ZoomInfo")]:
    cost_per_enrichment = tool["annual_cost"] / 12 / tool["enrichments_30d"]
    cost_per_match = cost_per_enrichment / tool["match_rate"]
    cost_per_active = tool["annual_cost"] / tool["active_30d"]
    print(f"{name}: ${cost_per_match:.2f}/match, ${cost_per_active:,.0f}/active user, util {tool['active_30d']/tool['license_count']:.0%}")

# Recommendation: Apollo for volume + cost; ZoomInfo for premium accounts only (reduce seats from 25 → 8)
# Estimated savings: ZoomInfo $65K → $25K = $40K/yr
```

### Recipe 10: Shadow IT discovery via SSO

```bash
# Pull SSO login events (Okta / Azure AD / Google Workspace)
# Find apps with > 5 unique sign-ins last 90 days but NOT in stack.csv
curl -s "https://your-org.okta.com/api/v1/logs?filter=eventType+eq+%22user.authentication.sso%22&since=2026-03-01" \
  -H "Authorization: SSWS $OKTA_TOKEN" | jq '.[] | .target[] | select(.type == "AppInstance") | .displayName' | sort -u > sso_apps.txt

# Compare to known stack
comm -23 <(sort sso_apps.txt) <(sort stack_known.txt) > shadow_apps.txt
```

### Recipe 11: Annual rationalization report

```python
# Big-picture: total spend, savings opportunity, kill list, renegotiate list, keep list
report = {
    "total_annual_spend": df["annual_cost"].sum(),
    "potential_savings": df["potential_savings"].sum(),
    "savings_pct": df["potential_savings"].sum() / df["annual_cost"].sum(),
    "kill_list": df[df["recommendation"].str.contains("KILL")][["tool", "annual_cost", "util_30"]].to_dict("records"),
    "renegotiate_list": df[df["recommendation"].str.contains("RENEGOTIATE")][["tool", "annual_cost", "util_30"]].to_dict("records"),
    "keep_list": df[df["recommendation"].str.contains("KEEP")][["tool", "annual_cost", "util_30"]].to_dict("records"),
}
print(f"Total spend: ${report['total_annual_spend']:,.0f}")
print(f"Potential savings: ${report['potential_savings']:,.0f} ({report['savings_pct']:.0%})")
```

### Recipe 12: api-gateway fallback

```bash
curl "https://gateway.maton.ai/zylo/v2/applications" \
  -H "Authorization: Bearer $MATON_API_KEY"

curl "https://gateway.maton.ai/productiv/v1/applications" \
  -H "Authorization: Bearer $MATON_API_KEY"

curl "https://gateway.maton.ai/vendr/v1/benchmarks/outreach" \
  -H "Authorization: Bearer $MATON_API_KEY"
```

## Examples

### Example 1: Annual rationalization — find $200K savings

**Goal:** Pre-budget cycle audit; surface ~$200K savings on $619K stack.

**Steps:**
1. Recipe 1 — confirm canonical inventory in notion.
2. Recipe 4 — utilization pull across all tools.
3. Recipe 5 — kill/keep/renegotiate scoring.
4. Recipe 6 — overlap detection. Find Apollo+ZoomInfo+Cognism overlap.
5. Recipe 9 — per-overlap scenario analysis. Recommend ZoomInfo seat cut + Cognism kill.
6. Recipe 7 — Vendr benchmarks for the renegotiate list.
7. Recipe 8 — generate renewal briefs per renegotiating tool.
8. Recipe 11 — annual report to CRO + CFO. Walk into Q4 budget meeting with $230K of identified savings.

**Result:** Stack spend drops from $619K → $390K; tool count from 9 → 7; per-AE access unchanged.

### Example 2: Apollo + ZoomInfo overlap kill

**Goal:** Decide which enrichment tool to keep.

**Steps:**
1. Recipe 9 — direct cost-per-match comparison.
2. Apollo: $25K, 35/50 active, 72% match rate, $0.40/match.
3. ZoomInfo: $65K, 12/25 active, 86% match rate, $6.30/match.
4. ZoomInfo cost-per-match is 15× Apollo. Premium accounts only justify it.
5. Cut ZoomInfo from 25 → 8 seats (CRO + named-AE only).
6. Recipe 8 — renewal brief with Vendr benchmark.
7. Negotiate ZoomInfo down to $20K from $65K; keep Apollo full team.

**Result:** $45K saved; 80% of enrichment volume preserved; premium tier-1 accounts still get ZoomInfo depth.

### Example 3: Shadow IT spike — 4 unauthorized tools

**Goal:** Zylo flagged 4 sales tools paid by individual reps on credit cards.

**Steps:**
1. Recipe 10 or Zylo — surface shadow apps.
2. Investigate: LinkedIn Sales Nav personal subs ($200/mo × 5 reps = $12K/yr), Clay personal sub ($150/mo), Apollo individual seats outside main contract.
3. Triage: bundle to existing contracts at corporate rate.
4. LinkedIn Sales Nav: negotiate team contract at $80/seat/mo (vs $200 personal) → save 60%.
5. Clay: consolidate under SalesOps-owned workspace (was personal).
6. Apollo: roll the 3 personal seats into the corporate contract.
7. Memo to reps: future tool requests go through SalesOps + procurement.

**Result:** $8K direct savings + central observability over the enrichment stack.

## Edge cases / gotchas

- **Last login ≠ active user** — some tools log "session" but rep may have only clicked through. Productiv engagement score handles this; raw last_login does not.
- **License vs seat vs concurrent license** — some tools (older Anaplan) have concurrent licenses, not per-seat. Adjust utilization math.
- **Free-tier tools won't appear in Zylo** — Zylo discovers paid SaaS via SSO + expense. Free tools (HubSpot Free, Clay free tier) need manual inventory.
- **Multi-product vendors** — Salesforce alone might be Sales Cloud + Service Cloud + CPQ + Spiff. Each has separate utilization. Treat as distinct line items.
- **Pilot / trial tools** — short-term contracts (90-day trial) shouldn't be scored against utilization yet. Tag separately.
- **Procurement contract terms might block kills mid-term** — auto-renewing contracts require 90-120 day notice. Calendar all renewals in `notion` 120 days out.
- **Vendor will counter with bundle deals** — kill threats often surface "70% off if you add product X." Worth comparing to standalone competitor cost.
- **Vendr benchmarks can lag** — current pricing on AI-powered tools (especially in CI / forecasting) moves quickly. Cross-check with at-least one peer SalesOps lead in Pavilion / RevOps Collective Slack.
- **Cost-per-active misleads at small N** — 2 active users on a $30K tool = $15K/user. Doesn't mean it's expensive; might be the only enterprise tier 1 user. Read context.
- **Killing a tool deletes data** — assess data retention before kill. Export call recordings (Gong), pipelines (Highspot views), commission histories (Spiff) before contract end.
- **Tool consolidation needs change management** — moving 30 reps from Salesloft to Outreach is a 6-week retraining project. Budget the time, not just the dollar.
- **Compliance/security review** — SOC2 + GDPR review per tool. Some tools are kept despite low utilization because they're compliant alternatives to a non-compliant one.
- **Departmental ownership disputes** — Marketing might claim Apollo; CS might claim Gong. Stack audit needs business-unit alignment first.
- **CRO override** — final kill/keep decision sits with CRO + sometimes CIO. SalesOps recommends; doesn't unilaterally cancel contracts.
- **Per-tool "active" definition varies** — "last login in 30 days" for SaaS engagement is loose. For dashboards (CRMA, Looker), even 90-day login can be enough if heavy usage in spike periods. Calibrate by category.

## Sources

- [Zylo — SaaS Management Platform](https://zylo.com/)
- [Zylo Developer Documentation](https://docs.zylo.com/)
- [Productiv — SaaS Engagement Score](https://productiv.com/)
- [Productiv API Documentation](https://docs.productiv.com/)
- [Vendr — SaaS Procurement + Benchmarks](https://vendr.com/)
- [Vendr Pricing Data](https://www.vendr.com/marketplace)
- [OpenView — SaaS Sales Tech Stack Guide](https://www.openview.com/saas-sales-tech-stack/)
- [G2 Stack — Tool Comparison Data](https://www.g2.com/sectors/sales)
- [SaaS Optics — Spend Management](https://www.saasoptics.com/)
- [Salesforce — Sales Hub Admin API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/)
- [Outreach Users API](https://developers.outreach.io/api/v2/users)
- [Salesloft Users API](https://developers.salesloft.com/api.html#!/Users)
- [Gong Users API](https://app.gong.io/settings/api/documentation#overview)
- [Apollo Users API](https://docs.apollo.io/reference/list-users)
- [Pavilion — Annual SaaS Stack Audit Playbook](https://www.joinpavilion.com/resources/saas-audit)
