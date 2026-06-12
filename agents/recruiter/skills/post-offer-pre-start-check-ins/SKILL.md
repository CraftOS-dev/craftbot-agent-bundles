<!--
Sources: https://www.greenhouse.io/onboarding
         https://www.enboarder.com/
         https://www.kallidus.com/blog/preboarding/
2026 renege data: 25-30% senior-hire renege rate without pre-start touch; drops to 5-10% with
weekly touch + pre-boarding + buddy. Day-1 readiness handed to operations-agent.
-->
# Post-Offer Pre-Start Check-Ins — SKILL

Run the offer-accepted-to-Day-1 dead zone where 25-30% of senior hires renege. Weekly touch cadence, pre-boarding kit, buddy assignment, Day-1 readiness checklist, manager 30-60-90 plan, counter-offer recapture protocol. Day-1 onboarding execution defers to `operations-agent`.

## When to use

- Offer accepted; start date 14-90 days out (especially senior+ with high counter-offer risk).
- Sentiment check at any silence signal (no response to weekly touch).
- Pre-boarding kit assembly.
- Trigger phrases: "pre-start check-in", "post-offer", "pre-boarding", "renege risk", "candidate stalled", "Day-1 readiness", "buddy assignment", "counter-offer recapture".
- Defer to `operations-agent`: Day-1 execution (laptop, accounts, badges, I-9, payroll), 30-60-90 plan delivery, benefits enrollment.

## Setup

```bash
# ATS
export GREENHOUSE_API_KEY="harvest_xxx"
export GH_USER_ID="123456"

# Onboarding platform (optional, recipient-paid)
export GREENHOUSE_ONBOARDING_API_KEY="xxx"
export SAPLING_API_KEY="xxx"                # https://www.sapling.com/
export ENBOARDER_API_KEY="xxx"              # https://www.enboarder.com/

# Comms
export SLACK_BOT_TOKEN="xoxb-xxx"
export GMAIL_OAUTH_TOKEN="<bearer>"

# Calendar for touch cadence + Day-1 setup
export GOOGLE_CAL_OAUTH="<bearer>"

# Pre-boarding kit asset host
export GOOGLE_DRIVE_OAUTH="<bearer>"
```

Auth model: ATS basic-auth. Sapling / Enboarder / Greenhouse Onboarding are paid SaaS layered on top of ATS.

## Common recipes

### Recipe 1: Schedule weekly touch cadence (google-calendar-mcp)
```python
# google-calendar-mcp insert recurring 15-min check-ins
import datetime
start = datetime.date(2026, 6, 15)   # offer accept date
end = datetime.date(2026, 8, 1)      # day 1 date
weeks = (end - start).days // 7
for w in range(weeks):
  touch_date = start + datetime.timedelta(weeks=w)
  # alternate: recruiter (week 1, 3, 5) + manager (week 2, 4, 6)
  who = "recruiter@acme.com" if w % 2 == 0 else "hm@acme.com"
  event = {
    "summary": f"Pre-start check-in — {who.split('@')[0]} + {{candidate_name}}",
    "start": {"date": touch_date.isoformat()},
    "end": {"date": touch_date.isoformat()},
    "attendees": [{"email": who}, {"email": "{candidate_email}"}]
  }
  # google_calendar.events.insert(...)
```

### Recipe 2: Pre-boarding kit content (notion-mcp + Drive)
```markdown
# Pre-boarding Kit — {candidate_name}

## Welcome
- Video from CEO / manager (3-5 min)
- Personal note from manager + buddy
- Logo-merch ship to home address (T-2 weeks)

## Logistics
- First-day calendar (10am intro coffee + 11am team standup + 12pm lunch + 2pm manager 1:1 + 4pm 1:1 with buddy)
- Office address + parking + bike room (if hybrid)
- Laptop shipping address + ETA
- Communication tools: Slack join link, Zoom test link

## Background reading
- 5-page company overview (mission, strategy, current bets, recent wins)
- Team intro: each direct report's 1-paragraph bio
- Manager's leadership philosophy doc
- 30-60-90 plan (manager-drafted)
- Q4 OKRs

## FAQ
- Benefits enrollment (deferred to operations-agent)
- PTO accrual + policy
- Office hours / work-from-anywhere policy
- Code of conduct
- Anti-harassment policy

## Buddy
- Name + role + LinkedIn
- Why they were picked: "{specific match reason}"

## Contact
- Recruiter (you) + manager + ops contact
- "Anything weird? Text recruiter."
```

### Recipe 3: Buddy assignment (peer-level, not manager)
```text
Buddy criteria:
- Peer-level (same or +/- 1 level)
- Same function NOT same team (cross-functional perspective)
- 12-24 months tenure (long enough to know systems; recent enough to remember new-hire pain)
- Volunteer (not assigned without consent — bad buddy = bad signal)

Buddy commitment:
- Weekly 30-min 1:1 for first 90 days
- Slack DM available
- "Stupid questions go here" channel for new hire

Compensation:
- L&D / spot-bonus / public recognition; companies vary
- Buddy training (1h workshop on what to do + what NOT to do)
```

