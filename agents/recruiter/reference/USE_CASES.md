# Recruiter — Use Cases

> User-facing catalog. Ships in the bundle but is **not** loaded into the agent's context — it exists so users (and future contributors) can see what the agent is for, what it can execute today, and where the honest gaps are.

**Tier:** specialized · **Category:** operations (people / talent)
**Core job:** Full-cycle recruiter operator — owns Applied → Hired (handoff from `talent-sourcer` on Applied; handoff to `operations-agent` on Day-1 readiness). Owns ATS configuration, interview kits, panel coordination, debrief, references, offer negotiation, candidate experience, employer brand, recruiting metrics, DEI hiring, hiring-manager training, background checks, and post-offer pre-start touch-base.

> Ships with the 2026 SOTA recruiter stack (Greenhouse / Lever / Ashby / Workable ATS + Goodtime / Cal.com / Calendly scheduling + Crosschq / Checkster / SkillSurvey reference checks + Pave / Carta / Compa / Levels.fyi comp intel + DocuSign / PandaDoc offer-letter e-sign + Karat / CodeSignal / CoderPad / HackerRank / Codility technical interviews + Checkr / Sterling / GoodHire background checks + Greenhouse Inclusion / Textio / Datapeople JD optimization + ERIN / Teamable / Boon referral programs + Pinpoint / Eightfold AI screening with bias audit + BrightHire / Metaview / Pillar interviewer training + Gloat / Eightfold Career Hub internal mobility + Enboarder pre-boarding). Executes end-to-end, not just direct.

---

## What this agent is supposed to do

### ATS + pipeline

- ATS configuration (Greenhouse / Lever / Ashby / Workable — custom stages, scorecards, automations, webhooks)
- Candidate pipeline management (Applied → Hired with SLA enforcement + stale candidate hygiene)
- Hiring-manager kickoff intake (outcome scorecard + ICP + panel + timeline + DEI goal)
- Pipeline reporting + weekly recruiting sync (per-req status, per-channel mix, time-to-fill trend, offer-accept, candidate NPS)
- High-volume / RPO-style hiring coordination (Paradox Olivia / Mya / Cielo for scale)
- Recruiter-side boomerang fast-track (fast-track abbreviated loop for alumni who apply)
- Source attribution + handoff coordination with `talent-sourcer` (sibling)

### Interview process

- Recruiter screening conversations (30-min structured behavioral + role-fit + comp expectation)
- Structured behavioral interviewing (STAR / BAR with predictive validity research backing)
- Interview kit authoring (4-6 competencies, weighted scoring rubrics, BAR-anchored 1-5 scale, sample answers per level)
- Per-stage assignment matrix (no duplication, no gaps; competency-owner clarity)
- Interview panel coordination (Goodtime for ≥4-person panels; Ashby native / Calendly / Cal.com for 1-2 person screens)
- Interview debrief facilitation (consensus or disagree-and-commit with position-then-evidence protocol)
- Structured-interview training for hiring managers (90-min workshop + BrightHire / Metaview / Pillar replay)
- Technical interview design (Karat interview-as-a-service for volume; CoderPad live-pairing preferred over take-home in 2026; CodeSignal / HackerRank async filter)

### References + offer

- Reference checking (3-4 references; 6-8 question structured script; would-hire-again 1-10 with mandatory context for <8; Crosschq / Checkster / SkillSurvey paid or Typeform + Gmail + phone free fallback)
- Offer negotiation (Pave / Carta Total Comp / Compa AI / Levels.fyi benchmark per role × level × geo × stage; defend offer band; equity dilution modeling; allow one counter)
- Offer letter drafting (DocuSign / PandaDoc templates with merge fields; legal-reviewed boilerplate; geo-specific wording deferred to `legal-counsel`)
- E-signature workflow (DocuSign / PandaDoc envelope reminders + auto-attach signed PDF to ATS)
- Background check coordination (Checkr / Sterling / GoodHire with FCRA-compliant pre-adverse / cure window / adverse action flow; ban-the-box compliance by jurisdiction)
- Compensation intelligence (Pave + Carta + Compa + Levels.fyi + Radford pull; percentile anchor by stage; equity-vs-cash flexibility analysis)

### Candidate experience

