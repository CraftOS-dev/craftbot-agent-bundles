<!--
Source: https://www.theempiremag.com/the-ceo-playbook-2026/
Crisis comms playbook: 5 archetypes + holding statements + cascade
-->
# Crisis Communication Playbook

5 archetypes (security breach / executive departure / product outage / layoffs / regulatory action). Each with: holding-statement template (60-min target), stakeholder cascade (customers → employees → investors → regulators → press), 24h-48h-7day cadence, single spokesperson rule. Document and rehearse BEFORE you need it.

## When to use

- Active crisis — need a holding statement in <60 min.
- Pre-crisis rehearsal — annual tabletop exercise.
- Post-crisis post-mortem.
- Onboarding leadership team on the playbook.

Trigger phrases: "crisis comms", "breach response", "outage statement", "layoff comms", "regulatory action", "holding statement", "tabletop exercise".

## Setup

```bash
# Notion as playbook source-of-record
mcp tool notion.search --query "Crisis playbook"

# Slack + email for cascade
mcp tool slack.list_channels --search "incident"
mcp tool gmail.list_labels --search "crisis"
```

Auth / API key requirements:
- `NOTION_API_KEY` — for playbook + drafted statements DB.
- `SLACK_API_TOKEN` — internal cascade scope `chat:write` + `channels:read`.
- `GOOGLE_OAUTH_TOKEN` — for emergency board email.
- `STATUSPAGE_API_KEY` — for public outage page (Statuspage / Better Stack / etc.).

## Common recipes

### Recipe 1: 5 archetype routing

```markdown
| Crisis | Speed | Cascade | DRI |
|---|---|---|---|
| Security breach | <60 min holding | Customers → Employees → Investors → Regulators → Press | CEO or CISO |
| Executive departure | Same-day | Board → Employees → Investors → Customers | CEO |
| Product outage | <30 min status page | Customers → Employees → Investors | Eng lead |
| Layoffs | Coordinated day-of | Affected employees → All employees → Customers → Investors | CEO + HR |
| Regulatory action | Per legal counsel | Legal-counsel guidance → Customers → Investors → Press | CEO + Legal |
```

### Recipe 2: Holding statement — Security breach

```markdown
# [DRAFT — fill, review with legal-counsel, send]

We've identified a [scope] security incident at [time, with timezone].

Initial assessment: [N] customers may be affected. [Type of data potentially exposed].

Immediate actions we've taken:
- [Containment step 1 — e.g., rotated affected credentials]
- [Containment step 2 — e.g., isolated affected systems]
- [Investigation step — e.g., engaged [external IR firm]]

We will provide an update by [time, no more than 4h out].

For affected customers: [specific action / link to dedicated incident page].

Contact: security@[domain].com or [DRI by name].

— [CEO name + title]
```

### Recipe 3: Holding statement — Executive departure

```markdown
[Name] is departing the company effective [date]. We are grateful for [specific contribution — naming 1 thing keeps it real].

[Successor named OR interim arrangement detailed].

Customer impact: [none / specific].
Investor impact: [board notification status].
Team impact: [reporting line changes].

[Optional, if amicable: brief warm closing.]

— [CEO name]
```

### Recipe 4: Holding statement — Product outage

```markdown
We're experiencing [scope] outage affecting [feature/service] since [time].

We are actively investigating. [Workaround if available, otherwise: "There is no workaround yet — we're working on it."]

Updates every [15/30/60 min] at [status page URL].

We're sorry for the disruption.

— [On-call eng lead]
```

### Recipe 5: Holding statement — Layoffs

```markdown
Today we're reducing [X] roles, approximately [Y%] of the company, focused on [areas].

[Reason — be honest, not corporate. Examples: "We over-hired against an optimistic plan that didn't materialize." NOT: "We're optimizing for efficiency."]

Severance for affected employees:
- [N weeks] of pay
- [Benefits continuation]
- [Outplacement support]
- [Equity acceleration if applicable]

Process: [when, how, support — example: "Affected employees will hear from their manager today between 10am-12pm PT. All-hands at 1pm PT to discuss with the whole company."]

For remaining employees: [what changes, what doesn't — example: "Reporting lines unchanged. Q3 roadmap unchanged. We have [N] months runway."]

Customer commitments: [unchanged with specifics].

— [CEO name]
```

