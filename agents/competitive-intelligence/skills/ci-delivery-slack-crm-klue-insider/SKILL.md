<!--
Sources: Klue Salesforce playbook https://klue.com/salesforce
         Klue × Salesforce blog https://klue.com/blog/the-salesforce-and-klue-playbook
         Crayon Sales App https://www.crayon.co/
         Klue Insider https://klue.com/insider
         Salesforce Lightning Components https://developer.salesforce.com/docs/component-library
Companion playbook: role.md → "Capability reference" → CI delivery channels + "Antipattern 4 — CI delivered only in Notion"
-->

# CI delivery (Slack + CRM + weekly digest — Klue Insider class)

Three delivery layers: (1) in-CRM cards — Klue Insider / Crayon Sales App embed inside the Salesforce opportunity record, or self-built Lightning component; (2) Slack channel for real-time competitor signals; (3) weekly digest email. Battlecards surface inside the opportunity record triggered by competitor field. Klue Insider, Crayon Sales App, Steve, northr, Insiteful all do this natively; self-build path works fully via Lightning + Slack + gmail-mcp.

## When to use

- "Where do the battlecards live?"
- "Wire CI delivery to reps"
- "Set up Slack hotline + Salesforce embed"
- New CI program kickoff — delivery layer setup
- Adoption-rate is below target — review delivery friction
- Migration from Notion-only delivery (Antipattern 4)

## When NOT to use

- Authoring the battlecards → use `battlecard-authoring-maintenance`
- Measuring delivery → use `ci-program-metrics-adoption-rate`
- Monitoring source signals → use `continuous-competitor-monitoring-klue-kompyte-crayon`

## Setup

```bash
# Klue Insider — Salesforce + Slack native apps
export KLUE_API_KEY="..."
export KLUE_API_BASE="https://api.klue.com/v1"

# Crayon Sales App — Salesforce + Slack
export CRAYON_API_KEY="..."

# Salesforce
export SF_USERNAME="..."
export SF_PASSWORD="..."
export SF_SECURITY_TOKEN="..."
export SF_INSTANCE_URL="https://your-instance.my.salesforce.com"

# Slack
export SLACK_BOT_TOKEN="xoxb-..."   # bot scope chat:write
export SLACK_HOTLINE_CHANNEL="#ci-hotline"
export SLACK_DIGEST_CHANNEL="#ci-digest"
export SLACK_LEADERSHIP_CHANNEL="#ci-leadership"

# Gmail for weekly digest
# (gmail-mcp auth)
```

MCPs in `agent.yaml`: `salesforce-api`, `slack-mcp`, `gmail-mcp`, `notion-mcp` (staging only), `linear-mcp` (CI program tickets).

## Common recipes

### Recipe 1: Klue Insider — install Salesforce app

Install from AppExchange ("Klue for Salesforce"). Configure:

```yaml
config:
  opportunity_competitor_field: Opportunity.Competitor__c
  surface: opportunity_record_page
  panes_shown: [positioning, objections, latest_deal_intel, pricing]
  open_logged_to_klue: true
```

### Recipe 2: Klue — Lightning component embed

```html
<!-- klue:battlecardPane attribute config -->
<klue:battlecardPane
  competitor="{!Opportunity.Competitor__c}"
  layout="compact"
  onOpen="{!logOpen}"
/>
```

### Recipe 3: Crayon Sales App — same shape, different vendor

```yaml
config:
  competitor_field: Opportunity.Competitor__c
  surface: opportunity_record_page
  panes: [overview, why_we_win, why_we_lose, latest_news]
```

### Recipe 4: Self-build Salesforce Lightning component

```javascript
// lwc/battlecardPane/battlecardPane.js
import { LightningElement, api, wire } from 'lwc';
import { getRecord } from 'lightning/uiRecordApi';
import getBattlecard from '@salesforce/apex/BattlecardController.getBattlecardByCompetitor';

export default class BattlecardPane extends LightningElement {
    @api recordId;
    competitor;
    battlecard;
    @wire(getRecord, { recordId: '$recordId', fields: ['Opportunity.Competitor__c'] })
    wiredRecord({ data }) {
        if (data) {
            this.competitor = data.fields.Competitor__c.value;
            getBattlecard({ competitor: this.competitor })
              .then(r => { this.battlecard = r; this.logOpen(); });
        }
    }
    logOpen() {
        // Activity record for analytics (Recipe 13 of ci-program-metrics-adoption-rate)
    }
}
```

### Recipe 5: Slack channel taxonomy

```yaml
channels:
  "#ci-hotline":      # hot signals — pricing change, exec move, M&A, analyst report drop
    audience: AEs + PMM + sales leaders
    cadence: real-time
    posting: bot only; people can react / thread
    retention: 90 days
  "#ci-digest":        # weekly digest summary
    audience: AEs + ICs
    cadence: weekly Friday 9am local
    posting: bot only
  "#ci-leadership":   # monthly program metrics + ROI
    audience: CRO + CMO + PMM lead + CI program manager
    cadence: monthly
    posting: bot only
  "#ci-pmm-staging": # PMM workspace
    audience: PMM
    cadence: real-time
```

