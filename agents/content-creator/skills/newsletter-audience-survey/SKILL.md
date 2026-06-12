# Newsletter Audience Survey — Beehiiv Polls + Typeform / Tally Embedded

> Run audience surveys via Beehiiv built-in polls, Typeform / Tally embedded forms, or Kit-tagged segmented surveys.

## When to use

Trigger on: "survey my audience", "newsletter poll", "Typeform embed", "Tally form", "audience research", "what should I cover next", "subscriber feedback", "NPS for newsletter". This skill owns: survey design, embedding mechanics per newsletter platform, response analysis, follow-up cadence. For Notion CRM-style pipeline tracking of insights see `content-calendar-notion-db`. For broader growth-loop optimization see `newsletter-subscriber-growth`.

## Setup

```bash
# Beehiiv polls — native (no API; in-issue widget)
# Configure when authoring a post

# Typeform API
curl -H "Authorization: Bearer $TYPEFORM_API_KEY" \
  https://api.typeform.com/me

# Tally — free / cheaper alternative
curl -H "Authorization: Bearer $TALLY_API_KEY" \
  https://api.tally.so/forms

# Kit (ConvertKit) — for tag-segmented surveys
curl -d "api_secret=$KIT_API_SECRET" \
  https://api.convertkit.com/v3/forms
```

Auth env vars:
- `TYPEFORM_API_KEY` — Typeform Pro+ for API access.
- `TALLY_API_KEY` — Tally Pro plan for API; free plan covers 200 responses/month.
- `BEEHIIV_API_KEY` — for embedding polls into Beehiiv posts.
- `KIT_API_SECRET` — for tag-based survey routing.

## Common recipes

### Recipe 1: Quarterly state-of-audience survey

```markdown
# Quarterly Audience Survey: <Newsletter Name>

## Goal
- Understand who's actually reading
- Identify content topics that resonate
- Flag pricing-sensitivity and willingness-to-pay
- Surface unmet needs

## Cadence
- Once per quarter (4×/year)
- Sent to engaged subs (opened ≥3 of last 10 issues)
- Targeted incentive: free PDF / 1:1 / lottery for $200 gift card

## 8-12 question structure
1. (Demographics) What's your role? [single-select]
2. (Demographics) What size company? [single-select]
3. (Demographics) How long have you been a subscriber? [single-select]
4. (Engagement) How often do you read? [Likert 1-5]
5. (Content) Which 3 topics resonate most? [multi-select with 6 options]
6. (Content) What topic should I cover that I'm not? [open-ended]
7. (Format) Preferred length? [Short / Medium / Long]
8. (Pricing) Would you pay for premium content? [Yes / No / Maybe + price range]
9. (Pricing) If yes, what would justify $X/month? [open-ended]
10. (Frequency) Current cadence is right? [Too often / Right / Too rare]
11. (Quote) Best moment from the newsletter? [open-ended for testimonials]
12. (NPS) Would you recommend? [0-10 scale]
```

### Recipe 2: Beehiiv built-in poll (in-issue widget)

```bash
# Add a Beehiiv poll to a post via the post API
curl -X POST "https://api.beehiiv.com/v2/publications/$BEEHIIV_PUBLICATION_ID/posts" \
  -H "Authorization: Bearer $BEEHIIV_API_KEY" \
  -d '{
    "title":"Issue 042",
    "content":{"free":{"html":"<p>What should I write about next?</p><poll question=\"Pick one\" options=\"Newsletter strategy|Podcast SOTA|Repurposing tools|Other\"></poll>"}}
  }'

# Pull poll results post-publish
curl -H "Authorization: Bearer $BEEHIIV_API_KEY" \
  "https://api.beehiiv.com/v2/publications/$BEEHIIV_PUBLICATION_ID/posts/<post_id>/poll_results"
```

In-issue polls have 3-5× higher response rate than embedded external forms because zero friction (single click in the email).

### Recipe 3: Typeform embedded survey

```bash
# Create a form via Typeform API
curl -X POST https://api.typeform.com/forms \
  -H "Authorization: Bearer $TYPEFORM_API_KEY" \
  -d @form_definition.json
```

`form_definition.json` partial example:

