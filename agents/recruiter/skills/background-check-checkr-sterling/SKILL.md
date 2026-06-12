<!--
Sources: https://developers.checkr.com/
         https://www.sterlingcheck.com/api-documentation/
         https://www.goodhire.com/
2026 background-check landscape: Checkr = founder-friendly API + 2-3 day turnaround; Sterling =
enterprise + global; GoodHire = SMB; Sterling Global / Checkr International for cross-border.
FCRA flow + Ban-the-Box + pre/adverse action wording defers to legal-counsel.
Canonical FCRA runbook lives in role.md "FCRA flow runbook".
Background-check package matrix lives in role.md "Background check package matrix".
-->
# Background Check — Checkr / Sterling — SKILL

Order, track, and adjudicate background checks via Checkr / Sterling / GoodHire APIs: invite candidate, package selection by role tier, webhook on report completion, FCRA pre-adverse + adverse action timing, EEOC-required individualized assessment, ATS auto-attachment. Pre-adverse + adverse-action wording defers to `legal-counsel`.

## When to use

- Offer accepted; background check triggered as contingency.
- Adjudication: report comes back with adverse finding → FCRA flow.
- International: Sterling Global / Checkr International for cross-border.
- Compliance: state-specific package selection (Ban-the-Box, CA Fair Chance Act, NYC FCA).
- Trigger phrases: "background check", "Checkr", "Sterling", "GoodHire", "FCRA", "adverse action", "Ban-the-Box", "individualized assessment", "I-9".
- Defer to `legal-counsel`: package selection per state, pre/adverse action letter wording, Ban-the-Box trigger timing, ADA accommodation requests, individualized assessment documentation.

## Setup

```bash
# Checkr
export CHECKR_API_KEY="chr_test_xxx"        # https://dashboard.checkr.com/
# Sandbox: https://api.checkr.com/v1 with chr_test_; prod with chr_live_

# Sterling
export STERLING_USERNAME="xxx"
export STERLING_PASSWORD="xxx"
export STERLING_ACCOUNT="xxx"
# https://www.sterlingcheck.com/api-documentation/

# GoodHire (SMB tier)
export GOODHIRE_API_KEY="xxx"
# https://www.goodhire.com/api/

# ATS for attachment
export GREENHOUSE_API_KEY="harvest_xxx"
export GH_USER_ID="123456"
```

Auth model:
- **Checkr:** basic-auth with API key, empty password (`-u "$CHECKR_API_KEY:"`).
- **Sterling:** OAuth2 with client credentials; tokens 1h.
- **GoodHire:** static API key in header.

Reference: full FCRA runbook lives in `role.md` "FCRA flow runbook". Package matrix in `role.md` "Background check package matrix".

## Common recipes

### Recipe 1: Send Checkr invitation
```bash
curl -s -X POST -u "$CHECKR_API_KEY:" \
  -H "Content-Type: application/json" \
  "https://api.checkr.com/v1/invitations" \
  -d '{
    "candidate": {
      "first_name": "Jane",
      "last_name": "Doe",
      "email": "jane@example.com"
    },
    "package": "tasker_standard",
    "work_locations": [{"country": "US", "state": "CA", "city": "San Francisco"}]
  }'
```
Response includes `invitation_url`; candidate completes consent + PII via Checkr UI. Use `tasker_standard` (Recipe 4 lists package codes).

### Recipe 2: Pull Checkr report status
```bash
curl -s -u "$CHECKR_API_KEY:" \
  "https://api.checkr.com/v1/reports/<report_id>" \
  | jq '{id, status, result, completed_at, candidate, package}'
# Status: pending, suspended, complete; Result: clear, consider, suspended
```
`result=consider` → adverse finding requiring adjudication.

