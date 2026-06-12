<!--
Source: https://www.onlinewritingclub.com/p/the-linkedin-substack-strategy-for
LinkedIn Marketing API: https://learn.microsoft.com/en-us/linkedin/marketing/overview
Substack: https://substack.com/
Beehiiv: https://www.beehiiv.com/
-->
# Executive Thought Leadership — LinkedIn Newsletter + Substack — SKILL

Cross-post executive long-form content from LinkedIn Newsletters (top-of-funnel reach + native distribution) and Substack/Beehiiv (owned email list + monetization). 2026 best practice: LinkedIn for discoverability, Substack/Beehiiv for audience ownership. Vale brand-voice + AI-slop lint mandatory pre-publish.

## When to use this skill

- **Monthly exec long-form newsletter** — 800-2,000 words, deep POV on industry trend.
- **CEO industry commentary** — response to a major industry event (acquisition, regulation, public earnings).
- **Founder narrative arc** — "what we learned" / "how we built it" / "what we got wrong" series.
- **Substack cross-publication** — every LinkedIn newsletter mirrors to owned Substack.
- **Real-time POV on news** — short-form LinkedIn post (handoff to `twitter-mcp` for X threads).

**Do NOT use this skill when:**
- The piece is a press release — use `press-release-writing-distribution`.
- The piece is a contributed op-ed in a third-party outlet (Forbes Contributor, HBR, FastCo) — use `op-ed-contributed-article-placement`.
- The piece is product marketing or feature announcement (defer to `marketing-agent`).

## Setup

### LinkedIn Marketing API (Newsletters endpoint)

```bash
# Requires Community Management API approval (~5-15 business days)
# Auth: 3-legged OAuth, scopes: w_member_social, r_member_social
export LINKEDIN_ACCESS_TOKEN="<token>"
export LINKEDIN_PERSON_URN="urn:li:person:<id>"   # for personal exec posts
export LINKEDIN_ORG_URN="urn:li:organization:<id>" # for company newsletters
export LINKEDIN_NEWSLETTER_ID="<newsletter-id>"    # one-time setup via UI
```

Newsletter object created first via LinkedIn UI (cannot create via API). Once created, publish via `/rest/articles`.

### Substack API

```bash
# Substack writer access setup
export SUBSTACK_PUBLICATION="acme-ceo-newsletter.substack.com"
export SUBSTACK_API_KEY="<key>"   # from Substack writer dashboard
```

Substack API is unofficial / partial; for guaranteed automation, use email-to-post relay or the Substack Sites API where available.

### Beehiiv API (better alternative for analytics + monetization)

```bash
export BEEHIIV_PUBLICATION_ID="<id>"
export BEEHIIV_API_KEY="<key>"
export BEEHIIV_API_BASE="https://api.beehiiv.com/v2"
```

### Vale brand-voice lint

```bash
uvx vale --config=.vale.ini --output=JSON article.md
# Rules: ban AI slop, em-dash density, banned openers
```

### Editorial calendar in Notion

DB schema:
- `title` (text)
- `exec` (select: CEO, CTO, etc.)
- `topic_pillar` (multi-select: industry-trend, customer-story, lessons-learned, real-time)
- `pub_date` (date)
- `linkedin_newsletter_url` (url)
- `substack_url` (url)
- `beehiiv_url` (url)
- `status` (select: draft, review, scheduled, published)
- `vale_score` (number)
- `metrics_30d` (rich text: reactions, comments, subscribers gained)

## Common recipes

### Recipe 1: LinkedIn Newsletter publish

```bash
mcp tool linkedin.create_article \
  --author "$LINKEDIN_PERSON_URN" \
  --newsletterId "$LINKEDIN_NEWSLETTER_ID" \
  --title "What We Learned Shipping AI Infrastructure to 200 Customers" \
  --content "$(cat article.html)" \
  --coverImage "@cover.jpg" \
  --publish true
```

Requirements:
- 250+ word minimum (LinkedIn rejects shorter)
- Cover image 1280x720
- Subscribers auto-notified
- Newsletter object must exist first (via UI setup)

