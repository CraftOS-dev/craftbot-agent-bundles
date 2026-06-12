<!--
Source: https://visible.vc/blog/investor-update-software/
Investor updates via Visible.vc — monthly default, KPI auto-sync
-->
# Investor Update — Monthly / Quarterly (Visible.vc)

Visible.vc is the de-facto investor-update tool in 2026 — KPI auto-sync from Stripe / Carta / analytics, template-based composition, deliver-once-send-to-many, engagement tracking (opens + time-per-section). Free tier covers solo founders. Format: TL;DR / KPIs / Wins / Lowlights / Asks / Cash + runway. AngelList Stack Updates as free fallback (note: AngelList Stack stops new customers Aug 2026 — current customers grandfathered).

## When to use

- Monthly investor update (default cadence pre-Series B).
- Quarterly investor update (Series B+, with monthly KPI-only ping).
- Year-end recap to investors.
- Pre-fundraise warm-up (3-6 months of consistent updates show momentum).

Trigger phrases: "investor update", "monthly investor", "send investors", "Visible update", "MRR for investors", "investor TL;DR".

## Setup

```bash
# Visible API + auth check
curl -fsSL "https://api.visible.vc/v1/me" \
  -H "Authorization: Bearer $VISIBLE_API_KEY"
```

Auth / API key requirements:
- `VISIBLE_API_KEY` — Visible Settings → API. Free tier API access for basic updates; paid for advanced KPI integrations.
- `STRIPE_API_KEY` — for MRR / churn auto-pull (read-only restricted key recommended).
- `XERO_API_KEY` (or `QUICKBOOKS_API_TOKEN`) — for cash + runway pull.
- `POSTHOG_API_KEY` / `AMPLITUDE_API_KEY` / `MIXPANEL_API_KEY` — for product KPI pull.

## Common recipes

### Recipe 1: Create the monthly update template (one-time setup)

```bash
curl -X POST "https://api.visible.vc/v1/updates/templates" \
  -H "Authorization: Bearer $VISIBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Monthly Investor Update",
    "sections": [
      {"key":"tldr","title":"TL;DR","type":"text"},
      {"key":"metrics","title":"Key Metrics","type":"metrics"},
      {"key":"wins","title":"Wins","type":"text"},
      {"key":"lowlights","title":"Lowlights","type":"text"},
      {"key":"next","title":"What is next (30 days)","type":"text"},
      {"key":"asks","title":"Asks","type":"text"},
      {"key":"cash","title":"Cash + runway","type":"text"}
    ]
  }'
```

### Recipe 2: KPI auto-pull from Stripe (MRR / churn)

```bash
# Pull MRR from Stripe via direct API, then post to Visible KPI
MRR=$(curl -s "https://api.stripe.com/v1/balance" \
  -u "$STRIPE_API_KEY:" \
  | jq '.subscriptions.amount / 100')

curl -X POST "https://api.visible.vc/v1/metrics/values" \
  -H "Authorization: Bearer $VISIBLE_API_KEY" \
  -d "{
    \"metric_id\":\"<mrr-metric-id>\",
    \"value\":$MRR,
    \"date\":\"$(date +%F)\"
  }"
```

### Recipe 3: KPI auto-pull from PostHog (active users)

```bash
WAU=$(curl -s "https://app.posthog.com/api/projects/$PH_PROJECT_ID/insights/<wau-insight-id>" \
  -H "Authorization: Bearer $POSTHOG_API_KEY" \
  | jq '.result[0].count')

curl -X POST "https://api.visible.vc/v1/metrics/values" \
  -H "Authorization: Bearer $VISIBLE_API_KEY" \
  -d "{\"metric_id\":\"<wau-metric-id>\",\"value\":$WAU,\"date\":\"$(date +%F)\"}"
```

### Recipe 4: Cash + runway from Xero

