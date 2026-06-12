<!--
Source: https://whalewisdom.com/
Source: https://13f.info/
Source: https://www.sec.gov/divisions/investment/13ffaq.htm
Source: https://www.onsemicdp.com/13f-holdings
Source: https://www.sec.gov/edgar/searchedgar/companysearch.html
Reference role.md: "13F monitoring playbook"
Round 2 enrichment: monthly cadence + 13D/G activist scan + Form 4 insider trade flag + outreach decision tree + new-buyer welcome packet.
-->

# 13F shareholder monitoring (institutional holdings)

Pulls 13F filings (institutional >$100M AUM quarterly, 45 days post quarter-end) via SEC EDGAR XBRL + Whale Wisdom / 13F Info. Reconciles vs prior quarter — flags NEW initiations, >=25% size changes, full EXITS. Also scans 13D/G for >5% concentrated holders + activist signals; Form 4 for insider trades. Triggers outbound to changed holders.

## When to use

- Monthly 13F refresh (45-day window means filings dribble in over April-May for Q1, etc.).
- New institutional buyer welcome (initiation flagged).
- 13D/G activist filing flag (>5% holder).
- Form 4 insider trade flag.
- Pre-NDR target list refresh (`roadshow-ndr-logistics`).
- Trigger phrases: "13F refresh", "13F update", "holder tracking", "institutional holders", "shareholder monitoring", "13D activist", "Form 4 insider trade".

NOT for: analyst notes (use `equity-analyst-relations-briefings`); roadshow scheduling (use `roadshow-ndr-logistics`); private-co cap-table (use `monthly-investor-update-visible`).

## Setup

```bash
# Whale Wisdom (Pro tier for API; free tier UI)
export WHALEWISDOM_API_KEY="<from WhaleWisdom Pro -> Account>"  # $200/mo+

# 13F Info (free UI; HTML scrape fallback via firecrawl-mcp)
# SEC EDGAR XBRL (free, direct)
export SEC_EDGAR_USER_AGENT="Investor Relations <ir@company.com>"

# Tools: sec-edgar-mcp for direct EDGAR; xlsx for delta tracker; notion-mcp for holder CRM
```

Auth / API key requirements:
- `WHALEWISDOM_API_KEY` — Pro tier ~$200/mo+ for REST.
- Free fallback: SEC EDGAR direct + 13F Info HTML scrape via `firecrawl-mcp`.
- `SEC_EDGAR_USER_AGENT` — required for EDGAR API (must include contact email).

Data inputs:
- Our ticker + CUSIP.
- Prior-quarter 13F snapshot (xlsx archive).
- Holder CRM (notion-mcp) — for outreach history.
- Free-tier 13F Info / OnSemiCDP for cross-reference.

## 13F regulatory framework

- Institutional investment managers with >$100M AUM file quarterly.
- 45-day window post quarter-end (so Q1 filings = May 15).
- Discloses long positions in 13F-eligible securities (most US equities, some options).
- Does NOT disclose shorts (unless reported via separate disclosures).
- Subject to confidential treatment exemptions (rare).
- Form 13F-HR is the standard; 13F-NT for omitted small positions.

## 13D / 13G distinction

- **13D** = >5% holder WITH activist intent (10-day filing window from threshold cross).
- **13G** = >5% holder WITHOUT activist intent (passive; 45-day filing window).
- 13D filer must file amendments on material changes; 13G has annual amendments.
- Activist flag = treat 13D as immediate escalation.

## Form 4 (insider trades)

- Officers / directors / >10% owners must file within 2 business days of trade.
- Discloses transaction type (buy/sell, derivative exercise, gift).
- Significant insider sells = potential analyst signal.
- 10b5-1 plan trades flagged separately.

## Monthly cadence

