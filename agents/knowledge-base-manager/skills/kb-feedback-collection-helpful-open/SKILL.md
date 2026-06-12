---
name: kb-feedback-collection-helpful-open
description: Per-article binary helpful/not-helpful feedback + optional open text on "not helpful". Native KB-platform widgets (Mintlify, Document360, Intercom, Zendesk) OR a FOSS fallback via Cloudflare Workers / Vercel API routes writing to Notion or Airtable. Use when articles ship without any feedback signal beyond views.
---

# KB feedback collection — helpful / not-helpful + open feedback

## When to use

Reach for this skill when the user says: "we have no idea which articles work", "no feedback on docs", "add a thumbs-up", "let users tell us when a page is wrong", "open-text feedback", "collect helpfulness ratings", or "wire feedback into our triage queue". This skill covers binary helpful/not-helpful + open follow-up; for in-product survey-style feedback (NPS, CSAT) defer to the marketing agent's survey skill. For AI-assistant thumbs (Kapa/Inkeep), use `ai-doc-assistant-kapa-inkeep-mendable` instead — the AI feedback is built-in.

## Setup

```bash
# FOSS fallback: Cloudflare Workers + Notion storage
npm i -g wrangler
wrangler login

# Native KB platform widgets — no install; configure via dashboard
# Mintlify: feedback is built-in (mintlify.json setting)
# Document360: built-in (settings → article feedback)
# Intercom Articles: built-in (Help Center settings)
# Zendesk Guide: built-in (per-article)
```

Auth / env vars:
- `CLOUDFLARE_API_TOKEN` — Workers + Pages deploy. Free tier 100k requests/day.
- `NOTION_API_TOKEN` — only if writing to Notion DB. Free for personal/team.
- `AIRTABLE_API_KEY` — only if writing to Airtable. Free up to 1k rows.
- `SLACK_WEBHOOK_URL` — to alert on "not helpful" responses. Free.

## Common recipes

### Recipe 1: Cloudflare Worker that accepts feedback + writes to Notion

```js
// worker.js
export default {
  async fetch(request, env) {
    if (request.method !== 'POST') return new Response('Method not allowed', { status: 405 });
    if (request.headers.get('origin') !== 'https://docs.example.com') {
      return new Response('Forbidden', { status: 403 });
    }
    const { article_id, helpful, comment, page_url } = await request.json();

    // Write to Notion
    const resp = await fetch('https://api.notion.com/v1/pages', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${env.NOTION_API_TOKEN}`,
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        parent: { database_id: env.NOTION_DB_ID },
        properties: {
          Article: { title: [{ text: { content: article_id } }] },
          Helpful: { checkbox: !!helpful },
          Comment: { rich_text: [{ text: { content: comment || '' } }] },
          URL: { url: page_url },
          Timestamp: { date: { start: new Date().toISOString() } },
        },
      }),
    });

    // Alert Slack on "not helpful" with comment
    if (!helpful && comment && env.SLACK_WEBHOOK_URL) {
      await fetch(env.SLACK_WEBHOOK_URL, {
        method: 'POST',
        body: JSON.stringify({ text: `Not helpful on ${page_url}: ${comment}` }),
      });
    }

    return new Response(JSON.stringify({ ok: resp.ok }), {
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': 'https://docs.example.com' },
    });
  },
};
```

```bash
# Deploy
wrangler init kb-feedback
wrangler secret put NOTION_API_TOKEN
wrangler secret put NOTION_DB_ID
wrangler secret put SLACK_WEBHOOK_URL
wrangler deploy
```

### Recipe 2: Drop-in HTML form for the worker

```html
<!-- Drop into every KB article footer -->
<div class="kb-feedback" data-article-id="how-to/sso-okta">
  <p>Was this article helpful?</p>
  <button class="kb-fb-yes">Yes</button>
  <button class="kb-fb-no">No</button>
  <div class="kb-fb-followup" hidden>
    <textarea placeholder="What was missing or wrong?"></textarea>
    <button class="kb-fb-submit">Send</button>
  </div>
</div>

<script>
document.querySelectorAll('.kb-feedback').forEach(box => {
  const articleId = box.dataset.articleId;
  const send = (helpful, comment = '') => fetch('https://kb-feedback.acme.workers.dev', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ article_id: articleId, helpful, comment, page_url: location.href }),
  });
  box.querySelector('.kb-fb-yes').onclick = () => { send(true); box.innerHTML = 'Thanks!'; };
  box.querySelector('.kb-fb-no').onclick = () => { box.querySelector('.kb-fb-followup').hidden = false; };
  box.querySelector('.kb-fb-submit').onclick = () => {
    const c = box.querySelector('textarea').value;
    send(false, c);
    box.innerHTML = 'Thanks — we will look into it.';
  };
});
</script>
```

### Recipe 3: Mintlify native feedback (`docs.json`)

```json
{
  "feedback": {
    "thumbsRating": true,
    "suggestEdit": true,
    "raiseIssue": true
  }
}
```

Mintlify renders thumbs + optional comment at the bottom of every page; data lands in the Mintlify dashboard. "Suggest edit" links to the source repo; "Raise issue" opens a GitHub issue prefilled with the article URL.

### Recipe 4: Document360 article feedback API

```bash
# Enable feedback in the dashboard, then pull responses via API
curl -X GET 'https://apihub.document360.io/v2/Feedbacks' \
  -H "api_token: $DOC360_API_TOKEN" \
  -G --data-urlencode 'startDate=2026-05-01' \
  --data-urlencode 'endDate=2026-05-31' \
  > feedback-may.json