```bash
CASH=$(curl -s "https://api.xero.com/api.xro/2.0/Accounts/<bank-account-id>" \
  -H "Authorization: Bearer $XERO_API_KEY" \
  | jq '.Accounts[0].Balance')

BURN=120000  # monthly burn — pull from FP&A or hardcode if static
RUNWAY=$(echo "$CASH / $BURN" | bc -l | xargs printf "%.0f")

curl -X POST "https://api.visible.vc/v1/metrics/values" \
  -H "Authorization: Bearer $VISIBLE_API_KEY" \
  -d "[
    {\"metric_id\":\"<cash-metric-id>\",\"value\":$CASH,\"date\":\"$(date +%F)\"},
    {\"metric_id\":\"<runway-metric-id>\",\"value\":$RUNWAY,\"date\":\"$(date +%F)\"}
  ]"
```

### Recipe 5: Draft the narrative sections

```markdown
## TL;DR
Strong April. MRR $52k (+8% MoM), driven by enterprise pilot conversions. VP Eng search closing this week.
Lowlight: churn ticked up to 4.2% in SMB. Investigating. Runway extends to 16 months at current burn.

## Wins
- Closed 3 enterprise pilots ($90k ARR combined)
- VP Eng candidate at offer (start May 15)
- Product NPS 52 (+8 from March)

## Lowlights
- SMB churn 4.2% (up from 2.8% in March) — root cause: pricing-to-value gap in low-tier
- Sales pipeline coverage 2.1x (target 3x) — investing in SDR hire

## What is next (30 days)
- Ship pricing v2 (mid-May)
- VP Eng start (May 15)
- Series B prep — banker selection
- Hire SDR (offer out by May 20)

## Asks
- Intros to: CISO at series-A healthcare cos (3 names)
- Advice on: Series B banker selection (current top 3: Goldman / Qatalyst / Lazard)
- Other: Beta testers for pricing v2

## Cash + runway
Current cash: $1.92M
Monthly burn: $120k
Runway: 16 months
Series B target: Q3 2027
```

### Recipe 6: Create the update + send

```bash
UPDATE_ID=$(curl -X POST "https://api.visible.vc/v1/updates" \
  -H "Authorization: Bearer $VISIBLE_API_KEY" \
  -d '{
    "template_id":"<monthly-template-id>",
    "period":"2027-04",
    "sections":{
      "tldr":"...",
      "wins":"...",
      "lowlights":"...",
      "next":"...",
      "asks":"...",
      "cash":"..."
    }
  }' | jq -r '.id')

# Send to investor distribution list
curl -X POST "https://api.visible.vc/v1/updates/$UPDATE_ID/send" \
  -H "Authorization: Bearer $VISIBLE_API_KEY" \
  -d '{"list_id":"<investor-list-id>"}'
```

### Recipe 7: Pull engagement after send (T+7 days)

```bash
curl -fsSL "https://api.visible.vc/v1/updates/$UPDATE_ID/recipients" \
  -H "Authorization: Bearer $VISIBLE_API_KEY" \
| jq '.recipients[] | {name, email, opened, time_on_page, sections_viewed}'
```

Low engagement on lowlights = investor is checked out. Act on this — call them, not email.

### Recipe 8: AngelList Stack fallback (free tier)

```bash
# Note: AngelList Stack stops accepting new customers Aug 2026.
# Existing customers grandfathered. Use Visible for new accounts.
curl -X POST "https://api.angellist.com/stack/v1/updates" \
  -H "Authorization: Bearer $ANGELLIST_TOKEN" \
  -d '{"period":"2027-04","content":"<markdown>"}'
```

### Recipe 9: Notion fallback (no investor SaaS budget)

```bash
mcp tool notion.create_page \
  --parent '{"page_id":"<investor-updates-db>"}' \
  --properties '{
    "Month":{"date":{"start":"2027-04-01"}},
    "Status":{"select":{"name":"Sent"}}
  }' \
  --children-markdown "./apr-2027-investor-update.md"

# Then email manually
mcp tool gmail.send \
  --to "investors@company.com" \
  --subject "April 2027 Investor Update" \
  --html-body "$(cat ./apr-2027-investor-update.md | pandoc -t html)"
```

### Recipe 10: KPI dashboard sync (one-time setup)

```bash
# Sync all dashboards to a central KPI sheet for Visible
mcp tool notion.create_page --parent "<kpi-dashboard-page>" \
  --properties '{"title":[{"text":{"content":"Investor KPI Sheet"}}]}'
# Populate with: MRR, Customers, Churn, NPS, Cash, Runway, North Star
# Visible pulls from sheet → embeds in every update
```

