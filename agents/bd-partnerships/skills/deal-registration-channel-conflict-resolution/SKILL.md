<!--
Source: https://partnerstack.com/blog/deal-registration + https://www.impartner.com/blog/deal-registration-best-practices + https://www.allbound.com/blog/deal-registration + https://developers.hubspot.com/docs/api/crm/objects/custom-objects
Deal registration workflow + channel conflict resolution (June 2026 SOTA).
-->
# Deal Registration + Channel Conflict Resolution — SKILL

Operate the deal-registration lifecycle: partner submits → 48-hour SLA review → approve / reject / counter / split → 60-day protected window + margin uplift; first-to-register wins by default, with appeal path. Surface conflicts to channel manager; log decisions; quarterly conflict report. Tools: HubSpot/Salesforce custom object + Partnerstack/Allbound/Impartner PRM + Notion conflict log + Slack alerts + Postgres SLA timer.

## When to use

- **Partner submits a deal-reg** — accept submission, create CRM record, start SLA timer.
- **Channel manager reviews registration** — check for conflicts, ICP, scope, approve / reject / counter.
- **48-hour SLA breach alert** — registration unactioned → escalate to director.
- **Conflict detected** — same prospect registered or in active direct pursuit; resolve per matrix.
- **Appeal filed** — losing party appeals; route to channel manager → director.
- **60-day protected window expiring** — alert partner 7 days before expiration; renew or release.
- **Quarterly conflict report** — # conflicts, first-to-register sustained %, appeals overturned %.
- **Trigger phrases**: "deal reg from Acme", "approve registration", "register Globex for partner-X", "channel conflict on Globex", "two partners on same deal", "appeal the rejection".

Do NOT use this skill for: **commission posting** (use `partnerstack-tackle-channel-management`); **partner agreement attribution clauses** (use `referral-affiliate-channel-oem-agreement-structuring`); **deal source-field tracking** (use `partner-sourced-pipeline-tracking`); **MDF requests** (use `mdf-allocation-tracking`).

## Setup

```bash
export MATON_API_KEY="<key>"
export HUBSPOT_PRIVATE_APP_TOKEN="<token>"
export SALESFORCE_INSTANCE_URL="<url>"
export SALESFORCE_ACCESS_TOKEN="<token>"
export PARTNERSTACK_API_KEY="<key>"
export ALLBOUND_API_KEY="<key>"
export IMPARTNER_API_KEY="<key>"
export NOTION_API_KEY="<key>"
export SLACK_BOT_TOKEN="<token>"
export WAREHOUSE_CONN_STR="postgres://..."
```

**One-time setup:**
- HubSpot custom object `deal_registrations` (or Salesforce custom obj) with required fields below
- Notion database `Conflict Register` (date, partner-A, partner-B, prospect, scope, resolution, decision-owner)
- Slack channel `#deal-reg` for submission alerts + `#deal-reg-conflicts` for conflict escalations
- Postgres SLA timer cron (every 1h) firing reminders at T+24h, breach alert at T+48h

## Common recipes

### Recipe 1: Create deal-reg custom object (HubSpot)

```bash
# One-time schema creation
curl -X POST "https://gateway.maton.ai/hubspot/crm/v3/schemas" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "name":"deal_registration",
    "labels":{"singular":"Deal Registration","plural":"Deal Registrations"},
    "primaryDisplayProperty":"prospect_company",
    "requiredProperties":["partner_id","prospect_company","prospect_email","submitted_at"],
    "properties":[
      {"name":"partner_id","label":"Partner","type":"string"},
      {"name":"prospect_company","label":"Prospect","type":"string"},
      {"name":"prospect_email","label":"Contact Email","type":"string"},
      {"name":"prospect_size_employees","label":"Size","type":"number"},
      {"name":"deal_size_hypothesis_usd","label":"Hypothesized $","type":"number"},
      {"name":"close_date_hypothesis","label":"Hypothesized close","type":"date"},
      {"name":"scope","label":"Scope","type":"string"},
      {"name":"justification","label":"Why this partner","type":"string"},
      {"name":"submitted_at","label":"Submitted","type":"datetime"},
      {"name":"status","label":"Status","type":"enumeration","options":[
        {"label":"Submitted","value":"submitted"},
        {"label":"Approved","value":"approved"},
        {"label":"Rejected","value":"rejected"},
        {"label":"Counter-offered","value":"countered"},
        {"label":"Expired","value":"expired"}
      ]},
      {"name":"expires_at","label":"Protection expires","type":"datetime"},
      {"name":"decision_at","label":"Decided","type":"datetime"},
      {"name":"decision_by","label":"Decided by","type":"string"},
      {"name":"decision_notes","label":"Notes","type":"string"}
    ]
  }'
```