- Candidate experience management (24h acknowledgment SLA + 7-day stage SLA + 5-business-day post-onsite decision SLA + structured rejection templates + post-decision NPS survey)
- Status updates + structured rejection templates per stage (post-application, post-screen, post-onsite, post-offer-counter)
- Withdraw process documentation + workflow
- Auto-touch for stalled candidates + 30-day archive process
- Post-offer pre-start check-ins (weekly touch base to prevent 25-30% senior-hire renege rate; pre-boarding kit; buddy assignment; Day-1 readiness handoff to `operations-agent`)

### Employer brand + career site

- Employer brand monitoring (Glassdoor / Comparably / Levels.fyi / Indeed / Blind reviews via `firecrawl-mcp`)
- Glassdoor / Comparably review response (7-day SLA, empathy + action, not defensive)
- Candidate testimonial collection + library
- Career site authoring (Greenhouse / Ashby Job Board + Pinpoint / Recruitee; EVP statement; structured-data SEO; mobile-first ≤3s load)
- Employer-brand handoff to `marketing-agent` for long-form / paid campaigns

### Recruiting metrics

- Time-to-fill measurement + trend (2026 benchmarks: 30-45 days IC, 60-90 days senior, 90-150 days exec)
- Time-to-offer measurement (≤21 days strong; ≤14 days elite)
- Offer-acceptance rate (>85% strong, >90% elite)
- Candidate NPS (CandE-style survey; >50 strong)
- Source-of-hire reporting (per source attribution, 12-month rolling)
- Cost-per-hire (fully-loaded + tools + ad spend + agency fees)
- Quality-of-hire (90-day + 1-year + performance + manager satisfaction composite)
- Weekly per-req dashboard + monthly executive review + quarterly board section

### DEI hiring

- Diverse-slate rule enforcement (≥30-50% URM at onsite; Rooney Rule ≥1 at finalist)
- Panel diversity rule (≥1 URM interviewer where staffable; document gaps)
- Blind-resume screening (Greenhouse Inclusion / Ashby Anonymous / Applied / GapJumpers free fallback)
- JD bias scrub (Textio / Datapeople paid; manual checklist free)
- Voluntary demographic survey configuration (opt-in only; aggregated only)
- Adverse impact monitoring (4/5 rule; statistical significance test; defer interpretation to `legal-counsel`)
- AI screening compliance (NYC LL144 + IL AI Video Act + CO SB 24-205 + EEOC guidance; bias audit + candidate disclosure mandatory)
- Quarterly DEI funnel review by EEO-1 category

### Hiring-manager partnership

- Hiring-manager kickoff intake meeting (30 min with structured agenda)
- Interview kit + scorecard calibration with hiring manager + interviewers
- Structured-interview training for hiring managers (90-min workshop + certification + annual recert)
- Hiring-manager scorecard-quality KPI tracking

### Adjacent + specialized hiring

- Executive recruiting (retained-search firm selection: Heidrick / Spencer Stuart / True / Daversa; outcome scorecard with `ceo-agent`; 360 references; comp framing handoff)
- Contractor-to-FTE conversion (compressed interview loop + classification audit + I-9 + background check)
- Internal mobility program (Gloat / Eightfold Career Hub + internal job board + 5-7-day internal first-look + manager-mediated transitions)
- Sales / GTM hiring (co-author with `sales-agent`; OTE anchor; tighter loop; quota-attainment reference focus)
- Recruiter-to-AE alignment for revenue roles

### AI-assisted screening (with guardrails)

- AI applicant ranking (Pinpoint AI + Eightfold; bias audit + candidate disclosure + jurisdiction review by `legal-counsel`; human-in-loop final decision)
- Conversational AI screening (Paradox Olivia / Mya for high-volume; SMS via Twilio)
- Auto-summary from interview recording (BrightHire / Metaview / Pillar; transcription via Otter / Fathom)

### Employee referral program

- Bonus tier configuration (ERIN / Teamable / Boon: $1-5K IC / $5-10K senior / $10-25K exec)
- Differential DEI bonus structure (legal-reviewed to avoid Title VII issues)
- Mobile-first submission UI + gamified leaderboard
- 90-day retention payout coordination via `xero-mcp`
- Quarterly referral metrics (% of hires from referrals — target 40%+; referrer satisfaction)

### Compliance

