<!--
Sources:
- Sessionize: https://sessionize.com
- Sessionize API docs: https://sessionize.com/playbook/speaker
- Papercall: https://www.papercall.io
- Pretalx: https://pretalx.com
- CFP-app: https://github.com/jagrutiti/cfp-app
- PCMA CFP best practices: https://www.pcma.org/call-for-proposals-cfp/
-->
# Conference CFP / CFS Track Design — SKILL

End-to-end Call-For-Papers / Call-For-Speakers pipeline: track + theme design → CFP page setup → open submission → rubric-based review → committee scoring → notifications → agenda assembly. Sessionize is the SOTA default for tech conferences; Papercall + Pretalx for community / open-source events. CFP isn't just a form — it's a content-curation system that shapes the conference identity.

## When to use this skill

- New conference needing 20-200 speaker slots filled by open submission (not pure invite)
- Multi-track conference with technical depth that benefits from community voice
- Established conference renewing CFP cycle (recurring annual event)
- Community / open-source conference where pay-to-speak is anti-pattern
- Conference where program committee wants distributed review (10-50 reviewers)
- DevConf, TechCrunch Disrupt-style, PyCon, KubeCon-style events

**Do NOT use this skill when:**
- Event is keynote-only or fully invited (use `speaker-management-sourcing-prep` instead)
- Single-track summit where curation is editorial, not crowd-sourced
- <5 speaker slots (manual outreach beats CFP overhead)
- Closed-door customer summit (no public CFP; defer to `customer-success`)

## Setup

### Tools

- `cli-anything` for Sessionize / Papercall / Pretalx REST API
- `gmail-mcp` for accept/reject/waitlist notifications
- `notion-mcp` for review rubric DB + committee scoring + agenda assembly
- `firecrawl-mcp` for past-talk verification of submitter
- `youtube-mcp-transcript` for prior-talk quality check

### Sessionize API

```bash
export SESSIONIZE_TOKEN="<api-key>"   # Settings > API
# Base: https://sessionize.com/api/v2/
```

### Papercall API

```bash
export PAPERCALL_TOKEN="<api-key>"    # Settings > API
# Base: https://www.papercall.io/api/v1/
```

### Pretalx (self-hosted or pretalx.com)

```bash
export PRETALX_TOKEN="<token>"
export PRETALX_BASE="https://pretalx.com/api"  # or your self-hosted URL
```

## Common recipes

### Recipe 1: Track + theme design (before opening CFP)

Decide tracks BEFORE opening CFP — submissions self-categorize, which drives review committee assignment.

```markdown
# DevConf 2027 — Tracks (decided 90 days before CFP opens)

## Track 1: AI / ML Engineering
- LLM application patterns
- Eval + observability
- Production deployment + cost
- Track owner: [Sarah K.]
- Slots: 18 (6 per day x 3 days)
- Format mix: 50% 30-min talks, 30% 45-min talks, 20% panels

## Track 2: Infrastructure
- Kubernetes at scale
- Database internals
- Distributed systems patterns
- Track owner: [Marcus L.]
- Slots: 18
- Format: 50/30/20 same

## Track 3: Frontend + Developer Experience
- Track owner: [Priya S.]
- Slots: 12

## Track 4: DevOps + Platform Engineering
- Track owner: [James T.]
- Slots: 12

## Track 5: Community + Career
- Track owner: [Aisha N.]
- Slots: 6 (lightning talks heavy)

## TOTAL: 66 slots across 5 tracks
## Submission target: 6-10x slots = 400-660 submissions = healthy CFP
```

### Recipe 2: Sessionize CFP setup

```bash
# 1. Create event
curl -X POST https://sessionize.com/api/v2/events \
  -H "Authorization: Bearer $SESSIONIZE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "DevConf 2027",
    "url": "devconf-2027",
    "startDate": "2027-09-15",
    "endDate": "2027-09-17",
    "timezone": "America/Chicago",
    "location": "Chicago, IL"
  }'

# 2. Create CFP with tracks
curl -X POST https://sessionize.com/api/v2/events/$EVENT_ID/cfp \
  -H "Authorization: Bearer $SESSIONIZE_TOKEN" \
  -d '{
    "title": "Speak at DevConf 2027",
    "intro": "We want experts on AI/ML, infra, frontend, devops, community. CFP open through July 30. Notifications August 15.",
    "categories": [
      {"name": "Track", "type": "single",
       "options": ["AI/ML", "Infra", "Frontend", "DevOps", "Community"]},
      {"name": "Level", "type": "single",
       "options": ["Beginner", "Intermediate", "Advanced"]},
      {"name": "Format", "type": "single",
       "options": ["30-min talk", "45-min talk", "60-min workshop", "10-min lightning", "Panel"]}
    ],
    "questions": [
      {"q": "Session title (max 80 chars)", "required": true},
      {"q": "Abstract (max 1500 chars) — what attendees learn", "required": true},
      {"q": "Detailed outline for committee (1000-3000 chars)", "required": true},
      {"q": "Target audience persona + level", "required": true},
      {"q": "Speaker bio (max 300 chars)", "required": true},
      {"q": "Prior talks: link to video of similar talk OR explain why first-time", "required": false},
      {"q": "Code of conduct + diversity statement acknowledgment", "required": true,
       "type": "checkbox"}
    ],
    "deadline": "2027-07-30T23:59:00Z",
    "notifyDate": "2027-08-15"
  }'

# 3. Publish CFP page (auto-generated URL: sessionize.com/devconf-2027)
```

