---
name: document-workflow-routing-approval
description: Orchestrate multi-stage approval routing for documents — legal → finance → exec → counterparty sign — using native CLM/e-sign workflows (PandaDoc, DocuSign, Ironclad) or external orchestrators (n8n, Zapier, Make.com). Slack/Teams in-message approvals, conditional routing, audit logging. Use when the user says "approval workflow", "route for review", "multi-stage signoff", "n8n workflow", "Slack approval", "approval routing".
---

# Document workflow routing + approval — n8n / native CLM / Slack-approval

This skill ships the orchestration layer between document generation and execution. The doc-gen tool produces the artifact; this skill routes it through human / system approval before the counterparty ever sees it.

## When to use

User says:

- "Route this contract through legal → finance → CEO → sign"
- "Add an approval step before send"
- "n8n / Zapier / Make.com workflow for docs"
- "Slack approval message"
- "Approve-by-emoji"
- "Conditional approval (skip legal if deal < $50K)"
- "Approval SLA / escalation"

Companion skills:
- `e-signature-docusign-adobe-sign-pandadoc` — execution step at end of workflow.
- `audit-trail-e-sign-versioning` — preserve approval audit trail.
- `clm-ironclad-contractworks-integration` — when CLM owns the workflow.
- `document-analytics-time-to-sign` — measure workflow throughput.

## Setup

```bash
# n8n (open-source workflow automation)
npm install -g n8n
# or Docker: docker run -it --rm -p 5678:5678 n8nio/n8n
# Self-host or cloud — n8n.io

# Zapier — no install; web-only
# Required env: ZAPIER_NLA_API_KEY (for AI Actions API integration)

# Make.com (formerly Integromat) — no install
# Web-only; API key for direct REST

# Slack Block Kit (for approval messages)
# Default skill: slack-mcp — install scopes chat:write, im:write, files:read
pip install slack_sdk

# Microsoft Teams
# Default skill: ms-teams-mcp

# Linear / Jira for approval-as-task pattern
# Default skills: linear-mcp / jira-mcp
```

## Common recipes

### Recipe 1: Pick the orchestrator

| Orchestrator | Best for | Pricing | Notes |
|---|---|---|---|
| n8n | Self-host + complex logic + open-source | Free (self-host) / $20+/mo cloud | JS-native; fair-code license |
| Zapier | SaaS-glue + simple steps | $20-799/mo | Largest connector library |
| Make.com | Visual + medium complexity | $9-29/mo | Stronger logic than Zapier |
| PandaDoc native workflow | If PandaDoc is source-of-truth | Bundled | UI-native approval |
| DocuSign Connect + Apex Flows | DocuSign-led shop | DocuSign tier | Multi-stage routing built in |
| Ironclad workflow | Ironclad CLM customers | Bundled | Best-in-class for contract routing |
| Slack Workflow Builder | Trivial approvals | Free | No code; limited |
| Native CLM | If CLM ships approval | Bundled | Don't reinvent if CLM has it |

Default: native CLM workflow if present; else n8n for self-host; else Zapier/Make.com for quick wins.

### Recipe 2: n8n — install + first workflow scaffold

```bash
# Self-host (Docker)
docker run -d --restart unless-stopped \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=changeme \
  -e WEBHOOK_URL=https://n8n.yourdomain.com \
  n8nio/n8n:latest
```

Workflow: Webhook → If (deal_value > 50000) → Slack approval block → Wait for response → POST DocuSign envelope.

### Recipe 3: Slack approval message (Block Kit)

```python
from slack_sdk import WebClient
client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

blocks = [
    {"type": "header", "text": {"type": "plain_text", "text": "Approval needed: Acme MSA"}},
    {"type": "section", "text": {"type": "mrkdwn",
        "text": f"*Deal:* Acme - $240K\n*Counterparty:* Acme Corp\n*Term:* 36 months\n*Drafted by:* @rep.smith"}},
    {"type": "section", "text": {"type": "mrkdwn",
        "text": "<https://docs.googleapis.com/.../msa-acme-draft.pdf|View draft>"}},
    {"type": "actions", "elements": [
        {"type": "button", "text": {"type": "plain_text", "text": "Approve"},
         "style": "primary", "value": "approve:env_abc123",
         "action_id": "msa_approve"},
        {"type": "button", "text": {"type": "plain_text", "text": "Reject"},
         "style": "danger", "value": "reject:env_abc123",
         "action_id": "msa_reject"},
        {"type": "button", "text": {"type": "plain_text", "text": "Request changes"},
         "value": "redline:env_abc123",
         "action_id": "msa_redline"},
    ]}
]
client.chat_postMessage(channel="C0000LEGAL", blocks=blocks, text="Approval needed")
```

### Recipe 4: Slack interaction handler (Approve → trigger send)

