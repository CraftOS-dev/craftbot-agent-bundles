<!--
Source: https://docs.apollo.io/reference/people-search + https://api-docs.zoominfo.com/ + https://clay.com/docs/api
Data enrichment waterfall — ZoomInfo + Apollo + Clay + Demandbase (June 2026 SOTA).
-->
# Data Enrichment Waterfall — ZoomInfo + Apollo + Clay + Demandbase — SKILL

Trigger-based enrichment waterfalled across multiple sources. **Apollo** for cost-efficient B2B baseline (~$0.10/match). **ZoomInfo** for gaps + Scoops intent (~$0.50/match). **Clay** for workflow orchestration across 100+ sources (~$0.30/match). **Demandbase** for ABM intent overlay (subscription). Spend cap + field-write priority rules.

## When to use

- **Set up enrichment waterfall** — on lead create / on stage change → enrich.
- **One-off enrichment batch** — fill gaps on existing records.
- **ABM intent tracking** — enrich tier-1 accounts with surge data.
- **Cost optimization** — Apollo first, ZoomInfo only if Apollo missed.
- **Field-write priority** — when sources disagree, who wins?
- **Trigger phrases**: "enrich leads", "Apollo + ZoomInfo waterfall", "Clay workflow", "Scoops intent", "Demandbase signals", "enrichment cost cap".

Do NOT use this skill for: **routing** (use `lead-routing-leandata-chili-piper`); **dedup** (use `duplicate-mgmt-leandata-dedupe`); **account hierarchy** (use `contact-account-hierarchy-maintenance`); **direct outreach** (use `apollo-clay-lead-enrichment` parent sales-agent skill — that one is for outreach, not infrastructure).

## Setup

```bash
# Apollo — API token
export APOLLO_API_KEY="<key>"

# ZoomInfo — OAuth client credentials
export ZI_CLIENT_ID="<id>"
export ZI_CLIENT_SECRET="<secret>"
# Fetch token (lasts 1 hour)
export ZI_TOKEN=$(curl -s -X POST "https://api.zoominfo.com/authorize" \
  -d '{"client_id":"'$ZI_CLIENT_ID'","client_secret":"'$ZI_CLIENT_SECRET'"}' | jq -r .jwt)

# Clay — API key (Settings → Workspace → API)
export CLAY_API_KEY="<key>"

# Demandbase — API key (Settings → Integrations → API)
export DEMANDBASE_API_KEY="<key>"

# Or via api-gateway
export MATON_API_KEY="<key>"

# Spend tracking
export ENRICHMENT_BUDGET_DB="postgresql://..."
```

Required:
- Apollo: paid plan with API access (~$200+/mo)
- ZoomInfo: enterprise plan with API (~$15K+/yr)
- Clay: paid (~$150-1000/mo by usage)
- Demandbase: enterprise ABM platform (~$25K+/yr)

## Common recipes

### Recipe 1: Waterfall priority + cost order

```yaml
# Canonical waterfall config — cheapest first, most authoritative last
trigger: lead_created OR (deal_stage_change AND from='Prospect')

step_1_apollo:
  endpoint: POST /apollo/api/v1/people/match
  cost_estimate_usd: 0.10
  fields_written: title, seniority, function, employees, industry
  fallback_if_not_found: continue_to_step_2

step_2_zoominfo:
  endpoint: POST /zoominfo/persons/enrich
  cost_estimate_usd: 0.50
  fields_written: mobile_phone, direct_phone, scoops_intent_topics
  conditional: apollo_returned_partial OR account_tam > 500000
  fallback_if_not_found: continue_to_step_3

step_3_clay:
  endpoint: POST /clay/workflows/<workflow_id>/trigger
  cost_estimate_usd: 0.30
  sources_tried: Hunter, RocketReach, Dropcontact, AeroLeads
  conditional: apollo_AND_zi_both_missed

step_4_demandbase:
  endpoint: POST /demandbase/account-intent
  cost_estimate_usd: 0  # subscription, no per-record
  fields_written: intent_topics, surge_score, buying_stage
  conditional: abm_tier in [1, 2]

spend_cap_per_record_usd: 5.00
field_write_priority:
  phone: zoominfo > apollo > clay
  email: clay > apollo > zoominfo
  industry: zoominfo > apollo
  intent: demandbase > zoominfo_scoops
```

### Recipe 2: Apollo person match

```bash
curl -X POST "https://api.apollo.io/v1/people/match" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "'$APOLLO_API_KEY'",
    "email": "alice@acme.com",
    "first_name": "Alice",
    "last_name": "Smith",
    "organization_name": "Acme Corp",
    "reveal_personal_emails": false,
    "reveal_phone_number": true
  }'

# Response includes: person.title, person.seniority, person.organization.industry,
# person.organization.estimated_num_employees, person.linkedin_url, person.phone_numbers[]
```

