# Podcast SEO — Titles + Descriptions + `<podcast:chapter>` + Google Key Moments

> Optimize podcast metadata + RSS chapter markers for Google Key Moments rich results + listener navigation.

## When to use

Trigger on: "optimize podcast SEO", "podcast title format", "Google Key Moments", "<podcast:chapter>", "RSS chapter tag", "episode description SEO", "podcast transcript SEO", "show notes for ranking". This skill owns: title structure, description SEO, `<podcast:chapter>` RSS namespace embed, transcript publishing, thumbnail rules, RSS metadata. For deeper editorial show notes see `podcast-scripting-show-notes`. For analytics see `content-analytics-retention-open-rates-chartable`.

## Setup

```bash
# Per-podcast-host APIs to update episode metadata + embed chapters
# Buzzsprout
curl -H "Authorization: Token token=$BUZZSPROUT_API_KEY" \
  "https://www.buzzsprout.com/api/$BUZZSPROUT_PODCAST_ID/episodes.json"

# Captivate
curl -H "Authorization: Bearer $CAPTIVATE_API_KEY" \
  https://api.captivate.fm/shows

# Transistor
curl -H "x-api-key: $TRANSISTOR_API_KEY" \
  https://api.transistor.fm/v1/episodes

# RSS.com
curl -H "Authorization: Bearer $RSS_COM_API_KEY" \
  https://api.rss.com/episodes

# Apple Podcasts Connect — no public API (manual)
# Spotify for Podcasters — no public API (manual)
```

Auth env vars: per podcast host (`BUZZSPROUT_API_KEY` / `CAPTIVATE_API_KEY` / `TRANSISTOR_API_KEY` / `RSS_COM_API_KEY`).

## Common recipes

### Recipe 1: Title format

```markdown
## SOTA podcast title format
`<Episode #>: <Front-Loaded Keyword> | <Guest Name or Hot Take>`

Examples:
- "042: Newsletter Open Rates Lie | Casey Newton"
- "037: AI Slop in 2026 | The Reframe You're Missing"
- "029: How I Built a $1M Newsletter | Substack Cofounder"

Why this format:
- Episode # → sortable across feeds
- Front-loaded keyword → SEO + Apple/Spotify search
- Guest name OR hot take → social hook for share-ability

## Anti-patterns
- "Episode 42: Talking with Casey about emails"  # vague, no keyword
- "Casey Newton on email"  # no episode #, no SEO frontload
- "🎙️ Latest episode out now!! 🔥"  # emoji-soup, no info
```

### Recipe 2: Description structure (150-200 words)

```markdown
## Description template

[Hook sentence — same as cold open or pull-quote from episode]

In this episode, <Guest Name> (<one-line credential>) and <Host Name> dig into <primary topic>.

Key takeaways:
- <takeaway 1 — specific>
- <takeaway 2>
- <takeaway 3>

We talk about:
- <topic 1>
- <topic 2>
- <topic 3>

Resources mentioned:
- <tool / book / article> — <URL>

Show notes (full transcript, chapters, links): <URL>

This episode is sponsored by <Brand>. Use code <SHOWNAME> for 30% off at <URL>.

Subscribe wherever you listen — Apple, Spotify, YouTube, RSS.

#podcast #<niche> #<creator-name>
```

### Recipe 3: Embed `<podcast:chapter>` namespace in RSS

```xml
<!-- Episode metadata in podcast host should include podcast:chapters URL pointing to a JSON chapters file -->

<item>
  <title>042: Newsletter Open Rates Lie | Casey Newton</title>
  <description>...</description>
  <enclosure url="https://cdn.example.com/ep042.mp3" length="48293120" type="audio/mpeg"/>
  <itunes:duration>2784</itunes:duration>
  <itunes:image href="https://cdn.example.com/ep042.jpg"/>
  <itunes:summary>...</itunes:summary>
  <itunes:keywords>newsletter,open rates,Apple MPP,creator economy</itunes:keywords>
  <podcast:chapters url="https://example.com/podcasts/ep042/chapters.json" type="application/json+chapters"/>
