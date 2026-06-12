# Operations Agent — Role Content (appended to AGENT.md)

> This file appends to `AGENT.md` and is **not** loaded into the agent's default context. The agent reads `soul.md` every turn and **greps** this file for deep references when stuck.
>
> Search-friendly headings include: "Capability reference", "Hiring playbook", "Onboarding playbook", "Offboarding playbook", "Performance cycle playbook", "Compensation bands playbook", "Vendor evaluation playbook", "SaaS spend audit playbook", "Procurement intake playbook", "Internal tools playbook", "Workflow automation playbook", "Process documentation playbook", "SSO setup playbook", "Device management playbook", "Payroll setup playbook", "EOR global hiring playbook", "Travel and expense playbook", "Insurance audit playbook", "Office management playbook", "Business continuity playbook", "Vendor risk assessment playbook", "Internal knowledge base playbook", "Runbook authoring playbook", "AI policy playbook", "Antipattern catalog", "SOTA tool reference", "Divio Diátaxis taxonomy", "Intake form templates", "Handbook section index", "Renewal calendar template".

For provenance, see `SOURCES.md`.

---

## Capability reference

### ATS / hiring platforms supported

- **Greenhouse** — 7,500+ customers; #1 G2 Winter 2026; 600+ integrations; structured-hiring leader. REST API for jobs, candidates, applications, scorecards.
- **Ashby** — founded 2019; modern architecture; deepest analytics (pipeline velocity, source attribution, interviewer calibration); built-in compensation field on public job feed (`includeCompensation=true`).
- **Lever** — ATS + CRM in one; clean public job-feed JSON (team, department, location, commitment, level filters).
- **Workable** — SMB-friendly; AI candidate sourcing.
- **Recruitee** — EU-focused; design-led.
- **Pinpoint** — mid-market; UK origin.
- **SmartRecruiters** — enterprise; recruitment marketing layer.
- **iCIMS / Workday Recruiting / SuccessFactors** — enterprise.

### HRIS / payroll platforms supported

- **Gusto** — SMB <50 employees; multi-state US; clean payroll; contractor support; ~$40/mo + $6/employee.
- **Rippling** — 50+ employees; HRIS + IT + Payroll + Finance in one; only platform that ships MDM + SSO + app provisioning natively; Mac/Win/Linux MDM.
- **Justworks** — PEO; small teams enterprise benefits; co-employment model.
- **HiBob** — mid-market; culture-led; BYO payroll (integrates with leading payroll providers); strong EU presence.
- **BambooHR** — SMB / mid-market US-focused; HRIS-led; lighter on payroll.
- **Paylocity / Paychex / ADP** — enterprise; deep payroll.
- **Personio** — EU mid-market.
- **Sequoia** — high-touch services + tech.
- **Trinet** — PEO.

### EOR / PEO global hiring platforms

- **Deel** — 150+ countries; only EOR with public API docs + sandbox + webhooks pre-contract; full workforce platform (EOR + payroll + contractors + HR + IT + compliance).
- **Remote.com** — 100+ countries; straightforward; owned entities + partner network.
- **Oyster HR** — 180+ countries; remote-first; employee experience focus.
- **Pebl** (formerly Velocity Global, rebranded Sept 2025) — AI-powered platform; 48-hour onboarding; AI assistant Alfie.
- **Globalization Partners (G-P)** — enterprise; established player.
- **Multiplier** — emerging; competitive pricing.
- **Rippling EOR** — bundled with Rippling.
- **Velocity Global** — (now Pebl).

### Performance / engagement platforms

- **Lattice** — default for growth-stage; goals + reviews + feedback + compensation + core HR.
- **15Five** — $9-15 PEPM; week-to-deploy; most affordable full perf-mgmt option.
- **Culture Amp** — engagement-survey DNA; research-driven; people analytics depth.
- **Leapsome** — widest breadth (perf + surveys + recognition + OKRs + onboarding + learning); EU GDPR-compliant.
- **Officevibe / Soapbox / Hypercontext** — 1:1-focused.
- **Bonusly / Workhuman** — recognition.
- **Reflektive** (now part of Lattice).
- **LifeLabs Learning** — manager training.

### Compensation platforms

- **Pave** — 11M+ data points; live compensation benchmarking.
- **Carta Total Comp** — integrated with cap table.
- **Comparably** — public-facing alt.
- **Levels.fyi** — engineering-comp public crowdsource.
- **Radford / Mercer / Aon Radford** — enterprise market data.
- **OpenComp** — alt market-data platform.

### Vendor / SaaS management platforms

- **Vendr** — 130K+ completed deals; largest deal database; AI negotiation agents + buyer team.
- **Tropic** — comprehensive vendor management beyond SaaS; benchmark data depth ($18B+).
- **Spendflo** — AI-driven; managed sourcing + automation.
- **Sastrify** — EU-focused.
- **Cledara** — EU.
- **Zylo** — finance-first spend visibility.
- **CloudEagle** — AI-driven.
- **Productiv** — usage-based optimization (SSO log cross-reference).
- **Torii** — alt usage-based.
- **SpendHound** — challenger.
- **Vertice** — combined procurement + spend.
- **Coupa** — enterprise procurement.
- **Ramp Procurement / Brex Procurement** — built-in to corp-card platforms.

### Workflow automation platforms

- **Zapier** — 8,000+ apps; Zapier Agents for autonomous tasks; widest app catalog; task-based billing.
- **Make.com** — 3,000+ apps; Maia AI assistant; agent builder beta; visual builder.
- **n8n** — 2.0 Jan 2026 native LangChain + 70+ AI nodes; self-host = no execution limits; 80-90% cheaper than Zapier for high volume.
- **Pipedream** — developer-friendly; code + UI hybrid.
- **Workato** — enterprise integration platform.
- **Tray.io** — enterprise; data-flow oriented.
- **Bardeen / Relay.app** — AI-first prompt-driven.
- **Apple Shortcuts** — personal / business macOS / iOS.

### Internal tool platforms

- **Retool** — mature commercial; polished UX; larger component library; higher per-user cost.
- **ToolJet** — open-source; AI-native architecture; Python support; "best Retool OSS alt" 2026.
- **Budibase** — open-source; no-code; auto-generated CRUD; built-in DB.
- **Appsmith** — open-source; JS-heavy code-first.
- **Internal.io** — commercial; design-focused.
- **Glide** — no-code mobile-first.
- **Bubble** — no-code web app.
- **Airtable Automations + Apps** — light internal-tool layer.
- **Softr / Stacker** — Airtable wrappers.
- **monday.com Apps** — embedded in monday.

### Device management platforms

- **Iru** (formerly Kandji, rebranded Oct 2025) — six-product unified platform: identity + endpoint + EDR + vuln mgmt + compliance + trust center; Mac/Win/Android single agent.
- **Jamf Pro** — Apple-only; deepest Apple-specific tooling; standalone Win/Android requires separate tool.
- **Microsoft Intune** — Win/Mac/iOS/Android single console; transitioning to Apple DDM framework.
- **Hexnode** — mixed fleet; SMB-friendly.
- **Mosyle** — Mac/iOS-focused.
- **Workspot** — Windows VDI.
- **Rippling IT** — lifecycle-tied (provisions on hire / deprovisions on offboard).
- **Electric** — MSP-style managed.
- **Esper / Scalefusion** — Android-focused.

### SSO / IAM platforms

- **Okta** — workforce + customer in one contract; enterprise; broadest integration catalog.
- **OneLogin** — workforce IAM alt.
- **JumpCloud** — open directory (IAM + MDM + infra access in one); Mac/Win/Linux MDM bundled.
- **WorkOS** — B2B SaaS enterprise readiness (SAML + SCIM + audit + orgs + IdP catalog productised; 4-week→4-day SAML).
- **Stytch** — B2B Organizations + Members + SCIM + RBAC + MFA; headless; pre-PMF/seed sweet spot.
- **Auth0** — Series A-B leader; decade incumbent.
- **Clerk** — B2B SSO; embeddable.
- **Tailscale** — zero-trust networking.
- **Scalekit** — SAML/OIDC SSO across Okta + Entra ID + Google + JumpCloud + OneLogin + AD FS + Ping + Shibboleth.

### Process documentation platforms

- **Notion** — most-deployed general doc + KB platform; Notion Agents for autonomous bots trained on teamspaces.
- **Confluence** — enterprise wiki; Rovo AI fully integrated 2026; 20+ pre-built agents.
- **GitBook** — docs-focused.
- **Slab** — 5-20 person teams; free <10 users; unified search across Slab + Slack + Drive + Notion.
- **Tettra** — Slack-native; AI-routed Q&A → KB.
- **Document360** — KB-focused.
- **Slite** — clean alt.
- **BookStack** — open-source self-host.
- **Tango** — auto-capture screenshot + annotation guide.
- **Scribe** — auto-capture live screen recording → step-by-step.
- **Whale** — Step Recorder + AI SOP draft.
- **Trainual** — training + SOPs + tracking + handbook.
- **Berrycast** — Loom-style.

### Travel + expense + corp card

- **Brex** — multi-entity 50+ countries; acquired by Capital One April 2026 ($5.15B); BrexPay for Navan since Oct 2024.
- **Ramp** — control-first; customizable card limits + AI duplicate/anomaly flagging.
- **Navan** (formerly TripActions) — AI assistant Ava; Expense Chat (94/100 CSAT beta); 70%+ corp-card txns zero manual intervention.
- **Expensify** — SMB-friendly expense.
- **SAP Concur** — enterprise.
- **Center** — alt.
- **Mesh Payments** — global.
- **Pleo** — EU.

### Insurance platforms

