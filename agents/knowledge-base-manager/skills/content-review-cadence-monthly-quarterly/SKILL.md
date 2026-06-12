---
name: content-review-cadence-monthly-quarterly
description: KB review cadence — monthly stale-bot pings (≥90d untouched → owner), quarterly multi-axis audit (broken links + prose + analytics + redundancy), annual taxonomy refresh from no-result-found queries. Automate via GitHub Actions cron + Slack/Notion notifications. Use when articles drift stale by default.
---

# Content review cadence — monthly stale-check, quarterly audit, annual refresh

## When to use

Reach for this skill when the user says: "our docs go stale", "set up review cadence", "stale-bot", "schedule the quarterly audit", "automate doc reviews", "ping owners when their articles age out", or "we need a calendar for content review". This skill defines the WHEN — cadence + triggers + notifications. The audit work itself lives in `content-audit-stale-inaccurate-redundant`; the lifecycle states (Draft/Stale/Archived) live in `content-lifecycle-draft-review-publish-archive`. Use this skill to schedule the audit + own the notification machinery.

## Setup

```bash
# GitHub Actions cron — no install; declared in .github/workflows/
# Use peter-evans/create-issue-from-file for digest issues
# Use actions/stale for native PR/issue stale labelling (not directly for docs files)

# Slack webhook (free)
# Notion API token (free)
# Optional: actionlint for workflow linting
brew install actionlint
actionlint --version
```

Auth / env vars:
- `SLACK_WEBHOOK_DOCS` — incoming webhook URL → posts to #docs-review channel.
- `NOTION_API_TOKEN` — for writing review digest into a Notion DB.
- `NOTION_REVIEW_DB_ID` — the target DB.
- `GH_TOKEN` — auto-provided in Actions; needed if posting to a different repo.

## Common recipes

### Recipe 1: Monthly stale-bot — find articles >180d untouched, ping owner

```yaml
# .github/workflows/monthly-stale-check.yml
name: Monthly stale content check
on:
  schedule:
    - cron: '0 9 1 * *'   # 1st of each month, 09:00 UTC
  workflow_dispatch:

jobs:
  stale:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }

      - name: Identify stale markdown
        run: |
          THRESHOLD_DAYS=180
          NOW=$(date -u +%s)
          : > stale.txt
          while IFS= read -r -d '' f; do
            ts=$(git log -1 --format=%ct -- "$f")
            age=$(( (NOW - ts) / 86400 ))
            if [ "$age" -gt "$THRESHOLD_DAYS" ]; then
              owner=$(awk -v p="$f" '$1==p {print $2}' .github/OWNERS.txt)
              echo "$f|$age|${owner:-@docs-team}" >> stale.txt
            fi
          done < <(find docs -name '*.md' -print0)

      - name: Post Slack digest
        env: { WEBHOOK: '${{ secrets.SLACK_WEBHOOK_DOCS }}' }
        run: |
          if [ -s stale.txt ]; then
            body=$(awk -F'|' '{printf "• %s (%dd) — %s\\n", $1, $2, $3}' stale.txt)
            curl -X POST -H 'Content-Type: application/json' \
              -d "{\"text\":\":hourglass_flowing_sand: Monthly stale check:\\n$body\"}" \
              "$WEBHOOK"
          fi

      - name: Open digest issue
        if: hashFiles('stale.txt') != ''
        uses: peter-evans/create-issue-from-file@v5
        with:
          title: 'Stale content — ${{ steps.date.outputs.date }}'
          content-filepath: stale.txt
          labels: docs-review,stale
```

### Recipe 2: Quarterly full audit aggregator

```yaml
# .github/workflows/quarterly-audit.yml
name: Quarterly KB audit
on:
  schedule:
    - cron: '0 9 1 1,4,7,10 *'   # 1st of Jan/Apr/Jul/Oct
  workflow_dispatch:

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install audit tools
        run: |
          curl -sSL https://github.com/lycheeverse/lychee/releases/latest/download/lychee-x86_64-unknown-linux-gnu.tar.gz | tar xz -C /usr/local/bin
          pip install simhash datasketch pytest-markdown-docs vale-cli

      - name: Broken links
        run: lychee --format json --output reports/links.json docs/

      - name: Code-fence validation
        run: pytest --markdown-docs docs/ --junitxml reports/code-fences.xml || true

      - name: Prose / style
        run: vale --output=JSON docs/ > reports/vale.json || true

      - name: Redundancy (simhash)
        run: |
          python -c "
          import pathlib, simhash, json
          articles = {str(p): simhash.Simhash(p.read_text().split()) for p in pathlib.Path('docs').rglob('*.md')}
          pairs = []
          keys = list(articles)
          for i,a in enumerate(keys):
              for b in keys[i+1:]:
                  if articles[a].distance(articles[b]) < 12:
                      pairs.append({'a':a,'b':b,'distance':articles[a].distance(articles[b])})
          json.dump(pairs, open('reports/redundant.json','w'))
          "

      - name: Aggregate
        run: |
          python scripts/aggregate_audit.py reports/ > reports/audit-summary.md

      - name: Open PR with audit-summary.md
        uses: peter-evans/create-pull-request@v6
        with:
          title: 'KB audit Q${{ steps.q.outputs.quarter }} ${{ steps.q.outputs.year }}'
          branch: 'kb-audit/q${{ steps.q.outputs.quarter }}-${{ steps.q.outputs.year }}'
          add-paths: reports/audit-summary.md
```

