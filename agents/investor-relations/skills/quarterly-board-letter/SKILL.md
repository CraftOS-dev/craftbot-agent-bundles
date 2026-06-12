<!--
Source: https://visible.vc/blog/quarterly-investor-update/
Source: https://www.kruzeconsulting.com/blog/board-meetings-startup/
Source: https://www.berkshirehathaway.com/letters/letters.html
Source: https://www.aboutamazon.com/news/company-news/2022-letter-to-shareholders
Source: https://www.jpmorganchase.com/ir/annual-report
Reference role.md: "Quarterly board + investor letter playbook" + "Annual shareholder letter playbook"
Round 2 enrichment: structure, Buffett/Bezos/Dimon bar comparison, board-pre vs investor-post variants, sanitization checklist.
-->

# Quarterly board + annual shareholder letter

Drafts the quarterly board letter (institutional cadence — denser than monthly, lighter than 10-Q) AND the annual shareholder letter (Buffett/Bezos/Dimon as the bar). Same scaffold serves both: board pre-meeting AND investor post-meeting versions (sanitized).

## When to use

- Drafting the quarterly board pre-read letter (private or public; 2-4 weeks before board meeting).
- Drafting the investor-facing quarterly letter (post-board, sanitized).
- Drafting the annual shareholder letter accompanying the 10-K (public) or year-end pack (private).
- Trigger phrases: "quarterly letter", "board letter", "annual letter", "shareholder letter", "CEO letter", "year in review".

NOT for: monthly cadence (use `monthly-investor-update-visible`); earnings press release (use `quarterly-earnings-press-release`); 10-K narrative drafting (use `10k-10q-drafting-workiva`); LP letter (use `fund-of-funds-lp-reporting`).

## Setup

```bash
# Visible.vc / Capboard / Sturppy for quarterly distribution
export VISIBLE_API_KEY="<from Visible Settings -> API>"
export CAPBOARD_API_KEY="<from Capboard Admin>"

# Q4 / Notified for public-co annual posting
export Q4_API_KEY="<from Q4 Admin -> Developer>"
export NOTIFIED_API_KEY="<from Notified Settings -> API>"

# Tools: docx (long-form), pdf (hosting), gmail-mcp (distribution), writing-skills (tone)
```

Auth / API key requirements:
- `VISIBLE_API_KEY` — Visible Standard $79/mo+ unlocks REST.
- `CAPBOARD_API_KEY` — Capboard's quarterly variant for board portal.
- `Q4_API_KEY` — Q4 Inc. ($20-100K/yr) for public-co IR website posting.
- `NOTIFIED_API_KEY` — Notified for public-co alt.

Data inputs:
- Prior 3 quarterly letters for tone-continuity baseline.
- `finance-agent`: revenue / ARR / gross margin / burn multiple / runway / segment splits.
- OKR tracker (Notion / Lattice / Ally.io): named OKRs vs progress.
- People tracker: hires (senior/named), departures (sanitized), regrettable-attrition rate.
- Competitive landscape deltas (3-5 named competitors).

## Quarterly board letter — mandatory structure

