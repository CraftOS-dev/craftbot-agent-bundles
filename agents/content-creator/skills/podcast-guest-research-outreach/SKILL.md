# Podcast Guest Research + Outreach — Podchaser / Listen Notes / Notion / Gmail

> Discover candidate guests, assemble a research packet, and run templated outreach with pipeline tracking.

## When to use

Trigger on: "find guests for my podcast", "research this person before booking", "who has X been on", "build a guest preparation packet", "send outreach to a candidate guest", "track guest pipeline". This skill owns guest discovery + research + outreach + pipeline. Hand off scripting to `podcast-scripting-show-notes` and sponsorship-related guest discovery to `podcast-sponsorship-integration`. Use Podchaser as the default discovery layer because it answers role-aware queries Listen Notes can't (who has been a co-host with X, who guested on shows like X).

## Setup

```bash
# Podchaser GraphQL — primary
curl -X POST https://api.podchaser.com/graphql \
  -H "Authorization: Bearer $PODCHASER_API_KEY" \
  -H "Content-Type: application/json"

# Listen Notes REST — secondary
curl -H "X-ListenAPI-Key: $LISTENNOTES_API_KEY" https://listen-api.listennotes.com/api/v2/

# Notion MCP for pipeline
npx -y @notionhq/mcp-server@latest

# Gmail MCP for outreach
npx -y @gongrzhe/server-gmail-autoauth-mcp@latest
```

Auth env vars:
- `PODCHASER_API_KEY` — Podchaser developer portal. Free tier = 1k queries/mo; Pro = 10k.
- `LISTENNOTES_API_KEY` — Listen Notes dashboard. Free = 1.5k req/mo.
- `NOTION_GUEST_PIPELINE_DB` — DB ID of the guest pipeline table.
- `GMAIL_FROM` — sender Gmail address with OAuth granted.

## Common recipes

### Recipe 1: Search Podchaser for candidate guests by topic + role

```graphql
query GuestSearch {
  podcasts(
    searchTerm: "newsletter operators",
    filters: { language: "en", ratingMin: 4 }
  ) {
    data {
      id
      title
      episodeCount
      averageRating
      credits(roleNames: ["guest"]) {
        person {
          id
          name
          bio
          socialUrls
        }
      }
    }
  }
}
```

```bash
curl -X POST https://api.podchaser.com/graphql \
  -H "Authorization: Bearer $PODCHASER_API_KEY" \
  -d '{"query":"<above>"}' \
  | jq '.data.podcasts.data[].credits[].person | {id,name}' \
  | sort -u
```

### Recipe 2: "Who has X been a guest on?"

```graphql
query PersonAppearances($personId: ID!) {
  person(identifier: { id: $personId, type: PODCHASER }) {
    name
    credits(roleNames: ["guest","host"], first: 50) {
      data {
        role
        episode {
          title
          airDate
          podcast { title }
          url
        }
      }
    }
  }
}
```

Use this to discover who a person has spoken to + what they talked about → tailor your pitch with specifics.

### Recipe 3: Listen Notes fallback (when person isn't in Podchaser)

```bash
curl "https://listen-api.listennotes.com/api/v2/search?q=interview+Casey+Newton&type=episode&len_min=20&len_max=90" \
  -H "X-ListenAPI-Key: $LISTENNOTES_API_KEY" \
  | jq '.results[] | {title,podcast:.podcast.title,audio_length_sec,description_original}'
```

Listen Notes is stronger for episode-level full-text search; weaker on structured credits.

### Recipe 4: Guest packet (auto-generate from Podchaser data)

```markdown
# Guest packet: <Name>

## Bio
<Podchaser bio + LinkedIn / personal site summary>

## Audience size + reach
- Twitter / X: <followers>
- LinkedIn: <followers>
- Newsletter / podcast: <subs>
- Total estimated reach: <number>

## Recent podcast appearances (last 10)
| Date | Show | Episode title | Listen / read |
|---|---|---|---|
| <date> | <show> | <title> | <URL> |

## Recurring themes from past interviews
- Theme 1: <named topic, with episodes 2-3 covering it>
- Theme 2: <...>
- Theme 3: <...>

## Fresh angle (what they HAVEN'T been asked yet)
<gap analysis: scan the past appearances above; what topic they've publicly hinted at but never been interviewed about>

## Custom question set (8-12 questions)
- Background: <one personal-history question to warm up>
- Substantive 1: <claim or counter-claim to react to>
- Substantive 2: <...>
- Specific to fresh angle: <2-3 questions on the under-covered topic>
- Reflection: <what would you tell your past self / next-generation question>
- Wrap: <where can people find you + what should they pay attention to>

## Conflict / sensitivity flags
- <past statements that might re-litigate; any topics they declined elsewhere>

## Pitch hook
<one sentence: why YOUR show, why NOW>
```

