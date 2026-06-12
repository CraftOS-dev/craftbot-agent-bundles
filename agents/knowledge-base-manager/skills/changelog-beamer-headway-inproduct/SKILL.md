---
name: changelog-beamer-headway-inproduct
description: In-product changelog — Beamer (widget), Headway (alt widget), LaunchNotes (segmented admin/end-user/dev). Free fallback: RSS / Atom feed via feedgen. Each entry ties to a deeper KB article. Use when product ships features without telling users, or when "what's new" lives only in release notes nobody reads.
---

# Changelog management — Beamer / Headway / LaunchNotes / RSS

## When to use

Reach for this skill when the user says: "set up a changelog", "what's new widget", "users don't see what we shipped", "Beamer", "Headway", "LaunchNotes", "release notes integration", or "in-product whats-new". Decision tree: simple widget + email digest = Beamer/Headway; segmented changelog (admin vs end-user vs dev) = LaunchNotes; FOSS / self-host = RSS via `feedgen`. Skip if release notes already land in CHANGELOG.md AND your audience is engineers who read GitHub releases.

## Setup

```bash
# Beamer / Headway / LaunchNotes — no install; embed widget JS in app
# FOSS RSS fallback
pip install feedgen

# For dev-changelog from git history
npm i -g conventional-changelog-cli   # or auto-changelog
```

Auth / env vars:
- `BEAMER_API_KEY` — Beamer Settings → API. Paid.
- `HEADWAY_API_KEY` — Headway Account → API. Paid.
- `LAUNCHNOTES_API_KEY` — LaunchNotes Workspace → API. Paid.
- `BEAMER_ACCOUNT_ID` / `HEADWAY_ACCOUNT_ID` / `LAUNCHNOTES_PROJECT_ID` — for scoping API calls.

## Common recipes

### Recipe 1: Beamer — POST a new changelog entry

```bash
curl -X POST 'https://api.getbeamer.com/v0/posts' \
  -H "Beamer-Api-Key: $BEAMER_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "title": [{ "language": "en", "value": "Webhook retry strategy v2" }],
    "content": [{ "language": "en", "value": "<p>We shipped exponential backoff + jitter...</p>" }],
    "category": "feature",
    "linkUrl": "https://docs.example.com/how-to/webhooks/retry-strategy",
    "linkText": [{ "language": "en", "value": "Read the docs" }],
    "publishedAt": "2026-06-11T09:00:00Z",
    "userSegments": ["all"],
    "notifyEmail": true
  }'
```

Notify-email auto-sends to opted-in users; widget shows the entry immediately to in-product visitors.

### Recipe 2: Embed Beamer widget

```html
<!-- Drop into your app once -->
<script type="text/javascript">
  var beamer_config = {
    product_id: '<your-product-id>',
    selector: '#whats-new-button',
    button_position: 'bottom-right',
    user_id: '<current-user-id>',
    user_email: '<current-user-email>',
  };
</script>
<script type="text/javascript" src="https://app.getbeamer.com/js/beamer-embed.js" defer></script>
<button id="whats-new-button">What's new</button>
```

`user_id` enables per-user read-state. Without it, Beamer treats every session as fresh.

### Recipe 3: Headway — POST changelog entry

```bash
curl -X POST 'https://api.headwayapp.co/v1/changelog' \
  -H "Authorization: Bearer $HEADWAY_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Webhook retry strategy v2",
    "content": "<p>Exponential backoff + jitter is now the default...</p>",
    "category": "improvement",
    "tags": ["webhooks", "api"],
    "url": "https://docs.example.com/how-to/webhooks/retry-strategy"
  }'
```

### Recipe 4: LaunchNotes — segmented post (admin / end-user / dev)

```bash
curl -X POST 'https://api.launchnotes.io/public/graphql' \
  -H "Authorization: Bearer $LAUNCHNOTES_API_KEY" \
  -H 'Content-Type: application/json' \
  -d @- <<'GQL'
{
  "query": "mutation CreatePost($input: CreatePublicPostInput!) { createPublicPost(input: $input) { post { id slug } } }",
  "variables": {
    "input": {
      "projectId": "<project_id>",
      "title": "Webhook retry strategy v2",
      "contentMarkdown": "## What changed\n\n- Exponential backoff + jitter default\n- Configurable retry budget per webhook\n\n[Read the docs](https://docs.example.com/how-to/webhooks/retry-strategy)",
      "categories": ["feature"],
      "subscriberLists": ["admins", "developers"],
      "publishAt": "2026-06-11T09:00:00Z"
    }
  }
}
GQL
```

