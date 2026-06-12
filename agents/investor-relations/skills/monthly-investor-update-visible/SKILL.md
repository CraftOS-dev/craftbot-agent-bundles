<!--
Source: https://visible.vc/templates/the-visible-standard-investor-update-template/
Source: https://visible.vc/product/updates/
Source: https://visible.vc/blog/the-best-investor-update-templates/
Source: https://visible.vc/blog/quarterly-investor-update/
Source: https://carta.com/learn/cap-table/investor-relations/
Reference role.md: "Monthly investor update playbook"
Round 2 enrichment: full Visible.vc Standard verbatim + cadence calendar + cap-table comm variant + send-via-API recipe + analytics interpretation.
-->

# Monthly investor update — Visible.vc Standard

Drafts and distributes the monthly investor update at the 2026 private-company SOTA bar via the Visible.vc Standard template (or fallback gmail-mcp blast when no investor-platform subscription). Designed for pre-seed through Series A active-raise; quarterly variant for steady-state Series B+. Also handles cap-table communications (new round / secondary / employee tender / cleanup) using the same scaffold with a cap-table-specific TL;DR.

## When to use

- Drafting the monthly (or quarterly) investor update for a private company.
- Sending cap-table communications to existing investors after a round closes, secondary, or material event.
- Drafting AngelList Updates content (Visible.vc Standard maps cleanly).
- Trigger phrases: "monthly update", "investor update", "Visible.vc update", "investor letter monthly", "cap-table comm", "secondary letter".

