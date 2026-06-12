<!--
Sources:
- Bizzabo Event ROI: https://www.bizzabo.com/blog/event-roi-calculation
- PCMA 2026 Industry Outlook: https://www.pcma.org/research-insights/2026-business-events-industry-outlook/
- HubSpot Event Attribution: https://www.hubspot.com/products/marketing/attribution
- Salesforce Pardot/MCAE Attribution: https://www.salesforce.com/products/marketing-cloud-account-engagement/
- Marketo Engage Attribution: https://www.marketo.com/multi-touch-attribution
- Forrester Event ROI Framework: https://www.forrester.com
-->
# Event ROI: Cost per Attendee + Pipeline-Influenced Revenue — SKILL

End-to-end ROI measurement pipeline: cost capture → attendee + MQL extraction → CRM attribution → pipeline-influenced revenue → ROI computation → executive report. ROI = (pipeline-influenced revenue − total event cost) / total event cost. Three attribution windows: 90 days (short-cycle), 180 days (typical B2B), 365 days (enterprise). Benchmark: 3-5x ROI for well-executed conferences; 8-15x for high-conversion event types.

## When to use this skill

- Computing post-event ROI for executive report (30-90 days post-event)
- Annual ROI summary across event program (CFO / VP Marketing review)
- Year-over-year benchmarking (was 2027 conference better than 2026?)
- Per-tier sponsor ROI (sponsor renewal conversation)
- Per-channel ROI (which marketing channel drove highest-value attendees)
- Event-format decision support (is in-person worth it vs hybrid?)

**Do NOT use this skill when:**
- Pure brand event with no pipeline goal (defer to `marketing-agent`)
- Marketing campaign ROI (not event ROI; defer to `marketing-agent`)
- Customer retention metric instead of revenue (use NPS via `event-analytics-engagement-nps`)
- Stakeholder report doesn't need financial detail (qualitative report sufficient)

## Setup

### Tools

- `cli-anything` for CRM (HubSpot / Salesforce / Marketo) + accounting (Xero / QuickBooks) APIs
- `postgresql-mcp` for cross-event ROI warehouse
- `notion-mcp` for ROI report templates + cost breakdown archive
- `hubspot-mcp` / `salesforce-mcp` if direct CRM MCP available

### CRM API access required

```bash
export HUBSPOT_TOKEN="<token>"           # HubSpot > Settings > Integrations > Private Apps
export HUBSPOT_PORTAL_ID="<portal-id>"

export SALESFORCE_TOKEN="<oauth-token>"
export SALESFORCE_INSTANCE="<instance>.salesforce.com"

export MARKETO_TOKEN="<oauth-token>"
export MARKETO_INSTANCE="<munchkin-id>.mktorest.com"
```

### Accounting API (cost capture)

```bash
export XERO_TOKEN="<oauth-token>"        # Xero developer.xero.com
export XERO_TENANT_ID="<tenant>"

export QUICKBOOKS_TOKEN="<oauth-token>"
export QUICKBOOKS_REALM_ID="<realm>"
```

## Common recipes

### Recipe 1: Cost capture from accounting

```python
# Pull all expenses tagged "DevConf 2027" from Xero
expenses = xero.invoices.list(
    where='Reference.Contains("DevConf 2027")',
    statuses=['AUTHORISED', 'PAID']
)

cost_breakdown = {
    'venue_av': 0,
    'catering_fb': 0,
    'speaker_fees': 0,
    'speaker_travel': 0,
    'marketing_promo': 0,
    'swag_signage': 0,
    'tech_platforms': 0,  # registration platform, streaming, app
    'insurance': 0,
    'other': 0
}

for inv in expenses:
    category = classify_expense(inv.line_items)  # by GL code or vendor name
    cost_breakdown[category] += inv.amount_total

total_cost = sum(cost_breakdown.values())
```

### Recipe 2: Sponsor revenue offset

```python
sponsor_revenue = notion.query_db('sponsors-2027', filter={'paid': True})
total_sponsor_revenue = sum(s['amount'] for s in sponsor_revenue)

net_cost = total_cost - total_sponsor_revenue
```

