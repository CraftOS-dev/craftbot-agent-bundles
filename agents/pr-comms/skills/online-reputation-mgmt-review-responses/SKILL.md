<!--
Source: https://developers.trustpilot.com/
G2 API: https://api.g2.com/
Glassdoor for Employers: https://www.glassdoor.com/employers/
-->
# Online Reputation Mgmt — Trustpilot / G2 / Glassdoor Review Responses — SKILL

Automated review pull + reply scaffolding for Trustpilot, G2, Glassdoor. Empathy + specific resolution = highest sentiment recovery rate. Negative reviews responded within 24 hours have 2-3x recovery rate vs unaddressed.

## When to use this skill

- **Negative review triage** — Trustpilot 1-2 star, G2 negative comments, Glassdoor employee complaints.
- **Positive review acknowledgement** — quick reply to validate + maintain relationship.
- **Reputation crisis** — review-bombing or coordinated negative campaign.
- **G2 vendor profile management** — managing G2 page, responding to reviews, tracking competitive positioning.
- **Glassdoor employer response** — engineering culture / leadership feedback responses.

**Do NOT use this skill when:**
- The "review" is actually a Twitter/Reddit thread — use `brand-reputation-monitoring-brandwatch-meltwater` + direct response.
- The review is a customer support escalation (active product issue) — defer to `customer-support-agent`.
- The review is from a verified press journalist — treat as press inquiry, use `journalist-outreach-cold-warm-embargoed`.

## Setup

### Trustpilot Business API

```bash
# Requires Trustpilot Business account ($299+/mo)
# https://business.trustpilot.com
export TRUSTPILOT_API_KEY="<key>"
export TRUSTPILOT_BUSINESS_UNIT_ID="<id>"
export TRUSTPILOT_API_BASE="https://api.trustpilot.com/v1"
```

### G2 API

```bash
# G2 vendor portal access required
# https://www.g2.com/vendor
export G2_API_TOKEN="<token>"
export G2_PRODUCT_ID="<product-id>"
export G2_API_BASE="https://api.g2.com/api/v1"
```

### Glassdoor for Employers

```bash
# https://www.glassdoor.com/employers — no public API
# Manual response via portal OR playwright-mcp automation
```

### App Store / Play Store reviews (mobile apps)

```bash
# Google Play Developer API
export GPLAY_SERVICE_ACCOUNT_JSON="<path-to-json>"
# Apple App Store Connect API
export APPSTORE_KEY_ID="<key-id>"
export APPSTORE_ISSUER_ID="<issuer-id>"
export APPSTORE_PRIVATE_KEY_PATH="<path-to-p8>"
```

### Notion review response DB

Per review:
- `platform` (select: Trustpilot, G2, Glassdoor, GPlay, AppStore, other)
- `review_id` (text, dedup key)
- `review_url` (URL)
- `reviewer_handle` (text)
- `review_date` (date)
- `rating` (number 1-5)
- `review_body` (rich text)
- `sentiment_topic` (multi-select: pricing, onboarding, support, bug, feature_request, leadership, work_life_balance)
- `severity` (select: critical, high, medium, low)
- `response_drafted_at` (datetime)
- `response_published_at` (datetime)
- `response_body` (rich text)
- `outcome` (select: response_only, reviewer_updated_rating, reviewer_deleted_review, no_change)

## Common recipes

### Recipe 1: Trustpilot review pull

```bash
# Pull all reviews from last 7 days
curl "$TRUSTPILOT_API_BASE/business-units/$TRUSTPILOT_BUSINESS_UNIT_ID/reviews?\
perPage=100&\
orderBy=createdat.desc&\
startDate=$(date -d '7 days ago' -I)" \
  -H "Authorization: Bearer $TRUSTPILOT_API_KEY" \
| jq '.reviews[] | {id, stars, title, text, consumer.name, createdAt, language}' \
> trustpilot_reviews.json

# Sync to Notion
jq -c '.[]' trustpilot_reviews.json | while read r; do
  notion-mcp upsert_page --db review_responses --properties "$r"
done
```

### Recipe 2: G2 review pull

```bash
curl "$G2_API_BASE/products/$G2_PRODUCT_ID/reviews?per_page=100&sort=date_desc" \
  -H "Authorization: Token $G2_API_TOKEN" \
| jq '.data[] | {id, rating, title, body_pros, body_cons, user.role, user.company_size, created_at}'
```

### Recipe 3: Triage by severity

```python
prompt = f"""
Classify this review for response prioritization.

REVIEW: {review['text']}
RATING: {review['rating']}/5

CLASSIFY:
- severity: critical / high / medium / low
- topic: [pricing, onboarding, support, bug, feature_request, leadership, work_life_balance, other]
- response_template: empathy / clarification / escalation / acknowledge
- requires_team_escalation: bool (route to product, support, HR?)
- target_response_time_hours: number

CRITICAL triggers: rating 1-2 + named exec + viral language ("worst experience", "going to court", "telling everyone")
HIGH: rating 1-2 + specific incident detail
MEDIUM: rating 3 OR generic negative comment
LOW: rating 4-5 (positive acknowledgment only)
"""
triage = claude(prompt)
```