</item>
```

### Recipe 4: Chapters JSON spec

```json
{
  "version": "1.2.0",
  "chapters": [
    {"startTime": 0, "title": "Cold open"},
    {"startTime": 150, "title": "Sponsor: Beehiiv", "url": "https://beehiiv.com/showname?utm_source=podcast"},
    {"startTime": 300, "title": "Why open rates lie post-MPP"},
    {"startTime": 720, "title": "Casey's framework for tracking CTR"},
    {"startTime": 1080, "title": "Guest backstory + how he got into newsletters"},
    {"startTime": 1920, "title": "Hot take: opens are vanity"},
    {"startTime": 2580, "title": "Listener Q&A"},
    {"startTime": 2784, "title": "CTA + outro"}
  ]
}
```

Spec: <https://podcastindex.org/namespace/1.0#chapters>

### Recipe 5: Upload chapters via podcast host API

```bash
# Buzzsprout — chapter markers via API
curl -X PATCH "https://www.buzzsprout.com/api/$BUZZSPROUT_PODCAST_ID/episodes/$EP_ID.json" \
  -H "Authorization: Token token=$BUZZSPROUT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "chapter_marks": [
      {"start_time": "00:00:00", "title": "Cold open"},
      {"start_time": "00:02:30", "title": "Sponsor: Beehiiv"},
      {"start_time": "00:05:00", "title": "Why open rates lie post-MPP"},
      {"start_time": "00:18:00", "title": "Casey backstory"},
      {"start_time": "00:32:00", "title": "Hot take"},
      {"start_time": "00:48:00", "title": "Q&A"},
      {"start_time": "00:55:00", "title": "CTA"}
    ]
  }'

# Captivate
curl -X PATCH "https://api.captivate.fm/episodes/$EP_ID" \
  -H "Authorization: Bearer $CAPTIVATE_API_KEY" \
  -d '{"chapters": [...]}'

# Transistor
curl -X PATCH "https://api.transistor.fm/v1/episodes/$EP_ID" \
  -H "x-api-key: $TRANSISTOR_API_KEY" \
  -d '{"chapters": [...]}'
```

### Recipe 6: Title front-load keyword research

```markdown
## Identify front-load keyword

1. Audience question being answered (from podcast-scripting-show-notes brief)
2. Long-tail keyword tied to that question (search via Brave / Listen Notes / Apple Podcasts search)
3. Front-load that keyword in title

Examples:
- Question: "How do I grow my newsletter?"
- Long-tail: "newsletter growth tactics 2026"
- Title: "042: Newsletter Growth Tactics 2026 | Casey Newton"

## Tools
- Brave Search → "people also search for"
- Apple Podcasts search autocomplete
- Spotify for Podcasters keyword data (limited)
- Listen Notes keyword stats
```

### Recipe 7: Publish full transcript on episode page

```markdown
## Why publish full transcripts

- Boosts indexable text content (SEO win)
- Long-tail query rankings (e.g., "Casey Newton on MPP impact 2026")
- Accessibility win
- Sharable snippets for social

## Format

# Episode 042: Newsletter Open Rates Lie | Casey Newton

[Audio embed]

## Full transcript

**Host (00:00):** Welcome back to <Show Name>. I'm <name>...

**Casey (00:30):** Thanks for having me.

**Host (00:45):** Let's get into it. <Question 1>?

**Casey (01:02):** ...

[continue in speaker-labeled, timestamped format]

