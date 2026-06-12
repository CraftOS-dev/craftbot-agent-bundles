# Recruiter — Role Content (appended to AGENT.md)

This content is appended to the recipient's `AGENT.md` after import. It is **not** in the agent's default turn-by-turn context — the agent reads `soul.md` every turn and **greps** `AGENT.md` for deep references when stuck.

Use **searchable H2/H3 headings** the agent will literally grep for: "Interview kit library", "STAR question bank", "Scorecard rubric library", "Offer letter template", "Decline template library", "DEI compliance audit", "FCRA flow runbook", "Background check package matrix", "Comp benchmark workflow", "ATS API recipes", "Antipattern catalog", "SOTA tool reference (June 2026)".

---

## Header note

This file appends to `AGENT.md` and is **not** loaded into the agent's default context. Grep when stuck. Searchable headings include: "Interview kit library", "STAR question bank by role family", "Scorecard rubric library", "Hiring manager intake template", "Recruiter screen template", "Debrief facilitation script", "Reference check structured questions", "Offer letter template per geo", "Decline template per stage", "Candidate-experience SLA matrix", "Glassdoor response patterns", "Recruiting metrics formulas", "DEI compliance audit checklist", "Greenhouse Inclusion configuration", "FCRA flow runbook", "Background check package matrix", "Comp benchmark workflow", "Pave / Carta / Compa pull recipe", "ATS API recipes (Greenhouse / Ashby / Lever / Workable)", "Goodtime scheduling playbook", "Technical interview platform comparison", "Karat / CodeSignal / CoderPad / HackerRank API recipes", "Executive recruiting process", "Post-offer pre-start checklist", "Antipattern catalog", "SOTA tool reference (June 2026)".

---

## Capability reference

> Factual lists banished from soul.md. Tagged with subsection headings the agent will grep for.

### ATS landscape by stage

- **Workable** — SMB tier (≤100 employees); inexpensive; native scheduling; light API.
- **Greenhouse** — Series B+ scaleups; G2 Winter 2026 ATS leader; Harvest API (100+ pre-built integrations); Inclusion anti-bias toolkit; mature scorecards + interview kits.
- **Ashby** — Series A-B scaleups; API-first; native analytics depth; `includeCompensation=true` on jobs API; native scheduling included.
- **Lever** — Series B+ tier; CRM-first pipeline (overlap with sourcing CRM); Lever Hooks webhooks.
- **Workday Recruiting** — Enterprise (5,000+ employees); integrates with Workday HCM; complex configuration; high TCO.
- **iCIMS** — Enterprise; high-volume hiring; SAP/Oracle integrations; verbose UI.
- **Recruitee** — SMB-mid; Pinpoint competitor; modern UI; integrated career sites.
- **Pinpoint** — SMB-mid; AI-native applicant ranking; integrated career sites; modern API.
- **Manatal** — Agency-focused; recruiter-CRM blended; lower-cost market.
- **Jobvite** (with RolePoint referrals merged) — Mid-market; referral-first positioning.
- **SmartRecruiters** — Mid-market enterprise; AI-assisted screening; integrated.
- **Zoho Recruit** — Zoho-shop recipients; lower price; native Zoho One integration.

### Interview kit components

- **Competency model** — 4-6 competencies per role; e.g., for Senior Backend Engineer: system design, code quality, debugging, collaboration, technical leadership, values fit.
- **STAR questions per competency** — 2-3 questions; e.g., "Tell me about a time when you had to design a system that needed to scale 10×. What constraints did you face? What did you propose? What was the outcome?"
- **BAR rubric per question** — 1-5 behaviorally-anchored scale: 1 (failed — example: "couldn't articulate trade-offs"), 2 (below — "named one trade-off but didn't quantify"), 3 (met — "named 3+ trade-offs and chose primary axis"), 4 (exceeded — "named 3+ + counter-proposed alternative + quantified"), 5 (role-model — "drove the discussion + raised novel angle interviewer hadn't considered").
- **Per-stage assignment matrix** — which interviewer owns which competency; no duplication, no gaps.
- **Sample answers per BAR level** — calibration reference for new interviewers.
- **Calibration meeting cadence** — kickoff calibration before first interview; quarterly recalibration; post-hire retro on which kit predicted success.

### Recruiter screen 30-min agenda

- 5 min — rapport + intro + role context ("here's why we're hiring; here's the team")
- 10 min — role-fit (must-haves validation; STAR question per must-have)
- 5 min — motivation ("why now / why us / current state at present employer")
- 5 min — comp expectation ("we're at $X-$Y; what range works for you?")
- 5 min — Q&A + next steps + transparent process timeline

### Reference check structured 6-8 questions

1. "In what capacity did you work with [candidate]? Period? Reporting relationship?"
2. "What was [candidate]'s primary scope of responsibility?"
3. "What's the most significant project / outcome you saw them ship?"
4. "How would you describe their working style? Strongest collaborator behaviors?"
5. "What's a growth area where they were stretching? How did they respond to feedback?"
6. "On a 1-10 scale, would you hire them again? Context for any score below 8?"
7. "Is there anything I haven't asked that I should know to make a great hire?"
8. (Optional, for senior+) "How did they handle a [specific challenge — e.g., underperforming report, ambiguous priorities, executive disagreement]?"

### Recruiting metrics formulas

- **Time-to-fill** — req-open date → accepted-offer date. 2026 benchmarks: 30-45 days IC, 60-90 days senior, 90-150 days exec.
- **Time-to-offer** — first interview → offer extended. ≤21 days strong; ≤14 days elite.
- **Offer-acceptance rate** — accepted offers / total offers extended. >85% strong, >90% elite.
- **Candidate NPS** — (% promoter — % detractor) from CandE survey. >50 strong.
- **Source-of-hire** — % of hires by channel (12-month rolling).
- **Cost-per-hire** — total recruiting spend / hires (incl. recruiter salary fully-loaded + tools + ad spend + agency fees).
- **Quality-of-hire** — composite: 90-day stay + 1-year stay + performance rating + manager satisfaction.
- **Diverse-slate compliance** — % of reqs meeting diverse-slate rule at finalist stage.
- **Panel diversity** — % of panels meeting ≥1 underrepresented interviewer rule.
- **Adverse impact** — 4/5 rule: selection rate of minority group ≥ 80% of majority group selection rate; if violated, statistical significance test required (`legal-counsel` interpretation).

### Compensation intelligence sources

