<!--
Source: https://www.eaglerockcfo.com/blog/research/saas-finance-metrics-benchmarks
Source: https://www.bessemerventures.com/atlas/scaling-to-100-million
Source: https://aws.amazon.com/billing/api/
Source: https://docs.anthropic.com/en/api/usage
-->

# COGS analysis + gross margin improvement

Decompose SaaS COGS: hosting + support + payment fees + LLM inference + 3rd-party APIs. Target gross margin >75% (healthy) / >80% (elite). Diagnose drift; surface levers.

## When to use

- Gross margin dropping quarter-over-quarter.
- Pre-fundraise: defend gross margin trajectory.
- Quarterly COGS review.
- New product launch: model COGS for unit economics.
- AWS / GCP commitment decision (RI, savings plans).
- Trigger phrases: "gross margin", "COGS", "hosting cost", "inference cost", "support cost", "AWS RI", "margin drop".

NOT for: total spend audit (use `vendor-procurement-saas-spend-audit`); pricing decisions (use `unit-economics-saas-metrics` + product manager).

## Setup

```bash
# Cost data sources:
# - AWS billing: cli-anything → curl ce.amazonaws.com (Cost Explorer)
# - GCP billing: cli-anything → bq query billing tables
# - Azure cost: az cost management
# - Stripe processing fees: stripe-mcp (default skill)
# - LLM provider billing: cli-anything → Anthropic /usage, OpenAI /usage
# - Support staff cost: xero-mcp + HRIS
```

## What goes in SaaS COGS

```
COGS LINE ITEMS (typical SaaS)
1. Hosting / infrastructure
   - AWS / GCP / Azure compute, storage, networking
   - CDN (CloudFront, Fastly, Cloudflare)
   - Database hosting (RDS, Snowflake, MongoDB Atlas)

2. Third-party APIs (delivery cost)
   - LLM inference (Anthropic, OpenAI, Cohere) — fastest-growing line in 2026
   - Maps / geocoding (Google Maps, Mapbox)
   - Email delivery (SendGrid, Postmark)
   - SMS (Twilio)
   - Payment processing (Stripe, Adyen)

3. Customer support
   - Support engineering salaries (fully loaded)
   - Customer success allocation (50% typical)
   - Support tools (Zendesk, Intercom)

4. Implementation / professional services
   - Solutions engineering allocation
   - Onboarding team

5. Reseller / channel fees
   - AWS Marketplace 3% (or 2% with negotiation)
   - Google Cloud Marketplace 3%
   - App store fees (Apple 15-30%, Google 15-30%)
```

NOT COGS (these are OPEX):
- Sales + marketing salaries (S&M)
- Product development / engineering (R&D)
- G&A
- Office, IT for non-revenue staff

## Common recipes

### Recipe 1 — Pull current AWS spend by service

```bash
# Cost Explorer API
curl -X POST "https://ce.us-east-1.amazonaws.com/" \
  -H "X-Amz-Target: AWSInsightsIndexService.GetCostAndUsage" \
  -H "Content-Type: application/x-amz-json-1.1" \
  --aws-sigv4 "aws:amz:us-east-1:ce" \
  -d '{
    "TimePeriod":{"Start":"2026-06-01","End":"2026-06-30"},
    "Granularity":"DAILY",
    "Metrics":["UnblendedCost"],
    "GroupBy":[{"Type":"DIMENSION","Key":"SERVICE"}]
  }'
```

Output: per-service spend. Identify top 5; investigate any service >10% MoM jump.

### Recipe 2 — Pull LLM inference cost (Anthropic)

```bash
curl -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  "https://api.anthropic.com/v1/organizations/usage_reports?start_date=2026-06-01&end_date=2026-06-30"
```

OpenAI equivalent:

```bash
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  "https://api.openai.com/v1/dashboard/billing/usage?start_date=2026-06-01&end_date=2026-06-30"
```

### Recipe 3 — Compute gross margin

