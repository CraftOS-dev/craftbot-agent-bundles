---
name: phishing-simulation-program
description: Multi-vector phishing simulation program — email (80%+), SMS (smishing), voice (vishing), QR code (quishing — surging 2026), AI-generated deepfake (CEO fraud, vendor impersonation, NEW 2026). Monthly minimum at org level; weekly for critical roles. Difficulty curve, theme rotation, severity escalation per-user. Measurement: click + report + credential-entry + dwell. Vendor: KnowBe4 / Hoxhunt / Arsen multi-vector.
---

# Phishing Simulation Program — Multi-Vector + Adaptive

Phishing simulation is the operational arm of security awareness training. 2026 expansion: voice (vishing) + QR (quishing) + deepfake AI video/audio. Arsen + Adaptive Security pioneered deepfake sim. Monthly minimum cadence; weekly for finance, exec assistants, executives.

## When to use

User says:
- "Phishing simulation" / "phishing test" / "phishing campaign"
- "Smishing" / "Vishing" / "Quishing"
- "Deepfake test" / "AI phishing"
- "Click rate" / "report rate"
- "BEC defense" / "Business Email Compromise"
- "Phishing program design"

Companion skills: `security-awareness-training-knowbe4-hoxhunt`, `incident-response-nist-sp-800-61`.

## Setup

```bash
# Multi-vector platforms (recipient supplies)
export KNOWBE4_API_KEY=<dashboard>
export HOXHUNT_API_KEY=<dashboard>
export ARSEN_API_KEY=<dashboard>
export SOSAFE_API_KEY=<dashboard>

# https://www.knowbe4.com/phishing-tests
# https://hoxhunt.com/phishing-simulation
# https://www.arsen.co/         — AI deepfake / voice sim
# https://www.adaptivesecurity.com/  — AI deepfake sim
```

Auth notes:
- KnowBe4 phishing sim included in KMSAT tiers.
- Hoxhunt adaptive difficulty per user.
- Arsen + Adaptive Security require enterprise contract; sandbox available.

## Common recipes

### Recipe 1: Vector matrix (2026)

```text
Email (80%+ of phishing volume):
- Pretext-driven (HR, IT, finance, vendor)
- Credential-harvest (login phish)
- Malware delivery (payload, redirect)
- BEC (CEO fraud, vendor invoice change)

SMS / smishing (10%):
- Package delivery (UPS, FedEx, USPS, "your package")
- Account verification (bank, wallet, IRS)
- 2FA code request
- HR / payroll

Voice / vishing (5%):
- IT helpdesk impersonation ("we need to verify your MFA")
- Sales / vendor impersonation
- Executive impersonation (CEO calling finance about wire)
- Government impersonation (IRS, SSA)

QR / quishing (5%, surging 2026):
- "Scan to log in"
- "Scan to see schedule"
- "Scan for free Wi-Fi"
- Often delivered via SMS, posters, email

Deepfake (NEW 2026):
- AI-generated video CEO fraud
- AI-generated voice (clone of executive)
- AI-generated avatar in video calls
- Vendor / partner impersonation
```

### Recipe 2: Frequency cadence

```text
Org-wide baseline: monthly minimum.

Risk-tier-driven:
- Tier 1 (Finance, Exec assistants, Executives, CS handling sensitive
  data, IT admins): weekly minimum
- Tier 2 (HR, Eng with prod access, Customer-facing sales): bi-weekly
- Tier 3 (general staff): monthly

Event-driven extras:
- Q4 holiday season (package delivery, charity, gift card themes)
- W-2 season (Jan-Feb)
- Open enrollment (HR themes)
- Quarterly close (finance themes)
- Material news (M&A → impersonation phishing)
```

### Recipe 3: Difficulty curve (KnowBe4 / Hoxhunt)