Reference: https://developers.hubspot.com/docs/api/crm/objects/custom-objects.

### Recipe 2: Accept partner submission

```bash
# Triggered by Partnerstack `lead.submitted` webhook OR partner portal form POST
curl -X POST "https://gateway.maton.ai/hubspot/crm/v3/objects/deal_registration" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "properties":{
      "partner_id":"acme-001",
      "prospect_company":"Globex Corp",
      "prospect_email":"buyer@globex.com",
      "prospect_size_employees":"850",
      "deal_size_hypothesis_usd":"125000",
      "close_date_hypothesis":"2026-09-30",
      "scope":"Module A + integration B; 12-month contract",
      "justification":"Acme has CTO relationship; running active eval; we have not engaged.",
      "submitted_at":"'"$(date -u +%FT%TZ)"'",
      "status":"submitted"
    }
  }'

# Immediately post to Slack #deal-reg for 48h SLA
curl -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" -H "Content-Type: application/json; charset=utf-8" \
  -d '{
    "channel":"#deal-reg",
    "text":"New deal-reg: Acme → Globex Corp ($125K). 48h SLA. Approve / Reject / Counter."
  }'
```

### Recipe 3: Conflict detection (run on every submission)

```sql
-- Find competing registrations or active direct pursuits on same prospect
SELECT 'PARTNER_CONFLICT' AS type, dr2.id, dr2.partner_id, dr2.submitted_at, dr2.status
FROM deal_registrations dr1
JOIN deal_registrations dr2
  ON LOWER(dr1.prospect_company) = LOWER(dr2.prospect_company)
  AND dr1.id <> dr2.id
WHERE dr1.id = :new_reg_id
  AND dr2.status IN ('submitted','approved')
  AND dr2.expires_at > NOW()
UNION ALL
SELECT 'DIRECT_CONFLICT' AS type, o.id::text, 'direct' AS partner_id, o.created_at, o.stage AS status
FROM opportunities o
WHERE LOWER(o.account_name) = LOWER(:prospect_company)
  AND o.source = 'Direct'
  AND o.stage NOT IN ('Closed Won','Closed Lost');
```

If non-empty → flag in Recipe 5 conflict log.

### Recipe 4: Approve registration

```bash
curl -X PATCH "https://gateway.maton.ai/hubspot/crm/v3/objects/deal_registration/<reg_id>" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "properties":{
      "status":"approved",
      "decision_at":"'"$(date -u +%FT%TZ)"'",
      "decision_by":"sarah.cm@vendor.com",
      "decision_notes":"Approved; partner has established relationship; ICP fit; no conflicts.",
      "expires_at":"'"$(date -u -d '+60 days' +%FT%TZ)"'"
    }
  }'

# Auto-update partner's CRM opportunity with deal-reg uplift on margin
curl -X PATCH "https://gateway.maton.ai/hubspot/crm/v3/objects/deals/<deal_id>" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{"properties":{"deal_reg_uplift_pts":"5","deal_reg_id":"<reg_id>"}}'

# Notify partner via gmail
```

### Recipe 5: Log conflict to Notion register

```python
def log_conflict(reg_id, conflict_party, scope_overlap_pct, resolution_type, decision_by):
    notion.pages.create(
        parent={"database_id": CONFLICT_REGISTER_DB_ID},
        properties={
            "Date": {"date": {"start": today().isoformat()}},
            "Reg ID": {"title": [{"text": {"content": reg_id}}]},
            "Partner A": {"rich_text": [{"text": {"content": lookup_partner_a(reg_id)}}]},
            "Partner B / Direct": {"rich_text": [{"text": {"content": conflict_party}}]},
            "Scope overlap %": {"number": scope_overlap_pct},
            "Resolution": {"select": {"name": resolution_type}},
            "Decision by": {"rich_text": [{"text": {"content": decision_by}}]},
        },
    )
```