## Chapter timestamps
- 00:00 — Cold open
- 02:30 — Sponsor read
- ...
```

### Recipe 8: itunes RSS tags (required for podcast directories)

```xml
<channel>
  <itunes:author>Show Name</itunes:author>
  <itunes:category text="Technology"/>
  <itunes:category text="Business"/>
  <itunes:image href="https://cdn.example.com/show_artwork_3000x3000.jpg"/>
  <itunes:explicit>false</itunes:explicit>
  <itunes:keywords>newsletter,creator economy,marketing,podcast</itunes:keywords>
  <itunes:summary>One-paragraph show description for podcast directories</itunes:summary>

  <item>
    <itunes:title>042: Newsletter Open Rates Lie | Casey Newton</itunes:title>
    <itunes:author>Show Name</itunes:author>
    <itunes:subtitle>One-line tagline distinct from title</itunes:subtitle>
    <itunes:summary>2-3 sentence episode summary</itunes:summary>
    <itunes:duration>2784</itunes:duration>
    <itunes:keywords>newsletter,MPP,Casey Newton,CTR</itunes:keywords>
    <itunes:image href="https://cdn.example.com/ep042_artwork.jpg"/>
    <itunes:explicit>false</itunes:explicit>
    <itunes:episode>42</itunes:episode>
    <itunes:season>4</itunes:season>
    <itunes:episodeType>full</itunes:episodeType>
  </item>
</channel>
```

### Recipe 9: Thumbnail (artwork) rules

```markdown
## Episode artwork