### Recipe 3: Papercall CFP setup (community alt)

```bash
curl -X POST https://www.papercall.io/api/v1/events \
  -H "Authorization: Token $PAPERCALL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "event": {
      "name": "PyData Chicago 2027",
      "url": "pydata-chicago-2027",
      "starts_at": "2027-10-05",
      "ends_at": "2027-10-07",
      "cfp_closes_at": "2027-08-15",
      "talk_types": ["Talk (30 min)", "Workshop (90 min)", "Lightning (10 min)"],
      "audience_levels": ["Beginner", "Intermediate", "Advanced"]
    }
  }'
```

### Recipe 4: Pretalx (open-source, German-led, used by many EU events)

```bash
curl -X POST $PRETALX_BASE/events/ \
  -H "Authorization: Token $PRETALX_TOKEN" \
  -d '{
    "name": {"en": "FOSDEM-style 2027"},
    "slug": "fosdem-style-2027",
    "date_from": "2027-02-04",
    "date_to": "2027-02-05",
    "timezone": "Europe/Brussels",
    "cfp_deadline": "2026-11-30"
  }'
```

### Recipe 5: Review rubric (committee-grade)

Send committee a shared rubric BEFORE reviewing — avoids each reviewer scoring on different axes.

```markdown
# Review rubric — 4 axes, 1-5 scale per axis (max 20)

## Axis 1: Relevance to track (1-5)
- 5 = Bullseye for track theme + audience persona
- 3 = Adjacent topic, would still draw attendees
- 1 = Off-topic; doesn't belong

## Axis 2: Novelty / hook (1-5)
- 5 = Fresh angle nobody else is presenting; canonical reference for the year
- 3 = Solid take, similar to other submissions
- 1 = Vendor pitch / rehash of last year's content

## Axis 3: Speaker credibility + delivery (1-5)
- 5 = Prior talks at this level; video evidence of great delivery
- 3 = Some prior speaking; lower-tier events
- 1 = First-time speaker with no evidence of delivery skill

## Axis 4: Audience fit + level alignment (1-5)
- 5 = Right level for stated audience; concrete takeaway
- 3 = Useful but mismatched level (e.g., beginner content for advanced track)
- 1 = Audience-mismatched OR no clear takeaway

## TOTAL: /20 max
## Acceptance threshold per track:
- Top 30% by score → accept
- Next 20% → waitlist (fill no-shows)
- Bottom 50% → polite decline with track-specific feedback
```

### Recipe 6: Programmatic submission pull + reviewer assignment

```bash
# Pull all submissions
curl -X GET https://sessionize.com/api/v2/events/$EVENT_ID/sessions \
  -H "Authorization: Bearer $SESSIONIZE_TOKEN" > submissions.json

# Distribute to reviewers (3 reviewers per submission for triangulation)
python distribute_to_reviewers.py submissions.json --reviewers reviewers.yaml --per-submission 3
```

```python
# distribute_to_reviewers.py — round-robin assignment
import json, yaml, random
subs = json.load(open('submissions.json'))['sessions']
reviewers = yaml.safe_load(open('reviewers.yaml'))['reviewers']

assignments = []
for sub in subs:
    track = sub['categoryItems'][0]
    track_reviewers = [r for r in reviewers if track in r['tracks']]
    chosen = random.sample(track_reviewers, 3)
    for r in chosen:
        assignments.append({'sub_id': sub['id'], 'reviewer': r['email'], 'track': track})

# Push to notion-mcp
for a in assignments:
    notion.create_db_row(database='cfp-reviews', properties=a)
```

### Recipe 7: Send accept / decline / waitlist notifications

```python
# After committee scoring closes
for sub in scored_submissions:
    if sub['final_score'] >= 16:
        status = 'accepted'
        template = 'cfp_accept.md'
    elif sub['final_score'] >= 13:
        status = 'waitlist'
        template = 'cfp_waitlist.md'
    else:
        status = 'declined'
        template = 'cfp_decline.md'

    body = render_template(template, sub=sub)
    mcp_tool('gmail.send_email',
             to=sub['speaker_email'],
             subject=f"DevConf 2027 — {status}",
             body=body)
```

