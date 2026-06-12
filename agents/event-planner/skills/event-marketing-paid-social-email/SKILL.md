<!--
Sources:
- LinkedIn Marketing API: https://learn.microsoft.com/en-us/linkedin/marketing/
- Meta Ads Manager API: https://developers.facebook.com/docs/marketing-apis
- Twitter (X) Ads API: https://developer.twitter.com/en/docs/twitter-ads-api
- TikTok Ads API: https://ads.tiktok.com/marketing_api
- Klaviyo API: https://developers.klaviyo.com
- HubSpot Email API: https://developers.hubspot.com/docs/api/marketing/marketing-emails
- Marketo API: https://developers.marketo.com
- Bizzabo Event Marketing: https://www.bizzabo.com/blog/event-marketing
- PostHog: https://posthog.com
-->
# Event Marketing (Paid Social + Email + PR) — SKILL

End-to-end event marketing brief authoring + campaign coordination + execution handoff. This agent OWNS the brief, dependency timeline, attribution tracking, and post-campaign analysis. Execution happens via `marketing-agent` (paid social, email nurture, content) and `pr-comms` (earned media). Coordinate across channels for layered registration push.

## When to use this skill

- Authoring marketing campaign brief for an upcoming event (90-120 days out)
- Coordinating registration push across paid social + email + PR (60 days out)
- Mid-campaign performance review + budget reallocation (30 days out)
- Last-minute fill push (T-14 to T-1 days)
- Post-campaign attribution analysis (T+30 days)
- Year-over-year channel performance benchmarking

**Do NOT use this skill when:**
- Marketing campaign execution (defer to `marketing-agent`)
- PR / earned media outreach (defer to `pr-comms`)
- Influencer partnerships (defer to `bd-partnerships`)
- Sponsor co-marketing (cross-cut with `sponsor-tier-deliverable-tracking`)

## Setup

### Tools

- `cli-anything` for paid platform APIs (LinkedIn / Meta / Twitter / TikTok)
- `notion-mcp` for campaign brief + dependency timeline
- `posthog-mcp` for funnel + attribution tracking
- `gmail-mcp` / `outlook-mcp` for stakeholder updates
- Handoff to `marketing-agent` for execution
- Handoff to `pr-comms` for earned media

### Platform decision matrix (by event type)

| Event type | Paid social default | Email | PR |
|---|---|---|---|
| B2B conference | Paid LinkedIn primary + paid Twitter retargeting | HubSpot / Marketo nurture | Industry trade press via `pr-comms` |
| Consumer / festival | Paid Meta (Facebook / IG) + TikTok + Twitter | Klaviyo / Mailchimp | Consumer press + influencer |
| Webinar | Paid LinkedIn + Twitter + email nurture | Marketo / HubSpot | Bylined article on industry blog |
| Customer summit (free) | LinkedIn promoted post + email | Customer-success email | Optional case-study PR via `pr-comms` |
| Investor / founder event | LinkedIn + email + PR-led | Direct outreach | Funding announcements via `pr-comms` |
| Recruiting / career fair | LinkedIn + indeed + Glassdoor | Email to past applicants | Local press |
| Workshop / training | LinkedIn + email | Sequences via Customer.io | None |

## Common recipes

### Recipe 1: Campaign brief authoring (90 days out)

```markdown
# DevConf 2027 — Marketing Campaign Brief

## Event basics
- Date: 2027-09-15 to 2027-09-17
- Format: In-person + virtual stream
- Capacity: 600 in-person + 5,000 virtual
- Goal: Sell 540 in-person tickets + 4,500 virtual passes by T-14 days

## Audience target
- Primary persona: Senior engineers + engineering managers at $50M+ tech companies (US-based)
- Secondary: International virtual attendees (EU + APAC)
- Decision-maker share target: 25%+ Director-level or above

## Positioning + key messages
- Positioning: "The 600-attendee dev conference where production AI gets real"
- Pillar 1: Speakers actually shipping LLMs at scale (not advice, receipts)
- Pillar 2: Networking via Brella matchmaking (5 pre-booked meetings)
- Pillar 3: Hands-on workshop day (Day 3)

## Budget envelope
- Paid social: $80K (50% LinkedIn, 30% Twitter, 15% Meta retargeting, 5% test channels)
- Email nurture: $0 (internal)
- PR: $30K (agency fee for `pr-comms` execution)
- Creative production: $25K (paid + organic + email creative)
- Total marketing budget: $135K

## Channel mix + dependencies
- T-90: Open registration; announce on Twitter + LinkedIn + email (organic)
- T-75: Open paid social (LinkedIn primary)
- T-60: PR launch via `pr-comms` (3 trade press pitches)
- T-45: Email nurture begins (4-touch sequence over 30 days)
- T-30: Early-bird pricing ends; price increase + scarcity push
- T-14: Final paid push (last call)
- T-7: Day-of comms (transit, parking, app, wifi)

## KPIs
- Registration target: 5,040 total
- CPL (cost per lead) target: <$45 (industry benchmark for B2B conferences)
- LinkedIn CTR target: >0.8%
- Email open rate target: >32%
- Channel-attribution split target: 30% paid LinkedIn / 25% email / 20% organic / 15% PR / 10% other

## Handoff
- `marketing-agent`: paid social execution + email nurture + creative production
- `pr-comms`: earned media pitches + press releases
- This agent: weekly performance review + budget reallocation calls + last-mile push coordination
```