```json
{
  "title": "State of <Audience> 2026",
  "fields": [
    {
      "title": "What's your role?",
      "type": "multiple_choice",
      "properties": {
        "choices": [
          {"label": "Founder / CEO"},
          {"label": "Marketing / growth"},
          {"label": "Product / engineering"},
          {"label": "Operations"},
          {"label": "Other"}
        ]
      }
    },
    {
      "title": "Would you pay for a premium tier?",
      "type": "yes_no"
    }
  ]
}
```

Embed in Beehiiv post or link from newsletter.

### Recipe 4: Tally free alternative

```bash
# Tally is cheaper / simpler; good for non-conditional surveys
curl -X POST https://api.tally.so/forms \
  -H "Authorization: Bearer $TALLY_API_KEY" \
  -d '{
    "title": "State of <Audience> 2026",
    "fields": [
      {"type": "MULTIPLE_CHOICE", "label": "What's your role?", "options": [...]}
    ],
    "public": true
  }'
```

### Recipe 5: Pull responses (Typeform)

```bash
curl -H "Authorization: Bearer $TYPEFORM_API_KEY" \
  "https://api.typeform.com/forms/<form_id>/responses?page_size=1000" \
  | jq '.items[] | {submitted_at, answers}'
```

### Recipe 6: Pull responses (Tally)

```bash
curl -H "Authorization: Bearer $TALLY_API_KEY" \
  "https://api.tally.so/forms/<form_id>/submissions"
```

### Recipe 7: Kit tag-segmented surveys

```bash
# Send different surveys to different segments based on tag
# E.g., "Engaged" subs get strategy survey; "Cold" subs get re-engagement survey

# Trigger Kit broadcast to a specific tag
curl -X POST "https://api.convertkit.com/v3/broadcasts" \
  -d "api_secret=$KIT_API_SECRET" \
  -d "subject=Quick 2-min survey?" \
  -d "content=<a href='<TYPEFORM_URL>'>Take the survey →</a>" \
  -d "subscriber_filter[tags][]=<engaged_tag_id>"
```

### Recipe 8: Response analysis (sentiment + clustering)

```python
import json, re
responses = json.load(open('survey_responses.json'))
open_ended = [r['What topic should I cover'] for r in responses if r.get('What topic should I cover')]

# Theme clustering via Claude
prompt = f"Cluster these {len(open_ended)} responses into 5-7 themes. List each theme + count + 2-3 verbatim quotes.\n\nResponses:\n" + "\n".join(open_ended[:200])

# Send to Claude API; output → Notion content backlog DB
```

### Recipe 9: NPS calculation

```python
nps_responses = [r['Would you recommend (0-10)'] for r in responses if 'Would you recommend' in r]
promoters = len([n for n in nps_responses if n >= 9])
passives = len([n for n in nps_responses if 7 <= n <= 8])
detractors = len([n for n in nps_responses if n <= 6])
nps = (promoters - detractors) / len(nps_responses) * 100
print(f"NPS: {nps:.0f} (promoters {promoters}, passives {passives}, detractors {detractors})")
```

NPS benchmarks for newsletters: 30+ = solid, 50+ = exceptional, <0 = restructure.

### Recipe 10: Survey + incentive

```markdown
## Incentives that boost response rate

- **Lottery (1 of 100)**: $200 gift card → 15-25% response rate
- **PDF lead magnet**: "Get the survey results report" → 10-20%
- **1:1 consultation slot**: 1 winner gets a 30-min call → 8-15%
- **Branded merch**: T-shirt / stickers → 5-10%
- **No incentive**: 2-5% baseline

## SOTA approach for serious surveys
- 60-day "we've heard you" report sent to all respondents
- Include 3 changes you'll make based on feedback
- This builds trust + signals you actually read responses
```

### Recipe 11: "We heard you" follow-up

```markdown
# After-survey newsletter issue: "What you told me + what I'll change"

## Top themes from responses
1. <Theme 1> — N responses
2. <Theme 2> — N responses
3. <Theme 3> — N responses

## What I'm changing
- Change 1: <specific action + timeline>
- Change 2: <...>

## What I'm NOT changing (and why)
- <pushback or trade-off explanation>

## NPS / engagement stats
- NPS: <score>
- Reply rate: <%>
- Open-ended response rate: <%>

## Thanks
- <names of winners / shoutouts to specific helpful responses>
```