```text
Easy (~30% click rate target — new hires + first quarter):
- Obvious typos in URL
- Plain-text low-effort lure
- Generic salutation ("Dear Employee")

Medium (~10-15% — second quarter onwards):
- Subdomain spoofing (login.bnk-of-america.com)
- Slight brand misalignment
- Personalized greeting + plausible context

Hard (~5-8% — mature orgs):
- Pixel-perfect brand replica
- Highly targeted (role-specific, recent project mention)
- Multi-step (initial benign → escalate via reply chain)
- DMARC bypass via lookalike domain

Hoxhunt adapts per user — high-clicker gets easier; low-clicker gets harder.
```

### Recipe 4: Theme rotation calendar

```text
Q1 (Jan-Mar):
- W-2 tax season (HR, IRS)
- New Year benefits (HR enrollment)
- "Important New Policy" (IT, HR, exec)

Q2 (Apr-Jun):
- Mid-year performance review
- Vacation request approvals
- IT password expiry / MFA renewal

Q3 (Jul-Sep):
- Back-to-office logistics
- Open enrollment prep
- Vendor / contract renewals

Q4 (Oct-Dec):
- Holiday package delivery (UPS, FedEx)
- Year-end finance close
- Charity / donation requests
- Gift card scams
- "Year-end bonus" announcements (BEC)

Continuous:
- BEC: invoice change request to finance
- Calendar invite spoof
- Microsoft 365 / Workspace "unusual sign-in"
- Workplace tool spoofing (Slack, Teams, Asana)
- AI assistant prompt-injection lures (NEW 2026)
```

### Recipe 5: KnowBe4 phishing campaign API

```bash
# https://developer.knowbe4.com/
# List campaigns
curl -X GET "https://us.api.knowbe4.com/v1/phishing/campaigns" \
  -H "Authorization: Bearer $KNOWBE4_API_KEY"

# Phishing test results
curl -X GET "https://us.api.knowbe4.com/v1/phishing/security_tests" \
  -H "Authorization: Bearer $KNOWBE4_API_KEY"

# Per-recipient
curl -X GET "https://us.api.knowbe4.com/v1/phishing/security_tests/<test_id>/recipients" \
  -H "Authorization: Bearer $KNOWBE4_API_KEY"
```

### Recipe 6: Hoxhunt simulation API

```bash
curl -X GET "https://api.hoxhunt.com/v1/teams/<id>/training-completion" \
  -H "Authorization: Bearer $HOXHUNT_API_KEY"

curl -X GET "https://api.hoxhunt.com/v1/users/<userId>/risk-score" \
  -H "Authorization: Bearer $HOXHUNT_API_KEY"
```

### Recipe 7: Arsen AI deepfake / voice sim

```bash
# https://www.arsen.co/ — for executive-focused programs
# Voice clone (synthetic of executive — with consent) + targeted call
# Engagement: high-stakes execs + finance
# Configurable scenarios:
# - Wire-transfer urgency
# - MFA code request from "IT"
# - Vendor invoice change confirm
# Reports include: pickup rate + engagement duration + outcome
```

### Recipe 8: Campaign design template

```markdown
# Phishing Campaign — <Name>

**Campaign ID:** <P-2026-Q2-001>
**Launch date:** <YYYY-MM-DD>
**Vector:** <Email / SMS / Voice / QR / Deepfake>
**Audience:** <All / Department / Tier 1 only>
**Difficulty:** <Easy / Medium / Hard>
**Theme:** <e.g. "Q2 Performance Review Available">
**Lure:** <"Click to view your review">
**Landing page:** <pixel-perfect fake login OR just-in-time learning page>

## Indicators of phish (training reinforcement)
- Sender domain mismatch (review@perform-revw.com vs perform-review.com)
- Urgency language
- Unsolicited link
- Generic greeting / mismatch with personalized context

## Expected metrics
- Click rate target: <%>
- Report rate target: <%>
- Credential entry target: <% (0% ideally)>

## Just-in-time learning content (on click)
- 1-min video: "Why this was a phish + how to spot it"
- Linked policy reference

## Reporting
- Daily during campaign (3-day duration typical)
- Final report 7 days post-campaign
- Trend analysis quarterly

---
*Disclaimer per template.*
```