- **Pave** — Real-time crowdsourced from 8K+ companies; Total Comp; benchmarks updated monthly; paid seat per recruiter.
- **Carta Total Comp** — Cap-table-aware (knows your equity dilution context); benchmarks via Carta Total Comp module; paid.
- **Levels.fyi** — Public crowd-sourced; free tier covers IC + manager / TL tiers; Engineering Salary Reports quarterly; fallback when paid seat absent.
- **Radford** — Enterprise gold standard; expensive ($10K-50K+ annual); HR-business-partner level.
- **Compa AI** — Negotiation-focused; offer-letter talking points + counter-prep; Salesforce-style integration with ATS.
- **Glassdoor + Comparably** — Public crowd-sourced; lower confidence than Pave but free fallback for ranges.

### Background check packages by role tier

- **Standard (IC)** — SSN trace + county criminal (7-year lookback) + federal criminal + sex-offender registry. $25-45 / candidate. 1-3 day turnaround.
- **Enhanced (senior IC + manager)** — Standard + motor-vehicle (if driving / fleet role) + education verification + 1-2 employment verifications. $75-125 / candidate. 2-5 day.
- **Executive (VP+)** — Enhanced + federal civil + credit (if FCRA-permissible per state) + media search + reference deep-dive. $200-500 / candidate. 5-10 day.
- **International** — Sterling Global, Checkr International, or HireRight Global. $50-300 / candidate / country. 5-15 day per country. Documentation in local language often required.
- **Healthcare / Finance / Government** — Compliance-specific (HIPAA + OIG / NPDB for healthcare; FINRA + Form U4 for finance; Public Trust / Secret / Top Secret for government).

### Interview-as-a-service vs in-house (technical)

- **Karat** — Karat interviewers run your loops; 24h turnaround; bias-audited via independent third-party; standardized rubrics; ~$300-500 / interview; scales easily. Use when: high-volume hiring + bias-audit required.
- **In-house live-pairing on CoderPad** — Your engineers interview; CoderPad provides IDE + collaboration; calibration required. Use when: ≤10 reqs / quarter + team has capacity.
- **CodeSignal Industry Coding Framework** — Async assessment; standardized; ICF scoring; AI cheat detection (Cosmo). Use when: top-of-funnel filter at high volume.
- **HackerRank** — Broad library + ATS-integrated interview platform; mid-range pricing. Use when: budget-constrained + need variety.
- **Codility** — European-favored; strong anti-cheat focus. Use when: European candidate base.

### DEI hiring rules (US — defer jurisdiction to legal-counsel)

- **Diverse-slate rule (Rooney Rule)** — ≥1 underrepresented candidate at finalist stage; aspire to ≥30-50% at onsite stage by role family.
- **Panel diversity rule** — ≥1 underrepresented interviewer where staffable.
- **Blind-resume screening** — initial screen with name + photo + school masked; Greenhouse Inclusion + Ashby Anonymous + Applied + GapJumpers (free).
- **JD bias scrub** — Textio / Datapeople (paid) or manual checklist (free): gendered language, age-coded, demand-coded, ≤8 must-haves, comp band where allowed.
- **Voluntary demographic survey** — Greenhouse / Ashby / Lever native; opt-in; aggregated only; never tied to individual decisions.
- **Adverse impact monitoring** — 4/5 rule (selection rate ≥ 80% of majority); statistical significance if violated; defer interpretation to `legal-counsel`.
- **AI screening compliance** — NYC LL144 (eff Jul 2023): bias audit annually + candidate disclosure required; Illinois AI Video Interview Act (2020): consent required; Colorado SB 24-205 (eff Feb 2026): impact assessment required.

### Candidate-experience SLA matrix

| Touchpoint | SLA | Action |
|---|---|---|
| Apply acknowledgment | <24 h | Auto-acknowledgment email via ATS native or Gem campaign |
| Initial screen scheduled | <72 h post-apply | Recruiter outreach with 3+ time options |
| Post-screen decision | <5 business days | Advance with hiring-manager screen scheduling OR decline with structured template |
| Post-onsite decision | <5 business days | Offer extended OR structured decline with future-role reconnection |
| Offer acceptance window | 5-7 business days | Auto-reminder T+2, T+4 days |
| Pre-start touch-base | Weekly | Recruiter + HM rotation; pre-boarding kit at T-2 weeks |
| Post-decision NPS survey | <7 days post-decision | Talent Board CandE-style survey |
| Bulk archive | 30 days no response | Auto-archive with re-engage tag |

---

## Interview kit library — Senior Backend Engineer (Python / Go) — startup ICP

> Battle-tested kit. Adapt; don't copy blindly.

**Competencies:**
1. **System design** (HM owns + technical interviewer)
2. **Code quality + debugging** (peer engineer owns)
3. **Collaboration + technical leadership** (peer + skip-level owns)
4. **Values fit + motivation** (HM owns + recruiter screen)

**STAR questions — System design competency:**
- "Tell me about a system you designed that needed to handle 10× growth. What were the constraints? What did you propose? What was the outcome?"
- "Walk me through a system you've worked on where you needed to balance reliability vs feature velocity. How did you trade off? What did you ship?"
- "Tell me about a time you proposed a design that the team initially disagreed with. How did you make the case? What happened?"

**BAR rubric per question (1-5):**
- **1 (failed)**: Couldn't articulate trade-offs; named tools without rationale.
- **2 (below)**: Named one trade-off but didn't quantify; surface-level analysis.
- **3 (met)**: Named 3+ trade-offs; chose primary axis; quantified expected scale and bottleneck.
- **4 (exceeded)**: Met + counter-proposed alternative design + quantified expected cost/latency/reliability impact.
- **5 (role-model)**: Drove the discussion + raised novel angle interviewer hadn't considered + proactively flagged what they don't know.

**Per-stage assignment:**
- Recruiter screen: competency 4 (values + motivation + comp expectation)
- HM screen: competency 4 (deeper) + competency 1 light
- Technical interview (live-pairing 90 min): competencies 2 + 3 partial
- System design interview (60 min): competency 1 + competency 3 partial
- Onsite peer panel (3× 45 min): competencies 2 + 3 + cross-cut
- Skip-level: competency 3 + 4 (leadership signal)

---

## STAR question bank by role family

### Engineering — IC

- "Tell me about a time you owned a system that broke in production. What was the failure mode? What did you ship to prevent recurrence?"
- "Tell me about the technical decision you regret most. What did you learn?"
- "Tell me about a time you disagreed with a senior engineer's design. How did you raise it? Outcome?"

### Engineering — Management

- "Tell me about a time you had to coach an underperforming engineer. What was the approach? Outcome?"
- "Tell me about a difficult prioritization call you made between two important projects. How did you decide?"
- "Tell me about a time you delivered a hard message to your team. Method?"

### Product Management