### Recipe 3: ZoomInfo person enrich

```bash
# ZoomInfo wants matching identifiers; emails + names + company
curl -X POST "https://api.zoominfo.com/enrich/contact" \
  -H "Authorization: Bearer $ZI_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "matchPersonInput": [{
      "personId": null,
      "firstName": "Alice",
      "lastName": "Smith",
      "emailAddress": "alice@acme.com",
      "companyName": "Acme Corp"
    }],
    "outputFields": ["id","firstName","lastName","email","phone","mobilePhone","jobTitle",
                     "managementLevel","department","company.name","company.industry",
                     "company.intent","company.employeeCount"]
  }'
```

### Recipe 4: Clay workflow trigger

```bash
# Clay workflows are user-defined in the Clay UI; trigger via webhook
curl -X POST "https://api.clay.com/v3/workflows/wf_xyz789/trigger" \
  -H "Authorization: Bearer $CLAY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "email": "alice@acme.com",
      "first_name": "Alice",
      "last_name": "Smith",
      "company": "Acme Corp",
      "domain": "acme.com"
    },
    "async": true,
    "callback_url": "https://your-system/webhook/clay-result"
  }'
```

### Recipe 5: Demandbase account intent

```bash
curl "https://api.demandbase.com/v2/account/intent?domain=acme.com" \
  -H "X-API-Key: $DEMANDBASE_API_KEY" \
  | jq '{domain, surge_score, top_intent_topics: .intent_topics[:5], buying_stage}'
```

### Recipe 6: Waterfall orchestration (Python)

```python
import requests, os, time

CONFIG = {
    "spend_cap_per_record": 5.00,
    "apollo_cost": 0.10,
    "zi_cost": 0.50,
    "clay_cost": 0.30
}

def enrich(lead):
    spent = 0.0
    result = {}

    # Step 1 — Apollo
    if spent + CONFIG["apollo_cost"] <= CONFIG["spend_cap_per_record"]:
        ar = requests.post("https://api.apollo.io/v1/people/match",
                           json={"api_key": os.environ["APOLLO_API_KEY"],
                                 "email": lead["email"],
                                 "first_name": lead["first_name"],
                                 "last_name": lead["last_name"],
                                 "organization_name": lead["company"]}).json()
        spent += CONFIG["apollo_cost"]
        if ar.get("person"):
            p = ar["person"]
            result.update({"title": p.get("title"),
                           "seniority": p.get("seniority"),
                           "industry": (p.get("organization") or {}).get("industry"),
                           "employees": (p.get("organization") or {}).get("estimated_num_employees"),
                           "linkedin": p.get("linkedin_url")})

    # Step 2 — ZoomInfo if missing phone or high-TAM
    missing_phone = not result.get("phone")
    high_tam = lead.get("account_tam_usd", 0) > 500000
    if (missing_phone or high_tam) and spent + CONFIG["zi_cost"] <= CONFIG["spend_cap_per_record"]:
        zir = requests.post("https://api.zoominfo.com/enrich/contact",
                            headers={"Authorization": f"Bearer {os.environ['ZI_TOKEN']}"},
                            json={"matchPersonInput": [{"firstName": lead["first_name"],
                                                        "lastName": lead["last_name"],
                                                        "emailAddress": lead["email"],
                                                        "companyName": lead["company"]}],
                                  "outputFields": ["mobilePhone","phone","company.intent"]}).json()
        spent += CONFIG["zi_cost"]
        if zir.get("data"):
            d = zir["data"][0]
            result.setdefault("phone", d.get("mobilePhone") or d.get("phone"))
            result["intent"] = (d.get("company") or {}).get("intent")

    # Step 3 — Clay if both missed
    if not result.get("phone") and not result.get("title") and \
       spent + CONFIG["clay_cost"] <= CONFIG["spend_cap_per_record"]:
        cr = requests.post("https://api.clay.com/v3/workflows/wf_xyz789/trigger",
                           headers={"Authorization": f"Bearer {os.environ['CLAY_API_KEY']}"},
                           json={"data": lead}).json()
        spent += CONFIG["clay_cost"]
        # Clay returns async; webhook callback completes the loop

    # Step 4 — Demandbase intent (always free if tier 1)
    if lead.get("abm_tier") in [1, 2]:
        dbr = requests.get(f"https://api.demandbase.com/v2/account/intent?domain={lead['domain']}",
                           headers={"X-API-Key": os.environ["DEMANDBASE_API_KEY"]}).json()
        result["abm_intent_topics"] = dbr.get("intent_topics", [])[:5]
        result["abm_surge_score"] = dbr.get("surge_score")

    result["_enrichment_cost"] = spent
    return result

# Log spend per record for budget tracking
```