1. **CEO opening narrative** (2-3 paragraphs; thematic, what changed in tone vs last quarter).
2. **Strategic update vs OKRs / pillars** (each pillar: status RED/YELLOW/GREEN, evidence, owner).
3. **Financial highlights** (revenue, ARR, gross margin, burn multiple, runway — cite `finance-agent`'s close).
4. **KPI scorecard vs plan** (table: KPI / Actual / Plan / Variance / Owner / Status).
5. **People** (hires named for seniors; departures sanitized; attrition rate; key roles open).
6. **Investor-relevant risks** + mitigations (3-5 risks: probability x impact + mitigation owner).
7. **Asks of the board** (mandatory non-empty; distinct from investor asks).

## Annual shareholder letter — Buffett/Bezos/Dimon bar

1. **Year in review** (the year as a chapter in a multi-year story).
2. **Progress vs multi-year plan** (3-year horizon set 2-3 years ago; honest grade).
3. **Competitive landscape evolution** (named competitors, moves, our positioning).
4. **Capital allocation summary** (where every dollar went; ROIC discipline).
5. **People + culture milestones** (named hires, promotions, departures, culture work).
6. **Forward look** (2-3 year horizon; specific bets named; risks acknowledged).

Length: 1500-3500 words typical; CEO-voice but IR-drafted.

## Common recipes

### Recipe 1 — Pull prior letters for tone continuity
```bash
curl -H "Authorization: Bearer $VISIBLE_API_KEY" \
  "https://visible.vc/api/v1/updates?type=quarterly&limit=4"
```

### Recipe 2 — Pull OKRs from Lattice
```bash
curl -H "Authorization: Bearer $LATTICE_API_KEY" \
  "https://api.lattice.com/v1/objectives?period=Q2-2026&include=progress"
```

### Recipe 3 — Pull competitor moves (Firecrawl on competitor IR pages)
```bash
mcp call firecrawl-mcp scrape \
  --url "https://competitor.com/investors" --formats markdown
```

### Recipe 4 — Generate sanitized investor version
```python
# Pattern: drop ANYTHING about specific customer ARR or live deal
SENSITIVE_PATTERNS = [
    r"\$\d+K ARR from [A-Z][a-z]+",         # specific customer ARR
    r"in discussion with [A-Z][a-z]+",      # live deals
    r"considering acquisition of",          # M&A
    r"specific named individual.*departure" # personnel
]
def sanitize(text):
    for p in SENSITIVE_PATTERNS:
        text = re.sub(p, "[REDACTED]", text)
    return text
```

### Recipe 5 — Annual letter prompt scaffold (Buffett style)
```
Open with: a story or principle from the year that captures the theme.
Use plain English; no buzzwords; numbers in context.
Compare to a 5-year arc, not just YoY.
Acknowledge errors specifically; credit team for wins.
Close with 2-3 commitments for the year ahead.
```

### Recipe 6 — Publish annual letter to IR website (Q4)
```bash
curl -X POST -H "Authorization: Bearer $Q4_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "annual_letter", "url": "https://cdn.../letter.pdf", "publish_at": "..."}' \
  "https://api.q4inc.com/v1/content"
```

### Recipe 7 — Distribute via gmail-mcp (private co; investor list)
```bash
mcp call gmail-mcp send_email \
  --to "ir@company.com" \
  --bcc "$(cat investors.txt | paste -sd, -)" \
  --subject "Q2 2026 Investor Letter — ACME" \
  --html "$(cat letter.html)" \
  --attachments letter.pdf
```

### Recipe 8 — Read-along check vs Buffett/Bezos/Dimon
```python
# Quality bar: grep for these patterns
PATTERNS = {
    "concrete numbers in context": r"\$[\d,]+[KMB] (vs|up|down)",
    "named principle stated":      r"we believe|our principle is|we hold that",
    "specific commitment forward": r"by (Q[1-4]|year-?end|fiscal)",
}
# Each section should hit 2+ of these patterns
```

### Recipe 9 — Sentiment baseline check (HuggingFace FinBERT)
```bash
mcp call huggingface-mcp inference \
  --model "yiyanghkust/finbert-tone" \
  --inputs "$(cat letter.txt)"
# Should not be more positive than prior 3 letters' avg by >1 stdev
```

### Recipe 10 — Pre-wire individual board members (T-7)
```python
# Pre-wire contentious items before they hit the letter
# Pattern: 1:1 with each board member who'd object; capture pushback; absorb into letter
# Goal: zero surprise reactions at the board meeting
PRE_WIRE_TOPICS = [
    "Burn rate exceeded plan 12%",
    "VP Sales departure",
    "Customer concentration > 25%",
    "Pivot from SMB to enterprise",
]
```

## Examples

### Example 1: Q2 2026 board letter (Series B)

**Goal:** Q2 board pre-read; 7 board members + 2 observers; 60-min meeting next week.

**Steps:**
1. Pull last 3 board letters (Recipe 1) for tone continuity.
2. Open: 2-paragraph CEO narrative — "Q2 was the quarter we moved from selling to enterprise to BEING bought by enterprise."
3. Strategic update against 5 named pillars (Enterprise, Expansion, Margin, Talent, Platform).
4. Financial highlights from `finance-agent`'s Q2 close.
5. KPI scorecard table (10 KPIs vs plan).
6. People section: senior hires (VP Eng, GM Enterprise), VP Sales departure (sanitized framing), 8% attrition.
7. Risks: 3-5 with mitigations.
8. Asks of board: intros to 2 named CIOs, FY27 plan review, succession planning workshop.
9. Pre-wire (Recipe 10) any contentious item T-7.
10. Send to board T-5 days before meeting.

**Result:** Board reads pre-meeting; meeting time spent on decisions not status.

### Example 2: Annual shareholder letter (public co, accompanies 10-K)

**Goal:** FY2025 annual letter; 2800 words; published with 10-K filing.

**Steps:**
1. Year in review opens with a single named theme ("platform inflection").
2. Progress vs 3-year plan: honest grades (A/B/C/D per pillar).
3. Capital allocation: cite every $100M+ bucket (CapEx, M&A, buybacks, dividends, growth).
4. Competitive landscape: 5 named competitors + named moves + our response.
5. People milestones: 5-7 named promotions, regrettable losses framed honestly.
6. Forward 2-3 year: 3 specific bets named with risks.
7. Sanitize draft via Recipe 4.
8. Counsel review for Safe Harbor + forward-looking statement coverage.
9. Publish via Q4 (Recipe 6) on 10-K filing day.

**Result:** Letter cited by 2+ analysts in earnings preview notes; sets thematic frame.

## Edge cases / gotchas

- **Board letter vs investor letter confusion.** Same scaffold; sanitization differs. Always use Recipe 4 before external send.
- **Tone-shift gap.** If quarterly tone shifts hard from prior quarter, name it in opening — don't make investors guess.
- **OKR status inflation.** RED/YELLOW/GREEN should be evidence-backed; everything GREEN = OKRs are too soft.
- **Annual letter Safe Harbor (public co).** Counsel must review forward-looking statements; specific guidance numbers elevate to formal guidance under Reg G.
- **Forward look without commitments = wasted page.** Specific dated bets differentiate from generic.
- **Sanitization misses named customers.** Regex catches obvious patterns; human review still required.
- **Plagiarism of Buffett style.** Read Berkshire letters for cadence, never copy phrasings. Voice must be CEO's.
- **Dimon-letter length trap.** 8000-word JPM letters are an exception; 2500-3500 words is the bar for most CEOs.
- **Q4/Notified posting timezone.** Public-co letter posts on filing day at market close T+0 (or T+1 morning); confirm timezone.
- **Pre-wire skipped.** Board surprises at the meeting = lost credibility for IR; Recipe 10 is mandatory.

> Mandatory disclaimer: For public-company letters that accompany or contain forward-looking statements, **consult licensed securities counsel** for Safe Harbor + Reg G coverage before any externally distributed letter touching forward-looking statements, guidance, or material non-public information.

## Sources

- Visible.vc Quarterly Investor Update: https://visible.vc/blog/quarterly-investor-update/
- Kruze Consulting Board Meetings guide: https://www.kruzeconsulting.com/blog/board-meetings-startup/
- Berkshire Hathaway Annual Letters: https://www.berkshirehathaway.com/letters/letters.html
- Amazon 2022 Letter to Shareholders: https://www.aboutamazon.com/news/company-news/2022-letter-to-shareholders
- JPMorgan Chase Annual Report: https://www.jpmorganchase.com/ir/annual-report
- Capboard: https://www.capboard.io/
- Sturppy: https://www.sturppy.com/
- See `role.md` -> "Quarterly board + investor letter playbook" + "Annual shareholder letter playbook"

## Related skills

- `monthly-investor-update-visible` — lighter monthly cadence.
- `10k-10q-drafting-workiva` — annual report narrative (separate from CEO letter).
- `investor-day-capital-markets-day` — when the letter sets up the deep-dive day.
- `fund-of-funds-lp-reporting` — LP-specific letter variant.