```python
# Receive at /slack/interactivity
@app.post("/slack/interactivity")
async def slack_interactivity(req: Request):
    payload = json.loads((await req.form())["payload"])
    if payload["type"] == "block_actions":
        action = payload["actions"][0]
        kind, envelope_id = action["value"].split(":")
        user = payload["user"]["id"]
        if kind == "approve":
            # Update message to show "Approved by @user at <ts>"
            client.chat_update(
                channel=payload["channel"]["id"],
                ts=payload["message"]["ts"],
                text=f"✓ Approved by <@{user}>",
                blocks=[]
            )
            # Trigger DocuSign send
            send_envelope(envelope_id)
            # Log to audit trail
            log_approval(envelope_id, user, "approve")
        elif kind == "reject":
            ...
    return {"ok": True}
```

### Recipe 5: Conditional routing (deal-value-based skip)

```text
n8n flow:
  Webhook → Set { deal_value }
  ↓
  IF deal_value < 50000:    # auto-route to send
    → DocuSign Send node
  ELSE:                      # legal approval needed
    → Slack Approval (Recipe 3)
    → Wait
    → If approved:
        IF deal_value > 250000:    # also finance approval
          → Slack Approval (Finance channel)
          → Wait
          → If approved: DocuSign Send
        ELSE: DocuSign Send
```

### Recipe 6: Approval-as-task in Linear

```python
import requests
def create_approval_task(deal_id, value, draft_url):
    r = requests.post(
        "https://api.linear.app/graphql",
        headers={"Authorization": os.environ["LINEAR_API_KEY"]},
        json={"query": """
        mutation($input: IssueCreateInput!) {
          issueCreate(input: $input) { success issue { id url } }
        }""",
        "variables": {"input": {
            "teamId": "<LEGAL_TEAM_ID>",
            "title": f"Approve: MSA for deal {deal_id} (${value:,})",
            "description": f"Draft: {draft_url}\n\nApprove or comment with redlines.",
            "labelIds": ["<LEGAL_LABEL_ID>"],
            "stateId": "<TRIAGE_STATE_ID>"
        }}}
    )
    return r.json()["data"]["issueCreate"]["issue"]["url"]
```

Watch the issue for state change to "Done" → trigger send.

### Recipe 7: PandaDoc native approval workflow

In PandaDoc → Templates → Approval Workflow → Add Step:
1. Step 1: Sales rep submits draft.
2. Step 2: Legal team (group) — approver = role.
3. Step 3: Finance — approver = role; conditional on $ threshold.
4. Step 4: VP Sales — final go.
5. Step 5: Send to recipient for signature.

PandaDoc tracks approvals per template; downstream events available via webhook.

### Recipe 8: DocuSign approval via routing

In DocuSign, set recipient with `recipient_type=signer + signer_role="Approve"` + use `routing_order` to enforce sequence.

```python
# Recipient that approves but doesn't sign
Signer(
    email="legal@widgetco.com",
    name="Legal Team",
    recipient_id="1",
    routing_order="1",
    recipient_type="approval",   # approval only — no signature tabs
)
```

Internal approver clicks Approve in DocuSign → flows to next recipient.

### Recipe 9: Escalation on SLA breach

```text
n8n flow:
  Slack Approval → Wait (max 24h)
  → IF not approved within 24h:
      → Send Slack DM to manager + post in #legal-escalations
      → Wait again (max 24h)
      → IF still no response:
          → Auto-escalate to General Counsel
          → Log in audit trail
```

### Recipe 10: Audit log every approval event

```python
# After every approval / rejection / change-request
{
  "envelope_id": "env_abc123",
  "event": "approve",            # or reject / redline / escalate
  "actor_email": "legal@widgetco.com",
  "actor_role": "Legal Approver",
  "timestamp": "2026-06-15T14:32:11Z",
  "channel": "slack",            # or email / linear / docusign
  "comment": "Standard terms; cleared.",
  "deal_value": 240000,
  "stage": "Legal Review",
  "draft_sha256": "abc...",      # hash of doc at approval time
}
```

Store in Google Sheet / Notion DB / Postgres for compliance.

### Recipe 11: Microsoft Teams approval

```python
# Teams Adaptive Card with Approve/Reject buttons
import requests
card = {
    "type": "AdaptiveCard",
    "version": "1.5",
    "body": [
        {"type": "TextBlock", "text": "Approval needed: Acme MSA", "size": "large"},
        {"type": "TextBlock", "text": "Deal: Acme - $240K"},
    ],
    "actions": [
        {"type": "Action.Http", "title": "Approve", "method": "POST",
         "url": "https://your-app/approve",
         "body": '{"envelope_id":"env_abc123","actor":"{{userPrincipalName}}"}'},
    ]
}
requests.post(TEAMS_WEBHOOK_URL, json={"type":"message","attachments":[{
    "contentType":"application/vnd.microsoft.card.adaptive",
    "content": card}]})
```

