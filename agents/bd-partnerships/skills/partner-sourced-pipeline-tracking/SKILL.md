<!--
Source: https://www.partnerstack.com/blog/partner-attribution + https://www.crossbeam.com/blog/attribution/ + https://developers.hubspot.com/docs/api/crm/deals + https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/
Partner-sourced pipeline attribution + weekly rollup (June 2026 SOTA).
-->
# Partner-Sourced Pipeline Tracking — SKILL

Tag every opportunity with `source = Partner` + `partner_id` in CRM; roll up pipeline weekly by partner; surface direct-vs-partner split to sales-agent + leadership; alert on stale or mis-attributed deals. Drives commission accuracy, scorecards, tier eligibility, and partner-program ROI math.

## When to use

- **CRM source-field design** — adding `Source` + `Partner_ID` fields and validation rules.
- **Weekly partner pipeline rollup** — Monday digest to partner managers + #partner-pipeline Slack.
- **Direct-vs-partner split** for leadership / board reporting.
- **Attribution audit** — confirming partner_id matches deal source narrative.
- **Stale partner deal alerts** — partner-sourced deal not touched in 14 days.
- **Re-attribution disputes** — partner-A vs partner-B touched same deal.
- **Feeds scorecard + commission** — input to `partner-scorecard-authoring` + `partnerstack-tackle-channel-management`.
- **Trigger phrases**: "partner pipeline this quarter", "partner-attributed revenue", "direct vs partner split", "weekly partner rollup", "who sourced this deal".

Do NOT use this skill for: **commission posting** (use `partnerstack-tackle-channel-management`); **partner agreement attribution clauses** (use `referral-affiliate-channel-oem-agreement-structuring`); **deal-reg conflict resolution** (use `deal-registration-channel-conflict-resolution`); **scorecard rendering** (use `partner-scorecard-authoring`).

## Setup

```bash
export MATON_API_KEY="<key>"
export HUBSPOT_PRIVATE_APP_TOKEN="<token>"     # if direct, not via Maton
export SALESFORCE_INSTANCE_URL="<url>"
export SALESFORCE_ACCESS_TOKEN="<token>"
export WAREHOUSE_CONN_STR="postgres://..."     # Postgres / Snowflake / BigQuery via postgresql-mcp
export PARTNERSTACK_API_KEY="<key>"
export SLACK_BOT_TOKEN="<token>"                # for #partner-pipeline alerts
```

**One-time CRM schema setup** (do once per CRM instance):
- HubSpot deal property `hs_lead_source_partner_id` (single-line) + `hs_lead_source` enum including `Partner`
- Salesforce Opportunity custom field `Partner_ID__c` (Lookup → Account where Type='Partner') + `LeadSource` picklist including `Partner`
- Validation rule: if `LeadSource = Partner` then `Partner_ID__c` REQUIRED

## Common recipes

### Recipe 1: HubSpot — tag deal as partner-sourced

```bash
curl -X PATCH "https://gateway.maton.ai/hubspot/crm/v3/objects/deals/<dealId>" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "hs_lead_source": "Partner",
      "hs_lead_source_partner_id": "acme-001",
      "partner_attribution_model": "last_touch",
      "partner_first_touch_date": "2026-05-12",
      "partner_last_touch_date": "2026-06-03"
    }
  }'
```

Reference: https://developers.hubspot.com/docs/api/crm/deals.

### Recipe 2: Salesforce — tag opportunity as partner-sourced

```bash
curl -X PATCH "$SALESFORCE_INSTANCE_URL/services/data/v60.0/sobjects/Opportunity/<oppId>" \
  -H "Authorization: Bearer $SALESFORCE_ACCESS_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "LeadSource":"Partner",
    "Partner_ID__c":"a0xxxxxxx",
    "Attribution_Model__c":"Last Touch",
    "Partner_First_Touch__c":"2026-05-12",
    "Partner_Last_Touch__c":"2026-06-03"
  }'
```

Reference: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/.

### Recipe 3: Weekly partner pipeline rollup (warehouse SQL)

```sql
-- Run weekly Monday 7am via postgresql-mcp cron
SELECT
  partner_id,
  partner_name,
  COUNT(*)                                                           AS opps_open,
  COUNT(*) FILTER (WHERE stage = 'Closed Won')                       AS closed_won,
  COUNT(*) FILTER (WHERE stage = 'Closed Lost')                      AS closed_lost,
  SUM(amount) FILTER (WHERE stage NOT IN ('Closed Won','Closed Lost')) AS pipeline_open,
  SUM(amount) FILTER (WHERE stage = 'Closed Won')                    AS revenue_won,
  ROUND(
    COUNT(*) FILTER (WHERE stage='Closed Won')::numeric /
    NULLIF(COUNT(*) FILTER (WHERE stage IN ('Closed Won','Closed Lost')), 0),
    3
  ) AS win_rate,
  MAX(last_activity_at)                                              AS last_touched_at
FROM opportunities
WHERE source = 'Partner'
  AND created_at >= DATE_TRUNC('quarter', NOW())
GROUP BY partner_id, partner_name
ORDER BY pipeline_open DESC;
```

