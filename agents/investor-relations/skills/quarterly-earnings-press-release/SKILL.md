<!--
Source: https://www.notified.com/products/press-release-distribution
Source: https://www.businesswire.com/portal/site/home/ir/
Source: https://www.prnewswire.com/services/financial-disclosure/
Source: https://www.globenewswire.com/
Source: https://www.sec.gov/rules/final/33-8176.htm
Reference role.md: "Earnings press release playbook"
Round 2 enrichment: full press release template + Reg G recon table + Safe Harbor verbatim + wire timing + GAAP-to-non-GAAP builder.
-->

# Quarterly earnings press release (public co)

Drafts the quarterly earnings press release for public companies — headline + summary bullets + CEO/CFO quotes + financial table (this Q + YoY + sequential) + guidance table + conference call info + GAAP-to-non-GAAP Reg G reconciliation + Safe Harbor + boilerplate. Wired via Notified / Business Wire / PR Newswire / Globe Newswire embargoed to T-30 from market close (or T+0 next morning per company convention). Paired with 8-K Item 2.02 simultaneous EDGAR filing.

## When to use

- Drafting the quarterly earnings press release.
- Embargoed wire timing coordination.
- GAAP-to-non-GAAP reconciliation table compilation (Reg G).
- Trigger phrases: "earnings press release", "earnings release", "Q-X press release", "quarterly results release".

NOT for: earnings call script (use `earnings-call-script-qa`); 10-K / 10-Q narrative (use `10k-10q-drafting-workiva`); guidance-number setting (use `guidance-setting`); 8-K filing logistics (use `8k-event-reporting`).

## Setup

```bash
# Wire distribution (per-release pricing $500-$5K)
export NOTIFIED_API_KEY="<from Notified Admin>"
export BUSINESSWIRE_API_KEY="<from BW Portal -> Developer>"
export PR_NEWSWIRE_API_KEY="<from PR Newswire Admin>"
export GLOBE_NEWSWIRE_API_KEY="<from Globe Newswire Admin>"

# Tools: docx for portable draft; sec-edgar-mcp for peer release precedent
```

Auth / API key requirements:
- One wire vendor (recipient picks based on cost + existing contract).
- `WORKIVA_API_KEY` (optional) — for paired 8-K Item 2.02 drafting.
- Free fallback: SEC EDGAR direct 8-K filing + Q4/Notified IR website post; wire vendor is the only paid step (typical contract: $5-$15K/yr for unlimited).

Data inputs:
- `finance-agent` financial close package: revenue (GAAP + organic), EPS (GAAP + adj), segments, cash, capex.
- Consensus snapshot (FactSet / Refinitiv / Yahoo Finance fallback).
- `guidance-setting` output: range / point + rationale.
- Prior 4 quarters' own releases for cadence baseline.
- CEO + CFO quote inputs (often drafted by IR with CEO/CFO edit).

## Standard structure (1500-3000 words)

1. **Headline** — revenue + EPS vs consensus + guidance signal (15-25 words).
2. **Subhead** — 1-line strategic frame (10-20 words).
3. **Summary bullets** — 3-5 bullets (financial + strategic mix).
4. **CEO quote** (40-80 words) — strategic narrative.
5. **CFO quote** (40-80 words) — financial discipline / outlook.
6. **Financial highlights table** — Revenue / Operating Income / Net Income / EPS / Cash; Quarter vs YoY + Sequential.
7. **Segment results** (if multi-segment) — revenue + operating income by segment.
8. **Capital allocation** — buybacks, dividends, M&A, cash position.
9. **Business highlights** (strategic) — 3-5 narrative bullets.
10. **Guidance** — Q+1 + full-year (range or point).
11. **Conference call info** — time + dial-in + webcast URL.
12. **GAAP-to-Non-GAAP reconciliation tables** — Reg G mandatory.
13. **Forward-looking statements / Safe Harbor** — counsel-supplied.
14. **About** boilerplate.
15. **Contact** — IR + media.

## Wire timing

| Path | Embargo Lift | Notes |
|------|--------------|-------|
| After market close | 4:01 PM ET (T+1 min) | Call typically 4:30-5:00 PM ET |
| Pre-market open | 6:00-7:00 AM ET | Call typically 8:00-8:30 AM ET |

- 8-K Item 2.02 filed simultaneously with wire.
- IR website (Q4 / Notified) earnings page goes live within minutes.
- Conference call typically 30-60 min after wire.

## Common recipes

### Recipe 1 — Pull peer release precedent
```bash
for peer in $PEER_TICKERS; do
  mcp call sec-edgar-mcp fetch_form --ticker=$peer --form=8-K --item="2.02" --limit=1
done
```