```python
def gross_margin(revenue, cogs):
    return (revenue - cogs) / revenue

# Pull period revenue + COGS from Xero
revenue = xero.reports.profit_and_loss(...).revenue
cogs = xero.reports.profit_and_loss(...).cogs
gm = gross_margin(revenue, cogs)
print(f"Gross Margin: {gm:.1%}")
# Benchmark: >75% healthy SaaS | >80% elite
```

### Recipe 4 — COGS decomposition

```python
import pandas as pd

cogs_decomp = pd.DataFrame([
  {"category":"Hosting (AWS)",          "amount": 18_500, "pct_revenue": 5.7, "pct_cogs": 24.4},
  {"category":"CDN (CloudFront)",       "amount":  1_200, "pct_revenue": 0.4, "pct_cogs":  1.6},
  {"category":"LLM Inference (Anthropic)","amount": 12_400, "pct_revenue": 3.8, "pct_cogs": 16.3},
  {"category":"Payment fees (Stripe)",  "amount":  9_400, "pct_revenue": 2.9, "pct_cogs": 12.4},
  {"category":"Email delivery (SG)",    "amount":    800, "pct_revenue": 0.2, "pct_cogs":  1.1},
  {"category":"Support staff loaded",   "amount": 26_000, "pct_revenue": 8.0, "pct_cogs": 34.3},
  {"category":"Customer Success alloc", "amount":  7_500, "pct_revenue": 2.3, "pct_cogs":  9.9},
])
print(cogs_decomp.sort_values("pct_cogs", ascending=False))
```

### Recipe 5 — Identify drivers of margin drift

```python
def margin_drift_analysis(this_q, last_q):
    drift = {}
    for cat in this_q.category:
        this_pct = this_q[this_q.category==cat]["pct_revenue"].iloc[0]
        last_pct = last_q[last_q.category==cat]["pct_revenue"].iloc[0]
        drift[cat] = this_pct - last_pct
    return sorted(drift.items(), key=lambda x: abs(x[1]), reverse=True)

# Output: largest drivers of margin movement, positive or negative
# Example: "LLM Inference +2.4pp" → main driver of 3pp margin compression
```

### Recipe 6 — AWS RI / Savings Plan evaluation

```python
# Reserved Instances (RI) or Savings Plans typically save 30-60% on compute
def ri_vs_on_demand_breakeven(on_demand_monthly, ri_upfront, ri_monthly_discount_pct):
    """
    on_demand_monthly: current monthly spend
    ri_upfront: 1-yr or 3-yr upfront cost
    ri_monthly_discount_pct: e.g., 0.30 = 30% discount on the on-demand rate
    """
    monthly_savings = on_demand_monthly * ri_monthly_discount_pct
    payback_months = ri_upfront / monthly_savings
    return {
      "monthly_savings": monthly_savings,
      "payback_months": payback_months,
      "annualized_savings": monthly_savings * 12,
    }

# Example: 1-yr RI commit at $50K upfront on $18K/mo workload
result = ri_vs_on_demand_breakeven(18_500, 50_000, 0.35)
print(result)
# {monthly_savings: 6475, payback_months: 7.7, annualized_savings: 77,700}
```

Decision rule: commit only if confident usage will continue 90%+ for the commitment term.

### Recipe 7 — LLM inference optimization checklist

```markdown
LLM COST OPTIMIZATION

1. Model selection
   [ ] Use cheaper model for non-critical paths (Haiku vs Sonnet vs Opus)
   [ ] Prompt caching enabled (90% discount on cached tokens — Anthropic)
   [ ] Batch API for non-realtime (50% discount — Anthropic / OpenAI)

2. Prompt engineering
   [ ] Token-count audit: are prompts unnecessarily verbose?
   [ ] Few-shot vs zero-shot tradeoff
   [ ] System prompts properly factored (cache hits)
   [ ] Output token caps appropriate

3. Architecture
   [ ] RAG: chunk size optimized
   [ ] Embedding cache for repeated content
   [ ] Re-ranker only when needed (vs always)

4. Volume controls
   [ ] User-tier rate limits enforced
   [ ] Free-tier daily caps
   [ ] Cost-per-user dashboards
```

