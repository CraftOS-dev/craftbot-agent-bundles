<!--
Source: https://www.holloway.com/g/equity-compensation/sections/the-option-pool
Source: https://www.thestartuplawblog.com/blog/equity-compensation-plan-design-startup-guide/
Source: https://review.firstround.com/The-Right-Way-to-Grant-Equity-to-Your-Employees
Reference role.md: "Equity comp design playbook"
-->

# Equity comp design — option pool + evergreen + grant policy

Designs the option pool, evergreen refresh, and per-employee grant policy. Industry standards: Initial pool 10-20% fully diluted; tech-sector IPO target 8-12%; evergreen 3-5% annual (Series A investors push back beyond 3%); per-employee evergreen 25% of new-hire grant at current FMV (smooths cliffs). ISO/NSO/RSU decisions, refresh triggers, ASC 718 expense modeling.

## When to use

- Pre-Series A: size initial pool against next 12-18mo hiring plan.
- Post-Series A: design evergreen + refresh policy.
- IPO prep: convert to public-grade equity plan + ESPP.
- Compensation review for senior hire / promotion / retention.
- Trigger phrases: "option pool", "evergreen", "equity comp", "grant policy", "ISO vs NSO vs RSU", "refresh grant", "equity refresh".

NOT for: cap-table mechanics (use Carta/Pulley directly); 409A (use `409a-valuation-negotiation`).

## Setup

```bash
uvx --with pandas --with numpy --with scipy python -c "import pandas, scipy"

# Carta / Pulley APIs (recipient supplies)
export CARTA_API_KEY="<from Carta>"
export PULLEY_API_KEY="<from Pulley>"

# Compensia / Pay Governance / Pearl Meyer for benchmarking (engaged)
```

## Pool sizing framework

```
INITIAL POOL (pre-seed → Series A)
  Target: 10-20% fully diluted; 12-15% typical
  Rationale: 12-18mo of hires at planned roles × planned grants
  Series A negotiation: investors push pre-money pool top-up to 12-15%

GROWTH STAGE EVERGREEN (Series B+)
  Annual evergreen: 3-5% increase to total FD shares
  Series A investors typical pushback at >3%
  Public IPO standard: 4-5% (often via "Compensation Plan" formula)

PER-EMPLOYEE EVERGREEN (First Round playbook)
  Annual grant = 25% of new-hire-equivalent grant for same role/level
  At current FMV (post-refresh 409A)
  Smooths cliffs; reduces flight risk
```

## Equity-instrument decision matrix

```
ISO (Incentive Stock Option)
  ✓ For employees
  ✓ Tax-advantaged (no income tax at exercise IF held >2yr from grant, >1yr from exercise)
  ✗ AMT trap (bargain element triggers AMT)
  ✗ $100K rule (limit on $K of ISOs vesting per year)
  Use case: standard early-stage employee grants

NSO (Non-qualified Stock Option)
  ✓ For contractors, advisors, non-employee directors
  ✓ For employee grants beyond $100K ISO limit
  ✗ Income tax at exercise on bargain element
  Use case: contractors; senior hire grants exceeding ISO limit

RSU (Restricted Stock Unit)
  ✓ For late-stage / public-track
  ✓ No exercise required (auto-converts on vest)
  ✗ Income tax on vest (employee must sell some shares for taxes)
  ✗ Requires liquidity event for full value
  Use case: pre-IPO + post-IPO standard

RESTRICTED STOCK (Founders)
  ✓ For founders + earliest employees
  ✓ 83(b) election lets recipient pay tax now on low FMV
  ✗ Requires cash to "buy" (typically $0.0001/share)
  Use case: founders; pre-Series A hires
```

## Common recipes

### Recipe 1 — Pool sizing model

```python
import pandas as pd

def pool_sizing(headcount_plan, grant_table_by_role, total_fd_shares, current_pool_pct):
    """Compute required pool size for next 12-18 months of hiring."""
    total_planned_grants = 0
    for role, count in headcount_plan.items():
        per_grant_pct = grant_table_by_role.get(role, 0.001)
        total_planned_grants += count * per_grant_pct

    new_pool_pct_needed = total_planned_grants
    target_pool_pct = current_pool_pct + new_pool_pct_needed
    target_pool_shares = total_fd_shares * (target_pool_pct / (1 - target_pool_pct))
    return {
        "headcount_to_hire": sum(headcount_plan.values()),
        "total_planned_grants_pct": total_planned_grants,
        "current_pool_pct": current_pool_pct,
        "target_pool_pct": target_pool_pct,
        "shares_to_add": target_pool_shares - total_fd_shares * (current_pool_pct / (1 - current_pool_pct))
    }

# Series A SaaS: 25 hires next 12 months
headcount_plan = {"VP": 2, "Director": 5, "Senior IC": 10, "Mid IC": 8}
grant_table = {"VP": 0.012, "Director": 0.005, "Senior IC": 0.002, "Mid IC": 0.0008}
print(pool_sizing(headcount_plan, grant_table, 10_000_000, current_pool_pct=0.08))
```

### Recipe 2 — Per-role grant table (industry standard)