### Recipe 6: Holding statement — Regulatory action

```markdown
[Authority] has [action — e.g., issued a subpoena / opened an inquiry / filed a complaint] regarding [topic].

We are [cooperating fully / contesting / [specific posture]].

Our customers: [specific impact assessment — likely "no impact to service" or "specific guidance for affected segment"].

Our position: [brief, factual, legally-cleared].

Legal counsel: [firm name + practice lead].

We will update [specific stakeholder] by [specific date].

— [CEO name]
```

### Recipe 7: Cascade order (60-min holding, then full)

```markdown
## Cascade order

| Order | Audience | Channel | Time |
|---|---|---|---|
| 1 | Affected customers | Email + status page + in-app banner | 60 min |
| 2 | All employees | Slack #incident channel + email | 60-120 min |
| 3 | Investors + board | Email to board + investor distro | Same day |
| 4 | Regulators | Per legal-counsel | Per legal timeline |
| 5 | Press | After above; single spokesperson | After internal cascade complete |

Rule: never reverse order. Press before customers = trust collapse.
```

### Recipe 8: Tabletop rehearsal (annual)

```markdown
## Crisis tabletop — annual

Schedule: 2h offsite, leadership team + legal counsel.

Pick 1 archetype (rotate annually):
- Year 1: Security breach
- Year 2: Product outage
- Year 3: Executive departure
- Year 4: Regulatory
- Year 5: Layoffs

For chosen archetype:
1. **Inject** (10 min) — facilitator presents scenario
2. **First 60 min** (30 min) — team drafts holding statement under time pressure
3. **Cascade** (20 min) — practice cascade order, identify failure points
4. **Critique** (30 min) — what worked, what didn't
5. **Update playbook** (30 min) — refresh templates with learnings

Tabletop output: refreshed playbook + identified gaps in tooling / contacts / authority.
```

### Recipe 9: Playbook DB schema

```bash
mcp tool notion.create_database \
  --parent '{"page_id":"<crisis-hub>"}' \
  --title '[{"text":{"content":"Crisis Playbook"}}]' \
  --properties '{
    "Archetype":{"select":{"options":[{"name":"Security breach"},{"name":"Executive departure"},{"name":"Product outage"},{"name":"Layoffs"},{"name":"Regulatory"}]}},
    "Holding template":{"rich_text":{}},
    "Cascade order":{"rich_text":{}},
    "DRI":{"people":{}},
    "Single spokesperson":{"people":{}},
    "Last rehearsed":{"date":{}},
    "Last activated":{"date":{}}
  }'
```

### Recipe 10: Active-crisis workflow

```bash
# Step 1: Spin up incident channel
mcp tool slack.create_channel --name "incident-2027-04-08-security" --private true

# Step 2: Invite DRIs only
mcp tool slack.invite_to_channel --channel "incident-2027-04-08-security" \
  --users "ceo,ciso,legal-counsel,head-of-eng,head-of-comms"

# Step 3: Pin holding statement template from Notion
mcp tool slack.send --channel "incident-2027-04-08-security" --message \
  "Pinning archetype: SECURITY BREACH. Holding template: [Notion link]. Single spokesperson: CISO. Comms cadence: 4h. Status page: [link]."

# Step 4: Draft holding statement
mcp tool notion.create_page \
  --parent '{"page_id":"<crisis-active>"}' \
  --properties '{"title":[{"text":{"content":"Active: 2027-04-08 Security"}}]}' \
  --children-template ./security-breach-template.md
```

### Recipe 11: Post-crisis post-mortem (2 weeks after resolution)

```markdown
## Post-mortem template

### Timeline (objective, with timestamps)
- [HH:MM] Incident started
- [HH:MM] Detection
- [HH:MM] Holding statement sent
- [HH:MM] Customer cascade complete
- [HH:MM] Resolved

### What worked
- [...]

### What didn't
- [...]

### Root cause (5 whys)
- [...]

### Action items
| Action | Owner | Due |
|---|---|---|
| ... | ... | ... |

### Playbook updates
- [What in the playbook will change]
```