### Recipe 9: Severity escalation per user

```text
First fail (click without credential):
- Just-in-time learning
- Logged on risk profile
- No notification to manager

Second fail (within 12 months):
- Just-in-time learning
- Manager notified (informational)
- Increased monitoring on sensitive actions

Third fail (within 12 months):
- 1:1 coaching with security team
- Manager + HR involved
- Custom training plan

Fourth fail (within 12 months):
- Senior management review
- Performance review note
- Re-attestation of AUP + acceptance of consequences

Credential entry (immediate, regardless of count):
- Immediate password reset
- Manager + IT notified
- Mandatory re-training within 7 days
- Account flagged for elevated monitoring
```

### Recipe 10: Measurement dashboard

```text
Per campaign:
- Sent count
- Opened (if email)
- Clicked (% of sent)
- Credential entered (% of clicked)
- Reported (% of sent) — most important metric
- Dwell time (sent → action)

Per user (rolling 12 months):
- Click count + trend
- Report count + trend
- Credential entry count
- Risk score (vendor-aggregated)

Per cohort:
- By department
- By role
- By tenure (new vs > 1yr)
- By region / language
- By manager span

Industry benchmark (KnowBe4 PII report):
- Overall click rate: 27.6% (baseline) → 5.4% (12mo of training)
- Knowledge-worker baseline higher than blue-collar baseline
- Healthcare + finance baseline elevated
```

### Recipe 11: BEC / vendor impersonation defense

```text
BEC = Business Email Compromise. FBI IC3 estimates $51B+ losses 2013-2023.

Common BEC scenarios:
1. CEO impersonation → CFO/finance ("urgent wire transfer")
2. Vendor invoice change ("update bank account for invoice payment")
3. Payroll diversion (HR-targeted)
4. Gift card scams (CEO to assistant)
5. Real-estate (closing fund diversion)

Phish-sim themes:
- Reply-spoof from CEO domain (similar lookalike)
- Vendor "we changed banks; here's new wire info"
- HR "update your direct deposit"

Controls trained:
- Out-of-band verification (known phone number, not number in email)
- Multi-person approval for wire changes
- Dual-control on payroll changes
- Vendor change verification SOP
- Suspicious email reporting
```

### Recipe 12: QR phishing (quishing) handling

```text
QR codes embed URLs without visible URL inspection. Surging 2026.

Common quishing vectors:
- Posters / flyers in office
- Emails containing QR
- SMS containing QR
- Physical mailers
- Restaurant menus / parking meters

Phish-sim:
- Email "scan QR to access Q2 bonus"
- "Scan QR to set up free Wi-Fi"
- "Scan QR to verify identity"

Controls trained:
- Don't scan QR from untrusted source
- If scanning, preview URL before navigating
- Don't enter credentials from QR-loaded page
- Verify out-of-band

Platform support: KnowBe4 + Hoxhunt + Arsen + SoSafe all offer QR sim 2026.
```

### Recipe 13: Reporting + handoff to SOC

```text
User-reported phish → SOC/IR:
1. User clicks "Report Phish" button (KnowBe4 PAB / Microsoft Report
   Message / Workspace tool).
2. Email captured + analyzed:
   - IOC extraction (URL, attachment hash, sender domain)
   - Cross-correlate with threat intel
3. Triage:
   - Confirmed phish → block at email gateway + endpoint + DNS
   - Phishing campaign sim (false alarm but rewarded reporting!) → 
     send confirmation
   - Genuine business email mistakenly reported → return to user
4. Org-wide alert if mass-targeting (Slack / Teams notification).
5. Incident response if credentials potentially compromised:
   - Force password + MFA reset
   - Account session revocation
   - Audit log review for affected user
```

## Examples

### Example 1: Stand up monthly phishing for SOC 2

**Goal:** Monthly phishing for 100-person SaaS for SOC 2 evidence.

