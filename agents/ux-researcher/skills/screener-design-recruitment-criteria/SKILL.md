<!--
Sources:
User Interviews screener template — https://www.userinterviews.com/blog/screener-survey-template
Respondent screener guide — https://respondent.io/help/researcher-faqs
Erika Hall — recruitment hygiene
NN/g — screener pitfalls — https://www.nngroup.com/articles/screening-research-participants/
-->
# Screener Design + Recruitment Criteria — SKILL

Build a screener that selects the *right* segment without telling participants the answer. Three rules: 1-3 must-have behavioral criteria, anti-screen for pros, no leading questions. Output: ready-to-push JSON for User Interviews / Respondent / Prolific / Ethnio.

## When to use

- Writing a screener for any moderated or unmoderated study.
- Building anti-screens against professional respondents and competitors.
- Routing a screener to the right panel platform.
- Pushing a screener via the User Interviews / Respondent / Prolific / Ethnio API.

Trigger phrases: "write a screener", "recruit criteria for X", "screen out pros", "anti-screen", "screener JSON for User Interviews", "in-product intercept screener".

## Setup

```bash
# User Interviews
curl -fsSL "https://api.userinterviews.com/v1/me" \
  -H "Authorization: Bearer $USER_INTERVIEWS_API_KEY"

# Respondent
curl -fsSL "https://api.respondent.io/v1/me" \
  -H "Authorization: Bearer $RESPONDENT_API_KEY"

# Prolific
curl -fsSL "https://api.prolific.com/api/v1/users/me/" \
  -H "Authorization: Token $PROLIFIC_API_TOKEN"

# Ethnio (in-product intercept)
curl -fsSL "https://ethn.io/api/v1/screeners" \
  -H "Authorization: Bearer $ETHNIO_API_KEY"
```

Auth:
- `USER_INTERVIEWS_API_KEY` — Settings → API. Paid plan.
- `RESPONDENT_API_KEY` — Researcher dashboard.
- `PROLIFIC_API_TOKEN` — Settings → Workspace → API tokens.
- `ETHNIO_API_KEY` — Account → API. Paid (~$249/mo).

## Common recipes

### Recipe 1: Screener template (paste-ready)

```markdown
# Screener: [Study Name]

**Incentive:** $[X] for [60-min] session

## Intro
We're [company / researcher] conducting a study on [topic]. Eligible participants receive [incentive]. Study is [duration]. All data is confidential. You can withdraw anytime.

## Must-have criteria (gating — auto-reject if fail)
1. [Behavior — e.g., "Used a CRM tool weekly in the last 30 days"]
2. [Segment — e.g., "Solo founder OR PM at a company <50 employees"]
3. [Context — e.g., "Have hired someone in the last 12 months"]

## Anti-screens (auto-reject)
- Works in market research / UX research / advertising agency (professional respondent guard)
- Earns >50% of income from study participation (panel pollution guard)
- Has participated in our research in the last 90 days
- Works for [competitor list] (B2B competitive guard)

## Demographics (collect, don't gate)
- Role: [open or multi-select]
- Company size: [bands]
- Years in role: [bands]
- Location: [country / region — match study scope]

## Availability
- Preferred time slots: [Calendly link]
- Recording consent: [checkbox + consent language]
- Communication preference: [email / SMS]

## Closing
Thanks. We'll be in touch within [N business days].
```

### Recipe 2: Push the screener to User Interviews

```bash
PROJECT_ID="<ui-project-id>"

curl -X POST "https://api.userinterviews.com/v1/projects/$PROJECT_ID/screener" \
  -H "Authorization: Bearer $USER_INTERVIEWS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "questions": [
      {
        "type": "single_select",
        "text": "How often do you use a CRM tool (Salesforce, HubSpot, Pipedrive, etc.)?",
        "options": [
          {"label": "Daily", "qualifies": true},
          {"label": "Weekly", "qualifies": true},
          {"label": "Monthly", "qualifies": false},
          {"label": "Never", "qualifies": false}
        ],
        "required": true
      },
      {
        "type": "single_select",
        "text": "What is your current role?",
        "options": [
          {"label": "Solo founder / co-founder", "qualifies": true},
          {"label": "Product Manager at <50-person company", "qualifies": true},
          {"label": "Product Manager at 50+ person company", "qualifies": false},
          {"label": "Other", "qualifies": false}
        ],
        "required": true
      },
      {
        "type": "single_select",
        "text": "Do you work in market research, UX research, or advertising?",
        "options": [
          {"label": "Yes", "qualifies": false},
          {"label": "No", "qualifies": true}
        ],
        "required": true,
        "tag": "anti_screen_professional"
      }
    ],
    "incentive_amount": 100,
    "session_duration_minutes": 60
  }'
```