### Recipe 2: Substack cross-post

```bash
# Substack API is limited; common approach is markdown → HTML → POST
curl -X POST "https://substack.com/api/v1/publications/$SUBSTACK_PUBLICATION/posts" \
  -H "Authorization: Bearer $SUBSTACK_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"What We Learned Shipping AI Infrastructure to 200 Customers\",
    \"subtitle\": \"Three convictions after 18 months.\",
    \"body_html\": \"$(cat article.html | jq -Rs .)\",
    \"is_published\": true,
    \"send_email\": true,
    \"audience\": \"everyone\"
  }"
```

Fallback if Substack API rejects: use Substack's email-to-post (send formatted email to `<pub>@substack.com` from authorized writer email).

### Recipe 3: Beehiiv publish (preferred when monetization in play)

```bash
curl -X POST "$BEEHIIV_API_BASE/publications/$BEEHIIV_PUBLICATION_ID/posts" \
  -H "Authorization: Bearer $BEEHIIV_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "What We Learned Shipping AI Infrastructure to 200 Customers",
    "subtitle": "Three convictions after 18 months.",
    "content": {"html": "<full HTML body>"},
    "scheduled_at": "2026-06-15T13:00:00Z",
    "audience": "free",
    "thumbnail_url": "https://acme.com/newsletters/jun-cover.jpg"
  }'
```

Beehiiv exposes analytics (open rates, click rates, subscriber growth) via API; Substack analytics require UI scrape.

### Recipe 4: Article draft via Claude with strict POV requirements

```python
prompt = f"""
You are drafting a 1500-word executive thought leadership piece for {exec['name']},
{exec['title']} at Acme Corp.

TOPIC: {topic}
POV: {clear_position}
EVIDENCE: {data_points}
RECENT EXAMPLES: {examples}
AUDIENCE: {audience_description}

REQUIREMENTS:
- Substantive POV in first 2 sentences. No hedging.
- 1 specific data point per section
- 1 named customer/example per section (with permission)
- First-person voice — direct statement, not "as a CEO I think"
- Structure: Hook → Position → 3 supporting arguments with evidence → Forward-looking close
- 1500 words ±200

BANNED:
- "Thrilled to announce", "in today's fast-paced world", "look no further than"
- "Leverage", "utilize", "synergize", "best-in-class", "game-changing"
- Sycophancy ("amazing", "great"), AI-slop transitions ("moreover", "furthermore")
- Em-dashes >1 per paragraph
- Passive voice chains
- Generic listicles without a thesis
"""
draft = claude(prompt)
```

### Recipe 5: Vale brand-voice lint + AI-slop strip

```bash
# Run Vale before publish
uvx vale --config=.vale.ini --output=JSON article.md > vale_results.json

# Quality gate: vale_score must be 0 errors, <5 warnings
errors=$(jq '[.[][] | select(.Severity == "error")] | length' vale_results.json)
warnings=$(jq '[.[][] | select(.Severity == "warning")] | length' vale_results.json)

if [ "$errors" -gt 0 ] || [ "$warnings" -gt 5 ]; then
  echo "Vale gate failed: $errors errors, $warnings warnings. Fix before publish."
  jq -r '.[][] | "\(.Severity): \(.Message) (line \(.Line))"' vale_results.json
  exit 1
fi
```

### Recipe 6: Cross-post sequence (LinkedIn first, Substack second)

```bash
# Order matters: LinkedIn first (canonical) -> Substack second to avoid SEO duplicate

# Step 1: LinkedIn publish
linkedin_url=$(mcp tool linkedin.create_article ... | jq -r .article_url)

# Step 2: Append LinkedIn canonical link to Substack version footer
sed -i "s|<!--CANONICAL-->|<p><em>Originally published on <a href=\"$linkedin_url\">LinkedIn</a>.</em></p>|" substack_article.html

# Step 3: Substack publish 24-48 hours later (avoid LinkedIn algo penalty for cross-post velocity)
sleep 86400 # 24 hr
substack_url=$(curl -X POST "https://substack.com/api/v1/publications/$SUBSTACK_PUBLICATION/posts" ... | jq -r .url)

# Step 4: Update Notion editorial calendar
notion-mcp update_row --filter "title=$title" \
  --linkedin_url "$linkedin_url" \
  --substack_url "$substack_url" \
  --status "published"
```

