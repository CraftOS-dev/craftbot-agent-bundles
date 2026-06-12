<!--
Source: https://docs.apollo.io/reference/people-search + https://clay.com/docs/api
Apollo + Clay + Lusha + ZoomInfo + Cognism waterfall (June 2026 SOTA).
-->
# Apollo + Clay Lead Enrichment — SKILL

Multi-source waterfall enrichment. Apollo first (270M+ contacts, broadest free-tier data); Clay for orchestrated multi-source fills (Apollo + Hunter + RocketReach + Dropcontact + ZeroBounce); Lusha for mobile phones; ZoomInfo for enterprise gaps; Cognism for EU-compliant data. Every source costs money; the waterfall stops the moment a contact passes the ICP-fit threshold so you don't double-pay for the same record.

## When to use

- **Build / refresh a target-account list** — input a domain set or ICP filter, output enriched contacts with email + phone + role.
- **Fill missing fields on existing CRM contacts** — pull `email IS NULL` or `phone IS NULL` from HubSpot/Salesforce, run through waterfall, write back.
- **Job-change / company-news monitoring** — Apollo's `enrich` + `news` endpoints fire when a champion moves, a new EB joins, or a funding event triggers buyer-readiness.
- **Trigger phrases**: "find emails for these 50 contacts", "enrich this account list", "give me VP Marketing contacts at Series B SaaS in EU", "who's the EB at <company>", "monitor job changes for our champion list".

Do NOT use this skill for: **scraped LinkedIn data alone** (use `linkedin-sales-navigator-outreach`); **B2C consumer records** (Apollo is B2B-only); **EU PII without a legal basis** (Cognism is the only GDPR-clean source — others may violate GDPR for cold outreach).

## Setup

```bash
# Apollo — sign up at apollo.io, generate API key in Settings → Integrations → API
export APOLLO_API_KEY="<key>"
# Free tier: 50 credits/mo + 200 email-finder/mo. Paid: $49/seat starter, $79 pro.

# Clay — sign up at clay.com, generate workspace API key
export CLAY_API_KEY="<key>"
export CLAY_WORKSPACE_ID="<workspace-uuid>"
# Clay pricing: $149/mo Starter (3.4k credits), $349 Pro (10k), $799 Enterprise (50k).

# Lusha — paid only ($29/seat/mo Pro, $51 Premium)
export LUSHA_API_KEY="<key>"

# ZoomInfo + Cognism — enterprise contracts, OAuth-only; route via api-gateway when onboarded
export MATON_API_KEY="<maton-key>"   # for managed OAuth to ZoomInfo + Cognism

# Optional: Hunter for email verification (free 25/mo, $34/mo Starter)
export HUNTER_API_KEY="<key>"
```

Free-vs-paid quick map:
- **Apollo**: 50 credits/mo on free; serious work needs $49+.
- **Clay**: no free tier; 7-day trial.
- **Lusha**: 5 free phone credits to test; production = paid.
- **ZoomInfo**: enterprise sales required; ~$15-30k/yr starter.
- **Cognism**: similar enterprise pricing; GDPR-clean differentiator.

## Common recipes

### Recipe 1: Apollo people search (ICP filter → contacts)

```bash
curl -X POST "https://api.apollo.io/api/v1/mixed_people/search" \
  -H "Cache-Control: no-cache" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $APOLLO_API_KEY" \
  -d '{
    "person_titles":["VP Marketing","Head of Marketing","Director of Marketing"],
    "person_seniorities":["vp","director","head"],
    "organization_num_employees_ranges":["51,200","201,500"],
    "organization_locations":["United States","United Kingdom"],
    "person_functions":["marketing"],
    "page":1,
    "per_page":25
  }'
```

Returns `people[]` with `id`, `name`, `title`, `email_status` (`verified` / `guessed` / `unavailable`), `organization`. Always check `email_status` before sending — guessed emails bounce at 15-30%.

### Recipe 2: Apollo organization enrich (one domain → company record)

```bash
curl -X GET "https://api.apollo.io/api/v1/organizations/enrich?domain=acme.com" \
  -H "X-Api-Key: $APOLLO_API_KEY"
```

Returns: `industry`, `estimated_num_employees`, `annual_revenue_printed`, `technologies[]` (tech-stack from BuiltWith), `latest_funding_stage`, `latest_funding_round_date`, `current_news` (last 30 days).

### Recipe 3: Apollo people enrich (bulk match by name + company)