| Date | Activity | Tool |
|------|----------|------|
| Day 1 | Pull all 13Fs containing our ticker | Recipe 1 / 2 |
| Day 2 | Compute deltas vs prior Q | Recipe 4 |
| Day 3 | Flag for outreach (Tree) | notion-mcp |
| Day 5 | Scan 13D/G + Form 4 | Recipe 6 + 7 |
| Day 7 | Digest to CEO/CFO/IR | Recipe 8 |
| Daily | New 13D/G + Form 4 alerts | Recipe 9 |

## Outreach decision tree

| Signal | Action | Timeline |
|--------|--------|----------|
| New initiation | IR welcome packet | T+30 days |
| Large add (>=25%) | Schedule 1:1 with PM | T+60 days |
| Exit | Respectful 1:1 (understand why) | T+90 days |
| Cross 1% of float (concentration) | IR awareness + brief | T+30 days |
| 13D filer (>5% with intent) | Escalate CEO/CFO/counsel | Immediate |
| 13G filer (>5% passive) | IR brief; routine 1:1 | T+45 days |
| Form 4 large insider sell | Brief CEO/CFO; prep for analyst Q | T+1 day |

## Common recipes

### Recipe 1 — Pull 13Fs via Whale Wisdom
```bash
curl -H "Authorization: Bearer $WHALEWISDOM_API_KEY" \
  "https://whalewisdom.com/api/v1/holders?ticker=$TICKER&quarter=$QUARTER_END&include_changes=true"
# Returns: list of all 13F filers + position size + delta vs prior Q
```

### Recipe 2 — Direct SEC EDGAR XBRL
```bash
mcp call sec-edgar-mcp fetch_form --ticker=$TICKER --form="13F-HR" --period=$PERIOD
# Cross-reference with 13F Info or OnSemiCDP for filer name lookup
```

### Recipe 3 — Build delta tracker xlsx
```python
import pandas as pd

current = pd.read_csv("13f_current_quarter.csv")
prior   = pd.read_csv("13f_prior_quarter.csv")

merged = current.merge(prior, on="filer_cik", how="outer", suffixes=("_now", "_prev"))
merged["delta_shares"] = merged["shares_now"].fillna(0) - merged["shares_prev"].fillna(0)
merged["pct_change"] = merged["delta_shares"] / merged["shares_prev"].replace(0, float("inf"))
merged["category"] = merged.apply(categorize, axis=1)
merged.to_excel("13f_delta_Q2_to_Q3_2026.xlsx")

def categorize(row):
    if pd.isna(row["shares_prev"]) and row["shares_now"] > 0: return "INITIATION"
    if pd.isna(row["shares_now"]) and row["shares_prev"] > 0: return "EXIT"
    if row["pct_change"] >= 0.25: return "LARGE_ADD"
    if row["pct_change"] <= -0.25: return "LARGE_TRIM"
    return "SAME"
```

### Recipe 4 — Holder CRM update (notion-mcp)
```bash
mcp call notion-mcp create_page --database=$HOLDER_DB \
  --properties='{
    "Filer": "BlackRock Inc.",
    "CIK": "0001364742",
    "Position (Q3 2026)": 5230000,
    "Position (Q2 2026)": 4180000,
    "Delta %": 25.1,
    "Category": "LARGE_ADD",
    "Stance": "PASSIVE",
    "Last 1:1": "2025-11-18",
    "Outreach Due": "2026-09-15"
  }'
```

### Recipe 5 — IR welcome packet template (new initiation)
```python
WELCOME_PACKET = [
    "Cover letter (1 page) — thank, frame our long-term thesis",
    "Latest investor deck",
    "Last 4 earnings transcripts",
    "10-K + 10-Q linkouts",
    "Capital allocation philosophy 1-pager",
    "Long-range model framework (from investor day)",
    "Offer: 1:1 with CFO or IR within 60 days",
]
# Send via gmail-mcp or Visible.vc-equivalent
```

### Recipe 6 — Scan 13D/G filings
```bash
mcp call sec-edgar-mcp fetch_form --ticker=$TICKER --form="SC+13D" --days=30
mcp call sec-edgar-mcp fetch_form --ticker=$TICKER --form="SC+13G" --days=30
# Flag any new filer; 13D = immediate escalation
```