### Recipe 2: Paid LinkedIn campaign setup (handoff to marketing-agent)

```python
# Define audience segments
linkedin_audience = {
    'name': 'DevConf 2027 — Senior Engineers @ $50M+ Tech',
    'targeting': {
        'locations': ['United States'],
        'job_seniorities': ['Senior', 'Manager', 'Director', 'VP'],
        'job_functions': ['Engineering', 'Information Technology'],
        'industries': ['Technology', 'Software'],
        'company_sizes': ['501-1000', '1001-5000', '5001-10000', '10001+'],
        'skills': ['Machine Learning', 'Distributed Systems', 'LLM', 'Kubernetes']
    }
}

# Campaign objectives
campaigns = [
    {'name': 'DevConf 2027 — Awareness',  'objective': 'BRAND_AWARENESS', 'budget_daily': 200},
    {'name': 'DevConf 2027 — Registration', 'objective': 'WEBSITE_CONVERSIONS', 'budget_daily': 800,
     'conversion_tracking': 'devconf-2027-reg'},
    {'name': 'DevConf 2027 — Retargeting', 'objective': 'WEBSITE_CONVERSIONS', 'budget_daily': 400,
     'targeting': {'matched_audience': 'website_visitors_90d'}}
]

# Handoff to marketing-agent for execution
mcp_tool('agent_call.marketing-agent',
         payload={
             'task': 'Launch LinkedIn paid campaigns',
             'audience': linkedin_audience,
             'campaigns': campaigns,
             'creative_brief': open('linkedin-creative-brief.md').read(),
             'budget': 80000,
             'start_date': '2027-06-15',
             'end_date': '2027-09-01'
         })
```

### Recipe 3: Email nurture sequence (HubSpot / Marketo)

```python
# 4-touch sequence over 30 days for registered-but-not-yet-attended
sequence = [
    {
        'day_after_reg': 1,
        'subject': 'Confirmed for DevConf 2027 — here\'s what\'s next',
        'body_template': 'confirmation.html',
        'cta': 'Add to calendar'
    },
    {
        'day_after_reg': 14,
        'subject': 'The agenda is live — here are 3 must-see sessions for you',
        'body_template': 'agenda_personalized.html',
        'cta': 'See full agenda',
        'personalization': 'recommend_sessions_by_role'
    },
    {
        'day_after_reg': 30,
        'subject': 'DevConf attendee list preview (8 from your industry)',
        'body_template': 'attendee_preview.html',
        'cta': 'Open Brella to book meetings'
    },
    {
        'day_after_reg': 60,
        'subject': 'Final logistics: transit, hotel, app, wifi',
        'body_template': 'final_logistics.html',
        'cta': 'Download conference app'
    }
]

mcp_tool('agent_call.marketing-agent',
         payload={
             'task': 'Build email nurture sequence',
             'platform': 'hubspot',
             'sequence': sequence,
             'list_id': 'devconf-2027-registered'
         })
```

### Recipe 4: PR campaign handoff (3-track approach)

