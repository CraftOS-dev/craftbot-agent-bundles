<!--
Source: https://visible.vc/templates/the-visible-standard-investor-update-template/
Source: https://carta.com/learn/private-funds/management/portfolio-management/investor-updates/
Reference role.md: "Investor update playbook"
-->

# Investor update — monthly / quarterly cadence

Standard investor update format using Visible.vc Standard template: header → metrics → highlights → lowlights → asks → financials → thanks. Cadence varies by stage. Conservative numbers; mandatory lowlights + asks.

## When to use

- Monthly investor updates during active raise or steady-state for early-stage.
- Quarterly updates for established companies or all-investor pack.
- Board pack (extended version of investor update).
- Quarterly + annual prep for institutional investors.
- Crisis updates (off-cadence): rare events requiring transparency.
- Trigger phrases: "investor update", "monthly update", "investor report", "board pack", "Visible".

NOT for: regulatory filings (defer to `legal-counsel`); customer/press updates (use marketing).

## Cadence by stage / situation

| Stage / situation | Cadence | Audience |
|---|---|---|
| Active raise | Monthly (or bi-weekly during close) | All investors + warm leads |
| Pre-seed / Seed (post-raise) | Monthly | All investors |
| Series A | Monthly to lead, quarterly to all | Lead + others |
| Series B+ | Monthly board pack, quarterly all-investor | Board + others |
| Post-IPO track | Quarterly aligned with audit | Board + select investors |
| Crisis | Off-cadence as needed | Lead only initially; expanded after stabilized |

## Visible.vc Standard template (the format)

```markdown
SUBJECT: [Company Name] — [Month YYYY] Update

TL;DR (3-5 lines, lead with cash + biggest win)
- [Cash position + runway one-liner]
- [Biggest revenue / growth metric movement]
- [Biggest product / customer milestone]
- [One ask or one challenge teaser]

KEY METRICS
- Cash on hand: $X | Runway: Y months | Net burn: $Z/mo
- ARR: $X (±% MoM) | MRR: $Y | NRR: Z%
- New logos: X | Logo churn: Y | Net new ARR: $Z
- Headcount: X (start) | hires: Y | departures: Z
- [Optional: NPS, top customer logos won, pipeline coverage]

HIGHLIGHTS (3-5 bullets, quantified)
- [Win 1 — quantified outcome]
- [Win 2]
- [Win 3]

LOWLIGHTS (3-5 bullets — MANDATORY — never skip)
- [Challenge 1 — what's happening + plan]
- [Challenge 2]
- [Challenge 3]

ASKS (MANDATORY — don't leave empty)
- Intros to [specific personas / companies]
- Help with [specific decision / hire / customer]
- Feedback on [specific question]

FINANCIALS (1-page summary; full pack in data room)
- P&L summary (Revenue / Gross Profit / OpEx / EBITDA)
- Balance Sheet summary (Cash / AR / AP / Deferred Revenue / Equity)
- Cash trend chart (trailing 12 months)

THANKS
- [Personal sign-off]

[Optional appendix: cohort retention, pipeline, headcount detail, product roadmap]
```

## Setup

```bash
# Data sources — already shipped:
# - stripe-mcp / stripe-api for ARR + MRR + retention
# - xero-mcp for P&L + Balance Sheet + Cash Flow
# - mercury-modern-treasury-banking for current cash
# - posthog-mcp / mixpanel-mcp for cohort retention + NRR
# - Carta / Pulley API for headcount + cap table

# Visible.vc API (optional, for distribution + tracking)
export VISIBLE_API_KEY="..."

# Distribution:
# - gmail-mcp (primary)
# - notion-mcp (archive)
```

## Common recipes

### Recipe 1 — Pull metrics for the pack

```python
def monthly_metric_pack(close_month):
    return {
      "cash":     total_cash_now(),  # from runway-burn-analysis Recipe 1
      "runway":   runway_months(),
      "net_burn": net_burn_t3m(),
      "arr":      stripe_arr(),
      "arr_mom":  arr_growth_mom(),
      "mrr":      stripe_arr() / 12,
      "nrr":      cohort_nrr(),
      "new_logos": crm_new_logos_in_month(close_month),
      "churn":    crm_churn_in_month(close_month),
      "headcount_start": hris.headcount_at(close_month.replace(day=1)),
      "headcount_end":   hris.headcount_at(close_month.replace(day=30)),
      "hires":           hris.hires_in_month(close_month),
      "departures":      hris.departures_in_month(close_month),
    }
```

### Recipe 2 — Draft TL;DR (the only thing many investors read)