### Recipe 12: Embed Typeform in Beehiiv post

```html
<!-- Beehiiv post HTML -->
<p>I'd love your input on what to cover next.</p>
<a href="https://yourform.typeform.com/to/abc123?email={{subscriber_email}}" target="_blank">
  <button style="background:#FF6B35;color:#fff;padding:12px 24px;border-radius:8px;">Take the 2-min survey →</button>
</a>
```

`{{subscriber_email}}` is a Beehiiv merge tag → auto-fills email field in Typeform so respondents don't have to.

## Examples

### Example 1: Quarterly state-of-audience survey

**Goal:** Q3 audience survey to inform Q4 content roadmap.

**Steps:**
1. Recipe 1: design 10-question survey.
2. Recipe 3: build in Typeform; configure email pass-through.
3. Recipe 10: add $200 lottery incentive.
4. Send via Recipe 12 embed in Beehiiv issue tagged "engaged" subs (Recipe 7).
5. 14 days: pull responses (Recipe 5).
6. Recipe 8: cluster open-ended into themes.
7. Recipe 9: compute NPS.
8. Recipe 11: send "we heard you" issue summarizing + announcing changes.
9. Update content calendar (`content-calendar-notion-db`) with top themes.

**Result:** Audience-driven content roadmap + boosted trust through "I read your feedback."

### Example 2: In-issue Beehiiv poll for fast feedback

**Goal:** Quick "which topic next" poll without external form.

**Steps:**
1. Recipe 2: embed Beehiiv poll in issue.
2. Send issue.
3. Pull results 72h later.
4. Use top-vote topic for next issue.

**Result:** 30-40% poll response rate (vs 2-5% external form); immediate signal.

### Example 3: NPS tracking quarterly

**Goal:** Track NPS over time as a leading indicator of newsletter health.

**Steps:**
1. Single-question survey: "Would you recommend (0-10)?"
2. Send to all engaged subs once per quarter.
3. Recipe 9: compute NPS each quarter.
4. Plot trend in Notion dashboard.
5. NPS drop >10 points = restructure trigger.

**Result:** Early-warning system before churn manifests.

## Edge cases / gotchas

- **Beehiiv in-issue polls have 3-5× higher response rate** than external forms (zero friction).
- **Typeform free tier = 10 fields max** + 100 responses/month. Pro tier ($25/mo) for serious surveys.
- **Tally free tier = unlimited fields** + 200 responses/month. Cheaper for high-volume.
- **Don't survey more than once per quarter** for full surveys — fatigue tanks response rate.
- **Open-ended questions raise response time** — keep to 1-2 per survey, place mid-form (not at start).
- **Pass through sub email** to pre-fill so respondents don't have to retype.
- **Incentives matter** — see Recipe 10. No incentive = 2-5% response rate.
- **Anchor questions matter** — first question sets engagement. Start with multiple-choice, not open-ended.
- **Survey response biases skew engaged** — your survey results = your most active 10% of subs, not the silent majority. Account for this.
- **Don't survey cold subs** without re-engaging first — they'll either ignore or give random answers.
- **NPS for newsletters is weaker signal than CTR + churn** — use as directional, not primary.
- **"We heard you" follow-up is critical** for trust — promising changes and not delivering = trust kill.
- **Quote responses verbatim in follow-up** (with permission) — boosts validation.
- **Survey results inform content backlog**, not direct roadmap — top votes are noisy. Combine survey + analytics + your editorial judgment.
- **GDPR / CCPA compliance** — if pulling EU data, anonymize; offer opt-out; don't store PII beyond survey window.

## Sources

- [Typeform API docs](https://developer.typeform.com/)
- [Tally API docs](https://tally.so/help/api)
- [Beehiiv polls](https://support.beehiiv.com/hc/en-us/articles/15064229843991-Polls)
- [Kit (ConvertKit) v3 API](https://developers.convertkit.com/)
- [NPS methodology — Bain](https://www.netpromoter.com/know/)
- [Newsletter audience research best practices](https://www.knockedupmoney.com/blog/convertkit-vs-beehiiv-whats-the-best-newsletter-platform)
- [Survey response rate benchmarks](https://surveyanyplace.com/blog/survey-response-rates/)
