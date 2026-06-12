<!--
Sources:
User Interviews API — https://www.userinterviews.com/api
Respondent API — https://respondent.io/help
dscout API — https://dscout.com/api
Prolific API — https://docs.prolific.com
-->
# Recruit: User Interviews + Respondent + dscout + Prolific — SKILL

Four-platform recruitment routing for UX research. Pick by study type: User Interviews for fast B2C/B2B; Respondent for B2B specialists (IT, healthcare, finance); dscout for mobile + diary + longitudinal; Prolific for academic + survey + behavioral-science panels. Every platform has REST APIs for project create, screener push, applicant review, and scheduling.

## When to use

- Recruiting 5-50+ participants for any research method.
- Routing by study type (B2C / B2B specialist / mobile / academic).
- Pushing screener + criteria + incentive to a panel via API.
- Monitoring applicant pipeline + accepting/rejecting before scheduling.

Trigger phrases: "recruit 5 founders", "find 30 healthcare professionals", "diary study panel", "academic survey panel", "panel for screen reader users", "compare User Interviews vs Respondent".

## Setup

```bash
# All four platforms below; recipient enables what they need
curl -fsSL "https://api.userinterviews.com/v1/me" -H "Authorization: Bearer $USER_INTERVIEWS_API_KEY"
curl -fsSL "https://api.respondent.io/v1/me"    -H "Authorization: Bearer $RESPONDENT_API_KEY"
curl -fsSL "https://dscout.com/api/v1/me"        -H "Authorization: Bearer $DSCOUT_API_KEY"
curl -fsSL "https://api.prolific.com/api/v1/users/me/" -H "Authorization: Token $PROLIFIC_API_TOKEN"
```

Auth:
- `USER_INTERVIEWS_API_KEY` — Researcher dashboard → API.
- `RESPONDENT_API_KEY` — Settings → Integrations.
- `DSCOUT_API_KEY` — Mission dashboard → Account → API.
- `PROLIFIC_API_TOKEN` — Workspace → Settings → API tokens.

## Platform routing matrix

| Study type | First choice | Why | Cost (typical) | Alt |
|---|---|---|---|---|
| B2C, fast (<2 weeks) | **User Interviews** | Largest consumer panel, fastest match | $50-150 / 60-min session | Respondent |
| B2B specialist (IT, finance, healthcare) | **Respondent** | Vetted professional panel | $150-400 / 60-min | dscout (slower B2B) |
| Mobile-first, longitudinal | **dscout** | Native mobile diary + missions | $300-1000 / 7-30 day mission | Indeemo |
| Academic, behavioral science, survey | **Prolific** | Academic-grade quality + ethics | £6-15 / 30-min survey | MTurk (legacy) |
| Accessibility (users with disabilities) | **Fable** (see `accessibility-research-with-disabilities`) | Vetted assistive-tech panel | $100-200 / session | AccessWorks |
| In-product intercept | **Ethnio** (see `screener-design-recruitment-criteria`) | Programmatic in-product banner | $249/mo + incentive | Typeform banner |
| In-house (existing customers) | Notion CRM + Gmail | Your panel, no platform fee | Incentive only | HubSpot/Klaviyo CRM |

## Common recipes

### Recipe 1: Create User Interviews project + push screener

```bash
# Step 1: Create the project
PROJECT_ID=$(curl -fsSL -X POST "https://api.userinterviews.com/v1/projects" \
  -H "Authorization: Bearer $USER_INTERVIEWS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Solo founder JTBD — Q3 2026",
    "session_type": "video_call",
    "session_duration_minutes": 60,
    "incentive_amount_cents": 10000,
    "target_participant_count": 12,
    "scheduling_url": "https://calendly.com/your-link"
  }' | jq -r '.id')

# Step 2: Push the screener (see screener-design-recruitment-criteria skill)
curl -X POST "https://api.userinterviews.com/v1/projects/$PROJECT_ID/screener" \
  -H "Authorization: Bearer $USER_INTERVIEWS_API_KEY" \
  -d @screener.json
```

### Recipe 2: Pull applicants + filter

```bash
curl -fsSL "https://api.userinterviews.com/v1/projects/$PROJECT_ID/applications?status=pending" \
  -H "Authorization: Bearer $USER_INTERVIEWS_API_KEY" \
| jq '.applications[] | select(.qualified == true) | {id, email, screener_responses}'
```