- **Vouch** — startup-only; web3 + AI-native coverage; entirely digital.
- **Embroker** — Startup Package — instant bundle of D&O + E&O + Cyber + EPLI.
- **Newfront** — InsureTech alt.
- **Coalition** — cyber insurance leader.
- **At-Bay** — cyber.
- **Founder Shield** — startup-focused broker.
- **The Hartford** — established carrier.
- **Sequoia** — high-touch services + insurance.
- **Coterie** — small business.

### Office / workplace platforms

- **Robin** — 2026 Gartner MQ Leader for Workplace Experience; AI-powered workplace ops; desk + room + parking booking.
- **Envoy** — visitor management leader; delivery; compliance features.
- **Tactic / Skedda** — desk booking alts.
- **Eden Workplace** — alt.
- **Ronspot** — desk booking + parking.
- **WeWork API** — for WeWork members.

### Knowledge base / wiki platforms

- **Notion** — 2026 Notion Agents trained on teamspaces (e.g., HR Agent monitoring Benefits DB).
- **Confluence** — Rovo AI 2026; 20+ pre-built agents.
- **Slab** — free <10 users; cross-tool unified search.
- **Tettra** — Slack-native; $4/user; AI-routed.
- **GitBook** — docs-focused.
- **Document360** — KB.
- **Slite** — clean.
- **Stack Overflow for Teams** — engineering KB.

### Background check + I-9 platforms

- **Checkr** — largest US background check.
- **GoodHire** — mid-market.
- **Certn** — global.
- **HireRight** — enterprise.
- **Sterling** — enterprise.
- **WorkBright** — I-9 specialist.

### Forms / surveys

- **Typeform** — design-led survey + form leader.
- **Tally.so** — fast / free / lightweight.
- **Notion forms** — embedded in Notion.
- **BlockSurvey** — privacy-focused.
- **SurveyMonkey** — enterprise.

---

## Hiring playbook

### Pipeline structure

```
Source (LinkedIn / Greenhouse jobs / Ashby careers / referrals)
  ↓
Recruiter screen (30 min — fit + signal + comp expectation + start date)
  ↓
Hiring manager screen (45 min — role-specific signal)
  ↓
Loop (3-5 interviewers, 45-60 min each, scorecards)
  ↓
Debrief (calibration session — 30 min, hire/no-hire by rubric)
  ↓
Offer (comp band check + offer letter draft → defer binding to `legal-counsel`)
```

### Scorecard structure per role

- **Must-haves** (3-5; pass/fail) — drives no-hire if any failed
- **Nice-to-haves** (3-5; signal) — drives differentiation between hire candidates
- **Disqualifiers** (named explicitly) — bias-checked
- **Interviewer-specific focus** (e.g., system design, behavioral, role-skill) — avoid duplicate coverage across loop

### Pass-through targets (calibrate per role)

| Stage | Healthy pass-through | Low signal |
|---|---|---|
| Source → Recruiter screen | 30-50% | <20% (sourcing miss) |
| Recruiter → HM screen | 50-70% | <30% (recruiter rubric weak) |
| HM → Loop | 40-60% | <25% (HM screen weak) |
| Loop → Offer | 25-40% | <15% (loop bias or pipeline weak) |
| Offer → Accept | 80%+ | <60% (comp band low or close mechanism weak) |

### JD authoring guardrails

- Open with team / mission / why-this-matters (3-5 lines), not bullet salad.
- Must-haves: tight, role-specific, explicit; "you have X years of Y" only if truly load-bearing.
- Nice-to-haves: separate section, not buried.
- Comp band: include (Colorado / NYC / WA law requires; AHA cohort data says posts with comp get 2-3x applicants).
- Bias review: scrub "rockstar", "ninja", gendered terms (Joblint / Textio); check for hidden disqualifiers.

---

## Onboarding playbook

### Day 0 (pre-start)

- **Hardware:** order via MDM zero-touch enrollment (Apple ABM / Microsoft AutoPilot); ship to arrive Day -3.
- **Provisioning:** HRIS profile + payroll + SCIM-driven app accounts (Google Workspace / Slack / GitHub / Notion / Linear / role apps); JIT provisioning via Okta / WorkOS / JumpCloud.
- **Documents:** offer letter signed (countersigned by `legal-counsel` if execs); handbook ACK pending; I-9 / W-4 (or W-9 for contractors); benefits enrollment forms.
- **Communications:** welcome email from manager Day -1; calendar holds (Day-1 / Day-7 / 30-day / 60-day / 90-day check-ins).

### Day 1

- **9am:** manager greeting (Zoom or in-person); team intro in Slack `#team-announce` channel.
- **10am:** HR / ops 1:1 — handbook walkthrough + ACK signed + benefits enrollment confirmed.
- **11am:** IT 1:1 — laptop login + MFA setup + tooling tour.
- **1pm:** team intro lunch (remote: virtual coffee).
- **3pm:** first task assignment from manager — small enough to ship Day 1.
- **EOD:** manager 1:1 check-in (30 min).

### Week 1

- **Buddy pairing:** named buddy (cross-team if possible); 3 standing 30-min coffees Week 1.
- **System tour:** access verification across all SaaS — flag any provisioning miss.
- **Stakeholder map:** manager-led intro to 5-7 key cross-team people.
- **First contribution:** ship a small change to a real artifact.

### 30 / 60 / 90 milestones

- **30 days:** competency assessment vs role rubric; expectations alignment; goal-setting (3-5 goals); manager debrief.
- **60 days:** delivery on first goal; expanded scope; manager + HR check-in.
- **90 days:** end-of-ramp review; comp / equity confirmation; long-term goals; promotion / extension path discussion.

### Provisioning matrix (per role)

| Role | Apps to provision (SCIM groups) |
|---|---|
| Engineering | Google Workspace / Slack / GitHub (org + repo by team) / Linear / Notion / Sentry / DataDog / 1Password |
| Sales | Google Workspace / Slack / Salesforce or HubSpot / Gong / Outreach / LinkedIn Sales Navigator / Notion |
| Marketing | Google Workspace / Slack / Buffer or Hootsuite / Figma / GA4 / Mailchimp or Klaviyo / Notion |
| Operations | Google Workspace / Slack / Notion / Linear / Rippling-Gusto / Okta / Brex-Ramp / Robin-Envoy |
| Customer support | Google Workspace / Slack / Zendesk or Intercom / Linear / Notion |
| Finance | Google Workspace / Slack / Xero or QBO / Brex-Ramp / Carta / Pulley / Notion |
| Executive | Google Workspace / Slack / Calendly / Notion / docusign |

---

## Offboarding playbook

### T-0 (last day)

- **9am same day:** SCIM deprovisioning across all SSO-connected apps; revoke direct logins.
- **10am:** device wipe via MDM (remote wipe → relocate to standby pool); courier label for hardware return if remote.
- **11am:** GitHub repo access revoke; transfer ownership of repos / Linear projects.
- **12pm:** exit interview (Typeform / Lattice exit survey) — schedule for week of departure.
- **EOD:** final paycheck calc per state law (PTO payout per state — CA / IL / MA require; TX / FL do not).

### State-specific final-paycheck rules (US)

| State | PTO payout? | Notes |
|---|---|---|
| CA | Yes (mandatory) | Plus immediate-pay-on-termination law |
| IL | Yes (if accrued, per policy) | |
| MA | Yes (per policy or law) | |
| NY | Per company policy | |
| TX | No (per company policy) | |
| FL | No (per company policy) | |
| WA | Per policy | |

### Access revocation order (priority)

1. SSO / SCIM directory (Okta / WorkOS / JumpCloud) — disables all downstream
2. Direct logins (apps without SCIM) — manual revoke
3. Code repositories (GitHub / GitLab / Bitbucket) — remove from teams
4. Cloud infrastructure (AWS / GCP / Azure IAM) — defer to `devops-engineer`
5. Customer data systems (Salesforce / HubSpot / Stripe) — revoke + audit
6. Communication (Slack / Teams) — convert to single-channel guest if exit-handoff needed
7. Email (Gmail / Outlook) — forward to manager 30 days then archive
8. MDM (device wipe + relocate to pool)
9. Hardware (laptop / monitor / keys / badge)
10. Audit log: timestamp each revocation; produce report

### Knowledge transfer template

- **In-flight projects:** list + owner-handoff + due dates
- **Recurring duties:** list + new owner + cadence
- **Vendor contacts:** vendor + relationship + renewal date
- **Tribal knowledge:** "things I know that aren't documented" (15-30 min capture session)
- **Direct reports (if manager):** 1:1 schedule transfer + check-in plan with new manager

---

## Performance cycle playbook

### Cadence options

- **Annual:** 1 big cycle / yr; often Q4 or Q1; pairs with comp review.
- **Semi-annual:** 2 cycles / yr; H1 + H2; lighter calibration each.
- **Continuous:** ongoing feedback + quarterly check-in; pairs with OKR; favored by 15Five / Lattice continuous philosophy.

### Cycle structure (e.g., annual)

1. **T-8 weeks:** open cycle; managers nominate raters; ICs draft self-review.
2. **T-6:** peer / upward feedback open.
3. **T-4:** all feedback closed; managers write summary review.
4. **T-2:** calibration sessions (cross-team) — normalize ratings + flag outliers.
5. **T-0:** comp decisions finalized; review delivery to ICs (managers).
6. **T+2:** comp letters delivered; promotion announcements.
7. **T+4:** retro on cycle — what worked, what to fix.

### Rating scale standard

- **5-point Likert with anchors:** Outstanding (5) / Exceeds (4) / Meets (3) / Developing (2) / Below (1).
- **Avoid 4-point** (forces hide-the-3 calibration); **avoid 3-point** (too coarse for comp).
- **Rubric per role + level** — concrete behaviors per anchor.

### Calibration session structure