### Recipe 3: Attendee + MQL extraction

```python
# Pull registered attendees from event platform
attendees = cvent.get_event_registrations(event_id='devconf-2027')
registered = len(attendees)
attended = sum(1 for a in attendees if a['checked_in'])

# Pull MQLs attributed to event source
mqls = hubspot.contacts.search(
    query={
        'filterGroups': [
            {
                'filters': [
                    {'propertyName': 'original_source_drill_down_1', 'operator': 'EQ', 'value': 'DevConf 2027'},
                    {'propertyName': 'lifecyclestage', 'operator': 'EQ', 'value': 'marketingqualifiedlead'}
                ]
            }
        ]
    }
)
mql_count = mqls.total
mql_rate = mql_count / attended  # benchmark: 20-30% in-person, 10-15% virtual
```

### Recipe 4: Pipeline-influenced revenue (3 attribution windows)

```sql
-- Salesforce / HubSpot via SQL warehouse
-- 90-day attribution window
WITH event_contacts AS (
  SELECT contact_id, first_touch_date
  FROM contacts
  WHERE event_source = 'DevConf 2027'
),
attributed_opps AS (
  SELECT o.opportunity_id, o.amount, o.close_date, o.stage,
         ec.contact_id, ec.first_touch_date,
         (o.created_date - ec.first_touch_date) AS days_since_event
  FROM opportunities o
  JOIN opportunity_contact_role ocr ON ocr.opportunity_id = o.opportunity_id
  JOIN event_contacts ec ON ec.contact_id = ocr.contact_id
)
SELECT
  COUNT(DISTINCT CASE WHEN days_since_event <= 90 THEN opportunity_id END) AS opps_90d,
  SUM(CASE WHEN days_since_event <= 90 THEN amount ELSE 0 END) AS pipeline_90d,
  COUNT(DISTINCT CASE WHEN days_since_event <= 180 THEN opportunity_id END) AS opps_180d,
  SUM(CASE WHEN days_since_event <= 180 THEN amount ELSE 0 END) AS pipeline_180d,
  COUNT(DISTINCT CASE WHEN days_since_event <= 365 THEN opportunity_id END) AS opps_365d,
  SUM(CASE WHEN days_since_event <= 365 THEN amount ELSE 0 END) AS pipeline_365d
FROM attributed_opps;
```

### Recipe 5: ROI computation

```python
roi_90 = (pipeline_90d - net_cost) / net_cost
roi_180 = (pipeline_180d - net_cost) / net_cost
roi_365 = (pipeline_365d - net_cost) / net_cost

cost_per_attendee = net_cost / registered
cost_per_mql = net_cost / mql_count
cost_per_opp = net_cost / opps_180d

# Benchmarks (2026):
# - In-person: $1,400 cost/attendee (avg); 3-5x ROI (well-executed conference)
# - Hybrid: $900 cost/attendee; similar ROI range
# - Virtual: $135 cost/attendee; 5-10x ROI (lower investment, lower friction)
```

### Recipe 6: Multi-touch attribution (linear / time-decay / U-shaped)

```python
# Linear: equal credit to all touchpoints
# Time-decay: more credit to recent touchpoints
# U-shaped: 40% first + 40% last + 20% middle

# HubSpot Attribution Reports natively support these models
attribution = hubspot.attribution.create_report(
    name='DevConf 2027 Attribution',
    model='u_shaped',
    attribution_type='revenue',
    filters={'deal_close_date': {'gte': '2027-09-15', 'lte': '2028-09-15'}}
)
```

### Recipe 7: Per-channel attendee ROI

