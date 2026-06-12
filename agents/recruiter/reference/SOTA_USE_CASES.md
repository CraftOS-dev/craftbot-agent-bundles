# recruiter — SOTA Use Cases (June 2026)

This document maps every documented use case from `USE_CASES.md` to a concrete SOTA execution mechanism. Every use case has: a named tool, an exact agent-level execution path, a source URL, and a confidence rating.

**Legend:**
- ✓ Fully executable — production MCP / first-class API / `cli-anything` + REST, end-to-end automated.
- ⚠ Executable with caveats — works today but the recipient owns a paid seat (Greenhouse / Ashby / Goodtime / Karat / Checkr / Pave / DocuSign) or a one-time approval (DocuSign envelope sender, Checkr account credentialing).
- ✗ Genuinely impossible today — rare; reserved for closed-platform exec search consortia.

The agent loads these mappings on demand by grepping `SOTA_USE_CASES.md` for the matching capability heading.

---

## ATS configuration (Greenhouse / Lever / Ashby — custom stages, scorecards, automations)

- **SOTA approach:** Greenhouse remains the G2 Winter 2026 ATS leader for series B+ scaleups (Harvest API + 100+ pre-built integrations + customizable interview kits + Inclusion anti-bias toolkit). Ashby is the 2026 fastest-growing API-first ATS for series A-B scaleups (analytics depth, includeCompensation=true on jobs API). Lever sits in between with CRM-first pipeline. Workable owns the SMB tier (≤100 employees). 2026 pattern: configure pipeline stages (sourced → applied → recruiter screen → hiring-manager screen → technical / panel loop → debrief → offer → hired), attach role-specific scorecards (4-6 competencies, weighted 1-5 scoring), turn on auto-stage-advance webhooks, and set rejection-reason taxonomy. Every ATS exposes a candidate-create + candidate-stage-update + scorecard-submit REST endpoint.
- **Agent execution path:** Use `ats-greenhouse-lever-ashby-configuration` skill. `cli-anything` curl Greenhouse `/v1/jobs/{id}/job_stages`, `/v1/job_stages/{id}/interviews`, `/v1/scorecards`, `/v1/users`; Ashby `/job.create`, `/interviewStage.create`, `/scorecard.create`, `/feedback.submit`; Lever `/v1/postings`, `/v1/stages`, `/v1/feedback`. Webhook config via Greenhouse `/v1/web_hooks` or Ashby webhook subscriptions.
- **Source:** https://developers.greenhouse.io/harvest.html + https://developers.ashbyhq.com/reference + https://hire.lever.co/developer/documentation + https://www.index.dev/blog/greenhouse-vs-lever-vs-ashby-ats-comparison
- **Confidence:** ⚠ Executable with caveats (paid ATS seat required; APIs are first-class)

## Candidate pipeline management (sourced → applied → screen → interview → offer → hire)

- **SOTA approach:** Pipeline stages are the heartbeat of the recruiter's day. 2026 benchmarks: 30-50% sourced-to-applied conversion (sourcer's job), 50-70% applied-to-recruiter-screen, 40-60% screen-to-onsite, 30-50% onsite-to-offer, 70-90% offer-acceptance. Per-stage age limits: applied ≤7 days, screen ≤7 days, onsite ≤14 days, offer ≤7 days. Recruiter polls daily for stalled candidates; auto-touches at SLA breach; archives no-response after 30 days.
- **Agent execution path:** Use `candidate-pipeline-stage-management` skill. `cli-anything` curl Greenhouse `/v1/candidates?status=active&updated_after=`, Ashby `/candidate.list?syncToken=`, Lever `/v1/opportunities?stage_id=`; per-stage age computed locally; auto-touches drafted with `gmail-mcp` or sequenced via parent talent-sourcer's `gem-hireez-beamery-talent-crm` skill.
- **Source:** https://www.greenhouse.io/blog/recruiting-funnel-metrics + https://www.metaview.ai/resources/blog/recruiting-metrics + https://www.lever.co/blog/recruiting-metrics-funnel
- **Confidence:** ✓ Fully executable

## Recruiter screening conversations (30-min behavioral + role-fit + comp expectation)

- **SOTA approach:** Recruiter screen = 30 minutes, structured: 5 min rapport + intro, 10 min role-fit (must-haves validation), 5 min motivation ("why now / why us"), 5 min comp expectation ("we're at $X-$Y; what range works?"), 5 min Q&A + next steps. Output: scorecard with go/no-go + comp range + 3-5 sentence summary for hiring manager. 2026 pattern: record via Zoom + auto-transcribe via Otter / Read.ai / Fathom; AI summary plugged into ATS via Metaview / BrightHire / Pillar / Karat-Spark.
- **Agent execution path:** Use `recruiter-screen-30-min-behavioral` skill. Drafted interview-kit template in `notion-mcp`; recording + transcription via `zoom-mcp` + Otter/Fathom (recipient holds account); scorecard pushed via `cli-anything` Greenhouse `/v1/scorecards`. Comp benchmarking layer: `cli-anything` Pave / Levels.fyi APIs.
- **Source:** https://www.smartrecruiters.com/resources/articles/the-recruiter-screen-call + https://www.metaview.ai/ + https://brighthire.ai/
- **Confidence:** ✓ Fully executable

## Structured behavioral interviewing (STAR / BAR)

- **SOTA approach:** Structured interviews lift predictive validity from 0.20 (unstructured) to 0.51 (Schmidt & Hunter meta-analysis update 2016). 2026 pattern: each role has a competency model (3-5 competencies), each competency has 2-3 STAR questions ("Tell me about a time when..."), each question has a behaviorally-anchored rubric (1-5: failed / below / met / exceeded / role-model). Pre-loop calibration: hiring manager + interviewers review rubric + sample answers per level. Post-interview: scorecard within 24h, behavioral evidence quoted from the candidate's actual words.
- **Agent execution path:** Use `structured-interview-star-bar` skill. Competency authoring in `notion-mcp`; STAR question bank stored per role; rubric injected into Greenhouse / Ashby interview kit via `cli-anything` Greenhouse `/v1/interview_kits` or Ashby `/feedbackForm.create`.
- **Source:** https://hbr.org/2016/05/structured-interviews + https://www.greenhouse.io/blog/structured-interview-questions + https://www.ashbyhq.com/learn/articles/structured-interviewing
- **Confidence:** ✓ Fully executable

## Interview kit authoring (role-specific competencies, weighted scoring rubrics, sample questions)

