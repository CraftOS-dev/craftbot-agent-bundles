<!--
Sources:
- EventManagerBlog Sponsorship Prospectus: https://www.eventmanagerblog.com/sponsorship-prospectus
- EventManagerBlog Sponsorship Management: https://www.eventmanagerblog.com/sponsorship-management
- Ungerboeck Sponsorship Management: https://www.ungerboeck.com/sponsorship-management
- Cvent Floor Plan Builder: https://www.cvent.com/en/event-marketing-management/event-floor-plan-design
- Cvent Lead Capture: https://www.cvent.com/en/event-marketing-management/lead-capture
- Klik SmartBadge: https://www.bizzabo.com/klik
- IAEE Selling Sponsorship: https://www.iaee.com
-->
# Sponsor Tier + Deliverable Tracking — SKILL

End-to-end sponsorship operations: tier definition → prospectus → outreach → contract parsing → deliverable extraction → tracker setup → weekly digest → lead handoff → post-event report. Sponsorship contracts are NOT marketing documents — they are operational documents where every line item is a task with an owner, due date, and proof-of-delivery requirement.

## When to use this skill

- Designing a sponsorship program for a new conference / summit / virtual event
- Renewing sponsorships for repeat events (anniversary, season 2, year-over-year)
- Mid-event sponsor crisis (booth not built, logo missing, deliverable failed)
- Pre-event sponsor walk-through (booth location confirmation, lead capture setup, sponsored item timing)
- Post-event lead handoff + ROI report to sponsors
- Sponsor renewal conversations (post-event → next-year commitment)

**Do NOT use this skill when:**
- Sponsor relationship management is the primary need (defer to `bd-partnerships`)
- Sponsor outreach is part of broader BD campaign (coordinate with `bd-partnerships`)
- Sponsored content creation (defer to `marketing-agent`)

## Setup

### Tools

- `firecrawl-mcp` + `brave-search` for sponsor prospect research
- `notion-mcp` for sponsor DB + deliverable tracker + prior-engagement history
- `gmail-mcp` for outreach + weekly digest + post-event report delivery
- `cli-anything` for DocuSign API (contract execution) + CRM API (lead sync)
- `drawio-mcp` for booth floor plan
- `pptx` skill for prospectus + deliverable status deck

### Optional MCPs

- `hubspot-mcp` / `salesforce-mcp` for direct lead-to-CRM sync
- `posthog-mcp` for sponsor-booked meeting funnel tracking
- `slack-mcp` for day-of sponsor coordination channel

## Common recipes

### Recipe 1: Tier definition (200-500 attendee SaaS conference)

```markdown
# Sponsorship Tiers — DevConf 2027

## Platinum — $75,000 (cap 2 sponsors)
- 30-min keynote slot on Day 1 (premium time)
- 20x20 ft booth in lobby premium location
- 5 attendee passes (named) + 5 booth-staff passes
- Branded networking happy hour (Day 1 evening, 200 attendees)
- Logo placement: stage backdrop, lanyards, website hero, app splash, all session intro slides, post-event recording bumper, swag bag insert
- Attendee list (opt-in): full export with email + company + title + interests
- Post-event report (custom 5-page deck)
- Renewable right of first refusal for 2028
- Decision-maker meetings: 5 pre-booked via Brella matchmaking

## Gold — $35,000 (cap 4 sponsors)
- 20-min breakout session (track of choice, time TBD by committee)
- 10x20 ft booth in main expo hall
- 4 attendee passes + 3 booth-staff passes
- Sponsored coffee break (branded cart + napkins + signage; 30-min window)
- Logo placement: website, app, lanyards, recording bumper, swag insert
- Attendee list (opt-in): export with email + company
- Post-event report (standard 2-page)
- Decision-maker meetings: 3 pre-booked via Brella

## Silver — $15,000 (cap 8 sponsors)
- 10-min lightning talk in community track (slot lottery)
- 10x10 ft booth in main expo hall
- 3 attendee passes + 2 booth-staff passes
- Logo placement: website, app, swag insert
- Lead capture access via Klik SmartBadge / Whova Lead Scanner
- Decision-maker meetings: 1 pre-booked via Brella

## Bronze — $5,000 (cap 16 sponsors)
- 10x10 ft booth in expo hall (corner location ineligible)
- 2 attendee passes + 1 booth-staff pass
- Logo placement: website, app
- Lead capture access

## In-Kind — varies
- Coffee bar / lunch / swag bag stuffer / charging stations / wifi sponsor
- Tier equivalence: $5K-$15K of in-kind value = Bronze; $25K+ = Gold equivalence
- Logo placement matched to equivalent paid tier
```