### Recipe 7: 30-day metrics pull

```bash
# LinkedIn article analytics
linkedin_analytics=$(mcp tool linkedin.get_article_analytics \
  --articleUrn "urn:li:article:<id>" \
  --period "30d")

# Beehiiv analytics
beehiiv_analytics=$(curl "$BEEHIIV_API_BASE/publications/$BEEHIIV_PUBLICATION_ID/posts/$post_id/stats" \
  -H "Authorization: Bearer $BEEHIIV_API_KEY")

# Substack analytics (UI scrape via firecrawl)
substack_analytics=$(firecrawl scrape --url "https://substack.com/dashboard/$SUBSTACK_PUBLICATION/posts/$slug")

# Combine into Notion row
notion-mcp update_row --filter "title=$title" \
  --metrics_30d "$(combine_metrics.py)"
```

### Recipe 8: Editorial calendar planning (quarterly)

```python
# Generate next-quarter editorial calendar with Claude
prompt = f"""
Build a 12-week editorial calendar for {exec['name']} ({exec['title']}, Acme Corp).

CADENCE:
- 1 LinkedIn newsletter / month (long-form 800-2000 words)
- 2-3 LinkedIn posts / week (substantive 800-2000 chars; not in this skill)
- 1 Substack cross-post / month (mirror of newsletter)

TOPIC MIX (per role.md):
- 40% industry trends + POV
- 30% customer/product evidence (with permission)
- 20% behind-the-scenes / lessons learned
- 10% real-time commentary on industry news

INPUTS:
- Industry events upcoming: {events}
- Company milestones: {milestones}
- Recent customer wins: {customers}
- Recent lessons: {lessons}
- Current public POV: {position}

OUTPUT 12 newsletter titles + 1-line summary per title.
"""
calendar = claude(prompt)
```

## Examples — full editorial program

```yaml
exec: Jane Smith, CEO Acme Corp
cadence:
  linkedin_newsletter: monthly (1st Wednesday)
  substack_crosspost: 48-hour delay (3rd Wednesday)
  linkedin_posts: Mon/Wed/Fri (via separate handle / writing-assistant skill)
  twitter_threads: 3-5/week (separate via twitter-mcp)

topic_pillars:
  - industry_trends: 40% (e.g., "Why AI infra is consolidating around 3 players")
  - customer_evidence: 30% (e.g., "How [customer] reduced infra cost 60% with us")
  - behind_scenes: 20% (e.g., "The bet we got wrong in Q1")
  - real_time: 10% (e.g., "Our take on [competitor's funding round]")

quality_gates:
  - vale lint: 0 errors, <5 warnings
  - claude humanize pass (humanize-ai-text)
  - second-opinion via gemini skill
  - founder approval (read aloud before publish)
  - cover image via canva-mcp or figma-mcp

metrics_30d_targets:
  - linkedin_newsletter_subscribers: +200/month
  - linkedin_engagement_rate: 8-12%
  - substack_open_rate: 40-55%
  - substack_paid_conversion: 1-3% (if monetized)
```

## Edge cases

### LinkedIn newsletter requires UI setup
Newsletter object cannot be created via API. Founder must create it once via LinkedIn UI. Once created, get the `newsletter_id` from URL, then publish programmatically.

### LinkedIn algorithm + cross-post velocity
LinkedIn penalizes "duplicate" content if it appears on multiple surfaces within ~24 hours. Sequence: LinkedIn FIRST, Substack 24-48 hours later, with canonical link back to LinkedIn.

### Substack API is unofficial
Substack doesn't have a fully public REST API. Common methods:
1. Email-to-post relay (formatted email to `<pub>@substack.com`)
2. Substack Sites API (newer, partial coverage)
3. Manual paste (last resort)