### Recipe 5: Notion guest pipeline DB schema

```yaml
Guest Pipeline DB:
  properties:
    Name: { type: title }
    Status: { type: select, options: [Researching, Pitched, Reply, Booked, Recorded, Aired, No Reply, Declined] }
    Source: { type: select, options: [Podchaser, Listen Notes, Manual, Referred] }
    Pitch Sent: { type: date }
    Last Touch: { type: date }
    Recording Date: { type: date }
    Air Date: { type: date }
    Audience Reach: { type: number }
    Fit Score: { type: number, range: 1-10 }
    Themes: { type: multi_select }
    Past Appearances: { type: rich_text }
    Pitch Hook: { type: rich_text }
    Episode Number: { type: text }
    Email: { type: email }
    Twitter: { type: url }
    LinkedIn: { type: url }
    Notes: { type: rich_text }
```

Create rows via Notion MCP:

```bash
npx @notionhq/mcp create_page \
  --database_id "$NOTION_GUEST_PIPELINE_DB" \
  --properties '{
    "Name":{"title":[{"text":{"content":"<Guest Name>"}}]},
    "Status":{"select":{"name":"Researching"}},
    "Source":{"select":{"name":"Podchaser"}},
    "Audience Reach":{"number":42000},
    "Fit Score":{"number":8},
    "Email":{"email":"guest@example.com"}
  }'
```

### Recipe 6: Templated Gmail outreach

```bash
# Compose
BODY=$(cat <<'EOF'
Hi <FirstName>,

I'm <YourName>, host of <PodcastName> — a <one-line desc>.
I caught your conversation with <RecentHost> on <RecentShow>
about <SpecificThemeFromTheirEpisode>. Specifically, when you said
"<verbatim quote>" — that reframe is one I keep coming back to.

I'd love to have you on for a 45-min conversation focused on the
angle you haven't been asked yet: <FreshAngle>. My audience is
<AudienceDesc> — <number> monthly listens, <%> in <PersonaSegment>.

A quick 3-line yes/no would be plenty. If yes, I'll send a
recording link with a few date options.

Either way, thanks for your work — <SpecificThingTheyDidThatMattered>
is the kind of thing that makes me want to do this work.

— <YourName>
<URL to most recent episode>
EOF
)

npx @gongrzhe/server-gmail-autoauth-mcp send \
  --to "guest@example.com" \
  --from "$GMAIL_FROM" \
  --subject "Conversation on <FreshAngle> — <PodcastName>" \
  --body "$BODY"

# Update Notion pipeline row
npx @notionhq/mcp update_page --page_id "$NOTION_GUEST_ROW" \
  --properties '{"Status":{"select":{"name":"Pitched"}},"Pitch Sent":{"date":{"start":"2026-06-10"}}}'
```

### Recipe 7: Follow-up cadence (3-touch)

```bash
# Touch 2 (day +7) — fresh hook + lower commitment ask
# Touch 3 (day +21) — break the pattern (audio note, written one-pager, video pitch)
# Touch 4 — none. Don't be that person. Move on.
```

Set Notion reminder filter: `Status = "Pitched" AND Last Touch < 7 days ago`. Run daily to surface follow-ups.

### Recipe 8: Find guests who match audience overlap

```graphql
query AudienceOverlap {
  podcasts(searchTerm: "creator economy", filters: { ratingMin: 4 }) {
    data {
      id
      title
      averageRating
      categories { name }
      credits(roleNames: ["host","guest"]) {
        person { id name }
      }
    }
  }
}
```

Filter results in Notion: any person who has appeared on ≥3 shows you'd want to be on = strong fit.

### Recipe 9: Bulk-research a list

```python
import requests, json
candidates = ["Person A", "Person B", "Person C"]  # 30+ candidates
out = []
for name in candidates:
    q = '{"query":"query($name:String!){people(searchTerm:$name){data{id name bio credits(roleNames:[\\"guest\\"],first:10){data{episode{title airDate podcast{title}}}}}}}","variables":{"name":"%s"}}' % name
    r = requests.post("https://api.podchaser.com/graphql",
        headers={"Authorization": f"Bearer {os.environ['PODCHASER_API_KEY']}"}, data=q).json()
    out.append(r)
json.dump(out, open("research.json","w"))
```

### Recipe 10: Quick "is this guest worth a slot" score

