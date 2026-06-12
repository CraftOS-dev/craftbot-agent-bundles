<!--
Sources: Klue battlecard software https://klue.com/topics/best-sales-battlecard-software
         Klue × Salesforce https://klue.com/blog/win-loss-battlecards-salesforce
         Crayon https://www.crayon.co/
Companion playbook: role.md → "Battlecard authoring playbook" + "Battlecard template"
-->

# Battlecard authoring + maintenance

One battlecard per competitor: positioning differentiator, top-3 objections + rebuttals, latest deal intel, feature parity snapshot, pricing leverage, kill-shots, traps, refresh trigger, provenance footer. Klue/Crayon for paid delivery; Notion + Slack + Salesforce Lightning for self-build. Refresh-on-signal — not on schedule.

## When to use

- "Build me a battlecard for [competitor]"
- "Refresh the [competitor] battlecard"
- New competitor enters the comp set
- Win/loss interview lands new objection theme
- Refresh-on-signal trigger fires (changelog / pricing / G2 / exec move)

## When NOT to use

- Deal-specific micro-battlecard → use `hot-deals-ci-deal-level`
- Kill-sheet-only refresh → use `kill-sheet-objection-rebuttals`
- Pure delivery-channel setup → use `ci-delivery-slack-crm-klue-insider`

## Setup

```bash
# Paid (Klue / Crayon)
export KLUE_API_KEY="..."
export CRAYON_API_KEY="..."

# Self-build path
export NOTION_API_KEY="secret_..."
export NOTION_DB_BATTLECARDS="..."
export SLACK_WEBHOOK_URL="..."

# Salesforce
export SF_INSTANCE_URL="..."
export SF_ACCESS_TOKEN="..."
```

MCPs in `agent.yaml`: `notion-mcp` / `better-notion`, `slack-mcp`, `salesforce-api`, `docx`, `pdf`, `gmail-mcp`.

## Common recipes

### Recipe 1: Battlecard JSON schema

```json
{
  "competitor": "acme-corp",
  "last_refresh": "2026-06-11",
  "pmm_approved_at": "2026-06-01",
  "pmm_owner": "@pmm-lead",
  "panes": {
    "positioning": "We close the [job-to-be-done] in [N] minutes vs Acme's [M] minutes — proven in [case study X].",
    "objections": [
      {"says":"Acme has better Snowflake integration","rebut":"Our Snowflake connector ships pushdown SQL for 3x faster query — see <case study>","sources":["g2:45678"]},
      {"says":"Acme cheaper at SMB tier","rebut":"True at $19 entry; our Pro at $29 includes SSO that Acme charges $5/seat for","sources":["acme.com/pricing"]},
      {"says":"Acme has SOC2","rebut":"We have SOC2 + HIPAA + ISO27001; Acme only SOC2","sources":["trust.acme.com","trust.us.com"]}
    ],
    "latest_deal_intel": {"window_days":90,"wins":12,"losses":4,"at_risk":3,
        "top_won":"integration breadth","top_lost":"price at SMB",
        "recent_quote":"'Snowflake pushdown was the inflection point' — Champion at <ListCo>"},
    "pricing": {"their_entry":"$19/seat","ours":"$29/seat","typical_discount":"15%"},
    "feature_parity_snapshot_url":"...parity.xlsx#acme",
    "kill_shots": ["48hr support response window — 4 of 10 recent G2 reviews", "Bandwidth caps not shown on pricing page"],
    "traps":["Don't claim 'we have more integrations' — they passed us in Apr 2026"],
    "refresh_triggers":["changelog_diff","pricing_diff","g2_review_batch_gt_3","exec_change","earnings_call"]
  },
  "sources": [
    {"url":"https://acme.example.com/pricing","ts":"2026-06-08","class":"public"},
    {"url":"https://www.g2.com/products/acme/reviews/45678","ts":"2026-06-07","class":"public"}
  ]
}
```

### Recipe 2: Klue create / update via REST API

