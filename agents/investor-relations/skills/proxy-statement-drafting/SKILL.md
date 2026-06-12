<!--
Source: https://www.workiva.com/solutions/proxy
Source: https://insights.issgovernance.com/
Source: https://www.glasslewis.com/policy-guidelines/
Source: https://www.sec.gov/files/rules/final/2022/33-11038.pdf
Source: https://www.ecfr.gov/current/title-17/chapter-II/part-240/subpart-A/subjgrp-21/section-240.14a-101
Reference role.md: "Proxy statement playbook" + "Item 402(v) Pay-versus-Performance walkthrough" + "ISS / Glass Lewis 2026 policy delta"
Round 2 enrichment: full CD&A template + Item 402(v) PVP table + Universal Proxy Card (UPC) section + AGM virtual coord.
-->

# Proxy statement (DEF 14A) drafting

Drafts the annual proxy statement (Form DEF 14A) for public companies — director bios, executive compensation (CD&A + Summary Comp Table + Item 402(v) Pay-versus-Performance + grants + outstanding equity + employment agreements + termination payouts), audit committee report, say-on-pay, auditor ratification, shareholder proposals, Universal Proxy Card setup. Pre-engages ISS Voting Insights + Glass Lewis Proxy Paper.

## When to use

- Annual DEF 14A drafting (typically issued T-30 to T-45 days before AGM).
- Item 402(v) Pay-versus-Performance table compilation (2025+ requirement).
- Engagement with ISS / Glass Lewis pre-publication on contested items.
- Universal Proxy Card preparation (Rule 14a-19, in effect since Sep 2022).
- Trigger phrases: "proxy statement", "DEF 14A", "proxy drafting", "AGM proxy", "say-on-pay", "Pay-versus-Performance", "Item 402(v)".

NOT for: 10-K Part III items by reference (use `10k-10q-drafting-workiva`); 8-K Item 5.07 AGM results (use `8k-event-reporting`); virtual AGM logistics (use `investor-day-capital-markets-day`).

## Setup

```bash
# Workiva for drafting (preferred)
export WORKIVA_API_KEY="<from Workiva Admin -> API>"

# ISS Voting Insights + Glass Lewis Proxy Paper (paid)
export ISS_API_KEY="<from ISS Issuer Portal>"
export GLASS_LEWIS_API_KEY="<from Glass Lewis Issuer Portal>"

# Tools: sec-edgar-mcp for peer DEF 14A precedent; docx for portable draft; xlsx for PVP table
```

Auth / API key requirements:
- `WORKIVA_API_KEY` — Workiva proxy module ($60K+/yr typical bundle).
- `ISS_API_KEY` — ISS Issuer Engagement subscription ($25K+/yr).
- `GLASS_LEWIS_API_KEY` — Glass Lewis Issuer Engagement ($20K+/yr).
- Free fallback: SEC EDGAR DEF 14A precedent + public ISS / Glass Lewis policy guidelines.

Data inputs:
- Prior-year DEF 14A (own + 3-5 peers).
- Director questionnaires (D&O) for bios + skills matrix.
- Comp consultant report (Pearl Meyer / Mercer / Pay Governance / Aon).
- Executive comp data (Summary Comp Table inputs: salary, bonus, equity grants, perks, deferred).
- TSR + Net Income + Company-Selected Measure for PVP table.

## DEF 14A 2026 structure

1. **Notice of Annual Meeting**
2. **Proxy Statement Summary** (1-2 page overview; investor-friendly)
3. **Voting Information** (record date, eligibility, deadlines, Universal Proxy Card)
4. **Election of Directors**
   - Director bios + skills matrix
   - Board structure + committee composition
   - Director independence determinations
   - Director compensation table
5. **Corporate Governance**
   - Board leadership structure + risk oversight
   - Codes of conduct + ethics
   - Cybersecurity governance (cross-ref to 10-K Item 1C)
   - ESG governance (if material)
   - Shareholder engagement summary