- "Tell me about a product decision you made that you initially thought was right but was wrong. How did you course-correct?"
- "Tell me about a time you said no to a high-status stakeholder. Approach?"
- "Walk me through a product launch that exceeded expectations. What worked and what was luck?"

### Sales

- "Tell me about your biggest deal lost. What went wrong? What would you do differently?"
- "Tell me about a deal you turned around when prospects had gone cold."
- "Walk me through your highest-quota year. What systems did you build that drove it?"

### Customer Success

- "Tell me about a customer escalation that ended in expansion. How did you turn it?"
- "Tell me about a customer you lost to churn that you could've saved."
- "Tell me about a process you built that improved a key retention metric."

### Marketing

- "Tell me about a campaign you ran that exceeded your goals. What was the insight that drove it?"
- "Tell me about a launch that underperformed. What went wrong?"
- "Walk me through a budget reallocation decision you made mid-quarter."

---

## Recruiter screen template

```
Hi {first_name}, thanks for taking the time today!

[5 min — Rapport + role context]
- "Quick intro: I'm [name], recruiter at [company]. Today is structured: I want to share the role + company context, learn about your background, talk comp expectations, and answer your questions. Sound good?"
- Company 1-min pitch: stage, funding, product, current team size, what we're scaling toward.
- Role 1-min pitch: title, what they'd own, who they'd work with, why we're hiring now.

[10 min — Role fit]
- "Walk me through your last role: scope, team, biggest things you shipped."
- STAR question on critical must-have: "Tell me about a time when..."
- Cross-check the 1-3 disqualifiers via question phrasing (e.g., "what's the team size you thrive in?" for "must thrive in startup chaos").

[5 min — Motivation]
- "Why are you looking now?"
- "What attracted you to [company]?"
- "If you got an offer in 2 weeks, what would you need to feel great about saying yes?"

[5 min — Comp expectation]
- "Quick comp note: we're at $X-$Y base + Z% bonus + W equity grant. What range works for you?"
- Note: never anchor on their previous salary (banned in CA, NY, MA, WA, IL, +; harmful to pay equity).
- Capture: their range, their flex, equity-vs-cash preference, any non-monetary asks.

[5 min — Q&A + next steps]
- "What can I answer for you?"
- Transparent timeline: "If we move forward, you'd have a HM screen with [name] within 7 days, then a 5-person panel within 14 days, with a decision within 5 business days of the onsite."
- Confirm: "I'll have a decision back to you within 5 business days. Sound good?"
```

**Post-call scorecard (submit within 24h):**
- Advance / Decline decision
- Comp range captured
- Strengths (2-3 bullets with behavioral evidence)
- Concerns (1-2 bullets with specific gap)
- 3-5 sentence summary for hiring manager (with their comp + motivation)
- Source attribution tagged

---

## Debrief facilitation script

```
Welcome. We're here to make a hire decision on [candidate] for [role]. 
Total time: 30-45 min. 

[Step 1 — Position-then-evidence, 10 min]
Each interviewer states yes/no FIRST + 2 specific behavioral evidence points. 
NO discussion until everyone has spoken. This avoids anchoring + groupthink.

[Step 2 — Open discussion, 15 min]
- Surface where positions converge + diverge
- For divergence: ask each side for the strongest counter-argument to their position
- Reference the kit's BAR rubric for calibration — was scoring consistent?

[Step 3 — Decision, 10 min]
Default decision rules:
- Unanimous yes → hire-bar met
- Hire-bar = competency owner strong yes + no veto → hire-bar met
- Veto from one interviewer → hold for stronger evidence OR no-hire
- Tie / hold → propose specific evidence we'd need (deeper reference + working session)

If disagree-and-commit:
- The dissenting interviewer logs their position + reasoning
- The team commits and proceeds; revisit at 30-day check-in if hired
```

**Post-debrief output:**
- Decision logged in ATS via `cli-anything` Greenhouse `/v1/applications/{id}/move?stage=offer` or Ashby
- Debrief notes attached
- Next-step communication drafted (offer extension OR decline template)

---

## Offer letter template per geo (sample — US FTE)

```
[Company Letterhead]
Date: {date}

Dear {candidate_name},

We are pleased to offer you the position of {title} at {company} ({legal_entity}) reporting to {manager_name}, with a start date of {start_date}. This is a {full-time | part-time} {exempt | non-exempt} position at our {office_location | remote} location.

Compensation:
- Base salary: ${base_salary} per year, paid bi-weekly per company schedule.
- Performance bonus: Up to {bonus_pct}% of base, paid annually subject to plan terms and individual + company performance.
- Equity: We will recommend to our Board of Directors a grant of {equity_amount} {ISO | NSO | RSU}, vesting over {vesting_schedule_years} years with a {cliff_period} cliff, per our standard equity plan. Final grant terms subject to Board approval.

Benefits: You will be eligible for our standard benefits package (health, dental, vision, 401(k), PTO, etc.) effective {benefits_start_date}. Details in attached Employee Benefits Summary.

Employment: This offer is for at-will employment, meaning either you or {company} may terminate the employment relationship at any time, with or without cause or notice, subject to applicable law.

Contingencies: This offer is contingent upon (1) satisfactory completion of a background check, (2) signed Confidentiality / IP Assignment Agreement (attached), and (3) verification of your authorization to work in the United States via Form I-9 within 3 business days of your start date.

Offer expiration: This offer is valid until 5:00 PM Pacific Time on {expiration_date}. Please respond by signing and returning this letter via DocuSign by that time.

We are excited about the prospect of you joining our team.

Sincerely,
{recruiter_name}
{title}, {company}

[Required acknowledgment]
[ ] I accept the offer of employment.
Signature: ______________________
Date: ______________________
```

**IMPORTANT — defer binding wording to `legal-counsel`:**
- At-will language (state-specific exceptions: Montana not at-will, NY public-sector restrictions, etc.)
- Non-compete (banned in CA, OK, ND, MN; enforceable elsewhere with specific drafting)
- IP assignment (CA Labor Code §2870 carve-out required)
- Background check contingency wording (FCRA disclosure must be standalone document)
- I-9 timing (3-business-day rule strict)
- Mandatory arbitration clause (state-by-state; CA AB 51, NY UJC §7515, increasingly restricted)
- Equity grant final terms (Board approval clause)

---

## Decline template library — per stage

### Post-application (no screen)

```
Hi {first_name},

Thank you for applying to the {role} role at {company} — we appreciate the time you spent on your application.

After review, we've decided to move forward with other candidates whose backgrounds align more closely with what we need for this specific role.

We'll keep your information on file and will reach out if a better-fit role opens up. We'd also encourage you to subscribe to our talent community at {careers_url} for future opportunities.

All the best in your search,
{recruiter_first_name}
```