```python
GRANT_TABLE_BY_STAGE = {
    # % of fully diluted at hire
    "Pre-seed": {
        "Founder_addition": 0.10, "VP": 0.03, "Director": 0.015,
        "Senior IC": 0.005, "Mid IC": 0.002, "Junior IC": 0.0005
    },
    "Seed": {
        "VP": 0.02, "Director": 0.01, "Senior IC": 0.0035,
        "Mid IC": 0.0015, "Junior IC": 0.0005
    },
    "Series A": {
        "VP": 0.012, "Director": 0.005, "Senior IC": 0.002,
        "Mid IC": 0.0008, "Junior IC": 0.0003
    },
    "Series B": {
        "VP": 0.008, "Director": 0.003, "Senior IC": 0.0012,
        "Mid IC": 0.0005, "Junior IC": 0.00015
    },
    "Series C+": {
        "VP": 0.005, "Director": 0.0018, "Senior IC": 0.0007,
        "Mid IC": 0.0003, "Junior IC": 0.0001
    },
}
```

### Recipe 3 — Evergreen schedule

```python
def evergreen_schedule(starting_pool_pct, annual_increase_pct, years=5):
    """Annual evergreen adds to pool."""
    schedule = [{"year": 0, "pool_pct": starting_pool_pct}]
    pool = starting_pool_pct
    for yr in range(1, years + 1):
        pool += annual_increase_pct
        schedule.append({"year": yr, "pool_pct": pool})
    return pd.DataFrame(schedule)

print(evergreen_schedule(0.12, annual_increase_pct=0.04, years=5))
```

### Recipe 4 — Per-employee evergreen (First Round playbook)

```python
def per_employee_evergreen(role, level, new_hire_grant_pct, refresh_factor=0.25):
    """Annual refresh = 25% of what we'd grant new hire today."""
    annual_refresh = new_hire_grant_pct * refresh_factor
    return {
        "role": role,
        "level": level,
        "new_hire_equivalent_pct": new_hire_grant_pct,
        "annual_refresh_pct": annual_refresh
    }

# Series B Senior IC w/ 0.0012% new-hire equivalent
print(per_employee_evergreen("Senior IC", "L4", 0.0012, refresh_factor=0.25))
```

### Recipe 5 — ASC 718 expense modeling

```python
from scipy.stats import norm
import math

def asc718_expense(grant_value_per_share, total_shares, vesting_years=4):
    """Total compensation expense recognized over vesting period (straight-line)."""
    total_expense = grant_value_per_share * total_shares
    annual_expense = total_expense / vesting_years
    return {
        "total_expense": total_expense,
        "annual_expense": annual_expense,
        "vesting_years": vesting_years
    }

def black_scholes_option_value(spot, strike, time_years, rf, vol, dividend_yield=0):
    """Black-Scholes for option grant fair value (for ASC 718)."""
    d1 = (math.log(spot / strike) + (rf - dividend_yield + 0.5 * vol**2) * time_years) / (vol * math.sqrt(time_years))
    d2 = d1 - vol * math.sqrt(time_years)
    call = spot * math.exp(-dividend_yield * time_years) * norm.cdf(d1) - strike * math.exp(-rf * time_years) * norm.cdf(d2)
    return call

# Example: $2.85 FMV, $2.85 strike, 4yr expected, 4% rf, 65% vol
per_option_value = black_scholes_option_value(2.85, 2.85, 4, 0.04, 0.65)
print(f"Per-option BS value: ${per_option_value:.3f}")
print(asc718_expense(per_option_value, total_shares=50_000))
```

### Recipe 6 — Vesting + acceleration policies

```python
def vesting_policy(role, stage):
    """Standard policies."""
    base = {"vesting_years": 4, "cliff_months": 12, "vest_cadence": "monthly"}
    if role in ("founder", "executive"):
        base["acceleration"] = "double-trigger on CoC + involuntary termination"
    if stage in ("seed",):
        base["acceleration"] = "single-trigger CoC for early hires (negotiable)"
    return base
```

### Recipe 7 — Carta grant issuance

```bash
# Create new option grant via Carta API
curl -X POST "https://api.carta.com/v1/companies/$COMPANY_ID/grants" \
  -H "Authorization: Bearer $CARTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "stakeholder_id": "STAKEHOLDER_ID",
    "security_type": "ISO",
    "quantity": 25000,
    "strike_price_per_share": 2.85,
    "grant_date": "2026-08-15",
    "vesting_schedule_id": "STANDARD_4Y_1Y_CLIFF",
    "board_approval_date": "2026-08-10"
  }'
```

### Recipe 8 — Cap-table dilution from grants

```python
def grant_dilution(grant_shares, current_fd_shares, current_holder_shares):
    """Compute dilution impact of a single grant."""
    new_fd = current_fd_shares + grant_shares
    new_holder_pct = current_holder_shares / new_fd
    old_holder_pct = current_holder_shares / current_fd_shares
    return {
        "dilution_pp": (old_holder_pct - new_holder_pct) * 100,
        "dilution_pct_relative": (old_holder_pct - new_holder_pct) / old_holder_pct,
        "new_fd_shares": new_fd
    }

print(grant_dilution(25_000, current_fd_shares=10_000_000, current_holder_shares=2_500_000))
```

