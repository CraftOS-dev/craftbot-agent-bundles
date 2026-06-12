---
name: content-migration-between-platforms
description: KB content migration — Notion → markdown (notion-to-md), Confluence → CommonMark (confluence-to-markdown), Zendesk/Intercom → markdown via REST + turndown/markdownify, Salesforce Knowledge → CSV → markdown. Preserves frontmatter, attachments, redirects. Use when changing KB platform.
---

# Content migration between KB platforms

## When to use

User says "migrate KB from Notion to Docusaurus", "leave Confluence", "Zendesk to Helpdesk", "consolidate KBs", "we're switching docs platforms". Reach BEFORE the cutover date and AFTER the destination IA is designed (taxonomy skill).

## Setup

```bash
# Notion → md
npm i -g notion-to-md
# or richer alternative
npm i -g @notion-stuff/v4-types notion-to-md

# Confluence → md
npm i -g confluence-to-markdown

# Generic HTML → md
pip install markdownify
# or
npm i -g turndown

# Useful tooling
pipx install httpx tenacity python-frontmatter
brew install pandoc       # for docx / rST source
```

Auth / API key requirements:
- `NOTION_TOKEN` — Notion integration; share source pages with integration
- `CONFLUENCE_USER` + `CONFLUENCE_API_TOKEN`
- `ZENDESK_USER` + `ZENDESK_API_TOKEN` + `ZENDESK_SUBDOMAIN`
- `INTERCOM_TOKEN`
- `DOCUMENT360_API_TOKEN`
- `HELPSCOUT_API_KEY`
- `SF_INSTANCE_URL` + `SF_ACCESS_TOKEN`

## Common recipes

### Recipe 1: Notion → markdown

```bash
# Single page
node -e "
const { Client } = require('@notionhq/client');
const { NotionToMarkdown } = require('notion-to-md');
const notion = new Client({ auth: process.env.NOTION_TOKEN });
const n2m = new NotionToMarkdown({ notionClient: notion });
(async () => {
  const blocks = await n2m.pageToMarkdown('$PAGE_ID');
  const md = n2m.toMarkdownString(blocks);
  console.log(md.parent);
})()
" > docs/page.md

# Whole database (each row = an article)
node scripts/notion-db-export.js > exported-pages.json
```

### Recipe 2: Notion database recursive export

```javascript
// scripts/notion-db-export.js
const { Client } = require('@notionhq/client');
const { NotionToMarkdown } = require('notion-to-md');
const fs = require('fs');
const notion = new Client({ auth: process.env.NOTION_TOKEN });
const n2m = new NotionToMarkdown({ notionClient: notion });
n2m.setCustomTransformer('callout', async (block) => {
  return `:::note\n${block.callout.rich_text.map(t=>t.plain_text).join('')}\n:::`;
});
(async () => {
  let cursor = undefined;
  do {
    const r = await notion.databases.query({
      database_id: process.env.DB_ID,
      start_cursor: cursor,
    });
    for (const page of r.results) {
      const title = page.properties.Title.title[0].plain_text;
      const slug = title.toLowerCase().replace(/[^a-z0-9]+/g,'-');
      const blocks = await n2m.pageToMarkdown(page.id);
      const body = n2m.toMarkdownString(blocks).parent;
      const fm = `---\ntitle: "${title}"\nslug: ${slug}\nstatus: published\nlast_verified: ${page.last_edited_time.slice(0,10)}\n---\n\n`;
      fs.writeFileSync(`docs/imported/${slug}.md`, fm + body);
    }
    cursor = r.next_cursor;
  } while (cursor);
})();
```

### Recipe 3: Confluence → markdown

```bash
# Spaces / pages listing
curl -G "https://${SITE}.atlassian.net/wiki/rest/api/content" \
  -u "${CONFLUENCE_USER}:${CONFLUENCE_API_TOKEN}" \
  --data-urlencode "spaceKey=DOCS" \
  --data-urlencode "expand=body.storage,ancestors,version" \
  --data-urlencode "limit=100" \
  > confluence-pages.json

# Convert each page's storage format → markdown
python scripts/confluence-export.py
```

