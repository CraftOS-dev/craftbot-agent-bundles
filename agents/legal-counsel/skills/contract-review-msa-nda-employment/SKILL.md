---
name: contract-review-msa-nda-employment
description: Primary contract review playbook covering MSAs, SOWs, NDAs, employment / contractor / vendor / SaaS agreements. Walks the clause checklist, quantifies flags (high/medium/low), produces a redline + memo with the consult-an-attorney disclaimer. Pair with `robin-spellbook-harvey-ai-contract-review` for AI-assisted first-pass markup over 10 pages.
---

# Contract Review — MSA / NDA / Employment / Contractor / Vendor

The workhorse contract-review skill. The agent uses this for ANY contract review unless the contract is a privacy / IP / equity / fundraising document (those have dedicated skills).

## When to use

Reach for this skill when the user says any of:

- "Review this MSA / NDA / employment / contractor / vendor / SaaS agreement"
- "Redline this contract"
- "What are the risky terms in this contract?"
- "Draft an NDA / MSA / contractor agreement"
- "Negotiate the indemnity / limitation of liability / IP / data clause"
- "Is this BAA / SLA / AUP standard?"
- "What's market for the [clause] in 2026?"
- "Compare this to Common Paper / Bonterms"

Do NOT use this skill for: privacy policies (`privacy-policy-gdpr-ccpa`), term sheets (`term-sheet-review-series-a-typical-terms`), founders agreements (`founders-agreement-vesting-ip-assignment`), SAFEs (`safe-convertible-note-yc-template`), equity grants (`equity-grants-isos-rsus-83b-election`), DPA (`dpa-data-processing-agreement`).

## Setup

```bash
# Document normalization (extract text from PDF / scanned contracts)
which pdftotext || (apt-get install -y poppler-utils || brew install poppler)
which pandoc || (apt-get install -y pandoc || brew install pandoc)

# Diff + redline visualization
pip install diff-match-patch
npm i -g docx-diff       # produces .docx redlines from two .docx inputs

# Template fetchers (used in recipes)
curl -fsSL -o common-paper-mnda.pdf https://commonpaper.com/standards/mutual-nda/
curl -fsSL -o bonterms-cloud.docx https://bonterms.com/forms/cloud-terms

# Optional: Robin AI / Spellbook for AI-assisted redlines (see sister skill)
# Optional: LegalSifter for concept-extraction; OCR via gemini-ocr-mcp / mistral-ocr-mcp for scanned contracts
```

Auth / API keys:
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` — if using LLM for clause-by-clause classification.
- No API keys required for Common Paper / Bonterms — both are open templates.

## Common recipes

### Recipe 1: Normalize input contract to text
```bash
pdftotext -layout input_contract.pdf input_contract.txt
# Or via pandoc for .docx
pandoc input_contract.docx -o input_contract.md --wrap=preserve
```
Always normalize before reading. PDFs have line breaks / hyphens that destroy regex; pandoc-to-markdown preserves structure best.

### Recipe 2: Run the MSA clause checklist
```bash
# Build a checklist file from soul.md / role.md MSA playbook
cat > msa_checklist.md <<'EOF'
- [ ] Term + termination (notice, for cause, cure period, effect on accrued fees)
- [ ] IP ownership (vendor retains vs assigns; pre-existing carve-outs; licenses back)
- [ ] Payment terms (net 30/60/90, late fees, disputed amounts, setoff)
- [ ] SLA + remedies (uptime %, credits, cap on credits, sole-and-exclusive remedy)
- [ ] Warranties (scope, period, disclaimer)
- [ ] Indemnification (mutual?, IP indemnity, cap)
- [ ] Limitation of liability (cap amount, carve-outs)
- [ ] Confidentiality (term, return/destruction, residuals, permitted disclosures)
- [ ] Data protection (DPA, SCC for EU, sub-processor list)
- [ ] Audit rights (frequency, notice, scope, cost)
- [ ] Insurance (types, limits, additional insured)
- [ ] Force majeure (post-COVID drafting, mitigation duty)
- [ ] Assignment + change-of-control
- [ ] Governing law + venue + dispute resolution
- [ ] Notices + entire agreement + order of precedence
EOF
```
Walk this top-to-bottom. Each unchecked item becomes a finding in the memo.

### Recipe 3: Diff against Common Paper / Bonterms benchmark
```bash
# Pull a known-good benchmark and diff
curl -fsSL https://commonpaper.com/standards/cloud-service-agreement/ -o benchmark.html
pandoc benchmark.html -o benchmark.md