### Recipe 6: Slack hot-signal block-kit message

```python
import requests
def post_hot_signal(competitor, signal_type, summary, source_url, battlecard_url=None):
    blocks = [
        {"type":"header","text":{"type":"plain_text","text":f"{competitor} • {signal_type}"}},
        {"type":"section","text":{"type":"mrkdwn","text":summary}},
        {"type":"context","elements":[
            {"type":"mrkdwn","text":f"<{source_url}|source>"
                                    + (f" • <{battlecard_url}|battlecard>" if battlecard_url else "")}
        ]},
    ]
    requests.post(SLACK_WEBHOOK_URL, json={"channel": SLACK_HOTLINE_CHANNEL, "blocks": blocks})
```

### Recipe 7: Weekly digest synthesis + Slack post

```python
def weekly_digest(week_of, signals, battlecard_updates, deal_intel):
    body = f"""*CI Weekly Digest — Week of {week_of}*

*TOP 5 COMPETITOR MOVES THIS WEEK*
{format_signals(signals)}

*BATTLECARD UPDATES*
{format_updates(battlecard_updates)}

*DEAL INTEL*
{format_deal_intel(deal_intel)}
"""
    requests.post(SLACK_WEBHOOK_URL, json={"channel": SLACK_DIGEST_CHANNEL, "text": body})
```

Use role.md "Weekly digest template" structure verbatim.

### Recipe 8: Weekly digest email via gmail-mcp

```python
from gmail_mcp import send
send(
    to=["sales-all@example.com"],
    cc=["pmm-lead@example.com"],
    subject=f"CI Weekly Digest — Week of {week_of}",
    body_html=render_html(digest_data),
)
```

### Recipe 9: Salesforce opportunity activity insert (auto-attach to deal)

```python
sf.Task.create({
    "Subject": f"CI Signal — {competitor}",
    "Description": signal_summary,
    "WhatId": opportunity_id,
    "Status": "Completed",
    "ActivityDate": today.isoformat(),
    "TaskSubtype": "Other",
})
```

### Recipe 10: Slack DM AE on competitor-flag deal

```python
def dm_ae_on_competitor_flag(opp_id, ae_slack_id, competitor, battlecard_url):
    requests.post(SLACK_WEBHOOK_URL, json={
        "channel": f"@{ae_slack_id}",
        "text": f":dart: Deal {opp_id} flagged as competing with *{competitor}*.\n"
                f"Battlecard: <{battlecard_url}>\nWeekly digest: <{digest_url}>"
    })
```

### Recipe 11: Refresh-on-signal cascade

```python
# When pricing change detected:
def on_pricing_diff(competitor, change):
    # 1. Flag battlecard pane 5 for refresh
    flag_battlecard(competitor, pane="pricing", reason="pricing_diff")
    # 2. Hot signal to #ci-hotline
    post_hot_signal(competitor, "PRICING CHANGE", summarize(change), change.source_url,
                    battlecard_url=bc_url(competitor))
    # 3. Linear ticket for PMM to refresh
    linear.issue_create(team_id=PMM_TEAM, title=f"Refresh {competitor} pricing pane",
                       description=change.diff)
```

### Recipe 12: Klue Insider Slack app native

Klue Insider's Slack app posts insights directly. Config:

```yaml
klue_slack_config:
  channel: "#ci-hotline"
  insight_types: [pricing_page_diff, changelog, exec_change, g2_review_batch]
  battlecard_link_inline: true
  alert_to_owner: true   # DM AE
```

### Recipe 13: Crayon Sales App — Slack + SF embed

```yaml
crayon_config:
  salesforce_embed_layout: opportunity_record_compact
  slack_app_channels: ["#ci-hotline","#ci-digest"]
  slack_dm_to_account_owner: true
```

### Recipe 14: Linear ticket auto-creation

```python
# CI program tickets — battlecard refreshes, kill-sheet PMM-approval queue
import requests
def create_ticket(title, description, team_id):
    requests.post("https://api.linear.app/graphql", headers={"Authorization": f"Bearer {LINEAR_API_KEY}"},
                  json={"query": "mutation($t:String!,$d:String!,$id:ID!){ issueCreate(input:{title:$t,description:$d,teamId:$id}){ issue { id url } } }",
                        "variables": {"t":title, "d":description, "id":team_id}})
```

### Recipe 15: Monthly leadership ROI post

```python
# Recipe 14 of ci-program-metrics-adoption-rate → monthly_snapshot
# Post to #ci-leadership with charts via Plotly export
```

## Examples

### Example 1: Wire Klue Insider end-to-end

**Goal:** All three delivery surfaces wired in 1 day.