### Recipe 6: Counter-offer (split scope)

```bash
# E.g., partner-A wins Module A, partner-B wins Module B
curl -X PATCH "https://gateway.maton.ai/hubspot/crm/v3/objects/deal_registration/<reg_a_id>" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{"properties":{"status":"countered","scope":"Module A only","decision_notes":"Split with Acme/B; B owns Module B."}}'

curl -X PATCH "https://gateway.maton.ai/hubspot/crm/v3/objects/deal_registration/<reg_b_id>" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{"properties":{"status":"countered","scope":"Module B only","decision_notes":"Split with Acme/A; A owns Module A."}}'
```

### Recipe 7: 48-hour SLA breach alert (cron)

```sql
-- Run every hour via postgresql-mcp cron
SELECT dr.id, dr.partner_id, dr.prospect_company, dr.submitted_at,
       EXTRACT(EPOCH FROM (NOW() - dr.submitted_at))/3600 AS hours_open
FROM deal_registrations dr
WHERE dr.status = 'submitted'
  AND dr.submitted_at < NOW() - INTERVAL '24 hours'
ORDER BY dr.submitted_at;
```

Each row at T+24h → Slack ping channel manager. At T+48h → escalate to director.

### Recipe 8: Expiry sweep (cron daily)

```sql
-- Expire approved registrations past 60-day window without a deal attached
UPDATE deal_registrations
SET status='expired'
WHERE status='approved'
  AND expires_at < NOW()
  AND NOT EXISTS (SELECT 1 FROM deals d WHERE d.deal_reg_id = id);
```

### Recipe 9: Expiry warning (7 days before)

```sql
SELECT dr.id, dr.partner_id, dr.prospect_company, dr.expires_at, p.contact_email
FROM deal_registrations dr
JOIN partners p USING(partner_id)
WHERE dr.status='approved'
  AND dr.expires_at BETWEEN NOW() AND NOW() + INTERVAL '7 days'
  AND NOT EXISTS (SELECT 1 FROM deals d WHERE d.deal_reg_id = dr.id);
```

Pipe to `gmail-mcp` reminder + `slack-mcp` to channel manager.

### Recipe 10: Quarterly conflict report

```sql
SELECT
  DATE_TRUNC('quarter', date)                                            AS quarter,
  COUNT(*)                                                               AS total_conflicts,
  COUNT(*) FILTER (WHERE resolution='first-to-register')                  AS first_to_reg_sustained,
  COUNT(*) FILTER (WHERE resolution='customer-preference')                AS customer_override,
  COUNT(*) FILTER (WHERE resolution='split-scope')                        AS split,
  COUNT(*) FILTER (WHERE resolution='appeal-overturned')                  AS appeals_overturned,
  ROUND(COUNT(*) FILTER (WHERE resolution='appeal-overturned')::numeric /
        NULLIF(COUNT(*) FILTER (WHERE appeal_filed), 0), 3)               AS appeal_overturn_rate
FROM conflict_register
WHERE date >= DATE_TRUNC('year', NOW())
GROUP BY 1 ORDER BY 1 DESC;
```

Render to `pdf`/`xlsx` for partner-program leadership.

### Recipe 11: Partner-side appeal submission

```python
def file_appeal(reg_id, partner_id, reason):
    notion.pages.create(parent={"database_id": APPEAL_LOG_DB_ID}, properties={
        "Reg ID": {"title":[{"text":{"content":reg_id}}]},
        "Partner": {"rich_text":[{"text":{"content":partner_id}}]},
        "Reason": {"rich_text":[{"text":{"content":reason}}]},
        "Filed at": {"date":{"start":now().isoformat()}},
        "Status": {"select":{"name":"open"}},
    })
    slack_chat_post("#deal-reg-conflicts", f"Appeal filed: {partner_id} on reg {reg_id}. SLA 5 business days.")
```

## Examples

### Example 1: Acme submits Globex; 48h SLA observed; approved

**Goal:** Acme submits Globex prospect; vendor approves within 48h; partner gets 60-day window.