### Recipe 3: Register Checkr webhook
```bash
curl -s -X POST -u "$CHECKR_API_KEY:" \
  -H "Content-Type: application/json" \
  "https://api.checkr.com/v1/webhooks" \
  -d '{
    "url": "https://hooks.example.com/checkr/report",
    "events": ["report.completed", "report.suspended", "candidate.eligible_to_drive"]
  }'
# Events: report.created, report.upgraded, report.completed, report.suspended
# Webhook payload signed with HMAC; verify via X-Checkr-Signature header.
```

### Recipe 4: List Checkr packages
```bash
curl -s -u "$CHECKR_API_KEY:" \
  "https://api.checkr.com/v1/packages" \
  | jq '.data[] | {slug, name, screenings: [.screenings[].type]}'
# Common slugs:
# - tasker_standard: SSN + county criminal + sex offender + federal criminal (~$25-45, 1-3 day)
# - tasker_pro: + motor vehicle + education verification (~$75-125, 2-5 day)
# - tasker_pro_criminal: enhanced criminal + extended SSN trace
# - global_tasker: international package
```
Pick per `role.md` "Background check package matrix" tier:
- Standard (IC): tasker_standard
- Enhanced (senior+ / manager): tasker_pro
- Executive (VP+): custom package + media search + credit (FCRA-permissible)

### Recipe 5: Sterling — create screening
```bash
# Sterling auth (OAuth client credentials):
TOKEN=$(curl -s -X POST \
  -d "grant_type=client_credentials&client_id=$STERLING_USERNAME&client_secret=$STERLING_PASSWORD" \
  "https://login.sterlingcheck.com/oauth/token" | jq -r '.access_token')

# Initiate screening:
curl -s -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.sterlingcheck.com/v2/screenings" \
  -d '{
    "client": {"accountId": "'$STERLING_ACCOUNT'"},
    "candidate": {"firstName": "Jane", "lastName": "Doe", "email": "jane@example.com"},
    "package": "<sterling_package_code>",
    "workLocations": [{"country": "US", "state": "CA"}]
  }'
```

### Recipe 6: Sterling global package (international)
```bash
curl -s -X POST -H "Authorization: Bearer $TOKEN" \
  -d '{
    "client": {"accountId": "'$STERLING_ACCOUNT'"},
    "candidate": {"firstName": "Jean", "lastName": "Dubois", "email": "jean@example.com",
                  "nationality": "FR", "currentCountry": "FR"},
    "package": "global_standard_intl",
    "workLocations": [{"country": "FR"}, {"country": "DE"}]
  }' \
  "https://api.sterlingcheck.com/v2/screenings"
# Documentation in local language often required; turnaround 5-15 days per country.
```

### Recipe 7: Pre-adverse action letter trigger (FCRA Step 4)
```text
When report.result=consider:
1. STOP — do NOT make a decision yet.
2. Send pre-adverse action letter + copy of report + FCRA Summary of Rights to candidate.
3. WAIT 5 business days (some states: 10 — defer to legal-counsel).
4. During window: candidate may dispute / correct / provide context (mitigating evidence).
5. Document individualized assessment (Recipe 8) per EEOC + state requirements.
```

```bash
# Email + certified mail combo. Use docusign/pandadoc envelope OR direct gmail-mcp with certified-mail follow-up.
# Body template defer to legal-counsel; FCRA Summary of Rights (CFPB) attached as PDF.
```

### Recipe 8: Individualized assessment (EEOC required for criminal findings)
```markdown
# Individualized Assessment — {candidate_name} / {role}

## Offense
- Nature: {felony / misdemeanor; offense type}
- Date: {when}; jurisdiction: {state}
- Time since: {N years}
- Sentence completed: yes/no; date

## Role
- Job duties: {scope}
- Workplace setting: {access to children, finances, vulnerable populations?}
- Direct nexus to offense: {evaluate}

## Considerations (EEOC Green factors)
- Nature + gravity of offense: {analysis}
- Time elapsed since: {analysis}
- Nature of job: {analysis}
- Mitigating evidence provided: {applicant explanation}
- Rehabilitation: {evidence}
- Character references: {reviewed?}

## Decision rationale
- Proceed with hire / Decline / Hold

## Defer-to-legal items
- Wording of adverse action letter (if proceeding to decline)
- State-specific factors (e.g., NYC FCA Article 23-A)
- CA Fair Chance Act considerations
- Documentation retention requirements

## Sign-off
- Recruiter: ___
- HR / legal-counsel: ___
- Hiring manager: ___
```