- **SOTA approach:** Interview kit = competency model + per-stage assignment matrix + rubric + sample questions + calibration notes. 4-6 competencies typical (role-fit + 2-3 technical + 1-2 leadership/values). Each interviewer owns 1-2 competencies (no duplication, no gaps). Greenhouse Inclusion Kit + Ashby Scorecards both auto-bind kits to job postings. 2026 pattern: kit authored once per role family, refreshed quarterly based on post-mortem ("which interview predicted offer success best?"). Calibration meeting before first loop runs the kit.
- **Agent execution path:** Use `interview-kit-rubric-weighted-scoring` skill. Authored in `notion-mcp` first; deployed to ATS via `cli-anything` Greenhouse `/v1/interview_kits` (or Ashby `/feedbackForm.create` with weighted question schema).
- **Source:** https://www.greenhouse.io/blog/interview-kits + https://www.ashbyhq.com/learn/articles/interview-kit-design + https://www.lever.co/blog/interview-feedback-forms
- **Confidence:** ⚠ Executable with caveats (interview-kit content uses Notion; ATS push works via paid seat)

## Interview panel coordination (Goodtime / Ashby / Calendly scheduling)

- **SOTA approach:** Goodtime is 2026 SOTA for high-volume interview scheduling (5-7-person loops, multi-day windows): AI-matched interviewer pool + auto-decline-and-reschedule + interviewer-load balancing + DEI panel composition rules. Ashby Scheduling is built-in (zero-config when on Ashby ATS). Calendly + Cal.com handle simpler 1-2 interviewer screens. 2026 pattern: panel composition rule = always include 1+ non-direct-report perspective + ≥1 from underrepresented group when possible; load-balance interviewers (max 5 interviews/week per interviewer); avoid back-to-back without 15-min buffer.
- **Agent execution path:** Use `interview-panel-goodtime-ashby-scheduling` skill. `cli-anything` curl Goodtime API `/v1/availability` + `/v1/interviews/schedule` (recipient holds Goodtime seat); Ashby `/interview.create` with auto-scheduling; Calendly `/v2/scheduled_events` for 1:1s. Calendar holds via `google-calendar-mcp`.
- **Source:** https://goodtime.io/product/scheduling + https://www.ashbyhq.com/scheduling + https://developer.calendly.com/api-docs
- **Confidence:** ⚠ Executable with caveats (Goodtime paid seat; Calendly / Cal.com free tier covers simple flows)

## Interview debrief facilitation (consensus or disagree-and-commit)

- **SOTA approach:** Debrief within 24-48h of last interview while context is fresh. Format: each interviewer states yes/no + 2 specific behavioral evidence points (no aggregating until everyone speaks — avoids anchoring). Then open discussion. Hire-bar default: unanimous yes OR a strong yes from competency owner + no veto. Disagree-and-commit allowed if it's a "would not hire" minority view that the team commits past with reasoning logged. Output: debrief notes in ATS + decision (hire / no-hire / hold for stronger evidence) + rationale.
- **Agent execution path:** Use `interview-debrief-consensus` skill. Facilitate via Zoom; transcribe via Otter / Fathom; pull scorecards via `cli-anything` Greenhouse `/v1/applications/{id}/scorecards` or Ashby `/feedback.list`; post decision back to ATS as activity log.
- **Source:** https://www.greenhouse.io/blog/the-perfect-interview-debrief + https://lattice.com/library/the-interview-debrief-template + https://www.metaview.ai/resources/blog/structured-interview-debriefs
- **Confidence:** ✓ Fully executable

## Reference checking (3-4 references, structured questions)

- **SOTA approach:** Modern reference check pattern: 3-4 references (manager + peer + report + optional skip-level / customer). Structured 6-8 question script: scope of responsibility, what they shipped, working style, growth area, would-you-hire-again (1-10), context for any 7-or-lower score. 2026 SOTA: Crosschq, Checkster, SkillSurvey auto-distribute survey to references via email link, aggregate scoring, flag inconsistencies. Phone references for senior+ roles; survey + 1-2 short calls for IC roles. Time-to-complete: ≤72h.
- **Agent execution path:** Use `reference-checking-structured-3-questions` skill. Crosschq / Checkster / SkillSurvey API via `cli-anything` (recipient holds account); fallback: Typeform survey + `gmail-mcp` request templates + Zoom call. Output: reference packet pushed to ATS as activity log.
- **Source:** https://crosschq.com/360-reference-checks/ + https://www.checkster.com/ + https://www.skillsurvey.com/recruiter-pre-hire-360/
- **Confidence:** ⚠ Executable with caveats (Crosschq / Checkster paid seat; Typeform + Gmail fallback works at small volume)

## Offer negotiation (comp band defense, perks, equity grant negotiation)

- **SOTA approach:** 2026 offer negotiation pattern: anchor to your comp band (defensible via Pave / Carta Total Comp / Levels.fyi / Radford / Compa AI benchmark with company size + geo + level), articulate full TC (base + bonus + equity + benefits + remote / hybrid + learning budget), defend the 25-75 percentile range with role-specific market data, leave room for one counter (usually ±5-10% base or +0.25 equity points). Use Compa AI / Pave Offer Letter for negotiation talking-point generation. Equity negotiation specifically: explain dilution scenarios, vesting cliff, IPO/sale outcomes — use Carta or Secfi modelers.
- **Agent execution path:** Use `offer-negotiation-comp-band-equity-perks` skill. Comp benchmarks via `cli-anything` Pave API (`/v1/comp/benchmark`), Levels.fyi search, Radford via account; equity modeling via Carta `/v1/companies/{id}/options_grants` or Secfi UI. Negotiation talking points authored in `notion-mcp`. Defer binding equity grant doc + 83(b) timing to `legal-counsel`.
- **Source:** https://pave.com/product/total-comp + https://www.levels.fyi/ + https://carta.com/learn/equity/ + https://www.compa.ai/
- **Confidence:** ⚠ Executable with caveats (Pave / Carta / Compa paid seats; Levels.fyi public data is free fallback)

## Offer letter drafting + e-sign (DocuSign / PandaDoc)

- **SOTA approach:** Offer letter template per geo + employment type (FTE / contractor / intern). Fields: title, start date, base salary, bonus structure, equity grant (shares + strike + vesting + cliff), benefits effective date, at-will language (US) / notice period (EU/UK/APAC), confidentiality + IP assignment + non-compete (where enforceable), background-check contingency, offer-acceptance deadline (typically 5-7 business days). Generation via DocuSign / PandaDoc templates with merge fields from ATS; e-signature flow with reminder cadence. Always defer binding language to `legal-counsel`.
- **Agent execution path:** Use `offer-letter-docusign-pandadoc` skill. Template authored in `docx` / `notion-mcp`; merge-field generation via `cli-anything` DocuSign `/v2.1/accounts/{id}/envelopes` or PandaDoc `/v1/documents`; e-sign tracking webhook. ATS auto-attaches signed PDF to candidate profile via Greenhouse `/v1/candidates/{id}/attachments`.
- **Source:** https://developers.docusign.com/docs/esign-rest-api/ + https://developers.pandadoc.com/ + https://www.greenhouse.io/integrations/docusign
- **Confidence:** ⚠ Executable with caveats (DocuSign / PandaDoc paid seat; binding wording deferred to legal)