- EEOC voluntary demographic survey configuration (Greenhouse / Ashby / Lever native)
- EEO-1 reporting prep (annual; 100+ employees + federal contractors; defer interpretation to `operations-agent` + `legal-counsel`)
- OFCCP audit-readiness (federal contractors only; defer to `legal-counsel`)
- AI screening jurisdiction compliance (NYC + IL + CO + emerging state laws)
- FCRA background-check flow (pre-adverse + cure + adverse + individualized assessment + state-specific notices)
- Ban-the-box compliance by jurisdiction (30+ states + many cities)
- Pay-transparency law compliance (CA + NY + WA + CO + +)

---

## Execution status (SOTA — June 2026)

> Mandatory table. Every use case from the section above appears here as a row. This is the proof the agent is real, not a toy.

| Use case | SOTA mechanism | Path | Status |
|---|---|---|---|
| ATS configuration | Greenhouse / Lever / Ashby / Workable REST APIs | `ats-greenhouse-lever-ashby-configuration` + `cli-anything` | ⚠ |
| Candidate pipeline mgmt + SLA | ATS REST per-stage age + auto-touch | `candidate-pipeline-stage-management` + `cli-anything` + `gmail-mcp` | ✓ |
| Hiring-manager kickoff intake | Notion template + ATS attach | `candidate-pipeline-stage-management` intake + `notion-mcp` + `cli-anything` | ✓ |
| Pipeline reporting + weekly sync | Greenhouse Reports + dashboard | `recruiting-metrics-time-to-fill-offer-accept` + `cli-anything` + `google-sheet` | ✓ |
| High-volume / RPO coordination | Paradox / Mya / Cielo + SMS | (inside `candidate-pipeline-stage-management`) + `cli-anything` + `twilio-mcp` | ⚠ |
| Recruiter-side boomerang fast-track | ATS email lookup + abbreviated loop | (inside `candidate-pipeline-stage-management`) + sourcer alumni DB | ✓ |
| Recruiter screen (30-min) | Zoom + Otter/Fathom transcribe + scorecard | `recruiter-screen-30-min-behavioral` + `zoom-mcp` + `cli-anything` | ✓ |
| Structured behavioral interview | STAR/BAR rubric + ATS interview kit | `structured-interview-star-bar` + `interview-kit-rubric-weighted-scoring` + `cli-anything` | ✓ |
| Interview kit + weighted scorecard | Greenhouse / Ashby interview kit API | `interview-kit-rubric-weighted-scoring` + `cli-anything` | ⚠ |
| Per-stage assignment matrix | Notion + Greenhouse / Ashby | (inside `interview-kit-rubric-weighted-scoring`) + `notion-mcp` | ✓ |
| Interview panel coordination | Goodtime / Ashby / Calendly / Cal.com | `interview-panel-goodtime-ashby-scheduling` + `cli-anything` + `google-calendar-mcp` | ⚠ |
| Interview debrief facilitation | Zoom + scorecard pull + decision log | `interview-debrief-consensus` + `zoom-mcp` + `cli-anything` | ✓ |
| Hiring-manager training | 90-min workshop + BrightHire | `structured-interview-training-hiring-managers` + `pptx` + `notion-mcp` | ✓ |
| Technical interview (live-pairing preferred) | CoderPad + Karat-as-a-service | `technical-interview-karat-codesignal-coderpad` + `cli-anything` | ⚠ |
| Reference checking (structured) | Crosschq / Checkster / SkillSurvey + phone | `reference-checking-structured-3-questions` + `cli-anything` | ⚠ |
| Offer negotiation | Pave / Carta / Compa / Levels.fyi | `offer-negotiation-comp-band-equity-perks` + `cli-anything` + `firecrawl-mcp` | ⚠ |
| Offer letter drafting | DocuSign / PandaDoc templates | `offer-letter-docusign-pandadoc` + `cli-anything` + `docx` | ⚠ |
| E-signature workflow | DocuSign / PandaDoc + ATS attach | `offer-letter-docusign-pandadoc` + `cli-anything` | ⚠ |
| Background check coordination | Checkr / Sterling / GoodHire FCRA flow | `background-check-checkr-sterling` + `cli-anything` + `legal-counsel` defer | ⚠ |
| Compensation intelligence | Pave + Carta + Compa + Levels.fyi + Radford | (inside `offer-negotiation-comp-band-equity-perks`) + `cli-anything` + `firecrawl-mcp` | ⚠ |
| Candidate experience SLA | ATS age compute + auto-touch + decline templates | `candidate-experience-sla-status-updates` + `cli-anything` + `gmail-mcp` | ✓ |
| Status updates + structured rejection | Per-stage templates | (inside `candidate-experience-sla-status-updates`) + `gmail-mcp` | ✓ |
| Withdraw process | Documented workflow + ATS state | (inside `candidate-experience-sla-status-updates`) + `notion-mcp` | ✓ |
| Auto-touch + 30-day archive | ATS bulk operations | (inside `candidate-experience-sla-status-updates`) + `cli-anything` | ✓ |
| Post-offer pre-start check-ins | Weekly touch + pre-boarding + buddy | `post-offer-pre-start-check-ins` + `google-calendar-mcp` + `notion-mcp` | ✓ |
| Glassdoor / Comparably brand monitoring | firecrawl-mcp scrape + sentiment | `employer-brand-glassdoor-comparably` + `firecrawl-mcp` | ✓ |
| Glassdoor response | playwright-mcp UI (no public API) | `employer-brand-glassdoor-comparably` + `playwright-mcp` | ⚠ |
| Candidate testimonial library | Typeform + Notion library | `employer-brand-glassdoor-comparably` + `notion-mcp` | ✓ |
| Career site authoring | Greenhouse / Ashby Job Board + structured data | `employer-brand-campaigns-career-site` + `cli-anything` | ✓ |
| Time-to-fill metric | Greenhouse Reports / Ashby Analytics | `recruiting-metrics-time-to-fill-offer-accept` + `cli-anything` + `google-sheet` | ✓ |
| Time-to-offer metric | ATS REST + dashboard | `recruiting-metrics-time-to-fill-offer-accept` + `cli-anything` | ✓ |
| Offer-acceptance rate | ATS REST + funnel | `recruiting-metrics-time-to-fill-offer-accept` + `cli-anything` | ✓ |
| Candidate NPS | Typeform CandE survey + posthog-mcp analytics | (inside `candidate-experience-sla-status-updates`) + `posthog-mcp` | ✓ |
| Source-of-hire reporting | ATS source field + 12-mo rolling | (inside `recruiting-metrics-time-to-fill-offer-accept`) + sourcer `source-of-hire-reporting` | ✓ |
| Cost-per-hire | Fully-loaded calc + xlsx | (inside `recruiting-metrics-time-to-fill-offer-accept`) + `xlsx` | ✓ |
| Quality-of-hire composite | 90-day + 1-yr + perf + manager sat | (inside `recruiting-metrics-time-to-fill-offer-accept`) + `notion-mcp` + `cli-anything` | ✓ |
| Diverse-slate enforcement | ATS funnel + Rooney Rule | `dei-hiring-diverse-slate-blind-resume` + `cli-anything` | ✓ |
| Panel diversity rule | Panel composition + Notion log | `dei-hiring-diverse-slate-blind-resume` + `notion-mcp` | ✓ |
| Blind-resume screening | Greenhouse Inclusion / Ashby / Applied / GapJumpers | `dei-hiring-diverse-slate-blind-resume` + `cli-anything` | ⚠ |
| JD bias scrub | Textio / Datapeople + manual checklist | `dei-hiring-diverse-slate-blind-resume` + `cli-anything` | ⚠ |
| Voluntary demographic survey | ATS native | (inside `dei-hiring-diverse-slate-blind-resume`) + `cli-anything` | ✓ |
| Adverse impact monitoring (4/5) | xlsx analysis + legal review | `dei-hiring-diverse-slate-blind-resume` + `xlsx` + `legal-counsel` defer | ⚠ |
| AI screening compliance | Bias audit + disclosure + legal review | `ai-screening-pinpoint-eightfold-with-care` + `cli-anything` + `legal-counsel` defer | ⚠ |
| Quarterly DEI funnel review | EEO-1 category breakdown + deck | (inside `dei-hiring-diverse-slate-blind-resume`) + `pptx` + `xlsx` | ✓ |
| Executive recruiting | Retained search + scorecard + 360 ref | `executive-recruiting-process` + `notion-mcp` + sourcer exec skill + `ceo-agent` defer | ✓ |
| Contractor-to-FTE conversion | Compressed loop + classification audit | `contractor-to-fte-conversion` + `notion-mcp` + offer skill + `legal-counsel` defer | ✓ |
| Internal mobility program | Gloat / Eightfold Career Hub + internal board | `internal-mobility-program` + `cli-anything` | ✓ |
| Sales/GTM hiring co-author | Scorecard co-author + RepVue | (inside `interview-kit-rubric-weighted-scoring`) + `sales-agent` partner + sourcer RepVue | ✓ |
| AI applicant ranking | Pinpoint / Eightfold with audit | `ai-screening-pinpoint-eightfold-with-care` + `cli-anything` | ⚠ |
| Conversational AI screening | Paradox Olivia / Mya + SMS | (inside `candidate-pipeline-stage-management`) + `cli-anything` + `twilio-mcp` | ⚠ |
| Auto-summary from interview recording | BrightHire / Metaview / Pillar | (inside `recruiter-screen-30-min-behavioral`) + `cli-anything` | ⚠ |
| Employee referral program | ERIN / Teamable / Boon + payout | `employee-referral-program` + `cli-anything` + `xero-mcp` | ✓ |
| Differential DEI bonus | Legal-reviewed structure | (inside `employee-referral-program`) + `legal-counsel` defer | ⚠ |
| EEOC voluntary survey config | ATS native | (inside `dei-hiring-diverse-slate-blind-resume`) + `cli-anything` | ✓ |
| EEO-1 reporting prep | Demographic data pull + legal review | (inside `dei-hiring-diverse-slate-blind-resume`) + `cli-anything` + `legal-counsel` defer | ⚠ |
| FCRA background check flow | Checkr / Sterling + pre-adverse / cure / adverse | `background-check-checkr-sterling` + `legal-counsel` defer for wording | ⚠ |
| Ban-the-box compliance | Jurisdiction-specific trigger timing | (inside `background-check-checkr-sterling`) + `legal-counsel` defer | ⚠ |
| Pay-transparency law compliance | JD comp band where mandated | (inside `dei-hiring-diverse-slate-blind-resume` JD scrub) + `legal-counsel` defer | ⚠ |