### Recipe 9: Adverse action letter (Step 6 — only after individualized assessment)
```text
After 5-biz-day window + individualized assessment finds disqualifying:
1. Send adverse action letter via email + certified mail
2. Include FCRA Summary of Rights (post-adverse version)
3. Include dispute procedure + CRA contact info
4. NYC FCA: must explain Article 23-A factors weighed
5. Document everything for record-retention (5+ years; state-dependent)

WORDING DEFERS TO LEGAL-COUNSEL. Do not draft templated rejection language for criminal findings.
```

### Recipe 10: Attach signed report to Greenhouse candidate
```bash
# Download report PDF from Checkr:
curl -s -u "$CHECKR_API_KEY:" \
  "https://api.checkr.com/v1/reports/<report_id>/document" \
  -o report.pdf

# Attach to candidate:
curl -s -X POST -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -F "filename=background_check_report.pdf" \
  -F "type=other" \
  -F "content=@./report.pdf" \
  "https://harvest.greenhouse.io/v1/candidates/<candidate_id>/attachments"
# Don't store in `offer_letter` category; use `other` to indicate sensitive.
```

### Recipe 11: Ban-the-Box trigger timing (defer to legal)
```text
"Ban the Box" laws restrict WHEN you can ask about criminal history.
2026 active jurisdictions (US): 35+ states + 150+ cities including CA / NY / IL / MA / WA / TX / FL.
Most require: criminal-history inquiry AFTER conditional offer, NOT on application.

Checkr / Sterling can only run BG check after conditional offer accepted.
Verify with `legal-counsel` per applicant geo before triggering. If candidate self-discloses
earlier, document carefully — Ban-the-Box typically tolerates this if not solicited.
```

### Recipe 12: Education / employment verification deep-dive
```bash
# Standard education verification: degree + school + dates
curl -s -X POST -u "$CHECKR_API_KEY:" \
  -d '{"candidate_id":"<id>","verification":{"type":"education"}}' \
  "https://api.checkr.com/v1/screenings"

# Employment verification: title + dates + reason for separation (where lawful to ask)
curl -s -X POST -u "$CHECKR_API_KEY:" \
  -d '{"candidate_id":"<id>","verification":{"type":"employment","look_back_years":7}}' \
  "https://api.checkr.com/v1/screenings"

# Education fraud is the #1 BG flag (5-10% of resumes contain degree misrepresentation per Sterling research).
# Senior+ roles: 2+ employment verifications + education for all degrees claimed.
```

## Examples

### Example 1: Standard IC hire — clean clear
**Goal:** Standard BG check for new Senior Backend Engineer.
**Steps:**
1. Recipe 1: send Checkr invitation with `tasker_standard` package.
2. Recipe 3: webhook fires `report.completed` 2-3 days later.
3. Recipe 2: result=clear.
4. Recipe 10: attach report to candidate.
5. Notify hiring manager + advance to Day-1 prep (`post-offer-pre-start-check-ins`).

**Result:** Cleared in 3 days; hire proceeds.

### Example 2: Senior hire with criminal finding → individualized assessment
**Goal:** Adverse finding requires FCRA flow.
**Steps:**
1. Recipe 2 returns `result=consider` — county misdemeanor 8 years ago.
2. Recipe 7: pre-adverse action letter sent; 5-biz-day window starts.
3. Candidate provides context: completed sentence + clean since + rehabilitation documentation.
4. Recipe 8: individualized assessment with HR + legal-counsel.
5. Decision: proceed with hire (offense unrelated to role, time elapsed, mitigating evidence).
6. Document assessment + decision; no adverse action letter needed.

