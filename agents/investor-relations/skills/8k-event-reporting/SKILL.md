<!--
Source: https://www.sec.gov/about/forms/form8-k.pdf
Source: https://www.workiva.com/solutions/sec-reporting/8-k-filings
Source: https://www.notified.com/products/press-release-distribution
Source: https://www.businesswire.com/portal/site/home/ir/
Source: https://www.prnewswire.com/services/financial-disclosure/
Reference role.md: "8-K event reporting playbook"
Round 2 enrichment: per-Item-number trigger-to-draft templates + Reg FD pairing for Item 7.01 + counsel-handoff checklist + paired wire release.
-->

# 8-K event reporting (4-business-day trigger)

Drafts 8-K event reports for public companies and paired press releases. 8-K must be filed within 4 business days of a triggering event (or sooner for Item 1.05 cyber and Item 8.01 Reg FD). This skill covers the most common items (1.01, 2.02, 2.03, 5.02, 7.01, 8.01, 1.05) and the paired wire-distribution workflow.

## When to use

- Material agreement signed (Item 1.01) — major customer contract, M&A, debt financing.
- Earnings press release attaches an 8-K Item 2.02 by convention.
- Officer / director change (Item 5.02).
- Reg FD disclosure when intentional public disclosure is the chosen path (Item 7.01).
- Other material event (Item 8.01).
- Material cybersecurity incident (Item 1.05; 4-business-day clock from materiality determination).
- Trigger phrases: "8-K", "8-K filing", "material event disclosure", "trigger event 8-K", "press release + 8-K".

NOT for: 10-K / 10-Q (use `10k-10q-drafting-workiva`); DEF 14A (use `proxy-statement-drafting`); dividend / buyback details narrative (use `dividend-buyback-secondary-comms`); M&A investor comms package (use `ma-investor-comms`).

## Setup

```bash
# Workiva for drafting (preferred)
export WORKIVA_API_KEY="<from Workiva Admin -> API>"

# Wire distribution (recipient picks one)
export NOTIFIED_API_KEY="<from Notified Settings>"
export BUSINESSWIRE_API_KEY="<from Business Wire Portal -> Developer>"
export PRNEWSWIRE_API_KEY="<from PR Newswire Account>"
export GLOBENEWSWIRE_API_KEY="<from Globe Newswire>"

# SEC EDGAR Next filer access
export SEC_EDGAR_USER_AGENT="Investor Relations <ir@company.com>"
```

Auth / API key requirements:
- `WORKIVA_API_KEY` — Workiva subscription ($50K+/yr). Free fallback: `docx` + SEC.gov EDGAR direct.
- Wire-distribution API keys — per-release pricing ($500-$5K). Pick one based on existing vendor contract.
- `SEC_EDGAR_USER_AGENT` — required for SEC EDGAR API (must include contact email).

Data inputs:
- Trigger event detail (counsel-vetted materiality determination).
- Counsel-supplied template language for the relevant Item.
- Press release draft (if Item is wire-paired).
- For Item 5.02: officer bio, separation agreement summary, any 10b5-1 plan.
- For Item 1.05: incident scope, materiality determination, remediation status.

## Reportable items (most common — full list in Form 8-K instructions)

| Item | Trigger | Deadline | Wire? |
|------|---------|----------|-------|
| 1.01 | Entry into material definitive agreement | 4 bus days | Often |
| 1.02 | Termination of material definitive agreement | 4 bus days | Sometimes |
| 1.05 | Material cybersecurity incident | 4 bus days from materiality determination | Yes |
| 2.01 | Completion of acquisition / disposition | 4 bus days | Yes |
| 2.02 | Results of operations + financial condition (earnings) | 4 bus days | Yes (paired with earnings release) |
| 2.03 | Material direct financial obligation | 4 bus days | Sometimes |
| 2.05 | Costs from exit / disposal activities | 4 bus days | Sometimes |
| 3.02 | Unregistered sales of equity | 4 bus days | Sometimes |
| 4.02 | Non-reliance on prior financials | 4 bus days | Yes |
| 5.02 | Officer / director appointment / departure / comp changes | 4 bus days | Often |
| 5.07 | Submission of matters to security holders (annual meeting results) | 4 bus days | Sometimes |
| 7.01 | Reg FD disclosure | "promptly" (24 hours conventional) | Yes |
| 8.01 | Other events (catch-all) | Discretionary timing | Often |

## Workflow

1. Identify trigger Item number + confirm 4-business-day window (counsel-vetted).
2. Draft press release first (if paired).
3. Draft 8-K body (Workiva or `docx` fallback).
4. Counsel review (always).
5. **Wire-to-public** via Notified / Business Wire / PR Newswire / Globe Newswire.
6. **EDGAR submission** via Workiva integration or SEC EDGAR Next.
7. Cross-link IR website (post 8-K + press release).
8. Post-file: shareholder Q&A library update (`shareholder-qa-maintenance`).

## Common recipes

