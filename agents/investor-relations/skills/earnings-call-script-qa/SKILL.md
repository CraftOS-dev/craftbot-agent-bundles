<!--
Source: https://www.notified.com/products/earnings-calls
Source: https://www.alpha-sense.com/use-cases/ir/
Source: https://www.sentieo.com/
Source: https://www.tegus.co/use-cases/investor-relations
Source: https://www.niri.org/standards-of-practice
Source: https://www.openexchange.tv/earnings-events
Reference role.md: "Earnings call script playbook"
Round 2 enrichment: full T-14 to T-0 cadence + Q&A binder schema + AlphaSense/Sentieo/Tegus mining recipes + tech contingencies + counsel checklist.
-->

# Earnings call script + 50-150 Q&A binder

Builds the public-company earnings call deliverable: script (Safe Harbor + Reg G + CEO open + CFO walkthrough + Q&A flow) + 50-150-question Q&A binder mined from prior peer calls via AlphaSense / Sentieo / Tegus. Hosted on Notified / OpenExchange / Q4. Defers binding Safe Harbor + Reg G language to `legal-counsel`.

## When to use

- Prep for next public-company earnings call (quarterly cadence).
- Building the rolling Q&A library that feeds future calls.
- Mining peer transcripts for question-pattern intelligence.
- Trigger phrases: "earnings call prep", "Q&A binder", "earnings script", "Q&A pack", "earnings prep", "analyst Q prep".

NOT for: earnings press release (use `quarterly-earnings-press-release`); guidance number setting (use `guidance-setting`); private-co cadence (use `monthly-investor-update-visible`); investor day (use `investor-day-capital-markets-day`).

## Setup

```bash
# Analyst research APIs (recipient supplies key — all paywalled)
export ALPHASENSE_API_KEY="<from AlphaSense Admin>"     # $20K+/yr/seat
export SENTIEO_API_KEY="<from Sentieo Admin>"           # $15K+/yr/seat
export TEGUS_API_KEY="<from Tegus Admin>"               # $10K+/yr/seat

# Call infrastructure (recipient picks one)
export NOTIFIED_API_KEY="<from Notified Admin>"         # preferred 2026
export OPENEXCHANGE_API_KEY="<from OpenExchange Admin>"
export Q4_API_KEY="<from Q4 Admin>"

# Fallback for analyst pattern mining (no paid key)
# sec-edgar-mcp transcript fetch + manual pattern extraction
```

Data inputs:
- Last 4 quarters' own transcripts (baseline cadence).
- 4-8 peer transcripts for Q&A pattern mining (Tegus + Sentieo).
- `guidance-setting` output: range / point + rationale.
- `finance-agent`: revenue / EPS / segment / cash / capital allocation.
- `13f-shareholder-monitoring`: any holder shifts that may surface in Q&A.

## T-cadence (run-of-show)

| T- | Activity | Tool |
|----|----------|------|
| T-21 | Pull last 4 own calls + 4 peer calls; categorize questions | AlphaSense / Sentieo |
| T-14 | Consensus pull (FactSet/Refinitiv); guidance frame from `finance-agent` | `guidance-setting` |
| T-10 | Draft script (Safe Harbor + Reg G + CEO 3-5min + CFO 5-7min + Q&A flow) | `docx` |
| T-7  | Assemble 50-150-Q binder per-topic; vetted A + bridge | `docx` + Notion |
| T-5  | Counsel review of script + Safe Harbor / Reg G language | `legal-counsel` hand-off |
| T-3  | Rehearsal #1 with CEO + CFO + IR (full mock Q&A) | calendar |
| T-2  | Rehearsal #2 — tough-Q drill; CFO mock-bombs | calendar |
| T-1  | Final script lock; deck lock; tech-check Notified webcast | Notified API |
| T-0  | Run the call; capture new Qs for library back-fill | Notified call recorder |
| T+1  | Transcript review; new Q ingestion into `shareholder-qa-maintenance` | AlphaSense |

## Q&A binder per-Q schema

```
QUESTION: <verbatim or paraphrased>
TOPIC: Guidance | Revenue | Margin | Capital Allocation | M&A | Competitive | ESG | Governance | Macro | People | Long-term thesis
ANSWER: <50-200 words; vetted by IR + CFO + counsel where binding>
BRIDGE: <1 sentence connecting to long-term thesis>
OWNER: CEO | CFO | IR (for routing if asked live)
AS-OF: <date — auto-expire after 90 days>
SOURCE: <internal model | analyst note | prior call>
CONFIDENCE: HIGH | MEDIUM | LOW
```

