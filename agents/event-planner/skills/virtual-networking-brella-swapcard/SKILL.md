<!--
Sources:
- Brella: https://brella.io
- Swapcard: https://www.swapcard.com
- Grip: https://grip.events
- Grip developer: https://docs.grip.events
- Hopin Networking (RingCentral Events): https://hopin.com
- EventMobi: https://www.eventmobi.com
- Whova matchmaking: https://whova.com
-->
# Virtual Networking + Matchmaking (Brella / Swapcard / Grip) — SKILL

End-to-end virtual networking pipeline: interest taxonomy → attendee onboarding → AI matchmaking → meeting scheduling → video chat infrastructure → in-meeting tools → post-meeting follow-up. Networking ROI is the #1 driver of virtual event satisfaction — attendees forgive bad content if they made one good connection. Build for "5 meetings booked" per attendee as success benchmark.

## When to use this skill

- Virtual or hybrid conference where networking is a primary value
- Trade show with B2B matchmaking focus
- Customer summit needing 1:1 customer-to-customer connections
- Investor conference with founder-investor matchmaking
- Recruiting event matching talent to companies
- Sponsor lead-gen value-add (sponsors meet pre-qualified attendees)

**Do NOT use this skill when:**
- Pure broadcast webinar (no networking value)
- Closed-door executive briefing (too small for matchmaking)
- Workshop format (cohort already knows each other)
- B2C festival (different platform tier — Bumble for Friends / Lunchclub)

## Setup

### Platform decision matrix

| Need | First-stop | Notes |
|---|---|---|
| AI matchmaking + 1:1 meetings | Brella | Industry leader; interest-based |
| Combined experience + content + matchmaking | Swapcard | Strong agenda integration |
| B2B trade-show matchmaking | Grip | Trade-show specialist |
| Hopin / RingCentral ecosystem | RingCentral Events Networking | Built-in for Hopin events |
| Mobile-app-primary, affordable | Whova matchmaking | Lower price tier |
| Branded mid-market | EventMobi networking | Custom branded |

### Tools

- `cli-anything` for Brella / Swapcard / Grip REST API
- `notion-mcp` for interest taxonomy source of truth
- `gmail-mcp` for pre-event matchmaking onboarding nudges
- `slack-mcp` for day-of meeting reminder ops channel
- `posthog-mcp` for matchmaking funnel tracking

### Brella API

```bash
export BRELLA_TOKEN="<api-key>"   # https://brella.io > Admin > API
# Base: https://api.brella.io/v1/
```

### Swapcard API

```bash
export SWAPCARD_TOKEN="<oauth-bearer>"
# Base: https://api.swapcard.com/graphql/
```

### Grip API

```bash
export GRIP_TOKEN="<api-key>"
# Base: https://api.grip.events/v1/
```

## Common recipes

### Recipe 1: Interest taxonomy design (foundational decision)

Interest taxonomy drives match quality. Too few categories = generic matches; too many = sparse matches.

```markdown
# Interest taxonomy — DevConf 2027

## Technical (pick 3-5)
- AI/ML Engineering
- LLM Production + Deployment
- LLM Eval + Observability
- Distributed Systems
- Database Internals
- Kubernetes / Container Orchestration
- Frontend Frameworks (React, Vue, Svelte)
- DevOps + Platform Engineering
- Security + Compliance

## Business (pick 2-4)
- Hiring (companies looking)
- Job Seeking (candidates)
- Investing / VC
- Co-Founder / Partnership Search
- Customer Discovery
- Sales Prospecting
- Acquisition Conversations

## Personal (pick 0-2)
- Mentor (offering)
- Mentee (seeking)
- Local Chicago Meetup
- Newcomer to the industry

## Target: 5-10 interests selected per attendee
## Algorithm: 1+ interest overlap = match candidate
## Match score: weighted by interest popularity (rare interests = stronger match signal)
```

### Recipe 2: Brella setup (interests + matchmaking)

```bash
# 1. Create event interest taxonomy
curl -X POST https://api.brella.io/v1/events/$EVENT_ID/interests \
  -H "Authorization: Bearer $BRELLA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "categories": [
      {
        "name": "Technical",
        "interests": ["AI/ML Engineering", "LLM Production", "Distributed Systems", "Kubernetes", "DevOps"]
      },
      {
        "name": "Business",
        "interests": ["Hiring", "Job Seeking", "Investing", "Co-Founder Search", "Sales Prospecting"]
      }
    ]
  }'

# 2. Configure matchmaking algorithm
curl -X PUT https://api.brella.io/v1/events/$EVENT_ID/matchmaking \
  -d '{
    "minInterestOverlap": 1,
    "suggestionsPerAttendee": 10,
    "diversityBias": "moderate",
    "excludeSameCompany": true,
    "matchSchedulingSlots": ["2027-09-15T11:00", "2027-09-15T15:30", "2027-09-16T10:30", "2027-09-16T14:00"]
  }'

# 3. Onboarding email cadence
curl -X POST https://api.brella.io/v1/events/$EVENT_ID/onboarding/cadence \
  -d '{
    "stages": [
      {"daysBefore": 14, "template": "select_interests"},
      {"daysBefore": 7, "template": "complete_profile"},
      {"daysBefore": 3, "template": "review_matches_book_meetings"},
      {"daysBefore": 1, "template": "final_meeting_check"}
    ]
  }'
```