### Recipe 1 — Pull peer 8-K precedent
```bash
mcp call sec-edgar-mcp fetch_form --ticker=$PEER_TICKER --form=8-K --item=$ITEM --limit=5
```
For each Item, find 5 most recent peer precedents to pattern-match language.

### Recipe 2 — Item 2.02 earnings 8-K (paired with press release)
```python
# Standard body for Item 2.02:
ITEM_2_02_BODY = """
On {date}, {Registrant} issued a press release announcing financial results for
the {period}. A copy of the press release is furnished as Exhibit 99.1 to this Form 8-K.

The information furnished pursuant to this Item 2.02, including Exhibit 99.1, shall
not be deemed "filed" for purposes of Section 18 of the Securities Exchange Act of
1934, as amended, or otherwise subject to the liabilities of that section, and shall
not be incorporated by reference into any registration statement or other document
filed under the Securities Act of 1933, except as expressly set forth by specific
reference in such a filing.
"""
```
The "furnished not filed" language is standard — counsel-supplied.

### Recipe 3 — Item 5.02 officer departure
```python
ITEM_5_02_BODY = """
On {effective_date}, {Officer Name}, the {Title} of {Registrant}, {departed/resigned}.
[Optional: reason if material; "not due to any disagreement with the Registrant on any
matter relating to the Registrant's operations, policies or practices" is the standard
no-disagreement framing.]

In connection with the {departure/resignation}, {Registrant} entered into a
{separation agreement / release} on {date}, which provides for: [summary of severance,
equity treatment, restrictive covenants]. The {agreement} is filed as Exhibit 10.1.
"""
```

### Recipe 4 — Item 7.01 Reg FD intentional disclosure
```python
# Use Item 7.01 when intentionally disclosing material info that wasn't simultaneously
# public — e.g., reaffirming guidance in a 1:1 with an analyst after a question that
# went into MNPI territory. Standard timing: file within 24 hours.
ITEM_7_01_BODY = """
On {date}, {Registrant} {presented/disclosed} certain information regarding its
{topic}. A copy of the {presentation/transcript} is furnished as Exhibit 99.1.
[Standard furnished-not-filed paragraph]
"""
```

### Recipe 5 — Item 1.05 cybersecurity material incident
```python
ITEM_1_05_BODY = """
On {determination_date}, {Registrant} determined that a cybersecurity incident
identified on {discovery_date} is material. The incident involved [description
of nature + scope + timing + impact, omitting specific technical details that
could impede remediation or aid further attack]. Remediation actions taken
to date include [summary]. The Registrant continues to investigate and may
amend this report as additional material information becomes available.
"""
# 4-business-day clock starts at materiality determination, NOT discovery.
```
Counsel + CISO + GC required before file.

### Recipe 6 — Workiva 8-K from template
```bash
curl -X POST -H "Authorization: Bearer $WORKIVA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"template_id": "8-K-base", "item": "2.02", "trigger_date": "2026-07-30"}' \
  "https://api.workiva.com/v1/documents"
```

### Recipe 7 — Submit press release via Business Wire
```bash
curl -X POST -H "Authorization: Bearer $BUSINESSWIRE_API_KEY" \
  -H "Content-Type: application/json" \
  -d @press_release.json \
  "https://api.businesswire.com/v2/releases"
# Schedule: T-30 minutes before market close OR T+0 pre-market (per convention)
```

### Recipe 8 — Submit via PR Newswire
```bash
curl -X POST -H "Authorization: Bearer $PRNEWSWIRE_API_KEY" \
  -d @release.json \
  "https://api.prnewswire.com/v2/releases"
```

### Recipe 9 — SEC EDGAR Next 8-K submission
```bash
# Workiva integrated submission (preferred)
curl -X POST -H "Authorization: Bearer $WORKIVA_API_KEY" \
  -d '{"action": "file_to_edgar", "doc_id": "'"$DOC_ID"'"}' \
  "https://api.workiva.com/v1/documents/$DOC_ID/submit"
# OR SEC EDGAR Next direct (counsel-supervised)
```

### Recipe 10 — Cross-link IR website (Q4)
```bash
curl -X POST -H "Authorization: Bearer $Q4_API_KEY" \
  -d '{"type": "8K", "title": "...", "url": "https://sec.gov/...", "pub_date": "..."}' \
  "https://api.q4inc.com/v1/sec-filings"
```

## Examples

### Example 1: Earnings 8-K (Item 2.02 + 99.1 press release)

**Goal:** Q2 earnings released after market close 2026-07-30.

**Steps:**
1. Press release drafted via `quarterly-earnings-press-release`.
2. Draft Item 2.02 body (Recipe 2); attach press release as Exhibit 99.1.
3. Counsel review.
4. T-15 min: Business Wire embargo lifts (Recipe 7).
5. T-0 (4:01 PM ET): Press release hits wire; simultaneously Workiva submits 8-K to EDGAR (Recipe 9).
6. T+5 min: Cross-link on IR website (Recipe 10).
7. T+25 min: Earnings call begins (paired with `earnings-call-script-qa`).

