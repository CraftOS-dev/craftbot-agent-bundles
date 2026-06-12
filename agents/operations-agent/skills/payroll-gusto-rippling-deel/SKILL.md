<!--
Sources: https://johngalt-finance.com/gusto-vs-justworks-vs-rippling-payroll-hr-2026/
         https://www.hibob.com/blog/rippling-vs-gusto-vs-hibob/
Gusto = SMB <50 EE. Rippling = 50+ with HRIS+IT+payroll in one. Deel = global contractors / EOR.
Justworks = PEO with enterprise benefits for small teams. HiBob = HRIS-only (BYO payroll).
-->
# Payroll Setup — Gusto / Rippling / Deel / Justworks — SKILL

Stand up payroll: company setup, employee enrollment, multi-state nexus, contractor onboarding, benefits sync, off-cycle runs, garnishments, year-end (W-2 / 1099 / W-9 / 1042-S). Stage-based picks: Gusto < 50, Rippling 50+ HRIS+IT bundle, Deel for global contractors / EOR, Justworks for PEO benefits-leverage, HiBob HRIS + BYO payroll for mid-market.

## When to use

- New company → first payroll provider.
- Adding a new state → nexus + UI registration.
- Onboarding a contractor (1099 / international).
- Annual: W-2 / 1099 filing, year-end true-ups.
- Garnishment intake.
- Trigger phrases: "payroll", "Gusto", "Rippling", "Deel", "Justworks", "HiBob", "1099", "W-2", "garnishment", "multi-state", "off-cycle".

## Setup

```bash
export GUSTO_API_KEY="xxx"      # https://docs.gusto.com — Embedded partner OAuth
export RIPPLING_KEY="xxx"       # https://developer.rippling.com
export DEEL_TOKEN="xxx"         # https://developer.deel.com — public docs + sandbox
export HIBOB_USER="xxx"
export HIBOB_TOKEN="xxx"
```

Sandbox availability:
- **Deel** — public sandbox + webhooks; **only EOR with this**.
- **Rippling** — sandbox tenant on partner program.
- **Gusto** — sandbox for embedded partners.
- **HiBob** — sandbox via demo tenant.

## Common recipes

### Recipe 1: Stage / company-shape platform selection
```yaml
choose:
  smb_under_50_us_only:
    primary: Gusto
    cost: "$40/mo + $6/employee + bens"
    why: Cleanest payroll UX; multi-state; contractors built-in
  growth_50_plus_hris_it_payroll_one:
    primary: Rippling
    why: Unique MDM + SSO + app provisioning; one HRIS for everything
  peo_small_team_wants_big_co_benefits:
    primary: Justworks
    why: Co-employment via PEO; bring enterprise benefit rates to a 10-person team
  hris_only_byo_payroll:
    primary: HiBob
    why: Strong EU presence; mid-market culture-led; integrate with leading payroll
  global_contractors_eor:
    primary: Deel
    why: 150+ countries; only EOR with public API + sandbox + webhooks pre-contract
  global_contractors_alt:
    primary: Remote.com or Oyster or Pebl
    why: Remote = 100+ countries straightforward; Oyster = 180+ employee experience; Pebl = AI Alfie + 48h onboarding
```

### Recipe 2: Create company (Gusto Embedded — Partner)
```bash
curl -s -X POST "https://api.gusto.com/v1/partner_managed_companies" \
  -H "Authorization: Bearer $GUSTO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "user":{"first_name":"Founder","last_name":"Name","email":"f@co.com"},
    "company":{"name":"Acme Inc","trade_name":"Acme","ein":"<EIN>"}
  }'
```

### Recipe 3: Add employee (Gusto)
```bash
curl -s -X POST "https://api.gusto.com/v1/companies/<co>/employees" \
  -H "Authorization: Bearer $GUSTO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "first_name":"Avery","last_name":"Lee",
    "email":"avery@co.com",
    "ssn":"<SSN>",
    "date_of_birth":"1995-04-12",
    "home_address":{"street_1":"...","city":"NYC","state":"NY","zip":"10001"}
  }'

# Then add compensation
curl -s -X POST "https://api.gusto.com/v1/employees/<emp>/compensations" \
  -H "Authorization: Bearer $GUSTO_API_KEY" -H "Content-Type: application/json" \
  -d '{"rate":"185000","payment_unit":"Year","flsa_status":"Exempt","effective_date":"2026-08-01"}'
```

