<!--
Source: https://www.alpha-sense.com/blog/q-a-prep-best-practices/
Source: https://www.niri.org/standards-of-practice
Source: https://www.notion.so/templates/ir-faq
Source: https://coda.io/templates/ir-knowledge-base
Reference role.md: "Shareholder Q&A library playbook"
Round 2 enrichment: Notion DB template + post-call back-fill + per-topic curation + IR FAQ public-vs-internal versioning.
-->

# Shareholder Q&A library + IR FAQ maintenance

Maintains the 100-300-entry shareholder Q&A library — per-topic categorization, vetted answers, as-of dates, owner routing (CEO/CFO/COO/IR/legal). Refreshed quarterly post-earnings; back-fills new Qs from each call. Powers earnings Q&A binder prep, post-call analyst answers, and data room "Diligence Q&A" section.

## When to use

- Q1 / Q2 / Q3 / Q4 post-earnings back-fill of new Qs from the call.
- Quarterly refresh of as-of dates.
- New entry on emerging topic (e.g., new regulatory rule, M&A integration, ESG framework adoption).
- Diligence Q&A export for fundraise / M&A data room.
- Trigger phrases: "update Q&A library", "shareholder FAQ", "IR FAQ", "Q&A binder back-fill", "diligence Q&A export".

NOT for: earnings call script + binder (use `earnings-call-script-qa`); 10-K Item 1A Risk Factors (use `10k-10q-drafting-workiva`); roadshow briefing books (use `roadshow-ndr-logistics`).

## Setup

```bash
# Notion (preferred home — recipient supplies workspace)
# notion-mcp from CraftBot catalog

# AlphaSense for new-Q pattern mining post-earnings
export ALPHASENSE_API_KEY="<from AlphaSense Admin>"

# Alt repos
# - Coda IR Knowledge Base
# - Confluence (Atlassian) for legal/IP-heavy entries
```

Auth / API key requirements:
- `notion-mcp` (free for Notion personal; team plan $10/user/mo+).
- `ALPHASENSE_API_KEY` — for new-Q pattern mining (optional but accelerates).
- Free fallback: manual transcript scraping; less efficient but works.

Data inputs:
- Last 4 earnings call transcripts (own + 4 peer).
- Latest 10-K + 10-Q + DEF 14A (for grounded answers).
- `guidance-setting` output (live guidance numbers).
- M&A diligence requests (when applicable).
- ISS / Glass Lewis policy guidelines (for governance Qs).

## Notion DB schema

```
QUESTION (title): <verbatim or paraphrased>
TOPIC (select): Strategy | Revenue | Margin | Cash | Capital Allocation | Competitive |
                M&A | ESG | Governance | People | Macro | Legal/IP | Tech | Customer
ANSWER (rich text, 50-200 words): <vetted current answer>
BRIDGE (text): <1 sentence connecting to long-term thesis>
OWNER (select): CEO | CFO | COO | IR | Legal
AS-OF (date): <YYYY-MM-DD; auto-expire flag after 90 days>
SOURCE (multi-select): internal model | published filing | analyst note | prior call
CONFIDENCE (select): HIGH | MEDIUM | LOW
PUBLIC/INTERNAL (select): public (data room ok) | internal (binder only)
TAGS (multi-select): guidance | YoY | segment | etc.
LAST USED (date): <date last referenced in call/1:1>
COUNT USED (number): <usage counter>
REVIEW STATUS (select): GREEN | YELLOW (>=60d stale) | RED (>=90d stale)
```

## Topical categories (target 100-300 entries)

| Category | Target #Qs |
|----------|-----------|
| Strategy / Vision | 15-30 |
| Financials — Revenue / Bookings / ARR | 15-30 |
| Financials — Margin / Unit Econ | 10-20 |
| Financials — Cash / Burn / Runway | 10-15 |
| Capital Allocation | 15-20 |
| Competitive | 10-20 |
| M&A | 5-15 |
| ESG / Climate / DEI | 10-20 |
| Governance | 10-15 |
| People / Succession | 5-10 |
| Macro / Regulatory | 5-10 |
| Legal / IP | 5-10 |
| Tech / Architecture (B2B SaaS) | 10-15 |
| Customer Success / Renewals | 5-10 |
| AI / LLM (2025+ emerging) | 5-15 |

## Public vs internal versioning

- **Internal binder** = earnings Q&A binder; full library; CEO/CFO/IR access; legal-tagged Qs only for counsel.
- **Public IR FAQ** = subset exported to IR website (Q4 / Notified); generic strategy + governance + ESG; NO forward numbers; NO specific customer references.
- **Diligence Q&A** = data-room subset for M&A / fundraise; includes financial detail; under NDA only.

## Post-call back-fill workflow