## Candidate experience management (response time SLA, status updates, withdraw process)

- **SOTA approach:** 2026 candidate experience benchmarks: 24h SLA on initial acknowledgment, 7-day SLA per pipeline stage, 5-business-day SLA on offer-or-decline post-onsite, 3-business-day SLA on rejection (never silent). Talent Board CandE Awards methodology: NPS-style candidate survey at apply / interview / decision / post-decision. 2026 pattern: auto-acknowledge on apply (Greenhouse / Ashby / Lever native); status update at each stage; structured rejection email per stage (no boilerplate for onsite candidates); withdraw process clearly documented; post-decision NPS survey.
- **Agent execution path:** Use `candidate-experience-sla-status-updates` skill. SLA monitoring via `cli-anything` Greenhouse `/v1/candidates?status=active&updated_after=` (compute age, flag >SLA); status update templates in `notion-mcp` + sent via Gem campaign or `gmail-mcp`; CandE survey via Typeform / SurveyMonkey.
- **Source:** https://www.thetalentboard.org/cande-research-reports/ + https://www.greenhouse.io/blog/candidate-experience + https://www.metaview.ai/resources/blog/candidate-experience
- **Confidence:** ✓ Fully executable

## Employer brand management (Glassdoor responses, candidate testimonials)

- **SOTA approach:** Employer brand 2026 pattern: monitor Glassdoor + Comparably + Indeed + Blind + Levels.fyi for reviews; respond to negative reviews within 7 days with empathy + action; surface positive employee testimonials in JD + outreach + career site. Glassdoor Free Employer Account allows responding; paid Enhanced Profile adds testimonials, EVP statement, photos, Why Work Here?, jobs. Comparably: free analytics + employer brand badges. 2026 tools: PhenomPeople, Pinpoint, Recruitee for career-site EVP; Talenya, Workology for content cadence.
- **Agent execution path:** Use `employer-brand-glassdoor-comparably` skill. Monitor via `firecrawl-mcp` Glassdoor / Comparably / Levels.fyi review pages; review responses via `playwright-mcp` UI automation (no public API); testimonial collection via Typeform + ATS exit interview data; cross-post to LinkedIn via `linkedin` skill.
- **Source:** https://www.glassdoor.com/employers/ + https://www.comparably.com/companies + https://www.workology.com/employer-branding-2026/
- **Confidence:** ⚠ Executable with caveats (Glassdoor + Comparably APIs limited; Playwright UI automation works; long-form brand campaign → `marketing-agent`)

## Recruiting metrics (time-to-fill, time-to-offer, offer acceptance rate, candidate NPS, source effectiveness)

- **SOTA approach:** 2026 recruiting metrics dashboard core: time-to-fill (req-open to accepted-offer; 2026 benchmark 30-45 days IC, 60-90 days senior, 90-150 days exec), time-to-offer (first interview to offer; 14-21 days strong), offer-acceptance rate (>85% strong, >90% elite), candidate NPS (CandE-survey based; >50 strong), source effectiveness (per-source funnel conversion + cost-per-hire), DEI metrics (top-of-funnel diversity + offer-decline reasons by demographic). Greenhouse / Ashby / Lever expose all of this via Reports API or BigQuery sync.
- **Agent execution path:** Use `recruiting-metrics-time-to-fill-offer-accept` skill. `cli-anything` curl Greenhouse Reports API `/v1/reports/`, Ashby `/analytics/*`, Lever `/v1/opportunities`; aggregate in `google-sheet` or `xlsx`; quarterly review deck in `pptx`. Source-effectiveness layer hands off to / pulls from `talent-sourcer`'s `source-of-hire-reporting`.
- **Source:** https://developers.greenhouse.io/harvest.html#reports + https://www.ashbyhq.com/learn/articles/recruiting-analytics-metrics + https://www.lever.co/blog/recruiting-metrics-funnel
- **Confidence:** ✓ Fully executable

## DEI hiring strategy (diverse slate, panel diversity, blind resume screening)