```markdown
# PR Brief — DevConf 2027 (handoff to pr-comms)

## Track 1: Trade press coverage (TechCrunch, The Verge, InfoQ, The New Stack)
- Lead with: "What's actually working in production LLM infra"
- Spokesperson: Sarah K. (keynote speaker)
- Pitch angle: industry survey data + speaker access for interview
- Embargo: 14 days pre-event

## Track 2: Trade publications (The New Stack, InfoQ)
- Lead with: bylined post-conference recap
- Spokesperson: Conference chair
- Pitch angle: technical deep-dive on conference themes

## Track 3: Earned media via speakers
- Each keynote / panel speaker has their own platform
- Coordinate their pre-event posts (Twitter, LinkedIn, blogs)
- Provide pre-written social copy + visuals
```

### Recipe 5: PostHog funnel tracking

```sql
-- HogQL: registration funnel by channel
SELECT
  properties.utm_source AS channel,
  properties.utm_campaign AS campaign,
  count(DISTINCT person_id) AS visitors,
  count(DISTINCT CASE WHEN event = 'reg_started' THEN person_id END) AS started,
  count(DISTINCT CASE WHEN event = 'reg_completed' THEN person_id END) AS completed,
  count(DISTINCT CASE WHEN event = 'reg_completed' THEN person_id END) * 100.0 / count(DISTINCT person_id) AS conversion_pct
FROM events
WHERE properties.event_name = 'DevConf 2027'
  AND timestamp > now() - interval '90 days'
GROUP BY channel, campaign
ORDER BY completed DESC;
```

### Recipe 6: Last-mile push (T-14 to T-1)

```markdown
# T-14 to T-1 Last-Mile Push

## T-14: scarcity push
- Subject: "Only 47 in-person seats left for DevConf 2027"
- Channel: email + LinkedIn organic + paid retargeting

## T-7: speaker spotlight
- Subject: "Sarah K. on what she'll cover at DevConf next week"
- Channel: email + speaker LinkedIn + Twitter

## T-3: final agenda confirmation
- Subject: "Your DevConf 2027 schedule is set"
- Channel: email to registered only

## T-2: app + logistics
- Subject: "Tomorrow we're seeing you in Chicago — bring this checklist"
- Channel: email + SMS via twilio-mcp

## T-1: confirmation + emergency contact
- Subject: "Confirmed for tomorrow + your in-event contact"
- Channel: email + push notification via event app
```

### Recipe 7: Day-of marketing (organic social)

```python
# Live tweet / LinkedIn post coordination
session_highlights = notion.query_db('devconf-2027-agenda')

for s in session_highlights:
    # 5 min into session, post highlight
    mcp_tool('twitter.post_tweet',
             text=f'Live from #DevConf2027: {s["speaker"]} on "{s["title"]}" — packed room. Thread incoming.',
             schedule_at=s['start_time'] + timedelta(minutes=5),
             media=[s['speaker_photo']])

    mcp_tool('linkedin.post',
             text=f'At DevConf 2027 today, {s["speaker"]} just made the case that {extract_quote(s)}. Worth the trip.',
             schedule_at=s['start_time'] + timedelta(minutes=10))
```

### Recipe 8: Post-campaign attribution analysis

```python
# Pull cost per channel
channel_costs = {
    'linkedin_paid': linkedin.get_spend('devconf-2027'),
    'twitter_paid': twitter.get_spend('devconf-2027'),
    'meta_paid': meta.get_spend('devconf-2027'),
    'email': 0,  # internal
    'pr': 30000  # agency fee
}

# Pull attendees per channel
channel_attendees = posthog.get_channel_attribution('devconf-2027')

# Compute CPL + cost-per-attendee per channel
for ch in channels:
    cpa = channel_costs[ch] / channel_attendees[ch] if channel_attendees[ch] else 'N/A'
    print(f"{ch}: cost ${channel_costs[ch]:,.0f} / attendees {channel_attendees[ch]} / CPA ${cpa}")
```

### Recipe 9: Sponsor co-marketing

For sponsors, coordinate co-marketing where they leverage their reach:

```markdown
# Sponsor Co-Marketing — Gold tier

## Sponsor responsibilities (per contract)
- Promote DevConf 2027 once per week starting T-60
- 3 LinkedIn posts (we provide draft copy + visuals)
- 1 email send to their list with our co-branded creative
- 1 customer reference / case study if applicable

## We provide
- Co-branded creative (sponsor logo + DevConf logo)
- Pre-written social copy in multiple voices
- UTM-tagged URLs for attribution credit
- Tracking dashboard showing their referrals
```

## Examples

### Example A: 5,000-attendee B2B conference, $135K marketing budget

