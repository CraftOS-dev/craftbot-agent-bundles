<!--
Source: https://www.bnymellon.com/us/en/insights/all-insights/non-deal-roadshow-best-practices.html
Source: https://www.qcomms.com/blog/non-deal-roadshow-best-practices
Source: https://www.notified.com/blog/non-deal-roadshow-virtual
Source: https://www.niri.org/professional-development/ipo-resources
Source: https://www.icrinc.com/services/ipo-edge/
Source: https://www.cooley.com/services/practice/securities-and-capital-markets/initial-public-offerings
Reference role.md: "Roadshow NDR playbook" + IPO management roadshow
Round 2 enrichment: per-meeting briefing book + sell-side desk routing + IPO mgmt roadshow 2-week sprint + virtual NDR.
-->

# Roadshow + non-deal roadshow (NDR) logistics

Plans and runs quarterly non-deal roadshows (NDRs) to existing + prospective institutional holders, plus IPO management roadshows (S-1 process). Coordinates with sell-side corporate access desks (Morgan Stanley / JPM / Goldman / B. Riley / Stifel / Cowen / Cantor) for meeting booking; builds briefing books with 13F attendee snapshots; runs logistics (travel + hotel + AV). Bounded by Reg FD on what can be said in 1:1 meetings.

## When to use

- Quarterly NDR planning (4-8 cities; 6-10 meetings/day/exec).
- IPO management roadshow (2-week sprint pre-pricing; 50-70 meetings).
- Conference appearance scheduling (sell-side conferences, industry events).
- Virtual NDR (off-cycle pulse check).
- Testing-the-waters meetings under Rule 163B (T-3 months pre-IPO).
- Trigger phrases: "non-deal roadshow", "NDR", "roadshow", "investor meetings", "IPO roadshow", "testing-the-waters", "TTW".

NOT for: financial modeling for S-1 (use `finance-agent`); 8-K announcement (use `8k-event-reporting`); investor day (use `investor-day-capital-markets-day`); analyst 1:1s (use `equity-analyst-relations-briefings`).

## Setup

```bash
# Sell-side corporate access (existing banking relationships)
# Each desk has its own portal — typically email/phone-based; some have REST APIs
export MS_CA_API_KEY="<from Morgan Stanley Corporate Access>"
export JPM_CA_API_KEY="<from JPM Corporate Access>"
export GS_CA_API_KEY="<from Goldman Corporate Access>"

# IR CRM (Salesforce IR variant common)
export SALESFORCE_IR_API_KEY="<from SF IR Cloud>"

# Tools: notion-mcp for meeting CRM; google-calendar-mcp for scheduling
# Tools: sec-edgar-mcp for 13F attendee snapshots; firstword-mcp (if recipient has) for logistics
```

Auth / API key requirements:
- Sell-side corporate access — relationship-based; each banking relationship gives access to that desk's institutional pipeline.
- `SALESFORCE_IR_API_KEY` — Salesforce IR Cloud or equivalent IR CRM ($30K+/yr).
- Free fallback: `notion-mcp` for meeting CRM + manual sell-side email.

Data inputs:
- Existing holder list (`13f-shareholder-monitoring` output).
- Prospect list (top non-holders by AUM in our sector).
- Bookrunner-supplied target list (for IPO mgmt roadshow).
- Latest earnings deck (post-earnings = best NDR window).
- 13F holdings snapshot per attendee.
- Recent published analyst notes from attending firms.

## NDR mechanics

| Meeting type | Duration | Participants | Notes |
|--------------|----------|--------------|-------|
| 1:1 | 45-60 min | 1 PM + 1-2 analysts; CEO+CFO+IR | Highest signal |
| Small group | 90 min | 4-6 funds; CEO+CFO+IR | Mid-volume |
| Group lunch / breakfast | 60-90 min | 10-15 funds; CEO+CFO | Cocktails; conf |
| Conference 1:1s | 30-45 min | 1-2/fund; CEO or CFO | Bank-arranged at conf |
| Virtual NDR | 30-45 min | 1 PM via Zoom; CEO+CFO+IR | Off-cycle pulse |

## Briefing book per-meeting schema (1-pager)

```
FUND: <Name + AUM + style: long-only/hedge/quant/index>
ATTENDEES: <Names + titles + AUM-following + tenure>
HOLDINGS: <Current 13F position vs prior Q; % of fund; sector tilt>
RECENT MOVES: <Adds/trims last 4 Qs>
PRIOR MEETINGS: <Date + outcome of last meeting>
PUBLISHED VIEWS: <Recent fund commentary, if available>
INTERESTS / FOCUS: <ESG / capital allocation / segment X / etc.>
TALKING POINTS (PREPARED REMARKS ONLY): <3-5 bullets from latest call>
LIKELY QUESTIONS: <3-5; cross-ref shareholder-qa-maintenance>
DO NOT DISCUSS: <MNPI items, current quarter trends, etc.>
```

## IPO management roadshow