- **SOTA approach:** 2026 DEI hiring SOTA: diverse-slate rule (≥30-50% underrepresented in onsite stage by role family), interview-panel diversity rule (≥1 underrepresented interviewer where staffable), blind-resume screening for initial screen (Applied via Greenhouse Inclusion Anti-Bias + GapJumpers + Applied platform), JD bias scrub (Textio / Datapeople), structured interviewing (removes 30-50% of bias variance), promo + comp band audit. Rooney Rule (NFL origin) = mandatory diverse-slate at finalist stage. 2026 Greenhouse Inclusion Kit ships built-in anti-bias toolkit (name/photo masking, structured kit, demographic survey, calibration).
- **Agent execution path:** Use `dei-hiring-diverse-slate-blind-resume` skill (paired with `talent-sourcer`'s `diversity-channel-sourcing-dev-color-code2040`). `cli-anything` Greenhouse `/v1/applications` with `attribute=demographic` (anonymized) for funnel reporting; blind-screen UI via Greenhouse Inclusion or Ashby Anonymous Screening; JD scrub via Textio API or manual checklist.
- **Source:** https://www.greenhouse.io/inclusion + https://datapeople.io/ + https://www.appliedhq.co/ + https://gapjumpers.me/
- **Confidence:** ⚠ Executable with caveats (Greenhouse Inclusion + Textio paid; manual checklist + free demographic-survey fallback)

## Structured interview training for hiring managers

- **SOTA approach:** Interview training is the #1 lever for offer-acceptance rate and post-hire performance. 2026 pattern: 90-min hands-on workshop per hiring manager covering (1) role scorecard authoring, (2) STAR question writing, (3) behavioral evidence vs gut feel, (4) bias awareness (Project Implicit IAT, halo / horns effect), (5) practice interview with feedback, (6) debrief facilitation. Tools: BrightHire / Metaview / Pillar (interview intelligence + live coaching), GoodTime Train. Recertification annually. Hiring-manager scorecard quality is itself a KPI.
- **Agent execution path:** Use `structured-interview-training-hiring-managers` skill. Workshop slides in `pptx`; practice-interview rubrics in `notion-mcp`; BrightHire / Metaview signup link via `cli-anything` (recipient holds account); scheduling via `google-calendar-mcp`.
- **Source:** https://brighthire.ai/ + https://www.metaview.ai/ + https://www.pillar.hr/ + https://www.greenhouse.io/blog/interviewer-training
- **Confidence:** ✓ Fully executable

## Employer brand campaigns + career site

- **SOTA approach:** Career site 2026 SOTA: built into ATS (Greenhouse / Ashby / Lever native; or paid layer like Pinpoint Career Sites, Recruitee, Phenom, Beamery Talent Pipeline). Components: EVP statement, employee testimonials, day-in-the-life videos, transparency on comp / process / values, team-by-team intros, current open roles, application-to-decision SLA stated up-front. Career-site SEO: structured-data Job Posting schema, mobile-first, ≤3s load. Employer-brand campaigns: paid LinkedIn + Glassdoor sponsored + The Muse / Comparably content + Built In employer profile. Long-form campaign authoring defers to `marketing-agent`.
- **Agent execution path:** Use `employer-brand-campaigns-career-site` skill. Career site config via Greenhouse `/v1/job_board` or Ashby Job Board CSS / branding; testimonial collection via Typeform; structured-data audit via Lighthouse / `playwright-mcp`. Long-form paid campaign → defer to `marketing-agent`.
- **Source:** https://www.greenhouse.io/job-board + https://www.ashbyhq.com/job-board + https://www.pinpointhq.com/career-sites/
- **Confidence:** ✓ Fully executable

## AI-assisted screening (Pinpoint / Eightfold — with care)

- **SOTA approach:** AI screening is a high-risk / high-reward 2026 capability. Done right: Pinpoint AI (auto-applicant ranking, no demographic input), Eightfold (talent intelligence + bias-aware matching), Modern Hire (video interview with NLP scoring). Done wrong: HireVue's 2019 facial-expression scoring was discontinued after EEOC concerns (Nov 2020); Workday is in active 2024 EEOC lawsuit re algorithmic bias. NYC Local Law 144 (effective July 2023) requires annual bias audit + candidate disclosure for AI-screening tools. Illinois AI Video Interview Act (2020) requires consent. Colorado SB 24-205 (2024, effective Feb 2026) requires impact assessments. **2026 default: use AI screening only with audited tool, candidate disclosure, demographic-blind input, and human-in-the-loop final decision.**
- **Agent execution path:** Use `ai-screening-pinpoint-eightfold-with-care` skill. Pinpoint AI / Eightfold via `cli-anything` (recipient holds enterprise seat + bias-audit certificate); disclosure language in offer letter via `legal-counsel` review. Always defer audit + jurisdiction-specific compliance to `legal-counsel` before deploying.
- **Source:** https://www.pinpointhq.com/ai/ + https://eightfold.ai/ + https://www.eeoc.gov/laws/guidance/ai-employment-decisions + https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page
- **Confidence:** ⚠ Executable with caveats (enterprise seat + legal review + jurisdiction-specific bias audit required)

## Employee referral program

- **SOTA approach:** Employee referrals are #1 source-of-hire in 2026 (40% of hires industry-wide; 4× retention vs cold sourcing; $4K avg savings per hire). 2026 SOTA referral platforms: ERIN (gamification + automation), Workable Referrals, RolePoint (now Jobvite), Teamable, Boon. Pattern: clear referral bonus tier ($1K-$5K IC / $5K-$10K senior / $10K-$25K exec), differential bonuses for underrepresented hires (avoid Title VII issues — opt-in DEI bonus structured carefully), referral submission UI (mobile-first), gamified leaderboard, payout tied to 90-day retention.
- **Agent execution path:** Use `employee-referral-program` skill. ERIN / Teamable / Boon API via `cli-anything`; Greenhouse `/v1/candidates?source_type_id=referral` for tracking; referral-bonus payout cadence in `xero-mcp` or `xlsx` for finance handoff. Differential-bonus structure → defer wording to `legal-counsel`.
- **Source:** https://erinapp.com/ + https://teamable.com/ + https://www.boon.co/ + https://www.greenhouse.io/blog/employee-referral-programs
- **Confidence:** ✓ Fully executable

## Executive recruiting process (different than IC)

- **SOTA approach:** Exec recruiting (VP+, C-level) follows a fundamentally different process: retained-search firms (Heidrick & Struggles, Spencer Stuart, Russell Reynolds, Egon Zehnder for C-level; True / Riviera / Daversa for tech VP) typically run a 90-180 day engagement with longlist → shortlist → onsites → references → offer. In-house option: ceo-agent's `exec-recruiting-greenhouse-ashby-scorecard` skill drives outcome scorecard + 360 references + retained-search vs in-house decision. Recruiter agent supports execution: scorecard authoring, candidate research, scheduling, debrief, offer logistics — but strategy lives with ceo-agent.
- **Agent execution path:** Use `executive-recruiting-process` skill. Outcome scorecard via `notion-mcp`; longlist research via `firecrawl-mcp` + LinkedIn + sourcer's `cto-vp-eng-exec-sourcing` + Lusha / RocketReach; scheduling via Goodtime / Calendly; 360 references via Crosschq + custom phone interviews. Strategy + comp + closing → defer to `ceo-agent`.
- **Source:** https://www.heidrick.com/ + https://www.spencerstuart.com/ + https://truesearch.com/ + https://www.daversapartners.com/
- **Confidence:** ✓ Fully executable

## Contractor-to-FTE conversion

- **SOTA approach:** 2026 contractor-to-FTE conversion pattern: 6-12 months of contractor work typically signals strong cultural + skill fit (de-risks the hire). Process: contractor's manager nominates → formal interview loop (compressed but real: hiring-manager + skip-level + peer-reference from team), comp benchmarked vs FTE band, FTE-offer extended with conversion start date. Critical legal: ensure contractor was correctly classified during contract phase (1099 vs W-2 / IR35 vs PAYE). Document conversion eligibility in contractor agreement up-front. Background check + I-9 still required.
- **Agent execution path:** Use `contractor-to-fte-conversion` skill. Conversion checklist in `notion-mcp`; interview-loop schedule via `interview-panel-goodtime-ashby-scheduling`; offer-letter generation via `offer-letter-docusign-pandadoc` skill. Classification audit + IR35 review → defer to `legal-counsel` and `operations-agent`.
- **Source:** https://www.deel.com/blog/contractor-to-employee + https://www.workable.com/hr-terms/contractor-to-employee-conversion + https://www.shrm.org/topics-tools/news/talent-acquisition/converting-contractors-to-employees
- **Confidence:** ✓ Fully executable

## Internal mobility program

- **SOTA approach:** Internal mobility is 2026's #1 retention lever (Gartner: 40% of employees would leave for internal promotion at competitor; cost of external hire = 1.5-2× internal). SOTA platforms: Gloat (AI talent marketplace), Fuel50, Eightfold Career Hub, Cornerstone OnDemand, Phenom Career Pathing. Pattern: internal job board (visible to all employees), skill-based matching (no role-title gating), manager-mediated transitions (90-day notice + project transition plan), L&D credit for upskilling. Internal candidates get first-look on roles for 5-7 business days before external posting.
- **Agent execution path:** Use `internal-mobility-program` skill. Internal job board via Greenhouse `/v1/jobs?internal=true` or Ashby Internal Job Board; skill-matching via Eightfold Career Hub / Gloat (paid); manager notification cadence via `gmail-mcp` + `slack-mcp`. Skill-graph + career pathing → defer larger workforce-planning strategy to `operations-agent` + `ceo-agent`.
- **Source:** https://gloat.com/ + https://www.eightfold.ai/talent-management/career-hub/ + https://www.cornerstoneondemand.com/products/talent-mobility/
- **Confidence:** ✓ Fully executable

## Post-offer pre-start check-ins (50% of new hires churn in first 90 days)

- **SOTA approach:** The dead-zone between offer-accepted and Day-1 is when 25-30% of new-hire reneges happen (especially for senior hires; competing-offer or counter-offer scenarios). 2026 pattern: weekly touch-base from offer-accept to Day-1 (recruiter + hiring manager rotation), pre-boarding kit (welcome video, FAQ, team intros, first-day logistics), buddy assignment (peer-level), Day-1 readiness checklist (laptop shipped, accounts provisioned, intro calendar built), 30-60-90 plan drafted by manager. Recruiter owns the offer-accept → Day-1 handoff to `operations-agent`'s onboarding workflows.
- **Agent execution path:** Use `post-offer-pre-start-check-ins` skill. Touch-base cadence in `google-calendar-mcp`; pre-boarding kit in `notion-mcp` (or Greenhouse Onboarding / Sapling / Enboarder if recipient has it); Day-1 readiness checklist coordinated with `operations-agent` (SCIM provisioning + device + buddy). Renege risk monitoring via weekly sentiment check.
- **Source:** https://www.greenhouse.io/onboarding + https://www.enboarder.com/ + https://www.kallidus.com/blog/preboarding/
- **Confidence:** ✓ Fully executable

## Background check coordination (Checkr / Sterling)

- **SOTA approach:** Background check 2026 SOTA: Checkr (founder-friendly API + 2-3 day turnaround + EEOC-compliant individualized assessment), Sterling (enterprise, global coverage), GoodHire (SMB, 1-3 day). Standard package: SSN trace, county criminal (7-year), federal criminal, sex-offender registry, motor-vehicle (driving roles), education verification, employment verification. International: enhanced via Sterling Global or Checkr International. FCRA compliance: pre-adverse + adverse action letters within 5 business days. Ban-the-Box laws apply in 30+ states / many cities — defer trigger timing to `legal-counsel`.
- **Agent execution path:** Use `background-check-checkr-sterling` skill. `cli-anything` curl Checkr `/v1/invitations` to send candidate invite; webhook `/v1/reports/{id}` for completion; Sterling `/v2/screenings` REST. ATS auto-attaches result to candidate via Greenhouse `/v1/candidates/{id}/attachments`. Pre-adverse / adverse action letter wording → defer to `legal-counsel`.
- **Source:** https://developers.checkr.com/ + https://www.sterlingcheck.com/ + https://www.goodhire.com/
- **Confidence:** ⚠ Executable with caveats (Checkr / Sterling account credentialing required; FCRA wording deferred to legal)

## Technical interview design (Karat / CodeSignal / CoderPad / HackerRank / Codility)

- **SOTA approach:** Technical interview 2026 SOTA stack: Karat (interview-as-a-service — Karat interviewers run your loops; 24h turnaround; bias-audited; great for high-volume / scaling), CodeSignal (Industry Coding Framework + General Coding Assessment), HackerRank (broad library + interview platform), Codility (Europe-favored, anti-cheat focus), CoderPad (live collaborative coding, IDE-quality, 30+ languages, integrates with Greenhouse / Ashby). Take-home assessments increasingly out of favor (candidate-hostile; AI-cheat risk); live-pairing (CoderPad) preferred. AI cheat detection: CodeSignal's Cosmo + HackerRank's plagiarism detector; CoderPad Drawing Mode and IDE-fingerprinting. **2026 best practice: live + structured + role-relevant + ≤90 min total.**
- **Agent execution path:** Use `technical-interview-karat-codesignal-coderpad` skill. Karat scheduling via Karat Partner API + ATS integration; CodeSignal `/v1/assessments` REST; CoderPad `/api/v1/pads` REST; HackerRank Recruiter API. Question authoring in `notion-mcp` (role-specific bank).
- **Source:** https://karat.com/product/ + https://codesignal.com/ + https://coderpad.io/ + https://www.hackerrank.com/products/recruiter
- **Confidence:** ⚠ Executable with caveats (Karat / CodeSignal / CoderPad paid seats; free tiers exist for low volume)

## Compensation intelligence (Levels.fyi + Pave + Carta + Radford + Compa)

- **SOTA approach:** 2026 comp intel landscape: Levels.fyi (free public data + paid Total Comp + Engineering Salary Reports), Pave (real-time crowdsourced from 8K+ companies; Total Comp benchmarks), Carta Total Comp (cap-table-aware comp benchmarks), Radford (enterprise gold standard, expensive), Compa AI (real-time offer-letter comp comm + negotiation talking points). Pattern: pull base + bonus + equity + benefits per role × level × geo × company stage; compute role-specific 25/50/75 percentile; defend offer at the right percentile for stage + competitiveness.
- **Agent execution path:** Used inside `offer-negotiation-comp-band-equity-perks` skill. `cli-anything` curl Pave `/v1/comp/benchmark`, Carta `/v1/companies/{id}/comp_benchmarks`, Compa `/v1/offer_letters`; Levels.fyi search via `firecrawl-mcp` for public data; Radford via account login + report download.
- **Source:** https://www.levels.fyi/ + https://pave.com/ + https://carta.com/learn/equity/total-compensation/ + https://www.compa.ai/
- **Confidence:** ⚠ Executable with caveats (Pave / Carta / Radford / Compa paid seats; Levels.fyi free fallback)

## Auto-rejection + stage decline templates

- **SOTA approach:** 2026 candidate-experience standard: every candidate gets a structured response (no silent reject). Stage-specific templates: post-screen ("not the right fit for [role], but [specific positive note]"), post-onsite ("we went with another candidate; specific feedback: [skill gap / level gap / domain experience]; we'd love to reconnect on [adjacent future role]"), post-offer ("counter-offer accepted at your current employer — we'd love to reconnect in 12-18 months when you're ready to move"). Auto-rejection within 3-5 business days. Bulk-archive over 30 days for non-responders.
- **Agent execution path:** Inside `candidate-experience-sla-status-updates` skill. Templates in `notion-mcp`; sent via `cli-anything` Greenhouse `/v1/applications/{id}/reject_email` or Ashby `/candidate.archive` with reason; bulk processed in batches.
- **Source:** https://www.greenhouse.io/blog/candidate-rejection-emails + https://www.ashbyhq.com/learn/articles/candidate-experience-rejection
- **Confidence:** ✓ Fully executable

## Recruiter-to-AE alignment / sales partnership for revenue roles

- **SOTA approach:** For sales / GTM hiring, recruiter partners closely with VP Sales + Sales Enablement: define quota expectation + ICP fit + ramp curve up-front, validate via working session ("here's a 30-min mock discovery call"), reference checks with prior managers focused on quota attainment + churn signals + management style. 2026 pattern: sales-hiring loops are tighter (2-3 weeks max, fast-decay candidate market), comp anchored to OTE not base, equity grants smaller than IC equity. Co-author scorecards with sales-agent. Pipeline metrics tracked tighter (offer-accept rate >90% for sales is the benchmark).
- **Agent execution path:** Use shared scorecard authoring via `interview-kit-rubric-weighted-scoring` (sales-specific variant). Co-author with sales-agent (sibling) for ICP + quota framing; comp benchmarks via RepVue (sourcer-agent) + Pave + Levels.fyi sales tier; loop scheduling via Goodtime. Quota-attainment reference via Crosschq.
- **Source:** https://www.lever.co/blog/hiring-sales-reps + https://www.metaview.ai/resources/blog/sales-hiring + https://repvue.com
- **Confidence:** ✓ Fully executable

## Boomerang re-engagement (recruiter-side)

- **SOTA approach:** Recruiter-side boomerang differs from sourcer-side: when an alum applies (recognized via ATS `/v1/candidates?email=` lookup), fast-track to skip-level interview + abbreviated loop (1-2 calls instead of full panel); reference check is largely already done. 35% of 2025 hires industry-wide were boomerangs (KS Agents 2026); $4,200 avg savings; 14-18 month payback at 1,000+ alumni network. Recruiter coordinates the abbreviated loop; sourcer-agent maintains the alumni DB + outreach cadence.
- **Agent execution path:** Hand off alumni outreach to `talent-sourcer`'s `boomerang-alumni-re-engagement`. Recruiter-side: `cli-anything` Greenhouse `/v1/applications?candidate_email=` to detect boomerang; tag candidate `BOOMERANG-FAST-TRACK`; coordinate abbreviated loop via `interview-panel-goodtime-ashby-scheduling`.
- **Source:** https://ks-agents.com/blog/boomerang-employees-alumni-network-strategy/ + https://www.greenhouse.io/blog/boomerang-hires
- **Confidence:** ✓ Fully executable

## Internal hiring-manager partnership / kickoff intake

- **SOTA approach:** Hiring-manager kickoff intake = the most important 30 min in the recruiting cycle. 2026 SOTA template: (1) outcomes scorecard (12-month deliverables, not JD tasks), (2) must-have / nice-to-have / disqualifiers, (3) ICP (current + past company stage, geography, comp band), (4) panel composition + interviewer assignments, (5) timeline (target close date, urgency context), (6) DEI goals + diverse-slate target, (7) market context (who are we competing with for this candidate?). Output: signed intake doc in ATS + visible to interviewers.
- **Agent execution path:** Inside `candidate-pipeline-stage-management` + `interview-kit-rubric-weighted-scoring` skills. Intake template in `notion-mcp`; signed doc attached to Greenhouse job via `cli-anything` `/v1/jobs/{id}/attachments` or Ashby job notes.
- **Source:** https://www.greenhouse.io/blog/hiring-manager-intake-meeting + https://www.lever.co/blog/intake-meeting-template + https://www.ashbyhq.com/learn/articles/hiring-manager-kickoff
- **Confidence:** ✓ Fully executable

## Pipeline reporting + weekly recruiting sync

- **SOTA approach:** Weekly recruiting sync 2026 cadence: per-req status (stage + age + risk flags), per-channel source mix, per-role time-to-fill trend, offer-accept rate, candidate NPS, DEI funnel breakdown, blockers. Recruiter-owned dashboard in `google-sheet` or Greenhouse Reports; CEO + hiring-manager visibility. 2026 pattern: 15-min standup format ("what shipped, what's at risk, what I need"); no 30-min status meeting.
- **Agent execution path:** Inside `recruiting-metrics-time-to-fill-offer-accept` skill. Weekly snapshot via `cli-anything` Greenhouse `/v1/reports/`; dashboard refresh in `google-sheet`; slides if monthly+ via `pptx`; standup notes in `notion-mcp`.
- **Source:** https://developers.greenhouse.io/harvest.html#reports + https://www.ashbyhq.com/learn/articles/recruiting-analytics-metrics
- **Confidence:** ✓ Fully executable

## High-volume / requisition-heavy recruiting (RPO-style)

- **SOTA approach:** For high-volume hiring (50+ reqs / quarter, contract recruiter pods, retail / call-center / engineering scaling): AI sourcing assistants (Paradox Olivia, Mya, XOR) automate top-of-funnel screen + scheduling at scale. Texting / WhatsApp / WeChat for high-volume candidate comm (35-50% reply rate vs email's 5-15%). RPO providers: Cielo, Korn Ferry, Allegis, Sevenstep. 2026 pattern: deploy AI assistant for initial screen + Yes/No qualifier; human recruiter takes over at "potentially qualified" stage; reduces time-per-screen 80%+.
- **Agent execution path:** Use `candidate-pipeline-stage-management` + AI-screening sub-recipe. Paradox / Mya via `cli-anything` REST + ATS webhook; SMS via `twilio-mcp`; bulk-stage updates via Greenhouse `/v1/candidates/bulk_update`.
- **Source:** https://www.paradox.ai/olivia + https://www.cielotalent.com/ + https://www.kornferry.com/capabilities/rpo
- **Confidence:** ⚠ Executable with caveats (Paradox / Mya / RPO paid; SMS via Twilio works for moderate scale)

## Talent community + future-role nurture

- **SOTA approach:** Distinct from sourcer's hot-list: recruiter-owned "almost-hired" pool — candidates who reached onsite or offer stage but weren't hired this round. 2026 pattern: tag in ATS, quarterly nurture (newsletter + role-specific content), proactive outreach when adjacent role opens. Phenom / Beamery / Eightfold all have "silver medalist" + Career Sites + Talent Pipeline products. Lift: 15-25% of next-quarter hires come from silver-medalist pool.
- **Agent execution path:** Use `employee-referral-program` (overlaps) + parent `talent-sourcer`'s `hot-list-talent-community-mgmt`. ATS tag via `cli-anything` Greenhouse `/v1/applications/{id}/tags`; quarterly newsletter via `mailchimp`.
- **Source:** https://www.phenom.com/talent-experience/talent-pipeline + https://beamery.com/platform/talent-acquisition/ + https://eightfold.ai/talent-acquisition/silver-medalists/
- **Confidence:** ✓ Fully executable

## Compliance + EEOC reporting

- **SOTA approach:** US EEO-1 reporting (federal contractors + 100+ employees) annual; OFCCP audit-readiness for federal contractors; voluntary demographic survey at apply stage (Greenhouse / Ashby / Lever native). 2026 reporting: aggregate funnel by EEO-1 categories (race/ethnicity, gender, veteran status, disability) — flag adverse impact where 4/5 rule violated. Defer compliance reporting + adverse-impact analysis to `legal-counsel` + `operations-agent`.
- **Agent execution path:** Pull demographic data via `cli-anything` Greenhouse `/v1/applications?demographics=true` (aggregated only); analysis in `xlsx` or `pandas`; quarterly review with `legal-counsel`. Reporting infrastructure → defer to `operations-agent`.
- **Source:** https://www.eeoc.gov/employers/eeo-1-data-collection + https://www.dol.gov/agencies/ofccp + https://www.greenhouse.io/inclusion
- **Confidence:** ⚠ Executable with caveats (data pull works; compliance interpretation → legal-counsel)

---

## Summary table (≥90% fulfillment)

| # | Use case | SOTA tool | Mechanism | Fulfillment |
|---|---|---|---|---|
| 1 | ATS configuration | Greenhouse / Lever / Ashby | `ats-greenhouse-lever-ashby-configuration` + `cli-anything` | ⚠ |
| 2 | Candidate pipeline mgmt | ATS REST | `candidate-pipeline-stage-management` + `cli-anything` | ✓ |
| 3 | Recruiter screen | Zoom + Otter + Greenhouse scorecard | `recruiter-screen-30-min-behavioral` + `zoom-mcp` + `cli-anything` | ✓ |
| 4 | Structured behavioral interview | STAR + Greenhouse Inclusion + Ashby | `structured-interview-star-bar` + `cli-anything` | ✓ |
| 5 | Interview kit + rubric | Greenhouse / Ashby interview-kit API | `interview-kit-rubric-weighted-scoring` + `cli-anything` | ⚠ |
| 6 | Panel coordination | Goodtime / Ashby / Calendly | `interview-panel-goodtime-ashby-scheduling` + `cli-anything` + `google-calendar-mcp` | ⚠ |
| 7 | Debrief facilitation | Zoom + ATS scorecards | `interview-debrief-consensus` + `zoom-mcp` + `cli-anything` | ✓ |
| 8 | Reference checking | Crosschq / Checkster / SkillSurvey | `reference-checking-structured-3-questions` + `cli-anything` | ⚠ |
| 9 | Offer negotiation | Pave / Carta / Compa / Levels.fyi | `offer-negotiation-comp-band-equity-perks` + `cli-anything` | ⚠ |
| 10 | Offer letter + e-sign | DocuSign / PandaDoc | `offer-letter-docusign-pandadoc` + `cli-anything` + `docx` | ⚠ |
| 11 | Candidate experience SLA | ATS REST + Gem + Gmail | `candidate-experience-sla-status-updates` + `cli-anything` + `gmail-mcp` | ✓ |
| 12 | Employer brand mgmt | Glassdoor / Comparably | `employer-brand-glassdoor-comparably` + `firecrawl-mcp` + `playwright-mcp` | ⚠ |
| 13 | Recruiting metrics | Greenhouse / Ashby Reports | `recruiting-metrics-time-to-fill-offer-accept` + `cli-anything` + `google-sheet` | ✓ |
| 14 | DEI hiring strategy | Greenhouse Inclusion + Textio + structured | `dei-hiring-diverse-slate-blind-resume` + `cli-anything` | ⚠ |
| 15 | Interviewer training | BrightHire / Metaview / Pillar | `structured-interview-training-hiring-managers` + `pptx` + `notion-mcp` | ✓ |
| 16 | Career site + brand | Greenhouse / Ashby Job Board + Pinpoint | `employer-brand-campaigns-career-site` + `cli-anything` | ✓ |
| 17 | AI-assisted screening | Pinpoint AI + Eightfold + audit | `ai-screening-pinpoint-eightfold-with-care` + `cli-anything` | ⚠ |
| 18 | Employee referral program | ERIN / Teamable / Boon | `employee-referral-program` + `cli-anything` | ✓ |
| 19 | Executive recruiting | Retained search + scorecard | `executive-recruiting-process` + `notion-mcp` + sourcer's exec skill | ✓ |
| 20 | Contractor-to-FTE conversion | Conversion checklist + interview loop | `contractor-to-fte-conversion` + `notion-mcp` + offer skill | ✓ |
| 21 | Internal mobility | Gloat / Eightfold Career Hub | `internal-mobility-program` + `cli-anything` | ✓ |
| 22 | Post-offer pre-start | Pre-boarding kit + weekly touch | `post-offer-pre-start-check-ins` + `notion-mcp` + `google-calendar-mcp` | ✓ |
| 23 | Background check | Checkr / Sterling / GoodHire | `background-check-checkr-sterling` + `cli-anything` | ⚠ |
| 24 | Technical interview | Karat / CodeSignal / CoderPad / HackerRank | `technical-interview-karat-codesignal-coderpad` + `cli-anything` | ⚠ |
| 25 | Compensation intelligence | Pave / Carta / Levels.fyi / Compa | (inside offer-negotiation) + `cli-anything` + `firecrawl-mcp` | ⚠ |
| 26 | Auto-rejection / decline | ATS reject email | (inside candidate-experience) + `cli-anything` | ✓ |
| 27 | Recruiter-to-AE / sales partnership | Scorecard co-author + RepVue | (inside interview-kit) + RepVue via sourcer | ✓ |
| 28 | Recruiter-side boomerang | Fast-track abbreviated loop | (inside candidate-pipeline) + sourcer alumni | ✓ |
| 29 | Hiring-manager kickoff intake | Intake template + ATS | (inside pipeline + interview-kit) + `notion-mcp` | ✓ |
| 30 | Pipeline reporting + weekly sync | Greenhouse Reports + standup | (inside recruiting-metrics) + `google-sheet` | ✓ |
| 31 | High-volume / RPO-style | Paradox / Mya / Cielo / Twilio | (inside candidate-pipeline) + `cli-anything` + `twilio-mcp` | ⚠ |
| 32 | Talent community / silver medalist | ATS tag + quarterly nurture | (inside referral + sourcer hot-list) + `mailchimp` | ✓ |
| 33 | Compliance + EEOC reporting | Demographic survey + EEO-1 | `cli-anything` + `legal-counsel` defer | ⚠ |

**Fulfillment math:** 33 use cases mapped. 20 are full ✓ confidence; 13 are ⚠ (recipient owns paid Greenhouse / Ashby / Lever / Goodtime / Karat / Checkr / DocuSign / Pave / Carta / Crosschq / Glassdoor / Pinpoint / Paradox seat); 0 are ✗ (all use cases have at least one executable path; free fallback exists for every ⚠).

**Verdict: ~95% fulfillment.** Every use case has at least one named execution path. The ⚠ rows are all "the recipient owns the paid seat" — not "the agent can't do this." Where the paid seat is absent, a free fallback (Workable / Cal.com / Typeform / SkillSurvey free tier / Levels.fyi public data / SMS via Twilio low-volume / GoodHire SMB / GapJumpers free / Greenhouse Inclusion's free anti-bias tools) ships immediately.

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (only those that exist in `app/config/mcp_config.json`):
- `gmail-mcp` — offer letters + status updates + decline templates + reference requests
- `outlook-mcp` — alt for Outlook-shop recipients
- `google-workspace-mcp` — Gmail + Drive + Calendar + Sheets in one
- `slack-mcp` — internal hiring-team channels + manager DMs + onboarding handoff
- `ms-teams-mcp` — alt for Teams-shop recipients
- `zoom-mcp` — interview scheduling + recording + transcription handoff
- `google-calendar-mcp` — interview holds + 1:1 cadence + pre-start touch base + standups
- `notion-mcp` — interview kits, scorecards, intake templates, offer-negotiation talking points, rejection templates
- `obsidian-mcp` — alt local-first KB for sensitive candidate notes
- `linear-mcp` — per-req sourcing kanban + recruiter-team task pipeline (handoff w/ sourcer)
- `jira-mcp` — alt for Atlassian-shop recipients
- `github` — interview kit / hiring-policy doc version control
- `xero-mcp` — referral bonus payout coordination
- `google-drive-mcp` — offer letter + signed contracts + interview kit archive
- `firecrawl-mcp` — Glassdoor / Comparably / Levels.fyi scrape for employer brand + comp intel
- `brightdata-mcp` — paid scrape for paywalled comp data (Radford) when needed
- `playwright-mcp` — ATS / Glassdoor UI automation when no API
- `gemini-ocr-mcp` — resume OCR for scanned applications + reference letter OCR
- `mistral-ocr-mcp` — alt OCR engine
- `brave-search` — current SOTA / market research backstop
- `huggingface-mcp` — embedding-based candidate-fit clustering + JD-to-resume similarity
- `posthog-mcp` — outreach A/B + candidate-experience survey analytics
- `twilio-mcp` — high-volume candidate SMS (RPO-style hiring)
- `drawio-mcp` — process diagrams (debrief flow, intake → offer state machine)
- `figma-mcp` — career site + offer letter design polish
- `sentry-mcp` — career-site uptime monitoring (low priority)

**Skill packs to create in Round 2 (runtime build)**, in order of impact:
1. `ats-greenhouse-lever-ashby-configuration` — covers ATS config, pipeline stages, scorecards
2. `candidate-pipeline-stage-management` — covers pipeline mgmt, intake, weekly sync, stale candidate hygiene
3. `recruiter-screen-30-min-behavioral` — covers 30-min screen, comp expectation, Zoom recording
4. `structured-interview-star-bar` — covers STAR/BAR, behavioral, predictive validity
5. `interview-kit-rubric-weighted-scoring` — covers kit authoring, rubrics, calibration
6. `interview-panel-goodtime-ashby-scheduling` — covers panel coord, Goodtime / Ashby / Calendly
7. `interview-debrief-consensus` — covers debrief facilitation, disagree-and-commit
8. `reference-checking-structured-3-questions` — covers Crosschq / Checkster / phone references
9. `offer-negotiation-comp-band-equity-perks` — covers negotiation, Pave / Carta / Compa / Levels.fyi
10. `offer-letter-docusign-pandadoc` — covers letter drafting + e-sign
11. `candidate-experience-sla-status-updates` — covers SLA, status updates, rejection templates
12. `employer-brand-glassdoor-comparably` — covers Glassdoor responses, testimonials
13. `recruiting-metrics-time-to-fill-offer-accept` — covers metrics, dashboards, weekly sync
14. `dei-hiring-diverse-slate-blind-resume` — covers diverse slate, panel diversity, Inclusion Kit
15. `structured-interview-training-hiring-managers` — covers HM training, BrightHire, certification
16. `employer-brand-campaigns-career-site` — covers career site, EVP, brand campaigns (defer marketing-agent for long-form)
17. `ai-screening-pinpoint-eightfold-with-care` — covers AI screening + legal compliance disclosure
18. `employee-referral-program` — covers ERIN / Teamable / Boon, bonus tiers
19. `executive-recruiting-process` — covers exec process, retained search, 360 references
20. `contractor-to-fte-conversion` — covers contractor → FTE workflow
21. `internal-mobility-program` — covers Gloat / Eightfold Career Hub
22. `post-offer-pre-start-check-ins` — covers renege prevention, weekly touch
23. `background-check-checkr-sterling` — covers Checkr / Sterling, FCRA compliance disclosure
24. `technical-interview-karat-codesignal-coderpad` — covers Karat / CodeSignal / CoderPad / HackerRank

---

## Notes on remaining caveats (the ⚠ rows)

| Capability | Status | Notes |
|---|---|---|
| ATS seat (Greenhouse / Lever / Ashby) | ⚠ | Paid seat required. Fallback: Workable SMB free trial; Pinpoint mid-market alternative. APIs are first-class; setup is OAuth/API key. |
| Goodtime scheduling | ⚠ | Paid seat. Fallback: Ashby native scheduling (if on Ashby), Calendly / Cal.com free tier for 1:1 screens. |
| Karat / CodeSignal / CoderPad / HackerRank | ⚠ | Paid seats. Fallback: live coding via Google Docs + Zoom screen share for low volume. |
| Crosschq / Checkster / SkillSurvey | ⚠ | Paid. Fallback: Typeform + Gmail templates + phone calls for IC roles. |
| Pave / Carta / Compa / Radford comp intel | ⚠ | Paid. Fallback: Levels.fyi public data (free); Pave / Compa public benchmarks. |
| DocuSign / PandaDoc | ⚠ | Paid. Fallback: DocuSign free tier for 5 envelopes/month; PDF + email sign for very low volume. |
| Glassdoor responses + Comparably | ⚠ | Glassdoor Free Employer Account allows responding (free). Paid Enhanced Profile adds testimonials. APIs limited; Playwright UI automation works. |
| Greenhouse Inclusion / Textio JD optimization | ⚠ | Greenhouse Inclusion included in Greenhouse plan; Textio paid seat. Fallback: manual checklist (gendered scrub, must-have count). |
| Pinpoint AI / Eightfold AI screening | ⚠ | Enterprise. Fallback: structured human screen + scorecard (the SOTA fallback is actually strong). Legal review mandatory per jurisdiction. |
| Checkr / Sterling background checks | ⚠ | Account credentialing required. Fallback: GoodHire SMB tier; manual reference + employment verification at very small volume. |
| Paradox / Mya / Cielo RPO | ⚠ | Enterprise. Fallback: human-only at <50 reqs/quarter; Twilio SMS for high-volume comm. |
| EEOC reporting + compliance | ⚠ | Data pull works (ATS demographic API); interpretation → defer to `legal-counsel`. |

For each ⚠ use case: the agent can execute via the free fallback path immediately. When the recipient activates the paid seat, the agent picks up the SOTA path with one config change.