### Recipe 2 — Headline scaffold
```python
HEADLINE_SCAFFOLD = """
{Company} Reports {Q-N FY} Results: Revenue Up {X}% to ${Y}M;
{Beat/In-line/Miss} Consensus on EPS; {Raised/Reaffirmed/Lowered} Full-Year Guidance
"""
# Keep 15-25 words; lead with biggest number; verify consensus before "beat" claim
```

### Recipe 3 — CEO + CFO quote drafting
```
CEO QUOTE PATTERN:
"<Headline strategic point>. <Specific evidence>. <Forward-looking frame>."
e.g., "Q2 demonstrated the durability of our platform momentum. ARR grew 28%
to $X billion and we added Y net new $1M+ ACV customers. We're entering the
back half with our strongest enterprise pipeline ever."

CFO QUOTE PATTERN:
"<Financial discipline anchor>. <Margin or efficiency proof>. <Capital allocation>."
e.g., "We continued to drive disciplined growth this quarter. Operating margin
expanded 200 bps to 24%, free cash flow margin reached 28%, and we returned
$X to shareholders through buybacks while investing in R&D."
```

### Recipe 4 — Reg G non-GAAP reconciliation table
```python
# Mandatory: equal-or-greater-prominence rule for GAAP
import pandas as pd

recon = pd.DataFrame({
    "GAAP Net Income": [120],
    "+ Stock-based comp": [40],
    "+ Restructuring": [8],
    "+ Acquisition-related amortization": [12],
    "+ Income tax effects": [(40 + 8 + 12) * 0.21 * -1],
    "= Non-GAAP Net Income": [None]  # compute
})
recon.iloc[0, -1] = recon.iloc[0, :-1].sum()
# Disclose with each non-GAAP measure used; counsel reviews
```

### Recipe 5 — Safe Harbor + Forward-looking statements (counsel-supplied)
```
This press release contains forward-looking statements within the meaning of the
Private Securities Litigation Reform Act of 1995. These forward-looking statements
include, but are not limited to, statements regarding our [revenue, margin, EPS]
guidance, expected impact of [strategic initiative], and [other forward-looking
statements]. These statements involve risks and uncertainties, and actual results
could differ materially. Factors that could cause actual results to differ
materially include: [refer to Risk Factors in our most recent 10-K]. We undertake
no obligation to update any forward-looking statement.
```
Counsel must review every cycle.

### Recipe 6 — Business Wire embargoed submission
```bash
curl -X POST -H "Authorization: Bearer $BUSINESSWIRE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "ACME Reports Q2 2026 Results...",
    "body_html": "<html>...</html>",
    "embargo_until": "2026-07-30T20:01:00Z",
    "industries": ["technology"],
    "distribution": ["national", "financial"]
  }' \
  "https://api.businesswire.com/v2/releases"
```

### Recipe 7 — PR Newswire submission
```bash
curl -X POST -H "Authorization: Bearer $PR_NEWSWIRE_API_KEY" \
  -d @release.json \
  "https://api.prnewswire.com/v2/financial-disclosure/releases"
```

### Recipe 8 — Notified earnings release submission
```bash
curl -X POST -H "Authorization: Bearer $NOTIFIED_API_KEY" \
  -d @release.json \
  "https://api.notified.com/v1/press-releases"
```

### Recipe 9 — Guidance table format
```python
GUIDANCE_TABLE = """
| Metric          | Q3 FY26          | Full Year FY26      |
|-----------------|------------------|---------------------|
| Revenue         | $1.10-1.13B      | $4.35-4.45B (raised)|
| Non-GAAP Op Inc | $260-270M        | $1.02-1.05B         |
| Non-GAAP EPS    | $1.78-1.82       | $7.05-7.20          |
"""
# Guidance must be cross-referenced in Safe Harbor; counsel reviews
```

### Recipe 10 — Cross-link to IR website + 8-K
```bash
# Trigger Q4 IR-website earnings center update
mcp call q4-website-update \
  --section earnings_center \
  --release_url "https://www.businesswire.com/..." \
  --8k_url "https://sec.gov/..."
```

### Recipe 11 — Post-release sentiment quick-read
```bash
# T+5 min: check Twitter / Bloomberg / Reuters headline reactions
mcp call twitter-mcp search --q "$TICKER earnings" --hours 1
```

## Examples

### Example 1: Beat-and-raise Q2 release (mid-cap SaaS)

**Goal:** Q2 close July 28, release after-market 4:01 PM ET July 30, call 5:00 PM ET.

