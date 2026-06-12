---
name: trademark-search-uspto-tess-wipo
description: Trademark clearance + filing prep — USPTO TESS (US), WIPO Global Brand Database (50+ countries), Trademarkia (common-law), and TEAS Standard / TEAS Plus / Madrid Protocol filing prep. Knock-out search (2-3 hours) vs full clearance (1-2 days). Output is a clearance memo + filing-prep packet with the consult-an-attorney disclaimer.
---

# Trademark Search — USPTO TESS / WIPO / Trademarkia

## When to use

User says:

- "Search trademark for [mark]"
- "Is [name] available?"
- "Run a trademark clearance"
- "File a trademark"
- "TEAS Plus vs TEAS Standard"
- "Madrid Protocol / international filing"
- "What Nice class do I file in?"
- "USPTO §2(d) likelihood of confusion"

Companion skills:
- `patent-search-uspto-lens-google` — sister IP skill.
- `dmca-takedown-process` — copyright takedown.

## Setup

```bash
# USPTO TESS — redesigned 2024 to "trademark search at tmsearch.uspto.gov"
# https://tmsearch.uspto.gov/

# WIPO Global Brand Database
# https://www.wipo.int/branddb/en/

# Trademarkia
# https://www.trademarkia.com/

# USPTO TEAS filing portal
# https://teas.uspto.gov/

# Nice Classification (12th edition currently — 2024-2025; check current)
# https://www.wipo.int/classifications/nice/en/

# uspto-mcp — direct queries from the agent
# (Configured via app/config/mcp_config.json)

# Python helpers (for parsing TESS / WIPO XML / JSON)
pip install requests beautifulsoup4 pandas

# Brand database / scraping via firecrawl-mcp
# Configured via app/config/mcp_config.json
```

Auth / API keys:
- USPTO TESS: no key required for web search.
- WIPO Brand DB: no key for web search.
- Trademarkia: paid API for bulk; web is free.
- USPTO TEAS filing: USPTO.gov account.

## Common recipes

### Recipe 1: Identify the mark + class
```python
# trademark_scoping.py
mark = "FOO"  # the word/design mark
form = "wordmark"  # wordmark | design | combined
goods_services = "Software as a service for project management"

# Nice Classification 12th ed common classes:
# Class 9 — downloadable software, hardware
# Class 35 — advertising, business services, retail
# Class 38 — telecommunications
# Class 41 — education, training
# Class 42 — SaaS, IT services, scientific research  <-- common for B2B SaaS
# Class 45 — legal services
# Full list: https://www.wipo.int/classifications/nice/en/

primary_class = 42  # SaaS / IT services
related_classes = [9, 35]  # downloadable + business services
```

### Recipe 2: USPTO TESS basic search
```text
1. Visit https://tmsearch.uspto.gov/
2. Search by Word Mark: "FOO"
3. Filter by:
   - Live registrations + applications
   - International Class (e.g., 42)
4. Review results: full mark + Owner + Goods/Services + Status

Search variants:
- Exact: "FOO"
- Wildcard: "FO*" "*OO" "F*O"
- Phonetic: "FOO" / "FU" / "PHOO"
- Plural: "FOOS"
- Foreign equivalents: "FÜ" / "FOO" in other lang
```

### Recipe 3: TESS expanded search (cross-class + common-law)
```text
After basic same-class search, expand:
1. Cross-class likelihood of confusion (related goods/services)
   - Software in C9 vs SaaS in C42 — examiner often finds similar
   - Apparel in C25 vs apparel design in C42 — usually distinct
2. Common-law (unregistered) searches:
   - Google: "FOO" + your industry keywords
   - LinkedIn / Twitter / Instagram handle search
   - Trademarkia common-law database
   - Industry-specific databases (e.g., AngelList, ProductHunt for SaaS)
3. Domain availability:
   - WHOIS: foo.com / foo.io / foo.app / foo.ai
   - Social handles: @foo on X, Instagram, TikTok, LinkedIn
```