NOT for: public-company quarterly earnings press release (use `quarterly-earnings-press-release`); board package financial slides (use `finance-agent`'s `board-cfo-financial-package`); LP reporting (use `fund-of-funds-lp-reporting`).

## Setup

```bash
# Visible.vc API (preferred — free Starter tier supports up to 100 investors)
export VISIBLE_API_KEY="<from Visible Settings -> API>"

# Alt platforms (recipient supplies one)
export ANGELLIST_API_KEY="<from AngelList Stack -> API>"
export CARTA_API_KEY="<from Carta Admin -> Developer>"

# Fallback: gmail blast (gmail-mcp BCC; segment by Visible.vc CRM tag)
# Fallback: Foundersuite investor CRM (https://www.foundersuite.com/)
```

Auth / API key requirements:
- `VISIBLE_API_KEY` — Visible Standard plan $79/mo+ unlocks REST; Starter tier UI-only (still free).
- `CARTA_API_KEY` — cap-table-of-record export for dilution math; free for issuers using Carta.
- `GMAIL_*` — gmail-mcp OAuth (free) for BCC blast fallback.

Data inputs:
- Last update (`docx` or Visible.vc Stream) for tone continuity.
- `finance-agent`'s last close: revenue / ARR / cash / runway / burn (mandatory in TL;DR).
- 30 days of operational deltas: hires, churn, customer wins, pipeline shifts, product milestones.
- Cap-table snapshot (Carta / Pulley) for cap-table comms variant.

## Visible.vc Standard structure (mandatory)

1. **TL;DR** (3-5 bullets) — lead with **cash + runway** (mandatory).
2. **Key Metrics** — 3-5 KPIs in a table vs prior month + plan + YoY.
3. **Highlights** — 3-5 (customer wins, hires, product milestones).
4. **Lowlights** — 3-5 **mandatory non-empty** (bad news first; empty section = lost credibility).
5. **Asks** — **mandatory non-empty** (intros / talent / advice / customer references).
6. **Financials snapshot** — optional P&L excerpt + commentary.
7. **Looking forward** — 1-2 sentences on next 30 days.
8. **Sign-off** — founder/CEO name.

## Common recipes

### Recipe 1 — Send update via Visible.vc API
```bash
curl -X POST -H "Authorization: Bearer $VISIBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "June 2026 Investor Update — ACME",
    "body_markdown": "...",
    "segment": "all_investors",
    "scheduled_send_at": "2026-07-05T15:00:00Z"
  }' \
  "https://visible.vc/api/v1/updates"
```
Returns `update_id` — keep for analytics pull.

### Recipe 2 — Pull open / click analytics post-send
```bash
curl -H "Authorization: Bearer $VISIBLE_API_KEY" \
  "https://visible.vc/api/v1/updates/$UPDATE_ID/analytics"
```
Interpret: investors who haven't opened by T+5 days = candidates for personal nudge from CEO (especially lead investor). Open rate <60% = subject line too cold; rewrite next month.

### Recipe 3 — Investor segmentation pull
```bash
curl -H "Authorization: Bearer $VISIBLE_API_KEY" \
  "https://visible.vc/api/v1/contacts?segment=lead_investor"
```
Standard tags to maintain: `lead_investor`, `pro_rata_holder`, `observer`, `angel`, `champion_advisor`.

### Recipe 4 — Gmail BCC fallback (no Visible.vc)
```bash
# via gmail-mcp
mcp call gmail-mcp send_email \
  --to "ir@company.com" \
  --bcc "$(cat investor_list.txt | paste -sd, -)" \
  --subject "June 2026 Investor Update" \
  --html "$(cat update.html)"
```
Always `--bcc` (never `--to` or `--cc`) — full visibility leaks the cap table.

### Recipe 5 — Cap-table snapshot pull (Carta)
```bash
curl -H "Authorization: Bearer $CARTA_API_KEY" \
  "https://api.carta.com/v1/firms/$ISSUER_ID/cap_table?as_of=$DATE"
```
Use for cap-table-comm variant — render dilution table inline (preferred holders, common, options pool).

### Recipe 6 — Round-close cap-table comm draft
```python
# Pattern for round-close letter
template = """
TL;DR: We closed our {round} at ${pre_money:,.0f}M pre / ${post_money:,.0f}M post,
${raised:,.0f}M new capital. Existing pro-rata holders: {pro_rata_exercised_pct}% exercised.
Post-money cap table attached. {runway_extension_months} additional months of runway.
"""
```

### Recipe 7 — Secondary tender comm
```python
# Pattern for employee/founder tender
# Reg FD treatment: if private co, no Reg FD, but still respect material-info handling.
# Disclose: bid price, eligibility, mechanics, deadline. NEVER post-fact (per Carta IR best practice).
```

### Recipe 8 — Schedule recurring monthly send
```bash
# Visible.vc recurring schedule
curl -X POST -H "Authorization: Bearer $VISIBLE_API_KEY" \
  -d '{"cadence": "monthly", "day_of_month": 5, "time": "10:00:00", "timezone": "America/New_York"}' \
  "https://visible.vc/api/v1/schedules"
```

### Recipe 9 — Pull last-month analytics into draft
```python
# Auto-include open rate of last update in this month's note
import requests, os
last = requests.get(f"https://visible.vc/api/v1/updates/last",
                    headers={"Authorization": f"Bearer {os.environ['VISIBLE_API_KEY']}"}).json()
open_rate = last["analytics"]["unique_opens"] / last["analytics"]["delivered"]
# If open_rate < 0.60: rewrite subject line, add hook in first 8 words
```

## Examples

### Example 1: Series A monthly update (steady-state)

**Goal:** June 2026 monthly update; 47 investors on cap table; cash $8.2M; runway 14 months.

**Steps:**
1. Pull metrics from `finance-agent`: ARR $4.2M (+8% MoM), cash $8.2M, burn $580K/mo, runway 14.1 mo.
2. Draft TL;DR (lead with runway): "Strong June: ARR +8% to $4.2M, cash $8.2M / 14mo runway, signed Acme Corp ($420K ACV)."
3. Build Key Metrics table (vs May / vs Plan / vs YoY).
4. List 3-5 Highlights (Acme close, 3 senior eng hires, NPS 71).
5. **Mandatory** 3-5 Lowlights (churned BetaCo $80K ARR, sales cycle Enterprise +28 days, infra cost overrun).
6. **Mandatory** Asks (3 customer-success leads at $500K+ ACV; intro to Series B leads; senior PM candidate).
7. Looking forward: "Q3 plan: close $1M ACV pipeline; hire VP Eng; start Series B conversations Aug."
8. Send via Recipe 1; pull analytics at T+7 (Recipe 2).

**Result:** Delivered to 47 investors; 78% open rate; 3 lead-investor pro-rata commits surfaced; 1 customer intro within 48 hours.

### Example 2: Cap-table comm — secondary tender

**Goal:** Founders + first 10 employees tendering $4M of common to a new lead at Series B mark.

**Steps:**
1. Pull cap-table snapshot (Recipe 5).
2. Draft TL;DR: "Secondary tender opened: $4M of common @ $X.XX/share (Series B FMV). Founders + first 10 employees eligible. Wires by July 31. Post-tender cap table attached."
3. Include mechanics: who, how much, deadline, tax-treatment note (advise tax counsel).
4. Distribute to **all** investors (Reg FD not in scope for private, but transparency norms apply).
5. NEVER post-fact — must precede the tender close.

**Result:** No surprised investors; signal of investor demand at SerB mark; clean comms.

## Edge cases / gotchas

- **Empty lowlights = refuse to send.** Investors smell hiding; credibility ratchets down permanently. If month was actually clean, write the trade-off (e.g., "we deprioritized X to ship Y").
- **Empty asks = close-the-loop signal.** Investors stop helping when you stop asking; never leave empty.
- **Tone shift period-over-period without naming why.** If June was bullish and July is sober, name it in TL;DR: "Tone this month is more measured because pipeline slipped 12%."
- **Quiet period overlap (if a sister bundle has public co).** Public-co quiet period = REFUSE + route to counsel + use `quiet-period-mgmt` skill. Private cos are not under Reg FD but still apply norms during M&A diligence.
- **Gmail BCC leak risk.** Never use `--to` or `--cc` for investor lists. One `--to` slip leaks the entire cap table.
- **Visible.vc free tier limits.** Starter = 100 investors max; Standard $79/mo = unlimited + analytics + API. Upgrade triggers at ~80 investors.
- **Cap-table comm timing.** Carta IR best practice: comm precedes close, not follows. Post-fact comms get punished.
- **AngelList Stack integration.** If on AngelList Stack, AngelList Updates is the default channel — Visible.vc Standard template still applies.
- **Visible.vc subject-line throttle.** Subject lines >80 chars get truncated in Gmail preview pane; aim 50-65.
- **Analytics interpretation pitfall.** Apple Mail Privacy Protection inflates open rate ~25%; weight click rate higher.

> Mandatory disclaimer: This skill drafts comms for private-company investor updates. **Consult licensed securities counsel** for any binding disclosure obligations (notably Rule 506(b) ongoing-disclosure for accredited investors, Rule 506(c) general-solicitation review, or Form D updates).

## Sources

- Visible.vc Standard template: https://visible.vc/templates/the-visible-standard-investor-update-template/
- Visible.vc Updates product: https://visible.vc/product/updates/
- Visible.vc Best Templates 2026: https://visible.vc/blog/the-best-investor-update-templates/
- Visible.vc Quarterly Update guide: https://visible.vc/blog/quarterly-investor-update/
- Carta IR / cap-table comms: https://carta.com/learn/cap-table/investor-relations/
- AngelList Stack Updates: https://www.angellist.com/stack
- Foundersuite investor CRM: https://www.foundersuite.com/
- See `role.md` -> "Monthly investor update playbook"

## Related skills

- `quarterly-board-letter` — denser quarterly format for institutional cadence.
- `fund-of-funds-lp-reporting` — when the audience is LPs, not equity investors.
- `quiet-period-mgmt` — refuse + route during public-co quiet period.
- `quarterly-earnings-press-release` — public-co counterpart.