### Recipe 3: Accept / reject applicants

```bash
# Accept
curl -X POST "https://api.userinterviews.com/v1/applications/$APP_ID/accept" \
  -H "Authorization: Bearer $USER_INTERVIEWS_API_KEY" \
  -d '{"message": "Thanks! Please book a time at the link in your email."}'

# Reject
curl -X POST "https://api.userinterviews.com/v1/applications/$APP_ID/reject" \
  -H "Authorization: Bearer $USER_INTERVIEWS_API_KEY" \
  -d '{"reason": "criteria_not_met"}'
```

### Recipe 4: Respondent — B2B specialist recruit

```bash
# B2B specialist with strict criteria
curl -X POST "https://api.respondent.io/v1/projects" \
  -H "Authorization: Bearer $RESPONDENT_API_KEY" \
  -d '{
    "title": "Healthcare IT decision-makers — interview",
    "session_type": "video",
    "duration": 60,
    "honorarium_cents": 30000,
    "target_count": 8,
    "criteria": {
      "industry": ["healthcare", "hospital_system"],
      "role": ["cio", "vp_it", "director_it"],
      "company_size": ["501-5000", "5000+"],
      "decision_authority": ["primary_decision_maker", "key_influencer"]
    },
    "exclusions": {
      "industry": ["market_research", "ux_research"],
      "research_in_last_90_days": true
    }
  }'
```

### Recipe 5: dscout mission (diary study)

```bash
# 14-day mobile diary mission — see diary-studies-dscout-7-30-day for full flow
curl -X POST "https://dscout.com/api/v1/missions" \
  -H "Authorization: Bearer $DSCOUT_API_KEY" \
  -d '{
    "title": "Founder daily inbox check — 14 days",
    "duration_days": 14,
    "target_count": 12,
    "honorarium_cents": 50000,
    "criteria": {
      "role": ["founder", "ceo"],
      "company_stage": ["seed", "series_a"],
      "device": "ios_or_android_with_camera"
    },
    "prompts": [
      {"day": 0, "type": "onboarding", "text": "Show us your inbox right now."},
      {"day": 1, "type": "daily", "text": "How many emails did you check today? Show me one that mattered."},
      {"day": 14, "type": "reflection", "text": "What changed over the 2 weeks?"}
    ]
  }'
```

### Recipe 6: Prolific study create (survey)

```bash
curl -X POST "https://api.prolific.com/api/v1/studies/" \
  -H "Authorization: Token $PROLIFIC_API_TOKEN" \
  -d '{
    "name": "Inbox habits survey — Q3 2026",
    "description": "10-min survey on email check habits. £2.50 for participation.",
    "external_study_url": "https://yourtypeform.typeform.com/to/ABC123?PROLIFIC_PID={{%PROLIFIC_PID%}}&STUDY_ID={{%STUDY_ID%}}",
    "prolific_id_option": "url_parameters",
    "completion_codes": [{"code": "INBOX2026", "code_type": "COMPLETED"}],
    "total_available_places": 200,
    "estimated_completion_time": 10,
    "reward": 250,
    "filters": [
      {"filter_id": "current-country-of-residence", "selected_values": ["1", "8", "21"]},
      {"filter_id": "fluent-languages", "selected_values": ["1"]},
      {"filter_id": "employment-status", "selected_values": ["1", "5"]}
    ]
  }'
```

### Recipe 7: Multi-platform routing decision (pseudo-code)

```python
def pick_platform(study_type, segment, timeline_days, longitudinal_days):
    if segment == "accessibility_users_with_disabilities":
        return "fable"  # see accessibility skill
    if longitudinal_days >= 7:
        return "dscout"
    if study_type == "survey" and segment == "general_population":
        return "prolific"
    if segment in {"healthcare_it", "finance_compliance", "enterprise_buyer"}:
        return "respondent"
    if timeline_days <= 14 and segment in {"consumer", "smb_founder", "general_pm"}:
        return "user_interviews"
    return "user_interviews"  # default
```

### Recipe 8: Calendly handoff after accept