**Steps:**
1. Recipe 2 — Submission via Partnerstack lead-submitted webhook.
2. Slack ping fires to `#deal-reg`.
3. Recipe 3 — Conflict detection runs; no conflicts found.
4. Channel manager reviews next morning; Recipe 4 approves; sets `expires_at` to T+60d; sends partner notification email.
5. Deal-reg uplift of +5 pts auto-applied when deal opportunity created.

**Result:** Acme has protected status + margin uplift; AE notified to coordinate motion.

### Example 2: Conflict — Acme + Initech both submit Globex within 24h

**Goal:** Two partners submit same prospect; resolve per matrix.

**Steps:**
1. Acme submits at T0; Initech submits at T+18h.
2. Recipe 3 detects `PARTNER_CONFLICT` on Initech's submission.
3. Recipe 5 logs to Notion conflict register.
4. Channel manager reviews scope: Acme = "full platform"; Initech = "Module B + services."
5. Recipe 6 counter-offers both: Acme = Module A + core platform; Initech = Module B + services. Both approved with adjusted scope.
6. Customer happy; both partners credited.

**Result:** Split-scope resolution preserves partner relationship + customer experience.

### Example 3: Appeal overturned; first-to-register rule held but with margin compensation

**Goal:** Initech appeals rejection of Globex; customer expressed preference for Initech.

**Steps:**
1. Recipe 11 — Initech files appeal with customer-preference evidence (email forward).
2. Channel manager reviews within 5 business days.
3. Decision: honor customer preference; Initech wins; Acme gets 50% of commission as goodwill credit (per agreement carve-out).
4. Recipe 5 logs as `customer-preference` resolution.
5. Quarter-end report (Recipe 10) shows 1 appeal overturned out of 8 conflicts.

**Result:** Customer wins; partner-relationship integrity preserved; rule transparency maintained.

## Edge cases / gotchas

- **First-to-register rule rigid abuse** — partner submits speculative regs to "lock" prospects they aren't actively working. Require scope + justification field; reject if no engagement evidence within 30 days.
- **48h SLA breach during weekends/holidays** — pause SLA clock during weekends; document in agreement.
- **Direct AE pre-existing relationship** — AE already engaging prospect for 30 days before partner submits. Don't auto-reject; require AE to provide engagement timeline; resolve per "active-pursuit" rule (typically: existing pursuit > 30 days wins; otherwise partner).
- **Partner submits after first sales call by direct AE** — partner doesn't know AE is engaged. Resolve via timestamp + activity audit.
- **Multi-partner co-sell** — both partners legitimately needed; agreement may allow joint deal-reg with split commission (60/40 default).
- **Customer-preference proof** — written email from customer required to overrule first-to-register. Verbal claims insufficient.
- **Scope creep mid-window** — partner registered for Module A; deal expands to A+B+C. Decide: extend reg to cover or require new reg (default: extend if same prospect+timeline).
- **Renewal of protected window** — 60-day expired; deal still in flight. Allow 1 renewal of 30 days with channel manager sign-off; do not auto-renew (forces accountability).
- **Quarterly conflict spike** — > 15% conflict rate signals territory / segment design issue. Audit partner overlap.
- **Multi-tenant CRM/PRM mismatch** — registration in Partnerstack ≠ deal in HubSpot. Sync via `deal_reg_id` foreign key; nightly reconciliation.
- **Deal-reg uplift gaming** — partner submits multiple regs for same deal under different opps to stack uplift. Enforce 1-reg-per-prospect-per-quarter.
- **Appeal escalation fatigue** — director appeal-load > 4/quarter signals channel manager decisions inconsistent. Track decision-quality metric.
- **International time zones** — 48h SLA across APAC + EMEA + AMER. Define SLA in business-hours-by-vendor-HQ; document.
- **PRM vs CRM source-of-truth conflict** — Allbound says approved; HubSpot says expired. Designate single source of truth + nightly sync (`postgresql-mcp` cron).

## Sources

- Partnerstack deal-reg: https://partnerstack.com/blog/deal-registration
- Impartner deal-reg best practices: https://www.impartner.com/blog/deal-registration-best-practices
- Allbound deal-reg: https://www.allbound.com/blog/deal-registration
- HubSpot custom objects API: https://developers.hubspot.com/docs/api/crm/objects/custom-objects
- Crossbeam channel conflict patterns: https://crossbeam.com/blog/channel-conflict/
