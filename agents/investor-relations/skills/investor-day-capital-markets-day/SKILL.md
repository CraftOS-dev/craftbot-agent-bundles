<!--
Source: https://www.notified.com/products/investor-day
Source: https://www.q4inc.com/blog/capital-markets-day-best-practices
Source: https://icrinc.com/services/investor-relations/
Source: https://www.fticonsulting.com/services/strategic-communications/investor-relations
Source: https://www.joelefrank.com/services/
Reference role.md: "Investor day playbook"
Round 2 enrichment: T-90 to T-0 cadence + agenda template + deck structure + virtual stream coord + senior advisor (ICR/FTI/JF) engagement.
-->

# Investor day / capital markets day

Plans and runs the annual or biennial investor day / capital markets day — CEO + strategy + segment deep-dives + CFO long-range model + Q&A panel + executive roundtables. Notified / Q4 host the hybrid event + virtual stream. ICR Inc. / FTI Consulting / Joele Frank are the senior advisors.

## When to use

- Annual or biennial investor day / capital markets day planning.
- Long-range (3-year) framework reset (paired with `guidance-setting`).
- Major strategic pivot communication (rebranding, new segment launch, M&A integration).
- AGM virtual + hybrid coordination.
- Trigger phrases: "investor day", "capital markets day", "CMD", "analyst day", "long-range plan day", "AGM virtual".

NOT for: quarterly earnings call (use `earnings-call-script-qa`); roadshow / NDR (use `roadshow-ndr-logistics`); 10-K Item 1 Business narrative (use `10k-10q-drafting-workiva`); M&A announcement event (use `ma-investor-comms`).

## Setup

```bash
# Notified Investor Day (preferred 2026)
export NOTIFIED_API_KEY="<from Notified Admin>"          # $15K-$50K+ per event

# Q4 Inc. (alt; bundled with IR website)
export Q4_API_KEY="<from Q4 Admin>"

# Senior advisors (engagement-based; $200K-$1M+ per event)
# ICR Inc. — IPO Edge playbook
# FTI Consulting — broad IR + M&A
# Joele Frank — M&A + activist defense

# Tools: pptx (deck); playwright-mcp (registration QA); figma-mcp (deck design)
```

Auth / API key requirements:
- `NOTIFIED_API_KEY` — per-event $15K-$50K hybrid event package.
- `Q4_API_KEY` — bundled with Q4 IR website subscription.
- Senior advisors — relationship-based engagement; one of ICR / FTI / JF / Brunswick.
- Free fallback: Zoom Webinar + Q4/Notified IR-website registration page (lower production value).