### Recipe 4: Counter-offer recapture protocol
```text
Signal: candidate goes quiet 1-2 weeks before start.

Step 1 (recruiter): personal phone call within 24h (NOT email; phone forces honesty).
"Hi Sarah, just wanted to check in. Everything good with start prep?"
LISTEN for "I need to talk to you about..." → counter-offer is happening.

Step 2 (recruiter, IF counter): 30-min recruiter call same day.
- Acknowledge: "I get why this is hard."
- Reframe value: "You chose us for X, Y, Z. Has anything changed?"
- Surface specifics: "What did they offer? What would close this for you?"

Step 3 (manager + CEO if exec): involve more senior + emotional case.
- Manager: "What's the 12-month trajectory we promised? Still excited about it?"
- CEO (exec only): "I think you'd build something meaningful here."

Step 4 (offer adjustment IF warranted): only if clear we under-offered or candidate has new info.
- Don't bid blindly; don't get bid up. ~5-10% adjustments OK; 25%+ counter offers signal misalignment.

Step 5 (let them go gracefully IF they go): 
- "We get it. Reconnect in 18 months. Cal reminder set."
- Move offer slot to next-best candidate within 48h.
```

### Recipe 5: Day-1 readiness checklist coordination (with operations-agent)
```text
T-14 days:
[ ] Laptop ordered + shipping to candidate
[ ] Software licenses provisioned (Greenhouse Onboarding / Sapling auto-trigger)
[ ] Workplace badge ordered (if applicable)
[ ] Email + calendar created (handed to ops-agent)
[ ] Slack added + manager + team channels invited
[ ] Manager + team Day-1 calendar built

T-7 days:
[ ] Pre-boarding kit delivered (Recipe 2)
[ ] Buddy assigned + introduced (Recipe 3)
[ ] 30-60-90 plan draft from manager
[ ] I-9 instructions sent (in-person verification on Day 1; remote: USCIS-approved authorized representative)

T-2 days:
[ ] Personal note from CEO / VP / manager (1-2 sentences; human touch)
[ ] Logistics confirmation (laptop received? Any blockers?)

T-1 day:
[ ] Recruiter check-in: "Excited for tomorrow? Any final blockers?"
[ ] Manager confirmation: "Day-1 calendar ready; team prepped"

Day 0:
[ ] Welcome email from CEO to all-hands announcing new hire (with role + buddy + manager intro)
```

### Recipe 6: Greenhouse Onboarding handoff
```bash
# Greenhouse Onboarding auto-fires when application moves to "hired"
# Triggers: welcome packet email, I-9 prep, software provisioning workflows
curl -s -X PATCH -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -H "Content-Type: application/json" \
  "https://harvest.greenhouse.io/v1/applications/<app_id>" \
  -d '{"status": "hired"}'
# Onboarding events ATS → operations-agent for execution.
```

### Recipe 7: Sapling pre-boarding workflow
```bash
curl -s -X POST -H "Authorization: Bearer $SAPLING_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.sapling.com/v1/employees" \
  -d '{
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane@example.com",
    "start_date": "2026-08-01",
    "workflow_template_id": "<pre_boarding_template>"
  }'
```

### Recipe 8: Enboarder candidate-journey campaign
```bash
curl -s -X POST -H "Authorization: Bearer $ENBOARDER_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.enboarder.com/v2/journeys" \
  -d '{
    "candidate_id": "<id>",
    "journey_template_id": "<pre_boarding_journey>",
    "start_date": "2026-08-01"
  }'
# Journeys = bite-sized content + reminders over 4-8 weeks pre-start
```

### Recipe 9: Renege risk flagging (sentiment loop)
```python
# Pull weekly touch responses; flag silence + concerning language
patterns = ["second thoughts", "competing offer", "counter offer", "ladders", "renege", "thinking about"]
# In gmail-mcp / slack-mcp transcripts, classify last 7 days touch responses
# Flag escalation criteria:
# - 2+ missed touches → recruiter phone call (Recipe 4)
# - Pattern match → emergency reach-out + manager loop-in
# - Day-3 silence pre-start → manager + CEO call
```

### Recipe 10: 30-60-90 plan draft (manager owns; recruiter facilitates)
```markdown
# 30-60-90 Plan — {new_hire} as {role}

## Days 0-30: Ramp
- Meet all direct reports + immediate stakeholders
- Read: codebase / playbook / Q4 OKRs / customer interviews
- Ship: 1-2 small low-risk fixes ("first commit" / "first ticket close")
- 1:1 cadence: weekly with manager, weekly with skip-level

## Days 31-60: Contribute
- Own 1 mid-size project end-to-end
- Identify 1-2 process improvements + propose
- Become go-to for at least 1 system / area
- Cross-functional: meet 2-3 partner-org leads

## Days 61-90: Lead
- Own a workstream that affects the team (release, on-call, hiring loop)
- Mentor someone (intern, contractor, junior IC)
- Self-review + manager review (calibration)
- Propose 90-180 day roadmap

## Sign-off
- New hire: ___
- Manager: ___
- Recruiter: ___ (for retention follow-up at 30 / 60 / 90)
```

