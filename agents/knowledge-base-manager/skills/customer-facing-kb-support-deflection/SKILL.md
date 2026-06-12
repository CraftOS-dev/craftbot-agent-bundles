---
name: customer-facing-kb-support-deflection
description: Customer-facing KB strategy — Intercom Articles, Zendesk Guide, Pylon Help Center, Help Scout Docs, Document360, Helpjuice, Bloomfire. In-product Help widget, transactional-email KB links, top-10-ticket-categories drives top-10-articles. Use when standing up a customer support KB.
---

# Customer-facing KB — support deflection

## When to use

User says "set up customer KB", "Help Center", "in-app help widget", "deflect tickets", "article-from-ticket workflow". Reach AFTER taxonomy is settled and AS the bridge between KB and support data.

Defer support-workflow design (Macros, escalation paths) to `customer-support-agent`. This skill covers the KB-as-deflection-product side.

## Setup

```bash
# Intercom CLI (community)
npm i -g intercom-api
# or use REST directly with curl

# Zendesk CLI
gem install zendesk_cli
# or use Zendesk's REST

# Pylon — REST only
# Document360 — REST only
```

Auth / API key requirements:
- `INTERCOM_TOKEN` — Intercom Developer Hub
- `ZENDESK_USER` + `ZENDESK_API_TOKEN` + `ZENDESK_SUBDOMAIN`
- `PYLON_API_KEY` — Pylon Settings → API
- `HELPSCOUT_API_KEY` — Help Scout My App → API keys
- `DOCUMENT360_API_TOKEN` — Document360 Settings → API tokens
- `HELPJUICE_API_KEY`
- `BLOOMFIRE_TOKEN`

## Common recipes

### Recipe 1: Pull top 10 ticket categories (last 90d) — driver for KB roadmap

```bash
# Zendesk
curl -G "https://${ZENDESK_SUBDOMAIN}.zendesk.com/api/v2/incremental/tickets/cursor.json" \
  -u "${ZENDESK_USER}/token:${ZENDESK_API_TOKEN}" \
  --data-urlencode "start_time=$(date -d '90 days ago' +%s)" \
  | jq -r '.tickets[] | .tags[]' \
  | sort | uniq -c | sort -rn | head -10
```

```bash
# Intercom
curl -X POST "https://api.intercom.io/conversations/search" \
  -H "Authorization: Bearer $INTERCOM_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":{"field":"created_at","operator":">","value":'$(date -d '90 days ago' +%s)'},"pagination":{"per_page":150}}' \
  | jq -r '.conversations[].tags.tags[].name' \
  | sort | uniq -c | sort -rn | head -10
```

### Recipe 2: Create Intercom article

```bash
curl -X POST "https://api.intercom.io/articles" \
  -H "Authorization: Bearer $INTERCOM_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"How to reset your password",
    "description":"Steps to recover account access",
    "body":"<h2>Steps</h2><ol><li>Click forgot password.</li>...</ol>",
    "author_id":12345,
    "state":"published",
    "parent_id":67890,
    "parent_type":"collection"
  }'
```

### Recipe 3: Create Zendesk Guide article

```bash
curl -X POST "https://${ZENDESK_SUBDOMAIN}.zendesk.com/api/v2/help_center/sections/$SECTION_ID/articles.json" \
  -u "${ZENDESK_USER}/token:${ZENDESK_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "article":{
      "title":"How to reset your password",
      "body":"<h2>Steps</h2>...",
      "locale":"en-us",
      "user_segment_id": null,
      "permission_group_id": 12345,
      "draft": false
    }
  }'
```

### Recipe 4: Pylon Help Center article

```bash
curl -X POST "https://api.usepylon.com/articles" \
  -H "Authorization: Bearer $PYLON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Reset your password",
    "body_markdown":"## Steps\n1. Click forgot password...",
    "collection_id":"col_123",
    "is_published": true
  }'
```

### Recipe 5: Document360 article

```bash
curl -X POST "https://apihub.document360.io/v2/Articles" \
  -H "api_token: $DOCUMENT360_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Reset password",
    "content":"<h2>Steps</h2>...",
    "category_id":"cat_abc",
    "language_code":"en"
  }'
```

### Recipe 6: Helpjuice article create

```bash
curl -X POST "https://yourdomain.helpjuice.com/api/v2/articles" \
  -H "Authorization: $HELPJUICE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"article":{"name":"Reset password","body":"...","category_id":42}}'
```

### Recipe 7: Bloomfire post

```bash
curl -X POST "https://api.bloomfire.com/api/v2/posts" \
  -H "X-Auth-Token: $BLOOMFIRE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Reset password","html_body":"...","series_id":"abc"}'
```

### Recipe 8: Help Scout Docs article