`subscriberLists` segments notifications. Admins get one notification; end-users don't see dev-only changes.

### Recipe 5: FOSS — generate RSS feed via feedgen

```python
# scripts/build_changelog_rss.py
from feedgen.feed import FeedGenerator
import yaml, pathlib

fg = FeedGenerator()
fg.id('https://docs.example.com/changelog')
fg.title('Acme Changelog')
fg.link(href='https://docs.example.com/changelog', rel='alternate')
fg.description('Latest Acme product updates')
fg.language('en')

# Each entry stored as a markdown file with frontmatter
for entry in sorted(pathlib.Path('changelog').glob('*.md'), reverse=True):
    meta = yaml.safe_load(entry.read_text().split('---')[1])
    fe = fg.add_entry()
    fe.id(f"https://docs.example.com/changelog/{entry.stem}")
    fe.title(meta['title'])
    fe.link(href=f"https://docs.example.com/changelog/{entry.stem}")
    fe.description(meta.get('summary', ''))
    fe.published(meta['date'])
    fe.category({'term': meta.get('category', 'general')})

fg.rss_file('public/changelog/rss.xml')
fg.atom_file('public/changelog/atom.xml')
```

```bash
python scripts/build_changelog_rss.py
# Ship public/changelog/rss.xml in the docs build
```

### Recipe 6: GitHub release → Beamer post (CI automation)

```yaml
# .github/workflows/release-to-beamer.yml
on:
  release:
    types: [published]
jobs:
  post:
    runs-on: ubuntu-latest
    steps:
      - name: Post to Beamer
        env: { KEY: '${{ secrets.BEAMER_API_KEY }}' }
        run: |
          BODY=$(jq -Rs . < <(echo "${{ github.event.release.body }}"))
          curl -X POST 'https://api.getbeamer.com/v0/posts' \
            -H "Beamer-Api-Key: $KEY" \
            -H 'Content-Type: application/json' \
            -d "{
              \"title\":[{\"language\":\"en\",\"value\":\"${{ github.event.release.name }}\"}],
              \"content\":[{\"language\":\"en\",\"value\":$BODY}],
              \"category\":\"feature\",
              \"linkUrl\":\"${{ github.event.release.html_url }}\",
              \"publishedAt\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
            }"
```

### Recipe 7: Email digest of monthly highlights

```bash
# Pull last 30d Beamer posts, format as email-ready HTML
SINCE=$(date -d '30 days ago' --iso-8601)
curl -s "https://api.getbeamer.com/v0/posts?startDate=$SINCE" \
  -H "Beamer-Api-Key: $BEAMER_API_KEY" \
  | jq -r '.[] | "<li><strong>\(.title[0].value)</strong> — \(.content[0].value)</li>"' \
  > monthly-highlights.html

# Send via gmail-mcp or marketing-agent's klaviyo-email-lifecycle skill
```

### Recipe 8: Auto-generate dev changelog from conventional commits

```bash
# In a release script
conventional-changelog -p angular -i CHANGELOG.md -s

# Or with auto-changelog
npx auto-changelog --output CHANGELOG.md --template keepachangelog
```

Then pass the rendered section to LaunchNotes (Recipe 4) tagged `developers`.

### Recipe 9: Tie every changelog entry to a KB article

```python
# Validate that every entry has a docs link before publishing
import re, sys, frontmatter
m = frontmatter.load(sys.argv[1])
if not m.get('docs_url') or not re.match(r'^https://docs\.example\.com/', m['docs_url']):
    print(f"FAIL: {sys.argv[1]} missing docs_url linking to docs.example.com")
    sys.exit(1)
```

Add to pre-commit hook on `changelog/*.md`.

### Recipe 10: Pull Beamer / Headway analytics

```bash
# Beamer engagement per post
curl -s "https://api.getbeamer.com/v0/posts/<post_id>/statistics" \
  -H "Beamer-Api-Key: $BEAMER_API_KEY" \
  | jq '{views, clicks, reactions, ctr: (.clicks / .views)}'

# Headway
curl -s "https://api.headwayapp.co/v1/changelog/<post_id>/analytics" \
  -H "Authorization: Bearer $HEADWAY_API_KEY"
```

CTR <2% on a major feature post = title isn't pulling; rewrite headline.