### Recipe 2: Sponsorship prospectus (pptx via `pptx` skill)

```markdown
# Prospectus deck — DevConf 2027 — 9 slides

1. Cover — DevConf 2027 / Sept 15-17 / Chicago / 600 attendees
2. Audience — 60% senior IC + 25% manager + 15% director+; 70% from $50M+ companies
3. Past sponsors — logos (with permission) + testimonial quotes
4. Attendance history — Year 1: 200 | Year 2: 350 | Year 3 target: 600
5. Why sponsor — brand + lead gen + recruiting + community + thought leadership
6. Tier comparison — table with all deliverables per tier
7. Investment + ROI — per-tier cost + benchmark lead conversion (10-20% trade-show avg)
8. Past sponsor results — "Acme captured 340 leads + closed $1.2M pipeline within 6 months"
9. CTA — Deadline July 1 for tier selection; sponsor@devconf.io contact
```

### Recipe 3: Sponsor outreach (per pr-comms cold-outreach pattern)

```bash
# Research prospect company first
mcp tool firecrawl.scrape --url "https://acme.com" --formats markdown
mcp tool brave-search.search --q "Acme Series B 2026 funding round"
mcp tool linkedin.search --q "Acme VP Marketing"

# Personalized email via gmail-mcp
mcp tool gmail.send_email \
  --to "vp-marketing@acme.com" \
  --subject "DevConf 2027 — Gold sponsor seat?" \
  --body "$(cat <<'EOF'
Hi [Name],

Saw Acme's Series B announcement last week — congrats. Your push on developer experience caught my eye.

DevConf 2027 is the year's mid-tier dev event: 600 attendees, 65% senior IC, 70% from $50M+ companies. Your decision-maker target overlaps tightly.

Gold tier is $35K and includes a 20-min breakout, 10x20 booth, 4 passes, sponsored coffee break, attendee list (opt-in), and Brella pre-booked meetings (3).

ROI benchmark from last year's Gold sponsors: avg 240 leads + $800K pipeline within 90 days.

Worth a 30-min call this week to walk you through the prospectus?

[Sender]
EOF
)" \
  --attachment "devconf-2027-prospectus.pptx"
```

### Recipe 4: Contract → deliverable extraction → tracker

Once contract is signed, parse it (LLM or manual) and create one Notion DB row per deliverable.

```python
# Parse contract via Claude or hand-extracted
contract = open('acme-gold-contract.pdf').read()
deliverables = extract_deliverables_via_claude(contract)
# deliverables looks like:
# [
#   {"deliverable": "Logo on stage backdrop", "tier": "Gold", "due": "2027-08-15", "owner": "Design", "status": "Not started"},
#   {"deliverable": "20-min breakout session", "tier": "Gold", "due": "2027-09-15", "owner": "Program", "status": "Pending sponsor topic"},
#   ...
# ]

for d in deliverables:
    notion.create_db_row(
        database='sponsor-deliverables-2027',
        properties={
            'Sponsor': 'Acme',
            'Tier': 'Gold',
            'Deliverable': d['deliverable'],
            'Owner': d['owner'],
            'Due': d['due'],
            'Status': 'Not started',
            'Proof URL': None,
            'Notes': d.get('notes', '')
        }
    )
```

### Recipe 5: Weekly digest to sponsor + internal

Every Monday during 8 weeks pre-event, send a digest of what's on track + at-risk.

```python
this_week_due = notion.query_db('sponsor-deliverables-2027',
    filter={'Due': {'before': 'now+7d'}, 'Status': {'not': 'Done'}})

at_risk = notion.query_db('sponsor-deliverables-2027',
    filter={'Due': {'before': 'now'}, 'Status': {'not': 'Done'}})

body = render_template('weekly_digest.md',
                       sponsor='Acme',
                       this_week=this_week_due,
                       at_risk=at_risk)

mcp_tool('gmail.send_email',
         to=['sponsor-contact@acme.com', 'internal-sponsor-lead@us.com'],
         subject=f"Acme — DevConf 2027 — Weekly status — {date.today()}",
         body=body)
```