```python
# Score = audience_reach × theme_overlap × novelty
def fit_score(guest):
    reach = min(guest.get('audience_reach', 0) / 10000, 10)  # cap at 10
    overlap = sum(1 for t in guest['themes'] if t in MY_PODCAST_THEMES) / max(len(MY_PODCAST_THEMES), 1) * 10
    novelty = 10 - min(len([a for a in guest['past_appearances'] if 'overlapping_show' in a]), 10)
    return round((reach + overlap + novelty) / 3, 1)
```

Push the score into Notion's `Fit Score` property; book only guests scoring ≥7.

## Examples

### Example 1: Find + book 12 guests for a new podcast season

**Goal:** Identify and book 12 guests for a creator-economy season starting in 6 weeks.

**Steps:**
1. Recipe 1: Podchaser query for top creator-economy podcasts (rating ≥4, English).
2. Pull all guests with ≥3 cross-show appearances; rank by audience reach.
3. Recipe 4: auto-generate 30 packets; rank-cut to top 20 with Recipe 10 fit-score.
4. Recipe 5: Notion DB row for each of top 20; set status=Researching.
5. Recipe 6: send 20 pitches over 4 days (5/day to avoid spam flags).
6. Recipe 7: follow up at day +7 with any non-responders.
7. Goal: 12 confirmed by week 4; backfill from waitlist.

**Result:** 12 booked guests over 6 weeks; season locked.

### Example 2: Pitch a high-profile guest with overlap analysis

**Goal:** Pitch Casey Newton onto your podcast.

**Steps:**
1. Recipe 2: query Casey's last 50 podcast appearances.
2. Identify the 3 topics he covers most + 1 topic he's hinted at but never covered.
3. Recipe 4: assemble packet with that fresh angle as the hook.
4. Find a specific 8-word verbatim quote from a recent appearance to reference in the pitch.
5. Recipe 6: send pitch with the quote + fresh angle + audience-relevance one-liner.
6. Follow up at day +7 with a different angle (his recent newsletter post, his book).

**Result:** Personalized pitch with 3-5× higher reply rate vs templated.

### Example 3: Build a year-1 guest waitlist before launching

**Goal:** Have a 24-person guest waitlist queued before episode 1.

**Steps:**
1. Recipe 1: pull 100 candidates across 5 sub-topics.
2. Recipe 4 + 10: score each, cut to 30.
3. Recipe 6 modified: send a "future show" intro pitch — "we're launching; want to be one of the first 24 guests".
4. Track in Notion DB with Status = "Researching" → "Pitched" → "Reply: yes" → "Reply: maybe later" → "No reply".
5. Book the 12 hottest yeses for season 1; keep the rest warm for season 2.

**Result:** Year-1 production secured without scrambling for guests after each episode.

## Edge cases / gotchas

- **Podchaser free tier = 1k queries/mo.** A 30-candidate research run + 10 person-deep-dives = ~200 queries. Pro plan for serious operators.
- **Listen Notes is full-text, not role-structured.** It can't answer "who's been a co-host with X" — Podchaser can. But Listen Notes nails episode-level keyword search.
- **Cold pitches under 150 words convert 3× better** than long pitches. Specifics > flattery > biography.
- **Reply rate benchmarks**: 15-25% on warm referrals; 5-10% on cold pitches with specifics; <2% on templated/spammy pitches.
- **Gmail outreach rate limit**: 500 emails/day for free Gmail; 2,000/day for Workspace. Cold outreach >50/day from a new sender = soft bounces.
- **Don't email-bomb**. Max 5 candidate pitches/day from a single sender to avoid spam flags. Drip across weeks.
- **Podchaser bio field is community-edited** — sometimes outdated. Cross-check social bios.
- **Don't pitch within 30 days of a guest's recent appearance on a competing show** — they'll have just retold those stories; wait for fresh material.
- **Diverse guest roster matters** — track gender / race / geographic distribution as a property in the Notion DB; aim for 50%+ underrepresented voices across a season.
- **Always include a one-click "no thanks" line**. "If this isn't a fit, a one-line no is the kindest thing you can send" — this raises reply rates by removing the "I should respond properly someday" guilt.
- **FTC compliance flag** — if you're paying guests for appearances, disclose it in episode show notes per `creator-collab-brand-partnership-briefing` skill.

## Sources

- [Podchaser API vs Listen Notes API](https://www.podchaser.com/articles/api/podchaser-api-vs-listen-notes-api)
- [Podchaser developer docs](https://api-docs.podchaser.com/)
- [Listen Notes API](https://www.listennotes.com/api/docs/)
- [Notion editorial calendar template](https://www.notion.com/templates/editorial-calendar)
- [Best podcast hosting 2026](https://www.thepodosphere.com/blog/best-podcast-hosting-platforms-2026-comparison-guide)
- [Cold-email best practices for podcast pitches](https://www.thoughtleaders.io/blog/podcast-trends-2026)
