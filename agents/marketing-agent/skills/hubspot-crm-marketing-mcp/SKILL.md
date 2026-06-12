<!--
Source: https://developers.hubspot.com/mcp
HubSpot remote MCP: mcp.hubspot.com (GA April 2026, OAuth 2.1 + PKCE)
-->
# HubSpot CRM + Marketing MCP — SKILL

HubSpot's remote MCP at `mcp.hubspot.com` went GA April 2026 with OAuth 2.1 + PKCE. Full CRM + Marketing Hub coverage: contacts, deals, companies, lists, landing pages, forms, workflows, scoring, sequences. **The B2B marketing-agent default** for lifecycle, lead capture, scoring, and revenue attribution.

## When to use this skill

- **B2B / SaaS / services brand** with sales-led or PLG motion.
- **Landing page generation** programmatically via `create_landing_page`.
- **Form + consent capture** via `create_form` (GDPR-compliant fields).
- **Contact scoring** for lead handoff (MQL → SQL).
- **Deal-stage workflows** — nurture by lifecycle stage, not just list membership.
- **CRM-driven email** — HubSpot Workflows for B2B nurture (vs Klaviyo for e-com).
- **Revenue attribution joining marketing → deal → closed-won**.

**Do NOT use this skill when:**
- **Pure e-commerce / DTC** lifecycle → use `klaviyo-email-lifecycle` skill.
- **Transactional emails only** → use Resend MCP.
- **Standalone CMS** (Webflow / Framer) — HubSpot CMS only works for the HubSpot landing pages tool.

## Setup

### Auth — OAuth 2.1 + PKCE

```bash
# Step 1: PKCE code challenge
CODE_VERIFIER=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-43)
CODE_CHALLENGE=$(echo -n "$CODE_VERIFIER" | openssl dgst -sha256 -binary | openssl base64 -A | tr -d "=+/" | cut -c1-43)

# Step 2: Open auth URL (one-time per workspace)
open "https://mcp.hubspot.com/oauth/authorize?client_id=craftbot&code_challenge=$CODE_CHALLENGE&code_challenge_method=S256&scope=crm.objects.contacts.read%20crm.objects.contacts.write%20crm.objects.deals.read%20crm.objects.deals.write%20content%20forms%20automation"

# Step 3: Exchange code for token
curl -X POST https://mcp.hubspot.com/oauth/token \
  -d "grant_type=authorization_code&code=<code>&code_verifier=$CODE_VERIFIER&client_id=craftbot"

# Save returned token
export HUBSPOT_MCP_TOKEN="<token>"
export HUBSPOT_PORTAL_ID="<portal-id>"
```

### MCP server connection

```json
{
  "hubspot": {
    "transport": "https",
    "url": "https://mcp.hubspot.com/v1",
    "auth": {"type":"bearer","token":"${HUBSPOT_MCP_TOKEN}"}
  }
}
```

### Tools available (selected)

**CRM (contacts/companies/deals):**
- `list_contacts` / `get_contact` / `create_contact` / `update_contact`
- `update_contact_score` / `merge_contacts`
- `list_deals` / `create_deal` / `update_deal` / `move_deal_stage`
- `list_companies` / `create_company` / `associate_contact_company`
- `search_objects` — generic filter-based search

**Marketing:**
- `create_landing_page` — html + CTA + form_id
- `create_form` — fields + legal basis + submit_action
- `create_workflow` — trigger + enrollment criteria + steps
- `create_email_campaign` — single-send (use Klaviyo for flows in e-com context)
- `create_list` — static or dynamic with filterGroups
- `update_contact_score` — score model id + delta
- `create_sequence` — Sales-Hub-style outbound sequence

**Content:**
- `create_blog_post` / `list_blog_posts`
- `create_cta` / `list_ctas`

## Common recipes

### Recipe 1: Lead capture landing page + form + workflow