### Recipe 11: Schedule the auto-update cron

```bash
# Run on 1st of month at 9am via CraftBot loop skill
# Pulls metrics, drafts narrative, queues for CEO review
0 9 1 * * /usr/bin/python3 /scripts/monthly-investor-update.py --review-then-send
```

### Recipe 12: Quarterly recap variant

```bash
# Quarterly = monthly format + retrospective + strategy update
curl -X POST "https://api.visible.vc/v1/updates" \
  -H "Authorization: Bearer $VISIBLE_API_KEY" \
  -d '{
    "template_id":"<quarterly-template-id>",
    "period":"2027-Q1",
    "sections":{
      "tldr":"...",
      "metrics":{"include_charts":true},
      "quarter_retrospective":"What we learned",
      "strategy_update":"What is changing",
      "wins":"...",
      "lowlights":"...",
      "next_quarter":"...",
      "asks":"...",
      "cash":"..."
    }
  }'
```

## Examples

### Example 1: Send first investor update post-seed close

**Goal:** Founder closed seed 2 weeks ago. First update next week.

**Steps:**
1. Set up Visible template (Recipe 1).
2. Add investor distribution list (post-seed CCs from term sheet).
3. Run Recipe 2-4 for KPI auto-pull. Verify numbers match dashboards.
4. Draft narrative (Recipe 5). Be honest about being early — investors expect this.
5. Send (Recipe 6).
6. T+7 days: check engagement (Recipe 7).

**Result:** First update sets expectation. Investors know what to expect monthly.

### Example 2: Pre-Series-B warm-up

**Goal:** 6 months before Series B, want investors deeply engaged.

**Steps:**
1. Confirm monthly cadence locked (calendar reminder, Recipe 11).
2. Each update: TL;DR + KPIs + Wins + Lowlights + Asks + Cash + 1 narrative anecdote.
3. Pull engagement monthly (Recipe 7). Investors with high engagement get extra 15-min coffee.
4. Investors with low engagement get personal call within 7 days of send.
5. Last update before fundraise: include "we will be raising in Q3" preview.

**Result:** When you open the round, investors are pre-sold; raise closes faster.

## Edge cases / gotchas

- **Skipping = signal of trouble.** Missing a month after consistent cadence is a red flag. Send even if metrics are bad.
- **Lowlights mandatory.** Updates with no lowlights lose investor trust. They suspect you're hiding something.
- **Asks must be specific.** "Intros to enterprise buyers" is fluff. "Intros to Head of IT at 3 healthcare $1B+ orgs" is an ask.
- **KPI inconsistency = audit.** If MRR in update is different from board pack number, investors notice. Source-of-record discipline matters.
- **Engagement data is for action.** Don't just read it. Low-engagement investors → call them. High-engagement → upgrade their access.
- **Free tier KPI limit.** Visible free tier limits metric integrations. Series A+ should pay for unlimited.
- **AngelList Stack EOL caveat.** Aug 2026 stops new customers. Existing customers grandfathered for now. Migration path: Visible.
- **Tagged metric pulls drift.** Stripe MRR can mismatch GAAP revenue. Document the methodology once in the update footer; refer back.
- **Forward-looking statements are legally sensitive.** Don't say "we will hit $5M ARR by Q4" — say "our plan is to reach $5M ARR by Q4."
- **Pre-IPO companies switch to gated.** When fundraising or pre-IPO, switch to DocSend-protected updates so distribution is auditable.
- **Quarter cadence skipping monthly mid-quarter = bad.** If you switch to quarterly, still send a 1-line monthly KPI ping.

## Sources

- [Visible.vc investor update software](https://visible.vc/blog/investor-update-software/)
- [Visible.vc API docs](https://docs.visible.vc/)
- [AngelList Stack Updates (legacy)](https://stack.angellist.com/)
- [Carta — Best Cap Table Software for 2026](https://carta.com/best-cap-table-software/)
- [Lenny Rachitsky — How to write a great weekly update](https://www.lennysnewsletter.com/p/how-to-write-a-great-weekly-update)
