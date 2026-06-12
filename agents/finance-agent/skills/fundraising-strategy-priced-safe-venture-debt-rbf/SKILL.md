<!--
Source: https://www.ecaplabs.com/blogs/revenue-based-financing
Source: https://www.recurclub.com/blog/venture-debt-vs-revenue-based-financing
Source: https://www.axisgroupventures.com/post/capital-stack-optimization-how-founders-are-blending-debt-equity-and-secondaries-in-2026
Source: https://www.ycombinator.com/documents
Reference role.md: "Fundraising strategy playbook"
-->

# Fundraising strategy — priced equity vs SAFE vs venture debt vs RBF vs secondaries

Decision tree by stage and revenue posture. 2026 trend: blended capital stack (equity + debt + secondaries) is dominant per Axis Group. Pre-seed/seed → post-money SAFE (YC). Series A+ → priced rounds via NVCA Oct 2025 model. Capital-efficient SaaS with ≥$1M ARR → venture debt 20-35% of last equity round, or revenue-based financing.

## When to use

- Founder asks "what should we raise next, and how much?"
- Pre-fundraise: capital strategy memo (vs alternatives).
- Capital stack design after term sheet received.
- Bridge planning when burn extends runway less than next raise.
- Trigger phrases: "raise strategy", "SAFE vs priced", "venture debt", "RBF", "revenue-based financing", "secondaries", "capital stack", "bridge round".

NOT for: term sheet review (use `term-sheet-nvca-grade-review`); 409A (use `409a-valuation-negotiation`); pitch deck (use `pitch-deck-financial-slides`).

## Setup

```bash
uvx --with pandas --with numpy python -c "import pandas, numpy"

# NVCA Oct 2025 model docs (free)
curl -O https://nvca.org/wp-content/uploads/2019/06/NVCA-Model-Term-Sheet-1.doc

# YC post-money SAFE template (free)
# https://www.ycombinator.com/documents → download "Safe: Valuation Cap, no Discount"
```

## Decision tree by stage

```
PRE-SEED / SEED ($0-$2M ARR)
├─ Capital need < $3M? → Post-money SAFE (YC template)
│   Valuation cap: $8M-$15M typical; rolling close; cheapest legal
├─ Capital need $3M-$8M? → Priced seed (NVCA model)
│   Pre-money $8M-$25M; 1x non-participating preferred; broad-based weighted-avg anti-dilution
└─ Already have $1M+ ARR? → Mix priced + SAFE bridge

SERIES A ($1M-$5M ARR)
├─ Default → Priced equity (NVCA Oct 2025 model)
│   Pre-money $20M-$60M; 1x non-participating pref; weighted-avg anti-dilution
├─ Bridge to next milestone → Convertible note OR extension SAFE
│   YC SAFE w/ valuation cap = current pre + premium; 20-25% discount alt
└─ Capital-efficient ($1M+ ARR, <2× burn multiple) → Add venture debt 20-35% of equity round
    Founderpath, Lighter Capital, Hercules Capital, Bigfoot Capital
    Term: 2-4 years; rate 8-12%; warrants 5-15%

SERIES B+ ($5M+ ARR)
├─ Priced equity (NVCA model)
├─ + Venture debt (if predictable revenue + healthy unit econ)
├─ + RBF for revenue-positive (Capchase, Pipe, Wayflyer for e-com)
└─ + Secondaries for founder + early-employee liquidity (Forge, EquityZen, CrossFlow)

LATE STAGE (>$30M ARR, IPO-track)
├─ Crossover round (mutual funds, hedge funds; e.g. Tiger, Coatue)
├─ Strategic / corp dev round (cash + commercial value)
├─ Pre-IPO secondaries (founder liquidity at lower valuation discount)
└─ Term loan + revolving facility (commercial banks; ARR multiple-based)
```

## Common recipes

### Recipe 1 — Post-money SAFE modeling (YC standard)