```bash
# Step 1: Create form (GDPR-compliant)
form_id=$(mcp tool hubspot.create_form \
  --name "Q3-Lead-Magnet-Form" \
  --fields '[
    {"name":"email","type":"email","required":true,"label":"Work email"},
    {"name":"firstname","type":"text","required":true,"label":"First name"},
    {"name":"company","type":"text","required":false,"label":"Company"},
    {"name":"consent","type":"single_checkbox","required":true,"legalBasis":"CONSENT_WITH_NOTICE","label":"I agree to receive marketing emails"}
  ]' \
  --submitAction "thank-you-page-url" \
  --postSubmitAction '[{"action":"add_to_list","listId":"<welcome-list>"}]')

# Step 2: Create landing page
mcp tool hubspot.create_landing_page \
  --name "Q3-Lead-Magnet-LP" \
  --slug "/lead-magnet-q3" \
  --templateId "<lp-template>" \
  --content '{
    "hero_headline":"Get our 2026 Marketing Playbook",
    "hero_subheadline":"42 pages, free download",
    "hero_image":"https://cdn.brand.com/lp/hero.jpg",
    "form_module":{"formId":"'$form_id'"}
  }' \
  --metaTitle "2026 Marketing Playbook | Brand" \
  --metaDescription "Download our 42-page guide..." \
  --publish true

# Step 3: Workflow — lead magnet delivery + nurture
mcp tool hubspot.create_workflow \
  --name "Lead Magnet — Delivery + Nurture" \
  --enrollmentCriteria '{"type":"list_membership","listId":"<welcome-list>"}' \
  --steps '[
    {"type":"send_email","delay":"0m","emailId":"<deliver-magnet-email>"},
    {"type":"send_email","delay":"3d","emailId":"<nurture-1>"},
    {"type":"send_email","delay":"7d","emailId":"<nurture-2>"},
    {"type":"if_then","condition":{"property":"hs_lead_status","equals":"NEW"},"then":[
      {"type":"send_email","delay":"14d","emailId":"<nurture-3>"}
    ]},
    {"type":"task","delay":"21d","owner":"<sdr-email>","title":"Follow up with high-intent lead"}
  ]'
```

### Recipe 2: Contact scoring model

```bash
# Update score on engagement events
mcp tool hubspot.update_contact_score \
  --contactId "<id>" \
  --scoreModelId "<score-model>" \
  --delta 10 \
  --reason "Downloaded lead magnet"

# Or via workflow on form submit:
mcp tool hubspot.create_workflow \
  --name "Score: Form Submission" \
  --enrollmentCriteria '{"type":"form_submission","formId":"<form>"}' \
  --steps '[{"type":"update_score","scoreModelId":"<model>","delta":15}]'
```

Standard scoring deltas:

| Event | Delta |
|---|---|
| Visited pricing page | +5 |
| Downloaded lead magnet | +10 |
| Watched webinar > 50% | +15 |
| Requested demo | +25 |
| Email open (deprecated by MPP, drop) | 0 |
| Email click | +3 |
| Replied to email | +20 |
| Unsubscribed | -50 |
| Hard bounce | -100 (suppress) |

MQL threshold: 50. SQL threshold: 75.

### Recipe 3: Deal-stage-triggered campaigns

```bash
mcp tool hubspot.create_workflow \
  --name "Post-Demo Follow-up" \
  --enrollmentCriteria '{"type":"deal_property_change","property":"dealstage","newValue":"<demo-completed-stage-id>"}' \
  --steps '[
    {"type":"send_email","delay":"1h","emailId":"<demo-recap-email>"},
    {"type":"send_email","delay":"2d","emailId":"<case-study-email>"},
    {"type":"task","delay":"5d","owner":"deal_owner","title":"Call to follow up on demo"}
  ]'
```

### Recipe 4: Multi-language consent forms

```bash
# Per-language form, post-submit routes to per-language list
for lang in EN BG FR; do
  form_id=$(mcp tool hubspot.create_form \
    --name "Newsletter-$lang" \
    --fields "$(deepl_translate fields.json $lang)" \
    --postSubmitAction "[{\"action\":\"add_to_list\",\"listId\":\"<newsletter-$lang-list>\"}]" \
    --legalBasis "CONSENT_WITH_NOTICE")
  echo "$lang: $form_id"
done
```

### Recipe 5: CRM-ESP sync to Klaviyo

```bash
# HubSpot static list → Klaviyo list via daily export
mcp tool hubspot.export_list \
  --listId "<hs-list>" \
  --format "csv" \
  --destination "s3://bucket/hs-export.csv"

# Then Klaviyo import
mcp tool klaviyo.sync_list \
  --source "s3://bucket/hs-export.csv" \
  --klaviyoListId "<klaviyo-list>"
```

### Recipe 6: Closed-won attribution join (for ROI)

```python
# Pseudo-flow — join HubSpot deals with marketing touchpoints
deals = hubspot.list_deals(filter={'stage':'closedwon','closedate':'>=2026-01-01'})

for deal in deals:
    contact = hubspot.get_contact(deal['primary_contact_id'])
    # First-touch source
    first_touch = contact['properties'].get('hs_analytics_first_referrer')
    # Last-touch
    last_touch = contact['properties'].get('hs_analytics_last_referrer')
    # Touchpoint count
    touches = contact['properties'].get('hs_analytics_num_visits')

    # Join with GA4 campaign data
    ga4_attrib = ga4.run_report(
        filter={'utm_campaign':contact['properties'].get('hs_analytics_first_url_utm_campaign')}
    )

    notion.create_page(db_id=attribution_db, properties={
        'Deal': deal['name'],
        'Amount': deal['amount'],
        'First-Touch Campaign': ga4_attrib['campaign'],
        'Last-Touch Source': last_touch,
        'Touches Before Close': touches,
    })
```

