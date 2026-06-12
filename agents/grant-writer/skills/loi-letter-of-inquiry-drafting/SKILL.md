---
name: loi-letter-of-inquiry-drafting
description: Draft 2-3 page Letters of Inquiry (LOIs) / concept papers that mirror funder priorities, address the program officer by name, and earn a "send the full proposal" invitation. Use when the user says "write an LOI to <funder>" or "draft a concept paper".
---

# Letter of Inquiry (LOI) drafting

A funder's LOI is a single short pitch — typically 2-3 pages — that earns (or loses) you the right to submit a full proposal. The structure is conventional; the win comes from priority alignment, primary-source data, and PO relationship signal.

## When to use

- User asks for an LOI for a specific foundation or corporate funder
- User wants a concept paper before deciding whether to invest in a full proposal
- User wants a pitch-style version of the proposal for a high-net-worth donor or family foundation
- First touch with a foundation that requires an LOI before full proposal

Do NOT use this skill for:
- Federal grant proposals (federal NOFOs rarely use LOIs → `full-grant-proposal-narrative-methods-evaluation`)
- Renewal asks where you have an existing relationship (often skip to full proposal)
- DAF-routed asks where the donor-advisor wants a 1-page brief (→ short pitch deck via `pptx`)

## Setup

```bash
# No specialized install. Standard writing stack:
# - filesystem (org docs + funder pages)
# - firecrawl-mcp (scrape foundation priorities)
# - docx (final output)
# - notion-mcp (foundation profile lookup)
```

Auth / API key requirements: None for the writing itself. Optional `firecrawl-mcp` API key for scraping funder pages.

## Common recipes

### Recipe 1: Pull funder priorities verbatim before drafting

```bash
# Via firecrawl-mcp
firecrawl_scrape url="https://hewlett.org/strategy/" formats=["markdown"]
```

Extract the funder's published strategy phrases (e.g., "advancing clean energy and reducing the impacts of climate change") and use them VERBATIM in the LOI opening + project description.

### Recipe 2: Pull PO name + bio via LinkedIn / foundation staff page

```bash
firecrawl_scrape url="https://hewlett.org/people/?role=program-officer" formats=["markdown"]
```

Address by name in greeting. If no PO is listed, use "Dear Grants Manager" or research via LinkedIn.

### Recipe 3: 5-paragraph LOI scaffold

```markdown
# Letter of Inquiry: <Project Name>
**To:** <PO Name>, Program Officer, <Funder>
**From:** <Org name>, <date>
**Re:** <Funder's program area> — <One-line project>

Dear <PO First Name>,

[Para 1 — Opening hook + ask: 3-4 sentences. Reference recent grant to peer org OR their published priority. Identify your org + ask in 2 sentences.]

[Para 2 — Statement of need: 4-5 sentences. Quantified problem with primary-source citation. Geographic scope + population. Why now.]

[Para 3-4 — Project: 6-10 sentences. Goal → 2-3 measurable objectives → activities → outcomes. Tied to logic model. Time-bounded.]

[Para 5 — Org credibility: 4-5 sentences. Years operating, prior similar work with numbers, key partners, evaluation track record.]

[Para 6 — Ask + close: 3-4 sentences. $<amount> over <period> against total $<X>. Match/leverage. "We welcome the opportunity to submit a full proposal."]

Sincerely,
<Name>, <Title>
<Email> | <Phone>
```

### Recipe 4: Word-count check

```bash
# 2-3 page LOI = ~1200-1800 words (single-spaced, 11pt, 1" margins)
wc -w loi.md
# If >1800, trim. Funders strictly enforce page limits.
```

### Recipe 5: Render to DOCX

```bash
pandoc loi.md -o loi.docx --reference-doc=templates/org_letterhead.docx
```

Use the org's letterhead reference DOCX so the LOI lands with branding. Templates live in `agent_bundle/agents/grant-writer/templates/` or the org's proposal library.

### Recipe 6: PO outreach email (before LOI)

```markdown
Subject: <Org name> — fit with <Funder>'s <priority> priority?

Dear <PO First Name>,

[1 sentence — referrer or hook: "Sarah Chen at <peer org> suggested I reach out" OR "I read your <article / public talk> on <topic>."]

[2-3 sentences — org + project + alignment: "<Org> works on <topic> in <geo>. We are planning <project>. We believe this fits <Funder>'s <priority> priority."]

[1 sentence — ask: "Would a brief 15-minute call be useful to confirm fit before we submit an LOI?"]

Best,
<Name>
```

Sent 2-4 weeks before the LOI deadline. A "yes, fit confirmed" response is gold. A "we are not funding <topic> this cycle" saves you a wasted LOI.

### Recipe 7: Mirror funder priority language

```bash
# Pull funder's grants list and extract recurring phrases
firecrawl_scrape url="https://hewlett.org/grants/" formats=["markdown"]
# grep -i 'we support|priorities|focus on'
```

Mirror their phrasing. If they say "advance economic mobility for working families," do not write "improve outcomes for low-income people."

### Recipe 8: LOI for a corporate funder (slightly different tone)