**Steps:**
1. KnowBe4 KMSAT Diamond tier (includes phishing campaigns).
2. Configure monthly campaign cadence (Recipe 4).
3. Difficulty curve per Recipe 3.
4. Phish report button deployed (Microsoft Report Message + KnowBe4 PAB).
5. Severity escalation per Recipe 9.
6. Monthly dashboard (Recipe 10) to leadership.

**Result:** SOC 2 CC1.4 evidence; click rate drops 27% → 6% within 12 months.

### Example 2: Add deepfake sim for execs

**Goal:** Quarterly deepfake / voice sim for executive team.

**Steps:**
1. Engage Arsen.
2. Consent + recording of executive voices for cloning.
3. Quarterly sim: vishing call to finance from "CEO" requesting urgent wire.
4. Track: pickup rate + engagement duration + verification action taken.
5. Just-in-time coaching post-event.

**Result:** Executive + finance team prepared for AI-driven attacks.

### Example 3: Weekly phishing for finance team

**Goal:** Weekly cadence for finance team to address BEC risk.

**Steps:**
1. Sub-campaign in KnowBe4: finance audience only.
2. Theme rotation per Recipe 11.
3. Hoxhunt complement: behavioral / adaptive baseline.
4. Monthly 1:1 between security lead + CFO on results.
5. Reduce wire-change SOP friction via security-app integration.

**Result:** Finance click rate declines; reporting improves; BEC risk reduced.

## Edge cases / gotchas

- **Report rate > click rate as KPI.** Detection culture > avoidance only.
- **Shame-and-blame backfires.** Even repeat clickers handled via coaching + manager 1:1, not public shaming.
- **High-volume roles click more.** Finance / sales / support process high volume → higher base rate. Adjust expectations + interventions.
- **Customer-domain phishing** — never target customers from sim platform; always internal.
- **Senior leadership exemption** weakens program. Sim them too (with their knowledge of program existence).
- **Test consent** — some jurisdictions (DE works councils, EU CCB) require notice that sim exists.
- **Real phish during sim** — train SOC to recognize sim-vs-real; tag sim emails with internal header.
- **Click-only ≠ credential entry.** Click alone is far less severe; weight credential-entry heavier.
- **Easy-target theme during stressful times** (Q4 holidays, RIF) feels mean. Adjust themes to context.
- **Vendor impersonation in sim feels unfair** if the impersonated vendor is a real partner — coordinate or use generic.
- **Deepfake sim consent** — exec voice clones require written consent + retention controls.
- **Reporting tool fatigue** — too many "Report Phish" alerts of real spam dilute signal. Triage hierarchy.
- **Phish-sim platform whitelisting at email gateway** — coordinate to avoid spam folder kill of sim.
- **Don't simulate gift card scams during holiday season** — too punitive.

> ⚠ **This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.**

## Sources

- [KnowBe4 Phishing](https://www.knowbe4.com/phishing)
- [Hoxhunt Phishing Simulation](https://hoxhunt.com/phishing-simulation)
- [Arsen](https://www.arsen.co/)
- [SoSafe Phishing Simulation](https://sosafe-awareness.com/products/phishing-simulation/)
- [KnowBe4 Phishing Benchmark Report](https://www.knowbe4.com/resource-center/free-research-tools/phishing-benchmark-report)
- [FBI IC3 Annual Report (BEC)](https://www.ic3.gov/AnnualReport)
- [APWG Phishing Activity Trends](https://apwg.org/trendsreports/)
- [Microsoft Report Message Add-in](https://learn.microsoft.com/en-us/defender-office-365/submissions-outlook-report-messages)
- [Microsoft Defender for Office 365 Attack Simulation Training](https://learn.microsoft.com/en-us/defender-office-365/attack-simulation-training-get-started)
- [Adaptive Security](https://www.adaptivesecurity.com/)
- [Verizon DBIR](https://www.verizon.com/business/resources/reports/dbir/)
