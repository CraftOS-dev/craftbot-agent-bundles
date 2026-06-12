---
name: kb-roi-deflection-rate
description: KB ROI + deflection — per-category deflection (views with no follow-up ticket in 24h / total views), $ saved formula, CRM "Self-Serve Health" custom property in Salesforce/HubSpot. Use when CFO asks "what does the KB return?" or CS leadership wants ROI.
---

# KB ROI — deflection rate, ticket reduction, $ saved

## When to use

User says "deflection rate", "KB ROI", "$ saved", "self-serve health", "tie KB to CRM", "show finance the docs return". Reach AFTER analytics is wired (Recipe relies on KB-view + ticket-open events). Defer support-process design to `customer-support-agent`.

## Setup

```bash
# CLI tooling — Salesforce CLI, HubSpot CLI
npm i -g @hubspot/cli
brew install salesforce-cli   # or: npm i -g @salesforce/cli

# Auth
sf org login web              # Salesforce
hs auth                       # HubSpot

# Intercom/Zendesk REST: API tokens from each app's developer settings
```

Auth / API key requirements:
- `INTERCOM_TOKEN` — Intercom Developer Hub → access token
- `ZENDESK_USER` + `ZENDESK_API_TOKEN` — Zendesk Admin → API
- `SALESFORCE_INSTANCE_URL` + `SALESFORCE_ACCESS_TOKEN`
- `HUBSPOT_PRIVATE_APP_TOKEN`

## Common recipes

### Recipe 1: Define deflection formula

```
Deflection rate (per category, 24h window) =
  (# KB views by account X in category C with NO ticket opened by account X in category C within 24h)
   / (total KB views by account X in category C)
```

Per-category, not per-article (article-level signal is too noisy at low volume).

### Recipe 2: Wire KB-view event

```javascript
// in your KB site (Docusaurus, Mintlify, etc.)
window.addEventListener('load', () => {
  const accountId = getCookie('account_id') || 'anon';
  fetch('https://events.example.com/track', {
    method: 'POST',
    body: JSON.stringify({
      event: 'kb_view',
      account_id: accountId,
      article_id: window.location.pathname,
      category: document.querySelector('meta[name=kb_category]')?.content,
      timestamp: new Date().toISOString(),
    }),
  });
});
```

### Recipe 3: Pull Intercom conversations for 24h join

```bash
curl -X POST "https://api.intercom.io/conversations/search" \
  -H "Authorization: Bearer $INTERCOM_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query":{"operator":"AND","value":[
      {"field":"created_at","operator":">","value":'$(date -d '7 days ago' +%s)'},
      {"field":"created_at","operator":"<","value":'$(date +%s)'}
    ]},
    "pagination":{"per_page":150}
  }' \
  | jq '.conversations[] | {id:.id, account:.contacts.contacts[0].external_id, tags:.tags.tags|map(.name), opened:.created_at}'
```

### Recipe 4: Pull Zendesk tickets

```bash
curl -G "https://${ZENDESK_SUBDOMAIN}.zendesk.com/api/v2/incremental/tickets/cursor.json" \
  -u "${ZENDESK_USER}/token:${ZENDESK_API_TOKEN}" \
  --data-urlencode "start_time=$(date -d '7 days ago' +%s)" \
  | jq '.tickets[] | {id, organization_id, tags, created_at}'
```

### Recipe 5: Compute deflection per category (Python)

```python
# deflection.py
import duckdb
con = duckdb.connect()
con.execute("""
CREATE TABLE views AS SELECT * FROM read_json('kb-views-7d.json');
CREATE TABLE tickets AS SELECT * FROM read_json('tickets-7d.json');

CREATE TABLE joined AS
SELECT v.category,
       COUNT(*) AS total_views,
       SUM(CASE WHEN t.id IS NULL THEN 1 ELSE 0 END) AS deflected
FROM views v
LEFT JOIN tickets t
  ON v.account_id = t.account_id
 AND v.category = t.category
 AND t.created_at BETWEEN v.timestamp AND v.timestamp + INTERVAL 24 HOUR
GROUP BY v.category;

SELECT category, total_views, deflected,
       deflected::FLOAT / total_views AS deflection_rate
FROM joined
ORDER BY total_views DESC;
""")
for row in con.fetchall():
    print(f"{row[0]:25}  views={row[1]:>6}  deflect={row[3]:.1%}")
```

### Recipe 6: $-saved calculation

```python
# Assumption: loaded support cost per ticket (CS salary + tooling / # tickets handled)
COST_PER_TICKET = 50.0   # adjust per org

con.execute("""
SELECT category,
       total_views,
       deflected,
       deflected * """ + str(COST_PER_TICKET) + """ AS dollars_saved
FROM joined
""")
```

### Recipe 7: Write "Self-Serve Health" custom property in Salesforce

```bash
# Add custom field via Metadata API or sf CLI
sf data create record \
  --sobject CustomField__c \
  --values 'Name="Self_Serve_Health" Type=Number AccountId=...'

# Write per-account score
sf data update record --sobject Account --record-id $ACCOUNT_ID \
  --values "Self_Serve_Health__c=0.94"
```