# Side-by-side diff
diff -u benchmark.md input_contract.md > deviations.diff
# Or word-level
wdiff benchmark.md input_contract.md > deviations.wdiff
```
The deviations file becomes the start of your flag list — anything materially different from the benchmark is a flag candidate.

### Recipe 4: Generate a flag table
```python
# flags.py — pandas-based scoring
import pandas as pd
flags = pd.DataFrame([
    {"section": "9.2 Indemnity", "issue": "Cap at 3-month fees; no carve-outs",
     "likelihood": "Med", "impact": "High", "tier": "HIGH",
     "redline": "Push cap to 12-month fees; carve out IP, confidentiality, data breach, willful misconduct"},
    {"section": "8.1 Auto-renewal", "issue": "12-month auto-renew, 90-day non-renewal notice",
     "likelihood": "High", "impact": "Med", "tier": "MED",
     "redline": "Tighten to 30-day notice; require 60-day reminder (CA SB-1659 model)"},
])
flags.to_markdown("flags.md", index=False)
```

### Recipe 5: Produce the redline (.docx)
```bash
# Take counterparty's .docx, apply tracked changes, save as redline
pip install python-docx
python -c "
from docx import Document
doc = Document('input_contract.docx')
# Programmatic clause replacement (preserve tracked-change markers)
# For complex redlines: open in Word + Track Changes ON; use Spellbook add-in
doc.save('input_contract_redlined.docx')
"
# Or use docx-diff
docx-diff original.docx revised.docx --output redline.docx
```

### Recipe 6: Produce the review memo (.docx / .md)
```markdown
# Contract Review Memo — <Counterparty> <Contract Type>

**Reviewed by:** Legal Counsel (AI agent)
**Date:** 2026-06-09
**Jurisdiction:** <state / country>
**Side:** <buyer | seller | mutual>

## Executive summary
- HIGH-tier flags: <count>
- MED-tier flags: <count>
- LOW-tier flags: <count>

## Material flags
### HIGH 1: Indemnity cap below market
- **Section:** 9.2
- **Issue:** Cap at 3 months of fees; no carve-outs.
- **Risk:** Below 2026 market (12 months is standard); no IP/confidentiality/data-breach carve-out caps your recovery on third-party claims.
- **Redline:** "...Provider's aggregate liability shall not exceed twelve (12) months of fees paid; provided that the foregoing cap shall not apply to (a) IP indemnification, (b) breach of confidentiality, (c) data breach, (d) willful misconduct or gross negligence, (e) indemnification for personal injury or property damage."
- **Citation:** Common Paper Cloud Service Agreement §9; Bonterms Cloud Terms §10.

[...repeat for each flag...]

## Recommendation
<accept | accept w/ redlines | reject>

---
**Disclaimer:** This is informational guidance from an AI agent, not legal advice. Always consult a licensed attorney in your jurisdiction before signing, filing, or executing binding legal documents. No attorney-client relationship is formed by this communication.
```

### Recipe 7: NDA-specific quick review
```bash
# Use Common Paper Mutual NDA as the benchmark
curl -fsSL -o cp-mnda.pdf https://commonpaper.com/standards/mutual-nda/
pdftotext cp-mnda.pdf cp-mnda.txt
diff -u cp-mnda.txt input_nda.txt > nda_deviations.diff
```
Key NDA flags to look for: (a) overbroad definition of Confidential Info, (b) missing exclusions (already known, independently developed, publicly available, required by law), (c) perpetual term (only OK for trade secrets specifically), (d) residuals clause (reject in most cases), (e) one-sided injunctive relief, (f) IP assignment slipped in (NDA is not an IP assignment vehicle).

### Recipe 8: Employment agreement — US state-aware
```bash
# Pull state-specific non-compete enforceability before drafting
curl -fsSL -o ncsl_noncompete.html https://www.ncsl.org/labor-and-employment/non-compete-agreements