Data inputs:
- 3-year long-range model (`finance-agent`'s output).
- Strategic narrative (CEO-voice; coordinated with `ceo-agent`).
- Segment business plans (each GM/segment president).
- ESG framework update (coordinated with `esg-investor-reporting-gri-sasb-tcfd`).
- 13F holder list (`13f-shareholder-monitoring`) + analyst coverage matrix.
- Prior investor day attendee list (for re-invitation).

## Cadence (T-90 to T-0)

| T- | Activity | Owner | Output |
|----|----------|-------|--------|
| T-180 | Concept + date + theme + senior advisor engagement | IR + CEO + CFO + advisor | Theme + draft agenda |
| T-120 | Venue + virtual stream platform locked | IR + ops | Notified/Q4 event setup |
| T-90 | Save-the-date to attendee list | IR | Email blast |
| T-75 | Agenda finalized + speakers locked | IR + CEO + CFO | Agenda + speaker order |
| T-60 | Deck outlines per speaker drafted | IR + each speaker | Deck outlines |
| T-45 | Long-range model 1-pager + ESG fact-pack | finance + ESG | 1-pagers |
| T-30 | Master deck v1; rehearsal #1 | IR + speakers | Deck v1 + redlines |
| T-21 | Press release draft (pre-event) | IR | Draft release |
| T-14 | Rehearsal #2 + Q&A drill | IR + CEO + CFO | Q&A binder |
| T-7 | Registration close + briefing books per attendee | IR | Per-attendee books |
| T-3 | Tech rehearsal (AV + stream) | IR + Notified | Tech check |
| T-1 | Master deck freeze | IR | Locked deck |
| T-0 | Run the day + capture Q&A | IR + execs | Live event |
| T+1 | Post-event press release + analyst digest | IR | Post release + digest |
| T+7 | Post-event analyst 1:1s + thank-you notes | IR | Follow-ups |

## Standard agenda (8 AM - 5 PM full day)

```
8:00  Continental breakfast + networking
9:00  CEO state of the company (30 min)
9:30  Strategy + 3-year vision (45 min — CEO + Chief Strategy)
10:15 Break
10:30 Segment 1 deep-dive (45 min — Segment GM)
11:15 Segment 2 deep-dive (45 min — Segment GM)
12:00 Lunch + investor-only mingle (60 min)
1:00  Segment 3 deep-dive (45 min — Segment GM)
1:45  Technology + platform (45 min — CTO)
2:30  Break
2:45  CFO long-range model + capital allocation (45 min — CFO)
3:30  Q&A panel (60 min — CEO + CFO + 2 segment GMs)
4:30  Executive roundtables (90 min — small-group breakouts)
5:00  Cocktail reception (90 min)
```

## Materials

- **Master deck** (40-60 slides; per-segment subs).
- **Briefing books** per institutional attendee (1-pager: fund + holdings + recent published views).
- **Long-range model 1-pager** (key drivers, multi-year framework, capital allocation framework).
- **ESG fact-pack** (1-pager).
- **Press release** pre-event (save-the-date) + post-event (key takeaways).
- **Q&A binder** (50-100 anticipated Qs; paired with `shareholder-qa-maintenance`).

## Common recipes

### Recipe 1 — Notified investor-day event creation
```bash
curl -X POST -H "Authorization: Bearer $NOTIFIED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "investor_day",
    "title": "ACME Investor Day 2026",
    "date": "2026-11-12",
    "format": "hybrid",
    "venue": "NYC HQ + Notified webcast",
    "registration_url": "...",
    "stream_url": "..."
  }' \
  "https://api.notified.com/v1/events"
```

### Recipe 2 — Registration page QA (playwright-mcp)
```bash
mcp call playwright-mcp run \
  --url "https://event.notified.com/acme-investor-day-2026" \
  --check "registration_form,calendar_invite,stream_dry_run"
```

### Recipe 3 — Per-attendee briefing book (1-pager)
```python
# For each registered institutional attendee
def briefing_book(attendee):
    return {
        "fund_name": attendee.fund,
        "aum": attendee.aum,
        "current_position": attendee.shares,
        "delta_from_prior_q": attendee.delta,
        "recent_published_views": attendee.notes,
        "topics_of_interest": attendee.topics,
        "prior_meeting_summary": attendee.last_meeting_notes,
    }
```

### Recipe 4 — Deck design coordination (figma-mcp)
```bash
mcp call figma-mcp get_node --file_key=$FILE_KEY --node_id=$NODE_ID
# Designers + IR + speakers iterate; export to pptx for final
```

### Recipe 5 — Long-range model 1-pager
```python
# Coordinate with finance-agent
LONG_RANGE = {
    "horizon": "FY26-FY29",
    "revenue_cagr": "20-25%",
    "gross_margin_target": "78%+",
    "operating_margin_target": "30%+",
    "fcf_conversion_target": "85%+",
    "capital_allocation": "60% reinvest / 30% buyback / 10% M&A",
    "key_assumptions": ["pricing", "ARR retention", "S&M efficiency"],
}
```

### Recipe 6 — Q&A binder build (paired with shareholder-qa-maintenance)
```python
# Pull top 50-100 entries by topic from shareholder Q&A library
# Anticipate long-range Qs:
# - "Bridge from current to FY29 revenue?"
# - "When do you expect operating margin to inflect to 30%+?"
# - "Capital allocation: why 30% buyback vs more M&A?"
# Each Q: vetted A + bridge to long-range framework
```

### Recipe 7 — Pre-event press release
```python
PRE_EVENT_RELEASE = """
{Company} to Host Investor Day on {Date} Outlining Three-Year Strategic Plan

{HQ City}, {Date} — {Company} (NASDAQ: TICKER) today announced it will host
an Investor Day on {Date} at {Venue} from {Time} ET. The event will include
presentations from CEO Name, CFO Name, and segment leadership, covering the
company's three-year strategic plan, long-range financial framework, and
capital allocation strategy.

Live webcast and registration at ir.company.com/investor-day-2026.
"""
```

### Recipe 8 — Post-event press release
```python
POST_EVENT_RELEASE = """
{Company} Outlines Three-Year Strategic Plan at 2026 Investor Day

KEY TAKEAWAYS:
- Long-range revenue growth target of {X}% CAGR through {YEAR}
- Operating margin expansion to {Y}% by {YEAR}
- Capital allocation framework: {X}% reinvest, {Y}% return, {Z}% M&A
- Long-range cumulative FCF target: ${X}B

Replay available at ir.company.com/investor-day-2026.
"""
```

### Recipe 9 — Tech rehearsal checklist
```
- AV check (microphones, speaker order, slide advance)
- Stream check (Notified video quality, audio sync, captions)
- Registration page open + functional
- Q&A submission flow (live + virtual)
- Stage timer + backstage runner
- Backup mic + laptop + dongles
- Wi-Fi capacity for in-person + speakers
```

### Recipe 10 — Post-event analyst digest
```python
# T+1: send analyst digest summarizing event + key takeaways + replay link
# Paired with `equity-analyst-relations-briefings` for 1:1 follow-ups
```

### Recipe 11 — Senior advisor engagement scope
```python
ADVISOR_SCOPES = {
    "ICR_IR_Edge": "IR-side IPO + first investor day (mid-cap)",
    "FTI_Strategic": "Mid-to-large cap; M&A overlap",
    "Joele_Frank": "Activist defense overlap; high-stakes events",
    "Brunswick": "Cross-border + media-heavy events",
}
```

## Examples

### Example 1: Annual investor day (mid-cap)

**Goal:** Nov 12, 2026 investor day; 200 in-person + 1,500 virtual; ICR Inc. advisor.

**Steps:**
1. T-180: Concept locked (theme: "Platform Inflection"); ICR engagement.
2. T-120: NYC HQ booked; Notified hybrid event setup (Recipe 1).
3. T-90: Save-the-date to 600 institutional contacts.
4. T-75: Agenda + 6 speakers locked.
5. T-60: Deck outlines drafted.
6. T-45: Long-range model 1-pager (Recipe 5); ESG fact-pack.
7. T-30: Master deck v1 + rehearsal #1.
8. T-21: Pre-event release (Recipe 7).
9. T-14: Rehearsal #2 + Q&A binder (Recipe 6).
10. T-7: Briefing books per attendee (Recipe 3).
11. T-3: Tech rehearsal (Recipe 9).
12. T-0: Run the day; 280 in-person + 1,820 virtual.
13. T+1: Post-event release (Recipe 8); analyst digest (Recipe 10).
14. T+7: Follow-up 1:1s with key attendees.

**Result:** 3 analyst PT raises within 30 days; sets thematic frame for next 4-6 quarters.

### Example 2: Virtual-only AGM with mini investor day

**Goal:** AGM virtual May 15, 2027; 90-min event with strategic update.

**Steps:**
1. Broadridge meeting ID + Notified virtual stream.
2. Mini-agenda: 5-min CEO update + 30-min Q&A + AGM business (votes).
3. Briefing books lighter (1-pager).
4. Tech rehearsal critical (Notified virtual platform).
5. Run; post-event press release + 8-K Item 5.07 AGM results.

**Result:** Hybrid AGM compliant + investor-engaging; lower production cost than full investor day.

### Example 3: Capital markets day post-M&A integration

**Goal:** 6 months post major M&A close; need to reset long-range framework.

**Steps:**
1. Coordinate with `ma-investor-comms` (deal narrative) and `finance-agent` (synergy realization).
2. Theme: "ACME + Beta: One Year In, Five Years Forward".
3. Agenda emphasizes integration milestones + synergy capture vs original plan + revised long-range model.
4. Joint segment leadership (some legacy + some acquired).
5. Q&A panel includes integration ML + synergy realization Qs.
6. Senior advisor: FTI Strategic Comms.

**Result:** Investor confidence in integration; long-range framework reset cleanly.

## Edge cases / gotchas

- **Long-range framework slippage punishes more than quarterly miss.** Don't issue a framework you can't hit; build conservative.
- **Senior advisor fee creep.** ICR/FTI/JF engagements $200K-$1M+; scope carefully.
- **Tech rehearsal critical.** Notified/Q4 events have stream-failure history 1-2 events/yr.
- **In-person attendance forecasting.** Mid-cap investor day RSVP rate 60-75%; over-invite by 40%.
- **Virtual stream Reg FD compliance.** If new material info shared, must be simultaneous + broad — investor day qualifies but timing matters.
- **Activist disruption risk.** Senior advisor recommends security + counsel + Q&A moderation.
- **Q&A live mic discipline.** Operator-moderated Q&A only; no open-floor (Reg FD risk).
- **Deck leakage pre-event.** Master deck embargo until event start; counsel-supervised.
- **Foreign-investor multilingual.** Live translation for top 1-2 languages if material non-English audience.
- **AGM voting integration.** Broadridge meeting ID for proxy-voting integration with Notified/Q4 module.
- **Post-event 8-K Item 7.01.** Some companies file Item 7.01 with materials; counsel decides.
- **Backup speaker.** Always have backup speaker for each segment (illness, travel).
- **Catering + dietary.** Trivial but critical for investor experience; over-cater.
- **Recording + replay rights.** Notified/Q4 give 12-month replay; longer = extra cost.

> Mandatory disclaimer: Investor day events that share material non-public information must be simultaneously broadly disseminated for Reg FD compliance. Long-range financial frameworks are forward-looking statements subject to Safe Harbor. **Consult licensed securities counsel** before any new MNPI shared on the day, before pre-event materials distribution, and for Safe Harbor coverage on long-range framework.

## Sources

- Notified Investor Day: https://www.notified.com/products/investor-day
- Q4 Capital Markets Day Best Practices: https://www.q4inc.com/blog/capital-markets-day-best-practices
- ICR Inc. Investor Relations: https://icrinc.com/services/investor-relations/
- FTI Strategic Comms IR: https://www.fticonsulting.com/services/strategic-communications/investor-relations
- Joele Frank Services: https://www.joelefrank.com/services/
- Brunswick Group: https://www.brunswickgroup.com/
- Broadridge Virtual AGM: https://www.broadridge.com/solution/virtual-annual-meetings
- See `role.md` -> "Investor day playbook"

## Related skills

- `guidance-setting` — long-range framework anchors.
- `ir-website-q4-notified` — event posting + registration.
- `equity-analyst-relations-briefings` — analyst pre-event + post-event 1:1s.
- `shareholder-qa-maintenance` — Q&A binder build.
- `quarterly-board-letter` — pre-event narrative continuity.
- `ma-investor-comms` — when day follows M&A close.
