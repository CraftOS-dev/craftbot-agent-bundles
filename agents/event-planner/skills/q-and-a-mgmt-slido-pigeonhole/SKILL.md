<!--
Sources:
- Slido API: https://www.slido.com/api
- Slido (Cisco) docs: https://community.slido.com/integrations-and-api-99
- Pigeonhole Live: https://www.pigeonhole.at
- Pigeonhole API: https://pigeonhole.at/api
- Mentimeter: https://www.mentimeter.com
- AhaSlides: https://ahaslides.com
- Wooclap: https://www.wooclap.com
- Kahoot: https://kahoot.com
-->
# Audience Q&A Management (Slido / Pigeonhole / Mentimeter) — SKILL

End-to-end audience Q&A pipeline: platform selection → session setup → moderation workflow → live integration → post-event analytics. Slido (Cisco) is the SOTA for moderated Q&A; Pigeonhole for enterprise events; Mentimeter for polls + word clouds. Q&A is the single highest-engagement moment in a session — moderation makes or breaks it.

## When to use this skill

- Conference / summit needing live audience Q&A across sessions
- Executive briefing where Q&A quality + moderation matters
- Town hall / all-hands needing anonymous Q&A
- Webinar with interactive polls + word clouds
- Hybrid event needing unified Q&A across in-room + virtual
- Educational event with quiz / poll integration

**Do NOT use this skill when:**
- Pure broadcast with no audience input (skip Q&A platform; use chat only)
- Workshop format with informal Q&A (Slack channel adequate)
- Closed-door investor briefing (1:1 conversation; no platform needed)
- Networking-first events (use `virtual-networking-brella-swapcard` for connection-first)

## Setup

### Platform decision matrix

| Need | First-stop | Notes |
|---|---|---|
| Moderated Q&A + polls + word clouds | Slido (Cisco) | Enterprise tier for API; gold standard |
| Enterprise event Q&A with custom branding | Pigeonhole Live | Enterprise-focused |
| Word clouds + interactive polls | Mentimeter | Best polls UX |
| Low-cost Q&A + polls + quizzes | AhaSlides | Most affordable |
| Education-focused interactive | Wooclap | Classroom-tuned |
| Gamified quiz format | Kahoot | Game-show format |

### Tools

- `cli-anything` for Slido / Pigeonhole / Mentimeter REST API
- `notion-mcp` for Q&A archive (post-event question DB)
- `slack-mcp` for moderator backchannel (review queue)
- `pptx` for slide-embed of Q&A code + URL

### Slido API (Enterprise tier required)

```bash
export SLIDO_TOKEN="<api-key>"   # Enterprise tier > Admin > API
# Base: https://api.slido.com/v1/
```

### Pigeonhole API

```bash
export PIGEONHOLE_TOKEN="<api-key>"
# Base: https://pigeonhole.at/api/v1/
```

### Mentimeter API

```bash
export MENTIMETER_TOKEN="<api-key>"
# Base: https://api.mentimeter.com/v1/
```

## Common recipes

### Recipe 1: Slido session creation (per stage / per session)

```bash
# Create Slido event (per stage; or one per conference)
curl -X POST https://api.slido.com/v1/events \
  -H "Authorization: Bearer $SLIDO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "DevConf 2027 — Main Stage",
    "code": "DEVCONF1",
    "startDate": "2027-09-15",
    "endDate": "2027-09-17",
    "settings": {
      "qa": {
        "enabled": true,
        "moderation": "review_before_publish",  # or "publish_immediately"
        "allowAnonymous": true,
        "duplicateDetection": true,
        "profanityFilter": true
      },
      "polls": {
        "enabled": true,
        "anonymousVoting": true
      }
    }
  }'
```

### Recipe 2: Pre-loaded polls per session

```bash
# For each session, pre-create the polls (deck order)
curl -X POST https://api.slido.com/v1/events/$EVENT_ID/polls \
  -d '{
    "polls": [
      {
        "type": "multiple_choice",
        "question": "How do you deploy LLMs?",
        "options": ["Bedrock", "Anthropic API", "OpenAI", "Self-hosted vLLM"],
        "session": "sarah-keynote-2027-09-15-09-00"
      },
      {
        "type": "word_cloud",
        "question": "One word for LLM production challenges",
        "session": "sarah-keynote-2027-09-15-09-00"
      },
      {
        "type": "rating",
        "question": "How likely are you to recommend this talk? (1-5)",
        "session": "sarah-keynote-2027-09-15-09-00"
      }
    ]
  }'
```

### Recipe 3: Moderation workflow

For high-stakes events, moderate Q&A before publish.

