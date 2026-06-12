<!--
Source: https://www.workiva.com/solutions/sec-reporting
Source: https://www.workiva.com/blog/sec-edgar-next-filer-access-2025
Source: https://www.sec.gov/about/forms/form10-k.pdf
Source: https://www.sec.gov/about/forms/form10-q.pdf
Source: https://www.intelligize.com/sec-filings
Source: https://www.dfin.com/products/edgar-pro-rdg
Reference role.md: "10-K drafting playbook" + "10-Q drafting playbook"
Round 2 enrichment: full Item-by-Item structure + Workiva REST + XBRL + Item 1C cyber + counsel review checklist + EDGAR Next workflow.
-->

# 10-K / 10-Q narrative drafting (Workiva + SEC EDGAR Next)

Drafts the narrative sections of 10-K (annual) and 10-Q (quarterly) for public companies, using Workiva as the single-source-of-truth XBRL-tagged drafting platform. Coordinates with `finance-agent` on the financial statements and defers binding filing sign-off to `legal-counsel`.

## When to use

- Drafting Item 1 Business / Item 1A Risk Factors / Item 1C Cybersecurity / Item 7 MD&A / Item 7A Quantitative + Qualitative Market Risk for 10-K.
- Drafting MD&A + material risk-factor updates for 10-Q.
- Building precedent-comparison redlines via Intelligize / Workiva diff.
- Item 1C Cybersecurity disclosure (post-SEC 2023 cyber rule).
- Trigger phrases: "10-K drafting", "10-Q drafting", "Risk Factors update", "MD&A", "annual report narrative", "Item 1C cyber".

NOT for: financial statements (use `finance-agent`); 8-K event reporting (use `8k-event-reporting`); proxy statement (use `proxy-statement-drafting`); CEO letter (use `quarterly-board-letter`).

## Setup

```bash
# Workiva (preferred — $50K+/yr; recipient supplies key)
export WORKIVA_API_KEY="<from Workiva Admin -> API>"
export WORKIVA_ORG_ID="<from Workiva Admin>"

# SEC EDGAR Next 2025 protocol (filer access, counsel-driven onboarding)
export SEC_EDGAR_USER_AGENT="Investor Relations <ir@company.com>"

# Alt platforms (recipient may use):
# - Donnelley RDG (DFIN) — incumbent: https://www.dfin.com/products/edgar-pro-rdg
# - Toppan Merrill — alt
# - Intelligize — redline vs precedent: https://www.intelligize.com/sec-filings
```

Auth / API key requirements:
- `WORKIVA_API_KEY` — Workiva subscription required for REST; free fallback is `docx` + SEC.gov direct EDGAR.
- `SEC_EDGAR_USER_AGENT` — mandatory for SEC EDGAR API (must include contact email).
- `INTELLIGIZE_API_KEY` — optional; redline vs precedent disclosures.

Data inputs:
- Prior-year 10-K + last 4 10-Qs (own filings) for baseline structure.
- 2-3 peer 10-Ks for Risk Factor + MD&A pattern mining.
- `finance-agent`: financial statements + footnotes + segment disclosures (XBRL-tagged).
- Cybersecurity risk register (CISO + IT + GC sign-off) for Item 1C.
- Counsel-supplied template language for Safe Harbor, Reg S-K Item 105 risk-factor framing.

## 10-K Item-by-Item structure

**Part I**
- Item 1: Business
- Item 1A: Risk Factors (~30-80 risks; ordered by materiality)
- Item 1B: Unresolved Staff Comments (rarely populated)
- Item 1C: **Cybersecurity** (post-2023 SEC rule — risk mgmt, governance, incidents)
- Item 2: Properties
- Item 3: Legal Proceedings
- Item 4: Mine Safety Disclosures (if applicable)

