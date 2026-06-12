<!--
Sources: https://whichpayroll.com/features/eor-api-access
         https://www.deel.com/blog/deel-vs-remote-honest-employer-of-record-service-comparison/
         https://nativeteams.com/blog/deel-vs-oyster
         https://alcor.com/velocity-global-alternatives/
Deel = 150+ countries, BEST DEV SURFACE (only EOR with public API + sandbox + webhooks).
Remote = 100+ owned entities + partners. Oyster = 180+ EE experience focus. Pebl = formerly Velocity Global (rebrand Sept 2025), AI Alfie + 48h.
-->
# PEO / EOR — Global Hiring — Deel / Remote / Oyster / Pebl / G-P — SKILL

Hire employees globally without setting up local entities. EOR (Employer of Record) compares: country coverage, owned-entity vs partner-network, fees, sandbox availability, API depth, benefits. Default to Deel for API-driven flows (only EOR with sandbox + webhooks pre-contract); Oyster for employee experience; Pebl for AI-assisted 48-hour onboarding; G-P for enterprise.

## When to use

- Hiring a full-time employee in a country where you have no entity.
- Converting a contractor to an employee in their home country.
- Compliance review across 5+ countries.
- Trigger phrases: "EOR", "PEO", "global hire", "international employee", "Deel", "Remote", "Oyster", "Pebl", "Velocity Global", "G-P", "Globalization Partners".

## Setup

```bash
export DEEL_TOKEN="xxx"           # https://developer.deel.com — sandbox + webhooks
export DEEL_SANDBOX="https://api-sandbox.letsdeel.com/rest/v2"
export DEEL_PROD="https://api.letsdeel.com/rest/v2"

export REMOTE_TOKEN="xxx"         # https://remote.com/api-docs — Public API
export OYSTER_TOKEN="xxx"         # https://oysterhr.com — partner API
export PEBL_TOKEN="xxx"           # https://pebl.com — formerly Velocity Global
export GP_TOKEN="xxx"             # https://www.globalization-partners.com
```

## Common recipes

### Recipe 1: Country / vendor selection matrix
```yaml
choose:
  api_first_workflow:
    primary: Deel
    why: Only EOR with public API + sandbox + webhooks pre-contract; full workforce platform
  owned_entities_priority:
    primary: Remote.com
    why: 100+ countries; ~25 owned entities; straightforward
  employee_experience_emphasis:
    primary: Oyster
    why: 180+ countries; employee-first design
  speed_with_ai_assist:
    primary: Pebl (formerly Velocity Global, rebranded Sept 2025)
    why: AI assistant Alfie; 48-hour onboarding claim
  enterprise_brand_safety:
    primary: G-P (Globalization Partners)
    why: Established enterprise player; risk-averse buyers
  hris_already_rippling:
    primary: Rippling EOR
    why: Bundle within existing Rippling subscription
```

### Recipe 2: Deel sandbox key (no contract needed)
```bash
# Deel is the only EOR exposing pre-sales sandbox
curl -s "$DEEL_SANDBOX/contracts?contract_type=eor" \
  -H "Authorization: Bearer $DEEL_TOKEN" \
  | jq '.data[] | {id, country, status, start_date}'
```

### Recipe 3: Quote a country (Deel)
```bash
curl -s "$DEEL_SANDBOX/eor/cost-calculator" \
  -H "Authorization: Bearer $DEEL_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "country":"GB",
    "salary_amount":75000,
    "salary_currency":"GBP",
    "benefits_package":"standard"
  }'
# Response: total employer cost (gross salary + statutory contributions + Deel EOR fee)
```

### Recipe 4: Country-specific employer-cost matrix (rough multipliers)
```yaml
# Total employer cost ≈ gross salary × multiplier (rough; varies year + tier)
employer_cost_multipliers:
  US:    1.13     # FICA + FUTA + state UI + WC + Deel fee
  UK:    1.20     # ER NIC + apprenticeship levy + pension + Deel
  DE:    1.36     # ER social contributions are heavy
  FR:    1.44     # Highest end; charges sociales patronales
  ES:    1.34
  IT:    1.40
  NL:    1.28
  PL:    1.22
  BG:    1.20     # Bulgaria — popular eng outsource geo
  RO:    1.28
  PT:    1.30
  IE:    1.18
  CA:    1.18
  AU:    1.18     # super + WC
  IN:    1.18
  BR:    1.55     # Heaviest among major hubs
  MX:    1.28
  AR:    1.45
  SG:    1.20
  JP:    1.27
# Deel EOR markup typically $400-700/mo per hire or 9-12% of salary
```

