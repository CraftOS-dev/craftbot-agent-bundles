<!--
Source: https://help.churnzero.com/ + https://docs.vitally.io/reference + https://help.catalyst.io/ + https://help.gainsight.com/docs/journey-orchestrator/
-->
# Playbook Automation — ChurnZero Plays / Vitally Playbooks / Catalyst — SKILL

Codify if-this-then-that workflows in CSP platforms: health drop -> CSM outreach + Slack alert; milestone hit -> congrats email + advocacy invite; renewal-T90 -> kick off renewal prep flow. ChurnZero Plays, Vitally Playbooks, Catalyst Playbooks, Gainsight Journey Orchestrator. Free fallback: Python + Postgres state + CraftBot MCP orchestration.

## When to use

- **Create new playbook** — automate a manual CSM motion.
- **Audit existing playbooks** — quarterly review of what's running, hit rate, ROI.
- **Migrate between CSPs** — Vitally -> Catalyst, or build Python fallback when CSP not available.
- **A/B test playbook variants** — fire variant A vs B; compare conversion.
- **Add Slack alerting** — push CSP-fired events to Slack channel.
- **Free-fallback orchestration** — no CSP; build playbooks in Python + Postgres + agent MCPs.

This skill is the **orchestration layer** under most CS workflows. `customer-onboarding-day-0-90`, `renewal-management-90-day-prep`, `at-risk-identification-escalation`, `churn-save-motion-intervention` all use playbooks built/managed here.

Trigger phrases: "playbook", "ChurnZero play", "Vitally playbook", "Journey Orchestrator", "if-this-then-that", "automation workflow", "CS automation".

## Setup

```bash
# CSP playbook authoring
export VITALLY_SUBDOMAIN="acme"
export VITALLY_API_KEY="<key>"
export CATALYST_API_KEY="<key>"
export CHURNZERO_API_KEY="<key>"
export GAINSIGHT_DOMAIN="acme.gainsightcloud.com"
export GAINSIGHT_TOKEN="<key>"

# Totango (alt)
export TOTANGO_APP_TOKEN="<key>"

# Python fallback orchestration
# postgresql-mcp + slack-mcp + gmail-mcp + linear-mcp + notion-mcp all wired
```

Workspace prerequisites:
- Playbook taxonomy locked: NAME(trigger, audience, actions, exit, owner).
- Notion "Playbook Catalog" DB tracking every active playbook + hit rate.
- Playbook approval gate: CSM Lead approves new automated outreach paths.
- Postgres `playbook_executions` audit log: which customer, which playbook, fired when, completed when, outcome.

## Common playbook patterns

| Pattern | Trigger | Action | Owner |
|---|---|---|---|
| Welcome Day 0 | customer.created | Send welcome email + Pendo enroll | CSM |
| First-aha celebration | first_aha_event fired | Send celebration + Day 7 milestone close | CSM |
| At-risk Red | health_score < 0.4 | Slack #at-risk + Linear save-plan issue | CSM Lead |
| At-risk Yellow | health 30d decline > 0.1 | CSM weekly review queue ping | CSM |
| Promoter detected | NPS >= 9 | Trigger advocacy invite | CSM |
| Sponsor silent | sponsor not seen 30d | Multi-thread outreach | CSM Lead |
| Renewal T-90 | days_to_renewal = 90 | Risk classification + cadence kick | CSM |
| Renewal T-30 | days_to_renewal = 30 | PandaDoc draft + approval thread | CSM Lead |
| Anniversary | tenure_days % 365 = 0 | Congrats email + advocacy invite | CSM |
| Feature non-adoption | feature_X not used by Day 30 | Pendo nudge + email | CSM |

## Common recipes

### Recipe 1: Create Vitally Playbook

```bash
curl -sS -X POST "https://$VITALLY_SUBDOMAIN.rest.vitally.io/resources/playbooks" \
  -H "Authorization: Basic $(echo -n $VITALLY_API_KEY: | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "At-Risk Red Save Play",
    "trigger": {
      "field": "account.healthScore",
      "operator": "<",
      "value": 0.4,
      "duration": "persistent_24h"
    },
    "steps": [
      {"type": "create_task", "assignee": "account.csm",
       "title": "[At-Risk] {{account.name}}", "due_in_days": 1},
      {"type": "send_email", "template_id": "save-play-email-v1",
       "to": "account.exec_sponsor.email"},
      {"type": "post_slack", "channel": "#cs-at-risk",
       "template": "Account {{account.name}} crossed at-risk; save play armed."}
    ]
  }'
```

Doc: https://docs.vitally.io/reference/playbooks

### Recipe 2: Create Catalyst Playbook

```bash
curl -sS -X POST "https://api.catalyst.io/v1/playbooks" \
  -H "Authorization: Bearer $CATALYST_API_KEY" \
  -d '{
    "name": "Onboarding Day 0-90",
    "trigger": {"event": "company.created"},
    "milestones": [
      {"name": "Day 0 - Kickoff", "due_in_days": 0, "assignee_role": "csm"},
      {"name": "Day 7 - First Value", "due_in_days": 7, "assignee_role": "customer"},
      {"name": "Day 30 - Activation", "due_in_days": 30, "assignee_role": "customer"}
    ]
  }'
```