```
Channel mix (final):
- Paid LinkedIn: $80K → 1,460 attendees @ $55 CPA
- Email nurture: $0 → 1,200 attendees (existing list)
- Organic search: $0 → 880 attendees
- PR earned: $30K → 650 attendees @ $46 CPA
- Paid Twitter: $15K → 420 attendees @ $36 CPA (best CPA)
- Paid Meta: $10K → 390 attendees @ $26 CPA
- Total: 5,000 attendees / $135K = $27 CPA

Attribution credit (U-shaped model):
- LinkedIn (29% of pipeline credit)
- Email (24%)
- Organic (18%)
- PR (13%)
- Other (16%)
```

### Example B: 200-attendee virtual webinar, $5K budget

```
Channel mix:
- Paid LinkedIn: $3K → 95 attendees @ $32 CPA
- Email nurture: $0 → 75 attendees
- Twitter organic: $0 → 30 attendees
- Total: 200 attendees / $5K = $25 CPA (excellent for virtual)
```

### Example C: 50-attendee customer summit, $10K budget

```
Channel mix:
- Direct outreach (BDR-led): $0 → 48 attendees (96% from named list)
- Email nurture: $0 → 2 from past-event list
- Total: 50 attendees, primary cost is BDR time + travel for invitees
- CPA $200 + travel (intentionally high — premium event)
```

## Edge cases

### Audience overlap between events
If you run multiple events to same audience, suppress recent attendees from upcoming-event ads. LinkedIn audience exclusion: upload past-attendee list, exclude.

### Channel cannibalization
Paid LinkedIn often steals credit from organic. Use multi-touch attribution; don't auto-blame channels for "stealing."

### Last-mile push fatigue
If you push too hard T-14, audience unsubscribes. Cap email frequency at 2-3 per week pre-event. Use SMS sparingly (Twilio) for T-1 only.

### Sponsor co-marketing not happening
Sponsors often skip co-marketing despite contractual commitment. Reminder cadence + escalation: T-60, T-45, T-30. Document non-compliance for renewal conversation.

### Speaker social amplification
Top speakers have huge platforms but don't always promote. Make it easy: pre-written tweets, LinkedIn posts, visuals. Send 30 days out.

### Influencer / podcast pitches
Podcast guesting drives quality registrations. Pitch 5-10 podcasts in target audience 60 days out. Speaker availability is the limit.

### PR embargo conflicts
If PR launch is T-14 but paid social campaign already disclosed event details, PR is moot. Coordinate timing: paid social can run earlier with high-level pitch; press launches with specific announcements (speakers added, venue locked).

### Last-minute reg price increase backfires
Increasing price T-14 sometimes causes wait-and-see behavior. Test: scarcity push ("47 seats left") vs price push ("$50 more after Friday"). Scarcity usually wins.

### International virtual attendees
For global virtual, multi-timezone email scheduling matters. Use platform timezone-aware send (HubSpot supports per-recipient timezone).

### Sponsor-driven audience
For sponsor-heavy events, sponsors bring their own attendees (sales prospects). Track separately for attribution; sponsor's CRM owns that lead.

### Email deliverability
Sending to mostly-new list can hurt sender reputation. Warm up: start with smaller engaged segments, scale gradually. Use Klaviyo / HubSpot deliverability tools.

### Privacy / consent for retargeting
GDPR + CCPA: retargeting requires consent. Cookie banner + meta pixel consent strict mode. Coordinate with privacy team.

### Channel diversification risk
Over-reliance on one channel (e.g., 70% from LinkedIn) is risky if LinkedIn changes algorithm. Maintain 30%+ from non-LinkedIn channels.

## Sources

- **LinkedIn Marketing API**: https://learn.microsoft.com/en-us/linkedin/marketing/
- **Meta Ads Manager API**: https://developers.facebook.com/docs/marketing-apis
- **Twitter (X) Ads API**: https://developer.twitter.com/en/docs/twitter-ads-api
- **TikTok Ads API**: https://ads.tiktok.com/marketing_api
- **Klaviyo API**: https://developers.klaviyo.com
- **HubSpot Email API**: https://developers.hubspot.com/docs/api/marketing/marketing-emails
- **Marketo API**: https://developers.marketo.com
- **Bizzabo Event Marketing**: https://www.bizzabo.com/blog/event-marketing
- **PostHog**: https://posthog.com
- **Sibling agent**: `marketing-agent` (execution)
- **Sibling agent**: `pr-comms` (earned media)