### Recipe 8: HubSpot custom property + update

```bash
# Create
curl -X POST "https://api.hubapi.com/crm/v3/properties/companies" \
  -H "Authorization: Bearer $HUBSPOT_PRIVATE_APP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"self_serve_health",
    "label":"Self-Serve Health",
    "type":"number",
    "fieldType":"number",
    "groupName":"company_information"
  }'

# Update for one company
curl -X PATCH "https://api.hubapi.com/crm/v3/objects/companies/$COMPANY_ID" \
  -H "Authorization: Bearer $HUBSPOT_PRIVATE_APP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"properties":{"self_serve_health":0.94}}'
```

### Recipe 9: Quarterly deflection report (markdown)

```python
quarter = "2026-Q2"
print(f"# Deflection — {quarter}\n")
print("| Category | Views | Tickets (same cat, 24h) | Deflection rate | $ saved |")
print("|---|---|---|---|---|")
totals = [0, 0, 0]
for row in con.fetchall():
    cat, views, defl, _ = row
    tickets = views - defl
    saved = defl * COST_PER_TICKET
    print(f"| {cat} | {views:,} | {tickets:,} | {defl/views:.1%} | ${saved:,.0f} |")
    totals = [totals[0]+views, totals[1]+tickets, totals[2]+saved]
print(f"| **Total** | **{totals[0]:,}** | **{totals[1]:,}** | **{(totals[0]-totals[1])/totals[0]:.1%}** | **${totals[2]:,.0f}** |")
```

### Recipe 10: Per-article ROI for top-traffic pages

```python
# views × per-category-deflection × cost = $/article/month
TOP = con.execute("""
SELECT article_id, category, COUNT(*) AS views
FROM views WHERE timestamp > now() - INTERVAL 30 DAY
GROUP BY 1,2 ORDER BY views DESC LIMIT 50
""").fetchall()

for art, cat, views in TOP:
    rate = DEFLECTION_BY_CAT[cat]
    monthly = views * rate * COST_PER_TICKET
    print(f"{art:50} {monthly:>10,.0f} $/mo")
```

### Recipe 11: Surface in Slack to CS team

```bash
curl -X POST "$SLACK_WEBHOOK_CS" \
  -H 'Content-Type: application/json' \
  -d "{\"text\":\"📈 KB Deflection Q2: 93.4% (Auth 96%, Billing 92%, Webhooks 89%). ~\\$118k saved.\"}"
```

## Examples

### Example 1: Stand up quarterly deflection report

**Goal:** First quarterly $-saved number for board deck.

**Steps:**
1. Wire `kb_view` event (Recipe 2) — 1 day to ship.
2. Pull 7d of views + tickets (Recipes 3, 4) — 1 hour.
3. Run deflection script (Recipe 5) — 5 min.
4. Compute $-saved (Recipe 6).
5. Write Salesforce/HubSpot property per account (Recipes 7, 8).
6. Generate quarterly report (Recipe 9).

**Result:** "Q2 KB deflected 93.4% of would-be tickets in covered categories, saving ~$118k."

### Example 2: Use deflection to prioritize content roadmap

**Goal:** Decide which categories need more articles.

**Steps:**
1. Per-category deflection rate (Recipe 5).
2. Multiply by ticket volume — low deflection + high volume = highest ROI to improve.
3. Cross-reference with no-result-found terms in that category (from `doc-analytics-...` skill).
4. Write article briefs ranked by expected $-saved (Recipe 10).

**Result:** Editorial roadmap weighted by $ impact, not gut feel.

## Edge cases / gotchas

- **Anonymous KB views** — anon cookie won't join to ticket. Anonymous viewers don't count in deflection denominator.
- **Cross-category misattribution** — user views Auth article, opens Billing ticket; that's not a failure. Per-category join is essential.
- **24h window is heuristic** — for billing-cycle questions, 7d window may be more accurate. Test both.
- **Salesforce custom fields require admin** — request from CRM admin before scripting.
- **HubSpot Free tier** has limited custom-property writes; use Operations Hub for bulk.
- **$-per-ticket varies wildly** — loaded cost typically $25-$100. Get from CS Ops; don't assume.
- **Deflection ≠ avoidance** — high deflection in a category may indicate clear articles OR low confusion. Look at ticket volume too.
- **Don't game the metric** — articles that "deflect" by being so confusing users give up are worse than no article. Pair with helpful% feedback.
- **Cookie consent** — GDPR/CCPA blocks `account_id` cookie for users who decline; deflection is undercounted for these users.

## Sources

- Intercom Conversations API: https://developers.intercom.com/intercom-api-reference/reference/listconversations
- Zendesk Tickets API: https://developer.zendesk.com/api-reference/ticketing/tickets/tickets/
- Salesforce Custom Fields: https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_customfield.htm
- HubSpot Custom Properties: https://developers.hubspot.com/docs/api/crm/properties
- HelpScout deflection benchmark: https://www.helpscout.com/blog/customer-self-service/
- Intercom Help Center reporting: https://www.intercom.com/help/en/articles/3539921-help-center-reporting