### Recipe 5: Create EOR employee (Deel)
```bash
curl -s -X POST "$DEEL_PROD/eor/contracts" \
  -H "Authorization: Bearer $DEEL_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "country":"GB",
    "title":"Senior Product Manager",
    "salary_amount":75000,
    "salary_currency":"GBP",
    "start_date":"2026-08-01",
    "benefits_package":"standard_uk",
    "scope_of_work":"...",
    "worker":{"first_name":"Sam","last_name":"O","email":"sam@example.com"}
  }'
```

### Recipe 6: Webhook listener (Deel — pre-contract)
```bash
# Only Deel exposes webhooks before signing
curl -s -X POST "$DEEL_PROD/webhooks" \
  -H "Authorization: Bearer $DEEL_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "url":"https://hooks.example.com/deel",
    "events":["contract.signed","contract.terminated","payroll.run.completed","contractor.invoice.issued"]
  }'
```

### Recipe 7: Remote.com hire
```bash
curl -s -X POST "https://gateway.remote.com/v1/employments" \
  -H "Authorization: Bearer $REMOTE_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "country":"DE",
    "job_title":"Senior Engineer",
    "annual_gross_salary":85000,
    "currency":"EUR",
    "personal_email":"dev@example.com",
    "first_name":"Anna","last_name":"M",
    "expected_start_date":"2026-08-01"
  }'
```

### Recipe 8: Termination across vendors
```bash
# Deel
curl -s -X POST "$DEEL_PROD/eor/contracts/<id>/terminate" \
  -H "Authorization: Bearer $DEEL_TOKEN" \
  -d '{"termination_date":"2026-09-30","reason":"performance","notice_period_days":30}'

# Remote
curl -s -X POST "https://gateway.remote.com/v1/employments/<id>/termination" \
  -H "Authorization: Bearer $REMOTE_TOKEN" \
  -d '{"effective_date":"2026-09-30","reason_for_termination":"performance"}'
```

### Recipe 9: Multi-country payroll dashboard (Python)
```python
import requests, os
from collections import defaultdict
DEEL = {'Authorization': f"Bearer {os.environ['DEEL_TOKEN']}"}
contracts = requests.get(f"{os.environ['DEEL_PROD']}/contracts", headers=DEEL).json()
by_country = defaultdict(list)
for c in contracts['data']:
    by_country[c['country']].append({'name': c['worker']['name'], 'salary': c['salary_amount'], 'ccy': c['salary_currency']})
for country, ws in by_country.items():
    total = sum(w['salary'] for w in ws)
    print(f"{country}: {len(ws)} employees, {total:,} {ws[0]['ccy']} gross/yr")
```

### Recipe 10: Right-to-work + visa coordination
```yaml
# EOR provides the legal employer; visa / work permit still per-country
visa_status_required_per_hire:
  - Right-to-work proof (passport, visa, work permit)
  - For non-citizen hires in EU: residence permit + work permit
  - For US H-1B etc: EOR cannot sponsor (EOR is local entity, not the visa sponsor)
  - For UK skilled-worker visa: EOR can sponsor in many cases (verify per provider)
# Defer to legal-counsel for binding visa eligibility per worker.
```

### Recipe 11: PEO vs EOR decision
```yaml
peo_vs_eor:
  peo:
    when: Company has its own local entity, wants co-employment + bundled HR/benefits
    examples: [Justworks (US), TriNet (US), Sequoia (US)]
    pricing: % of payroll (2-12%)
  eor:
    when: Company has NO local entity in that country
    examples: [Deel, Remote, Oyster, Pebl, G-P, Multiplier, Rippling EOR]
    pricing: Flat fee per employee ($400-700/mo) or % (9-12%)
```