### Recipe 7: Spend tracking ledger (postgres)

```sql
CREATE TABLE enrichment_spend (
    id SERIAL PRIMARY KEY,
    enriched_at TIMESTAMP DEFAULT NOW(),
    record_id TEXT,
    record_type TEXT,  -- lead, contact, account
    source TEXT,       -- apollo, zoominfo, clay, demandbase
    cost_usd NUMERIC(6,2),
    fields_returned JSONB,
    spent_cumulative_usd NUMERIC(8,2)
);

-- Per-month budget check
SELECT
  DATE_TRUNC('month', enriched_at) AS month,
  source,
  COUNT(*) AS calls,
  SUM(cost_usd) AS total_cost,
  AVG(cost_usd) AS avg_cost_per_record
FROM enrichment_spend
WHERE enriched_at >= DATE_TRUNC('month', NOW()) - INTERVAL '3 months'
GROUP BY 1, 2
ORDER BY 1 DESC, 4 DESC;
```

### Recipe 8: Field-write priority resolution

```python
# When ZoomInfo says industry='Software', Apollo says 'Information Technology'
# Apply priority rules

PRIORITY = {
    "phone":    ["zoominfo", "apollo", "clay"],
    "email":    ["clay", "apollo", "zoominfo"],
    "industry": ["zoominfo", "apollo"],
    "intent":   ["demandbase", "zoominfo_scoops"],
    "title":    ["zoominfo", "apollo"]
}

def resolve(field_values):
    """
    field_values: dict like {"phone": {"apollo": "555-1234", "zoominfo": "(555) 123-4567"}}
    Returns highest-priority source's value.
    """
    resolved = {}
    for field, by_source in field_values.items():
        for source in PRIORITY.get(field, ["apollo","zoominfo","clay"]):
            if by_source.get(source):
                resolved[field] = by_source[source]
                resolved[f"{field}_source"] = source
                break
    return resolved
```

### Recipe 9: Trigger from Salesforce flow (Apex callout)

```apex
// LeadEnrichmentService.cls — invoked from record-triggered flow on Lead create
public with sharing class LeadEnrichmentService {
    @InvocableMethod(label='Enrich Lead via Waterfall')
    public static void enrichBatch(List<Id> leadIds) {
        for (Id leadId : leadIds) {
            // Call api-gateway proxy that runs the Python waterfall
            HttpRequest req = new HttpRequest();
            req.setEndpoint('https://gateway.maton.ai/enrichment/waterfall');
            req.setMethod('POST');
            req.setHeader('Authorization', 'Bearer ' + Maton__c.getInstance().API_Key__c);
            req.setBody(JSON.serialize(new Map<String,Object>{'lead_id' => leadId}));
            Http h = new Http();
            HttpResponse res = h.send(req);
            // Async; the gateway writes results back via Salesforce REST
        }
    }
}
```

### Recipe 10: Trigger from HubSpot workflow

```javascript
// HubSpot custom-coded action — calls waterfall
exports.main = async (event, callback) => {
  const { email, firstName, lastName, company, domain } = event.inputFields;
  const r = await axios.post("https://gateway.maton.ai/enrichment/waterfall",
    { email, first_name: firstName, last_name: lastName, company, domain },
    { headers: { Authorization: `Bearer ${process.env.MATON_KEY}` } });

  callback({
    outputFields: {
      title: r.data.title || '',
      industry: r.data.industry || '',
      phone: r.data.phone || '',
      intent_topics: (r.data.abm_intent_topics || []).join(',')
    }
  });
};
```

### Recipe 11: ZoomInfo Scoops intent batch query

```bash
# Pull intent signals for all enterprise accounts (B2B account intent)
curl -X POST "https://api.zoominfo.com/intent/topics/companies" \
  -H "Authorization: Bearer $ZI_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "companyIds": [12345, 67890, 11111],
    "fromDate": "2026-06-01",
    "toDate": "2026-06-11",
    "topics": ["CRM Implementation", "Sales Operations Tool"]
  }'
```

### Recipe 12: Budget alert (monthly check)

```python
# Monthly: if spend > 80% of monthly budget, Slack alert
import requests, os, psycopg
from datetime import date

MONTHLY_BUDGET_USD = 5000

conn = psycopg.connect(os.environ['ENRICHMENT_BUDGET_DB'])
cur = conn.cursor()
cur.execute("""
  SELECT SUM(cost_usd) FROM enrichment_spend
  WHERE enriched_at >= DATE_TRUNC('month', NOW())
""")
spent = float(cur.fetchone()[0] or 0)
pct = 100 * spent / MONTHLY_BUDGET_USD

if pct > 80:
    requests.post("https://slack.com/api/chat.postMessage",
                  headers={"Authorization": f"Bearer {os.environ['SLACK_TOKEN']}"},
                  json={"channel": "#sales-ops",
                        "text": f":warning: Enrichment spend at {pct:.0f}% of ${MONTHLY_BUDGET_USD} monthly budget. Spent so far: ${spent:.0f}"})
```