### Recipe 6: Booth floor plan in drawio

```bash
# Create floor plan with sponsor booth placement
mcp tool drawio.create_diagram \
  --name "DevConf 2027 — Expo Floor" \
  --template "venue_floor_plan" \
  --grid 10 \
  --rooms '[
    {"name": "Lobby (Platinum)", "x": 0, "y": 0, "w": 40, "h": 40, "color": "gold"},
    {"name": "Main Expo Hall", "x": 50, "y": 0, "w": 200, "h": 150}
  ]' \
  --booths '[
    {"sponsor": "Acme (Gold)", "x": 60, "y": 20, "w": 10, "h": 20},
    {"sponsor": "Beta (Silver)", "x": 80, "y": 20, "w": 10, "h": 10}
  ]'
```

Booth-location strategy:
- **Platinum**: lobby premium (first thing attendees see at check-in)
- **Gold**: corner of main hall (high traffic at entry)
- **Silver**: row endpoints (visible from aisle)
- **Bronze**: middle rows (still walked, lower visibility)

### Recipe 7: Pre-event walk-through (1 week out)

Walk each sponsor through:
- Booth location confirmation (with floor plan PDF + GPS pin if outdoor)
- Booth setup window (e.g., Sept 14 4pm-8pm)
- Lead capture device pickup (Klik SmartBadge / Cvent LeadCapture / Whova scanner)
- Sponsored item timing + branded asset verification (logo printed correctly, cart branded)
- Sponsor session run-of-show (rehearsal slot, A/V cues, session moderator intro)
- Day-of comms channel (`slack-mcp` sponsor-ops channel; primary contact phone numbers)

### Recipe 8: Day-of monitoring

```python
# Hourly via cli-anything cron
for sponsor in sponsors:
    deliverables = notion.query_db('sponsor-deliverables-2027',
        filter={'Sponsor': sponsor, 'Status': 'Live'})
    for d in deliverables:
        if d['due'] < now and not d['proof_url']:
            slack.send_alert(channel='sponsor-ops',
                             text=f"{sponsor}: {d['deliverable']} not yet confirmed live")
```

### Recipe 9: Lead handoff within 48 hours

```bash
# Export leads from event platform
curl -X GET "https://api.cvent.com/v1/events/$EVENT_ID/lead-capture/exports?sponsor=acme" \
  -H "Authorization: Bearer $CVENT_API_TOKEN" \
  -o acme-leads.csv

# Sync to sponsor's CRM
mcp tool hubspot.import_contacts \
  --portal-id "$ACME_HUBSPOT_PORTAL" \
  --file acme-leads.csv \
  --source "DevConf 2027" \
  --pipeline "Conference Pipeline"

# Confirmation email
mcp tool gmail.send_email \
  --to "sponsor-contact@acme.com" \
  --subject "DevConf 2027 — your leads (240 captured)" \
  --body "$(cat acme_lead_summary.md)" \
  --attachment "acme-leads.csv"
```

### Recipe 10: Post-event report per sponsor

```markdown
# Acme @ DevConf 2027 — Post-Event Report

## Deliverables status (all completed)
[Checklist of all 18 deliverables with proof URLs]

## Lead capture
- Total scans: 287
- Opt-in leads: 240 (84% opt-in rate)
- Decision-maker leads (Director+): 96 (40%)
- Title breakdown: [chart]

## Brella meetings
- Pre-booked: 3 / scheduled: 3 / held: 3 / outcomes: 2 follow-ups + 1 deal in motion

## Brand visibility
- Logo impressions (stage backdrop): ~600 attendees x 12 hours = 7,200 impressions
- App splash impressions: 540 active app users
- Sponsored coffee break: 280 visitors

## Recordings
- Acme breakout view count: pending (Whisper transcript + YouTube upload Day 7)

## Renewal conversation
- Q4 follow-up scheduled with [BD lead] — propose Platinum 2028
```

