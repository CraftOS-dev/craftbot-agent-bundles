# Recruiter — Sources

> Section→source map for `soul.md` and `role.md`. Ships in the bundle but is **not** loaded into the agent's context. For humans verifying provenance and for future updates.

## soul.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Title + persona intro | `reference/SOTA_USE_CASES.md` (per-tool sourcing) | Action-verb-first per build_new_agent_instructions.md mandate |
| Three convictions | https://hbr.org/2016/05/structured-interviews + https://www.thetalentboard.org/cande-research-reports/ + Schmidt & Hunter meta-analysis | r=0.51 vs r=0.20; CandE 24h SLA standard |
| Purpose | `reference/SOTA_USE_CASES.md` + parent operations-agent + sibling talent-sourcer | Owns Applied → Hired; handoffs explicit |
| Execution stack | `reference/SOTA_USE_CASES.md` | Built during runtime build (Round 2) — 24 bundled skill pack names reserved |
| When invoked — per-mode entry procedures | Greenhouse / Ashby / Lever docs + interview-process literature | 20 modes documented |
| Core operating rules | Schmidt & Hunter + Talent Board CandE + EEOC AI guidance + NYC LL144 + jurisdiction-specific pay-transparency + FCRA | 21 hard rules; each tied to research / regulation |
| Mode-specific decisions | Per-mode quality bar derived from 2026 SOTA benchmarks | Done-when criteria |
| Quality gates | Verification checklist — pre-delivery enforcement | 13 gates |
| Output format | Recruiter-team artifact patterns | Interview kits in Notion → ATS; offer letters in DocuSign; dashboards in google-sheet |
| Communication style | https://www.metaview.ai/resources/blog/recruiting-metrics + https://hbr.org/2016/05/structured-interviews | Direct + benchmarked + DECISION REQUIRED label |
| When to push back / defer | `legal-counsel` + `ceo-agent` + `marketing-agent` + `talent-sourcer` + `operations-agent` cross-agent boundaries | 16 push-back rules + 10 defer rules |
| PROACTIVE self-init footer | `METHODOLOGY.md` standard footer | Same wording across all agents; routine questions specific to recruiter pain points |

## role.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Capability reference (ATS landscape, interview kit components, recruiter screen agenda, reference Qs, metrics formulas, comp intel, background check packages, technical interview matrix, DEI rules, candidate-experience SLA matrix) | All sources in `reference/SOTA_USE_CASES.md` per-tool documentation | Factual lists banished from soul.md |
| Interview kit library — Senior Backend Engineer | https://www.greenhouse.io/blog/interview-kits + https://www.ashbyhq.com/learn/articles/structured-interviewing + Schmidt & Hunter | Battle-tested kit pattern |
| STAR question bank by role family | https://www.greenhouse.io/blog/structured-interview-questions + role-specific recruiting literature | Engineering IC + Mgmt + PM + Sales + CS + Marketing |
| Recruiter screen template | https://www.smartrecruiters.com/resources/articles/the-recruiter-screen-call + https://www.metaview.ai/resources/blog/recruiting-metrics | 30-min agenda + post-call scorecard |
| Debrief facilitation script | https://www.greenhouse.io/blog/the-perfect-interview-debrief + https://lattice.com/library/the-interview-debrief-template | Position-then-evidence + consensus protocol |
| Offer letter template per geo (US FTE) | https://developers.docusign.com/docs/esign-rest-api/ + state-specific employment law + `legal-counsel` defer | At-will + non-compete + IP assignment + FCRA contingency disclaimer |
| Decline template library per stage | https://www.greenhouse.io/blog/candidate-rejection-emails + Talent Board CandE Awards methodology | Per-stage templates with future-reconnection patterns |
| ATS API recipes | https://developers.greenhouse.io/harvest.html + https://developers.ashbyhq.com/reference + https://hire.lever.co/developer/documentation + https://workable.readme.io/reference | Greenhouse Harvest + Ashby + Lever + Workable curl recipes |
| Goodtime scheduling playbook | https://help.goodtime.io/en/articles/api-documentation + https://goodtime.io/product/scheduling | Decision rule: ≥4-person → Goodtime; ≤2-person → Calendly |
| Karat / CodeSignal / CoderPad / HackerRank decision matrix | https://karat.com/product/ + https://codesignal.com/ + https://coderpad.io/ + https://www.hackerrank.com/products/recruiter | Live-pairing preferred 2026; cost + scale + anti-cheat matrix |
| Comp benchmark workflow | https://www.pave.com/developers + https://docs.carta.com/ + https://www.compa.ai/ + https://www.levels.fyi/ | Percentile anchor by stage |
| FCRA flow runbook | https://developers.checkr.com/ + 15 USC §1681 + state-specific (CA ICRAA, NYC FCA, IL, MA, NJ) + `legal-counsel` defer | 7-step compliance workflow |
| DEI compliance audit checklist | https://www.greenhouse.io/inclusion + https://www.eeoc.gov/laws/guidance/ai-employment-decisions + 4/5 rule + NYC LL144 + IL AI Video Act + CO SB 24-205 | Quarterly checklist |
| Antipattern catalog | Distilled from soul.md violations + 2026 recruiting literature | 7 BAD/GOOD pairs |
| SOTA tool reference (June 2026) | Per-tool URLs in `reference/SOTA_USE_CASES.md` | One H3 per tool, 10-30 lines each |
| SOTA execution playbook table | `reference/SOTA_USE_CASES.md` "Recommended agent.yaml additions" | Maps user request → first-stop skill pack |
| Brief templates (HM intake) | https://www.greenhouse.io/blog/hiring-manager-intake-meeting + https://www.lever.co/blog/intake-meeting-template + https://www.ashbyhq.com/learn/articles/hiring-manager-kickoff | Outcome scorecard + panel + DEI + timeline |