```python
# Which marketing channel drove highest-value attendees?
channels = ['paid_linkedin', 'organic_search', 'email_nurture', 'paid_meta', 'referral', 'pr_earned']

for ch in channels:
    attendees_ch = hubspot.contacts.search(query={
        'filterGroups': [{'filters': [
            {'propertyName': 'original_source', 'operator': 'EQ', 'value': ch},
            {'propertyName': 'event_source', 'operator': 'EQ', 'value': 'DevConf 2027'}
        ]}]
    })
    pipeline_ch = sum(opp_amount for opp in get_opps(attendees_ch))
    print(f"{ch}: {len(attendees_ch)} attendees → ${pipeline_ch:,.0f} pipeline")
```

### Recipe 8: Per-tier sponsor ROI (sponsor renewal conversation)

```python
sponsors = notion.query_db('sponsors-2027')
for sponsor in sponsors:
    leads_captured = cvent.get_leads(sponsor_id=sponsor.id)
    # Estimate sponsor pipeline assuming 10% MQL→opp × $80K × 25% close
    estimated_pipeline = len(leads_captured) * 0.10 * 80000 * 0.25
    sponsor_roi = (estimated_pipeline - sponsor.investment) / sponsor.investment
    notion.update_row(sponsor.id, {'estimated_pipeline': estimated_pipeline, 'roi_estimate': sponsor_roi})
```

### Recipe 9: Executive ROI report

```markdown
# DevConf 2027 — ROI Report (180-day attribution)

## Executive summary
- Registered: 612 / attended: 580 (95% attendance)
- NPS: 58 (target 50; benchmark 50-70)
- Total cost: $812,000
- Sponsor revenue: $450,000
- Net cost: $362,000
- Cost per attendee: $624
- MQLs: 137 (24% MQL rate)
- 180-day pipeline-influenced revenue: $4.2M
- 180-day ROI: 11.6x ($4.2M / $362K)
- 90-day pipeline: $1.8M (ROI 4.9x)
- 365-day pipeline projection: $7.5M (ROI 20.7x)

## Cost breakdown
| Category | Amount | % of Total |
|---|---|---|
| Venue + AV | $342K | 42% |
| Catering + F&B | $164K | 20% |
| Speaker fees + travel | $98K | 12% |
| Marketing + promo | $112K | 14% |
| Swag + signage | $34K | 4% |
| Tech platforms (reg, app, streaming) | $43K | 5% |
| Insurance + misc | $19K | 2% |
| **Total** | **$812K** | **100%** |
| Sponsor offset | -$450K | |
| **Net cost** | **$362K** | |

## Pipeline detail
- 90-day: 41 opps, $1.8M, avg $44K per opp
- 180-day: 96 opps, $4.2M, avg $44K per opp
- 365-day projection: ~210 opps, $7.5M (based on YoY closure rate)
- Closed-won 180-day: 18 opps, $720K
- Pipeline conversion forecast: 30-40% close → $1.4M-$1.7M revenue

## Per-channel performance
- Paid LinkedIn: 180 attendees → $1.1M pipeline (6.1x cost ratio)
- Email nurture: 142 attendees → $2.4M pipeline (16.9x cost ratio)  ← best
- Organic search: 95 attendees → $410K pipeline
- Paid Meta: 88 attendees → $190K pipeline
- Referral: 75 attendees → $98K pipeline

## Per-tier sponsor performance
- Platinum (2 sponsors): avg 13.7x ROI
- Gold (4 sponsors): avg 9.2x ROI
- Silver (8 sponsors): avg 4.3x ROI
- Bronze (8 sponsors): avg 1.8x ROI

## Recommendations for 2028
- Continue: speaker quality (Sarah K. drove 23% of NPS positive verbatims); networking via Brella
- Change: lunch line congestion (12% of negative verbatims) — expand seating + faster service
- Discontinue: paid Meta channel (low pipeline ratio); reallocate to email nurture
- Scale up: Platinum tier (waitlist exists; cap at 4 instead of 2)
```

### Recipe 10: Cross-event YoY benchmarking

```sql
-- postgresql-mcp: YoY ROI comparison
SELECT
  year,
  registered,
  attended,
  net_cost,
  cost_per_attendee,
  pipeline_180d,
  pipeline_180d / net_cost AS roi_180d,
  sponsor_revenue,
  sponsor_revenue / net_cost AS sponsor_offset_ratio,
  nps
FROM event_roi
WHERE event_name = 'DevConf' AND year BETWEEN 2024 AND 2027
ORDER BY year;
```

