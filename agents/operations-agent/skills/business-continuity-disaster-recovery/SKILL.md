<!--
Sources: https://www.atlassystems.com/blog/vendor-risk-assessment-checklist-key-questions
         BCP framework: BIA → RTO/RPO → DR plan per system tier. Cloud backup (AWS Backup, GCP, Druva, Rubrik).
-->
# Business Continuity / Disaster Recovery — SKILL

Author a BCP (Business Continuity Plan) + DR (Disaster Recovery) plan: Business Impact Analysis (BIA), per-system RTO/RPO targets, cloud-backup recipes (AWS Backup / Azure Backup / GCP Backup-and-DR / Druva / Rubrik), comms playbook (Slack + SMS + status page), tabletop exercise framework. Surfaces in audit + SOC 2 CC9.

## When to use

- SOC 2 / ISO 27001 / HITRUST audit prep.
- Post-incident retrospective produced a "missing BCP" finding.
- Customer security questionnaire requires BCP.
- Annual BCP review.
- Trigger phrases: "BCP", "DR", "disaster recovery", "RTO", "RPO", "tabletop", "BIA", "business continuity", "incident plan", "status page".

## Setup

```bash
# Cloud backup
aws configure   # AWS Backup
gcloud auth login   # GCP Backup-and-DR
az login   # Azure Backup

# Status page
export STATUSPAGE_TOKEN="xxx"      # https://statuspage.io
export BETTER_STACK_TOKEN="xxx"    # https://betterstack.com
export INSTATUS_TOKEN="xxx"

# Comms
export TWILIO_SID="xxx"
export TWILIO_TOKEN="xxx"
export SLACK_BOT_TOKEN="xxx"
```

## Common recipes

### Recipe 1: BCP/DR plan skeleton
```markdown
# Business Continuity Plan — [Co] — v2026.07

## 1. Purpose + scope
- Systems in scope: [list]
- Geographies: [list]
- Annual review: July
- Owner: [Head of Ops / CTO]

## 2. Business Impact Analysis (BIA)
| System / Process       | Business impact | RTO | RPO | Owner | Tier |
|------------------------|-----------------|-----|-----|-------|------|
| Customer-facing app    | $X/hr revenue   | 1h  | 5m  |       | T0   |
| Payment processing     | revenue stop    | 30m | 0m  |       | T0   |
| Salesforce / CRM       | sales paralysis | 4h  | 1h  |       | T1   |
| Email (Gmail)          | comms stop      | 4h  | 1h  |       | T1   |
| Slack                  | comms degraded  | 1h  | 5m  |       | T1   |
| Internal docs (Notion) | knowledge stop  | 8h  | 1h  |       | T2   |
| Marketing site         | brand           | 4h  | 1d  |       | T2   |
| Vendor portal (Ramp)   | finance close   | 24h | 1d  |       | T2   |

## 3. RTO / RPO definitions
- **RTO (Recovery Time Objective):** max acceptable downtime.
- **RPO (Recovery Point Objective):** max acceptable data loss (in time).
- **Tier 0:** RTO ≤ 1h, RPO ≤ 5m, automated failover.
- **Tier 1:** RTO ≤ 4h, RPO ≤ 1h, scripted recovery.
- **Tier 2:** RTO ≤ 24h, RPO ≤ 1d, manual recovery acceptable.

## 4. Recovery scenarios
- 4.1 Primary cloud region outage
- 4.2 Database corruption (logical / physical)
- 4.3 Account takeover / credential compromise
- 4.4 Ransomware
- 4.5 Key vendor outage (Stripe, AWS S3, Auth0, Salesforce)
- 4.6 Office unavailable (fire / weather / pandemic)
- 4.7 Key-person unavailability

## 5. Roles + responsibilities
- Incident Commander (IC): [primary, backup, backup-2]
- Communications Lead: [primary, backup]
- Tech Lead per system: see BIA table
- Legal contact: see legal-counsel
- Insurance carrier: Cyber policy contact line

## 6. Communications playbook
See Recipe 6.

## 7. Tabletop exercise schedule
- Quarterly: scenario from §4
- Annual full-day: cross-system + cross-team

## 8. Recovery procedures per scenario
[per scenario, link to runbook in runbook-authoring-operational-incident]

## 9. Plan distribution
- Live copy: Notion `Ops/BCP/v2026.07`
- Offline copy: encrypted USB + printed binder (offsite)
- Plan owner notifies all employees via Slack on revision
```