```python
# scripts/confluence-export.py
import json, pathlib, html2text, frontmatter
h = html2text.HTML2Text()
h.body_width = 0
h.ignore_links = False
pages = json.load(open('confluence-pages.json'))['results']
for pg in pages:
    title = pg['title']
    slug = title.lower().replace(' ','-')
    md = h.handle(pg['body']['storage']['value'])
    post = frontmatter.Post(md, title=title, slug=slug,
        confluence_id=pg['id'],
        last_modified=pg['version']['when'][:10])
    pathlib.Path(f"docs/imported/{slug}.md").write_text(frontmatter.dumps(post))
```

### Recipe 4: Zendesk Guide → markdown

```bash
# List articles (paginate)
NEXT="https://${ZENDESK_SUBDOMAIN}.zendesk.com/api/v2/help_center/articles.json?per_page=100"
> zendesk-articles.json
while [ -n "$NEXT" ]; do
  resp=$(curl -s -u "${ZENDESK_USER}/token:${ZENDESK_API_TOKEN}" "$NEXT")
  echo "$resp" | jq -c '.articles[]' >> zendesk-articles.json
  NEXT=$(echo "$resp" | jq -r '.next_page // empty')
done
```

```python
# Transform HTML body → markdown
import json, pathlib, markdownify, frontmatter
with open('zendesk-articles.json') as f:
    for line in f:
        a = json.loads(line)
        slug = a['html_url'].split('/')[-1]
        md = markdownify.markdownify(a['body'], heading_style='ATX')
        post = frontmatter.Post(md,
            title=a['title'],
            slug=f"how-to/{slug}",
            zendesk_id=a['id'],
            last_modified=a['updated_at'][:10],
            tags=a.get('label_names', []),
        )
        pathlib.Path(f"docs/imported/{slug}.md").write_text(frontmatter.dumps(post))
```

### Recipe 5: Intercom Articles → markdown

```bash
# List articles
curl "https://api.intercom.io/articles?per_page=200" \
  -H "Authorization: Bearer $INTERCOM_TOKEN" \
  > intercom-articles.json

# Transform
python -c "
import json, pathlib, markdownify, frontmatter
data = json.load(open('intercom-articles.json'))
for a in data['data']:
    slug = a['url'].split('/')[-1] if a.get('url') else str(a['id'])
    md = markdownify.markdownify(a.get('body') or '', heading_style='ATX')
    post = frontmatter.Post(md, title=a['title'], slug=slug, intercom_id=a['id'])
    pathlib.Path(f'docs/imported/{slug}.md').write_text(frontmatter.dumps(post))
"
```

### Recipe 6: Salesforce Knowledge → markdown

```bash
# Export via SOQL → CSV
sf data query --query "SELECT Id, Title, UrlName, Article_Body__c, LastModifiedDate FROM Knowledge__kav WHERE PublishStatus='Online'" \
  --result-format csv > sf-knowledge.csv

# Transform
python scripts/sf-to-md.py sf-knowledge.csv docs/imported/
```

### Recipe 7: Attachment migration

```bash
# Confluence attachments
curl "https://${SITE}.atlassian.net/wiki/rest/api/content/${PAGE_ID}/child/attachment" \
  -u "${CONFLUENCE_USER}:${CONFLUENCE_API_TOKEN}" \
  | jq -r '.results[] | "\(.id) \(.title) \(._links.download)"' \
  | while read id title link; do
      curl -L "https://${SITE}.atlassian.net/wiki${link}" \
        -u "${CONFLUENCE_USER}:${CONFLUENCE_API_TOKEN}" \
        -o "docs/assets/${id}-${title}"
    done

# Rewrite references in MD
sed -i 's|/wiki/download/attachments/[0-9]*/\([^"]*\)|/assets/\1|g' docs/imported/*.md
```

### Recipe 8: Build redirect map

```python
# scripts/build-redirects.py
import json, pathlib, frontmatter
redirects = []
for p in pathlib.Path('docs/imported').rglob('*.md'):
    post = frontmatter.load(p)
    if 'old_url' in post:
        redirects.append({"from": post['old_url'], "to": f"/docs/{post['slug']}", "code": 301})
json.dump({"redirects": redirects}, open('redirects.json','w'), indent=2)
```

```
# Netlify _redirects equivalent
/old/path  /docs/how-to/x  301!
```

### Recipe 9: Validate — link-check + page-count parity