```bash
curl -X POST "https://docsapi.helpscout.net/v1/collections/$COL_ID/articles" \
  -u "$HELPSCOUT_API_KEY:X" \
  -H "Content-Type: application/json" \
  -d '{"name":"Reset password","text":"...","status":"published"}'
```

### Recipe 9: In-app Intercom Help widget

```html
<!-- Intercom Messenger with Help Center articles -->
<script>
  window.intercomSettings = {
    app_id: "YOUR_APP_ID",
    custom_launcher_selector: "#help-button",
  };
</script>
<script src="https://widget.intercom.io/widget/YOUR_APP_ID"></script>

<button id="help-button">Need help?</button>
```

### Recipe 10: Pylon Help Widget

```html
<script src="https://pylon-chat.us.usepylon.com/snippet" defer></script>
<script>
  window.pylon = {
    app_id: "YOUR_APP_ID",
    user: { email: "user@example.com", name: "Jane" }
  };
</script>
```

### Recipe 11: Cluster tickets → article roadmap (LLM-assist)

```python
# scripts/cluster-tickets.py
import json, anthropic
client = anthropic.Anthropic()
tickets = json.load(open('tickets-90d.json'))
sample = [t['subject'] + '\n' + t['description'][:500] for t in tickets[:300]]
msg = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    messages=[{"role":"user","content":
        "Cluster these support tickets by root cause. Return top 10 clusters as JSON: [{cluster, count, suggested_article}].\n\n" + "\n---\n".join(sample)
    }]
)
print(msg.content[0].text)
```

### Recipe 12: Transactional-email KB link injection

```html
<!-- In your transactional email template -->
<p>Trouble signing in?</p>
<p><a href="https://help.example.com/how-to/sign-in-issues?utm_source=email&utm_campaign=transactional">Read troubleshooting guide</a></p>
```

### Recipe 13: Per-category deflection vs ticket volume report

See `kb-roi-deflection-rate` skill — this skill feeds it the content + analytics events.

## Examples

### Example 1: Stand up customer KB on Intercom

**Goal:** 0 → 25 articles covering top 10 ticket categories.

**Steps:**
1. Pull top 10 ticket categories (Recipe 1).
2. LLM-cluster tickets within each category (Recipe 11) → article briefs.
3. Author 25 articles (using templates from `kb-authoring-training-...`).
4. Bulk create via Intercom API (Recipe 2).
5. Wire in-app Messenger Help (Recipe 9).
6. Add KB links to transactional emails (Recipe 12).
7. Measure deflection per category (Recipe 13).

**Result:** ~30% of would-be tickets self-served within 60d.

### Example 2: Migrate Help Scout → Pylon

**Goal:** Consolidate KB into Pylon for B2B-support workflow.

**Steps:**
1. Export Help Scout articles via Recipe 8 (GET variant).
2. Transform to Pylon shape (HTML body, collection mapping).
3. Bulk create via Recipe 4.
4. Redirect Help Scout URLs to Pylon (DNS/proxy).
5. Embed Pylon widget (Recipe 10).

**Result:** Single Help Center; widget surfaces articles by user context.

## Edge cases / gotchas

- **Intercom rate-limit** — 83 req/sec; bulk imports need batching + retry.
- **Zendesk article body is HTML** — markdown won't render; convert first via markdownify reverse.
- **Pylon API beta** — endpoints can shift; pin to documented version. Confirm scope per integration.
- **Document360 workflows** require Pro tier+; on Free, just publish directly.
- **Helpjuice API** uses domain prefix (`yourcompany.helpjuice.com`); not a static host.
- **Bloomfire vs traditional KB** — designed for tribal knowledge sharing; "post" terminology vs "article".
- **In-app widgets and CSP** — `script-src` must allow the vendor domain. Confirm before shipping.
- **GDPR/CCPA for in-app help** — widgets capture session data; document the cookie usage.
- **Article-from-ticket** — don't just copy ticket text into KB; rewrite to general case with author voice.
- **Soft vs hard deflection** — clicking an article ≠ resolution. Pair view event with no-ticket-24h join.
- **Help Center search vs main KB search** — when both exist, search becomes confusing. Pick one search source-of-truth.

## Sources

- Intercom Articles API: https://developers.intercom.com/intercom-api-reference/reference/the-article-model
- Intercom Help Center reporting: https://www.intercom.com/help/en/articles/3539921-help-center-reporting
- Zendesk Help Center API: https://developer.zendesk.com/api-reference/help_center/help-center-api/articles/
- Pylon API: https://docs.usepylon.com/
- Document360 API: https://apidocs.document360.com/
- Help Scout Docs API: https://developer.helpscout.com/docs-api/
- Helpjuice API: https://help.helpjuice.com/en_US/api-v3
- Bloomfire API: https://developers.bloomfire.com/
- Intercom Messenger: https://developers.intercom.com/installing-intercom/web/installation/