### Recipe 3: Annual taxonomy refresh trigger from no-result-found queries

```yaml
# .github/workflows/annual-taxonomy-refresh.yml
name: Annual KB taxonomy refresh
on:
  schedule:
    - cron: '0 9 15 1 *'   # Jan 15 — gives Q1 strategy room
  workflow_dispatch:

jobs:
  refresh:
    runs-on: ubuntu-latest
    steps:
      - name: Pull top no-result-found from Algolia Insights
        env: { APP_ID: '${{ secrets.ALGOLIA_APP_ID }}', KEY: '${{ secrets.ALGOLIA_ANALYTICS_KEY }}' }
        run: |
          curl -s "https://analytics.algolia.com/2/searches/noResults?index=docs&startDate=$(date -d '365 days ago' +%F)&endDate=$(date +%F)&limit=100" \
            -H "X-Algolia-Application-Id: $APP_ID" \
            -H "X-Algolia-API-Key: $KEY" \
            > no-result-annual.json

      - name: Cluster into proposed taxonomy buckets
        run: |
          python scripts/cluster_queries.py no-result-annual.json > taxonomy-proposal.md

      - name: Open issue for taxonomy review
        uses: peter-evans/create-issue-from-file@v5
        with:
          title: 'Annual taxonomy refresh — proposed buckets from 365d no-result queries'
          content-filepath: taxonomy-proposal.md
          assignees: ${{ github.repository_owner }}
          labels: taxonomy,annual-refresh
```

### Recipe 4: Owner notification via OWNERS.txt + Slack DM

```bash
# .github/OWNERS.txt format
docs/how-to/authentication/    @alice
docs/how-to/webhooks/          @bob
docs/concept/                   @carol
docs/reference/                @docs-team
```

```bash
# In any workflow step
file="docs/how-to/authentication/sso-okta.md"
owner=$(awk -v p="$file" 'index(p, $1)==1 {print $2}' .github/OWNERS.txt | head -1)
curl -X POST "$SLACK_WEBHOOK_DOCS" -H 'Content-Type: application/json' \
  -d "{\"text\":\":robot_face: $owner please review: $file\"}"
```

### Recipe 5: Notion review queue (digest as DB rows, not Slack-only)

```bash
# Write each stale article into Notion review queue
while IFS='|' read -r file age owner; do
  curl -X POST 'https://api.notion.com/v1/pages' \
    -H "Authorization: Bearer $NOTION_API_TOKEN" \
    -H 'Notion-Version: 2022-06-28' \
    -H 'Content-Type: application/json' \
    -d "$(jq -n --arg f "$file" --arg a "$age" --arg o "$owner" '{
      parent: {database_id: env.NOTION_REVIEW_DB_ID},
      properties: {
        File: {title: [{text: {content: $f}}]},
        Age: {number: ($a|tonumber)},
        Owner: {rich_text: [{text: {content: $o}}]},
        Status: {select: {name: "Open"}},
        OpenedAt: {date: {start: now|todate}}
      }
    }')"
done < stale.txt
```

### Recipe 6: Escalation — owner unresponsive after 14d → docs-team triage

```yaml
# .github/workflows/escalate-stale.yml
on:
  schedule: [{ cron: '0 9 * * 1' }]   # Monday 09:00 UTC
jobs:
  escalate:
    runs-on: ubuntu-latest
    steps:
      - name: Pull Notion review queue (Status=Open AND OpenedAt < 14d ago)
        run: |
          curl -s "https://api.notion.com/v1/databases/$NOTION_REVIEW_DB_ID/query" \
            -H "Authorization: Bearer $NOTION_API_TOKEN" \
            -H 'Notion-Version: 2022-06-28' \
            -d '{"filter":{"and":[
              {"property":"Status","select":{"equals":"Open"}},
              {"property":"OpenedAt","date":{"before":"'$(date -d '14 days ago' --iso-8601)'"}}
            ]}}' \
            | jq -r '.results[]|.properties.File.title[0].plain_text' > escalate.txt

      - name: Ping docs-team for triage
        run: |
          if [ -s escalate.txt ]; then
            payload=$(awk '{printf "• %s\\n", $0}' escalate.txt)
            curl -X POST "$SLACK_WEBHOOK_DOCS" -H 'Content-Type: application/json' \
              -d "{\"text\":\":warning: 14d unresolved — triage these:\\n$payload\"}"
          fi
```

### Recipe 7: Per-release audit (every product release → KB diff)

```yaml
# .github/workflows/per-release-kb-diff.yml
on:
  release:
    types: [published]
jobs:
  kb-diff:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Diff docs touched in this release window
        run: |
          PREV=$(gh release list --limit 2 --json tagName -q '.[1].tagName')
          git diff --stat "$PREV"..HEAD -- 'docs/**/*.md' > release-kb-diff.txt
      - name: Comment on the release
        run: gh release edit ${{ github.event.release.tag_name }} \
          --notes-file release-kb-diff.txt
```