| Step | Action | Tool |
|------|--------|------|
| 1 | Pull transcript T+24h | Recipe 1 |
| 2 | Extract every Q asked | Recipe 2 |
| 3 | Match against library; flag new vs existing | Recipe 3 |
| 4 | Update existing if material; create new entries | Recipe 4 |
| 5 | Refresh as-of dates on entries used in call | Recipe 5 |
| 6 | Owner review within 2 weeks | notion-mcp |
| 7 | Counsel review on legal-tagged Qs | counsel hand-off |

## Common recipes

### Recipe 1 — Pull call transcript (own)
```bash
curl -H "Authorization: Bearer $ALPHASENSE_API_KEY" \
  "https://api.alpha-sense.com/v1/transcripts?ticker=$TICKER&latest=true"
```

### Recipe 2 — Extract Qs from transcript
```python
import re
ANALYST_INDICATOR = re.compile(r"\b(Question|Q:|^[A-Z][a-z]+ [A-Z][a-z]+:)", re.M)
def extract_questions(transcript):
    sections = transcript.split("Operator:")
    qa = [s for s in sections if "question" in s.lower() and "operator" in s.lower()]
    return [match for match in ANALYST_INDICATOR.findall(qa[0])] if qa else []
```

### Recipe 3 — Match against library (fuzzy)
```python
from rapidfuzz import fuzz, process

def match_existing(new_q, library_qs, threshold=80):
    best = process.extractOne(new_q, library_qs, scorer=fuzz.token_set_ratio)
    return best if best and best[1] >= threshold else None
```

### Recipe 4 — Create Q&A entry (notion-mcp)
```bash
mcp call notion-mcp create_page --database=$QA_DB \
  --properties='{
    "Question": "How are you thinking about the LLM provider concentration risk?",
    "Topic": "Tech",
    "Answer": "We mitigate LLM provider concentration by maintaining multi-provider integration across OpenAI, Anthropic, Google. Our standard provider rotation tests quarterly; in-house fine-tuned fallback model deployed Q2 2026...",
    "Bridge": "Multi-provider strategy underpins our long-term gross margin trajectory and product resilience.",
    "Owner": "CFO",
    "As-of": "2026-07-30",
    "Source": ["prior call", "internal model"],
    "Confidence": "HIGH",
    "Public/Internal": "internal",
    "Tags": ["AI", "risk", "tech"]
  }'
```

### Recipe 5 — Refresh as-of dates after call
```bash
# Query entries used in this call (matched via Recipe 3)
# Update As-of = call date for each
mcp call notion-mcp update_page --page_id=$PAGE_ID \
  --properties='{"As-of": "2026-07-30", "Last Used": "2026-07-30"}'
```

### Recipe 6 — Quarterly aging report
```python
# Find YELLOW (>=60d) and RED (>=90d) entries; route to owner for refresh
yellow = [e for e in entries if (today - e.as_of).days >= 60 and (today - e.as_of).days < 90]
red = [e for e in entries if (today - e.as_of).days >= 90]
```

### Recipe 7 — Public IR FAQ export
```python
# Filter Public + Confidence HIGH + not Legal/IP
public_subset = [e for e in entries
                 if e.public_internal == "public"
                 and e.confidence == "HIGH"
                 and e.topic not in ("Legal/IP",)
                 and not contains_forward_numbers(e.answer)]
# Render to markdown for Q4 / Notified IR website
```

### Recipe 8 — Diligence Q&A data-room export
```python
# Includes financial + tech + customer; under NDA
# Tag as "data room" with NDA gating
diligence_subset = filter_by_tags(entries, tags=["financials", "tech", "customer", "M&A"])
export_pdf(diligence_subset, "diligence_QA_2026Q3.pdf")
```

### Recipe 9 — Pre-earnings binder build (paired with `earnings-call-script-qa`)
```python
# Pull top-150 entries by:
# - Recently asked (used in last 2 calls)
# - Strategic priority (CEO/CFO marked)
# - High-confidence
# Then categorize for earnings binder
binder = get_top_entries(library, count=150, ranking=["recency", "priority", "confidence"])
binder.group_by("topic")
binder.export("earnings_binder_Q3_2026.docx")
```

### Recipe 10 — Owner-routing notification (Slack)
```bash
# Notify owner of new/updated entry
mcp call slack-mcp post_message \
  --channel "#ir-qa-review" \
  --text "$OWNER: 3 entries pending your review by $DEADLINE — https://notion.so/$URL"
```

### Recipe 11 — Counsel review queue (legal-tagged Qs)
```python
# Route any Q tagged Legal/IP or M&A or ESG-compliance to counsel
counsel_queue = [e for e in entries if "Legal/IP" in e.topic or "compliance" in e.tags]
# Counsel reviews within 5 business days; updates Confidence + As-of
```

### Recipe 12 — Pattern mining for emerging Qs (AlphaSense peer transcripts)
```bash
curl -H "Authorization: Bearer $ALPHASENSE_API_KEY" \
  "https://api.alpha-sense.com/v1/search?q=$PEER_TICKERS&doc_type=transcript&period=last_q&limit=10"
# Find Qs peers got but we haven't — add to library proactively
```

## Examples