```python
def safe_dilution(safe_principal, post_money_cap, series_a_pre_money, series_a_round_size):
    """Post-money SAFE: converts at min(cap, A pre-money) → A round price.
    Conversion shares = safe_principal / conversion_price"""
    series_a_post = series_a_pre_money + series_a_round_size
    conversion_price_per_share_relative = min(post_money_cap, series_a_post) / series_a_post
    # Effective dilution = safe_principal / conversion_price
    safe_ownership_post_a = safe_principal / min(post_money_cap, series_a_post)
    return {
        "safe_ownership_post_a": safe_ownership_post_a,
        "conversion_basis": "cap" if post_money_cap < series_a_post else "pre-money A"
    }

# $2.5M SAFE at $12M post-money cap; converts at $35M pre / $40M post A round
result = safe_dilution(2_500_000, 12_000_000, 35_000_000, 5_000_000)
print(result)  # SAFE holders end up with 20.8% post-A (cap binds)
```

### Recipe 2 — Priced equity round modeling

```python
def priced_round_cap_table(pre_round_shares, raise_amount, pre_money_valuation, option_pool_top_up=0.10):
    """Standard priced round mechanics.
    pre_round_shares: total existing FD shares
    option_pool_top_up: target FD pool size post-close (e.g. 10%); paid by existing holders (pre-money pool shuffle)"""

    pre_money_per_share = pre_money_valuation / pre_round_shares
    new_shares_for_money = raise_amount / pre_money_per_share

    # Option pool top-up shares (pre-money shuffle)
    post_money_shares_pre_pool = pre_round_shares + new_shares_for_money
    target_post_money_pool_shares = post_money_shares_pre_pool * option_pool_top_up / (1 - option_pool_top_up)

    return {
        "pre_money_per_share": pre_money_per_share,
        "new_shares_to_investors": new_shares_for_money,
        "investor_ownership_pct": new_shares_for_money / (pre_round_shares + new_shares_for_money + target_post_money_pool_shares),
        "pool_top_up_shares": target_post_money_pool_shares,
        "post_money_valuation": pre_money_valuation + raise_amount,
    }

# Series A: $10M raise on $30M pre-money; 10M shares outstanding; target 10% pool post-close
print(priced_round_cap_table(10_000_000, 10_000_000, 30_000_000))
```

### Recipe 3 — Venture debt sizing

```python
def venture_debt_sizing(last_equity_round, monthly_revenue, monthly_burn, target_extension_months):
    """Venture debt: rule of thumb = 20-35% of last equity round; lenders cap at 12-18mo extension."""
    pct_of_round = 0.30  # midpoint
    by_round = last_equity_round * pct_of_round

    # Alternative: ARR-multiple-based (typical 0.4-0.7x ARR for SaaS)
    arr = monthly_revenue * 12
    by_arr_mult = arr * 0.55

    # Extension math
    by_extension = monthly_burn * target_extension_months

    return {
        "by_pct_of_last_round": by_round,
        "by_arr_multiple": by_arr_mult,
        "by_runway_extension": by_extension,
        "recommended_max": min(by_round, by_arr_mult, by_extension)
    }

# Just raised $15M Series A; $400K MRR ($4.8M ARR); $450K monthly burn; want 12mo extension
print(venture_debt_sizing(15_000_000, 400_000, 450_000, 12))
```

### Recipe 4 — RBF (revenue-based financing) modeling

```python
def rbf_repayment(loan_amount, monthly_revenue, revenue_share_pct, target_multiple=1.4):
    """RBF: pay back loan_amount × target_multiple via fixed % of monthly revenue."""
    total_repayment = loan_amount * target_multiple
    monthly_payment = monthly_revenue * revenue_share_pct
    months_to_repay = total_repayment / monthly_payment if monthly_payment > 0 else float('inf')
    return {
        "total_repayment": total_repayment,
        "monthly_payment": monthly_payment,
        "months_to_repay": months_to_repay,
        "effective_apr": ((target_multiple ** (12/months_to_repay)) - 1) if months_to_repay else 0
    }

# $2M RBF at 5% monthly revenue share; $400K MRR; 1.4× multiple
print(rbf_repayment(2_000_000, 400_000, 0.05, 1.4))
```