## SOTA tool sources (June 2026)

> One row per SOTA tool referenced in the agent.

| Tool | Source URL | Used for |
|---|---|---|
| Greenhouse | https://developers.greenhouse.io/harvest.html | ATS config + scorecards + reports + interview kits |
| Ashby | https://developers.ashbyhq.com/reference | ATS API-first + native scheduling + feedback forms |
| Lever | https://hire.lever.co/developer/documentation | ATS + Lever Hooks webhooks + CRM-first pipeline |
| Workable | https://workable.readme.io/reference | SMB ATS + native scheduling |
| Goodtime | https://help.goodtime.io/en/articles/api-documentation | Multi-person panel scheduling + DEI composition |
| Calendly | https://developer.calendly.com/api-docs | 1-2 person screen scheduling |
| Cal.com | https://cal.com/docs/api | Open-source Calendly alternative |
| Crosschq | https://crosschq.com/360-reference-checks/ | Digital reference checks + 360 distribution |
| Checkster | https://www.checkster.com/ | Survey-based reference automation |
| SkillSurvey | https://www.skillsurvey.com/recruiter-pre-hire-360/ | Pre-hire 360 reference |
| Pave | https://pave.com/product/total-comp | Real-time Total Comp benchmarks |
| Carta Total Comp | https://carta.com/learn/equity/ | Cap-table-aware comp benchmarks + equity modeling |
| Compa AI | https://www.compa.ai/ | Offer-letter comp communication + negotiation talking points |
| Levels.fyi | https://www.levels.fyi/ | Free public crowd-sourced comp data |
| Radford | (enterprise account) | Enterprise comp survey gold standard |
| DocuSign | https://developers.docusign.com/docs/esign-rest-api/ | Offer letter e-sign + template merge fields |
| PandaDoc | https://developers.pandadoc.com/ | Alt offer letter + e-sign |
| Checkr | https://developers.checkr.com/ | Founder-friendly background checks + FCRA flow |
| Sterling | https://www.sterlingcheck.com/api-documentation/ | Enterprise + international background checks |
| GoodHire | https://www.goodhire.com/ | SMB background check tier |
| Karat | https://karat.com/product/ | Technical interview as a service + 24h turnaround |
| CoderPad | https://coderpad.io/help/api/ | Live-pairing technical interview + IDE + anti-cheat |
| CodeSignal | https://docs.codesignal.com/recruiter | Async technical assessment + ICF + Cosmo AI |
| HackerRank | https://www.hackerrank.com/work/api | Broad technical library + plagiarism detection |
| Codility | https://www.codility.com/api/ | European technical interview + anti-cheat focus |
| Greenhouse Inclusion | https://www.greenhouse.io/inclusion | Blind screening + structured calibration + demographic survey |
| Textio | https://textio.com/developers | JD bias scrub + female applicant rate lift |
| Datapeople | https://datapeople.io/ | JD optimization + template enforcement |
| Applied | https://www.appliedhq.co/ | Free blind hiring fallback |
| GapJumpers | https://gapjumpers.me/ | Free blind hiring alternative |
| BrightHire | https://docs.brighthire.ai/ | Interview recording + transcription + AI summary |
| Metaview | https://www.metaview.ai/ | Interview intelligence alt + smart notes |
| Pillar | https://www.pillar.hr/ | Real-time interviewer coaching |
| Pinpoint AI | https://www.pinpointhq.com/developers | AI applicant ranking + Career Sites + bias-audited |
| Eightfold AI | https://eightfold.ai/ | Talent intelligence + bias-aware matching + Career Hub |
| Paradox Olivia | https://www.paradox.ai/olivia | High-volume conversational AI screening |
| Phenom | https://www.phenom.com/talent-experience/talent-pipeline | Silver-medalist + Career Sites + Talent Pipeline |
| ERIN | https://erinapp.com/ | Gamified employee referral program |
| Teamable | https://teamable.com/ | Network-based referral + warm-intro |
| Boon | https://www.boon.co/ | Referral platform + bonus payout cadence |
| Gloat | https://gloat.com/ | AI internal talent marketplace |
| Enboarder | https://www.enboarder.com/ | Pre-boarding + post-offer touch-base |
| Heidrick & Struggles / Spencer Stuart / Russell Reynolds / Egon Zehnder | https://www.heidrick.com/ etc | C-level retained search |
| True Search / Riviera Partners / Daversa Partners | https://truesearch.com/ etc | Tech VP + venture-backed retained search |
| Talent Board CandE Awards | https://www.thetalentboard.org/cande-research-reports/ | Candidate experience NPS benchmarks |
| Schmidt & Hunter (1998) | https://psycnet.apa.org/record/1998-10661-006 | Predictive validity of selection methods (r=0.51 structured) |
| Project Implicit IAT | https://implicit.harvard.edu/implicit/ | Bias-awareness training reference |
| EEOC AI Employment Decisions | https://www.eeoc.gov/laws/guidance/ai-employment-decisions | AI screening compliance guidance |
| NYC Local Law 144 | https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page | Bias audit + candidate disclosure for AI screening |
| EEOC EEO-1 | https://www.eeoc.gov/employers/eeo-1-data-collection | Annual EEO-1 reporting requirements |
| OFCCP | https://www.dol.gov/agencies/ofccp | Federal contractor compliance |