## Examples

### Example A: 600-submission CFP for 60 slots (10x ratio)

```bash
# 1. Open CFP 90 days before event
# 2. Promote via marketing-agent + sponsor newsletters + Twitter
# 3. CFP runs 6 weeks
# 4. 600 submissions arrive
# 5. Reviewer pool: 20 reviewers, each gets ~90 submissions (3 reviews per submission)
# 6. Scoring period: 3 weeks
# 7. Committee meeting: 2 hours, narrow waitlist edge cases
# 8. Notifications sent: 60 accept, 60 waitlist, 480 decline
# 9. Decline notes: track-specific feedback + invite to re-submit next year
```

### Example B: Lightning talk track from waitlist

For waitlisted submissions, offer a lightning-talk slot (10 min) as fallback. Honors community contribution while staying within capacity.

```python
waitlist = [s for s in submissions if 13 <= s['score'] < 16]
lightning_slots = 12  # e.g., 1 lightning block per track
selected = sorted(waitlist, key=lambda s: s['score'], reverse=True)[:lightning_slots]
for s in selected:
    send_lightning_invite(s)
```

### Example C: Diversity-aware acceptance

After scoring, audit the accept list for diversity (gender, geographic, employer, level). If overrepresented in one axis, swap in waitlisted speakers from underrepresented groups (at equivalent quality threshold).

```python
accepts = [s for s in submissions if s['score'] >= 16]
diversity_audit = {
    'gender': count_by_field(accepts, 'gender'),
    'first_time_speakers': sum(1 for s in accepts if s['first_time']),
    'employer_concentration': max_share(accepts, 'employer')
}
if diversity_audit['employer_concentration'] > 0.15:
    # No employer >15% of program; swap lowest-scoring overrepresented for waitlist
    rebalance(accepts, waitlist, key='employer')
```

## Edge cases

### Vendor pitch detection
Submissions that are thinly veiled vendor pitches should be auto-flagged. Heuristic: abstract mentions vendor product >3 times AND outline has no architecture / no implementation detail. Reviewer rubric Axis 2 (novelty) handles, but flag in tooling.

### Co-speakers
Multi-presenter sessions are valid but add coordination overhead. Cap at 2 co-speakers; require all to confirm acceptance before scheduling.

### Late submissions
Submissions after deadline: do NOT accept unless committee unanimously votes for a late exception (e.g., for keynote-quality submission). Otherwise the deadline loses meaning.

### Speaker conflict of interest
Reviewers should self-recuse if they work at same company as submitter OR have personal relationship. Use Notion DB conflict-of-interest field on submission entry.

### Disputed scores
If reviewer scores differ by >5 points on same submission, escalate to committee chair for tiebreaker review. Don't auto-average.

### Past-talk verification
For accepted speakers, verify their prior-talk link via `youtube-mcp-transcript` for delivery quality. Surfaces speakers who claim talks they didn't actually give.

### CFP re-opening
If CFP submission count falls below 4x slots, extend deadline by 2 weeks OR run targeted outreach via `speaker-management-sourcing-prep`. Do NOT lower acceptance threshold; better to under-fill than over-accept weak content.

### Anonymous review
Some communities (PyCon, JuliaCon) anonymize speaker info during review to reduce bias. Sessionize supports via `anonymizeReview: true` flag. Decide policy before opening CFP.

### Decline feedback templates
Always send specific decline feedback (not just "thank you for applying"). Builds long-term relationship + better resubmissions next year. Template per track owner.

### Notification timing
Send accepts FIRST (within 24 hours of committee close); declines after acceptances are confirmed (in case substitutions needed). Avoids declined speakers seeing accepts on social before they hear from you.

### Sponsor speaker slots
Sponsor-tier speakers are NOT part of CFP. Track separately. See `sponsor-tier-deliverable-tracking`.

### Travel grant for selected speakers
For accepted speakers needing travel support (junior speakers, international, underrepresented), offer travel grant up to $X. Apply via separate form during acceptance phase. Hand off to `speaker-management-sourcing-prep` for booking.

## Sources

- **Sessionize**: https://sessionize.com
- **Sessionize Playbook**: https://sessionize.com/playbook
- **Papercall**: https://www.papercall.io
- **Pretalx**: https://pretalx.com
- **CFP-app (GitHub)**: https://github.com/jagrutiti/cfp-app
- **PCMA CFP best practices**: https://www.pcma.org/call-for-proposals-cfp/
- **WeAreDevelopers CFP guide**: https://www.wearedevelopers.com/magazine/how-to-write-a-cfp
- **TechCrunch Disrupt CFP**: https://techcrunch.com/events/tc-disrupt-2025/cfp/