## Examples

### Example 1: Beamer end-to-end — auto-post per GitHub release

**Goal:** Every GitHub release auto-posts to Beamer with link to docs.

**Steps:**
1. Sign up for Beamer; grab `BEAMER_API_KEY` (Setup).
2. Embed widget in app (Recipe 2).
3. Add `.github/workflows/release-to-beamer.yml` (Recipe 6).
4. Cut a release; confirm post appears in widget within 60s.
5. Add docs-link validation (Recipe 9).

**Result:** Zero-touch changelog; engineers stop manually writing release announcements.

### Example 2: LaunchNotes for segmented changelog (admin + end-user + dev)

**Goal:** Single changelog source, three audiences see different posts.

**Steps:**
1. Set up three subscriber lists in LaunchNotes: `admins`, `end-users`, `developers`.
2. Embed the per-segment widget in admin panel / app dashboard / developer portal respectively.
3. For each release, post with `subscriberLists` matching the relevant audiences (Recipe 4).
4. Customers see only what they care about.

**Result:** Admins don't see CSS tweaks; end-users don't see API deprecations; developers see everything they need.

### Example 3: FOSS RSS feed for changelog (no paid tool)

**Goal:** Engineer-heavy audience just wants an RSS feed.

**Steps:**
1. Author entries as markdown files in `changelog/*.md` with frontmatter (title, date, category, summary, docs_url).
2. Run `python scripts/build_changelog_rss.py` (Recipe 5) in CI.
3. Publish `public/changelog/rss.xml` with the docs build.
4. Link `<link rel="alternate" type="application/rss+xml" href="/changelog/rss.xml">` in `<head>`.

**Result:** Zero-tool, fully-portable changelog. Readers subscribe in any RSS reader.

## Edge cases / gotchas

- **Beamer / Headway / LaunchNotes are paid** — entry plans ~$50-200/mo. RSS via feedgen is the free fallback.
- **Beamer widget impression caps** — Free tier limited to 10k views/month. Costs ramp at scale.
- **LaunchNotes GraphQL** — be careful with mutations; no rollback. Stage in their preview env first.
- **Headway requires user identification** for per-user read-state — pass `user_id`. Without it, every visit shows all entries as unread.
- **`publishedAt` in the future** — Beamer / Headway accept future dates and auto-publish; LaunchNotes uses `publishAt` (different field).
- **Email notifications bypass widget** — if you notify-email, even users who haven't opened the app see it. Use sparingly to avoid email fatigue.
- **Changelog ≠ release notes ≠ marketing announcement** — pick the right audience per entry. Don't dump all three into one feed.
- **RSS validators** — run `feedvalidator.org` against the generated XML; invalid feeds break in some readers silently.
- **Headway category controlled vocabulary** — `feature`, `improvement`, `fix`, `announcement`. Don't invent new ones; widget won't render unknowns.
- **Beamer i18n** — `title` and `content` are arrays of `{language, value}`. Send all locales in one POST.
- **Link to KB, not to PR** — readers want context, not git diffs. Validate (Recipe 9).
- **Don't over-post** — 1-2 major + 3-5 minor per month is the sweet spot. Daily noise burns the widget's signal.
- **Mobile widget vs desktop** — Beamer / Headway have separate widget configs per platform. Test both.
- **GDPR + user data** — sending `user_email` to Beamer / Headway = data processor relationship. Update privacy policy.

## Sources

- [Beamer API docs](https://www.getbeamer.com/help/en/articles/3438037-api)
- [Beamer Posts endpoint](https://www.getbeamer.com/help/en/articles/3438037-api#posts)
- [Beamer widget embed](https://www.getbeamer.com/help/en/articles/3438030-installation)
- [Headway API docs](https://docs.headwayapp.co/)
- [LaunchNotes Public API](https://www.launchnotes.com/api-docs)
- [LaunchNotes segmented changelog patterns](https://www.launchnotes.com/blog/segmented-changelog)
- [feedgen library](https://feedgen.kiesow.be/)
- [conventional-changelog](https://github.com/conventional-changelog/conventional-changelog)
- [auto-changelog](https://github.com/CookPete/auto-changelog)
- [RSS 2.0 spec](https://www.rssboard.org/rss-specification)
- [Atom 1.0 (RFC 4287)](https://datatracker.ietf.org/doc/html/rfc4287)
- [Keep a Changelog](https://keepachangelog.com/)