### Recipe 8: Verify-stamp refresh + cron cheatsheet + lint

```bash
# Update last_verified for all touched docs
TODAY=$(date +%F)
for f in $(git diff --name-only HEAD~1 HEAD -- 'docs/**/*.md'); do
  grep -q '^last_verified:' "$f" \
    && sed -i "s/^last_verified:.*/last_verified: $TODAY/" "$f" \
    || sed -i "1a last_verified: $TODAY" "$f"
done

# Cron cheatsheet (UTC):
# '0 9 * * 1'         Monday 09:00 (weekly)
# '0 9 1 * *'         1st of month (monthly stale)
# '0 9 1 1,4,7,10 *'  Quarterly (Jan/Apr/Jul/Oct)
# '0 9 15 1 *'        Annual (Jan 15)

# Lint workflows before merging
actionlint .github/workflows/*.yml
```

## Examples

### Example 1: Stand up the full review cadence in a day

**Goal:** New KB; ship monthly stale-bot + quarterly audit + annual taxonomy refresh.

**Steps:**
1. Add `.github/OWNERS.txt` mapping every top-level docs folder to a Slack handle (Recipe 4).
2. Drop `monthly-stale-check.yml` (Recipe 1) + `quarterly-audit.yml` (Recipe 2) + `annual-taxonomy-refresh.yml` (Recipe 3).
3. Set `SLACK_WEBHOOK_DOCS`, `NOTION_API_TOKEN`, `ALGOLIA_APP_ID`, `ALGOLIA_ANALYTICS_KEY` secrets.
4. Validate with `actionlint`.
5. Run `gh workflow run monthly-stale-check.yml` to smoke-test once.
6. Confirm Slack digest + Notion rows.

**Result:** Three crons live; review queue self-populates monthly/quarterly/annually.

### Example 2: Add escalation when owners ghost stale pings

**Goal:** 14d-unresolved articles escalate to docs-team.

**Steps:**
1. Add `escalate-stale.yml` (Recipe 6).
2. Smoke-test by editing a Notion row to `OpenedAt = 21d ago`.
3. Confirm Slack alert lands in #docs-review.

**Result:** No silent rot — every stale article gets to triage within 14d.

### Example 3: Per-release KB diff in release notes

**Goal:** Engineers see which KB articles changed in each release.

**Steps:**
1. Add `per-release-kb-diff.yml` (Recipe 7).
2. Cut a release: `gh release create v2.0.3`.
3. Confirm release notes auto-append docs diff.

**Result:** Engineers see KB drift per release; mandatory verify-stamp refresh becomes natural.

## Edge cases / gotchas

- **GitHub Actions cron drift** — workflows triggered by `schedule` can run 15-30 min late under high org load. Use UTC + buffer.
- **`actions/stale`** is for PRs and issues, not file paths. Don't try to point it at `docs/`; build the file-scan loop (Recipe 1) yourself.
- **`fetch-depth: 0`** is required so `git log -1 --format=%ct -- file` returns the true last-modified timestamp (default shallow clone breaks this).
- **Slack message rate-limit** — webhooks cap at 1 msg/sec. Batch into one digest per run (Recipe 1).
- **Notion DB rate limit** — 3 req/s; if writing 100+ rows, sleep 0.4s between calls or use Notion's bulk import.
- **`OWNERS.txt` path matching** — prefix match (Recipe 4). Long-prefix specificity wins. Make sure the file is sorted longest-prefix-first for unambiguous resolution.
- **Workflow secrets scoping** — `secrets.SLACK_WEBHOOK_DOCS` works only in the repo where it's set; for org-wide cron, define at org level.
- **Cron drift after DST** — UTC sidesteps it, but if you want "Monday 9am ET" you'll see two times in spring/fall. Stick with UTC and accept the shift.
- **Audit PR (Recipe 2) burns minutes** — 100 docs × link-check + simhash can take 10-15min. Use `actions/cache` for the lychee binary + simhash output.
- **No-result-found Algolia quota** — Insights API requires Analytics tier. Free OSS DocSearch has no Insights.
- **Don't auto-archive without owner confirmation** — stale-bot pings only; never auto-mv to `_archived/`.
- **Verify-stamp staleness too** — the monthly cron should flag `last_verified > 90d`, not just the git timestamp.

## Sources

- [GitHub Actions cron syntax](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)
- [actions/stale repo](https://github.com/actions/stale)
- [peter-evans/create-issue-from-file](https://github.com/peter-evans/create-issue-from-file)
- [peter-evans/create-pull-request](https://github.com/peter-evans/create-pull-request)
- [Slack incoming webhooks rate limits](https://api.slack.com/messaging/webhooks#rate_limiting)
- [Notion API rate limits](https://developers.notion.com/reference/request-limits)
- [Algolia Insights / Analytics API](https://www.algolia.com/doc/rest-api/analytics/)
- [actionlint](https://github.com/rhysd/actionlint)
- [Diataxis on doc maintenance](https://diataxis.fr/needs/)