Render to `google-sheets` via `gspread` insert.

### Recipe 4: Direct vs Partner split (leadership view)

```sql
SELECT
  DATE_TRUNC('week', created_at)                                  AS week,
  CASE WHEN source='Partner' THEN 'Partner' ELSE 'Direct' END     AS channel,
  COUNT(*)                                                        AS new_opps,
  SUM(amount)                                                     AS pipeline_added,
  SUM(amount) FILTER (WHERE stage='Closed Won')                   AS revenue_won
FROM opportunities
WHERE created_at >= NOW() - INTERVAL '13 weeks'
GROUP BY 1, 2
ORDER BY 1 DESC, 2;
```

Drives quarterly direct-vs-partner share-of-pipeline chart for board deck.

### Recipe 5: Stale partner-deal alert

```sql
-- Partner-sourced deals with no activity in 14 days
SELECT o.id, o.name, o.partner_id, o.amount, o.stage, o.last_activity_at,
       p.partner_name, p.channel_manager_email
FROM opportunities o
JOIN partners p USING (partner_id)
WHERE o.source='Partner'
  AND o.stage NOT IN ('Closed Won','Closed Lost')
  AND o.last_activity_at < NOW() - INTERVAL '14 days'
ORDER BY o.amount DESC;
```

Pipe to `slack-mcp` `chat.postMessage` `#partner-pipeline` with @-mention of channel manager.

### Recipe 6: Slack weekly digest

```python
def post_weekly_partner_digest():
    rows = run_warehouse_query(WEEKLY_ROLLUP_SQL)
    blocks = [{"type":"header","text":{"type":"plain_text","text":f"Partner Pipeline — Week of {monday().isoformat()}"}}]
    for r in rows[:10]:
        blocks.append({
            "type":"section",
            "text":{
                "type":"mrkdwn",
                "text":(
                    f"*{r['partner_name']}* — open ${r['pipeline_open']:,.0f} "
                    f"| won ${r['revenue_won']:,.0f} | win-rate {r['win_rate']:.0%} "
                    f"| last touch {humanize(r['last_touched_at'])}"
                )
            }
        })
    slack_chat_post("#partner-pipeline", blocks=blocks)
```

Run via `postgresql-mcp` cron Monday 7am + `slack-mcp` `chat.postMessage`.

### Recipe 7: Auto-tag from Partnerstack lead-submitted webhook

```python
def on_partnerstack_lead_submitted(event):
    # event = {"lead_id","partner_id","email","company","first_name","last_name"}
    deal = create_hubspot_deal(
        name=f"{event['company']} — partner-sourced",
        amount=None,
        stage="qualified-to-buy",
        properties={
            "hs_lead_source":"Partner",
            "hs_lead_source_partner_id": event["partner_id"],
            "partner_first_touch_date": today(),
            "partnerstack_lead_id": event["lead_id"],
        },
    )
    return deal["id"]
```

Wire as Partnerstack webhook to your webhook proxy.

### Recipe 8: Multi-touch attribution snapshot

```sql
-- Position-based (W-shape): 30% first touch, 40% middle, 30% last touch
WITH touches AS (
  SELECT opportunity_id, partner_id, touch_at,
         ROW_NUMBER() OVER (PARTITION BY opportunity_id ORDER BY touch_at)        AS rn_asc,
         ROW_NUMBER() OVER (PARTITION BY opportunity_id ORDER BY touch_at DESC)   AS rn_desc,
         COUNT(*) OVER (PARTITION BY opportunity_id)                              AS n
  FROM partner_touches
)
SELECT opportunity_id, partner_id,
       SUM(CASE
         WHEN rn_asc=1 THEN 0.30
         WHEN rn_desc=1 THEN 0.30
         ELSE 0.40 / NULLIF(n-2, 0)
       END) AS attribution_weight
FROM touches GROUP BY opportunity_id, partner_id;
```

Join to opportunity `amount` for partner-influenced revenue.

### Recipe 9: Cross-agent push to sales-agent

```python
def push_to_sales_agent(partner_id):
    rows = warehouse_query(STALE_PARTNER_DEALS_SQL, partner_id=partner_id)
    if rows:
        publish_event("sales-agent.partner-deals-needing-nudge", {
            "partner_id": partner_id,
            "deals": rows,
            "suggested_action": "channel-manager warm-intro + joint follow-up call this week",
        })
```

`sales-agent` runs the actual follow-up; partnerships-agent only tags + flags.

### Recipe 10: Attribution audit (monthly)

```sql
-- Find Partner-tagged deals with no matching partner_touches event (likely mis-tagged)
SELECT o.id, o.name, o.partner_id, o.amount, o.created_at
FROM opportunities o
LEFT JOIN partner_touches pt ON pt.opportunity_id = o.id
WHERE o.source='Partner'
  AND o.created_at >= NOW() - INTERVAL '30 days'
  AND pt.id IS NULL;
```