# Pull current FTC Non-Compete Rule status (uncertain in 2026)
curl -fsSL -o ftc_noncompete.html https://www.ftc.gov/legal-library/browse/rules/noncompete-rule
```
Required clauses: at-will status (US default), comp + benefits + equity reference, classification (exempt/non-exempt FLSA), confidentiality, IP assignment with explicit "hereby assigns" + CA §2870 carve-out, non-solicit (more durable than non-compete), severance terms, choice of law/venue, mandatory arbitration + class waiver. Defer to `non-compete-non-solicit-state-enforceability` for state map.

### Recipe 9: Contractor agreement (IRS 20-factor + state ABC test)
```bash
curl -fsSL -o irs_contractor.html https://www.irs.gov/businesses/small-businesses-self-employed/independent-contractor-defined
# CA AB5 ABC test
curl -fsSL -o ca_ab5.html https://www.dir.ca.gov/dlse/faq_independentcontractor.htm
```
Critical clauses: (a) explicit IP assignment ("hereby assigns" — present-tense vesting), NOT just "work for hire" alone (software code is not in 17 USC §101 work-for-hire categories), (b) classification controls (avoid control over how work is done — only deliverables and deadlines), (c) no benefits / no withholding, (d) non-solicit ok, non-compete reject for contractors in most states.

### Recipe 10: Vendor / SaaS subscription (buyer-side)
Key flags: auto-renewal terms (negotiate 30-day notice), price escalators (cap at CPI or 5%), data ownership (you own your data), exit/portability (export rights + transition assistance), sub-processor consent, security warranties (SOC 2 / ISO 27001 reference), insurance limits ($5M cyber liability is market for B2B SaaS), assignment on CoC, force majeure with pandemic carve-in.

### Recipe 11: HIPAA Business Associate Agreement
```bash
curl -fsSL -o hhs_baa.html https://www.hhs.gov/hipaa/for-professionals/covered-entities/sample-business-associate-agreement-provisions/
```
Required elements per 45 CFR §164.504(e): (1) permitted/required uses + disclosures, (2) safeguards (admin/physical/technical), (3) report security incidents + breaches to CE within stated timeframe (60-day max), (4) ensure subcontractors agree to same restrictions, (5) provide access to PHI for individuals, (6) make available for HHS audit, (7) return / destroy PHI on termination.

### Recipe 12: Indemnity + LoL negotiation lever table

| Position | Buyer-friendly | Seller-friendly | Compromise |
|---|---|---|---|
| Liability cap | Unlimited / 24mo fees | 3-month fees / fees paid | 12-month fees (market) |
| IP indemnity | Uncapped | Subject to cap | Carve-out from cap |
| Data breach | Uncapped | Subject to cap | 2x-3x cap |
| Confidentiality breach | Uncapped | Subject to cap | Uncapped (market) |
| Willful misconduct / gross negligence | Uncapped | Subject to cap | Uncapped (market) |
| Consequential damages | Recoverable | Waived (both sides) | Mutual waiver (market) |
| Special / punitive | Recoverable | Waived | Mutual waiver |

## Examples

### Example 1: First MSA review (vendor SaaS, US buyer)
**Goal:** Review a 40-page vendor SaaS MSA before signing.
**Steps:**
1. `pdftotext -layout msa.pdf msa.txt` — normalize.
2. Walk Recipe 2 checklist; populate Recipe 4 flag table.
3. `diff -u benchmark_cp_cloud.md msa.md > deviations.diff` — compare to Common Paper Cloud Service Agreement.
4. Write redline in Word (Track Changes ON) following Recipe 5; for over-10-page contracts, use Spellbook from the sister skill `robin-spellbook-harvey-ai-contract-review`.
5. Write memo from Recipe 6 template.
6. Run `grep -i "consult a licensed attorney" memo.md` — verify disclaimer present.

**Result:** A flagged redline (.docx) + memo (.docx / PDF) ready to send to user's licensed counsel for final review and to counterparty for negotiation.

### Example 2: Mutual NDA between two startups
**Goal:** Draft a mutual NDA for a partnership exploration.
**Steps:**
1. `curl -fsSL https://commonpaper.com/standards/mutual-nda/ -o template.pdf`
2. Adapt the cover sheet (parties, purpose, term).
3. Verify exclusions (already known, independently developed, publicly available, required by law) are preserved.
4. Pick term: 2 years for general business, perpetual for trade secrets specifically.
5. Insert disclaimer in cover letter.