### Recipe 4: WIPO Global Brand Database — international
```text
1. Visit https://www.wipo.int/branddb/en/
2. Search "FOO" across:
   - Madrid Protocol registrations (international)
   - National registrations (50+ jurisdictions)
   - Well-known marks (Article 6bis Paris Convention)
3. Filter by:
   - Nice class
   - Jurisdiction(s) where you want to file
   - Status (active / expired)
4. Export results for memo
```

### Recipe 5: Trademarkia — fast common-law
```text
https://www.trademarkia.com/
- Free search for USPTO + state + common-law
- Returns Knock-out reports
- Paid: comprehensive 50-state clearance ($199-499)
```

### Recipe 6: Knock-out search (2-3 hours)
```markdown
# Knock-out report — Mark: "FOO"

## Search scope
- USPTO TESS: Class 42, live registrations + applications
- USPTO TESS: Related classes 9, 35
- WIPO Brand DB: US + EU + UK + AU + CA + JP + CN (top markets)
- Trademarkia common-law
- Google + LinkedIn handle search
- Domain (foo.com, foo.io, foo.app)
- Social (@foo)

## Findings
- USPTO Class 42: 0 identical; 2 phonetically similar (FOE INC reg 5,123,456; FU SOFTWARE app 87/123,456)
- USPTO related classes: 1 similar (FOO STUFF reg 6,123,456 in C35 — but distinct services)
- WIPO: 1 EU registration (FU GMBH, food/beverage Class 30 — distinct)
- Common-law: foo.app is taken by an unregistered startup
- Domain: foo.com unavailable; foo.ai available

## Risk assessment
- HIGH risk: phonetically similar mark in same class
- MEDIUM risk: similar mark in related class (likelihood of confusion analysis needed)
- LOW risk: unrelated foreign registrations
- KO-issue: foo.app taken by competitor

## Recommendation
- Consider alternative mark OR file a §2(d) opinion letter with TM attorney
- Verify foo.app actual use; if abandoned, ok to proceed
- Reserve foo.ai immediately

---
**Disclaimer:** Knock-out search is informational, not a substitute for full clearance + attorney opinion. Always consult a licensed trademark attorney before commercial use or filing.
```

### Recipe 7: Full clearance (1-2 days, with attorney recommended)
```text
Full clearance adds:
- Comprehensive USPTO search across ALL classes
- All-state common-law search (database + manual)
- International search in target markets (Madrid + national)
- Industry-specific publications + product directories
- AGENT (Aggregate Negative Examination Tactic) — examiner-perspective likelihood-of-confusion analysis
- §2(e) descriptiveness analysis
- §2(d) likelihood-of-confusion opinion letter (TM attorney signs)
- Risk assessment with recommended action

Typical attorney clearance: $500-2,500.
```

### Recipe 8: TEAS Plus vs TEAS Standard filing prep
```text
TEAS Plus ($250/class):
- Must use EXACT goods/services description from USPTO Acceptable ID Manual
  (https://idm-tmng.uspto.gov/)
- Must agree to electronic communication
- Must include claim of intent-to-use or use-in-commerce
- Faster examination

TEAS Standard ($350/class):
- Custom goods/services description allowed
- Paper-mail communication ok
- Slightly slower examination

Filing basis:
- §1(a) Use-in-commerce — requires Specimen + Date of First Use
- §1(b) Intent-to-use — file now, Statement of Use within 6 months
  (extendable in 6-month increments, $125-225/extension, up to 36 months total)
- §44 Foreign application/registration — base on home-country mark
- §66(a) Madrid Protocol — international extension
```