### Recipe 3: Swapcard setup (GraphQL API)

```graphql
mutation CreateEventInterests {
  createInterestTaxonomy(
    eventId: "devconf-2027"
    interests: [
      {name: "AI/ML Engineering", category: "Technical"}
      {name: "LLM Production", category: "Technical"}
      {name: "Hiring", category: "Business"}
    ]
  ) {
    id
    success
  }
}

mutation EnableMatchmaking {
  configureMatchmaking(
    eventId: "devconf-2027"
    algorithm: INTEREST_OVERLAP_WEIGHTED
    suggestionsPerAttendee: 8
    meetingDuration: 15
  ) {
    success
  }
}
```

### Recipe 4: Grip for B2B trade-show

```bash
# Grip uses ML for meeting-quality scoring (not just interest overlap)
curl -X POST https://api.grip.events/v1/events/$EVENT_ID/configure-matchmaking \
  -d '{
    "matchingType": "ml_recommended",
    "buyerSellerMatching": true,
    "categories": {
      "buyers": ["procurement", "engineering_lead"],
      "sellers": ["sponsor", "exhibitor"]
    },
    "meetingDuration": 20,
    "preEventMeetingsCap": 10
  }'
```

### Recipe 5: Pre-event nudge cadence (drives ROI)

The single biggest variable in networking ROI is whether attendees onboard pre-event. Cadence:

```python
# T-14 days: "Select your interests"
mcp_tool('gmail.send_email',
         to=attendee.email,
         subject='Select your 5-7 interests for DevConf networking',
         body=render_template('select_interests.md', attendee=attendee))

# T-7 days: "Complete your profile" (photo + bio + LinkedIn)
mcp_tool('gmail.send_email',
         subject='Final step: complete your DevConf profile',
         body=render_template('complete_profile.md', missing_fields=...))

# T-3 days: "We found you 12 matches" + 1-click meeting booking
mcp_tool('gmail.send_email',
         subject='12 high-match DevConf attendees waiting to meet you',
         body=render_template('book_meetings.md', matches=brella.get_matches(attendee)))

# T-1 day: "Your meeting schedule — print it"
mcp_tool('gmail.send_email',
         subject='Your DevConf meeting schedule (print this)',
         body=render_template('meeting_schedule.md', meetings=brella.get_meetings(attendee)))
```

### Recipe 6: Meeting infrastructure (in-person + virtual rooms)

For hybrid events, configure both:

```bash
# Virtual: Brella video chat (WebRTC native)
# In-person: physical meeting rooms or zones in venue floor plan

curl -X POST https://api.brella.io/v1/events/$EVENT_ID/meeting-locations \
  -d '{
    "virtual": {
      "videoChatProvider": "brella_webrtc",
      "duration": 15,
      "maxConcurrent": 200
    },
    "inPerson": {
      "zones": [
        {"name": "Networking Lounge A", "capacity": 30, "location": "2F"},
        {"name": "Quiet Meeting Pods", "capacity": 8, "location": "1F"},
        {"name": "Coffee Bar Zone", "capacity": 50, "location": "Lobby"}
      ]
    }
  }'
```

### Recipe 7: Speed networking session

```bash
# Speed networking: 5-min round-robin meetings, AI-matched
curl -X POST https://api.brella.io/v1/events/$EVENT_ID/speed-networking \
  -d '{
    "scheduledAt": "2027-09-15T17:00:00-05:00",
    "duration": 60,
    "matchDuration": 5,
    "modalities": ["video"],
    "matchAlgorithm": "interest_overlap"
  }'
```

### Recipe 8: Post-meeting follow-up automation

```bash
# After each meeting, prompt both attendees to capture takeaways
curl -X POST https://api.brella.io/v1/events/$EVENT_ID/meeting-followups \
  -d '{
    "triggerAfterMeeting": true,
    "followupQuestions": [
      "What was the highlight of the meeting?",
      "Want to continue the conversation? (LinkedIn / email exchange)",
      "Would you recommend this match algorithm?"
    ]
  }'
```

### Recipe 9: Sponsor pre-booked meetings (sponsor deliverable)

Many sponsor tiers include "X pre-booked meetings with qualified attendees" — automate this.

```python
# For each Gold-tier sponsor (3 meetings included)
sponsors_gold = notion.query_db('sponsors', filter={'tier': 'Gold'})
for sponsor in sponsors_gold:
    # AI-suggest top 5 matches by interest + decision-maker status
    candidates = brella.suggest_matches(
        from_company=sponsor.name,
        interests=sponsor.target_interests,
        decision_maker_only=True,
        n=5
    )
    # Offer top 3 to sponsor for confirmation
    for c in candidates[:3]:
        brella.invite_meeting(
            from_attendee_id=sponsor.attendee_id,
            to_attendee_id=c.id,
            time_slot='2027-09-15T11:00:00-05:00'
        )
```