6. **Executive Compensation**
   - **CD&A** (Compensation Discussion & Analysis)
   - Summary Compensation Table
   - Grants of Plan-Based Awards
   - Outstanding Equity Awards at Fiscal Year-End
   - Option Exercises + Stock Vested
   - Pension Benefits + Nonqualified Deferred Comp
   - Potential Payments on Termination + Change in Control
   - CEO Pay Ratio (Item 402(u))
   - **Item 402(v) Pay-versus-Performance** (table + narrative)
7. **Audit Committee Report** + Independent Auditor proposal
8. **Say-on-Pay Proposal**
9. **Say-on-Frequency** (every 6 years)
10. **Shareholder Proposals** (Rule 14a-8 proposals if received)
11. **Other Matters**
12. **Appendices** (typically: non-GAAP reconciliation; equity-plan info)

## Item 402(v) Pay-versus-Performance walkthrough

**Required table columns (smaller reporting companies have a stripped-down version):**

```
Year | SCT Total Comp PEO | Comp Actually Paid PEO | Avg SCT NEO | Avg CAP NEO |
     | Co TSR | Peer Group TSR | Net Income | Company-Selected Measure
```

**CAP (Compensation Actually Paid) adjustment math** (the trap):

```
CAP = SCT Total
    - Stock awards in SCT (fair value at grant)
    - Option awards in SCT (fair value at grant)
    + Stock awards fair value change EOY vs BOY (vested + unvested)
    + Option awards fair value change EOY vs BOY (vested + unvested)
    + Stock awards FV at vesting date (if vested in year)
    + Option awards FV at vesting date (if vested in year)
    - Stock + option awards forfeited
    + Dividends paid on unvested awards (if not in SCT)
```

Most companies under-disclose adjustment math — counsel + comp consultant must sign.

## Workflow

1. T-150: Pull last year's DEF 14A + 3-5 peer DEF 14As.
2. T-120: Comp consultant report finalized (drives CD&A narrative).
3. T-100: Director questionnaires returned; skills matrix drafted.
4. T-90: Pre-engage ISS Voting Insights + Glass Lewis Proxy Paper on say-on-pay structure.
5. T-75: Draft CD&A narrative + Item 402(v) PVP table.
6. T-60: Workiva diff vs prior; counsel pass #1.
7. T-45: Audit committee report draft; auditor coordination.
8. T-30: ISS / Glass Lewis check-in on draft.
9. T-21: SEC EDGAR Next submission (DEF 14A); printer (Donnelley/Workiva) prints + mails.
10. T-0: AGM held.

## Common recipes

### Recipe 1 — Pull peer DEF 14As
```bash
for peer in $PEER_TICKERS; do
  mcp call sec-edgar-mcp fetch_form --ticker=$peer --form="DEF+14A" --year=$PRIOR_YEAR
done
```

### Recipe 2 — ISS Voting Insights policy pull
```bash
curl -H "x-api-key: $ISS_API_KEY" \
  "https://api.issgovernance.com/v1/policy?year=2026&region=US"
```

### Recipe 3 — Glass Lewis Proxy Paper policy pull
```bash
curl -H "Authorization: Bearer $GLASS_LEWIS_API_KEY" \
  "https://api.glasslewis.com/v1/policy/us/2026"
```

### Recipe 4 — PVP table generator
```python
import pandas as pd

def cap_adjustment(sct_total, sct_stock_at_grant, sct_options_at_grant,
                   stock_fv_change_eoy_boy, options_fv_change_eoy_boy,
                   stock_fv_at_vesting, options_fv_at_vesting,
                   forfeitures, dividends_unvested):
    return (sct_total
            - sct_stock_at_grant - sct_options_at_grant
            + stock_fv_change_eoy_boy + options_fv_change_eoy_boy
            + stock_fv_at_vesting + options_fv_at_vesting
            - forfeitures
            + dividends_unvested)

# Build the 5-year (or 3-year for SRC) table; columns per spec
pvp_table = pd.DataFrame({
    "Year": [2022, 2023, 2024, 2025, 2026],
    "SCT_PEO": [...],
    "CAP_PEO": [...],
    "Avg_SCT_NEO": [...],
    "Avg_CAP_NEO": [...],
    "TSR_Company": [...],
    "TSR_Peer": [...],
    "Net_Income": [...],
    "CSM": [...],  # Company-Selected Measure
})
```