```bash
curl -X POST "https://api.apollo.io/api/v1/people/bulk_match" \
  -H "X-Api-Key: $APOLLO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "reveal_personal_emails":false,
    "reveal_phone_number":false,
    "details":[
      {"first_name":"Sam","last_name":"Lee","domain":"acme.com"},
      {"first_name":"Pat","last_name":"Cruz","domain":"globex.io"}
    ]
  }'
```

Up to 10 records per call. Costs 1 credit per match; phone reveal is +1 credit.

### Recipe 4: Clay workflow trigger (waterfall enrichment)

```bash
# Trigger a pre-built Clay table that runs Apollo → Hunter → Dropcontact in waterfall
curl -X POST "https://api.clay.com/v3/workspaces/$CLAY_WORKSPACE_ID/tables/<table-id>/rows" \
  -H "Authorization: Bearer $CLAY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "rows":[
      {"first_name":"Sam","last_name":"Lee","linkedin_url":"https://linkedin.com/in/samlee","company_domain":"acme.com"},
      {"first_name":"Pat","last_name":"Cruz","linkedin_url":"https://linkedin.com/in/patcruz","company_domain":"globex.io"}
    ],
    "webhook_on_complete":"https://your-app.com/webhook/clay-done"
  }'
```

Clay tables consume credits per cell. A typical email-find waterfall (Apollo + Hunter + Dropcontact + ZeroBounce verify) is ~4-5 credits per row.

### Recipe 5: Lusha phone reveal

```bash
curl -X GET "https://api.lusha.com/person?firstName=Sam&lastName=Lee&companyDomain=acme.com" \
  -H "api_key: $LUSHA_API_KEY"
```

Returns `mobile_phone`, `direct_phone`, `email`. 1 credit per match; mobile reveal costs an extra credit on most plans.

### Recipe 6: Hunter email verification (catch-all check)

```bash
curl -X GET "https://api.hunter.io/v2/email-verifier?email=sam@acme.com&api_key=$HUNTER_API_KEY"
```

Returns `result`: `deliverable` / `risky` / `undeliverable`. Skip anything but `deliverable` for cold outbound.

### Recipe 7: Apollo "company news" (trigger event mining)

```bash
curl -X POST "https://api.apollo.io/api/v1/organizations/enrich" \
  -H "X-Api-Key: $APOLLO_API_KEY" -H "Content-Type: application/json" \
  -d '{"domain":"acme.com"}' | jq '.organization.current_news[] | select(.date > "2026-04-01")'
```

Surfaces funding events, leadership changes, product launches in the last 30-90 days.

### Recipe 8: Apollo job-change webhook (champion-mover alert)

```bash
# One-time setup: register webhook for job-change events on a saved-search ID
curl -X POST "https://api.apollo.io/api/v1/webhooks" \
  -H "X-Api-Key: $APOLLO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "webhook_url":"https://your-app.com/webhook/apollo-jobchange",
    "trigger":"person_job_changed",
    "saved_search_id":"<champion-list-saved-search>"
  }'
```

Apollo posts `{"person":{...},"old_organization":{...},"new_organization":{...}}` when a tracked person changes jobs. Pair with `hubspot-sales-mcp` recipe 4 to auto-create a "champion-mover" task.

### Recipe 9: Cognism EU-compliant search (via api-gateway)

```bash
curl -X POST "https://gateway.maton.ai/cognism/v2/search/contacts" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "filters":{"countries":["DE","FR","NL"],"titles":["CMO"],"company_size":["51-200"]},
    "limit":100
  }'
```

Cognism flags every record's legal basis (legitimate-interest vs consent) so you can demonstrate GDPR compliance to a DPA audit.

### Recipe 10: Full waterfall in Python (Apollo → Clay fallback → Lusha)

```python
import os, requests, time

def enrich_contact(first, last, domain):
    headers_a = {"X-Api-Key": os.environ["APOLLO_API_KEY"]}
    r = requests.post(
        "https://api.apollo.io/api/v1/people/match",
        headers=headers_a,
        json={"first_name":first,"last_name":last,"domain":domain,"reveal_personal_emails":False},
    )
    p = r.json().get("person") or {}
    email = p.get("email") if p.get("email_status") == "verified" else None
    phone = None

    if not email:
        # Clay fallback
        cl = requests.post(
            f"https://api.clay.com/v3/workspaces/{os.environ['CLAY_WORKSPACE_ID']}/tables/<table>/rows",
            headers={"Authorization": f"Bearer {os.environ['CLAY_API_KEY']}"},
            json={"rows":[{"first_name":first,"last_name":last,"company_domain":domain}]},
        )
        # Clay is async — poll or use webhook

    if not phone:
        lh = requests.get(
            f"https://api.lusha.com/person?firstName={first}&lastName={last}&companyDomain={domain}",
            headers={"api_key": os.environ["LUSHA_API_KEY"]},
        )
        if lh.ok:
            phone = (lh.json().get("data") or {}).get("mobilePhone")

    return {"email": email, "phone": phone}
```