### Recipe 3: Push to Respondent (B2B specialist)

```bash
curl -X POST "https://api.respondent.io/v1/projects/$PROJECT_ID/criteria" \
  -H "Authorization: Bearer $RESPONDENT_API_KEY" \
  -d '{
    "industry": ["technology", "saas"],
    "company_size": ["1-10", "11-50"],
    "role": ["founder", "product_manager", "head_of_product"],
    "tool_usage": ["salesforce", "hubspot", "pipedrive"],
    "exclusions": ["market_research", "ux_research"],
    "incentive": 100,
    "minimum_quality_score": 4.5
  }'
```

### Recipe 4: Push to Prolific (behavioral science / academic)

```bash
curl -X POST "https://api.prolific.com/api/v1/studies/" \
  -H "Authorization: Token $PROLIFIC_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Inbox overload qualitative — Q3 2026",
    "internal_name": "inbox-q3",
    "description": "30-min interview on email habits. £15 for participation.",
    "external_study_url": "https://your-calendly-link",
    "prolific_id_option": "url_parameters",
    "completion_codes": [{"code": "ABCD1234", "code_type": "COMPLETED"}],
    "total_available_places": 12,
    "estimated_completion_time": 30,
    "reward": 1500,
    "device_compatibility": ["desktop", "tablet"],
    "filters": [
      {"filter_id": "current-country-of-residence", "selected_values": ["1", "8", "21"]},
      {"filter_id": "fluent-languages", "selected_values": ["1"]}
    ]
  }'
```

### Recipe 5: In-product intercept screener via Ethnio

```bash
# Ethnio screener — banner shown to traffic matching URL + behavior rules
curl -X POST "https://ethn.io/api/v1/screeners" \
  -H "Authorization: Bearer $ETHNIO_API_KEY" \
  -d '{
    "name": "Inbox feature intercept Q3",
    "targeting": {
      "url_pattern": "*/app/inbox*",
      "min_sessions": 3,
      "country": ["US", "CA", "GB"]
    },
    "questions": [
      {"type": "single_select", "text": "How often do you use our inbox?", "options": ["Daily", "Weekly", "Less"]},
      {"type": "open_text", "text": "What email or notification problem are you trying to solve right now?"}
    ],
    "incentive": "$50 Amazon gift card for 30-min interview",
    "calendly_redirect": "https://calendly.com/your-link"
  }'
```

### Recipe 6: Anti-screen quality matrix