# Group by article
jq 'group_by(.articleId) | map({article: .[0].articleTitle, total: length, negative: ([.[]|select(.feedbackType=="Negative")]|length)})' feedback-may.json
```

### Recipe 5: Intercom Articles feedback via Help Center settings

```bash
# Reactions are on by default in Intercom Help Center. Pull via Reporting API.
curl -X GET 'https://api.intercom.io/articles' \
  -H "Authorization: Bearer $INTERCOM_ACCESS_TOKEN" \
  -H 'Intercom-Version: 2.11' \
  > articles.json

# Per-article stats live in dashboard → Articles → Reporting (no per-article reaction API yet 2026)
```

### Recipe 6: Zendesk Guide article vote-up/vote-down API

```bash
# Aggregate per-article votes for the last 30 days
curl -X GET "https://$ZD_SUBDOMAIN.zendesk.com/api/v2/help_center/articles?include=vote_sum,vote_count" \
  -u "$ZENDESK_USER/token:$ZENDESK_API_TOKEN" \
  | jq '.articles[] | {id, title, vote_sum, vote_count, score: (.vote_sum/.vote_count)}' \
  | jq -s 'sort_by(.score)'

# Pull individual votes for one article
curl -X GET "https://$ZD_SUBDOMAIN.zendesk.com/api/v2/help_center/articles/<id>/votes" \
  -u "$ZENDESK_USER/token:$ZENDESK_API_TOKEN"
```

### Recipe 7: Weekly digest of "not helpful" votes to Slack

```bash
#!/usr/bin/env bash
# digest.sh — run on cron Friday morning
START=$(date -d '7 days ago' +%Y-%m-%d)
WORST=$(curl -s -u "$ZENDESK_USER/token:$ZENDESK_API_TOKEN" \
  "https://$ZD_SUBDOMAIN.zendesk.com/api/v2/help_center/articles?include=vote_sum,vote_count" \
  | jq -r '.articles[] | select(.vote_count > 5) | "\(.vote_sum)|\(.title)|\(.html_url)"' \
  | sort -n | head -5 | awk -F'|' '{printf "%s (score %s) — %s\\n", $2, $1, $3}')

curl -X POST -H 'Content-Type: application/json' \
  -d "{\"text\":\":mag: KB feedback — bottom 5 articles this week:\\n$WORST\"}" \
  "$SLACK_WEBHOOK_URL"
```

Add to `.github/workflows/feedback-digest.yml` with weekly cron.

### Recipe 8: Anti-abuse rate-limit on the Worker

```js
// Add to the Cloudflare Worker
const key = request.headers.get('cf-connecting-ip') + ':' + article_id;
const recent = await env.FEEDBACK_KV.get(key);
if (recent) return new Response('Too many submissions', { status: 429 });
await env.FEEDBACK_KV.put(key, '1', { expirationTtl: 600 });  // 10-min cool-down per IP per article
```

KV namespace lives free under Cloudflare's free tier (100k reads + 1k writes/day).

### Recipe 9: Feedback → triage Linear ticket (Notion automation route)

```js
// Notion automation triggered when "Helpful" = false AND "Comment" not empty
// Create a Linear ticket with the comment + page URL
fetch('https://api.linear.app/graphql', {
  method: 'POST',
  headers: { 'Authorization': process.env.LINEAR_API_KEY, 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: `mutation { issueCreate(input: { teamId: "${TEAM_ID}", title: "KB feedback: ${article_id}", description: "URL: ${page_url}\n\n${comment}" }) { success } }`,
  }),
});
```

Connects feedback to the doc team's triage queue.

### Recipe 10: Per-article CSV export for content-audit cross-reference

```bash
# Export 90d feedback for the content-audit playbook (axis: inaccurate)
curl -s "https://api.notion.com/v1/databases/$NOTION_FEEDBACK_DB/query" \
  -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H 'Notion-Version: 2022-06-28' \
  -d '{"filter":{"property":"Timestamp","date":{"past_90_days":{}}}}' \
  | jq -r '.results[] | [.properties.Article.title[0].plain_text, .properties.Helpful.checkbox, .properties.Comment.rich_text[0].plain_text] | @csv' \
  > feedback-90d.csv