### Recipe 5 — RBF vs venture debt comparison

```python
def compare_rbf_venture_debt(loan_amount, monthly_revenue, monthly_burn):
    rbf = rbf_repayment(loan_amount, monthly_revenue, 0.05, 1.4)
    # Venture debt: $X principal at 9% APR, 3yr term, 36-mo IO + 24-mo amort common
    vd_apr = 0.09
    vd_term_months = 36
    interest_only_months = 12
    monthly_rate = vd_apr / 12
    vd_total_interest_io_period = loan_amount * monthly_rate * interest_only_months
    amort_months = vd_term_months - interest_only_months
    vd_monthly_amort = loan_amount / amort_months + loan_amount * monthly_rate
    return {
        "RBF": rbf,
        "VD": {
            "monthly_payment_IO_period": loan_amount * monthly_rate,
            "monthly_payment_amort_period": vd_monthly_amort,
            "total_interest_36mo_approx": vd_total_interest_io_period + (vd_monthly_amort - loan_amount/amort_months) * amort_months,
        }
    }

# Compare $2M instrument at $400K MRR
print(compare_rbf_venture_debt(2_000_000, 400_000, 450_000))
```

### Recipe 6 — Bridge round design

```python
def bridge_round_design(current_runway_months, target_milestone_months, monthly_burn, current_post_money_valuation):
    """Bridge to next milestone (typically Series A/B)."""
    gap_months = target_milestone_months - current_runway_months
    bridge_amount = max(0, gap_months * monthly_burn * 1.3)  # 30% buffer

    # SAFE structure for bridge: 20-25% discount + uncapped or premium cap
    discount_pct = 0.20
    return {
        "bridge_amount": bridge_amount,
        "gap_months": gap_months,
        "structure": "Post-money SAFE w/ 20% discount + cap at current_post_money × 1.25",
        "cap": current_post_money_valuation * 1.25,
        "discount": discount_pct,
    }

print(bridge_round_design(8, 14, 350_000, 25_000_000))
```

### Recipe 7 — Capital stack visualizer

```python
def capital_stack_2026(stage_arr, monthly_burn, last_round_post_money):
    """Recommend blended stack."""
    rec = {}
    if stage_arr < 1_000_000:
        rec = {"equity": 1.0, "venture_debt": 0, "rbf": 0, "secondaries": 0}
    elif stage_arr < 5_000_000:
        rec = {"equity": 0.80, "venture_debt": 0.15, "rbf": 0.05, "secondaries": 0}
    elif stage_arr < 30_000_000:
        rec = {"equity": 0.65, "venture_debt": 0.25, "rbf": 0.05, "secondaries": 0.05}
    else:
        rec = {"equity": 0.55, "venture_debt": 0.30, "rbf": 0.05, "secondaries": 0.10}
    return rec
```

### Recipe 8 — Raise sizing (LTV:CAC × milestone gap)

```python
def raise_sizing(current_runway_mo, target_runway_post_raise_mo, monthly_burn, next_milestone_months):
    """Default: cover to next milestone + 6mo runway buffer."""
    target_months_post_raise = next_milestone_months + 6
    raise_amount_default = (target_months_post_raise * monthly_burn)
    return {
        "raise_amount": raise_amount_default,
        "target_runway_months_post": target_months_post_raise,
        "rationale": "next milestone + 6mo buffer"
    }

print(raise_sizing(8, 24, 420_000, 18))
```

## Examples

### Example 1: Series A founder asks "should we raise $10M or $15M?"

**Goal:** Right-size the raise.