### Recipe 5 — CD&A pay-mix discussion template
```
CD&A standard sections:
1. Executive summary (pay philosophy + this year's outcomes)
2. Compensation philosophy + objectives
3. Setting executive comp (process, comp committee, consultant)
4. Elements of compensation (base, STI, LTI, perks, benefits)
5. Pay-for-performance (PVP table reference)
6. Risk + clawback (Dodd-Frank Rule 10D-1 clawback policy)
7. Other (hedging policy, share ownership guidelines, perqs)
```

### Recipe 6 — Universal Proxy Card setup (Rule 14a-19)
```python
# UPC required since Sep 2022 in contested elections
# Standard UPC layout:
# - Issuer nominees in one column
# - Dissident nominees in adjacent column
# - "FOR/WITHHOLD/AGAINST" per nominee
# Issuer's proxy card MUST include dissident nominees (and vice versa)
# Notice + nomination deadlines extended
```

### Recipe 7 — Workiva diff + redline
```bash
curl -H "Authorization: Bearer $WORKIVA_API_KEY" \
  "https://api.workiva.com/v1/documents/$DOC_ID/diff?baseline=$PRIOR_DOC_ID"
```

### Recipe 8 — Shareholder engagement summary (CGSI)
```
Standard disclosure:
- Number of shareholders engaged (% of shares outstanding represented)
- Topics discussed (governance, ESG, comp, capital allocation)
- Changes made in response
```

### Recipe 9 — Audit committee report
```python
AUDIT_COMMITTEE_REPORT = """
The Audit Committee has reviewed and discussed the audited financial statements
with management and the independent registered public accounting firm. The
Committee has discussed with the independent auditor the matters required to
be discussed by [PCAOB Auditing Standard 1301]... [counsel-supplied boilerplate]
"""
# Standard structure; counsel-supplied
```

### Recipe 10 — SEC EDGAR DEF 14A submission
```bash
# Workiva integrated
curl -X POST -H "Authorization: Bearer $WORKIVA_API_KEY" \
  -d '{"action": "file_to_edgar", "form": "DEF 14A"}' \
  "https://api.workiva.com/v1/documents/$DOC_ID/submit"
```

## Examples

### Example 1: Routine annual DEF 14A (uncontested)

**Goal:** FY2026 DEF 14A; AGM 2027-05-15; all standard items.

**Steps:**
1. T-150 (Dec 2026): Pull last year + peer DEF 14As (Recipe 1).
2. T-120 (Jan 2027): Comp consultant report final.
3. T-90 (Feb 2027): ISS / Glass Lewis policy pull (Recipes 2 + 3); pre-engagement call.
4. T-75 (Mar 2027): Draft CD&A; PVP table (Recipe 4); director skills matrix.
5. T-60 (Mar 2027): Workiva draft + counsel pass #1.
6. T-30 (Apr 2027): ISS / Glass Lewis check-in on draft.
7. T-21 (Apr 2027): DEF 14A filed via EDGAR.
8. T-0 (May 2027): AGM; results filed via 8-K Item 5.07 within 4 business days.

**Result:** ISS + Glass Lewis recommendations Favor; say-on-pay passes >90%; clean AGM.

### Example 2: Contested election (activist nominee)

**Goal:** Activist has nominated 3 directors via Rule 14a-19; Universal Proxy Card.