### Recipe 4: Negative review response (empathy + specific resolution)

```python
prompt = f"""
Draft a response to this negative review.

REVIEWER: {reviewer_name}
RATING: {rating}/5
REVIEW BODY: {review_body}
ISSUE TOPIC: {topic}
OUR INTERNAL CONTEXT (NOT for response): {internal_status}

REQUIREMENTS:
- Open with reviewer's name (not "Hi there!")
- Acknowledge the specific issue (not generic "sorry to hear")
- Take ownership where appropriate (don't deflect)
- Offer SPECIFIC resolution (not "we'll look into it")
- Provide direct contact (named human, not "support@")
- Close with appreciation for honest feedback
- Tone: warm + direct + professional, not corporate

LENGTH: 80-150 words

BANNED:
- "We value your feedback" (corporate jargon)
- "Sorry for any inconvenience" (passive sympathy)
- "We're sorry you feel that way" (gaslighting)
- "Reach out to our support team" (deflection without specifics)
- Generic offers ("we'll do better")
"""
response = claude(prompt)
```

### Example good response:

```
Sarah —

Thank you for flagging the onboarding issue. You're right that the credentials sync error in step 3 is broken when the company has multiple OAuth domains — this is a known issue and we're shipping a fix in next week's release.

In the meantime, I'll have Maya (mlopez@acme.com), our onboarding lead, reach out personally Monday to walk you through a manual workaround. Use the time you've spent so far against your first month's invoice.

This kind of feedback is exactly what catches gaps we miss in QA — we appreciate you taking the time.

— Jane Chen, VP Customer Success
```

### Recipe 5: Positive review acknowledgment

```python
prompt = f"""
Draft a brief reply to this positive review.

REVIEWER: {reviewer_name}
RATING: {rating}/5
REVIEW BODY: {review_body}
WHAT THEY HIGHLIGHTED: {highlights}

REQUIREMENTS:
- Open with reviewer's name
- Reference SOMETHING SPECIFIC they mentioned (not generic "glad you like it")
- Brief thank-you
- Forward-looking offer ("if you ever want X, drop us a line")
- 40-80 words

BANNED:
- "We're so glad you love us"
- "Reviews like this make our day"
- Anything that sounds canned
"""
response = claude(prompt)
```

### Recipe 6: Publish response

```bash
# Trustpilot API
curl -X POST "$TRUSTPILOT_API_BASE/private/reviews/$review_id/reply" \
  -H "Authorization: Bearer $TRUSTPILOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"$response_body\"}"

# G2 API
curl -X POST "$G2_API_BASE/products/$G2_PRODUCT_ID/reviews/$review_id/responses" \
  -H "Authorization: Token $G2_API_TOKEN" \
  -d "{\"response\": \"$response_body\"}"

# Glassdoor — playwright-mcp (no API)
mcp tool playwright-mcp.browser_navigate --url "https://www.glassdoor.com/employers/dashboard/reviews"
# Login, navigate to review, paste response, submit

# Update Notion
notion-mcp update_row --filter "review_id=$review_id" \
  --response_published_at "$(date -Iseconds)" \
  --response_body "$response_body"
```

### Recipe 7: Critical / viral review escalation

```bash
# Severity = critical → page comms team immediately
slack-mcp send --channel "#comms-crisis" \
  --text "CRITICAL REVIEW: $platform | rating $rating | $review_url
Body: $review_body
Topic: $topic
Draft response below. Confirm before publish."

# Don't auto-publish critical responses. Human approval required.
# Pre-draft the response, send to Slack thread for sign-off, publish on approval.
```

### Recipe 8: Glassdoor automation via playwright-mcp

```javascript
// Glassdoor has no public API; playwright-mcp automates
const browser = await playwright.chromium.launch();
const page = await browser.newPage();
await page.goto('https://www.glassdoor.com/employers/dashboard/reviews');

// Auth (one-time storage state)
await page.context().storageState({ path: 'glassdoor_state.json' });

// Find unresponded reviews
const reviews = await page.$$('.review-card[data-responded="false"]');

for (const review of reviews) {
  const reviewText = await review.$eval('.review-body', el => el.textContent);
  const rating = await review.$eval('.rating', el => parseInt(el.textContent));

  // Generate response via Claude (per recipes 4/5)
  const response = await generateResponse(reviewText, rating);

  // Click "Respond"
  await review.$('.respond-button').click();
  await page.fill('textarea[name="response"]', response);
  await page.click('button:has-text("Submit Response")');

  // Screenshot for audit log
  await page.screenshot({ path: `glassdoor_responses/${reviewId}.png` });
}
```

## Examples — full reputation management program