Doc: https://help.catalyst.io/

### Recipe 3: Create ChurnZero Play

```bash
# ChurnZero Plays config via Plays API
curl -sS -X POST "https://api.churnzero.net/i/v1/plays" \
  -H "Authorization: Bearer $CHURNZERO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sponsor Silent Multi-Thread",
    "trigger": {
      "type": "attribute_change",
      "attribute": "sponsor_last_seen_days",
      "operator": ">",
      "value": 30
    },
    "actions": [
      {"type": "email", "template": "multi-thread-outreach", "recipient": "csm_lead"},
      {"type": "task", "assignee": "csm", "due": "+2d",
       "description": "Multi-thread {{account.name}}"}
    ]
  }'
```

Doc: https://help.churnzero.com/

### Recipe 4: Create Gainsight Journey Orchestrator program

Gainsight JO uses Rules + Programs; most setup happens in UI but program enrollment is API-able:

```bash
curl -sS -X POST "https://$GAINSIGHT_DOMAIN/v1/api/journey/program/$PROGRAM_ID/participants" \
  -H "accesskey: $GAINSIGHT_TOKEN" \
  -d '{"company_id": "'$CUSTOMER_ID'", "person_id": "'$SPONSOR_ID'"}'
```

Doc: https://help.gainsight.com/docs/journey-orchestrator/

### Recipe 5: Free fallback - Python playbook orchestrator

```python
# playbook_engine.py
import psycopg2
from datetime import datetime, timedelta

class Playbook:
    def __init__(self, name, trigger_fn, action_fns, audience_fn=None):
        self.name = name
        self.trigger_fn = trigger_fn
        self.audience_fn = audience_fn
        self.action_fns = action_fns

    def evaluate_and_fire(self):
        candidates = self.audience_fn() if self.audience_fn else postgres.query("SELECT customer_id FROM customers WHERE status='active'")
        for c in candidates:
            if self.trigger_fn(c):
                # Idempotency check
                if not playbook_already_fired(c.customer_id, self.name):
                    for action in self.action_fns:
                        action(c)
                    log_execution(c.customer_id, self.name)

# Example: at-risk Red playbook
def trigger_atrisk_red(customer):
    return get_health(customer.customer_id) < 0.4

def action_create_save_plan(customer):
    notion.create_page(...)  # Notion save plan

def action_slack_alert(customer):
    slack.chat_postMessage(channel="#cs-at-risk", text=...)

def action_create_linear_issue(customer):
    linear.create_issue(...)

p = Playbook(
    name="atrisk_red_save_play",
    trigger_fn=trigger_atrisk_red,
    action_fns=[action_create_save_plan, action_slack_alert, action_create_linear_issue],
)
p.evaluate_and_fire()
```

Run nightly via cron.

### Recipe 6: Playbook execution audit log

```sql
CREATE TABLE playbook_executions (
  id serial PRIMARY KEY,
  playbook_name text NOT NULL,
  customer_id text NOT NULL,
  fired_at timestamptz DEFAULT now(),
  actions_executed jsonb,
  outcome text,
  outcome_set_at timestamptz
);

CREATE INDEX idx_pe_customer ON playbook_executions(customer_id);
CREATE INDEX idx_pe_playbook ON playbook_executions(playbook_name);
```

Idempotency: don't fire same playbook for same customer within cooldown window.

### Recipe 7: Idempotency check

```sql
SELECT count(*) FROM playbook_executions
WHERE playbook_name = '$NAME'
  AND customer_id = '$CUSTOMER_ID'
  AND fired_at >= now() - INTERVAL '7 days';
```

If > 0, skip. (Cooldown is per-playbook; default 7d.)

### Recipe 8: Slack alerting from CSP webhooks

For Vitally fired actions: configure webhook in Vitally UI -> CraftBot endpoint -> forward to Slack via `slack-mcp`.

```python
# Webhook handler
@app.route("/webhook/vitally", methods=["POST"])
def vitally_webhook():
    event = request.json
    if event["type"] == "playbook_action_fired":
        slack.chat_postMessage(
            channel=event["meta"]["slack_channel"],
            text=event["template_rendered"],
        )
```

### Recipe 9: Playbook hit rate / conversion measurement

```sql
SELECT
  playbook_name,
  count(*) AS fired,
  count(*) FILTER (WHERE outcome = 'recovered') AS recovered,
  count(*) FILTER (WHERE outcome = 'churned') AS churned,
  count(*) FILTER (WHERE outcome IS NULL) AS in_flight,
  100.0 * count(*) FILTER (WHERE outcome = 'recovered') / nullif(count(*) FILTER (WHERE outcome IS NOT NULL), 0) AS recovery_pct
FROM playbook_executions
WHERE fired_at >= now() - INTERVAL '90 days'
GROUP BY playbook_name
ORDER BY recovery_pct DESC;
```

Quarterly playbook ROI review.

### Recipe 10: Playbook catalog audit

