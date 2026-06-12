<!--
Sources: https://www.showca.se/post/ugc-usage-rights + https://www.commonroom.io/ + https://www.bazaarvoice.com/ + https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
-->
# UGC Cultivation + Spotlights — SKILL

Member-spotlight cadence (1–2 per week), case-study mining, rights-request DM template (paid licensing per campaign window vs perpetual), repost workflow with attribution. Notion rights DB as source of truth. FTC-disclosure-aware. Output: weekly spotlight + monthly case study + quarterly highlight reel.

## When to use

- Community has organic posts/clips/screenshots worth amplifying.
- Brand marketing needs authentic content; UGC > studio every time.
- Quarterly campaign launch — want member voices in launch assets.
- Case-study pipeline empty — community success stories are gold.
- AMA recordings + member tweets pile up uncited.
- Social-media-manager asks for member content to repost; need rights workflow.

Trigger phrases: "member spotlight", "UGC", "user-generated content", "case study", "highlight reel", "rights request", "FTC disclosure", "repost".

## Setup

```bash
# Notion rights DB
mcp tool notion.create_database --parent_id $COMM_PAGE \
  --title "UGC Rights" \
  --properties '{"Author":{"title":{}},"Content URL":{"url":{}},"Type":{"select":{}},"Rights status":{"select":{}},"Window":{"date":{}},"Compensation":{"rich_text":{}},"FTC tag":{"checkbox":{}}}'

# Common Room for UGC surface
curl -H "Authorization: Bearer $COMMON_ROOM_TOKEN" \
  "https://app.commonroom.io/api/v1/activities?type=post&sentiment=positive&limit=100"

# Brand24 for off-community UGC
curl -H "X-Auth-Token: $BRAND24_TOKEN" \
  "https://api.brand24.com/v3/mentions?keyword=$BRAND&since=$LAST_RUN"

# Vale for FTC-disclosure check
vale --config vale-ftc.ini drafts/
```

Auth + env:
- `COMMON_ROOM_TOKEN` — Common Room API.
- `BRAND24_TOKEN` — Brand24 paid.
- Notion DB `UGC Rights` schema above.
- `FTC_DISCLOSURE_TEMPLATES` — `#ad`, `#sponsored`, `Promoted by Brand`.

Workspace prerequisites:
- Notion DB `UGC Rights`.
- Discord/Slack channel `#community-wins` for spotlight feed.
- Brand voice doc for spotlight captions.

## Common recipes

### Recipe 1: Surface UGC candidates (Common Room)

```bash
curl -H "Authorization: Bearer $COMMON_ROOM_TOKEN" \
  "https://app.commonroom.io/api/v1/activities?type=post&sentiment=positive&engagement_min=10&limit=50" \
  | jq '.results[] | {member, url, content, platform, engagement_score}'
```

Filter:
- Positive sentiment + ≥10 engagements.
- Includes screenshot / video / specific result mention.
- Not already in UGC rights DB.

### Recipe 2: Brand24 off-community surface

```bash
# Public mentions tweeting + Reddit threads + blogs
curl -H "X-Auth-Token: $BRAND24_TOKEN" \
  "https://api.brand24.com/v3/mentions?keyword=$BRAND&sentiment=positive&type=tweet,reddit,blog&since=$LAST_RUN" \
  | jq '.mentions[] | {url, snippet, author, platform, reach}'
```

### Recipe 3: Rights-request DM template

```markdown
Hey [Name] — we loved your post about [specific thing] in [channel]!

We'd like to share it on our [blog / social / newsletter / case study page] with credit to you.

Two options:
1. **One-time share** — we credit you + link back. No compensation, no exclusivity.
2. **Featured spotlight** — we'd use it across channels for 90 days + send a $X gift card / merch box / shoutout.

Cool to use it? Just reply YES to (1) or (2). We'll add the post to our member-of-month consideration too 🎉
```

### Recipe 4: Log to Notion rights DB

```bash
mcp tool notion.create_page --parent_id $UGC_DB \
  --properties '{
    "Author": "Jane Doe",
    "Content URL": "https://discord.com/channels/.../...",
    "Type": "Screenshot",
    "Rights status": "Pending",
    "Window": null,
    "Compensation": "$25 gift card",
    "FTC tag": false
  }'
```

On YES, update `Rights status: Granted` + set `Window` (90 days from today).

### Recipe 5: Member spotlight post (Discord)

```bash
mcp tool discord-mcp-full.create_message \
  --channel_id $WINS_CH \
  --content "🌟 Member spotlight: @jane

> $QUOTE_FROM_HER_POST

Jane shipped [thing] using [our product] and walked the community through it last week.

Read her full post: $URL"
```

### Recipe 6: Slack spotlight

```bash
mcp tool slack.chat_postMessage \
  --channel '#community-wins' \
  --blocks '[
    {"type":"section","text":{"type":"mrkdwn","text":"*Member spotlight: <@U123>* 🌟"}},
    {"type":"section","text":{"type":"mrkdwn","text":"> $QUOTE\n\nFull story: <$URL>"}},
    {"type":"context","elements":[{"type":"mrkdwn","text":"Shared with permission · UGC-2026-Q2-014"}]}
  ]'
```