### Recipe 12: Email-only approval (no Slack/Teams)

```python
# Send email with magic-link approval
approval_token = jwt.encode({"envelope_id":"env_abc123","actor":"legal@widgetco.com","exp":time.time()+86400}, SECRET, algorithm="HS256")
send_email(
    to="legal@widgetco.com",
    subject="Approval needed: Acme MSA",
    html=f'<a href="https://your-app/approve?token={approval_token}">Approve</a>'
)
```

## Examples

### Example 1: Tiered routing — under $50K skip legal, over $250K add CFO

**Goal:** Speed up small deals; add scrutiny on large ones.
**Steps:**
1. PandaDoc renders proposal (`proposal-automation-pandadoc-proposify-qwilr`).
2. n8n webhook fired (Recipe 2).
3. Recipe 5 — conditional logic per value.
4. Recipe 3 — Slack channels: #legal-approvals / #finance-approvals.
5. On all approvals received → DocuSign send.
6. Recipe 10 — every event logged.

**Result:** Deals < $50K close in hours; > $250K get exec scrutiny.

### Example 2: 24h SLA escalation

**Goal:** Approvals stop slipping.
**Steps:**
1. Recipe 6 — Linear issue created.
2. Recipe 9 — n8n watches issue age.
3. On 24h: DM the manager.
4. On 48h: page general counsel.

**Result:** Average approval time drops 50%.

### Example 3: Quarterly compliance audit ready in 5 minutes

**Goal:** Auditor asks "show every approval for Q2 MSAs".
**Steps:**
1. Recipe 10 — Postgres rows queried by stage = "Legal Review" + envelope.completed BETWEEN 2026-04-01 AND 2026-06-30.
2. Export as CSV with hash + actor + timestamp.

**Result:** Auditor satisfied without scrambling email threads.

## Edge cases / gotchas

- **Slack interactivity URL must be HTTPS + replied within 3 seconds.** Do heavy work async; respond immediately with `200 OK + replace_original`.
- **Signature verification on every webhook.** Slack: `X-Slack-Signature`; PandaDoc / DocuSign: HMAC headers — validate or replay attacks possible.
- **Approval token TTL.** Magic links / emoji-approvals must expire (max 24-72h); track + invalidate.
- **Approver identity matters.** Authentic approval = SSO-authenticated user; email-link is weakest evidence.
- **Concurrent approvals.** Race conditions — two approvers click simultaneously; lock state at first click.
- **PandaDoc workflow blocks send.** If template has workflow + you try to send without approval, API returns 403; pull workflow before send.
- **DocuSign approval recipient counts as a signer slot.** Counts against bulk limits; design recipient sequence carefully.
- **n8n cron + webhook persistence.** On Docker restart, in-flight executions can be lost — persist execution data to Postgres.
- **Zapier task limits.** Zapier counts every step as a task; high-fan-out flows blow through quotas — use Make.com / n8n for high-volume.
- **Approval bypass.** Always log the bypass case (e.g., "Emergency exec approval"); never silently skip.
- **Sensitive content in Slack messages.** Don't paste contract clauses; link to the doc only. Slack messages may persist in mobile clients.
- **Re-approval after redline.** If the doc changes, prior approval should be voided (track doc SHA-256).
- **Approval audit chain integrity.** Hash each event with prior event SHA → tamper-evident chain.
- **Notification fatigue.** Bundle approvals per approver (daily digest) when volume is high.
- **Compliance overlay (SOX / 21 CFR Part 11).** Regulated industries require dual-control; build that into Recipe 5.

## Sources

- [n8n docs](https://docs.n8n.io/) — workflow nodes + webhooks.
- [Zapier developer](https://platform.zapier.com/docs/welcome) — Zapier Platform CLI.
- [Make.com docs](https://www.make.com/en/help) — scenarios + filters.
- [Slack Block Kit](https://api.slack.com/block-kit) — approval-message blocks.
- [Slack Interactivity docs](https://api.slack.com/interactivity/handling) — handle button clicks.
- [Microsoft Teams Adaptive Cards](https://learn.microsoft.com/en-us/microsoftteams/platform/task-modules-and-cards/cards/cards-reference) — Teams equivalent.
- [PandaDoc Approval workflow](https://support.pandadoc.com/hc/en-us/articles/360011425933-Approval-Workflow) — native approval.
- [DocuSign Routing Order](https://support.docusign.com/s/document-item?language=en_US&bundleId=jux1643235969954) — recipient routing.
- [Linear API](https://developers.linear.app/docs) — issue create / state.
- Sister skills: `e-signature-docusign-adobe-sign-pandadoc`, `audit-trail-e-sign-versioning`, `clm-ironclad-contractworks-integration`, `document-analytics-time-to-sign`.