**Steps:**
1. Recipe 1 → Install Klue Insider Salesforce app.
2. Recipe 2 → Add Lightning component to opportunity layout.
3. Recipe 12 → Klue Insider Slack app to `#ci-hotline`.
4. Recipe 7 + 8 → weekly digest Slack + email.
5. Recipe 10 → DM cascade on competitor-flag.

**Result:** Reps see battlecard inline in opportunity; hot signals in Slack; weekly digest in inbox.

### Example 2: Self-build delivery (no Klue / Crayon)

**Goal:** Run all 3 delivery layers without paid CI vendor.

**Steps:**
1. Recipe 4 → Lightning component reads custom Battlecard__c object.
2. Recipe 5-7 → Slack channel + hot signal + digest posting via Slack webhook.
3. Recipe 8 → gmail-mcp digest send.
4. Recipe 9 → SF activity records auto-attach.
5. Recipe 11 → refresh-on-signal cascade.

**Result:** Full delivery stack on $0 incremental cost.

### Example 3: Migrate from Notion-only (Antipattern 4 remediation)

**Goal:** Reps don't open Notion battlecards; move to Salesforce + Slack.

**Steps:**
1. Notion stays as staging only.
2. Recipes 2 + 4 → Lightning component reads canonical battlecards (from Klue or custom object).
3. Recipe 7 → Slack digest replaces "go check Notion" email.
4. Measure open-rate via `ci-program-metrics-adoption-rate` 60 days post-migration.

**Expected:** Open-rate 3-5x once delivery moves to where reps live.

### Example 4: Refresh-on-signal cascade — pricing diff

**Goal:** Acme pricing diff → battlecard refresh + Slack post + Linear ticket → all in <1 hour.

**Steps:**
1. `competitor-pricing-page-visualping-distill` Recipe 1 fires webhook on pricing diff.
2. Recipe 11 cascade.
3. Recipe 6 posts to `#ci-hotline`.
4. Recipe 14 opens Linear ticket for PMM.
5. PMM updates pane 5; Klue auto-refreshes embedded battlecard.

**Result:** End-to-end refresh cycle; rep sees updated pricing pane next time they open the opportunity.

## Edge cases / gotchas

- **Salesforce permissions** — Klue / Crayon app needs `View All Opportunities` for some panes. RevOps coordination.
- **Lightning component performance** — heavy panes slow record load; defer-load behind a toggle.
- **Slack channel overload** — too many hot signals → ignored. Threshold rules per role.md Step 6 quarterly S/N audit.
- **DM fatigue** — DMing AE on every competitor-flag deal annoys; 1 DM per opportunity per 7 days.
- **Bot user identity** — `CI Bot` user account; clear avatar; pinned channel description.
- **Slack threading** — let reps thread questions on hot signals; PMM watches threads for clarification needs.
- **Email-digest opt-out** — let reps opt out of email; some prefer Slack only.
- **Klue Slack app spend** — usually included in Klue seat; check tier.
- **Klue Insider rep license cost** — per-seat addition; not all reps need a full Klue seat if Lightning component reads via API.
- **Lightning component caching** — competitor field change should invalidate component cache.
- **No Notion as primary** — Antipattern 4. Notion = staging only; Salesforce + Slack = primary.
- **Field name collisions** — `Competitor__c` may already exist for legacy reasons; namespace as `CI_Competitor__c` if needed.
- **Multi-competitor deals** — opportunity may face 2-3 competitors; multi-pick field; Klue handles, custom needs design.
- **Channel access** — `#ci-hotline` is sales+PMM; `#ci-leadership` is exec-only; ACL.
- **Digest send time** — Friday 9am local per role.md; respect multi-timezone teams (multiple posts).
- **PROACTIVE.md scheduling** — Slack digest Friday 9am; Linear ticket creation real-time; monthly ROI 1st of month.
- **Provenance footer** — every hot signal + digest item includes source URL + retrieval date.

## Sources

- Klue Salesforce playbook — https://klue.com/salesforce
- Klue × Salesforce blog — https://klue.com/blog/the-salesforce-and-klue-playbook
- Klue Insider — https://klue.com/insider
- Crayon Sales App — https://www.crayon.co/
- Salesforce Lightning Web Components — https://developer.salesforce.com/docs/component-library
- Slack Block Kit Builder — https://app.slack.com/block-kit-builder/
- role.md → "Capability reference" → CI delivery channels + "Antipattern 4" + "Weekly digest template"

## Related skills

- `battlecard-authoring-maintenance` — content that flows through the delivery
- `ci-program-metrics-adoption-rate` — measure of delivery effectiveness
- `continuous-competitor-monitoring-klue-kompyte-crayon` — source of hot signals delivered here
- `hot-deals-ci-deal-level` — deal-level micro-battlecard delivered via this layer
- `ethical-public-source-methodology` — provenance footer per hot signal