### Recipe 7 — Scan Form 4 (insider trades)
```bash
mcp call sec-edgar-mcp fetch_form --ticker=$TICKER --form=4 --days=30
# Filter: trades where shares > $1M or > 25% of insider's pre-trade holdings
# Flag any non-10b5-1 sell
```

### Recipe 8 — Monthly digest to CEO/CFO/IR
```markdown
# 13F Monthly Digest — September 2026

## Headline
- 3 NEW initiations (BlackRock +5.2M shares = 1.4% of float; ...)
- 2 LARGE ADDS (Fidelity +1.8M; ...)
- 1 EXIT (smaller hedge; thesis-divergent)
- 0 13D filings; 1 13G (Vanguard passive)

## Action Items
- IR welcome packet to BlackRock by T+30 days
- 1:1 scheduling for Fidelity by T+60 days
- Brief CEO on 13G (Vanguard reached 5.1%)

## Trend
- Top 10 holders own 38% of float (+2 pp vs Q2)
- Avg holding period (estimated) = 5.2 quarters
```

### Recipe 9 — Daily 13D/G + Form 4 alert
```bash
# Cron daily
mcp call sec-edgar-mcp fetch_form --ticker=$TICKER --form="SC+13D" --days=1
mcp call sec-edgar-mcp fetch_form --ticker=$TICKER --form=4 --days=1
# Email digest via gmail-mcp to ir@company.com
```

### Recipe 10 — Pre-NDR target list cross-ref
```python
# Cross-reference 13F holders with prospective NDR meeting list
existing_holders = pd.read_excel("13f_delta_Q3_2026.xlsx")
ndr_targets = pd.read_csv("ndr_target_list.csv")
ndr_targets["existing_position"] = ndr_targets["fund"].map(
    existing_holders.set_index("filer")["shares_now"].to_dict()
)
# Funds with positions get longer briefing books
```

### Recipe 11 — Free-tier 13F Info HTML scrape (fallback)
```bash
mcp call firecrawl-mcp scrape \
  --url "https://13f.info/manager/0001364742-blackrock-inc/$YEAR" \
  --formats markdown
```

### Recipe 12 — Quarterly concentration trend
```python
# Track concentration ratio: top-10 / top-25 / top-50 of float
def concentration(df, n):
    return df.nlargest(n, "shares_now")["shares_now"].sum() / df["shares_now"].sum()
print(f"Top 10: {concentration(current, 10):.1%}")
print(f"Top 25: {concentration(current, 25):.1%}")
# Rising concentration -> growing institutional interest; falling -> retail-shifting risk
```

## Examples

### Example 1: Monthly Q3 2026 refresh

**Goal:** Sept 15, 2026 — Q2 2026 filings deadline passed; build delta vs Q1.

**Steps:**
1. Pull Q2 filings via Whale Wisdom (Recipe 1).
2. Build delta xlsx vs Q1 (Recipe 3).
3. Categorize: 4 initiations, 6 large adds, 2 exits, 1 large trim.
4. Update notion-mcp holder CRM (Recipe 4).
5. Scan 13D/G + Form 4 (Recipes 6 + 7).
6. Build monthly digest (Recipe 8); send to CEO/CFO/IR.
7. Schedule outreach: 4 welcome packets (Recipe 5); 6 PM 1:1s.
8. NDR target list cross-ref (Recipe 10).

**Result:** Outreach pipeline live; 4 new holders welcomed; NDR list refreshed with current 13F context.

### Example 2: 13D activist flag

**Goal:** Schedule 13D filed by Acme Capital showing 5.4% stake + activist intent letter.