### Recipe 4: Add a new state (multi-state nexus)
```bash
# Gusto — declare new state work location → triggers state UI registration prompts
curl -s -X POST "https://api.gusto.com/v1/companies/<co>/locations" \
  -H "Authorization: Bearer $GUSTO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "street_1":"...","city":"Boston","state":"MA","zip":"02108","is_remote":true
  }'

# Gusto then provides a checklist of MA filings:
# - MA DOR — withholding registration
# - MA DUA — unemployment insurance
# - MA WC — workers' comp insurance
# - PFML notice posting
```

### Recipe 5: 1099 contractor onboarding (Gusto)
```bash
curl -s -X POST "https://api.gusto.com/v1/companies/<co>/contractors" \
  -H "Authorization: Bearer $GUSTO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "type":"Individual",
    "first_name":"Jules","last_name":"K",
    "email":"jules@example.com",
    "wage_type":"Hourly",
    "hourly_rate":"150.00",
    "self_onboarding":true
  }'
# Gusto sends contractor a self-onboarding link to add W-9 + bank info.
```

### Recipe 6: International contractor (Deel)
```bash
# Create contractor agreement (sandbox)
curl -s -X POST "https://api.letsdeel.com/rest/v2/contracts" \
  -H "Authorization: Bearer $DEEL_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "title":"Sr Software Engineer — Sofia",
    "type":"pay_as_you_go_time_based",
    "scope_of_work":"...",
    "rate":150,
    "currency":"USD",
    "frequency":"monthly",
    "worker":{"email":"dev@example.com","country_code":"BG"}
  }'
```

### Recipe 7: Deel EOR — full-time hire in another country
```bash
curl -s -X POST "https://api.letsdeel.com/rest/v2/eor/contracts" \
  -H "Authorization: Bearer $DEEL_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "title":"Senior Product Manager — UK",
    "country":"GB",
    "salary_amount":75000,
    "salary_currency":"GBP",
    "start_date":"2026-08-01",
    "benefits_package":"standard_uk",
    "worker":{"first_name":"Sam","last_name":"O","email":"sam@example.com"}
  }'
```

### Recipe 8: Off-cycle payroll (bonus / commission)
```bash
curl -s -X POST "https://api.gusto.com/v1/companies/<co>/payrolls" \
  -H "Authorization: Bearer $GUSTO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "check_date":"2026-07-15",
    "payroll_type":"off_cycle",
    "off_cycle_reason":"Bonus",
    "employee_compensations":[
      {"employee_id":"<emp>","fixed_compensations":[{"name":"Bonus","amount":"5000"}]}
    ]
  }'
```

### Recipe 9: Garnishment intake
```bash
curl -s -X POST "https://api.gusto.com/v1/employees/<emp>/garnishments" \
  -H "Authorization: Bearer $GUSTO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "active":true,
    "amount":"500.00",
    "description":"Child Support — CA Order #...",
    "court_ordered":true,
    "deduct_as_percentage":false,
    "pay_period_maximum":"500.00"
  }'
```

### Recipe 10: Year-end W-2 / 1099 reconciliation
```python
# Pull payroll YTD, compare to GL (Xero), flag deltas
import requests, os
GUSTO = {'Authorization': f"Bearer {os.environ['GUSTO_API_KEY']}"}
emps = requests.get('https://api.gusto.com/v1/companies/<co>/employees', headers=GUSTO).json()
for e in emps:
    ytd = requests.get(f"https://api.gusto.com/v1/employees/{e['id']}/payroll_summary?year=2026", headers=GUSTO).json()
    print(e['email'], ytd['ytd_gross'], ytd['ytd_taxes'], ytd['ytd_net'])
# Year-end action: generate W-2 (Gusto handles); contractor 1099 too.
```

### Recipe 11: Rippling unified hire (HRIS + IT + Payroll)
```bash
# Rippling: hire creates HRIS profile, ships device, provisions SaaS apps, runs first paycheck
curl -s -X POST "https://api.rippling.com/platform/api/employees" \
  -H "Authorization: Bearer $RIPPLING_KEY" -H "Content-Type: application/json" \
  -d '{
    "first_name":"Avery","last_name":"Lee",
    "work_email":"avery@co.com",
    "title":"Sr Ops Analyst",
    "start_date":"2026-08-01",
    "compensation":{"annual_salary":185000,"currency":"USD"},
    "team_id":"<ops-team>",
    "device_profile":"standard_macbook_pro_14",
    "apps":["google-workspace","slack","github","notion","linear"]
  }'
```