```bash
# Link check imported
lychee --format json --output report.json docs/imported/

# Page count parity
ORIGINAL=$(jq '.results | length' confluence-pages.json)
IMPORTED=$(find docs/imported -name '*.md' | wc -l)
echo "Source: $ORIGINAL, Target: $IMPORTED"
[ "$ORIGINAL" -ne "$IMPORTED" ] && echo "MISMATCH"
```

### Recipe 10: Visual spot-check via Playwright

```javascript
// scripts/visual-check.js
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext();
  for (const slug of process.argv.slice(2)) {
    const oldP = await ctx.newPage();
    const newP = await ctx.newPage();
    await oldP.goto(`https://old-kb.example.com/${slug}`);
    await newP.goto(`https://staging.docs.example.com/${slug}`);
    await oldP.screenshot({path: `diff/${slug}-old.png`});
    await newP.screenshot({path: `diff/${slug}-new.png`});
  }
  await browser.close();
})();
```

### Recipe 11: Cutover redirects (platform-native)

```json
// Vercel vercel.json
{"redirects":[{"source":"/old/path","destination":"/docs/how-to/x","permanent":true}]}
```

```
# Cloudflare Pages _redirects (same syntax as Netlify)
/old/path  /docs/how-to/x  301
```

## Examples

### Example 1: Notion → Docusaurus migration

**Goal:** 180 Notion pages → Docusaurus repo.

**Steps:**
1. Design destination IA (taxonomy skill).
2. Export via `notion-to-md` (Recipe 2).
3. Rewrite Notion mentions / links to internal paths.
4. Migrate attachments to `static/img/`.
5. Build redirect map (Recipe 8) for Notion shared URLs.
6. Lychee + page-count parity (Recipe 9).
7. Visual spot-check 10 articles (Recipe 10).
8. Soft launch (banner on Notion: "We've moved →"); DNS cutover; keep Notion read-only 30d.

**Result:** Clean Docusaurus site with redirects from Notion URLs.

### Example 2: Confluence → MkDocs

**Goal:** 400 Confluence pages → MkDocs Material.

**Steps:**
1. Export space → JSON (Recipe 3).
2. Transform via `html2text` → md.
3. Migrate attachments (Recipe 7).
4. Sidebar nav (taxonomy skill output).
5. Validate (Recipe 9).
6. Cutover with redirects (Recipe 11).

**Result:** MkDocs site live; Confluence kept as historical archive.

## Edge cases / gotchas

- **Notion blocks not all supported by notion-to-md** — synced_blocks, columns, embeds may need custom transformers.
- **Confluence storage format ≠ HTML** — has `<ac:*>` macro tags; `html2text` ignores them. Implement macro handlers (info panel → `:::note`).
- **Zendesk article_attachments** are separate from article body — must list per-article.
- **Intercom rich-text body** sometimes returned as JSON deltas; check `body` field type before markdownify.
- **Salesforce Knowledge categories vs Data Categories** — Data Categories don't export via SOQL; use Tooling API or manual map.
- **Redirect explosion** — Notion auto-generates random URL slugs. Map old slug → new path; expect 1:1 redirect per page.
- **Code fences in HTML** often have language hints lost — extract `<pre><code class="language-x">` to preserve.
- **DNS TTL** — drop to 60s 24h before cutover; raise back after.
- **Soft launch period** — minimum 7d; 30d safer.
- **Don't migrate everything** — apply audit (stale/redundant) BEFORE migration; ~20% of articles typically discarded.
- **Internal links break first** — rewrite during transform, not in a second pass.
- **Permissions / ACL migration** — SSO groups don't auto-port; rebuild on target.

## Sources

- notion-to-md: https://github.com/souvikinator/notion-to-md
- Notion API blocks reference: https://developers.notion.com/reference/block
- confluence-to-markdown: https://github.com/meridius/confluence-to-markdown
- Confluence REST v2: https://developer.atlassian.com/cloud/confluence/rest/v2/
- Zendesk Help Center API: https://developer.zendesk.com/api-reference/help_center/help-center-api/articles/
- Intercom Articles API: https://developers.intercom.com/intercom-api-reference/reference/the-article-model
- Salesforce Knowledge API: https://developer.salesforce.com/docs/atlas.en-us.knowledge_dev.meta/knowledge_dev/sforce_api_objects_knowledgearticleversion.htm
- markdownify (Python): https://github.com/matthewwithanm/python-markdownify
- turndown (JS): https://github.com/mixmark-io/turndown