## Common recipes

### Recipe 1 — Pull peer transcripts via AlphaSense
```bash
curl -H "Authorization: Bearer $ALPHASENSE_API_KEY" \
  "https://api.alpha-sense.com/v1/search?q=$PEER_TICKERS&doc_type=transcript&limit=20&sort=date_desc"
```
Returns transcript URLs + key-question extraction. Top 20 most recent typically suffices.

### Recipe 2 — Pull Q&A pairs via Sentieo
```bash
curl -H "x-api-key: $SENTIEO_API_KEY" \
  "https://api.sentieo.com/v1/transcripts/qa?tickers=$PEER_TICKERS&period=last_4q"
```
Sentieo's Q&A extraction is more precise than transcript dump; categorizes by speaker.

### Recipe 3 — Pull expert-call insights (Tegus, competitive intel)
```bash
curl -H "Authorization: Bearer $TEGUS_API_KEY" \
  "https://api.tegus.co/v1/transcripts/search?company=$COMPETITOR&topic=$THEME"
```
Use sparingly — expert calls have their own attribution rules.

### Recipe 4 — Question-pattern categorization
```python
import re
TOPICS = {
    "Guidance": [r"guide|guidance|outlook|forecast|FY|fiscal"],
    "Margin":   [r"margin|gross margin|operating margin|EBITDA"],
    "M&A":      [r"acquisition|M&A|deal|integration"],
    "Competitive": [r"competit|vs |against|market share|win rate"],
    "Capital allocation": [r"buyback|dividend|capex|return cash"],
}
def categorize(question_text):
    for topic, patterns in TOPICS.items():
        if any(re.search(p, question_text, re.I) for p in patterns):
            return topic
    return "Other"
```

### Recipe 5 — Script Safe Harbor + Reg G block (counsel-supplied template)
```
Safe Harbor: "Today's call contains forward-looking statements within the meaning
of the Private Securities Litigation Reform Act of 1995..."

Reg G Non-GAAP: "We use certain non-GAAP measures including [adjusted EBITDA / 
free cash flow / etc.]. Reconciliations are in our earnings release filed today
on Form 8-K and posted at [ir.company.com]."
```
**Defer to `legal-counsel`** for binding language each quarter.

### Recipe 6 — Build run-of-show deck (pptx)
```python
# Standard deck: 12-15 slides
# 1. Safe Harbor (always slide 1)
# 2. Reg G reconciliation pointer
# 3. Quarter highlights (3-5 bullets)
# 4-7. Financial summary (revenue / margin / segment / cash)
# 8-9. Strategic updates
# 10-11. Guidance summary
# 12. Q&A intro
```

### Recipe 7 — Schedule Notified webcast
```bash
curl -X POST -H "Authorization: Bearer $NOTIFIED_API_KEY" \
  -d '{"title": "Q2 2026 Earnings Call", "start": "2026-07-30T17:00:00Z", "duration_minutes": 60}' \
  "https://api.notified.com/v1/earnings/events"
```

### Recipe 8 — Pull our last 4 calls for cadence
```bash
mcp call sec-edgar-mcp fetch_form --ticker=$OUR_TICKER --form=8-K --item="2.02" --limit=4
# Earnings-call exhibits filed as 8-K Item 2.02
```

### Recipe 9 — Tough-Q rehearsal seed (red-team)
```
Generate 10 questions designed to make CFO sweat:
- Why did margin compress 200 bps when consensus expected +50 bps?
- What's the path to GAAP profitability and when?
- Why didn't you raise FY guidance after a beat?
- Walk us through the 8-K disclosed exec departure
- Are you seeing demand softness mid-quarter?
- ...
```

### Recipe 10 — Post-call transcript ingestion
```bash
# Pull our just-run call transcript T+24 hours
curl -H "Authorization: Bearer $ALPHASENSE_API_KEY" \
  "https://api.alpha-sense.com/v1/transcripts?ticker=$OUR_TICKER&latest=true"
# Extract new Qs not in library; route to shareholder-qa-maintenance for backfill
```

## Examples

### Example 1: Full Q2 prep cycle (mid-cap public co, $2B revenue)

**Goal:** Q2 2026 call on Jul 30; 8 sell-side analysts cover; 23 institutional holders >1%.