### Post-recruiter screen

```
Hi {first_name},

Thank you for taking the time to chat with me about the {role} role at {company}.

After thinking it through, we've decided not to move forward at this stage. {Specific positive note — e.g., "Your background in distributed systems is strong, but we're looking for someone with deeper Python/asyncio experience for this specific role"}.

I really enjoyed our conversation and want to be specific: I'd love to reconnect if {adjacent_role | growth_path | future_state} comes up. Please stay in touch on LinkedIn.

All the best,
{recruiter_first_name}
```

### Post-onsite

```
Hi {first_name},

Thank you for spending so much time with our team this past week — the panel really enjoyed meeting you.

After our debrief, we've decided to move forward with another candidate for this specific {role} position. {Specific feedback — e.g., "The team thought your system design depth was strong, but we wanted more hands-on Python production experience for this role"}.

This was a competitive process, and I want to be honest about what we saw and what we didn't. The team was specifically impressed with {1-2 specific positives}.

If you're open, I'd love to keep in touch — we expect to be hiring at {your_appropriate_level | adjacent_role} in {timeframe}. May I reach out then?

All the best,
{recruiter_first_name}
```

### Post-offer counter-offer / decline

```
Hi {first_name},

Thanks for letting me know. I completely understand — these decisions are hard, and the counter from {current_employer | other_offer} reflects what we already see in you.

We'd love to reconnect in 12-18 months when you're ready to move. I'll set a calendar reminder for {future_date} and reach out then.

Wishing you the best in this next chapter,
{recruiter_first_name}
```

---

## ATS API recipes

### Greenhouse Harvest API

```bash
# Pull active candidates per req
curl -X GET "https://harvest.greenhouse.io/v1/candidates?status=active&job_id={job_id}" \
  -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: {user_id}"

# Submit scorecard
curl -X POST "https://harvest.greenhouse.io/v1/applications/{app_id}/scorecards" \
  -u "$GREENHOUSE_API_KEY:" \
  -H "Content-Type: application/json" \
  -H "On-Behalf-Of: {user_id}" \
  -d '{
    "interview_step_id": {step_id},
    "submitted_by": {user_id},
    "interview": "Senior Backend Engineer — Onsite Loop",
    "overall_recommendation": "yes",
    "ratings": [...]
  }'

# Move candidate to next stage
curl -X PATCH "https://harvest.greenhouse.io/v1/applications/{app_id}" \
  -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: {user_id}" \
  -d '{"job_post_id": {job_post_id}, "status": "active"}'

# Send rejection email
curl -X POST "https://harvest.greenhouse.io/v1/applications/{app_id}/reject" \
  -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: {user_id}" \
  -d '{"rejection_reason_id": {reason_id}, "rejection_email": {"send_email_at": "now", "email_template_id": {template_id}}}'

# Attach signed offer letter
curl -X POST "https://harvest.greenhouse.io/v1/candidates/{candidate_id}/attachments" \
  -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: {user_id}" \
  -F "filename=offer_letter_signed.pdf" \
  -F "type=offer_letter" \
  -F "content=@./offer_letter_signed.pdf"
```

### Ashby API

```bash
# Submit feedback
curl -X POST "https://api.ashbyhq.com/feedback.submit" \
  -u "$ASHBY_API_KEY:" \
  -H "Content-Type: application/json" \
  -d '{
    "applicationId": "{app_id}",
    "feedbackFormId": "{form_id}",
    "ratings": [...],
    "summary": "Strong system-design depth; concerns on team lead experience.",
    "overallRating": "advance"
  }'

# Move candidate to next stage  
curl -X POST "https://api.ashbyhq.com/application.changeStage" \
  -u "$ASHBY_API_KEY:" \
  -d '{"applicationId": "{app_id}", "interviewStageId": "{stage_id}"}'

# Reject candidate with template
curl -X POST "https://api.ashbyhq.com/application.archive" \
  -u "$ASHBY_API_KEY:" \
  -d '{"applicationId": "{app_id}", "archiveReasonId": "{reason_id}", "sendEmail": true, "emailTemplateId": "{template_id}"}'
```

### Lever API

```bash
# List opportunities by stage
curl -X GET "https://api.lever.co/v1/opportunities?stage_id={stage_id}&limit=100" \
  -u "$LEVER_API_KEY:"

# Submit feedback
curl -X POST "https://api.lever.co/v1/opportunities/{opp_id}/feedback?perform_as={user_id}" \
  -u "$LEVER_API_KEY:" \
  -H "Content-Type: application/json" \
  -d '{"feedbackTemplate": "{template_id}", "scores": [...], "note": "..."}'

# Archive (decline) opportunity
curl -X POST "https://api.lever.co/v1/opportunities/{opp_id}/archived?perform_as={user_id}" \
  -u "$LEVER_API_KEY:" \
  -H "Content-Type: application/json" \
  -d '{"reason": "{reason_id}"}'
```

---

## Goodtime scheduling playbook

```bash
# Pull interviewer availability + auto-match panel
curl -X POST "https://api.goodtime.io/v1/interviews/schedule" \
  -H "X-API-Key: $GOODTIME_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": "{candidate_id}",
    "interview_template_id": "{template_id}",
    "candidate_availability_window": ["2026-06-15", "2026-06-22"],
    "constraints": {
      "max_interviews_per_interviewer_per_week": 5,
      "min_buffer_minutes": 15,
      "require_diversity": true,
      "no_back_to_back_for_interviewer": true
    }
  }'
```

**Goodtime decision rule:** Use when ≥4-person panel + ≥2-day candidate availability window. Cal.com / Calendly for 1-2 person screens.

---

## Karat / CodeSignal / CoderPad / HackerRank — platform decision matrix

| Modality | Karat | CodeSignal | CoderPad | HackerRank | In-house |
|---|---|---|---|---|---|
| Cost / interview | $300-500 | Variable | $30-90 / pad | Mid | Internal salary cost |
| Bias audit | Yes (third-party) | Internal | Internal | Internal | Depends on calibration |
| Live pairing | Yes | No (async) | Yes (gold standard) | Yes | Yes |
| Anti-cheat | Yes (interviewer + audit) | Cosmo AI | Drawing Mode + IDE fingerprint | Plagiarism + proctor | Visual + Zoom share |
| Scale | Best at >50 interviews / mo | Top of funnel async | Live up to 20 / mo | Mid volume | <10 / mo |
| Use case | High volume + scaling | Async filter | Live high-quality | Variety + budget | Small team + control |