```python
# Pull all playbooks from each CSP, write to Notion catalog
vitally_pbks = curl_get("https://$VITALLY/playbooks")
catalyst_pbks = curl_get("https://api.catalyst.io/v1/playbooks")

for p in vitally_pbks + catalyst_pbks:
    notion.create_or_update_page(
        parent={"database_id": PLAYBOOK_CATALOG_DB_ID},
        properties={
            "Name": {"title": [{"text": {"content": p.name}}]},
            "Source": {"select": {"name": p.source}},
            "Trigger": {"rich_text": [{"text": {"content": str(p.trigger)}}]},
            "Last Modified": {"date": {"start": p.modified_at}},
            "Hit Rate 90d": {"number": p.hit_rate},
            "Status": {"status": {"name": p.status}},
        },
    )
```

### Recipe 11: Disable / re-enable playbook

```bash
# Vitally
curl -sS -X PATCH "https://$VITALLY/playbooks/$PBK_ID" \
  -d '{"state": "disabled"}'
```

When a playbook misfires (e.g., wrong audience), disable + investigate before edits.

### Recipe 12: A/B test playbook variants

```python
def trigger_at_risk_red_a(customer):
    if hash(customer.customer_id) % 2 == 0 and get_health(customer.customer_id) < 0.4:
        return True
    return False

def trigger_at_risk_red_b(customer):
    if hash(customer.customer_id) % 2 == 1 and get_health(customer.customer_id) < 0.4:
        return True
    return False

# Variant A: standard save plan
# Variant B: save plan + immediate exec call ask

# 14 days; compare recovery_pct
```

## Examples

### Example 1: Stand up Vitally Playbook for at-risk Red

**Goal:** Migrate manual at-risk motion to automated playbook in Vitally.

**Steps:**
1. Document current motion: CSM Lead pings CSM, save plan created in Notion, Slack alert, Linear issue.
2. Recipe 1 - create Playbook in Vitally. 4 steps: task, email, Slack, Linear webhook.
3. Test on 1 staged customer; verify all fire.
4. Enable for production. Recipe 10 - log in catalog.
5. Recipe 9 - 30d check: how many fires, recovery rate.

**Result:** Manual motion automated; CSM Lead's time saved 5h/week.

### Example 2: Free-fallback Python orchestrator end-to-end

**Goal:** No CSP; build at-risk Red playbook in Python.

**Steps:**
1. Recipe 5 implement Playbook class.
2. Define `trigger_atrisk_red(customer)` using Postgres `health_scores` view.
3. Define actions: Notion save plan, Slack alert, Linear issue.
4. Recipe 6 audit log table.
5. Cron nightly 03:00 UTC; Recipe 7 idempotency gate.
6. Recipe 9 weekly review of fires + outcomes.

**Result:** CSP-free orchestration with full auditability.

## Edge cases / gotchas

- **Playbook misfire = trust damage** — if a Yellow account gets a Red save play email, customer is alarmed. Verify trigger logic thoroughly.
- **Idempotency violation** — playbook fires twice in same week = duplicate Slack + duplicate email. Recipe 7 gate is mandatory.
- **Webhook delivery failures** — Vitally webhooks can drop on transient network errors. Use retry queue or polling fallback.
- **CSP playbook UI vs API state drift** — admin edits in UI; API state shows old config. Force `Recipe 11 then Recipe 1` cycle for changes.
- **Stale audience filter** — playbook fires on trait that's not updated. Verify trait freshness before triggering.
- **Recovery rate doesn't equal save rate** — playbook may fire and customer recovers without intervention. Measure causally if possible (control group).
- **Permissions** — CSP API keys have admin scope. Rotate annually; audit usage quarterly.
- **Cross-CSP migration drift** — Vitally Playbook expressions != Catalyst syntax; re-author from scratch when migrating.
- **Email fatigue from playbook stack** — Day 0 welcome + Day 7 nudge + Day 14 detractor-recovery + Day 21 expansion = customer's inbox full. Coordinate via Notion send log.
- **Playbook scope creep** — start with 3 actions, end up with 15. Cap at 5 actions per playbook; chain via additional playbooks if needed.
- **A/B test sample size** — < 100 fires/variant = noisy. Run 30-60 days.
- **Disabling a live playbook** — customers mid-flow when disabled = abandoned. Add "graceful drain" mode (no new enrollments; existing complete).

## Sources

- [Vitally Playbooks docs](https://docs.vitally.io/reference/playbooks)
- [Vitally REST API](https://docs.vitally.io/reference)
- [ChurnZero Plays](https://help.churnzero.com/)
- [Catalyst Playbooks](https://help.catalyst.io/)
- [Gainsight Journey Orchestrator](https://help.gainsight.com/docs/journey-orchestrator/)
- [Gainsight Rules Engine](https://support.gainsight.com/gainsight_nxt/Rules_Engine)
- [Totango docs API](https://www.totango.com/docs/api)
- [Custify automation](https://docs.custify.com/)
- [Webhook retry patterns (Stripe blog)](https://stripe.com/blog/idempotency)