```bash
curl -X POST "$KLUE_API_BASE/battlecards" \
  -H "Authorization: Bearer $KLUE_API_KEY" \
  -d @battlecard-acme.json
```

```bash
# Update existing
curl -X PATCH "$KLUE_API_BASE/battlecards/<id>" \
  -H "Authorization: Bearer $KLUE_API_KEY" \
  -d '{"panes":{"objections":[...]}}'
```

### Recipe 3: Crayon battlecard upsert

```bash
curl -X PUT "https://api.crayon.co/v1/battlecards/acme-corp" \
  -H "Authorization: Bearer $CRAYON_API_KEY" \
  -d @battlecard-acme.json
```

### Recipe 4: Notion battlecard page (self-build)

```python
from notion_client import Client
n = Client(auth=os.environ["NOTION_API_KEY"])
n.pages.create(
    parent={"database_id": os.environ["NOTION_DB_BATTLECARDS"]},
    properties={
        "Name":{"title":[{"text":{"content":"Acme Corp battlecard"}}]},
        "Competitor":{"select":{"name":"acme-corp"}},
        "Last refresh":{"date":{"start":"2026-06-11"}},
        "PMM approved":{"date":{"start":"2026-06-01"}},
    },
    children=[
        {"object":"block","type":"heading_2","heading_2":{"rich_text":[{"text":{"content":"Positioning"}}]}},
        {"object":"block","type":"paragraph","paragraph":{"rich_text":[{"text":{"content":battlecard["panes"]["positioning"]}}]}},
        # ... more blocks per pane
    ],
)
```

### Recipe 5: Salesforce Lightning surface

```javascript
// LWC stub — pull battlecard for competitor field on opportunity
import { LightningElement, api, wire } from 'lwc';
import getBattlecard from '@salesforce/apex/CIController.getBattlecard';
export default class BattlecardPanel extends LightningElement {
  @api recordId;
  @wire(getBattlecard, { opportunityId: '$recordId' }) bc;
}
```

Klue Insider / Crayon Sales App = pre-built equivalent.

### Recipe 6: Render branded docx

```python
from docx import Document
doc = Document()
doc.add_heading(f"Battlecard: {bc['competitor']}", level=1)
doc.add_paragraph(f"Last refresh: {bc['last_refresh']}").bold = True
doc.add_heading("Positioning", level=2)
doc.add_paragraph(bc["panes"]["positioning"])
# ... loop other panes
doc.save("battlecards/acme.docx")
```

### Recipe 7: Refresh-on-signal trigger config

See role.md → "Refresh-on-signal trigger config" YAML pattern. Wire each signal source (Visualping monitor ID, Apify review pipe, Owler exec API) to a battlecard pane flag.

### Recipe 8: PMM approval workflow

```python
# When new differentiator language is drafted, set status to PENDING_PMM
# Slack the PMM owner with a 1-line preview + link
# On their reply (or Slack reaction :white_check_mark:), promote to APPROVED + set pmm_approved_at
```

### Recipe 9: Source / provenance footer auto-generator

```python
def footer(bc):
    lines = ["─────────────", f"SOURCES (last refresh: {bc['last_refresh']})", "─────────────"]
    for s in bc["sources"]:
        lines.append(f"• {s['url']} ({s['class']}, {s['ts']})")
    lines += ["─────────────",
              f"ETHICS CLASS: public-source-only · SCIP-compliant",
              f"PMM APPROVED: yes (signoff: {bc['pmm_approved_at']}, {bc['pmm_owner']})"]
    return "\n".join(lines)
```

### Recipe 10: Slack hot-refresh announcement

```python
requests.post(SLACK_WEBHOOK_URL, json={
    "text": f":battery: Battlecard refreshed: *{bc['competitor']}*",
    "blocks":[
        {"type":"section","text":{"type":"mrkdwn","text":
            f"*{bc['competitor']}* battlecard refreshed.\n"
            f"Trigger: `{trigger}` • Pane(s) updated: `{','.join(panes)}`"}},
        {"type":"actions","elements":[
            {"type":"button","text":{"type":"plain_text","text":"Open in Salesforce"},"url":sf_url}
        ]}
    ],
})
```