```bash
# CoderPad live-pairing pad creation
curl -X POST "https://coderpad.io/api/v1/pads" \
  -H "Authorization: Bearer $CODERPAD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Backend Engineer — Live Pairing",
    "language": "python",
    "examples": ["url_shortener", "lru_cache"],
    "interviewer_email": "interviewer@company.com",
    "candidate_email": "candidate@example.com"
  }'

# CodeSignal assessment send
curl -X POST "https://api.codesignal.com/v1/recruiter/assessments" \
  -H "X-API-Key: $CODESIGNAL_API_KEY" \
  -d '{
    "test_id": "{icf_test_id}",
    "candidate_email": "candidate@example.com",
    "expire_at": "2026-06-20T00:00:00Z"
  }'
```

---

## Comp benchmark workflow

```bash
# Pave benchmark pull
curl -X GET "https://api.pave.com/v1/comp/benchmark?role=engineer&level=staff&geo=san_francisco&company_size=200-500&data_type=total_comp" \
  -H "Authorization: Bearer $PAVE_API_KEY"

# Output: 25/50/75 percentile for base + bonus + equity + total

# Carta Total Comp (paid)
curl -X POST "https://api.carta.com/v1/companies/{company_id}/comp_benchmarks" \
  -H "Authorization: Bearer $CARTA_API_KEY" \
  -d '{"role_family": "engineering", "level": "staff", "geo": "us_remote"}'

# Levels.fyi free public scrape (firecrawl path)
firecrawl crawl "https://www.levels.fyi/?compare=Stripe,Brex&track=Software%20Engineer" \
  --extract-schema "title,base,equity,bonus,location"
```

**Decision rule for percentile anchor:**
- Stage A (seed / pre-Series A): 25-50th percentile + larger equity grant
- Stage B (Series A-B): 40-65th percentile + meaningful equity
- Stage C (Series C+): 50-75th percentile + smaller equity
- Stage D (late / public): 60-90th percentile + smallest equity
- Competitive / counter-offer scenarios: +10 percentile points + signing bonus

---

## FCRA flow runbook

```
1. PRE-CHECK
   - Candidate signs FCRA Disclosure + Authorization (standalone document, NOT in offer letter)
   - California-specific: Additional disclosure for ICRAA + CFCRA
   - Other state-specific: NYC FCA, MA, IL, NJ specific notices

2. ORDER CHECK
   - Send via Checkr `/v1/invitations` OR Sterling `/v2/screenings`
   - Webhook on `/v1/reports/{id}/complete`
   - Expected turnaround: 2-5 business days standard

3. REVIEW REPORT
   - All clear → notify hiring manager + advance to onboarding
   - Adverse finding flagged → proceed to PRE-ADVERSE ACTION

4. PRE-ADVERSE ACTION (defer wording to legal-counsel)
   - Send pre-adverse action letter via email + certified mail
   - Include copy of background report + FCRA Summary of Rights
   - CFR Title 12, Section 1022, Appendix M
   - 5-business-day cure window (some states: 10 business days)

5. INDIVIDUALIZED ASSESSMENT
   - EEOC-required: nature + gravity of offense, time since, nature of role
   - California ICRAA: written individualized assessment required
   - NYC FCA: Article 23-A factors required
   - Document assessment in ATS

6. ADVERSE ACTION (only if proceeding with rescission — defer wording to legal-counsel)
   - Send adverse action letter via email + certified mail
   - Include FCRA Summary of Rights (post-adverse version) + dispute procedure
   - NYC FCA: must explain Article 23-A factors weighed

7. RECORD-KEEPING
   - Retain FCRA disclosure + authorization for at least 5 years (state-dependent)
   - Retain background check report per state retention requirements
   - Document compliance with all state-specific notices
```

---

## DEI compliance audit checklist (quarterly)

```
[ ] Diverse-slate compliance: % of reqs meeting Rooney Rule (≥1 underrepresented at finalist)
[ ] Onsite diverse representation: ≥30-50% target per role family
[ ] Panel diversity rule: ≥1 underrepresented interviewer per panel where staffable; document gaps
[ ] JD bias scrub: every JD passes Textio/Datapeople OR manual checklist (gendered, age-coded, demand-coded, ≤8 must-haves)
[ ] Voluntary demographic survey enabled in ATS; opt-in only
[ ] Blind-resume screening at initial: Greenhouse Inclusion / Ashby Anonymous / Applied / GapJumpers
[ ] Adverse impact 4/5 rule check by EEO-1 category per role family; flag violations
[ ] AI screening tools have bias audit + candidate disclosure (NYC LL144, IL, CO)
[ ] Diverse-channel sourcing tracked: % from /dev/color, Code2040, Black Founders, Lesbians Who Tech, etc.
[ ] Hiring-manager training completion: structured interview + bias awareness (IAT) ≥ 95% of HMs in last 12 mo
[ ] Quarterly funnel report by EEO-1 category sent to leadership
[ ] Action plan for any flagged inequity (with legal-counsel review)
```

---

## Antipattern catalog

### Antipattern 1: Unstructured interview

**BAD:**
"Tell me about yourself" → "What questions do you have for us?" → "Thanks, we'll be in touch."

**Why it's bad:** Predictive validity r=0.20 (Schmidt & Hunter). Trains for gut-feel hiring + halo / horns bias. Cannot produce defensible decision.

**GOOD:**
Calibrated interview kit + STAR questions per competency + BAR rubric per question + scorecard in ATS within 24h.

**Why it's better:** Predictive validity r=0.51 (2.5× lift). Behavioral evidence forces specific examples. Scorecard creates audit trail.

### Antipattern 2: Silent rejection

**BAD:**
Apply → 3 weeks of silence → candidate moves on.

**Why it's bad:** Candidate experience destroyed; Glassdoor risk; competitor wins.

**GOOD:**
24h apply acknowledgment + structured rejection within 5 business days with specific feedback + future-role reconnection.

**Why it's better:** Maintains brand; preserves option to re-engage; 30% reduction in negative Glassdoor reviews observed.

### Antipattern 3: Anchor offer on last salary

**BAD:**
"You're at $140K. We'll offer $155K."

**Why it's bad:** Banned in CA, NY, MA, WA, IL, +. Perpetuates pay inequity (gender + race gap embeds across moves). Lower offer-accept rate.

**GOOD:**
Pave / Carta / Compa / Levels.fyi benchmark per role × level × geo × stage; anchor at appropriate percentile for stage + competitiveness.

**Why it's better:** Legal compliance. Pay equity. Defensible offer band. Higher offer-accept rate.

### Antipattern 4: All-male, all-Stanford panel

**BAD:**
"Best 5 engineers we have happen to all be [demographic / school cohort]."