- **T-12 months** to **T-3 months**: prep + testing-the-waters under Rule 163B.
- **T-3 weeks**: S-1 filed; bookrunners + counsel finalize roadshow plan.
- **T-2 weeks**: roadshow kicks off; 50-70 meetings over 9-10 trading days.
- Cities: NYC + Boston (50% of meetings) + SF + Chicago + LA + UK/Europe + Asia (depending on deal size).
- Mix: 60% 1:1 + 25% group lunch / dinner + 15% conference appearances.
- Daily debrief with bookrunners; build adjusts based on demand.
- T+0: pricing; T+1: open trading.

## Common recipes

### Recipe 1 — 13F snapshot per attendee fund
```bash
mcp call sec-edgar-mcp fetch_form --cik=$FUND_CIK --form=13F-HR --period=latest
# Returns position in our ticker + delta vs prior Q
```

### Recipe 2 — Build briefing book (Notion DB)
```bash
mcp call notion-mcp create_page \
  --database=$ROADSHOW_DB \
  --properties='{
    "Date": "2026-09-15",
    "City": "Boston",
    "Fund": "Acme Capital",
    "Attendees": "Jane Smith (PM), Bob Jones (analyst)",
    "Holding": "210,000 sh ($8.4M)",
    "Last Meeting": "2025-12-10",
    "Briefing Book URL": "https://...pdf"
  }'
```

### Recipe 3 — Sell-side corporate access request (email template)
```
To: corporate-access@<bank>.com
Subject: NDR target list — ACME — Sept 2026

We're planning an NDR Sept 14-25, four cities (NYC, Boston, SF, Chicago).
Attached: top 30 target funds by stake / sector fit.
Could we get 6-8 meetings/day, mix of 1:1 + small group + lunch?
CEO + CFO + IR attending. Specific dates flexible.
```

### Recipe 4 — Virtual NDR (Zoom + Notified)
```bash
# Notified investor-meeting module for streaming
curl -X POST -H "Authorization: Bearer $NOTIFIED_API_KEY" \
  -d '{"type": "virtual_meeting", "date": "...", "duration": 45}' \
  "https://api.notified.com/v1/investor-meetings"
```

### Recipe 5 — Attendee research (last 4 Qs of their published views)
```bash
# AlphaSense fund-commentary mining
curl -H "Authorization: Bearer $ALPHASENSE_API_KEY" \
  "https://api.alpha-sense.com/v1/search?author=$PM_NAME&doc_type=fund_commentary&limit=4"
```

### Recipe 6 — Logistics scheduler (google-calendar-mcp)
```bash
mcp call google-calendar-mcp create_event \
  --summary "NDR: Acme Capital (Smith)" \
  --location "Acme HQ 30th flr, NYC" \
  --start "2026-09-15T10:00:00-04:00" --duration 45 \
  --attendees "ceo@,cfo@,ir@,smith@acme.com"
```

### Recipe 7 — Daily NDR debrief template
```
Day: <date>
City: <city>
Meetings: <#>
Standouts: <2-3 specifically>
Pushback themes (1 per top 3): <margin / competitive / capital allocation>
New holder candidates: <names>
Existing holder concerns: <names + theme>
Followups due: <list with deadline>
```

### Recipe 8 — IPO testing-the-waters (Rule 163B)
```python
# Rule 163B permits pre-S-1 communications with QIBs (Qualified Institutional Buyers)
# + IAIs (Institutional Accredited Investors). Counsel-supervised.
TTW_RULES = {
    "audience": "QIBs + IAIs only",
    "approach": "verbal + materials; underwriter present",
    "no_offering": "no offers, no commitments, no allocation",
    "track": "list each fund + date + counsel sign-off",
    "filed_with_sec": "TTW materials filed as exhibit if substantive",
}
```

### Recipe 9 — Roadshow outcome scoring (post-trip)
```python
def score_meeting(meeting):
    return {
        "engagement": 1-5,         # how engaged was the PM
        "follow_up_requested": True/False,
        "model_change_likely": "increase/decrease/hold",
        "next_step": "1:1 in Q1 / send model / no action",
    }
# Aggregate; share with bookrunners / corporate access partners
```

### Recipe 10 — Sell-side conference appearance prep
```bash
# Pull conference attendee list (bank typically shares 1 week prior)
# Cross-ref to 13F holders + prospects
# Build per-attendee briefing book (Recipe 2)
```

## Examples

### Example 1: Q3 2026 NDR (mid-cap, 5 cities)

**Goal:** NDR Sept 14-25, 2026; 4 cities (NYC, Boston, SF, Chicago); 32 meetings.

**Steps:**
1. T-6 weeks: pull existing 13F holders (`13f-shareholder-monitoring`); identify 30 prospects.
2. T-5 weeks: email 4 sell-side corporate access desks (Recipe 3).
3. T-4 weeks: confirmed meeting list back from desks.
4. T-3 weeks: research each attendee (Recipe 5).
5. T-2 weeks: build briefing books (Recipe 2); CEO/CFO review.
6. T-1 week: calendar lock (Recipe 6); travel + hotel booked.
7. T-0 to T+12: execute meetings; daily debrief (Recipe 7).
8. T+15: outcomes scored (Recipe 9); shared with bookrunners + held in notion-mcp.
9. T+30: follow-ups completed; 2 model changes confirmed; 4 new initiations triggered.