```

Cross-reference with content audit "stale" list — articles that are stale AND drawing negative feedback get top-of-queue.

## Examples

### Example 1: Ship feedback widget on a static docs site (no platform-native)

**Goal:** Docusaurus site has no feedback; ship binary + open feedback in one afternoon.

**Steps:**
1. Build the Worker (Recipe 1) + deploy: `wrangler deploy`.
2. Create Notion database with columns: Article, Helpful, Comment, URL, Timestamp.
3. Add the HTML form (Recipe 2) to `src/theme/DocItemFooter.tsx`.
4. Test: click "No" on a doc, leave a comment, verify Notion row appears.
5. Wire Slack alert (Recipe 1, already included).
6. Weekly digest cron (Recipe 7).

**Result:** End-to-end feedback loop in <2h; free as long as <100k/day requests.

### Example 2: Mintlify-native feedback + dashboard review

**Goal:** Mintlify docs already on the platform; turn on feedback + review weekly.

**Steps:**
1. Add `feedback.thumbsRating: true` + `suggestEdit: true` + `raiseIssue: true` (Recipe 3).
2. Push to repo; Mintlify rebuilds.
3. Review feedback weekly via Mintlify dashboard → Analytics → Feedback.
4. Map low-score articles to content-audit "inaccurate" axis.

**Result:** Zero-code rollout; thumbs + edit + issue links in 24h.

### Example 3: Cross-reference feedback into the weekly KB analytics report

**Goal:** "Worst-feedback articles" appears in the doc-analytics playbook weekly report.

**Steps:**
1. Export 7d feedback CSV (Recipe 10 with date filter).
2. Aggregate: per-article negative-vote count.
3. Top 5 negative-vote articles → "Fix first" section of weekly KB analytics report (from `doc-analytics-clarity-ga4-algolia-insights`).
4. Each is assigned to its CODEOWNERS owner via stale-bot mechanism.

**Result:** Feedback drives the same fix-queue as exit-rate + rage-clicks.

## Edge cases / gotchas

- **Survivorship bias** — only motivated users vote. Don't take vote_sum as truth; combine with views (low-view + low-vote may indicate "no one finds it" vs "no one likes it").
- **Vote farming / spam** — rate-limit by IP+article (Recipe 8). Bots love empty feedback forms.
- **GDPR / consent** — open-text comments may contain PII. If you log user email or IP, document retention + offer deletion. Cloudflare Workers KV is GDPR-friendly if data center region is set to EU.
- **Comment quality** — most are 1-3 word complaints. Don't treat as a content brief — treat as a triage signal.
- **"Suggest edit" GitHub flow** — only works if your docs are public-source. Hide on closed-source repos to avoid 404s.
- **Mintlify "Raise issue" mode** — links to a repo issue; if your docs repo is private, this confuses readers. Switch off if private.
- **Don't show feedback in the navigation flow** — bottom of article only; otherwise it interrupts the read.
- **Form gets lost on long pages** — sticky footer on mobile is acceptable; modal popup is not.
- **Zendesk vote API** — `vote_sum` = upvotes - downvotes; `vote_count` = total votes. Negative `vote_sum` with high `vote_count` = clearly broken; negative with low `vote_count` = noise.
- **Intercom Help Center reactions** — only in the Help Center UI; no per-article reaction REST endpoint as of 2026. Pull via Reporting dashboard.
- **Document360 feedback API** — requires Business plan; Free tier captures feedback in the dashboard but lacks API export.
- **No auto-translation of feedback** — non-English comments will sit in your queue unless you wire DeepL or similar.
- **Don't auto-close as resolved** — even after you fix the article, leave the feedback row open until a human verifies. Closing prematurely loses learning signal.
- **CORS misconfig kills the Worker** — `Access-Control-Allow-Origin` must match the docs site origin EXACTLY (no trailing slash, no wildcards on POST).

## Sources

- [Mintlify feedback settings](https://mintlify.com/docs/settings/feedback)
- [Document360 article feedback](https://docs.document360.com/docs/article-feedback)
- [Document360 feedback API](https://apidocs.document360.com/apidocs/feedbacks)
- [Intercom Help Center reactions](https://www.intercom.com/help/en/articles/8158031-react-to-help-center-articles)
- [Zendesk Guide vote API](https://developer.zendesk.com/api-reference/help_center/help-center-api/votes/)
- [Cloudflare Workers free plan](https://developers.cloudflare.com/workers/platform/pricing/)
- [Cloudflare Workers KV](https://developers.cloudflare.com/kv/)
- [Notion pages API](https://developers.notion.com/reference/post-page)
- [Airtable web API](https://airtable.com/developers/web/api)
- [Slack incoming webhooks](https://api.slack.com/messaging/webhooks)