### Recipe 10: Matchmaking analytics

```sql
-- postgresql-mcp: networking funnel
SELECT
  COUNT(DISTINCT attendee_id) AS total_attendees,
  COUNT(DISTINCT CASE WHEN profile_complete THEN attendee_id END) AS profiles_complete,
  COUNT(DISTINCT CASE WHEN matches_viewed > 0 THEN attendee_id END) AS viewed_matches,
  COUNT(DISTINCT CASE WHEN meetings_booked > 0 THEN attendee_id END) AS booked_meetings,
  AVG(meetings_booked) AS avg_meetings_per_attendee,
  COUNT(DISTINCT CASE WHEN meetings_held > 0 THEN attendee_id END) AS held_meetings,
  AVG(meeting_rating) AS avg_meeting_rating
FROM networking_funnel
WHERE event_id = 'devconf-2027';
```

## Examples

### Example A: Brella for 600-attendee hybrid conference

```
Pre-event:
- 86% of attendees onboard (high)
- 73% select 5+ interests
- 58% upload photo
- 41% book at least 1 meeting
Day-of:
- 78% of booked meetings actually held
- Avg meeting rating: 4.2/5
- Avg meetings per attendee: 3.4
Post-event:
- 27% of meetings result in LinkedIn connection within 7 days
- 12% result in follow-up call within 30 days
- 4% result in business outcome within 90 days (deal, hire, partnership)
```

### Example B: Grip B2B trade show

```
Use case: 5,000-attendee trade show, buyers vs sellers
Configuration: Buyer-seller matching algorithm (not interest)
Buyer signals: "looking for ML inference infrastructure"
Seller signals: sponsor companies offering ML infra
ML scoring: combines interest + company size + recent funding + tech stack signals
Result: Each buyer gets 15-20 qualified seller suggestions; sellers get 30-50 buyer leads
```

### Example C: Hopin Speed Networking

```
2-hour session, 5-min matches
Avg 24 meetings per attendee in session
Post-session: 8% retention to LinkedIn connection
Cost: included in Hopin platform; no extra
```

## Edge cases

### Low onboarding rate kills value
If <40% of attendees onboard, matchmaking value collapses. Push 4+ nudge cadence. Make onboarding part of registration confirmation (not separate flow).

### Sponsors dominating matching
Sponsors over-prioritize their own matches and crowd out attendee-to-attendee meetings. Cap sponsor-initiated meetings at 30% of total meeting slots.

### Recruiter spam
Recruiters can flood matchmaking with mass meeting requests. Detect via Notion enrichment (>5 meeting requests in 1 hour = flag). Auto-throttle.

### Geographic mismatch
For hybrid events, virtual attendees can't physically meet in-room attendees. Tag meetings as "virtual only" / "in-person only" / "either"; filter accordingly.

### Time zone mismatches
For global virtual, attendees in 24 time zones can't all meet. Brella offers timezone-aware suggestions ("only suggest matches in compatible windows").

### Privacy / consent
Attendees must consent to: being in directory, being suggested as match, being contactable. Default at registration is OPT-OUT for visibility; opt-in to participate in matchmaking. GDPR / CCPA compliant.

### Photo / bio missing
Attendees without photo + bio get low match acceptance. Pre-event nudge with "you have 3x fewer matches without a photo" copy.

### No-show meetings
20-30% of booked meetings don't happen. Acceptable noise; don't over-engineer cancellation flow. Mark as "no-show" and learn.

### Interest taxonomy too coarse
"AI/ML" alone is too broad. Subcategorize: "LLM Production", "ML Infra", "ML Research", "ML Ethics". Specific = better matches.

### Anti-fraud (fake profiles)
Bots / fake registrants pollute matching. Require LinkedIn verification at registration OR email domain whitelist.

### Same-company filter
For internal company events, "exclude same company" filter is OFF. For external events, it's ON.

### Meeting room scarcity
For in-person, networking lounge capacity is finite. Track capacity in real-time; pause new bookings when near capacity.

### Sponsor pre-booked meeting quality
Force sponsors to fill out company brief + target persona BEFORE meeting suggestions are sent. Avoids "thanks for meeting, want a demo?" spam.

### Cross-event remembering
Repeat events can benefit from cross-event interest persistence (returning attendees keep their interests). Persistent profile via Brella account.

## Sources

- **Brella**: https://brella.io
- **Brella developer**: https://docs.brella.io
- **Swapcard**: https://www.swapcard.com
- **Swapcard developer**: https://developers.swapcard.com
- **Grip**: https://grip.events | API: https://docs.grip.events
- **Hopin Networking**: https://hopin.com
- **Whova matchmaking**: https://whova.com
- **EventMobi**: https://www.eventmobi.com
- **Lunchclub (consumer networking)**: https://lunchclub.com