1. **All managers in same level cohort.** Engineering managers calibrate engineering ICs together.
2. **Distribution target.** Target distribution (e.g., 10% / 25% / 50% / 15%) — flag overconcentration.
3. **Outlier review.** Top 10% and bottom 10% reviewed manager-by-manager for evidence.
4. **Adjustment.** Manager owns final rating but cohort calibrates.
5. **Output:** calibrated rating matrix → feeds comp-decision matrix.

### Comp-decision matrix

| Rating | Base raise | Equity refresh | Bonus % | Promo eligibility |
|---|---|---|---|---|
| Outstanding | 8-15% | Yes | 100-150% target | Yes |
| Exceeds | 5-8% | Yes | 100-125% target | Maybe |
| Meets | 3-5% | Standard refresh | 80-100% target | No |
| Developing | 0-3% | No | 50-80% target | No |
| Below | 0% (PIP) | No | 0-50% target | No |

---

## Compensation bands playbook

### Band structure

For each role × level × geography:
- **Band low** (P10 market or 0.85x midpoint)
- **Band mid** (P50 market — target band placement for "Meets" performer)
- **Band high** (P90 market or 1.15x midpoint)

### Geo tiers (US default — adapt globally)

- **Tier 1** (SF / NYC / Seattle / Boston / LA) — 100% market.
- **Tier 2** (Denver / Austin / Chicago / Portland / Atlanta / DC / SD) — 90-95%.
- **Tier 3** (most other US) — 85-90%.
- **Remote-global** — local market per country (Deel comp data) or US Tier-3 if US-policy.

### Sources for band data

1. **Pave** (live market data; 11M+ data points; paid).
2. **Carta Total Comp** (cap-table integrated; paid).
3. **Radford / Mercer / Aon Radford** (enterprise survey; paid).
4. **Levels.fyi** (engineering public crowdsource; free for ICs).
5. **Glassdoor** (broad self-reported; lower quality but free).
6. **State-mandated salary disclosures** (CO / NYC / WA / CA) — secondary public data.

### Band placement rules

- **New hire:** start within 50-75% of band based on level fit + market urgency.
- **Performer at "Meets":** target band midpoint over 2-3 cycles.
- **High performer:** can reach band high; promo when above-band performance sustains.
- **Band overlap:** adjacent levels can overlap by ~20%; flat-line beyond is wage compression.

---

## Vendor evaluation playbook

### Stage 0 — confirm the need is real

- **What problem are we solving?** Name the specific pain.
- **What's the cost of NOT solving it?** Quantify (hours / dollars / risk).
- **Have we tried existing tools first?** Often the answer is "expand the seat count on what we have."
- **Build vs buy** (Spolsky "Strategy Letter V" — is this core to the business or context?). Core = consider build; context = buy.

### Stage 1 — landscape map (3-5 candidates)

- Pull 2025-2026 comparison posts (avoid 2022 listicles).
- Filter by: stage-appropriate price tier, integration with existing stack, security posture (SOC 2 floor), data residency if relevant.
- Drop candidates that fail any non-negotiable filter at this stage.

### Stage 2 — TCO matrix

For each candidate:
- **License cost** (per seat × seats × 12; multi-year discount factored).
- **Integration cost** (engineering hours × loaded rate).
- **Training cost** (ops + manager hours × loaded rate).
- **Opportunity cost** (time-to-value × delayed-benefit value).
- **Switching cost** (data export complexity + retraining for future migration).
- **Vendor stability risk** (funding stage, recent layoffs, M&A risk).
- **Lock-in risk** (data portability, API openness, contract minimums).

### Stage 3 — security review

- SOC 2 Type 2 report — 73% of 2026 buyers start here per Secureframe.
- DPA available (purpose + sub-processors + breach notice + audit + retention/deletion + assistance).
- Pen-test summary (public or NDA-shared).
- ISO 27001 if global / regulated.
- Recent breach history (search company name + "data breach").

### Stage 4 — reference calls (2-3)

- Ask similar-stage / similar-use-case customers.
- Open-ended: "What's the worst thing about working with [vendor]?" surfaces the truth.
- Implementation reality: actual time, actual blockers.
- Renewal experience: did the price hike, did service degrade?

### Stage 5 — recommendation memo (1 page)

```
Decision: [Vendor X] — buy / build / pass

Rationale (3-5 bullets):
- ...

TCO (Year 1 / Year 3):
- Year 1: $X (license + impl + training)
- Year 3: $Y (annual run-rate × 3)

Alternatives considered:
- Vendor A: rejected because Z
- Vendor B: rejected because Z

Lock-in / switching cost:
- Data export: [format / complexity]
- Contract minimum: [length]
- Switching window: [weeks]

Security posture:
- SOC 2 Type 2: [Yes / No]
- DPA available: [Yes / No]
- Data residency: [US / EU / both]

Open questions / DECISION REQUIRED:
- ...
```

---

## SaaS spend audit playbook

### Inputs

- 12-month spend by vendor from `xero-mcp` GL (filter to SaaS / software-services accounts).
- Corp-card txns from Ramp / Brex APIs.
- SSO login data from Okta / WorkOS / JumpCloud (last-90-day login count per user per app).
- Seat counts from each SaaS platform admin console (or platform API).

### Analysis steps

1. **Rank by spend.** Top 10 should = ~70-80% of total spend per Tropic 2025 benchmark; flag if not.
2. **MAU check.** Tools with <50% MAU = candidate cut or seat reduction.
3. **Duplicate detection.** Common duplicates:
   - Notion + Confluence + Slab + Slite (consolidate to 1)
   - Slack + Teams + Discord (consolidate when possible)
   - Figma + Sketch + Adobe XD (Figma is 2026 standard)
   - Loom + Berrycast + Scribe + Tango (one capture tool)
   - Zoom + Google Meet + Teams (one video)
   - Calendly + SavvyCal + Cal.com (one scheduler)
   - LastPass + 1Password + Bitwarden (one password mgr)
   - Dropbox + Google Drive + OneDrive (one cloud storage)
4. **Shadow-IT scan.** Cross-ref corp-card txns vs known SaaS list — find unauthorized signups.
5. **Renewal calendar.** Every contract gets 90/60/30/7-day alerts in `notion-mcp` DB + `google-calendar-mcp` + Slack.

### Decision matrix per vendor

| Status | MAU | Spend | Recommendation |
|---|---|---|---|
| Critical (mission-critical workflow) | >70% | Any | Keep, negotiate multi-year |
| Useful (occasional value) | 30-70% | High | Reduce seats; negotiate renewal |
| Useful | 30-70% | Low | Keep |
| Underutilized | <30% | High | Cut or replace cheaper |
| Underutilized | <30% | Low | Cut at renewal |
| Duplicate | Any | Any | Consolidate to one |
| Shadow-IT | Any | Any | Audit + decide (cut or formalize) |

---

## Procurement intake playbook

### Intake form template (Typeform / Tally / Notion form)

```
1. Vendor name + URL + category
2. Business need (3-5 lines):
   - Problem being solved
   - Current workaround
   - Cost of NOT solving
3. Cost
   - Annual license $
   - Implementation $
   - Per-seat or fixed?
4. Alternatives considered (≥2)
5. Security
   - SOC 2 Type 2 available? (Y/N)
   - DPA available? (Y/N)
   - Data classification (PII / IP / public)?
6. Integration
   - Connects to: [list]
   - Engineering effort: [low / med / high]
7. Owner + manager approval
```

### Approval routing by spend tier

| Annual cost | Approval | SLA |
|---|---|---|
| <$500/yr | Manager only | 24h |
| $500-$5K | Manager + ops | 3 business days |
| $5K-$25K | Ops + exec | 5 business days |
| >$25K | Exec + (CFO if >$50K) | 10 business days + RFP |

### Contract + storage workflow

- Signed contracts → `google-drive-mcp` (folder by category: SaaS / Services / Insurance / Legal).
- DB entry in `notion-mcp` with: vendor / category / cost / contract start / contract end / auto-renew Y/N / owner / category / renewal-alert dates.
- Calendar entries: 90/60/30/7-day renewal alerts (manual or via n8n / Zapier workflow).

---

## Internal tools playbook

### Platform pick

```
Need polished UI + budget? → Retool
Need OSS + AI-native + Python? → ToolJet
Need fast no-code + auto-CRUD? → Budibase
Need JS-heavy code-first? → Appsmith
Need Airtable / Sheets back-end + simple UI? → Stacker / Softr
Need mobile-first? → Glide
Need full custom web app? → Bubble (no-code) or sub to engineering
```

### Build steps

1. **Data connection.** Connect to source (Postgres / MySQL / REST API / Airtable / Google Sheets).
2. **Query design.** Pre-build SQL / REST queries; parameterize.
3. **UI assembly.** Drag-and-drop components; bind to queries.
4. **Permission model.** Role-based access per row / column / action.
5. **Auth.** Ship behind SSO (SAML / OIDC via Okta / WorkOS / JumpCloud).
6. **Audit log.** Enable platform audit log for who-did-what.
7. **Documentation.** Notion KB entry with: purpose / users / queries / known issues / owner.

### When to NOT build internal tool

- One-time use → use a spreadsheet.
- High-frequency + customer-facing → real engineering project.
- Workflow > 5 steps → use workflow automation instead.
- Complex permissions / compliance → buy SaaS (Retool overhead grows).

---

## Workflow automation playbook

### Platform pick

```
<100 runs/mo + non-technical team + max app catalog → Zapier
100-5K runs/mo + visual builder + mid-technical → Make
>5K runs/mo OR LangChain agent needed OR self-host = data sovereignty → n8n
Developer-team + code-friendly → Pipedream
Enterprise + complex data flow → Workato or Tray.io
Personal / one-off macOS → Apple Shortcuts
```

### Workflow design rules