## Examples

### Example 1: New-lead enrichment waterfall

**Goal:** Every new lead enriched within 60 seconds, ≤ $0.50 per record.

**Steps:**
1. Recipe 9 (Salesforce) or Recipe 10 (HubSpot) — trigger on lead create.
2. Recipe 6 — waterfall runs: Apollo first (~$0.10), then ZoomInfo if needed (~$0.50), then Clay if both miss.
3. Recipe 8 — resolve conflicts using priority rules.
4. Write enriched fields back to lead.
5. Recipe 7 — log spend; Recipe 12 — monthly budget watch.

**Result:** 90%+ of leads have title + industry + employees within minutes; SDR research time drops 60%.

### Example 2: Tier-1 account intent monitoring

**Goal:** Top 100 ABM accounts get daily intent + surge score from Demandbase + ZoomInfo Scoops.

**Steps:**
1. Tag accounts with `ABM_Tier__c = '1'` in Salesforce (~100 accounts).
2. Daily cron triggers Recipe 5 (Demandbase) + Recipe 11 (ZoomInfo Scoops) for each.
3. Write `intent_topics` + `surge_score` back to Account record.
4. Auto-create a Salesforce Task for the account owner when surge_score jumps > 30 points.
5. Display in CRMA dashboard "ABM Tier 1 — Active Buyers."

**Result:** Account owners alerted to active research within 24h; outbound timing improves.

### Example 3: Gaps backfill batch

**Goal:** 12K existing leads with missing phone or title — fill in one batch.

**Steps:**
1. Pull leads missing phone OR title from Salesforce (Bulk API export).
2. Chunk to 200/run; Recipe 6 over each chunk.
3. Skip Demandbase step (overkill for old leads).
4. Spend cap: $0.50/record total → ~$6K for 12K records.
5. Recipe 8 — write results back via Composite API to Salesforce.
6. Compare pre/post coverage: title 30% → 92%, phone 12% → 78%.

**Result:** Lead records usable for outbound + segmentation; SDR pipeline-gen lifts.

## Edge cases / gotchas

- **Apollo's `person` vs `bulk_match`** — single uses `/people/match`; bulk: `/people/bulk_match` (up to 10 per call). Use bulk for batches.
- **Apollo reveal_phone returns empty if no quota** — paid plans have phone reveal quota.
- **ZoomInfo OAuth token expires hourly** — refresh + cache. Don't re-auth per call.
- **ZoomInfo Match Scores** — return a `matchScore`; below 80 = unreliable. Always check.
- **Clay workflow async** — callback URL pattern; don't wait synchronously.
- **Demandbase intent topics are taxonomized** — use their `/v2/intent/topics` list to filter.
- **Field-write conflicts** — silent overwrites are insidious. Always log `_source` field next to data.
- **Email reveal cost** — Apollo: free in match response. ZoomInfo: tiered. Clay: per-source.
- **GDPR EMEA blocks** — ZoomInfo + Apollo limit EU/EMEA contact details. Use Cognism or Dropcontact for EMEA enrichment.
- **Cost stacking** — running waterfall + retries → 2× cost. Idempotency keys on record updates.
- **Rate limits** — Apollo: 60 req/min on paid. ZoomInfo: 5K req/day standard. Clay: workflow-defined. Demandbase: low (consult).
- **Stale enrichment** — refresh quarterly; people change jobs. Cache field `last_enriched_at`; re-enrich > 180d old.
- **API key rotation** — Apollo + ZoomInfo: 90-day rotation policy.
- **Webhook reliability** — Clay async callbacks can drop. Have a polling fallback.
- **PII compliance** — enriched mobile phones can be PII; log access; honor opt-outs.
- **Industry taxonomy mismatch** — Apollo uses NAICS-ish; ZoomInfo uses SIC; Demandbase has own. Pick one canonical.

## Sources

- [Apollo.io API — People Search](https://docs.apollo.io/reference/people-search)
- [Apollo.io API — People Match](https://docs.apollo.io/reference/people-match)
- [ZoomInfo Enrich API](https://api-docs.zoominfo.com/#enrich-contact)
- [ZoomInfo Intent + Scoops API](https://api-docs.zoominfo.com/#intent)
- [Clay API docs](https://clay.com/docs/api)
- [Demandbase Intent API](https://docs.demandbase.com/intent/)
- [Enrichment waterfall best practices (Common Room)](https://www.commonroom.io/blog/enrichment-waterfall/)
- [B2B data quality cost benchmarks (Dreamdata 2026)](https://dreamdata.io/blog/data-quality-2026)