### Recipe 2: AWS Backup plan
```bash
# Daily backup of EBS + RDS + DynamoDB
aws backup create-backup-plan --backup-plan '{
  "BackupPlanName":"prod-daily",
  "Rules":[{
    "RuleName":"daily-35day",
    "TargetBackupVaultName":"prod-vault",
    "ScheduleExpression":"cron(0 5 * * ? *)",
    "StartWindowMinutes":60,
    "CompletionWindowMinutes":180,
    "Lifecycle":{"DeleteAfterDays":35,"MoveToColdStorageAfterDays":7},
    "CopyActions":[{"DestinationBackupVaultArn":"arn:aws:backup:us-west-2:<acct>:backup-vault:cross-region-prod-vault"}]
  }]
}'

aws backup create-backup-selection \
  --backup-plan-id <plan_id> \
  --backup-selection '{"SelectionName":"all-tagged","IamRoleArn":"arn:aws:iam::<acct>:role/AWSBackupServiceRole","Resources":["*"],"Conditions":{"StringEquals":{"aws:ResourceTag/Backup":"yes"}}}'
```

### Recipe 3: GCP Backup-and-DR (Snapshot schedules)
```bash
gcloud compute resource-policies create snapshot-schedule prod-daily \
  --region us-central1 \
  --max-retention-days 35 \
  --start-time 05:00 \
  --hourly-schedule 24
gcloud compute disks add-resource-policies <disk> --resource-policies prod-daily
```

### Recipe 4: Statuspage / Better Stack — create incident
```bash
# Statuspage
curl -s -X POST "https://api.statuspage.io/v1/pages/<page>/incidents" \
  -H "Authorization: OAuth $STATUSPAGE_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "incident":{
      "name":"Investigating elevated error rates",
      "status":"investigating",
      "impact_override":"major",
      "components_ids":["<api-component>"],
      "component_ids":["<api-component>"]
    }
  }'

# Better Stack
curl -s -X POST "https://uptime.betterstack.com/api/v2/status-pages/<page>/announcements" \
  -H "Authorization: Bearer $BETTER_STACK_TOKEN" -H "Content-Type: application/json" \
  -d '{"title":"Investigating","starts_at":"now","status_page_section":"<sec>"}'
```

### Recipe 5: Twilio SMS broadcast (employee / customer all-hands page)
```bash
# Don't pre-build customer phone list without consent; for employees only
curl -X POST "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_SID/Messages.json" \
  -u "$TWILIO_SID:$TWILIO_TOKEN" \
  -d "From=+15551111111" \
  -d "To=+15552222222" \
  -d "Body=[INCIDENT] Production degraded. Status: https://status.acme.com. IC: @alex"
```

### Recipe 6: Comms playbook template
```markdown
## Comms cadence (per incident)
- **T+0 (detect):** IC pages, Slack #incident-room created, status page → "Investigating"
- **T+15 min:** First public update (regardless of progress). "We are investigating reports of X. Updates every 30 min."
- **T+30 min:** Update. If still investigating, say what we've ruled out.
- **T+1 hr:** Status confirmed (identified / monitoring / resolved). Escalation if not.
- **T+resolved:** Status page → resolved. Schedule postmortem.

## Channels
- Internal: Slack #incident-room (one per incident) + #ops-leadership
- External users: status page (https://status.<co>.com) — primary
- External customers (account managers): Slack/email per CSM
- Press / partners: only via comms@ + CEO sign-off
- Legal / regulator: notify per breach-notice law (see legal-counsel)

## Severity definitions
- SEV-1: complete outage / data loss / security breach
- SEV-2: partial outage, major function impacted
- SEV-3: degraded but workable
- SEV-4: cosmetic / minor

## Notification matrix
| Sev | IC paged | Status page | Customer email | CEO | Board | Insurance | Regulator |
|-----|----------|-------------|----------------|-----|-------|-----------|-----------|
| 1   | yes      | yes         | yes (1h)       | yes | yes   | yes (24h) | per law   |
| 2   | yes      | yes         | optional       | yes | brief | optional  | no        |
| 3   | optional | optional    | no             | brief| no   | no        | no        |
| 4   | no       | no          | no             | no  | no    | no        | no        |
```

### Recipe 7: Tabletop exercise framework
```markdown
# Tabletop — Q3 2026 — Scenario: Primary AWS region outage

## Setup
- Date / time: 2026-08-15, 14:00-16:00
- Participants: IC + Comms + Tech leads + Legal + CEO observer
- Facilitator: head of ops
- Mode: discussion-based (no live break)

## Scenario script (read by facilitator)
"It is Tuesday 09:30. PagerDuty fires: api.acme.com health check failing in us-east-1.
AWS Health Dashboard reports networking degradation across multiple AZs.
First customer reports come in via Intercom."

## Inject points
- T+5min: "us-east-1 RDS Multi-AZ failover reports failing."
- T+15min: "AWS status page confirms regional issue, no ETA."
- T+30min: "Twitter starts trending. CEO calls."

## Discussion questions
1. Who declares the incident? When?
2. Do we fail over to us-west-2?
3. What do we tell customers at T+15min?
4. When do we engage legal?
5. When do we notify cyber-insurance carrier?

## Out-of-band
- IF the incident were ransomware: stop. Engage carrier breach hotline FIRST per policy.

## Findings + actions
- [ ] Action 1
- [ ] Action 2
```