```yaml
daily_cadence:
  0900_ET:
    - pull Trustpilot reviews from last 24h
    - pull G2 reviews from last 24h
    - pull Glassdoor via playwright (only T1 alerts auto-publish; rest human-approve)
    - pull GPlay + AppStore reviews if relevant

  1000_ET:
    - claude triages by severity
    - critical → slack page #comms-crisis
    - high → notion queue for human review + claude response draft
    - medium → notion queue + claude draft
    - low (positive) → claude generates short acknowledgment

  1100_ET:
    - PR lead reviews queued drafts
    - approves / edits / sends back

  1200_ET:
    - approved responses published via APIs
    - confirmation screenshots stored

weekly_cadence:
  - per-platform sentiment trend report
  - response time KPI (target <24hr for negative)
  - reviewer outcome tracking (did they update their review post-response?)

monthly_cadence:
  - per-topic analysis (what's most common complaint?)
  - feedback loop to product / support / HR
  - reputation score trend (Trustpilot TrustScore, G2 rating avg, Glassdoor overall)

quarterly_cadence:
  - review-bomb detection retrospective
  - response template effectiveness (which patterns earned highest update rate?)
  - update Notion templates per learning
```

## Edge cases

### 24-hour response window
Reviews responded within 24 hours have 2-3x recovery rate vs >7-day. Set hard SLA. Notion automation can ping if review > 24hr old without response.

### Personalization is non-negotiable
Generic responses ("Thank you for your feedback, we value all our customers") signal you didn't read the review. ALWAYS reference something specific from the review body. If you can't be specific, don't respond yet.

### Don't argue
A response is not the place to debate facts. Even if reviewer's claim is technically wrong, don't say "actually you're wrong because..." Acknowledge the perception, offer to discuss offline ("let's connect to walk through what happened"). Public arguments amplify.

### Take it offline for sensitive issues
If a review involves specific account details, billing dispute, security incident, or active investigation: brief public response + offer to take to private channel ("DM me at sarah@acme.com to share account details").

### Glassdoor sensitivity (employees)
Employee reviews touch culture + leadership. Tone matters more here than customer reviews. Don't sound corporate or defensive:
- Bad: "We take all feedback seriously and are committed to excellence"
- Good: "You're right that the on-call rotation has been heavy in Q1. We added 3 SRE hires in March and the load has improved; if you want to grab coffee and talk specifics, I'm at..."

### Review-bombing detection
Sudden spike (>5x normal rate) of 1-star reviews in <24hr = coordinated campaign. Don't respond individually; that amplifies. Instead:
1. Flag via `slack-mcp` to comms team
2. Report to platform (Trustpilot/G2 have report mechanisms for fake reviews)
3. Issue single public statement
4. Resume individual responses after surge subsides

### Fake review identification
Trustpilot/G2 verify reviewers but fakes leak through. Signals:
- New reviewer profile with only 1 review
- Generic language ("worst service ever, do not use")
- No specifics about product/feature
- Posted within minutes of competitor news

Report via platform; don't respond.

### Founder/CEO signed responses
For critical / viral reviews, CEO signature can de-escalate. Use sparingly — once a quarter at most. Hand off to `ceo-agent` for voice if so.

### Positive review amplification
Positive reviews with strong specifics can be requested for repurposing:
- "Hey Sarah, loved your review — would you be open to a 1-line quote for our website + a 60-min case study call?"
- Track in Notion `customer-reference-program-pr` skill DB

### Review platform algorithm gaming
Some platforms (G2) factor recent reviews more heavily into ranking. Encourage happy customers to leave reviews via:
- Post-onboarding email asking for honest review
- In-product NPS-triggered review request
- Customer success outreach

Don't incentivize reviews with discounts (terms of service violation).

### Cross-platform review consistency
Same reviewer may post on multiple platforms. Track via `reviewer_handle` or email match in Notion. Coordinated response across platforms (same reviewer, same response) prevents perception of inconsistency.

### Glassdoor anonymous reviews
Glassdoor reviewers are anonymous. Don't try to identify them via context clues; that's perceived as retaliation risk. Respond to the SUBSTANCE, not the reviewer.

### Compliance + legal review
Reviews involving discrimination, harassment, illegal activity claims → legal review BEFORE response. Standard generic acknowledgment ("We take this seriously and are reviewing internally") buys time.

### Response template library
Maintain Notion template library:
- Bug acknowledgment
- Pricing complaint
- Onboarding friction
- Feature request
- Positive acknowledgment
- Sensitive issue (legal-reviewed)

Templates speed response but personalize per recipe 4/5 every time.

### Track outcomes
Per response: did reviewer update their review? Delete it? Leave it as-is? Track in Notion. Refine templates based on what drives update rate.

## Sources

- **Trustpilot Business API**: https://developers.trustpilot.com/
- **G2 API**: https://api.g2.com/
- **Glassdoor for Employers**: https://www.glassdoor.com/employers/
- **Google Play Developer API**: https://developers.google.com/android-publisher/api-ref/rest
- **Apple App Store Connect API**: https://developer.apple.com/documentation/appstoreconnectapi
- **Review response best practices**: https://brand24.com/blog/brand-monitoring-tools/
- **Playwright docs (for Glassdoor automation)**: https://playwright.dev/