### Recipe 9: Goods/services description drafting
```text
Use Acceptable ID Manual: https://idm-tmng.uspto.gov/

Class 42 examples for SaaS:
- "Software as a service (SAAS) services featuring software for [function]"
- "Platform as a service (PAAS) featuring computer software platforms for [function]"
- "Providing temporary use of non-downloadable software for [function]"

Class 9 examples for downloadable software:
- "Downloadable mobile applications for [function]"
- "Downloadable computer software for [function]"

BAD: "Software" (too broad — TEAS Plus reject; TEAS Standard examiner inquiry)
GOOD: "Software as a service (SAAS) services featuring software for project management"
```

### Recipe 10: Filing prep packet
```markdown
# Trademark Application Prep — Mark: "FOO"

## Mark
- Word mark: FOO
- Standard character claim: Yes
- Stylized? No
- Color claim? No

## Owner
- Legal name: <Company LLC>
- Citizenship / State of incorporation: Delaware
- Address
- Owner email
- Owner type: corporation

## Class(es)
- Class 42 (primary)

## Goods/services
"Software as a service (SAAS) services featuring software for project management"

## Filing basis
- §1(b) Intent-to-use (will file Statement of Use after launch)

## Specimen (if §1(a))
- Screenshot of website footer showing mark in use
- Product UI screenshot
- Marketing email featuring mark

## Date of First Use (if §1(a))
- First use anywhere: <date>
- First use in commerce: <date>

## Filing fee
- $250/class TEAS Plus
- Total: $250

## Filing checklist
- [ ] USPTO.gov account created
- [ ] All required fields complete
- [ ] Specimen attached (if §1(a))
- [ ] Payment method ready
- [ ] Submit via https://teas.uspto.gov/

## Post-filing timeline
- ~3 months: USPTO examiner reviews
- ~6 months: if approved, published for opposition (30 days)
- ~3 months: registration issued (if §1(a)) OR Notice of Allowance (if §1(b))
- §1(b): file Statement of Use within 6 months of Notice of Allowance

---
**Disclaimer:** This is filing prep, not legal advice. Always consult a licensed trademark attorney before submitting a USPTO application or relying on this packet for filing decisions.
```

### Recipe 11: Madrid Protocol — international extension
```text
After US base application / registration:
1. File via USPTO TEAS Madrid Protocol application
2. Designate target countries (each pays own fee)
3. WIPO IB (International Bureau) processes
4. National examiners review per local law (12-18 months typical)
5. Each country may refuse independently

Costs (approx 2026):
- Basic WIPO fee: CHF 653 (B/W) or CHF 903 (color)
- Per-country supplementary fee: CHF 100 each
- Per-class fee: CHF 100 each (beyond 3 classes)
- USPTO transmittal fee: $100
- Target country exam fees: vary

Madrid base requirement: Active US application / registration; refusal of US destroys all extensions ("central attack" first 5 years).
```

### Recipe 12: USPTO §2(d) likelihood-of-confusion factors (DuPont)
```text
13 DuPont factors (In re E.I. du Pont de Nemours & Co., 476 F.2d 1357 (CCPA 1973)):

1. Similarity of marks (sight, sound, meaning, commercial impression)
2. Similarity of goods/services
3. Similarity of trade channels
4. Conditions of purchase (impulse vs careful)
5. Fame of prior mark
6. Number + nature of similar marks on similar goods
7. Nature + extent of actual confusion
8. Length of time + conditions without confusion
9. Variety of goods on which mark is used
10. Market interface (consent, agreements, license)
11. Extent of bar's right to exclude others
12. Extent of potential confusion
13. Any other established fact

Examiner weighs factors holistically — no single dispositive.
```

## Examples

### Example 1: Pre-launch SaaS startup, mark "FOO"
**Goal:** Clear "FOO" for Class 42 software services before brand launch.
**Steps:**
1. Recipe 1 scope mark + class.
2. Recipe 2 USPTO TESS basic search.
3. Recipe 3 expand to related classes + common-law.
4. Recipe 4 WIPO international.
5. Recipe 6 produce knock-out report.
6. If low risk → Recipe 10 filing prep + send to TM attorney for opinion letter.
7. If high risk → consider alternative mark.
8. Reserve domain + social handles.
9. Add disclaimer; deliver to user.