```python
# Moderator review queue via Slido API
unmoderated = requests.get(
    f'https://api.slido.com/v1/events/{EVENT_ID}/qa/pending',
    headers={'Authorization': f'Bearer {SLIDO_TOKEN}'}
).json()['questions']

# For each pending question, moderator decides:
# - Approve → publish to audience
# - Edit + approve → publish edited version (typo fix, profanity removal)
# - Reject → don't publish (off-topic, abusive)
# - Hold → save for later (good question, wait for time)

for q in unmoderated:
    decision = moderator_review(q)  # human-in-the-loop
    requests.put(
        f'https://api.slido.com/v1/qa/{q["id"]}',
        json={'status': decision.status, 'editedText': decision.edited_text}
    )
```

### Recipe 4: Slack notification for new Q&A

```bash
# Webhook → Slack moderator backchannel
curl -X POST https://api.slido.com/v1/events/$EVENT_ID/webhooks \
  -d '{
    "url": "https://hooks.slack.com/services/T.../B.../...",
    "events": ["qa.submitted"],
    "messageTemplate": "New Q for review: \"{question.text}\" — by {question.author}\nReview: https://app.slido.com/admin/event/{eventCode}/qa"
  }'
```

### Recipe 5: Hybrid Q&A bridge (in-room + virtual unified)

For hybrid events, single Slido session captures both audiences:

```
Display in-room:
- Slide deck shows Slido URL + code (large QR code)
- Top 3 questions overlay on side screen

Display virtual (Hopin / RingCentral Events):
- Embedded Slido panel in side rail
- Top 3 questions overlay on stream

Moderator workflow:
- All questions arrive in unified moderator queue
- Approve published questions → MC reads aloud OR speaker addresses
- Geo / role-balanced selection (don't favor only one audience)
```

### Recipe 6: Pigeonhole for enterprise event Q&A

```bash
curl -X POST https://pigeonhole.at/api/v1/sessions \
  -H "Authorization: Bearer $PIGEONHOLE_TOKEN" \
  -d '{
    "title": "Acme Q3 Town Hall",
    "passcode": "ACME-Q3",
    "branding": {
      "logo": "https://acme.com/logo.png",
      "primaryColor": "#FF5500"
    },
    "qa": {
      "moderationLevel": "premoderation",
      "anonymous": false,    # internal town hall — names visible
      "upvoting": true,
      "exportToSharePoint": true
    }
  }'
```

### Recipe 7: Mentimeter polls + word cloud

Slido is moderated Q&A focus; Mentimeter is best for polls + word clouds in slide deck.

```bash
curl -X POST https://api.mentimeter.com/v1/presentations \
  -d '{
    "name": "DevConf Keynote Polls",
    "slides": [
      {
        "type": "word_cloud",
        "question": "What is the future of LLMs?"
      },
      {
        "type": "scales",
        "question": "Rate your confidence in LLM production safety",
        "scaleMin": 1,
        "scaleMax": 10
      },
      {
        "type": "open_ended",
        "question": "What is your team's biggest LLM challenge?"
      }
    ],
    "shareLink": true
  }'

# Mentimeter embeds via mentimeter.com/<code> in slide deck
```

### Recipe 8: AhaSlides (low-cost alternative)

```bash
# Free tier supports 7 participants per slide; paid for more
# Best for: lightning talks, workshops, low-budget events

curl -X POST https://api.ahaslides.com/v1/presentations \
  -d '{
    "name": "DevConf Lightning Round",
    "slides": [
      {"type": "live_qa", "question": "Q&A"}
    ]
  }'
```

### Recipe 9: Wooclap for education-focused events

```bash
# Wooclap has rich question types (matching, sorting, hotspot, scale)
curl -X POST https://app.wooclap.com/api/v1/events \
  -d '{
    "name": "DevConf Hands-On Workshop",
    "questions": [
      {"type": "multiple_choice", "question": "Which model is fastest for inference?"},
      {"type": "scale", "question": "How comfortable are you with Kubernetes?"},
      {"type": "hotspot", "question": "Where would you place a load balancer?"}
    ]
  }'
```

### Recipe 10: Post-event Q&A archive + analytics

```python
# Export all questions + answers + upvote counts
qa_export = requests.get(
    f'https://api.slido.com/v1/events/{EVENT_ID}/qa/export',
    headers={'Authorization': f'Bearer {SLIDO_TOKEN}'}
).json()

# Push to Notion as searchable archive
for q in qa_export['questions']:
    notion.create_db_row(
        database='qa-archive-2027',
        properties={
            'Session': q['session'],
            'Question': q['text'],
            'Author': q.get('author', 'Anonymous'),
            'Upvotes': q['upvotes'],
            'Status': q['status'],
            'Answer': q.get('answer', '')
        }
    )

# Analytics: questions per session, avg engagement, upvote distribution
import pandas as pd
df = pd.DataFrame(qa_export['questions'])
print(df.groupby('session').agg(
    questions=('id', 'count'),
    avg_upvotes=('upvotes', 'mean'),
    answered=('status', lambda x: (x == 'answered').sum())
))
```