- **Idempotency.** Workflow can re-run without side effects.
- **Error handling.** Branch to alert channel (Slack / email) on failure.
- **Dry-run.** Test 10 cycles in dry-run before production.
- **Owner.** Named in Notion KB + last-tested date.
- **Cost projection.** vs alternative (Zapier tasks vs n8n self-host vs hand-execute).

### Common ops automations (priority order)

1. **New hire provisioning** — HRIS hire event → SCIM provision + Slack welcome + calendar holds.
2. **Termination deprovisioning** — HRIS term event → SCIM revoke + device wipe + ticket Linear.
3. **Vendor renewal reminders** — Notion DB date trigger → Slack + email 90/60/30/7-day alerts.
4. **Expense exception flagging** — Ramp / Brex anomaly → Slack alert to ops.
5. **Onboarding milestone tracking** — Google Calendar Day-1/Week-1/30-day → Notion update + manager Slack.
6. **Exit interview survey** — Termination event → Typeform survey to ex-employee.
7. **Handbook ACK tracking** — HRIS hire event → DocuSign → Notion DB.
8. **SaaS spend monthly sync** — Xero/QBO → Notion vendor DB.
9. **Status page incident** — Sentry alert → Statuspage update + Slack incident channel.

---

## Process documentation playbook

### Divio / Diátaxis taxonomy

Four doc types — each serves a different need; don't mix:

- **Tutorial** (learning by doing) — guide a beginner through a complete cycle.
- **How-to** (task accomplishment) — answer "how do I X?" with concrete steps.
- **Reference** (lookup) — exhaustive, structured factual info.
- **Explanation** (background) — why does this exist, what are the trade-offs.

### Tool pick

| Need | Tool |
|---|---|
| Auto-capture (live screen record → guide) | Scribe / Tango |
| Auto-capture (step-by-step with AI rewrite) | Whale |
| Org-wide handbook + SOPs + tracking | Trainual |
| General KB + AI agents | Notion |
| Enterprise wiki + Rovo AI | Confluence |
| Slack-native Q&A → KB | Tettra |
| Free <10 users + cross-tool search | Slab |
| Docs-as-code engineering | GitBook |

### Authoring quality bar

- **Title** — answers "what is this?" in 5 words.
- **Audience** — named explicitly: "For engineers onboarding to the data team."
- **Prereqs** — listed up top.
- **Steps** — numbered, imperative voice ("Click X" not "you should click X").
- **Verification** — "Done when X visible."
- **Last reviewed / owner** — in header.
- **30-day recheck** scheduled for criticality-1 docs.

---

## SSO setup playbook

### Stage-based platform pick

| Company stage | Pick | Why |
|---|---|---|
| Pre-PMF / seed (<5 engineers) | Stytch or SSOJet | Simple B2B Orgs+Members; low-cost |
| Series A-B ($1-20M ARR) | Auth0 | Decade leader; broad app support |
| Series A+ B2B SaaS w/ enterprise deals imminent | WorkOS | Productized enterprise readiness; 4-week→4-day SAML |
| Enterprise workforce + customer in one | Okta | Broadest catalog; single contract |
| Want IAM + MDM + infra access in one | JumpCloud | Open directory; bundled MDM |

### SCIM provisioning rules

- **One SCIM group per role × geography** — never per-individual.
- **JIT (just-in-time) provisioning** for first-login app activation.
- **Deprovisioning** triggered by HRIS termination event (same-day SLA).
- **Audit log** retained 1+ year for compliance.

### Top-10 apps to SCIM-connect first

1. Google Workspace (or Microsoft 365)
2. Slack
3. GitHub (or GitLab)
4. Notion (or Confluence)
5. Linear (or Jira)
6. AWS / GCP / Azure (defer to `devops-engineer`)
7. Sentry / DataDog
8. Salesforce or HubSpot
9. Zoom (or Teams)
10. 1Password / Bitwarden / LastPass

---

## Device management playbook

### Platform pick

| Fleet | Pick | Why |
|---|---|---|
| Apple-only, deep tooling | Jamf Pro | Apple-only, deepest |
| Apple-only, modern | Iru (formerly Kandji) | Six-product unified platform; Mac/Win/Android single agent post-rebrand |
| Mixed Win/Mac | Microsoft Intune | Transitioning to Apple DDM; Win-default |
| Mixed Win/Mac + lightweight | Hexnode | SMB-friendly |
| Want HRIS+MDM in one | Rippling IT | Lifecycle-tied; provision on hire / deprovision on term |
| Android-heavy | Esper or Scalefusion | Android-focused |

### Blueprint contents (per role)

- **App bundle** — core (Slack / Notion / 1Password / Zoom) + role-specific.
- **OS update policy** — auto-install N-1 within 14 days of release.
- **Encryption** — FileVault (Mac) / BitLocker (Win) enforced.
- **Endpoint protection** — Iru EDR or CrowdStrike or SentinelOne.
- **VPN / zero-trust** — Tailscale / Cloudflare WARP if not on-cloud.
- **Compliance check** — encryption + OS up-to-date + EDR running.

### Lifecycle hooks (HRIS → MDM)

- **Hire event** → enroll device → install blueprint → activate user.
- **Role change** → swap blueprint → re-install role apps.
- **Termination** → remote wipe → relocate to standby pool.

---

## Payroll setup playbook

### Platform pick

| Team size | Multi-state? | Pick |
|---|---|---|
| <50, US-only | Multi-state | Gusto |
| <50, US + benefits-led | — | Justworks PEO |
| 50+, US, distributed | Multi-state | Rippling |
| Mid-market US/global, HRIS-led | — | HiBob (BYO payroll) |
| Global contractors + EOR | — | Deel |
| Enterprise | — | Workday / ADP / Paychex |

### Setup steps

1. State tax registration per state of employment (defer binding to `finance-controller` + CPA).
2. Federal EIN if new entity.
3. Benefits: health / dental / vision / 401(k) / commuter (Justworks PEO bundles enterprise rates; Gusto + Guideline / Human Interest standalone).
4. Workers' comp registration per state (often statutory).
5. State-mandated required policies (CA paid sick leave, IL Domestic Workers Bill of Rights, etc.).
6. Pay schedule (bi-weekly / semi-monthly).
7. First payroll dry run → tie out to GL (defer to `finance-controller`).

---

## EOR global hiring playbook

### Country selection matrix

```
Hiring 1-2 people in country? → EOR (Deel / Remote / Oyster / Pebl / G-P).
Hiring 5+ people in country with intent to scale? → Open own entity.
Need 48-hour onboarding? → Pebl (AI-driven).
Need best API integration? → Deel (only EOR with public docs + sandbox + webhooks pre-contract).
EU-focused? → Oyster (180+ countries; experience focus) or Remote (100+).
Enterprise-grade? → G-P.
```

### Per-country gotchas

- **UK:** statutory holiday 28 days; pension auto-enrollment; notice period typically 1 mo.
- **Germany:** strong labor protection; written work council notice; non-compete must pay.
- **France:** 35-hr workweek baseline; 5 weeks paid leave; complex termination.
- **Singapore:** statutory CPF contributions; flexible at-will.
- **Australia:** Fair Work Act; superannuation 11.5%; redundancy pay schedule.
- **Brazil:** complex labor laws (CLT); 13th-month salary; FGTS contribution.
- **India:** EPF + Gratuity; notice periods up to 60 days; offer letter must include all.
- **Canada:** province-specific (ON, QC, BC); notice + severance per Employment Standards Act.
- **Mexico:** statutory 12-day vacation + 25% premium; profit-sharing (PTU); 13th-month aguinaldo.

**Always disclose:** "Defer to `legal-counsel` for binding country-specific employment-law review."

---

## Travel and expense playbook

### Platform pick

| Need | Pick |
|---|---|
| Integrated travel + card + expense | Brex (Capital One) + BrexPay for Navan |
| Control-first card + AI flagging | Ramp |
| Travel-focused with AI assistant Ava | Navan (uses Navan Connect to link existing cards) |
| SMB expense | Expensify |
| Enterprise | SAP Concur |
| Global / multi-currency | Mesh Payments |
| EU | Pleo |

### Policy components

- **Cabin class** (economy / premium econ / business — by flight duration + role).
- **Hotel cap** (per-city tier).
- **Meal per-diem** (by city tier).
- **Approval threshold** ($X auto-approve / $Y manager / $Z exec).
- **MCC restrictions** (block gambling, adult content, certain crypto).
- **Receipt threshold** ($25 standard; smaller for cash).
- **Out-of-policy escalation** flow.

---

## Insurance audit playbook

### Coverage stack by stage

| Stage | Coverage | Typical premium |
|---|---|---|
| Pre-funding / pre-revenue | General Liability + Business Property | $500-$1.5K/yr |
| Seed | Add D&O | $3-8K/yr |
| Series A | Add E&O + Cyber + EPLI (Embroker Startup Package) | $15-30K/yr bundled |
| Series B+ | Increase limits; add Crime, Fiduciary, K&R if global | $40-100K/yr |
| Pre-IPO | Add Side A D&O; reinsurance review | $200K+/yr |

### Coverage definitions

- **General Liability (GL):** third-party bodily injury, property damage.
- **Business Property:** office contents, equipment.
- **D&O (Directors & Officers):** protects execs + board from mgmt-decision lawsuits; required for institutional investors.
- **E&O (Errors & Omissions / Professional Liability):** customer claims for product / service failure.
- **Cyber:** data breach response + notification + ransomware. 2026 median premium $2,968.
- **EPLI (Employment Practices Liability):** wrongful termination, discrimination, harassment claims.
- **Workers' Comp:** state-mandated.
- **K&R (Kidnap & Ransom):** for execs traveling to high-risk regions.
- **Fiduciary:** ERISA / 401(k) breach claims.
- **Crime:** employee theft, fraud, social engineering.