**Steps:**
1. T-21: Pull 4 own + 6 peer transcripts (Recipe 1 + 2); categorize (Recipe 4).
2. T-14: Get consensus (FactSet via `guidance-setting`); review beat/miss/raise scenarios with CFO.
3. T-10: Draft script (Recipe 5 + 6); 8 slides.
4. T-7: Build 120-question binder; topic-categorized; CFO + IR review each A.
5. T-5: Counsel review (Safe Harbor + Reg G language).
6. T-3: Rehearsal #1 — full mock; CFO + CEO + IR + counsel.
7. T-2: Tough-Q drill (Recipe 9); identify 5 weakest A's; rewrite.
8. T-1: Tech check on Notified; final lock.
9. T-0: Run call (Recipe 7); IR captures live Qs not in binder.
10. T+1: Pull transcript (Recipe 10); new Qs into `shareholder-qa-maintenance` library.

**Result:** No analyst surprises; CEO/CFO speak from binder; 4 new Qs captured for library; analyst notes cite "well-prepared management" within 48 hours.

### Example 2: Bridge question on margin compression

**Goal:** Anticipate the obvious Q: "Why did gross margin compress 200 bps?"

**Steps:**
1. Pull binder entry: TOPIC=Margin, QUESTION="What drove margin compression Q2?"
2. ANSWER (vetted): "Two factors. First, mix shift to enterprise — enterprise gross margin is 6 points below SMB but customer lifetime value is 4x. Second, infra investment in our new region (Frankfurt) is front-loaded, will normalize over 3 quarters."
3. BRIDGE: "Long-term we expect gross margin to recover to 78%+ as Frankfurt amortizes."
4. OWNER: CFO.
5. CONFIDENCE: HIGH (CFO + finance team data-vetted).

**Result:** CFO answers crisply; analysts model the bridge correctly in next-day notes.

## Edge cases / gotchas

- **Reg FD violation risk in Q&A.** Never share material non-public info NOT in the prepared remarks. If a Q goes there, deflect: "We'll address that in our next 8-K / quarter."
- **Safe Harbor coverage gaps.** Counsel must review every Q&A entry that touches forward-looking statements; ensure the Safe Harbor statement at the top of the call covers it.
- **Reg G non-GAAP reconciliation.** Every non-GAAP measure cited live must have reconciliation in the press release (8-K) — if not, that's a Reg G violation.
- **Transcript ingestion lag.** AlphaSense / Sentieo / Bloomberg post own-call transcripts T+4 hours; competitor calls T+24-48 hours.
- **AlphaSense / Sentieo / Tegus paywall.** $20K+/yr each. Free fallback: `sec-edgar-mcp` for 8-K Item 2.02 transcripts (lower quality, no Q&A extraction).
- **Notified webcast tech issues.** Always have a backup dial-in (OpenExchange or Zoom Webinar); pre-stage the deck on both.
- **Tegus expert calls have attribution restrictions.** Cannot quote a Tegus expert call publicly without permission.
- **Mock-Q overconfidence.** Always have one Q in rehearsal that CFO can't answer cleanly — exposes the gap before live.
- **Live Q not in binder.** IR should signal CFO via Slack channel mid-call; CFO bridges: "We'll come back to that with detail."
- **Embargo on transcript publish.** Our own transcript should be posted on IR website within 24 hours (Q4 Inc. handles); delayed = analysts complain.

> Mandatory disclaimer: This skill drafts earnings call deliverables for public companies. **Consult licensed securities counsel** for binding Safe Harbor and Regulation G language each quarter, and for any Q&A entry touching forward-looking statements, material non-public information, or Regulation FD interpretation.

## Sources

- Notified Earnings Calls: https://www.notified.com/products/earnings-calls
- OpenExchange Earnings Events: https://www.openexchange.tv/earnings-events
- AlphaSense IR Use Case: https://www.alpha-sense.com/use-cases/ir/
- Sentieo: https://www.sentieo.com/
- Tegus IR Use Case: https://www.tegus.co/use-cases/investor-relations
- NIRI Standards of Practice: https://www.niri.org/standards-of-practice
- SEC Regulation FD Interpretations: https://www.sec.gov/divisions/corpfin/guidance/regfd-interp.htm
- SEC Regulation G: https://www.sec.gov/rules/final/33-8176.htm
- See `role.md` -> "Earnings call script playbook"

## Related skills

- `guidance-setting` — feeds the guidance section.
- `quarterly-earnings-press-release` — paired companion (8-K Item 2.02).
- `shareholder-qa-maintenance` — back-fills library from post-call transcript.
- `quiet-period-mgmt` — restricts comms in run-up window.
- `equity-analyst-relations-briefings` — analyst cadence around call.