**Steps:**
1. T-5 days: financial close package from `finance-agent`.
2. T-4: consensus snapshot (FactSet); identify beat/miss/raise scenarios.
3. T-3: draft headline (Recipe 2) — "ACME Q2 Revenue Up 28% to $1.05B; Raised Full-Year Guidance."
4. T-3: draft bullets, CEO quote (Recipe 3), CFO quote, financial highlights.
5. T-2: Reg G recon tables (Recipe 4); counsel review.
6. T-1: final lock; pre-load Business Wire embargoed submission (Recipe 6).
7. T-0 (July 30, 3:59 PM ET): IR confirms Business Wire embargo; Workiva 8-K Item 2.02 ready.
8. T-0 (4:01 PM ET): embargo lifts; wire goes; 8-K files; IR site updates (Recipe 10).
9. T+5: sentiment quick-read (Recipe 11).
10. T+30 min: earnings call begins.

**Result:** Wire-to-EDGAR-to-IR-website synced within 5 min; analyst notes reference "raise" within 30 min.

### Example 2: In-line Q with reaffirmed guidance

**Goal:** In-line quarter; no raise; need to avoid disappointment narrative.

**Steps:**
1. Headline emphasizes strategic: "ACME Q2 In Line with Expectations; Enterprise Pipeline +35% YoY; Reaffirmed Full-Year Guidance."
2. CEO quote emphasizes forward strategic frame, not Q-print numbers.
3. CFO quote emphasizes capital discipline + back-half visibility.
4. Bullets weight strategic over financial 60/40.
5. Reaffirmed guidance with explicit table (Recipe 9).
6. Standard wire path.

**Result:** Stock holds flat post-release; analyst notes use "steady" not "disappointing."

## Edge cases / gotchas

- **Reg G equal-or-greater-prominence violation.** Non-GAAP cannot be more prominent than GAAP; headline cannot lead with non-GAAP without GAAP equal mention.
- **Beat / miss / in-line claim error.** Must verify against consensus snapshot timestamp; consensus moves T-1 to T-0; pull both.
- **Embargo leak.** Business Wire / PR Newswire have insider leak history (rare but happens); have backup wire vendor.
- **8-K Item 2.02 mistiming.** Must file within minutes of wire; SEC EDGAR Next + Workiva integration helps.
- **CFO sign-off lag.** CFO typically locks numbers T-2 to T-1; build buffer.
- **Counsel Safe Harbor scope.** Each forward-looking statement must be covered by Safe Harbor; counsel reviews each new bullet.
- **Guidance table consistency with last release.** If raise: comp this Q vs prior bracket; if lower: name reason directly.
- **Conference call dial-in / passcode wrong.** Triple-check; analyst frustration = lost trust.
- **Segment reconciliation to total revenue.** Sum-of-segments must tie to total; check sum.
- **YoY vs sequential confusion.** Both should be in table; investors expect both.
- **Wire vendor outage.** Business Wire outage 1-2x/yr historically; have backup wire.
- **Pre-release sentiment hint.** Stock movement in last 60 min before release can signal a leak; investigate post.
- **Cross-link delay.** Q4/Notified earnings page update should be within minutes; longer = analyst complaints.
- **Foreign-language wire need.** ADR companies may need French/Japanese versions; coordinate with translation vendor.

> Mandatory disclaimer: Earnings press releases are paired with binding 8-K Item 2.02 filings. All forward-looking statements must comply with Safe Harbor + Reg G. All non-GAAP measures must comply with Reg G reconciliation + equal-or-greater-prominence rules. **Consult licensed securities counsel** for binding Safe Harbor language, Reg G reconciliation review, and guidance-statement Safe Harbor coverage each quarter.

## Sources

- Notified Press Release Distribution: https://www.notified.com/products/press-release-distribution
- Business Wire IR: https://www.businesswire.com/portal/site/home/ir/
- PR Newswire Financial Disclosure: https://www.prnewswire.com/services/financial-disclosure/
- Globe Newswire: https://www.globenewswire.com/
- SEC Regulation G (Non-GAAP reconciliation): https://www.sec.gov/rules/final/33-8176.htm
- SEC Compliance & Disclosure Interpretations — Non-GAAP: https://www.sec.gov/divisions/corpfin/guidance/nongaapinterp.htm
- Private Securities Litigation Reform Act (Safe Harbor): https://www.congress.gov/bill/104th-congress/house-bill/1058
- See `role.md` -> "Earnings press release playbook"

## Related skills

- `earnings-call-script-qa` — call script paired with release.
- `8k-event-reporting` — Item 2.02 paired filing.
- `guidance-setting` — guidance section sourced from this.
- `quarterly-board-letter` — internal cadence parallel.
- `quiet-period-mgmt` — lifts on release.
