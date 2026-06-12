# Legal Counsel — Source Attribution

This file maps every section of `soul.md` and `role.md` back to the research source(s) it was derived from. It is part of the bundle but is **not** loaded into the agent's context — it exists for human verification and future updates.

Upstream reference agents have not been downloaded in v1 (see `reference/INVENTORY.md`). Provenance is the SOTA web research summarized in `reference/SOTA_USE_CASES.md`. The "Notes on authored-from-synthesis" section below flags the small portions composed locally as operational glue.

---

## soul.md → source map

| Section in soul.md | Source(s) |
|---|---|
| Title + opening identity + load-bearing convictions | Authored from synthesis of the agent's per-agent prompt + `agent_bundle/METHODOLOGY.md` (load-bearing convictions pattern) |
| Purpose | Authored from synthesis informed by per-agent prompt's "one-line role" + Common Paper / Bonterms / NVCA / YC corpus surveys |
| Execution stack | `reference/SOTA_USE_CASES.md` (per-use-case skill-pack mapping) |
| When invoked — Contract review mode | `reference/SOTA_USE_CASES.md` § "MSA review" + "NDA review" + "Vendor / SaaS review" |
| When invoked — Contract drafting mode | `reference/SOTA_USE_CASES.md` § "Customer SaaS terms" + Common Paper / Bonterms intro material |
| When invoked — Privacy / compliance audit mode | `reference/SOTA_USE_CASES.md` § "GDPR readiness audit" + "CCPA / CPRA readiness audit" + "SOC 2 readiness" + ICO / EDPB / CPPA / AICPA guidance |
| When invoked — IP clearance mode | `reference/SOTA_USE_CASES.md` § "Trademark search + filing" + "Patent search + provisional vs non-provisional decision" + "Copyright registration" |
| When invoked — Equity / fundraising mode | `reference/SOTA_USE_CASES.md` § "Equity grant docs" + "SAFE / convertible note review" + "Term sheet review" + NVCA / Carta / YC sources |
| When invoked — Compliance setup mode | `reference/SOTA_USE_CASES.md` § "Privacy policy drafting" + "Cookie policy" + "DPA review" |
| When invoked — Research mode | `reference/SOTA_USE_CASES.md` § "Regulatory / case research" |
| Core operating rules (15 bullets) | Synthesis from the per-agent prompt's "CRITICAL DISCLAIMER" + ABA Model Rules of Professional Conduct (1.1 competence, 5.5 UPL, 1.5 fees, 1.6 confidentiality framing — for what the AI is NOT replacing) |
| Mode-specific decisions | `reference/SOTA_USE_CASES.md` per-use-case rows + NVCA / Carta state-of-market data |
| Quality gates | Authored from synthesis of the CRITICAL DISCLAIMER + ABA Model Rules framing + per-use-case verification points |
| Output format | Authored from synthesis informed by docx / pdf / markdown-converter skill defaults + Bluebook 21st ed. citation convention |
| Communication style | Authored from synthesis aligned with the load-bearing conviction "risk is a spectrum, not a yes/no" |
| When to push back | Synthesis from ABA Model Rules 5.5 (UPL) + 1.2 (scope of representation) + general engagement-letter best practices |
| When to defer (sibling agents) | Per-agent prompt's defer rules + CraftBot agent catalog |
| On first conversation (PROACTIVE init) | `METHODOLOGY.md` standard footer; the 3 routine questions tailored from the per-agent prompt |
| Closing rule | Authored from synthesis restating the three convictions |

---

## role.md → source map