- 3000×3000 minimum (Apple Podcasts spec; smaller = rejected)
- High contrast at small sizes (Apple's directory shows 192×192 in feeds)
- Person fills 60%+ vertical OR text-image-split horizontal
- 3-8 character text overlay max
- No "EPISODE 42" small text (illegible at thumbnail)
- Brand mark small (not dominant)

## Test
- Shrink to 192×192. Can you read the title? If not, rework.
```

### Recipe 10: YouTube version SEO (parallel optimization)

```markdown
## YouTube SEO for podcast video version

- Title: same as podcast feed title
- Description: same 150-200 word as feed + YouTube-specific CTA + timestamps
- Tags: 5-10 tags ("newsletter,creator economy,Casey Newton...")
- Custom thumbnail (use Recipe 9 rules)
- Chapters: YouTube auto-detects time-coded chapters in description
- Cards + end screens: subscribe + link to most-recent episode

## Description timestamps format (YouTube auto-detects)
00:00 Cold open
02:30 Sponsor read
05:00 Why open rates lie post-MPP
18:00 Casey backstory
32:00 Hot take
48:00 Q&A
55:00 CTA + outro
```

### Recipe 11: Update old episodes (back-catalog SEO refresh)

```bash
# Find episodes with thin descriptions / no chapters
EPS=$(curl -H "Authorization: Token token=$BUZZSPROUT_API_KEY" \
  "https://www.buzzsprout.com/api/$BUZZSPROUT_PODCAST_ID/episodes.json?limit=200" \
  | jq '.[] | select(.description | length < 200) | .id')

# Re-author description + add chapters via Recipe 5 batch update
```

### Recipe 12: Google Key Moments verification

```markdown
## After publishing with chapters

1. Wait 1-2 weeks for Google to index
2. Search "<your podcast name> <episode keyword>" in Google
3. Check for rich result with chapter timestamps + thumbnails
4. If not appearing: verify <podcast:chapter> RSS feed accessible at the URL specified
5. Submit feed via Google Podcasts Manager: https://podcastsmanager.google.com/
```

## Examples

### Example 1: New episode end-to-end SEO

**Goal:** Publish Episode 42 with full SEO optimization.

**Steps:**
1. Recipe 6: identify front-load keyword from audience question.
2. Recipe 1: write title per template.
3. Recipe 2: write description.
4. Recipe 4: author chapters JSON.
5. Host chapters.json at episode URL.
6. Recipe 5: upload via podcast host API; embed `<podcast:chapter>` URL in RSS.
7. Recipe 7: publish full transcript on episode page.
8. Recipe 8: verify all itunes RSS tags present.
9. Recipe 9: create thumbnail meeting Apple spec.
10. Recipe 10: parallel YouTube version SEO.
11. Recipe 12: verify Google Key Moments in 2 weeks.

**Result:** Episode discoverable via Apple search + Spotify search + Google Key Moments rich result.

### Example 2: Back-catalog SEO refresh

**Goal:** Update 50 old episodes that lack chapters + thin descriptions.

**Steps:**
1. Recipe 11: query episodes with sub-200-char descriptions.
2. For each: author description per Recipe 2 + chapters per Recipe 4.
3. Batch update via Recipe 5.
4. Wait 2 weeks; check organic traffic spike to episode pages.

**Result:** 50 episodes re-indexed for organic discovery; long-tail keyword rankings restored.

### Example 3: YouTube parallel optimization

**Goal:** YouTube version drives equal traffic as podcast feed via search.

**Steps:**
1. Recipe 10: parallel YouTube SEO matching podcast feed.
2. Custom thumbnail with high contrast + 3-character text overlay.
3. Chapters embedded in description.
4. Tags optimized via YouTube tag suggester.
5. Track YouTube Search vs Apple Podcasts Search vs Spotify Search referrals over 90 days.

**Result:** Multi-channel discoverability vs single-platform reliance.

## Edge cases / gotchas

- **`<podcast:chapter>` requires RSS namespace declaration** in channel header: `xmlns:podcast="https://podcastindex.org/namespace/1.0"`.
- **Apple Podcasts adopts chapters slowly** — Apple Podcasts Connect dashboard chapters are SEPARATE from `<podcast:chapter>` in RSS. Best practice: both.
- **Spotify ignores `<podcast:chapter>`** as of June 2026 — uses its own chapter system via Spotify for Podcasters.
- **Google Key Moments requires** chapters JSON + transcript on episode page + Schema.org PodcastEpisode markup.
- **Apple Podcasts thumbnail spec is strict:** 3000×3000, JPG/PNG, max 500KB. Smaller = directory rejection.
- **Don't keyword-stuff titles** — over-optimization tanks Apple ranking. Keep title human-readable.
- **Front-load keyword applies to long-tail too** — "newsletter open rates" not "open rates of newsletters".
- **Episode # in title aids sortability + listener UX.** Use 3-digit format ("042" not "42") for sort consistency.
- **Description over 200 words = diminishing SEO returns + Apple truncates.** Keep under 200.
- **Full transcript on episode page** boosts SEO 30-50% vs no transcript. Lazy but important.
- **`itunes:keywords` is deprecated** — Apple ignores; use `itunes:summary` and natural keyword density in description.
- **Podcast host APIs vary in chapter support** — Buzzsprout / Captivate / Transistor / RSS.com differ. Check per-host.
- **Spotify for Podcasters Connect dashboard chapters** are NOT auto-synced from RSS — re-enter manually.
- **YouTube auto-detects chapters from description timestamps** in format `00:00 Title` — must be at start of line.
- **Episode artwork must differ from show artwork** for max SEO benefit; per-episode visual signals to discovery algos.
- **Google Podcasts service was sunset in 2024** — Key Moments now appear in general Google Search results.
- **Schema.org PodcastEpisode markup** on episode page boosts rich-result eligibility.

## Sources

- [Podcast SEO 2026 (Spear Point)](https://www.thespearpoint.com/blog/seo-for-podcasts)
- [Shownotes — Podcast SEO tools 2026](https://shownotes.ai/podcast-seo-tools)
- [`<podcast:chapter>` namespace spec](https://podcastindex.org/namespace/1.0#chapters)
- [Google Key Moments documentation](https://developers.google.com/search/docs/appearance/structured-data/podcast)
- [Apple Podcasts requirements](https://podcasters.apple.com/support/)
- [Buzzsprout chapter markers](https://www.buzzsprout.com/help/197-how-do-i-add-chapter-markers-to-my-podcast)
- [Captivate chapter support](https://captivate.fm/help/api)
- [Transistor episode metadata](https://developers.transistor.fm/)
- [Schema.org PodcastEpisode](https://schema.org/PodcastEpisode)