## Notes on authored-from-synthesis

Sections that aren't directly lifted from a single source (operational glue):

- **Soul.md "Decision rule" in execution stack** — synthesis from talent-sourcer + ceo-agent patterns; no single canonical source for the phrasing.
- **Soul.md "When invoked" mode procedures** — synthesis from per-platform docs (Greenhouse + Ashby + Lever) into a unified procedure per mode.
- **Role.md "Per-stage assignment matrix" patterns** — derived from competency-modeling best practices + Greenhouse Inclusion + Ashby docs.
- **Role.md "Decision matrix" tables** — distilled from multi-tool comparison sources into agent-friendly tables.

## Refreshing from upstream

When SOTA tools change (e.g., new ATS API version, NYC LL144 amendments, EEOC new AI guidance):

1. Update the relevant skill pack(s) in `agents/recruiter/skills/<name>/SKILL.md` (Round 2 deliverables).
2. Update the SOTA sources table above.
3. Update `reference/SOTA_USE_CASES.md` confidence ratings if applicable.
4. Re-run `python verify.py recruiter` to confirm structure intact.
5. Re-build: `python build.py recruiter` produces a fresh `.craftbot`.

For the canonical reference repos (Step 2 of methodology):
- `wshobson/agents` — repull every quarter for SOTA agent definitions.
- `VoltAgent/awesome-claude-code-subagents` — same cadence.
- `msitarzewski/agency-agents` — same cadence.
- `vijaythecoder/awesome-claude-agents` — same cadence.

For SOTA tool refreshes:
- ATS landscape (Greenhouse / Ashby / Lever) — quarterly check for API version bumps + new endpoints
- DEI / AI-screening compliance (NYC LL144 / Illinois / CO SB 24-205 / EEOC) — quarterly check for new state laws + amendments; legal-counsel review on changes
- Comp intelligence (Pave / Carta / Compa / Levels.fyi / Radford) — monthly comp band refresh
- Interview intelligence (BrightHire / Metaview / Pillar) — quarterly product check