### Recipe 9 — Comp benchmarking via Pave / Carta / Compensia

```python
COMP_DATA_SOURCES = {
    "Pave": {"price": "Free for free-tier; $X paid", "coverage": "Tech-focused; 3K+ companies"},
    "Carta": {"price": "Free with Carta cap table sub", "coverage": "Carta-managed companies; reflects narrower set"},
    "Levels.fyi": {"price": "Free", "coverage": "Self-reported; tech-heavy"},
    "OptionImpact (Advanced HR)": {"price": "$X/yr", "coverage": "VC-backed companies"},
    "Compensia / Pay Governance / Pearl Meyer": {"price": "Project-based", "coverage": "Custom; for executives + board"}
}
```

### Recipe 10 — Refresh trigger checklist

```
Equity refresh triggered by:
  □ Tenure: ≥18-24 months since last grant
  □ Promotion: role / level increase
  □ Significant role expansion
  □ Performance: top-quartile / "exceeds expectations"
  □ Retention risk: at risk of departure
  □ Material company event: large round, M&A, IPO prep

NOT triggered by:
  ✗ Cost-of-living adjustment (handle via base salary)
  ✗ Standard "annual" refresh without performance basis
```

## Examples

### Example 1: Series A pool sizing

**Goal:** Size pool for next 12 months hiring at $30M post-money.

**Steps:**
1. Recipe 1 + 2 → headcount × grant table.
2. Account for Series A investors pushing pool to 12%.
3. Series A pre-money top-up = founders absorb dilution.
4. Recipe 7 → set up Carta plan.
5. Recipe 5 → ASC 718 expense forecast.

**Result:** Defensible pool size.

### Example 2: Senior IC evergreen at Series B

**Goal:** Annual refresh policy for 50+ Senior ICs at Series B.

**Steps:**
1. Recipe 4 → per-employee evergreen calculation.
2. Recipe 10 → trigger conditions (tenure + performance).
3. Recipe 9 → benchmark Senior IC compensation total (cash + equity).
4. Recipe 5 → ASC 718 expense forecast.
5. Approve at comp committee.

**Result:** Annual refresh program reduces flight risk; smooths cliff.

## Edge cases / gotchas

- **Pool top-up dilution = founders pay.** Series A investors get the pool top-up; founders absorb dilution. Negotiate size carefully against realistic hiring plan.
- **ISO $100K rule.** Limits ISO grants that can vest in any single year to $100K of FMV. Excess auto-converts to NSO. Carta handles automatically.
- **AMT trap.** ISO exercise triggers AMT on bargain element. Senior employees with large grants exercise during tax planning windows.
- **83(b) election deadline 30 days.** Restricted stock founders must file within 30 days of grant or lose tax-advantaged status.
- **ASC 718 expense flows to IS.** Must accrue evenly over vesting period, even for grants not yet vested. Big number for high-growth SaaS.
- **Carta in-house comp data.** Skewed to Carta-managed cos; not representative of full market.
- **First Round per-employee evergreen.** 25% of new-hire-equivalent each year. Smooths but adds expense.
- **Backdating is fraud.** Always: 409A → board approval → grant date in that order.
- **Refresh denominator drift.** As FD shares grow, % grants for new hires should shrink (Recipe 2 reflects). Don't apply early-stage table to late-stage hires.
- **Acceleration negotiation.** Single-trigger vs double-trigger. Double-trigger market for Series A+.
- **Promotion + grant timing.** Grant on promotion + 1 year later evergreen = grant on promotion AND on tenure. Document policy.
- **Stock-based comp expense is real cash.** Doesn't hit cash flow but does hit P&L (and dilutes via additional shares issued).

> ⚠ **This is informational guidance from an AI agent. Always consult a licensed CFO, CPA, or qualified investment advisor before making binding strategic-finance decisions.**

## Sources

- Holloway Guide equity comp — option pool: https://www.holloway.com/g/equity-compensation/sections/the-option-pool
- The Startup Law Blog equity comp design: https://www.thestartuplawblog.com/blog/equity-compensation-plan-design-startup-guide/
- First Round on grants: https://review.firstround.com/The-Right-Way-to-Grant-Equity-to-Your-Employees
- Compensia evergreen expiration: https://compensia.com/preparing-for-the-expiration-of-an-equity-plan-evergreen-feature/
- Carta equity plan: https://carta.com/learn/equity/equity-plans/
- Pulley equity plan: https://pulley.com
- ASC 718 (Stock Comp): https://asc.fasb.org/topic&trid=2226962
- IRS Sec 422 (ISOs): https://www.irs.gov/forms-pubs/about-form-3921

## Related skills

- `409a-valuation-negotiation` — drives strike price + grant FMV.
- `tax-strategy-qsbs-rd-credit-holdco` — QSBS interaction with grant timing.
- `ipo-readiness-s1-prep` — CD&A disclosure of equity programs.
- `capital-structure-debt-equity-mix-stage` — equity dilution accounting.
- `board-cfo-financial-package` — grant approvals at comp committee.