## Examples

### Example A: 600-attendee in-person, $362K net cost, 11.6x 180-day ROI

```
Net cost: $362K
Cost per attendee: $624
180-day pipeline: $4.2M
ROI: 11.6x
Verdict: above benchmark (3-5x typical); continue investment
```

### Example B: 200-attendee virtual, $25K net cost, 8.0x 90-day ROI

```
Net cost: $25K
Cost per attendee: $125 (vs $135 virtual benchmark)
90-day pipeline: $200K
ROI: 8.0x (higher conversion typical for virtual)
Verdict: continue; consider quarterly cadence
```

### Example C: Hybrid event, $200K net cost, breakeven year-over-year

```
Net cost: $200K
Cost per attendee: $300
180-day pipeline: $250K
ROI: 1.25x (below 3x benchmark)
Verdict: hybrid format may be wrong fit OR pipeline attribution misconfigured; investigate
- Check: were all event-source MQLs flagged in HubSpot?
- Check: are opps tagged with multi-touch correctly?
- Action: review attribution config, reconsider hybrid format vs full virtual/in-person
```

## Edge cases

### CRM attribution missing
If event-source field isn't populated for attendees, attribution fails. Verify pre-event:
1. Registration platform sends source field to CRM
2. CRM has custom field for event_source
3. New contacts mapped to event_source on creation

### Single-touch vs multi-touch
First-touch attribution under-credits events (they may be 3rd touch). Multi-touch (linear / time-decay / U-shaped) is fairer but harder. Document model used in report.

### Long sales cycles
Enterprise sales cycle > 365 days. Use 365-day window OR forecast based on historical closure rate. Don't penalize the event for slow downstream sales.

### Sponsor pipeline attribution conflict
Sponsor's own CRM attribution may differ from yours. Don't conflate. Provide leads handoff; sponsor measures independently.

### Internal attendees confuse ROI
Internal employees count as attendees but generate no pipeline. Exclude internal from MQL math.

### Discount + comp tickets
Comp tickets ($0 paid) skew cost-per-attendee math up. Report both gross (paid attendees only) AND net (all attendees including comps).

### Multi-event attribution
Attendee at 3 of your events in 12 months — which event gets credit? Use U-shaped or time-decay; document choice.

### Pre-event nurture vs post-event acceleration
Event isn't standalone — it's part of broader nurture. Some pipeline would have closed anyway; some accelerated by event. Forrester recommends "incremental pipeline" by comparing matched control group.

### Channel ROI vs platform CAC
Marketing channels have their own CAC; event is the conversion event. Don't double-count channel cost AND event cost for same opp.

### Cost capture timing
Some costs hit AP weeks after event. Lock cost report at T+60 days; cap revisions after that. Note: insurance / final invoices may slip.

### Speaker fee tax treatment
External speakers: 1099 issued; treated as professional fee. Internal: comp time. Different GL treatment; document.

### Marketing-channel attribution within event
Within event, attribution should credit pre-event marketing (e.g., LinkedIn ad → registered), not event itself. Adjust attribution rules to avoid event eating channel credit.

### Annual event program ROI
Cross-event ROI: sum all event costs + sum all event pipelines. Better than single-event view for executive context.

## Sources

- **Bizzabo Event ROI**: https://www.bizzabo.com/blog/event-roi-calculation
- **PCMA 2026 Industry Outlook**: https://www.pcma.org/research-insights/2026-business-events-industry-outlook/
- **HubSpot Attribution**: https://www.hubspot.com/products/marketing/attribution
- **Salesforce MCAE Attribution**: https://www.salesforce.com/products/marketing-cloud-account-engagement/
- **Marketo Multi-Touch Attribution**: https://www.marketo.com/multi-touch-attribution
- **Forrester Event ROI Framework**: https://www.forrester.com
- **CEMA Benchmarks**: https://cemaonline.com