### Recipe 8 — Payment processing fee analysis

```python
def stripe_processing_fee_analysis():
    txns = stripe.charges.list(created__gte="2026-06-01", created__lte="2026-06-30")
    by_card = pd.DataFrame([{
      "card_type": t.payment_method_details.card.brand if t.payment_method_details else "?",
      "country": t.billing_details.address.country,
      "amount": t.amount / 100,
      "fee": t.balance_transaction.fee / 100
    } for t in txns])

    # Effective fee rate by segment
    by_card.groupby(["card_type","country"]).apply(
      lambda g: g.fee.sum() / g.amount.sum()
    ).sort_values(ascending=False)

# Levers:
# - Negotiate Stripe Interchange Plus pricing at $1M+ TPV (lower than 2.9%+30¢ flat)
# - ACH for B2B large invoices (0.8% capped at $5)
# - Wire for enterprise (flat fee)
# - Encourage card-on-file vs invoice (reduces dispute risk)
```

### Recipe 9 — Support cost per customer

```python
def support_cost_per_customer():
    fully_loaded_support = sum(employee.loaded_cost for employee in employees if employee.function == "Support")
    customer_count = stripe.customers.list().count
    return fully_loaded_support / customer_count

# Lever check:
# Self-service docs improvement → typical 20-30% ticket reduction
# Tier-gating premium support → lifts support cost out of low-tier COGS
# AI deflection (chatbot, search) → 15-25% deflection benchmark in 2026
```

### Recipe 10 — Margin improvement plan template

```markdown
GROSS MARGIN IMPROVEMENT PLAN — FY27

CURRENT STATE
- Gross margin: 72.5% (vs 78.0% prior year)
- Drivers of decline:
  - LLM inference: +3.5pp (new AI features launched, no pricing change)
  - Hosting: +1.0pp (over-provisioned compute for traffic spike)
  - Support: +1.0pp (3 senior support hires for enterprise)

TARGET: 78.0% by end of FY27 (recover prior baseline)

LEVERS + EXPECTED IMPACT

Lever 1: LLM cost optimization (target: -2.0pp)
- Migrate non-critical paths from Sonnet → Haiku: ~-1.0pp
- Enable prompt caching (90% off cached tokens): ~-0.5pp
- Batch API for analytics workloads: ~-0.5pp
- Owner: VP Eng | Due: Q1

Lever 2: AWS commitment (target: -1.0pp)
- 1-yr Compute Savings Plan: ~35% discount on $220K/yr workload = $77K savings
- Auto-scaling tightening: ~-0.5pp
- Owner: VP Infra | Due: Q1

Lever 3: Support efficiency (target: -1.0pp)
- Self-service docs investment + AI deflection: ~20% ticket reduction
- Tier-gated premium support: shifts $30K/yr from COGS to OPEX (R&D)
- Owner: Head of Support | Due: Q2

Lever 4: Pricing review (target: -1.5pp)
- 8% list price increase on Pro tier (effective for new customers Q3)
- Pass-through pricing on LLM-heavy features (new AI add-on tier)
- Owner: VP Product | Due: Q3

TOTAL TARGETED IMPROVEMENT: 5.5pp → 78% target

TRACKING CADENCE
- Monthly: gross margin per close + driver decomposition
- Quarterly: lever progress review with owners
```

## Examples

### Example 1: Margin dropped 4pp QoQ — diagnose

**Goal:** Gross margin moved from 76% → 72%; identify cause.

**Steps:**

1. Recipe 4 → COGS decomposition this Q vs last Q.
2. Recipe 5 → drift analysis:
   - LLM inference: +2.8pp (largest driver)
   - Hosting: +0.6pp
   - Payment fees: +0.4pp
   - Support: +0.3pp (minor)
3. Investigate LLM inference jump:
   - New AI feature launched mid-Q, no pricing.
   - Per-user inference cost ~$8/mo vs ~$1/mo prior.
   - 80% of new feature usage from existing customers (no incremental revenue).