### Recipe 8: Quarterly DR drill — actual failover
```bash
# Test region failover for read-only path
aws rds promote-read-replica --db-instance-identifier <replica-west-2>
# Validate, smoke-test
# Then promote back
```

### Recipe 9: Vendor outage runbook (third-party dependency)
```markdown
## Vendor: Stripe — outage runbook
- Detection: Stripe status page yellow/red, our checkout error-rate > 5%
- Immediate:
  1. Set checkout page to "We're investigating payment delays" banner.
  2. Switch to fallback processor if configured (Recipe X).
  3. Queue failed payments for retry; do not auto-refund.
- Comms:
  - T+15min status page: "Payment delays — investigating."
  - T+30min: confirm or adjust.
- Post-resolution: replay queued payments; reconcile with Stripe; notify any duplicates.
- Contact: Stripe incident response — security@stripe.com, support
```

### Recipe 10: BCP digital + paper distribution
```bash
# Generate PDF for offsite binder
pandoc bcp.md -o BCP-v2026.07.pdf
# Encrypted USB stick — pinned to ops lead's go-bag
# Also: print binder for office safe
```

### Recipe 11: Cloud backup restore test (Python harness)
```python
# Monthly automated restore + validate sample restore worked
import boto3, datetime
backup = boto3.client('backup')
recovery_points = backup.list_recovery_points_by_backup_vault(
    BackupVaultName='prod-vault',
    ByCreatedAfter=datetime.datetime.utcnow() - datetime.timedelta(days=2)
)
sample = recovery_points['RecoveryPoints'][0]['RecoveryPointArn']
# Start restore job
job = backup.start_restore_job(
    RecoveryPointArn=sample,
    Metadata={...},
    IamRoleArn='arn:aws:iam::<acct>:role/AWSBackupRestoreRole'
)
# Verify within RTO target
```

## Examples

### Example 1: First BCP for SOC 2 audit
**Goal:** Pass CC9 (BCP) for SOC 2 Type II in 6 weeks.
**Steps:**
1. Recipe 1 skeleton → fill in BIA + RTO/RPO from system inventory.
2. Recipe 2/3: cloud-backup plans + cross-region copy.
3. Recipe 7 tabletop in week 4.
4. Document findings + remediation.
5. Recipe 10 distribution.

**Result:** SOC 2-passable BCP + evidence of testing.

### Example 2: Region failover drill quarterly
**Goal:** Verify Tier-0 RTO target (1h).
**Steps:**
1. Recipe 8 — promote replica.
2. Smoke-test app behaviors.
3. Time the cycle; document.
4. Failback after window.

**Result:** Verified RTO; surfaces drift between plan + reality.

## Edge cases / gotchas

- **Tabletop ≠ drill.** Tabletops are discussion; drills are real failover. SOC 2 looks for both.
- **RPO drift.** Setting RPO=5m but backing up every 24h fails plan-vs-reality. Recipe 11 monthly restore tests catch this.
- **Cross-region cost.** Copying every backup cross-region doubles storage costs. Limit to Tier-0/T1 systems.
- **Ransomware exclusions.** Cyber policy may require ransomware-specific notification timeline; check before paying anything. **Defer to `legal-counsel` + insurance carrier first.**
- **Status page over-communication.** Posting partial info early to "investigate" is better than going dark; but don't speculate cause.
- **Twilio cold-start.** First SMS in a year may rate-limit. Pre-warm via test sends.
- **BCP-plan staleness.** Owners + RPO/RTO drift; annual review mandatory; quarterly tabletop forces awareness.
- **Single-source-of-truth lapse.** If Notion is down during incident, the plan you wrote there is unreachable. Recipe 10 paper + offline copies essential.
- **Vendor SLA vs your RTO.** AWS SLA = 99.99%, but that's monthly aggregate. Your single-incident RTO target may not be met by their SLA. Plan for it.
- **Defer to `legal-counsel` for breach-notification timing (GDPR 72h, state breach laws varying 30-90 days, SEC 4-day cyber-incident disclosure for public cos), regulator coordination, and customer-notice drafting.**

## Sources

- Atlas Systems — Vendor Risk Assessment Checklist: https://www.atlassystems.com/blog/vendor-risk-assessment-checklist-key-questions
- NMS Consulting — Vendor Risk Management Checklist: https://nmsconsulting.com/vendor-risk-management-checklist/
- AWS Backup: https://docs.aws.amazon.com/aws-backup/
- GCP Backup-and-DR: https://cloud.google.com/backup-disaster-recovery
- Azure Backup: https://learn.microsoft.com/en-us/azure/backup/
- Statuspage API: https://developer.statuspage.io/
- Better Stack: https://betterstack.com/docs/uptime/api
- Twilio API: https://www.twilio.com/docs/sms
- SOC 2 CC9: https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2
- SEC cyber disclosure rule (4 business days): https://www.sec.gov/news/press-release/2023-139
