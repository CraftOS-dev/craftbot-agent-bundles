<!--
Sources: https://www.spendhound.com/blog/best-saas-spend-management-software
         https://www.spendhound.com/blog/vendr-alternatives
         https://www.tropicapp.io/compare/spendflo
TCO matrix; build-vs-buy; BATNA playbook; counter-letter templates.
Vendr 130K+ deals; Tropic $18B+ benchmark depth.
-->
# Vendor Evaluation + Negotiation — SKILL

Build a vendor evaluation TCO matrix, run a build-vs-buy decision, model 3-year ownership cost, and execute a structured negotiation playbook with BATNA + counter-letter templates. Pulls benchmark data from Vendr / Tropic / Spendflo when recipient has access; otherwise leans on the DIY playbook.

## When to use

- Evaluating 2-5 vendors for a new SaaS / tool / service.
- "Should we build or buy?" decision.
- Annual renewal negotiation (especially 90-day pre-renewal window).
- Mid-contract escalation or true-up dispute.
- Trigger phrases: "vendor evaluation", "TCO", "build vs buy", "RFP", "counter letter", "negotiation", "BATNA", "renewal", "price increase".

## Setup

```bash
export VENDR_API_KEY="xxx"           # https://www.vendr.com — managed buying; paid
export TROPIC_TOKEN="xxx"            # https://www.tropicapp.io — paid
export SPENDFLO_TOKEN="xxx"          # https://spendflo.com — paid
export SPENDHOUND_TOKEN="xxx"        # https://www.spendhound.com — free tier exists
```

## Common recipes

### Recipe 1: TCO matrix template (xlsx skill)
```
| Dimension                       | Option A | Option B | Option C | Build |
|---------------------------------|----------|----------|----------|-------|
| License (3-yr)                  |          |          |          | $0    |
| Implementation (one-time)       |          |          |          |       |
| Internal eng/ops time (months)  |          |          |          |       |
| Training (1x + ongoing)         |          |          |          |       |
| Integration build               |          |          |          |       |
| Ongoing maintenance             |          |          |          |       |
| Opportunity cost                |          |          |          |       |
| Security/compliance review      |          |          |          |       |
| Switching cost (if leaving)     |          |          |          |       |
| ----------------------------    |----------|----------|----------|-------|
| 3-Year TCO                      |          |          |          |       |
| Time-to-value (weeks)           |          |          |          |       |
| Lock-in risk (Low/Med/High)     |          |          |          |       |
| Roadmap fit                     |          |          |          |       |
```

### Recipe 2: Spolsky build-vs-buy (Strategy Letter V)
```python
def build_vs_buy(item):
    """
    Build if: it's a CORE differentiator and we have the talent + ops cycles.
    Buy if: it's CONTEXT (table-stakes that doesn't differentiate us).
    """
    if item['is_core_differentiator'] and item['have_eng_capacity']:
        return 'BUILD'
    if item['vendor_lock_in_risk'] == 'high' and item['easy_to_build']:
        return 'BUILD-LATER, BUY-NOW'
    return 'BUY'

# Examples:
# CRM → BUY (context for most cos)
# Pricing-engine for a SaaS product → BUILD (core)
# Identity (SSO/MFA) → BUY (context AND specialized expertise)
# Custom workflow tool for unique internal process → BUILD if core, BUY (Retool/ToolJet) otherwise
```

### Recipe 3: Vendr benchmark pull
```bash
curl -s "https://api.vendr.com/v1/benchmarks" \
  -H "Authorization: Bearer $VENDR_API_KEY" \
  --data-urlencode "vendor=hubspot" \
  --data-urlencode "tier=Marketing Hub Professional" \
  --data-urlencode "company_size=100-249" \
  | jq '{median, p25, p75, sample_size, last_updated}'
```

### Recipe 4: 90-day renewal calendar event + counter-letter draft
```bash
# Trigger 90 days pre-renewal via google-calendar-mcp
curl -s -X POST "https://www.googleapis.com/calendar/v3/calendars/<cal>/events" \
  -H "Authorization: Bearer $GCAL_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "summary":"[90D] Vendor renewal: <vendor>",
    "description":"Pull benchmark (Recipe 3). Draft counter (Recipe 5). Notify champion.",
    "start":{"date":"2026-09-01"},
    "end":{"date":"2026-09-01"}
  }'
```