### Recipe 7: Blog post programmatic publishing

```bash
mcp tool hubspot.create_blog_post \
  --name "Title" \
  --slug "/blog/title" \
  --blogId "<blog-id>" \
  --content "$(cat post.html)" \
  --metaTitle "..." \
  --metaDescription "..." \
  --tagIds '["<tag1>","<tag2>"]' \
  --authorId "<author>" \
  --publish true \
  --publishDate "2026-06-15T10:00:00Z"
```

### Recipe 8: CTA management

```bash
# Create reusable CTA
mcp tool hubspot.create_cta \
  --name "Q3-Demo-Request-CTA" \
  --html '<a href="/demo" class="btn">Request Demo</a>' \
  --redirectUrl "/demo?utm_campaign=q3-launch"

# Insert into blog post via merge token
# {{cta:cta_<id>}}
```

## Examples — full B2B funnel

```yaml
# A B2B SaaS funnel built via HubSpot MCP
top_of_funnel:
  - blog posts (SEO traffic) — create_blog_post
  - lead magnets — create_landing_page + create_form
  - newsletter signup — create_form

middle_of_funnel:
  - webinar registration — create_form + create_workflow
  - case study downloads — create_landing_page
  - score: form submission +10, pricing visit +5

bottom_of_funnel:
  - demo request — create_form + assign owner workflow
  - sales sequence — create_sequence (5 emails, 14 days)
  - score: demo request +25

attribution_layer:
  - first-touch + last-touch on contact properties (HS native)
  - join GA4 + HubSpot via UTM in form hidden field
  - Notion dashboard for monthly review
```

## Edge cases

### OAuth scopes
Minimum scopes for marketing-agent:
- `crm.objects.contacts.read`, `crm.objects.contacts.write`
- `crm.objects.deals.read`, `crm.objects.deals.write`
- `crm.lists.read`, `crm.lists.write`
- `content` (blog, pages, CTAs)
- `forms`
- `automation` (workflows + sequences)
- `e-commerce` (if Shopify integration enabled)

### Hub tier requirements
- **Free**: limited to 100 contacts in workflows, no scoring, no AB testing
- **Starter**: 1k workflows, basic scoring
- **Professional**: lead scoring engine, AB testing, custom reporting
- **Enterprise**: AI scoring, predictive lead scoring

Marketing Hub Professional ($800/mo) is the practical minimum for full agent capability.

### GDPR / legal basis on forms
Always set `legalBasis` per field:
- `CONSENT_WITH_NOTICE` — explicit opt-in
- `LEGITIMATE_INTEREST_CLIENT` — existing customer
- `LEGITIMATE_INTEREST_PQL` — product qualified lead
- `LEGITIMATE_INTEREST_OTHER` — other (document reasoning)
- `PERFORMANCE_OF_CONTRACT` — contractual

HubSpot stores legal basis, timestamp, IP automatically.

### Rate limits
- 100 req / 10s per OAuth app
- Daily limit: 250,000 req for Pro / 500,000 for Enterprise
- Bulk endpoints (`batch_create_contacts`, `batch_update_contacts`) consume one call per batch of 100

### Workflow gotchas
- Workflows do NOT re-enroll by default; toggle `allowContactToEnrollMoreThanOnce: true` when needed.
- Suppressed contacts (unsub, bounced) are auto-excluded from email sends.
- Goal-based workflows auto-exit on goal achievement; always set a goal for nurture flows.

### Score model best practices
- Hold one positive + one negative model (engagement vs disqualification)
- Decay: implement quarterly score reset for inactive contacts
- Sales hand-off: MQL → SQL threshold should match SDR capacity (test 50 → 75)

### Landing page templates
HubSpot requires `templateId` of a pre-existing template. The agent should:
1. List templates: `mcp tool hubspot.list_templates --type "landing_page"`
2. Select brand template
3. Use modules array to populate (per template schema)

For custom design, build template in HubSpot Design Manager once, then reuse via MCP.

### B2B email cadence rules
Per role.md email playbook:
- 1 email max per 48h to same contact (cross all workflows)
- Pause all marketing on deal stage = closedwon (transactional only)
- Suppress on hs_email_optout

HubSpot's "email send frequency cap" setting enforces #1 globally.

## Sources

- **HubSpot MCP docs**: https://developers.hubspot.com/mcp
- **OAuth 2.1 + PKCE flow**: https://developers.hubspot.com/docs/api/oauth-quickstart-guide
- **CRM API reference**: https://developers.hubspot.com/docs/api/overview
- **Workflows API**: https://developers.hubspot.com/docs/api/automation/workflows
- **Forms API**: https://developers.hubspot.com/docs/api/marketing/forms
- **GDPR legal basis**: https://knowledge.hubspot.com/account/use-gdpr-features-in-hubspot