**Result:** A Common Paper mutual NDA with cover sheet customized for the deal.

## Edge cases / gotchas

- **Scanned PDFs (no text layer).** Run OCR first: `gemini-ocr-mcp` MCP or `mistral-ocr-mcp` MCP. Don't try to read raw image PDFs.
- **Definitions section traps.** Bad definitions break the rest of the contract. Specifically check "Services", "Deliverables", "Confidential Information", "Affiliates", "Acceptance", "Effective Date" BEFORE reading substantive clauses.
- **Order of precedence between MSA / SOW / Order Form / website terms.** When multiple docs reference each other, the order-of-precedence clause controls. Spotting an inverted hierarchy (e.g., website ToS overrides the MSA) is a common error.
- **CA Labor Code §2870 carve-out missing.** Required for CA employees / contractors in IP assignment clauses. Missing = unenforceable IP assignment for personal-time inventions.
- **"Work made for hire" alone for software.** Software code is NOT in the 17 USC §101 work-for-hire categories. Always include explicit "hereby assigns" backup language.
- **Auto-renewal traps.** CA Bus. & Prof. Code §17602, NY GBL §5-903, and many other states require specific consumer disclosures for auto-renewal. Failing the disclosure makes the auto-renewal voidable.
- **Indemnity-without-cap-carve-outs.** A cap at 12-month fees that also caps IP indemnity is below market. IP indemnity carve-out (or 2x-3x cap) is the standard ask.
- **Non-compete enforceability is volatile.** FTC Non-Compete Rule April 2024 was stayed by 5th Cir Aug 2024; status uncertain in 2026. Always fetch current FTC.gov page before drafting. See `non-compete-non-solicit-state-enforceability` skill.
- **EU contracts need DPA + SCC.** Any contract involving EU personal data needs an Art. 28 DPA AND EU SCCs (2021/914 set) AND a Transfer Impact Assessment post-Schrems II. Defer to `dpa-data-processing-agreement` skill.

> Warning: **This is informational guidance from an AI agent. Always consult a licensed attorney in your jurisdiction before signing, filing, or executing binding legal documents.**

## Sources

- [Common Paper Standards](https://commonpaper.com/standards/) — open contract templates (NDA, Cloud Service Agreement, DPA, AUP, SLA).
- [Bonterms](https://bonterms.com/) — open template library (Cloud Terms, AUP, DPA, SLA, IDA).
- [Cooley GO Documents](https://www.cooleygo.com/documents/) — equity, founders, contractor, consulting templates.
- [HHS Sample BAA](https://www.hhs.gov/hipaa/for-professionals/covered-entities/sample-business-associate-agreement-provisions/) — HIPAA Business Associate Agreement.
- [IRS Independent Contractor Defined](https://www.irs.gov/businesses/small-businesses-self-employed/independent-contractor-defined) — 20-factor test.
- [AAA Rules](https://www.adr.org/Rules) + [JAMS Rules](https://www.jamsadr.com/rules-clauses) — arbitration clause drafting.
- [FTC Non-Compete Rule](https://www.ftc.gov/legal-library/browse/rules/noncompete-rule) — current US federal status (volatile in 2026).
- [NCSL Non-Compete State Map](https://www.ncsl.org/labor-and-employment/non-compete-agreements) — state-by-state enforceability.
- [Robin AI](https://www.robinai.com/) + [Spellbook](https://www.spellbook.legal/) — AI-assisted contract review (sister skill).
- [Cornell LII 17 USC §101](https://www.law.cornell.edu/uscode/text/17/101) — work-for-hire definition.