**Steps:**
1. Daily 13D scan triggers alert (Recipe 9) — within hours of filing.
2. IR escalates to CEO/CFO/counsel/board chair within 30 minutes.
3. Pull activist's track record (prior 13Ds; outcomes); rough timeline.
4. Pull activist's stated intent from 13D narrative.
5. Engage specialist activist-defense firm (Joele Frank / Sard Verbinnen).
6. Pull `equity-analyst-relations-briefings` — brief CEO/CFO on likely analyst Qs.
7. Counsel directs all comms; IR runs the playbook.
8. Update coverage matrix; brief next quarter's analyst 1:1s with counsel-approved talking points.

**Result:** Activist response coordinated; controlled comms; no surprise to investor base.

### Example 3: New initiation welcome

**Goal:** Tiger Global new initiation: 2.1M shares, $84M, Q3 filing.

**Steps:**
1. Pulled in delta tracker (Recipe 3); category = INITIATION.
2. Assemble welcome packet (Recipe 5).
3. CEO/CFO/IR co-sign cover letter; send within 30 days.
4. Schedule 1:1 within 60 days; CFO + IR attend.
5. Update notion CRM (Recipe 4); stance = INITIATING; cadence = quarterly.
6. Brief on multi-quarter thesis; not new news (Reg FD).
7. Add to next NDR list.

**Result:** Tiger Global added 30% in Q4 after welcome 1:1 (visibility built trust).

## Edge cases / gotchas

- **45-day filing window staggering.** Q1 filings = May 15; large funds typically file last week; smaller earlier. Refresh weekly post-deadline.
- **Confidential treatment requests.** Some 13Fs hide build-ups under confidential treatment; rare but possible.
- **Sub-advisor reporting.** A 13F filer may be sub-advisor; underlying owner of the stake may be elsewhere.
- **CUSIP changes.** Stock splits + reincorporations change CUSIPs; reconcile cross-event 13Fs carefully.
- **13D vs 13G crossover.** A passive 13G filer who turns activist must amend 13D within 10 days; track filings.
- **Form 4 timing.** 2-business-day filing; same-day for related-party trades.
- **10b5-1 plan trades.** Form 4 lists 10b5-1 separately; don't read as discretionary signal.
- **Whale Wisdom paywall.** Pro tier ~$200/mo. Free fallback: SEC EDGAR direct + Firecrawl on 13F Info.
- **Shorts not in 13F.** Hedge fund 13F shows longs only; short side is hidden.
- **Initiation false positive.** A "new" position may be sub-advisor migration not new bet; verify.
- **Reg FD risk in welcome 1:1.** Same as analyst 1:1; prepared remarks + published filings only.
- **Exit interview risk.** Exit holder may share thesis; do NOT use that for selective MNPI swap.
- **Concentration risk signal.** Very high top-10 concentration = liquidity risk if one exits.
- **Index fund inclusion / exclusion.** S&P/Russell/MSCI rebalances drive index-fund 13F deltas; not strategic.

> Mandatory disclaimer: 13F monitoring is research; outbound to holders is subject to Regulation FD. **Consult licensed securities counsel** before any communication with a 13D filer (potential activist), before any pre-arranged 1:1 with a new institutional holder, and for interpretation of Reg FD around holder briefings.

## Sources

- Whale Wisdom 13F Database: https://whalewisdom.com/
- 13F Info: https://13f.info/
- SEC 13F FAQ: https://www.sec.gov/divisions/investment/13ffaq.htm
- SEC EDGAR Company Search: https://www.sec.gov/edgar/searchedgar/companysearch.html
- OnSemiCDP 13F Holdings: https://www.onsemicdp.com/13f-holdings
- SEC Schedule 13D/G Rules: https://www.sec.gov/divisions/corpfin/cf-rule13d.htm
- SEC Form 4 Reporting: https://www.sec.gov/edgar/sec-api-documentation
- See `role.md` -> "13F monitoring playbook"

## Related skills

- `equity-analyst-relations-briefings` — analyst 1:1s with holders.
- `roadshow-ndr-logistics` — NDR target list cross-ref.
- `ma-investor-comms` — sweeping holder comms.
- `quiet-period-mgmt` — restricts holder briefings in run-up.
- `embargoed-disclosure-protocols` — for any embargoed holder briefing.