### Recipe 11: Recruiter retention follow-up (post Day-1)
```text
Recruiter owns 30 / 60 / 90 day check-ins post-start (handing performance ownership to manager):
- Day 30: 30-min coffee. "What's working? What's surprising? Anything we got wrong?"
- Day 60: 30-min. "How are you feeling about the role + manager + team?"
- Day 90: 30-min. "Would you recommend Acme to a friend? Would you do it again?"

Signal: any 90-day attrition is a recruiter feedback loop — what could the loop have surfaced earlier?
```

### Recipe 12: All-hands intro email + announcement
```text
[All-hands email, T-1 day before Day 1]
Subject: Welcome {first_name} to {team}!

Hi everyone,
I'm thrilled to welcome {first_name} {last_name} to Acme as {title} on {team}, starting tomorrow.

{1-line about why we're excited about them}.

{first_name} comes to us from {prior_company} where they {1-sentence about impact}. 
They'll be working with {team_members}, reporting to {manager}. 
Their buddy for the first 90 days will be {buddy_name}.

Please join me in welcoming {first_name}! Feel free to DM them a welcome.
{CEO_name}
```

## Examples

### Example 1: Senior IC offer accepted T-45 days; counter-offer happens
**Goal:** Prevent renege.
**Steps:**
1. Recipe 1 schedules weekly touches.
2. Week 3 touch: candidate quiet. Recipe 4 phone call.
3. Counter-offer revealed ($40K higher).
4. Manager + recruiter joint call: reaffirm scope + 12-month trajectory + 5% comp adjustment.
5. Candidate stays.

**Result:** Renege prevented; relationship strengthened.

### Example 2: New-hire pre-boarding kit for Engineer with T-60 days start
**Goal:** Kit delivered by T-14 days.
**Steps:**
1. Recipe 2: assemble in Drive + send to ops-agent for distribution.
2. Recipe 3: assign buddy (peer in adjacent team, 18-mo tenure).
3. Recipe 6: trigger Greenhouse Onboarding workflow.
4. Recipe 10: manager drafts 30-60-90.
5. Day-1 ready per Recipe 5.

**Result:** Smooth first day; new hire integrated by Day 2.

### Example 3: 90-day retention check
**Goal:** Did we predict this hire's success?
**Steps:**
1. Recipe 11 at Day 30 / 60 / 90.
2. Day 90: hire reports strong manager + buddy + scope; recommends Acme.
3. Pulled into recruiter retro: what predicted success? Adjust loop accordingly.

**Result:** Recruiting feedback loop; reduce future-hire risk.

## Edge cases / gotchas

- **Silence ≠ trouble (but often is).** 1 missed touch = give grace + email. 2 missed = phone. 3 missed = manager + recruiter joint call.
- **Counter-offer recapture timing.** 24-48h is golden; beyond 72h candidate has emotionally accepted counter.
- **Comp adjustment is not a magic answer.** If candidate's reservation is non-monetary (role scope, team, manager), bumping comp doesn't help. Recipe 4 step 2: surface the actual concern.
- **Buddy mismatch.** Bad buddy = worse than no buddy. Volunteer-only + brief vetting.
- **Pre-boarding kit fatigue.** Too much content T-14 days → ignored. Bite-sized + sequenced (T-14, T-7, T-2, Day-0).
- **Personal home address.** Laptop shipping needs home address; logistics-only. Don't surface for other systems.
- **Visa applicants.** International candidates may have visa-induced delays (start date slips); communicate proactively.
- **Office vs remote.** Hybrid / remote Day-1 logistics differ; tailor checklist.
- **Day-1 calendar over-stuffing.** 4-5 meetings is the max for Day 1. Otherwise overwhelm.
- **Manager unavailability on Day 1.** Reschedule pre-start if manager is OOO Day 1; alternative: skip-level fills in.
- **Internal moves.** Lower pre-boarding intensity (employee already onboarded once); focus on team-integration not company-onboarding.
- **Defer to `operations-agent`** for: Day-1 execution (laptop, badges, accounts, I-9, payroll setup, benefits enrollment), 30-60-90 manager facilitation, attrition data tracking.
- **Defer to `legal-counsel`** for: visa-induced timing changes, I-9 deadline (3-business-day rule strict), benefits eligibility waiting periods.

## Sources

- [Greenhouse Onboarding](https://www.greenhouse.io/onboarding)
- [Enboarder](https://www.enboarder.com/)
- [Sapling](https://www.sapling.com/)
- [Kallidus — Preboarding research](https://www.kallidus.com/blog/preboarding/)
- [SHRM — Onboarding new hires research](https://www.shrm.org/topics-tools/news/talent-acquisition/onboarding-key-retaining-engaging-talent)
- [LinkedIn Talent Solutions — Renege Rates 2025](https://business.linkedin.com/talent-solutions)
- [Form I-9 timing (USCIS)](https://www.uscis.gov/i-9-central/complete-correct-form-i-9/completing-section-2-employer-review-and-attestation)
- [Glassdoor — pre-boarding best practices](https://www.glassdoor.com/employers/blog/pre-boarding-best-practices/)