### Recipe 11: Speaker prep with anticipated Q&A

Before the session, pre-load Slido with FAQ as "Suggested questions":

```bash
curl -X POST https://api.slido.com/v1/events/$EVENT_ID/qa/suggested \
  -d '{
    "session": "sarah-keynote-2027-09-15-09-00",
    "suggestedQuestions": [
      "How does your team handle LLM eval at scale?",
      "What is your stance on open vs closed models?",
      "How do you measure cost per inference?"
    ]
  }'
```

## Examples

### Example A: 600-attendee conference, 25 sessions, full Slido integration

```
Pre-event:
- 1 Slido event covers full conference
- 25 sessions configured with unique session IDs
- Pre-loaded polls per session (avg 2 per session)
- Suggested questions per session from speaker prep

Day-of:
- Slack moderator channel with 3 moderators (rotation)
- Avg 18 questions per session (range 5-45)
- Approval rate: 92% of questions
- Avg response time: 12 sec from submit to publish

Post-event:
- Top question per session highlighted in recording chapters
- Q&A archive searchable in Notion
- Analytics: 78% of attendees submitted at least 1 question
```

### Example B: 50-attendee executive briefing, Pigeonhole enterprise

```
Use case: customer advisory board, sensitive Q&A
Configuration: 
- Premoderation enabled (CEO reviews before publish)
- Anonymous off (board members named)
- Branded with customer logo
- Export to SharePoint for post-meeting review
Outcome:
- Avg 12 questions over 2-hour session
- All questions reviewed in real-time
- Sensitive ones held for follow-up; standard ones answered live
```

### Example C: Internal all-hands, anonymous Mentimeter

```
Use case: 5,000-employee town hall
Configuration:
- Anonymous on (employees feel safe asking)
- Word cloud + multi-choice polls
- Embedded in MS Teams Live Events
Result:
- 1,800 word-cloud contributions
- 3,200 poll votes
- 240 Q&A submissions
- CEO answered top 12 live; rest documented for blog
```

## Edge cases

### API access requires Enterprise tier
Slido / Pigeonhole API is gated behind Enterprise tier. For self-serve tier events, use the web UI only. Workaround: Mentimeter / AhaSlides have free API tiers.

### Moderation backlog
If questions arrive faster than moderators can review (>1 per 10 sec), backlog builds. Have 3+ moderators for events >300 attendees; pre-write canned response templates.

### Profanity / abuse filter false positives
Auto-filter may block legitimate questions ("how do you handle the f*** up?"). Manual override needed. Test pre-event with diverse vocabulary.

### Duplicate detection over-aggressive
Slido auto-merges similar questions. Sometimes merges 2 genuinely different questions. Moderator can split; don't trust auto-merge blindly.

### MC reading Q&A vs speaker reading
Best practice: MC reads questions aloud to speakers. Speaker reading from screen breaks eye contact. Set expectation in MC briefing.

### Question hijacking (sponsor pitches)
Sponsors sometimes submit questions that are vendor pitches. Reject if not genuinely curious. Note in MC brief: vendor-pitch questions get held.

### Privacy of question authors
Default to anonymous for external events. Internal town halls can show names if culture supports. Document at session start.

### Cross-language Q&A
For international events, questions may arrive in multiple languages. Use DeepL via `deepl-mcp` for real-time translation. Moderator triages.

### Audience too quiet
If no questions arrive in first 2 minutes, MC has filler questions ready (see `mc-host-prep`). Slido "suggested questions" feature can seed.

### Audience too loud (question overflow)
If >50 questions arrive per session, moderator picks top 5 by upvote + relevance. Don't try to answer all live; archive rest.

### Off-topic question waves
After controversial keynote, off-topic / political questions flood in. Moderator scope check: only this session's topic; flag others "great question for the closing panel."

### Lost connection to Slido
If venue wifi drops, Slido falls back to cellular. Have backup: paper question cards collected by ushers + read aloud by MC.

### Post-event archive privacy
For internal events, Q&A archive may include sensitive content. Restrict access in Notion. Some questions may be redacted post-event.

### Webhook delivery failure
Slack webhook may fail. Have backup polling job that pulls pending questions every 30 sec.

## Sources

- **Slido**: https://www.slido.com | API: https://community.slido.com/integrations-and-api-99
- **Pigeonhole Live**: https://www.pigeonhole.at
- **Mentimeter**: https://www.mentimeter.com
- **AhaSlides**: https://ahaslides.com
- **Wooclap**: https://www.wooclap.com
- **Kahoot**: https://kahoot.com
- **DeepL**: https://www.deepl.com (multi-language translation)