## Examples

### Example 1: Build a 200-account target list with verified emails

**Goal:** Identify 200 EU Series B SaaS companies, 2-4 contacts each (CMO, Head of Demand, VP Sales).

**Steps:**
1. Apollo `mixed_people/search` filtered by `organization_num_employees_ranges=["51,200"]`, `organization_locations=["European Union"]`, `organization_keyword_tags=["saas"]`, `person_titles=[...]`, `per_page=25`, paginated to 600+ candidates (Recipe 1).
2. For each candidate with `email_status != "verified"`, Clay waterfall fallback (Recipe 4) → output `verified_email`.
3. For each verified contact, Hunter `email-verifier` to confirm deliverability (Recipe 6); drop `risky` + `undeliverable`.
4. Write to HubSpot via `hubspot-sales-mcp` recipe 3 (batch upsert contacts, set `lifecyclestage=lead`, `lead_source=Apollo Q3 ICP`).

**Result:** ~480 deliverable contacts at 200 accounts ready for outbound. Cost estimate: ~$60 (Apollo) + ~$15 (Clay) + $0 (Hunter free tier covers 25/mo, paid for the rest).

### Example 2: Daily champion-mover alert

**Goal:** When any contact tagged "champion" changes jobs, auto-create a "re-engage at new company" task.

**Steps:**
1. Build Apollo saved-search of all champion contacts. Register `person_job_changed` webhook (Recipe 8).
2. Webhook receiver creates a new HubSpot contact at the *new* company (Recipe 3 in `hubspot-sales-mcp`), copies old champion data, sets `lead_source="champion-mover-alert"`.
3. Creates a HubSpot task on the AE: "Champion moved from <oldco> to <newco> — book a re-engage call within 7 days".
4. Slack DM via `slack-mcp` to the AE who owned the old champion.

**Result:** Zero manual monitoring; champion-movers surface within 24-48h of LinkedIn updating.

## Edge cases / gotchas

- **Apollo email_status: "guessed" bounces at 15-30%.** Only trust `verified`. For `guessed`, route through Hunter `email-verifier` (Recipe 6) before sending.
- **Credit accounting is opaque** — Apollo charges a credit on every reveal (email, phone, mobile), and a `reveal_personal_emails: true` API call can drain a free plan in one batch. Always pass `reveal_personal_emails: false` unless you've budgeted it.
- **Clay's free trial caps at 100 credits** and locks tables after expiry. Don't build a production workflow on the trial.
- **Lusha mobile-phone reveal is regional** — strong in US/UK, weak in EU/APAC. For EU mobile, ZoomInfo is more reliable; for APAC, Cognism > both.
- **ZoomInfo's "Engage" product (sequences) is a separate SKU** from data; data-only contracts exist but require negotiation.
- **GDPR risk on cold outreach to EU contacts** — only Cognism warrants legitimate-interest basis. Apollo, Clay, Lusha data on EU PII is *not* automatically GDPR-clean. Document your legal basis in writing per contact, or stick to opted-in lists.
- **Apollo's `current_news` is sparse for SMB** — surfaces well for >$10M revenue, hit-or-miss below. Pair with `brave-search` + Crunchbase for SMB triggers.
- **Rate limits**: Apollo 100 req/min on paid; Clay 60 req/min; Lusha 30 req/min; Hunter 600 req/min. For bulk runs, batch and add `time.sleep(1)` between calls.
- **Webhook reliability**: Apollo + Clay both occasionally drop webhook deliveries. Implement an idempotent receiver + a nightly reconciliation query that compares webhook-received vs API-listed records.
- **Don't double-enrich**: dedupe by `email_lowercase` before each enrichment call. Re-enriching a record you already enriched today re-charges credits.

## Sources

- Apollo.io API reference: https://docs.apollo.io/reference/people-search
- Apollo organization endpoints: https://docs.apollo.io/reference/organizations-search
- Clay API docs: https://clay.com/docs/api
- Lusha API: https://www.lusha.com/business/api/
- Hunter email verifier API: https://hunter.io/api-documentation/v2#email-verifier
- Cognism for GDPR-clean B2B data (2026 review): https://www.cognism.com/blog/gdpr-compliant-b2b-data
- 2026 sales enrichment tool comparison (Clay vs Apollo vs ZoomInfo): https://clay.com/blog/sales-enrichment-tools-2026