Template:
```
TL;DR

- ARR $4.2M (+5.2% MoM, +83% YoY); on plan to exit '26 at $5.5M ARR.
- Closed [Customer X] — [strategic significance — e.g., first 7-figure logo].
- Cash $3.4M; runway 16 months at current burn; raising Series A
  starting July; targeting close by Sep.
- Ask: warm intros to GPs leading $8-15M Series A SaaS.
```

Lead with cash if runway < 18 months. Lead with growth if Default-Alive and growth is the story.

### Recipe 3 — Highlights with quantified outcomes

```markdown
HIGHLIGHTS
- Closed Acme Corp ($120K ACV / $480K TCV) — first 6-figure ACV.
- Launched API v2; 8/10 top customers migrated; reduced p99 latency 70%.
- Hired Head of Sales (ex-Series B SaaS exit); pipeline +35% post-hire.
- Customer reference call with [marquee customer] — 30-min recording shareable.
```

Quantify everything. "Big quarter" → "ARR +12% MoM"; "exec hire" → "ex-Series B SaaS, 9 yrs experience".

### Recipe 4 — Lowlights — the MANDATORY honesty section

```markdown
LOWLIGHTS
- Churned 2 customers in May ($14K total ARR) — both downgraded to lower tier
  due to budget compression; not product. Implementing tier-gating to prevent.
- Hosting costs +35% MoM driven by new ML inference cluster; not yet captured
  in pricing. Action: 30-day customer pricing review by [date].
- Senior SWE departure (personal reasons); team coverage in place; backfill
  posting goes live week of [date].
- Pipeline missed plan: 65% of goal. Root cause: 2 deals slipped to next quarter;
  high confidence on close.
```

Investors don't believe "no problems". No lowlights = signal that founder is hiding things. Be specific about plans.

### Recipe 5 — Asks (also mandatory)

```markdown
ASKS
- Intros to [VP Sales / RevOps] at $50M-$500M ARR SaaS companies for our
  customer development calls.
- Connections to enterprise SaaS lead investors (Series A focus, $8-15M rounds).
- Feedback on our pricing tier proposal (attached) before we test with customers.
- Help thinking through 18mo vs 24mo runway decision given Series A timing.
```

Make asks specific. "More intros" is useless; "intros to VP Sales at $50M-$500M ARR SaaS" is actionable.

### Recipe 6 — Generate financial summary

```python
def financial_summary_block(month):
    pnl = xero.reports.profit_and_loss(
      fromDate=f"{month.year}-{month.month:02d}-01",
      toDate=f"{month.year}-{month.month:02d}-{(month + relativedelta(months=1) - relativedelta(days=1)).day:02d}"
    )
    bs = xero.reports.balance_sheet(date=month.last_day)

    return f"""
FINANCIALS

P&L Summary
- Revenue: ${pnl.revenue:,.0f} ({arr_mom:+.1%} MoM)
- Gross Profit: ${pnl.gross_profit:,.0f} ({pnl.gross_margin:.1%} margin)
- OpEx: ${pnl.opex:,.0f}
- EBITDA: ${pnl.ebitda:,.0f}

Balance Sheet Highlights
- Cash: ${bs.cash:,.0f}
- AR: ${bs.ar:,.0f}
- Deferred Revenue: ${bs.deferred_revenue:,.0f}
- Equity: ${bs.equity:,.0f}

Cash Trend (T12M): [chart attached]
"""
```

### Recipe 7 — Cohort retention chart

```python
# Pull cohort retention from PostHog or build from Stripe data
import pandas as pd
def cohort_retention_table(months_back=12):
    # Rows: cohort start month; columns: months since acquisition
    cohorts = posthog.cohort_retention(months=months_back)
    df = pd.DataFrame(cohorts).fillna(0)
    # Format as heatmap-ready CSV for visualization
    df.to_csv("cohort_retention.csv")
    return df
```

Include in board pack (not always in investor update).

### Recipe 8 — Send via Visible.vc API

```bash
curl -X POST https://api.visible.vc/v1/updates \
  -H "Authorization: Bearer $VISIBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Acme Corp — June 2026 Update",
    "content": "<markdown content>",
    "recipients": ["investor1@vc.com", "investor2@vc.com"],
    "schedule_send": "2026-07-05T09:00:00Z"
  }'
```

Visible.vc tracks opens + clicks + comments per investor.

### Recipe 9 — Send via Gmail (backup / lead investors)

```python
# Personalized version for lead investor — same content + custom line
gmail.send(
  to="leadinvestor@vc.com",
  cc="founder@company.com",
  bcc="archive@company.com",
  subject="Acme Corp — June 2026 Update",
  body=template_render(metrics, highlights, lowlights, asks),
  attachments=["financials_pack.pdf", "cap_table_2026-06.pdf"]
)
```