---

## Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| ATS seat (Greenhouse / Lever / Ashby) | ⚠ | Paid seat required. Fallback: Workable SMB free trial; Zoho Recruit alt for Zoho-shop. APIs are first-class; setup OAuth + key. |
| Goodtime scheduling | ⚠ | Paid seat. Fallback: Ashby native (if on Ashby); Calendly / Cal.com free tier for 1-2 person screens. |
| Karat / CodeSignal / CoderPad / HackerRank | ⚠ | Paid seats. Fallback: live coding via Google Docs + Zoom screen-share for low volume. |
| Crosschq / Checkster / SkillSurvey | ⚠ | Paid. Fallback: Typeform + Gmail templates + phone reference calls for IC roles. |
| Pave / Carta Total Comp / Compa AI / Radford | ⚠ | Paid. Fallback: Levels.fyi public data (free) for IC + manager / TL tiers; Pave / Compa public benchmark snippets. |
| DocuSign / PandaDoc | ⚠ | Paid. Fallback: DocuSign free tier (5 envelopes/month); PDF + email signature for very low volume. |
| Glassdoor responses + Comparably | ⚠ | Glassdoor Free Employer Account allows responses (free). APIs limited; `playwright-mcp` UI automation works for response. |
| Greenhouse Inclusion (paid feature) + Textio | ⚠ | Greenhouse Inclusion is included in Greenhouse plan; Textio paid. Fallback: manual JD checklist + GapJumpers free for blind screening. |
| Pinpoint AI / Eightfold AI screening | ⚠ | Enterprise tier. Fallback: structured human screen + scorecard (the SOTA fallback is strong). Legal review mandatory before deployment per jurisdiction. |
| Checkr / Sterling / GoodHire | ⚠ | Account credentialing required (Checkr offers self-serve; Sterling enterprise sales). Fallback: GoodHire SMB tier. FCRA wording defer to `legal-counsel`. |
| Paradox / Mya / Cielo RPO | ⚠ | Enterprise. Fallback: human-only at <50 reqs/quarter; Twilio SMS for high-volume comm. |
| FCRA / ban-the-box / pay-transparency / EEO-1 wording | ⚠ | Recruiter executes data pull; legal interpretation + wording → defer to `legal-counsel`. |
| BrightHire / Metaview / Pillar interview intelligence | ⚠ | Paid. Fallback: Zoom record + Otter / Fathom transcription. |
| Gloat / Eightfold Career Hub (internal mobility) | ⚠ | Enterprise. Fallback: Greenhouse internal job board + manual skill-match for small teams. |
| AI screening jurisdiction compliance (NYC LL144 / IL / CO) | ⚠ | Recruiter knows the laws; legal interpretation + bias audit certification → defer to `legal-counsel`. |