### Example 1: Post-Q2 earnings back-fill

**Goal:** Q2 call 2026-07-30; back-fill new Qs by T+10 days.

**Steps:**
1. T+1: pull transcript (Recipe 1).
2. T+2: extract 18 distinct Qs (Recipe 2).
3. T+3: match against library (Recipe 3) — 13 match existing; 5 are new.
4. T+4: update 13 existing entries (As-of + counter); create 5 new (Recipe 4).
5. T+5: owner notification (Recipe 10).
6. T+7: counsel review on 2 legal-tagged entries.
7. T+10: aging report (Recipe 6) — 8 YELLOW + 2 RED; ticket owners.
8. T+14: all owners signed off; ready for Q3 binder build.

**Result:** Library current; next call binder pulls fresh entries; no stale answers.

### Example 2: New regulatory rule (SEC climate disclosure)

**Goal:** SEC final climate-disclosure rule released; add library entry.

**Steps:**
1. Counsel + compliance brief on rule.
2. Build Q&A entry (Recipe 4):
   - Q: "How are you preparing for the SEC climate-disclosure rule?"
   - A: "We've engaged Workiva ESG; began Scope 1 + 2 GHG inventory Q1 2026; expect first compliance filing FY2027..." (vetted).
   - Owner: ESG-lead + Counsel.
   - Confidence: HIGH (counsel-vetted).
   - Public/Internal: public.
2. Add to public IR FAQ export (Recipe 7); appears on IR website.
3. Add to earnings binder (Recipe 9).

**Result:** Proactive answer ready when analyst asks; counsel-approved; aligned across channels.

### Example 3: Diligence Q&A export for M&A

**Goal:** M&A target due diligence; need Q&A pack under NDA.

**Steps:**
1. Filter library subset for diligence (Recipe 8) — 80 entries.
2. Export to PDF; deposit in DocSend / Visible.vc data room under NDA.
3. Track per-entry views via DocSend page analytics.
4. Update library based on which Qs were viewed most (signal for future binder).

**Result:** Diligence efficient; 30% fewer ad-hoc Q requests during M&A process.

## Edge cases / gotchas

- **Reg FD risk in answers.** Any forward-looking answer must be in line with public guidance; counsel review forward Qs.
- **Stale answers in live earnings call.** If As-of >90 days and used live = high embarrassment risk; aging report (Recipe 6) is mandatory.
- **Public vs internal slip.** Internal answers leaking to public IR FAQ = Reg FD violation risk; gate by Public/Internal field.
- **Confidence inflation.** Everyone marks HIGH; force MEDIUM/LOW honest grading.
- **Owner sprawl.** Too many owners = no accountability; cap at 5-6 owners (CEO/CFO/COO/IR/Legal).
- **Topic taxonomy drift.** Quarterly review topic structure; emerging topics (AI, Climate) need own categories.
- **Match-against-library too aggressive.** Fuzzy match threshold 80 catches semi-duplicates; too low = pollution; too high = duplication.
- **AlphaSense paywall.** Free fallback: SEC EDGAR 8-K Item 2.02 transcripts (slower; lower fidelity).
- **Data room NDA leakage.** Diligence Q&A export must be under NDA; track per-page analytics; revoke access on close.
- **Counsel review backlog.** Counsel review on legal-tagged Qs can lag; build SLA into workflow.
- **Library bloat.** >300 entries = unwieldy; archive or prune low-usage entries quarterly.
- **Ownership transition.** Departing CFO = re-assign all "Owner: CFO" entries.
- **Foreign-language IR FAQ.** Multinational ADRs may need translation; tag entries needing translation.
- **Analyst patterning.** Some analysts ask the same Q every call; tag and prepare specific answer variants.

> Mandatory disclaimer: Q&A library answers that touch forward-looking statements, material non-public information, or governance/legal positions are subject to Regulation FD and Safe Harbor. **Consult licensed securities counsel** before publishing any answer touching forward statements, before any data-room diligence export to non-NDA parties, and before any public IR FAQ post containing forward numbers.

## Sources

- AlphaSense Q&A Prep Best Practices: https://www.alpha-sense.com/blog/q-a-prep-best-practices/
- NIRI Standards of Practice: https://www.niri.org/standards-of-practice
- Notion IR FAQ Template: https://www.notion.so/templates/ir-faq
- Coda IR Knowledge Base: https://coda.io/templates/ir-knowledge-base
- SEC Regulation FD Interpretations: https://www.sec.gov/divisions/corpfin/guidance/regfd-interp.htm
- See `role.md` -> "Shareholder Q&A library playbook"

## Related skills

- `earnings-call-script-qa` — pre-call binder build pulls from this library.
- `equity-analyst-relations-briefings` — analyst 1:1 briefings pull from this.
- `roadshow-ndr-logistics` — NDR briefing books cite this library.
- `10k-10q-drafting-workiva` — Risk Factor refresh draws on library trends.
- `ma-investor-comms` — diligence Q&A export for deal.