**Result:** Knock-out + filing prep packet; user instructed to engage TM attorney for filing.

### Example 2: International expansion to EU + UK + AU
**Goal:** Extend US mark to 3 countries via Madrid.
**Steps:**
1. Verify active US application / registration.
2. Pick target countries.
3. Recipe 11 Madrid filing prep (cost estimate, class structure).
4. Send to TM attorney for filing.

**Result:** Madrid extension filed (by attorney).

## Edge cases / gotchas

- **USPTO TESS redesigned 2024.** Old `tmsearch.uspto.gov/bin/showfield?f=login&p_lang=english` URL deprecated; new URL is `tmsearch.uspto.gov`. Always confirm current URL.
- **Knock-out ≠ clearance.** Knock-out catches obvious conflicts; full clearance + attorney opinion needed for actual filing.
- **§2(d) refusal is the most common.** Examiner finds likelihood of confusion with prior registration. Pre-clear with TESS + cross-class.
- **§2(e) descriptiveness refusal.** Mark merely describes the goods/services → refused. "PROJECT TOOLS" for project management software = likely §2(e).
- **§2(e) Supplemental Register.** Descriptive marks can register on Supplemental Register (no presumptive rights but blocks identical filings; can move to Principal after 5 years of substantially exclusive use).
- **Specimen of use rules tightened.** USPTO Examiner rejects mockups, generic screenshots without mark. Use clear product / marketing materials.
- **Intent-to-use bona-fide standard.** Filing §1(b) without actual intent to use = fraud risk → invalidates registration.
- **Madrid Protocol "central attack."** If US base is cancelled within 5 years, all Madrid extensions fall. Hold US base until international portfolio stable.
- **Common-law rights persist without registration.** Even unregistered marks can block your registration in their geographic area of use. Search common-law diligently.
- **TEAS Plus exact-ID requirement.** Using non-Acceptable ID descriptions in TEAS Plus auto-rejects → must refile as TEAS Standard ($+100/class).
- **Multi-class fees.** USPTO charges per class. 3-class application = $750+ TEAS Plus / $1,050 TEAS Standard.
- **Filing without attorney for foreign applicants.** USPTO requires foreign applicants to use US-licensed attorney. US applicants may file pro se but strongly discouraged.
- **Madrid + EU.** EU Trademark Office (EUIPO) is separate route — sometimes cheaper than Madrid extension for EU coverage. Compare costs per case.

> Warning: **This is informational guidance from an AI agent. Always consult a licensed attorney (specifically, a licensed trademark attorney) in your jurisdiction before signing, filing, or executing a trademark application or relying on this clearance for binding business decisions.**

## Sources

- [USPTO Trademark Search (tmsearch.uspto.gov)](https://tmsearch.uspto.gov/) — US trademark search.
- [USPTO TEAS Filing](https://teas.uspto.gov/) — application filing portal.
- [USPTO Trademark Manual of Examining Procedure (TMEP)](https://tmep.uspto.gov/) — examination rules.
- [USPTO Acceptable ID Manual](https://idm-tmng.uspto.gov/) — pre-approved goods/services descriptions.
- [WIPO Global Brand Database](https://www.wipo.int/branddb/en/) — international + 50+ jurisdictions.
- [WIPO Madrid Monitor](https://www3.wipo.int/madrid/monitor/) — Madrid Protocol registrations.
- [Nice Classification 12th ed.](https://www.wipo.int/classifications/nice/en/) — class definitions.
- [Trademarkia](https://www.trademarkia.com/) — common-law search.
- [INTA — International Trademark Association](https://www.inta.org/) — resources + practice guides.
- [In re E.I. du Pont de Nemours, 476 F.2d 1357 (CCPA 1973)](https://www.law.cornell.edu/uscode/text/15/1052) — DuPont factors for §2(d).
- Sister skill: `patent-search-uspto-lens-google`.