```bash
# Once accepted on the panel, send the Calendly booking link
curl -X POST "https://api.calendly.com/scheduled_events_invitations" \
  -H "Authorization: Bearer $CALENDLY_API_TOKEN" \
  -d '{
    "event_type_uri": "https://api.calendly.com/event_types/<your-event-type>",
    "invitee_email": "participant@example.com"
  }'
```

### Recipe 9: Over-recruit math

```python
def over_recruit(target, no_show_rate=0.20, qualification_rate=0.40):
    """
    target = sessions needed
    no_show_rate = % accepted who don't show
    qualification_rate = % applicants who pass screener
    """
    accept_count = target / (1 - no_show_rate)
    invite_count = accept_count / qualification_rate
    return int(round(accept_count)), int(round(invite_count))

# Example: target 12 sessions
# Need to accept 15; invite ~38 applicants
# Plan 38-50 applicant capacity in the panel project
```

### Recipe 10: Reject + thank-you note (panel hygiene)

```bash
# Always thank rejected applicants; panel hygiene + future reuse
curl -X POST "https://api.userinterviews.com/v1/applications/$APP_ID/reject" \
  -H "Authorization: Bearer $USER_INTERVIEWS_API_KEY" \
  -d '{
    "reason": "quota_full",
    "message": "Thanks so much for applying! We hit our participant cap for this study. We will keep you in our system for future research that matches your background."
  }'
```

## Examples

### Example 1: Recruit 8 healthcare CIOs
**Goal:** Talk to 8 healthcare IT decision-makers on EHR pain.

**Steps:**
1. Route: Respondent (B2B specialist) — Recipe 7.
2. Project create (Recipe 4) with strict criteria + $300 honorarium.
3. Push screener via `screener-design-recruitment-criteria`.
4. Review applicants daily (Recipe 2 equivalent on Respondent).
5. Calendly handoff (Recipe 8).
6. Track no-shows + over-recruit (Recipe 9).

**Result:** 8 high-quality CIO interviews in 2-3 weeks at ~$2.5K incentive spend.

### Example 2: 12-person 14-day diary study on inbox habits
**Goal:** Longitudinal data on real-world email behavior.

**Steps:**
1. Route: dscout (longitudinal + mobile) — Recipe 7.
2. Mission create (Recipe 5) with onboarding + daily + reflection prompts.
3. Monitor day-3 engagement; nudge non-responders; remove deadweight.
4. Pull entries via `GET /missions/$MISSION_ID/entries`; sync to Dovetail.

**Result:** 12 participants × 14 days = ~168 diary entries with photos/videos. Synthesize via `diary-studies-dscout-7-30-day` skill.

## Edge cases / gotchas

- **Panel platform mismatch.** Recruiting B2B specialists on User Interviews = noise. Use Respondent for vetted B2B.
- **Incentive too low for senior segments.** $50 for a CIO interview = no respondents. Standard B2B senior = $150-400.
- **Over-recruiting without a plan to reject.** Accepting 20 for 12 slots without a fair reject process = bad faith.
- **No anti-screen → professional respondents.** Pros warp findings — always include anti-screen (see screener skill).
- **Forgetting Calendly auto-cancel.** No-show rate is 15-25%; over-recruit + send reminders 24h before.
- **dscout dropouts on day 2-3.** Always include onboarding mission Day 0 + check-in Day 3; remove disengaged.
- **Prolific PROLIFIC_PID forwarding.** If you forget the URL parameter, you can't match survey response → participant for payment.
- **Cost overrun.** Track incentive spend vs budget per-project; cap recruit at target + buffer.
- **Quality score floor.** Respondent + User Interviews expose researcher ratings; set minimum 4.5/5.
- **GDPR consent always.** Every screener has it; panel platforms enforce but don't audit.
- **B2B respondent fatigue.** Senior B2B respondents get bombarded; personalize outreach + emphasize confidentiality.

## Sources

- [User Interviews API](https://www.userinterviews.com/api)
- [Respondent.io API](https://respondent.io/help)
- [dscout API docs](https://dscout.com/api)
- [Prolific API docs](https://docs.prolific.com)
- [Calendly API v2](https://developer.calendly.com)
- [NN/g — Recruiting](https://www.nngroup.com/articles/screening-research-participants/)
- [Erika Hall — Just Enough Research recruitment hygiene](https://abookapart.com/products/just-enough-research)