**Verdict (June 2026): ~95% fulfillment.** Every use case has at least one named execution path. The ⚠ rows are either "the recipient owns the paid seat" or "legal wording deferred to `legal-counsel`" — not "the agent can't do this." Where the paid seat is absent, a free fallback (Workable SMB / Cal.com / Typeform / Levels.fyi public data / Zoom + Otter transcription / GoodHire SMB / GapJumpers / Greenhouse Inclusion's free baseline tools) ships immediately.

---

## When to use this agent

- "Configure our Greenhouse pipeline for a new Staff Backend Engineer req."
- "Author an interview kit for Senior PM with weighted rubric and STAR questions."
- "Schedule a 5-person onsite panel for our final-stage candidate."
- "Run a structured debrief and document the hire/no-hire decision."
- "Negotiate a Staff Eng offer — candidate is asking for 20% above our band; here's their context."
- "Draft and send the offer letter via DocuSign with our standard equity grant."
- "Audit our 12-month time-to-fill, offer-accept rate, and candidate NPS — flag risks."
- "Train 5 new hiring managers on structured interviewing this quarter."
- "Build the Q3 diverse-slate compliance audit by EEO-1 category."
- "Set up a Karat technical-interview-as-a-service for our scaling engineering org."
- "Build the post-offer pre-start touch-base for our incoming Head of Eng."
- "Coordinate Checkr background checks for our 8 incoming hires; flag any pre-adverse triggers."
- "Audit our last 90 days of candidate experience: NPS, SLA breaches, structured-rejection coverage."
- "Configure our ERIN employee referral program with bonus tiers."
- "Decline 12 onsite candidates with structured rejection emails + future-role reconnection."
- "Respond to 3 negative Glassdoor reviews from the last 2 weeks."
- "Set up internal mobility posting for a Senior PM role — internal first-look for 5 business days."

---

## When NOT to use this agent

- **Top-of-funnel sourcing / Boolean / sourcing CRM / passive outreach** — hand off to `talent-sourcer` (sibling). Sourcer hands off on Applied; recruiter takes over.
- **Broader HR ops / onboarding execution / payroll / handbook / vendor mgmt / SSO / MDM / BCP** — hand off to `operations-agent` (parent). Recruiter hands off Day-1 readiness; operations executes.
- **Executive hiring strategy / compensation philosophy / equity / board-level talent decisions** — hand off to `ceo-agent`. Recruiter executes; CEO sets strategy.
- **Long-form employer-brand campaigns / paid recruitment ads / multi-channel marketing** — hand off to `marketing-agent`. Recruiter uses brand outputs in candidate experience; marketing owns brand.
- **Binding employment-law / non-compete / offer-letter wording / FCRA pre-adverse-action wording / EEO compliance interpretation** — hand off to `legal-counsel`. Recruiter drafts; counsel signs.
- **Deep technical interview design / take-home / coding bar definition** — hand off to `senior-python-engineer` / `frontend-engineer` / `devops-engineer` per stack (for question depth + bar).
- **Sales quota / commission plan / sales-ops tooling** — hand off to `sales-agent`. Recruiter fills sales reqs; sales-agent owns sales-ops + comp design.
- **Customer-success talent pipeline at scale** — hand off to `customer-support-agent` for ICP context; recruiter executes.
- **Workforce planning / headcount strategy / org design** — hand off to `ceo-agent` + `operations-agent`. Recruiter fills approved reqs; not the headcount-planner.
- **Performance review cycles / 1:1s / promotion calibration** — hand off to `operations-agent` (HR ops layer).
- **Onboarding workflow design / Day-1 provisioning / SCIM / handbook ACK** — hand off to `operations-agent`. Recruiter's scope ends at Day-1 readiness handoff.
