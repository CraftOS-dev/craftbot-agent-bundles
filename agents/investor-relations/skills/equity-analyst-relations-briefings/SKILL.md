<!--
Source: https://www.alpha-sense.com/use-cases/ir/
Source: https://www.sentieo.com/
Source: https://www.tegus.co/use-cases/investor-relations
Source: https://www.bloomberg.com/professional/product/investor-relations/
Source: https://www.meltwater.com/en/products/ir-monitoring
Source: https://mention.com/en/
Source: https://www.brandwatch.com/p/social-listening/
Source: https://www.talkwalker.com/
Reference role.md: "Analyst relations playbook"
Round 2 enrichment: coverage matrix Notion schema + per-stance briefing scripts + media monitoring dashboard recipe + post-earnings call-back roster automation.
-->

# Equity analyst relations + news/media monitoring (IR lens)

Maintains the equity analyst coverage matrix (bull/neutral/bear x influence x coverage start), runs 1-2x/Q 1:1 briefings, mines new analyst notes via AlphaSense / Sentieo / Tegus / Bloomberg, runs post-earnings call-back roster within 48 hours, and monitors news + media (Mention / Brandwatch / Talkwalker / Meltwater / Cision) for IR-relevant signals. Reg FD-bounded: no MNPI shared selectively.

## When to use

- Maintaining the analyst coverage matrix + 1:1 cadence.
- Post-earnings 48-hour call-back roster.
- Daily/weekly analyst-note alert triage for CEO/CFO.
- News + media monitoring (analyst upgrade/downgrade, activist Schedule 13D/G, class actions, ESG controversies, regulatory developments).
- New analyst initiation outreach.
- Trigger phrases: "analyst CRM", "brief analysts", "analyst meeting", "analyst note alert", "news monitoring IR", "media monitoring", "post-earnings call-back".

NOT for: shareholder Q&A library (use `shareholder-qa-maintenance`); 13F holder tracking (use `13f-shareholder-monitoring`); roadshow scheduling (use `roadshow-ndr-logistics`); embargoed disclosure (use `embargoed-disclosure-protocols`).

## Setup

```bash
# Analyst research (paywalled)
export ALPHASENSE_API_KEY="<from AlphaSense Admin>"      # $20K+/yr/seat
export SENTIEO_API_KEY="<from Sentieo Admin>"            # $15K+/yr
export TEGUS_API_KEY="<from Tegus Admin>"                # $10K+/yr
export BLOOMBERG_API_KEY="<from BBG BPIPE Terminal>"     # $24K+/yr

# News + media monitoring
export MENTION_API_KEY="<from Mention Admin>"            # $40-$500/mo
export MELTWATER_API_KEY="<from Meltwater Admin>"        # $6K+/yr
export TALKWALKER_API_KEY="<from Talkwalker Admin>"      # $9K+/yr
export CISION_API_KEY="<from Cision Admin>"              # $10K+/yr
export BRANDWATCH_API_KEY="<from Brandwatch Admin>"      # $1K+/mo

# Free fallback: Google Alerts RSS + Reddit/Twitter MCPs + sec-edgar-mcp
```

Auth / API key requirements:
- One of AlphaSense / Sentieo / Bloomberg for analyst notes (recipient picks).
- One of Mention / Meltwater / Talkwalker / Cision for media (recipient picks).
- Free fallback works for low-volume issuer.

Data inputs:
- Sell-side coverage list (from Bloomberg ANR or Refinitiv).
- Recent analyst notes (last 90 days; baseline sentiment).
- Estimates consensus (FactSet / Refinitiv).
- Earnings transcript (own + peers) for Q-author identification.

## Coverage matrix (Notion DB schema)

```
Analyst Name | Firm | Coverage Start | Stance: BULL/NEUTRAL/BEAR
  | Influence: 1-5 | Last 1:1 Date | Next 1:1 Due
  | Last PT | Last Rating | Last Note Date | Last Note URL
  | Topics of interest (multi-select) | Prior Qs (last 4 calls)
  | Personal notes (kid's school, golf, etc.)
  | Owner: CEO / CFO / IR
  | Cadence: monthly / quarterly / ad hoc
```

Influence weighting: top 3-5 analysts by AUM-following + commentary frequency get monthly cadence; tier-2 quarterly; tier-3 ad hoc.

## Workflow (daily / weekly / quarterly)

| Cadence | Activity | Tool |
|---------|----------|------|
| Daily | AlphaSense / Sentieo alert digest; flag downgrade/PT change to CEO/CFO | Recipe 1 |
| Daily | Media monitoring digest (Meltwater / Mention) | Recipe 6 |
| Weekly | Activist scan (Schedule 13D/G) + class action filings | Recipe 7 |
| Post-earnings (T+24-48h) | 1:1 with each lead analyst who asked a Q | Recipe 4 |
| Quarterly | Refresh coverage matrix; schedule tiered 1:1 cadence | Notion |
| Quarterly | Sentiment baseline trend (FinBERT on aggregated notes) | Recipe 5 |