### Recipe 11: Open-rate metrics surface

Klue / Crayon native: battlecard open per rep per deal. Self-build: log a Lightning Component view event into a custom object; query weekly.

```sql
SELECT Competitor__c, COUNT(Id) opens
FROM Battlecard_View__c
WHERE Viewed_At__c >= LAST_N_DAYS:30
GROUP BY Competitor__c
ORDER BY opens DESC
```

## Examples

### Example 1: First battlecard for a new competitor (Acme)

**Goal:** Stand up Acme battlecard from scratch in 1 day.

**Steps:**
1. Gather inputs (positioning, features, pricing, reviews, win/loss) per role.md battlecard playbook step 1.
2. Author panes per Recipe 1 schema; PMM-approve positioning + objection rebuttal language (Recipe 8).
3. Push to Klue (Recipe 2) or Notion + Salesforce LWC (Recipe 4 + 5).
4. Wire refresh triggers (Recipe 7) — changelog + pricing + G2 batch.
5. Announce in Slack (Recipe 10).

**Result:** Acme battlecard live in Salesforce + Notion mirror; 5 auto-refresh signals wired.

### Example 2: Refresh on pricing-change signal

**Goal:** Acme dropped Pro tier 20%. Refresh pane 5 + 1 within 24 hours.

**Steps:**
1. Distill.io / Visualping webhook fires.
2. Pull current pricing.yaml; patch battlecard pane 5 + recompute pane 1 if positioning shifts.
3. PMM-approval flag if positioning language changes (Recipe 8); else auto-promote.
4. Slack-announce (Recipe 10) so reps see the refresh.

**Result:** Battlecard reflects Acme's new pricing within 1 day; reps aren't caught flat.

## Edge cases / gotchas

- **6-8 bullets per pane max** — over-stuffed battlecards have 0 open-rate. Antipattern catalog has the rationale.
- **PMM ownership** — every claim has a PMM-approved version + a verbatim-source citation. Never ship un-approved differentiator language.
- **Refresh on schedule = stale** — refresh-on-signal is the rule. Schedule-refresh as fallback only.
- **Klue / Crayon Salesforce embed scope** — managed packages require admin install; allow 2-3 days. Have Notion fallback for IT-blocked envs.
- **Versioning** — battlecard JSON in git; PR review for material changes. Klue/Crayon Standard tier supports version history; Premium adds audit log.
- **Permissions** — battlecard with internal pricing strategy ≠ public; restrict Salesforce visibility to sales + PMM.
- **Provenance gap** — every claim needs a public source URL + date. If you can't cite, hold the claim.
- **Open-rate < 30%** — battlecard isn't load-bearing for reps; restructure pane 1, talk to top-quartile reps about what they actually use.
- **Multiple battlecards per competitor** — sometimes you need a segment-specific one (SMB vs Enterprise). Use child battlecards in Klue; or `acme-smb.json` + `acme-ent.json` self-build.
- **Klue / Crayon API rate limit** — typical 100 req/min. Batch updates.

## Sources

- Klue — Best Sales Battlecard Software — https://klue.com/topics/best-sales-battlecard-software
- Klue × Salesforce — https://klue.com/blog/win-loss-battlecards-salesforce
- Klue Salesforce playbook — https://klue.com/salesforce
- Crayon — https://www.crayon.co/
- role.md → "Battlecard authoring playbook" + "Battlecard template" (this bundle)

## Related skills

- `kill-sheet-objection-rebuttals` — objection content per pane 2
- `win-loss-ci-integration-klue-insider` — feeds pane 3 latest deal intel
- `feature-parity-tracking` — pane 4 snapshot source
- `competitor-pricing-tier-comparison` — pane 5 source
- `ci-delivery-slack-crm-klue-insider` — Salesforce + Slack surface mechanics
- `hot-deals-ci-deal-level` — deal-specific micro-battlecard variant