| Risk | Anti-screen question | Auto-reject if answer is |
|---|---|---|
| Professional respondents | "Do you work in market research, UX research, or advertising?" | Yes |
| Panel pollution | "What % of your income comes from research studies?" | >50% |
| Repeat respondent | "Have you participated in our company's research in the last 90 days?" | Yes |
| Competitor sourcing (B2B) | "What company do you currently work for?" | Listed competitor or industry analyst firm |
| Coached respondents | "Have you used [our specific product] before?" (if no = unbiased) | Per study scope |
| Insufficient context (behavior) | "Walk me through what you did the last time you [target behavior]." | Vague / generic answer = soft-reject |
| Pre-disposed answer | Phrase question behaviorally not preference-based | n/a (rephrase, don't gate) |

### Recipe 7: Leading-question rewrite cheat sheet

| Leading (bad) | Behavioral (good) |
|---|---|
| "Are you interested in trying new productivity tools?" | "Walk me through the tools you tried in the last 6 months." |
| "Do you struggle with email overload?" | "How many emails did you receive yesterday? How many did you read?" |
| "Would you pay for a premium tier?" | "Tell me about the last subscription you bought for work." |
| "Do you find the current solution easy?" | "Walk me through how you used [tool] yesterday." |

### Recipe 8: Demographic balance for behavioral panels

When recruiting for behavioral patterns, balance demographics so findings don't over-fit:

```python
# Quota example — 12 interviews for solo-founder JTBD
QUOTAS = {
    "company_stage": {"pre-seed": 3, "seed": 4, "series_a": 3, "bootstrapped": 2},
    "location": {"north_america": 6, "europe": 4, "other": 2},
    "current_tool": {"hubspot": 4, "salesforce": 2, "pipedrive": 2, "spreadsheet": 4},
}

# Use User Interviews / Respondent quota fields, or screen manually
```

### Recipe 9: GDPR + recording consent block

Every screener has this. Non-negotiable.

```markdown
## Consent
- I understand that I'm participating in a research study.
- I understand the session will be recorded for internal research only.
- I can withdraw at any time without giving a reason.
- I understand my data will be stored per GDPR / CCPA + deleted after [N months].
- I am 18 years or older.
[ ] I consent to the above.

## Contact (optional)
- I'd like to be contacted for future research: [yes / no]
```

### Recipe 10: Screener QA before launch

Before pushing live:

1. **Read the screener aloud** — does any question reveal the answer?
2. **Test the auto-reject paths** — submit as a professional respondent; verify rejection
3. **Check incentive amount vs market** — $50/30min for consumer, $100-200/60min for B2B, $200-500 for senior buyers
4. **Pilot with 2 internal users** — flag confusing wording before paid recruit starts

## Examples

### Example 1: Screener for solo-founder JTBD study
**Goal:** Recruit 12 solo founders for 60-min JTBD interviews.

**Steps:**
1. Write screener (Recipe 1) with 3 must-haves: solo founder, $50-200K ARR, used CRM in 30 days.
2. Add anti-screens (Recipe 6).
3. Push to Respondent (Recipe 3) for B2B specialist panel.
4. QA the screener (Recipe 10).
5. Launch; recruit batch of 16 (over-recruit for no-shows).

**Result:** 12 high-quality interviews booked within a week.

### Example 2: In-product intercept for inbox feedback
**Goal:** Recruit 10 active users from the inbox feature for 30-min interviews.

**Steps:**
1. Set URL pattern + min-sessions targeting (Recipe 5).
2. Behavioral questions only — no preference (Recipe 7).
3. Ethnio routes to Calendly post-screen.
4. Cap at 10; recruit closes auto.

**Result:** Users who actually use the feature, not what they think about it.

## Edge cases / gotchas

- **Telling participants the answer.** "We're testing the new inbox" attracts pros; say "we're studying email habits" instead.
- **Demographic-only screeners.** "Female, 25-40, tech-savvy" yields noise. Screen on behavior.
- **Compensation too low.** <$30/hr for consumer = pros only respond. B2B <$100/hr = senior people skip.
- **Incentive too high.** $500 for a 30-min consumer interview attracts professional respondents in droves.
- **Friends-and-family.** Recruiting from your network = bias. Use panel for unbiased recruit.
- **Single-channel recruit.** All from Twitter = Twitter-bubble bias. Mix sources.
- **No anti-screen for the obvious.** B2B competitive study without competitor anti-screen = leaks.
- **Quota over-rigidity.** Quotas that block real-world respondents (e.g., "must be exactly Series A") leave you short.
- **GDPR-blind recruitment.** Always require consent for recording + data retention.
- **Recruiting too many at once.** Send 16 invites for 12 slots; over-invite for 25-30% no-show rate.
- **Pilot the screener.** Internal pilot catches confusing wording before paid recruit pays the cost.

## Sources

- [User Interviews screener template](https://www.userinterviews.com/blog/screener-survey-template)
- [User Interviews API](https://www.userinterviews.com/api)
- [Respondent API](https://respondent.io/help)
- [Prolific API docs](https://docs.prolific.com)
- [Ethnio API](https://ethn.io/api)
- [NN/g — Recruiting Test Participants](https://www.nngroup.com/articles/screening-research-participants/)
- [Erika Hall — Just Enough Research](https://abookapart.com/products/just-enough-research)
- [Rob Fitzpatrick — The Mom Test](https://www.momtestbook.com)
