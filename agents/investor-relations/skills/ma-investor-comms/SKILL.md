<!--
Source: https://www.joelefrank.com/services/
Source: https://www.sardverb.com/services/mergers-and-acquisitions/
Source: https://www.fticonsulting.com/services/strategic-communications/mergers-acquisitions
Source: https://www.sec.gov/about/forms/form8-k.pdf
Source: https://www.cooley.com/services/practice/transactions/mergers-acquisitions
Reference role.md: "M&A investor comms playbook"
Round 2 enrichment: announcement-day timeline + investor deck structure + analyst notebook + shareholder vote integration + spin-off Form 10 variant.
-->

# M&A investor communications (announcement-day sequence)

Drafts M&A investor communications — joint announce 8-K (Item 1.01 or 2.01) + press release + investor deck (15-30 slides) + analyst notebooks + joint CEO conference call script + shareholder vote integration (if stock-funded). Coordinates with `finance-agent` (deal model + synergies + accretion/dilution), `ceo-agent` (CEO-voice narrative), `legal-counsel` (binding 8-K + M&A docs). Senior advisor coord: Joele Frank / Sard Verbinnen / FTI.

## When to use

- M&A announcement day comms (acquirer-side).
- Target-side comms (if target is public).
- Spin-off / Form 10 / Information Statement comms.
- Hostile / activist-defense response comms (Joele Frank specialty).
- Divestiture / disposition comms.
- Trigger phrases: "M&A announce", "M&A comms", "deal announce", "spin-off comms", "announcement day", "tender offer".