**Why it's bad:** Reproduces homogeneity. Signal to underrepresented candidates. Misses perspective gaps.

**GOOD:**
Panel diversity rule: ≥1 underrepresented interviewer + ≥1 non-direct-report perspective where staffable. Document gap when unstaffable.

**Why it's better:** Better hiring decisions (perspective variance reduces blind spots); better candidate experience; brand signal.

### Antipattern 5: Take-home assessment in 2026

**BAD:**
"Build a URL shortener over the weekend; submit by Monday."

**Why it's bad:** AI cheat risk (Claude, GPT, Cursor make assessment unreliable); candidate-hostile (unpaid work); selects against caregivers + busy candidates.

**GOOD:**
Live-pairing on CoderPad ≤90 min OR Karat interview-as-a-service for high volume.

**Why it's better:** Real-time skill signal + collaboration signal + bias-controlled timing + AI-mitigated.

### Antipattern 6: Skipping background check or triggering at wrong time

**BAD:**
"Let's start them next Monday — background check is just a formality."

**Why it's bad:** FCRA non-compliance + ban-the-box violations + adverse-action timing issues + no individualized assessment.

**GOOD:**
Background check after offer accepted (ban-the-box compliant) + FCRA disclosure standalone + 5-business-day cure window + legal-counsel-approved adverse action wording.

**Why it's better:** Compliance. Defensible. Candidate dignity preserved.

### Antipattern 7: No post-offer touch base

**BAD:**
Offer accepted T-30 days → silence until Day 1.

**Why it's bad:** 25-30% senior-hire renege rate (counter-offer; competing offer; cold feet).

**GOOD:**
Weekly touch from accept to Day-1 + pre-boarding kit + buddy assigned + first-day calendar built T-1 week.

**Why it's better:** Renege rate drops to 5-10%. Candidate ramps faster.

---

## SOTA tool reference (June 2026)

> Generated from `reference/SOTA_USE_CASES.md`. One H3 per tool, grep-friendly. Each section points to its bundled skill pack + brief usage note. Skill-pack folders are created in Round 2 (runtime build).

### Greenhouse (ATS)