### Recipe 5: Counter-letter template
```markdown
Subject: <Vendor> renewal — proposed 2026-2028 terms

Hi <AE>,

Thanks for sending over the renewal proposal. We're committed to staying with <Vendor> and have appreciated <2-3 specific things>.

That said, the proposed pricing is higher than our benchmarks and our budget. Here is the structure we're prepared to sign on:

**Term:** 36 months, locked.
**Pricing:** $<X>/yr — flat across all 3 years (vs proposed $<Y>).
**Seats:** <N> with the option to true-up at $<unit price> mid-year, no haircut.
**Auto-renewal:** removed; we will reaffirm 90 days before each term end.
**Price-protection clause:** any uplift > 5% triggers our right to terminate 60 days written notice.
**MSA changes we need:**
  - DPA + SCC current as of June 2026.
  - SOC 2 Type II annual delivery.
  - Notice of material sub-processor changes 30 days ahead.
  - Service-credit SLA: 99.9% monthly, 10% credit at 99.5%, 25% credit at 99%.

For context, market median for our tier and seat count per Vendr/Tropic benchmarks is $<benchmark>. We are working two alternatives in parallel; the decision is on me by <date>.

Happy to hop on a 20-min to align — what does next week look like?

— <Name>, Head of <Function>
```

### Recipe 6: BATNA matrix
```yaml
batna:
  primary_alternative:
    name: "Competitor X"
    cost_USD: 38000
    feature_gap: "Missing native Snowflake connector — 2 wk eng build"
    switching_cost_USD: 15000
    time_to_switch_weeks: 6
  secondary_alternative:
    name: "In-house OSS stack (n8n + Postgres)"
    cost_USD: 8000
    feature_gap: "No SLA, eng on-call"
    switching_cost_USD: 30000
    time_to_switch_weeks: 12
  walk_away_threshold_USD: 55000   # max we will pay current vendor
  ideal_landing_USD: 42000
```

### Recipe 7: Multi-vendor RFP scorecard (xlsx skill)
```
| Criterion (weight)                | Vendor A | Vendor B | Vendor C |
|-----------------------------------|----------|----------|----------|
| Feature parity (20%)              | 4        | 5        | 3        |
| Cost (20%)                        | 5        | 3        | 4        |
| Security posture (15%)            | 5        | 4        | 3        |
| Implementation speed (10%)        | 3        | 4        | 5        |
| Integration ecosystem (10%)       | 5        | 5        | 3        |
| Roadmap alignment (10%)           | 4        | 3        | 4        |
| Reference checks (5%)             | 4        | 4        | 3        |
| Lock-in risk inverse (5%)         | 3        | 4        | 5        |
| Total CSAT trend (5%)             | 4        | 4        | 3        |
| ---------------                   |          |          |          |
| Weighted total                    |          |          |          |
```

### Recipe 8: Reference call playbook
```markdown
**Setup:** Ask vendor for 3 references in roughly your industry + size. Pick the one they don't suggest first (less coached).

**Questions (15 min):**
1. How long have you been with <vendor>? Pricing tier?
2. What problem were you solving? Did they solve it?
3. What's their support quality like? Response times for P1?
4. Onboarding — how long did it actually take vs promised?
5. Any surprise costs after the initial quote?
6. If you had to do it again, what would you ask for in the contract?
7. What's a feature that's missing?
8. Roadmap promises kept vs missed?
9. How is their billing team / renewal process?
10. Who else did you evaluate, and why did <vendor> win?
```

### Recipe 9: Multi-year discount math (Python)
```python
def multi_year_offer(annual_list_USD, years, discount_pct):
    yr_price = annual_list_USD * (1 - discount_pct/100)
    total = yr_price * years
    savings = annual_list_USD * years - total
    return {'per_year_USD': yr_price, 'total_USD': total, 'savings_USD': savings}

# Standard SaaS multi-year discount ranges (Vendr benchmark):
# 1 year: 0-5% (auto-renewal only)
# 2 year: 8-12% (one true-up window)
# 3 year: 12-18% (locked, no escalator)
print(multi_year_offer(50000, 3, 15))
```