### Recipe 12: Benefits package tier comparison
```yaml
typical_uk_benefits_via_eor:
  basic:
    pension: 3% ER + 5% EE (auto-enrol minimum)
    leave: 28 days statutory
    sick_pay: SSP statutory
  standard:
    pension: 5-8% ER
    private_health: yes (vitality / bupa typical)
    life_insurance: 4x salary
    leave: 25 paid + bank holidays
  enhanced:
    pension: 10% ER
    private_health: family
    dental: yes
    life_insurance: 4-6x
    income_protection: yes
    leave: 28 paid + bank holidays + birthday
```

## Examples

### Example 1: Hire UK senior PM via Deel EOR
**Goal:** Live PM seat in 3 weeks.
**Steps:**
1. Recipe 3: cost calculator — UK £75k → £90k all-in.
2. Recipe 5: create contract; worker self-onboards (KYC, bank, P45/P46).
3. Day-1 starts; payroll handled by Deel via UK PAYE.
4. Recipe 6: webhook → Slack #people-ops alerts on milestones.

**Result:** Compliant UK hire; no UK entity needed.

### Example 2: Compare Deel vs Remote vs Oyster for German hire
**Goal:** Pick cheapest + best fit for DE €85k engineer.
**Steps:**
1. Recipe 3 cost calc for Deel.
2. Equivalent quotes from Remote + Oyster.
3. Recipe 4 multipliers as sanity check.
4. Choose Remote (owned DE entity → cleaner ER NIC handling) or Deel (faster API + webhooks).

**Result:** Best-priced + fit vendor selected.

### Example 3: Mass-convert 5 contractors to employees
**Goal:** Reduce IP / misclassification risk.
**Steps:**
1. Audit current contractors: country, fees, work-product IP terms.
2. Quote each via Recipe 3.
3. Deel "Convert contractor → EOR" workflow.
4. Communicate change to contractors (likely net-pay drop due to ER contributions).
5. Termination of contractor agreements + new EOR contracts.

**Result:** Cleaner IP chain, compliant employer model.

## Edge cases / gotchas

- **EOR cannot sponsor visas everywhere.** US H-1B / H-2B impossible. UK Skilled Worker varies by EOR. **Defer to `legal-counsel` + immigration adviser.**
- **EOR + foreign-source income tax for founder.** Founders on global payroll create tax complications back home. Personal tax review needed.
- **IP assignment in EOR contract.** Default EOR contracts may not vest IP in your US/UK parent. Side-letter / DPA for IP assignment required. **Defer to `legal-counsel`.**
- **Mass redundancies trigger consultation duties.** EU collective consultation (Works Councils, redundancy law) applies even via EOR. **Defer to `legal-counsel`.**
- **Switching EOR vendors.** Re-papering with new vendor + 30-90 day notice; benefits restart. Avoid mid-contract switch.
- **Contractor in country A with company in country B.** B may consider this as A having a permanent establishment in B (tax nexus). Limit B days < 183/yr.
- **Pebl (formerly Velocity Global, Sept 2025).** Brand transition still in progress; double-check contract names + API endpoints if existing relationship.
- **Sanctions / OFAC.** EOR hires in CU, IR, KP, SY (US sanctions) — disallowed for US-domiciled companies. **Defer to `legal-counsel`.**
- **Deel only EOR with sandbox** — others require sales contract before any API access. Plan procurement timeline differently.
- **Webhook signature verification.** Recipe 6 — verify HMAC-SHA256 with Deel signing secret; otherwise endpoint is spoof-target.
- **EOR vs entity-of-record vs PEO confusion.** Use Recipe 11 to clarify which you actually need.

## Sources

- WhichPayroll — EOR API Access 2026: https://whichpayroll.com/features/eor-api-access
- Deel — Deel vs Remote 2026: https://www.deel.com/blog/deel-vs-remote-honest-employer-of-record-service-comparison/
- Native Teams — Deel vs Oyster: https://nativeteams.com/blog/deel-vs-oyster
- Alcor — Pebl (Velocity Global) Alternatives 2026: https://alcor.com/velocity-global-alternatives/
- Deel Developer Portal: https://developer.deel.com/
- Remote Public API: https://developer.remote.com/
- Oyster Partners: https://www.oysterhr.com/integrations
- G-P (Globalization Partners): https://www.globalization-partners.com/