**Result:** Coordinated wire + EDGAR + IR website all within 5 minutes; no Reg FD gap.

### Example 2: Officer departure (Item 5.02)

**Goal:** CFO resignation effective 2026-08-15; announce 2026-08-15 close.

**Steps:**
1. Draft press release (factual, no disagreement language counsel-supplied).
2. Draft Item 5.02 body (Recipe 3); attach separation agreement as Exhibit 10.1.
3. Disclose interim CFO appointment (also Item 5.02 sub-paragraph (c)).
4. Counsel review (binding language, especially "no disagreement").
5. T-0 (4:01 PM ET 2026-08-15): wire + EDGAR file simultaneously.
6. Pre-brief top analysts within 30 min via Reg-FD-compliant 1:1s (no MNPI).
7. T+1: Update IR website leadership page.

**Result:** Departure disclosed cleanly; no leak risk; analyst notes calm.

### Example 3: Item 1.05 cyber incident

**Goal:** Material cyber incident discovered 2026-09-01; materiality determined 2026-09-05.

**Steps:**
1. CISO incident report + counsel materiality determination 2026-09-05.
2. 4-business-day clock starts 2026-09-05; deadline 2026-09-11.
3. Draft Item 1.05 body (Recipe 5); CISO + counsel + GC review.
4. Coordinate with `legal-counsel` on what NOT to disclose (technical detail that aids attacker).
5. T-0: EDGAR file + wire-to-public.
6. Plan for amendment if material new info emerges.

**Result:** Compliant filing within 4 business days; remediation continues; potential amendment trail.

## Edge cases / gotchas

- **4-business-day clock — when does it start?** Item 1.05 starts at materiality determination, not discovery; Item 1.01 at execution of definitive agreement (not LOI); Item 5.02 at decision (resignation accepted), not effective date.
- **"Furnished" vs "filed" distinction.** Items 2.02 and 7.01 default to "furnished" (lower liability); Items 1.01, 5.02 are "filed" (higher liability + incorporated by reference into S-3 registrations). Counsel chooses.
- **Reg FD intentional vs unintentional.** Intentional → file 7.01 simultaneously; unintentional → "promptly" (24-hour standard).
- **8-K + 10-Q overlap.** If a triggering event happens close to 10-Q filing, can disclose in 10-Q instead of separate 8-K (counsel call).
- **Item 5.02(e) compensation disclosure.** New executive comp arrangements that are material trigger Item 5.02(e), not just 5.02(c).
- **Cyber incident scope creep.** Item 1.05 disclosure is high-level by design; resist pressure to disclose technical detail.
- **Wire-vs-EDGAR timing skew.** Goal is simultaneous; in practice <5 min apart. Wire-first then EDGAR is OK; EDGAR-first then wire creates Reg FD risk (EDGAR is technically public but not widely scanned).
- **Workiva paywall.** Free fallback: `docx` draft + SEC.gov direct EDGAR submission (counsel-supervised).
- **Forgetting to update IR website.** Q4 / Notified IR-website cross-link should follow the wire by minutes.
- **Item 8.01 over-use.** Companies that use 8.01 for everything dilute its signal; reserve for genuinely "other."
- **Counsel typo trap.** "Resignation" vs "departure" vs "termination" have different legal weights; never edit counsel's word choice.

> Mandatory disclaimer: 8-K is a binding SEC filing. **Consult licensed securities counsel** for materiality determination, Item selection, Safe Harbor coverage, "furnished" vs "filed" framing, Reg FD interpretation, and EDGAR submission. This skill drafts to a counsel-reviewable bar; counsel approves binding filing.

## Sources

- SEC Form 8-K Instructions: https://www.sec.gov/about/forms/form8-k.pdf
- SEC 8-K Reportable Events Rule: https://www.sec.gov/rules/final/33-8400.htm
- SEC 2023 Cybersecurity Rule (Item 1.05): https://www.sec.gov/news/press-release/2023-139
- Workiva 8-K Filings: https://www.workiva.com/solutions/sec-reporting/8-k-filings
- Notified Press Release Distribution: https://www.notified.com/products/press-release-distribution
- Business Wire IR: https://www.businesswire.com/portal/site/home/ir/
- PR Newswire Financial Disclosure: https://www.prnewswire.com/services/financial-disclosure/
- Globe Newswire: https://www.globenewswire.com/
- SEC Regulation FD Interpretations: https://www.sec.gov/divisions/corpfin/guidance/regfd-interp.htm
- See `role.md` -> "8-K event reporting playbook"

## Related skills

- `quarterly-earnings-press-release` — paired with Item 2.02.
- `ma-investor-comms` — paired with Item 1.01 / 2.01.
- `dividend-buyback-secondary-comms` — paired with Item 1.01 / 8.01.
- `embargoed-disclosure-protocols` — embargo timing around 8-K wire.
- `10k-10q-drafting-workiva` — overlap when event close to periodic filing.