### Renewal review (annual)

- 90 days pre-renewal: pull declarations page + claims history.
- Re-quote with 2-3 brokers (Vouch / Embroker / Newfront / Founder Shield / Sequoia).
- Update limits per company growth.
- **Always disclose:** "Defer to `legal-counsel` + insurance broker for binding binder review."

---

## Office management playbook

### Platform pick

| Need | Pick |
|---|---|
| Desk + room + parking booking + AI workplace ops | Robin |
| Visitor management + delivery + compliance | Envoy |
| Lightweight desk booking | Tactic or Skedda |
| Full WeWork integration | WeWork API |
| Workplace experience platform | Eden |

### Hybrid policy components

- **In-office days** (e.g., Tue-Wed-Thu) vs flexible.
- **Anchor day** (e.g., Wed all-hands).
- **Hot-desking** vs assigned desks.
- **Room booking norms** (cancel <30 min before = released).
- **Visitor sign-in** (Envoy Kiosk).
- **Delivery handling** (Envoy delivery notifications).

---

## Business continuity playbook

### Business Impact Analysis (BIA)

For each system / function:
- **Criticality** (Mission-Critical / Important / Standard).
- **Users impacted** (count + customer-facing or not).
- **Downtime cost per hour** ($).
- **RTO** (Recovery Time Objective — max acceptable downtime).
- **RPO** (Recovery Point Objective — max acceptable data loss).
- **Dependencies** (upstream / downstream systems).

### Tier table

| Tier | RTO | RPO | Approach |
|---|---|---|---|
| 1 (Mission-Critical) | <4h | <1h | Active-passive multi-region cloud; auto-failover |
| 2 (Important) | <24h | <4h | Backup + restore; documented manual failover |
| 3 (Standard) | <1 week | <24h | Manual rebuild from backup |
| 4 (Low) | <1 mo | <1 week | Snapshot + low-frequency backup |

### Incident comms playbook

1. **Detection** → on-call paged via PagerDuty / Incident.io.
2. **Triage** → severity (SEV-0 / SEV-1 / SEV-2 / SEV-3).
3. **Comms** (SEV-0 / SEV-1):
   - Internal: Slack `#incident` channel, all-hands as needed.
   - Customer: status page (Statuspage / Better Stack) + email if data impact.
   - Regulator: 72-hr GDPR notice if EU PII breach (defer to `legal-counsel`).
4. **Resolution:** root cause + fix + verification.
5. **Post-mortem** (blameless template; Google SRE pattern) — within 5 business days.

### Tabletop exercise

- Quarterly cadence; 60-90 min.
- Pick a scenario (cloud-region failure / ransomware / key-person unavailability / vendor outage).
- Walk through runbook step-by-step; flag gaps; assign remediation.
- Output: tabletop report + 3-5 action items.

---

## Vendor risk assessment playbook

### Risk tier

| Tier | Trigger | Review cadence |
|---|---|---|
| Critical | Handles PII / financial / IP / source code | Annual + change events |
| Important | Handles aggregated user data / business systems | Biennial |
| Standard | Low-data internal tools (handbook builder, etc.) | Passive (entry on register) |

### Assessment per vendor

1. **SOC 2 Type 2 report** — request from vendor; review controls in scope; flag gaps.
2. **ISO 27001** — alternative if SOC 2 unavailable; common in EU.
3. **Security questionnaire** — CAIQ / SIG Lite / custom; 70% of 2026 buyers use this.
4. **DPA** (Data Processing Addendum):
   - Purpose of processing
   - Confidentiality obligations
   - Sub-processors listed + flow-down obligations
   - Breach notice (typically 24-72h)
   - Audit rights
   - Retention + deletion timelines
   - Data subject rights assistance (GDPR Art. 15-21)
5. **Pen-test summary** — public or NDA-shared.
6. **Insurance** — cyber + E&O carried by vendor.
7. **Data residency** — US / EU / both; sub-processor regions.

### Register entry

```
Vendor: [Name]
Category: [Critical / Important / Standard]
SOC 2 Type 2: [Date of report] / [No]
ISO 27001: [Yes / No]
DPA signed: [Date] / Pending
Sub-processors: [List]
Data classification: [PII / IP / Aggregated / Public]
Data residency: [US / EU / Both]
Last review: [Date]
Next review: [Date]
Owner: [Person]
Risk flags: [List]
```

---

## Internal knowledge base playbook

### KB architecture pick

| Team size | Slack-heavy? | Pick |
|---|---|---|
| 5-20 | No | Slab (free <10 users; cross-tool search) |
| 5-20 | Yes | Tettra ($4/user; Slack-native AI routing) |
| 20-50 | Either | Notion (Notion Agents 2026) |
| 50+ enterprise | — | Confluence (Rovo AI 2026) |
| Docs-as-code engineering | — | GitBook |
| KB-only customer-facing | — | Document360 |

### Architecture rules

- **One source of truth.** Pick ONE KB; don't sprawl.
- **Top-level structure by team or function**, not by document type.
- **AI agents** (Notion Agents / Rovo / Tettra) trained on specific team-spaces.
- **Cross-tool search** (Slab / Glean / Coveo if going enterprise) for federated lookup.
- **Permissions** map to SCIM groups, never individuals.
- **Stale-content flag** at 90 days; archive at 1 year if not updated.

---

## Runbook authoring playbook

### Structure (per scenario)

```
# [Scenario name]

## Severity & response time
- SEV-0 / SEV-1 / SEV-2 / SEV-3
- Page on-call within [time]

## Symptoms
- [What you see when this happens]

## Diagnostic steps
1. Check [metric / log / dashboard]
2. Run [command / query]
3. Verify [condition]

## Mitigation steps
1. [Immediate action]
2. [Next action]
3. [Verification]

## Communication
- Internal: Slack `#incident` channel
- Customer: status page if customer-facing
- Stakeholders: [list]