### Recipe 10: Negotiation timing playbook
```markdown
**Best times to negotiate:**
- Vendor end-of-quarter (last 2 weeks of Mar / Jun / Sep / Dec) — AE quota pressure
- 90 days pre-renewal — you have leverage (you can leave)
- After a new round of yours / theirs (you get budget; they sense growth)
- After an outage or material miss (service credits + concessions on table)

**Worst times:**
- Day-of renewal (no leverage, default to auto-uplift)
- Right after fundraising announcement (they think you're flush)
- Q1 their fiscal year start (no quota urgency)
```

## Examples

### Example 1: New CRM evaluation
**Goal:** Pick CRM for 50-person SaaS in 3 weeks.
**Steps:**
1. Recipe 2: confirm BUY (CRM is context, not core).
2. Recipe 7: weighted scorecard across HubSpot vs Salesforce Starter vs Pipedrive.
3. Recipe 3 + 6: Vendr benchmarks; build BATNA.
4. Recipe 8: 2 reference calls each.
5. Recipe 1: 3-year TCO including implementation + RevOps hire.
6. Recipe 5: counter-letter for final two.
7. Decision memo to founder; signed by Friday.

**Result:** Documented choice, market-priced, with renewal trigger calendar already set.

### Example 2: Renewal negotiation on key vendor
**Goal:** Hold annual price flat on a $200k/yr vendor.
**Steps:**
1. Recipe 4: 90-day calendar fires.
2. Recipe 3: pull market benchmark (Vendr or peer founder Slack).
3. Recipe 6: BATNA — explore Competitor X seriously enough that vendor knows.
4. Recipe 5: counter letter.
5. Recipe 9: offer 3-year @ 15% discount for term lock + no auto-renew + price-protection.
6. Recipe 10: time call to last 2 weeks of vendor's quarter.

**Result:** Flat pricing or better; auto-renewal removed; SOC 2 delivery codified.

## Edge cases / gotchas

- **Auto-renewal trap.** Many MSAs auto-renew 30-60 days before term end with 5-15% uplift. Recipe 4 calendar must fire ≥ 90 days out.
- **MFN clauses.** "Most Favored Nation" pricing language is gold; most enterprise vendors will give it under multi-year lock.
- **Termination for convenience.** Different from termination for cause. Most vendors won't give either; aim for termination on material price increase > X%.
- **Procurement red flags.** Verbal-only concessions, "we never put that in writing," NDA prerequisites to see benchmarks.
- **Vendor-financed deals (Vendr/Tropic managed).** They take 5-10% of savings or flat fee. Worth it on $50k+ deals; not worth on < $20k.
- **Build-then-buy regret.** Building a CRM / ATS / payroll system is almost always a mistake (CONTEXT items). **Defer to `legal-counsel` for any "build" decisions involving regulated data — wage data, PII, PHI.**
- **MSA red-line resource.** Don't redline an MSA in 24 hours. Allow 2-3 weeks for procurement + legal cycle. Standard turns: DPA → SCCs → Limitation of liability cap → IP indemnification → service-credit SLA → sub-processor notice.
- **3-year lock without escalator clause.** Vendor's biggest concession; insist on flat pricing across all 3 years (no CPI-based annual uplift).
- **Service-credit SLA math.** Standard: 99.9% monthly = 43 min downtime; 99.5% = 3.6h; credits cap at 25% monthly fee. Push for stronger credits, not stronger uptime promises.
- **Defer to `legal-counsel` for binding MSA / DPA / SCCs language and limitation-of-liability caps.**

## Sources

- SpendHound — Best SaaS Spend Management 2026: https://www.spendhound.com/blog/best-saas-spend-management-software
- SpendHound — Vendr Alternatives: https://www.spendhound.com/blog/vendr-alternatives
- Tropic vs Spendflo: https://www.tropicapp.io/compare/spendflo
- Joel Spolsky — Strategy Letter V: https://www.joelonsoftware.com/2002/06/12/strategy-letter-v/
- Vendr — pricing data: https://www.vendr.com/buyer-guides
- Spendflo: https://spendflo.com/
