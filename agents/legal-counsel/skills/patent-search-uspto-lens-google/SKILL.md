---
name: patent-search-uspto-lens-google
description: Patent prior-art search + provisional vs non-provisional decision support — USPTO Patent Public Search (ppubs.uspto.gov), Google Patents, Lens.org, EPO Espacenet, WIPO Patentscope. Pre-disclosure + grace-period awareness + PCT filing prep. Output is a prior-art memo + filing recommendation with the consult-an-attorney disclaimer. Filing itself requires a registered patent attorney/agent.
---

# Patent Search — USPTO Patent Public Search / Google Patents / Lens.org

## When to use

User says:

- "Search patent for [tech]"
- "Is [invention] novel?"
- "Provisional vs non-provisional?"
- "Should I file a patent?"
- "Prior art search for [feature]"
- "PCT / international patent"
- "§101 / §102 / §103 issues?"
- "Patentability of software / AI / biotech"

Companion skills:
- `trademark-search-uspto-tess-wipo` — sister IP skill.

## Setup

```bash
# USPTO Patent Public Search
# https://ppubs.uspto.gov/
# Replaced PatFT/AppFT in 2022; current as of 2026

# Google Patents (best free interface)
# https://patents.google.com/

# Lens.org
# https://www.lens.org/

# EPO Espacenet (European + worldwide)
# https://worldwide.espacenet.com/

# WIPO Patentscope
# https://patentscope.wipo.int/

# uspto-mcp — direct queries from agent
# (Configured in app/config/mcp_config.json)

# Classification systems
# CPC (Cooperative Patent Classification — current): https://www.cooperativepatentclassification.org/
# IPC (International Patent Classification — legacy): https://www.wipo.int/classifications/ipc/en/

# USPTO Filing
# https://efs-web.uspto.gov/

# Python helpers
pip install requests beautifulsoup4 pandas
```