**Use for:** Series B+ scaleups; G2 Winter 2026 ATS leader; integrated Inclusion anti-bias toolkit; 100+ pre-built integrations.
**Skill pack:** [`ats-greenhouse-lever-ashby-configuration`](skills/ats-greenhouse-lever-ashby-configuration/SKILL.md)
**API surface:** Harvest API (https://developers.greenhouse.io/harvest.html); Job Board API (public read); Interview Kits API; Reports API.
**Quick recipe:**
```bash
curl -X POST "https://harvest.greenhouse.io/v1/candidates" \
  -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: {user_id}" \
  -d '{"first_name":"Jane","last_name":"Doe","email_addresses":[{"value":"jane@example.com","type":"personal"}],"applications":[{"job_id":{job_id}}]}'
```
**Source:** https://developers.greenhouse.io/harvest.html

### Ashby (ATS)

**Use for:** Series A-B scaleups; API-first; native analytics + native scheduling; `includeCompensation=true` on jobs API.
**Skill pack:** [`ats-greenhouse-lever-ashby-configuration`](skills/ats-greenhouse-lever-ashby-configuration/SKILL.md)
**API surface:** https://developers.ashbyhq.com/reference; native interview scheduler + feedback forms.
**Quick recipe:**
```bash
curl -X POST "https://api.ashbyhq.com/candidate.create" \
  -u "$ASHBY_API_KEY:" \
  -d '{"name":"Jane Doe","email":"jane@example.com","applicationHistory":[{"jobId":"{job_id}","stageId":"{stage_id}"}]}'
```
**Source:** https://developers.ashbyhq.com/reference

### Lever (ATS)

**Use for:** Series B+ with CRM-first pipeline; Lever Hooks webhooks; CRM + ATS in one.
**Skill pack:** [`ats-greenhouse-lever-ashby-configuration`](skills/ats-greenhouse-lever-ashby-configuration/SKILL.md)
**API surface:** https://hire.lever.co/developer/documentation
**Source:** https://hire.lever.co/developer/documentation

### Workable (ATS)

**Use for:** SMB tier (≤100 employees); affordable; native scheduling; light API.
**Skill pack:** [`ats-greenhouse-lever-ashby-configuration`](skills/ats-greenhouse-lever-ashby-configuration/SKILL.md)
**API surface:** https://workable.readme.io/reference

### Goodtime (interview scheduling)

**Use for:** High-volume multi-person panels; auto-decline-and-reschedule; interviewer load balancing; DEI panel composition rules.
**Skill pack:** [`interview-panel-goodtime-ashby-scheduling`](skills/interview-panel-goodtime-ashby-scheduling/SKILL.md)
**API surface:** https://help.goodtime.io/en/articles/api-documentation
**Decision rule:** Use when ≥4-person panel + ≥2-day candidate availability window. Cal.com / Calendly for 1-2 person screens.

### Crosschq (reference checking)

**Use for:** 360 reference checks via digital survey distribution + scoring aggregation.
**Skill pack:** [`reference-checking-structured-3-questions`](skills/reference-checking-structured-3-questions/SKILL.md)
**API surface:** https://crosschq.com/api

### Pave (compensation intelligence)

**Use for:** Real-time crowdsourced Total Comp benchmarks from 8K+ companies; per-role-level-geo-stage.
**Skill pack:** [`offer-negotiation-comp-band-equity-perks`](skills/offer-negotiation-comp-band-equity-perks/SKILL.md)
**API surface:** https://www.pave.com/developers
**Decision rule:** Anchor offer band on Pave 50th percentile + adjust for stage + competitiveness.

### Carta Total Comp (compensation + equity modeling)

**Use for:** Cap-table-aware comp benchmarks; equity dilution scenario modeling.
**Skill pack:** [`offer-negotiation-comp-band-equity-perks`](skills/offer-negotiation-comp-band-equity-perks/SKILL.md)
**API surface:** https://docs.carta.com/

### Compa AI (offer-letter comp comm)

**Use for:** Real-time offer-letter comp communication + negotiation talking points.
**Skill pack:** [`offer-negotiation-comp-band-equity-perks`](skills/offer-negotiation-comp-band-equity-perks/SKILL.md)
**API surface:** https://www.compa.ai/

### Levels.fyi (free public comp data)

**Use for:** Free fallback when Pave / Carta / Compa not available; IC + manager / TL benchmarks; Engineering Salary Reports.
**Skill pack:** [`offer-negotiation-comp-band-equity-perks`](skills/offer-negotiation-comp-band-equity-perks/SKILL.md)
**Path:** `firecrawl-mcp` scrape; public data, no API key needed.
**Source:** https://www.levels.fyi/

### DocuSign (e-signature)

**Use for:** Offer-letter e-sign with template merge fields + auto-reminders + audit trail.
**Skill pack:** [`offer-letter-docusign-pandadoc`](skills/offer-letter-docusign-pandadoc/SKILL.md)
**API surface:** https://developers.docusign.com/docs/esign-rest-api/

### PandaDoc (alternative e-signature)

**Use for:** Offer-letter generation + e-sign alt to DocuSign; modern UI; better template flexibility.
**Skill pack:** [`offer-letter-docusign-pandadoc`](skills/offer-letter-docusign-pandadoc/SKILL.md)
**API surface:** https://developers.pandadoc.com/

### Checkr (background checks)

**Use for:** Founder-friendly API + 2-3 day turnaround + EEOC-compliant individualized assessment + FCRA workflow.
**Skill pack:** [`background-check-checkr-sterling`](skills/background-check-checkr-sterling/SKILL.md)
**API surface:** https://developers.checkr.com/

### Sterling (enterprise / international background)

**Use for:** Enterprise tier; global coverage via Sterling Global; healthcare / finance / government compliance.
**Skill pack:** [`background-check-checkr-sterling`](skills/background-check-checkr-sterling/SKILL.md)
**API surface:** https://www.sterlingcheck.com/api-documentation/

### Karat (interview-as-a-service)

**Use for:** Karat interviewers run your loops; 24h turnaround; bias-audited; standardized rubrics; high-volume scaling.
**Skill pack:** [`technical-interview-karat-codesignal-coderpad`](skills/technical-interview-karat-codesignal-coderpad/SKILL.md)
**API surface:** Partner API (recipient onboarded via Karat sales)

### CoderPad (live-pairing technical interview)

**Use for:** Live-pairing platform; IDE-quality + Drawing Mode anti-cheat; ATS integration with Greenhouse / Ashby / Lever.
**Skill pack:** [`technical-interview-karat-codesignal-coderpad`](skills/technical-interview-karat-codesignal-coderpad/SKILL.md)
**API surface:** https://coderpad.io/help/api/

### CodeSignal (async technical assessment)

**Use for:** Industry Coding Framework (ICF) standardized async assessment + Cosmo AI cheat detection.
**Skill pack:** [`technical-interview-karat-codesignal-coderpad`](skills/technical-interview-karat-codesignal-coderpad/SKILL.md)
**API surface:** https://docs.codesignal.com/recruiter

### HackerRank (broad technical library + recruiter platform)

**Use for:** Variety of question types + plagiarism detection + recruiter platform.
**Skill pack:** [`technical-interview-karat-codesignal-coderpad`](skills/technical-interview-karat-codesignal-coderpad/SKILL.md)
**API surface:** https://www.hackerrank.com/work/api

### BrightHire (interview intelligence)

**Use for:** Interview recording + auto-transcription + AI summary + hiring-manager training.
**Skill pack:** [`structured-interview-training-hiring-managers`](skills/structured-interview-training-hiring-managers/SKILL.md)
**API surface:** https://docs.brighthire.ai/

### Metaview (interview intelligence — alt)

**Use for:** Interview recording + auto-transcription + smart notes; competitive alt to BrightHire.
**Skill pack:** [`structured-interview-training-hiring-managers`](skills/structured-interview-training-hiring-managers/SKILL.md)

### Pillar (interview intelligence — live coaching)

**Use for:** Real-time interviewer coaching during the interview; live AI suggestions.
**Skill pack:** [`structured-interview-training-hiring-managers`](skills/structured-interview-training-hiring-managers/SKILL.md)

### Greenhouse Inclusion (anti-bias toolkit)

**Use for:** Built-in to Greenhouse; blind screening + structured calibration + demographic survey + bias-awareness training.
**Skill pack:** [`dei-hiring-diverse-slate-blind-resume`](skills/dei-hiring-diverse-slate-blind-resume/SKILL.md)
**Source:** https://www.greenhouse.io/inclusion

### Textio (JD optimization — paid)

**Use for:** Language-guidance engine for JD bias scrub; outcome-based predictions; female-applicant-rate lift.
**Skill pack:** [`dei-hiring-diverse-slate-blind-resume`](skills/dei-hiring-diverse-slate-blind-resume/SKILL.md)
**API surface:** https://textio.com/developers

### Datapeople (JD optimization — paid alt)

**Use for:** Template enforcement + readability + JD optimization; cheaper alt to Textio.
**Skill pack:** [`dei-hiring-diverse-slate-blind-resume`](skills/dei-hiring-diverse-slate-blind-resume/SKILL.md)

### Applied / GapJumpers (free blind-hiring fallback)

**Use for:** Blind resume screening when Greenhouse Inclusion not available.
**Skill pack:** [`dei-hiring-diverse-slate-blind-resume`](skills/dei-hiring-diverse-slate-blind-resume/SKILL.md)
**Source:** https://www.appliedhq.co/ + https://gapjumpers.me/

### Pinpoint AI (AI screening — bias-audited)

**Use for:** AI-assisted applicant ranking with bias audit + candidate disclosure compliance.
**Skill pack:** [`ai-screening-pinpoint-eightfold-with-care`](skills/ai-screening-pinpoint-eightfold-with-care/SKILL.md)
**API surface:** https://www.pinpointhq.com/developers

### Eightfold AI (talent intelligence)

**Use for:** AI talent intelligence + bias-aware matching + workforce intelligence + Career Hub for internal mobility.
**Skill pack:** [`ai-screening-pinpoint-eightfold-with-care`](skills/ai-screening-pinpoint-eightfold-with-care/SKILL.md) + [`internal-mobility-program`](skills/internal-mobility-program/SKILL.md)
**Source:** https://eightfold.ai/

### Paradox (Olivia — conversational AI for high-volume)

**Use for:** High-volume conversational AI for screening + scheduling at scale (Walmart, McDonald's level volume).
**Skill pack:** [`candidate-pipeline-stage-management`](skills/candidate-pipeline-stage-management/SKILL.md)
**Source:** https://www.paradox.ai/olivia

### Gloat (internal talent marketplace)

**Use for:** AI-powered internal mobility + skill-based matching + career pathing.
**Skill pack:** [`internal-mobility-program`](skills/internal-mobility-program/SKILL.md)
**Source:** https://gloat.com/

### ERIN (employee referral program)

**Use for:** Gamified referral submission + bonus tier management + 90-day retention payout tracking.
**Skill pack:** [`employee-referral-program`](skills/employee-referral-program/SKILL.md)
**Source:** https://erinapp.com/

### Glassdoor / Comparably (employer brand monitoring)

**Use for:** Review monitoring + response + EVP statement publication + employer brand badges.
**Skill pack:** [`employer-brand-glassdoor-comparably`](skills/employer-brand-glassdoor-comparably/SKILL.md)
**Path:** `firecrawl-mcp` scrape for monitoring + `playwright-mcp` UI for response.

### Retained search firms (executive — referenced, not API)

**Use for:** C-level + tech-VP retained search engagements (90-180 day).
**Skill pack:** [`executive-recruiting-process`](skills/executive-recruiting-process/SKILL.md)
**Firms:** Heidrick & Struggles, Spencer Stuart, Russell Reynolds, Egon Zehnder (C-level); True Search, Riviera Partners, Daversa Partners (tech VP + venture-backed).
**Handoff:** `ceo-agent` owns engagement decisions + comp framing + closing.

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| "configure ATS for new req" | `ats-greenhouse-lever-ashby-configuration` | Plus `candidate-pipeline-stage-management` for stages + SLA |
| "run recruiter screen" | `recruiter-screen-30-min-behavioral` | Plus `zoom-mcp` recording |
| "author interview kit" | `interview-kit-rubric-weighted-scoring` | Plus `structured-interview-star-bar` for question authoring |
| "schedule panel interview" | `interview-panel-goodtime-ashby-scheduling` | Goodtime for ≥4-person; Calendly for ≤2-person |
| "facilitate debrief" | `interview-debrief-consensus` | Pull scorecards before; surface dissent in discussion |
| "check references" | `reference-checking-structured-3-questions` | Crosschq paid; Typeform + Gmail + Zoom free fallback |
| "negotiate offer" | `offer-negotiation-comp-band-equity-perks` | Pave / Carta / Compa benchmark; defer binding to legal |
| "draft offer letter" | `offer-letter-docusign-pandadoc` | DocuSign / PandaDoc template; legal disclaimer footer |
| "decline candidate" | `candidate-experience-sla-status-updates` | Structured rejection by stage; future-reconnection where appropriate |
| "respond to Glassdoor review" | `employer-brand-glassdoor-comparably` | 7-day SLA; empathy + action; not defensive |
| "pull recruiting metrics" | `recruiting-metrics-time-to-fill-offer-accept` | Greenhouse Reports / Ashby Analytics; weekly + quarterly |
| "enforce diverse slate" | `dei-hiring-diverse-slate-blind-resume` | Greenhouse Inclusion + Textio + funnel audit |
| "train hiring managers" | `structured-interview-training-hiring-managers` | 90-min workshop + BrightHire / Metaview / Pillar replay |
| "build career site" | `employer-brand-campaigns-career-site` | Greenhouse / Ashby Job Board + structured-data SEO |
| "deploy AI screening" | `ai-screening-pinpoint-eightfold-with-care` | Bias audit + disclosure + legal review mandatory |
| "set up referral program" | `employee-referral-program` | ERIN / Teamable / Boon + bonus tier + retention payout |
| "fill an exec role" | `executive-recruiting-process` | Outcome scorecard + retained-search decision with `ceo-agent` |
| "convert contractor to FTE" | `contractor-to-fte-conversion` | Compressed loop + classification audit (legal review) |
| "post internal mobility role" | `internal-mobility-program` | Internal job board first; Gloat / Eightfold Career Hub for skill matching |
| "prevent post-offer renege" | `post-offer-pre-start-check-ins` | Weekly touch + pre-boarding + buddy + Day-1 handoff |
| "order background check" | `background-check-checkr-sterling` | Checkr / Sterling / GoodHire by tier; FCRA flow with legal |
| "design technical interview" | `technical-interview-karat-codesignal-coderpad` | Live-pairing > take-home in 2026 |
| "source candidates / Boolean" | **DEFER to `talent-sourcer`** | Top-of-funnel scope is sibling agent |
| "exec hiring strategy" | **DEFER to `ceo-agent`** | Recruiter executes; CEO sets strategy |
| "long-form brand campaign" | **DEFER to `marketing-agent`** | Recruiter uses brand outputs; marketing owns brand |
| "binding offer / non-compete / FCRA wording" | **DEFER to `legal-counsel`** | Recruiter drafts; counsel signs |
| "onboarding execution / SCIM / device" | **DEFER to `operations-agent`** | Recruiter hands off Day-1 ready; ops executes |

---

## Brief templates / Output templates

### Hiring-manager intake template

```markdown
# {Role Title} — Hiring Intake

## Outcome scorecard (12-month deliverables, NOT JD tasks)
1. ...
2. ...
3. ...

## ICP
- Must-have (3-5): ...
- Nice-to-have (3-5): ...
- Disqualifiers (1-3): ...

## Comp band
- Base: ${low}-${high}
- Bonus: {pct}% target
- Equity: {grant_size} {ISO/RSU} over {vesting}
- Geo / remote / hybrid: ...

## Panel composition + interviewer assignment matrix
- Recruiter screen: {recruiter}, owns competency: motivation + comp expectation
- HM screen: {HM}, owns competencies: ...
- Technical loop (live-pairing): {interviewer_1}, {interviewer_2}, owns competencies: ...
- Onsite panel:
  - {interviewer_3}, owns competency: ...
  - {interviewer_4}, owns competency: ...
  - {interviewer_5}, owns competency: ...
- Skip-level: {skip_level}, owns competency: ...

## Timeline
- Target close date: {date}
- Urgency context: ...
- Why now: ...

## DEI goal
- Diverse-slate target: {N}% URM at onsite stage
- Panel diversity rule applied: ≥1 URM interviewer
- Channels via sourcer: ...

## Market context
- Top 3 competitors for this candidate: ...
- Comp + brand positioning: ...

## Sign-off
- Hiring manager: ________ Date: ________
- Recruiter: ________ Date: ________
- Hiring leader (if needed): ________ Date: ________
```

---

## Closing rules

Configure the ATS. Author the kit with weighted rubric. Calibrate before the loop runs. Schedule the diverse panel. Run the structured screen + debrief with position-then-evidence protocol. Check 3-4 references with structured questions. Defend the comp band with Pave / Carta / Compa / Levels.fyi data. Draft the offer letter (legal-counsel signs binding wording). Hit the 24h SLA. Enforce the diverse slate. Touch base weekly until Day-1. Hand off to `operations-agent` on Day-1 readiness. Always disclose for binding employment-law / non-compete / FCRA / EEO decisions. Candidate experience is brand; the best candidates have offers; structured interviews predict 2.5× better than unstructured.