**Part II**
- Item 5: Market for Registrant's Common Equity, Related Stockholder Matters
- Item 6: [Reserved]
- Item 7: MD&A (Management's Discussion & Analysis)
- Item 7A: Quantitative & Qualitative Disclosures About Market Risk
- Item 8: Financial Statements + Supplementary Data (`finance-agent` owns)
- Item 9: Changes in / Disagreements With Accountants
- Item 9A: Controls and Procedures (SOX 302 + 404)
- Item 9B: Other Information
- Item 9C: Foreign Jurisdictions Preventing Inspections

**Part III** (often incorporated by reference to proxy)
- Items 10-14 (directors, exec comp, ownership, related-party, principal accountant fees)

**Part IV**
- Item 15: Exhibits + Financial Statement Schedules
- Item 16: 10-K Summary (optional)

## 10-Q simplified structure

**Part I — Financial Information**
- Item 1: Financial Statements (unaudited, `finance-agent`)
- Item 2: MD&A (narrative; material changes only)
- Item 3: Quantitative + Qualitative Market Risk (changes only)
- Item 4: Controls + Procedures

**Part II — Other Information**
- Item 1: Legal Proceedings (material changes)
- Item 1A: Risk Factors (material changes only; "from our most recent Form 10-K")
- Items 2-6: Sales of Unregistered Securities, Defaults, Mine Safety, Other, Exhibits

## Common recipes

### Recipe 1 — Pull last year's 10-K
```bash
mcp call sec-edgar-mcp fetch_form --ticker=$TICKER --form=10-K --year=$PRIOR_YEAR
```
Returns structured Item-by-Item.

### Recipe 2 — Pull 2-3 peer 10-Ks for pattern mining
```bash
for peer in $PEER_TICKERS; do
  mcp call sec-edgar-mcp fetch_form --ticker=$peer --form=10-K --year=$PRIOR_YEAR
done
```
Especially useful for Item 1A Risk Factors and Item 1C Cybersecurity.

### Recipe 3 — Workiva: create new 10-K from template
```bash
curl -X POST -H "Authorization: Bearer $WORKIVA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "template_id": "10-K-base",
    "fiscal_year": 2026,
    "title": "ACME 10-K FY2026"
  }' \
  "https://api.workiva.com/v1/documents"
```

### Recipe 4 — Workiva: diff vs prior period
```bash
curl -H "Authorization: Bearer $WORKIVA_API_KEY" \
  "https://api.workiva.com/v1/documents/$DOC_ID/diff?baseline=$PRIOR_DOC_ID"
```
Workiva diff highlights every change; flag any unchanged Risk Factor for review (boilerplate that hasn't aged is a red flag).

### Recipe 5 — XBRL tagging (Workiva embedded)
```bash
curl -H "Authorization: Bearer $WORKIVA_API_KEY" \
  "https://api.workiva.com/v1/documents/$DOC_ID/xbrl/validate"
```
Catches XBRL tagging errors before EDGAR submission.

### Recipe 6 — SEC EDGAR Next submission (filer access)
```bash
# EDGAR Next 2025 protocol: API submission replaces filer console upload
curl -X POST -H "User-Agent: $SEC_EDGAR_USER_AGENT" \
  -F "form=10-K" \
  -F "package=@10K_filing_package.zip" \
  "https://api.sec.gov/edgar/v1/submissions"
```
Counsel-supervised; binding filing.

### Recipe 7 — Item 1A Risk Factor refresh
```python
# Pattern: pull our prior RFs + peer RFs; cluster by topic; refresh language
TOPICS = [
    "macro / interest rate", "competitive", "regulatory", "cyber",
    "concentration", "supply chain", "IP", "litigation", "talent",
    "AI / LLM dependency", "climate / physical risk", "geopolitical"
]
# For each topic: keep if still material; refresh language if stale (2+ yr unchanged); drop if no longer material.
```

### Recipe 8 — Item 1C Cybersecurity walkthrough
```
Required sub-items (SEC 2023 cyber rule):
1. Risk management + strategy (processes for assessing, identifying, managing)
2. Engagement of consultants / auditors / third parties
3. Whether risks have materially affected (or reasonably likely to) the registrant
4. Governance — board oversight, management role, expertise
5. Material cybersecurity incidents (cross-ref 8-K Item 1.05)
```
**Defer binding language to `legal-counsel` + CISO**.

### Recipe 9 — Item 7 MD&A: results of operations
```
Standard structure:
1. Overview (3-5 paragraphs: macro + strategic frame)
2. Results of Operations (YoY by segment + drivers)
3. Liquidity + Capital Resources (cash position, sources, capex, covenants)
4. Critical Accounting Estimates (judgment-heavy; coordinate w/ auditors)
5. Off-balance-sheet arrangements (rare)
6. Recent Accounting Pronouncements (if applicable)
```

### Recipe 10 — Intelligize redline against peer
```bash
curl -H "Authorization: Bearer $INTELLIGIZE_API_KEY" \
  "https://api.intelligize.com/v1/compare?doc=$OUR_DOC&peer=$PEER_DOC"
# Identifies language we are missing that peers disclose (or vice versa)
```

### Recipe 11 — `finance-agent` hand-off
```python
# Financial statements are `finance-agent`'s domain
# We hand off:
# - Item 8 Financial Statements + footnotes
# - Item 7 financial-data tables (MD&A narrative pulls from these)
# - Item 9A SOX 302/404 attestation (CFO signs)
```

## Examples

### Example 1: 10-K full cycle (mid-cap)

**Goal:** FY2026 10-K filed within 60 days of fiscal year-end (large accelerated filer).

**Steps:**
1. T-60: Pull prior 10-K (Recipe 1) + 3 peer 10-Ks (Recipe 2).
2. T-55: Open Workiva 10-K shell (Recipe 3); seed each Item from prior year baseline.
3. T-45: Refresh Item 1A Risk Factors (Recipe 7); 6 deletions, 4 additions (AI / LLM dependency, supply chain Mexico tariff, etc.).
4. T-40: Draft Item 1C Cybersecurity (Recipe 8) — CISO walkthrough; counsel review.
5. T-35: Draft Item 7 MD&A (Recipe 9) using `finance-agent`'s tables.
6. T-25: Workiva diff vs prior (Recipe 4); flag unchanged RFs for fresh review.
7. T-20: XBRL validate (Recipe 5).
8. T-15: Counsel + audit committee + auditor review pass.
9. T-7: Intelligize redline vs 2 peers (Recipe 10).
10. T-3: Final lock.
11. T-0: SEC EDGAR Next submission via Workiva integration; CFO + CEO + audit committee sign-off.

**Result:** 10-K filed on time; XBRL clean; counsel + auditors signed; analyst notes cite "clean disclosure."

### Example 2: Item 1A Risk Factor add for AI dependency (2026)

**Goal:** Add a new Risk Factor — dependency on third-party LLM providers.

**Steps:**
1. Pull 5 peer 10-Ks (Recipe 2) — see how Microsoft, Salesforce, ServiceNow framed AI/LLM risk.
2. Draft factor (200-400 words):
   - Risk: Reliance on OpenAI, Anthropic, Google LLM APIs creates dependency.
   - Impact: API price changes, rate limits, model deprecations, terms changes could materially affect our cost of revenue and product capability.
   - Mitigation: multi-provider strategy, fine-tuned in-house fallback models, contractual commitments.
3. Counsel review (legal sufficiency under Reg S-K Item 105).
4. Insert into Item 1A in topic-ordered position.

**Result:** Counsel-approved RF; sets up disclosure of mid-year LLM-related events without surprise.

## Edge cases / gotchas

- **Item 1A boilerplate without refresh = SEC comment letter risk.** Any RF unchanged 3+ years gets SEC staff attention.
- **Item 1C Cybersecurity sub-item coverage.** All 5 sub-items must be addressed; missing one triggers SEC comment.
- **Item 1C 8-K material incident cross-ref.** Any 8-K Item 1.05 cyber filing within the year must be cross-referenced in 10-K Item 1C.
- **MD&A YoY granularity.** Drivers must be quantified ($X of $Y change came from price, $Z from volume).
- **Reg G non-GAAP rules in MD&A.** Every non-GAAP measure needs reconciliation; equal-or-greater-prominence rule for GAAP.
- **XBRL tagging errors block EDGAR submission.** Run Recipe 5 multiple times; tagging is unforgiving.
- **EDGAR Next 2025 protocol.** Filer access changed in 2025; recipient must onboard with SEC EDGAR Next first (counsel-supervised) before API submission works.
- **Workiva paywall.** $50K+/yr. Free fallback: `docx` + `sec-edgar-mcp` for fetch + SEC EDGAR direct submission via filer console.
- **Item 7A market-risk disclosures.** Often skipped or thin; SEC reviews for substance (interest rate, FX, commodity).
- **Filing deadlines (large accelerated filer).** 10-K 60 days from FY end; 10-Q 40 days from Q end. Smaller filers have longer.
- **Item 9A SOX 302/404 attestation.** CFO + CEO sign; cannot be IR-drafted (executive officer attestation).
- **Forward-looking statements in MD&A.** All must be covered by Safe Harbor; counsel review essential.
- **Critical Accounting Estimates section.** Should reflect material judgment areas (not boilerplate); auditor coordination required.

> Mandatory disclaimer: 10-K and 10-Q are binding SEC filings. **Consult licensed securities counsel** for every aspect of 10-K / 10-Q drafting — Reg S-K compliance, Safe Harbor framing, forward-looking statement coverage, Item 1A risk factor sufficiency, Item 1C cybersecurity disclosure, MD&A Reg G compliance, and EDGAR Next submission. This skill drafts to a counsel-reviewable bar; counsel approves binding filing.

## Sources

- Workiva SEC Reporting: https://www.workiva.com/solutions/sec-reporting
- Workiva SEC EDGAR Next 2025: https://www.workiva.com/blog/sec-edgar-next-filer-access-2025
- SEC Form 10-K Instructions: https://www.sec.gov/about/forms/form10-k.pdf
- SEC Form 10-Q Instructions: https://www.sec.gov/about/forms/form10-q.pdf
- SEC 2023 Cybersecurity Rule (Item 1C + 8-K Item 1.05): https://www.sec.gov/news/press-release/2023-139
- SEC Reg S-K (10-K + 10-Q content): https://www.ecfr.gov/current/title-17/chapter-II/part-229
- Intelligize SEC Filings (redline platform): https://www.intelligize.com/sec-filings
- DFIN Donnelley RDG (alt): https://www.dfin.com/products/edgar-pro-rdg
- See `role.md` -> "10-K drafting playbook" + "10-Q drafting playbook"

## Related skills

- `8k-event-reporting` — interim event reporting between 10-Q / 10-K.
- `proxy-statement-drafting` — Part III items often incorporated by reference.
- `esg-investor-reporting-gri-sasb-tcfd` — climate disclosure in 10-K Item 1 / 1A.
- `quarterly-earnings-press-release` — paired with 10-Q timing.