**Result:** 4 new institutional holders within 60 days; 2 existing holders added; analyst note coverage +1.

### Example 2: IPO management roadshow

**Goal:** S-1 filed Sept 1; pricing planned Sept 15-18; 60 meetings.

**Steps:**
1. T-12 months: IR website + investor day deck draft (placeholder content).
2. T-9 months: TTW meetings under Rule 163B (Recipe 8) with 8-10 anchor funds.
3. T-6 months: S-1 narrative drafted (paired with `finance-agent` financials).
4. T-3 weeks: S-1 filed; bookrunners build target list (Lead + Co-Lead + Co-Mgr).
5. T-2 weeks: roadshow kicks off — NYC + Boston (week 1); SF + Chicago + LA + London (week 2).
6. Daily debrief with bookrunners; demand-build adjusts.
7. T+0: pricing call; T+1: open trading.
8. T+90: 1st earnings as public co (paired with `earnings-call-script-qa`).

**Result:** Book covered 5-7x; pricing at high end of range; orderly aftermarket.

### Example 3: Virtual NDR pulse check

**Goal:** Off-cycle (mid-Q1) virtual NDR with top-10 holders to gauge sentiment on macro.

**Steps:**
1. Identify top 10 holders by stake; outreach for 30-min Zoom (Recipe 4).
2. Build lighter briefing books (no travel logistics).
3. Run 10 calls over 5 days.
4. Aggregate themes (Recipe 7).
5. Share with CEO + CFO; informs next earnings prep.

**Result:** Early read on macro concerns; theme baked into next earnings call narrative.

## Edge cases / gotchas

- **Reg FD risk in 1:1s.** Same risk as analyst 1:1s; prepared remarks + published filings only. **No MNPI; no current-Q trend confirmations.**
- **Quiet period overlap.** No NDR meetings 2 weeks before earnings; coordinate with `quiet-period-mgmt`.
- **Sell-side desk competition for slots.** Multiple banks may target the same funds; transparently coordinate.
- **IPO TTW Rule 163B violations.** Easy to slip into "offer" language; counsel must supervise.
- **Travel jet lag / exec fatigue.** 6-10 meetings/day for 5+ days is brutal; build buffer; cap energy.
- **Group lunch attendee leak risk.** Cocktail informalities can let MNPI slip; brief CEO/CFO on Reg FD topic-list before each.
- **Conference appearance recording.** Many sell-side conferences webcast; check Reg FD compliance (broad disclosure if material).
- **Bookrunner debrief candor.** Banks have own incentives; cross-check NDR demand vs other deals running.
- **Hotel + AV failure.** Always have backup AV (own laptop + dongles + adapters); always confirm room day-before.
- **Virtual NDR fatigue.** Zoom 6+ hours/day = degraded signal; cap at 4-5 calls/day.
- **Prospect list staleness.** Prospect list 6+ months old = funds may have shifted; refresh quarterly.
- **Banker pre-positioning bias.** Banks suggest meetings that suit their own narrative; cross-check with own 13F analysis.

> Mandatory disclaimer: Roadshow 1:1 meetings are subject to Regulation FD (selective MNPI disclosure prohibited). IPO testing-the-waters meetings are governed by Rule 163B and underwriter supervision. **Consult licensed securities counsel** before any roadshow communication touching MNPI, before any TTW meeting, and for interpretation of Reg FD safe harbors.

## Sources

- BNY Mellon NDR Best Practices: https://www.bnymellon.com/us/en/insights/all-insights/non-deal-roadshow-best-practices.html
- Q Comms NDR Playbook: https://www.qcomms.com/blog/non-deal-roadshow-best-practices
- Notified Virtual NDR: https://www.notified.com/blog/non-deal-roadshow-virtual
- NIRI IPO Resources: https://www.niri.org/professional-development/ipo-resources
- ICR IPO Edge: https://www.icrinc.com/services/ipo-edge/
- Cooley IPO Practice: https://www.cooley.com/services/practice/securities-and-capital-markets/initial-public-offerings
- SEC Rule 163B (TTW): https://www.sec.gov/rules/final/2019/33-10699.pdf
- SEC Regulation FD: https://www.sec.gov/divisions/corpfin/guidance/regfd-interp.htm
- See `role.md` -> "Roadshow NDR playbook"

## Related skills

- `equity-analyst-relations-briefings` — 1:1 cadence overlaps.
- `13f-shareholder-monitoring` — holder list feeds prospect targeting.
- `quiet-period-mgmt` — restricts NDR meetings in earnings run-up.
- `investor-day-capital-markets-day` — annual deep-dive (NDR fills between).
- `quarterly-earnings-press-release` — fresh material for post-earnings NDR.