### Recipe 10 — Quarterly board pack expansion

The board pack extends the monthly update with:

```markdown
QUARTERLY BOARD PACK ADDITIONS

1. Strategic Review
   - Progress vs annual plan
   - Pivots / direction changes (if any)

2. Detailed Financials (separate PDF)
   - Full P&L (12 months trailing + projected)
   - Full Balance Sheet
   - Cash Flow (direct + indirect)
   - Variance vs budget commentary
   - Reforecast if material variance

3. Operational Deep-Dive (rotate each quarter)
   - Q1: Product roadmap + technology debt
   - Q2: Sales motion + GTM efficiency
   - Q3: Customer success + churn root cause
   - Q4: People & culture + comp planning

4. Cohort Analysis
   - Retention by cohort
   - LTV:CAC by segment
   - NRR by tier

5. Cap Table + 409A Snapshot
   - Current cap table
   - 409A status + next refresh

6. Open Decisions
   - Items requiring board approval
   - Items for board input

7. Appendices
   - Org chart
   - Customer logos won/lost
   - Press / awards
```

## Examples

### Example 1: Monthly Visible.vc update — Series A startup

**Goal:** Standard monthly update to ~25 investors.

**Steps:**

1. Run Recipe 1 → pull metrics for June 2026.
2. Run Recipe 6 → financial summary.
3. Draft TL;DR (Recipe 2) leading with growth (Default Alive, growth is the story).
4. Compose 4 highlights (Recipe 3) and 3 lowlights (Recipe 4).
5. Define 3 specific asks (Recipe 5).
6. Draft → review with founder → iterate (typically 2-3 rounds).
7. Send via Visible.vc (Recipe 8) at 9am ET Thursday.
8. Lead investor follow-up call scheduled separately for next week.
9. Track open rates per investor; flag any non-opens for personal outreach.

**Result:** 22/25 opens within 48 hours; 4 investors reply with specific intros.

### Example 2: First-time monthly update — solo founder, 6 angels

**Goal:** Build muscle on the update cadence.

**Steps:**

1. Use simple gmail (no Visible.vc yet).
2. Keep to 1-page-equivalent (~400 words).
3. Always include all 6 sections (TL;DR, metrics, highlights, lowlights, asks, financials, thanks).
4. Send last Friday of every month.
5. Track replies in a simple sheet: who replied? what intro provided?
6. After 3 months, switch to Visible.vc if investor count > 10.

**Result:** Established habit; angels regularly send intros and customer leads.

## Edge cases / gotchas

- **Conservative numbers (HARD RULE):** ARR = current invoicing run-rate, not pipeline. Bookings = signed contracts. Pipeline = labeled as pipeline.
- **Net burn from actual, not budget:** runway = current cash / trailing-3-month actual burn. Don't use budgeted burn (always optimistic).
- **No-lowlights = red flag:** investors who get no-problems updates assume founder is hiding things. Build the muscle to share lowlights with a plan.
- **No-asks = closed loop:** "I don't need help" tells investors you don't value their network. Always ask for something specific.
- **Single-source-of-truth metrics:** if you change metric definition mid-year (e.g., recompute NRR), disclose in the update. Investors notice mid-year recasts.
- **Lead investor first:** for major news (round close, key hire, big customer), call lead investor before update goes out.
- **Crisis updates:** off-cadence updates only for material events: lead-investor departure, large customer loss, executive departure, fundraise difficulty. Don't bury bad news in routine updates.
- **Length discipline:** 1 page (max 2). Investors skim; respect their time.
- **Subject line:** "[Company] — [Month YYYY] Update". Standardize so investors auto-file.
- **Attach the data room link** so investors can dig deeper if they want.
- **Pacing:** don't change cadence without telling investors. If you went monthly → quarterly, announce why.
- **Quote sources:** if you reference external benchmarks (Bessemer, etc.) attribute. Investors notice unattributed numbers.
- **Forward-looking statements:** be careful with "we will close $X in Q3". Use "we expect" or "on track to" with disclaimer.

## Sources

- Visible.vc Standard template: https://visible.vc/templates/the-visible-standard-investor-update-template/
- Visible.vc product: https://visible.vc/
- Carta investor updates: https://carta.com/learn/private-funds/management/portfolio-management/investor-updates/
- DocSend (engagement analytics): https://www.docsend.com/
- Foundersuite: https://www.foundersuite.com/
- AngelList Updates (for AL Stack): https://www.angellist.com/

## Related skills

- `unit-economics-saas-metrics` — populates KEY METRICS section
- `runway-burn-analysis` — populates cash/burn/runway in TL;DR
- `monthly-close-procedure` — closes books before update goes out
- `fundraising-data-room` — link to data room in financials section