## Common recipes

### Recipe 1 — AlphaSense daily alert
```bash
curl -H "Authorization: Bearer $ALPHASENSE_API_KEY" \
  "https://api.alpha-sense.com/v1/alerts?ticker=$TICKER&days=1"
# Returns: new analyst notes, transcript mentions, news matching saved filters
```

### Recipe 2 — Sentieo Q&A pattern lookup
```bash
curl -H "x-api-key: $SENTIEO_API_KEY" \
  "https://api.sentieo.com/v1/transcripts/qa?tickers=$TICKER&author=$ANALYST_NAME"
# Pulls every Q this analyst asked us in last 8 calls; prep for 1:1
```

### Recipe 3 — Bloomberg ANR coverage list
```python
# via blpapi
import blpapi
session = blpapi.Session()
session.start()
session.openService("//blp/refdata")
service = session.getService("//blp/refdata")
request = service.createRequest("ReferenceDataRequest")
request.append("securities", "ACME US Equity")
request.append("fields", "EQY_REC_NUM_OF_ANALYSTS")
request.append("fields", "ANR_TGT_PRICE")
# ... iterate analyst list
```

### Recipe 4 — Post-earnings call-back roster
```python
# T+24h: pull list of analysts who asked a Q on the call
# Schedule 30-min call-back; only re-cover prepared remarks (NO new MNPI)
CALL_BACK_AGENDA = """
1. Acknowledge their question on the call (5 min)
2. Walk through any specifically referenced model line item (10 min)
3. Their open Qs not addressed live (10 min)
4. Their forward modeling concerns (5 min)
NEVER: share any forward number not in the prepared remarks
NEVER: confirm/deny specific Q+1 trend not yet disclosed
"""
```

### Recipe 5 — Sentiment baseline trend (FinBERT)
```bash
mcp call huggingface-mcp inference \
  --model "yiyanghkust/finbert-tone" \
  --inputs "$(cat last_quarter_notes.txt)"
# Compute rolling 4-Q sentiment; chart trend; flag when avg shifts >1 stdev
```

### Recipe 6 — Meltwater IR media monitoring
```bash
curl -H "Authorization: Bearer $MELTWATER_API_KEY" \
  "https://api.meltwater.com/v3/search?keyword=$COMPANY+$TICKER&days=7"
# Filter: news_only=true OR include_social=true depending on need
```

### Recipe 7 — Activist scan (Schedule 13D/G)
```bash
mcp call sec-edgar-mcp fetch_form --ticker=$TICKER --form="SC+13D" --days=30
mcp call sec-edgar-mcp fetch_form --ticker=$TICKER --form="SC+13G" --days=30
# 13D = activist (>5% with intent); 13G = passive (>5% no activist intent)
```

### Recipe 8 — Tegus competitor expert call mining
```bash
curl -H "Authorization: Bearer $TEGUS_API_KEY" \
  "https://api.tegus.co/v1/transcripts/search?company=$COMPETITOR"
# Use for competitive intel ahead of conference appearances
# Attribution restrictions apply — cannot quote publicly
```

### Recipe 9 — 1:1 briefing-book per analyst (assemble)
```python
def briefing_book(analyst):
    return {
        "bio": analyst.bio,
        "stance": analyst.stance,
        "last_note": analyst.last_note_excerpt,
        "last_pt": analyst.last_pt,
        "prior_qs": analyst.last_4_call_questions,
        "model_gap_vs_consensus": "where their published model differs from consensus",
        "topics_of_interest": analyst.topics,
        "talking_points_PREPARED_REMARKS_ONLY": [
            # NEVER: forward-looking MNPI
            # ALWAYS: prepared remarks + Reg G reconciliations + Safe Harbor framing
        ],
    }
```

### Recipe 10 — Schedule via google-calendar-mcp
```bash
mcp call google-calendar-mcp create_event \
  --summary "Analyst 1:1 — $ANALYST_NAME ($FIRM)" \
  --start "2026-07-15T14:00:00Z" --duration 30 \
  --attendees "$ANALYST_EMAIL,ceo@company.com,ir@company.com"
```

### Recipe 11 — New analyst initiation welcome
```python
WELCOME_KIT = [
    "Latest 10-K + 10-Q (with bookmarks)",
    "Last 4 earnings transcripts",
    "Investor day deck (last cycle)",
    "Capital allocation philosophy 1-pager",
    "Long-range model assumptions overview",
    "30-min intro 1:1 with CFO",
]
# Send within 7 days of initiation announcement
```

## Examples

### Example 1: Post-earnings 48-hour call-back

**Goal:** Q2 call July 30; T+48h call-backs scheduled with 6 sell-side analysts who asked Qs.

**Steps:**
1. T+1h post-call: assemble Q-author list from transcript.
2. T+4h: IR emails each analyst, offering 30-min call-back.
3. T+24h: 6 of 8 confirm; schedule Jul 31 - Aug 1 (Recipe 10).
4. For each: pull recent note + on-call Q (Recipes 1 + 2); assemble briefing book (Recipe 9).
5. Call-backs run; CFO + IR on each.
6. T+72h: send each analyst Reg G reconciliation links + transcript link (no MNPI).
7. Update coverage matrix with sentiment shifts.