NOT for: M&A target screen pre-deal (use `finance-agent`'s `ma-target-screen-and-qoe`); 10-K narrative after deal closes (use `10k-10q-drafting-workiva`); routine 8-K (use `8k-event-reporting`).

## Setup

```bash
# Senior advisor engagement (per-deal contract $500K-$2M+)
# - Joele Frank — M&A + activist defense (gold standard)
# - Sard Verbinnen — M&A + crisis
# - FTI Strategic Comms — broad
# - Brunswick — cross-border + media-heavy
# - Abernathy MacGregor — corporate + M&A

# Wire distribution
export BUSINESSWIRE_API_KEY="<from BW Portal>"
export NOTIFIED_API_KEY="<from Notified Admin>"
export PR_NEWSWIRE_API_KEY="<from PR Newswire>"

# Tools: pptx (deck); docx (press release + 8-K body); cli-anything (wire)
```

Auth / API key requirements:
- Senior advisor — relationship + engagement letter ($500K-$2M+ per deal).
- Wire vendor — paired with `quarterly-earnings-press-release` setup.
- Free fallback (small deals): SEC.gov EDGAR + Q4/Notified IR website + gmail-mcp.

Data inputs:
- Deal terms (counsel + financial advisor finalized).
- `finance-agent` deal model: accretion/dilution, synergies (cost + revenue), pro forma combined financials.
- `ceo-agent` CEO narrative (strategic rationale; integration philosophy).
- Combined company org chart + leadership team.
- Regulatory approval timeline (HSR, EU, etc.).
- Both companies' analyst coverage matrices (`equity-analyst-relations-briefings`).
- Both companies' 13F holders (`13f-shareholder-monitoring`).

## Announcement-day timeline (T-0)

| Time (ET) | Activity | Owner |
|-----------|----------|-------|
| 4:00 AM | Internal circulation; final review; counsel sign-off | All |
| 6:30 AM | Press release + 8-K + deck final-final | IR + counsel |
| 7:00 AM | Wire press release; file 8-K Item 1.01 (or 2.01); IR website updates | IR + Wire |
| 7:01 AM | IR-website earnings center updates; deck posted | Q4/Notified |
| 8:00 AM | Joint conference call (both CEOs + CFOs + Q&A 60-90 min) | All |
| 8:00 AM - 12:00 PM | Analyst pre-briefings (1:1 callbacks; prepared remarks only) | IR + CFO |
| 1:00 PM | Joint press conference (cross-functional media + IR) | All |
| 3:00 PM | Sell-side analyst hosted call (paired bank coordinates) | IR + bank |
| Following days | Roadshow / NDR with combined narrative | `roadshow-ndr-logistics` |
| T+30 days | Investor day or capital markets day update (if material) | IR |

## Investor deck structure (15-30 slides)

```
1. Transaction summary (1 slide)
   - Headline: deal value, structure (stock/cash/mix), accretion year
2. Strategic rationale (2-3 slides)
   - Why now? Why this target? What's the combined thesis?
3. Combined company snapshot (1 slide)
   - Revenue + segments + geos + headcount
4. Financial profile (2-3 slides)
   - Pro forma revenue / margin / EPS / FCF
5. Synergies (2-3 slides) — cost + revenue (timeframe + confidence)
   - Year 1 / Year 2 / Year 3 cost synergies ($X / $Y / $Z)
   - Revenue synergies (cross-sell, market expansion)
   - One-time integration costs
6. Integration plan + key risks (1-2 slides)
   - Day-1 readiness; 100-day plan; named integration leader
7. Leadership team + governance (1 slide)
   - Combined exec team; board composition
8. Financing structure (1-2 slides)
   - Cash / new debt / equity issuance; pro forma leverage
9. Timeline + regulatory approvals (1 slide)
   - HSR / EU / other; expected close
10. Q&A appendix (5-10 slides)
    - Synergy detail; segment math; comp basis
```

## Common recipes

### Recipe 1 — Press release headline scaffold
```python
HEADLINE_SCAFFOLD = """
{Acquirer} to Acquire {Target} in ${X}B Transaction;
Creates Leading Global {Sector} Platform; Expected ${X}M Run-Rate Cost Synergies by {Year}
"""
```

### Recipe 2 — 8-K Item 1.01 body (M&A entry into material agreement)
```python
ITEM_1_01_BODY = """
On {date}, {Registrant} entered into an Agreement and Plan of Merger
(the "Merger Agreement") with {Target}. Under the Merger Agreement,
{Registrant} will acquire {Target} for total consideration of approximately
${X} billion in {stock/cash/mix}. The transaction is subject to approval by
{Target} shareholders, regulatory approvals, and customary closing conditions.

A copy of the Merger Agreement is filed as Exhibit 2.1...
[Standard furnished/filed paragraphs; counsel-supplied]
"""
```

### Recipe 3 — CEO talk-track for joint call
```
Strategic rationale (3 paragraphs):
- Why this deal makes sense for our shareholders (the "thesis")
- What we're getting (capabilities, customers, talent, IP)
- How we'll integrate without breaking what works

Financial discipline (1 paragraph):
- Accretion path; balance sheet; capital allocation framework
- Synergy capture confidence; integration governance

Forward look (1 paragraph):
- Day-1 priorities; 100-day plan; communication cadence with shareholders
```

### Recipe 4 — Investor deck creation (pptx)
```python
# Standard deck shell; senior advisor (Joele Frank) iterates
from pptx import Presentation
deck = Presentation()
SLIDES = [
    "Transaction Summary",
    "Strategic Rationale",
    "Combined Company Snapshot",
    "Financial Profile",
    "Synergies",
    "Integration Plan",
    "Leadership & Governance",
    "Financing Structure",
    "Timeline & Approvals",
    "Q&A Appendix",
]
for title in SLIDES:
    slide = deck.slides.add_slide(deck.slide_layouts[1])
    slide.shapes.title.text = title
deck.save("deal_announce_deck.pptx")
```

### Recipe 5 — Analyst notebook template
```
ANALYST NOTEBOOK — FOR DISCUSSION (NOT FOR PUBLICATION):

Deal Summary:
- Acquirer: ACME (NASDAQ: ACME)
- Target: Beta (NYSE: BETA)
- Consideration: $X.XB ($Y per share, stock-for-stock)
- Exchange ratio: Z BETA -> 1 ACME
- Premium: A% to BETA 30-day VWAP
- Expected close: [date]; subject to HSR + shareholder vote

Pro Forma Financials:
- Revenue: $X (ACME) + $Y (BETA) = $Z combined
- EBITDA margin: improved by X bps
- Accretion: year +N ($X/share)

Synergies:
- Cost: $X run-rate by year +Y
- Revenue: $Z by year +A
- Integration: $X one-time over Y years

Key Q+A:
- Antitrust risk: [discussion]
- Customer attrition risk: [discussion]
- Talent retention: [discussion]
```

### Recipe 6 — Wire submission (Business Wire)
```bash
curl -X POST -H "Authorization: Bearer $BUSINESSWIRE_API_KEY" \
  -d @ma_press_release.json \
  "https://api.businesswire.com/v2/releases?embargo_until=$EMBARGO_TIME"
```

### Recipe 7 — Joint conference call (Notified)
```bash
curl -X POST -H "Authorization: Bearer $NOTIFIED_API_KEY" \
  -d '{
    "type": "ma_announce_call",
    "title": "ACME to Acquire BETA — Announcement Call",
    "start": "2026-09-15T12:00:00Z",
    "duration_minutes": 90,
    "speakers": ["ACME CEO", "BETA CEO", "ACME CFO", "BETA CFO"]
  }' \
  "https://api.notified.com/v1/events"
```

### Recipe 8 — Sell-side analyst Q&A pre-prep
```python
# Pull both companies' Q&A libraries; build combined binder
combined_qa = merge_libraries(
    library_acquirer=load("acme_qa.json"),
    library_target=load("beta_qa.json"),
    deal_specific=load("deal_qa_drafts.json"),
)
# Focus topics: synergy realization, customer overlap, integration risks
```

### Recipe 9 — Shareholder vote integration (if stock-funded)
```python
# Joint proxy statement (S-4 if cross-border or new shares)
# Both companies' DEF 14A integrated (paired with `proxy-statement-drafting`)
# Proxy solicitor (Innisfree / Okapi) engaged
# Vote-collection cadence T-60 to T-0
```

### Recipe 10 — Spin-off / Form 10 variant
```python
SPIN_OFF = {
    "form": "Form 10 / Information Statement",
    "key_documents": [
        "Form 10 registration statement",
        "Information statement to shareholders",
        "Tax opinion (Section 355 qualifying)",
        "Stand-alone separation agreement",
    ],
    "comms": "lighter deck; emphasis on rationale + capital structure + initial financials",
}
```

### Recipe 11 — Senior advisor coord (Joele Frank engagement)
```
Engagement scope (typical):
- Press release + 8-K + Item 1.01 wording strategy
- Investor deck slide-by-slide editorial
- CEO/CFO talk-track prep
- Analyst notebook framing
- Media + reporter coordination
- Activist intel / response if hostile counter
- Shareholder voting prediction
```

### Recipe 12 — Activist-counter response (if hostile)
```
Specialist domain — defer to senior advisor (Joele Frank or Sard Verbinnen).
Track activist's prior playbook; pre-position with ISS / Glass Lewis;
Proxy contest contingency planning;
Defense materials (white paper + counter-deck);
Bidder-letter response template.
```

### Recipe 13 — Cross-border announcement (multi-jurisdiction wire)
```python
# Coordinate multiple wire releases for time-zone fairness
# US: Business Wire / PR Newswire (7:00 AM ET)
# Europe: Reuters / Dow Jones (1:00 PM CET equivalent)
# Asia: PR Newswire Asia (9:00 PM HKT)
```

### Recipe 14 — Combined IR website page
```bash
curl -X POST -H "Authorization: Bearer $Q4_API_KEY" \
  -d '{
    "type": "ma_announcement",
    "title": "ACME-BETA Combination",
    "url": "/investors/acme-beta-combination",
    "deck_pdf": "...",
    "press_release_url": "...",
    "call_replay_url": "..."
  }' \
  "https://api.q4inc.com/v1/sec-filings"
```

## Examples

### Example 1: Strategic-acquirer mid-cap M&A announcement

**Goal:** ACME (acquirer) announces acquisition of Beta (target) for $4.2B stock + cash.

**Steps:**
1. T-7 days: Joele Frank engaged; senior advisor team installed.
2. T-3 days: Counsel + financial advisor + IR + both CEOs sequenced final ratification.
3. T-1 day: Press release + 8-K + investor deck v-final reviewed.
4. T-0 4:00 AM: Internal circulation final; both CFOs sign off.
5. T-0 7:00 AM: Wire goes (Recipe 6); 8-K files; IR website live (Recipe 14).
6. T-0 8:00 AM: Joint call (Recipe 7); both CEOs + CFOs; Q&A 90 min.
7. T-0 8:00 AM - 12:00 PM: Analyst pre-briefings (8-12 sell-side analysts; prepared remarks only).
8. T-0 1:00 PM: Joint press conference.
9. T+1: Roadshow planning (Recipe 5 + roadshow-ndr-logistics).
10. T+30: Investor day update.

**Result:** Synced comms across all channels; analyst notes published within 24h; sell-side support secured.

### Example 2: Spin-off announcement

**Goal:** ACME spins off SubCo as independent public company; tax-free Section 355.

**Steps:**
1. Information statement drafted (combined with `legal-counsel`).
2. Form 10 registration (Workiva).
3. Press release + 8-K Item 8.01.
4. SubCo CEO + ACME CEO joint call.
5. Investor deck (lighter; 15 slides; focus on rationale + capital structure).
6. Q&A library updated with SubCo entries.
7. Distribution ratio + record date communicated.

**Result:** Clean spin announcement; tax-free qualification preserved; investor narrative clear.

### Example 3: Hostile counter response

**Goal:** Hostile bidder approaches; activist 13D filed simultaneously.

**Steps:**
1. Immediate escalation: counsel + Joele Frank + financial advisor + board.
2. Defense playbook activated; specialist advisors run.
3. Counter-deck prep (white paper).
4. Pre-position with ISS / Glass Lewis.
5. Counter-press release: counsel-supplied; rejects bid + recommits to standalone plan.
6. Analyst 1:1s coordinated (counsel-approved talking points).
7. Roadshow defending standalone plan + capital allocation.

**Result:** Activist response coordinated; binary outcome depends on substance; preparation reduces surprise.

## Edge cases / gotchas

- **Senior advisor selection.** Joele Frank for hostile / activist; Sard Verbinnen for friendly; FTI broad; Brunswick cross-border. Match to deal type.
- **Both-side comms coordination.** Acquirer + target IR teams must align on every message; ego conflicts trip many deals.
- **Joint conference call talk-track tension.** Each CEO wants to look great; rehearsals essential.
- **Embargo leak from joint deal team.** Cross-company info-sharing widens leak risk; counsel-supervised.
- **Reg FD on day-of.** Wire + 8-K + IR website must be simultaneous; analyst calls T+1 hour minimum to absorb public.
- **Antitrust filing timing.** HSR pre-merger notification filed simultaneously; EU notification per timeline.
- **Section 16 disclosure overlap.** Insider trade restrictions during deal pendency.
- **DEF 14A integration (stock-funded).** Joint proxy statement; significant lead time.
- **Tax opinion (Section 355) for spin.** Must be qualified opinion or deal fails tax-free treatment.
- **Tender offer Schedule 14D-9.** Target's official response to tender; counsel + advisor coord.
- **Activist counter mid-deal.** Hostile bidder may emerge during friendly deal; senior advisor activates.
- **Shareholder vote prediction.** Proxy solicitor (Innisfree / Okapi) crucial for ratify.
- **Media leak control.** Wall Street Journal / Bloomberg / Reuters reporting often leaks day-prior; deal team confidentiality.
- **Combined company IR transition.** Day-1 IR ops merger; one IR website; renamed events calendar.
- **Bilateral exclusivity period.** "Go-shop" or "no-shop" clauses affect comm strategy.
- **Pre-bid market signal.** Stock moves pre-announcement = leak indicator; investigate.
- **Foreign-buyer comms.** Cross-border deals need multiple language wires + multi-jurisdiction filings.
- **Activist 13D simultaneous.** Both signal day-of; coordinated counter-response.

> Mandatory disclaimer: M&A communications involve binding SEC filings (8-K Item 1.01 / 2.01, possibly S-4 / DEF 14A) and disclosures subject to anti-fraud provisions of federal securities law. Hostile / activist M&A engages tender-offer rules under Williams Act and Section 14(d)-(e). **Consult licensed securities counsel** for every binding M&A comm — 8-K language, press release content, talk-track legal sufficiency, shareholder vote materials, and any activist-counter response. This skill drafts the playbook + materials; counsel + senior advisor + financial advisor approve binding execution.

## Sources

- Joele Frank Services: https://www.joelefrank.com/services/
- Sard Verbinnen M&A: https://www.sardverb.com/services/mergers-and-acquisitions/
- FTI Strategic Comms M&A: https://www.fticonsulting.com/services/strategic-communications/mergers-acquisitions
- Brunswick Group: https://www.brunswickgroup.com/
- SEC Form 8-K: https://www.sec.gov/about/forms/form8-k.pdf
- SEC Form S-4 (stock-funded M&A): https://www.sec.gov/about/forms/forms-4.pdf
- SEC Schedule 14D-9 (tender response): https://www.sec.gov/about/forms/schedule14d9.pdf
- Cooley M&A Practice: https://www.cooley.com/services/practice/transactions/mergers-acquisitions
- See `role.md` -> "M&A investor comms playbook"

## Related skills

- `8k-event-reporting` — Item 1.01 / 2.01 paired filing.
- `proxy-statement-drafting` — DEF 14A integration for stock-funded.
- `embargoed-disclosure-protocols` — pre-announcement wall-cross.
- `quarterly-earnings-press-release` — overlap if announcement near earnings.
- `roadshow-ndr-logistics` — post-announce investor education.
- `investor-day-capital-markets-day` — post-close capital markets day.