Auth / API keys:
- USPTO PPS / Google Patents / Lens.org: no key required for web.
- Lens.org API: free tier with key (https://www.lens.org/lens/user/subscriptions).
- USPTO filing: USPTO.gov account + Customer Number recommended.

## Common recipes

### Recipe 1: Scope determination — patent type
```python
# patent_scope.py
# What kind of patent?
invention_type = "utility"  # utility | design | plant

# Utility = process, machine, manufacture, composition of matter (35 USC §101)
# Design = ornamental design of an article (35 USC §171)
# Plant = new + distinct asexually reproduced plant variety (35 USC §161)

# For software / hardware founders: utility is the default
```

### Recipe 2: Find CPC classifications (search strategy)
```text
1. Open Google Patents: https://patents.google.com/
2. Search keywords for the invention area:
   - "user authentication" "biometric"
   - "machine learning" "training"
3. Look at top results' "CPC Classifications" header (e.g., G06F 21/32, G06N 3/088)
4. Pull all relevant CPC codes
5. Cross-reference at https://www.cooperativepatentclassification.org/cpcSchemeAndDefinitions/table
```

### Recipe 3: USPTO Patent Public Search (PPS)
```text
1. Visit https://ppubs.uspto.gov/pubwebapp/external.html?db=USPAT,USPAT_US-PGPUB,EPO,JPO,DERWENT
2. Enter Boolean / structured query:
   query := keywords AND CPC AND date
   - Example: "user authentication" AND CPC/G06F21/32 AND DD/2020:2026
3. Filter by:
   - Issue date / publication date
   - Patent type (utility / design / plant)
   - Status (granted / pending / abandoned)
4. Review each hit:
   - Title + Abstract + Claims (claims define the scope)
   - Inventors + Assignee
   - Forward + backward citations
5. Export top 20-50 references
```

### Recipe 4: Google Patents — best free interface
```text
1. Visit https://patents.google.com/
2. Use query: "user authentication biometric" assignee:Apple after:2018
3. Filters: jurisdiction (US, EP, WO, CN, JP), date, status
4. Result page shows: claims, drawings, citations, family
5. For each hit, click into:
   - Claims (the legal scope)
   - "Cited by" (forward citations — newer patents citing this one)
   - "References" (backward citations — what this patent cited)
6. Build a citation chain (3-5 hops typically catches the field)
```

### Recipe 5: Lens.org — patent + scholar cross-reference
```text
https://www.lens.org/
- Combines patent + non-patent literature (scholar)
- API for programmatic access
- Useful for: AI / ML / biotech where academic papers are key prior art
```

### Recipe 6: EPO Espacenet — European + worldwide
```text
https://worldwide.espacenet.com/
- 130M+ patent documents
- Smart search by family
- Patent family view = same invention filed in multiple jurisdictions
```

### Recipe 7: Prior-art memo skeleton
```markdown
# Prior-Art Search — <Invention>

## Invention summary
- Title:
- Inventors:
- Brief description (1-2 paragraphs):
- Key claims (independent claims):

## Search parameters
- Keywords:
- CPC classifications:
- Date range: <e.g., 2000-2026>
- Jurisdictions: US, EP, WO, CN, JP
- Databases: USPTO PPS, Google Patents, Lens, Espacenet

## Top 20 references

### Reference 1: US 11,XXX,XXX (Filed YYYY-MM-DD, Issued YYYY-MM-DD)
- Title:
- Assignee:
- Independent claim 1 summary:
- Relevance: HIGH / MED / LOW
- Notes:
- URL:

[...repeat for each reference...]

## Patentability assessment (35 USC §101-103)

### §101 Subject-matter eligibility
- Statutory category (process / machine / manufacture / composition)?
- Abstract idea exception (Alice / Mayo two-step):
  - Step 1: Directed to abstract idea? Yes / No
  - Step 2: Significantly more (inventive concept)? Yes / No
- Eligible / Concerns / Strong rejection risk
  
### §102 Novelty
- Identical disclosure in prior art? Yes / No
- If yes: which reference?

### §103 Non-obviousness
- Combination of references would make claim obvious to PHOSITA?
- Secondary considerations (commercial success, long-felt need, unexpected results)?

### Recommendation
- File as provisional / non-provisional / not patentable
- Suggested claim amendments to navigate prior art

---
**Disclaimer:** Prior-art search is informational, not a substitute for opinion of registered patent attorney/agent. Patentability decisions require professional review.
```

### Recipe 8: Provisional vs non-provisional decision
```text
PROVISIONAL ($60-300 micro entity / $130-300 small entity, $300+ standard):
- 12-month placeholder ("patent pending")
- No formal claims required (informal description ok)
- Preserves priority date for foreign filing
- USE WHEN:
  - Disclosure imminent (conference, paper, customer demo)
  - Need 12 months to refine invention
  - Budget-limited at filing time

NON-PROVISIONAL ($400 + $400-1820+ for small entity, more for standard):
- Substantive examination begins
- Formal claims required
- 18-24 month exam timeline typical
- $400-2,000+ in attorney fees plus USPTO fees
- Patent issued (if granted)

Conversion: convert provisional to non-provisional within 12 months (else lose priority).
```

### Recipe 9: Disclosure deadlines — 1-year US grace + foreign filing
```text
US 1-year grace period (35 USC §102(b)):
- After first public disclosure (publication, sale, public use, offer for sale)
- 12 months to file US patent
- Disclosure BY THE INVENTOR doesn't bar US filing within 12 months

FOREIGN: NO grace period in most jurisdictions
- EU, China, Japan, Korea require filing BEFORE any public disclosure
- Even within US, filing earlier preserves all options

RULE: File US provisional BEFORE any public disclosure if foreign filing is contemplated.
```

### Recipe 10: PCT (Patent Cooperation Treaty) — international
```text
PCT path:
1. File PCT application within 12 months of priority date
2. International Search Report (ISR) + Written Opinion (~16 months from priority)
3. International Preliminary Examination (optional)
4. 30-month deadline (from priority) to enter national phase in each country
5. Each country examines independently

PCT timeline:
- Month 0: Priority filing (provisional or non-provisional)
- Month 12: PCT filing
- Month 18: International publication (PCT WO/...)
- Month 30: National phase entry deadline

PCT cost: ~$3-5k filing + per-country national phase ($2-15k each).
```

### Recipe 11: §101 Alice analysis (software patents)
```text
After Alice Corp v. CLS Bank (2014):
Step 1 — Is claim directed to an abstract idea (or law of nature, natural phenomenon)?
  - Categories: fundamental economic practice; mathematical concept; mental process; method of organizing human activity
Step 2 — If yes, does claim recite "significantly more"?
  - Inventive concept
  - Improvement to a technology / computer functionality
  - Limiting to a particular technology
  - Specific machine / transformation

Software claims often fail §101 in 2026 if claim is "doing X on a computer" without specific technical improvement.
Strategies:
- Claim technical improvement (e.g., new memory architecture, novel data structure)
- Recite specific hardware integration
- Tie to physical world (sensor input → physical actuation)

USPTO 2024 §101 Guidelines: https://www.uspto.gov/patents/laws/examination-policy/subject-matter-eligibility
```

### Recipe 12: Small entity / micro entity status
```text
SMALL ENTITY (50% fee reduction):
- Individual inventor; OR
- Small business with <500 employees; OR
- Non-profit organization
- No exclusive license to non-small entity

MICRO ENTITY (75% fee reduction):
- Small entity status + 
- Income < ~3x median household ($212k 2024); AND
- Not named on > 4 prior US patent applications; AND
- No assignment to entity exceeding income limit
```

### Recipe 13: Inventor disclosure documentation
```text
Before drafting any patent:
1. Lab notebook / dated documentation of invention
2. Date of conception
3. Date of reduction to practice (working model or constructive — detailed disclosure)
4. Inventor list (all who contributed to inventive concept)
5. Funding source
6. Prior publications / disclosures
7. Related art known to inventor

USPTO IDS (Information Disclosure Statement) duty of candor — disclose all known prior art.
```

## Examples

### Example 1: Software startup considering patent on new auth mechanism
**Goal:** Assess patentability of novel biometric+behavioral authentication.
**Steps:**
1. Recipe 1 scope (utility patent).
2. Recipe 2 find CPC codes (G06F 21/32, H04L 9/32, etc.).
3. Recipe 3 USPTO PPS search.
4. Recipe 4 Google Patents broader.
5. Recipe 5 Lens.org for scholar cross-reference (academic biometrics literature).
6. Recipe 7 prior-art memo.
7. Recipe 11 §101 Alice analysis (high risk for software auth).
8. Recipe 8 recommend provisional first ($300 small entity) + draft formal claims for non-provisional in 12 months.
9. Add disclaimer; refer user to registered patent attorney for filing.

**Result:** Memo + filing recommendation; user files provisional via attorney.

### Example 2: Pre-disclosure check before conference paper
**Goal:** Inventor wants to publish at academic conference; needs to file before disclosure to preserve foreign rights.
**Steps:**
1. Verify conference date.
2. Run prior-art search (Recipes 3-6).
3. Draft provisional application (informal description + drawings).
4. File via patent attorney BEFORE conference disclosure.
5. Use 12-month window to refine + decide on PCT.

**Result:** Provisional filed; inventor presents at conference with US + foreign rights preserved.

## Edge cases / gotchas

- **§101 Alice rejection rate for software is ~50%+** in some art units. Software claims need technical improvement narrative.
- **AI / ML inventions face §101 scrutiny.** USPTO 2024 guidance allows AI inventions if claim recites specific technical implementation. Pure "use AI to do X" likely fails.
- **Inventor must be human (USPTO 2023+ rule).** AI cannot be named inventor. Human inventor must contribute to conception. Thaler v. Vidal, 43 F.4th 1207 (Fed. Cir. 2022).
- **Prior public use by inventor.** 35 USC §102(b)(1)(A) grace period only covers disclosures by inventor — disclosure by third party may bar.
- **Sale / offer for sale bar.** Confidential discussions with potential customers may or may not count; public sale starts the 1-year clock. See Helsinn v. Teva (2019) — sale to a counterparty bars even if confidential.
- **Continuation / divisional / CIP.** Filing strategies to capture additional claim scope; coordinate with patent attorney.
- **Patent term + adjustments.** 20 years from earliest priority date. Patent Term Adjustment (PTA) for USPTO delays. Patent Term Extension (PTE) for FDA-regulated drugs.
- **Provisional has NO claims requirement** but should still describe the invention with enabling detail. Bare 1-page provisional may fail to support later claims.
- **§102(g) prior invention.** Defunct after AIA (post-2013); now first-inventor-to-file (FITF). File fast.
- **Inequitable conduct — duty of candor.** All material prior art must be disclosed to USPTO. Failure = unenforceable patent (Therasense, 649 F.3d 1276 (Fed. Cir. 2011) raised bar).
- **Foreign filing license.** §184 requires USPTO foreign filing license before filing abroad. Auto-issued 6 months after US filing OR explicit petition.
- **Patentability search ≠ Freedom-to-Operate (FTO).** Patentability asks "can I get a patent?" FTO asks "can I sell without infringing?" Different questions, different searches.
- **PCT national phase costs.** ~$2-15k per country. Don't enter all PCT countries — pick markets that matter.

> Warning: **This is informational guidance from an AI agent. Always consult a licensed attorney (specifically, a registered USPTO patent attorney or agent) in your jurisdiction before signing, filing, or executing a patent application or relying on this analysis for filing decisions.**

## Sources

- [USPTO Patent Public Search](https://ppubs.uspto.gov/) — official US prior-art search.
- [Google Patents](https://patents.google.com/) — best free interface; covers 100+ jurisdictions.
- [Lens.org](https://www.lens.org/) — patent + scholarly cross-reference.
- [EPO Espacenet](https://worldwide.espacenet.com/) — European + worldwide.
- [WIPO Patentscope](https://patentscope.wipo.int/) — PCT + national filings.
- [Cooperative Patent Classification (CPC)](https://www.cooperativepatentclassification.org/) — current classification.
- [USPTO Manual of Patent Examining Procedure (MPEP)](https://www.uspto.gov/web/offices/pac/mpep/) — examination rules.
- [USPTO §101 Eligibility Guidance](https://www.uspto.gov/patents/laws/examination-policy/subject-matter-eligibility) — Alice / Mayo framework.
- [USPTO Patent Fees](https://www.uspto.gov/learning-and-resources/fees-and-payment/uspto-fee-schedule) — current fee schedule.
- [Alice Corp v. CLS Bank, 573 U.S. 208 (2014)](https://www.law.cornell.edu/supct/html/13-298.ZS.html) — §101 software case.
- [Thaler v. Vidal, 43 F.4th 1207 (Fed. Cir. 2022)](https://www.cafc.uscourts.gov/opinions-orders/21-2347.OPINION.8-5-2022_1985271.pdf) — AI inventorship.
- Sister skill: `trademark-search-uspto-tess-wipo`.