## Recovery verification
- [How you know it's resolved]

## Post-mortem
- Schedule within 5 business days
- Use blameless template (Google SRE)

## Last tested
- [Date] by [person]
```

### Post-mortem template (blameless)

```
# Post-mortem: [Incident name]

Date: [YYYY-MM-DD]
Duration: [X min downtime]
Severity: SEV-[0-3]
Author: [Name]

## Summary
- [3-5 lines]

## Timeline
- HH:MM — [event]
- ...

## Root cause
- [What caused this]

## Resolution
- [What fixed it]

## Impact
- Users affected: [count]
- Revenue impact: $[amount] (defer to `finance-controller` for revenue calc)
- Customer-facing comms: [link]

## Lessons learned
- [What went well]
- [What didn't]

## Action items
- [ ] [Owner] — [Action] — [Due]
```

---

## AI policy playbook

### Policy components

1. **Approved tools list** — explicitly named (e.g., ChatGPT Enterprise, Claude.ai, Notion AI, GitHub Copilot Business).
2. **Data classification tier** — what's allowed by tier:
   - **Public:** any AI tool.
   - **Internal/Confidential:** only approved enterprise tools with DPAs.
   - **PII / customer data:** only tools with explicit PII processing DPA.
   - **IP / proprietary code:** only tools with explicit IP protection (e.g., Copilot Business no-training).
3. **Prompt-injection defense** — never paste customer data + URL in same prompt to web-search-enabled AI.
4. **Output review tier** — high-stakes outputs (legal, financial, customer-facing) require human review.
5. **Vendor AI DPA** — added to standard DPA template (model used + retention + opt-out of training).

### Frameworks

- **NIST AI RMF** (AI Risk Management Framework).
- **ISO/IEC 42001** (AI Management System; 2024 standard).
- **EU AI Act** (high-risk AI obligations; effective 2026).
- **Anthropic responsible-use guidance.**

### Tracking

- Approved-tool inventory in Notion DB.
- Quarterly review of approved tools.
- AI training for all employees on policy (Trainual / Whale rollout).

---

## Renewal calendar template

```
Vendor: [Name]
Category: [SaaS / Services / Insurance / Other]
Annual cost: $[X]
Contract start: [YYYY-MM-DD]
Contract end: [YYYY-MM-DD]
Auto-renew: [Yes / No]
Notice required: [N days]
Renewal alerts:
- [Date - 90d]: 90-day alert (review usage + plan)
- [Date - 60d]: 60-day alert (start re-quote / negotiation)
- [Date - 30d]: 30-day alert (finalize decision)
- [Date - 7d]: 7-day alert (action urgent)
Owner: [Person]
Last reviewed: [Date]
Renewal decision: [Renew / Renegotiate / Cancel / Replace]
```

---

## Intake form templates

### New tool request (Typeform / Tally / Notion)

```
1. Vendor name + URL
2. Category
3. Business need (problem solved + cost of NOT solving)
4. Annual cost estimate
5. Per-seat or fixed pricing?
6. Alternatives considered (≥2)
7. SOC 2 Type 2 available? Y/N
8. DPA available? Y/N
9. Data classification (Public / Internal / PII / IP)
10. Integration needs (current stack)
11. Engineering effort estimate (low / med / high)
12. Requested by + manager + business sponsor
13. Anticipated start date
```

### New hire request (manager → ops)

```
1. Role title + level
2. Reports to
3. Team
4. Target start date
5. Geography (US state or country)
6. Comp range (vs band)
7. JD (or request authoring help)
8. Hiring panel (3-5 names)
9. Approval (manager + finance per headcount plan)
```

### Termination request (manager → HR)

```
1. Employee name + role
2. Last day
3. Type (resignation / termination / mutual)
4. PIP status (if applicable)
5. Equity vesting cutoff
6. Final pay calculation (PTO payout per state)
7. Knowledge transfer plan
8. Exit interview schedule
9. Access revocation flag (priority)
10. Communication plan (team / Slack)
```

---

## Handbook section index

Standard sections (multi-state US — adapt globally):

1. **Welcome + company mission**
2. **At-will employment statement** (US)
3. **Equal employment opportunity + anti-discrimination**
4. **Anti-harassment policy** (CA + NY require specific training)
5. **Code of conduct**
6. **Confidentiality + IP assignment** (defer binding language to `legal-counsel`)
7. **Compensation philosophy + pay practices**
8. **Benefits overview** (health / dental / vision / 401(k) / commuter / EAP)
9. **Time off** — PTO policy + sick leave (per state) + parental leave + bereavement + jury duty
10. **Work hours + overtime** (FLSA exempt / non-exempt; state-specific rules)
11. **Remote / hybrid / in-office policy**
12. **Equipment + BYOD policy**
13. **Travel + expense policy**
14. **Performance review process**
15. **Promotion + advancement**
16. **AI usage policy** (data classification + approved tools)
17. **Information security + acceptable use**
18. **Drug + alcohol policy**
19. **Social media policy**
20. **Conflict of interest + outside employment**
21. **Anti-bribery + anti-corruption**
22. **Whistleblower / reporting concerns**
23. **Termination + final pay** (state-specific)
24. **Multi-state appendix** (CA / NY / IL / MA / WA — variances)
25. **Acknowledgement form** (signed at hire + annually + on update)

---

## Antipattern catalog

### Antipattern 1: Hire without provisioning plan

**BAD:** Hire starts Monday; ops scrambles Monday morning to provision accounts + ship laptop.

**Why bad:** Day-1 dead time loses ~$500 in salary + signals chaos to the hire; bad first impression has measurable retention impact.

**GOOD:** T-7 days: hardware ordered + arriving by T-3. T-3 days: SCIM provisioning + handbook ACK + benefits enrollment links sent. T-1 day: welcome message in Slack + calendar holds confirmed. Day 1: hire logs in and is productive by 11am.

### Antipattern 2: Termination access revocation "we'll get to it next week"

**BAD:** Terminated employee retains email + Slack + GitHub access for 5 days while ops handles "the paperwork first."

**Why bad:** Security incident waiting to happen — disgruntled access risk + insider exfil + bad audit trail.

**GOOD:** Same-day SCIM deprovisioning is policy. Termination at 10am → access revoked by 11am via automated workflow triggered on HRIS termination event. Audit log timestamped.

### Antipattern 3: Auto-renewing SaaS contract with no calendar reminder

**BAD:** Signed Notion contract auto-renews at 30% price hike; ops finds out from credit card charge.

**Why bad:** Surprise charges erode trust + miss negotiation leverage. Vendor lock-in is technical debt with a billing schedule.

**GOOD:** Every contract enters Notion DB on signature with 90/60/30/7-day Slack + email reminders. Auto-renewal flagged as policy violation unless explicitly approved.

### Antipattern 4: Per-individual SaaS access "exceptions"

**BAD:** "Sarah needs admin on Salesforce because she's special" — single-user grant without expiry, no group mapping.

**Why bad:** Exception sprawl. Three years later nobody knows why Sarah has admin or who else does. Failed audit + over-privileged access.

**GOOD:** Role-based SCIM groups + JIT provisioning + expiry date for true exceptions ("expires 2026-09-30, owner: [name]").

### Antipattern 5: Buy enterprise tool for 10-person team

**BAD:** Series Seed company signs Workday HRIS 3-year contract because "we'll grow into it."

**Why bad:** TCO destruction. Workday at 10 employees has implementation cost > 2 years of Gusto + Notion. Stage-appropriate tools matter.

**GOOD:** Stage-match. <50 = Gusto. 50+ = Rippling. 200+ = HiBob or Workday. Buy what fits today; switch when you outgrow.

### Antipattern 6: Handbook last updated 2024, multi-state laws since changed

**BAD:** Handbook references California paid sick leave at "3 days/yr" (was 3 days, now 5 days per AB 1041 effective Jan 2024 — and 7 days proposed 2026).

**Why bad:** Non-compliance + lawsuit risk + bad signal. Handbook is your audit trail when disputes arise.

**GOOD:** Quarterly handbook freshness review; subscribe to legal-update services (Mineral / SHRM HR Knowledge); track state-by-state policy changes.

### Antipattern 7: Workflow automation without owner

**BAD:** Engineer builds a Zapier workflow for vendor onboarding; engineer leaves; workflow breaks silently 4 months later.

**Why bad:** Orphan automations break in surprise ways. Cost: months of unknown broken state.

**GOOD:** Every automation has named owner + last-tested date + KB entry. Quarterly re-test cycle for criticality-1 workflows.

### Antipattern 8: Skip post-mortem after incident

**BAD:** After SEV-1 outage, team patches the bug + moves on. "We don't have time for the post-mortem."

**Why bad:** Lessons not captured. Same incident pattern recurs. No org-wide learning.

**GOOD:** Within 5 business days, blameless post-mortem (Google SRE template). Action items tracked in Linear. Lessons-learned KB entry public to the org.

### Antipattern 9: Skip SOC 2 review for "small" vendor

**BAD:** Sign with a small vendor handling employee PII because they're cheap; skip SOC 2 review.

**Why bad:** Per Secureframe 2026 benchmark, 73% of buyers start with SOC 2. Skipping = audit fail later + PII breach risk.

**GOOD:** Even for small vendors handling PII, request SIG Lite if SOC 2 unavailable. Register entry with risk flag if accepted.

### Antipattern 10: Heroic individual on critical workflow

**BAD:** "Only Alex knows how to run payroll; if Alex is out, payroll waits."

**Why bad:** Bus factor of 1. Risk concentration + manager-to-IC overdependence + retention leverage in the wrong direction.

**GOOD:** Documented runbook + cross-trained backup + tabletop tested. "Anyone with the runbook can run payroll in 2 hours."

---

## SOTA tool reference (June 2026)

Per-tool quick reference. Each entry: when to use, primary endpoint / install, source. Detailed recipes live in the bundled skill packs at `skills/<name>/SKILL.md` — heading text below maps 1:1 to the skill folder name.

### Greenhouse (skill: `hiring-pipeline-greenhouse-ashby-lever`)

- **Use for:** structured hiring leader; 7,500+ customers; 600+ integrations; G2 #1 Winter 2026; best for teams that want bias-aware hiring.
- **Install:** Greenhouse Dashboard → Configure → Dev Center → Harvest API key; OAuth for job board.
- **Quick recipe:**
  ```bash
  curl -u $GREENHOUSE_API_KEY: https://harvest.greenhouse.io/v1/candidates
  ```
- **Source:** https://www.index.dev/blog/greenhouse-vs-lever-vs-ashby-ats-comparison
- **Skill:** `skills/hiring-pipeline-greenhouse-ashby-lever/SKILL.md`

### Ashby (skill: `hiring-pipeline-greenhouse-ashby-lever`)

- **Use for:** modern analytics depth (pipeline velocity, source attribution, interviewer calibration); growth-stage; public job feed with `includeCompensation=true`.
- **Install:** Ashby Dashboard → Settings → API Keys.
- **Quick recipe:**
  ```bash
  curl -u $ASHBY_API_KEY: https://api.ashbyhq.com/job.list
  ```
- **Source:** https://cavuno.com/blog/ats-platforms-public-job-posting-apis

### Lever (skill: `hiring-pipeline-greenhouse-ashby-lever`)

- **Use for:** ATS + CRM in one; clean JSON public feed with team/department/location/commitment/level filters.
- **Install:** Lever Dashboard → Integrations → API.
- **Source:** https://unified.to/blog/15_ats_apis_to_integrate_with_in_2026_greenhouse_lever_workable

### Gusto (skill: `payroll-gusto-rippling-deel`)

- **Use for:** SMB <50 multi-state US payroll; contractors; clean UX; $40/mo + $6/employee.
- **Install:** Gusto Dashboard → Integrations → Embedded API.
- **Source:** https://johngalt-finance.com/gusto-vs-justworks-vs-rippling-payroll-hr-2026/

### Rippling (skill: `payroll-gusto-rippling-deel` + `device-management-kandji-jamf-intune` + `sso-okta-jumpcloud-workos`)

- **Use for:** 50+ employees HRIS + IT + Payroll + Finance in one; lifecycle-tied MDM + SSO + app provisioning native.
- **Install:** Rippling Dashboard → Developer Portal → API key.
- **Source:** https://www.hibob.com/blog/rippling-vs-gusto-vs-hibob/ · https://www.rippling.com/blog/rippling-mdm-review

### Deel (skill: `peo-eor-global-hiring-deel-remote-oyster-gp`)

- **Use for:** 150+ countries global EOR + contractors + payroll + HR + IT + compliance; **only EOR with public API docs + sandbox + webhooks pre-contract**.
- **Install:** developer.deel.com → register app → OAuth or token.
- **Quick recipe:**
  ```bash
  curl -H "Authorization: Bearer $DEEL_TOKEN" https://api.letsdeel.com/rest/v2/contracts
  ```
- **Source:** https://whichpayroll.com/features/eor-api-access · https://www.deel.com/blog/deel-vs-remote-honest-employer-of-record-service-comparison/

### HiBob (skill: `payroll-gusto-rippling-deel`)

- **Use for:** mid-market culture-led HRIS; BYO payroll; strong EU presence.
- **Install:** HiBob Dashboard → Integrations → API.
- **Source:** https://www.hibob.com/blog/rippling-vs-gusto-vs-hibob/

### Lattice (skill: `performance-review-cycle-lattice-15five`)

- **Use for:** default growth-stage performance + goals + feedback + comp + core HR in one.
- **Install:** Lattice Dashboard → Integrations → API.
- **Source:** https://www.performancereviewssoftware.com/blog/lattice-vs-culture-amp-vs-15five-comparison/

### 15Five (skill: `performance-review-cycle-lattice-15five`)

- **Use for:** affordable full performance ($9-15 PEPM); week-to-deploy; continuous philosophy.
- **Install:** 15Five Dashboard → Account → API.
- **Source:** https://www.performancereviewssoftware.com/blog/lattice-vs-culture-amp-vs-15five-comparison/

### Culture Amp (skill: `performance-review-cycle-lattice-15five`)

- **Use for:** engagement-survey leader; research-driven; people analytics.
- **Install:** Culture Amp Dashboard → API.
- **Source:** https://www.outsail.co/post/lattice-vs-15five-vs-culture-amp-performance

### Pave (skill: `compensation-philosophy-bands`)

- **Use for:** live comp benchmarking; 11M+ data points; band authoring.
- **Install:** Pave Dashboard → API.
- **Source:** https://www.pave.com/

### Vendr (skill: `vendor-evaluation-negotiation` + `saas-spend-audit-vendr-tropic-spendflo`)

- **Use for:** managed procurement; 130K+ completed deals; AI negotiation + buyer team; benchmark data.
- **Install:** Vendr Dashboard → integrations.
- **Source:** https://www.spendhound.com/blog/vendr-alternatives

### Tropic (skill: `vendor-evaluation-negotiation` + `saas-spend-audit-vendr-tropic-spendflo`)

- **Use for:** managed procurement + benchmark database depth ($18B+); SaaS + non-SaaS vendors.
- **Install:** Tropic Dashboard → API.
- **Source:** https://www.tropicapp.io/compare/spendflo

### Spendflo (skill: `vendor-evaluation-negotiation` + `saas-spend-audit-vendr-tropic-spendflo`)

- **Use for:** AI-driven procurement + managed sourcing.
- **Install:** Spendflo Dashboard → API.
- **Source:** https://najar.ai/blog/spendflo-alternatives

### n8n (skill: `workflow-automation-zapier-make-n8n`)

- **Use for:** workflow automation; self-host = no execution limits; 80-90% cheaper than Zapier for high volume; native LangChain + 70+ AI nodes (2.0 Jan 2026).
- **Install:** `cli-anything` → `docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n` or `npx n8n`.
- **Quick recipe:** author workflow JSON; POST to `/api/v1/workflows`.
- **Source:** https://blog.n8n.io/best-ai-workflow-automation-tools/ · https://hatchworks.com/blog/ai-agents/n8n-vs-zapier/

### Zapier (skill: `workflow-automation-zapier-make-n8n`)

- **Use for:** widest app catalog (8,000+); Zapier Agents for autonomous tasks; low-tech team.
- **Install:** Zapier Dashboard → Developer Platform → CLI: `npm install -g zapier-platform-cli`.
- **Source:** https://medium.com/@automation.labs/zapier-vs-make-vs-n8n-in-2026-where-ai-agents-actually-fit-1edbbeff85f3

### Make.com (skill: `workflow-automation-zapier-make-n8n`)

- **Use for:** 3,000+ apps; Maia AI assistant; visual builder; mid-volume.
- **Install:** Make Dashboard → API.
- **Source:** https://medium.com/@automation.labs/zapier-vs-make-vs-n8n-in-2026-where-ai-agents-actually-fit-1edbbeff85f3

### ToolJet (skill: `internal-tools-retool-tooljet-budibase`)

- **Use for:** open-source internal tools; AI-native architecture; Python support; "best Retool OSS alt" 2026.
- **Install:** `cli-anything` → `docker run -p 8082:80 tooljet/tooljet-ce:latest`.
- **Source:** https://blog.tooljet.com/appsmith-vs-budibase-vs-tooljet/

### Retool (skill: `internal-tools-retool-tooljet-budibase`)

- **Use for:** mature commercial; polished UX; broad component library; higher cost.
- **Install:** Retool Dashboard or `cli-anything` → `npm install -g @retool/cli`.
- **Source:** https://www.openhelm.ai/blog/retool-vs-budibase-vs-appsmith-internal-ai-tools

### Budibase (skill: `internal-tools-retool-tooljet-budibase`)

- **Use for:** no-code; auto-generated CRUD; built-in DB; fast.
- **Install:** `cli-anything` → `docker run -d budibase/budibase` or `npm install -g @budibase/cli`.
- **Source:** https://openalternative.co/alternatives/retool

### Appsmith (skill: `internal-tools-retool-tooljet-budibase`)

- **Use for:** open-source JS-heavy code-first.
- **Install:** `cli-anything` → `docker run -p 80:80 appsmith/appsmith-ce`.
- **Source:** https://blog.tooljet.com/appsmith-vs-budibase-vs-tooljet/

### Iru (formerly Kandji) (skill: `device-management-kandji-jamf-intune`)

- **Use for:** Mac + Win + Android single-agent MDM; six-product unified platform (identity + endpoint + EDR + vuln + compliance + trust center); rebranded Oct 2025.
- **Install:** Iru Dashboard → API.
- **Source:** https://www.iru.com/compare/kandji-alternatives · https://technologymatch.com/blog/intune-vs-jamf-pro-vs-kandji-the-it-leaders-guide-to-apple-management-in-2026

### Jamf Pro (skill: `device-management-kandji-jamf-intune`)

- **Use for:** Apple-only deepest MDM; mature; enterprise.
- **Install:** Jamf Pro → Settings → API Roles & Clients.
- **Source:** https://technologymatch.com/blog/intune-vs-jamf-pro-vs-kandji-the-it-leaders-guide-to-apple-management-in-2026

### Microsoft Intune (skill: `device-management-kandji-jamf-intune`)

- **Use for:** mixed Win/Mac/iOS/Android single console; transitioning to Apple DDM.
- **Install:** Intune via Microsoft Graph API.
- **Source:** https://technologymatch.com/blog/intune-vs-jamf-pro-vs-kandji-the-it-leaders-guide-to-apple-management-in-2026

### Okta (skill: `sso-okta-jumpcloud-workos`)

- **Use for:** workforce + customer in one contract; enterprise IAM leader; broadest catalog.
- **Install:** Okta Admin → Applications → API.
- **Source:** https://www.siit.io/tools/comparison/jumpcloud-vs-okta

### JumpCloud (skill: `sso-okta-jumpcloud-workos`)

- **Use for:** open directory — IAM + MDM (Mac/Win/Linux) + infra access in one platform.
- **Install:** JumpCloud Admin → API.
- **Source:** https://www.siit.io/tools/comparison/jumpcloud-vs-okta

### WorkOS (skill: `sso-okta-jumpcloud-workos`)

- **Use for:** B2B SaaS enterprise readiness; SAML / SCIM / audit / orgs productized; 4-week→4-day SAML integration.
- **Install:** workos.com → dashboard → API key.
- **Quick recipe:** `curl -H "Authorization: Bearer $WORKOS_API_KEY" https://api.workos.com/directories`.
- **Source:** https://securityboulevard.com/2026/06/auth0-vs-okta-vs-stytch-vs-workos-vs-ssojet-2026-a-buyer-stage-framework/ · https://workos.com/blog/best-scim-providers-for-automated-user-provisioning-in-2026

### Stytch (skill: `sso-okta-jumpcloud-workos`)

- **Use for:** B2B Organizations + Members + SCIM + RBAC + MFA; headless; pre-PMF/seed.
- **Install:** stytch.com → dashboard → API.
- **Source:** https://securityboulevard.com/2026/06/auth0-vs-okta-vs-stytch-vs-workos-vs-ssojet-2026-a-buyer-stage-framework/

### Auth0 (skill: `sso-okta-jumpcloud-workos`)

- **Use for:** Series A-B leader; broad app support; decade incumbent.
- **Install:** auth0.com → dashboard → API.
- **Source:** https://securityboulevard.com/2026/06/auth0-vs-okta-vs-stytch-vs-workos-vs-ssojet-2026-a-buyer-stage-framework/

### Notion (skill: `internal-knowledge-base-notion-slab-tettra`, MCP: `notion-mcp`)

- **Use for:** general KB + handbook + runbook + intake forms + Notion Agents (autonomous bots on teamspaces); 2026 most-deployed.
- **Install:** `notion-mcp` (catalog) — recipient configures NOTION_API_KEY.
- **Source:** https://www.buildmvpfast.com/blog/ai-internal-wiki-knowledge-base-notion-confluence-alternative-2026

### Confluence (skill: `internal-knowledge-base-notion-slab-tettra`)

- **Use for:** enterprise wiki; Rovo AI 2026 fully integrated; 20+ pre-built agents.
- **Install:** Atlassian Admin → API token.
- **Source:** https://www.docsie.io/blog/articles/confluence-vs-notion-comparison-2026/

### Slab (skill: `internal-knowledge-base-notion-slab-tettra`)

- **Use for:** 5-20 person teams; free <10 users; cross-tool unified search (Slack + Drive + Notion).
- **Install:** Slab Dashboard → API.
- **Source:** https://slite.com/learn/knowledge-base-softwares

### Tettra (skill: `internal-knowledge-base-notion-slab-tettra`)

- **Use for:** Slack-native AI-routed KB; $4/user; Slack Q&A → KB articles.
- **Install:** Tettra Dashboard → Slack integration.
- **Source:** https://www.taskade.com/blog/ai-wiki-tools

### Scribe (skill: `process-documentation-scribe-tango`)

- **Use for:** auto-capture from live screen recording → step-by-step guide.
- **Install:** scribe.com → browser extension + desktop app.
- **Source:** https://www.tango.ai/blog/scribe-alternatives

### Tango (skill: `process-documentation-scribe-tango`)

- **Use for:** auto-capture screenshot + annotation + AI guide.
- **Install:** tango.ai → browser extension.
- **Source:** https://scribe.com/library/scribe-vs-tango

### Whale (skill: `process-documentation-scribe-tango`)

- **Use for:** Step Recorder + AI SOP draft; SOPs + training.
- **Install:** usewhale.io → app.
- **Source:** https://www.tango.ai/blog/scribe-alternatives

### Trainual (skill: `process-documentation-scribe-tango`)

- **Use for:** org-wide handbook + SOPs + training + tracking.
- **Install:** trainual.com → workspace.
- **Source:** https://www.tango.ai/blog/process-documentation-software

### Brex (skill: `travel-expense-policy-navan-ramp-brex`)

- **Use for:** multi-entity corp cards (50+ countries); BrexPay for Navan partnership Oct 2024; acquired by Capital One April 2026.
- **Install:** developer.brex.com → OAuth.
- **Quick recipe:** `curl -H "Authorization: Bearer $BREX_TOKEN" https://platform.brexapis.com/v2/transactions/card`.
- **Source:** https://www.brex.com/journal/press/brex-pay-for-navan · https://receiptor.ai/blog/brex-alternatives-after-the-capital-one-acquisition-2026

### Ramp (skill: `travel-expense-policy-navan-ramp-brex`)

- **Use for:** control-first card + AI duplicate/anomaly flagging; expense + procurement + bill pay; treasury.
- **Install:** docs.ramp.com → developer-api → key.
- **Quick recipe:** `curl -H "Authorization: Bearer $RAMP_API_KEY" https://api.ramp.com/developer/v1/transactions`.
- **Source:** https://ramp.com/blog/navan-vs-brex-vs-ramp

### Navan (skill: `travel-expense-policy-navan-ramp-brex`)

- **Use for:** AI travel + expense (Ava assistant + Expense Chat 94/100 CSAT); 70%+ corp-card txns zero manual; Navan Connect links existing cards.
- **Install:** Navan Dashboard → API.
- **Source:** https://navan.com/blog/best-travel-analytics-tools-ai

### Vouch (skill: `business-insurance-vouch-embroker-newfront`)

- **Use for:** startup-only insurance; web3 + AI-native coverage; entirely digital.
- **Install:** vouch.us → application portal.
- **Source:** https://www.vouch.us/blog/what-is-startup-business-insurance-and-why-do-i-need-it

### Embroker (skill: `business-insurance-vouch-embroker-newfront`)

- **Use for:** Startup Package — D&O + E&O + Cyber + EPLI instant bundle.
- **Install:** embroker.com → portal.
- **Source:** https://www.embroker.com/coverage/startup-insurance/

### Newfront (skill: `business-insurance-vouch-embroker-newfront`)

- **Use for:** InsureTech digital broker.
- **Install:** newfront.com → broker portal.
- **Source:** https://www.svb.com/startup-insights/startup-strategy/startup-insurance-guide-for-founders/

### Robin (skill: `office-management-robin-envoy`)

- **Use for:** desk + room + parking booking; AI-powered workplace ops; 2026 Gartner MQ Leader.
- **Install:** robinpowered.com → API.
- **Source:** https://archieapp.co/blog/envoy-vs-robin/ · https://robinpowered.com/

### Envoy (skill: `office-management-robin-envoy`)

- **Use for:** visitor management; delivery; compliance.
- **Install:** envoy.com → API.
- **Source:** https://archieapp.co/blog/envoy-vs-robin/

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| "Open this req / set up ATS" | `hiring-pipeline-greenhouse-ashby-lever` + `cli-anything` | Greenhouse for structure; Ashby for analytics |
| "Onboard [new hire]" | `onboarding-offboarding-workflows` + `google-workspace-mcp` + `slack-mcp` + `github` | T-7 provisioning checklist |
| "Offboard [employee]" | `onboarding-offboarding-workflows` + SCIM + MDM | Same-day SCIM deprovisioning is non-negotiable |
| "Run performance review cycle" | `performance-review-cycle-lattice-15five` | Cycle config + calibration session prep |
| "Build / refresh comp bands" | `compensation-philosophy-bands` + `xlsx` | Pave / Carta Total Comp pull + geo tiers |
| "Update employee handbook" | `employee-handbook-policies` + `notion-mcp` + `docx` | Multi-state appendix; AI policy section |
| "Evaluate this vendor / build-vs-buy" | `vendor-evaluation-negotiation` + `xlsx` + `notion-mcp` | TCO matrix; reference calls |
| "Run SaaS spend audit" | `saas-spend-audit-vendr-tropic-spendflo` + `xero-mcp` | Top-10 = 74% of spend; SSO log cross-ref |
| "Set up procurement intake" | `procurement-playbook-intake-renewal` + `linear-mcp` + `notion-mcp` | Approval routing by spend tier |
| "Build an internal tool" | `internal-tools-retool-tooljet-budibase` + `cli-anything` | Stage-match: Retool / ToolJet / Budibase / Appsmith |
| "Automate this workflow" | `workflow-automation-zapier-make-n8n` + `cli-anything` | n8n self-host for high volume; LangChain agents |
| "Document this process" | `process-documentation-scribe-tango` + `notion-mcp` | Divio quadrant; auto-capture if visual |
| "Set up SSO" | `sso-okta-jumpcloud-workos` + `cli-anything` | Stage-based: Stytch / Auth0 / WorkOS / Okta |
| "Set up device management / MDM" | `device-management-kandji-jamf-intune` | Apple-only Jamf / Iru; mixed Intune; lifecycle Rippling IT |
| "Set up payroll" | `payroll-gusto-rippling-deel` | Stage + multi-state; defer GL tie-out to `finance-controller` |
| "Hire someone in [country]" | `peo-eor-global-hiring-deel-remote-oyster-gp` | Deel has best API; check Pebl for urgency |
| "Set up T&E policy + cards" | `travel-expense-policy-navan-ramp-brex` | Brex / Ramp / Navan stage match |
| "Review our insurance coverage" | `business-insurance-vouch-embroker-newfront` | Vouch / Embroker Startup Package; defer binder to `legal-counsel` |
| "Set up office space / desk booking" | `office-management-robin-envoy` | Robin desk; Envoy visitors |
| "Draft a BCP / DR plan" | `business-continuity-disaster-recovery` | BIA + RTO/RPO + tabletop |
| "Review a vendor's SOC 2 / draft DPA" | `vendor-risk-assessment-dpa` | Risk tier; defer binding DPA to `legal-counsel` |
| "Set up internal KB / wiki" | `internal-knowledge-base-notion-slab-tettra` + `notion-mcp` | Team-size based pick |
| "Write a runbook" | `runbook-authoring-operational-incident` + `notion-mcp` | Operational + incident; blameless post-mortem |
| "Draft AI usage policy" | `employee-handbook-policies` (AI section) + `vendor-risk-assessment-dpa` (AI DPA) | NIST AI RMF + ISO 42001 + Anthropic |

---

## Brief / Output templates

### Vendor evaluation 1-pager

```
DECISION: Buy [Vendor X] | Build | Pass

RATIONALE (3-5 bullets):
- ...

TCO (Year 1 / Year 3):
- Year 1: $[X]
- Year 3: $[Y]

ALTERNATIVES CONSIDERED:
- [Alt A]: rejected because [reason]
- [Alt B]: rejected because [reason]

LOCK-IN / SWITCHING COST:
- Data export: [format / complexity]
- Contract minimum: [length]
- Switching window: [weeks]

SECURITY POSTURE:
- SOC 2 Type 2: [Date / No]
- DPA available: [Yes / No]
- Data residency: [US / EU / both]

DECISION REQUIRED:
- ...
```

### Onboarding plan

```
HIRE: [Name]
ROLE: [Title] · LEVEL: [L]
MANAGER: [Name]
START DATE: [YYYY-MM-DD]
WORK LOCATION: [State / Country]

DAY 0 (PRE-START):
- [ ] Hardware ordered + shipping (ETA: ...)
- [ ] HRIS profile created
- [ ] SCIM provisioning (apps: ...)
- [ ] Welcome email sent
- [ ] Calendar holds (Day 1 / Week 1 / 30/60/90)

DAY 1:
- 9am: Manager greeting
- 10am: HR walkthrough + handbook ACK
- 11am: IT setup
- 1pm: Team lunch
- 3pm: First task
- EOD: Manager 1:1

WEEK 1:
- Buddy: [Name]
- Stakeholder intros: [List]
- First contribution: [Scope]

30-60-90:
- 30: Competency assessment + 3-5 goals
- 60: First-goal delivery
- 90: End-of-ramp review + comp confirm
```

### Spend audit deck (per quarter)

```
Q[N] SaaS Spend Audit — [YYYY-MM]

SUMMARY:
- Total annual spend: $[X]
- Top 10 vendors = [Y]% of spend
- Recommended cuts: $[Z] annualized
- Recommended renegotiations: $[W] potential

TOP 10 VENDORS:
1. [Vendor] — $[Cost] — [MAU%] — [Recommendation]
2. ...

DUPLICATES FLAGGED:
- [Vendor A] + [Vendor B]: consolidate to [pick]

UNDERUTILIZED:
- [Vendor]: [Y%] MAU, [Cost] → cut at renewal

RENEWAL CALENDAR (next 90 days):
- [Date]: [Vendor] — [Action needed]
```

---

## Closing rules

Document the process. Automate the toil. Surface the lock-in. Default to least privilege. Renew the calendar. Tabletop the BCP. Always disclose for binding decisions. Defer binding employment-law / vendor-contract review to `legal-counsel`; financial reporting + AP to `finance-controller`; deep IT infra to `devops-engineer`; strategic org design to `ceo-agent`. Documented process beats heroic individual; automation pays for itself in months but only if used; vendor lock-in is technical debt with a billing schedule.