## Examples

### Example A: 16-sponsor conference, tier distribution

```
Platinum: 2 ($150K)
Gold: 4 ($140K)
Silver: 8 ($120K)
Bronze: 8 ($40K)
In-Kind: 3 (~$30K value)
Total cash sponsorship: $450K
Total in-kind value: $30K
Per-attendee sponsor offset: $750 (vs $1,400 cost-per-attendee → 53% offset)
```

### Example B: Sponsor crisis (Day 1, gold sponsor coffee break failed)

```
Issue: Gold sponsor's branded coffee cart didn't arrive
Resolution:
1. Slack ops alert to sponsor contact + internal team
2. Quick local catering replacement (white-label, no branding)
3. Sponsor offered makeup: prominent intro at next session + extended booth time + complimentary swag insert
4. Document in post-event report with mitigation; offer 5% credit on 2028 renewal
```

### Example C: Renewal conversation prep

```
Acme @ DevConf 2027 Gold: $35K invested
- Got 240 opt-in leads × benchmark MQL→opp rate 8% = 19 opps
- Avg deal size $80K × 25% close rate = 4 deals × $80K = $320K pipeline
- ROI: 9.1x ($320K / $35K)
→ Propose Platinum 2028 ($75K) with: keynote + premium booth + branded happy hour
→ Hand off to bd-partnerships for renewal close
```

## Edge cases

### Sponsor not meeting deliverable
If sponsor fails to deliver on their side (e.g., didn't ship booth materials), document immediately + email contact + offer hold-the-spot but defer to next available window. Don't auto-refund; refer to contract cancellation clause.

### Last-minute sponsor request
Sponsors WILL ask for things outside contract during the event ("can we get on the lanyard?", "extra logo placement?"). Default to no unless it's mutual benefit; document any concession for next-year contract.

### Competitor conflict
If two sponsors are direct competitors AND both bought Gold tier with breakout slots, schedule them on different days to avoid attendee defection. Note in deliverable tracker.

### Sponsor speaker quality concern
Sponsor-tier speakers may not match general program quality (vendor pitch risk). Require sponsor-track speaker to submit deck for review 14 days out. Right to coach / edit for technical accuracy.

### Logo file quality
Sponsor logos must be: vector (SVG/PDF/AI) + monochrome version + min 300 DPI raster. Reject low-quality logo files at contract signing. Add to onboarding checklist.

### Lead capture opt-in compliance
GDPR / CCPA: attendees must explicitly opt-in for sponsor lead sharing. Default at registration is OPT-OUT (not opt-in). Export only opt-in records. Document compliance in sponsor agreement.

### Sponsor branding conflict with venue
Some venues prohibit certain types of branding (banners over historic facades, exterior signage). Check venue contract before promising signage placement.

### Multi-sponsor coffee break
If multiple sponsors sponsor the same break (rare), divide visibility: alternating branded napkins, dual-logo cups, dual signage. Document in deliverable tracker.

### In-kind sponsor value disputes
For in-kind sponsors, document agreed equivalent value at signing. Avoids post-event renegotiation.

### Sponsor right of first refusal renewal
Platinum sponsors typically get right of first refusal for next year. Set 60-day window post-event for them to commit; release tier to next prospect after.

### Sponsor attendee pass abuse
Some sponsors send 10x more staff than allocated passes ("badge sharing"). Track scan counts at check-in; alert sponsor contact if >2x over allocation.

## Sources

- **EventManagerBlog Prospectus**: https://www.eventmanagerblog.com/sponsorship-prospectus
- **EventManagerBlog Sponsorship Management**: https://www.eventmanagerblog.com/sponsorship-management
- **Ungerboeck Sponsorship**: https://www.ungerboeck.com/sponsorship-management
- **IAEE Selling Sponsorship Guide**: https://www.iaee.com
- **Cvent Floor Plan Builder**: https://www.cvent.com/en/event-marketing-management/event-floor-plan-design
- **Cvent Lead Capture**: https://www.cvent.com/en/event-marketing-management/lead-capture
- **Klik SmartBadge (Bizzabo)**: https://www.bizzabo.com/klik
- **drawio-mcp**: https://www.drawio.com