## Examples

### Example 1: Stand up Gusto for a 12-person startup
**Goal:** First payroll in 7 days, two states (CA + NY).
**Steps:**
1. Recipe 1: Gusto picked.
2. Recipe 2: company setup.
3. Recipe 4: CA + NY locations registered → Gusto guides EDD + DOL filings.
4. Recipe 3: bulk add employees.
5. Benefits broker connect (Gusto-recommended).
6. First payroll run; verify YTD ledger sync to Xero.

**Result:** First paycheck on time; multi-state nexus filed; benefits broker tied.

### Example 2: Hire a contractor in Bulgaria
**Goal:** Onboard developer @ €5k/mo on a clean contract.
**Steps:**
1. Recipe 1: Deel for international contractor.
2. Recipe 6: contractor agreement w/ BG-localized terms.
3. Worker self-onboards (KYC + bank).
4. Monthly invoices auto-generated; payment routes via Deel.

**Result:** Compliant cross-border contractor at < 5% Deel fee.

### Example 3: Bonus off-cycle
**Goal:** $5k spot bonus paid Friday.
**Steps:**
1. Recipe 8: off-cycle payroll.
2. Verify withholding (supplemental rate 22% federal default, plus state).
3. Notify employee + manager.

**Result:** Paid same week, withholding correct.

## Edge cases / gotchas

- **State UI registrations.** Adding a state isn't instant; CA EDD 10-15 business days. Don't promise Day-1 paycheck across-state without 2 weeks lead.
- **Workers' Comp.** Required in nearly every state; Gusto offers pay-as-you-go via The Hartford / NEXT; verify coverage before first paycheck.
- **Contractor misclassification.** 1099 vs W-2 hinges on control, training, integration. CA AB5 (ABC test) is strict. **Defer to `legal-counsel`.**
- **Deel + tax residency.** Worker in BG paid via Deel US entity — must not work > 183 days in another country without Deel re-routing. Deel flags but doesn't enforce.
- **PEO co-employment quirks.** Justworks holds workers' comp + group health under their EIN. Switching off Justworks = re-papering everything; plan 90 days.
- **HiBob "BYO payroll".** HiBob is HRIS-only; you still need Gusto / Rippling / ADP for actual payroll. Integration depth varies.
- **Off-cycle withholding.** Supplemental rate is 22% federal up to $1M; > $1M = 37%. State varies (CA 10.23% supplemental).
- **Garnishments precedence.** Multiple garnishments compete for finite disposable income (CCPA limits). Order: support, IRS levy, then private creditor. **Defer to `legal-counsel`.**
- **W-2 corrections (W-2c).** Filed after Jan 31 are penalty-bearing. Run YE close in early Jan with manager attestation.
- **Year-end true-up: SCH C, fringe benefits, ISO/NSO exercises.** Must hit YE payroll; coordinate with finance.
- **Rippling pricing tiers.** HRIS, IT, Payroll, Finance modules sold separately; check what's included; module-creep at renewal.
- **Defer to `legal-counsel` for binding state-specific final-pay timing (CA same-day, MA same-day, NY next regular payday), wage-and-hour exposure, and exempt vs non-exempt FLSA classification.**

## Sources

- John Galt Finance — Gusto vs Justworks vs Rippling 2026: https://johngalt-finance.com/gusto-vs-justworks-vs-rippling-payroll-hr-2026/
- HiBob — Rippling vs Gusto vs HiBob: https://www.hibob.com/blog/rippling-vs-gusto-vs-hibob/
- Deel — Deel vs Remote 2026: https://www.deel.com/blog/deel-vs-remote-honest-employer-of-record-service-comparison/
- Gusto Embedded docs: https://docs.gusto.com/embedded-payroll
- Rippling Public API: https://developer.rippling.com/
- Deel Public API + sandbox: https://developer.deel.com/
- HiBob API: https://apidocs.hibob.com/
- CA AB5: https://www.dir.ca.gov/dlse/faq_independentcontractor.htm