**Result:** EEOC-compliant adjudication; candidate retained; defensible audit trail.

### Example 3: International hire (FR + DE)
**Goal:** BG check for FR-based candidate hired into DE entity.
**Steps:**
1. Recipe 6: Sterling Global with both work locations.
2. Documentation in FR / DE language; turnaround 10-12 days.
3. Recipe 10: attach.

**Result:** Compliant cross-border check; hire proceeds.

## Edge cases / gotchas

- **FCRA disclosure must be standalone document.** Not in offer letter, not in I-9. Separate form, candidate signs before BG check. Violation = $100-$1,000/applicant + class action exposure.
- **Two-party consent for some checks.** CA + CO + others require additional state-specific disclosures (ICRAA / CFCRA + CO Stop ID Theft Act).
- **NYC FCA Article 23-A.** Strict adverse action analysis required if criminal finding; must explain reasoning. Defer to legal.
- **CA Fair Chance Act.** Specific timing + individualized assessment requirements; written assessment required.
- **Ban-the-Box trigger.** Don't ask about criminal history before conditional offer. Tag the candidate `bg_check_eligible=true` only after offer signed.
- **Credit checks.** FCRA-permissible only for specific roles (finance, fiduciary, high-cash-handling). Many states ban for general roles (CA, CO, CT, HI, IL, MD, NV, OR, VT, WA). Default OFF.
- **Education fraud.** ~5-10% misrepresentation rate. Verify for all senior+ roles + any role where degree is a stated requirement.
- **Employment verification refusal.** Some prior employers refuse to share details ("name, dates of employment only"). Document attempt; don't penalize candidate for prior employer's policy.
- **Continuous monitoring.** Some companies enable continuous criminal monitoring post-hire (alerts on new findings). Adds compliance burden + employee disclosure required. Defer to legal.
- **International limits.** GDPR + UK DPA + similar restrict what can be checked. Country-specific limits embedded in Sterling Global / Checkr International packages.
- **Healthcare / Finance / Government.** Compliance-specific (HIPAA + OIG / NPDB for healthcare; FINRA + Form U4 for finance; Public Trust / Secret / Top Secret for government). Use specialty packages.
- **Adverse action timing window varies by state.** 5 biz days default; some states 10. Don't decide before window closes.
- **Sterling Global turnaround variability.** Documentation lag in some countries (India, Brazil); 10-30 days possible. Communicate timeline to hire + candidate.
- **Record retention.** FCRA disclosure + authorization 5+ years; report 5+ years; some states longer. Defer to legal.
- **Defer to `legal-counsel`** for: all binding wording (pre-adverse + adverse action letters), package selection per state, Ban-the-Box trigger timing, individualized assessment documentation, FCRA compliance audits, ADA accommodation requests, continuous monitoring deployment.

## Sources

- [Checkr Developer Docs](https://developers.checkr.com/)
- [Checkr Packages](https://developers.checkr.com/reference/packages)
- [Checkr Webhooks](https://developers.checkr.com/docs/webhooks)
- [Sterling API documentation](https://www.sterlingcheck.com/api-documentation/)
- [GoodHire](https://www.goodhire.com/)
- [FCRA — Fair Credit Reporting Act](https://www.consumer.ftc.gov/articles/fair-credit-reporting-act)
- [CFPB FCRA Summary of Rights](https://www.consumerfinance.gov/compliance/compliance-resources/credit-reporting-resources/summary-of-consumer-rights/)
- [EEOC — Consideration of Arrest and Conviction Records](https://www.eeoc.gov/laws/guidance/enforcement-guidance-consideration-arrest-and-conviction-records-employment-decisions)
- [NYC Fair Chance Act](https://www.nyc.gov/site/cchr/law/fair-chance-act.page)
- [CA Fair Chance Act](https://calcivilrights.ca.gov/posters/fair-chance-act-poster/)
- [Ban-the-Box state tracker](https://www.nelp.org/insights-research/ban-the-box-fair-chance-hiring-state-and-local-guide/)