**Result:** All 6 analyst notes published within 5 days; PT changes positive 4 of 6.

### Example 2: Activist 13D flag

**Goal:** Schedule 13D filed by Activist Fund showing 5.4% stake; activist intent.

**Steps:**
1. SEC EDGAR alert triggers (Recipe 7).
2. IR escalates to CEO + CFO + counsel + board chair within 1 hour.
3. Pull activist's stated intent from 13D (governance, capital allocation, strategy).
4. Pull activist's track record (prior 13Ds; outcomes).
5. **Defer** to specialist counsel + activist-defense firm (Joele Frank / Sard Verbinnen).
6. Coverage matrix updated; analysts likely to ask about activist stance.
7. Prep talking points for next analyst 1:1s ("we engage constructively with all shareholders" — counsel-supplied).

**Result:** Activist engagement playbook activated; controlled comms; analyst preparedness.

### Example 3: Sentiment shift detected

**Goal:** Quarterly sentiment baseline shows 1.4 stdev decline last 90 days.

**Steps:**
1. FinBERT trend (Recipe 5) flags decline.
2. Drill: which notes drove the shift? (5 of 14 analysts turned bearish).
3. Identify common bear theme (e.g., margin pressure, competitive).
4. Brief CEO + CFO before next earnings call.
5. Prep targeted Q&A entry in `shareholder-qa-maintenance` for the bear theme.
6. Consider proactive 1:1 with the 5 bears within 30 days (no MNPI; clarify model assumptions).

**Result:** Earnings call addresses the theme proactively; 3 of 5 bears reverse within 1-2 Qs.

## Edge cases / gotchas

- **Reg FD trap in 1:1s.** Selective MNPI = violation. Stick to prepared remarks + published filings + Reg G reconciliations only.
- **Tegus expert-call quotes have attribution restrictions.** Cannot republish publicly.
- **AlphaSense / Sentieo / Bloomberg paywall.** Each $15-$25K/yr. Free fallback: Google Alerts + Yahoo Finance + sec-edgar-mcp for own filings.
- **Bloomberg ANR list lag.** ANR coverage list updates 1-2 days after new initiation.
- **Sentiment models miss nuance.** FinBERT misclassifies hedge language; manual review of flagged notes essential.
- **Call-back roster Reg FD risk.** Treating 5 analysts to 1:1 deep-dive while 30 others get nothing creates Reg FD risk; offer to all analysts equally OR limit to published-question authors.
- **Media monitoring noise.** Twitter/Reddit sentiment for public co can be wildly volatile; weight by author follower count + verified status.
- **Activist 13D escalation.** Schedule 13D is binary signal; never DIY response; immediately escalate to specialist.
- **Conference appearance pre-brief.** Tegus expert calls 1-2 days pre-conference for competitive intel; due diligence on what competitors are saying about you.
- **Coverage matrix decay.** Stances ossify; refresh quarterly minimum (note: an analyst who's been BULL for 8 quarters may not still be).
- **Sell-side personnel turnover.** Analyst moves firm 1-2x in career; coverage matrix needs ownership-transfer protocol.
- **Pre-call analyst hint.** Don't tip analysts what guidance bracket on pre-call 1:1s; full Reg FD violation risk.

> Mandatory disclaimer: All analyst engagement is subject to Regulation FD (selective disclosure of material non-public information is prohibited). **Consult licensed securities counsel** before any 1:1 that risks touching MNPI, before any informational session with subset of analysts, and for interpretation of Reg FD safe harbors. This skill drafts briefings and outreach; counsel approves any communication touching MNPI.

## Sources

- AlphaSense IR Use Case: https://www.alpha-sense.com/use-cases/ir/
- Sentieo: https://www.sentieo.com/
- Tegus IR Use Case: https://www.tegus.co/use-cases/investor-relations
- Bloomberg Terminal IR: https://www.bloomberg.com/professional/product/investor-relations/
- Meltwater IR Monitoring: https://www.meltwater.com/en/products/ir-monitoring
- Mention: https://mention.com/en/
- Brandwatch Social Listening: https://www.brandwatch.com/p/social-listening/
- Talkwalker: https://www.talkwalker.com/
- Cision: https://www.cision.com/
- SEC Regulation FD: https://www.sec.gov/divisions/corpfin/guidance/regfd-interp.htm
- See `role.md` -> "Analyst relations playbook"

## Related skills

- `shareholder-qa-maintenance` — library back-fills from analyst Qs.
- `13f-shareholder-monitoring` — institutional holders side.
- `earnings-call-script-qa` — call prep coordinates with analyst expectations.
- `roadshow-ndr-logistics` — NDR scheduling overlaps with 1:1 cadence.
- `quiet-period-mgmt` — restricts analyst comms in run-up window.