4. Surface options:
   - Add AI tier ($15/mo add-on); estimated 30% attach rate at scale → recoups ~1.5pp.
   - Migrate to Haiku for analytics paths → ~1.0pp.
   - Prompt caching → ~0.5pp.
5. Recipe 10 → margin improvement plan.

**Result:** Diagnosis surfaces specific cause + concrete recovery plan.

### Example 2: AWS RI commit decision for steady workload

**Goal:** $220K/yr AWS compute steady-state; evaluate 1-yr vs 3-yr commit.

**Steps:**

1. Pull AWS spend by service (Recipe 1) for trailing 12mo → confirm steady.
2. AWS Cost Explorer Recommendations → 1-yr No Upfront Compute Savings Plan: 32% discount; 3-yr: 52% discount.
3. Recipe 6 → 1-yr: $70K/yr savings, payback ~immediate (no upfront).
4. Recipe 6 → 3-yr: $114K/yr savings, but locks in capacity for 3 years.
5. Risk: if business changes (acquisition, migration to GCP), 3-yr commit costs.
6. Recommend: 1-yr commit on baseline (covers 80% of capacity); pay on-demand for the 20% spike.
7. Surface to founder + VP Eng for approval; execute via AWS console.

**Result:** $56K/yr savings (~0.3pp margin improvement) with flexibility preserved.

## Edge cases / gotchas

- **COGS allocation purity:** if Support staff also does sales (e.g., expansion), allocate; don't put 100% in COGS.
- **CS team allocation:** customer success retention work = COGS; expansion work = S&M. Typical 50/50 split.
- **Capitalized software development:** if you capitalize R&D under ASC 350-40, amortization is COGS. Most early-stage don't capitalize.
- **Free-tier costs:** are these COGS? Yes if they support paying users' free trials; allocate proportional.
- **AI inference passthrough:** if customer is paying for AI usage, the cost is COGS. If you eat the cost, also COGS. Either way COGS — but pricing matters more.
- **Marketplace fees:** AWS Marketplace, App Store fees are COGS (cost of delivery), not S&M.
- **Stripe fees on annual prepay:** the full fee hits when you collect, but you recognize revenue ratably. Net effect: COGS spike in collection month vs revenue recognition month. Pre-amortize Stripe fees in models.
- **GPU compute volatility:** AI workloads on GPUs are pricier than CPU; track separately.
- **Reserved Instance lock-in:** if you commit to 3-yr RI and workload changes, you eat the cost. Use sparingly until usage is provably stable.
- **Inference batching trade-off:** batch API is 50% off but latency is high (24hr typical). Doesn't work for user-facing real-time.
- **Discount tier negotiations:** AWS Enterprise Discount Program (EDP) at $1M+/yr commit; Stripe Interchange Plus pricing at $1M+ TPV. Don't leave on the table.
- **Multi-cloud cost:** if you split AWS + GCP, fixed costs duplicate. Often cheaper to consolidate.
- **Inference cost forecasting:** as products mature, per-user inference goes up (more features use AI). Forecast 20-40% growth/yr per-user, not flat.

## Sources

- Eagle Rock 2026 SaaS metrics: https://www.eaglerockcfo.com/blog/research/saas-finance-metrics-benchmarks
- Bessemer Atlas — scaling: https://www.bessemerventures.com/atlas/scaling-to-100-million
- AWS billing API: https://aws.amazon.com/billing/api/
- AWS Cost Explorer: https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html
- Anthropic usage API: https://docs.anthropic.com/en/api/usage
- OpenAI usage API: https://platform.openai.com/docs/api-reference/usage
- Stripe pricing: https://stripe.com/pricing
- Prompt caching (Anthropic): https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching

## Related skills

- `vendor-procurement-saas-spend-audit` — broader spend audit including OPEX
- `unit-economics-saas-metrics` — gross margin is core unit-econ metric
- `xero-quickbooks-bookkeeping` — pulls revenue + COGS from GL
- `causal-mosaic-financial-modeling` — margin scenarios in 3-statement model