### Recipe 7: Case-study mining (long-form)

```python
# Quarterly: find members hitting strong outcomes
CRITERIA = "post mentions specific KPI improvement (e.g., '40% faster', '$10k saved', 'shipped in 2 weeks')"

candidates = common_room.search(
  query=CRITERIA,
  date_range="last_90_days",
  min_engagement=20
)

# DM top 5 with case-study offer:
case_study_dm = f"""
Hey {name} — your post about {specific_outcome} caught our eye.
Would you be open to a 30-min interview for a case study?
We'll feature you on our blog + amplify across socials.
You get the polished version to share on LinkedIn.
"""
```

### Recipe 8: FTC disclosure compliance

```python
# FTC rule: paid spotlights MUST disclose
def add_ftc_disclosure(post_text, compensation):
    if compensation and compensation != "$0":
        return f"#ad {post_text}\n\n(Promoted feature — $X compensation)"
    return f"{post_text}\n\n(Shared with permission, uncompensated.)"

# Vale custom rule
# styles/Brand/FTC.yml
extends: existence
message: "Missing FTC disclosure — add #ad or #sponsored when compensation involved"
level: error
scope: text
tokens:
  - "(?i)review.*recommended"
  - "(?i)you should try"
```

### Recipe 9: Quarterly highlight reel

```python
# Pull 12 best spotlights from past quarter
posts = notion.query(
  UGC_DB,
  filter={"Rights status": "Granted", "Created": "last_90_days"},
  sort=[{"property": "Engagement", "direction": "descending"}],
  page_size=12
)

# Compile into PDF (via pdf skill) or video reel (manual)
highlight_md = "\n\n".join([f"## {p.author}\n{p.content}\n— {p.url}" for p in posts])
write_file("quarterly_highlights.md", highlight_md)
```

### Recipe 10: Repost with attribution + UTM

```bash
# X / Twitter
curl -X POST -H "Authorization: Bearer $TWITTER_BEARER" \
  https://api.x.com/2/tweets \
  -d "{\"text\":\"$QUOTE — @jane (used with permission)\nhttps://brand.com/feature?utm_source=ugc&utm_campaign=q2-spotlight\"}"

# LinkedIn — via ayrshare-mcp or native API
```

Always:
- @-mention the original author.
- Link back to source.
- Add UTM for attribution.
- Add `#ad` if compensated.

## Examples

### Example 1: Weekly Discord spotlight

**Goal:** 1 Discord member-spotlight every Friday in `#community-wins`.

**Steps:**
1. Mon: Common Room query (Recipe 1) for week's top 5.
2. Tue: Rights-request DMs (Recipe 3).
3. Wed: Log YES'd entries in Notion (Recipe 4).
4. Thu: Draft spotlight + FTC check (Recipes 5, 8).
5. Fri: Post in `#community-wins`.

**Result:** 50 spotlights/year; 12 turn into case studies; member NPS +10.

### Example 2: Q2 launch — need 8 UGC clips

**Goal:** Product launch wants 8 authentic member video clips.

**Steps:**
1. Brand24 + Common Room scan (Recipes 1, 2) → 35 candidates with video.
2. Tier-1 DM offer: $50 gift card for 90-day usage rights.
3. 18 accept; log to Notion (Recipe 4).
4. Marketing-agent cuts 8 best into launch reel.
5. Each spotlight tagged `#ad` + author handle (Recipe 8).

**Result:** Launch landing CVR +18% vs studio-only version.

## Edge cases / gotchas

- **Implicit consent ≠ rights** — posting in your Discord ≠ permission to repost. Always ask.
- **Screenshot rights** — even of your own product UI, the member's framing/words are theirs.
- **Window vs perpetual** — perpetual rights are aggressive; default to 90-day window with renewal option.
- **FTC disclosure** — any compensation, even merch, requires `#ad` or `#sponsored`. Lawsuits exist.
- **EU/UK GDPR** — name + photo = personal data; explicit consent + right-to-revoke required.
- **Minors** — never spotlight under-18 without parent/guardian consent (even if 16y/o is a power-user).
- **Quoted-out-of-context risk** — share full post or paraphrase carefully; check author okay with edit.
- **Self-promo gaming** — power-users may post specifically to be spotlighted. Reward variety, not loudest voice.
- **Rights revocation** — Notion `Rights status: Revoked` → delete + take-down across channels in 48h.
- **Common Room paywall** — Brand24 + manual surfacing is fallback.
- **AI-generated UGC** — disclosure required even from member side; ask "is this AI-generated?" before featuring.
- **Repost cap** — same author no more than 1x/quarter to avoid fatigue.
- **Geographic equity** — rotate spotlights across regions/languages, not just English-power-users.

## Sources

- [Showcase — UGC usage rights](https://www.showca.se/post/ugc-usage-rights)
- [FTC influencer guidance](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers)
- [Common Room](https://www.commonroom.io/)
- [Brand24](https://brand24.com/)
- [Bazaarvoice UGC](https://www.bazaarvoice.com/)
- [Yotpo](https://www.yotpo.com/)