```markdown
[Para 1 — Opening: align with corp's brand / ESG report theme.]
[Para 2 — Need + corp's stakeholder benefit: "Your customers / employees / communities are affected by..."]
[Para 3 — Project + visibility opportunities: "Your brand would be recognized via <co-branding / event / employee volunteering / impact report>."]
[Para 4 — Org credibility: prior corp partnerships.]
[Para 5 — Ask: $<amount> + employee volunteer hours + in-kind opportunity. Co-investment angle.]
```

### Recipe 9: LOI for a DAF (Donor-Advised Fund) sponsor

DAF asks go through the DAF sponsor's philanthropic services team, NOT directly to the donor-advisor. The LOI lives at the sponsor's portal (Fidelity Charitable, Schwab Charitable). Keep to 1-2 pages and lead with the 501(c)(3) verification line.

### Recipe 10: Differential review before sending

```bash
# Run the LOI through the differential-review skill before submission
# Reviewers: ED + Program Lead + Finance lead at minimum
```

Reviewers check: priority alignment, primary-source citations present, ask amount aligns with funder's avg grant, no typos, PO name correct.

## Examples

### Example 1: LOI to a community foundation for a place-based ECE program

**Goal:** 3-page LOI to East Bay Community Foundation for a $50K, 18-month early childhood program serving Oakland.

**Steps:**
1. Scrape EBCF's 2026 strategy page for priority phrases ("advancing racial equity and economic security for East Bay families").
2. Pull EBCF's recent grants list — note 3 peer ECE orgs they funded in 2025.
3. Pull PO name (Maria Hernandez, Program Officer, Education) from staff page.
4. Draft using 5-paragraph scaffold. Open with reference to their grant to peer org. Mirror "racial equity" + "economic security" language verbatim.
5. Word-count check: aim for 1400 words. Render to DOCX on org letterhead.
6. Differential review with ED + Program Lead.
7. Send via `gmail-mcp` to PO with cover note + LOI PDF attached.

**Result:** Sent LOI with PO addressed by name; logged in Notion pipeline as "LOI sent" with expected decision date.

### Example 2: LOI to a national family foundation for a research project

**Goal:** 2-page LOI to the Robert Wood Johnson Foundation for a $250K policy research project.

**Steps:**
1. Scrape RWJF's "areas of focus" page; identify "Healthy Communities" priority.
2. Pull PO name from staff page.
3. Email PO requesting a 15-minute fit call.
4. Draft LOI emphasizing rigorous research methodology + dissemination to policymakers — RWJF priorities.
5. Cite primary-source data from CDC + Census + peer-reviewed studies (RWJF reviewers expect academic rigor).
6. Word-count check: aim for 900 words (RWJF caps LOIs at 2 pages).
7. Send via RWJF online portal (most large foundations require portal submission).

**Result:** LOI in RWJF portal; PO call done; expected response 60-90 days.

## Edge cases / gotchas

- **Strict page limits:** Most funders cap at 2-3 pages and will reject over-length LOIs without reading. Confirm cap on funder's "how to apply" page.
- **Single-spaced, 11-12pt, 1" margins:** Default. Some funders mandate 12pt or 1.5-spacing — verify per funder.
- **No appendices unless invited:** Don't append logic model, budget, letters of support unless funder allows. Save for the full proposal.
- **PO outreach before LOI:** Some funders explicitly forbid PO contact before submission. Read the "contact us" page; if it says "do not contact program staff before submission" — honor it.
- **Don't reuse without revision:** Funders cross-reference LOIs against peer orgs' submissions. Generic LOIs get caught. Each LOI must mirror that funder's priority language and reference their recent grants.
- **Tracking:** Log every LOI in Notion pipeline with funder, date sent, PO, expected decision date, full-proposal deadline if invited.
- **"Unsolicited" foundations:** Many large foundations (Gates, Ford) explicitly do not accept unsolicited LOIs. Confirm before drafting — sending an unsolicited LOI to a "no unsolicited" funder burns goodwill.
- **Tone mismatch:** Corporate LOIs tilt toward brand benefit + employee engagement; foundation LOIs tilt toward mission alignment + outcomes evidence. Wrong tone = decline.
- **Quantified need is non-negotiable:** "Many families face food insecurity" is decline-bait. "In 2025, 23.5% of Alameda County children under 5 lived in food-insecure households (USDA Economic Research Service, 2025)" is the bar.

## Sources

- Northwestern Foundation Relations — Letter of Inquiry guide: https://www.northwestern.edu/foundationrelations/grant-writing-guide/proposal-resources/letter-of-inquiry/
- Get Fully Funded — Killer LOI: https://getfullyfunded.com/how-to-write-a-killer-letter-of-inquiry-loi-to-get-a-grant/
- Spark the Fire — LOI guide 2026: https://sparkthefiregrantwriting.com/blog/loi
- Inside Philanthropy — LOI Explainer: https://www.insidephilanthropy.com/explainers/what-is-a-letter-of-inquiry-loi
- Candid — How to write an LOI: https://candid.org/