**Steps:**
1. Recipe 8 → milestone-based sizing; next milestone is $5M ARR (currently $1.5M); 24mo to get there at planned burn.
2. Recipe 2 → priced round mechanics; show dilution at $30M / $35M / $40M pre-money.
3. Recipe 7 → capital stack; consider $12M equity + $3M venture debt blend.
4. Recipe 3 → venture debt sizing within healthy range.
5. Compare dilution: $15M equity (~30% dilution) vs $12M + $3M VD (~24% equity dilution + interest).

**Result:** Memo recommending $12M priced + $3M venture debt; saves 6pp dilution.

### Example 2: $2M bridge to Series B

**Goal:** Bridge cash runway from 8mo to 14mo for Series B.

**Steps:**
1. Recipe 6 → bridge design; need ~$2.4M with 30% buffer.
2. SAFE structure: post-money SAFE w/ 20% discount, cap at current post-money × 1.25.
3. Compare against RBF (Recipe 4) for revenue-positive case.
4. Compare against extension venture debt from existing lender (Recipe 5).
5. Pick: SAFE if dilution-tolerant and Series B is near; venture debt extension if relationship is strong.

**Result:** $2.4M post-money SAFE bridge with 20% discount + cap at $31.25M post.

## Edge cases / gotchas

- **Post-money SAFE dilutes MORE than pre-money SAFE.** Investors get fixed % of post-money; founders absorb future SAFE conversions. Model carefully.
- **Option pool top-up = pre-money dilution.** Founders pay; investors don't. Negotiate target pool size against grants needed in next 12-18mo (avoid over-sizing).
- **Venture debt covenants.** Most lenders require MRR floor, cash floor, no material adverse change clause. Read carefully (use `term-sheet-nvca-grade-review` + `legal-counsel`).
- **RBF effective APR.** Recipe 4's "effective APR" assumes constant revenue; actual APR varies with growth. RBF is cheap for slow growth, expensive for fast.
- **Warrants on venture debt.** 5-15% of loan amount in warrants. Adds ~50-200bps to effective cost. Model in.
- **Secondaries hit cap-table dynamics.** Most preferred holders have ROFR (right of first refusal); transactions can stall.
- **Crossover rounds (mutual funds).** Bring liquidation prefs, registration rights, ratchets. Read terms carefully.
- **Bridge rounds signal weakness.** If bridge is from existing investors only, OK. If you need new lead → problem.
- **YC SAFE != "standard."** Specifically the post-money valuation cap version. Lots of pre-money SAFEs floating around; verify.
- **NVCA Oct 2025 update.** Tranched financings now formally addressed in SPA Annex; milestone-based tranches normalized.

> ⚠ **This is informational guidance from an AI agent. Always consult a licensed CFO, CPA, or qualified investment advisor before making binding strategic-finance decisions.**

## Sources

- ECL revenue-based financing 2026: https://www.ecaplabs.com/blogs/revenue-based-financing
- Recur Club venture debt vs RBF: https://www.recurclub.com/blog/venture-debt-vs-revenue-based-financing
- Axis Group capital stack 2026: https://www.axisgroupventures.com/post/capital-stack-optimization-how-founders-are-blending-debt-equity-and-secondaries-in-2026
- YC SAFE documents: https://www.ycombinator.com/documents
- NVCA Model Term Sheet (Oct 2025): https://nvca.org/wp-content/uploads/2019/06/NVCA-Model-Term-Sheet-1.doc
- Foley NVCA Oct 2025 breakdown: https://www.foley.com/insights/publications/2025/10/breaking-down-the-nvca-what-founders-and-vcs-need-to-know/
- Founderpath: https://founderpath.com
- Capchase: https://www.capchase.com
- Forge Global: https://forgeglobal.com
- EquityZen: https://equityzen.com

## Related skills

- `term-sheet-nvca-grade-review` — review the term sheet for the round.
- `409a-valuation-negotiation` — sets common share value post-round.
- `capital-structure-debt-equity-mix-stage` — overall stack.
- `pitch-deck-financial-slides` — deck for the raise.
- `investor-data-room-curation` — data room for diligence.