Each row → review with sales-agent; either add backdated `partner_touches` record or change `source` to `Direct`.

### Recipe 11: Render dashboard to Notion

```python
def render_notion_partner_dash():
    rows = warehouse_query(WEEKLY_ROLLUP_SQL)
    notion.databases.update_or_insert(
        database_id=PARTNER_DASH_DB_ID,
        rows=[{
            "Partner": r["partner_name"],
            "Open pipe ($)": r["pipeline_open"],
            "Won ($)": r["revenue_won"],
            "Win rate": r["win_rate"],
            "Last touched": r["last_touched_at"].isoformat(),
            "Health": "Green" if r["win_rate"]>=0.25 else "Yellow" if r["win_rate"]>=0.15 else "Red",
        } for r in rows],
    )
```

## Examples

### Example 1: Q3 board-deck slide — direct vs partner pipeline share

**Goal:** Show CEO the 13-week trend of partner-influenced pipeline as % of total.

**Steps:**
1. Recipe 4 SQL run.
2. Pivot to wide format (week × channel).
3. Render to stacked bar chart via `xlsx` or `google-sheets`.
4. Result: Partner share grew from 18% (Q1) to 27% (Q3) — board narrative confirmed.

**Result:** Board slide ships with confidence; partner-program ROI argument supported.

### Example 2: Monday 7am partner pipeline digest fires

**Goal:** Each Monday 7am, post per-partner weekly digest to `#partner-pipeline`.

**Steps:**
1. `postgresql-mcp` cron @ Monday 7am UTC runs Recipe 3.
2. Recipe 6 builds Slack blocks per top-10 partner by open pipe.
3. `slack-mcp` `chat.postMessage` posts to `#partner-pipeline`.
4. Recipe 5 also runs; stale deals (14d) ping channel manager via @-mention.

**Result:** Hands-off partner-manager Monday-AM context; alerts force action on stale partner deals.

### Example 3: Acme submitted a lead; auto-deal created + tagged

**Goal:** Acme partner submits prospect via Partnerstack form; deal auto-created in HubSpot.

**Steps:**
1. Partnerstack webhook fires on `lead.submitted`.
2. Recipe 7 creates HubSpot deal with `Partner` source + `partner_id=acme-001`.
3. HubSpot workflow routes to AE; first-touch date = today.
4. AE works deal; later closes-won; commission auto-posts via `partnerstack-tackle-channel-management` Recipe 2.

**Result:** Lead-to-cash partner attribution intact end-to-end.

## Edge cases / gotchas

- **Manual source-field hygiene fails** — AEs forget to set `source=Partner`. Solution: HubSpot/Salesforce validation rule + monthly Recipe 10 audit + channel manager remedial training. Don't trust source field 100% without audit.
- **First-touch vs last-touch dispute** — partner-A introduced 6 months ago; partner-B closed-pitch helped last week; both claim credit. Set policy in master agreement; default last-touch (Partnerstack default) but document W-shape for strategic deals.
- **Direct AE intercepts partner-sourced deal** — AE removes `source=Partner` tag to claim direct commission. Lock field after first-touch date set; only channel manager can re-attribute.
- **Lead vs deal vs opportunity** — HubSpot lifecycle differs by stage. Tag at lead, persist to deal/opp. Don't lose attribution at lead-to-deal conversion.
- **Re-attribution mid-deal** — partner introduced, then partner-B helped close. Add `partner_touches` event log; final commission calc applies attribution model at close.
- **Partner-name vs partner-ID** — using partner-name as join key fails at re-naming. Always use opaque `partner_id` (UUID or Partnerstack ID).
- **Quarter-boundary timing** — deal sourced Q1, closed Q2; which quarter does it credit? Default: source quarter for pipeline, close quarter for revenue.
- **CRM ARR vs ACV vs TCV** — different deal types use different amounts. Standardize on ACV for partner reporting; document conversion for TCV (multi-year) deals.
- **Multi-partner co-sourced deals** — both partners actually contributed. Track in `partner_touches` ledger; split commission per agreement (default 60/40 first/last; allow custom).
- **Partner of partner (sub-channel)** — distributor sells through their reseller. Attribute primary + secondary; commission per agreement.
- **Test data pollution** — sandbox deals tagged Partner pollute reports. Filter by `is_test_record=false` in all reports.
- **Stale-deal alert fatigue** — 50 stale deals every Monday. Filter to top-10 by amount; let smaller deals roll to monthly digest. Suppress for `stage=lost-recovery-in-progress`.
- **Cross-CRM partners** — partner operates in Salesforce; you're HubSpot. Account-mapping via Crossbeam plus manual partner_id sync; or both onboard to Partnerstack.

## Sources

- Partnerstack attribution: https://www.partnerstack.com/blog/partner-attribution
- Crossbeam attribution: https://www.crossbeam.com/blog/attribution/
- HubSpot Deals API: https://developers.hubspot.com/docs/api/crm/deals
- Salesforce REST API: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/
- Sirius Decisions partner attribution frameworks: https://www.forrester.com/blogs/category/partner-ecosystems/