| Section in role.md | Source(s) |
|---|---|
| Capability reference → Contract types in scope | Aggregated from Common Paper + Bonterms + NVCA + Cooley GO + Stripe Atlas + Clerky template catalogs |
| Capability reference → Compliance regimes | Aggregated from GDPR (EU 2016/679), CCPA / CPRA (Cal. Civ. Code §1798.100 et seq.), AICPA TSP 100, HIPAA (45 CFR §§ 160 / 162 / 164), PCI DSS v4.0, COPPA, FERPA, GLBA, ePrivacy Directive, CAN-SPAM, CASL, TCPA, ADA + WCAG, FTC Act §5, EU DSA / DMA, EU AI Act, NYC AI Bias Audit, Colorado AI Act |
| Capability reference → IP regimes | USPTO + US Copyright Office + WIPO + 17 USC §512 + Defend Trade Secrets Act 2016 + state UTSA |
| Capability reference → Equity instruments | IRC §§ 422 (ISO) / 409A / 83(b) / 83(i) / 423 (ESPP) + Rev. Proc. 93-27 / 2001-43 (profits interest) + YC SAFE variants |
| Capability reference → Funding rounds | NVCA model docs + Carta state-of-private-markets |
| Capability reference → Document libraries | Common Paper + Bonterms + YC + Cooley GO + Stripe Atlas + Clerky + NVCA + AICPA + EU Commission SCC + HHS BAA + AAA / JAMS |
| MSA review playbook | Synthesis from Bonterms Cloud Service Agreement + Common Paper Cloud Service Agreement + ABA Business Law Section materials |
| NDA review playbook | Synthesis from Common Paper Mutual NDA + Bonterms NDA materials |
| Employment agreement playbook (US, EU) | US: DOL guidance + FLSA + state non-compete map; EU: Working Time Directive + member-state employment law overview |
| Privacy policy checklist | GDPR Art. 13 / Art. 14 text + CCPA §1798.130 + CPRA additions |
| GDPR readiness checklist | ICO + EDPB + GDPR text (Art. 3, 4, 6, 9, 25, 28, 30, 33, 34, 35, 37, 44-49) |
| CCPA readiness checklist | Cal AG CCPA enforcement guides + CPPA regulations + CPRA additions |
| SOC2 readiness checklist | AICPA TSP 100 + Drata / Vanta / SecureFrame readiness documentation |
| Trademark search playbook | USPTO TESS (tmsearch.uspto.gov) + WIPO Global Brand Database + Trademarkia + Nice Classification + Madrid Protocol |
| Patent search playbook | USPTO PPS + Google Patents + Lens.org + EPO Espacenet + WIPO Patentscope + 35 USC §§ 101 / 102 / 103 + PCT |
| Equity grants reference | IRC §§ 422, 409A, 83(b), 83(i), 423 + Rev. Proc. 93-27 / 2001-43 + IRS Form 15620 |
| 83(b) election playbook | Treasury Reg §1.83-2(e) + Rev. Proc. 2012-29 + IRS Form 15620 |
| SAFE review playbook | YC SAFE template documentation (post-money + pre-money + MFN + cap-and-discount variants) |
| Term sheet decision table | NVCA model term sheet + Carta state-of-private-markets data + Holloway "Raising Venture Capital" reference |
| Cap table modeling | Carta + Pulley + AngelList Stack documentation + standard pre-money / post-money math |
| Founders agreement template | Cooley GO + Stripe Atlas + Clerky founder template overlap |
| OSS license obligation matrix | SPDX license list + OSI license catalog + OSS Review Toolkit license-classification rules |
| DMCA takedown playbook | 17 USC §512 (c) + (g) + Copyright Office DMCA Designated Agent Directory documentation |
| Non-compete state map | NCSL non-compete tracker + state code citations + FTC Non-Compete Rule + 5th Cir stay coverage |
| Antipattern catalog | Composition synthesis informed by ABA + Cooley + Stripe Atlas advisor commentary on common founder mistakes |
| Disclaimer templates | Authored from synthesis aligned with ABA Model Rules 5.5 (UPL) + 1.1 (competence) + the load-bearing CRITICAL DISCLAIMER from the per-agent prompt |
| SOTA tool reference (June 2026) | `reference/SOTA_USE_CASES.md` + per-tool source URLs (cited in the SOTA sources table below) |
| SOTA execution playbook | `reference/SOTA_USE_CASES.md` summary table |
| Closing rules | Authored from synthesis restating soul.md convictions |

---

## Notes on authored-from-synthesis

Sections composed as operational glue rather than lifted verbatim:

- **Core operating rules (soul.md)** — 15 bullets composed locally from the CRITICAL DISCLAIMER + ABA Model Rules framing + practical legal-agent operational rules. None of these are domain claims that lack underlying support.
- **When to push back / When to defer (soul.md)** — operational glue. Domain claims (UPL, fee terms, jurisdiction scope) come from ABA Model Rules; the framing is composed.
- **Antipattern catalog (role.md)** — composition synthesis from common founder mistakes documented in Cooley GO, Stripe Atlas, advisor commentary, and the FTC + Cal AG enforcement record. Each antipattern's underlying statute / template is cited inline.
- **Disclaimer templates (role.md)** — composed to be deployable; aligned with the load-bearing CRITICAL DISCLAIMER + ABA Model Rules 5.5 (UPL).
- **First-conversation routine questions (soul.md)** — adapted from the standard PROACTIVE.md self-init pattern in `METHODOLOGY.md`. The 3 role-specific questions are tailored to legal workflows.

These are operational glue, not domain claims. They do not introduce knowledge claims that lack a source.

---

## How to update this agent

If you want to refresh content from upstream:

1. Re-fetch the SOTA sources listed in the table below — many of these (FTC, ICO, EDPB, USPTO, copyright.gov, NVCA, Carta state-of-market) update quarterly or on major regulatory event.
2. Diff against the previous versions to see what changed.
3. Update the corresponding sections of `soul.md`, `role.md`, and `reference/SOTA_USE_CASES.md`.
4. Update this `SOURCES.md` if section names or source URLs changed.
5. Re-run `python verify.py legal-counsel` to confirm structure intact.
6. Re-run `python build.py legal-counsel` to regenerate `dist/legal-counsel.craftbot`.

The bundled skill packs (in `skills/`) are created in Round 2; their SKILL.md files cite tool-specific sources independently.

---

## SOTA tool sources (June 2026)

| Tool / framework | Source URL | Used in |
|---|---|---|
| Common Paper — standardized templates | https://commonpaper.com/standards/ | `skills/contract-review-msa-nda-employment` + `skills/terms-of-service-tos-drafting` + `skills/dpa-data-processing-agreement` + `reference/SOTA_USE_CASES.md` |
| Bonterms — open template library | https://bonterms.com/ | Same as above + `skills/contract-review-msa-nda-employment` SLA module |
| Y Combinator SAFE | https://www.ycombinator.com/documents | `skills/safe-convertible-note-yc-template` |
| Cooley GO documents | https://www.cooleygo.com/documents/ | `skills/equity-grants-isos-rsus-83b-election` + `skills/founders-agreement-vesting-ip-assignment` + `skills/contract-review-msa-nda-employment` |
| NVCA Model Legal Documents | https://nvca.org/model-legal-documents/ | `skills/term-sheet-review-series-a-typical-terms` |
| Carta — State of Private Markets | https://carta.com/learn/startups/state-of-private-markets/ | `skills/term-sheet-review-series-a-typical-terms` + `skills/safe-convertible-note-yc-template` |
| Stripe Atlas | https://stripe.com/atlas | `skills/equity-grants-isos-rsus-83b-election` + `skills/founders-agreement-vesting-ip-assignment` |
| Clerky | https://www.clerky.com/ | Same as above |
| Iubenda — Privacy Policy Generator | https://www.iubenda.com/en/privacy-policy-generator | `skills/iubenda-termly-privacy-policy-generators` |
| Termly | https://termly.io/ | `skills/iubenda-termly-privacy-policy-generators` |
| Cookiebot | https://www.cookiebot.com/ | `skills/cookie-consent-management-cookiebot-onetrust` |
| OneTrust | https://www.onetrust.com/products/cookie-consent/ | `skills/cookie-consent-management-cookiebot-onetrust` |
| GDPR.eu | https://gdpr.eu/ | `skills/gdpr-readiness-audit` + `skills/dpa-data-processing-agreement` |
| ICO (UK) | https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/ | `skills/gdpr-readiness-audit` |
| EDPB | https://edpb.europa.eu/ | `skills/gdpr-readiness-audit` + `skills/dpa-data-processing-agreement` |
| EU SCC 2021/914 | https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/standard-contractual-clauses-scc_en | `skills/dpa-data-processing-agreement` |
| California AG — CCPA | https://oag.ca.gov/privacy/ccpa | `skills/ccpa-cpra-readiness-audit` |
| CPPA — CPRA regulations | https://cppa.ca.gov/regulations/ | `skills/ccpa-cpra-readiness-audit` |
| Drata | https://drata.com/ | `skills/drata-vanta-secureframe-soc2-readiness` |
| Vanta | https://www.vanta.com/ | `skills/drata-vanta-secureframe-soc2-readiness` |
| SecureFrame | https://secureframe.com/ | `skills/drata-vanta-secureframe-soc2-readiness` |
| AICPA TSP 100 | https://us.aicpa.org/interestareas/frc/assuranceadvisoryservices/sorhome | `skills/drata-vanta-secureframe-soc2-readiness` |
| USPTO TESS | https://tmsearch.uspto.gov/ | `skills/trademark-search-uspto-tess-wipo` |
| USPTO Patent Public Search | https://ppubs.uspto.gov/ | `skills/patent-search-uspto-lens-google` |
| Google Patents | https://patents.google.com/ | `skills/patent-search-uspto-lens-google` |
| Lens.org | https://www.lens.org/ | `skills/patent-search-uspto-lens-google` |
| WIPO Global Brand Database | https://www.wipo.int/branddb/en/ | `skills/trademark-search-uspto-tess-wipo` |
| Trademarkia | https://www.trademarkia.com/ | `skills/trademark-search-uspto-tess-wipo` |
| US Copyright Office (eCO + DMCA Directory) | https://www.copyright.gov/ | `skills/dmca-takedown-process` + copyright registration prep recipe |
| IRS Form 15620 (83(b) model) | https://www.irs.gov/forms-pubs/about-form-15620 | `skills/equity-grants-isos-rsus-83b-election` |
| Treasury Reg §1.83-2(e) | https://www.law.cornell.edu/cfr/text/26/1.83-2 | `skills/equity-grants-isos-rsus-83b-election` |
| Robin AI | https://www.robinai.com/ | `skills/robin-spellbook-harvey-ai-contract-review` |
| Spellbook | https://www.spellbook.legal/ | `skills/robin-spellbook-harvey-ai-contract-review` |
| Harvey AI | https://www.harvey.ai/ | `skills/robin-spellbook-harvey-ai-contract-review` |
| Ironclad | https://ironcladapp.com/ | `skills/ironclad-contractworks-clm` |
| ContractWorks | https://www.contractworks.com/ | `skills/ironclad-contractworks-clm` |
| Lexion | https://www.lexion.ai/ | `skills/ironclad-contractworks-clm` |
| Evisort | https://www.evisort.com/ | `skills/ironclad-contractworks-clm` |
| LinkSquares | https://linksquares.com/ | `skills/ironclad-contractworks-clm` |
| Concord | https://www.concord.app/ | `skills/ironclad-contractworks-clm` |
| DocuSign Developer | https://developers.docusign.com/ | `skills/ironclad-contractworks-clm` (e-sign section) |
| Adobe Sign Developer | https://developer.adobe.com/document-services/apis/sign/ | Same as above |
| Dropbox Sign Developer | https://developers.hellosign.com/ | Same as above |
| PandaDoc Developer | https://developers.pandadoc.com/ | Same as above |
| 17 USC §512 (DMCA) | https://www.law.cornell.edu/uscode/text/17/512 | `skills/dmca-takedown-process` |
| 17 USC §101 (work for hire) | https://www.law.cornell.edu/uscode/text/17/101 | `skills/founders-agreement-vesting-ip-assignment` |
| Cal. Labor Code §2870 (employee inventions) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=LAB&sectionNum=2870 | `skills/founders-agreement-vesting-ip-assignment` |
| Cal. Bus. & Prof. Code §16600 (non-compete void) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=16600 | `skills/non-compete-non-solicit-state-enforceability` |
| FTC Non-Compete Rule | https://www.ftc.gov/legal-library/browse/rules/noncompete-rule | `skills/non-compete-non-solicit-state-enforceability` |
| NCSL Non-Compete State Map | https://www.ncsl.org/labor-and-employment/non-compete-agreements | `skills/non-compete-non-solicit-state-enforceability` |
| HHS HIPAA Sample BAA | https://www.hhs.gov/hipaa/for-professionals/covered-entities/sample-business-associate-agreement-provisions/ | `skills/contract-review-msa-nda-employment` (BAA recipe) |
| PCI Security Standards Council | https://www.pcisecuritystandards.org/ | PCI scope recipe |
| SPDX License List | https://spdx.org/licenses/ | `skills/open-source-license-mit-apache-gpl-agpl` |
| Open Source Initiative (OSI) | https://opensource.org/licenses | `skills/open-source-license-mit-apache-gpl-agpl` |
| OSS Review Toolkit (ORT) | https://github.com/oss-review-toolkit/ort | `skills/open-source-license-mit-apache-gpl-agpl` |
| Syft (Anchore) | https://github.com/anchore/syft | `skills/open-source-license-mit-apache-gpl-agpl` |
| FOSSA | https://fossa.com/ | `skills/open-source-license-mit-apache-gpl-agpl` |
| Cornell LII | https://www.law.cornell.edu/ | All compliance / IP / employment playbooks |
| CourtListener (Free Law Project) | https://www.courtlistener.com/ | Research recipes |
| Justia | https://www.justia.com/ | Research recipes |
| SEC EDGAR | https://www.sec.gov/edgar | `sec-edgar-mcp` + research recipes |
| AAA Arbitration Rules | https://www.adr.org/Rules | `skills/contract-review-msa-nda-employment` (jurisdictional clause recipe) |
| JAMS Rules | https://www.jamsadr.com/rules-clauses | Same as above |
| UCC §2-615 (commercial impracticability) | https://www.law.cornell.edu/ucc/2/2-615 | `skills/contract-review-msa-nda-employment` (force majeure recipe) |
| TN ELVIS Act | https://www.tn.gov/governor/news/2024/3/21/photo-release--gov--bill-lee-signs-the-elvis-act.html | Right of publicity recipe |

---

These sources informed the `SOTA tool reference (June 2026)` section in `role.md`, the per-use-case mapping in `reference/SOTA_USE_CASES.md`, and the bundled SOTA skill packs (Round 2 creates the SKILL.md content).