### Recipe 12: Single-spokesperson rule

```markdown
## Single spokesperson — enforce

Rule: ONE voice externally. CEO or designated DRI. Not 2 VPs giving different stories.

Enforce by:
1. Update Slack incident channel topic: "ONLY [name] speaks externally. All inquiries → [name]."
2. Press queue: route all media inquiries to comms DRI.
3. Customer-facing: pre-vetted statements only. CS team uses copy/paste; doesn't improvise.
4. Internal cascade: leadership repeats CEO message verbatim. No "I personally think..."

If second voice emerges, CEO addresses immediately in incident channel.
```

## Examples

### Example 1: Security breach — first 60 min

**Goal:** Identified breach 0:00. Holding statement out by 1:00.

**Steps:**
1. **0:00-0:05** Spin up incident channel (Recipe 10).
2. **0:05-0:15** Engage IR firm. Containment in progress.
3. **0:15-0:30** Draft holding statement (Recipe 2). Legal-counsel review.
4. **0:30-0:45** Status page update. Affected-customer email queued.
5. **0:45-0:55** Final legal review.
6. **0:55-1:00** SEND in cascade order (Recipe 7).
7. **1:00-1:15** Internal Slack cascade. Investors emailed.
8. **+4h** Full update. Cadence continues.

**Result:** Trust preserved by speed + honesty.

### Example 2: Layoffs — coordinated day-of

**Goal:** 15% reduction; need clean execution.

**Steps:**
1. T-2 weeks: legal counsel + operations-agent prep severance + offer letters.
2. T-1 week: CEO drafts holding statement (Recipe 5). Board notified.
3. T-day:
   - 9:00 — affected employees' managers notified.
   - 10:00-12:00 — 1:1 conversations with affected employees.
   - 12:00 — public statement live.
   - 13:00 — all-hands for remaining employees.
4. T+1 day — customer email reassurance.
5. T+1 week — post-mortem (Recipe 11).

**Result:** Clean execution; remaining team has clarity.

## Edge cases / gotchas

- **Speed > polish.** 60-min imperfect holding statement > 6h perfect one. Trust correlates with speed.
- **No second voice externally.** "I personally think..." from a VP undermines CEO. Educate. Enforce in incident channel.
- **Lowlights mandatory.** Hiding the bad makes the story worse. Be specific.
- **Don't speculate.** "We don't know yet" is acceptable; making things up is not. Trust dies on retracted claims.
- **Cascade order non-negotiable.** Customers first. Press last. Reversal = trust collapse.
- **Status page MUST exist before crisis.** Statuspage / Better Stack / Atlassian Statuspage. Provision now.
- **Legal-counsel involvement.** Every external statement reviewed before send. Build the relationship pre-crisis.
- **D&O insurance check.** Confirm crisis events are covered before crisis. Embroker / Founder Shield etc.
- **Internal cascade timing.** Employees should NOT first hear from press. Cascade order has internal #2 right after external #1.
- **Customer notification GDPR.** EU residents = 72h GDPR notification clock for breaches. Build the address book by region.
- **Single spokesperson burnout.** CEO can be spokesperson for 24-48h. After that, designate. Otherwise quality drops.
- **Post-mortem within 2 weeks.** Memory decays. Schedule on day 1 of crisis for 2 weeks out.
- **Don't rehearse only the easy archetype.** Rotate annually. Layoffs and breaches are most-skipped because uncomfortable.
- **Layoffs: don't "right-size" or "optimize."** Plain English. "We are reducing roles." Honest > corporate.

## Sources

- [Empire Magazine — CEO Playbook 2026](https://www.theempiremag.com/the-ceo-playbook-2026/)
- [HBR — Crisis Communication](https://hbr.org/topic/crisis-management)
- [Steve Wozniak / Apple crisis comms case studies](https://stories.gw.utah.edu)
- [Embroker D&O insurance](https://www.embroker.com/coverage/d-o-insurance/)
- [Atlassian Statuspage docs](https://support.atlassian.com/statuspage/)