**Steps:**
1. Pre-engagement: counsel, IR, comp consultant, financial advisor.
2. ISS / Glass Lewis early pre-engagement (Recipes 2 + 3); position firmly.
3. UPC layout (Recipe 6) — must include activist nominees alongside issuer's.
4. Heightened CD&A scrutiny (activist may attack on pay-for-performance gap).
5. Robust Item 402(v) PVP table (Recipe 4) — clean math; CAP adjustments fully disclosed.
6. Shareholder solicitation campaign (Innisfree / Okapi proxy solicitor).
7. **Defer** to specialist counsel + proxy solicitor on activist defense strategy.

**Result:** Outcome depends on substance; preparation reduces surprise.

## Edge cases / gotchas

- **Item 402(v) PVP CAP adjustment errors.** Most common SEC comment letter trigger 2024-2025; counsel + comp consultant must reconcile.
- **CEO Pay Ratio (Item 402(u)) methodology consistency.** Once you pick a methodology, must use it 3 years.
- **Universal Proxy Card mistakes.** Must include opposition slate; failure = SEC enforcement.
- **ISS / Glass Lewis 2026 policy delta from 2025.** Refresh policy each January; key changes: AI governance disclosure, climate transition risk, board diversity metrics.
- **Shareholder Proposal Rule 14a-8 timing.** Proposal received deadline 120 days before AGM; ground for exclusion is counsel-driven.
- **D&O questionnaire response delays.** Director bios can't be locked until D&O questionnaires returned; build buffer.
- **Comp consultant independence.** Consultant must be independent from management; disclosed in proxy.
- **Hedging / clawback / pledging policies.** Required disclosures under Item 407(i); easy to miss in update.
- **ESG governance overflow.** Some ESG items belong in proxy (board oversight); others in 10-K Item 1; coordinate with `esg-investor-reporting-gri-sasb-tcfd`.
- **Smaller Reporting Company (SRC) simplifications.** PVP table = 3 years not 5; some Item 402 sections skipped; check filer status.
- **Printer / mailer timing.** Workiva / Donnelley print T-21; physical mail must reach shareholders T-10.
- **AGM virtual / hybrid logistics.** Broadridge / Computershare / Notified handle virtual AGM streaming.
- **Dodd-Frank Rule 10D-1 clawback policy.** Required to disclose; if no clawback, must explain why.

> Mandatory disclaimer: DEF 14A is a binding SEC filing. **Consult licensed securities counsel** for every aspect — Reg S-K Item 14 / Item 402 compliance, Item 402(v) PVP CAP adjustments, Universal Proxy Card mechanics under Rule 14a-19, shareholder-proposal exclusion analysis under Rule 14a-8, and EDGAR submission. This skill drafts to a counsel-reviewable bar; counsel + audit committee + comp committee approve binding filing.

## Sources

- Workiva Proxy: https://www.workiva.com/solutions/proxy
- ISS Voting Insights: https://insights.issgovernance.com/
- Glass Lewis Policy Guidelines: https://www.glasslewis.com/policy-guidelines/
- SEC Item 402(v) Pay-versus-Performance Final Rule: https://www.sec.gov/files/rules/final/2022/33-11038.pdf
- SEC Rule 14a-19 Universal Proxy Card: https://www.sec.gov/rules/final/2021/34-93596.pdf
- SEC Schedule 14A Regulations: https://www.ecfr.gov/current/title-17/chapter-II/part-240/subpart-A/subjgrp-21/section-240.14a-101
- Dodd-Frank Rule 10D-1 (clawback): https://www.sec.gov/rules/final/2022/33-11126.pdf
- Pearl Meyer comp consultant: https://www.pearlmeyer.com/
- Broadridge Virtual AGM: https://www.broadridge.com/solution/virtual-annual-meetings
- See `role.md` -> "Proxy statement playbook" + "Item 402(v) walkthrough" + "ISS / Glass Lewis 2026 policy delta"

## Related skills

- `10k-10q-drafting-workiva` — 10-K Part III incorporated by reference.
- `8k-event-reporting` — Item 5.07 AGM results filing.
- `esg-investor-reporting-gri-sasb-tcfd` — ESG governance disclosures.
- `equity-analyst-relations-briefings` — analyst briefing around AGM season.