For full automation reliability, prefer Beehiiv (API-first design).

### Beehiiv vs Substack decision
- **Substack**: better discoverability via Substack's network effect, easier reader acquisition, weaker analytics + monetization controls
- **Beehiiv**: better API + analytics, more control over monetization, weaker reader network effect

Pick one; don't run both. For execs growing audience: Substack. For execs monetizing: Beehiiv.

### Claude draft is starting point, not finished
Even with strict prompts, Claude drafts read like Claude drafts after 3 paragraphs. Workflow:
1. Claude generates draft
2. Run `humanize-ai-text` skill pass
3. Vale lint
4. Founder reads aloud — anything that sounds wrong gets cut
5. `gemini` skill second-opinion pass
6. Founder final approval

### Voice consistency over time
Maintain a Notion "voice doc" per exec:
- Sentences that sound like them
- Words they actually use vs words they don't
- Recurring themes / arguments
- Phrases they avoid

Feed into Claude prompt as `voice_guide`. Strip stuff that's off-voice.

### Real-time commentary risk
On industry news (acquisitions, regulation, earnings), exec hot takes can go wrong fast. Discipline:
- 24-hour cool-off before publishing on hot topics
- Legal review for anything about competitors or regulators
- Don't take potshots — disagree on substance, not character

### Comment moderation
LinkedIn newsletters generate comments. Exec doesn't need to reply to every one, but reply to top 5-10 (algorithm boost + relationship building). Bot replies are detectable; have exec/EA write the responses.

### Image quality matters
Cover image is the first impression. Use `canva-mcp` for branded templates, `figma-mcp` for brand-system asset export, `imagegen-mcp` for AI gen when needed. NEVER use generic stock photos.

### Repurposing into other channels
Every newsletter generates:
- 5-8 LinkedIn posts (excerpts)
- 1 Twitter thread (key arguments)
- 1 podcast episode angle (if exec has podcast)
- 1 conference talk angle
- 1-2 op-ed pitches (route to `op-ed-contributed-article-placement`)

Map repurposing schedule in Notion at draft time.

### Banned topics
Some topics consistently land execs in trouble:
- Competitor product attacks (use neutral framing instead)
- Hot political topics unrelated to industry (alienates half the audience)
- Personal financial speculation
- Anything that could be seen as Reg-FD violation (public co.)
- Unannounced roadmap details

Build into voice doc + check pre-publish.

### Hand-off to ceo-agent for personal-tone matters
If the newsletter is exec-personal (family, beliefs, controversial position), hand off to `ceo-agent` for voice. PR-comms still handles editorial calendar + lint + publish mechanics.

### Newsletter as a relationship signal for journalists
Journalists subscribe to exec newsletters. They cite from them. Quote-friendly sentences in the newsletter become quotes in their articles. Engineer for extractability:
- Named source + title
- Specific number + date
- Bold claim with caveat ("X grew 40% in Q1" beats "X is growing fast")
- Comparative framing ("vs Y" pulls brand into broader queries)

This is the AEO earned-media optimization point — same surface, two different uses.

## Sources

- **LinkedIn + Substack strategy 2026**: https://www.onlinewritingclub.com/p/the-linkedin-substack-strategy-for
- **LinkedIn thought leadership 2026 playbook**: https://everything-pr.com/linkedin-thought-leadership-a-2026-playbook/
- **LinkedIn Marketing API**: https://learn.microsoft.com/en-us/linkedin/marketing/overview
- **LinkedIn Newsletters / Articles API**: https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/articles-api
- **Substack**: https://substack.com/
- **Beehiiv API**: https://developers.beehiiv.com/
- **Hispanic Executive newsletter strategy**: https://hispanicexecutive.com/executives-personal-newsletters-linkedin-substack/
- **Rosica LinkedIn TL tips 2026**: https://www.rosica.com/2026/02/23/linkedin-thought-leadership-tips-for-2026/
- **Vale linter**: https://vale.sh/
